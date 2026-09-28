# Changelog de golden-presenta

Aquí vive el acta. `SKILL.md` es instrucción; esto es memoria.


## GP2.2 · 2026-09-28 · Ley de versiones: sin letras

El Centro de Mando fijó el 28-sep que toda versión se escribe X.Y.Z, porque el vigilante, el plugin.json y el marketplace solo leen eso. Esta skill numeraba con letras (GP2.1a…GP2.1h), así que la ronda de numeración del 27-sep la dejó en GP2.1i, pero el repo la seguía viendo como 2.1.0, y quien la tenía instalada no se enteraba del cambio. La numeración queda en **GP2.2**. Las actas GP2.1a…h de abajo conservan su número histórico. El contenido de la versión es el mismo que se publicó el 27-sep como GP2.1i: arreglos P59 y la ruta completa de style-recipes. Aplicado por el chat 🧰 ARSENAL Y SKILLS por decisión del Centro de Mando.

## GP2.2 · 2026-09-27 · P59 · lo que se descartaba sin decirlo

Aplicado por el chat 🧰 ARSENAL Y SKILLS por orden directa de FER («que todas las skills estén perfectamente corregidas»), informado al Centro de Mando. No se encontró una sesión viva de esta fábrica. **No se numeró.**

- `scripts/verificar_deck.py`: las frases de más de 300 caracteres salían del chequeo de signos de apertura sin decirlo. Ahora van por `sin_verificar()`, con su conteo y su comienzo. No cambian el veredicto ni la cuenta de chequeos.
- `scripts/abrir_blindaje.sh`: el par ANTES → DESPUÉS no mostraba los archivos BORRADOS, porque el awk solo recorría el DESPUÉS. Y la huella solo miraba `.md`, `.py`, `.js`, `.html` y `.sh`, así que un `.json` o un `.css` cambiado no salía. Ahora se listan los borrados, entra todo archivo (salvo `.DS_Store` y `__pycache__`) y el conteo los suma.
- `SKILL.md:212`: la ruta de las recetas de estilo iba RELATIVA (`references/style-recipes/`) y es de `web-design-engineer`. El validador v1.26, que ya comprueba que la ruta exista en la skill dueña, se la atribuía a golden-cinematica, la skill golden- más cercana en el texto, y daba FALLO. Ahora lleva la ruta completa, como ya la tenía `references/atmosferas.md:63`. Con eso el validador queda sano.
- **Probado sobre copia, 9 de 9:**
  - `autoprueba_deck` sale 0.
  - La frase larga ahora sale en «sin verificar», y el chequeo sigue cazando «Hola?» sin ¿.
  - Con 5 archivos borrados y un `.json` cambiado, la versión anterior decía «**0** artefactos cambiados», y la nueva dice 6 y los nombra.

## GP2.2 · 2026-09-27 · Ley de los requisitos del usuario (aplicó el CENTRO DE MANDO)

Se añadió el bloque «Antes de empezar» del SKILL.md: qué tiene que tener el usuario antes de arrancar, cada requisito marcado BLOQUEANTE o DEGRADABLE y qué pasa si falta (doctrina del CdM del 27-sep). Lo redactó el chat 🧰 ARSENAL Y SKILLS (4 pasadas del golden-verificador adversarial, 0 fallas nuevas en la última) y lo aplicó el CdM sin numerar: el número lo pone la fábrica al ratificar. Solo inserción: 0 líneas quitadas.

## GP2.1h · 2026-09-24 · La página por escenas se delega a golden-cinematica

Fila del Centro de Mando, aplicada por el CdM porque la fábrica no tenía sesión abierta (una fila
nunca se vuelve bloqueo; se avisa a la fábrica). Desde GC1.5, las propuestas que se leen haciendo
scroll por escenas son de `golden-cinematica`. Sin esta línea, el disparador "una propuesta para un
cliente" nunca llegaba allá. Las láminas, el modo presentador y la cámara por el lienzo siguen aquí.
De paso: `golden-finanzas` aparecía como "agente en ~/.claude/agents/", y es skill desde el 19-sep.
Un dato que caduca, corregido.

