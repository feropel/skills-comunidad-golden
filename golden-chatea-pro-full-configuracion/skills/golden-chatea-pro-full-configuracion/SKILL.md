---
name: golden-chatea-pro-full-configuracion
description: Golden Group — ORQUESTADOR MAESTRO de Chatea Pro. Configura de punta a punta TODOS los asistentes de un espacio de trabajo (Comentarios, Logístico, Ventas WhatsApp y Carritos) llamando a las skills hijas especializadas, y garantiza que todas queden coherentes entre sí (misma voz de marca, mismo país, mismos datos de producto). Úsala SIEMPRE que el usuario quiera montar o configurar CHATEA PRO COMPLETO / TODO el bot / TODOS los asistentes de una tienda, o diga cosas como "configúrame todo chatea pro", "monta el bot completo", "configuración full de chatea pro", "arma todos los asistentes", "deja chatea pro listo", "configura mi espacio de trabajo de chatea pro". Si el usuario solo quiere UN asistente puntual (solo comentarios, solo logístico, solo ventas, solo carritos), esta skill lo deriva a la skill hija que corresponde. NO genera ella misma los JSON ni los prompts: dirige, ordena y audita a las skills hijas.
---

# Golden · Chatea Pro — Full Configuración (orquestador maestro)

<!-- skill v1.2 · 2026-08-21 (auditoría golden-skill-auditor 918/1000 PLATA → reparada) · 🔴 el mapa de hijas declaraba "Dos asistentes tienen skill hija" y omitía por completo `golden-chatea-pro-producto-comentarios` (el hijo de Comentarios, equivalente a prompt-ventas para Ventas: existe, está instalado, y config-comentarios ya lo cita como su propio hijo) — el orquestador dejaba huérfano el paso de cargar la ficha de cada producto en el asistente de Comentarios. Corregido en la tabla de asistentes, en el párrafo de hijas (ahora TRES), en PASO 1 (Comentarios invoca a producto-comentarios por cada producto) y en el mapa de derivación; sumado un chequeo de coherencia de producto entre Ventas/Carritos/Comentarios en PASO 2. -->
<!-- skill v1.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- v1.0 · sin sello previo -->

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


Esta skill es el **director de orquesta** de todo el ecosistema Chatea Pro de Golden. No hace el trabajo pesado ella misma: **llama, ordena y audita** a las skills hijas especializadas para dejar un espacio de trabajo 100% configurado y coherente. Es liviana en contenido y fuerte en criterio: su valor es coordinar, detectar huecos y corregir a cada asistente.

## Qué es Chatea Pro (contexto obligatorio)

Chatea Pro trabaja por **espacio de trabajo (workspace)**. Regla de hierro:

> **1 espacio de trabajo = 1 país.** Un workspace solo se conecta a un país. Toda la configuración (transportadoras, nomenclatura de dirección, medios de pago, tono) se define por ese país.

Dentro de un espacio de trabajo viven **4 asistentes**, cada uno con su configuración propia:

| Asistente | Qué hace | Skill hija que lo configura |
|---|---|---|
| 💬 **Comentarios** | Responde comentarios públicos de posts/anuncios, clasifica negativos y lleva la conversación al DM/venta | `golden-chatea-pro-config-comentarios` (padre) + `golden-chatea-pro-producto-comentarios` (hijo: la ficha de cada producto) |
| 📦 **Logístico** | Valida la dirección del cliente antes del envío COD (responde en una sola línea: correcta / falta info) | `golden-chatea-pro-config-logistico` (padre) + `golden-chatea-pro-validacion-direcciones` (hijo: el prompt de validación) |
| 🛒 **Ventas WhatsApp** | Agente conversacional que vende por WhatsApp (config general del asistente por workspace/país + productos) | `golden-chatea-pro-config-ventas-wp` |
| 🔁 **Carritos** | Recupera carritos/checkouts abandonados por WhatsApp con recordatorios y remarketing | `golden-chatea-pro-config-carritos` |

Tres asistentes tienen una skill **hija** que hace su trabajo fino:
- **Ventas WhatsApp** → cada **producto** tiene su **promo** (prompt de venta), que genera `golden-chatea-pro-prompt-ventas`.
- **Logístico** → su **prompt de validación de direcciones** lo genera `golden-chatea-pro-validacion-direcciones`.
- **Comentarios** → cada **producto** tiene su ficha de 5 llaves (`img/name/desc/rela/estado`) para que el bot sepa de qué producto habla cada comentario, que genera `golden-chatea-pro-producto-comentarios`.

## Cuándo usar esta skill vs. una hija directa

