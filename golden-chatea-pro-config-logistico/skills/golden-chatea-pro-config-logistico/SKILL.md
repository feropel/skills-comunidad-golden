---
name: golden-chatea-pro-config-logistico
description: >-
  Golden Group — Configura el asistente LOGÍSTICO de Chatea Pro (el PADRE). Deja listo el
  asistente que valida la dirección del cliente antes del envío contra entrega (COD) para
  minimizar devoluciones: define los datos operativos del negocio (transportadoras
  habilitadas para domicilio y recogida en oficina, transportadoras prohibidas, tiempos de
  entrega por zona) y arma el prompt de validación llamando a su skill HIJA
  golden-chatea-pro-validacion-direcciones (packs por país vía su hija — la plataforma
  acepta 10 países, hay packs para 8; Argentina y Brasil sin pack aún). Úsala SIEMPRE que el
  usuario quiera montar o configurar el asistente logístico / de direcciones de Chatea Pro,
  "configurar logística de chatea pro", "el bot que revisa direcciones antes de despachar",
  "el bot valida mal las direcciones", "configura las transportadoras del bot", "arma el
  asistente que evita devoluciones", o dejar listo el asistente logístico completo.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 944 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden · Chatea Pro — Asistente Logístico (padre)

<!-- Fábrica: CENTRO DE MANDO (chat 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR) — sin fábrica de chat propia; turnos y filas van a la bandeja del CdM. -->
<!-- corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto. -->
<!-- skill v1.6 · 2026-08-26 (CdM, edición de familia por la LLAVE DEL INTAKE respondida por FER) ·
PASO 0 vuelve a UNA PREGUNTA A LA VEZ: la v1.5 lo había pasado a "intake único en un solo turno"
siguiendo estandares-golden §3, pero FER resolvió hoy la contradicción en la fábrica de
prompt-ventas ("mejor uno por uno, porque en bloque se abruma la gente") y la nota de gobierno del
barrido pre-comprometía revertir esta skill JUNTO con prompt-ventas (mismo criterio de reversion, sin fijar version — una cita con numero caduca sola:
bloque solo si el interlocutor pega varios datos o lo pide). Lo que se conserva del §3: el
conjunto se releva AL INICIO y nada ya dado se re-pregunta. Fila entregada a la fábrica del
auditor para alinear el §3 y que el próximo barrido no lo devuelva al formulario. -->
<!-- skill v1.5 · 2026-08-24 (barrido total del arsenal, CdM): el PASO 0 decía "pregunta 1 a la vez" — goteo que contradice la ley de autonomía Golden (estandares-golden §3: los datos que solo el dueño tiene se piden UNA vez, al inicio, nunca goteados; cada repregunta es una fuga de turnos). Ahora el intake se pide completo en un solo turno. Los 6 datos, los techos (incl. adenda LONG JSON de dos niveles), gotchas de API, la LEY de no heredar datos y el resto quedan intactos. -->
<!-- skill v1.4 · 2026-08-23 (Estándar 9 — Conexión con el Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
<!-- skill v1.3 · 2026-08-21 (auditoría golden-skill-auditor) — description con más sinónimos/frases reales de disparo y desambiguación explícita de la hija (se activa sola, no hace falta llamarla aparte); PASO 1 con manejo de error si la hija golden-chatea-pro-validacion-direcciones no está instalada o no tiene el pack del país (nunca inventar el prompt a mano, declarar pendiente con motivo); PASO 2 con checklist explícito de "terminado" (país, transportadoras, tiempos, prompt de la hija, escribir-releer si aplica, barrido si el origen fue una cuenta guía). -->
<!-- skill v1.2.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): completada la ley de DOS NIVELES del techo — el tope de 20.000 escapados aplica al bot field tipo JSON legacy; un campo creado o convertido a LONG JSON aguanta hasta 500.000 (medido y validado en las hermanas config-comentarios v1.4.1 y config-ventas-wp v3.0). La cifra de esta skill era incompleta, no falsa: sin la mención a LONG JSON, quien la siga se autolimita. -->
<!-- skill v1.2 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v1.1 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat CONFIG CHATEA KEVIN MX): países corregidos a los 7 que acepta la plataforma (sale Guatemala, entran Panamá/Perú/Paraguay); sección de techos (logístico SIN tope nativo — manda el bot field: 20.000 ESCAPADOS, ~17.000 crudos); gotchas de API (PUT usa `data`, POST usa `var_type`+`value`, GET pagina, trigger sin emojis, tipos por llave, escribir y RELEER); higiene al clonar (los ganchos de venta del logístico fugan nombres de producto y paquetería de la cuenta origen). -->
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

