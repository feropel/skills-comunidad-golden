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
<!-- skill GVE1.9 · 2026-08-31 (CdM) · compuerta de la congelacion de Higgsfield (estandar de FER 30-ago repartido por el CdM): tecnica 2 remite el movimiento a HyperFrames (0 creditos), video de Higgsfield CONGELADO, costo-antes para imagenes. Reversible al levantar la congelacion. -->
<!-- skill GVE1.8 · 2026-08-31 (CdM, fila del FILTRO) · SEGUNDA COSECHA de la MISMA fuente externa:
GVE1.7 tomo la estructura del carrusel; GVE1.8 toma la capa numerica del brief PDF completo (6 pag)
que llego despues. No es duplicado — son dos entregas del mismo autor con niveles de detalle distintos.
13 criterios numericos instalados donde cada uno trabaja (intake, corte, subtitulos, b-roll, sonido,
render, fallos). La prueba del sonido apagado cierra el par asimetrico del 85%: copywriting lo sabia
(5 menciones), el editor casi no (1) — ahora el lado que MONTA tambien lo ejecuta. -->
<!-- skill GVE1.7 · 2026-08-31 (CdM, fila del FILTRO — origen externo declarado: carrusel de edicion
con IA; se toma la PIEZA, no el archivo) · LEY DE ORDEN instalada VIVA antes del pipeline: cortar →
subtitular → ilustrar → sonorizar con el porque de cada posicion (dependencias, no estilo), las 4
instrucciones textuales de maquina, y el bloque "lo que la maquina NO decide". Reglas de b-roll (donde
se nombra, objeto sobre negro, NO stock) y sfx-desacoplado ancladas en los Pasos 3 y 4. Hueco medido
antes: orden 0, subtitular 0, b-roll 0. El pipeline ya tenia el macro-orden correcto; esto le da el
porque y el lenguaje de instruccion. -->
<!-- skill GVE1.6 · 2026-08-27 (chat FILTRO) · FIX: multicamara-una-camara.md quedo DORMIDO en GVE1.5 — citado en el sello pero SIN disparador en el cuerpo, o sea invisible para el flujo. Lo cazo el detector golden-capacidad-huerfana, que estrena chequeo de RECURSOS DORMIDOS a peticion del CdM tras el mismo fallo en golden-web (catalogo-de-estilos). Mismo error mio dos veces la misma noche. Disparador puesto en el Paso 2, que es donde se cortan. Barrido del ecosistema: 1 dormido de 243 referencias — este. -->
<!-- skill GVE1.5 · 2026-08-26 (chat FILTRO, autoridad de FER) · NUEVO references/multicamara-una-camara.md. Destilado de 2 PDFs de NinoDirector que FER envio el 16-ago y llevaba 10 dias en DESTILADOS sin que ninguna skill lo nombrara. Barrido previo: capacidad NUEVA, 0 de 89 skills mencionaban multicamara, punch-in ni encuadre. Numeros: cambio de encuadre ~1min30, nunca cada 10s, punch-in 113% con tope duro 125%, ventana de silencio 1,5s y si no hay silencio NO se corta. Regla que lo hace funcionar: el frontal SE GUARDA para el CTA. Enlaza con golden-imagen-arena para generar los 3 fondos. -->
<!-- skill GVE1.4.1 · 2026-08-24 (centro de mando): bump que la reparación del barrido B dejó sin subir — 5 skills editadas sin bump las veía intactas el censo (verificador de cierre). -->

<!-- skill versión GVE1.4 · 2026-08-23: Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->
<!-- skill versión GVE1.3 · auditoría golden-skill-auditor 2026-08-21: cierra la inconsistencia de versión (el cuerpo ya traía los cambios de GVE1.2 pero la línea "Versión:" y el Changelog se habían quedado en GVE1.1 — ahora coinciden); documenta el blindaje (chflags uchg) en el propio SKILL.md, no solo en el filesystem; completa el ejemplo de tts con --output -->
<!-- skill versión GVE1.2 · auditoría 2026-07-25: transcribe SIN --output (ese flag es solo para sidecar SRT/VTT; el transcript.json se escribe solo); añadido el andamio real del pipeline (npx hyperframes init --video y npx hyperframes render con quality/fps/format), que era el esqueleto que faltaba; voz em_alex marcada como no verificada; puntero a transcript-guide.md para filtrar tokens basura -->
<!-- skill versión GVE1.1 · ruta completa a captions.md de hyperframes, transcribe con --model small --language es, dependencias TTS declaradas, estado honesto del stack, manejo de errores por paso, caso borde de producto sin claims -->
<!-- skill versión GVE1.0 · creación: destilado del tutorial Horizontes IA + stack Golden (Whisper local, claims, checklist) -->

