# Estructura de Disparo: saludo, multimedia, pregunta, recordatorios, remarketing

Orden de montaje en Chatea PRO:
```
palabra clave → SALUDO → MULTIMEDIA → PREGUNTA DE ENTRADA → PROMPT
```

## 0. EL PERFIL VENDE ANTES DE QUE ESCRIBAS (prerequisito del paquete)
El cliente ve el perfil ANTES de leer una sola palabra tuya: es el primer activo de confianza y no cuesta nada. **La fábrica no lo configura —vive en el negocio, no en el prompt— pero SÍ lo verifica antes de entregar**, porque un paquete perfecto sobre un perfil vacío rinde menos.
- **Foto:** una imagen del negocio **donde aparezcas TÚ** (junto al logo, la marca o el producto). Humaniza y genera confianza. Con sonrisa y un color de fondo distintivo que te haga reconocible en la lista de chats.
- **Descripción (máx. 160 caracteres):** detallada pero corta — qué consultas o pedidos se resuelven por esa línea, con llamado a la acción. Más largo aburre y no se lee.
- **Datos de contacto y enlaces:** correo, web y redes principales. Suman confiabilidad verificable.
⚠️ **Coherencia con el paquete:** si el recordatorio disruptivo envía una foto de la asesora, esa cara DEBE ser la misma del perfil (ver regla en Recordatorios). Un perfil con logo y un mensaje con selfie de otra persona rompen la credibilidad que el propio perfil construyó.
📌 Al entregar el paquete, revisa el perfil y dilo si está flojo. Es la corrección más barata que existe: cinco minutos, cero costo, y actúa sobre TODAS las conversaciones, no sobre una.

## 1. Saludo inicial (tope nativo del campo: 1.000 caracteres)
Cálido, con el nombre del asistente, crea expectativa para que el cliente espere la multimedia.

⛔ REGLA DURA — EL SALUDO NO LLEVA PREGUNTA. Chatea dispara en secuencia automática: SALUDO → MULTIMEDIA → PREGUNTA DE ENTRADA. Si pones una pregunta en el saludo, el cliente respondería antes de ver la multimedia y luego lo vuelves a preguntar en la pregunta de entrada = redundante y confuso. El saludo SOLO saluda y crea expectativa; termina invitando a esperar la multimedia (nunca con "...?"). **La ÚNICA pregunta que espera respuesta es la Pregunta de entrada (paso 3).**
```
Hola! 👋 Bienvenid@ a [MARCA]

Soy [NOMBRE], tu asesora personal 😊

Dame un momentico mientras te comparto algo que te va a encantar 👇
```

### 🔴 EL SALUDO NO LE ASIGNA GÉNERO AL CLIENTE (orden de FER, 2026-09-22)
Encontrado en vivo: un producto de cosmética antiedad abría con **"Bienvenida"**. Lo compran hombres, y además se compra de regalo. **Es la fuga más silenciosa que existe:** el que se siente en la conversación equivocada no reclama ni pregunta, simplemente no contesta — y eso no aparece en ninguna métrica, porque se ve igual que un cliente frío.

Palabras de FER: *"si es hombre o mujer, puedes tener un saludo neutro o puedes saludar con el @"*. Tres salidas válidas, en orden de preferencia:

1. **Saluda al PRODUCTO, no a la persona.** Es la doctrina de Juanma —el saludo va a lo único que comparten comprador y vendedor— y de paso el problema desaparece: *"Hola! Soy Valentina, de <negocio>. Dame un momentico que te muestro el <producto> 👇"*. No hay género que asignar porque no se saluda a nadie por su condición.
2. **Salúdalo por su NOMBRE**, que es lo más cálido y también neutro. ⚠️ Ojo: ninguno de los 12 productos del espacio de referencia usa variables hoy (medido 2026-09-22, cero ocurrencias en los 12 campos), así que **el token exacto se confirma en el panel antes de usarlo** — no se copia de otra plataforma ni se supone.
3. **Forma neutra explícita:** "Bienvenido/a", "Bienvenid@". Funciona, pero se lee a formulario; úsala si las dos anteriores no aplican.

⛔ Lo mismo vale para "querido/a", "estimado/a" y "señor/señora" en cualquier campo que abra la conversación.

