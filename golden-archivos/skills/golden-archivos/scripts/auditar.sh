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
find "$R" -type f "${EXCL[@]}" \( -iname 'IMG_*' -o -iname 'IMG-*' -o -iname '_MG_*' -o -iname 'DSC*' \
    -o -iname 'PXL_*' -o -iname 'VID_*' -o -iname 'MOV_*' -o -iname 'MVIMG*' \
    -o -iname 'Captura*' -o -iname 'Screenshot*' -o -iname 'Screen Shot*' \
  -o -iname 'RPReplay*' -o -iname 'ChatGPT Image*' -o -iname 'Gemini_Generated*' \
    -o -iname 'WhatsApp Image*' -o -iname 'WhatsApp Video*' \
    -o -iname 'Untitled*' -o -iname 'Sin titulo*' -o -iname 'descarga*' \
    -o -iname 'download*' -o -iname 'imagen*' -o -iname 'documento*' \
    -o -iname 'copia de*' -o -iname 'wetransfer*' -o -iname 'banner-[0-9]*' \
    -o -iname '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' \
  -o -iname '*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*' \) 2>/dev/null \
  | head -15 | sed "s|$R/|   |"
c=$(find "$R" -type f "${EXCL[@]}" \( -iname 'IMG_*' -o -iname 'IMG-*' -o -iname '_MG_*' -o -iname 'DSC*' \
    -o -iname 'PXL_*' -o -iname 'VID_*' -o -iname 'MOV_*' -o -iname 'MVIMG*' \
    -o -iname 'Captura*' -o -iname 'Screenshot*' -o -iname 'Screen Shot*' \
  -o -iname 'RPReplay*' -o -iname 'ChatGPT Image*' -o -iname 'Gemini_Generated*' \
    -o -iname 'WhatsApp Image*' -o -iname 'WhatsApp Video*' \
    -o -iname 'Untitled*' -o -iname 'Sin titulo*' -o -iname 'descarga*' \
    -o -iname 'download*' -o -iname 'imagen*' -o -iname 'documento*' \
    -o -iname 'copia de*' -o -iname 'wetransfer*' -o -iname 'banner-[0-9]*' \
    -o -iname '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' \
  -o -iname '*[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*' \) 2>/dev/null | wc -l | tr -d ' ')
[ "$c" -eq 0 ] && echo "   ✅ ninguno" || echo "   → total: $c"
echo ""

echo "📑 5. Copias sueltas evidentes"
# Medido el 28-09-2026 con 7 formas reales sembradas: el patron viejo detectaba
# 3. Se le escapaban `copia de x` en minuscula (usaba -name, sensible a
# mayusculas), el sufijo `x copia.jpg`, `x copy 2.jpg` y cualquier `(2)`, `(3)`…
# porque solo miraba `(1)`. Una lista de copias que ve 3 de 7 no es una lista de
# trabajo: es una muestra que se lee como el total.
cp=$(find "$R" -type f "${EXCL[@]}" \( \
       -iname 'copia de *' -o -iname '* copia.*' -o -iname '* copia [0-9]*' \
    -o -iname 'copy of *'  -o -iname '* copy.*'  -o -iname '* copy [0-9]*' \
    -o -iname '* ([0-9]).*' -o -iname '* ([0-9][0-9]).*' \
  \) 2>/dev/null)
if [ -z "$cp" ]; then
  echo "   ✅ ninguna"
else
  # La seccion 4 ya daba su total; esta cortaba con head -15 y CALLABA cuantas
  # faltaban. Medido: con 20 copias mostraba 15 y no decia nada de las otras 5,
  # asi que la lista de trabajo parecia completa. Una lista truncada sin total es
  # peor que una larga: no se ve que este truncada.
  ncp=$(printf '%s\n' "$cp" | grep -c .)
  printf '%s\n' "$cp" | sed "s|$R/|   |" | head -15
  [ "$ncp" -gt 15 ] && echo "   ... y $((ncp-15)) mas"
  echo "   → total: $ncp"
fi
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
