# El prompt maestro de ecom

Un solo prompt, idéntico para todos los motores de la arena. Si cambias el prompt entre
motores ya no estás midiendo motores, estás midiendo prompts.

⚠️ **Si el producto tiene texto en la etiqueta, NO uses la plantilla de abajo tal cual:**
aplica primero el método definitivo del paso 1.5 del SKILL.md (placa de fondo sin producto
+ `componer.py` con el PNG real). Ningún motor copia bien el microtexto de un empaque.
En ese caso el bloque [2 PRODUCTO] se reemplaza por: *"background plate only, do NOT
include any bottle or product; leave a clean empty pedestal area in the lower centre for
the product to be composited later; no rectangle, no panel, no block of flat colour"*.

## Estructura (5 bloques)

```
[1 ESCENA]      qué se ve, dónde está el producto, luz y fondo
[2 PRODUCTO]    la referencia manda: "usa el producto de la imagen de referencia
                EXACTAMENTE como es — mismo envase, mismo logo, misma etiqueta,
                mismos colores. No lo redibujes ni inventes texto sobre el empaque"
[3 TEXTO]       el copy literal que debe aparecer, entre comillas, con jerarquía
[4 ESTILO]      paleta, tipografía, referencias de layout, mobile-first
[5 PROHIBIDO]   la lista negra
```

## Plantilla lista para llenar

> Anuncio de ecommerce profesional para **{PRODUCTO}**, formato **{1080×1080 | 1080×1350}**,
> vertical **{nicho}**, mercado **{país}**.
>
> **Producto:** usa el producto de la imagen de referencia exactamente como es — mismo
> envase, mismo logo, misma etiqueta, mismos colores y proporciones. No lo redibujes, no
> inventes texto sobre el empaque, no cambies la forma. El producto es el héroe y debe
> verse nítido y completo.
>
> **Escena:** {fondo limpio / entorno de uso / superficie con textura}, luz suave de
> estudio, sombra natural, sin desorden visual.
>
> **Texto que debe aparecer, exactamente así:**
> - Titular grande: "{HOOK — el dolor o la promesa, máximo 6 palabras}"
> - Subtítulo: "{la solución en una línea}"
> - {3-4} beneficios cortos con ícono simple: "{beneficio 1}", "{beneficio 2}",
>   "{beneficio 3}"
> - {Sello/badge si aplica: "{garantía o prueba}"}
>
> **Estilo:** paleta {colores}, tipografía sans serif gruesa y muy legible, jerarquía
> clara, composición mobile-first — el titular debe leerse en una pantalla de 390 px de
> ancho. Estética de marca premium, no de plantilla genérica.
>
> **Prohibido:** botones, cajas que parezcan clickeables, "Compra aquí", "Pide ya",
> flechas de interfaz, logos de WhatsApp, números de teléfono, marcas de agua, texto
> recortado por el borde, texto inventado que yo no haya escrito arriba.

## Reglas del texto que va DENTRO de la imagen

- **Lo escribes tú**, en el español del país de destino (Colombia por defecto), no lo deja
  a criterio del modelo. Modelo que inventa texto = pieza descalificada.
- **Máximo ~7 palabras** en el titular. El 74% del tráfico LatAm compra en móvil.
- Ángulo de respuesta directa: **dolor → solución → prueba**. Si necesitas munición de
  ángulos, tira de `golden-copywriting`.
- **Cero claims inventados.** Nada de "cura garantizada", "resultados en 24 horas" o
  porcentajes que nadie midió. Compliance manda, sobre todo en salud y belleza.
- **Sin precio dentro de la imagen** salvo que el usuario lo pida explícitamente: el precio
  cambia y deja la imagen obsoleta; en la ficha lo pone `golden-shopify` como bloque nativo.
- **Sin botón ni CTA clickeable** (ley 3 de la skill). No se negocia.

## Reglas de arte para SALUD (dental y afines) — norma del Centro de Mando 2026-08-07

Probadas en campo en el un estudio de producto. Aplican a todo prompt de imagen cuando el
vertical es salud bucal o parecido (suplementos, piel, capilar con claim sensible):

**PROHIBIDO en la imagen:**
- Bocas con lesiones visibles (caries, manchas, encías inflamadas).
- Antes/después de dentadura.
- Delantal blanco, estetoscopio, sillón dental — cualquier cosa que parezca aval médico.
- Porcentajes de resultados en pantalla ("95% efectivo").
- Preguntas que señalen una condición del espectador ("tienes caries?").

**PERMITIDO y probado (lo que sí convierte):**
- Macro del gotario / del aplicador.
- Textura del producto.
- Corte de esmalte ILUSTRADO (diagrama estilizado, no fotografía clínica).
- Lifestyle de baño (rutina diaria, ambiente limpio).

Estas reglas van al bloque [5 PROHIBIDO] del prompt maestro cuando aplique el vertical.

## Antes/después: el corte por vertical (Meta 2026 — riesgo de cuenta)

El bloque de arriba prohíbe el antes/después **solo en dental**. Meta lo prohíbe en más
verticales, así que el corte real es este (verificado 2026-08-10):

- **PROHIBIDO generar antes/después** en antiedad / arrugas / reafirmante / lifting, en
  pérdida de peso, y en salud bucal o cualquier claim de salud sensible. Aplica aunque el
  encargo lo pida: se cambia la pieza, no se entrega el split.
- **Permitido** en cosmética general (uña, cabello, mancha localizada) con público 18+,
  la MISMA zona, sin rostros y sin inducir rechazo del propio cuerpo.

Transversal a todo vertical, va siempre al bloque [5 PROHIBIDO]: nada de segunda persona
que señale la condición del espectador ("tus arrugas", "tu papada") y nada de titular de
plazo con resultado ("resultados en 7 días"). Desde 2026 Meta juzga el significado
IMPLÍCITO: un plazo junto a un split de antes/después se lee como claim de transformación
engañoso aunque no aparezca la palabra "garantizado".

**Reemplazo que sí convierte:** macro de textura, modo de uso, mecanismo ilustrado,
ingredientes, lifestyle.

## Notas por motor

- **Nano Banana Pro / Hazel / GPT Image 2** obedecen bien el texto entre comillas. Ponlo
  literal y con la jerarquía marcada.
- **Seedream** responde mejor a instrucciones de edición ("mantén el envase, cambia solo
  el fondo") que a descripciones largas de escena.
- **FLUX.2** es literal: lo que no escribas, no aparece. Bueno para piezas minimalistas.
- **Recraft** acepta `colors` en hex (hasta 10) y `background_color`: úsalo para íconos y
  sellos que deban calzar con la paleta de la marca al pixel.
