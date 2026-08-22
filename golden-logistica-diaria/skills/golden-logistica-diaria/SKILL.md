---
name: golden-logistica-diaria
description: >
  Golden Group — LA CORRIDA DIARIA DE LOGÍSTICA de una tienda COD. Entra sola a Dropi y a
  Chatea Pro, revisa TODO lo del día y entrega UN informe con semáforos: qué pedido se despacha
  y por cuál transportadora, cuál hay que frenar antes de que salga, a qué cliente llamar por
  novedad y qué decirle, qué dirección está mala y la pregunta exacta para arreglarla, y qué
  conversación de WhatsApp se quedó trabada sin volverse pedido. Decide la transportadora con el
  balance real: precio de todas, efectividad EN ESE MUNICIPIO, y la huella del cliente solo para
  desempatar. Cruza lo que el cliente pidió en el chat contra lo que se cargó en Dropi y frena las
  órdenes que no coinciden. Úsala SIEMPRE que el usuario quiera: la revisión diaria de logística,
  "qué despacho hoy", "revisa los pedidos del día", "qué pedidos freno", "por cuál transportadora
  mando esto", "revisa las novedades", "el informe de logística", "qué chats se quedaron sin
  procesar", o cuando pida automatizar la operación logística de una tienda. Es el ORQUESTADOR:
  llama a golden-despachos para calificar la cola y a golden-logistica para el rescate de
  novedades, y aporta lo que ninguna hace — la auditoría del embudo de Chatea y el informe único.
  NO es para configurar asistentes de Chatea (eso es la familia golden-chatea-pro-*).
---

# Golden Logística Diaria — el director de orquesta del día

**Versión** `GLD1.42` · «flujo operativo cablea la orquestación» · Fábrica: chat «✅ SKILL golden-logistica-diaria»

> **GLD1.42 (2026-08-21, auditoría golden-skill-auditor).** Añade «Flujo operativo · la
> corrida de hoy, paso a paso»: hasta GLD1.41 el `description` prometía ser el
> ORQUESTADOR de `golden-despachos` y `golden-logistica`, y la propia tabla de
> pendientes confesaba «NO CABLEADO — hoy la orquestación es manual». Esa era una
> contradicción real entre lo que dispara la skill y lo que el cuerpo entrega. Se cierra
> en INSTRUCCIÓN (esta skill no tiene runtime propio para invocar otra skill): el nuevo
> flujo numerado dice el paso exacto en que se invoca cada hermana y qué declarar si no
> está disponible. Nada del conocimiento de campo existente se tocó.

> **La versión es UNA y vive aquí.** Llegó a haber tres a la vez — este archivo decía `GLD1.9`,
> el contrato del informe decía `GLD1.4` y lo congelado era `GLD1.12` — porque cada archivo
> llevaba su propio número y nadie los movía juntos. Un número de versión que no se puede
> contrastar no identifica nada. Los demás documentos citan esta, no la suya.

En COD la plata no se pierde en la venta, se pierde entre la venta y la entrega. Esta skill hace
la corrida completa de un día, sola, y entrega **un solo informe** con lo que hay que hacer.

## Genérica desde el día uno

**Nada de esta skill está atado a una tienda.** Todo lo específico es parámetro:

| Parámetro | Qué es | Ejemplo |
| --- | --- | --- |
| `shop_id` | La tienda en Dropi | `{ID_TIENDA}` |
| `user_id` | El usuario dueño de la huella | `{ID_USUARIO}` |
| `flow_ns` | El espacio de Chatea Pro | `f{ID_ESPACIO}` |
| `origen` | Ciudad desde donde despacha la bodega | `{CIUDAD_BODEGA}` |
| `operativas` | Las transportadoras que la bodega SÍ despacha | `{LAS QUE DESPACHE ESA BODEGA}` |
| `margen` | Utilidad bruta sobre el ticket | `0.40` |
| `factor_tienda` | Cuánto entrega esta tienda frente a su municipio | del archivo de calibración |

Dolce Incanto es su primer caso, no su contenido. **Cada tienda mide su propio `factor_tienda`.**

Los ejemplos de arriba van como `{MARCADOR}` a propósito: llevaban quemados los IDs reales de
la casa. Un ejemplo con un ID que existe se copia tal cual — y el día que esta skill la use
otra tienda, ese `shop_id` apunta a la de aquí. **Un ejemplo no debe poder funcionar.**

## Flujo operativo · la corrida de hoy, paso a paso (GLD1.42, cierra el "NO CABLEADO")

**Esto es lo que faltaba para que el ORQUESTADOR que promete el `description` exista de
verdad.** Hasta GLD1.41 esta sección no existía: todo el conocimiento de campo estaba
escrito, pero ningún sitio decía en qué orden correr los scripts ni en qué punto exacto
se invoca a `golden-despachos` y a `golden-logistica`. Un Claude que leyera la skill por
primera vez tenía la teoría completa y ningún runbook. Ejecuta estos pasos en orden;
cada uno declara qué produce y con qué se sigue si falla.

1. **Cosecha de Dropi** (una vez al día). Pide al usuario pegar `scripts/cosecha-dropi.js`
   en la consola del navegador logueado en Dropi y correr `await cosechar([shop_ids])`,
   `await detallar()`, `descargar()`. Resultado: `volcado-<tienda>-<fecha>.json`. Si
   `cosecha_completa` no es `true`, sigue igual pero decláralo (ver «Modo degradado»).
2. **Invoca `golden-despachos`** pasándole la cola de pedidos en `PENDIENTE` y
   `PENDIENTE CONFIRMACION` del volcado. Es la calificación PREVENTIVA (duplicados,
   dirección, huella, veto de bodega) — esta skill no la reimplementa, la reutiliza. Si
   `golden-despachos` no está instalada, decláralo en el informe como «calificación
   preventiva no corrida» y sigue: el motor propio (`decidir_transportadora.py`) cubre
   igual la elección de transportadora, aunque sin el cruce de duplicados.
3. **Barrido de Chatea, incremental**: `barrer_chats.py --contactos c.json --token t.txt
   --salida chats.json [--previo chats-de-ayer.json]`. Con `--previo` reusa lo ya bajado
   (ver «Por qué el barrido es incremental»).
4. **Embudo**: `embudo_chatea.py --contactos c.json --dropi volcado.json --embudo-out
   e.json --chatea-out ch.json --hoy <fecha>`.
5. **Motivos de no compra**: `analizar_conversaciones.py --chats chats.json --contactos
   c.json --dropi volcado.json --salida analisis.json [--contactos-universo lista.json]`.
6. **El motor decide transportadora**: `decidir_transportadora.py --config config.json`
   → `decisiones.json`. Necesita `torre`, `fletes`, `retorno` y `calibracion` de
   `FLETES-DROPI-COLOMBIA` (ver «De dónde salen los datos»).
7. **El informe diario (Parte 2)**: `generar_informe_diario.py --config config.json
   --decisiones decisiones.json --chatea ch.json --embudo e.json --salida dia.md`. Esto
   cruza el chat contra la orden (`cruzar_chat_orden.py`) por dentro.
8. **Si el volcado trae `NOVEDAD`**, invoca `golden-logistica` con esa lista para el plan
   de rescate por guía (mensaje al cliente, respuesta a la transportadora, prioridad). Es
   el lado REACTIVO que esta skill no reimplementa. Sin ella instalada, la sección
   «Novedades» del informe sigue saliendo (con la decisión de transportadora), pero sin
   el plan de rescate mensaje-por-mensaje; decláralo.
9. **El informe 360 (las dos partes)**: `informe_360.py --config config.json --decisiones
   decisiones.json --embudo e.json --analisis analisis.json --acciones dia.md --salida
   informe.md --pdf ~/Desktop/<chat>.pdf --fecha <fecha>`. Corre `verificar_informe.py`
   como paso final automático: si el papel no cuadra con el análisis, no se entrega.
10. **Entrega**: Markdown + PDF (regla dura, ver «Regla de entrega»). El PDF pasa por
    `golden-pdf-check` y su veredicto se imprime; «NO AUDITADO» no es «APROBADO».
11. **Antes de congelar una versión**, corre `auditar_cierre.py`: audita el propio
    reporte de cierre contra el disco, no contra lo que se cree haber hecho.

**Qué hacer si un paso 2 u 8 no se puede correr** (la skill hermana no está instalada, o
el usuario no la tiene activa en esta sesión): el informe SIGUE saliendo — esta skill no
depende de las hermanas para producir su parte del trabajo — pero la sección
correspondiente declara explícitamente que esa calificación no se hizo, con la misma
disciplina de «cero honesto» que rige el resto del informe. Nunca se calla la omisión.