**Versión:** `GVE1.9` · Fábrica: chat centro de mando. · Blindada con `chflags uchg` (desbloquear con `chflags -R nouchg` antes de editar, volver a blindar con `chflags -R uchg` al cerrar).

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

## LEY DE ORDEN (por qué el pipeline va en este orden — GVE1.7)

**Cortar → Subtitular → Ilustrar → Sonorizar. El orden no es estilo, es dependencia:**
1. **CORTAR primero** fija la línea de tiempo; todo lo que venga después se ubica contra esos cortes.
2. **SUBTITULAR después** porque va contra el audio YA cortado — al revés se rehace el trabajo dos veces.
3. **ILUSTRAR (b-roll)** donde se NOMBRA algo — la escena responde al guion ya montado.
4. **SONORIZAR al final** porque el sonido tiene que REACCIONAR a lo que ya está montado.

**Las 4 instrucciones, textuales (así se le pide a la máquina):**
- "cortá los silencios" — ritmo natural, sin que se note el corte (la ventana de 1,5 s de esta skill).
- "subtítulos por palabra" — a la altura del pecho, la palabra clave más grande y en color.
- "b-roll donde nombro algo" — escena de objeto sobre negro, **NO stock**.
- "sfx desacoplado del corte" — el sonido NO cae donde cae el tijeretazo.

**Lo que la máquina NO decide (el bloque que hace la pieza honesta):** qué se dice y en qué
orden (el montaje acomoda, no decide la idea) · dónde va el silencio que INCOMODA (la
instrucción de cortar silencios te lo come si no lo marcás antes) · si la pieza merecía
existir — un reel bien editado sobre nada sigue siendo nada. El criterio de negocio que
gobierna todo esto: **la IA baja el costo de PRODUCIR; no baja el costo de tener algo que decir.**

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

**Los 3 prerrequisitos del crudo (GVE1.8 — sin ellos el pipeline produce basura pulida):**
1. **Audio de cámara/micrófono, no de celular a 3 metros** — la calidad del audio define
   el **80% del resultado**; ningún paso posterior lo repara.
2. **El guion COMO SE GRABÓ**, no el que se escribió — sin él la skill no sabe en qué
   segundo se nombra cada cosa, y por eso el b-roll cae donde no va.
3. **El look fijado** (color, tipografía del subtítulo, color del resaltado) — sin eso
   cada reel sale distinto y la grilla se ve desprolija.
Truco de grabación: **3 segundos en silencio al principio** — sirven para medir el ruido
ambiente y limpiarlo.

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

**Si el video es un plano fijo que se hace largo, abre `references/multicamara-una-camara.md`
ANTES de cortar.** Ahí está el método para fabricar tres cámaras con una sola: cuándo cambia el
encuadre (cuando cambia la idea, ~1 min 30 s; **cada 10 s no es ritmo, es ruido**), el punch-in al
113% con tope duro en 125%, y la regla que más pesa: **el corte cae en el silencio más cercano
dentro de una ventana de 1,5 s, y si no hay silencio NO se corta**. Meter más gráficos encima de
un plano fijo compra tiempo hasta el próximo corte; no arregla que el espectador siempre vuelva
al mismo cuadro.
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
tokens basura del transcript (`♪`, `�`, gaps largos) antes de cortar. Si una palabra se
transcribió mal, **déjala MARCADA en vez de adivinar** qué decía — el detalle está en
`~/.claude/skills/hyperframes/references/transcript-guide.md`.

