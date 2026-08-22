#!/usr/bin/env python3
"""Arma el informe diario en Markdown-Golden, listo para build_pdf.py.

REGLA QUE ORIGINÓ ESTE ARCHIVO: toda frase con veredicto sale de una VARIABLE.
Nunca de un literal. Una versión llevaba escrita a mano la frase "hoy no hay
discrepancias" y era falsa.

REGLA QUE ORIGINÓ SU TERCERA VERSIÓN (13b): una variable vacía no basta. Cada
`if not X:` responde DOS preguntas: si está vacío porque no hay nada, o porque no
se pudo mirar. Un contador que no las distingue es la misma mentira, en código.

FORMA QUE ORIGINÓ SU CUARTA VERSIÓN (enmienda del Centro, 2026-08-10): **corto**.
FER tuvo dos informes del mismo día en el Escritorio, uno de 2 páginas y otro de 6,
y conservó el de 2. A las siete de la mañana necesita ACCIONES, no cobertura. De ahí
la regla estructural de este archivo: **una sección es un BLOQUE solo cuando TIENE
hallazgos; cuando no, no aparece.** La cobertura no desaparece — la ley del cero
honesto no se negocia — pero se va al final y ocupa una tabla, no media hoja.

  python3 generar_informe_diario.py --config config.json --decisiones decisiones.json \\
      --salida informe.md [--chatea contactos.json] [--embudo embudo.json]
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json
from comun import (contacto_de, tel10, miles, miles_seguro, pesos, nom_de,
                   huella_txt, concuerda, preparar_destino_pdf, marcar_como_propio,
                   avisar_banderas, guias_por_corregir, ventana_accionable,
                   se_puede_reasignar, aviso_default_bodega, recortar)
from cruzar_chat_orden import cruzar, uf  # noqa: E402

# LOS ESTADOS SON POR CUENTA, NO POR CODIGO.
# Medido: la cuenta de Dolce tiene 15 estados y NO tiene GUIA_GENERADA; la de Golden
# tiene ~28 y SI lo tiene. Quemar la lista aqui garantiza que la segunda tienda que
# use la skill pierda pedidos en silencio. Estos son los VALORES POR DEFECTO — el
# config los pisa con 'estados' cuando la cuenta trae otros.
ESTADOS_POR_DEFECTO = {
    "ya_salio": ["PREPARADO PARA TRANSPORTADORA", "DESPACHADA", "EN REPARTO",
                 "EN TERMINAL DESTINO", "EN BODEGA DESTINO", "GUIA_GENERADA"],
    "novedad": ["NOVEDAD"],
    "resuelta": ["NOVEDAD SOLUCIONADA"],
    "oficina": ["RECLAME EN OFICINA"],
    "modificables": ["PENDIENTE", "PENDIENTE CONFIRMACION", "PREPARADO PARA TRANSPORTADORA"],
    "quietos": ["PENDIENTE", "PENDIENTE CONFIRMACION"],
    # Pasado este punto el paquete ya no se reasigna: se llama, no se mueve.
    "ya_no_se_reasigna": ["EN REPARTO", "EN TERMINAL DESTINO", "EN BODEGA DESTINO"],
}

# AQUI VIVIA `tel_de(o)` Y SE MURIO CON EVIDENCIA.
# Devolvia "57" + los ultimos 10 digitos SIN mirar si habia digitos: con `phone` vacio
# imprimia "57" pelado, que es el bug que este expediente lleva tres rondas persiguiendo.
# Se arreglo `contacto_de` en la tabla estrella (ronda 12), luego en tres tablas mas
# (ronda 13)... y estos OCHO sitios seguian llamando a la funcion vieja. Dos funciones
# para la misma pregunta son dos respuestas en cuanto alguien corrige una.
# Ahora hay UNA, en `comun.py`, y el banco comprueba que no renazca ninguna copia.
#
# (Nota del que lo arreglo: el barrido que sustituyo `tel_de(` por `contacto_de(` tambien
# reescribio ESTE COMENTARIO, que quedo diciendo que aqui vivia contacto_de. Un
# reemplazo global no distingue codigo de prosa. Es la tercera vez en dos rondas que el
# barrido a ciegas hace algo que yo no pedi, y por eso todo barrido se relee.)

ROJO, AMARILLO, VERDE = "🔴", "🟡", "🟢"

DIR_OFICINA = re.compile(r"oficina|recoge|reclama|sucursal|agencia", re.I)


def dir_mala(d):
    d = (d or "").strip()
    if DIR_OFICINA.search(d):      # recoger en oficina es una modalidad, no un defecto
        return None
    if re.search(r"cual es la direccion|^\s*(nn|xx|na|no se|nose)\s*$", d, re.I):
        return "el cliente nunca dio la direccion"
    if len(d) < 12:
        return "demasiado corta para repartir"
    if not re.search(r"\d", d):
        return "sin numero de casa ni de calle"
    return None


def revisar_paso0(o, d, ya_no_se_reasigna=()):
    """Dice si este pedido que ya salió va bien o hay que frenarlo.

    Pregunta por TODOS los estados de decisión, no solo por "hay que cambiar". Antes,
    un pedido sin decisión salía "va bien" aquí y "la bodega no despacha" más abajo.
    """
    if d is None:
        return True, "no tiene decision calculada: revisalo a mano"
    rec = d.get("rec")
    if rec == "CAMBIAR":
        if o["status"] in ya_no_se_reasigna:
            return True, f"va mal, pero ya esta {o['status'].lower()}: llama, no reasignes"
        return True, d.get("motivo") or "hay que cambiar la transportadora"
    if rec == "SIN COBERTURA":
        return True, d.get("motivo") or "no hay con que decidir su transportadora"
    if rec == "ASIGNAR":
        return True, "salio sin transportadora asignada"
    if rec == "DEJAR":
        return False, "va bien"
    return True, f"estado de decision no previsto: {rec}"


def partir(texto, ancho=70):
    """Un mensaje copiable jamás se trunca: se parte sin cortar palabras."""
    palabras, linea, out = (texto or "").split(), "", []
    for p in palabras:
        if len(linea) + len(p) + 1 > ancho:
            out.append(linea); linea = p
        else:
            linea = f"{linea} {p}".strip()
    if linea:
        out.append(linea)
    return out or [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--decisiones", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--chatea")
    ap.add_argument("--embudo")
    ap.add_argument("--fecha", default="")
    ap.add_argument("--pdf", metavar="RUTA",
                    help="genera tambien el PDF con golden-pdf-check. REGLA DE FER: el informe "
                         "diario SIEMPRE se entrega en PDF al Escritorio, no solo en Markdown.")
    ap.add_argument("--mensajes", help="ruta del ANEXO con los mensajes para copiar. "
                    "Van aparte porque ocupaban el 42%% del informe y no se leen a las 7am: "
                    "se abren cuando toca escribirle a alguien.")
    a = ap.parse_args()

    # EL ANEXO SE LLAMA COMO EL INFORME, Y VIVE A SU LADO.
    # El informe citaba `basename(--mensajes)`, o sea el nombre que le pasara quien lo
    # corriera. En la corrida de fabrica ese nombre era un temporal, asi que el
    # entregable quedo citando un anexo `zSm.md` **que no existe en ninguna parte**:
    # un documento que manda al lector a un archivo inventado. El nombre se DERIVA del
    # entregable, que es lo unico que el lector tiene en la mano.
    if not a.mensajes:
        base = os.path.splitext(os.path.abspath(a.salida))[0]
        a.mensajes = base + "-mensajes.md"

    cfg = leer_json(a.config)
    avisar_banderas(cfg, a.config)
    E = dict(ESTADOS_POR_DEFECTO)
    E.update(cfg.get("estados") or {})
    YA_SALIO, NOVEDAD, RESUELTA = E["ya_salio"], E["novedad"], E["resuelta"]
    OFICINA, MODIFICABLES, QUIETOS = E["oficina"], E["modificables"], E["quietos"]
    YA_NO_SE_REASIGNA = set(E["ya_no_se_reasigna"])
    D = leer_json(cfg["dropi"])
    X = leer_json(a.decisiones)
    ords = D.get("ordenes") or []
    # LA VENTANA SALE DE UN SOLO SITIO Y DICE DE DONDE VIENE.
    # Aqui vivia `if acc:` sobre un campo opcional, y con el volcado oficial (que trae
    # `accionables: null` a proposito) el filtro NO disparaba: el informe barria la
    # cuenta entera y sacaba 124 «direcciones malas», 120 de ellas de pedidos ya
    # cerrados. Con la ventana derivada son 4.
    acc, origen_ventana = ventana_accionable(D)
    ords = [o for o in ords if o["id"] in acc]
    dec = {x["id"]: x for x in X}
    tienda = cfg.get("tienda", "la tienda")

    if D.get("cosecha_completa") is not True and not cfg.get("aceptar_cosecha_incompleta"):
        sys.exit("COSECHA NO CONFIABLE: " + (D.get("motivo_corte") or
                 "el volcado no declara si quedo completa") +
                 ". No se imprime un informe que parece entero sin serlo.")

    conocidos = set(YA_SALIO) | set(NOVEDAD) | set(RESUELTA) | set(OFICINA) | set(QUIETOS)
    vistos = {o["status"] for o in ords}
    nuevos = sorted(vistos - conocidos)

    salio = [o for o in ords if o["status"] in YA_SALIO]
    nov = [o for o in ords if o["status"] in NOVEDAD]
    resueltas = [o for o in ords if o["status"] in RESUELTA]
    ofi = [o for o in ords if o["status"] in OFICINA]
    quietos = [o for o in ords if o["status"] in QUIETOS]
    dirs = [(o, m) for o in ords if (m := dir_mala(o.get("dir")))]

    frenar = []
    for o in salio:
        hay, motivo = revisar_paso0(o, dec.get(o["id"]), YA_NO_SE_REASIGNA)
        if hay:
            frenar.append((o, motivo))

    # ------------------------------------------------------------------
    # LAS GUIAS YA GENERADAS SON EL PASO 1 DEL INFORME. Dictado por FER el 2026-08-11.
    #
    # No es "una seccion mas arriba": es la unica ventana que se cierra sola. Mientras
    # el paquete no salga fisicamente, una guia mala TODAVIA se cambia; en cuanto sale,
    # lo unico que queda es llamar. Un pedido que ya se movio y uno que solo tiene guia
    # generada piden dos cosas distintas del lector, y meterlos en la misma tabla hace
    # que el segundo se lea con la resignacion del primero.
    #
    # La linea que los separa ya existia y estaba bien puesta: `ya_no_se_reasigna`. Lo
    # que faltaba era imprimirla. Y va con LA PLATA EN JUEGO, porque una seccion que
    # pide trabajo sin decir cuanto vale se pospone.
    # La lista sale de la definicion UNICA (comun.guias_por_corregir), que mira la
    # guia y no el estado. Aqui solo se casa con el motivo que ya calculo el paso 0.
    #
    # Y LA LISTA NO SE CRUZA CON `frenar`, que es lo que hice primero y volvia a partir
    # la cifra: `frenar` solo recorre los estados de «ya salio», asi que un pedido en
    # NOVEDAD **con guia generada** se caia de la seccion. La guia no la define el
    # estado — la define el campo `guia`. Cruzarla con `frenar` dejaba 13 donde el 360
    # imprimia 19, con la misma plata debajo: dos cifras en el mismo paquete otra vez.
    _porcorregir, plata_guia = guias_por_corregir(X, E["ya_no_se_reasigna"])
    _ids_guia = {d["id"] for d in _porcorregir}
    _por_id = {o["id"]: o for o in ords}
    _motivo_frenar = {o["id"]: m for o, m in frenar}
    frenar_guia = [(_por_id[d["id"]],
                    _motivo_frenar.get(d["id"], d.get("motivo") or d.get("rec")))
                   for d in _porcorregir if d["id"] in _por_id]
    frenar_camino = [(o, m) for o, m in frenar if o["id"] not in _ids_guia]


    cambios, cambios_caros = [], []
    for x in X:
        if x["rec"] != "CAMBIAR":
            continue
        act = [c for c in x.get("cands", []) if c["t"] == x["actual"]]
        if act and x.get("elegida") and act[0]["costo"] < x["elegida"]["costo"]:
            cambios_caros.append(x)
        else:
            cambios.append(x)
    ids_quietos = {o["id"] for o in quietos}
    cambios_quietos = [x for x in cambios if x["id"] in ids_quietos]
    sinc = [x for x in X if x["rec"] == "SIN COBERTURA"]
    asignar = [x for x in X if x["rec"] == "ASIGNAR"]
    sin_decision = [o for o in ords if o["id"] not in dec]
    tuyos = len(sinc) + len(cambios_caros) + len(asignar) + len(sin_decision)

    if not a.chatea:
        cruce = {"estado": "NO_CORRIDO", "razon": "no se paso el volcado de Chatea"}
    elif not any(o.get("lineas") for o in ords):
        cruce = {"estado": "NO_CORRIDO",
                 "razon": "el volcado de Dropi no trae lineas de producto"}
    else:
        cruce = {"estado": "CORRIDO",
                 **cruzar(ords, leer_json(a.chatea), MODIFICABLES,
                         cfg.get("opciones_no_producto"))}

    if not a.embudo:
        embudo = {"estado": "NO_CORRIDO", "razon": "no se paso el volcado del embudo"}
    elif not os.path.exists(a.embudo):
        embudo = {"estado": "NO_CORRIDO", "razon": f"no existe {a.embudo}"}
    else:
        embudo = {"estado": "CORRIDO", **leer_json(a.embudo)}

    no_cuadran = cruce.get("disc") or []      # discrepancias de verdad
    contra = cruce.get("banderas") or []       # campos peleados: cuarentena, no veredicto

    # ------------------------------------------------------------------
    # LA TABLA DE ACCIONES. Es lo primero y, muchos días, lo único que hay
    # que leer. Cada fila lleva la ACCIÓN, no la observación.
    # ------------------------------------------------------------------
    filas = []

    def fila(sem, cuantos, que, accion):
        filas.append(f"| {sem} | **{cuantos}** | {que} | {accion} |")

    if frenar_guia:
        fila(ROJO, len(frenar_guia),
             "con guia ya generada y mal puesta"
             + (f" · {pesos(plata_guia)} en juego" if plata_guia else ""),
             "corrigelo en Dropi, el paquete todavia no sale")
    if frenar_camino:
        fila(ROJO, len(frenar_camino), "ya salieron y van mal",
             "llama a la bodega antes de que salga el camion")
    if nov:
        fila(ROJO, len(nov), "en novedad", "escribe hoy, el mensaje esta abajo")
    if no_cuadran:
        fila(ROJO, len(no_cuadran), "no coinciden con lo que pidio el cliente",
             "corrige en Dropi antes de despachar")
    if contra:
        fila(ROJO, len(contra), "los campos de Chatea se contradicen",
             "abre la conversacion: los campos no deciden")
    if ofi:
        fila(AMARILLO, len(ofi), "esperando en la oficina",
             "avisale al cliente o se devuelve")
    if cambios_quietos:
        fila(AMARILLO, len(cambios_quietos), "conviene cambiarles la transportadora",
             "cambialo en Dropi, todavia es gratis")
    if dirs:
        fila(AMARILLO, len(dirs), "con direccion inservible",
             "pide la direccion, el mensaje esta abajo")
    if embudo["estado"] == "CORRIDO" and embudo.get("fuga"):
        fila(AMARILLO, embudo["fuga"], "vendieron por WhatsApp y no hay orden",
             "subelos a Dropi")
    if tuyos:
        fila(AMARILLO, tuyos, "el calculo no alcanza", "decides tu, estan al final")

    rendido = set()          # ids que el informe SI imprime con una accion
    L = []
    A = L.append
    A(f"""---
