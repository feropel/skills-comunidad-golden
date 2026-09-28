---
name: golden-chatea-pro-producto-comentarios
description: >-
  Configura UN producto dentro del asistente de COMENTARIOS de Chatea Pro: entrega el objeto
  de 5 llaves exactas (img, name, desc, rela, estado) listo para pegar, con la desc bajo el
  tope de 500 y el rela cargado de disparadores para que el bot reconozca de qué producto
  habla cada comentario de Facebook o Instagram. Parametrizado por los 10 países que acepta
  la plataforma. Úsalo SIEMPRE que el usuario quiera cargar, agregar, editar, revisar o
  arreglar un producto del asistente de comentarios, o diga cosas como "sube este producto a
  comentarios", "arma la ficha de producto para comentarios", "el bot responde con el
  producto equivocado", "no reconoce los comentarios de este anuncio", "actualiza el rela",
  "cambié los copys de Meta", "sale comentario no automatizado", "agrega este producto a
  Comentarios Productos", "ordena los productos del asistente de comentarios". Dispara
  también cuando peguen un JSON de productos de comentarios pidiendo revisión.
---

**Fábrica:** chat «✅ SKILL golden-chatea-pro-producto-comentarios»
# Producto del asistente de COMENTARIOS · Chatea Pro

<!-- Actas anteriores a la v1.7 en `references/bitacora.md`. Se mudaron porque el cuerpo pasaba
     de 500 líneas; sus artefactos ejecutables se comprobaron fuera del changelog antes de mover. -->
<!-- skill v1.11.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v1.11 · 2026-09-22 (fábrica) · LA CONTRAPRUEBA TENIA EL MISMO FALLO QUE VINO A CAZAR.
     La fábrica de config-comentarios aplicó la lección a su banco, encontró 9 pruebas midiendo
     texto (3 con `not in`, que es el modo peor: un `in` roto da ROJO y se ve; un `not in` roto
     da VERDE y no se ve nunca) y de paso me atribuyó una defensa que yo NO tenía. Lo medí:
     · Mis 3 checks con negación SI tienen cobertura positiva cruzada. Ahí estaba limpio.
     · 🔴 Mi contraprueba usaba tres `str.replace` PELADOS, cero guardas. Si el texto buscado
       cambia, el replace no hace nada, la copia queda INTACTA y el paso B pasa en verde
       "tolerando una re-redacción" que nunca ocurrió. La prueba mentiría sin dar un error.
     · 🔴 Y no comprobaba que su sabotaje SABOTEARA. Un sabotaje inerte da la misma señal que un
       banco decorativo —todo verde— y llevan a conclusiones OPUESTAS.
     Arreglado: `sustituye()` aborta con exit 2 si no encuentra el texto; el paso B verifica que
     la conducta NO cambió (mismo número de errores antes y después); y el paso C mide que el
     sabotaje bajó los errores ANTES de juzgar al banco. Medido: B conducta 1 -> 1 intacta,
     C sabotaje 1 -> 0 efectivo, banco rojo. Las tres en verde. -->

