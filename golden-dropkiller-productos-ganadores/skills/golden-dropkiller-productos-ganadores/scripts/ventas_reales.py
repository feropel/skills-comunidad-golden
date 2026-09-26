#!/usr/bin/env python3
"""
ventas_reales.py — separa ventas REALES de AJUSTES DE INVENTARIO en el historial de DropKiller.

Por qué existe (medido 2026-09-18, top 20 de find_winning_products en Dropi Colombia):
DropKiller deriva las "ventas" de la CAÍDA DEL STOCK del proveedor (probador de inyectores:
500 − 378 = 122 vendidos, exacto). Cuando un proveedor vacía o corrige su inventario, esa
caída se cuenta como venta. 9 de los 20 "ganadores" eran eso: una sola caída gigante
(virex 3.000 → 300 = "2.700 vendidos"), casi siempre con el stock final en 1 o un número
redondo, y con días sin lectura justo antes.

Entrada: JSON con la respuesta de get_product_history ({"data":[...]}), un producto de
semantic_search_products (trae "history30d") o una lista de filas [fecha, stock, soldUnits,
salePrice]. Uso:
  python3 ventas_reales.py historial.json            # un producto
  python3 ventas_reales.py banco.json --banco        # {"productos":{nombre:{"h":[...]}}}
  python3 ventas_reales.py --autoprueba              # los 41 casos de assets/
Salida: JSON con veredicto REAL / FANTASMA / DUDOSO / SIN_VENTAS / SIN_DATOS y las ventas
DEPURADAS, que son las que van a la ficha (nunca las reportadas por DropKiller).
Solo usa la biblioteca estándar de Python 3.
"""
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

# Umbrales. Cada uno sale de un caso medido, no de una preferencia.
DIAS_CON_VENTA_MIN = 3      # juan (PY7sFAKQAOQ): "22 ventas en un solo día = no acertadas"; exige constancia
PICO_FACTOR = 5             # sebo de res: día de 1.326 contra una mediana de ~130 = ajuste dentro de un producto real
PICO_FACTOR_HUECO = 3       # tras ≥3 días sin lectura el ritmo ya viene diluido por el hueco (verificador, 2026-09-18)
CAIDAS_IGUALES_MIN = 4      # 4+ caídas idénticas de ≥20 = descarga por lotes, no ventas de clientes (verificador: 8 × 70)
CUOTA_UN_DIA_FANTASMA = 0.6 # si un solo día explica ≥60% de todo lo vendido y hay <3 días con venta = fantasma


def normalizar(entrada):
    """Devuelve filas [fecha, stock, vendidos, precio] ordenadas por fecha.

    Acepta los dos formatos del MCP: get_product_history ({"data":[{date, stock, soldUnits,
    salePrice}]}) y el history30d que traen search/semantic_search ([{d, s, u, p}]).
    Descarta los días SIN LECTURA: DropKiller rellena con stock 0, precio 0 y ventas 0 los
    días anteriores a la creación del producto y el día en curso (medido 2026-09-18; Naider
    Ortiz lo describe como "un delay de 2–3 días"). Tomados como lectura real, un producto sano
    parecía vaciado en stock 0 al final.
    """
    if isinstance(entrada, dict) and "data" in entrada:
        crudas, llaves = entrada["data"], ("date", "stock", "soldUnits", "salePrice")
    elif isinstance(entrada, dict) and "history30d" in entrada:
        crudas, llaves = entrada["history30d"], ("d", "s", "u", "p")
    elif isinstance(entrada, dict) and "h" in entrada:
        crudas, llaves = entrada["h"], None
    else:
        crudas, llaves = entrada, None
    if not isinstance(crudas, list):
        raise ErrorDeEntrada("el historial no es una lista (vino %s)" % type(crudas).__name__)
    filas = []
    for i, d in enumerate(crudas):
        if llaves and isinstance(d, dict):
            u = d.get(llaves[2])
            fila = [d.get(llaves[0]), d.get(llaves[1]), 0 if u is None else u, d.get(llaves[3])]  # False no es 0: se rechaza abajo
        elif isinstance(d, (list, tuple)) and len(d) >= 4:
            fila = list(d[:4])
        else:
            raise ErrorDeEntrada("fila %d ilegible: se esperaba {fecha, stock, vendidas, precio} y vino %r" % (i, d))
        iso = comun.fecha_iso(fila[0]) if isinstance(fila[0], str) else None
        if not iso:
            raise ErrorDeEntrada("fila %d sin fecha legible (vino %r)" % (i, fila[0]))
        fila[0] = iso  # DD-MM-AAAA ordenado como texto quedaba desordenado: todo pasa a AAAA-MM-DD
        for j in (1, 2, 3):
            x = fila[j]
            if x is not None and (isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)):
                raise ErrorDeEntrada("fila %d (%s): valor no numérico %r" % (i, fila[0], x))
        filas.append(fila)
    reales = [f for f in filas if not (not f[1] and not f[2] and not f[3])]
    # Dos filas del mismo día contaban las ventas dos veces (340 en vez de 170: verificador).
    # Se queda la ÚLTIMA lectura de cada día y se cuenta cuántas se descartaron.
    por_dia = {}
    for f in reales:
        por_dia[f[0]] = f
    # El conteo viaja CON las filas (antes era un contador global que pasaba a otro evaluar()).
    salida = Filas(sorted(por_dia.values(), key=lambda f: f[0]))
    salida.duplicadas = len(reales) - len(por_dia)
    return salida


