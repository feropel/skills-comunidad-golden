#!/bin/bash
# duplicados.sh "<carpeta1>" ["<carpeta2>" ...]
# Encuentra duplicados EXACTOS (mismo contenido) sin leer todo el disco:
# primero agrupa por TAMAÑO (instantáneo, no abre archivos) y solo hashea
# los que colisionan. Sobre 10 GB esto baja de "se cuelga" a segundos.
set -u
[ "$#" -ge 1 ] || { echo "Uso: duplicados.sh \"<carpeta1>\" [\"<carpeta2>\" ...]" >&2; exit 1; }
SIZES=$(mktemp); HASHES=$(mktemp)
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
