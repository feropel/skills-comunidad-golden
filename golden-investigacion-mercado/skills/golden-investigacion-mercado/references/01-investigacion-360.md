# Fase 1 — Investigación exhaustiva (qué buscar y dónde)

Ejecuta en paralelo donde se pueda. Cada hallazgo se guarda **con su fuente** (REGLA 1). Herramientas:
`firecrawl` (search/scrape/extract), Meta Ad Library, TikTok Creative Center, Google Maps/Business.

## 1.1 El negocio / la marca
- Propuesta de valor (headline héroe), tono y lenguaje, productos y **precios visibles**.
- CTAs, prueba social en el sitio, garantías, política de envío/devolución.
- Modelo de venta (COD / pago anticipado / mixto) y país(es). Canales activos.

## 1.2 El producto (a fondo)
- Qué es, qué problema resuelve, cómo funciona (mecanismo), ingredientes/specs/materiales.
- Beneficios → traducidos a **resultados emocionales**. Casos de uso. Diferenciales reales.
- Specs duras (mAh, medidas, voltaje, tallas): **confirmar con el dueño**, no inventar.
- Restricciones/claims sensibles (salud, INVIMA, certificaciones) → marcar para compliance.

## 1.3 Mercado y demanda
- Tamaño/tendencia (Google Trends, volumen de búsqueda). Estacionalidad.
- Está validado como ganador? Cruza con `golden-productos-ganadores` (Ad Library + TikTok).
- Nivel de saturación del nicho (cuántos anunciantes activos, hace cuánto).

## 1.4 Competidores (3–7)
Para cada uno: nombre + URL · propuesta de valor · **precio** · oferta/promo · diferencial ·
ángulo de marketing · qué hace bien · **hueco que deja** (oportunidad). Tabla comparativa.
- Revisa sus anuncios activos (Ad Library) y su contenido orgánico.

## 1.5 Voz del cliente (oro para el copy)
- **Google Maps/Business**: reseñas — top elogios y top quejas, **citas textuales** con fuente.
- **Amazon / marketplaces** (si aplica): reseñas 1–2★ (decepciones) y 4–5★ (lo que enamora).
- **Redes y foros**: comentarios, preguntas frecuentes, objeciones repetidas, jerga del cliente.
- Extrae: las **palabras exactas** del cliente (dolor y deseo) → son el mejor copy publicitario.

### Regla: SIN reseñas locales verificables (caso Chile, 2026-08-07)
Cuando en el país destino no hay UNA sola reseña verificable (las "707" o "+9.999" del propio
vendedor NO cuentan), lo que sí sirve: las reseñas del **mismo producto/formato en Amazon**,
**citando el ASIN** e **incluyendo las de 1 estrella**, más el bloque *"Customers say"* que Amazon
genera. Se usan **rotuladas como reseñas internacionales del producto, jamás presentadas como
reseñas locales**. Las de 1 estrella son las que enseñan qué expectativa hay que administrar
antes de despachar.

## 1.5.bis Data real de pedidos / CRM (la fuente reina CUANDO existe, que es lo raro)
> **Lo NORMAL es que el producto sea NUEVO y NO haya ninguna métrica ni data de pedidos** → se investiga
> desde cero (esta Fase estándar) y la pauta va en **Modo B (testeo)**. La data de pedidos/CRM de abajo
> aplica **SOLO en la EXCEPCIÓN**: producto que ya se vendió o que se relanza a otro país. **No pidas
> métricas como si siempre fueran a existir**; si no hay, se avanza sin frenar (todo queda `(estimado)`,
> REGLA 5). Cuando SÍ exista, es la fuente reina y manda sobre cualquier inferencia.

Antes de estimar demografía o mezcla de producto, **pregunta si el dueño tiene DATA REAL de pedidos/CRM**:
export de Dropi (órdenes COD), base de Chatea PRO, hoja de ventas, pixel/CRM. Si la hay, **manda sobre
cualquier inferencia y sobre las impresiones de pauta**: úsala para validar con hechos —
- **Demografía real** (quién compra de verdad: género, edad aproximada, ciudad/depto de entrega).
- **Mezcla de producto** (qué SKU/variante vende más) y **combo attach** (qué se compra junto).
- **Geo** (dónde entrega mejor, dónde se devuelve) — cruza con `golden-dropi-analisis` si aplica.
- **Trampa a evitar — demografía de pauta CONTAMINADA:** la demografía que muestra una cuenta de anuncios
  YA está sesgada por la segmentación que se aplicó (efecto *self-fulfilling*): si solo se pauteó el creativo
  femenino, la cuenta dirá "90% mujeres" aunque los **pedidos reales** sean 50/50. **Nunca tomes la
  demografía de pauta como "quién compra" sin cruzarla con los pedidos reales.** (Caso real: una línea que
  vendía mitad y mitad según Dropi aparecía como 90% mujeres en Ads Manager, solo porque no se había
  pauteado el creativo masculino.) Sin data de pedidos → márcalo `(estimado)` y dilo explícito (REGLA 5).

