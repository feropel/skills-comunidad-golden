---
name: golden-chatea-pro-full-configuracion
description: >-
  Golden Group — ORQUESTADOR MAESTRO de Chatea Pro. Configura de punta a punta TODOS los
  asistentes de un espacio de trabajo (Comentarios, Logístico, Ventas WhatsApp y Carritos)
  llamando a las skills hijas especializadas, y garantiza que queden coherentes entre sí
  (misma voz de marca, mismo país, mismos datos de producto). Úsala SIEMPRE que el usuario
  quiera montar o configurar CHATEA PRO COMPLETO / TODO el bot / TODOS los asistentes de una
  tienda ("configúrame todo chatea pro", "monta el bot completo", "arma todos los
  asistentes", "deja chatea pro listo"), INSTALARLE CHATEA A UN CLIENTE entregando datos del
  negocio y el token de un workspace ("instálale chatea a este cliente", "monta el bot de mi
  cliente", "aquí está el token del espacio"), o arreglar un espacio ya configurado o
  heredado de otra cuenta ("revisa y arregla el chatea de este cliente", "este workspace
  vino con datos de otra tienda").
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 908 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden · Chatea Pro — Full Configuración (orquestador maestro)
<!-- adenda 2026-08-24 (centro de mando, barrido D del arsenal): (1) BASE DE RUTAS declarada — toda ruta relativa PROYECTOS/... de esta skill se resuelve contra la carpeta PROYECTOS del Desktop MASTER de la casa (~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/🌐 PROYECTOS); un chat con otro cwd debe expandirla ahí. (2) Blindaje: la skill se re-blinda con chflags uchg al cerrar cada ronda. -->
<!-- skill v1.5 · 2026-08-28 (verificación ADVERSARIAL con el agente golden-verificador: 54 de 67 requisitos del briefing cubiertos, 16 fallas → reparadas). Regla que confirma esta ronda: quien construye no verifica. Todo lo de abajo lo encontró un tercero que solo vio el estado final. 🔴 F1 "la plataforma acepta SOLO 7 países" era FALSO — el bundle vivo de la app enumera 10 (COLOMBIA, ARGENTINA, BRASIL, CHILE, ECUADOR, GUATEMALA, MEXICO, PANAMA, PARAGUAY, PERU), los tres "prohibidos" con metadata de primera clase: la skill hacía RECHAZAR instalaciones que la plataforma sí soporta, y de paso acusaba a validacion-direcciones de tener un guatemala.md ilegítimo que resultó legítimo. El briefing está desactualizado ahí. 🔴 F7 "vaciar SIEMPRE [Integraciones] Datos de integracion" no estaba acotado al modo: ejecutado en MODO B le borra al cliente sus tokens vivos de Dropi/Shopify/Meta y le tumba el bot, además de destruir la fuente de verdad que la propia skill usa para identificar su tienda — ahora vale SOLO al clonar hacia un espacio nuevo, JAMÁS en producción. 🔴 F2 "el Logístico no tiene tope en sus campos de texto" era FALSO: pago_anticipado.estrategia_persuasion tiene maxLength 2000 + slice(0,2000) — es la clase de truncado silencioso que la skill enseña a temer, y el validador de la casa ya lo sabía y la contradecía. 🔴 F8 la LEY mandaba grep de marca de origen y "si aparece algo NO se escribe", lo que prohibía escribir Le'côterra, que el encargo EXIGE: la excepción de la LEY ahora es también excepción del barrido (--excepcion). 🔴 F9 la skill mandaba correr verificacion_final.py sin argumentos: son 4 controles (no 5) y el de INTERRUPTORES solo corre con --referencia; sin él sale verde sin auditar ni uno. 🔴 F6 la sección de interruptores del briefing estaba en 0 de 2 y el único texto de la skill decía lo contrario ("respeta los booleans") — un prompt perfecto detrás de un evaluar_direccion:"no" no corre; nuevo PASO 2 bis. 🔴 F11 la sección "reinstalar rompe los disparadores" estaba en 0 de 3, incluida la palabra clave que vive en DOS bot fields y no arranca si difieren en un acento (informacion vs información) — que es justo el trabajo de coherencia del maestro. 🟡 F3/F4 topes 12.000 y 4.000 presentados como "extraídos del código" cuando no existen en el bundle (vienen de capturas), y el 500 atribuido a Comentarios cuando es de Ventas; ahora separados en MEDIDOS / NO MEDIDOS / SIN DOCUMENTAR, con los de Comentarios que faltaban (10.000 y 8.000). 🟡 F5 contradicción interna sobre si el tipo de un campo se cambia (UI vs crear nuevo) → regla única. 🟡 F10 tres umbrales para la misma regla: el validador NO falla a 19.000, solo avisa — el corte operativo lo aplica el orquestador. 🟡 F12 el par array/Extendido estaba en su versión ya desmentida (puede estar poblado de los DOS lados). 🟡 F16 el "60% / mínimo 3 órdenes" era cifra sin fuente y chocaba con feedback_efectividad_sin_umbral. 🟡 F14 el frontmatter no parseaba con YAML estándar (comentario HTML dentro del bloque --- y ": " en un escalar sin comillas) — 7 de 91 skills de la casa comparten el defecto. Añadido además el puente Dropi→Chatea (ficha de operación: novedades reales reescriben el prompt de captura; nunca el export crudo en un bot field) y declarados 3 pendientes con dueño del entregable (img del producto-ejemplo imposible solo por API, valor literal de estado inactivo, orden vaciar/cargar). PENDIENTES DE FUENTE, no de esta skill: TOPES-NATIVOS-POR-CAMPO.md arrastra F2 y F3, y BRIEFING-PARA-SKILLS.md arrastra F1 — hay que remedirlos, y las 6 hermanas que copiaron esa tabla también. -->
<!-- skill v1.4.1 · 2026-08-24 (centro de mando): bump por las adendas del 24 (base de rutas + blindaje) que quedaron sin subir versión. -->

<!-- skill v1.4 · 2026-08-23 (auditoría golden-skill-auditor 804/1000 BRONCE → reparada) · alineación con el BRIEFING-PARA-SKILLS del 2026-08-07, que la skill no había absorbido. 🔴 CRÍTICO 1: el método cien de cien mandaba llenar "al 90-95%, ~18000-19000 crudos" — el techo real son 20.000 ESCAPADOS (~17.000 crudos, tilde=6 chars, emoji=12) y está MEDIDO que 19.922 crudos = 23.266 escapados = el asistente NO arranca, con la API respondiendo 200 ok y guardando cortado: la skill instruía exactamente el rango que mata la instalación. Reescrito como DOS TECHOS con tabla medida y la fórmula len(json.dumps(v)[1:-1]) < 19.000. 🔴 CRÍTICO 2: faltaba por completo el Techo B (tope NATIVO de cada campo del formulario, extraído del código de la app) — escribir por encima funciona por API pero el panel corta el texto al guardar; añadidos los topes más apretados + puntero a TOPES-NATIVOS-POR-CAMPO.md. 🔴 CRÍTICO 3: la definición de terminado era un checklist que llenaba quien construyó — la causa medida de seis fallas seguidas; nuevo PASO 3 COMPUERTA DE VERIFICACIÓN con el agente golden-verificador (adversarial, recibe solo el estado final), verificacion_final.py y relectura del servidor, reportando COBERTURA y nunca "quedó perfecto". 🔴 CRÍTICO 4: mandaba configurar [Logistico] Plantillas de mensaje, campo MUERTO (relleno "namespace":"string"; las plantillas reales viven dentro de Confirmaciones/Seguimiento/Novedad). 🔴 CRÍTICO 5: afirmaba un censo fijo de campos ("los 79", "~69-79") ya falso tres veces (56/69/79/82 según espacio y fecha) — reemplazado por "re-extrae paginando y clasifica lo que HAY". Añadidos: los 7 países que acepta la plataforma con lo que cambia de verdad entre ellos (código postal obligatorio en México, sin recogida en oficina, domicilio=casa) y la advertencia de que un pack clonado hereda el criterio equivocado; Le'côterra siempre inactivo (enseña, no vende); el encargo típico de instalación a cliente con su definición de terminado; la fuga menos obvia al clonar (nombres de producto y paquetería DENTRO de los ganchos de venta del logístico) y la lista de campos a vaciar; gotchas de API (llave data si no 400, create-bot-field con var_type+value si no 422, paginación con per_page ignorado, ensure_ascii/separators, trigger sin caracteres de 4 bytes, cada llave conserva su tipo, producto de Comentarios de 5 llaves exactas, pares array/Extendido donde array vacío NO significa sin productos, img de Comentarios que solo nace subiendo en el panel); valores por defecto que NO son defectos (comparar contra un workspace que funcione, no contra lo que uno supone); description ampliada al disparo real (instalar a un cliente con token, arreglar un espacio heredado). -->
<!-- skill v1.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
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
no vio. Ese `grep` es exactamente el flag `--marca` de la herramienta:
```bash
python3 "PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py" <archivo.json> \
  --marca "<marca de origen>" --excepcion "Le'côterra"
```

⚠️ **El producto-ejemplo autorizado NO cuenta como hallazgo.** Sin `--excepcion`, el barrido
marca Le'côterra como marca ajena y, aplicando "si aparece algo NO se escribe" al pie de la
letra, la LEY prohibiría escribir el producto que el encargo típico EXIGE dejar. La excepción de
la LEY de herencia es también excepción del barrido: decláraselo a la herramienta.

**La fuga menos obvia: los nombres de PRODUCTO y de PAQUETERÍA dentro de los ganchos de venta del
logístico.** No son configuración, son ejemplos — y la IA imita el ejemplo: con un producto ajeno
adentro escribe frases que venden lo que el cliente no vende. En una cuenta heredada aparecieron
transportadoras colombianas y la marca del profesor dentro del workspace de un alumno. Al barrer,
mira también los ganchos por estado (guía generada, en reparto, en oficina, entregado).

**Vaciar al CLONAR desde una cuenta guía hacia un espacio nuevo** — y SOLO en ese caso:
`[Integraciones] Datos de integracion` (llaves de Dropi, Shopify, OpenAI, Meta y Maps en texto
plano), `[Carritos IA] Información de productos #N` (productos cacheados por el bot),
`[Comentarios] Productos` y `[Producto Ventas Wp] N` (catálogos), `[WhatsApp IA] Ventas de
productos` / `Facturación` / `Pedidos de hoy` (métricas del dueño anterior).

🔴 **JAMÁS en MODO B.** En un workspace que ya es del cliente y está en producción, esos campos
son SUYOS: `[Integraciones] Datos de integracion` es además la fuente de verdad para identificar
su tienda real (MODO B punto 3). Vaciarlo le tumba el bot y le borra sus tokens vivos de Dropi,
Shopify y Meta CAPI. En MODO B no se vacía nada: se DIAGNOSTICA y se corrige con autorización.
La regla de vaciado existe para el material que viaja DESDE una cuenta guía, no para lo que ya
vive en el destino.

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

**Tres cabos sueltos de este entregable — pendientes con el dueño, no los improvises:**
1. **El `img` del producto-ejemplo en Comentarios NO se puede cargar solo por API.** Esas URLs
   (`media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...`) solo nacen subiendo la imagen en el
   panel, y copiar la de otra cuenta apunta a la cuenta de origen. O se sube a mano en el panel
   del cliente, o se decide qué va en `img`. Declara este paso manual al entregar.
2. **El valor literal de `estado` para "inactivo" no está confirmado** (`"inactivo"` / `"no"` /
   `false`). Léelo de un workspace que ya tenga el producto-ejemplo cargado antes de escribirlo.
3. **Orden entre vaciar catálogos y cargar el producto-ejemplo:** primero se vacía (solo al
   clonar, ver la LEY), y el producto-ejemplo se carga DESPUÉS. Al revés se borra lo que acabas
   de poner.

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

   **Techo B · el campo nativo del formulario.** Cada campo del panel tiene su propio tope.
   Escribir por encima por API funciona y no da error, pero el día que alguien abra ese
   formulario y pulse Guardar, **el campo se corta y se pierde el texto**.

   **MEDIDOS en el código vivo de la app** (`maxLength`, notación minificada `2e3`=2.000,
   `1e4`=10.000 — un regex que no la contemple reporta "sin tope" en falso):
   Comentarios → `comentarios_negativos.prompt_general` 10.000 · `venta_conversacional.prompt`
   8.000 · `respuesta_publica.prompt` 3.000 · `ej_a_eliminar` / `ej_a_no_eliminar` 1.000 ·
   `info_extra` 500 · `contacto` / `t_envio` / `datos_req` 200.
   Ventas (`Configuracion general 2`) → `comportamiento_ia.rol` / `restricciones` /
   `analizar_palabra.prompt` 2.000 c/u · descripción del producto 500 · `mensaje_inicial` /
   `pregunta_de_entrada` / `remarketing.prompt_N` 1.000 · `notificacion.mensaje` 400.
   Logístico → `pago_anticipado.estrategia_persuasion` **2.000** (`maxLength` + un
   `slice(0,2000)` en `onChange`).
   ⚠️ **"El Logístico no tiene tope" es FALSO** — lo decía una versión anterior de esta skill y lo
   sigue diciendo `TOPES-NATIVOS-POR-CAMPO.md`. El validador de la casa ya lo tiene bien.

   **NO medidos en código, vienen de capturas de pantalla** (trátalos como orientativos, no como
   verdad): `prompt_libre` 12.000 · `producto_segundos.prompt_datos` 4.000. No hay ningún
   `maxLength` de esos valores en el bundle.

   **Sin documentar todavía:** Carritos (el briefing dice "solo los de correo"; `CartsPage` no
   tiene ningún `maxLength`, así que viven en un módulo compartido sin localizar) y varios topes
   sueltos de Ventas medidos pero sin mapear a su campo (300 ×6, 800 ×2, 1.500).

   `TOPES-NATIVOS-POR-CAMPO.md` en `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/` tiene la tabla
   completa, **pero arrastra los dos errores de arriba**: consúltala sabiéndolo, y ante un campo
   crítico remídelo contra el bundle en vez de creerle a la tabla.

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

## Ficha de operación: afinar la config con datos reales (opcional, alto impacto)

Toda la configuración de arriba se escribe por **criterio de país**. Cuando el cliente ya tiene
historia en Dropi, esa historia dice **qué se rompe de verdad en SU operación** — y eso vale más
que cualquier convención. El ciclo que casi nadie cierra: *lo que falla en la entrega debería
reescribir lo que el bot pregunta en el chat.*

**Cómo entra el dato (y cómo NO).** El export de Dropi **jamás** se pega en un bot field: se come
el techo de ~17.000 crudos en dos días, los bot fields son configuración estable y no un feed, y
metería datos de clientes reales en un campo que cualquiera con el token lee. El camino correcto
es **Dropi → `golden-dropi-analisis` → ficha de media página → unas pocas líneas en los prompts**.
Lo que viaja a Chatea son **reglas derivadas**, nunca filas de datos.

Qué sacar de la ficha y a qué campo va:

| Dato de la operación | Qué afina | Dónde |
|---|---|---|
| **Novedades más frecuentes** | el prompt de captura se endurece EXACTAMENTE donde falla (si la #1 es dirección incompleta, ese campo se vuelve obligatorio y explícito; si es "no contaba con dinero", se confirma el total antes de cerrar) | Logístico `analisis_direccion.prompt_analisis` + captura de datos de Ventas |
| **Efectividad por ciudad/depto** | trato diferenciado: donde la entrega es mala, más detalle de dirección, empujar anticipado, o punto de oficina donde exista | Logístico + Ventas |
| **Mix real de cantidades** | valida si el anclaje funciona. Si todos caen en 1 unidad, el anclaje a 2-3 no está sirviendo y se cambia — se mide, no se adivina | prompt de venta del producto |
| **Corte real de efectividad del cliente** | el umbral que traiga el workspace es un valor heredado, no una verdad: el dato propio dice dónde está el corte real. Ley de la casa (`feedback_efectividad_sin_umbral`): si hay 1 envío, ese es el dato — se muestra SIEMPRE la muestra y la fuente, no un porcentaje pelado | `validaciones_orden` de Ventas, Logístico y Remarketing (los tres coherentes) |
| **Tasa de entrega por producto** | qué producto devuelve más y merece filtro más duro o solo anticipado | por producto |

**Reglas de esta ficha:**
- Es **por cliente y regenerable** (mensual). La ficha de un negocio NO toca el workspace de otro:
  es la misma LEY de no heredar datos.
- Va como **conocimiento derivado**, nunca como export crudo: cero teléfonos, cero nombres de
  clientes, cero direcciones. Solo agregados y las reglas que salen de ellos.
- Si el cliente **no tiene historia todavía**, se configura por criterio de país y se anota como
  pendiente revisar a los 30 días con dato propio. No se inventan porcentajes.

## Flujo de orquestación

### PASO 0 — Encuadre del espacio de trabajo (pregunta 1 a la vez)
1. **Negocio / tienda** que se va a configurar.
2. **País del workspace** (recuerda: 1 workspace = 1 país). Este dato manda sobre todas las hijas.
   **La plataforma acepta 10 países** (medido 2026-08-28 contra el bundle vivo de la app,
   `instalacion-asistentes.chateapro.app/assets/index-*.js`, constante de países): **COLOMBIA ·
   ARGENTINA · BRASIL · CHILE · ECUADOR · GUATEMALA · MEXICO · PANAMA · PARAGUAY · PERU**, en
   mayúscula y sin acentos. Los 10 tienen metadata de primera clase (indicativo, dígitos del
   celular, moneda). ⚠️ Una versión anterior de esta skill decía "solo 7" y excluía Argentina,
   Brasil y Guatemala: era FALSO y hacía rechazar instalaciones que la plataforma sí soporta.
   **Este número es una foto fechada: remídelo contra el bundle antes de rechazar a un cliente
   por su país**, nunca lo afirmes de memoria.
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

### PASO 2 bis — INTERRUPTORES y DISPARADORES (lo que más se rompe en silencio)

**Un prompt perfecto detrás de un interruptor apagado no hace nada.** Caso medido: un prompt de
validación de direcciones de 7.243 caracteres, correcto y cargado, con
`analisis_direccion.evaluar_direccion = "no"`. Nunca corrió, y nada avisó.

1. **Audita TODOS los interruptores contra un workspace que funcione**, no solo los textos:
   `activar`, `esta_activo`, `habilitar`, `evaluar_*`. Esto NO contradice la regla de respetar los
   datos del cliente en MODO B: se respetan sus VALORES de negocio (fletes, porcentajes, tiempos);
   un interruptor apagado que deja muerto un prompt que acabas de escribir es un HALLAZGO, se
   reporta y se enciende con autorización.
2. **`voz_con_ia` de cada producto:** puede venir con una `api_key` de ElevenLabs de la cuenta de
   origen y `habilitar: "si"`. Es la credencial exacta que ya se filtró una vez. Revísalo por
   producto, no por asistente.
3. **La palabra clave vive en DOS sitios y deben coincidir byte a byte:**
   `[Producto Ventas Wp] N.activadores_del_flujo.palabras_clave` y la entrada del producto en
   `[Ventas Wp] Disparador de productos Extendido`. **Si difieren en un solo acento, el producto
   no arranca** (caso real: `informacion` contra `información`). Compáralas byte a byte — esto es
   coherencia entre dos bot fields, o sea trabajo del maestro, no de una hija.
4. **Reinstalar un asistente rompe sus disparadores:** recrea los subflujos con `ns` nuevo y deja
   el disparador apuntando al viejo. Hay que reenlazarlos a mano, y se vuelve a romper en CADA
   reinstalación. Si reinstalas, reenlazar y volver a verificar es parte del trabajo.

### PASO 3 — COMPUERTA DE VERIFICACIÓN (obligatoria, no la haces tú)

**Nada se declara terminado sin esto.** Tu checklist del PASO 2 lo llenas tú, que construiste —
y quien construye no puede ser quien verifica. Esa fue la causa medida de que esta instalación
fallara seis veces seguidas. Regla del dueño:

1. **Agente `golden-verificador`** (en `~/.claude/agents/`): adversarial e independiente. Recibe
   SOLO el estado final y el estándar que debe cumplir — **nunca cómo lo construiste**. Su trabajo
   es romperlo, no confirmarlo. Devuelve cobertura medida (N de N revisados) y la lista de lo que
   falla o de lo que NO pudo verificar. Nunca dice "está perfecto".
2. **`verificacion_final.py`** — son **4 controles** (techos · topes nativos · contaminación ·
   interruptores), y el 4º **solo corre si le pasas `--referencia`**. Sin ese flag imprime
   `Interruptores comparados: NO (sin referencia)` y sale en verde sin auditar un solo
   interruptor: sería pasar la compuerta con el validador castrado. Invocación completa:
   ```bash
   python3 "PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/kevin/PLANTILLA-MEXICO/verificacion_final.py" \
     --token "<token del cliente>" \
     --referencia "<token de un workspace que YA funcione>" \
     --excepcion "Le'côterra"
   ```
   `--excepcion` evita que el producto-ejemplo autorizado se marque como contaminación.
   `--autoprueba` corre su banco de casos malos (úsalo si dudas del validador).
   ⚠️ **El validador NO falla a 19.000 escapados**: a partir de 19.000 avisa y solo falla en
   20.000. La regla de la casa es más estricta que la herramienta — **el corte operativo es
   <19.000 y lo aplicas tú**, no lo delegues en el verde del script.
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
  concluir "no hay productos" es un error.** Pero **NO lo generalices al revés**: el par puede
  estar poblado de LOS DOS lados (medido: `[Comentarios] Productos` con 6.980 caracteres Y su
  Extendido con 7 productos). **Mira siempre los dos campos.** Sobre cambiar el tipo de un campo
  existente, la regla única está en el método cien de cien: por API no se convierte (borrar y
  recrear cambia el `var_ns` y rompe el flujo) — se cambia en la UI.
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

## Fronteras y desambiguacion

Si solo quiere UN asistente puntual (solo comentarios, solo logístico, solo ventas, solo carritos), esta skill lo deriva a la hija que corresponde. NO genera ella misma los JSON ni los prompts, dirige, ordena y audita a las skills hijas.'
