#!/usr/bin/env python3
"""
ETIQUETA DESDE VIDEO / FOTO — Golden Group

POR QUE EXISTE (incidente real, 2026-09-05, suplemento COD):
Se publico una ficha con CINCO ingredientes falsos y un ALERGENO sin declarar (nuez negra),
porque los ingredientes se copiaron de la pagina de un COMPETIDOR que vendia otra formulacion
con el mismo nombre comercial. La fuente buena llevaba DIAS dentro del material del cliente:
estaba impresa en la etiqueta del frasco, legible ampliando un fotograma de un video del
proveedor. Nadie amplio el fotograma.

Leccion convertida en herramienta: AMPLIAR EL ENVASE ES UN PASO DE LA INVESTIGACION, no un
extra. Este script hace ese paso mecanico para que no dependa de que alguien se acuerde.

QUE HACE
  video -> extrae N fotogramas repartidos por toda la duracion
  foto  -> la toma tal cual
  luego: recorta opcionalmente, AMPLIA (x2..x8 con Lanczos) y guarda PNG sin perdida,
  listos para LEERLOS CON LOS OJOS del modelo (Read sobre el PNG).

QUE NO HACE (declarado, no simulado)
  NO hace OCR ni "entiende" la etiqueta. Entrega imagenes legibles; leerlas es del modelo.
  Si el envase esta borroso en el original, ampliar NO inventa nitidez: se declara ilegible.

USO
  python3 etiqueta_desde_video.py <video|imagen> [--n 12] [--zoom 4] [--out DIR]
  python3 etiqueta_desde_video.py frasco.mp4 --n 16 --zoom 6
  python3 etiqueta_desde_video.py foto.jpg --crop 0.25,0.10,0.75,0.90   # x0,y0,x1,y1 (0..1)

DESPUES DE CORRER: abrir los PNG con Read y transcribir LITERAL. Lo que no se lea = [ILEGIBLE],
se pide otra foto. Jamas se completa por parecido (REGLA 1) ni con la pagina de un competidor.

Requisitos: ffmpeg/ffprobe (video) y Pillow (ampliado). Ambos se verifican al arrancar.
Manual: ../references/00-identificacion-forense.md
"""

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".avi", ".mkv", ".mpg", ".mpeg"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".bmp", ".tif", ".tiff"}


def falta(binario):
    return shutil.which(binario) is None


