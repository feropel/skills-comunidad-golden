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
[ -d "$UNIT" ] || exit 0
if [ "$DRY" != "DRY" ]; then
  [ -n "$LOG" ] || { echo "🔴 Falta el log. Uso: nombrar.sh \"<carpeta>\" \"<log>\" [DRY]" >&2; exit 1; }
  mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] || { echo "🔴 Log no escribible: $LOG — no se renombra nada" >&2; exit 1; }
fi
raw="$(basename "$UNIT")"
PREFIX="$(printf '%s' "$raw" | sed 's/™//g; s/®//g; s/ - / /g; s/  */ /g' | sed 's/^ *//; s/ *$//')"
ALLOW="jpg jpeg png webp heic heif gif mp4 mov webm m4v avi pdf docx doc xlsx xls csv pptx"
TMP="$(mktemp)"
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
