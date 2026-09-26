#!/usr/bin/env python3
"""
correr_lote.py — pasa TODOS los candidatos de una corrida por el embudo en una sola pasada y
deja registro de cada uno (no solo de los elegidos).

Por qué existe: la primera corrida real (2026-09-18) procesó 12 de 35 candidatos a mano, uno
por uno, y dejó 17 sin revisar. El embudo solo es tan bueno como su cobertura. Y sin registro
de CADA candidato visto, la skill nunca sabe si acierta (propuesta del chat par, 2026-09-18).

Entrada: una carpeta con una subcarpeta por candidato:
  <corrida>/<candidato>/ficha.json      {"nombre","costo","incluir","dropi_id"}   (obligatorio)
  <corrida>/<candidato>/historial.json  get_product_history o history30d guardado tal cual
  <corrida>/<candidato>/mercado.json    semantic_search_products/search_products tal cual
  <corrida>/<candidato>/anuncios.json   semantic_search_ads con imagen + descripción (opcional)
Uso:
  python3 correr_lote.py <corrida> --pais CO [--etapa VALIDACION] [--max-proveedores N]
         [--max-anunciantes 3] [--min-7d 31] [--max-7d N] [--min-stock 80] [--canal landing|whatsapp]
         [--costo-min N] [--costo-max N] [--solo-verificados] [--antiguedad-min 7] [--precios]
         [--registro <archivo.jsonl>] [--hoy AAAA-MM-DD]
         [--entrega-golden PROYECTOS/CAZA-DIARIA-GANADORES/_entrega_golden.json]
  Cada bandera es una pregunta del menú (references/menu-arranque.md); la salida trae
  "filtros_aplicados" con todos los valores usados, también los que quedaron por defecto.
  python3 correr_lote.py --autoprueba
Salida: JSON con cada candidato, su estado (LISTA / CASI / FUERA / INCOMPLETO) y el motivo, en
orden de ranking. Nada se da por aprobado si falta un archivo: queda INCOMPLETO y se dice cuál.
"""
import json
import os
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ventas_reales as vr          # noqa: E402
import consolidar_mercado as cm     # noqa: E402
import competencia as co            # noqa: E402
import viabilidad_cod as vc         # noqa: E402
import comun                        # noqa: E402

ENTREGA = {}  # agregado de entrega_golden.py, si se pasa --entrega-golden
TASA_GENERAL = {}  # su tasa general YA VALIDADA en (0, 1] (comun.tasa); vacía si no hay agregado


def cargar_entrega(d):
    """Valida el agregado antes de usarlo: una tasa general de 73.5, -0.2 o True daba un PVP
    mínimo absurdo (hasta NEGATIVO) que salía LISTA (verificador, cuarta pasada)."""
    if not isinstance(d, dict) or not isinstance(d.get("total"), dict) or not isinstance(d.get("productos"), dict):
        raise ErrorDeEntrada("--entrega-golden no es un agregado de entrega_golden.py construir")
    t = comun.tasa(d["total"].get("tasa_entrega"))
    if t is None:
        raise ErrorDeEntrada("--entrega-golden: la tasa general %r no es una fracción en (0, 1]" % (d["total"].get("tasa_entrega"),))
    ENTREGA.clear()
    ENTREGA.update(d)
    TASA_GENERAL["v"] = t


def leer(ruta):
    try:
        return json.load(open(ruta, encoding="utf-8"))
    except (OSError, ValueError):
        return None


class ErrorDeEntrada(Exception):
    pass


# Valores por defecto del menú (references/menu-arranque.md). Los que están MEDIDOS lo dicen
# references/calibracion.md; el resto es heredado y se declara en la salida.
DEFECTO = {"pais": "CO", "etapa": "VALIDACION", "max_prov": None, "max_anun": 3, "con_precios": False,
           "min_7d": 31, "max_7d": None, "min_stock": 80, "canal": None, "costo_min": None,
           "costo_max": None, "solo_verificados": False, "antiguedad_min": 7, "frenando_es_casi": False,
           "dias_historial_viejo": 4}  # operativo, no medido: DropKiller lee con 2-3 días de retraso (Naider)
