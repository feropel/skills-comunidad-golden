# Registro de resultados (results ledger)

El skill APRENDE de campo con esto. Cada vez que entregas un prompt, agrega una fila. Cuando el usuario vuelva con números, actualiza la fila y usa lo aprendido para la siguiente versión. Copia este archivo por negocio si quieres (ej. `resultados-freshklin.md`).

## Cómo se usa
1. Al entregar un build → crea la fila con versión, fecha, hipótesis y "pendiente de datos".
2. Cuando el usuario reporte resultados → llena las métricas y marca qué ganó.
3. Antes de construir v+1 → LEE este ledger, mira qué versión convirtió mejor y por qué, y parte de ahí (no de cero).

## Métricas clave (el usuario las saca de Chatea PRO / CRM / Dropi)
- **% a captura** = conversaciones que llegan al PASO 5 (dan datos) ÷ conversaciones iniciadas.
- **% cierre** = pedidos confirmados con SÍ ÷ conversaciones que llegaron a captura.
- **% anticipado OK** = anticipados con comprobante válido ÷ anticipados intentados.
- **Efectividad** = entregados y pagados ÷ pedidos confirmados (mide calidad del filtro logístico).

## Tabla
| Producto | Versión | Fecha | Hipótesis (qué apostó) | % a captura | % cierre | % anticipado OK | Efectividad | Variable A/B testeada | Ganó? | Aprendizaje |
|---|---|---|---|---|---|---|---|---|---|---|
| _ej: FreshKlin_ | v1 | 2026-06-23 | base | — | — | — | — | — | — | pendiente de datos |
| _ej: FreshKlin_ | v2 | 2026-07-01 | precio más temprano + garantía reforzada | 62% | 34% | 88% | 71% | precio en msg 2 vs msg 4 | SÍ (msg 2) | dar precio antes sube cierre ~6pts |
| producto capilar (CO) | v3 | 2026-07-12 | prioridad de intención de compra + memoria del pedido + URLs blindadas + única confirmación | — | — | — | — | — | — | Test de campo con cliente simulado: los 5 asesinos de venta fueron (1) re-preguntar datos ya dados, (2) re-preguntar tras "quiero comprar", (3) URL equivocada tomada del historial, (4) resumen con campos (Pendiente)/inventados, (5) confirmaciones múltiples. Todos entraron como reglas fijas a plantilla-prompt.md. División de mensajes de la plataforma: límite 2, no 3 (con 3 la IA hace ráfagas robot). |

## Regla de oro del ledger
Una sola variable por versión. Si cambias 3 cosas y sube el cierre, no sabes cuál sirvió. El ledger solo vale si el A/B es limpio.
