# Estándar de movimiento Golden: los números exactos

Añadido 2026-08-26 por el chat FILTRO, a pedido directo de FER ("quiero páginas increíblemente
dinámicas"). Destilado de `review-animations` (skill instalada en el Mac que **ninguna skill de
Golden nombraba**), cuyo estándar viene de la ingeniería de diseño de Emil Kowalski.

**Hueco medido antes de escribir esto**, sobre golden-web: `ease-out` 0 menciones · `scale(0` 0 ·
`transform-origin` 0 · `@starting-style` 0 · springs 0 · regla de duración 0 · interrumpibilidad 0.
Lo único que ya estaba fuerte era `prefers-reduced-motion` (7): eso queda como está.

Este archivo sigue la misma ley que `golden-cinematica`: **tokens numéricos exactos, jamás
adjetivos**. "Suave" no es una instrucción; `cubic-bezier(0.23, 1, 0.32, 1)` sí.

## 1. Antes de animar: ¿debe animarse?

| Con qué frecuencia lo ve el usuario | Decisión |
|---|---|
| 100+ veces al día (atajos, abrir un panel) | **Nunca animar** |
| Decenas de veces al día (hover, navegar una lista) | Quitar o reducir mucho |
| Ocasional (modal, cajón, aviso) | Animación estándar |
| Raro o primera vez (bienvenida, confirmación, celebración) | Aquí sí cabe el detalle bonito |

Motivos válidos para mover algo: continuidad espacial, indicar estado, explicar, dar respuesta,
evitar un salto brusco. **"Se ve bien" no es motivo** en algo que se ve muchas veces al día.

**Para Golden esto se traduce así:** en una ficha de producto COD, la animación de entrada de la
sección de oferta es ocasional (sí anima). El hover de cada tarjeta de combo se ve decenas de
veces al bajar (reducir). El botón de "Pedir contra entrega" da respuesta al toque (sí, 160 ms).

## 2. Easing — el orden de decisión

- Entra o sale → **`ease-out`** (arranca rápido, se siente responsivo)
- Se mueve o se transforma en pantalla → **`ease-in-out`**
- Hover o cambio de color → **`ease`**
- Movimiento constante (marquesina, barra de progreso) → **`linear`**
- Si dudas → **`ease-out`**

**Nunca `ease-in` en interfaz.** Empieza lento justo en el instante que el usuario está mirando.
Un `ease-out` de 200 ms *se siente* más rápido que un `ease-in` de 200 ms.

Las curvas de CSS de fábrica son flojas. Las que se usan:

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);      /* entradas y salidas de UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);     /* movimiento en pantalla */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);      /* cajón tipo iOS */
```

## 3. Duración

| Elemento | Duración |
|---|---|
| Respuesta al pulsar un botón | 100-160 ms |
| Tooltip, globo pequeño | 125-200 ms |
| Desplegable, selector | 150-250 ms |
| Modal, cajón | 200-500 ms |
| Pieza de marketing o explicativa | Puede ser más larga |

**Regla: la interfaz se queda por debajo de 300 ms.** Un desplegable de 180 ms se siente más
responsivo que uno de 400 ms. El hero de una landing es marketing, no interfaz: ahí sí puede
respirar más.

## 4. Física — que no parezca dibujo animado

- **Nunca `scale(0)`.** Empieza en `scale(0.9)` a `scale(0.97)` con `opacity: 0`. Nada en el mundo
  real aparece de la nada.
- **El popover nace donde lo abriste**, no en el centro: `transform-origin` en el disparador.
  Los modales son la excepción: aparecen centrados y se quedan con `transform-origin: center`.
- **Respuesta al pulsar:** `transform: scale(0.97)` en `:active` con `transition: transform 160ms
  ease-out`. Sutil (0.95-0.98). Vale para cualquier cosa pulsable, y en COD el botón de pedido es
  el elemento más pulsado de la página.

## 5. Springs (cuando el movimiento debe sentirse vivo)

No tienen duración fija: se asientan por física. Para arrastre con inercia y elementos "vivos".

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }   // estilo Apple, más fácil de razonar
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // física clásica, más control
```

Rebote discreto: **0.1 a 0.3**. En la mayoría de la interfaz, sin rebote. Un rebote alegre en el
botón de compra resta seriedad justo donde el cliente decide dar su dirección sin haber pagado.

## 6. Interrumpibilidad

Las **transiciones** CSS se pueden interrumpir y reapuntar a mitad de camino. Los **keyframes**
reinician desde cero. Para cualquier cosa que se dispare rápido y repetido, transiciones.

Entrada sin JavaScript:

```css
.aviso {
  opacity: 1; transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

## 7. Tiempo asimétrico

Lento donde el usuario decide, rápido donde el sistema responde.

```css
.overlay              { transition: clip-path 200ms ease-out; }  /* soltar: rápido */
.boton:active .overlay{ transition: clip-path 2s linear; }       /* mantener: lento, deliberado */
```

## 8. Rendimiento — lo que más pesa en Golden

**El 74% del tráfico LatAm de Golden compra en móvil**, muchas veces en gama media con la red
justa. Una animación que salta frames no es un detalle estético: es una ficha que se siente barata
justo antes de pedir la dirección.

- **Anima solo `transform` y `opacity`.** Se saltan layout y paint y corren en la GPU.
  `padding`, `margin`, `height`, `width`, `top` y `left` disparan las tres etapas de render.
- **No muevas los hijos con una variable CSS del padre**: recalcula estilos de todos los hijos.
  ```js
  element.style.setProperty('--swipe', `${d}px`); // mal: recalcula en todos los hijos
  element.style.transform = `translateY(${d}px)`; // bien: solo este elemento
  ```
- **Los atajos de Framer Motion NO van por hardware.** `x`, `y` y `scale` corren en el hilo
  principal por rAF y pierden frames bajo carga. Hay que escribir el transform completo:
  ```jsx
  <motion.div animate={{ x: 100 }} />                          // pierde frames
  <motion.div animate={{ transform: "translateX(100px)" }} />  // acelerado por hardware
  ```
- **CSS gana a JS bajo carga**: corre fuera del hilo principal. Para movimiento predeterminado, CSS.
- **WAAPI** da control desde JS con rendimiento de CSS, sin librería:
  ```js
  element.animate(
    [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
  );
  ```

## 9. Lo que ya estaba bien y no se toca

`prefers-reduced-motion` ya aparece 7 veces en esta skill. Se mantiene: quien pidió menos
movimiento en su sistema debe recibir menos movimiento, y eso manda sobre todo lo de arriba.

## Dónde vive cada cosa

- El **vocabulario de efectos** (cómo pedirlos por su nombre: parallax, pin, scroll-linked,
  horizontal scroll, partículas) está en `golden-cinematica/references/vocabulario.md`.
- Las **escenas 3D reales** son de `golden-cinematica`.
- Este archivo es **el estándar de CÓMO se mueve** cualquier cosa: cuánto dura, con qué curva,
  desde dónde nace y por qué no salta frames.
- Auditar una animación ya escrita: la skill `review-animations` (está instalada, no se dispara
  sola, hay que llamarla por nombre).