**Compuerta:** `validar.sh --campo saludo` bloquea el género asignado y deja pasar las tres salidas. Probada en los dos sentidos, 6 de 6.

## 2. Multimedia (la ESCALERA de apertura, sin precio — ver `recursos-visuales.md`)
**No son candidatas sueltas ni una lista de la que eliges una: son tres peldaños que se contestan en cadena.** Cada uno responde una pregunta distinta, en el orden en que el cliente se las hace:

1. **EL RESULTADO** — ¿de verdad se nota? Antes/después, o el producto haciendo lo que promete. Si el producto se entiende mejor en movimiento (un aparato, algo que se arma), aquí va un video de 8-15 s en vez de la imagen.
2. **EL MECANISMO** — ¿por qué funcionaría en mí? Qué es y cómo actúa, en concreto, con dos o tres beneficios cortos. Es el peldaño que casi nunca existe y el que más falta hace: si no está, se compone.
3. **LA PRUEBA** — ¿y si me estafan? Clientes reales, y la banda que quita el riesgo (envío gratis, pagas al recibir).

Un cuarto peldaño **solo** si el producto tiene variantes que hay que ver (tonos, tallas, fragancias). Y si el cliente llega de una pauta muy editada, el peldaño de la prueba puede ser la **imagen real del producto**, que ataca justo esa duda.

⛔ **Lo que NO entra en la apertura:** modo de uso, ficha técnica, tablas y listas de siete beneficios. Eso es material de consulta y va bajo disparador. Apilarlo al abrir es el catálogo que satura.
⛔ **Si no tienes los tres, manda los que tengas.** Dos peldaños reales valen más que tres con uno de relleno. La vía de CERO piezas también sigue siendo legítima y es la que más te diferencia.
🔴 **Con la escalera montada, el bloque anti-fuga del prompt deja de ser opcional:** Chatea reenvía la multimedia INICIAL COMPLETA cuando el cliente pide una imagen y el prompt no dice qué mandar (ver `plantilla-prompt.md`). Con una pieza eso era un ruido; con tres es el catálogo entero de golpe.
No hace falta texto entre pieza y pieza si la imagen ya trae texto.

⛔ El texto que acompaña la multimedia TAMPOCO lleva una pregunta que espere respuesta (no compitas con la pregunta de entrada). Puede ser una frase de expectativa ("mira esto 👇"), pero la única pregunta va en el paso 3.

## 3. Pregunta de entrada (tope nativo del campo: 1.000 caracteres)
Debe segmentar al cliente en los caminos que el prompt sabe responder. Ejemplo (producto con varios usos):
```
Cuéntame una cosa para asesorarte mejor 😊

Buscas [PRODUCTO] para [uso A], para [uso B], o para ambos?
```
Clave: que NO sea invasiva (sobre todo en productos sensibles) y que conecte con los pasos del prompt.

## 4. Recordatorios (dentro de la ventana de 24h)

### 🔴 LA LEY DEL RECORDATORIO
> **El objetivo del recordatorio NO es recordar que existimos. Es darle al cliente una RAZÓN NUEVA para volver a responder.**

Esa frase decide si un recordatorio sirve o es ruido. Porque el diagnóstico del recordatorio típico es demoledor: **el cliente ya sabe que estás ahí, simplemente no le importa.** Recordárselo otra vez no cambia nada.

⛔ **LO QUE NO SE DEBE HACER** (es lo que manda casi todo el mercado, y por eso no funciona):
- "Recuerda que tenemos garantía de 30 días, hay algo en lo que te pueda ayudar?"
- "Estoy aquí por si tienes dudas" · "estoy aquí para asesorarte" · "aquí estoy para lo que necesites"
- "Nos quedan solo las últimas 5 unidades, te gustaría apartar la tuya?" ← además suele ser urgencia inventada (ver LEY DE LA URGENCIA REAL)
- Repetir el precio o la oferta que ya mandaste.
Todos dicen lo mismo: *existimos, míranos, aquí estamos*. Ninguno le da al cliente algo NUEVO por lo que valga la pena escribir.

### 🔴 EL RECORDATORIO SE ESCRIBE COMO INSTRUCCIÓN, NO COMO TEXTO FIJO (aprendido en corrida real, 2026-09-22)

El campo de recordatorio de Chatea admite **dos formas**, y la skill venía entregando la peor:

