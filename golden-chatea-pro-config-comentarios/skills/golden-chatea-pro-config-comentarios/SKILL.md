---
name: golden-chatea-pro-config-comentarios
description: Genera el JSON de configuración GENERAL del asistente de COMENTARIOS de Chatea Pro para una tienda (moderación de comentarios negativos, respuesta pública tipo community manager y venta conversacional que cierra en el mismo chat), con los prompts ya afinados y adaptados por país. Úsalo SIEMPRE que el usuario quiera montar o configurar el asistente de COMENTARIOS de Chatea Pro, generar o armar el JSON de comentarios/respuesta pública/venta conversacional, o diga cosas como "configura el asistente de comentarios", "arma el json de comentarios de chatea pro", "monta la respuesta pública de mi tienda", "necesito el config de comentarios". Si el usuario quiere configurar TODOS los asistentes a la vez (comentarios + logístico + ventas WhatsApp + carritos), eso lo hace golden-chatea-pro-full-configuracion; el asistente de VENTAS por WhatsApp lo hace golden-chatea-pro-config-ventas-wp; los TEXTOS de venta por producto los hace golden-chatea-pro-prompt-ventas; cargar o editar UN producto puntual dentro de Comentarios (el objeto img/name/desc/rela/estado, para que el bot sepa de qué producto habla cada comentario) lo hace golden-chatea-pro-producto-comentarios. NO sirve para configurar productos como cantidad y precios, que van en la ficha del producto y no en esta configuración general.
---

# Chatea Pro — Config del asistente de comentarios

