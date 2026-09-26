#!/usr/bin/env python3
"""
entrega_golden.py — cuánto se ENTREGA de verdad un producto, con los pedidos reales de la empresa.

Por qué existe (propuesta del chat par, 2026-09-18): DropKiller mide lo que BAJA el stock del
proveedor, no lo que llega al cliente. En contra entrega un producto que vende y se devuelve
pierde plata. La empresa tiene sus pedidos reales de Dropi (informes bimestrales "por
producto"): ahí está el ESTATUS de cada pedido con el PRODUCTO ID de Dropi, que es el mismo
externalId que devuelve DropKiller. Nadie más tiene ese dato.

Dos modos:
  construir  lee los informes .xlsx y escribe un JSON AGREGADO (sin un solo dato de cliente:
             ni nombre, ni teléfono, ni dirección, ni cédula). Necesita openpyxl. Medido el
             2026-09-20: openpyxl 3.1.5 responde en `python3`, `/opt/homebrew/bin/python3` y
             `/usr/bin/python3`. No creerle a esta línea: si falla el import, probar otro
             intérprete (`python3 -c "import openpyxl"`).
    python3 entrega_golden.py construir "<carpeta INFORMES DROPI de UNA empresa>" --salida <json>
  consultar  dice la tasa de entrega de uno o varios productos (Python 3 cualquiera):
    python3 entrega_golden.py consultar <json> --producto-id 2122331 [2184034 ...]
  python3 entrega_golden.py --autoprueba

Reglas:
- Una empresa por archivo. Golden, Le'côterra y otra empresa del grupo Incanto JAMÁS se mezclan: el JSON guarda
  la carpeta de origen y consultar lo muestra.
- Tasa de entrega = ENTREGADO / (ENTREGADO + DEVOLUCION). Cancelados y rechazados no cuentan:
  nunca salieron. Es la definición de economia-cod-golden.json (73,5% por PEDIDO el 06-sep); aquí
  se cuenta por PEDIDO-PRODUCTO y con más meses, así que da otra cifra. La cifra que vale es la
  que imprime `construir`, nunca una escrita a mano (una escrita aquí ya quedó vieja una vez).
- Productos de OTRA empresa vendidos por la misma cuenta de Dropi (medido 2026-09-18: sprays de
  Le'côterra en los informes de Golden) se excluyen con --excluir (por defecto la marca
  Le'côterra) y la lista de excluidos queda en el JSON. A quién pertenecen esas ventas lo decide
  FER o el Centro de Mando, no este script.
- Un pedido con dos productos cuenta una vez para cada uno. El mismo pedido repetido en dos
  informes cuenta una vez (se deduplica por ID de pedido + PRODUCTO ID).
- Menos de 30 pedidos terminados = "muestra chica": se muestra, no se usa como compuerta.
- El JSON NO va dentro de la skill: la skill se puede publicar y estos son datos internos.
  Destino sugerido: PROYECTOS/CAZA-DIARIA-GANADORES/_entrega_<empresa>.json
"""
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime

class ErrorDeEntrada(Exception):
    pass


MUESTRA_MIN = 30
TERMINADOS = ("ENTREGADO", "DEVOLUCION")
# La marca se busca en el nombre NORMALIZADO (sin tildes, un espacio) y ANTES de recortarlo:
# "Le'cóterra", "LE  COTERRA" o la marca al final de un nombre largo se escapaban (verificador).
EXCLUIR_DEFECTO = r"lecoterra"  # se busca en el nombre SOLO LETRAS: 'Lecoterra2', 'lecoterra_spray',
                                  # 'SPRAYLECOTERRA' y 'L e coterra' se fugaban con \b (verificador)
# Y por ID, que es la identidad (el rótulo puede cambiar): los PRODUCTO ID de Le'côterra vistos
# en los informes de Golden el 2026-09-18. Ampliar aquí, no por el nombre.
IDS_EXCLUIR_DEFECTO = {"2156262", "2143403", "2024632", "2222545", "2187934", "2004283"}


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402  (una sola forma de normalizar: el verificador la encontró duplicada aquí)
sin_tildes = comun.sin_tildes
fecha_iso = comun.fecha_iso


def ident(x):
    """El ident de comun, sin ceros a la izquierda: '02222545' y '2222545' son el mismo ID."""
    t = comun.ident(x)
    return t.lstrip("0") or t if t.isdigit() else t


