#!/bin/bash
# eliminar.sh "<archivo-a-borrar>" "<archivo-que-sobrevive>" "<ELIMINADOS.log>" [FORCE]
# Borra un duplicado SOLO si es idéntico byte a byte al sobreviviente, y deja la
# línea de registro en el formato exacto que la skill promete:
#   RM<TAB>ruta-borrada<TAB>ruta-del-sobreviviente<TAB>md5
#
# Por qué existe: sin esta verificación el borrado depende de que quien ejecuta
# "crea" que son iguales, y el md5 en el log es lo único que después prueba que
# lo borrado y lo conservado eran el mismo contenido. La recuperación es copiar
# el sobreviviente de vuelta a la ruta borrada.
#
# FORCE permite borrar cuando NO son idénticos (ej. misma imagen en menor
# resolución teniendo la mayor). Exige haberlas mirado antes: se registra con
# los dos md5 distintos para que quede claro que no fue un duplicado exacto.
set -u
DEL="${1:?Uso: eliminar.sh \"<a-borrar>\" \"<sobreviviente>\" \"<ELIMINADOS.log>\" [FORCE]}"
KEEP="${2:?Falta el archivo que sobrevive}"
LOG="${3:?Falta ELIMINADOS.log}"
MODE="${4:-}"

[ -f "$DEL" ]  || { echo "🔴 No existe el archivo a borrar: $DEL" >&2; exit 1; }
[ -f "$KEEP" ] || { echo "🔴 No existe el sobreviviente: $KEEP — sin sobreviviente NO se borra" >&2; exit 1; }
[ "$DEL" != "$KEEP" ] || { echo "🔴 Origen y sobreviviente son el mismo archivo" >&2; exit 1; }
mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] \
  || { echo "🔴 Log no escribible: $LOG — no se borra nada" >&2; exit 1; }

H_DEL="$(md5 -q "$DEL")"; H_KEEP="$(md5 -q "$KEEP")"

if [ "$H_DEL" = "$H_KEEP" ]; then
  rm "$DEL" && printf 'RM\t%s\t%s\t%s\n' "$DEL" "$KEEP" "$H_DEL" >> "$LOG" \
    && echo "✔ borrado (idéntico byte a byte): $(basename "$DEL")"
elif [ "$MODE" = "FORCE" ]; then
  rm "$DEL" && printf 'RM\t%s\t%s\t%s!=%s\n' "$DEL" "$KEEP" "$H_DEL" "$H_KEEP" >> "$LOG" \
    && echo "✔ borrado (FORCE, NO idéntico — se conserva $(basename "$KEEP")): $(basename "$DEL")"
else
  echo "🛑 NO son idénticos ($H_DEL vs $H_KEEP). No se borró nada." >&2
  echo "   Míralas lado a lado; pueden ser variantes legítimas (idioma, tono, fragancia," >&2
  echo "   GIF vs fijo, web vs master). Si aun así sobra, repite con FORCE." >&2
  exit 2
fi
