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
| B1b | A | **El mismo chequeo sobre TODO lo demás que pagina** (subflujos, tags, segmentos, agentes IA, tareas IA, webhooks…), no solo bot fields. Un listado corto en cualquiera de ellos dice DUDA, no ausencia: lo que no aparece puede existir y no haberse medido. |
| B2 | A | **Campos de usuario contra su límite.** Hay un tope por workspace (visto `412/200` en rojo en el panel). Pasado el límite, dejan de crearse campos nuevos en silencio. |
| B3 | A | **Asistentes detectados por prefijo de campo**, no por lo que se supone instalado. Los prefijos conocidos son `[Comentarios]`, `[Ventas Wp]` / `[Producto Ventas Wp]`, `[Logistico]` / `[Logistica]`, `[Carritos IA]`, `[Remarketing IA]`, `[WhatsApp IA]`, `[Novedades]`, `[Minimax]`, `[Meta]`, `[Integraciones]`. **Un prefijo desconocido es un hallazgo, no ruido**: significa que hay un asistente o una versión que la skill todavía no sabe auditar, y hay que declararlo. |
| B4 | A | **Subflujos, tags, agentes IA, tareas IA y webhooks entrantes** contados. |
| B7 | A | **Un endpoint que respondió con error se DECLARA, no tumba la auditoría.** El extractor guarda el error del servidor tal cual, así que el valor deja de ser una lista y pasa a ser un diccionario de error. Iterarlo como lista revienta la corrida entera con un traceback, y **un 500 puntual de la API no puede costar el informe completo**. Se degrada: esa zona se marca como no medida, con su error citado, y el resto sigue. |
| B5 | A | **Ranuras de producto ocupadas.** Campos `[Producto Ventas Wp] N` con contenido. No se asume cuáles: se cuentan. El volcado de la semana pasada no sirve, esa cuenta cambia de un día para otro. |
| B6 | A | **Lo que FALTA, no solo lo que hay.** Contar prefijos presentes nunca puede contestar "está completa la instalación de este cliente". Se cruza contra la lista de esperados de `assets/asistentes-esperados.json`, que trae los campos firma de cada asistente: **ninguno presente = no instalado · algunos = instalado a medias**, que se comporta distinto según el camino que tome el flujo. Los opcionales del archivo (`[Remarketing IA]`, `[Minimax]`…) no se reportan como faltantes: aparecen en unos espacios y en otros no. |

## Bloque C · Los dos techos

Los dos se respetan a la vez. Detalle y tablas en `topes.md`.

