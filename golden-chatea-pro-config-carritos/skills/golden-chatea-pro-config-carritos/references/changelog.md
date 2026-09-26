# Changelog · golden-chatea-pro-config-carritos

## v3.5 · 2026-09-22 · ruta de la hermana renombrada

`golden-productos-ganadores` pasó a llamarse `golden-dropkiller-productos-ganadores` (orden de FER,
avisada por su fábrica). La skill la citaba para correr `viabilidad_cod.py` antes de encender un
descuento: la ruta apuntaba a una carpeta que ya no existe y el paso habría fallado en el momento
de usarlo. Corregida. El script no cambió de parámetros.

## v3.4 · 2026-09-22 · segunda verificación adversarial: 23 fallas, corregidas las de la skill

El verificador atacó lo nuevo de la v3.3 y encontró que el cruce de catálogo decidía con una
heurística sin declarar sus supuestos. Lo corregido, cada cosa con su prueba:

- **`comparar()` reescrito.** Compara palabras de 3 letras **más los números** (Kit #2 descrito
  como Kit #3 ahora es crítica, antes pasaba), normaliza la clave a texto (un id guardado como
  número salía "producto retirado"), evalúa las entradas que no son diccionario en vez de
  saltárselas, y separa **AVISO de coincidencia débil** de CRÍTICA, medido contra el más corto de
  los dos nombres para no acusar a un nombre corto que calza entero.
- **Catálogo vacío ya no acusa al caché:** excepción propia `CatalogoVacio`. Si TODAS las entradas
  salen huérfanas, el aviso apunta al dominio. Si la paginación llega al tope, lo dice.
