> 🔒 **DATO LOCAL — NO DISTRIBUIBLE.** Este archivo trae CPA y rendimiento REALES de cuentas Golden con nombre. Se queda en la máquina de FER; si la skill se publica a alumnos, este archivo se EXCLUYE o se reemplaza por cifras de ejemplo (rótulo puesto por el CdM, 2026-08-20, autoevalúo del ecosistema).

# Tendencias vivas · bitácora que se refresca cada 8 días

<!-- Lo escribe la tarea programada `copywriting-tendencias-8-dias`. Entrada nueva ARRIBA. -->
<!-- Nunca se borra una entrada: se apila. El histórico es lo que deja ver qué envejece. -->

**Qué es esto:** lo que el mercado y las campañas propias de Golden dicen HOY sobre qué copy
vende. `estandar-meta-medido.md` es la base estable; este archivo es lo que se mueve.

**Cómo leerlo:** la entrada de arriba es la vigente. Si contradice a `estandar-meta-medido.md`,
manda la evidencia más reciente **siempre que traiga números y fuente**; si la entrada nueva es
una impresión sin medir, manda la base.

---

## 2026-08-21 · corrida 3 de la tarea automática

**Nota de higiene previa:** la skill se encontró **desblindada otra vez** (sin `uchg`). Esta vez
sí hay explicación: `tendencias-vivas.md` tiene fecha de modificación **2026-08-20 11:32**, que es
el día y la hora del autoevalúo del ecosistema en que el CdM le puso el rótulo "DATO LOCAL — NO
DISTRIBUIBLE" a este archivo. El CdM editó y no volvió a blindar. **Van dos corridas seguidas
encontrándola abierta** — el ritual de re-blindaje no se está cumpliendo fuera de esta tarea.

**Cobertura:** 74 cuentas inventariadas (`limit:100`, mismo número que la corrida anterior),
**42 barridas una por una** a nivel cuenta — las 36 consultables con medio de pago sin contar
`GOLDEN CP BACK UP` (excluida por orden del CdM, ni se lee) **más 6 sin medio de pago que las
corridas anteriores no miraban** (Lecoterra CP4/CP5, otra marca CP4/CP5, Vantta GUATE CP3, 2 CP
ORGANIC USA — las seis en cero, confirmado, ya no quedan como hueco). **17 con gasto en 30
días**, igual que la corrida pasada. 5 cuentas bajadas a nivel anuncio, 14 creativos leídos con
cuerpo completo. Mercado: 3 términos, 150 anuncios traídos, 57 páginas, 62 títulos medibles,
4 cuerpos pedidos por firecrawl (3 leídos, 1 fuera de la biblioteca).

### Lo más importante: por fin salió al aire un copy CORTO, y el mismo texto exacto rindió 8x distinto

**Dos hallazgos que valen más que todo el resto de la corrida.**

**1) El polo corto del estándar SE EJECUTÓ.** Van dos corridas diciendo que "los cortos nunca
salieron al aire". Ya no: en BLUE CP2, campaña **OPEN 7**, corre `OPEN 7 - V5 Bergamot` con un
cuerpo de **33 caracteres** — `BERGAMOT 36 es cítrica y fresca 🧊`. Resultado: 84.348 COP,
2 compras, CPA 42.174, **ROAS 3,62 — el más alto de los diez anuncios de esa cuenta.**
**Dos compras no son un veredicto**, y hay que decirlo así: es la primera ejecución del pico 1,
no su prueba. Pero deja de ser un hueco imposible de medir y pasa a ser una muestra que crece.

**2) El texto NO es la variable dominante — y ahora hay número.** En otra marca CP1, tres creativos
llevan el **mismo cuerpo byte por byte** (485 caracteres, "Usa tu celular sin sacarlo del bolso"),
mismo producto, misma cuenta, mismos 30 días:

| Creativo | CTA | Gasto | Compras | CPA | ROAS |
|---|---|---|---|---|---|
| 1363885315721657 | **WHATSAPP_MESSAGE** | 236.700 | 16 | **14.794** | 4,81 |
| 27989016884027390 | SHOP_NOW | 437.084 | 13 | 33.622 | 3,35 |
| 1565637911952315 | SHOP_NOW | 238.692 | 2 | **119.346** | 0,84 |

