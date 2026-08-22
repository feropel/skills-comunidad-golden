# Estándar de Meta MEDIDO · largos, formato y molde COD

<!-- Medido el 2026-08-10 en el chat Le'côterra. Tres fuentes externas + histórico propio. -->

Esto no son buenas prácticas de blog: son tres fuentes contrastadas y medidas. Cuando escribas
copy de Meta, este archivo manda sobre cualquier intuición de largo.

## 1 · Límites oficiales (fuente autoritativa)

Centro de ayuda de Meta, artículo **223409425500940** — *"Prácticas recomendadas de creatividad
para el texto de los anuncios"*:

| Campo | Recomendado por Meta |
|---|---|
| Texto principal | **125 caracteres** |
| Título / headline | **40 caracteres** |
| Descripción | **25 caracteres** |

Textual: *"el texto principal debe ocupar 1 a 3 líneas como máximo"*.

**La descripción es 25, no 30.** Medio internet repite 30 y se equivoca. Meta **trunca en
silencio**, no rechaza: el copy entra, se ve cortado y nadie se entera.

Meta también recomienda **de forma explícita cargar varias opciones por campo** para que el
sistema optimice la entrega. El estándar 5+5+5 de esta skill está respaldado por la fuente.

## 2 · El rendimiento es BIMODAL (lo que contradice al consejo estándar)

AdSpyder, sobre **43,9 millones de anuncios de Meta** (muestra aleatoria de 8.815):

| Largo del texto principal | Supervivencia a 30 días |
|---|---|
| **menos de 50 caracteres** | **15,5%** — el mejor |
| 250 a 500 | 10,8% — segundo pico |
| **50 a 125** | **7,7% — el peor** |

**Meta premita los extremos y castiga el término medio.** La mediana histórica de los 43M es 118
caracteres — justo dentro del valle. La mayoría del mercado escribe en la zona que peor funciona.

**Límite del dato, declararlo siempre:** mide **cuánto tiempo vive un anuncio**, no cuánto vende.
Un anuncio que sigue al aire suele ser uno que el anunciante no apagó, lo cual correlaciona con
que funciona — pero es un indicio, no una prueba de conversión.

### Cómo se aplica al 5+5+5

> **Actualizado 2026-08-21 · el polo corto YA se ejecutó, y el mecanismo tiene fuente oficial.**
> Dos corridas se cerraron diciendo "los cortos nunca salieron al aire". Ya salieron: BLUE CP2,
> campaña OPEN 7, anuncio `OPEN 7 - V5 Bergamot`, cuerpo de **33 caracteres** (`BERGAMOT 36 es
> cítrica y fresca 🧊`). **No es una pieza suelta: `OPEN 7` (14-ago) y `OPEN 8` (19-ago) son una
> tanda entera de copy corto en 8 cuentas**, 32-52 caracteres, 8 creativos leídos.
>
> **Y en agregado el corto PIERDE.** Misma marca, mismos 30 días, top-5 por gasto de cada cuenta:
> **corto 2.030.367 COP / 37 compras / CPA 54.875** contra **largo 8.635.362 COP / 193 compras /
> CPA 44.743** — el corto **23% más caro**. En las cuentas en dólares pasa lo contrario (9 vs 13
> USD) pero sobre 8 compras y otro mercado: no se suman, no hay ganador.
>
> **El dato que manda no es cuál gana: es que el mismo copy corto va de CPA 17.037 (INTER CP2) a
> 123.710 (GOLDEN CP1) — siete veces entre cuentas.** Esa dispersión es más grande que el 23% que
> se quiere medir. **Mientras sea así, el experimento corto-vs-largo no puede dar veredicto**, y
> el pico 1 del modelo bimodal sigue SIN probarse — ahora por varianza, ya no por falta de datos.
> Coherente con §6: el texto no es la variable dominante.
>
> El mecanismo de opciones múltiples **existe y Meta lo documenta**: *"Add text options: input
> multiple text options for the primary text, headline and description fields **when creating
> single image or video ads**"* (artículo 223409425500940). Aplica **solo a imagen o video único**.
> Lo que sigue sin poder verificarse por API es si un anuncio del arsenal lo tiene montado: la
> lectura devuelve un solo `body` por creativo y no expone `asset_feed_spec`. Van tres corridas.
> Para comprobarlo hay que abrir el anuncio a mano en el Administrador.

