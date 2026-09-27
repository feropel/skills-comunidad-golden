#!/bin/bash
# nombrar.sh "<carpeta-unidad>" "<movimientos.log>" [DRY]
# Antepone el nombre del producto (el de la carpeta-unidad) a cada creativo/
# documento: "VIDEO 8.mov" -> "<PRODUCTO> - VIDEO 8.mov". Conserva el nombre
# original (los huecos de numeración son información). Solo toca creativos y
# documentos (lista ALLOW); nunca código ni configuración.
# Con tercer argumento DRY solo imprime lo que haría, sin mover nada.
# El log es OBLIGATORIO (salvo en DRY) y se verifica escribible ANTES de mover:
# un renombrado sin registro no se puede deshacer.
set -u
UNIT="${1:?Uso: nombrar.sh \"<carpeta-unidad>\" \"<movimientos.log>\" [DRY]}"
LOG="${2:-}"
DRY="${3:-}"
# Normaliza la ruta: quita las barras finales. `for U in "$R"/*/` — la forma
# canonica de recorrer productos — SIEMPRE entrega barra final, y sin esto
# "$UNIT/archivo" no se puede recortar contra "$UNIT", asi que el script
# devolvia 0 SIN error (medido 2026-09-05: 1 pieza sin barra, 0 con barra).
while [ "$UNIT" != "/" ] && [ "${UNIT%/}" != "$UNIT" ]; do UNIT="${UNIT%/}"; done
[ -d "$UNIT" ] || exit 0
. "$(dirname "$0")/_comun.sh"
exigir_local "$UNIT" "Renombrar archivos"
if [ "$DRY" != "DRY" ]; then
  [ -n "$LOG" ] || { echo "🔴 Falta el log. Uso: nombrar.sh \"<carpeta>\" \"<log>\" [DRY]" >&2; exit 1; }
  mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] || { echo "🔴 Log no escribible: $LOG — no se renombra nada" >&2; exit 1; }
fi
raw="$(basename "$UNIT")"
PREFIX="$(printf '%s' "$raw" | sed 's/™//g; s/®//g; s/ - / /g; s/  */ /g' | sed 's/^ *//; s/ *$//')"
ALLOW="jpg jpeg png webp heic heif gif tiff tif bmp svg psd ai eps mp4 mov webm m4v avi mkv hevc pdf docx doc rtf txt md xlsx xls csv tsv numbers pptx ppt key pages zip rar 7z"
# Un mktemp que falla (sandbox sin TMPDIR, disco lleno) deja la variable VACIA
# y "$VAR/x" se vuelve "/x". Medido 2026-09-27 con un mktemp falso: sin esta
# guarda esta herramienta salia con EXIT 0 sin hacer nada — el peor de los
# ceros falsos, porque quien la llama en un bucle ve exito y da el trabajo por
# hecho. Se aborta en vez de seguir.
TMP="$(mktemp "${TMPDIR:-/tmp}/golden-archivos.XXXXXX")" || {
  echo "🔴 No se pudo crear el temporal: no se renombra nada." >&2; exit 1; }
find "$UNIT" -type f ! -name '.*' 2>/dev/null > "$TMP"   # snapshot PRIMERO (renombrar mientras find recorre salta archivos)
while IFS= read -r f; do
  [ -f "$f" ] || continue
  b="$(basename "$f")"; dir="$(dirname "$f")"
  ext="$(printf '%s' "${b##*.}" | tr '[:upper:]' '[:lower:]')"
  case " $ALLOW " in *" $ext "*) : ;; *) continue;; esac
  case "$b" in "$PREFIX - "*) continue;; esac
  dest="$dir/$PREFIX - $b"
  if [ -e "$dest" ]; then
    name="${b%.*}"; e2="${b##*.}"; [ "$name" = "$e2" ] && e2=""
    n=1; while [ -e "$dir/$PREFIX - ${name} (${n})${e2:+.$e2}" ]; do n=$((n+1)); done
    dest="$dir/$PREFIX - ${name} (${n})${e2:+.$e2}"
  fi
  if [ "$DRY" = "DRY" ]; then echo "$b -> $(basename "$dest")"; else
    mv "$f" "$dest" && printf 'MV\t%s\t%s\n' "$f" "$dest" >> "$LOG"
  fi
done < "$TMP"
rm -f "$TMP"
