---
name: golden-shopify
description: >-
  Construye, adapta y recolorea páginas de producto Shopify de alta conversión
  para venta CONTRA ENTREGA (COD con Releasit COD Form) y/o pago anticipado.
  Plantilla base = PRODUCTO DEMO (el build más completo, sobre Shrine Pro), adaptable a
  Dawn ("plantilla down", el tema que se enseña/regala), Sense y cualquier tema
  (la mayoría de bloques son custom-liquid y portables).
  Trabaja con DOS PERFILES sobre un mismo motor: "marca propia" (manifiesto,
  historia, línea de productos) y "catálogo/dropshipping" (escalera de combos,
  demostración y comparativa obligatorias, reglas de copy de dropshipping).
  Úsala SIEMPRE que el usuario quiera: crear o mejorar una landing/página de
  producto, armar un product.json o product.<tema>.json, adaptar una página de
  un cliente a otro tema, cambiar la marca/colores de una plantilla, agregar
  countdown, sticky bar, garantía, barra logística, reseñas, FAQ, manifiesto,
  combos/bundles, pirámide/"cómo actúa", precio dinámico, botón Releasit, o
  resolver dudas de carrito/Releasit/COD. También cuando venda un producto de
  Dropi o de catálogo público y necesite diferenciarse por oferta y por página. Dispara aunque no digan "plantilla down": basta con
  "página de producto", "landing de producto Shopify", "tema Dawn/Shrine/Sense",
  "contra entrega", "Releasit", "COD", o que peguen un product.json con bloques
  custom_liquid. NO usar para análisis de anuncios ni temas no-Shopify.
---

