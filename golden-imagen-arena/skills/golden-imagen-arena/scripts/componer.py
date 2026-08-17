#!/usr/bin/env python3
"""Pega el PNG real del producto (con canal alfa) sobre una placa generada por IA.

Uso: componer.py <placa.png> <salida.png> <producto.png:ancho_rel:cx_rel:cy_rel> [...]
  ancho_rel : ancho del producto como fraccion del ancho de la placa (0-1)
  cx_rel    : centro horizontal del producto (0-1)
  cy_rel    : posicion de la BASE del producto (0-1, 1 = borde inferior)
Se pueden pasar varios productos en la misma llamada.
La etiqueta queda intacta porque es la foto original, solo se escala.
Dependencia: Pillow (pip install Pillow).
"""
import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Falta Pillow. Instala con: pip install Pillow")


def recortar_alfa(im):
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def sombra(frasco, desenfoque=18, opacidad=90, offset=(6, 14)):
    alfa = frasco.split()[3]
    capa = Image.new("RGBA", (frasco.width + desenfoque * 4, frasco.height + desenfoque * 4), (0, 0, 0, 0))
    negro = Image.new("RGBA", frasco.size, (60, 40, 30, opacidad))
    capa.paste(negro, (desenfoque * 2 + offset[0], desenfoque * 2 + offset[1]), alfa)
    return capa.filter(ImageFilter.GaussianBlur(desenfoque))


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    placa = Image.open(sys.argv[1]).convert("RGBA")
    salida = sys.argv[2]
    W, H = placa.size

    for spec in sys.argv[3:]:
        ruta, ancho_rel, cx_rel, cy_rel = spec.rsplit(":", 3)
        frasco = recortar_alfa(Image.open(ruta).convert("RGBA"))
        nuevo_ancho = int(W * float(ancho_rel))
        nuevo_alto = int(frasco.height * nuevo_ancho / frasco.width)
        frasco = frasco.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        x = int(W * float(cx_rel)) - nuevo_ancho // 2
        y = int(H * float(cy_rel)) - nuevo_alto

        s = sombra(frasco)
        # alpha_composite exige dest >= 0; una colocacion cerca del borde daria
        # coordenada negativa y crashearia. Se recorta a 0 en ambos ejes.
        sx = max(0, x - (s.width - nuevo_ancho) // 2)
        sy = max(0, y - (s.height - nuevo_alto) // 2)
        placa.alpha_composite(s, (sx, sy))
        placa.alpha_composite(frasco, (max(0, x), max(0, y)))

    # PNG es sin perdida: 'quality' no aplica. La salida es un PNG intermedio pesado;
    # pasalo por optimizar-webp.py antes de entregar.
    placa.convert("RGB").save(salida)
    print("ok", salida, placa.size)


if __name__ == "__main__":
    main()
