# Releasit COD + botones

El sistema de pago es **Releasit COD Form** (contra entrega). El patrón clave:

## Arquitectura del botón
- El **bloque app oficial de Releasit** va SIEMPRE incluido pero **oculto**
  (`disabled: true`). Es el MOTOR del formulario COD. **NO se borra.**
- Un **botón custom** (`08-boton-compra.liquid`, `#custom-releasit-btn`) hace
  click programático sobre el botón real de la app:
  `#_rsi-buy-now-button-overwrite, ._rsi-buy-now-button`.
- El **sticky** (`12-sticky-bar.liquid`) dispara el mismo `#custom-releasit-btn`.

## Bundles / cantidades (2x, 3x) — viven en el FORMULARIO de Releasit
Las ofertas por cantidad (2x, 3x con descuento) **se configuran dentro del Releasit COD
Form** (sus "Quantity offers" / upsells del formulario), NO como un componente de la página.
- **NO construir** un selector de cantidad/bundle en el `product.json`. La página solo
  dispara el formulario; el cliente elige 1x/2x/3x dentro del form de Releasit.
- En el copy/oferta de la página se puede *mencionar* el ahorro por llevar más (ej.
  "Lleva 2 y ahorra"), pero la mecánica del bundle la maneja Releasit.
- Por eso "bundle" salió del roadmap de componentes: ya está resuelto por la app.

## Fallback del CTA a `/cart/add` — REGLA PERMANENTE en toda página (G4.2)
Aprendido en tienda real (chat Insulinum, 2026-08-07): si Releasit no está en la página
(app desinstalada, bloqueada por el navegador, o que aún no inyectó), el botón custom no
tenía a quién disparar y **no hacía nada** — un CTA muerto justo en la puerta de venta.
Desde G4.2, **TODO CTA de compra lleva fallback al formulario nativo `/cart/add`**, en
cualquier tema (no solo Horizon):
- Al clic, el botón busca el botón real de Releasit
  (`#_rsi-buy-now-button-overwrite, ._rsi-buy-now-button`). Si está, lo dispara como siempre.
- Si NO está, **espera ~1,5 s** (por si la app inyecta tarde) reintentando la búsqueda.
- Si tras la espera sigue sin aparecer, **cae al flujo nativo**: `POST /cart/add` con el
  `variant id` actual (fetch a `/cart/add.js` o submit de un `<form action="/cart/add">`
  oculto) y redirige a `/cart`. El cliente SIEMPRE puede comprar.
- Aplica al CTA principal, al sticky y a los `sec-cta-suelto`: todos disparan
  `#custom-releasit-btn`, así que el fallback vive UNA vez, dentro del botón custom
  (`08-boton-compra.liquid`), y cubre todas las puertas.
- Complementa la REGLA #2 del SKILL.md: el botón siempre sobresale... y siempre FUNCIONA
  aunque la app falte.

## MODE (Compra Segura / garantía — `09-garantia.liquid`)
Variable `MODE`:
- `ambos` (DEFAULT) → contra entrega + pago anticipado.
- `contraentrega` → solo COD.
- `anticipado` → solo pago anticipado.

## Override de colores de los botones Releasit
La app pinta sus botones con estilos **inline `!important`**, así que CSS normal no
los repinta. Solución probada: JS con `MutationObserver` + `setProperty(...,'important')`.
Config en `window.RELEASIT_BUTTON_CONFIG` (`08-boton-compra.liquid` / sticky):
- `RSI_PRIMARY_BG`, `RSI_SECONDARY_BG` (vacío = no tocar), `RSI_TEXT`.

⚠️ **Crítico — anclar selectores para NO tocar el downsell:** hay **3** botones
`_rsi-modal-submit-button` en la página (form COD, downsell, otro). Anclar al ancestro:
- COD: `._rsi-build-block-submit-button ._rsi-modal-submit-button`
- MercadoPago: `._rsi-build-block-custom-button ._rsi-buy-now-custom-additionals-button`

## El botón flotante teal de Releasit (gotcha conocido)
Releasit añade un botón FLOTANTE propio (`#_rsi-buy-now-button-floating`), color
teal `#347b77`, puesto INLINE con `!important` → no se repinta con CSS. En PRODUCTO DEMO se
**ocultó** (`display:none !important`) para dejar solo nuestro sticky. Para
recolorearlo de verdad: Releasit app → Buy Now Button → color.

## Brillo del botón (shine sweep)
`::before` con gradiente blanco semitransparente animado por
`@keyframes ggBtnShine` (cruza cada ~3.5s). Vive dentro de `08-boton-compra.liquid`.

## Bugs históricos ya resueltos (no reintroducir)
- Ticker bot tenía `#0000000` (7 ceros) → debe ser `#000000`.
- Typo "CONFÍANZA TOTAL" → "CONFIANZA TOTAL".
