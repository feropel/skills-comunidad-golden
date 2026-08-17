# Columnas del Ads Manager en ORDEN DE EMBUDO (para analizar bien)

La mayoría analiza con las columnas por defecto y se pierde. El orden correcto es **el del embudo**:
seguir el dinero desde que se muestra el anuncio hasta la venta. Así se ve **dónde se cae**.

> ⚠️ **Los presets de columnas son POR CUENTA, NO se comparten** (verificado en vivo 2026-06-25 en
> CP1/CP5/CP6 del usuario). Cada cuenta guarda sus propios presets, a menudo con nombres distintos
> (`FER 2026`, `GOLDEN 2026`, `GOLDEN 2025`, `Fer 2025`) y desactualizados. Resultado: cuentas sin
> unificar. Recomendación experta: **estandarizar por OBJETIVO de la cuenta, no un preset idéntico** →
> cuentas de **venta web/COD** usan el Set 1 (embudo web, FTIR); cuentas de **WhatsApp/mensajes** usan
> el Set 3 (costo por conversación). Nombra igual en todas (ej. "GOLDEN WEB" / "GOLDEN WHATSAPP") y
> revisa que la cuenta tenga ACTIVO el preset correcto (muchas tienen el viejo puesto teniendo el nuevo).
> Por navegador SÍ se puede seleccionar/reconstruir el preset; por MCP no.

> ⚠️ **Honestidad de capacidad**: el MCP de Meta **NO puede** cambiar la "vista de columnas guardada"
> de tu Ads Manager (eso es interfaz, no API). Lo que SÍ hacemos: (a) darte el **preset exacto** para
> guardarlo una vez en Ads Manager (Columnas → Personalizar columnas → Guardar como preset), y (b)
> **sacarte los datos ya en este orden** por MCP cuando quieras (con los `fields` de abajo).
> A pedido ("dame las columnas que debe tener la cuenta") → genera un **documento** con estos 3 sets.

## ⭐ SET MAESTRO GOLDEN (absorbido del preset real del usuario 09.2025 + mejoras)
Estas son las **26 columnas personalizadas reales de Golden** (preset "Métricas Personalizadas") +
**6 mejoras** que faltaban (marcadas ➕). Es el set autoritativo; los 3 sets de abajo son el "por qué".
Ordenado por embudo. Nombre → fórmula/config.

**Entrega/costo:** Entrega · Presupuesto · Importe gastado · **CPM** · **Frecuencia**
**Clic/gancho:** **CTR único** (clics únicos enlace ÷ impresiones, %) · **CPC** · Clics únicos en el
enlace · Interacción con la página · Clics a la tienda
**Video (si aplica):** Reproducción 3s · ➕ **Hook rate %** (3s ÷ impresiones) · Reproducción 50% ·
Reproducción 100% · ➕ **Hold rate %** (100% ÷ 3s) · ➕ **ThruPlay + costo/ThruPlay**
**Landing:** Visitas a la página de destino (LPV) · **Velocidad de carga %** (LPV ÷ clics enlace) ·
➕ **Agregar al carrito + costo** · Pagos iniciados
**Conversión/venta:** Compras · Resultados · Costo por resultado · **CPA final** (gasto ÷ compras) ·
**Tasa conversión compras %** (compras ÷ clics) · **Ticket promedio** (valor ÷ compras) · ROAS ·
**ROAS de compras** · **Tasa de CPA %** (CPA ÷ ticket promedio ≈ inverso del ROAS) ·
➕ **ROAS pagado (COD)** = ROAS × % entrega *(NO es columna de Ads Manager — cálculo en el análisis)*
**Saturación/frescura:** **FTIR** (First Time Impression Ratio — % de impresiones que fueron la 1ª vez
que la persona vio el anuncio; alto = llegando a gente nueva, cayendo = fatiga → sube CPA). Verificado
en la cuenta real del usuario (preset FER 2026); es de las métricas pro más valiosas para escalar COD.
**WhatsApp (Chatea PRO):** ➕ **Conversaciones iniciadas** · ➕ **Costo por conversación** ·
**Tasa conversión WhatsApp %** (eventos WhatsApp ÷ clics enlace)
**Diagnóstico subasta:** ➕ **Clasificación de calidad / interacción / conversión**
**Ident:** Identificador del anuncio