<!-- skill v1.5 · 2026-08-21 (auditoría golden-skill-auditor, PLATA 933→ORO) · (1) Referencia faltante a la hermana golden-chatea-pro-producto-comentarios añadida en description, Conexiones y Gotchas — esa skill existe y hace exactamente lo que la sección de gotchas describía (objeto de 5 llaves img/name/desc/rela/estado) sin que este SKILL.md la nombrara; riesgo real de que un pedido de "cargar un producto a comentarios" se intentara resolver aquí en vez de derivar. (2) build_config.py: cargar_template() y la carga de --intake ya no truenan con traceback crudo si falta el archivo o el JSON está corrupto — ahora dan ERROR legible y exit 1, igual que el resto de validaciones del script (patrón ya usado en validar_topes/validar_sin_placeholders). Probado: --intake inexistente, --intake con JSON roto, y las corridas normales (colombia, mexico con colombianismos, sin --producto) siguen exit 0/2/1 igual que antes. -->
<!-- skill v1.4.3 · 2026-08-08 (centro de mando, spot-check final) · COLOMBIANISMOS: añadido $150.000 (aparecía en la salida junto a $90.000 y la re-derivación de F4 lo omitió; mitigado por 'pesos colombianos' en la misma frase, pero la lista debe estar completa). -->
<!-- skill v1.4.2 · 2026-08-08 (centro de mando, verificación final: 3 bloqueantes) · F3: las frases colombianas QUEMADAS del prompt de venta que sobrevivían al relleno ("en qué departamento estás", la lista corta "nombre, teléfono, departamento..." y "calle, carrera, número") ahora salen del MISMO pack de país que datos_req ({{LISTA_DATOS_CORTA}}/{{DATO_REGION}}/{{DIRECCION_EJEMPLO}} + REGION_POR_PAIS y DIRECCION_EJ_POR_PAIS); departamento/barrio/carrera añadidos a la detección como red de seguridad (se saltan si son vocabulario legítimo del datos_req destino, ej. Departamento en Perú). F5: docstring del script reescrito — 5 datos + --producto obligatorio, y el esquema falso "México y similares: Colonia/Estado/CP" (que la skill ya había declarado falso para Chile/Ecuador/Perú/Panamá/Paraguay) reemplazado por "ver DATOS_POR_PAIS (7 packs)". LECCIÓN aplicada: una corrección entra en TODOS los soportes (SKILL.md + docstring + código) o no está corregida. F4: COLOMBIANISMOS re-derivados del grep real del template (fuera COP que nunca aparece; entran Barranquilla, Bucaramanga, Pereira, BGA, Valle del Cauca, colombiano/a, Colombia, carrera, departamento, barrio, $90.000, 310-555-7788) con comentario de re-derivación al editar el template. Menores: --out con directorio inexistente da error legible (makedirs), cifras del changelog v1.4 corregidas (607 constante, 11.161), y la afirmación "7/7 cazadas" de v1.4.1 reescrita honesta (17/19 y 18/23, clase anidados/no-alfanuméricos ABIERTA en bandeja). Gemelo: ventas-wp v4.1.3 cierra el {{PROMPT_MAESTRO}} literal con exit 0. -->
<!-- skill v1.4.1 · 2026-08-08 (centro de mando, reparación tras 2ª auditoría del golden-verificador: 17 corridas, 8 fallas) · (1) REGEX del validador reparado: \{\{[A-Z0-9_]+\}\} solo cazaba mayúsculas puras (6 de 7 variantes plantadas viajaban literales) → ahora \{\{[^{}]*\}\} para dobles + whitelist de llaves simples runtime ({NOMBRE_PRODUCTO}, {DESCRIPCION_PRODUCTO}) con ERROR ante cualquier otra; cobertura medida por el verificador: 17/19 y 18/23 — la clase de huecos ANIDADOS y NO-ALFANUMÉRICOS queda DECLARADA ABIERTA (los assets no contienen esas formas; registrada en bandeja). Mismo arreglo aplicado a la hermana config-ventas-wp (valida_producto.py, v4.1.2). (2) ej_a_no_eliminar y ej_a_eliminar ahora de TAMAÑO CONSTANTE (referencian las dolencias del prompt general sin repetir la lista — antes rompían el tope a los 10 productos); validar_topes() da ERROR DURO exit 1 SIN archivo si cualquier tope nativo o de negocio se excede: jamás truncar en silencio. (3) Semántica de exits redefinida (0=entregable midiendo COMPACTO+escapado contra LONG JSON 500.000; 1=error duro sin archivo; 2=exceso real con archivo) — antes exit 2 saltaba en el 100% de corridas sanas por el banner legado de 19.000, que ahora es NOTA informativa; documentada en docstring y SKILL.md. (4) reporte() mide TODOS los campos len/tope con OK/EXCEDE, incluidos contacto/t_envio/info_extra/datos_req (antes datos_req imprimía el valor, no la medida). (5) Multipaís HONESTO: checklist/orden/confirmación de datos de envío del prompt de venta salen del mismo pack que datos_req (México ya no contradice al prompt), y con --pais no-colombia el script grepea 9 colombianismos e imprime ADAPTACIÓN MANUAL PENDIENTE con exit 2; SKILL.md declara qué cubre --pais y qué no; description intacta; rediseño completo = proyecto aparte en bandeja. (6) "4 datos" corregido a 5 en intake y generación. (7) Docstring del script con --producto obligatorio y ejemplo completo que corre. (8) Anonimizado el workspace de producción citado en Techo A y gotcha del par array/Extendido (la sección Privacidad lo exigía). Probado: matriz de 5/7/10 productos, sin productos, malformado, 7 huecos plantados y --pais mexico. -->
<!-- skill v1.4 · 2026-08-08 (centro de mando, reparación tras golden-verificador adversarial de la v1.3.2) · CAMBIO FUNCIONAL del guardarraíl anti-dolencias: (1) placeholders pasan de llave simple {DOLENCIA_N} (indistinguible de los {RUNTIME} de Chatea, viajaban LITERALES a la config del cliente) a DOBLE LLAVE {{LISTA_DOLENCIAS}}/{{LISTA_PRODUCTOS_DOLENCIAS}}; build_config.py gana --producto "Nombre:dolencia" repetible (también lista "productos" en el intake), rellena el guardarraíl y da ERROR DURO exit 1 si queda cualquier {{...}} sin llenar (patrón de valida_producto.py de la hermana ventas-wp); mínimo 1 producto obligatorio. (2) REDISTRIBUCIÓN por topes nativos: el peso del guardarraíl (regla + lista por producto) vive en prompt_general (tope 10.000) y ej_a_eliminar/ej_a_no_eliminar quedan compactos bajo 1.000 con margen ≥15% (840 y 607 constante desde v1.4.1) — antes ej_a_no_eliminar iba en 998/1.000 y crecía por producto: el Save del panel cortaba EXACTAMENTE el guardarraíl. (3) reporte() ahora mide e imprime TODOS los campos con tope nativo, marcando excesos; respuesta_publica (3.895/3.000) y venta_conversacional (11.161/8.000 tras v1.4.1) EXCEDEN DELIBERADAMENTE (se pegan por JSON completo, prohibido guardar desde su formulario) y el reporte lo declara impreso. (4) Contradicción resuelta: el intake SÍ pregunta la lista Nombre:dolencia (punto 5 nuevo) — lo que sigue vetado es descripción/cantidades/precios. (5) info_extra por defecto ya no dice "varios años y miles de clientes" (violaba la 5ª categoría de la ley): texto neutro sin cifras ni antigüedad. (6) Números muertos: el "~19.800" de la plantilla reemplazado por "mirarlo en el reporte del script"; el 19.517/97,6% marcado snapshot 2026-08-07; los pares medidos 16.882/19.895 y 19.922/23.266 se CONSERVAN (son experimentos de plataforma, no medidas del template). (7) Corchetes [enfermedad] y [ ] declarados ILUSTRATIVOS (no rellenables); los [dolencia] del punto 7 viejo desaparecieron con la redistribución. (8) Declarado retroactivamente: la v1.3.2 añadió sin declarar un salto de línea al final de template.json (EOF newline); se mantiene. Probado end-to-end con intake de 3 productos: guardarraíl completo y rellenado, cero {{}} literales, 4 campos de comentarios_negativos bajo tope con margen. -->
<!-- skill v1.3.2 · 2026-08-08 (centro de mando) · GUARDARRAÍL ANTI-DOLENCIAS en assets/template.json, versión GENÉRICA con placeholders {DOLENCIA_N}/{PRODUCTO_N}: la "REGLA QUE MANDA SOBRE TODAS LAS DEMAS" en prompt_general (mencionar la dolencia que el producto trata = cliente interesado, jamás se borra; solo se modera si la causó el producto ya usado o si ataca la reputación), el OJO en ej_a_eliminar punto 3 y los puntos 7-8 de ej_a_no_eliminar. Origen: corrección anti-dolencias aplicada al bot vivo de Golden 2026-08-08, origen chat comentarios-debug/Kevin MX — el clasificador stock borraba compradores que mencionaban su dolencia; toda config nueva nacía con ese bug. Fuente histórica (solo trazabilidad, no material vigente): backup GOLDEN_Comentarios_Configuracion.json del mapa de asistentes. Medidas post-edición: prompt_general 2.934/10.000 · ej_a_no_eliminar 998/1.000 · ej_a_eliminar 1.122 (sobre el tope nativo 1.000, igual que el campo vivo de Golden 1.132: entra pegando el JSON completo, pero un Save del formulario lo corta — advertirlo al entregar). -->
<!-- skill v1.3.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v1.3 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → otra marca 2026-08-08 (se colaron una credencial, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat otro espacio de Chatea 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v1.2 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat CONFIG CHATEA KEVIN MX): el techo del bot field se mide en ESCAPADOS (20.000 escapados ~ 17.000 crudos; el script ahora imprime ambas medidas); tabla completa de topes NATIVOS por campo del panel de Comentarios y advertencia de que un Save en el formulario CORTA lo que la API escribió por encima; países limitados a los 7 que acepta la plataforma y datos_req por país REAL (Chile pedía Estado/Colonia/CP — criterio de México clonado y falso; igual Ecuador, Perú, Panamá; Paraguay ni existía); gotchas del producto de Comentarios (5 llaves exactas, par array/Extendido, img solo nace en el panel); higiene al clonar. -->
<!-- v1.1 · 2026-08-07 (centro de mando, cosecha del chat un estudio de producto) · build_config.py parcheado: ahora IMPRIME SIEMPRE el largo final del JSON generado y da ERROR visible (banner + exit code 2) si supera el tope del campo tipo JSON (20.000), recordando crear/convertir el Bot Field a LONG JSON y releer tras escribir. Motivo real: con datos de Chile el script generó 20.074 caracteres (74 sobre el tope) y el aviso genérico no gritó — un campo tipo JSON habría guardado el config CORTADO en silencio con la API respondiendo ok. Probado: caso normal exit 0, caso excedido banner ERROR + exit 2 con el archivo igualmente guardado. -->
<!-- v1.0 · sin sello previo (nota bandeja 2026-08-07: quedó en 1.0.0 por defecto en el repo público) -->

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


