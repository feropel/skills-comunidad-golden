---
name: golden-ugc-avatar
description: >
  End-to-end UGC avatar creation pipeline on the Higgsfield MCP. Generates hyperrealistic AI
  avatar images with Higgsfield Soul 2.0 (or Nano Banana Pro), then animates them into
  talking-head UGC videos with Seedance 2.0 — through structured prompt frameworks that lock
  character identity and enforce voice/body coherence. Supports reusable identity via Soul
  training and Reference Elements, so one avatar stays the same person across dozens of videos.
  Use this skill whenever the user mentions UGC avatars, AI avatars, avatar generation, creating
  UGC content, making AI talking-head videos, generating avatar images for video, the Higgsfield
  workflow, Soul characters, Nano Banana avatar, Seedance UGC, the avatar pipeline, or anything
  about creating AI-generated people for social media content, ads, or brand videos. Also trigger
  when the user asks to "make a person," "create a character for video," "generate a talking-head,"
  "haz un avatar," "crea un UGC," "hazme un video hablando," or "un avatar para mi marca." Handles
  the image step AND the video step as one unified pipeline, and runs either stage alone when needed.
---

# Golden UGC Avatar — Higgsfield Pipeline

<!-- skill v1.7 · 2026-08-10 (loop del arsenal, semana 2 · producción): before/after cut BY VERTICAL added to the Step 2 health block. The 2026-08-07 norm banned before/after for dental only; Meta 2026 also bans it for anti-aging/wrinkles/firming and weight loss, and allows it for general cosmetics with an 18+ audience. Two cross-vertical bans added to the negative prompt: second person pointing at the viewer's condition, and timeframe-plus-result headlines (Meta judges implied meaning). Mirrored in golden-ecom-magic and golden-imagen-arena -->
<!-- skill v1.6 · 2026-08-07 (centro de mando, cosecha del chat un estudio de producto) · reglas de arte para verticales de SALUD (dental y afines) en el Step 2, aplicables a prompts de imagen Y video: prohibido bocas con lesiones, antes/después de dentadura, delantal/estetoscopio/sillón dental, porcentajes en pantalla y preguntas que señalen condición del espectador; permitido macro del gotario, textura, corte de esmalte ilustrado y lifestyle de baño -->
<!-- skill v1.4 · pipeline foto→video UGC sobre Higgsfield MCP · imagen soul_2/nano_banana_pro + video seedance_2_0 (fallback seedance_2_0_mini en plan starter) · verificado en vivo el camino imagen+talking-head; Soul reutilizable documentado, aún sin correr end-to-end · changelog completo al pie -->

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
Step 0  Verify Higgsfield MCP + discover models live
   ↓
Step 1  Choose IDENTITY strategy → Soul (reusable) | Element (instant ref) | one-off
   ↓
Step 2  Build image prompt (5-block framework) → generate_image (soul_2 / nano_banana_pro)
   ↓                                              → preflight get_cost → display result → approve
Step 3  Build Seedance prompt (5-layer stack) → generate_video (seedance_2_0, start_image)
   ↓                                              → display result
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

### Art rules for HEALTH verticals (dental and similar) — Centro de Mando norm, 2026-08-07
Field-proven in the Dental el producto del estudio study (Chile). When the product's vertical is oral
health or any sensitive health claim (supplements, skin, hair), apply these to every image AND
video prompt (they also feed the negative prompt in Step 3):

**FORBIDDEN in the frame:**
- Mouths with visible lesions (cavities, stains, inflamed gums).
- Before/after shots of teeth.
- White coat, stethoscope, dental chair — anything that reads as medical endorsement.
- Result percentages on screen ("95% effective").
- Questions that point at a viewer's condition ("do you have cavities?").

**ALLOWED and proven to convert:**
- Macro of the dropper/applicator.
- Product texture.
- ILLUSTRATED enamel cross-section (stylized diagram, never clinical photography).
- Bathroom lifestyle (daily routine, clean setting).