def estado(x):
    """ENTREGADO / DEVOLUCION / otro. 'DEVOLUCIÓN' con tilde y 'DEVOLUCION EN BODEGA' son
    devoluciones (el verificador los encontró cayendo en 'otros')."""
    e = sin_tildes(x).strip().upper()
    if e.startswith("DEVOLUCION"):
        return "DEVOLUCION"
    if e == "ENTREGADO":
        return "ENTREGADO"
    return "otros"


def agregar(filas, origen, excluir=EXCLUIR_DEFECTO, ids_excluir=IDS_EXCLUIR_DEFECTO):
    """filas: iterable de dicts con ID, PRODUCTO ID, PRODUCTO, ESTATUS, FECHA. Devuelve el agregado."""
    vistos = set()
    por = {}
    excluidos = {}
    total = {"ENTREGADO": 0, "DEVOLUCION": 0, "otros": 0}
    patron = re.compile(excluir, re.I) if excluir else None
    for f in filas:
        # ident(): un ID numérico 0 es un ID, no un vacío, y ' 123298' o 123298.0 son el mismo
        pid = ident(f.get("PRODUCTO ID"))
        oid = ident(f.get("ID"))
        if not pid or not oid or (oid, pid) in vistos:
            continue
        vistos.add((oid, pid))
        completo = str(f.get("PRODUCTO") or "").strip()
        nombre = completo[:80]
        solo_letras = re.sub(r"[^a-z]", "", sin_tildes(completo).lower())
        if pid in {ident(i) for i in (ids_excluir or ())} or (patron and patron.search(solo_letras)):
            excluidos.setdefault(pid, {"producto": nombre, "filas": 0})["filas"] += 1
            continue
        p = por.setdefault(pid, {"producto": nombre, "ENTREGADO": 0,
                                 "DEVOLUCION": 0, "otros": 0, "primera": None, "ultima": None})
        clave = estado(f.get("ESTATUS"))
        p[clave] += 1
        total[clave] += 1
        fe = fecha_iso(f.get("FECHA"))
        if fe:
            p["primera"] = min(p["primera"] or fe, fe)
            p["ultima"] = max(p["ultima"] or fe, fe)
    for p in por.values():
        t = p["ENTREGADO"] + p["DEVOLUCION"]
        p["terminados"] = t
        p["tasa_entrega"] = round(p["ENTREGADO"] / t, 3) if t else None
        p["muestra_chica"] = t < MUESTRA_MIN
    tt = total["ENTREGADO"] + total["DEVOLUCION"]
    if not tt:
        raise ErrorDeEntrada("ningún pedido ENTREGADO ni DEVOLUCION: no hay tasa que calcular (solo cancelados u otros)")
    return {"origen": origen, "construido": str(date.today()), "pedidos_producto_unicos": len(vistos),
            "total": dict(total, terminados=tt, tasa_entrega=round(total["ENTREGADO"] / tt, 3) if tt else None),
            "definicion": "ENTREGADO / (ENTREGADO + DEVOLUCION); cancelados y rechazados fuera",
            "excluidos_por_marca": {"patron": excluir, "productos": excluidos},
            "productos": por}


def leer_xlsx(carpeta):
    import openpyxl  # medido 2026-09-20: 3.1.5 en los tres intérpretes del Mac
    archivos = sorted(glob.glob(os.path.join(carpeta, "**", "*por producto*.xlsx"), recursive=True))
    if not archivos:
        raise ErrorDeEntrada("no hay informes '*por producto*.xlsx' en %s" % carpeta)
    utiles = ("ID", "PRODUCTO ID", "PRODUCTO", "ESTATUS", "FECHA")
    for a in archivos:
        ws = openpyxl.load_workbook(a, read_only=True).active
        filas = ws.iter_rows(values_only=True)
        enc = [str(c).strip() if c else "" for c in next(filas)]
        falta = [u for u in utiles if u not in enc]
        if falta:
            print("AVISO: %s no trae %s: se salta" % (os.path.basename(a), falta), file=sys.stderr)
            continue
        idx = {u: enc.index(u) for u in utiles}
        for r in filas:  # solo se leen las 5 columnas útiles: ningún dato de cliente sale de aquí
            yield {u: r[i] for u, i in idx.items()}


