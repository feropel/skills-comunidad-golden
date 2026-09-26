# Historial completo de versiones — golden-ugc-avatar

<!-- Movido desde SKILL.md en v1.14 para bajar el coste de activacion. Las 3 ultimas viven tambien en SKILL.md. -->

- **v1.14** — Divulgación progresiva: el cuerpo bajó de 582 a menos de 500 líneas moviendo a
  referencias tres bloques que solo se necesitan en casos concretos (procedimiento de Google Vids,
  reglas de verticales sensibles, tabla de costos). En el cuerpo queda la **decisión** — cuándo ir a
  cada ruta y las prohibiciones que no pueden esperar a una lectura — y el **detalle** se carga solo
  cuando hace falta. Motivo: el validador oficial avisaba que un cuerpo largo encarece la activación
  en cada disparo, y un cuerpo que nadie termina de leer protege menos que uno corto y apuntado.
- **v1.13** — Cerrados dos huecos **medidos en campo**, no supuestos. (1) **Compuerta de identidad**
  en el Step 2: un `media_id` cruzado entre dos clientes del mismo chat produjo un video de un
  desconocido y costó **135 créditos**; ahora la skill obliga a descargar la referencia y mirarla
  antes de gastar, y declara la **clase** (todo identificador opaco: media_id, soul_id, preset_id,
  ad_account_id). (2) **Google Vids pasa de "no verificada" a VERIFICADA EN VIVO** con el
  procedimiento medido: `file_upload` y jamás clic en el file input, asistente de 4 pasos, tope de
  800 caracteres por escena, guion de escena poblada en solo-lectura con la escena nueva como
  salida, y los **dos** botones en secuencia (`Obtener vista previa` → `Generar`), cuyo salto
  producía "No generated videos found". Con la congelación de Higgsfield vigente, Vids queda
  declarada como **la** ruta de talking-head a 0 créditos — antes ese camino quedaba sin salida.
- **v1.12** (2026-08-31) — Compuerta de la CONGELACIÓN de Higgsfield (estándar de FER 30-ago): banner de bloqueo; Step 3 Seedance EN PAUSA (solo avatar en imagen); costo-antes-con-aprobación. Reversible.
- **v1.11** — Registrada la **ruta alterna Google Vids** (Workspace) para generar avatares sin
  gastar créditos de Higgsfield, con su frontera explícita: Vids para piezas corporativas/formación
  y horizontal dentro de Workspace; Higgsfield para UGC vertical y creativos de pauta, donde mandan
  el look de selfie sin pulir y el control fino de identidad y coherencia voz-cuerpo. Se deja dicho
  que el oficio de guion de esta skill (5 capas, perfiles A-E, tabla voz-cuerpo, espejo de
  compliance) es model-agnostic y sirve igual para un guion que se pega en Vids. Marcada como **no
  verificada en vivo** (no hay MCP de Vids; se opera a mano en la UI de Workspace) para no prometerle
  a un cliente capacidades no medidas. Dato aportado por FER.
- **v1.10** — Auditoría fresca (golden-skill-auditor): resuelta la colisión de dos pasos "0" — el
  bloque del cerebro de marca pasa a **Paso previo** y Step 0 sigue siendo el de toolchain, así no
  se renumera nada ya referenciado; el cerebro de marca **entra al diagrama** de pipeline (estaba
  declarado obligatorio pero no aparecía en el mapa del flujo); **Step 4 sube de H3 a H2** (era un
  paso par de 0-3 escondido dentro de Step 3, invisible al escanear encabezados aunque sí salía en
  el diagrama); y la regla de **compliance de la adenda 2026-08-23 baja al cuerpo** — sección propia
  en Step 3 (contrastar cada claim del guion contra la lista negra) más un quinto ítem en la
  compuerta de QA del Step 4, porque una instrucción que solo vive en un comentario HTML no la
  ejecuta nadie. Blindaje real documentado: doble (chflags uchg **y** chmod 0444).
