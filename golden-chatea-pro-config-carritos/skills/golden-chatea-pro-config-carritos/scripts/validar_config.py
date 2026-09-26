#!/usr/bin/env python3
"""Valida el JSON de [Carritos] Configuracion ANTES de escribirlo en el espacio.

POR QUE EXISTE. Esta skill sabia escribir los mensajes de recuperacion y no tenia el molde
del campo: cubria 4 de las 29 llaves. Un JSON incompleto no da error al pegarlo — el panel lo
acepta y el asistente lee vacio el trozo que falta y se inventa el comportamiento.

LOS TRES FALLOS QUE ESTE VALIDADOR EXISTE PARA ATRAPAR, los tres MEDIDOS en un espacio real
el 2026-09-08 y los tres SILENCIOSOS:

  1. Un campo por encima de su tope NATIVO. Medido: transportadoras_disponibles en 132 con
     tope 100. Funciona hoy porque se escribio por JSON. El dia que alguien abra el panel y
     pulse Guardar se corta en el 100, y el corte se come el final, que es donde suele ir la
     transportadora PROHIBIDA. El bot dejaria de saberlo y la ofreceria.
  2. `tiempo_recordatorio_3` con valor. El panel tiene DOS pares (tiempo, plantilla); esa llave
     vive en el JSON sin casilla y sin nada que enviar. Va vacia.
  3. `datos_pago_anticipado` HEREDADO. Lleva medio de pago, nombre y telefono de quien recibe
     el dinero. Clonado entre espacios, manda el dinero de un cliente a la cuenta de otro.

Uso:  python3 validar_config.py --in config.json [--dueño-confirmo-datos-de-pago]
      python3 validar_config.py --autoprueba
Salida: 0 sin criticas · 1 hay criticas · 2 error de uso.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chatea_api import u16  # noqa: E402  UNA sola definicion: la misma que usa escribir_config.py

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "limites.json"), encoding="utf-8") as _f:
    LIM = json.load(_f)
NATIVO = LIM["capa_nativa"]
BOT = LIM["bot_field"]

# Clase de error medida el 18-sep: frases comerciales que suenan bien y nadie confirmo.
SIN_CONFIRMAR = re.compile(r"mismo d[ií]a|antes de las \d|tiempo limitado|importador directo|"
                           r"legalmente constituida|lo procesamos hoy|despacho hoy|garantizad|"
                           r"en \d+ horas|llega ma[ñn]ana|si lo confirmamos hoy|solo por hoy|"
                           r"[uú]ltimas unidades|menos de un minuto", re.I)
# Una frase que menciona emojis y NO los niega en la MISMA frase, en un prompt de la IA, se los
# permite. Se mide por frase: un "no uses emojis en quejas" no perdona un "maximo dos emojis".
NIEGA = re.compile(r"\b(no|nunca|sin|jam[aá]s|prohibid)", re.I)
PAGO_AL_RECIBIR = re.compile(r"efectivo|al recibir|contra ?entrega|cuando (te )?llegue|"
                             r"pagar[aá]s", re.I)
# Todo texto que sale por WhatsApp. El correo no: es otro canal.
WHATSAPP = ["identidad_asistente.adaptacion_lenguaje", "identidad_asistente.metodo_anticancelacion",
            "mensajes_recuperacion.mensaje_agradecimiento", "datos_tienda.mensaje_descuento",
            "datos_tienda.ubicacion_tienda", "datos_logisticos.tiempos_envio",
            "datos_logisticos.transportadoras_disponibles"]


def es_si(v):
    return str(v).strip().lower() in ("si", "sí", "true", "1", "yes")


def hojas(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if str(k).startswith("_"):
                continue
            yield from hojas(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        yield (p or "(raiz)"), o
    else:
        yield p, o


def esperadas():
    """Las 29 llaves salen del propio template: una sola fuente, no una lista repetida."""
    with open(os.path.join(ASSETS, "template-botfield-configuracion.json"), encoding="utf-8") as f:
        return {k for k, _ in hojas(json.load(f))}


def escapado(valor):
    """Techo A, UNA sola vara (la de limites.json): len(json.dumps(valor)[1:-1]) con los valores
    por defecto de json.dumps, donde cada tilde ocupa 6 y cada emoji astral 12. Es la medida
    conservadora."""
    return len(json.dumps(valor, separators=(",", ":"))[1:-1])


def validar(d, dueno_confirmo=False):
    criticas, avisos = [], []
    plano = dict(hojas(d))

    # --- 1 · estructura completa
    faltan = sorted(esperadas() - set(plano))
    if faltan:
        criticas.append(f"faltan {len(faltan)} llaves: {', '.join(faltan[:8])}"
                        + (" ..." if len(faltan) > 8 else ""))

    # --- 2 · huecos sin rellenar
    huecos = [k for k, v in plano.items() if isinstance(v, str) and "{{" in v]
    if huecos:
        criticas.append(f"{len(huecos)} marcadores sin rellenar: {', '.join(huecos[:6])}")

    # --- 3 · TECHO B, campo por campo
    for k, v in plano.items():
        hoja = k.split(".")[-1]
        tope = NATIVO.get(hoja)
        if tope and isinstance(v, str) and u16(v) > tope:
            criticas.append(
                f"{k} mide {u16(v)} y su tope nativo es {tope}. Se puede escribir por JSON, "
                f"pero si alguien abre el panel y guarda, se CORTA en el {tope} y se pierde: "
                f"...{v[max(0,tope-18):tope]}|CORTE|{v[tope:tope+18]}...")

    # --- 4 · TECHO A, el campo entero
    esc = escapado(d)
    if esc > BOT["legacy_json_escapado"]:
        criticas.append(f"el JSON completo mide {esc} escapados y el tope es "
                        f"{BOT['legacy_json_escapado']}: se guarda CORTADO con un 200 ok")
    elif esc > BOT["seguro_escapado"]:
        avisos.append(f"el JSON COMPLETO mide {esc} escapados y el tope del campo entero es "
                      f"{BOT['legacy_json_escapado']}. Esto NO contradice 'el techo no es defecto': "
                      f"aquello habla de cada casilla; esto es el campo entero, donde pasarse "
                      f"guarda cortado con un 200 ok. No se recorta texto util: se convierte el "
                      f"campo a LONG JSON.")

    # --- 5 · el TERCER recordatorio: hora sin plantilla
    mr = d.get("mensajes_recuperacion", {})
    t3 = str(mr.get("tiempo_recordatorio_3", "")).strip()
    plantillas = mr.get("carritos", {})
    if t3:
        criticas.append(
            f"tiempo_recordatorio_3 vale '{t3}' y NO existe su plantilla. El panel solo tiene "
            f"DOS pares (tiempo, plantilla): esa llave vive en el JSON sin casilla y sin nada que "
            f"enviar. Se deja VACIA para que la configuracion deje de mentir.")

    # --- 6 · plantillas de Meta sin nombre
    for nombre, p in plantillas.items():
        if isinstance(p, dict) and not str(p.get("name", "")).strip():
            criticas.append(f"la plantilla '{nombre}' no tiene name. Un carrito abandonado SIEMPRE "
                            f"cae fuera de la ventana de 24 h: sin plantilla el mensaje NO SALE.")

    # --- 7 · 🔴 el dato de pago, que es el que mueve dinero
    pago = str(plano.get("datos_logisticos.metodo_pago.datos_pago_anticipado", "")).strip()
    anticipado = "si" if es_si(plano.get("datos_logisticos.metodo_pago.anticipado", "")) else "no"
    if pago and not dueno_confirmo:
        criticas.append(
            "datos_pago_anticipado trae contenido y NADIE ha confirmado que sea del dueño de "
            "ESTE espacio. Ese campo lleva medio de pago, nombre y telefono: heredado de otro "
            "espacio, manda el dinero de un cliente a la cuenta de otro, y no da ningun error. "
            "Confirmalo con el dueño y pasa --dueño-confirmo-datos-de-pago.")
    if anticipado == "si" and not pago:
        criticas.append("el pago anticipado esta ACTIVO y datos_pago_anticipado esta vacio: "
                        "el cliente elige anticipado y no hay a donde pagar.")

    # --- 8 · DOCTRINA de los textos (vigente en todos los asistentes del espacio)
    for k in WHATSAPP:
        t = str(plano.get(k, ""))
        if "¿" in t or "¡" in t:
            criticas.append(f"{k} trae signos de apertura (¿ ¡). La doctrina los prohibe en "
                            f"WhatsApp, y si van en un ejemplo el bot los imita aunque la regla diga "
                            f"lo contrario.")
    for k in WHATSAPP[:2]:
        for frase in re.split(r"(?<=[.:;\n])", str(plano.get(k, ""))):
            if re.search(r"emoji", frase, re.I) and not NIEGA.search(frase):
                criticas.append(f"{k} le permite emojis a la IA ('{frase.strip()[:60]}'). "
                                f"Doctrina: la IA NO genera emojis; solo los mensajes FIJOS.")
                break
    for k, t in plano.items():
        if isinstance(t, str) and SIN_CONFIRMAR.search(t):
            avisos.append(f"{k} dice '{SIN_CONFIRMAR.search(t).group(0)}': es una promesa "
                          f"comercial. Solo queda si el DUEÑO la confirmo; si no, es inventada.")
    tr = str(plano.get("datos_logisticos.transportadoras_disponibles", "")).strip().lower()
    if tr.startswith("transportadora"):
        avisos.append("transportadoras_disponibles repite el nombre del campo adentro: gasta "
                      "caracteres de un tope de 100 y empuja al corte lo que va al final.")
    agr = str(plano.get("mensajes_recuperacion.mensaje_agradecimiento", ""))
    if anticipado == "si" and PAGO_AL_RECIBIR.search(agr):
        criticas.append("mensaje_agradecimiento asume pago contra entrega y el anticipado esta "
                        "ACTIVO: ese mensaje sale en TODO pedido confirmado, tambien al que ya pago.")

    # --- 9 · compuerta y envio
    od = str(plano.get("acciones_especiales.origen_datos", "")).strip().lower()
    if od and od != "shopify":
        avisos.append(f"origen_datos es '{od}', no Shopify. No es un error por si solo: confirmar que "
                      f"la tienda esta en esa plataforma y que Chatea recibe sus carritos. Si no los "
                      f"recibe, el asistente NO APLICA en este espacio (no esta 'mal instalado').")
    if str(plano.get("mensajes_recuperacion.posicion_imagen", "")).strip() in ("", "None", "0"):
        criticas.append("posicion_imagen vacia: el mensaje de recuperacion lleva imagen y sin "
                        "posicion valida el envio falla.")
    extra = sorted(set(plano) - esperadas())
    if extra:
        avisos.append(f"llaves que no estan en el molde: {', '.join(extra[:6])}. Revisar a mano: "
                      f"pueden ser datos colados.")

    # --- 10 · configuracion muerta (no es defecto, pero se DECLARA)
    if str(plano.get("datos_tienda.ofrecer_descuento", "")).lower() in ("no",):
        if plano.get("datos_tienda.descuento_maximo") or plano.get("datos_tienda.mensaje_descuento"):
            avisos.append("ofrecer_descuento esta en 'no' pero descuento_maximo y "
                          "mensaje_descuento siguen escritos: es configuracion MUERTA. No hace "
                          "daño, pero en el panel parece activa.")
    return criticas, avisos


def autoprueba():
    """LOS DOS SENTIDOS: que muerda con el defecto y que CALLE con la config sana.
    Un validador que acusa siempre no protege, estorba — y a los tres informes nadie lo abre."""
    base = {
        "onboarding_completed": True,
        "identidad_asistente": {"nombre_asesor": "Ana", "adaptacion_lenguaje": "x" * 400,
                                "metodo_anticancelacion": "y" * 400},
        "datos_tienda": {"nombre_tienda": "T", "ubicacion_tienda": "u", "pais": "colombia",
                         "ofrecer_descuento": "si", "descuento_maximo": "10",
                         "mensaje_descuento": "m"},
        "datos_logisticos": {"tiempos_envio": "2-3 dias",
                             "metodo_pago": {"contraentrega": "si", "anticipado": "no",
                                             "datos_pago_anticipado": ""},
                             "transportadoras_disponibles": "Sin Transportadora X. A y B."},
        "mensajes_recuperacion": {
            "posicion_imagen": 1,
            "carritos": {
                "carritos_mensaje_1": {"name": "p1", "lang": "es", "namespace": "ns",
                                       "status": "APPROVED"},
                "recordatorio_1": {"name": "p2", "lang": "es", "namespace": "ns",
                                   "status": "APPROVED"},
                "recordatorio_2": {"name": "p3", "lang": "es", "namespace": "ns",
                                   "status": "APPROVED"}},
            "tiempo_recordatorio_1": "1 horas", "tiempo_recordatorio_2": "2 horas",
            "tiempo_recordatorio_3": "", "mensaje_agradecimiento": "gracias"},
        "envio_correos": {"activar_envio": "si", "asunto": "a", "contenido": "c"},
        "acciones_especiales": {"subida_automatica": "si", "imagenes_producto": "si",
                                "origen_datos": "shopify"},
    }
    import copy
    fallos, corridas = [], []

    def check(t, ok, ev=""):
        corridas.append(t)
        print(f"  {'OK   ' if ok else 'FALLA'} · {t}")
        if not ok:
            fallos.append(t)
            if ev:
                print(f"         {ev[:200]}")

    c, a = validar(base)
    check("0 · config limpia pasa SIN criticas (control negativo)", not c, str(c))

    d = copy.deepcopy(base); del d["envio_correos"]["asunto"]
    c, _ = validar(d)
    check("1 · llave que falta -> critica", any("faltan" in x for x in c))

    d = copy.deepcopy(base); d["datos_tienda"]["nombre_tienda"] = "{{NOMBRE_TIENDA}}"
    c, _ = validar(d)
    check("2 · marcador sin rellenar -> critica", any("marcadores" in x for x in c))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["transportadoras_disponibles"] = "T" * 132
    c, _ = validar(d)
    check("3 · transportadoras 132/100 -> critica que MUESTRA el corte",
          any("|CORTE|" in x for x in c))

    d = copy.deepcopy(base); d["mensajes_recuperacion"]["tiempo_recordatorio_3"] = "5 horas"
    c, _ = validar(d)
    check("4 · tercer recordatorio con hora y sin plantilla -> critica",
          any("tiempo_recordatorio_3" in x for x in c))

    d = copy.deepcopy(base)
    d["mensajes_recuperacion"]["carritos"]["recordatorio_1"]["name"] = ""
    c, _ = validar(d)
    check("5 · plantilla de Meta sin name -> critica", any("no tiene name" in x for x in c))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["metodo_pago"]["datos_pago_anticipado"] = "Nequi\\nAlguien\\n3001112233"
    c, _ = validar(d)
    check("6 · datos de pago sin confirmar el dueño -> critica", any("dinero" in x for x in c))
    c2, _ = validar(d, dueno_confirmo=True)
    check("6b · REGRESION: con el dueño confirmado, esa critica NO salta",
          not any("dinero" in x for x in c2), str(c2))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["metodo_pago"]["anticipado"] = "si"
    c, _ = validar(d)
    check("7 · anticipado activo y sin datos de pago -> critica",
          any("a donde pagar" in x for x in c))

    d = copy.deepcopy(base); d["datos_tienda"]["ofrecer_descuento"] = "no"
    _, a = validar(d)
    check("8 · descuento apagado con valores escritos -> AVISO, no critica",
          any("MUERTA" in x for x in a))

    d = copy.deepcopy(base); d["datos_tienda"]["nombre_tienda"] = "T" * 90
    c, _ = validar(d)
    check("9 · nombre_tienda 90/80 -> critica que MUESTRA el corte",
          any("|CORTE|" in x for x in c))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["transportadoras_disponibles"] = "Sin X. A, B, C 🚚" + "x" * 83
    c, _ = validar(d)
    check("10 · UTF-16: 99 caracteres con un emoji astral = 100, pasa (el techo NO es defecto)",
          not any("transportadoras" in x for x in c), str(c))
    d["datos_logisticos"]["transportadoras_disponibles"] += "x"
    c, _ = validar(d)
    check("10b · ...y 1 mas = 101 en el panel -> critica", any("|CORTE|" in x for x in c))

    d = copy.deepcopy(base)
    d["identidad_asistente"]["adaptacion_lenguaje"] = "FORMA. Maximo dos emojis por mensaje."
    c, _ = validar(d)
    check("11 · prompt que le permite emojis a la IA -> critica", any("emojis" in x for x in c))
    d["identidad_asistente"]["adaptacion_lenguaje"] = "FORMA. No uses emojis en tus respuestas."
    c, _ = validar(d)
    check("11b · 'No uses emojis' NO dispara (control negativo)",
          not any("emojis" in x for x in c), str(c))

    d = copy.deepcopy(base)
    d["identidad_asistente"]["metodo_anticancelacion"] = "Pregunta: ¿por qué cancelas?"
    c, _ = validar(d)
    check("12 · signo de apertura en un prompt -> critica", any("apertura" in x for x in c))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["tiempos_envio"] = "2-3 dias. Despacho el mismo dia si confirmas antes de las 2."
    _, a = validar(d)
    check("13 · promesa sin confirmar -> AVISO", any("promesa comercial" in x for x in a))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["transportadoras_disponibles"] = "Transportadoras disponibles: A, B."
    _, a = validar(d)
    check("14 · nombre del campo repetido adentro -> AVISO", any("repite el nombre" in x for x in a))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["metodo_pago"].update(anticipado="si", datos_pago_anticipado="Cuenta X")
    d["mensajes_recuperacion"]["mensaje_agradecimiento"] = "Listo. Pagas en efectivo al recibir."
    c, _ = validar(d, dueno_confirmo=True)
    check("15 · agradecimiento que asume contra entrega con anticipado activo -> critica",
          any("asume pago" in x for x in c))
    d["mensajes_recuperacion"]["mensaje_agradecimiento"] = "Listo. Envio gratis a todo el pais."
    c, _ = validar(d, dueno_confirmo=True)
    check("15b · 'envio gratis' con anticipado NO dispara (el anticipo es excepcion)",
          not any("asume pago" in x for x in c), str(c))

    for frase in ["Máx 2 emojis por mensaje.", "Puedes usar emojis con moderación.",
                  "Usa 1 o 2 emojis por respuesta.", "Maximo dos emojis. En quejas no uses emojis."]:
        d = copy.deepcopy(base); d["identidad_asistente"]["adaptacion_lenguaje"] = frase
        c, _ = validar(d)
        check(f"16 · permiso de emojis '{frase[:28]}' -> critica", any("emojis" in x for x in c))

    d = copy.deepcopy(base); d["datos_logisticos"]["tiempos_envio"] = "¿Cuándo? 2-3 dias."
    c, _ = validar(d)
    check("17 · ¿ en tiempos_envio -> critica", any("apertura" in x for x in c))

    for frase in ["Llega mañana garantizado.", "Entrega en 24 horas."]:
        d = copy.deepcopy(base); d["datos_logisticos"]["tiempos_envio"] = frase
        _, a = validar(d)
        check(f"18 · promesa '{frase}' -> AVISO", any("promesa comercial" in x for x in a))

    d = copy.deepcopy(base)
    d["datos_logisticos"]["metodo_pago"].update(anticipado=True, datos_pago_anticipado="Cuenta X")
    d["mensajes_recuperacion"]["mensaje_agradecimiento"] = "Listo. Pagarás cuando llegue."
    c, _ = validar(d, dueno_confirmo=True)
    check("19 · anticipado=True (booleano) + 'pagarás cuando llegue' -> critica",
          any("asume pago" in x for x in c))

    d = copy.deepcopy(base); d["acciones_especiales"]["origen_datos"] = "tiendanube"
    c, a = validar(d)
    check("20 · otra plataforma -> AVISO, nunca critica (la compuerta no asume Shopify)",
          any("origen_datos" in x for x in a) and not any("origen_datos" in x for x in c))
    d["acciones_especiales"]["origen_datos"] = "Shopify"
    c, _ = validar(d)
    check("20b · 'Shopify' con mayuscula NO dispara", not any("origen_datos" in x for x in c))

    d = copy.deepcopy(base); d["mensajes_recuperacion"]["posicion_imagen"] = ""
    c, _ = validar(d)
    check("21 · posicion_imagen vacia -> critica", any("posicion_imagen" in x for x in c))

    d = copy.deepcopy(base); d["datos_tienda"]["telefono_x"] = "3001112233"
    _, a = validar(d)
    check("22 · llave extra -> AVISO", any("no estan en el molde" in x for x in a))

    d = copy.deepcopy(base); d["mensajes_recuperacion"]["tiempo_recordatorio_3"] = "5 horas"
    d["mensajes_recuperacion"]["carritos"]["recordatorio_3"] = {"name": "p4", "lang": "es",
                                                              "namespace": "ns", "status": "APPROVED"}
    c, _ = validar(d)
    check("23 · tiempo_recordatorio_3 con valor aunque haya plantilla -> critica",
          any("tiempo_recordatorio_3" in x for x in c))

    check("24 · u16 compartida: un emoji astral vale 2", u16("🚚") == 2 and u16("á") == 1)

    TOTAL = len(corridas)
    print(f"\n  COBERTURA: {TOTAL - len(fallos)} de {TOTAL} pruebas en verde")
    return 0 if not fallos else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="entrada")
    p.add_argument("--autoprueba", action="store_true")
    p.add_argument("--dueño-confirmo-datos-de-pago", dest="dueno", action="store_true")
    a = p.parse_args()

    if a.autoprueba:
        sys.exit(autoprueba())
    if not a.entrada:
        p.error("hace falta --in o --autoprueba")

    with open(a.entrada, encoding="utf-8") as f:
        d = json.load(f)
    criticas, avisos = validar(d, a.dueno)

    print(f"[Carritos] Configuracion · {escapado(d)} escapados de "
          f"{BOT['legacy_json_escapado']}")
    for c in criticas:
        print(f"  🔴 {c}")
    for v in avisos:
        print(f"  🟠 {v}")
    if not criticas and not avisos:
        print("  sin criticas ni avisos. NO significa que este BIEN configurado: significa que "
              "pasa los controles que este validador sabe mirar.")
    sys.exit(1 if criticas else 0)


if __name__ == "__main__":
    main()
