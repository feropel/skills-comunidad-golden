---
name: golden-skill-auditor
description: >-
  Golden Group — AUDITOR MAESTRO de skills. Entra a cualquier skill instalada en
  ~/.claude/skills, la lee COMPLETA de inicio a fin (SKILL.md + references +
  scripts + assets, sin omitir un solo archivo), la califica sobre 1000 puntos
  con una rúbrica fija de 7 dimensiones, reporta qué está bien, qué está mal y
  qué le falta, y la ARREGLA hasta dejarla mil de mil: reestructura, optimiza
  el disparo (description), pule instrucciones, repara referencias rotas,
  valida scripts y verifica los estándares Golden (prefijo, autonomía, cero
  datos privados, blindaje). Úsala SIEMPRE que el usuario quiera: auditar,
  evaluar, calificar, revisar, optimizar, mejorar, perfeccionar o "dejar mil de
  mil" una skill; sepa qué le falta a una skill; diga "audita esta skill",
  "revisa la skill X", "qué le falta a mi skill", "optimiza la skill",
  "califícame esta skill", "está bien estructurada mi skill", "mejora todos
  los procesos de la skill". Dispara aunque no diga "auditar": basta con que
  pida diagnóstico o mejora de una skill existente. Línea divisoria con
  skill-creator: diagnosticar, calificar y reparar una skill EXISTENTE = esta
  skill; crear una skill desde cero o correr evals con subagentes =
  skill-creator. Tampoco es para auditar PDFs (golden-pdf-check) ni seguridad
  de código de apps (cyber-neo).
---

# Golden Skill Auditor — auditoría y reparación de skills mil de mil