<!-- skill v1.10 · 2026-09-22 (fábrica) · EL FALLO SIMÉTRICO, cazado por config-comentarios.
     Corregí el techo de GUARDADO porque su número venía heredado de campos [Producto Ventas Wp],
     y canonicé la ley "un tope medido en un campo no se traslada a otro aunque los dos sean
     array". Y acto seguido DEJÉ EN PIE el otro número heredado: las dos observaciones de
     EJECUCIÓN (19.895 dispara / 23.266 no) salen DEL MISMO CAMPO AJENO. Arreglé la mitad que
     dolió y conservé la que todavía no había dolido.
     · El aviso del escapado ahora DECLARA que su frontera es heredada y dice que para el campo
       de comentarios el límite de ejecución no está medido ni por arriba ni por abajo. Y dice
       explícitamente "no recortes por este número".
     · Queda escrito el experimento que cierra la ventana: la configuración que corre hoy en
       producción mide 21.457 escapados, o sea DENTRO de la zona desconocida. La prueba del post
       ya no responde una pregunta sino dos — si dispara, la frontera de ESTE campo sube por
       encima de 21.457 con un dato propio; si no dispara, hay techo por debajo y esa config hay
       que recortarla ~1.429 caracteres. (Ratio de ese texto: 1,0938 escapados por crudo; sube con
       la densidad de tildes, así que no es constante.)
     EL BANCO MEDÍA LA REDACCIÓN, NO EL COMPORTAMIENTO. El caso 18 se puso rojo el mismo día solo
     porque cambié el texto de un error. Eso era una CLASE: casi todos los checks hacían substring
     de la frase. Reescritos sobre `--json`, comprobando qué HACE el validador (error contra aviso,
     exit code) y anclando el motivo a una palabra estable (la llave afectada), nunca a la frase.
     Caso 20 nuevo: el veredicto viaja estructurado. 21 de 21.
     Y NACE scripts/contraprueba.py, porque un banco también se verifica: sobre una copia en
     tmpdir reescribe la redacción de dos errores (tiene que seguir en VERDE) y luego rompe el
     comportamiento (tiene que ponerse en ROJO). Medido: las dos direcciones correctas. -->

<!-- skill v1.9 · 2026-09-22 (fábrica) · 🔴 EL TECHO ESTABA MAL Y MI VALIDADOR RECHAZABA
     TRABAJO BUENO. Me corrigió la fábrica de config-comentarios con medición de primera mano
     (escribir y releer del servidor), y al contrastar las CINCO mediciones de la casa salió algo
     mejor que cualquiera de las dos posturas: NO HAY UN TECHO, HAY DOS, y se observan con
     pruebas distintas.
     · Observando GUARDAR y RELEER (22-sep, campo array de comentarios): 13.004 crudos guarda ·
       19.617 crudos / 21.457 escapados guarda y se relee IDÉNTICO byte a byte · 20.811 crudos da
       error 500 y el campo queda VACÍO en el servidor, no truncado.
     · Observando SI EL BOT DISPARA al ejecutarse (BRIEFING, agosto): 19.895 escapados dispara ·
       23.266 escapados NO dispara.
     Si el techo fuera "20.000 escapados", el campo de 21.457 escapados que HOY CORRE EN
     PRODUCCIÓN no existiría. Y si fuera crudos, el de 19.922 crudos habría disparado y no lo
     hizo. Conclusión: GUARDAR topa en ~20.000 CRUDOS; EJECUTAR tiene un límite propio más
     estrecho cuya única evidencia está en escapados, y la zona entre 19.895 y 23.266 NO está
     medida.
     QUÉ CAMBIA EN EL VALIDADOR: crudos BLOQUEA (medición directa de escritura), escapado solo
     AVISA con su explicación. Antes el error iba contra escapados, o sea que mi compuerta habría
     rechazado una configuración que está funcionando. Un guardarraíl que bloquea trabajo bueno
     cuesta más que no tenerlo, porque nadie duda de él y se empieza a recortar lo que sí cabía.
     DE DÓNDE VENÍA MI NÚMERO: el "20.000 escapados" se midió sobre campos [Producto Ventas Wp],
     no sobre el de comentarios. Un tope medido en un campo NO se traslada a otro aunque los dos
     sean array. Y lo que el panel ANUNCIA no es medición de comportamiento: dice 20.000 sin decir
     la unidad, y asumir escapados fue una inferencia mía.
     ENTRAN ADEMÁS, de la misma fábrica: la SUMA de los topes del panel NO es el presupuesto —
     suman 24.100 y el campo aguanta 20.000, el panel valida caja por caja y nunca la suma, y el
     500 aborta el campo ENTERO; el JSON gasta más que el contador del panel (cada salto de línea
     cuenta 2, y la estructura añade ~356, o sea ~800 de desfase); y el contador del panel cuenta
     en UTF-16, así que con emojis no coincide con Python.
     BANCO: el caso 18 se puso en rojo solo porque cambié el mensaje del error, e hizo su trabajo.
     Actualizado, y entra el caso 19 — el que faltaba: un campo EN LA VENTANA (guarda en crudos,
     se pasa en escapados) tiene que AVISAR y dejar pasar. Su fixture se CALIBRA contando tildes
     hasta caer en la ventana, no se adivina. 20 de 20. -->


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