| # | auto | Control |
|---|---|---|
| C1 | A | **Techo del bot field, ESCAPADO.** `len(json.dumps(valor)[1:-1])`. El flujo copia la config escapada: cada tilde ocupa 6 caracteres y cada emoji 12. **La frontera está MEDIDA en vivo entre 19.895, que sí dispara, y 23.266, que no.** De ahí salen dos severidades distintas, y confundirlas es gritar muerte donde hay riesgo: por encima de **19.895** es 🔴 MUERTO (pasó el último tamaño que se vio funcionar); entre **19.000 y 19.895** es 🟠, zona sin medir que se trata como riesgo. 19.000 es la alerta prudente, no una prueba de muerte. Los números viven en `assets/topes-nativos.json`, no en el código. |
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
| D3 | A | **Huérfanos en los dos sentidos.** Producto con campo cargado y **sin** entrada en el disparador, y entrada del disparador que apunta a un campo vacío o inexistente. **La severidad la decide el NEGOCIO, no la estructura**: un producto huérfano **con** `ids_de_anuncio` cargados es 🔴, porque cada clic de ese anuncio entra y no encuentra producto — es plata de pauta que no puede convertir; uno **sin** pauta es 🔵, porque no le llegan mensajes y hoy no se pierde nada. Criterio del dueño, medido: gritar rojo por productos sin pauta hace que el informe deje de leerse. |
| D3b | A | **El `estado` de la entrada manda sobre la severidad.** Una entrada del disparador que está `inactivo` **no puede estar MUERTA**: está apagada a propósito, no dispara y hoy no cuesta nada — es limpieza, no urgencia. Medido: 4 de las 5 entradas del disparador de Remarketing de Golden estaban inactivas y el auditor las gritó en rojo, imprimiendo `estado 'inactivo'` en su propia evidencia. Es el gemelo de la regla de D3 para huérfanos, y no se buscó al arreglarla la primera vez. **Al tocar una regla de severidad, buscar su gemelo antes de sellar.** |
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
| F3 | A | **Huecos sin llenar, por CLASE y en dos niveles de confianza.** La lista de nombres conocidos (`{{`, `TU_`, `XXX`, `[NOMBRE`, `lorem`, `ejemplo.com`) caza lo que ya sabemos; lo que la lista no ve se caza por forma. **Verbo de encargo** dentro del corchete (AQUÍ VA, PONER, FALTA, COMPLETAR, REEMPLAZAR) = 🔴 si el producto está activo, porque el cliente lee el corchete tal cual y si cae en el paso de cobro se pierde la venta ahí mismo. **Corchete en mayúsculas sostenidas** = 🔵 DUDA: medido contra los 12 productos de Golden, 3 de cada 4 eran plantilla viva del motor ([CATEGORÍA], [NOMBRE ASESORA]) — un auditor que acusa 3 falsos de 4 le enseña al dueño a ignorarlo. El corchete de variable en minúsculas (`[total]`, `[ciudad]`) no dispara. **Se busca en las hojas de TEXTO, no en el JSON crudo**: en el crudo, el `[` que abre un array parece un hueco. Caso real que lo pagó: un producto activo con los datos de pago sin llenar, invisible para la lista. |
| F4 | H | **Fugas de la cuenta de origen.** Nombres de otra tienda, otra asesora, otro dominio, otro WhatsApp, transportadoras de otro país, o la marca del profesor dentro del workspace de un alumno. **La fuga menos obvia son los nombres de producto y de paquetería dentro de los ganchos de venta del logístico**: son ejemplos que la IA imita. |
| F5 | A | **Coherencia de la ficha**: `precio` numérico y sin separadores raros · `moneda` que corresponde al país del espacio · `id_dropi` presente si el modelo es COD con Dropi · `estado` declarado · `tipo`. |
| F6 | A | **`multimedia` es lista, nunca cadena.** Escrita como cadena, el panel la muestra vacía y **al guardar la deja en `[]`**, sin un solo error. |
| F7 | A | **Las imágenes apuntan a esta cuenta.** Las URL de `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` llevan el ID de la cuenta que subió el archivo. Una imagen con el ID de OTRA cuenta apunta al origen, no al propio espacio. Las URLs externas (CDN de Shopify, CloudFront) sí están permitidas. |
| F8 | H | **Las URLs responden.** Se piden. Una imagen muerta en el embudo es un mensaje roto en el primer contacto. |
| F9 | H | **El prompt corresponde al producto real.** Precio, promesa, contenido del empaque y garantía contra la ficha real del producto. Lo que la caja dice no se inventa. |
| F10 | H | **Estructura contra el estándar.** Identidad, oferta, objeciones, cierre, restricciones. Ver `estandar-prompts.md`. |
| F11 | H | **Un prompt genérico que en realidad tiene horneado otro producto.** Caso real: el campo de fallback `producto_segundos.prompt_prompt` no era genérico, tenía el guion completo de un producto concreto y actuaba de fallback para todos los demás. |
| F12 | H | **País y lenguaje.** El país declarado manda: en México el código postal es requerido y no existe recolección en oficina; en Colombia al revés. **Cualquier país clonado de otra plantilla hereda el criterio equivocado.** Y la palabra "domicilio" significa el pedido en Colombia y la casa en México. |
| F13 | A | **La zona de agentes y tareas de IA.** El extractor baja los prompts de `/flow/ai-agents` y `/flow/ai-tasks`. Ahí vive texto que le llega al cliente y **ningún control de campos lo cubre**: los denominadores de F1, F2 y F3 lo excluyen por completo. Se audita aparte, con su propio denominador. |

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
| I1 | H | **La autoprueba pasó.** `autoprueba.py` siembra **30 defectos conocidos más 11 pruebas de comportamiento** (severidad por negocio, libro de decisiones, diff y su escapado real, colisión de claves, degradación, handoff y su filtro por severidad, sincronía B4/I3) y exige que los detecte todos. La cifra vive aquí y en el changelog de `SKILL.md`: al agregar un defecto se actualizan los dos, o el informe siguiente miente sobre su propia cobertura. **`auditar.py` no puede correr su propia autoprueba dentro de la misma corrida** (se corre aparte, con `python3 autoprueba.py`, antes de auditar datos reales): por eso es `H`, no `A` — es una condición que un humano confirma antes de publicar el informe, no algo que el código se audite a sí mismo en vivo. Si un auditor sale en verde a la primera contra datos reales, lo primero que se sospecha es el auditor. |
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

## Bloque J · Continuidad · lo que convierte la foto en vigilancia

Una auditoría que empieza de cero cada vez repite los mismos hallazgos hasta que el dueño deja
de abrirla. Estos dos controles son los que la vuelven algo que se mira a diario.

