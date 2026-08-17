# Receta del MCP de Meta (lectura en vivo sin fallos)

Validado en cuenta real (GOLDEN CP8 COL, 2026-06-25). Sigue esta secuencia EXACTA para no fallar.
Las tools son deferred → cárgalas con ToolSearch (`ads`) antes de llamarlas.

## Secuencia de un diagnóstico en vivo (solo-lectura)
1. **`ads_get_ad_accounts`** → localiza la cuenta por nombre. Lee y respeta:
   - `is_ads_mcp_enabled` (si false → NO operar), `is_queryable` (si false → NO `ads_get_ad_entities`;
     muestra `not_queryable_reason`), `account_status` (DISABLED/UNSETTLED → avisar), `currency`
     (las cifras salen en esa moneda!), `min_daily_budget_cents`.
2. **`ads_get_ad_entities`** (nivel `campaign`, luego `adset`, luego `ad`) con `date_preset` (last_30d/
   last_7d) para traer métricas. Sin rango de fechas NO devuelve métricas, solo atributos.
3. **`ads_get_opportunity_score`** → recomendaciones de Meta (puede venir 100 sin recs = cuenta sana).
4. Según hallazgos: `ads_insights_performance_trend` (tendencia), `ads_insights_anomaly_signal`
   (fugas), `ads_insights_auction_ranking_benchmarks` (overlap), `ads_account_get_activity_logs` (qué cambió).

## ⚠️ CHULETA DE CAMPOS (nombres EXACTOS — el error #1 es inventarlos)
`ads_get_ad_entities` NO acepta `purchases` ni `cost_per_purchase`. Los válidos son:
- **Entrega**: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `cpp`, `reach`, `frequency`.
- **Conversión (ventas COD)**: **`actions:omni_purchase`** (nº de compras), **`purchase_roas`** (ROAS),
  **`results`** + **`cost_per_result`** (resultado según el objetivo; en ventas = compras y su costo).
- **Genéricos de conversión**: `conversions`, `cost_per_conversion`, `cost_per_action_type`.
- **Mensajes/tráfico**: objetivo `LINK_CLICKS` → `results` sale como "N (Link clicks)" y
  `cost_per_result` como costo por clic; `actions:link_click`, `cost_per_link_click`.
- **Video** (para fatiga/retención): `video_p25/50/75/95/p100_watched_actions`,
  `video_thruplay_watched_actions`, `cost_per_thruplay`, `3_second_video_plays`.
- **Atributos/estado**: `id`, `name`, `objective`, `status`, `effective_status`, `daily_budget`,
  `lifetime_budget`, `bid_strategy`, `buying_type`, `created_time`.
- **Set recomendado (ventas)**: `["id","name","spend","actions:omni_purchase","results","cost_per_result","purchase_roas","ctr","cpm","frequency","objective"]`.
- **Si dudas de un campo → llama `ads_get_field_context` ANTES**, o pide un set mínimo y crece. Un
  campo inválido **tumba toda la llamada** (error VALIDATION que lista los válidos — úsalo).

## Lectura de la respuesta (formato real)
- Montos vienen formateados con la moneda: `"$ 5.575.906 COP"`. Parsea el número, NO asumas USD.
- `results`/`cost_per_result` vienen anidados: `{value:[{indicator:"actions:purchase",values:[{value:232}]}]}`.
- `"Not available"` en `actions:omni_purchase`/`purchase_roas` = esa campaña no registró compras (0 o sin señal).
- `effective_status` puede venir "Not available" a nivel agregado → si necesitas activo/pausado real,
  consulta a nivel campaña sin rango de fechas o con `status`/`effective_status` directos.

## Banderas automáticas al leer
- **Nombres duplicados** (varias campañas con el MISMO nombre, ej. tres "OPEN 6") → higiene: renombrar
  y comparar cuál rinde; casi siempre una es un duplicado que sangra presupuesto.
- **ROAS "Not available" con gasto** = quema sin señal de compra → revisar pixel/CAPI o pausar.
- **Cuenta DISABLED/UNSETTLED** = avisar al usuario (pauta pausada por Meta / pago pendiente), no intentar escribir.
- **Churn de encendido/apagado o reglas de "apagar al gastar X"** en `ads_account_get_activity_logs`
  (eventos `update_ad_set_run_status` repetidos, saltos de `budget`) = **reinicios de fase de
  aprendizaje** → fuga clásica que encarece. Marcar y explicar el fix (`14-fase-aprendizaje.md`).