## El orden de decisión, y no se salta ninguno

### Paso 0 · Lo primero del día: las GUÍAS YA GENERADAS

Es la única ventana que se cierra sola, y por eso es el **Paso 1 del informe** (FER, 2026-08-11):
mientras el paquete no salga físicamente de la bodega, una guía mal puesta **todavía se cambia
sola**. En cuanto sale, lo único que queda es llamar a pedir el favor. Un pedido con guía y uno
ya en reparto piden dos cosas distintas del lector, y meterlos en la misma tabla hace que el
primero se lea con la resignación del segundo.

La sección va **antes que nada** —antes de la Parte 1, que es la que más se lee— y **lleva la
plata en juego en el título**: una sección que pide trabajo sin decir cuánto vale se pospone
hasta que deja de servir.

Qué cuenta: **tiene guía** (el campo `guia`, que es el hecho) **y el paquete no se ha movido**
(el estado, que dice si la ventana sigue abierta) **y hace falta hacer algo**. La definición vive
en `comun.guias_por_corregir` y **la usan los dos generadores**, porque al escribirla dos veces
—una por estado y otra por campo— la misma sección del mismo día salió con 13 pedidos en un papel
y 19 en el otro. Las dos cuentas eran ciertas y contaban cosas distintas; para quien lee, eso no
es un matiz: es que uno de los dos documentos miente.

**`GUIA_GENERADA` SÍ EXISTE. Corrección de una afirmación falsa, medida el 2026-08-11.**
Aquí decía «`GUIA_GENERADA` NO existe en el panel de Dropi». Se midió contra dos volcados reales:
en la cuenta de **Golden del 11-ago hay 54 pedidos** en ese estado, de 3.426; en la de **Dolce del
10-ago, cero**. Se midió en la única cuenta donde daba cero y se escribió como ley del sistema —
la clase es **«una afirmación sobre un sistema externo lleva fecha y lleva cuenta, o no es una
afirmación»**. La factura de haberla creído: contra los 132 accionables reales de Golden, la lista
de estados que salía de ella habría conservado 49 y **perdido 83 — $8.516.104 en silencio**,
incluidos los 54 con guía, que son justo los de esta sección.

Por eso el cosechador ya **no** lleva una lista de lo que entra: lleva la lista de lo que está
**cerrado** (entregado, cancelado, rechazado, siniestro y la familia de devolución) y todo lo demás
es accionable. Una lista de lo que sí entra convierte cada estado nuevo en un pedido invisible; la
de lo cerrado es corta, estable, y un estado nuevo cae del lado que se ve. Se prefiere el ruido al
silencio. Comprobado: por negación salen exactos los 78 accionables de Dolce y los 132 de Golden,
más `EN PUNTO DROOP`, que ninguna lista escrita a mano tenía.

### El identificador impreso es el TELÉFONO, nunca el número de pedido (FER, 2026-08-11)

Dropi le cambia el número al pedido cuando se edita. Un informe que pide corregir un pedido y lo
nombra por su número **se invalida a sí mismo en cuanto lo obedeces**: corriges, el número cambia,
y la fila ya no apunta a nada. El teléfono no cambia nunca y además es con lo que se busca tanto
en Dropi como en WhatsApp.

**La razón va IMPRESA en el propio informe**, no solo aquí: sin ella, el primero que eche de menos
la columna la devuelve por comodidad.

### Paso 1 · Precio de TODAS, desde cero

Se cotizan todas las transportadoras que llegan a ese municipio. **Se ignora la que Dropi ya puso:
esa selección es automática y puede estar equivocada o no haberse hecho nunca.** Cada pedido se
vuelve a decidir de cero, todos los días.

Antes de comparar precios manda el **filtro de bodega**: solo las `operativas`. Recomendar una que
la bodega nunca ha despachado es recomendar un rechazo.

**Y quien pidió RECOGER EN PUNTO no entra al cambio por costo.** El principio es de FER
(2026-08-11) y no está en discusión: el punto pertenece a la transportadora, no al pedido, así que
cambiarla **borra el sitio al que mandaron a la clienta**. Un ahorro calculado sobre eso no es un
ahorro, es una devolución. Un criterio económico no puede arbitrar contra un compromiso ya hecho
con la clienta — el motor no sabe que a ella ya le dijeron a dónde ir.

**PERO HAY DOS CAPAS QUE HACEN LO MISMO, Y ESO HAY QUE DECIRLO EN VOZ ALTA**, porque quien lea una
sola creerá que la otra no existe:

| Capa | Dónde | Qué hace | Desde |
| --- | --- | --- | --- |
| **1 · filtro de candidatas** | `decidir_transportadora.py`, en `candidatas()` | si el pedido pide recogida y el config declara `oficina_solo`, **ninguna otra transportadora entra a competir**. También redacta el motivo cuando el resultado es «sin cobertura» | anterior a GLD1.29 |
| **2 · rama explícita** | `decidir_transportadora.py`, en `correr()` | fuerza `DEJAR` con su motivo escrito, avisa cuando un cambio forzado (la bodega no despacha por la actual) va a romper el punto, y **manda el veredicto al informe** | GLD1.29 |

**Quién consume cada estado:** `punto` y `dudoso` activan **las dos capas** — la 1 por el booleano
`oficina`, la 2 por `oficina_modo`. `dirección` no activa ninguna y el pedido va al balance normal.

**LO QUE LA EVIDENCIA SOSTIENE, Y LO QUE NO.** Medido el 2026-08-11 sobre los dos volcados:
**30 de 30 puntos de recogida son de Interrapidísimo**, que es exactamente el `oficina_solo` que
declaran las dos cuentas. Sobre los 78 pedidos de Dolce **las dos capas dan el mismo resultado**;
el único cambio de decisión (Pereira, CAMBIAR → DEJAR) **lo produce el detector, no la capa 2**.

Así que la capa 2 es, hoy, una **guarda de un caso que no se ha observado nunca**: un punto de
recogida de una transportadora distinta de `oficina_solo`, donde la capa 1 no solo no protege sino
que **recomendaría cambiar y rompería el punto**. Eso es un razonamiento, no una medición — y va
escrito como tal. **El caso de Quinchía con los $5.632 no lo reproduje**: en el volcado del 10-ago
ese pedido ya salía `DEJAR` con el detector viejo; el fallo estaba en un script ad-hoc de
operaciones, no en este motor. Se cita como dictado de FER, nunca como medición propia.

**Y una corrección de mi propio argumento**, que es la razón de que esta sección diga esto:
sostuve que retirar la capa 2 dejaría el estado `dudoso` **sin consumidor**, y es falso — la capa 1
lo consume por el booleano `oficina`. Lo que se perdería al retirarla es el motivo escrito, el
aviso del cambio forzado y el veredicto viajando al informe: menos de lo que dije. El arbitraje del
Centro (conservar el código, degradar el texto) se sostiene por sus otras dos razones — el código
está verificado funcionando y **cuando el código es correcto y el texto no, se corrige el texto**—
pero la mía estaba mal y se anota, porque un argumento que decide un arbitraje y luego resulta
falso es justo el que hay que dejar por escrito.

#### Y LA TRAMPA QUE NINGUNA PALABRA DELATA: la dirección de la oficina, escrita pelada

**Mandato de FER, 2026-08-16, nacido de devoluciones reales.** Sus palabras: *«mucha gente se
sabe la dirección de, por ejemplo, Inter Rapidísimo, y solamente pone la dirección… y muchas de
las devoluciones es porque ponían la dirección así, y uno asumía que era la dirección de la casa
y lo mandaba por Envía o por Veloces».*

**Ningún detector de texto puede cazar esto, ni en principio.** No hay palabra que detectar: es
una dirección normal y corriente que resulta ser la de la oficina. El motor la lee como la casa
del cliente, ve que otra transportadora es más barata, y cambia. **El paquete sale a repartir a
la oficina de la competencia y se devuelve** — y en el informe eso salía como un ahorro.

La única forma de cazarlo es **comparar contra la lista real de oficinas**. Por eso existe
`scripts/cosechar-oficinas-inter.js`, que baja de la consulta pública de cobertura de
Interrapidísimo **el país entero** y lo deja en un JSON con su fecha. El cruce vive en
`comun.es_oficina_de_inter` y **manda sobre el detector de palabras**, porque es un hecho
contrastado contra una lista, no una lectura de texto.

**Aplica a TODO el país, no solo a los pueblos** (FER lo amplió expresamente): en Bogotá pasa
igual con quien vive cerca de una oficina.

