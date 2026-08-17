# El Efecto Desglose — reglas antes de pausar conjuntos o anuncios

Aplica SIEMPRE antes de recomendar pausar un adset o un anuncio, en Modo A (Excel) o Modo B (API). Es una capa que va ENCIMA del análisis por capas / 3 Q's, no lo sustituye.

## Qué es

El **efecto desglose** es la interpretación errónea de que Meta "desperdicia" presupuesto en anuncios o ubicaciones de bajo rendimiento. En realidad el sistema de entrega usa machine learning para maximizar resultados **totales**, no individuales.

Meta prueba todos los anuncios/ubicaciones activos en paralelo (fase de aprendizaje). Aunque al inicio una ubicación tenga menor CPA, si el sistema proyecta que sus costos subirán más rápido que los de otra, redirige el presupuesto hacia la de menor CPA proyectado a lo largo de toda la campaña. Por eso el anuncio con más gasto puede parecer "más caro" en CPA puntual: el sistema ya agotó las oportunidades baratas de la otra opción.

**Regla de oro:** si apagas el anuncio que "parece malo", el conjunto pierde la cobertura de audiencia que servía, el algoritmo se resetea y el conjunto entero puede caer.

## En qué nivel evaluar según la configuración

| Configuración | Nivel correcto de evaluación |
|---------------|------------------------------|
| Presupuesto Advantage+ de campaña (CBO) | 🔴 Evalúa SOLO a nivel campaña — no decidas por adset |
| Presupuesto por adset + Ubicaciones Advantage+ | 🟡 Evalúa a nivel conjunto — no decidas por ubicación |
| Varios anuncios en un conjunto | 🟡 Evalúa a nivel conjunto — no decidas por anuncio aislado |

Pregunta siempre: **"Tu campaña usa Presupuesto Advantage+ (CBO) o presupuesto por conjunto?"** antes de analizar a nivel adset o anuncio.

## Antes de pausar un ADSET, verifica

- Presupuesto CBO? → Meta ya optimiza. No pauses sin mínimo 7 días de datos sólidos.
- En fase de aprendizaje? → Nunca pauses durante aprendizaje (reinicia todo).
- Qué % del gasto total representa? → Si es <10%, Meta ya lo deprioriza; pausar no cambia mucho.

## Antes de pausar un ANUNCIO

| Situación | Recomendación |
|-----------|---------------|
| <7 días activo | ⏳ Esperar — datos insuficientes |
| Único anuncio activo del adset | 🚫 No pausar — el adset se queda sin entrega |
| Bajo gasto y el adset funciona bien | ✅ Puede pausarse — Meta ya lo ignora |
| Alto gasto pero CPR peor que otros | ⚠️ Posible efecto desglose — evalúa el adset completo antes |
| Alto gasto Y el adset completo está mal | 🔴 Candidato a pausar — revisa si hay fase de aprendizaje |

**Nunca pauses varios anuncios a la vez** — un cambio a la vez para no resetear el aprendizaje del adset.

## Nota sobre métricas creativas a nivel adset

`% Reproducciones 3s` y `Tiempo promedio de reproducción` a nivel conjunto son un **promedio ponderado** de todos los anuncios del adset: ocultan qué creativo engancha. Para decisiones creativas (cambiar gancho, acortar video) revísalas al nivel del **anuncio individual** — ahí sí son la performance real del creativo. A nivel adset úsalas solo como señal agregada.
