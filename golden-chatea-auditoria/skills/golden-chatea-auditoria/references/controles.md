# Catálogo de controles · auditoría de un espacio de Chatea Pro

Se recorre **entero**. Revisar "lo importante" está prohibido: o se corren todos, o se declara
en el informe cuáles no se corrieron y por qué.

Cada control lleva: qué mide · cómo se mide · por qué existe (el caso real que lo pagó) ·
severidad si falla. La columna **auto** dice si lo corre `auditar.py` (A) o si es lectura
humana obligatoria (H).

---

## Bloque A · Identidad y acceso

| # | auto | Control |
|---|---|---|
| A1 | A | **El token responde.** `GET /me` da 200. Si da 401, el flujo apunta a una copia vieja del token, no es que la API esté caída. Si da Cloudflare 1010, falta el User-Agent de navegador. |
| A2 | A | **La identidad sale del servidor.** El espacio es el que dice `/me` y el prefijo `user_ns` de los campos, **nunca el nombre del archivo del token.** Caso real: un resumen de índice le colgó el ns de Golden a un cliente de México durante semanas. El informe abre nombrando el espacio medido. |
| A3 | A | **El espacio corresponde al negocio que se dijo auditar.** Se cruza contra país, moneda y correo de la tienda. Un espacio con `País = MEXICO` y precios en COP es una plantilla mal clonada. |
| A4 | A | **Canales conectados.** `GET /workspace-settings/channels`. Un canal desconectado deja muerto al asistente que depende de él, sin error en la config. |
| A5 | H | **El token de Meta está vivo.** Si los comentarios dejaron de responder y la config está sana, la causa típica es el token de Meta caído, no el prompt. Se verifica en el panel; si no se pudo, se declara. |

## Bloque B · Inventario (el denominador)

| # | auto | Control |
|---|---|---|
| B1 | A | **Campos de bot contados con la paginación agotada.** Se compara el número de campos traídos contra `meta.total`. Si no cuadra, el informe **se detiene**: un denominador incompleto invalida todo lo demás. |
| B2 | A | **Campos de usuario contra su límite.** Hay un tope por workspace (visto `412/200` en rojo en el panel). Pasado el límite, dejan de crearse campos nuevos en silencio. |
| B3 | A | **Asistentes detectados por prefijo de campo**, no por lo que se supone instalado. Los prefijos conocidos son `[Comentarios]`, `[Ventas Wp]` / `[Producto Ventas Wp]`, `[Logistico]` / `[Logistica]`, `[Carritos IA]`, `[Remarketing IA]`, `[WhatsApp IA]`, `[Novedades]`, `[Minimax]`, `[Meta]`, `[Integraciones]`. **Un prefijo desconocido es un hallazgo, no ruido**: significa que hay un asistente o una versión que la skill todavía no sabe auditar, y hay que declararlo. |
| B4 | A | **Subflujos, tags, agentes IA, tareas IA y webhooks entrantes** contados. |
| B5 | A | **Ranuras de producto ocupadas.** Campos `[Producto Ventas Wp] N` con contenido. No se asume cuáles: se cuentan. El volcado de la semana pasada no sirve, esa cuenta cambia de un día para otro. |

## Bloque C · Los dos techos

Los dos se respetan a la vez. Detalle y tablas en `topes.md`.