Los 5 textos principales **no se escriben todos del mismo largo**. Reparto por defecto:

| | Largo | Nivel de consciencia (Schwartz) |
|---|---|---|
| Texto 1 | menos de 50 | Más consciente: ya sabe lo que quiere |
| Texto 2 | menos de 50 | Consciente del producto: compra por el beneficio |
| Texto 3 | 250 a 500 | Consciente del problema: no sabe que hay solución |
| Texto 4 | 250 a 500 | Consciente de la solución: duda del mecanismo |
| Texto 5 | 250 a 500 | Necesita prueba antes de comprar |

Dos cortos y tres largos cubren los dos picos y **esquivan el valle 50-125**. Además, repartir
niveles de consciencia dentro del mismo conjunto le da al algoritmo con qué emparejar a cada
persona, en vez de cinco versiones del mismo mensaje compitiendo entre sí.

> ### Cómo se MONTA, que es donde se ha estado rompiendo
>
> Los 5 textos van como **opciones múltiples del campo Texto principal DENTRO DE UN MISMO
> ANUNCIO** — que es exactamente lo que Meta recomienda en el artículo 223409425500940 para que
> su sistema optimice la entrega. **No** como cinco anuncios distintos con un texto cada uno.
>
> **Esto no es un detalle de forma: es la diferencia entre probar el estándar y no probarlo.**
> Corrida del 2026-08-10: los 165 copys de Le'côterra se cargaron con **un solo cuerpo de 332
> caracteres por creativo**, y no salió al aire ni un copy de menos de 50 en ninguna de las 14
> cuentas con gasto. Se comparó largo contra largo. El reparto 2+3 lleva meses sin ejecutarse.
>
> **Antes de dar por buena o por mala esta tabla, verifica que los cortos estén corriendo.**

## 3 · Los primeros 125 caracteres son el anuncio entero

Ahí cae el **"Ver más"** y la mayoría no lo abre.

**Regla dura: en todo texto largo, el argumento de venta —precio, garantía de duración, envío
gratis, prueba social— tiene que caber dentro de los primeros 125 caracteres.**

Esta es **la clase de fallo más común al auditar copys largos**: el gancho se come la ventana
visible y el argumento queda escondido detrás del "Ver más". En la corrida de Le'côterra,
**13 de 33 textos largos fallaban esto** en el primer borrador. Revísalo siempre, uno por uno.

**Contraejemplo medido, tenlo presente antes de aplicarla como ley:** el anuncio que más vende
de todo el arsenal Golden —Tag Recede VIDEO 8, 43 compras a 24.531 COP de CPA en 30 días
(cuenta BLUE CP1, medido 2026-08-10)— tiene un cuerpo de **185 caracteres** y **no menciona
precio, envío gratis ni pago contra entrega en ningún punto**. Es un vertical con
restricciones de claims (uñas/hongos) y no hay un A/B contra él, así que no tumba la regla.
Lo que sí obliga: **cuando el producto no puede prometer, la regla no aplica; no le metas una
oferta al copy solo para cumplirla.**

