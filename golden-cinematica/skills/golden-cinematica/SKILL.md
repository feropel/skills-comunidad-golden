---
name: golden-cinematica
description: >-
  Golden Group — WEB CINEMATOGRÁFICA 3D nivel awwwards. Construye páginas con
  escenas 3D reales (partículas que ondulan, objetos cromados, nubes que siguen
  el cursor, cabezas de puntos, orbes de vidrio), preloader con contador y cortina
  de revelado, fondo de video pre-renderizado y movimiento lento de cine. Motor:
  Three.js por importmap en HTML de un archivo, o React Three Fiber si el proyecto
  es Next. Método: TOKENS NUMÉRICOS EXACTOS (milisegundos, grados, radios, hex),
  jamás adjetivos.
  Úsala SIEMPRE que el usuario pida: una página "espectacular", "como las de
  awwwards", "con 3D", "futurista", "robótica", "cinematográfica", "que se vea
  cara", "con partículas", "con un objeto que gire", "que se mueva sola", "tipo
  Apple", "que la gente pregunte qué agencia la hizo"; o cuando muestre de
  referencia un sitio con escena 3D, fondo animado o preloader. Dispara también
  para el HERO de una web que ya existe si el encargo es "súbele el nivel visual".
  NO usar para: página de producto Shopify COD (golden-shopify), sitio funcional
  sencillo o corporativo estándar (golden-web), ni imágenes sueltas de producto
  (golden-imagen-arena).
---

# Golden Cinemática — el salto de "página" a "experiencia"

<!-- skill GC1.3 (2026-08-21) · auditoría golden-skill-auditor: (1) desambigua la cita a `references/estilo-agencia-premium.md` — vive en golden-web, no localmente, se escribía sin dueño y se leía como archivo propio; (2) suma sección "Cuando algo falla o falta" con plan de degradación explícito (CDN caído, sin render de fondo, 60fps no alcanzado en móvil, tokens no entregados por el usuario) — antes no había manejo de error declarado; (3) TOC en references/recetas.md (309 líneas, pasaba el umbral de 300 sin índice). Blindaje: chflags uchg (quitar con chflags -R nouchg, reponer con chflags -R uchg) — mecanismo documentado aquí por primera vez -->
<!-- skill GC1.2 (2026-08-02) · filtro de 2 reels de efectos (code.xr OTP v5 · code_and_chill MENISCUS): dos familias NUEVAS que el vocabulario no tenia — ESTADOS (success state animado, carga en el boton, validacion en vivo, progreso por segmentos) con la nota de que en contra entrega la confirmacion NO es decoracion sino la venta (el cliente dio sus datos sin pagar y la duda reaparece como cancelacion al confirmar por WhatsApp), y NAVEGACION (morphing dock por path SVG y tangentes, sticky compacto, desplazamiento por vecindad). Ninguno de los 2 reels publica el codigo (piden comentar), asi que se documenta el PATRON, no la receta -->
<!-- skill GC1.1 (2026-07-27) · filtro de 9 reels: 5 términos nuevos al vocabulario de entrada y revelado (pixel/entrance reveal por grid, smooth loader con máscara, stacked sticky sections, fondo ligado al scroll) con la nota de que se hacen a mano en CSS/JS y no hace falta Framer -->
<!-- skill GC1.0 (2026-07-25) · nace de un diagnóstico de FER: "las páginas que me has hecho son 10 de 100". Destilado del análisis frame a frame de 6 sitios de Textura Agency (@textura.eu / getlayers.ai), donde se capturó el PROMPT REAL con sus tokens numéricos. El hallazgo central: la diferencia entre 10/100 y 100/100 no es la librería, es que el encargo lleva milisegundos, grados, radios y hex exactos en vez de adjetivos -->

**Versión:** `GC1.3` · Fábrica: chat centro de mando.

Esta skill existe por una razón concreta: las páginas Golden nombraban las librerías
correctas y aun así salían genéricas. El diagnóstico fue que **conocer el nombre de la
librería no produce nada**. Lo que produce es la receta con sus números.

## La ley que manda sobre todas

> **Números, no adjetivos.**

"Un preloader elegante" no construye nada. Esto sí:

