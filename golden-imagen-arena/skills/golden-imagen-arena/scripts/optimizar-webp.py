#!/usr/bin/env python3
"""
optimizar-webp.py — convierte una imagen a WebP < 150 KB en cualquier proporcion.
Uso: python3 optimizar-webp.py <entrada> <salida.webp> [1080x1080] [max_kb=150]

Ejemplos:
  python3 optimizar-webp.py hero.png "TAG RECEDE - Hero 01.webp" 1080x1080
  python3 optimizar-webp.py info.png "TAG RECEDE - Como actua 01.webp" 1080x1350 120

Por que existe: sips de macOS no exporta WebP, y las piezas de secciones son 1080x1350
(el script de golden-ecom-magic solo hacia cuadradas). Dependencia: Pillow.
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
