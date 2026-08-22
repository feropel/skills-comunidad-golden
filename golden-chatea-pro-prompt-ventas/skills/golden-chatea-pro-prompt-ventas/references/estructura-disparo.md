# Estructura de Disparo: saludo, multimedia, pregunta, recordatorios, remarketing

Orden de montaje en Chatea PRO:
```
palabra clave → SALUDO → MULTIMEDIA → PREGUNTA DE ENTRADA → PROMPT
```

## 1. Saludo inicial (tope nativo del campo: 1.000 caracteres)
Cálido, con el nombre del asistente, crea expectativa para que el cliente espere la multimedia.

⛔ REGLA DURA — EL SALUDO NO LLEVA PREGUNTA. Chatea dispara en secuencia automática: SALUDO → MULTIMEDIA → PREGUNTA DE ENTRADA. Si pones una pregunta en el saludo, el cliente respondería antes de ver la multimedia y luego lo vuelves a preguntar en la pregunta de entrada = redundante y confuso. El saludo SOLO saluda y crea expectativa; termina invitando a esperar la multimedia (nunca con "...?"). **La ÚNICA pregunta que espera respuesta es la Pregunta de entrada (paso 3).**
```
Hola! 👋 Bienvenid@ a [MARCA]

Soy [NOMBRE], tu asesora personal 😊

Dame un momentico mientras te comparto algo que te va a encantar 👇
```

## 2. Multimedia (3 piezas recomendadas, en orden)
1. Imagen de producto + propuesta de valor (con envío gratis / contraentrega visible)
2. Video corto (15-30s) mostrando producto y uso — el que más convierte
3. Imagen de prueba social (reseñas / testimonios / "+N clientes")

Si solo se puede una pieza, usar el video. No hace falta texto entre foto y foto si las imágenes ya traen texto.

⛔ El texto que acompaña la multimedia TAMPOCO lleva una pregunta que espere respuesta (no compitas con la pregunta de entrada). Puede ser una frase de expectativa ("mira esto 👇"), pero la única pregunta va en el paso 3.

## 3. Pregunta de entrada (tope nativo del campo: 1.000 caracteres)
Debe segmentar al cliente en los caminos que el prompt sabe responder. Ejemplo (producto con varios usos):
```
Cuéntame una cosa para asesorarte mejor 😊

Buscas [PRODUCTO] para [uso A], para [uso B], o para ambos?
```
Clave: que NO sea invasiva (sobre todo en productos sensibles) y que conecte con los pasos del prompt.

## 4. Recordatorios (dentro de la ventana de 24h, suaves, sin presionar cantidad)
TIEMPOS FIJOS: **Recordatorio 1 a la 1 hora, Recordatorio 2 a las 2 horas.**
Los recordatorios NO llevan plantilla ni instrucción de IA: son solo el mensaje de texto (se envían dentro de la ventana de 24h, no necesitan plantilla de Meta).
```
RECORDATORIO 1:
Te quedó alguna duda? Con gusto te ayudo 😊

RECORDATORIO 2:
Sigo por aquí si quieres que te lo deje listo ✨ Envío gratis y pagas al recibir 🙌
```

## 5. Remarketing (reabre la conversación tras varias horas)
Cada "Configuración Remarketing" en Chatea tiene un interruptor (activar) y TRES campos. La skill entrega los tres, listos:

**Campo 1 — Tiempo Remarketing:** número + unidad. FIJO: **Remarketing 1 = 3 Horas · Remarketing 2 = 6 Horas.**

**Campo 2 — Plantilla Mensaje:** es un desplegable donde se elige una **plantilla de Meta ya APROBADA**, o "No enviar plantilla". La plantilla se crea aparte en el Administrador de WhatsApp/Meta. La skill DISEÑA esa plantilla completa para que el vendedor la registre en Meta y luego la seleccione aquí. Anatomía de la plantilla de Meta:
- **Nombre:** minúsculas, SIN espacios, con guion bajo `_`. Ej.: `remarketing_1_[producto]`.
- **Categoría:** Marketing.  **Idioma:** Español.
- **Encabezado:** IMAGEN (ideal, del producto; la skill la genera o la pide, ver `recursos-visuales.md`).
- **Cuerpo:** texto con **variable `{{1}}` = nombre del cliente** (ej. "Hola {{1}} 😊 ..."). Meta pide un ejemplo de {{1}} (ej. "María").
- **Pie de página:** una línea corta y sobria; la skill la sugiere (ej. "[MARCA] · Pago contra entrega").
- **Botón(es):** 1 a 3 (CTA, ej. "Quiero pedirlo"). ⚠️ En el MAPEO del botón dentro de Chatea, ese botón se configura como **"botón de remarketing"** (así el clic enlaza al flujo). Indícaselo SIEMPRE al vendedor.
Si el vendedor no quiere plantilla (o aún no la aprueban), va "No enviar plantilla" y el remarketing funciona solo con el Campo 3.