title: {tienda} · que hago hoy
subtitle: {a.fecha or D.get('generado','')[:10]} · {len(ords)} pedidos vivos
kicker: Logistica diaria
author: Golden Group
---
""")
    if filas:
        A("| | | Que pasa | Que hago |")
        A("| --- | --- | --- | --- |")
        for f in filas:
            A(f)
        A("")
        A("En orden: lo de arriba se pierde hoy si no lo tocas, lo de abajo aguanta.\n")
    else:
        A(f"## {VERDE} Hoy no hay nada que hacer\n")
        A(f"Los {len(ords)} pedidos vivos van como deben. Al final dice que se reviso "
          "para llegar a esa conclusion.\n")

    # ------------------------------------------------------------------
    # LOS BLOQUES. Solo aparece el que TIENE algo. Nada de secciones vacias.
    # ------------------------------------------------------------------
    def _bloque_salio(titulo, grupo, cola):
        _filas = []
        for o, motivo in sorted(grupo, key=lambda z: -float(z[0].get("total") or 0)):
            rendido.add(o["id"])
            d = dec.get(o["id"]) or {}
            e = d.get("elegida")
            destino = e["t"] if e and o["status"] not in YA_NO_SE_REASIGNA else "decides tu"
            _filas.append(
                f"| {contacto_de(o)} | {nom_de(o)[:18]} | "
                f"{(o.get('city') or '')[:12]} | {o.get('carrier') or 'ninguna'} | "
                f"**{destino}** | {motivo} |")
        A(titulo)
        A("| WhatsApp | Cliente | Ciudad | Va por | Pasar a | Por que |")
        A("| --- | --- | --- | --- | --- | --- |")
        for _f in _filas:
            A(_f)
        A(cola)

    # PASO 1 DEL DIA: las que todavia se alcanzan a corregir.
    if frenar_guia:
        _bloque_salio(
            f"## {ROJO} Paso 1 · Guias ya generadas que hay que corregir · "
            f"{len(frenar_guia)}"
            + (f" · {pesos(plata_guia)} en juego" if plata_guia else "") + "\n",
            frenar_guia,
            "\nEstas van primero porque son las unicas que todavia se cambian solas: "
            "el paquete no ha salido. Manana ya no.\n")

    if frenar_camino:
        _bloque_salio(f"## {ROJO} Llama a la bodega · {len(frenar_camino)}\n", frenar_camino,
                      f"\nLos otros {len(salio) - len(frenar)} que ya salieron van bien.\n")

    # Las novedades y las "solucionadas" TAMBIEN llevan su decision de transportadora.
    # Antes se armaban por estado y nunca cruzaban con el motor: tres pedidos en
    # "novedad solucionada" iban por transportadora que la bodega NO despacha y
    # desaparecian bajo el literal "siguen su curso".
    en_novedad = nov + resueltas
    if en_novedad:
        A(f"## {ROJO} Novedades · {len(nov)} sin resolver"
          + (f" y {len(resueltas)} ya solucionadas" if resueltas else "") + "\n")
        A("| WhatsApp | Cliente | Ciudad | Valor | Va por | Decision | Cliente |")
        A("| --- | --- | --- | --- | --- | --- | --- |")
        for o in sorted(en_novedad, key=lambda z: -float(z.get("total") or 0)):
            d = dec.get(o["id"]) or {}
            e = d.get("elegida")
            _se_puede, _porque = se_puede_reasignar(o)
            if d.get("rec") == "CAMBIAR" and not _se_puede:
                # NUNCA «pasar a X» a un paquete que ya se movio. Dictado por FER:
                # un informe que propone lo imposible invita al error. Medido: los 5
                # pedidos en NOVEDAD tenian guia y 3 llevaban «pasar a otra».
                accion = f"**llama a la bodega** · {_porque}"
                rendido.add(o["id"])
            elif d.get("rec") == "CAMBIAR":
                accion = f"**pasar a {e['t']}**" if e else "**cambiar**"
                rendido.add(o["id"])
            elif d.get("rec") in ("SIN COBERTURA", "ASIGNAR"):
                accion = f"**{d['rec'].lower()}**"
                rendido.add(o["id"])
            elif not d:
                accion = "**sin decision**"
            else:
                accion = "sigue igual"
            est = "solucionada" if o["status"] in RESUELTA else "sin resolver"
            A(f"| {contacto_de(o)} | {nom_de(o)[:16]} | {(o.get('city') or '')[:12]} | "
              f"{pesos(o.get('total'))} | {o.get('carrier')} | {accion} · {est} | "
              f"{huella_txt(D, o)} |")
        A("")

    if no_cuadran or contra:
        rot = []
        if no_cuadran:
            rot.append(f"{len(no_cuadran)} no coinciden")
        if contra:
            rot.append(f"{len(contra)} sin poder juzgar")
        A(f"## {ROJO} Lo que pidio el cliente contra lo cargado · {' y '.join(rot)}\n")
        for x in no_cuadran:
            # SIN COMILLAS INVERTIDAS EN LOS IDs. `golden-pdf-check` clasifica el
            # monoespaciado como "bloque de prompt copiable" y avisa cuando uno queda
            # pegado al borde inferior — que es lo que tumbaba el PDF a REQUIERE
            # ARREGLO. Estos no son prompts: son numeros de pedido. El estilo de codigo
            # les daba un significado que no tienen, y ese significado tiene reglas de
            # maquetacion detras.
            #
            # RESERVA, MEDIDA EL 2026-08-11 Y ESCRITA AQUI PORQUE ES DONDE SE LEE:
            # la FAMILIA esta confirmada — el aviso del auditor sale de `risk_mono`, o
            # sea de tramos monoespaciados cerca del borde (control positivo). Pero la
            # SUB-CAUSA del caso concreto **NO esta discriminada**: al reintroducir las
            # comillas invertidas el PDF ya NO vuelve a fallar, asi que no se puede
            # afirmar que fueran ellas y no el desplazamiento de paginacion. Yo lo conte
            # como causa probada y no lo era. Que el sintoma desaparezca no prueba que
            # la causa fuera la que uno dijo.
            A(f"**{x['tel']} · {x['cliente']} · pedido {x['orden']}** · {x['ciudad']} · "
              f"{x['status']}\n")
            A(f"- Pidio: {x['chat']}")
            A(f"- Quedo: {x['dropi']}")
            for f in x["fallos"]:
                A(f"- **{f['tipo']}:** el chat dice {f['chat']} y Dropi tiene {f['dropi']}")
            A("")
        for x in contra:
            # SIN COMILLAS INVERTIDAS EN LOS IDs. `golden-pdf-check` clasifica el
            # monoespaciado como "bloque de prompt copiable" y avisa cuando uno queda
            # pegado al borde inferior — que es lo que tumbaba el PDF a REQUIERE
            # ARREGLO. Estos no son prompts: son numeros de pedido. El estilo de codigo
            # les daba un significado que no tienen, y ese significado tiene reglas de
            # maquetacion detras.
            #
            # RESERVA, MEDIDA EL 2026-08-11 Y ESCRITA AQUI PORQUE ES DONDE SE LEE:
            # la FAMILIA esta confirmada — el aviso del auditor sale de `risk_mono`, o
            # sea de tramos monoespaciados cerca del borde (control positivo). Pero la
            # SUB-CAUSA del caso concreto **NO esta discriminada**: al reintroducir las
            # comillas invertidas el PDF ya NO vuelve a fallar, asi que no se puede
            # afirmar que fueran ellas y no el desplazamiento de paginacion. Yo lo conte
            # como causa probada y no lo era. Que el sintoma desaparezca no prueba que
            # la causa fuera la que uno dijo.
            A(f"**{x['tel']} · {x['cliente']} · pedido {x['orden']}** · {x['ciudad']} · "
              f"{x['status']}\n")
            A(f"- **Chatea se contradice a si mismo:** el campo de cantidad dice {x['campo']} "
              f"y el texto del pedido dice {x['texto']}. En Dropi hay {x['en_dropi']}.")
            A(f"- Pidio, segun el texto: {x['chat']}")
            A(f"- **{x['que_hacer'].capitalize()}.** Esto NO es una discrepancia confirmada: "
              "es una que no se puede juzgar desde los campos.")
            A("")

    if ofi:
        A(f"## {AMARILLO} Esperando en la oficina · {len(ofi)}\n")
        A("| WhatsApp | Cliente | Ciudad | Valor | Va por | Decision |")
        A("| --- | --- | --- | --- | --- | --- |")
        for o in ofi:
            d = dec.get(o["id"]) or {}
            e = d.get("elegida")
            if d.get("rec") and d["rec"] != "DEJAR":
                accion = f"**{d['rec'].lower()}" + (f" a {e['t']}**" if e and d["rec"] == "CAMBIAR" else "**")
                rendido.add(o["id"])
            else:
                accion = "sigue igual"
            A(f"| {contacto_de(o)} | {nom_de(o)[:16]} | {(o.get('city') or '')[:12]} | "
              f"{pesos(o.get('total'))} | {o.get('carrier')} | {accion} |")
        A("")

    if cambios_quietos:
        A(f"## {AMARILLO} Cambiar transportadora · {len(cambios_quietos)}\n")
        # EL DEFAULT DE LA BODEGA, DECLARADO. Va aqui y no al final porque es
        # justo esta seccion la que puede parecer que contradice al panel.
        _av = aviso_default_bodega(cfg)
        if _av:
            A(_av + "\n")
        A("Todavia no tienen guia, asi que el cambio es gratis. **Entrega** es cuanto entrega "
          "esa transportadora en ese municipio.\n")
        A("| WhatsApp | Cliente | Ciudad | Hoy | Pasar a | Flete | Entrega |")
        A("| --- | --- | --- | --- | --- | --- | --- |")
        for x in sorted(cambios_quietos, key=lambda z: -z["total"]):
            rendido.add(x["id"])
            e = x["elegida"]
            A(f"| {contacto_de(x)} | {x['cliente'][:16]} | {(x['ciudad'] or '')[:12]} | "
              f"{x['actual']} | **{e['t']}** | {pesos(e['flete'])} | {e['pct_muni']}% |")
        A("")

    if dirs:
        A(f"## {AMARILLO} Direcciones que no sirven · {len(dirs)}\n")
        A("| WhatsApp | Cliente | Ciudad | Que le pasa |")
        A("| --- | --- | --- | --- |")
        for o, m in dirs:
            A(f"| {contacto_de(o)} | {nom_de(o)[:16]} | {(o.get('city') or '')[:12]} | "
              f"{m} |")
        A("")

    if embudo["estado"] == "CORRIDO" and embudo.get("lista"):
        A(f"## {AMARILLO} Vendieron por WhatsApp y no hay orden · {embudo['fuga']}\n")
        A("| WhatsApp | Cliente | Ciudad | Pidio | Ultima vez |")
        A("| --- | --- | --- | --- | --- |")
        _visE, _notaE = recortar(embudo["lista"], 25)
        for e in _visE:
            A(f"| {contacto_de(e)} | {(e.get('nombre') or '').strip()[:16]} | "
              f"{e.get('ciudad','')[:12]} | {(e.get('productos') or '')[:28]} | "
              f"{str(e.get('ult'))[:10]} |")
        if len(embudo["lista"]) > 25:
            A("")
            A(_notaE)
        A("")

    if tuyos:
        A(f"## {AMARILLO} Decides tu · {tuyos}\n")
        A("| WhatsApp | Cliente | Ciudad | Situacion |")
        A("| --- | --- | --- | --- |")
        for x in sinc:
            rendido.add(x["id"])
            A(f"| {contacto_de(x)} | {x['cliente'][:16]} | {(x['ciudad'] or '')[:12]} | "
              f"{x['motivo']} |")
        for x in asignar:
            rendido.add(x["id"])
            A(f"| {contacto_de(x)} | {x['cliente'][:16]} | {(x['ciudad'] or '')[:12]} | "
              "salio sin transportadora asignada |")
        for x in cambios_caros:
            rendido.add(x["id"])
            A(f"| {contacto_de(x)} | {x['cliente'][:16]} | {(x['ciudad'] or '')[:12]} | "
              f"dejarlo en {x['actual']} sale mejor que moverlo |")
        for o in sin_decision:
            A(f"| {contacto_de(o)} | {nom_de(o)[:16]} | {(o.get('city') or '')[:12]} | "
              "**el motor no lo devolvio** |")
        A("")

    # ---------------- mensajes: en ANEXO aparte ----------------
    # Medido: las tarjetas de mensaje eran 91 de 217 lineas del informe, el 42%. Nadie
    # las lee a las siete de la manana; se abren cuando toca escribirle a alguien. Van
    # a su propio archivo y el informe solo dice donde estan.
    M = []
    B = M.append
    if nov or ofi or dirs:
        B(f"""---
