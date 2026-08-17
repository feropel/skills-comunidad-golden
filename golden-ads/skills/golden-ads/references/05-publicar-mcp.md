# Publicar por MCP (crear campañas en vivo) — con confirmación

Solo si el usuario pide montarlo en vivo. **Todo nace en PAUSA**; activar requiere su OK (REGLA 3).
Carga las tools del MCP de Meta con ToolSearch (`ads_*`).

## Orden de creación (todo PAUSED)
1. **Campaña** — `ads_create_campaign`
   - `objective`: solo ODAX → `OUTCOME_SALES` (COD/venta), `OUTCOME_ENGAGEMENT` o `OUTCOME_LEADS`
     según modelo, `OUTCOME_TRAFFIC` solo para pruebas baratas. `buying_type`: `AUCTION`.
   - **CBO vs ABO**: para escalar ganador → set `campaign_daily_budget` (CBO). Para **testear** →
     NO pongas budget en la campaña; ponlo en cada conjunto (ABO). (No mezclar: budget en campaña ⇒ CBO.)
   - `special_ad_categories`: `[]` salvo vivienda/empleo/crédito/política.
2. **Conjunto** — `ads_create_ad_set`
   - `optimization_goal`: usa el `recommended_optimization_goal` que devolvió la campaña (Compra →
     `OFFSITE_CONVERSIONS`; mensajes → `CONVERSATIONS` con `destination_type` WHATSAPP/MESSENGER).
   - `promoted_object`: requerido en conversiones → `{"pixel_id":"...","custom_event_type":"PURCHASE"}`.
   - `billing_event`: `IMPRESSIONS`. Presupuesto: `daily_budget` SOLO en ABO (no bajo campaña CBO);
     respeta `min_daily_budget_cents`. `targeting`: amplio → `{"geo_locations":{"countries":["CO"]},"age_min":..,"age_max":..}`
     (NO inventar IDs de interés; si quieres intereses, primero busca IDs reales). Advantage+ Audience
     queda activo por defecto (las edades pasan a "sugerencia" salvo que fijes `advantage_audience=0`).
3. **Creativo** — `ads_create_creative` (necesita `page_id`; imagen→`image_hash/url`; video→`video_id`
   + thumbnail; `message`/`headline`/`description`/`call_to_action_type`). IG: pasa `instagram_user_id`.
   - Copys de `golden-copywriting`; medios de golden-ugc-avatar/MCP (sube imagen/video primero).
4. **Anuncio** — `ads_create_ad` (referencia el creativo). Repite por cada variante.
5. **A/B test** (opcional) — `ads_experiment_abtest_create_test` para comparar ángulos/creativos.
6. **Públicos** (escala) — `ads_create_custom_audience` (LOOKALIKE de compradores, WCA, etc.).

## Confirmar y activar
- Muestra al usuario el **resumen** (objetivo, presupuesto, público, evento, creativos) y los IDs creados.
- **Solo con su "sí, actívalo"**: `ads_activate_entity` de campaña → conjunto → anuncio (los 3 niveles
  deben estar ACTIVE para entregar). Recuérdale que a partir de ahí **se gasta dinero real**.
- Tras crear, sugiere `ads_get_opportunity_score` para validar mejores prácticas antes de activar.

## Nunca
- Activar sin confirmación. Inventar IDs de pixel/página/interés. Poner budget en campaña Y conjunto
  a la vez. Saltarte el pixel/CAPI (sin señal, la campaña no optimiza).
