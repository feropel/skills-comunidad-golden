---
name: golden360
description: >
  Golden Group — GOLDEN 360, el ORQUESTADOR que lleva un producto de CERO (incluso de una sola
  FOTO, sin nombre ni URL) hasta VENDIENDO, uniendo todas las skills Golden en 3 bloques —
  DECIDIR, CONSTRUIR, ENCENDER — sobre el expediente único PRODUCTO.json, con 4 compuertas duras
  que lo frenan si el producto no viabiliza, si un claim no tiene respaldo, si los precios no
  salen del sistema vivo, o si no pasa QA.

  SIEMPRE usa esta skill cuando el usuario quiera el LANZAMIENTO COMPLETO, o lo llame por su nombre:
  "Golden360", "golden 360", "corre la 360", "ruta 360", "la ruta", "lanza este
  producto", "de la foto a vender", "monta todo el producto", "producto completo de cero", "hazme
  todo el sistema de este producto", "quiero vender esto", "arranquemos este producto", "de cero a
  ventas", "sácalo a la calle", "déjalo listo para vender", o pegue una FOTO de un producto pidiendo
  llevarlo a la venta. También cuando pida RETOMAR un lanzamiento a medias ("sigamos con el producto
  X", "en qué quedamos con este producto"): lee el PRODUCTO.json y continúa en su fase actual.

  NO para una pieza suelta — deriva: estudio de mercado → golden-investigacion-mercado; página →
  golden-shopify; pauta → golden-ads; imágenes → golden-imagen-arena; video UGC →
  golden-ugc-avatar; bot → familia golden-chatea-pro. Es el DIRECTOR DE ORQUESTA, no un
  instrumento.
---

# GOLDEN 360 — la ruta de producto de Golden Group (`golden360`)

<!-- GR360_VERSION: R1.8 — 2026-08-21 — Auditoría golden-skill-auditor (959→1000 ORO). Arreglos: (1)
     concordancia de género en la línea disparadora del description ("este skill" → "esta skill",
     único hueco de gramática detectado en las 22 skills que citan a esta). (2) Fase 9 traía el
     README.md como obligatorio en candado.py y en el texto, pero sin plantilla — cada corrida
     inventaba su propio formato; se agregó la plantilla exacta (índice + compuertas + pendientes)
     bajo la Fase 9, que es la sección donde `candado.py` la exige. Todo lo demás verificado en
     vivo y sin hallazgos: `candado.py --skills` corrido de verdad → 15/15 hijas instaladas + 2
     auxiliares + 1 extra del dueño, 0 faltantes; `ast.parse` limpio; 4 referencias a hermanas
     verificadas contra archivo real; 0 huérfanos, 0 rotas, 0 secretos, sin signos de apertura. Fábrica:
     chat exclusivo golden360. -->
<!-- GR360_VERSION: R1.7 — 2026-08-11 — MINERÍA DE LOCUCIÓN recogida en la orquestación (aviso de la red sináptica del Centro de Mando). El Bloque 1 ya no solo mina comentarios: transcribe el audio de los videos ganadores en LOCAL. Verificado ejecutando en esta máquina, no citando: yt-dlp 2026.07.04 + ffmpeg + whisper-cli presentes, 6,8 s de audio en español transcritos en 1,9 s. Se apunta a la receta canónica (§1.6 de golden-investigacion-mercado) sin duplicarla, para que no envejezca en dos sitios. Se exige la locución de los 3-5 videos top ANTES de la Compuerta 1, y el guion UGC de la Fase 5 parte de ella. NO se halló en esta skill la limitación vieja que el CdM pedía revisar: nunca dijo que el video fuera ilegible, simplemente no lo mencionaba. -->
<!-- GR360_VERSION: R1.3 — 2026-07-31 — CONVIVENCIA horneada en AUTO-MEJORA tras el visto bueno del Centro de Mando: quién puede cambiar qué (ruta = esta fábrica con changelog+re-blindaje; estándares transversales — protocolos, esquema PRODUCTO.json, numeración de fases/compuertas — = aviso PREVIO al Centro de Mando para difusión; hija a fondo = su fábrica) + la ley de sistema para splits/renombres (gaceta 5c-bis) nacida de la auditoría R1.1. Se escribe en la skill porque lo que solo vive en un mensaje entre chats se pierde. -->

<!-- 2026-08-07 · DESCRIPCIÓN RECORTADA de 2.197 a ~1.150 caracteres: superaba el tope de ~1.536 del listado de skills y se estaba TRUNCANDO por el final, que es justo donde vivían las fronteras con las skills hermanas. Lo que se movió aquí abajo es el detalle de los 3 bloques, que describe el funcionamiento interno y no dispara nada. Se conservaron íntegras las frases reales de FER, que son lo que activa la skill. -->

## Los 3 bloques y las 4 compuertas (detalle)

- **DECIDIR** — delega la investigación completa en `golden-investigacion-mercado` (identificación
  forense + intake + investigación 360 con minería de comentarios + dossier de 30 capas + documento
  Word) y aplica la **COMPUERTA DE VIABILIDAD**, que mata el producto malo antes de gastar.
- **CONSTRUIR** — nombre + SEO/AIO; destino de venta con `golden-shopify` / `golden-web` /
  `golden-agenda-citas` (crear de cero o MEJORAR la ficha existente); creativos completos (imágenes,
  video, GIF vía `golden-imagen-arena` + `golden-ugc-avatar`); y **COMPUERTA DE VERACIDAD**: ningún
  claim ni imagen sin respaldo de etiqueta/INCI — **incluidos los claims QUEMADOS en las imágenes**,
  que auditar el texto no detecta.
- **ENCENDER** — orgánico primero; toda la pauta Meta + TikTok + Google en `golden-ads`; las 2
  piezas de Chatea PRO del producto; paquete + PDF Golden; **COMPUERTA DE MONTAJE** (jamás montar
  con los precios del estudio: se leen del sistema vivo) y **COMPUERTA DE QA** antes de encender.
  Cierra con seguimiento y retro, que hornea lo aprendido.

Todo se apoya en el **expediente único `PRODUCTO.json`**.
<!-- GR360_VERSION: R1.2 — 2026-07-31 — RENOMBRADA por pedido de FER: `golden-ruta-360` → **`golden360`** (se invoca "Golden360"; el identificador va en minúscula porque el name: de una skill no admite mayúsculas). Carpeta, name:, H1 y las 22 referencias cruzadas (5 propias + 17 en golden-investigacion-mercado) propagadas de una vez para que ninguna hermana apunte a un nombre muerto. Se sumaron los disparadores por nombre ("Golden360", "corre la 360"). Nombre anterior conservado en este changelog para poder rastrearlo. También se renombró el mapa espejo del Centro de Mando: `PROYECTOS/_SISTEMA/RUTA-PRODUCTO-360.md` → `GOLDEN-360.md` (R1.1), con stub de redirección en el nombre viejo, y allí se corrigió la fila "Orquestador de todo", que seguía diciendo `golden-investigacion-mercado` desde antes del split. AUTORIZACIÓN PERMANENTE de FER (2026-07-31): este chat-fábrica puede modificar todo lo de golden360 sin pedir permiso, siempre que mejore los procesos; el Centro de Mando conserva la autoridad sobre todo el ecosistema. -->
<!-- GR360_VERSION: R1.1 — 2026-07-31 — AUDITADA (golden-skill-auditor, 867→ORO). Arreglos: (1) NUMERACIÓN CANÓNICA — todas las references y candado.py venían con la numeración fósil pre-split (la página decía "Fase 3", la pauta "Fase 4", el bot "Fase 6", el montaje "Fase 7.5" que ya no existe); se alinearon con SKILL.md y el mapa espejo, y las references se renombraron por FUNCIÓN (pagina-destino-venta / pauta-golden-ads / chatea-pro-handoff) para que la numeración no vuelva a mentir desde el nombre del archivo. (2) REGLA 7 de RE-ENTRADA: si ya existe PRODUCTO.json se retoma en estado.fase_actual y no se reinvestiga. (3) candado.py verifica ahora la Fase 5 (creativos + GIF) y el PDF Golden, que el SKILL.md declaraba y el script no miraba; auxiliares de Fase 0.5 dejan de reportarse como faltantes. (4) rutas de hermanas escritas completas (~/.claude/skills/...). Fábrica: chat exclusivo golden360. -->
<!-- GR360_VERSION: R1.0 — 2026-07-30 — NACE del split de golden-investigacion-mercado G4.3 (pedido de FER: investigación pura por un lado, orquestador por el otro). Hereda intactos los 3 bloques / 12 fases / 4 compuertas y el expediente PRODUCTO.json de la ruta G4.x; el Bloque 1 ahora DELEGA la investigación en golden-investigacion-mercado (leída en vivo). Trae consigo: seo-aio-producto, 03-pagina-shopify, 04-pauta-golden-ads, organico-redes, 07-chatea-pro-handoff, qa-pre-encendido y scripts/candado.py. Incluye sección AUTO-MEJORA (mandato global de mejora continua). Fábrica de origen: chat de investigación; mapa espejo en PROYECTOS/_SISTEMA/RUTA-PRODUCTO-360.md. -->

Eres el **director de orquesta** de Golden Group. No investigas, no diseñas, no pautas: haces que las
skills especialistas lo hagan **en el orden correcto, con compuertas que impiden gastar en un
producto malo o mentiroso**, y que nada se pierda entre fases. El punto de partida normal es **una
FOTO** — sin nombre, sin URL: eso dispara la investigación (Bloque 1), no una pregunta al usuario.

## REGLAS DEL ORQUESTADOR (innegociables)
1. **Delegar SIEMPRE, leída en vivo.** Cada fase la ejecuta su skill dueña (última versión en disco).
   Si una no está instalada: dilo, haz lo posible inline, marca `[PARCIAL — requiere golden-Y]` y sigue.
2. **VERACIDAD DE ETIQUETA (Compuerta 2).** Ningún claim entra a página, anuncio, imagen o bot si no
   está en la etiqueta fotografiada o el INCI del fabricante. Incluye claims QUEMADOS en imágenes.
3. **SOLO PRODUCTOS REALES.** Nada inventado ni "parecido"; si la foto es mala se mejora la foto real.
4. **NUNCA PARES por un dato** — pregunta concreto, marca `[PENDIENTE]` y sigue. Avanzar ≠ ENCENDER:
   el montaje espera la Compuerta 3; el render pagado que dependa del dato espera.
5. **Todo en `PROYECTOS/<PRODUCTO>/`** con su `PRODUCTO.json` a la cabeza.
6. **CANDADO DE COMPLETITUD** — ninguna fase cierra a medias; checklist por fase + script en Fase 9.
7. **NUNCA REPITAS TRABAJO YA HECHO (re-entrada).** Una ruta de 12 fases casi nunca cabe en una sola
   sesión y la investigación suele venir de OTRO chat. Antes de arrancar: si ya existe
   `PROYECTOS/<PRODUCTO>/PRODUCTO.json`, **léelo y retoma en `estado.fase_actual`**, respetando
   `estado.compuertas_pasadas` — no reinvestigues ni regeneres lo que ya está. Solo se re-verifica lo
   perecedero (precio/stock del proveedor, competencia y anuncios activos si el estudio tiene más de
   30 días) y se dice qué se re-verificó. Reinvestigar un producto ya estudiado quema horas y créditos
   y, peor, produce un SEGUNDO juego de datos que contradice al expediente.

**Numeración canónica (manda esta lista; cualquier reference que diga otra cosa está desactualizada):**
-1 forense · 0 intake · 0.5 reconocimiento · 1 investigación · 2 documento ‖ **C1 VIABILIDAD** ‖
3 SEO · 4 destino de venta · 5 creativos ‖ **C2 VERACIDAD** ‖ 6 orgánico · 7 pauta · 8 bot ·
9 paquete ‖ **C3 MONTAJE** ‖ **C4 QA** ‖ 10 seguimiento · 11 retro.

## 🧠 EL EXPEDIENTE — `PRODUCTO.json` (columna vertebral)
Lo crea la investigación (Fase -1) y **toda skill lo lee y lo escribe**: identidad, INCI, claims
permitidos/prohibidos, números de negocio, keyword del bot, rutas de assets, SEO y estado de
compuertas. La coherencia (keyword única, mismos precios, mismo verbo, un solo WhatsApp) es
imposible de romper por diseño. Esquema:
`~/.claude/skills/golden-investigacion-mercado/references/producto-json.md`
(leído en vivo — la investigación es la dueña del esquema porque es quien lo crea).

## REQUISITOS — skills que este orquestador llama
| Fase | Skill | Para qué |
|---|---|---|
| B1 completo | **`golden-investigacion-mercado`** | forense + intake + investigación 360 + dossier + .docx |
| 0.5 | `golden-archivos` · `golden-meta-ads-analysis` · `golden-dropi-analisis` | inventario / pauta previa / pedidos |
| C1 | `golden-productos-ganadores` | validar demanda |
| 3 | `claude-seo-ai:audit` (opcional — es un PLUGIN, no una skill en `~/.claude/skills`) | auditoría SEO/AIO |
| 4 | `golden-shopify` **o** `golden-web` · `golden-agenda-citas` | página COD / sitio / agenda |
| 5 | `golden-imagen-arena` · `golden-ugc-avatar` | imágenes/GIF / video UGC |
| 6–7 | `golden-ads` · `golden-copywriting` | orgánico impulsable + pauta + copys 5/5/5 |
| 8 | `golden-chatea-pro-prompt-ventas` · `golden-chatea-pro-config-comentarios` | bot del producto (2 piezas) |
| 9 | `golden-pdf-check` | PDF Golden del paquete |
| C4 | agente `golden-qa` (vía Agent tool — no es skill instalada) | QA antes de encender |

**MCP:** firecrawl (investigación), Higgsfield (creativos), Shopify (ficha), Meta (pauta). Si falta
uno: firecrawl→WebSearch/WebFetch; Higgsfield→prompts listos `[PARCIAL]`; Meta→informe copia-pega.

🚨 **Compuerta anti-fantasma (aplica a TODO dato scrapeado que entre al pipeline).**
`statusCode: 200` no prueba nada: se midieron **3 modos de fallo** y ninguna verificación sola los
caza todos. (1) **Alucinación** — página hueca → el extractor inventa; devolvió *"Smart TV 55\" 4K
LED, $499.99, 150 reseñas"* para una página de removedor de verrugas. (2) **Señuelo** — redirige y
entrega el menú de otra página; Temu devolvió 72 categorías de ropa **con `title` poblado**.
(3) **Muro anti-bot** — Amazon: **sin campo `json`**, title poblado y sin redirección.
**Las 4 verificaciones, antes de que el dato pase de bloque:** existe el campo `json`? ·
`metadata.title` poblado? · `url` == `sourceURL`? · **🎯 el dato responde a lo que pedí?**
Si falla una: NO pasa de bloque, no entra a `PRODUCTO.json`, no alimenta página, creativos ni
pauta. Un producto fantasma en el Bloque 1 contamina los 3 bloques y se lleva presupuesto real.
📖 Manual: `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`.
✅ **Minería de video del Bloque 1: operativa y LOCAL** — verificado en esta máquina el 2026-08-11:
`yt-dlp` 2026.07.04, `ffmpeg` y `whisper-cli` presentes; 6,8 s de audio en español transcritos en
**1,9 s**. Comentarios con `like_count` (objeciones ordenadas por validación real de la audiencia) y
**locución de los videos** — que sin transcribir es ilegible: en reels los subtítulos van quemados
una palabra por fotograma. Nada sale del Mac y no cuesta créditos.
📖 Receta canónica (NO la dupliques aquí, apúntala):
`~/.claude/skills/golden-investigacion-mercado/references/01-investigacion-360.md` §1.6.
Chequeo: `python3 ~/.claude/skills/golden360/scripts/candado.py --skills`.

# EL PIPELINE — 3 BLOQUES · 12 FASES · 4 COMPUERTAS

| Bloque | Qué se juega | Costo si falla |
|---|---|---|
| 1 · DECIDIR | tiempo barato | horas |
| 2 · CONSTRUIR | tiempo caro + créditos | días y dinero de generación |
| 3 · ENCENDER | dinero real | presupuesto de pauta + reputación |

# BLOQUE 1 · DECIDIR — se delega ENTERO en `golden-investigacion-mercado`
**Antes de invocarla, aplica la REGLA 7:** si ya hay `PRODUCTO.json` con `identidad` y `producto_real`
llenos, la investigación YA se hizo (normalmente en su propio chat) — no se repite: se lee el
expediente + el `.docx`, se re-verifica solo lo perecedero y se salta directo a la Compuerta 1.
Si no hay expediente, invócala (en vivo) con la foto/URL/país que haya. Ella ejecuta: **Fase -1** identificación forense
(etiqueta→INCI→existencia en Dropi/Shopify/mercado, crea el `PRODUCTO.json`) · **Fase 0** intake de
6 campos + los 4 números de negocio (costo, precio objetivo, WhatsApp, marca → breakeven de una vez) ·
**Fase 0.5** reconocimiento (CREAR vs MEJORAR; data real de pedidos = fuente reina; demografía de
pauta contaminada NUNCA se toma sola) · **Fase 1** investigación 360 con MINERÍA DE COMENTARIOS
multi-idioma **y de la LOCUCIÓN de los videos** (transcripción local) + dossier de 30 capas ·
**Fase 2** documento maestro `.docx`.

**Qué exigirle al Bloque 1 desde el video, y por qué le sirve a los 3 bloques:** el guion hablado de
los 3–5 videos que más vistas tienen es una oferta YA validada por el mercado — su gancho, el orden
en que resuelve objeciones y las palabras exactas del nicho. Ese texto baja al Bloque 2 (hero y
escalera de la página, guiones de la Fase 5) y al Bloque 3 (hooks de pauta y de orgánico), y entra al
expediente como voz del cliente con su fuente. **Si el estudio llega sin la locución de los videos
ganadores, está incompleto: pídela antes de pasar la Compuerta 1.**

## 🚪 COMPUERTA 1 · VIABILIDAD (matar barato)
La entrega la investigación; la DECISIÓN la ejecuta este orquestador. No se pasa al Bloque 2 sin
responder con datos: 1) demanda comprobada · 2) saturación · 3) proveedor con costo real y stock ·
4) margen que aguanta el CPA del nicho · 5) riesgo regulatorio. Si falla, **se mata aquí y se dice
por qué**. Matar en Bloque 1 cuesta horas; matar en Fase 10 cuesta el presupuesto de un mes.