title: {tienda} · mensajes del dia
subtitle: {a.fecha or D.get('generado','')[:10]} · para copiar y pegar en WhatsApp
kicker: Logistica diaria
author: Golden Group
---
""")
        B("Sin signos de apertura, para que se peguen tal cual.\n")
        for o in nov:
            B(f"**{contacto_de(o)} · {nom_de(o)}**\n")
            B("```")
            B(f"Hola {o.get('name','')}, le escribimos de {tienda} por su pedido.")
            B("La transportadora reporto una novedad y queremos resolverla hoy mismo.")
            B("Nos confirma si esta direccion esta bien?")
            for t in partir(o.get("dir") or ""):
                B(t)
            B("```\n")
        for o in ofi:
            B(f"**{contacto_de(o)} · {nom_de(o)}**\n")
            B("```")
            B(f"Hola {o.get('name','')}, su pedido de {tienda} ya llego a la oficina")
            B(f"de {o.get('carrier','la transportadora')} en {o.get('city','')} y la esta "
              "esperando.")
            B("Puede pasar a recogerlo cuando le quede facil.")
            B("Si se le dificulta ir, nos avisa y vemos como se lo hacemos llegar.")
            B("```\n")
        for o, m in dirs:
            B(f"**{contacto_de(o)} · {nom_de(o)}**\n")
            B("```")
            B(f"Hola {o.get('name','')}, le escribimos de {tienda}.")
            B(f"Ya tenemos su pedido listo para {o.get('city','')}, pero con la direccion")
            B("que quedo registrada el mensajero no logra llegar.")
            B("Nos puede confirmar calle, numero y un punto de referencia?")
            B("```\n")

    if M and a.mensajes:
        escribir_texto(a.mensajes, "\n".join(M))
        A(f"Los mensajes para escribirle a esas {len(nov) + len(ofi) + len(dirs)} personas "
          f"estan en el anexo `{os.path.basename(a.mensajes)}`.\n")
    elif M:
        A("**Los mensajes no se generaron**: no se paso `--mensajes` con la ruta del anexo.\n")

    # ---------------- cobertura: al final, compacta, obligatoria ----------------
    A("## Que se reviso\n")
    # DE DONDE SALIO LA VENTANA. Va aqui porque el lector no puede distinguir un
    # informe corto «porque hoy hay poco» de uno corto «porque el filtro se aplico
    # sobre el conjunto equivocado» — y el dia que el volcado no declare accionables,
    # la skill los deduce y tiene que decirlo.
    A(f"Los pedidos de hoy salieron asi: **{origen_ventana}**.\n")
    A("| Revision | De | Se miro | Ciego |")
    A("| --- | --- | --- | --- |")
    # LA COSECHA NO DEFINE SU PROPIO UNIVERSO. Dropi declara cuantas ordenes tiene la
    # cuenta (`total_ordenes_cuenta`); si el volcado trajo menos, esa resta es una zona
    # ciega y va escrita. Medirse contra lo que uno mismo bajo siempre da cobertura
    # perfecta — y el config de esta tienda ya ORDENA por escrito declarar las que
    # faltan, no callarlas.
    # LA FILA NO SE OMITE NUNCA. Antes solo aparecia cuando habia diferencia, asi que
    # "sin zona ciega" y "no se pudo medir la zona ciega" se veian igual: sin fila. Y el
    # arreglo se habia aplicado solo al informe 360 — el gemelo se quedo sin el, que es
    # la clase que este expediente lleva tres rondas persiguiendo. Todo arreglo va a los
    # DOS generadores o no se declara hecho.
    _tot_cta = D.get("total_ordenes_cuenta")
    _bajadas = len(D.get("ordenes") or [])
    _ciego_ord = max(0, _tot_cta - _bajadas) if _tot_cta else 0
    if _tot_cta:
        A(f"| Ordenes de la cuenta | {miles(_tot_cta)} declara Dropi | {miles(_bajadas)} "
          f"bajadas | "
          + (f"**{miles(_ciego_ord)} sin bajar**" if _ciego_ord else "0") + " |")
    else:
        A(f"| Ordenes de la cuenta | **no declarado** | {miles(_bajadas)} bajadas | "
          f"**no se puede medir: el volcado no dice cuantas tiene la cuenta** |")
    A(f"| Pedidos vivos | {miles(_bajadas)} de la tienda | {miles(len(ords))} | 0 |")
    A(f"| Transportadora | {len(ords)} | {len(X)} | {len(ords) - len(X)} |")
    A(f"| Costo y utilidad | {len(ords)} | {sum(1 for o in ords if o.get('tiene_detalle'))} | "
      f"{sum(1 for o in ords if not o.get('tiene_detalle'))} |")
    if cruce["estado"] == "CORRIDO":
        # Ausente no es cero: si el cruce no reporto contradicciones es que no las midio.
        cuar = cruce["campos_contradictorios"] if "campos_contradictorios" in cruce else None
        A(f"| Cantidad contra el chat | {cruce['modificables']} modificables | "
          f"{cruce['comparadas_cantidad']} | {cruce['sin_dato_cantidad']} sin dato"
          + (f" + {cuar} en cuarentena" if cuar else "") + " |")
        A(f"| Color contra el chat | idem | {cruce['comparadas_color']} | "
          f"{cruce['sin_dato_color']} sin nota de color"
          + (f" + {cuar} en cuarentena" if cuar else "") + " |")
    else:
        A(f"| Chat contra la orden | {len(ords)} | **0** | **todos: {cruce['razon']}** |")
    if embudo["estado"] == "CORRIDO":
        A(f"| Embudo de WhatsApp | {embudo['pedidos']} contactos | {embudo['revisados']} | "
          f"{embudo['sin_respuesta'] if 'sin_respuesta' in embudo else '**no declarado**'} |")
    else:
        A(f"| Embudo de WhatsApp | ? | **0** | **todo: {embudo['razon']}** |")
    A(f"| Direcciones | {len(ords)} | {len(ords)} | 0 |")
    A("")

    if nuevos:
        A(f"**Aparecieron {len(nuevos)} estados que esta configuracion no conoce:** "
          + ", ".join(f"`{x}`" for x in nuevos) +
          ". Los pedidos que esten ahi no entran en ninguna seccion por estado; si alguno "
          "lleva decision, sale arriba en «sin seccion asignada». Hay que agregarlos a "
          "`estados` en el config de esta tienda.\n")

    # La lista de ciegos empieza por lo mas grande, que estaba fuera: las ordenes que
    # Dropi declara y la cosecha no bajo. El informe llego a decir "no hubo zonas
    # ciegas" con 322 declaradas en su propia tabla de arriba.
    ciegos = []
    if _ciego_ord:
        ciegos.append(f"**{miles(_ciego_ord)} ordenes** que Dropi declara y la cosecha no bajo")
    if cruce["estado"] == "CORRIDO":
        if cruce["sin_dato_color"]:
            ciegos.append(f"el color de **{cruce['sin_dato_color']} pedidos**, porque la orden "
                          "no trae la nota donde Dropi lo escribe")
        if cruce["sin_dato_cantidad"]:
            ciegos.append(f"la cantidad de **{cruce['sin_dato_cantidad']} pedidos**, porque el "
                          "chat no guardo el numero")
        if cruce["saltadas"]:
            ciegos.append(f"**{len(cruce['saltadas'])} pedidos** sin ficha de chat que mirar")
        if cruce.get("campos_contradictorios"):
            ciegos.append(f"**{cruce['campos_contradictorios']} pedidos en cuarentena**, donde "
                          "los campos de Chatea se contradicen y solo la conversacion decide")
    else:
        ciegos.append(f"**el cruce entero**: {cruce['razon']}")
    if embudo["estado"] == "CORRIDO" and embudo.get("sin_respuesta"):
        ciegos.append(f"**{embudo['sin_respuesta']} contactos** que no respondieron")
    elif embudo["estado"] != "CORRIDO":
        ciegos.append(f"**el embudo entero**: {embudo['razon']}")
    if ciegos:
        A("**No se dio por bueno lo que no se miro.** Quedo sin verificar " +
          "; ".join(ciegos) + ".\n")

    # ------------------------------------------------------------------
    # LA INVARIANTE. Un veredicto que el motor dicta y el informe no imprime
    # es una decision que nunca llega a nadie. Pasaba porque las secciones se
    # armaban POR ESTADO y los estados de novedad no cruzaban con la decision:
    # el motor dictaba 27 cambios y el papel mostraba 20.
    # Esto NO se arregla mirando; se arregla contando y muriendo.
    # ------------------------------------------------------------------
    # RED ESTRUCTURAL. Antes de comparar, se barre por ESTADO: cualquier pedido con
    # veredicto no-DEJAR que ninguna seccion haya registrado se imprime aqui, en vez
    # de matar el informe. Fallar cerrado esta bien; fallar cerrado TODOS los dias
    # porque aparecio un estado nuevo, no. Asi el informe sale y el hueco se ve.
    debian = {x["id"] for x in X if x.get("rec") and x["rec"] != "DEJAR"}
    huerfanos = sorted(debian - rendido)
    if huerfanos:
        A(f"## {ROJO} Sin seccion asignada · {len(huerfanos)}\n")
        A("Estos llevan decision del motor y ninguna seccion los recogio, porque su estado")
        A("no estaba previsto. Se imprimen aqui para que no se pierdan, y hay que darles")
        A("su sitio en la proxima version.\n")
        A("| WhatsApp | Cliente | Ciudad | Estado | Decision |")
        A("| --- | --- | --- | --- | --- |")
        for i in huerfanos:
            x = dec[i]
            o = next((z for z in ords if z["id"] == i), {})
            e = x.get("elegida")
            A(f"| {x.get('tel','')} | {x.get('cliente','')[:16]} | "
              f"{(x.get('ciudad') or '')[:12]} | {o.get('status','?')} | "
              f"**{x['rec']}**" + (f" a {e['t']}" if e and x['rec'] == 'CAMBIAR' else "") + " |")
            rendido.add(i)
        A("")
    faltan = debian - rendido
    if faltan:
        detalle = ", ".join(f"{i} ({dec[i]['rec']}, {dec[i].get('ciudad')})"
                            for i in sorted(faltan)[:12])
        sys.exit(
            f"INFORME INCOMPLETO: el motor dicta {len(debian)} decisiones que no son DEJAR y "
            f"el informe solo imprime {len(rendido & debian)}. Se pierden {len(faltan)}: "
            f"{detalle}.\nNo se escribe un informe al que le faltan decisiones: quien lo lea "
            "creeria que esos pedidos van bien.")

    escribir_texto(a.salida, "\n".join(L))

    # ------------------------------------------------------------------
    # EL PDF. Regla de FER: el informe diario SIEMPRE sale tambien en PDF.
    # Se hace con golden-pdf-check, que es el estandar de la casa: motor
    # Playwright, compuerta verbatim y auditoria. Si el PDF no sale o no
    # queda APROBADO, esto lo DICE — no se entrega un Markdown solo
    # fingiendo que se cumplio la regla.
    # ------------------------------------------------------------------
    if a.pdf:
        import subprocess
        # COMPUERTA DE SOBRESCRITURA. Pasó de verdad: una corrida de prueba escribió
        # encima del PDF que otro chat había dejado en el Escritorio y que FER había
        # decidido conservar. Un entregable ajeno no se pisa aunque el nombre coincida.
        # MISMA POLITICA QUE EL 360, importada del mismo sitio: lo propio se archiva,
        # lo ajeno no se toca. Aqui se negaba SIEMPRE, asi que la segunda corrida del
        # dia no producia PDF; alli se archivaba TODO, incluido lo de otro chat.
        ok, msg = preparar_destino_pdf(
            a.pdf, os.path.join(os.path.dirname(os.path.abspath(a.salida)), "_archivo"))
        if not ok:
            sys.exit(msg)
        if msg:
            print(msg)
        PY_PDF = os.path.expanduser("~/.golden/pdfenv/bin/python")
        SK_PDF = os.path.expanduser("~/.claude/skills/golden-pdf-check/scripts")
        if not os.path.exists(PY_PDF):
            print(f"AVISO: no se genero el PDF porque no existe {PY_PDF}. "
                  "El informe queda solo en Markdown y la regla de entrega NO se cumplio.",
                  file=sys.stderr)
        else:
            r = subprocess.run([PY_PDF, f"{SK_PDF}/build_pdf.py", a.salida, a.pdf, "--no-index"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print(f"AVISO: el PDF FALLO.\n{r.stderr[-400:]}", file=sys.stderr)
            else:
                au = subprocess.run([PY_PDF, f"{SK_PDF}/audit_pdf.py", a.pdf],
                                    capture_output=True, text=True)
                # La linea del auditor es:  **Veredicto:** APROBADO
                # Se toma lo que va DESPUES del ultimo '**'. Antes se tomaba el trozo
                # anterior y salia siempre "Veredicto:", lo que disparaba un aviso falso
                # de "no aprobado" en cada corrida. Un aviso que grita siempre no avisa.
                # NO-AUDITADO NO ES APROBADO, y hay que leer el CODIGO DE SALIDA para
                # saberlo. Si al auditor le falta una libreria, imprime que la instales
                # y termina — y esta lectura, que solo buscaba la palabra "Veredicto",
                # se quedaba con "SIN VEREDICTO" y seguia adelante marcando el PDF como
                # propio. Un PDF sin auditar quedaba indistinguible de uno aprobado.
                # Es la ley del cero honesto en el ultimo paso de la entrega: "no se
                # pudo mirar" y "esta bien" son respuestas distintas.
                ver = "SIN VEREDICTO"
                if au.returncode != 0:
                    ver = f"NO AUDITADO (el auditor fallo, salida {au.returncode})"
                    print(f"  AVISO: {(au.stderr or au.stdout).strip()[:200]}",
                          file=sys.stderr)
                else:
                    for ln in au.stdout.splitlines():
                        if "Veredicto" in ln:
                            ver = ln.rsplit("**", 1)[-1].strip() if "**" in ln else ln.strip()
                            break
                print(f"  PDF: {a.pdf} · auditoria {ver}")
                marcar_como_propio(a.pdf)   # deja la senal: el de manana sabra que es nuestro
                if "APROBADO" not in ver:
                    print("  OJO: el PDF no quedo aprobado por el estandar. Revisalo antes de "
                          "mandarlo.", file=sys.stderr)
    print(f"informe: {a.salida}")
    print(f"  invariante: {len(debian)} decisiones no-DEJAR dictadas, "
          f"{len(rendido & debian)} impresas")
    print(f"  acciones {len(filas)} · frenar {len(frenar)}/{len(salio)} · novedades {len(nov)} · "
          f"oficina {len(ofi)} · cambios {len(cambios_quietos)} · direcciones {len(dirs)} · "
          f"tuyos {tuyos}")
    if cruce["estado"] == "CORRIDO":
        print(f"  cruce: {len(no_cuadran)} no cuadran + {len(contra)} contradictorios, sobre "
              f"{cruce['comparadas']} comparadas de {cruce['modificables']}")
    else:
        print(f"  cruce NO CORRIDO: {cruce['razon']}")
    if embudo["estado"] == "CORRIDO":
        print(f"  embudo: {embudo['fuga']} fugas sobre {embudo['revisados']} revisados")
    else:
        print(f"  embudo NO CORRIDO: {embudo['razon']}")


if __name__ == "__main__":
    main()
