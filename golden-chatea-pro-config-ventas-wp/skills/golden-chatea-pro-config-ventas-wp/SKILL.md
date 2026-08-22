---
name: golden-chatea-pro-config-ventas-wp
description: Golden Group — Configura el asistente de VENTAS POR WHATSAPP de Chatea Pro (la "Experta en ventas por WhatsApp", el bot/agente de ventas) de punta a punta con los Bot Fields JSON NATIVOS listos para COPIAR Y PEGAR — 2 campos de configuración general (Dropi, validaciones de orden, Producto en Segundos con prompt maestro, notificaciones, comportamiento de la IA), 1 campo por producto ([Producto Ventas Wp] N: información, embudo con multimedia, prompt de venta, voz, recordatorios, remarketing, activadores, pixel) y su entrada en el Disparador de productos Extendido — con los prompts del motor afinados, parametrización por los 7 países que acepta la plataforma, y validadores de los DOS techos reales (bot field medido ESCAPADO + tope nativo de cada formulario, con truncada silenciosa y sin caracteres de 4 bytes en el trigger). Úsala SIEMPRE que el usuario quiera montar, configurar o replicar el asistente/agente/bot de ventas de WhatsApp de Chatea Pro para una tienda o cliente, "configurar ventas whatsapp", "montar el asistente de ventas", "el JSON del asistente de ventas", "genera los bot fields de ventas", "configura la experta en ventas", o cargar/validar un producto nuevo en ese asistente. La promo/prompt de venta de cada producto se genera con golden-chatea-pro-prompt-ventas; para comentarios, logístico o carritos usa sus skills hermanas; para los 4 a la vez, golden-chatea-pro-full-configuracion.
---

# Golden · Chatea Pro — Asistente de Ventas WhatsApp

