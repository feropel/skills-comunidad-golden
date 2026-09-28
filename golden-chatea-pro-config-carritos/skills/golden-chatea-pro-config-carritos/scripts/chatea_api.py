#!/usr/bin/env python3
"""Piezas comunes para hablar con la API de Chatea Pro desde los scripts de esta skill.

No guarda ni imprime el token: lo lee de un archivo (--token-file), que vive en la carpeta
.secrets/ del proyecto del cliente, nunca dentro de la skill.
"""
import http.client
import json
import shutil
import subprocess
import urllib.error
import urllib.request

BASE = "https://chateapro.app/api"
UA = "Mozilla/5.0 golden-carritos"
CAMPO = "[Carritos] Configuracion"
PREFIJO_CACHE = "[Carritos IA] Información de productos"
# Los campos de caché se DESCUBREN por prefijo: fijar "#1" y "#2" dejaba invisible un "#3".
CACHE = [PREFIJO_CACHE + " #1", PREFIJO_CACHE + " #2"]  # solo como referencia del molde


def campos_cache(campos):
    return sorted(n for n in campos if n.startswith(PREFIJO_CACHE))


def u16(s):
    """Como cuenta el contador del panel: cada emoji astral vale 2."""
    return len(str(s).encode("utf-16-le")) // 2


class Api:
    def __init__(self, token_file):
        with open(token_file, encoding="utf-8") as f:
            self.tok = f.read().strip()
        self.cupo = None
        self.por_curl = False  # se enciende si urllib corto y hubo que repetir con curl

    def pedir(self, metodo, ruta, cuerpo=None):
        """Pide a la API. Si urllib entrega una respuesta CORTADA, repite con curl.

        Medido: dentro del sandbox de Claude, urllib devuelve `IncompleteRead` en respuestas
        grandes (los bot fields de un espacio real lo disparan) y la corrida muere a mitad. curl
        las trae completas. Sin este respaldo, la skill funciona a mano y falla en cualquier
        sesion con sandbox o rutina desatendida, que es justo donde nadie la esta mirando."""
        datos = json.dumps(cuerpo, ensure_ascii=False).encode() if cuerpo is not None else None
        req = urllib.request.Request(BASE + ruta, data=datos, method=metodo, headers={
            "Authorization": "Bearer " + self.tok, "User-Agent": UA,
            "Accept": "application/json", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                self.cupo = r.headers.get("x-ratelimit-remaining")
                return json.loads(r.read().decode())
        except (http.client.IncompleteRead, urllib.error.URLError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError):
                raise
            self.por_curl = True
            return self._curl(metodo, ruta, datos)

    def _curl(self, metodo, ruta, datos):
        if not shutil.which("curl"):
            raise RuntimeError("urllib corto la respuesta y no hay curl para repetir la peticion")
        cmd = ["curl", "-sS", "-D", "-", "-X", metodo, BASE + ruta,
               "-H", "Authorization: Bearer " + self.tok, "-H", "User-Agent: " + UA,
               "-H", "Accept: application/json", "-H", "Content-Type: application/json",
               "--max-time", "60"]
        if datos is not None:
            cmd += ["--data-binary", "@-"]
        r = subprocess.run(cmd, input=datos, capture_output=True, check=True)
        salida = r.stdout.decode()
        # El proxy del sandbox antepone su propio bloque ("HTTP/1.1 200 Connection Established"),
        # asi que se consumen TODOS los bloques de cabecera y no solo el primero: partir por el
        # primer separador dejaba el cuerpo empezando en "HTTP/2 200" y json no lo podia leer.
        resto, cabeza = salida, ""
        while resto.startswith("HTTP/"):
            cabeza, _, resto = resto.partition("\r\n\r\n")
            for linea in cabeza.splitlines():
                if linea.lower().startswith("x-ratelimit-remaining:"):
                    self.cupo = linea.split(":", 1)[1].strip()
        codigo = cabeza.split()[1] if len(cabeza.split()) > 1 else "?"
        if codigo.startswith(("4", "5")):
            raise RuntimeError(f"la API respondio {codigo} en {ruta}")
        cuerpo_txt = resto
        return json.loads(cuerpo_txt)

    def campos(self, max_pag=40):
        """Todos los bot fields. Si se agotan las paginas sin terminar, lo DICE (self.parcial):
        una lectura parcial que se declara completa convierte cualquier frente en cobertura falsa."""
        todos, vistos = [], set()
        self.parcial = False
        for page in range(1, max_pag + 1):
            d = self.pedir("GET", f"/flow/bot-fields?page={page}")
            filas = d.get("data", d if isinstance(d, list) else [])
            nuevos = [f for f in filas if f.get("name") not in vistos]
            if not nuevos:
                break
            vistos.update(f.get("name") for f in nuevos)
            todos += nuevos
            if page == max_pag:
                self.parcial = True
        return {f["name"]: f for f in todos}

    def escribir(self, pares):
        """pares = {nombre_campo: valor_python}. Escribe con PUT set-bot-fields-by-name."""
        data = [{"name": n, "value": v if isinstance(v, str) else
                 json.dumps(v, ensure_ascii=False, separators=(",", ":"))} for n, v in pares.items()]
        return self.pedir("PUT", "/flow/set-bot-fields-by-name", {"data": data})

    def plantillas(self):
        """OJO: es POST (con GET da 405) y PAGINA de 10 en 10 en silencio: medido 18-sep, 48
        plantillas en 5 paginas. Sin recorrerlas, una plantilla aprobada de la pagina 2 se
        reportaria como 'no existe'."""
        todas = []
        for page in range(1, 51):
            d = self.pedir("POST", "/whatsapp-template/list", {"limit": 100, "page": page})
            filas = d.get("data", d if isinstance(d, list) else [])
            todas += filas
            ultima = (d.get("meta") or d).get("last_page", 1) if isinstance(d, dict) else 1
            if not filas or page >= int(ultima or 1):
                break
        return todas


def valor(f):
    v = f.get("value")
    if isinstance(v, str):
        try:
            return json.loads(v)
        except ValueError:
            return v
    return v


def get(o, ruta):
    for k in ruta.split("."):
        o = o[k]
    return o


def put(o, ruta, v):
    ks = ruta.split(".")
    for k in ks[:-1]:
        o = o[k]
    o[ks[-1]] = v
