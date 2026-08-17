# Intake inteligente (recolección + investigación antes de construir)

Meta: hacerle la vida fácil al vendedor y ser RÁPIDO. La skill pregunta **TODO lo NECESARIO para que el prompt quede perfecto** (no lo mínimo), pero lo hace en un **FORMULARIO de una vez**: un solo mensaje con todas las preguntas agrupadas y numeradas, país primero, marcando obligatorio vs opcional. El cliente responde de corrido lo que tenga (puede pegar varios datos juntos, como en la vida real). Nada de ida-y-vuelta pregunta por pregunta: eso cansa. Acepta la info en el formato que el cliente tenga (URL, imagen o nada) e investiga por su cuenta lo que falte. Lo único que NO se pregunta es lo condicional que no aplica o lo que ya se obtuvo de la URL/foto/investigación (en ese caso se confirma en el borrador, no se vuelve a preguntar).

## Modo por defecto: FORMULARIO de una vez
Manda las preguntas JUNTAS, así:
```
Para armarte el mejor asistente te pido estos datos (respóndeme de corrido lo que tengas; lo que no sepas, yo lo propongo):

PAÍS (obligatorio): ...
PRODUCTO (obligatorio): nombre y qué hace. Tienes URL o foto?
PRECIO (obligatorio al menos 1): de 1, 2 y 3 (unidades o combos; di cuántas trae cada combo)
Variantes (si aplica): sabores/colores/modelos + se venden por unidad o por combo mezclable?
Pago: contra entrega, anticipado o ambos? (si anticipado: titular, banco/entidad, número y tipo de cuenta)
Asesor: nombre del bot (personalidad la pongo yo según el producto)
Para cerrar mejor (opcional): cuántos clientes/reseñas tienes, garantía, regalo o bono, envío discreto, producto original
URL de tu tienda (opcional, solo si tienes tienda web): para redirigir si preguntan por otro producto
```
⛔ ENTREGA — NO SE PREGUNTA (regla de FER): los tiempos de entrega y la transportadora van PREDETERMINADOS por país (ver `paises.md`). La skill los aplica sola y los muestra en el borrador como supuesto ("dejé los tiempos estándar; si tu operación es distinta, dime"); solo cambian si el vendedor los corrige por iniciativa propia.
- **Relleno inteligente:** con lo que responda, DEDUCE lo posible (moneda/indicativo del país, tono por producto, beneficios de la URL/foto) y PROPÓN defaults para lo que falte, marcándolos como supuestos. Solo REPREGUNTA si falta un OBLIGATORIO (precio de 1, país, producto). El resto no bloquea.
- **Alternativa por bloques** (solo si el cliente lo prefiere o parece abrumado): 3 tandas — 1) producto · 2) precio y oferta · 3) operación y negocio. El "uno por uno" es último recurso, no default.

## Lo que SIEMPRE se pregunta (lo necesario para un prompt perfecto)
1. **Nombre del asesor/a** (cómo se llamará el bot) y personalidad (cálida, directa…).
2. **País** donde vende (para el pack de `paises.md`: dirección, transportadoras, pago, tono).
3. **Producto**: tienes URL, foto, o ninguna? (ver "Fuentes de producto").
3b. **URL de la tienda / catálogo** (si tiene): sirve para dos cosas — (a) que la skill lea el catálogo si hace falta, y (b) que el bot pueda redirigir al cliente a la tienda cuando pregunte por OTRO producto. Pregúntala. Si no tiene tienda web, el bot mantiene foco en el único producto.
4. **Modelo de pago** (gate): "Vas a solicitar **pago anticipado**?"
   - Si **SÍ** → pídele los datos completos: **titular + banco/entidad (Nequi/Daviplata/Bancolombia/etc.) + número/llave + TIPO de cuenta** (ahorros/corriente/billetera).
   - Si **NO** → NO pidas nada de anticipado; el prompt queda solo contra entrega.
5. ~~Tiempos de entrega y transportadora~~ → **NO SE PREGUNTAN** (regla de FER): default por país en `paises.md`, mostrados como supuesto en el borrador; se ajustan solo si el vendedor los corrige solo.

## Preguntas CONDICIONALES (solo si aplican — no preguntes de más)
- **Variantes/colores/sabores** → solo si el producto los tiene. Si no, ni se menciona (no hay "color"). Si las tiene, pregunta ADEMÁS si se vende por unidad o por **combo de cantidad fija con variantes mezclables** (ej. docena de 12 a elegir sabores) — cambia la captura, el upsell y el resumen (ver `plantilla-prompt.md`).
- **Datos de anticipado** → solo si respondió que sí al gate.
- **URLs de imágenes conversacionales** → por cada imagen que el prompt use (ver `recursos-visuales.md`); si no las tiene, la skill genera o entrega el prompt de imagen.
- **Combos 2/3 y mayorista** → pregúntalos; si solo hay 1 unidad, construye igual (precio de 1 es el único obligatorio).
- **Garantía, regalo/bono, envío discreto, original** → pregúntalos una vez; si no aplica, se omiten.

