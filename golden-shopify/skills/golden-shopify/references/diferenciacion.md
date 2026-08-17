# Regla de diferenciación — cada página DEBE ser distinta

**Principio innegociable:** dos productos NUNCA pueden quedar como la misma página
con otro color y otras fotos. Pueden compartir **identidad de sistema** (calidad,
convención de bloques, motor Releasit, config center) pero el **diseño visible tiene
que ser distinto**: distinto layout, distintas secciones, distintos bloques, distinta
sensación — adaptado a ESE producto.

## Por qué
La base PRODUCTO DEMO aporta el **MOTOR** (Releasit, precio dinámico, config center, convención
EDITAR/NO TOCAR, JSON-LD), NO el **ASPECTO**. Clonar el aspecto produce páginas espejo
que se ven en serie, bajan la percepción de marca y aburren. Cada producto merece su
propia puesta en escena.

## Las palancas (usa VARIAS en cada página, no todas iguales que la anterior)

1. **Orden y selección de secciones.** No siempre ticker→producto→cómo actúa→reseñas→
   manifiesto→FAQ. Reordena, omite, inserta. Una página puede abrir con `image_banner`,
   otra con propuesta de valor a pantalla, otra directo al producto.

2. **Sección educativa ÚNICA por producto.** No repetir el mismo formato. Elegir el que
   encaje con el producto:
   - Pirámide olfativa (perfume) · Mecanismo "cómo actúa" (suplemento) ·
     Comparativa nosotros-vs-otros · Antes/después · Pasos de uso (1-2-3) ·
     Ingredientes/activos · Tabla de beneficios · Timeline de resultados.
   - Si dos productos llevan "cómo actúa", que el LAYOUT sea distinto (vertical vs
     escalonado vs tarjetas vs split).

3. **Hero distinto.** image_banner nativo · propuesta custom full-width · título XXL con
   fondo · video/imagen con overlay. No el mismo hero dos veces seguidas.

4. **Tipografía por vertical** (ver combos en `efectos-premium.md`):
   Perfume → Playfair+Montserrat · Salud → Cormorant+DM Sans · Lujo → Bodoni+Inter ·
   Tech/moderno → Inter/Montserrat. Cambiar el pairing cambia toda la cara.

5. **Paleta que se IDENTIFIQUE con el producto.** No reusar el verde de marca-demo ni el
   rojo de PRODUCTO DEMO por inercia. El color debe "sonar" al producto.

6. **Efectos NO siempre los mismos.** Reparte del catálogo: una con tilt 3D, otra con
   glassmorphism marcado, otra con partículas, otra minimalista sin efectos pesados.

7. **Layout de reseñas / FAQ / beneficios variado.** Grid vs carrusel vs reseña
   destacada; acordeón vs tarjetas abiertas; 4 columnas vs 2 filas, etc.

8. **Manifiesto opcional y propio.** Cuando se use, estructura y tono propios del
   producto; no el mismo "3 escalones + cierre" calcado.

## Chequeo antiespejo (antes de entregar)
Compara la página nueva contra las ya hechas (en `examples/` y en las plantillas previas).
Pregúntate: *"si le quito color e imágenes, se distingue de la anterior?"* Si la
respuesta es no → cambia al menos **3 palancas** de arriba (orden de secciones, sección
educativa, hero, tipografía o layout de reseñas) antes de entregar.

## Lo que SÍ se mantiene constante (no confundir diferenciación con inconsistencia)
- El motor Releasit/COD y la convención de código (`📝 EDITAR AQUI` / `NO TOCAR`).
- El config center y los config-driven (PRICE_CONFIG, RELEASIT_BUTTON_CONFIG, MODE).
- Las reglas de oro (copy/legal) y la calidad/acabado.
- La validez técnica del JSON y el adaptador de tema.
