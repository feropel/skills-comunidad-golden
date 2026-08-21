#!/bin/bash
# inventario.sh — radiografía determinista de una skill antes de auditarla.
# Uso: bash inventario.sh <ruta-de-la-skill>
# Solo lee; nunca modifica nada.

set -u

SKILL_PATH="${1:-}"
if [ -z "$SKILL_PATH" ] || [ ! -d "$SKILL_PATH" ]; then
  echo "ERROR: pasa la ruta de la skill. Uso: bash inventario.sh ~/.claude/skills/<nombre>" >&2
  exit 1
fi

# Resolver symlink para leer el contenido real
REAL_PATH=$(cd "$SKILL_PATH" && pwd -P)
SKILL_NAME=$(basename "$SKILL_PATH")

echo "==================================================="
echo "INVENTARIO: $SKILL_NAME"
echo "Ruta: $SKILL_PATH"
[ "$REAL_PATH" != "$SKILL_PATH" ] && echo "Symlink hacia: $REAL_PATH"
echo "==================================================="

# --- Blindaje ---
echo ""
echo "## BLINDAJE"
FLAGS=$(ls -ldO "$REAL_PATH" | awk '{print $5}')
if [ "$FLAGS" = "uchg" ]; then
  echo "Blindada con chflags uchg (desbloquear: chflags -R nouchg)"
elif [ ! -w "$REAL_PATH" ]; then
  echo "Blindada por permisos chmod (desbloquear: chmod -R u+w)"
else
  echo "Sin blindaje (escribible)"
fi

# --- Árbol de archivos ---
echo ""
echo "## ARCHIVOS (con líneas)"
TOTAL_FILES=0
while IFS= read -r f; do
  TOTAL_FILES=$((TOTAL_FILES+1))
  rel="${f#"$REAL_PATH"/}"
  case "$f" in
    *.md|*.txt|*.sh|*.py|*.js|*.json|*.css|*.html|*.yaml|*.yml|*.liquid|*.csv)
      lines=$(wc -l < "$f" | tr -d ' ')
      printf "  %-60s %6s líneas\n" "$rel" "$lines"
      ;;
    *)
      size=$(du -h "$f" | awk '{print $1}')
      printf "  %-60s %6s (binario)\n" "$rel" "$size"
      ;;
  esac
done < <(find "$REAL_PATH" -type f ! -name ".DS_Store" | sort)
echo "  Total: $TOTAL_FILES archivos"

# --- SKILL.md ---
echo ""
echo "## SKILL.MD"
SKILL_MD="$REAL_PATH/SKILL.md"
if [ ! -f "$SKILL_MD" ]; then
  echo "🔴 CRÍTICO: no existe SKILL.md"
else
  LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
  echo "Líneas: $LINES $([ "$LINES" -gt 500 ] && echo '⚠️ >500 (revisar jerarquía)')"
  NAME_FM=$(awk '/^name:/{sub(/^name:[ ]*/,""); print; exit}' "$SKILL_MD")
  echo "name: '$NAME_FM' $([ "$NAME_FM" != "$SKILL_NAME" ] && echo "⚠️ NO coincide con la carpeta '$SKILL_NAME'")"
  DESC_CHARS=$(awk '/^description:/{f=1} f&&/^---$/{exit} f{print}' "$SKILL_MD" | wc -c | tr -d ' ')
  echo "description: ~$DESC_CHARS caracteres"
fi