## Los techos · esto es lo que rompe en silencio

**Los cuatro topes del FORMULARIO del panel**, leídos de sus propios contadores el 2026-09-22 en
la pantalla "Agregar nuevo producto" del agente de comentarios:

| Campo del formulario | Llave | Tope | Cómo se midió |
|---|---|---|---|
| Nombre del producto | `name` | **255** | contador "36/255 caracteres" |
| Descripción del producto | `desc` | **500** | contador "481/500 caracteres", en rojo |
| **Cómo relacionar el post** | `rela` | **10 ETIQUETAS** | contador "7/10 etiquetas" |
| — | `estado` | toggle Inactivo / Activo | — |

🔴 **El tope del `rela` es de CANTIDAD, no de caracteres, y es el que más duele.** Un `rela` que
funciona lleva 25-30 disparadores. Por la vía formulario entran **10** y se pierden el resto — y
lo que se pierde es la cola, o sea la capa 4, que son los hooks del anuncio. Medido en el campo
vivo de una cuenta real: un producto con **71 etiquetas perdería 61**.

**Y el techo del bot field depende del TIPO del campo, no de la plataforma:**

| Tipo del campo | Techo |
|---|---|
| `JSON` | **20.000** escapados (~17.000 crudos) |
| `LONG JSON` | **500.000** — lo dice el propio panel: *"El contenido de datos JSON largos debe tener menos de 500.000 caracteres"* |

Por eso `[Comentarios] Productos` (JSON) aprieta y `[Comentarios] Productos extendido`
(Long JSON) no. El validador asume JSON, que es lo estricto; con `--long-json` mide contra el
techo grande.

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

**Obligatorio, y ninguno se supone:**

1. **País** — uno de los **10** que acepta la plataforma (`references/paises.md`). Si es BRASIL, la
   ficha va en **portugués**, no en español.
2. **Nombre del producto.**
3. **Precio de al menos 1 unidad.**
4. **La VÍA por la que va a entrar el producto** — `formulario` (alguien lo pega en el panel) o
   `json` (Campos de Bot / API). Decide si el tope de 500 **bloquea o solo avisa**, así que
   pregúntala: suponerla es entregar un texto que se corta solo. Ver §4.

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
- `references/kevin-doctrina.md` — **la doctrina de Kevin Galeano con minuto y cita**, y sus
  huecos declarados. Léelo antes de atribuirle nada.
- `references/paises.md` — moneda, formato y vocabulario de los 10 países.

### 4 · Compuerta: el validador en verde, o no se entrega

```bash
V=~/.claude/skills/golden-chatea-pro-producto-comentarios/scripts/validar_producto.py
python3 "$V" productos.json --via formulario   # se pega en el panel: 255/500/10 BLOQUEAN
python3 "$V" productos.json --via json         # Campos de Bot / API: solo avisan
python3 "$V" productos.json --via json --long-json   # el campo destino es Long JSON (500.000)
python3 "$V" --medir borrador.txt              # mide una desc suelta mientras la recortas
python3 "$V" productos.json --via json --json  # mismo veredicto en JSON, para encadenar
```

**`--via` es obligatoria y el validador se niega a correr sin ella.** No es burocracia: la misma
`desc` de 675 caracteres es un error que bloquea por `formulario` y un aviso aceptable por `json`.
Un validador que la supusiera daría verde a un texto que el panel va a cortar, que es exactamente
el fallo que esta skill existe para evitar.

