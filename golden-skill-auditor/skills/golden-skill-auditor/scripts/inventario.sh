#!/bin/bash
# inventario.sh — radiografía determinista de una skill antes de auditarla.
# Uso: bash inventario.sh <ruta-de-la-skill>
# Solo lee; nunca modifica nada.
#
# v1.14 — QUINTA ronda adversarial (v1.13 NO RATIFICADA: la clase "regla en una rama,
# ausente en la gemela" reapareció por CUARTA vez). Esta ronda NO parchea puntos:
# CENTRALIZA — que sea imposible repetir la clase porque solo existe UNA puerta:
#   A. UN SOLO EXTRACTOR de rutas: extrae_rutas() — los 6 puntos de extracción de la
#      v1.13 (REF/ROOT/GLOB/DIR/RELDIR/ESPACIOS) pasan por la misma función y TODOS los
#      patrones se construyen con FRONT/FRONT_DURA. El punto que quedó sin frontera en
#      v1.13 (la cobertura por directorio: "ad-assets/imagenes/" fabricaba la cobertura
#      "assets/imagenes/") ya no puede divergir: no hay otra puerta.
#   B. UNA SOLA COMPARACIÓN de rutas: compara_ruta() con IZQ/DER SIEMPRE (modo mencion)
#      y frontera de segmento garantizada (modo prefijo). El rescate contra el citante
#      comparaba por grep -qF crudo (motor.sh.viejo resolvía a motor.sh) y la cobertura
#      por directorio comparaba con prefijo pelado.
#   C. UN SOLO find: busca() = find -L siempre, stderr recogido (jamás tragado). El
#      blindaje ATRAVIESA symlinks: el verificador escribió dentro de una skill
#      "Blindada 5 de 5" vía enlace — con -L el nodo se evalúa por su DESTINO
#      (verificado empírico 2026-08-22: find -L -flags +uchg y -perm +0200 miran el
#      archivo real detrás del enlace).
#   D. POLÍTICA DE STDERR: en la RUTA DE DATOS del informe está prohibido 2>/dev/null.
#      Un archivo ilegible (chmod 000) produce "🔴 N archivos NO LEÍDOS — informe
#      parcial" con la lista, y NINGÚN verde se imprime pelado sobre lo no leído
#      (verde_o_parcial). El stderr de find va a un registro que el informe declara.
#   E. CLASIFICADOR DE TOKENS endurecido: normaliza_token() colapsa //, ./ y seg/..
#      léxicamente ANTES de clasificar, y sister_valida() rechaza ".", "..", "~",
#      vacío y nombres con / como candidatos a hermana ([ -d "$SKILLS_ROOT/." ] siempre
#      es verdadero — falsos rojos VIVOS medidos 2026-08-22: golden-investigacion-mercado
#      con skills/../references/scraping-firecrawl.md en rojo EXISTIENDO y baoyu-design
#      con 4). "../x" y "./x" se resuelven contra el DIR DEL CITANTE (../references
#      desde scripts/ = la raíz de la skill), en las DOS direcciones (rotas y huérfanos).
#   F5. GUARDIA DE SHELL COMPLETA: /bin/sh de macOS es bash 3.2 en modo POSIX con
#      BASH_VERSION definido — la guardia vieja no re-ejecutaba y el informe salía
#      TRUNCADO tras BLINDAJE sin aviso (la sustitución de procesos <(...) es error de
#      sintaxis en POSIX; medido 2026-08-22). Ahora el modo POSIX se detecta por
#      SHELLOPTS y se re-ejecuta /bin/bash.
#   F6. SECRETOS con ALCANCE DECLARADO: familias nuevas (PEM PRIVATE KEY, sk-ant-,
#      AKIA, EAA de Meta, act_+dígitos, contraseña/clave en español, +57), conteo N
#      total (si se trunca: "mostrando 5 de N"), filtro anti-falso-positivo de base64
#      de imagen, y el verde SIEMPRE declara qué cubre y qué NO — nunca verde absoluto.
#   F8. MODO PLUGIN: raíz con .claude-plugin/plugin.json o marketplace.json = REPO
#      PLUGIN — no se exige SKILL.md raíz (se cuentan las sub-skills skills/*/SKILL.md)
#      y los archivos estándar de plugin no son intrusos.
#   Menores: description en CARACTERES reales (sin la clave, sin el literal ">-", sin
#   indentación — medido en esta misma skill: 1361 impresos vs 1290 reales); claves
#   raíz con dígito (version2:) cierran la description; sin frontmatter se declara
#   "SIN FRONTMATTER" (jamás se pesca del cuerpo); .ts entra a TEXT_EXTS (corrección
#   fechada 2026-08-22 del claim "cero .ts" del changelog v1.10: hay 47 alcanzables
#   con find -L en el arsenal — el claim viejo midió sin -L); el tamaño de binarios se
#   informa en BYTES reales (stat -f%z), no en bloques de du; el blindaje chmod MIXTO
#   (algunos nodos sin escritura) es ⚠️ informativo, no 🔴 (un repo con 3 archivos
#   read-only de 241 no es un blindaje parcial — caso claude-ads).

# C9-guardia (v1.12): bajo zsh el `for x in $LISTA` NO hace word-splitting y TEXT_EXTS queda
# como UN token — lista_texto no encuentra nada, no hay texto vivo, y el informe sale VERDE
# MENTIROSO de punta a punta (medido: zsh inventario.sh daba verde total). Si el shell no es
# bash, re-exec con bash o morir gritando: jamás un verde falso por shell equivocado.
if [ -z "${BASH_VERSION:-}" ]; then
  if command -v bash >/dev/null 2>&1; then
    exec bash "$0" "$@"
  fi
  echo "ERROR: este script exige bash (otro shell produce un informe verde FALSO) y no hay bash en PATH" >&2
  exit 97
fi
# F5 (v1.14): /bin/sh de macOS ES bash (3.2) en modo POSIX y define BASH_VERSION, así que
# la guardia de arriba no lo caza — y en POSIX la sustitución de procesos `< <(...)` es
# error de sintaxis: el informe moría TRUNCADO justo tras BLINDAJE, sin aviso (medido
# 2026-08-22 con `sh inventario.sh`). El modo POSIX se delata en SHELLOPTS; se re-ejecuta
# /bin/bash UNA vez (GSA_REEXEC corta el bucle si hasta esa re-ejecución cayera en POSIX).
case ":${SHELLOPTS:-}:" in
  *:posix:*)
    if [ "${GSA_REEXEC:-0}" != "1" ] && [ -x /bin/bash ]; then
      GSA_REEXEC=1 exec /bin/bash "$0" "$@"
    fi
    echo "ERROR: bash en modo POSIX (sh) trunca el informe y no pude re-ejecutar /bin/bash" >&2
    exit 97
    ;;
esac
# Ya en bash pleno: limpiar el marcador para que NO se herede a procesos hijos (un
# `sh inventario.sh` lanzado desde aquí debe poder re-ejecutarse él también).
unset GSA_REEXEC 2>/dev/null || true

set -u

SKILL_PATH="${1:-}"
if [ -z "$SKILL_PATH" ] || [ ! -d "$SKILL_PATH" ]; then
  echo "ERROR: pasa la ruta de la skill. Uso: bash inventario.sh ~/.claude/skills/<nombre>" >&2
  exit 1
fi

# Resolver symlink para leer el contenido real
REAL_PATH=$(cd "$SKILL_PATH" && pwd -P)
SKILL_NAME=$(basename "$SKILL_PATH")

