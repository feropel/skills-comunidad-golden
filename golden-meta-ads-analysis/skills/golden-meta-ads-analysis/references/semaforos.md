# Semáforos y KPIs

## Sistema de semáforos (5 niveles)

Para cada elemento (campaña, adset, creativo, segmento demográfico) hay que asignar un veredicto. El sistema estándar es:

| Símbolo | Veredicto | CPA vs breakeven | Acción |
|---|---|---|---|
| 🟢 | EXCELENTE | ≤ CPA con margen 20%+ | Escalar agresivamente (+20% cada 48h) |
| 🟢 | BUENO | ≤ CPA con margen 10% | Escalar (+10-20%/48h) |
| 🟡 | ACEPTABLE | ≤ CPA con margen 5% | Mantener, optimizar creativo o segmentación |
| 🟡 | MARGINAL | ≤ CPA breakeven | Revisar tendencia. Si va peor, pausar. |
| 🔴 | PIERDE | > CPA breakeven, ≤ 1.5x | Pausar y rediseñar |
| ⚫ | DESCARTAR | > 1.5x CPA breakeven | Apagar, no rescatar |

## Umbrales por KPI

### CPA (Costo por adquisición)
- Verde: ≤ CPA con margen 10%
- Amarillo: entre CPA margen 10% y CPA breakeven
- Rojo: > CPA breakeven

### ROAS (Return on Ad Spend)
- Calculado como: `ingresos_meta / gasto_pauta` o `(compras × ticket) / gasto`
- Verde: ≥ ROAS para margen 10%
- Amarillo: ROAS breakeven a margen 10%
- Rojo: < ROAS breakeven

### CTR único (porcentaje de clics en el enlace)
Es un indicador de calidad del creativo. Independiente del breakeven.

| Producto típico | Verde | Amarillo | Rojo |
|---|---|---|---|
| Belleza / Cosméticos | ≥1.5% | 1.0-1.49% | <1.0% |
| Salud / Suplementos | ≥1.1% | 0.8-1.09% | <0.8% |
| E-commerce general | ≥1.2% | 0.8-1.19% | <0.8% |

### CPC (Costo por clic)
- Verde: ≤ $700 COP
- Amarillo: $700-$950
- Rojo: > $950

### CPM (Costo por mil impresiones)
- Verde: ≤ $10,000 COP
- Amarillo: $10,000-$15,000
- Rojo: > $15,000

CPM alto puede indicar mala calidad creativa, audiencia muy competida, o cuenta nueva sin trust.

### Hold rate al 50% (% de visualizaciones que pasan del 50%)
- Calculado como: `views_50pct / views_3s × 100`
- Verde: ≥30%
- Amarillo: 20-29%
- Rojo: <20%

### View through al 100% (% que completa el video)
- Verde: ≥12%
- Amarillo: 7-11%
- Rojo: <7%

### Frecuencia
- Verde: ≤2.5
- Amarillo: 2.6-3.5
- Rojo: >3.5 (audiencia saturada, refresh inminente)

En Advantage+ tolera frecuencia más alta (hasta 4-5).

### Tasa de conversión visita LP → compra
- Verde: ≥3%
- Amarillo: 1.5-2.9%
- Rojo: <1.5%

### Tasa de conversión pago iniciado → compra
- Verde: ≥25%
- Amarillo: 15-24%
- Rojo: <15%

## Reglas de decisión rápida

### Por CPA
- **CPA verde**: escalar 20% cada 48h
- **CPA amarillo + CTR verde**: el creativo funciona, problema en landing/checkout
- **CPA amarillo + CTR amarillo**: optimizar audiencia o creativo
- **CPA rojo + CTR rojo**: creativo no engancha, cambiar ángulo
- **CPA rojo + CTR verde**: hay clics pero no convierte, problema de landing o producto-mercado

### Por etapa del embudo
- **Clic → Visita baja**: problema técnico (carga lenta, mobile mal optimizado)
- **Visita → Pago iniciado baja**: producto no resuena, precio rechazado, formulario malo
- **Pago iniciado → Compra baja**: checkout complejo, falta de métodos de pago, problema técnico