# GOLDEN SHOPIFY (`golden-shopify`)
<!-- skill G4.3 · 2026-08-07 (centro de mando, cosecha del chat un estudio de producto): componente estándar "LO QUE ESTE PRODUCTO NO HACE" para verticales de SALUD, descrito junto a sec-disclaimer/sec-es-para-ti como obligatorio-recomendado — declara el límite del producto con honestidad (ej. "no repara una caries ya formada; sí cuida el esmalte") y convierte la objeción "es estafa" en razón de compra en categorías donde los competidores usan avales inventados y estadísticas sin estudio; el mismo mensaje se replica en pauta y en la respuesta pública de comentarios · G4.2 · 2026-08-07 (fuente: chat otro producto/otro producto): TOPE 50 KB por setting custom_liquid (punto 9 del RESUMEN DURO + check obligatorio en auto-check.md) + límites duros y RECETA PROBADA Horizon/Pitch (horizon-bloques.md) + fallback permanente del CTA a /cart/add si Releasit falta (REGLA #2 + releasit-cod.md) + nota [DEUDA] product.base.json en 17 vs 24 secciones; G4.1 · fix 2026-07-27: resumen del PROTOCOLO TEMA VIVO subido al tope (un chat recibió la skill truncada y trabajó sin él — lo crítico va ARRIBA); G4.0 · PERFILES (marca propia | catálogo-dropshipping) + embudo canónico de 24 secciones + bloque alternado imagen-texto + revelado seguro (el CTA nunca se oculta) + video lazy + srcset + schema SEO-AIO en sección propia; historial completo en references/changelog.md -->

> 🔒 **SKILL CANÓNICA — SOLO-LECTURA.** Estos archivos están protegidos (read-only) a propósito.
> Se pueden LEER y usar libremente, pero **NO se editan desde fuera de la "fábrica"** (el chat del
> usuario dedicado a mejorar la skill). Prohibido a otras sesiones/linters/absorciones modificarla.
> Para cambiarla: el usuario la desbloquea en la fábrica, se edita, y se vuelve a bloquear.

## 🚨 PROTOCOLO TEMA VIVO + MEDIA — RESUMEN DURO (leer ANTES de escribir a cualquier tema)
*Versión completa al final de este archivo (sección "PROTOCOLO TEMA VIVO + MEDIA"). Si este archivo te llegó cortado y no ves esa sección, reléela del disco: `~/.claude/skills/golden-shopify/SKILL.md` desde la línea ~460.*
1. **Verificar QUÉ tema es MAIN** antes de tocar nada (`{themes{nodes{name role id}}}`) — el vivo cambia entre sesiones sin aviso.
2. **Escritura**: `themeFilesUpsert` body `{type:"BASE64"}`; tras escribir, RELEER y comparar contenido. UNA sola sesión escribe por tema.
3. **Caché storefront**: la página pública puede servir el render viejo 15-60 min — verificar el ARCHIVO del tema, no re-subir a ciegas.
4. **NUNCA borrar media de producto sin inventariar referencias** (`/files/` lo incrustan plantillas, Releasit, renders); un borrado se rescata re-subiendo con el MISMO filename.
5. **Galería**: mínimo 5 imágenes 1:1; `galeria_portada_al_final` (Dawn Golden) es diseño APROBADO, no "corregirlo".
6. **CSS prohibido**: jamás `html,body{overflow-x:clip}` — mata el scroll vertical; el desborde se arregla en el elemento culpable.
7. **Releasit**: el Sticky Bar NUNCA se desactiva en el panel (se oculta por CSS) y el botón se prueba PULSÁNDOLO (abrir el modal).
8. **Media de la ficha vive en el TEMA y en la DESCRIPCIÓN del producto** (descriptionHtml) — un barrido/parche de media mira ambos. **Video de contenido: `poster` OBLIGATORIO** (sin poster + sin autoplay = recuadro en blanco que simula sección vacía) y el autoplay se comprueba con play() o teléfono real, nunca desde el panel del navegador. GIF pesado (>1 MB) → convertir a MP4 `<video autoplay muted loop playsinline>` (caso real: 23,5 MB → 3,3 MB).
9. **TOPE DURO: cada setting `custom_liquid` admite máximo 50 KB** — aplica a TODOS los temas, no solo a Horizon/Pitch. Al pasarse, el guardado revienta con *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"* (descubierto con `FileSaveError` en tienda real, chat otro producto 2026-08-07). Medir CADA valor en **bytes UTF-8, no caracteres**, antes de entregar (verificación obligatoria en `references/auto-check.md`); si una pieza se acerca al tope, partirla en secciones más pequeñas (una sección por pieza, REGLA #5).

Sistema para generar páginas de producto Shopify de alta conversión COD. Nació
del proyecto interno "plantilla down" (tema **Dawn**) y se probó en dos productos
reales: **MARCA DEMO** (perfume, Dawn) y **PRODUCTO DEMO** (vitalidad, Shrine Pro).

**Idea central:** NO es "clonar un archivo". Es un sistema de **componentes
`custom-liquid` portables** + un **adaptador de tema** para las pocas piezas
nativas que cambian entre Dawn / Shrine / Sense. Por eso ~80% del trabajo sirve
igual en cualquier tema; solo se adapta el ~20% nativo (tickers, footer, bloques
`title`/`description`/`related-products`).

**Plantilla BASE = PRODUCTO DEMO** (`assets/product.base.json`). Es el archivo más evolucionado
del sistema (config center "PALETA & MARCA", `PRICE_CONFIG`, `RELEASIT_BUTTON_CONFIG`,
override de color Releasit con MutationObserver). Está construido sobre **Shrine Pro**;
para Dawn/Sense se adapta con `references/temas.md`. Todo producto nuevo PARTE de esta
base, sin importar el tema final.

> ⚠️ **[DEUDA G4.x]** `assets/product.base.json` **sigue en el orden de 17 secciones vs las 24 del
> embudo canónico G4.0 — pendiente de sesión dedicada para regenerarlo.** Hasta entonces, la
> referencia canónica de ORDEN es la tabla del embudo en este SKILL.md, NO el base. El base sigue
> siendo válido como motor (config center, Releasit, precio), pero nadie debe usarlo creyendo que
> su orden de secciones está al día. (Detectado en el chat otro producto, 2026-08-07.)

## ⚠️ REGLA #1 — Cada página DEBE ser distinta (innegociable)
Dos productos NUNCA quedan como la misma página con otro color/fotos. La base PRODUCTO DEMO
aporta el **motor** (Releasit, precio, config center, convención), NO el **aspecto**.
El diseño visible se **rediseña por producto**: distinto orden/selección de secciones,
sección educativa única, hero distinto, tipografía por vertical, paleta propia del
producto, efectos repartidos, layouts de reseñas/FAQ variados. Antes de entregar, aplica
el **chequeo antiespejo** de `references/diferenciacion.md` (si quitando color e imágenes
se parece a una página previa, cambia al menos 3 palancas). Lo que sí se mantiene
constante: motor COD, convención de código, config-driven, reglas de oro y calidad.

## ⚠️ REGLA #2 — El botón de compra SIEMPRE sobresale (innegociable)
El botón de compra (CTA principal) tiene que ser el **elemento más visible y de mayor
contraste** de toda la página: debe destacar sobre TODOS los colores (secciones, fondos,
botones secundarios). Reglas permanentes:
- **COLOR FIJO: verde ganador `#1D9E06`** (`CTA_BG` del config center; oscuro `#157A04`).
  Es SIEMPRE este verde, en todo producto, salvo que el usuario pida otro expresamente.
  Aplica al botón principal y al sticky. (Excepción a la paleta por-producto: el resto de
  la página cambia de color según el producto, pero el CTA se mantiene en este verde porque
  es el que más convierte.)
- Más grande, peso fuerte, con su `shine sweep`/realce; el sticky inferior repite ese
  mismo color para que el cliente lo identifique al instante.
- Botones secundarios (ver más, info) en estilo discreto, jamás compiten con el CTA.
- **Chequeo de 1 vistazo:** el ojo va directo al botón de compra? Si no, súbele
  contraste/tamaño. Aplica también en móvil.
- **El CTA siempre FUNCIONA, aunque Releasit falte (regla permanente G4.2, toda página, no solo
  Horizon):** el botón de compra lleva **fallback al formulario nativo `/cart/add`**. Si Releasit
  no está presente en la página (app desinstalada, bloqueada o que no inyectó), el clic espera
  ~1,5 s por si la app inyecta tarde y luego agrega el producto por `/cart/add` y lleva al carrito.
  Antes, sin Releasit, el botón no hacía nada — un CTA muerto en la última puerta. Detalle e
  implementación en `references/releasit-cod.md`.

**CTA verde vs WhatsApp verde (resuelto):** el CTA es verde ganador `#1D9E06` (vivo/oscuro)
y el WhatsApp es verde `#25D366` (más claro) — son **tonos distintos** y además difieren en
forma/tamaño/posición/ícono (CTA = barra grande con texto; WhatsApp = burbuja redonda
flotante). NO se confunden. Mantener el WhatsApp siempre `#25D366` (convención) y no pegarlo
justo al lado del CTA.

## ⚠️ REGLA #3 — Nunca dejar vacío: reseñas de ejemplo SÍ; datos de riesgo se confirman (innegociable)
La página SIEMPRE se entrega **llena y funcionando**. Está PROHIBIDO dejar cualquier sección o
bloque **vacío o con placeholder visible** (`[RATING]`, `[N] reseñas`, "sé el primero", arrays
vacíos, `0.0/5`). Nada en blanco llega al cliente.

**MATIZ PAUTA (2026-07-29, gaceta 4f punto 3):** en fichas que reciben pauta, el rating/reseñas del
display propio SE QUEDAN (doctrina de FER), pero JAMÁS: porcentajes tipo "X% de usuarias/satisfacción"
presentados como dato de estudio, testimonios quemados en IMÁGENES con nombre/estrellas, ni atribución
a terceros ("verificado por Google/nadie externo").

**Reseñas y rating (cuando el cliente NO los tiene todavía) → INVENTAR ejemplos buenos:**
- 5–6 reseñas variadas, con **nombres locales** y **alguna de 4★** para que se vean creíbles.
- Un **rating creíble** (ej. `4.8 · 127 reseñas`).
- TODO marcado en comentario como `EJEMPLO — reemplazar por reales`, para que el cliente los
  cambie cuando tenga los suyos. Nunca se deja la sección de reseñas vacía ni el rating en placeholder.

**Honestidad SOLO en datos de riesgo legal** — estos se **CONFIRMAN, no se inventan** como reales:
- **Precios, descuentos, `compare_at_price`** (se leen del producto; no hardcodear).
- **Tiempos de entrega** (dependen del país — ver `paises-entrega.md`).
- **Claims médicos / resultados / certificaciones / INVIMA / ingredientes.**
- **Specs duras** (mAh, voltajes, medidas, materiales) — ej. la `sec-ficha-tecnica`.
Para estos: preguntar de forma concreta y, mientras falte, dejar un placeholder evidente
(`[confirmar]`) **solo en ese dato puntual** — nunca un número de riesgo que parezca real.

La línea es clara: las **reseñas de ejemplo** no son un riesgo legal (se marcan reemplazables);
los **datos de arriba** sí lo son. El **JSON-LD `aggregateRating`** (lo que Google indexa) se
mantiene condicional al conteo REAL — los ejemplos de reseñas son solo visuales en la página,
no se inyectan como estructura a Google (fix de G2.2).

## ⚠️ REGLA #4 — Completitud: NUNCA entregar algo mediocre o incompleto (innegociable)
El usuario parte normalmente DE CERO y quiere una plantilla **hiper ganadora**, no una ficha.
Toda página entregada DEBE traer **TODO el sistema** — todos los bloques y secciones que
manejamos — sin que falte ninguno. La variación (REGLA #1) está en el **orden, estilo,
layout y copy**, NUNCA en quitar piezas de conversión.

**Set mínimo OBLIGATORIO en cada página** (presentación distinta, pero presentes siempre):
config center · propuesta/hero · título · oferta · **countdown real** (evergreen ~15 min) ·
**verificado/rating lleno** (ejemplo reemplazable si no hay real — REGLA #3) · **precio dinámico** ·
botón Releasit (motor, oculto) · **CTA verde + doble CTA** · **garantía COD en humano** · barra
logística (país correcto) · descripción · **sticky** · sección educativa propia del producto ·
**escalera de venta / demo** · **reseñas llenas** (5–6, ejemplos reemplazables si no hay reales) ·
manifiesto (si aplica al arquetipo) · FAQ · **por qué elegir?** · **banda de autoridad** ·
ficha técnica (en gadget/kit) · tickers · **botón flotante WhatsApp** · sello + nota interna.
(Ver checklist de página ganadora en `references/arquetipos.md` y `references/checklist-producto.md`.)

- Los **arquetipos** cambian el ÉNFASIS y el orden, no si los bloques existen. "Salud lean"
  = estilo sobrio, NO = página incompleta.
- **Prohibido** declarar una página "lista/100" si le falta cualquiera de estos elementos o
  si no la viste renderizada (Regla 0 / render visual).
- Si algo no aplica de verdad a ese producto, **dilo explícitamente** ("omito X porque…"),
  no lo dejes faltando en silencio.

## ⚠️ REGLA #5 — Bloques independientes y apagables; nada abierto (innegociable)
Mucha gente que usará la plantilla NO sabe editar código. Por eso:
- **Cada efecto/función = SU PROPIO bloque.** Prohibido meter 2-3 cosas en un solo bloque
  (ej. el viejo "propuesta" traía hero+ignition+header+cart+SEO → se separó en 5 bloques).
  Así cada uno se **apaga/prende solo** desde el editor de Shopify (el "ojo" del bloque).
- **Nada de bloques "abiertos"** que el usuario tenga que rellenar con Liquid/HTML o "pega tu
  video aquí". Todo bloque llega **funcionando y completo**. Si se necesita un video/imagen,
  usar una **sección NATIVA del tema** (que cualquiera sabe usar), NUNCA un slot de código.
- **El intro IGNITION** es bloque propio, **apagable**, y **distinto en cada página**
  (cinematográfico, 100% CSS) — ver `references/ignition-variantes.md`. Nunca el mismo dos veces.
- Al construir, numera y nombra los bloques claro para que el usuario los identifique y togglee.

## ⚠️ REGLA #6 — Ninguna animación puede esconder lo que vende (innegociable, G4.0)
Aprendido en producción: una página con revelado al scroll dejó secciones enteras invisibles
porque el `IntersectionObserver` no disparó, y el cliente se quedó mirando huecos en blanco.
- **El botón de compra, el sticky y las imágenes NUNCA entran en el revelado.** Van marcados
  con `!important` fuera de la animación. Si todo lo demás falla, el cliente igual puede comprar.
- **Toda animación de entrada lleva red de seguridad por tiempo:** a los ~1.2 s, lo que no se
  haya revelado se fuerza visible. Nunca se depende solo del observer.
- **Sin JS, la página se ve completa.** El revelado es opt-in por una clase en `<html>` que
  pone el propio script; si el script no corre, no se oculta nada.
- Mismo principio que la salida del Ignition (nunca solo-CSS) y que el sticky anclado al `<body>`.
Motor listo en `componentes/efx-reveal-seguro.liquid`. Ninguna página nueva escribe su propio
revelado: usa ese.

## Modo landing sin distracciones (recomendado para COD)
Para que el visitante no se vaya y solo pueda comprar, **ocultar el menú del header y el
footer** en la página de producto (solo en el PDP, no en toda la tienda). Usar
`componentes/landing-sin-distracciones.liquid` (oculta menú/header/footer, desactiva el
link del logo al home, y oculta el "Ir directamente al contenido"). Útil sobre todo
cuando el home aún no está configurado. Nota: el "skip to content" solo lo ve quien
navega con teclado/editor, no el cliente con mouse.

## Cuándo usar cada modo

1. **Producto nuevo desde cero** → clonar un ejemplo base y rellenarlo.
2. **Adaptar la página de un cliente** que ya viene en otro tema → detectar el
   tema, conservar lo suyo, inyectar/ajustar nuestros componentes.
3. **Solo recolorear / cambiar marca** de una plantilla existente.
4. **Agregar UN componente** (countdown, garantía, etc.) a una página existente.
5. **Actualizar una página a la versión actual** (upgrade pass) — ver abajo.

Pregunta al usuario qué modo necesita si no es obvio.

## Modo actualización (UPGRADE PASS)
Para poner al día un `product.json` ya generado (*"actualiza este JSON a la última versión"*):
leer su sello `GFS_VERSION` → diff contra la skill → aplicar solo lo que falta sin romper lo
que sirve → subir el sello → entregar un solo archivo. **Pasos detallados en `references/operacion.md` (A).**

## Preguntas iniciales (pedir SIEMPRE antes de construir)

1. **Tema** de la tienda — 2 familias (adapto TODO el código al que indiques):
   - **Clásica (product.json pega):** Dawn · Shrine / Shrine Pro · Sense.
   - **Nueva (product.json NO pega → bloques Custom Liquid sueltos):** Horizon · Pitch.
   - Otro → fallback genérico. Detalle y reglas por tema en `references/temas.md`.
2. **PERFIL — marca propia o catálogo público?** (CRÍTICO, define secciones y tono):
   - **`marca`** → el producto es tuyo o de un cliente con marca real. Entran manifiesto,
     historia/origen y línea de productos. Vendes identidad y recompra.
   - **`catalogo`** → viene de un catálogo público (Dropi y similares) y otras tiendas
     venden lo mismo. La **escalera de combos es obligatoria**, la demostración es la
     protagonista, y aplican las reglas de copy de dropshipping (nunca "original"/"réplica").
   Si no lo dice y no se deduce, **pregúntalo**. Detalle completo en `references/perfiles.md`.
3. **Producto**: nombre + **URL** (ver regla "La URL es CONTEXTO" abajo).
   Pregunta también: **la URL es tu tienda o es una referencia/competencia?** (cambia el
   anti-duplicado).
4. **PAÍS de venta** (CRÍTICO — define los tiempos de entrega de la landing).
   Guatemala / Colombia / otro. Ver `references/paises-entrega.md`. Si el país no
   está en la tabla, **pregúntale al cliente** los tiempos reales. NUNCA poner fechas
   de un país en otro (ej. no usar los 1-4 días de Guatemala para Colombia).
5. **Colores**: pregunta si el cliente tiene color de marca.
   - Si lo tiene → úsalo de `primary` y deriva dark/bright/light.
   - Si NO, o pide recomendación → **recomienda tú** un color enfocado al producto:
     el que más vende / más persuade / más genera impulso de compra para ese vertical
     (ver `references/colores-conversion.md`). Propón 1 recomendado + 1 alternativa.
6. **Modo de pago**: `ambos` (default) / `contraentrega` / `anticipado`.
7. **WhatsApp**: número con código de país — se integra al **botón flotante de WhatsApp**
   (`componentes/whatsapp-flotante.liquid`) y al config center.
8. **Reviews** (cantidad + rating) si los tiene.
9. **Imágenes — PREGUNTAR SIEMPRE: CON o SIN generación?** (define todo el flujo de assets)
   - **CON generación:** genero imágenes reales con **Nano Banana Pro** (Gemini API key,
     modelo `gemini-3-pro-image`), optimizo a **<300 KB**, las subo a Shopify Files por API y
     las dejo en **bloques de la landing + galería/multimedia del producto**.
   - **SIN generación (el cliente ya tiene imágenes):** pedir las **URLs/links** o **reutilizar
     la galería/multimedia del producto**. No tocar la descripción.
   - Si pide generar y NO hay API/herramienta conectada → avisar en 1 línea y seguir con slots.
   - El **producto REAL nunca se inventa** (REGLA #3): el frasco se *compone* desde su foto real.
   Pipeline completo + troubleshooting en `references/imagenes.md`.

Si falta alguno de estos datos, **pregúntalo explícitamente** antes de construir.

## Workflow

### Paso 0 — PLAN DE DIFERENCIACIÓN (obligatorio, ANTES de escribir JSON)
Para que cada producto tenga su propia cara (REGLA #1), antes de construir **declara
explícitamente** este plan y muéstralo en una línea por punto:
- **Arquetipo** elegido (A Perfume / B Salud lean / C Vitalidad full) y por qué encaja.
- **Orden y selección de secciones** (distinto del flujo por defecto cuando se pueda).
- **Hero** (image_banner / propuesta full / título XXL / otro).
- **Sección educativa** específica de ESTE producto (pirámide / cómo actúa / comparativa /
  antes-después / pasos / ingredientes…).
- **Pairing tipográfico** (según vertical, ver `efectos-premium.md`).
- **Set de efectos** que SÍ se usan (no meter siempre los mismos).
- **Color primario + color del CTA** (justificado por conversión, REGLA #2).

Reglas del plan:
- **Compara contra los ejemplos** (`examples/demo-dawn-v2.json` ⭐ la plantilla PRO recomendada,
  `examples/demo-shrine.json`, `examples/demo-dawn.json`)
  y contra cualquier página que el usuario te muestre o que esté en
  `~/.claude/SHOPIFY BY CLAUDE/PLANTILLAS/`. El plan DEBE divergir de ellas.
- Si construyes **varios productos en una misma sesión**, cada plan debe pulsar **palancas
  distintas** a los anteriores (no repetir arquetipo+orden+hero idénticos).
- Si el usuario arma productos en chats separados, **pídele** (o revisa en PLANTILLAS) las
  páginas previas para no repetirlas.
Solo después de fijar el plan, sigue al Paso 1. Ver `references/diferenciacion.md`.

### Paso 0.0 — La URL es CONTEXTO, NO tu página (clave)
Cuando el usuario manda una URL, **no asumas que es suya ni que es el diseño a copiar**.
Puede ser **su tienda, la de un competidor, o solo una referencia** para que entiendas el
producto. Úsala SOLO para extraer **contexto del producto**: qué es, para qué sirve,
beneficios, ingredientes, público, objeciones, ángulo de venta → para **adaptar el copy** con
información real (apoya la REGLA #3 anti-invención).
- **NUNCA** clones el diseño de esa URL, ni limites/bajes la calidad de la plantilla a lo que
  esa página tenga. Tú construyes **desde cero** una plantilla completa y ganadora (REGLA #4).
- **NUNCA** copies reseñas/claims de un competidor como si fueran del usuario.
- Si es competencia, además sirve para **diferenciarte y superarla**, no para imitarla.

### Paso 0.1 — Anti-duplicado (solo si la URL ES la tienda del usuario)
Si la URL **es del usuario** y su descripción nativa YA trae landing completo (hero,
comparativas, "cómo usar", reseñas, garantía), **no dupliques** ese contenido: cambia el
ángulo o desactiva esa sección nuestra; reseñas propias = personas distintas. Si la URL es
**referencia/competencia**, esto no aplica: construyes la página completa desde cero.

### Paso 1 — Partir de la base PRODUCTO DEMO y adaptar al tema
SIEMPRE parte de `assets/product.base.json` (la base PRODUCTO DEMO, la más completa). Luego:
- Tema **Shrine / Shrine Pro** → ya estás en el tema nativo de la base, sigue directo.
- Tema **Dawn** → aplica el adaptador de `references/temas.md` (tickers→custom-liquid,
  footer `.footer`, quita settings Shrine-only). Usa `examples/demo-dawn.json`
  como referencia viva de cómo queda en Dawn.
- Tema **Sense / otro** → como Dawn, + fallback genérico de `temas.md`.

Lee `references/temas.md` para saber exactamente qué cambia entre temas.

### Paso 2 — Config center + recolorear (TOKENIZADO)
Inserta el **config center** como primer bloque del main (`BRAND_NAME`, colores `BRAND_*` +
`*_RGB`, `CTA_BG`, WhatsApp, reviews). **Recolorear = cambiar esas variables** (los componentes
leen `var(--brand-*)` / `var(--cta)` del `:root`; sin search-replace). CTA fijo `#1D9E06`.
Recalcula los `*_RGB` al cambiar un color. Detalle y tokenización de páginas viejas en `references/sistema.md`.

### Paso 3 — Config-driven blocks
Ajusta los bloques que SÍ tienen config propia:
- **Precio** → `window.PRICE_CONFIG` (`06-precio-dinamico.liquid`).
- **Botón Releasit + sticky** → `window.RELEASIT_BUTTON_CONFIG` (override de
  colores de los botones de la app). Ver `references/releasit-cod.md`.
- **Garantía / Compra Segura** → variable `MODE` = `ambos|contraentrega|anticipado`.

### Paso 4 — Contenido por producto
Antes de escribir copy, lee `references/reglas-de-oro.md` (copy emocional COD, qué
NUNCA decir en perfumes/dropshipping, garantía por proceso). Para agregar o reforzar
efectos visuales, usa `references/efectos-premium.md`. Reescribe el copy específico:
- Propuesta de valor (`01-propuesta.liquid`).
- Sección educativa: "Cómo actúa" / pirámide olfativa / etc.
  (`sec-como-actua.liquid`) → **siempre se reemplaza por producto**.
- Reseñas (`sec-resenas.liquid`, array `window.GFS_REVIEWS`).
- FAQ (`sec-faq.liquid`), manifiesto, beneficios.

### Paso 5 — Activar/desactivar y ordenar
- **Countdown**: oculto por defecto (`disabled: true`).
- **Releasit COD app block**: SIEMPRE incluido pero **oculto** (`disabled: true`)
  — es el MOTOR del COD, NO se borra. Lo dispara nuestro botón custom.
- **Productos relacionados**: última posición, desactivado por defecto.
- **Compra Segura**: `MODE="ambos"` por defecto.
- Numera bloques (1..N) y secciones (1..N) consecutivos.

### Paso 6 — Entregar UN solo archivo
Entrega un único `product.<slug>.json` (o `product.<slug>.<tema>.json`). **Regla
del usuario: un solo archivo por producto.** No crear variantes `.MEJORADO`,
`.LEAN`, etc. Si pide cambios, editar el mismo archivo y reentregar.

Antes de entregar: corre la **auto-verificación** de `references/auto-check.md` (script que
atrapa JSON roto, color viejo, rating 0.0, sin sello, sin Ignition, sin Releasit) **y** la
**checklist** de `references/checklist-producto.md`. No declares la página lista si algo falla.

## Convención de código en cada bloque (mantener SIEMPRE)
Cada bloque `custom-liquid` separa lo editable de lo que no se toca:
```liquid
{% comment %} 📝 EDITAR AQUI {% endcomment %}
{% assign VARIABLE = "valor" %}
{% comment %} ═══ ↓ NO TOCAR DE AQUI HACIA ABAJO ↓ ═══ {% endcomment %}
<style>...</style><div>...</div>
```
Cualquier bloque nuevo sigue este patrón. El usuario edita arriba; el motor vive abajo.

> ⚠️ **REGLA DE INGENIERÍA (innegociable):** antes de escribir CUALQUIER bloque o sección,
> cumple **`references/estandares-liquid.md`** — código **sano** (scope con prefijo único BEM +
> tokens de la Paleta con fallback, nada hardcodeado), **accesible** (WCAG 2.2: roles/ARIA, foco,
> contraste, `alt`, labels, `aria-live`) y **rápido** (`content-visibility`, `lazy`+dimensiones sin
> CLS, animar solo `transform`/`opacity`, `prefers-reduced-motion`, JS vanilla con progressive
> enhancement). Ningún bloque se entrega sin pasar su **checklist "código sano"**. Para **temas
> Horizon o tiendas nuevas**, consulta además **`references/horizon-bloques.md`** (arquitectura
> block-based + theme blocks nativos).

## Estructura canónica = EMBUDO CON RITMO (G4.0 — 24 secciones, 4 puertas, PAS + neuroventa)
La página NO es una lista de secciones: es un **embudo con ritmo** donde **cada fase pide la venta** y,
a quien no compra, la siguiente lo recupera atacando **la objeción exacta**. El blueprint completo con
los principios de neuroventa está en `references/reglas-de-oro.md` (Regla 0-A).

**Cambio estructural de G4.0** (absorbido de la página real en producción, que ya iba en 24 mientras
la skill seguía documentando 17):
- **Candado, Ignition y WhatsApp salen del main y pasan a ser SECCIONES sueltas.** Son overlays
  `position:fixed` o CSS puro: su orden no afecta al layout, y como secciones el cliente las
  prende y apaga sin entrar a los bloques del producto.
- **El cuerpo de la landing se construye con `sec-bloque-alternado.liquid`** (imagen + texto, el
  lado alterna). Menos texto, más imagen, y la página respira sola.
- **El schema JSON-LD vive en su propia sección invisible** (`sec-seo-aio-schema.liquid`), no
  dentro del FAQ: si el cliente apaga o mueve el FAQ, el SEO sobrevive.
- **3 tickers** (arriba, medio, abajo) en vez de 2: el del medio es el respiro entre las dos
  mitades pesadas del embudo.

| # | Fase | Sección | Trabajo | Puerta |
|---|---|---|---|---|
| — | Sistema | **Candado landing** (sección) | Sin salidas al home | |
| — | Sistema | **Ignition** (sección) | Intro cinematográfico, 1 vez por sesión | |
| — | Sistema | **WhatsApp flotante** (sección) | Canal directo, siempre visible | |
| 1 | Atención | Ticker superior | Micro-confianza (envío gratis · contra entrega) | |
| 2 | Oferta | **HERO/main** (galería+título+oferta+precio+**CTA#1**+logística+sticky) | Cierre del comprador caliente | **🚪1** |
| 3 | Problema | Dolor · público A | El cliente se reconoce | |
| 4 | Problema | Dolor · público B *(solo si hay 2 públicos reales)* | El otro perfil se reconoce | |
| 5 | | **CTA#2** (`sec-cta-suelto`) | Cierra al que ya se vio retratado | **🚪2** |
| 6 | Confianza | **Seguridad · objeción #1** | Desactiva el miedo ANTES de las features | |
| 7 | Solución | Mecanismo / cómo actúa | El "ajá" | |
| 8 | Respiro | Ticker medio | Corta entre las dos mitades pesadas | |
| 9 | | **CTA#3** (`sec-cta-suelto`) | Pico de convicción | **🚪3** |
| 10 | Demostración | Secuencia / demo / escalera | Verlo funcionando | |
| 11 | Alcance | Variantes o usos *(si el producto los tiene)* | Cada quién encuentra el suyo | |
| 12 | Uso | Modo de uso | Baja la fricción del "y cómo se usa" | |
| 13 | Calificación | Es para ti | Auto-selección → menos devoluciones | |
| 14 | Prueba social | Reseñas | Confianza de otros | |
| 15 | Respiro | Ticker inferior | | |
| 16 | Oferta | **Escalera de combos** (`sec-combos`) | Sube el ticket. **Obligatoria en `catalogo`** | |
| 17 | Riesgo→0 | Envío + garantía | Reversión de riesgo justo antes del cierre | |
| 18 | Cierre | **CTA final** (`sec-cta-suelto`) | Última puerta | **🚪4** |
| 19 | Objeciones | **FAQ** | El último "pero" cuando ya lo quiere | |
| 20 | Legal | Disclaimer | Ligero, cumplimiento | |
| 21 | SEO/AIO | **Schema invisible** (`sec-seo-aio-schema`) | Google + buscadores con IA | |

**Por PERFIL** (ver `references/perfiles.md`):
- **`marca`** añade manifiesto, historia/origen y línea de productos; la escalera de combos es opcional.
- **`catalogo`** quita manifiesto e historia, y hace **obligatorias** la escalera de combos, la
  demostración y la comparativa.

**Estado por defecto en producción** (aprendido de la página real): countdown, garantía-bloque y
descripción nativa van **apagados** cuando ya hay una sección que hace ese trabajo mejor. No es que
sobren: es que duplicados restan.

**Off por defecto** (ruido / condicional): autoridad (cifras placeholder), ficha técnica, related-products.
WhatsApp flota (posición indiferente) + Sticky siempre visible.

- **Cadencia de CTA:** una puerta cada 2-3 secciones — todas disparan
  `#custom-releasit-btn`. El **FAQ baja a antes del cierre** (G2.6): las objeciones solo importan
  cuando ya hay deseo, así que se resuelven tras la prueba social y justo antes del último CTA.
  La **tranquilidad COD inmediata** (garantía + "pagas al recibir" + logística) ya vive en
  *Riesgo→0* dentro de `main`, así que el comprador caliente no necesita la FAQ arriba.
- **Activos por defecto** (antes off/sueltos): escalera, doble CTA, autoridad, por qué elegir?,
  CTA del manifiesto. **Ficha técnica** va incluida pero **apagada** (solo gadget/kit; sus specs
  son datos duros `[confirmar]` → no se envían activas, REGLA #3).
- **Bloques del main:** config center · propuesta · ignition · título · oferta · countdown ·
  verificado · precio · **CTA #1 Releasit** · garantía · barra logística · **descripción** · sticky.

> ✅ Los ejemplos `examples/demo-shrine.json` y `examples/demo-dawn-v2.json` están **sincronizados
> con la arquitectura actual (G3.8+)**. Aun así, la referencia de orden canónica es **`product.base.json`**;
> ante cualquier duda base-vs-ejemplo, gana el base.
>
> ⚠️ **[DEUDA G4.x] — excepción vigente al párrafo anterior:** `assets/product.base.json` **sigue en
> 17 secciones vs las 24 del embudo canónico — pendiente de sesión dedicada.** Mientras no se
> regenere, para el ORDEN de secciones manda la **tabla de arriba** (embudo G4.0 de 24), no el base;
> el base solo gana en el motor y la config de cada bloque. (Chat otro producto, 2026-08-07.)

Antes del Paso 1, elige **arquetipo** por vertical (define énfasis/orden, no si los bloques
existen — REGLA #4): A) Perfume · B) Salud lean · C) Vitalidad full · D) Gadget/Demo · E) Kit.
Matriz completa en `references/arquetipos.md`.

## PLAYBOOK DE GENERACIÓN (0 → 1000) — la receta para una página PERFECTA
No entregues un esqueleto con copy demo. Una página 1000 tiene TODO el copy escrito para ESTE
producto y coherente de arriba a abajo. Sigue estos pasos SIEMPRE:

**Paso 0 · Datos reales primero (nunca inventar — REGLA del usuario).** Antes de generar, ten:
nombre del producto, forma (spray/gotero/crema/parche…), ingrediente/USP estrella, precio y precio
tachado, WhatsApp real con código de país, país (tiempos de entrega), rating+nº reseñas, y si tiene
o no aval legal real. Si falta algo que cuesta render o es un claim, **PREGUNTA** (no inventes).

**Paso 1 · Centro de control (PALETA & MARCA).** Cambia BRAND_NAME, los 4 colores de marca
(BRAND_PRIMARY/DARK/BRIGHT/LIGHT + sus RGB), WHATSAPP_NUMBER real, REVIEW_COUNT y RATING_VALUE.
El CTA se queda VERDE (Regla #2). Toda la página hereda estos tokens.
⚠️ **OJO con los textos que NO son `{% assign %}`:** el botón Releasit (`RELEASIT_BUTTON_CONFIG.text`)
y el sticky traen el nombre del producto **dentro de un objeto JS** (ej. "QUIERO MI PRODUCTO DEMO").
Reescríbelos con el nombre real o quedan como fósil demo (el auto-check #18 lo caza).

**Paso 2 · Reescribe el copy de CADA sección para el producto** (cero copy demo — auto-check lo caza):
- **Tickers:** 3 beneficios COD/producto por ticker (envío gratis, contra entrega, USP). Nada de
  "energía/vitalidad"; nada que el producto NO haga (ej. "lunares" si no trata lunares).
- **Hero:** badge-gancho + subtítulo con la promesa y la USP ("con [ingrediente estrella]…").
- **Te suena / Ya lo intentaste:** 4 escenas del dolor real + 4 alternativas que ya falló (PAS).
- **Cómo actúa:** 3 pasos con el VERBO correcto de la forma (spray→rocía) y la USP en el paso 2.
- **Escalera:** 5 paneles problema→solución→beneficio→USP→resultado. Kickers variados (no repetir).
- **Cine:** 3-4 líneas de future-pacing ("imagina…") + CTA.
- **Reseñas:** 3-6 testimonios CREÍBLES con nombre, específicos del producto (nunca vacío — inventa
  ejemplos buenos si no hay reales, y ponlos a reemplazar).
- **Timeline:** qué esperar por etapas, realista ("varía según la persona").
- **Es para ti:** 4 SÍ + 4 "consulta antes" (incluye lo que NO trata → baja devoluciones + da confianza).
- **Por qué elegir / FAQ / Manifiesto:** comparación, 5 objeciones reales, cierre emocional identitario.
- **Disclaimer:** cosmético/legal. Claims (INVIMA/registro) solo si son REALES; si no lo necesita,
  enfoque positivo ("por sus características no requiere registro"), nunca "no tiene registro".

**Paso 3 · Imágenes — golden-shopify es el CEREBRO (ver `references/imagenes-orquestacion.md`).**
Tú decides el plan visual y **repartes** cada pieza al generador correcto (no las generas aquí):
- **Infografía (foto real + texto de venta) → `golden-imagen-arena`** (MCP de Higgsfield por API; SOLO imágenes).
- **GIF / video / demo / persona → `golden-ugc-avatar`** (Higgsfield).
- **Foto photoreal / escena sin texto → Nano Banana** (pipeline de `imagenes.md`).
Produce un **BRIEF VISUAL** (tabla: slot · ubicación · formato · generador · foto fuente · TEXTO dentro ·
propósito), confirma el set con el usuario (cada pieza gasta créditos de Higgsfield) e invoca la skill
generadora con SUS filas — ella sabe CÓMO, tú le das el QUÉ. Formatos: galería **1080×1080**,
descripción **solo 1-3** infografías **1080×1350**, escalera `P#_IMG` **1:1**, cine fondo **16:9**/video.
Escalera y Cine usan **URLs NUEVAS**, nunca las infografías de la descripción (se duplicarían). El resto
de la venta = **bloques nativos** (SEO + editable + liviano). WebP <150KB, con width/height + alt (sin CLS).

**Paso 4 · Coherencia de producto (Regla 0-C).** La forma manda el verbo en TODAS las secciones;
la USP lidera el mecanismo; no vender lo que no trata; un solo WhatsApp; claims solo si reales.

**Paso 5 · Cierre.** Corre `references/auto-check.md` (JSON válido, cero fósiles, candado, FAQ a11y,
relacionados off, sin fugas `{# #}`). Luego **RENDER REAL** (subir a tema no publicado + screenshot
móvil Y escritorio) antes de decir "listo". Nunca "1000/1000" sin verla con ojos.

## Sello de versión + NOTA INTERNA (OBLIGATORIO en cada página)
Cada página lleva: (1) **sello arriba** en el config center (`GFS_VERSION` + comentario HTML
con versión/marca/fecha) y (2) **nota interna al FINAL** (comentario HTML invisible con la
fecha y hora REALES de generación, fijas, dentro del último bloque — NUNCA tras el `}` final).
**Formato exacto y reglas en `references/operacion.md` (B).**

## ⚠️ PROTOCOLO TEMA VIVO + MEDIA (absorbido 2026-07-25, obligatorio antes de escribir)
1. **Verificar QUÉ tema es MAIN antes de tocar nada** (`{themes{nodes{name role id}}}`): el tema
   vivo puede cambiar entre sesiones sin aviso (pasó: otro chat publicó Dawn y los parches se
   estaban subiendo al borrador). Nunca asumir el tema por memoria.
2. **Escritura fiable**: `themeFilesUpsert` con body `{type:"BASE64"}`; tras escribir, RELEER el
   archivo y comparar contenido (no fiarse del OK ni del tamaño). Una sola sesión escribe por tema.
3. **Caché del storefront**: tras cambiar plantillas o media, la página pública puede servir el
   render VIEJO 15-60 min (por URL, incluso con cache-buster). Si un fix "no aparece": verificar
   el ARCHIVO del tema, no re-subir a ciegas; esperar la purga.
4. **Borrar media de producto = romper URLs**: los product media viven en `/files/` y otros
   consumidores los incrustan (plantillas, constructores, config de upsells de Releasit, renders
   cacheados). ANTES de borrar: inventariar referencias y reemplazarlas; el archivo borrado se
   puede rescatar del caché del CDN re-subiéndolo con el MISMO filename (la URL revive).
5. **Galería estándar Golden**: mínimo 5 imágenes por producto, TODAS cuadradas 1:1 (portada
   packshot + tarjetas de beneficios + macros; reutilizables entre productos de la familia).
   La portada va posición 1 en Admin (colecciones/búsqueda); si el tema trae
   `galeria_portada_al_final` (Dawn Golden), la ficha abre con los creativos y el packshot
   cierra — es diseño aprobado, NO "corregirlo".
6. **CSS prohibido**: jamás `html,body{overflow-x:clip}` (clip contagia el otro eje y MATA el
   scroll vertical). Un desborde horizontal se arregla en el elemento culpable (ej. ticker
   marquee con `overflow:hidden;max-width:100%`), nunca en html/body.
7. **Sticky/Releasit**: nunca desactivar el Sticky Bar en el panel de Releasit (rompe el botón en
   silencio); se oculta por CSS (`_rsi-buy-now-button-floating`) y toda ficha conserva SIEMPRE un
   CTA fijo propio. Probar el botón DE VERDAD (abrir el modal), no solo que exista.

## Auto-mejora — RITUAL DE ABSORCIÓN
Cuando el usuario diga *"absorbe las mejoras de esta página"* o pegue un `product.json` que le
gustó: parsear → diff contra base+componentes → extraer lo nuevo/mejor como componente → subir
versión en `changelog.md` → confirmar en una línea. **Nunca degradar, un componente por función,
y NUNCA reintroducir nombres reales** (usar descriptores de categoría; la skill es anónima).
**Pasos detallados en `references/operacion.md` (C).**

## Archivos de esta skill
- `references/reglas-de-oro.md` — **copy/legal + 12 reglas de oro + tabla de errores. LEER SIEMPRE.**
- `references/perfiles.md` — **G4.0: los 2 perfiles (marca propia | catálogo-dropshipping): qué secciones entran en cada uno, qué tono y qué reglas de copy. LEER antes del Paso 0.**
- `references/diferenciacion.md` — **REGLA #1: palancas para que cada página sea distinta + chequeo antiespejo.**
- `references/ignition-variantes.md` — **REGLA #5: intro Ignition distinto por página (8 variantes CSS).**
- `references/arquetipos.md` — **3 arquetipos de página + matriz de componentes por vertical.**
- `references/paises-entrega.md` — **tiempos de entrega por país (Guatemala/Colombia). NUNCA mezclar.**
- `references/colores-conversion.md` — **cómo recomendar el color que más vende por vertical.**
- `references/estandares-liquid.md` — **ESTÁNDARES DE CÓDIGO LIQUID (original): arquitectura section/block/snippet + schema, CSS BEM/tokenizado con fallback, JS progressive, rendimiento y accesibilidad WCAG 2.2 + checklist "código sano". LEER antes de escribir cualquier bloque.**
- `references/horizon-bloques.md` — **arquitectura block-based del tema HORIZON (theme blocks nativos, `@theme`/`@app`, `block.shopify_attributes`, presets anidados) y cuándo usar Horizon vs `custom_liquid`. Para tiendas nuevas o migración.**
- `references/rendimiento.md` — **velocidad de carga: fuentes, imágenes, JS, CSS + checklist. LEER al construir.**
- `references/imagenes.md` — **imágenes: producto real (lo da el usuario) vs infografías-en-HTML vs decorativo-IA; hosting en Shopify; slots.**
- `references/imagenes-orquestacion.md` — **CEREBRO de imágenes: reparto golden-imagen-arena (infografías) / golden-ugc-avatar (video/GIF) / Nano Banana (photoreal); el BRIEF VISUAL como contrato de sincronización; matriz de formatos por ubicación.**
- `references/sistema.md` — el sistema de componentes + estado del config center.
- `references/temas.md` — **adaptador Shrine (base PRODUCTO DEMO) → Dawn / Sense / fallback**.
- `references/releasit-cod.md` — override de botones Releasit, MODE, MutationObserver.
- `references/efectos-premium.md` — catálogo de snippets (3D, glass, partículas, manifiesto, tilt, contadores).
- `references/checklist-producto.md` — checklist final antes de entregar.
- `references/auto-check.md` — **auto-verificación ejecutable de cierre (script). Correr antes de entregar.**
- `references/changelog.md` — **historial de versiones / mejoras absorbidas.**
- `references/operacion.md` — **detalle de: modo actualización (A), sello + nota interna (B), ritual de absorción (C).**
- `references/componentes/*.liquid` — cada componente real, listo para pegar. Incluye
  `sec-piramide.liquid` y, de la auditoría de la tienda real (v1.19), las **secciones de
  página ganadora**: `sec-escalera.liquid` (storytelling alternado imagen+texto/GIFs, el
  motor de venta de productos de demostración), `sec-por-que-elegir.liquid` (trust-grid de 4
  íconos personalizado al producto) y `sec-autoridad.liquid` (banda de prueba social de marca).
  Desde v1.30: `sec-cta-mid.liquid` (**doble CTA a media página**, verde, sombra suave) y los
  fixes de `12-sticky-bar.liquid` / `whatsapp-flotante.liquid` (anclados al `<body>`).
  **Desde G3.1 (fusión con la línea "GOLDEN FULL") — vertical SALUD/estética:**
  `sec-disclaimer.liquid` (**disclaimer legal**: cosmético ≠ medicamento + contraindicaciones; flag
  de registro/INVIMA solo si es REAL) y `sec-es-para-ti.liquid` (**"es para ti?" + seguridad**:
  califica al cliente y lista cuándo NO usar / consultar antes). **Ambos son OBLIGATORIOS en
  productos de salud/estética COD** (protección legal, REGLA #3).
  **Desde G4.3 (cosecha del un estudio de producto, 2026-08-07) — componente estándar
  "LO QUE ESTE PRODUCTO NO HACE"** (obligatorio-recomendado en verticales de SALUD, junto a
  `sec-disclaimer` / `sec-es-para-ti`): sección de 3-5 líneas que declara el LÍMITE del producto
  con honestidad brutal ("No repara una caries ya formada — eso lo hace el dentista. Sí cuida el
  esmalte y apoya la remineralización"). **Racional probado en campo:** en categorías donde todos
  los competidores usan odontólogo inventado, logos de cadenas como "distribuidores oficiales" y
  estadísticas sin estudio (95%/96%/97%/100%), **declarar el límite convierte la objeción "esto es
  una estafa" en la razón para comprar** — el único vendedor honesto de la categoría se queda con
  el cliente escéptico, que es la mayoría. Se maqueta como `custom-liquid` con el patrón de
  `sec-es-para-ti` (lista ❌ "no hace" / ✅ "sí hace") y su mensaje se replica en el ángulo de
  pauta y en la respuesta pública de comentarios (mismo texto, tres soportes).
  **Desde G4.0 (absorbidos de la página real en producción):**
  `sec-bloque-alternado.liquid` (**el patrón dominante del cuerpo de la landing**: imagen + texto
  con el lado alternando; PC en 2 columnas, móvil apilado, imagen con `srcset` y sin CLS) ·
  `sec-seguridad.liquid` (**la objeción #1 resuelta ANTES de las features** — una de las secciones
  que más convierte y casi nadie tiene) · `sec-dolor-segmentado.liquid` (dos secciones de dolor,
  una por público, cuando el producto le habla a dos perfiles con dolores distintos) ·
  `sec-combos.liquid` (**escalera de combos 1/2/3 con razón de uso**; obligatoria en perfil
  `catalogo`) · `sec-cta-suelto.liquid` (**el CTA reutilizable de las puertas 2, 3 y 4**, con
  fallback a scroll si el botón principal no existe; reemplaza a `sec-cta-mid.liquid`) ·
  `sec-seo-aio-schema.liquid` (**JSON-LD en sección invisible propia**, sobrevive a que apaguen el FAQ) ·
  `efx-reveal-seguro.liquid` (**motor de revelado con red de seguridad**: el CTA y las imágenes
  NUNCA se ocultan, y a los 1.2 s todo lo no revelado se fuerza visible) ·
  `efx-video-lazy.liquid` (video de demostración con `data-src` + poster WebP: no descarga nada
  hasta que se acerca al viewport).
- `assets/product.base.json` — **PLANTILLA BASE (PRODUCTO DEMO), el master a clonar.**
- `assets/config-center.liquid` — el bloque config center para insertar.
- `assets/related-products.premium.css.txt` — CSS premium para featured-collection.
- `examples/demo-dawn-v2.json` — ⭐ **PLANTILLA PRO v2 (Dawn) — la referencia recomendada:** embudo
  completo de impulso (countdown activo, escalera con imágenes reales, doble CTA, autoridad,
  manifiesto, FAQ), sticky/WhatsApp anclados al body, sin sombra dura, slots de imagen. (v1.30)
- `examples/demo-dawn.json` — referencia previa de adaptación a **Dawn** (v1).
- `examples/demo-shrine.json` — copia de la base en **Shrine Pro**.

## Roadmap v2 (fuera de v1, no implementar salvo que lo pidan)
- **Trust badges** como fila de sellos reutilizable.
- **TICKER_CONFIG** para parametrizar textos de los tickers.
- **Tema "Golden"** (custom, en desarrollo) — documentar sus selectores cuando exista.
- ✅ ~~Tokenizar colores~~ HECHO en v1.14 (recolorear = cambiar variables del config center).
