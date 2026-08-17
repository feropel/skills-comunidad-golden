#!/usr/bin/env python3
"""
GOLDEN PDF · build_pdf.py
Convierte contenido Markdown-Golden en un PDF con la identidad de
Comunidad Golden, márgenes correctos, paginación y — lo esencial —
tarjetas de prompt ATÓMICAS que nunca se parten entre páginas.

Además, tras construir, corre una COMPUERTA VERBATIM: re-extrae el texto
del PDF y confirma que el contenido de cada prompt aparece idéntico
(regla inviolable: el texto no se toca). Si algo cambió, avisa.

Uso:
    python build_pdf.py entrada.md salida.pdf [opciones]
        --title / --subtitle / --kicker / --author   sobrescriben el front matter
        --save-html archivo.html                      guarda el HTML intermedio
        --no-verify                                   omite la compuerta verbatim
        --strict                                      falla (exit 3) si el verbatim no cuadra
        --no-index                                    omite la página de CONTENIDO (por defecto SÍ va)

Norma FER (v5.4): todo PDF Golden abre con una página de **CONTENIDO** que lista, línea por
línea, TODO lo que trae el documento (secciones y subsecciones, en orden de ejecución) y marca
cuántos textos copiables tiene cada una. Se genera SOLA desde los encabezados: nadie la escribe
a mano y nunca queda desactualizada.

Formato de entrada: ver references/content-format.md.
Todo lo que va en ``` ``` ``` (o ~~~ ~~~) o en ::: prompt ::: es una tarjeta
copiable atómica.
"""
import sys, os, re, html, argparse, subprocess, tempfile, json, shutil, logging, base64

logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")

# --- geometría (única fuente de verdad; cuadra con auto-fit y márgenes PDF) ---
PAGE = "A4"
MARGIN_MM = 15
FOOTER_MM = 16
PX_PER_MM = 3.7795275591
PRINT_WIDTH_PX = round((210 - 2 * MARGIN_MM) * PX_PER_MM)    # ancho útil A4 ≈ 680
PRINT_HEIGHT_PX = round((297 - MARGIN_MM - FOOTER_MM) * PX_PER_MM)


def load_asset(name):
    with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
        return f.read()


# ---------------- parser markdown-golden ----------------
def parse_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            text = text[end + 4:]
    return meta, text.lstrip("\n")


