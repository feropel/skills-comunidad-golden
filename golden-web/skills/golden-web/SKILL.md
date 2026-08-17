---
name: golden-web
description: >-
  Golden Group — Construcción de SITIOS y LANDING PAGES de alta conversión por
  perfil de cliente: MARCA PROPIA (e-commerce/branding), CREADOR DE CONTENIDO
  (link-in-bio, portafolio, venta de infoproductos) y EMPRESA (sitio corporativo,
  servicios, captación de leads/citas). Diseño moderno y tecnológico, deploy a la
  nube con Vercel y dominio propio.
  Úsala SIEMPRE que el usuario quiera: crear una web/landing que NO sea página de
  producto Shopify COD — sitio de marca, link-in-bio, portafolio de creador,
  web corporativa, página de servicios, captación de leads. Dispara con "hazme una
  web para", "landing de marca", "página para mi empresa", "link in bio",
  "sitio para un creador/consultorio".
  Para página de producto dropshipping COD usa golden-shopify. Para el portal de la
  comunidad Golden con login/recursos, ese es su propio proyecto.
---

# Golden Group — Web por Perfil

**Versión:** `GW2.2` · Fábrica: este chat.
_GW2.2 (2026-07-25): + `references/estilo-agencia-premium.md` — receta del look agencia premium (destilado 2026-07: serif display gigante peso 400 + sans ultra-light, gradiente firma único sobre casi-negro, springs por letra en titulares, Lenis, video como textura, copy de una frase con CTA único de agenda). Destilado a nivel de código de una agencia Awwwards de referencia; receta Golden original, sin textos ni marca ajena._
_GW2.1 (2026-07-17): + sección **CITABLE POR LA IA (GEO/AEO)** obligatoria: los 2 ejes (Google vs motores de IA), la distinción crítica entre bots de ENTRENAMIENTO (GPTBot/ClaudeBot, bloqueables) y bots de CITACIÓN (OAI-SearchBot/**Claude-SearchBot**/PerplexityBot — si los bloqueas desapareces de las respuestas en vivo), bloques de respuesta extraíbles, densidad de hechos/entidades, FAQ+LocalBusiness en JSON-LD, y la verdad sobre llms.txt (impacto incierto, no venderlo como ranking). Destilado de la guía de claude-seo-ai (plugin MIT de tododeia). Oportunidad anotada: vender auditoría de visibilidad en IA._
_GW2.0 (2026-07-17): **SECUENCIA sube de nivel** — método oficial 2 imágenes (inicial+final con Nano Banana) → 1 video (Kling) → ~120 frames WebP con ffmpeg, en vez de 60 generaciones sueltas: mucho más barato y con consistencia perfecta. + GOTCHA de publicación (los frames se excluyen del repo y la animación muere en producción) + plan mode + auto-mejora de la skill tras cada build. + Framer Motion como estándar de motion en React. Destilado del tutorial de Nate Herk (230k vistas, "Nano Banana 2 + Claude Code = $10k websites") y del setup de noocap (Claude Code + motion + design skill + 21st.dev = lo que ya teníamos)._
_GW1.9 (2026-07-17): + EFECTO GOLDEN AURORA (héroe interactivo estilo SaaS de lujo): manchas de gradiente vibrante en mezcla aditiva que flotan y siguen el cursor con bloom + tarjeta glassmorphism encima. Canvas 2D liviano (sin WebGL), parallax, resorte, grano+viñeta, reduced-motion. Demo en vivo: comunidadgolden.com/aurora. Destilado de un prompt "Aurora Gradient" de referencia (SaaS de lujo/Awwwards), reescrito original. Del mismo lote: descartados por redundantes OpenMontage (video → ya HyperFrames), Open-Generative-AI (→ ya Higgsfield), dataviz (built-in ya disponible); NoirPixel reconfirma dirección Noir Premium (GW1.2)._
_GW1.8 (2026-07-14): + EFECTO GOLDEN SECUENCIA (scroll-linked frame sequence, "el efecto Apple AirPods"): el producto se ARMA o gira 360° cuadro por cuadro al hacer scroll — frames generados con IA (Nano Banana Pro / Higgsfield) y scrubbeados sobre canvas con GSAP ScrollTrigger. Sirve para el héroe de golden-web Y para la página de producto golden-shopify (el momento wow que vende). + Aceternity UI y Nano Banana Pro citados como fuentes de la capa visual. Destilado de referencias externas (reels de webs IA), sin clonar ni nombrar marcas ajenas._
_GW1.7 (2026-07-13): + patrón LANDING GOLDEN DE SERVICIO (vender bots/servicios a negocios locales): demo de chat simulado como héroe, pestañas por sector con asistente nombrado, sección "el coste de no responder" (antes/después), 3 pasos, barra de stats. Destilado de la competencia (SaaS de chatbots), mejorado a lo Golden._
_GW1.6 (2026-07-12): + capa GOLDEN CINEMÁTICA 3D (WebGL real): ruta React con react-three-fiber + drei, ruta no-code embebiendo escenas de Spline, y el patrón de scroll narrativo por producto (line-up → héroe → specs → cierre). Cablea ui-ux-pro-max como inteligencia de diseño OBLIGATORIA. Destilado de referencias externas (webs 3D awwwards) sin clonar ni nombrar marcas ajenas._
_GW1.5 (2026-07-12): + catálogo EFECTOS GOLDEN de heros cinematográficos (Nebulosa, Trazo, Cromo, Chips, Kinética, Split, Aliento) con reglas técnicas de rendimiento — destilado original de referencias externas, sin nombres ajenos ni librerías de pago._
_GW1.4 (2026-07-12): + arsenal de motion pro (apple-design, improve-animations, animation-vocabulary, emil-design-eng) cableado en el Stack — la capa de movimiento ahora se ejecuta con criterio de motion físico/springs, no solo fades._
_GW1.3 (2026-07-11): TODO se llama GOLDEN — catálogo de 4 direcciones de arte (Luxury/Tech/Belleza/Impacto) sin nombres de referencias externas + CAPA DE MOVIMIENTO obligatoria (nunca páginas estáticas: reveals, sticky cinemático, micro-interacciones, prefers-reduced-motion) + tip Claude Design._
_GW1.2 (2026-07-11): + dirección de arte premium para negocios locales/servicios (destilada de referencia externa, no clonada) + patrones de landing para VENDER servicios web._
_GW1.1 (2026-07-03): encadena la trifecta — `cyber-neo` (auditoría pre-deploy) + `all-deploy` (publicación) en el flujo._

