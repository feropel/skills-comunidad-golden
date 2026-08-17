# Rendimiento — página rápida = más conversión

La velocidad de carga afecta directo la conversión (cada segundo de más baja ventas).
Aplica SIEMPRE estas reglas; el objetivo es LCP < 2.5s y CLS ≈ 0 en móvil.

## Fuentes (la causa #1 de lentitud aquí)
- **NUNCA cargar fuentes con `@import`** dentro de `<style>` → es render-blocking (la
  página espera la fuente antes de pintar). Es el error más común.
- En su lugar, en el bloque propuesta (primero), usar:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">
  ```
- `display=swap` SIEMPRE (muestra texto con fuente de sistema y cambia al cargar; no deja
  la pantalla en blanco).
- Cargar SOLO los pesos que se usan (no `wght@100..900` entero). Cada peso pesa.

## Imágenes (la causa #2)
- **Hero / primera imagen visible:** `fetchpriority="high"` y NO lazy (debe cargar ya).
- **Todo lo demás (abajo del fold):** `loading="lazy"` y `decoding="async"`.
- **SIEMPRE `width` y `height`** (o `aspect-ratio`) en cada `<img>` para evitar CLS
  (que el layout salte mientras carga = se ve roto y penaliza).
- Preferir formatos modernos (WebP/AVIF) cuando el usuario suba imágenes.

## JavaScript
- Consolidar: evitar muchos `<script>` sueltos repitiendo `DOMContentLoaded`. Un solo
  motor de animación (IntersectionObserver compartido) en el bloque propuesta sirve a toda
  la página (ver `efectos-premium.md` snippet 1). No crear un observer por sección.
- Nada de listeners de `scroll` sin `throttle`/`requestAnimationFrame` (causan jank).
- Scripts no críticos: que corran tras `DOMContentLoaded`, nunca bloqueando el render.
- El `MutationObserver` del override Releasit: que se desconecte (`disconnect()`) tras
  aplicar, no quede observando para siempre.

## CSS / efectos
- `backdrop-filter` (glassmorphism) es **caro en móvil**: úsalo en POCOS elementos, no en
  listas largas. Si la sección tiene muchas tarjetas, usar fondo sólido translúcido.
- `content-visibility:auto` en secciones largas de abajo (reseñas, FAQ, beneficios) para
  que el navegador no las renderice hasta acercarse.
- Animar solo `transform` y `opacity` (la GPU las maneja); evitar animar `width/height/top/left`.
- **Quitar el "killer" de `prefers-reduced-motion`** que congela TODAS las animaciones en
  móvil (viene en `01-propuesta.liquid`): mata los efectos en celular, que es el 80%
  del tráfico. Conservar microanimaciones suaves; respetar reduced-motion solo apagando lo
  agresivo, no todo.

## Peso
- No incrustar imágenes en base64 dentro del JSON (engorda y no cachea). Subirlas a
  Shopify/Archivos y referenciar por URL.
- Reusar el motor de animación; no duplicar el mismo CSS/JS en varios bloques.

## Checklist de rendimiento (antes de entregar)
- [ ] Fuentes con preconnect + `display=swap`, sin `@import`, solo pesos usados.
- [ ] Hero con `fetchpriority=high`; demás imágenes `loading=lazy` + `width/height`.
- [ ] Un solo motor de animación (observer compartido), sin observers duplicados.
- [ ] `backdrop-filter` solo en pocos elementos; `content-visibility:auto` en secciones largas.
- [ ] Sin killer global de `prefers-reduced-motion`.
- [ ] Sin imágenes base64 pesadas dentro del JSON.