def esc(s):
    return html.escape(s, quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r'<code class="inline">\1</code>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


# ---------------- figuras (v5.6) ----------------
# Un manual de pasos necesita PANTALLAS. La figura es atómica igual que la
# tarjeta de prompt: la imagen y su pie viajan juntos y nunca se parten entre
# páginas. La imagen se incrusta en base64 para que el PDF sea autocontenido.
FIG_COUNTER = {"n": 0}
IMAGE_BASE = [os.getcwd()]
IMAGE_MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
              ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp"}
IMG_RE = re.compile(r"^!\[(.*?)\]\(([^)\s]+)\)\s*(?:\{([^}]*)\})?\s*$")


def figure_html(caption, src, size=None):
    path = src if os.path.isabs(src) else os.path.join(IMAGE_BASE[0], src)
    ext = os.path.splitext(path)[1].lower()
    if os.path.exists(path):
        with open(path, "rb") as fh:
            uri = "data:%s;base64,%s" % (IMAGE_MIME.get(ext, "image/png"),
                                         base64.b64encode(fh.read()).decode())
    else:
        uri = esc(src)
        sys.stderr.write("⚠️  Imagen no encontrada: %s\n" % path)
    FIG_COUNTER["n"] += 1
    style = ' style="width:%s"' % esc(size.strip()) if size and size.strip() else ""
    cap_txt = (" " + inline(caption)) if caption.strip() else ""
    return ('<figure class="figure">'
            '<img src="' + uri + '" alt="' + esc(caption) + '"' + style + ">"
            '<figcaption><span class="fig-num">Figura ' + str(FIG_COUNTER["n"]) + "</span>"
            + cap_txt + "</figcaption></figure>")


def prompt_card(title, body, mono=True):
    head_title = esc(title) if title else "Prompt"
    # El cuerpo del prompt SIEMPRE se escapa literal (regla verbatim): nada de
    # transformar **negrita**, backticks o enlaces. La única diferencia entre
    # mono y prosa es la tipografía; el texto se conserva carácter por carácter,
    # con sus saltos de línea (white-space: pre-wrap en ambos).
    if mono:
        body_html = '<pre class="prompt-body">' + esc(body.rstrip("\n")) + "</pre>"
    else:
        body_html = '<div class="prompt-body prose">' + esc(body.rstrip("\n")) + "</div>"
    card_html = (
        '<div class="prompt-card">'
        '<div class="prompt-head">'
        '<span class="prompt-title">' + head_title + "</span>"
        '<span class="prompt-tag">Prompt · copiar</span>'
        "</div>" + body_html + "</div>"
    )
    return card_html


def md_to_html(md):
    """Devuelve (html, cards) donde cards son los textos crudos de cada
    tarjeta de prompt (para la compuerta verbatim)."""
    out, cards = [], []
    lines = md.split("\n")
    i = 0
    list_buffer, list_type = [], None

    def flush_list():
        nonlocal list_buffer, list_type
        if list_buffer:
            tag = "ol" if list_type == "ol" else "ul"
            out.append("<" + tag + ">" + "".join(list_buffer) + "</" + tag + ">")
            list_buffer, list_type = [], None

    while i < len(lines):
        line = lines[i]

        # fence ``` o ~~~ -> tarjeta monoespaciada
        mfence = re.match(r"^(```|~~~)(.*)$", line)
        if mfence:
            flush_list()
            fence, title = mfence.group(1), mfence.group(2).strip()
            buf = []
            i += 1
            while i < len(lines) and lines[i].rstrip() != fence:
                buf.append(lines[i]); i += 1
            i += 1
            raw = "\n".join(buf)
            cards.append(raw)
            out.append(prompt_card(title, raw, mono=True))
            continue

        # ::: prompt Título ... :::
        mp = re.match(r"^:::\s*prompt\s*(.*)$", line, re.I)
        if mp:
            flush_list()
            title = mp.group(1).strip()
            buf = []
            i += 1
            while i < len(lines) and not re.match(r"^:::\s*$", lines[i]):
                buf.append(lines[i]); i += 1
            i += 1
            raw = "\n".join(buf)
            cards.append(raw)
            out.append(prompt_card(title, raw, mono=False))
            continue

        # bloque con estilo:  ::: nota Título ... :::   (v5.7)
        # Sirve para que un documento largo respire: destacados, tarjetas de
        # datos, avisos. El contenido de adentro SÍ se procesa como Markdown
        # (a diferencia de la tarjeta de prompt, que es literal). La clase
        # sale del nombre del bloque: ::: nota  ->  <div class="block nota">
        mblk = re.match(r"^:::\s*([a-zA-Z][\w-]*)\s*(.*)$", line)
        if mblk and mblk.group(1).lower() != "prompt":
            flush_list()
            cls = mblk.group(1).lower()
            btitle = mblk.group(2).strip()
            buf = []
            i += 1
            while i < len(lines) and not re.match(r"^:::\s*$", lines[i]):
                buf.append(lines[i]); i += 1
            i += 1
            inner_html, inner_cards = md_to_html("\n".join(buf))
            cards.extend(inner_cards)
            head = ('<p class="block-title">' + inline(btitle) + "</p>") if btitle else ""
            out.append('<div class="block ' + esc(cls) + '">' + head + inner_html + "</div>")
            continue

        # figura:  ![Pie de figura](ruta/imagen.svg){70%}   (el ancho es opcional)
        mimg = IMG_RE.match(line)
        if mimg:
            flush_list()
            out.append(figure_html(mimg.group(1), mimg.group(2), mimg.group(3)))
            i += 1
            continue

        if line.startswith("### "):
            flush_list(); out.append("<h3>" + inline(line[4:]) + "</h3>"); i += 1; continue
        if line.startswith("## "):
            flush_list(); out.append("<h2>" + inline(line[3:]) + "</h2>"); i += 1; continue
        if line.startswith("# "):
            flush_list(); out.append("<h2>" + inline(line[2:]) + "</h2>"); i += 1; continue

        if re.match(r"^---+\s*$", line):
            flush_list(); out.append("<hr>"); i += 1; continue

        # tabla markdown:  | a | b |  con línea separadora | --- | --- |
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$", lines[i + 1]):
            flush_list()
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            header = cells(line)
            i += 2  # saltar cabecera y separador
            body_rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body_rows.append(cells(lines[i])); i += 1
            thead = "".join("<th>" + inline(h) + "</th>" for h in header)
            tbody = "".join("<tr>" + "".join("<td>" + inline(c) + "</td>" for c in r) + "</tr>"
                            for r in body_rows)
            out.append("<table><thead><tr>" + thead + "</tr></thead><tbody>" + tbody + "</tbody></table>")
            continue

        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if list_type not in (None, "ul"): flush_list()
            list_type = "ul"; list_buffer.append("<li>" + inline(m.group(1)) + "</li>"); i += 1; continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            if list_type not in (None, "ol"): flush_list()
            list_type = "ol"; list_buffer.append("<li>" + inline(m.group(1)) + "</li>"); i += 1; continue

        if line.strip() == "":
            flush_list(); i += 1; continue

        flush_list()
        para = [line]; i += 1
        while i < len(lines) and lines[i].strip() != "" and not re.match(
            r"^(```|~~~|:::|#{1,3}\s|---+\s*$|\s*[-*]\s|\s*\d+\.\s|!\[)", lines[i]
        ):
            para.append(lines[i]); i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")

    flush_list()
    return "\n".join(out), cards


def outline(body_md):
    """Esquema del documento SIN tocar el contenido: una entrada por cada H2/H3,
    con el número de tarjetas copiables que cuelgan de ella. Alimenta la página
    de CONTENIDO (norma FER v5.4)."""
    items, lines, i = [], body_md.split("\n"), 0

    def bump():
        if items:
            items[-1]["cards"] += 1

    while i < len(lines):
        ln = lines[i]
        mfence = re.match(r"^(```|~~~)(.*)$", ln)
        if mfence:
            fence = mfence.group(1)
            i += 1
            while i < len(lines) and lines[i].rstrip() != fence:
                i += 1
            i += 1
            bump()
            continue
        if re.match(r"^:::\s*prompt", ln, re.I):
            i += 1
            while i < len(lines) and not re.match(r"^:::\s*$", lines[i]):
                i += 1
            i += 1
            bump()
            continue
        m = re.match(r"^(#{2,3})\s+(.*)$", ln)
        if m:
            items.append({"lvl": len(m.group(1)), "text": m.group(2).strip(), "cards": 0})
        i += 1
    return items


def build_index(body_md):
    """Página de CONTENIDO: todo lo que hay en el documento, línea por línea.
    Va SIEMPRE justo después de la portada (norma FER v5.4)."""
    items = outline(body_md)
    if not items:
        return ""
    rows = []
    for idx, it in enumerate(items):
        n = it["cards"]
        if it["lvl"] == 2:                     # una sección suma las tarjetas de sus subsecciones
            j = idx + 1
            while j < len(items) and items[j]["lvl"] == 3:
                n += items[j]["cards"]
                j += 1
        rows.append((it["lvl"], it["text"], n))
    total = sum(it["cards"] for it in items)
    lis = []
    for lvl, text, n in rows:
        badge = ('<span class="toc-count">' + str(n) + '</span>') if n else ""
        lis.append('<li class="toc-h%d">%s<span class="toc-text">%s</span></li>'
                   % (lvl, badge, inline(text)))
    hint = ("Todo lo que hay en este documento, en orden de ejecución. El número al lado de una "
            "línea es la cantidad de textos listos para copiar y pegar que trae esa parte"
            + (" (%d en total)." % total if total else "."))
    # Documentos largos (manuales, guías de módulo): con 2 columnas el índice
    # se derrama a una segunda hoja que queda medio vacía — el mismo defecto de
    # la portada vacía. A partir de 70 líneas pasa a 3 columnas y vuelve a caber
    # en la hoja de la portada.
    dense = (" dense dense-4" if len(rows) > 105 else
             " dense" if len(rows) > 70 else "")
    return ('<section class="toc' + dense + '">'
            '<p class="kicker">Índice del documento</p>'
            '<h1 class="toc-title">CONTENIDO</h1>'
            '<p class="toc-hint">' + hint + "</p>"
            '<ul class="toc-list">' + "".join(lis) + "</ul>"
            "</section>")


def build_cover(meta, logo_path=None):
    # Logo alterno (v5.6): documentos que NO se emiten bajo la marca Comunidad
    # Golden — p.ej. el MBA, cuyo emisor formal es la empresa — pasan su propio
    # sello con --logo. Sin el flag, el emblema Golden de siempre.
    if logo_path and os.path.exists(logo_path):
        ext = os.path.splitext(logo_path)[1].lower()
        with open(logo_path, "rb") as fh:
            logo = ("<img src='data:%s;base64,%s' alt=''>"
                    % (IMAGE_MIME.get(ext, "image/png"),
                       base64.b64encode(fh.read()).decode()))
    else:
        logo = load_asset("logo-golden.svg")
    kicker = esc(meta.get("kicker", "Comunidad Golden"))
    title = esc(meta.get("title", "Documento"))
    subtitle = meta.get("subtitle", "")
    author = esc(meta.get("author", "Golden Group"))
    date = esc(meta.get("date", ""))
    sub_html = '<p class="subtitle">' + esc(subtitle) + "</p>" if subtitle else ""
    meta_line = "<strong>" + author + "</strong>" + (" · " + date if date else "")
    return (
        '<section class="cover">'
        '<div class="logo">' + logo + "</div>"
        '<p class="kicker">' + kicker + "</p>"
        '<div class="cover-rule"></div>'
        "<h1>" + title + "</h1>" + sub_html +
        '<div class="cover-meta">' + meta_line + "</div>"
        "</section>"
    )


def fonts_style():
    """Incrusta las fuentes de marca (Inter + JetBrains Mono, OFL) como data
    URIs. Así el documento se ve IDÉNTICO en cualquier equipo, no depende de las
    fuentes del sistema. Chrome subsetea al imprimir, así que el PDF queda ligero."""
    # Fuentes ESTÁTICAS (no variables): Chrome las incrusta como CID TrueType con
    # ToUnicode correcto → el copiar-pegar sale idéntico. Las variables se
    # convertían en Type 3 y corrompían caracteres como los corchetes.
    specs = [("GoldenSans", "Inter-Regular.ttf", 400),
             ("GoldenSans", "Inter-Bold.ttf", 700),
             ("GoldenMono", "JBMono-Regular.ttf", 400)]
    faces = []
    for fam, fn, wght in specs:
        p = os.path.join(ASSETS, "fonts", fn)
        if not os.path.exists(p):
            continue
        with open(p, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        faces.append("@font-face{font-family:'%s';src:url(data:font/ttf;base64,%s) "
                     "format('truetype');font-weight:%d;font-style:normal;}" % (fam, b64, wght))
    if not faces:
        return ""   # sin fuentes bundled: cae a las del sistema
    override = ("<style>" + "".join(faces) +
                ":root{--font:'GoldenSans',-apple-system,BlinkMacSystemFont,'Segoe UI',"
                "Roboto,Helvetica,Arial,sans-serif;"
                "--mono:'GoldenMono',ui-monospace,Menlo,Consolas,monospace;}</style>")
    return override


def build_html(meta, body_md, with_index=True, logo_path=None, theme_css=None):
    css = load_asset("golden-print.css")
    # TEMA ALTERNO (v5.7): una hoja de estilo que se anexa DESPUES de la de
    # marca y solo redefine variables/colores. La identidad Golden sigue
    # intacta por defecto; los documentos que se emiten bajo otra marca
    # (el MBA, por ejemplo) pasan la suya con --css.
    if theme_css and os.path.exists(theme_css):
        with open(theme_css, encoding="utf-8") as fh:
            css += "\n/* ---- tema alterno ---- */\n" + fh.read()
    autofit = load_asset("autofit.js")
    body, cards = md_to_html(body_md)
    # Geometría de UNA sola fuente: el alto máximo de tarjeta se deriva del
    # tamaño de página y los márgenes reales (área útil menos un colchón),
    # y sobreescribe el valor del CSS para que nunca se descuadren.
    # Colchón de 20mm, no 8: la tarjeta casi nunca abre la página — va DEBAJO
    # de su encabezado de sección (### ≈ 10-14mm con márgenes). Con 8mm una
    # tarjeta llena terminaba a ~5mm del borde y audit_pdf.py (umbral 6mm)
    # reprobaba un PDF que este mismo motor produjo.
    card_max_mm = (297 - MARGIN_MM - FOOTER_MM) - 20
    geom = "<style>:root{--card-max-mm:%d}</style>" % card_max_mm
    return (
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>"
        "<style>" + css + "</style>" + geom + fonts_style() + "</head><body>"
        + build_cover(meta, logo_path)
        + (build_index(body_md) if with_index else "") +
        '<main class="doc">' + body + "</main>"
        "<script>" + autofit + "</script></body></html>"
    ), cards


# ---------------- render a PDF ----------------
def footer_template(label="Comunidad Golden"):
    return (
        '<div style="width:100%;font-size:8px;color:#9a7b1e;'
        'font-family:Helvetica,Arial,sans-serif;padding:0 15mm;'
        'display:flex;justify-content:space-between;align-items:center;">'
        "<span>" + html.escape(label) + "</span>"
        '<span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>'
        "</div>"
    )


def render_with_playwright(html_str, out_path, footer_label="Comunidad Golden"):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": PRINT_WIDTH_PX, "height": PRINT_HEIGHT_PX})
        page.emulate_media(media="print")
        page.set_content(html_str, wait_until="load")
        try:
            page.wait_for_function("window.__golden_fit_done === true", timeout=8000)
        except Exception:
            pass
        warnings = []
        try:
            warnings = page.evaluate("window.__golden_warnings || []")
        except Exception:
            pass
        pdf_kwargs = dict(
            path=out_path, format=PAGE, print_background=True,
            display_header_footer=True, header_template="<div></div>",
            footer_template=footer_template(footer_label),
            margin={"top": f"{MARGIN_MM}mm", "bottom": f"{FOOTER_MM}mm",
                    "left": f"{MARGIN_MM}mm", "right": f"{MARGIN_MM}mm"},
        )
        try:
            page.pdf(tagged=True, **pdf_kwargs)   # PDF etiquetado (accesible) si la versión lo soporta
        except TypeError:
            page.pdf(**pdf_kwargs)
        browser.close()
    return "playwright", warnings


def find_chrome():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chrome"),
    ]
    return next((c for c in candidates if c and os.path.exists(c)), None)


def render_with_chrome(html_str, out_path):
    chrome = find_chrome()
    if not chrome:
        raise RuntimeError("No hay Playwright ni Chromium/Chrome disponible. "
                           "Instala Playwright: pip install playwright && python -m playwright install chromium")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_str); tmp = f.name
    try:
        # --window-size al ANCHO ÚTIL del PDF para que el auto-fit mida igual
        # que como se imprimirá (evita reducir de más/de menos).
        subprocess.run([
            chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={PRINT_WIDTH_PX},{PRINT_HEIGHT_PX}",
            "--no-pdf-header-footer", "--print-to-pdf-no-header",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=4000",
            "--print-to-pdf=" + out_path, "file://" + tmp,
        ], check=True, timeout=60, capture_output=True)
    finally:
        os.unlink(tmp)
    # Chrome CLI no expone los avisos del auto-fit (no podemos leer el DOM).
    return "chrome-cli (sin numeración en pie; instala Playwright para numeración)", []


