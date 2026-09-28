#!/bin/bash
# abrir_blindaje.sh - Abre el blindaje de la skill Y CAPTURA EL ANTES en el mismo acto.
#
# POR QUE EXISTE. La forma canonica del Centro de Mando pide `md5 <artefacto>
# ANTES -> DESPUES`. Fallé dos veces el mismo dia, en el mismo archivo: tomé el
# ANTES despues de haber editado, asi que el comando imprimio el mismo valor a
# los dos lados. Dos veces el mismo tropiezo no es descuido, es que el
# procedimiento pedia memoria en el momento de menos atencion.
#
# La regla que faltaba: EL ANTES SE TOMA EN EL MISMO COMANDO QUE ABRE EL
# BLINDAJE, antes de la primera escritura. Si depende de que te acuerdes
# despues, se pierde. Si viaja pegado al acto de abrir, no.
#
#   ./scripts/abrir_blindaje.sh            -> abre y guarda el ANTES
#   ./scripts/abrir_blindaje.sh --cerrar   -> imprime los pares y vuelve a blindar
#
# LA CANONICA DEL ARSENAL ES `~/.golden/bin/golden-blindaje`, que generaliza este
# diseño para las 38 skills. Este de aqui sobrevive solo porque encontro y arreglo
# un fallo que la canonica todavia hereda (el acta que no se consume). En cuanto la
# canonica lo tenga, este archivo se sustituye por una llamada a ella: dos recetas
# compitiendo es el fallo que nombro golden360, y la fuente autoritativa no se
# reimplementa, se delega.

set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
ACTA="${TMPDIR:-/tmp}/blindaje_$(basename "$SKILL").md5"

hashes() {
  cd "$SKILL"
  # P59 (27-sep): antes solo .md/.py/.js/.html/.sh; un .json o .css cambiado no salia en el par.
  find . -type f ! -name '.DS_Store' ! -path '*/__pycache__/*' \
    | sort | while read -r f; do echo "$(md5 -q "$f")  ${f#./}"; done
}

if [ "$1" = "--cerrar" ]; then
  [ -f "$ACTA" ] || { echo "No hay ANTES guardado. Se abrio sin este script: el par no se puede dar."; exit 1; }
  # EL ACTA CADUCA. Medido el 2026-09-05: la primera version no la borraba al
  # cerrar, asi que --cerrar se podia repetir indefinidamente y devolvia SIEMPRE
  # el mismo par, con cara de captura fresca. Una skill sin tocar podia reportar
  # "1 artefacto cambiado". Un acta que sobrevive a su cierre es peor que no
  # tenerla: la ausencia se nota, la rancia no.
  EDAD=$(( $(date +%s) - $(stat -f %m "$ACTA") ))
  if [ "$EDAD" -gt 43200 ]; then
    echo "El ANTES tiene $((EDAD/3600)) horas: es de otra sesion, no de este trabajo."
    echo "No doy pares con un acta rancia. Borrala y vuelve a abrir:  rm $ACTA"
    exit 1
  fi
  echo "md5 ANTES -> DESPUES  (ruta: $SKILL)"
  hashes > "${ACTA}.despues"
  # Solo los que cambiaron: un par identico no dice nada.
  awk 'NR==FNR{a[$2]=$1;next} a[$2]!=$1 {printf "  %-30s %s -> %s\n", $2, a[$2], $1}' \
      "$ACTA" "${ACTA}.despues"
  # P59: los BORRADOS no salian (el awk de arriba solo recorre el DESPUES). Se listan y se cuentan.
  awk 'NR==FNR{b[$2]=1;next} !($2 in b) {printf "  %-30s %s -> (BORRADO)\n", $2, $1}' \
      "${ACTA}.despues" "$ACTA"
  n=$(( $(awk 'NR==FNR{a[$2]=$1;next} a[$2]!=$1' "$ACTA" "${ACTA}.despues" | wc -l | tr -d ' ') \
      + $(awk 'NR==FNR{b[$2]=1;next} !($2 in b)' "${ACTA}.despues" "$ACTA" | wc -l | tr -d ' ') ))
  echo "  ($n artefactos cambiados)"
  [ "$n" = "0" ] && echo "  OJO: cero cambios. Si dices que mejoraste algo, la nota es falsa."
  chflags -R uchg "$SKILL"
  rm -f "$ACTA" "${ACTA}.despues"   # el acta SE CONSUME: un cierre, un par
  echo "Blindada, y el acta consumida. Para otra ronda hay que volver a abrir."
  exit 0
fi

chflags -R nouchg "$SKILL"
chmod -R u+w "$SKILL"
hashes > "$ACTA"
echo "Blindaje abierto. ANTES capturado de $(wc -l < "$ACTA" | tr -d ' ') artefactos en:"
echo "  $ACTA"
echo "Al terminar: $0 --cerrar"
