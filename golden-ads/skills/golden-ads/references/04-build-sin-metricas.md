# Modo B — Producto a TESTEAR (sin métricas)

No hay historial. El objetivo es una **estructura de testeo** que encuentre el ganador (ángulo +
creativo + público) lo más rápido y barato posible, y genere los datos que el Modo A luego optimiza.

## 1. Insumos (de la investigación)
Toma de `golden-investigacion-mercado` (o investiga lo mínimo): **3–5 ángulos**, buyer persona,
objeciones, oferta/ancla, y los **anuncios activos del nicho** (`ads_library_search` / Ad Library)
para ver qué ya funciona y diferenciarte.

## 2. Estructura de testeo recomendada (COD / e-commerce)
- **1 campaña** · Objetivo **Ventas** (`OUTCOME_SALES`) optimizando a Compra (o **Interacción→WhatsApp**
  si la venta es conversacional).
- **Presupuesto ABO** (parejo por conjunto) para testear limpio — no CBO al inicio.
- **N conjuntos = N ángulos** (3–5). Público **amplio** (Advantage+ Audience, solo país + edad/sexo de
  la persona). Mismas edades/sexos/ubicaciones en todos para aislar la variable "ángulo".
- **2–3 creativos por conjunto** (mismo ángulo, distinto hook/formato). Video preferido.
- Presupuesto de prueba por conjunto ≈ 2–3× el CPA objetivo/día (piso para salir de learning;
  respeta `min_daily_budget_cents` de la cuenta).

## 3. Criterios de decisión — DEFINIR ANTES de lanzar (no decidir con el corazón)
- **Matar** un conjunto/creativo: gastó ≥ 1.5–2× CPA objetivo sin compra (o CTR < 1% y CPC alto en
  fase de tráfico). 
- **Ganador**: CPA ≤ breakeven con ≥ 2–3 compras, o señales tempranas fuertes (CTR alto + LPV baratos
  + ATC). → pasa a Modo A (escalar).
- Ventana de evaluación: 2–4 días por conjunto antes de juzgar (dar salir de learning).

## 4. Lo que se necesita listo antes de lanzar
- **Pixel + CAPI** instalados y evento de Compra probado (sin señal, el test no aprende).
- **Página** lista (Fase 3 de golden-investigacion / golden-shopify).
- **Creativos + copys**: por ángulo, 5 hooks/5 títulos/5 descripciones (`golden-copywriting`) y los
  videos/imágenes (golden-ugc-avatar + MCP), o sus prompts si no hay saldo.

## 5. Entregable
`ADS-TEST-PLAN.md`: estructura (campaña/conjuntos/creativos), segmentación exacta, presupuestos,
criterios de matar/escalar, y checklist de pre-lanzamiento. Si se aprueba → `05-publicar-mcp.md`.