- **Texto fijo** — se envía tal cual. Es lo que casi todo el mundo pone.
- **Instrucción para la IA** — se escribe como `EVENTO: … ` y el modelo COMPONE el mensaje en el momento.

**La instrucción gana, y no por estilo: por una razón estructural.** La ley del recordatorio exige darle al cliente una *razón nueva* para contestar, y buena parte de esa razón es **retomar el punto exacto donde se quedó la conversación**. Un texto fijo no puede saber dónde se quedó — se escribió antes de que la conversación existiera. Una instrucción sí. Un texto fijo solo puede hablar del producto en abstracto; por eso termina siempre en "sigo por aquí por si te quedó alguna duda", que es el antipatrón.

**Cómo se escribe una instrucción de recordatorio:**
```
EVENTO: [qué pasó — el cliente dejó de responder, es el segundo intento, etc.]
[Qué NO hacer, porque es lo que hace todo el mundo]
[Los movimientos, numerados y en orden]
[El límite: palabras, emojis, una sola pregunta]
[Y siempre: retoma donde quedó, sin repetir lo ya dicho]
```

⛔ **EL PRESUPUESTO, MEDIDO EN CAMPO Y NO ESTIMADO.** El campo tiene **800 caracteres** y una instrucción bien escrita come casi todos. En la corrida de 11 productos, una plantilla de 790 caracteres **reventó el tope en uno de ellos** (810) solo porque el gancho de ese producto era una frase más larga.
**Presupuesta ~650 y deja 150 de margen.** La parte variable por producto es la que crece, y crece justo donde no la estás mirando. Compruébalo siempre con `validar.sh --campo recordatorio <archivo>`.

### RECORDATORIO 1 (2 horas) — LA SEGUNDA CONEXIÓN
No es un recordatorio: es volver a conectar. **La premisa: si se fue, es porque le quedó una duda** — casi siempre de confianza, no de precio. Así que en vez de empujar, pregunta cuál es esa duda y ofrece demostrar.
```
Corazón, me quedó una inquietud 🙋

Hay algo que esté en mis manos que me ayude a demostrarte que tenemos el producto que necesitas?

Te quiero mostrar el caso de [nombre REAL de una clienta, ciudad]. Ella también tenía muchas dudas antes de empezar, mira su experiencia 👇
[TESTIMONIO REAL en video o imagen]

Si quieres, cuéntame qué es lo que más te genera duda y yo misma te digo con total sinceridad si considero que [PRODUCTO] tiene sentido para tu caso.
```
POR QUÉ FUNCIONA (los cuatro movimientos, no los cambies):
1. **No vende.** No pregunta "cuál te llevas" ni reenvía la oferta: pregunta por SU duda. El cliente siente que se preocupan por él, no que lo persiguen.
2. **Ofrece demostrar**, que es lo contrario de insistir: "hay algo que esté en mis manos para demostrarte…".
3. **Muestra a alguien que tuvo el mismo miedo** y lo resolvió — es la respuesta exacta a una duda de confianza.
4. **Cierra ofreciendo decirle que NO.** "Te digo con total sinceridad si considero que tiene sentido para tu caso" cambia el marco entero: lo pone en estado de EXCLUSIVIDAD y no de necesidad, y es la misma doctrina del tono asesor (recomendar con criterio aunque implique no vender). Ese giro es el que hace que responda.

### RECORDATORIO 2 (6 horas) — DISRUPTIVO, para romper el hielo
Segundo y último intento. Aquí no se vende NADA: solo se rompe la tensión con humor, porque a esas alturas el silencio ya se volvió incómodo para los dos.
```
Uishhh, ni mi ex me había ignorado así 😅
[imagen de la asesora, ver regla abajo]
```
- **Adapta el remate al país**: "ya no lloramos, facturamos" es dicho colombiano y en otro país no aterriza. Sustitúyelo por el equivalente local o quítalo: el "ni mi ex me había ignorado así" funciona solo.
- Funciona porque **rompe el guion comercial**: el cliente esperaba otro mensaje de venta y recibe algo humano. Pruébalo tú mismo con alguien que te tenga en visto y lo verás.
- Un solo intento. Si no responde, se cierra y pasa a remarketing.