def render_pdf(html_str, out_path, footer_label="Comunidad Golden"):
    try:
        import playwright  # noqa
        return render_with_playwright(html_str, out_path, footer_label)
    except ImportError:
        return render_with_chrome(html_str, out_path)


# ---------------- compuerta verbatim ----------------
import unicodedata

# Equivalencias tipográficas: la extracción de texto de un PDF puede devolver
# la elipsis, las comillas curvas o los guiones largos como variantes visuales
# del mismo carácter. Canonicalizarlas ANTES de comparar evita falsos
# "caracteres no idénticos" sin dejar de atrapar texto realmente perdido.
_TYPO_EQ = {"…": "...", "‘": "'", "’": "'", "“": '"',
            "”": '"', "–": "-", "—": "-", " ": " "}


def _nfkc(s):
    # NFKC unifica ligaduras (ﬁ→fi) y variantes: comparación robusta.
    for k, v in _TYPO_EQ.items():
        s = s.replace(k, v)
    # Selectores de variación de emoji (⚠️ = ⚠ + U+FE0F): el extractor de PDF
    # los pierde aunque el emoji se vea bien; se ignoran al comparar.
    s = s.replace("️", "").replace("︎", "")
    return unicodedata.normalize("NFKC", s)


def _norm(s):
    return re.sub(r"\s+", " ", _nfkc(s)).strip()