Genera el JSON de configuración del asistente de **comentarios** de una tienda en Chatea Pro. Trae fijos y ya afinados: el clasificador de comentarios negativos, el prompt de respuesta pública (community manager + copywriter de la marca) y el prompt de venta conversacional (9 etapas, modo captura, objeciones, cierre en el mismo chat). Todo en español colombiano, humanizado y con precios en `$`.

**Guardarraíl anti-dolencias (obligatorio, viene en el template):** el clasificador trae la "REGLA QUE MANDA SOBRE TODAS LAS DEMAS" — un comentario que nombra la dolencia que el producto trata PREGUNTANDO si le sirve es un CLIENTE interesado y jamás se borra; solo se modera si la dolencia la CAUSÓ el producto ya usado o si ataca la reputación. Existe porque el clasificador stock borraba compradores que mencionaban su dolencia (bug real corregido en el bot vivo de Golden el 2026-08-08). El template trae los placeholders de DOBLE LLAVE `{{LISTA_DOLENCIAS}}` y `{{LISTA_PRODUCTOS_DOLENCIAS}}` (doble llave = los llena `build_config.py`; llave simple tipo `{DESCRIPCION_PRODUCTO}` = los llena Chatea en runtime — no confundirlos). Se rellenan pasando `--producto "Nombre:dolencia que trata"` (repetible, mínimo 1) con los productos de LA TIENDA DESTINO — nunca los de otra (ley de no-herencia, arriba); el script da ERROR DURO si algún `{{...}}` queda sin llenar.