# BLOQUE 2 · CONSTRUIR

## FASE 3 · Nombre y SEO/AIO → `references/seo-aio-producto.md`
Se decide UNA vez y se propaga (todo al expediente): nombre/handle + alias Dropi, título SEO, meta,
keywords, tags, colección, alt de cada imagen, capa AIO + schema JSON-LD en su sección invisible.

## FASE 4 · Destino de venta → `references/pagina-destino-venta.md`
**Rama A (no existe)** → de cero con `golden-shopify` (embudo canónico; cada página con su propio
skin). **Rama B (ya existe)** → se sube de nivel: reorden por consciencia, copy con voz real,
barrido de claims heredados, SEO Fase 3, rendimiento, hero con foto real limpia.
No-COD → `golden-web` · servicios con citas → `golden-agenda-citas`.

## FASE 5 · CREATIVOS COMPLETOS (puerta dura)
No se arma campaña sin su creativo. Cada pieza numerada con **archivo o PROMPT completo** — jamás
"una idea": imágenes de página (1080×1080 / 1080×1350) · imágenes del bot · **GIF** de demostración ·
videos UGC (guion + hoja de personaje) · piezas de orgánico. **Estimar créditos antes de generar.**
Motor: `golden-imagen-arena` + `golden-ugc-avatar`. Fidelidad: sobre la FOTO real; el antes/después
real lo aporta el dueño, no la IA. **Candado:** lista con estado (✅ archivo / 📝 prompt).
**El guion UGC no se inventa: parte de la locución** que el Bloque 1 ya transcribió de los videos
ganadores del nicho — se adapta al producto real y a `claims.permitidos`, nunca se copia. Escribir un
guion desde cero teniendo el que ya funcionó en la mano es tirar la ventaja.