# F6 (v1.11): LA lista de formatos de texto — UNA sola decisión compartida por el barrido
# de referencias (lista_texto), el árbol ARCHIVOS y las SEÑALES Golden. Antes cada bloque
# tenía la suya y divergían. Agregar un formato = tocar SOLO esta línea y sembrar su caso
# en el banco (regla: toda corrección entra con su sabotaje en la suite).
# v1.14: entra .ts — corrección fechada 2026-08-22 del claim "cero .ts en el arsenal"
# (v1.10): ese censo corrió find SIN -L; con find -L hay 47 .ts alcanzables. Mismo
# criterio que .js. (SINTAXIS no lo valida: node --check no compila TypeScript.)
TEXT_EXTS="md txt py sh js ts json css html xml yaml yml liquid csv"
# F3 (v1.11): tr '[:upper:]' '[:lower:]' NO pliega acentos en locale C — BITÁCORA.md no
# casaba la rama es_historia y revivía el falso rojo. Pliegue explícito del set español
# (bytes UTF-8 literales vía sed, funciona en locale C y UTF-8) además del tr; se usa en
# TODO sitio que compare en minúsculas.
minusculas() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/Á/á/g;s/É/é/g;s/Í/í/g;s/Ó/ó/g;s/Ú/ú/g;s/Ñ/ñ/g;s/Ü/ü/g'
}
# C6 (v1.12): la extensión se compara EN MINÚSCULAS — un references/GUIA.MD o un roto.SH
# eran invisibles en cuatro superficies. Aquí vía minusculas() y en cada busca vía -iname.
es_texto() {
  et_ext=$(minusculas "${1##*.}")  # C6-minusculas-ext
  case " $TEXT_EXTS " in
    *" $et_ext "*) return 0 ;;
    *) return 1 ;;
  esac
}
# F9 (v1.11): cut -c corta por BYTES y parte caracteres multibyte (mojibake real impreso
# sobre all-deploy) — truncado seguro por CARACTERES con python3, que ya es dependencia
# de este script (ast.parse en SINTAXIS).
trunca() {
  python3 -X utf8 -c 'import sys
n = int(sys.argv[1])
sys.stdin.reconfigure(errors="replace")
for l in sys.stdin:
    print(l.rstrip("\n")[:n])' "$1"
}

# =====================================================================
# D (v1.14) — POLÍTICA DE STDERR EN LA RUTA DE DATOS: prohibido 2>/dev/null.
# Lo que no se pudo leer se REGISTRA y el informe lo declara; un verde sobre datos
# a medio leer es un veredicto, no cobertura.
# =====================================================================
NO_LEIDOS_F=$(mktemp)     # archivos que la ruta de datos no pudo leer (chmod 000, etc.)
ERR_RECORRIDO=$(mktemp)   # stderr acumulado de los find (bucles de symlinks, permisos)
EXTRACT_ERR=$(mktemp)     # fallas del extractor perl — el informe las grita
# C (v1.14) — UN SOLO find: TODA búsqueda pasa por aquí. -L SIEMPRE (symlinks se evalúan
# por su DESTINO: el blindaje, el texto, los secretos y los intrusos los atraviesan) y el
# stderr se acumula, jamás se traga.
busca() { find -L "$@" 2>>"$ERR_RECORRIDO"; }
# D: filtro de legibilidad para las listas de la ruta de datos — lo ilegible se registra
# con su ruta relativa (registra-no-leido), jamás se salta en silencio.
solo_legibles() {
  while IFS= read -r sl_f; do
    if [ -r "$sl_f" ]; then
      printf '%s\n' "$sl_f"
    else
      printf '%s\n' "${sl_f#"$REAL_PATH"/}" >> "$NO_LEIDOS_F"   # registra-no-leido
    fi
  done
}
# D: un verde jamás se imprime pelado si quedaron archivos sin leer.
verde_o_parcial() {
  if [ -s "$NO_LEIDOS_F" ]; then
    vp_n=$(sort -u "$NO_LEIDOS_F" | grep -c .)
    echo "⚠️ ${1#✅ } — SOLO en lo leído ($vp_n archivo(s) sin leer, informe parcial)"
  else
    echo "$1"
  fi
}

echo "==================================================="
echo "INVENTARIO: $SKILL_NAME"
echo "Ruta: $SKILL_PATH"
[ "$REAL_PATH" != "$SKILL_PATH" ] && echo "Symlink hacia: $REAL_PATH"
echo "==================================================="

# --- F8 (v1.14): modo plugin ---
# Un repo con .claude-plugin/plugin.json o marketplace.json en la raíz es un PLUGIN de
# Claude Code, no una skill suelta: el SKILL.md vive en cada sub-skill (skills/*/SKILL.md)
# y los archivos de repo (LICENSE, README, tests...) son estándar, no intrusos.
ES_PLUGIN=0; N_SUB=0
if [ -f "$REAL_PATH/.claude-plugin/plugin.json" ] || [ -f "$REAL_PATH/.claude-plugin/marketplace.json" ] || [ -f "$REAL_PATH/marketplace.json" ]; then
  ES_PLUGIN=1
  if [ -d "$REAL_PATH/skills" ]; then
    N_SUB=$(busca "$REAL_PATH/skills" -mindepth 2 -maxdepth 2 -name "SKILL.md" | wc -l | tr -d ' ')
  fi
  echo "MODO PLUGIN: REPO PLUGIN con $N_SUB sub-skill(s) en skills/*/SKILL.md (.claude-plugin presente)"
fi

# --- Blindaje ---
echo ""
echo "## BLINDAJE"
# C8 (v1.12): mirar UN inodo (ls -ldO de la raíz) afirmaba "Blindada" con los archivos
# internos sueltos. Se cuenta N de M nodos con uchg y solo M de M es "Blindada".
# C (v1.14): el conteo pasa por busca() (find -L) — el verificador escribió dentro de una
# skill "Blindada 5 de 5" vía SYMLINK a un archivo externo mutable; con -L el nodo se
# evalúa por su destino y ese agujero cuenta como nodo sin blindar.
# v1.14: el gemelo chmod MIXTO (algunos nodos read-only, la mayoría escribibles) baja a
# ⚠️ informativo — un repo con 3 archivos read-only de 241 no es un blindaje parcial
# (caso claude-ads); el blindaje deliberado de la casa es uchg y ese sí grita en rojo.
M_TOT=$(busca "$REAL_PATH" | wc -l | tr -d ' ')
N_UCHG=$(busca "$REAL_PATH" -flags +uchg | wc -l | tr -d ' ')  # C8-conteo-uchg
N_ESCR=$(busca "$REAL_PATH" -perm +0200 | wc -l | tr -d ' ')
if [ "$N_UCHG" -eq "$M_TOT" ] && [ "$M_TOT" -gt 0 ]; then
  echo "Blindada con chflags uchg — $N_UCHG de $M_TOT nodos (desbloquear: chflags -R nouchg)"
elif [ "$N_UCHG" -gt 0 ]; then
  echo "🔴 Blindaje PARCIAL: $N_UCHG de $M_TOT nodos con uchg — el resto se puede escribir (cerrar: chflags -R uchg)"
elif [ "$N_ESCR" -eq 0 ]; then
  echo "Blindada por permisos chmod — 0 de $M_TOT nodos escribibles (desbloquear: chmod -R u+w)"
elif [ "$N_ESCR" -lt "$M_TOT" ]; then
  echo "⚠️ Sin blindaje uchg; chmod mixto: $((M_TOT-N_ESCR)) de $M_TOT nodos sin escritura, $N_ESCR escribibles (no es blindaje completo; el estándar de la casa es chflags -R uchg)"
else
  echo "Sin blindaje (escribible)"
fi

