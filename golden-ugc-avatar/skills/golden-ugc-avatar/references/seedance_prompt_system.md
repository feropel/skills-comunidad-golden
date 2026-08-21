# Seedance 2.0 Prompt System — Full Reference

Complete prompt architecture for animating a UGC avatar image into a talking-head video with
Seedance 2.0 (`seedance_2_0`) via the Higgsfield MCP. The SKILL.md has the operating summary;
this file has the depth — the five avatar profiles with their vocabulary DNA, the layer
formulas, the negative-prompt library, and full worked templates.

## Table of contents
1. [The 5-layer stack](#1-the-5-layer-stack)
2. [Layer 1 — Avatar profiles & vocabulary DNA](#2-layer-1--avatar-profiles--vocabulary-dna)
3. [Layer 2 — Scene formula](#3-layer-2--scene-formula)
4. [Layer 3 — Emotional/physical state](#4-layer-3--emotionalphysical-state)
5. [Layer 4 — Voice direction](#5-layer-4--voice-direction)
6. [Layer 5 — Timestamp choreography](#6-layer-5--timestamp-choreography)
7. [Dialogue writing rules](#7-dialogue-writing-rules)
8. [Voice-to-action matching](#8-voice-to-action-matching)
9. [Negative-prompt library](#9-negative-prompt-library)
10. [Full worked templates](#10-full-worked-templates)
11. [Technical settings](#11-technical-settings)

---

## 1. The 5-layer stack

A Seedance UGC prompt is assembled from five layers. Each answers a different question:

| Layer | Question it answers |
|---|---|
| 1. Avatar identity | Who is talking, and how do they talk? |
| 2. Scene | Where are they and what's around them? |
| 3. Emotional/physical state | What is the body doing and feeling right now? |
| 4. Voice direction | What does the voice literally sound like? |
| 5. Timeline | What happens, second by second? |

The single most important principle across all layers: **the voice must match the body**. If
Layer 3 says she just ran up stairs, Layer 4 and Layer 5 must show breathlessness. Any
disconnect between how the avatar looks and how it sounds is what makes AI video read as fake.

---

## 2. Layer 1 — Avatar profiles & vocabulary DNA

Pick the profile that matches the character. Each profile is a complete voice: its vocabulary
DNA, speech rhythm, and forbidden words. The dialogue you write in Layer 5 must obey the chosen
profile's DNA — that consistency is what makes the avatar feel like a specific real person
rather than a generic AI script.

### Profile A — Gen Z Creator (18–24)
- **Use for:** fitness, lifestyle, trends, casual UGC, product hauls
- **Vocabulary DNA:** "lowkey," "highkey," "no but actually," "it's giving," "the way that," "I can't," "literally obsessed," "bestie," "trust me on this"
- **Speech patterns:** runs sentences together, trails off, self-interrupts, upspeak at ends, fast then sudden pause for emphasis
- **Delivery:** intimate, like talking to a close friend on FaceTime; low mic distance; unpolished energy
- **Never says:** "furthermore," "I find this invigorating," "in conclusion," anything that sounds scripted or corporate

### Profile B — Millennial Wellness (25–34)
- **Use for:** wellness, self-care, skincare, reflective/aspirational content
- **Vocabulary DNA:** "honestly," "I've been loving," "this has genuinely," "little ritual," "checking in," "be gentle with yourself," "small thing but," "game changer"
- **Speech patterns:** warmer, more complete sentences than Gen Z, but still casual; thoughtful pauses; soft landings
- **Delivery:** calm, confiding, slightly slower; the friend who has their life a bit more together
- **Never says:** Gen Z slang ("it's giving," "lowkey" feels forced), hard-sell language

### Profile C — Authority / Expert (30–50)
- **Use for:** business, consulting, educational, "here's what most people get wrong" content
- **Vocabulary DNA:** "here's the thing," "what most people miss," "the data shows," "in my experience," "let me break this down," "the mistake I see," "three things"
- **Speech patterns:** structured, deliberate, full sentences, confident pauses, numbered logic
- **Delivery:** measured, credible, direct to camera; controlled pacing; clear articulation
- **Never says:** filler slang, uptalk, "lowkey," anything that undercuts authority

### Profile D — High-Energy Fitness (any age)
- **Use for:** workout content, HIIT, motivation, action
- **Vocabulary DNA:** "let's go," "no excuses," "one more," "you've got this," "right now," "feel that," "don't stop," "push"
- **Speech patterns:** short bursts, imperatives, counting, cut by breath; energy carries over words
- **Delivery:** loud-adjacent, driving, breath-interrupted; physically exerted
- **Critical:** this profile almost always pairs with a breathless/exerted physical state — Layer 4 and 5 must show audible breathing

### Profile E — Luxury / Aspirational (any age)
- **Use for:** luxury products, ASMR-adjacent, aesthetic, "quiet luxury" content
- **Vocabulary DNA:** sparse, precise: "this," "notice," "the way it," "quietly," "effortless," "you deserve," long pauses instead of filler
- **Speech patterns:** slow, low, deliberate; few words, heavy silences; lets the visual breathe
- **Delivery:** breathy-close mic, intimate, unhurried; almost whispered
- **Never says:** hype slang, fast delivery, anything loud or rushed

---

## 3. Layer 2 — Scene formula

```
[Location type] + [Time/lighting] + [Atmosphere] + [Key props] + [Ambient sound]
```

Example: *"Sunlit bedroom + soft morning light + calm and private + unmade bed and coffee mug
+ faint birdsong and a distant city hum."*

The ambient sound matters as much as the visual — it grounds the clip as a real captured
moment. Silence-clean audio reads as a studio.

---

## 4. Layer 3 — Emotional/physical state

```
Physical: [what the body just did / is doing]
Emotional: [primary emotion] with [undercurrent]
Physical tells: [how it shows — breathing, posture, micro-expressions]
```

Example:
```
Physical: just sat down after a brisk morning walk
Emotional: content with a thread of quiet excitement
Physical tells: slightly elevated breathing settling down, a flush in the cheeks, relaxed shoulders
```

The "undercurrent" is what keeps the avatar from looking flat — a single clean emotion reads as
a mask; a primary emotion with a second one underneath reads as a person.

---

## 5. Layer 4 — Voice direction

```
[Gender], approximately [age]. [Register]. [Delivery style].
[Physical influence on voice]. [Emotional coloring]. [Mic proximity].
```

Example: *"Female, approximately 28. Warm mid-register, slight vocal fry. Confiding, unhurried
delivery. Breath still settling from the walk so phrases come in gentle waves. Colored with
quiet excitement. Close mic, intimate, like a voice note to a friend."*

Every clause does work: register and delivery set the baseline, the physical-influence clause
is what enforces voice-body coherence, and mic proximity sets the intimacy that UGC lives on.

---

## 6. Layer 5 — Timestamp choreography

Structure each shot. Keep one thought per window (~5s) so the model can actually perform it.

```
SHOT [n] ([start]s-[end]s): [Shot type + camera move]
Visual: [what happens on screen]
Action: [the specific physical motion]
Voice: (delivery notes) "Dialogue line"
Audio: [ambient + SFX]
Emotion: [the feeling in this exact moment]
```

Example:
```
SHOT 1 (0s-5s): Selfie close-up, slight handheld sway
Visual: she settles into frame, pushes a strand of hair back
Action: small exhale, soft smile blooms
Voice: (gentle, breath settling) "okay so... [exhale] I have to tell you about this"
Audio: faint birdsong, room tone
Emotion: warm, conspiratorial
```

---

## 7. Dialogue writing rules

1. **No full scripts.** Write fragments, interruptions, restarts — the way people actually talk. A clean paragraph read aloud is the tell of AI.
2. **Match vocabulary to the profile, always.** Check every line against the Layer 1 DNA.
3. **Physical state overrides personality.** Even the Profile C expert sounds different after climbing stairs. Body first.
4. **One thought per timestamp window.** Cramming two ideas into 5 seconds makes delivery rushed and unnatural.
5. **Silence is dialogue.** Direct the pauses explicitly — a held beat communicates more than a filler word.
6. **Write the breathing.** Use `[inhale]`, `[catching breath]`, `[exhale]` inline so the model performs real breath, not smooth TTS.
7. **End on resonance, not information.** Close on a feeling or an open loop, not a summary. UGC sells the vibe, not the bullet points.

---

## 8. Voice-to-action matching

This is the non-negotiable coherence table. Whatever the body is doing in Layer 3, the voice in
Layers 4–5 must carry the matching signature:

| Physical state | Voice must include |
|---|---|
| Running / HIIT | Audible breathing, staccato delivery, words cut short mid-phrase |
| Post-workout | Recovering breath, interrupted sentences, slower than normal pace |
| Walking and talking | Rhythmic cadence matching footsteps, natural conversational pace |
| Seated / still | Controlled breathing, full sentences, deliberate pacing |
| Lying / stretching | Slowest pace, deepest register, long audible exhales |
| Just laughed / excited | Slightly breathless, higher pitch, words tumbling |
| Cold / outdoors | Tighter breath, quicker clipped delivery, occasional shiver in voice |

---

## 9. Negative-prompt library

Always include a `【Negative Prompts】` block. Pull from these four categories. Omitting them is
a top cause of uncanny output.

- **Visual:** facial drift / face morphing, identity change between frames, deformed hands or
  extra fingers, warped teeth, flickering features, plastic skin, doubled pupils, melting
  accessories, background warping.
- **Audio:** robotic/monotone delivery, smooth TTS cadence, audio-video lip desync, unnatural
  pacing, missing breath, studio-clean silence where ambient sound belongs.
- **Performance:** teleprompter eyes (reading off-camera), frozen body, mechanical head turns,
  over-acting, fake smile held too long, no micro-expressions.
- **Style:** over-saturated color, cinematic film look that breaks the smartphone UGC aesthetic,
  studio lighting, slow-motion where it isn't wanted, watermark, on-screen text artifacts.

---

## 10. Full worked templates

### Template 1 — Profile B, 10s skincare UGC (calm, seated)

```
【Avatar】
A 28-year-old Latina woman, slim build, warm light-brown skin, dark brown loose waves with a
center part, oval soft-jawed face, warm brown almond eyes, a small beauty mark above the left
lip, wearing an oversized cream knit sweater. Just sat down on her bed.
Maintain exact appearance throughout, consistent character, no deformation.

【Scene】
Sunlit bedroom, soft morning window light, calm and private, unmade white bedding and a coffee
mug nearby, faint birdsong and quiet room tone.

【Emotional/Physical State】
Physical: settled, relaxed shoulders, holding the phone at arm's length
Emotional: content with a thread of quiet excitement
Physical tells: easy breathing, a soft natural blink rate, a half-smile that comes and goes

【Voice Direction】
Female, approximately 28. Warm mid-register, slight vocal fry. Confiding, unhurried. Easy
relaxed breath. Colored with quiet excitement. Close mic, intimate, like a voice note.

【Timeline】
SHOT 1 (0s-5s): Selfie close-up, slight handheld sway
Visual: she tucks a strand of hair back, soft smile
Voice: (gentle) "honestly? [exhale] I wasn't gonna post this but..."
Audio: birdsong, room tone
Emotion: warm, conspiratorial

SHOT 2 (5s-10s): same framing, leans in slightly
Visual: small genuine smile, glance down then back to camera
Voice: (softer, landing) "this little morning thing just... changed my whole skin. that's it."
Audio: room tone
Emotion: quietly proud, open loop

【Negative Prompts】
Facial drift, identity change, deformed hands, plastic skin; robotic/TTS delivery, lip desync,
missing breath; teleprompter eyes, frozen body, held fake smile; over-saturated color, studio
lighting, on-screen text.

【Technical】
720p, 9:16, 10s. Handheld selfie. Slight wide-angle. Natural warm color grade.
```

### Template 2 — Profile D, 15s post-workout (breathless, exerted)

```
【Avatar】
A 25-year-old athletic man, lean muscular build, short dark hair damp with sweat, defined jaw,
wearing a black training tee. Just finished a hard set.
Maintain exact appearance throughout, consistent character, no deformation.

【Scene】
Home gym, hard daylight through a window, intense focused atmosphere, dumbbells and a towel,
the hum of effort and a faint fan.

【Emotional/Physical State】
Physical: just dropped the weights, chest heaving
Emotional: driven, satisfied burn
Physical tells: heavy audible breathing, sweat at the brow, words cut by breath

【Voice Direction】
Male, approximately 25. Lower register pushed by effort. Driving, breath-interrupted. Heavy
breathing breaks the phrases. Charged with adrenaline. Close mic, a bit loud.

【Timeline】
SHOT 1 (0s-5s): Chest-up, slight handheld bounce
Visual: wipes brow with forearm, looks to camera
Voice: (breathless, staccato) "[catching breath] okay— that one... that one hurt."
Audio: fan hum, breath
Emotion: spent but fired up

SHOT 2 (5s-10s): same, leans on knees then up
Voice: (cut by breath) "no excuses today. [inhale] one more round. let's go."
Audio: breath, distant clank
Emotion: defiant

SHOT 3 (10s-15s): straightens, points at camera
Voice: (driving) "[exhale] you've got this. right now."
Audio: fan hum
Emotion: motivating, direct

【Negative Prompts】
Calm composed voice (mismatch), facial drift, deformed hands; smooth TTS, missing breath, lip
desync; frozen body, teleprompter eyes; cinematic slow-mo, over-saturation, watermark.

【Technical】
1080p, 9:16, 15s. Handheld. Natural high-contrast daylight grade.
```

---

## 11. Technical settings *(live-verified)*

Tool: `generate_video`. Set `model` and params at the top level of `params`. Confirm exact ranges
with `models_explore action=get model_id=seedance_2_0` before relying on them.

| Parameter | Real values |
|---|---|
| Model | `seedance_2_0` (identity-consistent, native audio) — **needs Pro/Ultimate plan** (403 on starter/free). **Starter fallback: `seedance_2_0_mini`** (480p/720p only; ~25 cr for 10s/720p, verified live). A 403 does not consume credits. |
| `duration` | integer seconds, **4–15** (default 5). UGC sweet spot 8–12 |
| `resolution` | `480p` / `720p` / `1080p` / `4k` — **`1080p` and `4k` require `mode: "std"`**; `mode: "fast"` supports only 480p/720p |
| `mode` | `std` (quality, all resolutions) / `fast` (cheaper, 480p–720p) |
| `generate_audio` | `true` for a talking-head with native audio (default true); `false` for silent |
| `genre` | `auto` (keep auto for UGC realism); others: action/horror/comedy/noir/drama/epic |
| `bitrate_mode` | `standard` / `high` |
| `aspect_ratio` | `9:16` for vertical UGC (also: auto/16:9/4:3/3:4/1:1/21:9) |
| Media roles | `start_image` (the approved avatar) + optional `end_image`, `image_references`, `video_references`, `audio_references` |

**Presets (verified live):** `presets_show` lists Higgsfield's presets, but they are **viral /
cinematic character-effect** clips (e.g. Baseball Game, Drift Racing, Zombie Dance, Red Carpet,
superhero transforms) — NOT talking-head UGC. For a person speaking to camera, use the hand-built
Seedance prompt above. Use a preset only for a viral effect clip: pick a `preset_id` from
`presets_show`, then `generate_video` with `model: "higgsfield_preset"` + `preset_id`. List live —
the catalog changes.

**Media rule:** `medias[].value` must be a `media_id` (from `media_confirm` / `media_import_url`)
or a completed image **job id** — never a raw `https://` URL.

**MCP call sequence:**
1. Get a `media_id` for the approved image: `media_upload` → PUT bytes → `media_confirm`
   (Apps UI local file → `media_upload_widget`; web URL → `media_import_url`). Or reuse the image's
   completed **job id** directly as the `medias` value — no re-upload needed.
2. *(optional)* `generate_video` with `params.get_cost: true` to preflight credits; report it.
3. `generate_video` — `model: "seedance_2_0"`, the full prompt, `medias: [{ role: "start_image",
   value: "<media_id or job_id>" }]`, `aspect_ratio`, `duration`, `resolution`, `mode`,
   `generate_audio: true`.
4. `job_display` the returned job id to render the result.

There is **no `job_status` polling tool** — generations are non-blocking; do not loop a poll step.
Use `job_display` (one id per call) or `show_generations` to browse history.