- **v1.9** — Estándar 9 (Centro de Mando): declarado explícitamente que los cambios relevantes de
  esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR (regla de FER, 2026-08-22,
  `estandares-golden.md` §9). Tarea liviana, sin auditoría completa.
- **v1.8** — Reparación (golden-skill-auditor): description ahora declara desambiguación explícita
  (no usar para imágenes de producto, página, ads o edición — remite a la skill correcta en cada
  caso); corregido el handoff de edición para apuntar a `golden-video-editor` en vez de
  `hyperframes` (el motor real de corte/subtítulos/ensamblaje que consume esta skill); quitado el
  residuo "(Moko)" del H1 de `seedance_prompt_system.md` (el changelog v1.3 decía que ya se había
  quitado y no era cierto); des-duplicada la tabla de coherencia voz-cuerpo en SKILL.md — ahora
  apunta a la tabla completa de `references/seedance_prompt_system.md` §8 en vez de repetir una
  copia corta que podía desincronizarse; agregado el Paso 4 (auto-chequeo: identidad, coherencia
  voz-cuerpo, reglas de vertical, negative prompt presente) con definición explícita de
  "terminado", ya que el pipeline no tenía compuerta de QA antes de la entrega. Blindaje:
  `chflags uchg` (documentado aquí por primera vez, según estandares-golden.md §6).
- **v1.7** — Before/after cut BY VERTICAL agregado al bloque de salud del Step 2 (2026-08-10, loop
  del arsenal semana 2). La norma del 2026-08-07 prohibía antes/después solo para dental; Meta 2026
  también lo prohíbe en anti-edad/arrugas/firmeza y pérdida de peso, y lo permite en cosmética
  general con audiencia 18+. Dos prohibiciones cross-vertical agregadas al negative prompt: segunda
  persona señalando la condición del espectador, y titulares de plazo-más-resultado (Meta juzga el
  significado implícito). Reflejado en `golden-ecom-magic` y `golden-imagen-arena`.
- **v1.6** — Art rules for HEALTH verticals (dental and similar) baked into Step 2, applying to image and video prompts. Harvest of the "ESTUDIO 360 un producto de salud oral de terceros (Chile)" chat, assigned by the Centro de Mando (2026-08-07): forbidden — visible lesions, teeth before/after, medical-endorsement props (white coat, stethoscope, dental chair), on-screen result percentages, condition-pointing questions; allowed and field-proven — dropper macro, product texture, illustrated enamel cross-section, bathroom lifestyle.
- **v1.5** — Added the **Cost reality check** section: verified per-generation prices (Flux Schnell $0.03 → Veo 3 $3.00) and the pay-per-use vs subscription break-even (~30/mo saves, ~60-100 ties, >200 costs 3-5x more). Conclusion baked in: Golden stays on the Higgsfield subscription; "free repo" alternatives get checked against this table first. Rule: iterate cheap, spend on the final only. Destilado de una guía pública de Open-Generative-AI/MuAPI (mayo 2026), sin instalar nada.
- **v1.4** — Added `references/seedance_advanced.md` (destilado original, sin copiar terceros): multi-reference role mapping (image/video/audio, up to ~9/3/3), beat-budgeting by duration, multi-shot transition language, film-verb camera vocabulary, audio-as-first-class, prompt hygiene (keep settings out of prose), and **character-sheet identity locking** incl. photoreal identity sheets — the fix for one-off-invented drift. Wired into Step 1 (identity), Step 3 (video) and the reference list. Enriquece con lo mejor de la skill `video-prompting` (Seedance 2.0 + hojas de personaje) sin depender de ella.
- **v1.3** — Polish for community sharing: unified to English throughout, removed the legacy "Moko" trigger, flagged the Reference Element path as not-yet-verified-live. Core image+video path is live-proven; the Soul (trained reusable identity) path remains documented but unverified end-to-end.
- **v1.2** — Live-verified against the Higgsfield MCP end-to-end (image `soul_2` + video `seedance_2_0_mini`). Baked in: plan gating + `seedance_2_0_mini` fallback, `credits_exact` reporting, real presets are viral-effect (not UGC) clips, cross-skill handoffs, troubleshooting table. Privacy-audited for community sharing (no personal data in package).
- **v1.1** — Rewrote all operational wiring against the real model catalog (correct model IDs, params, media flow, no `job_status`, `get_cost` preflight, Soul/Element identity strategy).
- **v1.0** — Initial two-stage pipeline (image framework + Seedance system) with reference files.

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> End-to-end UGC avatar creation pipeline on the Higgsfield MCP. Generates hyperrealistic AI avatar images with Higgsfield Soul 2.0 (or Nano Banana Pro), then animates them into talking-head UGC videos with Seedance 2.0 — through structured prompt frameworks that lock character identity and enforce voice/body coherence, with reusable identity via Soul training and Reference Elements so one avatar stays the same person across videos. Use this skill whenever the user mentions UGC avatars, AI avatars, avatar generation, creating UGC content, AI talking-head videos, the Higgsfield workflow, Soul characters, Nano Banana avatar, Seedance UGC, the avatar pipeline, or anything about creating AI-generated people for social media content, ads, or brand videos. Also trigger when the user asks to "make a person," "create a character for video," "generate a talking-head," "haz un avatar," "crea un UGC," "hazme un video hablando," or "un avatar para mi marca." Runs either stage alone when needed. Do NOT use for product-only images (packshots, infographics, product listing photos) — that is `golden-imagen-arena`. Do NOT use to build the product page, run ads, or edit/caption the final clip — those are `golden-shopify`, `golden-ads`, and `golden-video-editor` respectively.


