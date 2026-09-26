# Scraping con Firecrawl — manual verificado Golden

## Índice
1. [Regla Cero — el resultado puede ser BASURA aunque todo diga que salió bien](#-regla-cero--el-resultado-puede-ser-basura-aunque-todo-diga-que-salió-bien) (4 modos de fallo + el candado)
2. [Matriz de fuentes — Firecrawl](#matriz-de-fuentes--qué-funciona-y-qué-no-medido)
3. [Matriz por navegador](#matriz-por-navegador--el-respaldo-también-medido-2026-08-02)
4. [Bibliotecas de anuncios — Meta, Google y TikTok](#bibliotecas-de-anuncios--qué-cubre-cada-una-y-cómo-se-lee-medido-2026-09-06) (**Google por RPC, gratis** · TikTok es solo Europa)
5. [Recetas verificadas](#recetas-verificadas)
6. [Parámetros que importan](#parámetros-que-importan)
7. [Video y comentarios — `yt-dlp`](#video-y-comentarios--yt-dlp--instalado-2026-08-01)
8. [Checklist antes de entregar cualquier dato scrapeado](#checklist-antes-de-entregar-cualquier-dato-scrapeado)
9. [La matriz CADUCA — la suite de verificación](#-la-matriz-caduca--la-suite-de-verificación)
10. [Changelog](#changelog)

**Versión:** `SF3.1` · Probado en vivo el **2026-07-31, 08-01 y 08-02** contra AliExpress, YouTube,
TikTok Creative Center, Temu, Amazon, MercadoLibre Colombia, Reddit y dos dominios propios —
**por Firecrawl Y por navegador real**.
Todo lo que sigue está MEDIDO ejecutando la herramienta, no leído de su documentación.
Lo que no se probó, se dice que no se probó.

Fuente única de verdad de scraping del ecosistema Golden. La usan:
`golden-investigacion-mercado`, `golden-dropkiller-productos-ganadores`, `golden-matriz-viral`,
`golden-video-teardown`, `golden-chatea-pro-prompt-ventas`, `golden-shopify`, `golden360`.

---

## 🚨 REGLA CERO — el resultado puede ser BASURA aunque todo diga que salió bien

`statusCode: 200` no significa nada. Se midieron **tres formas distintas** de fallar, y
**ninguna verificación sola las caza todas**.

### Modo 1 · ALUCINACIÓN TOTAL — la página viene hueca y el extractor inventa
Pedida la ficha de un removedor de verrugas en AliExpress. Redirigió a `.us` y sirvió HTML vacío.
Firecrawl no devolvió error: **inventó un producto entero.**
```json
{ "titulo": "Smart TV 55\" 4K LED", "precio": "$499.99", "rating": "4.5", "num_resenas": "150" }
```
**Tell:** `metadata.title` **vacío** (y `og:title` vacío).

### Modo 2 · EXTRACCIÓN SEÑUELO — carga otra página y te da el menú
Buscado "wart remover" en Temu. Redirigió a la portada genérica y devolvió **72 categorías de
ropa** ("Vestidos de mujer", "Jeans para hombre", "Botas"), todas con `precio: "N/A"`.
Igual en TikTok Creative Center: devolvió los botones del menú ("Top Ads", "Trends", "API").
**Aquí `metadata.title` viene POBLADO. El check del Modo 1 pasa en verde.**
**Tells:** `metadata.url` ≠ `metadata.sourceURL` (hubo redirección) · valores `"N/A"` en masa ·
etiquetas que son navegación, no datos.

### Modo 3 · MURO ANTI-BOT — no hay dato y no hay aviso
Buscado "wart remover" en Amazon. La respuesta **no trae campo `json` en absoluto**, solo
`metadata` — con `anti-csrftoken-a2z` repetido 70 veces y `encrypted-slate-token`.
**`title` poblado ("Amazon.com : wart remover") y SIN redirección: los dos checks anteriores
pasan en verde y aun así no hay nada.**
**Tell:** el campo `json` **no existe** en la respuesta.

### Modo 4 · CAPTCHA — inventa datos CON el título poblado (rompe el check del Modo 1)
Buscado "removedor de verrugas" en **MercadoLibre Colombia**. Devolvió ocho productos:
```json
{"titulo": "Producto 1", "precio": "$50,000", "vendidos": "10", "rating": "4.5"}
{"titulo": "Producto 2", "precio": "$70,000", "vendidos": "20", "rating": "4.0"}
```
Relleno de plantilla puro, con precios, ventas y ratings inventados. El metadata delata la causa:
`url: ".../captcha/wall"` — **un muro de captcha**.
**Aquí `metadata.title` viene POBLADO ("Seguridad — Mercado Libre") y SÍ hay campo `json`:
los checks 1 y 2 pasan en verde.** Es el modo más traicionero de los cuatro.
**Tells:** `/captcha/` en `metadata.url` · el título es un muro ("Seguridad", "Iniciar sesión",
"Access denied") · valores secuenciales tipo `Producto 1`, `Producto 2`.

### ✅ La verificación que sí funciona (correr las 4, en orden)

1. **Existe el campo `json`?** Si no está → muro anti-bot. Descartar.
2. **`metadata.title` poblado?** Vacío → alucinación. Descartar.
3. **`metadata.url` == `sourceURL`?** Si cambió → estás leyendo OTRA página. Verificar.
4. **🎯 EL DATO RESPONDE A LO QUE PEDÍ?** Es la única que caza los tres modos.
   Si buscaste "removedor de verrugas" y te llegan "Vestidos de mujer", es basura aunque
   los tres checks anteriores estén verdes. Si todos los valores son `"N/A"`, es basura.

**Regla dura:** el dato que no pasa las 4 no se usa, no se cita, no entra a `PRODUCTO.json` y no
se reporta. Se escribe **"no obtenido"** y se propone otra vía. Un "no pude" es un resultado
válido; un dato inventado destruye la decisión y el presupuesto que va detrás.

### 🔒 EL CANDADO — no confíes en acordarte, córrelo

Las 4 verificaciones están **automatizadas**. Guarda la respuesta del scrape y pásala por:

```bash
python3 ~/.claude/skills/golden-investigacion-mercado/scripts/candado_scraping.py \
  respuesta.json --pedi "removedor de verrugas"
```

El `--pedi` se compara **sin tildes y sin mayúsculas** (desde G5.21.1): "PEPTEA serum" casa con
"PEPTÉA Sérum". Antes, una tilde bastaba para descartar la página correcta. Para comprobar que el
candado sigue sano: `candado_scraping.py --autoprueba` (5 casos con control negativo).

Devuelve **PASA · REVISAR · DESCARTAR** con el motivo, y código de salida 1 si hay que descartar
(encadenable con `&&`). El flag `--pedi` activa el check 4, que es el más importante: **pásalo siempre.**

**Probado contra los 4 fallos reales de este manual: los caza los 4, y deja pasar el dato bueno.**
Una regla escrita se olvida; un candado que devuelve DESCARTAR, no.

Este es el mecanismo por el que se violarían **"solo productos REALES"** y **"datos reales antes
de generar"** sin que nadie mienta: mentiría la herramienta. Verificar ES cumplir esas reglas.

> **Excepción útil:** `formats:["rawHtml"]` **no pasa por el extractor**, así que es inmune a los
> modos 1 y 2. Si solo necesitas buscar una cadena en el HTML (detectar un tema Shopify, un pixel,
> un script), pide `rawHtml`, guárdalo a archivo y usa `grep`. Es la vía más honesta que hay.

---

## Matriz de fuentes — qué funciona y qué no (MEDIDO)

| Fuente | Estado | Detalle |
|---|---|---|
| **AliExpress** listado | ✅ **Funciona** | 8 productos reales con precio y "480 sold" / "3,000+ sold". 9 créditos |
| **AliExpress** ficha individual | ⚠️ Inestable | Redirige a `.us` y sirve página hueca → **Modo 1**. Usar el listado |
| **YouTube** metadatos | ✅ **Funciona** | Título, canal, vistas, likes exactos (postprocesador nativo `youtube`) |
| **YouTube** comentarios | ❌ Firecrawl no llega | `comentarios: []`. Usar `yt-dlp` (ver abajo) |
| **Temu** | ❌ **No funciona** | La búsqueda redirige a portada genérica → **Modo 2** |
| **Amazon** | ❌ **No funciona** | Muro anti-bot, sin campo `json` → **Modo 3** |
| **TikTok Creative Center** · Top Ads/productos | ❌ **No funciona** | App JS tras redirección → **Modo 2** |
| **TikTok Creative Center** · hashtags | ⚠️ Parcial | En `markdown` SÍ salen datos reales (#hashtag, posts, vistas), pero **región US por defecto**; el selector de país es JS. No sirve para Colombia sin navegador |
| **MercadoLibre Colombia** | ❌ **No funciona** | Muro de **captcha** → **Modo 4**: inventó "Producto 1..8" con title poblado |
| **Reddit** | ❌ **No funciona** | Firecrawl lo rechaza de plano: *"we do not support this site"*. Falla en voz alta |
| **Sitios propios / Shopify** | ✅ Funciona | Ver `golden-shopify/references/temas.md` (vía `rawHtml`) |

## Matriz por NAVEGADOR — el respaldo, también medido (2026-08-02)

Lo que Firecrawl no saca, a veces lo saca un navegador real. **También probado, no supuesto.**

| Fuente | Navegador | Detalle medido |
|---|---|---|
| **Amazon** | ✅ **FUNCIONA, y bien** | 48 tarjetas · **34 con contador de ventas (71%)** · 46 con precio · 45 con rating · total "155 resultados" · precios ya en **COP** y "Enviar a Colombia" detectado solo. **Re-verificado el 2026-09-08: sigue igual de bueno** — 48 tarjetas, 30 con contador (62%), 44 con precio, total "145 resultados", en español |
| **Temu** | ❌ **Muro de sesión** | Redirige a login: *"Email o número de teléfono → Continuar"*. No es JS, es autenticación |
| **MercadoLibre CO** | ❌ **Muro de sesión** | *"Para continuar, ingresa a tu cuenta"* |
| **Reddit** | ❌ **Bloqueado por política** | El panel no permite abrirlo |


> 🔶 **Amazon disparó la alarma de la suite el 2026-09-08** (de 1.716.438 b a ~173.000-245.000 b por HTTP
> plano, y desapareció la marca `anti-csrftoken`). **Re-verificado con la herramienta real ese mismo día: la
> vía por navegador NO se rompió.** Es el caso de manual de por qué el veredicto es CAMBIO / IGUAL y nunca
> FUNCIONA / NO FUNCIONA: cambió lo que Amazon le sirve a un curl desnudo, no lo que ve un navegador. Tras
> verificar, se re-graba la base con `--baseline`.

### Receta del scanner de volumen en Amazon (la que quedó buena)
Navegar a `amazon.com/s?k=<producto>` y extraer del DOM:
```js
document.querySelectorAll('[data-component-type="s-search-result"]')
// por tarjeta: /([\d.,]+\s*K?\+?)\s+comprados el mes pasado/  ← el contador de demanda
//             /COP\s?([\d.,]+)/  ·  /([\d.]+) de 5 estrellas/
// y el total:  /1 a \d+ de ([\d.,]+) resultados/
```
Muestra real medida: `1 K+`, `10 K+`, `300+` comprados el mes pasado. Amazon detecta Colombia y
convierte precios solo, así que **no hace falta forzar país**.

**Consecuencia para el scanner de volumen.** De las tres tiendas que se citaban:
- **AliExpress** ✅ por Firecrawl (`json` sin actions)
- **Amazon** ✅ **por navegador** (mejor que AliExpress: da ventas + rating + reseñas + total)
- **Temu** ❌ por ninguna vía sin una cuenta. Solo funcionaría con `claude-in-chrome` si el usuario
  **ya tiene sesión iniciada** en su Chrome real. Preguntárselo, no asumirlo.
- **MercadoLibre** ❌ igual que Temu: necesita cuenta.

⚠️ **Corrección de SF2.0:** ese manual decía *"para Temu y Amazon hay que ir al Chrome MCP"*
**sin haberlo probado**. Medido hoy: era cierto para Amazon y **falso para Temu**. Mismo error que
esta casa corrige en todas partes — afirmar por deducción en vez de por ejecución.


## Bibliotecas de anuncios — qué cubre cada una y cómo se lee (MEDIDO 2026-09-06)

Las tres no son intercambiables: **una tiene límite legal de países, no técnico**. Antes de dar por
rota una biblioteca que devuelve cero, mirar si el país siquiera está en su lista.

| Biblioteca | Cobertura | Vía que funciona | Coste |
|---|---|---|---|
| **Meta Ad Library** | Mundial | MCP de Meta: `ads_library_search` con `countries` + `ad_active_status:"ACTIVE"`, y luego scrapear el `ad_snapshot_url` **sin `includeTags`** | Gratis |
| **Google · Centro de Transparencia** | Mundial | Su **RPC interno**, receta abajo | Gratis, sin llave |
| **TikTok · Commercial Content Library** | ❌ **Solo 32 países europeos** | No aplica a LatAm: el dato no existe | — |

### ✅ Google · Centro de Transparencia por su RPC interno (gratis, sin llave, sin cookies)

Medido el 2026-09-06: devuelve los creativos activos de un dominio en un país, en una sola petición
y sin autenticación.

```bash
# 1 · Anunciantes de un país (devuelve id AR..., país y conteo de anuncios)
curl -s --compressed -X POST \
  'https://adstransparency.google.com/anji/_/rpc/SearchService/SearchSuggestions?authuser=' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode 'f.req={"1":"<término>","2":10,"3":10,"4":[2170],"5":{"1":1}}'

# 2 · Creativos activos de un dominio o anunciante
curl -s --compressed -X POST \
  'https://adstransparency.google.com/anji/_/rpc/SearchService/SearchCreatives?authuser=' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode 'f.req={"2":40,"3":{"8":[2170],"12":{"1":"<dominio>","2":true}},"7":{"1":1,"2":0,"3":2170}}'
```

> 🚨 **EL `"2":40` ES EL TOPE QUE PIDES, NO UN CONTEO — trampa medida el 2026-09-08.** La primera
> redacción de esta receta decía "40 anuncios activos" y era falso: **cinco países distintos
> devolvieron 40, 40, 40, 40 y 40**, que es exactamente el límite del propio `f.req`. Cambiado a
> `"2":100`, devuelve 100. **Nunca reportes ese número como "cuántos anuncios corre el
> competidor"**: de ahí sale una lectura de saturación del nicho, y con ella una decisión de
> lanzar o matar un producto. Para contar de verdad hay que **paginar subiendo el tope hasta que
> una página devuelva MENOS que el límite pedido**; ese último tramo sí cierra el conteo.
>
> ✅ **Lo que sí quedó probado: el país filtra de verdad.** Colombia (2170) y España (2724) sobre el
> mismo dominio devolvieron **0 ids en común de 40 contra 40**. Si el parámetro se estuviera
> ignorando, las dos listas serían la misma — que es la comprobación que hay que hacer siempre
> antes de fiarse de un filtro geográfico.

- **El país es un NÚMERO** (criterio geográfico de Google). Cambiarlo es todo lo que hace falta para
  **barrer país por país**: es la vía más barata que hay al mapa mundial. Códigos probados el
  2026-09-08, los cinco con respuesta real: **Colombia 2170 · México 2484 · Argentina 2032 ·
  Chile 2152 · España 2724**. Los demás salen del listado de criterios geográficos de Google Ads.
- Cada anuncio vuelve con un id `CR...`; la pieza se abre en
  `adstransparency.google.com/advertiser/<AR...>/creative/<CR...>?region=<país>`.
- ⚠️ **Scrapear la página con Firecrawl NO sirve** (medido el mismo día): devuelve la portada,
  porque los resultados los pinta JavaScript. El RPC es la única vía limpia.

> **La técnica es lo que se reutiliza.** El esquema del `f.req` no se adivina: se captura envolviendo
> `window.fetch` y `XMLHttpRequest.prototype.send` en la página real, haciendo la búsqueda a mano y
> leyendo el cuerpo que manda su propio front. Cuando un sitio "no se puede scrapear", muchas veces
> lo que falta es el esquema del cuerpo, no permiso. Probado aquí en dos vueltas: con el cuerpo
> inventado, `400 BadRequestException`; con el capturado, 40 anuncios.

### ❌ TikTok Ad Library: límite LEGAL, no técnico

`library.tiktok.com` existe porque una ley europea obliga a publicarla. Lista completa de su selector,
leída el 2026-09-06: los 27 de la UE más Reino Unido, Suiza, Noruega, Islandia, Liechtenstein y
Turquía. **No están Colombia, México, LatAm ni Estados Unidos.** Una búsqueda con `region=CO` devuelve
"Total de anuncios: 0" y eso **no es un bloqueo**: el dato no existe ahí. Su API interna responde 421
o 425 desde fuera, así que insistir por ahí es perder el día.

**Para TikTok en LatAm**, medido el mismo día: el **Creative Center** (`ads.tiktok.com/business/creativecenter`)
carga Colombia **sin login** con industria, likes, percentil de CTR y presupuesto, pero corta con
"Log in to access all Top Ads"; con una cuenta de TikTok Ads (gratis) logueada en el Chrome real se
abre completo. Su API interna sin sesión responde `40101 no permission`. Histórico de creativos: solo
con herramienta de pago.

---

## Recetas verificadas

### ✅ Listado de productos → `json` SIN actions
```
firecrawl_scrape
  url: <listado de AliExpress>
  formats: ["json"]
  proxy: "stealth"
  location: { country: "CO", languages: ["es"] }
  jsonOptions: { prompt: "...", schema: {...} }
  ❌ SIN actions
```
Los listados ya traen 8-12 productos en el HTML inicial: **el scroll no hace falta**, y meterlo
rompe la llamada.

### ❌ `json` + `actions` → SE CAE POR TIMEOUT
Probado 3 de 3 (listado AliExpress, video YouTube, y de nuevo en v2). **No usar esa combinación.**

### ✅ Scroll infinito → `actions` + `markdown`
```
formats: ["markdown"] · proxy: "stealth"
actions: [{wait 3000}, {scroll down}, {wait 2000}, {scroll down}, {wait 2000}]
```
Medido: 182.409 caracteres de AliExpress con los contadores reales dentro.
⚠️ **Inunda el contexto.** Volcar a archivo y `grep`, o mandar a subagente. Nunca entero al hilo.

### ✅ `firecrawl_map` → inventario de URLs (VERIFICADO)
Medido: 35 URLs de `comunidadgolden.com` con título y descripción. Barato, no baja contenido.
⚠️ **Un map vacío NO prueba que el sitio no tenga páginas** — solo que Firecrawl no lo tiene
indexado (probado: otro dominio propio devolvió `links: []` estando vivo). Igual que la regla de
la casa **"un cero solo prueba si cubrió TODO"**: antes de afirmar un "no existe", cambiar de vía.

### ⚪ `firecrawl_monitor` → disponible, sin ejercitar
`firecrawl_monitor_list` responde `success: true` con `data: []`: el endpoint funciona y la cuenta
está autorizada, hoy con cero monitores. **No se creó ninguno de prueba** porque programa chequeos
recurrentes y correos en la cuenta de FER — es decisión suya, no de la skill.
Uso natural si se activa: vigilar precio de un competidor o quiebre de stock de un proveedor.

---

## Parámetros que importan
- **`proxy: "stealth"`** — obligatorio en AliExpress/Temu/TikTok/Amazon. Sin él, bloqueo directo.
- **`location: { country: "CO", languages: ["es"] }`** — sin esto sales con `timezone:
  America/New_York` y precios de USA. **Para Golden el país objetivo casi siempre es CO** (o PA).
- **`waitFor`** — no arregla una página hueca (probado: 5000 ms sobre la ficha rota, siguió vacía).
- **`maxAge`** — reusa caché, ahorra créditos en re-consultas del mismo día.
- **Coste medido:** 9 créditos por scrape con stealth (5 si la página es liviana). `map` es mucho
  más barato: úsalo para inventariar antes de scrapear en serie.

---

## Video y comentarios — `yt-dlp` (✅ INSTALADO 2026-08-01)

`yt-dlp` y `ffmpeg` están instalados y **probados en vivo** (versiones: `yt-dlp --version` y
`ffmpeg -version` en el momento; no se escriben aquí porque caducan solas).

### Comentarios (lo que Firecrawl no puede)
```bash
yt-dlp --write-comments --skip-download --no-warnings \
  --extractor-args "youtube:comment_sort=top;max_comments=100" \
  -o "salida.%(ext)s" "<URL>"
```
Medido: 30 comentarios extraídos, con **`author`, `text` y `like_count`**, de ~2.450.067
disponibles. Leerlos con `jq`:
```bash
jq -r '.comments[] | "[\(.like_count)] \(.author): \(.text)"' salida.info.json
```
🎯 **`like_count` es la joya:** un comentario con miles de likes es un dolor o una objeción que la
audiencia YA validó por votación. Ordenar por likes da la jerarquía real de objeciones — mejor
que cualquier lista escrita a mano. Alimenta la minería de comentarios de la investigación y la
matriz viral.

⚠️ `comment_sort=top` y `max_comments` son obligatorios: sin tope, intenta bajar millones.

### ⚠️ Fuera de YouTube: metadatos sí, comentarios NO (medido 2026-08-02)
Probado en un video real de TikTok (`@philsmypharmacist`):
- ✅ **Metadatos reales:** título, canal, **49.400 vistas, 986 likes**
- ❌ **Comentarios: 0 descargados.** `--write-comments` funciona en YouTube, **no en TikTok**

| Red | Metadatos | Comentarios |
|---|---|---|
| YouTube | ✅ | ✅ con `like_count` |
| TikTok | ✅ vistas y likes | ❌ **cero** |
| Instagram / Facebook | ⚪ sin probar | ⚪ sin probar |

**Consecuencia:** la minería de comentarios hoy es **solo de YouTube**. Para TikTok se tienen las
métricas del video (que ya sirven para rankear qué pieza estudiar), pero el texto de los
comentarios hay que sacarlo por navegador o pegado del usuario.

### Descargar el video (para teardown)
```bash
yt-dlp -o "~/Desktop/teardown/%(title).60s.%(ext)s" "<URL>"
```
Cubre YouTube, TikTok, Instagram, Facebook y X (la descarga de TikTok sí funciona: solo fallan
los comentarios). Con el archivo en disco, el pipeline de `ffmpeg` + fotogramas + transcripción
funciona completo.

---

## Checklist antes de entregar cualquier dato scrapeado
1. Existe el campo `json`? (si no → muro anti-bot)
2. `metadata.title` poblado? (vacío → alucinación)
3. `metadata.url` == `sourceURL`? (cambió → otra página)
4. **El dato responde a lo que pedí?** (la que caza todo)
5. Es del país objetivo? (`location` puesto, moneda correcta)
6. Si es cifra de prueba social que va a una página o un anuncio: **doble verificación**, porque
   de ahí sale un claim público.

## 🔁 La matriz CADUCA — la suite de verificación

Todo lo de arriba está medido, pero medido **una vez**. Los sitios cambian defensas cada pocos
meses y el riesgo real es que nadie se entere: las skills seguirían afirmando "Amazon funciona por
navegador" hasta que un día no.

```bash
python3 ~/.claude/skills/golden-investigacion-mercado/scripts/verificar_fuentes.py
```

Toma la huella de cada fuente (tamaño, redirección, marcas de muro, HTTP) y la compara con la del
día que se midió. Corre además las sondas de `yt-dlp`, que **sí son definitivas** porque usan la
herramienta real.

**Es un detector de CAMBIO, no de funcionamiento.** Amazon devuelve firma anti-bot por HTTP plano
y aun así funciona por navegador: una firma no prueba que algo esté roto. Por eso el veredicto es
CAMBIO / IGUAL. Si algo se movió, hay que re-verificar con la herramienta de verdad — y para eso
el script imprime la **checklist de sondas MCP** (Firecrawl y navegador, que no puede correr él
mismo) con sus parámetros exactos y el resultado esperado.

- Línea base grabada: **2026-08-02**. Avisa solo al pasar los **60 días**.
- Tras re-verificar y actualizar esta matriz: `verificar_fuentes.py --baseline` para re-grabar.
- ⚠️ `scripts/fuentes_baseline.json` **queda fuera del blindaje** a propósito: el script tiene que
  poder reescribirlo. Si se blinda, la suite deja de poder actualizarse.
- Probado el 2026-08-02: sin cambios reporta IGUAL, y con la base falseada cazó los tres cambios
  simulados (tamaño, marcas nuevas, redirección).

### ⚠️ Correrla UNA VEZ AL MES — sondear dispara lo que se está midiendo
Hallazgo de la propia construcción de la suite: tras sondear AliExpress varias veces el mismo día,
pasó de **640.990 b a 2.391 b con `captcha`**. Cinco sondas seguidas, resultado idéntico: no era
intermitencia. **El sitio no había cambiado su política — nos limitó a nosotros.**

Un detector que se corre a cada rato genera sus propios falsos positivos, y un detector ruidoso se
ignora, que es la peor forma de fallar. El script marca ese patrón (desplome de tamaño + captcha
nuevo) como **PROBABLE AUTO-BLOQUEO** para que no se confunda con un cambio real, pero la
disciplina de no abusar es lo que de verdad lo evita.

**Si sale AUTO-BLOQUEO: esperar unas horas y repetir ANTES de tocar la matriz.**

## Changelog
- **SF3.1** (2026-08-02) — **`scripts/verificar_fuentes.py`: la matriz deja de ser una foto.**
  Ataca el problema de fondo que quedaba abierto — todo estaba medido, pero una sola vez, y su
  caducidad dependía de que alguien se acordara. Ahora hay una huella grabada por fuente y un
  comparador. Honestidad de diseño: **es detector de cambio, no de funcionamiento**, porque una
  firma anti-bot por HTTP no prueba que el navegador falle (caso Amazon). Lo que no puede correr
  (Firecrawl y navegador, que son MCP) lo emite como checklist con parámetros y resultado esperado,
  en vez de simular que los cubre.
- **SF3.0** (2026-08-02) — **Modo 4 (CAPTCHA) + el CANDADO ejecutable + matriz por navegador.**
  (a) **Nuevo modo de fallo que rompía la verificación existente:** MercadoLibre CO devuelve un
  muro de captcha y el extractor inventa `"Producto 1".."Producto 8"` con precios y ratings falsos
  — **con `metadata.title` POBLADO y campo `json` presente**, así que los checks 1 y 2 pasaban en
  verde. Tells nuevos: `/captcha/` en la url, título de muro, valores secuenciales de plantilla.
  (b) **`scripts/candado_scraping.py`**: las 4 verificaciones dejan de ser prosa que hay que
  recordar y pasan a ser un script que devuelve PASA/REVISAR/DESCARTAR con código de salida.
  **Probado contra los 4 fallos reales del manual: los caza los 4 y deja pasar el bueno.**
  (c) **Matriz por navegador, medida:** Amazon ✅ (48 tarjetas, 34 con contador de ventas, precios
  en COP, total 155) · Temu ❌ muro de sesión · MercadoLibre ❌ muro de sesión · Reddit ❌ bloqueado.
  Esto **corrige una afirmación no verificada de SF2.0** ("para Temu y Amazon usar Chrome MCP"):
  cierta para Amazon, falsa para Temu. Se escribió por deducción, no por ejecución — el mismo error
  que esta casa corrige en todas partes, cometido dentro del propio manual anti-errores.
  (d) **yt-dlp fuera de YouTube:** TikTok da metadatos (49.400 vistas, 986 likes) pero **cero
  comentarios**. La minería de comentarios es, hoy, solo de YouTube.
- **SF2.0** (2026-08-01) — **Regla Cero ampliada de 1 a 3 modos de fallo tras probar 3 sitios más.**
  El check de `metadata.title` de SF1.0 solo cazaba el Modo 1: Temu y TikTok fallan con title
  poblado (Modo 2, señuelo/redirección) y Amazon falla con title poblado Y sin redirección
  (Modo 3, sin campo `json`). Se añade la verificación que sí caza los tres: **"el dato responde
  a lo que pedí?"**. + Matriz de fuentes medida (AliExpress ✅ · Temu ❌ · Amazon ❌ · TikTok ❌) que
  **corrige la sobre-generalización de SF1.0**, la cual dio por bueno el scanner de volumen en las
  tres tiendas habiendo probado solo una. + `firecrawl_map` verificado (y el aviso de que un map
  vacío no prueba ausencia). + `firecrawl_monitor` verificado como disponible, sin crear ninguno.
  + `yt-dlp` INSTALADO y probado: 30 comentarios con `like_count`. + Nota de inmunidad de `rawHtml`.
- **SF1.0** (2026-07-31) — Creación. Alucinación en páginas huecas, timeout de json+actions, scroll
  infinito resuelto con actions+markdown, coste, postprocesador de YouTube, ausencia de comentarios.
