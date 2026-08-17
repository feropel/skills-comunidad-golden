#!/bin/bash
# clasificar.sh "<carpeta>" "<movimientos.log>"
# Clasifica SOLO los archivos sueltos que están directamente en <carpeta>
# (no entra en subcarpetas existentes) moviéndolos a subcarpetas por tipo.
# El log es OBLIGATORIO y se verifica escribible ANTES del primer movimiento:
# un archivo movido sin registro es un archivo que ya no se puede deshacer.
set -u
DIR="${1:?Uso: clasificar.sh \"<carpeta>\" \"<movimientos.log>\"}"
LOG="${2:?Falta el log. Uso: clasificar.sh \"<carpeta>\" \"<movimientos.log>\"}"
[ -d "$DIR" ] || { echo "  (no existe: $DIR)"; exit 0; }
# El log debe poder escribirse ANTES de mover nada
mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] || { echo "🔴 Log no escribible: $LOG — no se mueve nada" >&2; exit 1; }

move() { # move <src> <subfolder>
  local src="$1" sub="$2"
  local base="$(basename "$src")"
  local destdir="$DIR/$sub"
  mkdir -p "$destdir"
  local dest="$destdir/$base"
  # evitar colisiones
  if [ -e "$dest" ]; then
    local n=1 name="${base%.*}" ext="${base##*.}"
    [ "$name" = "$ext" ] && ext=""
    while [ -e "$destdir/${name} (${n})${ext:+.$ext}" ]; do n=$((n+1)); done
    dest="$destdir/${name} (${n})${ext:+.$ext}"
  fi
  mv "$src" "$dest"
  printf 'MV\t%s\t%s\n' "$src" "$dest" >> "$LOG"
}

shopt -s nullglob
for f in "$DIR"/*; do
  [ -f "$f" ] || continue          # saltar subcarpetas
  b="$(basename "$f")"
  case "$b" in .*|Icon$'\r') continue;; esac   # saltar ocultos
  lc="$(echo "$b" | tr '[:upper:]' '[:lower:]')"
  ext="${lc##*.}"
  # LOGOS por nombre
  if echo "$lc" | grep -Eq 'logo|marca|isotipo|imagotipo|brand'; then
    case "$ext" in png|jpg|jpeg|webp|svg|ai|psd|pdf|eps) move "$f" "LOGOS Y MARCA"; continue;; esac
  fi
  case "$ext" in
    mp4|mov|webm|m4v|avi|mkv|hevc)          move "$f" "VIDEOS";;
    gif)                                     move "$f" "GIFS";;
    jpg|jpeg|png|webp|heic|heif|tiff|tif|bmp|svg|psd|ai|eps) move "$f" "IMÁGENES";;
    xlsx|xls|csv|numbers|tsv)                move "$f" "DATOS Y EXCEL";;
    pdf|docx|doc|txt|md|rtf|pptx|ppt|key|pages) move "$f" "DOCUMENTOS";;
    zip|rar|7z)                              move "$f" "DATOS Y EXCEL";;
    *)                                       move "$f" "OTROS";;
  esac
done