CALIENTE = 120  # más de esto en 7 días se marca "caliente": la demanda persiste, medir competencia


def num(x):
    return comun.numero(x)  # "30.000" = 30000 y "30000.5" = 30000,5: igual que viabilidad_cod


def uno(carpeta, f):
    r = {"carpeta": os.path.basename(carpeta), "faltan": [], "motivos": [], "casi": [], "avisos": []}
    ficha = leer(os.path.join(carpeta, "ficha.json"))
    if not isinstance(ficha, dict):
        ficha = {}
    r.update({k: ficha.get(k) for k in ("nombre", "costo")})
    r["dropi_id"] = comun.ident(ficha.get("dropi_id")) or None
    r["verificado"] = ficha.get("verificado") if isinstance(ficha.get("verificado"), bool) else "sin consultar"
    h = leer(os.path.join(carpeta, "historial.json"))
    m = leer(os.path.join(carpeta, "mercado.json"))
    for nombre, dato in (("ficha.json", ficha), ("historial.json", h), ("mercado.json", m)):
        if not dato:
            r["faltan"].append(nombre)
    if r["faltan"]:
        r["estado"] = "INCOMPLETO"
        return r
    try:
        filas_h = vr.normalizar(h)
        v = vr.evaluar(filas_h)
        filas = m.get("data") if isinstance(m, dict) else m
        c = cm.consolidar(filas, f["pais"], ficha.get("incluir"), None, f["etapa"], f["max_prov"])
    except (vr.ErrorDeEntrada, cm.ErrorDeEntrada) as e:
        r["estado"] = "INCOMPLETO"
        r["faltan"].append("dato ilegible: %s" % e)
        return r
    hoy = f["hoy"]
    r["ventas"] = {k: v.get(k) for k in ("veredicto", "vendidas_depuradas", "vendidas_reportadas",
                                          "ventas_7d", "aceleracion", "tendencia", "reabastecimientos")}
    r["mercado"] = {k: c.get(k) for k in ("ventas_totales_mercado", "etapa", "proveedores_activos",
                                           "criterio_1_ventas_100_a_validacion", "criterio_2_pocos_proveedores")}
    r["avisos"] += [a for a in c["avisos"][:-1]] + [x for x in v.get("motivos", []) if "recortad" in x or "negativ" in x]

    # Historial viejo: una lectura de enero no dice nada de hoy (verificador: salía LISTA).
    try:
        ultima = date.fromisoformat(filas_h[-1][0][:10]) if filas_h else None
    except ValueError:
        ultima = None
    if ultima is None or (hoy - ultima).days > f["dias_historial_viejo"]:
        r["casi"].append("historial viejo o sin fecha: última lectura %s" % (ultima or "ilegible"))
    stock = filas_h[-1][1] if filas_h else None
    if stock is None or stock < f["min_stock"]:
        r["casi"].append("stock del proveedor %s, mínimo %d (menú 10)" % (stock, f["min_stock"]))
    if f["solo_verificados"] and not ficha.get("verificado"):
        r["casi"].append("proveedor no verificado (menú 10)")

    costo = num(ficha.get("costo"))
    if costo is None or costo <= 0:
        r["casi"].append("sin costo del proveedor legible: no hay PVP mínimo (regla 9)")
    else:
        if f["costo_min"] is not None and costo < f["costo_min"] or f["costo_max"] is not None and costo > f["costo_max"]:
            r["casi"].append("costo $%d fuera del rango pedido (menú 10)" % costo)
        p = vc.cargar()
        prods = ENTREGA.get("productos") if isinstance(ENTREGA.get("productos"), dict) else {}
        prop = prods.get(r["dropi_id"] or "")
        propia = comun.numero(prop.get("tasa_entrega"), miles=False) if isinstance(prop, dict) else None
        if isinstance(prop, dict) and prop.get("muestra_chica") is False and propia == 0:
            # Una entrega de 0% con muestra es un dato (el peor), no un vacío: FUERA, no error.
            r["motivos"].append("entrega propia 0%% en %s pedidos terminados: todo se devuelve" % prop.get("terminados"))
        elif isinstance(prop, dict) and prop.get("muestra_chica") is False and comun.tasa(propia) is not None:
            p["p"] = comun.tasa(propia)
            r["entrega"] = "propia: %.1f%% en %s pedidos terminados" % (p["p"] * 100, prop.get("terminados"))
        elif TASA_GENERAL.get("v") is not None:
            # La general del agregado de la empresa, no la del asset: la que se imprime es la que se usa.
            p["p"] = TASA_GENERAL["v"]
            r["entrega"] = "la empresa no lo ha vendido (o <30 pedidos): tasa general %.1f%% del agregado, supuesto declarado" % (p["p"] * 100)
        else:
            r["entrega"] = "sin agregado de la empresa: tasa del asset %.1f%%, supuesto declarado" % (p["p"] * 100)
        r["pvp_minimo"] = round(vc.pvp_minimo(costo, p["piso"], p["p"], p["flete"], p["fallido"], p["comision"], p["cpa"]))

    # Puertas duras: lo que no es un producto real o no cumple el método, FUERA.
    if v["veredicto"] == "FANTASMA":
        r["motivos"].append("ventas fantasma (ajuste de inventario)")
    if v["veredicto"] in ("SIN_VENTAS", "SIN_DATOS"):
        r["motivos"].append("sin ventas medibles")
    if not c["etapa_es_la_pedida"]:
        r["motivos"].append("etapa %s, se pidió %s (%d ventas)" % (c["etapa"], f["etapa"], c["ventas_totales_mercado"]))
    if not c["criterio_2_pocos_proveedores"]:
        r["motivos"].append("%d proveedores activos, tope %d" % (c["proveedores_activos"], c["tope_proveedores"]))

    # Criterio 3, antigüedad de los anuncios y plata: si rompen el filtro, CASI (no FUERA).
    anuncios = leer(os.path.join(carpeta, "anuncios.json"))
    filas_a = anuncios.get("data") if isinstance(anuncios, dict) else anuncios
    if not isinstance(filas_a, list) or not filas_a:
        r["casi"].append("canal SIN MEDIR (%s)" % ("falta anuncios.json" if anuncios is None else "0 anuncios legibles"))
    else:
        filas_a = [a for a in filas_a if isinstance(a, dict)]
        k = co.canal(filas_a, ficha.get("incluir_anuncios"), hoy, f["canal"])
        todos = k["activos"] + k["cementerio"]
        por = k["activos_por_canal"]
        if f["canal"]:
            activos_tope, canal_usado = k["anunciantes_activos"], f["canal"]
        else:
            # 9C "el más libre": se cuentan los dos canales y el tope se mide en el MÁS LIBRE.
            canal_usado = k["canal_mas_libre"]
            activos_tope = por[canal_usado]
        r["canal"] = {"activos": activos_tope, "activos_por_canal": por, "canal_medido": canal_usado,
                      "cementerio": k["anunciantes_en_cementerio"],
                      "nombres_activos": [a["anunciante"] for a in k["activos"]]}
        r["avisos"] += [a for a in k["avisos"] if "sin lastSeenActiveAt" in a]
        if not todos:
            r["casi"].append("canal SIN MEDIR (0 anuncios del producto tras el filtro)")
        elif activos_tope > f["max_anun"]:
            r["casi"].append("%d anunciantes activos en %s (el canal %s), tope %d" % (
                activos_tope, canal_usado, "elegido" if f["canal"] else "más libre", f["max_anun"]))
        if todos and f["antiguedad_min"] and max(a["max_dias_activo"] for a in todos) < f["antiguedad_min"]:
            r["casi"].append("ningún anuncio corrió %d días o más (menú 7)" % f["antiguedad_min"])
        if f["con_precios"] and r.get("pvp_minimo"):
            pr = co.precios(filas_a, r["pvp_minimo"], None, ficha.get("incluir_anuncios"))
            r["competencia_precio"] = {k2: pr.get(k2) for k2 in ("leidas", "landings", "precio_min", "precio_mediana", "precio_max", "plata")}
            r["avisos"] += ["precios: " + a for a in pr.get("avisos", [])]  # "un solo precio", packs fuera: a la tarjeta
            if pr.get("plata") == "NO CIERRA":
                r["casi"].append("la competencia vende a $%s, el mínimo es $%s" % (int(pr["precio_mediana"]), r["pvp_minimo"]))
    if v["veredicto"] == "DUDOSO":
        r["casi"].append("ventas DUDOSAS")

    # Ritmo de 7 días y frenado: los umbrales y cuánto están medidos viven en calibracion.md.
    v7 = v.get("ventas_7d") or 0
    if v7 < f["min_7d"]:
        r["casi"].append("%d ventas en 7 días, piso %d (calibracion.md)" % (v7, f["min_7d"]))
    if f["max_7d"] is not None and v7 > f["max_7d"]:
        r["casi"].append("%d ventas en 7 días, techo %d (menú 6A)" % (v7, f["max_7d"]))
    if v7 > CALIENTE:
        r["avisos"].append("CALIENTE: %d en 7 días; la demanda persiste, la competencia se mide sí o sí" % v7)
    if v.get("tendencia") == "frenando":
        texto = "FRENANDO (aceleración %s, calibracion.md)" % v.get("aceleracion")
        (r["casi"] if f["frenando_es_casi"] else r["avisos"]).append(texto)
    if f["pais"] != "CO":
        r["avisos"].append("umbrales de ritmo medidos solo en Colombia: en %s son supuesto" % f["pais"])

    r["estado"] = "FUERA" if r["motivos"] else ("CASI" if r["casi"] else "LISTA")
    return r