Webs que se ven caras y convierten, montadas rápido y publicadas en la nube. Selecciona el perfil y aplica el blueprint.

## Stack (todo ya disponible)
- **Diseño/maquetado:** skills `frontend-design`, `ui-ux-pro-max`, `web-artifacts-builder`, `theme-factory` + MCP Magic (componentes 21st.dev) + MCP Stitch (design systems).
- **Movimiento de nivel Apple:** skills `apple-design` (motion físico/springs/gestos — úsala SIEMPRE en la capa de movimiento y en Golden Tech), `improve-animations` (audita y planea mejoras de motion de un sitio ya hecho), `animation-vocabulary` (nombrar el efecto exacto) y `emil-design-eng` (pulido de detalles invisibles).
- **3D / WebGL (capa Golden Cinemática):** skill `three` (fundamentos three.js) + `gsap` (ScrollTrigger). Código React: `react-three-fiber` + `drei` + opcional `@react-three/postprocessing` / Theatre.js. No-code: `Spline` (spline.design) embebido con `@splinetool/react-spline`. Ver sección **Golden Cinemática 3D**.
- **Imágenes/assets:** Higgsfield (`generate_image`) + **Nano Banana Pro** (imágenes de producto/escena hiperrealistas, ideal para los frames de Golden Secuencia y heroes fotográficos), `canvas-design`, `golden-imagen-arena`.
- **Motion en React:** **Framer Motion** (`motion/react`) es el estándar para builds React/Next — reveals por scroll, entradas escalonadas y hovers suaves. Regla: si el proyecto es React, Framer Motion; si es HTML/canvas puro, CSS + GSAP. Nunca dejes una web estática.
- **Componentes animados de referencia:** MCP Magic (21st.dev) + Aceternity UI (aceternity.com — biblioteca React/Tailwind de componentes con micro-animaciones y efectos de scroll; se DESTILA el efecto, no se pega la marca ajena).
- **Hosting + dominio:** skill **`all-deploy`** (`/all-deploy` — detecta stack, elige hosting Vercel/Railway/VPS, preview→prod con rollback) + MCP Vercel + MCP Domains (verificar dominio).
- **Seguridad pre-publicación:** skill **`cyber-neo`** (`/cyber-neo .`) cuando la web tenga login, formularios, datos o claves — arregla Critical/High antes de publicar.
- **Contenido/CMS ligero:** Notion (si quiere editar sin tocar código).

