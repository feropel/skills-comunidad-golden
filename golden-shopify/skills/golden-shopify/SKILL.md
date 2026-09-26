---
name: golden-shopify
description: >-
  Construye, adapta y recolorea páginas de producto Shopify de alta conversión para venta
  CONTRA ENTREGA (COD con Releasit COD Form) y para pago anticipado. Plantilla base =
  PRODUCTO DEMO (el build más completo, sobre Shrine Pro), adaptable a Dawn ("plantilla
  down", el tema que se enseña o se regala), Sense y cualquier tema, porque la mayoría de
  bloques son custom-liquid y portables. Trabaja con DOS PERFILES sobre un mismo motor:
  "marca propia" y "catálogo o dropshipping". Úsala SIEMPRE que el usuario quiera: crear o
  mejorar una landing o página de producto, armar un product.json o product.tema.json,
  adaptar la página de un cliente a otro tema, cambiar la marca o los colores de una
  plantilla, agregar countdown, sticky bar, garantía, barra logística, reseñas, FAQ,
  manifiesto, combos, pirámide o "cómo actúa", precio dinámico, botón Releasit, o resolver
  dudas de carrito, Releasit o COD. También cuando venda un producto de Dropi o de catálogo
  público y necesite diferenciarse por oferta y por página.
---
# GOLDEN SHOPIFY (`golden-shopify`)
<!-- skill G4.27 · 2026-09-05 (revalidacion con metodo de OTRA FAMILIA, ley del CdM): el check del disparador tenia un FALSO NEGATIVO EN PRODUCCION que el banco no podia ver. En la tienda viva los espacios del `text=` viajan como `+` (?text=Hola+quiero+informacion+...), y el patron con \s no casaba: un mensaje mal escrito pasaba invisible. El banco saboteaba con espacios LITERALES, o sea su formato no era el de produccion. Ahora se decodifica con unquote_plus antes de juzgar, y el banco lleva el caso real copiado del enlace vivo. -->
<!-- skill G4.26b · 2026-09-05: el arreglo de G4.26 creo un falso NEGATIVO y lo cazo el banco. Al apuntar el check solo al enlace de WhatsApp, el patron cortaba en el primer ESPACIO — y el mensaje del disparador lleva espacios, asi que capturaba 'wa.me/...?text=Hola,' y perdia lo que habia que juzgar. El href se corta en la COMILLA, no en el espacio. Sin el caso malo en el banco, habria entregado un check que ya no cazaba nada. -->
<!-- skill G4.26 · 2026-09-05 (disfraz de golden-presenta, medido con DELTA contra control): el check del disparador acusaba al texto por su FORMA y no por su AUTORIDAD. Un <pre><code> que documenta el error, un <script application/json> de config y un atributo data-* lo disparaban: los tres tienen la forma exacta y cero mando, y marcarlos castiga a quien documenta el fallo. Ahora solo mira dentro del enlace wa.me/api.whatsapp.com, que es donde el disparador MANDA de verdad. La pregunta no es como esta escrito, sino sobre quien manda. -->
<!-- skill G4.25b · 2026-09-05: el caso disfrazado cazo DOS falsos positivos en su primera corrida. Los checks 2 (hex huerfano) y 22 (disparador) miraban `allcl` —todo el liquid, comentarios incluidos— mientras 18/25/27/28 ya miraban solo lo visible: un ACTA en un comentario los encendia. La funcion compartida existia y dos consumidores no la usaban. Ahora `visible_txt` se calcula UNA vez y la usan todos los checks de contenido. -->
<!-- skill G4.25 · 2026-09-05 (refinamiento de golden-ads via CdM): CASO DISFRAZADO en la autoprueba. El lado bueno era prosa inocente, y prosa cualquiera no mueve casi ningun contador; lo que prueba un detector es texto que SE PARECE al dato. Nuevo caso: un ACTA con los cinco patrones prohibidos a la vez (disparador mal escrito, apertura, raya, lenguaje de tienda, hex huerfano) DENTRO de un comentario Liquid — no debe disparar ninguno, y de paso prueba la funcion compartida solo_visible() contra sus cuatro consumidores en un solo caso. -->
<!-- skill G4.24 · 2026-09-05 (fila del CdM dentro del ciclo): DOS CIFRAS CLAVADAS QUE YA MENTIAN. El cuerpo decia '24 secciones = 21 + 3' cuando el generador declara 34 (22 activas, 12 apagadas por defecto), y '12 reglas de oro' cuando hay 9. Sustituidas por el ARCHIVO QUE LAS MIDE. Ademas, aviso del margen de la description (~1008 de 1024) donde se lee, porque las 38 fabricas estan afinando disparadores esta noche y pasarse deja la skill invalida en silencio. MEDIDO Y NO MUDADO: el peso del cuerpo es PROCEDIMIENTO, no acta — el Workflow son 7 pasos ejecutables. -->
<!-- skill G4.23 · 2026-09-05 (ciclo de automejora, mandato v2): TECHO DE NITIDEZ. La skill mandaba galeria a 1080x1080 para todo, y Shopify **achica pero NUNCA agranda** (medido: width=2048 sobre un original de 1088 devuelve 1088). Esa regla plana ponia techo PERMANENTE de nitidez en la galeria de cada ficha de la casa. Corregido a tamano POR DESTINO con un criterio unico: si Shopify transforma esa imagen (galeria 2048, ~300 KB) o si viaja tal cual (descripcion y secciones, <150 KB). 4 archivos tocados, 0 menciones de 2048 antes. -->
<!-- skill G4.22 · 2026-09-05 (autocalificacion, mandato de FER): la reserva que costaba -10 se CERRO EJERCIENDOLA. El candado ampliado en G4.20 se probo en tiendas reales que NO son Dawn: Impulse 9.0.0 y Prestige 11.4.0, control antes/despues, y OCULTA en las dos. El dato que valida la ampliacion: el header de Impulse es `.site-header`, uno de los selectores anadidos en G4.20 — sin ella no habria ocultado nada. Debut, Booster y Ella quedan SIN verificar: sus demos ya no se publican en el theme store. Cobertura declarada: 3 familias medidas, 3 sin demo accesible. -->
<!-- HISTORIAL COMPLETO en `references/changelog.md` — aqui solo viven los sellos VIGENTES. Los 21 anteriores se mudaron alli el 2026-09-05 (auditoria golden-skill-auditor): se cargaban en cada activacion y eran la causa unica del aviso de tamano del validador. -->
<!-- skill G4.21 · 2026-09-05 (auditoria golden-skill-auditor, reparacion): el SKILL.md cargaba 24 sellos de version en comentarios (50 de 550 lineas) y 23 ya estaban en references/changelog.md. Ese historial duplicado se leia entero en CADA activacion y era la causa UNICA del aviso del validador oficial (cuerpo 534, recomendado <500). Mudado al changelog (nada se borro: el bloque del CdM, que no estaba alli, se copio tal cual). Quedan los sellos vigentes + la doctrina de los dos ejes. -->
<!-- skill G4.20 · 2026-09-04 (la skill se comparte y corre sobre el tema de OTRA persona): el tema ya estaba cubierto en references/temas.md ('preguntar SIEMPRE', 2 familias) pero NO era compuerta de arranque — el Paso 0 solo exigia el cerebro de marca — y el protocolo asumia acceso por API, que un VIP en su propio Claude puede no tener. Nuevo Paso 0-A: el tema se DECLARA antes de generar, y se MIDE desde la URL publica (Shopify.theme.schema_name da la familia real aunque el tema este renombrado) antes que preguntarlo. Ademas el candado asumia la familia Dawn: sus 13 selectores no cubrian Debut/Impulse/Prestige/Booster/Ella y fallaba EN SILENCIO. -->
<!-- skill G4.19 · 2026-09-03: la doc no decia COMO correr los validadores. En G4.10 el encabezado nuevo nunca entro porque el patron buscaba 'Auto-verificacion' y el archivo dice 'Auto-verificación' CON TILDE: el reemplazo no fallo, simplemente no hizo nada, y el changelog lo dio por hecho. Ocho versiones con la doc rota. Regla nueva en 0-H: tras editar se verifica que el texto nuevo ESTA, no que el comando salio sin error. -->
<!-- skill G4.18 · 2026-09-03 (fila del CdM): la description llevaba `product.<tema>.json` y la spec de publicacion PROHIBE los angulares — no era longitud (1010 de 1024). El arreglo son dos caracteres; la causa de fondo no: esta skill validaba a fondo el product.json que PRODUCE y no se validaba A SI MISMA como artefacto publicable, aunque se publica al marketplace. La autoprueba ahora corre el validador OFICIAL de skill-creator sobre esta skill. -->
<!-- DOS EJES DE VERSIÓN (no confundir, no son desincronía): (a) VERSIÓN DE LA SKILL = este sello + references/changelog.md, con sufijos a/b/c/d por ronda de auditoría; (b) GFS_VERSION = lo que se estampa en la PÁGINA GENERADA (config-center + componentes/00 + product.base.json), y solo sube cuando cambia lo que la página produce. La versión VIGENTE de cada eje se lee de su fuente, no de esta nota: la de la skill en el sello de arriba + references/changelog.md, y GFS_VERSION en assets/config-center.liquid. Al bumpear, tocar TODAS las caras del eje que cambió (y ninguna del otro). -->

> ⚠️ **LA `description` VA AL LÍMITE: mide ~1008 de 1024 duros.** Si le añades un disparador,
> **revalida DESPUÉS** con `agentskills validate <RUTA ABSOLUTA>` (con `.` da falso negativo).
> Pasarse la deja INVÁLIDA en silencio. Lo explicativo baja al cuerpo, que no tiene tope duro.
>
> 🔒 **SKILL CANÓNICA — SOLO-LECTURA.** Estos archivos están protegidos (read-only) a propósito.
> Se pueden LEER y usar libremente, pero **NO se editan desde fuera de la "fábrica"** (el chat del
> usuario dedicado a mejorar la skill). Prohibido a otras sesiones/linters/absorciones modificarla.
> Para cambiarla: el usuario la desbloquea en la fábrica, se edita, y se vuelve a bloquear.
> **Fábrica: chat `✅ SKILL golden-shopify`** — titularidad declarada aquí, no solo en memoria
> (REGISTRO-FABRICAS.md). Solo la fábrica numera esta skill (ley del número de versión).

<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->
## Paso 0-A · QUE TEMA ES (compuerta: no se genera nada sin esto)
Esta skill construye **sobre el tema de OTRA persona**. Si se asume Dawn y la tienda corre otra
familia, lo que se entrega no encaja — y en el peor caso encaja a medias, que es peor porque parece
bien. **Antes de escribir una sola linea, el tema queda DECLARADO.** Tres vias, en este orden:

1. **MEDIRLO desde la tienda publica** (no hace falta API ni permisos: basta la URL). En el HTML de
   cualquier tienda Shopify vive `Shopify.theme`, y lo que manda es **`schema_name`**, no `name`:
   `name` es el rotulo que le puso el dueno ("Mi tienda v2") y no dice nada; **`schema_name` dice la
   FAMILIA real** aunque lo hayan renombrado.
   ```js
   // pegar en la consola de la tienda, o leerlo del HTML publico
   ({familia: Shopify.theme.schema_name, version: Shopify.theme.schema_version, rotulo: Shopify.theme.name})
   ```
2. **Por API**, si hay MCP/credencial: `{themes{nodes{name role id}}}` — y ademas el tema MAIN cambia
   entre sesiones sin avisar, asi que se relee cada vez (`references/tema-vivo.md`).
3. **Preguntarle al usuario**, si no hay ni URL ni API: *"Que tema usa la tienda? Si no lo sabes,
   mandame la URL y lo miro yo."*

**Nunca se asume Dawn.** Si las tres vias fallan, se dice en la entrega que el build se hizo a ciegas
sobre familia clasica y que hay que verificarlo antes de publicar. El reparto por familia y las
diferencias de cada una estan en `references/temas.md` (clasica: Dawn/Shrine/Sense, el product.json
pega · nueva: Horizon/Pitch, NO pega y va por bloques Custom Liquid).

## Paso 0 · Cerebro de marca (obligatorio antes de generar)
El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta de la ruta la declara
`golden-brand-brain`: ante duda de ruta, invócala en vez de adivinar.

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.

## 🚨 PROTOCOLO TEMA VIVO + MEDIA — RESUMEN DURO (leer ANTES de escribir a cualquier tema)
*Detalle completo en `references/tema-vivo.md` (si este archivo te llegó cortado, léelo del disco).*
1. **Verificar QUÉ tema es MAIN** antes de tocar nada (`{themes{nodes{name role id}}}`) — el vivo cambia entre sesiones sin aviso.
2. **Escritura**: `themeFilesUpsert` body `{type:"BASE64"}`; tras escribir, RELEER y comparar contenido. UNA sola sesión escribe por tema.
3. **Caché storefront**: la página pública puede servir el render viejo 15-60 min — verificar el ARCHIVO del tema, no re-subir a ciegas.
4. **NUNCA borrar media de producto sin inventariar referencias** (`/files/` lo incrustan plantillas, Releasit, renders); un borrado se rescata re-subiendo con el MISMO filename.
5. **Galería**: mínimo 5 imágenes 1:1; `galeria_portada_al_final` (Dawn Golden) es diseño APROBADO, no "corregirlo".
6. **CSS prohibido**: jamás `html,body{overflow-x:clip}` — mata el scroll vertical; el desborde se arregla en el elemento culpable.
7. **Releasit**: el Sticky Bar NUNCA se desactiva en el panel (se oculta por CSS) y el botón se prueba PULSÁNDOLO (abrir el modal).
8. **Media de la ficha vive en el TEMA y en la DESCRIPCIÓN del producto** (descriptionHtml) — un barrido/parche de media mira ambos. **Video de contenido: `poster` OBLIGATORIO** (sin poster + sin autoplay = recuadro en blanco que simula sección vacía) y el autoplay se comprueba con play() o teléfono real, nunca desde el panel del navegador. GIF pesado (>1 MB) → convertir a MP4 `<video autoplay muted loop playsinline>` (caso real: 23,5 MB → 3,3 MB).
9. **TOPE DURO: cada setting `custom_liquid` admite máximo 50 KB** — aplica a TODOS los temas, no solo a Horizon/Pitch. Al pasarse, el guardado revienta con *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"* (descubierto con `FileSaveError` en tienda real, chat Insulinum 2026-08-07). Medir CADA valor en **bytes UTF-8, no caracteres**, antes de entregar (verificación obligatoria en `references/auto-check.md`); si una pieza se acerca al tope, partirla en secciones más pequeñas (una sección por pieza, REGLA #5).

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

> ✅ **`assets/product.base.json` regenerado al embudo canónico de 24 (G4.5)** — vuelve a ser la
> referencia de ORDEN ya construida, además del motor (config center, Releasit, precio).

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
- **Compara contra los ejemplos** (`references/examples/demo-dawn-v2.json` ⭐ la plantilla PRO recomendada,
  `references/examples/demo-shrine.json`, `references/examples/demo-dawn.json`)
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
  footer `.footer`, quita settings Shrine-only). Usa `references/examples/demo-dawn.json`
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

