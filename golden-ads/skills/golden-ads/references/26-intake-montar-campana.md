# 26 · INTAKE y secuencia para "crea una campaña de [objetivo] de [producto] con presupuesto de [valor]"

**Orden de FER (2026-09-03):** *"si le pido a un chat nuevo crear una campaña de [objetivo] de
[producto] con un presupuesto de [valor], estos campos si no se los doy me los debe pedir"*.

Este archivo es el **portero y el índice** del pedido más común. No repite lo que ya está escrito:
manda a cada especialista en el orden correcto. Nace de 3 fallas medidas en campo el 2026-09-03.

---

## PASO 1 · LOS 3 CAMPOS — si falta uno, se PREGUNTA (no se asume)

| Campo | Por qué es obligatorio | Si no lo dan |
|---|---|---|
| **OBJETIVO** | **tráfico · interacción · venta** → tabla de traducción en `28-objetivos-de-campana.md`. Define el ODAX, la optimización, el evento y el destino: adivinarlo obliga a REHACER la campaña | **PREGUNTAR** (los 3, no 2) |
| **PRODUCTO** | sin él no hay ángulo, ni breakeven, ni reglas de marca que respetar | **PREGUNTAR** |
| **PRESUPUESTO** | monto **y** si es diario o total. Ver PASO 2: aquí se cometió el error de los 100× | **PREGUNTAR** |

**Se preguntan los tres JUNTOS, una sola vez, y se arranca:**
> "Para montarla necesito 3 datos: **objetivo** — venta (compras en la web), interacción (que te
> escriban por WhatsApp) o tráfico (visitas) —, **producto** exacto, y **presupuesto diario** con su
> moneda. Con eso arranco."

**Lo que NO se pregunta** (autonomía Golden: se decide por convención y se INFORMA): estructura
ABO/CBO, edades de arranque (25–44, `07`), público (Advantage+), ubicaciones, naming (`reference_naming_campanas_meta`),
puja. **Lo que se deduce solo:** cuenta (si hay una operativa o la nombraron), país/moneda (de la
cuenta), pixel y página. Preguntar lo que ya está en el chat o en memoria es fuga, no cortesía.

---

## PASO 2 · 🔴 PRESUPUESTO — la compuerta de los 100×

Regla completa en **`reglas-de-oro.md` §5**. Resumen operativo, obligatorio:

1. `ads_get_ad_accounts` → lee `currency` y **`min_daily_budget_cents`** (el testigo).
2. **Escribe el renglón del cálculo ANTES de mandar nada:**
   > "Cuenta en COP (mínimo 3.076 → moneda sin decimales) → $50.000/día se manda como `daily_budget: 50000`."
   - `min_daily_budget_cents` ≈ **100** → CON decimales (USD/EUR/MXN/PEN/BRL) → **×100**
   - `min_daily_budget_cents` ≈ **3.000+** → SIN decimales (**COP/CLP/PYG**) → **×1**
3. Tras crear: **relee `daily_budget` del servidor** y compáralo con lo pedido. Si no coincide,
   `ads_update_entity` y **releer otra vez**.

> **Incidente real:** se pidieron $50.000/día y quedaron **$5.000.000** (×100 "por centavos"). El
> parámetro se llama `_cents` y **miente** en monedas de cero decimales. Nunca reportes un
> presupuesto que no leíste de vuelta del servidor.

---

## PASO 3 · CONTEXTO — que la campaña coincida con la investigación previa

- **Si existe investigación** (`PROYECTOS/<PRODUCTO>/` de `golden-investigacion-mercado`): **LÉELA
  ANTES de estructurar**. De ahí salen los ángulos (= los conjuntos), la persona, las objeciones,
  la oferta y el tono. **La estructura se adapta al creativo**, pero los ángulos vienen de ahí.
- **Si no existe**: dilo y sigue con los ángulos que se ven en el creativo + Ad Library. No bloquees.
- **Reglas de marca del producto**: viven en la memoria de la casa. **Leerlas antes de redactar**
  (`25` Paso 4, prueba 5) — un copy que viola el posicionamiento no se publica.
- **Breakeven y modelo de pago** (`12`, REGLAS 2 y 9): pídelos; si faltan, `[PENDIENTE]` y sigue.
- **Momento/temporada** (`21` §4): si entra una temporada relevante, ajusta el ángulo y dilo.

---

## PASO 4 · CREATIVO Y COPYS → todo el detalle en `25-cuenta-sin-creativos.md`

No se duplica aquí. Secuencia obligatoria de ese archivo:
1. **Medir** si la cuenta ya tiene material (`ads_get_ad_videos` / `ads_get_ad_images`) — "vacía"
   casi nunca es cierto.
2. **Meter el medio**: `ads_creative_upload_media` (las `upload_image`/`upload_video` están
   **DEPRECADAS**). Vía URL pública = Claude lo hace solo; archivo del Mac = lo elige el usuario.
3. 🔴 **ANALIZAR el video viéndolo Y ESCUCHÁNDOLO** (transcripción local / `golden-video-teardown`).
   Copy escrito sin escuchar el video es copy inventado.
4. **15 copys por pieza** (5 textos + 5 títulos + 5 descripciones · 125/40/25) con
   `golden-copywriting`, y las **6 pruebas de coherencia** con ese creativo.
5. **Montar y VERIFICAR con los ojos**: `ads_get_ad_preview` y entregar el `preview_url`.

> ⚠️ **Por qué "no suben los 15 copys" (tope MEDIDO, no bug):** `ads_create_creative` expone
> `message`, `headline` y `description` **en singular** — **no expone `asset_feed_spec`**. Por API
> salen **1+1+1**. Los 15 se entregan igual en el chat/documento y **se cargan en el panel** como
> opciones múltiples del anuncio. **Decirlo siempre en el reporte como pendiente, nunca callarlo
> ni entregar solo 3 copys.**

---

## PASO 5 · MONTAJE, UTM Y CIERRE
- **Montaje** → `05-publicar-mcp.md` (campaña → conjunto → creativo → anuncio, todo **PAUSED**).
- **UTM** → `24-utm-atribucion.md` (REGLA 18). Por MCP el anuncio nace sin UTM: se pegan en el panel
  antes de activar. CTWA exento.
- **Salud de señal** → `23-salud-de-senal-y-andromeda.md` (CAPI, dedup, EMQ) antes de leer resultados.
- **Auto-check** → `13-auto-check.md` (incluye la relectura del presupuesto).
- **Seguimiento** → `20-seguimiento.md`. **Activar solo con OK explícito** (REGLA 3).

## Qué se reporta al entregar (con evidencia, no con intención)
IDs creados · **presupuesto RELEÍDO del servidor** · `preview_url` de cada anuncio · los 15 copys
por creativo en bloques copiables (REGLA 15) · lo que quedó pendiente para el panel (los 15 en
`asset_feed_spec`, UTM) · y el plan de seguimiento.