## Reglas de oro
1. **Mobile-first** y velocidad (LatAm, datos móviles). Imágenes WebP livianas.
2. **Una promesa clara above-the-fold** + CTA único por objetivo.
3. **Diseño tecnológico, no plantilla genérica** — consulta SIEMPRE `ui-ux-pro-max` (inteligencia de diseño: 67 estilos, 96 paletas, 57 pares tipográficos, guías UX por stack) ANTES de elegir estilo/paleta/tipografía, y `frontend-design` para evitar el "look IA". No inventes el sistema visual: pídeselo a la skill y adáptalo a la marca.
4. **Siempre termina publicado** (Vercel) con URL compartible, o entrega el código listo para deploy.

## Blueprints por perfil

### 🛍️ Marca propia
Objetivo: vender catálogo + construir marca.
Secciones: Hero con propuesta de valor → productos destacados → diferenciales/garantía → prueba social → historia de marca → newsletter/CTA. Integra checkout (Shopify) si aplica.

### 🎥 Creador de contenido
Objetivo: centralizar audiencia y monetizar.
Secciones: Hero personal → link-in-bio (redes, contenidos) → portafolio/mejores piezas → infoproductos/servicios con CTA de compra → testimonios → contacto/colaboraciones.

### 🏢 Empresa
Objetivo: autoridad + captación de leads/citas.
Secciones: Hero con servicio principal → servicios → casos/resultados → equipo/confianza → CTA de cotización o **agendar cita** (enlaza con `golden-agenda-citas`) → contacto/mapa.

## Catálogo de direcciones GOLDEN (el usuario pide "una web golden")

**Regla de marca:** las direcciones se llaman SIEMPRE Golden — jamás mencionar al usuario nombres
de referencias externas (las referencias se analizan, se destilan y desaparecen). Cuando pidan
"hazme una web golden", ofrece el catálogo o decide tú la mejor dirección para el negocio e
INFORMA (máxima autonomía). El acento se adapta al color de la marca del cliente (dorado solo
si es su marca).

### ✨ GOLDEN LUXURY — negocios que deben verse caros
Barberías, cafés, restaurantes, estética, consultorios premium.
- Fondo casi-negro `#050505` + textura sutil (grid fino `rgba(255,255,255,.03)` con máscara radial).
- Texto crema cálido `#F5F2EA` (nunca blanco puro: el crema hace el negro "caro").
- Acento metálico 2 tonos: base `#D6B15A` + claro `#F0D894`; chips/CTAs fantasma = acento al 6%
  de fondo + texto claro. Pills MAYÚSCULAS con letter-spacing ~2px.
