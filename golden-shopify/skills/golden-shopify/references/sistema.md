# El sistema de componentes

La página es un `product.json` de Shopify con dos tipos de piezas:

1. **Bloques/secciones `custom-liquid`** — HTML+CSS+JS propios. **Portables a
   cualquier tema.** Son el ~80% de la página.
2. **Piezas nativas del tema** — `title`, `description`, `related-products`,
   tickers de sección. Cambian entre temas → ver `temas.md`.

## Inventario de componentes (`references/componentes/`)

| Archivo | Qué es | Config propia | Reemplazar por producto |
|---|---|---|---|
| `00-config-center.liquid` | Paleta & marca (define tokens) + capa layout PC | vars BRAND_* | sí (marca) |
| `01-propuesta.liquid` | Hero/propuesta (badge+subtítulo). SOLO esto | — | copy |
| `sec-ignition.liquid` | **Intro cinematográfico (bloque propio, apagable, DISTINTO por página)** | IGN_* | **sí, variante** |
| `efx-header-cine.liquid` | Efecto header cinematográfico (independiente) | — | no |
| `efx-seo-cart.liquid` | SEO JSON-LD + carrito animado (independiente) | — | no |
| `efx-footer-color.liquid` | Override color del footer (independiente) | — | no |
| `03-oferta-destacada.liquid` | Banda de oferta | — | copy |
| `04-countdown.liquid` | Cuenta regresiva (off por defecto) | — | no |
| `05-verificado-google.liquid` | Sello verificado + estrellas | — | rating |
| `06-precio-dinamico.liquid` | Precio con tachado/descuento | `window.PRICE_CONFIG` | precios |
| `08-boton-compra.liquid` | Botón que dispara Releasit | `window.RELEASIT_BUTTON_CONFIG` | no |
| `09-garantia.liquid` | Compra segura / garantía | var `MODE` | copy |
| `10-barra-logistica.liquid` | Barra envío/pago/garantía | — | copy |
| `12-sticky-bar.liquid` | Sticky inferior (dispara Releasit) | `window.RELEASIT_BUTTON_CONFIG` | no |
| `sec-resenas.liquid` | Reseñas glassmorphism | `window.GFS_REVIEWS` | **sí, reseñas** |
| `sec-manifiesto.liquid` | Manifiesto cinematográfico | — | copy |
| `sec-faq.liquid` | FAQ acordeón | — | **sí, preguntas** |
| `sec-como-actua.liquid` | Sección educativa del producto | — | **SIEMPRE** |
| `sec-beneficios.liquid` | Por qué elegir? (4 beneficios) | — | copy |
| `sec-piramide.liquid` | Pirámide olfativa 3D (perfumes) | — | copy |
| `sec-escalera.liquid` | Escalera de venta (storytelling imagen+texto/GIF) | — | **sí, paneles** |
| `sec-por-que-elegir.liquid` | Trust-grid de 4 íconos por producto | — | copy |
| `sec-autoridad.liquid` | Banda de autoridad / prueba social | — | copy (placeholders) |
| `sec-cta-mid.liquid` | Doble CTA verde a media página | — | no |
| `whatsapp-flotante.liquid` | Botón flotante WhatsApp (anclado al body) | WA_* | número |
| `landing-sin-distracciones.liquid` | Oculta menú/header/footer (modo COD) | toggles | no |
| `dawn-ticker.liquid` | Ticker marquee custom-liquid | — | textos |
| `dawn-titulo.liquid` | Título como custom-liquid (variante Dawn) | — | — |

> Todos los componentes son **bloques independientes** (REGLA #5): cada uno se apaga/prende
> solo desde el editor de Shopify. El que tenía 5 cosas dentro (`01-propuesta-valor`) se separó.

## Config center: TOKENIZADO (v1.14) — ya manda de verdad

El bloque `00-config-center.liquid` declara variables Liquid y las publica como CSS custom
properties en `:root` (`--brand-primary`, `--brand-dark`, `--brand-bright`, `--brand-light`,
sus `*-rgb`, y `--cta` / `--cta-dark` / `--cta-rgb`) y como JS (`window.GFS_BRAND`).

**Desde v1.14 los componentes SÍ consumen estos tokens.** Recolorear un producto =
**cambiar las variables del config center** (y recalcular `*_RGB`); toda la página se
repinta sola. Ya **no** hay search-replace de hex. El CTA usa `var(--cta)` (verde fijo
`#1D9E06`), separado de la marca.

Verifícalo:
```
grep -c 'var(--brand' references/componentes/*.liquid   # ahora SÍ los usan
```
(El único bloque con hex literales es el config center: son los defaults editables.)

## Variables RGB
El config center también guarda tripletes RGB (`BRAND_PRIMARY_RGB = "184,38,34"`)
para usar en `rgba(...)`. Si cambias un color, recalcula su RGB
(hex→rgb) o las sombras/transparencias quedarán del color viejo.

## El NOMBRE/NÚMERO que ves en el editor sale del `"name"` del JSON (G3.17)
El rótulo que Shopify muestra en el editor de temas para cada **sección** y para cada **bloque**
sale del campo `"name"` dentro del `product.json` — **NO** del `{% schema %}` del archivo de sección
ni de comentarios en el código. Para numerar/nombrar el panel (ej. `"5 TICKER TOP"`,
`"0 CONFIG CENTER (Paleta & Marca)"`), se edita ese `"name"` de cada sección/bloque en el JSON.
Aplica igual a secciones `custom-liquid`, a `main-product` y a `related-products`.

> **Error a NO repetir:** crear archivos de sección propios (`sections/lc-NN-*.liquid`) SOLO para
> renombrar el panel es INNECESARIO — el editor ya usa el `"name"` del JSON. Cambia el `"name"`, no crees archivos.

## Reglas de estructura (convención del usuario)
- Numerar bloques del main 1..N y secciones 1..N, consecutivos (vía el campo `"name"` del JSON, ver arriba).
- Bloque **Releasit** siempre presente, etiquetado "(motor — NO TOCAR)", `disabled:true`.
- Countdown `disabled:true` por defecto. Productos relacionados últimos y off.
- `MODE="ambos"` por defecto en garantía.
- **Un solo archivo por producto.** Nunca variantes `.MEJORADO`/`.LEAN`. Editar y reentregar.
