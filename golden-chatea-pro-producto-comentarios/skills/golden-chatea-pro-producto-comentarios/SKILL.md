---
name: golden-chatea-pro-producto-comentarios
description: Configura UN producto dentro del asistente de COMENTARIOS de Chatea Pro — entrega el objeto de 5 llaves exactas (img, name, desc, rela, estado) listo para pegar, con la desc bajo el tope de 500 y el rela cargado de disparadores para que el bot reconozca de qué producto habla cada comentario de Facebook o Instagram. Parametrizado por los 7 países que acepta la plataforma. Úsalo SIEMPRE que el usuario quiera cargar, agregar, editar, revisar o arreglar un producto del asistente de comentarios, o diga cosas como "sube este producto a comentarios", "arma la ficha de producto para comentarios", "el bot responde con el producto equivocado", "no reconoce los comentarios de este anuncio", "actualiza el rela", "cambié los copys de Meta", "sale comentario no automatizado", "agrega este producto a Comentarios Productos", "ordena los productos del asistente de comentarios". Dispara también cuando peguen un JSON de productos de comentarios pidiendo revisión. La configuración GENERAL de ese asistente (prompts, negocio, país) la hace golden-chatea-pro-config-comentarios; el paquete de venta del producto en WhatsApp lo hace golden-chatea-pro-prompt-ventas.
---

# Producto del asistente de COMENTARIOS · Chatea Pro

<!-- skill v1.3.2 · 2026-08-21 (auditoría golden-skill-auditor, 960 ORO → 1000): 🟡 escritura-api.md
     tenía una frase telegráfica ("16.882/19.895 dispara; 19.922/23.266 no") que exigía reconstruir
     el criterio del techo con el número al lado; reescrita en dos viñetas explícitas (pasa con
     aviso / no pasa, techo). Verificado en vivo: el validador corrido contra el ejemplo horneado
     de `ejemplo-completo.md` reproduce exacto 461/500 desc, 24 disparadores, 1.146/1.272 —
     y corrido contra un caso plantado malo (desc vacía, estado en mayúscula, rela genérico y
     repetido entre productos) cae con los 5 errores esperados y exit 1. Sin hallazgos críticos:
     cero secretos, cero referencias rotas, las 8 skills hermanas citadas existen hoy. -->
<!-- skill v1.3.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v1.3 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v1.2 · 2026-08-07 · auditoría independiente golden-skill-auditor (762 BRONCE → reparada): 🔴 el medidor del techo usaba ensure_ascii=False, con lo que una tilde contaba 1 en vez de 6 y un emoji 2 en vez de 12 — certificaba en verde campos por encima de 20.000 (corregido en escapado() y en escritura-api.md); 🔴 el detector de genéricos dejaba pasar hongos/brillo y las preguntas de capa 5 sin producto (reescrito: marca dentro, o 2 palabras con contenido, o una de 7+; categorías nunca solas ni estando en el nombre); regla de la coma en los hooks; el tercer campo espejo (TOON) sube al camino principal; plan B si la compuerta no puede correr; --medir excluyente del posicional; el 500 anclado con honestidad a su fuente; techos desduplicados a una sola fuente -->
<!-- skill v1.1 · 2026-08-07 · pruebas en seco (producto nuevo MX + reparación de JSON roto CO): añadido el modo AUDITAR con tabla síntoma→causa, la compuerta de entrega, la regla de tildes, el presupuesto por producto, el catálogo de reglas de marca por categoría y el banco fonético; --medir en el validador; contención de disparadores y excepción de erratas de marca; resuelta la contradicción marcador-de-img vs validador -->
<!-- skill v1.0 · 2026-08-07 · fábrica: chat "✅ SKILL golden-chatea-pro-producto-comentarios" · cubre el hueco declarado en _BANDEJA-CENTRO-DE-MANDO.md (2026-08-07): config-comentarios decía "esto es referencia, no lo genera este skill" sobre la ficha de producto. Fuentes: BRIEFING-PARA-SKILLS.md + TOPES-NATIVOS-POR-CAMPO.md + dos workspaces vivos de referencia (uno propio con 7 productos, uno de plantilla) -->

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

