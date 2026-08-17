# Playbook de Replicación en otros BMs y cuentas

## Tres escenarios de replicación

### Escenario 1: Replicar en OTRA CUENTA del MISMO Business Manager

Es el caso más fácil. Comparten BM Verification, dominio probablemente compartido, y mismo ecosistema de pixel.

**Setup técnico (1-2 horas):**
1. Crear cuenta publicitaria nueva dentro del mismo BM
2. Compartir dominio verificado existente (si la tienda destino está bajo el mismo dominio)
3. Crear pixel nuevo o usar el existente (depende si quieres atribución separada)
4. Configurar eventos CAPI: los mismos eventos del original (Compra arriba)
5. Si es Shopify, agregar la cuenta de Meta en la app Facebook & Instagram

**Migración de assets (30 min):**
- Descargar los 3-5 videos ganadores como `.mp4` desde la biblioteca de la cuenta original
- Re-subirlos a la nueva cuenta (Meta los procesa como nuevos creativos, no comparte ID)
- Copiar el copy/texto exacto de los anuncios ganadores

**Lanzamiento (Día 1):**
- Replicar la estructura ganadora identificada en el análisis
- Presupuesto inicial: 50-70% del presupuesto diario actual de la cuenta origen
- Mismo target demográfico, mismas ubicaciones
- Lanzar 3 adsets idénticos al ganador (con los 3 mejores creativos)

**Calentamiento:**
- Día 1-3: dejar correr, no tocar
- Día 4-7: si CPA está bajo el breakeven, escalar 20% cada 48-72h
- Día 7-14: si CPA está estable, agregar adset de retargeting

**Errores comunes a evitar:**
- No replicar todos los adsets de una vez. Empezar con los 2-3 ganadores y agregar resto después.
- No copiar adsets perdedores. El análisis ya dijo cuáles pausar.
- No esperar mismo CPA exacto en día 1. Las cuentas nuevas tienen 7-14 días de aprendizaje.

### Escenario 2: Replicar en cuenta de OTRO Business Manager (BM nuevo)

Más complejo porque se crea ecosistema desde cero. Más riesgo de bloqueos, rechazos y mala entrega inicial.

**Setup técnico (1-2 días):**
1. Crear BM nuevo con cuenta personal limpia (sin historial de bloqueos)
2. Verificar el BM con documentos
3. Crear cuenta publicitaria
4. Verificar dominio (importante para iOS 14.5+ y Aggregated Event Measurement)
5. Instalar pixel en la tienda (Shopify, WooCommerce, plataforma propia)
6. Configurar CAPI (Conversions API) — crítico para atribución
7. Priorizar 8 eventos en Aggregated Event Measurement (Compra en posición 1)
8. Vincular página de Facebook al BM (debe ser página con historial limpio)

**Calentamiento de la cuenta (5-7 días antes de pautar fuerte):**
- Día 1-2: campaña pequeña de engagement o tráfico al sitio ($30,000-$50,000 COP/día)
- Día 3-5: aumentar a $80,000-$120,000/día con la campaña real (1 adset, 2 creativos)
- Día 6-7: comenzar a evaluar entrega y CPM
- A partir del día 8: escalar gradualmente

**Si la entrega es baja en los primeros días:**
- Verificar que el pixel y CAPI estén disparando bien
- Probar diferentes audiencias
- Aumentar CPM bid (en pujas con tope) temporalmente
- No tocar campañas más de 1 vez al día

**Materiales a transferir:**
- Los 3-5 videos ganadores en `.mp4` (descargar desde la biblioteca de Meta)
- Los textos exactos de los anuncios ganadores
- Los thumbnails de los videos (puede subirlos como imagen secundaria)
- Documentación de la audiencia ganadora (edad, sexo, ubicaciones)

**Errores comunes a evitar:**
- No usar tarjeta de pago compartida con cuentas previas bloqueadas
- No copiar copies con claims agresivos o palabras prohibidas (Meta es estricto con cuentas nuevas)
- No subir el video y lanzar el mismo día: dejar pasar 24h para que Meta lo procese
- No correr 5 adsets en el día 1. Empezar con 1-2, luego expandir.

### Escenario 3: Replicar a OTRO PRODUCTO similar dentro del ecosistema

Caso de un producto de una categoría → producto similar de la misma categoría, o una línea de producto → otra línea.

**Lo que SÍ se puede reutilizar:**
- La metodología de análisis (este skill)
- La estructura ganadora de campañas (ABO vs CBO vs ASC)
- Los aprendizajes sobre ubicaciones y plataformas ganadoras/perdedoras
- El sentido demográfico (si el producto original fue 82% hombres 25-54, otro producto de la misma categoría probablemente también — pero validar con datos del nuevo archivo)

**Lo que NO se puede reutilizar:**
- Los creativos exactos (cada producto necesita sus propios videos)
- Los copies (cada producto tiene su propuesta de valor)
- Las landings (cada producto tiene su URL)
- El pixel y eventos (cada producto debería tener su propio pixel)

