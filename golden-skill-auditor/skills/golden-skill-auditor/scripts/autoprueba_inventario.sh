#!/bin/bash
# autoprueba_inventario.sh — banco adversarial del detector de referencias de inventario.sh.
#
# MODO NORMAL (sin argumentos): siembra en un TMPDIR (jamás en el arsenal real) los árboles:
#   1. skill-prueba     — el banco principal (todas las clases de rota/huérfana/dudosa) +
#      el CORPUS DE REGRESIÓN REAL (casos copiados de skills reales; regla: cada ronda
#      añade al menos un caso real no elegido por el constructor).
#   2. skill-selfaudit  — contexto SELF-AUDIT (es_yo + es_fixture del banco propio).
#   3. skill-f8         — cero huérfanos confirmados PERO archivos sin cita en DUDOSOS
#      (el verde no puede imprimirse) + frontmatter con metadata y clave con dígito tras
#      la description (C7). Se corre bajo bash, ZSH (C9) y SH (F5: POSIX re-ejecuta solo).
#   4. skill-blind      — SOLO la raíz con chflags uchg (C8: PARCIAL 1 de M).
#   5. skill-blindlink  — v1.14, ANTI-VERDE de "Blindada": todo con uchg MENOS un symlink
#      a un archivo externo escribible — el blindaje debe atravesar el enlace (find -L) y
#      declarar PARCIAL, jamás "Blindada M de M" con el agujero abierto.
#   6. skill-000        — v1.14, ANTI-VERDE de lectura (D): un archivo chmod 000 produce
#      "🔴 N archivo(s) NO LEÍDOS — informe parcial" y degrada TODOS los verdes.
#   7. skill-secretos   — v1.14, ANTI-VERDE de secretos (F6): una familia por archivo
#      (PEM, sk-ant, AKIA, EAA, act_, contraseña/clave español, +57, api_key clásica),
#      el conteo N total con "mostrando 5 de N", y el anti-falso-positivo: un data URI
#      base64 de imagen NO debe sonar.
#   8. skill-plugin     — v1.14 (F8): raíz con .claude-plugin/plugin.json — encabezado
#      "REPO PLUGIN con N sub-skills", sin CRÍTICO por SKILL.md raíz, archivos estándar
#      de plugin eximidos del bloque de intrusos y el intruso REAL aún cazado.
# Corre inventario.sh con HOME redirigido al sandbox y sale 0 solo si TODAS las aserciones
# pasan. Cada aserción se ancla al BLOQUE del informe donde la señal debe aparecer
# (extractor bloque()), nunca al texto completo, y cada bloque lleva CONTEO EXACTO.
#
# F9 (v1.14) — BANCO HONESTO POR RAMA: cada clase declarada toca la RAMA REAL del
# detector (la centralización ayuda: extractor/comparador/find únicos — sabotear la
# puerta única tumba TODOS los casos que pasan por ella), y cada VEREDICTO VERDE del
# informe (sin rotas, sin huérfanos, sin secretos, blindada, sin intrusos, sin signos,
# todos leídos) tiene su caso construido para ENGAÑARLO que debe caer en rojo/⚠️
# (sección ANTI-VERDE abajo).
#
# PARIDAD banco↔detector: el banco extrae textualmente las ramas de los case de
# inventario.sh (clasificador de tokens, es_historia, es_fixture) y las compara contra el
# MANIFIESTO de abajo. Rama sin caso o caso sin rama = banco en rojo.
#
# MODO SABOTAJES (bash autoprueba_inventario.sh sabotajes [regex]): copia detector+banco a
# un tmpdir, aplica de a UNO los sabotajes conocidos y exige que el banco los TUMBE.
# El regex opcional filtra por nombre (p. ej. "s1[0-9] " o "s_fmt") para correr POR LOTES.
# REGLA DE LA CASA (v1.11): toda corrección nueva del detector entra con su sabotaje en
# ESTA suite, viva donde viva la corrección.
# Suite v1.14 (nuevos): s22 repuntado al parser python de description, s26 normaliza_token
# quitada (skills/.. vuelve a ser hermana fantasma), s27 sister_valida apagada, s28 el
# rescate del citante vuelve a grep -qF crudo (motor.sh.viejo resuelve motor.sh), s30 el
# registro de NO LEÍDOS callado (chmod 000 vuelve a dar verde), s31 familia AKIA quitada
# del barrido de secretos, s32 modo plugin quitado (CRÍTICO falso vuelve), s33 guardia
# POSIX quitada (sh trunca el informe), s35 DIR_RE sin frontera (ad-assets/imagenes/
# vuelve a fabricar cobertura), s36 rescate-ups quitado (../references desde scripts/
# deja de salvar), s_fmt_ts (.ts fuera de TEXT_EXTS).
#
# Uso: bash autoprueba_inventario.sh [sabotajes [regex]]   (idéntico bajo zsh y sh: guardia)

# C9-guardia: el mismo tratamiento que el detector.
if [ -z "${BASH_VERSION:-}" ]; then
  if command -v bash >/dev/null 2>&1; then
    exec bash "$0" "$@"
  fi
  echo "ERROR: el banco exige bash y no hay bash en PATH" >&2
  exit 97
fi
case ":${SHELLOPTS:-}:" in
  *:posix:*)
    if [ "${GSA_REEXEC:-0}" != "1" ] && [ -x /bin/bash ]; then
      GSA_REEXEC=1 exec /bin/bash "$0" "$@"
    fi
    echo "ERROR: banco bajo bash POSIX (sh) y no pude re-ejecutar /bin/bash" >&2
    exit 97
    ;;
esac
# Ya en bash pleno: limpiar el marcador para que el `sh inventario.sh` del caso F5
# (proceso hijo) pueda re-ejecutarse él tambien.
unset GSA_REEXEC 2>/dev/null || true

set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# SELF capturado en el nivel superior: bajo zsh, $0 DENTRO de una funcion es el nombre
# de la funcion (FUNCTION_ARGZERO) y el auto-copiado del modo sabotajes moria en silencio.
SELF_PATH="$SCRIPT_DIR/$(basename "$0")"
INV="$SCRIPT_DIR/inventario.sh"
[ -f "$INV" ] || { echo "FALLA: no encuentro inventario.sh junto a la autoprueba" >&2; exit 1; }

