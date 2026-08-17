# Paso 0 — Detectar e ingerir la fuente de datos

Determina con qué trabajas, en este orden de preferencia. Declara la fuente y sus límites.

## A) Conexión EN VIVO a Meta (MCP) — preferida
El entorno tiene un **MCP de Meta Ads** (Facebook) conectado. Sus tools están "deferred": cárgalas
con **ToolSearch** (`select:ads_get_ad_accounts,ads_insights_performance_trend,...` o keyword `ads`).
1. `ads_get_ad_accounts` → lista cuentas (id, nombre, business, moneda, `is_ads_mcp_enabled`,
   `min_daily_budget_cents`). Si `is_ads_mcp_enabled=false`, no operes esa cuenta.
2. `ads_get_ad_entities` → campañas/conjuntos/anuncios con su estado y config (si `is_queryable`).
3. Insights y diagnóstico (ver `02-diagnostico.md`): `ads_insights_performance_trend`,
   `ads_insights_anomaly_signal`, `ads_insights_industry_benchmark`,
   `ads_insights_auction_ranking_benchmarks`, `ads_get_opportunity_score`,
   `ads_account_get_activity_logs`, `ads_insights_advertiser_context`.
4. Inteligencia competitiva: `ads_library_search` (anuncios activos del nicho/competidores).
5. Escritura (con confirmación, ver `05-publicar-mcp.md`): `ads_create_campaign/ad_set/creative/ad`,
   `ads_create_custom_audience`, `ads_experiment_abtest_create_test`, `ads_activate_entity`.

> Ventaja: datos reales + capacidad de montar/optimizar en vivo. Es el modo ideal.

## B) Informe exportado (Excel/CSV/PDF de Ads Manager)
El usuario sube el archivo. Para el análisis profundo (unit economics + semáforo 🔴🟡🟢, ranking de
campañas/creativos, demografía, ubicaciones, plan campo por campo) **delega en
`golden-meta-ads-analysis`** (está hecho exactamente para eso) o `3qs` (metodología 3 Q's).
- Pide que el export traiga: nivel (campaña/conjunto/anuncio), gasto, impresiones, CTR, CPC, CPM,
  compras/resultados, CPA, ROAS, frecuencia, fechas. Si faltan columnas, dilo.
- Cruza con unit economics (REGLA 2) para convertir métricas en veredicto de rentabilidad.

## C) SIN datos (producto nuevo a testear)
No hay cuenta ni informe. Se trabaja en **Modo B (testeo)** → `04-build-sin-metricas.md`:
toma la investigación (de `golden-investigacion-mercado`) o investiga lo mínimo (ángulos, persona,
objeciones, oferta) + mira anuncios activos del nicho con `ads_library_search` / Meta Ad Library.

## D) Cuando HAYA data de PEDIDOS reales, cruza con ella (manda sobre las impresiones)
> **Aplica SOLO si hay data real/histórico** (la excepción: producto ya vendido o relanzamiento a otro
> país). Para producto **NUEVO sin datos — el caso normal — el default es Modo B (testeo)** y **NO se pide
> ni se asume métricas**: se testea y la data llega después. Lo de abajo es para cuando esa data ya existe.

La demografía de la **cuenta de pauta** (breakdowns de impresiones/compras que da Meta) está
**contaminada** por la segmentación que ya aplicaste — es self-fulfilling, refleja a quién le mostraste,
no necesariamente a quién compra. Por eso, cuando exista, **cruza con la data de PEDIDOS real**
(export **Dropi** / **Chatea** / **CRM**) y deja que esa data mande:
- **Género inferido por nombre** del comprador (quién paga de verdad, no a quién impactó Meta).
- **Mezcla de producto** (qué variante/fragancia se lleva la mayoría de los pedidos).
- **Combo attach** = unidades por pedido (palanca de rentabilidad — ver `12-unit-economics.md`).
- **Geo** real de entrega (ciudad/departamento) y **tasa de entrega por transportadora** (ver `17`/`12`).
- Herramienta: **`golden-dropi-analisis`** consolida los exports COD y saca justo estos cortes.

> Jerarquía de verdad: **PEDIDOS reales > breakdowns de la cuenta**. Si la cuenta dice "90% mujeres" pero
> los pedidos de la línea masculina son 90% hombres, mandan los pedidos. Reporta ambos y decide con el pedido.

## Qué confirmar siempre (pendientes bloqueantes)
- **Cuenta y país/moneda.** **Producto: costo, precio, margen, breakeven** (REGLA 2).
- Objetivo del negocio (vender COD / mensajes WhatsApp / leads). Presupuesto disponible.
- Pixel/CAPI o Events configurados (si no, es lo primero a resolver — sin señal no hay optimización).
