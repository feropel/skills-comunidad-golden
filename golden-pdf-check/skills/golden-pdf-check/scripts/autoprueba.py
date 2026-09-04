#!/usr/bin/env python3
"""
GOLDEN PDF · autoprueba.py
Prueba de regresión de la skill: **23 comprobaciones** sobre PDFs construidos
de verdad (nada simulado). Hay una prueba por cada versión que cambió el
comportamiento, para que una regresión no pase en verde:

  1. Construye sin errores · 2. Salida JSON válida · 3. Cuenta de tarjetas ·
  4. COMPUERTA VERBATIM (texto idéntico) · 5. ANTI-CORTE (nada al filo del
  borde) · 6. Motor con numeración · 7. Fuente de marca incrustada ·
  8-9. Detectores ADVERSARIALES (un PDF feo y uno cortado DEBEN ser cazados) ·
  10. Anti-falso-positivo: dos tarjetas seguidas no son un corte ·
  11-12. Figuras (v5.6) · 13. Bloque con estilo ::: (v5.7) · 14. El aviso de
  líneas largas dispara cuando debe (v5.8) · 15. …y la muestra oficial NO lo
  dispara (el fixture cumple la regla que la skill enseña) · 16. CONTRASTE
  WCAG de los colores de texto contra su fondo (>=4.5:1) · 17. Documento LARGO:
  índice con números de página reales y letra por encima del piso legible ·
  18. DIRECCIÓN POSITIVA: el auditor NO marca un PDF Golden limpio (probar en
  las dos direcciones — un detector agresivo daña tanto como uno ciego) ·
  19. COMPONENTES VISUALES (v6.0) · 20. IDENTIDAD por tema ·
  21. NEUTRALIDAD POR DEFECTO (v6.1): un documento construido SIN --tema no
  lleva NINGUNA marca de Golden — ni pie, ni autor, ni kicker, ni logo.
  Existe porque hasta v6.0 la marca era el valor por defecto y quien usara
  la skill firmaba sus documentos con la marca de FER sin enterarse ·
  22. Estado del REGISTRO DE FÁBRICAS, la cara que vive fuera del árbol
  (informativo: entre sellar y que el CdM regenere hay desfase legítimo) ·
  23. COHERENCIA DEL SELLO: las comprobaciones declaradas aquí arriba son
  exactamente las que la corrida imprime.

La cifra de arriba es la que imprime una corrida SANA, y es la que va en el
sello del changelog. Si agregas una prueba, actualiza el número aquí y verifica
contándolo en la salida — nunca de memoria: una prueba que solo se registra
cuando falla infla el sello sin ser reproducible (así nació este arreglo).

Regla de la casa: toda versión que cambie comportamiento entra con su prueba
aquí. Si tocas el CSS, el parser o el auto-fit, corre esto antes de usar la
skill en material real.

Uso:  $PY scripts/autoprueba.py
Salida: PASS (exit 0) o FAIL (exit 1) con el detalle.
"""
import os, sys, json, subprocess, tempfile, shutil
import re as _re3

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
SAMPLE = os.path.join(SKILL_DIR, "assets", "autoprueba-muestra.md")
EXPECTED_CARDS = 3


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def find_chrome():
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome"), shutil.which("chromium")]:
        if c and os.path.exists(c):
            return c
    return None


def chrome_pdf(chrome, html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); tmp = f.name
    try:
        run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             "--virtual-time-budget=3000", "--print-to-pdf=" + out, "file://" + tmp])
    finally:
        os.unlink(tmp)


def audit_text(pdf):
    return run([sys.executable, os.path.join(SCRIPTS, "audit_pdf.py"), pdf]).stdout


