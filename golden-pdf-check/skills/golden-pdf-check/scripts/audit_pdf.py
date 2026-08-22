#!/usr/bin/env python3
"""
GOLDEN PDF · audit_pdf.py
Revisa un PDF ya existente contra el estándar de Comunidad Golden y
emite un informe (Markdown + JSON) con los problemas detectados:

  - Márgenes: contenido que invade el borde de la página.
  - Paginación: bloques/contenido que rozan el borde inferior
    (señal de posible bloque cortado que continúa en la página siguiente).
  - Colores: hex fuera de la paleta Golden.
  - Estructura: número de páginas, densidad, texto pegado al borde.

Es un análisis HEURÍSTICO y ADVISORY: el arreglo definitivo es
regenerar el PDF con build_pdf.py, que garantiza bloques atómicos.

Uso:
    python audit_pdf.py documento.pdf [--json informe.json]

Requiere pdfplumber (preferido) o pypdf. Si falta, indica cómo instalar.
"""
import sys, os, json, argparse, logging

# pdfminer/pdfplumber son ruidosos con PDFs de Chrome (avisos de FontBBox y
# colores con nombre). Son inofensivos: los silenciamos para un informe limpio.
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = json.load(open(os.path.join(SKILL_DIR, "assets", "golden-brand.json"), encoding="utf-8"))
ALLOWED = set(h.lower() for h in BRAND["allowed_hex_for_audit"])

MARGIN_MM = BRAND["geometry"]["margin_mm"]
FOOTER_MM = BRAND["geometry"].get("footer_reserve_mm", 16)
PT_PER_MM = 2.83465
MARGIN_PT = MARGIN_MM * PT_PER_MM
FOOTER_PT = FOOTER_MM * PT_PER_MM
BOTTOM_ALERT_MM = 6           # contenido a <6mm del borde del ÁREA de contenido
BOTTOM_ALERT_PT = BOTTOM_ALERT_MM * PT_PER_MM
BAND_PT = 20 * PT_PER_MM      # banda (20mm) para detectar bloques al borde sup/inf
MONO_HINTS = ("mono", "courier", "cour", "consol", "menlo", "jetbrain", "roboto mono", "fira")


def is_mono(fontname):
    fn = (fontname or "").lower()
    return any(h in fn for h in MONO_HINTS)


def rgb_to_hex(c):
    try:
        if isinstance(c, (list, tuple)) and len(c) >= 3:
            return "#%02x%02x%02x" % tuple(int(round(x * 255)) if x <= 1 else int(x) for x in c[:3])
    except Exception:
        return None
    return None


def near(hexval, allowed, tol=18):
    """Dice si el color esta cerca de algun permitido (tolerancia por canal)."""
    try:
        r, g, b = int(hexval[1:3], 16), int(hexval[3:5], 16), int(hexval[5:7], 16)
    except Exception:
        return True
    for a in allowed:
        ar, ag, ab = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
        if abs(r - ar) <= tol and abs(g - ag) <= tol and abs(b - ab) <= tol:
            return True
    return False


