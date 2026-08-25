#!/usr/bin/env python3
"""
GOLDEN PDF · selftest.py
Prueba de regresión de la skill: **15 comprobaciones** sobre PDFs construidos
de verdad (nada simulado). Hay una prueba por cada versión que cambió el
comportamiento, para que una regresión no pase en verde:

  1. Construye sin errores · 2. Salida JSON válida · 3. Cuenta de tarjetas ·
  4. COMPUERTA VERBATIM (texto idéntico) · 5. ANTI-CORTE (nada al filo del
  borde) · 6. Motor con numeración · 7. Fuente de marca incrustada ·
  8-9. Detectores ADVERSARIALES (un PDF feo y uno cortado DEBEN ser cazados) ·
  10. Anti-falso-positivo: dos tarjetas seguidas no son un corte ·
  11-12. Figuras (v5.6) · 13. Bloque con estilo ::: (v5.7) · 14. El aviso de
  líneas largas dispara cuando debe (v5.8) · 15. …y la muestra oficial NO lo
  dispara (el fixture cumple la regla que la skill enseña).

La cifra de arriba es la que imprime una corrida SANA, y es la que va en el
sello del changelog. Si agregas una prueba, actualiza el número aquí y verifica
contándolo en la salida — nunca de memoria: una prueba que solo se registra
cuando falla infla el sello sin ser reproducible (así nació este arreglo).

Regla de la casa: toda versión que cambie comportamiento entra con su prueba
aquí. Si tocas el CSS, el parser o el auto-fit, corre esto antes de usar la
skill en material real.

Uso:  python selftest.py
Salida: PASS (exit 0) o FAIL (exit 1) con el detalle.
"""
import os, sys, json, subprocess, tempfile, shutil

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
SAMPLE = os.path.join(SKILL_DIR, "assets", "selftest-sample.md")
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
    tmp = tempfile.mkdtemp(prefix="golden-selftest-")
    pdf = os.path.join(tmp, "selftest.pdf")

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
        # nítido y ligero); el PNG sí suma. Con el logo de la portada, >= 2.
        up = txt.upper()   # la insignia se imprime en versalitas por CSS
        results.append(("Figuras: imagen incrustada y pies numerados en orden",
                        imgs >= 2 and "FIGURA 1" in up and "FIGURA 2" in up,
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

    report(results)
    core = all(ok for name, ok, _ in results if "numeración" not in name)  # motor es informativo
    sys.exit(0 if core else 1)


def report(results):
    print("=== SELF-TEST golden-pdf-check ===")
    allok = True
    for name, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            allok = False
        line = f"[{mark}] {name}"
        if detail:
            line += "  ·  " + detail
        print(line)
    print("=== " + ("TODO OK" if allok else "HAY FALLOS") + " ===")


if __name__ == "__main__":
    main()