Luego, sobre esos timestamps:
- Quita **silencios largos**, muletillas y **tomas repetidas** — de las repetidas te quedas
  con la **SEGUNDA** (la repetición casi siempre mejora la toma); y **si dudas entre cortar
  o dejar, DEJA**
- **Nunca cortes la primera ni la última palabra** de una frase
- Deja **200 ms de aire entre frases** — es el arreglo exacto cuando los cortes suenan secos
  y se pisan las palabras (cortar demasiado suena robótico)

Subtítulos: **palabra por palabra, sincronizados**, **máximo 3 palabras en pantalla** a la vez, mayúsculas, alto contraste, en
**español de Colombia**. Convenciones de estilo y sincronía: lee
`~/.claude/skills/hyperframes/references/captions.md` (reference de la skill `hyperframes`).

> Calibración: el primer corte casi nunca queda. Se ajusta diciendo "reduce más los
> silencios" o "no seas tan estricto". Es normal y es rápido.

### Paso 3 · Visuales (lo que da el dinamismo)

**Regla de b-roll (ley de orden):** se ilustra donde el guion NOMBRA algo — escena de objeto sobre negro, jamás stock genérico, y de **menos de un segundo** cada pieza.
Mete un visual **cada vez que se menciona algo concreto**. Varía la técnica, no repitas:

1. **Imágenes IA** — Higgsfield o `golden-imagen-arena`. Producto = **foto real como
   semilla**, jamás redibujado (regla Golden de imágenes fieles).
2. **Animaciones** — para los momentos hero. **🔴 CONGELADO (FER 30-ago, `feedback_higgsfield_solo_imagenes_y_costo_antes`): CERO video en Higgsfield hasta que FER lo levante.** El movimiento se hace con HyperFrames (el motor de esta skill, 0 créditos), NO con clips de Higgsfield. Si necesitas una IMAGEN de Higgsfield para un frame, di el costo con `get_cost:true` y ESPERA el sí de FER antes de generar.
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

**Regla de sfx (ley de orden):** desacoplado del corte — el efecto no cae donde cae el tijeretazo, reacciona al montaje ya hecho.
- **Efectos** en los cortes y las apariciones (pop, whoosh, ding). Si no hay librería a
  mano, arma una carpeta `sfx/` con archivos nombrados por su uso (`pop.wav`, `whoosh.wav`)
  y la skill los coloca por nombre.
- **Música** de fondo con **ducking: 12 dB abajo cuando hay voz** — así nunca la tapa. Puede ser propia o generada.
- **Voz en off** cuando haga falta:
  ```bash
  npx hyperframes tts "texto del guion" --voice ef_dora --output narracion.wav
  ```
  `ef_dora` es la voz española verificada en el stack Golden (`em_alex`, masculina, es un ID
  válido de Kokoro pero conviene probarlo antes de prometerlo). Lista las voces con
  `npx hyperframes tts --list`.
  El TTS necesita dependencias que NO vienen con el paquete: `pip3 install kokoro-onnx soundfile`
  y, para fonemas en español, `brew install espeak-ng`. Si faltan, instálalas primero (una vez);
  si la instalación no es posible en ese momento, sigue el pipeline SIN voz en off e informa
  el comando pendiente — la voz en off es opcional, el video no se bloquea por ella.

### Paso 5 · Render y verificación
Renderiza con `npx hyperframes render` (añade `--quality high` y el `--fps`/`--format`
del destino) y **míralo antes de dar por listo**.

**Antes de renderizar, pide SIEMPRE el reporte de cortes: "dime en qué segundo quedó cada
corte y qué frases descartaste".** Sin ese reporte, la frase importante que se comió el corte
la descubres mirando el reel ya publicado.
**Número de control:** un crudo de 1:40 baja a **~58 s con ~40 cortes**. Si devuelve **1:20,
los silencios NO se cortaron** — hay ruido de fondo que impide detectarlos (ver "Si algo falla").

Checklist Golden:
- **Prueba del sonido apagado** (el **85% ve sin sonido** — ley que golden-copywriting ya
  aplica al escribir): mira el corte MUDO. Si se entiende de qué va y en qué momento quedarse,
  el montaje está bien; **si necesitas el audio, faltan cortes o falta b-roll**. Subtítulos
  legibles en móvil.