- **Full (esta skill):** el usuario quiere montar/configurar TODO el bot de una tienda. Aquí orquestas las 4 (o las que apliquen).
- **Puntual (deriva a la hija):** el usuario solo quiere un asistente. No reimplementes: invoca directamente la skill hija correspondiente y punto.

Nunca dupliques la lógica de una hija dentro de esta skill. Tu trabajo es dirigir.

## Dos modos de operación (detéctalo ANTES de preguntar nada)

**MODO A — Workspace nuevo/vacío:** intake completo (PASO 0) y se genera todo desde cero.

**MODO B — Workspace de un cliente YA configurado** (te dan el token de un espacio que el cliente
llenó). Protocolo validado en producción con el primer cliente real (2026-07-09):

1. **LEER TODO primero.** Baja los ~69-79 Bot Fields por API y clasifícalos ANTES de preguntar
   nada: el cliente ya respondió muchas preguntas del intake con lo que dejó escrito. Preguntar
   solo lo que falte, sin repetirle lo que ya llenó.
2. **Backup completo** de todos los campos (archivo con timestamp, `chmod 600` — trae secretos:
   tokens Dropi/Shopify/OpenAI/Meta CAPI, keys de Maps, voz).
3. **Identificar la tienda REAL:** la Shopify conectada en `[Integraciones] Datos de integracion`
   es la fuente de verdad — el dominio `*.myshopify.com` redirige al dominio real (verifícalo con
   curl). No te fíes del nombre de tienda que aparezca en los textos de los asistentes.
4. **Detectar contaminación de otra tienda:** es COMÚN que la config venga reciclada de otro
   negocio (plantilla copiada de otro workspace). Señales: nombres de tienda/URLs/historias
   distintas entre asistentes (ej. Logístico dice tienda X y Carritos/Comentarios dicen tienda Y),
   WhatsApp inválido (celular colombiano = 10 dígitos), años de operación contradictorios, moneda
   equivocada (USD en un workspace COP). Todo se unifica hacia la tienda real.
5. **Diagnóstico al dueño ANTES de tocar:** qué está lleno ✅, qué está vacío, qué está
   incoherente, con propuesta de corrección por convención. El dueño autoriza.
6. **Regla de hierro del dueño:** los **datos de negocio predeterminados del cliente SE
   RESPETAN** (fletes, porcentajes de validación, booleans/interruptores, tiempos de envío,
   plantillas Meta, saludos que el cliente escribió). Lo que SÍ se corrige/mejora con
   autorización es **identidad y comportamiento**.
7. **NUNCA cambiar el nombre del asesor/asistente sin preguntar.** El nombre lo decide el
   cliente. Igual la URL, el WhatsApp y todo dato de identidad: se PREGUNTAN y se toman SOLO de
   la información que entregue el dueño (por texto, archivo o foto). Si un dato luce inválido,
   verifícalo contra la web del cliente (ej. el wa.me publicado en su tienda) — jamás inventarlo.
8. **Verificación post-push:** releer cada campo del servidor y comparar contra lo enviado.
9. **Registro por cliente** en `PROYECTOS/<CLIENTE>/`: backup pre-cambios, config aplicada,
   token (`chmod 600`) y `REGISTRO-CAMBIOS.md` con cada cambio aplicado y los pendientes.
10. **Ediciones concurrentes:** si el dueño o el cliente trabaja el workspace en la UI al mismo
    tiempo, tus campos pueden ser sobrescritos (pasó en vivo el mismo día). Antes de cualquier
    push, RELEE el campo; si cambió desde tu última lectura, avisa y coordina. Si el dueño dice
    que él está trabajando el espacio, pasa a solo-lectura inmediatamente.

## Reporte obligatorio de cambios (regla del dueño)

TODO cambio se reporta SIEMPRE con este formato, sin excepción — y debe poder reconstruirse
después desde el backup (diff campo por campo):

> **Asistente → Campo (y dónde se ve en la UI) → texto ANTES → texto DESPUÉS**

## Método de prompts "cien de cien" (regla del dueño)

Para TODO prompt de identidad/comportamiento de un asistente (rol de ventas, restricciones,
analizador de palabra clave, saludo, anticancelación, ganchos de venta):

1. **La semilla es el prompt base del dueño**, NO el que traiga el workspace. El master de
   ventas vive en `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/PROMPT-BASE-FER-ventas-general2.json`
   (rol de cierre por WhatsApp + restricciones + analizador de palabra clave). Los prompts que
   trae un workspace de cliente son básicos: se ANALIZAN y se les rescata lo mejor que tengan,
   pero no son la base.
2. **Proceso obligatorio antes de escribir:** calificar → clasificar → comprimir → analizar →
   EXTENDER. Fusión = lo mejor del prompt del dueño + lo mejor de lo existente + criterio propio
   = un solo prompt cien de cien.
