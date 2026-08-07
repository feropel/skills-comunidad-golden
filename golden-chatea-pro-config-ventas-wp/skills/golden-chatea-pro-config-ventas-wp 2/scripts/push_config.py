#!/usr/bin/env python3
"""
push_config.py — Carga la configuración del asistente de ventas de Chatea Pro
(whitelabel de UChat) en CUALQUIER workspace de un cliente, por API. Reusable
para instalaciones en serie: mismo script, distinto token + distintos JSON.

API base:  https://chateapro.app/api   (override con --base)
Auth:      Bearer token del workspace del cliente (Settings -> API Keys)
Endpoints (verificados en vivo 2026-07-09):
  GET  /flow/bot-fields?name=<q>        -> leer/verificar
  PUT  /flow/set-bot-fields-by-name     -> { "data":[ {"name","value"}, ... ] }

El TOKEN nunca se hornea aquí. Orden de búsqueda:
  1) --token <valor>
  2) variable de entorno  CHATEAPRO_TOKEN
  3) archivo              ~/.chatea_pro_token  (primera línea)

Uso:
  # verificar los campos de un workspace
  python3 push_config.py read --name "[Ventas Wp] Configuracion general"

  # respaldar el estado actual ANTES de escribir
  python3 push_config.py backup ./backup.json \
      --name "[Ventas Wp] Configuracion general" \
      --name "[Ventas Wp] Configuracion general 2"

  # empujar (dry-run sin --confirm). Los pares nombre=archivo van ANTES de --confirm:
  python3 push_config.py push \
      "[Ventas Wp] Configuracion general=/ruta/BOTFIELD_1.json" \
      "[Ventas Wp] Configuracion general 2=/ruta/BOTFIELD_2.json" \
      --confirm

NOTAS OPERATIVAS (verificado en vivo 2026-07-09):
  * El token DEBE estar atado al bot/flujo del asistente. Un token sin flujo da
    404 "Flow not found". En Settings -> API Keys, crear el token con el Bot correcto.
  * Cloudflare bloquea urllib sin User-Agent (error 1010); por eso call() manda UA de
    navegador. Con eso, funciona desde Bash directo (no hace falta el navegador).
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error


def get_token(cli_token):
    if cli_token:
        return cli_token.strip()
    tok = os.environ.get("CHATEAPRO_TOKEN")
    if tok:
        return tok.strip()
    path = os.path.expanduser("~/.chatea_pro_token")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.readline().strip()
    sys.exit("Falta el token: usa --token, CHATEAPRO_TOKEN o ~/.chatea_pro_token")


def call(method, path, token, base, body=None, query=None):
    url = base + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/json")
    # UA de navegador para evitar el bloqueo anti-bot de Cloudflare (error 1010)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    req.add_header("Accept-Language", "es-ES,es;q=0.9,en;q=0.8")
    req.add_header("Origin", "https://chateapro.app")
    req.add_header("Referer", "https://chateapro.app/api")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "ignore")[:500]}


def parse_pairs(pairs):
    out = []
    for p in pairs:
        if "=" not in p:
            sys.exit(f"Par inválido (esperado nombre=archivo): {p}")
        name, path = p.split("=", 1)
        with open(path, encoding="utf-8") as f:
            value = f.read()
        json.loads(value)  # el valor debe ser JSON válido
        out.append({"name": name.strip(), "value": value})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["read", "backup", "push"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--token")
    ap.add_argument("--base", default="https://chateapro.app/api")
    ap.add_argument("--name", action="append", default=[])
    ap.add_argument("--confirm", action="store_true")
    a = ap.parse_args()
    token = get_token(a.token)

    if a.cmd == "read":
        nombres = a.name or a.args
        for n in nombres:
            st, resp = call("GET", "/flow/bot-fields", token, a.base, query={"name": n})
            items = resp.get("data", resp) if isinstance(resp, dict) else resp
            print(f"[{st}] {n}")
            if isinstance(items, list):
                for it in items:
                    print(f"    id={it.get('id')} name={it.get('name')!r} len={len(str(it.get('value','')))}")
            else:
                print("   ", str(resp)[:300])

    elif a.cmd == "backup":
        dest = a.args[0] if a.args else "backup-bot-fields.json"
        respaldo = []
        for n in a.name:
            st, resp = call("GET", "/flow/bot-fields", token, a.base, query={"name": n})
            respaldo.append({"name": n, "status": st, "response": resp})
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(respaldo, f, ensure_ascii=False, indent=2)
        print(f"Respaldo en {dest}")

    elif a.cmd == "push":
        data = parse_pairs(a.args)
        for d in data:
            print(f"  preparado: {d['name']}  ({len(d['value'])} chars)")
        if not a.confirm:
            print("\nDRY-RUN: nada enviado. Repite con --confirm para escribir.")
            return
        st, resp = call("PUT", "/flow/set-bot-fields-by-name", token, a.base, body={"data": data})
        print(f"\n[{st}] {str(resp)[:400]}")
        if not 200 <= st < 300:
            print("FALLÓ ❌")
            sys.exit(1)
        # HTTP 200 NO significa que se guardó completo: si el valor excede el tope
        # del TIPO de campo (JSON=20000, LONG JSON=500000) la API TRUNCA EN SILENCIO
        # y responde ok igual. Verificado en vivo el 2026-07-25. Por eso se relee
        # y se compara SIEMPRE; sin esto un push puede mutilar la config sin avisar.
        print("\nVerificando lo que quedó guardado (la API trunca en silencio)...")
        malos = []
        for d in data:
            st2, resp2 = call("GET", "/flow/bot-fields", token, a.base,
                              query={"name": d["name"]})
            items = resp2.get("data", []) if isinstance(resp2, dict) else []
            campo = next((i for i in items if i.get("name") == d["name"]), None)
            if campo is None:
                print(f"  ⚠️  {d['name']}: no se pudo releer (HTTP {st2})")
                malos.append(d["name"])
                continue
            guardado = str(campo.get("value") or "")
            tipo = campo.get("var_type")
            if guardado == d["value"]:
                print(f"  ✅ {d['name']}  {len(guardado)} chars  ({tipo}) íntegro")
            else:
                perdidos = len(d["value"]) - len(guardado)
                print(f"  ❌ {d['name']}  ({tipo}) enviados {len(d['value'])} "
                      f"pero guardados {len(guardado)} — faltan {perdidos}")
                if tipo != "longtext":
                    print(f"     → el campo es '{tipo}' (tope 20000). Cámbialo a "
                          f"LONG JSON en la UI para llegar a 500000.")
                malos.append(d["name"])
        if malos:
            print("\nFALLÓ ❌ — configuración TRUNCADA en: " + ", ".join(malos))
            sys.exit(1)
        print("\nOK ✅ todo guardado íntegro.")


if __name__ == "__main__":
    main()