- El **primer segundo tiene algo que frena el scroll**, y el gancho pega en los **primeros 3 segundos**
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
- **Cortes secos, palabras que se pisan** → falta el aire: 200 ms entre frases.
- **Subtítulos desfasados** → se sincronizaron contra el CRUDO en vez del video ya cortado:
  rehacer desde el Paso 2 respetando la ley de orden. Es **el error más caro** — por eso
  subtitular va SIEMPRE después de cortar.
- **B-roll fuera de lugar** → no se entregó el guion COMO SE GRABÓ (prerrequisito 2 del intake).
- **La música tapa la voz** → falta el ducking de −12 dB del Paso 4.
- **El video sale largo (1:20 en vez de ~58 s)** → los silencios no se detectaron por ruido
  de fondo: limpiar el audio con la muestra de los 3 s iniciales y recortar de nuevo.
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

- **GVE1.9** (2026-08-31) — Compuerta de la CONGELACIÓN de Higgsfield (cambio de estándar de FER 30-ago, repartido por el CdM): la técnica 2 de visuales deja de ofrecer clips de video de Higgsfield (congelados) y remite el movimiento a HyperFrames (0 créditos); recuerda el costo-antes-con-aprobación para imágenes. Reversible cuando FER levante la congelación.
- **GVE1.8** (2026-08-31) — SEGUNDA COSECHA de la misma fuente (GVE1.7 vino del carrusel; esto del brief PDF completo de 6 páginas, fila del FILTRO): la capa NUMÉRICA — 200 ms de aire entre frases, máx 3 palabras en pantalla, b-roll <1 s, ducking −12 dB, quedarse con la SEGUNDA toma, palabra mal transcrita se marca no se adivina, 3 prerrequisitos del crudo (audio de cámara = 80% del resultado, guion como se grabó, look fijado, 3 s de silencio inicial), reporte de cortes obligatorio antes de renderizar, número de control 1:40→~58 s (1:20 = ruido), tabla de 5 fallos con causa y arreglo, prueba del sonido apagado (ley del 85% que ya vivía en golden-copywriting, ahora también en el lado que MONTA), y el criterio de negocio de cierre.
- **GVE1.7** (2026-08-31) — LEY DE ORDEN instalada viva antes del pipeline (cortar→subtitular→ilustrar→sonorizar con el porqué de cada dependencia), las 4 instrucciones textuales de máquina, el bloque "lo que la máquina NO decide", y reglas de b-roll (donde se nombra, objeto sobre negro, NO stock) y sfx-desacoplado en los Pasos 3 y 4. Origen externo declarado; fila del FILTRO, horneado en el CdM.
- **GVE1.4.1** (2026-08-24): bump de las ediciones del 24 (verificador de cierre R2: la version vive en 4 caras — sello, linea Version, Changelog y REGISTRO — y el bump anterior toco solo el sello).
- **GVE1.4** (2026-08-23) — Estándar 9 (Centro de Mando): los cambios relevantes de esta skill
  se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. (Entrada añadida en el barrido del
  arsenal 2026-08-24: el cambio existía solo como sello en comentario, sin su entrada aquí.)
- **GVE1.3** (2026-08-21) — Re-auditoría con golden-skill-auditor: la línea "Versión" y este
  Changelog se habían quedado en GVE1.1 mientras el cuerpo del pipeline ya traía los cambios
  de GVE1.2 (andamio `init --video`, `transcribe` sin `--output`, voz `em_alex` marcada como
  no verificada) — ahora todo coincide. Se documenta el blindaje (`chflags uchg`) en la línea
  de versión y se completa el ejemplo de `tts` con `--voice`/`--output`.
- **GVE1.2** (2026-07-25) — Andamio real del pipeline: `npx hyperframes init --video` para
  scaffoldar y transcribir de una, `transcribe` sin `--output` (ese flag es solo para sidecar
  SRT/VTT), ejemplos de `render` con `--quality`/`--fps`/`--format`, voz `em_alex` marcada
  como no verificada, puntero a `transcript-guide.md` para filtrar tokens basura.
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
