#!/usr/bin/env python3
"""Genera el JSON de configuración del asistente de COMENTARIOS de Chatea Pro.

Pide 5 datos de intake (uno a la vez): país, contacto, tiempos de envío,
información adicional del negocio, y la lista de productos con la dolencia que
trata cada uno (guardarraíl anti-dolencias, --producto obligatorio y repetible).

Datos que la IA pide al cliente (datos_req): se generan solos según el país.
Ver DATOS_POR_PAIS (7 packs: COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU,
PARAGUAY — cada uno con su nomenclatura real de direcciones; no existe un
esquema "internacional"). Lista manual: --datos-cliente.

Cantidad y precios NO se piden aquí: van en la ficha del producto dentro de
Chatea Pro, no en esta configuración general.

Uso (ejemplo completo que corre — --producto es OBLIGATORIO, repetible):
    python3 build_config.py \
        --pais "colombia" \
        --contacto "WhatsApp: +57 ..." \
        --t-envio "Ciudad principal: 2 a 3 días ..." \
        --info-extra "Pago contra entrega y productos originales." \
        --producto "Serum X:hongos en las uñas" \
        --producto "Crema Y:piel flácida en el cuello" \
        --out /ruta/salida_CONFIG.json

También acepta un archivo de intake JSON (con lista "productos"):
    python3 build_config.py --intake intake.json --out salida.json

SEMÁNTICA DE EXIT CODES (v1.4.1):
    0 = config ENTREGABLE: placeholders llenos, todos los topes nativos y de
        negocio respetados, y cabe en LONG JSON (500.000, medido COMPACTO y
        escapado, que es lo que se escribe por API). El campo del bot SIEMPRE
        se crea/convierte a LONG JSON — el tope legado de 20.000 del tipo JSON
        se reporta como NOTA informativa, no como fallo.
    1 = ERROR DURO y NO se escribe archivo: placeholders sin llenar o llave
        simple desconocida, sin productos, producto malformado, o cualquier
        campo con tope nativo/de negocio EXCEDIDO (jamás truncar en silencio).
    2 = exceso real que muta la entrega, archivo SÍ escrito: config que no
        cabe ni en LONG JSON, o (con --pais distinto de colombia)
        colombianismos detectados que exigen adaptación manual.
"""
import argparse
import json
import os
import re
import sys

# El tope lo pone el TIPO del Bot Field, no la plataforma (medido por API 2026-07-25):
#   tipo JSON (var_type text/array) = 20.000   ·   tipo LONG JSON (longtext) = 500.000
# El campo se crea LONG JSON. LIMITE_JSON queda para avisar cuando el campo del
# cliente todavía sea del tipo viejo. Pasarse NO da error: la API responde 200 ok
# y guarda el JSON CORTADO, así que siempre hay que releer y comparar.
LIMITE_JSON = 20000        # techo duro del campo tipo JSON, medido en ESCAPADOS
LIMITE_ESCAPADO_SEGURO = 19000  # margen de trabajo (briefing 2026-08-07)
LIMITE_TOTAL = 500000
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(SCRIPT_DIR, "..", "assets", "template.json")

# Datos que la IA debe pedirle al cliente para completar la compra, por país
# y según su nomenclatura REAL de direcciones (briefing 2026-08-07).
# La plataforma solo acepta 7 países: COLOMBIA, ECUADOR, CHILE, MEXICO,
# PANAMA, PERU, PARAGUAY. El viejo esquema "internacional" con
# Estado/Colonia/Código Postal era un criterio de MÉXICO clonado: falso en
# Chile (comuna, sin CP), Ecuador, Perú (distrito), Panamá y Paraguay.
# El CP solo es REQUERIDO en México (define la zona de reparto).
DATOS_POR_PAIS = {
    "colombia": ("Nombre completo; Número de WhatsApp; Dirección exacta; "
                 "Barrio o punto de referencia; Ciudad; Departamento"),
    "mexico": ("Nombre completo; Número de WhatsApp; Dirección exacta; "
               "Colonia; Ciudad / Municipio; Estado; Código Postal"),
    "chile": ("Nombre completo; Número de WhatsApp; Dirección exacta "
              "(calle y número); Comuna; Región o referencia"),
    "ecuador": ("Nombre completo; Número de WhatsApp; Dirección exacta "
                "(calle principal y secundaria, o Mz y Villa/Solar); "
                "Barrio, ciudadela o referencia; Ciudad; Provincia"),
    "panama": ("Nombre completo; Número de WhatsApp; Dirección exacta o "
               "referencia clara; Barriada / urbanización o PH y apartamento; "
               "Corregimiento; Distrito; Provincia"),
    "peru": ("Nombre completo; Número de WhatsApp; Dirección exacta "
             "(calle/jirón y número, o Mz y Lote); Urbanización o AA.HH.; "
             "Distrito; Provincia; Departamento"),
    "paraguay": ("Nombre completo; Número de WhatsApp; Dirección (calle y "
                 "entre qué calles o casi qué esquina); Barrio; Ciudad; "
                 "Departamento; Referencia"),
}
# Vocabulario regional para las frases del prompt de venta (F3 2026-08-08: las
# frases colombianas de envio estaban QUEMADAS y sobrevivian al relleno).
REGION_POR_PAIS = {
    "colombia": "departamento", "mexico": "estado", "chile": "comuna",
    "ecuador": "provincia", "panama": "provincia", "peru": "distrito",
    "paraguay": "departamento",
}
DIRECCION_EJ_POR_PAIS = {
    "colombia": "calle, carrera, número", "mexico": "calle, número y colonia",
    "chile": "calle y número", "ecuador": "calle principal y secundaria",
    "panama": "calle o referencia clara", "peru": "calle o jirón y número",
    "paraguay": "calle y entre qué calles",
}