# --- Árbol de archivos ---
echo ""
echo "## ARCHIVOS (con líneas)"
# C5 (v1.12): find -L — los SYMLINKS entran al listado (y al escaneo de texto, refs y
# secretos): SKILL.md promete seguirlos. Desde v1.14 vía busca() con stderr registrado.
# D (v1.14): la legibilidad se prueba AQUÍ para todo el árbol — un chmod 000 sale como
# 🔴 NO LEGIBLE, entra a NO_LEIDOS y degrada todos los verdes posteriores a "parcial".
TOTAL_FILES=0
while IFS= read -r f; do
  TOTAL_FILES=$((TOTAL_FILES+1))
  rel="${f#"$REAL_PATH"/}"
  if [ ! -r "$f" ]; then
    printf "  %-60s %6s\n" "$rel" "🔴 NO LEGIBLE"
    printf '%s\n' "$rel" >> "$NO_LEIDOS_F"   # registra-no-leido
  elif es_texto "$f"; then  # F6: misma lista TEXT_EXTS que el barrido de referencias
    lines=$(wc -l < "$f" | tr -d ' ')
    printf "  %-60s %6s líneas\n" "$rel" "$lines"
  else
    # v1.14: bytes REALES (stat -f%z), no bloques de du — un archivo de 1 byte decía 4.0K
    size=$(stat -f%z "$f" 2>>"$ERR_RECORRIDO" || wc -c < "$f" | tr -d ' ')
    printf "  %-60s %6s B (binario)\n" "$rel" "$size"
  fi
done < <(busca "$REAL_PATH" -type f ! -name ".DS_Store" | sort)
echo "  Total: $TOTAL_FILES archivos (symlinks que resuelven incluidos)"
# C5: bajo find -L lo que sigue siendo -type l es un symlink que NO resuelve
LN_ROTOS=$(busca "$REAL_PATH" -type l | sed "s|^$REAL_PATH/||")
if [ -n "$LN_ROTOS" ]; then
  echo "⚠️ Symlinks que NO resuelven (destino inexistente):"
  echo "$LN_ROTOS" | sed 's/^/    /'
fi

# --- SKILL.md ---
echo ""
echo "## SKILL.MD"
SKILL_MD="$REAL_PATH/SKILL.md"
if [ ! -f "$SKILL_MD" ]; then
  if [ "$ES_PLUGIN" -eq 1 ]; then
    echo "Modo plugin: sin SKILL.md raíz — $N_SUB sub-skill(s) llevan el suyo en skills/*/SKILL.md (no es CRÍTICO en un plugin)"
  else
    echo "🔴 CRÍTICO: no existe SKILL.md"
  fi
else
  LINES=$(wc -l < "$SKILL_MD" | tr -d ' ')
  echo "Líneas: $LINES $([ "$LINES" -gt 500 ] && echo '⚠️ >500 (revisar jerarquía)')"
  # v1.14: name y description salen SOLO del frontmatter (sin frontmatter se declara, jamás
  # se pesca del cuerpo), la description se mide en CARACTERES reales (sin la clave, sin el
  # literal ">-"/"|" y sin indentación — el conteo viejo por bytes daba 1361 donde hay 1290)
  # y C7 cierra también en claves raíz CON dígito (version2:).
  FM_OUT=$(python3 -X utf8 - "$SKILL_MD" <<'PYEOF'
import sys, re
lines = [l.rstrip('\r') for l in open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\n')]
if not lines or lines[0].strip() != '---':
    print("SINFM\t\t"); sys.exit()
fm = []
cerrado = False
for l in lines[1:]:
    if l.strip() == '---':
        cerrado = True
        break
    fm.append(l)
if not cerrado:
    print("SINFM\t\t"); sys.exit()
key = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):(.*)$')  # C7: claves raíz con dígito cierran
vals = {}
cur = None
for l in fm:
    m = key.match(l)  # C7-corte-clave
    if m:
        cur = m.group(1)
        v = m.group(2).strip()
        vals[cur] = [] if v in ('>-', '>', '|', '|-', '>+', '|+') else [v]
    elif cur is not None and (l.startswith(' ') or not l.strip()):
        vals[cur].append(l.strip())
name = ' '.join(x for x in vals.get('name', []) if x).strip()
desc = ' '.join(x for x in vals.get('description', []) if x).strip()
print("OK\t%s\t%d" % (name, len(desc)))
PYEOF
)
  FM_ST=$(printf '%s' "$FM_OUT" | cut -f1)
  if [ "$FM_ST" != "OK" ]; then
    echo "🔴 SIN FRONTMATTER: name y description no declarados (no se pescan del cuerpo)"
  else
    NAME_FM=$(printf '%s' "$FM_OUT" | cut -f2)
    DESC_CHARS=$(printf '%s' "$FM_OUT" | cut -f3)
    echo "name: '$NAME_FM' $([ "$NAME_FM" != "$SKILL_NAME" ] && echo "⚠️ NO coincide con la carpeta '$SKILL_NAME'")"
    echo "description: ~$DESC_CHARS caracteres (reales: sin clave, sin marcador de bloque, sin indentación)"
  fi
fi

# --- Referencias rotas y huérfanas ---
echo ""
echo "## REFERENCIAS CRUZADAS"
# v1.14 — QUINTA ronda: CENTRALIZAR (ver cabecera). Historia de las rondas previas:
# v1.12 — B1 glob amplio respeta barras; B2 FRONTERA IZQUIERDA compartida (FRONT+PFX);
#   B3 prefijos de VARIABLE como clase; B4 resolución SIMÉTRICA de rotas (citante → raíz
#   → sufijo interno → hermanas); C5 symlinks con find -L; C6 mayúsculas; C7 description;
#   C8 blindaje N de M; C9 guardia de shell; C10 límites declarados.
# v1.11 — F1 glob no cruza barras y el amplio no exime; F2 normalización simétrica de
#   prefijos en limpia_texto; F3 pliegue español; F5c límite derecho de mención; F6
#   TEXT_EXTS unificada; F7 es_fixture solo en self-audit; F8 verde de huérfanos declara
#   la duda; F9 truncado por caracteres; F12 rutas con espacios.
# v1.10 — identidad por substring muerta (nombra_duena, es_historia/es_fixture anclados,
#   rescate por ruta completa, URLs fuera); token desnudo no exime; es_yo; tripwire de
#   paridad banco↔detector; letras del español en rutas.
# v1.9/v1.8 — multi-formato, citas relativas al citante, colisión de nombres, historia,
#   fixtures, cross-skill, ~, dir/glob, comentarios HTML, changelogs.
# Huérfanos: un archivo solo es huérfano si ninguna mención con la ruta COMPLETA lo nombra
# en el texto VIVO (sin historia, sin comentarios, sin fixtures, sin URLs, sin el propio
# auditor) Y ningún directorio específico/glob citado lo cubre.
# Regla de duda (mandato 2026-08-20): ante duda NO se marca rojo — se cuenta en DUDOSOS.
RAW_LIVE=$(mktemp); MENT_LIVE=$(mktemp); EXISTING=$(mktemp); SISTER=$(mktemp)
EXTERN_OK=$(mktemp); DUDOSO_F=$(mktemp); PAT_DIR=$(mktemp); PAT_GLOB=$(mktemp)
LIVE_TXT=$(mktemp); PAT_ACC=$(mktemp); PAT_NAKED=$(mktemp); STRIP_DIR=$(mktemp -d)
PAT_GLOB0=$(mktemp); PAT_GLOBB=$(mktemp)
SKILLS_ROOT="$HOME/.claude/skills"
REAL_NAME=$(basename "$REAL_PATH")
# (n) letras del español en rutas — clase de bytes UTF-8 literales.
ACC='áéíóúñüÁÉÍÓÚÑÜ'
# B2 (v1.12): FRONTERA IZQUIERDA compartida — el segmento canónico solo abre cita si lo
# precede inicio, espacio, backtick, comilla, paréntesis o el / de un prefijo que también
# es ruta; JAMÁS un guion o letra pegada ("./ad-assets/x.png" no pare assets/x.png).
# FRONT_DURA (v1.14) tampoco admite el / — para patrones que arrancan una ruta COMPLETA.
# PFX exige que todo segmento de prefijo TERMINE en / (ad- pegado no es prefijo de nada).
FRONT="(?<![A-Za-z0-9._~${ACC}-])"
FRONT_DURA="(?<![A-Za-z0-9._~/${ACC}-])"
PFX="(?:[A-Za-z0-9._~${ACC}-]*/)*"
REF_RE="${FRONT}(${PFX}(?:references|scripts|assets|agents)/[A-Za-z0-9._/${ACC}-]+\.[A-Za-z0-9]+)"
GLOB_RE="${FRONT}(${PFX}(?:references|scripts|assets|agents)/[A-Za-z0-9._/${ACC}-]*\*[A-Za-z0-9._/*${ACC}-]*)"
# (d) la raíz de una hermana no tiene segmento canónico: patrón propio para skills/<otra>/SKILL.md
ROOT_RE="${FRONT}(${PFX}skills/[A-Za-z0-9._${ACC}-]+/SKILL\.md)"
# A (v1.14): la cobertura por DIRECTORIO citado también lleva FRONT — este era el punto
# sin frontera de la v1.13: "ad-assets/imagenes/" en prosa fabricaba la cobertura
# "assets/imagenes/" y eximía huérfanos ajenos.
#   El lookahead también rechaza "/": "references//x.md" es una CITA de archivo (con //
#   que la normalización colapsa), no una cita de la carpeta "references/".
DIR_RE="${FRONT}((?:references|scripts|assets|agents)(?:/[A-Za-z0-9._${ACC}-]+)*/)(?![A-Za-z0-9._*/${ACC}-])"
# (b) citas de directorio RELATIVAS al archivo que cita (frontera DURA: arranca la ruta)
RELDIR_RE="${FRONT_DURA}((?:[A-Za-z0-9._${ACC}-]+/)+)(?![A-Za-z0-9._*/${ACC}-])"
# F12: rutas con espacios solo cuentan entre backticks/comillas (la comilla es la frontera)
ESP_RE="[\`\\x22\\x27]([A-Za-z0-9._~/${ACC}-]*(?:references|scripts|assets|agents)/[A-Za-z0-9._/ ${ACC}-]+\\.[A-Za-z0-9]+)[\`\\x22\\x27]"

