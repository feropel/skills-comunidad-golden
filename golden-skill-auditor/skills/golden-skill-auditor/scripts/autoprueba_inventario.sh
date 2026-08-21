#!/bin/bash
# autoprueba_inventario.sh — banco adversarial del detector de referencias de inventario.sh.
# Siembra en un TMPDIR (jamás en el arsenal real) un árbol con UN caso por CADA rama del
# case de inventario.sh (regla v1.9: rama sin caso sembrado = rama sin banco):
#   - falsos positivos que NO deben sonar: cross-skill OK, SKILL.md de hermana, forma corta
#     v1.7, ruta con ~, glob, directorio, dir RELATIVO desde references/, comentario HTML,
#     changelog, rescate EN_HERMANA (dueña única nombrada);
#   - males REALES que SÍ deben sonar: rota local, rota citada en un .py, hermana existente
#     con archivo faltante, forma corta rota, huérfano real, huérfano salvado antes solo por
#     una palabra suelta, huérfano cuya única mención es historia;
#   - dudas que van a DUDOSOS con conteo EXACTO: skills/ inexistente, externa faltante,
#     SKILL.md de skill fantasma, colisión multi-hermana, dueña única no nombrada.
# Cada aserción se ancla al BLOQUE del informe donde la señal debe aparecer (extractor
# bloque()), nunca al texto completo: una aserción que no puede fallar no prueba nada.
# Corre inventario.sh contra el árbol con HOME redirigido al sandbox y sale 0 solo si
# TODAS las aserciones pasan.
# Uso: bash autoprueba_inventario.sh

set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INV="$SCRIPT_DIR/inventario.sh"
[ -f "$INV" ] || { echo "FALLA: no encuentro inventario.sh junto a la autoprueba" >&2; exit 1; }

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
FAKE_HOME="$T/home"
SKILL="$FAKE_HOME/.claude/skills/skill-prueba"

# --- Siembra ---
mkdir -p "$SKILL/references/plantillas-sub" "$SKILL/scripts" "$SKILL/assets" "$SKILL/examples"
mkdir -p "$FAKE_HOME/.claude/skills/skill-hermana/scripts" "$FAKE_HOME/.claude/skills/skill-hermana/references"
mkdir -p "$FAKE_HOME/.claude/skills/skill-otra/references"
mkdir -p "$FAKE_HOME/taller/scripts"

echo "echo util" > "$FAKE_HOME/.claude/skills/skill-hermana/scripts/util.sh"     # hermana con archivo existente → OK
echo "# hermana" > "$FAKE_HOME/.claude/skills/skill-hermana/SKILL.md"            # raíz de hermana citable → OK
echo "corta" > "$FAKE_HOME/.claude/skills/skill-hermana/references/corta.md"     # forma corta v1.7 → OK
echo "vive" > "$FAKE_HOME/.claude/skills/skill-hermana/references/vive-en-hermana.md"  # rescate EN_HERMANA
echo "x" > "$FAKE_HOME/.claude/skills/skill-hermana/references/compartida.md"    # colisión: vive en 2 hermanas
echo "x" > "$FAKE_HOME/.claude/skills/skill-otra/references/compartida.md"       # colisión: vive en 2 hermanas
echo "x" > "$FAKE_HOME/.claude/skills/skill-otra/references/de-otra.md"          # dueña única NO nombrada en el texto
echo "echo externo" > "$FAKE_HOME/taller/scripts/externo.sh"                     # existe tras expandir ~

echo "guia con plantillas en plantillas-sub/ listas" > "$SKILL/references/guia.md"  # cita dir RELATIVO a references/
echo "t1" > "$SKILL/references/plantillas-sub/t1.md"      # cubierta SOLO por el dir relativo de guia.md
echo "echo vivo" > "$SKILL/scripts/vivo.sh"               # citada por ruta
printf '# motor\n# datos maestros en references/rota-en-py.md\n' > "$SKILL/scripts/motor.py"  # rota citada en un .py
echo "{}" > "$SKILL/assets/config-a.json"                 # citada SOLO por glob assets/*.json
echo "{}" > "$SKILL/assets/config-b.json"                 # citada SOLO por glob assets/*.json
echo "echo solo" > "$SKILL/scripts/solo-por-dir.sh"       # citada SOLO por directorio scripts/
echo "huerfano" > "$SKILL/references/huerfano-real.md"    # huerfano REAL: nadie lo nombra
echo "palabra" > "$SKILL/references/palabra-suelta.md"    # solo mencionada como palabra suelta (sin /): huerfana
echo "hist" > "$SKILL/references/solo-en-historia.md"    # solo mencionada en el changelog: huerfana
echo "intruso" > "$SKILL/examples/demo.txt"               # material fuera de las carpetas canonicas

cat > "$SKILL/references/changelog.md" <<'EOF'
# Changelog de skill-prueba

