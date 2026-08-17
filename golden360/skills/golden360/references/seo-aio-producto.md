# FASE 3 · Nombre y SEO/AIO del producto

Fase propia, no un apéndice del schema de la página. Aquí se decide **cómo se llama el producto en
todo el ecosistema** y cómo lo encuentran, tanto Google como los buscadores con IA.

Se decide **una sola vez** y se escribe al expediente; de ahí se propaga a archivos, imágenes,
campañas y bot.

## 1 · Nombre e identidad

| Campo | Regla |
|---|---|
| `nombre_oficial` | el de la etiqueta, literal |
| `nombre_comercial` | el que ve el cliente; puede sumar el beneficio, nunca contradecir la etiqueta |
| `handle` | minúsculas, sin tildes, con guiones; es la URL y no se cambia después |
| `alias_dropi` | todos los nombres con que figura en el proveedor |
| `slug_archivos` | prefijo de TODOS los archivos del producto |

El nombre comercial no puede prometer lo que la Compuerta 2 no respalda. "Crema con colágeno" cuando
el INCI no trae colágeno es un claim falso desde el título.

## 2 · SEO clásico

- **Título SEO**: nombre + beneficio principal + país o modalidad si aporta. Que quepa sin cortarse.
- **Meta descripción**: promesa + diferencial + llamada a la acción, escrita para que den clic, no
  para rellenar palabras clave.
- **Keywords**: las del **nicho** y sobre todo las del **dolor**, sacadas de la voz del cliente de la
  Fase 1. La gente busca su problema, no el nombre del producto que no conoce.
- **Tags** y **colección por necesidad** a la que entra el producto.
- **Alt text** de cada imagen: describe lo que se ve, con el nombre del producto, sin amontonar keywords.

## 3 · Capa AIO (buscadores con IA)

- **Respuestas extraíbles**: cada duda real del cliente resuelta en un pasaje corto y autocontenido,
  que una IA pueda citar sin tener que reconstruirlo del resto de la página.
- **Densidad de hechos**: datos concretos y verificables (contenido neto, activos con porcentaje,
  modo de uso, tiempo de resultado del fabricante) en vez de adjetivos.
- **Entidad clara**: marca, fabricante y producto nombrados de forma consistente en toda la página.
- **Schema JSON-LD** en su **sección invisible propia**, nunca dentro del FAQ: si el cliente apaga o
  mueve el FAQ, el SEO tiene que sobrevivir.

## 4 · Si la ficha ya existe (rama B)

Antes de reescribir, auditar lo que hay: título y meta actuales, handle (no se cambia si ya tiene
tráfico, se conserva), duplicados de la misma keyword en varias fichas, imágenes sin alt, y schema
mal ubicado o ausente. Se corrige lo que está mal y se conserva lo que ya rankea.

Herramienta opcional para la auditoría: `claude-seo-ai`.

## Checklist de cierre

- [ ] Nombre comercial y handle decididos y escritos al expediente
- [ ] Alias de Dropi mapeados
- [ ] Título SEO y meta descripción escritos
- [ ] Keywords del dolor, no solo del producto
- [ ] Colección y tags asignados
- [ ] Alt text de cada imagen
- [ ] Bloque de respuestas extraíbles y datos concretos para AIO
- [ ] Schema JSON-LD en sección propia, verificado