### Before/after: the cut by vertical (Meta 2026 — account risk)
The block above bans before/after for dental only. Meta bans it in more verticals, so the
real cut is this (verified 2026-08-10) and it applies to image AND video prompts:

- **FORBIDDEN** in anti-aging / wrinkles / firming / lifting, in weight loss, and in oral
  health or any sensitive health claim. Applies even if the brief asks for it: change the
  piece, do not deliver the split.
- **Allowed** in general cosmetics (nail, hair, localized spot) with an 18+ audience, the
  SAME area, no faces, and nothing that induces negative self-perception.

Across every vertical, and always into the negative prompt: no second person pointing at the
viewer's condition ("your wrinkles"), and no timeframe-plus-result headline ("results in 7
days"). Since 2026 Meta judges IMPLIED meaning — a timeframe next to a before/after split
reads as a misleading transformation claim even without the word "guaranteed".

**What replaces it and still converts:** texture macro, how-to-use, illustrated mechanism,
ingredients, lifestyle.

### Image models & settings *(verify with `models_explore action=get` before relying on these)*

| | `soul_2` (Higgsfield Soul 2.0) — **default for UGC/avatar** | `nano_banana_pro` (Google) — max quality / text |
|---|---|---|
| Use for | Realistic UGC, portraits, fashion, character; reusable Soul via `soul_id` | 4K detail, on-image text, diagrams, one-off refs |
| Key params | `quality`: `1.5k` / `2k` (default `2k`); `soul_id` (optional, from a trained Soul) | `resolution`: `1k` / `2k` / `4k` (default `1k`) |
| Aspect ratios | `1:1 16:9 9:16 4:3 3:4 3:2 2:3` | `1:1 9:16 16:9 4:5 5:4 4:3 3:4 3:2 2:3 21:9` |
| Reference media | one `image` role | one `image` role |

For vertical UGC use `aspect_ratio: "9:16"`. Pass a reference via `medias: [{ role: "image",
value: "<media_id or job_id>" }]` — never a raw URL (import URLs first with `media_import_url`).

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

### The coherence guarantee — voice must match the body
| Physical state | Voice must include |
|---|---|
| Running / HIIT | Audible breathing, staccato delivery, words cut short |
| Post-workout | Recovering breath, interrupted sentences, slower pace |
| Walking and talking | Cadence matching steps, natural pace |
| Seated / still | Controlled breathing, full sentences, deliberate pacing |
| Lying / stretching | Slowest pace, deepest register, long exhales |

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
- `golden-productos-ganadores` → the **product/niche** that defines which avatar and message.

**Hands off to (outputs):**
- `golden-ads` → the **UGC .mp4 as a paid-ad creative** (Meta/TikTok). The #1 consumer of this
  skill's video. Hand over the video URL + the script used.
- `golden-shopify` → **image/video** for the product page (video section, UGC testimonials).
- `golden-web` / community portal → **welcome / hero video** (case proven live).

**Do not confuse with (clear boundaries):**
- `golden-imagen-arena` = **product** images (real photo + composed text, infographics/carousel). If
  the user asks for "product images for the listing" → that skill, not this. This makes **people
  and video**; that one makes **product**. Complementary, never substitutes.
- `hyperframes` (the official video engine) = editing/composition with HTML. This skill **generates**
  the raw UGC clip; if it needs **editing/assembly/captions**, that's HyperFrames.

Golden rule: this skill's job ends when it delivers the **asset** (image and/or .mp4). Publishing,
running ads, laying out a page, or editing belongs to the destination skill.

## Cost reality check (why we stay on Higgsfield)

Pay-per-use aggregators (self-hosted frontends over MuAPI-style gateways) look "free" because the
repo is free — **the generations are not**. Verified market prices (mayo 2026), useful both to pick
the right model per job and to sanity-check any "free alternative":

