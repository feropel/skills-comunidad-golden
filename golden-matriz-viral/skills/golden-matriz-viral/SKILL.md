---
name: golden-matriz-viral
description: >
  Golden Group — MATRIZ DE CONTENIDO VIRAL. Desmenuza el contenido que YA funcionó (tuyo o de
  2-3 creadores de referencia) y extrae la fórmula: hooks, estructuras, temas, emociones y CTAs
  que conectan — en una MATRIZ accionable. Con esa matriz genera guiones nuevos on-brand
  (reels/TikTok/shorts) y los pre-califica con una rúbrica de viralidad antes de grabar.
  Úsala SIEMPRE que el usuario quiera: analizar sus videos virales, "por qué pegó este video",
  sacar la fórmula/patrón viral de un creador, armar la matriz de contenido, generar guiones
  para reels/TikTok con base en lo que funciona, planear contenido orgánico del mes, armar el
  calendario editorial de reels/TikTok (cuánto publicar, mezcla tráfico/valor/conexión/venta),
  o predecir si un guion tiene potencial. Dispara con "matriz viral", "fórmula viral", "analiza
  estos videos", "guiones virales", "contenido para redes basado en datos", "calendario de
  contenido", "cuánto debo publicar". NO es para pauta pagada (golden-ads) ni para escribir el
  copy de un anuncio suelto (golden-copywriting): esto es la CAPA DE INTELIGENCIA del contenido
  orgánico.
---

# Golden Matriz Viral — la fórmula de tu contenido

<!-- skill v1.6 · 2026-08-21 · golden-skill-auditor: (1) Versión desincronizada — la etiqueta decía
GMV1.4 mientras el Changelog ya iba en GMV1.5 (la transcripción local con whisper-cpp de la Fase 1
ya estaba en el cuerpo pero la versión no lo reflejaba); corregido a GMV1.6, único número en todo
el archivo. (2) El description no mencionaba la Fase 5 CALENDARIZAR (capacidad real que la skill
ya entrega) — se agregaron trigger y frase de disparo. (3) Se agregó un ejemplo concreto
entrada→salida de un renglón de matriz y un guion (Fase 2/3) para que el primer uso no dependa de
inferir el formato. (4) Se agregó definición explícita de "terminado" por fase. (5) Blindaje:
`chflags uchg` — mecanismo documentado aquí y en el registro de golden-skill-auditor. -->

**Versión:** `GMV1.6` · Fábrica: chat centro de mando.
El principio: el algoritmo ya te dijo qué funciona — está en tus métricas y en las de los
creadores que admiras. Esta skill convierte esa evidencia en una fórmula reutilizable.

## Fase 1 — INGESTA (juntar la evidencia)

Acepta lo que el usuario tenga, sin exigir formato. **Máxima autonomía: si el usuario da links,
NO le pidas que pegue métricas a mano — tráelas tú primero** (paso 1) y solo pide lo que falte.

1. **Automático con Firecrawl** (verificado 2026-07-31, funciona HOY sin instalar nada):
   `firecrawl_scrape` con `formats:["json"]` + `proxy:"stealth"` sobre la URL del video.
   - **YouTube:** trae **título, canal, vistas y likes exactos** — Firecrawl tiene postprocesador
     nativo de YouTube. Medido: 1.798.929.737 vistas / 19.293.598 likes, cifras limpias.
   - ⚠️ **NO trae comentarios** (`comentarios: []`, con y sin scroll). Cargan por JS bajo demanda.
   - ⚠️ **Nunca `json` + `actions`:** se cae por timeout (probado 2 de 2). Pedir el json pelado.
   - 📖 Recetas completas y trampas: `golden-investigacion-mercado/references/scraping-firecrawl.md`
2. **El TEXTO del video — ✅ se transcribe SOLO, en local (2026-08-11).** Ya no hay que pedirle al
   usuario que pegue el guion:
   ```bash
   # Una sola vez:  brew install ffmpeg whisper-cpp  + bajar un modelo ggml-small.bin
   ffmpeg -v error -i "<video>" -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
   whisper-cli -m <ruta>/ggml-small.bin -l es -nt -f audio.wav
   # Atajo si el equipo lo tiene en el PATH:  golden-transcribe "<video>"
   # Sin instalar nada (mismo motor, más lento): npx hyperframes transcribe "<video>" --model small --language es
   ```
   Whisper-cpp, gratis, sin llave y **sin que el archivo salga del Mac**. *Medido: 7,5 minutos de
   audio en 29 segundos.* Transcribe todas las piezas que vayas a desmenuzar: el guion hablado es
   la materia prima del hook, y los subtítulos quemados **no** se leen del fotograma porque van una
   palabra por cuadro. Un guion pegado por el usuario sigue sirviendo, pero ahora es el respaldo.