def uno_seguro(carpeta, f):
    """Un candidato roto no tumba el lote: queda INCOMPLETO con el error a la vista."""
    try:
        return uno(carpeta, f)
    except Exception as e:  # noqa: BLE001 — se reporta, no se esconde
        return {"carpeta": os.path.basename(carpeta), "estado": "INCOMPLETO", "motivos": [], "casi": [],
                "faltan": ["error inesperado: %s: %s" % (type(e).__name__, e)]}


def clave_ranking(r):
    """Orden de dropkiller-caza.md §6 paso 9 (el mismo texto allá): estado → proveedores →
    anunciantes activos → ventas de 7 días. Los reabastecimientos NO entran: con N = 2 no se
    pudieron medir (calibracion.md, backtest v2)."""
    orden = {"LISTA": 0, "CASI": 1, "FUERA": 2, "INCOMPLETO": 3}[r["estado"]]
    m = r.get("mercado") or {}
    v = r.get("ventas") or {}
    k = r.get("canal") or {}
    def o(x, vacio):  # 0 es un dato (el mejor), no un vacío: `or 99` lo mandaba al final
        return vacio if x is None else x
    return (orden, o(m.get("proveedores_activos"), 99), o(k.get("activos"), 99), -o(v.get("ventas_7d"), 0))