Configura el **asistente logístico** de un espacio de trabajo de Chatea Pro. Su misión: **validar la dirección del cliente antes del despacho COD** para minimizar devoluciones y reprocesos de última milla.

Tiene dos niveles:
1. **Config del asistente (esta skill, el padre):** los datos operativos del negocio — transportadoras habilitadas, recogida en oficina, transportadoras prohibidas, tiempos de entrega por zona.
2. **El prompt de validación (la skill hija):** el cerebro que lee la dirección y decide si es entregable. Lo genera `golden-chatea-pro-validacion-direcciones`.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. Este asistente se configura con el país del workspace.
> **La plataforma acepta 10 (remedido 2026-08-29) países** (campo `[Comentarios IA] País`, en MAYÚSCULA y sin acentos): COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY. Nada de Guatemala, Argentina, Bolivia ni Costa Rica.

## Los dos techos (antes de escribir cualquier campo)

- **Techo A — el bot field: 20.000 ESCAPADOS, no crudos.** Al ejecutarse, el flujo copia la configuración escapada: cada tilde ocupa 6 caracteres y cada emoji 12. El techo práctico en crudos queda en ~17.000. Pasarse NO da error: la API responde `200 ok`, guarda el JSON cortado y el asistente muere en silencio (el error solo aparece en Panel → Registros de errores). Medir siempre: `escapado = len(json.dumps(valor)[1:-1])` y que quede bajo 19.000. **Nivel B — LONG JSON:** el tope de 20.000 es del campo tipo JSON legacy; si el bot field se crea o convierte a **LONG JSON**, el techo sube a 500.000 escapados (ley de dos niveles medida en las hermanas config-comentarios y config-ventas-wp). Con configuraciones grandes, convertir el campo a LONG JSON antes de escribir.
- **Techo B — el campo nativo: el logístico NO tiene tope** en sus campos de texto (Adaptación del lenguaje, Método para evitar la cancelación, Políticas de garantía, Restricciones). Los únicos `maxLength` de su formulario son numéricos (días/horas). Aquí manda únicamente el Techo A. Fuente: `TOPES-NATIVOS-POR-CAMPO.md` de CHATEA-PRO-ASISTENTES-MAPA (extraído del código de la app, 2026-08-07).

## Gotchas de API (si la config se escribe por API)

- `PUT /flow/set-bot-fields-by-name` usa la llave **`data`**: `{"data":[{"name","value"}]}`. Con `bot_fields` responde 400.
- `POST /flow/create-bot-field` usa **`var_type`** (no `type`) y **exige `value`**. Con otra llave, 422.
- `GET /flow/bot-fields` **PAGINA** y `per_page` se ignora: recorrer todas las páginas antes de concluir que un campo no existe.
- El valor se guarda como string con `ensure_ascii=False, separators=(',',':')`; otro formato infla el conteo contra el techo sin cambiar el contenido.
- **El trigger no admite caracteres de 4 bytes:** un emoji lo corrompe y el bot no arranca nunca. Validar: `[c for c in texto if ord(c) >= 0x10000] == []`.
- **Cada llave conserva su tipo:** un array escrito como cadena se ve vacío y el panel lo deja en `[]` al guardar, sin error.
- **Escribir y RELEER siempre:** comparar el valor guardado contra el enviado es la única prueba real.

## Flujo de configuración

