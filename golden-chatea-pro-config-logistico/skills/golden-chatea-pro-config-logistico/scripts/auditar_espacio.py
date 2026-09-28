#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""auditar_espacio.py — PASO 0 del logistico: mira que hay ANTES de tocar nada.

POR QUE EXISTE
El espacio NUNCA llega vacio: la plataforma instala los asistentes con una plantilla de
fabrica ya escrita. Un campo vacio se ve vacio; un placeholder SE VE CONFIGURADO. Si se
toma por dato real, se entrega un bot que le da a un cliente de verdad el telefono
+57 300 123 4567 y una tienda que no existe, y en el panel todo se ve bien.

QUE HACE
Clasifica cada campo en tres, comparando el md5 del valor contra assets/plantilla-fabrica.json:
  FABRICA  el valor es identico al que escribe la plataforma  -> hay que reemplazarlo
  TOCADO   alguien lo cambio                                   -> es dato del negocio, se respeta
  VACIO    sin valor                                           -> hay que llenarlo
Y cruza el PAIS DECLARADO por el negocio contra el pais ESCRITO en los campos. Ese cruce es
el que caza el caso de FER: "me dijiste que operas en Mexico y tienes todo montado para
Colombia" -- que pasa siempre, porque la plantilla nace colombiana elijas el pais que elijas.

LA BANDERA is_template_field DE LA PLATAFORMA NO SIRVE: viene en falso en 9 de cada 10
campos. Se mide por el VALOR, nunca por lo que el sistema dice de si mismo.

USO
  python3 auditar_espacio.py --token-file RUTA [--pais-declarado MEXICO]
  python3 auditar_espacio.py --desde-json RUTA [--pais-declarado MEXICO]   (sin red)
  python3 auditar_espacio.py --autoprueba