## GP2.1g · 2026-09-13 · Auditoría golden-skill-auditor: cifra desactualizada en SKILL.md

Hallazgo real de la auditoría periódica: `SKILL.md` seguía diciendo "los ocho tipos de
lámina" en dos sitios (línea del Paso 3 y en la lista de referencias) desde antes de que
`arquitectura-narrativa.md` sumara los 3 tipos visuales (`t-visual`, `t-galeria`,
`t-pantalla`) el 2026-09-03. La referencia ya documentaba correctamente "Los 11 tipos de
lámina: 8 de texto y 3 visuales", pero SKILL.md nunca se actualizó cuando eso pasó — una
inconsistencia de cifra entre archivo instructor y referencia (dimensión Robustez).
Arreglado: las dos menciones de SKILL.md ahora dicen "los 11 tipos de lámina". Sin cambios
de comportamiento ni de estructura. Re-verificado: `inventario.sh` y `validar_arsenal.py`
en verde, autoprueba_deck.py 15/15.

## GP2.1f · 2026-09-05 · El acta que no se consumía

El Centro de Mando corrió mi guardarraíl y le dio pares sin haber abierto: lo
contrario de lo que yo había declarado. Fue a mirar la prueba antes de acusarme
—mi propia ley— y resultó que su corrida no era el caso malo, porque el acta de
mi sesión seguía en `$TMPDIR`.

Pero eso mismo era un defecto MÍO, más grave que el que él buscaba: **el acta no
se borraba al cerrar.** Medido: `--cerrar` se puede repetir indefinidamente y
devuelve SIEMPRE el mismo par, con cara de captura fresca. Una skill que no
cambió nada podía reportar "1 artefacto cambiado" — justo la afirmación que
invalida una nota bajo el mandato.

**Un acta que sobrevive a su cierre es peor que no tenerla: la ausencia se nota,
la rancia no.** Un guardarraíl que promete negarse cuando no abriste deja de
cumplirlo silenciosamente después del primer uso.

Arreglado: el acta SE CONSUME al cerrar (un cierre, un par) y CADUCA a las 12
horas, con negativa explícita en vez de pares dudosos. Probado contra los tres
casos que se saben malos: cerrar dos veces seguidas (se niega, sale 1), cerrar
sin acta (se niega, sale 1), cerrar con un acta envejecida a 20 horas (se niega
y dice por qué, sale 1).

La versión canónica del arsenal (`~/.golden/bin/golden-blindaje`) hereda el fallo,
porque se generalizó desde la mía antes de encontrarlo. Reportado a su dueño con
el parche exacto; este archivo se sustituye por una llamada a ella en cuanto lo
tenga, porque dos recetas compitiendo es el fallo que nombró golden360.

## GP2.1e · 2026-09-05 · Un guardarraíl, no otra regla

Fallé dos veces el mismo día en el mismo archivo: tomé el md5 "antes" de
`autoprueba_deck.py` DESPUÉS de haberlo editado, así que el comando imprimió el
mismo valor a los dos lados. Dos veces el mismo tropiezo no es descuido: es que
el procedimiento pedía memoria en el momento de menos atención.

Escrito `scripts/abrir_blindaje.sh`. Abre el blindaje **y captura el ANTES en el
mismo acto**, antes de la primera escritura. Al cerrar imprime solo los pares que
CAMBIARON, vuelve a blindar, y avisa si no cambió nada: *"cero cambios; si dices
que mejoraste algo, la nota es falsa"*. Si alguien abrió sin él, se NIEGA a dar
los pares en vez de reconstruirlos (sale 1).

La ley: **si un dato depende de que te acuerdes de tomarlo, se pierde; si viaja
pegado al acto que lo hace necesario, no.** Contra un fallo que se repite no sirve
otra regla, sirve mover el momento en que se ejecuta.

Probado contra los dos casos malos que se saben malos: cerrar sin acta previa
(se niega, sale 1) y cerrar sin cambios (avisa).

