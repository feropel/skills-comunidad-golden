# Salud de la señal y Andromeda: lo que Meta ve, no lo que tú ves

Añadido 2026-08-26. Origen: extracción de `claude-ads` v2.4.0 (MIT, 33 MB instalados en el Mac y
**nunca corridos**), agente `audit-meta`, categorías con peso. Medido antes de escribir: de estos
umbrales, `golden-ads` tenía **cero menciones** de EMQ, deduplicación, Learning Limited, Andromeda
y la regla de presupuesto por conjunto.

**Esto NO reemplaza `07-benchmarks-kpis.md`.** Esa tabla es mejor que la de cualquier auditor
genérico porque está calibrada a COD LatAm (pide CTR >1,5% donde los genéricos piden 1,0%, y
frecuencia <2 donde aceptan <3). Aquella mide **el rendimiento**; esta mide **la calidad de la
señal que Meta recibe**, que es lo que decide si el rendimiento puede siquiera existir.

## Por qué esta capa importa más en COD que en pago anticipado

En pago anticipado el navegador confirma la compra y el evento sale limpio. En COD la venta se
confirma **por WhatsApp, horas después, fuera del navegador**. La señal llega pobre, tarde o no
llega. Si además el pixel duplica o el match es malo, Meta optimiza a ciegas y el presupuesto se
va en entregas malas. Por eso el bloque de señal pesa **30%** en la auditoría de origen.

## Los siete controles que faltaban

### 1. CAPI activo (crítico)
Sin Conversions API se pierde entre **30% y 40% de los datos** desde iOS 14.5. En COD el golpe es
peor porque la conversión real ya ocurre fuera del navegador.
**Control:** si la cuenta pauta con objetivo de compra y no tiene CAPI, eso va primero en el
informe, antes que cualquier recomendación de creativo o presupuesto.

### 2. Deduplicación de eventos ≥90%
Si el pixel y CAPI mandan el mismo evento sin `event_id` compartido, Meta lo cuenta **dos veces**.
El informe muestra el doble de compras de las reales y el CPA parece la mitad.
| Dedup | Veredicto |
|---|---|
| ≥90% | sano |
| 70-90% | vigilar |
| <70% | **falla** — los números del informe no son de fiar |

**Ojo Golden:** esto se parece a la trampa ya conocida de las **órdenes fantasma de Dropi** (al
editar una orden cambia el id y la vieja sigue contando). Misma clase de error, distinto sistema:
un identificador que cambia y hace contar dos veces lo mismo.

### 3. Event Match Quality (EMQ) ≥8.0 en Purchase
Mide cuántos datos del comprador logra casar Meta (correo, teléfono, nombre, ciudad).
| EMQ | Veredicto |
|---|---|
| ≥8.0 | sano |
| 6.0-7.9 | vigilar |
| <6.0 | **falla** |

**MEDIDO EN EL PÍXEL COLOMBIA `375426632099018` el 27-ago (7 días), y corrige lo que este archivo
suponía:** el `Purchase` de Golden tiene **EMQ 9.3** con **cobertura 100% en las 13 claves**
(email, teléfono, nombre, apellido, ciudad, estado, código postal, país, ip, user agent, fbp, fbc,
external_id). `AddPaymentInfo` va en **8.7**. Los dos por encima del umbral: **sanos**.

Yo había escrito aquí que en COD el EMQ tendría techo bajo porque el cliente casi nunca da correo
(1,7% de consentimiento). **Es falso para el Purchase**: llega con todo. El consentimiento de
*marketing* y los datos que Releasit manda al píxel son cosas distintas, y confundirlas llevaba a
no auditar un evento que está bien.

**Donde sí falla es ANTES de la compra**, y ahí la palanca es real:

| Evento | EMQ | Cobertura de email / teléfono |
|---|---|---|
| Purchase | **9.3** | 100% / 100% |
| AddPaymentInfo | **8.7** | 100% / 100% |
| AddToCart | 6.4 | 12% / 12% |
| PageView | 6.2 | 3,7% / 3,7% |
| ViewContent | 6.1 | 0,6% / 0,6% |
| Search | 4.4 | sin email ni teléfono |

