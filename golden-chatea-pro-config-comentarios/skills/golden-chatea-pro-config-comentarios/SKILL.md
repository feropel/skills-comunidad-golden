---
name: golden-chatea-pro-config-comentarios
description: Genera el JSON de configuración del asistente de COMENTARIOS de Chatea Pro para una tienda (moderación de comentarios negativos, respuesta pública tipo community manager y venta conversacional que cierra en el mismo chat), con los prompts ya afinados y adaptados por país. Úsalo SIEMPRE que el usuario quiera montar o configurar el asistente de COMENTARIOS de Chatea Pro, generar o armar el JSON de comentarios/respuesta pública/venta conversacional, o diga cosas como "configura el asistente de comentarios", "arma el json de comentarios de chatea pro", "monta la respuesta pública de mi tienda", "necesito el config de comentarios". Si el usuario quiere configurar TODOS los asistentes a la vez (comentarios + logístico + ventas WhatsApp + carritos), eso lo hace golden-chatea-pro-full-configuracion; el asistente de VENTAS por WhatsApp lo hace golden-chatea-pro-config-ventas-wp; los TEXTOS de venta por producto los hace golden-chatea-pro-prompt-ventas. NO sirve para configurar productos como cantidad y precios, que van en la ficha del producto y no en esta configuración general.
---

# Chatea Pro — Config del asistente de comentarios

Genera el JSON de configuración del asistente de **comentarios** de una tienda en Chatea Pro. Trae fijos y ya afinados: el clasificador de comentarios negativos, el prompt de respuesta pública (community manager + copywriter de Golden) y el prompt de venta conversacional (9 etapas, modo captura, objeciones, cierre en el mismo chat). Todo en español colombiano, humanizado y con precios en `$`.

Lo único que cambia entre tiendas es la **información del negocio**, que se pregunta al ejecutar.

## Qué preguntar al usuario (intake)

Pregunta estos 4 datos, **uno a la vez** y en este orden. No los pidas todos de golpe.

1. **País** donde opera la tienda (ej: colombia).
2. **Contacto**: una página web, un WhatsApp **o** un correo. Solo uno; es dato de referencia, no para mandar al cliente a otro canal.
3. **Tiempos de envío**: cuánto demora la entrega (ej: ciudad principal 2-3 días, intermedia 3-4, rural 5-7). Este dato **se pregunta siempre**, no se asume.
4. **Información adicional del negocio**: una o dos líneas de respaldo (años en el mercado, número de clientes, sede, pago contra entrega, originalidad).

### Datos que la IA le pide al cliente (campo `datos_req`) — se genera solo

En Chatea Pro existe el campo **"datos que la IA debe solicitar al cliente para completar la compra"** (en el JSON: `venta_conversacional.datos_req`). **No lo preguntes en el intake**: el script lo arma automáticamente según el **país** y su nomenclatura de direcciones:

- **Colombia**: Nombre completo; Número de WhatsApp; Dirección exacta; Barrio o punto de referencia; Ciudad; Departamento.
- **México y otros países con estado/colonia/CP**: Nombre completo; Número de WhatsApp; Dirección exacta; Colonia; Ciudad / Municipio; Estado; Código Postal.

Si el usuario quiere una lista distinta a la del país, pásala manualmente con `--datos-cliente "campo1; campo2; ..."` y el script la usa tal cual.

### Lo que NO se pregunta aquí

No pidas producto, descripción, cantidad ni precios. Esa información va **en la ficha de cada producto dentro de Chatea Pro**, no en esta configuración general. Si el usuario los menciona, acláralo con amabilidad y sigue con el intake. El prompt de venta conversacional ya lee el producto a través de la variable `{DESCRIPCION_PRODUCTO}` que Chatea Pro llena producto por producto.

## Cómo generar el JSON

Con los 4 datos del intake, corre el script. Los prompts no se tocan: solo se reemplaza la información del negocio.

```bash
python3 scripts/build_config.py \
  --pais "colombia" \
  --contacto "<lo que dio el usuario>" \
  --t-envio "<tiempos de envío del usuario>" \
  --info-extra "<info del negocio del usuario>" \
  --out <negocio>_CONFIG.json
```

El campo `datos_req` (datos que la IA le pide al cliente) se genera solo según `--pais`. Solo agrega `--datos-cliente "campo1; campo2; ..."` si el usuario pide una lista distinta a la estándar del país.

El tope del campo depende de su **TIPO**, no de la plataforma: tipo **JSON** = 20.000, tipo
**LONG JSON** = **500.000** (medido por API el 2026-07-25). **Crea el campo como LONG JSON** y el
problema de espacio desaparece: la plantilla base usa ~19.800, que en LONG JSON es el 4% del cupo.

Si el campo del cliente **todavía es tipo JSON** (los workspaces viejos lo son, incluido
GOLDEN GROUP V2, donde `[Comentarios] Configuracion General` va en 19.517 = **97,6% del tope**),
entonces sí hay que apretar: **no recortes los prompts** — acorta los campos de negocio (contacto,
tiempos de envío, info), que es lo único editable. Lo correcto es cambiar el tipo del campo a
LONG JSON en la UI, no seguir recortando.

⚠️ **Pasarse del tope NO da error:** la API responde `200 ok` y guarda el JSON **cortado**, con lo
que el asistente empieza a fallar sin un solo mensaje de error. Después de escribir, relee el campo
y compara la longitud.

## Cómo lo usa el usuario

El JSON resultante se pega en Chatea Pro. Aunque la respuesta pública y la venta conversacional superen su tope nativo por campo (3.000 y 8.000), al pegar el JSON completo el backend solo valida el total del campo, así que entra sin problema.

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

Este skill configura **solo** el asistente de comentarios. Deriva cuando el pedido sea más amplio:

- **Todos los asistentes a la vez** (comentarios + logístico + ventas WhatsApp + carritos) → `golden-chatea-pro-full-configuracion` (orquestador).
- **Asistente de ventas por WhatsApp** (Bot Fields, embudo, prompt maestro) → `golden-chatea-pro-config-ventas-wp`.
- **Asistente logístico / novedades preventivas** → `golden-chatea-pro-config-logistico`.
- **Carritos abandonados** → `golden-chatea-pro-config-carritos`.
- **Los TEXTOS del prompt de venta por producto** (no la estructura) → `golden-chatea-pro-prompt-ventas`.

## Privacidad (skill compartible)

Este skill se comparte. Los prompts son genéricos y la información del negocio se pregunta al ejecutar; **nunca** hornees dentro de la skill datos reales de un negocio o cliente (WhatsApp, nombre de tienda, sede, cifras). La plantilla base usa valores de ejemplo obviamente ficticios que el intake sobrescribe siempre.
