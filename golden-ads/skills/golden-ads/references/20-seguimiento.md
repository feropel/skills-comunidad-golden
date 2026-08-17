# Seguimiento post-lanzamiento (ya se activó — qué mirar, cuándo tocar y cuándo NO)

La campaña se activó. El error #1 ahora es tocarla demasiado pronto (cada edición reinicia el
aprendizaje, `14`); el #2 es no mirarla y dejar que sangre. Este es el ritmo correcto para COD.
Se lee SIEMPRE con el preset GOLDEN PRO y su 🚦 semáforo de metas (`19`), y con la regla de
significancia (REGLA 12): antes del umbral de volumen todo es señal temprana, no veredicto.

## Ritmo de revisión (calendario operativo)

**Día 0 (activación + 2–4 h)** — checklist técnico, NO de rendimiento:
- Entrega = "Activa" en los 3 niveles (campaña/conjunto/anuncio). Sin rechazos de anuncios.
- El pixel registra eventos (Compras/Conversaciones empiezan a aparecer). Gasto corriendo.
- 🔴 ÚNICO motivo para intervenir hoy: anuncio rechazado, error de URL/destino, o gasto en 0.

**Día 1** — solo señales rápidas (estabilizan antes que el CPA):
- CTR (>1% bien), CPC vs histórico, Hook Rate (>25%) y Hold Rate si es video, CPM vs histórico.
- 🔴 Matar YA solo si: CTR <0.5% con ≥1.000 impresiones Y hook <15% (creativo muerto), o gasto
  ≥1× breakeven con CERO señal en todo el embudo (ni clics ni carritos). Lo demás: NO tocar.

**Día 2–3** — primer corte de embudo (GOLDEN PRO de arriba a abajo):
- Dónde se cae? (clics OK pero sin LPV = landing; carritos sin compra = checkout; conversaciones
  sin venta = cierre/bot). Arregla el ESLABÓN (landing, oferta, bot), no la campaña.
- Compara conjuntos entre sí (ranking relativo). Aún NO pausar por CPA salvo caso 🔴 del día 1.

**Día 4–7 (o al salir de aprendizaje)** — primer VEREDICTO:
- Con gasto ≥ 2–3× CPA objetivo y/o ≥ 15–30 compras: aplicar semáforo contra breakeven (`12`):
  🟢 CPA < breakeven → escalar · 🟡 cerca → optimizar creativo/landing · 🔴 CPA > breakeven
  sostenido → pausar (una vez, definitivo — no en bucle).
- Revisar frecuencia (>2.5–3 = fatiga → refrescar creativo `08`) y FTIR (bajando = saturación).

**Semanal (cuenta en marcha)** — rutina fija:
- Semáforo por campaña/conjunto/creativo + 3 listas (PAUSAR/ESCALAR/AJUSTAR, formato de `02`).
- Fatiga: frecuencia, FTIR, CTR decayendo → rotar creativos ANTES de que muera el ganador.
- Activity log: cachar apagados/encendidos o reglas de umbral (fuga clásica, `14`).
- Retargeting alimentado y sin solapamiento con prospecting (`06`).

## Cómo escalar SIN romper el aprendizaje (resumen operativo de `03`+`14`)
- Vertical: subir presupuesto **20–30% cada 2–3 días** al conjunto 🟢 (nunca duplicarlo de golpe).
- Horizontal: duplicar el ganador hacia CBO o nuevo ángulo/público (LAL de compradores, `16`).
- El creativo ganador NO se edita (se duplica y se itera la copia); el original sigue corriendo.

## Por MCP (rutina de chequeo en vivo)
`ads_get_ad_entities` (campaign→adset→ad, `date_preset` last_7d) con el set recomendado de `11` +
`ads_insights_performance_trend` (tendencia) + `ads_insights_anomaly_signal` (fugas) +
`ads_account_get_activity_logs` (qué se tocó). Entregar SIEMPRE: semáforo + 3 listas + nivel de
confianza del dato (REGLA 12) + próxima fecha de revisión sugerida.

## Nunca (en seguimiento)
- Editar presupuesto/segmentación/creativo de un conjunto EN aprendizaje salvo caso 🔴.
- Pausar/prender en bucle (usa topes, `14`). Juzgar CPA con 2 ventas. Escalar >30% de un salto.
- Reportar sin decir el nivel de confianza y la acción concreta (REGLA 6).