- **Autoprueba propia de 5 a 11 casos**, con control negativo, acentos, ids numéricos y dominio muerto.
- **La auditoría dejó de declarar cobertura que no tenía:** el frente de caché solo cuenta si el
  espacio tiene campos de caché (se descubren por prefijo, ya no fijos en #1 y #2), la lectura de
  bot fields avisa si se cortó por paginación, una fecha ilegible ya no mata la corrida y una
  casilla de plantilla vacía es crítica en vez de un salto silencioso.
- **El nombre del asesor dejó de inventar asesores:** la regex pedía mayúscula y nombres compuestos;
  antes "soy más directo" daba un asesor llamado "más". Medido en vivo tras el arreglo: detecta
  Valentina y María, que es una diferencia real entre hermanas, y la reporta como aviso.
- **`motivo_basura`** ya no toma por URL cualquier palabra suelta (`Fijador` se borraba con
  `--escribir`), y detecta "no disponible" en cualquier caja.
- **El guardarraíl de país** caza listas en prosa y en minúscula, no solo en MAYÚSCULA.
- **Privacidad:** fuera los nombres de productos y transportadoras reales de los ejemplos del código.
- **El aviso de margen** quedó explicado: habla del campo entero, no de una casilla, y por eso no
  choca con "el techo no es defecto".
- **Cobertura sin números a mano** en las autopruebas y en el cuerpo.

Quedan declarados como NO verificables desde aquí: los topes del panel (vienen de capturas), que el
panel tenga dos pares de recordatorio, la conexión de Shopify y la prueba con un carrito real.

## v3.3 · 2026-09-22 · la auditoría deja de mirar solo la FORMA del caché

Hueco que yo mismo había declarado al calificarme: "la verdad del caché se lee a mano". Ya no del
todo. Nuevo `scripts/catalogo_tienda.py`: lee el catálogo público de la tienda Shopify
(`/products.json`, sin token ni permisos) y cruza cada entrada del caché por su ID de producto.
Caza dos clases: el producto que ya no existe y el nombre que no coincide con el título real.
Autoprueba propia 5/5, con control negativo y con acentos plegados. La auditoría pasa de 5 a 7
frentes: se suma el cruce con el catálogo y la FRESCURA del caché (hace cuánto no entra un
producto nuevo por el webhook), que es la única señal de que el cable puede estar mudo sin tener
que abandonar un carrito.
Medido en Golden al estrenarlo: 3 entradas de productos retirados que el bot seguía describiendo
(último producto cacheado hacía 43 días). Límite declarado: compara NOMBRE, no la descripción
entera, y solo sirve en Shopify con catálogo público.


## v3.2 · 2026-09-20 · auditoría del arsenal (acta que faltaba)

`scripts/chatea_api.py`, la librería común que importan los otros scripts, no aparecía nombrada en
el cuerpo y el inventario la marcaba como huérfana potencial. Se agregó su línea en SKILL.md. Sin
cambios de comportamiento. El acta vivía solo como comentario HTML en el cuerpo; se baja aquí,
que es donde se guarda la historia.

## v3.1 · 2026-09-18 · la compuerta deja de asumir Shopify (fila del Centro de Mando)

El Reto 360 corre en Tienda Nube. La compuerta decía "comprueba que sea Shopify" y marcaba mal
instalado un espacio de otra plataforma. Ahora se pregunta la plataforma primero: Shopify tiene
sus tres comprobaciones; otra plataforma exige confirmar que Chatea recibe sus carritos (Tienda
Nube: NO VERIFICADO) y, si no, se declara "no aplica todavía", no "mal instalado". El validador
pasa `origen_datos` distinto de Shopify de crítica a aviso (caso 20 reescrito).

## v3.0 · 2026-09-18 · la skill pasa de REDACTORA DE PLANTILLAS a CONFIGURADORA DEL ESPACIO

Hecha en su fábrica, afinando carritos de Golden en vivo con FER. Lo que cambió y por qué:

- **Las plantillas de Meta dejaron de ser el entregable.** FER: "las plantillas no hacen parte de
  la configuración; ya vienen por defecto". La v2.x entregaba plantillas para aprobar y calificaba
  su contenido. Ahora solo se revisa su ESTADO; la redacción bajó a
  `references/plantillas-meta-solo-si-lo-piden.md`.
- **Regla del techo:** cerca del tope pasa; nunca se recorta contenido útil por margen.
- **Medida UTF-16** en el validador (antes `len()`): medido 248 contra 249 del panel.
- **Doctrina de los textos** escrita en el cuerpo y vigilada por el validador: prompts que permiten
  emojis a la IA, signos de apertura, promesas comerciales sin confirmar, nombre del campo repetido
  adentro, agradecimiento que asume contra entrega con anticipado activo. Autoprueba de 11 a 20.
- **Nombre del asesor = uno por espacio** (se lee de los hermanos). **Pago anticipado por
  asistente**, datos solo del dueño, monto por defecto = un flete. Envío gratis y anticipo no chocan.
- **Recordatorios:** el panel tiene DOS pares; `tiempo_recordatorio_3` es llave sin casilla y va vacía
  (la v2.x decía que "el panel acepta tres tiempos").
- **Scripts nuevos, genéricos y probados contra Golden:** `auditar_carritos.py` (5 frentes, solo
  lectura), `escribir_config.py` (solo llaves que cambian, aborta si la tienda no es la esperada,
  relee y compara), `limpiar_cache_productos.py` (caché de la búsqueda web), `chatea_api.py`.
- **Ejemplo completo reescrito** como entrega por campo. Sus propias cifras se midieron: la primera
  versión traía 71/182/98 y medían 55/216/106. La lección que la skill enseña se aplicó a la skill.
- Pruebas: autoprueba 20/20; validador contra la config VIEJA de Golden (caso que se sabe malo)
  → 4 críticas y 8 avisos, todos reales; contra la config actual → 0 críticas; limpiador contra el
  respaldo sucio → 16 entradas basura detectadas, y aborta con tienda equivocada.

### v3.0 · misma fecha · cierre con golden-verificador (16 fallas, corregidas las de la skill)

- Plantillas: la API pagina de 10 en 10 (48 en 5 páginas); `plantillas()` ahora recorre todas.
- Cobertura de la auditoría: ya no imprime "5 de 5" fijo; cuenta lo que de verdad verificó.
- Emojis: la detección es por FRASE; "Máx 2", "con moderación", "1 o 2" ya muerden, y una frase
  negativa en otra parte no perdona a la permisiva.
- Signos de apertura en todos los campos de WhatsApp; promesas ampliadas (garantizado, en N horas,
  mañana, si lo confirmamos hoy, menos de un minuto); anticipado booleano; pago al recibir con más
  formas; origen_datos distinto de Shopify; posicion_imagen vacía; llaves extra;
  tiempo_recordatorio_3 con valor SIEMPRE crítica.
- `u16` UNA sola definición (chatea_api) y probada; `escapado` UNA sola vara (la de limites.json).
- `escribir_config.py` valida el resultado antes de escribir y exige
  `--dueño-confirmo-datos-de-pago` si toca el dato de pago.
- Caché: la forma no dice si es verdad. La auditoría lista cada entrada para leerla a mano;
  `--quitar` para las falsas. Medido: 3 entradas con fecha e id y contenido falso.
- Privacidad: fuera "$15.000", "medido en Golden" y la cifra de clientes del caso de la ley.
- Autoprueba 20 → 34, con sabotaje de u16 que muerde (32 de 34).

## Actas que vivían como comentarios en el cuerpo de la v2.5 (bajadas verbatim el 18-sep)

```
skill v2.5 — 2026-09-13 — auditoría golden-skill-auditor (AUDITA+ARREGLA). UN hallazgo real
con evidencia: `assets/limites.json` (capa_nativa) no traía `nombre_tienda`, pese a que el
SKILL.md documenta su tope de 80 (tabla de techos, sección "Datos de la tienda | Nombre"). El
validador lee ese diccionario para comprobar el TECHO B campo por campo, así que un
`nombre_tienda` de 200 caracteres pasaba `scripts/validar_config.py` SIN crítica ni aviso —
probado con un caso sembrado antes del arreglo. Es la misma clase de fallo silencioso que la
skill existe para atrapar en `transportadoras_disponibles`, solo que en el propio validador.
Arreglado: `nombre_tienda: 80` agregado a `capa_nativa`, y caso 9 nuevo en la autoprueba que
siembra un `nombre_tienda` de 90 y exige que el validador lo cace con el marcador `|CORTE|` —
autoprueba pasa de 10 a 11 casos, actualizado en las dos citas del cuerpo (líneas de la sección
"Antes de escribir"). Resto de la skill: inventario limpio (0 rotas, 0 huérfanos), compuerta
`validar_arsenal.py` en verde, 2 referencias a hermanas verificadas, sintaxis de los 2 scripts
OK, verificador de país en verde.
```

```
skill v2.4 — 2026-09-08 — TUTORIAL OFICIAL de Chatea Pro sobre el nuevo metodo de
integracion Shopify (16:02) cableado como COMPUERTA antes del PASO 0. La skill sabia que los
carritos entran por el webhook de Shopify, pero no decia como se conecta ni como se comprueba:
se podia dejar las 29 llaves perfectas y no recuperar un solo carrito, sin ningun error. Nuevo
references/integracion-shopify-paso-menos-uno.md con el procedimiento en dos mitades y los
cuatro sitios donde se atasca la gente (el primero: shpss_ no es shpat_ y los dos empiezan por
'sh'). Nuevo assets/permisos-shopify-24.txt con los 24 scopes para pegar de golpe.
```

```
skill v2.3 — 2026-09-08 — LE FALTABA EL MOLDE, Y ESO ERA TODO.
Medida contra el campo REAL del espacio de referencia (FER pego el JSON completo): esta skill
nombraba **4 de las 29 llaves**. No estaba mal escrita — lo que hace lo hace bien (las
plantillas de Meta, la ventana de 24 h, la mecanica de reactivacion) — pero se escribio el
06-sep y el mapa de las 29 llaves se levanto el 08. Era anterior al mapa.

LA DIFERENCIA ENTRE LAS CINCO SKILLS DE CONFIGURACION ES UNA SOLA COLUMNA, y se ve al medirlas
todas contra produccion: ventas-wp 24/24 con 3 plantillas · comentarios 15/15 con 2 ·
remarketing 14/14 con 1 · **carritos 4/29 con NINGUNA** · logistico 0/12 con ninguna.
No es calidad de redaccion: es que a dos les falta la pieza.

LO QUE SE AÑADE:
· `assets/template-botfield-configuracion.json` — las 29 llaves con sus marcadores.
· `assets/limites.json` — los DOS techos y el tope de cada casilla, leidos del panel.
· `scripts/validar_config.py` — 11 pruebas, con su CONTROL NEGATIVO (una config limpia tiene
  que pasar en silencio; un validador que acusa siempre no protege, estorba).
· Seccion nueva en el cuerpo con la tabla de las 29 llaves y los tres fallos.

LOS TRES FALLOS QUE AHORA SE ATRAPAN, los tres medidos en un espacio real y los tres SILENCIOSOS:
 1. `transportadoras_disponibles` a **132 con tope 100**. Funciona hoy porque se escribio por
    JSON. El dia que alguien abra el panel y guarde, se corta en el 100 y **el corte cae justo
    antes de "No trabajamos con Servientrega"**. El validador imprime donde caeria el corte.
 2. **Tercer recordatorio con hora y sin plantilla.** El panel acepta 3 tiempos y solo tiene 2
    plantillas: el panel muestra tres avisos y el cliente recibe dos.
 3. **`datos_pago_anticipado` heredado.** Nombre, telefono y medio de pago de quien cobra.
    Clonado, manda el dinero de un cliente a la cuenta de otro. El validador SE NIEGA a pasar
    sin `--dueño-confirmo-datos-de-pago`.

VERIFICADO EJECUTANDO, y con la contraprueba: autoprueba 10/10 · **saboteadas tres piezas EN SU
SITIO** (el tope nativo, el guardarrail del pago y el tercer recordatorio) y en las tres cae
**solo** el caso que las vigila, 9/10 · restaurado y comparado byte a byte contra el respaldo.

🔴 Y UNA TRAMPA PROPIA, cazada en el acto: el primer intento de sabotaje se hizo sobre una COPIA
en el scratchpad y salio sin ninguna FALLA. Parecia "el banco no muerde". **El script ni
siquiera arrancaba**: desde ahi no encontraba sus assets y moria en la linea 31. Un fallo de
arranque disfrazado de veredicto — la misma familia que el resto de trampas de hoy. Se repitio
en su sitio y ahi si mordio. **Antes de creerle a un sabotaje que no muerde, comprobar que el
sabotaje llego a correr.**
```

```
skill v2.3 · 2026-09-06 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): el changelog (15 actas, 16.397 B, 40% del archivo) baja a references/changelog.md — un comentario HTML en el cuerpo se paga en CADA activación; corregidos dos punteros muertos al 'punto 7' de un intake que hoy tiene 4 preguntas; el checklist exigía 4 ángulos cuando el cuerpo prohíbe prometer 4; y references/ejemplo-completo.md, declarado 'vara de calidad', contradecía al cuerpo diciendo 'texto libre'. Historial completo en references/changelog.md.
```


## v2.5 · 2026-09-13 · auditoría golden-skill-auditor (AUDITA+ARREGLA)

UN hallazgo real, evidencia archivo:línea, medido ejecutando (no por lectura):
`assets/limites.json` (sección `capa_nativa`) no traía la llave `nombre_tienda`, pese a que
`SKILL.md` documenta su tope como **80** en la tabla "Techos de caracteres" ("Datos de la tienda
| Nombre | 80"). `scripts/validar_config.py` lee ese diccionario para el TECHO B (campo por
campo): sin la llave, un `nombre_tienda` de 200 caracteres **pasaba sin crítica ni aviso**
—probado antes del arreglo con un caso sembrado, `validar()` devolvía `[]`. Es la misma clase de
fallo silencioso que esta skill existe para atrapar (`transportadoras_disponibles` 132/100), solo
que esta vez vivía en el propio validador.

Arreglo: `nombre_tienda: 80` agregado a `capa_nativa`. Caso 9 nuevo en la autoprueba (siembra
`nombre_tienda` de 90 caracteres, exige el marcador `|CORTE|`) — autoprueba pasa de 10 a 11 casos,
verde 11/11 tras el arreglo. Las dos citas del cuerpo que mencionaban "10 pruebas"/"10 de 10" se
actualizaron a 11. Resto de la skill verificado sano: inventario limpio (0 rotas, 0 huérfanos,
0 dudosos), `validar_arsenal.py` exit 0, 2 referencias a hermanas verificadas
(`golden-chatea-pro-config-logistico`, `golden-productos-ganadores`), sintaxis de los 2 scripts
OK, `verificar_pais_no_es_puerta.sh` en verde.


> **Por qué existe este archivo (Centro de Mando, 2026-09-06).** Estas actas vivían dentro
> del `SKILL.md` como comentarios HTML: **16 bloques, 16.397 bytes, el 40% del archivo** — y
> un comentario HTML dentro del cuerpo **se paga en cada activación** aunque nadie lo lea.
> Las tres hermanas (`config-logistico`, `config-ventas-wp`, `config-comentarios`) ya tenían
> su changelog aquí; esta era la única de las cuatro que no. **El cuerpo se paga siempre, el
> acta solo cuando se consulta.** No se perdió una palabra: bajaron verbatim.

## CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las 

CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 870 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo.

## skill v2.1 · 2026-09-06 (ADENDA a la fila del CdM, con capturas del PANEL VIVO del espacio de F

skill v2.1 · 2026-09-06 (ADENDA a la fila del CdM, con capturas del PANEL VIVO del espacio de FER) · CINCO cosas, y la primera es una CORRECCIÓN DE UN DATO FALSO QUE YO SOSTENÍA: (1) EL PANEL SÍ TIENE maxLength. Mi cuerpo afirmaba en cinco sitios, citando el código de la app, que CartsPage no tenía tope, y llegaba a decir 'no recortes por un número que no existe'. Los contadores se ven en pantalla: 50/2000/2000 en Identidad, 80/200 en Datos de la tienda, 150/300 en Logísticos, 80/500 en Correos. Con mi texto, un correo de 900 caracteres se perdía a la mitad sin aviso. LECCIÓN: lo que se VE en el panel gana a un dato de código leído de segunda mano, y ante duda el default seguro es el que NO trunca. (2) La ley de dos niveles del techo sigue en pie pero ahora tiene DEFAULT: instalación normal respeta los topes del panel; el campo JSON (20.000, o 500.000 en LONG JSON) es solo para el espacio de FER y los VIP — porque lo escrito para el JSON se corta en silencio si quien lo carga usa el formulario. (3) ESTE MÓDULO NO CONFIGURA PRODUCTOS: los carritos entran por el webhook de Shopify del propio panel, así que producto/oferta/precio es un dato que no tiene dónde guardarse; se retira también de la lista de lo que se lee. (4) El País es un DESPLEGABLE y los mensajes se SELECCIONAN de plantillas de Meta ya aprobadas, no se escriben libres — cambia el orden del trabajo: la plantilla se redacta y se aprueba ANTES, en el panel solo se elige. (5) Economía del incentivo con números medidos: un 10% de descuento cuesta hasta $8.467 por pedido generado y el piso es $8.000, así que en un producto de $120.000 el descuento se come el piso entero. Se corre viabilidad_cod.py antes de proponer un porcentaje.

## skill v2.0 · 2026-09-06 (FILA del CENTRO DE MANDO: STACK-GOLDEN/FILAS/2026-09-06-carritos-el-pa

skill v2.0 · 2026-09-06 (FILA del CENTRO DE MANDO: STACK-GOLDEN/FILAS/2026-09-06-carritos-el-pais-deja-de-ser-puerta.md) · Cambio de DOCTRINA, por eso mayor y no parche. TRES cosas: (1) EL PAÍS DEJA DE SER PUERTA — se retira la lista de 10 del cuerpo y el "uno de los 10" del intake. El país sigue preguntándose porque de él dependen jerga, transportadoras y pack de direcciones, pero no tenerlo en lista NO bloquea: se investiga y se configura igual. La cura de un dato que caduca no es vigilarlo, es no depender de él — y esta skill es la prueba: el 05-sep su cuerpo decía 7 cuando eran 10 y rechazaba tres países. Precedente ya aplicado en config-logistico. (2) CUATRO PREGUNTAS RETIRADAS DEL INTAKE (producto/precio, modelo de pago, tiempos de entrega, nombre y tono): el propio texto decía que debían coincidir EXACTO con el asistente de ventas, y lo que tiene que coincidir con algo ya escrito se LEE, no se pregunta — preguntarlo abre justo el riesgo que el texto quería cerrar. Quedan 4 preguntas de 8, todas de dato que solo tiene el dueño. (3) PASO 0 NUEVO, auditar el espacio antes de preguntar: la plataforma instala plantilla de fábrica ya escrita (61 de 61 campos idénticos entre un espacio CO y uno MX; los de Carritos nacen con pais: colombia) y un campo de fábrica no se ve vacío, se ve configurado. Se DELEGA en el detector ya probado de config-logistico (autoprueba 6/6 verificada por mí antes de citarla) en vez de reimplementarlo. Y el verificador de países cambia de oficio: en vez de exigir que la lista esté completa, ahora exige que NO haya lista — defiende la doctrina nueva en vez del dato viejo.

## skill v1.9 · 2026-09-06 (auditoría golden-skill-auditor) · UN hallazgo real con evidencia: `scr

skill v1.9 · 2026-09-06 (auditoría golden-skill-auditor) · UN hallazgo real con evidencia:
     `scripts/verificar_paises.sh` existía y funcionaba (probado: sale 0, "10 de 10 en la línea
     declarante") pero era HUÉRFANO — el único archivo que lo mencionaba era el propio changelog
     de la v1.6, y esta skill ya declara en el script mismo que "un changelog es historia, no
     regla". Sin puntero en el cuerpo vivo, nadie que edite el país volvía a correrlo, que es
     justo el defecto que el script nació a prevenir (la v1.6 rompió 3 países por no probar el
     cambio). Se agrega el puntero en la sección de países y una entrada en el QA. Sin cambio de
     contenido funcional del resto de la skill.

## skill v1.8 · 2026-09-05 (turno del CENTRO DE MANDO: unificación del blindaje) · Esta skill era 

skill v1.8 · 2026-09-05 (turno del CENTRO DE MANDO: unificación del blindaje) · Esta skill era la ÚNICA excepción del arsenal: de 38 skills golden, 31 protegidas y de esas 30 por `chflags uchg` y solo esta por `chmod` puro (medido con `find -perm +0200 ! -flags +uchg`, que es la pregunta operativa; contar solo el bit de modo da falsos positivos porque uchg manda sobre el modo). Pasa a `uchg`, el estándar que declara su dueña golden-blindaje. CÓMO SE LLEGÓ A LA EXCEPCIÓN, que es lo aprovechable: la puesta en norma del 03-sep cambió el mecanismo sin declararlo, y al reparar se aplicó la regla "repón el mecanismo que tenía" — regla razonable que, sobre un cambio no declarado, PROPAGA la excepción en vez de corregirla. Corregida en la gaceta: se repone el ESTÁNDAR, no lo que había, y si difieren se declara al CdM en vez de heredarlo en silencio. Sin cambio de contenido funcional.

## skill v1.7 · 2026-09-05 (mismo ciclo, ronda 2) · El verificador de países de la v1.6 DABA VERDE

skill v1.7 · 2026-09-05 (mismo ciclo, ronda 2) · El verificador de países de la v1.6 DABA VERDE con la lista saboteada, y lo descubrí probándolo contra un caso que sabía malo en vez de darlo por bueno. Dos defectos encadenados, los dos de la misma familia (un CERO se prueba, no se cree): (a) hacía grep sobre el archivo ENTERO, así que los países borrados del cuerpo seguían "presentes" porque el CHANGELOG los nombra — un changelog es historia, no regla; ahora descarta los comentarios HTML y mide solo texto vivo. (b) Ya midiendo solo el cuerpo, quitar UN país de la lista seguía pasando, porque ese país seguía nombrado en la frase del matiz sobre packs de direcciones, dentro de la MISMA línea; la comprobación se ancló a la línea que DECLARA la lista y el matiz se separó a su propia línea, que además se lee mejor. Banco de 3 casos en scratchpad: 'siete' y 'quita_uno' muerden, 'sano' pasa. La v1.6 solo cazaba el sabotaje burdo.

## skill v1.6 · 2026-09-05 (automejora bajo el MANDATO DE AUTOCALIFICACIÓN de FER + fila del CdM) 

skill v1.6 · 2026-09-05 (automejora bajo el MANDATO DE AUTOCALIFICACIÓN de FER + fila del CdM) · DOS defectos de comportamiento, ninguno cosmético: (1) DATO FALSO EN TEXTO VIVO — el cuerpo afirmaba "la plataforma solo acepta 7 países" y listaba 7. Son DIEZ desde el remedido del 2026-08-29: faltaban GUATEMALA, ARGENTINA y BRASIL. Verificado por mí en la fuente dura (assets/limites.json de golden-chatea-pro-config-ventas-wp), no de oídas. Con el texto viejo esta skill RECHAZABA tres países que la plataforma sí acepta. Se añade el matiz que el JSON declara y la prosa perdía: Argentina y Brasil no tienen pack de direcciones, así que ahí los datos se preguntan al negocio. Barrido de gemelos hecho: una sola ocurrencia, sin hermano; esta skill no tiene código ni JSON, así que el texto ES el dato y por eso se comprueba con scripts/verificar_paises.sh. (2) VÍA DEL USUARIO ausente — la entrega se consume por dos puertas con topes distintos (formulario del panel CartsPage, sin maxLength; bot field/API, 20.000 escapados o 500.000 en LONG JSON) y la skill no preguntaba por cuál entra. Aplicar siempre el tope de API recorta sin motivo al que pega en el panel; no aplicarlo nunca parte en silencio al que escribe por API. La vía pasa a ser entrada OBLIGATORIA del intake (punto 0) y chequeo del QA.

## skill v1.5.1 · 2026-08-26 (turno concedido por el CENTRO DE MANDO, LEY DEL CAMBIO ÚNICO de FER 

skill v1.5.1 · 2026-08-26 (turno concedido por el CENTRO DE MANDO, LEY DEL CAMBIO ÚNICO de FER 2026-08-25) · alcance de UNA línea: se estampa la FÁBRICA en el propio SKILL.md. Motivo medido: REGISTRO-FABRICAS.md resolvía esta skill a "CENTRO DE MANDO (por ley: sin fábrica declarada)" porque `grep Fábrica` daba 0, mientras la memoria afirmaba que la fábrica era su chat — memoria y registro se contradecían, y con eso dos manos podían creerse dueñas a la vez (clase FILAS ABIERTAS: la memoria es buen índice, mal candado). El CdM arbitró a favor de la memoria (v1.1 y v1.5 salieron de ese chat) y concedió turno para sellarlo. Sin cambio de contenido funcional. Rige además la LEY DEL NÚMERO DE VERSIÓN: solo la fábrica numera, el resto entrega fila.

## skill v1.5 · 2026-08-23 (auditoría golden-skill-auditor 878 PLATA→ORO, corrida fresca) · CUATRO

skill v1.5 · 2026-08-23 (auditoría golden-skill-auditor 878 PLATA→ORO, corrida fresca) · CUATRO hallazgos con evidencia: (1) CONTRADICCIÓN DE TECHOS — la mecánica decía "Instrucción especial ≤1000 caracteres" mientras la sección de techos afirma, confirmado del código, que CartsPage NO tiene maxLength; quien seguía el ≤1000 recortaba mensajes sin necesidad. El ≤1000 queda marcado como supuesto heredado de prompt-ventas, no como límite del módulo. (2) ESTRUCTURA — las 52 líneas de la LEY de no heredar datos se cargaban en CADA invocación y empujaban hasta la línea 68 la explicación de qué hace la skill; la ley se movió verbatim a references/ley-datos-entre-espacios.md con puntero de cuándo leerla (aplica solo al clonar entre espacios). (3) QA CIEGO AL FALLO MÁS CARO — el checklist no verificaba el largo ESCAPADO ni el releer tras escribir, pese a que la propia skill documenta que pasarse devuelve 200 ok y mata el asistente en silencio; ambos entran al checklist y a la definición de terminado. (4) los ejemplos escribían preguntas sin ningún signo, contra la regla propia de "solo el de cierre". Además: conexión al Centro de Mando declarada (estándar 9).

## skill v1.4 · 2026-08-21 (auditoría golden-skill-auditor 934→ORO): hallazgo real — el paso "Reso

skill v1.4 · 2026-08-21 (auditoría golden-skill-auditor 934→ORO): hallazgo real — el paso "Resolver la objeción" recomendaba prueba social pero el intake nunca pedía ese dato, y el ejemplo de vara de calidad traía una cifra inventada ("Más de 12.000 clientas") sin marcarla como dato real requerido; eso fosilizaba la fabricación de una cifra de negocio, justo lo que la LEY de arriba prohíbe entre espacios y el estándar Golden "datos reales antes de generar" prohíbe siempre. Se añadió el punto 7 al intake (prueba social real, opcional), la regla explícita de nunca inventar cifras de negocio, el chequeo en el QA, y se corrigió el ejemplo para dejar la cifra marcada como dato real del intake, no como técnica libre.

## adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): completada la ley de DOS NIVELE

adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): completada la ley de DOS NIVELES del techo — el tope de 20.000 escapados aplica al bot field tipo JSON legacy; un campo creado o convertido a LONG JSON aguanta hasta 500.000 (medido y validado en las hermanas config-comentarios v1.4.1 y config-ventas-wp v3.0). La cifra de esta skill era incompleta, no falsa: sin la mención a LONG JSON, quien la siga se autolimita.

## skill v1.3.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª cate

skill v1.3.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio).

