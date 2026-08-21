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

- **El flujo lee el `array`.** El 2026-08-05 una reinstalación dejó de responder porque Chatea
  había migrado el contenido al `extendido` y dejó el array **vacío**. Síntoma exacto:
  *"🚨 Comentario NO automatizado — no hay información sobre el producto"*, y de paso los
  comentarios negativos dejan de eliminarse porque el flujo aborta antes de clasificar.
- **Leer el `array`, verlo vacío y concluir "no hay productos" es un error.** Ya pasó: array
  vacío, `extendido` con 7 productos vivos.
- **Es copia, no traslado.** Si cambia un precio hay que tocar los dos.
- **El `TOON` puede estar viejo.** Se ha encontrado nombrando un producto que ya no existe. No lo
  escribas a ciegas: si difiere de los otros dos, pregunta cuál es la fuente de verdad antes de
  tocarlo.
- **El tipo de un campo existente no se puede cambiar.** Para cambiar de tipo hay que crear uno
  nuevo.

**Protocolo:** lee los tres, compáralos, y si difieren pregunta en vez de elegir tú.

---

## Leer — y paginar, siempre

```
GET /flow/bot-fields?page=N
```

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

**Crear un campo nuevo:**

```
POST /flow/create-bot-field
{"name": "...", "var_type": "array", "value": "[]"}
```

Usa **`var_type`** (no `type`) y **exige `value`**. Con otra llave, **422**.

### 🔴 `POST` al EDITAR devuelve 200 y NO escribe

Es el gotcha que más tiempo cuesta: la respuesta trae 200 y un mensaje que no dice "error", y el
valor sigue igual. **Crear es POST, editar es PUT.** Esta es una de las razones por las que releer
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

## Los dos techos, otra vez

```python
crudo    = len(valor)
escapado = len(json.dumps(valor)[1:-1])          # ensure_ascii POR DEFECTO. Objetivo: < 19.000
```

⚠️ **El `ensure_ascii` de esta línea va en su valor por defecto (`True`), y no es un descuido: es
justo lo que hace la medición.** Con `True`, una tilde se vuelve `\u00e1` (6 caracteres) y un emoji
un par subrogado (12) — que es lo que el flujo copia al ejecutarse. Si lo pones en `False`, una
tilde cuenta 1, la medición queda apagada y un campo de 20.345 se reporta como 10.769 y pasa en
verde. (Fallo real cazado en la auditoría de esta skill.)

**No lo confundas con la serialización de arriba**, que sí va con `ensure_ascii=False`. La regla en
una línea: **se guarda sin escapar y se mide escapado.**

Dos mediciones reales, para calibrar el ojo:

- **16.882 crudos / 19.895 escapados** → pasa (queda bajo el techo de 20.000), pero **dispara el
  aviso** porque ya superó el objetivo de 19.000: sin margen para crecer.
- **19.922 crudos / 23.266 escapados** → **no** pasa: supera el techo de 20.000 y muere sin un
  error visible. El único rastro queda en Panel → Registros de errores.

Y por producto, `desc ≤ 500` (ver `desc-plantilla.md`).

---

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
