#!/bin/bash
# separar-web.sh "<carpeta-unidad>" "<movimientos.log>" [APLICAR]
# Separa el material LISTO PARA SUBIR de los originales master, dentro de un
# producto: mueve a "<unidad>/🌐 WEB SHOPIFY" los WebP y los MP4 livianos que
# estén en carpetas-librería GENÉRICAS. Los masters (PNG/JPG pesados, .mov, 4K)
# se quedan donde están.
#
# Sin APLICAR corre en seco (solo lista lo que movería). El default es seco
# porque este paso reubica material que el usuario reconoce de memoria: conviene
# leer la lista antes.
#
# Por qué solo carpetas genéricas: los sets creativos deliberados (por
# orientación, por tamaño de Canva, por propósito como ADS o ANTES Y DESPUES)
# son piezas de pauta, no assets de ficha de producto. Arrastrarlos a la carpeta
# web rompe el criterio de "todo lo que hay aquí se sube" y destruye una
# organización que suele ser mejor que la genérica.
set -u
UNIT="${1:?Uso: separar-web.sh \"<carpeta-unidad>\" \"<movimientos.log>\" [APLICAR]}"
LOG="${2:-}"
MODE="${3:-}"
[ -d "$UNIT" ] || { echo "  (no existe: $UNIT)"; exit 0; }

# Carpetas-librería genéricas: donde el material se acumula sin criterio y
# por eso web y master terminan revueltos.
es_generica() {
  # nocasematch pliega el casing ASCII (Fotos/FOTOS/fotos, Canva/CANVA); los patrones
  # van en minúscula. Sin esto, una carpeta "Fotos" del usuario no se reconocía y sus
  # .webp no se separaban — devolvía "0 piezas" en silencio.
  shopt -s nocasematch
  # nocasematch NO pliega la tilde (Á≠á), así que las formas acentuadas se listan
  # en sus dos casings: "imágenes" cubre Imágenes/imágenes, "IMÁGENES" cubre el todo-mayúsculas.
  case "$1" in
    imágenes|IMÁGENES|imagenes|imagen|img|foto|fotos|videos|video|canva|camva) shopt -u nocasematch; return 0;;
    *) shopt -u nocasematch; return 1;;
  esac
}

# Un archivo es "movible" solo si TODOS los tramos entre la unidad y el archivo
# son genéricos. Basta con mirar el padre inmediato no alcanza: un "VIDEO" dentro
# de "ANTES Y DESPUES" es parte de un set deliberado (la pareja foto+video del
# antes/después), y sacarlo a la carpeta web rompe ese grupo. Si algún ancestro
# es un set con propósito/tamaño/orientación (no genérico), NO se toca.
ruta_solo_generica() {  # ruta_solo_generica "<archivo>"
  local rel="${1#$UNIT/}"      # ruta relativa a la unidad
  local dir="$(dirname "$rel")"
  [ "$dir" = "." ] && return 1  # archivo suelto en la raíz de la unidad: no es librería
  local IFS='/'
  for seg in $dir; do es_generica "$seg" || return 1; done
  return 0
}

LIMITE_VIDEO=$((10*1024*1024))   # 10 MB: por encima se trata como master
WEB="$UNIT/🌐 WEB SHOPIFY"

if [ "$MODE" = "APLICAR" ]; then
  [ -n "$LOG" ] || { echo "🔴 Falta el log. Uso: separar-web.sh \"<carpeta>\" \"<log>\" APLICAR" >&2; exit 1; }
  mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] \
    || { echo "🔴 Log no escribible: $LOG — no se mueve nada" >&2; exit 1; }
fi

TMP="$(mktemp)"
find "$UNIT" -type f ! -name '.*' 2>/dev/null > "$TMP"   # snapshot antes de mover
n=0
while IFS= read -r f; do
  padre="$(basename "$(dirname "$f")")"
  case "$padre" in "🌐 WEB SHOPIFY") continue;; esac       # ya está separado
  ruta_solo_generica "$f" || continue                       # ancestro deliberado = no tocar
  b="$(basename "$f")"
  ext="$(printf '%s' "${b##*.}" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in
    webp) : ;;                                            # webp = optimizado para web
    mp4)  sz=$(stat -f%z "$f" 2>/dev/null || echo 0)
          [ "$sz" -lt "$LIMITE_VIDEO" ] || continue ;;     # mp4 pesado = master
    *)    continue ;;                                      # png/jpg/mov = master
  esac
  n=$((n+1))
  if [ "$MODE" != "APLICAR" ]; then
    echo "   $padre/$b"
    continue
  fi
  mkdir -p "$WEB"
  dest="$WEB/$b"
  if [ -e "$dest" ]; then
    name="${b%.*}"; e2="${b##*.}"; [ "$name" = "$e2" ] && e2=""
    k=1; while [ -e "$WEB/${name} (${k})${e2:+.$e2}" ]; do k=$((k+1)); done
    dest="$WEB/${name} (${k})${e2:+.$e2}"
  fi
  mv "$f" "$dest" && printf 'MV\t%s\t%s\n' "$f" "$dest" >> "$LOG"
done < "$TMP"
rm -f "$TMP"

if [ "$MODE" = "APLICAR" ]; then
  echo "✔ $(basename "$UNIT"): $n piezas movidas a 🌐 WEB SHOPIFY"
else
  echo "   → $n piezas se moverían. Repite con APLICAR para ejecutar."
fi