**Los dos errores no cuestan lo mismo, y por eso el sesgo va escrito:** marcar como oficina una
casa cuesta unos pesos de flete; **no marcarla cuesta el pedido entero**. Así que hay tres
estados — `igual` cambia la transportadora sola, **`parecida` no cambia nada pero sale marcada**
en el informe para que alguien la confirme con el cliente, y `no` sigue su curso. Un «casi» no
se decide solo.

Y la comparación es **tolerante a cómo escribe la gente**: `CRA 7 # 4 - 47`, `Carrera 7 No 4-47`
y `cra 7 4 47` son la misma puerta con tres grafías. El núcleo que se compara lleva la vía y
**tres** números, no dos — con dos, los vecinos de la oficina se volvían la oficina.

**LO QUE ESTE CRUCE NO CUBRE, medido:** la fuente pública lista **una oficina por municipio**, y
en las ciudades grandes es solo la principal (sale rotulada `OF. PRINC`; Bogotá, Medellín,
Barranquilla y Cartagena traen una sola fila cada una). **Quien escriba la dirección de una
sucursal de barrio en una ciudad grande no se detecta.** Se declara aquí y en el propio archivo
para que nadie lea el cero de esas ciudades como «ahí no pasa».

**El detector mira lo que va PEGADO a la palabra, no la palabra.** «oficina» a secas no distingue
`Oficina InterRapidisimo` (punto de recogida) de `oficina 303 Edificio Central` (la dirección de
trabajo de una clienta de Pereira, falso positivo medido). Si al lado está el nombre de una
transportadora, es un punto; si al lado hay un número, un piso o una torre, es donde vive o
trabaja el cliente. El nombre se reconoce **como suena** —«Inter rapidísimo» partido, o
«interrapidicimo» con c— porque 1 de cada 6 direcciones de recogida de Dolce lo traía roto.

Y hay **tres estados, no dos**: `punto`, `dirección` y `dudoso`. Una dirección que dice «reclamar
en oficina» a secas no es ninguna de las dos: es una que nadie ha medido. Devolverla como
«dirección» sería darle permiso al motor para cambiarla, y equivocarse hacia «no cambio» cuesta
el ahorro mientras equivocarse hacia «cambio» cuesta el pedido entero. **Un detector binario
convierte «no lo sé» en un permiso.** Vive en `comun.pide_oficina`, con banco en
`scripts/prueba_oficina.py` — cuyos dos primeros casos son ajenos y de signo contrario.

### Paso 2 · Efectividad EN ESE MUNICIPIO

Municipio, no departamento — y **no porque el departamento esté inflado**, que es lo que decía
esta línea y era falso. Medido con fuente homogénea sobre 443 pares comparables: el municipio
entrega **más** que su departamento en 359 de ellos, con mediana +2,9 puntos.

La razón real es la **granularidad**. La diferencia municipio-departamento va de **−18,9 a +18,2
puntos**: Plato con Envía entrega 61,2% mientras Magdalena promedia 80,2; Fusagasugá con TCC
entrega 96,4% mientras Cundinamarca promedia 78,1. Un promedio departamental esconde ese rango
en las dos direcciones, así que decidir con él es decidir con ruido. Ver
`references/por-que-municipio.md`.

#### La Torre es un insumo AJENO, y puede cambiar de forma cualquier día

**Rotura en producción del 2026-08-16.** La rutina que regenera `TORRE-MUNICIPIOS.json` migró a
la API FENIX y **cambió el contrato de las filas sin avisar y sin versión de esquema**:

| | Fila |
| --- | --- |
| antes | `{"t": "ENVIA", "pct": 81.93, "ent": 38353, "dev": 8457, "dias": 2.82, "flete": …}` |
| ahora | `["ENVIA", 73.83, 149568]` = `[transportadora, pct, n]` |

El motor hacía `{x["t"]: x for x in v}` y murió con `TypeError: list indices must be integers or
slices, not str` **para cualquier tienda** — sin nombrar el archivo, ni la fecha, ni la fila. Lo
parchó la operación en su copia local para poder despachar ese día.

**El arreglo son dos capas, y hacen falta las dos.** `fila_torre()` acepta los dos contratos y
normaliza a `t`, `pct`, `n`; y la carga **valida el esquema y muere hablando** si llega una forma
que no conoce, diciendo archivo, fila de muestra, `generado` y `rango`. Banco:
`scripts/prueba_torre.py`, con las dos formas reales, **seis formas inventadas que tienen que
morir**, y una corrida del motor entero que exige que el mensaje nombre archivo, fila y fecha —
porque el fallo no fue que faltara tolerancia, fue que **el error no decía nada**.

**LA PÉRDIDA SILENCIOSA, que es peor que la caída.** El formato nuevo tampoco trae `dias`, y el
motor lo leía con `round(m.get("dias", 0), 1)`: habría impreso **«0 días de entrega» para toda la
cuenta**, un número inventado con cara de medido. Ahora `dias` ausente es `None` —nunca `0`— y la
corrida avisa cuántas filas vienen sin él. Un insumo que cambia de forma se nota; **uno que
cambia de contenido y deja un cero plausible, no**.

**Y LA TORRE VA IMPRESA EN EL INFORME.** El factor de calibración de Golden pasó de **0,92 a
1,00 en un día sin que nadie tocara un pedido**: solo cambió la ventana de la Torre (ahora
`2026-03-02 → 05-31`, excluyendo junio y julio por inmaduros). Decir «según la Torre» sin decir
**cuál** es pedirle al lector que defienda un número que se mueve solo por debajo. La fecha, el
rango y la nota de ventana viajan pegados a cada decisión y se imprimen en la Parte 2.

### Paso 3 · El balance: costo real

```
costo real = flete + (1 - p) x (costo de devolución + utilidad perdida)
```

`p` sale del porcentaje del municipio corregido por `factor_tienda`. El costo de devolución es el
**medido** por transportadora, no supuesto.

**Si una gana claro, se decide aquí.** En la primera corrida real, 32 de 44 pedidos se resolvieron
en este paso sin tocar la huella.

### Paso 4 · Solo si está apretado, la huella del cliente

Cuando las dos mejores se llevan menos de `$3.000`, entra el historial de **esa persona** con cada
transportadora. Con dos reglas que no se negocian:

**(0) Un porcentaje sin muestra no entra a la comparación.** Antes de mirar precio o
efectividad, una transportadora tiene que tener **≥50 envíos y ≥5% del total del municipio**
en la Torre de 90 días. La Torre daba Envía al "100%" en Leticia con **4 envíos**, y en vivo
esa transportadora ni siquiera cubría; la buena era Interrapidísimo con 1.961. Con este filtro
la Torre sola basta y no hace falta cotizar en vivo pedido por pedido. Se configura con
`min_envios_muni` y `min_cuota_muni`.

**(a) La ausencia de historial NO penaliza.** Un cliente con 10/10 en Coordinadora y nada en Envía
no dice que Envía sea mala para él: lo más probable es que pidió en otra tienda que solo usaba
Coordinadora. **Quien no tiene historial no participa del desempate, pero no pierde por ello.**

**(b) Un buen historial no se abandona por ahorrar.** 5 entregas de 6 es un buen cliente. Solo se
paga más flete si a la otra le ha ido **20 puntos o más** mejor con esa persona, o si a la barata
le ha ido **mal de verdad**, por debajo del 60%.

**(c) Cuando la huella no decide, manda el costo esperado, no el flete pelado.** Irse por el
flete más barato dentro de la banda de empate puede salir más caro si la otra entrega mejor:
en Villamaría era menos flete y más costo real (la cifra exacta cambia con cada corrida: ver `comparar_decisiones.py`). El desempate por precio
devuelve la de menor costo, no la de menor tarifa.

Estas reglas son de FER y existen porque el motor, sin ellas, movía pedidos por diferencias
que no se pueden probar: 5/6 contra 9/9 son estadísticamente indistinguibles.


## EL DETECTOR DE PLANTILLAS · por qué cambió y a quién movió (2026-08-11)

Meta prellena el primer mensaje cuando alguien toca el botón del anuncio. Distinguir eso de lo
que la persona escribió decide **a quién se llama**: al que solo tocó el botón no hay a quién
llamar. Esta skill lo hacía con una regex y **la cambió por medición**, tras una adjudicación
con la implementación de LOGISTICA DOLCE sobre los mismos 743 contactos.

**Las dos implementaciones discrepaban en 13 contactos y las dos estaban flojas, en casos
distintos.** Por frecuencia se cazan los prellenados comunes y se escapan los raros; por forma
se cazan los raros y solo los que alguien enumeró. **Ciegos complementarios: el criterio nuevo
usa los dos** — es plantilla si aparece en ≥3% de los hilos **o** si llega idéntica de ≥3
personas distintas y abre con «¡», signo que casi nadie teclea en WhatsApp.