```
Preloader: HOLD_AT 90 · MIN_VISIBLE_MS 1300 · REVEAL_END 145 · REVEAL_FEATHER 14
Anillo r=46 · 14 cometas · ángulo π*0.28
Gradiente: linear-gradient(104.458deg, #ffe5ac 10.028%, #97bdde 100%)
Acentos de tinta: #ffd75a / #6ccfff
```

Ese bloque es de un sitio real de referencia. **Cada valor está decidido.** Cuando algo
se deja "a criterio", sale el promedio — y el promedio es exactamente el 10 de 100.

**Regla de ejecución:** antes de escribir una línea de código, escribe el bloque de
tokens de esa página: paleta en hex, duraciones en ms, curvas de easing, radios,
cantidades de partículas, grados de rotación. Ese bloque va en `:root` del CSS y como
constantes arriba del JS. Si un número no está decidido, la pieza no está diseñada.

## Los 7 mecanismos del "wow"

Verificados frame a frame en sitios que sí lo logran. Una página cinematográfica usa
**3 o 4 de estos**, nunca los 7 (eso es ruido).

1. **Preloader con contador 0→100 y cortina que barre.** Lo primero que se ve. Mínimo
   1.300 ms garantizados aunque cargue antes: es un ritual de entrada, no un spinner.
2. **Un solo objeto 3D protagonista**, centrado, sobre negro absoluto, con **una** luz
   cálida y bloom. Nada más compite por atención.
3. **Campo de partículas emisivas que ondula en loop infinito.** Movimiento permanente
   sin que el usuario toque nada — la página está viva antes de que hagas scroll.
4. **Elemento volumétrico que persigue el cursor con inercia y estela**, cambiando de
   tinte según la zona.
5. **Video o render pre-hecho como fondo del hero**, con las capas de UI y partículas
   encima. Calidad de cine sin costo de GPU: lo caro se pre-renderiza, no se calcula.
6. **Wireframe blanco de 1px** (esferas, órbitas, retículas) sobre el objeto 3D. Le da
   lectura de instrumento técnico en vez de adorno.
7. **Choque tipográfico:** display enorme (serif itálico o grotesca pesada) contra
   microcopy de 10px con tracking abierto, numeración de sección `(026)` y reloj en
   vivo con ciudad en el header.

## Cómo se entrega (la decisión que casi siempre se falla)

| Si el entregable es… | Motor | Cómo |
|---|---|---|
| **Un HTML publicado en Vercel** (lo normal en Golden) | **Three.js por importmap** | Un solo archivo, sin build, sin npm. Ver `references/recetas.md` |
| Un proyecto Next/React ya existente | **React Three Fiber + drei** | `@react-three/fiber`, `@react-three/drei`, `@react-three/postprocessing` |
| El cliente no toca código y quiere editar la escena | **Spline** | Escena en spline.design embebida con `<spline-viewer>` |

**Error histórico que esta skill corrige:** recomendar React Three Fiber cuando el
entregable real es un archivo HTML. R3F necesita build de React — si vas a publicar un
HTML, R3F no aplica y la página termina cayendo a gradientes CSS. **Decide el motor
ANTES de diseñar.**

## Orden de trabajo (5 fases)

Destilado de un método público de 8 prompts, reordenado y con la disciplina de tokens
que a ese método le faltaba.

**1 · Plano.** Define en un solo documento: arquitectura de secciones, identidad visual
con hex exactos, cuál es el objeto 3D protagonista, el lenguaje de movimiento (duración
y easing por tipo de interacción) y el presupuesto de rendimiento. **Justifica cada
animación:** si no sirve a la historia, se borra.

**2 · Tokens.** Escribe el bloque `:root` completo y las constantes JS. Nada de "azul
oscuro": `#0B1E3D`. Nada de "rápido": `380ms cubic-bezier(.22,1,.36,1)`.

**3 · Escena.** Construye el objeto 3D protagonista con la receta que corresponda
(`references/recetas.md`). Primero que se vea bien quieto; después se anima.

**4 · Movimiento y conversión.** Preloader, scroll, cursor, reveals. Y la pregunta que
salva la página: **dónde el 3D construye confianza y dónde estorbaría la conversión.**
El formulario y el precio no se animan: se leen.

**5 · Publicar.** 60fps, peso, accesibilidad, `prefers-reduced-motion`, SEO. La lista
completa abajo.

## Vara de calidad — no se entrega si falla algo de esto