| # | auto | Control |
|---|---|---|
| C1 | A | **Techo del bot field, ESCAPADO.** `len(json.dumps(valor)[1:-1])`. El flujo copia la config escapada: cada tilde ocupa 6 caracteres y cada emoji 12. El techo práctico de un `array` es **19.000 escapados**; por encima, el asistente **deja de responder sin un solo error visible**. Medido: 19.895 dispara, 23.266 no. |
| C2 | A | **Alerta de proximidad.** Por encima del 90% del techo es 🟠 MUERTE ANUNCIADA: la próxima línea que alguien agregue lo corta solo. Caso real: `[Comentarios] Configuracion General` a 483 caracteres del techo. |
| C3 | A | **Tope nativo del campo del formulario.** Escribir por encima por API funciona y no da error, pero el día que alguien abra ese formulario en el panel y guarde, **el campo se corta y se pierde el texto**. Tabla completa en `topes.md`. |
| C4 | A | **Tipo del campo.** `text` y `array` topan en 20.000; `longtext` en 500.000. Un campo de configuración que sigue siendo `array` y va por el 80% es un candidato a migrar. **El tipo es inmutable**: no se cambia ni por UI ni por API, hay que crear uno nuevo y repuntar la referencia. |
| C5 | A | **Pares `X` / `X Extendido`.** Los espacios migrados dejan el `array` vacío y los datos en el `longtext`. **Leer el array y concluir "no hay productos" es un error**, y leer solo el Extendido cuando los dos están poblados también. Se reportan los tres casos: solo array · solo Extendido · **los dos poblados** (🟠, hay que saber cuál lee el flujo). |
| C6 | A | **Truncada silenciosa.** Un valor que no parsea como JSON estando declarado `array`/`longtext` es señal de contenido cortado por haberse pasado del techo con un `200 ok`. |

## Bloque D · Disparadores · lo que hace que el asistente arranque

Este bloque es el que más muertes silenciosas produce. Un producto puede estar impecable y no
existir para el bot.

| # | auto | Control |
|---|---|---|
| D1 | A | **La palabra clave vive en DOS sitios y tienen que ser idénticas byte a byte**: `[Producto Ventas Wp] N.activadores_del_flujo.palabras_clave` y la entrada `keyW` del mismo producto en `[Ventas Wp] Disparador de productos Extendido`. Si difieren **aunque sea en un acento**, el producto no arranca. Caso real: `informacion` contra `información`. 🔴 |
| D2 | A | **El disparador no admite caracteres de 4 bytes.** Un emoji lo corrompe y el bot no arranca nunca. Validación: `[c for c in texto if ord(c) >= 0x10000] == []`. 🔴 |
| D3 | A | **Huérfanos en los dos sentidos.** Producto con campo cargado y **sin** entrada en el disparador = cargado y muerto. Entrada en el disparador que apunta a un campo **vacío o inexistente** = disparo al vacío. Los dos son 🔴. |
| D4 | A | **Coherencia de estado.** `estado` del producto dentro del campo contra `estado` de su entrada en el disparador. Uno activo y el otro inactivo es ambigüedad, y la ambigüedad se resuelve preguntando. |
| D5 | A | **Las siete ranuras.** `keyW` e `idAd` son siete ranuras separadas por coma. Un valor con más o menos de siete ranuras está malformado. |
| D6 | A | **IDs de anuncio.** Se listan los `idAd` cargados por producto. Vacíos no es necesariamente un fallo (así están varios en producción), pero **un producto que se está pautando y tiene la ranura vacía pierde la atribución**: se reporta como DUDA para contrastar contra las campañas activas. |
| D7 | H | **El disparador apunta a un subflujo VIVO.** Reinstalar un asistente recrea los subflujos con `ns` nuevo y **el disparador se queda apuntando al viejo**, en silencio. Se cruza el `ns` referenciado contra los subflujos que devuelve la API; lo que no se pueda cruzar por API se verifica en el panel o se declara no verificado. 🔴 |
| D8 | H | **Palabra clave contra el texto que manda el anuncio.** El botón del anuncio de Meta manda un texto predefinido ("Hola quiero información y precio de X"). Si la palabra clave del producto no es exactamente ese texto, el clic del anuncio no entra. Se compara contra el creativo real. |

## Bloque E · Interruptores

Un prompt perfecto detrás de un interruptor apagado no hace nada, y **ningún chequeo del
contenido lo detecta**. Caso real que lo pagó: un prompt de validación de direcciones de 7.243
caracteres, correcto y cargado, con `evaluar_direccion = "no"`.

