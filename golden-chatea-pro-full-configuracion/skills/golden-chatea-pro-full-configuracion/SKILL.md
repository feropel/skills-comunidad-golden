---
name: golden-chatea-pro-full-configuracion
description: Golden Group — ORQUESTADOR MAESTRO de Chatea Pro. Configura de punta a punta TODOS los asistentes de un espacio de trabajo (Comentarios, Logístico, Ventas WhatsApp y Carritos) llamando a las skills hijas especializadas, y garantiza que queden coherentes entre sí (misma voz de marca, mismo país, mismos datos de producto). Úsala SIEMPRE que el usuario quiera montar o configurar CHATEA PRO COMPLETO / TODO el bot / TODOS los asistentes de una tienda ("configúrame todo chatea pro", "monta el bot completo", "arma todos los asistentes", "deja chatea pro listo"), INSTALARLE CHATEA A UN CLIENTE entregando datos del negocio y el token de un workspace ("instálale chatea a este cliente", "monta el bot de mi cliente", "aquí está el token del espacio"), o arreglar un espacio ya configurado o heredado de otra cuenta ("revisa y arregla el chatea de este cliente", "este workspace vino con datos de otra tienda"). Si solo quiere UN asistente puntual (solo comentarios, solo logístico, solo ventas, solo carritos), esta skill lo deriva a la hija que corresponde. NO genera ella misma los JSON ni los prompts: dirige, ordena y audita a las skills hijas.
---

# Golden · Chatea Pro — Full Configuración (orquestador maestro)

