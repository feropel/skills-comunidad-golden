# Guía campo por campo — Generador de Anuncios

Pantalla: **Generador de Anuncios → [Producto] → "Generar Nuevo Anuncio"**.
Cada generación consume **1 crédito**. Llena bien los campos ANTES de generar: un campo
vacío o flojo = imagen floja = crédito perdido.

## Los campos, en orden

### Referencia (obligatorio)
El estilo/layout que Ecom Magic va a imitar.
- **"Seleccionar Plantilla"** (Galería EcomMagic) — elige un molde acorde al mensaje de la
  pieza. Ej.: grilla de beneficios, pack de precios, testimonio, antes/después, "cómo actúa".
- **"Subir desde PC"** — para replicar un molde propio del usuario.

**Heurística de molde por pieza (decide rápido, no preguntes):**

| Pieza / objetivo | Molde de referencia a buscar |
|---|---|
| Hero de beneficios (salud/estética natural) | checklist de beneficios con íconos, paleta natural |
| Antes/Después (resultado en piel/cuerpo) | split "Antes / Después" de la MISMA zona (mano/pie/piel), **no rostros**. ⛔ **Antes de elegir este molde, mira el VERTICAL** — ver el corte de abajo: en antiedad/arrugas/reafirmante y en pérdida de peso, este molde NO se usa |
| Cómo actúa / mecanismo | 3 pasos numerados con íconos |
| Pack de precios / oferta | grilla de packs 1/2/3 con precio tachado |
| Prueba social | testimonio con estrellas + foto |
| Ingredientes / composición | bote + lista de ingredientes con íconos |

### ⛔ CORTE DE ANTES/DESPUÉS POR VERTICAL (Meta 2026 — riesgo de cuenta)

La política de Meta **no trata igual todos los antes/después**. Verificado 2026-08-10:

| Vertical del producto | Antes/después |
|---|---|
| Antiedad, arrugas, reafirmante, lifting | **PROHIBIDO** — no lo generes |
| Pérdida de peso / adelgazamiento | **PROHIBIDO** — no lo generes |
| Salud bucal y claim de salud sensible | **PROHIBIDO** (norma Golden 2026-08-07) |
| Cosmética general (uña, cabello, mancha localizada) | Permitido con público 18+, misma zona, sin rostros y sin inducir rechazo del propio cuerpo |

Y sin excepción de vertical: **nada de segunda persona que señale la condición del
espectador** ("tu papada", "acabá con tus arrugas") ni titulares de plazo con resultado
("resultados en 7 días") — desde 2026 Meta evalúa el significado IMPLÍCITO, así que un
titular de plazo junto a un split de antes/después se lee como claim de transformación
engañoso aunque nunca aparezca la palabra "garantizado".

**Qué se pone en su lugar cuando el vertical está prohibido:** macro de textura, modo de
uso, mecanismo ilustrado ("cómo actúa"), ingredientes y lifestyle. Convierten y no arriesgan
la cuenta.

Filtra la galería por **"Belleza y Cuidado Personal"** para salud/estética (por la categoría
afín en otros verticales). Si el producto tiene identidad de color fuerte (ej. miel/amarillo),
prefiere un molde que **contraste** sin pelear con esa identidad.

### Foto del Producto (obligatorio)
De 1 a 3 fotos **reales** del producto. En Claude Code **la sube el usuario** arrastrándola al
recuadro "Imagen 1" (el sandbox bloquea la subida programática — el detalle y los otros entornos
están en `ui-navegacion.md` → "Subir la FOTO"). Usa la mejor foto limpia; si hay varias tomas
útiles, aprovecha las 3 ranuras.

### Tamaño de salida del anuncio (obligatorio)
Dropdown. Estándar Golden:
- **1080×1080 (Instagram Cuadrado)** → piezas de carrusel/multimedia Shopify.
- **1080×1350 (Instagram vertical)** → infografías de secciones.
Ajusta según la pieza que estés generando.

### Idioma del copy anuncio
**Español** por defecto (mercado LatAm).

### Modelo
Toggle **Ecom Magic** ↔ **GPT Image 2 (Nuevo)**. Por defecto Ecom Magic; prueba GPT Image 2
si quieres otra estética o el resultado no convence. (No cambia el costo: 1 crédito.)