3. **Capacidad del campo:** el tope lo pone el **TIPO** de Bot Field, no la plataforma (medido
   por API el 2026-07-25): tipo **JSON** = 20000 · tipo **LONG JSON** = **500000** (25x).
   **Crea todos los campos de configuración como LONG JSON.** Con eso el prompt deja de estar
   apretado: la referencia de "llegar al 90-95% del límite" aplicaba al tope viejo de 20000
   (~18000-19000 en el JSON completo) y sigue siendo la vara de cuánta potencia debe tener el
   prompt — no un techo que haya que rozar.
   ⚠️ **Pasarse del tope NO da error:** la API responde `200 {"status":"ok"}` y guarda el
   contenido **cortado**. Todo push tiene que releer el campo y comparar la longitud
   (`push_config.py` de la skill de ventas-wp ya lo hace). Sin esa verificación se puede mutilar
   la configuración de un asistente sin que nada avise.
   Los campos que ya existen como JSON **no se convierten por API**: borrar y recrear cambia el
   `var_ns` y rompe las referencias del flujo. El tipo se cambia en la UI.
4. **Adaptado SIEMPRE a la tienda y al país** — nunca verbatim: nombre del asesor del cliente,
   su URL, sus claims y ejemplos de su vertical.
5. **CERO rastros de Golden en clientes:** el prompt base del dueño trae horneada la URL de la
   tienda Golden en el analizador de palabra clave ("…puedes conseguirlo en nuestra página web
   👉 …"). En cada despliegue se reemplaza por la web DEL CLIENTE, y se audita que ningún texto
   final mencione a Golden Group ni sus dominios.
6. **Presentar el prompt final al dueño ANTES de escribirlo** al workspace, con su calificación
   y qué se tomó de cada fuente.

## Flujo de orquestación

### PASO 0 — Encuadre del espacio de trabajo (pregunta 1 a la vez)
1. **Negocio / tienda** que se va a configurar.
2. **País del workspace** (recuerda: 1 workspace = 1 país). Este dato manda sobre todas las hijas.
3. **Qué asistentes quiere montar:** los 4, o solo algunos. (Por defecto propón los 4.)
4. **Datos base de marca compartidos** que todas las hijas necesitan para ser coherentes: nombre del asistente/marca, tono, contacto de referencia, tiempos de entrega por zona, y modelo de pago (contra entrega / anticipado / ambos).

> Estos datos base se preguntan UNA sola vez aquí y se pasan a cada hija, para que no le pregunten lo mismo al usuario cuatro veces ni queden datos distintos entre asistentes.

### PASO 1 — Orden de configuración recomendado
Configura en este orden (cada uno invocando su skill hija y pasándole país + datos base):
1. **Ventas WhatsApp** (`golden-chatea-pro-config-ventas-wp`) → es el corazón; define productos y voz de venta.
   - Por cada producto, dispara la **promo** con `golden-chatea-pro-prompt-ventas`.
2. **Comentarios** (`golden-chatea-pro-config-comentarios`) → alinea la respuesta pública con la misma voz y lleva al DM de ventas.
   - Por cada producto, carga su ficha con `golden-chatea-pro-producto-comentarios` (mismo objeto de 5 llaves que ya armaste al montar Ventas — reutilízalo, no lo reinventes).
3. **Logístico** (`golden-chatea-pro-config-logistico`) → config operativa (transportadoras/tiempos) + su hijo `golden-chatea-pro-validacion-direcciones` arma el prompt con el pack del país.
4. **Carritos** (`golden-chatea-pro-config-carritos`) → recupera los abandonos con la misma oferta y datos de pago.

### PASO 2 — Auditoría de coherencia (el valor real del maestro)
Cuando cada hija entregue su config, NO termines: revisa que todas encajen. Corrige si algo no cuadra:
- **Mismo país** en las 4 (nomenclatura de dirección, transportadoras y pago consistentes con el pack de país).
- **Misma voz de marca** (nombre del asistente, tono, sin signos de apertura, humano, nunca "soy un bot").
- **Mismos datos de producto y precios** entre Ventas, Carritos y Comentarios (que no haya un precio o un nombre de producto en un asistente y otro distinto en el resto; la ficha de Comentarios reutiliza el mismo producto que ya armaste en Ventas, no uno nuevo).
- **Mismos datos de pago anticipado** (si aplica) en Ventas y Carritos.
- **Mismos tiempos de entrega** en Logístico, Ventas y Carritos.
- **Handoff correcto:** Comentarios → lleva a la venta; Ventas → dispara Logístico al pedir dirección; Carritos → reengancha con la misma oferta.

Entrega un **checklist final** marcando cada asistente configurado, su país, y las incoherencias que corregiste.

## Reglas de oro del orquestador
- **No hagas el trabajo de las hijas.** Si te descubres escribiendo un prompt de venta o un JSON, párate y llama a la hija.
- **Si falta una skill hija instalada**, dilo con claridad y ofrece el camino: instalarla o configurar ese asistente manualmente. Nunca inventes el contenido de una hija ausente.
- **Datos reales antes de generar:** precio, WhatsApp, cuentas de pago y claims SIEMPRE se preguntan/confirman; nunca se inventan (aplica a todas las hijas).
- **Un workspace, un país.** Si el usuario pide dos países, son dos workspaces y dos corridas de esta skill.
- **En workspaces de cliente (MODO B):** datos de negocio del cliente se respetan; identidad se mejora solo con autorización; el nombre del asesor JAMÁS se cambia sin preguntar.
- **Todo cambio se reporta** asistente → campo → ANTES → DESPUÉS (formato obligatorio del dueño).
- **Prompts siempre por el método cien de cien** (semilla del dueño + lo mejor de lo existente + extender al 90-95% del campo), presentados al dueño antes del push.
- **Cero rastros de Golden** (nombre o dominios) en cualquier workspace de cliente.

## Skills hijas (mapa de derivación)
- 💬 Comentarios (padre) → `golden-chatea-pro-config-comentarios`
- 🗂️ Ficha de producto en Comentarios (hijo de Comentarios) → `golden-chatea-pro-producto-comentarios`
- 📦 Logístico (padre) → `golden-chatea-pro-config-logistico`
- 🧭 Validación de direcciones (hijo del logístico) → `golden-chatea-pro-validacion-direcciones`
- 🛒 Ventas WhatsApp (padre) → `golden-chatea-pro-config-ventas-wp`
- 🎯 Promo por producto (hijo de Ventas) → `golden-chatea-pro-prompt-ventas`
- 🔁 Carritos → `golden-chatea-pro-config-carritos`

## Carga automática por API (verificado en vivo 2026-07-09)

Chatea Pro es whitelabel de **UChat**: TODA la config de los 4 asistentes vive en **Bot Fields
JSON** y se lee/escribe por API (`https://chateapro.app/api`, auth Bearer atada al bot/flujo).
Esto permite armar el workspace COMPLETO por API, sin pegar a mano. El mapa maestro de los 79 Bot
Fields (clasificados por asistente, con el esquema de claves de cada config) está levantado en
`PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/MAPA-FULL-CONFIGURACION.md` + `extraccion/esquemas/`.

Campos de config por asistente: Ventas (`[Ventas Wp] Configuracion general` +2), Logístico
(`[Logistico] Configuracion General` + Confirmaciones + Seguimiento + Novedad + Plantillas),
Carritos (`[Carritos] Configuracion` + Información de productos), Comentarios
(`[Comentarios] Configuracion General` + Productos), Remarketing, Meta pixel, Integraciones.

El pusher genérico vive en `golden-chatea-pro-config-ventas-wp/scripts/push_config.py`
(read → backup → push --confirm por `set-bot-fields-by-name`). Gotchas: token atado a flujo
(sin flujo = 404 "Flow not found"), User-Agent de navegador (Cloudflare 1010), pares
nombre=archivo antes de --confirm. Token = dato sensible: scope mínimo, rotar al terminar.

**Gotchas adicionales (producción, 2026-07-09):**
- `GET /flow/bot-fields` está **PAGINADO: 10 campos por página**. Para leer/respaldar TODO hay
  que recorrer `meta.last_page` (`?page=N`) y unir los `data`. Un backup de una sola página
  pierde ~85% del workspace. (`push_config.py read/backup` consulta por nombre, eso sí trae el
  campo completo; el inventario total requiere paginar.)
- La lista de campos varía por workspace (69 en el del cliente vs 79 en el de referencia): no
  asumas que existen todos (ej. Remarketing puede no estar según la versión del bot). Clasifica
  lo que HAY.
- Verificación de escritura: el `PUT` responde 200 con `matched_items`; aún así, relee el campo
  y compara — es la única prueba real (y detecta si alguien pisó tu cambio desde la UI).
- Las plantillas de Meta (namespace propio por cliente) solo se REFERENCIAN por API, no se crean
  ni se aprueban: si una está `PENDING`, se resuelve en Meta, no aquí.

## Privacidad (skill compartible con la comunidad)
Esta skill se comparte. Nunca hornees datos de un negocio real (nombres, precios, cuentas de pago, números, tiendas) en sus archivos: se preguntan en cada uso y viven solo en la config entregada. Los ejemplos internos son ficticios.
