# Arquetipos de página (qué montar según el producto)

Comparando las 5 páginas reales hechas hasta hoy, emergen **3 arquetipos**. No toda
página lleva todo: elige el arquetipo por vertical y de ahí activas/desactivas
componentes. Esto evita páginas genéricas y reduce trabajo.

## A) PERFUME / BELLEZA / LUJO
Ejemplos: `Producto Demo`, `marca-demo-essence` (Dawn, verde #0F6F5C).
- **Tipografía:** Playfair Display (títulos) + Montserrat (cuerpo).
- **Componentes clave:** `sec-piramide.liquid` (pirámide olfativa 3D con tilt),
  `sec-manifiesto.liquid` (momento emocional), `sec-resenas.liquid`, partículas, tilt 3D.
- **Copy:** emocional/deseo (ver `reglas-de-oro.md`). NUNCA "original/réplica".
- **NO** suele necesitar barra logística agresiva ni comparativas técnicas.

## B) SALUD / COSMÉTICA FUNCIONAL (lean)
Ejemplos: `Producto Demo` (azul #2B80FF), `verrugas` (naranja #F7A540).
- **Más sobrio, menos secciones emocionales.** Foco en claridad y conversión rápida.
- **Componentes clave:** `image_banner` nativo (hero arriba del producto),
  precio dinámico (`PRICE_CONFIG`), countdown, sticky, FAQ. Pocas o ninguna reseña/
  manifiesto/pirámide.
- **Copy:** expectativas REALISTAS (ej. Producto Demo = fibra que cubre, no tratamiento).
- **Estructura más corta:** 5–7 secciones, 11 bloques main.

## C) VITALIDAD / SUPLEMENTO (full, el más completo)
Ejemplo: `producto-demo` (Shrine, rojo #b82622). **Es la BASE de la skill.**
- Trae TODO lo técnico: **config center**, `PRICE_CONFIG`, `RELEASIT_BUTTON_CONFIG`,
  **override Releasit con MutationObserver**, **JSON-LD**, sección educativa
  "cómo actúa", reseñas, manifiesto, FAQ, beneficios, sticky.
- Es el punto de partida; para A o B se podan/cambian secciones.

## D) GADGET / DEMOSTRACIÓN (físico que se ve funcionar)
Ejemplos reales: gadget perfumador (perfume auto), cubre-rayones (cubre-rayones), espejo LED (espejo).
- **El producto se VENDE mostrándolo en acción.** El motor es la **escalera de venta**
  (`sec-escalera.liquid`) con GIFs/antes-después: cada panel = 1 beneficio que mata 1 objeción.
- Apertura tipo PAS: 2–3 preguntas-dolor encadenadas (kickers de la escalera) antes de la solución.
- Tono según comprador (ver presets en `reglas-de-oro.md`): lujo / DIY-ahorro / belleza.
- Cierra con `sec-por-que-elegir.liquid` personalizado al beneficio + doble CTA.

## E) KIT / ESCALERA DE VALOR (sube ticket componiendo productos)
Ejemplo real: Kit capilar completo (Fibra + Atomizador + Fijador) a $149.900 (antes $259.700).
**Distinto del bundle 2x/3x** (eso lo maneja el Releasit COD Form, ver `releasit-cod.md`):
un KIT es un producto/landing propio que **compone varios productos diferentes**.
- **Ancla de precio = suma de partes:** el `compare_at_price` ≈ precios individuales sumados,
  así el ahorro absoluto en pesos (💸 "$109.800") es el héroe del hero.
- **Desglosa qué hace cada componente** + su mini modo-de-uso (reduce el miedo a "no sé usarlo").
- Posiciónalo como el upgrade "profesional / cobertura total" del producto de enganche.
- El producto barato es la puerta de entrada; el kit es donde está el margen.

## Matriz: qué activar por arquetipo
| Componente | A Perfume | B Salud lean | C Vitalidad full | D Gadget/Demo | E Kit |
|---|---|---|---|---|---|
| config center | ✓ | ✓ | ✓ | ✓ | ✓ |
| image_banner hero | — | ✓ | opcional | opcional | opcional |
| eyebrow de beneficio | opcional | ✓ | ✓ | ✓ | ✓ |
| pirámide olfativa | ✓ | — | — | — | — |
| sección "cómo actúa" | — | opcional | ✓ | opcional | ✓ |
| **escalera de venta** (`sec-escalera`) | opcional | opcional | ✓ | ✓ | ✓ |
| manifiesto | ✓ | — | ✓ | opcional | — |
| reseñas | ✓ | opcional | ✓ | ✓ | ✓ |
| **por qué elegir?** (`sec-por-que-elegir`) | ✓ | ✓ | ✓ | ✓ | ✓ |
| **banda de autoridad** (`sec-autoridad`) | opcional | opcional | ✓ | ✓ | ✓ |
| **ficha técnica** (`sec-ficha-tecnica`) | — | opcional | opcional | ✓ | ✓ |
| countdown | ✓ | ✓ | ✓ | ✓ | ✓ |
| doble CTA (compra a media página) | opcional | opcional | ✓ | ✓ | ✓ |
| sticky | ✓ | ✓ | ✓ | ✓ | ✓ |
| PRICE_CONFIG | ✓ | ✓ | ✓ | ✓ | ✓ |
| JSON-LD | ✓ | ✓ | ✓ | ✓ | ✓ |
| tilt 3D / partículas | ✓ | — | ✓ | opcional | — |

## Piezas nativas útiles detectadas
- **`image_banner`** (de Producto Demo): hero nativo de Dawn/Shrine arriba del producto.
  Settings: `image`, `image_height`, `image_overlay_opacity`, `desktop_content_position`,
  `show_text_box`, `color_scheme`. Útil para arquetipo B. No requiere custom-liquid.
- **`featured-collection` premium** (de Producto Demo): relacionados con `custom_css`
  premium (cards con hover lift, badges rojos, animación de entrada escalonada).
  CSS listo en `assets/related-products.premium.css.txt`.

## CHECKLIST DE PÁGINA GANADORA (v1.19 — absorbido de la tienda real)
En la tienda auditada, la diferencia entre una página que VENDE (Fibra/Full Kit, sérum facial,
espejo LED) y una ficha cruda que no (mascarilla verde, tratamiento capilar) NO es el tema ni el color —
es la presencia de estos 5 elementos. Aplícalos por defecto en arquetipos C/D/E:
1. **Countdown real** activo (evergreen ~15 min), no solo texto "por tiempo limitado".
2. **Garantía COD redactada en humano** ("Pagas al recibir, en la puerta de tu casa, sin
   transferencias ni adelantos. Producto original y sellado.") justo bajo el CTA.
3. **Escalera de venta con GIFs / antes-después** (`sec-escalera.liquid`): el producto se
   muestra funcionando; cada panel mata una objeción.
4. **CTA personalizado al producto + doble CTA** ("QUIERO MI [PRODUCTO] 🔥" en hero y a media página).
5. **Escalera de valor hacia el kit** cuando el producto lo permita (arquetipo E).
Ventaja sobre el competidor: ellos clonan UN esqueleto y meten el copy dentro de imágenes
(malo para SEO/edición). Nuestras páginas usan texto real + precio dinámico + REGLA #1
(cada página distinta) → más mantenibles y diferenciadas.

## Lo que AÚN no existe en ninguna página (oportunidades reales = roadmap)
Pendientes: **video/animación embebido**, **lottie**, **fila de trust badges** como sellos.
(✅ Ya construidos: escalera de venta, por qué elegir? por producto, banda de autoridad,
botón flotante de WhatsApp. Los bundles 2x/3x van en el Releasit COD Form, no en la página.)
