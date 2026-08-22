#!/usr/bin/env python3
"""
SECRETOS · golden-chatea-operacion

Fuente UNICA de los patrones de redaccion de credenciales, compartida por `extraer.py` (la
compuerta que bloquea la escritura del DUMP) y `clasificar.py` (la evidencia citada de cada
hallazgo). Antes de este archivo, cada script mantenia su PROPIA copia de la lista y
`references/api.md` (lineas ~119-125) AFIRMABA que estaban sincronizadas -- no era cierto:
`extraer.py` tenia 11 familias, `clasificar.py` tenia 17, y el umbral de `SanctumBearer` era
distinto en cada uno (`{32,}` en extraer.py, `{20,}` en clasificar.py). El defecto
`CREDENCIALES-AMPLIADAS` de la ronda de verificacion anterior NO lo detecto porque su unica
prueba directa importaba `redactar_texto` de `clasificar.py`, nunca del camino real que escribe
el DUMP en disco (`extraer.py`) -- exactamente el bug de raiz que este archivo corrige: ya no
hay DOS copias que puedan desincronizarse, hay UNA que los dos scripts importan.

Hallazgo F3, golden-verificador 2026-08-22. Si aparece una familia nueva de credencial, se
agrega SOLO aqui -- nunca en `extraer.py` ni en `clasificar.py` por separado.
"""

import re

# Umbral elegido para SanctumBearer: {20,} (el MAS ESTRICTO de los dos que existian --
# el minimo mas bajo atrapa MAS casos, no menos). Un bearer Sanctum real de Laravel es
# "<id numerico>|<hash>"; el hash puede ser mas corto que 32 caracteres segun la config
# del proyecto, y un umbral de 32 dejaba pasar en claro un token real mas corto.
PATRONES_SECRETO = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),           # cubre sk-ant- tambien
    ("ElevenLabs", re.compile(r"sk_[A-Za-z0-9]{24,}")),
    ("StripeSecret", re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{10,}")),
    ("StripeWebhook", re.compile(r"whsec_[A-Za-z0-9]{10,}")),
    ("MercadoPago", re.compile(r"(?:APP_USR|TEST)-[A-Za-z0-9\-]{10,}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("Meta", re.compile(r"EAA[A-Za-z0-9]{40,}")),
    ("Shopify", re.compile(r"shp(?:at|ss|ca)_[A-Fa-f0-9]{20,}")),
    ("xAI", re.compile(r"xai-[A-Za-z0-9]{20,}")),
    ("Google", re.compile(r"AIza[A-Za-z0-9_\-]{30,}")),
    ("GoogleOAuthRefresh", re.compile(r"1//0[A-Za-z0-9_\-]{20,}")),
    ("SanctumBearer", re.compile(r"\b\d+\|[A-Za-z0-9]{20,}\b")),
    ("GitHubToken", re.compile(r"(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}")),
    ("AWSAccessKey", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("SlackToken", re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("SendGrid", re.compile(r"SG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}")),
    # Bearer generico hexadecimal largo (64 caracteres, forma comun de un token opaco de
    # sesion o de API): mas ancho que los anteriores a proposito, va AL FINAL para no
    # tapar coincidencias mas especificas primero.
    ("HexBearerGenerico", re.compile(r"\b[0-9a-fA-F]{64}\b")),
]


def redactar_texto(t):
    """Sustituye cualquier coincidencia de PATRONES_SECRETO por un marcador que declara
    la familia y el largo, nunca el valor. Usada por extraer.py (la compuerta que
    bloquea la escritura del DUMP) y por clasificar.py (toda evidencia citada)."""
    for etiqueta, patron in PATRONES_SECRETO:
        t = patron.sub(lambda m: f"<<REDACTADO {etiqueta} len={len(m.group(0))}>>", t)
    return t


def quedan_secretos(obj_json_texto):
    """Recibe el texto YA serializado (json.dumps) de un objeto y devuelve la lista de
    familias que todavia aparecen SIN redactar. Usada como compuerta final antes de
    escribir cualquier archivo a disco."""
    encontrados = []
    for etiqueta, patron in PATRONES_SECRETO:
        for m in patron.finditer(obj_json_texto):
            encontrados.append(f"{etiqueta} ({len(m.group(0))} caracteres)")
    return encontrados
