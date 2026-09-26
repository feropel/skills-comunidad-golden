#!/usr/bin/env python3
"""Piezas comunes para hablar con la API de Chatea Pro desde los scripts de esta skill.

No guarda ni imprime el token: lo lee de un archivo (--token-file), que vive en la carpeta
.secrets/ del proyecto del cliente, nunca dentro de la skill.
"""
import json
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

    def pedir(self, metodo, ruta, cuerpo=None):
        datos = json.dumps(cuerpo, ensure_ascii=False).encode() if cuerpo is not None else None
        req = urllib.request.Request(BASE + ruta, data=datos, method=metodo, headers={
            "Authorization": "Bearer " + self.tok, "User-Agent": UA,
            "Accept": "application/json", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            self.cupo = r.headers.get("x-ratelimit-remaining")
            return json.loads(r.read().decode())

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
