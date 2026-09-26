# Formato por destino: en qué medida sale cada pieza y cuánto cuesta cambiarla

Añadido 2026-08-30 por el chat FILTRO (tabla de formato por red, del documento "Un post en
todas partes" de Maurys Alvarez). Su herramienta central (Metricool de pago, Make/n8n) **no se
trae**: no está contratada, y lo que Golden sí tiene montado publica por Composio.

🔴 **Reescrito el 2026-09-08 con el hallazgo del techo de nitidez.** Antes este archivo daba
una sola cifra base — 1080 — para las cinco redes, y el SKILL.md la extendía a todo con
"< 150 KB". Esa regla plana le ponía techo de nitidez a la galería de TODAS las fichas de la
casa. El tamaño ahora se decide **por destino**, no por costumbre.

## 🔴 Lo primero: el tamaño de SUBIDA es un techo permanente

**Medido en vivo contra el CDN de Shopify el 2026-09-08**, sobre una imagen real de la tienda
(600×600 de origen):

| Petición | Devuelve |
|---|---|
| sin parámetro | 600×600 · 47 KB |
| `?width=400` | **400×400 · 33 KB** — sí reduce |
| `?width=1024` | 600×600 · 47 KB |
| `?width=2048` | 600×600 · 47 KB |
| `?width=4000` | 600×600 · 47 KB |

**Shopify REDUCE al servir, pero NUNCA AGRANDA.** Pedir más de lo que se subió devuelve lo
subido, sin error y sin aviso. Consecuencia dura: **subir una galería a 1080 condena el zoom
de esa ficha a 1080 para siempre.** No se arregla con un parámetro, con un tema ni con una
app: se arregla **volviendo a subir**, es decir rehaciendo la pieza.

Por eso el peso no manda en la galería. Shopify ya sirve la variante liviana al móvil por su
cuenta a partir del original grande; lo que no puede hacer es inventar detalle que no subiste.

## La tabla que manda: medida por DESTINO

| Destino | Medida | Peso meta | Por qué esa y no otra |
|---|---|---|---|
| **Galería de ficha Shopify** | **2048×2048** | ~300 KB | El CDN sirve variantes livianas solo hacia abajo. Es el techo de zoom, permanente |
| **Infografía de la descripción** | **1080×1350** | **< 150 KB** | Va al HTML **sin pasar por transformación**: aquí el peso sí lo paga el comprador |
| Instagram feed · Facebook · Reddit | 1080×1350 (4:5) | < 150 KB | La red recomprime igual; subir más no compra nitidez |
| TikTok · reels · stories | 1080×1920 (9:16) | < 150 KB | |
| LinkedIn · Telegram · Threads | 1080×1080 (1:1) | < 150 KB | |
| YouTube · Google Business | 1920×1080 (16:9) | < 200 KB | |
| X · Pinterest | 1080×1620 (2:3) | < 150 KB | El menos usado de la casa |

**La distinción que hay que entender, porque es la que decide:** la galería pasa por el
transformador del CDN (`?width=`), la infografía de la descripción **no** — va incrustada en
el HTML tal como se subió. Por eso una sube grande y la otra baja apretada. **Una sola cifra
para todo optimiza el caso equivocado.**

El script ya trae estos destinos por nombre, y **no deforma nunca** (ver más abajo):

```bash
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py hero.png "TAG RECEDE - Galeria 01.webp" galeria-shopify
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py info.png "TAG RECEDE - Como actua 01.webp" ficha-html
```

**Para pauta manda la red, no esta casa.** El orden de importancia de Golden no es el del
documento de origen: el 74% del tráfico compra en móvil y el negocio corre en Meta, así que
**4:5 y 9:16 primero**. El 16:9 solo si hay pieza para YouTube o para la ficha de Google
Business.

## 🔴 El script deformaba el producto un 20% (medido y corregido el 2026-09-08)

Este archivo llegó a decir *"el script de la casa ya acepta cualquiera de estas medidas, no hay
que cambiarlo"*. **Era falso, y esa frase es justo la que impidió que nadie lo mirara.**

`optimizar-webp.py` hacía `im.resize(size)` a secas: estiraba hasta la medida pedida sin mirar
la proporción de origen. **Control con resultado conocido** (círculo perfecto de 1024×1024
llevado a 1080×1350): salió un óvalo de relación **0,800 — un 20% de deformación**.

Los motores entregan 1:1 o 2K cuadrado; la ficha pide 4:5. Es decir, **el caso deformado era el
caso normal**, no el raro. Y la Ley 1 de esta skill descalifica una pieza por envase deformado:
el jurado estaba castigando al motor por lo que hacía el script de entrega.

Ahora el script **no puede deformar**: escala conservando la proporción y luego
- `cover` (por defecto) — recorta el sobrante por el centro. Correcto para packshot de Golden,
  donde el producto va centrado y lo que sobra es fondo.
- `contain` — mete la pieza entera y rellena el borde. Cuando recortar se comería producto o texto.

Se comprueba solo: `optimizar-webp.py --autoprueba` (4 casos). **Muerde el caso malo** — el
estirón conocido lo sigue detectando con relación 0,800 — **y calla ante los buenos.** Un banco
que solo prueba el lado bueno no prueba nada.

## Lo barato es generar en la medida correcta, no arreglarla después

**Generar de nuevo en el ratio destino cuesta lo mismo que generar la primera vez.** Por eso el
ratio se decide **en el preflight**, antes de disparar la arena.

Si la pieza ya existe y hay que cambiarla, hay dos caminos y **no son lo mismo**:

- **Recortar** (crop). Gratis, local, instantáneo. Se pierden los bordes. Es el caso normal de
  un packshot de Golden, y es lo que hace el modo `cover` del script.
- **Rellenar** (`outpaint_image` imagen, `reframe` video). Cuesta créditos y lo inventa una IA.
  Conserva todo el original y fabrica los bordes nuevos. Solo vale la pena cuando recortar se
  comería producto o texto.

**Mira la pieza antes de elegir**: si el sujeto ocupa el centro, recorta y no gastes.

## Los dos instrumentos NO cubren los mismos formatos (medido contra el schema vivo, 30-ago)

| Formato | `outpaint_image` (imagen) | `reframe` (video) |
|---|---|---|
| 9:16 | sí | sí |
| **4:5** | sí | **NO** |
| 1:1 | sí | sí |
| 16:9 | sí | sí |
| **2:3** | sí | **NO** |

**Consecuencia operativa:** un video no se reencuadra a 4:5 ni a 2:3 con `reframe`, y 4:5 es
justo el feed de Instagram. Para llevar video a 4:5 el camino es **recorte con ffmpeg en
`golden-video-editor`**. Para imagen sí están los cinco.

`reframe` tope en **60 segundos**, y por encima de 15 s exige `duration_seconds` y `resolution`.

## Lo que cuesta, medido contra la cuenta real

Sacado con `get_cost:true`, que devuelve el precio **sin lanzar el job**:

| Reframe de video | Créditos |
|---|---|
| 15 s a 720p | **72** |
| 15 s a 1080p | **139,5** |
| 30 s a 1080p | **277,5** |

Sube en línea recta con la duración, y **720p cuesta cerca de la mitad que 1080p**.

⚠️ **El saldo era de 223,5 créditos (plan plus) el 30-ago.** Un reframe de 30 s a 1080p cuesta
277,5: **no alcanza**. A ese saldo caben uno de 15 s a 1080p, o tres de 15 s a 720p.
**Ese saldo es de hace más de una semana y otros chats gastan de la misma cuenta: está
CADUCADO.** Antes de ofrecer un reencuadre corre `balance` y `get_cost` y di el número de hoy.

**El costo de `outpaint_image` NO se pudo medir**: exige un `image_id` real ya subido y
confirmado, no acepta estimación en seco. Sin cifra hasta correrlo sobre una pieza de verdad.

## Lo que este archivo NO trae, y por qué

El documento de origen propone publicar en trece plataformas con un planificador de pago.
**Eso no se trae.** A cuántas redes se publica lo decide FER, no esta skill. Aquí solo queda
**en qué medida sale la pieza**, que es el trabajo de esta casa.

Las **zonas seguras** de cada red (cuánto tapa la interfaz de TikTok o Instagram encima del
video) **no están verificadas contra la documentación oficial de cada plataforma** y por eso no
se escriben como número. Regla provisional: en 9:16 no pongas texto ni logo en el quinto
superior ni en el cuarto inferior del alto.