- **Display serif editorial** (Playfair o similar, peso 400) GIGANTE — H1 `clamp(3rem,10vw,9rem)`,
  line-height ~0.9 — + **Inter** de cuerpo. Ese contraste ES el look. Halo cálido tras el titular.

### 🍎 GOLDEN TECH — estilo Apple, producto como héroe
Tecnología, apps, gadgets, marcas que quieren sentirse "del futuro".
- Fondo limpio (blanco puro o negro puro), UN producto protagonista al centro, aire extremo.
- Tipografía sans grande y precisa, copy mínimo ("menos palabras, más impacto por palabra").
- **Scroll cinemático**: secciones sticky donde el producto se queda fijo y el relato avanza
  alrededor; el scroll cuenta la historia (revelar → acercar → explotar en detalles → CTA).
- Detalles: números enormes para specs, transiciones suaves, cero decoración gratuita.

### 🌸 GOLDEN BELLEZA — cosmética, skincare, bienestar
- Fondos claros cálidos (crema/blush), fotografía grande del producto/textura, aire.
- Serif elegante para titulares + sans suave; paleta pastel con UN acento de marca.
- Secciones: ritual de uso paso a paso, ingredientes con iconos, antes/después, prueba social
  fuerte (reseñas con foto). Movimiento suave y femenino (fades lentos, parallax sutil).

### 🔥 GOLDEN IMPACTO — bold, comida, street, energía
Food trucks, comida, fitness, marcas jóvenes que gritan.
- Colores saturados de la marca, tipografía ULTRA pesada y enorme, composición diagonal.
- Marquees (cintas que corren), stickers/badges, fotos con actitud, hover que reacciona.
- CTA omnipresente y directo. Es volumen alto — pero con retícula: bold no es desorden.

### 🎬 CAPA DE MOVIMIENTO (obligatoria en TODA dirección — nunca páginas estáticas)
Una web Golden se siente VIVA. Mínimos en cada build:
1. **Reveals al hacer scroll** (IntersectionObserver): cada sección entra con fade+rise sutil.
2. **Un momento sticky/cinemático** por página (el hero o el producto) — el "efecto Apple".
3. **Micro-interacciones**: hovers con intención (escala 1.02-1.05, glow del acento), botones
   que responden, links con subrayado animado.
4. **Vida ambiental**: contadores que suben, marquee, halo que respira — UNA por página, no todas.
5. **Rendimiento y respeto**: animar solo `transform`/`opacity`, lazy en media, mobile-first,
   y `prefers-reduced-motion` SIEMPRE respetado. El movimiento nunca sacrifica velocidad (LatAm).

### 🎇 EFECTOS GOLDEN — heros cinematográficos (nivel "qué locura de página")

Catálogo de efectos wow para el HERO (o un momento clave). Regla: **UN efecto protagonista por
página** — el efecto es el escenario del mensaje, nunca compite con él. Texto SIEMPRE legible
encima (overlay/contraste). Elegir el que sirva a la marca:

1. **Golden Nebulosa** — campo de miles de partículas que fluyen como olas u forman una figura
   (hélice, logo, producto). Canvas 2D o three.js Points; las partículas derivan suave y
   reaccionan levemente al mouse (parallax). Variante "constelación": puntos + líneas cercanas.
2. **Golden Trazo** — geometría de líneas finas (círculos, retículas, órbitas) que se DIBUJA
   sola sobre el fondo (SVG `stroke-dasharray/dashoffset` animado). Elegante, técnico, liviano.
   Combina perfecto encima de Nebulosa.
3. **Golden Cromo** — escultura 3D cromo/vidrio flotando (manos, estrella, objeto de marca) con
   reflejos, girando lento con parallax. Producción: render/imagen PNG de alta calidad + CSS 3D
   parallax (barato) o three.js con environment map (premium). Ancla de la dirección Luxury/Tech.
