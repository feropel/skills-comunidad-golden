#!/usr/bin/env python3
"""
GOLDEN PDF · verbatim_check.py
Compuerta de seguridad para el modo "arreglar": confirma que el PDF nuevo
conserva el texto del original SIN alterar una sola palabra.

Compara el texto de --old (PDF o .txt/.md) contra --new (PDF). Para cada
línea con contenido del original, verifica que aparezca idéntica en el nuevo
(normalizando solo los espacios en blanco). Reporta lo que falte o cambió.

Uso:
    python verbatim_check.py --old viejo.pdf --new nuevo.pdf
    python verbatim_check.py --old fuente.md --new nuevo.pdf --json diff.json

Salida: exit 0 si todo coincide; exit 3 si hay diferencias.
"""
import sys, os, re, json, argparse, logging, unicodedata
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Misma canonicalización que la compuerta de build_pdf.py: NFKC + equivalencias
# tipográficas (elipsis, comillas curvas, guiones largos, nbsp). Así las dos
# compuertas juzgan igual y no hay falsos "no idéntico" por variantes visuales.
_TYPO_EQ = {"…": "...", "‘": "'", "’": "'", "“": '"',
            "”": '"', "–": "-", "—": "-", " ": " "}


def read_text(path):
    if path.lower().endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)
    with open(path, encoding="utf-8") as f:
        return f.read()


def norm(s):
    for k, v in _TYPO_EQ.items():
        s = s.replace(k, v)
    # Selectores de variación de emoji (U+FE0F/U+FE0E): el extractor de PDF los
    # pierde aunque el emoji se vea bien; se ignoran al comparar (igual que en
    # la compuerta de build_pdf.py — las dos deben juzgar idéntico).
    s = s.replace("️", "").replace("︎", "")
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def segments(text):
    """Trozos con contenido real para comparar (líneas no vacías, sin markup
    de maquetación tipo fences, ::: o front matter).

    El PDF conserva el TEXTO, no el marcado: un `## Título` sale como "Título",
    una tabla pierde los pipes, y el front matter YAML se vuelve portada sin las
    etiquetas `clave:`. Por eso acá se compara el texto ya despojado de marcado,
    igual de ambos lados: así la compuerta no marca falsas diferencias cuando el
    original es un .md (uso documentado en el encabezado)."""
    # El front matter YAML es metadata de portada, no contenido copiable literal.
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    segs = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"^(```|~~~|:::|---+$)", s):
            continue
        # El PDF no lleva el marcador de encabezado, de lista ni los pipes de tabla.
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^([-*]|\d+\.)\s+", "", s)
        if s.startswith("|"):
            s = s.strip("|").replace("|", " ")
        if len(norm(s)) < 3:
            continue
        segs.append(s)
    return segs



# v6.2 · EL PUNTO CIEGO DE ESTA COMPUERTA, medido ejerciendo el Paso C contra un
# PDF ajeno de verdad. Esta compuerta compara EXTRACCION contra EXTRACCION, asi
# que garantiza "no cambie lo que lei", NO "lo que lei es lo que el documento
# decia". Si el PDF de origen usa una fuente monoespaciada con ligaduras, el
# extractor ya entrega el texto corrompido y los dos lados traen el MISMO error:
# la comparacion da OK con el dano dentro. Medido: un `<<JSON>>` del documento
# original salio `<>` en la extraccion, viajo al PDF reconstruido y la compuerta
# lo bendijo. Es la misma clase que se arreglo en v5.5 para JetBrains Mono, pero
# ahora en una fuente que no controlamos. No se puede reparar desde aqui; SI se
# puede AVISAR, que es la diferencia entre un riesgo conocido y una trampa.
# AQUI VIVIO UN DETECTOR DE LIGADURAS, RETIRADO EN v6.4. Se escribio en v6.2
# para defender de un fallo que resulto NO EXISTIR: yo mismo escribi `<<JSON>>`
# sin escapar en el HTML del fixture con el que lo "medi", el navegador se comio
# `<JSON>` como una etiqueta desconocida y el PDF YA DECIA `<>` antes de que
# ningun extractor lo tocara. El extractor fue fiel y la compuerta acerto al dar
# OK. Comprobado despues con los dos fixtures lado a lado: escapado devuelve
# `<<JSON>>`, sin escapar devuelve `<>`.
#
# Se retira por dos razones y las dos importan:
#   1. No defendia de nada demostrado. Un guardian contra un fallo imaginario
#      es deuda: hay que mantenerlo y enseña a desconfiar de lo que esta bien.
#   2. SI hacia dano medible. Acusaba al IDIOMA, no al defecto: contra un prompt
#      de programacion legitimo (funcion flecha, operador !=, etiquetas HTML,
#      fragmento <> de React) marcaba LAS CUATRO secuencias, todas correctas.
#
# Lo que SI queda, porque es cierto por construccion y no por medicion: esta
# compuerta compara EXTRACCION contra EXTRACCION, asi que no puede ver un error
# del extractor. Eso no se arregla con patrones; se arregla pidiendo la FUENTE
# ORIGINAL al reconstruir un PDF ajeno, y asi esta escrito en el Paso C.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--json")
    args = ap.parse_args()

    old_text = read_text(args.old)
    new_full = norm(read_text(args.new))

    missing = []
    checked = 0
    for seg in segments(old_text):
        checked += 1
        if norm(seg) not in new_full:
            missing.append(seg)

    ok = not missing
    print("# Compuerta verbatim")
    print("Original:", os.path.basename(args.old), "· Nuevo:", os.path.basename(args.new))
    print("Segmentos verificados:", checked)
    if ok:
        print("Resultado: OK — el texto se conservó idéntico.")
        print("   (idéntico ENTRE LOS DOS PDFs. Si el original venía de otra")
        print("    herramienta, esto NO prueba que el PDF viejo dijera lo que")
        print("    decía su documento fuente: para eso hace falta la fuente.)")
    else:
        print("Resultado: DIFERENCIAS —", len(missing), "segmento(s) del original NO aparecen idénticos:")
        for m in missing[:40]:
            print("   -", (m[:90] + ("…" if len(m) > 90 else "")))
        print("\n> El texto no debe alterarse. Revisa la extracción o corrige el nuevo PDF.")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"ok": ok, "checked": checked, "missing": missing,
                       },
                      f, ensure_ascii=False, indent=2)

    sys.exit(0 if ok else 3)


if __name__ == "__main__":
    main()