| # | auto | Control |
|---|---|---|
| E1 | A | **Inventario de TODOS los interruptores**: toda llave `activar*`, `esta_activo`, `habilitar*`, `evaluar_*`, `activo`, `habilitado`, y los campos de bot `boolean`. Se listan con su valor, agrupados por asistente. No se juzgan solos: se comparan contra la referencia. |
| E2 | A | **Apagados sospechosos**: interruptor en `no`/`false` que gobierna un contenido lleno. Un prompt de 7.000 caracteres detrás de un `no` es 🔴. |
| E3 | A | **`voz_con_ia` de cada producto.** Puede traer una `api_key` de ElevenLabs **de la cuenta de origen** con `habilitar: si`. Copiar un producto "exacto" copia la credencial. Se reporta la existencia y el largo, **nunca el valor**. 🟡 |
| E4 | A | **Eventos de `[Meta]`.** En cero no es un defecto por sí solo (así están en producción), pero se listan para contrastar. |

## Bloque F · Contenido de los prompts · producto por producto

Se leen **enteros**, uno por uno. No se muestrean. El estándar está en `estandar-prompts.md`.

| # | auto | Control |
|---|---|---|
| F1 | A | **Acentos y mojibake EN EL RENDER.** Se buscan las secuencias rotas (`Ã¡`, `Ã©`, `â€`, `Ã±`…) y los caracteres de reemplazo. Un acento roto suele ser cien: cuando aparece uno, se busca **la clase**, no el caso. |
| F2 | A | **Sin signos de apertura.** Regla de Golden: nada de `¿` ni `¡` en el texto que le llega al cliente. |
| F3 | A | **Placeholders sin reemplazar**: `{{`, `TU_`, `XXX`, `[NOMBRE`, `<...>`, `lorem`, `ejemplo.com`. |
| F4 | A | **Fugas de la cuenta de origen.** Nombres de otra tienda, otra asesora, otro dominio, otro WhatsApp, transportadoras de otro país, o la marca del profesor dentro del workspace de un alumno. **La fuga menos obvia son los nombres de producto y de paquetería dentro de los ganchos de venta del logístico**: son ejemplos que la IA imita. |
| F5 | A | **Coherencia de la ficha**: `precio` numérico y sin separadores raros · `moneda` que corresponde al país del espacio · `id_dropi` presente si el modelo es COD con Dropi · `estado` declarado · `tipo`. |
| F6 | A | **`multimedia` es lista, nunca cadena.** Escrita como cadena, el panel la muestra vacía y **al guardar la deja en `[]`**, sin un solo error. |
| F7 | A | **Las imágenes apuntan a esta cuenta.** Las URL de `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` llevan el ID de la cuenta que subió el archivo. Una imagen con el ID de OTRA cuenta apunta al origen, no al propio espacio. Las URLs externas (CDN de Shopify, CloudFront) sí están permitidas. |
| F8 | H | **Las URLs responden.** Se piden. Una imagen muerta en el embudo es un mensaje roto en el primer contacto. |
| F9 | H | **El prompt corresponde al producto real.** Precio, promesa, contenido del empaque y garantía contra la ficha real del producto. Lo que la caja dice no se inventa. |
| F10 | H | **Estructura contra el estándar.** Identidad, oferta, objeciones, cierre, restricciones. Ver `estandar-prompts.md`. |
| F11 | H | **Un prompt genérico que en realidad tiene horneado otro producto.** Caso real: el campo de fallback `producto_segundos.prompt_prompt` no era genérico, tenía el guion completo de un producto concreto y actuaba de fallback para todos los demás. |
| F13 | A | **La zona de agentes y tareas de IA.** El extractor baja los prompts de `/flow/ai-agents` y `/flow/ai-tasks`. Ahí vive texto que le llega al cliente y **ningún control de campos lo cubre**: los denominadores de F1, F2 y F3 lo excluyen por completo. Se audita aparte, con su propio denominador. |
| F12 | A | **País y lenguaje.** El país declarado manda: en México el código postal es requerido y no existe recolección en oficina; en Colombia al revés. **Cualquier país clonado de otra plantilla hereda el criterio equivocado.** Y la palabra "domicilio" significa el pedido en Colombia y la casa en México. |