**El cambio movió 40 contactos de cubo**, medido uno por uno, no por totales:

| Movimiento | Contactos |
| --- | --- |
| escribió una vez → solo el clic | 22 |
| conversó sin ubicación → escribió una vez | 7 |
| escribió una vez → conversó sin ubicación | 6 |
| solo el clic → escribió una vez | 5 |

**Dos lecciones que valen más que el detector:**

**El total idéntico es el escondite perfecto de dos errores que se compensan.** Las dos
implementaciones sumaban 351 en los dos cubos y discrepaban en cuáles. Cuadrar el total fue
justo lo que casi cierra el caso sin mirarlo.

**Un banco escrito por el autor de la regla prueba lo que su autor ya sabía.** El banco de 9
casos de la regex **pasaba entero** y no contenía ninguna de las dos clases que la tumbaron. Su
verde no decía nada sobre lo que a su autor no se le ocurrió. Por eso los 7 casos reales que
fallaron entraron al banco **como casos**, y por eso la adjudicación la hizo alguien de afuera.

## LOS RESPALDOS VAN A RUTA DURABLE

`~/.claude/skill-backups/golden-logistica-diaria-<versión>/`, **no al scratchpad de la sesión**.

Nació de un fallo concreto: la duodécima verificación **no pudo comprobar que la Parte B
siguiera intacta** porque la única copia de la versión anterior vivía en el scratchpad de la
sesión que la congeló, y desde fuera de esa sesión no existe. Un respaldo que solo puede leer
quien lo hizo no es un respaldo — es una nota personal.

La congelación no termina hasta que la copia está en la ruta durable **y su md5 de conjunto
coincide con el que se reportó**. Eso es lo que permite que un tercero verifique "esto no
cambió" sin creerle a nadie.

## BLINDAJE · el ritual, con su trampa

<!-- Esta sección la escribió otro chat del ecosistema el 2026-08-10 por el canal
     equivocado. Se conserva porque el contenido es correcto y su solución es MEJOR
     que la que tenía la fábrica: purgar el __pycache__ a mano es acordarse cada vez;
     la variable de entorno lo evita de raíz. El canal se juzga aparte del contenido.
     Autoría pendiente de confirmar para dar el crédito. -->

```
chflags -R nouchg golden-logistica-diaria
# ... editar ...
find golden-logistica-diaria -name __pycache__ -type d -exec rm -rf {} +
chflags -R uchg golden-logistica-diaria
```

**Purgar el `__pycache__` no es opcional.** Correr los scripts lo regenera, y si se blinda
con él dentro queda un `.pyc` congelado que ya nadie puede borrar ni actualizar. Para
evitarlo del todo: `export PYTHONDONTWRITEBYTECODE=1` antes de correr.

## REFERENCIAS · los módulos que concentran una regla

| Archivo | Qué concentra | Por qué existe |
| --- | --- | --- |
| `scripts/denominador.py` | LA regla del denominador de conversión | vivía en dos scripts y publicaban 10,44% y 6,07% en la misma página |
| `scripts/comun.py` | pintar contactos, miles, pesos, huella, política de PDF, banderas | `tel_de` sobrevivió dos rondas de «ya lo unifiqué» porque nadie contaba las copias |
| `scripts/escritura.py` | escritura atómica y la guarda de insumos | una protección importada en 7 sitios y llamada en 1 costó 5 horas de barrido |
| `scripts/verificar_informe.py` | **verifica el ARCHIVO del informe** contra el JSON, desde el disco | cinco versiones de auto-verificación dentro del generador midieron el intermedio y lo llamaron el entregable |
| `scripts/prueba_verificador.py` | banco del anterior, con 10 casos **ajenos** | un banco escrito por el autor de la regla prueba lo que su autor ya sabía |
| `scripts/auditar_cierre.py` | audita el REPORTE DE CIERRE contra el disco | tres reclamos de «cerrado» no existían en el disco: un reporte también es un conjunto de afirmaciones |
| `scripts/prueba_denominador.py` | banco de los tres anteriores | el módulo que centraliza una regla es MÁS peligroso sin banco que el código duplicado que reemplazó |

## EL CONTRATO DEL ENTREGABLE · qué puede entrar al PDF del cliente

**NADA que sirva solo para verificar.** Ni marcas, ni anclas, ni comentarios HTML, ni IDs
vestidos de código. El documento es del cliente: si algo no le sirve a quien lo lee, no entra.

Nació de un fallo con las dos mitades del mismo error. Puse anclas invisibles
(`<!--v:calientes--> 9`) para poder verificar que cada dato llegaba al papel, declaré «no salen
en el PDF, lo medí hoy»… y **salían las siete, la primera en la página 1 del informe entregado**.
`build_pdf` escapa todo el HTML: en ese motor un comentario no puede ser un comentario, y no es
«algún día», es siempre.

**Y lo que medí fue el markdown.** Corrí un `grep` sobre el `.md` con un rótulo encima que decía
«las anclas NO se ven en el PDF», anuncié la comprobación del PDF y no la hice. El número que
salió significaba lo contrario de lo que concluí. **Un `grep` con un `echo` encima no es una
medición: es una conclusión con decorado de medición.**

De ahí las dos reglas:

- **Si hay que instrumentar, se instrumenta el generador, no el entregable.** Hoy el generador
  parsea el markdown que acaba de emitir y cuenta las filas de cada sección contra el JSON.
- **Una afirmación con fecha nombra el artefacto que se abrió.** La fecha certifica CUÁNDO se
  midió, no QUE se midió: sin el artefacto al lado, la fecha solo consigue que nadie vuelva a
  mirar. Se dice «medido sobre `X.pdf`, 0 apariciones», no «lo medí hoy».

**El gesto de la mañana está permitido y por escrito:** mirar el informe, corregir algo y volver
a generar. El productor rehace lo suyo aunque otro lo haya leído. Lo que sigue bloqueado es leer
un archivo y escribir encima de ÉL, que es el desastre que costó cinco horas de barrido.

## LA RUTA DEL ENTREGABLE · declarada en un solo sitio

**Por defecto, el Escritorio, con el nombre del chat que corre la tienda** — que es donde FER
lo busca. La ruta exacta la arma el generador; no se repite aquí en literal, porque una ruta
escrita en dos sitios envejece en uno solo.

**Condición que hay que decir, porque cambia el resultado:** la app necesita permiso del
sistema para escribir en el Escritorio (TCC de macOS), y ese permiso **se puede cerrar a mitad
de una corrida**. Pasó el 2026-08-11. Cuando está cerrado, el entregable se escribe en
`DROPI-LOGISTICA/salidas/` **y el informe lo dice**: nunca se da por entregado en el Escritorio
algo que no llegó ahí. Es el cero honesto aplicado a la propia entrega.

## LO QUE NO SE VERIFICA · declarado aquí, no en un mensaje

Tres cosas quedan sin arreglar y **es una decisión, no un olvido**. Se escriben aquí porque
la ronda pasada las declaré en un mensaje al Centro y **cero de ellas existía en el disco** —
lo que solo vive en el reporte no existe para quien abre el código.

| Qué falta | Qué pasa hoy | Riesgo |
| --- | --- | --- |
| **`audit_pdf.py` sin `pdfplumber`** | CERRADO *(medido 2026-08-11)* | **Medido en un venv sin la librería: sale con `exit 2`, stdout vacío y el mensaje «Falta dependencia. Instala: pip install pdfplumber» por stderr — nunca con código 0.** Esta fila decía lo contrario y yo declaré haberla corregido sin tocarla: iba mal medida y mal reportada. El generador ya lee `returncode` y escribe **«NO AUDITADO (el auditor falló, salida N)»** en vez de dar por bueno un PDF sin veredicto |
| **La marca de autoría se pone aunque el auditor no haya podido auditar** | DECIDIDO, se mantiene *(2026-08-11)* | `marcar_como_propio()` es incondicional, y así se queda: **la marca es de AUTORÍA, no de calidad** — existe para que la compuerta anti-pisado sepa que ese PDF lo escribió esta skill, y lo escribió, haya o no veredicto. La calidad la declara el papel con «NO AUDITADO». Lo que estaba mal no era el código: era que esto no estuviera escrito en ninguna parte |
| **«Autoría pendiente de confirmar» del comentario BLINDAJE** | ABIERTO *(2026-08-11)* | vive en prosa dentro de `SKILL.md` y **no tenía fila**: es la única que el barrido lista-vs-prosa encontró suelta. Sigue sin confirmarse quién escribió esa sección |
| **La vigilancia de pendientes cuenta, no compara uno a uno** | ABIERTO *(2026-08-11)* | el auditor exige «al menos 8 filas con estado» y **hoy hay muchas más** — el número exacto lo dice el propio auditor al correr, y por eso no se escribe aquí: cuando lo puse (26) envejeció **el mismo día**, porque mis propias ediciones añadieron cuatro filas. **Convertir en prosa cualquier fila que no sea la vigilada deja el conteo por encima del mínimo y nadie cae** (medido por el verificador). Es un límite conocido del conteo, no una cobertura |
| **«Ficha por pedido \| PARCIAL» vive fuera del universo auditado** | ABIERTO *(2026-08-11)* | está en `references/informe-diario.md`, y el auditor **solo parsea `SKILL.md`**: un pendiente que vive en otro archivo no lo vigila nadie. O se extiende el universo, o se mueve la fila |
| **Política de canal de los avisos** | varios avisos salen solo por `stderr` con código 0; `2>/dev/null` los borra | un aviso cierto que nadie ve equivale a no tenerlo |
| **Alcance del detector de `open(`** | no cubre `open (` con espacio, `getattr(builtins,'open')` ni `Path.read_text` | una lectura sin apuntar escapa a la guarda de insumos |

