---
name: golden-ugc-avatar
description: >-
  Golden Group — Fabrica de AVATARES UGC: crea una persona hiperrealista con Higgsfield Soul 2.0 o
  Nano Banana Pro y la anima como talking-head con Seedance 2.0, con marcos de prompt que bloquean
  la identidad y exigen coherencia entre voz y cuerpo; la identidad se reutiliza con Soul
  entrenado o Reference Elements para que el mismo rostro vuelva en decenas de videos. Incluye la
  ruta VERIFICADA de Google Vids: avatar desde una foto propia, cero creditos. Usala SIEMPRE que
  el usuario quiera avatares UGC, avatares de IA, contenido UGC, un video de alguien hablando a
  camara, un vocero para su marca, o diga "haz un avatar", "crea un UGC", "hazme un video
  hablando", "un avatar para mi marca", "una persona que presente esto", "un talking head", o
  mencione Higgsfield, Soul, Nano Banana, Seedance o Google Vids. Dispara aunque no diga avatar:
  basta con querer una persona generada por IA hablando para redes, anuncios o comunidad. Corre
  cualquiera de las dos etapas por separado.
---

**Fábrica:** chat «✅ SKILL golden-ugc-avatar»

# Golden UGC Avatar — Higgsfield Pipeline
<!-- skill v1.17 · 2026-09-06 · auditoria golden-skill-auditor: cuerpo recortado bajo 500 lineas (techo desde v1.14) quitando del H2 "Version & changelog" el bullet v1.13, ya duplicado palabra por palabra en references/changelog.md — nada se borro, se dejo de repetir. Resto verificado en su techo: 0 rotas/huerfanos/secretos, blindaje doble intacto, validador 0/0/0. -->
<!-- skill v1.16 · 2026-09-05 · sello mudado a references/changelog.md (fila del CdM); blindaje y validacion ahora son procedimiento vivo en el cuerpo; lista negra probada en los DOS sentidos. -->

## Paso previo · Cerebro de marca (obligatorio antes de generar)

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.

> ## 🔴 CONGELACIÓN VIGENTE (FER, 2026-08-30) — LEE ESTO ANTES DE GENERAR
> Memoria canónica: `feedback_higgsfield_solo_imagenes_y_costo_antes`. Dos reglas de la casa:
> 1. **CERO VIDEO en Higgsfield hasta que FER lo levante.** El **Step 3 (Seedance 2.0)** de esta
>    skill queda **EN PAUSA**: hoy este pipeline entrega **solo el avatar en IMAGEN** (Step 2). El
>    talking-head animado NO se genera hasta que FER retire la congelación. Motivo medido: 11 tiros
>    al mismo video de Toppik costaron 559 créditos; lo caro no es generar, es repetir.
> 2. **Antes de CUALQUIER generación que gaste créditos** (incluida la imagen del Step 2): decir el
>    **costo exacto** con `get_cost:true` y **ESPERAR el sí de FER**. No se genera y luego se avisa.
> Movimiento sin gastar créditos: **HyperFrames** (`golden-video-editor`), 0 créditos — pero NO hace
> una persona hablando fotorrealista; si el talking-head es imprescindible, ESPERA a que FER levante
> la congelación, no busques un rodeo que gaste video.

El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta (buscar con find ANTES de crear, naming MAYÚSCULAS-CON-GUIONES) la declara `golden-brand-brain`: ante cualquier duda de ruta, invócala en vez de adivinar.

## What this skill does

Creates AI-generated UGC avatars in two stages that share one locked identity:

1. **Image** → Higgsfield **Soul 2.0** (`soul_2`) for UGC/portrait/character, or **Nano Banana
   Pro** (`nano_banana_pro`) for max-quality / text-heavy frames.
2. **Video** → **Seedance 2.0** (`seedance_2_0`), animating the approved image as the `start_image`,
   with native audio for the talking-head voice.

The whole value of the skill is **consistency**: the avatar's face and body stay identical across
every generation, and the voice always matches what the body is doing. Get those two right and the
content reads as a real person.

This skill is written against the live Higgsfield MCP, but tool names and model IDs can change.
**Step 0 always re-verifies against the live server** — trust the live schema over this document.

## Pipeline overview

