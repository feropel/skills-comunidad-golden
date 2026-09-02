---
name: golden-presenta
description: >-
  Golden Group — PRESENTACIONES CINEMATOGRÁFICAS de un solo archivo HTML, con
  FONDO VIVO (8 atmósferas en WebGL y canvas: nebulosa, aurora, pulso, enjambre,
  retícula, duna, viaje), láminas de cristal con desenfoque, cámara que viaja por
  un lienzo (el efecto Prezi), modo presentador con notas y cronómetro, vista
  general del mapa, salida a PDF y marca parametrizable. CADA PRESENTACIÓN SE VE
  DISTINTA: la atmósfera, la paleta y la tipografía se eligen por el tema del que
  se habla. Cero dependencias externas: no hay CDN que se caiga ni suscripción. Trae verificador ejecutable
  (scripts/verificar_deck.py) que mide contraste real, colisiones de láminas,
  acentos y densidad de texto, y reporta COBERTURA, nunca "quedó perfecto".
  Úsala SIEMPRE que el usuario pida: "hazme una presentación", "un deck", "unas
  diapositivas", "un pitch", "una propuesta para un cliente", "slides para la
  charla", "algo tipo Prezi", "una presentación que se vea cara", "pasa este
  documento a presentación", "material para el MBA o la comunidad", "presentación
  para vender X"; o cuando muestre Prezi, Gamma, Beautiful.ai, Tome o Canva
  Presentaciones como referencia. Dispara también con "mejora este deck",
  "esta presentación se ve fea" o si pega un guion, un esquema o un documento y
  pide convertirlo en presentación.
  NO usar para: página de producto Shopify COD (golden-shopify), sitio web o
  landing (golden-web / golden-cinematica), PDF que NO es presentación
  (golden-pdf-check), ni un .pptx que el cliente deba editar en PowerPoint (skill
  `pptx`) — aunque esta skill sí decide cuándo derivar a esas.
---

# Golden Presenta — el deck como activo propio, no como suscripción

**Versión:** `GP2.0` · Fábrica: chat centro de mando.

<!-- skill GP1.0 · 2026-09-02 · Nace de un encargo de FER: Prezi AI como referencia,
     con la pregunta de si conectarse a su cuenta o replicar el modelo. Medido ese día
     en prezi.com/es/features/ai: su flujo es prompt/archivo -> esquema editable ->
     estilo/paleta, y su foso real son el lienzo con zoom y 160 millones de usuarios,
     no su IA. Decisión: motor propio, porque alquilar el de otro es ser su cliente. -->

## Por qué existe esta skill

Golden ya sabía construir movimiento de cine (`golden-cinematica`), copy que vende
(`golden-copywriting`) y PDFs con estándar (`golden-pdf-check`). Lo que no tenía era el
**motor de navegación de una presentación**: una cámara que viaja por un lienzo, notas
de presentador, mapa general y deep-link por lámina.

Eso es exactamente lo único que hacía falta comprarle a Prezi. Ya no.

## La ley que manda

> **Primero la historia, después la cámara.**

Un deck bonito con un argumento flojo sigue siendo un deck flojo, y el movimiento lo
empeora porque distrae. El orden de trabajo no se negocia: esquema, marca, láminas,
verificación. Quien salta al HTML sin esquema entrega diapositivas con efectos.

La segunda ley la hereda de `golden-cinematica` y aplica igual aquí:
**números, no adjetivos.** "Una transición elegante" no construye nada;
`1100ms cubic-bezier(0.77,0,0.175,1)` sí.

## Paso 0 · Cerebro de marca (obligatorio antes de generar)

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md,
avatares.md, competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO
y genera con esa voz — jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece
crearlo con `golden-brand-brain` antes de continuar; si el usuario pide seguir sin cerebro,
se declara en la entrega que el contenido se generó sin voz de marca cargada.

El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta (buscar con
find ANTES de crear, naming MAYÚSCULAS-CON-GUIONES) la declara `golden-brand-brain`.

## Orden de trabajo (4 fases, ninguna opcional)

### 1 · Esquema
Antes de tocar el HTML, escribe la lista de láminas con una frase por lámina y el tipo de
cada una. Se le muestra al usuario y se ajusta ahí, que es donde cuesta barato cambiarlo.
Los frameworks y los tipos de lámina viven en `references/arquitectura-narrativa.md`.

Regla de tamaño medida: **8 a 12 láminas** para una propuesta comercial, 12 a 20 para una
clase. Menos de 3 no cuenta una historia; más de 25 pierde a la sala.

### 2 · Atmósfera y marca
**Primero se decide de qué habla el deck**, y de ahí salen a la vez el fondo vivo, la
paleta y la tipografía. El mapa completo (tema → atmósfera → paleta → receta de estilo)
está en `references/atmosferas.md`, y es de consulta obligatoria: es lo que impide que
todas las presentaciones se parezcan.