Lo único que cambia entre tiendas es la **información del negocio**, que se pregunta al ejecutar.

## Qué preguntar al usuario (intake)

Pregunta estos 5 datos, **uno a la vez** y en este orden. No los pidas todos de golpe.

1. **País** donde opera la tienda (ej: colombia). **La plataforma solo acepta 7** (campo `[Comentarios IA] País`, MAYÚSCULA y sin acentos): COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY. Si el usuario da otro (Guatemala, Argentina, Bolivia, Costa Rica…), avísale que la plataforma no lo acepta antes de seguir.
2. **Contacto**: una página web, un WhatsApp **o** un correo. Solo uno; es dato de referencia, no para mandar al cliente a otro canal.
3. **Tiempos de envío**: cuánto demora la entrega (ej: ciudad principal 2-3 días, intermedia 3-4, rural 5-7). Este dato **se pregunta siempre**, no se asume.
4. **Información adicional del negocio**: una o dos líneas de respaldo (sede, pago contra entrega, originalidad; si el usuario aporta años o clientes, que sean los REALES de SU negocio — jamás los del template ni los de otra tienda).
5. **Productos y su dolencia** (para el guardarraíl anti-dolencias): la lista de productos de la tienda con la dolencia/problema que trata cada uno, formato `Nombre:dolencia` (ej: `Serum X:hongos en las uñas`). Mínimo 1. Sin esto el clasificador no sabe qué dolencias son señal de compra y el script no genera.

### Datos que la IA le pide al cliente (campo `datos_req`) — se genera solo