**DOS VARIANTES DEL DISRUPTIVO — elige según lo que tengas:**
- **A · Foto de la asesora** (la de arriba). Más personal y más creíble, pero exige una foto real con permiso y que coincida con el perfil.
- **B · MEME.** Un meme conocido con texto tipo *"así de viejo me estoy poniendo esperando a que respondas"*. Ventajas sobre la foto: no necesita el consentimiento de nadie, no depende de un dicho local —viaja a cualquier país— y el formato ya es reconocible, así que el cliente entiende al instante que es humor y no venta. Es la opción por defecto cuando el negocio no tiene una persona real que ponga su cara.
⚠️ Con memes: sirven como HUMOR para romper el hielo, nunca para insinuar que alguien famoso respalda el producto. Un meme que hace reír está bien; una cara conocida puesta como si avalara lo que vendes es otra cosa y no se hace.

📌 **PRUÉBALO ANTES DE ADOPTARLO.** Estas dos variantes no salieron de una teoría: salieron de probarlas. Haz lo mismo — mándaselo a un amigo o a un familiar que te tenga en visto y mira si responde. Lo que funcione en esa prueba pequeña es lo que vale la pena poner en el bot; lo que te dé pena mandarle a un conocido, probablemente tampoco funcione con un cliente.

⚠️ **REGLA DE LA FOTO DE LA ASESORA** (si el recordatorio 2 lleva imagen):
- La foto debe ser de una **persona real que dio su permiso** para usarla como imagen de la asesora. Nunca una foto de banco de imágenes, nunca la de un tercero sin consentimiento, nunca una identidad robada.
- **Debe COINCIDIR con la foto de perfil del WhatsApp.** Si el perfil muestra a una persona y el mensaje envía otra cara, la credibilidad se cae de golpe y el efecto se invierte.
- Selfie natural, no producida: la gracia es que parezca lo que es, un mensaje de una persona.
- No le atribuyas a esa persona credenciales que no tiene (no la presentes como doctora, nutricionista o especialista si no lo es).

## 5. Remarketing (reabre la conversación tras varias horas)
Cada "Configuración Remarketing" en Chatea tiene un interruptor (activar) y TRES campos. La skill entrega los tres, listos:

**Campo 1 — Tiempo Remarketing:** número + unidad. FIJO: **Remarketing 1 = 3 Horas · Remarketing 2 = 8 Horas.**

**Campo 2 — Plantilla Mensaje:** es un desplegable donde se elige una **plantilla de Meta ya APROBADA**, o "No enviar plantilla". La plantilla se crea aparte en el Administrador de WhatsApp/Meta. La skill DISEÑA esa plantilla completa para que el vendedor la registre en Meta y luego la seleccione aquí. Anatomía de la plantilla de Meta:
- **Nombre:** minúsculas, SIN espacios, con guion bajo `_`. Ej.: `remarketing_1_[producto]`.
- **Categoría:** Marketing.  **Idioma:** Español.
- **Encabezado:** IMAGEN (ideal, del producto; la skill la genera o la pide, ver `recursos-visuales.md`).
- **Cuerpo:** texto con **variable `{{1}}` = nombre del cliente** (ej. "Hola {{1}} 😊 ..."). Meta pide un ejemplo de {{1}} (ej. "María").
- **Pie de página:** una línea corta y sobria; la skill la sugiere (ej. "[MARCA] · Pago contra entrega").
- **Botón(es):** 1 a 3 (CTA, ej. "Quiero pedirlo"). ⚠️ En el MAPEO del botón dentro de Chatea, ese botón se configura como **"botón de remarketing"** (así el clic enlaza al flujo). Indícaselo SIEMPRE al vendedor.
### 🔴 EL REMARKETING SIGUE LA MISMA LEY QUE EL RECORDATORIO
No es "recordarle que existimos" con plantilla de Meta: es **darle una razón nueva para volver**, y ahora con más peso, porque han pasado horas y el cliente ya se enfrió del todo. La diferencia con el recordatorio no es el tono: es que **aquí ya no puedes preguntar**, tienes un solo tiro y una plantilla aprobada.