**Actualizado 2026-08-16, ya no es un caso aislado.** Se leyeron los 5 anuncios de mayor
volumen de tres cuentas distintas —Le'côterra CP2, Tag Recede BLUE CP1 y Dolce CP1 (por
primera vez cruzado)— y **ninguno de los cinco mete el argumento de venta en los primeros
125 caracteres, y los cinco venden**: V6·15 copys (332 car., 3 compras, CPA 15.030), V6
Bergamot (221 car., 14 compras, CPA 40.765), Tag Recede VIDEO 8 (185 car., 31 compras, CPA
24.381), Dolce Anuncio 3 (361 car., 35 compras, CPA 24.496) y Dolce Anuncio 3 Drive (485
car., 9 compras, CPA 16.569). **Le'côterra y Dolce no tienen restricción de claims de salud**
— el escudo que protegía la excepción de Tag Recede ya no aplica a los otros dos. La regla
sigue siendo el consejo por defecto (y Meta la respalda en el artículo oficial), pero **deja
de tratarse como ley dura sin excepción: se sostiene en 0 de 5 de los mayores vendedores
medidos.** Sigue faltando el A/B directo — no hay un anuncio idéntico que SÍ cumpla la regla
corriendo en paralelo para comparar contra estos cinco. Detalle completo en la entrada
2026-08-16 de `tendencias-vivas.md`.

**Actualizado 2026-08-21, tercera corrida: 0 de 8, y ya hay explicación.** Ocho anuncios con
cuerpo legible y ventas, en cuatro cuentas y cuatro verticales, **ninguno** mete el argumento
en los primeros 125: Dolce Anuncio 3 Drive (485 car., 16 compras, CPA 14.794), Dolce Anuncio 3
(361, 41, 22.946), Tag Recede VIDEO 8 (185, 21, 23.779), Dolce Anuncio 19 Drive (485, 13,
33.622), Le'côterra V6 vigente (221, 8, 37.344), V6 15 copys (332, 13, 38.165), V6 CP1 (221,
14, 40.765) y OPEN 7 V5 (33, 2, 42.174).

**La explicación no es que la regla esté mal: es que la oferta se mudó de sitio.** En los tres
cuerpos de mercado leídos el 2026-08-21 —Alquimia Store, Caphero leather y Laboratorio special
xs— los tres ponen la promesa logística en el **titular o la descripción del enlace**, no en el
cuerpo. Y el titular **no se corta nunca**; los primeros 125 del cuerpo sí desaparecen tras el
"Ver más" si el lector no lo abre.

**Cómo aplicarla desde ahora:**
1. **La oferta va en el TÍTULO** (40 caracteres, siempre visible). Ese es el sitio seguro.
2. Si la oferta ya está en el título, **el cuerpo queda libre para el argumento** y la regla de
   los 125 deja de ser obligatoria — pasa a ser preferencia.
3. Si la oferta **no** está en el título, entonces sí: métela en los primeros 125 del cuerpo.
4. Producto que no puede prometer (claims restringidos): no le inventes una oferta para cumplir.

**Contraste medido, con su límite:** en Dolce CP1, mismo producto y misma cuenta, título-oferta
(`🚛Envío gratis y Pago Contraentrega📦`, 41 compras, CPA 22.946) contra título-beneficio (`Usa
tu celular sin sacarlo del bolso`, 16 compras, CPA 14.794). Gana el beneficio, **pero el CTA
también cambia entre los dos**, así que no aísla la variable. No lo cites como prueba de que el
título-beneficio gana.

## 4 · El molde COD que está corriendo en Colombia

> **Actualizado 2026-08-21 · dos cambios medidos en el molde.**
> **(a) La oferta emigró al titular.** En los 3 cuerpos de mercado leídos hoy, los 3 sacaron la
> línea 🚚 y la línea 💵 del cuerpo y las pusieron en el titular o la descripción del enlace.
> **(b) Apareció una tercera variante, la del MECANISMO** (Laboratorio special xs): pregunta de
> apertura *"¿Cómo funciona exactamente X? 🤔"* → ingredientes o piezas → cada una traducida a
> beneficio con emoji → remate que desactiva la incredulidad (*"No es magia — es que…"*) →
> **precio + envío + contra entrega consolidados en UNA línea** → cierre hacia conversación
> (*"¿Tienes preguntas? Escríbenos antes de comprar 👇"*), destino WhatsApp. Sirve para producto
> que necesita explicarse antes de venderse.
> **(c) Registro de marca, no de catálogo** (Caphero leather): tres párrafos, cero emoji, cero
> bullets, cero precio, toda la oferta en el titular. Es el molde del perfil "marca propia".

