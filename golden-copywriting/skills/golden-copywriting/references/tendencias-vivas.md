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

## 2026-08-25 · corrida 4 de la tarea automática

**Nota de higiene previa:** la skill se encontró **sin blindar, y esta vez eso es lo correcto.**
`GCW1.3.8` (24-ago, decisión del CdM) **derogó el `uchg`** para esta skill: la protección pasó a ser
la regla de manos autorizadas, no el flag, justamente porque el flag producía el choque que las
corridas 2 y 3 reportaron. **Mi mandato de tarea todavía ordena `chflags -R uchg` y comprobar que el
blindaje volvió: esa instrucción quedó vencida y NO la ejecuté** — la fábrica declarada manda. Va a
la bandeja para que el CdM actualice el texto de la tarea. Sí se hizo el respaldo previo.

**Cobertura:** 74 cuentas inventariadas (`limit:100`, sin `next_cursor` — mismo número que las
corridas 2 y 3). **58 barridas una por una a nivel cuenta: el censo COMPLETO de lo legible**
(74 − 13 no consultables − 2 con Ads MCP deshabilitado − `GOLDEN CP BACK UP`, excluida por orden del
CdM y ni leída). Las corridas anteriores barrieron 42; ya no queda cuenta legible sin mirar.
**16 con gasto en 30 días** (eran 17: **`INTER CP4 COL` salió — pasó a DISABLED**). 6 cuentas bajadas
a nivel anuncio, 13 creativos leídos con cuerpo completo, 8 cuerpos de creativo propio recuperados.
Mercado: 3 términos, 150 anuncios, 84 páginas, 142 títulos medibles, 5 cuerpos pedidos por firecrawl
(4 leídos, 1 vacío). Script de medición con autotest de 16 checks, 0 fallos.

### 🔴 Lo más importante: la lectura por API NO cubre el gasto de la cuenta, y eso ensucia las tres corridas anteriores

**Encontré el mecanismo del cherry-picking que la corrida 3 se autocriticó sin poder explicar.**

Al bajar a nivel anuncio, lo que la API devuelve **no suma lo que la cuenta gastó**:

| Cuenta | Gasto de la CUENTA | Gasto que suman los anuncios legibles | Cobertura |
|---|---|---|---|
| GOLDEN CP6 | 3.171.690 COP | **0 — devuelve lista vacía** | **0%** |
| BLUE CP5 DOLAR | 777,20 USD | **0 — devuelve lista vacía** | **0%** |
| BLUE CP1 | 3.545.529 COP | 167.142 COP | **4,7%** |
| GOLDEN CP1 | 4.198.431 COP | 967.222 COP | 23% |
| Le'côterra CP2 | 2.670.379 COP | 1.224.515 COP | 46% |

**No es el filtro de `effective_status`.** Lo probé contra el caso que sabía malo: GOLDEN CP6 devuelve
vacío **con filtro, sin filtro y a nivel CAMPAÑA también**. Es un hueco de la API de lectura, no del
método de consulta. La nota del mandato ("un listado sin filtro devuelve vacío") describe un caso;
**hay otro caso, el inverso, y nadie lo había medido.**

**Por qué importa para el copy y no es una nota técnica:** en BLUE CP1 el anuncio legible
`OPEN 7 - V5 Bergamot` reporta **CPA 27.783 / ROAS 5,38**. Su campaña completa —la misma campaña que
lo contiene— reporta **CPA 60.444 / ROAS 2,31**. Mirar el anuncio que la API deja ver da un número
**2,2 veces más bonito** que la realidad de la campaña. Las tablas anuncio-por-anuncio de las corridas
1, 2 y 3 se construyeron así, **sin comprobar nunca que sumaran el gasto de la cuenta.**

**Regla de método que sale de esto, y que hay que aplicar desde ya:** antes de comparar CPA entre
copys, **sumar el gasto de los anuncios leídos y contrastarlo contra el gasto de la cuenta**. Si la
cobertura no llega a un umbral decente, el ranking de copys no se reporta: se reporta la cobertura.
Es la versión medible de la lección del 21-ago ("se busca la clase entera antes de escribir la frase").

### El experimento del estándar 2+3 se APAGÓ antes de dar veredicto

El punto 9 del mandato pide cerrar el lazo: los 165 copys de Le'côterra con reparto 2 cortos + 3
largos, contra el lote anterior todo-largo. **No se puede cerrar, y no por falta de datos: el
experimento ya no existe.**