def audit_with_pdfplumber(path):
    import pdfplumber
    findings = {"pages": 0, "issues": [], "colors_foreign": [], "margins": [],
                "bottom_risk": [], "mono_split": []}
    with pdfplumber.open(path) as pdf:
        findings["pages"] = len(pdf.pages)
        foreign = {}
        last = len(pdf.pages)
        mono_bottom = {}     # pág -> hay texto mono pegado al borde inferior útil
        mono_top_y = {}      # pág -> `top` del PRIMER carácter mono en la banda superior
        header_tops = {}     # pág -> lista de `top` de cabeceras de tarjeta ("PROMPT · COPIAR")
        for pno, page in enumerate(pdf.pages, 1):
            pw, ph = page.width, page.height
            content_area_bottom = ph - FOOTER_PT   # borde inferior del área útil
            all_words = page.extract_words() or []
            # Excluir el pie (vive en la banda reservada bajo el área de contenido);
            # así no se confunde el número de página con un "bloque al borde".
            words = [w for w in all_words if w["bottom"] <= content_area_bottom + 2]
            # Cabeceras de tarjeta: la banda dorada dice "PROMPT · COPIAR".
            # Si una página arranca con cabecera antes del mono, es una tarjeta
            # NUEVA, no la continuación de la anterior.
            header_tops[pno] = [w["top"] for w in words
                                if w.get("text", "").strip().upper() in ("COPIAR", "PROMPT")]
            if words:
                min_x = min(w["x0"] for w in words)
                max_x = max(w["x1"] for w in words)
                min_top = min(w["top"] for w in words)
                max_bottom = max(w["bottom"] for w in words)
                left, right, top = min_x, pw - max_x, min_top
                for name, val in (("izq", left), ("der", right), ("sup", top)):
                    if val < MARGIN_PT * 0.5:  # menos de la mitad del margen objetivo
                        findings["margins"].append(
                            {"page": pno, "side": name, "mm": round(val / PT_PER_MM, 1)})
                # Contenido al filo del borde inferior en página no-última.
                # Solo BLOQUEA si lo que roza el borde es MONO (posible tarjeta al
                # filo); el texto normal (párrafos) se reporta como aviso: un
                # párrafo que termina cerca del margen es paginación normal.
                gap = content_area_bottom - max_bottom
                if pno != last and gap < BOTTOM_ALERT_PT:
                    edge_mono = any(
                        is_mono(ch.get("fontname"))
                        and ch["bottom"] >= content_area_bottom - BOTTOM_ALERT_PT
                        and ch["bottom"] <= content_area_bottom + 2
                        for ch in (page.chars or []))
                    findings["bottom_risk"].append(
                        {"page": pno, "mm_from_content_bottom": round(gap / PT_PER_MM, 1),
                         "mono": edge_mono})
            # colores de texto (por objeto; complementado con la pasada por píxeles)
            # y rastro de bloques monoespaciados en las bandas superior/inferior.
            for ch in (page.chars or []):
                hx = rgb_to_hex(ch.get("non_stroking_color"))
                if hx and hx not in ALLOWED and not near(hx, ALLOWED):
                    foreign[hx] = foreign.get(hx, 0) + 1
                if is_mono(ch.get("fontname")):
                    if ch["bottom"] >= content_area_bottom - BAND_PT and ch["bottom"] <= content_area_bottom + 2:
                        mono_bottom[pno] = True
                    if ch["top"] <= MARGIN_PT + BAND_PT:
                        y = ch["top"]
                        if pno not in mono_top_y or y < mono_top_y[pno]:
                            mono_top_y[pno] = y
        # Un bloque monoespaciado (prompt/código) que termina al borde inferior de
        # una página y reaparece al inicio de la siguiente = prompt probablemente
        # cortado — SALVO que la página siguiente traiga una cabecera de tarjeta
        # ("PROMPT · COPIAR") por ENCIMA de ese mono: entonces es una tarjeta
        # nueva que simplemente empieza arriba (dos tarjetas seguidas ≠ corte).
        for pno in range(1, last):
            if mono_bottom.get(pno) and (pno + 1) in mono_top_y:
                y_mono = mono_top_y[pno + 1]
                nueva_tarjeta = any(t <= y_mono + 2 for t in header_tops.get(pno + 1, []))
                if not nueva_tarjeta:
                    findings["mono_split"].append({"between": [pno, pno + 1]})
        findings["colors_foreign"] = [
            {"hex": k, "count": v} for k, v in sorted(foreign.items(), key=lambda x: -x[1])[:12]
        ]
    return findings