- **60fps sostenidos** en el hero, medidos en móvil de gama media, no en el Mac
- **El first paint no espera al 3D:** el bundle de la escena carga aparte (dynamic import)
- **Fallback real:** con `prefers-reduced-motion` o en gama baja se muestra un render
  estático de alta calidad de la MISMA escena. Nunca un hueco negro
- **Una sola escena WebGL protagonista por página.** `dpr` limitado a `[1, 2]`
- **La escena se pausa fuera del viewport** (`IntersectionObserver`) — no quema batería
- **Texto legible sobre la escena:** contraste AA real, no "se alcanza a leer"
- **El CTA se ve sin hacer scroll** y no compite con la animación
- Modelos comprimidos (draco/meshopt), texturas ≤ 2k, video de fondo ≤ 3 MB y `muted loop playsinline`

## Referencias de esta skill
- `references/vocabulario.md` — **cómo pedir cada efecto por su nombre.** 25 términos en
  español con su equivalente técnico. Empieza SIEMPRE aquí cuando el encargo venga vago
- `references/recetas.md` — código real y probado: preloader con cortina, partículas que
  ondulan, cromado con reflejos, cursor con inercia, wireframe, scroll cinemático

## Encadena con
- `golden-web` → estructura y blueprints por perfil, con su propia
  `references/estilo-agencia-premium.md` (tipografía display + springs + aire). Esta skill
  es su capa 3D
- `three` · `gsap` (ScrollTrigger) · `apple-design` (easing físico) · `emil-design-eng`
  (pulido invisible) · `improve-animations` (auditar una web ya hecha)
- `golden-imagen-arena` / Higgsfield → generar el render pre-hecho del fondo del hero
- `all-deploy` → publicar · `cyber-neo` → si la página lleva formularios o datos

## Cuando algo falla o falta (degradación, no bloqueo)

- **El CDN de unpkg no responde o el import falla:** no inventes una versión distinta a la
  fijada en `references/recetas.md`. Informa el corte, reintenta una vez, y si sigue caído
  entrega igual el HTML con el `<script type="importmap">` correcto — el sitio funcionará
  en cuanto el CDN vuelva. Nunca se degrada a gradientes CSS por un corte temporal.
- **No hay foto/render para el fondo del hero (mecanismo 5):** delega a
  `golden-imagen-arena` o Higgsfield para producirlo; si tampoco están disponibles, arranca
  con la escena WebGL sola (mecanismos 2-4) y dilo explícitamente como pendiente — no se
  inventa un video de stock genérico.
- **El 60fps no se sostiene en móvil de gama media (vara de calidad):** en este orden,
  antes de tocar el diseño: baja `COLS`/`ROWS` de la malla de partículas (receta 2), baja
  el `dpr` cap de `[1,2]` a `[1,1.5]`, apaga el bloom, y solo si sigue sin llegar, reduce a
  3 mecanismos en vez de 4. Nunca se sacrifica el fallback de `prefers-reduced-motion` para
  ganar fps: ese camino ya es la salida de emergencia.
- **El usuario no da los hex/tokens exactos:** no se inventan colores "bonitos" a ciegas —
  se piden UNA vez al inicio con la plantilla de `references/vocabulario.md`, y si el
  usuario no los tiene, se extraen del logo o la paleta de marca ya existente del proyecto
  (nunca un genérico #000/#fff sin decisión).

## Changelog
- **GC1.3** (2026-08-21) — Auditoría golden-skill-auditor: desambigua la cita a
  `estilo-agencia-premium.md` (vive en golden-web), suma la sección de degradación
  ("Cuando algo falla o falta") y el índice de `references/recetas.md`.
- **GC1.2** (2026-08-02) — Vocabulario de ESTADOS (confirmación en contra entrega) y
  NAVEGACIÓN (morphing dock), del filtro de 2 reels de efectos.
- **GC1.1** (2026-07-27) — 5 términos nuevos de entrada y revelado, del filtro de 9 reels.
- **GC1.0** (2026-07-25) — Creación. Diagnóstico de FER ("10 de 100") + análisis frame a
  frame de 6 sitios de referencia. Aporta lo que faltaba: la disciplina de tokens
  numéricos, la ruta HTML por importmap (el entregable real de Golden), las recetas con
  código y el vocabulario para encargar.