### CAMPOS [Meta] = VALORES CALIENTES, NO INTERRUPTORES

Los bot fields `[Meta] Ver Contenido`, `[Meta] Agregar al carrito` y demás eventos de pixel los
**MUEVE EL FLUJO en tiempo real** mientras corren contactos — no son configuración estable. Caso
real (2026-08-08): se leyeron como "apagados" y cambiaron solos minutos después sin escritura de
nadie; la conclusión "el evento Comprar está apagado" tuvo que retractarse. **PROHIBIDO sacar
conclusiones de pauta o diagnóstico de una lectura suelta de esos campos**: se observan en ventana
(varias lecturas separadas en el tiempo) o se diagnostica el pixel en Meta directamente. Detalle:
memoria `reference_chatea_clonar_config_entre_espacios`.

Esta skill hace **una** cosa: el **producto** dentro del asistente de comentarios. No toca la
configuración del asistente (prompts, negocio, país, moderación) — eso es
`golden-chatea-pro-config-comentarios`. Es la gemela de `golden-chatea-pro-prompt-ventas`, que
hace el producto del lado de Ventas WhatsApp.

## El contrato: 5 llaves exactas, en este orden

```json
[{"img":"","name":"","desc":"","rela":"","estado":"activo"}]
```

| Llave | Qué es | Regla dura |
|---|---|---|
| `img` | imagen que el bot manda por privado | URL que responda 200. Ver §Imágenes |
| `name` | nombre comercial completo | como se llama en la tienda y en el anuncio |
| `desc` | todo lo que el bot sabe del producto; alimenta `{DESCRIPCION_PRODUCTO}` | **≤ 500 caracteres**, con tildes |
| `rela` | con qué texto se reconoce el comentario | lo que más pesa; ver `references/rela-metodo.md` |
| `estado` | `activo` o `inactivo` | minúscula, esos dos valores |

**Las 5 son obligatorias.** Un objeto de 4 llaves, sin `estado`, el panel **no lo interpreta** —
el producto queda invisible sin un solo mensaje de error. El campo entero es una **lista de
objetos**; un objeto suelto sin corchetes tampoco se renderiza.

Cada llave conserva su **tipo**: todo string. Un número o un booleano escrito ahí se pierde al
guardar desde el panel, igual que `multimedia` escrita como cadena en Ventas WhatsApp.

**Tildes: la `desc` y el `rela` van CON tildes.** La `desc` es el texto con el que el bot escribe
**en público**, y un acento comido se ve. Cada tilde cuesta 6 caracteres contra el techo escapado,
pero una `desc` de 500 con ~25 tildes son 150 escapados: irrelevante frente a los 20.000. Lo único
que se escribe **sin** tilde es el nombre del país en el campo `[Comentarios IA] País`.

## Dos modos de uso

**MONTAR** — no existe el producto, hay que crearlo. Vas al §Flujo de trabajo.

**AUDITAR / REPARAR** — ya hay productos cargados y algo falla. Es el caso más frecuente y el que
más dispara esta skill. **Empieza por esta tabla, no por el intake:**

| Síntoma que reporta el usuario | Causa casi siempre | Dónde se arregla |
|---|---|---|
| *"Comentario NO automatizado"* en todos los productos | el `array` está vacío porque la cuenta migró al `extendido` | `references/escritura-api.md` |
| *"Comentario NO automatizado"* solo en un producto | `rela` pobre: menos de 8 disparadores, o sin la capa 4 | `references/rela-metodo.md` |
| Responde bien hasta que cambió el anuncio | los copys de Meta rotaron y la capa 4 del `rela` quedó vieja | capa 4 |
| **Responde con el producto equivocado** | disparador repetido o contenido entre dos productos | el validador lo caza |
| Un producto captura comentarios ajenos | disparador genérico suelto (`base`, `crema`, `spray`) | capa 3 |
| El comentario genérico (*"precio?"*) es lotería | faltan hooks del post, o sobran productos en `activo` | capa 4 + `estado` |
| Un producto desapareció del panel | objeto de 4 llaves, tipo no-string, o `desc` cortada por el panel | el contrato de arriba |
| Texto que ayer estaba y hoy no | alguien guardó desde el panel y cortó lo que pasaba de tope | los dos techos |