def audit_colors_pixels(path):
    """Auditoría de color REAL: renderiza el PDF a imagen y muestrea píxeles.
    Funciona con cualquier PDF (Canva, Word, Chrome…), no depende de cómo se
    codificaron los colores. Devuelve el % de área con color fuera de la paleta
    y los tonos foráneos dominantes. Requiere pdftoppm (poppler) + Pillow."""
    import tempfile, subprocess, glob, shutil
    try:
        from PIL import Image
    except ImportError:
        return None
    if not shutil.which("pdftoppm"):
        return None
    allowed_rgb = []
    for h in ALLOWED:
        try:
            allowed_rgb.append((int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)))
        except Exception:
            pass
    tmp = tempfile.mkdtemp(prefix="golden-audit-")
    try:
        subprocess.run(["pdftoppm", "-png", "-r", "48", path, os.path.join(tmp, "p")],
                       check=True, capture_output=True, timeout=90)
        total = foreign = 0
        buckets = {}
        for png in sorted(glob.glob(os.path.join(tmp, "p*.png"))):
            im = Image.open(png).convert("RGB")
            for px in im.getdata():
                total += 1
                r, g, b = px
                if max(px) - min(px) < 18:        # gris/blanco/negro = papel y texto
                    continue
                near_any = any(abs(r - ar) <= 42 and abs(g - ag) <= 42 and abs(b - ab) <= 42
                               for ar, ag, ab in allowed_rgb)
                if near_any:
                    continue
                foreign += 1
                key = (r // 24 * 24, g // 24 * 24, b // 24 * 24)
                buckets[key] = buckets.get(key, 0) + 1
        pct = round(100.0 * foreign / max(total, 1), 2)
        top = sorted(buckets.items(), key=lambda x: -x[1])[:6]
        top_hex = [{"hex": "#%02x%02x%02x" % k,
                    "pct": round(100.0 * v / max(total, 1), 2)} for k, v in top]
        return {"foreign_pct": pct, "top": top_hex}
    except Exception:
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def audit_with_pypdf(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    return {
        "pages": len(r.pages),
        "issues": ["Análisis básico: pypdf no extrae posiciones/colores finos. "
                   "Instala pdfplumber para el auditoría completa."],
        "colors_foreign": [], "margins": [], "bottom_risk": [],
    }


def build_report(path, f):
    lines = []
    lines.append("# Auditoría Golden PDF")
    lines.append("")
    lines.append("**Archivo:** " + os.path.basename(path))
    lines.append("**Páginas:** " + str(f["pages"]))
    lines.append("")
    score_hits = []

    if f["margins"]:
        lines.append("## Márgenes invadidos")
        for m in f["margins"]:
            lines.append(f"- Página {m['page']}: borde {m['side']} a solo {m['mm']}mm "
                         f"(objetivo {MARGIN_MM}mm).")
        score_hits.append("margenes")
    else:
        lines.append("## Márgenes — OK")
    lines.append("")

    mono_split = f.get("mono_split", [])
    risk_mono = [b for b in f["bottom_risk"] if b.get("mono")]
    risk_texto = [b for b in f["bottom_risk"] if not b.get("mono")]
    if mono_split or risk_mono:
        lines.append("## Riesgo de bloque cortado / paginación")
        if mono_split:
            lines.append("**Prompt monoespaciado cortado entre páginas** (lo peor para "
                         "copiar y pegar):")
            for s in mono_split:
                lines.append(f"- Un bloque de código/prompt sigue de la página "
                             f"{s['between'][0]} a la {s['between'][1]}.")
        for b in risk_mono:
            lines.append(f"- Página {b['page']}: un bloque de prompt llega a "
                         f"{b['mm_from_content_bottom']}mm del borde del área útil "
                         f"(y no es la última página).")
        lines.append("")
        lines.append("> Recomendación: regenerar con `build_pdf.py` para que cada "
                     "prompt quede en una sola página (bloques atómicos + auto-fit).")
        score_hits.append("paginacion")
    else:
        lines.append("## Paginación — sin bloques cortados")
    if risk_texto:
        lines.append("")
        lines.append("### Avisos (no bloquean el veredicto)")
        for b in risk_texto:
            lines.append(f"- Página {b['page']}: texto normal termina a "
                         f"{b['mm_from_content_bottom']}mm del borde del área útil — "
                         f"paginación normal de párrafos, nada cortado.")
    lines.append("")

    # Color: la pasada por píxeles manda (funciona en cualquier PDF).
    cp = f.get("colors_pixel")
    if cp is not None:
        if cp["foreign_pct"] >= 2.0:
            lines.append("## Colores fuera de marca")
            lines.append(f"~{cp['foreign_pct']}% del área usa color fuera de la paleta Golden. "
                         "Tonos foráneos dominantes:")
            for c in cp["top"]:
                if c["pct"] >= 0.2:
                    lines.append(f"- `{c['hex']}` (~{c['pct']}% del área).")
            score_hits.append("colores")
        else:
            lines.append(f"## Colores — dentro de la paleta Golden (~{cp['foreign_pct']}% foráneo)")
    elif f["colors_foreign"]:
        lines.append("## Colores fuera de marca")
        for c in f["colors_foreign"]:
            lines.append(f"- `{c['hex']}` ({c['count']} usos) no pertenece a la paleta Golden.")
        score_hits.append("colores")
    else:
        lines.append("## Colores — dentro de la paleta Golden")
    lines.append("")

    for extra in f.get("issues", []):
        lines.append("> " + extra)

    verdict = "APROBADO" if not score_hits else "REQUIERE ARREGLO (" + ", ".join(score_hits) + ")"
    lines.insert(4, "**Veredicto:** " + verdict + "\n")
    return "\n".join(lines), verdict, score_hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--json")
    ap.add_argument("--palette",
                    help="JSON con allowed_hex_for_audit propio (documentos de otra marca)")
    args = ap.parse_args()

    if args.palette:
        # Paleta alterna: el mismo auditor sirve para documentos que no se
        # emiten bajo la marca Golden.
        global ALLOWED
        with open(args.palette, encoding="utf-8") as fh:
            ALLOWED = set(h.lower() for h in json.load(fh)["allowed_hex_for_audit"])

    try:
        f = audit_with_pdfplumber(args.pdf)
        f["colors_pixel"] = audit_colors_pixels(args.pdf)   # None si falta Pillow/pdftoppm
        engine = "pdfplumber"
    except ImportError:
        try:
            f = audit_with_pypdf(args.pdf)
            engine = "pypdf"
        except ImportError:
            print("Falta dependencia. Instala:  pip install pdfplumber", file=sys.stderr)
            sys.exit(2)

    report, verdict, hits = build_report(args.pdf, f)
    print(report)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"engine": engine, "verdict": verdict, "issues": hits, "detail": f},
                      fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
