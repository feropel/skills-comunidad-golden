---
name: golden-video-teardown
description: Golden Group — TEARDOWN exhaustivo de videos publicitarios (ads, reels, TikTok, UGC, VSL). Desarma un video de cero a cien, segundo por segundo: transcribe el texto en pantalla y la locución, mapea el beat sheet completo (gancho, educación, demo, oferta, CTA), diagnostica el ángulo/enfoque, el hook, el copy y la oferta, marca fortalezas, debilidades y riesgos de baneo, y entrega una FÓRMULA replicable + brief para producir videos nuevos. Úsala SIEMPRE que el usuario quiera analizar, desglosar, "destripar" o entender un video de anuncio a fondo, saber qué dice/cómo está hecho, por qué funciona o no, qué copy usar, o extraer la fórmula para replicarlo — o diga cosas como "analiza este video", "desglosa este ad", "qué dice este video segundo a segundo", "hazme el teardown", "por qué funciona este creativo", "sácame la fórmula de este video", "analiza mis videos para replicarlos". Funciona para cualquier producto, nicho y país. Frontera: el RENDIMIENTO en números (CPA/ROAS/qué pausar) lo da golden-meta-ads-analysis; la PRODUCCIÓN del video nuevo la hacen golden-ugc-avatar (video) y golden-ads + golden-copywriting (hooks/copys). Esta skill es el puente: convierte un video en su fórmula y su brief. Acepta uno o varios archivos locales (.mov/.mp4/.webm) por ruta, y URLs de YouTube/TikTok/Instagram/Facebook para descargar antes de analizar (la descarga y sus comentarios están medidos en TikTok; Instagram y Facebook sin probar aún — ver Paso 0).
---

# Golden Group — Teardown de videos publicitarios

<!-- skill v1.4 · 2026-08-21 (auditoría golden-skill-auditor) · Reparación tras auditoría 840/1000 (BRONCE):
     (1) corregido el sobre-promesa de Instagram/Facebook en el description y el Paso 0 — antes sonaba
     verificado, ahora dice explícitamente que solo YouTube/TikTok están medidos; (2) nuevo Paso "Intake"
     al inicio (producto/país/moneda/rendimiento se piden UNA vez, no goteados); (3) nuevo Paso 5 de QA
     con checklist de "terminado" contra los 6 Principios, antes de guardar; (4) ejemplo real entrada→salida
     agregado a plantilla-teardown.md; (5) ruta de mlx-whisper ya no asume Python 3.9 hardcoded, se resuelve
     en vivo; (6) blindaje: chflags uchg (documentado aquí, no solo en el inventario). Blindada de nuevo al
     cierre de esta reparación. -->
<!-- skill v1.3 · 2026-08-02 (centro de mando) · ALCANCE REAL DE yt-dlp EN TIKTOK, medido sobre un video real: la DESCARGA funciona (bajo formato 1080p) y los METADATOS tambien (canal, 49.400 vistas, 986 likes), pero --write-comments devuelve comments: 0. El teardown segundo a segundo de un TikTok sale COMPLETO; la capa de comentarios no. Para esa: Chrome MCP o pegado. Instagram/Facebook siguen sin probar y se dice que no se probaron -->
<!-- skill v1.2 · 2026-08-01 (centro de mando) · yt-dlp 2026.07.04 INSTALADO Y PROBADO: el Paso 0 pasa de "pendiente-con-dueño" a operativo, flujo URL→teardown completo. + Se añade la descarga de COMENTARIOS con like_count (30 medidos): los más votados son objeciones/elogios ya validados por la audiencia, material directo para fortalezas/debilidades y para el brief. + Regla Cero ampliada a 3 modos de fallo (alucinación / señuelo con title poblado / muro anti-bot sin campo json): la verificación que caza los tres es "el dato responde a lo que pedi?" -->
<!-- skill v1.1 · 2026-07-31 (centro de mando) · ACEPTA URL: nuevo Paso 0 de descarga (yt-dlp para YouTube/TikTok/IG/FB) — antes solo aceptaba ruta local, así que un link no se podía analizar. yt-dlp YA ESTÁ INSTALADO (v2026.07.04, verificado el 2026-08-11 — el pendiente quedó resuelto); ffmpeg SÍ (v8.1.2). Mientras tanto, 3 salidas sin bloquear: metadatos por Firecrawl (YouTube da título/canal/vistas/likes reales, postprocesador nativo — pero NO el archivo), descarga manual, o Meta Ad Library. Regla Cero heredada: metadata.title vacío = json alucinado -->
<!-- skill v1.0 · teardown segundo a segundo + fórmula/brief · extract_frames.sh (ffmpeg) + STT opcional (hyperframes transcribe / mlx-whisper / openai-whisper) -->