# --- Referencias rotas y huérfanas ---
echo ""
echo "## REFERENCIAS CRUZADAS"
# v1.9 — expediente del verificador adversarial cerrado (ronda 2026-08-21):
#   a) el escaneo VIVO ya no lee solo .md: barre .md .py .sh .json .liquid .html .csv
#      (misma decisión multi-formato que las señales Golden; una rota citada en el
#      comentario de un .py era invisible).
#   b) citas RELATIVAS desde dentro de references/ (caso golden-web: su guía de arte generativo
#      cita el subdirectorio de templates como ruta relativa a sí misma) se resuelven también
#      respecto del directorio del archivo que cita, y solo dan cobertura si el directorio existe.
#   c) colisión de nombres: una cita local rota solo se degrada a ℹ️ si la ruta existe en
#      EXACTAMENTE UNA hermana Y el texto vivo de la skill nombra a esa hermana; si no,
#      va a DUDOSOS con la lista de hermanas donde existe (66 rutas relativas viven en 2+
#      de las 91 skills; degradar por cualquier coincidencia tapaba rotas reales).
#   d) refs a la raíz de una hermana (skills/<otra>/SKILL.md) ahora se capturan y verifican.
#   e) SIMETRÍA de historia: el filtro que las rotas ya tenían (comentarios HTML +
#      changelog/bitácora) aplica también al rescate de huérfanos, y la mención que salva
#      a un archivo debe parecer RUTA ("/nombre.ext"), no una palabra suelta.
#   f) los bancos de prueba (*autoprueba*, *selftest*, *fixture*) citan rutas rotas a
#      propósito: sus citas no cuentan como refs vivas.
# v1.8 — cinco clases de falso positivo neutralizadas (autoevalúo 2026-08-19/20):
#   1 cross-skill: si la ruta citada existe en OTRA skill de ~/.claude/skills no es rotura
#     (el rescate hoy exige dueña única + mención por nombre, ver (c)).
#   2 rutas con ~: se expande el tilde ANTES de probar existencia.
#   3 cita por directorio ("scripts/") o glob ("assets/*.json"): cubre huérfanos, no exige archivo literal.
#   4 comentarios HTML <!-- ... -->: sellos de versión = historia, se quitan antes del escaneo vivo.
#   5 archivos changelog/bitácora/historial: son HISTORIA — sus menciones no cuentan como refs vivas
#     y ellos mismos no se marcan huérfanos.
# Huérfanos: un archivo solo es huérfano si ninguna mención con forma de ruta lo nombra en el
# texto VIVO (sin historia, sin comentarios, sin fixtures) Y ningún directorio/glob citado lo cubre.
# Regla de duda (mandato 2026-08-20): ante duda NO se marca rojo — se cuenta en DUDOSOS.
RAW_LIVE=$(mktemp); MENT_LIVE=$(mktemp); EXISTING=$(mktemp); SISTER=$(mktemp)
EXTERN_OK=$(mktemp); DUDOSO_F=$(mktemp); PAT_DIR=$(mktemp); PAT_GLOB=$(mktemp)
LIVE_TXT=$(mktemp); PAT_ACC=$(mktemp)
SKILLS_ROOT="$HOME/.claude/skills"
REAL_NAME=$(basename "$REAL_PATH")
REF_RE='[A-Za-z0-9._~/-]*(references|scripts|assets|agents)/[A-Za-z0-9._/-]+\.[A-Za-z0-9]+'
GLOB_RE='[A-Za-z0-9._~/-]*(references|scripts|assets|agents)/[A-Za-z0-9._/-]*\*[A-Za-z0-9._/*-]*'
# (d) la raíz de una hermana no tiene segmento canónico: patrón propio para skills/<otra>/SKILL.md
ROOT_RE='[A-Za-z0-9._~/-]*skills/[A-Za-z0-9._-]+/SKILL\.md'

es_historia() {
  case "$(basename "$1" | tr '[:upper:]' '[:lower:]')" in
    *changelog*|*bitacora*|*bitácora*|*historial*) return 0 ;;
    *) return 1 ;;
  esac
}
# (f) bancos de autoprueba: siembran rutas rotas a propósito — no son refs vivas
es_fixture() {
  case "$(basename "$1" | tr '[:upper:]' '[:lower:]')" in
    *autoprueba*|*selftest*|*fixture*) return 0 ;;
    *) return 1 ;;
  esac
}
lista_texto() {  # (a) todo formato de texto donde viva una cita, no solo .md
  find "$REAL_PATH" -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \
    -o -name "*.json" -o -name "*.liquid" -o -name "*.html" -o -name "*.csv" \) | sort
}

# Texto VIVO consolidado (sin historia, sin fixtures, sin comentarios HTML):
# de aquí salen las refs, los patrones de cobertura y la mención-por-nombre de hermanas.
while IFS= read -r f; do
  es_historia "$f" && continue
  es_fixture "$f" && continue
  perl -0777 -pe 's/<!--.*?-->//gs' "$f" 2>/dev/null >> "$LIVE_TXT"
  printf '\n' >> "$LIVE_TXT"
  # (b) citas de directorio RELATIVAS al archivo que cita: solo si el dir existe de verdad
  fdirrel=$(dirname "${f#"$REAL_PATH"/}")
  perl -0777 -pe 's/<!--.*?-->//gs' "$f" 2>/dev/null | \
    perl -ne 'while (/(?<![A-Za-z0-9._~\/-])((?:[A-Za-z0-9._-]+\/)+)(?![A-Za-z0-9._*-])/g){print "$1\n"}' | \
    sort -u | while IFS= read -r cand; do
      [ -z "$cand" ] && continue
      if [ "$fdirrel" = "." ]; then res="$cand"; else res="$fdirrel/$cand"; fi
      [ -d "$REAL_PATH/${res%/}" ] && echo "${res%/}/" >> "$PAT_ACC"
    done