3. **Comentarios — ✅ `yt-dlp` INSTALADO Y PROBADO (2026-08-01).** Es la mina de oro real:
   ```bash
   yt-dlp --write-comments --skip-download --no-warnings \
     --extractor-args "youtube:comment_sort=top;max_comments=100" \
     -o "salida.%(ext)s" "<URL>"
   jq -r '.comments[] | "[\(.like_count)] \(.author): \(.text)"' salida.info.json
   ```
   Medido: 30 comentarios con **`author`, `text` y `like_count`**, de ~2.450.067 disponibles.
   🎯 **`like_count` es lo que cambia el juego:** un comentario con miles de likes es un dolor,
   una objeción o un chiste que la audiencia YA validó **por votación**. Ordenados por likes dan
   la jerarquía real de lo que le importa a la gente — mejor materia prima para hooks que
   cualquier lluvia de ideas. Alimenta directo la columna Tema/ángulo y Emoción de la matriz.
   ⚠️ `comment_sort=top` y `max_comments` son obligatorios: sin tope intenta bajar millones.

   🚨 **SOLO YOUTUBE. En TikTok da CERO comentarios** (medido 2026-08-02 sobre un video real:
   metadatos sí — título, canal, **49.400 vistas, 986 likes** — pero `comments: 0`).
   | Red | Metadatos | Comentarios |
   |---|---|---|
   | YouTube | ✅ | ✅ con `like_count` |
   | TikTok | ✅ vistas y likes | ❌ **cero** |
   | Instagram / Facebook | ⚪ sin probar | ⚪ sin probar |

   **Para TikTok:** usar los metadatos para RANKEAR qué piezas valen el estudio (vistas y likes son
   dato duro), y sacar el texto de los comentarios por **Chrome MCP** (scrollear y leer el DOM) o
   pegado del usuario. **Decirlo cuando pase — nunca presentar como "minado" lo que no se minó.**
   Reddit no es opción: Firecrawl lo rechaza y el navegador lo bloquea por política.
4. **Pantallazos de métricas** para lo que ninguna vía saque (saves, shares, retención — esas
   solo están en el panel del creador y solo el dueño de la cuenta las ve).

🚨 **Regla Cero del scraping — 4 modos de fallo, `statusCode: 200` no prueba nada.**
🔒 **Lo más rápido es correr el candado, no acordarse:**
`python3 ~/.claude/skills/golden-investigacion-mercado/scripts/candado_scraping.py resp.json --pedi "<lo pedido>"`
Devuelve PASA / REVISAR / DESCARTAR. A mano, las 4 verificaciones:
existe el campo `json`? (si no → muro anti-bot, medido en Amazon) · `metadata.title` poblado?
(vacío → **el extractor inventa**: devolvió un Smart TV con precio y reseñas falsos para una
página de verrugas) · `metadata.url` == `sourceURL`? (cambió → estás leyendo otra página: Temu
devolvió 72 categorías de ropa con `title` poblado) · **🎯 el dato responde a lo que pedí?**
Una métrica falsa en la matriz contamina TODOS los guiones que salgan de ella. Enlaza con la
regla de la Fase 2: **métricas reales, jamás inventadas.**

**Nunca bloquear por falta de herramienta:** si una vía no está, se dice y se sigue por la
siguiente.

**Regla de arranque:** si el usuario tiene poco contenido propio, pedir 2-3 creadores de
referencia que le gusten y analizar SU contenido viral (para destilarlo y SUPERARLO — nunca
clonarlo). Mínimo útil: ~10-15 piezas, mezclando virales y flojas (el contraste ES el dato).

## Fase 2 — LA MATRIZ (desmenuzar el patrón)

Por cada pieza, extraer y tabular:
| Campo | Qué mirar |
|---|---|
| Hook (0-3s) | La frase/imagen exacta que frena el scroll — literal, palabra por palabra |
| Estructura | Problema→giro→prueba→CTA · lista · storytime · antes/después · reto · dato-shock |
| Tema/ángulo | De qué habla y desde qué ángulo (dolor, deseo, curiosidad, polémica) |
| Emoción | Qué dispara: sorpresa, identificación, indignación, aspiración, humor |
| Formato | Duración, ritmo de cortes, texto en pantalla, cara vs b-roll, audio |
| CTA | Qué pide y cuándo (comenta X, sígueme para, guarda esto) |
| Resultado | Métricas reales de la pieza (jamás inventadas) |