**Cuando el producto vaya por `json` y la `desc` pase de 500, entrega DOS versiones:** la completa
para pegar por Campos de Bot, y una de 500 recortada con `--medir` para el día que alguien abra ese
producto en el formulario. Dile al usuario cuál es cuál y por qué existen las dos.

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

🔴 **CUÁL DE LOS TRES CAMPOS LEE EL FLUJO ES UNA INCÓGNITA ABIERTA. No escribas ninguno por API
hasta cerrarla.** En una cuenta conviven tres campos con nombres parecidos:

| Campo | Qué es |
|---|---|
| `[Comentarios] Productos` (`array`) | **el que lee el flujo** · aquí va el producto |
| `[Comentarios] Productos extendido` (`longtext`) | espejo de la migración · **copia, no traslado** |
| `[Comentarios] TOON Productos` (`longtext`) | espejo comprimido · **puede estar desfasado** |

**Por qué es incógnita y no un detalle.** En agosto se dedujo "lee el array" por descarte: el
`extendido` tenía los datos y el `array` estaba **vacío**. Ese razonamiento **ya no se sostiene**.
Medición del Centro de Mando el **2026-09-22** sobre un espacio real: el `array` tiene **7
productos** y el `extendido` tiene **los mismos siete, verificados nombre por nombre**. Los dos
poblados y sincronizados, así que el descarte no decide nada.

**La consecuencia es dura: escribir uno solo los DESINCRONIZA** y deja al flujo leyendo vaya a
saber cuál, con datos distintos a los del otro. Por eso la compuerta es no escribir ninguno de los
tres por API hasta confirmar.

**Y la prueba que lo cierra no es de disco.** No hay forma de saberlo leyendo campos: hay que
**comentar en un post de prueba y ver qué responde el bot**. Eso lo hace quien es dueño del
espacio, no esta skill. Mientras tanto se entrega el JSON y se dice esto mismo.

(Los hechos verificados sobre cada campo, en `references/escritura-api.md`.)

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
2b. `name` ≤ 255 y `rela` ≤ 10 etiquetas **si va por formulario**; por JSON entran completos.
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

## Cuándo NO soy yo

Si el encargo es alguno de estos, **dilo y manda al usuario a la skill correcta** en vez de
improvisar aquí:

| El usuario quiere… | No es esta skill |
|---|---|
| Los prompts del asistente: moderación de negativos, respuesta pública, venta conversacional | `golden-chatea-pro-config-comentarios` |
| Los datos del negocio: contacto, tiempos de envío, país del asistente, datos que pide la IA | `golden-chatea-pro-config-comentarios` |
| Vender ese producto por WhatsApp: saludo, multimedia, prompt de 12.000, remarketing | `golden-chatea-pro-prompt-ventas` |
| Que el disparador de VENTAS no engancha, o cargar el ID de anuncio | `golden-chatea-pro-config-ventas-wp` |
| Montar los 4 asistentes de un espacio nuevo | `golden-chatea-pro-full-configuracion` |
| Saber por qué el espacio entero está roto, campo por campo | `golden-chatea-auditoria` |
| Escribir o rotar los copys de los anuncios | `golden-copywriting` |

**La frontera en una línea:** si lo que cambia es **cómo habla** el asistente, no soy yo; si lo que
cambia es **de qué producto habla**, sí.

Y al revés: cuando roten los copys de Meta de un producto, el trabajo vuelve **aquí**, aunque el
encargo haya empezado en pauta.

## Privacidad

Skill compartible: **nunca hornees en sus archivos datos reales de un negocio** (tienda, asesora,
precios, WhatsApp, URLs con ID de cuenta, cifras). Los ejemplos de las referencias son ficticios a
propósito. Un dato real incrustado en un archivo de la skill es un error: quítalo.