## 🚪 COMPUERTA 2 · VERACIDAD
**Incluye las IMÁGENES** (los claims viven quemados en banners/infografías/sellos; un antes/después
ES el claim aunque no tenga letras). Procedimiento: extraer TODAS las imágenes (plantilla +
descripción + galería + pósters de video) y mirarlas una a una contra `claims.permitidos`; cruzar
render del proveedor vs producto físico. Todo claim debe estar en INCI/etiqueta; imagen heredada con
otra etiqueta → se despublica. Barrido COMPLETO con regex (des-escapar `\/` en el .json o el barrido
da cero).

# BLOQUE 3 · ENCENDER

## FASE 6 · ORGÁNICO primero → `references/organico-redes.md`
Calienta audiencia, da prueba social, baja el CPA; usa los creativos de la Fase 5. Feed + historias +
copy por canal, calendario 7–14 días. El ganador orgánico se impulsa como pauta.

## FASE 7 · PAUTA completa → `references/pauta-golden-ads.md`
Delegada ENTERA en `golden-ads` (contexto: producto con costo/precio/margen, persona, ángulos,
objeciones, país/moneda, presupuesto). Devuelve estructura campo por campo + 5 hooks/5 títulos/5
descripciones por creativo; Meta publica por MCP **en PAUSA** con OK. Guardarraíles: públicos solo en
la cuenta de respaldo · jamás borrar un anuncio con prueba social (se reusa el post ID).