**Lo primero, siempre: lee lo que hay en el servidor y pásalo por el validador.** El diagnóstico
sale de ahí, no de suponer. Después arreglas, y el resto del flujo es el mismo.

## Por qué el `rela` es la llave que decide si esto funciona

El asistente de comentarios **no tiene campo de ID de anuncio** — verificado en vivo el
2026-08-07: sus 5 bot fields no lo aceptan, y no va a aparecer buscando más. La **única** forma
que tiene el bot de saber de qué producto habla un comentario es emparejar el texto del
post/anuncio contra el `rela` de cada producto.

Consecuencias, y todas se pagan **en público, en el post del cliente**:

- `rela` pobre → *"🚨 Comentario NO automatizado"*. Nadie responde **y tampoco se elimina el
  comentario negativo**, porque el flujo aborta antes de clasificar.
- `rela` desactualizado → el bot ancla al producto equivocado y responde con el precio y el
  enlace de otro. Caso real: un comentario en un reel de un spray fue respondido con la ficha de
  una base de maquillaje.
- Un disparador genérico de una sílaba **secuestra comentarios ajenos**.

**Regla de mantenimiento que va con cada entrega:** cada vez que cambian, rotan o se reescriben
los copys de Meta de ese producto, hay que volver aquí y actualizar el `rela` con los hooks
nuevos. Es un paso del montaje de campañas, no una tarea opcional. Dilo siempre al entregar.

El método (las 5 capas, cuántos disparadores, cómo no fabricar colisiones) está en
`references/rela-metodo.md`. **Léelo antes de escribir un `rela`.**

## Los dos techos · esto es lo que rompe en silencio

| Techo | Qué mide | Cuánto |
|---|---|---|
| Campo nativo | la `desc` de **cada** producto | **500** |
| Bot field | el campo **entero**, escapado, con todos los productos | **20.000** (~17.000 crudos) |

Los dos fallan igual de callados. Pasarse del nativo funciona por API y se corta el día que
alguien abra el producto en el panel y guarde: un producto de Golden tenía la `desc` en 3.928
caracteres porque le habían metido el brief de venta completo, y se recortó a 483. Pasarse del bot
field responde `200 ok`, guarda el JSON **cortado** y el asistente muere; el rastro solo queda en
Panel → Registros de errores.

**Presupuesto operativo:** con 1 o 2 productos el techo del bot field es irrelevante. Con 7 —lo
normal en una cuenta que vende— el presupuesto real es de **~2.500 escapados por producto**. Si te
acercas, recorta las `desc` antes que los `rela`: la `desc` la usa el bot *después* de reconocer el
producto; el `rela` es lo que decide si llega a reconocerlo.

La fórmula, los endpoints y el porqué están en `references/escritura-api.md`. No estimes a ojo:
el validador mide los dos.

## Flujo de trabajo

### 1 · Intake mínimo (decide tú, no interrogues)

Pide **en un solo mensaje** lo que no puedas deducir, y propón defaults marcados como supuesto
para el resto.

**Obligatorio:** **país** (uno de los 7), **nombre del producto**, **precio de al menos 1 unidad**.

**Se deduce o se propone:** moneda y formato del país · palabras locales (`references/paises.md`) ·
`estado` · las reglas de marca según la categoría (`references/desc-plantilla.md`) · los
disparadores del `rela` (los escribe la skill).

**Se pide solo si existe:** URL de la ficha o del anuncio · foto · los **copys de Meta activos** ·
la URL de la imagen.

Sin URL ni copys, construye igual y entrega el `rela` **marcado como provisional en la capa 4**,
diciendo que se completa en cuanto existan los anuncios.

> Si lees una URL con un scraper, comprueba que el dato **responde a lo que pediste** antes de
> meterlo en la ficha. Un `statusCode: 200` no prueba nada: los extractores alucinan producto,
> precio y reseñas de páginas que no cargaron. Aquí ese dato falso lo dice el bot en público.

### 2 · `estado`