4. **Golden Chips** — tarjetas de vidrio (glassmorphism sutil: blur + borde 1px translúcido)
   flotando SOBRE el arte con stats que cuentan hacia arriba (120+, 5.0, 68%). Micro-parallax a
   distinta velocidad que el fondo = profundidad. Datos SIEMPRE reales.
5. **Golden Kinética** — el titular entra palabra por palabra o por máscara (clip-path reveal),
   con una palabra clave en acento. La tipografía ES el efecto; ideal cuando no hay arte 3D.
6. **Golden Split** — hero dividido en dos mundos (mitad clara editorial + mitad oscura con el
   arte/efecto). El contraste entre ambos lados es el impacto.
7. **Golden Aliento** — la "interfaz viva": nada está quieto del todo — halo que respira, glow
   que pulsa, escultura que deriva 1-2px. Imperceptible pero hace la página sentirse VIVA.
8. **Golden Secuencia** — el producto se ARMA, gira 360° o se transforma **cuadro por cuadro
   mientras el usuario hace scroll** (el efecto de las páginas de producto de Apple: AirPods,
   MacBook). Es el momento wow que MÁS vende porque el producto es el protagonista y el scroll
   lo controla. Cómo se hace (barato y sin WebGL):
   - **MÉTODO OFICIAL (2 imágenes → 1 video → 120 frames):** NO generes 24-60 imágenes sueltas
     (caro e inconsistente). El camino barato y perfecto es:
     **(a)** genera el **cuadro INICIAL** con Nano Banana Pro: _"imagen profesional de estudio de
     [PRODUCTO], fondo negro plano, sin sombras, sin manos, sin reflejos"_, formato 16:9.
     **(b)** genera el **cuadro FINAL** con el MISMO prompt + la transformación (ej: "…ahora
     abierto mostrando sus capas" / "…lleno de fruta y jugo"), usando la imagen inicial como
     semilla para que sea el mismo producto.
     **(c)** anima inicial→final con **Kling** (start frame + end frame). El prompt del video
     pídeselo a Claude pasándole ambos cuadros: _"ayúdame a escribir el prompt de video: [lo que
     debe pasar], sin sombras, sin manos, sin reflejos"_.
     **(d)** entrega el video y **extrae ~120 frames en WebP con ffmpeg** (Claude lo hace; si no
     tienes ffmpeg, él lo instala). Cada frame se mapea a una posición de scroll.
     Ventaja: 2 imágenes + 1 video en vez de 60 generaciones → mucho más barato y con
     consistencia perfecta (todos los cuadros salen del mismo video). Foto REAL del producto como
     semilla — la IA no lo redibuja (regla Golden de imágenes fieles).
   - **Scrub con scroll:** precarga los frames (WebP livianos), dibuja el frame actual en un
     `<canvas>` fijo/`pinned`, y mapea el progreso de scroll → índice de frame con **GSAP
     ScrollTrigger** (`pin:true`, `scrub:true`). El resultado se siente pulido y "caro".
   - **Uso:** héroe de producto en golden-web y **la sección héroe de la página de producto COD
     en golden-shopify** — el producto "cobra vida" antes de la ficha y el botón Releasit.
   - ⚠️ **GOTCHA de publicación (falla al 90%):** al subir a GitHub/Vercel, la carpeta de
     `frames/` se excluye por gitignore y **la animación desaparece en producción** (el sitio
     carga pero el producto no aparece). Verifica SIEMPRE que los frames viajen en el repo, y
     abre la URL real después de publicar. Trabaja en localhost → prueba → recién ahí publica.
   - **Método de trabajo:** arranca en **plan mode** (mejor resultado a la primera), y cuando el
     resultado te guste, pídele a Claude que **actualice esta skill** con lo que funcionó — así
     el efecto mejora en cada build.
