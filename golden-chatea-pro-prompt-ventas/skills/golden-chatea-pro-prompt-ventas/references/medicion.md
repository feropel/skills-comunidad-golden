# Medición: cómo saber si el prompt funcionó (y no creerlo)

> Sin esto, la skill produce prompts y nadie sabe si mejoran algo. Este archivo convierte la entrega en algo verificable: **qué anotar antes de tocar, qué mirar después, y cuándo se declara que un cambio sirvió.**

## ⛔ LA REGLA QUE ORDENA TODO
**Un cambio no "funcionó" porque el prompt se lea mejor. Funcionó si un número se movió.** Y para que un número se pueda mover, hay que haberlo anotado ANTES. Sin línea base no hay medición: hay opinión.

## PASO 1 — LÍNEA BASE (antes de tocar nada, 10 minutos)
Del producto que vas a cambiar, sobre los últimos 7 días completos:
```
Producto: ______            Del ___ al ___ (7 días)
1. Conversaciones nuevas ......................... ____
2. De esas, cuántas contestaron algo ............. ____
3. Cuántas llegaron a pedir precio ............... ____
4. Cuántas dieron los datos ...................... ____
5. Pedidos confirmados ........................... ____
6. Pedidos ENTREGADOS (no despachados) ........... ____
7. Rechazados o devueltos ........................ ____
```
De ahí salen las 4 tasas que importan, y **cada una señala un tramo distinto del prompt**:
- **Respuesta** (2÷1): falla el saludo, la multimedia o la pregunta de entrada.
- **Interés** (3÷2): falla la conexión o la recomendación.
- **Captura** (4÷3): falla el precio, la oferta o la razón de preferencia.
- **Cierre** (5÷4): falla la compuerta, el resumen o la confirmación.
- **Entrega** (6÷5): eso ya no es el prompt — es logística, dirección o expectativa mal puesta.
Anótalas. **Ese es el número contra el que vas a comparar.**

## PASO 2 — DÓNDE MUEREN LOS CHATS (el diagnóstico que más rinde)
Abre 20 conversaciones perdidas de esa semana y clasifica cada una por el ÚLTIMO mensaje del cliente:
| Murió en… | Lo que hay que arreglar |
|---|---|
| No contestó nunca | Multimedia inicial, saludo o pregunta de entrada (revisa saturación: ver regla anti-catálogo) |
| Contestó y se fue antes del precio | Conexión aspiracional: no llegó a querer el producto |
| Se fue al ver el precio | Falta valor apilado, ancla o razón de preferencia. NO es que el precio esté caro: es que llegó desnudo |
| Pidió precio y no volvió | Se dio el número pelado, sin pregunta de diagnóstico (regla de precio) |
| Se fue en la captura de datos | Se pidió demasiado, o se pidió algo que ya había dado |
| Dijo "lo pienso" y no volvió | Ahí trabajan los recordatorios: mide cuántos de estos rescatas |
20 chats bastan. El patrón aparece con 20; no necesitas 200.

## PASO 3 — LO QUE SE MIDE PIEZA POR PIEZA
- **Recordatorio 1 y 2:** de los que no respondieron, cuántos volvieron tras cada uno. Se miden POR SEPARADO — si el 1 rescata y el 2 no, el 2 se cambia solo.
- **Remarketing 1 y 2:** igual, y además cuántos se dieron de baja o bloquearon. Si molesta más de lo que rescata, se apaga.
- **Antes/después y testimonios:** de los que lo recibieron, cuántos avanzaron al precio.
- **Oferta:** cuál de las tres se llevan. Si nadie toma la 2 estando etiquetada, la etiqueta no está funcionando o el salto de precio es muy grande.
- **Talla (ropa):** % de devoluciones por talla, antes y después de recomendar en vez de solo mandar la tabla.

## PASO 4 — CÓMO DECIDIR SI SIRVIÓ (sin engañarse)
1. **Cambia UNA cosa a la vez.** Si cambias prompt, recordatorios y multimedia el mismo día y sube la venta, no sabes qué lo hizo — y el día que baje, tampoco sabrás qué devolver.
2. **7 días mínimo**, y compara contra los 7 anteriores del MISMO producto. No compares productos entre sí ni semanas con festivo contra semanas normales.
3. **Mira el volumen antes de celebrar:** pasar de 1 de 3 a 2 de 4 no es "subir del 33% al 50%", es ruido. Con menos de 30 conversaciones en la semana, la tasa no dice nada — espera a acumular.
4. **Si la pauta cambió, la comparación no vale.** Más presupuesto o un creativo nuevo mueven la calidad del tráfico, y eso mueve todas las tasas sin que el prompt tenga nada que ver.
5. **Criterio de decisión:** si la tasa del tramo que tocaste sube y las demás no bajan, se queda. Si sube esa y baja otra, se revisa: casi siempre significa que empujaste más y filtraste menos.

## PASO 5 — QUÉ HACER CON EL RESULTADO
- **Sirvió** → se replica al resto del catálogo, y se anota en `resultados-ledger.md` qué se cambió y cuánto movió.
- **No sirvió** → se revierte al prompt anterior (por eso siempre se guarda la versión previa) y se anota TAMBIÉN. Un cambio que no funcionó, documentado, vale tanto como uno que sí: evita repetirlo dentro de seis meses.
- **No se puede saber** → se declara así, sin adornar. Muestra pequeña, pauta cambiada o dos cambios a la vez: se repite el experimento limpio.

## Lo que esta skill NO puede medir sola
Ni la entrega ni el rechazo en destino dependen del prompt: eso vive en la operación logística. Si la tasa de entrega cae mientras las de conversación suben, el problema no está aquí — está en direcciones, transportadora o expectativa de tiempos. Dilo en el reporte en vez de atribuirte una caída que no es tuya.