# =====================================================================
# A (v1.14) — UN SOLO EXTRACTOR: toda extracción de rutas del texto pasa por esta
# puerta. No existe otro perl/grep de extracción en el script: es imposible extraer
# sin frontera porque solo hay una puerta y todos sus patrones nacen de FRONT/FRONT_DURA.
# $1=tipo (ref|root|glob|dir|reldir|espacios)  $2=archivo (omitir o "-" = stdin)
# Falla de perl → se registra en EXTRACT_ERR y el informe la grita (jamás verde callado).
# =====================================================================
extrae_rutas() {
  case "$1" in
    ref)      er_re="$REF_RE" ;;
    root)     er_re="$ROOT_RE" ;;
    glob)     er_re="$GLOB_RE" ;;
    dir)      er_re="$DIR_RE" ;;
    reldir)   er_re="$RELDIR_RE" ;;
    espacios) er_re="$ESP_RE" ;;
    *) echo "tipo desconocido: $1" >> "$EXTRACT_ERR"; return 9 ;;
  esac
  # OJO: delimitador m{...} porque el patrón está lleno de "/" (con m/.../ perl muere —
  # y tragar ese stderr volvería el informe un verde mentiroso: rc y stderr se registran).
  if [ "${2:--}" = "-" ]; then
    perl -ne "while (m{$er_re}g){print \"\$1\\n\"}" || { echo "extracción $1 (stdin) falló" >> "$EXTRACT_ERR"; return 1; }
  else
    perl -ne "while (m{$er_re}g){print \"\$1\\n\"}" "$2" || { echo "extracción $1 sobre $2 falló" >> "$EXTRACT_ERR"; return 1; }
  fi
}

# =====================================================================
# B (v1.14) — UNA SOLA COMPARACIÓN de rutas. Modo "mencion": búsqueda en texto con
# límites IZQ/DER SIEMPRE (el rescate contra el citante comparaba con grep -qF crudo y
# "motor.sh.viejo" resolvía una cita de motor.sh). Modo "prefijo": pertenencia bajo un
# directorio con frontera de SEGMENTO garantizada (el prefijo se cierra en / sí o sí).
# =====================================================================
# Límites de la mención (m7/m8; v1.11 endureció el DERECHO): a la izquierda no puede venir
# pegado un carácter de ruta (ni "/" en citas locales); a la derecha no puede seguir ni
# alfanumérico ni ".alfanumérico" — references/guia.md.bak NO salva a references/guia.md.
IZQ_LOCAL='(^|[^A-Za-z0-9._~/-])'
IZQ_ABS='(^|[^A-Za-z0-9._~-])'
DER_RUTA='([^A-Za-z0-9.]|\.([^A-Za-z0-9.]|$)|$)'
compara_ruta() {
  cr_modo="$1"; shift
  case "$cr_modo" in
    mencion)  # $1=archivo-limpio $2=ruta $3=1 si se permite "/" a la izquierda (forma abs)
      cr_esc=$(printf '%s' "$2" | sed -e 's/[][\.*^$(){}+?|]/\\&/g')
      if [ "${3:-0}" -eq 1 ]; then cr_izq="$IZQ_ABS"; else cr_izq="$IZQ_LOCAL"; fi
      grep -Eq "${cr_izq}${cr_esc}${DER_RUTA}" "$1"
      ;;
    prefijo)  # $1=ruta-relativa $2=directorio (se garantiza la / final: sin prefijo crudo)
      cr_dir="$2"
      case "$cr_dir" in */) : ;; *) cr_dir="$cr_dir/" ;; esac
      case "$1" in "$cr_dir"*) return 0 ;; *) return 1 ;; esac
      ;;
    *) echo "🔴 compara_ruta: modo desconocido '$cr_modo'" >&2; return 2 ;;
  esac
}