**Proceso recomendado:**
1. Producir 3-5 videos siguiendo los ángulos ganadores del producto original (problema-solución, transformación, UGC, demostración)
2. Replicar la estructura de campañas con valor del producto nuevo
3. Empezar más conservador en presupuesto (las primeras semanas son aprendizaje)
4. Comparar performance con el producto original en CPA y ROAS — si está dentro del 30%, vas bien

## Checklist de pre-lanzamiento en cuenta nueva

Antes de lanzar la primera campaña, verificar:

- [ ] BM verificado con documentos
- [ ] Cuenta publicitaria activa, sin restricciones
- [ ] Dominio verificado en BM
- [ ] Pixel instalado y disparando (verificar en Test Events)
- [ ] CAPI configurada y disparando eventos (verificar en Event Manager → Test events)
- [ ] 8 eventos priorizados en Aggregated Event Measurement
- [ ] Compra como evento #1 prioritario
- [ ] Página de Facebook vinculada al BM
- [ ] Instagram conectado a la página (si vas a usar IG placements)
- [ ] Tarjeta de pago activa en la cuenta
- [ ] Política de privacidad actualizada en el sitio web
- [ ] URL de la landing valida con HTTPS

## Métricas de "todo va bien" en cuenta nueva

| Día | Métrica a vigilar | Verde | Amarillo | Rojo |
|---|---|---|---|---|
| Día 1-2 | Entrega (impresiones) | Sube establemente | Constante | Baja o nula |
| Día 3-5 | CPM | $5K-$15K | $15K-$25K | >$25K |
| Día 5-7 | CTR | ≥1.0% | 0.5-0.9% | <0.5% |
| Día 7-10 | CPA | ≤ breakeven | 1.0-1.3x breakeven | >1.5x breakeven |
| Día 10-14 | ROAS | ≥ ROAS_breakeven | 80-99% del objetivo | <80% del objetivo |

Si día 10 todavía estás en rojo: revisar pixel, CAPI, calidad creativa, landing.

## Quick reference: tiempo total de replicación

| Tipo replicación | Setup técnico | Calentamiento | Tiempo hasta CPA estable |
|---|---|---|---|
| Otra cuenta mismo BM | 1-2 horas | 0 días (cuenta hereda BM verification) | 5-10 días |
| Otro BM (cuenta de cero) | 1-2 días | 5-7 días | 14-21 días |
| Otro producto similar | 1-2 días (BM existente) | 0 | 7-14 días |

## Riesgos típicos en replicación

**Bloqueo de cuenta nueva (común en BMs nuevos)**
- Causa: pago con tarjeta de cuenta bloqueada previa, claims agresivos en copy, página con historial
- Solución: aplicar revisión, contactar soporte de Meta, esperar 48-72h
- Prevención: usar tarjeta limpia, copies suaves al inicio, página limpia

**Rechazo de anuncios por política**
- Causa: claims médicos, antes/después no permitidos, lenguaje que sugiera atributos personales
- Solución: editar copy, volver a enviar a revisión
- Prevención: leer las políticas de anuncios de Meta antes de lanzar

**Baja entrega los primeros 3-5 días**
- Es normal en cuentas nuevas
- No tocar campañas, dejar que el algoritmo aprenda
- Si pasa día 7 sin entrega, verificar pixel/CAPI

**CPA inicial 2-3x el esperado**
- Es normal en aprendizaje
- Mantener presupuesto, no apagar prematuramente
- Suele estabilizar entre día 7-14

**CPM mucho más alto que cuenta origen**
- Indicador de que la cuenta aún no es trusted
- Calentar con campañas de engagement primero ayuda

## Cálculo de presupuesto inicial para cuenta nueva

El presupuesto diario mínimo para que el adset acumule data suficiente depende del CPA esperado:

```
presupuesto_minimo_diario = CPA_breakeven × 3

Ejemplo: si CPA breakeven es $24,000
→ presupuesto mínimo = $72,000/día por adset
→ Así consigues ~3 compras/día para leer data

Para lectura estadística confiable (5+ compras/día):
presupuesto_optimo_diario = CPA_breakeven × 5
```

### Distribución sugerida del presupuesto total

| Tipo de adset | % del budget total | Función |
|---|---|---|
| Adset frío principal (top creativo + audiencia validada) | 40-50% | Motor de ventas |
| Adset frío secundario (2do/3er creativo) | 15-20% | Diversificación |
| Retargeting web caliente (carrito/checkout 30d) | 15-20% | Cierre de ventas |
| Retargeting tibio (visitantes/engagers 30d) | 10-15% | Alimentación de funnel |
| Experimental (nuevos ángulos, landings, audiencias) | 5-10% | Descubrimiento |

### Escalado seguro (regla 20/48)

- Subir presupuesto máximo 20% cada 48-72 horas
- Si después de subir el CPA se mantiene estable 48h, subir de nuevo
- Si el CPA sube >20% después de escalar, volver al presupuesto anterior y esperar 72h
- Nunca duplicar presupuesto de un día para otro (reset de aprendizaje)

### Cuándo reducir presupuesto

- CPA lleva 3+ días consecutivos en amarillo/rojo
- Frecuencia >4 sin señal de estabilización
- CPM sube >30% en 7 días (señal de penalización o audiencia agotada)
- Después de bajar, esperar mínimo 72h antes de volver a escalar