En Le'côterra CP2 ya **no corren** ni `V6 · Bergamot · 15 copys` ni `Video 6 · Bergamot · mejor CPA`
—los dos brazos que la corrida 3 midió en empate técnico (38.165 vs 37.344)—. Los 4 anuncios con
gasto de la cuenta son ahora **catálogo dinámico** (`VIDEO 1`, cuerpo `{{product.name}}` sin resolver)
más un `48 horas de frescura`:

| Creativo | Gasto | Compras | CPA | ROAS | Cuerpo legible? |
|---|---|---|---|---|---|
| 1685356375876870 | 425.611 | 29 | **14.676** | **6,03** | NO — catálogo |
| 833486096421326 | 506.655 | 15 | 33.777 | 2,82 | NO — catálogo |
| 1685356375876870 (2º ad) | 215.194 | 9 | 23.910 | 4,47 | NO — catálogo |
| 4668771433370210 | 77.055 | 1 | 77.055 | 1,04 | sí |

**Cuarta corrida seguida en que el creativo de mejor rendimiento de todo el conjunto es justo el que
no se puede auditar.** Y ahora es peor que antes: la cuenta entera migró a catálogo, así que el
83% de su gasto legible corre con un cuerpo que la API no devuelve. **El estándar 2+3 no se validó ni
se refutó: se quedó sin banco de pruebas.** Si el CdM quiere una respuesta, hay que volver a montarlo.

### El copy corto: sigue vivo, pero el conjunto lo estranguló

La tanda `OPEN 7` se mudó a **BLUE CP1** y ahí es lo único que corre en su campaña. Los tres cuerpos,
leídos completos:

| Creativo | Cuerpo | Car. | Gasto | Compras | CPA |
|---|---|---|---|---|---|
| 1821981265638223 | `BERGAMOT 36 es cítrica y fresca 🧊` | 33 | 166.697 | 6 | 27.783 |
| 2016353339017999 | `La segunda te sale en $60.000. 🎁` | 32 | **436** | 0 | — |
| 1327948092657604 | `VANILLA 26 es vainilla cálida y dura 48 horas ✨` | 47 | **9** | 0 | — |

**Dos de las tres piezas recibieron 436 y 9 pesos: entrega cero.** El algoritmo le dio el 99,7% del
presupuesto a una sola. **Eso no es un test de tres copys — es un copy con dos testigos.** Y explica
por qué el experimento corto-vs-largo nunca converge: cuando se cargan variantes como anuncios
separados, el conjunto elige uno en las primeras horas y las demás no llegan a tener muestra.
**Consecuencia directa para el 5+5+5:** refuerza que los textos van como **opciones múltiples DENTRO
de un anuncio** (mecanismo documentado por Meta), no como anuncios hermanos. Cargarlos como anuncios
hermanos garantiza que no se midan.

### El CTA vuelve a ganarle al texto, ahora con muestra decente

