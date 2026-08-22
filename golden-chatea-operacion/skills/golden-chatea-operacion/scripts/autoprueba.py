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
    extraer_atributos, es_resumen_final_r6,
)
from secretos import PATRONES_SECRETO, redactar_texto as redactar_texto_compartida  # noqa: E402
import extraer as _extraer_modulo                                 # noqa: E402

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
        {"content": "c3 (mas nuevo)", "type": "in", "ts": "2026-08-19 10:03:00"},
        {"content": "c1 (mas viejo)", "type": "in", "ts": "2026-08-19 10:01:00"},
        {"content": "c2 (medio)", "type": "out", "ts": "2026-08-19 10:02:00"},
    ]
    resultado = invertir_hilo(crudo)
    orden_ok = [m["content"] for m in resultado] == ["c1 (mas viejo)", "c2 (medio)",
                                                      "c3 (mas nuevo)"]
    marcar("P3", orden_ok, f"orden obtenido: {[m['content'] for m in resultado]}")

    # P4: TODOS los ts en None. El servidor entrega reciente->viejo (raw[0] es el mas nuevo).
    raw_reciente_a_viejo = [
        {"content": "el mas nuevo", "type": "out", "ts": None},
        {"content": "medio", "type": "in", "ts": None},
        {"content": "el mas viejo", "type": "in", "ts": None},
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
    audio_con_texto = {"content": "", "type": "in", "msg_type": "audio",
                       "ts": "2026-08-19 11:00:00",
                       "payload": {"transcribed_text": "hola quiero saber el precio"}}
    audio_sin_texto = {"content": "", "type": "in", "msg_type": "audio",
                       "ts": "2026-08-19 11:05:00"}
    comentario_feed = {"content": "que bonito producto", "type": "in",
                       "msg_type": "feed", "ts": "2026-08-19 11:10:00"}
    saludo_empresa = {"content": "hola, en que te ayudo", "type": "out",
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
         "mensajes": [{"content": "hola", "type": "in", "msg_type": "text",
                      "ts": "2026-08-19 08:00:00"}]},
        {"user_ns": "f1normal", "get_info": {"data": {"opted_in_through": "chat"}},
         "mensajes": [{"content": "hola", "type": "in", "msg_type": "text",
                      "ts": "2026-08-19 08:00:00"},
                     {"content": "hola, en que te ayudo", "type": "out",
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
                   {"content": "quiero comprarlo", "type": "in", "msg_type": "text",
                    "ts": "2026-08-19 09:00:00"},
                   {"content": "listo, pedido confirmado, gracias por tu compra",
                    "type": "out", "msg_type": "text", "ts": "2026-08-19 09:01:00"},
               ]}

    def contacto_abierto(n):
        return {"user_ns": f"abierto{n}", "get_info": {},
               "mensajes": [
                   {"content": "hola, en que te ayudo", "type": "out",
                    "msg_type": "text", "ts": "2026-08-19 09:00:00"},
                   {"content": "cuanto cuesta el envio a mi ciudad", "type": "in",
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
                   {"content": "hola", "type": "in", "msg_type": "text",
                    "ts": "2026-08-19 08:00:00"},
                   {"content": "estoy interesado", "type": "in", "msg_type": "text",
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
         "mensajes": [{"content": "hola, cuanto cuesta?", "type": "in",
                      "msg_type": "text", "ts": "2026-08-19 14:00:00"}]}
    # R2: respuesta tardia (61 min de verdad entre el mensaje del cliente y la respuesta)
    c2 = {"user_ns": "fR2", "get_info": {},
         "mensajes": [
             {"content": "cuanto cuesta", "type": "in", "msg_type": "text",
              "ts": "2026-08-19 12:00:00"},
             {"content": "disculpa la demora, cuesta 74900", "type": "out",
              "msg_type": "text", "ts": "2026-08-19 13:01:00"},
         ]}
    # R3: bucle (3 iguales seguidas)
    c3 = {"user_ns": "fR3", "get_info": {},
         "mensajes": [
             {"content": "no entendi, puedes reformular?", "type": "out",
              "msg_type": "text", "ts": "2026-08-19 13:03:00"},
             {"content": "no entendi, puedes reformular?", "type": "out",
              "msg_type": "text", "ts": "2026-08-19 13:02:00"},
             {"content": "no entendi, puedes reformular?", "type": "out",
              "msg_type": "text", "ts": "2026-08-19 13:01:00"},
             {"content": "hola necesito ayuda con mi pedido", "type": "in",
              "msg_type": "text", "ts": "2026-08-19 13:00:00"},
         ]}
    # R4: frase prohibida, modo cod
    c4 = {"user_ns": "fR4", "get_info": {},
         "mensajes": [
             {"content": "para procesar tu pedido necesitas hacer un pago anticipado",
              "type": "out", "msg_type": "text", "ts": "2026-08-19 15:01:00"},
             {"content": "hola quiero el producto", "type": "in", "msg_type": "text",
              "ts": "2026-08-19 15:00:00"},
         ]}
    # Q4: pregunta sin cobertura
    c5 = {"user_ns": "fQ4", "get_info": {},
         "mensajes": [
             {"content": "no entendi tu mensaje", "type": "out", "msg_type": "text",
              "ts": "2026-08-19 16:01:00"},
             {"content": "que garantia tiene el producto si llega defectuoso?",
              "type": "in", "msg_type": "text", "ts": "2026-08-19 16:00:00"},
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


def test_ts_epoch_ordena_correctamente():
    """F1 (CRITICO, golden-verificador 2026-08-22): ANTES de este fix, `parse_fecha` no leia
    epoch -- un `ts` epoch (la forma REAL de los 4 DUMPs de produccion medidos, 100% de los
    mensajes de LIBIDO-UP) se trataba como 'no parseable' y esta prueba (entonces llamada
    TS-ILEGIBLE) EXIGIA que se comportara asi. Ahora que `parse_fecha` SI lee epoch, la
    expectativa se invierte: con epoch parseable, `invertir_hilo` debe ORDENAR
    cronologicamente (rama TODO-parseable de P4), no limitarse a invertir la lista cruda.
    Server entrega mas-reciente-primero (descendente); se mezcla el orden crudo a proposito
    para confirmar que se ORDENA, no que casualmente coincide con invertir."""
    crudo = [
        {"type": "out", "content": "ULTIMO_BOT", "ts": 1755000300},
        {"type": "in", "content": "PRIMERO_CLIENTE", "ts": 1755000100},   # fuera de orden
        {"type": "in", "content": "MEDIO_CLIENTE", "ts": 1755000200},
    ]
    hilo = invertir_hilo(crudo)
    orden_obtenido = [m["content"] for m in hilo]
    paso = orden_obtenido == ["PRIMERO_CLIENTE", "MEDIO_CLIENTE", "ULTIMO_BOT"]
    marcar("TS-EPOCH-ORDENA", paso,
          f"orden obtenido: {orden_obtenido} (se espera "
          "['PRIMERO_CLIENTE', 'MEDIO_CLIENTE', 'ULTIMO_BOT'] -- ORDENADO por el epoch "
          "parseado, no invertido a ciegas ni dejado en el orden crudo desordenado que "
          "trae este fixture a proposito)")


def test_ts_no_numerico_sigue_ilegible():
    """F1: un `ts` que NO es epoch ni fecha valida (texto arbitrario) debe seguir tratandose
    como no parseable -> P4 (fallback: invertir la lista cruda tal cual). Confirma que el fix
    de F1 amplio lo que se ACEPTA como fecha, sin ampliar de mas lo que se acepta como tal."""
    crudo = [
        {"type": "out", "content": "ULTIMO_BOT", "ts": "no-es-una-fecha"},
        {"type": "in", "content": "MEDIO_CLIENTE", "ts": "tampoco"},
        {"type": "in", "content": "PRIMERO_CLIENTE", "ts": ""},
    ]
    hilo = invertir_hilo(crudo)
    esperado = list(reversed(crudo))
    paso = hilo == esperado
    marcar("TS-NO-NUMERICO-ILEGIBLE", paso,
          f"orden obtenido: {[m['content'] for m in hilo]} (se espera "
          f"{[m['content'] for m in esperado]} -- invertido tal cual, un ts basura sigue "
          "siendo no parseable)")


def test_ts_epoch_milisegundos_se_detecta():
    """F1: un epoch en MILISEGUNDOS (13 digitos, ~1000x el valor en segundos de la misma
    fecha) debe detectarse por MAGNITUD y dar la MISMA fecha que su equivalente en segundos
    -- no una fecha en el año 58000 por dividir de mas, ni una fecha en 1970 por no dividir."""
    segundos = 1755000200
    milisegundos = segundos * 1000
    d_seg = parse_fecha(segundos)
    d_ms = parse_fecha(milisegundos)
    paso = d_seg is not None and d_ms is not None and d_seg == d_ms
    marcar("TS-EPOCH-MS-DETECTADO", paso,
          f"parse_fecha({segundos}) = {d_seg} · parse_fecha({milisegundos}) = {d_ms} "
          "(deben dar la MISMA fecha -- la magnitud del numero, no un flag aparte, decide "
          "si son segundos o milisegundos)")


def test_ts_epoch_como_cadena_se_parsea():
    """F1: el mismo epoch, pero serializado como CADENA de digitos ('1787114990' en vez de
    1787114990), tambien debe parsearse -- algunos DUMPs/JSON lo entregan asi."""
    d_int = parse_fecha(1787114990)
    d_str = parse_fecha("1787114990")
    paso = d_int is not None and d_str is not None and d_int == d_str
    marcar("TS-EPOCH-CADENA", paso,
          f"parse_fecha(1787114990) = {d_int} · parse_fecha('1787114990') = {d_str} "
          "(deben coincidir -- epoch como int o como cadena numerica es la misma fecha)")


def test_r1_r2_r3_con_ts_epoch_real():
    """F1: R1 (sin respuesta, con gap MEDIBLE), R2 (respuesta tardia) y R3 (bucle) deben
    funcionar con `ts` en formato epoch real -- exactamente la forma de los 4 DUMPs de
    produccion (LIBIDO-UP, 2026-08-21). Ambos epoch tomados de un rango real de esos DUMPs.
    ANTES del fix de F1, ninguno de los tres disparaba con epoch: R1 caia siempre en RIESGO
    por 'gap no medible', R2 nunca calculaba el gap (ambos ts deben parsear), R3 no dependia
    de fechas pero se agrega aqui para dejar los tres juntos, con la forma real del DUMP."""
    epoch_base = 1787114980
    # R1: cliente pregunta y nadie responde, corte del dia 3 horas (10800s) despues ->
    # gap medible y >= 120 min -> debe ser MUERTO, no RIESGO.
    c_r1 = {"user_ns": "fepoch-r1", "get_info": {},
           "mensajes": [{"type": "in", "content": "cuanto cuesta?",
                        "ts": epoch_base}]}
    c_ancla_corte = {"user_ns": "fepoch-ancla", "get_info": {},
                     "mensajes": [{"type": "out", "content": "ancla del corte del dia",
                                  "ts": epoch_base + 10800}]}
    # R2: respuesta tardia, 61 minutos (3660s) despues, con epoch real.
    c_r2 = {"user_ns": "fepoch-r2", "get_info": {},
           "mensajes": [
               {"type": "in", "content": "cuanto cuesta", "ts": epoch_base},
               {"type": "out", "content": "disculpa la demora, cuesta 74900",
                "ts": epoch_base + 3660},
           ]}
    # R3: bucle, 3 respuestas identicas seguidas con epoch creciente.
    c_r3 = {"user_ns": "fepoch-r3", "get_info": {},
           "mensajes": [
               {"type": "in", "content": "hola necesito ayuda", "ts": epoch_base},
               {"type": "out", "content": "no entendi, puedes reformular?",
                "ts": epoch_base + 60},
               {"type": "out", "content": "no entendi, puedes reformular?",
                "ts": epoch_base + 120},
               {"type": "out", "content": "no entendi, puedes reformular?",
                "ts": epoch_base + 180},
           ]}
    c = Clasificador({"contactos": [c_r1, c_ancla_corte, c_r2, c_r3]}, modo="cod").correr()
    r1 = next((h for h in c.hallazgos
              if h["control"] == "R1" and "fepoch-r1" in h["titulo"]), None)
    r2 = next((h for h in c.hallazgos
              if h["control"] == "R2" and "fepoch-r2" in h["titulo"]), None)
    r3 = next((h for h in c.hallazgos
              if h["control"] == "R3" and "fepoch-r3" in h["titulo"]), None)
    r1_es_muerto = r1 is not None and r1["severidad"] == "MUERTO"
    paso = r1_es_muerto and r2 is not None and r3 is not None
    marcar("EPOCH-R1-R2-R3-REALES", paso,
          f"R1 con gap medible por epoch, severidad {r1['severidad'] if r1 else None} "
          "(debe ser MUERTO, no RIESGO -- antes de F1 SIEMPRE caia en RIESGO con epoch) · "
          f"R2 disparado: {r2 is not None} (antes de F1 nunca disparaba con epoch) · "
          f"R3 disparado: {r3 is not None}")


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
    mismo resultado. Antes, el primer orden rompia con FileNotFoundError('--modo').
    Ronda 3 agrega '--zona-horas' (4-tupla en vez de 3, con zona_horas=None por default
    cuando no se declara)."""
    r1 = _parsear_argv(["--modo", "cod", "archivo.json"])
    r2 = _parsear_argv(["archivo.json", "--modo", "cod"])
    r3 = _parsear_argv(["archivo.json", "--modo", "cod", "--zona-horas", "-5"])
    paso = (r1 == r2 == ("archivo.json", "cod", None, None) and
           r3 == ("archivo.json", "cod", None, -5))
    marcar("MAIN-ARGS-ORDEN", paso,
          f"orden 1: {r1} · orden 2: {r2} (deben ser iguales) · con --zona-horas -5: {r3}")


def test_plantilla_solo_frecuencia_se_declara():
    """Ronda 3: 5+ clientes reales con la MISMA objecion de precio, SIN '¡', cruzan el
    umbral de frecuencia (limite heredado de produccion, no un bug de esta skill) y
    borran esas objeciones -- pero el hallazgo P6/DUDA que lo declara DEBE disparar,
    nombrando el texto, para que no se lea como un dia sin objeciones de precio."""
    def objecion(n):
        return {"user_ns": f"obj{n}", "get_info": {},
               "mensajes": [{"type": "in", "content": "esta muy caro",
                            "ts": f"2026-08-19 10:{n:02d}:00"}]}
    contactos = [objecion(i) for i in range(5)]
    c = Clasificador({"contactos": contactos}).correr()
    borradas = all(conv["motivo_no_compra"] == [] for conv in c.conversaciones)
    declarado = any(h["control"] == "P6" and h["severidad"] == "DUDA" and
                    "esta muy caro" in h["evidencia"] for h in c.hallazgos)
    paso = borradas and declarado
    marcar("PLANTILLA-FRECUENCIA-DECLARADA", paso,
          f"5 objeciones identicas sin '¡' cruzan el umbral de frecuencia y se borran: "
          f"{borradas} · el hallazgo P6/DUDA que lo declara con el texto citado "
          f"disparo: {declarado}")


# ------------------------------------------------------------------------------------- R6
# COHERENCIA INTRA-CHAT (sin Dropi). Tres casos que el encargo exige explicitamente:
# incoherencia real clara, cambio de opinion legitimo (NO debe marcarse), y caso ambiguo
# (debe caer en DUDA, no forzar severidad). Mas dos casos adicionales de robustez.

def test_r6_incoherencia_real():
    """Caso 1 (obligatorio): cliente pide azul, el resumen final del bot dice rojo, sin
    ningun mensaje del cliente entre medio que explique el cambio -> MUERTO."""
    contacto = {"user_ns": "fr6-incoherente", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "lo quiero en azul",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "out", "content": "perfecto, tu pedido: 1 producto, "
                    "confirmamos tu pedido en color rojo, direccion recibida",
                    "ts": "2026-08-19 09:10:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    h = next((x for x in c.hallazgos if x["control"] == "R6"), None)
    lleva_disclaimer = h is not None and "cambió de opinión" in h["consecuencia"]
    paso = h is not None and h["severidad"] == "MUERTO" and lleva_disclaimer
    marcar("R6-INCOHERENCIA-REAL", paso,
          f"hallazgo R6 disparado: {h is not None} · severidad: "
          f"{h['severidad'] if h else None} (debe ser MUERTO) · lleva el disclaimer de "
          f"'puede ser un cambio de opinion legitimo' en consecuencia: {lleva_disclaimer}")


def test_r6_cambio_opinion_no_se_marca():
    """Caso 2 (obligatorio): cliente pide azul, LUEGO dice 'mejor cambialo a rojo', el
    resumen final dice rojo -- coherente, NO debe generar ningun hallazgo R6."""
    contacto = {"user_ns": "fr6-cambio-legitimo", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "lo quiero en azul",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "in", "content": "mejor cambialo a rojo",
                    "ts": "2026-08-19 09:05:00"},
                   {"type": "out", "content": "listo, confirmamos tu pedido en color rojo, "
                    "direccion recibida", "ts": "2026-08-19 09:10:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    disparo = any(x["control"] == "R6" for x in c.hallazgos)
    marcar("R6-CAMBIO-OPINION-NO-MARCA", not disparo,
          f"hallazgo R6 disparado: {disparo} (debe ser False -- el resumen final SI "
          "recogio el ultimo valor que dijo el cliente, no es una incoherencia)")


def test_r6_ambiguo_cae_en_duda():
    """Caso 3 (obligatorio): el cliente menciona 3+ valores distintos de color a lo largo
    del hilo -- no se fuerza severidad alta, cae en DUDA."""
    contacto = {"user_ns": "fr6-ambiguo", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "lo quiero en azul", "ts": "2026-08-19 09:00:00"},
                   {"type": "in", "content": "mejor en verde", "ts": "2026-08-19 09:02:00"},
                   {"type": "in", "content": "no espera, a negro",
                    "ts": "2026-08-19 09:04:00"},
                   {"type": "out", "content": "confirmamos tu pedido en color rojo, "
                    "direccion de envio recibida", "ts": "2026-08-19 09:10:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    h = next((x for x in c.hallazgos if x["control"] == "R6"), None)
    paso = h is not None and h["severidad"] == "DUDA"
    marcar("R6-AMBIGUO-DUDA", paso,
          f"hallazgo R6 disparado: {h is not None} · severidad: "
          f"{h['severidad'] if h else None} (debe ser DUDA, no una severidad alta forzada)")


def test_r6_sin_atributo_no_genera_ruido():
    """Robustez: una conversacion donde el cliente nunca menciono un atributo concreto no
    debe generar NINGUN hallazgo R6 (no es ruido, es 'nada que comparar')."""
    contacto = {"user_ns": "fr6-sin-atributo", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "hola, cuanto cuesta el envio",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "out", "content": "el envio es gratis, gracias por tu compra",
                    "ts": "2026-08-19 09:10:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}).correr()
    disparo = any(x["control"] == "R6" for x in c.hallazgos)
    marcar("R6-SIN-ATRIBUTO", not disparo,
          f"hallazgo R6 disparado: {disparo} (debe ser False -- nada que comparar)")


def test_r6_no_requiere_dropi():
    """Robustez: R6 funciona con un DUMP que no trae ningun rastro de Dropi (get_info
    vacio, sin opted_in_through) -- confirma que el control es puramente intra-chat."""
    contacto = {"user_ns": "fr6-sin-dropi", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "quiero talla M",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "out", "content": "confirmamos tu pedido, talla L, direccion "
                    "recibida", "ts": "2026-08-19 09:10:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    h = next((x for x in c.hallazgos if x["control"] == "R6"), None)
    paso = h is not None and h["severidad"] == "MUERTO"
    marcar("R6-SIN-DROPI", paso,
          f"R6 funciono sin ningun dato de Dropi en get_info: hallazgo {h is not None}, "
          f"severidad {h['severidad'] if h else None} (debe ser MUERTO -- talla M vs L)")


# ---------------------------------------------------- fixes de la verificacion adversarial R6
# Cada uno reproduce un defecto REAL que golden-verificador encontro corriendo R6 contra hilos
# reales de produccion (2026-08-21) -- no un caso hipotetico. La cifra especifica de esa ronda
# ("1.829 hilos de dos espacios") es una cifra citada de una verificacion anterior cuyo
# artefacto no se conservo -- se declara honestamente sin el numero puntual; el hallazgo
# cualitativo (los defectos reales que reproducen las pruebas de abajo) sigue siendo la razon
# de estas pruebas.

def test_r6_talla_no_captura_basura():
    """El verificador midio 'no se cual es mi talla' -> talla='LA', 'que talla me
    recomienda' -> talla='ME' contra produccion real. PATRON_TALLA ahora solo acepta
    valores reales de talla (S/M/L/XL/XXL/XS o 1-2 digitos)."""
    casos_basura = [
        "no se cual es mi talla la verdad",
        "que talla me recomienda",
        "la talla no me quedo",
        "cual es la talla de este producto",
    ]
    capturas_basura = []
    for texto in casos_basura:
        atributos = extraer_atributos(texto)
        if any(t == "talla" for t, _ in atributos):
            capturas_basura.append((texto, atributos))
    caso_real = extraer_atributos("necesito talla M por favor")
    talla_real_ok = ("talla", "M") in caso_real
    paso = not capturas_basura and talla_real_ok
    marcar("R6-TALLA-NO-CAPTURA-BASURA", paso,
          f"frases sin talla real que NO deben capturar nada: "
          f"{'ninguna capturo basura' if not capturas_basura else capturas_basura} · "
          f"'talla M' sigue capturando talla=M: {talla_real_ok}")


def test_r6_color_sin_leadin_no_dispara():
    """El verificador midio, contra produccion real: 'a lo mejor la transportadora no
    vino a entregar' y 'no me vino no se porque' -> color='vino' (falso positivo del
    VERBO 'vino'), y lo mismo con 'cafe' (bebida), 'rosa' (nombre), 'gris' (clima). Sin
    un lead-in ('color'/'en'/'a' + palabra de color) esas frases NO deben producir
    ninguna mencion de color -- con el lead-in, el color real SI se sigue detectando."""
    frases_sin_leadin = [
        "a lo mejor la transportadora no vino a entregar",
        "no me vino no se porque",
        "me tome un cafe esperando el pedido",
        "rosa es mi vecina que tambien compro",
        "el clima esta gris hoy por aca",
    ]
    falsos = [(t, extraer_atributos(t)) for t in frases_sin_leadin
             if any(tp == "color" for tp, _ in extraer_atributos(t))]
    con_leadin = extraer_atributos("lo quiero en color vino") + extraer_atributos(
        "mandalo en cafe") + extraer_atributos("cambialo a rosa")
    detecta_con_leadin = sum(1 for t, v in con_leadin if t == "color") == 3
    paso = not falsos and detecta_con_leadin
    marcar("R6-COLOR-SIN-LEADIN-NO-DISPARA", paso,
          f"frases con palabras-color-que-son-palabras-corrientes SIN lead-in, falsos "
          f"positivos: {falsos or 'ninguno'} · con lead-in ('en'/'a'/'color') los 3 "
          f"colores reales se detectan igual: {detecta_con_leadin}")


def test_r6_correccion_post_resumen():
    """El verificador encontro que un cliente que corrige el color DESPUES del resumen
    final quedaba en silencio total (ni MUERTO ni DUDA). Ahora debe generar DUDA."""
    contacto = {"user_ns": "fr6-post-resumen", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "hola quiero el producto",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "out", "content": "confirmamos tu pedido en color rojo, "
                    "direccion de envio recibida", "ts": "2026-08-19 09:05:00"},
                   {"type": "in", "content": "espera, yo lo pedi en azul",
                    "ts": "2026-08-19 09:06:00"},
               ]}
    c = Clasificador({"contactos": [contacto]}, modo="cod").correr()
    h = next((x for x in c.hallazgos if x["control"] == "R6"), None)
    paso = h is not None and h["severidad"] == "DUDA" and "DESPUÉS" in h["titulo"]
    marcar("R6-CORRECCION-POST-RESUMEN", paso,
          f"hallazgo R6 disparado para correccion posterior al resumen: {h is not None} · "
          f"severidad: {h['severidad'] if h else None} (debe ser DUDA, no silencio)")


def test_credenciales_extraer_py_camino_real():
    """F3 (CRITICO SEGURIDAD, golden-verificador 2026-08-22): el defecto de raiz de la ronda
    anterior (CREDENCIALES-AMPLIADAS) fue que su UNICA prueba directa importaba
    `redactar_texto` de `clasificar.py` -- nunca del camino real que escribe el DUMP a disco
    (`extraer.py`). Esta prueba corre las 17 familias de `secretos.PATRONES_SECRETO` contra
    `extraer.redactar()` (la funcion que limpia cada campo del DUMP) y contra
    `extraer.quedan_secretos()` (la compuerta final que bloquea la escritura) -- el camino
    REAL, no una funcion suelta."""
    casos = {
        "sk_live_" + "A" * 24: "StripeLive",
        "whsec_" + "A" * 20: "StripeWebhook",
        "APP_USR-1234567890123456-081020-abcdef1234567890abcdef1234567890-123456789":
            "MercadoPagoLive",
        "12345|" + "a" * 25: "SanctumBearer-umbral-20",   # {20,}: antes 32 en extraer.py
        "ghp_" + "c" * 36: "GitHubPAT",
        "github_pat_" + "d" * 60: "GitHubFineGrained",
        "AKIA" + "E" * 16: "AWSAccessKey",
        "xoxb-" + "1" * 20: "SlackToken",
        "SG." + "f" * 20 + "." + "g" * 20: "SendGrid",
        "1//0" + "h" * 30: "GoogleOAuthRefresh",
        "a" * 64: "HexBearerGenerico",
    }
    fallos_redactar = []
    fallos_compuerta = []
    for secreto, etiqueta in casos.items():
        objeto = {"campo_cualquiera": f"el cliente escribio {secreto} en el chat"}
        limpio = _extraer_modulo.redactar(objeto)
        if secreto in json.dumps(limpio, ensure_ascii=False):
            fallos_redactar.append(etiqueta)
        if secreto in json.dumps(objeto, ensure_ascii=False):
            encontrados = _extraer_modulo.quedan_secretos(objeto)
            if not encontrados:
                fallos_compuerta.append(etiqueta)
    paso = not fallos_redactar and not fallos_compuerta
    marcar("CREDENCIALES-EXTRAER-PY-REAL", paso,
          f"familias sin redactar por extraer.redactar(): {fallos_redactar or 'ninguna'} · "
          f"familias que la compuerta extraer.quedan_secretos() NO detecto: "
          f"{fallos_compuerta or 'ninguna'} (probado por el camino REAL de extraer.py, no "
          "por una funcion suelta importada de clasificar.py)")


def test_cantidad_vocabulario_ampliado():
    """F4 (RIESGO, golden-verificador 2026-08-22): el vocabulario original de cantidad
    ('unidades|pares|combos|paquetes') tenia recall=0 contra 165 conversaciones reales
    medidas. Las FORMAS reales que quedaban sin cobertura (no el texto literal de ningun
    cliente -- regla del encargo, fixtures SINTETICOS inspirados en la forma general):
    cantidad singular sin plural, "N frasco(s)/similar", cantidad con verbo/articulo de
    pedido sin unidad explicita, y el nombre de un producto generico usado como unidad
    implicita. Se prueba que esas formas ahora capturan cantidad, y que las condiciones que
    YA pasaban antes de ampliar (no pide Dropi, no acusa cambio de opinion legitimo, declara
    DUDA en ambiguos) siguen pasando -- ver CONTROL_R6 mas arriba, no se repiten aqui."""
    casos = {
        "necesito 1 unidad nada mas": "1",
        "me interesa probar un frasco antes de pedir mas": "1",
        "me llevo 2, muchas gracias": "2",
        "dame 3 cajas": "3",
        # nombre de producto GENERICO/ficticio, EN SU PROPIA LINEA -- forma real medida en
        # produccion (direccion en una linea, "N producto" solo en la ultima linea). Ronda 2
        # de verificacion (golden-verificador, 2026-08-22): la version anterior de este
        # patron no exigia linea completa y el 76% de sus disparos reales eran numeros de
        # direccion (un numero de torre o apartamento seguido de la palabra siguiente de la
        # direccion) -- ahora exige que la linea ENTERA sea "numero + palabra", nada mas, por
        # eso el fixture simula una direccion en una linea y la cantidad en la siguiente.
        "Calle 10 # 20-30 apto 402\n1 crematonica": "1",
    }
    fallos = []
    for texto, esperado in casos.items():
        atributos = extraer_atributos(texto)
        cantidades = [v for t, v in atributos if t == "cantidad"]
        if esperado not in cantidades:
            fallos.append((texto, cantidades))
    # No debe capturar cantidad en frases de TIEMPO (falso positivo del stoplist).
    falso_positivo_tiempo = extraer_atributos("llega en 3 dias habiles")
    tiene_cantidad_falsa = any(t == "cantidad" for t, _ in falso_positivo_tiempo)
    # Ronda 2 de verificacion (golden-verificador, 2026-08-22): direcciones REALES medidas
    # que antes disparaban cantidad falsa (formas SINTETICAS aqui, misma estructura que las
    # que fallaron en produccion: numero de torre/apto/interior/piso seguido de una palabra,
    # y un numero de casa seguido del nombre del barrio) -- ahora NINGUNA debe disparar,
    # porque el patron de producto implicito exige que la LINEA COMPLETA sea "numero +
    # palabra" y una direccion nunca es eso.
    direcciones_sinteticas = [
        "Diagonal 61 # 20-19 torre 3 apto 501",
        "Kra 88 # 9c - 41 barrio villanueva",
        "Avenida 30 # 71-8 barrio san jose",
        "Circular 12 # 40b - 3 piso 5 oficina",
    ]
    falsos_direccion = [(t, extraer_atributos(t)) for t in direcciones_sinteticas
                        if any(tp == "cantidad" for tp, _ in extraer_atributos(t))]
    paso = not fallos and not tiene_cantidad_falsa and not falsos_direccion
    marcar("CANTIDAD-VOCABULARIO-AMPLIADO", paso,
          f"casos reales sin capturar: {fallos or 'ninguno'} · falso positivo en "
          f"'3 dias habiles' (no debe capturar cantidad): {tiene_cantidad_falsa} · "
          f"falsos positivos de DIRECCION (no deben capturar cantidad, hallazgo de la "
          f"ronda 2 de verificacion — 76% de los disparos reales eran direcciones): "
          f"{falsos_direccion or 'ninguno'}")


def test_r2_r3_r4_acotan_al_dia_auditado():
    """FALLA 1 (golden-verificador, ronda 2 sobre GCO1.4, 2026-08-22): el hilo descargado
    trae el HISTORICO COMPLETO del contacto, no solo el dia auditado -- R2/R3/R4/Q4 recorrian
    el hilo completo y podian acusar al bot de una demora, un bucle o una frase de OTRO DIA.
    Contacto sintetico con dos gaps de mas de 30 min: uno el dia ANTERIOR al auditado (no debe
    disparar R2), otro el dia auditado (SI debe disparar R2). `_fecha` del dump = el dia
    auditado."""
    dia_anterior = "2026-08-18"
    dia_auditado = "2026-08-19"
    contacto = {"user_ns": "facota-dia", "get_info": {},
               "mensajes": [
                   # gap de 61 min el dia ANTERIOR -- NO debe generar R2.
                   {"type": "in", "content": "cuanto cuesta",
                    "ts": f"{dia_anterior} 08:00:00"},
                   {"type": "out", "content": "cuesta 74900",
                    "ts": f"{dia_anterior} 09:01:00"},
                   # gap de 61 min el dia AUDITADO -- SI debe generar R2.
                   {"type": "in", "content": "y el envio cuanto vale",
                    "ts": f"{dia_auditado} 10:00:00"},
                   {"type": "out", "content": "el envio es gratis",
                    "ts": f"{dia_auditado} 11:01:00"},
               ]}
    dump = {"_fecha": dia_auditado, "contactos": [contacto]}
    c = Clasificador(dump, modo="cod").correr()
    r2 = [h for h in c.hallazgos if h["control"] == "R2"]
    solo_dia_auditado = len(r2) == 1 and dia_auditado in r2[0]["evidencia"]
    otro_dia_ausente = not any(dia_anterior in h["evidencia"] for h in r2)
    paso = solo_dia_auditado and otro_dia_ausente
    marcar("R2-ACOTA-AL-DIA", paso,
          f"hallazgos R2: {len(r2)} (debe ser 1, solo el gap del {dia_auditado}) · "
          f"cita el dia auditado: {solo_dia_auditado} · NO cita el gap del "
          f"{dia_anterior}: {otro_dia_ausente}")


def test_listado_paginacion_no_medible_se_declara():
    """FALLA 3 (golden-verificador, ronda 2 sobre GCO1.4, 2026-08-22): si el DUMP no trae la
    clave `_listado_paginacion` (DUMP extraido con una version de extraer.py anterior a este
    campo, como los 4 DUMPs reales de LIBIDO-UP usados para validar F1-F11), la version
    anterior de este fix declaraba `listado_truncado_por_tope_500: False` -- ausencia de dato
    leida como 'no se trunco', exactamente la regla I4 que esta misma skill prohibe en el
    control INV. Ahora debe declararse 'no_medible' con un hallazgo DUDA propio."""
    contacto = {"user_ns": "fsinpaginacion", "get_info": {},
               "mensajes": [{"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00"}]}
    dump_sin_clave = {"contactos": [contacto]}          # sin _listado_paginacion
    dump_con_clave = {"contactos": [contacto],
                      "_listado_paginacion": {"truncado_por_tope_500": False}}
    c_sin = Clasificador(dump_sin_clave).correr()
    c_con = Clasificador(dump_con_clave).correr()
    no_medible_declarado = c_sin.universo["listado_truncado_por_tope_500"] == "no_medible"
    hallazgo_no_medible = any(h["control"] == "P-listado-truncado" and h["severidad"] == "DUDA"
                              for h in c_sin.hallazgos)
    con_clave_da_false = c_con.universo["listado_truncado_por_tope_500"] is False
    paso = no_medible_declarado and hallazgo_no_medible and con_clave_da_false
    marcar("LISTADO-PAGINACION-NO-MEDIBLE", paso,
          f"sin la clave en el DUMP: listado_truncado_por_tope_500="
          f"{c_sin.universo['listado_truncado_por_tope_500']!r} (debe ser 'no_medible', no "
          f"False) · hallazgo DUDA disparado: {hallazgo_no_medible} · con la clave presente "
          f"(False real): {con_clave_da_false} (debe seguir siendo False, no 'no_medible')")


def test_acotado_al_dia_respeta_zona_horaria():
    """ROTO NUEVO (golden-verificador, TERCERA ronda de verificacion sobre GCO1.4,
    2026-08-22): el fix de FALLA 1 comparaba `dt.date()` en UTC (de `_epoch_a_fecha`) contra
    `self.fecha_auditada` (hora LOCAL del servidor, medido -5h/Colombia en el unico espacio
    confirmado) -- sin ajustar el offset, un mensaje real cerca de medianoche local caia del
    lado equivocado del calendario en UTC. Medido contra los 4 DUMPs reales: 111 mensajes
    reales del dia se perdian, 78 de otro dia se colaban -- la MISMA clase de fallo que FALLA
    1 decia haber cerrado. Fixture: un mensaje a las 23:30 hora Colombia del dia auditado (por
    lo tanto 04:30 UTC del dia SIGUIENTE) debe seguir contando como del dia auditado."""
    dia_auditado = "2026-08-19"
    # 2026-08-20 04:30:00 UTC == 2026-08-19 23:30:00 hora Colombia (UTC-5).
    ts_medianoche_local = 1787200200
    ts_respuesta = 1787200260   # +1 min, 04:31:00 UTC == 23:31:00 local, mismo dia local
    contacto = {"user_ns": "fzona-horaria", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "todavia estan disponibles",
                    "ts": ts_medianoche_local},
                   {"type": "out", "content": "no entendi, puedes reformular?",
                    "ts": ts_respuesta},
                   {"type": "out", "content": "no entendi, puedes reformular?",
                    "ts": ts_respuesta + 60},
                   {"type": "out", "content": "no entendi, puedes reformular?",
                    "ts": ts_respuesta + 120},
               ]}
    dump = {"_fecha": dia_auditado, "contactos": [contacto]}
    c_con_zona = Clasificador(dump, modo="cod").correr()
    r3_con_zona = any(h["control"] == "R3" for h in c_con_zona.hallazgos)
    c_sin_ajuste = Clasificador(dump, modo="cod", zona_horas=0).correr()
    r3_sin_ajuste = any(h["control"] == "R3" for h in c_sin_ajuste.hallazgos)
    zona_declarada = c_con_zona.universo.get("zona_horas_usada") == -5
    paso = r3_con_zona and not r3_sin_ajuste and zona_declarada
    marcar("ACOTADO-RESPETA-ZONA-HORARIA", paso,
          f"con zona_horas=-5 (default): R3 disparado (mensajes cerca de medianoche local "
          f"reconocidos como del dia auditado): {r3_con_zona} · con zona_horas=0 (UTC a "
          f"secas, el bug): R3 NO disparado (mensajes descartados por caer del lado UTC "
          f"equivocado): {not r3_sin_ajuste} (debe ser True -- confirma que el offset SI "
          f"hace la diferencia) · zona_horas_usada declarada en universo: {zona_declarada}")


def test_sin_fecha_auditada_se_declara():
    """ROTO NUEVO (golden-verificador, TERCERA ronda, 2026-08-22): si el DUMP no trae
    `_fecha`, `_mensajes_del_dia` se desactivaba EN SILENCIO (sin hallazgo, sin clave en
    `universo`) -- la misma clase de fallo 'ausencia de dato leida como sano' que la propia
    skill prohibe en el control INV y que ya corrige para `_listado_paginacion`. Ahora debe
    declararse con un hallazgo DUDA y con `universo['acotado_al_dia_activo'] = False`."""
    contacto = {"user_ns": "fsinfecha", "get_info": {},
               "mensajes": [{"type": "in", "content": "hola", "ts": "2026-08-19 09:00:00"}]}
    dump_sin_fecha = {"contactos": [contacto]}          # sin _fecha
    dump_con_fecha = {"_fecha": "2026-08-19", "contactos": [contacto]}
    c_sin = Clasificador(dump_sin_fecha).correr()
    c_con = Clasificador(dump_con_fecha).correr()
    hallazgo_disparado = any(h["control"] == "P-sin-fecha-auditada" and h["severidad"] == "DUDA"
                             for h in c_sin.hallazgos)
    universo_declara_false = c_sin.universo.get("acotado_al_dia_activo") is False
    con_fecha_no_dispara = not any(h["control"] == "P-sin-fecha-auditada"
                                   for h in c_con.hallazgos)
    universo_declara_true = c_con.universo.get("acotado_al_dia_activo") is True
    paso = (hallazgo_disparado and universo_declara_false and con_fecha_no_dispara and
           universo_declara_true)
    marcar("SIN-FECHA-AUDITADA-DECLARADA", paso,
          f"sin `_fecha`: hallazgo DUDA disparado: {hallazgo_disparado} · "
          f"acotado_al_dia_activo=False declarado: {universo_declara_false} · con `_fecha`: "
          f"NO dispara el hallazgo: {con_fecha_no_dispara} · acotado_al_dia_activo=True: "
          f"{universo_declara_true}")


def test_fecha_auditada_malformada_se_declara():
    """ROTO NUEVO 5a (golden-verificador, CUARTA ronda de verificacion, 2026-08-22): una
    `_fecha` PRESENTE pero con formato distinto a AAAA-MM-DD (o corrompida) hacia que
    `_mensajes_del_dia` filtrara TODO a una lista vacia, con `acotado_al_dia_activo=True`
    (formalmente cierto, enganoso: el 'acotado' esta activo pero es inutil) -- R2/R3/R4/Q4
    corrian en silencio sobre cero mensajes. Medido: 2 hallazgos R4/MUERTO reales (pago
    anticipado mencionado por el bot) desaparecian sin aviso con una `_fecha` malformada en
    la corrida real. Ahora una `_fecha` malformada se trata IGUAL que una `_fecha` ausente:
    mismo hallazgo DUDA, `acotado_al_dia_activo=False`."""
    contacto = {"user_ns": "ffechamal", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "necesito pago anticipado o contra entrega",
                    "ts": "2026-08-19 09:00:00"},
                   {"type": "out", "content": "para procesar tu pedido necesitas hacer un "
                    "pago anticipado", "ts": "2026-08-19 09:01:00"},
               ]}
    dump = {"_fecha": "19/08/2026", "contactos": [contacto]}   # formato NO AAAA-MM-DD
    c = Clasificador(dump, modo="cod").correr()
    r4_sobrevive = any(h["control"] == "R4" for h in c.hallazgos)
    hallazgo_disparado = any(h["control"] == "P-sin-fecha-auditada" and h["severidad"] == "DUDA"
                             for h in c.hallazgos)
    acotado_correcto = c.universo.get("acotado_al_dia_activo") is False
    paso = r4_sobrevive and hallazgo_disparado and acotado_correcto
    marcar("FECHA-AUDITADA-MALFORMADA-DECLARADA", paso,
          f"con `_fecha` malformada ('19/08/2026'): el hallazgo R4 real SIGUE saliendo "
          f"(no se pierde en silencio): {r4_sobrevive} · hallazgo P-sin-fecha-auditada "
          f"disparado: {hallazgo_disparado} · acotado_al_dia_activo=False (no True "
          f"enganoso): {acotado_correcto}")


def test_ts_mezclado_epoch_e_iso_no_revienta():
    """ROTO NUEVO 5b (golden-verificador, CUARTA ronda de verificacion, 2026-08-22):
    `parse_fecha` devolvia NAIVE para epoch pero AWARE para ISO-con-offset (ej. terminado en
    'Z') -- un DUMP que mezclara ambas formas (nunca visto en produccion, pero declarado
    como aceptado) hacia que cualquier resta/comparacion entre las dos reventara con
    `TypeError: can't compare offset-naive and offset-aware datetimes`, tumbando TODA la
    corrida sin capturar. Ahora ambas formas se normalizan a NAIVE (UTC)."""
    epoch_dt = parse_fecha(1787114990)
    iso_z_dt = parse_fecha("2026-08-19T04:49:50Z")
    ambos_naive = epoch_dt.tzinfo is None and iso_z_dt.tzinfo is None
    coinciden = epoch_dt == iso_z_dt
    # Camino REAL: un contacto con un ts epoch y otro ts ISO-con-Z en el MISMO hilo no debe
    # levantar excepcion al invertir/clasificar (antes de este fix, reventaba aqui).
    contacto = {"user_ns": "fmixed", "get_info": {},
               "mensajes": [
                   {"type": "in", "content": "hola", "ts": 1787114980},
                   {"type": "out", "content": "hola, en que te ayudo",
                    "ts": "2026-08-19T04:49:50Z"},
               ]}
    exploto = False
    try:
        Clasificador({"contactos": [contacto]}).correr()
    except TypeError:
        exploto = True
    paso = ambos_naive and coinciden and not exploto
    marcar("TS-MEZCLADO-EPOCH-ISO-NO-REVIENTA", paso,
          f"epoch y ISO-Z ambos naive: {ambos_naive} · fechas coinciden: {coinciden} "
          f"({epoch_dt} vs {iso_z_dt}) · Clasificador con un hilo mezclado NO lanza "
          f"TypeError: {not exploto}")


TRAMPAS_DEL_ENCARGO = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11",
                      "P12", "P13"]
EXTRA_CALIDAD = ["R1", "R2", "R3", "R4", "Q4"]
FIXES_ADVERSARIALES = ["TYPE-REAL", "DESCONOCIDOS", "COMPUERTA-SILENCIA",
                       "DROPI-EXCLUIDO-PCT", "MODO-INVALIDO", "BUCLE-FALSO-POSITIVO",
                       "Q4-FALSO-POSITIVO", "INVENTARIO-ABORTA", "CREDENCIALES-AMPLIADAS"]
FIXES_RONDA_2 = ["DROPI-NORMALIZADO", "CORTE-IGNORA-NOTAS",
                "DENOMINADOR-3-ESTADOS", "PLANTILLA-NO-BORRA-OBJECION",
                "PLANTILLA-CHICO-DECLARADO", "DINERO-RECHAZA-NO-STR", "MAIN-ARGS-ORDEN",
                "PLANTILLA-FRECUENCIA-DECLARADA"]
CONTROL_R6 = ["R6-INCOHERENCIA-REAL", "R6-CAMBIO-OPINION-NO-MARCA", "R6-AMBIGUO-DUDA",
             "R6-SIN-ATRIBUTO", "R6-SIN-DROPI"]
FIXES_R6_VERIFICACION = ["R6-TALLA-NO-CAPTURA-BASURA", "R6-COLOR-SIN-LEADIN-NO-DISPARA",
                         "R6-CORRECCION-POST-RESUMEN"]
# F1/F2 (golden-verificador 2026-08-22): `ts` epoch es la forma REAL de los 4 DUMPs de
# produccion medidos (LIBIDO-UP, 100% de los mensajes). TS-ILEGIBLE (ronda 2) EXIGIA que un
# epoch se tratara como no parseable -- expectativa invertida ahora que SI se parsea; ver
# `test_ts_epoch_ordena_correctamente` (reemplaza a la vieja TS-ILEGIBLE) y las 4 fixtures
# nuevas que la acompañan.
FIXES_F1_EPOCH = ["TS-EPOCH-ORDENA", "TS-NO-NUMERICO-ILEGIBLE", "TS-EPOCH-MS-DETECTADO",
                  "TS-EPOCH-CADENA", "EPOCH-R1-R2-R3-REALES"]
FIXES_GCO14 = FIXES_F1_EPOCH + ["CREDENCIALES-EXTRAER-PY-REAL", "CANTIDAD-VOCABULARIO-AMPLIADO"]
# Ronda 2 de verificacion sobre GCO1.4 (golden-verificador, 2026-08-22): FALLA 1 (R2/R3/R4/Q4
# sin acotar al dia auditado) y FALLA 3 (paginacion no medible leida como "no se trunco").
FIXES_GCO14_RONDA2 = ["R2-ACOTA-AL-DIA", "LISTADO-PAGINACION-NO-MEDIBLE",
                      "ACOTADO-RESPETA-ZONA-HORARIA", "SIN-FECHA-AUDITADA-DECLARADA"]
# Cuarta ronda de verificacion sobre GCO1.4 (golden-verificador, 2026-08-22): ROTO NUEVO 5a
# (`_fecha` malformada leida como sana) y 5b (mezcla epoch/ISO-Z revienta con TypeError).
FIXES_GCO14_RONDA3 = ["FECHA-AUDITADA-MALFORMADA-DECLARADA", "TS-MEZCLADO-EPOCH-ISO-NO-REVIENTA"]


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
    test_corte_del_dia_ignora_notas()
    test_denominador_tres_estados()
    test_plantilla_forma_no_borra_objecion_real()
    test_plantilla_universo_chico_declarado()
    test_parse_dinero_rechaza_no_str()
    test_main_args_orden_independiente()
    test_plantilla_solo_frecuencia_se_declara()

    test_r6_incoherencia_real()
    test_r6_cambio_opinion_no_se_marca()
    test_r6_ambiguo_cae_en_duda()
    test_r6_sin_atributo_no_genera_ruido()
    test_r6_no_requiere_dropi()

    test_r6_talla_no_captura_basura()
    test_r6_color_sin_leadin_no_dispara()
    test_r6_correccion_post_resumen()

    test_ts_epoch_ordena_correctamente()
    test_ts_no_numerico_sigue_ilegible()
    test_ts_epoch_milisegundos_se_detecta()
    test_ts_epoch_como_cadena_se_parsea()
    test_r1_r2_r3_con_ts_epoch_real()

    test_credenciales_extraer_py_camino_real()
    test_cantidad_vocabulario_ampliado()
    test_r2_r3_r4_acotan_al_dia_auditado()
    test_listado_paginacion_no_medible_se_declara()
    test_acotado_al_dia_respeta_zona_horaria()
    test_sin_fecha_auditada_se_declara()
    test_fecha_auditada_malformada_se_declara()
    test_ts_mezclado_epoch_e_iso_no_revienta()

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

    print("\nControl R6 · coherencia intra-chat (sin Dropi) -- incoherencia real, cambio "
         "de opinion legitimo (NO debe marcarse) y caso ambiguo (debe caer en DUDA):")
    fallidas_r6 = []
    for codigo in CONTROL_R6:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:26} {detalle}")
        if not paso:
            fallidas_r6.append(codigo)

    print("\nFixes de la verificacion adversarial de golden-verificador sobre R6 "
         "(2026-08-21, hilos reales de produccion -- cifra especifica de esa ronda no "
         "conservada, ver comentario en el codigo) -- cada uno reproduce un defecto real "
         "que encontro:")
    fallidas_r6_verif = []
    for codigo in FIXES_R6_VERIFICACION:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:30} {detalle}")
        if not paso:
            fallidas_r6_verif.append(codigo)

    print("\nFixes de la verificacion adversarial de golden-verificador GCO1.4 (2026-08-22, "
         "4 DUMPs reales de LIBIDO-UP, 165 conversaciones) -- F1 (epoch en `ts`), F3 "
         "(camino real de extraer.py) y F4 (vocabulario de cantidad ampliado):")
    fallidas_gco14 = []
    for codigo in FIXES_GCO14:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:30} {detalle}")
        if not paso:
            fallidas_gco14.append(codigo)

    print("\nFixes de la SEGUNDA verificacion adversarial sobre GCO1.4 (golden-verificador, "
         "2026-08-22, misma corrida contra los 4 DUMPs reales) -- FALLA 1 (R2/R3/R4/Q4 sin "
         "acotar al dia auditado) y FALLA 3 (paginacion no medible leida como 'no se "
         "trunco'):")
    fallidas_gco14_r2 = []
    for codigo in FIXES_GCO14_RONDA2:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:30} {detalle}")
        if not paso:
            fallidas_gco14_r2.append(codigo)

    print("\nFixes de la CUARTA verificacion adversarial sobre GCO1.4 (golden-verificador, "
         "2026-08-22) -- ROTO NUEVO 5a (`_fecha` malformada leida como sana) y 5b (mezcla "
         "epoch/ISO-Z revienta con TypeError):")
    fallidas_gco14_r3 = []
    for codigo in FIXES_GCO14_RONDA3:
        paso, detalle = RESULTADOS.get(codigo, (False, "no se corrio ninguna prueba"))
        marca = "OK   " if paso else "FALLA"
        print(f"  {marca} {codigo:30} {detalle}")
        if not paso:
            fallidas_gco14_r3.append(codigo)

    if (fallidas or fallidas_extra or fallidas_fixes or fallidas_ronda2 or fallidas_r6 or
            fallidas_r6_verif or fallidas_gco14 or fallidas_gco14_r2 or fallidas_gco14_r3):
        print(f"\nAUTOPRUEBA FALLIDA. Trampas del encargo sin detectar: {fallidas or 'ninguna'}. "
             f"Controles de calidad sin detectar: {fallidas_extra or 'ninguno'}. "
             f"Fixes adversariales (ronda 1) sin confirmar: {fallidas_fixes or 'ninguno'}. "
             f"Fixes (ronda 2) sin confirmar: {fallidas_ronda2 or 'ninguno'}. "
             f"Control R6 sin confirmar: {fallidas_r6 or 'ninguno'}. "
             f"Fixes de verificacion R6 sin confirmar: {fallidas_r6_verif or 'ninguno'}. "
             f"Fixes GCO1.4 sin confirmar: {fallidas_gco14 or 'ninguno'}. "
             f"Fixes GCO1.4 (ronda 2) sin confirmar: {fallidas_gco14_r2 or 'ninguno'}. "
             f"Fixes GCO1.4 (ronda 3) sin confirmar: {fallidas_gco14_r3 or 'ninguno'}.")
        print("El clasificador esta roto. No se corre contra un DUMP real hasta arreglarlo.")
        return 1

    total_controles = (len(TRAMPAS_DEL_ENCARGO) + len(EXTRA_CALIDAD) +
                       len(FIXES_ADVERSARIALES) + len(FIXES_RONDA_2) + len(CONTROL_R6) +
                       len(FIXES_R6_VERIFICACION) + len(FIXES_GCO14) + len(FIXES_GCO14_RONDA2) +
                       len(FIXES_GCO14_RONDA3))
    print(f"\n  {total_controles} de {total_controles} controles confirmados en total "
         f"({len(TRAMPAS_DEL_ENCARGO)} trampas del encargo + {len(EXTRA_CALIDAD)} calidad + "
         f"{len(FIXES_ADVERSARIALES)} fixes ronda 1 + {len(FIXES_RONDA_2)} fixes ronda 2 + "
         f"{len(CONTROL_R6)} control R6 + {len(FIXES_R6_VERIFICACION)} fixes verificacion R6 + "
         f"{len(FIXES_GCO14)} fixes GCO1.4 + {len(FIXES_GCO14_RONDA2)} fixes GCO1.4 ronda 2 + "
         f"{len(FIXES_GCO14_RONDA3)} fixes GCO1.4 ronda 3)")
    print("\nAutoprueba pasada. Esto valida el DETECTOR contra casos que se SABEN rotos, no "
         "valida ningun dia real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
