#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de una mesa de empaque 3D.

    python3 verificar_mesa.py <archivo.html>

Reporta COBERTURA (N de N), nunca un veredicto. Lo que no se pudo medir se declara.
Sale con codigo 1 si hay fallos de LEY, 0 si solo hay avisos.
"""
import io
import os
import re
import sys

LEYES = [
    ("Visor fijo arriba",
     lambda s: re.search(r"\.viewer\s*\{[^}]*position\s*:\s*sticky", s, re.S) is not None,
     "El visor debe llevar position:sticky. Sin eso hay que bajar a escribir y se pierde la pieza."),

    ("Controles debajo del visor, no al lado",
     lambda s: s.find('class="viewer"') < s.find('class="desk"') if 'class="desk"' in s else False,
     "El bloque de controles debe ir DESPUES del visor en el HTML."),

    ("Rotacion libre en las tres vistas",
     lambda s: re.search(r"view\s*===?\s*['\"]plano['\"]\s*\?\s*0\s*:", s) is None,
     "Se detecto la rotacion bloqueada en la vista de plano. Debe girar en las tres."),

    ("Sin Three.js en pieza de caras planas",
     lambda s: ("preserve-3d" in s) and ("three.min.js" not in s),
     "Para caras planas va CSS 3D. Si la pieza tiene curvatura real, este aviso se descarta a mano."),

    ("Costo pegado a los acabados",
     lambda s: ("FIN" in s or "FINISH" in s) and "costnote" in s,
     "Cada acabado debe mostrar cuanto suma por unidad."),
]

GRUPOS = [
    ("Referencia",        r"data-ref="),
    ("Medidas en cm",     r"id=\"i-w\"|id='i-w'"),
    ("Color de franja",   r"id=\"i-band\"|id='i-band'"),
    ("Color de cuerpo",   r"id=\"i-body\"|id='i-body'"),
    ("Color de tinta",    r"id=\"i-ink\"|id='i-ink'"),
    ("Fondo del estudio", r"id=\"i-stage\"|id='i-stage'"),
    ("Posicion de franja", r"data-bm="),
    ("Fuente del logotipo", r"id=\"i-logofont\"|id='i-logofont'"),
    ("Fuente de variante",  r"id=\"i-varfont\"|id='i-varfont'"),
    ("Fuente de texto",     r"id=\"i-textfont\"|id='i-textfont'"),
    ("Tamano de logotipo",  r"id=\"i-logosize\"|id='i-logosize'"),
    ("Interletra",          r"id=\"i-logotrack\"|id='i-logotrack'"),
    ("Orientacion del logotipo", r"data-or="),
    ("Textos de cara trasera",   r"id=\"i-back\"|id='i-back'"),
    ("Acabados",            r"id=\"c-emboss\"|id='c-emboss'"),
    ("Precio de venta",     r"id=\"i-price\"|id='i-price'"),
    ("Guardar versiones",   r"id=\"save-btn\"|id='save-btn'"),
    ("Volver al original",  r"id=\"reset-btn\"|id='reset-btn'"),
    # admite encadenamiento opcional: claude.use('sample') y claude?.use?.('sample')
    ("Opinion de Claude",   r"claude\??\.use\??\.?\(\s*['\"]sample['\"]\s*\)"),
    ("Acercamiento",        r"id=\"i-zoom\"|id='i-zoom'"),
    ("Vista desarmada",     r"data-view=\"explotada\"|data-view='explotada'"),
    ("Plano de troquel",    r"data-view=\"plano\"|data-view='plano'"),
    ("Centrar la vista",    r"id=\"recenter\"|id='recenter'"),
]

HIGIENE = [
    ("Tema claro definido en :root",
     lambda s: re.search(r":root\s*\{[^}]*--ink\s*:", s, re.S) is not None,
     "Los tokens de color se declaran completos en :root."),

    ("Tema oscuro por consulta de medios",
     lambda s: 'prefers-color-scheme: dark' in s and ':root:not([data-theme="light"])' in s,
     "Falta el bloque oscuro protegido, o la pagina se ve rota en modo oscuro del sistema."),

    ("Tema oscuro por atributo",
     lambda s: ':root[data-theme="dark"]' in s,
     "Falta el bloque que gana cuando el visor fuerza oscuro."),

    ("body con fondo explicito",
     lambda s: re.search(r"body\s*\{[^}]*background\s*:\s*var\(", s, re.S) is not None,
     "Un body transparente hereda el fondo del anfitrion y el texto queda ilegible."),

    ("Gutter lateral en movil",
     lambda s: re.search(r"padding\s*:\s*0\s+16px|padding-inline\s*:\s*16px|padding:\s*10px\s+16px", s) is not None,
     "Debe haber al menos 16 px de margen lateral a cualquier ancho."),

    ("localStorage envuelto en try/catch",
     lambda s: (s.count("localStorage") == 0) or
               (len(re.findall(r"try\s*\{[^}]*localStorage", s, re.S)) >= s.count("localStorage.setItem")),
     "En ventana privada localStorage lanza excepcion y tumba la pagina."),

    ("Respeta prefers-reduced-motion",
     lambda s: "prefers-reduced-motion" in s,
     "Falta apagar las animaciones para quien las desactivo."),

    ("Fuentes solo desde Google Fonts",
     lambda s: all(h in ("fonts.googleapis.com", "fonts.gstatic.com")
                   for h in re.findall(r"<link[^>]+href=\"https://([^/\"]+)", s)),
     "El sandbox solo admite Google Fonts como servidor de tipografias."),

    ("Scripts externos solo desde CDN permitido",
     lambda s: all(h in ("cdnjs.cloudflare.com", "cdn.jsdelivr.net", "cdn.tailwindcss.com", "code.jquery.com")
                   for h in re.findall(r"<script[^>]+src=\"https://([^/\"]+)", s)),
     "Cualquier otro origen se bloquea sin error visible."),

    ("display=swap en las fuentes",
     lambda s: ("fonts.googleapis.com" not in s) or ("display=swap" in s),
     "Sin swap la pieza aparece sin texto mientras cargan las fuentes."),

    ("Texto vertical con writing-mode, no rotate",
     lambda s: ("writing-mode" in s) or ("vertical" not in s.lower()),
     "rotate(90deg) saca el bloque de la cara. Va writing-mode."),

    ("Escala calculada, no fija",
     lambda s: "clientHeight" in s,
     "Sin calcular contra el alto del visor, la pieza se sale al cambiar las medidas."),

    ("Se vuelve a ajustar al cambiar el tamano de ventana",
     lambda s: re.search(r"addEventListener\(\s*['\"]resize['\"]", s) is not None,
     "Al girar el telefono la pieza queda cortada."),

    ("Titulo declarado",
     lambda s: re.search(r"<title>[^<]{3,}</title>", s) is not None,
     "El titulo nombra el artefacto en la galeria."),
]

# --------------------------------------------------------------------------
# GUARDAS DE LOS FALLOS QUE YA OCURRIERON.
# Puestas el 22-sep-2026 despues de que el auditor demostrara que la compuerta
# daba 44/44 y exit 0 con los tres fallos del dia reintroducidos a mano.
# Arreglar el caso y escribir la leccion NO instala la guarda: esto la instala.
# --------------------------------------------------------------------------
REINCIDENCIA = [
    ("charset declarado en el HTML",
     lambda s: re.search(r'<meta[^>]+charset\s*=\s*["\']?utf-8', s, re.I) is not None,
     "Sin el meta, fuera del artifact los acentos salen mojibake (Le'cA´terra). "
     "Dentro del artifact no se ve porque el anfitrion lo inyecta."),

    ("viewport declarado en el HTML",
     lambda s: re.search(r'<meta[^>]+name\s*=\s*["\']?viewport', s, re.I) is not None,
     "Es el gemelo del charset. Sin el, el telefono maqueta a 980 px CSS y la Ley 1 "
     "-- el visor fijo arriba -- queda sin efecto justo en el aparato para el que se escribio."),

    ("el plano de troquel entra de frente y quieto",
     lambda s: re.search(r"view\s*===?\s*['\"]plano['\"]\s*\)\s*\{[^}]*setSpin\(false\)[^}]*rx\s*=\s*0", s) is not None,
     "Un troquel se mira de frente. Debe entrar con rx=0, ry=0 y el giro apagado; "
     "girarlo a mano sigue permitido."),

    ("la escala cuenta el hueco de la vista desarmada",
     lambda s: ("explotada" in s and re.search(r"need\s*=", s) is not None
                and re.search(r"explotada['\"]\s*\?\s*\(H\s*\+\s*2\s*\*\s*GAP", s) is not None),
     "Con need = H*1.35 las caras desplegadas se salen del visor: la altura real es "
     "H + 2*GAP + D. Hay que calcularla, no estimarla."),

    ("el nombre de la marca tiene control de texto",
     lambda s: 'id="i-logotext"' in s and "$('logo').textContent" in s,
     "El logotipo tenia control de fuente, tamano, grosor, interletra y orientacion, "
     "de todo menos de lo que dice. La Ley 2 exige que todo lo visible se pueda cambiar."),

    ("cada grupo de casillas de color tiene su listener",
     lambda s: all(re.search(r"\$\('%s'\)\.addEventListener\(\s*['\"]click" % g, s)
                   for g in re.findall(r'id="(\w*sw)"', s)) if re.findall(r'id="(\w*sw)"', s) else True,
     "Reportado por FER el 24-sep-2026: la seleccion de colores no hacia nada. Los dos "
     "addEventListener de #bandsw y #bodysw se habian borrado en un parche. Los CINCO "
     "validadores daban verde, porque comprueban que el control EXISTA, no que HAGA algo."),

    ("todo control de la mesa esta cableado a algo",
     lambda s: not sorted(
         {i for i in re.findall(r'id="(i-[\w-]+|c-[\w-]+)"', s)}
         - {m for m in re.findall(r"on\('([\w-]+)'", s)}
         - {m for m in re.findall(r"\$\('([\w-]+)'\)", s)}),
     "Un control con id en el HTML que el JS nunca toca es un control muerto: se ve, se "
     "puede pulsar y no pasa nada. Es el fallo mas caro de esta mesa porque no da error."),
]


def medir(nombre, pruebas, fuente):
    print("\n" + nombre)
    print("-" * len(nombre))
    fallos = []
    for item in pruebas:
        etiqueta, prueba, porque = item
        try:
            ok = bool(prueba(fuente))
        except Exception as exc:                      # la prueba misma fallo
            print("  ??  %-46s  no se pudo medir: %s" % (etiqueta, exc))
            fallos.append((etiqueta, "no medible"))
            continue
        print("  %s  %s" % ("OK " if ok else "NO ", etiqueta))
        if not ok:
            fallos.append((etiqueta, porque))
    print("  cobertura: %d de %d" % (len(pruebas) - len(fallos), len(pruebas)))
    return fallos


def revisar_skill_propia():
    """La mesa puede estar perfecta y la SKILL no validar. Son cosas distintas.

    Este bloque existe porque el 22-sep-2026 se entrego la skill con una description de
    1382 caracteres sobre un tope de 1024: el validador de la mesa daba 42 de 42 y el
    oficial la rechazaba. Pasar el propio no dice nada de los otros.
    """
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill = os.path.join(base, "SKILL.md")
    if not os.path.isfile(skill):
        return []
    with io.open(skill, "r", encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(r"^---\n(.*?)\n---", src, re.S)
    if not m:
        return [("frontmatter de SKILL.md", "no se encontro el bloque --- ---")]
    fm = m.group(1)
    d = re.search(r"description:\s*>-\n((?:  .*\n?)+)", fm)
    if not d:
        return [("description de SKILL.md", "no se pudo leer")]
    txt = " ".join(l.strip() for l in d.group(1).splitlines())
    print("\nLA SKILL MISMA")
    print("-" * 14)
    fallos = []
    ok = len(txt) <= 1024
    print("  %s  description dentro del tope (%d de 1024)" % ("OK " if ok else "NO ", len(txt)))
    if not ok:
        fallos.append(("description de SKILL.md",
                       "%d caracteres sobre el tope de 1024. El validador oficial la rechaza "
                       "aunque la skill cargue: el truncado del harness ocurre despues, "
                       "cerca de 1536, asi que el fallo NO se ve usandola." % len(txt)))
    tiene_name = re.search(r"^name:\s*\S", fm, re.M) is not None
    print("  %s  frontmatter con name" % ("OK " if tiene_name else "NO "))
    if not tiene_name:
        fallos.append(("name de SKILL.md", "falta la llave name en el frontmatter"))
    print("  cobertura: %d de 2" % (2 - len(fallos)))
    print("\n  Este bloque NO reemplaza a los otros dos validadores. Corre tambien:")
    print("    agentskills validate <carpeta de la skill>")
    print("    ~/.golden/bin/golden-barrido-publicacion <carpeta de la skill>")
    return fallos


def main():
    if len(sys.argv) < 2:
        print("uso: python3 verificar_mesa.py <archivo.html>")
        return 2
    ruta = sys.argv[1]
    if not os.path.isfile(ruta):
        print("no existe el archivo: %s" % ruta)
        return 2

    with io.open(ruta, "r", encoding="utf-8") as fh:
        fuente = fh.read()

    print("=" * 64)
    print("VERIFICACION DE MESA DE EMPAQUE 3D")
    print("archivo: %s  (%d KB)" % (os.path.basename(ruta), len(fuente.encode("utf-8")) // 1024))
    print("=" * 64)

    fallos_ley = medir("LEYES DE LA SKILL", LEYES, fuente)

    print("\nGRUPOS DE CONTROLES")
    print("-" * 19)
    faltan = []
    for etiqueta, patron in GRUPOS:
        ok = re.search(patron, fuente) is not None
        print("  %s  %s" % ("OK " if ok else "NO ", etiqueta))
        if not ok:
            faltan.append(etiqueta)
    print("  cobertura: %d de %d" % (len(GRUPOS) - len(faltan), len(GRUPOS)))

    fallos_hig = medir("HIGIENE DE LA PAGINA", HIGIENE, fuente)
    fallos_rein = medir("GUARDAS DE REINCIDENCIA (fallos ya ocurridos)", REINCIDENCIA, fuente)
    fallos_skill = revisar_skill_propia()

    total = len(LEYES) + len(GRUPOS) + len(HIGIENE) + len(REINCIDENCIA) + 2
    malos = (len(fallos_ley) + len(faltan) + len(fallos_hig)
             + len(fallos_rein) + len(fallos_skill))

    print("\n" + "=" * 64)
    print("COBERTURA TOTAL: %d de %d comprobaciones pasan" % (total - malos, total))
    print("=" * 64)

    if fallos_ley:
        print("\nFALLOS DE LEY (bloquean la entrega):")
        for etiqueta, porque in fallos_ley:
            print("  - %s\n      %s" % (etiqueta, porque))
    if faltan:
        print("\nCONTROLES QUE FALTAN:")
        for etiqueta in faltan:
            print("  - %s" % etiqueta)
    if fallos_hig:
        print("\nHIGIENE POR CORREGIR:")
        for etiqueta, porque in fallos_hig:
            print("  - %s\n      %s" % (etiqueta, porque))
    if fallos_rein:
        print("\nREINCIDENCIA (un fallo que ya ocurrio volvio a entrar):")
        for etiqueta, porque in fallos_rein:
            print("  - %s\n      %s" % (etiqueta, porque))
    if fallos_skill:
        print("\nLA SKILL NO VALIDA (bloquea la entrega):")
        for etiqueta, porque in fallos_skill:
            print("  - %s\n      %s" % (etiqueta, porque))

    print("\nLO QUE ESTE SCRIPT NO MIDE, y hay que hacer a mano:")
    print("  - Abrir la pagina y GIRAR la pieza en las tres vistas")
    print("  - Cambiar un color, una fuente y un texto y ver que responda")
    print("  - Pedir la opinion de Claude y leer lo que contesta")
    print("  - Mirarla a 390 px de ancho y confirmar que no hay scroll horizontal")
    print("  - Confirmar que los numeros de costo son los del proyecto y no los de la plantilla")

    return 1 if (fallos_ley or fallos_rein or fallos_skill) else 0


if __name__ == "__main__":
    sys.exit(main())
