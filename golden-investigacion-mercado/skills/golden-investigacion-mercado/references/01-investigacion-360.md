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
- Está validado como ganador? Lo dicen sus ventas REALES en DropKiller (§1.3.bis), no su fama.
- Nivel de saturación del nicho (cuántos anunciantes activos, hace cuánto).

## 1.3.bis 🥇 El producto en DROPKILLER: sus ventas REALES (opción de búsqueda · G6.3)
Orden de FER (02-oct-2026): DropKiller va en las DOS skills, con dos usos distintos.
`golden-dropkiller-productos-ganadores` tiene **dos modos**: CAZA (busca productos que todavía no
conoces) y **VALIDAR** (su paso 1b: toma un producto YA conocido y dice si pasa su rúbrica y cuál es
su PVP mínimo). **Quién entra con "valida este producto":** si lo que se quiere es el veredicto
rápido de pasa/no pasa y el PVP mínimo, es la hermana; si lo que se quiere es el ESTUDIO (mercado,
competidores, voz del cliente, dossier, documento), es esta skill — que para la parte de mercado
llama a los mismos scripts, sin duplicarlos. Aquí el
producto **ya está elegido** y DropKiller se usa para medir SU mercado: cuánto vende de verdad,
cuántos lo venden, en qué etapa está y si sube o baja. Es la evidencia de nivel **COMPRA** de la
regla 15 (unidades que alguien pagó), por encima del gasto en anuncios y de la opinión.

**Cuándo se usa:** siempre que el producto se venda, o pueda venderse, por dropshipping en un país
que DropKiller indexa (`list_product_filters` da los países y plataformas). Si es marca propia y no
tiene ficha en esas plataformas, se busca su FUNCIÓN (el mismo problema resuelto por otro producto)
y se rotula que son **sustitutos, no el mismo producto**. Si DropKiller no responde o no hay cuenta,
se declara y la demanda queda sostenida por GASTO u OPINIÓN, rotulada así (regla 15).

**Receta, medida en vivo el 02-oct-2026** (un suplemento de drenaje linfático, Colombia):
1. **Barrer el mercado — DOS búsquedas, no una.** Ninguna sola es el mercado:
   - 1a · **PALABRA CLAVE PAGINADA, y esta es la que mide el mercado**: `search_products` con
     `q` + `countryCode`, siguiendo `nextCursor` **hasta `hasNext:false`**. Solo así el conteo
     queda **CERRADO**. *(Medido 02-oct-2026, "lymphatic" + CO: 194 filas en 4 páginas de 50.)*
   - 1b · **SEMÁNTICA, para ENCONTRAR el producto, no para medirlo**: `semantic_search_products`
     con `query` = nombre + función en el idioma del país, o `imageUrl` si hay foto (trae menos
     ruido). Sirve cuando no se sabe cómo lo llaman, o para hallarlo por su función.
   - 🚨 **La semántica devuelve 40 y 40 es su TOPE, no el mercado.** Desde este cliente MCP
     **no se puede subir `limit`**: el conector lo recibe como TEXTO y lo rechaza por validación
     (medido dos veces, con 10 y con 100). Se asume 40 y **se declara ABIERTO**. El `cursor` sí
     pasa, porque es texto: por eso 1a sí puede cerrar.
   - 🚨 **Las dos apenas se solapan:** en la corrida real, las 40 semánticas y las 194 por palabra
     clave compartían **UN solo id**. Quedarse con una sola vía es ver un pedazo y creerlo entero.
   Ambas respuestas se guardan en `PROYECTOS/<PRODUCTO>/dropkiller/` con su fecha (son grandes,
   ~116 KB las 40): no se leen en el chat.
2. **Consolidar el mercado** con el script de la skill hermana, que no se duplica aquí:
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/consolidar_mercado.py mercado.json --pais XX --incluir "<regex del nombre>"`.
   Devuelve fichas únicas, espejos descartados, proveedores activos con sus ventas y su stock, ventas
   totales del mercado y la ETAPA. El regex lo decide quien miró las fotos, no el script, y su
   `cuadre` tiene que cerrar. Se consolida **la UNIÓN de 1a y 1b**, no una sola.
   *Medido 02-oct-2026 (drenaje linfático, CO), unión de las dos búsquedas: **234 filas → 81 ids →
   3 fuera por nombre, 151 espejos, 80 únicas, 30 proveedores, 72.946 unidades, etapa QUEMADO**,
   cuadre cerrado. El listado que la empresa ya vendía aparece primero (25.758 u.).*
   🔴 **Por qué importa este dato y no el anterior:** la primera medición usó **solo la semántica**
   y dio 20.254 u. con 10 proveedores — **el 28 % del mercado**, y el listado propio ni aparecía.
   El número pequeño no era "otro recorte": era un **PISO presentado como universo**. Sigue ABIERTO
   para otros términos (p. ej. "drenaje linfatico" por palabra clave no se corrió).
3. **Ventas reales** del que más vende y del proveedor que se usaría: su ficha trae `history30d`
   (o `get_product_history` con su id) →
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/ventas_reales.py ficha.json`.
   Da REAL / DUDOSO / FANTASMA, vendidas depuradas contra reportadas, ritmo diario, reabastecimientos
   y tendencia. *Medido: 8.570 reportadas en 30 días → 6.966 reales (un pico de 1.871 en un día
   recortado al ritmo base de 267), 3 reabastecimientos, tendencia "frenando".* Sin este paso, un
   ajuste de inventario se lee como venta.