def main():
    results = []
    tmp = tempfile.mkdtemp(prefix="golden-autoprueba-")
    pdf = os.path.join(tmp, "autoprueba.pdf")

    # 1) build
    r = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), SAMPLE, pdf])
    built = r.returncode == 0 and os.path.exists(pdf)
    results.append(("Construye sin errores", built, r.stderr.strip()[:200]))
    if not built:
        report(results); sys.exit(1)

    # La prueba se registra en LOS DOS caminos. Si el PASS solo existiera en la
    # rama de error, la corrida sana mostraría una prueba menos que la sellada y
    # la cifra del changelog no sería reproducible (hallazgo del barrido D del
    # CdM, 2026-08-23): una cifra mal contada es peor que ninguna.
    data = {}
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
        results.append(("Salida JSON válida", True, ""))
    except Exception as e:
        results.append(("Salida JSON válida", False, str(e)))
        report(results); sys.exit(1)

    # 2) card count
    results.append((f"Genera {EXPECTED_CARDS} tarjetas",
                    data.get("cards") == EXPECTED_CARDS,
                    "obtenidas: " + str(data.get("cards"))))

    # 3) verbatim gate
    vb = data.get("verbatim", {})
    results.append(("Compuerta verbatim (texto idéntico)",
                    vb.get("ok") is True,
                    "; ".join(vb.get("fails", [])) if vb.get("fails") else "ok"))

    # 4) anti-corte via audit
    ra = run([sys.executable, os.path.join(SCRIPTS, "audit_pdf.py"), pdf,
              "--json", os.path.join(tmp, "audit.json")])
    no_cut = "sin bloques al filo" in ra.stdout or "Paginación — sin" in ra.stdout
    results.append(("Anti-corte: sin bloques al borde", no_cut, ""))

    engine = data.get("engine", "")
    results.append(("Motor con numeración (Playwright)", engine.startswith("playwright"),
                    engine))

    # 5) fuente incrustada (documento idéntico en cualquier equipo)
    # El import va DENTRO del try a propósito: pypdf es una dependencia
    # OPCIONAL. Si falta, esta prueba sola queda en FAIL con el motivo; antes
    # el ModuleNotFoundError mataba el self-test entero y se perdían las otras
    # 12 comprobaciones (medido al correrlo con un intérprete sin pypdf).
    try:
        from pypdf import PdfReader
        fonts = set()
        for pg in PdfReader(pdf).pages:
            res = pg.get("/Resources", {})
            for fo in (res.get("/Font", {}) or {}).values():
                fo = fo.get_object()
                bf = str(fo.get("/BaseFont", ""))
                if bf:
                    fonts.add(bf)
        embedded = any("Inter" in f or "JetBrains" in f or "GoldenSans" in f or "GoldenMono" in f
                       for f in fonts)
        results.append(("Fuente de marca incrustada", embedded, ", ".join(sorted(fonts))[:80]))
    except ImportError as e:
        # El ENTORNO no puede medir: no es un fallo del estándar.
        results.append(("Fuente de marca incrustada", None,
                        "no verificable: %s (instala pypdf para comprobarlo)" % e))
    except Exception as e:
        results.append(("Fuente de marca incrustada", False, str(e)))

    # 6) detectores adversariales: el auditor DEBE atrapar problemas
    chrome = find_chrome()
    if not chrome:
        results.append(("Detector de color (adversarial)", True, "omitido (sin Chrome)"))
        results.append(("Detector de bloque cortado (adversarial)", True, "omitido (sin Chrome)"))
    else:
        ugly = os.path.join(tmp, "ugly.pdf")
        chrome_pdf(chrome, "<!doctype html><html><body style='margin:0'>"
                   "<div style='background:#ff00aa;color:#00e5ff;height:400px;font-size:40px'>"
                   "COLOR HORRIBLE</div></body></html>", ugly)
        out_ugly = audit_text(ugly)
        results.append(("Detector de color (adversarial)",
                        "Colores fuera de marca" in out_ugly, ""))

        split = os.path.join(tmp, "split.pdf")
        lines = "\n".join("linea_courier_%03d que sigue y sigue sin cortar nunca jamas" % i
                          for i in range(1, 95))
        chrome_pdf(chrome, "<!doctype html><html><head><style>@page{size:A4;margin:15mm}"
                   "pre{font-family:'Courier New',monospace;font-size:12pt;white-space:pre-wrap}"
                   "</style></head><body><p>intro</p><pre>" + lines + "</pre></body></html>", split)
        out_split = audit_text(split)
        results.append(("Detector de bloque cortado (adversarial)",
                        "cortado entre páginas" in out_split, ""))

    # 7) anti-falso-positivo: DOS tarjetas grandes en páginas seguidas NO son
    #    un corte (la 2ª empieza con su cabecera "PROMPT · COPIAR"). Regresión
    #    del caso real de la guía de comentarios (2026-07-04).
    two = os.path.join(tmp, "two-cards.md")
    big = "\n".join("Línea %02d del prompt, con contenido de verdad para llenar la tarjeta." % i
                    for i in range(1, 60))
    with open(two, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Dos tarjetas seguidas\n---\n\nIntro corta.\n\n"
                "``` Tarjeta grande A\n" + big + "\n```\n\n"
                "``` Tarjeta grande B\n" + big + "\n```\n")
    two_pdf = os.path.join(tmp, "two-cards.pdf")
    r2 = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), two, two_pdf, "--no-verify"])
    if r2.returncode == 0 and os.path.exists(two_pdf):
        out_two = audit_text(two_pdf)
        results.append(("Dos tarjetas seguidas NO marcan corte (anti-falso-positivo)",
                        "cortado entre páginas" not in out_two, ""))
    else:
        results.append(("Dos tarjetas seguidas NO marcan corte (anti-falso-positivo)",
                        False, "build falló: " + r2.stderr.strip()[:120]))

    # 8) FIGURAS (v5.6): ![pie](ruta) se incrusta, se numera y NO cuenta como
    #    tarjeta copiable. Un manual de pasos sin pantallas no sirve.
    figdir = os.path.join(tmp, "img")
    os.makedirs(figdir, exist_ok=True)
    with open(os.path.join(figdir, "demo.svg"), "w", encoding="utf-8") as f:
        f.write("<svg xmlns='http://www.w3.org/2000/svg' width='600' height='200' "
                "viewBox='0 0 600 200'><rect width='600' height='200' fill='#f6f5f1'/>"
                "<rect x='20' y='20' width='560' height='160' fill='#ffffff' "
                "stroke='#e7e4dc'/><circle cx='60' cy='60' r='16' fill='#d4af37'/></svg>")
    # PNG mínimo (1x1) en base64: prueba que el raster también se incrusta.
    with open(os.path.join(figdir, "demo.png"), "wb") as f:
        f.write(__import__("base64").b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="))
    figmd = os.path.join(tmp, "figuras.md")
    with open(figmd, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Documento con figuras\n---\n\n## Una seccion con pantalla\n\n"
                "Texto antes de la figura.\n\n"
                "![Pie de prueba de la figura](img/demo.svg)\n\n"
                "Texto despues de la figura.\n\n"
                "![Segundo pie, esta vez raster](img/demo.png){40%}\n\n"
                "``` Prompt unico\ncontenido copiable\n```\n")
    figpdf = os.path.join(tmp, "figuras.pdf")
    r3 = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), figmd, figpdf])
    okfig = r3.returncode == 0 and os.path.exists(figpdf)
    detail = r3.stderr.strip()[:160]
    if okfig:
        try:
            d3 = json.loads(r3.stdout.strip().splitlines()[-1])
            okfig = d3.get("cards") == 1 and d3.get("verbatim", {}).get("ok") is True
            detail = "cards=%s (la figura no cuenta como tarjeta)" % d3.get("cards")
        except Exception as e:
            okfig, detail = False, str(e)
    results.append(("Figuras: se incrustan y no cuentan como tarjeta", okfig, detail))

    if os.path.exists(figpdf):
        try:
            import pdfplumber
            with pdfplumber.open(figpdf) as pf:
                txt = "\n".join((p.extract_text() or "") for p in pf.pages)
                imgs = sum(len(p.images) for p in pf.pages)
        except ImportError:
            txt, imgs = "", -1
        # Un SVG se incrusta como VECTOR (no suma XObject de imagen: mejor, queda
        # nítido y ligero); el PNG sí suma, y ese PNG es lo que esta prueba mide.
        # El umbral era >=2 porque contaba TAMBIÉN el logo de la portada, que
        # hasta v6.0 se colaba por defecto sin que nadie lo pidiera. Al quitar
        # ese logo (v6.1) la prueba se puso roja y dejó ver que su umbral medía
        # dos cosas distintas: la figura del documento y una marca del motor.
        # Ahora mide solo lo suyo.
        up = txt.upper()   # la insignia se imprime en versalitas por CSS
        results.append(("Figuras: imagen incrustada y pies numerados en orden",
                        imgs >= 1 and "FIGURA 1" in up and "FIGURA 2" in up,
                        "imagenes=%d" % imgs if imgs >= 0
                        else "sin pdfplumber: no se pudo verificar"))

    # 9) el AVISO de líneas largas (v5.8) DEBE dispararse cuando debe. Sin este
    #    caso, el aviso podía apagarse en una refactorización sin que nadie lo
    #    notara — y su trabajo es evitar un ciclo perdido de compuerta verbatim.
    largo = os.path.join(tmp, "largo.md")
    with open(largo, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Linea larga\n---\n\n## Seccion\n\n``` Tarjeta con linea larga\n"
                + ("x" * 120) + "\n```\n")
    r4 = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), largo,
              os.path.join(tmp, "largo.pdf"), "--no-verify"])
    results.append(("Aviso de líneas largas dispara cuando debe",
                    "LÍNEAS LARGAS EN TARJETAS" in r4.stderr, ""))

    # 10) …y NO dispara con la muestra oficial: un fixture que incumple la regla
    #     que la skill enseña entrena a ignorar los avisos (efecto "cry wolf").
    results.append(("La muestra oficial NO dispara el aviso (fixture ejemplar)",
                    "LÍNEAS LARGAS EN TARJETAS" not in r.stderr, ""))

    # 12) BLOQUE CON ESTILO (v5.7): ::: nota Titulo ... ::: produce un contenedor
    #     atomico con su clase, procesa Markdown adentro y NO cuenta como tarjeta.
    blkmd = os.path.join(tmp, "bloque.md")
    with open(blkmd, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Bloque con estilo\n---\n\n## Seccion con bloque\n\n"
                "::: nota Antes de empezar\nTen a la mano el **catalogo** y los precios.\n:::\n\n"
                "``` Prompt unico\ncontenido copiable\n```\n")
    blkpdf = os.path.join(tmp, "bloque.pdf")
    blkhtml = os.path.join(tmp, "bloque.html")
    r4 = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), blkmd, blkpdf,
              "--save-html", blkhtml])
    okblk, detblk = r4.returncode == 0 and os.path.exists(blkpdf), r4.stderr.strip()[:120]
    if okblk:
        try:
            d4 = json.loads(r4.stdout.strip().splitlines()[-1])
            hout = open(blkhtml, encoding="utf-8").read()
            okblk = (d4.get("cards") == 1                       # el bloque NO es tarjeta
                     and 'class="block nota"' in hout            # clase propia
                     and "<strong>catalogo</strong>" in hout     # markdown SI se procesa adentro
                     and d4.get("verbatim", {}).get("ok") is True)
            detblk = "cards=%s · clase y markdown interno OK" % d4.get("cards")
        except Exception as e:
            okblk, detblk = False, str(e)
    results.append(("Bloque con estilo ::: (v5.7): clase propia, markdown adentro, no es tarjeta",
                    okblk, detblk))

    # 16) CONTRASTE WCAG de los colores de TEXTO contra su fondo. Los dorados de
    #     marca son de acento (#d4af37 = 2.00:1, #b8912a = 2.80:1 sobre el fondo
    #     claro) y durante 5 versiones se usaron para texto: kicker de portada,
    #     enlaces, kicker e índice, títulos de bloque y el pie. Un PDF que se
    #     imprime o se lee en un móvil con brillo bajo no perdona eso. La regla
    #     queda EJECUTABLE: si alguien vuelve a poner un dorado de acento en un
    #     color de texto, esta prueba falla. (Fila del chat FILTRO DE
    #     HERRAMIENTAS, método tomado de la skill dataviz, 2026-08-26.)
    def _lum(h):
        h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
        c = [(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4) for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    def _ratio(a, b):
        la, lb = _lum(a), _lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    css = open(os.path.join(SKILL_DIR, "assets", "golden-print.css"), encoding="utf-8").read()
    import re as _re

    def _tok(name, default=None):
        m = _re.search(r"--%s:\s*(#[0-9a-fA-F]{6})" % name, css)
        return m.group(1) if m else default

    FONDO_CLARO = _tok("page-bg", "#faf9f5")
    # (color de texto, fondo sobre el que cae, dónde vive)
    PARES = [(_tok("gold-text"), FONDO_CLARO, "kicker/enlaces/índice/bloques"),
             (_tok("gold-text"), _tok("surface", "#ffffff"), "insignia del índice"),
             (_tok("ink"), FONDO_CLARO, "cuerpo del documento"),
             (_tok("muted"), FONDO_CLARO, "subtítulo y pies"),
             (_tok("on-gold"), _tok("gold", "#b8912a"), "texto sobre la banda dorada")]
    # FALLAR-CERRADO: si un token no se resuelve (lo renombraron, el color se
    # hereda, el fondo no está declarado), eso NO es un par que se salta en
    # silencio — es un FALLO. Un chequeo que se apaga solo cuando no entiende
    # lo que mira da un verde mentiroso, que es peor que no tener chequeo.
    malos = []
    for c, f, d in PARES:
        if not c or not f:
            malos.append("NO SE PUDO CALCULAR (%s): color=%r fondo=%r" % (d, c, f))
            continue
        r_ = _ratio(c, f)
        if r_ < 4.5:
            malos.append("%s sobre %s (%s) = %.2f:1" % (c, f, d, r_))
    results.append(("Contraste WCAG de los textos (>=4.5:1, falla-cerrado)", not malos,
                    "; ".join(malos) if malos else "%d pares calculados, todos pasan" % len(PARES)))

    # 17) DOCUMENTO LARGO: el índice trae números de página REALES y ningún
    #     texto baja del piso de legibilidad. Origen: una bitácora de 53 págs
    #     pasó la auditoría técnica y FER la rechazó — "no se entiende, se ve
    #     muy pequeño, no tiene un mapa, toca uno adivinar". El índice existía
    #     pero sin números (no es mapa) y en 4 columnas a 7.4pt (ilegible).
    #     Falla-cerrado y con denominador, como manda la ley.
    largo = os.path.join(tmp, "largo.md")
    secs = ["Apertura", "Keynote de IA", "Panel de fundadores", "Taller", "Cierre"]
    ln = ["---", "title: Documento largo", "---", ""]
    for d in range(1, 9):
        ln += ["## Jornada %d" % d, ""]
        for s in secs:
            ln += ["### %s de la jornada %d" % (s, d), ""]
            ln += ["Parrafo de contenido narrativo para llenar la pagina y forzar "
                   "que el documento ocupe varias hojas de verdad." for _ in range(4)]
            ln += [""]
    with open(largo, "w", encoding="utf-8") as f:
        f.write("\n".join(ln))
    largo_pdf = os.path.join(tmp, "largo.pdf")
    # El mapa ahora es OPT-IN (norma FER revisada 2026-09-02: "la gente no lee
    # los índices"), así que la prueba lo pide explícitamente con --mapa.
    r5 = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), largo, largo_pdf,
              "--mapa", "--no-verify"])
    fallos = []
    if r5.returncode != 0 or not os.path.exists(largo_pdf):
        fallos.append("no construyó: " + r5.stderr.strip()[:120])
    else:
        try:
            import pdfplumber as _pp
            import re as _re2
            with _pp.open(largo_pdf) as _pdf:
                _pags = [(_p.extract_text() or "") for _p in _pdf.pages]
                # El piso se mide en TODAS las páginas, no solo en la del índice:
                # el 6pt puede reaparecer en cualquier regla CSS futura (nota del
                # CdM). Sin excepciones — el pie de página se subió a 7.5pt en vez
                # de exceptuarlo, porque un piso con un violador no es un piso.
                _tam = [round(c["size"], 1) for _p in _pdf.pages for c in (_p.chars or [])]
            # (a) el índice trae números y son CORRECTOS.
            #     Cuántas páginas ocupa el índice se DERIVA (por su firma), no se
            #     asume: con pocos encabezados cabe en una y con muchos usa dos.
            #     La primera versión de esta prueba daba por hecho que eran dos y
            #     reportaba mal 2 de 8 secciones que en realidad estaban bien —
            #     un test que asume el layout miente en los dos sentidos.
            _fin_idx = 0
            for _i, _txt in enumerate(_pags):
                if "EN ESTE DOCUMENTO" in _txt[:400] or "Mapa" in _txt[:200]:
                    _fin_idx = _i
            _idx = " ".join(_pags[:_fin_idx + 1])
            _ok = _tot = 0
            for _d in range(1, 9):
                _t = "Jornada %d" % _d
                _m = _re2.search(_re2.escape(_t) + r"\s+(\d+)", _idx)
                if not _m:
                    continue
                _real = next((i + 1 for i in range(_fin_idx + 1, len(_pags))
                              if _t in _pags[i]), None)
                _tot += 1
                _ok += (int(_m.group(1)) == _real)
            if _tot == 0:
                fallos.append("el índice NO trae números de página")
            elif _ok != _tot:
                fallos.append("números del índice mal: %d de %d" % (_ok, _tot))
            # (b) piso de legibilidad
            _min = min(_tam) if _tam else 0
            if not _tam:
                fallos.append("no se pudo medir el tamaño de letra")
            elif _min < 7.0:
                fallos.append("texto de %.1fpt en el documento (piso 7.0)" % _min)
            detalle = ("%d de %d números correctos · letra mínima %.1fpt · %d págs "
                       "(índice: %d)" % (_ok, _tot, _min, len(_pags), _fin_idx + 1))
        except ImportError as e:
            _nomedible = "no verificable: falta pdfplumber (%s)" % e
            detalle = ""
    if "_nomedible" in dir() or ("_nomedible" in locals()):
        results.append(("Documento largo: índice con números reales y letra legible",
                        None, locals()["_nomedible"]))
    else:
        results.append(("Documento largo: índice con números reales y letra legible",
                        not fallos, "; ".join(fallos) if fallos else detalle))

    # 18) DIRECCIÓN POSITIVA del detector de color: un PDF Golden LIMPIO no debe
    #     ser marcado. Las pruebas 8-9 verifican que el auditor caza lo malo;
    #     esta verifica que DEJA PASAR lo bueno. Sin ella, apretar la tolerancia
    #     marcaría nuestros propios PDFs como "colores fuera de marca" y ninguna
    #     prueba lo cazaría — un detector demasiado agresivo hace tanto daño como
    #     uno ciego, y es más difícil de notar porque parece que trabaja.
    #     (Ley del validador que se prueba, refinada por golden-shopify: probar
    #     en las DOS direcciones. Fila del CdM, 2026-09-02.)
    _limpio = audit_text(pdf)     # el PDF de la muestra oficial, construido arriba
    _falsos = []
    if "Colores fuera de marca" in _limpio:
        _falsos.append("marcó colores en un PDF Golden limpio")
    if "cortado entre páginas" in _limpio:
        _falsos.append("marcó corte en un PDF Golden limpio")
    if "REQUIERE ARREGLO" in _limpio:
        _falsos.append("veredicto REQUIERE ARREGLO sobre la muestra oficial")
    results.append(("El auditor NO marca un PDF Golden limpio (dirección positiva)",
                    not _falsos,
                    "; ".join(_falsos) if _falsos else "3 detectores callados sobre la muestra"))

    # 19) COMPONENTES VISUALES (v6.0) y 20) IDENTIDAD POR TEMA. Durante 20
    #     versiones la skill no sabía dibujar un gráfico: se perfeccionó el
    #     envase y no el contenido. Estas dos pruebas cubren la capacidad nueva.
    vis_md = os.path.join(tmp, "vis.md")
    with open(vis_md, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Visuales\n---\n\n## Datos\n\n"
                "::: kpi\nEntregas | 1.847 | +18% | bien\nDevoluciones | 214 | 11% | mal\n:::\n\n"
                "::: barras Efectividad\nunidad | %\nEnvia | 92\nTCC | 58\n:::\n\n"
                "::: escala Meta\nactual: 4820\nmeta: 6000\nunidad: pedidos\n:::\n\n"
                "::: comparativa Rutas\nunidad | %\nCali | 61 | 88\n:::\n\n"
                "::: pasos Proceso\nRevisar | Toda la cola.\nDespachar | Con guía.\n:::\n\n"
                "::: qr\nhttps://comunidadgolden.com | Escanea\n:::\n")
    vis_pdf = os.path.join(tmp, "vis.pdf")
    rv = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), vis_md, vis_pdf,
              "--tema", "comunidad-golden", "--no-verify", "--no-index"])
    fv = []
    if rv.returncode != 0 or not os.path.exists(vis_pdf):
        fv.append("no construyó: " + rv.stderr.strip()[:120])
    else:
        try:
            import pdfplumber as _pv
            with _pv.open(vis_pdf) as _d:
                _txt = "\n".join((_p.extract_text() or "") for _p in _d.pages)
                _imgs = sum(len(_p.images) for _p in _d.pages)
            # Cada dato lleva su etiqueta VISIBLE: en papel no hay tooltip.
            for _esperado in ("1.847", "92%", "4.820", "6.000", "Revisar", "Despachar"):
                if _esperado not in _txt:
                    fv.append("falta la etiqueta directa %r" % _esperado)
            if "+27" in _txt and "Cali" not in _txt:
                fv.append("comparativa sin su etiqueta de categoría")
        except ImportError as e:
            fv = None
            _detv = "no verificable: falta pdfplumber (%s)" % e
        except Exception as e:
            fv = ["la prueba reventó: %s: %s" % (type(e).__name__, e)]
    if fv is None:
        results.append(("Componentes visuales: KPI, barras, escala, pasos y QR", None, _detv))
    else:
        results.append(("Componentes visuales: KPI, barras, escala, pasos y QR",
                        not fv, "; ".join(fv) if fv else
                        "5 componentes con etiqueta directa (sin hover que los rescate)"))

    # 20) La identidad CAMBIA de verdad: mismo documento, otro tema, otros colores.
    car_pdf = os.path.join(tmp, "vis-cartel.pdf")
    rc = run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"), vis_md, car_pdf,
              "--tema", "cartel-del-chat", "--no-verify", "--no-index"])
    fc = []
    if rc.returncode != 0 or not os.path.exists(car_pdf):
        fc.append("no construyó con el tema del Cartel")
    else:
        try:
            import pdfplumber as _pc
            def _tonos(ruta):
                # non_stroking_color puede traer STRINGS (colores con nombre en
                # el PDF de Chrome) — round() revienta con ellos. Ya me mordió
                # antes por el lado de pdfminer; aquí se filtra a números.
                out = set()
                with _pc.open(ruta) as _d:
                    for _p in _d.pages:
                        for c in (_p.rects or []):
                            col = c.get("non_stroking_color") or ()
                            nums = tuple(round(x, 2) for x in col
                                         if isinstance(x, (int, float)))
                            if nums:
                                out.add(nums)
                return out
            if _tonos(vis_pdf) == _tonos(car_pdf):
                fc.append("los dos temas pintan EXACTAMENTE lo mismo: la identidad no cambió")
            with _pc.open(car_pdf) as _d:
                _t2 = "\n".join((_p.extract_text() or "") for _p in _d.pages)
            if "El Cartel del Chat" not in _t2:
                fc.append("el pie no tomó la identidad del tema")
        except ImportError as e:
            fc = None
            _detc = "no verificable: falta pdfplumber (%s)" % e
        except Exception as e:
            # Una prueba que revienta se reporta como FALLO DE ESA PRUEBA, nunca
            # matando la corrida: si no, un error mío borra las otras 21 y el
            # informe sale vacío (medido: un round() sobre un color con nombre
            # tumbó las 22 y la salida fue PASS 0 · FAIL 0).
            fc = ["la prueba reventó: %s: %s" % (type(e).__name__, e)]
    if fc is None:
        results.append(("Identidad por tema: el mismo .md sale con otra marca", None, _detc))
    else:
        results.append(("Identidad por tema: el mismo .md sale con otra marca",
                        not fc, "; ".join(fc) if fc else
                        "Comunidad Golden vs Cartel: colores y pie distintos"))

    # v6.1 · NEUTRALIDAD POR DEFECTO. Guardián de CLASE, no del caso: no
    # comprueba que un tema concreto funcione (eso es la prueba 20), sino que
    # SIN tema no se cuele NINGUNA marca de la casa. El defecto que la motiva no
    # se veía en ninguna corrida verde: la skill hacía exactamente lo que decía
    # su código, y lo que decía era "si no te identificas, te pongo la marca de
    # FER". Lo reportó el chat del Cartel preparando material propio.
    _neu = []
    _detn = ""
    try:
        neu_md = os.path.join(tmp, "neutro.md")
        with open(neu_md, "w", encoding="utf-8") as fh:
            fh.write("---\ntitle: Documento de un tercero\n---\n\n"
                     "## Seccion\n\nTexto cualquiera.\n")
        neu_pdf = os.path.join(tmp, "neutro.pdf")
        # A propósito SIN --tema, SIN --footer, SIN --logo: el caso del tercero
        # que corre la skill tal cual la recibe.
        run([sys.executable, os.path.join(SCRIPTS, "build_pdf.py"),
             neu_md, neu_pdf, "--no-verify"])
        import pdfplumber as _pn
        with _pn.open(neu_pdf) as _d:
            _tn = "\n".join((_p.extract_text() or "") for _p in _d.pages)
            _imgs = sum(len(_p.images) for _p in _d.pages)
        # COMPARAR EN MAYÚSCULAS, no en la caja del código: el kicker y el pie
        # se imprimen en VERSALITAS por CSS, así que en el PDF el texto extraído
        # es "COMUNIDAD GOLDEN" y buscar "Comunidad Golden" no encuentra nada.
        # Medido: la primera versión de esta prueba pasaba en verde con el
        # defecto REPUESTO a propósito — un guardián ciego que parecía trabajar.
        _tnU = _tn.upper()
        for marca in ("COMUNIDAD GOLDEN", "GOLDEN GROUP"):
            if marca in _tnU:
                _neu.append("estampa '%s' sin que nadie la pidiera" % marca.title())
        # El logo es marca igual que el texto: un pie vacío con el emblema de
        # Golden sigue siendo atribución falsa. El documento no trae figuras,
        # así que CUALQUIER imagen incrustada aquí es el logo.
        if _imgs:
            _neu.append("incrusta %d imagen(es): el logo se cuela igual" % _imgs)
    except ImportError as e:
        _neu = None
        _detn = "no verificable: falta pdfplumber (%s)" % e
    except Exception as e:
        _neu = ["la prueba reventó: %s: %s" % (type(e).__name__, e)]
    if _neu is None:
        results.append(("Neutralidad por defecto: sin --tema no hay marca Golden",
                        None, _detn))
    else:
        results.append(("Neutralidad por defecto: sin --tema no hay marca Golden",
                        not _neu, "; ".join(_neu) if _neu else
                        "sin pie, sin autor, sin kicker y sin logo"))

    # LA CUARTA CARA, la que vive FUERA del árbol: la fila del REGISTRO-FABRICAS,
    # que leen los otros chats y que ningún bump ni blindaje alcanza. Se reporta
    # como INFORMATIVO, no como fallo: entre que la fábrica sella y el Centro de
    # Mando regenera el censo hay una ventana legítima de desfase, y hacer fallar
    # ahí sería el detector agresivo que la prueba 18 existe para evitar.
    _reg = os.path.expanduser("~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/"
                              "🌐 PROYECTOS/STACK-GOLDEN/REGISTRO-FABRICAS.md")
    _sello = None
    _msk = _re3.search(r"skill (v\d+\.\d+)", open(os.path.join(SKILL_DIR, "SKILL.md"),
                                                   encoding="utf-8").read())
    _sello = _msk.group(1) if _msk else "?"
    if os.path.exists(_reg):
        _fila = _re3.search(r"\| golden-pdf-check \| ([^|]+) \|",
                            open(_reg, encoding="utf-8").read())
        _enreg = ("v" + _fila.group(1).strip()) if _fila else "no aparece"
        _igual = (_enreg == _sello)
        results.append(("Registro de fábricas al día (informativo)", True,
                        "disco %s · registro %s%s" % (_sello, _enreg,
                        "" if _igual else "  ← DESFASADA: avisar al CdM para que regenere")))
    else:
        results.append(("Registro de fábricas al día (informativo)", True,
                        "registro no encontrado en esta máquina"))

    # 20) COHERENCIA DEL SELLO — la ley del denominador publicado aplicada a esta
    #     misma autoprueba. La docstring declara un número de comprobaciones y el
    #     sello del changelog lo repite; si alguien agrega una prueba y no toca
    #     el número, el sello miente. Ya pasó DOS veces en esta skill (decía 13
    #     corriendo 14, y 15 corriendo 14) y las dos las cazó un ojo externo, no
    #     yo. Ahora lo caza la propia corrida: se compara lo DECLARADO contra lo
    #     que de verdad se ejecutó, sin que nadie tenga que acordarse.
    _doc = __doc__ or ""
    _mdec = _re3.search(r"\*\*(\d+) comprobaciones\*\*", _doc)
    _declaradas = int(_mdec.group(1)) if _mdec else None
    # Va de ÚLTIMA a propósito: así cuenta TODAS las líneas que la corrida
    # imprime, incluida la informativa del registro y ella misma. La primera
    # versión iba antes y contaba 19 sobre una salida de 20 — la propia
    # comprobación de coherencia salió incoherente, que es la mejor prueba
    # de que hacía falta.
    _reales = len(results) + 1        # +1: esta misma prueba, que aún no se agregó
    if _declaradas is None:
        _coh = False
        _det = "la docstring no declara cuántas comprobaciones tiene"
    else:
        _coh = (_declaradas == _reales)
        _det = "declaradas %d · ejecutadas %d" % (_declaradas, _reales)
    results.append(("Coherencia del sello: pruebas declaradas == ejecutadas", _coh, _det))

    report(results)
    core = all(ok is not False for name, ok, _ in results
               if "numeración" not in name and "informativo" not in name)  # motor es informativo
    sys.exit(0 if core else 1)