## Archivos de referencia

- `references/rela-metodo.md` — **el método del `rela`**: las 5 capas, el banco de erratas, la
  regla anti-colisión y qué hacer con los emojis. Léelo antes de escribir cualquier `rela`.
- `references/desc-plantilla.md` — los 500 caracteres: esqueleto, **catálogo de reglas de marca
  por categoría**, método de recorte y qué material va en el prompt de ventas y no aquí.
- `references/paises.md` — los **10 países**: moneda y formato, vocabulario, y el detalle
  Colombia/México para quien trabaje esos dos.
- `references/escritura-api.md` — **solo si vas a escribir por API**: endpoints, paginación,
  respaldo, relectura, y los tres campos de comentarios que se confunden.
- `references/kevin-doctrina.md` — **la doctrina de Kevin Galeano (clase M7, 2026-09-02) con
  minuto y cita textual**, separando lo que dijo de lo que NO dijo: el `rela` como identificador
  único, la regla de validarlo contra el copy del anuncio, el método del "ejemplo" para superar
  los 500, el semáforo de encaje y las tres trampas del JSON. **Léelo antes de atribuirle una
  regla**: la "regla de la abuela" circulaba como suya y no está en ninguna de las 16 clases.
- `references/ejemplo-completo.md` — un producto ficticio horneado, con sus medidas reales. Vara
  de calidad de tu salida.
- `scripts/autoprueba.py` — **el banco del validador (14 de 14).** 🔴 Córrelo ANTES de confiar
  en `validar_producto.py` y SIEMPRE que lo toques: siembra un sabotaje por cada pieza y exige
  que cada uno produzca su error. Hasta el 2026-09-07 este validador no tenía banco. **Toda
  corrección nueva entra con su sabotaje**, o la suite acaba cubriendo solo lo ya arreglado.
- `scripts/validar_producto.py` — **el validador y la compuerta**. También `--medir` para recortar
  una `desc` sin adivinar, y `--json` para el veredicto estructurado.
- `scripts/autoprueba.py` — **el banco**: sabotea el validador pieza por pieza y exige que muerda
  cada una. Un cambio al validador sin el banco en verde no se sella.
- `scripts/contraprueba.py` — **la prueba del banco**. Sobre una copia en tmpdir: reescribe la
  redacción de dos errores (el banco debe seguir en verde) y después rompe el comportamiento (debe
  ponerse en rojo). Existe porque el banco llegó a medir el TEXTO de los mensajes y un cambio de
  redacción lo ponía en rojo sin que nada se hubiera roto. Un banco frágil entrena a ignorarlo.

## Fronteras y desambiguacion

🔴 **Aquí NO se guarda una copia de la description, y esta skill es el caso que originó la
regla.** Había una, con el rótulo *"se conserva para no perder ningún matiz de frontera"*, y ya
había **divergido**: llevaba dos frases de frontera que la description viva no tiene. Esa clase de
copia **envejece y acaba contradiciendo a la description real** — es como se coló el dato falso de
"7 países" en una hermana de esta familia. Lo que es frontera se escribe **como frontera**, aquí
abajo, en una sola versión que se mantiene:

**Esta skill monta UN PRODUCTO dentro del asistente de comentarios. No configura el asistente.**

· La **configuración GENERAL** de ese asistente —prompts, datos del negocio, país— la hace
  `golden-chatea-pro-config-comentarios`. Quien diga "configura el asistente de comentarios" o
  "arma el JSON de comentarios" va ahí, no aquí.
· El **paquete de venta del producto en WhatsApp** —prompt de venta, saludo, recordatorios,
  remarketing, activador— lo hace `golden-chatea-pro-prompt-ventas`. Aquí solo se monta la ficha
  que el bot de comentarios usa para reconocer de qué producto habla cada comentario.
· **Auditar** lo ya instalado en un espacio → `golden-chatea-auditoria`.