## skill v1.3 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "

skill v1.3 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta.

## skill v1.2 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTE

skill v1.2 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat de configuración de un espacio de México): confirmado desde el código de la app que el módulo Carritos (CartsPage) NO tiene topes nativos salvo los campos de correo — cierra parte del pendiente "verificar en vivo"; añadido el techo del bot field (20.000 ESCAPADOS ~ 17.000 crudos, corte silencioso con 200 ok); países limitados a los 7 que acepta la plataforma; higiene al clonar ([Carritos IA] Información de productos #N no se hereda) y regla de escribir y RELEER.

## skill v1.1 · auditada con golden-skill-auditor 893→ORO: corregida la regla real de la ventana d

skill v1.1 · auditada con golden-skill-auditor 893→ORO: corregida la regla real de la ventana de 24h (contacto frío = plantilla en el primer toque), etiquetas unificadas (REACTIVACIÓN N), paso de QA + checklist de "terminado", modelo de plataforma marcado "verificar en vivo", changelog añadido


## v2.3 · 2026-09-06 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

Cinco defectos. Ninguno lo veía un validador: los cuatro primeros son **contradicciones internas**
—el documento peleándose consigo mismo— y el quinto es un archivo que se copia sin releerse.

### 1 · El 40% del SKILL.md era changelog que se pagaba en cada activación

16 bloques de comentario HTML, **16.397 bytes de 40.646**. Un comentario HTML dentro del cuerpo
**se carga en cada activación aunque nadie lo lea**. Las tres hermanas ya tenían su
`references/changelog.md`; esta era la única de las cuatro que no. Bajaron **verbatim**, sin perder
una palabra. SKILL.md: 40.646 → **25.608 bytes, 36% menos**.

### 2 · Dos punteros muertos dentro del propio documento

Las reglas de oro y el QA remitían a *"el intake (punto 7)"* para la prueba social. **El intake
bajó de 8 preguntas a 4 en la v2.0** y ese dato pasó a ser el punto 3; los dos punteros se quedaron
apuntando a un punto que ya no existe. Quien siguiera el QA iba a buscar un punto 7 y no lo
encontraba.

### 3 · El checklist exigía cuatro pasos que el cuerpo prohíbe prometer

La v2.2 declaró, con toda razón, que **cuántos pares (tiempo, plantilla) admite el módulo es
DESCONOCIDO** —la captura corta debajo de "Recordatorio 1"— y escribió *"no prometas una secuencia
de 4 pasos sin haber visto que caben 4"*. Pero el checklist seguía pidiendo **"4 ángulos distintos"**
y la definición de terminado seguía siendo **"los 4 bloques copy-paste"**.

**El checklist es lo que se ejecuta al cerrar.** Si él exige cuatro, la prohibición del cuerpo no
sirve de nada: la corrida entrega cuatro igual y el fallo aparece recién frente al panel.

### 4 · Ruta relativa en el QA

`bash scripts/verificar_pais_no_es_puerta.sh` solo corre si por casualidad estás dentro de la
carpeta de la skill. Puesta absoluta, con el porqué.

### 5 · 🔴 La "vara de calidad" contradecía al cuerpo, y la vara es lo que se copia

`references/ejemplo-completo.md` está declarado en el SKILL.md como **"vara de calidad de la
salida"**. Contradecía al cuerpo en lo esencial, en siete puntos:

· Entregaba las reactivaciones **2 y 3 como texto libre** (*"si el cliente ya respondió va como
  texto libre"*), en un módulo donde lo observado es que **todo se selecciona de plantillas
  aprobadas y no hay campo de texto libre**.
· Traía un **"Campo Instrucción especial"** que no existe en el panel observado.
· La tabla de resumen repetía *"Texto libre si respondió"* en dos filas.
· No mencionaba la **Posición de la imagen**, que es un campo real del bloque 1 y cuya elección
  equivocada (posición vacía o GIF) **rompe el envío** — la interfaz lo avisa.
· No decía que las plantillas se **crean y aprueban ANTES** y luego se recargan.
· Entregaba cuatro pasos como si estuviera confirmado que caben cuatro.
· Sus etiquetas seguían siendo `REACTIVACIÓN N` "hasta verificar los nombres reales", cuando los
  nombres reales ya se conocen (`Mensajes de recuperación`, `Tiempo recordatorio N` +
  `Recordatorio N`).

**Un ejemplo desactualizado hace más daño que ninguno**, porque nadie lo revisa: se copia. Con el
texto viejo, la corrida producía una entrega que el panel no puede recibir, y el fallo aparecía
recién al ir a configurar. Reescrito completo contra lo observado, con las casillas reales, el aviso
del GIF, el orden "plantilla primero" y la advertencia de que las filas 2 a 4 **asumen** tres pares
sin que esté confirmado.

### Y la `description`

Decía *"las plantillas de Meta que la ventana de 24 h exige"*, que sugiere condicional. Aquí las
exige **siempre**, no solo fuera de la ventana. Corregida.

### Reserva que sigue abierta

**Cuántos recordatorios admite el módulo.** La cierra una captura de "Mensajes de recuperación"
desplegada hasta abajo. Hasta entonces, la skill configura los que el panel ofrezca y lo declara.


## 2026-09-06 · barrido de publicación: un NOMBRE DE CLIENTE llevaba 16 días en el cuerpo

El acta de la v1.2 (2026-08-07) citaba el chat de origen por su nombre, y ese nombre era **el de un
cliente**. Vivía dentro del `SKILL.md` como comentario HTML desde el **2026-08-21**.

**Por qué nadie lo vio:** un comentario HTML no se lee al revisar la skill, pero **sí viaja al repo,
que es PÚBLICO**. La compuerta `golden-barrido-publicacion` sí lo mira ("árbol entero, comentarios
HTML incluidos") — y no había corrido sobre esta skill. Se destapó al mover el changelog a este
archivo y correr la compuerta como parte del cierre de auditoría.

**Lo aprovechable:** mover las actas fuera del cuerpo no creó el problema, **lo hizo visible**. Un
dato escondido en un comentario está igual de publicado que uno a la vista, y encima nadie lo
audita. La compuerta se corre **antes de cerrar cualquier skill**, no solo antes de publicar.

Sustituido por una referencia neutra. **El nombre no vuelve** aunque se cite el acta.

## 2026-09-07 · CUPO DE LA API repartido a toda la familia (orden de FER)

**Dato de FER vía el desarrollador de Chatea, verificado contra la API viva:** el límite es
**1.000 peticiones por HORA**, pasarse **bloquea una hora entera**, y la respuesta trae el contador:

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: <las que quedan>

En inglés **X-RateLimit-Limit** y **X-RateLimit-Remaining**. **Se repone cada hora.**

🔴 **La trampa está en el CUÁNDO, no en el cuánto.** No viene `x-ratelimit-reset`: el servidor no
dice a qué minuto empezó la ventana. Observado por nuestro lado: dentro de la misma hora el
contador **solo baja** — no gotea crédito, se repone de golpe. Por eso, si te bloqueas, se espera
una **hora completa** desde ese momento y se comprueba **mirando** el contador
(`golden-chatea-cupo`, 1 petición), nunca calculándolo.

**Hasta hoy ninguna de las diez skills leía ese contador.** Se trabajaba a ciegas y el bloqueo
aparecía a mitad de la operación.

**Reparto, y cada bloque está escrito para SU skill** —lo que cambia entre ellas es cuánto cuesta
y qué se rompe si el cupo se agota a mitad; un bloque idéntico en diez sitios sería ruido:

· **Con CÓDIGO** (leen el contador de cada respuesta, avisan y no reintentan ante un 429):
  `chatea-auditoria` (comprueba antes de arrancar sus 137 peticiones y se niega si no caben),
  `chatea-operacion` (cuenta lo gastado; su coste **no es constante**),
  `config-logistico` (el PASO 0 de las cuatro hijas y el orquestador),
  `config-ventas-wp` (**el que escribe**, donde un 429 a mitad deja la config a medias).
· **Con DOCTRINA en el cuerpo** (producen texto o JSON que otro escribe por API):
  `config-carritos`, `config-comentarios`, `full-configuracion`, `producto-comentarios`,
  `prompt-ventas`, `validacion-direcciones`.

**Cobertura: 10 de 10.** Herramienta de casa: `golden-chatea-cupo [token] [--necesito N]`.