**REMARKETING 1 (3h) — LA PRUEBA QUE NO ALCANZÓ A VER**
Se fue sin decidir: dale lo que probablemente le faltó. Encabezado con imagen (antes/después o testimonio real) y cuerpo que apunta al resultado, no al producto:
```
Hola {{1}} 👋 Te quedé debiendo algo: mira lo que le pasó a alguien que estaba justo donde tú.
[resultado concreto y real]
Si te sirve, te lo dejo listo hoy y pagas cuando lo recibas.
```
Botón: "Quiero verlo". Nunca "Comprar ahora": pide un paso más pequeño que la compra.

**REMARKETING 2 (8h) — LA PUERTA QUE SE CIERRA BIEN**
⚠️ Ajustado de 6h a 8h para evitar la COLISIÓN con el Recordatorio 2, que desde v3.36 también cae a las 6h: dos mensajes al mismo minuto se leen como spam y queman lo que ambos intentan rescatar.
Último contacto. No insistas: **cierra con elegancia y deja la puerta abierta.** Paradójicamente es el que más recupera, porque quita la presión.
```
Hola {{1}} 😊 No quiero seguir escribiéndote si no era el momento.
Te dejo esto por aquí y tú me dices cuando quieras: [beneficio en una línea].
Aquí estaré 💛
```
⛔ Prohibido en ambos: urgencia inventada, "últimas unidades" si no es cierto, y repetir la misma oferta con las mismas palabras que ya ignoró — si no leyó eso, no lo va a leer otra vez.
📌 La **instrucción de IA** de cada remarketing (campo 3) retoma sin reiniciar: usa lo que YA dijo el cliente, no vuelve al saludo ni repregunta lo contestado.

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

### 🔴 EL DISPARADOR CASA BYTE A BYTE, Y ESO TIENE UNA TRAMPA DE CLASE (ley de la casa, horneada v3.49.0)
Esta regla vivía solo en la memoria del ecosistema, y una regla que vive en la memoria **no es un guardarraíl: es un recuerdo.** Aquí queda dentro de la skill que produce el activador.

**El botón o enlace de WhatsApp que apunta al bot NO lleva texto: lleva un DISPARADOR, y casa BYTE A BYTE.** Fórmula canónica verificada:
```
Hola quiero información y precio de <PRODUCTO>
```
Sin coma después de "Hola". CON "y precio". Un carácter de diferencia y no casa.

**Qué pasa cuando no casa, y por qué nadie se entera:** el mensaje cae en *"Producto/Servicio no encontrado"* y aterriza en el tablero **"No automatizado"**, que no mira nadie. No hay error, no hay alerta: hay clientes que escribieron y a los que nunca contestó nadie.

⛔ **LA TRAMPA, y es de clase, no un descuido.** El nombre que dispara es **el registrado en el bot field**, y casi nunca coincide con el título comercial de la tienda. Disparador `Marca` contra `product.title` = *"Marca Spray | Frescura que Dura 48 Horas"*. **Tomar el título del producto automáticamente parece lo elegante y es EXACTAMENTE lo que rompe el byte a byte.** El disparador se copia A MANO del bot field. El título comercial solo sirve para mensajes que lee una persona (atención al cliente), nunca para el trigger.

Esto no es teoría: una skill hermana generó `"Hola, quiero informacion de X"` —coma de más, "y precio" de menos— y habría mandado a sus clientes al vacío.

⛔ SIN EMOJIS EN LA PALABRA CLAVE (regla de FER, 2026-07-25): la frase del activador y del botón va
SIN emoji al final. Dos razones de campo: (1) quien escribe la frase A MANO (vio el anuncio y abrió
WhatsApp directo) jamás teclea el emoji → el bot no dispara y la venta se pierde en silencio;
(2) algunos teléfonos/clientes alteran el emoji al pasar por el link wa.me y el match exacto se rompe.
Si la página ya tiene un botón con emoji, se corrige el botón — no se le pone emoji a la keyword.


VALIDACIÓN DURA DEL ACTIVADOR (antes de entregar): LA validación es `bash scripts/validar.sh --activador <archivo>` — usa una LISTA PERMITIDA (solo letras, números y puntuación básica) que bloquea CUALQUIER emoji o símbolo raro, de 3 o de 4 bytes. Contexto: los 4 bytes están PROBADOS corrompiendo el trigger (incidente real 2026-07-26 con un 👋); los de 3 bytes (✨ ✅ ‼ ⁉ ℹ) no están probados contra la base, así que el default seguro es cero. La fórmula `[c for c in t if ord(c) >= 0x10000]` solo caza los 4 bytes y NO basta como validación manual.
Corre `bash scripts/validar.sh --activador <archivo-con-el-activador>`: el veredicto exige 0 emojis de CUALQUIER tipo (4 bytes Y 3 bytes como ✨ ⛔ ✅) y sin BOM; si falla, bloquea con exit distinto de 0.