### Por frecuencia
- **Frec > 3.5 y CPA estable**: audiencia satura pero aún rinde. Aguantar 3-5 días más.
- **Frec > 3.5 y CPA subiendo**: launchar adset paralelo con nuevos creativos. Audiencia agotada.
- **Frec < 2 y entrega alta**: público amplio, todo bien

## Cuándo apagar vs cuándo mantener

### Apagar inmediatamente (no esperar)
- CPA > 2x breakeven después de $300K-$500K gastados
- CTR < 0.5% después de $200K gastados (creativo está roto)
- 0 compras después de $400K gastados (problema serio: audiencia, creativo o pixel)
- Rechazo del anuncio sin posibilidad de apelar

### Mantener 24-48h más
- CPA marginal (1.0-1.3x breakeven) con tendencia mejorando
- CTR amarillo con conversiones (puede ser problema de audiencia, no creativo)
- Performance variable día a día (necesita más data)

### Escalar 20% cada 48-72h
- CPA verde estable por 3+ días
- Frecuencia bajo 3.0
- ROAS verde estable
- Si después de subir 20% el CPA aguanta, repetir

### Bajar presupuesto 30%
- CPA pasa de verde a amarillo de un día a otro
- Frecuencia llega a 3.5+
- Audiencia se está saturando

## Cuándo lanzar un creativo nuevo

- Cuando los videos actuales tienen frecuencia >3.5 acumulada
- Cuando el CTR de los videos actuales baja >25% en una semana
- Cuando el CPA empieza a subir consistentemente
- Cuando se quiere probar un nuevo ángulo del mismo concepto ganador

Nunca lanzar 5 creativos nuevos a la vez. Lanzar 1-2 por semana en rotación con los ganadores.

## Cuándo refrescar audiencia

- Frecuencia consistentemente >4
- CPM subiendo >20% en 7 días sin cambio de creativo
- Caída de CTR sin explicación creativa

Refrescar = duplicar el adset con un nombre nuevo. Meta lo trata como nuevo learning aunque la audiencia sea idéntica.

## Benchmarks del embudo de conversión

Tasas de referencia validadas en e-commerce Colombia (Meta Ads):

| Etapa del embudo | Verde | Amarillo | Rojo |
|---|---|---|---|
| Clic en enlace → Visita LP | ≥70% | 50-69% | <50% |
| Visita LP → Pago iniciado | ≥15% | 8-14% | <8% |
| Pago iniciado → Compra | ≥20% | 12-19% | <12% |
| Visita LP → Compra (directo) | ≥3% | 1.5-2.9% | <1.5% |
| Velocidad de carga LP | ≤1.0s | 1.0-2.0s | >2.0s |

### Diagnóstico por etapa del embudo

Cuando un creativo tiene CPA rojo pero CTR verde, el problema NO está en el anuncio sino en una etapa posterior. Usa estas reglas:

**Clic → Visita baja (<50%):**
- La landing carga lento o tiene redirect problemático
- La URL del anuncio es incorrecta o tiene error 404
- Mobile no optimizado (la mayoría del tráfico es mobile en Colombia)

**Visita → Pago iniciado baja (<8%):**
- El precio asusta al usuario (no coincide con lo que esperaba del anuncio)
- La landing no tiene coherencia con el creativo (promete una cosa, muestra otra)
- Formulario muy largo o confuso
- Falta de prueba social (testimonios, reviews)
- No hay oferta clara o urgencia

**Pago → Compra baja (<12%):**
- Checkout complejo o lento
- Pocos métodos de pago disponibles
- Costos extra inesperados (flete alto al final)
- Falta de confianza (no tiene sello de seguridad, no tiene SSL visible)
- Error técnico en el checkout

**Tasa de conversión alta pero CPA alto:**
- El CPM está inflado (audiencia competida o cuenta penalizada)
- La frecuencia es alta (audiencia saturada)
- El creativo tiene CTR bajo (no genera clic)