def correr(raiz, registro=None, **filtros):
    f = dict(DEFECTO, **{k: val for k, val in filtros.items() if val is not None or k in ("max_prov", "max_7d")})
    f["hoy"] = filtros.get("hoy") or date.today()
    f["etapa"] = comun.clave(f["etapa"]).upper()
    if f["etapa"] not in cm.ETAPAS_PEDIBLES:
        raise ErrorDeEntrada("--etapa debe ser una de %s" % ", ".join(cm.ETAPAS_PEDIBLES))
    # Rango, no solo tipo: un tope negativo o un piso negativo pasaban en silencio (verificador).
    for k in ("max_anun", "min_7d", "min_stock", "antiguedad_min", "max_prov", "max_7d", "costo_min", "costo_max"):
        if f[k] is not None and f[k] < 0:
            raise ErrorDeEntrada("--%s no puede ser negativo (vino %s)" % (k.replace("_", "-"), f[k]))
    if f["max_7d"] is not None and f["max_7d"] < f["min_7d"]:
        raise ErrorDeEntrada("--max-7d (%s) menor que --min-7d (%s): ningún producto podría pasar" % (f["max_7d"], f["min_7d"]))
    if f["canal"] not in (None, "landing", "whatsapp"):
        raise ErrorDeEntrada("--canal debe ser landing o whatsapp (sin la bandera cuenta los dos)")
    if not os.path.isdir(raiz):
        raise ErrorDeEntrada("no existe la carpeta %s" % raiz)
    carpetas = sorted(os.path.join(raiz, d) for d in os.listdir(raiz)
                      if os.path.isdir(os.path.join(raiz, d)) and not d.startswith((".", "_")))
    res = sorted((uno_seguro(c, f) for c in carpetas), key=clave_ranking)
    cuenta = {e: sum(1 for r in res if r["estado"] == e) for e in ("LISTA", "CASI", "FUERA", "INCOMPLETO")}
    if registro:
        carpeta_reg = os.path.dirname(os.path.abspath(registro))
        if not os.path.isdir(carpeta_reg) or not os.access(carpeta_reg, os.W_OK):
            raise ErrorDeEntrada("--registro: no se puede escribir en %s" % carpeta_reg)
        try:
            fh = open(registro, "a", encoding="utf-8")
        except OSError as e:  # archivo de solo lectura, o es una carpeta
            raise ErrorDeEntrada("--registro %s: %s" % (registro, e))
        with fh:
            for r in res:
                fh.write(json.dumps({"fecha": str(f["hoy"]), "pais": f["pais"], "nombre": r.get("nombre"),
                                     "dropi_id": r.get("dropi_id"), "estado": r["estado"],
                                     "ventas": r.get("ventas"), "mercado": r.get("mercado"),
                                     "canal": r.get("canal"), "pvp_minimo": r.get("pvp_minimo")},
                                    ensure_ascii=False) + "\n")
    aplicados = {k: (str(val) if isinstance(val, date) else val) for k, val in f.items()}
    return {"fecha": str(f["hoy"]), "pais": f["pais"], "filtros_aplicados": aplicados,
            "candidatos": len(res), "cuenta": cuenta,
            "cobertura": "%d de %d con datos completos" % (len(res) - cuenta["INCOMPLETO"], len(res)),
            "resultados": res}


