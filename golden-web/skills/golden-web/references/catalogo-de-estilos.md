# Catálogo de estilos: 26 direcciones ancladas, mapeadas a los clientes de Golden

Añadido 2026-08-26 por el chat FILTRO. **Esto NO copia nada**: apunta a un catálogo que ya vive
en el Mac, en la skill `web-design-engineer` (252 KB), que estaba instalada y que **ninguna skill
de Golden nombraba**.

Cada receta trae paleta con hex exactos, tipografía con tamaños y line-height, escala de
espaciado, radio, sombra, **movimiento con milisegundos**, los gestos que definen ese estilo, lo
que hay que EVITAR, y hasta una semilla de prompt para generar la foto de producto.

Ruta base: `~/.claude/skills/web-design-engineer/references/style-recipes/`

## Cuándo abrir el catálogo

| Situación | Qué leer |
|---|---|
| El cliente no sabe qué quiere ("hazme algo bonito") | `../design-directions.md` — conversación de 6 escuelas, se eligen 3 de filas distintas |
| El cliente tiene un ancla ("estilo Linear", "como Aesop") | **una** receta, directa |
| Hay escuela pero falta concreción | `style-recipes/INDEX.md` y de ahí 2-3 recetas |

## El mapa para los perfiles de ESTA skill

| Perfil de golden-web | Caso real de Golden | Recetas de primera elección |
|---|---|---|
| **MARCA PROPIA** (cuidado personal, cosmética) | Le'côterra, Toppik | `aesop` · `muji-kenya-hara` · `monocle-magazine` |
| **CREADOR DE CONTENIDO** (link-in-bio, portafolio) | marca personal, infoproducto | `stripe-press` · `are-na` · `notion-pre-ai` |
| **EMPRESA** (corporativo, servicios, captación) | Llanos Constructores | `pentagram` · `vignelli-swiss-helvetica` · `monocle-magazine` |

## Y para lo que esta skill NO construye, pero Golden sí tiene

| Encargo | Recetas | Skill dueña |
|---|---|---|
| Portal de comunidad con login, herramientas | `linear` · `vercel-mesh` · `raycast` | proyecto del portal |
| Panel de datos (gasto, pauta, logística) | `tufte-dataink` · `bloomberg-terminal` · `vignelli-swiss-helvetica` | los paneles |
| "Que pregunten qué agencia la hizo" | `active-theory` · `resn-storytelling` · `field-io` | **`golden-cinematica`** |

Ese último renglón importa: **`active-theory`** (momentos WebGL, interacción con física, transiciones
de cine) y **`resn-storytelling`** (narrativa por scroll, la recompensa por explorar) describen con
nombre y referente lo que `golden-cinematica` ya construye. Si el encargo llega en esos términos,
esa es la skill, no esta.

## Por qué `aesop` es la receta que más se va a usar aquí

Es la que mejor encaja con el negocio real de Golden: producto de cuidado personal, premium,
donde el producto es el protagonista. Trae, entre otras cosas:

- Fondo **chamois cálido `#E8E4D9`**, tinta `#1B1B1B`, salvia `#7A8470`, ámbar `#7A4623` muy medido
- Una sola serif transitional en todos los tamaños · cuerpo 16-18 px · interlínea ~1.65
- Espaciado 8 / 16 / 24 / 40 / 72 / 120 · **radio 0** · **sin sombras**
- **Movimiento: fundidos sutiles, cajón ~450 ms ease-out, nunca rebote de spring**
- Prohibido: negritas (todo regular e itálica), azules y morados, ventanas emergentes, y foto de
  modelo sonriendo — solo producto y utilería

Ese bloque de movimiento cumple solo el `estandar-movimiento.md` de esta skill: ease-out para
entrada, sin rebote, y una duración de marketing (450 ms) que es legítima porque no es interfaz.

## Cómo se encadena con lo que ya tenemos

- **Los números del movimiento** los pone `references/estandar-movimiento.md`. La receta dice
  "cajón lento"; el estándar dice con qué curva y por qué nunca `ease-in`.
- **La foto del producto** la produce `golden-imagen-arena`. Cada receta trae su semilla de prompt,
  y esa semilla se traduce a especificación técnica con `vocabulario-foto.md` (lente, esquema de
  luz con ángulo y ratio, superficie). La receta da la INTENCIÓN, el vocabulario da los NÚMEROS.
- **La voz y el producto** salen del cerebro de marca (`golden-brand-brain`), que esta skill lee
  en su Paso 0. La receta viste; el cerebro dice qué se está vistiendo.

## ⚠️ Los nombres NO salen al cliente

Esta skill tiene una regla de marca que manda sobre este archivo: **las direcciones se llaman
SIEMPRE Golden, y las referencias externas se analizan, se destilan y desaparecen.**

Los nombres de las recetas (`aesop`, `linear`, `stripe-press`) son **vocabulario interno** para
elegir y ejecutar con precisión. Al cliente jamás se le dice "te hice una web estilo Aesop": se le
presenta la dirección con nombre Golden y se le describe por lo que hace, no por a quién se parece.

Un cliente que oye el nombre de otra marca entiende que le copiaron algo. Y el valor de la receta
no es el nombre: son la paleta, la tipografía, el espaciado y el movimiento, que sí viajan.

## Regla de uso

Se elige **una** receta y se respeta entera, incluida su lista de prohibiciones. Mezclar la paleta
de una con la tipografía de otra y el movimiento de una tercera es exactamente lo que produce el
"look de plantilla" que estas recetas existen para evitar.

`web-design-engineer` trae además `references/advanced-patterns.md` (521 líneas: motor de línea de
tiempo de animación, marcos de simulación de dispositivo, panel de ajustes, emparejamientos de
color y tipografía) y `references/critique-guide.md` para criticar una página ya hecha.
