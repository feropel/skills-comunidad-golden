---
name: golden-chatea-pro-config-carritos
description: Golden Group — Configura el asistente de CARRITOS ABANDONADOS de Chatea Pro: recupera por WhatsApp los checkouts/carritos que el cliente dejó a medias en la tienda, con una secuencia de reactivación (recordatorio suave → resolver objeción → urgencia honesta → último intento + incentivo) que reabre la conversación y cierra la venta o dispara el flujo logístico. Entrega cada mensaje en bloque copy-paste + las plantillas de Meta que la ventana de 24 h exige, todo alineado con la oferta, el tono y los datos de pago del asistente de ventas del mismo workspace. Úsala SIEMPRE que el usuario quiera montar o configurar el asistente de carritos / recuperación de carritos abandonados de Chatea Pro, "recuperar carritos", "mensajes de carrito abandonado", "configurar carritos de chatea pro", "reenganchar clientes que no terminaron la compra", "secuencia de recuperación". Para el remarketing de UNA conversación de venta por WhatsApp que se enfrió (no un checkout abandonado en la tienda), eso lo hace golden-chatea-pro-prompt-ventas. Para configurar TODOS los asistentes a la vez, usa golden-chatea-pro-full-configuracion.
---

# Golden · Chatea Pro — Asistente de Carritos Abandonados

