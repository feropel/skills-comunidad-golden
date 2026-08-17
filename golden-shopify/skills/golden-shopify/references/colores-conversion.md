# Colores para conversión — cómo recomendar

Cuando el cliente NO tiene color definido (o pide recomendación), elige el color
**enfocado al producto**: el que más vende, más persuade y más genera **impulso de
compra** para ese vertical. Siempre propón **1 recomendado + 1 alternativa** y deja que
el cliente decida.

## Principio
El color de marca da identidad; el **CTA y los acentos de urgencia** son los que
empujan la compra. Aunque la marca sea sobria, el **botón de compra y los badges de
oferta** deben ser de un color de acción y alto contraste (rojo/naranja/verde vivo).

## Guía rápida por psicología / vertical
| Color | Dispara | Va bien con | Ejemplo |
|---|---|---|---|
| **Rojo** | urgencia, impulso, energía, deseo | vitalidad, ofertas, COD impulsivo, picante | PRODUCTO DEMO `#b82622` |
| **Naranja / ámbar** | urgencia amigable, accesible, acción | salud accesible, "compra ya", combos | verrugas `#F7A540` |
| **Verde** | salud, natural, bienestar, confianza, "dinero" | suplementos, natural, orgánico, perfumes frescos | marca-demo `#0F6F5C` |
| **Azul** | confianza, limpieza, médico, tecnología | cosmética funcional, salud seria, tech | Producto Demo `#2B80FF` |
| **Dorado / negro** | lujo, premium, elegancia | perfume de lujo, fashion, alta gama | Golden dorado |
| **Rosa / magenta** | belleza, femenino, romance, deseo | cosmética femenina, perfume floral | — |
| **Morado** | premium asequible, místico, antiedad | antiedad, esotérico, suplementos premium | — |

## Lógica de recomendación
1. Identifica el **vertical** del producto (vitalidad, perfume, salud, belleza, tech…).
2. Recomienda el color de mayor **impulso** para ese vertical (tabla arriba).
3. Para **impulso máximo de compra** (productos de antojo/COD), inclínate por rojo o
   naranja en el CTA aunque la marca use otro color de fondo.
4. Da el `primary` recomendado + deriva `dark` (más oscuro), `bright` (más vivo, acentos)
   y `light` (tint claro para fondos), y calcula sus tripletes RGB para el config center.
5. Para venta COD impulsiva: badges de oferta SIEMPRE en rojo (`#ef4444 → #dc2626`),
   contraste alto, sin importar el color de marca.

## Jerarquía del CTA (REGLA #2 — el botón de compra SIEMPRE sobresale)
El botón de compra es el elemento más visible de la página, sin excepción.
- **COLOR FIJO: verde ganador `#1D9E06`** (oscuro `#157A04`), en TODO producto, salvo orden
  expresa del usuario. La guía de colores por vertical de arriba aplica a la **marca/acentos**
  de la página, **NO al CTA** (el CTA siempre es este verde porque es el que más convierte).
- **Debe seguir destacando:** si la página tiene mucho verde, asegurar contraste del CTA con
  tamaño, sombra de profundidad y `shine sweep` para que no se pierda contra fondos verdes.
- **WhatsApp siempre verde `#25D366`** (redondo, flotante — convención universal). El CTA
  puede ser verde también: NO se confunden porque difieren en forma/tamaño/posición/ícono.
  Si ambos quedan verdes, dale al CTA un verde de marca distinto (más vivo/oscuro) y no los
  pongas pegados. Lo esencial: el CTA destaca sobre las SECCIONES y fondos de la página.
- **Realce obligatorio:** tamaño grande, peso 800, `shine sweep`, sombra de profundidad,
  hover/active marcados. El **sticky inferior repite el mismo color** del CTA.
- **Secundarios discretos:** "ver más", "info", links → estilo plano/outline, jamás
  compiten con el botón de compra.
- **Test de 1 vistazo:** al abrir la página (desktop y móvil), el ojo debe ir directo al
  botón de compra. Si no, sube contraste/tamaño hasta que destaque.
- Mapa rápido marca → CTA sugerido: verde→rojo/naranja · azul→naranja/verde lima ·
  dorado/negro→dorado brillante o rojo · rosa→magenta/rojo · rojo→rojo vivo (+sombra fuerte).

## Armonía de paleta — máximo 2 colores fuertes (leer junto a REGLA #2)
La REGLA #2 (CTA sobresale) NO significa "mete un matiz nuevo". **"Destacar" = contraste
de brillo / tamaño / sombra**, no necesariamente cambio de tono:
- Un **CTA verde profundo/brillante** sobre secciones verde claro YA destaca. No hace
  falta naranja ni rojo si la marca/producto es verde.
- **Tope duro: 2 colores fuertes simultáneos** y **un único color de acción** (el CTA).
  Si apilas verde + naranja + rojo (botón naranja + caja roja + countdown rojo + badge rojo),
  se ve "circo de descuento" y choca. Caso real fallido: un sérum facial (ejemplo) v1.8.
- **Un solo acento de urgencia.** Si el countdown ya marca urgencia, la caja de oferta y el
  badge de precio se quedan en el color de marca o neutros — no agregues un segundo rojo.
- **La instrucción explícita del usuario sobre color manda** sobre esta tabla y sobre
  "badges en rojo" (ver Regla 0 en `reglas-de-oro.md`).
- **Verticales naturales / botánicos / salud:** armonía monocromática del color del
  producto + a lo sumo un acento cálido pequeño; evita la "alarma roja".

## Importante
- El color debe **identificarse con el producto** (ver REGLA #1 de diferenciación):
  no reutilizar el verde de marca-demo ni el rojo de PRODUCTO DEMO por inercia en cada producto.
- Recomendar con criterio (di POR QUÉ ese color vende para ese producto), no solo nombrarlo.