### PASO 0 — Intake operativo del negocio (UNA PREGUNTA A LA VEZ — decisión de FER 2026-08-26 — y no inventes nada)
Releva los 6 datos AL INICIO, conversacionalmente, **una pregunta a la vez** ("en bloque se
abruma la gente" — FER). El bloque completo de una sola vez es la EXCEPCIÓN: solo cuando el
interlocutor ya pegó varios datos juntos (reconócelos todos y pregunta solo lo que falte) o
pida expresamente que se le mande todo de una. Lo que NO cambia: el conjunto se releva al
inicio y un dato ya dado JAMÁS se re-pregunta después.
1. **País** del workspace.
2. **Transportadoras habilitadas** para **domicilio** (las que el negocio realmente tiene contratadas).
3. Si ofrece **recogida en oficina** y con qué transportadoras.
4. **Transportadoras prohibidas** (ej. en Colombia, muchos negocios no usan Servientrega).
5. **Tiempos de entrega por zona** (capital 2-3 días, intermedia 3-4, rural 5-7) — dato compartido con Ventas y Carritos.
6. Si conserva los emojis de estado (✅/⚠️) en las respuestas.

### PASO 1 — Generar el prompt de validación (delega en la hija)
Con los datos del intake, **invoca `golden-chatea-pro-validacion-direcciones`** pasándole el país y las transportadoras confirmadas. La hija carga el pack del país (Colombia = patrón oro) y devuelve el prompt de validación con:
- Contrato de salida en **una sola línea** (`dirección correcta` / `Para completar su envío, nos regala [dato]?`).
- Interpretación de nomenclatura local, vivienda colectiva, rural y GPS.
- Principio rector: si un mensajero puede llegar sin llamar → válida; si hay riesgo de devolución → falta info.

**Si la hija no está instalada o no devuelve el pack del país pedido:** no inventes el prompt de validación a mano — es exactamente el trabajo que existe para no reinventarse en prosa cada vez. Informa al usuario que falta `golden-chatea-pro-validacion-direcciones`, entrega igual el resumen operativo del PASO 2 (transportadoras/tiempos, que sí es de esta skill) y deja pendiente explícito el prompt de validación con el motivo exacto (skill hija ausente / país sin pack todavía).

### PASO 2 — Entregar
Entrega al usuario: (a) el resumen de la config operativa (transportadoras/tiempos), y (b) el prompt de validación listo para pegar en el campo del asistente logístico de Chatea Pro.

**Definición de terminado (checklist):**
- [ ] País confirmado y es uno de los 7 que acepta la plataforma.
- [ ] Transportadoras de domicilio, recogida en oficina y prohibidas confirmadas con el negocio (ninguna inventada).
- [ ] Tiempos de entrega por zona confirmados y coherentes con Ventas y Carritos.
- [ ] Prompt de validación recibido de la hija (o, si no, el pendiente queda declarado con motivo — ver PASO 1).
- [ ] Si la config se escribe por API: valor escrito releído del servidor y comparado contra el enviado (ver "Escribir y RELEER siempre").
- [ ] Barrido de datos ajenos corrido si el origen fue una cuenta guía o un espacio distinto al del cliente final.

## Reglas de oro
- **Nunca inventes transportadoras ni tiempos:** se preguntan/confirman por negocio y país.
- **Vocabulario por país:** en Colombia se dice transportadora, domicilio (= el pedido), plata, mensajero; en México paquetería, pedido, dinero, repartidor. Ojo con **domicilio**: en Colombia es el pedido, en México es la casa — "para recibir tu domicilio" no se entiende en México.
- **Al clonar a otro cliente, los ganchos de venta del logístico fugan datos:** nombres de producto y de paquetería dentro de los ejemplos son texto que la IA imita (en una cuenta heredada aparecieron transportadoras colombianas y la marca del profesor en el workspace de un alumno). Parametrizar siempre, nunca quemar: nombre de la tienda, URL, nombre de la asesora, WhatsApp, tiempos de entrega y políticas de garantía.
- **Ante la duda, comparar contra un workspace que funcione** (Golden vende a diario), no contra lo que uno supone que debería haber: hay defaults que no son defectos.
- **No reimplementes la validación:** el prompt lo hace la hija `golden-chatea-pro-validacion-direcciones`. Este padre solo aporta los datos operativos y coordina.
- **Tiempos de entrega coherentes** con Ventas (`golden-chatea-pro-config-ventas-wp`) y Carritos (`golden-chatea-pro-config-carritos`).

## Conexiones (skills hermanas)
- 🧭 Hijo — prompt de validación de direcciones → `golden-chatea-pro-validacion-direcciones`
- 🛒 Asistente de ventas (dispara el logístico al pedir la dirección) → `golden-chatea-pro-config-ventas-wp`
- 🔁 Asistente de carritos (mismos tiempos de entrega) → `golden-chatea-pro-config-carritos`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales (transportadoras contratadas, tienda, cuentas) en los archivos de la skill. Se preguntan en cada uso.

## Fronteras y desambiguacion

Para configurar TODOS los asistentes a la vez, usa golden-chatea-pro-full-configuracion; para el prompt de validación en sí (el cerebro que decide si la dirección es entregable), la skill hija golden-chatea-pro-validacion-direcciones se activa sola desde aquí — no hace falta llamarla aparte.
