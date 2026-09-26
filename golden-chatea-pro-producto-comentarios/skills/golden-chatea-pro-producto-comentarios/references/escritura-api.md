# Leer, escribir y RELEER el campo de productos

Base URL del whitelabel: `https://chateapro.app/api`
Cabeceras: `Authorization: Bearer <api_key>` + `Accept: application/json`

El token es del workspace del cliente. **Nunca lo escribas dentro de la skill, ni en un archivo
del proyecto, ni en un ejemplo.** Va por variable de entorno o por el gestor de secretos del
usuario.

---

## Los tres campos que se confunden

En una cuenta pueden convivir tres bot fields con nombres parecidos — `[Comentarios] Productos`
(`array`), `[Comentarios] Productos extendido` y `[Comentarios] TOON Productos` (los dos
`longtext`). Cuál es cuál está en la tabla del §5 de `SKILL.md`; aquí van los hechos que la
sostienen. Escribir el equivocado duplica o rompe respuestas **en público**.

- 🔴 **CUÁL LEE EL FLUJO: INCÓGNITA ABIERTA. No escribas ninguno por API hasta cerrarla.**
  En agosto se dedujo "lee el array" por descarte, y el razonamiento caducó. Las tres mediciones:

  | Fecha | `Productos` (array) | `Productos extendido` | Qué se pudo concluir |
  |---|---|---|---|
  | 2026-08-05 | **vacío** | con datos | el array vacío rompía el bot, así que **algo** lo lee |
  | 2026-09-22 (primera lectura) | 7 productos (7.249 car.) | los mismos 7 (7.061 car.) | se anotó "sincronizados" — **era falso**, solo se compararon los NOMBRES |
  | **2026-09-22 (comparación real)** | 7 productos, **los 7 con `estado`** | los mismos 7, **6 SIN `estado`** y con el texto VIEJO | **están DESINCRONIZADOS desde antes de tocar nada** |

  🔴 **"Mismos nombres" no es "mismo contenido".** La primera lectura comparó la lista de `name`,
  vio 7 y 7, y escribió "sincronizados". Comparando el CONTENIDO aparecieron dos diferencias
  graves que llevaban ahí desde antes: el `extendido` conserva una redacción anterior de cada
  `desc`, y **a 6 de sus 7 productos les falta la llave `estado`** — la misma cuya ausencia hace
  que el panel no interprete el producto. **Compara valores, no inventarios.**

### 🔴 De qué campo deriva el TOON — medido por huella de texto

`[Comentarios] TOON Productos` no es un tercer JSON: es una **serialización compacta** con
cabecera `productos[7]{img,name,desc,rela,estado}:` y una fila por producto.

