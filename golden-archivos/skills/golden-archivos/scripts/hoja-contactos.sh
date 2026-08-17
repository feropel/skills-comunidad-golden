#!/bin/bash
# hoja-contactos.sh "<carpeta>" "<salida.png>" [columnas] [filas]
# Arma una hoja de contactos (mosaico) para poder VER de un vistazo qué hay
# dentro de una carpeta: fotos, GIFs y videos (toma un fotograma de cada uno).
# Sirve para identificar archivos con nombre críptico y para comparar candidatos
# a duplicado antes de borrar nada.
#
# Detalles que cuestan tiempo si no se saben:
#  - format=rgb24 es obligatorio: si mezclas PNG con alfa (RGBA) y JPG (RGB),
#    el filtro tile falla y devuelve un mosaico vacío.
#  - NO usar drawtext para numerar: en muchos ffmpeg de macOS no hay fuente
#    configurada y el filtro entero se cae en silencio. Se imprime el índice
#    por consola y así se mapea número -> nombre.
#  - -start_number 1 porque el patrón %03d empieza a buscar en 0.
#  - Si no pasas filas, se calculan solas para que TODAS las piezas entren en
#    el mosaico: un mosaico corto que calla piezas invalida la verificación visual.
set -u
DIR="${1:?carpeta}"; OUT="${2:?salida.png}"; COLS="${3:-5}"; ROWS="${4:-}"
command -v ffmpeg >/dev/null 2>&1 || { echo "🔴 Falta ffmpeg (instalar: brew install ffmpeg). Sin mosaico, verifica abriendo los archivos uno a uno con Read." >&2; exit 1; }
S=230
WORK=$(mktemp -d)
i=1
while IFS= read -r f; do
  ffmpeg -y -loglevel error -i "$f" \
    -vf "scale=$S:$S:force_original_aspect_ratio=decrease,pad=$S:$S:(ow-iw)/2:(oh-ih)/2:white,format=rgb24" \
    -frames:v 1 "$WORK/$(printf '%03d' $i).png" 2>/dev/null
  if [ -f "$WORK/$(printf '%03d' $i).png" ]; then
    echo "$i = $(basename "$f")"
    i=$((i+1))
  else
    echo "   (no se pudo leer: $(basename "$f"))" >&2
  fi
done < <(find "$DIR" -maxdepth 1 -type f ! -name '.*' \
          \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \
             -o -iname '*.gif' -o -iname '*.heic' -o -iname '*.mp4' -o -iname '*.mov' \) | sort)

n=$((i-1))
[ "$n" -eq 0 ] && { echo "Sin imágenes legibles en $DIR"; rm -rf "$WORK"; exit 1; }
# Filas automáticas: que quepan TODAS las piezas
[ -z "$ROWS" ] && ROWS=$(( (n + COLS - 1) / COLS ))
if [ "$n" -gt $((COLS * ROWS)) ]; then
  echo "⚠️ $n piezas no caben en ${COLS}x${ROWS} ($((COLS*ROWS)) celdas): el mosaico quedará INCOMPLETO. Sube filas/columnas o corre por tandas." >&2
fi
# Tope de alto: un mosaico gigantesco se vuelve ilegible al mirarlo y pesa de más,
# así que la verificación visual se hace por tandas en vez de en una sola lámina.
MAX_ROWS=8
if [ "$ROWS" -gt "$MAX_ROWS" ]; then
  echo "⚠️ $n piezas → ${ROWS} filas: demasiado alto para revisar de un vistazo." >&2
  echo "   Corre por tandas (ej. subcarpetas) o sube columnas: hoja-contactos.sh \"\$DIR\" salida.png $(( (n + MAX_ROWS - 1) / MAX_ROWS ))" >&2
fi
(cd "$WORK" && ffmpeg -y -loglevel error -framerate 1 -start_number 1 -i "%03d.png" \
  -filter_complex "tile=${COLS}x${ROWS}:padding=6:color=gray" -frames:v 1 "$OUT")
rm -rf "$WORK"
echo ""
echo "Hoja de contactos ($n piezas): $OUT"
