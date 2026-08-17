# Modo A — Diagnóstico con datos reales

Objetivo: convertir las métricas en un **veredicto de rentabilidad** y una lista de acciones. Siempre
sobre datos reales (REGLA 1) y contra el **breakeven** del producto (REGLA 2).

> Antes de leer la cuenta: sigue la **receta exacta del MCP** (`11-mcp-meta-recipe.md`) para no fallar
> con los nombres de campo, y ten la **calculadora de breakeven COD** (`12-unit-economics.md`). Al
> cerrar corre el **auto-check** (`13`). Estándar de entrega: `examples/EJEMPLO-diagnostico.md`.

## 0. El dato es CONFIABLE? (REGLA 12 — antes de concluir nada)
Filtra por **significancia** antes de dar veredicto. Una entidad es concluyente si: **gasto ≥ 2–3× CPA
objetivo Y ≥ ~15–30 compras Y ≥ 3–4 días** (fuera de aprendizaje). Si no llega:
- Márcala **"señal temprana (dato insuficiente)"**, NO la pauses/escales en firme.
- Apóyate en lo que **de verdad convertiría**: histórico más amplio de la cuenta/producto, la
  investigación, y señales que estabilizan rápido (CTR, hook rate, CPC) — no un CPA con 2–3 ventas.
- Reporta el **nivel de confianza** de cada campaña (🟢 confiable / 🟡 parcial / ⚪ insuficiente).

## 1. Fijar el marco económico (antes de mirar métricas)
- Breakeven CPA = margen bruto por unidad (precio − costo − envío/COD − devoluciones).
- Breakeven ROAS = precio / margen bruto. En COD, multiplica por la **tasa de entrega efectiva**.
- Toda métrica se juzga contra esto: un CPA "bueno" es el que está bajo el breakeven, no un número genérico.

## 2. Lectura de la cuenta (MCP en vivo)
| Pregunta | Herramienta | Qué leer |
|---|---|---|
| Cómo viene la tendencia? | `ads_insights_performance_trend` | CPA/ROAS/CTR/CVR en el tiempo (mejora o empeora) |
| Hay fugas/anomalías? | `ads_insights_anomaly_signal` | gastos disparados, caídas de CVR, picos de CPM |
| Cómo voy vs pares? | `ads_insights_industry_benchmark` | CPA/CTR vs advertisers similares (mismo goal) |
| Compito conmigo mismo? | `ads_insights_auction_ranking_benchmarks` | overlap de subasta → consolidar conjuntos |
| Qué recomienda Meta? | `ads_get_opportunity_score` | mejores prácticas faltantes |
| Qué cambió y cuándo? | `ads_account_get_activity_logs` | cambios que rompieron algo — **en especial apagados/encendidos repetidos y saltos de presupuesto = reinicios de aprendizaje** (ver `14`) |
| Mi contexto/funnel? | `ads_insights_advertiser_context` | objetivo correcto para el negocio |

Pide insights por **nivel**: campaña → conjunto → anuncio (3 llamadas), para ubicar dónde está el dinero.
**Lee las métricas en ORDEN DE EMBUDO** (`18-columnas-ads-manager.md`) — según el modelo (venta web,
video o WhatsApp/Chatea PRO) — para ver en qué escalón se cae. A pedido, entrega el preset de columnas.
**Siempre** revisa el activity log buscando **churn de encendido/apagado** o reglas automáticas de
"apagar al gastar X" — es una fuga clásica de COD que encarece todo (`references/14-fase-aprendizaje.md`).

## 3. Ranking y clasificación (semáforo)
Clasifica cada entidad contra breakeven:
- 🟢 **GANA** (CPA < breakeven, ROAS > breakeven, volumen): candidata a **escalar**.
- 🟡 **LÍMITE** (cerca del breakeven): **optimizar** (creativo/segmentación/puja) antes de decidir.
- 🔴 **PIERDE** (CPA > breakeven con gasto suficiente, o sin compras tras 1–2× CPA objetivo): **pausar**.

## 4. Diagnóstico del embudo (dónde se cae)
Impresiones → CTR → clics → LPV (landing page views) → ATC → IC → **compra**. Localiza el cuello:
- CTR bajo → problema de **creativo/ángulo**. LPV ≪ clics → **velocidad/landing**. ATC/IC altos pero
  compra baja → **checkout/precio/confianza** (revisar página, COD form). Costo por conversación alto
  (WhatsApp) → **oferta/calificación**.
- **Umbrales por métrica**: usa el 🚦 SEMÁFORO DE METAS de `19-golden-pro-preset.md` (Frecuencia <2,
  CTR >1%, carga >80%, Hook >25%, Hold >20%, conv compras >1–2%…) como vara de cada escalón; CPM/CPC
  contra el histórico propio, y calibrar todo con los datos reales de la cuenta cuando haya volumen.

## 5. Salida del diagnóstico
- Tabla semáforo por campaña/conjunto/creativo con su número.
- **3 listas**: QUÉ PAUSAR · QUÉ ESCALAR · QUÉ AJUSTAR (cada una con la acción exacta y el porqué).
- Cuello de botella del embudo + hipótesis de causa.
→ Pasa a `03-build-con-metricas.md` para ejecutar la reestructura.