Como el `array` y el `extendido` tienen redacciones DISTINTAS del mismo producto, cada diferencia
entre ellos es un trazador gratis. Buscando esos trozos dentro del TOON (Le'côterra, 2026-09-22):

| Trozo discriminante | ¿está en el TOON? |
|---|---|
| `"No tapa el mal olor, lo"` (del **array**) | **SÍ** |
| `"Fragancia espectacular que"` (del **extendido**) | no |
| 7 trozos más, uno por producto | **todos los del array, ninguno del extendido** |

**En la cuenta de Golden el TOON refleja el `array`.** Y el `extendido` es el que quedó atrás.

⚠️ **Pero esto NO cierra la incógnita, y conviene ver por qué.** En la cuenta de Kevin
(un espacio de referencia, **versión 2.1.2**, una por delante de Golden) la foto es distinta: el `array` está
**vacío**, el `extendido` tiene el producto, el TOON tiene contenido **y no coincide con ninguno
de los dos**. Además existe un campo que Golden no tiene: `[Comentarios] Nombres de los productos`.
O sea: **el esquema cambia entre versiones**, y lo medido en 2.1.1 no se puede extrapolar. Datar
la versión antes de aplicar nada: `[Comentarios] Versión` → Golden **2.1.1**, Kevin **2.1.2**.

**Y hay una cita que tira para el otro lado:** el método de Kevin edita **el extendido**
(*"venimos a la carpeta donde dice producto extendido"*, 1:46:48) y luego **recarga el
formulario**. Si esa recarga regenera el resto desde el extendido, entonces el extendido es la
puerta de entrada y el array un derivado — lo contrario de lo que sugiere la huella. **Las dos
lecturas son compatibles con lo medido; ninguna está probada.** Solo la prueba del post decide.

**Salida robusta mientras la incógnita siga abierta:** que la ficha quepa en el MÁS ESTRECHO de
los tres (el `array`, **20.000 crudos**) y escribir los tres **con el mismo contenido**. Se
sacrifica tamaño y se gana que, lea el que lea, lea lo correcto. Escribir un largo solo en los
`longtext` apuesta la operación a una incógnita.
- **Lo que SÍ sigue en pie del 2026-08-05:** con el `array` vacío el asistente dejó de responder
  —*"🚨 Comentario NO automatizado — no hay información sobre el producto"*— y de paso los
  comentarios negativos dejaron de eliminarse, porque el flujo aborta antes de clasificar. Eso
  prueba que el array **participa**; no prueba que sea el único que se lee.
- **Leer el `array`, verlo vacío y concluir "no hay productos" es un error.** Ya pasó: array
  vacío, `extendido` con 7 productos vivos.
- **Es copia, no traslado.** Si cambia un precio hay que tocar los dos.
- **El `TOON` puede estar viejo.** Se ha encontrado nombrando un producto que ya no existe. No lo
  escribas a ciegas: si difiere de los otros dos, pregunta cuál es la fuente de verdad antes de
  tocarlo.
- **El tipo de un campo existente no se puede cambiar.** Para cambiar de tipo hay que crear uno
  nuevo.

**Protocolo, mientras la incógnita siga abierta:** lee los tres y compáralos. Si están
sincronizados, **no escribas ninguno por API**: entrega el JSON y di que falta la prueba del post.
Si difieren, tampoco elijas tú — pregunta cuál es la fuente de verdad.

---

## 🔴 El cupo: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera

Medido contra la API viva el **2026-09-07**. Cada respuesta trae **`x-ratelimit-remaining`** (las
que quedan) y `x-ratelimit-limit`. **Se repone cada hora**, pero **no viene `x-ratelimit-reset`**:
el servidor no dice a qué minuto empezó la ventana, así que si te bloqueas se espera una **hora
completa** y se comprueba **mirando** el contador (`golden-chatea-cupo [--necesito N]`), nunca
calculándolo de cabeza.

**Cómo te afecta cargando productos.** Se escribe con **PUT** y la **relectura es obligatoria**,
así que cada producto son al menos **dos peticiones**. Si cargas muchos de golpe, cuenta el total
antes: quedarte sin cupo a mitad deja el array **escrito por la mitad**, y el panel no lo delata.

## 🔴 Dos formas de creer que algo está roto cuando no lo está

**1 · `urllib` recibe 403 de Cloudflare. No es el token.** Medido el 2026-09-22: cualquier
petición desde `urllib.request` vuelve con **HTTP 403, `error_code` 1010**, *"Access denied based
on your browser's signature"*. Es la firma del cliente, no la credencial, no el endpoint y no el
cupo. **Con `curl` el mismo token responde 200.** Un 403 así se lee como token muerto y manda a
rotar credenciales sanas — que además invalida las que otros chats están usando. **Antes de tocar
un token, prueba con `curl`:**

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://chateapro.app/api/flow/bot-fields?page=1" -H "Authorization: Bearer $T"
```

**2 · Borrar un campo es `DELETE`, no `POST`.** `POST /flow/delete-bot-field` devuelve **405** con
la lista de métodos admitidos. Es de los pocos sitios donde la API avisa bien: el resto de esta
página existe porque **no** avisa.

---

## Leer — y paginar, siempre

```
GET /flow/bot-fields?page=N
```

*(Corrido en vivo el 2026-09-22 por el Centro de Mando contra tres espacios distintos, con Bearer
y User-Agent de navegador. Pagina de 10 en 10.)*

**Pagina, y `per_page` se ignora.** Un workspace de 56 campos son 6 páginas: pedir solo la
primera deja fuera 46. Recorre hasta que la página vuelva vacía.

Un cero solo prueba algo si cubriste todas las páginas. "Este cliente no tiene el campo" dicho
sobre la página 1 no es un hallazgo, es un descuido.

---

## Escribir

**Por `var_ns` (un campo):**

```
PUT /flow/set-bot-field
{"var_ns": "<ns_del_campo>", "value": "<string>"}
```

**Por nombre (varios campos):**

```
PUT /flow/set-bot-fields-by-name
{"data": [{"name": "...", "value": "..."}]}
```

La llave es **`data`**. Con `bot_fields` responde **400**.

*(Usado en vivo el 2026-09-22 para escribir un campo de 12 entradas y un booleano en un espacio
real, releído y comparado como JSON **parseado**. Funciona.)*

**Crear un campo nuevo:**

```
POST /flow/create-bot-field
{"name": "...", "var_type": "array", "value": "[]"}
```

Usa **`var_type`** (no `type`) y **exige `value`**. Con otra llave, **422**.
*(Medido en 2026-08-07 y **no reverificado** desde entonces. Trátalo como dato fechado, no
fresco.)*

### 🔴 `POST` al EDITAR devuelve 200 y NO escribe

Es el gotcha que más tiempo cuesta: la respuesta trae 200 y un mensaje que no dice "error", y el
valor sigue igual. **Crear es POST, editar es PUT.** *(Medido en 2026-08-07 y **no reverificado**;
dato fechado.)* Esta es una de las razones por las que releer
no es opcional.

---

## El valor va como string, y el formato importa

El contenido del campo es un **string** que contiene el JSON de la lista. Serialízalo compacto:

```python
valor = json.dumps(productos, ensure_ascii=False, separators=(',', ':'))
```

Otro formato (indentado, o con `ensure_ascii=True`) **infla el campo sin cambiar el contenido**:
con `ensure_ascii=True` cada tilde se guarda como `\u00e1`, y el campo puede reventar el techo sin
que hayas añadido una sola palabra.

---

## 🔴 No hay UN techo: hay DOS, y se observan con pruebas distintas

Esto costó una contradicción entre dos fábricas y se resolvió poniendo las cinco mediciones de la
casa una al lado de la otra. **Ninguna hipótesis de techo único las explica todas.**

| Qué se observó | Medición | Resultado |
|---|---|---|
| **GUARDAR y RELEER** *(config-comentarios, 2026-09-22, campo array de comentarios)* | 13.004 crudos | guarda |
| | **19.617 crudos / 21.457 escapados** | **guarda y se relee IDÉNTICO byte a byte** |
| | 20.811 crudos | **error 500**, y el campo queda **VACÍO** en el servidor |
| **SI EL BOT DISPARA al ejecutarse** *(BRIEFING, 2026-08)* | 16.882 crudos / 19.895 escapados | dispara |
| | 19.922 crudos / **23.266 escapados** | **NO dispara** |

**Lo que mata cada hipótesis.** Si el techo fuera *20.000 escapados*, el campo de **21.457
escapados que hoy está guardado y funcionando no existiría**. Y si fuera *20.000 crudos*, el de
19.922 crudos habría disparado, y no disparó.

**La lectura que sí sobrevive:**

- **GUARDAR topa en 20.000 CRUDOS EXACTOS.** Medido directo el 2026-09-22 (ver abajo). **Esto es
  lo que bloquea el validador.**

#### 🔴 Medición DIRECTA del techo, y la trampa que destapó (2026-09-22)

El número anterior venía heredado de un campo ajeno. Se midió el tipo que importa, en un campo de
prueba propio (`create-bot-field` tipo `array`, búsqueda binaria, **releyendo del servidor** cada
vez, y borrado al final). 10 escrituras, 132 peticiones:

| Pedido | HTTP | Releído | Veredicto |
|---:|---:|---:|---|
| 1.000 | 200 | 1.000 | guarda entero |
| 15.750 | 200 | 15.750 | guarda entero |
| 19.437 | 200 | 19.437 | guarda entero |
| **19.898** | 200 | **19.898** | **guarda entero — último que entra** |
| **20.128** | **200** | **20.000** | **TRUNCA** |
| 23.125 | 200 | 20.000 | trunca |
| 60.000 | **200** | **20.000** | trunca |

> ### 🔴 El campo `array` TRUNCA EN SILENCIO a 20.000 y responde **HTTP 200**
>
> No da error 500 ni deja el campo vacío: **recorta y dice que todo salió bien.** Un payload de
> 32.834 crudos habría perdido 12.834 caracteres sin un solo aviso, cortando el JSON a mitad de
> palabra: deja de parsear, y el bot se queda **sin productos** respondiendo que no tiene
> información. Todo con un 200 en el log.
>
> **Por eso el 200 NO es prueba de nada y releer no es opcional: es LA prueba.** Y releer tampoco
> basta si solo se mira que "hay algo" — hay que comparar **longitud y contenido** contra lo que
> se mandó.
>
> El "error 500 con el campo vacío" que anota la medición de la otra fábrica **es una vía
> distinta** (no esta llamada de API). Las dos pueden ser ciertas a la vez; lo que no se puede es
> contar con el error como aviso. **Por API no hay aviso.**

**20.000 es redondo, y un redondo repetido es un tope**, no una casualidad de los datos.
- **EJECUTAR tiene un límite propio y más estrecho**, y la única evidencia que existe está en
  escapados. La zona entre 19.895 (dispara) y 23.266 (no dispara) **no está medida**. El validador
  **avisa** ahí, no bloquea.

> **Por qué avisa y no bloquea.** Poner error en escapados rechazaría una configuración que hoy
> corre en producción. Un guardarraíl que bloquea trabajo bueno cuesta más que no tenerlo, porque
> nadie duda de él y se empieza a recortar contenido que sí cabía.

### 🔴 Y la frontera de ejecución también es HEREDADA (el fallo simétrico)

Esto casi se nos cuela a las dos fábricas. **Las dos observaciones de ejecución —19.895 dispara,
23.266 no— se midieron sobre campos `[Producto Ventas Wp]`.** Es exactamente el mismo campo ajeno
del que venía el número equivocado del guardado.

O sea que **la ley que corrigió el primer número se aplica igual al segundo**: para el campo de
comentarios, el límite de ejecución **no está medido ni por arriba ni por abajo**. No existe un
"16.882 escapados dispara" observado en `[Comentarios] Configuracion General`; existe observado en
otro sitio.

Corregir un número heredado y dejar en pie el otro es el **fallo simétrico**: se arregla la mitad
que dolió y se conserva la que todavía no ha dolido. Por eso el aviso del validador **declara que
su frontera es prestada**, y por eso no se recorta contenido basándose en él.

**Y hay un experimento vivo que puede cerrar la ventana.** La configuración que corre hoy en
producción mide **21.457 escapados**, o sea que está **dentro de la zona desconocida**. La prueba
del post (comentar y ver si el bot responde) responde dos preguntas de una:

| Resultado | Qué prueba |
|---|---|
| **dispara** | la frontera de ejecución de ESTE campo está **por encima de 21.457**, y la ventana se estrecha por abajo con un dato propio |
| **no dispara** | hay techo por debajo de 21.457, y esa configuración hay que recortarla (≈1.429 caracteres, que es bajar a ~18.188 crudos) |

*(Ratio medido sobre ese texto concreto: **1,0938 escapados por crudo**. Sirve para convertir ese
caso, no como constante: el ratio sube con la densidad de tildes y emojis.)*

**De dónde salía el número equivocado, por si reaparece:** el "20.000 escapados" se midió sobre
campos `[Producto Ventas Wp]`, no sobre el de comentarios. **Un tope medido en un campo no se
traslada a otro aunque los dos sean `array`.** Y lo que el panel *anuncia* no es una medición de
comportamiento: dice 20.000 sin decir la unidad, y asumir escapados fue una inferencia.

### El tipo del campo sí manda sobre el número

| Tipo | Techo de guardado |
|---|---|
| `JSON` | **~20.000 crudos** |
| `LONG JSON` | **500.000** — lo dice el panel: *"El contenido de datos JSON largos debe tener menos de 500.000 caracteres"* |

El validador asume `JSON`, que es lo estricto; con `--long-json` mide contra el grande.

### 🔴 La suma de los topes del panel NO es el presupuesto

Hallazgo de `config-comentarios`, medido en vivo el 2026-09-22: **los topes nativos del formulario
de comentarios suman 24.100 y el campo aguanta 20.000.** El panel valida **caja por caja y nunca
la suma**. Se pueden llenar todas en verde, con sus contadores azules, y que el guardado reviente
con *"Request failed with status code 500"*.

Y el 500 **aborta el campo entero, no lo trunca**: el campo que falló quedó **vacío** en el
servidor y los otros ocho intactos. O sea que el modo de fallo no es "se pierde la cola", es "se
pierde todo".

### Dos trampas de medición que cuestan caro

- **El JSON gasta más que el contador del panel.** Cada salto de línea cuenta **2** dentro del
  valor, y la estructura del objeto añade lo suyo (medido: 356 caracteres extra en un caso real).
  Presupuestar sobre el conteo del panel se queda corto por unos **800**.
- **El contador del panel cuenta en UTF-16.** Sin emojis coincide con Python exactamente; **con
  emojis, no**. Si mides un texto con emojis y te da distinto que el panel, no es un error tuyo.

### Cómo se mide

```python
crudo    = len(valor)                        # lo que decide si GUARDA
escapado = len(json.dumps(valor)[1:-1])      # la señal del limite de EJECUCION
```

El `ensure_ascii` del escapado va en su valor por defecto (`True`): eso es lo que convierte cada
tilde en `\u00e1` (6 caracteres) y cada emoji en un par subrogado (12). No lo confundas con la
**serialización** que se manda a la API, que sí va con `ensure_ascii=False`.

Y por producto, `desc ≤ 500`, `name ≤ 255` y `rela ≤ 10 etiquetas` **en el formulario**.

## Releer SIEMPRE — es la única prueba

```
escribir → GET /flow/bot-fields (paginando) → comparar el valor guardado contra el enviado
```

Comparar byte a byte es lo único que demuestra que se escribió. Además detecta dos cosas que no se
ven de otra forma: que la API haya guardado el JSON **cortado** por techo, y que **otra mano lo
haya pisado** desde el panel.

**Y el estado vivo se lee del servidor, nunca de un respaldo local.** Diagnosticar sobre un backup
del proyecto ya llevó a reportar como roto algo que estaba arreglado.

---

## Antes de escribir, respalda

Guarda el valor actual de los tres campos en un archivo con fecha antes de tocar nada. La API no
tiene "deshacer", y los subflujos de Comentarios son **plantillas bloqueadas de Chatea sin
endpoint de creación**: lo que se rompa ahí no se reconstruye desde la API.

---

## Lo que no se hereda al clonar una cuenta

Si estás montando el workspace de un cliente a partir de otro, **vacía** el campo de productos
antes de entregar: los catálogos son del negocio anterior. Lo mismo con
`[Integraciones] Datos de integracion` (lleva llaves de Dropi, Shopify, OpenAI, Meta y Google Maps
en texto plano), los productos cacheados de Carritos, y las métricas del dueño.

La fuga menos obvia son los **nombres de producto y de transportadora dentro de los textos**: son
ejemplos que la IA imita. En una cuenta heredada aparecieron transportadoras de otro país y la
marca del profesor dentro del workspace de un alumno.