En Chatea Pro existe el campo **"datos que la IA debe solicitar al cliente para completar la compra"** (en el JSON: `venta_conversacional.datos_req`). **No lo preguntes en el intake**: el script lo arma automáticamente según el **país** y su nomenclatura REAL de direcciones (cada uno de los 7 tiene su lista propia; ya no existe el esquema "internacional" con Estado/Colonia/CP para todos, que era un criterio de México clonado y falso en Chile, Ecuador, Perú, Panamá y Paraguay):

- **Colombia**: Nombre completo; Número de WhatsApp; Dirección exacta; Barrio o punto de referencia; Ciudad; Departamento. (Sin código postal: no se exige.)
- **México**: Nombre completo; Número de WhatsApp; Dirección exacta; Colonia; Ciudad / Municipio; Estado; **Código Postal** (en México el CP es REQUERIDO: define la zona de reparto).
- **Chile**: Nombre completo; Número de WhatsApp; Dirección exacta (calle y número); **Comuna** (el dato rey); Región o referencia. (Sin código postal.)
- **Ecuador**: Nombre completo; Número de WhatsApp; Dirección exacta (calle principal y secundaria, o Mz y Villa/Solar); Barrio, ciudadela o referencia; Ciudad; Provincia.
- **Panamá**: Nombre completo; Número de WhatsApp; Dirección exacta o referencia clara; Barriada / urbanización o PH y apartamento; Corregimiento; Distrito; Provincia.
- **Perú**: Nombre completo; Número de WhatsApp; Dirección exacta (calle/jirón y número, o Mz y Lote); Urbanización o AA.HH.; **Distrito**; Provincia; Departamento.
- **Paraguay**: Nombre completo; Número de WhatsApp; Dirección (calle y entre qué calles o casi qué esquina); Barrio; Ciudad; Departamento; Referencia.

Si el usuario quiere una lista distinta a la del país, pásala manualmente con `--datos-cliente "campo1; campo2; ..."` y el script la usa tal cual. `datos_req` tiene tope nativo de **200** caracteres.

**Qué cubre `--pais` HOY (sin ambigüedad):** solo (1) la lista `datos_req` del país y (2) la coherencia interna del prompt de venta (checklist, orden y confirmación de datos de envío salen del MISMO pack que `datos_req`). **Lo que NO cubre:** moneda (los prompts dicen pesos colombianos y $90.000), medios de pago (Nequi, Daviplata), ciudades de referencia (Bogotá, Medellín...) y jerga colombiana. Con `--pais` distinto de colombia el script GREPEA el resultado por esos colombianismos e imprime la checklist de **ADAPTACIÓN MANUAL PENDIENTE** con exit 2: no entregues sin adaptarla. El rediseño multipaís completo es proyecto aparte (bandeja del centro de mando).

### Lo que NO se pregunta aquí

No pidas **descripción, cantidades ni precios** de los productos: eso va **en la ficha de cada producto dentro de Chatea Pro**, no en esta configuración general (el prompt de venta conversacional lo lee por la variable `{DESCRIPCION_PRODUCTO}` que Chatea llena producto por producto). OJO, esto NO contradice el punto 5 del intake: la lista `Nombre:dolencia` SÍ se pregunta — es para el guardarraíl del clasificador, no una ficha de producto.

## Cómo generar el JSON

Con los 5 datos del intake, corre el script. Los prompts no se tocan: solo se reemplaza la información del negocio.

```bash
python3 scripts/build_config.py \
  --pais "colombia" \
  --contacto "<lo que dio el usuario>" \
  --t-envio "<tiempos de envío del usuario>" \
  --info-extra "<info del negocio del usuario>" \
  --producto "<Nombre:dolencia que trata>" \
  --producto "<OtroNombre:su dolencia>" \
  --out <negocio>_CONFIG.json
```

El campo `datos_req` (datos que la IA le pide al cliente) se genera solo según `--pais`. Solo agrega `--datos-cliente "campo1; campo2; ..."` si el usuario pide una lista distinta a la estándar del país.