# =====================================================================
# MODO SABOTAJES
# =====================================================================
if [ "${1:-}" = "sabotajes" ]; then
  S_FILTRO="${2:-}"
  S_PASAN=0; S_FALLAN=0; S_SALTADOS=0
  sabotaje() {  # $1=nombre $2=sed sobre inventario.sh ('' = ninguno) $3=sed sobre el banco ('' = ninguno) $4=texto exigido en la salida ('' = solo exit!=0)
    if [ -n "$S_FILTRO" ] && ! printf '%s' "$1" | grep -qE -- "$S_FILTRO"; then
      S_SALTADOS=$((S_SALTADOS+1)); return
    fi
    W=$(mktemp -d)
    cp "$INV" "$W/inventario.sh"; cp "$SELF_PATH" "$W/autoprueba_inventario.sh"
    if [ -n "$2" ]; then
      cp "$W/inventario.sh" "$W/antes"; sed -i '' "$2" "$W/inventario.sh"
      if cmp -s "$W/antes" "$W/inventario.sh"; then
        echo "  FALLA $1 — el sed del sabotaje no aplicó (blanco desapareció del detector)"; S_FALLAN=$((S_FALLAN+1)); rm -rf "$W"; return
      fi
    fi
    if [ -n "$3" ]; then
      cp "$W/autoprueba_inventario.sh" "$W/antesb"; sed -i '' "$3" "$W/autoprueba_inventario.sh"
      if cmp -s "$W/antesb" "$W/autoprueba_inventario.sh"; then
        echo "  FALLA $1 — el sed del sabotaje no aplicó (blanco desapareció del banco)"; S_FALLAN=$((S_FALLAN+1)); rm -rf "$W"; return
      fi
    fi
    LOG="$W/log"
    bash "$W/autoprueba_inventario.sh" > "$LOG" 2>&1
    rc=$?
    if [ "$rc" -eq 0 ]; then
      echo "  FALLA $1 — el banco NO mordió (salió 0 con el detector saboteado)"; S_FALLAN=$((S_FALLAN+1))
    elif [ -n "$4" ] && ! grep -qF -- "$4" "$LOG"; then
      echo "  FALLA $1 — el banco falló pero sin el grito esperado ('$4')"; S_FALLAN=$((S_FALLAN+1))
    else
      echo "  PASA  $1 — el banco mordió (exit $rc)"; S_PASAN=$((S_PASAN+1))
    fi
    rm -rf "$W"
  }

  echo "== SABOTAJES: cada uno debe TUMBAR el banco =="
  sabotaje "s1 dueña única -eq 1 → -ge 1" 's/"$n_duenas" -eq 1 ] \&\& nombra_duena/"$n_duenas" -ge 1 ] \&\& nombra_duena/' '' ''
  sabotaje "s2 es_fixture apagado (fixtures cuentan como texto vivo)" '/^es_fixture()/,/^}/ s/return 0/return 1/' '' ''
  sabotaje "s3 autoexclusión del rescate quitada (citarse a sí mismo salva)" '/autoexclusion del rescate: citarse a si mismo no salva/d' '' ''
  sabotaje "s4 SKILL.md fuera de EXISTING y sin rescate de raíz (b)" 's/echo "SKILL.md"/true/;/# (b) la raíz la resuelve/d' '' ''
  sabotaje "s5 tripwire de paridad (manifiesto pierde una rama)" '' '/^\*skills\/\*\/\*	/d' 'rama sin caso'
  sabotaje "s6 es_yo apagado (las cadenas del propio detector salvan)" '/es_yo "\$/d' '' ''
  sabotaje "s7 límite derecho relajado (.bak vuelve a salvar al .md)" 's|^DER_RUTA=.*|DER_RUTA="([^A-Za-z0-9]\|$)"|' '' ''
  sabotaje "s8 límite izquierdo relajado (barra a la izquierda salva)" 's|^IZQ_LOCAL=.*|IZQ_LOCAL="(^\|[^A-Za-z0-9._~-])"|' '' ''
  sabotaje "s9 glob cruza barras (assets/*.json cubre assets/sub/deep.json)" 's|gm_g="\$1"; gm_p="\$2"|case "$2" in $1) return 0 ;; esac; gm_g="$1"; gm_p="$2"|' '' ''
  sabotaje "s10 pliegue español quitado (BITÁCORA.md deja de ser historia)" 's@ | sed .s/Á.*@@' '' ''
  sabotaje "s11 prefijo HOME sin resolver (\${HOME}/taller fabrica rota)" '/norm-prefijo/d' '' ''
  sabotaje "s12 rutas con espacios apagadas" 's/^GSA_ESPACIOS=1/GSA_ESPACIOS=0/' '' ''
  sabotaje "s13 glob amplio exime en silencio (sin línea a DUDOSOS)" '/cubierta solo por el glob amplio/d' '' ''
  sabotaje "s14 verde F8 mentiroso (la duda sin cita no frena el ✅)" 's/"\$N_SIN_CITA" -gt 0/"$N_SIN_CITA" -gt 99999/' '' ''
  sabotaje "s15 truncado por bytes (vuelve cut -c y parte multibyte)" 's/trunca 120/cut -c1-120/' '' ''
  sabotaje "s16 sufijo re-admitido en es_historia (precios-sin-changelog exento)" 's/^    changelog|/    *changelog*|/' '' ''
  sabotaje "s17 frontera izquierda quitada (ad-assets vuelve a fabricar citas)" 's|^FRONT=.*|FRONT=""|' '' ''
  sabotaje "s18 resolución contra el citante quitada (la sub-skill vuelve a dar rota falsa)" 's|^resuelve_contra_citante() {.*|resuelve_contra_citante() { return 1;|' '' ''
  sabotaje "s19 prefijos \$VAR genéricos quitados (la variable irresoluble se vuelve roja)" '/norm-var-generica/d' '' ''
  sabotaje "s20 busca sin -L (symlinks invisibles en texto, secretos, blindaje y rotas)" 's/find -L /find /g' '' ''
  sabotaje "s21 -iname a -name (.MD y .SH en mayúsculas invisibles otra vez)" 's/-iname/-name/g' '' ''
  sabotaje "s22 parser de description ciego (la clave no corta: conteo muerto)" 's/m = key.match(l)  # C7-corte-clave/m = None/' '' ''
  sabotaje "s23 blindaje por un inodo (raíz con uchg vuelve a dar Blindada)" 's|-eq "$M_TOT" ] && \[ "$M_TOT" -gt 0 ]|-ge 1 ]|' '' ''
  sabotaje "s24 guardia de shell quitada (zsh vuelve a correr el detector directo)" 's|exec bash "$0" "$@"|:|' '' ''
  sabotaje "s25 sufijo interno quitado (la cita imprecisa intra-skill se vuelve roja)" 's|hit_interno=$(.*# B4-sufijo-interno|hit_interno=""|' '' ''
  # s26: el blanco vivo de la normalizacion es la de TEXTO (direccion de huerfanos) — la
  # de token en el clasificador tiene defensa redundante DECLARADA (sister_valida + el
  # propio filesystem colapsa .. y //), asi que sola no muerde; la de texto si.
  sabotaje "s26 normaliza_texto quitada (skills/../ deja de salvar huerfanas)" 's@ | normaliza_texto @ @' '' ''
  # s27/s34: la rama ../* y sister_valida son defensas EN CAPAS del mismo mandato E (el
  # clasificador jamas acepta .. como hermana). s27 quita la rama (la rota ../ pierde su
  # forma → muerde); s34 quita la rama Y la guardia (la hermana fantasma skills/.. vuelve
  # → muerde). La guardia sola no muerde porque la rama la cubre — redundancia declarada.
  sabotaje "s27 rama-sube quitada (../x pierde la resolucion contra el citante)" '/rama-sube/,+5d' '' ''
  sabotaje "s34 rama-sube y sister_valida quitadas (.. vuelve a ser hermana fantasma)" '/rama-sube/,+5d;/^sister_valida()/,/^}/ s/return 1/return 0/' '' ''
  sabotaje "s28 rescate del citante con grep crudo (motor.sh.viejo resuelve motor.sh)" 's|compara_ruta mencion "$STRIP_DIR/$rcc_idx" "$rcc_b" 0 && return 0|grep -qF -- "$rcc_b" "$STRIP_DIR/$rcc_idx" \&\& return 0|' '' ''
  sabotaje "s30 registro de NO LEÍDOS callado (chmod 000 vuelve a dar verde)" '/registra-no-leido/d' '' ''
  sabotaje "s31 familia AKIA quitada del barrido de secretos" 's/AKIA\[A-Z0-9\]{16}|//' '' ''
  sabotaje "s32 modo plugin quitado (CRÍTICO falso y 23 intrusos vuelven)" 's/ES_PLUGIN=1/ES_PLUGIN=0/' '' ''
  sabotaje "s33 guardia POSIX quitada (sh trunca el informe tras BLINDAJE)" 's|GSA_REEXEC=1 exec /bin/bash "$0" "$@"|:|' '' ''
  sabotaje "s35 DIR_RE sin frontera (ad-assets/imagenes/ fabrica cobertura de assets/)" 's|^DIR_RE="${FRONT}|DIR_RE="|' '' ''
  sabotaje "s36 rescate-ups quitado (../references desde scripts/ deja de salvar)" '/rescate-ups/,+2d' '' ''
  for fmt in md txt py sh js ts json css html xml yaml yml liquid csv; do
    case "$fmt" in
      md)  SEDX='/^TEXT_EXTS=/ s/"md /"/' ;;
      csv) SEDX='/^TEXT_EXTS=/ s/ csv"/"/' ;;
      *)   SEDX="/^TEXT_EXTS=/ s/ $fmt / /" ;;
    esac
    sabotaje "s_fmt_$fmt (formato .$fmt fuera de lista_texto)" "$SEDX" '' ''
  done
  echo ""
  echo "SABOTAJES: $S_PASAN mordidos, $S_FALLAN fallas, $S_SALTADOS fuera del filtro (de $((S_PASAN+S_FALLAN+S_SALTADOS)))"
  [ "$S_FALLAN" -gt 0 ] && exit 1
  exit 0
fi

# =====================================================================
# MODO NORMAL
# =====================================================================
T=$(mktemp -d)
# C8: los casos blindados dejan nodos con uchg dentro del sandbox — sin el nouchg previo
# el rm -rf fallaria y el tmpdir quedaria como basura inmortal. El chmod 000 igual.
trap 'chflags -R nouchg "$T" 2>/dev/null; chmod -R u+rwX "$T" 2>/dev/null; rm -rf "$T"' EXIT
FAKE_HOME="$T/home"
SKILL="$FAKE_HOME/.claude/skills/skill-prueba"

# --- Siembra: skill-prueba (banco principal) ---
mkdir -p "$SKILL/references/plantillas-sub" "$SKILL/scripts" "$SKILL/assets/sub" "$SKILL/assets/brand" "$SKILL/examples"
mkdir -p "$FAKE_HOME/.claude/skills/skill-hermana/scripts" "$FAKE_HOME/.claude/skills/skill-hermana/references"
mkdir -p "$FAKE_HOME/.claude/skills/skill-otra/references"
mkdir -p "$FAKE_HOME/.claude/skills/skill-her/references"
mkdir -p "$FAKE_HOME/taller/scripts"

echo "echo util" > "$FAKE_HOME/.claude/skills/skill-hermana/scripts/util.sh"     # hermana con archivo existente → OK
echo "# hermana" > "$FAKE_HOME/.claude/skills/skill-hermana/SKILL.md"            # raíz de hermana citable → OK
echo "corta" > "$FAKE_HOME/.claude/skills/skill-hermana/references/corta.md"     # forma corta v1.7 → OK
echo "vive" > "$FAKE_HOME/.claude/skills/skill-hermana/references/vive-en-hermana.md"  # rescate EN_HERMANA (única + nombrada)
echo "x" > "$FAKE_HOME/.claude/skills/skill-hermana/references/compartida.md"    # colisión: vive en 2 hermanas
echo "x" > "$FAKE_HOME/.claude/skills/skill-otra/references/compartida.md"       # colisión: vive en 2 hermanas
echo "x" > "$FAKE_HOME/.claude/skills/skill-otra/references/de-otra.md"          # dueña única NO nombrada en el texto
echo "x" > "$FAKE_HOME/.claude/skills/skill-her/references/de-sub.md"            # dueña única cuyo nombre es SUBSTRING de skill-hermana
echo "echo externo" > "$FAKE_HOME/taller/scripts/externo.sh"                     # existe tras expandir ~