## PENDIENTES DECLARADOS · lo que la descripción promete y todavía no existe

Se escriben aquí, no solo en el chat, porque quien lee la skill no lee el chat.

> **Toda cifra de esta tabla lleva la fecha en que se midió.** Un pendiente con número se
> vuelve mentira solo: el mundo cambia y la fila se queda. Sin fecha no se puede saber si
> hay que volver a medir, y alguien la cita como si fuera de hoy. Ya pasó con las
> transportadoras (decía 3 y 13, eran 2 y 14).

| Prometido | Estado | Qué falta |
| --- | --- | --- |
| Sección **plata parada** (pedidos que fallaron al subir a Dropi) | NO CONSTRUIDA | leer el tablero de error de Chatea |
| Sección **tendencia** contra ayer y la semana | NO CONSTRUIDA | guardar el informe diario para tener serie |
| Cabecera única de "qué quedó ciego hoy" | PARCIAL | cada sección lo declara por separado |
| Llamar a `golden-despachos` y `golden-logistica` | **CUMPLIDA** *(2026-08-21)* | pasos 2 y 8 de «Flujo operativo · la corrida de hoy» instruyen el punto exacto de invocación y qué declarar si la hermana no está disponible. Cablear en INSTRUCCIÓN, no en código: esta skill no tiene runtime propio para invocar otra skill — lo que faltaba era decírselo al Claude que la ejecuta, y ya está dicho |
| **Corrida contra el API VIVO de Dropi** | PENDIENTE | la cadena cosechar → detallar → descargar → motor → informe está probada contra un Dropi **simulado** con la forma real. Lo que queda probado es el contrato entre piezas, **no** la respuesta viva del servidor. Falta una corrida con sesión de Dropi abierta |
| Los 11 municipios añadidos a la Torre el 2026-08-10 | INCOMPLETOS *(medido 2026-08-10)* | les falta el campo `flete` que los 122 originales sí traen; hay que recapturarlos con el mismo método, y necesita sesión viva de Dropi |
| **El barrido no guarda el TIPO de mensaje** | ABIERTO *(medido 2026-08-11)* | el API entrega `msg_type` (`text`, `audio`, `feed`…) y hasta `payload.transcribed_text`, y el barrido guarda solo el texto. Un audio llega como comilla vacía, idéntico a un mensaje borrado. Medido: 58 entrantes vacíos en Dolce, **20 de ellos el último del cliente** — y uno era una nota de voz de hace 8 días en la lista de "responder hoy". Mientras no se capture, un vacío se cuenta como mensaje y la fila lo declara |
| **Dos transportadoras rotuladas como "la bodega no despacha"** | ABIERTO *(medido 2026-08-11)* | medido sobre la corrida del 2026-08-11: **14 pedidos** (COORDINADORA 11, JAMV-DRIVE 3). El criterio tiene TRES estados (vetada / marginal-confirmar / **nunca usada**) y el informe los pinta con uno solo. Una "nunca usada" tiene cero de no-mirado, no un veto — y JAMV-DRIVE tiene 250 pedidos cerrados al 75,2%. *(Este número decía "3 transportadoras y 13 pedidos" y estaba vencido: un pendiente con cifra se vuelve mentira solo, así que la cifra lleva la fecha de su medición.)* |
| **`cruzar()` valida la FORMA de sus argumentos** | NO CONSTRUIDA *(concedida 2026-08-18)* | recibe dos listas y no lo comprueba: si le llegan los contactos como diccionario por teléfono —que es como los tiene medio ecosistema— muere con `AttributeError` dentro de un `max(...)`, lejos de la causa. **Lo pisé yo mismo escribiendo el banco del defecto del universo, media hora después de arreglar esa misma trampa**: si el que acaba de taparla cae en ella, el problema no es el descuido, es que **la firma no se defiende sola**. Se arregla como el universo: normalizar lo que se entiende, morir nombrando el argumento y el archivo con lo que no |
| **Ficha individual por pendiente de confirmación** (paso 4 de FER) | NO CONSTRUIDA *(dictado 2026-08-14)* | FER la pidió con cuatro cosas por pendiente: dirección, transportadora, **coherencia con el chat** (color y cantidad) y **métricas del cliente** («si devuelve mucho, no sale sin anticipo»). Las cuatro piezas ya existen sueltas —`dir_mala`, el motor, `cruzar_chat_orden` y ahora `huella_base`—; lo que falta es la ficha que las junta por pedido en vez de repartirlas en cuatro tablas |
| **El informe en el ORDEN de 8 pasos de FER** | PARCIAL *(dictado 2026-08-14)* | hecho: el Paso 1 va primero y **dentro va ordenado por causa** — las guías con error de oficina («lo primordial»: devolución segura) antes que las de mal balance, con la causa impresa en la primera columna. Falta el resto del orden dictado: direcciones malas al puesto 3, los pendientes al 4, y novedades/oficina/varados agrupados en el 5 como «solo llamar». Es una reestructuración del ensamble, no un ajuste — se hace entera o no se hace |
| **«Días sin moverse» por pedido** | NO SE PUEDE HOY *(medido 2026-08-17)* | lo pidió FER y el valor es claro (un `GUIA_GENERADA` de 20 días no es la misma urgencia que uno de hoy; DOLCE midió uno en INDEMNIZADA con **442 días** quieto). **Pero el volcado no trae `updated_at`** — solo `created`, que es justo el que no sirve: el creado no dice si se movió. Hacen falta DOS pasos: comprobar contra el API vivo que Dropi entrega el campo, y capturarlo en la cosecha. **No se cablea con `created`**: daría un número plausible y falso, que es el `.get(campo, 0)` que ya nos costó una rotura. Va con la ronda de migración a API, que es donde se rediseña la cosecha |
| **Toda corrida imprime la EDAD de cada insumo, no solo su existencia** | NO CONSTRUIDA *(dictado 2026-08-16)* | fecha del insumo (`generado`, `rango` o `mtime`) contra la fecha de la corrida, y un insumo de más de N días se declara **VIEJO en la tabla de cobertura**. Cierra una familia entera que dio **tres casos el mismo día**: la Torre regenerada sin aviso, un caché de tandas reusado de otro día, y un informe fechado el 14 corrido el 16 sobre una base sin refrescar. Las compuertas de hoy preguntan *si el insumo existe*, y los tres existían — **lo que ninguna pregunta es contra qué reloj**. La Parte 2 ya imprime la fecha de la Torre (GLD1.31); falta generalizarlo a todos los insumos y llevarlo a la tabla de cobertura |
| **El listado de oficinas de Interrapidísimo** | **CUMPLIDA** *(2026-08-17)* | `FLETES-DROPI-COLOMBIA/datos/OFICINAS-INTERRAPIDISIMO.json` — **1.377 oficinas, 32 departamentos**. Lo cosechó el chat de fletes por la misma consulta pública; esta fábrica lo había medido por su cuenta en tres corridas y dio **idéntico** (1.377/32/92 páginas). **Dos productores independientes que coinciden ES la verificación cruzada** — recosechar sería repetir, no comprobar. Pasa la compuerta por FORMA (91 páginas de 15 + una de 12). Procedencia y md5 del origen van dentro del archivo; el original no se movió. Se activa poniendo `oficinas_inter` en el config |
| **Compuerta de bodega única por color** (Dolce, con bodega propia) | NO CONSTRUIDA *(dictado 2026-08-11)* | con bodega propia el **color es una restricción PREVIA al balance**, no un dato del pedido: no se parte un pedido entre dos bodegas porque **se pagan dos guías**, así que un color no importado arrastra el pedido entero a la bodega vieja. Hoy el motor cotiza sin mirar de dónde sale la mercancía. Es pariente de **multi-bodega (GLD2.0)** y se resuelve con ella: por eso hoy es fila y no código — construirla suelta sería cablear media regla |
| **¿Los contactos sin teléfono cuentan en el denominador?** | DECISIÓN DE FER, pendiente *(medido 2026-08-11)* | son **94 de 857 (11%)**: llegan por comentario de Facebook e Instagram y el cruce contra Dropi es por teléfono, así que **no pueden aparecer en el numerador ni aunque compren**. Con ellos dentro la conversión sale sesgada a la baja; fuera, deja de ser «de la cuenta» y pasa a ser «de WhatsApp». Es regla de negocio: la skill los declara y no los toca |
| **`opciones_no_producto` se RE-MIDE, no se declara una vez** | DISEÑO VIGENTE *(2026-08-11)* | la bandera tiene **tres** estados: ausente = nadie miró · `[]` = medido, ninguna · lista = filtra. Pero **un `[]` de hace seis meses vuelve a ser un «ausente» disfrazado**: los formularios cambian y la medición envejece sola. Por eso el `[]` va con la fecha y el tamaño de la muestra en el config (Dolce: 81 contactos, 2026-08-11) y **se re-mide cuando cambie el formulario o cada trimestre**. Un «medido» sin cuándo es una afirmación sin fecha, que es lo que esta skill lleva veintitrés rondas prohibiendo |
| **Multi-bodega** | GLD2.0 · diseño mayor aparte *(medido 2026-08-11, corrida de Golden)* | reparto real de ese día: **Suppli Cali 107 · eshoppi Bogotá 9 · La Herramienta Hogar 8 · Bodega Principal Medellín 4 · GoldBox 3 · Punto Barato 1**. Y la vuelta que cambia el modelo: **la tabla de fletes correcta depende de la CIUDAD DE ORIGEN de cada bodega, no de la tienda** — hoy el config toma UNA sola tabla, así que un pedido que sale de Cali se cotiza con los fletes de otro origen. No es un parámetro más: cada bodega tiene su origen, sus fletes y sus transportadoras operativas. LOGISTICA GOLDEN queda disponible para la consulta de diseño cuando llegue esa ronda |
| **Recogida en oficina: falta la regla** | ABIERTO *(medido 2026-08-11, corrida de Golden)* | cuando la dirección dice «oficina de X», lo que manda es **el punto de recogida**, no el costo — hoy la skill marca esos pedidos como SIN COBERTURA. Caso real: pedido {PEDIDO_EJEMPLO_6}, Timaná |
| **Análisis de transportadoras propias** | ABIERTO *(2026-08-11)* | comparar la efectividad **de la tienda** contra la Torre **sobre la misma muestra**, y medir el costo de devolución real por transportadora en vez de tomarlo del config |
| **La cosecha se autodeclara completa** | ABIERTO *(2026-08-11)* | `cosecha_completa: true` lo escribe el propio cosechador: es una autodeclaración, no una comprobación independiente. Falta una compuerta que contraste contra `total_ordenes_cuenta` **antes** de aceptar el volcado |
| **Serie diaria (delta contra ayer)** | ABIERTO *(2026-08-11)* | no hay histórico: cada informe es una foto sin comparación. Requiere guardar el informe de cada día con su fecha |
| **`_CASOS_*` de `analizar_conversaciones.py`: sin evaluar** | ABIERTO *(2026-08-11)* | son listas de literales dentro de un validador, o sea candidatos a la clase «un guardia no puede ser su propio testigo». **La di por no aplicable sin medirla** — que es exactamente lo que esta skill prohíbe. La evaluación está sin hacer, no descartada |
| **`subprocess.run` sin leer `returncode` en dos bancos** | ABIERTO *(2026-08-11)* | `prueba_escritura.py` y `prueba_previo.py` lanzan procesos y no miran con qué código salieron. *(El del verificador dentro de `informe_360.py` sí lo lee, y los dos auditores de PDF también: estos dos son los que quedan.)* Un proceso que falla y no se mira es un banco que aprueba sin haber probado |
| **`~/.golden/patrones-privacidad.txt` es una dependencia externa NO versionada** | ABIERTO *(2026-08-11)* | el `fail-closed` cubre que el archivo **falte**, no que esté **incompleto**: si alguien lo vacía a medias, el auditor da verde sobre una skill sucia. *Mitigación propuesta, no implementada: que el auditor imprima el número de patrones cargados, para que un archivo raquítico se vea a simple vista* |
| **La skill dejó de ser autocontenida** | ABIERTO *(2026-08-11)* | al sacar los patrones de privacidad fuera, la skill pasó a depender de un archivo que **no viaja con ella**. Quien la instale en otra máquina tiene el guardián sin su lista, y el `fail-closed` le impedirá auditar hasta que la cree. Es el precio de que el guardia no lleve encima lo que persigue — pero es un precio, y va escrito, no supuesto |
| **El auditor de cierre comprobaba contra una LISTA escrita a mano** | CERRADO *(2026-08-11)* | su lista tenía 8 entradas y el noveno pendiente nunca entró: dio «8 de 8 CUMPLE» por el punto ciego exacto que ese pendiente describía. **Ahora extrae los pendientes DE LAS FILAS de esta tabla**: el universo sale del artefacto, no de la memoria de quien lo mantiene |
| **Los patrones de privacidad vivían DENTRO del detector** | CERRADO *(2026-08-11)*, con reserva | el guardia llevaba escrito el teléfono real de una clienta y tres nombres propios: **el detector de fugas ERA la fuga**. Y era ciego a sí mismo, porque `\b` delante del número impide que la frontera case en su propio archivo. Ahora los patrones viven en `~/.golden/patrones-privacidad.txt` (fuera de la skill, fail-closed si falta) y el barrido **se incluye a sí mismo**. **Reserva:** teléfonos y nombres se buscan por LISTA de literales, no por formato — un teléfono de otra clienta no lo detecta nadie. El barrido por formato solo cubre los IDs de orden |
| **El informe CORTO no pasa por el verificador del papel** | ABIERTO *(2026-08-11)* | solo el 360 lo ejecuta; el corto se entrega sin contrastar contra nada |
| **`--analisis` es opcional en el 360** | ABIERTO *(2026-08-11)* | sin él se entrega sin verificar **y sin decirlo**: el papel no declara que no se contrastó |
| **«No se entrega» no cubre el `.md`** | ABIERTO *(2026-08-11)* | cuando el verificador falla, el markdown YA está escrito en disco; solo se frena el PDF |
| **`-corrida-de-fabrica` vive solo en la prosa** | ABIERTO *(2026-08-11)* | el nombre que evita colisionar con el entregable del chat de la tienda no lo pone el código: hay que acordarse — la clase de `pisar_pdf` |
| **El chequeo de ámbito de coberturas es flojo** | ABIERTO *(2026-08-11)* | detecta «tiene un ·» en el título; una tabla con un punto medio decorativo pasa como si declarara su ámbito |
| **`DROPI-LOGISTICA/salidas/DECISIONES-DOLCE.json`** | HISTÓRICO, no se pisa *(medido 2026-08-11)* | difiere en **DOS pedidos**, no en uno. Es **anterior al arreglo de `HUELLA_MALA`**: en el {PEDIDO_EJEMPLO_1} ({CLIENTA_A}, Bogotá) dice `VELOCES` por criterio CLARO y el motor de hoy dice `ENVIA` por HUELLA_MALA — Veloces le entregó 3 de 8 (38%) y Envía 54 de 72 (75%); y el **{PEDIDO_EJEMPLO_4}** también cambia. *(Yo declaré «un pedido» mirando la última línea del diff en vez de contarlas: el diff imprime los casos y el que se queda en pantalla es el último.)* **No se regenera desde aquí: ese archivo lo produce el chat de la tienda, y pisar el entregable de otro chat está prohibido.** Queda declarado como foto vieja, con su diferencia medida |