ALIAS_PAIS = {
    "co": "colombia", "méxico": "mexico", "mx": "mexico", "cl": "chile",
    "ec": "ecuador", "panamá": "panama", "pa": "panama", "perú": "peru",
    "pe": "peru", "py": "paraguay",
}


def datos_req_por_pais(pais, override=None):
    """Devuelve la lista de datos a solicitar al cliente según el país.

    Si se pasa `override`, se usa tal cual (lista manual del usuario).
    """
    if override:
        return override.strip()
    clave = (pais or "").strip().lower()
    clave = ALIAS_PAIS.get(clave, clave)
    if clave in DATOS_POR_PAIS:
        return DATOS_POR_PAIS[clave]
    # País fuera de los 7 que acepta la plataforma: avisar y usar el esquema
    # de Colombia (el patrón oro) como base neutra, nunca el de México.
    print(f"AVISO: '{pais}' no está entre los 7 países que acepta Chatea Pro "
          "(COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY). "
          "Confirma el país o pasa --datos-cliente con la lista correcta.")
    return DATOS_POR_PAIS["colombia"]


def cargar_template():
    with open(TEMPLATE, encoding="utf-8") as f:
        return json.load(f)


def parsear_productos(items):
    """Convierte ["Nombre:dolencia que trata", ...] en [(nombre, dolencia), ...].

    Acepta también dicts {"nombre":..., "dolencia":...} (intake JSON)."""
    out = []
    for it in items or []:
        if isinstance(it, dict):
            nombre, dolencia = (it.get("nombre") or "").strip(), (it.get("dolencia") or "").strip()
        else:
            nombre, _, dolencia = str(it).partition(":")
            nombre, dolencia = nombre.strip(), dolencia.strip()
        if not nombre or not dolencia:
            print(f"ERROR: producto mal formado: {it!r} — el formato es 'Nombre:dolencia que trata'.")
            sys.exit(1)
        out.append((nombre, dolencia))
    return out


def _pais_clave(pais):
    clave = (pais or "").strip().lower()
    return ALIAS_PAIS.get(clave, clave)


def rellenar_datos_envio(cfg):
    """Coherencia interna: la checklist/orden/confirmación de datos de envío del
    prompt de venta salen del MISMO pack de país que datos_req (antes estaban
    quemadas con el esquema de Colombia y contradecían a México)."""
    datos = [x.strip() for x in cfg["venta_conversacional"]["datos_req"].split(";") if x.strip()]
    checklist = "\n".join("[ ] " + d for d in datos) + "\n[ ] Pedido confirmado (producto + cantidad)"
    orden = " → ".join(datos) + " → Pedido"
    confirmacion = "\n".join(d.split("(")[0].strip() + ": ___" for d in datos)
    clave = _pais_clave(cfg["informacion_del_negocio"]["pais"])
    region = REGION_POR_PAIS.get(clave, "ciudad")
    direccion_ej = DIRECCION_EJ_POR_PAIS.get(clave, "calle y número")
    lista_corta = ", ".join(d.split("(")[0].strip().lower() for d in datos)

    def rellena(o):
        if isinstance(o, dict):
            return {k: rellena(v) for k, v in o.items()}
        if isinstance(o, str):
            return (o.replace("{{CHECKLIST_DATOS_ENVIO}}", checklist)
                     .replace("{{ORDEN_DATOS_ENVIO}}", orden)
                     .replace("{{CONFIRMACION_DATOS_ENVIO}}", confirmacion)
                     .replace("{{LISTA_DATOS_CORTA}}", lista_corta)
                     .replace("{{DATO_REGION}}", region)
                     .replace("{{DIRECCION_EJEMPLO}}", direccion_ej))
        return o
    return rellena(cfg)