> Las 6 ➕ son mi recomendación experta sobre el preset del usuario: hook/hold rate (tenía el 3s/100%
> crudos, no las tasas), costo por conversación WhatsApp (tenía la tasa, no el costo), ATC (escalón
> faltante), clasificaciones (subasta) y ROAS pagado COD. Al aplicar: es preset de UI → se guarda a
> mano en Ads Manager (el MCP no fija la vista); por MCP se sacan los datos ya en este orden.

## SET 1 — VENTA WEB / COD (el orden perfecto para analizar)
| # | Columna (Ads Manager) | Campo MCP | Qué diagnostica |
|---|---|---|---|
| 1 | Presupuesto | `daily_budget`/`lifetime_budget` | cuánto se está arriesgando |
| 2 | Importe gastado | `spend` | gasto real |
| 3 | Impresiones | `impressions` | volumen de entrega |
| 4 | CPM (costo x 1.000) | `cpm` | qué tan cara está la subasta |
| 5 | Frecuencia | `frequency` | fatiga (>2–3 = quemando) |
| 6 | Clics en el enlace | `actions:link_click` | interés real |
| 7 | CTR (link) | `ctr` | fuerza del gancho/creativo |
| 8 | CPC (link) | `cost_per_link_click` | costo del clic |
| 9 | Visitas a la página de destino (LPV) | `results` (LPV) | el clic llega y carga? |
| 10 | % de conexión (LPV ÷ clics) | *(calculado)* | velocidad/coherencia de landing |
| 11 | Pagos iniciados (Checkout) | `actions:omni_initiated_checkout` | intención de compra |
| 12 | **Compras** | `actions:omni_purchase` | la venta |
| 13 | **Costo por compra (CPA)** | `cost_per_result`/`cost_per_action_type` | vs breakeven → gana/pierde |
| 14 | **ROAS de compra** | `purchase_roas` | retorno (descontar entrega COD!) |
| 15 | CVR (compras ÷ LPV) | *(calculado)* | poder de cierre de la página |
| 16 | Clasificaciones (calidad/interacción/conversión) | *(ranking)* | vs competencia en subasta |

## SET 2 — LANDING / WEB con CREATIVO DE VIDEO (añadir métricas de video)
Mismo embudo del Set 1 + **antes del clic**, la salud del video (donde se gana o pierde el scroll):
| Columna | Campo MCP | Diagnostica |
|---|---|---|
| Reproducciones de 3s | `3_second_video_plays` | el hook frena el scroll? |
| **Hook rate** (3s ÷ impresiones) | *(calculado)* | fuerza de los primeros 3s |
| ThruPlays | `video_thruplay_watched_actions` | retención real |
| Reproducciones al 25/50/75/100% | `video_p25/p50/p75/p100_watched_actions` | dónde abandonan |
| **Hold rate** (100% ÷ 3s) | *(calculado)* | qué tan completo se ve |
> Un CTR alto con hook rate/hold bajos = clickbait que no convierte. Video primero, luego el embudo web.

## SET 3 — WHATSAPP / MENSAJES (venta por Chatea PRO → Meta)
En venta conversacional el evento clave NO es "compra web" sino **conversación** — y **Chatea PRO
envía la CONVERSIÓN (venta) de vuelta a Meta** (por CAPI/eventos), así que Meta también mide la compra.
| # | Columna | Campo MCP | Diagnostica |
|---|---|---|---|
| 1 | Importe gastado | `spend` | gasto |
| 2 | Impresiones / CPM | `impressions` / `cpm` | entrega |
| 3 | Clics / CTR | `clicks` / `ctr` | gancho |
| 4 | **Conversaciones iniciadas** | `actions:onsite_conversion.messaging_conversation_started_7d` | cuántos escriben? |
| 5 | **Costo por conversación** | `cost_per_action_type` (messaging) | eficiencia de entrada al chat |
| 6 | **Compras (que reporta Chatea PRO)** | `actions:omni_purchase` / conversión custom | la venta real |
| 7 | **Costo por compra (CPA)** | `cost_per_result` | vs breakeven |
| 8 | ROAS | `purchase_roas` | retorno (×entrega) |
| 9 | Tasa conversación→venta | *(calculado)* | qué tan bien cierra el bot/asesor |
> Requisito: Chatea PRO debe estar **enviando la conversión a Meta** (evento/CAPI configurado). Si no,
> Meta solo ve "conversación" y optimiza a chats, no a ventas → hay que conectarlo (bandera en diagnóstico).

## Regla
Al analizar cualquier cuenta, ORDENA la lectura por embudo (Set según el modelo) y **localiza el
escalón donde se cae** (CTR bajo=creativo · LPV≪clics=landing · conversación sin venta=cierre/bot).
