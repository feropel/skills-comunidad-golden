#!/usr/bin/env python3
"""
CLASIFICADOR · golden-chatea-operacion

Corre los controles del catalogo (references/clasificacion.md) sobre un DUMP producido por
extraer.py y emite hallazgos con evidencia citada del hilo real, mas cobertura medida.

Uso:
    python3 clasificar.py <DUMP.json> [--json salida.json] [--modo cod|prepago]

NO escribe nada en Chatea. Clasifica y reporta.

`--modo` declara si el espacio vende contra entrega (cod) o con pago anticipado (prepago). Sin
declararlo, cualquier mencion de pago anticipado en boca del bot se reporta como DUDA en vez de
como fallo confirmado -- nunca se asume el modelo de pago.

Si la COMPUERTA DE CORDURA se activa, o si el denominador de la Fase 1 no cuadra, el script
NO IMPRIME el informe normal (universo + hallazgos + cobertura completos): imprime solo el
aviso de aborto y sale con codigo distinto de cero. Ver references/clasificacion.md.

CAMPOS REALES DEL API (confirmados por medicion de produccion, ver
scripts/extraer.py y references/api.md para el detalle y la fuente de cada uno):
  - direccion del mensaje y notas de pixel: campo `type`, valores "in" / "out" / "note".
  - contenido de texto: campo `content`.
  - tiempo: campo `ts` UNICAMENTE (`created_at` y `date` llegan vacios, medido 6.911 de
    6.911 mensajes en otro espacio -- no son un fallback util, son ruido).
  - `msg_type` (valores text/audio/feed/button_template) y `payload.transcribed_text` son
    del encargo original de esta skill, un eje DISTINTO al de `type`: uno dice quien habla,
    el otro dice de que esta hecho el mensaje. Los dos se leen.
Sobre `type`/`content`/`ts` no queda duda: estan medidos contra el servidor real por
`golden-logistica-diaria/scripts/barrer_chats.py` y `analizar_conversaciones.py`, que barren
el MISMO endpoint. Por eso son la deteccion PRIMARIA aqui, con alternativas conocidas de otras
integraciones tipo uChat como respaldo SECUNDARIO, nunca al reves.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SEV = {"MUERTO": "🔴", "RIESGO": "🟠", "HUECO": "🟡", "DUDA": "🔵"}

UMBRAL_TARDANZA_MIN = 30
UMBRAL_SIN_RESPUESTA_MUERTO_MIN = 120     # SKILL.md: MUERTO es "> 2 horas"
UMBRAL_COMPUERTA = 0.90

MODOS_VALIDOS = ("cod", "prepago")

FRASES_PROHIBIDAS_COD = [
    "pago anticipado", "pago adelantado", "transferencia antes de despachar",
    "pagar antes de recibir", "debes pagar por adelantado", "consignar antes",
]

PATRON_INTERROGATIVO = re.compile(
    r"\?|\b(que|qué|como|cómo|cuando|cuándo|donde|dónde|cuanto|cuánto|cual|cuál)\b",
    re.IGNORECASE)

FALLBACK_GENERICO = [
    "no entendi", "no entendí", "puedes reformular", "no logro entender",
    "podrias repetir", "podrías repetir",
]

PALABRAS_OBJECION_PRECIO = re.compile(
    r"\b(caro|costoso|muy alto el precio|no tengo esa plata|no me alcanza)\b", re.IGNORECASE)
PALABRAS_OBJECION_ENVIO = re.compile(
    r"env[ií]o muy caro|demora mucho|no llega", re.IGNORECASE)
PALABRAS_OBJECION_DESCONFIANZA = re.compile(
    r"\b(estafa|desconf[ií]o|es real esto)\b", re.IGNORECASE)

CAMPOS_TS = ("ts", "timestamp", "created_at", "date", "fecha", "sent_at")

# ------------------------------------------------------------------------------------- R6
# COHERENCIA INTRA-CHAT (sin Dropi). Heuristica declarada, NO certeza absoluta (asi lo pide
# el control): compara lo que el CLIENTE dijo sobre un atributo concreto y variable del
# producto (color/talla/cantidad) contra lo que el mensaje final de RESUMEN/CONFIRMACION del
# bot dice sobre ese mismo atributo -- todo dentro del MISMO hilo, sin tocar Dropi/Shopify.
# Distinto de R5 (que contrasta contra la FICHA REAL del producto, fuera de alcance aqui).

# Colores comunes en espanol, canonizados (variantes de genero/acento -> una sola forma).
# Incluye la paleta de canas/cabello (castano/rubio/caoba/canoso/cobrizo/ceniza) porque el
# catalogo real medido en produccion (Fibra Capilar Toppik, ver verificacion adversarial
# 2026-08-21) usa esos nombres, no los colores "de ropa" que trae la lista base. Diccionario
# razonable, NO exhaustivo -- declarado como heuristica en clasificacion.md, no como catalogo
# cerrado: una tienda con su propia paleta puede tener nombres que esta lista no cubre.
CANON_COLOR = {
    "rojo": "rojo", "roja": "rojo",
    "azul": "azul",
    "verde": "verde",
    "amarillo": "amarillo", "amarilla": "amarillo",
    "negro": "negro", "negra": "negro",
    "blanco": "blanco", "blanca": "blanco",
    "rosado": "rosado", "rosada": "rosado", "rosa": "rosado",
    "morado": "morado", "morada": "morado", "violeta": "morado",
    "gris": "gris",
    "cafe": "cafe", "café": "cafe", "marron": "cafe", "marrón": "cafe",
    "dorado": "dorado", "dorada": "dorado",
    "plateado": "plateado", "plateada": "plateado",
    "naranja": "naranja",
    "celeste": "celeste",
    "beige": "beige",
    "turquesa": "turquesa",
    "vino": "vino", "vinotinto": "vino",
    "fucsia": "fucsia",
    "lila": "lila",
    "nude": "nude",
    "castano": "castano", "castaño": "castano",
    "chocolate": "chocolate",
    "rubio": "rubio", "rubia": "rubio",
    "caoba": "caoba",
    "canoso": "canoso", "canosa": "canoso", "cano": "canoso", "cana": "canoso",
    "cobrizo": "cobrizo", "cobriza": "cobrizo",
    "ceniza": "ceniza",
    "platino": "platino",
}
_ALTERNATIVAS_COLOR = "|".join(sorted(CANON_COLOR.keys(), key=len, reverse=True))
# LEAD-IN obligatorio ("color X" / "en X" / "a X", p.ej. "cambialo a rojo"): medido contra
# produccion (verificacion
# adversarial 2026-08-21) -- sin el lead-in, colores que tambien son palabras corrientes del
# espanol ("vino" el verbo, "cafe" la bebida, "rosa" un nombre de persona, "gris" el clima,
# "naranja" la fruta) generaban MUERTO falso sobre hilos reales (0 aciertos, varios falsos
# positivos en 1.829 hilos medidos). Costo declarado: baja el recall (un "mandeme el negro"
# suelto, sin "en"/"color" antes, ya no se lee) a cambio de no acusar en falso -- mismo
# criterio de la skill en general (preferir DUDA/silencio a una acusacion sin base).
PATRON_COLOR = re.compile(
    r"\b(?:color|en|a)\s+(" + _ALTERNATIVAS_COLOR + r")\b", re.IGNORECASE)
# Talla: SOLO valores reconocidos de la vida real (letras de talla de ropa o numero de 1-2
# digitos de calzado/anillo) -- nunca "cualquier palabra corta que sigue a 'talla'". Medido
# en produccion: sin esta lista, "no se cual es mi talla" capturaba talla='LA', "que talla me
# recomienda" capturaba talla='ME'.
_VALORES_TALLA = r"xxxl|xxl|xl|xs|s|m|l|\d{1,2}"
PATRON_TALLA = re.compile(r"\btalla\s*[:\s]?\s*(" + _VALORES_TALLA + r")\b", re.IGNORECASE)
PATRON_NUMERO_CALZADO = re.compile(r"\bn[uú]mero\s*[:\s]?\s*(\d{2,3})\b", re.IGNORECASE)
PATRON_CANTIDAD_UNIDAD = re.compile(
    r"\b(\d{1,3})\s*(unidades?|pares?|combos?|paquetes?)\b", re.IGNORECASE)
PATRON_CANTIDAD_DECLARADA = re.compile(r"\bcantidad\s*[:\s]?\s*(\d{1,3})\b", re.IGNORECASE)
# Cantidad escrita en palabras (1-10): "quiero dos unidades" no tenia cobertura -- declarado
# como limite en clasificacion.md para lo que quede fuera (mas de 10, u otras formas).
NUMEROS_ESCRITOS = {
    "un": "1", "uno": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9", "diez": "10",
}
PATRON_CANTIDAD_ESCRITA = re.compile(
    r"\b(" + "|".join(NUMEROS_ESCRITOS.keys()) + r")\s*(unidades?|pares?|combos?|paquetes?)\b",
    re.IGNORECASE)

# Marcadores del "resumen/confirmacion final" (elemento 1: mencion de producto; elemento 3:
# direccion o frase de cierre). El elemento 2 (atributo) se calcula con extraer_atributos.
# Reusa parte del vocabulario de _cierra_con_cliente (Q6) pero es un criterio PROPIO y mas
# amplio: R6 no exige un cierre literal, exige 2 de 3 señales genericas en el mismo mensaje.
# SOLO frases de varias palabras -- medido en produccion (verificacion adversarial
# 2026-08-21): las versiones sueltas "tu pedido", "confirmamos" y "direccion"/"dirección"
# (sin mas contexto) hacian que 847 de 6.911 mensajes de 2 dias reales calzaran como
# "resumen final" (una pregunta como "cual es tu direccion?" ya sumaba este elemento),
# inundando el informe de DUDA sin señal real. Se retiran las sueltas, se dejan solo frases
# completas de cierre real.
MARCADORES_PRODUCTO_R6 = ("pedido", "producto", "orden", "compra")
MARCADORES_CIERRE_R6 = (
    "pedido confirmado", "confirmamos tu pedido", "tu pedido va en camino",
    "listo, quedo confirmado", "gracias por tu compra", "muchas gracias por tu compra",
    "queda registrado", "quedo registrado", "pedido registrado",
    "direccion de envio", "direccion de entrega",
)


def extraer_atributos(texto):
    """Devuelve [(tipo, valor_normalizado), ...] con los atributos concretos y variables
    (color/talla/cantidad) que aparecen en `texto`. Heuristica por palabra clave, declarada
    como tal -- no es una lectura certera de lo que el cliente realmente quiso decir."""
    t = normalizar(texto)
    out = []
    for m in PATRON_COLOR.finditer(t):
        out.append(("color", CANON_COLOR[m.group(1).lower()]))
    for m in PATRON_TALLA.finditer(t):
        out.append(("talla", m.group(1).upper()))
    for m in PATRON_NUMERO_CALZADO.finditer(t):
        out.append(("talla", m.group(1)))
    for m in PATRON_CANTIDAD_UNIDAD.finditer(t):
        out.append(("cantidad", m.group(1)))
    for m in PATRON_CANTIDAD_DECLARADA.finditer(t):
        out.append(("cantidad", m.group(1)))
    for m in PATRON_CANTIDAD_ESCRITA.finditer(t):
        out.append(("cantidad", NUMEROS_ESCRITOS[m.group(1).lower()]))
    return out


def es_resumen_final_r6(texto):
    """2+ de 3 elementos en el MISMO mensaje: mencion de producto/pedido, un atributo
    concreto (color/talla/cantidad), y una direccion o frase de cierre de pedido real.
    Devuelve (es_resumen: bool, atributos: list[(tipo,valor)])."""
    t = normalizar(texto)
    tiene_producto = any(p in t for p in MARCADORES_PRODUCTO_R6)
    atributos = extraer_atributos(t)
    tiene_atributo = bool(atributos)
    tiene_cierre = any(c in t for c in MARCADORES_CIERRE_R6)
    elementos = sum([tiene_producto, tiene_atributo, tiene_cierre])
    return elementos >= 2, atributos

# P6: umbral de "plantilla del anuncio", igual criterio que golden-logistica-diaria (medido,
# no adivinado): una frase identica en >=3 personas, o que pasa la cuota de frecuencia.
MIN_PERSONAS_FORMA = 3
CUOTA_FRECUENCIA = 0.03
MIN_FRECUENCIA = 5

# Patrones de secretos que NUNCA pueden llegar a un hallazgo citado. Ampliados dos veces
# tras verificacion adversarial: la primera vuelta parcheo los 3 strings que se nombraron
# (Stripe live, Mercado Pago, Sanctum) y no la FAMILIA -- leccion de la propia clase
# "se parchea el caso, no la clase" que este mismo ecosistema ya tiene documentada. Esta
# lista cubre la familia completa de cada proveedor nombrado, no solo el ambiente "live".
PATRONES_SECRETO = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),           # cubre sk-ant- tambien
    ("ElevenLabs", re.compile(r"sk_[A-Za-z0-9]{24,}")),
    ("StripeSecret", re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{10,}")),
    ("StripeWebhook", re.compile(r"whsec_[A-Za-z0-9]{10,}")),
    ("MercadoPago", re.compile(r"(?:APP_USR|TEST)-[A-Za-z0-9\-]{10,}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("Meta", re.compile(r"EAA[A-Za-z0-9]{40,}")),
    ("Shopify", re.compile(r"shp(?:at|ss|ca)_[A-Fa-f0-9]{20,}")),
    ("xAI", re.compile(r"xai-[A-Za-z0-9]{20,}")),
    ("Google", re.compile(r"AIza[A-Za-z0-9_\-]{30,}")),
    ("GoogleOAuthRefresh", re.compile(r"1//0[A-Za-z0-9_\-]{20,}")),
    ("SanctumBearer", re.compile(r"\b\d+\|[A-Za-z0-9]{20,}\b")),
    ("GitHubToken", re.compile(r"(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}")),
    ("AWSAccessKey", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("SlackToken", re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("SendGrid", re.compile(r"SG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}")),
    # Bearer generico hexadecimal largo (64 caracteres, forma comun de un token opaco de
    # sesion o de API): mas ancho que los anteriores a proposito, va AL FINAL para no
    # tapar coincidencias mas especificas primero.
    ("HexBearerGenerico", re.compile(r"\b[0-9a-fA-F]{64}\b")),
]

# Candidatos de campo para un valor monetario dentro de get-info. Ninguno esta confirmado
# contra el servidor real (mismo caso que el endpoint de listado en extraer.py): se
# declara cual se uso, nunca se asume en silencio.
CAMPOS_VALOR_CANDIDATOS = ("Valor pedido", "Total", "Valor", "Precio", "Total pedido")


def redactar_texto(t):
    for etiqueta, patron in PATRONES_SECRETO:
        t = patron.sub(lambda m: f"<<REDACTADO {etiqueta} len={len(m.group(0))}>>", t)
    return t


# ------------------------------------------------------------------ utilidades de parseo

def parse_fecha(valor):
    """Parsea fechas con ESPACIO ('2026-08-10 11:25:39') o con 'T' (ISO). Nunca se
    compara como texto (P9): el espacio (0x20) es menor que 'T' (0x54) y una comparacion
    textual deja todo contacto nuevo por debajo de una marca ISO, siempre, en silencio."""
    if valor is None:
        return None
    s = str(valor).strip()
    if not s:
        return None
    try:
        if "T" in s:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        return datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def parse_dinero(valor):
    """Distingue el formato ANTES de limpiar (P10). Mismo algoritmo, verificado en
    produccion por golden-logistica-diaria (`plata()`): si el ULTIMO separador deja
    EXACTAMENTE dos digitos detras y es el final de la cadena, es decimal; si no, todos
    los separadores son de miles. '142.800' -> 142800.0 (miles). '74900.00' -> 74900.0
    (decimal). Devuelve (monto, formato) o (None, motivo).

    SOLO acepta texto (str). Un `int`/`float` ya perdio la informacion de formato que
    esta funcion existe para leer -- '74900.0' como float no dice si el cliente/el API
    querian decir 74.900 (miles) o 74900,0 (decimal con un solo digito, fuera de la
    regla de dos). Adivinar ahi es exactamente la clase de fallo que esta trampa
    (P10) existe para evitar: mejor declarar 'tipo_no_soportado' que inventar un
    monto 10 veces mayor o menor en silencio. Medido en produccion: `plata()` recibe
    siempre cadenas del hilo de chat y nunca tuvo que resolver este caso."""
    if valor is None:
        return None, "vacio"
    if not isinstance(valor, str):
        return None, "tipo_no_soportado"
    s = valor.strip().replace("$", "").replace(" ", "")
    if not s:
        return None, "vacio"
    if not re.fullmatch(r"[\d.,]+", s):
        return None, "no_parseable"
    m = re.search(r"[.,](\d+)$", s)
    if m and len(m.group(1)) == 2 and len(s) - m.end() == 0:
        entero = re.sub(r"[.,]", "", s[:m.start()])
        try:
            return round(float(f"{entero}.{m.group(1)}"), 2), "decimal"
        except ValueError:
            return None, "no_parseable"
    try:
        return float(re.sub(r"[.,]", "", s)), "miles"
    except ValueError:
        return None, "no_parseable"


def obtener_ts(msg):
    for k in CAMPOS_TS:
        if msg.get(k):
            return msg[k]
    return None


def invertir_hilo(mensajes):
    """El hilo llega del MAS RECIENTE al mas viejo (P3). Se invierte a orden cronologico.

    Regla TODO-O-NADA (P4), igual que la version medida en produccion
    (`analizar_conversaciones.py`): si TODOS los mensajes traen `ts`, se ordena por `ts`
    parseado. Si falta aunque sea UNO, no se hace un ordenamiento parcial de confianza
    dudosa: se invierte la lista entera tal cual llego (el API entrega descendente, y esa
    es la unica informacion de orden que queda). Confiar en un `ts` suelto en medio de
    mensajes sin tiempo es peor que no usarlo: un solo mensaje sin `ts` colado entre los
    demas invertiria justo la señal de quien hablo de ultimo."""
    if not mensajes:
        return []
    # OJO: la condicion es PARSEABLE, no solo "presente". Un ts truthy que parse_fecha
    # no puede leer (otro formato, un epoch, un tipo inesperado) es indistinguible de
    # un ts ausente para efectos de ORDEN: si se confiara en su presencia sin poder
    # parsearlo, todos caerian al mismo `datetime.min` con un sort() ESTABLE que deja
    # el hilo tal cual llego del servidor -- descendente -- sin invertir, y sin avisar.
    todos_parseables = all(parse_fecha(obtener_ts(m)) is not None for m in mensajes)
    if todos_parseables:
        return sorted(mensajes, key=lambda m: parse_fecha(obtener_ts(m)))
    return list(reversed(mensajes))


def es_nota_pixel(msg):
    """P5. Campo PRIMARIO confirmado: `type == "note"`. `msg_type` es un eje distinto
    (de que esta hecho el mensaje) y se acepta como respaldo si `type` no vino."""
    if "type" in msg:
        return (msg.get("type") or "").lower() == "note"
    return (msg.get("msg_type") or "").lower() == "note"


def es_feed(msg):
    return (msg.get("msg_type") or "").lower() == "feed"


def es_audio(msg):
    return (msg.get("msg_type") or "").lower() == "audio"


def contenido_real(msg):
    """P8: audio usa payload.transcribed_text, nunca 'content' a secas."""
    if es_audio(msg):
        payload = msg.get("payload") or {}
        texto = payload.get("transcribed_text") if isinstance(payload, dict) else None
        if texto:
            return texto
    return msg.get("content") or ""


def direccion(msg):
    """Campo PRIMARIO confirmado contra el servidor real: `type` con valores "in"
    (cliente) / "out" (empresa). Si `type` no vino (DUMP de otra fuente, u otra
    integracion tipo uChat), se prueban alternativas conocidas como respaldo. Un
    mensaje que no calza con ninguna se declara 'desconocido' -- nunca se adivina en
    silencio, y (P-desconocidos) genera un hallazgo si aparece."""
    t = msg.get("type")
    if isinstance(t, str):
        tl = t.lower()
        if tl == "in":
            return "cliente"
        if tl == "out":
            return "empresa"
        if tl == "note":
            return "nota"

    d = msg.get("direction")
    if isinstance(d, str):
        dl = d.lower()
        if dl in ("incoming", "in", "received", "user", "cliente", "inbound"):
            return "cliente"
        if dl in ("outgoing", "out", "sent", "bot", "empresa", "outbound"):
            return "empresa"
    if "is_bot" in msg:
        return "empresa" if msg["is_bot"] else "cliente"
    if "from_bot" in msg:
        return "empresa" if msg["from_bot"] else "cliente"
    s = msg.get("sender")
    if isinstance(s, str):
        sl = s.lower()
        if sl in ("user", "cliente", "subscriber"):
            return "cliente"
        if sl in ("bot", "empresa", "assistant", "agent"):
            return "empresa"
    return "desconocido"


def normalizar(t):
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def plantillas_de(primeros_mensajes):
    """P6, criterio MEDIDO (no regex fija), IGUAL al validado en produccion
    (golden-logistica-diaria/scripts/analizar_conversaciones.py) -- dos condiciones,
    cada una ciega a la mitad del problema:
      - FRECUENCIA: `n >= umbral` (dominante o pasa la cuota del 3%). Caza el
        prellenado del boton aunque nunca se sepa que empieza con "¡".
      - FORMA: `n >= 3 Y empieza con "¡"`. Caza el boton MINORITARIO que la
        frecuencia sola no alcanza, con la repeticion como evidencia extra.

    LIMITE HEREDADO Y DECLARADO (no silencioso): la rama de FRECUENCIA no exige la
    forma. Si 5 o mas clientes reales escriben la MISMA objecion real como primer
    mensaje ("esta muy caro" x5) sobre un dia con pocos contactos, esa frase cruza el
    umbral de frecuencia y se trata como plantilla del anuncio -- borrando esas
    objeciones. Es el mismo comportamiento medido en produccion (mismos umbrales),
    no una regresion de esta skill, pero se devuelve aparte para que quien llama
    pueda DECLARARLO en vez de tragarlo en silencio."""
    from collections import Counter
    frec = Counter(t for t in (normalizar(x) for x in primeros_mensajes) if t)
    hilos = sum(frec.values()) or 1
    umbral = max(MIN_FRECUENCIA, int(CUOTA_FRECUENCIA * hilos))
    plantillas = set()
    solo_por_frecuencia_sin_forma = set()
    for t, n in frec.items():
        por_forma = n >= MIN_PERSONAS_FORMA and t.startswith("¡")
        por_frecuencia = n >= umbral
        if por_forma or por_frecuencia:
            plantillas.add(t)
        if por_frecuencia and not por_forma:
            solo_por_frecuencia_sin_forma.add(t)
    return plantillas, solo_por_frecuencia_sin_forma


# ------------------------------------------------------------------------ el clasificador

class Clasificador:
    def __init__(self, dump, modo=None):
        self.d = dump
        if modo is not None:
            modo = modo.lower()
            if modo not in MODOS_VALIDOS:
                raise ValueError(f"--modo debe ser uno de {MODOS_VALIDOS}, no {modo!r}")
        self.modo = modo
        self.hallazgos = []
        self.cobertura = []
        self.universo = {}
        self._vistos = set()
        self.conversaciones = []
        self.excluidos_dropi = []
        self.plantillas = set()

    def falla(self, control, sev, titulo, evidencia, consecuencia="", accion=""):
        evidencia = redactar_texto(evidencia)
        huella = (control, titulo, evidencia[:200])
        if huella in self._vistos:
            return
        self._vistos.add(huella)
        self.hallazgos.append({
            "control": control, "severidad": sev, "titulo": redactar_texto(titulo),
            "evidencia": evidencia, "consecuencia": consecuencia, "accion": accion,
        })

    def cubre(self, control, estado, revisados=None, nota=""):
        self.cobertura.append({"control": control, "estado": estado,
                               "revisados": revisados, "nota": nota})

    # ---------------------------------------------------------------- P1-P13 + clasif.
    def clasificar_contacto(self, contacto, corte_del_dia):
        crudo = contacto.get("mensajes") or []

        hilo = invertir_hilo(crudo)
        hilo_sin_notas = [m for m in hilo if not es_nota_pixel(m)]     # P5

        mensajes_privados = [m for m in hilo_sin_notas if not es_feed(m)]
        comentarios_feed = [m for m in hilo_sin_notas if es_feed(m)]

        # P-desconocidos: un mensaje que no calzo con ninguna direccion conocida se
        # declara, nunca se cuenta en silencio como si no existiera.
        desconocidos = [m for m in mensajes_privados if direccion(m) == "desconocido"]
        if desconocidos:
            self.falla("P-desconocidos", "DUDA",
                       f"`{contacto.get('user_ns')}` tiene mensajes de direccion no "
                       "reconocida",
                       f"{len(desconocidos)} de {len(mensajes_privados)} mensajes con "
                       "'type'/'direction' fuera de los valores conocidos",
                       "Esos mensajes no entran en 'quien hablo de ultimo' ni en ningun "
                       "otro calculo: pueden estar escondiendo un cambio de formato del "
                       "proveedor. No se adivina su direccion.")

        direcciones = [direccion(m) for m in mensajes_privados]
        if mensajes_privados and "cliente" in direcciones and "empresa" not in direcciones:
            self.falla("P1", "DUDA",
                       f"`{contacto.get('user_ns')}` no tiene NINGUN mensaje de la empresa "
                       "en todo el hilo",
                       f"{len(mensajes_privados)} mensajes, todos de direccion 'cliente'",
                       "Puede ser un abandono real o una extraccion sin include_bot=1. No "
                       "se clasifica como 'abandonado' sin confirmar cual de las dos es.")

        msgs_cliente = [m for m in mensajes_privados if direccion(m) == "cliente"]
        msgs_cliente_reales = [m for m in msgs_cliente
                               if normalizar(contenido_real(m)) not in self.plantillas]
        msgs_empresa = [m for m in mensajes_privados if direccion(m) == "empresa"]

        motivo_no_compra = self._motivo_no_compra(msgs_cliente_reales)

        audios_sin_texto = [m for m in mensajes_privados
                            if es_audio(m) and not contenido_real(m).strip()]
        if audios_sin_texto:
            self.falla("P8", "DUDA",
                       f"`{contacto.get('user_ns')}` tiene audio sin transcripcion",
                       f"{len(audios_sin_texto)} mensajes de audio sin content ni "
                       "payload.transcribed_text",
                       "Ese mensaje queda mudo para toda clasificacion de contenido.")

        ultimo = mensajes_privados[-1] if mensajes_privados else None
        quien_ultimo = direccion(ultimo) if ultimo else "sin_mensajes"
        cierra_con_cliente = self._cierra_con_cliente(ultimo)

        # R1: sin respuesta -- ultimo mensaje es del cliente. Severidad segun SKILL.md:
        # MUERTO si pasaron mas de 2 horas desde ese mensaje hasta el corte del dia
        # (el ts mas nuevo visto en todo el dump); si no se pudo medir el gap, RIESGO.
        sin_respuesta = quien_ultimo == "cliente"
        if sin_respuesta and ultimo is not None:
            t_ultimo = parse_fecha(obtener_ts(ultimo))
            gap_min = ((corte_del_dia - t_ultimo).total_seconds() / 60
                      if t_ultimo and corte_del_dia else None)
            sev = "MUERTO" if (gap_min is not None and
                              gap_min >= UMBRAL_SIN_RESPUESTA_MUERTO_MIN) else "RIESGO"
            self.falla("R1", sev,
                       f"`{contacto.get('user_ns')}` - la empresa se fue de ultimo",
                       f"ultimo mensaje del cliente: \"{contenido_real(ultimo)[:140]}\" "
                       f"({obtener_ts(ultimo)}"
                       + (f", {gap_min:.0f} min antes del corte del dia)" if gap_min is not None
                          else ", gap no medible: falta ts)"),
                       "Cliente esperando respuesta.",
                       "Va primero en el informe. MUERTO si el gap es >= 2 horas.")

        tardanzas = self._tardanzas(mensajes_privados)
        for gap_min, cita in tardanzas:
            if gap_min > UMBRAL_TARDANZA_MIN:
                self.falla("R2", "RIESGO",
                           f"`{contacto.get('user_ns')}` - respuesta tardia ({gap_min:.0f} min)",
                           cita, "El cliente pudo enfriarse o irse a otro lado.")

        bucle = self._detectar_bucle(mensajes_privados)
        if bucle:
            self.falla("R3", "RIESGO",
                       f"`{contacto.get('user_ns')}` - el bot repite la misma respuesta",
                       f"\"{bucle[:140]}\" repetido 3+ veces seguidas SIN mensaje del "
                       "cliente entre medio",
                       "Senal de flujo roto, quedo repitiendo el mismo nodo.")

        frases_encontradas = self._frases_prohibidas(msgs_empresa)
        for frase, cita in frases_encontradas:
            sev = "MUERTO" if self.modo == "cod" else "DUDA"
            self.falla("R4", sev,
                       f"`{contacto.get('user_ns')}` - el bot menciono \"{frase}\"",
                       cita,
                       "Si el espacio es contra entrega, esto le miente al cliente." if
                       self.modo == "cod" else
                       "Modo de pago no declarado (--modo). Se reporta como duda, no como "
                       "fallo confirmado.")

        preguntas_sin_cobertura = self._preguntas_sin_cobertura(mensajes_privados)
        for pregunta, respuesta in preguntas_sin_cobertura:
            self.falla("Q4", "HUECO",
                       f"`{contacto.get('user_ns')}` - pregunta sin cobertura en el prompt",
                       f"cliente: \"{pregunta[:140]}\" -> empresa: \"{respuesta[:140]}\"",
                       "Materia prima para golden-chatea-pro-prompt-ventas.")

        hallazgos_r6 = self._coherencia_intra_chat(mensajes_privados)
        for sev, titulo_corto, evidencia, consecuencia, accion in hallazgos_r6:
            self.falla("R6", sev,
                       f"`{contacto.get('user_ns')}` - {titulo_corto}",
                       evidencia, consecuencia, accion)

        atribucion = self._atribucion(mensajes_privados)
        paso = self._paso_embudo(msgs_empresa)
        valor_declarado = self._valor_declarado(contacto.get("get_info") or {})

        get_info = contacto.get("get_info") or {}
        opted = None
        if isinstance(get_info, dict):
            datos = get_info.get("data") if isinstance(get_info.get("data"), dict) else get_info
            opted = datos.get("opted_in_through") if isinstance(datos, dict) else None
        # Normalizado SIEMPRE (mismo criterio que golden-logistica-diaria/denominador.py,
        # cuyo propio comentario advierte: "el dia que devuelva 'Dropi' o 'DROPI', ninguno
        # de los dos contactos se excluye y la conversion vuelve a inflarse sin que nada
        # falle a la vista"). Es el unico marcador de esta skill que se compara asi; todo
        # lo demas (--modo, direccion, es_nota_pixel) ya normalizaba.
        es_dropi = isinstance(opted, str) and opted.strip().lower() == "dropi"
        if es_dropi:
            self.excluidos_dropi.append(contacto.get("user_ns"))

        conv = {
            "user_ns": contacto.get("user_ns"),
            "n_mensajes_privados": len(mensajes_privados),
            "n_comentarios_feed": len(comentarios_feed),
            "n_desconocidos": len(desconocidos),
            "quien_hablo_ultimo": quien_ultimo,
            "cierra_con_cliente": cierra_con_cliente,
            "sin_respuesta": sin_respuesta,
            "paso_embudo": paso,
            "atribucion": atribucion,
            "motivo_no_compra": motivo_no_compra,
            "preguntas_sin_cobertura": len(preguntas_sin_cobertura),
            "frases_prohibidas": len(frases_encontradas),
            "bucle": bool(bucle),
            "es_dropi": es_dropi,
            "valor_declarado": valor_declarado,
            "r6_hallazgos": len(hallazgos_r6),
        }
        self.conversaciones.append(conv)
        return conv

    # -------------------------------------------------------------------- sub-controles
    def _motivo_no_compra(self, msgs_cliente_reales):
        """P7: SOLO sobre mensajes de direccion 'cliente' y sin la plantilla del anuncio."""
        motivos = []
        for m in msgs_cliente_reales:
            texto = contenido_real(m)
            if PALABRAS_OBJECION_PRECIO.search(texto):
                motivos.append("precio")
            if PALABRAS_OBJECION_ENVIO.search(texto):
                motivos.append("envio")
            if PALABRAS_OBJECION_DESCONFIANZA.search(texto):
                motivos.append("desconfianza")
        return motivos

    def _cierra_con_cliente(self, ultimo):
        if ultimo is None or direccion(ultimo) != "empresa":
            return False
        texto = normalizar(contenido_real(ultimo))
        patrones_cierre = ("pedido confirmado", "gracias por tu compra", "tu pedido va en "
                           "camino", "listo, quedo confirmado", "muchas gracias por tu "
                           "compra", "confirmamos tu pedido")
        return any(p in texto for p in patrones_cierre)

    def _tardanzas(self, mensajes):
        gaps = []
        for i in range(len(mensajes) - 1):
            if direccion(mensajes[i]) == "cliente" and direccion(mensajes[i + 1]) == "empresa":
                t1 = parse_fecha(obtener_ts(mensajes[i]))
                t2 = parse_fecha(obtener_ts(mensajes[i + 1]))
                if t1 and t2 and t2 > t1:
                    gap_min = (t2 - t1).total_seconds() / 60
                    cita = (f"cliente {obtener_ts(mensajes[i])!r} -> empresa "
                            f"{obtener_ts(mensajes[i + 1])!r} ({gap_min:.0f} min)")
                    gaps.append((gap_min, cita))
        return gaps

    def _detectar_bucle(self, mensajes_privados):
        """R3: 3+ mensajes de EMPRESA con contenido identico, SEGUIDOS entre si sin que
        un mensaje del CLIENTE se haya intercalado. Recorre el hilo completo (no solo
        los mensajes de empresa ya filtrados) para que una racha de respuestas a
        preguntas DISTINTAS del cliente nunca se confunda con un bucle."""
        racha = []
        for m in mensajes_privados:
            d = direccion(m)
            if d == "cliente":
                racha = []
                continue
            if d != "empresa":
                continue
            racha.append(m)
            if len(racha) >= 3:
                textos = {normalizar(contenido_real(x)) for x in racha[-3:]}
                if len(textos) == 1 and next(iter(textos)):
                    return contenido_real(racha[-1])
        return None

    def _frases_prohibidas(self, msgs_empresa):
        hallados = []
        for m in msgs_empresa:
            texto = normalizar(contenido_real(m))
            for frase in FRASES_PROHIBIDAS_COD:
                if frase in texto:
                    hallados.append((frase, f"empresa dijo: \"{contenido_real(m)[:160]}\""))
        return hallados

    def _coherencia_intra_chat(self, mensajes_privados):
        """R6: coherencia intra-chat (sin Dropi). Compara el/los atributo(s) concretos que
        el CLIENTE menciono (color/talla/cantidad) contra lo que dice el mensaje final de
        RESUMEN/CONFIRMACION de la EMPRESA sobre ese MISMO atributo. Frontera explicita:
        SOLO usa el chat, nunca confirma contra Dropi -- si el hallazgo real termina siendo
        que el cliente cambio de opinion, `golden-logistica-diaria` (con Dropi conectado) es
        la que hace la confirmacion definitiva contra el pedido real; esto es la version que
        funciona sin esa integracion.

        Devuelve una lista de tuplas (severidad, titulo_corto, evidencia, consecuencia,
        accion), lista para pasar a `self.falla('R6', ...)`."""
        menciones_cliente = []       # [(indice, tipo, valor, texto_citado)]
        idx_resumen = None
        atributos_resumen = None
        texto_resumen = None

        for i, m in enumerate(mensajes_privados):
            d = direccion(m)
            texto = contenido_real(m)
            if d == "cliente":
                for tipo, valor in extraer_atributos(texto):
                    menciones_cliente.append((i, tipo, valor, texto))
            elif d == "empresa":
                es_resumen, atributos = es_resumen_final_r6(texto)
                if es_resumen:
                    # se queda con el ULTIMO candidato del hilo: el resumen/confirmacion
                    # real esta cerca del final del embudo, no al principio.
                    idx_resumen = i
                    atributos_resumen = atributos
                    texto_resumen = texto

        if not menciones_cliente:
            # El cliente nunca menciono un atributo concreto y variable -- no hay nada que
            # comparar. No se genera un hallazgo: forzar una DUDA en cada conversacion sin
            # atributo mencionado seria ruido, no señal (la mayoria de hilos no llegan a
            # discutir color/talla/cantidad).
            return []

        salidas = []

        if idx_resumen is None:
            salidas.append((
                "DUDA",
                "coherencia intra-chat: el cliente mencionó un atributo pero no se detectó "
                "resumen/confirmación final del pedido",
                f"cliente mencionó {[(t, v) for _, t, v, _ in menciones_cliente][:5]} en el "
                "hilo, sin un mensaje final de la empresa con forma de resumen/confirmación "
                "de pedido (2+ de: producto, atributo, dirección/cierre)",
                "No se puede comparar sin un resumen final detectable — puede ser que el "
                "pedido se cerró en otro formato que el criterio no reconoce, o que la "
                "conversación no llegó a cerrar.",
                "SOLO chat, sin Dropi (frontera R6): revisar a mano si hubo pedido real; "
                "si lo hay, golden-logistica-diaria confirma contra Dropi.",
            ))
            return salidas

        tipos_resumen = {}
        for tipo, valor in atributos_resumen:
            tipos_resumen[tipo] = valor      # el resumen es un solo mensaje: se queda con
                                              # el ultimo valor citado ahi mismo si repite

        tipos_cliente = {}
        for i, tipo, valor, texto in menciones_cliente:
            if i >= idx_resumen:
                continue          # solo cuenta lo dicho ANTES del resumen final
            tipos_cliente.setdefault(tipo, []).append((valor, texto))

        for tipo, lista in tipos_cliente.items():
            if tipo not in tipos_resumen:
                salidas.append((
                    "DUDA",
                    f"coherencia intra-chat: el resumen final no menciona el atributo "
                    f"'{tipo}' que el cliente sí mencionó",
                    f"cliente mencionó {tipo}={lista[-1][0]!r} (\"{lista[-1][1][:120]}\"), "
                    f"pero el resumen final (\"{texto_resumen[:160]}\") no lo incluye",
                    "El resumen puede haberlo omitido sin error (el atributo puede constar "
                    "en otro campo/paso), o puede ser una omisión real.",
                    "SOLO chat, sin Dropi (frontera R6): lectura humana confirma si el "
                    f"'{tipo}' quedó registrado correctamente; con Dropi conectado, "
                    "golden-logistica-diaria lo confirma contra el pedido real.",
                ))
                continue

            valores_distintos = {v for v, _ in lista}
            valor_resumen = tipos_resumen[tipo]
            if len(valores_distintos) > 2:
                salidas.append((
                    "DUDA",
                    f"coherencia intra-chat: el cliente mencionó {len(valores_distintos)} "
                    f"valores distintos de '{tipo}' antes del resumen — no queda claro cuál "
                    "es el último válido",
                    f"valores de {tipo} mencionados en orden: "
                    f"{[v for v, _ in lista]} · resumen final dice {tipo}={valor_resumen!r}",
                    "Caso ambiguo: no se fuerza una severidad alta sin saber cuál mención "
                    "es la definitiva.",
                    "SOLO chat, sin Dropi (frontera R6): lectura humana abre el hilo y "
                    "confirma cuál de los valores es el correcto antes de despachar; con "
                    "Dropi conectado, golden-logistica-diaria lo confirma contra el pedido "
                    "real.",
                ))
                continue

            ultimo_valor, ultimo_texto = lista[-1]
            if ultimo_valor == valor_resumen:
                # Coherente -- incluye el caso del cliente que cambió de opinión y el
                # resumen del bot SÍ recogió el cambio: eso no es un hallazgo.
                continue

            primero_valor, primero_texto = lista[0]
            salidas.append((
                "MUERTO",
                f"posible incoherencia de '{tipo}' entre lo que pidió el cliente y el "
                "resumen final del bot",
                f"cliente dijo {tipo}={ultimo_valor!r} (\"{ultimo_texto[:120]}\"), el "
                f"resumen final dice {tipo}={valor_resumen!r} (\"{texto_resumen[:160]}\"), "
                "sin un mensaje posterior del cliente que explique el cambio",
                "Esto puede ser un aviso legítimo de que el cliente cambió de opinión más "
                "tarde en el chat con una frase que este criterio por palabra clave no "
                "capturó; queda para lectura humana confirmar cuál es el atributo correcto "
                "— nunca se asume automáticamente que el resumen del bot está mal.",
                "SOLO chat, sin Dropi (frontera R6): revisar el pedido antes de despachar. "
                "Con Dropi conectado, golden-logistica-diaria hace la confirmación "
                "definitiva cruzando contra el pedido real.",
            ))

        # Hallado en verificacion adversarial (2026-08-21): un mensaje del CLIENTE que llega
        # DESPUES del resumen final y menciona un valor DISTINTO del mismo atributo quedaba
        # en silencio total (ni MUERTO ni DUDA) -- justo el caso caro: se despacha con el
        # valor del resumen y el cliente dijo otra cosa despues. No se fuerza MUERTO (llegar
        # despues del resumen puede ser charla suelta, no necesariamente una correccion real
        # del pedido), se declara DUDA para que quede en el informe y no en silencio.
        for i, tipo, valor, texto in menciones_cliente:
            if i <= idx_resumen or tipo not in tipos_resumen:
                continue
            if valor != tipos_resumen[tipo]:
                salidas.append((
                    "DUDA",
                    f"coherencia intra-chat: el cliente mencionó {tipo}={valor!r} DESPUÉS "
                    "del resumen final, distinto de lo que el resumen dice",
                    f"resumen final (\"{texto_resumen[:160]}\") dice "
                    f"{tipo}={tipos_resumen[tipo]!r}, y DESPUÉS el cliente escribió "
                    f"\"{texto[:140]}\" (con {tipo}={valor!r})",
                    "Puede ser una corrección real que llegó tarde para el pedido ya "
                    "resumido, o solo charla suelta sin relación con el pedido — no se "
                    "fuerza una severidad alta sin lectura humana.",
                    "SOLO chat, sin Dropi (frontera R6): revisar si el pedido ya se "
                    "despachó con el valor equivocado; con Dropi conectado, "
                    "golden-logistica-diaria confirma contra el pedido real.",
                ))

        return salidas

    def _preguntas_sin_cobertura(self, mensajes):
        salidas = []
        for i in range(len(mensajes) - 1):
            if direccion(mensajes[i]) != "cliente":
                continue
            texto = contenido_real(mensajes[i])
            if not PATRON_INTERROGATIVO.search(texto):
                continue
            siguiente_empresa = None
            for j in range(i + 1, len(mensajes)):
                if direccion(mensajes[j]) == "empresa":
                    siguiente_empresa = mensajes[j]
                    break
                if direccion(mensajes[j]) == "cliente":
                    break        # el cliente volvio a escribir antes de que respondieran
            if siguiente_empresa is None:
                continue
            respuesta = normalizar(contenido_real(siguiente_empresa))
            if any(f in respuesta for f in FALLBACK_GENERICO) or len(respuesta) < 3:
                salidas.append((contenido_real(mensajes[i]), contenido_real(siguiente_empresa)))
        return salidas

    def _atribucion(self, mensajes):
        """El texto del anuncio (`headline`) lo controla un TERCERO (quien pauta), no
        Chatea ni esta skill: nada impide que contenga, por accidente o mala fe, algo
        con forma de credencial. Este diccionario sale COMPLETO al --json (no pasa por
        `falla()`), asi que se redacta aqui mismo -- la unica funcion de la skill cuya
        salida evita el camino normal de hallazgos y por eso necesita su propia
        compuerta."""
        for m in mensajes:
            payload = m.get("payload") or {}
            referral = payload.get("referral") if isinstance(payload, dict) else None
            if referral and referral.get("source_id"):
                return {"source_id": redactar_texto(str(referral.get("source_id") or "")),
                        "headline": redactar_texto(str(referral.get("headline") or "")),
                        "ctwa_clid": redactar_texto(str(referral.get("ctwa_clid") or ""))}
        return None

    def _paso_embudo(self, msgs_empresa):
        """Q2: heuristica DECLARADA, no un hecho verificado contra la config real."""
        if not msgs_empresa:
            return "sin_iniciar"
        texto = normalizar(contenido_real(msgs_empresa[-1]))
        if any(p in texto for p in ("pedido confirmado", "confirmamos tu pedido")):
            return "cierre"
        if any(p in texto for p in ("direccion", "dirección", "ciudad", "telefono",
                                    "teléfono", "numero de contacto")):
            return "recopilando_datos"
        if len(msgs_empresa) <= 1:
            return "saludo_inicial"
        return "en_conversacion"

    def _valor_declarado(self, get_info):
        """P10 en uso real: si get-info trae alguno de los campos candidatos de valor
        monetario, se parsea con parse_dinero y se declara cual campo se uso. Ninguno
        de estos nombres esta confirmado contra el servidor real (ver CAMPOS_VALOR_
        CANDIDATOS): se declara el candidato usado, nunca se asume en silencio."""
        if not isinstance(get_info, dict):
            return None
        datos = get_info.get("data") if isinstance(get_info.get("data"), dict) else get_info
        if not isinstance(datos, dict):
            return None
        for campo in CAMPOS_VALOR_CANDIDATOS:
            if campo in datos and datos[campo] not in (None, ""):
                monto, formato = parse_dinero(datos[campo])
                if monto is not None:
                    return {"campo_usado": campo, "monto": monto, "formato": formato}
        return None

    # --------------------------------------------------------------------------- correr
    def correr(self):
        contactos = self.d.get("contactos") or []
        self.universo = {
            "contactos_en_dump": len(contactos),
            "endpoint_listado_usado": self.d.get("_listado_endpoint_usado"),
            "hilos_no_descargados": len(self.d.get("_hilos_no_descargados") or []),
        }
        if not contactos:
            self.falla("P1", "MUERTO", "El DUMP no trae contactos",
                       "sin contactos no hay nada que clasificar")
            return self

        # FASE 1 / SKILL.md: si el denominador declarado por extraer.py no cuadra con
        # lo efectivamente traido, el informe SE DETIENE -- no se clasifica a medias.
        # TRES ESTADOS, no dos: "cuadra" / "no_cuadra" / "no_medible". El error que se
        # peleo en verificacion adversarial era tratar "no pude medirlo" (falta
        # `_conteos`, o `declarados_por_servidor` vino None/string porque el endpoint de
        # listado ni esta confirmado) como si fuera "cuadra" -- exactamente lo que
        # `references/clasificacion.md` I4 (heredado de la hermana) prohibe: "ausencia
        # no es prueba". "No medible" NO aborta (no hay con que decidir), pero tampoco
        # se declara sano: se declara tal cual, sin adjetivos.
        conteos = self.d.get("_conteos") or {}
        listado = conteos.get("contactos_del_dia") or {}
        traidos, declarados = listado.get("traidos"), listado.get("declarados_por_servidor")
        if not isinstance(traidos, int) or not isinstance(declarados, int):
            estado_denominador = "no_medible"
        elif traidos != declarados:
            estado_denominador = "no_cuadra"
        else:
            estado_denominador = "cuadra"
        self.universo["denominador_fase1"] = estado_denominador
        self.universo["denominador_incompleto"] = (estado_denominador == "no_cuadra")
        if estado_denominador == "no_cuadra":
            self.falla("INV", "MUERTO",
                       "El denominador de la Fase 1 no cuadra -- el informe se detiene",
                       f"extraer.py trajo {traidos} contactos, el servidor declaro "
                       f"{declarados}",
                       "Un universo incompleto invalida cualquier cobertura calculada "
                       "encima.",
                       "Repetir la extraccion antes de clasificar.")
            return self
        if estado_denominador == "no_medible":
            self.falla("INV", "DUDA",
                       "El denominador de la Fase 1 no se pudo medir",
                       f"_conteos.contactos_del_dia = {listado!r}",
                       "No se puede confirmar que el universo del dia este completo, "
                       "pero tampoco hay evidencia de que falte: se sigue, declarado.",
                       "Confirmar el endpoint real de listado y que declare "
                       "meta.total/declarados_por_servidor.")

        # P6, criterio MEDIDO: el primer mensaje 'in' de cada contacto forma el corpus
        # con el que se detecta cual texto es el prellenado del boton del anuncio.
        primeros = []
        for c in contactos:
            hilo = [m for m in invertir_hilo(c.get("mensajes") or []) if not es_nota_pixel(m)]
            for m in hilo:
                if direccion(m) == "cliente":
                    primeros.append(contenido_real(m))
                    break
        self.plantillas, sin_forma = plantillas_de(primeros)
        self.universo["plantillas_detectadas"] = len(self.plantillas)
        if sin_forma:
            self.falla("P6", "DUDA",
                       "Plantilla(s) detectada(s) SOLO por frecuencia, sin la forma del "
                       "boton de Meta (sin '¡')",
                       f"{len(sin_forma)} texto(s): {sorted(sin_forma)[:3]}"
                       + (f" y {len(sin_forma) - 3} mas" if len(sin_forma) > 3 else ""),
                       "Puede ser el prellenado real del boton (asi lo mediria "
                       "produccion), o puede ser 5+ clientes reales escribiendo la "
                       "misma objecion por coincidencia -- si es lo segundo, esas "
                       "objeciones desaparecieron de motivo_no_compra.",
                       "Revisar a mano si ese texto abre con un signo de exclamacion "
                       "de apertura en el panel; si no, es un falso positivo de la "
                       "rama de frecuencia (limite heredado del criterio medido en "
                       "produccion, ver plantillas_de en el codigo).")
        # Punto ciego DECLARADO, no silencioso: por debajo de MIN_PERSONAS_FORMA
        # contactos, el criterio de FRECUENCIA no tiene con que activarse (nunca junta
        # las 3 repeticiones que exige), y una plantilla real puede pasar sin detectar.
        # Ver clasificacion.md P6. Se avisa aqui para que "0 plantillas" en un espacio
        # chico no se lea como "no habia plantilla que detectar".
        if len(contactos) < MIN_PERSONAS_FORMA:
            self.falla("P6", "DUDA",
                       "Universo del dia demasiado chico para el criterio de frecuencia",
                       f"{len(contactos)} contactos (el criterio necesita "
                       f"{MIN_PERSONAS_FORMA}+ para poder disparar por frecuencia)",
                       "Un texto de boton del anuncio puede colarse como si fuera "
                       "palabra del cliente, y ninguna objecion basada en el se detecta.",
                       "Revisar a mano los primeros mensajes de cada contacto.")

        # Corte del dia: el ts mas nuevo visto en todo el dump, EXCLUYENDO notas de
        # pixel (P5 aplica tambien aqui -- una nota que se dispara horas despues del
        # ultimo mensaje real no puede correr el corte del dia ni subir la severidad
        # de un R1 que en realidad llevaba menos tiempo esperando).
        todos_ts = []
        for c in contactos:
            for m in (c.get("mensajes") or []):
                if es_nota_pixel(m):
                    continue
                dt = parse_fecha(obtener_ts(m))
                if dt:
                    todos_ts.append(dt)
        corte_del_dia = max(todos_ts) if todos_ts else None

        for c in contactos:
            self.clasificar_contacto(c, corte_del_dia)

        con_valor = sum(1 for c in self.conversaciones if c["valor_declarado"] is not None)
        con_desconocidos = sum(1 for c in self.conversaciones if c["n_desconocidos"] > 0)

        self.cubre("P1", "corrido", len(self.conversaciones))
        self.cubre("P2", "ESTRUCTURAL",
                  nota="literal en extraer.py (user_ns/include_bot), no hay dato que "
                       "medir en esta corrida — lo comprueba la autoprueba leyendo la "
                       "fuente, no clasificar.py")
        self.cubre("P3", "corrido", len(self.conversaciones))
        self.cubre("P4", "corrido", len(self.conversaciones), nota="regla todo-o-nada")
        self.cubre("P5", "corrido", len(self.conversaciones))
        self.cubre("P6", "corrido", len(self.conversaciones),
                  nota=f"{len(self.plantillas)} plantillas detectadas por medicion sobre "
                       f"{len(contactos)} contactos (ver aviso si el universo es chico)")
        self.cubre("P7", "corrido", len(self.conversaciones))
        self.cubre("P8", "corrido", len(self.conversaciones))
        self.cubre("P9", "corrido", nota="usado en toda comparacion de fecha")
        self.cubre("P10", "corrido", con_valor,
                  nota=f"parse_dinero se EJERCIO en {con_valor} de {len(self.conversaciones)} "
                       "conversaciones (las que traian un campo de valor candidato)")
        self.cubre("P11", "corrido", len(self.excluidos_dropi),
                  nota=f"{len(self.excluidos_dropi)} contactos dropi excluidos del "
                       "denominador de conversion/cordura")
        self.cubre("P12", "ESTRUCTURAL",
                  nota="Productos escogidos no se lee como evidencia — regla de diseño, "
                       "no hay dato que medir en esta corrida")
        self.cubre("P13", "corrido", len(self.conversaciones), nota="compuerta de cordura")
        self.cubre("P-desc", "corrido", con_desconocidos,
                  nota=f"{con_desconocidos} de {len(self.conversaciones)} conversaciones "
                       "con algun mensaje de direccion no reconocida")
        self.cubre("INV", "corrido", nota=f"denominador_fase1={estado_denominador}")
        self.cubre("Q1", "corrido", len(self.conversaciones))
        self.cubre("Q2", "corrido", len(self.conversaciones), nota="heuristica, declarada DUDA")
        self.cubre("Q3", "corrido", len(self.conversaciones))
        self.cubre("Q4", "corrido", len(self.conversaciones))
        self.cubre("Q5", "corrido", len(self.conversaciones))
        self.cubre("Q6", "corrido", len(self.conversaciones))
        self.cubre("R1", "corrido", len(self.conversaciones))
        self.cubre("R2", "corrido", len(self.conversaciones))
        self.cubre("R3", "corrido", len(self.conversaciones))
        self.cubre("R4", "corrido", len(self.conversaciones))
        self.cubre("R5", "NO_VERIFICADO",
                  nota="requiere la ficha real del producto, fuera del alcance de esta skill")
        con_menciones_r6 = sum(1 for h in self.hallazgos if h["control"] == "R6")
        self.cubre("R6", "corrido", len(self.conversaciones),
                  nota=f"coherencia intra-chat (sin Dropi), heuristica por palabra clave "
                       f"color/talla/cantidad — {con_menciones_r6} hallazgo(s); frontera "
                       "declarada con golden-logistica-diaria (confirmacion definitiva "
                       "con Dropi conectado)")

        # P13 / Q6: compuerta de cordura. EXCLUYE dropi del denominador, igual que
        # cualquier otra tasa de conversion (P11): un contacto que nace de un pedido ya
        # existente no participa de la señal de "cierre real de conversacion".
        base = [c for c in self.conversaciones if not c["es_dropi"]]
        total = len(base)
        cierres = sum(1 for c in base if c["cierra_con_cliente"])
        pct = cierres / total if total else 0
        self.universo["cierra_con_cliente_pct"] = round(pct, 4)
        self.universo["cierra_con_cliente_base"] = total
        self.universo["compuerta_activada"] = pct > UMBRAL_COMPUERTA
        if pct > UMBRAL_COMPUERTA:
            self.falla("P13", "MUERTO",
                       "COMPUERTA DE CORDURA ACTIVADA - no se publica informe",
                       f"{cierres} de {total} conversaciones no-dropi ({pct:.1%}) "
                       "clasificaron como cierra_con_cliente=True, por encima del 90%",
                       "Resultado absurdo de cara: ningun espacio real cierra asi de bien "
                       "todos los dias.",
                       "Revisar el patron de deteccion de cierre o los ejemplos citados "
                       "antes de confiar en esta corrida.")
        return self

    def abortado(self):
        return bool(self.universo.get("compuerta_activada") or
                    self.universo.get("denominador_incompleto"))


def imprimir(c):
    print("=" * 78)
    print(f"OPERACION - {c.d.get('_etiqueta')} - {c.d.get('_fecha')} - "
          f"extraido {c.d.get('_extraido')}")
    print("=" * 78)

    print("\nUNIVERSO DEL DIA")
    for k, v in c.universo.items():
        print(f"  {k:34} {v}")

    if c.abortado():
        motivo = ("COMPUERTA DE CORDURA ACTIVADA" if c.universo.get("compuerta_activada")
                  else "DENOMINADOR DE LA FASE 1 NO CUADRA")
        print(f"\n*** {motivo}: EL INFORME NORMAL NO SE ESCRIBE ***")
        print("Ver references/informe.md — seccion 'si se activo la compuerta de cordura'.")
        print("Los hallazgos y la cobertura completos NO se imprimen en este modo: solo el "
             "aviso de aborto, para que nadie confunda esta salida con un informe valido.")
        return

    orden = {"MUERTO": 0, "RIESGO": 1, "HUECO": 2, "DUDA": 3}
    print(f"\nHALLAZGOS ({len(c.hallazgos)})")
    for h in sorted(c.hallazgos, key=lambda x: orden.get(x["severidad"], 9))[:50]:
        print(f"\n{SEV.get(h['severidad'], '')} {h['severidad']} - {h['control']} - {h['titulo']}")
        print(f"     evidencia: {h['evidencia']}")
        if h["consecuencia"]:
            print(f"     consecuencia: {h['consecuencia']}")
        if h["accion"]:
            print(f"     accion: {h['accion']}")
    if len(c.hallazgos) > 50:
        print(f"\n  ... y {len(c.hallazgos) - 50} hallazgos mas (ver --json)")

    print("\nCOBERTURA")
    corridos = sum(1 for x in c.cobertura if x["estado"] == "corrido")
    for x in c.cobertura:
        rev = f"{x['revisados']}" if x["revisados"] is not None else ""
        print(f"  {x['control']:5} {x['estado']:14} {rev:8} {x['nota']}")
    print(f"\n  {corridos} de {len(c.cobertura)} controles corridos por codigo")
    print("\n  Un cero de hallazgos solo prueba algo si la cobertura fue completa.")


def _parsear_argv(argv):
    """Parser manual, chico a proposito: separa el DUMP posicional de las banderas con
    valor (`--modo X`, `--json Y`) SIN asumir que el primer argumento crudo es la ruta.
    `--modo cod archivo.json` y `archivo.json --modo cod` deben dar el mismo resultado;
    antes de este fix el primero rompia con FileNotFoundError('--modo')."""
    ruta = None
    modo = None
    json_salida = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--modo":
            if i + 1 >= len(argv):
                sys.exit("--modo requiere un valor: cod o prepago")
            modo = argv[i + 1]
            i += 2
            continue
        if a == "--json":
            if i + 1 >= len(argv):
                sys.exit("--json requiere una ruta de salida")
            json_salida = argv[i + 1]
            i += 2
            continue
        if ruta is None:
            ruta = a
        i += 1
    if ruta is None:
        sys.exit(__doc__)
    return ruta, modo, json_salida


def main():
    ruta_arg, modo, json_salida = _parsear_argv(sys.argv[1:])
    ruta = Path(ruta_arg)
    if not ruta.exists():
        sys.exit(f"No existe el DUMP: {ruta}")
    dump = json.loads(ruta.read_text())
    try:
        c = Clasificador(dump, modo=modo).correr()
    except ValueError as e:
        sys.exit(str(e))
    imprimir(c)

    if json_salida:
        destino = Path(json_salida)
        if c.abortado():
            destino.write_text(json.dumps({"universo": c.universo, "abortado": True,
                                          "hallazgo_aborto": [h for h in c.hallazgos
                                                              if h["control"] in
                                                              ("P13", "INV")]},
                                         ensure_ascii=False, indent=1))
            print(f"\nAviso de aborto (sin detalle de hallazgos) en {destino}")
        else:
            destino.write_text(json.dumps(
                {"universo": c.universo, "hallazgos": c.hallazgos, "cobertura": c.cobertura,
                 "conversaciones": c.conversaciones},
                ensure_ascii=False, indent=1))
            print(f"\nDetalle en {destino}")

    return 2 if c.abortado() else 0


if __name__ == "__main__":
    sys.exit(main())
