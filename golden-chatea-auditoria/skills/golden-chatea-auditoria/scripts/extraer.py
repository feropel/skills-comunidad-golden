#!/usr/bin/env python3
"""
EXTRACTOR · golden-chatea-auditoria

Saca el 100% de lo que la API de Chatea Pro expone de un espacio y lo deja en un DUMP
auditable. Es la FASE 1 (inventario): sin este archivo no hay denominador y no hay informe.

Uso:
    python3 extraer.py <archivo-token> <etiqueta> [carpeta-salida]

Ejemplo:
    python3 extraer.py .secrets/token-golden.txt golden ./auditoria

Escribe: <carpeta-salida>/DUMP-<etiqueta>.json

SEGURIDAD: la API devuelve las llaves de las integraciones EN TEXTO PLANO. Este script las
REDACTA siempre (guarda si hay valor y de que largo, nunca el valor). No se desactiva.

PAGINACION: casi todo pagina de 10 en 10 e ignora per_page. Se agota la paginacion y se
guarda el total declarado por el servidor para poder comprobar que no falto nada.
"""

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://chateapro.app/api"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

SENSIBLE = ("token", "api_key", "apikey", "secret", "password", "access_token",
            "key", "client_secret", "webhook_url", "authorization")

# Redactar POR NOMBRE DE LLAVE no protege nada: el secreto tambien viaja dentro del
# `value` de un bot field, y `value` no es un nombre sensible. Medido: el mismo DUMP
# tapaba la llave de Dropi en /integration/dropi y la dejaba en claro, con el mismo
# largo, dentro de `[Integraciones] Datos de integracion`. Se redacta tambien POR
# PATRON DE VALOR, y de forma quirurgica: se sustituye solo el secreto, no el campo
# entero, para que la configuracion siga siendo auditable.
PATRONES = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),
    ("ElevenLabs", re.compile(r"sk_[A-Za-z0-9]{24,}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("Meta", re.compile(r"EAA[A-Za-z0-9]{40,}")),
    ("Shopify", re.compile(r"shpat_[A-Fa-f0-9]{20,}")),
    ("xAI", re.compile(r"xai-[A-Za-z0-9]{20,}")),
    ("Google", re.compile(r"AIza[A-Za-z0-9_\-]{30,}")),
]


def redactar_texto(t):
    """Sustituye cualquier secreto reconocible DENTRO de una cadena."""
    for etiqueta, patron in PATRONES:
        t = patron.sub(lambda m: f"<<REDACTADO {etiqueta} len={len(m.group(0))}>>", t)
    return t

SIMPLES = [
    "/me", "/team-info", "/flow/bot-users-count",
    "/flow/settings/get-default-ai-provider", "/workspace-settings/channels",
    "/installed-mini-app/list",
    "/integration/dropi", "/integration/shopify", "/integration/woocommerce",
    "/integration/openai", "/integration/calude", "/integration/xai",
    "/integration/meta-conversions-api", "/integration/s3storage",
    "/integration/ainvented",
]

PAGINADOS = [
    "/team-flows", "/flow/bot-fields", "/flow/user-fields", "/flow/subflows",
    "/flow/template-installs", "/templates", "/team/ticket-lists",
    "/flow/tags", "/flow/segments", "/flow/custom-events", "/flow/agents",
    "/flow/inbound-webhooks", "/flow/ai-agents", "/flow/ai-tasks",
    "/flow/chat-button-widgets", "/openai-embeddings",
    "/team-members", "/team/labels", "/team/agent-groups",
]


def redactar(obj):
    """Redacta por NOMBRE de llave y por PATRON de valor. Las dos puertas, siempre."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(v, str) and v and any(s in k.lower() for s in SENSIBLE):
                out[k] = f"<<REDACTADO len={len(v)}>>"
            else:
                out[k] = redactar(v)
        return out
    if isinstance(obj, list):
        return [redactar(x) for x in obj]
    if isinstance(obj, str):
        return redactar_texto(obj)
    return obj


def quedan_secretos(obj):
    """Ultima compuerta antes de escribir: barre el DUMP ya redactado buscando
    cualquier patron que se haya escapado. Si queda uno, el archivo no se escribe."""
    crudo = json.dumps(obj, ensure_ascii=False)
    encontrados = []
    for etiqueta, patron in PATRONES:
        for m in patron.finditer(crudo):
            encontrados.append(f"{etiqueta} ({len(m.group(0))} caracteres)")
    return encontrados


# 🔴 CUPO DE LA API · 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.
# Medido contra la API viva el 2026-09-07: la respuesta trae `x-ratelimit-limit: 1000` y
# `x-ratelimit-remaining: N` (en ingles X-RateLimit-Limit / X-RateLimit-Remaining). Hasta hoy
# NINGUNA skill de la familia leia ese contador: se trabajaba a ciegas y el bloqueo aparecia a
# mitad de la operacion, con la configuracion escrita a medias.
#
# 🔴 COSTE MEDIDO, en dos espacios distintos:
#     espacio de referencia casi VACIO (61 campos) ...... 137   (2026-09-07)
#     espacio REAL (Dolce Incanto, 86 campos) ........... 172   (2026-09-08)
# Las 137 eran el PISO y ya se midio cuanto sube. Por eso la guardia usa 200 y no 137: con 137
# dejaria arrancar una extraccion de un espacio real que NO cabe, y el bloqueo llegaria a mitad
# -- que es exactamente lo que esta guardia existe para evitar. Con 1.000/hora caben ~5.
COSTE_MEDIDO = 200
#
# EL RESET: cada hora (dato del desarrollador via FER). Pero NO viene `x-ratelimit-reset`,
# asi que el servidor no dice A QUE MINUTO empezo la ventana: si te bloqueas, espera una
# hora COMPLETA desde ese momento, y para saber si ya se repuso MIRA el contador (1
# peticion), no lo calcules.
CUPO = {"quedan": None, "limite": None, "leidas": 0}


def _anotar_cupo(resp):
    """Guarda el contador de cada respuesta. Es gratis: viaja en la cabecera que ya llego."""
    try:
        q = resp.headers.get("x-ratelimit-remaining")
        if q is not None:
            CUPO["quedan"] = int(q)
            CUPO["limite"] = int(resp.headers.get("x-ratelimit-limit") or 0) or CUPO["limite"]
            CUPO["leidas"] += 1
    except Exception:                                         # noqa: BLE001
        pass


def informe_cupo():
    """Lo que hay que DECIR al terminar. Un numero sin vara al lado no es un chequeo."""
    if CUPO["quedan"] is None:
        return ("⚠️ el servidor no devolvio 'x-ratelimit-remaining' en ninguna respuesta: "
                "NO se sabe cuanto cupo queda, y eso NO es lo mismo que 'queda de sobra'.")
        # Callarlo seria peor que no mirarlo: el siguiente creeria que hay cupo.
    q, lim = CUPO["quedan"], CUPO["limite"] or 1000
    linea = f"CUPO API: quedan {q} de {lim} peticiones esta hora"
    if q < COSTE_MEDIDO:
        return (f"🔴 {linea}. NO alcanza para otra extraccion (cuesta ~{COSTE_MEDIDO}). "
                "Pasarse BLOQUEA una hora entera.")
    if q < COSTE_MEDIDO * 2:
        return f"⚠️ {linea}. Alcanza para UNA extraccion mas, no dos."
    return f"{linea} · ~{q // COSTE_MEDIDO} extracciones mas"


def pedir(token, path, metodo="GET", cuerpo=None, **params):
    if params:
        path += "?" + urllib.parse.urlencode(params)
    datos = json.dumps(cuerpo).encode() if cuerpo else None
    req = urllib.request.Request(
        BASE + path, data=datos, method=metodo,
        headers={"Authorization": "Bearer " + token, "User-Agent": UA,
                 "Accept": "application/json", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            _anotar_cupo(r)
            return json.load(r)
    except urllib.error.HTTPError as e:
        _anotar_cupo(e)          # el 429 tambien trae la cabecera: es cuando mas importa
        if e.code == 429:
            # 🔴 No se disimula ni se reintenta: reintentar sobre un bloqueo lo alarga. El
            # DUMP queda incompleto y hay que decirlo, porque un inventario a medias sin
            # aviso se lee como el universo entero -- el fallo que esta casa ya pago.
            return {"_ERROR_HTTP": 429,
                    "_detalle": "CUPO AGOTADO (1.000/hora). El bloqueo dura una hora. "
                                "Este DUMP esta INCOMPLETO: no lo audites como si fuera todo."}
        return {"_ERROR_HTTP": e.code,
                "_detalle": e.read()[:300].decode("utf8", "ignore")}
    except Exception as e:                                    # noqa: BLE001
        return {"_ERROR": str(e)}


def todas_las_paginas(token, path):
    """Agota la paginacion. Devuelve (filas, total_declarado_por_el_servidor).

    Dos guardas medidas:
      - si un endpoint ignora ?page= y repite el mismo lote, se corta (no se duplica);
      - se conserva meta.total para que el auditor compruebe que no falto ninguna pagina.
    """
    filas, pagina, previo, total = [], 1, None, None
    while pagina <= 500:
        r = pedir(token, path, page=pagina)
        if "_ERROR" in r or "_ERROR_HTTP" in r:
            return (r if pagina == 1 else filas), total
        meta = r.get("meta") or {}
        if total is None:
            total = meta.get("total")
        lote = r.get("data")
        if not isinstance(lote, list) or not lote:
            break
        huella = json.dumps(lote, sort_keys=True, ensure_ascii=False)
        if huella == previo:
            break
        previo = huella
        filas += lote
        ultima = meta.get("last_page")
        if ultima and pagina >= ultima:
            break
        pagina += 1
    return filas, total


def main():
    # 🔴 COMPROBACION PREVIA. Arrancar una extraccion de ~137 peticiones sin saber si caben
    # es la forma de quedarse bloqueado A MITAD, con el DUMP incompleto. Cuesta 1 peticion
    # saberlo antes; cuesta una hora averiguarlo despues.
    if len(sys.argv) < 3:
        sys.exit(__doc__)

    ruta_token = Path(sys.argv[1])
    if not ruta_token.exists():
        sys.exit(f"No existe el archivo de token: {ruta_token}")
    token = ruta_token.read_text().strip()
    if len(token) < 20 or "TU_TOKEN" in token:
        sys.exit(f"El archivo {ruta_token} no parece un token real ({len(token)} bytes). "
                 "Apunta al deposito, no a un marcador de posicion.")

    # Una peticion barata para saber si CABE la extraccion entera.
    sonda = pedir(token, "/team-info")
    if isinstance(sonda, dict) and sonda.get("_ERROR_HTTP") == 429:
        sys.exit("🔴 CUPO AGOTADO (1.000 peticiones/hora). El bloqueo dura una hora. "
                 "No se arranca la extraccion: quedaria a medias.")
    if CUPO["quedan"] is not None and CUPO["quedan"] < COSTE_MEDIDO:
        sys.exit(f"🔴 NO ARRANCO: quedan {CUPO['quedan']} peticiones de "
                 f"{CUPO['limite'] or 1000} y una extraccion cuesta ~{COSTE_MEDIDO}.\n"
                 f"   Empezar ahora deja el DUMP incompleto Y gasta el resto del cupo.\n"
                 f"   Espera a que se reponga, o corre `golden-chatea-cupo` para verlo.\n"
                 f"   (Si de verdad hace falta un DUMP parcial, se pide a mano y se DECLARA "
                 f"como parcial en el informe -- nunca se audita como si fuera todo.)")
    if CUPO["quedan"] is not None:
        print(f"  cupo antes de empezar: {CUPO['quedan']} de {CUPO['limite'] or 1000} "
              f"· esta extraccion cuesta ~{COSTE_MEDIDO}")

    etiqueta = sys.argv[2]
    salida = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd()

    dump = {
        "_etiqueta": etiqueta,
        "_extraido": datetime.now().isoformat(timespec="seconds"),
        "_token_archivo": str(ruta_token),
        "_conteos": {},
    }

    print(f"Extrayendo '{etiqueta}' ...")

    ident = pedir(token, "/me")
    if "_ERROR_HTTP" in ident:
        codigo = ident["_ERROR_HTTP"]
        pista = ("401 = el token no es valido para este espacio (una copia vieja no se "
                 "resucita, se apunta al deposito)" if codigo == 401 else
                 "1010/403 = falta el User-Agent de navegador" if codigo in (403, 1010)
                 else "")
        sys.exit(f"El token no responde: HTTP {codigo}. {pista}")
    dump["/me"] = redactar(ident)
    print(f"  /me  -> {ident.get('email', '?')}")

    for p in SIMPLES[1:]:
        dump[p] = redactar(pedir(token, p))
        print(f"  {p}")

    for p in PAGINADOS:
        filas, total = todas_las_paginas(token, p)
        dump[p] = redactar(filas)
        n = len(filas) if isinstance(filas, list) else None
        dump["_conteos"][p] = {"traidos": n, "declarados_por_servidor": total}
        marca = ""
        if isinstance(n, int) and isinstance(total, int) and n != total:
            marca = f"  <<< NO CUADRA: servidor declara {total}"
        print(f"  {p}  ({n}){marca}")

    # El prompt COMPLETO de cada agente y tarea de IA: ahi viven metodos de venta y
    # referencias que pueden haber quedado apuntando al vacio.
    def filas_de(clave):
        v = dump.get(clave)
        return v if isinstance(v, list) else []

    dump["_agentes_detalle"] = {}
    for a in filas_de("/flow/ai-agents"):
        ns = a.get("ai_agent_ns") or a.get("ns")
        if ns:
            dump["_agentes_detalle"][ns] = redactar(
                pedir(token, "/flow/ai-agent-info", "POST", {"ai_agent_ns": ns}))
    print(f"  detalle de {len(dump['_agentes_detalle'])} agentes IA")

    dump["_tareas_detalle"] = {}
    for t in filas_de("/flow/ai-tasks"):
        ns = t.get("ai_task_ns") or t.get("ns")
        if ns:
            dump["_tareas_detalle"][ns] = redactar(
                pedir(token, "/flow/ai-task-info", "POST", {"ai_task_ns": ns}))
    print(f"  detalle de {len(dump['_tareas_detalle'])} tareas IA")

    fugas = quedan_secretos(dump)
    if fugas:
        sys.exit("EL DUMP NO SE ESCRIBE: quedaron secretos sin redactar -> "
                 + ", ".join(sorted(set(fugas)))
                 + "\nAnade el patron a PATRONES y repite. Un DUMP con una credencial "
                   "en claro no se guarda ni se comparte.")

    salida.mkdir(parents=True, exist_ok=True)
    destino = salida / f"DUMP-{etiqueta}.json"
    destino.write_text(json.dumps(dump, ensure_ascii=False, indent=1))
    print(f"\nListo -> {destino}  ({destino.stat().st_size:,} bytes)")
    print("  " + informe_cupo())
    print("Siguiente: autoprueba.py y despues auditar.py sobre este DUMP.")


if __name__ == "__main__":
    main()