**Semántica de exit codes del script (v1.4.1):** `0` = config entregable (placeholders llenos, topes nativos y de negocio respetados, cabe en LONG JSON de 500.000 medido COMPACTO+escapado, que es lo que se escribe por API; el tope legado de 20.000 del tipo JSON se imprime como NOTA, no es fallo). `1` = error duro y NO se escribe archivo (placeholder sin llenar o llave simple desconocida, sin productos, producto malformado, tope nativo o de negocio excedido — jamás truncar en silencio). `2` = exceso real que muta la entrega, archivo escrito (no cabe ni en LONG JSON, o colombianismos pendientes con `--pais` no-colombia).

El tope del campo depende de su **TIPO**, no de la plataforma: tipo **JSON** = 20.000, tipo
**LONG JSON** = **500.000** (medido por API el 2026-07-25). **Crea el campo como LONG JSON** y el
problema de espacio desaparece (la plantilla llena queda en el orden del 4-5% del cupo LONG JSON —
la cifra exacta cambia con cada edición del template: NO la cites de memoria, mírala en el reporte
del script, que la imprime siempre en crudos y escapados).

⚠️ **El techo del bot field se mide en ESCAPADOS, no en crudos** (verificado en vivo 2026-08-07):
al ejecutarse, el flujo copia la configuración escapada — cada tilde ocupa 6 caracteres y cada
emoji 12 — así que el techo práctico de un campo tipo JSON queda en **~17.000 crudos**, no 20.000
(medido: 16.882 crudos = 19.895 escapados dispara; 19.922 crudos = 23.266 escapados ya no).
Fórmula: `escapado = len(json.dumps(valor)[1:-1])`, y que quede bajo 19.000. El script imprime
las dos medidas.

Si el campo del cliente **todavía es tipo JSON** (los workspaces viejos lo son, incluido
un workspace real de producción, donde `[Comentarios] Configuracion General` iba en 19.517 = 97,6%
del tope — snapshot del 2026-08-07, medir de nuevo antes de citarlo),
entonces sí hay que apretar: **no recortes los prompts** — acorta los campos de negocio (contacto,
tiempos de envío, info), que es lo único editable. Lo correcto es cambiar el tipo del campo a
LONG JSON en la UI, no seguir recortando.

⚠️ **Pasarse del tope NO da error:** la API responde `200 ok` y guarda el JSON **cortado**, con lo
que el asistente empieza a fallar sin un solo mensaje de error. Después de escribir, relee el campo
y compara la longitud.

## Cómo lo usa el usuario

El JSON resultante se pega en Chatea Pro. Aunque la respuesta pública y la venta conversacional superen su tope nativo por campo (3.000 y 8.000), al pegar el JSON completo el backend solo valida el total del campo, así que entra sin problema.

### Techo B — los topes NATIVOS del formulario (y por qué igual importan)

Escribir por API (o pegando el JSON) por encima del tope nativo funciona y no da error. Pero el día que alguien **abra ese formulario en el panel y pulse Guardar, el campo se corta y se pierde el texto**. Adviértelo siempre al entregar: si los prompts superan su tope nativo, nadie debe guardar desde el formulario de Comentarios sin revisar. Topes del panel de Comentarios (extraídos del código de la app, 2026-08-07 · `TOPES-NATIVOS-POR-CAMPO.md` de CHATEA-PRO-ASISTENTES-MAPA):

| Campo | Tope |
|---|---|
| `comentarios_negativos.prompt_general` | 10.000 |
| `venta_conversacional.prompt` | 8.000 |
| `respuesta_publica.prompt` | 3.000 |
| `ej_a_eliminar` · `ej_a_no_eliminar` | 1.000 c/u |
| `informacion_del_negocio.info_extra` | 500 |
| `contacto` · `t_envio` · `datos_req` | 200 c/u |
| descripción del producto de Comentarios | 500 |

### Gotchas del asistente de Comentarios (si se escribe por API)

Cargar cada producto (con su `rela` de disparadores) NO es trabajo de este skill — es `golden-chatea-pro-producto-comentarios`. Lo de abajo es contexto para entender el terreno, no una tarea que este skill ejecute.

