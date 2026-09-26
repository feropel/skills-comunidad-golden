#!/usr/bin/env python3
"""
autoprueba_push.py — Banco de pruebas de scripts/push_config.py SIN tocar un
workspace vivo.

POR QUE EXISTE: hasta hoy el comportamiento de push_config contra la API estaba
confirmado SOLO POR LECTURA DE CODIGO — la reserva declarada en cada auditoria
("no ejecutado, exige token de workspace real y escribiria sobre una cuenta
viva"). Este banco levanta un servidor local que IMITA la API de Chatea Pro y
ejerce las 5 promesas del script contra casos que se SABEN malos:

  1. El PUT usa la llave `data` (con `bot_fields` la API responde 400).
  2. Escribe y RELEE, comparando lo guardado contra lo enviado.
  3. Detecta la TRUNCADA SILENCIOSA: la API responde 200 {"status":"ok"} pero
     guarda el valor CORTADO -> push_config debe FALLAR (exit 1), no dar por
     bueno el 200.
  4. Con todo integro sale exit 0 y dice "todo guardado integro".
  5. Compara el JSON PARSEADO, no el texto crudo (hallazgo golden-skill-auditor
     2026-09-22): la API real recorta el salto de linea final al guardar, y un
     archivo con \n al final (uno editado a mano, por ejemplo) es integro en
     CONTENIDO aunque distinto en BYTES -> push_config NO debe reportar TRUNCADA.

Uso:
    python3 autoprueba_push.py            # corre el banco, imprime N de N
Exit 0 si todas pasan; exit 1 si alguna falla (y dice cual).

LIMITE DECLARADO: esto prueba la LOGICA de push_config (llaves, relectura,
deteccion de truncada), NO la API real de Chatea. Un cambio de contrato del
servidor real seguiria sin detectarse aqui; para eso hace falta un workspace de
control desechable. Es la diferencia entre "simulado y verde" y "probado en vivo".
"""
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PUSH = os.path.join(SCRIPT_DIR, "push_config.py")

# Estado del "servidor Chatea" de mentira
GUARDADO = {}
# Llaves de nivel superior del ultimo PUT recibido (para probar que se manda `data`)
LLAVES_RECIBIDAS = []
# Cualquier campo cuyo nombre contenga esto se guarda CORTADO (truncada silenciosa)
MARCA_TRUNCA = "TRUNCA"
TOPE_FALSO = 40
# Cualquier campo cuyo nombre contenga esto se guarda SIN el salto de linea final -- asi
# se documenta el comportamiento REAL de la API (references/espacio-existente.md), que
# push_config.py comparaba con el texto crudo hasta el hallazgo de golden-skill-auditor
# (2026-09-22): un guardado integro EN CONTENIDO pero distinto EN BYTES se reportaba
# como TRUNCADA. La correccion compara el JSON parseado; este caso prueba que ya no muerde
# donde no debe.
MARCA_RECORTA_NL = "RECORTANL"


class FakeChatea(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass  # silencio: el banco imprime lo suyo

    def _json(self, code, obj):
        cuerpo = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path != "/flow/bot-fields":
            return self._json(404, {"error": "ruta desconocida"})
        nombre = parse_qs(u.query).get("name", [""])[0]
        if nombre not in GUARDADO:
            return self._json(200, {"data": []})
        return self._json(200, {"data": [{
            "id": 1, "name": nombre, "value": GUARDADO[nombre],
            "var_type": "array" if MARCA_TRUNCA in nombre else "longtext",
        }]})

    def do_PUT(self):
        u = urlparse(self.path)
        if u.path != "/flow/set-bot-fields-by-name":
            return self._json(404, {"error": "ruta desconocida"})
        n = int(self.headers.get("Content-Length") or 0)
        try:
            cuerpo = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._json(400, {"error": "json invalido"})
        # PROMESA 1: la API real exige la llave `data`; con `bot_fields` da 400
        LLAVES_RECIBIDAS.clear()
        LLAVES_RECIBIDAS.extend(sorted(cuerpo.keys()))
        if "data" not in cuerpo:
            return self._json(400, {"error": "se esperaba la llave 'data'"})
        for item in cuerpo["data"]:
            val = item.get("value", "")
            # PROMESA 3: truncada SILENCIOSA — corta y responde 200 ok igual
            if MARCA_TRUNCA in item.get("name", ""):
                val = val[:TOPE_FALSO]
            # COMPORTAMIENTO REAL DE LA API: recorta el salto de linea final al guardar
            # (references/espacio-existente.md). El contenido JSON sigue siendo el mismo.
            if MARCA_RECORTA_NL in item.get("name", ""):
                val = val.rstrip("\n")
            GUARDADO[item["name"]] = val
        return self._json(200, {"status": "ok"})


def arrancar():
    srv = HTTPServer(("127.0.0.1", 0), FakeChatea)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_port}"