- **`activo`** — producto real, vendiéndose, con anuncios corriendo.
- **`inactivo`** — producto de **ejemplo** en una instalación nueva, producto **sin pauta activa**,
  o descontinuado que se conserva para que sus comentarios viejos sigan reconociéndose sin vender.

En una instalación nueva de cliente, el producto de muestra va **siempre `inactivo`**: enseña cómo
se configura, no vende. Y cuantos menos `activo` haya, menos lotería en el comentario genérico:
por encima de ~6 activos, cada uno de más es un candidato más al que el bot puede anclar mal.

### 3 · Escribir cada llave

- `references/desc-plantilla.md` — el esqueleto de los 500, el **catálogo de reglas de marca por
  categoría** (cosmético, aparato eléctrico, suplemento, ropa, deportivo) y el método de recorte.
- `references/rela-metodo.md` — las 5 capas, el banco de erratas y la regla anti-colisión.
- `references/paises.md` — moneda, formato y vocabulario de los 7 países.

### 4 · Compuerta: el validador en verde, o no se entrega

```bash
V=~/.claude/skills/golden-chatea-pro-producto-comentarios/scripts/validar_producto.py
python3 "$V" productos.json          # valida el array completo
python3 "$V" --medir borrador.txt    # mide una desc suelta mientras la recortas
python3 "$V" productos.json --json   # mismo veredicto en JSON, para encadenar
```

**Esto no es una recomendación, es una condición de entrega.** Mientras el validador salga en
rojo, no entregas el JSON ni lo escribes en el workspace: corriges y vuelves a correr. Un producto
con una `desc` de 533 se ve perfecto hoy y desaparece dentro de tres meses, y para entonces nadie
recuerda quién lo tocó.

Usa `--medir` **mientras** recortas, no al final: mide una `desc` suelta contra los 500, te dice
por cuánto te pasas y qué línea pesa más. Recortar a ojo cuesta cuatro intentos; medir cuesta uno.

El validador comprueba las 5 llaves y su orden, los tipos, `desc ≤ 500`, `estado`, los dos techos,
los disparadores repetidos **o contenidos** entre productos, los genéricos, y devuelve el **JSON
compacto listo para pegar** (`ensure_ascii=False`, `separators=(',',':')` — otro formato infla el
campo sin cambiar el contenido). `--medir` y el archivo JSON son excluyentes: cada uno por
separado, para que nunca creas que validaste cuando solo mediste.

**Si el validador no puede correr** (no hay `python3`, el script no está), no entregues como si
hubiera pasado: dilo explícitamente, comprueba a mano los cuatro puntos que más rompen —las 5
llaves, `desc ≤ 500` con `len()`, `estado` en minúscula, y ningún disparador repetido entre
productos— y entrega marcando **"sin verificar con el validador"**. Un entregable honestamente
marcado sirve; uno que aparenta estar validado, no.

### 5 · Dónde se pega

El producto vive en el bot field **`[Comentarios] Productos`** (tipo `array`) — **ese es el que
lee el flujo**. Pero en una cuenta pueden convivir **tres** campos con nombres parecidos:

| Campo | Qué es |
|---|---|
| `[Comentarios] Productos` (`array`) | **el que lee el flujo** · aquí va el producto |
| `[Comentarios] Productos extendido` (`longtext`) | espejo de la migración · **copia, no traslado** |
| `[Comentarios] TOON Productos` (`longtext`) | espejo comprimido · **puede estar desfasado** |

**Lee los tres y compáralos antes de escribir.** Si el `extendido` tiene datos, la copia va también
ahí: si cambia un precio hay que tocar los dos. El `TOON` se ha encontrado nombrando un producto
que ya no existía — si difiere de los otros, pregunta cuál es la fuente de verdad en vez de elegir
tú. Escribir el campo equivocado duplica o rompe respuestas en público. (Los hechos verificados
sobre cada campo, en `references/escritura-api.md`.)

**Si vas a escribir por API, lee `references/escritura-api.md`** (endpoints, la llave `data`, la
paginación, el respaldo previo y la relectura obligatoria). Dos cosas que no pueden fallar:
**`POST` al editar devuelve 200 y NO escribe** — se edita con `PUT`; y el estado vivo se lee **del
servidor**, nunca de un respaldo local.

