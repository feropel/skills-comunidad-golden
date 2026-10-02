#!/usr/bin/env python3
"""
consolidar_mercado.py — cuánto ha vendido DE VERDAD un producto en un país y cuántos
proveedores reales lo tienen, a partir de lo que devuelve DropKiller.

Por qué existe (medido 2026-09-18):
1. La regla de Juan Vargas (cofundador de DropKiller) es "sumar las ventas de TODOS los
   proveedores del mismo producto". Aplicada al pie de la letra CUENTA DOBLE: DropKiller
   lista el MISMO producto de Dropi varias veces, una por cada plataforma que lo refleja
   (DROPI, WINPY, DROPLATAM, SEVENTY_BLOCK), con el mismo externalId, el mismo proveedor y
   el mismo historial de stock. Dr. Melaxin salía 4 veces: sumarlas daba ~37.000 ventas
   de un solo proveedor.
2. Un mismo proveedor con dos fichas distintas es UN proveedor (se suman sus ventas, se
   cuenta una vez).
3. La búsqueda por imagen trae productos PARECIDOS que no son el mismo (el spray "peel shot"
   al buscar la crema). Por eso se filtra por nombre con --incluir (regex) y lo decide quien
   mira las fotos, no el script.

Regla de la casa (GPG1.16, tras el verificador adversarial): un DATO QUE FALTA nunca aprueba.
Si falta createdAt, stock, proveedor o externalId, el script elige la opción conservadora y
lo dice en "avisos". Un mercado vacío no pasa ningún criterio.

Entrada: JSON de semantic_search_products o search_products ({"data":[...]}).
Uso:
  python3 consolidar_mercado.py resp.json --pais CO --incluir "probador de inyectores"
        [--etapa VALIDACION|NUEVO|ESCALADO]   etapa que el usuario eligió en el menú (5)
        [--max-proveedores N]                 tope que el usuario eligió en el menú (8)
  python3 consolidar_mercado.py --autoprueba
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402  (una sola forma de normalizar IDs, nombres, números y fechas)

# Etapas del producto por ventas TOTALES sumadas en el país. Fuente: Juan Vargas,
# video hYpcanJ12fU (08-ago-2026), "las etapas que yo he podido deducir": son HEURÍSTICA de
# un practicante, no una medida publicada. Los huecos que él no define (CO 5.000–8.000,
# EC 4.500–6.000, GT 3.000–5.000) se asignan a ESCALADO y se declara.
ETAPAS = {
    "CO": [(100, "NUEVO"), (3000, "VALIDACION"), (8000, "ESCALADO"), (15000, "SATURACION")],
    "EC": [(90, "NUEVO"), (2000, "VALIDACION"), (6000, "ESCALADO"), (10000, "SATURACION")],
    "GT": [(80, "NUEVO"), (1000, "VALIDACION"), (5000, "ESCALADO"), (8000, "SATURACION")],
}
# Máximo de proveedores para seguir considerándolo poco competido. Fuente: curso gEQbjW7-2HY
# (CO <5, MX 3–4, GT 2) y clase y-OWDawyb2c (PE/GT 1–2). El usuario puede cambiarlo en el
# menú (pregunta 8) con --max-proveedores.
MAX_PROVEEDORES = {"CO": 5, "MX": 4, "GT": 2, "PE": 2}
DIAS_PARA_INACTIVO = 30  # ficha sin verse en 30 días = eliminada o privatizada: no cuenta como proveedor activo
ETAPAS_PEDIBLES = ("NUEVO", "VALIDACION", "ESCALADO")


class ErrorDeEntrada(Exception):
    pass


def num(x):
    """Unidades como entero. Acepta int, float y texto con dígitos ("1.193", "1193").
    Devuelve None si no hay número: el que llama decide y lo avisa."""
    v = comun.numero(x)
    # Negativo, fraccionario, NaN o texto no son unidades: dato roto, se devuelve None y se avisa.
    if v is None or v < 0 or not float(v).is_integer():
        return None
    return int(v)


def fecha(iso):
    """Fecha con zona. Una fecha sin zona se toma como UTC (DropKiller no la manda en createdAt)."""
    if not isinstance(iso, str) or not iso:
        return None
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def etapa(pais, total):
    tabla = ETAPAS.get(pais)
    aviso = None
    if tabla is None:
        tabla = ETAPAS["CO"]
        aviso = "no hay tabla de etapas para %s: se aplicó la de Colombia (declararlo, puede sobrestimar la holgura en mercados chicos)" % pais
    for techo, nombre in tabla:
        if total < techo:
            return nombre, aviso
    return "QUEMADO", aviso


def consolidar(filas, pais, incluir=None, hoy=None, etapa_pedida="VALIDACION", max_proveedores=None):
    hoy = hoy or datetime.now(timezone.utc)
    if filas is None or not isinstance(filas, list):
        raise ErrorDeEntrada("la respuesta no trae una lista de productos (data vacío o null)")
    try:
        patron = re.compile(incluir, re.I) if incluir else None
    except re.error as e:
        raise ErrorDeEntrada("--incluir no es una expresión válida: %s" % e)
    avisos = []
    excluidas = []
    candidatas = []
    no_registro = 0
    for f in filas:
        # 🔴 P59, segunda mitad (2026-09-28): lo que se descarta se CUENTA y se NOMBRA. Antes esta
        # rama tiraba en silencio las filas que no son registros de producto: `filas_recibidas` SÍ
        # las incluía y ningún campo las contaba, así que el total no cuadraba y nadie tenía con
        # qué notarlo. Un descarte que no se cuenta no es un filtro, es una fuga.
        if not isinstance(f, dict):
            no_registro += 1
            continue
        nombre = (f.get("name") or "").strip()
        if patron and not patron.search(nombre):
            excluidas.append(nombre)
            continue
        candidatas.append(f)
    if no_registro:
        avisos.append("%d fila(s) de la respuesta no son registros de producto: "
                      "descartadas y contadas" % no_registro)

    # 1) colapsar espejos: mismo externalId = mismo producto de Dropi en otra plataforma.
    #    Una fila SIN externalId ni id no puede ser espejo de nada: va sola.
    grupos = {}
    sin_id = 0
    for i, f in enumerate(candidatas):
        clave = comun.ident(f.get("externalId")) or comun.ident(f.get("id"))
        if not clave:
            sin_id += 1
            clave = "_sin_id_%d" % i
        grupos.setdefault(str(clave), []).append(f)
    if sin_id:
        avisos.append("%d ficha(s) sin externalId ni id: cada una se contó como producto aparte" % sin_id)

    por_ext = {}
    for clave, filas_g in grupos.items():
        for f in filas_g:
            f["_u"] = num(f.get("totalSoldUnits"))
        malas = [f for f in filas_g if f["_u"] is None]
        if malas:
            avisos.append("espejo(s) de %s sin totalSoldUnits legible: se tomaron como 0" % clave)
            for f in malas:
                f["_u"] = 0
        # Un espejo en 0 junto a otros con ventas es una lectura perdida, no un dato: fuera.
        con_venta = [f for f in filas_g if f["_u"] > 0]
        if con_venta and len(con_venta) < len(filas_g):
            avisos.append("espejo(s) de %s en 0 junto a otros con ventas: descartados como lectura perdida" % clave)
            filas_g = con_venta
        ordenadas = sorted(filas_g, key=lambda x: x["_u"])
        bajo, alto = ordenadas[0]["_u"], ordenadas[-1]["_u"]
        if len(ordenadas) == 1 or bajo == alto or (bajo > 0 and alto / bajo <= 1.3):
            elegido = ordenadas[-1]  # cuadran: el más alto solo corrige lecturas perdidas
        else:
            # No cuadran. Medido 2026-09-18 en el brasier reafirmante: DROPI 2.324 contra
            # WINPY y DROPLATAM 1.193; tomar el máximo inflaba el mercado al doble.
            fechas = [fecha(f.get("createdAt")) for f in ordenadas]
            # El alto solo se cree si TODOS traen fecha y el alto es el más viejo por >7 días
            # (tablero LED de impor house: DROPI de nov-2025 con 1.981, legítimo). Con una fecha
            # que falta no se puede comprobar, y un dato que falta nunca aprueba.
            todas = all(fechas)
            alto_es_viejo = todas and all((fechas[i] - fechas[-1]).days > 7 for i in range(len(ordenadas) - 1))
            if alto_es_viejo:
                elegido = ordenadas[-1]
                avisos.append("espejos de %s no cuadran (%d a %d) pero el alto es el más viejo: se tomó %d"
                              % (clave, bajo, alto, alto))
            else:
                if len(ordenadas) == 2:
                    elegido = ordenadas[0]
                    como = "el menor (con dos espejos no hay mediana: se toma el conservador)"
                else:
                    elegido = ordenadas[len(ordenadas) // 2]
                    como = "la mediana"
                avisos.append("espejos de %s no cuadran (%d a %d): se tomó %d, %s%s"
                              % (clave, bajo, alto, elegido["_u"], como,
                                 "" if todas else " (faltó createdAt en algún espejo: no se pudo ver si el alto es el más viejo)"))
        por_ext[clave] = elegido
    espejos = len(candidatas) - len(por_ext)

    # 2) agrupar por proveedor: un proveedor con dos fichas es uno solo. Sin nombre no se
    #    puede saber si dos fichas son del mismo: cada una cuenta aparte (lo conservador).
    proveedores = {}
    sin_nombre = sin_stock = 0
    for clave, f in por_ext.items():
        prov_crudo = f.get("providerName") or (f.get("provider") if isinstance(f.get("provider"), dict) else {}).get("name")
        prov = comun.clave(prov_crudo)
        if not prov:
            sin_nombre += 1
            prov = "(sin nombre, ficha %s)" % clave
        d = fecha(f.get("lastSeenAt"))
        dias = (hoy - d).days if d else None
        stock = num(f.get("stock"))
        if stock is None:
            sin_stock += 1
            con_stock = True  # sin dato de stock se cuenta como activo: nunca baja el conteo de competencia
        else:
            con_stock = stock > 0
        # Solo un INACTIVE o BLOCKED explícito apaga al proveedor: status vacío, None o "active"
        # en minúscula es activo (un dato que falta nunca baja la competencia: verificador).
        activa = comun.clave(f.get("status")) not in ("inactive", "blocked") and (dias is None or dias <= DIAS_PARA_INACTIVO) and con_stock
        p = proveedores.setdefault(prov, {"fichas": 0, "ventas": 0, "activa": False, "stock": 0})
        p["fichas"] += 1
        p["ventas"] += f["_u"]
        p["activa"] = p["activa"] or activa
        if activa:
            p["stock"] += stock or 0
    if sin_nombre:
        avisos.append("%d ficha(s) sin nombre de proveedor: cada una se contó como proveedor distinto" % sin_nombre)
    if sin_stock:
        avisos.append("%d ficha(s) sin dato de stock: se contaron como proveedor activo" % sin_stock)

    total = sum(p["ventas"] for p in proveedores.values())
    activos = sorted([k for k, p in proveedores.items() if p["activa"]])
    nombre_etapa, aviso = etapa(pais, total)
    if aviso:
        avisos.insert(0, aviso)
    tope = max_proveedores if max_proveedores is not None else MAX_PROVEEDORES.get(pais)
    if tope is None:
        tope = MAX_PROVEEDORES["CO"]
        avisos.append("no hay tope de proveedores para %s: se aplicó el de Colombia (%d), que también es heredado y sin verificar" % (pais, tope))

    vacio = not por_ext
    if vacio:
        avisos.append("ninguna ficha quedó para evaluar (mercado vacío o --incluir no casó nada): no se concluye nada, ni a favor ni en contra")
    # Criterio 1 del método: de 100 ventas al techo de VALIDACIÓN. Se reporta siempre, y
    # aparte si la etapa es la que el usuario pidió en el menú (NUEVO = riesgo, no validado;
    # ESCALADO = solo para importar y competir por precio).
    # Una ficha sin cifra de ventas legible puede esconder un mercado ya quemado: con ese dato
    # faltando, la etapa NO se puede asegurar y los criterios de etapa no aprueban.
    etapa_incierta = any("sin totalSoldUnits legible" in a for a in avisos)
    if etapa_incierta:
        avisos.append("etapa NO asegurada: hay fichas sin cifra de ventas; el criterio 1 no aprueba hasta leerlas")
    criterio_ventas = (not vacio) and not etapa_incierta and nombre_etapa == "VALIDACION" and total >= 100
    etapa_ok = (not vacio) and not etapa_incierta and nombre_etapa == etapa_pedida
    if etapa_pedida == "NUEVO" and etapa_ok:
        avisos.append("etapa NUEVO pedida: menos de 100 ventas, no cumple el criterio 1 (sin validar, marcarlo)")
    criterio_proveedores = (not vacio) and len(activos) <= tope
    for f in candidatas:
        f.pop("_u", None)
    return {
        "pais": pais,
        "filas_recibidas": len(filas),
        "no_son_registros": no_registro,
        "excluidas_por_nombre": len(excluidas),
        "cuadre": "recibidas %d = no_registros %d + excluidas_por_nombre %d + candidatas %d" % (
            len(filas), no_registro, len(excluidas), len(candidatas)),
        "espejos_descartados": espejos,
        "fichas_unicas": len(por_ext),
        "proveedores_activos": len(activos),
        "proveedores": {k: v for k, v in sorted(proveedores.items(), key=lambda x: -x[1]["ventas"])},
        "ventas_totales_mercado": total,
        "etapa": nombre_etapa,
        "etapa_pedida": etapa_pedida,
        "etapa_es_la_pedida": etapa_ok,
        "criterio_1_ventas_100_a_validacion": criterio_ventas,
        "criterio_2_pocos_proveedores": criterio_proveedores,
        "tope_proveedores": tope,
        "avisos": avisos + ["el criterio 3 (pocos anunciantes POR CANAL) no sale de aquí: se mide en la biblioteca de anuncios"],
    }


def autoprueba():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "banco_consolidacion.json")
    if not os.path.exists(ruta):
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco_consolidacion.json")
    banco = json.load(open(ruta, encoding="utf-8"))
    hoy = datetime(2026, 9, 18, 23, 59, tzinfo=timezone.utc)
    fallos = 0
    for nombre, caso in banco["casos"].items():
        r = consolidar(caso["data"], caso.get("_pais", "CO"), caso.get("_incluir"), hoy,
                       caso.get("_etapa", "VALIDACION"), caso.get("_max_proveedores"))
        for k, v in caso["_esperado"].items():
            if k == "_aviso_contiene":
                if not any(v in a for a in r["avisos"]):
                    fallos += 1
                    print("FALLA %s · ningún aviso contiene %r" % (nombre, v))
            elif r[k] != v:
                fallos += 1
                print("FALLA %s · %s: esperado %s, salió %s" % (nombre, k, v, r[k]))
    total = sum(len(c["_esperado"]) for c in banco["casos"].values())
    print("AUTOPRUEBA %d de %d" % (total - fallos, total))
    return 1 if fallos else 0


def valor(bandera):
    i = sys.argv.index(bandera)
    if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
        raise ErrorDeEntrada("%s necesita un valor" % bandera)
    return sys.argv[i + 1]


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    try:
        try:
            datos = json.load(open(sys.argv[1], encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise ErrorDeEntrada("no se pudo leer %s: %s" % (sys.argv[1], e))
        filas = datos.get("data") if isinstance(datos, dict) else datos
        pais = valor("--pais").upper() if "--pais" in sys.argv else "CO"
        incluir = valor("--incluir") if "--incluir" in sys.argv else None
        etapa_pedida = comun.clave(valor("--etapa")).upper() if "--etapa" in sys.argv else "VALIDACION"
        if etapa_pedida not in ETAPAS_PEDIBLES:
            raise ErrorDeEntrada("--etapa debe ser una de %s" % ", ".join(ETAPAS_PEDIBLES))
        tope = None
        if "--max-proveedores" in sys.argv:
            tope = num(valor("--max-proveedores"))
            if tope is None:
                raise ErrorDeEntrada("--max-proveedores debe ser un entero de 0 en adelante (vino %r)" % valor("--max-proveedores"))
        print(json.dumps(consolidar(filas, pais, incluir, None, etapa_pedida, tope), ensure_ascii=False, indent=1))
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 — cualquier forma rara del JSON: error controlado, no traza
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