## Actas y sello mudados desde SKILL.md (v1.16, 2026-09-05)

Nada se borró: se mudó. Orden original, de arriba abajo.

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 998 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill v1.13 · 2026-09-05: DOS huecos medidos cerrados. (1) Nueva COMPUERTA DE IDENTIDAD en el Step 2: antes de generar con `medias` hay que descargar la imagen y MIRARLA — un media_id cruzado entre dos clientes del mismo chat costó 135 creditos y el diagnostico inicial culpo al prompt; declarada como CLASE (todo identificador opaco que dispare gasto). (2) Google Vids sube de "no verificada" a VERIFICADA EN VIVO con el procedimiento medido de 5 puntos (file_upload y nunca clic en el file input, asistente de 4 pasos, tope 800 car/escena, guion de escena poblada es solo-lectura y se resuelve con escena nueva, y los DOS botones vista previa -> Generar). Con la congelacion vigente, Vids queda declarada como LA ruta de talking-head a 0 creditos. -->

<!-- skill v1.12 · 2026-08-31 (CdM) · COMPUERTA de la congelacion de Higgsfield (estandar de FER 30-ago repartido por el CdM): banner de bloqueo arriba, Step 3 (Seedance video) EN PAUSA — hoy solo el avatar en IMAGEN; costo-antes-con-aprobacion para toda generacion. Reversible al levantar la congelacion. memoria: feedback_higgsfield_solo_imagenes_y_costo_antes. -->

<!-- skill v1.11 · 2026-08-24: registrada la RUTA ALTERNA Google Vids (Workspace) como forma de generar avatares sin gastar creditos de Higgsfield — con su frontera declarada (Vids para corporativo/formacion horizontal; Higgsfield para UGC vertical y ads, que es donde manda el look selfie y el control fino de identidad y coherencia voz-cuerpo) y marcada como NO verificada en vivo (no hay MCP de Vids; se opera a mano). Dato aportado por FER. -->