def consultar(ruta, ids):
    try:
        d = json.load(open(ruta, encoding="utf-8"))
        tasa = comun.tasa(d["total"]["tasa_entrega"])
        productos = d["productos"]
        if not isinstance(productos, dict) or tasa is None:
            raise TypeError("productos debe ser un objeto y la tasa general una fracción en (0, 1]")
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise ErrorDeEntrada("%s no es un agregado de entrega_golden.py construir (%s: %s)" % (ruta, type(e).__name__, e))
    out = {"origen": d.get("origen"), "tasa_general": tasa, "productos": {}}
    for i in ids:
        p = productos.get(ident(i))
        if not p:
            out["productos"][str(i)] = "la empresa nunca lo vendió: sin dato propio, usar la tasa general como supuesto y DECLARARLO"
            continue
        if not isinstance(p, dict):
            out["productos"][ident(i)] = "ficha ilegible en el agregado: reconstruirlo"
            continue
        p = dict(p)
        if p.get("tasa_entrega") is not None and p.get("muestra_chica") is False:
            dif = p["tasa_entrega"] - tasa
            p["frente_a_la_general"] = "%+.1f puntos" % (dif * 100)
            p["compuerta"] = "BAJO: se devuelve más que el promedio" if dif <= -0.05 else "ok"
        else:
            p["compuerta"] = "muestra chica (<%d terminados): solo referencia" % MUESTRA_MIN
        out["productos"][ident(i)] = p
    return out


def autoprueba():
    filas = []
    def ped(oid, pid, est, nombre="x"):
        filas.append({"ID": oid, "PRODUCTO ID": pid, "PRODUCTO": nombre, "ESTATUS": est, "FECHA": "2026-05-01"})
    for i in range(40):
        ped(i, "A", "ENTREGADO" if i < 30 else "DEVOLUCION")          # A: 75%
    for i in range(40, 80):
        ped(i, "B", "ENTREGADO" if i < 60 else "DEVOLUCION")          # B: 50%
    for i in range(80, 85):
        ped(i, "C", "ENTREGADO")                                      # C: 5 pedidos, muestra chica
    ped(85, "A", "CANCELADO")                                          # no cuenta como terminado
    ped(0, "A", "ENTREGADO")                                           # duplicado de otro informe
    ped(86, "A", "ENTREGADO"); ped(86, "B", "DEVOLUCION")             # pedido con dos productos
    ped(90, "D", "DEVOLUCIÓN"); ped(91, "D", "DEVOLUCION EN BODEGA"); ped(92, " D ", "entregado")  # tildes, bodega, minúsculas, espacios
    ped(93, "L", "ENTREGADO", "Lecoterra Spray")                     # otra empresa: fuera
    ped(96, "L2", "ENTREGADO", "Spray íntimo " + "x" * 80 + " Le'cóterra")  # marca al final de un nombre largo, tilde aguda
    ped(97, "L3", "ENTREGADO", "LE  COTERRA spray")                  # doble espacio
    ped(98, "L4", "ENTREGADO", "SPRAYLECOTERRA2_x")                   # pegada, con dígitos y guion bajo
    filas.append({"ID": 94, "PRODUCTO ID": 555.0, "PRODUCTO": "y", "ESTATUS": "ENTREGADO", "FECHA": "31-08-2026"})
    filas.append({"ID": 95, "PRODUCTO ID": "555", "PRODUCTO": "y", "ESTATUS": "ENTREGADO", "FECHA": "01-09-2025"})
    d = agregar(filas, "prueba")
    fallos = []
    def chequeo(n, ok):
        if not ok:
            fallos.append(n)
    a, b, c = d["productos"]["A"], d["productos"]["B"], d["productos"]["C"]
    chequeo("A: 31 entregados de 41 (duplicado fuera, cancelado fuera)", (a["ENTREGADO"], a["terminados"]) == (31, 41))
    chequeo("cancelado va a otros", a["otros"] == 1)
    chequeo("B: pedido con dos productos cuenta para B", b["terminados"] == 41)
    chequeo("C muestra chica", c["muestra_chica"])
    import tempfile
    ruta = os.path.join(tempfile.mkdtemp(), "e.json")
    json.dump(d, open(ruta, "w"))
    q = consultar(ruta, ["A", "B", "C", "Z"])["productos"]
    chequeo("B marcado BAJO", q["B"]["compuerta"].startswith("BAJO"))
    chequeo("A ok", q["A"]["compuerta"] == "ok")
    chequeo("C no es compuerta", q["C"]["compuerta"].startswith("muestra chica"))
    chequeo("Z nunca vendido lo dice", isinstance(q["Z"], str) and "DECLARARLO" in q["Z"])
    dd = d["productos"]["D"]
    chequeo("DEVOLUCIÓN y EN BODEGA son devolución, minúsculas y espacios normalizados", (dd["DEVOLUCION"], dd["ENTREGADO"]) == (2, 1))
    chequeo("la otra empresa queda fuera y declarada", "L" not in d["productos"] and "L" in d["excluidos_por_marca"]["productos"])
    chequeo("variantes de la marca también quedan fuera", all(x not in d["productos"] for x in ("L2", "L3", "L4")))
    chequeo("ID con cero a la izquierda se excluye igual", "02222545" not in agregar(
        [{"ID": 1, "PRODUCTO ID": "02222545", "PRODUCTO": "spray", "ESTATUS": "ENTREGADO"},
         {"ID": 2, "PRODUCTO ID": "7", "PRODUCTO": "otro", "ESTATUS": "ENTREGADO"}], "x")["productos"])
    chequeo("exclusión por ID aunque el nombre no diga la marca", "2222545" not in agregar(
        [{"ID": 1, "PRODUCTO ID": "2222545", "PRODUCTO": "spray", "ESTATUS": "ENTREGADO"},
         {"ID": 2, "PRODUCTO ID": "7", "PRODUCTO": "otro", "ESTATUS": "ENTREGADO"}], "x")["productos"])
    try:
        agregar([{"ID": 1, "PRODUCTO ID": "9", "PRODUCTO": "y", "ESTATUS": "CANCELADO"}], "x")
        chequeo("solo cancelados da error controlado", False)
    except ErrorDeEntrada:
        chequeo("solo cancelados da error controlado", True)
    y = d["productos"]["555"]
    chequeo("555.0 y '555' son el mismo producto", y["terminados"] == 2)
    chequeo("fechas DD-MM-AAAA ordenan bien", (y["primera"], y["ultima"]) == ("2025-09-01", "2026-08-31"))
    q = consultar(ruta, [" 555 "])["productos"]
    try:
        consultar(os.path.join(tempfile.mkdtemp(), "no.json"), ["1"])
        chequeo("archivo que no existe da error controlado", False)
    except ErrorDeEntrada:
        chequeo("archivo que no existe da error controlado", True)
    for f in fallos:
        print("FALLA", f)
    print("AUTOPRUEBA %d de 17" % (17 - len(fallos)))
    return 1 if fallos else 0


