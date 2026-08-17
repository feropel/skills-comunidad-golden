# Seedance 2.0 — Advanced techniques (multi-reference, beats, transitions, character sheets)

Companion to `seedance_prompt_system.md`. That file covers the single-`start_image` talking-head
(the 5-layer stack). Use **this** file when the shot needs more: multiple references, a multi-shot
sequence, tighter camera/audio direction, or a character sheet to lock identity before animating.

Written original for Golden. Underlying model behavior per ByteDance Seed / Volcengine Seedance 2.0
official prompting guides. Always confirm exact param names/ranges live with
`models_explore action=get model_id=seedance_2_0` before relying on them.

---

## 1. Multi-reference prompting — map every asset to a role

Seedance 2.0 is multimodal: besides the `start_image`, it accepts extra references
(`image_references`, `video_references`, `audio_references` per the live schema; official materials
cite up to ~9 images / 3 videos / 3 audio clips). **Don't just attach them — name what each one
contributes**, or the model averages them into mush.

Role map (name each in the prompt):
- **Character reference** → identity anchor: face, build, wardrobe. The most important.
- **Scene reference** → environment / location.
- **Props / wardrobe reference** → objects, costume detail.
- **Storyboard / composition reference** → framing and shot layout.
- **Video reference** → motion rhythm, camera move, continuity.
- **Audio reference** → voice texture, ambience, music, timing.

Write one explicit mapping line, e.g.:
> "Use the person from the character reference, the location from the scene reference, the props
> from the wardrobe reference, and the motion rhythm from the video reference."

**Image-to-video / edit / extend:** treat the references as fixed anchors and describe **only what
changes, continues, or should be emphasized** — do not re-describe the anchor in depth (that fights
the reference). In the MCP call, `start_image` stays the approved avatar; attach the extras in their
`*_references` roles.

---

## 2. Beat budgeting — match complexity to duration

Duration is a **generation param, not prose**. Use it only to plan how many beats fit:

| Duration | Beats to write |
|---|---|
| 4–6s | 1 beat — one action arc + one camera move |
| 8–12s (UGC sweet spot) | 2–3 beats |
| 15s | 2–4 beats, or a short multi-shot sequence |

Cramming beats makes delivery rushed and breaks realism — the same reason the 5-layer stack keeps
**one thought per ~5s window**.

---

## 3. Multi-shot transitions

When a clip has more than one shot, direct the **cuts** so the sequence feels planned, not stitched.
Explicit labels work well: `Shot 1`, `Cut to close-up`, `Final shot`. Transition phrasing:
- "opening with…"
- "the shot transitions to…"
- "the camera pans to reveal…"
- "the ending pushes in on…"

Keep shot order explicit and coherent; **one main camera move per shot**.

---

## 4. Camera & motion vocabulary (film verbs, not mood words)

Seedance is marketed on camera control — use standard verbs:
`slow push-in`, `fast pan`, `tracking shot`, `profile shot`, `orbit`, `low-angle follow`,
`close-up`, `top-lit close-up`, `rack focus`, `whip pan`.

Describe motion in **chronological beats** with visible cause/effect and physical outcomes
(balance shift, fabric drag, breath, recoil, splashing) — visible behavior beats abstract intensity
words. A good Seedance prompt reads like a compact shot breakdown, not a keyword list.

---

## 5. Audio as first-class (deepen Layers 4–5)

Seedance generates **native audio** — direct it, don't leave it to chance:
- **Dialogue:** the exact spoken line (brief enough to fit the shot's timing).
- **Ambience:** room tone, street, birdsong.
- **Music:** a style, or explicitly "no background music".
- **Foley / SFX:** specific triggers.
- **Sync moments:** where a sound hits an action — e.g. "voiceover enters only on the final product
  close-up", "laughter rises as the reveal lands".

If the clip should be silent except one sound family, say so directly ("only the sound of rain").

---

## 6. Prompt hygiene — what NOT to put in the prompt text

Keep these **out of the prompt prose** — they are generation **params** set in the MCP call, not
words the model should read:
`model name/version (seedance_2_0)`, `duration`, `resolution`, `aspect ratio`, `mode`, `generate_audio`.

The `【Technical】` block in the worked templates is a **planning note for you** — do not send it as
part of the model prompt. Putting settings into prose can confuse the model and wastes tokens.

---

## 7. Character sheets — lock identity BEFORE image-to-video

A **character sheet** (turnaround / model sheet / identity sheet) is one image with the same
character from multiple angles + expressions. It is the strongest **prompt-only** consistency tool,
and it is the fix for the **"one-off invented" drift** problem (Step 1): generate the sheet first,
then every scene still and every i2v shot references it.

**Downstream order:**
1. Generate the character sheet (image model: `soul_2` / `nano_banana_pro`).
2. Generate a scene still using the sheet as the reference.
3. Generate the Seedance image-to-video from that scene still.

**Prompt order for a sheet:**
1. State the output **is** a character sheet / turnaround / model sheet.
2. Define identity in concrete visual terms (age range, build, skin tone, hair, face anchors, notable features).
3. Lock the outfit + silhouette.
4. Specify the panels: full-body front, three-quarter, profile, back; + optional expression row + hands/props.
5. Consistency constraints across panels: "the same person in every panel, identical face and wardrobe, neutral even lighting, plain background".
6. **One character per sheet** (separate sheets for multiple characters).

### Photoreal identity-sheet mode (real-person / documentary realism)
When the avatar must feel like a **real person photographed repeatedly**, not a redesigned 3D asset:
- preserve **facial asymmetry** (don't average into a generic beauty render)
- keep **age cues, skin texture, small imperfections**
- natural posture, not rigid symmetry

Useful phrasing: `real-world photographic identity sheet`, `the same person photographed across
multiple angles`, `natural human asymmetry preserved`, `real skin texture and age cues`,
`soft neutral documentary lighting`. Use negative constraints sparingly (only to suppress a
synthetic / over-stylized look). If the user uploaded a portrait, treat it as the identity anchor
and build the sheet around it instead of reinventing the character.

---

**When to reach for this file:** multi-subject or multi-reference shots, sequences longer than one
beat, clips that need real camera/audio direction, or any time identity drifts — build a character
sheet and feed it back. For the standard single-`start_image` talking head, `seedance_prompt_system.md`
is enough.