## 1.6 MINERÍA DE COMENTARIOS — YouTube + TikTok + todas las redes (multi-idioma)
Los comentarios son la voz del cliente SIN filtro: ahí está lo que la gente necesita, de qué se
queja, lo bueno y lo malo — antes de que ningún vendedor lo edite. Se buscan del producto **exacto
Y de similares/categoría**, en **cualquier idioma** (mínimo: idioma del país destino + inglés +
portugués + el idioma del mercado de origen del producto, ej. reviews en inglés de AliExpress).
Las citas en otro idioma se traducen y se marcan *(traducida)*.

### YouTube (el archivo de objeciones más profundo)
- Busca videos del producto exacto y similares: `"<producto>" review`, `"<producto>" funciona`,
  `"<producto>" antes y después`, `"<producto>" X meses después`, unboxing, tutorial, "no compres".
- De los VIDEOS: cuáles tienen más vistas (esos títulos = **hooks ya probados por el mercado**),
  qué ángulo usan, qué muestran en la miniatura.
- De los COMENTARIOS: qué pregunta la gente (= FAQ real), de qué se quejan, qué les funcionó,
  dudas de uso, comparaciones con otros productos, **citas textuales**.
- **Método (ya no depende de la suerte del scraper).** Los comentarios cargan por JavaScript, así que
  Firecrawl solo a veces alcanzaba los primeros. **`yt-dlp` los baja de la API, con sus LIKES**, y el
  like es un **voto**: la queja más votada es la objeción más común del mercado, no la más ruidosa.

```bash
# 1 · COMENTARIOS con like_count
yt-dlp --write-comments --skip-download \
  --extractor-args "youtube:max_comments=200,all,200" -o "<producto>" "<URL del video>"
# → deja <producto>.info.json con .comments[]: text, like_count, author, timestamp

# 2 · LOCUCIÓN del video — en LOCAL, gratis y sin llave (el archivo no sale de tu equipo)
#     ANTES de instalar o descargar nada, mira si el modelo YA ESTÁ en el equipo
#     (hyperframes lo deja en ~/.cache/hyperframes/whisper/models/ggml-small.bin —
#     seguirla receta a ciegas re-descarga ~500 MB para nada):
#       ls ~/.cache/hyperframes/whisper/models/ggml-small.bin 2>/dev/null || echo "descargar"
#     Requisitos, una sola vez (solo si faltan):  brew install ffmpeg whisper-cpp
#     Y un modelo (solo si no apareció arriba):  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
ffmpeg -v error -i "<video>" -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
whisper-cli -m <ruta>/ggml-small.bin -l es -nt -f audio.wav
```

> Si el equipo ya tiene el atajo `golden-transcribe` en el PATH, esas dos líneas son una sola:
> `golden-transcribe "<video>"`. Y si `whisper-cli` no está instalado, la alternativa sin instalar
> nada es `npx hyperframes transcribe "<video>" --model small --language es` (mismo motor, más
> lento). **Nunca mandes a un servicio externo un video del cliente sin decírselo.**

> *Medido el 2026-08-11: 25 comentarios con sus likes reales en una sola corrida; y 7,5 minutos de
> audio transcritos en 29 segundos.* **Transcribe los 3–5 videos top**: la locución es el guion de
> venta que ya le funciona a alguien, y los subtítulos quemados no se pueden leer del fotograma
> porque van **una palabra por cuadro**.

- Si aun así no hay acceso → **decláralo** ("comentarios de YouTube no accesibles") y sigue
  (REGLA 5). **Nunca inventes comentarios.**

### TikTok
- Hashtags del producto/categoría (en varios idiomas), videos top del nicho y sus **comentarios**,
  sonidos en tendencia, creadores UGC que ya venden productos similares.
- Los videos con más interacción revelan el **formato nativo que convierte** (POV, demostración,
  storytime); los comentarios revelan el escepticismo típico ("es estafa?", "a mí no me sirvió").
- Método: `firecrawl_search`/`firecrawl_scrape` sobre tiktok.com + **TikTok Creative Center** (1.7).

### Instagram / Facebook
- Comentarios de los posts y ANUNCIOS de competidores (ahí la gente pregunta precio, duda y reclama
  en público — objeciones gratis). Grupos de Facebook del nicho (compra/venta, maternidad, salud…).