Desarma cualquier video de anuncio de punta a punta y lo convierte en (1) un teardown exhaustivo segundo a segundo y (2) una fórmula replicable con brief para producir videos nuevos. Es la capa de INTELIGENCIA CREATIVA entre el rendimiento (`golden-meta-ads-analysis`) y la producción (`golden-ugc-avatar`, `golden-ads`).

## Cuándo se dispara
- "analiza este video / estos videos", "desglosa este ad", "teardown", "qué dice segundo a segundo", "por qué funciona este creativo", "sácame la fórmula", "analiza mis videos para replicarlos".
- El usuario pasa uno o más archivos de video por ruta local (.mov, .mp4, .webm…).
- **O pasa una URL** de YouTube / TikTok / Instagram / Facebook / Meta Ad Library → ver Paso 0.

## Principios
1. **Cero a cien, sin omitir.** Del segundo 0 al último. Cada beat con su timestamp, su texto en pantalla y su descripción visual.
2. **El texto quemado es el guion.** Los ads COD suelen llevar subtítulos quemados: son la fuente principal del copy. Transcríbelos literal.
3. **Locución cuando se pueda.** Si hay whisper/STT disponible, transcribe el audio; si no, recupera el guion del texto en pantalla (di explícitamente que la locución no se transcribió).
4. **Diagnóstico, no descripción.** No basta con "sale una persona": di el ÁNGULO (problema-solución, testimonio, autoridad, demo satisfactorio, miedo/HPV, veneno-vs-crioterapia…), por qué el hook funciona, y qué copiar.
5. **Riesgo de baneo explícito.** Marca marcas de agua ajenas, CTA en inglés, empaques de otra marca, español automático, claims médicos prohibidos.
6. **Siempre termina en fórmula + brief.** El objetivo es replicar: qué ADN reusar, qué evitar, y un brief listo para producción.

## Flujo

### Paso 0 — Si llega una URL en vez de un archivo (descarga)

El teardown necesita el archivo en disco: los fotogramas salen de `ffmpeg` (✅ instalado, v8.1.2).
Una URL no se analiza directamente — se descarga primero.

```bash
# Vía principal (cubre YouTube, TikTok, Instagram, Facebook, X):
yt-dlp -o "~/Desktop/teardown/%(title).60s.%(ext)s" "<URL>"

# Con comentarios y metadatos, que alimentan el diagnóstico de ángulo:
yt-dlp --write-comments --write-info-json -o "~/Desktop/teardown/%(title).60s.%(ext)s" "<URL>"
```

⚠️ **La DESCARGA funciona en TikTok; los COMENTARIOS no** (medido 2026-08-02 sobre un video real:
bajó el formato 1080p sin problema y trajo metadatos —canal, 49.400 vistas, 986 likes— pero
`comments: 0`). O sea: el teardown segundo a segundo de un TikTok sale completo; lo que no sale
es la capa de comentarios. Para esa, Chrome MCP o pegado del usuario.

⚠️ **Instagram y Facebook: la descarga NO está probada** (solo YouTube y TikTok tienen medición
real documentada arriba). Si `yt-dlp` funciona ahí, trátalo con la misma Regla Cero que Firecrawl
más abajo: confirma que el archivo bajado abre y dura lo mismo que el original antes de seguir. Si
falla o el resultado no coincide, dilo explícitamente y usa las 3 salidas sin bloquear de abajo —
nunca reportes IG/FB como "descargado y verificado" sin haber corrido esa comprobación.

✅ **`yt-dlp 2026.07.04` INSTALADO y probado** (2026-08-01), junto a `ffmpeg 8.1.2`. El flujo
URL → teardown está operativo de punta a punta.

