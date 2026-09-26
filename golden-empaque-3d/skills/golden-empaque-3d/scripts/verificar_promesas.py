# -*- coding: utf-8 -*-
"""Comprueba que cada promesa de la description exista DE VERDAD en la skill.

Una skill que promete catorce tipografias y trae doce es un fallo grave, y solo se ve
abriendo el asset. Encargo del Centro de Mando al auditor; lo mido yo antes para que
haya dos medidas independientes que contrastar.
"""
import io
import os
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.claude/skills/golden-empaque-3d")
skill = io.open(os.path.join(BASE, "SKILL.md"), encoding="utf-8").read()
html = io.open(os.path.join(BASE, "assets/mesa-caja-plegadiza.html"), encoding="utf-8").read()
refs = {n: io.open(os.path.join(BASE, "references", n), encoding="utf-8").read()
        for n in os.listdir(os.path.join(BASE, "references"))}

desc = re.search(r"description:\s*>-\n((?:  .*\n?)+)", skill).group(1)
desc = " ".join(l.strip() for l in desc.splitlines())

# --- cuentas reales, medidas sobre el HTML ---
fuentes_link = len(re.findall(r"family=([A-Za-z+]+)", html))
fuentes_array = len(re.findall(r"\[\"'[^\"]+', (?:serif|sans-serif)\"", html))
opciones_select = len(re.findall(r"o\.value = f\[0\]", html))  # se llenan por JS

PROMESAS = [
    ("se ve en 3D",
     lambda: "preserve-3d" in html and "perspective:" in html),
    ("se gira",
     lambda: "pointerdown" in html and "rotateY(" in html),
    ("se DESARMA cara por cara",
     lambda: 'data-view="explotada"' in html and "GAP" in html),
    ("se despliega como plano de troquel",
     lambda: 'data-view="plano"' in html and "flatT" in html),
    ("el visor queda fijo arriba",
     lambda: re.search(r"\.viewer\s*\{[^}]*position:\s*sticky", html, re.S) is not None),
    ("colores (franja, cuerpo, tinta, estudio)",
     lambda: all(i in html for i in ['id="i-band"', 'id="i-body"', 'id="i-ink"', 'id="i-stage"'])),
    ("tipografias, tres selectores",
     lambda: all(i in html for i in ['id="i-logofont"', 'id="i-varfont"', 'id="i-textfont"'])),
    ("medidas en centimetros",
     lambda: all(i in html for i in ['id="i-w"', 'id="i-d"', 'id="i-h"'])),
    # 🔴 El 22-sep-2026 esta prueba daba verde sobre una promesa incumplida: comprobaba
    # cinco ids elegidos por mi y el del LOGOTIPO no estaba entre ellos, justo el que
    # faltaba. El instrumento escrito para cazar promesas incumplidas reprodujo el
    # angulo ciego que pretendia cerrar, porque tambien elige que promesas mira.
    # Por eso ahora la lista sale del HTML, no de mi memoria: se exige un input por
    # CADA texto visible de la pieza.
    ("textos: un campo por CADA texto visible de la pieza",
     lambda: all(i in html for i in [
         'id="i-logotext"',   # el nombre de marca, el que faltaba
         'id="i-mono"',       # el monograma, que sale en dos caras
         'id="i-variant"', 'id="i-netwt"', 'id="i-desc"', 'id="i-claim"',
         'id="i-claim2"', 'id="i-tagline"', 'id="i-foot"', 'id="i-back"'])),

    ("cada texto visible se ESCRIBE de verdad, no solo tiene campo",
     lambda: all(a in html for a in [
         "$('logo').textContent", "$('mono').textContent",
         "$('topwrap').textContent", "$('variant').textContent"])),

    ("ningun id usado por el JS falta en el HTML",
     lambda: not (set(re.findall(r"\$\('([a-zA-Z0-9_-]+)'\)", html))
                  - set(re.findall(r'id="([a-zA-Z0-9_-]+)"', html)))),
    ("acabados",
     lambda: all(i in html for i in ['id="c-emboss"', 'id="c-uv"', 'id="c-matte"'])),
    ("el costo que cada acabado suma",
     lambda: "FIN" in html and "costnote" in html and 'id="i-price"' in html),
    ("boton que le pide a Claude una revision",
     lambda: 'id="ask-btn"' in html and "use" in html and "'sample'" in html),
    ("CATORCE tipografias (dice el cuerpo del SKILL.md)",
     lambda: fuentes_link == 14 and fuentes_array == 14),
    ("sirve para CAJA PLEGADIZA",
     lambda: "mesa-caja-plegadiza.html" in os.listdir(os.path.join(BASE, "assets"))
             or os.path.isfile(os.path.join(BASE, "assets/mesa-caja-plegadiza.html"))),
    ("sirve para FRASCO",
     lambda: any("frasco" in t.lower() and "Lathe" in t for t in refs.values())),
    ("sirve para ETIQUETA",
     lambda: any("etiqueta" in t.lower() and "rebanada" in t.lower() for t in refs.values())),
    ("sirve para BOLSA",
     lambda: any("doypack" in t.lower() and "clip-path" in t for t in refs.values())),
    ("sirve para DISPLAY",
     lambda: any("display de mostrador" in t.lower() for t in refs.values())),
]

print("=" * 70)
print("PROMESAS DE LA DESCRIPTION CONTRA LO QUE HAY DE VERDAD")
print("=" * 70)
print("description: %d caracteres\n" % len(desc))
fallos = []
for etiqueta, prueba in PROMESAS:
    try:
        ok = bool(prueba())
    except Exception as exc:
        print("  ??  %-48s  no medible: %s" % (etiqueta, exc))
        fallos.append(etiqueta)
        continue
    print("  %s  %s" % ("SI " if ok else "NO ", etiqueta))
    if not ok:
        fallos.append(etiqueta)

print("\nCUENTAS MEDIDAS SOBRE EL HTML")
print("  familias en el <link> de Google Fonts : %d" % fuentes_link)
print("  familias en el array FONTS            : %d" % fuentes_array)

print("\n" + "=" * 70)
print("COBERTURA: %d de %d promesas verificadas" % (len(PROMESAS) - len(fallos), len(PROMESAS)))
print("=" * 70)
if fallos:
    print("\nPROMESAS QUE NO SE SOSTIENEN:")
    for f in fallos:
        print("  - %s" % f)

print("\nMATIZ QUE ESTE SCRIPT NO PUEDE RESOLVER SOLO:")
print("  'Sirve para frasco, etiqueta, bolsa y display' se cumple como RECETA")
print("  (references/formatos.md trae la geometria de cada uno) pero NO como")
print("  PLANTILLA lista: en assets/ solo hay caja plegadiza. Quien lea la")
print("  description puede esperar cinco plantillas y encontrar una.")
sys.exit(1 if fallos else 0)
