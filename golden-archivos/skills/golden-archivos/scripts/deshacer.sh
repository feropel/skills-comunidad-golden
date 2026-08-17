#!/bin/bash
# deshacer.sh "<log>" — revierte TODOS los movimientos del log, en orden inverso.
# Portable macOS: tac no existe en Darwin; se usa tail -r (y tac si está, en Linux).
# Nunca sobrescribe (mv -n): si el origen ya está ocupado, lo reporta y sigue.
set -u
LOG="${1:?Uso: deshacer.sh \"<movimientos.log>\"}"
[ -f "$LOG" ] || { echo "No hay log: $LOG"; exit 1; }

reverse() { if command -v tac >/dev/null 2>&1; then tac "$1"; else tail -r "$1"; fi; }

OK=0; FALTA=0; OCUPADO=0
while IFS=$'\t' read -r op src dest; do
  [ "$op" = "MV" ] || continue
  if [ ! -e "$dest" ]; then
    echo "⚠️ no existe (ya movido o borrado): $dest" >&2; FALTA=$((FALTA+1)); continue
  fi
  mkdir -p "$(dirname "$src")"
  if [ -e "$src" ]; then
    echo "⚠️ origen ocupado, NO se sobrescribe: $src" >&2; OCUPADO=$((OCUPADO+1)); continue
  fi
  mv -n "$dest" "$src" && { echo "revertido: $dest -> $src"; OK=$((OK+1)); }
done < <(reverse "$LOG")

# Limpiar las carpetas que quedaron vacías al devolver los archivos:
# si no, revertir deja el esqueleto de la clasificación y el usuario cree que falló.
# Se repite hasta que no borre nada, para vaciar también los niveles superiores.
VAC=0
while :; do
  antes=$VAC
  while IFS= read -r d; do
    rmdir "$d" 2>/dev/null && VAC=$((VAC+1))
  done < <(awk -F'\t' '$1=="MV"{print $3}' "$LOG" | while IFS= read -r p; do dirname "$p"; done | sort -u)
  [ "$VAC" -eq "$antes" ] && break
done

echo ""
echo "Revertidos: $OK · No encontrados: $FALTA · Origen ocupado (sin tocar): $OCUPADO · Carpetas vacías eliminadas: $VAC"