# =====================================================================
# E (v1.14) — CLASIFICADOR DE TOKENS endurecido.
# normaliza_token: colapso LÉXICO (sin tocar disco) de //, ./ y seg/../ — la cita
# "skills/../references/x.md" ES "references/x.md" (falsos rojos vivos medidos:
# golden-investigacion-mercado 1, baoyu-design 4 — los 5 destinos EXISTÍAN).
# El "../" inicial se conserva: se resuelve contra el DIR DEL CITANTE más abajo.
# =====================================================================
normaliza_token() {
  printf '%s\n' "$1" | perl -pe '
    s{/{2,}}{/}g;                                          # nt-dobles: // no es un segmento
    s{(?<=/)\./}{}g;                                       # nt-punto: ./ interno sobra
    1 while s{(?:^|(?<=/))(?!\.\.(?:/|$))[^/]+/\.\./}{};   # nt-colapso: seg/../ se cancela
    s{^\./}{};                                             # nt-punto-inicial
  '
}
# E: el MISMO colapso léxico aplicado al texto entero de las copias de mención — la cita
# "skills/../references/x.md" o "references//x.md" debe SALVAR a x.md de huérfana igual
# que salva de rota (simetría de las dos direcciones, la lección de todas las rondas).
normaliza_texto() {
  perl -pe '
    s{/{2,}}{/}g;
    s{(?<=/)\./}{}g;
    1 while s{(?:^|(?<=/))(?!\.\.(?:/|$))[^/]+/\.\./}{};
  '
}
# E: JAMÁS aceptar ".", "..", "~", vacío o algo con / como NOMBRE de skill hermana —
# [ -d "$SKILLS_ROOT/." ] y [ -d "$SKILLS_ROOT/.." ] son verdaderos SIEMPRE y fabricaban
# hermanas fantasma en rojo.
sister_valida() {
  case "$1" in ""|.|..|"~"|*/*) return 1 ;; *) return 0 ;; esac
}

# (h) exención ANCLADA — nombre base sin extensión, en minúsculas (F3: pliegue con minusculas()).
base_ancla() { b=$(basename "$1"); b="${b%.*}"; minusculas "$b"; }
# PARIDAD (l): las ramas de estos case se extraen textualmente en autoprueba_inventario.sh;
# si agregas o cambias una alternativa aquí, actualiza el MANIFIESTO del banco o el banco grita.
es_historia() {
  case "$(base_ancla "$1")" in
    changelog|changelog[-_.]*|bitacora|bitacora[-_.]*|bitácora|bitácora[-_.]*|historial|historial[-_.]*)
      return 0 ;;
    *)
      return 1 ;;
  esac
}
# (f) bancos de autoprueba: siembran rutas rotas a propósito — no son refs vivas.
# F7 (v1.11): la exención es del banco PROPIO del auditor — solo aplica en contexto
# self-audit (ES_SELF_AUDIT). Los selftest/autoprueba de OTRAS skills son scripts reales.
es_fixture() {
  [ "${ES_SELF_AUDIT:-0}" -eq 1 ] || return 1
  case "$(base_ancla "$1")" in
    autoprueba|autoprueba[-_.]*|selftest|selftest[-_.]*|fixture|fixtures|fixture[-_.]*|fixtures[-_.]*)
      return 0 ;;
    *)
      return 1 ;;
  esac
}
# (k) autoexclusión: en un self-audit las cadenas del propio inventario.sh no son menciones.
SELF_INV="$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")"
# F7: contexto self-audit = este mismo inventario.sh vive dentro de la skill auditada.
case "$SELF_INV" in
  "$REAL_PATH"/*) ES_SELF_AUDIT=1 ;;
  *) ES_SELF_AUDIT=0 ;;
esac
es_yo() {
  d=$(cd "$(dirname "$1")" 2>/dev/null && pwd -P) || return 1
  [ "$d/$(basename "$1")" = "$SELF_INV" ]
}
lista_texto() {  # (a)(m) todo formato de texto donde viva una cita — la lista es TEXT_EXTS (F6)
  # C5+C (v1.14): vía busca() (find -L, stderr registrado); D: lo ilegible a NO_LEIDOS.
  # C6 (v1.12): -iname — un .MD o .SH en mayúsculas es el mismo formato.
  lt_args=(); lt_first=1
  for lt_e in $TEXT_EXTS; do
    if [ "$lt_first" -eq 1 ]; then lt_first=0; else lt_args+=(-o); fi
    lt_args+=(-iname "*.${lt_e}")
  done
  busca "$REAL_PATH" -type f \( "${lt_args[@]}" \) | solo_legibles | sort
}
# (i) texto limpio: fuera comentarios HTML y fuera URLs (esquema://...) — lo que vive dentro
# de una URL no es una cita local, no salva huérfanos y no fabrica rotas.
# F2 (v1.11): normalización COMPARTIDA de prefijos de citación en la ÚNICA función por la
# que pasa el texto de las DOS direcciones (rotas Y huérfanos).
GSA_PFX_SELF1="$REAL_PATH/"; export GSA_PFX_SELF1
GSA_PFX_SELF2=""; case "$SKILL_PATH" in /*) GSA_PFX_SELF2="$SKILL_PATH/" ;; esac
export GSA_PFX_SELF2
# B3 (v1.12): la CLASE completa de prefijos de variable. ${HOME}/$HOME se RESUELVEN de
# verdad; cualquier OTRO $VAR/, ${VAR}/ o <VAR>/ pegado al segmento canónico se marca
# gsavar-VAR/ y el clasificador lo resuelve contra la skill → hermanas → DUDOSOS, jamás rojo.
# D (v1.14): sin 2>/dev/null — si perl no pudo leer el archivo, se registra como NO LEÍDO.
limpia_texto() {
  perl -0777 -pe '
    s/<!--.*?-->//gs;
    s{[A-Za-z][A-Za-z0-9+.\-]*://[^]\s\x22\x27<>)]*}{}g;
    s/\$\{?HOME\}?(?=\/)/$ENV{HOME}/g;  # norm-prefijo home resuelto de verdad
    s/\$([A-Za-z_][A-Za-z0-9_]*)\/(?=(?:references|scripts|assets|agents)\/)/gsavar-$1\//g;   # norm-var-generica
    s/\$\{([A-Za-z_][A-Za-z0-9_]*)\}\/(?=(?:references|scripts|assets|agents)\/)/gsavar-$1\//g; # norm-var-generica
    s/<([A-Za-z_][A-Za-z0-9_]*)>\/(?=(?:references|scripts|assets|agents)\/)/gsavar-$1\//g;   # norm-var-generica
    for my $p ($ENV{GSA_PFX_SELF1}, $ENV{GSA_PFX_SELF2}) {
      next unless defined $p and length $p > 5;
      s/\Q$p\E//g;
    }
  ' "$1" || printf '%s\n' "${1#"$REAL_PATH"/}" >> "$NO_LEIDOS_F"
}

# Texto VIVO consolidado (sin historia, sin fixtures, sin el propio auditor, sin comentarios,
# sin URLs): de aquí salen las refs, los patrones de cobertura y la mención de hermanas.
while IFS= read -r f; do
  es_historia "$f" && continue
  es_fixture "$f" && continue
  es_yo "$f" && continue
  limpia_texto "$f" >> "$LIVE_TXT"
  printf '\n' >> "$LIVE_TXT"
  # (b) citas de directorio RELATIVAS al archivo que cita: solo si el dir existe de verdad
  fdirrel=$(dirname "${f#"$REAL_PATH"/}")
  limpia_texto "$f" | extrae_rutas reldir - | \
    sort -u | while IFS= read -r cand; do
      [ -z "$cand" ] && continue
      if [ "$fdirrel" = "." ]; then res="$cand"; else res="$fdirrel/$cand"; fi
      [ -d "$REAL_PATH/${res%/}" ] && echo "${res%/}/" >> "$PAT_ACC"
    done
done < <(lista_texto)

# A: extracción de citas y raíces de hermana — por la única puerta.
extrae_rutas ref  "$LIVE_TXT" >> "$RAW_LIVE"
extrae_rutas root "$LIVE_TXT" >> "$RAW_LIVE"

# F12 (v1.11): rutas con ESPACIOS — solo entre backticks/comillas. La que existe queda viva;
# la citada que NO existe va a DUDOSOS y no a rojas (entre comillas también vive prosa).
GSA_ESPACIOS=1
if [ "$GSA_ESPACIOS" -eq 1 ]; then
  extrae_rutas espacios "$LIVE_TXT" \
    | sort -u | while IFS= read -r sp; do
      case "$sp" in *" "*) : ;; *) continue ;; esac
      spx="$sp"; case "$spx" in "~"*) spx="$HOME${spx#\~}" ;; esac
      if [ -e "$REAL_PATH/$sp" ] || [ -e "$spx" ]; then
        :
      else
        echo "$sp → ruta con espacios citada que no existe (confirmar a mano)" >> "$DUDOSO_F"
      fi
    done
fi

# Cobertura por directorio (anclado a la raíz, CON frontera desde v1.14) y glob citados
extrae_rutas dir "$LIVE_TXT" >> "$PAT_ACC"
# (j) separar cobertura: token DESNUDO (carpeta canónica pelada) aparte — no exime, solo duda.
sort -u "$PAT_ACC" | grep -E '^(references|scripts|assets|agents)/$' > "$PAT_NAKED" || true
sort -u "$PAT_ACC" | grep -Ev '^(references|scripts|assets|agents)/$' > "$PAT_DIR" || true
extrae_rutas glob "$LIVE_TXT" | grep -oE "(references|scripts|assets|agents)/[A-Za-z0-9._/*${ACC}-]*" | sort -u > "$PAT_GLOB0" || true
# F1 (v1.11): un glob AMPLIO de carpeta (termina en /* sin más ancla) NO exime en silencio.
grep -E '/\*$' "$PAT_GLOB0" > "$PAT_GLOBB" || true
grep -Ev '/\*$' "$PAT_GLOB0" > "$PAT_GLOB" || true

while IFS= read -r tok; do
  # E (v1.14): normalizar ANTES de clasificar — skills/../references/x ES references/x.
  tok=$(normaliza_token "$tok")
  [ -z "$tok" ] && continue
  case "$tok" in
    gsavar-*/*)
      # B3: cita con prefijo de variable ($VAR/, ${VAR}/, <VAR>/). Se resuelve primero
      # contra la PROPIA skill; si no, hermanas; si no → DUDOSOS. Nunca rojo.
      gv="${tok#gsavar-}"; gvar="${gv%%/*}"; gvrest="${gv#*/}"
      if [ -e "$REAL_PATH/$gvrest" ]; then
        echo "$gvrest"
      else
        gvhit=""
        for gd in "$SKILLS_ROOT"/*/; do
          [ -d "$gd" ] || continue
          gdn=$(basename "$gd")
          { [ "$gdn" = "$SKILL_NAME" ] || [ "$gdn" = "$REAL_NAME" ]; } && continue
          [ -e "$gd$gvrest" ] && { gvhit="$gdn"; break; }
        done
        if [ -n "$gvhit" ]; then
          echo "\$${gvar}/$gvrest → prefijo de variable; existe en la hermana $gvhit (confirmar a mano)" >> "$DUDOSO_F"
        else
          echo "\$${gvar}/$gvrest → prefijo de variable sin resolver (no existe en la skill ni en hermanas; confirmar a mano)" >> "$DUDOSO_F"
        fi
      fi
      ;;
    ../*)  # rama-sube (E v1.14)
      # cita relativa que SUBE (../x): se deja ENTERA en el flujo local y la escalera B4
      # la prueba contra el dir de cada citante (scripts/foo.sh citando ../references/x.md
      # = references/x.md de la raíz). Nota de redundancia DECLARADA: sister_valida (abajo)
      # es la última línea si esta rama faltara — el banco sabotea ambas por separado.
      echo "$tok"
      ;;
    *skills/*/*)
      after="${tok##*skills/}"; sister="${after%%/*}"; rest="${after#*/}"
      if [ "$sister" = "$SKILL_NAME" ] || [ "$sister" = "$REAL_NAME" ]; then
        echo "$rest"
      elif ! sister_valida "$sister"; then
        # E: ".", "..", "~", vacío o similar NO es un nombre de hermana — al flujo local
        # con su parte canónica (la escalera B4 decide), jamás hermana fantasma en rojo.
        rest2=$(printf '%s\n' "$tok" | grep -oE "(references|scripts|assets|agents)/[A-Za-z0-9._/${ACC}-]+\.[A-Za-z0-9]+" | head -1)
        if [ -n "$rest2" ]; then echo "$rest2"; else echo "$tok → token con forma skills/ irregular (confirmar a mano)" >> "$DUDOSO_F"; fi
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
      # v1.7 (NO regresar): forma CORTA de hermana (nombre-de-hermana + carpeta canónica +
      # archivo, sin prefijo skills). E (v1.14): el candidato pasa por sister_valida —
      # basename ".." de un prefijo "../" ya no fabrica la hermana fantasma "..".
      rest=$(echo "$tok" | grep -oE "(references|scripts|assets|agents)/[A-Za-z0-9._/${ACC}-]+\.[A-Za-z0-9]+")
      pre="${tok%"$rest"}"; pre="${pre%/}"; cand=$(basename "$pre" 2>/dev/null || true)
      if [ -n "$cand" ] && sister_valida "$cand" && [ "$cand" != "$SKILL_NAME" ] && [ "$cand" != "$REAL_NAME" ] \
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

