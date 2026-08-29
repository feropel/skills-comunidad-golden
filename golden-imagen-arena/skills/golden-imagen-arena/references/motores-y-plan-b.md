# Los motores que hay de verdad, y qué hacer si el MCP se cae

Añadido 2026-08-26 por el chat FILTRO. Recoge dos destilados que estaban sueltos en
`STACK-GOLDEN/DESTILADOS/` sin que ninguna skill los nombrara:
`motores-generativos-quien-hace-que.md` y `higgsfield-api-directa-plan-b.md`.

## 1. Esta skill NO es el único motor de Golden

Hay dos plataformas pagadas y hacen cosas distintas. Saldo medido el 23-ago: Higgsfield **plan
plus, 459,75 créditos**; Ecom Magic **plan mentor, 202 créditos** (renuevan el 1 de cada mes).

**La regla del reparto:** si la pieza debe parecerse a un formato que ya funciona, la hace **Ecom
Magic** (el activo es la plantilla). Si necesita el producto REAL a medida, o movimiento, o
sonido, la hace **Higgsfield** (el activo es el motor). Se solapan en UNA sola cosa: la imagen de
anuncio estático, que es justo lo que hace esta arena.

Cuándo NO usar esta skill y usar Ecom Magic:
- **Anuncio sobre plantilla probada** → `banners_generate`, 1 crédito. Su catálogo tiene cientos de
  referencias y admite nivel de conciencia de Schwartz (`awareness_level`).
- **Sección de landing tipada** (hero, oferta, comparativa, testimonios, FAQ) → `landings_generate`.
- **Sección de LOGÍSTICA con transportadoras reales por país y sello contra entrega** → no existe
  en ningún otro lado.
- **Precio de venta óptimo COD** → `financial_analyze`, **gratis y sin IA**: devuelve precio para
  1/2/3 unidades, punto de equilibrio, ROAS de equilibrio y CPA objetivo, con flete, comisión de
  recaudo, cancelaciones y devoluciones.
- **Ángulo de venta y avatar desde 1-3 fotos** → `research_generic_angle`, **gratis**.

## 2. Hay 4 motores pagados que el MCP NO lista

Contrastado el catálogo del MCP (60 modelos inventariados el 23-ago) contra el RUNBOOK de un
cliente REST público:

| Endpoint REST | ¿Está en el catálogo del MCP? |
|---|---|
| `POST /veo3.1/fast/text-to-video` | **NO** — es Google Veo 3.1 |
| `POST /lightricks/ltx-2.5/text-to-video/pro` | **NO** |
| `POST /kling-video/v3.0/std/text-to-video` | **NO** (el MCP solo trae Kling O1 *Image*) |
| `POST /alibaba/qwen-image-3/text-to-image` | **NO** |
| `/nano-banana-2/lite/text-to-image` · `/openai/gpt-image-2` · `/minimax/h3/text-to-video` | sí |

**Sin verificar:** el RUNBOOK es de un tercero, no documentación oficial. Antes de dar por buenos
esos 4 hay que llamar la API con credenciales propias de FER.

## 3. El plan B: la API directa

Todo lo generativo de Golden entra hoy por el MCP de Higgsfield. **Si el MCP se cae, no hay
motor** — y no es hipotético: el 26-ago se desconectó y reconectó dos veces en una sola sesión.

    base: https://platform.higgsfield.ai
    auth: Authorization: Key <key_id>:<secret>
    body: {"prompt": "..."}  →  devuelve {request_id, status_url}

**El patrón de espera que conviene copiar** (y que aplica también al MCP cuando la arena lanza a
varios motores a la vez): polling con **retroceso exponencial y jitter** — arranca en 2 s,
multiplica por 1,5 hasta un tope de 10 s, y suma un aleatorio de hasta 0,5 s. Sin jitter, varias
generaciones en paralelo golpean la API en el mismo instante.

**Credenciales:** FER genera las suyas en Higgsfield y van a variable de entorno o al llavero.
**Jamás a un archivo del repositorio** — el repo del que salió este patrón dejó las suyas
expuestas en un `.env` commiteado, y por eso ese repo no se usa.

## 4. El costo por generación NO lo expone la API

Ni `models_explore --list` ni `--get` devuelven créditos por modelo. En Ecom Magic casi todo cuesta
**1 crédito por pieza** y se puede presupuestar; aquí solo se sabe generando. Por eso el
**preflight de créditos** (paso 0 del flujo) no es opcional.

También medido: los modelos marcados `supports_unlim` tienen hoy `unlim.available = false`.
