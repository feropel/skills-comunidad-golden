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
# Normaliza la ruta: quita las barras finales. `for U in "$R"/*/` — la forma
# canonica de recorrer productos — SIEMPRE entrega barra final, y sin esto
# "$UNIT/archivo" no se puede recortar contra "$UNIT", asi que el script
# devolvia 0 SIN error (medido 2026-09-05: 1 pieza sin barra, 0 con barra).
while [ "$UNIT" != "/" ] && [ "${UNIT%/}" != "$UNIT" ]; do UNIT="${UNIT%/}"; done
[ -d "$UNIT" ] || { echo "  (no existe: $UNIT)"; exit 0; }
. "$(dirname "$0")/_comun.sh"
exigir_local "$UNIT" "Mover material a 🌐 WEB SHOPIFY"

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

# Un mktemp que falla (sandbox sin TMPDIR, disco lleno) deja la variable VACIA
# y "$VAR/x" se vuelve "/x". Medido 2026-09-27 con un mktemp falso: sin esta
# guarda esta herramienta salia con EXIT 0 sin hacer nada — el peor de los
# ceros falsos, porque quien la llama en un bucle ve exito y da el trabajo por
# hecho. Se aborta en vez de seguir.
TMP="$(mktemp "${TMPDIR:-/tmp}/golden-archivos.XXXXXX")" || {
  echo "🔴 No se pudo crear el temporal: no se mueve nada." >&2; exit 1; }
find "$UNIT" -type f ! -name '.*' 2>/dev/null > "$TMP"   # snapshot antes de mover
n=0; YA_WEB=0; FUERA_RUTA=0; PESADOS=0
: > "$TMP.fuera"
while IFS= read -r f; do
  padre="$(basename "$(dirname "$f")")"
  b="$(basename "$f")"
  ext="$(printf '%s' "${b##*.}" | tr '[:upper:]' '[:lower:]')"
  case "$padre" in "🌐 WEB SHOPIFY") YA_WEB=$((YA_WEB+1)); continue;; esac   # ya está separado
  # Las exclusiones de abajo son CORRECTAS, pero antes se tomaban en SILENCIO:
  # una pieza web suelta en la raiz de la unidad, o dentro de un set deliberado,
  # no se movia NI se contaba. Medido el 27-09-2026: con 4 webp presentes el
  # informe decia "1 piezas se moverian" y de las otras 3 no se sabia nada.
  # Quien lee ese 1 cree que la unidad ya estaba separada.
  if ! ruta_solo_generica "$f"; then
    case "$ext" in
      webp|mp4) FUERA_RUTA=$((FUERA_RUTA+1)); printf '%s\n' "$f" >> "$TMP.fuera" ;;
    esac
    continue                                              # ancestro deliberado = no tocar
  fi
  case "$ext" in
    webp) : ;;                                            # webp = optimizado para web
    mp4)  sz=$(stat -f%z "$f" 2>/dev/null || echo 0)
          [ "$sz" -lt "$LIMITE_VIDEO" ] || { PESADOS=$((PESADOS+1)); continue; } ;;
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

# Si NADA entro y todo lo que hay cuelga de subcarpetas que a su vez parecen
# unidades, lo mas probable es que se haya pasado la carpeta que CONTIENE los
# productos en vez de un producto. Medido: yo mismo lo hice el 27-09 y la
# herramienta contesto "0 piezas se moverian" sin una palabra, asi que lei un
# cero que en realidad significaba "me diste el nivel equivocado".
# Un cero por no encontrar nada y un cero por estar mirando donde no es se leen
# igual, y solo uno de los dos es una respuesta.
if [ "$n" -eq 0 ] && [ "$FUERA_RUTA" -gt 0 ]; then
  sub_uni=0
  for d in "$UNIT"/*/; do
    [ -d "$d" ] || continue
    for g in "$d"*/; do
      [ -d "$g" ] || continue
      es_generica "$(basename "$g")" && { sub_uni=$((sub_uni+1)); break; }
    done
  done
  if [ "$sub_uni" -gt 0 ]; then
    echo "   🔴 Esto no parece una carpeta de PRODUCTO: $sub_uni de sus subcarpetas si lo parecen."
    echo "      Seguramente le pasaste la carpeta que CONTIENE los productos. Corre la"
    echo "      herramienta una vez por producto, no sobre la carpeta madre."
  fi
fi
if [ "$FUERA_RUTA" -gt 0 ]; then
  echo "   ⚠️  $FUERA_RUTA pieza(s) web NO contadas: estan sueltas en la raiz de la unidad"
  echo "       o dentro de un set deliberado, donde esta herramienta no entra a proposito."
  sed "s|$UNIT/|       |" "$TMP.fuera" | head -15
  [ "$FUERA_RUTA" -gt 15 ] && echo "       ... y $((FUERA_RUTA-15)) mas"
fi
[ "$PESADOS" -gt 0 ] && echo "   ⚠️  $PESADOS mp4 por encima del limite: se tratan como master, no se mueven."
[ "$YA_WEB" -gt 0 ] && echo "   ℹ️  $YA_WEB ya estaban en 🌐 WEB SHOPIFY."
rm -f "$TMP.fuera"
fi