# C5 (v1.12): find -L — un symlink que RESUELVE es un archivo existente, no una rota.
{ for exd in references scripts assets agents; do
    [ -d "$REAL_PATH/$exd" ] || continue
    (cd "$REAL_PATH" && busca "$exd" -type f ! -name ".DS_Store")
  done
  [ -f "$REAL_PATH/SKILL.md" ] && echo "SKILL.md"; } | sort -u > "$EXISTING"

# (i)(k) copias limpias del texto vivo, con el dir relativo de cada citante — B4 las
# necesita para resolver una cita contra el directorio del CITANTE. El marcador
# gsavar-VAR/ se descuenta: una cita $VAR/references/x.md que resolvió contra la skill
# también salva a x.md de huérfana (el beneficio es del archivo).
: > "$STRIP_DIR/indice"
n_strip=0
while IFS= read -r tf; do
  es_historia "$tf" && continue
  es_fixture "$tf" && continue
  es_yo "$tf" && continue
  n_strip=$((n_strip+1))
  limpia_texto "$tf" | sed -E 's|gsavar-[A-Za-z0-9_]+/||g' | normaliza_texto > "$STRIP_DIR/$n_strip"
  printf '%s\t%s\n' "$n_strip" "${tf#"$REAL_PATH"/}" >> "$STRIP_DIR/indice"
done < <(lista_texto)

# (g) la dueña debe estar NOMBRADA con límites de palabra: ni "cro" dentro de "sincroniza"
# ni copywriting dentro de golden-copywriting. Guion y guion bajo son parte del nombre.
nombra_duena() {
  for dn in $1; do
    esc=$(printf '%s' "$dn" | sed -e 's/[][\.*^$(){}+?|]/\\&/g')
    grep -Eq "(^|[^A-Za-z0-9_-])${esc}([^A-Za-z0-9_-]|\$)" "$LIVE_TXT" && return 0
  done
  return 1
}

# Rotas: citadas en texto vivo sin archivo local. B4 (v1.12) — resolución SIMÉTRICA:
# (a) dir del CITANTE, (b) raíz, (b2) sufijo interno → DUDOSO, (c) hermanas — y solo si
# TODO falla es roja. B (v1.14): la mención del citante se compara por compara_ruta con
# límites IZQ/DER — grep -qF crudo dejaba que "motor.sh.viejo" resolviera motor.sh.
resuelve_contra_citante() {  # B4-rescate-citante: $1=ruta citada — 0 si un citante la resuelve
  rcc_b="$1"
  while IFS=$'\t' read -r rcc_idx rcc_tfrel; do
    rcc_dir=$(dirname "$rcc_tfrel")
    [ "$rcc_dir" = "." ] && continue
    [ -e "$REAL_PATH/$rcc_dir/$rcc_b" ] || continue
    compara_ruta mencion "$STRIP_DIR/$rcc_idx" "$rcc_b" 0 && return 0
  done < "$STRIP_DIR/indice"
  return 1
}
BROKEN=""; EN_HERMANA=""
while IFS= read -r b; do
  [ -z "$b" ] && continue
  resuelve_contra_citante "$b" && continue   # (a) el citante la resuelve → viva
  [ -e "$REAL_PATH/$b" ] && continue         # (b) la raíz la resuelve (symlink o fuera de EXISTING)
  # (b2) gemelo intra-skill de EN_HERMANA: la ruta citada COMPLETA existe como sufijo (con
  # frontera de segmento, jamás por base pelada) en OTRA carpeta de la MISMA skill — cita
  # imprecisa, no rotura clara → DUDOSO (regla de la duda).
  hit_interno=$(busca "$REAL_PATH" -path "*/$b" ! -path "*/.git/*" | head -1)  # B4-sufijo-interno
  if [ -n "$hit_interno" ]; then
    echo "$b → no está donde la cita dice, pero existe en la misma skill: ${hit_interno#"$REAL_PATH"/} (cita imprecisa, confirmar a mano)" >> "$DUDOSO_F"
    continue
  fi
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
  elif [ "$n_duenas" -eq 1 ] && nombra_duena "$duenas"; then
    EN_HERMANA="${EN_HERMANA}${b} → existe en ${duenas}
"
  elif [ "$n_duenas" -eq 1 ]; then
    echo "$b → existe solo en $duenas pero el texto no la nombra (confirmar a mano)" >> "$DUDOSO_F"
  else
    echo "$b → existe en $n_duenas hermanas ($duenas): cita ambigua, confirmar a mano" >> "$DUDOSO_F"
  fi
done < <(comm -23 "$MENT_LIVE" "$EXISTING")