done < <(lista_texto)

grep -oE "$REF_RE" "$LIVE_TXT" >> "$RAW_LIVE" || true
grep -oE "$ROOT_RE" "$LIVE_TXT" >> "$RAW_LIVE" || true

# Clase 3: directorios (anclados a la raíz) y globs citados — dan cobertura a huérfanos
perl -ne 'while (/((?:references|scripts|assets|agents)(?:\/[A-Za-z0-9._-]+)*\/)(?![A-Za-z0-9._*-])/g){print "$1\n"}' \
  "$LIVE_TXT" >> "$PAT_ACC"
sort -u "$PAT_ACC" > "$PAT_DIR"
grep -oE "$GLOB_RE" "$LIVE_TXT" | grep -oE '(references|scripts|assets|agents)/[A-Za-z0-9._/*-]*' | sort -u > "$PAT_GLOB"

while IFS= read -r tok; do
  case "$tok" in
    *skills/*/*)
      after="${tok##*skills/}"; sister="${after%%/*}"; rest="${after#*/}"
      if [ "$sister" = "$SKILL_NAME" ] || [ "$sister" = "$REAL_NAME" ]; then
        echo "$rest"
      elif [ ! -d "$SKILLS_ROOT/$sister" ]; then
        # dice skills/ pero esa carpeta no está en el arsenal: duda, no rojo
        echo "$tok" >> "$DUDOSO_F"
      elif [ -f "$SKILLS_ROOT/$sister/$rest" ]; then
        echo "OK skills/$sister/$rest" >> "$SISTER"
      else
        echo "ROTA skills/$sister/$rest" >> "$SISTER"
      fi
      ;;
    "~"*|/*)
      # Clase 2: ruta absoluta o con tilde — expandir ~ y probar el archivo real
      exp="$tok"; case "$exp" in "~"*) exp="$HOME${exp#\~}" ;; esac
      if [ -e "$exp" ]; then
        echo "$tok" >> "$EXTERN_OK"
      else
        echo "$tok" >> "$DUDOSO_F"
      fi
      ;;
    *)
      # v1.7 (NO regresar): forma CORTA de hermana (nombre-de-hermana + carpeta canónica + archivo, sin prefijo skills)
      # (caso real: el changelog de golden360 la usa y producía el mismo archivo
      # como ✅ hermana Y 🔴 rota-local a la vez — falso rojo medido 2026-08-11).
      rest=$(echo "$tok" | grep -oE '(references|scripts|assets|agents)/[A-Za-z0-9._/-]+\.[A-Za-z0-9]+')
      pre="${tok%"$rest"}"; pre="${pre%/}"; cand=$(basename "$pre" 2>/dev/null || true)
      if [ -n "$cand" ] && [ "$cand" != "$SKILL_NAME" ] && [ "$cand" != "$REAL_NAME" ] \
         && [ -d "$SKILLS_ROOT/$cand" ]; then
        if [ -f "$SKILLS_ROOT/$cand/$rest" ]; then
          echo "OK skills/$cand/$rest" >> "$SISTER"
        else
          echo "ROTA skills/$cand/$rest" >> "$SISTER"
        fi
      else
        echo "$rest"
      fi
      ;;
  esac
done < <(sort -u "$RAW_LIVE") | sort -u > "$MENT_LIVE"

{ (cd "$REAL_PATH" && find references scripts assets agents -type f ! -name ".DS_Store" 2>/dev/null)
  [ -f "$REAL_PATH/SKILL.md" ] && echo "SKILL.md"; } | sort -u > "$EXISTING"

# Rotas: citadas en texto vivo sin archivo local. Rescate (c): solo si la ruta existe en
# EXACTAMENTE UNA hermana Y el texto vivo de esta skill la nombra, se informa aparte
# (cita imprecisa, no rotura). Cualquier otra coincidencia cross-skill = DUDOSO con lista.
BROKEN=""; EN_HERMANA=""
while IFS= read -r b; do
  [ -z "$b" ] && continue
  duenas=""; n_duenas=0
  for d in "$SKILLS_ROOT"/*/; do
    [ -d "$d" ] || continue
    dn=$(basename "$d")
    { [ "$dn" = "$SKILL_NAME" ] || [ "$dn" = "$REAL_NAME" ]; } && continue
    if [ -f "$d$b" ]; then duenas="${duenas:+$duenas }$dn"; n_duenas=$((n_duenas+1)); fi
  done
  if [ "$n_duenas" -eq 0 ]; then
    BROKEN="${BROKEN}${b}
