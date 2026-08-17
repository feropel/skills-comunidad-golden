#!/usr/bin/env python3
"""
quitar-fondo.py — recorta el fondo de imágenes de producto EN LOCAL, sin gastar créditos.

Por qué existe: `remove_background` del MCP cuesta créditos por imagen. Este script hace lo
mismo con rembg (MIT, corre en tu máquina) y en un catálogo de decenas de packshots la
diferencia es real. Medido el 2026-08-02 con un packshot 1080x1080 de Golden:
**0,86 s por imagen** tras cargar el modelo, y el recorte resolvió bien el caso difícil
(tapa blanca sobre fondo blanco) sin halos ni bordes duros.

INSTALACIÓN (una sola vez, en entorno aislado para no tocar el Python del sistema):
    python3 -m venv ~/.golden-rembg
    ~/.golden-rembg/bin/pip install "rembg[cpu]"
La primera ejecución descarga el modelo u2net (~176 MB) a ~/.u2net/ y queda cacheado.
Esa descarga es la ÚNICA salida a internet: después funciona sin conexión.

USO:
    ~/.golden-rembg/bin/python quitar-fondo.py <entrada> [salida] [--fondo RRGGBB]

    <entrada>  archivo o CARPETA (procesa .jpg .jpeg .png .webp)
    [salida]   carpeta destino (por defecto: <entrada>/sin-fondo)
    --fondo    compone sobre un color sólido en vez de dejar transparencia
               (útil para ver halos: --fondo 5E1A2C es el vino Golden)

SALIDA: PNG con canal alfa. Para la web, pásalo después por optimizar-webp.py.
"""
import os
import sys
import time

MIN_ALFA = 8          # por debajo de esto se considera transparente
MAX_ALFA = 247        # por encima, opaco
EXTS = (".jpg", ".jpeg", ".png", ".webp")


def fatal(msg):
    print(f"❌ {msg}")
    sys.exit(1)


try:
    from PIL import Image
    from rembg import remove, new_session
except ImportError:
    fatal("falta rembg. Instálalo con:\n"
          "   python3 -m venv ~/.golden-rembg\n"
          '   ~/.golden-rembg/bin/pip install "rembg[cpu]"\n'
          "   y corre este script con ~/.golden-rembg/bin/python")


def revisar(img):
    """Mide el recorte. Un borde semitransparente entre 0,5% y 5% indica antialiasing sano;
    0% suele ser recorte de tijera y se ve pegado en la página."""
    # histogram() en vez de getdata(): getdata está deprecado y desaparece en Pillow 14
    # (oct 2027). histogram devuelve los 256 niveles de alfa contados, es estable y más rápido.
    h = img.split()[-1].histogram()
    n = sum(h) or 1
    transp = sum(h[:MIN_ALFA])
    opac = sum(h[MAX_ALFA + 1:])
    borde = n - transp - opac
    return transp / n * 100, opac / n * 100, borde / n * 100


def procesar(ruta_in, ruta_out, sesion, fondo_hex=None):
    src = Image.open(ruta_in)
    if src.mode not in ("RGB", "RGBA"):
        src = src.convert("RGB")
    t0 = time.time()
    out = remove(src, session=sesion)
    dt = time.time() - t0

    t, o, b = revisar(out)

    if fondo_hex:
        rgb = tuple(int(fondo_hex[i:i + 2], 16) for i in (0, 2, 4))
        base = Image.new("RGBA", out.size, rgb + (255,))
        base.alpha_composite(out)
        out = base

    out.save(ruta_out)
    kb = os.path.getsize(ruta_out) / 1024
    aviso = ""
    if b < 0.3:
        aviso = "  ⚠️ borde duro, revísalo a ojo"
    elif t < 5:
        aviso = "  ⚠️ recortó casi nada, quizá el fondo no se detectó"
    print(f"  ✅ {os.path.basename(ruta_out):<38} {dt:>5.2f}s · {kb:>6.0f} KB · "
          f"transp {t:.0f}% · borde {b:.1f}%{aviso}")
    return dt


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fondo = None
    for a in sys.argv[1:]:
        if a.startswith("--fondo"):
            fondo = a.split("=", 1)[1] if "=" in a else None
    if fondo is None and "--fondo" in sys.argv:
        i = sys.argv.index("--fondo")
        if i + 1 < len(sys.argv):
            fondo = sys.argv[i + 1]
            args = [a for a in args if a != fondo]

    if not args:
        print(__doc__)
        sys.exit(0)

    entrada = os.path.abspath(os.path.expanduser(args[0]))
    if not os.path.exists(entrada):
        fatal(f"no existe: {entrada}")

    if os.path.isdir(entrada):
        archivos = sorted(
            os.path.join(entrada, f) for f in os.listdir(entrada)
            if f.lower().endswith(EXTS) and not f.startswith(".")
        )
        destino = os.path.abspath(os.path.expanduser(args[1])) if len(args) > 1 \
            else os.path.join(entrada, "sin-fondo")
    else:
        archivos = [entrada]
        destino = os.path.abspath(os.path.expanduser(args[1])) if len(args) > 1 \
            else os.path.dirname(entrada)

    if not archivos:
        fatal(f"no hay imágenes {'/'.join(EXTS)} en {entrada}")
    os.makedirs(destino, exist_ok=True)

    print(f"🖼️  {len(archivos)} imagen(es) · destino: {destino}")
    print("   cargando modelo (la 1a vez descarga ~176 MB, luego es instantáneo)...")
    sesion = new_session("u2net")

    total = 0.0
    for f in archivos:
        base = os.path.splitext(os.path.basename(f))[0]
        salida = os.path.join(destino, f"{base}-sin-fondo.png")
        try:
            total += procesar(f, salida, sesion, fondo)
        except Exception as e:
            print(f"  ❌ {os.path.basename(f)}: {e}")

    if archivos:
        print(f"\n⏱️  {total:.1f}s en total · {total/len(archivos):.2f}s por imagen · "
              f"0 créditos gastados")
        print("   siguiente paso: optimizar-webp.py para dejarlas < 150 KB")


if __name__ == "__main__":
    main()
