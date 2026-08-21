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

<!-- skill v1.9 — 2026-08-21 — ronda contra el expediente del verificador adversarial (v1.8 NO RATIFICADA). inventario.sh: (a) el escaneo de referencias vivas barre .md .py .sh .json .liquid .html .csv, no solo .md (rota citada en comentario de un .py era invisible); (b) citas de directorio RELATIVAS desde dentro de references/ se resuelven contra el directorio del archivo que cita (caso golden-web: arte-generativo-templates/ dejaba 2 huérfanos falsos); (c) la degradación cross-skill a ℹ️ exige dueña ÚNICA + mención de esa hermana por nombre en el texto vivo — cualquier otra colisión va a DUDOSOS con la lista (66 rutas relativas viven en 2+ de las 91 skills); (d) skills/<hermana>/SKILL.md ahora se captura y verifica (antes invisible por exigir segmento canónico); (e) SIMETRÍA de historia en huérfanos: la mención que salva debe estar en texto vivo (sin changelogs, sin comentarios HTML, sin fixtures) y parecer ruta ("/nombre.ext") — una palabra suelta no salva; (f) material intruso baja de 🔴 a ⚠️ "mover a references/" (no es rotura, es orden). autoprueba_inventario.sh reescrita: extractores de bloque para TODAS las secciones (rotas, huérfanas, ℹ️, DUDOSOS, hermanas rotas, hermanas OK, intrusos), un caso sembrado por CADA rama del case, conteos exactos por bloque — 38/38 con el detector nuevo, y los 4 sabotajes del verificador (s7 rotas-de-hermana-como-OK, s8 sin-forma-corta, s9 sin-rescate-EN_HERMANA, s10 hermana-nunca-existe) hacen FALLAR el banco (mordida demostrada sobre copias en tmpdir). SKILL.md:puntero py_compile sin número de línea muerto; estandares-golden.md deja de afirmar el blindaje de terceros y lo marca como foto fechada -->
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
   El script reporta: blindaje (chflags uchg / chmod 0444), árbol de archivos con líneas, frontmatter, referencias rotas (mencionadas pero inexistentes, barriendo texto vivo en .md .py .sh .json .liquid .html .csv), archivos huérfanos (existen pero ninguna cita con forma de ruta los menciona), la línea DUDOSOS con lo que exige confirmación a mano, y chequeo de sintaxis de scripts (bash -n / ast.parse de Python, sin escribir nada en la skill auditada).
   Si vas a tocar el detector de referencias, corre antes y después su banco adversarial:
   ```bash
   bash ~/.claude/skills/golden-skill-auditor/scripts/autoprueba_inventario.sh
   ```
   El banco siembra un árbol en tmpdir con un caso por cada rama del detector y sale 0 solo si las 38 aserciones pasan; un cambio al detector sin banco verde no se sella.
3. Si el script falla o no existe, haz el inventario a mano con `find`, `wc -l` y lectura del frontmatter — la auditoría no se detiene por el script.

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

**El puntaje es un VEREDICTO HOLÍSTICO, no una suma que se completa.** Las 7 dimensiones son un
lente para encontrar fallas, NO un banco de puntos que se rellena hasta 1000. El número final es
tu evaluación honesta de la calidad REAL del conjunto: 1000 significa "un experto que la lea por
primera vez no le cambiaría nada relevante", no "acumulé arreglos hasta sumar 1000". Nunca subas
el veredicto porque "agregué una feature que vale X": una feature nueva que no hacía falta no
mejora la skill, la infla. Reparar un hallazgo real eleva la calidad y por eso sube el veredicto;
agregar relleno para llegar al número, no. Si queda una reserva real que no se cierra con código
(ej. la skill solo se probó en campo con un input; su promesa de ser genérica aún no se ejerció
con un caso distinto), dilo y baja el número con honestidad. **Honestidad > complacencia: un 970
honesto y explicado vale más que un 1000 de cortesía.**

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