def duracion(ruta):
    """Segundos de un video. None si ffprobe no puede decirlo (no se inventa)."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", ruta],
        capture_output=True, text=True)
    try:
        d = float(r.stdout.strip())
        return d if d > 0 else None
    except (ValueError, TypeError):
        return None


def extraer_fotogramas(video, out, n):
    """N fotogramas repartidos por toda la duracion. Devuelve rutas creadas."""
    d = duracion(video)
    if d is None:
        print("  ffprobe no pudo leer la duracion: se extrae 1 fotograma del inicio.")
        marcas = [0.0]
    else:
        # se evitan los extremos exactos (suelen ser negro/transicion)
        marcas = [d * (i + 0.5) / n for i in range(n)]
    hechos = []
    for i, t in enumerate(marcas, 1):
        dest = os.path.join(out, f"frame_{i:02d}_{t:07.2f}s.png")
        r = subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", video,
             "-frames:v", "1", "-y", dest],
            capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0:
            hechos.append(dest)
        elif r.stderr.strip():
            print(f"  aviso en {t:.2f}s: {r.stderr.strip().splitlines()[0][:70]}")
    return hechos


def ampliar(rutas, zoom, crop, out):
    """Recorta (opcional) y amplia con Lanczos. Devuelve [(ruta, wxh), ...]."""
    from PIL import Image
    salidas = []
    for r in rutas:
        try:
            im = Image.open(r).convert("RGB")
        except Exception as e:                                  # imagen ilegible
            print(f"  no se pudo abrir {os.path.basename(r)}: {e}")
            continue
        if crop:
            x0, y0, x1, y1 = crop
            w, h = im.size
            caja = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
            if caja[2] > caja[0] and caja[3] > caja[1]:
                im = im.crop(caja)
        im = im.resize((im.width * zoom, im.height * zoom), Image.LANCZOS)
        dest = os.path.join(out, "ZOOM_" + os.path.splitext(os.path.basename(r))[0] + ".png")
        im.save(dest, "PNG")
        salidas.append((dest, f"{im.width}x{im.height}"))
    return salidas


def par_crop(txt):
    try:
        v = [float(x) for x in txt.split(",")]
        if len(v) != 4 or not all(0.0 <= x <= 1.0 for x in v):
            raise ValueError
        if v[0] >= v[2] or v[1] >= v[3]:
            raise ValueError
        return tuple(v)
    except ValueError:
        raise argparse.ArgumentTypeError("--crop pide x0,y0,x1,y1 entre 0 y 1, con x0<x1 y y0<y1")


def main():
    p = argparse.ArgumentParser(description="Fotogramas ampliados para LEER la etiqueta del envase.")
    p.add_argument("fuente", help="video o imagen del producto (material del cliente)")
    p.add_argument("--n", type=int, default=12, help="fotogramas a extraer si es video (def. 12)")
    p.add_argument("--zoom", type=int, default=4, choices=range(2, 9), metavar="2-8",
                   help="factor de ampliado (def. 4)")
    p.add_argument("--crop", type=par_crop, default=None,
                   help="recorte relativo x0,y0,x1,y1 (0..1) para aislar la etiqueta")
    p.add_argument("--out", default=None, help="carpeta destino (def. <fuente>_etiqueta/)")
    a = p.parse_args()

    if not os.path.exists(a.fuente):
        print(f"No existe: {a.fuente}")
        return 2

    ext = os.path.splitext(a.fuente)[1].lower()
    es_video = ext in VIDEO_EXT
    if not es_video and ext not in IMG_EXT:
        print(f"Extension no reconocida ({ext}). Video: {sorted(VIDEO_EXT)} · Imagen: {sorted(IMG_EXT)}")
        return 2

    if importlib.util.find_spec("PIL") is None:
        print("Falta Pillow (pip3 install Pillow). Sin el no se puede ampliar.")
        return 2
    if es_video and (falta("ffmpeg") or falta("ffprobe")):
        print("Falta ffmpeg/ffprobe (brew install ffmpeg). Sin ellos no se extraen fotogramas.")
        return 2

    out = a.out or os.path.splitext(a.fuente)[0] + "_etiqueta"
    os.makedirs(out, exist_ok=True)

    print("=" * 68)
    print("  ETIQUETA DESDE VIDEO/FOTO — la fuente de la ficha es el ENVASE")
    print("=" * 68)

    if es_video:
        print(f"  Video: {os.path.basename(a.fuente)} · extrayendo {a.n} fotogramas...")
        base = extraer_fotogramas(a.fuente, out, a.n)
        if not base:
            print("  NO se extrajo ningun fotograma. El video puede estar corrupto.")
            return 1
        print(f"  {len(base)} fotogramas extraidos.")
    else:
        base = [a.fuente]
        print(f"  Imagen: {os.path.basename(a.fuente)}")

    print(f"  Ampliando x{a.zoom}" + (f" con recorte {a.crop}" if a.crop else "") + "...")
    zooms = ampliar(base, a.zoom, a.crop, out)
    if not zooms:
        print("  NO se genero ninguna ampliacion.")
        return 1

    print("-" * 68)
    for r, wh in zooms:
        print(f"  [{wh:>12}]  {r}")
    print("-" * 68)
    print(f"  {len(zooms)} imagen(es) listas en: {out}")
    print()
    print("  AHORA, y esto es lo que faltaba el dia del incidente:")
    print("   1. ABRE cada PNG con Read y busca el panel de INGREDIENTES del envase.")
    print("   2. Transcribe LITERAL: ingredientes, contenido neto, modo de uso, registro.")
    print("   3. Copia TAL CUAL toda advertencia de ALERGENO ('contains', 'contiene',")
    print("      'elaborado en instalaciones que...'). Es lo unico de una ficha que puede")
    print("      hacerle dano fisico a una persona: se publica SIEMPRE.")
    print("   4. Lo que no se lea = [ILEGIBLE] y se pide otra foto de ese lado.")
    print("      Ampliar no inventa nitidez, y la pagina de un competidor NO es la fuente:")
    print("      dos tiendas venden el mismo nombre con formulas distintas.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