**Extra que vale la pena en un teardown:** bajar también los COMENTARIOS del anuncio. Traen
`like_count`, así que los más votados son las objeciones y los elogios que la audiencia ya validó
— material directo para las secciones de fortalezas/debilidades y para el brief:
```bash
yt-dlp --write-comments --write-info-json --no-warnings \
  --extractor-args "youtube:comment_sort=top;max_comments=100" \
  -o "~/Desktop/teardown/%(title).60s.%(ext)s" "<URL>"
jq -r '.comments[] | "[\(.like_count)] \(.author): \(.text)"' <archivo>.info.json
```
Medido: 30 comentarios con autor, texto y likes. `comment_sort=top` y `max_comments` son
obligatorios o intenta bajar millones.

**Si yt-dlp falla con una URL concreta (red social que cambió su API), tres salidas — nunca bloquear:**
1. **Metadatos por Firecrawl:** `firecrawl_scrape` con `formats:["json"]` + `proxy:"stealth"` da
   **título, canal, vistas y likes reales** de YouTube (postprocesador nativo, cifras verificadas).
   Encuadra el video y mide su tracción, pero **no da el archivo**.
   ⚠️ Nunca `json` + `actions`: timeout (3 de 3). Y correr la Regla Cero: existe el campo `json`? ·
   `metadata.title` poblado? · `url` == `sourceURL`? · **el dato responde a lo que pedí?**
   📖 `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`
2. **Descarga manual** por el usuario y pasar la ruta local — el camino que nunca falla.
3. **Meta Ad Library:** los creativos de la competencia se bajan desde la propia biblioteca; el
   MCP de Meta (`ads_library_search`) da la ficha del anuncio para cruzarla con el teardown.

Una vez hay archivo en disco, seguir al Paso 1 con normalidad.