<!-- skill v4.2 · 2026-08-21 (auditoría golden-skill-auditor, PLATA→verificar) · DOS CONTRADICCIONES reales cazadas por ejecución (no por lectura): (1) SKILL.md Intake #6 decía "(Opcional)" el prompt maestro, pero build_config.py YA fallaba con exit 1 sin él desde v4.1.4 — el docstring se corrigió entonces pero el cuerpo de SKILL.md quedó desincronizado; ahora dice EXIGE y por qué. (2) build_config.py tenía --flete-max con required=True SIEMPRE, contradiciendo el caso borde documentado "Negocio sin Dropi... el flete no se pregunta" — probado en vivo: --dropi no sin --flete-max tiraba error de argparse (exit 2). Ahora --flete-max solo es obligatorio si --dropi si (el default); sin Dropi se omite y el JSON queda con "0". Probado: dropi=si sin flete-max → exit claro pidiendo el dato; dropi=no sin flete-max → exit 0, JSON con flete_minimo="0". -->
<!-- skill v4.1.4 · 2026-08-08 (centro de mando, spot-check final) · docstring de scripts/build_config.py: --prompt-maestro re-etiquetado de '(opcional)' a OBLIGATORIO (el código lo volvió bloqueante en v4.1.3 y el docstring quedó sin corregir — la lección 'todos los soportes' aplicada al soporte que la incumplía). -->
<!-- skill v4.1.3 · 2026-08-08 (centro de mando, verificación final, bloqueante F2) · scripts/build_config.py entregaba {{PROMPT_MAESTRO}} LITERAL con exit 0 cuando faltaba --prompt-maestro (solo un aviso ⚠️) — la clase exacta que v4.1.2 declaró cerrada, viva en el script que nadie miró. Ahora valida la SALIDA con el mismo validador de huecos que valida_producto (dobles {{[^{}]*}} + llaves simples fuera de la whitelist runtime) y ante cualquier hueco da exit 1 SIN escribir archivo, con mensaje que manda a generar el prompt maestro con golden-chatea-pro-prompt-ventas. También: --out-prefix con directorio inexistente da error legible (makedirs). Probado: sin --prompt-maestro exit 1 y cero archivos; con él exit 0 y los 2 BOTFIELD escritos. -->
<!-- skill v4.1.2 · 2026-08-08 (centro de mando, hallazgo del golden-verificador en la auditoría de la hermana config-comentarios) · FIX PUNTUAL en scripts/valida_producto.py: el regex de placeholders \{\{[A-Z0-9_]+\}\} solo cazaba mayúsculas puras — {{Hueco}}, {{hueco}}, {{ X }}, {{HUECO-2}}, {{HUECO 3}} y los slots de llave SIMPLE sin llenar ({URL_TIENDA}, {ID_DROPI}...) viajaban LITERALES al bot del cliente. Ahora: dobles con \{\{[^{}]*\}\} (cualquier contenido) + llaves simples contra whitelist de las 5 runtime legítimas de Chatea (las de notificacion-venta-realizada.txt: nombre_cliente, nombre_producto, porcentaje_entrega, telefono_cliente, valor_venta) con error ante cualquier otra. Probado: 5 variantes dobles plantadas cazadas, slot simple colado cazado, producto lleno con {valor_venta} runtime sin falso positivo. -->
<!-- skill v4.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v4.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v4.0 · 2026-08-07 · BRIEFING de instalación (aprobado por FER, verificado en vivo contra dos workspaces reales). FIX MAYOR: los 2 TECHOS. (A) el bot field se mide ESCAPADO — len(json.dumps(valor)[1:-1]), cada tilde 6, cada emoji 12 — no en crudo; salida COMPACTA (separators). (B) topes NATIVOS del formulario extraídos del CÓDIGO de la app (rol/restr/analisis 2000, prompt_datos 4000, notif 400, prompt_libre 12000, mensaje_inicial/pregunta 1000, remarketing 1000, descripcion 500, token Dropi 1200). PAÍSES: solo 7 válidos (COLOMBIA/ECUADOR/CHILE/MEXICO/PANAMA/PERU/PARAGUAY), build_config los valida; references/paises.md con deltas (MX: CP requerido, sin oficina, "domicilio"=casa). Gotchas API: llave `data`, var_type+value al crear, listado PAGINA, trigger sin 4-bytes (validado, rompe el bot), releer siempre. Sección "no se hereda al clonar" (incl. nombres de producto/paquetería en los ganchos). -->
<!-- skill v3.2 · 2026-07-12 · prompts del motor endurecidos tras test de campo (3 prioridades, memoria del pedido, única confirmación, URLs blindadas, sin 2 preguntas/mensaje); division.limite 3→2 (con 3 la IA responde en ráfagas robot; 2 cubre imagen-URL + texto) -->
<!-- skill v3.1 · 2026-07-09 · PRODUCTOS también nativos: 1 Bot Field JSON por producto ([Producto Ventas Wp] N) + entrada en el índice "[Ventas Wp] Disparador de productos Extendido" (Long JSON); template-botfield-producto.json con esquema real (recordatorios=prompt-instrucción EVENTO/35 palabras, remarketing=rol por fase, keyW/idAd=7 slots por comas), valida_producto.py con cruce producto↔registro y copia _LIMPIO; interruptores Boolean del workspace documentados -->
<!-- skill v3.0 · 2026-07-09 · FORMATO NATIVO descubierto y verificado: la config general vive en 2 Bot Fields JSON (<20000 c/u, carpeta del agente); templates con el esquema real (claves intocables), build_config.py emite los 2 campos copy-paste (estructura IDÉNTICA a producción); prompts del motor pulidos ≤ límites de la UI -->
<!-- skill v2.1 · 2026-07-09 · auditoría golden-skill-auditor 838→990: sin ¿¡ en prompts horneados, limites.json fuente única, casos borde + checklist -->
<!-- skill v2.0 · 2026-07-08 · reconstruida sobre el mapa levantado en vivo de la UI de Entrenar -->

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

**Regla de Chatea Pro:** 1 workspace = 1 país (solo 7 válidos, ver "Países" abajo).

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

**Interruptores del workspace** (Bot Fields Boolean, se dejan en su default salvo pedido):
Respuesta Múltiple=true · Oficina=false · Pedido programado=true · Intento de
cancelación=true · Solo Con Recaudo=true · Solo Sin Recaudo=false · Solo Pendiente
confirmación=false · Desactivar Skill Datos=false · Desactivar asignación=false.

