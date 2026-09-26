#!/bin/bash
# autoprueba.sh — el banco que esta skill NO TENÍA.
#
# POR QUÉ EXISTE (auditoría del Centro de Mando, 2026-09-07, orden de FER)
# Esta es la skill más grande del arsenal —22 ficheros— y su trabajo es VALIDAR el prompt que
# otros van a poner delante de clientes reales. Tenía DOS validadores y **ninguno tenía banco**.
# Es decir: nadie había comprobado nunca que muerdan.
#
# Ley de la casa que lo obliga: "si tu script dice que todo está bien a la primera, sospecha del
# script — pruébalo contra un caso que sepas malo". Y la del barrido de listas blancas: **el
# banco debe MORDER ante el sabotaje de CADA pieza**, no solo del conjunto. Un banco que solo
# prueba el caso global da verde con media herramienta rota.
#
# CÓMO ESTÁ HECHO: se parte de la vara mínima de la propia skill (references/ejemplo-minimo.md),
# que es un prompt que SÍ pasa, y se le mete un sabotaje cada vez. Cada sabotaje tiene que
# producir el bloqueo Y nombrar su motivo. Si un sabotaje pasa en verde, ese chequeo está muerto.
#
# Uso:  bash scripts/autoprueba.sh      ·  0 = todo muerde  ·  1 = hay un chequeo muerto
set -uo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
V="$D/scripts/validar.sh"
DOC="$D/scripts/validar-doctrina.sh"
VARA="$D/references/ejemplo-minimo.md"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

ok=0; total=0; fallos=()

# Extrae el prompt de la vara a un .txt plano, que es lo que el validador come en modo PROMPT.
python3 - "$VARA" "$T/bueno.txt" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"```[a-z]*\n(.*?)```", t, re.S)
open(sys.argv[2], "w", encoding="utf-8").write(m.group(1) if m else t)
PY

# check <n> <nombre> <esperado: PASA|BLOQUEA> <fichero> [texto que debe aparecer]
check() {
  local n="$1" nom="$2" esp="$3" f="$4" frase="${5:-}"
  total=$((total+1))
  local sal rc
  sal="$(bash "$V" "$f" 2>&1)"; rc=$?
  local bien=0
  if [ "$esp" = "BLOQUEA" ]; then
    [ "$rc" -eq 3 ] && bien=1
    if [ -n "$frase" ] && ! printf '%s' "$sal" | grep -qi -- "$frase"; then bien=0; fi
  else
    [ "$rc" -ne 3 ] && bien=1
  fi
  if [ "$bien" -eq 1 ]; then ok=$((ok+1)); echo "   OK  $n. $nom"
  else echo "   🔴  $n. $nom  (exit=$rc, esperado $esp)"; fallos+=("$n. $nom"); fi
}

# 🔴 TRAMPA DE pipefail, y me mordió a mí construyendo este banco (2026-09-07).
# Con `set -o pipefail`, en `if bash validar.sh f | grep -q "X"; then` el `if` evalúa el exit de
# la TUBERÍA, que con pipefail es el del validador (3 = bloqueado), NO el de grep (0 = encontró).
# Resultado: tres chequeos VIVOS se reportaron como muertos, y estuve a punto de "arreglar" un
# validador que funcionaba. La salida se captura a variable ANTES de grepear, siempre.
# dice <fichero> <modo> <frase>  ·  0 si la frase aparece en la salida
dice() {
  local f="$1" modo="$2" frase="$3" sal
  if [ "$modo" = "activador" ]; then sal="$(bash "$V" --activador "$f" 2>&1)"
  else sal="$(bash "$V" "$f" 2>&1)"; fi
  printf '%s' "$sal" | grep -qiE -- "$frase"
}

# sabotea <fichero-destino> <texto a inyectar>
sabotea() { cp "$T/bueno.txt" "$1"; printf '\n%s\n' "$2" >> "$1"; }

echo "  === AUTOPRUEBA · los dos sentidos, sabotaje por PIEZA ==="

# ---- 1 · el caso BUENO tiene que pasar. Un banco que solo muerde no sirve: ----
#      si todo bloquea, el validador no discrimina, y eso también es estar roto.
check 1 "la VARA MÍNIMA de la propia skill PASA" PASA "$T/bueno.txt"