De cuerpos completos de anuncios activos leídos en la Biblioteca de Anuncios (CreaClub, Seta,
Cedanni). Los tres, la misma forma exacta:

```
😩 Hook de dolor, una sola línea
(línea en blanco)
Qué es el producto y qué hace
(línea en blanco)
✅ beneficio
✅ beneficio
✅ beneficio
(línea en blanco)
🚚 Envío GRATIS
(línea en blanco)
💵 Paga al recibir
(línea en blanco)
👉 CTA
```

**Una idea por línea, línea en blanco entre bloques, emoji al inicio de cada línea.** Muy
escaneable en móvil, que es donde compra el 74% del tráfico LatAm.

### Títulos: 57 anuncios activos medidos con script

Medición del **2026-08-10 (tarde)**, 3 términos de búsqueda, títulos únicos por página, 45
páginas distintas. Script reproducible con autotest en la bitácora de la tarea programada.

| Métrica | Valor |
|---|---|
| Longitud media | **30 caracteres** |
| Mediana | 31 |
| Cabe en 40 | **82%** |
| Cabe en 25 | 40% |
| Lleva emoji | **51%** (mitad al final, un tercio al inicio) |
| Va en MAYÚSCULAS | 26% |
| **Usa el título para la OFERTA** (envío gratis / paga al recibir) | **32%** |
| Usa el título para el PRECIO | 9% |
| Sin título, o con `{{product.name}}` sin resolver | **19% del total traído** |

**Cuidado al comparar con mediciones viejas.** Una primera medición a mano (35 títulos) dio
33 caracteres, 60% emoji y 51% de oferta. No dejó escrito su método de deduplicación ni su
criterio de "oferta", así que **la diferencia es de método, no prueba que el mercado se moviera**.
Sumando los títulos de precio, la cifra comparable de oferta sube a 41%. **Manda la medición
con script, que es la que se puede repetir.**

El accionable no cambia: **un tercio largo del mercado colombiano usa el título para la oferta
y no para el beneficio.** Reparto recomendado por concepto: **3 títulos de beneficio + 2 de
oferta.** Y el 19% que desperdicia el titular es el hueco más barato de aprovechar.

### Emojis

Los estudios que circulan (+20% CTR, +30-56%, +241%) salen de blogs de agencias que se citan
entre sí, sin metodología publicada. **Tratar como señal, jamás como dato.** Lo que sí es
observable y medido: **el 60% de los anuncios activos en Colombia llevan emoji en el título**, y
todos los cuerpos COD leídos abren cada línea con uno. El mercado ya decidió.

## 5 · Tildes

Los anuncios que están corriendo las llevan. Una tilde faltante se lee como descuido y el copy
pierde autoridad. **Escribir siempre con ortografía correcta** — recordando que la regla de la
casa prohíbe los signos de apertura `¿` `¡`, que es otra cosa.

## Cómo volver a levantar esta evidencia

- **Límites oficiales:** `ads_get_help_article` del MCP de Meta.
- **Títulos del mercado:** `ads_library_search` con `countries: ["CO"]`, `ad_active_status: ACTIVE`
  y un término de oferta ("envío gratis", "paga al recibir"). Devuelve el **título**, nunca el cuerpo.
- **Cuerpo del anuncio:** hay que **scrapear el `ad_snapshot_url` con firecrawl** (`waitFor: 4000`,
  `onlyMainContent: true`). El cuerpo aparece después de `**Sponsored**`.
- **Trampa a evitar:** la API devuelve por **recencia**, así que casi todo lo que trae lleva horas
  al aire. Sirve para leer el molde del mercado, **no para probar qué convierte**. Si necesitas
  ganadores, cruza contra las campañas propias (ver `tendencias-vivas.md`).
- **Rendimiento propio:** `ads_get_ad_entities` a nivel `ad`. El campo del texto NO viene ahí:
  trae `creative_id` y después pide el `body` y el `title` con `ads_get_creatives`.

### La trampa que más gasto esconde (verificada el 2026-08-10)