Re-corrida completa de la batería tras GP2.1d, por la fila de golden-shopify
(estrechar el criterio para matar falsos positivos fabrica falsos negativos):
**13 de 13 en las dos direcciones, con el control en limpio.** El lado malo
entero, no solo el disfraz nuevo.

## GP2.1d · 2026-09-05 · El verde liso miente por omisión

Ley de golden360 vía el Centro de Mando: cuando un chequeo PASA, tiene que
declarar su límite EN LA MISMA LÍNEA del OK. Aplicada a la autoprueba.

Cada comprobación de coherencia dice ahora qué no cubre justo al lado del verde
—por ejemplo, que derivar la lista del motor lee la lista DECLARADA y no
comprueba que cada atmósfera pinte—, y el remate dejó de ser "15 de 15" a secas:
enumera lo que la batería no toca (que el deck se vea bien, que los fondos se
muevan, los 60fps, la veracidad de los datos, y que lo probado son estos casos y
no todo el verificador).

El porqué: "15 de 15 pruebas pasan" se lee como "el verificador está bien", y solo
dice "estos 15 casos salen". Es la forma ejecutable de COBERTURA, no veredicto:
el límite viaja pegado al resultado y no en un párrafo aparte que nadie abre.

## GP2.1c · 2026-09-05 · El caso DISFRAZADO, que es distinto de la prosa

Fila del Centro de Mando: el lado bueno de una prueba no puede ser solo prosa
legítima; tiene que incluir texto escrito con la SINTAXIS EXACTA del dato real
sin serlo. Tenía razón, y mi "9 de 9 en las dos direcciones" del parte anterior
no cubría eso. Probados tres disfraces contra el detector recién reescrito:

- el catálogo de OTRA skill con la sintaxis exacta -> ACUSADO
- un contraejemplo dentro de un bloque de código ("esto NO se escribe") -> ACUSADO
- el catálogo viejo citado en un blockquote -> ACUSADO

**3 de 3 falsos positivos otra vez**, con un detector que ya estaba anclado a
sintaxis. La sintaxis no bastaba: faltaba el ESTADO del texto. Añadido:

- se ignoran los bloques de código cercados (suelen ser contraejemplos, y
  acusarlos castiga justo a quien documenta el error) y las citas en bloque
  (son historia, o el catálogo de otra skill);
- el marcador `Catálogo del motor:` tiene que abrir SU PROPIA LÍNEA. A media
  frase es una mención, no el catálogo.

Batería final: **13 de 13 en las dos direcciones** — 6 de prosa, 3 de disfraz,
4 casos malos (fantasma en el catálogo, `data-atmosfera` inexistente en texto
vivo, atmósfera del motor fuera del catálogo, atmósfera fuera del mapa).

La ley que queda: **un ancla sintáctica sin estado sigue acusando de más.** No
basta preguntar "¿cómo está escrito?"; hay que preguntar "¿esto manda sobre
alguien?". Código cercado y cita en bloque tienen la forma del dato y ninguna
autoridad.

## GP2.1b · 2026-09-05 · El detector que escribí por la mañana estaba mal

Fila del Centro de Mando, ley de esa madrugada: **un detector hecho de patrones
acusa al IDIOMA, no al defecto**, y se prueba en los DOS sentidos: debe MORDER el
caso malo y CALLAR ante el bueno. Probar solo el lado malo deja pasar versiones,
porque muerden y por eso parecen buenas.

Le apliqué la ley al chequeo de coherencia que acababa de escribir. Mordía
`retabla`, así que parecía bueno. Probado en el otro sentido, acusó a
"oro, cian, magenta", a "outfit, gloock, tektur" y a "elegir, calmar, apagar":
**3 de 3 falsos positivos**. Buscaba listas en negrita en cualquier línea que
hablara de atmósferas, es decir, leía prosa.

Reescrito sobre SINTAXIS, no sobre idioma. Dos anclas:
- lo que va entre comillas de un `data-atmosfera="X"`, que solo puede ser un
  nombre de atmósfera;
