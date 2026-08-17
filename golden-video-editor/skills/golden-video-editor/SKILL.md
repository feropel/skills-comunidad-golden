---
name: golden-video-editor
description: >-
  Golden Group — EDITOR DE VIDEO AUTOMÁTICO. Toma una grabación cruda (celular,
  cámara, pantalla) y la deja como anuncio o reel terminado: transcribe, corta
  silencios/muletillas/tomas repetidas, pone subtítulos sincronizados palabra por
  palabra, mete visuales (imágenes IA, animaciones, mockups, texto grande),
  efectos de sonido y música, y renderiza el video final. Motor: HyperFrames
  (gratis, local). Transcripción: Whisper LOCAL sin API key.
  Úsala SIEMPRE que el usuario quiera: editar un video, "córtame este video",
  "quítale los silencios", "ponle subtítulos", "edítame este reel", "hazme el
  anuncio con este video", "límpiame esta grabación", "replica este estilo de
  edición", o cuando arrastre un archivo de video pidiendo que lo deje listo para
  publicar. Dispara aunque no diga "editar": basta con una grabación cruda que
  haya que dejar publicable.
  NO usar para: analizar un anuncio ajeno y sacarle la fórmula (eso es
  golden-video-teardown), generar un avatar/UGC hablando desde cero
  (golden-ugc-avatar), escribir el guion (golden-copywriting / golden-matriz-viral),
  ni para imágenes de producto sueltas (golden-imagen-arena).
---

# Golden Video Editor — de grabación cruda a anuncio publicable

<!-- skill versión GVE1.2 · auditoría 2026-07-25: transcribe SIN --output (ese flag es solo para sidecar SRT/VTT; el transcript.json se escribe solo); añadido el andamio real del pipeline (npx hyperframes init --video y npx hyperframes render con quality/fps/format), que era el esqueleto que faltaba; voz em_alex marcada como no verificada; puntero a transcript-guide.md para filtrar tokens basura -->
<!-- skill versión GVE1.1 · ruta completa a captions.md de hyperframes, transcribe con --model small --language es, dependencias TTS declaradas, estado honesto del stack, manejo de errores por paso, caso borde de producto sin claims -->
<!-- skill versión GVE1.0 · creación: destilado del tutorial Horizontes IA + stack Golden (Whisper local, claims, checklist) -->

**Versión:** `GVE1.1` · Fábrica: chat centro de mando.

Graba con el celular sin preocuparte por trabarte, repetir o quedarte callado. Esta skill
se encarga del resto. Pensada para **anuncios COD y contenido orgánico de Golden**, no para
video genérico.

## Qué necesitas (cero API keys)

| Pieza | Para qué | Estado |
|---|---|---|
| Skills `hyperframes` + `hyperframes-media` + `hyperframes-cli` | Motor, media y CLI (en `~/.claude/skills/`) | ✅ instaladas |
| Paquete `hyperframes` (npm) | Corre vía `npx hyperframes ...`; se descarga solo al primer uso | ✅ verificado (v0.7.68+) |
| Whisper local | Lo trae el propio `transcribe`; descarga su modelo (~466 MB `small`) al primer uso a `~/.cache/hyperframes/` | ✅ autocontenido |
| `ffmpeg` | Cortes, extracción de audio, frames | ✅ instalado (Homebrew) |
| MCP Higgsfield | Imágenes y animaciones para los visuales | ⚠️ verificar en vivo (plan B abajo) |
| TTS español (`kokoro-onnx` + `soundfile` + `espeak-ng`) | Solo si hay voz en off | ⚠️ instalar al primer uso (paso 4) |

**Primera corrida:** necesita internet y unos minutos (npx baja el paquete y `transcribe`
baja el modelo Whisper). De ahí en adelante todo queda en caché y corre local.

**Ventaja Golden:** la transcripción corre **local con Whisper** vía
`npx hyperframes transcribe`. Sin AssemblyAI, sin OpenAI API, sin correo empresarial y sin
costo por minuto. Si algún día la detección de silencios queda corta, ahí sí se evalúa una
API externa — no antes.

## El pipeline (6 pasos)

