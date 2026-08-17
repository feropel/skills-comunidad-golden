# Benchmarks / KPIs por etapa + reglas de decisión

⚠️ Son **rangos de referencia LatAm COD** para orientar, NO verdades absolutas. El único umbral que
manda es tu **breakeven** (REGLA 2). Úsalos para ubicar dónde está el cuello, no para decidir solo.

## Tabla orientativa (feed Meta, COD LatAm)
| Métrica | 🟢 Sano | 🟡 Vigilar | 🔴 Malo | Lee… |
|---|---|---|---|---|
| **CTR (link)** | >1.5% | 0.8–1.5% | <0.8% | gancho/creativo/ángulo |
| **CPM** | bajo-medio del nicho | medio-alto | muy alto | saturación/segmentación/calidad |
| **Conexión landing** (clics→LPV) | >80% | 60–80% | <60% | velocidad/landing/coherencia |
| **CVR** (LPV→compra) | >2% | 1–2% | <1% | oferta/precio/confianza/checkout |
| **Frecuencia** (7d) | <2 | 2–3 | >3 | fatiga → refrescar creativo |
| **CPA** | < breakeven | ≈ breakeven | > breakeven | veredicto de rentabilidad |
| **ROAS** | > breakeven ROAS | ≈ | < | ídem (ajustar por entrega COD) |

## MATRIZ DE VEREDICTO DEL TESTEO (la regla principal)

Un conjunto no se juzga por UNA métrica: se juzga por su **huella completa**, y cada escenario
tiene su **propia ventana**. Matar rápido lo muerto, esperar solo lo ambiguo, escalar rápido lo
ganador. Una ventana única para todo comete dos errores caros a la vez: deja respirando tests
muertos y ejecuta ganadores que iban a resolver al día 2.

**Los eventos disponibles cambian según el modelo de pago. Confírmalo antes de leer la huella:**

| | Embudo de eventos | `InitiateCheckout` |
|---|---|---|
| **COD (Releasit)** | LPV → ATC / apertura del formulario → Compra al enviar | **no existe**, no lo busques ni lo uses de corte |
| **Pago anticipado (Shopify)** | LPV → ATC → **InitiateCheckout** → AddPaymentInfo → Compra | **sí existe, y es la mejor señal temprana**: separa al que solo miró del que llegó a pagar |

En pago anticipado, un conjunto con muchos `InitiateCheckout` y pocas compras **no es un creativo
malo, es un checkout que se cae** (precio con el envío sorpresa, pasarela lenta, pedir cuenta
obligatoria). Ahí se arregla la tienda, no el anuncio. En COD ese diagnóstico se hace con el ATC,
porque el ATC es la apertura del formulario.

| Escenario | Huella (todas a la vez) | Ventana | Acción |
|---|---|---|---|
| **1 · MUERTO** | gastó ≥60% del presupuesto del día · **0 compras** · <3 ATC · CTR <0,9% | **el mismo día** | APAGAR hoy. No esperes 48 h: eso es presupuesto quemado por regla |
| **2 · SEÑAL SIN VENTA** | gastó 100% del día · 0 compras **PERO ≥5 ATC** · **CTR ≥1,3%** | 48 h | **NO TOCAR.** El día 2 resuelve muchas veces solo. Matarlo aquí es matar un ganador |
| **3 · SEMI-GANADOR** | 2–5 compras · ≥10 ATC · CPA ≈ breakeven | 48 h | apagar los conjuntos caros, **aislar los 2 hooks que vendieron**, 4 variaciones, relanzar en conjunto DUPLICADO |
| **4 · GANADOR** | >5 compras · ≥10 ATC · CPA muy por debajo del breakeven | **día 1** | escalar ya: +20–30% o duplicar a CBO. No esperes las 48 h |

**El CPA que se compara es SIEMPRE el Breakeven CPA por compra en Meta** — margen cobrado ×
% de entrega — nunca el margen bruto. Ver `12-unit-economics.md`. **Este es el punto donde
cualquier método de mercado prepago miente en COD:** su breakeven asume cobrar el 100%. Con 65%
de entrega, un breakeven "de papel" de $41.800 es en realidad ~$27.200. Aplicar el de papel te
hace escalar campañas que están perdiendo plata **y el tablero no lo muestra hasta 3 semanas
después**, cuando llega el dato de entrega real.

### Reglas de decisión (fallback y complementos)
- **MATAR (sin volumen para leer la huella):** gastó **≥1.5–2× el CPA objetivo sin compra**, o
  CPA > breakeven sostenido, o CTR <0.8% + CPC alto en fase de tráfico.
- **ESCALAR**: CPA ≤ breakeven con ≥2–3 compras y estable → subir presupuesto **20–30% cada 2–3 días**
  (no más, para no reiniciar learning) o duplicar a CBO/Advantage+ Shopping.
- **OPTIMIZAR (🟡)**: antes de matar, prueba nuevo hook/creativo, ajusta segmentación o evento/puja.
- **Ventana mínima de juicio** cuando no aplique la matriz: 2–4 días o ~50 eventos de
  optimización/semana (salir de learning).
- **Mentalidad del testeo:** no estás buscando ganar plata todavía, estás comprando información.
  Pero en COD la información tarda: la venta se confirma al despachar, la plata al entregar.

## Patrón de EDAD en COD LatAm (cuidado personal) — punto de arranque
Validado en Le'côterra en **3 cuentas**. Sirve como hipótesis de arranque; calibra con los pedidos reales:
| Rango | Desempeño típico | Acción |
|---|---|---|
| **18–24** | el más flojo (peor ROAS/CPA) | **cortar** |
| **25–44** | el **núcleo** (mejor CPA + ROAS + volumen) | base de la campaña |
| **45–54** | aceptable | mantener/vigilar |
| **55+** | buen ROAS pero **poco volumen** | dejar correr, no escalar solo |
> Arranca los conjuntos en **25–44** y expande a 45–54 según data. No malgastes en 18–24 salvo que los
> pedidos reales demuestren lo contrario. (Ajusta si el producto es de nicho joven.)

## Diagnóstico del cuello (dónde se cae el embudo)
CTR bajo → creativo/ángulo. LPV≪clics → velocidad/landing. CVR bajo con ATC alto → checkout/precio/
confianza. Costo por conversación alto (WhatsApp) → oferta/calificación del bot.

> En COD, ajusta CPA/ROAS por **tasa de entrega efectiva** (no todo lo vendido se cobra).
