#!/usr/bin/env python3
"""guardar_fuentes.py · golden-ebook

Guarda en disco el TEXTO de cada fuente del ebook, para que la hoja del Paso 5b pueda citarla
literalmente y el verificador (C25) compruebe esa cita contra el texto real, no contra la
memoria de quien escribió.

Uso:
    $PY scripts/guardar_fuentes.py EBOOK/ebook.json [--rehacer]
      → EBOOK/fuentes-texto/<id>.txt, uno por fuente. Si el archivo ya existe no se vuelve a
        bajar (salvo con --rehacer): puedes pegar tú el texto de una fuente que ningún método
        logre leer, y queda anotado en su primera línea.

Métodos, en orden, según la URL:
  · doi.org/...     → registro de Crossref (título, autores, revista, año) + resumen de PubMed
                      si el DOI está indexado ahí.
  · un .pdf         → descarga y pdftotext.
  · cualquier otra  → navegador Chromium (Playwright): el texto visible de la página. Muchos
                      sitios bloquean a los robots con 403 pero sí sirven al navegador.

La primera línea de cada .txt dice de dónde y cuándo salió el texto. Uso interno: el texto no
se publica ni se entrega; solo sirve para comprobar citas. Códigos: 0 todas guardadas ·
1 alguna no se pudo leer (se lista) · 2 error de uso.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (golden-ebook; verificacion de fuentes)"}


def bajar(url, timeout=60):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def por_doi(doi):
    partes = []
    reg = json.loads(bajar("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    autores = ", ".join(f"{a.get('family', '')} {a.get('given', '')}".strip() for a in reg.get("author", []))
    partes.append(f"TÍTULO: {' '.join(reg.get('title', []))}\nAUTORES: {autores}\n"
                  f"REVISTA: {' '.join(reg.get('container-title', []))}\n"
                  f"AÑO: {reg.get('issued', {}).get('date-parts', [[None]])[0][0]}")
    e = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ids = json.loads(bajar(f"{e}/esearch.fcgi?db=pubmed&retmode=json&term="
                           + urllib.parse.quote(doi + "[doi]")))["esearchresult"]["idlist"]
    if ids:
        partes.append(bajar(f"{e}/efetch.fcgi?db=pubmed&id={ids[0]}&rettype=abstract&retmode=text")
                      .decode("utf-8", "replace"))
    return "\n\n".join(partes), "Crossref" + (" + PubMed" if ids else "")


def por_pdf(url):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as t:
        t.write(bajar(url, timeout=300))
    try:
        return subprocess.run(["pdftotext", "-layout", t.name, "-"], capture_output=True, text=True,
                              timeout=600).stdout, "PDF + pdftotext"
    finally:
        os.unlink(t.name)


def por_navegador(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
                                     "(KHTML, like Gecko) Chrome/151.0 Safari/537.36")
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(2500)
        # Todo el texto del documento, también el oculto: en un carrusel o en pestañas el
        # innerText solo trae lo visible (medido: la página del acueducto perdía sus cifras).
        texto = pg.evaluate("""() => { const c = document.body.cloneNode(true);
            c.querySelectorAll('script,style,noscript,svg').forEach(n => n.remove());
            c.querySelectorAll('p,div,li,h1,h2,h3,h4,br,td,section').forEach(n => n.append(' '));
            return c.textContent; }""")
        nav.close()
    return texto, "navegador Chromium"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not os.path.exists(args[0]):
        print(__doc__)
        sys.exit(2)
    rehacer = "--rehacer" in sys.argv
    e = json.load(open(args[0], encoding="utf-8"))
    carpeta = os.path.join(os.path.dirname(os.path.abspath(args[0])), "fuentes-texto")
    os.makedirs(carpeta, exist_ok=True)
    hoy = datetime.date.today().isoformat()
    malas, hechas = [], 0
    for f in e.get("fuentes", []):
        destino = os.path.join(carpeta, f"{f['id']}.txt")
        if os.path.exists(destino) and not rehacer:
            hechas += 1
            continue
        url = str(f.get("url", ""))
        try:
            if url.startswith("https://doi.org/"):
                texto, metodo = por_doi(url[len("https://doi.org/"):])
            elif re.search(r"\.pdf(?:$|\?)", url, re.I):
                texto, metodo = por_pdf(url)
            else:
                texto, metodo = por_navegador(url)
            # Un registro de Crossref sin resumen es corto por naturaleza (título, autores,
            # revista, año); una página web de menos de 200 caracteres es casi siempre un bloqueo.
            minimo = 60 if metodo.startswith("Crossref") else 200
            if len(texto.strip()) < minimo:
                raise ValueError(f"texto demasiado corto ({len(texto.strip())} caracteres): ¿bloqueo o página vacía?")
            with open(destino, "w", encoding="utf-8") as out:
                out.write(f"# fuente {f['id']} · {url} · {metodo} · {hoy}\n\n{texto}")
            hechas += 1
        except Exception as ex:  # noqa: BLE001
            malas.append(f"{f['id']}: {type(ex).__name__} {str(ex)[:120]}")
    print(json.dumps({"carpeta": carpeta, "guardadas": hechas, "total": len(e.get("fuentes", [])),
                      "sin_leer": malas}, ensure_ascii=False))
    sys.exit(1 if malas else 0)


if __name__ == "__main__":
    main()