```html
<body data-atmosfera="pulso">   <!-- evento en vivo -->
<body data-atmosfera="aurora">  <!-- formación, MBA -->
<body data-atmosfera="reticula"><!-- datos, panel -->
```

Después se rellena UN solo bloque `:root` y con eso cambia toda la identidad, **fondo
incluido**: las atmósferas se tiñen con `--accent` y `--accent-2`, no traen color propio.
Los cuatro perfiles de Golden están con sus hex exactos en `references/marca-blanca.md`.

Para afinar tipografía y espaciado, se lee **UNA** receta de las 26 de
`web-design-engineer` (nunca el catálogo entero) y se respeta completa, prohibiciones
incluidas. Los nombres de esas recetas jamás salen al cliente.

**Marca blanca:** para un cliente, la identidad es la del CLIENTE. Golden no firma la
lámina, salvo que el cliente lo pida.

### 3 · Láminas
Se parte de `assets/deck-base.html`, se copian los bloques `<section class="slide">` que
haga falta y se colocan en el lienzo. La disposición y las coordenadas están en
`references/motor.md`; los ocho tipos de lámina y su criterio de uso, en
`references/arquitectura-narrativa.md`.

**Disposición por defecto: serpentina.** Filas de 4 láminas, separación 1560 en x y 900 en
y, con la fila par en sentido inverso para que el recorrido sea continuo. Medido a
1280x800: una fila recta de 8 láminas deja la vista general en `scale 0.09` (tira
ilegible); la serpentina 4x2 la deja en `scale 0.18`, que sí se lee como mapa.

### 4 · Verificar (jamás se salta)
```bash
python3 ~/.claude/skills/golden-presenta/scripts/verificar_deck.py /ruta/al/deck.html
```
Corre **hasta 30 comprobaciones**: placeholders sin rellenar, restos de sustitución a
medias, codificación y mojibake,
**palabras escritas sin su tilde en el texto que se ve**, signos de apertura, estructura del
motor, atmósfera declarada y su motor incrustado, dependencias de red, colisiones de
láminas, notas de presentador, densidad de texto y **contraste WCAG real calculado sobre
los hex declarados**.

El número no es fijo y el informe siempre dice cuántas corrió: si el archivo no declara la
paleta en `:root` se saltan las 3 de contraste, y si no es un HTML válido se salta el
bloque de láminas. **Un denominador que baja es en sí mismo una señal**: el archivo está
peor de lo que el resumen sugiere. Por eso se lee la línea "Comprobaciones corridas", no
solo el "pasan".

Y después, **abrir el deck de verdad**: 390 px, 768 px y PC, mirar la consola, avanzar
láminas, entrar en vista general, comprobar que el fondo se mueve. El script lee el
archivo; no ve el render. **Los nueve fallos corregidos al construir esta skill salieron
TODOS de abrirla en un navegador**, ninguno del script — la bitácora está en
`references/motor.md`. Ese es el argumento de por qué esta fase no se salta.

## Qué entrega esta skill

| Salida | Estado | Cómo |
|---|---|---|
| **HTML cinemático de un archivo** | Construida y verificada | `assets/deck-base.html`. Se publica como Artifact, en Vercel o se manda por WhatsApp: corre abriendo el archivo, sin servidor y sin internet |
| **PDF** | Por el navegador | El deck trae `@media print` con una lámina por página y colores reales. Imprimir a PDF desde el navegador. Para un PDF con estándar Golden de documento, encadenar `golden-pdf-check` |
| **.pptx editable** | Derivada | Si el cliente EXIGE editarlo en PowerPoint, se deriva a la skill `pptx`. Este motor no genera .pptx |

## Lo que este motor NO hace (y hay que decirlo antes, no después)

- **No tiene editor visual.** El cliente no arrastra cajas con el ratón. Si el encargo es
  "que el cliente lo edite él mismo sin tocar código", este no es el camino: eso es Canva,
  Google Slides (`gws-slides`) o PowerPoint (`pptx`).
- **No trae biblioteca de imágenes con licencia.** Las imágenes se producen con
  `golden-imagen-arena` o Higgsfield, o las aporta el cliente. Nunca se pega una foto de
  internet sin derechos en un deck que va a un cliente.
- **No hay colaboración en vivo ni encuestas en sala.** Prezi sí las tiene. Si el encargo
  las necesita, se dice y se busca otra herramienta para esa parte.
- **No garantiza que el contenido sea veraz.** Los datos, cifras y citas los verifica una
  persona contra la fuente. El verificador lo declara explícitamente como no verificable.

## Vara de calidad — no se entrega si falla algo de esto

