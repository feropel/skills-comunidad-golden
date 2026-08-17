# Intro IGNITION — SIEMPRE diferente por producto

El intro cinematográfico (`componentes/sec-ignition.liquid`) es **su propio bloque**
(se apaga/prende solo desde el editor). **Regla: NUNCA repetir el mismo intro entre páginas.**
Cada producto estrena un intro **espectacular, cinematográfico y distinto**, hecho 100% en
CSS (sin assets, sin video pesado), que dura ~2.5–3.4s y se desvanece revelando la página.

## Cómo lograr que sea distinto cada vez
1. **Elige una VARIANTE según el vertical** (tabla abajo) — no la misma dos veces seguidas.
2. **Re-autoriza el CSS** (no copy-paste idéntico): cambia colores (tokens de marca), tiempos,
   easing, dirección, el texto (`IGN_TITLE`/`IGN_SUBTITLE`) y el motivo visual.
3. Registra cuál usaste (mentalmente / en el plan de diferenciación) para no repetir.

## Catálogo de variantes (concepto + técnica CSS clave)
1. **Ignición / Explosión** (la base actual) — núcleo que estalla + rayos + título gigante.
   Técnica: `radial-gradient` + `scale()` del core, 8 `span` rotados como rayos. *Vertical: energía/vitalidad/deportivo.*
2. **Telón / Cortina que se abre** — dos paneles que se separan (izq/der o arriba/abajo)
   revelando la página. Técnica: 2 divs `position:fixed` con `transform:translateX(±100%)`. *Lujo/perfume/fashion.*
3. **Flash + Onda expansiva (shockwave)** — destello blanco y un anillo que se expande.
   Técnica: overlay `opacity` flash + `box-shadow`/`border` de un círculo con `scale()`. *Tech/gadget/oferta.*
4. **Barrido de luz / Scanlines** — líneas de luz que recorren la pantalla y desaparecen.
   Técnica: `repeating-linear-gradient` animado con `background-position` o un `span` que cruza. *Tech/limpieza/médico.*
5. **Niebla / Humo que se disipa** — bruma que se aclara y revela el nombre.
   Técnica: capas con `filter:blur` + `opacity` + `mask`/gradiente que se desvanece. *Perfume/elegante/skincare.*
6. **Partículas que se ensamblan** — puntos que caen/flotan y forman el título.
   Técnica: varios `span` con `transform` desde posiciones aleatorias → convergen. *Belleza/joyería/femenino.*
7. **Zoom-portal desde el centro** — la página entra como atravesando un portal/destello.
   Técnica: overlay con `clip-path:circle()` que crece de 0 a 150%. *Universal moderno.*
8. **Cuenta atrás relámpago "3·2·1"** — números gigantes que pulsan y revientan.
   Técnica: 3 títulos con `animation-delay` escalonado + flash final. *Oferta/urgencia/impulso.*
9. **Respiración / Bloom** — un núcleo que "respira" (inhala-exhala con `scale()`), suelta
   anillos concéntricos y partículas que se elevan, y el título aparece letra por letra (cada
   `span` con `--i` y `animation-delay` escalonado) bajo un barrido de luz diagonal final.
   Técnica: `@keyframes` de breath en el core (`scale(0)→1.15→.65→1→2.6→8`), `span` de anillos con
   `scale(0→36)`, partículas con `translate(var(--dx),-230px)`, letras con `blur+translateY`, y un
   `.sweep` con `skewX(-12deg)`. *Salud/bienestar/digestivo/respiratorio/clorofila.* (Absorbida de un build real, G2.3.)

## Reglas
- Hecho 100% CSS, sin video ni imágenes (carga instantánea, no rompe rendimiento).
- Respeta REGLA #2: no usa el verde del CTA como protagonista (es un intro, no un botón).
- Móvil: dura un poco más (que dé tiempo a leer) y el título baja de tamaño.
- Es un **bloque aparte y apagable**: si el usuario/cliente no lo quiere, lo desactiva en el editor.
- Va de los primeros en el `block_order` (es un overlay `position:fixed`, su orden no afecta layout).

## REGLA DE SALIDA (G3.15, innegociable) — el intro JAMÁS depende de CSS para quitarse
Caso real (build de un suplemento nocturno): la salida por `animation … forwards` NO corre si la
pestaña se abre en segundo plano (Chrome pausa las animaciones CSS) o si otra capa las resetea →
el overlay queda MONTADO tapando la página. La animación CSS es estética; la SALIDA es JS multi-vía:
0. **RE-PARENT al `<body>` (G3.16)**: `if(g.parentNode!==document.body){document.body.appendChild(g);}` como
   primera línea del script. Si el overlay vive como bloque del main (Dawn/Shrine animan contenedores con
   `transform`), `position:fixed` queda atrapado y se ve como un CUADRITO dentro del layout — el mismo motivo
   por el que sticky y WhatsApp ya se re-parentan. Verificar: `getBoundingClientRect()` del overlay = viewport.
1. `pointer-events:none` SIEMPRE en el overlay (aunque todo falle, no bloquea la compra).
2. Kill por TIMER JS (vida ~2.5s desktop / ~3.4s móvil): fade + `removeChild` (FUERA del DOM, no display:none).
3. Kill por INTERACCIÓN: `pointerdown/touchstart/wheel/keydown/scroll` (once) lo quitan al instante.
4. Si `document.visibilityState === 'hidden'` al cargar: NO arrancar la secuencia; esperar
   `visibilitychange` a visible (que el visitante SÍ lo vea) — el failsafe corre igual.
5. FAILSAFE absoluto: `setTimeout(killNow, 7000)` + `pagehide` → `removeChild` incondicional.
6. `sessionStorage` (`gfs_ign_seen`): el intro se muestra UNA vez por sesión.
7. `prefers-reduced-motion: reduce` → `display:none` + killNow. PROHIBIDO el "bypass" que fuerza animaciones.
El componente `componentes/sec-ignition.liquid` ya trae este motor: al adaptar el intro a otra variante,
NO recortar el `<script>` final.
**VERIFICACIÓN OBLIGATORIA (render real):** recarga limpia (`sessionStorage.removeItem('gfs_ign_seen')`)
→ el intro aparece → a los ~3s YA NO está en el DOM (`document.querySelector('.gfs-ignition')` = null).
Probar también con la pestaña abierta en segundo plano. Sin esa prueba, el intro NO se entrega.