<!-- skill v1.13 — 2026-08-22 — AUTO-AUDITORÍA (esta skill se aplicó a sí misma): inventario.sh 147/147 + sabotajes 38/38 en verde, self-audit sin rotas/huérfanas/dudosos, sintaxis OK, sin secretos reales (solo el fixture a propósito del banco), blindaje 8/8. Investigado el hallazgo reportado en la auditoría de golden-chatea-pro-config-comentarios ("inventario.sh reportó chflags uchg cuando el mecanismo real era chmod 0444/0555"): CONFIRMADO real mecanismo de esa skill = chmod (0 nodos con uchg, 0 escribibles, verificado con find -flags/-perm y ls -lO), pero el bug YA estaba corregido antes de esta sesión por el fix C8 de la v1.12 (blindaje contado N de M nodos con rama chmod separada, `find -perm +0200`) — corrida en vivo contra esa skill hoy: "Blindada por permisos chmod — 0 de 6 nodos escribibles", NUNCA chflags uchg. Único hallazgo nuevo real (Recursos): dependencias de scripts (perl, python3, node) no estaban declaradas con su fallback en Fase 0 — agregado el punto 4. Esta skill misma resultó estar blindada por AMBOS mecanismos a la vez (chflags uchg Y chmod 0444/0555) — redundante pero no dañino; se re-blinda con el estándar de la casa (chflags -R uchg) al cerrar. -->
<!-- skill v1.12 — 2026-08-21 — ronda contra el CUARTO expediente adversarial (v1.11 NO RATIFICADA). Principio rector de la ronda: toda regla arreglada en un sitio se busca en su GEMELO antes de sellar — las 3 bloqueantes eran la misma forma (la regla existía en una rama y faltaba en la hermana). inventario.sh: B1 el glob AMPLIO también respeta barras (la rama que lo manda a DUDOSOS usaba prefijo crudo case "$rel" in "$pbase"/* donde * cruzaba /; ahora glob_matches TAMBIÉN ahí — references/* cubre UN nivel y references/hondo/masfondo/hondisimo.md profundo sin cita vuelve a ser huérfano); B2 FRONTERA IZQUIERDA compartida (constantes FRONT+PFX, UNA sola para REF_RE/GLOB_RE/ROOT_RE): el segmento canónico no abre cita con guion o letra pegada — "./ad-assets/x.png" fabricaba assets/x.png (12 de las 43 "rotas" de claude-ads) y "managed-agents/" fabricó la ÚNICA "rota" de claude-api; extracción por perl con lookbehind y delimitador m{} (el patrón está lleno de /; con m/.../ perl moría y un 2>/dev/null lo volvía verde mentiroso — ese stderr ya NO se traga y el rc se grita); B3 prefijos de VARIABLE como CLASE, no 3 literales: ${HOME}/$HOME se resuelven de verdad (ruta absoluta reconocible), cualquier otro $VAR/, ${VAR}/, <VAR>/ pegado al segmento canónico se resuelve contra la skill → hermanas → DUDOSOS con el prefijo declarado, JAMÁS rojo ($CLAUDE_PLUGIN_ROOT sembrado); B4 resolución SIMÉTRICA de rotas — la misma escalera que los huérfanos: (a) dir del citante, (b) raíz, (b2) sufijo con frontera de segmento en OTRA carpeta de la misma skill → DUDOSO "cita imprecisa" (gemelo intra-skill de EN_HERMANA), (c) hermanas; solo rojo si todo falla (claude-ads: 26/43 existían resueltas contra el citante — estructura de sub-skills — y 4 más en ads/references/; contraste medido claude-ads 43→1, claude-api 1→0); C5 SYMLINKS de verdad (find -L en listado, texto vivo, EXISTING, señales, sintaxis; grep -r de BSD no los sigue y un symlink a un archivo con api_key salía "Sin patrones"; symlink que resuelve = existente, el que no = listado aparte); C6 extensiones en MAYÚSCULAS (.MD/.SH) vía minusculas() e -iname en todas las superficies; C7 el contador de description corta en la siguiente clave YAML raíz, no solo en --- (watch: 520 impresos vs ~247 reales, 21/92 skills); C8 blindaje por N de M nodos (find -flags +uchg), nunca por el inodo de la raíz — "Blindada" solo M de M, si no "PARCIAL: N de M" en rojo, gemelo chmod contado igual; C9 guardia de shell (sin BASH_VERSION → exec bash o muere: zsh sin word-splitting dejaba TEXT_EXTS como un token y el informe salía verde MENTIROSO); C10 límites DECLARADOS en Fase 0 (rutas externas sin segmento canónico fuera de alcance, globs segmento a segmento, sin normalización NFD) y TERCERA limitación del sello en Fase 5 (find -type f no ve symlinks: repuntar un enlace no altera md5 ni conteo — variante que sí los cuenta declarada). autoprueba_inventario.sh: CORPUS DE REGRESIÓN REAL — sección nueva con casos COPIADOS de skills reales que el constructor NO eligió, origen documentado (sub-skills de claude-ads, prefijos-trampa ad-assets/managed-agents, $CLAUDE_PLUGIN_ROOT y ${HOME}, .MD/.SH reales, trío de symlinks del verificador, description con metadata de watch) y REGLA ESCRITA: cada ronda de reparación añade al corpus al menos un caso de una skill real que el constructor no eligió; cuarto sandbox skill-blind (raíz sola con uchg = PARCIAL); f8 corre también bajo zsh y su description con metadata prueba C7; guardia de shell propia; suite de sabotajes 29→38 (s17 frontera, s18 rescate-citante, s19 $VAR, s20 find sin -L, s21 -iname, s22 corte de description, s23 blindaje un inodo, s24 guardia shell, s25 sufijo interno). LECCIÓN DE LA PROPIA RONDA (gemelos también en el banco): dos sabotajes viejos quedaron NEUTRALIZADOS por redundancia del detector nuevo — s4 (EXISTING sin SKILL.md) dejó de doler porque el rescate de raíz (b) salva por -e directo, y s11 (strips literales de $SKILL_DIR) porque la clase genérica $VAR es su superconjunto; el código redundante se RETIRÓ (una regla, un lugar) y ambos sabotajes se repuntaron al blanco vivo: s4 = EXISTING mutilado + sin rescate (b), s11 = prefijo HOME sin resolver (caso sembrado ${HOME}/taller/scripts/externo.sh — sin resolución fabrica la rota scripts/externo.sh). Cifras medidas 2026-08-21: banco 147/147 bash y 147/147 zsh (idéntico), sabotajes bash 38/38 mordidos + muestreo zsh 3/3 (s17, s20, s24), contrastes claude-ads 43→1 rotas (la residual scripts/foo.py es un placeholder de doc en tests/, evaluada a mano; 4 pasan a DUDOSO "cita imprecisa" con su ruta real ads/references/ declarada), claude-api 1→0 (la fabricada murió), all-deploy 0/0, golden-pdf-check 0/0, golden-web 0/0, self-audit 0 rotas 0 huérfanas 0 dudosos -->
<!-- skill v1.11 — 2026-08-21 — ronda contra el tercer expediente adversarial (v1.10 NO RATIFICADA, 12 fallas). inventario.sh: F1 el * de un glob ya NO cruza barras (glob_matches compara segmento a segmento: assets/*.json ya no cubre assets/sub/deep.json) y el glob AMPLIO de carpeta (dir/*) deja de eximir en silencio — va a DUDOSOS igual que el token desnudo (un references/* en un test de claude-ads apagaba la carpeta entera); F2 normalización SIMÉTRICA en limpia_texto, la ÚNICA función por la que pasa el texto de las DOS direcciones: los prefijos $SKILL_DIR/, ${SKILL_DIR}/, <SKILL_DIR>/ (idioma de cita de las skills oficiales) y la ruta absoluta propia se descuentan igual en rotas y en huérfanos (antes $SKILL_DIR/references/x.md como única cita dejaba a x.md huérfana, y <SKILL_DIR>/scripts/audit.py fabricaba el DUDOSO /scripts/audit.py en all-deploy); F3 pliegue español explícito (minusculas(): tr no pliega acentos en locale C — BITÁCORA.md no casaba es_historia), aplicado en todo sitio que compara en minúsculas; F5c menciona_ruta endurece el límite DERECHO (tras el match no puede seguir .alfanumérico: guia.md.bak ya no salva a guia.md) y los límites viven en IZQ_LOCAL/IZQ_ABS/DER_RUTA saboteables; F6 lista de formatos UNIFICADA en TEXT_EXTS (una variable para referencias, ARCHIVOS y SEÑALES; +.txt .yml .css .xml .yaml — ci.yml de all-deploy y golden-print.css de golden-pdf-check eran citas vivas invisibles); F7 es_fixture solo exime en contexto SELF-AUDIT (ES_SELF_AUDIT): los selftest/autoprueba de otras skills son scripts reales y sus citas cuentan (assets/selftest-sample.md de golden-pdf-check sale de DUDOSOS); F8 el verde de huérfanos no se imprime con archivos sin cita en DUDOSOS — "0 huérfanos confirmados · N en duda"; F9 truncado por CARACTERES (trunca() con python3), no por bytes (cut -c partía multibyte y imprimía mojibake), y los bloques de señales reportan rutas RELATIVAS; F12 rutas con espacios entre backticks/comillas cuentan (existente=viva, faltante=DUDOSO por regla de la duda — claude-ads tiene 5 archivos con espacio). autoprueba_inventario.sh: TRES sandboxes (banco principal + self-audit para es_yo/es_fixture + caso F8), un caso por CADA formato de TEXT_EXTS en las DOS direcciones, casos m7/m8, BITÁCORA.md, precios-sin-changelog.md (el que SKILL.md citaba como medido y no estaba sembrado), normalización, espacios, glob amplio/profundo y trampa de truncado verificada con iconv; suite de sabotajes ampliada a 29 (s1-s16 + 13 formatos) — REGLA DE LA CASA: toda corrección nueva del detector entra con su sabotaje en la suite, viva donde viva (los 9 sabotajes de comportamiento que el tripwire de ramas no cubría ahora muerden). Además: F10 UNA regla de puntaje idéntica en SKILL.md y rubrica.md (base determinista = suma tras restas; ajuste holístico declarado aparte con su porqué); F11 estandares-golden.md deja de fijar censo de la familia chatea (arsenal vivo, ejemplos marcados como ejemplos); EXTRA receta del md5 canónico declarada en Fase 5 con su limitación (no incluye nombres; el conteo de archivos acompaña siempre) -->
<!-- skill v1.10 — 2026-08-21 — ronda contra el segundo expediente adversarial (v1.9 NO RATIFICADA). TRES CLASES MADRE muertas en inventario.sh, no parcheadas: CLASE 1 identidad por SUBSTRING — (g) la guardia "dueña única Y nombrada" casa el nombre de la hermana con límites de palabra (nombra_duena; guion/guion bajo son parte del nombre): "cro" ya no matchea dentro de 33 skills ni copywriting dentro de golden-copywriting, y sin nombre con límites → DUDOSOS; (h) es_historia/es_fixture ANCLADOS a nombre base exacto o prefijo estricto clave+[-_.] — "precios-sin-changelog.md" ya no queda exento (el sufijo se prohibió a propósito: cualquier sufijo re-admite ese caso); (i) el rescate de huérfanos casa la RUTA RELATIVA COMPLETA (dir+base, desde la raíz, en forma absoluta de esta skill, o resuelta desde el dir del citante) con límites — references/manual.md ya no salva a scripts/manual.md — y las URLs (esquema://) se borran del texto antes de extraer refs y de casar menciones. CLASE 2 cobertura sin ancla — (j) el token DESNUDO ("references/", "scripts/" pelados) NO exime huérfanos: cobertura real = dir específico, glob o cita; lo cubierto solo por token desnudo va a DUDOSOS (cobertura total explícita se declara con glob scripts/*); (k) autoexclusión es_yo: en self-audit las cadenas/echo del propio inventario.sh no cuentan como mención (su ":296 mover a references/" se auto-eximía). CLASE 3 banco de memoria — (l) TRIPWIRE DE PARIDAD en autoprueba_inventario.sh: extrae textualmente las ramas de los case del detector (clasificador de tokens + es_historia + es_fixture) y las compara contra un MANIFIESTO declarado en el banco; rama nueva sin caso = "rama sin caso: X" y banco en rojo, manifiesto huérfano = "caso sin rama: X" — la promesa v1.9 de "un caso por cada rama" pasa de manual a verdadera POR CONSTRUCCIÓN; además modo `sabotajes` re-corrible: s1 dueña -eq→-ge, s2 es_fixture apagado, s3 autoexclusión del rescate quitada, s4 SKILL.md fuera de EXISTING, s5 manifiesto mutilado — los 5 TUMBAN el banco (medido 2026-08-21: 67/67 en verde y 5/5 mordidos). Puntuales: (m) .js entra al barrido de texto vivo (SINTAXIS ya le corría node --check); .ts evaluado: cero en el arsenal, no se agrega hasta que exista; (n) rutas citadas aceptan áéíóúñü y mayúsculas (clases de bytes UTF-8, funcionan en locale C y UTF-8) con caso acentuado sembrado en ambas direcciones; cifras de censo del arsenal ya no se fijan en el texto vivo (se derivan al correr) -->
<!-- v1.10.1 (2026-08-21, centro de mando): SELF_PATH del banco capturado en nivel superior — bajo zsh, $0 dentro de funciones es el nombre de la funcion y el modo sabotajes moria en silencio (5/5 en bash, 4/5 en zsh); ahora identico en ambos shells. Caso: corrida de verificacion del CdM. -->
<!-- skill v1.9 — 2026-08-21 — ronda contra el expediente del verificador adversarial (v1.8 NO RATIFICADA). inventario.sh: (a) el escaneo de referencias vivas barre .md .py .sh .json .liquid .html .csv, no solo .md (rota citada en comentario de un .py era invisible); (b) citas de directorio RELATIVAS desde dentro de references/ se resuelven contra el directorio del archivo que cita (caso golden-web: arte-generativo-templates/ dejaba 2 huérfanos falsos); (c) la degradación cross-skill a ℹ️ exige dueña ÚNICA + mención de esa hermana por nombre en el texto vivo — cualquier otra colisión va a DUDOSOS con la lista (66 rutas relativas vivían en 2+ skills del arsenal — censo de ese día; la cifra no es vigente, se deriva al correr); (d) skills/<hermana>/SKILL.md ahora se captura y verifica (antes invisible por exigir segmento canónico); (e) SIMETRÍA de historia en huérfanos: la mención que salva debe estar en texto vivo (sin changelogs, sin comentarios HTML, sin fixtures) y parecer ruta ("/nombre.ext") — una palabra suelta no salva; (f) material intruso baja de 🔴 a ⚠️ "mover a references/" (no es rotura, es orden). autoprueba_inventario.sh reescrita: extractores de bloque para TODAS las secciones (rotas, huérfanas, ℹ️, DUDOSOS, hermanas rotas, hermanas OK, intrusos), un caso sembrado por CADA rama del case (promesa manual en esta versión; desde v1.10 la garantiza por construcción el tripwire de paridad), conteos exactos por bloque — 38/38 con el detector de esa versión, y los 4 sabotajes del verificador (s7 rotas-de-hermana-como-OK, s8 sin-forma-corta, s9 sin-rescate-EN_HERMANA, s10 hermana-nunca-existe) hacen FALLAR el banco (mordida demostrada sobre copias en tmpdir). SKILL.md:puntero py_compile sin número de línea muerto; estandares-golden.md deja de afirmar el blindaje de terceros y lo marca como foto fechada -->
<!-- skill v1.8 — 2026-08-21 — inventario.sh: detector de referencias reescrito contra las 5 clases de falso positivo del autoevalúo 2026-08-19/20: (1) cross-skill se verifica contra ~/.claude/skills, con rescate de citas escritas como locales que en realidad viven en una hermana (caso golden-ads → 01-investigacion-360.md, ahora línea informativa, no rotura); (2) rutas con ~ se expanden antes de probar existencia; (3) citas por directorio o glob cubren huérfanos (los 42 componentes vivos de golden-shopify y las fonts de golden-pdf-check salieron de la lista de borrado); (4) comentarios HTML <!== ==> son historia, no referencias vivas; (5) archivos changelog/bitácora/historial son historia — sus menciones no cuentan como refs vivas (las 3 "rotas" de golden-investigacion-mercado eran entradas de changelog) y ellos mismos nunca son huérfanos. Huérfano = archivo cuyo NOMBRE no aparece en ningún archivo de texto de la skill y que ningún directorio/glob citado cubre. Ante duda NO se marca rojo: se cuenta en la línea DUDOSOS: N. Nuevo scripts/autoprueba_inventario.sh: banco adversarial sembrado en tmpdir (5 clases + huérfano por glob que NO deben marcarse, más rota REAL y huérfano REAL que SÍ) — 16/16 con el script nuevo y 10 fallas de 16 con el viejo, o sea el banco sabe morder. Conserva intacto el arreglo v1.7 de hermanas short-form. Contraste real de banderas rojas: golden-shopify 42→0, golden-ads 2→0, golden-investigacion-mercado 3→0, golden-pdf-check 7→1 (brand.md, hueco de cita genuino) -->
<!-- skill v1.7 — 2026-08-11 — inventario.sh reconoce la forma CORTA de rutas a hermanas (`<hermana>/references/x.md` sin prefijo skills/): antes el mismo archivo salía ✅ verificado como hermana Y 🔴 roto como local (falso rojo medido en golden360, reportado por su fábrica vía red sináptica); ahora la forma corta se verifica contra la hermana y solo lo local sin dueño existente cuenta como local. Probado contra caso malo plantado: la rota local y la hermana-corta rota siguen cazándose. · v1.6 · inventario.sh detecta material intruso que se publicaría al marketplace (carpetas fuera de references/scripts/assets/agents, archivos sueltos en la raíz) — cazó un .claude/settings.local.json auto-shippeado; changelog reconoce **Versión** y ## Changelog además del comentario HTML; rúbrica cita ast.parse en vez de py_compile -->
<!-- skill v1.5 · inventario.sh distingue skills hermanas: menciones con ruta a ~/.claude/skills/<otra>/ se verifican contra la hermana (existe = verificada, no existe = rota aparte) en vez de marcarse como referencia local rota -->
<!-- skill v1.4 · puntaje HOLÍSTICO: el total es un veredicto de calidad real del conjunto, no una suma que se rellena hasta 1000; nunca inflar con features de relleno; reserva que solo cierra el uso real se declara y baja el número con honestidad (feedback FER 2026-07-12) -->
<!-- skill v1.3 · blindaje al cierre: skill golden- que cierra en 1000 sin pendientes se blinda sola (chflags uchg); terceros y skills con pendientes no se blindan -->
<!-- v1.2 · meta de reparación = 1000 EXACTO (no ≥950): si el hallazgo tiene evidencia se arregla; solo se detiene antes por puntos que dependan de un dato del dueño -->
<!-- v1.1 · auto-auditada 900→1000: ast.parse en vez de py_compile (falso error en blindadas), backups a ~/.claude/skill-backups (no contaminar skills/), rollback si la reparación empeora, manejo de nombre no encontrado, ejemplo de hallazgo, barrido  multi-formato, frontera nítida con skill-creator -->
<!-- v1.0 · rúbrica 1000 pts / 7 dimensiones · inventario por script · protocolo de reparación con blindaje -->

Esta skill convierte cualquier skill instalada en una skill de nivel comunidad: la lee entera, la mide contra una rúbrica fija de 1000 puntos, entrega un informe accionable y aplica los arreglos. El estándar de salida es el mismo que ya alcanzaron golden-investigacion-mercado y golden-pdf-check: lista para usarse mil veces sin supervisión.

**Principio rector:** una skill se audita como se auditaría un empleado nuevo — no por lo que dice que hace, sino por lo que un modelo que la lea por primera vez lograría hacer con ella. Cada hallazgo debe responder: "si Claude ejecuta esta skill mañana en un chat limpio, dónde se tropieza".

## Modos de operación

Detecta el modo por lo que pidió el usuario. En la duda, aplica AUDITA+ARREGLA (es lo que casi siempre quiere).

| El usuario dice | Modo |
|---|---|
| "audita", "califica", "qué le falta", "revísala" | **AUDITA** — informe completo + plan de arreglo, sin tocar archivos |
| "mejórala", "arréglala", "déjala mil de mil", "optimízala", "perfecciónala" | **AUDITA+ARREGLA** — informe + reparación + re-auditoría hasta 1000 |

Regla de autonomía Golden: decide todo lo decidible por convención e INFORMA. No preguntes qué arreglar — la rúbrica lo dicta. La única pregunta permitida es cuando falta información que solo el usuario tiene (ej. cuál skill auditar si no la nombró y hay ambigüedad real).

## Flujo completo

### Fase 0 — Localizar y radiografiar

1. Resuelve la ruta: `~/.claude/skills/<nombre>` (sigue symlinks si los hay). Si no existe con ese nombre exacto (typo, nombre a medias como "la de carritos"), lista `~/.claude/skills/`, elige la coincidencia más cercana, INFORMA cuál elegiste y sigue. Solo pregunta si hay dos candidatas realmente ambiguas.
2. Corre el inventario determinista:
   ```bash
   bash ~/.claude/skills/golden-skill-auditor/scripts/inventario.sh <ruta-de-la-skill>
   ```
   El script reporta: blindaje contado por N de M NODOS (find -flags +uchg contra el total; "Blindada" solo con M de M — un solo inodo con uchg en la raíz es "PARCIAL" en rojo, y el gemelo chmod se cuenta igual), árbol de archivos con líneas (symlinks que resuelven incluidos vía find -L, y los que no resuelven listados aparte), frontmatter (la description se cuenta cortando en la SIGUIENTE clave YAML de nivel raíz, no solo en el --- de cierre — license/metadata/allowed-tools no se suman), referencias rotas (mencionadas pero inexistentes, barriendo texto vivo en TODOS los formatos de TEXT_EXTS: .md .txt .py .sh .js .json .css .html .xml .yaml .yml .liquid .csv — una sola lista compartida con ARCHIVOS y SEÑALES, con extensiones también en MAYÚSCULAS vía -iname; una cita solo es rota si falla la escalera completa: dir del citante → raíz de la skill → sufijo en otra carpeta de la misma skill (→ DUDOSO "cita imprecisa") → hermanas), archivos huérfanos (existen pero ninguna cita con la ruta relativa completa los menciona; el segmento canónico solo abre cita con frontera izquierda limpia — jamás un guion o letra pegada, "ad-assets/" no fabrica citas de assets/ — y los prefijos de variable se tratan como clase: ${HOME}/$HOME se resuelven de verdad, $SKILL_DIR/, ${SKILL_DIR}/ y <SKILL_DIR>/ se descuentan, y cualquier otro $VAR//<VAR>/ se resuelve contra la skill o va a DUDOSOS con el prefijo declarado, nunca a rojo), la línea DUDOSOS con lo que exige confirmación a mano (incluye lo cubierto solo por un token desnudo tipo "references/" pelado o por un glob amplio tipo "scripts/*", que NO eximen — y el glob amplio también respeta las barras: references/* alcanza UN nivel, no toda la profundidad — y las rutas con espacios citadas entre backticks/comillas que no existen), y chequeo de sintaxis de scripts (bash -n / ast.parse de Python / node --check, symlinks y .SH en mayúsculas incluidos, sin escribir nada en la skill auditada). Cuando no hay huérfanos confirmados pero sí archivos sin cita en DUDOSOS, el informe dice "0 huérfanos confirmados · N en duda" — nunca el verde pelado.
   Límites DECLARADOS del detector (existen; callarlos sería mentir por omisión): (1) las rutas externas SIN segmento canónico (~/lab/bin/x.sh, sin references|scripts|assets|agents ni skills/<otra>/SKILL.md) quedan FUERA del alcance del barrido de referencias — el detector no puede distinguirlas de prosa; (2) los globs se comparan segmento a segmento estilo pathlib (el * nunca cruza /), también en la rama de DUDOSOS; (3) no hay normalización Unicode NFD↔NFC: macOS guarda nombres en NFD y una cita tecleada en NFC de un nombre acentuado puede no casar byte a byte — ante un huérfano/rota con acentos, confirmar a mano antes de creerle.
   Si vas a tocar el detector de referencias, corre antes y después su banco adversarial:
   ```bash
   bash ~/.claude/skills/golden-skill-auditor/scripts/autoprueba_inventario.sh
   bash ~/.claude/skills/golden-skill-auditor/scripts/autoprueba_inventario.sh sabotajes
   ```
   El banco siembra un árbol en tmpdir, corre todas sus aserciones con conteo exacto por bloque y además verifica PARIDAD banco↔detector: extrae las ramas de los case de inventario.sh y las compara contra su manifiesto de casos — una rama nueva sin caso sembrado pone el banco en rojo con "rama sin caso: X", así que "un caso por cada rama" es verdad por construcción, no por memoria del constructor. El modo `sabotajes` auto-verifica la mordida: aplica sabotajes conocidos al detector en copias tmpdir y exige que el banco los tumbe. El tripwire de ramas cubre los case; los COMPORTAMIENTOS fuera de case los cubre la regla de la casa: **toda corrección nueva del detector entra con su sabotaje en la suite, viva donde viva** (así la suite integrada cubre todo lo declarado en el changelog, no solo lo que un case delata). Un cambio al detector sin banco Y sabotajes en verde no se sella, y el banco debe pasar idéntico bajo bash y zsh.
3. Si el script falla o no existe, haz el inventario a mano con `find`, `wc -l` y lectura del frontmatter — la auditoría no se detiene por el script.
4. Dependencias del script (binarios en PATH, sin librerías externas): `bash` (guardia C9 re-ejecuta si el shell activo no es bash), `perl` (extracción de referencias — si falta, la extracción muere con `🔴 ERROR: extracción de referencias (perl) falló` y esa sección del informe no es confiable, el resto sigue), `python3` (validación de sintaxis `.py` vía `ast.parse` y el truncado seguro de líneas largas — si falta, esos dos puntos fallan silenciosamente: un `.py` roto puede reportarse como sintaxis OK y las líneas truncadas de SEÑALES pueden salir vacías; confirmar ambos a mano si `python3` no está en PATH), y opcionalmente `node` (solo para `node --check` de `.js`; su ausencia ya se reporta como advertencia en el propio informe, no detiene nada). Sin fallback automático: si falta `perl` o `python3`, la Fase 0 sigue con el inventario a mano del punto 3 para lo que ese binario cubría.

### Fase 1 — Lectura total

Lee TODOS los archivos de la skill, completos, sin excepción: SKILL.md, cada reference, cada script, cada asset legible. Los archivos >2000 líneas se leen por tramos hasta cubrirlos enteros. Esta fase no se recorta: una auditoría que no leyó todo no puede afirmar "no omití ningún detalle", que es exactamente la promesa de esta skill. Mientras lees, anota en una lista corrida cada fricción con su archivo:línea.

### Fase 2 — Calificación por rúbrica

Lee `references/rubrica.md` y califica las 7 dimensiones (1000 pts en total):

1. **Activación** (120) — el description dispara cuando debe y NO dispara cuando no debe
2. **Estructura** (140) — divulgación progresiva, SKILL.md ≤500 líneas, punteros claros
3. **Instrucciones** (200) — imperativas, con el porqué, sin contradicciones, con ejemplos
4. **Proceso y flujo** (180) — pasos completos, defaults autónomos, manejo de errores, definición de "terminado"
5. **Recursos** (120) — scripts que corren, referencias vivas, sin archivos muertos
6. **Estándares Golden** (120) — lee `references/estandares-golden.md` y verifica cada uno
7. **Robustez** (120) — versionado, consistencia interna, degradación elegante

Cada punto restado necesita evidencia citable (archivo:línea o ausencia concreta). Prohibido restar "por sensación".

Regla de puntaje (ÚNICA, escrita idéntica en SKILL.md Fase 2 y en references/rubrica.md, Cálculo y veredicto): la BASE del puntaje es determinista — la suma de las 7 dimensiones tras las restas con evidencia (mínimo 0 por dimensión). Sobre esa base se admite UN ajuste holístico, declarado APARTE con su porqué (ej. una reserva que solo cierra el uso real, o un defecto transversal que las dimensiones no capturan); el informe reporta base, ajuste y veredicto final. Nunca se infla la base con features de relleno ni se mueve el ajuste para alcanzar un número redondo.

**Filosofía del ajuste (feedback FER 2026-07-12):** las 7 dimensiones son un lente para
encontrar fallas, NO un banco de puntos que se rellena hasta 1000. El veredicto final es tu
evaluación honesta de la calidad REAL del conjunto: 1000 significa "un experto que la lea por
primera vez no le cambiaría nada relevante", no "acumulé arreglos hasta sumar 1000". Nunca subas
el veredicto porque "agregué una feature que vale X": una feature nueva que no hacía falta no
mejora la skill, la infla. Reparar un hallazgo real eleva la calidad y por eso sube el veredicto;
agregar relleno para llegar al número, no. Si queda una reserva real que no se cierra con código
(ej. la skill solo se probó en campo con un input; su promesa de ser genérica aún no se ejerció
con un caso distinto), decláralo como ajuste holístico negativo con su porqué. **Honestidad >
complacencia: un 970 honesto y explicado vale más que un 1000 de cortesía.**

### Fase 3 — Verificación cruzada

Los errores más caros viven ENTRE archivos, no dentro de uno:

- Cada archivo que SKILL.md manda leer, existe y contiene lo prometido.
- Los ejemplos usan los mismos nombres, cifras y formatos que las instrucciones.
- El description promete exactamente lo que el cuerpo entrega (ni más ni menos).
- Los nombres de skills hermanas que menciona existen hoy en ~/.claude/skills (los renombres las rompen en silencio).
- Si depende de un MCP o tool externa, declara qué hacer cuando falte.

### Fase 4 — Informe

Entrega SIEMPRE este formato exacto:

```
# Auditoría: <skill> · <puntaje>/1000 · <veredicto>

| Dimensión | Puntos | Nota |
|---|---|---|
(7 filas + total)

## 🔴 Crítico (bloquea el mil de mil)
- <hallazgo> — <archivo:línea> — <arreglo concreto>

## 🟡 Mejorable
- ...

## 🟢 Lo que ya está bien
- ... (esto también se reporta: protege lo bueno de futuras ediciones)

## Plan de reparación
1. ... (ordenado por impacto en puntos)
```

Veredictos: **ORO** 950–1000 (lista para comunidad) · **PLATA** 850–949 (sólida, pulir) · **BRONCE** 700–849 (funciona con huecos) · **EN OBRA** <700 (reestructurar).

Así se ve un hallazgo bien escrito (evidencia + consecuencia + arreglo, no opinión):

> 🔴 El script valida Python con `py_compile`, que escribe bytecode — `scripts/inventario.sh`, sección SINTAXIS DE SCRIPTS de la v1.0 — en una skill blindada la escritura falla y reporta un error de sintaxis FALSO. Arreglo: validar con `ast.parse` (solo lectura). *(Hallazgo real de la v1.0 de esta misma skill, ya corregido; se cita la sección y no un número de línea porque las líneas bailan con cada versión.)*

Y así NO ("el script podría mejorarse", "la estructura se siente desordenada" — sin archivo:línea ni consecuencia, no vale como hallazgo).

### Fase 5 — Reparación (solo en modo AUDITA+ARREGLA)

1. **Backup primero, siempre:** `mkdir -p ~/.claude/skill-backups && cp -R <skill> ~/.claude/skill-backups/<nombre>-$(date +%Y%m%d-%H%M%S)`. Sin backup no se toca nada. NUNCA dentro de `~/.claude/skills/`: una copia con SKILL.md válido ahí se registra como skill duplicada y compite en el disparo.
2. **Desbloquea si está blindada** (el pedido de arreglar del usuario ES la autorización):
   - `chflags uchg` → `chflags -R nouchg <skill>`
   - chmod 0444/0555 → `chmod -R u+w <skill>`
3. **Arregla en orden del plan** (crítico primero). Reestructura sin miedo si la rúbrica lo exige: partir un SKILL.md monolítico en references, fusionar archivos redundantes, reescribir el description. Lo que NO se cambia: la intención y el conocimiento de campo de la skill — se reorganiza y se pule, no se reinventa. Textos que el dueño dictó verbatim se conservan intactos.
4. **Registra:** añade o actualiza la línea de versión/changelog en el comentario HTML bajo el H1 de SKILL.md (patrón de la casa: `<!-- skill vX.Y · qué cambió -->`).
5. **Blindaje al cierre** (política Golden: lo que quedó perfecto se protege):
   - Si YA estaba blindada → re-blinda con el MISMO mecanismo que tenía (uchg → `chflags -R uchg`; chmod → `chmod -R a-w`).
   - Si NO estaba blindada y es skill propia (golden-) que cierra en 1000 sin pendientes con dueño → blíndala con el estándar de la casa (`chflags -R uchg`) e informa. Una skill perfecta sin blindar se degrada con la primera edición descuidada.
   - NO blindar: skills de terceros (rompe sus actualizaciones) ni skills que cierran con pendientes con dueño (van a necesitar edición pronto; se blindan al cerrar el pendiente).
6. Borra el backup solo si el usuario lo pide; por defecto se queda.
7. **Sello md5 canónico** (la receta de la casa, tal cual se usa en las actas):
   ```bash
   cd <skill> && find . -type f | sort | xargs md5 -q | md5 -q
   ```
   Limitaciones conocidas y declaradas: (a) el sello NO incluye los nombres de archivo — un
   renombre que conserve el orden y el contenido no lo altera; por eso el conteo de archivos
   (`find . -type f | wc -l`) acompaña SIEMPRE al md5 en las actas. (b) xargs parte las rutas
   CON ESPACIOS (medido sobre claude-ads, que tiene 5): en skills con espacios en nombres se
   usa la variante segura `find . -type f -print0 | sort -z | xargs -0 md5 -q | md5 -q` y el
   acta declara cuál receta se usó. (c) `find . -type f` EXCLUYE los symlinks: repuntar un
   enlace hacia otro destino no altera ni el md5 ni el conteo — el sello no lo ve. En skills
   con symlinks se acompaña con la variante que sí los cuenta,
   `find . \( -type f -o -type l \) | wc -l`, y si el contenido apuntado importa, el hash
   con `find -L . -type f | sort | xargs md5 -q | md5 -q` (sigue el enlace y hashea el
   destino); el acta declara qué variante se usó.

### Fase 6 — Re-auditoría

Repite Fases 1–4 sobre la skill reparada (lectura fresca, sin reutilizar la memoria de la primera pasada — los arreglos también introducen errores). La meta es **excelencia real, no un número redondo**: si un hallazgo tiene evidencia, se arregla — no se deja "porque ya alcanzó ORO". Pero arreglar sube el veredicto solo porque sube la calidad real; jamás se agrega relleno para "completar" 1000 (ver la filosofía de puntaje en Fase 2). Hay dos detenciones legítimas antes de 1000: (a) puntos que dependen de algo que solo el usuario tiene (ej. la palabra clave real del bot, etiquetas exactas de una plataforma cerrada) → se reportan como "pendientes con dueño" con lo que valen; y (b) reservas que solo cierra el uso real (ej. una skill genérica probada aún en un solo caso) → se declaran con honestidad y bajan el veredicto sin inflarlo.

**Rollback:** si la re-auditoría sale PEOR que el puntaje previo a la reparación, restaura el backup completo, informa qué arreglo salió mal y reintenta solo los arreglos que sí sumaron. Empeorar una skill que funcionaba es el único fracaso inaceptable de esta skill.

Cierre del informe final: puntaje antes → después, lista de cambios aplicados, ruta del backup y estado del blindaje.

## Reglas de juicio (leer antes de calificar)

- **Larga ≠ buena.** Una skill de 2000 líneas sin jerarquía puntúa PEOR que una de 300 bien apuntada. Premia contexto barato: que el modelo cargue solo lo que necesita.
- **MUST-walls son bandera amarilla.** Muros de ALWAYS/NEVER sin porqué producen obediencia frágil. La instrucción fuerte es la que explica la consecuencia ("si el precio no es real, el render se paga dos veces").
- **Sobreajuste es deuda.** Instrucciones que solo funcionan para el producto/ejemplo con que se probó la skill restan en Proceso, aunque "funcionen".
- **Lo implícito no existe.** Si un paso vive solo en la cabeza del dueño (etiquetas exactas de un módulo, credenciales, un pantallazo pendiente), la skill debe declararlo como dato de entrada o pendiente explícito.
- **Cada skill se compara con su trabajo, no con otras skills.** Una skill chica que hace una cosa perfecta puede ser ORO; un orquestador gigante con un cabo suelto no.

## Además de "funciona": en cuántas vueltas

Una skill que llega al resultado correcto en ocho idas y vueltas **no está bien hecha**, está
compensando con esfuerzo lo que le falta en instrucciones. Al auditar, mide también el camino:

- **Cuántos turnos** necesitó para el primer entregable aceptable. Si el usuario tuvo que
  corregir tres veces lo mismo, esa corrección pertenecía al SKILL.md.
- **Cuántas preguntas hizo** antes de arrancar. Preguntar lo que ya está en el intake o en la
  memoria es una fuga: el dato existía y no se leyó.
- **Cuánto costó.** Un flujo que quema el triple de tokens por el mismo resultado tiene un
  problema de diseño, no de modelo.

Esto **resta en Proceso y flujo (180)**: una skill que funciona pero cuesta el doble no es ORO.

**Para probar sin gastar ni exponer datos reales:** genera los fixtures **con un script de Python**,
no escribiéndolos token a token. Es más barato, produce sets grandes de verdad, y no saca datos del
negocio mientras la skill todavía se está moviendo. Los datos reales entran cuando ya pasó la
prueba, no antes.

## Límites y delegación

- Crear una skill desde cero → **skill-creator** (esta skill puede sugerirlo y pasar el brief).
- Optimizar el description con evals automáticos de disparo → ofrecer el loop de **skill-creator** como paso extra opcional al final; el arreglo manual del description sí es de esta skill.
- Auditar seguridad de código de una app → **cyber-neo**. Auditar un PDF → **golden-pdf-check**.
- Skills de terceros (no golden-): se auditan igual, pero la dimensión 6 (Estándares Golden) evalúa solo lo universal (datos privados, autonomía) y reparte los puntos de marca en las demás verificaciones de esa dimensión; además NO se reescriben para redistribuir (licencia de terceros) — solo se reparan localmente.