## Fuentes de producto (acepta lo que el cliente tenga)
La skill se adapta a cómo llegue la info:

**A) El cliente manda URL(s)** (su tienda o de competidores):
- Scrapea cada URL (Firecrawl) y extrae: nombre, precio, combos, beneficios, modo de uso, reseñas/rating, garantía, claims.
- ⚠️ COMBOS — NUNCA los deduzcas ni los calcules: la oferta por cantidad (1/2/3 unidades) vive en el widget de compra (Releasit COD Form o app de quantity break), y su matemática de descuento (fijo/porcentaje/sobre bruto/con código) se interpreta mal casi siempre. Puedes MENCIONAR que detectaste una oferta de 2/3 unidades, pero **PÍDELE al vendedor que lea los 3 precios EXACTOS directo de su widget de compra** ("abre tu página, dale comprar y dime el precio de 1, de 2 y de 3"). Solo el precio de 1 unidad (og:price / precio visible) se puede tomar directo. Presentar un combo deducido como si fuera real = error grave (datos reales antes de generar).
- Si son de competidores, úsalas para ángulos de venta y objeciones reales (NO copies su estructura; ver regla de blindaje).

**B) El cliente manda una FOTO del producto:**
- Analiza la imagen (visión): identifica qué es, tipo de producto, presentación.
- Con eso, busca el producto en la web y en anuncios de la competencia para completar ficha, beneficios y precios de referencia.

**C) El cliente NO manda nada** (solo el nombre o una idea):
- Investiga: busca el producto y competidores (Firecrawl search), revisa anuncios activos (Meta Ad Library si está disponible), reseñas y tendencias.
- Arma un borrador de ficha (beneficios, ángulos, objeciones típicas, rango de precio de mercado).

## De la investigación salen objeciones y hooks REALES (no inventados)
Cuando scrapees competidores o reseñas, extrae:
- **Objeciones reales** que aparecen en reseñas negativas y preguntas → aliméntalas al bloque OBJECIONES (además de las de `objeciones.md`).
- **Hooks/ángulos que ya venden** en los anuncios activos de la competencia (Meta Ad Library) → úsalos para el saludo, la pregunta de entrada y el espejo del dolor. NO copies su estructura de prompt (blindaje); toma solo el ángulo/insight.
- **Rango de precio del mercado** → para sugerir combos y detectar si el precio del cliente está fuera de mercado (avísale).

## Adaptación por NICHO (la skill funciona en todos)
Ajusta tono, claims y objeciones al nicho, sin cambiar la estructura:
- **Salud/belleza/cosmético:** claims de APARIENCIA, nunca de cura; disclaimer "no es medicamento"; remite a médico (ver `cumplimiento.md`).
- **Íntimos/sensibles:** enfatiza envío discreto y privacidad; pregunta de entrada NO invasiva.
- **Suplementos/ingesta:** cuidado extra con claims; edad mínima; "no reemplaza una dieta/medicamento".
- **Ropa/accesorios/hogar/mascotas:** aquí sí suele haber **variantes** (talla, color, modelo) → incluye el campo de variante y combos por variante.
- **Electrónica/valor alto:** refuerza garantía, originalidad y soporte; el anticipado es más común.
Pregunta el nicho si no es obvio, y elige el pack de país (`paises.md`) + las objeciones que apliquen.

## Regla de datos reales (crítica)
Lo investigado sirve para ACELERAR, no para inventar. El **precio real, el WhatsApp, el nombre del negocio y los claims** SIEMPRE se confirman con el cliente antes de construir. Nunca pongas un precio "de mercado" como si fuera el suyo: propónlo como supuesto y pide confirmación.

## Cómo procede la skill
1. Manda el **formulario de una vez** (todas las preguntas juntas, país 1º, obligatorio vs opcional) + el gate de anticipado incluido.
2. Toma la fuente de producto que el cliente dé (URL / foto / nada) e investiga lo que falte; deduce moneda/tono/beneficios.
3. Arma un **borrador de ficha** y lo confirma con el cliente (precio, combos, claims): "esto entendí/encontré, lo confirmas o lo ajusto?". Solo repregunta lo OBLIGATORIO que falte.
4. Solo entonces construye el paquete (PASO 2 en adelante).

## Capacidades disponibles (úsalas)
- **Scrapear URL** → Firecrawl (ficha, precio, reseñas de la propia página o de competidores).
- **Buscar en la web / competencia** → Firecrawl search, Meta Ad Library (anuncios activos), tendencias.
- **Analizar imagen del producto** → visión (identificar producto desde una foto).
- **Generar imágenes** → Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch (para la multimedia y las imágenes conversacionales; ver `recursos-visuales.md`).
Si una capacidad no está disponible en el momento, dilo y ofrece el camino manual (que el cliente pegue la URL/foto o los datos).
