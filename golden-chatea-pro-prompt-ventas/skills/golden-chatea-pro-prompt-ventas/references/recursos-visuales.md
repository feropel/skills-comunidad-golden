# Recursos visuales: imágenes conversacionales y sus URLs

Objetivo: que el cliente NUNCA se quede trabado por una imagen. La skill intenta generarla; si no puede, le da un prompt profesional listo y le explica cómo subirla a Chatea para obtener la URL. En el PROMPT solo va la URL; las instrucciones y prompts de imagen van APARTE, debajo del prompt.

## Dos tipos de audiovisual (no confundir)
- **Multimedia INICIAL** (se envía al entrar, antes de la pregunta de entrada) → va en la sección "Contenido multimedia inicial" de Chatea, NO en el prompt.
- **Imágenes CONVERSACIONALES** (las que el agente envía DURANTE el chat cuando el cliente pregunta) → su URL va ESCRITA DENTRO del prompt, en el punto donde el agente la manda.

## Qué imágenes conversacionales suele necesitar un producto
Elige las que apliquen (no todas existen para todo producto):
1. **Modo de uso** — cómo se aplica/usa.
2. **Tabla de precios** — la promo de 1/2/3 unidades.
3. **Testimonios / reseñas** — prueba social.
4. **Antes / después** — resultados ilustrativos (con disclaimer, ver cumplimiento.md).
5. **Colores / variantes** — SOLO si el producto tiene variantes.
6. **Sellos / garantía / original** — confianza.

## Cómo queda en el PROMPT (solo la URL o el marcador)
Dentro del prompt, en el punto donde el agente la envía:
```
Si pide ver el modo de uso, envía: [IMAGEN 1 — URL]
Si pide ver reseñas, envía: [IMAGEN 2 — URL]
```
Cuando el cliente te dé la URL real, reemplaza `[IMAGEN N — URL]` por el enlace. Mientras no la tenga, deja el marcador etiquetado (no bloquea la entrega del prompt).

## MANIFIESTO DE IMÁGENES (va DEBAJO del prompt, en la entrega — nunca dentro del prompt)
Por cada imagen que el prompt usa, entrega al cliente este bloque:

```
IMAGEN 1 — Modo de uso
• Ya tienes la URL? → pégamela y la dejo lista en el prompt.
• No la tienes? Tienes dos caminos:
   A) Te la genero yo (si hay herramienta de imágenes conectada): la creo y te la entrego.
   B) La generas tú con este PROMPT DE IMAGEN listo para pegar en cualquier IA de imágenes:
      "<prompt de imagen profesional y específico para esta foto>"
• Luego: sube la imagen a Chatea PRO → Chatea te da una URL → pégamela y finalizo el prompt con la URL puesta.
```

## Flujo que sigue la skill (orden)
1. Al armar el prompt, LISTA las imágenes conversacionales que usará (numeradas: IMAGEN 1, 2, 3…).
2. Pregunta al cliente, imagen por imagen: **"tienes la URL de esta imagen?"**
3. Si la tiene → la pega en el prompt.
4. Si NO la tiene:
   a. **Intenta generarla la skill misma** si hay una herramienta de imágenes conectada (Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch u otra disponible por MCP). La crea y se la entrega al cliente.
   b. Si no hay herramienta o el cliente prefiere hacerlo él → le entrega el **PROMPT DE IMAGEN profesional** (ver plantilla abajo) para que lo genere en cualquier app.
   c. Le explica: **súbela a Chatea PRO → Chatea genera una URL → pásame esa URL** y yo dejo el prompt final con el enlace puesto.
5. El prompt se entrega funcional con marcadores `[IMAGEN N — URL]`; cuando lleguen las URLs, se reemplazan y queda 100% listo.