- v0.9: se elimino scripts/borrado-historico.sh (mudado a otra skill). Historia, no rotura.
- v0.8: la guia vieja references/solo-en-historia.md quedo documentada aqui y en ningun lado mas.
EOF

cat > "$SKILL/SKILL.md" <<'EOF'
---
name: skill-prueba
description: banco de autoprueba del detector de referencias
---

# Skill de prueba

<!-- skill v1.0 · en el sello historico se retiro references/fantasma-comentario.md del paquete -->

El motor vive en scripts/vivo.sh con apoyo de scripts/motor.py y la guia en references/guia.md.
Las configuraciones se cargan todas desde assets/*.json al arrancar.
Los utilitarios de la carpeta scripts/ corren solos.
Herramienta de la hermana skill-hermana: ~/.claude/skills/skill-hermana/scripts/util.sh
Su portada: ~/.claude/skills/skill-hermana/SKILL.md y la propia ~/.claude/skills/skill-prueba/SKILL.md
Forma corta valida: skill-hermana/references/corta.md
Forma corta rota: skill-hermana/references/corta-rota.md
Pieza de hermana que falta: ~/.claude/skills/skill-hermana/scripts/no-existe.sh
Utilidad externa del taller: ~/taller/scripts/externo.sh
Utilidad externa que falta: ~/taller/scripts/no-esta.sh
Skill que no esta en el arsenal: ~/.claude/skills/skill-inexistente/scripts/x.sh
Portada fantasma: ~/.claude/skills/skill-fantasmagorica/SKILL.md
Referencia rota de verdad: references/rota-real.md
Cita imprecisa que vive en la hermana: references/vive-en-hermana.md
Cita con colision de nombres: references/compartida.md
Cita cuya duena nadie nombra: references/de-otra.md
El archivo palabra-suelta.md se menciona aqui sin ruta y eso no es una cita.
La bitacora completa esta en references/changelog.md.
EOF

# --- Correr el inventario contra el sandbox (HOME redirigido: cero contacto con el arsenal real) ---
OUT="$T/salida.txt"
HOME="$FAKE_HOME" bash "$INV" "$SKILL" > "$OUT" 2>&1

bloque() {  # extrae las lineas indentadas que siguen a un encabezado del informe
  awk -v m="$1" 'index($0,m){f=1;next} f&&/^    /{print;next} f{exit}' "$OUT"
}
B_ROTAS=$(bloque "Mencionadas pero NO existen")
B_HUERF=$(bloque "Existen pero nadie las menciona")
B_HERM=$(bloque "viven en otra skill")
B_DUD=$(bloque "DUDOSOS:")
B_SIS_ROTA=$(bloque "skills hermanas que NO existen")
B_SIS_OK=$(bloque "skills hermanas verificadas")
B_INTRUSO=$(bloque "fuera de las carpetas canónicas")

PASAN=0; FALLAN=0
chk() {  # chk <descripcion> <0|1 esperado-encontrado> ...
  local desc="$1" cond="$2"
  if [ "$cond" -eq 1 ]; then echo "  PASA  $desc"; PASAN=$((PASAN+1));
  else echo "  FALLA $desc"; FALLAN=$((FALLAN+1)); fi
}
contiene() { printf '%s' "$1" | grep -qF -- "$2" && echo 1 || echo 0; }
no_contiene() { printf '%s' "$1" | grep -qF -- "$2" && echo 0 || echo 1; }
cuenta() { [ "$(printf '%s' "$1" | grep -c .)" -eq "$2" ] && echo 1 || echo 0; }

echo "== ASERCIONES (direccion 1: los falsos positivos NO se marcan, cada una en SU bloque) =="
chk "hermana OK: util.sh en el bloque VERIFICADAS"             "$(contiene "$B_SIS_OK" "skills/skill-hermana/scripts/util.sh")"
chk "hermana OK: util.sh NO en el bloque de hermanas ROTAS"    "$(no_contiene "$B_SIS_ROTA" "util.sh")"
chk "raiz de hermana: skills/skill-hermana/SKILL.md verificada" "$(contiene "$B_SIS_OK" "skills/skill-hermana/SKILL.md")"
chk "forma corta v1.7: corta.md en el bloque VERIFICADAS"      "$(contiene "$B_SIS_OK" "skills/skill-hermana/references/corta.md")"
chk "SKILL.md propio citado no cae en rotas"                   "$(no_contiene "$B_ROTAS" "SKILL.md")"
chk "tilde: 1 ruta externa verificada en el informe"           "$(contiene "$(cat "$OUT")" "1 ruta(s) externa(s) verificadas")"
chk "tilde: externo.sh NO en dudosos"                          "$(no_contiene "$B_DUD" "externo.sh")"
chk "comentario HTML: fantasma-comentario.md no en rotas"      "$(no_contiene "$B_ROTAS" "fantasma-comentario.md")"
chk "changelog: borrado-historico.sh no en rotas"              "$(no_contiene "$B_ROTAS" "borrado-historico.sh")"
chk "rescate EN_HERMANA: vive-en-hermana.md en el bloque info" "$(contiene "$B_HERM" "vive-en-hermana.md → existe en skill-hermana")"
chk "rescate EN_HERMANA: vive-en-hermana.md NO en rotas"       "$(no_contiene "$B_ROTAS" "vive-en-hermana.md")"
chk "huerfano por glob: config-a.json no es huerfana"          "$(no_contiene "$B_HUERF" "config-a.json")"
chk "huerfano por glob: config-b.json no es huerfana"          "$(no_contiene "$B_HUERF" "config-b.json")"
chk "huerfano por directorio: solo-por-dir.sh no es huerfana"  "$(no_contiene "$B_HUERF" "solo-por-dir.sh")"
chk "dir RELATIVO desde references/: t1.md no es huerfana"     "$(no_contiene "$B_HUERF" "plantillas-sub/t1.md")"
chk "citadas por ruta: vivo.sh, motor.py y guia.md no huerfanas" "$([ "$(contiene "$B_HUERF" "vivo.sh")" -eq 0 ] && [ "$(contiene "$B_HUERF" "motor.py")" -eq 0 ] && [ "$(contiene "$B_HUERF" "guia.md")" -eq 0 ] && echo 1 || echo 0)"

echo "== ASERCIONES (direccion 2: lo REALMENTE malo SI se marca, en SU bloque) =="
chk "rota REAL cazada: references/rota-real.md"                "$(contiene "$B_ROTAS" "references/rota-real.md")"
chk "rota citada en un .py cazada: references/rota-en-py.md"   "$(contiene "$B_ROTAS" "references/rota-en-py.md")"
chk "exactamente 2 rotas (ni mas ni menos)"                    "$(cuenta "$B_ROTAS" 2)"
chk "huerfano REAL cazado: references/huerfano-real.md"        "$(contiene "$B_HUERF" "references/huerfano-real.md")"
chk "palabra suelta NO salva: palabra-suelta.md es huerfana"   "$(contiene "$B_HUERF" "references/palabra-suelta.md")"
chk "mencion solo-historia NO salva: solo-en-historia.md huerfana" "$(contiene "$B_HUERF" "references/solo-en-historia.md")"
chk "exactamente 3 huerfanas (ni mas ni menos)"                "$(cuenta "$B_HUERF" 3)"
chk "hermana existente con archivo faltante: no-existe.sh ROTA" "$(contiene "$B_SIS_ROTA" "skills/skill-hermana/scripts/no-existe.sh")"
chk "forma corta rota cazada: corta-rota.md ROTA"              "$(contiene "$B_SIS_ROTA" "skills/skill-hermana/references/corta-rota.md")"
chk "exactamente 2 hermanas rotas"                             "$(cuenta "$B_SIS_ROTA" 2)"
chk "exactamente 3 hermanas verificadas"                       "$(cuenta "$B_SIS_OK" 3)"
chk "intruso examples/ marcado como ⚠️ mover a references/"    "$(contiene "$(cat "$OUT")" "mover a references/")"
chk "intruso examples/ listado en su bloque"                   "$(contiene "$B_INTRUSO" "examples")"
chk "intruso ya NO es 🔴"                                      "$(no_contiene "$(cat "$OUT")" "🔴 Material")"

echo "== ASERCIONES (direccion 3: la duda va a DUDOSOS, con conteo exacto) =="
chk "skills/ a carpeta inexistente → dudoso"                   "$(contiene "$B_DUD" "skill-inexistente")"
chk "externa faltante → dudoso: no-esta.sh"                    "$(contiene "$B_DUD" "no-esta.sh")"
chk "SKILL.md de skill fantasma → dudoso"                      "$(contiene "$B_DUD" "skill-fantasmagorica")"
chk "colision multi-hermana → dudoso con lista: compartida.md" "$(contiene "$B_DUD" "compartida.md → existe en 2 hermanas")"
chk "colision multi-hermana NO degradada a info"               "$(no_contiene "$B_HERM" "compartida.md")"
chk "duena unica sin nombrar → dudoso: de-otra.md"             "$(contiene "$B_DUD" "de-otra.md → existe solo en skill-otra")"
chk "duena unica sin nombrar NO degradada a info"              "$(no_contiene "$B_HERM" "de-otra.md")"
chk "DUDOSOS: 5 exacto"                                        "$(contiene "$(cat "$OUT")" "DUDOSOS: 5")"

echo ""
echo "AUTOPRUEBA: $PASAN pasan, $FALLAN fallan (de $((PASAN+FALLAN)))"
if [ "$FALLAN" -gt 0 ]; then
  echo "--- salida completa del inventario para diagnostico ---"
  cat "$OUT"
  exit 1
fi
exit 0