9. **Golden Aurora** — el fondo interactivo estilo SaaS de lujo (Stripe/Apple): manchas de
   gradiente vibrante (dorado + púrpura, azul, cian, rosa, esmeralda) que se funden con **mezcla
   aditiva** (`globalCompositeOperation='lighten'`) y flotan sin parar, creando una aurora suave.
   Cuando el usuario mueve el cursor, las manchas cercanas **se avivan, se expanden y hacen "pop"**
   siguiendo la mano con un **bloom** y física de resorte (easing, nunca instantáneo). Cómo se hace
   (barato, sin WebGL): canvas 2D con gradientes radiales grandes en modo `lighten`,
   `requestAnimationFrame` a 60 FPS, parallax por capas (cada mancha a distinta profundidad),
   bloom radial en el cursor con lerp de resorte, grano SVG sutil (feTurbulence) + viñeta
   cinematográfica, y una tarjeta **glassmorphism** (`backdrop-filter: blur`) con el mensaje
   encima. La aурora nunca se satura de más; el texto siempre legible sobre la tarjeta de vidrio.
   Móvil: menos manchas + deriva automática (sin mouse), DPR cap 2; reduced-motion → frame estático
   elegante. **Uso:** héroe de landing de marca/servicio/SaaS. Destilado de un prompt "Aurora
   Gradient" de referencia (SaaS de lujo, Awwwards) — reescrito original, sin librerías de pago.

**Reglas técnicas (obligatorias):**
- Canvas/three.js se PAUSA fuera del viewport (IntersectionObserver) y con
  `prefers-reduced-motion` cae a una versión estática elegante (frame congelado + gradiente).
- Móvil primero: reducir densidad de partículas (~40%), cap de devicePixelRatio a 2,
  `requestAnimationFrame` único. El wow nunca sacrifica velocidad (LatAm, datos móviles).
- Stack: three.js solo si el efecto lo amerita; Nebulosa/Trazo/Kinética salen con canvas 2D,
  SVG y CSS puro (más livianos). Criterio de motion: skill `apple-design`.

### 🧊 GOLDEN CINEMÁTICA 3D — WebGL de verdad (nivel awwwards)

Cuando la marca amerita 3D real (producto héroe girando, escena interactiva, storytelling con
scroll), sube de canvas 2D a **WebGL**. Dos rutas según quién construye:

**A) Ruta CÓDIGO (React/Next — control total):**
- **`react-three-fiber`** (`@react-three/fiber`) = three.js declarativo en React. La base.
- **`drei`** (`@react-three/drei`) = helpers listos: `<Environment>` (reflejos HDRI para el cromo),
  `<Float>`, `<ScrollControls>`/`<Scroll>` (scroll cinemático), `<Center>`, `<Bounds>`,
  `<MeshTransmissionMaterial>` (vidrio), `<Text3D>`, carga de modelos `useGLTF`.
- **`@react-three/postprocessing`** para bloom/DOF (el glow premium) — con mesura.
- **Scroll narrativo:** `<ScrollControls>` de drei, o **GSAP ScrollTrigger** (skill `gsap`), o
  **Theatre.js** (`@theatre/core` + `@theatre/r3f`) cuando quieras animar cámara/objetos por
  keyframes como en After Effects (secuenciar la historia con precisión). Elige UNA.
- La skill `three` (instalada) da los fundamentos de three.js; `apple-design` da el criterio de
  cámara/easing físico.

**B) Ruta NO-CODE (tú o un alumno, sin programar):**
- **Spline** (spline.design) = editor 3D visual. Diseñas la escena (objeto de marca, luces,
  interacción) y la embebes con **`@splinetool/react-spline`** (`<Spline scene="...splinecode" />`)
  o el `<spline-viewer>` web component. Ideal para el Cromo/objeto héroe sin tocar shaders.
- Se integra en cualquier build Golden: la escena de Spline va como el arte del hero y el texto
  Golden se maqueta encima (mismas reglas de contraste/legibilidad).

