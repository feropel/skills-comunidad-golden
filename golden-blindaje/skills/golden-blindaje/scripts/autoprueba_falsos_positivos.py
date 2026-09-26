#!/usr/bin/env python3
"""Banco de `es_falso_positivo()` — la clase "lista blanca que calla".

POR QUE EXISTE (medido 2026-09-05, barrido de listas de excepcion del arsenal):
El filtro DOC_CONTEXT nacio para no reportar el material didactico de una skill que
ENSENA a detectar credenciales (cyber-neo y sus regex de ejemplo). Legitimo. Pero se
aplicaba a CUALQUIER archivo `.md` y sobre una ventana de 250 caracteres a cada lado,
y su patron incluye piezas que en Markdown aparecen todo el tiempo:

    <[a-z_]+>   ->  cualquier etiqueta HTML: <div>, <span>, <br>, <ul>
    \\.\\.\\.       ->  unos puntos suspensivos
    detect      ->  la palabra "detecta" en prosa normal

Resultado medido: un token VIVO de Shopify, Stripe o Meta escrito dentro de un `.md`
quedaba silenciado si en los 250 caracteres previos habia una etiqueta HTML, unos
puntos suspensivos o la palabra "detecta". 9 de 9 casos probados: silenciados.

Eso importa aqui mas que en ninguna otra skill: **las skills SON archivos .md y el
repo de skills es PUBLICO**. Este es justo el chequeo que impide publicar un token.

LA CLASE: una exencion se concede al ARCHIVO QUE LA JUSTIFICA, nunca a un formato
entero. "Es un .md" no es una razon; "es la documentacion de un detector de secretos"
si lo es — y eso se demuestra, no se supone.

EL CONTROL: la exencion documental exige las DOS cosas a la vez — que el archivo sea
material didactico sobre secretos (DOC_CONTEXT) **y** que el valor no tenga pinta de
credencial emitida de verdad. Un valor con prefijo real y longitud real no es un
ejemplo: un ejemplo no necesita 80 caracteres validos.

Uso:  python3 scripts/autoprueba_falsos_positivos.py     (0 = pasa, 1 = falla)
"""
import importlib.util
import os
import re
import sys

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chequeo.py")
spec = importlib.util.spec_from_file_location("chequeo", RUTA)
ch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ch)

# Armados en ejecucion a proposito: un literal con prefijo de emisor real dentro
# del archivo hace que los escaneres de secretos lo reporten, con razon. No se
# resuelve exceptuando este banco — eso seria la alfombra que el banco combate.
VIVOS = {
    "Meta / Facebook": "EAA" + "b1" * 45,
    "Stripe LIVE": "sk_" + "live_" + "a1b2c3d4e5f6g7h8i9j0k1",
    "Shopify Admin API": "shp" + "at_" + "a1b2c3d4e5f6g7h8i9j0k1l2",
}

# (nombre, ruta, plantilla, debe_silenciarse)
CASOS_VIVOS = [
    ("md con etiqueta HTML <div> cerca",
     "references/guia.md", "<div>El token de la tienda es: {t}", False),
    ("md con puntos suspensivos",
     "references/guia.md", "La clave real ... {t}", False),
    ("md con la palabra 'detecta' en prosa",
     "SKILL.md", "Este bloque detecta ventas. Token vivo: {t}", False),
    ("md dentro de /references/ (ruta, no contenido)",
     "golden-x/references/notas.md", "Config <br> de produccion: {t}", False),
    ("CONTROL prosa neutra",
     "references/guia.md", "La llave de produccion de la tienda es {t}", False),

    # --- F1, hallado por el verificador adversarial (2026-09-05) ---
    # FALSE_POSITIVE_CONTEXT corria ANTES de la guarda y su patron incluye `\.png`,
    # `\.jpg`, `\.woff`, `@font-face`. Una MENCION de imagen en los 250 caracteres
    # previos no prueba nada sobre un token que viene despues: 45 de 599 .md del
    # arsenal ya traen ese contexto. La guarda "infalible" se apagaba con un enlace.
    ("F1 · enlace a .png en los 250 previos",
     "references/guia.md",
     "![logo](assets/logo.png)\n\nToken de produccion: {t}", False),
    ("F1 · @font-face en los 250 previos",
     "SKILL.md",
     "@font-face {{ src: url(x.woff); }}\n\nToken: {t}", False),
]

