#!/bin/bash
# auditar.sh "<raíz>"
# Diagnóstico de salud de una biblioteca. Corre todos los chequeos de una vez
# para saber qué falta antes de empezar y para verificar al cerrar.
# No modifica nada: solo reporta.
set -u
R="${1:?ruta raíz}"
# Normaliza la ruta: quita las barras finales. `for U in "$R"/*/` — la forma
# canonica de recorrer productos — SIEMPRE entrega barra final, y sin esto
# "$R/archivo" no se puede recortar contra "$R", asi que el script
# devolvia 0 SIN error (medido 2026-09-05: 1 pieza sin barra, 0 con barra).
while [ "$R" != "/" ] && [ "${R%/}" != "$R" ]; do R="${R%/}"; done
# Array y no string: sin comillas el shell puede glob-expandir los patrones antes de que find los vea
# La raiz misma no tiene nada que recortar: sin esto sale su ruta ABSOLUTA
# en medio de un informe de rutas relativas y no se puede leer de un vistazo.
rel_de(){ [ "$1" = "$R" ] && printf "(raiz)" || printf "%s" "${1#$R/}"; }
EXCL=(! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/.next/*' ! -path '*/dist/*')

echo "📋 AUDITORÍA: $R"
echo ""

echo "📁 1. Carpetas que MEZCLAN archivos sueltos con subcarpetas"
mix=0
while IFS= read -r d; do
  f=$(find "$d" -maxdepth 1 -type f ! -name '.*' 2>/dev/null | wc -l | tr -d ' ')
  s=$(find "$d" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  if [ "$f" -gt 0 ] && [ "$s" -gt 0 ]; then
    echo "   [$f archivos + $s carpetas] $(rel_de "$d")"; mix=$((mix+1))
  fi
done < <(find "$R" -type d "${EXCL[@]}" 2>/dev/null)
[ "$mix" -eq 0 ] && echo "   ✅ ninguna"
echo ""

echo "🗑️ 2. Carpetas VACÍAS"
emp=$(find "$R" -type d -empty "${EXCL[@]}" 2>/dev/null)
if [ -z "$emp" ]; then echo "   ✅ ninguna"; else echo "$emp" | sed "s|$R/|   |"; fi
echo ""

echo "🧹 3. Basura (descargas a medias, temporales)"
jj=$(find "$R" -type f "${EXCL[@]}" \( -iname '*.crdownload' -o -iname '*.part' -o -iname '*.download' -o -iname '*.tmp' \) 2>/dev/null)
if [ -z "$jj" ]; then echo "   ✅ ninguna"; else echo "$jj" | sed "s|$R/|   |"; fi
echo ""

echo "❓ 4. Nombres CRÍPTICOS (hay que mirarlos para saber qué son)"
find "$R" -type f "${EXCL[@]}" \( -iname 'IMG_*' -o -iname 'DSC*' -o -iname 'Captura*' \
  -o -iname 'RPReplay*' -o -iname 'ChatGPT Image*' \
  -o -iname '*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*' \) 2>/dev/null \
  | head -15 | sed "s|$R/|   |"
c=$(find "$R" -type f "${EXCL[@]}" \( -iname 'IMG_*' -o -iname 'DSC*' -o -iname 'Captura*' \
  -o -iname 'RPReplay*' -o -iname 'ChatGPT Image*' \
  -o -iname '*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*' \) 2>/dev/null | wc -l | tr -d ' ')
[ "$c" -eq 0 ] && echo "   ✅ ninguno" || echo "   → total: $c"
echo ""

echo "📑 5. Copias sueltas evidentes"
cp=$(find "$R" -type f "${EXCL[@]}" \( -name 'Copia de *' -o -name '* copy.*' -o -name '* (1).*' \) 2>/dev/null)
if [ -z "$cp" ]; then echo "   ✅ ninguna"; else echo "$cp" | sed "s|$R/|   |" | head -15; fi
echo ""

echo "🌐 6. Mezcla WEB (webp) + MASTER (png/jpg) en la misma carpeta"
mz=0
while IFS= read -r d; do
  w=$(find "$d" -maxdepth 1 -iname '*.webp' 2>/dev/null | wc -l | tr -d ' ')
  h=$(find "$d" -maxdepth 1 \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) 2>/dev/null | wc -l | tr -d ' ')
  if [ "$w" -gt 0 ] && [ "$h" -gt 0 ]; then
    echo "   [web:$w + master:$h] $(rel_de "$d")"; mz=$((mz+1))
  fi
done < <(find "$R" -type d "${EXCL[@]}" 2>/dev/null)
[ "$mz" -eq 0 ] && echo "   ✅ ninguna"
echo ""
echo "🏁 Fin. Los puntos con ✅ ya están sanos; el resto es la lista de trabajo."