- los tokens entre acentos graves de la línea marcada `Catálogo del motor:`. El
  ancla es una etiqueta literal, no una posición: coger "el primer párrafo tras
  el título" volvía a acusar a cualquier frase que alguien metiera ahí. Y la
  etiqueta va VISIBLE en el texto, nunca dentro de un comentario HTML, que es
  justo lo que se tragó esta sección entera la vez anterior.

Añadida la cobertura al revés: ninguna atmósfera del motor puede faltar ni en el
mapa de `references/atmosferas.md` ni en el catálogo de `SKILL.md`, así que no se
puede añadir ni quitar una en silencio.

Probado 9 de 9 EN LAS DOS DIRECCIONES: 6 casos buenos que debe dejar pasar y 3
malos que debe cazar (fantasma en el catálogo, `data-atmosfera` inexistente,
atmósfera del motor sin documentar). Autoprueba 13 → 15 casos.

**Y la description: el Centro de Mando decía 1013 y yo 1016. Tenía razón él.**
Mi medidor unía a mano el escalar de bloque de YAML; el parser de verdad da 1013,
11 de margen. Es exactamente la clase que cerré esta mañana para los nombres de
atmósfera — no midas con una copia a mano de lo que hace la fuente — cometida por
mí en el propio instrumento de medida.


## GP2.1 · 2026-09-05 · Lo que estaba escrito y no era verdad

Ciclo de autocalificación. Cinco fallos MEDIDOS, ninguno reportado por un usuario
porque ninguno rompía nada a la vista:

1. **La sección "Atmósferas disponibles" de SKILL.md estaba dentro de un
   comentario HTML.** Un `<!--` del acta del Centro de Mando abría en la línea 17
   y cerraba en la 27, y la sección había quedado sepultada en medio. Es decir: el
   único sitio de SKILL.md que documentaba los fondos llevaba días sin llegar a
   ninguna lectura. Sacada fuera y puesta después del título.

2. **Se documentaba una atmósfera que no existía: `retabla`.** Había quedado un
   `ATM.retabla = null` (dedazo de `reticula`) en `atmosferas.js` y en
   `deck-base.html`, y SKILL.md la listaba como una de "nueve". Quien siguiera la
   documentación al pie de la letra se llevaba un FONDO MUERTO. Son ocho fondos
   vivos más la opción `ninguna`. Líneas muertas borradas.

3. **Por qué nadie lo vio: cada validador tenía SU PROPIA copia de la lista, a
   mano.** `verificar_deck.py` clavaba los nombres en el código. Ahora los DERIVA
   de `Atmosfera.lista` en `assets/atmosferas.js`, que es el motor y por tanto la
   fuente que manda; y si no puede leerla, declara NO VERIFICADO en vez de
   inventarse un respaldo. La autoprueba subió de 10 a 13 casos: los tres nuevos
   comparan la documentación contra el motor. Probados sembrando `retabla` otra
   vez en SKILL.md: la autoprueba cayó a 12 de 13 y nombró al intruso.

4. **Cifras que envejecieron solas.** El motor se citaba como "17 KB" en dos
   sitios y "21 KB" en otro; mide 21.370 bytes. Corregidas y con la orden de
   medirlas al lado.

5. **La única petición de red que quedaba viva.** El deck no traía icono, así que
   todo navegador pedía `/favicon.ico` y dejaba un 404 en la consola de cada
   presentación, en una skill cuya ley es cero red. Icono SVG incrustado como
   data URI, con el acento del deck. Ojo: el hex va como `%23`, porque dentro de
   un data URI la almohadilla abre un fragmento y corta la URL.

**Comprobado en navegador real** (Playwright, no el panel integrado, que congela
las animaciones cuando está oculto): las 8 atmósferas PINTAN y SE MUEVEN, con dos
muestras a tiempos distintos. Las 4 de shader daban "fondo muerto" al medirlas con
`drawImage`, y era artefacto del método: un canvas WebGL sin `preserveDrawingBuffer`
se lee vacío fuera del frame. Repetida la medida con `gl.readPixels` dentro de
`requestAnimationFrame`: las cuatro pintan y se mueven. **Un cero se prueba por
segunda vía antes de creerlo, también cuando el cero es malo.**