## EL CONTRATO · el informe es 360, en dos partes y en este orden (FER, 2026-08-10)

El informe diario **no es la cola de Dropi**. Es un solo PDF con las dos mitades del negocio:

**Parte 1 · el asistente de WhatsApp.** Todos los contactos de Chatea, el embudo completo,
dónde se quedó cada quien y **por qué no compró**. Y de primera, antes que nada: **la lista de
los que hablaron de último y nadie les contestó** — ahí el que se fue no fue el cliente, fue la
empresa. Esa es la plata más caliente del día.

**Parte 2 · la logística.** Los pedidos, transportadoras, precios, efectividad por municipio,
huella del cliente y la decisión pedido a pedido.

«Acciones primero» sigue mandando **dentro** de cada parte.

### Cómo se leen las conversaciones

`GET /subscriber/chat-messages?user_ns=<ns>&include_bot=1`.

**Sin `include_bot=1` el endpoint devuelve SOLO los mensajes entrantes**, y entonces «el bot
nunca respondió» y «el bot respondió y el cliente se fue» se ven exactamente igual. Esa fue la
razón por la que durante semanas no se pudo responder por qué no compraban. Medido en un hilo
real: 2 mensajes del bot sin el parámetro, **55 con él**. Y el parámetro es `user_ns` — con
`subscriber_id` el API responde 422.

