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
# Normaliza la ruta: quita las barras finales. `for U in "$R"/*/` — la forma
# canonica de recorrer productos — SIEMPRE entrega barra final, y sin esto
# "$DIR/archivo" no se puede recortar contra "$DIR", asi que el script
# devolvia 0 SIN error (medido 2026-09-05: 1 pieza sin barra, 0 con barra).
while [ "$DIR" != "/" ] && [ "${DIR%/}" != "$DIR" ]; do DIR="${DIR%/}"; done
command -v ffmpeg >/dev/null 2>&1 || { echo "🔴 Falta ffmpeg (instalar: brew install ffmpeg). Sin mosaico: las imagenes y los PDF se miran uno a uno con Read; los VIDEOS no los abre Read, sacales un fotograma con 'qlmanage -t -s 400 -o <salida> \"<video>\"' y mira ese PNG. Lo que aun asi no se vea, no se clasifica por el nombre." >&2; exit 1; }
S=230
# Un mktemp que falla (sandbox sin TMPDIR, disco lleno) deja la variable VACIA
# y "$VAR/x" se vuelve "/x". Medido 2026-09-27 con un mktemp falso: sin esta
# guarda esta herramienta salia con EXIT 0 sin hacer nada — el peor de los
# ceros falsos, porque quien la llama en un bucle ve exito y da el trabajo por
# hecho. Se aborta en vez de seguir.
WORK=$(mktemp -d "${TMPDIR:-/tmp}/golden-archivos.XXXXXX") || {
  echo "🔴 No se pudo crear el temporal: no se puede armar el mosaico." >&2; exit 1; }

# La lista debe cubrir TODO lo que clasificar.sh manda a IMÁGENES/GIFS/VIDEOS.
# Si un formato falta aquí, su archivo no se intenta siquiera: no sale en el
# mosaico NI en la línea "no se pudo leer" — desaparece en silencio, y un mosaico
# que calla piezas invalida la verificación visual (que es el corazón de la fase 6).
MEDIA_EXTS="jpg jpeg png webp gif heic heif tiff tif bmp svg psd ai eps mp4 mov webm m4v avi mkv hevc"
ARGS=(); primero=1
for e in $MEDIA_EXTS; do
  [ $primero -eq 1 ] && primero=0 || ARGS+=(-o)
  ARGS+=(-iname "*.$e")
done
CANDIDATOS=()
while IFS= read -r c; do CANDIDATOS+=("$c"); done < <(
  find "$DIR" -maxdepth 1 -type f ! -name '.*' \( "${ARGS[@]}" \) 2>/dev/null | sort)
TOTAL_ARCHIVOS=$(find "$DIR" -maxdepth 1 -type f ! -name '.*' 2>/dev/null | wc -l | tr -d ' ')
NO_MEDIA=$(( TOTAL_ARCHIVOS - ${#CANDIDATOS[@]} ))
i=1
while IFS= read -r f; do
  # `-nostdin` NO es adorno: sin el, ffmpeg DRENA la entrada estandar, que aqui
  # es la lista de archivos del propio bucle, y se come lineas. Medido el
  # 27-09-2026 sobre una biblioteca real: 85 renderizadas de 92 candidatas, sin
  # un solo error. Las piezas comidas no se clasifican y nadie sabe cuales son.
  #
  # Y el escalado va en DOS PASOS cuando el directo falla. Un HEIC es una imagen
  # en MOSAICOS: ffmpeg le arma por dentro un filtergraph complejo y un `-vf`
  # simple choca con el ("Simple and complex filtering cannot be used together
  # for the same stream"). Se decodifica primero y se escala despues.
  # El camino directo se intenta igual porque es mas rapido y sirve para todo lo
  # demas; el segundo paso solo corre si el primero no produjo nada.
  destino="$WORK/$(printf '%03d' $i).png"
  ffmpeg -nostdin -y -loglevel error -i "$f" \
    -vf "scale=$S:$S:force_original_aspect_ratio=decrease,pad=$S:$S:(ow-iw)/2:(oh-ih)/2:white,format=rgb24" \
    -frames:v 1 "$destino" 2>/dev/null
  if [ ! -s "$destino" ]; then
    TMPCRUDO="$WORK/crudo-$(printf '%03d' $i).png"
    ffmpeg -nostdin -y -loglevel error -i "$f" -frames:v 1 "$TMPCRUDO" 2>/dev/null
    if [ -s "$TMPCRUDO" ]; then
      ffmpeg -nostdin -y -loglevel error -i "$TMPCRUDO" \
        -vf "scale=$S:$S:force_original_aspect_ratio=decrease,pad=$S:$S:(ow-iw)/2:(oh-ih)/2:white,format=rgb24" \
        -frames:v 1 "$destino" 2>/dev/null
    fi
    rm -f "$TMPCRUDO"
  fi
  if [ -f "$WORK/$(printf '%03d' $i).png" ]; then
    echo "$i = $(basename "$f")"
    i=$((i+1))
  else
    echo "   (no se pudo leer: $(basename "$f"))" >&2
  fi
done < <(printf '%s\n' "${CANDIDATOS[@]}")

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
(cd "$WORK" && ffmpeg -nostdin -y -loglevel error -framerate 1 -start_number 1 -i "%03d.png" \
  -filter_complex "tile=${COLS}x${ROWS}:padding=6:color=gray" -frames:v 1 "$OUT")
rm -rf "$WORK"
echo ""
echo "Hoja de contactos: $n de ${#CANDIDATOS[@]} piezas renderizadas → $OUT"
if [ "$n" -lt "${#CANDIDATOS[@]}" ]; then
  echo "⚠️ $(( ${#CANDIDATOS[@]} - n )) no se pudieron renderizar (ver líneas anteriores): el mosaico está INCOMPLETO, verifícalas con Read." >&2
fi
if [ "$NO_MEDIA" -gt 0 ]; then
  echo "ℹ️ $NO_MEDIA archivo(s) de la carpeta no son media (docs, datos) y no entran al mosaico." >&2
fi