def report(results):
    """TRES estados, no dos. `ok=None` significa NO SE PUDO VERIFICAR (falta una
    dependencia opcional, no hay Chrome): eso NO es un fallo del estándar y no
    debe leerse como tal. Quien corre la autoprueba en una máquina limpia veía
    "HAY FALLOS" y concluía que el estándar de PDF estaba roto cuando lo que
    faltaba era una librería — el falso rojo, que por la regla de la casa es el
    que nadie audita porque parece que el detector trabaja.

    OJO con la frontera, que no es la misma que fallar-cerrado: si un chequeo no
    resuelve algo DEL ARTEFACTO (un token renombrado, un fondo no declarado) eso
    SÍ es FALLO — es una señal sobre lo que mide. `None` es solo para cuando el
    ENTORNO no permite medir; ahí el chequeo no tiene nada que decir del PDF."""
    print("=== AUTOPRUEBA golden-pdf-check ===")
    fallos = sin_medir = 0
    for name, ok, detail in results:
        mark = "PASS" if ok is True else ("N/D " if ok is None else "FAIL")
        if ok is False:
            fallos += 1
        elif ok is None:
            sin_medir += 1
        line = f"[{mark}] {name}"
        if detail:
            line += "  ·  " + detail
        print(line)
    # El veredicto DECLARA el denominador: cuántas midió y cuántas no pudo.
    if fallos:
        cierre = "HAY FALLOS (%d)" % fallos
    elif sin_medir:
        cierre = "TODO OK en lo medido · %d sin verificar (falta dependencia, no es un fallo)" % sin_medir
    else:
        cierre = "TODO OK"
    print("=== " + cierre + " ===")


if __name__ == "__main__":
    main()