def correr(base, pares, confirmar=True):
    cmd = [sys.executable, PUSH, "push", *pares, "--token", "FALSO", "--base", base]
    if confirmar:
        cmd.append("--confirm")
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    import tempfile
    srv, base = arrancar()
    tmp = tempfile.mkdtemp()
    integro = os.path.join(tmp, "ok.json")
    with open(integro, "w", encoding="utf-8") as f:
        json.dump({"conexion_con_dropi": {"conectar": "si", "pais": "colombia"}},
                  f, ensure_ascii=False)
    largo = os.path.join(tmp, "largo.json")
    with open(largo, "w", encoding="utf-8") as f:
        json.dump({"texto": "x" * 300}, f, ensure_ascii=False)
    con_salto = os.path.join(tmp, "con_salto.json")
    with open(con_salto, "w", encoding="utf-8") as f:
        json.dump({"conexion_con_dropi": {"conectar": "si", "pais": "mexico"}}, f, ensure_ascii=False)
        f.write("\n")  # a proposito: el archivo termina en salto de linea, como uno editado a mano

    fallos = []
    hechas = []

    def check(nombre, cond, detalle=""):
        hechas.append(nombre)
        print(("  OK   " if cond else "  FALLA") + f" · {nombre}" + (f" :: {detalle}" if not cond and detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("BANCO push_config (servidor Chatea simulado)")

    # 1 · dry-run NO debe escribir nada en el servidor
    GUARDADO.clear()
    rc, out = correr(base, [f"[CampoA]={integro}"], confirmar=False)
    check("dry-run no escribe (sin --confirm)", rc == 0 and not GUARDADO, f"rc={rc} guardado={list(GUARDADO)}")

    # 2 · push integro: exit 0, releido y comparado
    GUARDADO.clear()
    rc, out = correr(base, [f"[CampoA]={integro}"])
    check("push integro -> exit 0", rc == 0, f"rc={rc}")
    check("releyo y confirmo integridad", ("integro" in out.lower() or "\u00edntegro" in out.lower()),
          out.strip().splitlines()[-1:])
    check("el servidor recibio el valor completo", GUARDADO.get("[CampoA]") == open(integro, encoding="utf-8").read())

    # 3 · TRUNCADA SILENCIOSA: 200 ok pero guardado cortado -> debe FALLAR
    GUARDADO.clear()
    rc, out = correr(base, [f"[Campo TRUNCA]={largo}"])
    check("truncada silenciosa -> exit 1 (no se traga el 200 ok)", rc == 1, f"rc={rc}")
    check("el informe dice que fue TRUNCADA", "TRUNCADA" in out or "faltan" in out, "")
    check("y nombra el tipo del campo (array)", "array" in out, "")

    # 4 · PROMESA 1 probada de VERDAD: el servidor recuerda las llaves de nivel superior
    #     que recibio. Si push_config volviera a mandar `bot_fields` (el bug que da 400 en
    #     la API real), esta asercion FALLA. Antes aqui habia un "or True" que no podia
    #     fallar nunca: una prueba que siempre pasa no es prueba, es alfombra.
    GUARDADO.clear(); LLAVES_RECIBIDAS.clear()
    rc, out = correr(base, [f"[CampoA]={integro}"])
    check("el PUT manda EXACTAMENTE la llave 'data' (no 'bot_fields')",
          LLAVES_RECIBIDAS == ["data"], f"recibidas={LLAVES_RECIBIDAS}")
    check("y el servidor lo acepta y guarda", rc == 0 and "[CampoA]" in GUARDADO, f"rc={rc}")

    # 5 · LA API RECORTA EL SALTO DE LINEA FINAL (hallazgo golden-skill-auditor 2026-09-22):
    #     el contenido enviado y el guardado difieren en BYTES (sin el \n) pero son el MISMO
    #     JSON. push_config debe compararlos parseados y decir integro, no TRUNCADA.
    GUARDADO.clear()
    enviado = open(con_salto, encoding="utf-8").read()
    rc, out = correr(base, [f"[Campo RECORTANL]={con_salto}"])
    check("guardado real difiere en bytes del enviado (el caso es real, no un no-op)",
          GUARDADO.get("[Campo RECORTANL]") != enviado,
          f"guardado={GUARDADO.get('[Campo RECORTANL]')!r} enviado={enviado!r}")
    check("push_config compara el JSON parseado: salto de linea final NO es TRUNCADA",
          rc == 0 and ("integro" in out.lower() or "íntegro" in out.lower()), f"rc={rc}\n{out[-300:]}")

    # 6 · CONTRAPRUEBA del banco (que el banco sepa morder): un PUT con `bot_fields`
    #     en vez de `data` DEBE ser rechazado con 400 por el servidor simulado.
    import urllib.request, urllib.error
    req = urllib.request.Request(base + "/flow/set-bot-fields-by-name",
                                 data=json.dumps({"bot_fields": []}).encode(),
                                 method="PUT", headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req); codigo = 200
    except urllib.error.HTTPError as e:
        codigo = e.code
    check("contraprueba: un PUT con 'bot_fields' es rechazado (400)", codigo == 400, f"codigo={codigo}")

    srv.shutdown()
    total = len(hechas)
    print(f"\nCOBERTURA: {total - len(fallos)} de {total} pruebas en verde")
    if fallos:
        print("FALLAN: " + ", ".join(fallos))
        sys.exit(1)
    print("Banco en verde. LIMITE: esto simula la API, no la prueba en vivo.")
    sys.exit(0)


if __name__ == "__main__":
    main()