Con la tabla llena, producir la **MATRIZ**: qué se repite en los virales que NO está en los
flojos → 3-5 **patrones ganadores** (combinación hook+estructura+emoción+tema) y la lista de
**anti-patrones** (lo que consistentemente muere). Esa matriz se guarda en la carpeta del
proyecto del usuario y — si la marca tiene **brand-brain** — se registra ahí como aprendizaje
(anuncios-ganadores/cambios-recientes) para que TODO el ecosistema la use.

**Ejemplo de un renglón real de la tabla** (para que el primer uso no dependa de adivinar el
formato):
| Campo | Ejemplo |
|---|---|
| Hook (0-3s) | "Nadie te dice esto antes de comprar minoxidil" (texto en pantalla + cara a cámara) |
| Estructura | Dato-shock → prueba (antes/después) → CTA |
| Tema/ángulo | Dolor (miedo a hacerlo mal) + curiosidad |
| Emoción | Sorpresa + indignación ("me estaban ocultando esto") |
| Formato | 22s, corte cada 2-3s, texto grande, cara + b-roll de producto |
| CTA | "Comenta CAÍDA y te mando el link" |
| Resultado | 340K vistas / 28K likes / 190 comentarios (medido, no estimado) |

Patrón ganador que sale de ahí: **dato-shock + dolor + prueba visual**, que después alimenta un
guion en la Fase 3 con ese mismo patrón como origen declarado.

**Terminado de esta fase:** hay tabla completa para cada pieza analizada (mínimo 10-15, mezclando
virales y flojas), 3-5 patrones ganadores nombrados con evidencia (no una sola pieza sustentando
un patrón) y la lista de anti-patrones. Si el brand-brain de la marca existe, la matriz quedó
registrada ahí.

## Fase 3 — GENERAR (guiones nuevos con la fórmula)

- Cada guion nuevo nace de UN patrón ganador de la matriz + el tema del negocio.
- On-brand siempre: leer el brand-brain de la marca (voz, avatares, claims permitidos);
  el copy fino puede apoyarse en `golden-copywriting`.
- Formato de entrega por guion: HOOK exacto (primeras palabras) → guion segundo a segundo
  (hablado + texto en pantalla + plano) → CTA → patrón de origen.
- Entregar en lotes (ej. 5-10 guiones) cubriendo 2-3 patrones distintos — variedad de apuestas.
- Si no hay brand-brain de la marca, decide con lo que el usuario haya dado en la Fase 1 (voz,
  producto, país) e INFORMA que el on-brand quedó a nivel básico hasta que exista brand-brain —
  no te detengas a pedirlo si el usuario ya dio lo mínimo para producir.

**Ejemplo mínimo de un guion entregado** (mismo patrón del ejemplo de la Fase 2):
> **HOOK:** "Nadie te dice esto antes de comprar minoxidil"
> **Guion:** 0-3s cara a cámara, texto "ESTO TE LO OCULTAN" — 3-8s muestra el frasco, dato-shock
> del ingrediente — 8-18s antes/después del producto propio — 18-22s "Comenta CAÍDA y te mando
> el link"
> **CTA:** Comenta CAÍDA (remarketing directo)
> **Patrón de origen:** dato-shock + dolor + prueba visual (Fase 2)

**Terminado de esta fase:** cada guion entregado trae los 4 campos completos (hook, guion
segundo a segundo, CTA, patrón de origen) y el lote cubre al menos 2 patrones distintos.

## Fase 4 — PRE-CALIFICAR (simular antes de grabar)

Rúbrica de potencial (0-10 por criterio, promedio final):
1. **Gancho** — genera pregunta/tensión en 3 segundos sin el contexto del canal?
2. **Retención** — hay razón para quedarse (giro, lista, promesa de payoff al final)?
3. **Identificación** — el avatar del brand-brain diría "esto me pasa a mí"?
4. **Compartibilidad** — da estatus o utilidad compartirlo/guardarlo?
5. **Claridad del CTA** — se entiende qué hacer después?
Para VIDEO ya renderizado: si el conector de Higgsfield está activo, correr también su
predictor de viralidad (hook strength, retención) como segunda opinión.

**Honestidad obligatoria:** esto es predicción, no garantía — el algoritmo tiene humor propio.
Regla de la casa: **publicar todo igual** (el score solo ordena la prioridad de producción);
a veces el video que menos promete es el que explota. La matriz se re-alimenta cada 2-4
semanas con los resultados reales: lo que pegó entra, lo que murió se anota como anti-patrón.