Los cuatro de abajo están bajo el umbral de 8.0. Meta optimiza la fase de descubrimiento con señal
pobre aunque la compra llegue impecable. **La palanca no es el formulario: es mandar por CAPI el
identificador que ya existe** cuando el visitante vuelve, que hoy se queda en Dropi y en Chatea.

⚠️ **Dos cosas que aparecieron al medir y hay que mirar:**
1. `InitiateCheckout` **existe en este píxel** (167 eventos en 7 días) cuando `07-benchmarks-kpis.md`
   dice que en COD no existe. O hay tráfico de pago anticipado mezclado, o Releasit lo dispara.
   Hasta saber cuál, **no se usa de corte** — la regla de benchmarks sigue mandando.
2. En el conteo total, `Purchase` aparece **partido en dos entradas (63 y 60)**, igual que PageView
   (1392 y 1320) y ViewContent (1139 y 975). Puede ser dos dominios, o web y servidor ya
   deduplicados. **NO es prueba de doble conteo** y no se puede concluir con esta herramienta:
   `ads_get_dataset_quality` no devuelve tasa de deduplicación. Queda abierto.

### 4. Learning Limited: menos del 30% de los conjuntos
`14-fase-aprendizaje.md` explica qué reinicia el aprendizaje. Falta el umbral de cuántos conjuntos
pueden estar atascados a la vez.
| Conjuntos en Learning Limited | Veredicto |
|---|---|
| <30% | sano |
| 30-50% | vigilar |
| >50% | **falla** — la cuenta entera está aprendiendo, no vendiendo |

### 5. Presupuesto por conjunto ≥5x CPA (la regla que explica el atasco)
| Presupuesto diario del conjunto | Veredicto |
|---|---|
| ≥5x CPA objetivo | sano |
| 2-5x CPA | vigilar |
| **<2x CPA** | **falla** — no junta eventos suficientes para salir de aprendizaje |

**Cómo se usa en Golden:** el CPA objetivo sale de los unit economics (`12-unit-economics.md`), y
ahora también de la calculadora gratuita de Ecom Magic (`financial_analyze`, modo `cod`, por país),
que lo devuelve junto al punto de equilibrio y al ROAS de equilibrio.

⚠️ **Revisar con este umbral las cuentas que corren a $50.000/día por conjunto.** Si el CPA
objetivo de ese producto ronda los $25.000-30.000 COP, ese presupuesto es 1,7-2x: zona de fallo o
de vigilancia, no de salud. **Esto NO se ha medido producto por producto todavía** — es lo primero
que hay que correr con este archivo en la mano.