## Bloque G · Seguridad

| # | auto | Control |
|---|---|---|
| G1 | A | **Las integraciones devuelven las credenciales en TEXTO PLANO.** `GET /integration/openai\|shopify\|dropi\|calude\|xai\|s3storage` entrega la llave completa. Cualquiera con el token del bot lee todas las llaves del workspace. El extractor las **redacta**: guarda si hay valor y de qué largo, nunca el valor. **Nunca darle un token de bot a un alumno o cliente "solo para configurar".** |
| G2 | A | **La integración apunta a donde debe.** Caso real: la de Shopify del espacio de Golden apuntaba a un dominio `myshopify.com` que no es la tienda. |
| G3 | A | **Credenciales dentro de bot fields.** Tokens que viven como valor de un campo (el de Dropi vive así). Se reporta su existencia y largo para saber que están, sin exponerlos. |
| G4 | H | **Rotación.** Si el token se compartió alguna vez, las llaves que ese token podía leer se consideran expuestas y se rotan. La nota de la rotación entra al informe. |

## Bloque H · Cruces externos

Opcionales según qué llaves haya. **Si no se corren, se declaran como no verificados**; no se
omiten en silencio.

| # | auto | Control |
|---|---|---|
| H1 | H | `id_dropi` de cada producto y de cada upsell existe en Dropi y está activo. |
| H2 | H | Precio del prompt contra el precio real de la tienda. |
| H3 | H | `idAd` contra los anuncios activos de Meta: anuncio corriendo sin ranura cargada, y ranura cargada apuntando a un anuncio que ya no existe. |
| H4 | H | Las tres empresas de Golden son independientes: un espacio no hereda datos de otro. |

## Bloque I · Cordura del propio auditor

| # | auto | Control |
|---|---|---|
| I1 | A | **La autoprueba pasó.** `autoprueba.py` siembra 29 defectos conocidos y exige encontrarlos todos. Si un auditor sale en verde a la primera contra datos reales, lo primero que se sospecha es el auditor. |
| I2 | A | **Cero solo prueba algo si cubrió todo.** Un bloque con cero hallazgos y cobertura parcial no se reporta como sano: se reporta la cobertura. |
| I3 | A | **Todo lo que entra al DUMP se audita o se declara.** Se cruzan las zonas extraídas contra las que tienen control. Una zona extraída y sin auditar no es una zona sana: es una zona sobre la que no se midió nada, y su silencio se lee como salud. |
| I4 | A | **Ausencia no es prueba.** Que un campo no aparezca en el DUMP no significa que no exista: puede ser paginación sin agotar o un endpoint que devuelve vacío. Se distingue "medido y vacío" de "no medido". |

---

## Cuatro clases de fallo que ya se pagaron, y que hay que buscar al ampliar la skill

Salieron de una verificación adversarial de la propia skill. No son casos, son **clases**:

1. **Redactar por nombre de llave no protege nada.** El secreto viaja dentro del `value` de un
   bot field, y `value` no es un nombre sensible. Un mismo archivo tapaba la llave de Dropi en
   `/integration/dropi` y la dejaba en claro, con el mismo largo, dentro de
   `[Integraciones] Datos de integracion`. **Se busca por patrón de valor** (`sk-`, `sk_`,
   `eyJ`, `EAA`, `shpat_`), nunca solo por nombre.
2. **El detector solo mira donde le sembraron el defecto.** Cada control con una constante
   estructural es candidato: "más de una cuenta" no ve un espacio clonado entero, "dos niveles
   de anidamiento" no ve un interruptor en la raíz, "dos nombres de campo" no ve el tercer
   disparador. **El fixture describe el caso conocido y el código termina codificando el
   fixture.**
3. **Lo extraído que nadie audita.** Toda zona que entra al DUMP aparece en la cobertura, aunque
   sea como no verificada.
4. **El número de revisados no puede ser el número de hallazgos.** Un `cubre(..., N)` donde N
   solo crece al fallar dice "cero objetos revisados" cuando todo salió bien.
