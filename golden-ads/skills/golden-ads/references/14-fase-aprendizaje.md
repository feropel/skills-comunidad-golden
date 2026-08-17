# Higiene de la fase de aprendizaje (el error que MÁS encarece en COD)

Caso real (GOLDEN CP8, 2026-06-25): el usuario puso una regla que **apagaba la campaña al llegar a
$35.000 de gasto**. Cada apagado/encendido **reiniciaba el aprendizaje** → el algoritmo nunca
estabilizó → costos disparados. Terminó borrando las campañas. Este error es clásico y evitable.

## Qué es la fase de aprendizaje
Al crear/editar un conjunto, Meta explora para encontrar compradores. Sale de "aprendizaje" tras
~**50 eventos de optimización (compras) en ~7 días** con **entrega continua**. Mientras aprende, el
costo es más alto y volátil. Si se **reinicia**, vuelve a pagar ese "impuesto" desde cero.

## Qué REINICIA el aprendizaje (evitar durante la fase)
- **Apagar y volver a prender** el conjunto (reglas de "apagar al gastar X" = veneno!).
- **Cambios de presupuesto > 20–30%** de golpe (subir o bajar).
- Editar **segmentación, puja, optimización/evento, creativo** del conjunto.
- Pausas frecuentes (dayparting agresivo, apagar de noche).
- Fragmentar en muchos conjuntos con poco presupuesto (nunca juntan 50 eventos).

## La alternativa correcta al "apagar por gasto"
El miedo es "que no se dispare el gasto". La solución NO es apagar, es **poner un tope**:
- **Tope de presupuesto** (daily/lifetime) en campaña (CBO) o conjunto (ABO) — Meta nunca lo pasa.
- **Spend cap de la campaña** (`campaign_spend_cap`) o de la cuenta como red de seguridad dura.
- Reglas automáticas SOLO para **avisar** (notificación), o para **pausar de forma definitiva** algo
  que ya se decidió matar — NUNCA para apagar/prender en bucle un conjunto en aprendizaje.
- Para escalar sin resetear: subir presupuesto **20–30% cada 2–3 días** (ver `03`), o duplicar a CBO.

## Detección en el diagnóstico (Modo A)
Revisa `ads_account_get_activity_logs` (categorías `status`, `budget`) y busca:
- **Patrón de encendido/apagado repetido** del mismo conjunto → bandera "reinicios de aprendizaje".
- **Saltos de presupuesto** grandes y frecuentes → misma bandera.
- Conjuntos que llevan tiempo pero siguen en learning (`update_ad_set_learning_stage_status`).
Si aparece: dilo claro — *"esto te está encareciendo; cambia la regla de apagado por un tope de
presupuesto y deja correr para que salga de aprendizaje"*.

## Regla de oro operativa
**En COD, controla el gasto con TOPES, no con apagados.** Un conjunto que promete se deja correr para
que aprenda; uno que ya perdió se **pausa una vez** (definitivo), no en bucle.