class Filas(list):
    duplicadas = 0


class ErrorDeEntrada(Exception):
    pass


def reabastecimientos(filas):
    """Cuántas veces SUBIÓ el stock en la ventana. Juan Vargas (clase y-OWDawyb2c) lo quiere y
    reconoce que DropKiller no lo muestra: un proveedor que reabastece ya tiene dropshippers
    vendiéndole el producto. Sube = crece más de 10% y al menos 20 unidades sobre la lectura
    anterior (los vaivenes chicos son devoluciones que vuelven a bodega)."""
    n = 0
    for a, b in zip(filas, filas[1:]):
        if a[1] is not None and b[1] is not None and b[1] - a[1] >= max(20, 0.1 * (a[1] or 1)):
            n += 1
    return n


def evaluar(filas):
    if not filas:
        return {"veredicto": "SIN_DATOS", "motivos": ["historial vacío: no concluir"]}
    dup = getattr(filas, "duplicadas", 0)
    # Una venta negativa no existe: es stock que VOLVIÓ (devolución o corrección). Se cuenta
    # como 0 y se avisa; sumada, daba ventas depuradas negativas (verificador, 2026-09-18).
    negativas = [f[0] for f in filas if (f[2] or 0) < 0]
    if negativas:
        filas = [[f[0], f[1], max(f[2] or 0, 0), f[3]] for f in filas]
    resultado = _evaluar(filas)
    if negativas:
        resultado.setdefault("motivos", []).append(
            "%d día(s) con ventas negativas (stock que volvió) contados como 0: %s" % (len(negativas), ", ".join(negativas[:5])))
    if dup:
        resultado.setdefault("motivos", []).append("%d fila(s) repetidas del mismo día descartadas (se usó la última lectura)" % dup)
    resultado["reabastecimientos"] = reabastecimientos(filas)
    resultado.update(aceleracion(filas, resultado))
    return resultado


def aceleracion(filas, resultado):
    """Pendiente, no nivel: el ganador se caza en la SUBIDA (propuesta del chat par, 2026-09-18).
    Compara lo vendido en los últimos 7 días del historial con el promedio semanal de la ventana
    DEPURADA. >1,3 = acelerando · 0,7–1,3 = estable · <0,7 = frenando. Si el historial es de
    menos de 14 días no hay contra qué comparar y se dice."""
    from datetime import date, timedelta
    try:
        fin = date.fromisoformat(filas[-1][0][:10])
        ini = date.fromisoformat(filas[0][0][:10])
    except ValueError:
        return {"aceleracion": None, "tendencia": "sin fechas legibles"}
    corte = (fin - timedelta(days=6)).isoformat()
    dep_filas = resultado.pop("_dep_filas", None) or [max(f[2] or 0, 0) for f in filas]
    v7 = sum(d for f, d in zip(filas, dep_filas) if f[0][:10] >= corte)  # depuradas: un pico recortado no acelera
    dias = (fin - ini).days + 1
    dep = resultado.get("vendidas_depuradas")
    if dias < 14 or not dep:
        return {"ventas_7d": v7, "aceleracion": None, "tendencia": "historial corto: sin comparación"}
    semanal = dep / dias * 7
    a = round(v7 / semanal, 2) if semanal else None
    t = "acelerando" if a and a > 1.3 else ("frenando" if a is not None and a < 0.7 else "estable")
    return {"ventas_7d": v7, "promedio_semanal": round(semanal, 1), "aceleracion": a, "tendencia": t}


