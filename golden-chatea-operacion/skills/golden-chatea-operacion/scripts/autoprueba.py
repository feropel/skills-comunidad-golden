#!/usr/bin/env python3
"""
AUTOPRUEBA · golden-chatea-operacion

Fabrica un dia de conversaciones que se SABE roto, con las 13 trampas del encargo sembradas
una por una (mas casos extra de calidad de respuesta), y exige que clasificar.py las detecte
TODAS antes de correr contra un DUMP real.

Por que existe: un clasificador que sale en verde contra un dia real no prueba que el dia este
sano, prueba que el clasificador no mira. La higiene es al reves -- si un script dice que todo
esta bien a la primera, lo primero que se sospecha es el script.

Metodo: para las trampas que son funciones puras (parseo de fecha, de dinero, inversion de
hilo, deteccion del mensaje automatico) se prueba la funcion directamente con un caso que se
SABE roto. Para las que solo se ven en la clasificacion completa de una conversacion (dropi,
compuerta de cordura, preguntas sin cobertura, calidad de respuesta) se arma un contacto
sintetico y se corre Clasificador encima.

Uso:
    python3 autoprueba.py
"""

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from clasificar import (                                          # noqa: E402
    Clasificador, invertir_hilo, parse_fecha, parse_dinero,
    direccion, contenido_real, redactar_texto, imprimir, es_nota_pixel,
    plantillas_de, MIN_PERSONAS_FORMA, _parsear_argv,
)

RESULTADOS = {}   # codigo -> (paso: bool, detalle: str)


def marcar(codigo, paso, detalle=""):
    RESULTADOS[codigo] = (paso, detalle)


# ---------------------------------------------------------------------- P2 (estructural)
def test_p2():
    """El parametro de contacto es user_ns, nunca subscriber_id (encargo trampa 2)."""
    fuente = (AQUI / "extraer.py").read_text()
    usa_user_ns = "user_ns=user_ns" in fuente
    usa_include_bot = "include_bot=1" in fuente
    marcar("P2", usa_user_ns and usa_include_bot,
          f"user_ns=user_ns presente: {usa_user_ns} · include_bot=1 presente: {usa_include_bot}")


# ---------------------------------------------------------------------- P3 / P4 (inversion)
def test_p3_p4():
    """P3: el hilo llega del mas reciente al mas viejo y se invierte a orden cronologico.
    P4: si TODOS los ts son None, el fallback invierte -- nunca un sort() no-op."""
    # P3: servidor entrega en un orden CUALQUIERA con ts reales; se debe reordenar por ts.
    crudo = [
        {"content": "c3 (mas nuevo)", "direction": "cliente", "ts": "2026-08-19 10:03:00"},
        {"content": "c1 (mas viejo)", "direction": "cliente", "ts": "2026-08-19 10:01:00"},
        {"content": "c2 (medio)", "direction": "empresa", "ts": "2026-08-19 10:02:00"},
    ]
    resultado = invertir_hilo(crudo)
    orden_ok = [m["content"] for m in resultado] == ["c1 (mas viejo)", "c2 (medio)",
                                                      "c3 (mas nuevo)"]
    marcar("P3", orden_ok, f"orden obtenido: {[m['content'] for m in resultado]}")

    # P4: TODOS los ts en None. El servidor entrega reciente->viejo (raw[0] es el mas nuevo).
    raw_reciente_a_viejo = [
        {"content": "el mas nuevo", "direction": "empresa", "ts": None},
        {"content": "medio", "direction": "cliente", "ts": None},
        {"content": "el mas viejo", "direction": "cliente", "ts": None},
    ]
    resultado2 = invertir_hilo(raw_reciente_a_viejo)
    esperado = list(reversed(raw_reciente_a_viejo))
    es_invertido = resultado2 == esperado
    es_no_op = resultado2 == raw_reciente_a_viejo
    paso = es_invertido and not es_no_op
    marcar("P4", paso,
          f"invertido correctamente: {es_invertido} · fue un no-op (mal): {es_no_op}")


# ---------------------------------------------------------------------- P5 (notas de pixel)
def test_p5():
    """Llama a `es_nota_pixel` de verdad (no reimplementa el filtro en linea: eso fue
    un defecto real de esta misma autoprueba, hallado en la segunda verificacion
    adversarial -- el test pasaba aunque la funcion real devolviera False siempre)."""
    crudo = [
        {"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00"},
        {"type": "out", "content": "hola, en que te ayudo", "ts": "2026-08-19 09:01:00"},
        {"type": "note", "content": "PageView pixel event", "ts": "2026-08-19 09:02:00"},
    ]
    hilo = invertir_hilo(crudo)
    hilo_limpio = [m for m in hilo if not es_nota_pixel(m)]
    paso = len(hilo_limpio) == 2 and all(not es_nota_pixel(m) for m in hilo_limpio)
    marcar("P5", paso, f"{len(hilo)} mensajes crudos, {len(hilo_limpio)} tras excluir notas "
                       "(via es_nota_pixel real)")