**Campo 3 — Instrucción especial del remarketing:** UN solo campo de texto, **máximo 1000 caracteres**, que contiene el MENSAJE con que el bot reabre + la instrucción para la IA entre corchetes (van juntos en el mismo campo). Ejemplo:
```
Hola 😊 soy [NOMBRE] de [MARCA]

Muchas personas ya disfrutan [PRODUCTO] ✨

Te dejo tu pedido listo? Envío gratis y pagas al recibir 🙌

[Instrucción IA: retoma con calidez sin reiniciar ni repetir lo ya dicho. Refuerza con la prueba social. Si dudó por precio, ancla el valor. Lleva a cerrar. Máximo 1 intento, sin presionar.]
```
Cada toque trae un ÁNGULO NUEVO (RM1 prueba social/beneficio; RM2 valor/último toque), sin repetir los recordatorios. Redacta suave para que la plantilla de Meta pase aprobación.

RESUMEN de qué entrega la skill por cada remarketing:
1. Tiempo (3h / 6h).
2. Texto del Campo 3 (mensaje + [Instrucción IA], ≤1000 caracteres) — copy-paste directo.
3. La plantilla de Meta completa (nombre, categoría, idioma, imagen, cuerpo {{1}}, pie, botón) para crear en Meta y seleccionar en el Campo 2; recordar que el botón se mapea como "botón de remarketing".

## 6. Activador de flujo — NORMA DE DOS ACTIVADORES (aprobada por el Centro de Mando 2026-08-07)
Se registran **DOS activadores por producto**. El activador único (solo la frase) no alcanza:
funciona donde el enlace **precarga** el mensaje (botón de la página, CTA de WhatsApp en Meta),
pero en **TikTok, los estados de WhatsApp y los comentarios NO hay nada que precargue** — ahí el
cliente escribe a mano y el bot no dispara. (Misma familia del bug Libido UP: el orgánico decía
"escribe RITUAL" y el activador registrado era otro. Solución probada en el estudio dental de
Chile: frase completa + palabra corta "SONRISA".)

**Activador 1 — la FRASE COMPLETA del anuncio/botón**, palabra por palabra, incluyendo el nombre
del producto. Es la que dispara desde los canales con mensaje precargado:
```
Hola quiero información y precio de [PRODUCTO]
```

**Activador 2 — UNA palabra corta ÚNICA y propia del producto** (ej. estilo "SONRISA", "HONGOS").
Es la que se usa en **todo CTA escrito** ("comenta X", "escribe X") en TikTok, estados y
comentarios. Reglas duras:
- **ÚNICA en el bot**: verificarla contra TODAS las palabras clave de los demás productos para
  que no se cruce con ninguna.
- **JAMÁS genéricas** ("información", "precio", "promo"): el vendedor maneja varios productos y
  esas palabras solas disparan el bot equivocado.
- El CTA escrito de cada pieza orgánica debe usar EXACTAMENTE esa palabra (coherencia verificable
  por grep en todas las piezas).

Entrega las DOS líneas, como texto crudo para copiar y pegar, sin prefijos ni comillas. NO
agregues más palabras sueltas aparte de la palabra corta única del producto.

⛔ SIN EMOJIS EN LA PALABRA CLAVE (regla de FER, 2026-07-25): la frase del activador y del botón va
SIN emoji al final. Dos razones de campo: (1) quien escribe la frase A MANO (vio el anuncio y abrió
WhatsApp directo) jamás teclea el emoji → el bot no dispara y la venta se pierde en silencio;
(2) algunos teléfonos/clientes alteran el emoji al pasar por el link wa.me y el match exacto se rompe.
Si la página ya tiene un botón con emoji, se corrige el botón — no se le pone emoji a la keyword.


VALIDACIÓN DURA DEL ACTIVADOR (antes de entregar): LA validación es `bash scripts/validar.sh --activador <archivo>` — usa una LISTA PERMITIDA (solo letras, números y puntuación básica) que bloquea CUALQUIER emoji o símbolo raro, de 3 o de 4 bytes. Contexto: los 4 bytes están PROBADOS corrompiendo el trigger (incidente real 2026-07-26 con un 👋); los de 3 bytes (✨ ✅ ‼ ⁉ ℹ) no están probados contra la base, así que el default seguro es cero. La fórmula `[c for c in t if ord(c) >= 0x10000]` solo caza los 4 bytes y NO basta como validación manual.
Corre `bash scripts/validar.sh --activador <archivo-con-el-activador>`: el veredicto exige 0 emojis de CUALQUIER tipo (4 bytes Y 3 bytes como ✨ ⛔ ✅) y sin BOM; si falla, bloquea con exit distinto de 0.

## 7. URLs dentro del prompt (recursos visuales conversacionales)
Las URLs que el AGENTE envía durante la conversación (no la multimedia inicial) van ESCRITAS dentro del prompt, con instrucción de cuándo enviarlas. Patrón:
```
Si pide ver [X], envía: https://...
```
Ubícalas en el paso donde tienen sentido (modo de uso en PASO 1 o soporte; tabla de precios en PASO 2; testimonios en PASO 3, etc.). No las modifiques ni acortes.
