#!/usr/bin/env python3
"""Por que no compraron. Clasifica cada conversacion que no termino en pedido.

No inventa motivos: cada contacto cae en una categoria PORQUE hay una senal en el
texto o en la estructura del dialogo, y la categoria "no se sabe" existe y se
reporta. Un informe que reparte 806 contactos en cinco motivos bonitos sin dejar
ninguno sin clasificar esta mintiendo.

La senal mas cara del negocio es QUIEN HABLO DE ULTIMO:
  - ultimo mensaje del CLIENTE  -> la pelota la tiene la empresa. Es plata caliente
    esperando: el cliente pregunto y nadie contesto.
  - ultimo mensaje del BOT      -> el cliente se fue. Ahi si aplica el motivo.

  python3 analizar_conversaciones.py --chats c.json --contactos k.json \
      --dropi v.json --salida a.json
"""
import argparse, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json
from denominador import medir_conversion
from comun import tel10
from collections import Counter


def norm(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


# Cada patron se dispara sobre lo que ESCRIBIO EL CLIENTE, nunca sobre lo que dijo
# el bot: si buscaramos "precio" en todo el hilo, el bot lo dice siempre y todos
# los contactos quedarian clasificados como "objecion de precio".
SENALES = [
    ("precio_caro", r"\bcaro|costoso|muy alto|no tengo (plata|dinero)|esta cara|mucha plata|rebaja|descuento|mas economic"),
    ("desconfianza", r"\bestafa|es seguro|confiable|no confio|sera verdad|es real|robo|fraude|garantia"),
    ("pago_contraentrega", r"contra ?entrega|contraentrega|pago cuando|al recibir|efectivo|no pago (antes|adelantado)|anticipad|transferencia"),
    ("cobertura", r"llega a|llegan a|hacen envio|envian a|cubren|hasta mi (pueblo|vereda|municipio)"),
    ("tiempo_entrega", r"cuanto (se demora|tarda|dura)|cuando (llega|me llega)|demora|dias habiles"),
    ("solo_preguntando", r"solo (preguntaba|queria saber)|mas adelante|luego (le|te) (escribo|aviso)|lo pienso|despues compro|ahorita no|por ahora no"),
    ("producto_dudas", r"que material|es (de )?cuero|tamano|medidas|cabe|color(es)? tiene|foto|video|como es"),
    ("ya_no_quiere", r"^no$|ya no (quiero|me interesa)|cancel|no gracias|no me interesa|dejelo asi"),
]
PREGUNTA = re.compile(r"\?|cuanto|como|donde|cuando|que |sirve|tiene")

# AQUI VIVIA `PIDIO_DATOS`, y se murio a proposito.
# Era una regex sobre lo que decia EL BOT ("nombre completo", "direccion", "ciudad"...)
# y de ella salia el cubo "se le pidieron los datos y no los completo". Medido sobre el
# universo entero de Dolce, 743 de 743: se tragaba 623, el 83,8%. Claro que si — el bot
# pide los datos SIEMPRE, asi que la regex acertaba siempre y por eso no distinguia nada.
# Un cubo que se lleva ocho de cada diez no es una clasificacion, es el guion del bot
# escrito al reves. Se reemplaza por `etapa_de_caida`, que pregunta por el CLIENTE.


def canal_de(tel):
    """Sin telefono no es WhatsApp: es un comentario publico de Facebook o Instagram.

    Medido: 84 de 743 contactos de Dolce (11%) no tienen telefono, y 3 de los 9 clientes
    que quedaron esperando respuesta estaban ahi. A esos, "llamar" no es una accion
    posible; la accion es responder el comentario, y URGE MAS, porque un mensaje sin
    responder lo lee una persona y un comentario sin responder debajo de un anuncio vivo
    lo lee todo el que llegue al anuncio.
    """
    return "whatsapp" if (tel or "").strip() else "comentario_publico"


def etapa_de_caida(ciudad, direccion, n_del_cliente, n_propios):
    """Hasta donde llego el cliente. Formulacion de LOGISTICA DOLCE, adoptada con credito.

    LA PRIORIDAD ES PARTE DE LA DEFINICION, no un detalle de implementacion: un contacto
    cae en varias a la vez y gana la de mas arriba, porque es la que manda la ACCION.
    Va de mas accionable a menos: primero al que le falta UN dato, de ultimo el que no
    dejo nada con que trabajar. Cambiar el orden cambia los numeros, y por eso el orden
    se imprime en la salida junto con los conteos.
    """
    if ciudad and not direccion:
        return "Se cayo en la direccion: dio la ciudad y falto la direccion"
    if ciudad and direccion:
        return "Dio todos los datos y no hay pedido"
    if not n_del_cliente:
        return "Nunca escribio: entro y no dijo nada"
    if not n_propios:
        return "Solo el clic del anuncio: nunca escribio nada suyo"
    if n_propios <= 1:
        return "Escribio una sola vez y no volvio"
    return "Converso y nunca llego a dar la ubicacion"

# EL TEXTO DEL BOTON DEL ANUNCIO NO ES PALABRA DEL CLIENTE.
# Meta manda un texto PREDEFINIDO cuando alguien toca el boton del anuncio. Contarlo
# como algo que la persona escribio produce objeciones falsas y "trabados" que nunca
# dijeron nada propio. Medido: 303 de 314 filas imprimian "Hola! Info del Bolso..."
# como "lo ultimo que escribio el cliente".
#
# AQUI HABIA UNA REGEX (`BOTON` + `es_del_boton`) Y SE MURIO CON EVIDENCIA.
# La undecima verificacion la adjudico contra la implementacion de LOGISTICA DOLCE
# sobre datos reales: perdia en LAS DOS DIRECCIONES, 7 casos de 7.
#   (a) Se tragaba hasta seis palabras TECLEADAS despues del boton — "...y precio 2x1",
#       "...cuanto sale" daban boton=True. Cinco personas que SI escribieron, borradas.
#   (b) No consumia el «¡» de apertura, asi que "¡Hola! Quiero mas informacion" daba
#       False: 22 contactos de plantilla contados como palabra propia (la plantilla
#       identica aparece en 38 personas distintas).
# Y lo que mas duele: mi banco de 9 casos PASABA ENTERO sin contener ninguna de las
# dos clases. Un banco escrito por el mismo que escribio la regla prueba lo que su
# autor ya sabia; las clases que no se le ocurrieron no estan, y su verde no dice nada
# sobre ellas. Los 7 casos reales que fallaron entraron al banco COMO CASOS.
#
# SE REEMPLAZA POR EL CRITERIO DE LOGISTICA DOLCE: se MIDE que textos son plantilla
# en vez de adivinarlos con un patron, y se combinan los dos criterios porque cada uno
# ve solo la mitad (medido: discrepabamos en 13 contactos, y los dos estabamos flojos).
MIN_PERSONAS_FORMA = 3      # una frase identica en 3 personas distintas no la escribio nadie
CUOTA_FRECUENCIA = 0.03     # 3% de los hilos
MIN_FRECUENCIA = 5


def plantillas_de(primeros):
    """Que textos son plantilla del anuncio. Recibe el PRIMER mensaje de cada cliente.

    Se mide, no se quema a mano: asi sirve en cualquier tienda sin hornear el copy de
    esta. Dos criterios, porque cada uno es ciego a la mitad del problema:
      - FRECUENCIA: caza el prellenado dominante y el segundo, pero se le escapan los
        botones POCO usados (uno de 10 hilos no llega a ningun umbral razonable).
      - FORMA: los textos de boton de Meta abren con «¡», signo que practicamente nadie
        teclea en WhatsApp, y son frases formales completas. Eso caza los raros.
    Al criterio de forma se le EXIGE repeticion igual: una frase que aparece identica en
    tres personas distintas no la escribio ninguna de las tres.
    """
    frec = Counter(t for t in (norm(x or "").strip() for x in primeros) if t)
    hilos = sum(frec.values()) or 1
    umbral = max(MIN_FRECUENCIA, int(CUOTA_FRECUENCIA * hilos))
    return {t for t, n in frec.items()
            if n >= umbral or (n >= MIN_PERSONAS_FORMA and t.startswith("¡"))}


# EL DINERO VIENE EN DOS FORMATOS A LA VEZ: "142.800" y "74900.00".
# Limpiar sin mirar el formato convierte 74900.00 en 7490000. Medido en produccion:
# $86,5M falsos contra $58,5M reales.
def plata(txt):
    """Devuelve el numero, o None si no se puede leer. Nunca adivina."""
    t = (txt or "").strip().replace("$", "").replace(" ", "")
    if not t:
        return None
    import re as _re
    if not _re.fullmatch(r"[\d.,]+", t):
        return None
    # Si el ultimo separador deja EXACTAMENTE dos digitos detras, es decimal.
    m = _re.search(r"[.,](\d+)$", t)
    if m and len(m.group(1)) == 2 and len(t) - m.end() == 0:
        ent = _re.sub(r"[.,]", "", t[:m.start()])
        try:
            return float(f"{ent}.{m.group(1)}")
        except ValueError:
            return None
    try:
        return float(_re.sub(r"[.,]", "", t))
    except ValueError:
        return None


# La autoprueba corre en el camino que produce el entregable, no bajo __main__.
# Si vive solo bajo __main__, un import la salta y un clasificador roto reparte
# 800 contactos en motivos inventados sin que nadie lo note.
_CASOS = [
    ("esta muy caro no tengo plata", "precio_caro"),
    ("eso sera verdad o es estafa", "desconfianza"),
    ("yo pago contra entrega cuando reciba", "pago_contraentrega"),
    ("llega a mi pueblo?", "cobertura"),
    ("cuanto se demora en llegar", "tiempo_entrega"),
    ("solo preguntaba, mas adelante compro", "solo_preguntando"),
    ("de que material es?", "producto_dudas"),
    ("ya no me interesa", "ya_no_quiere"),
    # Los dos que NO deben clasificarse. Sin estos, un patron demasiado ancho
    # aprueba la prueba y le pone motivo a todo el mundo.
    ("hola buenas tardes", None),
    ("si señora, el negro", None),
]
# R5: un caso que IMPRIME la falla pero no la cuenta no es una prueba. Estos casos
# van a la MISMA lista de fallas que los del clasificador, y esa lista aborta.
#
# LOS SIETE PRIMEROS SON LOS QUE TUMBARON LA REGEX ANTERIOR, tomados de datos reales
# por la undecima verificacion. Entran COMO CASOS y no como anecdota: un banco solo
# prueba las clases que su autor ya conocia, asi que cuando una clase aparece de
# afuera, el banco se queda con ella para siempre.
# El caso se da como (corpus de primeros mensajes, texto a juzgar, esperado): el
# criterio es de CORPUS, no de mensaje suelto — por eso hay que traer el vecindario.
_P1 = "¡Hola! Quiero mas informacion"                       # plantilla: 38 personas
_P2 = "¡Hola! Me gustaria conseguir mas informacion sobre esto."   # plantilla: 10 personas
_P3 = "Hola! Info del Bolso Portacelular y precio"          # plantilla dominante
_CORPUS = [_P1] * 38 + [_P2] * 10 + [_P3] * 600 + [
    "Hola! Info del Bolso Portacelular y precio 2x1",       # TECLEADO detras del boton
    "Hola! Info del Bolso Portacelular y precio cuanto sale",
    "precio", "cuanto bale", "confirmar pedido",
]
_CASOS_BOTON = [
    # (a) la regex vieja se tragaba lo tecleado DESPUES del boton: 5 personas borradas
    (_CORPUS, "Hola! Info del Bolso Portacelular y precio 2x1", False),
    (_CORPUS, "Hola! Info del Bolso Portacelular y precio cuanto sale", False),
    # (b) la regex vieja no consumia el «¡»: 22 contactos de plantilla contados como
    #     palabra propia. Los dos textos con «¡» son plantilla, uno por frecuencia y
    #     el otro SOLO por forma repetida — ese es el que la frecuencia sola pierde.
    (_CORPUS, _P1, True),
    (_CORPUS, _P2, True),
    (_CORPUS, _P3, True),
    # control: gente escribiendo de verdad, aunque sea corto y se repita algo
    (_CORPUS, "precio", False),
    (_CORPUS, "cuanto bale", False),
    # el mismo texto de plantilla, en un corpus donde NO se repite, ya no es plantilla:
    # la repeticion es la evidencia, no la forma. Sin este caso, «¡» sola bastaria.
    ([_P2, "hola", "buenas"], _P2, False),
]
_CASOS_PLATA = [
    ("142.800", 142800.0), ("74900.00", 74900.0), ("$ 69.900", 69900.0),
    ("1.199.900", 1199900.0), ("99900.50", 99900.5), ("", None), ("gratis", None),
]
# El residuo del otro lado se prueba como todo lo demas: con un caso que se sabe.
_CASOS_HUERFANAS = [
    ({"a": [], "b": [], "c": []}, {"a", "b"}, 1),      # c sobra en los chats
    ({"a": []},                    {"a", "b"}, 0),      # b sobra en contactos: ese NO es
    ({},                           {"a"},      0),
    ({"x": [], "y": []},           set(),      2),      # lista vacia: las dos son huerfanas
]
# CADA CASO ES UNA DECISION DE PRIORIDAD, no un ejemplo bonito. Los tres primeros son
# el mismo contacto con el mismo texto, cambiando solo los datos: si la prioridad se
# altera, cambian de cubo y estos casos lo cazan.
_CASOS_ETAPA = [
    # (ciudad, direccion, n_cliente, n_propios) -> cubo
    (("Bogota", "", 5, 4), "Se cayo en la direccion: dio la ciudad y falto la direccion"),
    (("Bogota", "Calle 1", 5, 4), "Dio todos los datos y no hay pedido"),
    (("", "", 5, 4), "Converso y nunca llego a dar la ubicacion"),
    (("", "", 0, 0), "Nunca escribio: entro y no dijo nada"),
    (("", "", 3, 0), "Solo el clic del anuncio: nunca escribio nada suyo"),
    (("", "", 1, 1), "Escribio una sola vez y no volvio"),
    # El que solo toco el boton PERO dio ciudad sigue siendo el de la direccion: le falta
    # un dato y se le puede pedir. Es la razon de que la ciudad vaya de primera.
    (("Cali", "", 2, 0), "Se cayo en la direccion: dio la ciudad y falto la direccion"),
]
# El canal decide la accion. Sin telefono no hay a quien llamar, por muy caliente que este.
_CASOS_CANAL = [("3001234567", "whatsapp"), ("", "comentario_publico"), (None, "comentario_publico")]
_probado = [False]


def _exigir_autoprueba():
    if _probado[0]:
        return
    fallas = []
    for txt, esperado in _CASOS:
        t = norm(txt)
        hall = [n for n, p in SENALES if re.search(p, t)]
        got = hall[0] if hall else None
        if got != esperado:
            fallas.append(f"'{txt}' -> {got}, se esperaba {esperado}")
    for ch_, ns_, esperado in _CASOS_HUERFANAS:
        got = len([k for k in ch_ if k not in ns_])
        if got != esperado:
            fallas.append(f"huerfanas: {ch_} contra {ns_} -> {got}, se esperaba {esperado}")
    for corpus, txt, esperado in _CASOS_BOTON:
        got = norm(txt) in plantillas_de(corpus)
        if got != esperado:
            fallas.append(f"plantilla: '{txt}' -> {got}, se esperaba {esperado}")
    for txt, esperado in _CASOS_PLATA:
        if plata(txt) != esperado:
            fallas.append(f"plata: '{txt}' -> {plata(txt)}, se esperaba {esperado}")
    for args, esperado in _CASOS_ETAPA:
        got = etapa_de_caida(*args)
        if got != esperado:
            fallas.append(f"etapa: {args} -> '{got}', se esperaba '{esperado}'")
    for tel, esperado in _CASOS_CANAL:
        got = canal_de(tel)
        if got != esperado:
            fallas.append(f"canal: {tel!r} -> {got}, se esperaba {esperado}")
    if fallas:
        raise SystemExit("EL CLASIFICADOR DE MOTIVOS ESTA ROTO, no se analiza nada:\n  " +
                         "\n  ".join(fallas))
    _probado[0] = True



MAL_CHATS = """NO SE ENTIENDE EL ARCHIVO DE CHATS: %s
  Se esperaba lo que produce `barrer_chats.py`: un objeto con la clave 'chats'
  (un diccionario ns -> conversacion).
  Lo que llego: %s.
  Sin los hilos no se puede decir quien hablo de ultimo ni por que no compraron, y
  esas dos son las columnas de la Parte 1. No se analiza lo que no se entiende."""


MAL_UNIVERSO = """NO SE ENTIENDE EL UNIVERSO DE CONTACTOS: %s
  Se esperaba una lista de contactos, o un objeto con 'contactos' / 'data' /
  'subscribers' (lista, o diccionario ns->contacto).
  Lo que llego: %s.
  No se calcula una conversion sobre algo que no se sabe contar: el denominador
  saldria plausible y falso."""


def _universo_como_lista(u, ruta):
    """El universo de contactos, venga como venga. Y si no se entiende, MUERE hablando.

    POR QUE EXISTE, medido por LOGISTICA GOLDEN el 2026-08-18: aqui se hacia
    `_u.get("contactos") or _u.get("data") or []`, y el productor real
    (`cosecha_chatea_total.py`) entrega `data` como **diccionario ns->contacto**. Un dict
    es verdadero, asi que pasaba el `or`... y despues se iteraba, que en un dict
    devuelve las CLAVES: cadenas. `medir_conversion()` moria con
    `AttributeError: 'str' object has no attribute 'get'` — un error a tres funciones de
    distancia de la causa, que es la peor forma de fallar: el mensaje no nombra ni el
    archivo ni el campo.

    LA CLASE: **un `or` encadenado no valida, solo elige el primero que no sea falso.**
    Y un contenedor vacio de la forma correcta y uno lleno de la forma equivocada se
    parecen mucho cuando solo se pregunta si son verdaderos.
    """
    if isinstance(u, list):
        datos = u
    elif isinstance(u, dict):
        for clave in ("contactos", "data", "subscribers"):
            v = u.get(clave)
            if isinstance(v, list):
                datos = v
                break
            if isinstance(v, dict):
                # ns -> contacto: los contactos son los VALORES, no las claves.
                datos = list(v.values())
                break
        else:
            datos = None
    else:
        datos = None
    if datos is None or (datos and not isinstance(datos[0], dict)):
        sys.exit(MAL_UNIVERSO % (ruta, type(u).__name__))


    return datos


def main():
    _exigir_autoprueba()
    sin_tiempo = 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--chats", required=True)
    ap.add_argument("--contactos", required=True)
    ap.add_argument("--dropi", required=True)
    ap.add_argument("--salida", required=True)
    # LA CONVERSION DE LA CUENTA NO SE PUEDE MEDIR DESDE UN RECORTE, Y NO HAY VUELTA.
    # `--contactos` suele ser el recorte de no compradores: adentro no hay un solo
    # comprador, asi que cualquier division da cero. La conversion real solo existe
    # cruzando la lista COMPLETA del espacio contra Dropi, y por eso se pide aparte.
    # Si no se entrega, no se estima ni se aproxima: el informe se niega a publicarla.
    # (El intento anterior fue restar el recorte a los pedidos del embudo: daba 157
    # cuando eran 94, porque son dos universos distintos metidos en la misma resta.)
    ap.add_argument("--contactos-universo", dest="universo",
                    help="lista COMPLETA del espacio; sin ella no se publica conversion")
    a = ap.parse_args()

    # LAS TRES PUERTAS DE ENTRADA SE DEFIENDEN IGUAL.
    #
    # Medido el 2026-08-19 corriendo el runbook paso a paso: de las cuatro entradas de
    # este script, **dos tenian compuerta, una la tenia a medias y `--chats` ninguna**.
    # Pasarle a `--chats` un archivo de otra forma moria con
    # `TypeError: list indices must be integers` en `CH["chats"]`, sin nombrar el
    # archivo ni decir que se esperaba.
    #
    # Y lo que hace este caso distinto: **la compuerta del universo se escribio ayer
    # para esta misma clase** y se aplico a UNA puerta. Arreglar una entrada y no su
    # familia es como no arreglarla — la de al lado sigue muriendo igual. Es la tercera
    # vez en esta revision que aparece el mismo «dos de cuatro»: la regla existia,
    # estaba escrita, y se aplico donde alguien se acordo.
    CH = leer_json(a.chats)
    if not isinstance(CH, dict) or not isinstance(CH.get("chats"), dict):
        sys.exit(MAL_CHATS % (a.chats, type(CH).__name__))
    chats = CH["chats"]
    contactos = _universo_como_lista(leer_json(a.contactos), a.contactos)
    D = leer_json(a.dropi)
    if D.get("cosecha_completa") is not True:
        raise SystemExit("ANALISIS NO CONFIABLE: el volcado de Dropi no dice cosecha_completa=true.")

    # AQUI VIVIA UNA COPIA DE `tel10` ANIDADA Y RENOMBRADA A `t10`: doble evasion del
    # detector de copias, que buscaba `^def tel10` a nivel de modulo. Anidar y renombrar
    # no es astucia, es como sobreviven los duplicados a los barridos.
    t10 = tel10

    tel_dropi = {t10(o.get("phone")) for o in D["ordenes"] if t10(o.get("phone"))}

    def uf(c, n):
        for f in (c.get("user_fields") or []):
            if f.get("name") == n:
                return f.get("value")
        return None

    motivos = Counter()
    quien_cierra = Counter()
    calientes, por_motivo, sin_chat = [], {}, 0

    # ------------------------------------------------------------------
    # EL RESIDUO DEL OTRO LADO. Este analizador recorre LOS CONTACTOS y busca la
    # conversacion de cada uno, asi que tiene contador para "contacto sin
    # conversacion" — y no tenia ninguno para "conversacion sin contacto".
    # Una conversacion que llega y no esta en la lista NO se contaba, NO se
    # declaraba y NO existia: se caia del universo sin dejar rastro.
    # Medido cuando lo destapo el chat LOGISTICA DOLCE: de 100 conversaciones que
    # entregaron, 57 no estaban en la lista de contactos — la lista era de 17 horas
    # antes. El analisis dijo "42 con conversacion" sobre 100 reales, y ningun
    # numero del informe lo delataba.
    #
    # LA CLASE: todo cruce de dos conjuntos declara LOS DOS residuos. Las compuertas
    # de esta skill vigilaban el lado del universo que ella controla; ninguna
    # vigilaba el lado que le entregan.
    #
    # Y no es lo mismo que el otro residuo: "no baje su conversacion" es un dato que
    # falta; "tengo su conversacion y no se de quien es" es un dato que LLEGO y se
    # esta tirando.
    # ------------------------------------------------------------------
    ns_contactos = {c.get("user_ns") for c in contactos}
    huerfanas = [ns for ns in chats if ns not in ns_contactos]
    compradores, no_compradores = 0, 0

    # EL CORPUS DE PRIMEROS MENSAJES, que es lo que define que texto es plantilla.
    # El prellenado es el PRIMER mensaje cronologico del cliente. Cual extremo del
    # array sea eso depende de quien escribio el archivo, asi que aqui tampoco se
    # asume: con `ts` se ordena, y sin `ts` se invierte, el mismo criterio explicito
    # que usa el resto del modulo.
    primeros = []
    for _c in contactos:
        _ms = [m for m in (chats.get(_c.get("user_ns")) or []) if m.get("t") in ("in", "out")]
        if not _ms:
            continue
        if all(m.get("ts") for m in _ms):
            _ms = sorted(_ms, key=lambda m: m["ts"])
        else:
            _ms = list(reversed(_ms))
        for m in _ms:
            if m.get("t") == "in":
                primeros.append(m.get("c"))
                break
    PLANTILLAS = plantillas_de(primeros)

    def es_propio(m):
        """Lo escribio la persona: ni plantilla del anuncio, ni mensaje sin texto.

        UN MENSAJE VACIO NO ES SILENCIO, ES UN DATO QUE FALTA. Medido: 58 entrantes
        vacios en Dolce, y el barrido no guarda `msg_type`, asi que un AUDIO, una foto
        y un mensaje borrado se ven identicos — una comilla vacia. Uno de esos vacios
        resulto ser una nota de voz de una clienta que llevaba ocho dias sin respuesta,
        con su transcripcion esperando en el API. Por eso no se descarta: cuenta como
        mensaje y la fila lo DECLARA. Equivocarse llamando a alguien cuesta un mensaje;
        equivocarse borrandolo cuesta la venta (formulacion de LOGISTICA DOLCE).
        """
        return norm((m.get("c") or "").strip()) not in PLANTILLAS

    for c in contactos:
        ns = c.get("user_ns")
        compro = t10(c.get("phone")) in tel_dropi
        if compro:
            compradores += 1
            continue
        no_compradores += 1
        msgs = chats.get(ns)
        if msgs is None:
            sin_chat += 1
            motivos["NO SE PUDO MIRAR: no se bajo la conversacion"] += 1
            continue
        # El hilo trae TRES tipos: 'in' (lo escribio el cliente), 'out' (lo dijo el
        # bot o el agente) y 'note' (eventos internos, sobre todo los avisos de pixel
        # de Meta). Las notas NO son conversacion y hay que sacarlas antes de nada:
        # como se disparan despues del ultimo mensaje real, si cuentan como "hablo el
        # bot" invierten la señal mas cara del informe y un cliente que quedo
        # esperando respuesta aparece como cliente que se fue.
        # Las `note` NO son conversacion: son los eventos de pixel de Meta, y se
        # disparan DESPUES del ultimo mensaje real. Si cuentan como "hablo el bot",
        # invierten justo la señal mas cara del informe.
        reales = [m for m in msgs if m.get("t") in ("in", "out")]
        del_cliente = [m for m in reales if m.get("t") == "in"]
        del_bot = [m for m in reales if m.get("t") == "out"]
        texto_cliente = norm(" ".join((m.get("c") or "") for m in del_cliente))
        texto_bot = " ".join((m.get("c") or "") for m in del_bot)

        item = {"tel": t10(c.get("phone")), "nombre": c.get("name") or "",
                "ciudad": (uf(c, "Ciudad") or "").strip(),
                "producto": (uf(c, "Productos escogidos") or "").strip(),
                "tablero": uf(c, "Tablero") or "",
                "ult": c.get("last_interaction") or c.get("subscribed"),
                "msgs_cliente": len(del_cliente), "msgs_bot": len(del_bot)}

        if not del_cliente:
            motivos["Nunca escribio: entro y no dijo nada"] += 1
            por_motivo.setdefault("Nunca escribio: entro y no dijo nada", []).append(item)
            continue

        # ORDENAR SIN TIEMPO ES EL CASO QUE HAY QUE RESOLVER, NO EL EXCEPCIONAL.
        # Un archivo de otra mano puede venir sin `ts` — pasa: `created_at` y `date`
        # vienen vacios en el API y quien guarde esos se queda sin tiempos. Si aqui
        # se ordenara por `ts` a secas, con todos en None el sort NO HACE NADA y el
        # array se queda como llego: del mas reciente al mas viejo. O sea que el
        # "arreglo" reintroduciria la inversion en silencio, que es peor que no tenerlo.
        # Por eso: con tiempo se ordena; SIN tiempo se INVIERTE, porque el API entrega
        # descendente y esa es la unica informacion de orden que queda.
        con_ts = [x for x in reales if x.get("ts")]
        if len(con_ts) == len(reales) and reales:
            reales = sorted(reales, key=lambda x: x["ts"])
            orden_por = "ts"
        else:
            reales = list(reversed(reales))
            orden_por = "posicion (el archivo no trae ts)"
        sin_tiempo += 0 if orden_por == "ts" else 1
        ultimo = reales[-1] if reales else None
        cierra_cliente = bool(ultimo and ultimo.get("t") == "in")
        quien_cierra["cliente" if cierra_cliente else "bot"] += 1

        if cierra_cliente:
            m = "LA PELOTA LA TIENE LA EMPRESA: el cliente escribio de ultimo y nadie respondio"
            motivos[m] += 1
            propios = [x for x in del_cliente if es_propio(x)]
            _ult = (propios[-1].get("c") if propios else "") or ""
            # UNA FILA MUDA TIENE QUE DECIR QUE ESTA MUDA. Aqui salia una comilla
            # vacia: la fila afirmaba que alguien esperaba respuesta y no decia que
            # pregunto, sin explicar por que. Era una nota de voz.
            item["sin_texto"] = bool(propios) and not _ult.strip()
            item["ultimo_texto"] = (_ult[:160] if _ult.strip() else
                                    "[mensaje sin texto — probablemente un audio o una "
                                    "imagen; el barrido no guarda el tipo. HAY QUE ABRIR "
                                    "LA CONVERSACION EN CHATEA]")
            item["solo_toco_el_boton"] = not propios
            item["pregunta"] = bool(PREGUNTA.search(norm(item["ultimo_texto"])))
            # EL CANAL MANDA LA ACCION, Y NO TODOS SE PUEDEN LLAMAR.
            # Medido: 84 de 743 contactos (11%) no tienen telefono — no son de WhatsApp,
            # son comentarios de Facebook e Instagram. Tres de los nueve calientes eran
            # de esos. Una lista de acciones que no dice el canal manda a "llamar" a
            # quien no tiene numero, y esa fila se queda sin hacer sin que nadie sepa.
            # Y el comentario publico URGE MAS: un mensaje sin responder lo lee uno; un
            # comentario sin responder debajo de un anuncio vivo lo lee todo el que
            # llegue al anuncio. Se midio uno donde dos clientas comentaban que estaba
            # mas barato en otro lado, sin una sola respuesta de la empresa.
            item["canal"] = canal_de(item["tel"])
            item["accion"] = ("llamar o escribir por WhatsApp" if item["tel"]
                              else "RESPONDER EL COMENTARIO en el anuncio (no hay telefono, "
                                   "y lo esta leyendo todo el que llega al anuncio)")
            calientes.append(item)
            por_motivo.setdefault(m, []).append(item)
            continue

        # ETAPA DE CAIDA · formulacion del chat LOGISTICA DOLCE, adoptada con credito.
        #
        # QUE REEMPLAZA: aqui habia un cubo "se le pidieron los datos y no los completo"
        # que se disparaba con lo que decia EL BOT. Medido sobre el universo entero de
        # Dolce (743 de 743): se tragaba 623, el 83,8%. Un cubo que se lleva ocho de cada
        # diez no clasifica nada — describe el guion del bot, que pide los datos siempre.
        #
        # LA CLASE: el motivo no se busca en lo que el bot dijo, sino en HASTA DONDE
        # LLEGO EL CLIENTE. Esa pregunta si tiene respuestas distintas por contacto, y
        # cada respuesta trae su accion: al que le falta un solo dato se le pide ese dato;
        # al que solo toco el boton no hay a quien llamar.
        #
        # LA PRIORIDAD ES PARTE DE LA DEFINICION, no un detalle: un contacto cae en
        # varias a la vez y el cubo que gana es el que manda la accion. Va de mas
        # accionable a menos: primero al que le falta UN dato, de ultimo el que no dejo
        # nada con que trabajar. Cambiar este orden cambia los numeros; por eso se
        # declara aqui y se imprime en la salida.
        propios = [x for x in del_cliente if es_propio(x)]
        ciudad = item["ciudad"]
        direccion = (uf(c, "Direccion") or uf(c, "Dirección") or "").strip()
        hallados = [n for n, p in SENALES if re.search(p, texto_cliente)]
        if hallados:
            # La objecion DICHA POR EL CLIENTE gana sobre la etapa: si dijo por que no
            # compra, eso es mejor informacion que hasta donde llego en el formulario.
            m = "Objecion del cliente: " + hallados[0]
            item["senales"] = hallados
        else:
            m = etapa_de_caida(ciudad, direccion, len(del_cliente), len(propios))
        item["etapa_de_caida"] = m
        motivos[m] += 1
        por_motivo.setdefault(m, []).append(item)

    # COMPUERTA DE CORDURA (idea del chat LOGISTICA DOLCE, que la pago primero).
    # Si casi todas las conversaciones "cierran con el cliente", no es que la empresa
    # nunca conteste: es que el hilo viene al reves y se esta leyendo el saludo inicial
    # como si fuera el ultimo mensaje. A ellos les dio 369 de 374 — 98,7% — y el
    # absurdo se ve de cara. Una señal que sale asi NO SE PUBLICA.
    _tot = quien_cierra["cliente"] + quien_cierra["bot"]
    if _tot >= 20 and quien_cierra["cliente"] / _tot > 0.90:
        raise SystemExit(
            f"ORDEN SOSPECHOSO: {quien_cierra['cliente']} de {_tot} conversaciones "
            f"({100 * quien_cierra['cliente'] / _tot:.1f}%) cierran con el cliente.\n"
            "Eso no pasa en una operacion real. Casi seguro el hilo viene al reves y se "
            "esta leyendo el primer mensaje como si fuera el ultimo.\n"
            "NO se escribe una lista de 'nadie le respondio' construida sobre eso.")

    calientes.sort(key=lambda x: x.get("ult") or "", reverse=True)
    # UN UNIVERSO SIN COMPRADORES NO PRODUCE UNA CONVERSION, PRODUCE UN CERO.
    # Medido el 2026-08-11: esta lista suele ser el RECORTE de no compradores con
    # actividad reciente, o sea que por construccion no tiene un solo comprador
    # dentro. La division sale 0.0 y el informe la imprimia como "la conversion de
    # la cuenta es 0.0%" — que no es un conteo mal puesto sino una AFIRMACION FALSA
    # sobre el negocio: la real era 10,44% sobre los 900 del espacio completo.
    # Es la ley del cero honesto en el sitio mas caro. Un cero que sale de un
    # universo que no podia contener otra cosa no mide el negocio, mide el filtro.
    # Por eso el numero no viaja solo: viaja con la bandera que dice si se puede leer.
    recorte = compradores == 0 and no_compradores > 0

    # La conversion verdadera, si y solo si se entrego la lista completa.
    uni_n = uni_compra = uni_pct = None
    conv = None
    if a.universo:
        try:
            _u = leer_json(a.universo, encoding="utf-8")
            _u = _universo_como_lista(_u, a.universo)
            # LA REGLA DEL DENOMINADOR NO SE ESCRIBE AQUI: se importa.
            # Este script contaba a todo el mundo y el embudo excluia a los contactos
            # que crea la integracion de Dropi. Misma pregunta, dos respuestas, las dos
            # publicadas en la misma pagina: 10,44% contra 6,07%. Ahora la regla vive
            # en `denominador.py` y los dos la usan, asi que no puede haber dos.
            conv = medir_conversion(_u, tel_dropi)
            uni_n = conv["denominador"]
            uni_compra = conv["compradores"]
            uni_pct = conv["conversion_pct"]
        except (OSError, ValueError) as e:
            raise SystemExit(f"NO SE PUDO LEER LA LISTA COMPLETA {a.universo}: {e}\n"
                             "  Se corrige la ruta o se corre sin ella; lo que no se hace "
                             "es publicar una conversion que no se midio.")
    res = {
        "universo": len(contactos),
        "compradores": compradores,
        "no_compradores": no_compradores,
        "universo_es_recorte_sin_compradores": recorte,
        "conversion_pct_se_puede_leer": not recorte,
        "_por_que_no_se_puede_leer": ("el universo no contiene ni un comprador, asi que el "
                                      "porcentaje es cero por construccion y no dice nada de "
                                      "la cuenta. La conversion real se mide sobre la lista "
                                      "COMPLETA del espacio, no sobre el recorte") if recorte else "",
        "conversion_pct": round(100 * compradores / len(contactos), 2) if contactos else None,
        # La cuenta entera. None significa "no se midio", jamas "no hay".
        "universo_completo": uni_n,
        "compradores_universo": uni_compra,
        "conversion_universo_pct": uni_pct,
        # SOLO EL NOMBRE DEL ARCHIVO, NUNCA LA RUTA. La ruta absoluta lleva el nombre
        # de usuario del Mac y este JSON se comparte entre chats y se adjunta.
        "_fuente_conversion": (f"cruce de {os.path.basename(a.universo)} contra los telefonos "
                               f"del volcado de Dropi, con la regla de denominador.py"
                               if uni_n is not None
                               else "NO SE MIDIO: no se entrego --contactos-universo. El "
                               "informe no debe publicar conversion de la cuenta"),
        # Todo lo que hace falta para LEER ese porcentaje: a quien se excluyo y por que,
        # cuantos no pueden estar arriba del todo, y contactos contra personas.
        "conversion_detalle": conv,
        "sin_chat_bajado": sin_chat,
        "conversaciones_sin_contacto": len(huerfanas),
        "conversaciones_sin_contacto_ns": huerfanas[:50],
        "_que_es_sin_contacto": ("conversaciones que venian en el archivo de chats y cuyo "
                                 "user_ns NO esta en la lista de contactos: hay dato y no se "
                                 "puede usar. Casi siempre significa que la lista de contactos "
                                 "es mas vieja que el barrido; se arregla rebajando el listado "
                                 "al inicio de la corrida, no ignorandolas"),
        "quien_habla_de_ultimo": dict(quien_cierra),
        "hilos_sin_tiempo": sin_tiempo,
        "motivos": dict(motivos.most_common()),
        "_orden_de_los_cubos": ("etapa_de_caida, formulacion de LOGISTICA DOLCE. Un contacto "
                                "cae en varios cubos a la vez y gana el de mas arriba, porque "
                                "es el que manda la accion. Orden: objecion declarada > ciudad "
                                "sin direccion > datos completos sin pedido > nunca escribio > "
                                "solo el clic del anuncio > escribio una vez > converso sin "
                                "ubicacion. Cambiar el orden cambia los numeros"),
        "calientes": calientes,
        "calientes_por_canal": {
            "whatsapp": sum(1 for x in calientes if x.get("canal") == "whatsapp"),
            "comentario_publico": sum(1 for x in calientes
                                      if x.get("canal") == "comentario_publico"),
        },
        "contactos_sin_telefono": sum(1 for c in contactos if not t10(c.get("phone"))),
        "por_motivo": {k: v[:60] for k, v in por_motivo.items()},
        # EL NOMBRE GRITA QUE ES UNA MUESTRA. Se llamaba `fallos_barrido` y estaba
        # recortada a 20: un consumidor que hiciera `len(...)` publicaba 20 cuando
        # eran 64 (medido en Golden el 2026-08-18). El total vive aparte y siempre
        # se lee del total, nunca del largo de la muestra.
        "muestra_fallos_barrido": CH.get("fallos", [])[:20],
        "n_fallos_barrido": len(CH.get("fallos", [])),
    }
    escribir_json(a.salida, res, indent=1)
    lectura = (f"({res['conversion_pct']}%)" if not recorte
               else "(NO se puede leer: el universo es un recorte sin compradores)")
    print(f"universo {len(contactos)} | compraron {compradores} {lectura} | "
          f"no compraron {no_compradores}")
    for k, v in motivos.most_common():
        print(f"  {v:4d}  {k}")
    print(f"calientes (la empresa debe responder): {len(calientes)}")
    if huerfanas:
        print(f"  OJO: {len(huerfanas)} conversaciones del archivo NO tienen contacto en la "
              f"lista y quedan fuera de esta medicion ({100*len(huerfanas)/max(len(chats),1):.0f}% "
              f"de las {len(chats)} bajadas). La lista de contactos esta mas vieja que el "
              "barrido: rebajala al inicio de la corrida.")


if __name__ == "__main__":
    main()