## Estructura canónica = EMBUDO CON RITMO (4 puertas de CTA, estructura PAS)
La página NO es una lista de secciones: es un **embudo con ritmo** donde cada fase pide la venta.
**El conteo NO se clava aquí, se MIDE** en `assets/product.base.json` (secciones del `order`, y cuántas nacen `disabled`) — la tabla del embudo vive en `references/embudo-canonico.md`. Clavarlo envejece: esta línea decía 24 cuando el generador ya iba por otra cifra (candado, ignition, WhatsApp: overlays `position:fixed`,
su orden no afecta al layout). **4 puertas de compra:** HERO (CTA#1) · tras el dolor (CTA#2) ·
pico de convicción (CTA#3) · cierre (CTA final). Blueprint de neuroventa: `references/reglas-de-oro.md` (Regla 0-A).

> 📖 **Tabla fila por fila, perfiles (`marca` | `catalogo`), estado por defecto y cadencia de CTA:**
> **`references/embudo-canonico.md`**. Ese orden ya viene CONSTRUIDO en `assets/product.base.json`.

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
generadora con SUS filas — ella sabe CÓMO, tú le das el QUÉ. Formatos: galería **2048×2048** (~300 KB —
Shopify ACHICA pero NUNCA agranda: subir 1080 pone techo permanente de nitidez; el detalle medido y la
tabla por destino, en `references/imagenes.md`),
descripción **solo 1-3** infografías **1080×1350**, escalera `P#_IMG` **1:1**, cine fondo **16:9**/video.
Escalera y Cine usan **URLs NUEVAS**, nunca las infografías de la descripción (se duplicarían). El resto
de la venta = **bloques nativos** (SEO + editable + liviano). WebP con width/height + alt (sin CLS);
el peso va POR DESTINO: <150 KB donde Shopify NO transforma (descripción, secciones), ~300 KB en galería.

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

## PROTOCOLO TEMA VIVO + MEDIA — version completa
El **resumen duro de 9 puntos esta al inicio de este archivo** (obligatorio antes de escribir a un tema).
Detalle completo, con el porque de cada punto y los casos reales: **`references/tema-vivo.md`**.

## Auto-mejora — RITUAL DE ABSORCIÓN
Cuando el usuario diga *"absorbe las mejoras de esta página"* o pegue un `product.json` que le
gustó: parsear → diff contra base+componentes → extraer lo nuevo/mejor como componente → subir
versión en `changelog.md` → confirmar en una línea. **Nunca degradar, un componente por función,
y NUNCA reintroducir nombres reales** (usar descriptores de categoría; la skill es anónima).
**Pasos detallados en `references/operacion.md` (C).**

## Archivos de esta skill
- `references/breakeven-combos.md` — **Regla 0-F: umbral de rentabilidad ANTES de escribir la escalera de combos (criterio de golden-ads + aritmetica COD)**
- `references/reglas-de-oro.md` — copy/legal + las reglas de oro (el número lo dice el propio archivo) + tabla de errores
- `references/perfiles.md` — G4.0: los 2 perfiles (marca propia | catálogo-dropshipping): qué secciones entran en cada uno, qué tono y
- `references/diferenciacion.md` — REGLA #1: palancas para que cada página sea distinta + chequeo antiespejo.
- `references/ignition-variantes.md` — REGLA #5: intro Ignition distinto por página (8 variantes CSS).
- `references/arquetipos.md` — 3 arquetipos de página + matriz de componentes por vertical.
- `references/paises-entrega.md` — tiempos de entrega por país (Guatemala/Colombia)
- `references/colores-conversion.md` — cómo recomendar el color que más vende por vertical.
- `references/estandares-liquid.md` — ESTÁNDARES DE CÓDIGO LIQUID (original): arquitectura section/block/snippet + schema, CSS BEM/tokenizado c
- `references/horizon-bloques.md` — arquitectura block-based del tema HORIZON (theme blocks nativos, `@theme`/`@app`, `block.shopify_attribut
- `references/rendimiento.md` — velocidad de carga: fuentes, imágenes, JS, CSS + checklist
- `references/imagenes.md` — imágenes: producto real (lo da el usuario) vs infografías-en-HTML vs decorativo-IA; hosting en Shopify; s
- `references/imagenes-orquestacion.md` — CEREBRO de imágenes: reparto golden-imagen-arena (infografías) / golden-ugc-avatar (video/GIF) / Nano Ban
- `references/sistema.md` — el sistema de componentes + estado del config center.
- `references/temas.md` — adaptador Shrine (base PRODUCTO DEMO) → Dawn / Sense / fallback.
- `references/releasit-cod.md` — override de botones Releasit, MODE, MutationObserver.
- `references/efectos-premium.md` — catálogo de snippets (3D, glass, partículas, manifiesto, tilt, contadores).
- `references/checklist-producto.md` — checklist final antes de entregar.
- `references/auto-check.md` — auto-verificación ejecutable de cierre (script)
- `references/changelog.md` — historial de versiones / mejoras absorbidas.
- `references/operacion.md` — detalle de: modo actualización (A), sello + nota interna (B), ritual de absorción (C).
- `references/componentes/*.liquid` — cada componente real, listo para pegar
- `assets/product.base.json` — PLANTILLA BASE (PRODUCTO DEMO), el master a clonar.
- `assets/config-center.liquid` — el bloque config center para insertar.
- `assets/related-products.premium.css.txt` — CSS premium para featured-collection.
- `references/examples/demo-dawn-v2.json` — ⭐ PLANTILLA PRO v2 (Dawn) — la referencia recomendada: embudo
- `references/examples/demo-dawn.json` — referencia previa de adaptación a Dawn (v1).
- `references/examples/demo-shrine.json` — copia de la base en Shrine Pro.

## Roadmap v2 (fuera de v1, no implementar salvo que lo pidan)
- **Trust badges** como fila de sellos reutilizable.
- **TICKER_CONFIG** para parametrizar textos de los tickers.
- **Tema "Golden"** (custom, en desarrollo) — documentar sus selectores cuando exista.
- ✅ ~~Tokenizar colores~~ HECHO en v1.14 (recolorear = cambiar variables del config center).

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Construye, adapta y recolorea páginas de producto Shopify de alta conversión para venta CONTRA ENTREGA (COD con Releasit COD Form) y/o pago anticipado. Plantilla base = PRODUCTO DEMO (el build más completo, sobre Shrine Pro), adaptable a Dawn ("plantilla down", el tema que se enseña/regala), Sense y cualquier tema (la mayoría de bloques son custom-liquid y portables). Trabaja con DOS PERFILES sobre un mismo motor: "marca propia" y "catálogo/dropshipping". Úsala SIEMPRE que el usuario quiera: crear o mejorar una landing/página de producto, armar un product.json o product.<tema>.json, adaptar una página de un cliente a otro tema, cambiar la marca/colores de una plantilla, agregar countdown, sticky bar, garantía, barra logística, reseñas, FAQ, manifiesto, combos/bundles, pirámide/"cómo actúa", precio dinámico, botón Releasit, o resolver dudas de carrito/Releasit/COD. También cuando venda un producto de Dropi o de catálogo público y necesite diferenciarse por oferta y por página. Dispara aunque no digan "plantilla down": basta con "página de producto", "landing de producto Shopify", "tema Dawn/Shrine/Sense", "contra entrega", "Releasit", "COD", o que peguen un product.json con bloques custom_liquid. NO usar para análisis de anuncios ni temas no-Shopify.