echo "guia con plantillas en plantillas-sub/ listas" > "$SKILL/references/guia.md"  # cita dir RELATIVO específico desde references/
echo "t1" > "$SKILL/references/plantillas-sub/t1.md"      # cubierta SOLO por el dir relativo de guia.md
echo "echo vivo" > "$SKILL/scripts/vivo.sh"               # citada por ruta
printf '# motor\n# datos maestros en references/rota-en-py.md\n' > "$SKILL/scripts/motor.py"  # rota citada en un .py
echo "{}" > "$SKILL/assets/config-a.json"                 # citada SOLO por glob CON ancla assets/*.json
echo "{}" > "$SKILL/assets/config-b.json"                 # citada SOLO por glob CON ancla assets/*.json
echo "{}" > "$SKILL/assets/sub/deep.json"                 # F1: el glob assets/*.json NO cruza la barra → huerfana
echo "logo" > "$SKILL/assets/brand/logo.txt"              # F1: cubierta SOLO por glob AMPLIO assets/brand/* → DUDOSO
echo "echo solo" > "$SKILL/scripts/solo-por-dir.sh"       # cubierta SOLO por el token desnudo scripts/ → DUDOSO, no exenta
echo "huerfano" > "$SKILL/references/huerfano-real.md"    # huerfano REAL: nadie lo nombra
echo "palabra" > "$SKILL/references/palabra-suelta.md"    # solo mencionada como palabra suelta (sin /): huerfana
echo "hist" > "$SKILL/references/solo-en-historia.md"     # solo mencionada en el changelog: huerfana
echo "acento" > "$SKILL/references/guía-acentuada.md"     # ruta con acento, citada: ni rota ni huerfana
echo "auto" > "$SKILL/references/auto-salvada.md"         # se cita SOLO a si misma: huerfana (autoexclusion)
printf 'yo misma vivo en references/auto-salvada.md\n' >> "$SKILL/references/auto-salvada.md"
echo "ref" > "$SKILL/references/mismo-nombre.md"          # citada por su ruta completa
echo "asset" > "$SKILL/assets/mismo-nombre.md"            # MISMA base, otra carpeta: nadie la cita → huerfana (mata "/base")
echo "url" > "$SKILL/references/remoto-url.md"            # solo "citada" dentro de una URL → huerfana (URL no salva)
echo "intruso" > "$SKILL/examples/demo.txt"               # material fuera de las carpetas canonicas
echo "precios" > "$SKILL/references/precios-sin-changelog.md"  # F5d: el sufijo NO exime (es_historia anclada) → huerfana
echo "der" > "$SKILL/references/limite-der.md"            # m8: solo mencionada como ...md.bak → huerfana
echo "bak" > "$SKILL/references/limite-der.md.bak"        # el .bak citado existe y se salva a si mismo
echo "izq" > "$SKILL/references/limite-izq.md"            # m7: solo mencionada con barra a la izquierda → huerfana
echo "dolar" > "$SKILL/references/norm-dolar.md"          # F2: citada SOLO como $SKILL_DIR/... → viva
echo "angulo" > "$SKILL/references/norm-angulo.md"        # F2: citada SOLO como <SKILL_DIR>/... → viva
echo "vivoesp" > "$SKILL/references/con espacio vivo.md"  # F12: citada entre backticks CON espacio → viva
echo "cargada" > "$SKILL/references/cargada-por-selftest.md"  # F7: citada SOLO por scripts/selftest.py (que ya cuenta)
printf '# selftest REAL de skill-prueba\n# corre contra references/cargada-por-selftest.md\n' > "$SKILL/scripts/selftest.py"

# F3: historia con MAYUSCULAS acentuadas — BITACORA con tilde exenta, y su mencion no salva
printf '# BITACORA vieja\n- se documento references/solo-en-bitacora-may.md aqui y en ningun lado mas\n' > "$SKILL/references/BITÁCORA.md"
echo "may" > "$SKILL/references/solo-en-bitacora-may.md"

# =====================================================================
# CORPUS DE REGRESION REAL — casos COPIADOS de skills reales que el constructor NO eligio.
# REGLA DEL BANCO: cada ronda de reparacion AÑADE al corpus al menos un caso tomado de una
# skill real que el constructor no eligio. Origen documentado de cada caso:
#   v1.12: sub-skills de claude-ads; prefijos-trampa ./ad-assets/ y managed-agents/
#     (claude-ads 12/43 rotas fabricadas, claude-api 1/1); $CLAUDE_PLUGIN_ROOT y ${HOME};
#     .MD/.SH en mayusculas; el trio de symlinks del verificador; description con
#     metadata detras (watch: 520 impresos vs ~247 reales).
#   v1.14: la cita "../references/x" desde scripts/ (golden-investigacion-mercado, 1 rojo
#     falso EXISTIENDO) y "../agents/x" desde references/ (baoyu-design, 4 rojos falsos)
#     — la hermana fantasma ".."; la prosa "ad-assets/imagenes/" que NO debe fabricar
#     cobertura de assets/imagenes/ (gemelo del prefijo-trampa, ahora en el extractor de
#     DIRECTORIOS); motor.sh.viejo contra el rescate del citante; el arbol plugin de
#     claude-ads (CRITICO falso + 23 intrusos falsos).
# =====================================================================
# B4: sub-skill que cita su propio references/ (claude-ads)
mkdir -p "$SKILL/skills/sub-uno/references"
echo "sub" > "$SKILL/skills/sub-uno/references/de-sub-skill.md"
printf '# Sub-skill\nLa guia propia: references/de-sub-skill.md\n' > "$SKILL/skills/sub-uno/SKILL.md"
# B4-b2: citada desde la raiz pero vive en OTRA carpeta de la misma skill -> DUDOSO
echo "imprecisa" > "$SKILL/skills/sub-uno/references/en-otra-carpeta.md"
# B (v1.14) caso motor.sh.viejo contra el rescate del citante: la cita rota de la raiz
# references/caso-der.md NO debe resolverla un citante cuyo texto solo dice ...md.viejo
# aunque su directorio SI contenga references/caso-der.md (grep crudo la resolvia).
mkdir -p "$SKILL/skills/sub-dos/references"
echo "existe" > "$SKILL/skills/sub-dos/references/caso-der.md"
printf '# Sub-dos\nrespaldo viejo: references/caso-der.md.viejo\n' > "$SKILL/skills/sub-dos/SKILL.md"
# v1.14: scripts/motor-viejo.sh citado NO existe (rota) y el legado scripts/motor-viejo.sh.viejo
# existe sin cita (huerfano) — el sufijo .viejo no satisface a nadie en ninguna direccion.
echo "legado" > "$SKILL/scripts/motor-viejo.sh.viejo"
# E (v1.14) las cuatro formas relativas, en las DOS direcciones:
echo "punto" > "$SKILL/references/punto-viva.md"          # citada SOLO como ./references/punto-viva.md → viva
echo "sube" > "$SKILL/references/rel-subida.md"           # citada SOLO como ../references/rel-subida.md desde scripts/ → viva
printf '# citador relativo\n# manual: ../references/rel-subida.md\n# y la que falta: ../references/rota-rel.md\n' > "$SKILL/scripts/cita-rel.sh"
echo "colapso" > "$SKILL/references/colapso-viva.md"      # citada SOLO como skills/../references/colapso-viva.md → viva (jamas hermana "..")
echo "doble" > "$SKILL/references/doble-barra.md"         # citada SOLO como references//doble-barra.md → viva
# A (v1.14) PROSA ad-assets/imagenes/: NO fabrica la cobertura assets/imagenes/ — el
# archivo sin cita bajo assets/imagenes/ sigue siendo huerfano.
mkdir -p "$SKILL/assets/imagenes"
echo "png" > "$SKILL/assets/imagenes/prosa-huerfana.png"
# C6: extensiones en mayusculas, ambas direcciones + sintaxis
echo "may viva" > "$SKILL/references/MAYUSCULA.MD"
echo "salvada" > "$SKILL/references/viva-por-mayus.md"
printf 'La viva: references/viva-por-mayus.md y la rota: references/rota-mayuscula.MD\n' > "$SKILL/references/CITA-EN-MAYUS.MD"
printf 'if [ x\nthen (\n' > "$SKILL/scripts/roto.SH"
# B3: prefijos de variable
echo "plugin" > "$SKILL/references/plugin-var.md"
echo "home" > "$SKILL/references/por-home.md"
# C5: trio de symlinks — texto citador externo, secreto externo, y el listado
printf 'Guia externa enlazada.\nviva: references/salvada-por-symlink.md\nrota: references/rota-por-symlink.md\n' > "$FAKE_HOME/taller/texto-externo.md"
echo "sym viva" > "$SKILL/references/salvada-por-symlink.md"
ln -s "$FAKE_HOME/taller/texto-externo.md" "$SKILL/references/enlace-texto.md"
printf 'config vieja\napi_key = "AAAABBBB1234CCCCDDDD9999"\n' > "$FAKE_HOME/taller/secreto.txt"
ln -s "$FAKE_HOME/taller/secreto.txt" "$SKILL/assets/config-secreta.txt"
# B1: el glob amplio assets/brand/* NO alcanza dos niveles — lo profundo sin cita es huerfano
mkdir -p "$SKILL/assets/brand/sub"
echo "deep" > "$SKILL/assets/brand/sub/deep-brand.txt"