# F1 (v1.11): el * de un glob NO cruza barras — comparación SEGMENTO a segmento.
glob_matches() {  # $1=glob $2=ruta relativa
  gm_g="$1"; gm_p="$2"
  while :; do
    gm_gs="${gm_g%%/*}"; gm_ps="${gm_p%%/*}"
    case "$gm_ps" in
      $gm_gs) : ;;
      *) return 1 ;;
    esac
    case "$gm_g" in
      */*)
        case "$gm_p" in */*) : ;; *) return 1 ;; esac
        gm_g="${gm_g#*/}"; gm_p="${gm_p#*/}" ;;
      *)
        case "$gm_p" in */*) return 1 ;; *) return 0 ;; esac ;;
    esac
  done
}

# (i) una mención solo salva si casa la RUTA RELATIVA COMPLETA (dir + base) con límites:
#   - tal cual desde la raíz de la skill (references/x.md),
#   - o con "./" explícito (./references/x.md),
#   - o en forma absoluta de ESTA skill (skills/<esta>/references/x.md),
#   - o resuelta desde el directorio del citante (sub/x.md citado desde references/guia.md),
#   - o SUBIENDO desde el citante con ../ (E v1.14: ../references/x.md citado desde
#     scripts/ nombra a references/x.md de la raíz — tantos ../ como segmentos tenga el
#     dir del citante).
#   La base pelada no salva (palabra suelta ≠ cita) y la ruta de OTRA carpeta tampoco.
ORPHAN=""
while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  [ "$rel" = "SKILL.md" ] && continue
  es_historia "$rel" && continue
  salvado=0
  while IFS=$'\t' read -r idx tfrel; do
    [ "$tfrel" = "$rel" ] && continue  # autoexclusion del rescate: citarse a si mismo no salva
    sf="$STRIP_DIR/$idx"
    if compara_ruta mencion "$sf" "$rel" 0 \
       || compara_ruta mencion "$sf" "./$rel" 0 \
       || compara_ruta mencion "$sf" "skills/$SKILL_NAME/$rel" 1 \
       || { [ "$REAL_NAME" != "$SKILL_NAME" ] && compara_ruta mencion "$sf" "skills/$REAL_NAME/$rel" 1; }; then
      salvado=1; break
    fi
    tfdir=$(dirname "$tfrel")
    if [ "$tfdir" != "." ]; then
      # rescate-ups (E v1.14): la cita ../ que sube desde el citante hasta la raíz
      ups=$(printf '%s' "$tfdir" | awk -F/ '{o="";for(i=1;i<=NF;i++)o=o"../";printf "%s",o}')
      if compara_ruta mencion "$sf" "${ups}${rel}" 0; then salvado=1; break; fi
      case "$rel" in
        "$tfdir"/*)
          relrel="${rel#"$tfdir"/}"
          case "$relrel" in
            */*)
              if compara_ruta mencion "$sf" "$relrel" 0 || compara_ruta mencion "$sf" "./$relrel" 0; then
                salvado=1; break
              fi
              ;;
          esac
          ;;
      esac
    fi
  done < "$STRIP_DIR/indice"
  [ "$salvado" -eq 1 ] && continue
  cubierto=0
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    # B (v1.14): pertenencia bajo directorio por compara_ruta (frontera de segmento
    # garantizada) — nada de prefijo crudo.
    if compara_ruta prefijo "$rel" "$p"; then cubierto=1; break; fi
  done < "$PAT_DIR"
  if [ "$cubierto" -eq 0 ]; then
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      if glob_matches "$p" "$rel"; then cubierto=1; break; fi
    done < "$PAT_GLOB"
  fi
  if [ "$cubierto" -eq 0 ]; then
    # F1: glob amplio de carpeta — NO exime, va a DUDOSOS para confirmar a mano.
    # B1 (v1.12): también aquí el * respeta las barras (glob_matches, segmento a segmento).
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      if glob_matches "$p" "$rel"; then
        echo "$rel → sin cita; cubierta solo por el glob amplio '$p' (no exime, confirmar a mano)" >> "$DUDOSO_F"
        cubierto=2; break
      fi
    done < "$PAT_GLOBB"
  fi
  if [ "$cubierto" -eq 0 ]; then
    # (j) token desnudo: NO exime — va a DUDOSOS para confirmar a mano
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      if compara_ruta prefijo "$rel" "$p"; then
        echo "$rel → sin cita; cubierta solo por el token desnudo '$p' (no exime, confirmar a mano)" >> "$DUDOSO_F"
        cubierto=2; break
      fi
    done < "$PAT_NAKED"
  fi
  [ "$cubierto" -eq 0 ] && ORPHAN="${ORPHAN}${rel}
"
done < "$EXISTING"

if [ -n "$BROKEN" ]; then
  echo "🔴 Mencionadas pero NO existen:"
  printf '%s' "$BROKEN" | sed 's/^/    /'
else
  verde_o_parcial "✅ Sin referencias rotas"
fi
if [ -n "$EN_HERMANA" ]; then
  echo "ℹ️ Citadas como locales pero viven en otra skill (afinar la cita; no es rotura):"
  printf '%s' "$EN_HERMANA" | sed 's/^/    /'
fi
if [ -n "$ORPHAN" ]; then
  echo "⚠️ Existen pero nadie las menciona (huérfanas potenciales):"
  printf '%s' "$ORPHAN" | sed 's/^/    /'
else
  # F8 (v1.11): el verde no puede afirmarse mientras haya archivos SIN CITA esperando
  # confirmación en DUDOSOS — eso sería un veredicto, no cobertura.
  N_SIN_CITA=$(sort -u "$DUDOSO_F" | grep -c "sin cita" || true)
  if [ "$N_SIN_CITA" -gt 0 ]; then
    echo "0 huérfanos confirmados · $N_SIN_CITA en duda (ver DUDOSOS)"
  else
    verde_o_parcial "✅ Sin archivos huérfanos"
  fi
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
# se publicaría al marketplace tal cual. No es rotura — ⚠️ ordenar, no 🔴 romper.
# F8 (v1.14): en modo plugin los archivos estándar de repo/plugin NO son intrusos.
INTRUSOS=$( (cd "$REAL_PATH" && busca . -maxdepth 1 -mindepth 1 \
  ! -name SKILL.md ! -name references ! -name scripts ! -name assets ! -name agents \
  ! -name ".DS_Store" ! -name ".git" ! -name "README.md" | sed 's|^\./||') | sort -u)
if [ "$ES_PLUGIN" -eq 1 ] && [ -n "$INTRUSOS" ]; then
  # OJO bash 3.2: dentro de $( ) los patrones de case llevan el paréntesis de APERTURA,
  # o el parser viejo confunde el ) del patrón con el cierre de la sustitución.
  INTRUSOS=$(printf '%s\n' "$INTRUSOS" | while IFS= read -r it; do
    case "$it" in
      (.claude-plugin|skills|commands|hooks|docs|tests|evals|.github|.gitignore|.gitattributes|LICENSE*|README*|CHANGELOG*|CODE_OF_CONDUCT*|CONTRIBUTING*|SECURITY*|SUPPORT*|CITATION*|NOTICE*|CLAUDE.md|AGENTS.md|marketplace.json|plugin.json|package.json|package-lock.json|requirements.txt|install.sh|install.ps1|uninstall.sh|uninstall.ps1) : ;;  # plugin-estandar
      (*) printf '%s\n' "$it" ;;
    esac
  done)
fi
if [ -n "$INTRUSOS" ]; then
  if [ "$ES_PLUGIN" -eq 1 ]; then
    echo "⚠️ Material NO estándar de plugin en la raíz (revisar a mano; lo estándar de repo/plugin ya se eximió):"
  else
    echo "⚠️ Material fuera de las carpetas canónicas (mover a references/ según estandares-golden.md):"
  fi
  echo "$INTRUSOS" | sed 's/^/    /'