4. **Anuncios y precios de quien lo vende:** §1.7 (DropKiller primero). Para canal y precios por
   producto: `semantic_search_ads` con la imagen + una descripción corta + el país (la imagen sola
   trae ruido) → `competencia.py canal` y `competencia.py precios` de la misma hermana.

**Qué alimenta:** la sección 3 del documento (Mercado y demanda) y, en el veredicto, tres de los
cinco datos: **demanda** (unidades reales, nivel COMPRA), **saturación** (etapa + proveedores
activos + anunciantes) y **proveedor** (`salePrice` = costo, `stock`, `providerVerified`). El PVP
mínimo y la cuenta COD salen de `viabilidad_cod.py` de la hermana: aquí se citan, no se recalculan.

**Trampas medidas:**
- **TODO conteo dice si quedó CERRADO o ABIERTO.** Cerrado = se paginó hasta `hasNext:false`.
  Abierto = tocó un tope (las 40 de la semántica) o quedaron términos sin correr: se escribe `N+`,
  y **una columna con `N+` no se ordena de mayor a menor**, porque los abiertos no son comparables.
- La búsqueda trae VECINOS: por eso el `--incluir`, y **la foto la mira una persona**, no el regex.
  *(El regex de la primera corrida excluía por nombre cosas que sí eran el producto y dejaba dentro
  gotas de otras marcas: el filtro por texto no sustituye mirar.)*
- `totalSoldUnits` cuenta ajustes de inventario: nunca se cita crudo, se cita lo depurado.
- DropKiller mide las plataformas de dropshipping que indexa, **no** Shopify propias, MercadoLibre
  ni tiendas físicas. Es el mercado de dropshipping, y se rotula así, no "el mercado total".
- Toda cifra lleva fecha de medición (regla 13): la etapa cambia en semanas.
- Sin la skill hermana instalada se leen a mano los campos `totalSoldUnits`, `soldUnitsLast7Days`,
  `soldUnitsLast30Days`, `suspectedSalesAdjustment` y `salesConfidence`, y se declara
  **"sin depurar ventas fantasma"**.

## 1.4 Competidores (3–7)
Para cada uno: nombre + URL · propuesta de valor · **precio** · oferta/promo · diferencial ·
ángulo de marketing · qué hace bien · **hueco que deja** (oportunidad). Tabla comparativa.
- Revisa sus anuncios activos (**DropKiller primero**, ver 1.7) y su contenido organico.
- **El STACK del competidor se mide:** `store_tech_report` (tema, apps, pixeles) — dato duro.
- 🚨 **Los INGRESOS de tienda NO son un dato** (trampa 8, medida): el propio conector **retiro los
  ordenamientos por ingresos y visitas el 2026-07-02 por fuente desactualizada**, y el canal oficial
  los llama "estimaciones, no 100 % reales". `get_store`/`get_store_revenue_history` se pueden mirar
  para **ordenar por tamano aproximado**, jamas para escribir una cifra de facturacion en el estudio.
  Si se cita, va rotulado `(estimado viejo, no verificable)`. El `billing` de un producto tampoco es
  facturacion de la tienda: es precio de proveedor x unidades.
- El tamano REAL del rival se infiere de lo que si se mide: unidades vendidas del producto
  (§1.3.bis, nivel COMPRA) y anuncios con ventana observada (§1.7, nivel GASTO).

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
### 🥇 DROPKILLER PRIMERO (MCP propio · verificado en vivo 2026-09-28)
Indexa Meta y TikTok **con historia**, que es lo que la Ad Library publica no da: cuantos dias
**declara** cada anuncio y, sobre todo, **cuando se le vio** de verdad.

🚨 **TRAMPA DEL ANUNCIO ZOMBI (trampa 11 de la hermana, medida sobre 80 anuncios).** `activeDays`
es **exactamente `endDate - startDate`: fechas DECLARADAS, no dias observados**, y avanza solo —
el mismo anuncio declaraba 11 dias el 18-sep y 16 el 23-sep sin que nadie lo viera. 17 de 80 (21 %)
declaran mas de 7 dias por encima de lo observado; el peor, **466 declarados contra 105 vistos**, y
uno declara 81 dias **con UNA sola observacion**. Por eso:
- **Un `activeDays` alto NO prueba gasto sostenido.** La prueba es la **ventana observada**
  (`firstSeenAt` .. `lastSeenActiveAt`), y se cita asi: *"declara N dias, observado M"*.
- **El error simetrico tambien cuenta:** 74 de 80 empezaron ANTES de que DropKiller mirara, asi que
  la ventana observada es un **PISO, no la verdad**. Castigar por ella sin decirlo es el mismo fallo
  al reves. Se dan los dos numeros y se deja decidir.