# F9: trampa de truncado — dos lineas ¿ con offset de 1 byte: el corte por bytes parte una
{ printf 'x¿'; for i in $(seq 1 120); do printf 'á'; done; printf '\n'
  printf 'xy¿'; for i in $(seq 1 120); do printf 'á'; done; printf '\n'; } > "$SKILL/references/apertura-larga.md"

# F5a: un caso por CADA formato de TEXT_EXTS, en las DOS direcciones (rota citada en el
# formato + archivo vivo salvado SOLO por una cita en ese formato). v1.14: entra .ts.
for fmt in md txt py sh js ts json css html xml yaml yml liquid csv; do
  echo "viva" > "$SKILL/references/viva-fmt-$fmt.md"
done
printf 'La rota: references/rota-fmt-md.md y la viva: references/viva-fmt-md.md\n' > "$SKILL/references/cita-en-md.md"
printf 'rota references/rota-fmt-txt.md viva references/viva-fmt-txt.md\n' > "$SKILL/references/cita-en-txt.txt"
printf '# references/rota-fmt-py.md\n# references/viva-fmt-py.md\n' > "$SKILL/scripts/cita-en-py.py"
printf '# references/rota-fmt-sh.md\n# references/viva-fmt-sh.md\n' > "$SKILL/scripts/cita-en-sh.sh"
printf '// references/rota-fmt-js.md\n// references/viva-fmt-js.md\n' > "$SKILL/scripts/cita-en-js.js"
printf '// references/rota-fmt-ts.md\n// references/viva-fmt-ts.md\nexport const x: number = 1;\n' > "$SKILL/scripts/cita-en-ts.ts"
printf '{"rota": "references/rota-fmt-json.md", "viva": "references/viva-fmt-json.md"}\n' > "$SKILL/references/cita-en-json.json"
printf '/* references/rota-fmt-css.md y references/viva-fmt-css.md */\n' > "$SKILL/references/cita-en-css.css"
printf '<p>references/rota-fmt-html.md y references/viva-fmt-html.md</p>\n' > "$SKILL/references/cita-en-html.html"
printf '<notas rota="references/rota-fmt-xml.md" viva="references/viva-fmt-xml.md"/>\n' > "$SKILL/references/cita-en-xml.xml"
printf 'rota: references/rota-fmt-yaml.md\nviva: references/viva-fmt-yaml.md\n' > "$SKILL/references/cita-en-yaml.yaml"
printf 'rota: references/rota-fmt-yml.md\nviva: references/viva-fmt-yml.md\n' > "$SKILL/references/cita-en-yml.yml"
printf '{%% comment %%} references/rota-fmt-liquid.md y references/viva-fmt-liquid.md {%% endcomment %%}\n' > "$SKILL/references/cita-en-liquid.liquid"
printf 'rota,viva\nreferences/rota-fmt-csv.md,references/viva-fmt-csv.md\n' > "$SKILL/references/cita-en-csv.csv"

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
La carpeta de marca entera se declara con el glob amplio assets/brand/* y eso no exime.
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
Referencia rota con acento: references/versión-perdida.md
Guia acentuada viva: references/guía-acentuada.md
Cita imprecisa que vive en la hermana: references/vive-en-hermana.md
Cita con colision de nombres: references/compartida.md
Cita cuya duena nadie nombra: references/de-otra.md
Cita cuya duena solo es substring de otra: references/de-sub.md
La variante buena es references/mismo-nombre.md y la de assets no se cita jamas.
Recurso remoto que no salva nada: https://cdn.ejemplo.com/references/remoto-url.md
Doc remota que no fabrica rotas: https://github.com/x/y/references/rota-por-url.md
El selftest REAL de esta skill se corre siempre: scripts/selftest.py
El archivo palabra-suelta.md se menciona aqui sin ruta y eso no es una cita.
La bitacora completa esta en references/changelog.md.
El respaldo viejo quedo como references/limite-der.md.bak y ese sufijo no salva al original.
La izquierda tampoco salva: otra-carpeta/references/limite-izq.md no es cita local valida.
Cita normalizada dolar: $SKILL_DIR/references/norm-dolar.md
Cita normalizada angulo: <SKILL_DIR>/references/norm-angulo.md
Cita con espacios viva: `references/con espacio vivo.md`
Cita con espacios rota: `references/con espacio roto.md`
Trampa de truncado con apertura: references/apertura-larga.md
Casos por formato: references/cita-en-md.md references/cita-en-txt.txt scripts/cita-en-py.py scripts/cita-en-sh.sh scripts/cita-en-js.js scripts/cita-en-ts.ts references/cita-en-json.json references/cita-en-css.css references/cita-en-html.html references/cita-en-xml.xml references/cita-en-yaml.yaml references/cita-en-yml.yml references/cita-en-liquid.liquid references/cita-en-csv.csv
Corpus real - prefijos trampa que NO fabrican citas: los renders van a ./ad-assets/demo-1.png y el plan a managed-agents/planner.md
Corpus real - prosa de carpeta trampa que NO fabrica cobertura: los recursos quedaron en ad-assets/imagenes/ desde el rediseno
Corpus real - cita de plugin oficial: $CLAUDE_PLUGIN_ROOT/references/plugin-var.md
Corpus real - variable irresoluble: $OTRA_VAR/references/no-existe-var.md
Corpus real - home resuelto de verdad: ${HOME}/.claude/skills/skill-prueba/references/por-home.md
Corpus real - herramienta externa por home: ${HOME}/taller/scripts/externo.sh
Corpus real - mayusculas: references/MAYUSCULA.MD con su citadora references/CITA-EN-MAYUS.MD y el legado scripts/roto.SH
Corpus real - symlinks: el texto enlazado references/enlace-texto.md y la config enlazada assets/config-secreta.txt
Corpus real - cita imprecisa intra-skill: references/en-otra-carpeta.md
Corpus real (v1.14) - punto explicito: ./references/punto-viva.md
Corpus real (v1.14) - colapso lexico: skills/../references/colapso-viva.md
Corpus real (v1.14) - doble barra: references//doble-barra.md
Corpus real (v1.14) - el citador relativo: scripts/cita-rel.sh
Corpus real (v1.14) - cita rota de la raiz que sub-dos NO debe resolver: references/caso-der.md
Corpus real (v1.14) - legado con sufijo: la cita scripts/motor-viejo.sh apunta a un script que ya no esta
EOF

# --- Siembra: skill-selfaudit (contexto es_yo + es_fixture del banco propio) ---
SELFSK="$FAKE_HOME/.claude/skills/skill-selfaudit"
mkdir -p "$SELFSK/scripts" "$SELFSK/references"
cp "$INV" "$SELFSK/scripts/inventario.sh"
printf '\n# cadena del informe que NO debe salvar: references/salvada-por-mi-echo.md\n' >> "$SELFSK/scripts/inventario.sh"
echo "x" > "$SELFSK/references/salvada-por-mi-echo.md"    # solo la nombra el propio detector → huerfana
echo "x" > "$SELFSK/references/solo-en-fixture.md"        # solo la nombra el fixture → huerfana
cat > "$SELFSK/references/fixture-caso.md" <<'EOF'
# Banco de casos sembrados (fixture): en self-audit sus citas NO cuentan como texto vivo
la referencia sembrada rota: references/rota-fixture.md
y el archivo references/solo-en-fixture.md que solo este banco nombra
EOF
cat > "$SELFSK/SKILL.md" <<'EOF'
---
name: skill-selfaudit
description: caso self-audit del detector (es_yo + es_fixture)
---

# Skill self-audit

El detector vive en scripts/inventario.sh y su banco de casos en references/fixture-caso.md.
EOF

# --- Siembra: skill-f8 (verde con duda pendiente + frontmatter C7) ---
F8SK="$FAKE_HOME/.claude/skills/skill-f8"
mkdir -p "$F8SK/scripts"
echo "echo suelto" > "$F8SK/scripts/suelto.sh"            # cubierta SOLO por token desnudo → DUDOSO, cero huerfanas
cat > "$F8SK/SKILL.md" <<'EOF'
---
name: skill-f8
description: caso del verde con duda pendiente
version2: la clave raiz CON digito tambien cierra la description (C7 v1.14)
metadata:
  relleno: este bloque viene DESPUES de la description (corpus real - watch) y el contador no debe sumarlo al conteo de caracteres porque seria imprimir un numero inflado como si fuera la description
allowed-tools: Bash, Read
---

# Skill f8

Los utilitarios de la carpeta scripts/ corren solos.
EOF

# --- Siembra: skill-blind (C8: blindaje por UN inodo — solo la raiz con uchg) ---
BLSK="$FAKE_HOME/.claude/skills/skill-blind"
mkdir -p "$BLSK/scripts"
echo "echo ok" > "$BLSK/scripts/ok.sh"
cat > "$BLSK/SKILL.md" <<'EOF'
---
name: skill-blind
description: caso del blindaje parcial (solo la raiz con uchg)
---

# Skill blind

Su unico script: scripts/ok.sh
EOF
chflags uchg "$BLSK" 2>/dev/null || true   # SOLO la raiz — el sabotaje historico del verificador

# --- Siembra v1.14: skill-blindlink (ANTI-VERDE de Blindada — el agujero via symlink) ---
BLLNK="$FAKE_HOME/.claude/skills/skill-blindlink"
mkdir -p "$BLLNK"
cat > "$BLLNK/SKILL.md" <<'EOF'
---
name: skill-blindlink
description: anti-verde del blindaje (symlink a archivo externo escribible)
---

# Skill blindlink

Config enlazada: references/config-fuera.txt
EOF
mkdir -p "$BLLNK/references"
echo "mutable" > "$FAKE_HOME/taller/mutable.txt"          # externo, escribible, SIN uchg
ln -s "$FAKE_HOME/taller/mutable.txt" "$BLLNK/references/config-fuera.txt"
chflags uchg "$BLLNK/SKILL.md" "$BLLNK/references" "$BLLNK" 2>/dev/null || true
chflags -h uchg "$BLLNK/references/config-fuera.txt" 2>/dev/null || true

# --- Siembra v1.14: skill-000 (ANTI-VERDE de lectura: chmod 000 = informe parcial) ---
CEROSK="$FAKE_HOME/.claude/skills/skill-000"
mkdir -p "$CEROSK/references"
cat > "$CEROSK/SKILL.md" <<'EOF'
---
name: skill-000
description: anti-verde de lectura (archivo ilegible)
---

# Skill 000

La guia oculta: references/oculto.md
EOF
echo "contenido que nadie puede leer" > "$CEROSK/references/oculto.md"
chmod 000 "$CEROSK/references/oculto.md"

# --- Siembra v1.14: skill-secretos (ANTI-VERDE de secretos: familias F6) ---
SECSK="$FAKE_HOME/.claude/skills/skill-secretos"
mkdir -p "$SECSK/references"
cat > "$SECSK/SKILL.md" <<'EOF'
---
name: skill-secretos
description: anti-verde del barrido de secretos (una familia por linea)
---

# Skill secretos

Todas las configuraciones viven en references/config-mala.md y el arte en references/arte.md.
EOF
cat > "$SECSK/references/config-mala.md" <<'EOF'
pem: -----BEGIN RSA PRIVATE KEY-----
anthropic: sk-ant-api03-abcdefghijklmnop
aws: AKIAIOSFODNN7EXAMPLE
meta: EAAabcdefghijklmnopqrstuvwxyz1234567890ABCDEFGH
cuenta: act_123456789012
contraseña: miClaveSecreta99
clave = otraClave2026
telefono: +57 3001234567
api_key = "AAAABBBB1234CCCCDDDD9999"
EOF
printf 'imagen inline que NO debe sonar:\n<img src="data:image/png;base64,tokenpasswordapikeyAAAABBBBCCCCDDDDEEEEFFFF0000111122223333444455556666777788889999"/>\n' > "$SECSK/references/arte.md"

# --- Siembra v1.14: skill-plugin (F8: repo plugin, sin SKILL.md raiz) ---
PLGSK="$FAKE_HOME/.claude/skills/skill-plugin"
mkdir -p "$PLGSK/.claude-plugin" "$PLGSK/skills/uno" "$PLGSK/skills/dos" "$PLGSK/tests" "$PLGSK/.github"
printf '{"name":"skill-plugin"}\n' > "$PLGSK/.claude-plugin/plugin.json"
printf 'MIT\n' > "$PLGSK/LICENSE"
printf '# readme\n' > "$PLGSK/README.md"
printf '# changelog\n' > "$PLGSK/CHANGELOG.md"
printf 'echo instala\n' > "$PLGSK/install.sh"
printf 'assert true\n' > "$PLGSK/tests/test_basico.py"
cat > "$PLGSK/skills/uno/SKILL.md" <<'EOF'
---
name: uno
description: sub-skill uno
---
# Uno
EOF
cat > "$PLGSK/skills/dos/SKILL.md" <<'EOF'
---
name: dos
description: sub-skill dos
---
# Dos
EOF
echo "colado" > "$PLGSK/archivo-colado.txt"   # intruso REAL: ni canonico ni estandar de plugin

# --- Correr el inventario contra los sandbox (HOME redirigido: cero contacto con el arsenal real) ---
OUT="$T/salida.txt"
HOME="$FAKE_HOME" bash "$INV" "$SKILL" > "$OUT" 2>&1
OUT2="$T/salida-self.txt"
HOME="$FAKE_HOME" bash "$SELFSK/scripts/inventario.sh" "$SELFSK" > "$OUT2" 2>&1
OUT3="$T/salida-f8.txt"
HOME="$FAKE_HOME" bash "$INV" "$F8SK" > "$OUT3" 2>&1
OUT4="$T/salida-blind.txt"
HOME="$FAKE_HOME" bash "$INV" "$BLSK" > "$OUT4" 2>&1
OUT5="$T/salida-blindlink.txt"
HOME="$FAKE_HOME" bash "$INV" "$BLLNK" > "$OUT5" 2>&1
OUT6="$T/salida-000.txt"
HOME="$FAKE_HOME" bash "$INV" "$CEROSK" > "$OUT6" 2>&1
OUT7="$T/salida-secretos.txt"
HOME="$FAKE_HOME" bash "$INV" "$SECSK" > "$OUT7" 2>&1
OUT8="$T/salida-plugin.txt"
HOME="$FAKE_HOME" bash "$INV" "$PLGSK" > "$OUT8" 2>&1
# C9: el detector corrido con ZSH debe dar EXACTAMENTE el mismo informe (la guardia
# re-ejecuta con bash); sin guardia, zsh no parte TEXT_EXTS y todo sale verde mentiroso.
OUT3Z="$T/salida-f8-zsh.txt"
if command -v zsh >/dev/null 2>&1; then
  HOME="$FAKE_HOME" zsh "$INV" "$F8SK" > "$OUT3Z" 2>&1
else
  cp "$OUT3" "$OUT3Z"   # sin zsh en PATH el caso no es evaluable: no debe tumbar el banco
fi
# F5 (v1.14): el detector corrido con SH (bash POSIX de macOS) debe re-ejecutarse SOLO y
# entregar el informe COMPLETO — sin guardia moria truncado tras BLINDAJE sin aviso.
OUT3S="$T/salida-f8-sh.txt"
if command -v sh >/dev/null 2>&1; then
  HOME="$FAKE_HOME" sh "$INV" "$F8SK" > "$OUT3S" 2>&1
else
  cp "$OUT3" "$OUT3S"
fi

bloque() {  # $1=marca $2=archivo — extrae las lineas indentadas que siguen a un encabezado
  awk -v m="$1" 'index($0,m){f=1;next} f&&/^    /{print;next} f{exit}' "$2"
}
B_ROTAS=$(bloque "Mencionadas pero NO existen" "$OUT")
B_HUERF=$(bloque "Existen pero nadie las menciona" "$OUT")
B_HERM=$(bloque "viven en otra skill" "$OUT")
B_DUD=$(bloque "DUDOSOS:" "$OUT")
B_SIS_ROTA=$(bloque "skills hermanas que NO existen" "$OUT")
B_SIS_OK=$(bloque "skills hermanas verificadas" "$OUT")
B_INTRUSO=$(bloque "fuera de las carpetas canónicas" "$OUT")
B2_ROTAS=$(bloque "Mencionadas pero NO existen" "$OUT2")
B2_HUERF=$(bloque "Existen pero nadie las menciona" "$OUT2")

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
chk "externas: 2 verificadas (una por ~ y una por \${HOME} resuelto)" "$(contiene "$(cat "$OUT")" "2 ruta(s) externa(s) verificadas")"
chk "B3 home externo: sin rota fabricada de scripts/externo.sh" "$(no_contiene "$B_ROTAS" "externo.sh")"
chk "tilde: externo.sh NO en dudosos"                          "$(no_contiene "$B_DUD" "externo.sh")"
chk "comentario HTML: fantasma-comentario.md no en rotas"      "$(no_contiene "$B_ROTAS" "fantasma-comentario.md")"
chk "changelog: borrado-historico.sh no en rotas"              "$(no_contiene "$B_ROTAS" "borrado-historico.sh")"
chk "URL: rota-por-url.md dentro de una URL NO fabrica rota"   "$(no_contiene "$B_ROTAS" "rota-por-url.md")"
chk "acento: guía-acentuada.md citada NO en rotas"             "$(no_contiene "$B_ROTAS" "guía-acentuada.md")"
chk "acento: guía-acentuada.md citada NO huerfana"             "$(no_contiene "$B_HUERF" "guía-acentuada.md")"
chk "rescate EN_HERMANA: vive-en-hermana.md en el bloque info" "$(contiene "$B_HERM" "vive-en-hermana.md → existe en skill-hermana")"
chk "rescate EN_HERMANA: vive-en-hermana.md NO en rotas"       "$(no_contiene "$B_ROTAS" "vive-en-hermana.md")"
chk "huerfano por glob CON ancla: config-a.json no es huerfana" "$(no_contiene "$B_HUERF" "config-a.json")"
chk "huerfano por glob CON ancla: config-b.json no es huerfana" "$(no_contiene "$B_HUERF" "config-b.json")"
chk "dir RELATIVO especifico desde references/: t1.md no es huerfana" "$(no_contiene "$B_HUERF" "plantillas-sub/t1.md")"
chk "citadas por ruta: vivo.sh, motor.py y guia.md no huerfanas" "$([ "$(contiene "$B_HUERF" "vivo.sh")" -eq 0 ] && [ "$(contiene "$B_HUERF" "motor.py")" -eq 0 ] && [ "$(contiene "$B_HUERF" "guia.md")" -eq 0 ] && echo 1 || echo 0)"
chk "citada por ruta completa: references/mismo-nombre.md no huerfana" "$(no_contiene "$B_HUERF" "references/mismo-nombre.md")"
chk "F2 normalizacion dolar: norm-dolar.md NO huerfana"        "$(no_contiene "$B_HUERF" "norm-dolar.md")"
chk "F2 normalizacion angulo: norm-angulo.md NO huerfana"      "$(no_contiene "$B_HUERF" "norm-angulo.md")"
chk "F2 normalizacion: nada de norm- en rotas"                 "$(no_contiene "$B_ROTAS" "norm-")"
chk "F2 normalizacion: nada de norm- en DUDOSOS"               "$(no_contiene "$B_DUD" "norm-")"
chk "F3 pliegue: BITÁCORA.md es historia, NO huerfana"         "$(no_contiene "$B_HUERF" "BITÁCORA.md")"
chk "F7 selftest de la skill cuenta: cargada-por-selftest.md NO huerfana" "$(no_contiene "$B_HUERF" "cargada-por-selftest.md")"
chk "F12 espacios: con espacio vivo.md NO huerfana"            "$(no_contiene "$B_HUERF" "con espacio vivo.md")"
chk "F12 espacios: con espacio vivo.md NO en DUDOSOS"          "$(no_contiene "$B_DUD" "con espacio vivo.md")"
chk "m8: el .bak citado se salva a si mismo (no huerfano)"     "$(no_contiene "$B_HUERF" "limite-der.md.bak")"
chk "E punto explicito: ./references/punto-viva.md salva → NO huerfana" "$(no_contiene "$B_HUERF" "punto-viva.md")"
chk "E punto explicito: punto-viva.md NO en rotas"             "$(no_contiene "$B_ROTAS" "punto-viva.md")"
chk "E subida ../: rel-subida.md citada desde scripts/ NO huerfana" "$(no_contiene "$B_HUERF" "rel-subida.md")"
chk "E subida ../: rel-subida.md NO en rotas"                  "$(no_contiene "$B_ROTAS" "rel-subida.md")"
chk "E subida ../: rel-subida.md NO en hermanas rotas (adios hermana ..)" "$(no_contiene "$B_SIS_ROTA" "rel-subida.md")"
chk "E colapso: skills/../references/colapso-viva.md ES local → NO rota ni hermana" "$([ "$(contiene "$B_ROTAS" "colapso-viva.md")" -eq 0 ] && [ "$(contiene "$B_SIS_ROTA" "colapso-viva.md")" -eq 0 ] && echo 1 || echo 0)"
chk "E colapso: colapso-viva.md NO huerfana (la cita colapsada salva)" "$(no_contiene "$B_HUERF" "colapso-viva.md")"
chk "E doble barra: references//doble-barra.md ES local viva"  "$([ "$(contiene "$B_ROTAS" "doble-barra.md")" -eq 0 ] && [ "$(contiene "$B_HUERF" "doble-barra.md")" -eq 0 ] && echo 1 || echo 0)"

echo "== ASERCIONES (direccion 2: lo REALMENTE malo SI se marca, en SU bloque) =="
chk "rota REAL cazada: references/rota-real.md"                "$(contiene "$B_ROTAS" "references/rota-real.md")"
chk "rota citada en un .py cazada: references/rota-en-py.md"   "$(contiene "$B_ROTAS" "references/rota-en-py.md")"
chk "rota con ACENTO cazada: references/versión-perdida.md"    "$(contiene "$B_ROTAS" "references/versión-perdida.md")"
for fmt in md txt py sh js ts json css html xml yaml yml liquid csv; do
  chk "F5a formato .$fmt caza su rota: rota-fmt-$fmt.md"       "$(contiene "$B_ROTAS" "references/rota-fmt-$fmt.md")"
  chk "F5a formato .$fmt salva su viva: viva-fmt-$fmt.md NO huerfana" "$(no_contiene "$B_HUERF" "viva-fmt-$fmt.md")"
done
chk "C6 rota citada en un .MD mayuscula cazada: rota-mayuscula.MD" "$(contiene "$B_ROTAS" "references/rota-mayuscula.MD")"
chk "C5 rota citada en texto tras symlink cazada: rota-por-symlink.md" "$(contiene "$B_ROTAS" "references/rota-por-symlink.md")"
chk "E subida ../ rota cazada: ../references/rota-rel.md"      "$(contiene "$B_ROTAS" "../references/rota-rel.md")"
chk "B el caso-der.md.viejo citado inexistente ROTA (extraccion greedy honesta)" "$(contiene "$B_ROTAS" "references/caso-der.md.viejo")"
chk "v1.14 legado: scripts/motor-viejo.sh citado sin archivo → ROTA" "$(contiene "$B_ROTAS" "scripts/motor-viejo.sh")"
chk "exactamente 22 rotas (ni mas ni menos)"                   "$(cuenta "$B_ROTAS" 22)"
chk "huerfano REAL cazado: references/huerfano-real.md"        "$(contiene "$B_HUERF" "references/huerfano-real.md")"
chk "palabra suelta NO salva: palabra-suelta.md es huerfana"   "$(contiene "$B_HUERF" "references/palabra-suelta.md")"
chk "mencion solo-historia NO salva: solo-en-historia.md huerfana" "$(contiene "$B_HUERF" "references/solo-en-historia.md")"
chk "auto-mencion NO salva: auto-salvada.md huerfana"          "$(contiene "$B_HUERF" "references/auto-salvada.md")"
chk "ruta de OTRA carpeta no salva: assets/mismo-nombre.md huerfana" "$(contiene "$B_HUERF" "assets/mismo-nombre.md")"
chk "URL no salva: references/remoto-url.md huerfana"          "$(contiene "$B_HUERF" "references/remoto-url.md")"
chk "F3 mencion en BITÁCORA no salva: solo-en-bitacora-may.md huerfana" "$(contiene "$B_HUERF" "references/solo-en-bitacora-may.md")"
chk "F5d es_historia anclada: precios-sin-changelog.md huerfana" "$(contiene "$B_HUERF" "references/precios-sin-changelog.md")"
chk "m8 limite derecho: el .bak NO salva → limite-der.md huerfana" "$(contiene "$B_HUERF" "references/limite-der.md")"
chk "m7 limite izquierdo: barra a la izquierda NO salva → limite-izq.md huerfana" "$(contiene "$B_HUERF" "references/limite-izq.md")"
chk "F1 glob no cruza barras: assets/sub/deep.json huerfana"   "$(contiene "$B_HUERF" "assets/sub/deep.json")"
chk "B1 glob AMPLIO tampoco cruza barras: deep-brand.txt huerfana (ni dudosa)" "$(contiene "$B_HUERF" "assets/brand/sub/deep-brand.txt")"
chk "A prosa ad-assets/imagenes/ NO fabrica cobertura: prosa-huerfana.png huerfana" "$(contiene "$B_HUERF" "assets/imagenes/prosa-huerfana.png")"
chk "A prosa: prosa-huerfana.png tampoco degradada a DUDOSO"   "$(no_contiene "$B_DUD" "prosa-huerfana.png")"
chk "v1.14 legado: motor-viejo.sh.viejo sin cita NO se salva por la cita .sh — queda en duda por el token desnudo scripts/, jamas exento" "$(contiene "$B_DUD" "scripts/motor-viejo.sh.viejo → sin cita; cubierta solo por el token desnudo 'scripts/'")"
chk "v1.14 legado: motor-viejo.sh.viejo NO exento en silencio (no huerfana porque esta en duda, no porque el .sh la salve)" "$(no_contiene "$B_HUERF" "motor-viejo.sh.viejo")"
chk "exactamente 13 huerfanas (ni mas ni menos)"               "$(cuenta "$B_HUERF" 13)"
chk "hermana existente con archivo faltante: no-existe.sh ROTA" "$(contiene "$B_SIS_ROTA" "skills/skill-hermana/scripts/no-existe.sh")"
chk "forma corta rota cazada: corta-rota.md ROTA"              "$(contiene "$B_SIS_ROTA" "skills/skill-hermana/references/corta-rota.md")"
chk "exactamente 2 hermanas rotas"                             "$(cuenta "$B_SIS_ROTA" 2)"
chk "exactamente 3 hermanas verificadas"                       "$(cuenta "$B_SIS_OK" 3)"
chk "exactamente 1 en el bloque info (ℹ️ con conteo exacto)"    "$(cuenta "$B_HERM" 1)"
chk "intruso examples/ marcado como ⚠️ mover a references/"    "$(contiene "$(cat "$OUT")" "mover a references/")"
chk "intruso examples/ listado en su bloque"                   "$(contiene "$B_INTRUSO" "examples")"
chk "intruso ya NO es 🔴"                                      "$(no_contiene "$(cat "$OUT")" "🔴 Material")"
A_TRUNC=$(grep -a 'apertura-larga' "$OUT" || true)
chk "F9 truncado por caracteres: lineas de apertura truncadas son UTF-8 valido" "$([ -n "$A_TRUNC" ] && printf '%s\n' "$A_TRUNC" | iconv -f UTF-8 -t UTF-8 >/dev/null 2>&1 && echo 1 || echo 0)"

echo "== ASERCIONES (direccion 3: la duda va a DUDOSOS, con conteo exacto) =="
chk "skills/ a carpeta inexistente → dudoso"                   "$(contiene "$B_DUD" "skill-inexistente")"
chk "externa faltante → dudoso: no-esta.sh"                    "$(contiene "$B_DUD" "no-esta.sh")"
chk "SKILL.md de skill fantasma → dudoso"                      "$(contiene "$B_DUD" "skill-fantasmagorica")"
chk "colision multi-hermana → dudoso con lista: compartida.md" "$(contiene "$B_DUD" "compartida.md → existe en 2 hermanas")"
chk "colision multi-hermana NO degradada a info"               "$(no_contiene "$B_HERM" "compartida.md")"
chk "duena unica sin nombrar → dudoso: de-otra.md"             "$(contiene "$B_DUD" "de-otra.md → existe solo en skill-otra")"
chk "duena unica sin nombrar NO degradada a info"              "$(no_contiene "$B_HERM" "de-otra.md")"
chk "SUBSTRING no es nombrar: de-sub.md → dudoso (skill-her ⊄ skill-hermana)" "$(contiene "$B_DUD" "de-sub.md → existe solo en skill-her")"
chk "SUBSTRING no es nombrar: de-sub.md NO degradada a info"   "$(no_contiene "$B_HERM" "de-sub.md")"
chk "token desnudo scripts/ NO exime: solo-por-dir.sh → dudoso" "$(contiene "$B_DUD" "solo-por-dir.sh → sin cita; cubierta solo por el token desnudo 'scripts/'")"
chk "token desnudo: solo-por-dir.sh NO en huerfanas (esta en duda, no exenta)" "$(no_contiene "$B_HUERF" "solo-por-dir.sh")"
chk "F1 glob amplio NO exime: brand/logo.txt → dudoso"         "$(contiene "$B_DUD" "assets/brand/logo.txt → sin cita; cubierta solo por el glob amplio 'assets/brand/*'")"
chk "F1 glob amplio: logo.txt NO en huerfanas (esta en duda, no exenta)" "$(no_contiene "$B_HUERF" "logo.txt")"
chk "F12 espacios: la rota con espacio va a DUDOSOS"           "$(contiene "$B_DUD" "references/con espacio roto.md → ruta con espacios citada que no existe")"
chk "F12 espacios: la rota con espacio NO en rotas (regla de la duda)" "$(no_contiene "$B_ROTAS" "con espacio roto.md")"
chk "B3 variable irresoluble → dudoso con prefijo declarado"   "$(contiene "$B_DUD" "no-existe-var.md → prefijo de variable sin resolver")"
chk "B3 variable irresoluble JAMAS en rotas"                   "$(no_contiene "$B_ROTAS" "no-existe-var.md")"
chk "B4-b2 cita imprecisa intra-skill → dudoso con la ruta real" "$(contiene "$B_DUD" "en-otra-carpeta.md → no está donde la cita dice, pero existe en la misma skill: skills/sub-uno/references/en-otra-carpeta.md")"
chk "B4-b2 cita imprecisa intra-skill NO en rotas"             "$(no_contiene "$B_ROTAS" "en-otra-carpeta.md")"
chk "B caso-der.md: el .viejo del citante NO la resuelve (compara_ruta con DER) — queda como cita imprecisa hacia sub-dos, no resuelta en silencio" "$(contiene "$B_DUD" "references/caso-der.md → no está donde la cita dice, pero existe en la misma skill: skills/sub-dos/references/caso-der.md")"
chk "DUDOSOS: 13 exacto"                                       "$(contiene "$(cat "$OUT")" "DUDOSOS: 13")"

echo "== ASERCIONES (corpus de regresion real) =="
chk "B2 frontera: ./ad-assets/ NO fabrica assets/demo-1.png (claude-ads)" "$(no_contiene "$B_ROTAS" "assets/demo-1.png")"
chk "B2 frontera: managed-agents/ NO fabrica agents/planner.md (claude-api)" "$(no_contiene "$B_ROTAS" "agents/planner.md")"
chk "B2 frontera: los prefijos-trampa tampoco caen en DUDOSOS" "$([ "$(contiene "$B_DUD" "demo-1.png")" -eq 0 ] && [ "$(contiene "$B_DUD" "planner.md")" -eq 0 ] && echo 1 || echo 0)"
chk "B3 \$CLAUDE_PLUGIN_ROOT resuelve contra la skill: plugin-var.md NO rota" "$(no_contiene "$B_ROTAS" "plugin-var.md")"
chk "B3 \$CLAUDE_PLUGIN_ROOT tambien salva: plugin-var.md NO huerfana" "$(no_contiene "$B_HUERF" "plugin-var.md")"
chk "B3 \${HOME} resuelto de verdad: por-home.md NO huerfana"  "$(no_contiene "$B_HUERF" "por-home.md")"
chk "B4 sub-skill (claude-ads): de-sub-skill.md NO rota (resuelve contra el citante)" "$(no_contiene "$B_ROTAS" "de-sub-skill.md")"
chk "C5 symlink que resuelve NO es rota: enlace-texto.md"      "$(no_contiene "$B_ROTAS" "enlace-texto.md")"
chk "C5 el texto tras el symlink salva: salvada-por-symlink.md NO huerfana" "$(no_contiene "$B_HUERF" "salvada-por-symlink.md")"
chk "C5 symlink en el listado de ARCHIVOS"                     "$(contiene "$(cat "$OUT")" "references/enlace-texto.md")"
chk "C5 secreto detras de symlink CAZADO (grep -r no lo veia)" "$(contiene "$(cat "$OUT")" "Posibles secretos hardcodeados")"
chk "C6 MAYUSCULA.MD citada NO huerfana"                       "$(no_contiene "$B_HUERF" "MAYUSCULA.MD")"
chk "C6 la cita dentro de un .MD mayuscula salva: viva-por-mayus.md NO huerfana" "$(no_contiene "$B_HUERF" "viva-por-mayus.md")"
chk "C6 sintaxis: scripts/roto.SH cazado por bash -n"          "$(contiene "$(cat "$OUT")" "roto.SH — error de sintaxis bash")"
chk "skill-prueba sin blindaje: el conteo N de M no inventa un PARCIAL" "$(no_contiene "$(cat "$OUT")" "PARCIAL")"

echo "== ASERCIONES (self-audit: es_yo + es_fixture del banco propio) =="
chk "es_yo: las cadenas del propio detector NO salvan → salvada-por-mi-echo.md huerfana" "$(contiene "$B2_HUERF" "references/salvada-por-mi-echo.md")"
chk "es_fixture en self-audit: mencion solo-fixture NO salva → solo-en-fixture.md huerfana" "$(contiene "$B2_HUERF" "references/solo-en-fixture.md")"
chk "es_fixture en self-audit: rota-fixture.md sembrada NO fabrica rota" "$(no_contiene "$B2_ROTAS" "rota-fixture.md")"
chk "self-audit: sin rotas en absoluto"                        "$(contiene "$(cat "$OUT2")" "✅ Sin referencias rotas")"
chk "self-audit: exactamente 2 huerfanas"                      "$(cuenta "$B2_HUERF" 2)"

echo "== ASERCIONES (F8: el verde no puede mentir) =="
chk "F8: con duda sin cita pendiente NO se imprime el verde"   "$(no_contiene "$(cat "$OUT3")" "✅ Sin archivos huérfanos")"
chk "F8: se declara cobertura — 0 confirmados y N en duda"     "$(contiene "$(cat "$OUT3")" "0 huérfanos confirmados · 1 en duda (ver DUDOSOS)")"

echo "== ASERCIONES (C7: contador de description — caracteres reales, corta en clave raiz CON digito) =="
DESCN=$(grep -oE 'description: ~[0-9]+' "$OUT3" | grep -oE '[0-9]+' | head -1)
chk "C7: ni el metadata ni version2: se suman, y el conteo es real (20..100)" "$([ -n "${DESCN:-}" ] && [ "$DESCN" -ge 20 ] && [ "$DESCN" -le 100 ] && echo 1 || echo 0)"

echo "== ASERCIONES (C8: blindaje N de M, nunca por un inodo) =="
chk "C8: raiz-sola-con-uchg NO es Blindada — se declara PARCIAL" "$(contiene "$(cat "$OUT4")" "Blindaje PARCIAL")"
chk "C8: el conteo dice 1 de 4 nodos con uchg"                 "$(contiene "$(cat "$OUT4")" "1 de 4 nodos con uchg")"

echo "== ASERCIONES (C9: bajo zsh el informe es IDENTICO — la guardia re-ejecuta) =="
chk "C9: zsh + guardia = misma cobertura declarada que bash"   "$(contiene "$(cat "$OUT3Z")" "0 huérfanos confirmados · 1 en duda (ver DUDOSOS)")"
chk "C9: zsh no imprime el verde mentiroso"                    "$(no_contiene "$(cat "$OUT3Z")" "✅ Sin archivos huérfanos")"

echo "== ASERCIONES (F5 v1.14: bajo sh — bash POSIX — el informe se re-ejecuta y sale COMPLETO) =="
chk "F5: sh entrega el informe hasta el final (sin truncado tras BLINDAJE)" "$(contiene "$(cat "$OUT3S")" "=== Inventario completo")"
chk "F5: sh declara la misma cobertura que bash"               "$(contiene "$(cat "$OUT3S")" "0 huérfanos confirmados · 1 en duda (ver DUDOSOS)")"

echo "== ASERCIONES (ANTI-VERDE v1.14: cada veredicto verde tiene su caso que lo engana y cae) =="
# verde "Blindada": skill-blindlink esta toda con uchg MENOS el destino del symlink
chk "anti-verde Blindada: el symlink a archivo mutable rompe el M de M → PARCIAL" "$(contiene "$(cat "$OUT5")" "Blindaje PARCIAL")"
chk "anti-verde Blindada: jamas se imprime Blindada con el agujero abierto" "$(no_contiene "$(cat "$OUT5")" "Blindada con chflags uchg")"
# verde de lectura (D): skill-000 tiene un chmod 000
chk "anti-verde lectura: chmod 000 produce el rojo NO LEIDOS con informe parcial" "$(contiene "$(cat "$OUT6")" "NO LEÍDOS — informe parcial")"
chk "anti-verde lectura: el archivo ilegible se lista"         "$(contiene "$(cat "$OUT6")" "references/oculto.md")"
chk "anti-verde lectura: el verde de secretos NO sale pelado (degradado a parcial)" "$(no_contiene "$(cat "$OUT6")" "✅ Sin patrones de secretos")"
chk "anti-verde lectura: el verde de rotas NO sale pelado"     "$(no_contiene "$(cat "$OUT6")" "✅ Sin referencias rotas")"
chk "anti-verde lectura: skill-prueba (todo legible) SI declara lectura completa" "$(contiene "$(cat "$OUT")" "✅ Todos los archivos del árbol se pudieron leer")"
# verde de secretos (F6): 9 familias sembradas una por linea en config-mala.md. El conteo
# EXACTO "5 de 9" es la prueba de cobertura completa: una familia que no case da 8, y el
# blob base64 de arte.md colandose daria 10 — el numero no puede mentir en ningun sentido.
B7_SEC=$(bloque "Posibles secretos hardcodeados" "$OUT7")
chk "F6 PEM PRIVATE KEY cazado (visible entre los 5 primeros)" "$(contiene "$B7_SEC" "BEGIN RSA PRIVATE KEY")"
chk "F6 sk-ant- cazado"                                        "$(contiene "$B7_SEC" "sk-ant-api03")"
chk "F6 AKIA cazado"                                           "$(contiene "$B7_SEC" "AKIAIOSFODNN7EXAMPLE")"
chk "F6 EAA de Meta cazado"                                    "$(contiene "$B7_SEC" "EAAabcdef")"
chk "F6 act_ cuenta publicitaria cazada"                       "$(contiene "$B7_SEC" "act_123456789012")"
chk "F6 conteo EXACTO 9 (contraseña, clave=, +57 y api_key cuentan; el base64 NO): mostrando 5 de 9" "$(contiene "$(cat "$OUT7")" "mostrando 5 de 9")"
chk "F6 anti-falso-positivo: el blob base64 de arte.md NO esta entre los hallazgos" "$(no_contiene "$B7_SEC" "arte.md")"
chk "F6 alcance declarado: el barrido dice que NO cubre JWT/ghp_/AIza" "$(contiene "$(cat "$OUT7")" "NO CUBRE: JWT")"
chk "F6 el alcance tambien se declara en el verde (skill-f8 sin secretos)" "$(contiene "$(cat "$OUT3")" "Alcance del barrido — CUBRE:")"
chk "F6 verde con alcance, nunca absoluto: skill-f8 dice 'en las familias cubiertas'" "$(contiene "$(cat "$OUT3")" "Sin patrones de secretos en las familias cubiertas")"
# verde "sin signos": la trampa de apertura los tiene
chk "anti-verde signos: skill-prueba SI reporta signos de apertura" "$(contiene "$(cat "$OUT")" "Signos de apertura ¿ ¡ encontrados")"
# verde "sin intrusos": examples/ en skill-prueba (ya asertado) y el colado del plugin abajo

echo "== ASERCIONES (F8 v1.14: modo plugin) =="
chk "plugin: encabezado REPO PLUGIN con 2 sub-skills"          "$(contiene "$(cat "$OUT8")" "REPO PLUGIN con 2 sub-skill(s)")"
chk "plugin: sin CRITICO por SKILL.md raiz"                    "$(no_contiene "$(cat "$OUT8")" "CRÍTICO: no existe SKILL.md")"
chk "plugin: LICENSE no es intruso"                            "$(no_contiene "$(bloque "NO estándar de plugin" "$OUT8")" "LICENSE")"
chk "plugin: tests no es intruso"                              "$(no_contiene "$(bloque "NO estándar de plugin" "$OUT8")" "tests")"
chk "plugin: .claude-plugin no es intruso"                     "$(no_contiene "$(bloque "NO estándar de plugin" "$OUT8")" ".claude-plugin")"
chk "plugin anti-verde intrusos: el archivo-colado.txt SI se caza" "$(contiene "$(bloque "NO estándar de plugin" "$OUT8")" "archivo-colado.txt")"
chk "skill normal NO se marca como plugin"                     "$(no_contiene "$(cat "$OUT")" "MODO PLUGIN")"

echo "== PARIDAD banco↔detector (tripwire: rama nueva sin caso sembrado = banco en rojo) =="
# El manifiesto: patron EXACTO de cada rama (texto hasta el parentesis) + el caso que la cubre.
# Campos separados por TAB. Crece con el detector: rama nueva → caso nuevo → linea nueva aqui.
MAN="$T/manifiesto"
cat > "$MAN" <<'EOF'
gsavar-*/*	casos plugin-var.md (B3, $CLAUDE_PLUGIN_ROOT resuelve contra la skill) / no-existe-var.md (B3, DUDOSO con prefijo declarado)
../*	casos rel-subida.md (viva contra el citante) / rota-rel.md (rota) — E v1.14
*skills/*/*	casos hermana-OK/hermana-ROTA/skill-inexistente/portada-fantasma + colapso-viva.md (normalizada antes de llegar aqui)
"~"*|/*	casos externa-OK (externo.sh) / externa-faltante (no-esta.sh)
*	casos local (rota-real) / forma corta (corta.md, corta-rota.md) / sister_valida (rel-subida via ..)
HIST:changelog|changelog[-_.]*|bitacora|bitacora[-_.]*|bitácora|bitácora[-_.]*|historial|historial[-_.]*	casos changelog.md (borrado-historico, solo-en-historia) + BITÁCORA.md (F3) + precios-sin-changelog (F5d, sufijo NO exime)
HIST:*	caso: todo lo demas es texto vivo
FIX:autoprueba|autoprueba[-_.]*|selftest|selftest[-_.]*|fixture|fixtures|fixture[-_.]*|fixtures[-_.]*	casos fixture-caso.md en skill-selfaudit (rota-fixture, solo-en-fixture); F7: fuera de self-audit selftest.py cuenta (cargada-por-selftest)
FIX:*	caso: todo lo demas es texto vivo
EOF

ramas_de_case() {  # $1=archivo $2=ancla textual de apertura del case
  awk -v a="$2" 'index($0,a){f=1;next} f&&/^[[:space:]]*esac/{exit} f' "$1" \
    | grep -E '^[[:space:]]*[^ =$#]+\)' \
    | sed -E 's/^[[:space:]]*//; s/\).*$//'
}
RAMAS="$T/ramas"
{ ramas_de_case "$INV" 'case "$tok" in'
  ramas_de_case "$INV" 'es_historia() {' | sed 's/^/HIST:/' | grep -v '^HIST:case' || true
  ramas_de_case "$INV" 'es_fixture() {' | sed 's/^/FIX:/' | grep -v '^FIX:case' || true
} > "$RAMAS"
N_RAMAS=$(grep -c . "$RAMAS")
chk "paridad: el extractor encuentra ramas (no esta ciego)" "$([ "$N_RAMAS" -ge 8 ] && echo 1 || echo 0)"
while IFS= read -r r; do
  [ -z "$r" ] && continue
  if grep -qF -- "$r	" "$MAN" || grep -qF -- "$r$(printf '\t')" "$MAN"; then
    PASAN=$((PASAN+1)); echo "  PASA  paridad: rama con caso — $r"
  else
    FALLAN=$((FALLAN+1)); echo "  FALLA rama sin caso: $r (siembra el caso y dala de alta en el manifiesto)"
  fi
done < "$RAMAS"
while IFS=$'\t' read -r r c; do
  [ -z "$r" ] && continue
  if grep -qxF -- "$r" "$RAMAS"; then
    PASAN=$((PASAN+1)); echo "  PASA  paridad: manifiesto vigente — $r"
  else
    FALLAN=$((FALLAN+1)); echo "  FALLA caso sin rama: $r (la rama cambio o se fue; actualiza el manifiesto)"
  fi
done < "$MAN"

echo ""
echo "AUTOPRUEBA: $PASAN pasan, $FALLAN fallan (de $((PASAN+FALLAN)))"
if [ "$FALLAN" -gt 0 ]; then
  echo "--- salida completa del inventario (skill-prueba) para diagnostico ---"
  cat "$OUT"
  echo "--- salida self-audit ---"
  cat "$OUT2"
  echo "--- salida f8 ---"
  cat "$OUT3"
  echo "--- salida secretos ---"
  cat "$OUT7"
  echo "--- salida plugin ---"
  cat "$OUT8"
  exit 1
fi
exit 0
