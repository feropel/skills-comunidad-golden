# Checklist final (antes de entregar el product.json)

Corre esto SIEMPRE antes de dar por terminado un producto.

## Render visual (OBLIGATORIO — antes de declarar lista la página)
- [ ] **Vi la página RENDERIZADA** (screenshot del storefront), no solo validé el JSON.
      Prohibido decir "100/100" sin haberla mirado con los ojos.
- [ ] **Armonía:** máximo 2 colores fuertes y UN solo color de acción. No hay verde +
      naranja + rojo apilados. Un único acento de urgencia (si countdown rojo, oferta/badge
      NO van de otro color). Ver Regla 0 en `reglas-de-oro.md`.
- [ ] Respeté la **instrucción explícita de color del usuario** (pisa REGLA #2 / "badges rojo").

## Botón de compra (REGLA #2)
- [ ] **El botón de compra es VERDE GANADOR `#1D9E06`** (y el sticky igual). Salvo que el
      usuario pida otro color. Verifiqué que no quedó del color viejo (#b82622, etc.).
- [ ] **Test de 1 vistazo:** al abrir la página (desktop y móvil) el ojo va directo al
      botón de compra. Es el elemento de mayor contraste (con sombra/realce si el fondo es verde).
- [ ] El CTA NO se pierde contra el fondo/secciones (destaca sobre todos los colores).
- [ ] WhatsApp queda verde #25D366 (burbuja flotante). Si el CTA también es verde, es un
      verde distinto y no están pegados (no se confunden por forma/posición).
- [ ] El sticky inferior usa el mismo color de acción del CTA. Secundarios discretos.

## Página ganadora (arquetipos C / D / E — productos de demostración o ticket alto)
Los 5 elementos que separan una landing que vende de una ficha cruda (ver `arquetipos.md`):
- [ ] **Countdown real** activo (evergreen ~15 min), no solo texto "por tiempo limitado".
- [ ] **Garantía COD humana** bajo el CTA ("Pagas al recibir, en la puerta de tu casa…").
- [ ] **Escalera de venta** (`sec-escalera.liquid`) con GIFs/antes-después: cada panel mata una objeción.
- [ ] **CTA personalizado** ("QUIERO MI [PRODUCTO] 🔥") + **doble CTA** (hero y media página).
- [ ] **Escalera de valor / kit** ofrecida si el producto lo permite (arquetipo E).
- [ ] **Tono coherente con el ángulo** (lujo / DIY-ahorro / belleza / salud) en copy + emojis + CTA.
- [ ] Si es vertical sensible (íntimo / antiedad / hongos): copy compliant, sin claim médico riesgoso.

## Diferenciación (REGLA #1)
- [ ] **Chequeo antiespejo:** si le quito color e imágenes, se distingue de las páginas
      ya hechas? Si no → cambié al menos 3 palancas (orden de secciones, sección educativa,
      hero, tipografía, layout de reseñas). Ver `diferenciacion.md`.
- [ ] La sección educativa es la que encaja con ESTE producto (no la misma de la anterior).
- [ ] La paleta y tipografía se identifican con el producto, no heredadas por inercia.

## Bloque 1 / Intro
- [ ] **El intro IGNITION** (cortina cinematográfica 100% CSS del bloque 1 / propuesta) está
      presente — NO se quita al reescribir el copy, salvo que el usuario lo pida. Vive embebido
      en `01-propuesta.liquid`; verifica que `gfs-ignition` siga en el JSON.

## Contenido
- [ ] Revisé la URL del producto y **no dupliqué** reseñas / cómo-usar / beneficios
      que ya estén en la descripción nativa.
- [ ] Las reseñas propias son **personas distintas** a las de la descripción.
- [ ] La sección educativa (`sec-como-actua`) está **reescrita para ESTE producto**
      (no quedó copy de PRODUCTO DEMO/marca-demo).
- [ ] Copy de propuesta, oferta, garantía, FAQ alineado al producto y mercado.

## Marca / colores
- [ ] Config center actualizado: `BRAND_NAME`, colores `BRAND_*` + `*_RGB`, `CTA_BG`,
      WhatsApp, reviews. (v1.14 tokenizado: con esto se repinta toda la página, sin search-replace.)
- [ ] Recalculé los tripletes `*_RGB` para los colores nuevos (se usan en `rgba(var(--..-rgb))`).
- [ ] Si partí de un componente/página VIEJA (pre-v1.14) con hex hardcodeados, la tokenicé.

## Config-driven
- [ ] `window.PRICE_CONFIG` con los precios reales.
- [ ] `window.RELEASIT_BUTTON_CONFIG` con los colores de botón correctos.
- [ ] `MODE` correcto (`ambos`/`contraentrega`/`anticipado`).

## Estructura
- [ ] Bloque **Releasit** presente, `disabled: true`, etiquetado "(motor — NO TOCAR)".
- [ ] Countdown `disabled: true` (salvo que el usuario lo quiera activo).
- [ ] Productos relacionados al final, desactivado por defecto.
- [ ] Bloques 1..N y secciones 1..N numerados consecutivos.
- [ ] Cada bloque conserva la convención `📝 EDITAR AQUI` / `NO TOCAR DE AQUI HACIA ABAJO`.

## Tema
- [ ] Apliqué el adaptador de `temas.md` para el tema correcto.
- [ ] Si NO es Shrine: quité `horizontal-ticker`, `title_highlight_color`,
      `arrows_color_scheme`, `transparent_arrows`; footer override usa `.footer`.
- [ ] Tickers correctos para el tema (nativo en Shrine / `custom-liquid` en Dawn/Sense).

## Rendimiento (ver rendimiento.md)
- [ ] Fuentes con preconnect + `display=swap` (sin `@import`), solo pesos usados.
- [ ] Hero `fetchpriority=high`; demás imágenes `loading=lazy` + `width/height` (sin CLS).
- [ ] Un solo motor de animación; sin killer global de `prefers-reduced-motion`.

## Calificación
- [ ] La estrella/rating muestra el valor REAL (ej. 4.8/5), **nunca "0.0/5"**. Los contadores
      animados (`.pe-counter`) arrancan con su valor final como texto, no en 0.0.

## Anti-invención (REGLA #3)
- [ ] No hay reseñas/rating/claims/precios/tiempos inventados. Lo que faltó se preguntó o
      quedó como placeholder evidente, nunca como dato falso que parezca real.

## Validez técnica
- [ ] El JSON parsea (ojo: estos archivos llevan un comentario `/* ... */` al inicio
      y pueden tener saltos de línea dentro de strings → validar con
      `json.loads(raw, strict=False)` tras quitar el comentario).
- [ ] Ningún `#0000000` (7 ceros) ni typos como "CONFÍANZA".

## Sello y nota interna
- [ ] Sello de versión arriba (config center) con la versión actual.
- [ ] **Nota interna al final** (último bloque, comentario HTML) con **fecha y hora reales
      de generación** — invisible para el cliente, NO después del `}` final del JSON.

## Entrega
- [ ] **UN solo archivo** `product.<slug>.json`. Sin variantes `.MEJORADO`/`.LEAN`.