def valor(bandera):
    if bandera not in sys.argv:
        return None
    i = sys.argv.index(bandera)
    if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
        raise ErrorDeEntrada("%s necesita un valor" % bandera)
    return sys.argv[i + 1]


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 3 or sys.argv[1] not in ("construir", "consultar"):
        print(__doc__)
        sys.exit(2)
    try:
        if sys.argv[1] == "construir":
            salida = valor("--salida")
            if not salida:
                raise ErrorDeEntrada("construir necesita --salida <json>")
            excluir = valor("--excluir") if "--excluir" in sys.argv else EXCLUIR_DEFECTO
            try:
                re.compile(excluir)
            except re.error as e:
                raise ErrorDeEntrada("--excluir no es una expresión válida: %s" % e)
            d = agregar(leer_xlsx(sys.argv[2]), os.path.abspath(sys.argv[2]), excluir)
            json.dump(d, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            t = d["total"]
            ex = d["excluidos_por_marca"]["productos"]
            print("OK · %d productos · %d pedido-producto únicos · %d terminados · tasa %.1f%% · %d producto(s) de otra marca excluidos → %s"
                  % (len(d["productos"]), d["pedidos_producto_unicos"], t["terminados"], t["tasa_entrega"] * 100, len(ex), salida))
        else:
            i = sys.argv.index("--producto-id") if "--producto-id" in sys.argv else -1
            ids = [x for x in sys.argv[i + 1:] if not x.startswith("--")] if i >= 0 else []
            if not ids:
                raise ErrorDeEntrada("consultar necesita --producto-id <id> [<id> ...]")
            print(json.dumps(consultar(sys.argv[2], ids), ensure_ascii=False, indent=1))
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
