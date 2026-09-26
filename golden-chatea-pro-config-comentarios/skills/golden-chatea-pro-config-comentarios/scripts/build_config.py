#!/usr/bin/env python3
"""Genera el JSON de configuración del asistente de COMENTARIOS de Chatea Pro.

Pide 5 datos de intake (uno a la vez): país, contacto, tiempos de envío,
información adicional del negocio, y la lista de productos con la dolencia que
trata cada uno (guardarraíl anti-dolencias, --producto obligatorio y repetible).

Datos que la IA pide al cliente (datos_req): se generan solos según el país.
Ver DATOS_POR_PAIS (8 packs: COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU,
PARAGUAY, GUATEMALA; ARGENTINA y BRASIL aceptados sin pack — cada uno con su nomenclatura real de direcciones; no existe un
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

# TECHO DEL CAMPO — REMEDIDO EN VIVO EL 2026-09-22, y la corrección importa:
# el tope de 20.000 se mide en CRUDOS, no en escapados. Durante semanas este
# script lo trató como escapados y de ahí salió un "techo práctico de ~17.000
# crudos" que era falso y que RECHAZABA configuraciones buenas con exit 1.
#
#   MEDIDO en un espacio real, campo [Comentarios] Configuracion General (array):
#     13.004 crudos            -> guarda
#     19.617 crudos = 21.457 escapados -> guarda por API y se relee IDÉNTICO
#     20.811 crudos            -> error 500 al guardar desde el panel
#
# Es decir: 21.457 escapados viven sin problema. La unidad es el CRUDO.
# El tipo del campo (array) NO se cambia por API y NO hace falta cambiarlo:
# el campo array aguanta la configuración completa.
LIMITE_CRUDO = 20000         # techo del bot field, EN CRUDOS (medido 2026-09-22)
MARGEN_SEGURO = 400          # se entrega por debajo de 19.600 crudos
LIMITE_TOTAL = 500000        # tipo longtext, para el caso raro de un campo así
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(SCRIPT_DIR, "..", "assets", "template.json")

# Datos que la IA debe pedirle al cliente para completar la compra, por país
# y según su nomenclatura REAL de direcciones (briefing 2026-08-07).
# La plataforma acepta 10 países (REMEDIDO 2026-08-29 contra el bundle vivo;
# deroga el "solo 7"): los 7 con pack propio + GUATEMALA, ARGENTINA y BRASIL.
# Guatemala YA tiene pack aquí (esquema de ZONAS, tomado de la skill hermana
# golden-chatea-pro-validacion-direcciones, que lo tiene medido). Argentina y
# Brasil están aceptados por la plataforma pero AÚN SIN PACK: se declaran para
# no mentirle al usuario diciendo que su país no existe, y se le pide la lista
# con --datos-cliente en vez de darle la nomenclatura de otro país.
# El viejo esquema "internacional" con
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
    "guatemala": ("Nombre completo; Número de WhatsApp; Dirección exacta con "
                  "ZONA (ej. 5a avenida 12-34, Zona 10); Colonia, residenciales "
                  "o aldea si es área rural; Municipio; Departamento"),
}
# Aceptados por la plataforma pero SIN pack de direcciones propio: se les pide la
# lista al negocio en vez de heredarles la nomenclatura de otro país.
SIN_PACK = {"argentina", "brasil"}
# Vocabulario regional para las frases del prompt de venta (F3 2026-08-08: las
# frases colombianas de envio estaban QUEMADAS y sobrevivian al relleno).
REGION_POR_PAIS = {
    "colombia": "departamento", "mexico": "estado", "chile": "comuna",
    "ecuador": "provincia", "panama": "provincia", "peru": "distrito",
    "paraguay": "departamento", "guatemala": "departamento",
}
DIRECCION_EJ_POR_PAIS = {
    "colombia": "calle, carrera, número", "mexico": "calle, número y colonia",
    "chile": "calle y número", "ecuador": "calle principal y secundaria",
    "panama": "calle o referencia clara", "peru": "calle o jirón y número",
    "paraguay": "calle y entre qué calles",
    "guatemala": "avenida o calle con número y ZONA",
}

# Palabra LOCAL con la que el cliente dice que un producto es malo o no original.
# El clasificador stock no la entiende y deja pasar justo el comentario que más
# duele. Origen: clase M7 de Kevin Galeano (2026-09-02) — "chafa" en Guatemala le
# pasaba seguido y tuvo que agregarla A MANO EN VIVO durante la clase.
#
# 🔴 HONESTIDAD SOBRE LA PROCEDENCIA DE ESTAS PALABRAS, porque quien las use tiene
# derecho a saber de dónde salen:
#   · GUATEMALA está MEDIDA: "chafa" la dijo Kevin en la clase, sobre su propia
#     operación, tras verla llegar repetida.
#   · EL RESTO ES SEMILLA, NO DATO. Salen de conocimiento general del español
#     regional, NO de los comentarios reales de ninguna tienda. Se intentó
#     verificarlas contra la operación viva de Golden y NO SE PUDO: la API de
#     Chatea tiene 227 rutas y NINGUNA de comentarios (medido 2026-09-05), y
#     /flow/conversations/data devuelve 0 registros en ese espacio, tanto global
#     como por suscriptor, con control positivo hecho (11.626 suscriptores sí se
#     leen, así que el token funciona y el vacío es real).
#
# POR ESO EL DISEÑO CAMBIÓ: una lista fija de argot es la solución equivocada, y
# lo dice el propio método de Kevin — "leo los comentarios, detecto el patrón,
# ajusto". La semilla arranca el trabajo; la palabra que MANDA es la que el dueño
# ve en SUS comentarios y pasa con --despectivo. Lo que se pase por bandera
# REEMPLAZA a la semilla, no se suma, para que nadie herede argot que no es suyo.
DESPECTIVO_POR_PAIS = {
    "guatemala": "chafa",          # MEDIDA en la clase M7, caso real de Kevin
    # --- de aquí abajo, SEMILLA sin verificar en comentarios reales ---
    "colombia": "chiviado, corroncho, cacharro",
    "mexico": "chafa, pirata, corriente",
    "chile": "trucho, chanta, ordinario",
    "ecuador": "bamba, feque, cachina",
    "panama": "pirata, cachivache",
    "peru": "bamba, cachina",
    "paraguay": "trucho, pirata",
}
DESPECTIVO_MEDIDOS = {"guatemala"}   # los únicos con fuente real
DESPECTIVO_GENERICO = "chafa, trucho, bamba, chiviado, pirata, corriente"

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
    # 🔴 SIN PACK NO SE FABRICA. Hasta el 2026-09-06 las dos ramas de abajo avisaban de que
    # heredar la nomenclatura de otro país produce direcciones no entregables... y a dos
    # líneas hacían `return DATOS_POR_PAIS["colombia"]`. Medido: argentina y bolivia salían
    # con "Barrio…; Ciudad; Departamento" colombiano. En Argentina no hay departamentos.
    # La autoprueba daba 24/24 porque comprobaba EL AVISO, no EL RESULTADO.
    #
    # El país NO se rechaza —eso lo prohíbe la doctrina de FER, el país es parámetro y no
    # puerta—: lo que se rechaza es INVENTAR sus campos de dirección. Un hueco declarado se
    # llena; una dirección fabricada llega mal y nadie sabe por qué.
    #
    # 🔴 CORREGIDO EL 2026-09-07: este mensaje decía "Pregúntale al negocio qué campos lleva
    # una dirección ahí", y eso contradice de frente la ley de FER del 06-sep: "La jerga y la
    # configuración de las direcciones NO se le pregunta a la gente, porque precisamente para
    # eso es la skill. Tú tienes que ir a Internet, revisar, estudiar, analizar, extraer esa
    # información y configurarla." El bloqueo estaba bien; el SIGUIENTE PASO que ordenaba
    # estaba mal, y un mensaje de error es una instrucción: se obedece tal cual.
    # Preguntar lo averiguable es cobrarle al negocio nuestro trabajo, y encima arriesga que
    # conteste mal y esa respuesta mala quede escrita como regla.
    conocido = "tiene pack de direcciones pendiente" if clave in SIN_PACK else \
        "todavía no tiene pack de direcciones en esta skill"
    sys.exit(
        f"🔴 '{pais}' {conocido}. El país NO está rechazado: lo que falta es un dato.\n"
        f"   NO se hereda el pack de otro país: produce direcciones no entregables.\n"
        f"   La forma de la dirección se INVESTIGA, NO se le pregunta al negocio (ley de FER,\n"
        f"   2026-09-06). Averigua en fuentes del país —correos/servicio postal, webs de las\n"
        f"   transportadoras, y sitios donde gente real escribe direcciones de verdad— qué\n"
        f"   campos la componen, en qué orden y cómo se abrevian. Tres fuentes independientes.\n"
        f"   Lo que no se logre confirmar se marca NO VERIFICADO y SOLO eso se le confirma al\n"
        f"   negocio, diciéndole por qué se le pregunta.\n"
        f"   Con la lista en la mano, vuelve a correr con:\n"
        f"     --datos-cliente \"Nombre completo; Número de WhatsApp; …\"\n"
        f"   Y entrega el pack investigado con sus fuentes, para que el siguiente negocio de\n"
        f"   ese país no obligue a repetir la investigación entera.")


def cargar_template():
    try:
        with open(TEMPLATE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: no se encontró la plantilla en {TEMPLATE}.")
        print("       La skill está corrupta o incompleta (falta assets/template.json).")
        print("       Reinstala golden-chatea-pro-config-comentarios y vuelve a intentar.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: assets/template.json no es JSON válido ({e}).")
        print("       La skill está corrupta. Reinstala golden-chatea-pro-config-comentarios.")
        sys.exit(1)


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


def rellenar_datos_envio(cfg, despectivo_real=None):
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
    if despectivo_real:
        despectivo = despectivo_real.strip()
    else:
        despectivo = DESPECTIVO_POR_PAIS.get(clave, DESPECTIVO_GENERICO)
        if clave not in DESPECTIVO_MEDIDOS:
            print(f"AVISO: la palabra despectiva local de '{clave}' es SEMILLA, no dato "
                  "medido en comentarios reales. Mira TUS comentarios y pasa la que de "
                  "verdad te llega con --despectivo \"palabra1, palabra2\". "
                  "El metodo de Kevin: leo, detecto el patron, ajusto.")

    def rellena(o):
        if isinstance(o, dict):
            return {k: rellena(v) for k, v in o.items()}
        if isinstance(o, str):
            return (o.replace("{{CHECKLIST_DATOS_ENVIO}}", checklist)
                     .replace("{{ORDEN_DATOS_ENVIO}}", orden)
                     .replace("{{CONFIRMACION_DATOS_ENVIO}}", confirmacion)
                     .replace("{{LISTA_DATOS_CORTA}}", lista_corta)
                     .replace("{{DATO_REGION}}", region)
                     .replace("{{DIRECCION_EJEMPLO}}", direccion_ej)
                     .replace("{{DESPECTIVO_LOCAL}}", despectivo))
        return o
    return rellena(cfg)


TOPE_DOLENCIAS = 12   # cuántas dolencias distintas entran en el guardarraíl


def rellenar_guardarrail(cfg, productos):
    """Rellena {{LISTA_DOLENCIAS}} y {{LISTA_PRODUCTOS_DOLENCIAS}} con las
    DOLENCIAS de la tienda destino — nunca con los nombres de sus productos.

    DOS DEFECTOS QUE ESTO CORRIGE (2026-09-22):

    1. CADUCIDAD. La versión anterior escribía una línea por producto con su
       NOMBRE ("- Tag Recede: trata verrugas..."). El día que la tienda saca ese
       producto, el clasificador sigue citándolo y nadie se entera, porque el bot
       no da error: simplemente razona sobre un catálogo que ya no existe.

    2. NO ESCALABA. Con ~20 productos el bloque ya pesaba miles de caracteres y
       con ~50 reventaba el campo entero. Un catálogo grande rompía la skill.

    La clave: al clasificador NO le hace falta saber qué producto trata qué. Le
    hace falta reconocer la FORMA de la frase con la que alguien nombra su
    problema. Por eso se deduplican las dolencias y se cortan en TOPE_DOLENCIAS:
    el guardarraíl deja de crecer con el catálogo y el prompt es estable tenga la
    tienda 3 productos o 1.000."""
    vistas, unicas = set(), []
    for _, d in productos:
        clave = d.strip().lower()
        if clave and clave not in vistas:
            vistas.add(clave)
            unicas.append(d.strip())
    recortadas = unicas[:TOPE_DOLENCIAS]
    lista_dolencias = ", ".join(recortadas)
    if len(unicas) > TOPE_DOLENCIAS:
        lista_dolencias += (f", y cualquier otra condición del mismo tipo "
                            f"({len(unicas) - TOPE_DOLENCIAS} más que esta lista no enumera)")
    lineas = ("Ninguna de estas frases se elimina jamás, y no dependen del catálogo: "
              "cualquier frase del mismo tipo entra aquí aunque los productos cambien.\n"
              + "; ".join(f"tengo {d}" for d in recortadas)
              + "; llevo años con esto; ya probé de todo.")

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


def cargar_overrides_no_vip():
    """DEROGADA el 2026-09-22. Cargaba los prompts recortados de la via NO VIP.

    Ya no existe esa via: la plantilla actual cabe entera respetando los nueve
    topes nativos, asi que una sola base sirve a todos. Se conserva la funcion
    (no el asset) para que, si algo antiguo la llama, falle RUIDOSAMENTE en vez
    de devolver silenciosamente unos prompts que ya no existen."""
    print("ERROR: la via NO VIP fue derogada (FER 2026-09-22). Hay UNA sola base,")
    print("       que cabe en los topes nativos. No hay overrides que cargar.")
    sys.exit(1)


def construir(pais, contacto, t_envio, info_extra, datos_cliente=None, productos=None,
              negocio=None,
              aut_link=None, aut_precio=None, vip=True, despectivo=None):
    cfg = cargar_template()
    # BASE UNICA (FER, 2026-09-22). Ya NO hay via VIP en la configuracion general.
    # Antes habia dos entregables: uno completo que se pegaba como JSON en Campos
    # de Bot excediendo topes a proposito, y uno recortado para quien pega en el
    # formulario. La bifurcacion existia porque la plantilla vieja NO CABIA
    # (3.895 > 3.000 y 10.771 > 8.000, ~22.7k en total).
    # La plantilla actual cabe entera respetando los nueve topes nativos, asi que
    # la variante recortada perdio su razon de ser: una sola base sirve a todos,
    # se pegue por formulario o por JSON. El VIP ahora vive solo en el manejo de
    # PRODUCTOS, que es otra skill (golden-chatea-pro-producto-comentarios).
    # Panel "Autorizaciones" de Respuesta pública. Son DECISIONES DE VENTA, no
    # detalles: definen si el comentario empuja al privado o saca al cliente del
    # anuncio. Doctrina medida en la clase M7 de Kevin (2026-09-02):
    #   enlace NO  -> el asistente cierra en la misma conversación; mandarlo a la
    #                 web lo enfría y se pierde el hilo caliente.
    #   precio SÍ  -> el precio filtra curiosos EN PÚBLICO, y aun así el asistente
    #                 abre el privado solo, así que no se pierde el lead.
    # Se dejan configurables porque quien vende por landing sí quiere el enlace.
    if aut_link is not None:
        cfg["respuesta_publica"]["aut_link_pub"] = "sí" if aut_link else "no"
    if aut_precio is not None:
        cfg["respuesta_publica"]["aut_precio_pub"] = "sí" if aut_precio else "no"
    # NOMBRE DEL NEGOCIO. Es la primera pieza de la parte dinamica y durante mucho
    # tiempo NO existio como parametro: el ROL del clasificador decia "esta tienda"
    # mientras el espacio vivo decia el nombre real, asi que la skill y el espacio
    # se separaban desde la primera linea del prompt. Si no se pasa, se queda el
    # generico, que es correcto aunque menos concreto — nunca se hornea un nombre.
    if negocio:
        cfg = {k: ({kk: (vv.replace("{{NOMBRE_NEGOCIO}}", negocio) if isinstance(vv, str) else vv)
                    for kk, vv in v.items()} if isinstance(v, dict) else v)
               for k, v in cfg.items()}
    else:
        cfg = {k: ({kk: (vv.replace("{{NOMBRE_NEGOCIO}}", "esta tienda") if isinstance(vv, str) else vv)
                    for kk, vv in v.items()} if isinstance(v, dict) else v)
               for k, v in cfg.items()}
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
    cfg = rellenar_datos_envio(cfg, despectivo_real=despectivo)
    validar_sin_placeholders(cfg)
    return cfg


TOPES_NATIVOS = [
    # (ruta, tope, deliberado). Desde 2026-09-22 NINGUN campo es "deliberado":
    # FER derogo la via VIP de la configuracion general y quedo UNA sola base,
    # que cabe entera respetando todos los topes nativos. El tercer elemento se
    # conserva en False para no romper a quien lea la tupla.
    #
    # OJO, LA COSTURA QUE NADIE VE: estos topes SUMAN 24.100 y el campo aguanta
    # 20.000. El panel valida caja por caja y NUNCA la suma, asi que se pueden
    # llenar las nueve en verde y que el guardado reviente con un 500 sin decir
    # por que. Respetar el tope de cada campo NO garantiza que el conjunto entre:
    # eso lo decide el gate de LIMITE_CRUDO de mas abajo.
    ("informacion_del_negocio.contacto", 200, False),
    ("informacion_del_negocio.t_envio", 200, False),
    ("informacion_del_negocio.info_extra", 500, False),
    ("comentarios_negativos.prompt_general", 10000, False),
    ("comentarios_negativos.ej_a_eliminar", 1000, False),
    ("comentarios_negativos.ej_a_no_eliminar", 1000, False),
    ("respuesta_publica.prompt", 3000, False),
    ("venta_conversacional.prompt", 8000, False),
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


def validar_topes(cfg, vip=True):
    """ERROR DURO (exit 1, SIN archivo) si un campo excede su tope nativo.
    Jamás truncar en silencio: el Save del panel cortaría el campo.

    Desde 2026-09-22 TODOS los topes bloquean, sin excepción: se acabaron los
    campos "deliberados". El parámetro vip se conserva para no romper llamadas
    antiguas y ya no cambia nada."""
    excesos = [(r, len(_campo(cfg, r)), tope)
               for r, tope, deliberado in TOPES_NATIVOS
               if (not deliberado or not vip) and len(_campo(cfg, r)) > tope]
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


def reporte(cfg, vip=True):
    out = json.dumps(cfg, ensure_ascii=False, indent=4)
    # Lo que se escribe por API es el JSON COMPACTO: medir contra el tope
    # LONG JSON (500.000) sobre esa forma, escapada (tilde=6, emoji=12).
    compacto = json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))
    escapado = len(json.dumps(compacto)[1:-1])
    tope_trabajo = LIMITE_CRUDO - MARGEN_SEGURO
    print("=" * 62)
    print(f"LARGO indentado (para pegar en panel): {len(out)} crudos")
    print(f"LARGO COMPACTO — ES EL QUE CUENTA: {len(compacto)} / {LIMITE_CRUDO} crudos "
          f"(margen {LIMITE_CRUDO - len(compacto)})")
    if len(compacto) > tope_trabajo:
        print(f"    SE PASA del limite de trabajo ({tope_trabajo}). No se entrega.")
    print(f"escapado: {escapado} — informativo. NO es la unidad del techo: medido")
    print("  el 2026-09-22, 21.457 escapados viven en el campo sin problema.")
    print("=" * 62)
    print(f"  pais: {cfg['informacion_del_negocio']['pais']}")
    # Los dos interruptores del panel Autorizaciones se IMPRIMEN siempre: son
    # decisiones de venta y un interruptor que nadie ve es uno que nadie revisa.
    rp = cfg.get("respuesta_publica", {})
    link, precio = rp.get("aut_link_pub", "?"), rp.get("aut_precio_pub", "?")
    print(f"  Autorizaciones -> enlace en respuesta pública: {link} · precio: {precio}")
    if link == "sí":
        print("    AVISO: con el enlace encendido el cliente sale del anuncio hacia la web "
              "y se enfría. Déjalo en 'no' si quieres que el asistente cierre en el chat.")
    print("  BASE UNICA: sirve igual pegando campo por campo en el formulario que")
    print("  pegando el JSON en Campos de Bot. Ya no hay via VIP (FER 2026-09-22).")
    print("  Campos con tope (len/tope). Un Save del panel CORTA lo que sobre:")
    for ruta, tope, deliberado in TOPES_NATIVOS:
        deliberado = False   # ya no existen excesos permitidos
        n = len(_campo(cfg, ruta))
        if n <= tope:
            print(f"    OK      {ruta}: {n} / {tope} (margen {(tope - n) / tope * 100:.0f}%)")
        elif deliberado:
            print(f"    EXCEDE  {ruta}: {n} / {tope} — DELIBERADO: se pega por JSON completo")
            print("            (el backend valida el total). PROHIBIDO guardar desde ese formulario.")
        else:
            print(f"    EXCEDE  {ruta}: {n} / {tope} — no deberia llegar aqui (validar_topes fallo antes)")
    if len(compacto) > LIMITE_CRUDO - MARGEN_SEGURO:
        print()
        print(f"  NOTA: {len(compacto)} crudos supera el limite de trabajo")
        print(f"        ({LIMITE_CRUDO - MARGEN_SEGURO}). El guardado desde el panel devolveria")
        print("        ERROR 500 y abortaria el campo entero. Hay que recortar.")
    print("  Tras escribir por API: RELEER del servidor y comparar. Es la unica prueba.")
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
    p.add_argument("--negocio", help="Nombre del negocio tal como debe nombrarlo el bot "
                        "(ej: Golden Group). Entra en el ROL del clasificador. Si se omite "
                        "queda el generico \"esta tienda\": correcto, pero menos concreto.")
    p.add_argument("--out", required=True, help="Ruta del JSON de salida")
    p.add_argument("--destino", choices=["array", "longjson"], default="array",
                   help="Tipo REAL del bot field destino. Por defecto 'array', que es lo que "
                        "son los campos de Comentarios y lo que NO hay que cambiar: medido el "
                        "2026-09-22, un campo array guarda 19.617 crudos y los devuelve "
                        "idénticos. El gate mide CRUDOS contra 20.000, no escapados. Pasa "
                        "'longjson' solo si verificaste en el servidor que el campo es longtext.")
    p.add_argument("--vip", choices=["si", "no"], default="no",
                   help="DEROGADO el 2026-09-22 por orden de FER: ya no hay vía VIP en la "
                        "configuración general, hay UNA sola base que cabe en los topes "
                        "nativos y sirve igual por formulario que por JSON. Se sigue "
                        "aceptando para no romper llamadas antiguas, pero no cambia nada y "
                        "pasar 'si' imprime un aviso. El VIP hoy vive solo en el manejo de "
                        "PRODUCTOS, que es la skill golden-chatea-pro-producto-comentarios.")
    p.add_argument("--despectivo",
                   help="Palabra o palabras LOCALES con las que TUS clientes dicen que el "
                        "producto es malo o no original, separadas por coma. Sale de MIRAR tus "
                        "comentarios, no de una lista generica: reemplaza la semilla del pack de "
                        "pais. Kevin tuvo que agregar 'chafa' a mano en vivo por esto mismo.")
    p.add_argument("--aut-link", dest="aut_link", choices=["si", "no"],
                   help="Autorizaciones: enviar el ENLACE en la respuesta pública. "
                        "Por defecto se respeta el template. Ponlo en 'no' si quieres que el "
                        "asistente cierre en la misma conversación (recomendado cuando el "
                        "canal de cierre es el propio chat); 'si' solo si vendes por landing.")
    p.add_argument("--aut-precio", dest="aut_precio", choices=["si", "no"],
                   help="Autorizaciones: enviar el PRECIO en la respuesta pública. "
                        "'si' filtra curiosos en público sin perder el lead, porque el "
                        "asistente abre el privado igual.")
    a = p.parse_args()

    if a.intake:
        try:
            with open(a.intake, encoding="utf-8") as f:
                d = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: no se encontró el archivo de intake {a.intake}.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: {a.intake} no es JSON válido ({e}).")
            sys.exit(1)
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

    aut_link = None if a.aut_link is None else (a.aut_link == "si")
    aut_precio = None if a.aut_precio is None else (a.aut_precio == "si")
    vip = (a.vip == "si")
    if vip:
        print("AVISO: --vip esta DEROGADO desde el 2026-09-22 y no cambia la salida.")
        print("       Hay UNA sola base y cabe en los topes nativos. Para el manejo")
        print("       VIP de productos, usa golden-chatea-pro-producto-comentarios.")
    cfg = construir(pais, contacto, t_envio, info_extra, datos_cliente, productos,
                    negocio=a.negocio,
                    aut_link=aut_link, aut_precio=aut_precio, vip=vip,
                    despectivo=a.despectivo)
    validar_topes(cfg, vip=vip)                      # exit 1 SIN archivo si un tope nativo revienta
    out, escapado, excede_total = reporte(cfg, vip=vip)
    crudo = len(json.dumps(cfg, ensure_ascii=False, separators=(",", ":")))
    if a.destino == "array" and crudo > LIMITE_CRUDO - MARGEN_SEGURO:
        print()
        print("!" * 62)
        print(f"ERROR: {crudo} crudos supera el limite de trabajo "
              f"({LIMITE_CRUDO - MARGEN_SEGURO} = {LIMITE_CRUDO} menos {MARGEN_SEGURO} de margen).")
        print("       El campo NO trunca en silencio: el panel devuelve ERROR 500 y")
        print("       aborta el guardado del campo entero (medido 2026-09-22: 19.617")
        print("       crudos guarda y se relee identico; 20.811 crudos da 500).")
        print("       Se recorta por ORDEN DE MENOR VALOR, nunca de la rotacion")
        print("       anti-baneo ni de los criterios de borrado:")
        print("         1. justificacion economica escrita para humanos")
        print("         2. ejemplos atados a NOMBRES de producto (ademas caducan)")
        print("         3. repeticiones literales de la misma lista")
        print("         4. campos de negocio: contacto, tiempos de envio, info extra")
        print("       No se escribio ningun archivo.")
        print("!" * 62)
        sys.exit(1)
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