def autoprueba():
    import tempfile
    t = tempfile.mkdtemp()
    def cand(nombre, ventas, mercado, anuncios=None, costo=30000, incluir="producto", mes="09", stock0=5000):
        d = os.path.join(t, nombre)
        os.makedirs(d)
        json.dump({"nombre": nombre, "costo": costo, "incluir": incluir, "dropi_id": nombre},
                  open(os.path.join(d, "ficha.json"), "w"))
        s, h = stock0, []
        for i, x in enumerate(ventas):
            s -= x
            h.append(["2026-%s-%02d" % (mes, i + 1), s, x, 20000])
        json.dump({"h": h}, open(os.path.join(d, "historial.json"), "w"))
        json.dump({"data": [{"externalId": nombre + str(i), "name": "producto " + nombre, "providerName": "prov%d" % i,
                             "totalSoldUnits": u, "stock": 100, "status": "ACTIVE",
                             "lastSeenAt": "2026-09-18T00:00:00Z"} for i, u in enumerate(mercado)]},
                  open(os.path.join(d, "mercado.json"), "w"))
        if anuncios is not None:
            json.dump({"data": [{"advertiserName": "a%d" % i, "lastSeenActiveAt": "2026-09-17T00:00:00Z",
                                 "landingUrl": "https://a%d-%s.co/products/x" % (i, nombre),
                                 "activeDays": 12, "title": "producto"} for i in range(anuncios)]},
                      open(os.path.join(d, "anuncios.json"), "w"))
    cand("bueno", [10] * 14, [400], anuncios=2)
    cand("saturado", [10] * 14, [400], anuncios=6)
    cand("sin_canal", [10] * 14, [400])
    cand("fantasma", [0] * 13 + [2000], [2000], anuncios=1)
    cand("quemado", [10] * 14, [20000], anuncios=1)
    cand("muchos_prov", [10] * 14, [100] * 7, anuncios=1)
    cand("lento", [3] * 14, [400], anuncios=1)                      # 21 en 7 días: bajo el piso de 31
    cand("frenando", [20] * 21 + [5] * 7, [800], anuncios=1)        # 35 en 7 días pero frenando
    cand("viejo", [10] * 14, [400], anuncios=1, mes="01")           # última lectura en enero
    cand("sin_costo", [10] * 14, [400], anuncios=1, costo=None)
    cand("stock_bajo", [10] * 14, [400], anuncios=1, stock0=150)     # termina con 10 unidades
    cand("caliente", [30] * 14, [2000], anuncios=1)                  # 210 en 7 días: aviso, no descarte
    cand("anuncios_rotos", [10] * 14, [400])
    json.dump({"data": 5}, open(os.path.join(t, "anuncios_rotos", "anuncios.json"), "w"))
    cand("ficha_lista", [10] * 14, [400], anuncios=1)
    json.dump(["no", "es", "un", "dict"], open(os.path.join(t, "ficha_lista", "ficha.json"), "w"))
    os.makedirs(os.path.join(t, "incompleto"))
    errores_carga = []
    for mala in (73.5, -0.2, True, "nan"):
        try:
            cargar_entrega({"total": {"tasa_entrega": mala}, "productos": {}})
            errores_carga.append("agregado con tasa general %r: debía dar error" % (mala,))
        except ErrorDeEntrada:
            pass
    cargar_entrega({"total": {"tasa_entrega": 0.727}, "productos": {
        "bueno": {"tasa_entrega": 0.95, "muestra_chica": False, "terminados": 200},
        "lento": {"tasa_entrega": 0.0, "muestra_chica": False, "terminados": 40}}})
    reg = os.path.join(t, "_registro.jsonl")
    r = correr(t, registro=reg, hoy=date(2026, 9, 18))
    est = {x["carpeta"]: x["estado"] for x in r["resultados"]}
    # "saturado": 6 anunciantes, todos a landing. Con 9C (por defecto) WhatsApp queda libre y
    # pasa; con --canal landing debe quedar CASI (se prueba abajo).
    esperado = {"bueno": "LISTA", "saturado": "LISTA", "sin_canal": "CASI", "fantasma": "FUERA",
                "quemado": "FUERA", "muchos_prov": "FUERA", "incompleto": "INCOMPLETO",
                # "lento" va FUERA: su entrega propia es 0% con 40 pedidos terminados
                "lento": "FUERA", "frenando": "LISTA", "viejo": "CASI", "sin_costo": "CASI",
                "stock_bajo": "CASI", "caliente": "LISTA", "anuncios_rotos": "CASI", "ficha_lista": "INCOMPLETO"}
    fallos = [k for k in esperado if est.get(k) != esperado[k]] + errores_carga
    lineas = open(reg, encoding="utf-8").read().splitlines()
    fre = [x for x in r["resultados"] if x["carpeta"] == "frenando"][0]
    if not any("FRENANDO" in a for a in fre.get("avisos", [])):
        fallos.append("frenando: debía quedar en LISTA pero con el aviso FRENANDO a la vista")
    cal = [x for x in r["resultados"] if x["carpeta"] == "caliente"][0]
    if not any("CALIENTE" in a for a in cal.get("avisos", [])):
        fallos.append("caliente: debía llevar el aviso CALIENTE")
    r2 = correr(t, hoy=date(2026, 9, 18), etapa="VALIDACIÓN")
    if {x["carpeta"]: x["estado"] for x in r2["resultados"]}.get("bueno") != "LISTA":
        fallos.append("etapa con tilde: 'VALIDACIÓN' debía funcionar igual que 'VALIDACION'")
    try:
        correr(t, hoy=date(2026, 9, 18), etapa="XYZ")
        fallos.append("etapa inexistente: debía dar error, no dejar todo FUERA en silencio")
    except ErrorDeEntrada:
        pass
    if len(lineas) != 15:
        fallos.append("registro: %d líneas, se esperaban 15 (una por candidato, no solo los elegidos)" % len(lineas))
    pv = {x["carpeta"]: x.get("pvp_minimo") for x in r["resultados"]}
    if not (pv.get("bueno") and pv.get("saturado") and pv["bueno"] < pv["saturado"]):
        fallos.append("entrega propia: con 95%% el PVP mínimo debe bajar (salió %s contra %s)" % (pv.get("bueno"), pv.get("saturado")))
    ENTREGA.clear()
    TASA_GENERAL.clear()
    # Un error inesperado en UN candidato no tumba el lote (verificador: {"data":5} lo tumbaba)
    original = vr.evaluar
    def explota(filas):
        raise RuntimeError("fallo forzado")
    vr.evaluar = explota
    try:
        r3 = correr(t, hoy=date(2026, 9, 18))
        if not all(x["estado"] == "INCOMPLETO" for x in r3["resultados"]) or r3["candidatos"] != len(esperado):
            fallos.append("un error inesperado debía dejar INCOMPLETO a cada candidato sin tumbar el lote")
    except RuntimeError:
        fallos.append("un error inesperado tumbó el lote entero")
    finally:
        vr.evaluar = original
    for mala in ({"max_anun": -1}, {"min_7d": -5}, {"min_stock": -1}, {"antiguedad_min": -3}):
        try:
            correr(t, hoy=date(2026, 9, 18), **mala)
            fallos.append("valor negativo %s: debía dar error" % mala)
        except ErrorDeEntrada:
            pass
    rl = correr(t, hoy=date(2026, 9, 18), canal="landing")
    if {x["carpeta"]: x["estado"] for x in rl["resultados"]}.get("saturado") != "CASI":
        fallos.append("--canal landing: 'saturado' (6 anunciantes en landing) debía quedar CASI")
    sat = [x for x in r["resultados"] if x["carpeta"] == "saturado"][0]
    if sat["canal"]["canal_medido"] != "whatsapp" or sat["canal"]["activos_por_canal"] != {"landing": 6, "whatsapp": 0}:
        fallos.append("9C: debía medir en WhatsApp (0) y reportar landing 6 · whatsapp 0; salió %s" % sat["canal"])
    orden = [x["carpeta"] for x in r["resultados"][:4]]
    # LISTA, todos con 0 activos en su canal más libre: manda el ritmo de 7 días (210, 70, 70, 35)
    if orden != ["caliente", "bueno", "saturado", "frenando"]:
        fallos.append("ranking: se esperaba caliente, bueno, saturado, frenando; salió %s" % orden)
    for f in fallos:
        print("FALLA", f, "| salió", est.get(f))
    total = len(esperado) + 14
    print("AUTOPRUEBA %d de %d" % (total - len(fallos), total))
    return 1 if fallos else 0


