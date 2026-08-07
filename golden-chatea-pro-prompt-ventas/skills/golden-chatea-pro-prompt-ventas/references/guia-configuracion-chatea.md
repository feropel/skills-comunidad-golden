# Guía de Configuración en Chatea PRO v2 (dónde va cada cosa)

IMPORTANTE: el paquete que genera este skill NO va todo en un solo campo. Se reparte en varias secciones de Chatea PRO. NO sigas la numeración como si fuera un orden secuencial en un solo lugar; cada pieza tiene su sección. Esta guía es para que cualquier persona lo configure sin enredarse.

## Mapa de ubicación

| Pieza del paquete | Sección en Chatea PRO | Campo exacto |
|---|---|---|
| Datos del producto (nombre, precio, tipo, ID Dropi, variaciones, imagen) | Información del producto | Varios campos |
| Saludo inicial | Mensajes de bienvenida | Mensaje de bienvenida |
| Multimedia inicial (imágenes/video que se envían al entrar) | Mensajes de bienvenida | Contenido multimedia inicial |
| Pregunta de entrada | Mensajes de bienvenida | Pregunta de entrada |
| Prompt de venta | Prompt del producto | Prompt personalizado (modo "Prompt libre") |
| URLs que el agente envía DURANTE el chat | (van escritas DENTRO del prompt) | — |
| Recordatorio 1 y 2 | Recordatorios | Recordatorio 1 / 2 + sus tiempos |
| Remarketing 1 y 2 | Remarketing | Plantilla mensaje + Instrucción especial |
| Palabras clave del activador | Activador de flujo | Palabras clave |

## Información del producto (primera sección, fácil de olvidar)

Antes del prompt, en la sección "Información del producto" se configuran los datos base. Llénalos todos:
- **Nombre del producto** (ej: un serum, una crema, un accesorio)
- **Precio del producto** + moneda (COP, MXN, etc.)
- **Tipo de producto**: normalmente "Producto Físico"
- **ID del producto en Dropi** (solo números): conecta el pedido con el fulfillment en Dropi. OPCIONAL para generar el prompt; se puede agregar después.
- **Tiene variaciones?**: Sí/No (Sí cuando hay colores, sabores, tallas, etc.)
- **Estado**: Activo
- **Imagen del producto**

El precio de esta sección también se puede dejar para después. Lo realmente importante para vender es que el precio y los combos queden DENTRO del prompt.

IMPORTANTE sobre el precio: el precio de esta sección es solo el que se MUESTRA en la visualización del producto. Para que la IA lo diga al cliente en el chat, **el precio (y los combos) deben ir también escritos en el prompt**. No basta con ponerlo aquí.

## Regla clave sobre multimedia (la confusión más común)

Hay DOS tipos de audiovisuales y van en lugares distintos:

1. **Multimedia INICIAL** (lo que se envía apenas el cliente entra: imagen de productos, video, prueba social) → va en **"Contenido multimedia inicial"** dentro de Mensajes de bienvenida. **NO va en el prompt.**

2. **URLs que el AGENTE envía durante la conversación** (ej: imagen de modo de uso, tabla de precios, testimonios, cuando el cliente los pide o cuando aplica) → van **ESCRITAS DENTRO del prompt**, con la instrucción de cuándo enviarlas. Ejemplo dentro del prompt: `Si pide ver cómo se aplica, envía: https://...`

Por eso el prompt siempre debe incluir las URLs conversacionales adentro. La multimedia inicial se sube aparte.

## Activador de flujo (palabra clave)

- UNA sola palabra clave, y es la **frase completa del mensaje del anuncio/botón** (con el nombre del producto). Esa frase entera ES la palabra clave:
  ```
  Hola quiero información y precio de [PRODUCTO]
  ```
- NO agregues palabras sueltas extra como `información` o `precio` por separado: con varios productos se cruzan y disparan el bot equivocado. La frase completa (única, con el nombre del producto) va idéntica como palabra clave Y como mensaje del botón.

## Tiempos (fijos)

- Recordatorio 1: 1 hora — sin plantilla (solo el mensaje).
- Recordatorio 2: 2 horas — sin plantilla.
- Remarketing 1: 3 horas — plantilla de Meta.
- Remarketing 2: 6 horas — plantilla de Meta.
- Rango horario de envío sugerido: ajústalo a la operación del negocio (ej. 8:00 a.m. a 8:00 p.m.).

## Cómo se configura el Remarketing (3 campos)

Cada "Configuración Remarketing" tiene un interruptor (activar) y tres campos:
1. **Tiempo Remarketing:** número + unidad (3 Horas / 6 Horas).
2. **Plantilla Mensaje:** desplegable donde eliges una **plantilla de Meta ya aprobada**, o "No enviar plantilla". La plantilla se crea en el Administrador de WhatsApp/Meta (nombre en minúsculas_con_guion_bajo, categoría Marketing, idioma Español, imagen del producto, cuerpo con variable `{{1}}` = nombre del cliente, pie de página, y botón — el botón se mapea en Chatea como "botón de remarketing").
3. **Instrucción especial del remarketing:** un solo campo (máx. 1000 caracteres) donde va TODO junto: el mensaje con que el bot reabre + la instrucción para la IA entre corchetes.

Si el negocio no quiere/aún no aprueba plantilla, deja "No enviar plantilla" y el remarketing funciona solo con el Campo 3.
