#!/bin/bash
# autoprueba_inventario.sh — banco adversarial del detector de referencias de inventario.sh.
# Siembra en un TMPDIR (jamás en el arsenal real) un árbol con:
#   - las 5 clases de falso positivo que NO deben marcarse (cross-skill, ~, dir/glob,
#     comentario HTML, changelog), y un huérfano citado solo por glob/directorio,
#   - MÁS una referencia rota REAL y un huérfano REAL que SÍ deben marcarse
#     (un banco que no puede fallar no prueba nada).
# Corre inventario.sh contra el árbol con HOME redirigido al sandbox y verifica
# las dos direcciones. Sale 0 solo si TODAS las aserciones pasan.
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
mkdir -p "$SKILL/references" "$SKILL/scripts" "$SKILL/assets"
mkdir -p "$FAKE_HOME/.claude/skills/skill-hermana/scripts"
mkdir -p "$FAKE_HOME/taller/scripts"

echo "echo util" > "$FAKE_HOME/.claude/skills/skill-hermana/scripts/util.sh"   # clase 1: existe en la hermana
echo "echo externo" > "$FAKE_HOME/taller/scripts/externo.sh"                    # clase 2: existe tras expandir ~

echo "guia" > "$SKILL/references/guia.md"                 # citada por nombre: ni rota ni huerfana
echo "echo vivo" > "$SKILL/scripts/vivo.sh"               # citada por nombre
echo "{}" > "$SKILL/assets/config-a.json"                 # citada SOLO por glob assets/*.json
echo "{}" > "$SKILL/assets/config-b.json"                 # citada SOLO por glob assets/*.json
echo "echo solo" > "$SKILL/scripts/solo-por-dir.sh"       # citada SOLO por directorio scripts/
echo "huerfano" > "$SKILL/references/huerfano-real.md"    # huerfano REAL: nadie lo nombra

cat > "$SKILL/references/changelog.md" <<'EOF'
# Changelog de skill-prueba

- v0.9: se elimino scripts/borrado-historico.sh (mudado a otra skill). Historia, no rotura.
EOF

cat > "$SKILL/SKILL.md" <<'EOF'
---
name: skill-prueba
description: banco de autoprueba del detector de referencias
---

# Skill de prueba

<!-- skill v1.0 · en el sello historico se retiro references/fantasma-comentario.md del paquete -->

El motor vive en scripts/vivo.sh y la guia de uso en references/guia.md.
Las configuraciones se cargan todas desde assets/*.json al arrancar.
Los utilitarios de la carpeta scripts/ corren solos.
Herramienta de la hermana: ~/.claude/skills/skill-hermana/scripts/util.sh
Utilidad externa del taller: ~/taller/scripts/externo.sh
Referencia rota de verdad: references/rota-real.md
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

PASAN=0; FALLAN=0
chk() {  # chk <descripcion> <0|1 esperado-encontrado> ...
  local desc="$1" cond="$2"
  if [ "$cond" -eq 1 ]; then echo "  PASA  $desc"; PASAN=$((PASAN+1));
  else echo "  FALLA $desc"; FALLAN=$((FALLAN+1)); fi
}
contiene() { printf '%s' "$1" | grep -qF -- "$2" && echo 1 || echo 0; }
no_contiene() { printf '%s' "$1" | grep -qF -- "$2" && echo 0 || echo 1; }

echo "== ASERCIONES (direccion 1: los falsos positivos NO se marcan) =="
chk "clase 1 cross-skill: util.sh no aparece como ROTA"        "$(no_contiene "$(cat "$OUT")" "ROTA skills/skill-hermana")"
chk "clase 1 cross-skill: util.sh aparece verificada"          "$(contiene "$(cat "$OUT")" "skills/skill-hermana/scripts/util.sh")"
chk "clase 2 tilde: externo.sh no esta en rotas"               "$(no_contiene "$B_ROTAS" "externo.sh")"
chk "clase 2 tilde: ruta externa verificada en el informe"     "$(contiene "$(cat "$OUT")" "externa(s) verificadas")"
chk "clase 3 glob: assets/*.json no esta en rotas"             "$(no_contiene "$B_ROTAS" "assets/*")"
chk "clase 4 comentario HTML: fantasma-comentario no en rotas" "$(no_contiene "$B_ROTAS" "fantasma-comentario.md")"
chk "clase 5 changelog: borrado-historico no en rotas"         "$(no_contiene "$B_ROTAS" "borrado-historico.sh")"
chk "huerfano por glob: config-a.json no es huerfana"          "$(no_contiene "$B_HUERF" "config-a.json")"
chk "huerfano por glob: config-b.json no es huerfana"          "$(no_contiene "$B_HUERF" "config-b.json")"
chk "huerfano por directorio: solo-por-dir.sh no es huerfana"  "$(no_contiene "$B_HUERF" "solo-por-dir.sh")"
chk "citadas por nombre: vivo.sh y guia.md no son huerfanas"   "$([ "$(contiene "$B_HUERF" "vivo.sh")" -eq 0 ] && [ "$(contiene "$B_HUERF" "guia.md")" -eq 0 ] && echo 1 || echo 0)"
chk "sin dudosos en el banco (DUDOSOS: 0)"                     "$(contiene "$(cat "$OUT")" "DUDOSOS: 0")"

echo "== ASERCIONES (direccion 2: lo REALMENTE malo SI se marca) =="
chk "rota REAL cazada: references/rota-real.md"                "$(contiene "$B_ROTAS" "references/rota-real.md")"
chk "huerfano REAL cazado: references/huerfano-real.md"        "$(contiene "$B_HUERF" "references/huerfano-real.md")"
chk "exactamente 1 rota (ni mas ni menos)"                     "$([ "$(printf '%s' "$B_ROTAS" | grep -c .)" -eq 1 ] && echo 1 || echo 0)"
chk "exactamente 1 huerfana (ni mas ni menos)"                 "$([ "$(printf '%s' "$B_HUERF" | grep -c .)" -eq 1 ] && echo 1 || echo 0)"

echo ""
echo "AUTOPRUEBA: $PASAN pasan, $FALLAN fallan (de $((PASAN+FALLAN)))"
if [ "$FALLAN" -gt 0 ]; then
  echo "--- salida completa del inventario para diagnostico ---"
  cat "$OUT"
  exit 1
fi
exit 0
