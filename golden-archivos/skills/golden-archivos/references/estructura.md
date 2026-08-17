# Estructura estándar y reglas de identidad

## Anatomía de una carpeta de producto

Este es el destino al que converge cualquier carpeta de producto. No todas las secciones existen siempre — crea solo las que reciban archivos.

```
<PRODUCTO>/
├── IMÁGENES/            fotos y creativos master (PNG/JPG pesados)
├── VIDEOS/              videos master (.mov, 4K, pesados)
├── GIFS/                animaciones
├── LOGOS Y MARCA/       identidad visual del producto
├── DOCUMENTOS/          fichas, prompts, informes, inventarios
├── DATOS Y EXCEL/       xlsx, csv, zips de datos
└── 🌐 WEB SHOPIFY/      lo ÚNICO que se sube: WebP + MP4 liviano
```

Cuando el producto tiene **sub-productos** (una línea con varias referencias), cada sub-producto es la unidad y lleva su propia estructura adentro. El prefijo de nombrado es el del sub-producto, no el de la línea: `BERGAMOT 36 - …`, no `LECOTERRA - …`.

Cuando ya existe una organización deliberada por orientación (`Img Cuadradas`, `Img Verticales`), por tamaño (`1080 x 1080`, `1080 x 1920 Historias`) o por propósito (`ADS`, `ANTES Y DESPUES`, `TESTIMONIOS`), **consérvala**. Es más informativa que la genérica.

## Regla de nombrado

```
<PRODUCTO> - <nombre original>.<ext>
```

El producto va **primero** para que el archivo siga siendo identificable aunque salga de su carpeta — que es exactamente el problema que resuelve. El nombre original se conserva porque su numeración suele cargar información (huecos = piezas faltantes).

Excepción: nombres crípticos sin valor (`IMG_4924`, UUIDs, `RPReplay_Final1622270379`). Esos se reemplazan por una descripción real, **obtenida mirando el archivo**.

## WEB vs MASTER

| | Formato | Destino | Uso |
|---|---|---|---|
| **Web** | WebP, MP4 < 10 MB | `🌐 WEB SHOPIFY` | Subir a la tienda |
| **Master** | PNG/JPG pesado, `.mov`, 4K | Carpetas de estudio | Editar, archivar |

El formato es la señal más confiable: WebP casi siempre significa "optimizado para subir".

Los creativos de **pauta** (anuncios) no van a `🌐 WEB SHOPIFY` aunque sean livianos: no son assets de ficha de producto y mezclarlos rompe el criterio de "todo lo que hay aquí se sube".

## Reglas de identidad entre productos

Dos nombres comerciales pueden ser el mismo producto físico. El criterio de asignación es **la marca visible en el creativo**:

- Si el creativo **no muestra marca** → sirve para cualquiera de los dos nombres; déjalo donde esté siendo usado.
- Si **muestra la marca** → pertenece a esa marca, sin discusión.

Productos que se parecen pero **son distintos** (misma categoría, distinta marca o distinta función) van siempre en carpetas separadas. Dos fibras capilares de marcas diferentes son dos productos. Un producto y su "optimizador" o accesorio son dos productos.

Estas equivalencias son conocimiento de negocio: **pregúntalas, no las deduzcas**. Un creativo mal asignado se propaga a la tienda y a la pauta.

## Carpetas vacías

Elimínalas, salvo cuando representen un **producto real que aún no tiene material**. Esas consérvalas y díselo al usuario: son el hogar esperando el contenido, y borrarlas hace perder la señal de que ese producto existe.

## Qué no es material de producto

No mezclar en el catálogo de productos:

- **Marca corporativa**: logos de la empresa, banners institucionales, fondos de videollamada, tarjetas de presentación, documentos legales
- **Informes y datos**: exports de ventas, informes de logística, análisis
- **Comunidad/formación**: material educativo, portadas de curso
- **Personal**: fotos, eventos, documentos privados

Cada uno merece su propia sección al mismo nivel que el catálogo, nunca dentro de un producto.
