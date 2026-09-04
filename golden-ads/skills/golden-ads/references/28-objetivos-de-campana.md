# 28 · LOS OBJETIVOS DE CAMPAÑA — tabla de decisión (esto NO se pregunta dos veces)

Los 3 que usa Golden son **TRÁFICO · INTERACCIÓN · VENTA**. Este archivo dice, para cada uno, qué
enum va en la API, qué optimización, qué evento, qué destino y **cuándo se elige**. Si el usuario
nombra el objetivo, se traduce con esta tabla y **no se vuelve a preguntar**.

Enums ODAX verificados contra la Marketing API de Meta (`ad-campaign-group`, 2026-09-03). Los 6
existentes son `OUTCOME_SALES`, `OUTCOME_ENGAGEMENT`, `OUTCOME_TRAFFIC`, `OUTCOME_LEADS`,
`OUTCOME_AWARENESS`, `OUTCOME_APP_PROMOTION`. Golden opera los tres primeros.

---

## Los 3 de Golden

| Lo que dice el usuario | `objective` | `optimization_goal` | `promoted_object` / destino | Se mide por |
|---|---|---|---|---|
| **"venta"**, "ventas", "vender", "compras", "conversión" | **`OUTCOME_SALES`** | `OFFSITE_CONVERSIONS` | `{"pixel_id":"…","custom_event_type":"PURCHASE"}` | **Compras** y CPA vs breakeven |
| **"interacción"**, "mensajes", "WhatsApp", "que escriban", "conversaciones" | **`OUTCOME_ENGAGEMENT`** | `CONVERSATIONS` | `destination_type`: `WHATSAPP` (o `MESSENGER`) | **Conversaciones iniciadas** y su costo |
| **"tráfico"**, "visitas", "clics", "que entren a la página" | **`OUTCOME_TRAFFIC`** | `LANDING_PAGE_VIEWS` (mejor que `LINK_CLICKS`) | URL de destino | **LPV** y costo por LPV |

> **`LANDING_PAGE_VIEWS` antes que `LINK_CLICKS`**: el clic solo dice que tocaron; la LPV dice que la
> página **cargó**. Optimizar a clics compra clics baratos que nunca llegan (ver `19` velocidad de carga).

## Cuál elegir (criterio, no gusto)

- **VENTA** es el default de Golden siempre que **el pixel tenga señal de Compra**. Es el único
  objetivo que optimiza hacia gente que COMPRA. Requisito duro: pixel + CAPI con el evento probado
  (`23-salud-de-senal-y-andromeda.md`). Sin señal, Meta no puede optimizar a compra y el objetivo miente.
- **INTERACCIÓN** cuando la venta es **conversacional** (el cierre lo hace el bot/asesor en WhatsApp,
  Chatea PRO). Ojo: optimiza a que ESCRIBAN, no a que compren — el costo por conversación puede verse
  hermoso y el negocio perder si el bot no cierra. Por eso Chatea PRO debe **devolver la conversión a
  Meta** (`18` Set 3): con eso, Meta aprende de ventas y no solo de chats.
- **TRÁFICO** es el más barato y el que **menos vende**: sirve para pruebas baratas de creativo o para
  calentar un pixel nuevo. **No es objetivo de campaña de venta.** Si alguien pide "tráfico" esperando
  ventas, dilo: se está optimizando a la métrica equivocada.

## La compuerta del intake (`26`)
Si el usuario **dice el objetivo**, se traduce con la tabla y se sigue. Si **no lo dice**, se pregunta
así — con los tres, no con dos:
> "**Objetivo**: venta (compras en la web), interacción (que te escriban por WhatsApp) o tráfico
> (visitas a la página)?"

Y se INFORMA la traducción hecha, en una línea: *"Objetivo venta → `OUTCOME_SALES` optimizando a
`OFFSITE_CONVERSIONS` con el evento PURCHASE del pixel."*

## Consecuencias que arrastra el objetivo (por eso no se adivina)
Cambiarlo cambia **toda** la campaña: el evento de optimización, el destino del anuncio, el CTA del
creativo, las columnas con que se lee (`19`), el KPI del semáforo (`07`) y el breakeven contra el que
se compara (`12`). Montar con el objetivo equivocado no se arregla editando: **se rehace** (y editar
el conjunto reinicia el aprendizaje, `14`).

## Los otros 3 (existen, Golden casi no los usa)
`OUTCOME_LEADS` (formularios/lead ads) · `OUTCOME_AWARENESS` (alcance/recordación, marca grande) ·
`OUTCOME_APP_PROMOTION` (instalaciones de app). Si un caso los pide, se usan — pero no son el default
de una operación COD ni de marca propia.

Relacionado: `26-intake-montar-campana.md` (dónde se pregunta) · `05-publicar-mcp.md` (cómo se crea) ·
`18-columnas-ads-manager.md` (qué columnas lee cada objetivo) · `07-benchmarks-kpis.md` (su KPI).
