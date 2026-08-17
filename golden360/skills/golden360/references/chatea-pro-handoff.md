# FASE 8 · Chatea PRO del PRODUCTO (2 piezas por-producto)

Objetivo: dejar el **producto investigado** listo para venderse por WhatsApp y para responder en comentarios, que el dueño solo **copie y pegue**, sin redactar nada.

## Regla — por qué solo 2 skills
El estudio produce **un PRODUCTO**. Para lanzarlo se configuran las **dos piezas que dependen del producto**:

1. **Venta por WhatsApp del producto** → **`golden-chatea-pro-prompt-ventas`**
2. **Comentarios del producto** → **`golden-chatea-pro-config-comentarios`**

Las demás skills de Chatea PRO (**`golden-chatea-pro-config-logistico`** + **`golden-chatea-pro-validacion-direcciones`**, **`golden-chatea-pro-config-carritos`**, **`golden-chatea-pro-config-ventas-wp`** y el orquestador **`golden-chatea-pro-full-configuracion`**) son **configuración del espacio de trabajo** (transportadoras, validación de direcciones por país, carritos, config general): se montan **una sola vez por tienda/país**, NO por cada producto. Por eso **NO** se llaman en esta fase. Si el dueño quiere montar el workspace completo de cero, eso es un flujo aparte con `golden-chatea-pro-full-configuracion`.

## Qué le pasa el expediente (del Bloque 1 y la Fase 4)
Producto, beneficios, objeciones (voz del cliente), oferta/precio, país, garantía COD, diferenciales, y la **palabra clave del bot** (`activacion.keyword_bot` = el mensaje del botón WhatsApp de la página; pregúntala si no se definió). La palabra clave debe ser la MISMA en página, pauta, orgánico y bot.

## Las 2 piezas que deja listas

1. **Venta WhatsApp** (`golden-chatea-pro-prompt-ventas`) → el **paquete de venta por producto**: saludo, plan de multimedia, pregunta de entrada, **prompt de venta** con las objeciones reales del estudio, recordatorios y remarketing. Entrega **copy-paste por campo separado**; el **manifiesto de imágenes va DEBAJO del prompt, nunca dentro**.
2. **Comentarios** (`golden-chatea-pro-config-comentarios`) → respuesta pública en posts/anuncios del producto → lleva la conversación al DM. Cierra el círculo orgánico + pauta → conversación.

## Entregable
`PROYECTOS/<PRODUCTO>/CHATEA-PRO.md` con las **2 piezas por-producto** rotuladas y separadas, listas para copiar/pegar en Chatea PRO. Nada de "ajusta esto tú" — todo redactado y completo.
**Candado (REGLA 6 del orquestador — completitud):** deben estar las **2 piezas** (venta WhatsApp + comentarios). Si falta alguna, la fase está INCOMPLETA y `candado.py` la reprueba.
**Y el botón no se monta si `activacion.cargado_en_bot` es `false`:** un botón que dispara a un bot que no conoce el producto es un embudo roto.

> El contenido lo producen las dos skills de Chatea PRO. Esta skill solo delega y les pasa el contexto del estudio. La config de workspace (logístico, carritos, config general) queda fuera de este flujo de producto.
