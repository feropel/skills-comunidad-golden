# Segmentación: desde cero vs desde histórico

La segmentación NO se inventa cuando hay datos. Dos caminos según haya o no historial del producto
(o de uno similar) en la cuenta.

## A) SIN histórico (producto/cuenta nuevos) → recomendar
- **Público amplio** (Advantage+ Audience) — deja que el algoritmo encuentre; en COD rinde más que estrecho.
- **Edad/sexo** por el **buyer persona** de la investigación (marcado como hipótesis a validar).
- **Ubicaciones**: país + ciudades con **cobertura COD**; excluir zonas sin reparto.
- Intereses solo como "pista" (con IDs reales vía `ads_targeting_search`; NO inventar IDs).
- Es una hipótesis: el testeo (Modo B) la valida y luego se ajusta con lo que compre.

## B) CON histórico → basar la segmentación en QUIÉN COMPRA (no quién ve)
Saca los **breakdowns reales** del MCP y sesga la campaña nueva hacia lo que convierte. Usa
`ads_get_ad_entities` con `breakdowns` (uno por llamada) + campos `spend`, `actions:omni_purchase`,
`cost_per_result`, `purchase_roas` — mirando **compras/CPA**, no impresiones:
| Dimensión | breakdown | Qué decide |
|---|---|---|
| Sexo | `gender` | a qué sexo priorizar / excluir |
| Edad | `age` | rango de edad que compra barato |
| Ubicación | `region` (o `country`) | ciudades/regiones con mejor CPA |
| Plataforma | `publisher_platform` | Facebook vs Instagram |
| Posición | `platform_position` | Feed vs Reels vs Stories |
| Dispositivo | `impression_device` | móvil/desktop (casi siempre móvil en COD) |

- **Construye la nueva segmentación** con el sesgo ganador (ej. si el 70% de las **compras** son mujeres
  35–55 en Bogotá/Medellín y el CPA más bajo es en IG Reels → priorizar eso). Repórtalo con el número.
- **Públicos**: crea **Custom Audience de compradores** del histórico y su **Lookalike 1–3%**
  (`ads_create_custom_audience`) — la señal de segmentación más potente que existe.
- **No sobre-estrechar**: usa el histórico como semilla/sesgo, deja que Advantage+ expanda. El dato
  manda sobre la corazonada, pero el algoritmo amplía mejor con público sano.

> Salida: una tabla "quién compra" (sexo/edad/ubicación/plataforma con su CPA) → traducida a la
> segmentación exacta de los conjuntos nuevos. Va en `META-ADS.md`.

## C) Segmenta por el COMPRADOR REAL de cada creativo/producto — NO por la etiqueta ni "a ciegas abierto"
> **Aplica SOLO si hay data real/histórico** (la excepción: producto ya vendido o relanzamiento a otro
> país). Para producto **NUEVO sin datos — el caso normal — el default es Modo B (testeo)** (ver §A) y
> **NO se pide ni se asume métricas**: el testeo revela al comprador real y recién ahí se aplica lo de abajo.

Regla de oro (validada en Le'côterra, cuidado personal COD Colombia): el segmento se decide por **quién
compra ese creativo/producto**, no por el género que dice la etiqueta del producto ni dejando todo
"abierto" por comodidad.
- Un producto **"para hombre"** puede tener comprador **MUJER** (lo regala a su pareja) y uno **"para
  mujer"** comprador **hombre**. La etiqueta engaña; el pedido no.
- **Un conjunto (o campaña) por comprador-objetivo** y **FONDEA todos con presupuesto real**. El error
  caro es **subfinanciar** un segmento (ej. hombres) y concluir "no funciona": nunca salió de learning.
  Sin fondeo comparable, no hay veredicto — hay hambre de datos.
- **Cuidado con la demografía "de la cuenta"**: está sesgada por lo que ya pautaste (self-fulfilling).
  Caso real Le'côterra: la cuenta marcaba **"90% mujeres"** solo porque corría casi puro creativo Vanilla.
  Al fondear cada línea, el comprador real era **Vanilla → 76% mujeres** (regalo íntimo femenino),
  **Bergamot → 90% hombres** (autocompra masculina), **Athletix → 50/50** (pies/objetos, uso familiar).
  Tres compradores distintos que la cuenta escondía. Fondea, mide por PEDIDOS (ver `01-fuentes-datos.md`
  §D) y deja que cada creativo pre-califique a su comprador.
