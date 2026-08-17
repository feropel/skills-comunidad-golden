#!/usr/bin/env python3
"""
optimizar-webp.py — baja una imagen a WebP < 150 KB para Shopify/Golden, en
cualquier proporcion (cuadrada 1080x1080 o vertical 1080x1350).
Acepta un archivo local O una URL http(s) (la del output del MCP, `jobs_get`).
Uso: python3 optimizar-webp.py <entrada.png|jpg|URL> <salida.webp> [1080x1080] [max_kb=150]

Ejemplos:
  python3 optimizar-webp.py hero.png "TAG RECEDE - Carrusel 01.webp" 1080x1080
  python3 optimizar-webp.py info.png "TAG RECEDE - Seccion 01.webp" 1080x1350 120
  python3 optimizar-webp.py "https://ecom-magic.ai/public-banners/mcp-1.png" pieza.webp

Por que existe: la descarga "optimizada" del navegador no siempre aterriza en disco, y
sips de macOS no exporta WebP. Metodo fiable = bajar el PNG full-res del DOM y convertir
aqui con Pillow. Las infografias de secciones son 1080x1350, no cuadradas: pasar el tamano
como WxH conserva la proporcion (misma logica que golden-imagen-arena).
Dependencia: Pillow (pip install Pillow). Ej. real Tag Recede: quality 85 -> 124.8 KB.
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow. Instala con: pip install Pillow")


def parse_size(txt):
    """'1080x1350' -> (1080, 1350). '1080' -> (1080, 1080). '' -> None (deja el original)."""
    if not txt or txt.lower() in ("orig", "original", "-"):
        return None
    if "x" in txt.lower():
        w, h = txt.lower().split("x", 1)
        return int(w), int(h)
    lado = int(txt)
    return lado, lado


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    size = parse_size(sys.argv[3] if len(sys.argv) > 3 else "1080x1080")
    max_kb = float(sys.argv[4]) if len(sys.argv) > 4 else 150.0

    if src.startswith(("http://", "https://")):
        import io
        import urllib.request
        with urllib.request.urlopen(src, timeout=90) as r:
            src = io.BytesIO(r.read())

    im = Image.open(src).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)

    q = 90
    while True:
        im.save(out, "WEBP", quality=q, method=6)
        kb = os.path.getsize(out) / 1024
        if kb <= max_kb or q <= 40:
            break
        q -= 5

    estado = "OK" if kb <= max_kb else "AVISO: no bajo del limite ni con quality=40"
    print(f"{estado} {out} · quality={q} · {kb:.1f} KB · {im.width}x{im.height}")


if __name__ == "__main__":
    main()