## Plantilla de PROMPT DE IMAGEN (para que el cliente genere fotos profesionales)
Rellena los [corchetes] según el producto. Foto real y fiel al producto, fondo limpio, texto sobrio (nada de amarillo chillón), formato vertical para WhatsApp.
```
Fotografía publicitaria profesional de [PRODUCTO: nombre y descripción física exacta: color, forma, envase], producto real y fiel (no rediseñar el empaque). [ESCENA: p. ej. sobre superficie limpia / mano aplicando / antes-después ilustrativo]. Iluminación de estudio suave, fondo [color/limpio], enfoque nítido en el producto, estilo e-commerce premium. Composición vertical 4:5 para WhatsApp. Espacio para un texto corto: "[TEXTO OPCIONAL: beneficio breve]". Alta resolución, realista, sin marcas de agua.
```
Reglas de la imagen (de las preferencias del negocio): producto fiel y real, WebP liviano (<150KB) cuando se pueda, nada de amarillo, texto compuesto sobre foto real (no IA que redibuje el producto).

## Recetario del SET completo (cuando el cliente NO tiene fotos)
Si el cliente no tiene ninguna foto, entrégale (o genera) un SET consistente de prompts, uno por pieza. Receta común: **fondo crema con degradado dorado suave, luz de estudio cálida, estilo gourmet/e-commerce premium, sin personas ni manos salvo que se indique, el texto en español va incrustado tal cual entre comillas, alta resolución.** Ajusta el aspect ratio a cada uso. Piezas típicas:
- **Hero (1080x1080)** — producto en primer plano mostrando su mejor atributo (relleno/textura/detalle), con overlay de nombre arriba y franja "ENVÍO GRATIS · PAGAS AL RECIBIR" abajo.
- **Grilla de variantes (1080x1080)** — todas las variantes/sabores/colores ordenados en cuadrícula limpia, con título "ARMA TU COMBO · N SABORES" (solo si hay variantes/combo mezclable).
- **Prueba social (1080x1080)** — tarjetas de reseña estilo WhatsApp con 5 estrellas doradas (texto de reseña genérico/editable) + titular con la cifra real ("MILES DE PEDIDOS AL MES").
- **Header Remarketing 1 y 2 (1200x628, 1.91:1)** — foto del producto SIN texto incrustado (el texto lo pone la plantilla de Meta); RM1 producto en detalle, RM2 presentación de regalo/aspiracional.
- **Video del "pull" (9:16, 8-15s)** — opcional para la multimedia inicial; cámara macro, cámara lenta suave, sin texto (para modelos de video; ver `golden-ugc-avatar`).
Recuerda: lo ideal siempre es FOTO REAL con texto compuesto encima; el set generado es el plan B cuando no hay fotos. El día que llegue una foto real, componer el texto sobre ella en vez de regenerar.

## Entrega en PDF (cuando el paquete se documenta)
Cuando el paquete se entrega también como PDF (ver `entrega-pdf.md`), estos prompts de imagen van en su propia sección del documento, cada uno en una tarjeta copiable, junto al manifiesto (qué imagen es, dónde va, cómo obtenerla).

## Multimedia INICIAL (las 3 piezas de entrada) — también las produce la skill
Además de las conversacionales, la skill ayuda con la multimedia inicial (la que se envía al entrar, va en "Contenido multimedia inicial", NO en el prompt). Recomendadas, en orden:
1. Imagen de producto + propuesta de valor (con "envío gratis / pago al recibir" visible).
2. Video corto (15-30s) de producto y uso — el que más convierte.
3. Imagen de prueba social (reseñas / "+N clientes").

Para cada una: si el cliente la tiene, que la use; si no, la skill **la genera** (imágenes con Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch; para el video, entrega guion/libreto o la genera si hay herramienta de video) o entrega el **prompt de imagen** listo. Respeta las preferencias del negocio (producto fiel y real, WebP liviano, nada de amarillo, texto compuesto sobre foto real).

## Regla de oro
La skill intenta hacerlo todo por el cliente. Si puede generar la imagen o el video, lo genera. Si no, entrega el prompt/guion perfecto + las instrucciones para subirlo a Chatea y obtener la URL. El cliente nunca se queda con "consigue una foto" sin saber cómo.