**Patrón "Storytelling por scroll" (el de las webs 3D que enamoran):** un solo producto es el
protagonista y el scroll cuenta su historia en actos, con la cámara/objeto reaccionando:
`01 line-up` (presenta) → `02 héroe` (producto flotando con luz/humo/partículas) →
`03 specs` (números enormes + detalle macro) → `04 armado/uso` → `05 CTA`. Cada acto es una
sección sticky; el objeto 3D permanece y el relato avanza. Sirve para comida, gadget, cosmético,
cualquier producto con "alma".

**Reglas técnicas 3D (además de las de EFECTOS GOLDEN):**
- WebGL es caro: **1 escena 3D protagonista por página**, `dpr={[1, 2]}` (cap), `frameloop="demand"`
  cuando no hay animación continua, y **pausa/deja de renderizar fuera del viewport**.
- Móvil y `prefers-reduced-motion`: fallback a un **PNG/render de alta calidad** de la misma escena
  (nunca dejar al usuario de gama baja sin hero). Modelos comprimidos (draco/meshopt), texturas ≤2k.
- Peso: lazy-load del bundle 3D (dynamic import), nunca bloquear el first paint. El wow jamás
  sacrifica velocidad (LatAm, datos móviles).

### 💬 LANDING GOLDEN DE SERVICIO — vender bots/automatización a negocios locales

Cuando la web VENDE un servicio conversacional (bot de WhatsApp, asistente, agenda automática,
web+bot para un negocio local), el patrón ganador es MOSTRAR el servicio funcionando, no contarlo:

1. **Demo de chat simulado como héroe** — una conversación estilo WhatsApp (burbujas, checks ✓✓,
   hora) que se ESCRIBE sola con animación (mensajes aparecen en secuencia con typing dots).
   El guion demo: cliente pregunta → bot responde al instante → agenda/vende en 3-4 mensajes.
   HTML/CSS propio (burbujas verdes/blancas, avatar del asistente) + JS de secuencia. Datos del
   demo genéricos y realistas — precios/beneficios REALES los pone el dueño.
2. **Asistente con nombre y cara** — "Valentina · Recepción", "Diego · Ventas": humaniza y hace
   tangible el servicio. El nombre lo decide el cliente/dueño (regla: jamás cambiar el nombre
   del asesor de un cliente existente).
3. **Pestañas por sector** — cada nicho (ecommerce, clínica/estética, restaurante, inmobiliaria,
   servicios) con SU conversación demo y SUS beneficios en ✓. El visitante se ve a sí mismo.