| Model | What it is | ~Cost per generation | Best for |
|---|---|---|---|
| Flux Schnell | fast image | ~$0.03 | iterating ideas |
| Flux Pro | pro image | ~$0.10 | final deliverables |
| Midjourney v7 | stylised image | ~$0.15 | brand/aesthetic shots |
| Kling 2.5 | ~5s realistic video | ~$0.50 | reels, product motion |
| Sora 2 | ~10s cinematic video | ~$2.00 | hero shots |
| Veo 3 | ~8s video with audio | ~$3.00 | ads with sound |

**The break-even that nobody does:** under ~30 generations/month, pay-per-use is cheaper (saves
~$19/mo). At ~60-100/month it is a tie. **Above ~200/month you pay 3-5x more** than a flat
subscription. Golden operates well above the tie point (UGC + product images + ads), so the
**Higgsfield subscription stays** — and any "install this free repo instead" claim gets checked
against this table before switching. Rule: iterate with the cheap model, spend on the final only.

## Reference files
- `references/image_framework.json` — The 5-block avatar prompt template, every field, enumerated options, a worked example, and the live-verified model/settings notes. Read when building or reusing an avatar identity.
- `references/seedance_prompt_system.md` — The full Seedance 2.0 system: 5 avatar profiles with vocabulary DNA, the layer formulas, the negative-prompt library, full worked templates, and live-verified Seedance params + media flow. Read when writing the video prompt.
- `references/seedance_advanced.md` — Advanced Seedance techniques beyond the single talking head: multi-reference role mapping (@image/@video/@audio), beat-budgeting by duration, multi-shot transitions, camera/audio vocabulary, prompt hygiene, and character-sheet identity locking (incl. photoreal identity sheets). Read for multi-reference/multi-shot work or when identity drifts.

---

## Version & changelog
- **v1.6** — Art rules for HEALTH verticals (dental and similar) baked into Step 2, applying to image and video prompts. Harvest of the "un estudio de producto(Chile)" chat, assigned by the Centro de Mando (2026-08-07): forbidden — visible lesions, teeth before/after, medical-endorsement props (white coat, stethoscope, dental chair), on-screen result percentages, condition-pointing questions; allowed and field-proven — dropper macro, product texture, illustrated enamel cross-section, bathroom lifestyle.
- **v1.5** — Added the **Cost reality check** section: verified per-generation prices (Flux Schnell $0.03 → Veo 3 $3.00) and the pay-per-use vs subscription break-even (~30/mo saves, ~60-100 ties, >200 costs 3-5x more). Conclusion baked in: Golden stays on the Higgsfield subscription; "free repo" alternatives get checked against this table first. Rule: iterate cheap, spend on the final only. Destilado de una guía pública de Open-Generative-AI/MuAPI (mayo 2026), sin instalar nada.
- **v1.4** — Added `references/seedance_advanced.md` (destilado original, sin copiar terceros): multi-reference role mapping (image/video/audio, up to ~9/3/3), beat-budgeting by duration, multi-shot transition language, film-verb camera vocabulary, audio-as-first-class, prompt hygiene (keep settings out of prose), and **character-sheet identity locking** incl. photoreal identity sheets — the fix for one-off-invented drift. Wired into Step 1 (identity), Step 3 (video) and the reference list. Enriquece con lo mejor de la skill `video-prompting` (Seedance 2.0 + hojas de personaje) sin depender de ella.
- **v1.3** — Polish for community sharing: unified to English throughout, removed the legacy "Moko" trigger, flagged the Reference Element path as not-yet-verified-live. Core image+video path is live-proven; the Soul (trained reusable identity) path remains documented but unverified end-to-end.
- **v1.2** — Live-verified against the Higgsfield MCP end-to-end (image `soul_2` + video `seedance_2_0_mini`). Baked in: plan gating + `seedance_2_0_mini` fallback, `credits_exact` reporting, real presets are viral-effect (not UGC) clips, cross-skill handoffs, troubleshooting table. Privacy-audited for community sharing (no personal data in package).
- **v1.1** — Rewrote all operational wiring against the real model catalog (correct model IDs, params, media flow, no `job_status`, `get_cost` preflight, Soul/Element identity strategy).
- **v1.0** — Initial two-stage pipeline (image framework + Seedance system) with reference files.