"
  elif [ "$n_duenas" -eq 1 ] && grep -qF -- "$duenas" "$LIVE_TXT"; then
    EN_HERMANA="${EN_HERMANA}${b} → existe en ${duenas}
"
  elif [ "$n_duenas" -eq 1 ]; then
    echo "$b → existe solo en $duenas pero el texto no la nombra (confirmar a mano)" >> "$DUDOSO_F"
  else
    echo "$b → existe en $n_duenas hermanas ($duenas): cita ambigua, confirmar a mano" >> "$DUDOSO_F"
  fi
done < <(comm -23 "$MENT_LIVE" "$EXISTING")

# Huérfanos (e): mismo filtro de historia que las rotas — la mención que salva debe estar en
# texto VIVO (sin changelogs, sin comentarios HTML, sin fixtures), venir de OTRO archivo, y
# parecer RUTA ("/nombre.ext"): una palabra suelta igual al nombre no es una cita.
ORPHAN=""
while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  [ "$rel" = "SKILL.md" ] && continue
  es_historia "$rel" && continue
  base=$(basename "$rel")
  salvado=0
  while IFS= read -r tf; do
    [ "$tf" = "$REAL_PATH/$rel" ] && continue
    es_historia "$tf" && continue
    es_fixture "$tf" && continue
    if perl -0777 -pe 's/<!--.*?-->//gs' "$tf" 2>/dev/null | grep -qF -- "/$base"; then
      salvado=1; break
    fi
  done < <(lista_texto)
  [ "$salvado" -eq 1 ] && continue
  cubierto=0
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    case "$rel" in "$p"*) cubierto=1; break ;; esac
  done < "$PAT_DIR"
  if [ "$cubierto" -eq 0 ]; then
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      case "$rel" in $p) cubierto=1; break ;; esac
    done < "$PAT_GLOB"
  fi
  [ "$cubierto" -eq 0 ] && ORPHAN="${ORPHAN}${rel}
"
done < "$EXISTING"

if [ -n "$BROKEN" ]; then
  echo "🔴 Mencionadas pero NO existen:"
  printf '%s' "$BROKEN" | sed 's/^/    /'
else
  echo "✅ Sin referencias rotas"
fi
if [ -n "$EN_HERMANA" ]; then
  echo "ℹ️ Citadas como locales pero viven en otra skill (afinar la cita; no es rotura):"
  printf '%s' "$EN_HERMANA" | sed 's/^/    /'
fi
if [ -n "$ORPHAN" ]; then
  echo "⚠️ Existen pero nadie las menciona (huérfanas potenciales):"
  printf '%s' "$ORPHAN" | sed 's/^/    /'
else
  echo "✅ Sin archivos huérfanos"
fi
if [ -s "$EXTERN_OK" ]; then
  N_EXT=$(sort -u "$EXTERN_OK" | grep -c .)
  echo "✅ $N_EXT ruta(s) externa(s) verificadas con ~ expandido"
fi
N_DUD=$(sort -u "$DUDOSO_F" | grep -c . || true)
echo "DUDOSOS: $N_DUD"
if [ "$N_DUD" -gt 0 ]; then
  sort -u "$DUDOSO_F" | sed 's/^/    /'
fi
# Material fuera de las 4 carpetas canónicas o suelto en la raíz (fuera de SKILL.md):
# se publicaría al marketplace tal cual. No es rotura — el estándar de casa manda ese
# material a references/ — así que es ⚠️ ordenar, no 🔴 romper.
INTRUSOS=$( (cd "$REAL_PATH" && find . -maxdepth 1 -mindepth 1 \
  ! -name SKILL.md ! -name references ! -name scripts ! -name assets ! -name agents \
  ! -name ".DS_Store" ! -name ".git" ! -name "README.md" 2>/dev/null | sed 's|^\./||') | sort -u)
if [ -n "$INTRUSOS" ]; then
  echo "⚠️ Material fuera de las carpetas canónicas (mover a references/ según estandares-golden.md):"
  echo "$INTRUSOS" | sed 's/^/    /'
else
  echo "✅ Sin material intruso en la raíz"
fi
SISTER_ROTA=$(grep '^ROTA ' "$SISTER" 2>/dev/null | sed 's/^ROTA //' | sort -u)
SISTER_OK=$(grep '^OK ' "$SISTER" 2>/dev/null | sed 's/^OK //' | sort -u)
if [ -n "$SISTER_ROTA" ]; then
  echo "🔴 Rutas a skills hermanas que NO existen:"
  echo "$SISTER_ROTA" | sed 's/^/    /'