| # | auto | Control |
|---|---|---|
| J1 | A | **Diff contra la corrida anterior.** `--anterior <DUMP-viejo.json>` compara campo por campo y reporta creados, borrados y editados, con el delta de escapados. Un campo **borrado** es grave aunque no falle nada hoy: un flujo que lo referencie por `var_ns` queda apuntando al vacío. Y si un campo **cruzó** el techo entre las dos corridas, el cambio que lo cruzó es el sospechoso inmediato. |
| J2 | A | **Libro de decisiones del dueño.** `--decisiones <archivo.json>`. La clave se acepta en dos formas: **AMPLIA** (`control|campo`) silencia todos los hallazgos de ese campo y control, **FINA** (`control|campo::huella`) silencia uno solo, y el informe avisa cuando una amplia cubre más de uno. Las dos existen porque una sola decisión llegó a silenciar 5 hallazgos sin que nadie lo notara, y porque al añadir la huella se rompieron en silencio 4 de las 6 decisiones ya escritas. **Una clave que cambia de forma con una mejora del código no es estable, y el libro entero vale por su estabilidad.** Cada hallazgo tiene una `clave` estable (`control\|objetivo`) que **no cambia con los conteos** del título. Lo que el dueño ya resolvió sale en una sección aparte, con su motivo y su fecha, y no vuelve a contarse entre los hallazgos sin resolver. **Guarda:** si el libro declara un `espacio` que no coincide con el del DUMP, el auditor se detiene — un libro de otro espacio silenciaría fallas reales. |

### Cómo se escribe una decisión

```json
{
  "espacio": "<user_ns del espacio, ej. f000000>",
  "decisiones": [
    {
      "clave": "D3|huerfanos-sin-pauta",
      "motivo": "sin pauta activa no llegan mensajes; se registran cuando se les ponga pauta",
      "fecha": "2026-08-20",
      "reabrir_si": "se les carga un id de anuncio"
    }
  ]
}
```

`reabrir_si` es la parte que impide que el libro se vuelva una alfombra: dice en qué condición
la decisión deja de valer.

**Esto lo aplica el código, no la buena voluntad.** Una decisión sin `motivo` o sin `fecha`
**detiene la corrida** con el mensaje de cuáles están incompletas: silenciar un hallazgo sin
dejar rastro de quién lo decidió ni cuándo es exactamente el abuso que el libro podría habilitar.
Una decisión sin `reabrir_si` sí se acepta, pero el informe avisa que queda silenciada para
siempre.

### Handoff · `--handoff <archivo.md>`

Esta skill no escribe en Chatea, pero dejar el arreglo en prosa obliga al siguiente chat a
reconstruir el contexto entero. El handoff agrupa los hallazgos accionables **por la skill
dueña del campo** (inferida del prefijo) y encabeza cada paquete con las dos reglas que se
pagan caro: medir el escapado antes de escribir, y releer del servidor después.

Abre con **las preguntas que hay que contestar antes de tocar**: los hallazgos 🔵 que traen
acción concreta no se corrigen a ciegas ni se tiran a la basura — se contestan, y cada uno viene
con su `clave` lista para escribir la respuesta en el libro de decisiones.

## Bloque K · El ciclo, simulado antes de vivirlo

| # | auto | Control |
|---|---|---|
| K1 | A | **La decisión CADUCA sola cuando la situación cambia.** `reabrir_si` es prosa para humanos y ningún código puede evaluarla; lo que sí se puede verificar es si cambió la **evidencia**. Cada decisión guarda `evidencia_al_decidir` — la foto del día en que se tomó — y si la evidencia de hoy difiere, el hallazgo **vuelve a contar** con las dos fotos lado a lado. Sin esto, una decisión silencia para siempre: la de los huérfanos decía "reabre si se les carga un id de anuncio" y el día que se cargara habría seguido callada. Una decisión sin esa foto se avisa: **no puede caducar**. |
| K2 | A | **Los días se simulan, no se esperan.** `scripts/simular_dias.py` corre el ciclo sobre un espacio que evoluciona: se corta un campo desde el panel, un campo cruza el techo, se borra un campo, la API falla un día, se enciende pauta. Validar el ciclo dejándolo correr días reales descubre los fallos en producción; simularlos cuesta minutos. |
| K3 | A | **El banco tiene que MORDER.** Un día que pasa con el arreglo saboteado no prueba nada. Cada día del simulador se verifica con el arreglo vivo **y** con el arreglo roto: si pasa en los dos, la comprobación se está auto-aprobando por una vía que no prueba nada. Caso real: el día 7 registraba el producto, el hallazgo desaparecía y el test pasaba aunque la caducidad estuviera muerta. Se reescribió para que el hallazgo persista y solo cambie su evidencia. |