# ---------------------------------------------------------------------- P6 / P7 (anuncio y objecion)
def test_p6_p7():
    """P6 usa deteccion MEDIDA (frecuencia/forma), igual criterio que
    golden-logistica-diaria: una frase identica en 3+ personas es plantilla del anuncio.
    Se fabrican 3 contactos con el MISMO primer mensaje (para que cruce el umbral) y uno
    de ellos ademas escribe una objecion real de precio."""
    plantilla = "¡Hola! Quiero informacion y precio de CREMA X"

    def gemelo(n, extra=None):
        msgs = [{"type": "in", "content": plantilla, "ts": f"2026-08-19 10:00:0{n}",
                "payload": {"referral": {"source_id": "999", "body": plantilla}}}]
        if extra:
            msgs.append(extra)
        return {"user_ns": f"f1p6p7-{n}", "get_info": {}, "mensajes": msgs}

    extra_objecion = {"type": "in", "content": "eso me parece muy costoso la verdad",
                      "ts": "2026-08-19 10:02:00"}
    respuesta_bot = {"type": "out", "content": "hola, con gusto te cuento",
                     "ts": "2026-08-19 10:01:00"}

    contactos = [gemelo(0, extra_objecion), gemelo(1, respuesta_bot), gemelo(2)]
    c = Clasificador({"contactos": contactos}).correr()
    conv0 = c.conversaciones[0]

    es_plantilla = plantilla.lower() in c.plantillas
    motivo_correcto = conv0["motivo_no_compra"] == ["precio"]
    paso = es_plantilla and motivo_correcto
    marcar("P6", es_plantilla,
          f"plantilla detectada por medicion (3 personas identicas): {es_plantilla} · "
          f"plantillas = {c.plantillas}")
    marcar("P7", motivo_correcto, f"motivo_no_compra = {conv0['motivo_no_compra']} (debe ser "
                                  "exactamente ['precio'], sin contar el mensaje del anuncio "
                                  "ni lo que dice el bot)")


# ---------------------------------------------------------------------- P8 (audio y feed)
def test_p8():
    audio_con_texto = {"content": "", "direction": "cliente", "msg_type": "audio",
                       "ts": "2026-08-19 11:00:00",
                       "payload": {"transcribed_text": "hola quiero saber el precio"}}
    audio_sin_texto = {"content": "", "direction": "cliente", "msg_type": "audio",
                       "ts": "2026-08-19 11:05:00"}
    comentario_feed = {"content": "que bonito producto", "direction": "cliente",
                       "msg_type": "feed", "ts": "2026-08-19 11:10:00"}
    saludo_empresa = {"content": "hola, en que te ayudo", "direction": "empresa",
                      "msg_type": "text", "ts": "2026-08-19 10:59:00"}

    texto_ok = contenido_real(audio_con_texto) == "hola quiero saber el precio"

    contacto = {"user_ns": "f1p8", "get_info": {},
               "mensajes": [comentario_feed, audio_sin_texto, audio_con_texto, saludo_empresa]}
    c = Clasificador({"contactos": [contacto]}).correr()
    conv = c.conversaciones[0]
    feed_separado = conv["n_comentarios_feed"] == 1
    disparo_sin_texto = any(h["control"] == "P8" for h in c.hallazgos)
    paso = texto_ok and feed_separado and disparo_sin_texto
    marcar("P8", paso, f"transcripcion usada: {texto_ok} · feed separado: {feed_separado} "
                       f"({conv['n_comentarios_feed']}) · aviso de audio mudo disparado: "
                       f"{disparo_sin_texto}")


# ---------------------------------------------------------------------- P9 (fechas)
def test_p9():
    """Mismo dia: 'a' con ESPACIO es 23:59:59 (tarde). 'b' con T es 00:00:01 (temprano).
    Textualmente 'a' < 'b' (espacio 0x20 < 'T' 0x54) pero en tiempo real a > b."""
    a = "2026-08-10 23:59:59"
    b = "2026-08-10T00:00:01"
    comparacion_textual_dice_a_menor = a < b
    da, db = parse_fecha(a), parse_fecha(b)
    comparacion_real_dice_a_mayor = da is not None and db is not None and da > db
    paso = comparacion_textual_dice_a_menor and comparacion_real_dice_a_mayor
    marcar("P9", paso,
          f"texto dice a<b: {comparacion_textual_dice_a_menor} · parseado dice a>b: "
          f"{comparacion_real_dice_a_mayor} (la trampa es real y parse_fecha la resuelve)")


# ---------------------------------------------------------------------- P10 (dinero)
def test_p10():
    miles, fmt_miles = parse_dinero("142.800")
    decimal, fmt_decimal = parse_dinero("74900.00")
    paso = (miles == 142800.0 and fmt_miles == "miles" and
           decimal == 74900.0 and fmt_decimal == "decimal")
    marcar("P10", paso, f"'142.800' -> {miles} ({fmt_miles}) · '74900.00' -> {decimal} "
                        f"({fmt_decimal})")


# ---------------------------------------------------------------------- P11 (dropi)
def test_p11():
    contactos = [
        {"user_ns": "f1dropi", "get_info": {"data": {"opted_in_through": "dropi"}},
         "mensajes": [{"content": "hola", "direction": "cliente", "msg_type": "text",
                      "ts": "2026-08-19 08:00:00"}]},
        {"user_ns": "f1normal", "get_info": {"data": {"opted_in_through": "chat"}},
         "mensajes": [{"content": "hola", "direction": "cliente", "msg_type": "text",
                      "ts": "2026-08-19 08:00:00"},
                     {"content": "hola, en que te ayudo", "direction": "empresa",
                      "msg_type": "text", "ts": "2026-08-19 08:01:00"}]},
    ]
    c = Clasificador({"contactos": contactos}).correr()
    excluido = "f1dropi" in c.excluidos_dropi and "f1normal" not in c.excluidos_dropi
    declarado = any(x["control"] == "P11" for x in c.cobertura)
    paso = excluido and declarado
    marcar("P11", paso, f"excluidos_dropi = {c.excluidos_dropi} · declarado en cobertura: "
                        f"{declarado}")