### 6. Andromeda: 100 variaciones no son 10 conceptos
Andromeda es el motor de **RECUPERACIÓN** (retrieval) de Meta — la **primera** etapa del sistema de
recomendación de anuncios. De **decenas de millones** de anuncios candidatos selecciona **unos pocos
miles** que pasan a competir. **Decide quién COMPITE, no quién gana**: el ganador de la subasta lo
deciden los modelos de ranking posteriores (fuente primaria: blog de ingeniería de Meta, "Meta
Andromeda", 2-dic-2024, leído en vivo por el CdM el 2026-08-31).

Cada anuncio se representa como un **embedding precomputado** del creativo, en un **índice jerárquico**
que escala a un volumen enorme de creativos. Consecuencia estructural (inferencia razonada, NO palabra
literal de Meta): dos creativos casi idénticos caen cerca en ese índice y compiten por el mismo espacio
de recuperación — repetir el mismo ángulo con otras palabras **no amplía a cuánta gente eres elegible**.

⚠️ **CORRECCIÓN 2026-08-31 (verificada contra la fuente primaria):** la versión anterior de este
control afirmaba un **"Similarity Score superior al 60% = supresión de recuperación"**. Ese umbral del
60% **NO aparece en el blog de Meta** — venía de terceros (agencias / `claude-ads`), no de Meta. Se
retira como cifra. Lo que la fuente SÍ sostiene es lo estructural de arriba, sin número de corte.

**Esto choca de frente con la forma de producir de Golden.** El estándar de 5+5+5 copys y lotes como
los 70 videos de Toppik **solo suman si los conceptos son distintos**: cinco formas de decir la misma
frase caen en la misma rama del índice y no amplían el alcance de recuperación.

La distinción operativa: **variación** es el mismo ángulo con otras palabras; **concepto** es otro
ángulo, otro dolor, otro formato o otro protagonista. `golden-matriz-viral` y `golden-copywriting` ya
trabajan por ángulos: **el ángulo es la unidad que cuenta, no el archivo**. Umbral operativo de Golden
(criterio PROPIO, no de Meta): una cuenta con **menos de ~10 conceptos genuinamente distintos** queda
marcada para revisar diversidad.

**Lo que Meta reporta de Andromeda (cifras de la fuente primaria, con su condición):** +6% recall del
sistema de recuperación · +8% calidad de anuncios en segmentos seleccionados · **+22% ROAS en
anunciantes que NO usaban Advantage+ creative y activaron su targeting por IA** (la condición importa:
no es +22% para todos) · +7% conversiones con generación de imagen. El contexto que explica el porqué:
más de **1 millón de anunciantes generaron 15 millones de anuncios en un mes** con las herramientas de
IA de Meta — esa avalancha de creativos es el problema que Andromeda resuelve.

> Nota sobre "el primer frame es targeting": circula en agencias que Meta lee el primer fotograma del
> video para decidir la entrega. Es **plausible** (el creativo sí determina elegibilidad vía embedding)
> pero **NO aparece en la fuente primaria de Meta**. Queda como observación de mercado, nunca criterio.

### 7. La caída de CTR de febrero de 2025 no fue tuya
En febrero de 2025 Meta redefinió la métrica de **link clicks**: ahora **excluye los clics de
interacción social**. Las cuentas vieron caer el CTR sin que el creativo empeorara.
**Control:** antes de declarar fatiga por una caída de CTR, verificar que la caída no coincida con
ese cambio de definición. Un creativo bueno pudo ser jubilado por un cambio de contador.

### Extra: Offline Conversions API está discontinuada (mayo 2025)
Si alguna cuenta sigue configurada contra ella, está mandando datos a un sistema muerto.

## Orden de lectura en un diagnóstico

Estos siete van **antes** de mirar creativos o presupuesto. Si la señal está rota, todo lo demás
se mide sobre datos falsos. El orden es: CAPI → dedup → EMQ → Learning Limited → presupuesto por
conjunto → Andromeda → verificación de la métrica.

## Lo que NO está verificado

- **Corrido contra cuentas reales: SOLO el control 3 (EMQ)**, el 27-ago sobre el píxel Colombia.
  Resultado arriba. Los controles 1, 2, 4, 5, 6 y 7 **siguen sin correr**: son el estándar a medir,
  no un diagnóstico. El más urgente de los que faltan es el 5 (presupuesto por conjunto).
- **Andromeda (control 6):** lo ESTRUCTURAL (recuperación vs ranking, índice por embedding de creativo)
  y las cifras de lift quedan verificados contra la fuente primaria de Meta (31-ago). Lo que NO tiene
  respaldo de Meta y se retiró: el umbral "Similarity >60%". El umbral operativo de "~10 conceptos
  distintos" es criterio propio de Golden, sin medición en cuenta real todavía.
- **La deduplicación (control 2) NO se pudo medir** con las herramientas del conector:
  `ads_get_dataset_quality` da EMQ y cobertura de claves, pero no tasa de dedup. El pendiente de
  memoria sobre el posible Purchase doble **queda abierto**, ahora con más contexto pero sin
  veredicto.
- La lectura de EMQ y dedup requiere `ads_get_dataset_quality` y `ads_get_dataset_stats`, que ya
  están disponibles en el conector de Meta.