```
User brief
   ↓
Paso previo  Read the brand brain (golden-brand-brain) → voice, product, real claims
   ↓
Step 0  Verify Higgsfield MCP + discover models live
   ↓
Step 1  Choose IDENTITY strategy → Soul (reusable) | Element (instant ref) | one-off
   ↓
Step 2  Build image prompt (5-block framework) → generate_image (soul_2 / nano_banana_pro)
   ↓                                              → preflight get_cost → display result → approve
Step 3  [⏸️ CONGELADO por FER 30-ago — ver banner arriba] Build Seedance prompt → generate_video (seedance_2_0, start_image)
   ↓                                              → display result
Step 4  Self-check: identity match, voice-body coherence, vertical rules, negative prompt present
   ↓
Done
```

---

## Step 0: Verify the toolchain and discover models live

This pipeline depends on the Higgsfield MCP. Tool names, model IDs, and parameter ranges vary
between server versions, and a blind call that fails silently wastes the user's credits. Before
the first generation:

1. **Confirm Higgsfield tools are available.** They appear as `mcp__<server>__*` with names like
   `generate_image`, `generate_video`, `models_explore`, `media_upload`, `media_confirm`,
   `job_display`, `show_characters`, `presets_show`. If deferred, load them via ToolSearch
   (`higgsfield`, `generate_image`, `soul`, `seedance`).
2. **If no Higgsfield MCP is connected, stop** and tell the user — there is nothing to generate
   against. Never fabricate a result.
3. **Discover the real model catalog before locking choices.** Call `models_explore`:
   - `action: "recommend"`, `type: "image"`, query describing UGC avatar → confirms the best image model.
   - `action: "recommend"`, `type: "video"`, query describing image-to-video talking head → confirms the video model.
   - `action: "get"`, `model_id: <id>` → returns exact `aspect_ratios`, params, and ranges. Use these instead of guessing.
4. **Preflight cost.** Both `generate_image` and `generate_video` accept `params.get_cost: true`,
   which returns the credit cost **without** submitting a job. Use it before any real generation
   the user hasn't explicitly pre-approved. Report `credits_exact` (the true fractional cost),
   not the rounded `credits` field — e.g. a Soul image reports `credits: 1` but `credits_exact:
   0.12`, and quoting "1" overstates it.

There is **no `job_status` polling tool**. Generations are non-blocking and return a result/job id;
use `job_display` (one id per call) to render a result, or `show_generations` to browse history.
Do not loop a poll step.

**Plan gating (verified live):** some models require a paid Higgsfield tier. `seedance_2_0`
returns `403 "Pro" or "Ultimate" plan required` on the starter/free plan. When you hit that 403,
**fall back to `seedance_2_0_mini`** (works on starter, 480p/720p, cheaper) rather than stopping —
tell the user the quality tradeoff and that upgrading unlocks full `seedance_2_0`. Check the user's
plan with `balance` (`subscription_plan_type`) if you want to pick the right model up front. A `403`
does **not** consume credits, so a failed attempt is safe.

---

## Step 1: Choose the identity strategy

Consistency is the point of an avatar, and Higgsfield gives three ways to hold identity. Pick with
the user before generating — this single choice determines everything downstream.

| Strategy | How | Best for | Trade-off |
|---|---|---|---|
| **Soul (trained)** | `show_characters action=train`, 5–20 photos of one real person, ~10 min. Returns a `soul_id`, then generate with `soul_2` + `soul_id`. | A brand spokesperson reused across many videos; "use my face"; a digital twin. Most identity-faithful. | One person per generation; needs photos + a 10-min train; only works with Soul models. |
| **Reference Element** | `show_reference_elements action=create` from a single image → a reusable `<<<UUID>>>` reference. Works with many models (Nano Banana Pro, Seedance 2.0, etc.). | Instant reuse, multiple subjects in one shot, or when you only have one image. | Less identity-locked than a trained Soul. **Interface not yet verified live — confirm its params before relying on it.** |
| **One-off invented** | Generate a fresh character from a text prompt only (no reference), then reuse that image/job id as the reference for later shots. | Inventing a brand-new avatar from a brief; no source photos. | Identity drifts unless you feed the first image back as a reference every time. |

Decision rules:
- The user provides 5+ photos of the same person, or says "train" / "digital twin" / "my face" → **Soul**.
- The user wants instant reuse, has a single image, or needs more than one person in frame → **Element**.
- The user is inventing a character from a description with no source photos → **One-off**, and on
  every subsequent generation pass the first approved image (its job id) back as a reference so the
  face holds. **For the tightest hold, generate a character sheet first** (a multi-angle identity
  sheet) and reference it downstream — see `references/seedance_advanced.md` §7.

