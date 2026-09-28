---
name: golden-video-teardown
description: >-
  Golden Group — TEARDOWN exhaustivo de videos publicitarios (ads, reels, TikTok, UGC, VSL).
  Desarma un video de cero a cien, segundo por segundo: transcribe el texto en pantalla y la
  locución, mapea el beat sheet completo (gancho, educación, demo, oferta, CTA), diagnostica
  el ángulo/enfoque, el hook, el copy y la oferta, marca fortalezas, debilidades y riesgos
  de baneo, y entrega una FÓRMULA replicable + brief para producir videos nuevos. Úsala
  SIEMPRE que el usuario quiera analizar, desglosar, "destripar" o entender un video de
  anuncio a fondo, saber qué dice/cómo está hecho, por qué funciona o no, qué copy usar, o
  extraer la fórmula para replicarlo — o diga cosas como "analiza este video", "desglosa
  este ad", "qué dice este video segundo a segundo", "hazme el teardown", "por qué funciona
  este creativo", "sácame la fórmula de este video", "analiza mis videos para replicarlos".
  Funciona para cualquier producto, nicho y país.
---

**Fábrica:** chat «✅ SKILL golden-video-teardown»
<!-- skill v1.6.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v1.6 · 2026-09-06 (auditoría golden-skill-auditor) · inventario.sh marcó "sin línea de versión bajo el H1": el comentario apuntaba al historial pero no seguía el patrón de la casa con la versión vigente visible de un vistazo. Historial completo en references/changelog.md (el cuerpo se paga en cada activación; el acta no). -->
# Golden Group — Teardown de videos publicitarios


Desarma cualquier video de anuncio de punta a punta y lo convierte en (1) un teardown exhaustivo segundo a segundo y (2) una fórmula replicable con brief para producir videos nuevos. Es la capa de INTELIGENCIA CREATIVA entre el rendimiento (`golden-meta-ads-analysis`) y la producción (`golden-ugc-avatar`, `golden-ads`).

## Antes de empezar — lo que TÚ tienes que tener

El teardown sale de los fotogramas reales del video, así que depende de herramientas del equipo.

| Qué necesitas | Tipo | Para qué | Cómo se consigue |
|---|---|---|---|
| **ffmpeg** (trae `ffprobe`) | Bloqueante | Sacar los fotogramas del gancho y de todo el video | `brew install ffmpeg` |
| **yt-dlp** | Degradable | Bajar el video cuando pasas un enlace (Paso 0) | `brew install yt-dlp` |
| **whisper-cpp** con el modelo `ggml-small.bin` | Degradable | Transcribir la locución | `brew install whisper-cpp`. El modelo: mira si ya está en `~/.cache/hyperframes/whisper/models/`; si no, `ggml-small.bin` de huggingface.co/ggerganov/whisper.cpp |
| *Opcional:* **jq** | Degradable | Leer los comentarios bajados con yt-dlp | `brew install jq` |

**Lo bloqueante para:** sin ffmpeg, `scripts/extract_frames.sh` se detiene con el comando para instalarlo; sin fotogramas no hay teardown. **Lo degradable se pide y se sigue:** con un enlace y sin yt-dlp no se bloquea (Paso 0): se pide el archivo y, mientras tanto, los metadatos salen por Firecrawl o por la biblioteca de anuncios de Meta, si están conectados. Sin transcriptor, el guion sale del texto en pantalla y se dice que la locución no se transcribió (principio 3). Si no tienes algo, dime y te guío paso a paso.

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

El teardown necesita el archivo en disco: los fotogramas salen de `ffmpeg` (instalado en este Mac;
la versión se comprueba con `ffmpeg -version`, no se escribe aquí — un número de versión en una
skill caduca solo y miente sin que nadie lo toque).
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

✅ **`yt-dlp` y `ffmpeg` INSTALADOS; el flujo URL → teardown se probó de punta a punta el
2026-08-01.** Las versiones NO se escriben aquí: se comprueban en el momento con `yt-dlp --version`
y `ffmpeg -version`. (Esta línea decía `yt-dlp 2026.07.04` y `ffmpeg 8.1.2`; el 18-sep ya eran
2026.08.19 y 9.0.1. `yt-dlp` en particular se actualiza muy seguido porque persigue los cambios de
cada red social: una versión vieja es la causa típica de que una descarga que funcionaba deje de
hacerlo, así que ante un fallo de descarga lo primero es `brew upgrade yt-dlp`.)

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

## Fronteras y desambiguacion

Frontera: el RENDIMIENTO en números (CPA/ROAS/qué pausar) lo da golden-meta-ads-analysis; la PRODUCCIÓN del video nuevo la hacen golden-ugc-avatar (video) y golden-ads + golden-copywriting (hooks/copys). Acepta uno o varios archivos locales (.mov/.mp4/.webm) por ruta, y URLs de YouTube/TikTok/Instagram/Facebook para descargar antes de analizar (ver Paso 0).

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-video-teardown
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-video-teardown
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-video-teardown`

Historial completo en `references/changelog.md`.
