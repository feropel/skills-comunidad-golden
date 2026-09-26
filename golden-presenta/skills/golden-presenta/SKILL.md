---
name: golden-presenta
description: >-
  Golden Group — PRESENTACIONES CINEMATOGRÁFICAS en un solo archivo HTML, con FONDO VIVO (8
  atmósferas WebGL y canvas), láminas de cristal, cámara que viaja por un lienzo (el efecto
  Prezi), modo presentador con notas y cronómetro, vista de mapa, salida a PDF y marca
  parametrizable. CADA PRESENTACIÓN SE VE DISTINTA: atmósfera, paleta y tipografía se eligen
  por el tema. Cero dependencias externas: no hay CDN que se caiga ni suscripción. Trae
  verificador ejecutable que mide contraste, colisiones de láminas, acentos y densidad, y
  reporta COBERTURA. Úsala SIEMPRE que el usuario pida: "hazme una presentación", "un deck",
  "unas diapositivas", "un pitch", "una propuesta para un cliente", "slides para la charla",
  "algo tipo Prezi", "una presentación que se vea cara", "pasa este documento a
  presentación", "material para el MBA o la comunidad", "presentación para vender X"; o
  muestre Prezi, Gamma, Beautiful.ai, Tome o Canva como referencia. Dispara también con
  "mejora este deck" o "esta presentación se ve fea".
---
# Golden Presenta — el deck como activo propio, no como suscripción

**Versión:** `GP2.1h` · **Fábrica: chat `✅ SKILL golden-presenta`.**

Ahí se construye y se repara esta skill. Los demás chats la USAN y mandan fila a la fábrica;
no la editan por su cuenta. Si un chat necesita un cambio, lo pide, no lo hace.


## Atmósferas disponibles

Ocho fondos vivos más la opción `ninguna`.

Catálogo del motor: `ninguna`, `nebulosa`, `aurora`, `pulso`, `candela`, `enjambre`, `reticula`, `duna`, `viaje` (entre acentos graves porque es lo que se escribe tal cual en `data-atmosfera`, sin tilde). La lista autoritativa es `Atmosfera.lista` dentro de `assets/atmosferas.js`; si esta línea y esa lista no coinciden, manda el motor y `scripts/verificar_deck.py` lo caza. `candela` (octava, añadida el 2026-09-03 por encargo de FER) es nebulosa de candela naranja con cian y estrellas, con los colores muestreados del video de los mentores del Cartel del Chat; usa `u_a`/`u_b`/`u_bg`, así que respeta los tokens de cada deck y no lleva colores quemados. El catálogo completo con el mapa tema → fondo → paleta vive en `references/atmosferas.md`.

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
**Al menos 1 de cada 4 láminas lleva algo que no sea texto** (logo, captura, diagrama). Hay
tres tipos visuales para eso: `t-visual`, `t-galeria` y `t-pantalla`. Un deck de marca todo
tipográfico se lee como un documento proyectado, y ese fue un fallo medido el 3 de septiembre.
Los recursos van incrustados con `scripts/incrustar_recurso.py`, nunca como ruta a un archivo.

Se parte de `assets/deck-base.html`, se copian los bloques `<section class="slide">` que
haga falta y se colocan en el lienzo. La disposición y las coordenadas están en
`references/motor.md`; los 11 tipos de lámina y su criterio de uso, en
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
  esquema, los frameworks por tipo de encargo y los 11 tipos de lámina con su criterio
- `references/atmosferas.md` — **los 8 fondos vivos y el mapa tema → fondo → paleta →
  receta.** Se consulta SIEMPRE: es lo que hace que dos decks no se parezcan
- `references/marca-blanca.md` — los 4 perfiles de Golden con hex exactos y su contraste
  medido, y cómo se entrega con la marca de un cliente
- `references/motor.md` — coordenadas, atajos, cómo añadir tipos de lámina, y la
  **bitácora de los 6 fallos medidos** al construir esta skill
- `assets/deck-base.html` — la plantilla funcional. No se reescribe desde cero: se copia
- `assets/atmosferas.js` — el motor de fondos vivos (21 KB medidos con `ls -l`, cero red). Fuente única: se
  incrusta en el deck con `scripts/incrustar_atmosferas.py`, nunca se copia a mano
- `scripts/verificar_deck.py` — el auditor. Se corre siempre antes de entregar
- `scripts/autoprueba_deck.py` — prueba al auditor contra casos que SE SABEN malos.
  Se corre después de tocar el auditor: si pasa a la primera, sospecha del script
- `references/changelog.md` — el acta de cada versión, fuera de aquí a propósito
- `scripts/abrir_blindaje.sh` — abre el blindaje Y captura el md5 ANTES en el mismo
  acto. `--cerrar` imprime los pares que cambiaron y vuelve a blindar. Se usa
  SIEMPRE para editar esta skill: el antes tomado de memoria se pierde

## Encadena con

- `golden-brand-brain` → la voz y la identidad (Paso 0, obligatorio)
- `golden-copywriting` → el texto de las láminas de venta. Un deck comercial sin copy de
  respuesta directa es una presentación bonita que no cierra
- `web-design-engineer` → **las 26 recetas de estilo** (paleta, tipografía, espaciado,
  movimiento y prohibiciones) en `references/style-recipes/`. Una por deck, entera
- `golden-cinematica` → de donde salen el preloader y el estándar de movimiento; úsala
  cuando el encargo necesite una escena 3D de verdad (objeto cromado, modelo que rota,
  entorno HDRI). Aquí el fondo acompaña; allí la escena ES la página. 🔴 **Si piden la
  propuesta como PÁGINA que se lee haciendo scroll por escenas** (no láminas), se delega a
  `golden-cinematica`: desde GC1.5 ese formato es suyo, con sus 12 piezas y su vara de calidad.
  Las láminas, el modo presentador y la cámara por el lienzo siguen siendo de esta skill
- `golden-web/references/estandar-movimiento.md` → los números del movimiento
- `golden-imagen-arena` o Higgsfield → producir las imágenes del deck
- `golden-finanzas` (skill desde el 19-sep-2026; antes era agente) → si el deck es una propuesta
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

## Historial

El acta completa de cada versión, con lo que se midió y lo que se rompió, vive en
`references/changelog.md`. Aquí no, para que este archivo sea instrucción y no memoria.