<!-- skill v1.3.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): completada la ley de DOS NIVELES del techo — el tope de 20.000 escapados aplica al bot field tipo JSON legacy; un campo creado o convertido a LONG JSON aguanta hasta 500.000 (medido y validado en las hermanas config-comentarios v1.4.1 y config-ventas-wp v3.0). La cifra de esta skill era incompleta, no falsa: sin la mención a LONG JSON, quien la siga se autolimita. -->
<!-- skill v1.4 · 2026-08-21 (auditoría golden-skill-auditor 934→ORO): hallazgo real — el paso "Resolver la objeción" recomendaba prueba social pero el intake nunca pedía ese dato, y el ejemplo de vara de calidad traía una cifra inventada ("Más de 12.000 clientas") sin marcarla como dato real requerido; eso fosilizaba la fabricación de una cifra de negocio, justo lo que la LEY de arriba prohíbe entre espacios y el estándar Golden "datos reales antes de generar" prohíbe siempre. Se añadió el punto 7 al intake (prueba social real, opcional), la regla explícita de nunca inventar cifras de negocio, el chequeo en el QA, y se corrigió el ejemplo para dejar la cifra marcada como dato real del intake, no como técnica libre. -->
<!-- skill v1.3 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v1.2 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat CONFIG CHATEA KEVIN MX): confirmado desde el código de la app que el módulo Carritos (CartsPage) NO tiene topes nativos salvo los campos de correo — cierra parte del pendiente "verificar en vivo"; añadido el techo del bot field (20.000 ESCAPADOS ~ 17.000 crudos, corte silencioso con 200 ok); países limitados a los 7 que acepta la plataforma; higiene al clonar ([Carritos IA] Información de productos #N no se hereda) y regla de escribir y RELEER. -->
<!-- skill v1.1 · auditada con golden-skill-auditor 893→ORO: corregida la regla real de la ventana de 24h (contacto frío = plantilla en el primer toque), etiquetas unificadas (REACTIVACIÓN N), paso de QA + checklist de "terminado", modelo de plataforma marcado "verificar en vivo", changelog añadido -->

## LEY: NUNCA HEREDAR DATOS ENTRE ESPACIOS (FER 2026-08-08)

Al basarse en una cuenta guía (Golden o cualquier otra) se hereda **estructura, prompts y
configuración de asistentes** — JAMÁS datos, en ninguna dirección, ni entre marcas propias:

- **APIs y tokens** de cualquier tipo: ElevenLabs, OpenAI, Dropi, Shopify, el token del propio bot.
- **Plantillas de WhatsApp**: `name`, `namespace`, `lang` y `status` van atados al WABA de cada
  espacio; copiarlas rompe el destino (llama plantillas que su WABA no tiene o que Meta no aprobó).
- **Datos personales y de marca**: teléfonos, correos, dominios, nombre de la empresa, firmas en
  mensajes al cliente.
- **Productos** y sus disparadores.
- **Claims y cifras de negocio**: años en el mercado, número de clientes, porcentajes de
  entrega, premios. Heredarlos no rompe nada técnico — ningún barrido de llaves los detecta —
  pero ponen al bot a MENTIRLE al cliente con datos de otra empresa. Caso real (2026-08-08): la
  plantilla maestra clonada traía "Más de 100.000 clientes atendidos en Colombia" (dato de
  Golden) a punto de quedar en boca del bot de otro espacio.

**Única excepción autorizada:** Le'côterra como producto-ejemplo en los espacios de trabajo
(asistente de WhatsApp y de comentarios), para que la gente vea cómo se configura un producto.

**La guía tampoco puede llevar nada de eso adentro**: un material de referencia con una llave o un
dato personal ya está mal, aunque nadie lo copie.

**Método obligatorio al escribir en un espacio ajeno** — ANTES de escribir, barrer lo que se va a
escribir buscando `sk_`, `shpat_`, `eyJ`, teléfonos, correos, dominios, nombres de plantilla y de
marca del origen; si aparece algo, NO se escribe. DESPUÉS de escribir: releer del servidor y barrer
otra vez. Herramienta encadenable del barrido:
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (correrla ANTES de escribir y DESPUÉS releyendo del
servidor; sale con código 3 si encuentra algo CRITICA).

**LA MARCA VIVE TAMBIÉN EN PROSA LIBRE, no solo en campos estructurados.** Preservar las
llaves de identidad del destino NO basta: el nombre de la marca de origen viaja escondido dentro
de ganchos posventa, agradecimientos y plantillas de prompt. Al método de barrido se le añade el
paso `grep -i` por el NOMBRE de la marca de origen sobre TODO el texto que se va a escribir —
así se cazaron 10 menciones de la marca origen en 3 campos del destino que el mapeo de llaves
no vio.

Origen: 2026-08-08, al clonar la config de Golden a otro espacio se colaron la llave de ElevenLabs,
el teléfono, la plantilla de notificación y agradecimientos firmados con la marca del origen.
Revertido el mismo día desde respaldo.

Cómo clonar sin romper el destino (qué se copia, qué se preserva del destino, por qué las plantillas jamás viajan): memoria `reference_chatea_clonar_config_entre_espacios`.

### CAMPOS [Meta] = VALORES CALIENTES, NO INTERRUPTORES

Los bot fields `[Meta] Ver Contenido`, `[Meta] Agregar al carrito` y demás eventos de pixel los
**MUEVE EL FLUJO en tiempo real** mientras corren contactos — no son configuración estable. Caso
real (2026-08-08): se leyeron como "apagados" y cambiaron solos minutos después sin escritura de
nadie; la conclusión "el evento Comprar está apagado" tuvo que retractarse. **PROHIBIDO sacar
conclusiones de pauta o diagnóstico de una lectura suelta de esos campos**: se observan en ventana
(varias lecturas separadas en el tiempo) o se diagnostica el pixel en Meta directamente. Detalle:
memoria `reference_chatea_clonar_config_entre_espacios`.

Configura el asistente que **recupera carritos/checkouts abandonados** por WhatsApp: el cliente empezó a comprar en la tienda (dejó producto, a veces nombre y teléfono) y no terminó. Este asistente lo reengancha con una secuencia corta, humana y con un ángulo distinto por mensaje, hasta cerrar la venta o agotar los intentos.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. Usa el mismo país, oferta, tono y datos de pago que el **asistente de ventas** del workspace, para no contradecirlo. Si algo no coincide, manda lo que ya generó `golden-chatea-pro-config-ventas-wp`.
> **La plataforma solo acepta 7 países** (campo `[Comentarios IA] País`, MAYÚSCULA y sin acentos): COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY.

## Techos de caracteres (confirmado desde el código de la app, 2026-08-07)

- **Techo nativo del módulo Carritos (`CartsPage`): NO hay `maxLength`** en sus campos de texto. Solo los campos de **correo** (asunto y contenido) validan longitud, contra una tabla de un módulo compartido. Fuente: `TOPES-NATIVOS-POR-CAMPO.md` de CHATEA-PRO-ASISTENTES-MAPA.
- **Techo del bot field: 20.000 ESCAPADOS, no crudos** (~17.000 crudos: cada tilde ocupa 6 caracteres y cada emoji 12). Pasarse NO da error — la API responde `200 ok`, guarda cortado y el asistente muere en silencio; el error solo aparece en Panel → Registros de errores. Medir: `len(json.dumps(valor)[1:-1])` bajo 19.000. Tras escribir por API, **releer y comparar** siempre. **Nivel B — LONG JSON:** el tope de 20.000 es del campo tipo JSON legacy; si el bot field se crea o convierte a **LONG JSON**, el techo sube a 500.000 escapados (ley de dos niveles medida en las hermanas config-comentarios y config-ventas-wp). Con configuraciones grandes, convertir el campo a LONG JSON antes de escribir.
- **Al clonar un workspace a otro cliente:** vaciar `[Carritos IA] Información de productos #N` (son productos reales cacheados por el bot del dueño anterior) y jamás arrastrar `[Integraciones] Datos de integracion`.

## Qué es esto y qué NO es (límite con Ventas)

No confundir dos reactivaciones distintas del universo Chatea Pro:

- **Carritos (esta skill):** el disparador es un **checkout abandonado en la tienda** (Shopify / la web). El cliente casi nunca escribió por WhatsApp; el módulo de Carritos abre el chat para rescatarlo.
- **Recordatorios/Remarketing de Ventas (`golden-chatea-pro-prompt-ventas`):** el disparador es una **conversación de venta por WhatsApp que se enfrió** (escribió, no cerró). Va DENTRO del paquete del producto.

Comparten motor y estética (mensajes cortos, ventana de 24 h, plantillas de Meta), pero son campos y momentos distintos. Esta skill se ocupa solo del carrito.

## La regla de la ventana de 24 h (lo que decide si un mensaje necesita plantilla)

Esto es de WhatsApp/Meta, no de Chatea Pro, así que es fijo y no se inventa:

- El reloj de 24 h cuenta desde el **último mensaje del CLIENTE**, no desde el abandono del carrito.
- **Un carrito abandonado suele ser un contacto FRÍO:** el cliente dejó el checkout en la tienda pero **nunca escribió a tu WhatsApp**. Entonces **no hay ventana abierta y el PRIMER mensaje de recuperación ya exige una plantilla de Meta aprobada.** No se puede abrir con texto libre.
- **En cuanto el cliente responde**, se abre su ventana de 24 h y los mensajes siguientes pueden ir como **texto libre** (sin plantilla), mientras estés dentro de esas 24 h.
- Si vuelve a pasar de 24 h desde su última respuesta, el siguiente mensaje **vuelve a necesitar plantilla**.

Excepción: si el carrito viene de alguien que **sí tenía una conversación activa** (abandonó a mitad de chat), su ventana ya está abierta y el primer toque puede ir sin plantilla. En la duda, trátalo como frío → plantilla.

## Mecánica del módulo Carritos (modelo por defecto — VERIFICAR EN VIVO)

Chatea Pro reutiliza su **motor de reactivación** en todo el producto, así que arrancamos con el modelo ya conocido de `golden-chatea-pro-prompt-ventas` en lugar de partir de cero. **Trátalo como hipótesis a confirmar, no como hecho:**

- Cada paso de reactivación suele exponer 3 campos: **Tiempo** (cuándo dispara), **Plantilla Mensaje** (desplegable: una plantilla de Meta aprobada o "No enviar plantilla") e **Instrucción especial** (≤1000 caracteres: el MENSAJE + la `[Instrucción IA]` juntos).
- **Dato del carrito para personalizar:** producto, nombre y teléfono suelen venir; el link de pago/checkout a veces. No asumas que traes todos: escribe cada mensaje para que funcione aunque solo tengas el producto.

⚠️ **Pendiente que solo el dueño puede cerrar (verificar en vivo la 1.ª vez y guardar como nota):** los **nombres/etiquetas exactos del módulo Carritos**, **cuántos pasos** admite y **dónde vive** (en cuentas de referencia no aparece como ítem suelto del menú v1: revisar dentro del flujo del bot o en "Chatea PRO v2"). Si el módulo difiere de este modelo, ajústalo y **no inventes** campos ni límites. La regla de 24 h de arriba sí es fija.

**Lo que YA quedó confirmado (2026-08-07, del código de la app):** el módulo existe como `CartsPage` y sus campos de texto **no tienen tope nativo** (solo los de correo validan longitud) — ver la sección de techos arriba. El pendiente que queda es el de etiquetas, pasos y ubicación en el menú.

## Intake del negocio (pregunta 1 a la vez)

Reusa lo que ya definió el asistente de ventas del workspace; solo pregunta lo que falte.

1. **País** del workspace.
2. **Producto(s)** y su **oferta/precio** (debe coincidir exacto con el asistente de ventas).
3. **Modelo de pago** (contra entrega / anticipado / ambos). Si hay anticipado, los datos de la cuenta (para blindarlos, nunca confirmar sin comprobante).
4. **Incentivo de recuperación disponible** (envío gratis, descuento, regalo, bono) — si existe. Sin incentivo, el paso 4 cierra con valor/garantía, no con descuento.
5. **Tiempos de entrega por zona** — el mismo dato que Ventas y Logístico, para no contradecir.
6. **Nombre y tono del asistente** (el mismo del asistente de ventas).
7. **Prueba social real (opcional)** — número de clientes/reseñas o calificación, SOLO si el negocio la tiene y la confirma. Se usa en REACTIVACIÓN 2 (resolver objeción). Sin este dato, ese mensaje se apoya en garantía y contra entrega, nunca en una cifra inventada.

## Secuencia de recuperación (estructura ganadora)

Diseña **4 mensajes, cada uno con un ángulo distinto** — nunca repetir el mismo "no terminaste tu compra". Tiempos por defecto (ajústalos a lo que permita el módulo); el reloj de disparo arranca en el abandono del carrito. La columna "Plantilla Meta" aplica la regla de la ventana de 24 h de arriba:

| # (etiqueta) | Ángulo | Tiempo por defecto | Plantilla Meta |
|---|---|---|---|
| REACTIVACIÓN 1 | **Recordatorio suave** | ~20-30 min | **Sí** si el contacto está frío (lo normal) · No si ya tenía ventana abierta |
| REACTIVACIÓN 2 | **Resolver la objeción** | ~3-4 h | No si el cliente ya respondió (ventana abierta) · Sí si sigue frío |
| REACTIVACIÓN 3 | **Urgencia / escasez honesta** | ~20-24 h | No dentro de ventana abierta · Sí si pasó de 24 h |
| REACTIVACIÓN 4 | **Último intento + incentivo** | ~24-48 h | **Sí** (casi siempre fuera de las 24 h) |

1. **Recordatorio suave** (temprano): retoma con calidez, sin presión. Recuerda el producto y ofrece terminar en segundos. Ej: "Vi que dejaste [producto] casi listo, te ayudo a cerrar el pedido en 1 minuto."
2. **Resolver la objeción** (medio): ataca la razón típica de abandono — dudas de confianza, envío, forma de pago. Prueba social + garantía. **Contra entrega es el argumento fuerte:** "Pagas cuando lo recibes en tu casa, sin arriesgar nada."
3. **Urgencia / escasez honesta** (más tarde): stock real que baja, cierre de promo, tiempos de entrega que corren. **Nunca inventes escasez falsa.**
4. **Último intento + incentivo** (fuera de 24 h → plantilla Meta): el empujón final con el incentivo disponible (envío gratis / descuento / regalo). Tras este, **máximo 1-2 reactivaciones** y se suelta; sin desesperación ni acoso.

### Reglas de oro de los mensajes
- **Cortos** (≤35 palabras), **máx 2 emojis**, **UNA sola pregunta** por mensaje, tono humano local, nunca robótico, nunca "soy un bot".
- **Sin signos de apertura de interrogación ni exclamación** (solo el de cierre). Más humano, menos robótico.
- **Beneficio, no reproche:** reengancha por lo que **gana** el cliente, no por lo que "dejó a medias".
- **Precio claro** si lo pregunta; **anticipado blindado** (nunca confirmar sin comprobante).
- **Personaliza con lo que traiga el carrito** (nombre, producto) pero que el mensaje funcione aunque falte un dato.
- **Nunca inventes cifras de negocio** (número de clientes, reseñas, porcentajes de entrega, años en el mercado) en ningún mensaje — es la misma prohibición de la LEY de arriba, aplicada dentro de un solo espacio, no solo al clonar entre espacios. Úsalas solo si el negocio las confirmó en el intake (punto 7); si no hay dato real, el mensaje de objeción se apoya en garantía y contra entrega.
- Al cerrar, **dispara el flujo de venta/logístico** para tomar la dirección y confirmar el pedido (no reimplementes la validación de dirección aquí).

## Plantilla de Meta (para todo mensaje que caiga fuera de la ventana)

Todo mensaje a un contacto frío o fuera de las 24 h necesita una **plantilla de Meta aprobada**. Entrégala completa y lista para crear/seleccionar:

- **Nombre:** en `minúsculas_con_guion_bajo` (ej. `carrito_ultimo_intento`).
- **Categoría:** Marketing.
- **Idioma:** español.
- **Cuerpo:** con variable `{{1}}` = nombre del cliente. Ejemplo:
  `Hola {{1}}, te guardamos tu [producto] con [incentivo]. Lo activamos hoy y te llega contra entrega. Lo cerramos.`
- **Botón:** de respuesta rápida o CTA, mapeado como "botón de remarketing/carrito".
- Junto a la plantilla, entrega también el texto del **campo Instrucción especial** (mensaje + `[Instrucción IA]`) por si el módulo lo pide aparte.

## Entrega

- Cada mensaje en un **bloque copy-paste separado**, con su **título fuera del bloque** (etiqueta LIMPIA y uniforme: `REACTIVACIÓN 1`, `REACTIVACIÓN 2`… — sin paréntesis ni ángulo dentro del título). Cuando confirmes los nombres reales de los campos del módulo, renombra las etiquetas para que calcen con el módulo.
- El **ángulo** (recordatorio / objeción / urgencia / incentivo) y el **tiempo** (20 min / 3 h / 24 h) van en el texto del informe, **no dentro del bloque copiable**.
- Para cada mensaje, marca claramente **si necesita plantilla de Meta** (contacto frío / fuera de 24 h) o va como texto libre. Para los que la necesitan, separa cada campo de la plantilla (nombre, cuerpo, botón, instrucción IA).
- Cierra con un **resumen de configuración**: qué paso va en qué campo del módulo Carritos, su tiempo y si lleva plantilla.
- Toma `references/ejemplo-completo.md` como vara de calidad de la salida.

### QA antes de entregar (autochequeo obligatorio)
Antes de dar la secuencia por lista, verifica y corrige:
- [ ] **Precio, oferta y datos de pago** idénticos a los del asistente de ventas (`golden-chatea-pro-config-ventas-wp`). Si no coinciden, manda Ventas.
- [ ] **Tiempos de entrega** iguales a Ventas y Logístico.
- [ ] Cada mensaje: ≤35 palabras, máx 2 emojis, 1 sola pregunta, sin signos de apertura, beneficio (no reproche).
- [ ] **Sin cifras de negocio inventadas** (clientes, reseñas, porcentajes): si aparece una, viene del intake (punto 7) o se retira.
- [ ] **4 ángulos distintos** (ningún mensaje repite el mismo gancho).
- [ ] El **primer mensaje** trae plantilla de Meta si el contacto es frío (caso normal).
- [ ] Cada mensaje fuera de la ventana tiene su **plantilla completa** (nombre, cuerpo con `{{1}}`, botón).
- [ ] El cierre **dispara venta/logístico** para dirección y confirmación.

**Terminado =** los 4 bloques copy-paste + sus plantillas de Meta donde aplique + el resumen de configuración, con el checklist de arriba todo en verde. Lo único que puede quedar pendiente son los nombres/pasos reales del módulo Carritos si aún no se verificaron en vivo (se entrega igual, marcando ese pendiente).

## Conexiones (skills hermanas)
- 🛒 Asistente de ventas (misma oferta y datos de pago) → `golden-chatea-pro-config-ventas-wp`
- 🎯 Prompt/promo + recordatorios/remarketing por producto → `golden-chatea-pro-prompt-ventas`
- 📦 Asistente logístico (toma la dirección al cerrar) → `golden-chatea-pro-config-logistico`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

Si una hermana no está instalada, entrega igual la secuencia de carritos y avisa qué pieza queda por conectar (no bloquees el trabajo por una dependencia ausente).

## Privacidad (skill compartible)
Nunca hornees datos reales (producto, precios, cuentas de pago, tienda, nombres) en los archivos de la skill. Se preguntan en cada uso y viven solo en los mensajes entregados. Los ejemplos internos son ficticios.