fi
if [ -n "$SISTER_OK" ]; then
  N_OK=$(echo "$SISTER_OK" | wc -l | tr -d ' ')
  echo "✅ $N_OK referencia(s) a skills hermanas verificadas:"
  echo "$SISTER_OK" | sed 's/^/    /'
fi
rm -f "$RAW_LIVE" "$MENT_LIVE" "$EXISTING" "$SISTER" "$EXTERN_OK" "$DUDOSO_F" "$PAT_DIR" "$PAT_GLOB" "$LIVE_TXT" "$PAT_ACC"

# --- Sintaxis de scripts ---
echo ""
echo "## SINTAXIS DE SCRIPTS"
FOUND_SCRIPTS=0
while IFS= read -r s; do
  FOUND_SCRIPTS=1
  rel="${s#"$REAL_PATH"/}"
  case "$s" in
    *.sh)  bash -n "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  🔴 $rel — error de sintaxis bash" ;;
    # ast.parse y no py_compile: py_compile escribe __pycache__ (falla en skills blindadas y deja basura)
    *.py)  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  🔴 $rel — error de sintaxis python" ;;
    *.js)  node --check "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  ⚠️ $rel — node --check falló o node no disponible" ;;
  esac
done < <(find "$REAL_PATH" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) | sort)
[ "$FOUND_SCRIPTS" -eq 0 ] && echo "  (sin scripts)"

# --- Señales de estándares Golden ---
echo ""
echo "## SEÑALES GOLDEN (verificar a mano las que marquen)"
# -F (cadena fija) evita que el grep de macOS confunda los bytes UTF-8 de ¿¡ con tildes.
# Barre todo formato de texto donde puedan vivir plantillas, no solo .md.
TXT_INCLUDES=(--include='*.md' --include='*.txt' --include='*.json' --include='*.liquid' --include='*.html' --include='*.csv' --include='*.yaml' --include='*.yml')
APERTURA=$({ grep -rnF "${TXT_INCLUDES[@]}" '¿' "$REAL_PATH" 2>/dev/null; grep -rnF "${TXT_INCLUDES[@]}" '¡' "$REAL_PATH" 2>/dev/null; } | sort -u | head -5)
if [ -n "$APERTURA" ]; then
  echo "⚠️ Signos de apertura ¿ ¡ encontrados (primeros 5):"
  echo "$APERTURA" | cut -c1-120 | sed 's/^/    /'
else
  echo "✅ Sin signos de apertura ¿ ¡"
fi
SECRETS=$(grep -rniE '(api[_-]?key|token|password|secret|bearer)[ "'"'"':=]+[A-Za-z0-9_-]{16,}' "$REAL_PATH" --include="*" 2>/dev/null | grep -v '\.git' | head -5)
if [ -n "$SECRETS" ]; then
  echo "🔴 Posibles secretos hardcodeados (verificar):"
  echo "$SECRETS" | cut -c1-120 | sed 's/^/    /'
else
  echo "✅ Sin patrones de secretos"
fi
# OJO con los acentos: una clase de corchetes con carácter multibyte, [oó], se rompe en el
# locale C — y este script suele correr con LANG vacío, así que grep no cazaba «**Versión**» y
# reportaba "sin versión" a skills que SÍ la declaran (falso positivo medido el 2026-08-20 sobre
# golden-logistica-diaria, que declara GLD1.40). Con alternancia (o|ó) funciona en ambos locales.
# Formas que SÍ existen en el arsenal y hay que reconocer todas (equiparado al detector del
# censo el 2026-08-20, que cazaba dos que este no): **Versión** y **Versión:** con y sin dos
# puntos, <!-- skill v1.2, <!-- skill G4.3 · (prefijo de letras + número, sin la v), y ## Changelog.
CHANGELOG=$(grep -m1 -iE '<!--[[:space:]]*skill[[:space:]]+(v[0-9]|[A-Z]{1,4}[0-9])|<!--.*(versi(o|ó)n|version)|\*\*versi(o|ó)n:?\*\*|^##[[:space:]]*changelog' "$SKILL_MD" 2>/dev/null)
if [ -n "$CHANGELOG" ]; then
  echo "✅ Versión/changelog: $(echo "$CHANGELOG" | cut -c1-100)"
else
  echo "⚠️ Sin línea de versión/changelog bajo el H1"
fi

echo ""
echo "=== Inventario completo. Ahora: Fase 1, leer TODOS los archivos. ==="
