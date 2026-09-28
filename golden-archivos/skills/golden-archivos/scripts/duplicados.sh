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
  h=$(md5 -q "$f" 2>/dev/null)
  # Un md5 que falla devuelve VACIO, y todos los vacios se agrupan entre si:
  # dos archivos ILEGIBLES del mismo tamaño salian juntos como "duplicados"
  # aunque su contenido fuera distinto. Se apartan y se nombran.
  if [ -z "$h" ]; then printf '%s\n' "$f" >> "${HASHES}.ilegibles"; continue; fi
  printf '%s\t%s\n' "$h" "$f" >> "$HASHES"
done

VACIOS=$(find "$@" -type f ! -name '.*' -size 0 2>/dev/null | wc -l | tr -d ' ')
echo "Archivos analizados: $(wc -l < "$SIZES" | tr -d ' ')"
# Los de CERO bytes se excluyen del hasheo a proposito: todos comparten el mismo
# md5 (el del vacio) y un deduplicador los agrupa como si fueran la misma cosa,
# cuando son fallos DISTINTOS — medido el 27-09-2026 en un respaldo real: 16
# imagenes de WhatsApp que nunca terminaron de bajar, agrupadas como "16 copias".
# Pero excluir en SILENCIO es la clase que esta skill persigue: 16 archivos rotos
# en una biblioteca son un HALLAZGO, no ruido. Se cuentan y se nombran.
if [ "$VACIOS" -gt 0 ]; then
  echo "⚠️  $VACIOS archivo(s) de 0 bytes, fuera del analisis (todos comparten hash y NO son duplicados entre si):"
  find "$@" -type f ! -name '.*' -size 0 2>/dev/null | sed 's/^/   /'
fi
cut -f1 "$HASHES" | sort | uniq -d > "${HASHES}.dup"
if [ -s "${HASHES}.ilegibles" ]; then
  echo "⚠️  $(wc -l < "${HASHES}.ilegibles" | tr -d ' ') archivo(s) que NO se pudieron leer, fuera del analisis:"
  sed 's/^/   /' "${HASHES}.ilegibles"
  echo "   (sin huella no se puede afirmar que sean copias de nada)"
fi
echo "Grupos de duplicados exactos: $(wc -l < "${HASHES}.dup" | tr -d ' ')"
echo ""
i=0
while IFS= read -r h; do
  i=$((i+1)); echo "-- Grupo $i --"
  grep "^$h	" "$HASHES" | cut -f2 | sed 's/^/   /'
  echo ""
done < "${HASHES}.dup"
rm -f "$SIZES" "${SIZES}.dup" "${HASHES}.dup" "${HASHES}.ilegibles"   # se conserva solo el TSV de hashes
echo "TSV completo de hashes: $HASHES"