Deck de prueba en el navegador: 0 peticiones de red, 10 láminas, 19 acentos
renderizados, sin mojibake, consola sin errores ni avisos.

Además, el historial salió de SKILL.md a este archivo: 301 → 228 líneas, el acta
pasó de ~22% del archivo a un puntero de 4 líneas.


Aquí vive el acta. `SKILL.md` es instrucción; esto es memoria. Se separaron el
2026-09-05 porque el historial ocupaba ~22% de SKILL.md, y porque una de las actas
estaba abierta con `<!--` y sin cerrar antes de tiempo: se había tragado la sección
"Atmósferas disponibles" entera, que llevaba días sin llegar a ninguna lectura.

## Actas al margen que estaban dentro de SKILL.md

```
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1013 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '

## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare · (4) Esta skill estaba SIN BLINDAR: se le puso 'uchg' y se comprobo que el candado muerde. Para editarla: chflags -R nouchg <ruta>, y al cerrar chflags -R uchg · (5) Se le construyo la AUTOPRUEBA que no tenia (scripts/autoprueba_deck.py): su verificador nunca se habia probado contra un caso que se supiera malo.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill GP1.0 · 2026-09-02 · Nace de un encargo de FER: Prezi AI como referencia,
     con la pregunta de si conectarse a su cuenta o replicar el modelo. Medido ese día
     en prezi.com/es/features/ai: su flujo es prompt/archivo -> esquema editable ->
     estilo/paleta, y su foso real son el lienzo con zoom y 160 millones de usuarios,
     no su IA. Decisión: motor propio, porque alquilar el de otro es ser su cliente. -->
```

## Changelog

- **GP2.0** (2026-09-02) — **Fondo vivo.** Veredicto de FER sobre GP1.1: "muy plana, le falta
  dinamismo, movimiento, tecnología, fondo, vida", con la orden de desplegar lo que ya
  sabíamos y quizá no estaba instalado. Añadido:
  (1) **motor de 8 fondos vivos** (`assets/atmosferas.js`, 21 KB medidos) en **WebGL puro y canvas 2D,
  sin Three.js** — decisión medida: la ley de cero dependencias de red, más el hallazgo del
  Centro de Mando de que un fragment shader de ~1 KB aguanta framerate en móvil donde una
  escena Three.js no. Three.js minificado ronda 600 KB y entra por CDN;
  (2) **láminas de cristal** con `backdrop-filter` y filo de luz, para que el fondo se vea
  a través sin comerse el texto;
  (3) **mapa tema → atmósfera → paleta → receta** en `references/atmosferas.md`, que es lo
  que responde al encargo de que cada presentación sea distinta;
  (4) **enganche con `web-design-engineer`**, 26 recetas de estilo que estaban instaladas y
  que ninguna skill de presentaciones nombraba;
  (5) revelado con desenfoque que se resuelve, en vez de solo opacidad.
  Tres fallos hallados ejecutando en Chrome real con Playwright, ninguno visible en el
  script: el título salía como "MBA Comunidad Golden_TARJETAS" porque `GP_TITULO` es
  prefijo de `GP_TITULO_TARJETAS` y se sustituía a medias (arreglado sustituyendo de la
  clave más larga a la más corta, y añadido un check que caza el resto colgando); y en
  móvil las láminas no activas salían borrosas, primero por el `filter` del `.slide` y
  después por el del revelado escalonado, que es del modo lienzo y se colaba al de flujo.