else
  verde_o_parcial "✅ Sin material intruso en la raíz"
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
rm -f "$RAW_LIVE" "$MENT_LIVE" "$EXISTING" "$SISTER" "$EXTERN_OK" "$DUDOSO_F" "$PAT_DIR" "$PAT_GLOB" "$LIVE_TXT" "$PAT_ACC" "$PAT_NAKED" "$PAT_GLOB0" "$PAT_GLOBB"
rm -rf "$STRIP_DIR"

# --- Sintaxis de scripts ---
echo ""
echo "## SINTAXIS DE SCRIPTS"
# C5+C6: busca (find -L) e -iname + case en minúsculas. Los checkers (bash -n, ast.parse,
# node --check) sí silencian SU stderr: el veredicto lo lleva el rc y el archivo ya pasó
# el filtro de legibilidad — no es la ruta de datos del informe la que se calla.
# .ts se lista como texto pero NO se valida aquí (node --check no compila TypeScript).
FOUND_SCRIPTS=0
while IFS= read -r s; do
  FOUND_SCRIPTS=1
  rel="${s#"$REAL_PATH"/}"
  case "$(minusculas "$s")" in
    *.sh)  bash -n "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  🔴 $rel — error de sintaxis bash" ;;
    # ast.parse y no py_compile: py_compile escribe __pycache__ (falla en skills blindadas y deja basura)
    *.py)  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  🔴 $rel — error de sintaxis python" ;;
    *.js)  node --check "$s" 2>/dev/null && echo "  ✅ $rel" || echo "  ⚠️ $rel — node --check falló o node no disponible" ;;
  esac
done < <(busca "$REAL_PATH" -type f \( -iname "*.sh" -o -iname "*.py" -o -iname "*.js" \) | solo_legibles | sort)
[ "$FOUND_SCRIPTS" -eq 0 ] && echo "  (sin scripts)"

# --- Señales de estándares Golden ---
echo ""
echo "## SEÑALES GOLDEN (verificar a mano las que marquen)"
# -F (cadena fija) evita que el grep de macOS confunda los bytes UTF-8 de ¿¡ con tildes.
# C5: el barrido va archivo por archivo sobre la lista de busca/lista_texto (los symlinks
# y las mayúsculas entran); D: sin 2>/dev/null — lo ilegible ya quedó en NO_LEIDOS.
APERTURA=$(while IFS= read -r sf; do
  grep -nHF '¿' "$sf"; grep -nHF '¡' "$sf"
done < <(lista_texto) | sed "s|^$REAL_PATH/||" | sort -u | head -5)
if [ -n "$APERTURA" ]; then
  echo "⚠️ Signos de apertura ¿ ¡ encontrados (primeros 5):"
  echo "$APERTURA" | trunca 120 | sed 's/^/    /'
else
  verde_o_parcial "✅ Sin signos de apertura ¿ ¡"
fi
# F6 (v1.14): secretos con FAMILIAS AMPLIADAS, conteo total y ALCANCE DECLARADO.
# Dos barridos: -i para las familias por palabra clave y sensible a mayúsculas para las
# familias por FORMA de token (AKIA/EAA/sk-ant/act_/PEM/+57 pierden su forma en -i).
# Anti-falso-positivo: los data URI de imagen (data:image, ;base64,) se excluyen — son
# blobs largos que casan cualquier patrón de valor y no son secretos.
SEC_RE_I='(api[_-]?key|token|password|secret|bearer)[ "'"'"':=]+[A-Za-z0-9_-]{16,}|(contraseña|contrasena|clave)[[:space:]]*[:=][[:space:]]*[^[:space:]]{6,}'
SEC_RE_S='-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-ant-[A-Za-z0-9_-]{10,}|AKIA[A-Z0-9]{16}|EAA[A-Za-z0-9]{40,}|act_[0-9]{8,}|\+57[ .]?[0-9]{10}'
SEC_ALL=$(mktemp)
while IFS= read -r sf; do
  # -e obligatorio: SEC_RE_S empieza con guiones y sin -e el grep lo comeria como opciones
  grep -nHiE -e "$SEC_RE_I" "$sf"
  grep -nHE -e "$SEC_RE_S" "$sf"
done < <(busca "$REAL_PATH" -type f ! -path "*/.git/*" | solo_legibles) \
  | grep -Ev 'data:image/|;base64,' | sed "s|^$REAL_PATH/||" | sort -u > "$SEC_ALL"
N_SEC=$(grep -c . "$SEC_ALL")
if [ "$N_SEC" -gt 5 ]; then
  echo "🔴 Posibles secretos hardcodeados — $N_SEC hallazgos (mostrando 5 de $N_SEC; verificar):"
  head -5 "$SEC_ALL" | trunca 120 | sed 's/^/    /'
elif [ "$N_SEC" -gt 0 ]; then
  echo "🔴 Posibles secretos hardcodeados — $N_SEC hallazgo(s) (verificar):"
  trunca 120 < "$SEC_ALL" | sed 's/^/    /'
else
  verde_o_parcial "✅ Sin patrones de secretos en las familias cubiertas"
fi
echo "    Alcance del barrido — CUBRE: api_key/token/password/secret/bearer con valor de 16+, contraseña/clave con : o =, bloque PEM PRIVATE KEY, sk-ant- (Anthropic), AKIA+16 (AWS), EAA de 43+ (Meta), act_+dígitos (cuenta publicitaria), +57 con 10 dígitos. NO CUBRE: JWT (eyJ...), ghp_/gho_ (GitHub), AIza (Google), claves OpenSSH sin cabecera PEM, secretos partidos en varias líneas, secretos ofuscados o en base64 (los data:image se excluyen a propósito)."
rm -f "$SEC_ALL"
# OJO con los acentos: una clase de corchetes con carácter multibyte, [oó], se rompe en el
# locale C. Con alternancia (o|ó) funciona en ambos locales.
if [ -f "$SKILL_MD" ]; then
  CHANGELOG=$(grep -m1 -iE '<!--[[:space:]]*skill[[:space:]]+(v[0-9]|[A-Z]{1,4}[0-9])|<!--.*(versi(o|ó)n|version)|\*\*versi(o|ó)n:?\*\*|^##[[:space:]]*changelog' "$SKILL_MD")
  if [ -n "$CHANGELOG" ]; then
    echo "✅ Versión/changelog: $(echo "$CHANGELOG" | trunca 100)"
  else
    echo "⚠️ Sin línea de versión/changelog bajo el H1"
  fi
elif [ "$ES_PLUGIN" -eq 1 ]; then
  echo "Modo plugin: versión/changelog se busca en el repo (CHANGELOG.md), no en SKILL.md raíz"
fi

# --- D (v1.14): cobertura de lectura — lo que el informe NO pudo leer se declara ---
echo ""
echo "## COBERTURA DE LECTURA"
if [ -s "$NO_LEIDOS_F" ]; then
  N_NL=$(sort -u "$NO_LEIDOS_F" | grep -c .)
  echo "🔴 $N_NL archivo(s) NO LEÍDOS — informe parcial (todo verde de arriba es solo sobre lo leído):"
  sort -u "$NO_LEIDOS_F" | sed 's/^/    /'
else
  echo "✅ Todos los archivos del árbol se pudieron leer"
fi
if [ -s "$EXTRACT_ERR" ]; then
  echo "🔴 ERROR del extractor de referencias — esa sección NO es confiable:"
  sort -u "$EXTRACT_ERR" | sed 's/^/    /'
fi
if [ -s "$ERR_RECORRIDO" ]; then
  echo "⚠️ Avisos del recorrido de archivos (stderr de find, declarado, no tragado):"
  sort -u "$ERR_RECORRIDO" | trunca 120 | sed 's/^/    /' | head -10
fi
rm -f "$NO_LEIDOS_F" "$ERR_RECORRIDO" "$EXTRACT_ERR"

echo ""
echo "=== Inventario completo. Ahora: Fase 1, leer TODOS los archivos. ==="
