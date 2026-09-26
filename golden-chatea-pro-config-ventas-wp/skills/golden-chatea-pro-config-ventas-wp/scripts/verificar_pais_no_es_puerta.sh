#!/bin/bash
# verificar_pais_no_es_puerta.sh — guardarrail de DOCTRINA, no de sintaxis.
#
# POR QUE EXISTE (Centro de Mando, 2026-09-06, mandato de FER)
# El pais es PARAMETRO, no PUERTA: "hoy son diez, manana doce, pasado treinta; el pais se
# pide para saber COMO enfocarlo, no para prohibir". Hasta la v4.7 esta skill tenia la
# puerta VIVA Y EJECUTABLE en build_config.py: 'el salvador' y 'bolivia' salian rechazados
# por escrito, sin generar nada.
#
# Y no basta con quitarla una vez. La lista de paises es un dato que CADUCA SOLO y que ya
# caduco aqui una vez (decia 7 cuando eran 10, y rechazo Guatemala, Argentina y Brasil).
# La tentacion de "validar el pais" vuelve sola en cada refactor, y vuelve con buena
# intencion. Este guion existe para que vuelva EN ROJO.
#
# QUE COMPRUEBA (ejerciendo, no leyendo):
#  1. build_config.py genera los dos bot fields para un pais que NO esta en la lista.
#  2. no queda ningun sys.exit atado a la pertenencia del pais a la lista.
#  3. el pais conocido sigue funcionando (que quitar la puerta no rompa lo de siempre).
#
# Uso:  bash scripts/verificar_pais_no_es_puerta.sh     ·  0 = doctrina viva · 1 = volvio la puerta
set -uo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
echo "prompt maestro de prueba" > "$T/pm.txt"
fallos=0

echo "  === EL PAIS NO ES UNA PUERTA · se verifica EJERCIENDO ==="

# 1 · un pais fuera de la lista TIENE que producir configuracion
python3 "$D/scripts/build_config.py" --pais "el salvador" --moneda "USD" \
  --flete-max "23000" --whatsapp-notif "+503 70000000" --url-tienda "https://x.sv" \
  --nombre-bot "Ana" --nombre-tienda "Empresa" --modelo dropshipping \
  --prompt-maestro "$T/pm.txt" --out-prefix "$T/sv" >/dev/null 2>&1
if [ -f "$T/sv_BOTFIELD_1.json" ] && [ -f "$T/sv_BOTFIELD_2.json" ]; then
  echo "   OK  un pais SIN pack (el salvador) se configura igual"
else
  echo "   🔴 VOLVIO LA PUERTA: 'el salvador' no genero configuracion"; fallos=$((fallos+1))
fi

# 2 · ningun sys.exit puede colgar de la pertenencia a la lista
if grep -n "not in PAISES" "$D/scripts/build_config.py" | grep -q "sys.exit"; then
  echo "   🔴 hay un sys.exit atado a 'not in PAISES'"; fallos=$((fallos+1))
else
  ctx=$(grep -A3 "not in PAISES" "$D/scripts/build_config.py" | grep -c "sys.exit" || true)
  if [ "$ctx" -gt 0 ]; then
    echo "   🔴 VOLVIO LA PUERTA: sys.exit dentro del bloque de 'not in PAISES'"; fallos=$((fallos+1))
  else
    echo "   OK  ningun sys.exit cuelga de la pertenencia a la lista"
  fi
fi

# 3 · y lo de siempre sigue funcionando
python3 "$D/scripts/build_config.py" --pais "colombia" --flete-max "23000" \
  --whatsapp-notif "+57 3001234567" --url-tienda "https://x.co" \
  --nombre-bot "Ana" --nombre-tienda "Empresa" --modelo dropshipping \
  --prompt-maestro "$T/pm.txt" --out-prefix "$T/co" >/dev/null 2>&1
if [ -f "$T/co_BOTFIELD_1.json" ]; then
  echo "   OK  un pais CON pack (colombia) sigue funcionando"
else
  echo "   🔴 REGRESION: colombia dejo de generar configuracion"; fallos=$((fallos+1))
fi

# 4 · contraprueba: el banco tiene que MORDER si alguien repone la puerta
# 🔴 chmod OBLIGATORIO tras el cp: la skill vive BLINDADA (chflags uchg + chmod 444) y la
# copia hereda el 444, asi que el sabotaje moria con PermissionError. Medido el 2026-09-07
# en corrida fresca: este guardarrail pasaba cuando lo escribi —con la skill abierta— y
# fallaba con la skill sellada, que es su estado NORMAL. Un guardarrail que solo funciona
# mientras alguien edita no sirve: el momento en que hace falta es justo el otro.
cp "$D/scripts/build_config.py" "$T/bc_saboteado.py"
chmod u+w "$T/bc_saboteado.py"
python3 - "$T/bc_saboteado.py" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
s = s.replace('    if a.pais.upper() not in PAISES:\n',
              '    if a.pais.upper() not in PAISES:\n        sys.exit("puerta repuesta")\n', 1)
open(p, "w", encoding="utf-8").write(s)
PY
if grep -A1 "not in PAISES" "$T/bc_saboteado.py" | grep -q "sys.exit"; then
  echo "   OK  contraprueba: el detector VE la puerta cuando alguien la repone"
else
  echo "   🔴 el detector NO ve la puerta ni cuando esta puesta a proposito"; fallos=$((fallos+1))
fi

echo
if [ "$fallos" -eq 0 ]; then echo "  4 de 4 · el pais sigue siendo parametro"; exit 0
else echo "  🔴 $fallos fallo(s): la puerta volvio"; exit 1; fi
