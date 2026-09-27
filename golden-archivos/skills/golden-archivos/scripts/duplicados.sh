#!/bin/bash
# duplicados.sh "<carpeta1>" ["<carpeta2>" ...]
# Encuentra duplicados EXACTOS (mismo contenido) sin leer todo el disco:
# primero agrupa por TAMAÑO (instantáneo, no abre archivos) y solo hashea
# los que colisionan. Sobre 10 GB esto baja de "se cuelga" a segundos.
set -u
[ "$#" -ge 1 ] || { echo "Uso: duplicados.sh \"<carpeta1>\" [\"<carpeta2>\" ...]" >&2; exit 1; }
# Un mktemp que falla (sandbox sin TMPDIR, disco lleno) deja la variable VACIA
# y "$VAR/x" se vuelve "/x". Medido 2026-09-27 con un mktemp falso: sin esta
# guarda esta herramienta salia con EXIT 0 sin hacer nada — el peor de los
# ceros falsos, porque quien la llama en un bucle ve exito y da el trabajo por
# hecho. Se aborta en vez de seguir.
SIZES=$(mktemp "${TMPDIR:-/tmp}/golden-archivos.XXXXXX") \
  && HASHES=$(mktemp "${TMPDIR:-/tmp}/golden-archivos.XXXXXX") || {
  echo "🔴 No se pudo crear el temporal: sin el, el conteo de duplicados saldria en CERO y ese cero seria mentira." >&2; exit 1; }
find "$@" -type f ! -name '.*' -size +0 2>/dev/null -exec stat -f '%z	%N' {} + > "$SIZES"
cut -f1 "$SIZES" | sort -n | uniq -d > "${SIZES}.dup"
while IFS= read -r s; do
  awk -F'\t' -v S="$s" '$1==S{print $2}' "$SIZES"
done < "${SIZES}.dup" | while IFS= read -r f; do
  printf '%s\t%s\n' "$(md5 -q "$f" 2>/dev/null)" "$f" >> "$HASHES"
done

echo "Archivos analizados: $(wc -l < "$SIZES" | tr -d ' ')"
cut -f1 "$HASHES" | sort | uniq -d > "${HASHES}.dup"
echo "Grupos de duplicados exactos: $(wc -l < "${HASHES}.dup" | tr -d ' ')"
echo ""
i=0
while IFS= read -r h; do
  i=$((i+1)); echo "-- Grupo $i --"
  grep "^$h	" "$HASHES" | cut -f2 | sed 's/^/   /'
  echo ""
done < "${HASHES}.dup"
rm -f "$SIZES" "${SIZES}.dup" "${HASHES}.dup"   # se conserva solo el TSV de hashes
echo "TSV completo de hashes: $HASHES"