# ---- 2-9 · cada pieza, saboteada por separado ----
sabotea "$T/s2.txt" "Hola, ¿cómo estás? ¡Bienvenido!"
check 2 "muerde los SIGNOS DE APERTURA" BLOQUEA "$T/s2.txt" "SIGNOS DE APERTURA"

sabotea "$T/s3.txt" "Te atiende Santiago, tu asesor."
check 3 "muerde el ASESOR DE FÁBRICA (Santiago)" BLOQUEA "$T/s3.txt" "DATO DE FÁBRICA"

sabotea "$T/s4.txt" "Somos una tienda con 5 años de experiencia."
check 4 "muerde la BIOGRAFÍA DE FÁBRICA (5 años de experiencia)" BLOQUEA "$T/s4.txt" "DATO DE FÁBRICA"

sabotea "$T/s5.txt" "Soy un bot automatizado creado con inteligencia artificial."
check 5 "muerde que EL BOT SE DELATE COMO IA" BLOQUEA "$T/s5.txt" "SE DELATA"

sabotea "$T/s6.txt" "Usa la clave sk_live_AAAAAAAAAAAA para conectarte."
check 6 "muerde una CREDENCIAL (sk_live_)" BLOQUEA "$T/s6.txt" "CREDENCIAL"

# 6b · LAGUNA REAL cerrada el 2026-09-07: sk-ant- (Anthropic) NO estaba en la lista y un
#      prompt con una clave de Anthropic pasaba en verde. Mi primer caso 6 usaba justo ese
#      patron y lo di por "chequeo muerto" sin mirar: no lo era, era una laguna distinta.
sabotea "$T/s6b.txt" "Conecta con sk-ant-api03-AAAAAAAAAAAAAAAAAAAA."
check 6b "muerde una CREDENCIAL de Anthropic (sk-ant-)" BLOQUEA "$T/s6b.txt" "CREDENCIAL"

sabotea "$T/s7.txt" "Mira esto 🎉🎊🥳🎁🔥🚀 no te lo pierdas 💥⭐"
check 7 "muerde el ABUSO DE EMOJIS en una línea" BLOQUEA "$T/s7.txt" "EMOJIS"

# la regla de brevedad: se quita del prompt bueno y tiene que saltar
python3 - "$T/bueno.txt" "$T/s8.txt" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
# 🔴 La vara escribe "máx 35 palabras" CON ACENTO. Mi primera version de este sabotaje
# buscaba "máximo" y hacia CERO sustituciones: el fichero salia intacto, pasaba en verde, y yo
# lo lei como "el chequeo de brevedad esta muerto". No lo estaba. Se normaliza igual que el
# validador antes de sustituir. Un banco solo prueba lo que su autor imagino.
import unicodedata
def _sin(x):
    return "".join(c for c in unicodedata.normalize("NFD", x) if unicodedata.category(c) != "Mn")
_pat = re.compile(r"(maximo|max\.?|no mas de|no superes|hasta)\s*\d{1,3}\s*palabras", re.I)
_out = []
for _l in t.splitlines(True):
    _out.append("responde corto\n" if _pat.search(_sin(_l)) else _l)
t = "".join(_out)
open(sys.argv[2], "w", encoding="utf-8").write(t)
PY
check 8 "muerde la FALTA DE REGLA DE BREVEDAD" BLOQUEA "$T/s8.txt" "BREVEDAD"

# 9 · El BOM se comprueba en modo ACTIVADOR, no en modo prompt, y ese alcance es CORRECTO:
#     el BOM rompe el match BYTE A BYTE del trigger; dentro de un prompt largo no rompe nada.
#     Mi primer caso lo probaba en modo prompt y lo conto como chequeo muerto. No lo era: era
#     yo probando la pieza equivocada.
total=$((total+1))
printf '\xef\xbb\xbfQUIERO EL CEPILLO 360\n' > "$T/s9.txt"
if dice "$T/s9.txt" activador "BOM invisible"; then
  ok=$((ok+1)); echo "   OK  9. muerde el BOM invisible en el ACTIVADOR"
else echo "   🔴  9. NO muerde el BOM en el activador"; fallos+=("9. BOM activador"); fi