- El verificador corre **sin FALLAS**. Los avisos son decisión del autor; las reglas duras
  de Golden (acentos puestos, sin signos de apertura, sin dependencias de red, ninguna
  lámina por encima de 550 caracteres) son FALLA y bloquean la entrega
- **Se abrió en 390 px, 768 px y PC**, y la consola está limpia
- **Sin scroll horizontal** en ningún ancho (medido: `scrollWidth === innerWidth`)
- **Contraste AA real** del texto principal sobre la lámina, calculado, no estimado
- **Los acentos se ven bien EN PANTALLA**, no solo en el archivo. Y eso incluye los
  `aria-label` y las notas del presentador, que es donde nadie mira
- Cada lámina tiene `data-notas`: un deck sin notas no se puede presentar
- **Una idea por lámina.** Si una lámina pasa de 550 caracteres, se parte en dos
- El deck **arranca aunque la pestaña esté en segundo plano** (verificado: el preloader
  lee el reloj, no acumula ticks)
- **La atmósfera declarada existe y el motor está incrustado** (lo comprueba el verificador)
- **El fondo no compite con el texto.** Si hay que entornar los ojos, pierde el fondo
- **Ninguna lámina sale borrosa en móvil.** El desenfoque de profundidad de campo es del
  modo lienzo y solo de ahí

## Referencias de esta skill

- `references/arquitectura-narrativa.md` — **empieza SIEMPRE aquí.** Cómo se arma el
  esquema, los frameworks por tipo de encargo y los 8 tipos de lámina con su criterio
- `references/atmosferas.md` — **las 8 atmósferas y el mapa tema → fondo → paleta →
  receta.** Se consulta SIEMPRE: es lo que hace que dos decks no se parezcan
- `references/marca-blanca.md` — los 4 perfiles de Golden con hex exactos y su contraste
  medido, y cómo se entrega con la marca de un cliente
- `references/motor.md` — coordenadas, atajos, cómo añadir tipos de lámina, y la
  **bitácora de los 6 fallos medidos** al construir esta skill
- `assets/deck-base.html` — la plantilla funcional. No se reescribe desde cero: se copia
- `assets/atmosferas.js` — el motor de fondos vivos (17 KB, cero red). Fuente única: se
  incrusta en el deck con `scripts/incrustar_atmosferas.py`, nunca se copia a mano
- `scripts/verificar_deck.py` — el auditor. Se corre siempre antes de entregar

## Encadena con

- `golden-brand-brain` → la voz y la identidad (Paso 0, obligatorio)
- `golden-copywriting` → el texto de las láminas de venta. Un deck comercial sin copy de
  respuesta directa es una presentación bonita que no cierra
- `web-design-engineer` → **las 26 recetas de estilo** (paleta, tipografía, espaciado,
  movimiento y prohibiciones) en `references/style-recipes/`. Una por deck, entera
- `golden-cinematica` → de donde salen el preloader y el estándar de movimiento; úsala
  cuando el encargo necesite una escena 3D de verdad (objeto cromado, modelo que rota,
  entorno HDRI). Aquí el fondo acompaña; allí la escena ES la página
- `golden-web/references/estandar-movimiento.md` → los números del movimiento
- `golden-imagen-arena` o Higgsfield → producir las imágenes del deck
- `golden-finanzas` (**agente**, vive en `~/.claude/agents/`) → si el deck es una propuesta
  comercial, los números salen de ahí
- `pptx` → cuando el entregable DEBE ser un PowerPoint editable
- `gws-slides` → cuando debe vivir en Google Slides
- `golden-pdf-check` → si además se entrega un PDF con estándar de documento Golden
- `all-deploy` → publicar el deck con un enlace propio
- `golden-verificador` (**agente**, no skill) → cierre adversarial antes de entregar a un
  cliente. Obligatorio en entregables mayores

## Cuando algo falla o falta (degradación, no bloqueo)

- **El usuario no da los hex de marca:** no se inventan colores a ciegas. Se piden UNA vez
  con la plantilla de `references/marca-blanca.md`; si no los tiene, se extraen del logo o
  del cerebro de marca. Nunca un #000/#fff sin decisión.
- **No hay imágenes para el deck:** se entrega el deck tipográfico (que es la versión que
  mejor envejece) y se declara la imagen como pendiente. No se rellena con banco genérico.
- **El contenido excede 25 láminas:** no se encoge la letra. Se parte en dos decks o se
  mueve el detalle a un documento anexo, y se dice por qué.
- **El verificador reporta contraste bajo:** se corrige el token, nunca se baja el umbral.
  Si el cliente EXIGE su color de marca aunque no llegue a AA, se entrega con el aviso
  escrito de que su paleta no se leerá al fondo de la sala.
- **El encargo real necesita editor visual o colaboración en vivo:** se dice de entrada y
  se deriva, en vez de entregar algo que el cliente no va a poder mantener.