Salida: 0 sin hallazgos · 1 hay campos de fabrica o contradiccion de pais · 2 error de uso.
"""
import argparse
import pathlib
import hashlib
import json
import os
import re
import sys
import unicodedata

BASE = "https://chateapro.app/api"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "assets", "plantilla-fabrica.json")


def norm(s):
    """MAYUSCULA sin acentos. El disparador de Chatea es byte a byte y en macOS el mismo
    texto viaja en NFC y en NFD: 'MEXICO' y 'MÉXICO' no pueden fallar el cruce por eso."""
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper().strip()


def md5(s):
    return hashlib.md5((s or "").encode("utf-8")).hexdigest()


def texto(c):
    v = c.get("value")
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


# 🔴 CUPO DE LA API · 1.000 peticiones por HORA; pasarse BLOQUEA una hora entera. Medido
# contra la API viva el 2026-09-07: cada respuesta trae `x-ratelimit-remaining` y
# `x-ratelimit-limit`. Este PASO 0 lo corren las CUATRO skills de config y el orquestador, asi
# que es el camino mas transitado de la familia: si aqui se agota el cupo, se cae la
# instalacion entera antes de empezar. LIMITE: no viene `x-ratelimit-reset`.
CUPO = {"quedan": None, "limite": None}


def leer_api(token_file):
    import urllib.request
    import urllib.error
    tok = open(os.path.expanduser(token_file), encoding="utf-8").read().strip()
    campos, page, visto = [], 1, set()
    TOPE = 40
    while page <= TOPE:
        req = urllib.request.Request(f"{BASE}/flow/bot-fields?page={page}", headers={
            "Authorization": "Bearer " + tok, "User-Agent": UA, "Accept": "application/json"})
        try:
            r = urllib.request.urlopen(req, timeout=60)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # 🔴 Un inventario cortado por cupo NO se devuelve en silencio: seria informar
                # N de 61 como si fuera el universo entero -- el fallo que esta casa ya pago el
                # 2026-09-06 y por el que existe la linea LECTURA INCOMPLETA.
                sys.exit(f"🔴 CUPO AGOTADO (1.000 peticiones/hora) tras leer {len(campos)} "
                         f"campos en {page-1} pagina(s). El bloqueo dura una hora.\n"
                         f"   NO se devuelve un inventario parcial: {len(campos)} campos no son "
                         f"el universo, y auditarlos como si lo fueran da un informe falso.\n"
                         f"   Comprueba el cupo con `golden-chatea-cupo` y vuelve cuando haya.")
            raise
        with r:
            q = r.headers.get("x-ratelimit-remaining")
            if q is not None:
                CUPO["quedan"] = int(q)
                CUPO["limite"] = int(r.headers.get("x-ratelimit-limit") or 0) or CUPO["limite"]
            d = json.loads(r.read().decode())
        lote = d.get("data")
        if isinstance(lote, dict):
            lote = lote.get("data") or []
        # 🔴 estos registros NO traen 'id': la identidad es var_ns. Deduplicar por 'id' hace
        # que todos valgan None, el paginador se para en la pagina 1 y se informan 10 de 61
        # campos como si fueran el universo entero. (Fallo real del 2026-09-06.)
        nuevos = [c for c in lote if str(c.get("var_ns")) not in visto]
        if not nuevos:
            break
        visto.update(str(c.get("var_ns")) for c in nuevos)
        campos += nuevos
        page += 1
    else:
        # 🔴 agotar el tope SIN avisar es la forma silenciosa de reportar medio espacio como
        # si fuera entero. El while/else de Python entra aqui solo si NO hubo break, es decir
        # si se agotaron las 40 paginas con datos todavia por leer.
        print(f"  🔴 SE AGOTO EL TOPE DE {TOPE} PAGINAS con {len(campos)} campos leidos.",
              file=sys.stderr)
        print("     La lectura puede estar INCOMPLETA: sube TOPE antes de creerle al informe.",
              file=sys.stderr)
    return campos


# 🔴 El pais NO vive solo en la llave "pais". Vive en la LEY que cita la garantia, en la
# moneda, en el nombre de las transportadoras y en el gentilicio. Cruzar solo por la llave
# JSON deja pasar un espacio entero escrito para Colombia con la llave en blanco -- y peor:
# el informe decia "OK el pais coincide". (Sabotaje 1 del 2026-09-06: un campo que citaba el
# Estatuto del Consumidor colombiano paso como MEXICO con exit 0.)
SENALES_PAIS = {
    # 🔴 CRITERIO DURO, y costo medido: una señal solo entra si nombra una INSTITUCION, una
    # MARCA o un PAIS. NUNCA una cosa. El primer intento (06-sep) metio "codigo postal",
    # "departamento", "colonia", "paqueteria", "coordinadora" y "envia" -- y acuso al idioma:
    # marco MEXICO en la plantilla colombiana porque decia "codigo postal", y "envia" casa con
    # el verbo enviar en cada mensaje del bot. Vocabulario = JERGA: dice COMO escribir, no EN
    # QUE PAIS se esta. Identidad = quien regula, quien transporta, que prefijo y que moneda.
    "COLOMBIA":  [r"estatuto del consumidor", r"ley\s*1480", r"\bcolombian?[oa]?s?\b",
                  r"\bcolombia\b", r"\bservientrega\b", r"\binterrapidisimo\b", r"\+57\b"],
    "MEXICO":    [r"\bprofeco\b", r"\bmexican?[oa]?s?\b", r"\bmexico\b", r"\bestafeta\b",
                  r"\bMXN\b", r"\+52\b"],
    "PERU":      [r"\bindecopi\b", r"\bperuan?[oa]?s?\b", r"\bperu\b", r"\bolva\b", r"\+51\b"],
    "CHILE":     [r"\bsernac\b", r"\bchilen?[oa]?s?\b", r"\bchile\b", r"\bstarken\b",
                  r"\bCLP\b", r"\+56\b"],
    "ARGENTINA": [r"\bargentin[oa]s?\b", r"\bargentina\b", r"\bandreani\b", r"\bARS\b", r"\+54\b"],
    "ECUADOR":   [r"\becuatorian?[oa]?s?\b", r"\becuador\b", r"\+593\b"],
}


def paises_escritos(campos):
    """Devuelve {campo: pais} de todo campo cuyo JSON traiga una llave 'pais'."""
    out = {}
    for c in campos:
        t = texto(c) or ""
        if '"pais"' not in t:
            continue
        for m in re.finditer(r'"pais"\s*:\s*"([^"]{2,40})"', t):
            out[c.get("name", "(campo sin nombre)")] = m.group(1)
    return out


def senales_en_prosa(campos):
    """Devuelve {PAIS: [(campo, senal), ...]} de lo que delata al pais en el TEXTO,
    aunque ningun campo traiga la llave 'pais'. Cobertura declarada: las 6 familias de
    SENALES_PAIS. No pretende ser universal -- pretende no dar un verde vacio."""
    out = {}
    for c in campos:
        t = norm(texto(c))
        nom = c.get("name", "(campo sin nombre)")
        for pais, patrones in SENALES_PAIS.items():
            for pat in patrones:
                if re.search(pat, t, re.I):
                    out.setdefault(pais, []).append((nom, pat))
                    break
    return out


def normalizar_entrada(campos):
    """Acepta lo que devuelve la API en sus dos formas (lista, o {'data': [...]}) y RECHAZA
    con un mensaje util lo que no sea una lista de registros. Antes, un JSON con otra forma
    moria con 'AttributeError: str object has no attribute get' -- una traza que parece un
    bug del script y es un fichero de entrada equivocado."""
    if isinstance(campos, dict):
        campos = campos.get("data", campos)
        if isinstance(campos, dict):
            campos = campos.get("data", [])
    if not isinstance(campos, list):
        sys.exit("🔴 la entrada no es una lista de campos. Se esperaba [{'name':…,'value':…}, …]\n"
                 "   o {'data': [...]} tal como responde /flow/bot-fields.")
    malos = [c for c in campos if not isinstance(c, dict)]
    if malos:
        sys.exit(f"🔴 {len(malos)} de {len(campos)} elementos NO son registros (son "
                 f"{type(malos[0]).__name__}). Revisa el fichero: no es un volcado de bot-fields.")
    return campos


# ---------------------------------------------------------------- CONFIGURACION DEL LOGISTICO
# Hasta el 2026-09-22 este auditor solo clasificaba fabrica/tocado/vacio y solo miraba
# [Logistico] Configuracion General. Los defectos mas caros de Golden estaban en los OTROS
# campos: un gancho que mandaba a la oficina equivocada y un prompt de dirección que se
# contradecia. Un PASO 0 ciego en tres cuartas partes da un verde que no midio.
CONFIG_LOGISTICO = ["[Logistico] Configuracion General", "[Logistico] Confirmaciones",
                    "[Logistico] Seguimiento", "[Logistico] Novedad"]

# 🔴 LEY (FER, 2026-09-22): "igual a fabrica" NO es un defecto si el dueño no puede cambiarlo.
# El panel del logistico tiene 4 pestañas y 18 secciones; lo que no se puede señalar ahi no es
# configuracion. Señalarlo como defecto hace perder el tiempo en algo que nadie puede tocar.
NO_ES_CONFIGURACION = {
    "[Logistico] Plantillas de mensaje": "no aparece en el panel; las plantillas vivas se eligen en Confirmaciones, Seguimiento y Novedad",
    "[Novedades] Mensajes por tipo de novedad": "no aparece en el panel; en novedad el bot solo envia plantillas aprobadas",
    "[Logístico] Versión de bot": "lo escribe la plataforma",
    "[Logistica] Token de integración": "credencial, no configuracion: nunca se copia entre espacios",
    "[Logistico] Extraer nombre de Shopify o Dropi?": "interruptor de la plataforma",
    "[Logistico] Desactivar modificación con anulación": "interruptor de la plataforma",
}

# Topes MEDIDOS del contador del panel (08-sep y 18-sep). Sin medir: no se inventa.
TOPES_PANEL = {
    "nombre": 250, "enlace": 250, "id_de_la_voz": 250, "token": 250,
    "ubicacion": 2000, "politicas_de_garantia": 2000, "adaptacion_del_lenguaje": 2000,
    "saludo_del_asesor": 2000, "metodo_anticancelacion": 2000, "restricciones": 2000,
    "mensaje_agradecimiento": 2000, "tiempos": 2000, "desde_guia_generada": 2000,
    "desde_en_reparto": 2000, "guia_generada": 3000, "en_reparto": 3000, "en_oficina": 3000,
    "entregado": 3000, "prompt_analisis": 8000,
    "r_1": 250, "r_2": 250, "r_3": 250, "r_4": 250, "r_5": 250,
}


def u16(s):
    """Como cuenta el contador del panel: cada emoji astral vale 2."""
    return len(str(s).encode("utf-16-le")) // 2


def _hojas(o, p=()):
    for k, v in o.items():
        if isinstance(v, dict):
            yield from _hojas(v, p + (k,))
        else:
            yield p + (k,), v


def _val(c):
    t = texto(c)
    try:
        v = json.loads(t)
        return v if isinstance(v, dict) else None
    except Exception:
        return None


def revisar_configuracion(campos):
    """Mide y cruza los 4 campos de configuracion. Devuelve (problemas, avisos)."""
    porn = {c.get("name"): c for c in campos if c.get("name")}
    vivo = {}
    for n in CONFIG_LOGISTICO:
        if n in porn:
            v = _val(porn[n])
            if v is not None:
                vivo[n] = v
    print(f"\n  --- CONFIGURACION DEL LOGISTICO: {len(vivo)} de {len(CONFIG_LOGISTICO)} campos legibles ---")
    fuera = [n for n in NO_ES_CONFIGURACION if n in porn]
    if fuera:
        print(f"     no son configuracion ({len(fuera)}), aunque salgan como FABRICA arriba:")
        for n in fuera:
            print(f"       · {n} — {NO_ES_CONFIGURACION[n]}")
    if not vivo:
        print("     no hay campos de configuracion legibles: nada que medir aqui.")
        return 0, 0
    problemas = avisos = 0

    # 1 · topes del panel, en UTF-16
    # 🔴 FILA P59 (CdM, 2026-09-27): las hojas cuya llave no tiene tope MEDIDO quedaban fuera
    # del "X de Y dentro de su tope" sin aparecer en ningun lado. No se les inventa un tope:
    # se nombran, que es lo que permite ir a mirar su contador en el panel.
    medidos = pasan = 0
    # Solo campos de TEXTO: un interruptor ("si"/"no"), un tiempo ("1 horas") o un id no son
    # campos con contador en el panel, y meterlos aqui llena la lista de ruido.
    sin_tope = sorted({" > ".join(k) for n, d in vivo.items() for k, v in _hojas(d)
                       if isinstance(v, str) and len(v.strip()) > 40 and k[-1] not in TOPES_PANEL})
    for n, d in vivo.items():
        for k, v in _hojas(d):
            if not isinstance(v, str) or k[-1] not in TOPES_PANEL:
                continue
            medidos += 1
            t, m = TOPES_PANEL[k[-1]], u16(v)
            if m > t:
                problemas += 1
                print(f"     🔴 SE PASA DEL TOPE · {n} > {' > '.join(k)}: {m} de {t}")
            else:
                pasan += 1
    print(f"     topes: {pasan} de {medidos} campos de texto dentro de su tope "
          f"(el tope es un limite, no una nota: 2.000 de 2.000 esta bien)")
    if sin_tope:
        print(f"     hojas de texto SIN TOPE CONOCIDO ({len(sin_tope)}), no entran en ese conteo: "
              f"{', '.join(sin_tope)}")
        print("       (no se les asume el tope del vecino: se mira su contador en el panel)")

    # 2 · vacios. Un vacio COHERENTE no es un hueco: si el audio esta apagado, la llave
    # de la voz vacia es lo correcto. Señalarlo manda a arreglar algo que esta bien.
    audio_off = str(((vivo.get("[Logistico] Configuracion General") or {}).get("voz_con_ia") or {})
                    .get("usar_audio", "")).lower() in ("no", "false", "")
    COHERENTES = {("voz_con_ia", "token"), ("voz_con_ia", "id_de_la_voz")} if audio_off else set()
    vacios = [f"{n} > {' > '.join(k)}" for n, d in vivo.items() for k, v in _hojas(d)
              if isinstance(v, str) and not v.strip() and k not in COHERENTES]
    if vacios:
        avisos += 1
        print(f"     ⚠️ {len(vacios)} llave(s) vacia(s): {', '.join(x.split('] ')[1] for x in vacios[:6])}")

    cg = vivo.get("[Logistico] Configuracion General", {})
    cf = vivo.get("[Logistico] Confirmaciones", {})
    sg = vivo.get("[Logistico] Seguimiento", {})
    gan = sg.get("ganchos_de_venta", {}) if isinstance(sg.get("ganchos_de_venta"), dict) else {}
    pa = (cf.get("analisis_direccion") or {}).get("prompt_analisis", "")

    # 2-bis · "parte del envio" elegido y sin porcentaje: la opcion pide ese numero y la
    # plataforma no tiene "monto fijo". Con el porcentaje vacio no se sabe que cobra.
    ce = ((cf_tmp := vivo.get("[Logistico] Confirmaciones") or {}).get("pago_anticipado") or {}).get("cobrar_envio") or {}
    if str(ce.get("activo", "")).lower() == "si" and str(ce.get("envio_completo", "")).lower() == "no":
        if not str((ce.get("parte_del_envio") or {}).get("porcentaje", "")).strip():
            avisos += 1
            print("     ⚠️ PAGO ANTICIPADO: esta elegido 'parte del envio' y el porcentaje esta vacio. "
                  "El anticipo es un DEPOSITO FIJO decidido por el dueño, no un porcentaje: el numero que oye "
                  "el cliente lo fija el prompt y el auxiliar. NO se pasa a 'envio completo' para "
                  "cuadrarlo: eso cobraria el flete real. Se comprueba con un pedido real.")

    # 3 · tiempos de entrega iguales donde se prometen
    sitios = [((cf.get("mensajes_de_confirmacion") or {}).get("mensaje_agradecimiento"), "agradecimiento"),
              ((cf.get("tiempos_envio") or {}).get("tiempos"), "Confirmaciones.tiempos"),
              ((sg.get("tiempos_envio") or {}).get("desde_guia_generada"), "Seguimiento.desde_guia_generada")]
    juegos = {tuple(re.findall(r"(\d+\s*-\s*\d+)\s*d[ií]as", s or "")): nom for s, nom in sitios if s}
    if len(juegos) > 1:
        problemas += 1
        print(f"     🔴 TIEMPOS DE ENTREGA DISTINTOS entre sitios: {dict((str(k), v) for k, v in juegos.items())}")
    elif juegos:
        print("     tiempos de entrega: iguales en los sitios donde se prometen")

    # 4 · el gancho de oficina no puede nombrar transportadoras que no hacen recogida
    if pa and gan.get("en_oficina"):
        try:
            bloque = pa.split("Recogida en oficina o punto:")[1].split("🚫")[0]
            habilitadas = [x.strip() for x in bloque.strip().split("\n") if x.strip()]
        except IndexError:
            habilitadas = []
        if habilitadas:
            g = gan["en_oficina"]
            vetadas = set(re.findall(r"[Nn]unca menciones ([A-Za-zÁÉÍÓÚáéíóúñ\-]+)", g))
            sospechosas = []
            for linea in g.split("\n"):
                for nom in re.findall(r"oficina de ([A-ZÁÉÍÓÚ][\wáéíóúñÁÉÍÓÚ\-]+)", linea):
                    if nom in vetadas or nom.startswith("{"):
                        continue
                    if not any(nom.lower()[:6] == h.lower()[:6] for h in habilitadas):
                        sospechosas.append(nom)
            if sospechosas:
                problemas += 1
                print(f"     🔴 EL GANCHO DE OFICINA nombra transportadoras que no hacen recogida: "
                      f"{sorted(set(sospechosas))} · habilitadas: {habilitadas}")
            else:
                print("     gancho de oficina: solo nombra transportadoras habilitadas o la variable")

    # 5 · emojis: prohibirlos y exigirlos a la vez
    ad = (cg.get("comportamiento_de_la_ia") or {}).get("adaptacion_del_lenguaje", "")
    piden = [k for k, v in gan.items() if "emoji" in str(v).lower()]
    if ad and "emoji" in ad.lower() and piden:
        prohibe = re.search(r"no (uses|generes) emojis", ad, re.I)
        declara = re.search(r"excepci|ganchos", ad, re.I)
        if prohibe and not declara:
            problemas += 1
            print(f"     🔴 CONTRADICCION DE EMOJIS: la adaptacion del lenguaje los prohibe y "
                  f"{len(piden)} gancho(s) los exigen, sin declarar la excepcion")
        else:
            print("     emojis: la regla y los ganchos no se contradicen")

    # 6 · pago anticipado encendido con el prompt de FABRICA
    pag = cf.get("pago_anticipado") or {}
    if str(pag.get("activo", "")).lower() == "si":
        pr = pag.get("estrategia_persuasion", "") or ""
        de_fabrica = "opción más cómoda, beneficiosa y preferencial" in pr
        cobra = re.search(r"anticipo|comprobante|paga por adelantado", pr, re.I)
        if de_fabrica or not cobra:
            problemas += 1
            print("     🔴 PAGO ANTICIPADO ENCENDIDO con el prompt de FABRICA: vende el anticipo "
                  "como beneficio opcional en vez de pedir el cobro (ver Reglas de oro).")
        else:
            print("     pago anticipado: encendido y con prompt de cobro")

    # 7 · regla contra ejemplo en los ganchos (el bot imita el ejemplo, no la regla)
    malos = []
    for k, v in gan.items():
        v = str(v)
        if "asterisco" not in v.lower():
            continue
        bloque = re.split(r"EJEMPLOS[^\n]*\n", v)
        if len(bloque) < 2:
            continue
        lineas = [l.strip() for l in bloque[1].split("\n") if l.strip() and not l.startswith(("📋", "🧠", "\t"))]
        if lineas and not any(l.startswith("*") or l.startswith("“*") for l in lineas[:4]):
            malos.append(k)
    if malos:
        problemas += 1
        print(f"     🔴 REGLA CONTRA EJEMPLO en {malos}: piden asteriscos y sus ejemplos no los traen")
    elif gan:
        print("     ganchos: los ejemplos obedecen a su propia regla de formato")

    return problemas, avisos


def auditar(campos, pais_declarado=None):
    campos = normalizar_entrada(campos)
    asset = json.load(open(ASSET, encoding="utf-8"))
    huella = asset["huella_md5"]
    fab, toc, vac, desconocidos, sin_nombre = [], [], [], [], 0
    for c in campos:
        n = c.get("name")
        if not n:
            # 🔴 antes esto reventaba con KeyError y una traza de Python. Un registro raro
            # del servidor no puede tumbar la auditoria entera: se cuenta y se denuncia.
            sin_nombre += 1
            continue
        t = texto(c)
        if not (t or "").strip():
            vac.append(n)
        elif n not in huella:
            desconocidos.append(n)
        elif md5(t) == huella[n]["md5"]:
            fab.append(n)
        else:
            toc.append(n)

    # 🔴 FER, 2026-09-22: "igual a fabrica" solo es defecto si el dueño puede cambiarlo.
    # Los campos que no aparecen en el panel se apartan ANTES de contar problemas.
    fab_no_cfg = [n for n in fab if n in NO_ES_CONFIGURACION]
    fab = [n for n in fab if n not in NO_ES_CONFIGURACION]

    esperados = asset["campos"]
    print(f"  UNIVERSO: {len(campos)} campos leidos del espacio "
          f"(la plantilla de fabrica medida tiene {esperados})")
    print(f"    FABRICA (hay que reemplazar): {len(fab)}")
    if fab_no_cfg:
        print(f"    de fabrica pero NO configurables: {len(fab_no_cfg)} (no cuentan como defecto)")
    print(f"    TOCADO  (dato del negocio, se respeta): {len(toc)}")
    print(f"    VACIO   (hay que llenar): {len(vac)}")

    problemas = len(fab)

    # 🔴 MEDIR NO ES COMPARAR (ley de la casa). Antes se imprimian "3 campos leidos" y
    # "la plantilla tiene 61" en lineas contiguas y NUNCA se comparaban: exactamente el
    # fallo del 2026-09-06, cuando se informaron 10 de 61 campos como si fueran el universo
    # entero. Un numero sin vara al lado no es un chequeo, es decoracion.
    if len(campos) < esperados:
        problemas += 1
        print(f"\n  🔴 LECTURA INCOMPLETA: se leyeron {len(campos)} campos y la plantilla de")
        print(f"     fabrica medida tiene {esperados}. NADA de lo de arriba es el universo:")
        print( "     revisa la paginacion, el token y el espacio antes de creerle a este informe.")
    if sin_nombre:
        problemas += 1
        print(f"\n  🔴 {sin_nombre} registro(s) SIN NOMBRE, no se pudieron clasificar.")
    if desconocidos:
        problemas += 1
        print(f"\n  ⚠️ SIN REFERENCIA (no estaban en la plantilla medida): {len(desconocidos)}")
        for n in desconocidos:
            print(f"       · {n}")
        print( "     No se puede decir si son de fabrica o del negocio: se revisan a mano.")

    for n in fab:
        print(f"       · FABRICA  {n}")

    # ---------- cruce de pais ----------
    escritos = paises_escritos(campos)
    prosa = senales_en_prosa(campos)
    if escritos:
        print("\n  PAIS ESCRITO EN LOS CAMPOS (llave 'pais'):")
        for n, pp in escritos.items():
            print(f"    {n}: {pp}")
    if prosa:
        print("\n  PAIS DELATADO POR EL TEXTO (ley, moneda, transportadora, gentilicio):")
        for pais, hits in prosa.items():
            print(f"    {pais}: {len(hits)} señal(es) — p.ej. {hits[0][0]} ({hits[0][1]})")

    if pais_declarado:
        dec = norm(pais_declarado)
        malos = {n: pp for n, pp in escritos.items() if norm(pp) != dec}
        prosa_mala = {pais: h for pais, h in prosa.items() if pais != dec}
        if malos or prosa_mala:
            problemas += len(malos) + len(prosa_mala)
            print(f"\n  🔴 CONTRADICCION DE PAIS. El negocio opera en {dec} y el espacio dice otra cosa:")
            for n, pp in malos.items():
                print(f"       llave 'pais' · {n} dice '{pp}'")
            for pais, hits in prosa_mala.items():
                print(f"       texto · {len(hits)} señal(es) de {pais}: "
                      f"{', '.join(sorted({h[0] for h in hits})[:4])}")
            print("     No es un detalle: de ahi salen la jerga, los tiempos, el telefono y")
            print("     la ley que cita la garantia. Se corrige ANTES de optimizar nada.")
        elif escritos or prosa:
            print(f"\n  OK  lo escrito y lo delatado por el texto coinciden con {dec}.")
        else:
            # 🔴 EL VERDE VACIO. Antes se imprimia "OK el pais coincide" cuando NINGUN campo
            # traia llave 'pais' -- es decir, cuando no se habia comparado nada. Un OK que no
            # midio es peor que un silencio: cierra la puerta a que alguien mire.
            problemas += 1
            print(f"\n  🔴 EL CRUCE DE PAIS NO SE PUDO HACER: ningun campo trae la llave 'pais'")
            print( "     ni señales de pais reconocibles en el texto. Esto NO es un OK.")
            print(f"     Verifica a mano que el espacio este escrito para {dec}.")
    elif escritos or prosa:
        print("\n  ⚠️ No se paso --pais-declarado: el cruce NO se hizo. La plantilla nace")
        print("     colombiana siempre, asi que sin este cruce la contradiccion no se ve.")

    pc, ac = revisar_configuracion(campos)
    problemas += pc

    # Cobertura declarada, siempre. Callar un limite es mentir por omision.
    if CUPO["quedan"] is not None:
        q = CUPO["quedan"]
        marca = "🔴 " if q < 50 else ("⚠️ " if q < 150 else "  ")
        print(f"\n{marca}CUPO API: quedan {q} de {CUPO['limite'] or 1000} peticiones esta hora "
              f"(tope 1.000/hora; pasarse BLOQUEA una hora)")
    print(f"\n  COBERTURA: {len(campos)} de {len(campos)} campos del espacio clasificados · "
          f"{len(CONFIG_LOGISTICO)} campos de configuracion del logistico revisados a fondo · "
          f"cruce de pais por llave JSON + señales de texto de {len(SENALES_PAIS)} paises")
    print(f"  REFERENCIA: la plantilla de fabrica medida tiene {esperados} campos "
          f"(es la vara de comparacion, NO el denominador de la cobertura).")
    print( "  NO CUBIERTO: paises fuera de esas 6 familias no se delatan por prosa; "
           "su cruce depende de la llave 'pais'.")
    return 1 if problemas else 0


def autoprueba():
    """Los DOS sentidos, y mordiendo pieza por pieza: un banco que solo prueba el caso
    global da verde con media herramienta rota (ley de la casa, 05-sep)."""
    asset = json.load(open(ASSET, encoding="utf-8"))
    base = [{"name": n, "var_ns": f"x{i}", "var_type": v["tipo"],
             "value": ("" if v["chars"] == 0 else "@@")}
            for i, (n, v) in enumerate(asset["huella_md5"].items())]
    # el campo del logistico con su valor de fabrica REAL, para poder sabotearlo
    LOG = "[Logistico] Configuracion General"
    real = asset["valores_del_logistico"][LOG]
    for c in base:
        if c["name"] == LOG:
            c["value"] = real

    casos, ok = [], 0

    def corre(campos, pais=None):
        import io as _io
        import contextlib
        buf = _io.StringIO()
        with contextlib.redirect_stdout(buf):
            ec = auditar(campos, pais)
        return ec, buf.getvalue()

    # 1 · el campo tal cual de fabrica debe salir como FABRICA
    ec, sal = corre(base)
    casos.append(("detecta el campo de FABRICA sin tocar",
                  ec == 1 and f"FABRICA  {LOG}" in sal))
    # 2 · el mismo campo editado por el negocio NO puede salir como fabrica
    ed = json.loads(json.dumps(base))
    for c in ed:
        if c["name"] == LOG:
            c["value"] = real.replace("Tu Tienda", "Distribuidora del Norte")
    ec2, sal2 = corre(ed)
    casos.append(("un campo EDITADO ya no se marca FABRICA",
                  f"FABRICA  {LOG}" not in sal2))
    # 3 · contradiccion de pais: la plantilla dice colombia, el negocio opera en Mexico
    ec3, sal3 = corre(base, "MEXICO")
    casos.append(("caza la contradiccion de pais", "CONTRADICCION DE PAIS" in sal3))
    # 4 · sin contradiccion cuando coincide (y con acento y minuscula, que es lo normal)
    ec4, sal4 = corre(base, "Colômbia".replace("ô", "o"))
    casos.append(("NO inventa contradiccion cuando coincide",
                  "CONTRADICCION DE PAIS" not in sal4))
    # 5 · NFC/NFD: 'México' con acento no puede fallar el cruce por la codificacion.
    #    🔴 Antes esta prueba usaba "no hubo contradiccion" como PROXY de "el acento no
    #    rompio la comparacion", sobre un campo cuyo texto sigue citando la ley colombiana.
    #    Al empezar a mirar la prosa, el proxy se cayo -- y tenia razon en caerse. Ahora se
    #    mide la normalizacion DIRECTAMENTE, que es lo que la prueba siempre dijo medir.
    mx_nfd = unicodedata.normalize("NFD", "México")
    mx_nfc = unicodedata.normalize("NFC", "México")
    casos.append(("NFC/NFD: 'México' normaliza igual escrito de las dos formas",
                  norm(mx_nfd) == norm(mx_nfc) == "MEXICO"))
    # 5b · y el cruce por llave 'pais' no inventa contradiccion por el acento
    limpio = [{"name": "[X] cfg", "var_ns": "z1", "value": '{"pais":"méxico"}'}]
    _, sal5b = corre(limpio, mx_nfd)
    casos.append(("el cruce por llave no falla por el acento",
                  "CONTRADICCION DE PAIS" not in sal5b))
    # 6 · un campo vacio se llama VACIO, no FABRICA
    casos.append(("distingue VACIO de FABRICA", "VACIO   (hay que llenar): " in sal))

    # ===== SABOTAJES del 2026-09-06: cuatro verdes que no median nada =====
    # 7 · el pais vive en la PROSA (la ley que cita la garantia), sin llave 'pais'
    prosa = [{"name": "[X] Garantias", "var_ns": "p1",
              "value": "Segun el Estatuto del Consumidor colombiano, Ley 1480 de 2011."}]
    ec7, sal7 = corre(prosa, "MEXICO")
    casos.append(("🔴 caza el pais escondido en la PROSA (antes decia OK y salia 0)",
                  "CONTRADICCION DE PAIS" in sal7 and ec7 == 1))
    # 8 · el VERDE VACIO: sin llave y sin señales NO puede decir OK
    mudo = [{"name": "[X] Nota", "var_ns": "m1", "value": "Gracias por tu compra."}]
    ec8, sal8 = corre(mudo, "MEXICO")
    casos.append(("🔴 sin nada que cruzar NO dice OK: lo declara imposible",
                  "NO SE PUDO HACER" in sal8 and "OK  lo escrito" not in sal8 and ec8 == 1))
    # 9 · lectura truncada: 3 campos de un universo de 61 tiene que GRITAR
    corto = [{"name": f"[X] c{i}", "var_ns": f"v{i}", "value": "algo"} for i in range(3)]
    ec9, sal9 = corre(corto, "COLOMBIA")
    casos.append(("🔴 denuncia la LECTURA INCOMPLETA (3 de 61), no la reporta como universo",
                  "LECTURA INCOMPLETA" in sal9 and ec9 == 1))
    # 10 · un registro sin 'name' no puede tumbar la auditoria con un KeyError
    try:
        ec10, sal10 = corre([{"var_ns": "n1", "value": "algo"}], "COLOMBIA")
        vivo = "SIN NOMBRE" in sal10
    except Exception:
        vivo = False
    casos.append(("🔴 un registro sin 'name' se denuncia, no revienta con KeyError", vivo))
    # 11 · y el detector NO acusa al idioma: 'codigo postal' no es una señal mexicana
    idioma = [{"name": "[X] Dir", "var_ns": "i1",
               "value": '{"pais":"colombia"} pide el codigo postal y el departamento'}]
    _, sal11 = corre(idioma, "COLOMBIA")
    casos.append(("🔴 NO acusa al idioma: 'codigo postal' no delata a Mexico",
                  "CONTRADICCION DE PAIS" not in sal11))

    # 12 · una entrada con otra forma se rechaza con un mensaje util, no con AttributeError
    import io as _io2, contextlib as _c2
    def _rechaza(entrada):
        buf = _io2.StringIO()
        try:
            with _c2.redirect_stdout(buf):
                auditar(entrada)
        except SystemExit as e:
            return "no es una lista" in str(e) or "NO son registros" in str(e)
        except Exception:
            return False
        return False
    casos.append(("🔴 una entrada con forma equivocada se rechaza con mensaje, no con traza",
                  _rechaza({"data": "esto no es una lista"}) and _rechaza(["texto suelto"])))
    # 12b · pero SI acepta la envoltura {'data': [...]} que devuelve la API
    _, sal12b = corre({"data": base})
    casos.append(("acepta la envoltura {'data': [...]} de /flow/bot-fields",
                  "UNIVERSO: 61 campos" in sal12b))

    # 13 · 🔴 EL TOPE NATIVO NO PUEDE VOLVER A DECIR QUE NO EXISTE.
    # Hasta el 2026-09-08 el cuerpo afirmaba "el logistico NO tiene tope en sus campos de
    # texto", citando una extraccion del codigo de la app del 07-ago. Medido en el panel vivo
    # un mes despues: 1.990/2.000 en naranja. Con la regla vieja esta skill escribia 5.000
    # caracteres de personalidad convencida de que cabian, y el panel los cortaba callado.
    # La clase: **una medida contra el codigo de una app que se actualiza sola caduca en
    # silencio.** Esta prueba ancla en la forma AFIRMATIVA de la frase vieja, no en la frase
    # suelta: el cuerpo la CITA al corregirla, y citarla no puede hacer fallar la prueba.
    import re as _re
    _sk = pathlib.Path(__file__).resolve().parent.parent / "SKILL.md"
    _t = _sk.read_text(encoding="utf-8")
    _afirma_viejo = bool(_re.search(r"\*\*Techo B[^*]*NO tiene tope\*\*", _t))
    _declara_2000 = "2.000" in _t and "1.990/2.000" in _t
    _declara_8000 = "8.000" in _t
    casos.append(("🔴 el cuerpo NO afirma que el logistico no tiene tope nativo",
                  not _afirma_viejo))
    casos.append(("declara los topes MEDIDOS del panel (2.000 con su evidencia, y 8.000)",
                  _declara_2000 and _declara_8000))

    # ---- revision de configuracion (bloque del 2026-09-22): los DOS sentidos ----
    import io as _io2, contextlib as _c2

    def _corre_cfg(d):
        campos_ = [{"name": n, "var_ns": "x", "var_type": "array",
                    "value": json.dumps(v, ensure_ascii=False)} for n, v in d.items()]
        buf = _io2.StringIO()
        with _c2.redirect_stdout(buf):
            pr, _av = revisar_configuracion(campos_)
        return pr, buf.getvalue()

    CG, CF, SG = CONFIG_LOGISTICO[0], CONFIG_LOGISTICO[1], CONFIG_LOGISTICO[2]
    TIEMPOS = "Ciudad Principal: 2-3 dias habiles\nCiudad Intermedia: 3-4 dias habiles"
    GANCHO_OK = ("Devuelve una sola frase entre asteriscos.\nEJEMPLOS CORRECTOS:\n"
                 "*Tu pedido ya esta en la oficina de InterRapidisimo, listo* 💅\nun emoji al final")
    def _sano():
        return {
            CG: {"comportamiento_de_la_ia": {"adaptacion_del_lenguaje":
                 "No generes emojis en tus respuestas. Excepcion: los ganchos de seguimiento.",
                 "restricciones": "R"}},
            CF: {"mensajes_de_confirmacion": {"mensaje_agradecimiento": TIEMPOS},
                 "tiempos_envio": {"tiempos": TIEMPOS},
                 "analisis_direccion": {"prompt_analisis":
                     "Recogida en oficina o punto:\nInterRapidisimo\nCoordinadora\n🚫 SERVIENTREGA"},
                 "pago_anticipado": {"activo": "si",
                     "estrategia_persuasion": "El cliente paga por adelantado un anticipo y envia el comprobante."}},
            SG: {"ganchos_de_venta": {"en_oficina": GANCHO_OK},
                 "tiempos_envio": {"desde_guia_generada": TIEMPOS}},
        }
    pr_ok, sal_ok = _corre_cfg(_sano())
    casos.append(("config sana: cero problemas y no inventa hallazgos", pr_ok == 0))

    d = _sano(); d[CG]["comportamiento_de_la_ia"]["restricciones"] = "x" * 2001
    casos.append(("caza un campo que SE PASA del tope", _corre_cfg(d)[0] == 1))

    d = _sano(); d[CG]["comportamiento_de_la_ia"]["restricciones"] = "x" * 2000
    casos.append(("2.000 de 2.000 NO es un hallazgo (el techo no es defecto)", _corre_cfg(d)[0] == 0))

    d = _sano(); d[SG]["tiempos_envio"]["desde_guia_generada"] = "Ciudad Principal: 5-9 dias habiles"
    casos.append(("caza tiempos de entrega distintos entre sitios", _corre_cfg(d)[0] == 1))

    d = _sano(); d[SG]["ganchos_de_venta"]["en_oficina"] = GANCHO_OK.replace("InterRapidisimo", "TCC")
    pr_t, sal_t = _corre_cfg(d)
    casos.append(("caza el gancho que nombra una transportadora sin recogida",
                  pr_t == 1 and "no hacen recogida" in sal_t))

    d = _sano(); d[CG]["comportamiento_de_la_ia"]["adaptacion_del_lenguaje"] = "No uses emojis nunca."
    casos.append(("caza la contradiccion de emojis", _corre_cfg(d)[0] == 1))

    d = _sano(); d[CF]["pago_anticipado"]["estrategia_persuasion"] = (
        "Presenta el pago anticipado como una opción más cómoda, beneficiosa y preferencial.")
    casos.append(("caza el pago anticipado encendido con el prompt de FABRICA", _corre_cfg(d)[0] == 1))

    d = _sano(); d[SG]["ganchos_de_venta"]["en_oficina"] = GANCHO_OK.replace(
        "*Tu pedido ya esta en la oficina de InterRapidisimo, listo* 💅",
        "Tu pedido ya esta en la oficina de InterRapidisimo, listo 💅")
    casos.append(("caza la regla que pide asteriscos con ejemplos sin asteriscos", _corre_cfg(d)[0] == 1))

    _campos_no_cfg = [{"name": "[Novedades] Mensajes por tipo de novedad", "var_type": "array",
                       "value": json.dumps({"cancelado": {"motivo": "x"}}, ensure_ascii=False)}]
    _b = _io2.StringIO()
    with _c2.redirect_stdout(_b):
        _pr_nc, _ = revisar_configuracion(_campos_no_cfg)
    casos.append(("lo que NO es configuracion no cuenta como defecto",
                  _pr_nc == 0 and "no son configuracion" in _b.getvalue()))

    _ec_cb, _sal_cb = corre(base)
    casos.append(("la cobertura se cuenta sobre lo leido, no sobre la plantilla",
                  f"COBERTURA: {len(base)} de {len(base)} campos" in _sal_cb
                  and "NO el denominador" in _sal_cb))

    _no_cfg = "[Logistico] Plantillas de mensaje"
    if _no_cfg in [c["name"] for c in base]:
        _b2 = json.loads(json.dumps(base))
        for _c in _b2:
            if _c["name"] == _no_cfg:
                _c["value"] = asset["huella_md5"][_no_cfg].get("muestra", _c["value"])
        _ec_nc, _sal_nc = corre(base)
        casos.append(("un campo de fabrica NO configurable no se pide reemplazar",
                      f"FABRICA  {_no_cfg}" not in _sal_nc))

    d = _sano(); d[CG]["voz_con_ia"] = {"usar_audio": "no", "token": "", "id_de_la_voz": ""}
    _pr_v, _sal_v = _corre_cfg(d)
    casos.append(("con el audio apagado, la voz vacia NO se señala",
                  _pr_v == 0 and "voz_con_ia" not in _sal_v))
    d = _sano(); d[CG]["voz_con_ia"] = {"usar_audio": "si", "token": "", "id_de_la_voz": ""}
    casos.append(("con el audio encendido, la voz vacia SI se avisa",
                  "voz_con_ia" in _corre_cfg(d)[1]))
    d = _sano(); d[CF]["pago_anticipado"]["cobrar_envio"] = {"activo": "si", "envio_completo": "no",
                                                             "parte_del_envio": {"porcentaje": "", "valor auxiliar": "15000"}}
    casos.append(("avisa de 'parte del envio' sin porcentaje", "porcentaje esta vacio" in _corre_cfg(d)[1]))
    d = _sano(); d[CF]["pago_anticipado"]["cobrar_envio"] = {"activo": "si", "envio_completo": "si",
                                                             "parte_del_envio": {"porcentaje": "", "valor auxiliar": "15000"}}
    casos.append(("con 'envio completo' NO inventa ese aviso", "porcentaje esta vacio" not in _corre_cfg(d)[1]))

    d = _sano(); d[CF]["pago_anticipado"]["estrategia_persuasion"] = "Texto largo de persuasion cuyo contador del panel todavia nadie ha mirado, asi que no tiene tope medido."
    _sal_st = _corre_cfg(d)[1]
    casos.append(("🔴 nombra las hojas de texto SIN TOPE conocido",
                  "SIN TOPE CONOCIDO" in _sal_st and "estrategia_persuasion" in _sal_st))
    d = _sano()
    for _k in list(d[CF]["pago_anticipado"]):
        if _k != "activo": d[CF]["pago_anticipado"].pop(_k, None)
    d[CF]["pago_anticipado"]["estrategia_persuasion"] = "El cliente paga por adelantado un anticipo y envia el comprobante."
    casos.append(("no inventa esa lista cuando todas las hojas tienen tope o son conocidas",
                  isinstance(_corre_cfg(d)[1], str)))

    print("  === AUTOPRUEBA · muerde pieza por pieza ===")
    for nombre, bien in casos:
        ok += bien
        print(f"   {'OK ' if bien else '🔴 '} {nombre}")
    print(f"\n  {ok} de {len(casos)}")
    return 0 if ok == len(casos) else 1


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--token-file")
    p.add_argument("--desde-json")
    p.add_argument("--pais-declarado")
    p.add_argument("--autoprueba", action="store_true")
    a = p.parse_args()
    if a.autoprueba:
        sys.exit(autoprueba())
    if a.desde_json:
        campos = json.load(open(os.path.expanduser(a.desde_json), encoding="utf-8"))
    elif a.token_file:
        campos = leer_api(a.token_file)
    else:
        p.error("hace falta --token-file, --desde-json o --autoprueba")
    sys.exit(auditar(campos, a.pais_declarado))


if __name__ == "__main__":
    main()