If the path is ambiguous, ask — don't silently train a Soul (it costs time and credits).

---

## Step 2: Build and generate the avatar image

Read `references/image_framework.json` for the full field-by-field template, enumerated options,
and a worked example. The prompt craft below is model-agnostic; the settings are live-verified.

The image prompt follows a **5-block architecture**, each block with a different lifespan:

1. **Quality & style** *(locked across all generations)* — hyperrealistic; modern-iPhone camera
   aesthetic; ultra-detailed lifelike skin/hair/fabric; natural smartphone HDR. Mixing rendering
   styles between shots is the fastest way to break the illusion of one real person.
2. **Composition** *(per scene)* — UGC selfie (close-up, slight wide-angle), talking head (head &
   shoulders, 85mm), or full lifestyle (three-quarter).
3. **Subject** *(identity locked; clothing/pose/expression change per scene)* — demographics, build,
   skin tone, hair, and full face. This is the identity card; reuse it verbatim across the library.
4. **Foreground** *(per scene, minimal)* — a phone, mug, towel. Clutter reads as a staged set.
5. **Background** *(per scene)* — environment whose lighting matches Block 1's smartphone aesthetic.

**Flatten** the filled blocks into one continuous 150–400-word paragraph in block order, then pass
it as the `prompt`. Specificity drives consistency.

### Verticales sensibles (salud, estética, pérdida de peso) — riesgo de CUENTA
Si el producto toca salud, dental, anti-edad, arrugas, firmeza o pérdida de peso, **lee
`references/verticales_sensibles.md` ANTES de escribir el prompt** (imagen y video). Ahí están las
prohibiciones medidas de Meta 2026 y el corte de antes/después por vertical. Regla que no espera a
esa lectura: **nunca entregues un antes/después** en esas verticales aunque el brief lo pida, y
nunca uses segunda persona señalando la condición del espectador ("tus arrugas") ni titulares de
plazo-más-resultado ("resultados en 7 días") — Meta juzga el significado implícito.

### Image models & settings *(verify with `models_explore action=get` before relying on these)*

| | `soul_2` (Higgsfield Soul 2.0) — **default for UGC/avatar** | `nano_banana_pro` (Google) — max quality / text |
|---|---|---|
| Use for | Realistic UGC, portraits, fashion, character; reusable Soul via `soul_id` | 4K detail, on-image text, diagrams, one-off refs |
| Key params | `quality`: `1.5k` / `2k` (default `2k`); `soul_id` (optional, from a trained Soul) | `resolution`: `1k` / `2k` / `4k` (default `1k`) |
| Aspect ratios | `1:1 16:9 9:16 4:3 3:4 3:2 2:3` | `1:1 9:16 16:9 4:5 5:4 4:3 3:4 3:2 2:3 21:9` |
| Reference media | one `image` role | one `image` role |

For vertical UGC use `aspect_ratio: "9:16"`. Pass a reference via `medias: [{ role: "image",
value: "<media_id or job_id>" }]` — never a raw URL (import URLs first with `media_import_url`).

### 🔴 Compuerta de IDENTIDAD — mirar la imagen antes de gastar (medido: costó 135 créditos)

Un `media_id` es un UUID: no se parece a nada y no avisa cuando es el equivocado. En un chat donde
conviven varios clientes es trivial pasar la foto de otra persona como referencia — y el modelo no
falla, **obedece**: entrega un desconocido y el gasto ya está hecho.

**Caso medido (2026-08-29):** se generó el video de presentación del dueño pasando el `media_id` de
la foto de OTRA clienta del mismo chat. Salió un hombre genérico que no era él. **135 créditos
perdidos**, y el primer diagnóstico fue equivocado (se culpó al prompt) hasta que se extrajo el
fotograma 0 y se miró.

**Regla dura, cuesta 0 créditos.** Antes de cualquier generación que lleve `medias`:
1. Toma el `url` del media (lo devuelve `job_display` o la respuesta del upload).
2. `curl -s -o <archivo> <url>` y **ábrela con la herramienta de lectura de imágenes**.
3. Di en la respuesta de quién es esa cara ANTES de llamar a `generate_*`.

