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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from secretos import redactar_texto, quedan_secretos as _quedan_secretos_texto  # noqa: E402

BASE = "https://chateapro.app/api"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# CONFIRMADO contra un token real (espacio ESPACIO-REF, 2026-08-21): el endpoint que existe es
# `/subscribers` (sin prefijo /subscriber ni /flow), y ESE es el unico dato confirmado contra
# el servidor real -- que el DUMP se construyo con `/subscribers` (200, universo=486
# contactos totales del espacio ese dia, ver `_listado_universo_completo_del_espacio` en el
# propio DUMP). Los otros tres (/subscriber/list, /flow/subscribers, /subscriber/get-list) NO
# se probaron contra ningun servidor real en esa corrida (F8, golden-verificador 2026-08-22:
# la frase anterior aqui decia que "dan 404 en el servidor real", una afirmacion sin artefacto
# que la respalde -- se corrige: no confirmado, se dejan como fallback por si otro
# espacio/version los necesita, sin asumir que fallan.
#
# TRAMPA-LISTADO (nueva, medida; renombrada para no colisionar con la "trampa 14" documental
# de references/api.md, que es otra cosa -- la API sin saldo/consumo): `/subscribers` NO
# filtra por `from_date`/`to_date` en el servidor -- CONFIRMADO: pedir con y sin esos dos
# parametros devuelve el mismo total. F8 (golden-verificador 2026-08-22): la version anterior
# de este comentario afirmaba "probadas 4 variantes de nombre de parametro, las 4 devuelven el
# mismo total" -- esa medicion de las otras 3 variantes (`date_from/date_to`,
# `start_date/end_date`, `subscribed_from/to`) NO tiene artefacto que la respalde, se retira la
# cifra inventada. Lo confirmado es `from_date`/`to_date` sin filtrar; las demas variantes
# quedan como NO PROBADAS, pendientes de correr contra un token real antes de citarlas como
# medicion. No hay ventana de fecha confirmada en el servidor para este endpoint.
# `listar_contactos_del_dia` compensa: pagina el universo COMPLETO (barato, 10 por
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

SENSIBLE = ("token", "api_key", "apikey", "secret", "password", "access_token",
            "key", "client_secret", "authorization")

# F3 (CRITICO SEGURIDAD, golden-verificador 2026-08-22): la lista de patrones ANTES vivia
# DUPLICADA aqui (11 familias) y en clasificar.py (17 familias) -- references/api.md afirmaba
# que estaban sincronizadas y no era cierto. Ahora las dos importan la MISMA lista de
# `secretos.py` (ver arriba, `from secretos import PATRONES_SECRETO, redactar_texto`); ya no
# hay copia local que redactar_texto() defina aqui.