### Personalización del Anuncio (toggle, déjalo ON)
- **"Desarrollar Ángulo de Ventas General con IA"** — la IA propone el ángulo.
- **"Seleccionar Ángulo de Venta Guardado"** — reutiliza uno guardado del producto.

### Adaptar Personajes (opcional)
Nacionalidad, Sexo, Rango de Edad de las personas que aparezcan en la pieza. Ajusta al
avatar real del producto (ej.: mujer 45-55 para un producto de menopausia).

### Detalles del Producto (máx. 700)
Datos duros: precios COD, presentación, envío, notas de composición. Ej. (con la moneda del
país que corresponda):
```
1 unidad — [precio]
2 unidades — [precio con descuento]
3 unidades — [precio mejor oferta]
Pago contra entrega · Envío gratis
```
Usa los datos REALES que dio el usuario. Este campo alimenta lo que la IA puede escribir.

### Ángulo de Venta (máx. 700)
A quién le hablas y desde qué deseo/dolor. Ej.: "Mujeres 45-55 con primeros síntomas de
menopausia que buscan alivio natural con respaldo científico."

### Problema específico que aborda el ángulo (máx. 700)
El dolor concreto y por qué las soluciones actuales no le funcionan.

### Avatar o Público Objetivo (máx. 700)
Descripción del comprador ideal (edad, contexto, nivel de consciencia, objeciones).

### Cómo el producto se vuelve la solución ideal (máx. 700)
Mecanismo de acción, por qué funciona mejor que alternativas, la transformación prometida.

### Instrucciones Adicionales (máx. 700)
El campo más útil para el control fino: precio exacto a mostrar, personaje, color, nombre
del producto, qué NO poner, jerarquía del texto. Ej.: "Muestra el precio grande abajo a la
derecha. No pongas testimonios. Título máximo 5 palabras. Paleta verde y blanco."

## Botón Generar

**"Generar Anuncio Profesional"** (dice "Esta generación consumirá 1 crédito"). Se habilita
cuando hay referencia + foto de producto. Genera **una pieza a la vez** y revísala.

También existe **"Descargar anuncios de forma masiva"** para bajar todo lo ya generado de un
producto de una sola vez.

## Cómo escribir el TEXTO que va dentro de la imagen

Tú escribes el copy de cada pieza (vía Instrucciones Adicionales / Detalles / Ángulo). Reglas:
- **Texto GRANDE y legible en móvil** (74% del tráfico LatAm es celular; la gente escanea,
  no lee). Poca palabra, alto contraste.
- **Una idea por pieza.** Hook arriba, beneficio/prueba en el cuerpo.
- **SIN botón ni CTA clickeable** (ley 4). Nada de "Compra aquí / Pide ya" dibujado como
  botón, ni número/keyword de WhatsApp incrustado. La imagen persuade; el CTA real + botón
  los pone golden-shopify DEBAJO. Puedes cerrar con un cierre emocional o de beneficio
  ("Verrugas fuera, piel libre"), pero nunca con un control que imite ser clickeable.
- **Respuesta directa** en el mensaje visual: hook → beneficio → prueba. Apóyate en
  `golden-copywriting` para ángulos si hace falta.
- **El precio** solo si la pieza es específicamente de oferta/pack y el usuario lo pide; si
  no, déjalo para el bloque nativo de golden-shopify (se edita sin regenerar).
- **Nada inventado**: precios, claims y garantías salen de los datos reales del usuario.
- **Coherencia de marca**: no metas amarillos gratis en fondos/diseño; respeta la paleta real
  del producto (si el producto ya es amarillo, como Tag Recede, eso es *producto fiel*, no la
  regla que se evita).

## Supervisión y arreglo

- **"Editar anuncio"** (en "Ver Anuncio") → instruye cambios concretos sobre una pieza ya
  generada ("quita X, pon Y, cambia color").
- **"Redimensionar"** → misma pieza en otro tamaño.
- **"Traducir"** → otra versión de idioma.
- **"Solicitar reembolso de crédito"** → si la pieza salió inservible, recupera el crédito.