**Terminado de esta fase:** cada guion del lote tiene los 5 criterios calificados y el promedio,
y el orden de prioridad de grabación quedó explícito (no implica descartar ninguno).

## Fase 5 — CALENDARIZAR (volumen + ritmo, del guion al plan)

Los guiones ganadores no sirven en un cajón: hay que **planificarlos como calendario editorial**.

1. **Objetivo de volumen:** definir con el usuario cuántas piezas/día o /semana (default sano
   para crecer: 1-3 al día si hay capacidad, mínimo 1 diaria de L a S; domingo opcional/descanso).
   Máxima autonomía: si no lo define, proponer un ritmo realista según el material disponible e
   INFORMAR.
2. **Mezcla por tipo (regla de reparto, no todo venta):** balancear la semana entre
   **Tráfico/alcance** (hook fuerte, tema amplio — engancha desconocidos), **Autoridad/valor**
   (enseña algo, genera confianza), **Conexión/comunidad** (historia, detrás de cámara, humano) y
   **Venta/conversión** (oferta directa, CTA de compra). Regla anti-quema: la venta NO domina el
   feed — la mayoría es tráfico+valor+conexión, la venta es la minoría que cierra.
3. **Asignar a la cuadrícula:** repartir los guiones del lote (Fase 3) en una tabla
   Lunes→Sábado × franjas, cada celda con: patrón de origen, tipo (tráfico/valor/conexión/venta),
   hook y estado (idea → guion → grabado → editado → publicado). Priorizar por el score de la
   Fase 4 (lo más prometedor primero), pero **publicar todo** igual.
4. **Salida:** el calendario se entrega como tabla en la carpeta del proyecto (y, si el usuario
   usa Notion, se puede volcar ahí como tablero). Cada 2-4 semanas se refresca con los resultados
   reales (misma re-alimentación de la Fase 4: lo que pegó marca el ritmo del siguiente ciclo).

Objetivo: que el usuario nunca se siente frente a "y hoy qué subo" — el plan ya está armado,
balanceado y priorizado por evidencia.

**Terminado de esta fase:** la cuadrícula L-S está llena con al menos una pieza/día, la mezcla de
tipos respeta la regla anti-quema (venta en minoría) y cada celda trae patrón, tipo, hook y
estado. Con esto la skill entrega su ciclo completo: de la evidencia bruta al calendario listo
para producir.

## Encadenado al ecosistema
- **Lee de:** brand-brain (voz/avatares) · métricas reales del usuario · creadores de referencia.
- **Entrega a:** `golden-ugc-avatar` (los guiones se vuelven videos con avatar) · `golden-ads`
  (un orgánico ganador es el mejor candidato a anuncio) · HyperFrames (edición/captions).
- **No pisa a:** `golden-copywriting` (copy de venta directa) ni `golden-ads` (pauta).

## Changelog
- **GMV1.6** (2026-08-21) — Auditoría `golden-skill-auditor`: (1) la etiqueta de versión decía
  GMV1.4 mientras este Changelog ya iba en GMV1.5 — la capacidad de transcripción local (Fase 1)
  ya estaba en el cuerpo pero la versión no lo reflejaba; sincronizado a GMV1.5→GMV1.6, un solo
  número en todo el archivo. (2) el description no mencionaba la Fase 5 CALENDARIZAR — agregado
  el trigger. (3) agregado un ejemplo entrada→salida de un renglón de matriz y de un guion
  (Fases 2 y 3) y criterio explícito de "terminado" por fase (2 a 5), para que el primer uso no
  dependa de inferir el formato. Blindaje: `chflags uchg` (mismo mecanismo de antes, re-aplicado
  al cierre).
- **GMV1.5** (2026-08-11) — **El TEXTO del video ya no depende de que el usuario lo pegue.** GMV1.4
  declaraba el guion pegado como "el único que hoy da el TEXTO del video"; eso dejó de ser cierto:
  el audio se transcribe en local con `whisper-cpp`, gratis, sin llave
  y sin que el archivo salga del Mac (medido: 7,5 min de audio en 29 s). Cambia el alcance real de
  la skill — antes, si el usuario no pegaba el guion, la pieza se analizaba solo por métricas y
  comentarios. La capacidad ya existía en el ecosistema desde `golden-video-editor`, pero **nunca
  se había propagado a las skills que la necesitaban**: ese fue el hueco, no la herramienta.