## Prompts del motor (fijos, horneados en `assets/prompts/`)

Pulidos y genéricos — NUNCA se recortan ni se rehacen a mano. Se mantienen dentro de los
límites de la UI de Entrenar para que sirvan por las dos vías:

| Archivo | Va en | Límite UI |
|---|---|---|
| `assets/prompts/rol-general.txt` | campo 2 → `comportamiento_ia.rol` | 2000 |
| `assets/prompts/restricciones.txt` | campo 2 → `comportamiento_ia.restricciones` | 2000 |
| `assets/prompts/analisis-palabra-clave.txt` | campo 2 → `analizar_palabra.prompt` (lleva `{{URL_TIENDA}}`) | 2000 |
| `assets/prompts/reglas-estructura-producto.txt` | campo 1 → `producto_segundos.prompt_datos` | 4000 |
| `assets/prompts/notificacion-venta-realizada.txt` | campo 1 → `notificaciones...mensaje` (variables `{nombre_producto}` etc.) | 400 |

## Intake (pregunta solo lo que falte; el resto por defecto e INFORMA)

1. **País** del workspace (ej: colombia).
2. **Moneda** (ej: COP) y **flete máximo** para validar la orden (ej: 23000).
3. **WhatsApp** que recibe las notificaciones de venta.
4. **URL de la tienda** (para redirigir productos no configurados).
5. **Dropi** sí/no (default sí).
6. **Prompt maestro** de Producto en Segundos: el prompt de venta GENERAL del negocio que usa
   "Crea tu asistente en segundos". **`build_config.py` lo EXIGE** (falla con exit 1 y no
   escribe archivos si falta — el bot field no puede quedar con `{{PROMPT_MAESTRO}}` literal);
   no es opcional para generar los 2 Bot Fields. Su único tope es el del bot field (Techo A
   escapado). Si el negocio todavía no tiene uno, pídelo a `golden-chatea-pro-prompt-ventas`
   como prompt de negocio (catálogo completo) ANTES de correr `build_config.py`.

Defaults sin preguntar: subida automática del pedido sí · validar entregas sí (mín 3
órdenes, 60%) · validar flete sí · división "varios" / **máx 2 mensajes** (con 3 la IA
responde en ráfagas de 3 burbujas que se sienten robot; 2 cubre el caso legítimo de
imagen-URL + texto) · análisis de palabra clave activado · notificación de Venta Realizada
activa sin plantilla Meta.

### Generar los 2 Bot Fields

```bash
python3 scripts/build_config.py \
  --pais "colombia" --moneda "COP" --flete-max "23000" \
  --whatsapp-notif "+57 3001234567" \
  --url-tienda "https://mitienda.co" \
  --prompt-maestro /ruta/prompt_maestro.txt \
  --out-prefix /ruta/<NEGOCIO>
```

Produce `<NEGOCIO>_BOTFIELD_1.json` y `<NEGOCIO>_BOTFIELD_2.json` **compactos** (sin claves
_meta), inyecta los prompts fijos, reemplaza `{{URL_TIENDA}}`, **valida el país** contra los 7
y valida los DOS techos: Techo A (bot field ESCAPADO ≤19.000 seguro / ≤500.000 en LONG JSON) y
Techo B (cada prompt bajo su tope nativo). Exit 1 si algo excede un tope duro — nunca recortes
los prompts fijos; acorta el prompt maestro o lo variable. La entrega es: los 2 archivos + en
cuál Bot Field va cada uno + recordar crearlos como LONG JSON.

### Carga automática por API (opcional, recomendado para instalaciones en serie)

Chatea Pro es whitelabel de **UChat**: su API (base `https://chateapro.app/api`, Swagger en
`/api#/`, auth Bearer) permite **escribir los Bot Fields directamente**, sin pegar a mano — la
skill se vuelve una máquina de instalaciones para muchos clientes/países. Endpoints:
`GET /flow/bot-fields?name=` · `PUT /flow/set-bot-fields-by-name` con
`{ "data":[ {"name","value"}, ... ] }`.