### Paso 0 · Intake
Antes de tocar el video, confirma:
- **Destino:** anuncio Meta/TikTok (9:16), YouTube (16:9), o reel orgánico
- **Producto** y sus **claims permitidos y prohibidos** (lee el cerebro de marca o la
  memoria del producto — Toppik, Tag Recede y Le'côterra tienen claims blindados).
  Si el producto es nuevo y no tiene cerebro de marca ni memoria, pide los claims
  permitidos y prohibidos AQUÍ, una sola vez — jamás editar a ciegas: un claim malo
  tumba el anuncio en Meta y el render se paga dos veces
- **Duración objetivo** (ads COD: 25-40 s)
- **Estilo:** el de Golden por defecto, o replicar una referencia (ver "Replicar un estilo")

### Paso 1 · Contexto en CLAUDE.md + andamio del proyecto
Crea la carpeta del proyecto y un `CLAUDE.md` con: producto, destino, duración, estilo,
paleta, claims prohibidos y qué visual va en cada momento. Es la memoria del editor: sin
esto, cada iteración empieza de cero.

Scaffolda el proyecto real con:
```bash
npx hyperframes init <nombre> --video grabacion.mp4
```
Eso crea la estructura de HyperFrames, copia el video y ya transcribe con Whisper (hace el
Paso 1 y el Paso 2 de una). El video final es un **HTML de composición** con atributos
`data-*` que la skill `hyperframes` sabe autorar: ese HTML es el que junta cortes,
subtítulos, visuales y audio, y es lo que se renderiza al final.

### Paso 2 · Base limpia (cortes + subtítulos)
Si no usaste `init --video`, transcribe aparte:
```bash
npx hyperframes transcribe grabacion.mp4 --model small --language es
```
El comando escribe `transcript.json` (formato whisper.cpp, con timestamps de palabra) en
la carpeta del proyecto por sí solo. `--output` en `transcribe` es únicamente para exportar
un sidecar SRT/VTT y va con `--to srt|vtt`, no para el JSON.

**Siempre `--language es` y jamás un modelo `.en`:** los modelos `.en` TRADUCEN el audio
al inglés en vez de transcribirlo (regla no negociable de `hyperframes-media`). Si el
audio viniera en otro idioma, cambia el código; si no sabes el idioma, quita `--language`
y deja que Whisper lo detecte.

Pide la transcripción **con timestamps y SIN limpiar**. El transcript "sucio" es el que
permite cortar: si el modelo ya borró las repeticiones, se pierde dónde estaban. Filtra
tokens basura del transcript (`♪`, `�`, gaps largos) antes de cortar — el detalle está en
`~/.claude/skills/hyperframes/references/transcript-guide.md`.

Luego, sobre esos timestamps:
- Quita **silencios largos**, muletillas y **tomas repetidas**, quedándote con la buena
- **Nunca cortes la primera ni la última palabra** de una frase
- Deja un respiro mínimo entre frases (cortar demasiado suena robótico)

Subtítulos: **palabra por palabra, sincronizados**, mayúsculas, alto contraste, en
**español de Colombia**. Convenciones de estilo y sincronía: lee
`~/.claude/skills/hyperframes/references/captions.md` (reference de la skill `hyperframes`).

> Calibración: el primer corte casi nunca queda. Se ajusta diciendo "reduce más los
> silencios" o "no seas tan estricto". Es normal y es rápido.

### Paso 3 · Visuales (lo que da el dinamismo)
Mete un visual **cada vez que se menciona algo concreto**. Varía la técnica, no repitas:

1. **Imágenes IA** — Higgsfield o `golden-imagen-arena`. Producto = **foto real como
   semilla**, jamás redibujado (regla Golden de imágenes fieles).
2. **Animaciones** — clips cortos de Higgsfield para los momentos hero.
   > **Si el MCP Higgsfield no está conectado** (verifícalo antes de prometer visuales IA):
   > no te detengas — cubre esos momentos con mockups HTML/CSS, texto grande y las fotos
   > reales del producto (técnicas 3-5, gratis y locales), e INFORMA que las imágenes IA
   > quedaron pendientes de reconectar el MCP.
3. **Mockups en HTML/CSS** — interfaces, notificaciones, chats de WhatsApp, terminal.
   Se construyen con código dentro de HyperFrames: nítidos y sin costo.
4. **Texto grande** — la palabra clave a pantalla completa, resaltada.
5. **Iconos y logos** — apps, banderas, sellos de garantía.

Reglas: un visual no compite con la voz, la refuerza. El producto siempre se ve real.

### Paso 4 · Sonido
- **Efectos** en los cortes y las apariciones (pop, whoosh, ding). Si no hay librería a
  mano, arma una carpeta `sfx/` con archivos nombrados por su uso (`pop.wav`, `whoosh.wav`)
  y la skill los coloca por nombre.
- **Música** de fondo baja, que no tape la voz. Puede ser propia o generada.
- **Voz en off** cuando haga falta: `npx hyperframes tts` con voz española `ef_dora` (la
  única que trae la CLI verificada; `em_alex`, masculina, es un ID válido de Kokoro pero
  conviene probarlo antes de prometerlo). Lista las voces con `npx hyperframes tts --list`.
  El TTS necesita dependencias que NO vienen con el paquete: `pip3 install kokoro-onnx soundfile`
  y, para fonemas en español, `brew install espeak-ng`. Si faltan, instálalas primero (una vez);
  si la instalación no es posible en ese momento, sigue el pipeline SIN voz en off e informa
  el comando pendiente — la voz en off es opcional, el video no se bloquea por ella.

### Paso 5 · Render y verificación
Renderiza con `npx hyperframes render` (añade `--quality high` y el `--fps`/`--format`
del destino) y **míralo antes de dar por listo**. Checklist Golden:
- Se entiende sin sonido (subtítulos legibles en móvil)
- El gancho pega en los **primeros 3 segundos**
- Ningún claim prohibido del producto se coló en subtítulos ni en texto en pantalla
- Sin marcas de agua ajenas ni CTA en inglés
- Formato y duración correctos para el destino

### Paso 6 · Empaquetar el estilo
Cuando el resultado te guste, **destila ese estilo en su propia skill hija** (por ejemplo
`golden-video-editor-lecoterra`) con la paleta, los tiempos, el tipo de subtítulo y los
visuales que funcionaron. La próxima vez es un solo comando.

## Si algo falla (no se abandona el video)
- **`transcribe` falla o sale vacío** → verifica que el archivo tenga pista de audio
  (`ffprobe grabacion.mp4`); si el audio es ruidoso, sube a `--model medium`; si el modelo
  no descarga (sin internet), extrae el audio con ffmpeg y reintenta cuando haya conexión.
- **`npx hyperframes` no corre** → `npx hyperframes doctor` diagnostica el entorno
  (Chrome headless, Node, permisos). La skill `hyperframes-cli` tiene el detalle.
- **El render falla o se ve roto** → corre `npx hyperframes lint` y `npx hyperframes inspect`
  antes de reintentar: cachan tracks solapados y texto desbordado, que son las causas típicas.
- **MCP Higgsfield ausente** → plan B del paso 3 (mockups + texto grande + fotos reales).
- **TTS sin dependencias** → nota del paso 4 (instalar o entregar sin voz en off, informando).

## Replicar un estilo de referencia
Toma **capturas de pantalla** del video de referencia (3-5 momentos: gancho, un visual,
un subtítulo, el cierre) y pásalas como imagen. De ahí se extrae paleta, tipografía,
ritmo de corte y tipo de animación. **Se destila, no se clona:** el resultado sale con
identidad Golden, nunca con la marca ajena (regla de referencias).

## Reglas de oro
1. **Foto y video reales del producto.** La IA no redibuja el producto.
2. **Claims por producto.** Antes de escribir un subtítulo o un texto en pantalla, revisa
   lo prohibido de ese producto. Un claim malo tumba el anuncio en Meta.
3. **Sin signos de apertura** (ni el de interrogación ni el de admiración) en subtítulos ni en pantalla: solo los de cierre.
4. **Español de Colombia**, nada de traducción automática ni CTA en inglés.
5. **El primer resultado se itera.** Nadie acierta a la primera: se le dice qué cambiar.
6. **Verificar antes de entregar** (paso 5). Nunca se da por listo sin ver el render.

## Encadena con
- `golden-video-teardown` → saca la fórmula de un anuncio ganador; esta skill la ejecuta.
- `golden-copywriting` / `golden-matriz-viral` → el guion antes de grabar.
- `golden-ugc-avatar` → si no hay grabación real, genera el avatar hablando y luego se edita aquí.
- `golden-ads` → el video editado entra como creativo de la campaña.
- `hyperframes` + `hyperframes-media` + `hyperframes-cli` → el motor por debajo.

## Changelog
- **GVE1.1** (2026-07-23) — Auditoría con golden-skill-auditor: ruta completa a
  `captions.md` de la skill `hyperframes`, `transcribe` con `--model small --language es`
  (los modelos `.en` traducen, no transcriben), estado honesto del stack (npx descarga al
  primer uso; MCP Higgsfield se verifica en vivo con plan B; dependencias del TTS
  declaradas), sección "Si algo falla" y caso borde de producto nuevo sin claims.
- **GVE1.0** (2026-07-23) — Creación. Destilado del tutorial de Santiago Muñoz (Horizontes IA,
  "Claude Code acaba de destruir a los editores de video") y adaptado al stack Golden:
  se reemplaza AssemblyAI/OpenAI por **Whisper local** vía `hyperframes-media` (sin API key
  ni costo), se añaden las reglas Golden de claims y producto fiel, el checklist de
  verificación y el encadenado con las skills de ads. Aporte propio del tutorial que sí se
  conserva: transcript **sucio con timestamps** como base del corte, variar la técnica de
  visual en cada mención, replicar estilo desde capturas, y empaquetar el estilo final en
  una skill hija.