- **GMV1.4** (2026-08-02) — **Corregido un alcance que la skill daba por bueno: `yt-dlp` NO trae
  comentarios de TikTok.** GMV1.3 escribió "comentarios de YouTube/TikTok" habiendo probado solo
  YouTube. Medido hoy sobre un video real de TikTok: metadatos **sí** (título, canal, 49.400 vistas,
  986 likes) y **comentarios: 0**. Como esta skill vive de contenido de TikTok, la diferencia no es
  menor: ahora se usa el metadato para RANKEAR qué piezas estudiar, y el texto de los comentarios
  sale por Chrome MCP o pegado — **diciéndolo**, nunca presentando como minado lo que no se minó.
  + Reddit descartado como fuente (Firecrawl lo rechaza, el navegador lo bloquea por política).
  + **Regla Cero pasa de 3 a 4 modos** (nuevo: captcha, que inventa datos con el título poblado)
  y se apunta al **candado ejecutable** en vez de depender de recordar las verificaciones.
- **GMV1.3** (2026-08-01) — **`yt-dlp` instalado y probado: la ingesta de comentarios pasa de
  "pendiente-con-dueño" a operativa.** Medido: 30 comentarios con `author`, `text` y **`like_count`**
  de ~2.450.067 disponibles. El `like_count` es el hallazgo que sube el nivel de la skill: un
  comentario con miles de likes es un dolor o una objeción **validada por votación** de la
  audiencia, así que ordenarlos por likes da la jerarquía real de lo que importa — mejor materia
  prima para hooks que cualquier lluvia de ideas. Receta exacta en la Fase 1 (con `comment_sort=top`
  y `max_comments`, obligatorios o intenta bajar millones).
  🚨 Regla Cero ampliada a **3 modos de fallo**: el check de `metadata.title` solo cazaba la
  alucinación total; Temu falla con title poblado (señuelo: devolvió 72 categorías de ropa) y
  Amazon con title poblado y sin redirección (muro anti-bot, sin campo `json`). Se añade la
  verificación que caza los tres: **"el dato responde a lo que pedí?"**.
- **GMV1.2** (2026-07-31) — **Fase 1 INGESTA reescrita: la skill ya no depende de que le peguen
  todo a mano.** Pedía un conector de scraping que no existe (Apify, "pendiente-con-dueño") mientras
  **Firecrawl ya estaba instalado y activo** — la skill se estaba autolimitando por información
  vencida. Probado en vivo el 2026-07-31: `firecrawl_scrape` con `formats:["json"]` +
  `proxy:"stealth"` sobre una URL de YouTube devuelve **título, canal, vistas y likes exactos**
  (1.798.929.737 vistas / 19.293.598 likes verificados) gracias a un postprocesador nativo de
  YouTube. Ahora el paso 1 es automático y solo se pide a mano lo que ninguna vía saca.
  Límites medidos y escritos, no supuestos: **NO trae comentarios** (`comentarios: []`, con y sin
  scroll) y **`json` + `actions` se cae por timeout** (2 de 2). Para comentarios se ordenan 3 vías
  (`yt-dlp` ⚠️ no instalado → Chrome MCP → pegado). Saves/shares/retención siguen siendo pantallazo:
  solo existen en el panel del creador.
  🚨 **Regla Cero enlazada a la regla "métricas reales, jamás inventadas" de la Fase 2:** si
  `metadata.title` viene vacío, el `json` es **alucinado** (medido: inventó un producto entero con
  precio y reseñas falsos). Una métrica falsa en la matriz contamina todos los guiones que salgan
  de ella. 📖 `golden-investigacion-mercado/references/scraping-firecrawl.md`.
- **GMV1.1** (2026-07-12) — + Fase 5 CALENDARIZAR: calendario editorial (objetivo de volumen,
  mezcla por tipo tráfico/valor/conexión/venta, cuadrícula L-S con estado y prioridad por score,
  salida a carpeta/Notion). Destilado de una referencia externa de "sistema de contenido", sin
  clonar ni nombrar la fuente.
- **GMV1.0** (2026-07-11) — Creación: ingesta flexible (pegado/links/scraper opcional),
  matriz de patrones vs anti-patrones, generación on-brand por patrón, rúbrica de 5 criterios
  + predictor externo opcional, y re-alimentación quincenal con resultados reales.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección **AUTO-MEJORA** (mandato global de FER, autorización permanente). Sin esta sección la skill no se auto-calificaba al cerrar corrida. Contenido operativo intacto. Backup: `_backups/2026-08-02-loop-arsenal-s1/`.