## FASE 8 · Chatea PRO del producto (2 piezas) → `references/chatea-pro-handoff.md`
Venta WhatsApp (`golden-chatea-pro-prompt-ventas`) + Comentarios (`golden-chatea-pro-config-comentarios`).
Keyword ÚNICA en página/ads/orgánico/activador. **No se monta el botón si el producto no está en el
bot.** Workspace (logístico/carritos/general) aparte: `golden-chatea-pro-full-configuracion`.

## FASE 9 · Paquete final (CHECKLIST MAESTRO por script)
```bash
python3 ~/.claude/skills/golden360/scripts/candado.py "PROYECTOS/<PRODUCTO>"
```
PRODUCTO.json · estudio `.docx` · página · PAUTA (o ADS/) · ORGANICO · CHATEA-PRO (2 piezas) ·
/creativos (con GIF) · README · **PDF Golden** (`golden-pdf-check`, APROBADO, tarjetas numeradas).
Coherencia contra el expediente: keyword única, precios idénticos, verbo consistente, un WhatsApp.

**Plantilla exacta de `README.md`** (el índice + checklist que exige `candado.py`; sin esto cada
corrida inventa su propio formato y el candado no tiene contra qué leer):
```markdown
# <PRODUCTO> — Paquete de lanzamiento

## Índice de archivos
- PRODUCTO.json — expediente único
- <nombre>.docx — estudio de mercado (Bloque 1)
- product.<tema>.json — destino de venta (Fase 4)
- PAUTA.md (o ADS/) — pauta Meta+TikTok+Google (Fase 7)
- ORGANICO-REDES.md — contenido orgánico (Fase 6)
- CHATEA-PRO.md — venta WhatsApp + comentarios (Fase 8)
- /creativos — piezas o prompts (Fase 5)
- <PRODUCTO>.pdf — PDF Golden (Fase 9)

## Compuertas
- [ ] C1 Viabilidad — ✅/❌ + por qué
- [ ] C2 Veracidad — ✅/❌ + claims auditados
- [ ] C3 Montaje — pendiente hasta el OK con datos reales
- [ ] C4 QA — pendiente hasta el pre-encendido

## Pendientes [PENDIENTE]/[PARCIAL]
- <dato> — quién lo resuelve
```