def rellenar_guardarrail(cfg, productos):
    """Rellena los placeholders {{LISTA_DOLENCIAS}} y {{LISTA_PRODUCTOS_DOLENCIAS}}
    del guardarraíl anti-dolencias con los productos de LA TIENDA DESTINO."""
    lista_dolencias = ", ".join(d for _, d in productos)
    lineas = "\n".join(
        f"- {n}: trata {d}. Comentarios tipo 'tengo {d}', 'esto sirve para {d}' = cliente interesado."
        for n, d in productos)

    def rellena(o):
        if isinstance(o, dict):
            return {k: rellena(v) for k, v in o.items()}
        if isinstance(o, str):
            return (o.replace("{{LISTA_DOLENCIAS}}", lista_dolencias)
                     .replace("{{LISTA_PRODUCTOS_DOLENCIAS}}", lineas))
        return o
    return rellena(cfg)


# Llaves SIMPLES legítimas: las variables runtime de Chatea. Cualquier otra
# llave simple con pinta de token es un placeholder colado (ej: {DOLENCIA_1}).
RUNTIME_LEGITIMAS = {"NOMBRE_PRODUCTO", "DESCRIPCION_PRODUCTO"}


def validar_sin_placeholders(cfg):
    """Error DURO si queda CUALQUIER {{...}} (con espacios, minúsculas, guiones,
    lo que sea: [^{}]*) o una llave simple tipo token fuera de la whitelist
    runtime. El regex viejo [A-Z0-9_]+ dejaba pasar {{Hueco}}, {{ X }} y
    {DOLENCIA_1} — cazado por el verificador 2026-08-08."""
    texto = json.dumps(cfg, ensure_ascii=False)
    dobles = sorted(set(re.findall(r"\{\{[^{}]*\}\}", texto)))
    simples = sorted({m for m in re.findall(
        r"(?<!\{)\{([A-Za-z0-9_][A-Za-z0-9_ .\-]*)\}(?!\})", texto)
        if m not in RUNTIME_LEGITIMAS})
    if dobles or simples:
        print("!" * 62)
        if dobles:
            print(f"ERROR: placeholders {{{{...}}}} sin llenar: {', '.join(dobles)}")
        if simples:
            print("ERROR: llave simple desconocida: " + ", ".join("{%s}" % s for s in simples))
            print("       Las únicas llaves simples legítimas (runtime de Chatea) son:")
            print("       " + ", ".join("{%s}" % s for s in sorted(RUNTIME_LEGITIMAS)))
        print("       Un placeholder literal viajaría tal cual al bot del cliente.")
        print("!" * 62)
        sys.exit(1)


def construir(pais, contacto, t_envio, info_extra, datos_cliente=None, productos=None):
    cfg = cargar_template()
    # Solo se reemplaza la información del negocio. Los prompts quedan intactos.
    cfg["informacion_del_negocio"]["pais"] = pais
    cfg["informacion_del_negocio"]["contacto"] = contacto
    cfg["informacion_del_negocio"]["t_envio"] = t_envio
    cfg["informacion_del_negocio"]["info_extra"] = info_extra
    # Datos que la IA debe solicitar al cliente, según el país.
    cfg["venta_conversacional"]["datos_req"] = datos_req_por_pais(pais, datos_cliente)
    # Guardarraíl anti-dolencias: SIEMPRE con los productos de la tienda destino.
    cfg = rellenar_guardarrail(cfg, productos or [])
    # Datos de envío del prompt de venta: mismo pack de país que datos_req.
    cfg = rellenar_datos_envio(cfg)
    validar_sin_placeholders(cfg)
    return cfg


TOPES_NATIVOS = [
    # (ruta, tope, deliberado): deliberado=True EXCEDE a proposito (se pega por
    # JSON completo; prohibido guardar desde su formulario del panel).
    ("informacion_del_negocio.contacto", 200, False),
    ("informacion_del_negocio.t_envio", 200, False),
    ("informacion_del_negocio.info_extra", 500, False),
    ("comentarios_negativos.prompt_general", 10000, False),
    ("comentarios_negativos.ej_a_eliminar", 1000, False),
    ("comentarios_negativos.ej_a_no_eliminar", 1000, False),
    ("respuesta_publica.prompt", 3000, True),
    ("venta_conversacional.prompt", 8000, True),
    ("venta_conversacional.datos_req", 200, False),
]