<!-- skill v1.10 · 2026-08-24 (golden-skill-auditor, auditoria fresca): resuelta la COLISION de dos pasos "0" (el cerebro de marca pasa a "Paso previo"; Step 0 sigue siendo el de toolchain, asi no se renumera nada ya referenciado); el cerebro de marca ENTRA al diagrama de pipeline (era obligatorio y no aparecia en el mapa); Step 4 sube de H3 a H2 (era un paso par de 0-3 escondido dentro de Step 3, invisible al escanear encabezados pese a salir en el diagrama); y la regla de COMPLIANCE de la adenda 2026-08-23 baja del comentario HTML al CUERPO — seccion propia en Step 3 + quinto item en la compuerta de QA del Step 4 (una instruccion que solo vive en un comentario no es una instruccion). Blindaje real: chflags uchg Y chmod 0444 (doble; reponer ambos). Cambios relevantes reportados a GOLDEN - CENTRO DE MANDO. -->

<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->

<!-- adenda 2026-08-23 (centro de mando, alineación de espejo de compliance tras auditoría de ecom-magic v2.2): la LISTA NEGRA de claims inventados (Ley 6 de golden-ecom-magic, espejada en golden-imagen-arena) aplica TAMBIÉN a los guiones del avatar — un claim médico/curativo inventado dicho por un avatar es el mismo riesgo de cuenta que impreso en una imagen. Antes de aprobar un guion: contrastar claims contra la lista negra del espejo. -->

<!-- skill v1.8 · 2026-08-21 (golden-skill-auditor, reparación): description now states explicit
disambiguation (NOT for product-only images/page/ads/editing, with the correct hermana for each);
fixed the "hyperframes" handoff to point at golden-video-editor (the actual cut/caption/assembly
skill); removed the residual "(Moko)" from the seedance_prompt_system.md H1 (stale legacy name the
v1.3 changelog claimed was already removed); de-duplicated the voice/body coherence table in
SKILL.md — it now points to the single source of truth in seedance_prompt_system.md §8 instead of
repeating a shorter, driftable copy; added Step 4 (self-check: identity match, voice-body coherence,
vertical rules, negative-prompt present) with an explicit "done" definition, since the pipeline had
no QA gate before handoff. Blindaje: chflags uchg (desbloquear con `chflags -R nouchg`, reponer con
`chflags -R uchg`) — mechanism now documented here per estandares-golden.md §6. -->

<!-- skill v1.7 · 2026-08-10 (loop del arsenal, semana 2 · producción): before/after cut BY VERTICAL added to the Step 2 health block. The 2026-08-07 norm banned before/after for dental only; Meta 2026 also bans it for anti-aging/wrinkles/firming and weight loss, and allows it for general cosmetics with an 18+ audience. Two cross-vertical bans added to the negative prompt: second person pointing at the viewer's condition, and timeframe-plus-result headlines (Meta judges implied meaning). Mirrored in golden-ecom-magic and golden-imagen-arena -->

<!-- skill v1.6 · 2026-08-07 (centro de mando, cosecha del chat ESTUDIO 360 un producto de salud oral de terceros Chile) · reglas de arte para verticales de SALUD (dental y afines) en el Step 2, aplicables a prompts de imagen Y video: prohibido bocas con lesiones, antes/después de dentadura, delantal/estetoscopio/sillón dental, porcentajes en pantalla y preguntas que señalen condición del espectador; permitido macro del gotario, textura, corte de esmalte ilustrado y lifestyle de baño -->

<!-- skill v1.4 · pipeline foto→video UGC sobre Higgsfield MCP · imagen soul_2/nano_banana_pro + video seedance_2_0 (fallback seedance_2_0_mini en plan starter) · verificado en vivo el camino imagen+talking-head; Soul reutilizable documentado, aún sin correr end-to-end · changelog completo al pie -->


<!-- skill v1.10.1 · 2026-08-24 (centro de mando, remediación del verificador de cierre): línea de RUTA del cerebro en el Paso 0 (las lectoras ordenaban LÉELO PRIMERO sin decir dónde — un chat limpio no podía ejecutar la orden) + bump que las ediciones del 23-24 dejaron sin subir. -->

<!-- v1.9 — Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