def _tight(s):
    # solo caracteres significativos (sin ningún espacio): el chequeo más estricto.
    return re.sub(r"\s+", "", _nfkc(s))


def verbatim_gate(pdf_path, cards):
    """Confirma que el texto de cada prompt aparece idéntico en el PDF, con dos
    chequeos: (a) a nivel de palabra/espacios y (b) a nivel de caracter (sin
    espacios). Además localiza líneas perdidas. Devuelve (ok, [fallas])."""
    try:
        import pdfplumber
    except ImportError:
        return None, ["pdfplumber no instalado: no se pudo verificar (pip install pdfplumber)"]
    with pdfplumber.open(pdf_path) as pdf:
        raw_full = "\n".join((p.extract_text() or "") for p in pdf.pages)
    full = _norm(raw_full)
    full_tight = _tight(raw_full)
    fails = []
    for idx, raw in enumerate(cards, 1):
        cn, ct = _norm(raw), _tight(raw)
        if ct and ct not in full_tight:
            # localizar qué línea se perdió/cambió
            perdidas = [ln.strip() for ln in raw.splitlines()
                        if _tight(ln) and _tight(ln) not in full_tight]
            det = (" · línea alterada: «%s…»" % perdidas[0][:60]) if perdidas else ""
            fails.append(f"Prompt #{idx}: caracteres no idénticos en el PDF{det}")
        elif cn and cn not in full:
            fails.append(f"Prompt #{idx}: espaciado/orden alterado → «{cn[:60]}…»")
    return (len(fails) == 0), fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--title"); ap.add_argument("--subtitle")
    ap.add_argument("--kicker"); ap.add_argument("--author")
    ap.add_argument("--save-html")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--logo", help="ruta a un logo alterno para la portada (png/jpg/svg)")
    ap.add_argument("--css", help="hoja de estilo de tema que se anexa a la de marca")
    ap.add_argument("--footer", default="Comunidad Golden",
                    help="texto del pie de pagina (por defecto: Comunidad Golden)")
    ap.add_argument("--no-index", action="store_true",
                    help="omite la página de CONTENIDO (por defecto SÍ va · norma FER v5.4)")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        raw = f.read()
    # Las rutas de imagen se resuelven contra la carpeta del .md, no contra el
    # directorio desde el que se corre el script.
    IMAGE_BASE[0] = os.path.dirname(os.path.abspath(args.input)) or os.getcwd()
    FIG_COUNTER["n"] = 0
    meta, body = parse_front_matter(raw)
    for k in ("title", "subtitle", "kicker", "author"):
        if getattr(args, k):
            meta[k] = getattr(args, k)

    html_str, cards = build_html(meta, body, with_index=not args.no_index,
                                 logo_path=args.logo, theme_css=args.css)

    # v5.8 · AVISO DE LÍNEAS LARGAS EN TARJETAS (un chat de producto, 2026-08-07):
    # dentro de una tarjeta monoespaciada, una línea de más de ~76 caracteres se
    # ENVUELVE al renderizar y la compuerta verbatim la reporta como
    # "espaciado/orden alterado" (pasó con dos prompts de imagen; se resolvió
    # reescribiéndolos a 72-84 caracteres por línea). Avisar ANTES de renderizar
    # con la tarjeta y la línea exactas, para corregir el contenido y no perder
    # un ciclo de compuerta.
    LINEA_MAX = 76
    lineas_largas = []
    for idx, card in enumerate(cards, 1):
        for n, ln in enumerate(card.split("\n"), 1):
            if len(ln) > LINEA_MAX:
                lineas_largas.append((idx, n, len(ln)))
    if lineas_largas:
        sys.stderr.write("\n⚠️  LÍNEAS LARGAS EN TARJETAS (riesgo de compuerta "
                         "verbatim): una línea de más de ~%d caracteres se "
                         "envuelve al renderizar\n    y la compuerta la reporta "
                         "como 'espaciado/orden alterado'. Reescribir a 72-76 "
                         "caracteres por línea:\n" % LINEA_MAX)
        for idx, n, ln_len in lineas_largas:
            sys.stderr.write(f"   - Tarjeta #{idx}, línea {n}: {ln_len} caracteres\n")
        sys.stderr.write("\n")

    if args.save_html:
        with open(args.save_html, "w", encoding="utf-8") as f:
            f.write(html_str)

    engine, fit_warnings = render_pdf(html_str, args.output, args.footer)

    if fit_warnings:
        sys.stderr.write("\nℹ️  AUTO-FIT: estos prompts quedaron muy reducidos "
                         "(considera partirlos en el contenido):\n")
        for w in fit_warnings:
            estado = "escalado" if w.get("scaled") else f"{w.get('font_px')}pt"
            sys.stderr.write(f"   - Prompt #{w.get('index')} «{w.get('title')}» → {estado}\n")
        sys.stderr.write("\n")

    verbatim = {"checked": False}
    if not args.no_verify:
        ok, fails = verbatim_gate(args.output, cards)
        verbatim = {"checked": ok is not None, "ok": ok, "fails": fails}
        if fails:
            sys.stderr.write("\n⚠️  COMPUERTA VERBATIM: el texto del PDF no coincide 100%:\n")
            for fl in fails:
                sys.stderr.write("   - " + fl + "\n")
            sys.stderr.write("   Revisa el contenido; el texto no debe alterarse.\n\n")

    print(json.dumps({"ok": True, "output": args.output, "engine": engine,
                      "cards": len(cards), "verbatim": verbatim,
                      "fit_warnings": fit_warnings}, ensure_ascii=False))

    if args.strict and verbatim.get("ok") is False:
        sys.exit(3)


if __name__ == "__main__":
    main()