**Mismo texto, CPA de 14.794 a 119.346: ocho veces.** El copy no explica esa brecha; el CTA y el
creativo sí. Los dos con muestra decente (16 y 13 compras) dan **WhatsApp 2,3x mejor que
SHOP_NOW con texto idéntico** — esa es la comparación honesta; el de CPA 119.346 tiene 2 compras
y no aguanta conclusión. **Consecuencia para la skill: al auditar un copy que rinde mal, mirar
primero destino y creativo antes de reescribir el texto.** Un copy no se juzga solo contra su CPA.

### El estándar 2 cortos + 3 largos: primera comparación pareja de verdad

En BLUE CP2, mismo video (V6 Bergamot), misma cuenta, mismos 30 días:

| Lote | Gasto | Compras | CPA |
|---|---|---|---|
| `V6 · Bergamot · 15 copys` (lote nuevo) | 496.151 | 13 | **38.165** |
| `Video 6 · Bergamot · mejor CPA` (vigente) | 298.751 | 8 | **37.344** |

**Empate técnico: 2% a favor del vigente sobre 13 y 8 compras.** Es el mismo empate que dio la
corrida 1 (41.207 vs 40.303) con muestra distinta. **Dos mediciones independientes apuntando a lo
mismo: el lote nuevo no gana ni pierde.** Sigue sin ser un veredicto, pero deja de ser ruido.

**Y el creativo "15 copys" SIGUE llevando un solo texto de 332 caracteres.** Lo leí completo. Van
**tres corridas** sin poder confirmar opciones múltiples: la API expone un `body` y un `title` por
creativo, sin `asset_feed_spec`. **Novedad de fuente:** el artículo oficial de Meta (223409425500940)
sí documenta el mecanismo con nombre — *"Add text options: input multiple text options for the
primary text, headline and description fields **when creating single image or video ads**"*. Es
decir, el 5+5+5 existe y está soportado, pero **solo en anuncios de imagen o video único**, y la
API de lectura no lo devuelve. El hueco es de lectura, no de que el mecanismo no exista.

### La regla de los 125: 0 de 8, tercera corrida seguida

Ocho anuncios con cuerpo legible y ventas, cuatro cuentas, cuatro verticales:

| Anuncio | Largo | Compras | CPA | ¿Argumento en 125? |
|---|---|---|---|---|
| otra marca · Anuncio 3 Drive (WhatsApp) | 485 | 16 | 14.794 | NO |
| otra marca · Anuncio 3 | 361 | 41 | 22.946 | NO |
| Tag Recede · VIDEO 8 | 185 | 21 | 23.779 | NO |
| otra marca · Anuncio 19 Drive | 485 | 13 | 33.622 | NO |
| Le'côterra · Video 6 vigente (CP2) | 221 | 8 | 37.344 | NO |
| Le'côterra · V6 15 copys | 332 | 13 | 38.165 | NO |
| Le'côterra · Video 6 (CP1) | 221 | 14 | 40.765 | NO |
| Le'côterra · OPEN 7 V5 (corto) | 33 | 2 | 42.174 | NO |

