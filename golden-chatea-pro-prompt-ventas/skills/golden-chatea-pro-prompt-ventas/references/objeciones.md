# Librería de objeciones (respuestas cortas, listas para el prompt)

Inserta las que apliquen dentro del bloque OBJECIONES del prompt. Mantén ≤35 palabras, ≤2 emojis, tono humano. Adapta cifras/moneda al negocio. NUNCA prometas resultados médicos ni cures nada (ver `cumplimiento.md`).

## A) PRECIO / VALOR
- **"Está caro"** → "Te entiendo 🙏 Piénsalo así: sale menos de $X al día por [beneficio]. Además pagas al recibir, sin riesgo. Te muestro la promo de 2?"
- **"En otro lado es más barato"** → aquí se juega la RAZÓN DE PREFERENCIA (ver PASO 0.7 de `plantilla-prompt.md`): en positivo, sin hablar mal de nadie. "Puede ser 🙂 la diferencia es que aquí es original, pagas al recibir y revisas antes de pagar, y si algo llega mal te lo cambiamos. Eso es lo que estás pagando de más: que alguien responda." Nunca digas que el otro vende réplicas ni lo nombres.
- **"No tengo el dinero ahora"** → "Tranqui, no pagas nada hoy 🙌 Es contra entrega: el dinero lo tienes listo para cuando llegue. Te lo dejo agendado?"
- **"Hay descuento?"** → "La mejor oferta es llevando 2 o 3: sale más económico por unidad y con envío gratis 🔥 Cuál te sirve?"

## B) CONFIANZA / MARCA
- **"Será que sí funciona?"** → "Sí 💛 +[N] personas ya lo usan y repiten. Por eso lo puedes pagar al recibir: si no te da confianza al verlo, no lo recibes."
- **"Es original?"** → "100% original ✅ Nada de réplicas. Por eso ofrecemos pago contra entrega y garantía."
- **"Me da desconfianza comprar por WhatsApp"** → "Te entiendo 🙏 Por eso trabajamos contra entrega: primero lo tienes en tus manos y luego pagas. El riesgo lo asumimos nosotros."
- **"Puedo ver reseñas?"** → "Claro 😊 mira lo que dicen quienes ya lo tienen: [AQUÍ VA URL DE TESTIMONIOS]"

## C) LOGÍSTICA / ENTREGA
- **"Cuánto se demora?"** → "Ciudad principal 2-3 días, intermedia 3-5, zonas rurales 5-7 📦 A qué ciudad sería?"
- **"Puedo recoger en oficina?"** (SOLO países con oficina en su pack, ej. Colombia — en MÉXICO NO existe: responde que la entrega es a domicilio) → "Sí! Llega a la oficina de [TRANSPORTADORA] de tu ciudad. Solo necesito tu ciudad y departamento 😊"
- **"Puedo revisar antes de pagar?"** → DEPENDE DE LA POLÍTICA DEL NEGOCIO (pregúntala en el intake, ítem 10; nunca la asumas). Si permite: "Sí, puedes revisar el empaque al recibir ✅". Si NO permite: "Por políticas de la transportadora no está permitido abrirlo antes de pagar, pero tienes garantía: si algo llega mal, respondemos 🙏".
- **"El envío es discreto?"** → "Totalmente discreto 🤫 Nadie sabe qué contiene el paquete. Tu privacidad primero."

## D) SALUD / LEGAL (sin prometer nada indebido — ver cumplimiento.md)
- **"Tiene efectos secundarios?"** → "Es de uso [tópico/externo] y no es medicamento. Aun así, si tienes una condición particular, consulta con tu médico 🙏"
- **"Sirve para [condición médica]?"** → "Es un producto de [categoría], no un tratamiento médico. Te ayuda con [beneficio permitido]. Para temas de salud, tu médico es quien orienta."
- **"Tiene registro sanitario?"** → "[Responder con la verdad del negocio]. Es un producto de [categoría] de uso [externo/cosmético]."

## E) DECISIÓN / TIEMPO
- **"Lo voy a pensar"** → (1 intento, jamás dos) "Claro, tómate tu tiempo 😊 recuerda que pagas al recibir, así decides con el producto en la mano. Aquí estoy cuando quieras." ⛔ NO inventes que la promo vence hoy: si la oferta no tiene fecha real, no le pongas una (LEY DE LA URGENCIA REAL).
- **"Después te escribo"** → "Con gusto 💛 aquí estoy cuando quieras. Si te decides, te lo dejo listo en un momentico." (No prometas apartar nada que no se aparte de verdad.)
- **"Déjame preguntarle a mi esposo/a"** → "Perfecto 🙂 mientras tanto te aparto la oferta. Recuerda que pagas al recibir, así que el riesgo es cero."

## Regla al usarlas
Elige SOLO las objeciones que apliquen a este producto/país. No metas las 20 al prompt: infla caracteres. Prioriza precio, confianza y la médica/legal si el producto es sensible.

## Antes y después (cuando duda si funciona)
Es el recurso que más convierte ante "sirve de verdad?", pero solo con material REAL del negocio: fotos de clientes reales con permiso, sin retoque que exagere, con el disclaimer "los resultados varían según cada persona" y sin claims de cura. Envía la imagen y pregunta "te identificas con el antes?". Si el negocio no tiene, se omite y se refuerza con riesgo cero (pagas al recibir, revisas antes de pagar) — jamás se simula ni se toma de otra marca.

## ⛔ LEY DE LA URGENCIA REAL (hermana de la ley de prueba social real)
La urgencia es CIERTA o NO EXISTE. Prohibido decir "la promo es de hoy", "últimas unidades", "te lo aparto" o "el precio sube mañana" cuando no es verdad — es la misma mentira que un testimonio inventado, con la misma consecuencia: en COD el cliente que vuelve al día siguiente y encuentra la misma promo entiende que le mintieron, y ese pedido se rechaza con el flete perdido. Además contradice `cumplimiento.md` §4, que exige que la escasez sea cierta o rotativa honesta.
Urgencia que SÍ se puede usar porque es real: stock verdaderamente limitado (si el vendedor lo confirmó), una promoción con fecha real de fin, tiempos de despacho ("si lo confirmas hoy sale mañana"), o la rotativa honesta (la oferta cambia de verdad cada semana). Si no hay ninguna, se cierra con lo que sobra: pagas al recibir, revisas antes de pagar, sin riesgo.