- Nivel de evidencia (regla 15): esto es **GASTO**, nunca COMPRA — y gasto *declarado* hasta que la
  ventana observada lo respalde.

```
search_ads  countryCodes:["CO"]  status:"ACTIVE"  maxStaleDays:7
            broadcastDuration:"evergreen"        # >30 dias corriendo
            sort:"duration"  distinctAdvertisers:true  q:"<termino del nicho>"
```
Devuelve, medido: `activeDays` (DECLARADO — ver la trampa del zombi arriba) ·
`firstSeenAt`/`lastSeenActiveAt` (**la ventana observada: esto es lo que vale**) ·
`copyPreview` (copy VERBATIM del competidor) · `cta` ·
`landingUrl` (revela el embudo: `api.whatsapp.com/send` = COD por WhatsApp; dominio propio =
landing) · `winnerScore` · `imageUrl`/`videoUrl` descargables · `externalUrl` a la Ad Library.
*Corrida real 2026-09-28 en Colombia: un anuncio con 1.111 dias activos (desde 2019), staleDays 0.*

🚨 **TRAMPA MEDIDA: `status:"ACTIVE"` MIENTE SOLO.** La propia API lo declara — un anuncio pasa a
`INACTIVE` **solo tras 60 dias sin verse**. Pedir `ACTIVE` a secas trae anuncios que nadie ve hace
semanas, y el estudio concluye que un competidor "sigue pautando" cuando ya se apago.
**`maxStaleDays: 7` SIEMPRE junto a `status:"ACTIVE"`.** Es la diferencia entre *estaba* y *esta*.

⚠️ **`q` es texto libre** sobre titulo, descripcion y anunciante: buscar "colageno" trajo serums y
centros de estetica. Aplica la Regla Cero — el dato responde a lo que pedi? — y descarta a mano lo
que no sea del nicho ANTES de citarlo.

| Necesidad del estudio | Llamada | Que aporta |
|---|---|---|
| Con que esta construido el competidor | `store_tech_report` (por dominio, sin UUID) | tema, apps (Releasit = COD), pixeles, redes |
| Tamano APROXIMADO del competidor | `get_store` · `get_store_revenue_history` | ⚠️ **estimacion vieja** (fuente retirada 2026-07-02, trampa 8): sirve para ordenar, NO para citar como cifra |
| Si el producto sube o baja | `get_product_history` → **depurado con `ventas_reales.py`, nunca crudo** | precio, stock y unidades por dia; crudo mete ajustes de inventario y dias rellenos con cero |
| Creativos del competidor | `get_ad_creatives` · `list_store_ads` | piezas para el teardown |
| Ficha comercial de una tienda | `brief_store` | ingresos + ads + top productos en una llamada |

🟢 **Respeta la REGLA 12 sola**: cuando no tiene redes capturadas responde *"NO significa que la
tienda no las tenga; no las hemos inspeccionado — no reportes su ausencia como hallazgo"*.
**Un cero suyo tampoco se cree**, se prueba.

**Frontera (G6.4):** aquí DropKiller estudia un producto que YA se eligió: sus ventas reales
(§1.3.bis), sus anuncios y el stack de quien lo vende. La hermana
`golden-dropkiller-productos-ganadores` hace dos cosas distintas: **CAZA** (encontrar productos que
no se conocen) y **VALIDAR** (su paso 1b: rúbrica y PVP mínimo de un producto conocido). El PVP
mínimo y la cuenta COD **siempre** salen de ella: aquí se citan, no se recalculan.

### Vias de respaldo (si DropKiller no responde, se DECLARA y se baja a estas)
- **Meta Ad Library**: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<PAÍS>&q=<producto>`
  → mensajes, ofertas, formatos, **cuánto llevan activos** (los que no se apagan, convierten).
- **Google · Centro de Transparencia** (la tercera biblioteca, y la que casi nadie mira):
  se lee por su RPC interno, **gratis y sin llave**, y el país es un número, así que **barre país
  por país**. Receta exacta en `scraping-firecrawl.md` §Bibliotecas de anuncios. Medido: 40 anuncios
  activos de un dominio en Colombia en una sola petición.
- **TikTok Creative Center**: top ads/hooks del nicho, sonidos en tendencia, formatos nativos.
  ⚠️ **La Ad Library de TikTok (`library.tiktok.com`) NO cubre LatAm** — solo 32 países europeos, por
  ley del DSA. Un cero ahí significa *el dato no existe*, no *está bloqueado*: no se reporta como
  fallo ni se insiste. Para LatAm, Creative Center **con sesión iniciada** (sin login se ve recortado).
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

> **SIGUE LA FASE 3** (`03-mercado-en-vivo.md`): con los datos duros y el dossier en la mano, ahí se
> levanta el mapa país por país, la matriz de combos, la autopsia de las páginas que ya venden y el
> inventario de creativos — y de ahí salen LOS HUECOS, que es lo que se convierte en oferta propia.

> PUERTA: no avanzas a la página ni a las campañas sin datos duros + dossier (buyer persona, ángulos,
> objeciones, disparadores, públicos) listos.