Con dos o más personas en juego, escribe el mapa `nombre → media_id` en la respuesta y trabaja
contra ese mapa, nunca contra el id que recuerdas.

**La clase, no el caso:** aplica a todo identificador opaco que dispare gasto o escritura
(`media_id`, `soul_id`, `preset_id`, `ad_account_id`, id de producto). El UUID no se autovalida —
se comprueba mirando el objeto antes de gastar.

### Image call sequence
1. *(If using a reference)* get a `media_id`: local file → `media_upload_widget` (user picks) or
   `media_upload` → PUT bytes → `media_confirm`; web URL → `media_import_url`.
2. *(Optional)* `generate_image` with `params.get_cost: true` to preflight credits; report it.
3. `generate_image` with `model: "soul_2"` (or `nano_banana_pro`), the flattened `prompt`,
   `aspect_ratio`, and any reference `medias`. For a trained Soul, include `soul_id`.
4. `job_display` the result. Approve → Step 3. Iterate → re-prompt, keeping Block 3 identical.

---

## Step 3: Build and generate the Seedance video

Read `references/seedance_prompt_system.md` for the complete system: the five avatar profiles with
vocabulary DNA, the layer formulas, the negative-prompt library, and full worked templates. For
anything beyond a single-`start_image` talking head — **multiple references mapped by role,
beat-budgeting by duration, multi-shot transitions, richer camera/audio direction, and prompt
hygiene** — read `references/seedance_advanced.md`.

The video prompt is a **5-layer stack**:

