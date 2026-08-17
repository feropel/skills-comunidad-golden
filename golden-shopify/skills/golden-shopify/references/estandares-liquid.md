# Estándares de código Liquid Golden

> Reference original de golden-shopify. Define el "código sano" que TODO bloque
> `custom_liquid` y toda sección/plantilla debe cumplir: correcto, accesible y rápido.
> Conocimiento redactado para Golden (no derivado de terceros).

**REGLA DURA:** antes de escribir cualquier bloque, cumple este documento. Si un bloque
no pasa el checklist final, no se entrega.

---

## 1. Arquitectura: sección vs bloque vs snippet

- **Sección** = unidad grande con su propio `{% schema %}`; el merchant la agrega/mueve en el editor.
- **Bloque** = pieza dentro de una sección (`blocks` en el schema); reordenable y repetible.
- **Snippet** = fragmento reutilizable que se incluye con `{% render 'nombre' %}` (NO `{% include %}`, obsoleto).
- En el modelo de golden-shopify la mayoría de piezas viven como **bloques `custom_liquid`** dentro de
  `main-product` → portables entre temas. Mantén cada bloque **autocontenido** (su HTML + su `<style>`).

**Cuándo cada uno:**
- Se repite en varias páginas con datos distintos? → snippet con parámetros.
- El merchant debe encender/mover/duplicar la pieza? → bloque.
- Es estructura de página completa? → sección.

## 2. Schema JSON correcto

- Cada `setting` con `type` válido (`text`, `richtext`, `range`, `select`, `checkbox`, `color`,
  `image_picker`, `url`, `product`, `collection`…), `id` único y `label`.
- Usa `range` (con `min`/`max`/`step`/`unit`) en vez de pedir números a mano.
- `presets` para que la sección/bloque aparezca lista en el editor con valores por defecto sensatos.
- `enabled_on`/`disabled_on` por plantilla cuando aplique (ej. solo en `product`).
- Respeta los **límites**: máx. settings/bloques razonables; no inflar el schema.
- Valida el JSON: una coma de más rompe el tema. Llaves y comillas balanceadas.

## 3. Traducciones (nunca texto hardcodeado)

- En código de tema nativo, el texto va por claves: `{{ 'sección.clave' | t }}` y locales en `/locales`.
- En bloques `custom_liquid` de Golden, el equivalente es la zona **"EDITAR AQUÍ"** con `{% assign %}`:
  todo texto editable arriba, separado del motor. Nunca texto suelto enterrado en el HTML.
- Esto permite traducir/duplicar sin tocar el diseño.

## 4. CSS dentro de bloques

- **BEM con prefijo único por bloque** para no colisionar con el tema:
  `.gfs-faq__q`, `.tr-bc__b`. Un prefijo corto e irrepetible por componente.
- **Design tokens**: hereda de la Paleta con CSS custom properties
  (`var(--brand-primary)`, `var(--cta)`), con **fallback**: `var(--brand-primary,#f7a540)`.
  Así el bloque funciona aunque falte el bloque de Paleta.
- **CSS defensiva**: estiliza solo TUS clases; no toques selectores globales del tema salvo override
  consciente y documentado. Evita `*`, `body`, `img` sin scope.
- **`!important` solo** para sobrescribir estilos del tema, y comentado por qué.
- **Scope estricto**: prefijo en el contenedor raíz del bloque y todo cuelga de ahí.

## 5. JavaScript: mínimo y progresivo

- Por defecto **CSS-only**. JS solo si aporta valor real (acordeón, slider, cuenta regresiva).
- **Progressive enhancement**: la pieza debe verse y leerse aunque el JS no cargue.
- Para interactividad reutilizable, usa **Web Components / custom elements** (encapsulan estado y
  no ensucian el global). Nada de librerías pesadas (jQuery, frameworks) en un bloque.
- `defer`/al final; jamás bloquees el render. No `document.write`. No `eval`.
- Limpia listeners; usa delegación cuando haya muchos nodos.

## 6. Rendimiento (complementa references/rendimiento.md, no lo dupliques)

- `content-visibility:auto` + `contain-intrinsic-size:auto Xpx` en bloques largos (ya es patrón Golden).
- Imágenes con `loading="lazy"`, `decoding="async"`, `width/height` o `aspect-ratio` para **evitar CLS**.
- Anima **solo** `transform` y `opacity` (no `width/height/top`). Usa `will-change` con moderación.
- Respeta `@media (prefers-reduced-motion: reduce)`: desactiva animaciones de entrada.
- Cero fuentes extra por bloque; usa la del tema (`font-family:inherit`).
- HTML semántico y liviano; no anidamientos absurdos.

## 7. Accesibilidad (WCAG 2.2 para ecommerce)

- **Foco visible** y orden lógico de tabulación; nada interactivo solo con el mouse.
- **Contraste** suficiente texto/fondo (AA): cuida el CTA y los badges.
- **Imágenes**: `alt` descriptivo (vacío `alt=""` solo si es decorativa).
- **Formularios**: cada input con `<label>` asociado; errores anunciados.
- Patrones por componente:
  - **Acordeón/FAQ**: `<details>/<summary>` nativo, o `button` + `aria-expanded`.
  - **Carrusel**: controles con `aria-label`, navegable por teclado, sin autoplay que atrape el foco.
  - **Cart drawer / modal**: `role="dialog"`, `aria-modal="true"`, foco atrapado dentro, cierra con `Esc`.
  - **Precio/stock dinámico**: `aria-live="polite"` para anunciar cambios.
  - **Sticky bar / countdown**: no debe tapar contenido ni el foco.
- Iconos emoji decorativos: `aria-hidden="true"`.
- **Contraste de emoji vs su fondo (G3.17):** ningún emoji debe ser del **mismo color que el fondo sobre
  el que va** (un ✅/💚 verde sobre botón verde se pierde). Elige un emoji **contrastante** con ese fondo
  (ej. sobre CTA verde usa 🔥/✨/👉, no 💚). Regla para TODA la página, no solo el CTA.

## 8. Checklist "código sano" (antes de entregar cada bloque)

- [ ] Texto editable arriba en "EDITAR AQUÍ"; nada hardcodeado abajo.
- [ ] Clases con prefijo único (BEM); sin colisión con el tema.
- [ ] Usa tokens de Paleta con fallback.
- [ ] Schema JSON válido (si aplica) y con preset.
- [ ] Imágenes lazy + dimensiones (sin CLS).
- [ ] Animaciones solo transform/opacity + `prefers-reduced-motion`.
- [ ] Accesible: foco, contraste, alt, labels, roles del patrón.
- [ ] JS mínimo, con degradación elegante (o cero JS).
- [ ] `content-visibility` en bloques largos.
- [ ] Probado mobile y desktop.