# ---- 10-11 · el modo ACTIVADOR, que es otro camino de código ----
total=$((total+1))
echo "Hola, quiero información y precio" > "$T/act_gen.txt"
# 🔴 ANCLAS SIN ACENTOS, y el motivo es de los que se pagan dos veces: sin un locale UTF-8
#    (LANG viene vacío aquí), grep trabaja por BYTES, no por caracteres. "F.RMULA" NO casa con
#    "FÓRMULA" porque la Ó ocupa DOS bytes y el punto consume uno solo. Costó dar por muerto un
#    chequeo que estaba vivo. Se ancla en subcadenas ASCII puras, que casan en cualquier locale.
if dice "$T/act_gen.txt" activador "DISPARADOR FUERA DE LA|ACTIVADOR GEN"; then
  ok=$((ok+1)); echo "   OK  10. muerde un ACTIVADOR genérico"
else echo "   🔴  10. NO muerde un activador genérico"; fallos+=("10. activador genérico"); fi

total=$((total+1))
printf 'QUIERO EL CEPILLO 360 \xf0\x9f\x94\xa5\n' > "$T/act_emoji.txt"
if dice "$T/act_emoji.txt" activador "permitida del activador"; then
  ok=$((ok+1)); echo "   OK  11. muerde un EMOJI en el activador (corrompe el trigger)"
else echo "   🔴  11. NO muerde un emoji en el activador"; fallos+=("11. emoji en activador"); fi

# ---- 12 · el AVISO de cifras sale AUNQUE el prompt pase en verde ----
#      Este es el caso peligroso de verdad: no el prompt que bloquea, sino el que pasa
#      limpio llevando una cifra heredada dentro.
total=$((total+1))
sabotea "$T/s12.txt" "Más de 100.000 clientes atendidos."
if dice "$T/s12.txt" prompt "CIFRAS DE NEGOCIO"; then
  ok=$((ok+1)); echo "   OK  12. AVISA de las cifras de negocio sin bloquear la entrega"
else echo "   🔴  12. NO avisa de una cifra de negocio"; fallos+=("12. aviso de cifras"); fi

# ---- 13-14 · el validador de DOCTRINA ----
total=$((total+1))
if bash "$DOC" --vara "$VARA" >/dev/null 2>&1 || [ $? -ne 3 ]; then
  ok=$((ok+1)); echo "   OK  13. la vara mínima CUMPLE la doctrina"
else echo "   🔴  13. la vara mínima no pasa su propio validador de doctrina"; fallos+=("13. doctrina vara"); fi

total=$((total+1))
echo "Vendemos el producto. Cuesta 50000. Escríbeme." > "$T/sin_doctrina.txt"
bash "$DOC" "$T/sin_doctrina.txt" >/dev/null 2>&1; _rc=$?
if [ "$_rc" -eq 3 ]; then
  ok=$((ok+1)); echo "   OK  14. BLOQUEA un texto sin los tramos de la doctrina"
else echo "   🔴  14. deja pasar un texto sin doctrina (exit=$_rc)"; fallos+=("14. doctrina vacía"); fi

# ---- 15-17 · las dos reglas que vivían solo en los .md (v3.63.0) ----
#      El 17 es el que de verdad importa: prueba que NO muerde el idioma normal. Un detector
#      de apodos sin este caso bloquearía "cuida tu corazón" en un producto cardiovascular.
sabotea "$T/s15.txt" "Magnífico Corazón 💚, mira estas opciones."
check 15 "muerde el APODO DE FALSA CERCANÍA (Magnífico Corazón)" BLOQUEA "$T/s15.txt" "FALSA CERCAN"

total=$((total+1))
sabotea "$T/s16.txt" "Solo nos quedan 7 unidades con la promoción."
if dice "$T/s16.txt" prompt "ESCASEZ SIN CONFIRMAR"; then
  ok=$((ok+1)); echo "   OK  16. AVISA de la escasez sin confirmar sin bloquear la entrega"
else echo "   🔴  16. NO avisa de una escasez sin confirmar"; fallos+=("16. aviso de escasez"); fi

sabotea "$T/s17.txt" "Cuida tu corazón y tu presión arterial; es la reina del hogar quien decide."
check 17 "NO acusa al idioma: corazón y reina fuera de vocativo PASAN" PASA "$T/s17.txt"

echo
if [ "${#fallos[@]}" -eq 0 ]; then
  echo "  $ok de $total · los dos validadores muerden pieza por pieza"
  exit 0
fi
echo "  🔴 $ok de $total — CHEQUEOS MUERTOS:"
for f in "${fallos[@]}"; do echo "     · $f"; done
exit 1