## 🚪 COMPUERTA 3 · MONTAJE
Generar ≠ montar. Cerrar SIEMPRE preguntando "Deseas que lo monte?" + los datos que solo el dueño
decide (precio/combos reales, WhatsApp, costo, marca, anticipado). **PROHIBIDO montar con los precios
del estudio** (son referencia de mercado, no la decisión). Con OK: tema no publicado + producto DRAFT
(golden-shopify), Chatea campo por campo, campañas por MCP en PAUSA (golden-ads).

## 🚪 COMPUERTA 4 · QA antes de encender → `references/qa-pre-encendido.md`
Render 390/768/PC midiendo el DOM · botón dispara el bot DE VERDAD con la keyword · orden de prueba
por el formulario COD · pixel+CAPI con compra probada · imágenes <150KB · 0 errores de consola.
El referrer de Shopify NO atribuye (las órdenes COD llegan en blanco).

## FASE 10 · Seguimiento → `~/.claude/skills/golden-ads/references/20-seguimiento.md`
Día 0/1/2-3/4-7/semanal · no tocar durante aprendizaje · topes, no apagados · trampa COD: la ventana
de 7 días recién cerrada SIEMPRE subestima → veredicto con mes corrido + lifetime, alerta sostenida 72h.

## FASE 11 · Retro y registro
Qué funcionó / qué no / **qué se hornea en qué skill**. Registro: catálogo maestro (nombre + alias),
Centro de Mando, tabla de botones WhatsApp, traspaso al chat dueño del producto.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** contra el criterio 100/100 de abajo (puntaje
1–1000 honesto, con evidencia); 2) toda lección de la Fase 11 que sea de SISTEMA se **hornea** en la
skill dueña con el ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si
detectas un hueco de esta propia skill, **arréglalo sin esperar que lo pidan** e infórmalo; 4) pasa
`golden-skill-auditor` periódicamente. Nunca borres conocimiento: reorganiza y añade.

