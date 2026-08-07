---
name: golden-chatea-pro-config-carritos
description: Golden Group — Configura el asistente de CARRITOS ABANDONADOS de Chatea Pro: recupera por WhatsApp los checkouts/carritos que el cliente dejó a medias en la tienda, con una secuencia de reactivación (recordatorio suave → resolver objeción → urgencia honesta → último intento + incentivo) que reabre la conversación y cierra la venta o dispara el flujo logístico. Entrega cada mensaje en bloque copy-paste + las plantillas de Meta que la ventana de 24 h exige, todo alineado con la oferta, el tono y los datos de pago del asistente de ventas del mismo workspace. Úsala SIEMPRE que el usuario quiera montar o configurar el asistente de carritos / recuperación de carritos abandonados de Chatea Pro, "recuperar carritos", "mensajes de carrito abandonado", "configurar carritos de chatea pro", "reenganchar clientes que no terminaron la compra", "secuencia de recuperación". Para el remarketing de UNA conversación de venta por WhatsApp que se enfrió (no un checkout abandonado en la tienda), eso lo hace golden-chatea-pro-prompt-ventas. Para configurar TODOS los asistentes a la vez, usa golden-chatea-pro-full-configuracion.
---

# Golden · Chatea Pro — Asistente de Carritos Abandonados

<!-- skill v1.1 · auditada con golden-skill-auditor 893→ORO: corregida la regla real de la ventana de 24h (contacto frío = plantilla en el primer toque), etiquetas unificadas (REACTIVACIÓN N), paso de QA + checklist de "terminado", modelo de plataforma marcado "verificar en vivo", changelog añadido -->

Configura el asistente que **recupera carritos/checkouts abandonados** por WhatsApp: el cliente empezó a comprar en la tienda (dejó producto, a veces nombre y teléfono) y no terminó. Este asistente lo reengancha con una secuencia corta, humana y con un ángulo distinto por mensaje, hasta cerrar la venta o agotar los intentos.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. Usa el mismo país, oferta, tono y datos de pago que el **asistente de ventas** del workspace, para no contradecirlo. Si algo no coincide, manda lo que ya generó `golden-chatea-pro-config-ventas-wp`.

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

## Intake del negocio (pregunta 1 a la vez)

Reusa lo que ya definió el asistente de ventas del workspace; solo pregunta lo que falte.

1. **País** del workspace.
2. **Producto(s)** y su **oferta/precio** (debe coincidir exacto con el asistente de ventas).
3. **Modelo de pago** (contra entrega / anticipado / ambos). Si hay anticipado, los datos de la cuenta (para blindarlos, nunca confirmar sin comprobante).
4. **Incentivo de recuperación disponible** (envío gratis, descuento, regalo, bono) — si existe. Sin incentivo, el paso 4 cierra con valor/garantía, no con descuento.
5. **Tiempos de entrega por zona** — el mismo dato que Ventas y Logístico, para no contradecir.
6. **Nombre y tono del asistente** (el mismo del asistente de ventas).

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