`scripts/push_config.py` hace read → backup → push (dry-run por defecto; escribe solo con
`--confirm`). Token del workspace del cliente por `--token`, env `CHATEAPRO_TOKEN` o
`~/.chatea_pro_token`. Flujo seguro SIEMPRE: (1) `read` los 2 campos; (2) `backup` del estado
actual; (3) mostrar qué cambia y, con OK del usuario, `push --confirm`.

```bash
CHATEAPRO_TOKEN="<TOKEN_DEL_CLIENTE>" python3 scripts/push_config.py push \
  "[Ventas Wp] Configuracion general=/ruta/<NEGOCIO>_BOTFIELD_1.json" \
  "[Ventas Wp] Configuracion general 2=/ruta/<NEGOCIO>_BOTFIELD_2.json" \
  --confirm
```

**Gotchas de API verificados en vivo (2026-07-09 y 2026-08-07):**
- El `PUT /flow/set-bot-fields-by-name` usa la llave **`data`**: `{"data":[{"name","value"}]}`.
  Con `bot_fields` responde **400**.
- El alta `POST /flow/create-bot-field` usa **`var_type`** (no `type`) y **exige `value`** aunque
  sea vacío; con otra llave, **422**. Campo nuevo = `var_type: "longtext"` (LONG JSON).
- `GET /flow/bot-fields` **PAGINA** y `per_page` se ignora; para listar TODO hay que recorrer
  páginas (pedir solo la primera dejó fuera 46 de 56 campos en un workspace real). `push_config.py` consulta
  por nombre exacto, así que no depende de paginar.
- El token debe estar **atado al bot/flujo** o la API responde 404 `"Flow not found"`.
- Cloudflare bloquea urllib sin User-Agent (error 1010) — `call()` manda UA de navegador.
- Los pares `nombre=archivo` van ANTES de `--confirm`.
- **Escribir y RELEER siempre**: comparar lo guardado contra lo enviado es la única prueba real
  (y detecta si alguien pisó el cambio desde el panel). `push_config.py` lo hace.

**Token = dato sensible**: no es de pagos pero da acceso a datos de suscriptores del cliente y
puede enviar mensajes. Scope mínimo ("Gestionar el flujo"), no hornearlo en la skill ni en git,
rotar/borrar al terminar. Un `push` a un workspace en vivo SIEMPRE se confirma antes de escribir.

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

## Terminado = checklist

- [ ] País entre los 7 válidos; `build_config.py` con exit 0 → los 2 Bot Fields con Techo A
  (escapado) OK y cada prompt bajo su tope nativo (Techo B).
- [ ] Campos creados como **LONG JSON** (no JSON) y `push_config.py` cerrando con "todo guardado
  íntegro" (releído y comparado).
- [ ] Sin caracteres de 4 bytes (emoji) en las palabras clave/trigger.
- [ ] Por cada producto: `valida_producto.py --registro` con exit 0, sin `{{placeholders}}`,
  y entregada la copia `_LIMPIO.json`.
- [ ] Datos reales confirmados por el usuario (precio, WhatsApp, palabra clave, ID Dropi).
- [ ] Entregados los archivos con la instrucción exacta de dónde se pega cada uno:
  config general → campos 1 y 2 · producto → su campo `[Producto Ventas Wp] N` · registro →
  AÑADIR al Disparador de productos Extendido.
- [ ] Informados los defaults aplicados y los casos borde activados.

## Países (solo 7 válidos)

Chatea Pro **solo acepta**: **COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY**
(sin Guatemala/Argentina/Bolivia/etc.). `build_config.py` rechaza cualquier otro. En el JSON,
`conexion_con_dropi.pais` va en minúscula pero debe ser uno de los 7. Lo que cambia por país
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
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales de un negocio (números de WhatsApp, cuentas de pago, API keys,
IDs de voz, URLs, precios, marcas) en los archivos de la skill: se preguntan en cada uso y
viven solo en los JSON entregados. Los prompts de `assets/prompts/` son genéricos por
diseño; los ejemplos reales viven fuera de la skill, en la carpeta del proyecto.