def redactar(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            # FALLA 6 (golden-verificador, re-auditoria 2026-08-22): antes solo redactaba
            # por nombre de llave sensible cuando el VALOR ademas era `str` -- un secreto
            # bajo una llave sensible (token/api_key/password/...) que llegara como lista,
            # dict o numero (medido: {"token": ["..."]}, {"api_key": {"v": "..."}},
            # {"password": 12345678901234567890}) se saltaba esta rama, caia en el
            # `redactar(v)` recursivo, y salia SIN redactar si su forma no calzaba ademas
            # con una de las 17 familias de `secretos.py` -- la compuerta `quedan_secretos`
            # tampoco lo detectaba (busca por PATRON, no por llave). Ahora cualquier valor
            # no vacio bajo una llave sensible se redacta, sea cual sea su tipo.
            if v not in (None, "", [], {}) and any(s in k.lower() for s in SENSIBLE):
                out[k] = f"<<REDACTADO len={len(str(v))}>>"
            else:
                out[k] = redactar(v)
        return out
    if isinstance(obj, list):
        return [redactar(x) for x in obj]
    if isinstance(obj, str):
        return redactar_texto(obj)
    return obj


def quedan_secretos(obj):
    """F3: compuerta final antes de escribir el DUMP a disco. Usa la MISMA lista de
    `secretos.py` que redacta la evidencia citada en clasificar.py -- una fuente unica,
    no dos listas que se puedan desincronizar."""
    return _quedan_secretos_texto(json.dumps(obj, ensure_ascii=False))


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
    """TRAMPA-LISTADO: `last_message_at` primero (mas cerca de 'hubo charla ese dia'), luego
    `last_interaction`, luego `subscribed` como ultimo respaldo. Devuelve (fecha_AAAA-MM-DD,
    campo_usado) o (None, None) si los tres vienen vacios.

    FALLA 8 (golden-verificador, re-auditoria 2026-08-22): la version anterior hacia
    `v[:10]` sin comprobar el tipo -- confirmado contra produccion, estos tres campos
    llegan como TEXTO ('AAAA-MM-DD HH:MM:SS', ver api.md), pero un valor NUMERICO (la misma
    forma epoch que SI se confirmo para `ts` en el hilo de mensajes) hacia `v[:10]` reventar
    con `TypeError: 'int' object is not subscriptable`, sin capturar -- tumbaba TODA la
    Fase 1 (el listado de contactos del dia) por un solo contacto con un campo en un formato
    no visto aun. Ahora un valor no-texto se trata como 'no utilizable para este campo' (se
    prueba el siguiente campo de respaldo) en vez de adivinar un slice sobre un numero o
    reventar la corrida entera."""
    for campo in ("last_message_at", "last_interaction", "subscribed"):
        v = contacto.get(campo)
        if isinstance(v, str) and v:
            return v[:10], campo
    return None, None


def listar_contactos_del_dia(token, fecha):
    """Prueba los candidatos de endpoint hasta encontrar uno que responda 200 con una lista.
    Para `/subscribers` (TRAMPA-LISTADO: no filtra por fecha en el servidor), pagina el universo COMPLETO
    y filtra en cliente por actividad de `fecha`. Para los demas candidatos (si alguno llega a
    responder), respeta el filtro de servidor via from_date/to_date como antes.
    Devuelve (contactos_del_dia, endpoint_usado, total_declarado_por_servidor_para_el_dia,
    campo_fecha_por_ns, universo_completo_declarado_por_servidor, paginacion). El 3er valor es
    None cuando el servidor no da un total POR DIA (caso /subscribers); el 5to siempre lleva el
    total bruto que sí dio el servidor, para declarar contexto sin usarlo como denominador del
    día. El 6to (F9) declara si la paginación del LISTADO se truncó por el tope de 500 páginas
    y cuántas páginas se trajeron de verdad — nunca implícito."""
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
            # F9 (HUECO, corregido tras verificacion 2026-08-22): el tope de 500 paginas
            # cortaba la paginacion EN SILENCIO -- si un espacio algun dia tiene mas de 500
            # paginas de contactos (5.000 con 10 por pagina), el DUMP quedaba incompleto sin
            # que nada lo declarara. Se registra cuantas paginas se trajeron de verdad y si
            # se llego al tope, para que `clasificar.py` pueda emitir un hallazgo.
            paginas_traidas = 1
            trunco_por_tope_500 = False
            while ultima and pagina <= ultima:
                if pagina > 500:
                    trunco_por_tope_500 = True
                    break
                params2 = {"page": pagina} if sin_filtro_de_servidor else {
                    "from_date": fecha, "to_date": fecha, "page": pagina}
                r2 = pedir(token, ep, **params2)
                lote2 = r2.get("data") if isinstance(r2, dict) else None
                if not isinstance(lote2, list) or not lote2:
                    break
                filas += lote2
                paginas_traidas += 1
                pagina += 1
            paginacion = {
                "paginas_traidas": paginas_traidas,
                "ultima_pagina_declarada_por_servidor": ultima,
                "truncado_por_tope_500": trunco_por_tope_500,
                # Limitacion conocida y DECLARADA (F9), no implicita: si el servidor no
                # manda meta.last_page, este bucle NUNCA pagina mas alla de la primera
                # pagina (la condicion `while ultima and ...` es falsy sin `ultima`) --
                # se trae solo lo que venga en la primera respuesta.
                "sin_meta_last_page_no_pagina": not bool(ultima),
            }
            if not sin_filtro_de_servidor:
                return filas, ep, total, {}, total, paginacion
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
            return del_dia, ep, None, campo_por_ns, total, paginacion
    return None, None, None, {}, None, {}


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
    # FALLA 4 (golden-verificador, re-auditoria 2026-08-22): `meta.get("last_page") or 1`
    # colapsaba DOS casos distintos en el mismo numero -- "el servidor SI declaro 1 pagina"
    # (hilo real de una sola pagina) y "el servidor NO declaro last_page en absoluto" (dato
    # ausente). El listado de contactos (`listar_contactos_del_dia`) SI distingue ese caso
    # (`sin_meta_last_page_no_pagina`, declarado en `_listado_paginacion`); el hilo no tenia
    # el equivalente -- si el servidor omitia `last_page`, este bucle se quedaba en la
    # primera pagina EN SILENCIO, sin ningun aviso que lo declarara.
    ultima_pagina_declarada = meta.get("last_page")
    sin_last_page = not bool(ultima_pagina_declarada)
    ultima_pagina = ultima_pagina_declarada or 1
    truncado = bool(ultima_pagina_declarada) and ultima_pagina > MAX_PAG_HILO
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
    elif sin_last_page:
        aviso = {"ns": user_ns,
                 "razon": "el servidor no declaro meta.last_page para este hilo: no se "
                          "pagino mas alla de la primera pagina (limitacion conocida, "
                          "mismo criterio que sin_meta_last_page_no_pagina del listado de "
                          "contactos) -- puede haber mas mensajes sin traer"}
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
     universo_completo, paginacion_listado) = listar_contactos_del_dia(token, fecha)
    dump["_listado_endpoint_usado"] = endpoint_usado
    dump["_listado_filtra_fecha_en_servidor"] = endpoint_usado != "/subscribers"
    dump["_listado_campo_fecha_por_ns"] = campo_fecha_por_ns
    dump["_listado_universo_completo_del_espacio"] = universo_completo
    dump["_listado_paginacion"] = paginacion_listado
    if paginacion_listado.get("truncado_por_tope_500"):
        print("  AVISO: el listado de contactos se TRUNCO en el tope de 500 paginas -- "
              f"se trajeron {paginacion_listado.get('paginas_traidas')} de "
              f"{paginacion_listado.get('ultima_pagina_declarada_por_servidor')} declaradas "
              "por el servidor. El DUMP queda incompleto, declarado en "
              "_listado_paginacion.")
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
