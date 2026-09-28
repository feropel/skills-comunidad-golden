#!/usr/bin/env bash
# extract_frames.sh — Extrae fotogramas de un video para el teardown (golden-video-teardown).
# Genera 3 recursos legibles: hook strip (primeros 4s), filmstrip denso (1 frame/1.5s) y specs.
#
# Uso:
#   bash extract_frames.sh "/ruta/al/Video.mov" "/ruta/salida"
#   (si no das salida, usa ./frames_teardown)
#
# Requiere ffmpeg + ffprobe.

set -u
VID="${1:?Falta la ruta del video}"
OUT="${2:-./frames_teardown}"
mkdir -p "$OUT"

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "❌ Falta ffmpeg/ffprobe. Instálalo: brew install ffmpeg"
  exit 1
fi
if [ ! -f "$VID" ]; then
  echo "❌ No existe el video: $VID"
  exit 1
fi

base="$(basename "$VID")"
name="${base%.*}"
# sanea el nombre para el archivo de salida
safe="$(echo "$name" | tr ' /' '__' | tr -cd '[:alnum:]_-')"

dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")"
res="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$VID")"
aud="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$VID" 2>/dev/null)"
echo "🎬 $base"
echo "   duración: ${dur}s · resolución: ${res} · audio: ${aud:-ninguno}"

# 1) Hook strip — primeros 4s, 1 frame cada 0.5s (8 en fila) → lee el gancho al detalle
ffmpeg -y -loglevel error -ss 0 -t 4 -i "$VID" \
  -vf "fps=2,scale=270:480,tile=8x1" -frames:v 1 "$OUT/hook_${safe}.png" \
  && echo "   ✅ hook_${safe}.png (gancho 0-4s)"

# 2) Filmstrip denso — 1 frame cada 1.5s, tile 4 columnas → cubre todo el video, captions legibles
fps="$(awk -v d="$dur" 'BEGIN{ if (d>0) printf "%.4f", 1/1.5; else print "0.6667"}')"
cols=4
frames="$(awk -v d="$dur" 'BEGIN{ n=int(d/1.5)+1; if(n<4)n=4; print n}')"
rows="$(awk -v f="$frames" -v c="$cols" 'BEGIN{ r=int((f+c-1)/c); print r}')"
ffmpeg -y -loglevel error -i "$VID" \
  -vf "fps=${fps},scale=260:462,tile=${cols}x${rows}" -frames:v 1 "$OUT/dense_${safe}.png" \
  && echo "   ✅ dense_${safe}.png (${frames} frames, 1 cada 1.5s)"

echo "   → Lee esos PNG con la tool Read para transcribir texto en pantalla + visuales beat por beat."