Al pedir los anuncios hay que filtrar por `effective_status`, pero **si filtras solo por
ACTIVE / PAUSED / ADSET_PAUSED / CAMPAIGN_PAUSED te pierdes la mayoría del gasto.** Medido:
GOLDEN CP1 devolvió **cero anuncios** teniendo 3.290.484 COP gastados en 30 días, y Le'côterra
CP 2 mostró 502.980 de 3.612.625 COP reales. **Casi todo el gasto del mes vive en anuncios
ARCHIVED, DELETED o WITH_ISSUES**, porque las campañas se archivan al rotarlas.

Pide siempre la lista larga: `ACTIVE, PAUSED, ADSET_PAUSED, CAMPAIGN_PAUSED, ARCHIVED, DELETED,
DISAPPROVED, PENDING_REVIEW, PREAPPROVED, PENDING_BILLING_INFO, IN_PROCESS, WITH_ISSUES`.

**Y después cuadra**: suma el gasto de los anuncios y compáralo contra el total de la cuenta a
nivel `ad_account`. Si no cuadra, te falta cobertura — ese cuadre es lo único que delata el
hueco, porque una lista corta no da error, devuelve menos y parece correcta.

### Cuántas cuentas hay que mirar

`ads_get_ad_accounts` con `limit: 100`. El 2026-08-10 devolvió **75 cuentas**: 62 consultables,
13 no (DISABLED, UNSETTLED o CLOSED). De las consultables, solo **36 tienen medio de pago** y de
esas **14 tuvieron gasto en 30 días**. Ese embudo 75 → 36 → 14 es el denominador del informe.
**`GOLDEN CP BACK UP` (408753721820872) no se toca ni se lee** — orden del Centro de Mando.

## 6 · El copy NO es la variable dominante (medido 2026-08-21)

Antes de reescribir un copy que rinde mal, **descarta primero destino y creativo.**

En Dolce CP1, tres creativos llevan el **mismo cuerpo byte por byte** (485 caracteres), mismo
producto, misma cuenta, mismos 30 días:

| CTA | Gasto | Compras | CPA | ROAS |
|---|---|---|---|---|
| WHATSAPP_MESSAGE | 236.700 | 16 | **14.794** | 4,81 |
| SHOP_NOW | 437.084 | 13 | 33.622 | 3,35 |
| SHOP_NOW | 238.692 | 2 | 119.346 | 0,84 |

**Mismo texto, CPA de 14.794 a 119.346 — ocho veces.** La comparación honesta es entre los dos
con muestra decente: **WhatsApp 2,3x mejor que SHOP_NOW con texto idéntico** (16 y 13 compras).
El de CPA 119.346 tiene 2 compras y no aguanta conclusión.

**Qué obliga esto:** un copy no se juzga contra su CPA a secas. Si dos piezas con el mismo texto
se separan 8x, el texto no explica la diferencia. Al auditar, pregunta primero **a dónde manda el
anuncio y con qué creativo corre**, y solo después toca las palabras.

## 7 · Qué del mercado se puede medir y qué no (método, 2026-08-21)

Tres corridas de 150 anuncios por recencia dejan esto claro:

- **El largo del título SÍ es medible.** Media 30,1 → 29,6 → 30,0; "cabe en 40" entre 81% y 84%.
  Estable en tres muestras independientes. Úsalo como base.
- **Emoji, MAYÚSCULAS y "título = oferta" NO son medibles así.** Emoji hizo 51% → 65% → 26% en
  tres corridas. Eso no es una tendencia, es una muestra que cambia de composición. Se probó la
  robustez midiendo **1 título por página** (neutraliza al anunciante que repite): 30%, casi igual
  — o sea, no lo sesga un anunciante concentrado, **el indicador se mueve solo**.
- **Corrección explícita a la corrida del 2026-08-16:** allí se anotó el alza de emoji y
  MAYÚSCULAS como "señal a vigilar". Era ruido. No se sostiene.
- **Recordatorio permanente:** la API devuelve por RECENCIA. Muestra el molde del mercado, **no
  prueba qué convierte.** Nunca lo reportes como "lo que funciona".