### 🔴 CREAR UN PRODUCTO NUEVO: LA RUTA QUE PARECE FUNCIONAR NO CREA NADA
Medido el 2026-09-22 por el Centro de Mando y confirmado aquí. **`set-bot-fields-by-name` NO CREA.** Si le mandas un producto entero a un nombre que no existe, devuelve **HTTP 200 con cara de éxito y no escribe nada**. Tres reintentos, tres 200, el campo nunca apareció. Un 200 de esa ruta sobre un nombre nuevo no significa absolutamente nada.

**La ruta que sí crea:** `POST /flow/create-bot-field` con `{"name": …, "var_type": …, "value": …}` → **201** con el `var_ns` nuevo.
- `var_type` es **obligatorio**: sin él, 422 *"The var type field is required"*.
- **Solo minúsculas**, y solo dos valen: `text` y `longtext`. `LONG_JSON`, `long_json`, `JSON`, `json` y `TEXT` devuelven 422 *invalid*.
- Para un producto va **`longtext`**, que es el que tienen los productos vivos.
- Para borrar: `DELETE /flow/delete-bot-field` con **`var_ns`**, nunca con `name` (422), y solo por DELETE (POST da 405).

⛔ **Y si el nombre ya existe, el create devuelve 400 "Bot field exists".** Eso NO es un error tuyo: es otro chat trabajando en el mismo espacio. Sube al siguiente número y reintenta (ver la regla de la medición que caduca).

### 🔴 LA MEDICIÓN DE UN ESPACIO COMPARTIDO CADUCA AL INSTANTE
Medido el 2026-09-22: a las 10:00 se midió que el slot 13 estaba libre y se informó así. A las 12:40 el servidor respondió *"Bot field exists"* — otro chat había montado ahí un producto distinto a las 12:21, en la ventana entre la medición y la escritura.

El POST falló como debía y no se pisó nada. **Pero un PUT sobre el `var_ns` lo habría borrado, sin error y sin aviso.**

**Cómo se escribe entonces:**
1. **Medir y crear en la MISMA corrida.** Nunca medir, preparar contenido una hora, y escribir después con el número viejo.
2. **Tratar el "ya existe" como otro chat trabajando**, no como fallo: subir al siguiente número y reintentar, hasta agotar un rango razonable.
3. **Cuando el sistema deja crear duplicados EN SILENCIO** (no hay colisión de nombre que te frene), releer el contenedor después de escribir y **CONTAR**. Sin releer reportas lo que creaste, no lo que quedó.

⛔ **El disparador extendido es UNA SOLA cadena con TODOS los productos**, así que escribirlo es reescribirlo entero: si otro chat añade su entrada entre tu lectura y tu PUT, se la borras. **Verificación obligatoria después de escribir:** releer y comprobar que siguen estando todas las entradas previas **más** la tuya. Reportar ese número no es un extra, es la prueba.

⛔ **Y la palabra corta vive en DOS sitios que tienen que coincidir:** el `keyW` de la entrada del disparador y el `palabras_clave` del propio producto. Escrita en uno solo, el disparo queda a medias según por dónde entre el cliente. Antes de elegirla, compárala contra todas las vivas en los dos sentidos —que la tuya no contenga a otra y que ninguna te contenga a ti—, porque si chocan el match se vuelve lotería y contesta el bot equivocado.

## 7. URLs dentro del prompt (recursos visuales conversacionales)
Las URLs que el AGENTE envía durante la conversación (no la multimedia inicial) van ESCRITAS dentro del prompt, con instrucción de cuándo enviarlas. Patrón:
```
Si pide ver [X], envía: https://...
```
Ubícalas en el paso donde tienen sentido (modo de uso en PASO 1 o soporte; tabla de precios en PASO 2; testimonios en PASO 3, etc.). No las modifiques ni acortes.