**Si no vas a escribir por API**, sáltate esa referencia: entrega el JSON compacto en un bloque
copiable, di en qué campo o campos va, y lista lo que quedó pendiente.

## Imágenes · la trampa del ID de cuenta

`img` acepta URLs externas (el CDN de Shopify está probado y responde 200). Pero en producción
casi todos los productos usan `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/archivo.jpg`, y
**esas URLs solo nacen subiendo la imagen desde el panel**: en los 225 endpoints de la API no hay
ninguno de subida.

Ese `<ID_DE_CUENTA>` es la trampa: **copiar la URL de una cuenta a otra apunta a la cuenta de
origen**. Nunca reutilices el `img` de un workspace en otro.

Si el cliente todavía no tiene la imagen subida, deja `"img": ""` y **repórtalo aparte** como
pendiente, con la instrucción de qué subir y dónde. No inventes una URL ni copies una ajena. (El
validador también acepta un marcador entre corchetes —`"[AQUÍ VA LA URL DE LA IMAGEN]"`— y lo
reporta como pendiente; sirve para un borrador, pero **nunca se escribe así en el workspace**,
porque el bot mandaría ese texto como si fuera una imagen.)

## Antes de dar por configurado un producto

1. Las **5 llaves**, en orden, todas string.
2. `desc` ≤ 500, con tildes, y termina con las **reglas de marca** de su categoría.
3. `rela` con las 5 capas, incluidos los **hooks literales de los copys que corren ahora**.
4. Ningún disparador genérico suelto, ni repetido, ni **contenido** en el de otro producto.
5. Precios reales y **coincidentes** con los del mismo producto en Ventas WhatsApp.
6. Moneda, formato y vocabulario del país.
7. `estado` correcto; los productos sin pauta, en `inactivo`.
8. `img` responde y no es de otra cuenta.
9. El campo completo bajo **19.000 escapados**.
10. **Validador en verde.**
11. Escrito y **releído del servidor**, comparando byte a byte.

## Fronteras (skills hermanas)

Config general del asistente de comentarios → `golden-chatea-pro-config-comentarios` · producto y
paquete de venta en WhatsApp → `golden-chatea-pro-prompt-ventas` · logístico y direcciones →
`golden-chatea-pro-config-logistico` y `golden-chatea-pro-validacion-direcciones` · carritos →
`golden-chatea-pro-config-carritos` · instalación completa de los 4 asistentes →
`golden-chatea-pro-full-configuracion` (el orquestador llama a esta skill para cargar productos) ·
copys de anuncios → `golden-copywriting` · pauta → `golden-ads`. Cuando esos copys cambien, se
vuelve **aquí** a actualizar el `rela`.

## Privacidad

Skill compartible: **nunca hornees en sus archivos datos reales de un negocio** (tienda, asesora,
precios, WhatsApp, URLs con ID de cuenta, cifras). Los ejemplos de las referencias son ficticios a
propósito. Un dato real incrustado en un archivo de la skill es un error: quítalo.

## Archivos de referencia

- `references/rela-metodo.md` — **el método del `rela`**: las 5 capas, el banco de erratas, la
  regla anti-colisión y qué hacer con los emojis. Léelo antes de escribir cualquier `rela`.
- `references/desc-plantilla.md` — los 500 caracteres: esqueleto, **catálogo de reglas de marca
  por categoría**, método de recorte y qué material va en el prompt de ventas y no aquí.
- `references/paises.md` — los **7 países**: moneda y formato, vocabulario, y el detalle
  Colombia/México para quien trabaje esos dos.
- `references/escritura-api.md` — **solo si vas a escribir por API**: endpoints, paginación,
  respaldo, relectura, y los tres campos de comentarios que se confunden.
- `references/ejemplo-completo.md` — un producto ficticio horneado, con sus medidas reales. Vara
  de calidad de tu salida.
- `scripts/validar_producto.py` — **el validador y la compuerta**. También `--medir` para recortar
  una `desc` sin adivinar.