- El producto de Comentarios es un objeto de **5 llaves exactas**: `img`, `name`, `desc`, `rela`, `estado`. Con 4 llaves el panel no lo interpreta.
- El `img` del producto usa URLs `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` que **solo nacen subiendo la imagen en el panel** (en los 225 endpoints de la API no hay subida). Copiar la URL de otra cuenta apunta a la cuenta de origen.
- **Par `array` / `Extendido`:** en workspaces migrados `[Comentarios] Productos` (array) está vacío y los productos viven en `[Comentarios] Productos extendido` (longtext) — verificado en un workspace real de producción (7 productos, venta diaria) en el Extendido. Leer el array y concluir "no hay productos" es un error. El tipo de un campo existente no se puede cambiar: hay que crear uno nuevo.
- `PUT /flow/set-bot-fields-by-name` usa la llave **`data`** (con `bot_fields` responde 400); `POST /flow/create-bot-field` usa **`var_type`** y exige `value` (si no, 422); `GET /flow/bot-fields` **PAGINA** y `per_page` se ignora.
- Al escribir por API, el valor va como string con `ensure_ascii=False, separators=(',',':')` (compacto): otro formato infla el conteo contra el techo sin cambiar el contenido. El JSON con `indent` que genera el script es para PEGAR en el panel; para API, compactarlo.
- **Escribir y RELEER siempre:** comparar el valor guardado contra el enviado es la única prueba real.
- **Corchetes `[enfermedad]` y `[ ]` del template son ILUSTRATIVOS**, no rellenables: `[enfermedad]` enseña al bot de venta la clase de pregunta de salud, y los `[ ]` son la checklist del modo captura. No tocarlos. Lo rellenable usa DOBLE llave `{{...}}` y lo valida el script.
- **Al clonar a otro cliente:** vaciar `[Comentarios] Productos` y el Extendido (catálogo del dueño) y jamás arrastrar `[Integraciones] Datos de integracion` (llaves en texto plano). Si se carga un producto de ejemplo para enseñar, va siempre con `estado` inactivo: enseña, no vende.

## Después: la ficha del producto (aparte)

Esto es referencia, no lo genera este skill. Cada producto se carga aparte en Chatea Pro con este formato (es lo que llena `{DESCRIPCION_PRODUCTO}`):

```
✨ [Nombre del producto] ✨
[Descripción del beneficio principal + características]

💰 Precios:
1 unidad: $XX.XXX
2 unidades: $XX.XXX
3 unidades: $XX.XXX

🚚 Envío gratis | Pago contra entrega
👉 [link del producto]
```

Ahí van la cantidad y los precios. Una tienda se configura una sola vez con este skill; los productos se cargan tantas veces como productos haya.

## Conexiones (skills hermanas)

Este skill configura **solo** la parte GENERAL del asistente de comentarios (prompts, país, negocio). Deriva cuando el pedido sea más amplio o más puntual:

- **Todos los asistentes a la vez** (comentarios + logístico + ventas WhatsApp + carritos) → `golden-chatea-pro-full-configuracion` (orquestador).
- **Asistente de ventas por WhatsApp** (Bot Fields, embudo, prompt maestro) → `golden-chatea-pro-config-ventas-wp`.
- **Asistente logístico / novedades preventivas** → `golden-chatea-pro-config-logistico`.
- **Carritos abandonados** → `golden-chatea-pro-config-carritos`.
- **Los TEXTOS del prompt de venta por producto** (no la estructura) → `golden-chatea-pro-prompt-ventas`.
- **Cargar/editar UN producto dentro del asistente de comentarios** (el objeto de 5 llaves `img/name/desc/rela/estado` de `[Comentarios] Productos`, para que el bot reconozca de qué producto habla cada comentario) → `golden-chatea-pro-producto-comentarios`. Esta skill deja la config general lista; esa hermana carga cada producto encima, uno por uno.

## Privacidad (skill compartible)

Este skill se comparte. Los prompts son genéricos y la información del negocio se pregunta al ejecutar; **nunca** hornees dentro de la skill datos reales de un negocio o cliente (WhatsApp, nombre de tienda, sede, cifras). La plantilla base usa valores de ejemplo obviamente ficticios que el intake sobrescribe siempre.