# Lista DERIVADA DEL GREP DEL TEMPLATE (2026-08-08) — al editar el template,
# re-derivar. COP se quitó (nunca aparece); departamento/barrio/carrera son red
# de seguridad (se saltan si el término es legítimo en el datos_req del destino).
COLOMBIANISMOS = [
    ("pesos colombianos", r"\bpesos colombianos\b"),
    ("colombiano/a", r"\bcolombian[oa]s?\b"),
    ("Colombia", r"\bColombia\b"),
    ("Nequi", r"\bNequi\b"),
    ("Daviplata", r"\bDaviplata\b"),
    ("Bogotá", r"\bBogotá\b"),
    ("Medellín", r"\bMedellín\b"),
    ("Cali", r"\bCali\b"),
    ("Barranquilla", r"\bBarranquilla\b"),
    ("Bucaramanga", r"\bBucaramanga\b"),
    ("Pereira", r"\bPereira\b"),
    ("BGA", r"\bBGA\b"),
    ("Valle del Cauca", r"\bValle del Cauca\b"),
    ("Chapinero", r"\bChapinero\b"),
    ("Medallo", r"\bMedallo\b"),
    ("carrera", r"\bcarreras?\b"),
    ("departamento", r"\b[Dd]epartamentos?\b"),
    ("barrio", r"\b[Bb]arrios?\b"),
    ("$90.000", r"\$90\.000\b"),
    ("$150.000", r"\$150\.000\b"),
    ("310-555-7788", r"\b310-555-7788\b"),
]


def _campo(cfg, ruta):
    seccion, llave = ruta.split(".")
    return cfg[seccion][llave]


def validar_topes(cfg):
    """ERROR DURO (exit 1, SIN archivo) si un campo no-deliberado excede su tope
    nativo. Jamás truncar en silencio: el Save del panel cortaría el campo."""
    excesos = [(r, len(_campo(cfg, r)), tope)
               for r, tope, deliberado in TOPES_NATIVOS
               if not deliberado and len(_campo(cfg, r)) > tope]
    if excesos:
        print("!" * 62)
        for r, n, tope in excesos:
            print(f"ERROR: {r} mide {n} y su tope nativo es {tope} (+{n - tope}).")
        print("       NO se escribe archivo: recorta el dato de negocio o el")
        print("       numero de productos. Un Save del panel cortaria el campo.")
        print("!" * 62)
        sys.exit(1)


def detectar_colombianismos(cfg, pais):
    """Con --pais distinto de colombia, el template aun trae moneda/ciudades/
    jerga de Colombia. Se reportan como CHECKLIST de adaptacion manual."""
    if (pais or "").strip().lower() in ("colombia", "co"):
        return []
    texto = json.dumps(cfg, ensure_ascii=False)
    legit = cfg["venta_conversacional"]["datos_req"].lower()
    hallazgos = []
    for term, patron in COLOMBIANISMOS:
        if term.lower() in legit:
            continue  # vocabulario legítimo del país destino (ej: Departamento en Perú)
        n = len(re.findall(patron, texto))
        if n:
            hallazgos.append((term, n))
    return hallazgos