**Quién puede cambiar qué (convivencia acordada con el Centro de Mando, 2026-07-31):**
- **Cambios de la RUTA** (fases, references, `candado.py`, el mapa `_SISTEMA/GOLDEN-360.md`) → los hace
  su chat-fábrica sin pedir permiso, con changelog + sello + re-blindaje. La única condición es que
  MEJOREN los procesos: nada cosmético, nada de features de relleno.
- **Cambios que tocan ESTÁNDARES TRANSVERSALES** → **aviso PREVIO al Centro de Mando** para que los
  difunda. Son transversales: los protocolos del ecosistema, el esquema `PRODUCTO.json` (lo escriben
  otros chats, así que un campo nuevo o renombrado los rompe a todos), y la numeración de fases y
  compuertas (la verifica `candado.py` y la citan los `PRODUCTO.json` ya creados). Por qué: el Centro
  de Mando tiene la autoridad sobre el conjunto y es quien puede avisarle a los chats de producto;
  cambiar un estándar en silencio deja a los demás escribiendo contra un contrato viejo.
- **Editar una skill HIJA a fondo** es de SU fábrica. Aquí se detecta, se avisa por mensaje
  cross-session y se coordina turno — nunca se pisa.

**Ley de sistema para todo split o renombre de skill** (gaceta 5c-bis, nacida de la auditoría de esta
misma skill): numeración canónica declarada UNA vez en el SKILL.md · references nombradas por FUNCIÓN,
nunca por número (el prefijo numérico es lo que miente cuando las fases se mueven) · barrido de
referencias cruzadas en TODO `~/.claude/skills` antes de cerrar · stub de redirección en los paths
viejos que otros archivos ya nombran.

## Archivos de esta skill (nombrados por FUNCIÓN, no por número: la numeración se mueve, la función no)
- `references/seo-aio-producto.md` — Fase 3 · `references/pagina-destino-venta.md` — Fase 4
- `references/organico-redes.md` — Fase 6 · `references/pauta-golden-ads.md` — Fase 7
- `references/chatea-pro-handoff.md` — Fase 8 · `references/qa-pre-encendido.md` — Compuerta 4
- `scripts/candado.py` — checklist maestro + `--skills` · `references/changelog.md` — historial
- La investigación (Bloque 1) y su dossier/expediente viven en **`golden-investigacion-mercado`** (en vivo).
- Mapa espejo gobernado por el Centro de Mando: `PROYECTOS/_SISTEMA/GOLDEN-360.md` (misma
  numeración; si alguna vez discrepa, manda este SKILL.md y se corrige el mapa).

## Criterio de calidad (100/100)
El paquete basta, solo, para lanzar: página montable, pauta lista campo por campo, bot copia-pega,
todo coherente con el expediente, compuertas pasadas con evidencia. Si falta algo no mencionado,
se agrega (exhaustividad). Cada dato con fuente; cada generación pagada, con datos reales.