# ---------------------------------------------------------------------- P12 (campo autollenado)
def test_p12():
    """No basta con que el texto 'Productos escogidos' no aparezca (aparece en la nota de
    cobertura, documentando la regla). Lo que se prueba es que el codigo NUNCA lo LEE como
    evidencia: ni con .get(...) ni con acceso por indice."""
    fuente = (AQUI / "clasificar.py").read_text()
    patrones_de_lectura = [
        '.get("Productos escogidos")', ".get('Productos escogidos')",
        '["Productos escogidos"]', "['Productos escogidos']",
    ]
    lo_lee = any(p in fuente for p in patrones_de_lectura)
    marcar("P12", not lo_lee,
          f"clasificar.py {'SI' if lo_lee else 'no'} lee 'Productos escogidos' como campo "
          "-- solo puede aparecer documentado, nunca consultado como evidencia")


# ---------------------------------------------------------------------- P13 (compuerta)
def test_p13():
    def contacto_cierre(n):
        return {"user_ns": f"cierre{n}", "get_info": {},
               "mensajes": [
                   {"content": "quiero comprarlo", "direction": "cliente", "msg_type": "text",
                    "ts": "2026-08-19 09:00:00"},
                   {"content": "listo, pedido confirmado, gracias por tu compra",
                    "direction": "empresa", "msg_type": "text", "ts": "2026-08-19 09:01:00"},
               ]}

    def contacto_abierto(n):
        return {"user_ns": f"abierto{n}", "get_info": {},
               "mensajes": [
                   {"content": "hola, en que te ayudo", "direction": "empresa",
                    "msg_type": "text", "ts": "2026-08-19 09:00:00"},
                   {"content": "cuanto cuesta el envio a mi ciudad", "direction": "cliente",
                    "msg_type": "text", "ts": "2026-08-19 09:05:00"},
               ]}

    # dia SANO: 5 de 10 cierran -> 50%, NO debe activar la compuerta
    dia_sano = [contacto_cierre(i) for i in range(5)] + [contacto_abierto(i) for i in range(5)]
    c_sano = Clasificador({"contactos": dia_sano}).correr()
    sano_no_activa = c_sano.universo["compuerta_activada"] is False

    # dia ROTO: 19 de 20 cierran -> 95%, DEBE activar la compuerta
    dia_roto = [contacto_cierre(i) for i in range(19)] + [contacto_abierto(0)]
    c_roto = Clasificador({"contactos": dia_roto}).correr()
    roto_si_activa = c_roto.universo["compuerta_activada"] is True
    disparo = any(h["control"] == "P13" for h in c_roto.hallazgos)

    paso = sano_no_activa and roto_si_activa and disparo
    marcar("P13", paso,
          f"dia sano (50%) activa={c_sano.universo['compuerta_activada']} (debe ser False) · "
          f"dia roto (95%) activa={c_roto.universo['compuerta_activada']} (debe ser True) · "
          f"hallazgo P13 disparado: {disparo}")