**El motivo de no compra se lee SOLO de lo que escribió el cliente** (`type == "in"`). El bot
menciona precio y envío en todas las conversaciones: buscar «caro» en el hilo completo clasifica
al 100% como objeción de precio.

## REGLA DE ENTREGA · el informe SIEMPRE sale también en PDF (FER, 2026-08-10)

El informe del día **no se entrega solo en Markdown**. Se genera su PDF con `golden-pdf-check`
— el estándar de la casa: motor Playwright, compuerta verbatim y auditoría — y se deja en
`~/Desktop/<NOMBRE DEL CHAT>.pdf`. Aplica a todas las tiendas. El nombre y el archivado están
descritos arriba, en el contrato; **no se repite el formato aquí para que no envejezca en dos
sitios a la vez** — ya pasó con el factor de la tienda y con las cifras del documento municipal.

**Está en el flujo, no solo escrito aquí:** `generar_informe_diario.py --pdf <ruta>` lo produce,
lo audita y **dice el veredicto**. Si el PDF falla o no queda aprobado, lo avisa; no se entrega
un Markdown solo fingiendo que la regla se cumplió.

**Y no pisa lo ajeno.** Esto no es precaución teórica: una corrida de prueba sobrescribió el
informe que otro chat había dejado en su sitio (ver «LA RUTA DEL ENTREGABLE», que es donde
vive esa decisión) y que FER había decidido conservar. Se
restauró desde su Markdown, pero el archivo estuvo perdido un rato.

La política es **una sola para los dos generadores** y vive en `scripts/comun.py`: cuando esta
skill escribe un PDF deja al lado una **marca de autoría**. Si mañana hay un PDF en esa ruta y
**tiene la marca**, es suyo y se archiva en `_archivo/` antes de escribir el nuevo. Si **no
tiene marca**, es de otro y **no se toca**: el generador se niega y lo dice.

*(Aquí decía que se podía forzar con `"pisar_pdf": true` en el config. Esa bandera nunca
existió en el código: estaba documentada, estaba en la lista de claves válidas y no la leía
nadie. Documentar una palanca que no está conectada es peor que no documentarla — quien la
usa cree haber desactivado una protección que sigue puesta, o al revés. Para reemplazar un PDF
ajeno a propósito, se borra a mano.)*

## EL REPARTO · quién hace qué (arbitraje del Centro, 2026-08-10)

**La cosecha es única y la hace esta skill**, una vez al día, a
`DROPI-LOGISTICA/datos/volcado-dolce-<fecha>.json`. Todos los demás **consumen ese archivo**.
Está prohibido volver a bajar las órdenes desde otro chat: dos cosechas son dos verdades que
pueden discrepar sin que nadie lo note, y el que se equivoque despacha un paquete mal.

**Mientras la skill no cierre verificación**, el informe operativo lo emite el chat de API
DROPI con su formato, consumiendo esta cosecha. Esta skill **sí emite informe** — el 360 y el corto — y la frase anterior («no emite informe
paralelo») venció: hoy produce los dos y los deja en `salidas/`. Lo que NO hace es escribir en
el sitio del entregable de otro chat, que era la preocupación real. Con su condición: **la
corrida de fábrica lleva `-corrida-de-fabrica` en el nombre**, precisamente para que no pueda
colisionar con el que produce el chat de la tienda. Dicho así porque
**sí avisa las excepciones sueltas** — una orden que no coincide con el chat no espera al
informe del día siguiente.

## POR QUÉ EL BARRIDO ES INCREMENTAL

No es una comodidad: **es la condición para que la Parte A exista como rutina diaria.**

Medido el 2026-08-10 contra el API de Chatea: **900 contactos a ritmo suave son unas 5 horas**,
casi todas gastadas en reintentos de 429 — a 2 hilos con pausa de 1 segundo no se pasó de 100
contactos en 36 minutos. Y subir los hilos empeora: a 10 hilos se perdieron **503 de 900**.

Un informe que sale **todas las mañanas** no puede depender de un proceso de cinco horas que,
si se corta a la hora cuatro, **se pierde entero**. Con `--previo`, cada tanda que sobrevive
queda ganada y la corrida diaria pasa a ser «lo que cambió desde ayer».

**El archivo declara la mezcla**: cuántas conversaciones vinieron del previo, cuántas se
bajaron frescas y de cuándo es el dato más viejo reusado. Un archivo de dos corridas son dos
fotos, y esa clase ya cobró dos veces en este ecosistema.

**Un previo ilegible mata la corrida con mensaje** en vez de rebarrer entero en silencio, que
costaría horas de 429 que nadie pidió.

## TODO ARCHIVO SE ESCRIBE ATÓMICO

`scripts/escritura.py` es el único sitio donde esta skill escribe. Temporal en el mismo
directorio, `fsync`, y `os.replace` al final — que es atómico: el destino queda como el viejo
entero o como el nuevo entero, **nunca a medias**. Y `exigir_salida_distinta` mata la corrida
si alguien apunta la salida a un archivo que también es insumo.

**El caso que lo originó fue real y la recomendación peligrosa salió de esta fábrica:** el
barrido aceptaba el mismo archivo como `--previo` y como `--salida`. Si el proceso muere
escribiendo, el archivo queda truncado y se lleva por delante la única copia. La compuerta que
detecta «previo corrupto» evita el rebarrido silencioso — que es el **segundo** daño — pero
para cuando habla, el dato ya no está.

**La clase, formulada por el chat LOGISTICA DOLCE al reportarla:** *un banco de pruebas
comprueba qué hace el código cuando TERMINA; nadie comprueba qué queda en disco si NO termina.*
Los cinco bancos de esta skill hacían la primera pregunta. `scripts/prueba_escritura.py` hace
la segunda: mata la escritura a la mitad y verifica que el archivo anterior sigue intacto.

## LAS COMPUERTAS · por qué esta skill se niega a correr

Tres, y las tres nacieron de un informe que mintió sin equivocarse en ningún número.

**1 · La cosecha incompleta no se decide ni se imprime.** El volcado lleva
`cosecha_completa` y `motivo_corte`. Si no dice `true`, el motor sale con error y el
generador del informe **también**, por separado. Una página caída a mitad de cosecha
producía antes un informe que parecía entero.

**2 · El extractor se prueba en el camino que produce el entregable.** `cruzar()` corre su
propia autoprueba en la primera llamada, venga de consola o de un import. Antes la prueba
vivía solo bajo `__main__`: el generador importaba la función, nunca la probaba, y un
extractor roto imprimía "no hay discrepancias" sobre una orden que sí las tenía.

**3 · La compuerta de tienda deja el estado inutilizable.** Si falta una tienda pedida, no
basta con vaciar las órdenes: `descargar()` se niega. Antes seguía vivo y emitía un JSON
válido con cero órdenes, y todo aguas abajo decía "todo en orden" sobre un conjunto vacío.

## LA REGLA · un cero siempre dice de dónde sale

Cada `if not X:` de esta skill responde **dos** preguntas: ¿está vacío porque no hay nada, o
porque no se pudo mirar? Un contador que no las distingue es la misma mentira de siempre,
escrita en código en vez de en prosa.

Ejemplos vivos: el cruce reporta `comparadas` (lo realmente comparado) y no `modificables`
(lo que era candidato); el resumen imprime "no se pudo mirar" donde iría un cero prestado;
la huella del cliente divide entre **pedidos cerrados**, nunca entre el total, porque contar
lo que va en camino como fracaso pinta de rojo a quien apenas empieza.

## Lo demás que se revisa cada día

**El chat contra la orden.** Si el cliente pidió rojo y amarillo y en Dropi entró amarillo y
amarillo, **la orden se frena y se corrige antes de despachar**.

**De dónde sale cada dato, porque no está donde uno esperaría.** La cantidad viene del detalle
por pedido: el listado de Dropi no la trae. Y el color **no** está en `variation.values`, que
viene vacío en el 100% de las líneas, ni se puede sacar del `variation_id`, que no decodifica
— el mismo id aparece con diez colores distintos. El color vive en `notes`, como texto, una
entrada por producto. Solo lo traen unas 28 de cada 63 órdenes modificables; en el resto el
color **no se puede comparar** y el informe lo dice.