<!-- skill v1.4 · 2026-08-23 (auditoría golden-skill-auditor 804/1000 BRONCE → reparada) · alineación con el BRIEFING-PARA-SKILLS del 2026-08-07, que la skill no había absorbido. 🔴 CRÍTICO 1: el método cien de cien mandaba llenar "al 90-95%, ~18000-19000 crudos" — el techo real son 20.000 ESCAPADOS (~17.000 crudos, tilde=6 chars, emoji=12) y está MEDIDO que 19.922 crudos = 23.266 escapados = el asistente NO arranca, con la API respondiendo 200 ok y guardando cortado: la skill instruía exactamente el rango que mata la instalación. Reescrito como DOS TECHOS con tabla medida y la fórmula len(json.dumps(v)[1:-1]) < 19.000. 🔴 CRÍTICO 2: faltaba por completo el Techo B (tope NATIVO de cada campo del formulario, extraído del código de la app) — escribir por encima funciona por API pero el panel corta el texto al guardar; añadidos los topes más apretados + puntero a TOPES-NATIVOS-POR-CAMPO.md. 🔴 CRÍTICO 3: la definición de terminado era un checklist que llenaba quien construyó — la causa medida de seis fallas seguidas; nuevo PASO 3 COMPUERTA DE VERIFICACIÓN con el agente golden-verificador (adversarial, recibe solo el estado final), verificacion_final.py y relectura del servidor, reportando COBERTURA y nunca "quedó perfecto". 🔴 CRÍTICO 4: mandaba configurar [Logistico] Plantillas de mensaje, campo MUERTO (relleno "namespace":"string"; las plantillas reales viven dentro de Confirmaciones/Seguimiento/Novedad). 🔴 CRÍTICO 5: afirmaba un censo fijo de campos ("los 79", "~69-79") ya falso tres veces (56/69/79/82 según espacio y fecha) — reemplazado por "re-extrae paginando y clasifica lo que HAY". Añadidos: los 7 países que acepta la plataforma con lo que cambia de verdad entre ellos (código postal obligatorio en México, sin recogida en oficina, domicilio=casa) y la advertencia de que un pack clonado hereda el criterio equivocado; Le'côterra siempre inactivo (enseña, no vende); el encargo típico de instalación a cliente con su definición de terminado; la fuga menos obvia al clonar (nombres de producto y paquetería DENTRO de los ganchos de venta del logístico) y la lista de campos a vaciar; gotchas de API (llave data si no 400, create-bot-field con var_type+value si no 422, paginación con per_page ignorado, ensure_ascii/separators, trigger sin caracteres de 4 bytes, cada llave conserva su tipo, producto de Comentarios de 5 llaves exactas, pares array/Extendido donde array vacío NO significa sin productos, img de Comentarios que solo nace subiendo en el panel); valores por defecto que NO son defectos (comparar contra un workspace que funcione, no contra lo que uno supone); description ampliada al disparo real (instalar a un cliente con token, arreglar un espacio heredado). -->
<!-- skill v1.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
<!-- skill v1.2 · 2026-08-21 (auditoría golden-skill-auditor 918/1000 PLATA → reparada) · 🔴 el mapa de hijas declaraba "Dos asistentes tienen skill hija" y omitía por completo `golden-chatea-pro-producto-comentarios` (el hijo de Comentarios, equivalente a prompt-ventas para Ventas: existe, está instalado, y config-comentarios ya lo cita como su propio hijo) — el orquestador dejaba huérfano el paso de cargar la ficha de cada producto en el asistente de Comentarios. Corregido en la tabla de asistentes, en el párrafo de hijas (ahora TRES), en PASO 1 (Comentarios invoca a producto-comentarios por cada producto) y en el mapa de derivación; sumado un chequeo de coherencia de producto entre Ventas/Carritos/Comentarios en PASO 2. -->
<!-- skill v1.1.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v1.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → otra marca 2026-08-08 (se colaron una credencial, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat otro espacio de Chatea 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
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
**Va SIEMPRE con `estado: inactivo`: enseña, no vende.** Un producto-ejemplo activo le responde
a clientes reales del cliente con un producto que no es suyo.

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

**La fuga menos obvia: los nombres de PRODUCTO y de PAQUETERÍA dentro de los ganchos de venta del
logístico.** No son configuración, son ejemplos — y la IA imita el ejemplo: con un producto ajeno
adentro escribe frases que venden lo que el cliente no vende. En una cuenta heredada aparecieron
transportadoras colombianas y la marca del profesor dentro del workspace de un alumno. Al barrer,
mira también los ganchos por estado (guía generada, en reparto, en oficina, entregado).

**Vaciar SIEMPRE antes de entregar a otro cliente:** `[Integraciones] Datos de integracion`
(llaves de Dropi, Shopify, OpenAI, Meta y Maps en texto plano), `[Carritos IA] Información de
productos #N` (productos cacheados por el bot), `[Comentarios] Productos` y `[Producto Ventas
Wp] N` (catálogos), `[WhatsApp IA] Ventas de productos` / `Facturación` / `Pedidos de hoy`
(métricas del dueño anterior).

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

## El encargo típico: instalarle Chatea a un cliente

El dueño entrega **los datos del negocio y el token del workspace**. Tú devuelves **los 4
asistentes montados, funcionando y adaptados al país**, más **Le'côterra cargado como producto de
ejemplo** en Ventas WhatsApp y en Comentarios (siempre `inactivo`), para que el cliente vea cómo
se configura un producto de ahí en adelante y pueda replicarlo solo.

**Terminado** = los 4 asistentes escritos y releídos del servidor + el producto-ejemplo inactivo
en los dos asistentes + el reporte ANTES→DESPUÉS completo + la **compuerta de verificación del
PASO 3 pasada** (verificador adversarial, no tu propio checklist).

## Dos modos de operación (detéctalo ANTES de preguntar nada)

**MODO A — Workspace nuevo/vacío:** intake completo (PASO 0) y se genera todo desde cero.

**MODO B — Workspace de un cliente YA configurado** (te dan el token de un espacio que el cliente
llenó). Protocolo validado en producción con el primer cliente real (2026-07-09):

1. **LEER TODO primero.** Baja TODOS los Bot Fields por API **paginando hasta `meta.last_page`**
   (son 10 por página y `per_page` se ignora: pedir solo la primera deja fuera la mayoría) y
   clasifícalos ANTES de preguntar nada: el cliente ya respondió muchas preguntas del intake con
   lo que dejó escrito. Preguntar solo lo que falte, sin repetirle lo que ya llenó.
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
3. **Capacidad del campo: hay DOS techos y el orquestador verifica LOS DOS.** Las hijas ven solo
   su parte del JSON; tú ves el campo entero, así que esta verificación es tuya, en cada push.

   **Techo A · el bot field: 20.000 ESCAPADOS, no crudos.** Al ejecutarse, el flujo copia la
   configuración **escapada**: cada tilde ocupa 6 caracteres y cada emoji 12. El techo práctico
   en crudos queda en **~17.000**. Medido (2026-08-07):

   | crudo | escapado | el asistente arranca |
   |---|---|---|
   | 16.882 | 19.895 | sí |
   | 19.922 | 23.266 | **NO** |

   ```python
   escapado = len(json.dumps(valor)[1:-1])   # regla dura: < 19.000
   ```
   ⚠️ **Pasarse NO da error:** la API responde `200 {"status":"ok"}`, guarda el JSON **cortado**
   y el asistente **muere en silencio**. El error solo aparece en Panel → Registros de errores.

   **Techo B · el campo nativo del formulario.** Cada campo del panel tiene su propio tope
   (extraído del código de la app). Escribir por encima por API funciona y no da error, pero el
   día que alguien abra ese formulario y pulse Guardar, **el campo se corta y se pierde el
   texto**. Los más apretados: `respuesta_publica.prompt` 3.000 · `ej_a_eliminar` /
   `ej_a_no_eliminar` 1.000 · `info_extra` 500 · `contacto` / `t_envio` / `datos_req` 200 ·
   `comportamiento_ia.rol` / `restricciones` / `analizar_palabra.prompt` 2.000 ·
   `mensaje_inicial` / `pregunta_de_entrada` / `remarketing.prompt_N` 1.000 ·
   `notificacion.mensaje` 400 · `prompt_libre` 12.000 · `producto_segundos.prompt_datos` 4.000 ·
   descripción de producto en Comentarios 500. Logístico no tiene tope en sus campos de texto.
   **Tabla completa y método de extracción: `TOPES-NATIVOS-POR-CAMPO.md`** en
   `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/` — consúltala antes de escribir, no la reproduzcas de
   memoria.

   Sobre el TIPO de campo: **JSON** = 20.000 · **LONG JSON** = 500.000 (medido 2026-07-25). Crear
   los campos nuevos como LONG JSON da aire para el JSON completo, **pero NO levanta el Techo A**
   (el flujo sigue copiando escapado) **ni el Techo B** (el formulario corta igual). Los campos
   que ya existen como JSON **no se convierten por API**: borrar y recrear cambia el `var_ns` y
   rompe las referencias del flujo. El tipo se cambia en la UI.

   La vara de "cuánta potencia debe tener el prompt" sigue siendo llenar el campo de verdad — pero
   contra el **crudo ~17.000**, nunca contra 19.000 crudos, que es exactamente el rango medido que
   deja el asistente muerto.
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
   **La plataforma acepta SOLO 7 países**, en mayúscula y sin acentos, tal como los escribe el
   campo `[Comentarios IA] País`: **COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU ·
   PARAGUAY**. No hay más: nada de Guatemala, Argentina, Bolivia ni Costa Rica, aunque aparezcan
   en Dropi. Si el cliente opera en uno que no está, dilo antes de empezar — no se puede montar.
   Y lo que cambia por país no es el acento: cambian la división territorial (estado/municipio/
   colonia vs departamento/ciudad/barrio), si el **código postal es obligatorio** (México sí,
   Colombia no), si **existe recogida en oficina** (en México no, todo va a domicilio), la
   zonificación, el regulador y hasta las palabras (paquetería/transportadora, dinero/plata; y
   ojo con *domicilio*: en Colombia es el pedido, en México es la casa). **Un pack de país
   clonado de otro hereda el criterio equivocado**: revísalo campo por campo, no lo asumas.
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

### PASO 3 — COMPUERTA DE VERIFICACIÓN (obligatoria, no la haces tú)

**Nada se declara terminado sin esto.** Tu checklist del PASO 2 lo llenas tú, que construiste —
y quien construye no puede ser quien verifica. Esa fue la causa medida de que esta instalación
fallara seis veces seguidas. Regla del dueño:

1. **Agente `golden-verificador`** (en `~/.claude/agents/`): adversarial e independiente. Recibe
   SOLO el estado final y el estándar que debe cumplir — **nunca cómo lo construiste**. Su trabajo
   es romperlo, no confirmarlo. Devuelve cobertura medida (N de N revisados) y la lista de lo que
   falla o de lo que NO pudo verificar. Nunca dice "está perfecto".
2. **`verificacion_final.py`** — corre los 5 controles sobre la instalación nueva:
   `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/kevin/PLANTILLA-MEXICO/verificacion_final.py`.
3. **Releer del servidor** cada campo escrito y comparar contra lo enviado (longitud cruda,
   longitud escapada y contenido). Es la única prueba real y de paso detecta si alguien pisó el
   cambio desde la UI.

Si el verificador encuentra algo, se arregla y se vuelve a verificar. Se informa **cobertura, no
veredicto**: "N de N campos revisados, esto falla, esto no se pudo verificar" — jamás "quedó
perfecto".

## Reglas de oro del orquestador
- **No hagas el trabajo de las hijas.** Si te descubres escribiendo un prompt de venta o un JSON, párate y llama a la hija.
- **Si falta una skill hija instalada**, dilo con claridad y ofrece el camino: instalarla o configurar ese asistente manualmente. Nunca inventes el contenido de una hija ausente.
- **Datos reales antes de generar:** precio, WhatsApp, cuentas de pago y claims SIEMPRE se preguntan/confirman; nunca se inventan (aplica a todas las hijas).
- **Un workspace, un país.** Si el usuario pide dos países, son dos workspaces y dos corridas de esta skill.
- **En workspaces de cliente (MODO B):** datos de negocio del cliente se respetan; identidad se mejora solo con autorización; el nombre del asesor JAMÁS se cambia sin preguntar.
- **Todo cambio se reporta** asistente → campo → ANTES → DESPUÉS (formato obligatorio del dueño).
- **Prompts siempre por el método cien de cien** (semilla del dueño + lo mejor de lo existente + extender), presentados al dueño antes del push.
- **Cero rastros de Golden** (nombre o dominios) en cualquier workspace de cliente.
- **Los DOS techos se verifican en CADA push** — escapado <19.000 y el tope nativo del campo. Las hijas ven su parte; tú ves el campo entero: esta verificación no la delegas.
- **Solo 7 países.** Si el cliente no está en COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY, se dice antes de empezar.
- **Nada se declara terminado sin la compuerta del PASO 3.** Quien construye no verifica: eso lo hace el agente `golden-verificador`. Se reporta COBERTURA (N de N), nunca "quedó perfecto".
- **Ante la duda sobre un valor raro, compara contra un workspace que funcione** — no contra lo que supones que debería haber.

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
Esto permite armar el workspace COMPLETO por API, sin pegar a mano. El mapa maestro (Bot Fields
clasificados por asistente, con el esquema de claves de cada config) está levantado en
`PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/MAPA-FULL-CONFIGURACION.md` + `extraccion/esquemas/`, y el
briefing operativo completo en `BRIEFING-PARA-SKILLS.md` de esa misma carpeta — **léelo antes de
instalar una cuenta nueva**.

**El censo de campos NO es fijo**: varía por workspace y en el tiempo (se han medido 56, 69, 79 y
82 en distintos espacios y fechas). Cualquier número escrito aquí sería una foto vencida:
**re-extrae paginando y clasifica lo que HAY**, nunca asumas que existen todos (Remarketing puede
no estar según la versión del bot).

Campos de config por asistente: Ventas (`[Ventas Wp] Configuracion general` +2), Logístico
(`[Logistico] Configuracion General` + Confirmaciones + Seguimiento + Novedad), Carritos
(`[Carritos] Configuracion` + Información de productos), Comentarios
(`[Comentarios] Configuracion General` + Productos), Remarketing, Meta pixel, Integraciones.

⚠️ **`[Logistico] Plantillas de mensaje` es un CAMPO MUERTO** (verificado 2026-08-03): contiene
relleno (`"namespace":"string"`). Las plantillas que de verdad trabajan están declaradas DENTRO
de Confirmaciones, Seguimiento y Novedad. No lo leas ni lo escribas: es gastar tokens en un campo
que nadie interpreta.

El pusher genérico vive en `golden-chatea-pro-config-ventas-wp/scripts/push_config.py`
(read → backup → push --confirm por `set-bot-fields-by-name`). Gotchas: token atado a flujo
(sin flujo = 404 "Flow not found"), User-Agent de navegador (Cloudflare 1010), pares
nombre=archivo antes de --confirm. Token = dato sensible: scope mínimo, rotar al terminar.

**Gotchas adicionales (producción, 2026-07-09):**
- `GET /flow/bot-fields` está **PAGINADO: 10 campos por página**. Para leer/respaldar TODO hay
  que recorrer `meta.last_page` (`?page=N`) y unir los `data`. Un backup de una sola página
  pierde ~85% del workspace. (`push_config.py read/backup` consulta por nombre, eso sí trae el
  campo completo; el inventario total requiere paginar.)
- Verificación de escritura: el `PUT` responde 200 con `matched_items`; aún así, relee el campo
  y compara — es la única prueba real (y detecta si alguien pisó tu cambio desde la UI).
- Las plantillas de Meta (namespace propio por cliente) solo se REFERENCIAN por API, no se crean
  ni se aprueban: si una está `PENDING`, se resuelve en Meta, no aquí.
- El `PUT /flow/set-bot-fields-by-name` usa la llave **`data`**: `{"data":[{"name","value"}]}`.
  Con `bot_fields` responde **400**.
- El alta `POST /flow/create-bot-field` usa **`var_type`** (no `type`) y **exige `value`**. Con
  otra llave, **422**.
- El valor se guarda como string con `ensure_ascii=False, separators=(',',':')`. Otro formato
  infla el conteo contra el Techo A sin cambiar el contenido.
- **El trigger no admite caracteres de 4 bytes.** Un emoji lo corrompe y el bot no arranca nunca:
  `[c for c in texto if ord(c) >= 0x10000] == []`.
- **Cada llave conserva su tipo.** `multimedia` escrita como cadena se ve vacía y el panel la deja
  en `[]` al guardar, sin un solo error.
- El producto de Comentarios es un objeto de **5 llaves exactas** (`img`, `name`, `desc`, `rela`,
  `estado`). Con 4 llaves el panel no lo interpreta.
- **Pares `array` / `Extendido`:** los workspaces migrados dejan el campo `array` vacío y los datos
  en el `longtext` `... Extendido`. Verificado en un espacio que vende a diario: `[Ventas Wp]
  Disparador de productos` vacío con 4 productos activos en el Extendido. **Leer el `array` y
  concluir "no hay productos" es un error.** El tipo de un campo existente no se puede cambiar:
  hay que crear uno nuevo.
- **Imágenes:** `multimedia` e `imagen` aceptan URLs externas (CDN de Shopify, probado). Pero el
  `img` del producto de Comentarios usa `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` y
  esas URLs **solo nacen subiendo la imagen en el panel** — no hay endpoint de subida. Copiar la
  URL de una cuenta a otra apunta a la cuenta de origen, no a la propia.
- **Valores por defecto que NO son defectos** (comprobado comparando dos workspaces sanos): las
  instrucciones de recolección vacías, el disparador `array` vacío, `voice_id:
  "English_MaturePartner"` y los eventos de `[Meta]` en cero. **No los "arregles".** El método
  ante la duda es comparar contra un workspace que funcione, no contra lo que uno supone.

## Privacidad (skill compartible con la comunidad)
Esta skill se comparte. Nunca hornees datos de un negocio real (nombres, precios, cuentas de pago, números, tiendas) en sus archivos: se preguntan en cada uso y viven solo en la config entregada. Los ejemplos internos son ficticios.