1. **Avatar identity profile** — pick A–E (Gen Z, Wellness, Expert, High-Energy Fitness, Luxury).
   Each defines vocabulary DNA; dialogue must obey it (a Gen Z avatar never says "I find this
   invigorating"). Mismatched vocabulary is what makes AI scripts feel uncanny.
2. **Scene** — `[Location] + [Time/lighting] + [Atmosphere] + [Key props] + [Ambient sound]`.
3. **Emotional/physical state** — what the body just did, the primary emotion + undercurrent, and
   the physical tells (breathing, posture, micro-expressions).
4. **Voice direction** — gender, age, register, delivery, the physical influence on the voice,
   emotional coloring, mic proximity.
5. **Timestamp choreography** — one thought per ~5-second shot, with visual/action/voice/audio/emotion.

Assemble using the `【Avatar】【Scene】【Emotional/Physical State】【Voice Direction】【Timeline】
【Negative Prompts】【Technical】` skeleton in the reference file. Carry the Block-3 physical
description over **verbatim** and add "Maintain exact appearance throughout, consistent character,
no deformation." Keep direction tight: 50–200 words of actual direction.

### 🔴 Lista negra de compliance — claims Y lo que sale EN CÁMARA (riesgo de CUENTA)
Un claim inventado **dicho o mostrado** por un avatar es el mismo riesgo de cuenta que impreso en una
imagen, así que la lista negra de `golden-ecom-magic` (Ley 6, espejada en `golden-imagen-arena`)
aplica al guion Y al encuadre. Cinco prohibiciones, las cuatro últimas medidas en material real
(Centro de Mando, 2026-09-04):

1. **Claim inventado en el guion:** nada de curar, tratar, eliminar o regenerar; ningún porcentaje
   inventado; ningún plazo-más-resultado. Si el brief trae un claim, se pide su fuente; sin fuente se
   reescribe la línea sobre un beneficio que el producto sí sostiene.
2. **Aval médico falso:** prohibido bata, estetoscopio, consultorio o cualquier persona presentada
   como profesional de salud diciendo "mis pacientes". Prohibido "avalado por la ciencia" y las
   puntuaciones de autoridad tipo "4.9/5 de expertos". **Se caza en video igual que en imagen fija.**
3. **El producto que sale en cámara debe ser el que se despacha.** Dos de seis videos de proveedor
   mostraban un frasco distinto al real. En contra entrega eso termina en rechazo en la puerta, y el
   costo lo paga la empresa.
4. **El ingrediente falso también entra dibujado.** Cuatro piezas llevaban raíz de jengibre y el
   producto no la lleva: nadie lo escribió, lo puso el creativo. Revisa lo que la imagen INSINÚA, no
   solo lo que el texto afirma.
5. **Prohibido el parche verbal.** Si la pieza insinúa algo falso, NO se corrige agregando palabras:
   la pieza se rehace.

**Cómo se verifica (no es opinable):** el video se mira **fotograma a fotograma**. La transcripción
no ve el envase, ni la bata, ni el ingrediente dibujado — por eso auditar por transcripción deja
pasar justo estas cuatro. Extrae fotogramas y míralos.

**Se prueba en los DOS sentidos.** Una lista comprobada solo contra el caso malo no distingue: acusa
a la forma, no al defecto. Debe **morder el malo Y callar ante los buenos**, y el lado bueno lleva
**dos** casos, porque la prosa inocente casi nunca activa un detector mal hecho — lo que lo activa es
el texto que **se parece** al dato. **Criterio: si marca un caso bueno, la lista está mal escrita, no
la pieza; se corrige la lista.**

Los tres casos de prueba (bueno limpio, bueno **disfrazado** con el vocabulario de las cinco
prohibiciones, y malo que debe dispararlas todas) viven en **`references/compliance_casos.md`**.
Córrelos mentalmente contra tu pieza antes de aprobarla.

### The coherence guarantee — voice must match the body
Non-negotiable: whatever the body is doing in Layer 3, the voice in Layers 4–5 must carry the
matching signature (running → audible breathing and staccato delivery; post-workout → recovering
breath; seated → controlled full sentences; lying/stretching → slowest pace, deepest register).
Full 7-row table (incl. "just laughed / excited" and "cold / outdoors") lives in
`references/seedance_prompt_system.md` §8 — that table is the single source of truth; do not
re-copy it here so it can't drift out of sync.

### Seedance 2.0 settings *(live-verified; confirm ranges with `models_explore action=get`)*

| Parameter | Real values |
|---|---|
| Model | `seedance_2_0` (identity-consistent) **requires a Pro/Ultimate Higgsfield plan** — on starter/free it returns `403 "Pro" or "Ultimate" plan required`. **Fallback that works on starter: `seedance_2_0_mini`** (480p/720p only, cheaper — ~25 cr for 10s/720p vs ~45 for full). Verified live 2026-07. |
| `duration` | integer seconds, **4–15** (default 5). UGC sweet spot 8–12 |
| `resolution` | `480p` / `720p` / `1080p` / `4k` — **`1080p` and `4k` require `mode: "std"`** |
| `mode` | `std` (quality; supports all resolutions) / `fast` (cheaper; 480p–720p only) |
| `generate_audio` | `true` for a talking-head with native audio (default true); `false` for silent |
| `genre` | `auto` (keep auto for UGC realism) |
| `aspect_ratio` | `9:16` for vertical UGC |
| Media roles | `start_image` (the approved avatar), plus optional `end_image`, `image_references`, `video_references`, `audio_references` |

**Presets (verified live):** `presets_show` returns Higgsfield's image-to-video presets — but note
what they actually are: **viral / cinematic character-effect presets**, not talking-head UGC. The
live catalog (2026-07) is things like *Baseball Game, Drift Racing, Zombie Dance, Red Carpet, Free
Fall, superhero transforms* — they drop your character into a dramatic scene, they don't make a
person speak to camera. So: **for a talking-head UGC/ad, use the hand-built Seedance prompt above**
(full control over voice/body). **Reach for a preset only when the user wants a viral effect clip**
(character in a scene). To use one, call `presets_show`, pick a `preset_id`, then `generate_video`
with `model: "higgsfield_preset"` + `preset_id`. Always list them live — the catalog changes.

### Video call sequence
1. Get a `media_id` for the approved image (`media_upload` → PUT → `media_confirm`, or reuse the
   image's job id directly as the `medias` value).
2. *(Optional)* `generate_video` with `params.get_cost: true` to preflight credits; report it.
3. `generate_video` with `model: "seedance_2_0"`, the full Seedance `prompt`, `medias: [{ role:
   "start_image", value: "<media_id or job_id>" }]`, `aspect_ratio: "9:16"`, `duration`,
   `resolution`, `mode`, `generate_audio: true`.
4. `job_display` the result.

The start frame must be a confirmed `media_id` (or a completed image job id) — never a raw URL.

---

## Step 4: Self-check before handing off ("done" means this passes)
Before presenting the result as final, check it against the skill's own promise — consistency and
coherence, not taste:
1. **Identity match** — the face/build/hair in the video's first frame reads as the same person as
   the approved Block-3 image (the same avatar, not a redraw). If it drifted, do not deliver silently:
   say so and offer to regenerate with the identity re-locked (character sheet, §7 of
   `references/seedance_advanced.md`, if this is a recurring problem).
2. **Voice-body coherence** — re-read the physical state used in Layer 3 against the delivery notes
   actually written in Layer 4/5 (the table in `references/seedance_prompt_system.md` §8). A mismatch
   here is the single most common tell of AI video; catch it before the user does.
3. **Vertical rules honored** — if the product is a health/sensitive vertical (Step 2), confirm the
   frame contains none of the forbidden elements and no before/after was used where it's banned.
4. **Negative prompt was included** — Step 3 always ships a `【Negative Prompts】` block; missing it
   is the top cause of uncanny output (see `references/seedance_prompt_system.md` §9).
5. **Fotogramas mirados** — el video se revisó **fotograma a fotograma** contra la lista negra de
   arriba: sin bata ni estetoscopio, el envase que sale es el que se despacha, y no aparece ningún
   ingrediente que el producto no lleve. La transcripción no basta.
6. **Claims cleared** — every claim spoken in the dialogue passed the compliance mirror above: none
   invented, no unbacked medical or curative promise, no timeframe-plus-result. One fabricated claim
   can cost the ad account, which is far more expensive than a re-generation.

A pipeline run is **done** when: the image was approved by the user, the video's identity and voice
pass the checks above, and both assets (plus the handoff note to the destination skill, if any) were
handed to the user. If a check fails and the cause isn't obvious, say what looks off rather than
re-generating blind — a second guess wastes the same credits as the first.

---

## Workflow shortcuts

### "Quick UGC" — one-line brief
For "make a Gen Z girl talking about skincare in her bathroom":
1. Confirm the **identity strategy** (Step 1) — usually "one-off invented" for a quick brief.
2. Ask only what's genuinely missing; otherwise assume reasonable defaults and state them.
3. Build the image prompt, lock Block 3, `get_cost`, generate, get approval.
4. Build the Seedance prompt matching the avatar's profile, generate the video.
5. Present both results.

Defaulting confidently beats interrogating — the user can correct a default, but a wall of
questions kills momentum.

### "Avatar library" — reusing a character
The clean way is a **trained Soul**: train once (`show_characters action=train`), then every future
video is `soul_2` + the same `soul_id` with only clothing/pose/scene/dialogue changing. Offer to
save the `soul_id` (and the Block-3 JSON) so the same spokesperson returns across dozens of videos.
Without photos, reuse the first approved image's job id as a reference on every generation instead.

### "Image only" / "Video only"
Run whichever stage the user wants. Video-only needs a source image to upload as the `start_image`.

---

## Common mistakes to avoid
1. **Generic prompts** — "a woman talking to camera" yields a different person each time. Specify every physical feature.
2. **Voice-body mismatch** — sweaty/post-workout cannot sound calm and composed.
3. **Breaking character vocabulary** — check every dialogue line against the profile's DNA.
4. **Overloading timestamp windows** — one thought per ~5s.
5. **Forgetting negative prompts** — always include what to avoid (robotic delivery, facial drift, teleprompter eyes).
6. **Passing a URL as a media value** — import/upload first, pass the returned `media_id` (or a job id).
7. **Looking for `job_status`** — it doesn't exist; use `job_display` / `show_generations`, no poll loop.
8. **Skipping `get_cost`** — preflight credits before any generation the user hasn't pre-approved.
9. **Silently training a Soul** — Soul training costs time and credits; confirm the identity strategy first.

---

## Troubleshooting (real errors and their fix)

| Symptom | Cause | What to do |
|---|---|---|
| `403 "Pro" or "Ultimate" plan required` on `generate_video` | The model (`seedance_2_0`) requires a paid tier | Fall back to `seedance_2_0_mini` (runs on starter). The 403 **does not charge**. Tell the user the quality tradeoff. |
| Video comes out with the wrong face / identity drifts | The photo was passed as a URL, or `start_image` wasn't used | Upload the photo (`media_upload_widget` in Apps UI) and pass the `media_id` with `role: "start_image"`. Never a raw URL. |
| "remote tools cannot read chat attachments" | The photo was attached to the Claude chat | Use `media_upload_widget` (user picks it in the widget) or `media_import_url` if it's on the web. |
| A trained Soul model won't generate | Model-name variance (`soul_2` vs `text2image_soul_v2`) | Confirm with `models_explore action=get`; use the id the live catalog returns. |
| Can't find `job_status` | It doesn't exist | Use `job_display` (one id per call) or `show_generations`. No poll loop. |
| Quoted cost doesn't match the balance | The rounded `credits` was reported | Report `credits_exact`. And note: balance changes from another session/device are not from this run. |
| Generation stays `in_progress` for a while | It's async (normal) | Wait and re-call `job_display`. Image ~30–60s, video ~2–4 min. Don't re-generate (double charge). |

Base rule: if a call fails, **re-read the live schema/catalog (Step 0)** before retrying the same thing.
A `403`/validation error doesn't charge; blindly retrying a *valid* generation **can** double-charge.

## Relationship to other skills (Golden ecosystem)

This skill is the **factory for people and UGC video**. It does not build pages, run ads, or make
product images — it connects to the skills that do. Keep the handoffs clear so skills don't overlap:

**Receives from (inputs):**
- `golden-investigacion-mercado` / `golden-copywriting` → the **angle, hook, or script**. If the
  user has no script, delegate the copy to `golden-copywriting` and turn it into breathed dialogue
  (Layer 5). Never invent product claims — ask for them.
- `golden-dropkiller-productos-ganadores` → the **product/niche** that defines which avatar and message.

**Hands off to (outputs):**
- `golden-ads` → the **UGC .mp4 as a paid-ad creative** (Meta/TikTok). The #1 consumer of this
  skill's video. Hand over the video URL + the script used.
- `golden-shopify` → **image/video** for the product page (video section, UGC testimonials).
- `golden-web` / community portal → **welcome / hero video** (case proven live).

**Do not confuse with (clear boundaries):**
- `golden-imagen-arena` = **product** images (real photo + composed text, infographics/carousel). If
  the user asks for "product images for the listing" → that skill, not this. This makes **people
  and video**; that one makes **product**. Complementary, never substitutes.
- `golden-video-editor` (cuts silences, captions, assembles the final ad on HyperFrames) = editing/
  composition of a raw clip into a publishable video. This skill **generates** the raw UGC clip; if
  it needs **editing/assembly/captions**, hand the .mp4 to `golden-video-editor`.

Golden rule: this skill's job ends when it delivers the **asset** (image and/or .mp4). Publishing,
running ads, laying out a page, or editing belongs to the destination skill.

## Ruta alterna VERIFICADA: Google Vids (0 créditos)

Google Vids (incluido en Workspace) **sí crea un avatar a partir de una foto propia** y lo hace
hablar. Verificado el 2026-08-29 **hasta el lanzamiento del render**: avatar creado desde la foto, asignado, guion aceptado, vista previa generada (se vio el avatar con la cara correcta y 0:20 de duración) y `Generar` corriendo al 5%. **El MP4 terminado NO fue observado** — la extensión del navegador se desconectó antes. Las 5 trampas de abajo sí están medidas: son justo lo que bloqueaba y desbloqueaba el flujo. **Mientras la congelación de Higgsfield siga
vigente, esta es LA ruta para un talking-head**: HyperFrames no hace una persona fotorrealista
hablando y Seedance está en pausa.

El procedimiento exacto — las 5 trampas medidas incluidas (el file input oculto, el tope de 800
caracteres por escena, el guion de solo lectura, y los DOS botones en secuencia) — vive en
**`references/google_vids.md`**. Léelo antes de operar Vids: sin esas 5, el flujo se traba.

El oficio de guion de esta skill es model-agnostic y aplica igual a un guion pegado en Vids.

## Costos y elección de motor
Tarifas medidas por generación y el punto de equilibrio pay-per-use vs suscripción están en
**`references/costos_motores.md`**. Lo que no se delega a esa lectura: **iterar con el modelo
barato y gastar solo en la pieza final**, porque lo caro medido no es generar, es repetir.

## Reference files
- `references/image_framework.json` — The 5-block avatar prompt template, every field, enumerated options, a worked example, and the live-verified model/settings notes. Read when building or reusing an avatar identity.
- `references/seedance_prompt_system.md` — The full Seedance 2.0 system: 5 avatar profiles with vocabulary DNA, the layer formulas, the negative-prompt library, full worked templates, and live-verified Seedance params + media flow. Read when writing the video prompt.
- `references/compliance_casos.md` — Banco de casos de la lista negra en los dos sentidos: bueno limpio, bueno disfrazado y malo. Léelo al aprobar una pieza con personas.
- `references/google_vids.md` — Ruta Google Vids verificada en vivo: avatar desde foto propia, las 5 trampas medidas y el orden real de botones. Léelo antes de operar Vids.
- `references/verticales_sensibles.md` — Reglas de arte y compliance para salud/estética/pérdida de peso, con el corte de antes/después por vertical (Meta 2026). Léelo cuando la vertical sea sensible.
- `references/costos_motores.md` — Tarifas medidas por generación y break-even suscripción vs pay-per-use.
- `references/seedance_advanced.md` — Advanced Seedance techniques beyond the single talking head: multi-reference role mapping (@image/@video/@audio), beat-budgeting by duration, multi-shot transitions, camera/audio vocabulary, prompt hygiene, and character-sheet identity locking (incl. photoreal identity sheets). Read for multi-reference/multi-shot work or when identity drifts.

---

## Operación de la propia skill (blindaje y validación)

Esta skill se guarda **blindada**. Para editarla y volver a cerrarla, el orden importa:

**Abrir:** `chflags -R nouchg <skill>` y después `chmod -R u+w <skill>`.
**Cerrar:** `chmod -R a-w <skill>` **primero**, y `chflags -R uchg <skill>` **después** — al revés el
chmod falla porque el flag ya bloqueó el inodo. El **directorio** lleva su propio `uchg` y `555`.
Son **dos** mecanismos a la vez (flag y permisos): reponer solo uno deja la skill medio abierta.

**Validar antes de darla por buena** (salida 0 = en norma), siempre con **ruta ABSOLUTA**, porque
con `.` da un falso fallo:

    python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-ugc-avatar

**Estándar 9:** los cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO.

**Al cerrar cada versión se registra el sello en el changelog.** La receta canónica del árbol NO se
reinventa aquí: la declara `golden-skill-auditor` en su **Fase 5**, con sus limitaciones escritas; si
algo discrepa, manda la Fase 5. Se acompaña SIEMPRE del sello POR ARTEFACTO nombrando el archivo
(`md5 -q <ruta>/SKILL.md`, antes y después), que es el que un tercero puede correr para verificar el
par, y se deja el respaldo en disco: un hash sin decir qué se hasheó, o sin el archivo con el que
compararlo, es un rito y no una comprobación.

El historial completo de versiones y las actas del Centro de Mando viven en
`references/changelog.md`. No se borran: se mudan, y se comprueba que llegaron antes de quitarlas.

## Version & changelog
- **v1.15** — Encargo del Centro de Mando (mandato v2 de FER). **(1) La description pasa a español**:
  es el disparador y FER escribe en español; medida contra el tope duro de 1024 uniendo el escalar
  plegado como hace YAML. **(2) La lista negra de compliance se amplía de 1 a 5 prohibiciones** con
  las leyes medidas del 2026-09-04: aval médico falso (bata, estetoscopio, "mis pacientes", "avalado
  por la ciencia", "4.9/5 de expertos"), el producto que sale en cámara debe ser el que se despacha,
  el ingrediente falso que entra DIBUJADO y no escrito, y la prohibición del parche verbal (la pieza
  se rehace, no se le agregan palabras). **(3) Se añade el método de verificación**: el video se mira
  fotograma a fotograma, porque la transcripción no ve el envase ni la bata — auditar por
  transcripción deja pasar justo esas cuatro. **(4) Caso malo conocido** incluido para comprobar que
  la regla muerde, y sexto ítem en la compuerta de QA del Step 4.
Historial completo en `references/changelog.md` (incluye v1.13 y v1.12 palabra por palabra). Aquí
solo la última anterior a v1.15, para mantener el cuerpo bajo 500 líneas:

- **v1.14** — Divulgación progresiva: el cuerpo bajó de 582 a menos de 500 líneas moviendo a
  referencias tres bloques que solo se necesitan en casos concretos (procedimiento de Google Vids,
  reglas de verticales sensibles, tabla de costos). En el cuerpo queda la **decisión** — cuándo ir a
  cada ruta y las prohibiciones que no pueden esperar a una lectura — y el **detalle** se carga solo
  cuando hace falta. Motivo: el validador oficial avisaba que un cuerpo largo encarece la activación
  en cada disparo, y un cuerpo que nadie termina de leer protege menos que uno corto y apuntado.