- **GP1.1** (2026-09-02) — Ronda del agente `golden-verificador` (adversarial, 16 corridas
  del script contra archivos fabricados para romperlo, más Chrome headless en 4 anchos).
  Encontró 10 fallas y **la clase que las une: reglas duras de Golden degradadas a aviso, y
  variables calculadas que nunca llegaban a un `check()`**. Corregido:
  (1) el deck entregable no tenía **un solo acento** en `aria-label`, texto visible ni notas
  de presentador, y el script contaba las tildes sin comprobarlas nunca. Ahora hay un check
  que busca palabras que en español siempre llevan tilde, mirando solo lo que ve el usuario
  (texto, atributos accesibles y cadenas del JS), no el CSS ni los comentarios;
  (2) una lámina sin posición se saltaba el check de notas por un `continue`;
  (3) "sin dependencias externas" solo miraba `<script>` y `<link>`, dejaba pasar `<img>`,
  `<iframe>` y `@import`, y excluía Google Fonts a propósito: ahora mira cualquier
  referencia de red y es FALLA;
  (4) el detector de mojibake usaba controles latin-1 en vez de los caracteres cp1252
  reales y se le colaban 2 de 6 variantes, incluida la comilla curva, que es la más común
  al pegar desde Word;
  (5) los signos de apertura y (6) la densidad de 550 caracteres pasan de aviso a FALLA,
  porque la vara decía "no se entrega" y el script daba exit 0;
  (7) SKILL.md mandaba a `motor.md` por los tipos de lámina, que viven en
  `arquitectura-narrativa.md`;
  (8) contradicción de 8 a 14 contra 8 a 12 láminas en propuesta comercial;
  (9) "26 comprobaciones" se presentaba como fijo siendo variable, y el denominador se
  encoge justo cuando el archivo está peor: ahora se explica como señal;
  (10) `golden-finanzas` y `golden-verificador` se citaban como skills siendo agentes.
  Además, este SKILL.md se reescribió con acentuación correcta: tenía una sola tilde en
  todo el archivo, y esa costumbre fue la que arrastró el fallo (1) hasta el entregable.

- **GP1.0** (2026-09-02) — Creación. Encargo de FER a partir de Prezi AI. Motor de cámara
  sobre lienzo, 8 tipos de lámina, modo presentador con notas y cronómetro, vista general,
  deep-link, modo flujo en móvil, salida a PDF y marca parametrizable. Verificador con
  contraste WCAG calculado. Seis fallos detectados y corregidos ejecutando en navegador,
  no razonando: láminas sin colocar en el lienzo, preloader congelado por ralentización de
  temporizadores en segundo plano, cronómetro con el mismo defecto, el arranque pisando la
  navegación del usuario, el modo sin recuperarse al cambiar el tamaño de ventana (caso
  "conectar el proyector") y el HUD apelmazado en 375 px. Además, un fallo del propio
  verificador: contaba como lámina un ejemplo que vivía dentro de un comentario HTML.

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — PRESENTACIONES CINEMATOGRÁFICAS de un solo archivo HTML, con FONDO VIVO (9 atmósferas en WebGL y canvas: nebulosa, aurora, pulso, enjambre, retícula, duna, viaje), láminas de cristal con desenfoque, cámara que viaja por un lienzo (el efecto Prezi), modo presentador con notas y cronómetro, vista general del mapa, salida a PDF y marca parametrizable. CADA PRESENTACIÓN SE VE DISTINTA: la atmósfera, la paleta y la tipografía se eligen por el tema del que se habla. Cero dependencias externas: no hay CDN que se caiga ni suscripción. Trae verificador ejecutable (scripts/verificar_deck.py) que mide contraste real, colisiones de láminas, acentos y densidad de texto, y reporta COBERTURA, nunca "quedó perfecto". Úsala SIEMPRE que el usuario pida: "hazme una presentación", "un deck", "unas diapositivas", "un pitch", "una propuesta para un cliente", "slides para la charla", "algo tipo Prezi", "una presentación que se vea cara", "pasa este documento a presentación", "material para el MBA o la comunidad", "presentación para vender X"; o cuando muestre Prezi, Gamma, Beautiful.ai, Tome o Canva Presentaciones como referencia. Dispara también con "mejora este deck", "esta presentación se ve fea" o si pega un guion, un esquema o un documento y pide convertirlo en presentación. NO usar para: página de producto Shopify COD (golden-shopify), sitio web o landing (golden-web / golden-cinematica), PDF que NO es presentación (golden-pdf-check), ni un .pptx que el cliente deba editar en PowerPoint (skill `pptx`) — aunque esta skill sí decide cuándo derivar a esas.

x