Corrida 3 lo vio con una pieza de 2 compras y se autocorrigió por eso. **Esta vez las tres piezas
tienen muestra.** otra marca CP1, **mismo cuerpo byte por byte** (461 caracteres, "¿Cansada de cargar
bolsos grandes…"), mismo producto, mismos 30 días:

| Creativo | CTA | Gasto | Compras | CPA | ROAS |
|---|---|---|---|---|---|
| 1363885315721657 | **WHATSAPP_MESSAGE** | 387.596 | **21** | **18.457** | 3,99 |
| 27989016884027390 | SHOP_NOW | 537.454 | 16 | 33.591 | 3,44 |
| 939600362502516 | SHOP_NOW | 496.237 | 12 | 41.353 | 2,42 |

**Texto idéntico, CPA de 18.457 a 41.353 — 2,24x. WhatsApp 1,8x mejor que SHOP_NOW.** Corrida 3 midió
2,3x en la misma dirección con otra muestra. **Dos mediciones independientes, misma dirección, ahora
con 21/16/12 compras.** Sigue sin ser un A/B controlado (el creativo de video también cambia), pero
ya no es una anécdota. **Regla que se mantiene y se refuerza: al auditar un copy que rinde mal, mirar
destino y creativo ANTES de reescribir el texto.**

### Los dos fallos de higiene de otra marca: cuarta corrida vivos, y el de asteriscos mutó

Reportados el 16-ago, el 21-ago, y verificados hoy otra vez en el creativo en vivo:

- **Negrita Unicode falsa** (`👜𝐔𝐬𝐚 𝐭𝐮 𝐜𝐞𝐥𝐮𝐥𝐚𝐫…`, Mathematical Bold, 4 bytes por carácter) sigue en
  `970698286006700` y `892892237194757` — juntos **62 compras** (48 + 14).
- **`**asteriscos**` de Markdown literales sin renderizar**: 1 creativo el 16-ago → 3 el 21-ago →
  **3 hoy, pero uno DISTINTO**. Entró `939600362502516` ("Anuncio 20 Drive") y salió del top
  `1565637911952315`. **No es que se estabilizó en 3: es que rota. Cada clonación arrastra el fallo
  dentro.** Los tres que lo llevan hoy suman 49 compras.

Fuera de mi dominio ejecutarlo. Va a la bandeja por tercera vez, ahora con el mecanismo nombrado.

### Mercado colombiano · 142 títulos medibles (84 páginas)

Mismo script, mismos 3 términos, mismo criterio de "oferta" (envío/forma de pago, sin precio).
Autotest de 16 checks **incluyendo casos negativos deliberados** (que "Solo por hoy $129.900" NO
cuente como oferta logística, que "2X$189,990" no cuente como MAYÚSCULAS): 0 fallos.

| Métrica | c1 (57) | c2 (52) | c3 (62) | **c4 · 1er seg. (142)** | c4 · 1 tít./página (76) |
|---|---|---|---|---|---|
| Longitud media | 30,1 | 29,6 | 30,0 | **32,5** | 32,5 |
| Mediana | 31 | 27 | 28 | **25,5** | 25,0 |
| Cabe en 40 | 82% | 81% | 84% | **79%** | 87% |
| Emoji | 51% | 65% | 26% | **58%** | 53% |
| MAYÚSCULAS | 26% | 37% | 13% | **27%** | 24% |
| Título = OFERTA | 32% | 31% | 26% | **22%** | 18% |

**Corrección a lo que llevo tres corridas diciendo: "la longitud media es la cifra estable" no se
sostiene.** Iba 30,1 → 29,6 → 30,0 y hoy salta a 32,5, mientras **la mediana baja de 28 a 25,5**.
Media arriba y mediana abajo significa cola larga: dos anunciantes metieron títulos de 300+ caracteres
(TYD PL Leonor, C&M) que arrastran la media y no dicen nada del típico. **La media era estable por
suerte de muestreo, no por ser robusta. La cifra que sí aguanta cuatro corridas es `cabe en 40`:
79-87%, siempre alrededor de cuatro de cada cinco.** Esa es la base, y es la que importa porque es la
que se traduce en una regla escribible.

**Y emoji vuelve a confirmar lo que la corrida 3 concluyó:** 51 → 65 → 26 → **58**. Cuatro lecturas,
ningún patrón. **Emoji, MAYÚSCULAS y "título = oferta" siguen sin ser medibles con 150 anuncios por
recencia. No los reportes como tendencia.** El único que baja de forma monótona las cuatro veces es
"título = OFERTA" (32 → 31 → 26 → 22): **es la única señal de mercado que merece vigilarse**, y aun
así con el descargo de que la muestra cambia de composición.

### Molde COD: sigue vigente tal cual, y vuelve el dato numérico

4 cuerpos leídos (Latin shop devolvió vacío):

- **klent.store · el molde canónico, intacto.** Pregunta con emoji (`😣 ¿Sientes tu cuello cansado…`),
  contexto, 3 bullets ✅, cierre, y **línea 🚚 / línea 💳 / línea 👉 por separado**. Es exactamente el
  molde que la skill enseña. **No apareció ningún molde nuevo que lo reemplace.**
- **Legado Natural (BURURAN)** corre el molde con la logística **consolidada en una línea final**
  (`🚚 ENVÍO GRATIS 💵 PAGA AL RECIBIR`) **y repetida en el título del enlace**. Novedad: el bloque de
  bullets ✅ inflado a **ocho**, mucho más de lo habitual. Destino WhatsApp.
- **Regalos de Avril (Magnesium) · el registro telegráfico, y VUELVE el dato numérico.** Frases de 3
  a 6 palabras, una por línea: pregunta → causa → **`El 70% de colombianos tiene deficiencia`** →
  3 bullets → `3 X 120.000 | Envío GRATIS` → `Compra ahora →`. Destino WhatsApp. La corrida 3 dijo que
  la prueba social numérica **no** había aparecido; **hoy vuelve**. Van tres corridas con el patrón y
  una sin él — deja de ser casualidad, pero sigue sin ser ley.
- **Te lo dice Carmen (True Fem) · segundo caso del registro "marca sin oferta".** Párrafos largos de
  salud femenina, cero emoji en el cuerpo, cero precio, cero envío, cero contra entrega. Es el mismo
  registro que Caphero el 21-ago **y el mismo que Tag Recede VIDEO 8**, el mejor anuncio del arsenal
  Golden. **Los tres son verticales con restricciones de claims.** Ya no es un contraejemplo suelto:
  **es una clase.** Cuando el producto no puede prometer, el mercado tampoco promete.

### La regla de los 125: 1 de 4 en el mercado, y el que cumple es el corto

- **Avril CUMPLE**: `¿Por qué estás siempre cansado? / Podría ser falta de magnesio. / El 70% de
  colombianos tiene deficiencia.` = ~103 caracteres. **El argumento de credibilidad entra entero en la
  ventana visible.** Es el único de los cuatro, y es el de registro telegráfico.
- klent.store, Legado Natural: **NO** — la logística va al final del cuerpo.
- Te lo dice Carmen: no aplica, no tiene oferta.

**Y la tesis de la corrida 3 se sostiene:** los que no meten la oferta en los 125 la ponen **en el
título o en la descripción del enlace**, que nunca se cortan. Legado Natural la repite en el título;
Avril la pone en la descripción (`Envío gratis. Paga al recibir.`). **Poner la oferta donde nunca se
trunca sigue siendo mejor solución que forzarla dentro de los primeros 125.**

### Límites oficiales de Meta: SIN CAMBIO, cuarta verificación — pero hay dos citas nuevas

`ads_get_help_article`, artículo **223409425500940**, corrido hoy: **125 / 40 / 25, sin cambio**, y
sigue el consejo *"primary text should span 1-3 lines at most"*. Cuatro corridas con la misma fuente.

Dos hallazgos de fuente que **no estaban en la base** y sí cambian cómo se trabaja:

1. **Meta genera hasta 5 variantes de texto, y SOPORTA ESPAÑOL.** Artículo **180641596861873**:
   *"text variations with and without personas are currently available when primary text inputs are in
   english, portuguese and spanish"*. Es decir, el mecanismo de opciones múltiples que el 5+5+5
   necesita **está disponible en el idioma en que Golden pauta**. Deja de ser una limitación teórica.
2. **La descripción de 25 es para información NO esencial, y lo dice Meta.** Artículo
   **497610041230617**: *"your description should contain only nonessential information"*. Eso cierra
   una duda vieja: no hay que pelear por meter el argumento de venta en 25 caracteres — **no es el
   campo donde va**.

### GOLDEN CP BACK UP

No se tocó ni se leyó (`408753721820872`) — orden del Centro de Mando respetada.

### Qué quedó SIN VERIFICAR

- **`asset_feed_spec`: cuarta corrida sin poder leerlo.** Sigue siendo el hueco más viejo. Se sabe que
  el mecanismo existe, que Meta lo documenta, que aplica a imagen/video único y que **soporta español**
  (nuevo hoy). Lo que falta es una mirada MANUAL en el Administrador de anuncios: la API no lo expone
  y van cuatro corridas intentándolo. **Recomiendo dejar de reintentarlo por API.**
- **El gasto de GOLDEN CP6 (3.171.690 COP) y BLUE CP5 (777,20 USD) es ILEGIBLE** a nivel anuncio y
  campaña. No sé qué copy lo gastó. No es omisión: la API devuelve vacío.
- **El 95% del gasto de BLUE CP1 y el 77% del de GOLDEN CP1** no corresponde a ningún anuncio que la
  API devuelva.
- **Le'côterra CP2 corre 83% catálogo dinámico**, cuerpo no legible. El mejor CPA del conjunto
  (14.676, ROAS 6,03) sigue sin poder auditarse — cuarta corrida.
- **42 de las 58 cuentas barridas no tuvieron gasto** — sin resultado que cruzar, fuera del análisis
  por diseño, no por omisión.
- **El cuerpo de mercado de Latin shop** devolvió vacío. 4 de 5 leídos.
- **No se aisló la variable CTA** en el contraste de otra marca: el video cambia junto con el destino.
- **`INTER CP4 COL` pasó a DISABLED** y salió de las cuentas con gasto. Fuera de mi dominio
  investigarlo; va a la bandeja.

---

## 2026-08-21 · corrida 3 de la tarea automática

> ### 🔴 CORRECCIÓN DEL MISMO DÍA (ampliación de cobertura, escrita horas después)
>
> **Lo que escribí más abajo sobre el copy corto estaba mal, y estaba mal por cherry-picking.**
> Cerré la primera pasada diciendo *"OPEN 7 - V5 Bergamot, 33 caracteres, ROAS 3,62, el más alto
> de esa cuenta"*. Elegí el número que me gustaba, de UNA pieza con **2 compras**, en UNA cuenta.
>
> Al bajar a nivel anuncio las **12 cuentas con gasto que había dejado fuera**, resultó que
> `OPEN 7` (14-ago) y `OPEN 8` (19-ago) **no son una pieza suelta: son una tanda entera de copy
> corto corriendo en 8 cuentas.** Leí 8 creativos distintos de la tanda: 32 a 52 caracteres,
> todos con emoji al inicio y el beneficio en el título (`BERGAMOT 36 es cítrica y fresca 🧊`,
> `NEUTRALIZA el mal olor de raíz y dura 48 horas 💦`, `La segunda te sale en $60.000. 🎁`,
> `3 fragancias, una sola familia Le'côterra 🎁`, `ATHLETIX aguanta hasta después del gimnasio 💪`…).
>
> **Con la muestra completa, el corto PIERDE.** Misma marca, mismos 30 días, top-5 por gasto de
> cada cuenta:
>
> | | Gasto | Compras | CPA |
> |---|---|---|---|
> | **CORTO** (OPEN 7/8, 32-52 car.) | 2.030.367 COP | **37** | **54.875** |
> | **LARGO** (221-332 car.) | 8.635.362 COP | **193** | **44.743** |
>
> **El corto sale 23% más caro**, sobre 37 compras — ya no son 2. En las cuentas en dólares pasa
> lo contrario (corto 9 USD contra largo 13 USD sobre 8 compras), pero son otro mercado y otra
> muestra: **no se pueden sumar y no declaro ganador con 8 compras.**
>
> **Y el hallazgo de verdad no es cuál gana, es la dispersión.** El mismo copy corto, por cuenta:
>
> | Cuenta | Gasto | Compras | CPA |
> |---|---|---|---|
> | INTER CP2 | 51.110 | 3 | **17.037** |
> | GOLDEN CP8 | 492.053 | 16 | 30.753 |
> | BLUE CP2 | 84.348 | 2 | 42.174 |
> | INTER CP4 | 249.674 | 5 | 49.935 |
> | INTER CP5 | 237.741 | 3 | 79.247 |
> | INTER CP1 | 173.184 | 2 | 86.592 |
> | GOLDEN CP1 | 742.257 | 6 | **123.710** |
>
> **Siete veces de diferencia con el mismo texto entre cuentas.** Esa brecha es más grande que
> la brecha corto-vs-largo que se supone que estamos midiendo. **Mientras la varianza entre
> cuentas sea 7x y la diferencia a medir sea 23%, este experimento no puede dar veredicto.**
> Es la misma lección que §6: el texto no es la variable dominante.
>
> **Qué queda en pie del párrafo original:** que el polo corto **sí se ejecutó** — eso era cierto
> y era la novedad. **Qué queda tumbado:** que estuviera funcionando. No lo sé, y con esta
> dispersión no lo puedo saber así.
>
> **Lección de método, para mí mismo en la próxima corrida:** cerré una pasada con un ROAS de una
> pieza de 2 compras porque era el número bonito. **Un indicador sobre 2 compras no se reporta,
> ni siquiera con el descargo de "no es veredicto" al lado.** Se busca la clase entera antes de
> escribir la frase.
>
> **Límite de esta corrección:** es top-5 por gasto de cada cuenta, no el censo de anuncios. Corta
> la cola de las dos poblaciones por igual, pero no es muestra completa.


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
cuerpo de **33 caracteres** — `BERGAMOT 36 es cítrica y fresca 🧊`. Resultado: 84.348 COP, 2 compras, CPA 42.174.
**(Corregido arriba: esta pieza no es el caso, es una tanda de 8 cuentas, y en agregado el corto
pierde por 23%. La frase original que celebraba su ROAS era cherry-picking.)**
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

| Anuncio | Largo | Compras | CPA | Argumento en 125? |
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