**Ninguno cumple. Ninguno.** Y ahora hay una explicación mejor que "la regla está mal", que sale
de leer el mercado: **la oferta emigró del cuerpo al TÍTULO.** En los tres cuerpos de mercado que
se pudieron leer hoy, los tres ponen la promesa logística en el titular o la descripción del enlace,
no en el cuerpo — Alquimia Store (*"Envío Gratis ➕ Paga en Casa"*), Caphero leather (*"🔒Paga al
Recibir + Envió Gratis"*), Laboratorio special xs (*"💰 $130.000 · Solo pagas al recibir"*). **El
título es siempre visible; los primeros 125 del cuerpo no lo son si el lector no abre "Ver más".**
Poner la oferta donde nunca se corta es mejor solución que meterla a la fuerza en los primeros 125.

**Contraste medido dentro de una sola cuenta y un solo producto** (otra marca CP1, bolso portacelular):
oferta en el título (`🚛Envío gratis y Pago Contraentrega📦`, 41 compras, CPA 22.946) contra
beneficio en el título (`Usa tu celular sin sacarlo del bolso`, 16 compras, **CPA 14.794**). Gana
el beneficio. **Ojo: también cambia el CTA entre los dos, así que no aísla la variable título.**

### Los dos fallos de higiene de otra marca SIGUEN VIVOS, y uno se replicó

Reportados a la bandeja el 16-ago, no corregidos, y verificados hoy en el creativo en vivo:
- **Negrita Unicode falsa** (`𝐔𝐬𝐚 𝐭𝐮 𝐜𝐞𝐥𝐮𝐥𝐚𝐫…`, Mathematical Bold, 4 bytes por carácter) sigue en
  los creativos `970698286006700` y `892892237194757` — juntos, **56 compras**.
- **`**asteriscos**` de Markdown literales sin renderizar**: el 16-ago estaban en 1 creativo. Hoy
  están en **3** (`1363885315721657`, `1565637911952315`, `27989016884027390`) — el copy se
  duplicó con el fallo dentro. **Se está propagando.** Fuera de mi dominio ejecutarlo; va otra vez
  a la bandeja, ahora con la nota de que se replica cada vez que alguien clona el anuncio.

### Mercado colombiano · 62 títulos medibles (57 páginas)

Mismo script con autotest (12 checks, 0 fallos), mismos 3 términos, mismo criterio de "oferta"
(envío/forma de pago, sin precio).

| Métrica | Corrida 1 (57) | Corrida 2 · 1er seg. (52) | Esta corrida · 1er seg. (62) | 1 título/página (50) |
|---|---|---|---|---|
| Longitud media | 30,1 | 29,6 | **30,0** | 29,6 |
| Mediana | 31 | 27 | 28 | 28 |
| Cabe en 40 | 82% | 81% | **84%** | 82% |
| Emoji | 51% | 65% | **26%** | 30% |
| MAYÚSCULAS | 26% | 37% | **13%** | 16% |
| Título = OFERTA | 32% | 31% | **26%** | 30% |

**El largo es la única cifra estable de las tres corridas** (30,1 → 29,6 → 30,0; cabe en 40 entre
81% y 84%). Eso sí se puede tratar como base.

**Y hay que corregir a la corrida pasada: la "tendencia a vigilar" de emoji y MAYÚSCULAS era
ruido.** El 16-ago se anotó que emoji subía 51%→65% y MAYÚSCULAS 26%→37%, "señal a vigilar". Hoy
caen a 26% y 13%, por debajo de las dos lecturas anteriores. Un indicador que hace 51 → 65 → 26 no
tiene tendencia: **tiene una muestra que cambia de composición cada corrida** (esta trajo un
catálogo de 11 títulos de lavadoras sin emoji y una tanda de dramas cortos). Se probó la robustez
midiendo también **1 título por página**, que neutraliza al anunciante que repite: 30% de emoji,
prácticamente igual. **No es el catálogo el que sesga: es que el indicador se mueve solo.**
**Conclusión de método: emoji, MAYÚSCULAS y "título = oferta" NO son medibles con 150 anuncios por
recencia. No los reportes como tendencia.** El largo sí.

### Molde COD: aparece una tercera variante, la del mecanismo

3 cuerpos leídos (Alquimia Store, Caphero leather, Laboratorio special xs). El cuarto
(Regalados colombia) devolvió *"Ad isn't in the Ad Library"* — sin impresiones todavía.

- **Alquimia Store** corre el molde clásico de una idea por línea con emoji, pero **la línea 🚚 y
  la línea 💵 ya no están en el cuerpo**: viajaron al titular. Cierra con un bloque de hashtags
  (`#Comprameloya #LinternaSolar…`), que no es habitual en COD.
- **Caphero leather** no corre el molde COD en absoluto: tres párrafos de marca, cero emoji, cero
  bullets, cero precio. Toda la oferta vive en el titular. Es el registro "marca", no "catálogo" —
  útil como referencia para el perfil de marca propia. (Lleva un typo, *"Envió Gratis"*.)
- **Laboratorio special xs · variante NUEVA, la del MECANISMO:** abre con pregunta
  (*"¿Cómo funciona exactamente G180 Plus? 🤔"*), nombra los ingredientes, los traduce a beneficios
  con emoji, remata con *"No es magia — es que por fin tu cuerpo tiene el apoyo que necesitaba"*,
  consolida **precio + envío + contra entrega en UNA sola línea** (`💰 $130.000 · Envío gratis ·
  Contra entrega`) y cierra hacia conversación, no hacia compra: *"¿Tienes preguntas? Escríbenos
  antes de comprar 👇"* con destino WhatsApp. **Vale mirarla de cerca**: es el mismo destino
  WhatsApp que en otra marca da el mejor CPA de todo el conjunto.

**La prueba social numérica antes del hook** (Levin Store 10-ago, Wonder Store 16-ago) **no
apareció en esta muestra.** Dos corridas con el patrón y una sin él: no lo des por asentado.

### Límites oficiales de Meta: SIN CAMBIO, tercera verificación

`ads_get_help_article`, artículo 223409425500940, corrido hoy: **125 / 40 / 25, sin cambio.** Sigue
el consejo *"primary text should span 1-3 lines at most"*. Tres corridas confirmándolo con la misma
fuente.

### GOLDEN CP BACK UP

No se tocó ni se leyó (`408753721820872`) — orden del Centro de Mando respetada.

### Qué quedó SIN VERIFICAR

- **`asset_feed_spec`**: tercera corrida sin poder leerlo. Ahora se sabe que el mecanismo existe y
  está documentado por Meta, y que aplica solo a imagen/video único. Lo que falta es leerlo por API
  o mirarlo a mano en el Administrador de anuncios. **Es el hueco más viejo de la bitácora.**
- **El anuncio de catálogo dinámico de Le'côterra CP2** (`VIDEO 1`, creativo `1685356375876870`) es
  **el mejor CPA de todo el conjunto: 30 compras, CPA 16.032, ROAS 5,38** — y su cuerpo sigue sin
  poder leerse (`{{product.name}}` sin resolver). **El de mejor rendimiento es justo el que no se
  puede auditar.** Van tres corridas.
- **19 de las 42 cuentas barridas no tuvieron gasto** — sin resultado que cruzar, fuera del análisis
  por diseño, no por omisión.
- **El cuerpo de mercado de Regalados colombia** no se pudo leer (sin impresiones). 3 de 4 leídos.
- **No se aisló la variable título** en el contraste de otra marca: el CTA cambia junto con el titular.
- No se bajó a nivel anuncio en 12 de las 17 cuentas con gasto (CP1/CP3/CP5/CP6/CP8/CP9, INTER
  CP1-CP5, BLUE CP5). Se priorizaron las cinco que deciden las preguntas abiertas del estándar.

---

## 2026-08-16 · corrida 2 de la tarea automática

**Nota de higiene previa a esta corrida:** la skill se encontró **desblindada** (sin `uchg`)
al empezar — no hubo forcejeo de escritura, el flag simplemente no estaba puesto. No se pudo
determinar quién la desbloqueó ni cuándo. Se re-blindó al cerrar esta corrida (ver más abajo).
Repórtalo en la bandeja: una skill desblindada es la puerta por la que dos manos se pisan.

**Cobertura:** 74 cuentas de anuncios inventariadas (`limit:100`, una menos que la corrida
anterior — una cuenta pasó a CLOSED), 62 consultables, 46 con medio de pago, 36 revisadas una
por una sin contar `GOLDEN CP BACK UP` (excluida por orden del CdM, ni se lee), **17 con gasto
en 30 días** (sube de 14). Mercado: 3 términos, 150 anuncios traídos, 46 páginas distintas, 60
títulos únicos por página, 4 cuerpos completos leídos por firecrawl.

### Lo más importante: el patrón que contradecía la regla de los 125 ya NO es un caso aislado

La corrida pasada solo Tag Recede (uñas, vertical con restricción de claims) rompía la regla de
meter el argumento de venta en los primeros 125 caracteres. Esta corrida se leyeron los 5
anuncios de mayor volumen de tres cuentas distintas — Le'côterra, Tag Recede y **otra marca por
primera vez** — y **ninguno de los cinco cumple la regla, y los cinco venden**:

| Anuncio | Cuenta | Largo | Compras (30d) | CPA | Argumento en 125 |
|---|---|---|---|---|---|
| V6 · 15 copys | Le'côterra CP2 | 332 | 3 | 15.030 COP | NO |
| V6 Bergamot | Le'côterra CP2 | 221 | 14 | 40.765 COP | NO |
| VIDEO 8 | Tag Recede BLUE CP1 | 185 | 31 | 24.381 COP | NO |
| Anuncio 3 | otra marca CP1 | 361 | 35 | 24.496 COP | NO |
| Anuncio 3 Drive | otra marca CP1 | 485 | 9 | 16.569 COP | NO |

Le'côterra y otra marca **no tienen restricción de claims de salud** — el escudo que protegía la
excepción de Tag Recede ya no aplica. **Actualizado `estandar-meta-medido.md`** con este dato:
la regla de los 125 sigue siendo el consejo por defecto (y el artículo oficial de Meta la
respalda: *"el texto principal debe ocupar 1 a 3 líneas"*), pero **ya no se sostiene como ley
dura sin excepción** — tres verticales distintas, sin restricción de claims entre ellas, venden
sin cumplirla. Sigue sin haber un A/B directo que la tumbe: los ganadores no cumplen la regla,
pero tampoco hay un anuncio idéntico que SÍ la cumpla corriendo en paralelo para comparar.

### El reparto 2 cortos + 3 largos: sigue sin ejecutarse

El copy "V6 · 15 copys" de Le'côterra —el que se cargó como el lote nuevo del estándar—
**sigue siendo un solo texto de 332 caracteres**, no cinco opciones dentro del mismo anuncio.
La API de creativos sigue sin exponer `asset_feed_spec`, así que **de nuevo no se pudo
confirmar** si algún anuncio del arsenal usa opciones múltiples de texto. Van dos corridas
seguidas sin poder verificar esto — queda como el hueco más persistente de la bitácora.

Comparación pareja V6 (misma pieza que la corrida pasada), con MENOS gasto total esta vez
porque la campaña rotó: nuevo 45.091 COP/3 compras/CPA 15.030 vs vigente 570.705 COP/14
compras/CPA 40.765. El nuevo gana 63% más barato, **pero sobre 3 compras — muestra demasiado
chica para veredicto.** Sigue sin poder probarse el estándar de verdad mientras los "cortos"
no salgan al aire.

### Hallazgo nuevo, en copy PROPIO no de mercado: dos fallos de higiene en otra marca CP1

Al leer el cuerpo del segundo mayor vendedor de otra marca (Anuncio 3, 35 compras) apareció:
- **64 caracteres en negrita Unicode falsa** (`𝐔𝐬𝐚 𝐭𝐮 𝐜𝐞𝐥𝐮𝐥𝐚𝐫...`, rango Mathematical Bold,
  caracteres de 4 bytes) — rompe copiar y pegar, lectores de pantalla, y búsqueda de texto.
- El creativo "Anuncio 3 Drive" (9 compras, CPA 16.569) lleva `**asteriscos**` de Markdown
  **literales sin renderizar** — el mismo fallo que se vio en un anuncio de mercado
  ("Salud y bienestar") la corrida pasada, pero esta vez **es copy propio de Golden**, no un
  ejemplo ajeno. Ninguno de los dos frena las ventas (ROAS 4.16 y 3.95), pero es higiene que
  se ve y no cuesta nada corregir. **Fuera de mi dominio ejecutarlo — va a la bandeja del CdM.**

### Mercado colombiano · títulos, 60 únicos por página (46 páginas)

Medido con el mismo script con autotest de la corrida pasada, contra los mismos 3 términos.
**8 de 60 páginas no llevan título (13%, baja de 19-23%)**, cero placeholders sin resolver
esta vez. De los 52 medibles, 9 vienen concatenados por tarjetas de carrusel — se reporta
crudo y por "primer segmento" (la tarjeta 1, que es lo comparable con la corrida pasada):

| Métrica | Corrida 1 (57, script) | Esta corrida · CRUDO (52) | Esta corrida · 1ER SEGMENTO (52) |
|---|---|---|---|
| Longitud media | 30,1 | 48,7 | **29,6** |
| Mediana | 31 | 31 | 27 |
| Cabe en 40 | 82% | 67% | **81%** |
| Emoji | 51% | 65% | 65% |
| MAYÚSCULAS | 26% | 37% | 37% |
| Título = OFERTA | 32% | 31% | 31% |

**El "primer segmento" es la cifra comparable** (29,6 vs 30,1 de la corrida pasada — estable).
El "crudo" sube porque esta muestra trajo más carruseles con títulos concatenados por `|`; no
es que el mercado escriba títulos más largos, es que se cuentan las tarjetas pegadas. **Emoji
y MAYÚSCULAS sí subieron de forma consistente en ambas lecturas (51%→65%, 26%→37%)** — con dos
puntos de dato es una tendencia a vigilar, no todavía un veredicto.

### Molde COD: sigue igual, confirma la variante de prueba social numérica

4 cuerpos leídos (Smart shop, Faith, Wonder Store, Distriplaneta). **Distriplaneta corre el
molde clásico letra por letra**: hook de dolor en mayúsculas negrita, qué es, 👉 pasos,
🚚 envío + 💵 pago, cierre con CTA. **Wonder Store repite la prueba social numérica ANTES del
hook** ("Más de 1.000 unidades vendidos") que apareció por primera vez la corrida pasada en
Levin Store — **van dos corridas seguidas con el mismo patrón**, empieza a ser señal y no
ruido, aunque siguen siendo solo 2 anunciantes de una muestra pequeña.

### Límites oficiales de Meta: SIN CAMBIO, verificado de nuevo

`ads_get_help_article`, artículo 223409425500940, corrida hoy: **125 / 40 / 25, sin cambio**.
Van dos corridas confirmándolo con la misma fuente.

### GOLDEN CP BACK UP

No se tocó ni se leyó (`408753721820872`) — orden del Centro de Mando respetada.

### Qué quedó SIN VERIFICAR

- **Asset feed spec de las opciones múltiples de texto**: van 2 corridas sin poder
  confirmarlo. La API expone un solo `body`/`title` por creativo.
- **19 de 36 cuentas con medio de pago no tuvieron gasto en 30 días** — no se cruzó su copy
  porque no hay resultado que cruzar; quedan fuera del análisis de rendimiento por diseño,
  no por omisión.
- El anuncio de catálogo dinámico de Le'côterra (el de mejor CPA histórico) sigue sin poder
  leerse — su `body` sigue devolviendo `{{product.name}}` sin resolver.
- No se leyó el cuerpo de Tag Recede de nuevo (se reusó el dato de la corrida pasada, que
  sigue activo con el mismo CPA-líder); si cambió el copy desde entonces, esta corrida no lo
  detectaría.

---

## 2026-08-10 (tarde) · corrida 1 de la tarea automática

**Cobertura:** 75 cuentas de anuncios inventariadas, 36 con capacidad de gasto revisadas una
por una, 14 con gasto en 30 días analizadas a nivel anuncio. Mercado: 3 términos, 150 anuncios
traídos, 57 títulos únicos por página (45 páginas), 5 cuerpos completos leídos.

### Lo más importante: el estándar NO se pudo poner a prueba

Los 165 copys de Le'côterra ya gastaron, pero **el lote nuevo se llevó 927.574 COP de
9.457.700 COP totales de Le'côterra: el 9,8%.** Con esa tajada no hay veredicto posible.

Comparación pareja, mismo creativo (V6 Bergamot), que es la única honesta:

| Lote | Gasto | Compras | CPA |
|---|---|---|---|
| Nuevo (2 cortos + 3 largos) | 824.135 COP | 20 | **41.207 COP** |
| Vigente (lote anterior) | 3.627.229 COP | 90 | **40.303 COP** |

**Empate técnico** (2% de diferencia sobre 20 compras). En dólares lo mismo: 12,79 vs 11,65 USD
sobre 2 compras, que no significa nada.

**La excepción manda la señal:** en **BLUE CP2**, la única cuenta donde ambos lotes recibieron
presupuesto parecido, el copy nuevo **ganó**: CPA 33.653 COP (10 compras, 336.533 COP) contra
40.103 COP del vigente (11 compras, 441.128 COP) — **16% mejor**.

### Y hay un problema más grave que el resultado: el reparto no está en el aire

Leí los cuerpos reales de los anuncios "15 copys". **Cada creativo lleva UN solo texto de 332
caracteres.** No encontré ni un copy de menos de 50 caracteres corriendo en ninguna cuenta.

Es decir: **la predicción del estándar —que 2 cortos + 3 largos supera a todo-largo— no ha sido
probada, porque los cortos nunca salieron al aire.** Lo que se comparó fue largo (332) contra
largo (221). El estándar no falló: no se ejecutó. Antes de defenderlo o corregirlo hay que
montarlo de verdad, con los 5 textos como opciones múltiples dentro del mismo anuncio.

### El mayor vendedor de todo el conjunto contradice la regla de los 125

**Tag Recede** (BLUE CP1) es el mayor productor de ventas de las 14 cuentas:

| Anuncio | Gasto | Compras | CPA |
|---|---|---|---|
| VIDEO 8 | 1.054.827 COP | **43** | **24.531 COP** |
| VIDEO 4 | 1.260.267 COP | **41** | 30.738 COP |
| VIDEO 3 | 1.004.609 COP | 36 | 27.906 COP |

Su cuerpo tiene **185 caracteres** — ni pico 1 (<50) ni pico 2 (250-500): cae en la franja
125-250 que el estándar trata como zona muerta. Y **no lleva envío gratis, ni precio, ni pago
contra entrega en ningún punto del texto**, mucho menos en los primeros 125.

Cuidado con la lectura: es otro producto y otro vertical (uñas, con restricciones de claims de
salud), y no hay un A/B contra él. **No prueba que la regla esté mal; sí prueba que no es
universal.** Anotado para vigilar en la próxima corrida.

### Mercado colombiano · 57 títulos activos, medidos con script

| Métrica | 2026-08-10 mañana (35 títulos, a mano) | Esta corrida (57 títulos, script) |
|---|---|---|
| Longitud media | 33 | **30,1** |
| Mediana | sin dato | 31 |
| Cabe en 40 | 80% | **82%** |
| Lleva emoji | 60% | **51%** |
| En MAYÚSCULAS | 34% | **26%** |
| Título = OFERTA | 51% | **32%** |

**No leas esto como que el mercado se movió.** La entrada anterior se midió a mano y no dejó
escrito su método de deduplicación ni su criterio de "oferta"; esta se midió con script sobre
títulos únicos por página, contando como oferta solo envío/pago. Sumando los títulos que usan
**precio** (9%), la cifra comparable sube a 41%. **La brecha es de método, no de mercado.**
De aquí en adelante manda la cifra con script, que es reproducible.

Dato nuevo que la entrada anterior no traía: **9 de 57 anuncios no llevan título** y **4 usan
el placeholder `{{product.name}}` sin resolver** — el 19% del mercado desperdicia el titular.

### Molde COD: sigue igual, con una variante nueva

Los 5 cuerpos leídos (Merakcol, Levin Store, CreaClub, Veleo, Salud y bienestar) confirman el
molde: una idea por línea, emoji al inicio de cada línea, línea 🚚 de envío, línea de pago,
cierre con 👉 o 👇. CreaClub lo corre idéntico a como se midió en la mañana.

**Lo que apareció y no estaba:** **prueba social numérica ANTES del gancho de dolor.**
Levin Store abre con "⭐ MÁS DE 2.500 PEDIDOS ENTREGADOS EN COLOMBIA" y recién después pregunta
por el dolor; Veleo mete "+500 CLIENTES SATISFECHOS" en el titular. Levin además mete la
**escalera de combos (1 / x2 / x3) dentro del cuerpo del anuncio**, no en la página.
Es un molde a probar, no una regla: son 2 de 5 anuncios y no hay métricas de terceros.

**Fallo a no copiar:** el anuncio de "Salud y bienestar" lleva `**asteriscos**` literales en el
texto — alguien pegó Markdown en un campo que no lo renderiza. Se le ve al usuario.

### Límites oficiales de Meta: SIN CAMBIO

`ads_get_help_article`, artículo **223409425500940**, verificado hoy: siguen siendo
**125 / 40 / 25**. Textual: *"el texto principal debe ocupar 1 a 3 líneas como máximo"*.
También sigue en pie la recomendación de cargar varias opciones por campo, que es justo lo que
no se está haciendo (ver arriba). `estandar-meta-medido.md` no necesita corrección de números.

### Qué quedó SIN VERIFICAR

- **El copy del mejor CPA de todos no se pudo leer.** El anuncio VIDEO 1 de Lecoterra CP 2
  (29 compras, CPA 17.344 COP, ROAS 5,27) es de catálogo dinámico: su creativo devuelve
  `{{product.name}}` y ningún `body`. El texto vive en el catálogo, no en el creativo.
- **No se pudo confirmar si algún anuncio lleva múltiples textos** (opciones por campo): la API
  de creativos expone un solo `body` y no el `asset_feed_spec`.
- **otra marca CP 1** (5.349.836 COP, el segundo mayor gasto) usa nombres genéricos "Anuncio 1..22
  Drive" y no se le cruzó el copy contra el resultado. Queda para la próxima corrida.
- Las cuentas **GOLDEN CP2 y CP4 (UNSETTLED)** y 10 más DISABLED no son consultables: 13 de 75
  quedaron fuera por completo.

### Trampa nueva encontrada (afecta a toda corrida futura)

Filtrar `effective_status` solo por ACTIVE/PAUSED/ADSET_PAUSED/CAMPAIGN_PAUSED **esconde la
mayoría del gasto**: GOLDEN CP1 devolvió CERO anuncios teniendo 3.290.484 COP gastados, y
Le'côterra CP 2 mostró 502.980 de 3.612.625 COP. **Casi todo el gasto de 30 días vive en
anuncios ARCHIVED, DELETED o WITH_ISSUES.** Hay que pedir la lista larga de estados —y después
cuadrar la suma de los anuncios contra el total de la cuenta, que es lo que delata el hueco.

---

## 2026-08-10 · entrada inicial (medida a mano, chat Le'côterra)

**Mercado colombiano** — 35 títulos activos + 3 cuerpos completos de la Biblioteca de Anuncios:
- Título medio **33 caracteres**, 80% cabe en 40, **60% con emoji**, 34% en mayúsculas.
- **51% usa el título para la oferta** (envío gratis / paga al recibir) en vez del beneficio.
- Molde COD dominante: una idea por línea, bloque ✅, línea 🚚, línea 💵, cierre 👉.

**Dato estructural** (AdSpyder, 43,9M anuncios): rendimiento **bimodal** — gana <50 caracteres,
segundo pico 250-500, peor rango 50-125. Detalle y límites del dato en `estandar-meta-medido.md`.

**Campañas propias · Le'côterra** (histórico de 15 cuentas, medido el 2026-08-09):

| Creativo | Ventas | CPA |
|---|---|---|
| V9 · Mix | 7 | **$23.729** |
| Video 1 · Vanilla | 30 | $28.200 |
| V6 · Bergamot | **67** | $32.100 |
| Video 4 · Duo | 2 | $48.564 |
| Video 5 · Bergamot | 0 | — |

**Ángulo ganador confirmado:** *neutraliza de raíz + 48 horas*. Segundo: *base agua sin alcohol*.
Tercero: *pagas al recibir*.

**Pendiente de la próxima corrida:** los 165 copys de Le'côterra reescritos con este estándar
todavía **no han gastado un peso**. Cuando corran, esa es la primera validación real de si el
reparto 2 cortos + 3 largos supera al lote anterior, que era todo largo.

---
