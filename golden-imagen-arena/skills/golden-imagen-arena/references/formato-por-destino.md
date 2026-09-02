# Formato por destino: en qué medida sale cada pieza y cuánto cuesta cambiarla

Añadido 2026-08-30 por el chat FILTRO. Origen: el documento "Un post en todas partes"
(Maurys Alvarez) que FER trajo el 30-ago, del que se toma **la tabla de formato por red**.
Su herramienta central (Metricool de pago, y Make/n8n para el resto) **no se trae**: no está
contratada, y la publicación que Golden sí tiene montada va por Composio.

**Hueco medido antes de escribir esto.** Con `sinapsis.py`: la frase `formato por red social`
daba **0 de 93 skills**. Sobre esta skill: `9:16` cero menciones, `16:9` cero, `2:3` cero. El
prompt maestro solo ofrecía `{1080×1080 | 1080×1350}`, es decir cuadrado y vertical de feed.
**Faltaban tres de los cinco formatos**, incluido el vertical completo de reel y story, que es
donde vive el video corto.

## Los cinco formatos y a dónde va cada uno

| Relación | Píxeles base | Dónde se publica |
|---|---|---|
| **9:16** | 1080×1920 | TikTok · reels y stories · Discord · transmisión en vivo |
| **4:5** | 1080×1350 | Instagram feed · Facebook · Reddit |
| **1:1** | 1080×1080 | LinkedIn · Telegram · Threads |
| **16:9** | 1920×1080 | YouTube · Google Business |
| **2:3** | 1080×1620 | X · Pinterest |

El script de la casa ya acepta cualquiera de estas medidas, no hay que cambiarlo:

```bash
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py entrada.png salida.webp 1080x1920 150
```

**Para Golden el orden de importancia no es el del documento.** El 74% del tráfico compra en
móvil y el negocio corre en Meta: **4:5 y 9:16 primero**, que son feed de Instagram y reel.
El 16:9 solo cuando hay pieza para YouTube o para la ficha de Google Business. El 2:3 es el
menos usado de la casa y no justifica una generación aparte.

## Lo barato es generar en la medida correcta, no arreglarla después

La regla que decide: **generar de nuevo en el ratio destino cuesta lo mismo que generar la
primera vez.** Convertir una pieza ya hecha cuesta aparte. Por eso el ratio se decide **en el
preflight**, antes de disparar la arena, no al final.

Si la pieza ya existe y hay que cambiarla, hay dos caminos y **no son lo mismo**:

- **Recortar** (crop). Gratis, local, instantáneo. Se pierden los bordes. Sirve cuando el
  producto está centrado y sobra fondo, que es el caso normal de un packshot de Golden.
- **Rellenar** (`outpaint_image` para imagen, `reframe` para video). Cuesta créditos y lo
  inventa una IA. Conserva todo el contenido original y fabrica los bordes nuevos. Solo vale
  la pena cuando recortar se comería producto o texto.

De 16:9 a 9:16 recortando se pierden los lados. Rellenando se conservan. **Mira la pieza antes
de elegir**: si el sujeto ocupa el centro, recorta y no gastes.

## Los dos instrumentos NO cubren los mismos formatos (medido contra el schema vivo, 30-ago)

| Formato | `outpaint_image` (imagen) | `reframe` (video) |
|---|---|---|
| 9:16 | sí | sí |
| **4:5** | sí | **NO** |
| 1:1 | sí | sí |
| 16:9 | sí | sí |
| **2:3** | sí | **NO** |

**Consecuencia operativa:** un video no se puede reencuadrar a 4:5 ni a 2:3 con `reframe`,
y 4:5 es justo el formato del feed de Instagram. Para llevar video a 4:5 el camino es
**recorte con ffmpeg en `golden-video-editor`**, no esta herramienta. Para imagen sí están
los cinco.

`reframe` además tope en **60 segundos**, y por encima de 15 segundos exige declarar
`duration_seconds` y `resolution`.

## Lo que cuesta, medido hoy contra la cuenta real

Los tres puntos se sacaron con `get_cost:true`, que devuelve el precio **sin lanzar el job**:

| Reframe de video | Créditos |
|---|---|
| 15 s a 720p | **72** |
| 15 s a 1080p | **139,5** |
| 30 s a 1080p | **277,5** |

El precio sube en línea recta con la duración, y **720p cuesta cerca de la mitad que 1080p**.

⚠️ **El saldo de la cuenta el 30-ago era de 223,5 créditos, plan plus.** Un solo reframe de
30 segundos a 1080p cuesta 277,5: **no alcanza**. A ese saldo caben un reframe de 15 s a
1080p, o tres de 15 s a 720p. Antes de ofrecer un reencuadre de video, **corre `balance` y
`get_cost` y di el número**, igual que ya manda el preflight del paso 0.

**El costo de `outpaint_image` NO se pudo medir**: exige un `image_id` real ya subido y
confirmado, no acepta estimación en seco. Queda sin cifra hasta que se corra sobre una pieza
de verdad.

## Lo que este archivo NO trae, y por qué

El documento de origen propone publicar en trece plataformas con un planificador de pago.
**Eso no se trae.** Golden publica hoy en Instagram por Composio, y el propio documento avisa
de no automatizar trece plataformas de golpe sino probar con tres. La decisión de a cuántas
redes se publica es de FER, no de esta skill. Aquí solo queda **en qué medida sale la pieza**,
que es el trabajo de esta casa.

Las **zonas seguras** de cada red (cuánto tapa la interfaz de TikTok o de Instagram encima
del video) **no están verificadas contra la documentación oficial de cada plataforma** y por
eso no se escriben aquí como número. Regla provisional mientras tanto: en 9:16 no pongas texto
ni logo en el quinto superior ni en el cuarto inferior del alto.