## Changelog

- **GP2.0** (2026-09-02) — **Fondo vivo.** Veredicto de FER sobre GP1.1: "muy plana, le falta
  dinamismo, movimiento, tecnología, fondo, vida", con la orden de desplegar lo que ya
  sabíamos y quizá no estaba instalado. Añadido:
  (1) **motor de 8 atmósferas** (`assets/atmosferas.js`, 17 KB) en **WebGL puro y canvas 2D,
  sin Three.js** — decisión medida: la ley de cero dependencias de red, más el hallazgo del
  Centro de Mando de que un fragment shader de ~1 KB aguanta framerate en móvil donde una
  escena Three.js no. Three.js minificado ronda 600 KB y entra por CDN;
  (2) **láminas de cristal** con `backdrop-filter` y filo de luz, para que el fondo se vea
  a través sin comerse el texto;
  (3) **mapa tema → atmósfera → paleta → receta** en `references/atmosferas.md`, que es lo
  que responde al encargo de que cada presentación sea distinta;
  (4) **enganche con `web-design-engineer`**, 26 recetas de estilo que estaban instaladas y
  que ninguna skill de presentaciones nombraba;
  (5) revelado con desenfoque que se resuelve, en vez de solo opacidad.
  Tres fallos hallados ejecutando en Chrome real con Playwright, ninguno visible en el
  script: el título salía como "MBA Comunidad Golden_TARJETAS" porque `GP_TITULO` es
  prefijo de `GP_TITULO_TARJETAS` y se sustituía a medias (arreglado sustituyendo de la
  clave más larga a la más corta, y añadido un check que caza el resto colgando); y en
  móvil las láminas no activas salían borrosas, primero por el `filter` del `.slide` y
  después por el del revelado escalonado, que es del modo lienzo y se colaba al de flujo.

- **GP1.1** (2026-09-02) — Ronda del agente `golden-verificador` (adversarial, 16 corridas
  del script contra archivos fabricados para romperlo, más Chrome headless en 4 anchos).
  Encontró 10 fallas y **la clase que las une: reglas duras de Golden degradadas a aviso, y
  variables calculadas que nunca llegaban a un `check()`**. Corregido:
  (1) el deck entregable no tenía **un solo acento** en `aria-label`, texto visible ni notas
  de presentador, y el script contaba las tildes sin comprobarlas nunca. Ahora hay un check
  que busca palabras que en español siempre llevan tilde, mirando solo lo que ve el usuario
  (texto, atributos accesibles y cadenas del JS), no el CSS ni los comentarios;
  (2) una lámina sin posición se saltaba el check de notas por un `continue`;
  (3) "sin dependencias externas" solo miraba `<script>` y `<link>`, dejaba pasar `<img>`,
  `<iframe>` y `@import`, y excluía Google Fonts a propósito: ahora mira cualquier
  referencia de red y es FALLA;
  (4) el detector de mojibake usaba controles latin-1 en vez de los caracteres cp1252
  reales y se le colaban 2 de 6 variantes, incluida la comilla curva, que es la más común
  al pegar desde Word;
  (5) los signos de apertura y (6) la densidad de 550 caracteres pasan de aviso a FALLA,
  porque la vara decía "no se entrega" y el script daba exit 0;
  (7) SKILL.md mandaba a `motor.md` por los tipos de lámina, que viven en
  `arquitectura-narrativa.md`;
  (8) contradicción de 8 a 14 contra 8 a 12 láminas en propuesta comercial;
  (9) "26 comprobaciones" se presentaba como fijo siendo variable, y el denominador se
  encoge justo cuando el archivo está peor: ahora se explica como señal;
  (10) `golden-finanzas` y `golden-verificador` se citaban como skills siendo agentes.
  Además, este SKILL.md se reescribió con acentuación correcta: tenía una sola tilde en
  todo el archivo, y esa costumbre fue la que arrastró el fallo (1) hasta el entregable.

- **GP1.0** (2026-09-02) — Creación. Encargo de FER a partir de Prezi AI. Motor de cámara
  sobre lienzo, 8 tipos de lámina, modo presentador con notas y cronómetro, vista general,
  deep-link, modo flujo en móvil, salida a PDF y marca parametrizable. Verificador con
  contraste WCAG calculado. Seis fallos detectados y corregidos ejecutando en navegador,
  no razonando: láminas sin colocar en el lienzo, preloader congelado por ralentización de
  temporizadores en segundo plano, cronómetro con el mismo defecto, el arranque pisando la
  navegación del usuario, el modo sin recuperarse al cambiar el tamaño de ventana (caso
  "conectar el proyector") y el HUD apelmazado en 375 px. Además, un fallo del propio
  verificador: contaba como lámina un ejemplo que vivía dentro de un comentario HTML.