### Intake (una sola vez, al inicio)
Antes de arrancar, reúne de una vez lo que solo el usuario tiene y que va en el encabezado del
teardown (`references/plantilla-teardown.md`): producto, país, modelo de pago (COD/anticipado),
moneda, y si hay datos de rendimiento (CPA/ROAS) de `golden-meta-ads-analysis` para cruzar. Si el
usuario no los da y no se infieren del nombre del archivo/URL, pregúntalos UNA vez aquí — no los
gotees pregunta por pregunta a mitad del teardown. Si de verdad no importan para el análisis
creativo (el usuario solo quiere la fórmula), sigue sin ellos y dilo en el encabezado ("país/moneda
no informados").

### Paso 1 — Specs y fotogramas
Para cada video, corre:
```bash
bash ~/.claude/skills/golden-video-teardown/scripts/extract_frames.sh "<ruta del video>" "<carpeta de salida>"
```
Genera `hook_<nombre>.png` (gancho 0-4s, 8 frames) y `dense_<nombre>.png` (1 frame/1.5s, todo el video), e imprime duración/resolución/audio. Léelos con la tool **Read** para transcribir texto + visuales.
- Prioriza densidad en los primeros 3s (el hook decide el 80% del rendimiento).
- Si un video es largo (>45s) o denso, extrae un segundo filmstrip de la parte que falte.

### Paso 2 — Locución (opcional, si hay STT)
**Flujo validado (recomendado):** fotogramas (hojas de contacto del Paso 1) + transcripción del AUDIO con
whisper → con las dos capas se mapea el **ÁNGULO de venta por video** (dolor, deseo, prueba social,
autoridad, demo satisfactorio, miedo/urgencia…). Ese ángulo es el puente hacia el resto del arsenal:
`golden-copywriting` (los copys/hooks por video) y `golden-ads` (ruteo video→destino: qué creativo a qué
conjunto/página). Para la locución hay tres vías, de más a menos garantizada:
```bash
# 1) Whisper local directo (la más rápida y la que deja el texto en pantalla):
#    Una sola vez: brew install whisper-cpp + un modelo ggml-small.bin
ffmpeg -v error -i "<video>" -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y && \
  whisper-cli -m <ruta>/ggml-small.bin -l es -nt -f audio.wav
#    Atajo si está en el PATH del equipo: golden-transcribe "<video>"
#    Medido 2026-08-11 sobre el mismo video: 3,7 s contra 21,7 s de la vía npx, y el texto sale
#    por stdout en vez de quedarse en un archivo. Mismo motor y mismo modelo (ggml-small).
# 1b) La misma vía, por hyperframes (la que usa golden-video-editor):
npx hyperframes transcribe "<video>" --model small --language es
# 2) mlx-whisper (Neural Engine, rápida). OJO: su binario NO suele estar en el PATH — vive en
#    ~/Library/Python/<versión de python3 del equipo>/bin. Averigua la versión real en vez de
#    asumir 3.9 (varía por Mac): python3 --version
#    y usa esa carpeta, o agrégala al PATH:
ffmpeg -y -i "<video>" -vn -ac 1 -ar 16000 audio.wav && ~/Library/Python/"$(python3 -c 'import platform;print(".".join(platform.python_version_tuple()[:2]))')"/bin/mlx_whisper audio.wav --language Spanish --model mlx-community/whisper-small
# 3) openai-whisper portable (instala con: pip3 install openai-whisper):
ffmpeg -y -i "<video>" -vn -ac 1 -ar 16000 audio.wav && whisper audio.wav --language Spanish --model small
```
`transcribe` de HyperFrames baja su modelo la primera vez y no pide API key. Si NINGÚN
STT está disponible, salta este paso, apóyate en el texto quemado y dilo en el reporte.
Nunca uses un modelo `.en`: traduce al inglés en vez de transcribir.

### Paso 3 — Teardown por video
Rellena la plantilla de `references/plantilla-teardown.md` para cada video: metadata → beat sheet segundo a segundo → hook → ángulo/enfoque → copy/guion → oferta/CTA → fortalezas → debilidades/riesgos → veredicto (replicar/rescatar/descartar). Si hay datos de rendimiento (de `golden-meta-ads-analysis`), crúzalos.

### Paso 4 — Síntesis
Cuando hay varios videos: tabla comparativa (ganador/medio/descartar), los ADN ganadores comunes, la lista de OBLIGATORIOS y PROHIBIDOS, y 2-3 briefs de video nuevo (hook + texto en pantalla + estructura), listos para pasar a producción.

### Paso 5 — QA antes de entregar
Antes de guardar, revisa tu propio teardown contra esta checklist — es la definición de "terminado":
- El beat sheet cubre del segundo 0 al último, sin saltos (Principio 1 — cero a cien, sin omitir).
- Cada texto en pantalla citado es literal, no parafraseado (Principio 2).
- Dice explícitamente si la locución se transcribió o no, y con qué vía (Principio 3).
- Cada video tiene ángulo diagnosticado, no solo descrito (Principio 4).
- Se revisaron los riesgos de baneo de la plantilla: marca de agua, CTA en inglés, empaque ajeno, español automático, claims médicos (Principio 5).
- Hay fórmula + brief de cierre, no solo el desglose (Principio 6).
- Ningún dato del video (metadatos, comentarios, descarga) se reportó como verificado sin haber pasado la Regla Cero del Paso 0.
Si algo de esto falta, complétalo antes de entregar — no lo dejes para que el usuario lo note.

### Paso 6 — Entregable y guardado
Guarda el teardown completo como documento markdown en la carpeta del producto/proyecto (no dentro de la memoria: la memoria solo lleva un puntero). Reporta al usuario la síntesis + el siguiente paso (producir con golden-ugc-avatar / golden-ads).

## Conexiones
- **Números (CPA/ROAS, qué pausar/escalar):** `golden-meta-ads-analysis`. Cruza sus rankings con este teardown para saber qué creativo GANADOR replicar.
- **Producir el video nuevo:** `golden-ugc-avatar` (avatar/UGC/talking-head), `golden-ads` + `golden-copywriting` (hooks y copys).
- **Investigación de producto/mercado (voz del cliente, ángulos):** `golden-investigacion-mercado`.

## Pendiente / limitación conocida
- **No existe hoy una skill de OPTIMIZACIÓN de video a spec de Meta** (exportar a 1080×1920, H.264, AAC,
  `+faststart`, recompresión de material 4K a peso subible). Esta skill DESARMA y diagnostica, no reempaqueta
  el archivo final. Es candidata a **skill nueva** o a un **módulo dentro de `golden-ads`**. Anotado como
  hueco del arsenal — NO implementar aquí; cuando se aborde, decidir dónde vive antes de construir.

## Recursos
- `scripts/extract_frames.sh` — extrae hook strip + filmstrip denso de un video.
- `references/plantilla-teardown.md` — plantilla estándar del teardown por video + síntesis.