### Otros medios que SIEMPRE conviene barrer
- **Reddit / foros / Quora**: hilos honestos "does X work?" — el escepticismo más articulado.
- **Marketplaces**: Amazon (Q&A + reseñas 1–2★ y 4–5★), **AliExpress** (reviews con fotos REALES del
  producto de origen), MercadoLibre (reseñas y preguntas en español del mercado local).
- **Google**: "opiniones <producto>", "<producto> es confiable", autocompletado (= dudas masivas).
- Cualquier otro medio que el nicho use (Pinterest, blogs, podcasts): si el producto vive ahí, se mina.

### Qué se extrae de TODO lo anterior (la salida de 1.6)
| Qué | Para qué sirve |
|---|---|
| Necesidades expresadas ("ojalá tuviera…") | ángulos y diferenciales |
| Quejas top (lo malo) | objeciones a rebatir + qué NO prometer |
| Elogios top (lo bueno) | beneficios a liderar + prueba social |
| Preguntas repetidas | la FAQ real de la página y del bot |
| Lenguaje textual del cliente | hooks y copy que suenan a persona, no a marca |
| Títulos/videos con más vistas | hooks y formatos YA validados por el mercado |
Todo con fuente (URL del video/hilo) y volcado a la voz del cliente (1.5) y al dossier (capas 7–13 y 21).

## 1.7 Anuncios activos del nicho (inteligencia competitiva)
- **Meta Ad Library**: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<PAÍS>&q=<producto>`
  → mensajes, ofertas, formatos, **cuánto llevan activos** (los que no se apagan, convierten).
- **TikTok Creative Center**: top ads/hooks del nicho, sonidos en tendencia, formatos nativos.
- **✅ Receta PROBADA con el MCP de Meta (estudio Chile, 2026-08-07 — la vía más rápida):**
  1) `ads_library_search` con `countries:["<PAÍS>"]` + `ad_active_status:"ACTIVE"` + término del
     nicho → devuelve conteo de anuncios activos y las páginas que los corren;
  2) scrapear el **`ad_snapshot_url`** de cada anuncio **con firecrawl SIN `includeTags`** →
     devuelve el **copy verbatim del anuncio + el dominio de la landing del competidor**.
  - ⚠️ **Con `includeTags` el scrape vuelve VACÍO.** Detalle que cuesta tiempo si no se sabe.
  - Rendimiento real: así se levantaron 5 competidores con precios, combos y estrategia de copy
    en minutos.
- **Método alterno (si no hay MCP de Meta):** la Ad Library a veces bloquea el scraping directo. Plan por orden:
  1) `firecrawl_scrape` sobre la URL de Ad Library del producto/competidor;
  2) si bloquea → `firecrawl_search` de la categoría en TikTok/IG/FB (revela anuncios y ángulos activos);
  3) si aún no hay datos → **decláralo explícito** ("no se pudo acceder a anuncios activos") y sigue con
     lo que sí hay (REGLA 5). Nunca inventes que "vimos X anuncios".
- Sintetiza: ángulos dominantes, ofertas estándar del mercado, y **dónde diferenciarse**.

## 1.8 Síntesis estratégica (la salida de la fase)
- **Buyer personas (2–3)**: demográficos *(estimado, marcado como tal — o VALIDADO si hay data de
  pedidos/CRM, ver 1.5.bis; jamás copiados de la demografía de pauta sin cruzar con pedidos reales)*,
  situación "antes", dolores, deseos "después", objeciones, y **frases textuales** que usan.
- **Mapa de ángulos** (5–8): cada ángulo = 1 dolor/deseo + el beneficio que lo resuelve.
- **Lista de objeciones** + cómo rebatir cada una (alimenta página, ads y WhatsApp).
- **Diferenciales** ordenados por fuerza. **Oferta recomendada** (ancla de precio, bono, garantía).

## 1.9 Dossier psicológico de 30 capas (profundidad)
Con los datos duros recogidos, construye el **dossier psicológico** (`dossier-psicologico.md`): 30 capas
de promesa, mecanismo, dolores/miedos/anhelos, disparadores, criterios, objeciones, nivel de consciencia,
insights y públicos múltiples. **Ancla cada capa en las fuentes de arriba** (reseñas/competidores/redes);
lo que no tenga fuente, márcalo `(inferencia)`. Esta es la capa que más alimenta copy, ads y página.

> PUERTA: no avanzas a la página ni a las campañas sin datos duros + dossier (buyer persona, ángulos,
> objeciones, disparadores, públicos) listos.