def comun_num(x):
    v = comun.numero(x)  # "30.000" y "30,000" = treinta mil, igual que viabilidad_cod
    if v is None:
        raise ValueError(x)
    return v


def arg(bandera, defecto=None, tipo=str):
    if bandera not in sys.argv:
        return defecto
    i = sys.argv.index(bandera)
    if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
        raise ErrorDeEntrada("%s necesita un valor" % bandera)
    try:
        return tipo(sys.argv[i + 1])
    except ValueError:
        raise ErrorDeEntrada("%s: valor inválido %r" % (bandera, sys.argv[i + 1]))


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print(__doc__)
        sys.exit(2)
    try:
        eg = arg("--entrega-golden")
        if eg:
            try:
                d = json.load(open(eg, encoding="utf-8"))
            except (OSError, ValueError) as e:
                raise ErrorDeEntrada("--entrega-golden %s: %s" % (eg, e))
            cargar_entrega(d)
        out = correr(sys.argv[1], registro=arg("--registro"),
                     pais=arg("--pais", "CO").upper(), etapa=arg("--etapa", "VALIDACION"),
                     max_prov=arg("--max-proveedores", None, int), max_anun=arg("--max-anunciantes", 3, int),
                     con_precios="--precios" in sys.argv, hoy=arg("--hoy", None, date.fromisoformat),
                     min_7d=arg("--min-7d", 31, int), max_7d=arg("--max-7d", None, int),
                     min_stock=arg("--min-stock", 80, int), canal=arg("--canal"),
                     costo_min=arg("--costo-min", None, comun_num), costo_max=arg("--costo-max", None, comun_num),
                     solo_verificados="--solo-verificados" in sys.argv,
                     antiguedad_min=arg("--antiguedad-min", 7, int))
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
