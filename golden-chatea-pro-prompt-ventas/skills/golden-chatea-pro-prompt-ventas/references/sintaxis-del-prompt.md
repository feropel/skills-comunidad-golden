# Sintaxis del prompt: los 5 comandos que hacen que la IA obedezca

> De la clase del MBA 2026-09-01. Es la mecánica de CÓMO se escribe el prompt. La skill ya la usaba de forma implícita; aquí queda explícita para que cualquiera pueda ajustar su propio prompt sin romperlo.

## 1. `#` y `##` — SECCIONES Y JERARQUÍA (Markdown)
La IA lee mucho mejor un texto jerarquizado que un bloque plano. Tres niveles bastan:
```
# ROL
Eres [NOMBRE], asesora de [MARCA] con [N] años de experiencia.

# OBJETIVO
Convertir conversaciones en pedidos.

# REGLAS
## REGLA 1
Nunca inventes información.
## REGLA 2
Haz máximo una pregunta por mensaje.
```
Estructura habitual: `# SECCIÓN PRINCIPAL` (rol, objetivo, reglas, producto, flujo, objeciones) · `## Subsección` (ficha técnica, interacción 1, interacción 2, preguntas frecuentes) · `### Sub-subsección` (la respuesta a cada objeción).

## 2. `" "` COMILLAS — TEXTO LITERAL ⭐ (el comando más importante)
**Lo que va entre comillas, la IA lo dice EXACTAMENTE así. Lo que va sin comillas, lo dice a su manera** — la misma idea en quince versiones distintas.
Ese es el interruptor entre un bot robótico y uno humano, y hay que usarlo con criterio:
- **CON comillas** (literal, no se toca): precios y tabla de opciones · datos de pago anticipado · el mensaje de captura de datos · el resumen del pedido · frases legales o de cumplimiento · el disclaimer de resultados.
- **SIN comillas** (que varíe): saludos, transiciones, empatía, espejo del dolor, refuerzos. Si el bot da SIEMPRE la misma frase de bienvenida o la misma reacción, suena a máquina — y quien escribe dos veces lo nota.
Regla: **literal donde un error cuesta plata o cumplimiento; libre donde la repetición delata al bot.**

## 3. `( )` PARÉNTESIS — ACLARACIONES SECUNDARIAS
Para condicionar o matizar una instrucción sin partirla en dos reglas:
```
Pregunta el nombre del cliente (solo si todavía no lo conocemos).
Ofrece pago contra entrega (cuando esté disponible para esa ciudad).
Envía la imagen de antes y después (solo si el negocio tiene fotos reales).
```

## 4. `[ ]` CORCHETES — VARIABLES
Marcan lo que la IA debe REEMPLAZAR por el dato real, y hacen el prompt reutilizable entre productos:
```
Hola [NOMBRE], tenemos disponible [PRODUCTO].
Precio: [PRECIO] · Beneficio principal: [BENEFICIO]
```
⚠️ **CÓMO SE RELACIONA CON LA REGLA DE PLANTILLA (no son contradictorias, son las dos caras):** el corchete existe para que la IA lo RELLENE con el valor real; el fallo que la skill persigue es que el corchete SALGA LITERAL en el mensaje al cliente ("Hola [NOMBRE]" enviado tal cual). Por eso todo prompt lleva además la instrucción explícita: *los [corchetes] son instrucciones para TI, jamás aparecen en el mensaje; si falta el dato, no lo inventes ni dejes el corchete: pídelo.*

## 5. `IMPORTANTE` / `NUNCA` / `SIEMPRE` EN MAYÚSCULAS — REGLAS CRÍTICAS
Las mayúsculas le dan peso a la regla. Se reservan para lo que no se puede fallar:
```
IMPORTANTE: nunca inventes precios.
NUNCA: ofrezcas un producto que no aparezca en la información proporcionada.
SIEMPRE: revisa la conversación antes de responder.
```
⚠️ Úsalas con moderación. Si TODO está en mayúsculas, nada destaca: el énfasis funciona por contraste. Reserva estas tres palabras para las reglas que protegen plata, cumplimiento o la experiencia del cliente.

## Cómo usar esto para CORREGIR un prompt en caliente
Son las cinco herramientas para ajustar sin reescribir: si el bot dice algo mal → ponlo entre comillas · si se salta una condición → métela en paréntesis · si mezcla temas → sepáralos con `##` · si repite un dato fijo → conviértelo en variable · si ignora una regla → súbela a IMPORTANTE/NUNCA/SIEMPRE.
