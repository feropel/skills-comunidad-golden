#!/usr/bin/env python3
"""
optimizar-webp.py — lleva una pieza a su medida de DESTINO sin deformar el producto.

Uso: python3 optimizar-webp.py <entrada> <salida.webp> [destino|WxH] [max_kb] [--modo cover|contain]

El tercer argumento acepta un DESTINO con nombre (recomendado) o una medida cruda:

    galeria-shopify   2048x2048  300 KB   zoom de la ficha. TECHO PERMANENTE, ver abajo
    ficha-html        1080x1350  150 KB   infografia dentro de la descripcion (sin transformar)
    ig-feed           1080x1350  150 KB   Instagram feed - Facebook - Reddit
    ig-reel           1080x1920  150 KB   TikTok - reels - stories
    cuadrado          1080x1080  150 KB   LinkedIn - Telegram - Threads
    youtube           1920x1080  200 KB   YouTube - Google Business
    pinterest         1080x1620  150 KB   X - Pinterest

Ejemplos:
  python3 optimizar-webp.py hero.png "TAG RECEDE - Galeria 01.webp" galeria-shopify
  python3 optimizar-webp.py info.png "TAG RECEDE - Como actua 01.webp" ficha-html
  python3 optimizar-webp.py x.png y.webp 1080x1350 120 --modo contain

🔴 POR QUE ESTE SCRIPT NO DEFORMA (defecto medido el 2026-09-08)
La version anterior hacia `im.resize(size)` a secas: estiraba la imagen hasta la medida
pedida sin mirar la proporcion de origen. Medido contra un caso de control (circulo
perfecto de 1024x1024 llevado a 1080x1350): salia un ovalo de relacion 0,800, un
**20% de deformacion**. Es decir, el script de entrega de esta skill adulteraba el envase
justo cuando la Ley 1 descalifica una pieza por envase adulterado. Ahora es imposible:
se recorta (`cover`, por defecto) o se rellena con borde (`contain`), nunca se estira.

🔴 POR QUE LA GALERIA VA A 2048 Y NO A 1080
Verificado contra el CDN real de Shopify el 2026-09-08 (imagen de 600 px de la tienda):
`?width=400` devolvio 400 - `?width=1024`, `?width=2048` y `?width=4000` devolvieron los
600 originales. **Shopify REDUCE al servir, pero NUNCA AGRANDA.** El tamano de SUBIDA es
un techo permanente: una galeria subida a 1080 queda con zoom de 1080 para siempre, y no
se arregla con un parametro sino volviendo a subir. Por eso la galeria sube a 2048 (Shopify
ya sirve la variante liviana al movil por su cuenta) y solo lo que va al HTML sin
transformacion — las infografias de la descripcion — se aprieta a 1080 / 150 KB.
Una sola cifra para todo optimiza el caso equivocado.

Autoprueba: `python3 optimizar-webp.py --autoprueba` (6 casos: deformacion y agrandado,
cada uno en los dos sentidos - debe morder el malo y callar ante el bueno).
Dependencia: Pillow.
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow. Instala con: pip install Pillow")


# destino -> (ancho, alto, max_kb). Fuente: references/formato-por-destino.md
DESTINOS = {
    "galeria-shopify": (2048, 2048, 300),
    "ficha-html":      (1080, 1350, 150),
    "ig-feed":         (1080, 1350, 150),
    "ig-reel":         (1080, 1920, 150),
    "cuadrado":        (1080, 1080, 150),
    "youtube":         (1920, 1080, 200),
    "pinterest":       (1080, 1620, 150),
}


def parse_destino(txt):
    """Devuelve (size|None, max_kb|None). Acepta nombre de destino, 'WxH', 'W' u 'orig'."""
    if not txt or txt.lower() in ("orig", "original", "-"):
        return None, None
    t = txt.lower()
    if t in DESTINOS:
        w, h, kb = DESTINOS[t]
        return (w, h), float(kb)
    if "x" in t:
        w, h = t.split("x", 1)
        return (int(w), int(h)), None
    lado = int(t)
    return (lado, lado), None


def encajar(im, size, modo="cover"):
    """Lleva `im` a `size` SIN deformar nunca.

    cover   — escala hasta cubrir y recorta el sobrante por el centro. Es el default
              porque en un packshot de Golden el producto va centrado y lo que sobra es
              fondo: recortar es gratis y no inventa pixeles.
    contain — escala hasta caber entero y rellena el resto con el color del borde. Se usa
              cuando recortar se comeria producto o texto.
    """
    destino_w, destino_h = size
    origen_w, origen_h = im.size
    if (origen_w, origen_h) == (destino_w, destino_h):
        return im

    escala_cubrir = max(destino_w / origen_w, destino_h / origen_h)
    escala_caber = min(destino_w / origen_w, destino_h / origen_h)
    escala = escala_cubrir if modo == "cover" else escala_caber

    nuevo = (max(1, round(origen_w * escala)), max(1, round(origen_h * escala)))
    im = im.resize(nuevo, Image.LANCZOS)

    if modo == "cover":
        izq = (nuevo[0] - destino_w) // 2
        arr = (nuevo[1] - destino_h) // 2
        return im.crop((izq, arr, izq + destino_w, arr + destino_h))

    # contain: lienzo del color de la esquina superior izquierda, pieza centrada
    fondo = im.getpixel((0, 0))
    lienzo = Image.new("RGB", (destino_w, destino_h), fondo)
    lienzo.paste(im, ((destino_w - nuevo[0]) // 2, (destino_h - nuevo[1]) // 2))
    return lienzo


def detalle_inventado(origen, size, modo):
    """Cuanto del resultado son pixeles que el motor NUNCA genero.

    🔴 La trampa que esto vigila es la MISMA del techo de nitidez, disfrazada al reves:
    pedir `galeria-shopify` sobre un render de 1K devuelve un archivo de 2048x2048 que solo
    tiene 1024 de detalle real. El fichero dice 2048 y el zoom sigue siendo de 1K. Un techo
    con nombre de solucion es peor que el techo, porque nadie vuelve a mirarlo.
    Se arregla generando en 2K desde el motor, no agrandando despues.
    """
    if not size:
        return 0.0
    ow, oh = origen
    escala = max(size[0] / ow, size[1] / oh) if modo == "cover" else min(size[0] / ow, size[1] / oh)
    return (escala - 1) * 100 if escala > 1 else 0.0


def optimizar(src, out, size=None, max_kb=150.0, modo="cover"):
    im = Image.open(src).convert("RGB")
    origen = im.size
    if size:
        im = encajar(im, size, modo)

    q = 90
    while True:
        im.save(out, "WEBP", quality=q, method=6)
        kb = os.path.getsize(out) / 1024
        if kb <= max_kb or q <= 40:
            break
        q -= 5
    return origen, im.size, q, kb


def autoprueba():
    """Debe MORDER el caso malo y CALLAR ante el bueno. Sin las dos mitades no prueba nada."""
    from PIL import ImageDraw
    import tempfile
    try:
        import numpy as np
    except ImportError:
        print("❌ la autoprueba necesita numpy para medir la proporcion: pip install numpy")
        print("   (sin el no se puede comprobar que el script no deforma: NO se da por buena)")
        return 1

    tmp = tempfile.mkdtemp()
    fallos = []

    def relacion(ruta):
        a = np.array(Image.open(ruta).convert("L"))
        ys, xs = np.where(a < 128)
        return (xs.max() - xs.min()) / (ys.max() - ys.min())

    # control: circulo perfecto, relacion conocida = 1,000
    ctrl = os.path.join(tmp, "ctrl.png")
    im = Image.new("RGB", (1024, 1024), "white")
    ImageDraw.Draw(im).ellipse([112, 112, 912, 912], outline="black", width=12)
    im.save(ctrl)

    # 1 · LADO MALO: el estiron que hacia la version vieja debe seguir siendo detectable
    malo = os.path.join(tmp, "malo.webp")
    Image.open(ctrl).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(malo, "WEBP", quality=90)
    r = relacion(malo)
    ok = abs(1 - r) > 0.05
    print(f"  {'✅' if ok else '❌'} 1 caso MALO (estiron a 4:5)      relacion={r:.3f} · el banco {'lo detecta' if ok else 'NO MUERDE'}")
    if not ok:
        fallos.append("el banco no detecta un estiron conocido")

    # 2 · LADO BUENO: el script actual sobre el mismo control NO debe deformar
    bueno = os.path.join(tmp, "bueno.webp")
    optimizar(ctrl, bueno, (1080, 1350), 150, "cover")
    r = relacion(bueno)
    ok = abs(1 - r) <= 0.02
    print(f"  {'✅' if ok else '❌'} 2 modo cover a 4:5               relacion={r:.3f} · esperado 1,000 ± 0,02")
    if not ok:
        fallos.append(f"cover deforma: relacion {r:.3f}")

    # 3 · contain tampoco deforma, y ademas conserva el circulo entero
    cont = os.path.join(tmp, "cont.webp")
    optimizar(ctrl, cont, (1080, 1920), 150, "contain")
    r = relacion(cont)
    ok = abs(1 - r) <= 0.02
    print(f"  {'✅' if ok else '❌'} 3 modo contain a 9:16            relacion={r:.3f} · esperado 1,000 ± 0,02")
    if not ok:
        fallos.append(f"contain deforma: relacion {r:.3f}")

    # 4 · el destino con nombre trae su medida Y su peso (galeria = 2048, no 1080)
    gal = os.path.join(tmp, "gal.webp")
    size, kb = parse_destino("galeria-shopify")
    _, final, _, peso = optimizar(ctrl, gal, size, kb, "cover")
    ok = final == (2048, 2048) and peso <= 300
    print(f"  {'✅' if ok else '❌'} 4 destino galeria-shopify        {final[0]}x{final[1]} · {peso:.0f} KB · esperado 2048x2048 ≤300 KB")
    if not ok:
        fallos.append(f"galeria-shopify dio {final} / {peso:.0f} KB")

    # 5 · LADO MALO del agrandado: 1K pedido a galeria (2048) debe DELATARSE
    inv = detalle_inventado((1024, 1024), (2048, 2048), "cover")
    ok = inv > 2
    print(f"  {'✅' if ok else '❌'} 5 caso MALO (1K -> galeria 2K)   agrandado={inv:.0f}% · el aviso {'salta' if ok else 'NO SALTA'}")
    if not ok:
        fallos.append("el agrandado silencioso de 1K a 2K no se detecta")

    # 6 · LADO BUENO del agrandado: un origen que ya es 2K NO debe dar aviso
    inv = detalle_inventado((2048, 2048), (2048, 2048), "cover")
    ok = inv <= 2
    print(f"  {'✅' if ok else '❌'} 6 caso BUENO (2K -> galeria 2K)  agrandado={inv:.0f}% · el aviso {'calla' if ok else 'ACUSA EN FALSO'}")
    if not ok:
        fallos.append("el aviso de agrandado acusa a un origen que ya venia en 2K")

    print()
    if fallos:
        print("❌ AUTOPRUEBA FALLIDA:")
        for f in fallos:
            print(f"   · {f}")
        return 1
    print("✅ autoprueba 6/6 · muerde los dos casos malos y calla ante los buenos")
    return 0


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())

    modo = "cover"
    argv = sys.argv[1:]
    if "--modo" in argv:
        i = argv.index("--modo")
        modo = argv[i + 1] if i + 1 < len(argv) else "cover"
        argv = argv[:i] + argv[i + 2:]
    if modo not in ("cover", "contain"):
        sys.exit(f"--modo debe ser cover o contain, no '{modo}'")

    if len(argv) < 2:
        sys.exit(__doc__)
    src, out = argv[0], argv[1]

    txt = argv[2] if len(argv) > 2 else "ficha-html"
    size, kb_destino = parse_destino(txt)
    max_kb = float(argv[3]) if len(argv) > 3 else (kb_destino if kb_destino else 150.0)

    origen, final, q, kb = optimizar(src, out, size, max_kb, modo)

    estado = "OK" if kb <= max_kb else "AVISO: no bajo del limite ni con quality=40"
    nota = ""
    if size and origen != final:
        ro, rf = origen[0] / origen[1], final[0] / final[1]
        if abs(ro - rf) > 0.01:
            nota = f" · {modo} (origen {origen[0]}x{origen[1]}, proporcion distinta: se {'recorto' if modo == 'cover' else 'relleno'}, NO se deformo)"
    print(f"{estado} {out} · quality={q} · {kb:.1f} KB · {final[0]}x{final[1]}{nota}")

    inventado = detalle_inventado(origen, size, modo)
    if inventado > 2:
        print(f"🔴 AGRANDADO {inventado:.0f}%: el origen era {origen[0]}x{origen[1]} y la salida dice "
              f"{final[0]}x{final[1]}. Ese detalle de mas NO lo genero el motor, lo invento el "
              f"redimensionado.")
        print("   El fichero dice 2K y el zoom sigue siendo de 1K: es el techo de nitidez con otro "
              "nombre. Regenera la pieza en 2K desde el motor (resolution 2k), no la agrandes aqui.")


if __name__ == "__main__":
    main()
