---
name: golden-chatea-pro-config-ventas-wp
description: >-
  Golden Group — Configura el asistente de VENTAS POR WHATSAPP de Chatea Pro (la "Experta en
  ventas por WhatsApp", el bot o agente de ventas) con los Bot Fields JSON nativos listos para
  pegar: 2 campos de configuración general (Dropi, validaciones
  de orden, Producto en Segundos con prompt maestro, notificaciones, comportamiento de la
  IA), 1 campo por producto ([Producto Ventas Wp] N) y su entrada en el Disparador de
  productos Extendido, con los prompts del motor afinados, parametrización por país (el país es
  parámetro, no puerta: sin pack se configura igual) y validadores de los DOS techos reales. Úsala SIEMPRE que quiera montar,
  configurar o replicar el asistente, agente o bot de ventas de WhatsApp de Chatea Pro, "configurar ventas whatsapp", "montar el
  asistente de ventas", "el JSON del asistente de ventas", "genera los bot fields de
  ventas", "configura la experta en ventas", o cargar y validar un producto nuevo en ese
  asistente.
---

**Fábrica:** chat «✅ SKILL golden-chatea-pro-config-ventas-wp»
# Golden · Chatea Pro — Asistente de Ventas WhatsApp

## 📋 Requisitos: qué necesita del usuario antes de arrancar

- **Token API del espacio de Chatea Pro** · BLOQUEANTE, atado al Bot (*Settings → API Keys*). 🔴 **`push_config.py` lo toma de `--token`, de `CHATEAPRO_TOKEN` o, si no hay ninguno, del archivo `~/.chatea_pro_token`, SIN avisar ni comprobar a qué espacio escribe**, y ningún script de la skill muestra hoy la tienda del token. Por eso el token se exporta en `CHATEAPRO_TOKEN` **desde el `.secrets/` de la carpeta de ESE cliente**, y si hay cualquier duda de a qué espacio pertenece, **no se hace el push**. Nunca `--token <valor>` en el comando. La comprobación automática está pedida a la fábrica (bandeja del CdM, 27-sep, fila 1).
- **Argumentos de `build_config.py`** · BLOQUEANTES (el script los exige): `--pais`, `--url-tienda`, `--nombre-bot`, `--nombre-tienda` y `--modelo`, más el **prompt maestro**.
- **`--flete-max`** · BLOQUEANTE fuera de Colombia cuando se despacha por Dropi: `--dropi` vale "si" por defecto y el script solo trae el tope de Colombia (sin Dropi, `--dropi no`).
- **WhatsApp de notificaciones** (`--whatsapp-notif`) · DEGRADABLE: es opcional en el script.
- **Correo y contraseña del espacio** (dato 6 del intake del cliente) · DEGRADABLE: el trabajo por API va con el token. Nunca se guardan en un `.md`.
- Esta skill **no monta productos** (eso es `golden-chatea-pro-prompt-ventas`) ni escribe el token de proveedor de Dropi, que vive en `[Integraciones]`.

**Si falta algo BLOQUEANTE: no se hace lo que depende de él** (si es de toda la skill, se PARA antes de tocar nada) y se pide con nombre propio: qué es, dónde se saca y dónde se pone. **Si falta algo DEGRADABLE: se pide y se sigue**, dejando marcado como pendiente en todo lo que depende de él. Nunca se presenta como completo.

<!-- skill v4.18.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v4.18 — 2026-09-27 — CdM: bloque de REQUISITOS al principio (ley de FER del 02-sep). -->
<!-- skill v4.17 — 2026-09-22 — el Centro de Mando reverifico v4.16 en vivo (espacio de Golden, servidor) y pregunto por el doble negativo de "[WhatsApp IA] Desactivar consulta de recordatorios" antes de que alguien lo invirtiera dos veces: el valor false esta CORRECTO (confirmado contra el servidor, no de memoria) y se le sumo la nota _trampa_doble_negativo en campos-sueltos.json para el siguiente lector. Antes, v4.16 — 2026-09-22 — auditoría golden-skill-auditor (AUDITA+ARREGLA, pedido de FER "que se automejore y llegue a mil"): 890→ver acta, 5 hallazgos reparados (Argentina/Brasil caducado en 3 archivos, push_config comparaba texto crudo en vez de JSON parseado, detector de fuga de vocabulario solo conocía Colombia, chequeo de signos de apertura no cubría remarketing/upsells, "18" mal corregido a "16" y vuelto a corregir con precisión). Además: retirado el puntero a golden-chatea-pro-config-remarketing (orden de FER vía Centro de Mando — la skill se borró del arsenal; el campo Producto Remarketing de ESTA skill no se tocó, es de otro dueño). Antes, v4.15 — 2026-09-21 — el Centro de Mando reverificó v4.14 con sus propios sabotajes (7 de 7 detectados) y midió un pulido: borrar un país entero reventaba con KeyError en vez de fallar limpio. Corregido con un roster de países ANCLADO por nombre (PAISES_MAPA) que se compara antes de indexar. Con esto el CdM dio cerrada la extensión de vocabulario. Antes, v4.14 — 2026-09-21 — el Centro de Mando midió TRES puntos ciegos del banco de vocabulario (campo alterado con la cita intacta, aclaración alterada, origen borrado, los tres 100% verdes antes) y se corrigieron: contenido validado contra el PACK COMPLETO, origen de un conjunto cerrado, total anclado. Antes, v4.13 — 2026-09-20 — MAPA DE VOCABULARIO DE DIRECCIÓN de 23 países copiado de los packs (autorizado por el Centro de Mando) + ley de credenciales en el dato 6. Antes, v4.12 — 2026-09-19 — INTAKE AL CLIENTE Y FLETE (estándar de FER, vía Centro de Mando): intake de siete datos, WhatsApp de último y tras el pago, correo/contraseña del espacio como ACCESO no como campo. Historial completo en references/changelog.md. Auditoría golden-skill-auditor 2026-09-20: agregada esta línea de versión bajo el H1, que faltaba; sin otros hallazgos con evidencia (los 2 DUDOSOS de inventario.sh son falsos positivos — concatenación de string Python `S + "/scripts/..."` en autoprueba_d1.py, ambos archivos están citados en el cuerpo). Cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO. -->

**⚠️ Gotcha D1 — palabras clave son BYTE A BYTE con el Disparador (incidente de campo del 2026-08-23 en un espacio VIP):**
cualquier edición de texto sobre un campo que contenga `activadores_del_flujo.palabras_clave`
(quitar signos, tildes, mayúsculas, un espacio) rompe la coincidencia exacta con el Disparador de
productos Extendido y el producto DEJA DE ARRANCAR en silencio. Regla: todo barrido o edición
genérica de texto EXCLUYE ese subcampo, o se verifica D1 (palabra clave == entrada del Disparador,
byte a byte, los N productos) inmediatamente después de escribir. El incidente real: quitar ¿¡ de
un campo rompió D1 y solo lo cazó la re-auditoría.

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

Configura la **Experta en ventas por WhatsApp** de un workspace de Chatea Pro.

> **CÓMO FUNCIONA DE VERDAD:** la configuración general del asistente vive en **2 Bot Fields**
> — se pega el JSON completo y listo. Ruta: Chatea Pro → **Bot Fields** → carpeta del agente
> de ventas → click al campo → modal "Edit Bot Field" → pegar en **Valor**. **Crea los campos
> como tipo LONG JSON.** Las claves del JSON las lee el flujo por nombre → **NUNCA renombrar
> claves**; convenciones nativas: "si"/"no" en minúscula, país en minúscula, números como
> string, `activar: true` boolean. Esquema real:
> `PROYECTOS/CHATEA-PRO-VENTAS-WP/bot-fields-reales/`.

**Regla de Chatea Pro:** 1 workspace = 1 país. 🔴 **El país es PARÁMETRO, no PUERTA**:
de él dependen jerga, transportadoras, moneda y forma de la dirección, así que se pide
siempre — pero **no tenerlo en nuestra lista nunca bloquea**. Ver "Países" abajo.

## Los DOS techos (lo que más rompe — verificado en vivo 2026-08-07)

Hay que respetar **los dos**; `assets/limites.json` los tiene y los scripts los aplican solos.

- **Techo A · el bot field.** El JSON completo se guarda **ESCAPADO**: cada tilde ocupa 6
  caracteres y cada emoji 12. Se mide con `len(json.dumps(valor)[1:-1])`, **NUNCA en crudo**
  (medir crudo ya mató configs). El valor se serializa **compacto** (`separators=(',',':')`,
  `ensure_ascii=False`); otro formato infla el conteo. Topes: **≤19.000 escapados** cabe en
  cualquier campo; entre 19.000 y 500.000 **solo** en LONG JSON (si es JSON legacy se corta a
  20.000 y el bot muere); ≥500.000 no cabe ni en LONG JSON. **Pasarse no da error:** la API
  responde `200 ok` y guarda CORTADO; solo se ve en Panel → Registros de errores. Por eso todo
  push **relee y compara** (`push_config.py` lo hace).
- **Techo B · el campo nativo del formulario.** Escribir por API por encima del tope nativo
  funciona, pero el día que alguien abra ese formulario en el panel y guarde, **el campo se
  corta**. Se mide en **unidades UTF-16** (como cuenta el panel: cada emoji astral vale 2), no
  en code points. Topes (del código de la app): rol/restricciones/análisis 2.000 · `prompt_datos`
  4.000 · notificación 400 · `prompt_libre` 12.000 · mensaje_inicial/pregunta_de_entrada
  1.000 · remarketing 1.000 c/u · descripción del producto (`dta_prompt`) 500 · pixel
  (`meta_conversion.id`/`aud_id`) 150. El token de proveedor Dropi (1.200) y el "mensaje
  inicial" de upsell (200) son de OTROS campos que esta skill no genera → en
  `limites.json._referencia_sin_campo`, no se validan aquí. Tabla completa:
  `references/paises.md` y el proyecto `TOPES-NATIVOS-POR-CAMPO.md`.

## Las piezas

**Configuración general** (1 vez por tienda) → 2 Bot Fields:
- Campo `[Ventas Wp] Configuracion general` → `assets/template-botfield-1-configuracion.json`
  (Dropi, validaciones de orden, Producto en Segundos con prompt maestro, notificaciones)
- Campo `[Ventas Wp] Configuracion general 2` → `assets/template-botfield-2-comportamiento.json`
  (comportamiento de la IA: división de mensajes, rol, restricciones, análisis de palabra clave)

**Producto** (se repite por producto) → 2 piezas SIEMPRE juntas:
- Su Bot Field `[Producto Ventas Wp] N` → `assets/template-botfield-producto.json`
  (información, embudo de ventas, prompt libre, voz, recordatorios, remarketing,
  activadores, meta conversión, upsells)
- Su entrada en el índice `[Ventas Wp] Disparador de productos Extendido` (Long JSON,
  <500.000, UNO por workspace) → `assets/template-registro-disparador.json`. Se AÑADE al
  array existente sin borrar los demás productos.

**Interruptores del workspace** — 16 Bot Fields sueltos, uno por campo, NO son la
configuración (esa son los 2 JSON de arriba): `assets/campos-sueltos.json` es su ÚNICA
fuente (`build_config.py` los emite en `<prefijo>_CAMPOS_SUELTOS.txt`). Oficina y los dos
de Recaudo se DERIVAN de país/modelo, los demás son fijos — no se copian valores sueltos
aquí porque un texto fijo describiendo un valor derivado es la misma trampa que ya rompió
el conteo de países.

**Prefijo `[WhatsApp IA]`** (10 campos, MEDIDO en vivo 2026-09-08, mismo archivo): 7 son
ESTADO que escribe el bot mientras opera — contadores de venta, logs, versión — y **nunca
se tocan al configurar**: escribir sobre ellos borra datos de venta reales del día (uno
trae literalmente "NO MODIFICAR ESTE VALOR" en su descripción). Solo 2 son decisión real
del negocio: si el recordatorio revisa el estado del producto antes de enviarse, y si sale
la nota de felicitación en cada venta. Uno queda `_pendiente_declarado`: sin descripción
en el panel, no se le inventa semántica.

## Prompts del motor (fijos, horneados en `assets/prompts/`)

Pulidos y genéricos — NUNCA se recortan ni se rehacen a mano. Se mantienen dentro de los
límites de la UI de Entrenar para que sirvan por las dos vías:

| Archivo | Va en | Límite UI |
|---|---|---|
| `assets/prompts/rol-general.txt` | campo 2 → `comportamiento_ia.rol` (huecos `{{IDENTIDAD}}`, `{{CAMPOS_DIRECCION}}`) | 2000 |
| `assets/prompts/restricciones.txt` | campo 2 → `comportamiento_ia.restricciones` (huecos `{{PAGO_REGLA}}`, `{{ACLARACION_DIRECCION}}`) | 2000 |
| `assets/prompts/analisis-palabra-clave.txt` | campo 2 → `analizar_palabra.prompt` (lleva `{{URL_TIENDA}}`) | 2000 |
| `assets/prompts/reglas-estructura-producto.txt` | campo 1 → `producto_segundos.prompt_datos` (hueco `{{ACLARACION_CORTA}}`; solo ~15 caracteres de margen) | 4000 |
| `assets/prompts/notificacion-venta-realizada.txt` | campo 1 → `notificaciones...mensaje` (variables `{nombre_producto}` etc.) | 400 |

**Huecos derivados, no escritos a mano.** El vocabulario de direccion (departamento/barrio en
Colombia, estado/colonia/código postal en México, comuna en Chile…) sale de `assets/limites.json →
vocabulario_direccion_por_pais`, nunca del texto fijo. El mapa tiene **23 países**, copiados de los
packs de `golden-chatea-pro-validacion-direcciones` (cada entrada guarda `fuente` y la cita literal).
Un país sin pack NO bloquea ni hereda a Colombia: cae a un genérico neutro y lo declara. Cómo se
regenera, cómo añadir un país y por qué la cláusula corta pesa: `references/paises.md`.

## Intake — LOS 7 DATOS que se le piden al cliente (estándar de FER, 2026-09-19)

🔴 **Vale igual para instalación nueva y para optimización de un espacio en uso**, y es el conjunto
de TODOS los asistentes del espacio: se releva una vez. Lo que no está aquí no se pregunta: se lee,
se deriva o se decide con nuestro criterio. FER: *"mucha gente confía en mi criterio... preguntarles
sería una fricción y me van a responder cualquier cosa sin saberlo realmente"*. Un cliente que no
sabe de optimización contesta por salir del paso, y ese dato malo queda configurado.

1. **Nombre y link de la tienda.** → `rol` (nombre de la empresa) y `analizar_palabra.prompt` (la URL a
   la que se redirige lo no configurado). La web se **LEE** para escribir el prompt maestro y para el nicho.
2. **País.** → `conexion_con_dropi.pais`. De él salen la moneda, el flete nativo, el vocabulario de
   dirección y el interruptor Oficina: ninguno se pregunta.
3. **Dropshipping, marca propia o los dos.** → `--modelo dropshipping|marca|mixto`. Decide el modelo de
   pago del `rol` y las restricciones y los dos interruptores de recaudo (dropshipping = contra entrega ·
   marca = anticipado · **mixto = contra entrega por defecto y anticipo solo si el cliente lo pide o la
   ficha del producto lo exige**, como opera Golden). Es el dato que más cambia el texto.
4. **Nombre del asesor.** → `--nombre-bot`. No existe llave propia: vive DENTRO del `rol` (tope 2.000).
   `build_config.py` mide el conjunto y, si se pasa, **no escribe nada** en vez de entregar un rol cortado.
5. **WhatsApp de la empresa.** → `notificaciones.notificacion_1.whatsapp`. Va **DE ÚLTIMO y después del
   pago**. Si aún no lo tiene, se monta igual con la notificación apagada y se conecta cuando lo tenga.
6. **Correo y contraseña del espacio.** → es **ACCESO, no un campo**: excepción a "todo lo que se pregunta
   cae en un campo", autorizada por FER. Nunca va a un archivo, JSON o bot field, ni se repite en el chat;
   la API va por **token**, no por contraseña; el asistente **no teclea contraseñas** en formularios; al
   cerrar se cambia (protocolo VIP: rotar al cerrar). Si hay que guardarlos temporalmente, van a
   `<PROYECTO>/.secrets/` con permisos 600 (ley del Centro de Mando), jamás a un `.md`, a un JSON ni a esta
   skill, que es repositorio público.
7. **Desde qué valor considera que un flete ya es demasiado caro.** → `validar_flete.flete_minimo`: el
   corte de "cliente no calificado". Ver "Flete".

**Ya NO se preguntan:** el **nicho** (se lee de su web) y el **número de servicio al cliente**.

### Nicho: se LEE de su web, y el modelo dice cuánto pesa
Se lee la **web**, no los productos cargados en un campo. `--nicho` es opcional; sin él la identidad se
escribe sin coletilla (nunca un paréntesis vacío).
- **Marca propia:** una sola línea → si la web muestra una especialidad clara, entra como nicho.
- **Dropshipping o mixto:** por definición vende sin relación entre categorías y rota lo que promociona →
  **por defecto sin nicho**; solo si la web muestra UNA especialidad clara y sostenida.
🔴 Error real (2026-09-18, Golden): se derivó "cuidado capilar y bienestar" de los 12 productos cargados
ese día y la empresa vende también café, crema para arrugas y más. Prometer una asesora "experta en X"
en un catálogo variado es peor que no decir nada, y como el catálogo rota, el texto caduca solo.

### Flete: promedio del país + el corte del cliente
- **Nativo:** `assets/limites.json → flete_max_por_pais` (el promedio del país). Hoy solo Colombia (25.000);
  los otros nueve los aporta el Centro de Mando y se añaden cada uno en la moneda de su país.
- **El corte del cliente manda encima:** su respuesta al dato 7 va a `--flete-max` (acepta "25.000" o
  "$25 000"). Quien no sepa responder se queda con el promedio nativo, así que la pregunta no lo frena.
- Si el **ticket promedio del espacio subió**, el tope se sube por criterio de Golden o se consulta.
  🔴 **NO se deriva el flete del ticket ignorando el promedio del país**, ni se copia el de otro país.
- País sin promedio y sin respuesta: el script se detiene y lo pide. Sin Dropi no aplica (queda "0").

**NO SE PREGUNTA — se lee del espacio, se deriva o es doctrina:**

· **Dropi conectado** → se LEE del espacio con el token. Si no se puede leer, default sí e INFORMA.
· **Subida automática del pedido** → se LEE: sin historial de órdenes entra en **NO** (recomendación de
  FER para quien arranca); con operación en marcha, sí.
· **Moneda** → se DERIVA del país (`assets/limites.json`).
· **Rol y restricciones** → doctrina de la casa más los datos 1, 3 y 4. Las restricciones son método con
  **UNA sola línea que depende del negocio: la regla de pago**, que decide el dato 3.
· **Prompt maestro** → **NO se pide: se ESCRIBE**, con `golden-chatea-pro-prompt-ventas`, leyendo la web y
  con la doctrina de venta de la casa. `build_config.py` lo EXIGE (exit 1 sin escribir si falta, para que el
  campo no quede con `{{PROMPT_MAESTRO}}` literal).
· **Plantilla de Meta** → **NO se usa** (FER, 2026-09-08). `notificacion_1.plantilla` queda vacía; las
  banderas `--plantilla-notif` y `--plantilla-ns` siguen en el script por si alguna vez hace falta.

**Defaults de FER, no se preguntan y no se negocian:** validar entregas sí, con **60%** y mínimo **3
órdenes** · validar flete sí · división "varios" / **máx 2 mensajes** (con 3 la IA responde en ráfagas que
se sienten robot) · análisis de palabra clave activado · notificación de Venta Realizada.

🔵 **Sin fuente, y se declara:** las transportadoras prohibidas del asistente logístico. Se intenta LEER de
Dropi; esa pregunta es del logístico, no de este asistente.

## Producto (Bot Field por producto + registro)

División de responsabilidades: **esta skill pone la ESTRUCTURA** (JSON nativo, límites,
validación); **`golden-chatea-pro-prompt-ventas` pone los TEXTOS** (prompt de venta,
mensaje inicial, pregunta de entrada, recordatorios, prompts de remarketing).

1. Copia `assets/template-botfield-producto.json` y llena los `{{PLACEHOLDERS}}`:
   - **Datos duros** (preguntar, nunca inventar): nombre, precio (solo dígitos; repetirlo
     dentro del prompt: la IA lo cita desde ahí), ID Dropi (va en `id` Y en `id_dropi`),
     SIMPLE o VARIABLE, URL de imagen de portada, URLs de multimedia, palabra clave,
     IDs de anuncio si hay, API key + ID de voz si usa voz (si no: `habilitar: "no"` y
     vacíos).
   - **Textos de venta** (de `golden-chatea-pro-prompt-ventas`): OJO con el formato nativo —
     los recordatorios son PROMPT-instrucción ("EVENTO: el usuario no respondió...
     MÍNIMO 35 PALABRAS." + ejemplo), y el remarketing son ROLES por fase (1 = reactivación
     suave, 2 = último llamado con urgencia), no mensajes literales.
2. Llena `assets/template-registro-disparador.json` con el MISMO nombre, palabra clave e
   IDs de anuncio, y el `name` del campo (`[Producto Ventas Wp] N` — mira en Bot Fields el
   último N usado y suma 1).
3. **Valida SIEMPRE antes de entregar** (genera además la copia `_LIMPIO.json` sin _meta,
   lista para pegar):
   ```bash
   python3 scripts/valida_producto.py --in /ruta/<producto>_BOTFIELD.json \
     --registro /ruta/<producto>_REGISTRO.json
   ```

Defaults de producto: voz estabilidad 0.3 / similaridad 0.7 / estilo 0.5 / velocidad 1 /
speaker_boost false / responder audio con audio sí / máx 5 audios / probabilidad 100 ·
recordatorios 30 min y 2 horas · remarketing 3 horas y 23 horas · rango 06:00–22:00 ·
meta_conversion habilitado por defecto · **upsells desactivados por defecto** (el template
los deja `activo:"no"`, pero YA NO están bloqueados por plan — se activaron el 2026-07-12).

**Upsells nativos** (opcionales, 2 tarjetas que Chatea muestra tras "compra realizada"):
título ≤80, descripción ≤80, botón ≤20, precio, id_dropi. Si se activan, el **prompt del
producto NO hace su propio pitch de upsell** (se pisarían y el cliente vería doble
ofrecimiento): el prompt solo procesa la aceptación y cuadra el total. El texto de las
tarjetas lo produce `golden-chatea-pro-prompt-ventas`; el validador chequea sus límites.

## Espacio que YA existe: se AUDITA antes de tocar (optimizar, no instalar)

```bash
python3 scripts/auditar_espacio.py --token-file <ruta>     # solo lectura; --guardar-volcado para respaldo
```
Da una nota medida sobre 1000 y separa **DEFECTO** (se arregla), **DECISIÓN** (puede ser una elección del
negocio: la resuelve Golden con su criterio, con la propuesta ya validada, y **no se escribe por cuenta
propia**; en un espacio de cliente NO se le consulta al cliente, salvo el corte de flete) y **AVISO**.
Ejemplo real: 8 de 12 productos activos sin entrada en el Disparador. Puede ser un defecto o una
decisión de vender kits solo dentro del flujo del producto principal; cambia qué arranca en
producción, así que se pregunta. Después: respaldo → escribir → releer del servidor → auditar de nuevo.
🔴 **Antes de "restaurar" un espacio que se ve en blanco, LEER el servidor:** el panel puede mostrar
vacío un espacio intacto (workspace equivocado, caché, JSON inválido). Restaurar sobre datos buenos
con una copia vieja los destruye. Detalle, rúbrica y trampas de la API: `references/espacio-existente.md`.

## Casos borde (decide por convención e informa)

- **Negocio sin Dropi** → `--dropi no` (apaga también la subida automática); `--flete-max` se
  omite (deja de ser obligatorio) y el JSON conserva las claves con `"0"` (el flujo las espera).
- **Sin voz ElevenLabs** → `usar_voz: No` y se omiten API key, ID y parámetros.
- **Sin plantillas Meta aprobadas** → remarketing "No enviar plantilla"; solo recordatorios
  (ventana 24h) y avisar que el fuera-de-ventana queda apagado hasta aprobar plantillas.
- **Un texto excede su límite** → regenerar esa pieza con `golden-chatea-pro-prompt-ventas`
  en versión corta; los prompts fijos no se tocan.
- **Falta la skill hermana** → escribir los textos a mano respetando límites e informar.
- **La plataforma no coincide con este mapa** → Chatea Pro cambia sin aviso: re-verificar
  en vivo y actualizar `assets/limites.json` + la referencia del proyecto.
- **Nombres de los Bot Fields distintos** → si el workspace del cliente usa otra plantilla
  de bot, ubicar los campos JSON equivalentes en Bot Fields y pegar ahí (el contenido es
  el mismo); si no existen, crearlos con esos nombres dentro de la carpeta del agente.
- **Producto nuevo en workspace ajeno** → antes de asignar el `N` del campo, revisar en
  Bot Fields qué números ya existen; el registro del Disparador se EDITA añadiendo la
  entrada, jamás pegando un array que borre los productos anteriores.
- **Par `Disparador` / `Disparador Extendido` (gotcha crítico)** → Chatea migró: el campo
  viejo `[Ventas Wp] Disparador de productos` (tipo JSON/array) quedó **VACÍO** y el vivo es
  `[Ventas Wp] Disparador de productos Extendido` (LONG JSON). Un flujo que siga leyendo el
  array viejo lee vacío. Al auditar o instalar, escribir SIEMPRE en el campo con "Extendido"
  y verificar cuál lee el flujo; buscar siempre el par `X` / `X extendido`.
- **Prompt de producto >12000** → va SOLO por Bot Field (LONG JSON). La pantalla "Prompt del
  producto" de la UI v2 lo corta a 12000 y su "Guardar asistente" sobrescribe con la versión
  cortada: para esos productos, tratar esa pantalla como solo-lectura. El validador avisa.
- **Truncada silenciosa al cargar por API** → pasarse del tope del campo devuelve `200 ok`
  con el texto CORTADO; `push_config.py` relee y compara longitud. Nunca dar por buena una
  carga sin ver el "todo guardado íntegro".
- **Pendiente con dueño**: otros eventos del dropdown de notificaciones (falta pantallazo
  del dropdown abierto).

## Techo alcanzable de esta skill (mandato de autocalificacion v2)

PARA EL 1000 ME FALTA: probar la ESCRITURA de `scripts/push_config.py` contra la API REAL de
Chatea Pro en un workspace de control desechable. (Verificado en vivo el 2026-09-18: `read` y
`backup`, y así se descubrió que el filtro `name` casa por coincidencia parcial; la escritura no.) **(Actualizado el 2026-09-06: la otra reserva que había aquí
—la puerta de país— ya no es una reserva, es un defecto reparado; ver el changelog.)** Hoy su comportamiento esta verificado por
`scripts/autoprueba_push.py`, que SIMULA la API (12 de 12 en verde, con contraprueba que
demuestra que el banco muerde); pero un simulador escrito por la misma mano que el codigo puede
compartir su error, y un cambio de contrato del servidor real no se veria. Lo puede dar: FER /
una corrida real / una credencial. No lo puedo cerrar yo.

Con eso declarado, el techo alcanzable de esta skill es **985/1000**, y ese es su estado:
terminada y correcta, no incompleta.

## Terminado = checklist

- [ ] `build_config.py` con exit 0 → los 2 Bot Fields con Techo A
      🔴 **Este punto ya NO exige que el país esté en una lista.** Lo exigía, y era una
      puerta ejecutable: rechazaba El Salvador y Bolivia por escrito. Si el país no tiene
      pack, se investiga lo que falte (moneda incluida) y se configura igual.
  (escapado) OK y cada prompt bajo su tope nativo (Techo B).
- [ ] Campos creados como **LONG JSON** (no JSON) y `push_config.py` cerrando con "todo guardado
  íntegro" (releído y comparado).
- [ ] Sin caracteres de 4 bytes (emoji) en las palabras clave/trigger.
- [ ] Si se tocó `scripts/valida_producto.py`, su banco en verde:
  `python3 scripts/autoprueba_d1.py` (9 casos del cruce D1 con el registro en su forma
  REAL de array, incluidos los que se saben malos).
- [ ] Si se tocó `scripts/build_config.py`, el guardarraíl de doctrina en verde:
  `bash scripts/verificar_pais_no_es_puerta.sh` (4 de 4). **No comprueba que la lista de países
  esté completa —eso es un dato que caduca solo— sino que la lista NO haya vuelto a ser una
  puerta**, ejerciendo con un país sin pack, y trae contraprueba que muerde si alguien la repone.
- [ ] Si se tocó `scripts/push_config.py`, su banco en verde:
  `python3 scripts/autoprueba_push.py` (10 pruebas contra un servidor que imita la API,
  incluida la truncada silenciosa). Simula la API; NO sustituye una prueba en vivo.
- [ ] **D1 verificado**: la palabra clave del producto y la entrada del Disparador Extendido
  son idénticas **byte a byte** (lo chequea `valida_producto.py --registro`; sin `--registro`
  ese cruce NO se hace). Re-verificar D1 también DESPUÉS de cualquier edición de texto que
  toque `palabras_clave` — es lo que rompió el arranque en ese incidente de campo.
- [ ] Por cada producto: `valida_producto.py --registro` con exit 0, sin `{{placeholders}}`,
  y entregada la copia `_LIMPIO.json`.
- [ ] Datos reales confirmados por el usuario (precio, WhatsApp, palabra clave, ID Dropi).
- [ ] Entregados los archivos con la instrucción exacta de dónde se pega cada uno:
  config general → campos 1 y 2 · producto → su campo `[Producto Ventas Wp] N` · registro →
  AÑADIR al Disparador de productos Extendido.
- [ ] Informados los defaults aplicados y los casos borde activados.

## Compuertas de esta skill

Cuatro reglas de procedimiento que se aplican a esta skill misma, no al bot del cliente.

- **Validador oficial:** `agentskills validate <RUTA ABSOLUTA>` debe decir "Valid skill".
  Con `.` en vez de la ruta absoluta da un fallo FALSO (confirmado); no se corre con punto.
- **Tope DURO de la `description`: 1024 caracteres.** Lo que se pasa se TRUNCA, y lo primero que
  se pierde son los disparadores del final, que son los mas nuevos. Lo comprueba
  `python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>`
  (salida 0 = en norma). Medir sin comparar contra la vara no es un chequeo: por eso esto se
  corre, no se mira.
- **Auditoría repetible:** `python3 scripts/autoprueba_auditor.py` (26 de 26) prueba que
  `auditar_espacio.py` da 1000 a lo limpio en dos países y tres modelos y muerde 16 clases de fallo
  (incluida la fuga de vocabulario entre CUALQUIER par de los 23 países, no solo Colombia).
  Si se toca `build_config.py`, los assets o los límites, se corren los cuatro bancos:
  `autoprueba_push` 12/12 · `autoprueba_d1` 9/9 · `autoprueba_auditor` 26/26 (incluye el flete) · `verificar_pais_no_es_puerta.sh` 4/4 ·
  `autoprueba_vocabulario` 299/299 (los 23 países del roster ANCLADO por nombre —PAISES_MAPA—, cita literal,
  derivación, contenido contra el pack COMPLETO —no solo la cita—, origen de un conjunto cerrado, la excepción
  de campos_memoria atada al país, un país borrado se nombra en vez de reventar, techos, y los cinco sabotajes
  que midió el CdM reproducidos y en rojo).
- **Estandar 9:** todo cambio relevante de esta skill se reporta al Centro de Mando.
- **`division.limite` = 2 y no se sube a 3.** Con 3 la IA responde en rafagas de robot; 2 cubre
  imagen-URL mas texto. El valor vive en `assets/template-botfield-2-comportamiento.json`.

Historial de versiones (19 actas de sello, verbatim): `references/changelog.md`.

## Países — para saber CÓMO enfocarlo, nunca para prohibir

🔴 **Mandato de FER (2026-09-06):** *"Hoy son diez, mañana doce, pasado treinta. El país se pide
para saber cómo enfocarlo, cuál es la jerga, cuál es la validación de direcciones, pero no para
prohibir."* Hasta la v4.7 esta skill tenía la puerta **viva y ejecutable**: `build_config.py`
rechazaba `el salvador` y `bolivia` por escrito, con exit ≠ 0 y sin generar nada. **Ya no.**

**Por qué se retiró en vez de corregir la cifra.** Una lista de países dentro de una skill es un
dato que **caduca solo**, y esta ya caducó una vez: decía 7 cuando eran 10 y rechazaba por escrito
a Guatemala, Argentina y Brasil. Vigilar la cifra deja el trabajo abierto para siempre; retirar la
puerta se lleva la clase entera de defecto. El guardarraíl es
`scripts/verificar_pais_no_es_puerta.sh` — **no comprueba que la lista esté completa: comprueba
que no vuelva a ser una puerta**, ejerciendo, y trae contraprueba que muerde si alguien la repone.

**Los que HOY tienen pack conocido** (remedido 2026-08-29 contra el bundle vivo): **COLOMBIA ·
ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY · GUATEMALA · ARGENTINA · BRASIL**. Eso es
todo lo que significa esa lista: **dónde ya no hay que investigar**. Para cualquier otro país
`build_config.py` avisa y **sigue**; lo único que pide es `--moneda`, y esa **se INVESTIGA (el
código ISO-4217), no se le pregunta al negocio.** Esta lista es distinta del mapa de
**vocabulario de dirección** (23 países, ver "Prompts del motor" arriba): Argentina y Brasil SÍ
tienen vocabulario derivado desde v4.13, aunque no eran de los "7 originales" de esta lista de
plataforma. Brasil va en portugués. En el JSON,
`conexion_con_dropi.pais` va en minúscula pero debe ser uno de los 10. Lo que cambia por país
—división geográfica, código postal, oficina, zonificación, regulador, vocabulario— está en
`references/paises.md`. **México:** código postal **REQUERIDO**, **no existe** recolección en
oficina (todo a domicilio), y "domicilio" = la CASA (en Colombia es el pedido). No copies el
criterio de un país a otro: revísalo uno por uno.

## Lo que NO se hereda al clonar a otro cliente

Al reusar una configuración para otro negocio, **vaciar/parametrizar** (si no, se filtran datos
del dueño anterior):
- **Parametrizar, nunca quemar:** nombre de la tienda, URL, nombre de la asesora, WhatsApp de
  notificaciones, tiempos de entrega, políticas de garantía, país y moneda.
- **Vaciar:** catálogos (`[Producto Ventas Wp] N`, el Disparador Extendido), métricas del dueño,
  y cualquier campo de integraciones con llaves en texto plano (Dropi/Shopify/OpenAI/Meta).
- **La fuga menos obvia:** los **nombres de producto y de paquetería dentro de los ganchos de
  venta** (prompt del producto, ejemplos). La IA los imita: en una cuenta heredada aparecieron
  transportadoras y la marca del dueño anterior dentro del workspace de otro cliente. Revisar
  los textos, no solo los campos de datos.
- **Imágenes:** las URLs `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` apuntan a la
  cuenta de ORIGEN y solo nacen subiendo la imagen en el panel (la API no tiene endpoint de
  subida). Copiar esa URL a otro cliente muestra la imagen de la cuenta ajena. Usar URLs
  propias (CDN de Shopify sirve) o subir en el panel del cliente.

## Conexiones (skills hermanas)
- 🎯 Prompt/promo por producto y prompt maestro → `golden-chatea-pro-prompt-ventas`
- 💬 Asistente de comentarios → `golden-chatea-pro-config-comentarios`
- 📦 Asistente logístico → `golden-chatea-pro-config-logistico`
- 🔁 Asistente de carritos → `golden-chatea-pro-config-carritos`
- 🗂️ Producto del asistente de COMENTARIOS (otro campo, otras 5 llaves) → `golden-chatea-pro-producto-comentarios`
- 📍 Prompt de validación de direcciones (hijo del logístico) → `golden-chatea-pro-validacion-direcciones`
- 🎬 Coordinar los asistentes del espacio → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales de un negocio (números de WhatsApp, cuentas de pago, API keys,
IDs de voz, URLs, precios, marcas) en los archivos de la skill: se preguntan en cada uso y
viven solo en los JSON entregados. Los prompts de `assets/prompts/` son genéricos por
diseño; los ejemplos reales viven fuera de la skill, en la carpeta del proyecto.

## Fronteras y desambiguacion

🔴 **Aquí NO se guarda una copia de la description.** Se guardaba "para no perder ningún
matiz", y esa clase de copia ya mordió dos veces en el arsenal: **envejece y acaba
contradiciendo a la description viva** — así se coló el dato falso de "7 países" en una
hermana. Lo que sí es frontera se escribe como frontera, aquí abajo, y se mantiene.

**Esta skill INSTALA el asistente de ventas. No monta productos.**

· El **producto** —su campo y su prompt de venta juntos— lo monta `golden-chatea-pro-prompt-ventas`.
  Quien diga "monta este producto", "hazme el prompt de X" o "mejora este prompt" va ahí, no aquí.
· **Comentarios, logístico y carritos** tienen cada uno su propia skill hermana.
· **Los cuatro a la vez** los orquesta `golden-chatea-pro-full-configuracion`.
· Auditar lo instalado → `golden-chatea-auditoria`. Auditar cómo va operando → `golden-chatea-operacion`.
