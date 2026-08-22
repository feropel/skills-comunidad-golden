#!/usr/bin/env python3
"""
EXTRACTOR · golden-chatea-operacion

Barre las conversaciones de UN DIA (o de la ventana pedida) de un espacio de Chatea Pro y deja
un DUMP con el hilo COMPLETO de cada contacto. Es la FASE 1 (inventario): sin este archivo no
hay denominador y no hay informe.

Uso:
    python3 extraer.py <archivo-token> <etiqueta> <fecha-AAAA-MM-DD> [carpeta-salida]

Ejemplo:
    python3 extraer.py .secrets/token-golden.txt golden 2026-08-19 ./operacion

Escribe: <carpeta-salida>/DUMP-<etiqueta>-<fecha>.json

SEGURIDAD: un cliente puede pegar por error un token o una contrasena dentro del chat. Este
script REDACTA por patron de valor (no solo por nombre de llave) antes de escribir el DUMP, y
tiene una compuerta final que bloquea la escritura si queda un secreto reconocible. No se
desactiva.

TRAMPA P1/P2 (ver references/api.md): la descarga del hilo usa SIEMPRE `include_bot=1` y
SIEMPRE `user_ns` (nunca `subscriber_id`). Los dos estan codificados como literales en
`descargar_hilo`, no como parametros opcionales que alguien pueda omitir sin querer.

TRAMPA del listado de contactos: el encargo original no fija el endpoint exacto para listar
contactos con ventana de fecha (a diferencia de bot-users-count, chat-messages y get-info, que
si estan medidos contra el servidor real). Este script prueba una lista de candidatos
razonables, usa el primero que responda 200 con una lista, y DECLARA en el DUMP cual uso. Antes
de la primera corrida real, se confirma contra la pestana de red del panel y, si el endpoint
correcto es otro, se ajusta CANDIDATOS_LISTADO aqui abajo -- no se corrige a ciegas.
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

# CONFIRMADO contra un token real (espacio LIBIDOUP, 2026-08-21): el endpoint que existe es
# `/subscribers` (sin prefijo /subscriber ni /flow). Los tres candidatos originales
# (/subscriber/list, /flow/subscribers, /subscriber/get-list) dan 404 en el servidor real -- se
# dejan aqui abajo solo como fallback por si otro espacio/version los tiene.
#
# TRAMPA P14 (nueva, medida): `/subscribers` NO filtra por `from_date`/`to_date` ni por ninguna
# variante probada (`date_from/date_to`, `start_date/end_date`, `subscribed_from/to`) -- las
# cuatro devuelven el MISMO total sin filtrar. No hay ventana de fecha en el servidor para este
# endpoint. `listar_contactos_del_dia` compensa: pagina el universo COMPLETO (barato, 10 por
# pagina) y filtra en cliente por actividad ese dia, usando `last_message_at` primero (la senal
# mas cercana a "hubo conversacion ese dia"), con `last_interaction` y `subscribed` como
# respaldo si `last_message_at` viene vacio. Queda declarado en el DUMP cual campo decidio cada
# contacto. LIMITACION DECLARADA: un contacto cuya conversacion cruza mas de un dia con su
# `last_message_at` cayendo en un dia POSTERIOR al pedido no aparece en el universo de un dia
# anterior aunque haya tenido mensajes ese dia -- el servidor no expone actividad por dia, solo
# el ultimo momento.
CANDIDATOS_LISTADO = [
    "/subscribers",
    "/subscriber/list",
    "/flow/subscribers",
    "/subscriber/get-list",
]

PATRONES = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),
    ("ElevenLabs", re.compile(r"sk_[A-Za-z0-9]{24,}")),
    ("StripeLive", re.compile(r"sk_live_[A-Za-z0-9]{10,}")),
    ("StripeRestricted", re.compile(r"rk_live_[A-Za-z0-9]{10,}")),
    ("MercadoPago", re.compile(r"APP_USR-[A-Za-z0-9\-]{10,}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("Meta", re.compile(r"EAA[A-Za-z0-9]{40,}")),
    ("Shopify", re.compile(r"shpat_[A-Fa-f0-9]{20,}")),
    ("xAI", re.compile(r"xai-[A-Za-z0-9]{20,}")),
    ("Google", re.compile(r"AIza[A-Za-z0-9_\-]{30,}")),
    # Bearer con forma Sanctum (id|hash) — el framework de Chatea Pro es Laravel, y
    # esa es la forma de token que emite Sanctum. Medido en verificacion adversarial:
    # sin este patron, un token de ese formato pegado por error en un chat se filtraba
    # entero al DUMP.
    ("SanctumBearer", re.compile(r"\b\d+\|[A-Za-z0-9]{32,}\b")),
]

SENSIBLE = ("token", "api_key", "apikey", "secret", "password", "access_token",
            "key", "client_secret", "authorization")


def redactar_texto(t):
    for etiqueta, patron in PATRONES:
        t = patron.sub(lambda m: f"<<REDACTADO {etiqueta} len={len(m.group(0))}>>", t)
    return t


def redactar(obj):
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
    crudo = json.dumps(obj, ensure_ascii=False)
    encontrados = []
    for etiqueta, patron in PATRONES:
        for m in patron.finditer(crudo):
            encontrados.append(f"{etiqueta} ({len(m.group(0))} caracteres)")
    return encontrados


def pedir(token, path, **params):
    """SOLO LEE. A diferencia de la hermana (que necesita PUT/POST para auditar
    escritura), esta skill nunca escribe en Chatea -- el encargo lo exige y
    SKILL.md lo declara. Por eso `metodo` no es un parametro: no existe forma de
    llamar a esta funcion con otra cosa que no sea GET. Es una garantia
    ESTRUCTURAL, no de disciplina de quien llama."""
    if params:
        path += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        BASE + path, method="GET",
        headers={"Authorization": "Bearer " + token, "User-Agent": UA,
                 "Accept": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"_ERROR_HTTP": e.code,
                "_detalle": e.read()[:300].decode("utf8", "ignore")}
    except Exception as e:                                       # noqa: BLE001
        return {"_ERROR": str(e)}


def _fecha_de(contacto):
    """P14: `last_message_at` primero (mas cerca de 'hubo charla ese dia'), luego
    `last_interaction`, luego `subscribed` como ultimo respaldo. Devuelve (fecha_AAAA-MM-DD,
    campo_usado) o (None, None) si los tres vienen vacios."""
    for campo in ("last_message_at", "last_interaction", "subscribed"):
        v = contacto.get(campo)
        if v:
            return v[:10], campo
    return None, None


def listar_contactos_del_dia(token, fecha):
    """Prueba los candidatos de endpoint hasta encontrar uno que responda 200 con una lista.
    Para `/subscribers` (P14: no filtra por fecha en el servidor), pagina el universo COMPLETO
    y filtra en cliente por actividad de `fecha`. Para los demas candidatos (si alguno llega a
    responder), respeta el filtro de servidor via from_date/to_date como antes.
    Devuelve (contactos_del_dia, endpoint_usado, total_declarado_por_servidor_para_el_dia,
    campo_fecha_por_ns, universo_completo_declarado_por_servidor). El 3er valor es None cuando
    el servidor no da un total POR DIA (caso /subscribers); el 5to siempre lleva el total bruto
    que sí dio el servidor, para declarar contexto sin usarlo como denominador del día."""
    for ep in CANDIDATOS_LISTADO:
        sin_filtro_de_servidor = (ep == "/subscribers")
        params = {"page": 1} if sin_filtro_de_servidor else {
            "from_date": fecha, "to_date": fecha, "page": 1}
        r = pedir(token, ep, **params)
        if "_ERROR" in r or "_ERROR_HTTP" in r:
            continue
        lote = r.get("data") if isinstance(r, dict) else r
        if isinstance(lote, list):
            filas = list(lote)
            pagina = 2
            meta = r.get("meta") or {}
            total = meta.get("total")
            ultima = meta.get("last_page")
            while ultima and pagina <= ultima and pagina <= 500:
                params2 = {"page": pagina} if sin_filtro_de_servidor else {
                    "from_date": fecha, "to_date": fecha, "page": pagina}
                r2 = pedir(token, ep, **params2)
                lote2 = r2.get("data") if isinstance(r2, dict) else None
                if not isinstance(lote2, list) or not lote2:
                    break
                filas += lote2
                pagina += 1
            if not sin_filtro_de_servidor:
                return filas, ep, total, {}, total
            # filtro en cliente por actividad del dia pedido. El servidor no declara un total
            # POR DIA para este endpoint (total=meta.total es el universo completo, no el del
            # dia) -- devolver ese numero como "declarado" haria que clasificar.py comparara
            # peras con manzanas y abortara con "no_cuadra" sobre un desacople que no es un
            # fallo real. Se devuelve None: clasificar.py lo declara "no_medible" (avisa, no
            # aborta) tal como esta disenado para cuando el servidor no da un total fiable.
            del_dia = []
            campo_por_ns = {}
            for c in filas:
                fch, campo = _fecha_de(c)
                if fch == fecha:
                    del_dia.append(c)
                    ns = c.get("user_ns") or c.get("ns") or c.get("id")
                    campo_por_ns[ns] = campo
            return del_dia, ep, None, campo_por_ns, total
    return None, None, None, {}, None


MAX_PAG_HILO = 12   # golden-logistica-diaria midio: con 5 se truncaba el 5% de los hilos


def descargar_hilo(token, user_ns):
    """TRAMPA P1/P2: include_bot=1 y user_ns son LITERALES, no opcionales.
    include_note=1 e include_system=1 se piden tambien (igual que
    golden-logistica-diaria/scripts/barrer_chats.py, que barre el mismo endpoint):
    las notas de pixel HAY que traerlas para poder excluirlas con evidencia (P5) en
    vez de asumir que no vinieron. PAGINA hasta MAX_PAG_HILO: un hilo largo sin
    paginar es un hilo incompleto con un `200 ok` que no lo delata."""
    base = pedir(token, "/subscriber/chat-messages", user_ns=user_ns,
                include_bot=1, include_note=1, include_system=1)
    if "_ERROR" in base or "_ERROR_HTTP" in base:
        return None, base, None
    mensajes = list(base.get("data") or []) if isinstance(base, dict) else []
    meta = (base.get("meta") or {}) if isinstance(base, dict) else {}
    ultima_pagina = meta.get("last_page") or 1
    truncado = ultima_pagina and ultima_pagina > MAX_PAG_HILO
    for pagina in range(2, min(ultima_pagina, MAX_PAG_HILO) + 1):
        r = pedir(token, "/subscriber/chat-messages", user_ns=user_ns,
                 include_bot=1, include_note=1, include_system=1, page=pagina)
        lote = r.get("data") if isinstance(r, dict) else None
        if not isinstance(lote, list) or not lote:
            break
        mensajes += lote
    aviso = None
    if truncado:
        aviso = {"ns": user_ns,
                 "razon": f"conversacion de {ultima_pagina} paginas, se leyeron "
                          f"{MAX_PAG_HILO}: el hilo quedo TRUNCADO"}
    sin_ts = sum(1 for m in mensajes if not m.get("ts"))
    if sin_ts and not aviso:
        aviso = {"ns": user_ns,
                 "razon": f"{sin_ts} de {len(mensajes)} mensajes sin 'ts': el orden de "
                          "ese hilo no es de fiar salvo que TODOS carezcan de ts "
                          "(ver invertir_hilo en clasificar.py)"}
    return mensajes, None, aviso


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)

    ruta_token = Path(sys.argv[1])
    if not ruta_token.exists():
        sys.exit(f"No existe el archivo de token: {ruta_token}")
    token = ruta_token.read_text().strip()
    if len(token) < 20 or "TU_TOKEN" in token:
        sys.exit(f"El archivo {ruta_token} no parece un token real ({len(token)} bytes). "
                 "Apunta al deposito, no a un marcador de posicion.")

    etiqueta = sys.argv[2]
    fecha = sys.argv[3]
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        sys.exit(f"La fecha '{fecha}' no es AAAA-MM-DD.")
    salida = Path(sys.argv[4]) if len(sys.argv) > 4 else Path.cwd()

    dump = {
        "_etiqueta": etiqueta,
        "_fecha": fecha,
        "_extraido": datetime.now().isoformat(timespec="seconds"),
        "_token_archivo": str(ruta_token),
        "_conteos": {},
    }

    print(f"Extrayendo operacion de '{etiqueta}' para {fecha} ...")

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

    dump["/flow/bot-users-count"] = redactar(pedir(token, "/flow/bot-users-count"))
    print(f"  /flow/bot-users-count  -> {dump['/flow/bot-users-count']}")

    (contactos, endpoint_usado, total_declarado, campo_fecha_por_ns,
     universo_completo) = listar_contactos_del_dia(token, fecha)
    dump["_listado_endpoint_usado"] = endpoint_usado
    dump["_listado_filtra_fecha_en_servidor"] = endpoint_usado != "/subscribers"
    dump["_listado_campo_fecha_por_ns"] = campo_fecha_por_ns
    dump["_listado_universo_completo_del_espacio"] = universo_completo
    if contactos is None:
        sys.exit(
            "No se pudo listar contactos del dia con ninguno de los endpoints candidatos "
            f"{CANDIDATOS_LISTADO}. Esto NO esta entre las trampas ya medidas del encargo: "
            "confirma el endpoint correcto en la pestana de red del panel de Chatea y ajusta "
            "CANDIDATOS_LISTADO en este script. No se inventa un universo vacio."
        )
    print(f"  listado de contactos -> endpoint '{endpoint_usado}', "
          f"{len(contactos)} traidos, {total_declarado} declarados por el servidor")

    dump["_conteos"]["contactos_del_dia"] = {
        "traidos": len(contactos), "declarados_por_servidor": total_declarado}

    dump["contactos"] = []
    errores = []
    avisos = []
    for c in contactos:
        user_ns = c.get("user_ns") or c.get("ns") or c.get("id")
        if not user_ns:
            errores.append({"contacto": redactar(c), "motivo": "sin user_ns"})
            continue
        info = redactar(pedir(token, "/subscriber/get-info", user_ns=user_ns))
        mensajes, error, aviso = descargar_hilo(token, user_ns)
        if error is not None:
            errores.append({"user_ns": user_ns, "motivo": error})
            mensajes = []
        if aviso is not None:
            avisos.append(aviso)
        dump["contactos"].append({
            "user_ns": user_ns,
            "resumen": redactar(c),
            "get_info": info,
            "mensajes": redactar(mensajes),
        })

    dump["_hilos_no_descargados"] = redactar(errores)
    dump["_avisos_de_hilo"] = redactar(avisos)
    dump["_conteos"]["hilos_descargados"] = {
        "ok": len(dump["contactos"]) - len(
            [c for c in dump["contactos"] if not c["mensajes"]]),
        "total_contactos": len(dump["contactos"]),
        "fallidos": len(errores),
    }
    print(f"  hilos descargados: {len(dump['contactos'])} contactos, "
          f"{len(errores)} fallidos, {len(avisos)} avisos (truncados o sin ts)")

    fugas = quedan_secretos(dump)
    if fugas:
        sys.exit("EL DUMP NO SE ESCRIBE: quedaron secretos sin redactar -> "
                 + ", ".join(sorted(set(fugas)))
                 + "\nAnade el patron a PATRONES y repite. Un DUMP con una credencial "
                   "en claro no se guarda ni se comparte.")

    salida.mkdir(parents=True, exist_ok=True)
    destino = salida / f"DUMP-{etiqueta}-{fecha}.json"
    destino.write_text(json.dumps(dump, ensure_ascii=False, indent=1))
    print(f"\nListo -> {destino}  ({destino.stat().st_size:,} bytes)")
    print("Siguiente: autoprueba.py y despues clasificar.py sobre este DUMP.")


if __name__ == "__main__":
    main()
