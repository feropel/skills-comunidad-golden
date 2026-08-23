#!/usr/bin/env python3
"""
CLASIFICADOR · golden-chatea-operacion

Corre los controles del catalogo (references/clasificacion.md) sobre un DUMP producido por
extraer.py y emite hallazgos con evidencia citada del hilo real, mas cobertura medida.

Uso:
    python3 clasificar.py <DUMP.json> --modo cod|prepago [--json salida.json] [--zona-horas N]

NO escribe nada en Chatea. Clasifica y reporta.

`--modo` declara si el espacio vende contra entrega (cod) o con pago anticipado (prepago). Sin
declararlo, cualquier mencion de pago anticipado en boca del bot se reporta como DUDA en vez de
como fallo confirmado -- nunca se asume el modelo de pago.

`--zona-horas` (entero, offset UTC en horas, ej. -5) declara la zona horaria del espacio para
acotar R2/R3/R4/Q4 al dia auditado (ver ZONA_HORAS_DEFAULT_NO_CONFIRMADA y
references/api.md). Sin declararlo, usa el default -5 -- medido SOLO contra el espacio de
Colombia validado (ESPACIO-REF); la plataforma sirve 7 paises con offsets distintos, asi que un
espacio de otro pais debe declarar su propio offset hasta confirmarlo contra el panel de
Chatea.

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
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from secretos import PATRONES_SECRETO, redactar_texto  # noqa: E402

SEV = {"MUERTO": "🔴", "RIESGO": "🟠", "HUECO": "🟡", "DUDA": "🔵"}

UMBRAL_TARDANZA_MIN = 30
UMBRAL_SIN_RESPUESTA_MUERTO_MIN = 120     # SKILL.md: MUERTO es "> 2 horas"
UMBRAL_COMPUERTA = 0.90
UMBRAL_UNIVERSO_COMPUERTA_BAJA = 10   # F5: lado bajo de la compuerta, ver clasificacion.md
# ROTO NUEVO (tercera ronda de verificacion, 2026-08-22): offset UTC del "dia" que declara
# `last_message_at` en extraer.py, medido en UN espacio (ESPACIO-REF, Colombia): -5h EXACTAS y
# CONSTANTES en 161 de 161 pares comparables de los 4 DUMPs reales. NO confirmado contra el
# panel de Chatea, y NO universal -- la plataforma sirve 7 paises con offsets distintos. Se usa
# como DEFAULT declarado (nunca silencioso: ver `universo['zona_horas_usada']`), pasable como
# `zona_horas=` a `Clasificador` para un espacio de otro pais.
ZONA_HORAS_DEFAULT_NO_CONFIRMADA = -5

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
# catalogo real medido en produccion en ESPACIO-REF (producto capilar, ver verificacion
# adversarial 2026-08-21) usa esos nombres, no los colores "de ropa" que trae la lista base.
# FALLA 5 (golden-verificador, re-auditoria 2026-08-22): esta linea nombraba el producto y
# la marca real vendidos en ese espacio -- inconsistente con la anonimizacion de GCO1.5, que
# cambio el nombre del espacio a ESPACIO-REF pero dejo pasar el nombre del producto/marca.
# Se generaliza a "producto capilar", suficiente para explicar por que la paleta existe, sin
# nombrar la marca real. Diccionario
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
# produccion (verificacion adversarial 2026-08-21) -- sin el lead-in, colores que tambien son
# palabras corrientes del espanol ("vino" el verbo, "cafe" la bebida, "rosa" un nombre de
# persona, "gris" el clima, "naranja" la fruta) generaban MUERTO falso sobre hilos reales (0
# aciertos, varios falsos positivos). La cifra especifica de hilos de esa ronda ("1.829") es
# una cifra citada de una ronda de verificacion anterior cuyo artefacto no se conservo -- se
# retira el numero puntual, se mantiene declarado el hallazgo cualitativo (falsos positivos
# reales sin lead-in) que SI sigue siendo la razon de este diseno. Costo declarado: baja el
# recall (un "mandeme el negro" suelto, sin "en"/"color" antes, ya no se lee) a cambio de no
# acusar en falso -- mismo criterio de la skill en general (preferir DUDA/silencio a una
# acusacion sin base).
PATRON_COLOR = re.compile(
    r"\b(?:color|en|a)\s+(" + _ALTERNATIVAS_COLOR + r")\b", re.IGNORECASE)
# Talla: SOLO valores reconocidos de la vida real (letras de talla de ropa o numero de 1-2
# digitos de calzado/anillo) -- nunca "cualquier palabra corta que sigue a 'talla'". Medido
# en produccion: sin esta lista, "no se cual es mi talla" capturaba talla='LA', "que talla me
# recomienda" capturaba talla='ME'.
_VALORES_TALLA = r"xxxl|xxl|xl|xs|s|m|l|\d{1,2}"
PATRON_TALLA = re.compile(r"\btalla\s*[:\s]?\s*(" + _VALORES_TALLA + r")\b", re.IGNORECASE)
PATRON_NUMERO_CALZADO = re.compile(r"\bn[uú]mero\s*[:\s]?\s*(\d{2,3})\b", re.IGNORECASE)
# F4 (RIESGO, golden-verificador 2026-08-22, recall=0 contra 165 conversaciones reales de
# ESPACIO-REF): el vocabulario original ("unidades|pares|combos|paquetes") no reconocia NINGUNA
# de las FORMAS reales medidas (parafraseadas aqui, nunca el texto literal de un cliente
# real -- regla del encargo): cantidad en SINGULAR ("1" + la unidad sin plural), cantidad
# mencionada dentro de una frase mas larga sobre querer probar el producto, cantidad SIN
# unidad explicita con un articulo antes del numero, y una PREGUNTA del cliente sobre cuanto
# trae cada unidad (esta ultima SI debe seguir sin capturar como cantidad pedida -- ver el
# filtro de PALABRAS_PEDIDO_CANTIDAD mas abajo). Se amplia en 3 frentes.
PATRON_CANTIDAD_UNIDAD = re.compile(
    r"\b(\d{1,3})\s*(unidad(?:es)?|par(?:es)?|combo(?:s)?|paquete(?:s)?|frasco(?:s)?|"
    r"botella(?:s)?|caja(?:s)?|kit(?:s)?|pote(?:s)?)\b", re.IGNORECASE)
PATRON_CANTIDAD_DECLARADA = re.compile(r"\bcantidad\s*[:\s]?\s*(\d{1,3})\b", re.IGNORECASE)
# Cantidad escrita en palabras (1-10): "quiero dos unidades" no tenia cobertura -- declarado
# como limite en clasificacion.md para lo que quede fuera (mas de 10, u otras formas).
NUMEROS_ESCRITOS = {
    "un": "1", "uno": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9", "diez": "10",
}
PATRON_CANTIDAD_ESCRITA = re.compile(
    r"\b(" + "|".join(NUMEROS_ESCRITOS.keys()) + r")\s*(unidad(?:es)?|par(?:es)?|combo(?:s)?|"
    r"paquete(?:s)?|frasco(?:s)?|botella(?:s)?|caja(?:s)?|kit(?:s)?|pote(?:s)?)\b",
    re.IGNORECASE)
# Cantidad SIN unidad explicita, con un verbo/articulo de pedido antes del numero (formas
# SINTETICAS de ejemplo, no texto literal de cliente real: "necesito 1", "dame 3", "quiero
# llevarme 2") -- la forma "articulo/verbo + numero suelto, sin unidad" es la que ningun
# patron anterior cubria, medido en produccion F4. Deliberadamente NO incluye "cuanto"/"cual"
# antes del numero (evita capturar preguntas del cliente, tipo "cual de los 2 es mejor", como
# si fueran una cantidad pedida).
PALABRAS_PEDIDO_CANTIDAD = ("quiero", "dame", "mandame", "mándame", "enviame", "envíame",
                            "necesito", "los", "las", "llevo", "pido", "ordeno", "envíeme",
                            "envieme")
PATRON_CANTIDAD_SIN_UNIDAD = re.compile(
    r"\b(?:" + "|".join(PALABRAS_PEDIDO_CANTIDAD) + r")\s+(\d{1,3})\b", re.IGNORECASE)
# Cantidad implicita por el NOMBRE DEL PRODUCTO usado como unidad (ejemplo sintetico: "1
# producto-x"): no hay lista cerrada de nombres de producto (cada tienda tiene el suyo).
# VERSION ANTERIOR (rota, hallazgo de golden-verificador en la ronda de verificacion de
# GCO1.4, medido contra los 4 DUMPs reales de ESPACIO-REF -- cifras agregadas citadas aqui,
# nunca el texto literal de un cliente real): "cualquier palabra de 4+ letras inmediatamente
# despues de un numero, en cualquier parte del mensaje" -- contra 625 mensajes de cliente
# reales, 17 dispararon cantidad y 13 de los 17 (76%) eran un NUMERO DE DIRECCION (el numero
# de una torre, apartamento o casa seguido de la palabra siguiente de la direccion): en un
# espacio COD, CADA cliente escribe su direccion con numeros seguidos de palabras, asi que
# ese patron era estructuralmente ruido, no una excepcion rara. Corregido: el patron SOLO
# dispara cuando el numero+palabra ocupa la LINEA COMPLETA del mensaje (anclado a inicio de
# mensaje o de renglon, y a fin de renglon o de mensaje) -- la forma real que SI hay que
# capturar llega como su propia linea al final de un mensaje con la direccion arriba, nunca
# embebida en medio de la direccion misma. Se pierde el caso de un nombre de producto escrito
# en medio de una frase sin verbo de pedido antes (ya cubierto por PATRON_CANTIDAD_SIN_UNIDAD
# si el cliente escribe "quiero"/"necesito"/etc. antes del numero) -- limite declarado,
# preferible al 76% de falsos positivos medido.
STOPLIST_CANTIDAD_GENERICA = {
    "dias", "día", "días", "dia", "semana", "semanas", "mes", "meses", "hora", "horas",
    "minuto", "minutos", "año", "años", "ano", "anos", "veces", "vez", "pesos", "dolares",
    "dólares", "cuotas", "personas", "kilometros", "kilómetros", "cuadras", "años,",
    # Defensa en profundidad (F4, segunda ronda): vocabulario de DIRECCION que el anclaje a
    # linea completa ya bloquea en el 76% medido, pero se deja como segunda barrera por si
    # algun dia una direccion SI llega como linea propia con esta forma.
    "apto", "apartamento", "torre", "piso", "interior", "bloque", "casa", "manzana",
    "barrio", "local", "oficina", "edificio", "urbanizacion", "urbanización", "conjunto",
    "sur", "norte", "oriente", "occidente", "centro", "sector", "vereda", "corregimiento",
}
# fullmatch (no finditer) contra cada LINEA por separado -- ver extraer_atributos, que
# recorre `texto.split("\n")` en vez de trabajar sobre el texto normalizado de una sola
# linea (normalizar() colapsa saltos de linea a espacio, y ese colapso es justo lo que
# habria vuelto inutil el anclaje "linea completa" que corrige el 76% de falsos positivos).
PATRON_CANTIDAD_PRODUCTO_IMPLICITO = re.compile(
    r"(\d{1,3})\s+([a-záéíóúñ]{4,})", re.IGNORECASE)

# Marcadores del "resumen/confirmacion final" (elemento 1: mencion de producto; elemento 3:
# direccion o frase de cierre). El elemento 2 (atributo) se calcula con extraer_atributos.
# Reusa parte del vocabulario de _cierra_con_cliente (Q6) pero es un criterio PROPIO y mas
# amplio: R6 no exige un cierre literal, exige 2 de 3 señales genericas en el mismo mensaje.
# SOLO frases de varias palabras -- medido en produccion (verificacion adversarial
# 2026-08-21): las versiones sueltas "tu pedido", "confirmamos" y "direccion"/"dirección"
# (sin mas contexto) hacian que una porcion grande de los mensajes reales medidos calzaran
# como "resumen final" (una pregunta como "cual es tu direccion?" ya sumaba este elemento),
# inundando el informe de DUDA sin señal real. La cifra especifica ("847 de 6.911") es una
# cifra citada de esa ronda de verificacion cuyo artefacto no se conservo -- se retira el
# numero puntual, se mantiene declarado el hallazgo cualitativo que sigue siendo la razon de
# este diseno. Se retiran las sueltas, se dejan solo frases completas de cierre real.
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

    # F4: cantidad -- varios patrones que pueden solapar el mismo tramo de texto ("1
    # frasco" calza con UNIDAD y tambien con PRODUCTO_IMPLICITO). Se recorren en orden de
    # especificidad y se marcan los caracteres ya cubiertos (`ocupado`) para no duplicar
    # el mismo numero dos veces por el mismo motivo.
    ocupado = [False] * len(t)

    def _marcar(inicio, fin):
        for i in range(inicio, fin):
            ocupado[i] = True

    def _libre(inicio, fin):
        return not any(ocupado[inicio:fin])

    for m in PATRON_CANTIDAD_UNIDAD.finditer(t):
        out.append(("cantidad", m.group(1)))
        _marcar(*m.span())
    for m in PATRON_CANTIDAD_DECLARADA.finditer(t):
        out.append(("cantidad", m.group(1)))
        _marcar(*m.span())
    for m in PATRON_CANTIDAD_ESCRITA.finditer(t):
        out.append(("cantidad", NUMEROS_ESCRITOS[m.group(1).lower()]))
        _marcar(*m.span())
    for m in PATRON_CANTIDAD_SIN_UNIDAD.finditer(t):
        if _libre(*m.span()):
            out.append(("cantidad", m.group(1)))
            _marcar(*m.span())

    # PRODUCTO_IMPLICITO opera por LINEA sobre el texto ORIGINAL, con `fullmatch` (la linea
    # COMPLETA debe ser "numero + palabra", nada mas) -- ver el comentario junto al patron.
    # `normalizar(texto)` (usado por todos los patrones de arriba) colapsa saltos de linea a
    # espacio, asi que este control necesita su propia pasada sobre `texto.split("\n")` para
    # que el anclaje "linea completa" tenga saltos de linea reales que anclar.
    ya_vistos = {(tipo, valor) for tipo, valor in out}
    for linea in (texto or "").split("\n"):
        linea_norm = normalizar(linea)
        if not linea_norm:
            continue
        m = PATRON_CANTIDAD_PRODUCTO_IMPLICITO.fullmatch(linea_norm)
        if not m:
            continue
        palabra = m.group(2).lower()
        if palabra in STOPLIST_CANTIDAD_GENERICA:
            continue
        par = ("cantidad", m.group(1))
        if par in ya_vistos:
            continue          # ya capturado por UNIDAD/DECLARADA/ESCRITA/SIN_UNIDAD
        out.append(par)
        ya_vistos.add(par)
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

# F3 (CRITICO SEGURIDAD, golden-verificador 2026-08-22): PATRONES_SECRETO y redactar_texto
# YA NO se definen aqui -- vivian duplicados entre este archivo (17 familias) y extraer.py
# (11 familias), y references/api.md afirmaba (falso) que estaban sincronizados. Ahora los
# dos scripts importan la MISMA lista de `secretos.py` (ver el import al inicio de este
# archivo). Ampliados dos veces tras verificacion adversarial ANTES de unificarse aqui: la
# primera vuelta parcheo los 3 strings que se nombraron (Stripe live, Mercado Pago, Sanctum)
# y no la FAMILIA -- leccion de la propia clase "se parchea el caso, no la clase" que este
# mismo ecosistema ya tiene documentada; la lista en `secretos.py` cubre la familia completa
# de cada proveedor nombrado, no solo el ambiente "live".

# Candidatos de campo para un valor monetario dentro de get-info. Ninguno esta confirmado
# contra el servidor real (mismo caso que el endpoint de listado en extraer.py): se
# declara cual se uso, nunca se asume en silencio.
CAMPOS_VALOR_CANDIDATOS = ("Valor pedido", "Total", "Valor", "Precio", "Total pedido")


# ------------------------------------------------------------------ utilidades de parseo

UMBRAL_EPOCH_MS = 10 ** 11    # por debajo: segundos (hasta ~2286); por encima: milisegundos


def _epoch_a_fecha(numero):
    """Convierte un epoch (segundos o milisegundos, detectado por MAGNITUD) a datetime
    naive en UTC -- naive a proposito, para poder compararse sin romper contra el resto
    de fechas de este archivo (P9/P4), que tambien son naive salvo que la cadena ISO
    traiga un offset explicito."""
    try:
        segundos = numero / 1000 if numero > UMBRAL_EPOCH_MS else numero
        return datetime.fromtimestamp(segundos, tz=timezone.utc).replace(tzinfo=None)
    except (ValueError, OSError, OverflowError):
        return None


def parse_fecha(valor):
    """Parsea fechas con ESPACIO ('2026-08-10 11:25:39'), con 'T' (ISO), o EPOCH (F1,
    hallazgo critico de golden-verificador 2026-08-22): la forma REAL que trae `ts` en
    los 4 DUMPs de produccion medidos (ESPACIO-REF, 165 conversaciones, 100% de los
    mensajes con `ts` entero) es un epoch, no texto -- exactamente como lo trata
    `golden-logistica-diaria/scripts/barrer_chats.py` (`x.get("ts") or 0`, linea ~134).
    Antes de este fix, un `ts` epoch nunca se parseaba: R1 nunca podia medir el gap real
    (todo caia en RIESGO por 'no medible', nunca en MUERTO) y R2 (respuesta tardia) no
    disparaba jamas, porque `_tardanzas` exige ambos `ts` parseados. Acepta:
      - int/float: epoch en segundos o milisegundos (se distingue por MAGNITUD, ver
        `UMBRAL_EPOCH_MS` -- un epoch en ms de una fecha real es varios ordenes de
        magnitud mayor que uno en segundos, no hay ambiguedad real en el rango de
        fechas que esta skill procesa).
      - cadena TODO-digitos de 9 a 13 caracteres ('1787114990'): mismo epoch, pero
        serializado como texto (algunos DUMPs/JSON lo entregan asi). Fuera de ese
        rango de longitud NO se trata como epoch -- una fecha real de pocos digitos
        (como un dia del mes suelto) no se adivina como timestamp.
      - ESPACIO o 'T' (ISO): la trampa original (P9), intacta -- no se toca.
    Nunca se compara como texto (P9): el espacio (0x20) es menor que 'T' (0x54) y una
    comparacion textual deja todo contacto nuevo por debajo de una marca ISO, siempre,
    en silencio."""
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return _epoch_a_fecha(valor)
    s = str(valor).strip()
    if not s:
        return None
    if re.fullmatch(r"\d{9,13}", s):
        return _epoch_a_fecha(float(s))
    try:
        if "T" in s:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            # ROTO NUEVO 5b (cuarta ronda de verificacion, 2026-08-22): una fecha ISO CON
            # offset (p.ej. terminada en "Z" o "+02:00") vuelve `dt` AWARE, mientras el
            # epoch (`_epoch_a_fecha`) y el formato con ESPACIO siempre devuelven NAIVE. Un
            # DUMP que mezclara ambas formas (nunca visto en produccion -- 100% epoch
            # medido, pero `parse_fecha` declara aceptar las tres formas) hacia que
            # cualquier resta/comparacion entre una fecha epoch y una ISO-con-offset
            # reventara con `TypeError: can't compare offset-naive and offset-aware
            # datetimes` -- sin capturar, tumbaba TODA la corrida. Se normaliza a UTC y se
            # vuelve NAIVE aqui mismo (mismo criterio que `_epoch_a_fecha`), para que las
            # tres formas de `ts` sean SIEMPRE comparables entre si sin importar cual trajo
            # el DUMP.
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            return dt
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
        # FALLA 1 (golden-verificador, re-auditoria 2026-08-22, hallazgo real medido
        # end-to-end): `sorted()` es ESTABLE -- dos mensajes con el MISMO `ts` (epoch en
        # SEGUNDOS, la forma real medida en produccion) conservaban el orden de ENTRADA, que
        # es DESCENDENTE (P3, el servidor entrega mas-reciente-primero). Eso deja al mensaje
        # MAS NUEVO de un empate ANTES del mas viejo en el hilo "ya ordenado" -- invierte
        # "quien hablo de ultimo" justo en el caso mas barato de reproducir (bot y cliente
        # cerrando en el mismo segundo). Medido: 12 hallazgos R1/MUERTO falsos sobre 13
        # contactos sinteticos donde el bot SI cerraba el pedido en el mismo segundo. Se
        # rompe el empate con el INDICE original: por P3, un indice MAYOR en la lista
        # descendente del servidor es un mensaje MAS VIEJO, y debe listarse primero en el
        # orden cronologico de salida -- de ahi el `-indice` como desempate.
        return [m for _, m in sorted(
            enumerate(mensajes),
            key=lambda par: (parse_fecha(obtener_ts(par[1])), -par[0]))]
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


def _valor_verdadero(v):
    """FALLA 7 (golden-verificador, re-auditoria 2026-08-22): `is_bot`/`from_bot` son
    campos de RESPALDO (solo se usan si `type` no vino -- ver `direccion`), pero un `bool`
    de Python nativo no es la unica forma en que llegan por una API PHP/Laravel: '0'/'1',
    'false'/'true' como TEXTO son una serializacion habitual. Antes, `if msg["is_bot"]`
    trataba CUALQUIER cadena no vacia (incluida '0' o 'false') como verdadera -- Python no
    hace conversion de texto a booleano, `bool("0")` es `True`. Medido: un mensaje de
    CLIENTE con `is_bot: '0'` se clasificaba como 'empresa', en SILENCIO (no cae en
    'desconocido', asi que el control P-desc -- disenado para hacer visible un cambio de
    campo del proveedor -- nunca dispara)."""
    if isinstance(v, str):
        return v.strip().lower() not in ("", "0", "false", "no", "null", "none")
    return bool(v)


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
        return "empresa" if _valor_verdadero(msg["is_bot"]) else "cliente"
    if "from_bot" in msg:
        return "empresa" if _valor_verdadero(msg["from_bot"]) else "cliente"
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
    def __init__(self, dump, modo=None, zona_horas=None):
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
        # F1-FALLA-1: fecha declarada por extraer.py en el DUMP (`_fecha`, "AAAA-MM-DD").
        # Usada para acotar R2/R3/R4/Q4 al dia auditado -- ver `_mensajes_del_dia`.
        # ROTO NUEVO 5a (cuarta ronda de verificacion, 2026-08-22): una `_fecha` PRESENTE
        # pero con formato distinto a AAAA-MM-DD (o de un dia que no calza con ningun
        # mensaje real) hacia que `_mensajes_del_dia` filtrara TODO a una lista vacia --
        # R2/R3/R4/Q4 corrian sobre cero mensajes, en silencio total, con
        # `acotado_al_dia_activo` declarado `True` (formalmente cierto, pero enganoso: el
        # acotado esta "activo" y a la vez inutil). Medido: 2 hallazgos R4 MUERTO reales
        # (el bot mencionando pago anticipado) desaparecian sin ningun aviso con una
        # `_fecha` malformada. Se valida el FORMATO aqui (no el contenido: una fecha bien
        # formada pero que no calza con ningun mensaje real sigue produciendo cero
        # coincidencias, y eso SI es una lectura legitima de "no hay actividad ese dia") --
        # una `_fecha` mal formada se trata como AUSENTE, con el mismo hallazgo declarado
        # que la ausencia total.
        cruda = dump.get("_fecha") if isinstance(dump, dict) else None
        self.fecha_auditada = (
            cruda if isinstance(cruda, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", cruda)
            else None)
        self._fecha_auditada_malformada = bool(cruda) and self.fecha_auditada is None
        # ROTO NUEVO (golden-verificador, TERCERA ronda de verificacion, 2026-08-22): la
        # primera version de `_mensajes_del_dia` comparaba `dt.date()` (parse_fecha/
        # _epoch_a_fecha convierte SIEMPRE a UTC) contra `self.fecha_auditada` (que viene de
        # `last_message_at[:10]` en extraer.py -- hora LOCAL del servidor, sin zona
        # declarada). Medido contra los 4 DUMPs reales: desfase de 5h EXACTAS y CONSTANTE en
        # 161 de 161 pares comparables (hora Colombia, UTC-5) -- con el bug, 111 mensajes
        # reales del dia se descartaban en silencio y 78 mensajes de OTRO dia se colaban como
        # si fueran del dia auditado, la MISMA clase de fallo que este fix decia haber
        # cerrado. `zona_horas` (horas de offset respecto a UTC, ej. -5 para Colombia)
        # permite declarar la zona real del espacio -- default None usa
        # `ZONA_HORAS_DEFAULT_NO_CONFIRMADA` (medida en UN espacio, Colombia, no confirmada
        # contra el panel de Chatea ni universal a los 7 paises que sirve la plataforma: SKILL.md
        # exige tratarla como una limitacion declarada, no una verdad general). Se declara
        # explicitamente en el informe (`universo['zona_horas_usada']`), nunca en silencio.
        self.zona_horas = zona_horas if zona_horas is not None else ZONA_HORAS_DEFAULT_NO_CONFIRMADA

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

        # FALLA 1 (golden-verificador, ronda 2 sobre GCO1.4, 2026-08-22): `mensajes_privados`
        # trae el HISTORICO COMPLETO del contacto (extraer.py descarga todo el hilo, no solo
        # el dia pedido) -- R2/R3/R4/Q4 recorrian ese historico entero y podian acusar al bot
        # de una demora, un bucle o una frase de DIAS ANTERIORES al dia que encabeza el
        # informe, contradiciendo la promesa de "el informe del DIA" (medido: los 7
        # hallazgos R2 de la corrida real caian, los 7, fuera de la fecha auditada). Se
        # filtra a `mensajes_del_dia` (mismo dia que `_fecha` en el DUMP) ANTES de correr
        # estos cuatro controles -- R1 (sin respuesta) y R6 (coherencia intra-chat) siguen
        # usando el hilo completo a proposito: R1 mide el ESTADO actual de la conversacion
        # (una pregunta sin responder sigue sin responder sin importar cuando se hizo), y R6
        # compara contra el resumen final de UN pedido que puede legitimamente cruzar dias
        # antes de cerrarse -- frontera declarada, no un descuido igual al de R2/R3/R4.
        mensajes_del_dia = self._mensajes_del_dia(mensajes_privados)
        msgs_empresa_del_dia = [m for m in mensajes_del_dia if direccion(m) == "empresa"]

        tardanzas = self._tardanzas(mensajes_del_dia)
        for gap_min, cita in tardanzas:
            if gap_min > UMBRAL_TARDANZA_MIN:
                self.falla("R2", "RIESGO",
                           f"`{contacto.get('user_ns')}` - respuesta tardia ({gap_min:.0f} min)",
                           cita, "El cliente pudo enfriarse o irse a otro lado.")

        bucle = self._detectar_bucle(mensajes_del_dia)
        if bucle:
            self.falla("R3", "RIESGO",
                       f"`{contacto.get('user_ns')}` - el bot repite la misma respuesta",
                       f"\"{bucle[:140]}\" repetido 3+ veces seguidas SIN mensaje del "
                       "cliente entre medio",
                       "Senal de flujo roto, quedo repitiendo el mismo nodo.")

        frases_encontradas = self._frases_prohibidas(msgs_empresa_del_dia)
        for frase, cita in frases_encontradas:
            sev = "MUERTO" if self.modo == "cod" else "DUDA"
            self.falla("R4", sev,
                       f"`{contacto.get('user_ns')}` - el bot menciono \"{frase}\"",
                       cita,
                       "Si el espacio es contra entrega, esto le miente al cliente." if
                       self.modo == "cod" else
                       "Modo de pago no declarado (--modo). Se reporta como duda, no como "
                       "fallo confirmado.")

        preguntas_sin_cobertura = self._preguntas_sin_cobertura(mensajes_del_dia)
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
    def _mensajes_del_dia(self, mensajes_privados):
        """FALLA 1 (ronda 2) + ROTO NUEVO corregido (ronda 3), ambas de golden-verificador,
        2026-08-22: el hilo descargado por extraer.py trae el HISTORICO COMPLETO del
        contacto, no solo el dia auditado -- sin acotar, R2/R3/R4/Q4 podian citar evidencia
        de OTRO dia (medido: hasta 818 min de un intercambio de dias antes, en un informe
        fechado distinto). Filtra a los mensajes cuyo `ts` cae en `self.fecha_auditada`
        (declarado por extraer.py en `_fecha`) -- pero la comparacion NO puede hacerse en UTC
        a secas: `_epoch_a_fecha` convierte `ts` a UTC, mientras `_fecha` viene de
        `last_message_at[:10]` en hora LOCAL del servidor (medido: -5h constante en el unico
        espacio confirmado, `self.zona_horas`). Se le resta el offset a `dt` ANTES de comparar
        el dia -- sin este ajuste, un mensaje cerca de medianoche local caia del lado
        equivocado del calendario en UTC (medido: 111 mensajes reales del dia se perdian, 78
        de otro dia se colaban, en los 4 DUMPs reales).
        Si `self.fecha_auditada` NO esta declarado, el acotado se DESACTIVA -- declarado con
        su propio hallazgo DUDA (ver `correr()`, nunca en silencio: la version anterior de
        este metodo devolvia todo sin avisar, la misma clase de fallo "ausencia de dato leida
        como sano" que el control INV le prohibe al resto de la skill). Un mensaje puntual sin
        `ts` parseable se MANTIENE (preferible a perder evidencia real por un `ts` roto de un
        solo mensaje aislado)."""
        if not self.fecha_auditada:
            return mensajes_privados
        offset = timedelta(hours=self.zona_horas)
        out = []
        for m in mensajes_privados:
            dt = parse_fecha(obtener_ts(m))
            if dt is None or (dt + offset).date().isoformat() == self.fecha_auditada:
                out.append(m)
        return out

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
        # FALLA 3 (golden-verificador, ronda 2 sobre GCO1.4, 2026-08-22): la version
        # anterior hacia `self.d.get("_listado_paginacion") or {}` y declaraba
        # `listado_truncado_por_tope_500: False` cuando la CLAVE NI SIQUIERA venia en el
        # DUMP (los 4 DUMPs reales de ESPACIO-REF, extraidos ANTES de que extraer.py
        # declarara este campo, no la traen) -- exactamente la regla I4 que esta misma
        # skill exige en el control INV ("ausencia de dato nunca es prueba de que el
        # universo este completo"), incumplida aqui mismo. Ahora se distinguen los DOS
        # casos: la clave NO vino (DUMP viejo, o de una version anterior de extraer.py) ->
        # "no_medible", declarado con su propio hallazgo DUDA, nunca leido como "no se
        # trunco"; la clave SI vino -> se usa el valor real.
        paginacion_listado = self.d.get("_listado_paginacion")
        paginacion_no_medible = paginacion_listado is None
        paginacion_listado = paginacion_listado or {}
        self.universo = {
            "contactos_en_dump": len(contactos),
            "endpoint_listado_usado": self.d.get("_listado_endpoint_usado"),
            "hilos_no_descargados": len(self.d.get("_hilos_no_descargados") or []),
            "listado_truncado_por_tope_500": (
                "no_medible" if paginacion_no_medible
                else bool(paginacion_listado.get("truncado_por_tope_500"))),
            # ROTO NUEVO (ronda 3): declarada SIEMPRE, nunca en silencio -- la zona horaria
            # que decide el acotado de R2/R3/R4/Q4 al dia (ver _mensajes_del_dia).
            "zona_horas_usada": self.zona_horas,
            "acotado_al_dia_activo": bool(self.fecha_auditada),
        }
        if not self.fecha_auditada:
            # Misma clase de fallo que P-listado-truncado (I4, ausencia de dato leida como
            # sano): la version anterior de _mensajes_del_dia se desactivaba en silencio sin
            # declararlo -- ahora queda como hallazgo, no como una llave que simplemente no
            # aparece. ROTO NUEVO 5a (ronda 4): distingue AUSENTE de MALFORMADA -- una
            # `_fecha` con formato invalido (ej. "18/08/2026") producia el peor de los dos
            # mundos: `acotado_al_dia_activo=True` (formalmente cierto, "algo" habia en
            # `_fecha`) pero CERO mensajes calzaban nunca con esa cadena, asi que R2/R3/R4/Q4
            # corrian sobre una lista vacia en silencio -- 2 hallazgos R4 MUERTO reales
            # desaparecian sin aviso en la medicion de esta ronda. Ambos casos (ausente y
            # malformada) llevan el MISMO hallazgo declarado.
            motivo = ("el DUMP trae `_fecha` con un formato distinto a AAAA-MM-DD (DUMP de "
                      "otra fuente, o con el campo corrompido)" if self._fecha_auditada_malformada
                      else "falta `_fecha` en el DUMP (DUMP de una versión de extraer.py "
                      "anterior a que este campo se declarara, o de otra fuente)")
            self.falla("P-sin-fecha-auditada", "DUDA",
                       "El DUMP no declara una `_fecha` utilizable -- R2/R3/R4/Q4 NO se "
                       "acotan al día",
                       motivo,
                       "Sin `_fecha` utilizable no hay con qué acotar el hilo al día "
                       "auditado: R2/R3/R4/Q4 corren sobre el HISTÓRICO COMPLETO del "
                       "contacto, con el mismo riesgo que motivó el acotado (evidencia de "
                       "otro día citada como si fuera del día del informe) -- o, si la "
                       "`_fecha` estaba malformada, corren sobre una lista VACÍA (peor: "
                       "pierden evidencia real en silencio).",
                       "Repetir la extracción con la versión actual de extraer.py, que sí "
                       "declara `_fecha` en formato AAAA-MM-DD.")
        # Re-auditoria 2026-08-22 (segunda pasada, en frio): este control SIEMPRE se evalua
        # (la comprobacion de `self.fecha_auditada` corre en cada llamada a `correr()`), pero
        # antes de esta linea solo dejaba rastro en `self.cobertura` cuando SI disparaba un
        # hallazgo -- un DUMP sano (con `_fecha` bien formada) hacia que la tabla de cobertura
        # de la Fase 3 del informe (`references/informe.md`, seccion 3) no mencionara
        # "P-sin-fecha-auditada" en absoluto, aunque el control si se hubiera corrido y hubiera
        # confirmado que todo estaba bien. Se declara SIEMPRE, con el estado real.
        self.cubre("P-sin-fecha-auditada",
                  "corrido" if self.fecha_auditada else "DUDA_DECLARADA",
                  nota=("`_fecha` bien formada, acotado al día activo" if self.fecha_auditada
                        else "sin `_fecha` utilizable -- ver hallazgo P-sin-fecha-auditada"))

        # FALLA 4 (golden-verificador, re-auditoria 2026-08-22): `extraer.py` SI declara
        # `_avisos_de_hilo` cuando un hilo quedo TRUNCADO (mas de MAX_PAG_HILO paginas) o
        # trae mensajes sin `ts` -- pero ANTES de este fix, nadie en `clasificar.py` leia esa
        # clave: grep en toda la skill confirmo 0 apariciones fuera de `extraer.py`. Un hilo
        # truncado se clasificaba y se reportaba como si estuviera COMPLETO, con exactamente
        # el mismo riesgo que ya tiene su propio control para el LISTADO
        # (`P-listado-truncado`) pero sin el equivalente para el HILO. Se convierte cada
        # aviso en un hallazgo declarado -- RIESGO si el hilo quedo truncado (puede faltar
        # evidencia real de "quien hablo de ultimo"), DUDA si el aviso es por mensajes sin
        # `ts` (el orden de ese hilo especifico no es de fiar).
        avisos_de_hilo = self.d.get("_avisos_de_hilo") or []
        for aviso in avisos_de_hilo:
            razon = (aviso or {}).get("razon", "")
            ns_aviso = (aviso or {}).get("ns", "?")
            sev_aviso = "RIESGO" if "TRUNC" in razon.upper() else "DUDA"
            self.falla("P-hilo-truncado", sev_aviso,
                       f"`{ns_aviso}` - aviso de extracción del hilo",
                       razon,
                       "Un hilo truncado puede estar reportando 'quién habló de último' o "
                       "un gap sobre evidencia incompleta; un hilo con mensajes sin `ts` "
                       "tiene un orden que no es de fiar." if sev_aviso == "RIESGO" else
                       "Ese hilo específico puede tener el orden de mensajes invertido o "
                       "parcial.",
                       "Repetir la extracción de este contacto, o subir MAX_PAG_HILO si el "
                       "espacio tiene hilos consistentemente largos (extraer.py).")
        self.cubre("P-hilo-truncado", "corrido", len(avisos_de_hilo),
                  nota=f"{len(avisos_de_hilo)} aviso(s) de extracción de hilo declarados "
                       "por extraer.py (`_avisos_de_hilo`)")

        if paginacion_no_medible:
            self.falla("P-listado-truncado", "DUDA",
                       "No se puede saber si el listado de contactos se truncó",
                       "el DUMP no trae la clave `_listado_paginacion` (DUMP extraído con "
                       "una versión de extraer.py anterior a que este campo se declarara, "
                       "o de otra fuente)",
                       "Ausencia de dato no es prueba de que el listado esté completo -- "
                       "no se lee como 'no se truncó' sin evidencia.",
                       "Repetir la extracción con la versión actual de extraer.py para "
                       "confirmar si hubo truncado.")
        # F9 (HUECO): el listado de contactos puede truncarse en el tope de 500 paginas sin
        # que nada lo avise -- ahora extraer.py lo declara en `_listado_paginacion` y aqui se
        # convierte en hallazgo, nunca queda implicito en un DUMP que solo dice "22 contactos"
        # sin decir si esos 22 son TODOS los del dia o solo lo que cupo antes del tope.
        if paginacion_listado.get("truncado_por_tope_500"):
            self.falla("P-listado-truncado", "RIESGO",
                       "El listado de contactos se truncó en el tope de 500 páginas",
                       f"se trajeron {paginacion_listado.get('paginas_traidas')} de "
                       f"{paginacion_listado.get('ultima_pagina_declarada_por_servidor')} "
                       "páginas que declaró el servidor",
                       "El universo del día puede estar incompleto: contactos que existen "
                       "en páginas posteriores al tope no entraron a esta corrida.",
                       "Espacio con un volumen de contactos fuera de lo medido hasta ahora "
                       "-- confirmar con el panel si el universo real es mayor al traído.")
        # Re-auditoria 2026-08-22 (segunda pasada, en frio), mismo criterio que el fix de
        # arriba para P-sin-fecha-auditada: este control SIEMPRE se evalua, pero antes solo
        # dejaba rastro en `self.cobertura` cuando disparaba un hallazgo -- un listado que NO
        # se trunco no aparecia como "corrido" en la tabla de cobertura del informe.
        self.cubre("P-listado-truncado",
                  "no_medible" if paginacion_no_medible else "corrido",
                  nota=("no se pudo confirmar si el listado se trunco -- ver hallazgo "
                        "P-listado-truncado/DUDA" if paginacion_no_medible
                        else f"truncado_por_tope_500="
                             f"{paginacion_listado.get('truncado_por_tope_500', False)}"))
        if paginacion_listado.get("sin_meta_last_page_no_pagina"):
            self.cubre("P-listado-paginacion", "LIMITACION_CONOCIDA",
                      nota="el servidor no declaró meta.last_page en esta corrida: "
                           "extraer.py NO paginó el listado más allá de la primera "
                           "página (comportamiento actual, declarado, no implícito)")
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

        # F5 (RIESGO, golden-verificador 2026-08-22): la compuerta ANTES solo miraba el lado
        # ALTO (>90%). Contra los 4 dias reales de ESPACIO-REF el cierre medido fue 0%, 0%, 0%
        # y 6.67% -- igual de absurdo de cara que un 95% (ningun espacio real cierra el 0% de
        # sus conversaciones TODOS los dias sin que algo este mal calibrado), y nada lo
        # detectaba. Umbral elegido (documentado tambien en clasificacion.md): 0% EXACTO con
        # un universo de 10+ conversaciones no-dropi -- no un rango arbitrario, el limite mas
        # defendible sin datos de mas espacios para calibrar un umbral intermedio. A
        # diferencia del lado alto, el lado bajo NO aborta la corrida (un dia real sin ningun
        # cierre es posible, a diferencia de un 95%+ que es matematicamente inverosimil) --
        # SI declara la anomalia como hallazgo, para que no quede en silencio.
        self.universo["compuerta_baja_activada"] = (
            total >= UMBRAL_UNIVERSO_COMPUERTA_BAJA and pct == 0.0)
        if self.universo["compuerta_baja_activada"]:
            self.falla("P13", "RIESGO",
                       "COMPUERTA DE CORDURA - lado BAJO: 0% de cierre en un universo "
                       "suficiente",
                       f"0 de {total} conversaciones no-dropi cerraron con el cliente "
                       f"(0.0%), universo >= {UMBRAL_UNIVERSO_COMPUERTA_BAJA}",
                       "Puede ser un dia real muy malo (posible, a diferencia del lado "
                       "alto), o un bug de clasificacion de Q6: el patron de cierre "
                       "(MARCADORES_CIERRE_R6 / patrones_cierre en _cierra_con_cliente) "
                       "puede no calzar con las frases de cierre reales de este espacio.",
                       "Revisar a mano 3-5 conversaciones donde el bot SI parecio cerrar "
                       "un pedido, para confirmar si el patron de cierre esta calzando "
                       "con el texto real de este espacio antes de asumir que el dia fue "
                       "asi de malo. No aborta la corrida (a diferencia del lado alto).")
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
    valor (`--modo X`, `--json Y`, `--zona-horas N`) SIN asumir que el primer argumento
    crudo es la ruta. `--modo cod archivo.json` y `archivo.json --modo cod` deben dar el
    mismo resultado; antes de este fix el primero rompia con FileNotFoundError('--modo').
    `--zona-horas` (tercera ronda de verificacion, 2026-08-22): offset UTC en horas del
    espacio auditado, para el acotado de R2/R3/R4/Q4 al dia real -- ver
    `ZONA_HORAS_DEFAULT_NO_CONFIRMADA`. Sin declararlo, se usa el default (-5, medido SOLO
    en el espacio de Colombia validado; otro pais puede necesitar otro valor)."""
    ruta = None
    modo = None
    json_salida = None
    zona_horas = None
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
        if a == "--zona-horas":
            if i + 1 >= len(argv):
                sys.exit("--zona-horas requiere un valor entero (offset UTC en horas, ej. -5)")
            try:
                zona_horas = int(argv[i + 1])
            except ValueError:
                sys.exit(f"--zona-horas debe ser un entero, no {argv[i + 1]!r}")
            i += 2
            continue
        if ruta is None:
            ruta = a
        i += 1
    if ruta is None:
        sys.exit(__doc__)
    return ruta, modo, json_salida, zona_horas


def main():
    ruta_arg, modo, json_salida, zona_horas = _parsear_argv(sys.argv[1:])
    ruta = Path(ruta_arg)
    if not ruta.exists():
        sys.exit(f"No existe el DUMP: {ruta}")
    dump = json.loads(ruta.read_text())
    try:
        c = Clasificador(dump, modo=modo, zona_horas=zona_horas).correr()
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