**Y hay una tercera respuesta, además de "coincide" y "no coincide".** Cuando los campos que
guarda Chatea se contradicen entre sí — el campo de cantidad dice 2 y el texto del pedido dice
1 — la skill **no dictamina**: levanta la bandera «campos contradictorios» y manda a leer la
conversación, que es el único árbitro. Nació de un caso real: {CLIENTA_B} escribió tres
veces «amor son dos, el negro y como el marroncito». El campo tenía razón, el texto y el valor
de la compra mentían, y en Dropi entró un solo bolso sin el café.

**Las direcciones**, con el estándar por país, y la pregunta exacta para el cliente cuando falta
un dato.

**Las novedades**, priorizadas por valor y por intentos consumidos, con el mensaje listo.

**Los de oficina**, que se pierden en silencio.

**El embudo de Chatea**: los contactos que dieron todos los datos y nunca se volvieron pedido.
Esta capa usa `[General] Payload del Agente` para leer **lo que respondió el bot**, no solo lo que
escribió el cliente.

## De dónde salen los datos

| Dato | Ruta |
| --- | --- |
| Órdenes | `GET api.dropi.co/api/orders/myorders/v2?result_number=500&start=N` |
| Huella del cliente | `GET api-v2.dropi.co/bff/customers/fingerprint/v2?country_code=CO&user_id=<U>&phone=<T>&months=0` |
| Efectividad por municipio | `POST api-v2.dropi.co/logistic/logistic-tower/carrier/get_report_carrier_with_filters` con `state_name` y `city_name` |
| Contactos y chats | `GET chateapro.app/api/subscribers` y `/subscriber/chat-messages` |
| Respuesta del bot | campo `[General] Payload del Agente` del contacto |

Auth de Dropi: JWT de `localStorage`, cabecera `X-Authorization: Bearer`. Se entra por el
navegador del usuario con `scripts/cosecha-dropi.js`.

::: ALTO · el error de los dos navegadores
**Antes de usar cualquier dato de Dropi hay que verificar en qué cuenta se está.** Si el usuario
tiene varios Chrome o varios logins, es fácil traer las órdenes de otra tienda. Ya pasó: se
trajeron 500 órdenes de la cuenta equivocada.

`cosecha-dropi.js` recibe el `shop_id` como argumento, imprime qué tiendas trajo, y **si la pedida
no aparece borra lo cosechado y se detiene**. Esa compuerta no se quita.
:::

## Modo degradado

Si falta un insumo, **la skill corre igual y lo declara**:

| Si falta | Qué se pierde | Qué hace la skill |
| --- | --- | --- |
| Sesión de Dropi | órdenes, huella y novedades | Corre solo la parte de Chatea y lo dice |
| Torre municipal de un destino | la efectividad de esa ciudad | Usa el departamento y lo marca en ese pedido |
| Huella del cliente | el desempate | Decide por costo, sin penalizar a nadie |
| Costo real del producto | precisión del balance | Usa el `margen` parámetro y lo declara como supuesto |

**Nunca un informe que calle lo que no pudo ver.** Pero ojo con dónde se dice: ver abajo.

## Las dos audiencias

**Para FER y el ecosistema:** cobertura completa, N de N, y qué quedó sin verificar.

**Para el equipo del cliente:** hallazgos y decisiones. El alcance se dice **en positivo** ("sobre
los 604 contactos que traen ID de anuncio"), no como carencia. **Sin sección de "lo que no pude
hacer".** El rigor no se pierde, se reubica.

## Reglas duras

- **No ejecuta.** Recomienda; el usuario aprueba. No genera guías, no confirma pedidos, no cancela.
- **Nada le sale a un cliente sin aprobación.** La skill redacta, el usuario manda.
- **Datos reales siempre.** Lo que no se obtuvo se marca; jamás se inventa un flete ni una huella.
- **Un hallazgo contra la configuración no es un bug.** Si el bot dice una cosa y la config otra,
  se pregunta si es diseño o error. La regla de negocio la define el dueño, no un flag.
- **El teléfono manda sobre el ID.** Dropi cambia el ID al editar una orden.
- **Verificar antes de afirmar.** Un resultado que cuadra demasiado, que es absurdo de cara, o que
  acusa un hueco grande en trabajo ajeno, se reproduce a mano antes de reportarse.

## Por qué las versiones anteriores estaban mal

Esta skill nace en su tercera versión. Las dos primeras se tumbaron con evidencia, y el porqué
importa más que la regla:

1. **La primera usaba la Torre por departamento.** No por inflada — se comprobó que no lo está —
   sino por gruesa: promedia la capital con pueblos
   de poco volumen y sobreestimaba la entrega hasta 25 puntos.
2. **La segunda la reemplazó por la efectividad propia del municipio.** Peor: con 3 a 86 envíos,
   los intervalos de confianza pasaban de 20 puntos y decidían sobre ruido.

La tercera usa la **Torre por municipio** —decenas de miles de envíos por ciudad— corregida por un
factor de tienda medido, y deja la huella solo para desempatar. **El motor terminó más simple y
más fuerte: la huella decide 1 de 44, no 13.**

Las tres correcciones vinieron de fuera: dos de FER preguntando, una de un cuestionamiento de
método. **Que dos capas del ecosistema coincidan no es verificación.**

## Encadenado al ecosistema

- **Llama a** `golden-despachos` (calificar la cola antes de la guía) y `golden-logistica`
  (rescate de novedades) — en los pasos 2 y 8 de «Flujo operativo · la corrida de hoy»,
  arriba. No duplica lo que ellas hacen.
- **Comparte datos con** `DROPI-LOGISTICA/datos/` y `FLETES-DROPI-COLOMBIA/datos/`.
- **Entrega a** `golden-ads`: la efectividad real de la tienda es el insumo del breakeven COD.

## Referencias

- `references/por-que-municipio.md` — la evidencia de que el departamento engaña.
- `scripts/prueba_e2e.js` — corre el cosechador real contra un Dropi simulado y comprueba que
  el volcado trae el contrato que consumen el motor y el cruce. Red simulada, contrato probado.
- `scripts/prueba_cosecha.js` — el banco de las compuertas del cosechador.
- `scripts/embudo_chatea.py` — el productor del embudo: clasifica los contactos por tablero y
  detecta las ventas sin orden cruzando por teléfono contra TODAS las órdenes.
- `scripts/barrer_chats.py` — baja el hilo completo de cada contacto, **con `include_bot=1`**,
  captura `ts` y **ordena cronológicamente al guardar**. Con `--previo` es **incremental**:
  reusa lo ya bajado y solo pide lo que falta, aceptando archivos parciales.
- `scripts/prueba_previo.py` — el banco del incremental, con red simulada.
- `scripts/escritura.py` — el único escritor: atómico, y salida ≠ insumo.
- `scripts/prueba_escritura.py` — el banco de la escritura: **qué queda en disco si el
  proceso no termina**.
- `scripts/analizar_conversaciones.py` — por qué no compraron. Su autoprueba corre en el camino
  del entregable, con casos negativos.
- `scripts/informe_360.py` — arma el informe de las dos partes.
- `scripts/comparar_decisiones.py` — compara dos corridas del motor **pedido por pedido**.
  Separa lo que cambia la acción de lo que solo cambia la explicación. Nació de haber afirmado
  "cero cambios" mirando el conteo agregado, que no prueba nada.
- `references/informe-diario.md` — el contrato del entregable, sección por sección.
- `scripts/cosecha-dropi.js` — saca órdenes, el detalle por pedido (cantidad, costo, flete y utilidad) y huellas desde el
  navegador. Recibe una LISTA de `shop_id` y se detiene si alguna no aparece.
- `scripts/decidir_transportadora.py` — el motor. Todo por `--config`, nada quemado.
- `scripts/cruzar_chat_orden.py` — compara lo pedido en el chat contra lo cargado en Dropi.
  Trae autoprueba: si el extractor de cantidad falla contra sus casos conocidos, no corre.
- `scripts/generar_informe_diario.py` — arma el Markdown-Golden del informe.

## La regla que originó la versión 1.1

**Toda frase con veredicto en un entregable generado sale de una VARIABLE, jamás de un literal.**
La versión 1.0 llevaba escrita a mano la frase *"hoy no hay ninguna discrepancia viva"* y era
falsa: el informe se la habría dicho a FER todos los días con una discrepancia viva encima.

De ahí sale la otra mitad de la regla: **si algo no se pudo calcular, se dice que no se pudo.**
Nunca se afirma que no existe. Si falta el volcado de Chatea o las líneas de producto, la
sección 5 imprime que el cruce no se corrió y por qué.