def reporte(cfg):
    out = json.dumps(cfg, ensure_ascii=False, indent=4)
    # Lo que se escribe por API es el JSON COMPACTO: medir contra el tope
    # LONG JSON (500.000) sobre esa forma, escapada (tilde=6, emoji=12).
    compacto = json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))
    escapado = len(json.dumps(compacto)[1:-1])
    print("=" * 62)
    print(f"LARGO indentado (para pegar en panel): {len(out)} crudos")
    print(f"LARGO compacto  (para escribir por API): {len(compacto)} crudos")
    print(f"LARGO ESCAPADO compacto (cuenta contra el techo): {escapado} / {LIMITE_TOTAL} (LONG JSON)")
    print("=" * 62)
    print(f"  pais: {cfg['informacion_del_negocio']['pais']}")
    print("  Campos con tope (len/tope). Un Save del panel CORTA lo que sobre:")
    for ruta, tope, deliberado in TOPES_NATIVOS:
        n = len(_campo(cfg, ruta))
        if n <= tope:
            print(f"    OK      {ruta}: {n} / {tope} (margen {(tope - n) / tope * 100:.0f}%)")
        elif deliberado:
            print(f"    EXCEDE  {ruta}: {n} / {tope} — DELIBERADO: se pega por JSON completo")
            print("            (el backend valida el total). PROHIBIDO guardar desde ese formulario.")
        else:
            print(f"    EXCEDE  {ruta}: {n} / {tope} — no deberia llegar aqui (validar_topes fallo antes)")
    if escapado > LIMITE_JSON:
        print()
        print(f"  NOTA: {escapado} escapados > {LIMITE_JSON}: esta config NO cabe en un bot field")
        print("        tipo JSON legado. El campo DEBE ser LONG JSON (500.000) — asi lo")
        print("        exige esta skill. Tras escribir por API: RELEER y comparar.")
    excede_total = escapado > LIMITE_TOTAL
    if excede_total:
        print()
        print("!" * 62)
        print(f"ERROR: ni LONG JSON aguanta esto ({escapado} > {LIMITE_TOTAL}).")
        print("!" * 62)
    return out, escapado, excede_total


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--intake", help="Archivo JSON con pais, contacto, t_envio, info_extra")
    p.add_argument("--pais")
    p.add_argument("--contacto")
    p.add_argument("--t-envio", dest="t_envio")
    p.add_argument("--info-extra", dest="info_extra")
    p.add_argument("--datos-cliente", dest="datos_cliente",
                   help="Lista manual de datos a pedir al cliente (separados por ;). "
                        "Si se omite, se genera según el país.")
    p.add_argument("--producto", action="append", dest="productos", metavar="'Nombre:dolencia'",
                   help="Producto de la tienda y la dolencia que trata (repetible). "
                        "Rellena el guardarrail anti-dolencias. Obligatorio: al menos 1.")
    p.add_argument("--out", required=True, help="Ruta del JSON de salida")
    a = p.parse_args()

    if a.intake:
        with open(a.intake, encoding="utf-8") as f:
            d = json.load(f)
        pais = d.get("pais", a.pais)
        contacto = d.get("contacto", a.contacto)
        t_envio = d.get("t_envio", a.t_envio)
        info_extra = d.get("info_extra", a.info_extra)
        datos_cliente = d.get("datos_cliente", a.datos_cliente)
        productos_raw = d.get("productos", a.productos)
    else:
        pais, contacto, t_envio, info_extra = a.pais, a.contacto, a.t_envio, a.info_extra
        datos_cliente = a.datos_cliente
        productos_raw = a.productos

    faltan = [n for n, v in [("pais", pais), ("contacto", contacto), ("t_envio", t_envio), ("info_extra", info_extra)] if not v]
    if faltan:
        print("Faltan datos del intake:", ", ".join(faltan))
        print("El skill debe preguntarlos antes de armar el JSON.")
        sys.exit(1)

    productos = parsear_productos(productos_raw)
    if not productos:
        print("ERROR: falta al menos un --producto 'Nombre:dolencia que trata' (o la lista")
        print("       'productos' en el intake). El guardarrail anti-dolencias es obligatorio")
        print("       y se rellena con los productos de LA TIENDA DESTINO, jamas de otra.")
        sys.exit(1)

    cfg = construir(pais, contacto, t_envio, info_extra, datos_cliente, productos)
    validar_topes(cfg)                      # exit 1 SIN archivo si un tope nativo revienta
    out, escapado, excede_total = reporte(cfg)
    destino = os.path.dirname(os.path.abspath(a.out))
    try:
        os.makedirs(destino, exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
    except OSError as e:
        print(f"ERROR: no se pudo escribir {a.out}: {e}")
        sys.exit(1)
    print(f"\nGuardado en: {a.out}")
    hallazgos = detectar_colombianismos(cfg, pais)
    if hallazgos:
        print()
        print("=" * 62)
        print(f"ADAPTACION MANUAL PENDIENTE — --pais {pais} pero el config trae colombianismos:")
        for term, n in hallazgos:
            print(f"  [ ] {term} (x{n})")
        print("  --pais hoy solo cubre datos_req + coherencia de datos de envio.")
        print("  Moneda, ciudades, jerga y medios de pago hay que adaptarlos a mano")
        print("  antes de entregar (rediseno multipais completo: proyecto aparte).")
        print("=" * 62)
    if excede_total or hallazgos:
        # Exit 2: exceso real que muta la entrega (no cabe ni en LONG JSON, o
        # requiere adaptacion manual de pais). El archivo SI se escribio.
        sys.exit(2)


if __name__ == "__main__":
    main()