def _evaluar(filas):
    ventas = [f[2] for f in filas]
    total = sum(ventas)
    dias_venta = [v for v in ventas if v > 0]
    motivos = []
    if total == 0:
        return {"veredicto": "SIN_VENTAS", "vendidas_reportadas": 0, "vendidas_depuradas": 0,
                "dias_con_venta": 0, "motivos": ["cero ventas en la ventana"]}

    mayor = max(ventas)
    idx_mayor = ventas.index(mayor)
    cuota_mayor = mayor / total
    stock_final = filas[-1][1]

    # Días transcurridos desde la lectura anterior: DropKiller no lee todos los días, y lo
    # vendido en un hueco de 5 días aparece de golpe en una sola fila (caso A3 del banco).
    def dias_desde_previa(i):
        if i == 0:
            return 1
        try:
            from datetime import date
            a = date.fromisoformat(filas[i - 1][0][:10])
            b = date.fromisoformat(filas[i][0][:10])
            return max((b - a).days, 1)
        except ValueError:
            return 1
    ritmos = [v / dias_desde_previa(i) for i, v in enumerate(ventas)]

    # Señales de ajuste de inventario en el día de la caída mayor
    dia = filas[idx_mayor]
    previo = filas[idx_mayor - 1] if idx_mayor > 0 else None
    senales = []
    # "Stock final en 1" solo acusa si la caída fue grande: un producto lento que agota sus
    # últimas 5 unidades también termina en 1 (verificador, caso 6 → 5 → 1).
    if stock_final is not None and stock_final <= 1 and mayor >= 20:
        senales.append("stock final en %s" % stock_final)
    if previo and previo[3] is not None and dia[3] is not None and previo[3] != dia[3]:
        senales.append("el precio cambió el mismo día de la caída (%s → %s)" % (previo[3], dia[3]))
    if mayor >= 100 and mayor % 100 == 0:
        senales.append("caída en número redondo (%s)" % mayor)
    if previo and previo[1] and dia[1] is not None and previo[1] >= 100 and dia[1] / previo[1] <= 0.15:
        senales.append("el stock se desplomó %s → %s en una lectura" % (previo[1], dia[1]))

    # 1) Casi todo en un día y sin constancia. Se llama FANTASMA solo si la caída es grande
    #    (≥100) o trae señal de ajuste; si no, no está probado que sea falso: DUDOSO (caso A1:
    #    un producto lento con 3 y 2 ventas no es un vaciado de inventario).
    if len(dias_venta) < DIAS_CON_VENTA_MIN and cuota_mayor >= CUOTA_UN_DIA_FANTASMA:
        motivos.append("%d de %d unidades (%.0f%%) en un solo día (%s) y solo %d día(s) con venta"
                       % (mayor, total, cuota_mayor * 100, dia[0], len(dias_venta)))
        motivos += senales
        if mayor >= 100 or senales:
            return {"veredicto": "FANTASMA", "vendidas_reportadas": total, "vendidas_depuradas": 0,
                    "dias_con_venta": len(dias_venta), "motivos": motivos}
        motivos.append("caída chica y sin señal de ajuste: no probado falso, tampoco validado")
        return {"veredicto": "DUDOSO", "vendidas_reportadas": total, "vendidas_depuradas": total,
                "dias_con_venta": len(dias_venta), "motivos": motivos}

    # 2) Producto con venta en varios días: recortar picos que son ajustes.
    #    La línea base es la mediana del RITMO diario sin el 20% más alto: si el vaciado se
    #    partió en dos lecturas, la mediana simple se contamina y deja pasar el ajuste (caso A2).
    ritmos_venta = sorted(r for r in ritmos if r > 0)
    quitar = -(-len(ritmos_venta) // 5)  # techo del 20%
    base_lista = ritmos_venta[:-quitar] if len(ritmos_venta) - quitar >= 1 else ritmos_venta
    mediana = statistics.median(base_lista)
    depuradas = 0
    dep_filas = []  # lo depurado día por día: la aceleración lo necesita sin los picos
    picos = []
    dias_normales = 0
    for i, (f, v) in enumerate(zip(filas, ventas)):
        d = dias_desde_previa(i)
        # Tras un hueco de lectura de 3 días o más, el ritmo ya viene promediado por el hueco:
        # un vaciado de 300 en 15 días sin lectura da 20/día contra una base de 5 y pasaba
        # entero (verificador). Ahí basta con 3 veces la base.
        factor = PICO_FACTOR_HUECO if d >= 3 else PICO_FACTOR
        if ritmos[i] > factor * mediana and v >= 50:
            picos.append("%s: %d en %d día(s) (base %.0f/día)" % (f[0], v, d, mediana))
            depuradas += int(round(mediana * d))
            dep_filas.append(int(round(mediana * d)))
        else:
            depuradas += v
            dep_filas.append(v)
            if v > 0:
                dias_normales += 1
    if picos:
        motivos.append("picos recortados al ritmo base: " + "; ".join(picos))
        recortado = 1 - depuradas / total
        if recortado >= 0.8 and dias_normales < DIAS_CON_VENTA_MIN:
            motivos.append("%.0f%% de lo reportado era ajuste y quedan %d día(s) de venta normal"
                           % (recortado * 100, dias_normales))
            motivos += senales
            return {"veredicto": "FANTASMA", "vendidas_reportadas": total, "vendidas_depuradas": depuradas,
                    "dias_con_venta": len(dias_venta), "motivos": motivos}

    # Un vaciado repartido en lotes iguales (8 caídas de 70 exactas) tiene "constancia" y
    # engaña a la mediana. Clientes reales no compran la misma cantidad exacta día tras día.
    from collections import Counter
    iguales = Counter(v for v in ventas if v >= 20).most_common(1)
    lotes = iguales[0] if iguales and iguales[0][1] >= CAIDAS_IGUALES_MIN else None
    if lotes:
        # Solo acusa si los lotes están MUY por encima del resto de días con venta (el caso del
        # verificador: lotes de 70 contra días de 2). Un producto de ritmo parejo, sin otros
        # días que contrasten, no se puede distinguir y no se condena (casos A3, A8 del banco).
        otros = [v for v in ventas if v > 0 and v != lotes[0]]
        if len(otros) < 2 or max(otros) >= 0.25 * lotes[0]:
            lotes = None

    if dias_normales < DIAS_CON_VENTA_MIN:
        veredicto = "DUDOSO"
        motivos.append("solo %d día(s) con venta: pocos datos para confirmar constancia" % len(dias_venta))
    elif lotes:
        veredicto = "DUDOSO"
        motivos.append("%d caídas idénticas de %d unidades: patrón de descarga por lotes, no de venta; confirmar con el proveedor"
                       % (lotes[1], lotes[0]))
    else:
        veredicto = "REAL"
    return {"veredicto": veredicto, "vendidas_reportadas": total, "vendidas_depuradas": depuradas,
            "dias_con_venta": len(dias_venta), "dias_leidos": len(filas),
            "ritmo_diario_mediana": mediana, "_dep_filas": dep_filas, "motivos": motivos or ["venta repartida en varios días"]}


def autoprueba():
    """Corre los dos bancos de assets/: 21 casos reales del top 20 de Colombia y 20 casos
    escritos para romper el detector. Sale 1 si falla uno solo."""
    import os
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    fallos = total = 0
    for nombre in ("banco_top20_co_2026-09-18.json", "banco_ventas_adversarial.json"):
        ruta = os.path.join(base, nombre)
        if not os.path.exists(ruta):
            print("FALTA el banco %s: la autoprueba no se puede correr" % ruta)
            return 1
        casos = json.load(open(ruta, encoding="utf-8"))["productos"]
        for caso, p in casos.items():
            r = evaluar(normalizar(p))
            ok = r["veredicto"] == p.get("_esperado")
            if "_depuradas" in p:
                ok = ok and r.get("vendidas_depuradas") == p["_depuradas"]
            if "_reabastecimientos" in p:
                ok = ok and r.get("reabastecimientos") == p["_reabastecimientos"]
            if "_tendencia" in p:
                ok = ok and r.get("tendencia") == p["_tendencia"]
            total += 1
            if not ok:
                fallos += 1
                print("FALLA %s: esperado %s · depuradas %s · reabastecimientos %s | salió %s · %s · %s" % (
                    caso, p.get("_esperado"), p.get("_depuradas"), p.get("_reabastecimientos"),
                    r["veredicto"], r.get("vendidas_depuradas"), r.get("reabastecimientos")))
    print("AUTOPRUEBA %d de %d" % (total - fallos, total))
    return 1 if fallos else 0


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    try:
        datos = json.load(open(sys.argv[1], encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("ERROR DE ENTRADA: no se pudo leer %s: %s" % (sys.argv[1], e), file=sys.stderr)
        sys.exit(2)
    try:
        _main(datos)
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 — forma rara del JSON: error controlado, no traza
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


def _main(datos):
    if "--banco" in sys.argv:
        salida = {}
        aciertos = 0
        casos = datos.get("productos") if isinstance(datos, dict) else None
        if not isinstance(casos, dict):
            raise ErrorDeEntrada("--banco espera {\"productos\": {nombre: historial}}")
        for nombre, p in casos.items():
            r = evaluar(normalizar(p))
            esperado = p.get("_esperado")
            r["esperado"] = esperado
            r["acierta"] = (esperado == r["veredicto"]) if esperado else None
            # El veredicto solo no basta: un recorte mal hecho deja REAL con la cifra equivocada.
            if "_depuradas" in p:
                r["acierta"] = bool(r["acierta"]) and r.get("vendidas_depuradas") == p["_depuradas"]
            aciertos += 1 if r["acierta"] else 0
            salida[nombre] = r
        print(json.dumps(salida, ensure_ascii=False, indent=1))
        print("ACIERTOS %d de %d" % (aciertos, len(casos)), file=sys.stderr)
    else:
        print(json.dumps(evaluar(normalizar(datos)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
