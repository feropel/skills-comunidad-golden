# EJEMPLO — DIAGNOSTICO.md (modelo de entrega, Modo A)

> Ejemplo real anonimizado (cuenta COD Colombia, COP, últimos 30 días). Es el ESTÁNDAR de cómo debe
> verse una entrega: economics arriba, semáforo contra breakeven, 3 listas accionables, banderas.
> Reemplaza los datos por los de la cuenta analizada.

## 0. Cuenta y fuente
- Cuenta: `CUENTA X` (id 000…) · **Moneda: COP** · ACTIVE · MCP en vivo (solo-lectura).
- Rango: últimos 30 días. Fuente: `ads_get_ad_entities` (nivel campaña) + `ads_get_opportunity_score`.

## 1. Unit economics (REGLA 2) — [rellenar con datos reales del dueño]
PRECIO `[__]` · COSTO `[__]` · ENVIO `[__]` · ENTREGA `[__]%` → **Breakeven CPA Meta = `[__]`** ·
Breakeven ROAS Meta ≈ `[__]`. *(Sin estos datos, el veredicto es RELATIVO, no absoluto.)*
> Recordatorio COD: **ROAS pagado ≈ ROAS Meta × entrega**. Ej. ROAS Meta 3,0 × 65% ≈ **1,95 real**.

## 2. Panorama
Gasto ~$22,5M COP · ~830 compras · CPA mezclado ~$27.000 · producto estrella = PRODUCTO A (90% del gasto).
Frecuencia 1,0–1,4 (sin fatiga → hay techo para escalar). Opportunity Score Meta: 100/100 (sin recs).

## 3. Semáforo por campaña (contra breakeven; aquí relativo por falta de economics)
| Campaña | Gasto | Compras | CPA | ROAS Meta | ROAS pagado* | Acción |
|---|--:|--:|--:|--:|--:|:--:|
| A · OPEN 2 | 1.258.644 | 60 | 20.977 | 3,77 | ~2,45 | 🟢 escalar |
| A · OPEN 6 | 3.177.732 | 141 | 22.537 | 3,39 | ~2,20 | 🟢 escalar |
| A · OPEN 5 | 5.575.906 | 232 | 24.034 | 3,24 | ~2,11 | 🟢 escalar |
| A · OPEN 4 | 3.817.405 | 153 | 24.950 | 3,06 | ~1,99 | 🟡 vigilar |
| A · OPEN 9 | 1.398.538 | 39 | 35.860 | 2,35 | ~1,53 | 🟡/🔴 |
| A · OPEN 6 (dup) | 1.252.360 | 29 | 43.185 | 1,91 | ~1,24 | 🔴 pausar |
| B (secundario) | 1.889.794 | 47 | ~40.208 | ~2,0 | ~1,3 | 🔴 podar |
| C · OPEN 1 | 41.130 | 0 | — | — | — | 🔴 creativo muerto (CTR 0,71%) |
*ROAS pagado = estimado con entrega 65% supuesta (marcar y confirmar).

## 4. Veredicto — 3 listas
- **ESCALAR**: OPEN 2, OPEN 6, OPEN 5 (mejor ROAS + volumen + frecuencia baja). Subir 20–30% cada 2–3 días.
- **PAUSAR**: OPEN 6 duplicado (1,91 vs 3,39 del original), OPEN X, línea B floja, C sin compras.
- **AJUSTAR**: OPEN 4/9 (probar nuevos hooks del ganador antes de decidir); consolidar duplicados.

## 5. Banderas y oportunidades
- **Nombres duplicados**: tres campañas "OPEN 6" → renombrar; el duplicado sangra presupuesto.
- **Sin retargeting**: todo es prospecting "OPEN" → montar embudo `06` (MOF/BOF + carrito/DPA) = CPA barato sin explotar.
- **Pendiente bloqueante**: precio/costo/entrega de PRODUCTO A para el veredicto de rentabilidad absoluto.

## 6. Próximos pasos
1. Confirmar economics → recalcular semáforo absoluto. 2. Pausar los 🔴. 3. Escalar los 🟢.
4. Montar retargeting. 5. Refrescar creativos de los 🟡 (matriz `08`).