4. **"El coste de no responder"** — pares Antes ✕ / Después ✓ ("Cliente pregunta a las 11pm.
   Nadie contesta. Compra en la competencia." → "El asistente responde al instante y cierra").
   El miedo a perder ventas vende más que la lista de features.
5. **3 pasos** ("Conecta → Entrena con tu contenido → Vende") + **barra de stats** (24/7 · <1s ·
   sin contratar personal). Números genéricos de capacidad sí; cifras de resultados solo reales.
6. CTA directo a WhatsApp del dueño con palabra clave (regla WA = disparador del bot).

Encaja con: perfil 🏢 Empresa, oferta "Web Premium Local" y la familia Chatea PRO (el bot que se
vende con esta landing se configura con las skills golden-chatea-pro-*). Oportunidad Golden:
empaquetar web + bot + agenda como servicio recurrente replicable por los alumnos.

**Patrones de sección que venden (aplicar los que sumen):**
`01` numeración editorial · Antes/Después ("de links regados a una marca que da confianza") ·
vitrina multi-dispositivo · grid de industrias · precio único limpio ("incluido" + "lo que queda
tuyo"; precio SIEMPRE del dueño) · case-study por proyecto (chip + título gigante + meta).

**Uso comercial (Golden + alumnos):** este catálogo convierte a golden-web en una máquina de
VENDER webs — el paquete "web Golden de una página" a precio único es un servicio replicable
para la comunidad (cada alumno puede ofrecerlo en su ciudad).

**Tip de diseño previo (opcional):** la versión visual se puede bocetar en claude.ai/design
(Claude Design, ya incluido en el plan) y traer por handoff a Claude Code — declarando el stack
destino (Next + Tailwind + shadcn) desde el primer prompt.

## 🤖 CITABLE POR LA IA (GEO/AEO) — obligatorio en toda web Golden

Hoy la gente no solo busca en Google: le pregunta a ChatGPT, Perplexity, Gemini y Claude. Ser
bueno para Google y ser **citable por la IA** son **dos cosas distintas** — se miden por separado y
una no garantiza la otra. Toda web Golden nace lista para los dos ejes:

**Eje 1 · Search SEO (Google):** títulos y meta reales, jerarquía de headings, canonical, robots.txt,
sitemap, datos estructurados (JSON-LD), Core Web Vitals, señales E-E-A-T.

**Eje 2 · Visibilidad en IA (GEO/AEO):**
- **Deja entrar a los bots de CITACIÓN.** Hay dos tipos y NO son lo mismo: los de **entrenamiento**
  (`GPTBot`, `ClaudeBot`) usan el contenido para aprender — se pueden bloquear sin perder nada; los
  de **búsqueda y citación** (`OAI-SearchBot`, **`Claude-SearchBot`**, `PerplexityBot`) son los que
  te citan en respuestas EN VIVO — **si los bloqueas, desapareces de esas respuestas**. Decláralos
  explícitos en `robots.txt`.
- **Bloques de respuesta extraíbles:** párrafos que contestan UNA pregunta concreta de forma directa
  (pregunta como encabezado + respuesta completa en 2-4 líneas debajo). La IA cita párrafos que se
  sostienen solos, no promesas de marketing.
- **Densidad de hechos y entidades claras:** datos, cifras, nombres propios, ciudades, productos y
  términos concretos. Lo vago no se cita.
- **FAQ real con JSON-LD** (`FAQPage`) y ficha del negocio (`LocalBusiness`/`Organization`) — es lo
  que más levanta la citabilidad de un negocio local.

**Honestidad (nada de mitos SEO):** `llms.txt` se puede generar, pero hoy **su impacto es incierto**
— solo algunos motores lo respetan y Google no lo usa para sus respuestas de IA. No lo vendas como
factor de ranking. Igual que la velocidad: se mide, no se promete.

**Auditoría:** existe el plugin open-source `claude-seo-ai` (MIT, corre offline, sin API keys) que
audita los DOS ejes y da dos notas separadas 0-100 (nunca promediadas). Útil para auditar un sitio
propio o de cliente — **oportunidad de servicio Golden: auditoría de visibilidad en IA.**

## Flujo
1. **Perfil + datos** (negocio, objetivo, marca/colores, secciones, dominio).
2. **Diseñar** con el blueprint usando las skills de frontend.
3. **Assets** (imágenes/logo) con Higgsfield/canvas-design si faltan.
4. **Blindar (si aplica)** — si la web maneja login, formularios, datos o claves, corre `cyber-neo` (`/cyber-neo .`) y arregla Critical/High antes de seguir.
5. **Publicar** con `all-deploy` (`/all-deploy`): elige hosting (Vercel para estático/Next/Vite; Railway/VPS si hay backend), preview → prod con rollback. Conecta dominio. *(NO uses `all-deploy` para páginas de producto Shopify — esas van por su flujo.)*
6. **Entregar** URL + cómo editar a futuro.

## Cierre
Ofrece: «Conecto dominio propio, agrego captación de citas (`golden-agenda-citas`) o sumo esta web como recurso del Portal Golden?»

> Fondos/efectos generativos (galería Golden): ver `references/arte-generativo-golden.md` (método p5.js con semilla + templates).
> Look agencia premium (tipografía display + movimiento + aire): ver `references/estilo-agencia-premium.md` — receta destilada 2026-07 con tokens, secciones, checklist de motion y fórmula de copy.