# ------------------------------------------------------------ P1 (contacto sin mensaje saliente)
def test_p1():
    contacto = {"user_ns": "f1p1", "get_info": {},
               "mensajes": [
                   {"content": "hola", "direction": "cliente", "msg_type": "text",
                    "ts": "2026-08-19 08:00:00"},
                   {"content": "estoy interesado", "direction": "cliente", "msg_type": "text",
                    "ts": "2026-08-19 08:01:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    disparo = any(h["control"] == "P1" for h in c.hallazgos)
    marcar("P1", disparo, f"hallazgo P1 disparado para contacto sin mensajes de empresa: "
                          f"{disparo}")


# ----------------------------------------------------- calidad de respuesta (complementarios)
def test_calidad():
    # R1: sin respuesta
    c1 = {"user_ns": "fR1", "get_info": {},
         "mensajes": [{"content": "hola, cuanto cuesta?", "direction": "cliente",
                      "msg_type": "text", "ts": "2026-08-19 14:00:00"}]}
    # R2: respuesta tardia (61 min de verdad entre el mensaje del cliente y la respuesta)
    c2 = {"user_ns": "fR2", "get_info": {},
         "mensajes": [
             {"content": "cuanto cuesta", "direction": "cliente", "msg_type": "text",
              "ts": "2026-08-19 12:00:00"},
             {"content": "disculpa la demora, cuesta 74900", "direction": "empresa",
              "msg_type": "text", "ts": "2026-08-19 13:01:00"},
         ]}
    # R3: bucle (3 iguales seguidas)
    c3 = {"user_ns": "fR3", "get_info": {},
         "mensajes": [
             {"content": "no entendi, puedes reformular?", "direction": "empresa",
              "msg_type": "text", "ts": "2026-08-19 13:03:00"},
             {"content": "no entendi, puedes reformular?", "direction": "empresa",
              "msg_type": "text", "ts": "2026-08-19 13:02:00"},
             {"content": "no entendi, puedes reformular?", "direction": "empresa",
              "msg_type": "text", "ts": "2026-08-19 13:01:00"},
             {"content": "hola necesito ayuda con mi pedido", "direction": "cliente",
              "msg_type": "text", "ts": "2026-08-19 13:00:00"},
         ]}
    # R4: frase prohibida, modo cod
    c4 = {"user_ns": "fR4", "get_info": {},
         "mensajes": [
             {"content": "para procesar tu pedido necesitas hacer un pago anticipado",
              "direction": "empresa", "msg_type": "text", "ts": "2026-08-19 15:01:00"},
             {"content": "hola quiero el producto", "direction": "cliente", "msg_type": "text",
              "ts": "2026-08-19 15:00:00"},
         ]}
    # Q4: pregunta sin cobertura
    c5 = {"user_ns": "fQ4", "get_info": {},
         "mensajes": [
             {"content": "no entendi tu mensaje", "direction": "empresa", "msg_type": "text",
              "ts": "2026-08-19 16:01:00"},
             {"content": "que garantia tiene el producto si llega defectuoso?",
              "direction": "cliente", "msg_type": "text", "ts": "2026-08-19 16:00:00"},
         ]}

    c = Clasificador({"contactos": [c1, c2, c3, c4, c5]}, modo="cod").correr()
    controles = {h["control"] for h in c.hallazgos}
    marcar("R1", "R1" in controles, "sin respuesta detectado")
    marcar("R2", "R2" in controles, "respuesta tardia detectada")
    marcar("R3", "R3" in controles, "bucle detectado")
    r4_severidad = next((h["severidad"] for h in c.hallazgos if h["control"] == "R4"), None)
    marcar("R4", r4_severidad == "MUERTO",
          f"frase prohibida detectada con severidad {r4_severidad} (modo cod -> debe ser MUERTO)")
    marcar("Q4", "Q4" in controles, "pregunta sin cobertura detectada")


# ============================================================================
# Controles agregados tras la verificacion adversarial de golden-verificador
# (2026-08-20). Cada uno prueba, con un caso que se SABE roto, un defecto real
# que el verificador encontro en la primera version. No se retira ninguno de
# los de arriba: estos se SUMAN.
# ============================================================================

def test_campo_type_real():
    """Verificador #1: la forma REAL del payload usa `type` con valores in/out/note,
    medida contra produccion (golden-logistica-diaria). Si el clasificador solo supiera
    leer `direction`/`msg_type` para la nota, esta prueba falla."""
    contacto = {"user_ns": "freal", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "hola, cuanto cuesta?",
                    "ts": "2026-08-19 18:00:00"},
                   {"type": "note", "content": "PageView pixel event",
                    "ts": "2026-08-19 18:00:05"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    conv = c.conversaciones[0]
    nota_excluida = conv["n_mensajes_privados"] == 1
    quien_correcto = conv["quien_hablo_ultimo"] == "cliente"
    r1_dispara = any(h["control"] == "R1" for h in c.hallazgos)
    paso = nota_excluida and quien_correcto and r1_dispara
    marcar("TYPE-REAL", paso,
          f"con type=in/out/note real: nota excluida={nota_excluida}, "
          f"quien_hablo_ultimo={conv['quien_hablo_ultimo']} (debe ser cliente), "
          f"R1 disparado={r1_dispara}. Sin esto la nota sobrevive y la señal mas cara "
          "del informe (quien hablo de ultimo) queda invertida.")


def test_desconocidos_se_declaran():
    """Verificador #2: un mensaje con direccion no reconocida generaba silencio total.
    Ahora debe producir un hallazgo P-desconocidos."""
    contacto = {"user_ns": "fdesc", "get_info": {},
               "mensajes": [
                   {"campo_raro": "algo", "content": "mensaje ilegible", "ts":
                    "2026-08-19 09:00:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    conv = c.conversaciones[0]
    disparo = any(h["control"] == "P-desconocidos" for h in c.hallazgos)
    paso = conv["n_desconocidos"] == 1 and disparo
    marcar("DESCONOCIDOS", paso,
          f"n_desconocidos={conv['n_desconocidos']} · hallazgo disparado: {disparo}")


def test_compuerta_no_imprime_hallazgos():
    """Verificador #4: la compuerta activada NO puede imprimir el informe completo
    (evidencia citada) antes de abortar."""
    def contacto_cierre(n):
        return {"user_ns": f"c{n}", "get_info": {},
               "mensajes": [{"type": "in", "content": "MENSAJE_SECRETO_DE_PRUEBA",
                            "ts": "2026-08-19 09:00:00"},
                           {"type": "out", "content": "pedido confirmado, gracias por "
                            "tu compra", "ts": "2026-08-19 09:01:00"}]}
    dia_roto = [contacto_cierre(i) for i in range(19)] + [
        {"user_ns": "abierto", "get_info": {},
         "mensajes": [{"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00"}]}]
    c = Clasificador({"contactos": dia_roto}).correr()
    buf = io.StringIO()
    with redirect_stdout(buf):
        imprimir(c)
    salida = buf.getvalue()
    no_filtro_evidencia = "MENSAJE_SECRETO_DE_PRUEBA" not in salida
    avisa_aborto = "COMPUERTA DE CORDURA ACTIVADA" in salida
    paso = c.abortado() and no_filtro_evidencia and avisa_aborto
    marcar("COMPUERTA-SILENCIA", paso,
          f"abortado={c.abortado()} · evidencia NO impresa: {no_filtro_evidencia} · "
          f"avisa el aborto: {avisa_aborto}")


def test_dropi_excluido_de_pct():
    """Verificador #5: los contactos dropi deben quedar FUERA del calculo de
    cierra_con_cliente_pct, no solo listados en excluidos_dropi."""
    def cierre_dropi(n):
        return {"user_ns": f"d{n}", "get_info": {"data": {"opted_in_through": "dropi"}},
               "mensajes": [{"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00"},
                           {"type": "out", "content": "pedido confirmado, gracias por "
                            "tu compra", "ts": "2026-08-19 09:01:00"}]}

    def abierto_real(n):
        return {"user_ns": f"r{n}", "get_info": {},
               "mensajes": [{"type": "out", "content": "hola, en que te ayudo",
                            "ts": "2026-08-19 09:00:00"},
                           {"type": "in", "content": "cuanto cuesta",
                            "ts": "2026-08-19 09:05:00"}]}
    # 10 dropi que "cierran" + 10 reales de los que solo 1 cierra: si dropi se colara
    # en el denominador, el pct publicado seria ~0.55 en vez de ~0.10.
    contactos = [cierre_dropi(i) for i in range(10)] + [abierto_real(i) for i in range(10)]
    c = Clasificador({"contactos": contactos}).correr()
    pct = c.universo["cierra_con_cliente_pct"]
    base = c.universo["cierra_con_cliente_base"]
    paso = base == 10 and pct == 0.0
    marcar("DROPI-EXCLUIDO-PCT", paso,
          f"base={base} (debe ser 10, sin los 10 dropi) · pct={pct} (debe ser 0.0, "
          "ninguno de los 10 reales cerro)")


def test_modo_invalido():
    """Verificador #10: '--modo COD' en mayusculas u otro valor no valido debe
    normalizarse o rechazarse explicitamente, nunca degradar en silencio."""
    try:
        Clasificador({"contactos": []}, modo="COD")
        normalizado_ok = True   # 'COD' se acepto porque se normaliza a minuscula
    except ValueError:
        normalizado_ok = False
    invalido_rechazado = False
    try:
        Clasificador({"contactos": []}, modo="contraentrega")
    except ValueError:
        invalido_rechazado = True
    paso = normalizado_ok and invalido_rechazado
    marcar("MODO-INVALIDO", paso,
          f"'COD' (mayusculas) se normaliza: {normalizado_ok} · 'contraentrega' se "
          f"rechaza con ValueError: {invalido_rechazado}")


def test_bucle_no_falso_positivo():
    """Verificador #8: 3 respuestas cortas IDENTICAS del bot a 3 preguntas DISTINTAS
    del cliente, con el cliente escribiendo entre cada una, NO es un bucle."""
    contacto = {"user_ns": "fnobucle", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "tienen color rojo", "ts": "2026-08-19 10:00:00"},
                   {"type": "out", "content": "Claro que si", "ts": "2026-08-19 10:00:30"},
                   {"type": "in", "content": "y talla grande", "ts": "2026-08-19 10:01:00"},
                   {"type": "out", "content": "Claro que si", "ts": "2026-08-19 10:01:30"},
                   {"type": "in", "content": "y llega manana", "ts": "2026-08-19 10:02:00"},
                   {"type": "out", "content": "Claro que si", "ts": "2026-08-19 10:02:30"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    disparo = any(h["control"] == "R3" for h in c.hallazgos)
    marcar("BUCLE-FALSO-POSITIVO", not disparo,
          f"R3 disparado: {disparo} (debe ser False -- el cliente respondio entre cada "
          "una de las tres respuestas identicas, no es un bucle)")


def test_q4_no_falso_positivo_substring():
    """Verificador #7: 'ya me llego el paquete, todo bien' NO debe marcarse como
    pregunta sin cobertura solo porque 'paquete' contiene la subcadena 'que'."""
    contacto = {"user_ns": "fq4falso", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "ya me llego el paquete, todo bien",
                    "ts": "2026-08-19 11:00:00"},
                   {"type": "out", "content": "Que bueno! Cualquier cosa me avisas",
                    "ts": "2026-08-19 11:01:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    disparo = any(h["control"] == "Q4" for h in c.hallazgos)
    marcar("Q4-FALSO-POSITIVO", not disparo,
          f"Q4 disparado: {disparo} (debe ser False -- 'paquete' no es la palabra 'que', "
          "y el mensaje del cliente no es una pregunta)")


def test_inventario_incompleto_aborta():
    """SKILL.md Fase 1: si el denominador declarado no cuadra con lo traido, el
    informe se detiene -- no se clasifica a medias."""
    dump = {"_conteos": {"contactos_del_dia": {"traidos": 8, "declarados_por_servidor": 12}},
           "contactos": [{"user_ns": "x", "get_info": {},
                          "mensajes": [{"type": "in", "content": "hola",
                                       "ts": "2026-08-19 09:00:00"}]}]}
    c = Clasificador(dump).correr()
    disparo = any(h["control"] == "INV" for h in c.hallazgos)
    paso = c.universo["denominador_incompleto"] is True and c.abortado() and disparo
    marcar("INVENTARIO-ABORTA", paso,
          f"denominador_incompleto={c.universo.get('denominador_incompleto')} · "
          f"abortado={c.abortado()} · hallazgo INV disparado: {disparo}")


def test_credenciales_ampliadas_en_evidencia():
    """Ronda 2 de verificacion adversarial: no basta con parchar el string que se
    nombro (sk_live_, APP_USR-, un Sanctum largo) -- se prueba la FAMILIA completa de
    cada proveedor, y se prueba a traves del CAMINO REAL de un hallazgo (`falla()`,
    via `Clasificador`), no llamando a `redactar_texto` suelto: ese fue exactamente el
    defecto que la mutacion encontro la vez pasada ("la prueba prueba la funcion, no
    el camino del entregable")."""
    casos = {
        "sk_live_" + "A" * 24: "StripeLive",
        "sk_test_" + "A" * 24: "StripeTest",
        "whsec_" + "A" * 20: "StripeWebhook",
        "APP_USR-1234567890123456-081020-abcdef1234567890abcdef1234567890-123456789":
            "MercadoPagoLive",
        "TEST-1234567890123456-081020-abcdef1234567890abcdef1234567890-123456789":
            "MercadoPagoTest",
        "12345|" + "a" * 40: "SanctumLargo",
        "7|" + "b" * 25: "SanctumCorto",
        "ghp_" + "c" * 36: "GitHubPAT",
        "github_pat_" + "d" * 60: "GitHubFineGrained",
        "AKIA" + "E" * 16: "AWSAccessKey",
        "xoxb-" + "1" * 20: "SlackToken",
        "SG." + "f" * 20 + "." + "g" * 20: "SendGrid",
        "1//0" + "h" * 30: "GoogleOAuthRefresh",
        "sk-ant-" + "i" * 30: "AnthropicComoOpenAI",
        "a" * 64: "HexBearerGenerico",
    }
    fallos_directos = []
    for secreto, etiqueta in casos.items():
        redactado = redactar_texto(f"el cliente escribio su token {secreto} por error")
        if secreto in redactado:
            fallos_directos.append(etiqueta)

    # Y por el CAMINO REAL: el secreto sembrado dentro del contenido de un mensaje que
    # termina citado como evidencia de un hallazgo (R4, via _frases_prohibidas).
    secreto_camino = "sk_live_" + "Z" * 24
    contacto = {"user_ns": "fcamino", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "hola quiero el producto",
                    "ts": "2026-08-19 15:00:00"},
                   {"type": "out", "content": f"necesitas pago anticipado, mi token "
                    f"interno es {secreto_camino}", "ts": "2026-08-19 15:01:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    r4 = next((h for h in c.hallazgos if h["control"] == "R4"), None)
    fuga_en_hallazgo = r4 is not None and secreto_camino in r4["evidencia"]

    # Y en la atribucion del --json (el unico dato que no pasa por falla()).
    secreto_referral = "sk_live_" + "Y" * 24
    contacto2 = {"user_ns": "fatrib", "get_info": {},
                "mensajes": [
                    {"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00",
                     "payload": {"referral": {"source_id": "1",
                                              "headline": f"promo {secreto_referral}"}}},
                ]}
    c2 = Clasificador({"contactos": [contacto2]}).correr()
    atribucion = c2.conversaciones[0]["atribucion"]
    fuga_en_atribucion = atribucion is not None and secreto_referral in json.dumps(atribucion)

    paso = not fallos_directos and not fuga_en_hallazgo and not fuga_en_atribucion
    marcar("CREDENCIALES-AMPLIADAS", paso,
          f"familias sin redactar: {fallos_directos or 'ninguna'} · fuga en hallazgo R4: "
          f"{fuga_en_hallazgo} · fuga en atribucion del --json: {fuga_en_atribucion}")


# ------------------------------------------------- controles de la segunda verificacion
def test_dropi_normalizado():
    """Ronda 2: 'Dropi'/'DROPI'/' dropi ' deben excluirse igual que 'dropi'."""
    def contacto(n, valor):
        return {"user_ns": f"nd{n}", "get_info": {"data": {"opted_in_through": valor}},
               "mensajes": [{"type": "in", "content": "hola",
                            "ts": "2026-08-19 09:00:00"}]}
    variantes = ["dropi", "Dropi", "DROPI", " dropi "]
    c = Clasificador({"contactos": [contacto(i, v) for i, v in enumerate(variantes)]}).correr()
    paso = len(c.excluidos_dropi) == len(variantes)
    marcar("DROPI-NORMALIZADO", paso,
          f"variantes probadas: {variantes} · excluidas: {len(c.excluidos_dropi)} de "
          f"{len(variantes)} (deben ser todas)")


def test_ts_ilegible_no_engana_al_orden():
    """Ronda 2: un ts PRESENTE pero que parse_fecha no puede leer (epoch numerico, por
    ejemplo) debe tratarse como 'no parseable' -> se invierte la lista completa, igual
    que si faltara -- nunca un sort() estable que deja todo tal cual llego."""
    crudo = [
        {"type": "out", "content": "ULTIMO_BOT", "ts": 1755000300},
        {"type": "in", "content": "MEDIO_CLIENTE", "ts": 1755000200},
        {"type": "in", "content": "PRIMERO_CLIENTE", "ts": 1755000100},
    ]
    hilo = invertir_hilo(crudo)
    # Con ts epoch ilegible por parse_fecha, se espera la lista INVERTIDA tal cual
    # llego (comportamiento P4), no el orden original ni un intento de ordenar por el
    # epoch crudo.
    esperado = list(reversed(crudo))
    paso = hilo == esperado
    marcar("TS-ILEGIBLE", paso,
          f"orden obtenido: {[m['content'] for m in hilo]} (se espera "
          f"{[m['content'] for m in esperado]} -- invertido, no ordenado por el epoch "
          "crudo ni dejado tal cual)")


def test_corte_del_dia_ignora_notas():
    """Ronda 2: una nota de pixel disparada horas despues del ultimo mensaje real NO
    puede correr el corte del dia ni subir a MUERTO un R1 que en realidad esperaba
    poco tiempo."""
    def dump_con(incluir_nota):
        msgs = [
            {"type": "in", "content": "hola, cuanto cuesta", "ts": "2026-08-19 10:00:00"},
        ]
        if incluir_nota:
            msgs.append({"type": "note", "content": "PageView",
                        "ts": "2026-08-20 02:00:00"})   # 16h despues
        return {"contactos": [{"user_ns": "fcorte", "get_info": {}, "mensajes": msgs}]}

    c_sin_nota = Clasificador(dump_con(False)).correr()
    c_con_nota = Clasificador(dump_con(True)).correr()
    sev_sin = next((h["severidad"] for h in c_sin_nota.hallazgos if h["control"] == "R1"), None)
    sev_con = next((h["severidad"] for h in c_con_nota.hallazgos if h["control"] == "R1"), None)
    # Sin corte de dia (un solo mensaje, sin mas ts), el gap no es medible -> RIESGO.
    # Si la nota corriera el corte, pasaria a MUERTO (16h de gap medido) -- eso es el bug.
    paso = sev_sin == sev_con
    marcar("CORTE-IGNORA-NOTAS", paso,
          f"severidad de R1 sin nota: {sev_sin} · con nota 16h despues: {sev_con} "
          "(deben ser IGUALES -- la nota no puede cambiar el corte del dia)")


def test_denominador_tres_estados():
    """Ronda 2: 'no medible' (falta _conteos, o declarados_por_servidor no es int) es
    un TERCER estado, distinto de 'cuadra'. Antes se leia como 'cuadra' en silencio."""
    base_contacto = {"user_ns": "x", "get_info": {},
                     "mensajes": [{"type": "in", "content": "hola",
                                  "ts": "2026-08-19 09:00:00"}]}
    casos = {
        "sin _conteos": {"contactos": [base_contacto]},
        "declarados None": {"_conteos": {"contactos_del_dia": {"traidos": 1,
                                         "declarados_por_servidor": None}},
                            "contactos": [base_contacto]},
        "declarados string": {"_conteos": {"contactos_del_dia": {"traidos": 1,
                                           "declarados_por_servidor": "1"}},
                              "contactos": [base_contacto]},
    }
    fallos = []
    for nombre, dump in casos.items():
        c = Clasificador(dump).correr()
        estado = c.universo.get("denominador_fase1")
        if estado != "no_medible" or c.universo.get("denominador_incompleto") is not False:
            fallos.append(f"{nombre} -> denominador_fase1={estado}")
    paso = not fallos
    marcar("DENOMINADOR-3-ESTADOS", paso,
          f"casos que NO dieron 'no_medible' (deberian): "
          f"{fallos or 'ninguno -- los 3 casos declararon no_medible sin decir cuadra'}")


def test_plantilla_forma_no_borra_objecion_real():
    """Ronda 2: 3 clientes que escriben la MISMA objecion real de precio como primer
    mensaje ('esta muy caro') NO deben clasificarse como plantilla del anuncio -- les
    falta la condicion de FORMA (abrir con '¡'), que es la que distingue un boton de
    Meta de una coincidencia real."""
    def contacto(n):
        return {"user_ns": f"car{n}", "get_info": {},
               "mensajes": [{"type": "in", "content": "esta muy caro",
                            "ts": f"2026-08-19 10:0{n}:00"}]}
    c = Clasificador({"contactos": [contacto(i) for i in range(3)]}).correr()
    motivos = [conv["motivo_no_compra"] for conv in c.conversaciones]
    paso = all(m == ["precio"] for m in motivos)
    marcar("PLANTILLA-NO-BORRA-OBJECION", paso,
          f"motivo_no_compra por contacto: {motivos} (los 3 deben decir ['precio'] -- "
          "'esta muy caro' no empieza con '¡', no es plantilla aunque se repita)")


def test_plantilla_universo_chico_declarado():
    """Ronda 2: con menos de MIN_PERSONAS_FORMA contactos, el punto ciego del criterio
    de frecuencia debe quedar DECLARADO (hallazgo P6 DUDA), no silencioso."""
    contacto = {"user_ns": "fchico", "get_info": {},
               "mensajes": [{"type": "in", "content": "Hola quiero info",
                            "ts": "2026-08-19 09:00:00"}]}
    c = Clasificador({"contactos": [contacto]}).correr()
    disparo = any(h["control"] == "P6" and h["severidad"] == "DUDA" for h in c.hallazgos)
    marcar("PLANTILLA-CHICO-DECLARADO", disparo,
          f"con {MIN_PERSONAS_FORMA - 2} contacto(s), hallazgo P6/DUDA de universo chico "
          f"disparado: {disparo}")


def test_parse_dinero_rechaza_no_str():
    """Ronda 2: un float/int no se adivina -- '74900.0' como float NO dice si el monto
    real era 74.900 (miles) o 74900,0 (decimal con un digito). Se declara
    tipo_no_soportado en vez de multiplicar por 10 en silencio."""
    monto, formato = parse_dinero(74900.0)
    paso = monto is None and formato == "tipo_no_soportado"
    marcar("DINERO-RECHAZA-NO-STR", paso,
          f"parse_dinero(74900.0) -> ({monto}, {formato!r}) (debe ser (None, "
          "'tipo_no_soportado'), nunca 749000.0)")


def test_main_args_orden_independiente():
    """Ronda 2: '--modo cod archivo.json' y 'archivo.json --modo cod' deben dar el
    mismo resultado. Antes, el primer orden rompia con FileNotFoundError('--modo')."""
    r1 = _parsear_argv(["--modo", "cod", "archivo.json"])
    r2 = _parsear_argv(["archivo.json", "--modo", "cod"])
    paso = r1 == r2 == ("archivo.json", "cod", None)
    marcar("MAIN-ARGS-ORDEN", paso, f"orden 1: {r1} · orden 2: {r2} (deben ser iguales)")


TRAMPAS_DEL_ENCARGO = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11",
                      "P12", "P13"]
EXTRA_CALIDAD = ["R1", "R2", "R3", "R4", "Q4"]
FIXES_ADVERSARIALES = ["TYPE-REAL", "DESCONOCIDOS", "COMPUERTA-SILENCIA",
                       "DROPI-EXCLUIDO-PCT", "MODO-INVALIDO", "BUCLE-FALSO-POSITIVO",
                       "Q4-FALSO-POSITIVO", "INVENTARIO-ABORTA", "CREDENCIALES-AMPLIADAS"]
FIXES_RONDA_2 = ["DROPI-NORMALIZADO", "TS-ILEGIBLE", "CORTE-IGNORA-NOTAS",
                "DENOMINADOR-3-ESTADOS", "PLANTILLA-NO-BORRA-OBJECION",
                "PLANTILLA-CHICO-DECLARADO", "DINERO-RECHAZA-NO-STR", "MAIN-ARGS-ORDEN"]


def main():
    print("AUTOPRUEBA · fabricando un dia que se SABE roto (13 trampas del encargo)\n")

    test_p2()
    test_p3_p4()
    test_p5()
    test_p6_p7()
    test_p8()
    test_p9()
    test_p10()
    test_p11()
    test_p12()
    test_p13()
    test_p1()
    test_calidad()

    test_campo_type_real()
    test_desconocidos_se_declaran()
    test_compuerta_no_imprime_hallazgos()
    test_dropi_excluido_de_pct()
    test_modo_invalido()
    test_bucle_no_falso_positivo()
    test_q4_no_falso_positivo_substring()
    test_inventario_incompleto_aborta()
    test_credenciales_ampliadas_en_evidencia()

    test_dropi_normalizado()
    test_ts_ilegible_no_engana_al_orden()
    test_corte_del_dia_ignora_notas()
    test_denominador_tres_estados()
    test_plantilla_forma_no_borra_objecion_real()
    test_plantilla_universo_chico_declarado()
    test_parse_dinero_rechaza_no_str()
    test_main_args_orden_independiente()

    print("Las 13 trampas del encargo (ENCARGO-golden-chatea-operacion.md):")
    fallidas = []
    for codigo in TRAMPAS_DEL_ENCARGO:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:4} {detalle}")
        if not paso:
            fallidas.append(codigo)

    print(f"\n  {len(TRAMPAS_DEL_ENCARGO) - len(fallidas)} de {len(TRAMPAS_DEL_ENCARGO)} "
          f"trampas del encargo detectadas")

    print("\nControles complementarios de calidad de respuesta (no forman parte de las 13 "
         "trampas de parseo, pero se prueban porque son el corazon de la skill):")
    fallidas_extra = []
    for codigo in EXTRA_CALIDAD:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:4} {detalle}")
        if not paso:
            fallidas_extra.append(codigo)

    print("\nControles agregados tras la verificacion adversarial de golden-verificador "
         "(2026-08-20) -- cada uno reproduce un defecto real que encontro:")
    fallidas_fixes = []
    for codigo in FIXES_ADVERSARIALES:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:20} {detalle}")
        if not paso:
            fallidas_fixes.append(codigo)

    print("\nControles agregados tras la SEGUNDA verificacion adversarial (17 hallazgos, "
         "misma fecha) -- cada uno reproduce un defecto real de esa ronda:")
    fallidas_ronda2 = []
    for codigo in FIXES_RONDA_2:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:26} {detalle}")
        if not paso:
            fallidas_ronda2.append(codigo)

    if fallidas or fallidas_extra or fallidas_fixes or fallidas_ronda2:
        print(f"\nAUTOPRUEBA FALLIDA. Trampas del encargo sin detectar: {fallidas or 'ninguna'}. "
             f"Controles de calidad sin detectar: {fallidas_extra or 'ninguno'}. "
             f"Fixes adversariales (ronda 1) sin confirmar: {fallidas_fixes or 'ninguno'}. "
             f"Fixes (ronda 2) sin confirmar: {fallidas_ronda2 or 'ninguno'}.")
        print("El clasificador esta roto. No se corre contra un DUMP real hasta arreglarlo.")
        return 1

    total_controles = (len(TRAMPAS_DEL_ENCARGO) + len(EXTRA_CALIDAD) +
                       len(FIXES_ADVERSARIALES) + len(FIXES_RONDA_2))
    print(f"\n  {total_controles} de {total_controles} controles confirmados en total "
         f"({len(TRAMPAS_DEL_ENCARGO)} trampas del encargo + {len(EXTRA_CALIDAD)} calidad + "
         f"{len(FIXES_ADVERSARIALES)} fixes ronda 1 + {len(FIXES_RONDA_2)} fixes ronda 2)")
    print("\nAutoprueba pasada. Esto valida el DETECTOR contra casos que se SABEN rotos, no "
         "valida ningun dia real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
