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
. "$(dirname "$0")/_comun.sh"
exigir_local "$DEL" "BORRAR un archivo"
mkdir -p "$(dirname "$LOG")" && touch "$LOG" && [ -w "$LOG" ] \
  || { echo "🔴 Log no escribible: $LOG — no se borra nada" >&2; exit 1; }

H_DEL="$(md5 -q "$DEL" 2>/dev/null)"; H_KEEP="$(md5 -q "$KEEP" 2>/dev/null)"

# Si `md5` falla (permisos, archivo ilegible, disco con errores) devuelve VACIO,
# y la comparacion de abajo compara "" con "" y da IGUAL. Medido el 27-09-2026:
# dos archivos con contenido DISTINTO ("bbbb" y "cccc") en chmod 000 se
# declararon "identico byte a byte" y uno se BORRO. Es el peor fallo posible de
# esta herramienta: la verificacion md5 es TODA la garantia de seguridad del
# borrado, y cuando el instrumento falla, su silencio se lee como conformidad.
# Un hash vacio no es un hash: es la ausencia de la medicion.
for par in "DEL:$H_DEL:$DEL" "KEEP:$H_KEEP:$KEEP"; do
  cual="${par%%:*}"; resto="${par#*:}"; h="${resto%%:*}"; ruta="${resto#*:}"
  if [ -z "$h" ]; then
    echo "🔴 No se pudo calcular el md5 de $ruta ($cual). NO se borra nada." >&2
    echo "   Sin las dos huellas no hay verificacion, y sin verificacion este" >&2
    echo "   script no tiene derecho a borrar. Revisa permisos o si el archivo esta danado." >&2
    exit 1
  fi
done

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
