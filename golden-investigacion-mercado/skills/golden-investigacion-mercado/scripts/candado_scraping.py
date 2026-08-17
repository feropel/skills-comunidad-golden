#!/usr/bin/env python3
"""
CANDADO DE SCRAPING — Golden Group
Convierte la REGLA CERO de prosa (que se puede olvidar) en un chequeo que no se puede saltar.

Recibe la respuesta cruda de firecrawl_scrape y dictamina si el dato SIRVE o es BASURA.
Los 4 modos de fallo que cubre están MEDIDOS en vivo, no supuestos:
  1 ALUCINACION  - pagina hueca, el extractor inventa un producto entero
  2 SENUELO      - redirige y devuelve el menu/portada de otra pagina
  3 MURO ANTI-BOT- no viene el campo json en absoluto
  4 CAPTCHA      - muro de captcha, inventa datos CON metadata.title poblado (rompe el check 2)

Uso:
  python3 candado_scraping.py respuesta.json
  python3 candado_scraping.py respuesta.json --pedi "removedor de verrugas"
  cat respuesta.json | python3 candado_scraping.py -

Salida: informe legible + codigo de salida 0 (PASA) o 1 (DESCARTAR).
Manual: ../references/scraping-firecrawl.md
"""

import json
import re
import sys

# Marcas de captcha / muro de seguridad vistas en vivo (MercadoLibre, Amazon)
SENALES_CAPTCHA_URL = ("/captcha", "captcha/wall", "/errors/validatecaptcha", "/sorry/")
SENALES_CAPTCHA_TITULO = ("seguridad", "security", "captcha", "robot", "verificacion",
                          "verificación", "access denied", "iniciar sesion", "iniciar sesión",
                          "sign in", "log in")
SENALES_ANTIBOT_META = ("anti-csrftoken", "encrypted-slate-token", "cf-chl", "datadome")

# Valores que delatan relleno inventado
BASURA = {"", "n/a", "na", "none", "null", "-", "sin datos", "no disponible", "0"}
PLACEHOLDER = re.compile(r"^\s*(producto|product|item|articulo|artículo|title|titulo|título|"
                         r"ejemplo|example|nombre|name)\s*[\-_ ]?\d+\s*$", re.I)


def _aplanar(obj, prof=0):
    """Devuelve todos los valores hoja de un json anidado."""
    if prof > 8:
        return []
    if isinstance(obj, dict):
        return [v for x in obj.values() for v in _aplanar(x, prof + 1)]
    if isinstance(obj, list):
        return [v for x in obj for v in _aplanar(x, prof + 1)]
    return [obj]


def _norm(u):
    if not u:
        return ""
    u = re.sub(r"^https?://(www\.)?", "", str(u).strip().lower())
    return u.rstrip("/").split("?")[0]