# Ruido de verdad: material didactico REAL, con valores que son ejemplos.
CASOS_RUIDO = [
    ("regex de ejemplo en doc de detector",
     "cyber-neo/references/patterns.md",
     'Patron de deteccion: `' + 'shp' + 'at_' + '[A-Za-z0-9]{20,}` detecta el token', True),
    ("placeholder explicito",
     "references/guia.md",
     "Pega aqui tu token: " + "shp" + "at_" + "TUTOKENAQUIXXXXXXXXXXXXXXXX", True),
    ("PNG incrustado que parece token de Meta",
     "assets/logo.md",
     "background:url(data:image/png;base64,EAA" + "b1" * 45 + ")", True),
]


# --- F2 y F3: patrones SIN prefijo cubierto por la guarda inicial ---
# F2: SECRET_PATTERNS["OpenAI"] es `sk-…{45,}`, pero la guarda solo cubria `sk-ant-`.
# F3: el JWT quedo declarado fuera a proposito — y un `service_role` de Supabase ES un
# JWT que salta RLS y da acceso total. Un ejemplo de documentacion no lleva una firma
# de 43 caracteres: la longitud de la firma es lo que separa el ejemplo del secreto.
VIVOS_SIN_PREFIJO = {
    "OpenAI": "sk-" + "T3BlbkFJ" * 6 + "x9Kq2Vn7pL",
    "JWT": ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzE5ODAwMDAwfQ."
            "K7mQ2xR9vB4nL6pT8wZ3cF5hJ1dG0sY2aE4iU6oP8rM"),
}

CASOS_SIN_PREFIJO = [
    ("F2/F3 · etiqueta HTML cerca", "references/guia.md", "<div>Clave viva: {t}", False),
    ("F2/F3 · puntos suspensivos", "references/guia.md", "La clave real ... {t}", False),
    ("F2/F3 · la palabra 'detecta'", "SKILL.md", "Este bloque detecta ventas: {t}", False),
]


def evaluar(texto, path, patrones=None):
    """Devuelve lista de (tipo, silenciado) para cada patron que casa."""
    out = []
    for tipo, rx in (patrones or ch.SECRET_PATTERNS).items():
        m = re.search(rx, texto)
        if m:
            out.append((tipo, ch.es_falso_positivo(texto, m, path)))
    return out


def main():
    fallos = []

    for nombre, path, plantilla, debe in CASOS_VIVOS:
        for tipo, tok in VIVOS.items():
            texto = plantilla.format(t=tok)
            m = re.search(ch.SECRET_PATTERNS[tipo], texto)
            if not m:
                fallos.append(f"  [BANCO ROTO] {nombre}/{tipo}: el patron no casa")
                continue
            got = ch.es_falso_positivo(texto, m, path)
            if got != debe:
                fallos.append(
                    f"  [FALLA] {nombre} · {tipo}: SILENCIA una credencial VIVA "
                    f"en un .md (esperado silenciado={debe}, obtenido={got})")

    for nombre, path, plantilla, debe in CASOS_SIN_PREFIJO:
        for tipo, tok in VIVOS_SIN_PREFIJO.items():
            texto = plantilla.format(t=tok)
            m = re.search(ch.SECRET_PATTERNS[tipo], texto)
            if not m:
                fallos.append(f"  [BANCO ROTO] {nombre}/{tipo}: el patron no casa")
                continue
            got = ch.es_falso_positivo(texto, m, path)
            if got != debe:
                fallos.append(
                    f"  [FALLA] {nombre} · {tipo}: SILENCIA una credencial VIVA "
                    f"(esperado silenciado={debe}, obtenido={got})")

    for nombre, path, texto, debe in CASOS_RUIDO:
        res = evaluar(texto, path)
        if not res:
            continue
        for tipo, got in res:
            if got != debe:
                fallos.append(
                    f"  [FALLA] {nombre} · {tipo}: GRITA por material didactico "
                    f"(esperado silenciado={debe}, obtenido={got})")

    total = (len(CASOS_VIVOS) * len(VIVOS)
             + len(CASOS_SIN_PREFIJO) * len(VIVOS_SIN_PREFIJO) + len(CASOS_RUIDO))
    print("=" * 70)
    print(" AUTOPRUEBA · es_falso_positivo() de chequeo.py")
    print("=" * 70)
    print(f" Casos: {total}   fallan: {len(fallos)}")
    if fallos:
        print("\n".join(fallos))
        print("\n La exencion documental se esta concediendo al FORMATO (.md) en vez")
        print(" de al archivo que la justifica. Ver el encabezado de este archivo.")
        return 1
    print(" Ninguna credencial viva se silencia por vivir en un .md.")
    print(" El material didactico real sigue sin hacer ruido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