def auditar(resp, pedi=None):
    """Devuelve (veredicto, lista_de_hallazgos). veredicto: 'PASA' | 'DESCARTAR' | 'REVISAR'."""
    fallos, avisos, oks = [], [], []
    meta = resp.get("metadata", {}) or {}

    # ---- CHECK 1 - existe el campo json? (modo 3: muro anti-bot)
    tiene_json = "json" in resp and resp["json"] not in (None, {}, [])
    if not tiene_json:
        # rawHtml/markdown no pasan por el extractor: son inmunes a los modos 1, 2 y 4
        if any(k in resp for k in ("rawHtml", "markdown", "html")):
            oks.append("Formato sin extractor (rawHtml/markdown): inmune a alucinacion. "
                       "Verificar el contenido a mano igual.")
            return "REVISAR", (fallos, avisos, oks)
        fallos.append("CHECK 1 · MURO ANTI-BOT: la respuesta NO trae campo `json`. "
                      "Medido en Amazon: solo metadata con anti-csrftoken.")
    else:
        oks.append("CHECK 1 · existe el campo `json`")

    blob = " ".join(str(v).lower() for v in _aplanar(meta))
    if any(s in blob for s in SENALES_ANTIBOT_META):
        fallos.append("CHECK 1 · metadata con firma anti-bot "
                      f"({', '.join(s for s in SENALES_ANTIBOT_META if s in blob)}).")

    # ---- CHECK 2 - metadata.title poblado? (modo 1: alucinacion)
    titulo = (meta.get("title") or meta.get("ogTitle") or meta.get("og:title") or "").strip()
    if not titulo:
        fallos.append("CHECK 2 · ALUCINACION: `metadata.title` VACIO. La pagina no cargo y el "
                      "extractor inventa. Medido: devolvio un Smart TV en una pagina de verrugas.")
    else:
        oks.append(f"CHECK 2 · title poblado ({titulo[:55]!r})")
        # modo 4: el title puede estar poblado Y ser un muro
        tl = titulo.lower()
        if any(s in tl for s in SENALES_CAPTCHA_TITULO):
            fallos.append(f"CHECK 2-bis · CAPTCHA/LOGIN: el title es un muro ({titulo[:45]!r}). "
                          "Medido en MercadoLibre: 'Seguridad — Mercado Libre' + 8 productos "
                          "inventados. OJO: el check 2 normal pasa en verde aqui.")

    # ---- CHECK 3 - url == sourceURL? (modo 2: senuelo)
    src, fin = _norm(meta.get("sourceURL")), _norm(meta.get("url"))
    if src and fin and src != fin:
        if any(s in fin for s in SENALES_CAPTCHA_URL):
            fallos.append(f"CHECK 3 · CAPTCHA: redirigido a un muro -> {fin[:70]}")
        else:
            avisos.append(f"CHECK 3 · REDIRECCION: pediste {src[:45]} y leiste {fin[:45]}. "
                          "Puede ser el modo SENUELO (Temu devolvio 72 categorias de ropa).")
    elif src:
        oks.append("CHECK 3 · sin redireccion")

    # ---- CHECK 4 - el dato responde a lo que pedi? (la unica que caza los 4 modos)
    if tiene_json:
        hojas = [v for v in _aplanar(resp["json"]) if isinstance(v, (str, int, float))]
        textos = [str(v).strip() for v in hojas]
        if not textos:
            fallos.append("CHECK 4 · el `json` no trae ningun valor.")
        else:
            vacios = sum(1 for t in textos if t.lower() in BASURA)
            pct = vacios / len(textos)
            if pct >= 0.5:
                fallos.append(f"CHECK 4 · {vacios}/{len(textos)} valores vacios o 'N/A' "
                              f"({pct:.0%}). Medido en Temu: 72 categorias con precio N/A.")
            elif pct >= 0.25:
                avisos.append(f"CHECK 4 · {vacios}/{len(textos)} valores vacios ({pct:.0%}).")

            marcadores = [t for t in textos if PLACEHOLDER.match(t)]
            if marcadores:
                fallos.append(f"CHECK 4 · RELLENO INVENTADO: valores tipo plantilla "
                              f"{marcadores[:3]}. Medido en MercadoLibre: 'Producto 1'..'Producto 8'.")

            if pedi:
                claves = [w for w in re.findall(r"\w+", pedi.lower()) if len(w) > 3]
                if claves:
                    cuerpo = " ".join(textos).lower()
                    hit = [k for k in claves if k in cuerpo]
                    if not hit:
                        fallos.append(f"CHECK 4 · EL DATO NO RESPONDE A LO PEDIDO: ninguna palabra "
                                      f"de {claves} aparece en el resultado. Es la verificacion que "
                                      f"caza los 4 modos.")
                    else:
                        oks.append(f"CHECK 4 · el dato menciona lo pedido ({hit})")
            else:
                avisos.append("CHECK 4 · sin --pedi no se puede verificar la pertinencia. "
                              "Es la verificacion MAS importante: pasala siempre.")

    if fallos:
        return "DESCARTAR", (fallos, avisos, oks)
    if avisos:
        return "REVISAR", (fallos, avisos, oks)
    return "PASA", (fallos, avisos, oks)


def main():
    args = [a for a in sys.argv[1:]]
    pedi = None
    if "--pedi" in args:
        i = args.index("--pedi")
        pedi = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]

    if not args:
        print(__doc__)
        return 2

    try:
        crudo = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()
        resp = json.loads(crudo)
    except Exception as e:
        print(f"No se pudo leer el JSON: {e}")
        return 2

    veredicto, (fallos, avisos, oks) = auditar(resp, pedi)

    print("=" * 68)
    print(f"  CANDADO DE SCRAPING — VEREDICTO: {veredicto}")
    print("=" * 68)
    for o in oks:
        print(f"  [ok]     {o}")
    for a in avisos:
        print(f"  [AVISO]  {a}")
    for f in fallos:
        print(f"  [FALLO]  {f}")
    print("-" * 68)
    if veredicto == "DESCARTAR":
        print("  NO usar este dato. No citarlo, no guardarlo en PRODUCTO.json, no reportarlo.")
        print("  Escribir 'no obtenido' y proponer otra via. Un 'no pude' es un resultado valido.")
    elif veredicto == "REVISAR":
        print("  Revisar a mano antes de usar. La duda NO se resuelve a favor del dato.")
    else:
        print("  Dato utilizable. Citar la fuente y la fecha de consulta igual.")
    print()
    return 1 if veredicto == "DESCARTAR" else 0


if __name__ == "__main__":
    sys.exit(main())
