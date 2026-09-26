# Historial de golden-chatea-pro-config-logistico

<!-- skill v1.8 · 2026-09-06 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): cuatro sabotajes tumbaron a auditar_espacio.py — decía "OK el país coincide" sin haber comparado nada, reportaba 3 de 61 campos como universo entero, reventaba con KeyError ante un registro sin nombre y agotaba el tope de páginas en silencio. Reparado y con el cruce ampliado a las señales del texto de 6 países. Autoprueba 6 → 12. Acta: references/changelog.md. -->

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- Fábrica: CENTRO DE MANDO (chat 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR) — sin fábrica de chat propia; turnos y filas van a la bandeja del CdM. -->

<!-- corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto. -->

<!-- skill v1.6 · 2026-08-26 (CdM, edición de familia por la LLAVE DEL INTAKE respondida por FER) ·
PASO 0 vuelve a UNA PREGUNTA A LA VEZ: la v1.5 lo había pasado a "intake único en un solo turno"
siguiendo estandares-golden §3, pero FER resolvió hoy la contradicción en la fábrica de
prompt-ventas ("mejor uno por uno, porque en bloque se abruma la gente") y la nota de gobierno del
barrido pre-comprometía revertir esta skill JUNTO con prompt-ventas (mismo criterio de reversion, sin fijar version — una cita con numero caduca sola:
bloque solo si el interlocutor pega varios datos o lo pide). Lo que se conserva del §3: el
conjunto se releva AL INICIO y nada ya dado se re-pregunta. Fila entregada a la fábrica del
auditor para alinear el §3 y que el próximo barrido no lo devuelva al formulario. -->

<!-- skill v1.5 · 2026-08-24 (barrido total del arsenal, CdM): el PASO 0 decía "pregunta 1 a la vez" — goteo que contradice la ley de autonomía Golden (estandares-golden §3: los datos que solo el dueño tiene se piden UNA vez, al inicio, nunca goteados; cada repregunta es una fuga de turnos). Ahora el intake se pide completo en un solo turno. Los 6 datos, los techos (incl. adenda LONG JSON de dos niveles), gotchas de API, la LEY de no heredar datos y el resto quedan intactos. -->

<!-- skill v1.4 · 2026-08-23 (Estándar 9 — Conexión con el Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v1.3 · 2026-08-21 (auditoría golden-skill-auditor) — description con más sinónimos/frases reales de disparo y desambiguación explícita de la hija (se activa sola, no hace falta llamarla aparte); PASO 1 con manejo de error si la hija golden-chatea-pro-validacion-direcciones no está instalada o no tiene el pack del país (nunca inventar el prompt a mano, declarar pendiente con motivo); PASO 2 con checklist explícito de "terminado" (país, transportadoras, tiempos, prompt de la hija, escribir-releer si aplica, barrido si el origen fue una cuenta guía). -->

<!-- skill v1.2.1 · 2026-08-08 (centro de mando, chat CHATEA otra empresa del grupo COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->

<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): completada la ley de DOS NIVELES del techo — el tope de 20.000 escapados aplica al bot field tipo JSON legacy; un campo creado o convertido a LONG JSON aguanta hasta 500.000 (medido y validado en las hermanas config-comentarios v1.4.1 y config-ventas-wp v3.0). La cifra de esta skill era incompleta, no falsa: sin la mención a LONG JSON, quien la siga se autolimita. -->

<!-- skill v1.2 · 2026-08-08 (centro de mando, chat CHATEA otra empresa del grupo COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → otra empresa del grupo Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA otra empresa del grupo COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->

<!-- skill v1.1 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat configuración de un espacio de México): países corregidos a los 7 que acepta la plataforma (sale Guatemala, entran Panamá/Perú/Paraguay); sección de techos (logístico SIN tope nativo — manda el bot field: 20.000 ESCAPADOS, ~17.000 crudos); gotchas de API (PUT usa `data`, POST usa `var_type`+`value`, GET pagina, trigger sin emojis, tipos por llave, escribir y RELEER); higiene al clonar (los ganchos de venta del logístico fugan nombres de producto y paquetería de la cuenta origen). -->

<!-- v1.0 · sin sello previo -->
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 944 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->


## 2026-09-06 · La puerta de países se retira entera (mandato de FER)

**Qué estaba mal.** El cuerpo decía *"la plataforma acepta 10 países"* y a continuación
enumeraba solo siete, cerrando con una prohibición explícita de tres de ellos. El checklist
de cierre, por su lado, exigía que el país fuera *"uno de los 7"* mientras la description de
la misma skill decía 10. Alguien actualizó el número y no la lista. Efecto medido sobre el
texto: la skill **instruía por escrito rechazar a clientes de Argentina, Brasil y Guatemala**,
que la plataforma sí acepta.

**Qué dijo FER (06-sep).** *"Los países no deberían importar mucho, porque ahorita son diez,
mañana son doce, pasado mañana son veinte, treinta. El país se pide para saber cómo enfocarlo,
cuál es la jerga, cuál es la validación de direcciones, pero no para prohibir."*

**Qué se hizo.** No se corrigió la cifra: **se retiró la puerta**. El país pasa de filtro a
parámetro — determina jerga, tiempos por zona y pack de direcciones, y nunca decide a quién se
le puede configurar. `paises_validos` se sigue consultando, pero solo para saber si ya hay
jerga y pack conocidos; que un país no aparezca significa dato atrasado o pack pendiente, y en
los dos casos se sigue adelante declarando el hueco.

**La ley que queda.** Cuando un dato caduca solo (una lista de países, un cupo, un precio de
plataforma), mantenerlo al día es una tarea infinita que se falla en silencio. **Se elimina la
dependencia, no se actualiza el dato.** Y el relato del defecto vive en el acta, no en el
cuerpo: el cuerpo se paga en cada activación, y repetir ahí la frase prohibitiva la deja a la
vista del modelo cada vez que la skill se enciende.

## 2026-09-06 · skill v1.7 (golden-skill-auditor, auditoría completa)

**Puntaje:** 915/1000 base determinista (PLATA) antes de reparar → 935/1000 después. Compuerta
dura (`validar_arsenal.py`) en 0, sana. Inventario limpio: 0 referencias rotas, 0 huérfanos,
2 archivos, blindada con `chflags uchg` (se conserva el mismo mecanismo al cerrar).

**Qué se reparó (evidencia real, robustez −20 en la rúbrica):** el SKILL.md tenía el historial
completo en `references/changelog.md` pero ningún sello de versión vigente bajo su propio H1 —
el comentario de la línea 16 solo apuntaba al acta, sin número de versión. El validador de
inventario lo marcó como aviso ("Sin línea de versión/changelog bajo el H1"). Se agregó la línea
`<!-- skill v1.7 · 2026-09-06 · ... -->` bajo el H1, sin tocar contenido ni comportamiento.

**Qué queda declarado como pendiente con dueño (no se inventó, no se tocó):** el flujo entrega
"el resumen operativo" y "el prompt de validación listo para pegar en el campo del asistente
logístico de Chatea Pro" sin nombrar el bot field nativo exacto donde va cada dato del intake
(transportadoras habilitadas, prohibidas, tiempos por zona) dentro de los cuatro campos nativos
ya listados en la sección de Techos (Adaptación del lenguaje / Método para evitar la cancelación
/ Políticas de garantía / Restricciones). Mapear qué dato va en qué campo exige verificar en vivo
contra el panel de Chatea Pro — es conocimiento de plataforma que solo se confirma probándolo
contra un espacio real, no se adivina desde este chat. Rúbrica: Instrucciones (falta plantilla
exacta de salida) e Proceso y flujo (falta el último tramo del punta a punta). No se resolvió
para no inventar el mapeo y dejar una regla falsa peor que la ausencia de regla.

**Fuentes de verificación:** `golden-skill-auditor/references/rubrica.md` y `estandares-golden.md`
(pesos y chequeos), `validar_arsenal.py` corrido en vivo (exit 0), `ls ~/.claude/skills` para
confirmar que las 4 skills hermanas citadas (`golden-chatea-pro-validacion-direcciones`,
`golden-chatea-pro-config-ventas-wp`, `golden-chatea-pro-config-carritos`,
`golden-chatea-pro-full-configuracion`) existen hoy con la capacidad que se les atribuye.

**Fase 7 pendiente:** reportar este cierre al Centro de Mando manualmente (el mensajero entre
sesiones no está disponible en este entorno).

### 2026-09-06 (mismo día, segunda pasada) · El PASO 0-bis: país sin pack

FER matizó: **el país sí es importante** —de él dependen jerga, transportadoras, tiempos y
validación de direcciones, y siempre se pregunta—, lo que no puede es bloquear. *"Si de pronto
crean otro país, un El Salvador que no está, que la skill tenga la libertad de configurarlo,
pero le tiene que preguntar varias cosas."*

Retirar la puerta (primera pasada) dejaba la mitad del trabajo: quitaba el "no se puede" pero
no decía **qué hacer en su lugar**, y un hueco sin protocolo se llena con lo que cada corrida
improvise. Se añadió el **PASO 0-bis**, con el anuncio en una frase (*"todavía no lo tengo
cargado, pero lo procesamos igual"*) y los 8 datos que se relevan: transportadoras del país,
modalidades y cuáles hacen contra entrega, tiempos por zona (en blanco, diciendo por qué),
entrega en oficina, composición de la dirección, jerga local, moneda, zonas sin cobertura.

**No se pregunta la prioridad de transportadoras** — FER la descartó expresamente.

Y se cierra el ciclo: lo relevado se entrega como **pack propuesto** a
`golden-chatea-pro-validacion-direcciones`. Sin eso, el siguiente negocio del mismo país repite
el interrogatorio entero y **el hueco deja de ser un hueco para volverse una costumbre**.

### 2026-09-06 (tercera pasada) · El PASO 0-bis se INVESTIGA, no se pregunta

Mi versión anterior del PASO 0-bis convertía el hueco en un interrogatorio de 8 preguntas, y
entre ellas metía la jerga local y cómo se compone una dirección. FER lo tumbó:

> *"La jerga y la configuración de las direcciones no se le pregunta a la gente, porque
> precisamente para eso es la skill, para que nosotros lo hagamos. Eso ya lo tenemos, eso ya
> lo hacemos nosotros. Tú tienes que ir a Internet, revisar, estudiar, analizar, extraer esa
> información y configurarla perfectamente. Tenemos que preguntar lo menos posible de lo que
> nosotros ya sabemos configurar. La menor fricción es lo ideal."*

**El error de fondo:** quitar una puerta y sustituirla por un cuestionario no baja la fricción,
la mueve. Y preguntar lo averiguable es **cobrarle al cliente nuestro trabajo**, con el agravante
de que una respuesta mala queda escrita como regla — el mismo defecto que ya cerramos el 06-sep
con *"qué tal que el cliente se equivoque y diga que puede hacer promesas"*.

**La frontera queda escrita en tres clases, no en dos:**
· **Se PREGUNTA** lo que no existe en ninguna fuente porque vive en la cabeza del dueño: nombre
  de la tienda, país, WhatsApp de servicio, web, transportadoras contratadas y prohibidas.
· **Se SUGIERE** lo que es decisión suya pero podemos proponer: el nombre del bot, el tono.
  *"Podemos sugerir, mas no adivinar."*
· **Se INVESTIGA** todo lo que es del país, porque el país no es secreto de nadie: forma de la
  dirección, **cómo la gente explica cómo llegar** (*"la casa roja"*, *"el balcón amarillo"*,
  *"frente a la iglesia"*, que es el corazón del pack), jerga, transportadoras que existen y
  cuáles hacen contra entrega, tiempos típicos, si hay recogida en oficina, moneda.

Listón: **tres fuentes independientes** y de distinto tipo (transportadoras del país, lugares
donde gente real escribe direcciones, documentación postal). Lo no confirmado se marca **NO
VERIFICADO** y solo eso se le confirma al negocio, diciéndole por qué. El pack propuesto viaja
**con sus fuentes**.

### 2026-09-06 (cuarta pasada) · La skill deja de CONFIGURAR: AUDITA y OPTIMIZA

**Lo que estaba mal de raíz.** El flujo entero suponía un espacio en blanco. Eso no existe:
el dueño instala los cuatro asistentes primero —si no, no hay plantillas que conocer— y la
plataforma los deja **con una plantilla de fábrica ya escrita**. FER: *"Nosotros no
configuramos nada. Lo que hacemos es cambiar los campos. Siempre vamos a auditar ese espacio,
porque ya hay campos llenos, y lo vamos a mejorar."*

**Lo medido que lo sostiene** (dos espacios nuevos, 06-sep): 61 de 61 campos **idénticos byte
a byte** entre uno nacido en cuenta de Colombia y otro creado eligiendo México en la encuesta.
**La plantilla nace colombiana elijas el país que elijas.**

**Lo que se añadió:**
· `scripts/auditar_espacio.py` — clasifica los 61 campos en **FÁBRICA / TOCADO / VACÍO** por
  md5 del valor contra `assets/plantilla-fabrica.json`, y **cruza el país declarado contra el
  escrito**. Corrido contra el espacio real de México: 51 de fábrica, 0 tocados, 10 vacíos y
  **4 campos diciendo `colombia`** en un espacio creado para México. Autoprueba 6 de 6, que
  muerde pieza por pieza.
· `assets/plantilla-fabrica.json` — la huella de los 61 campos y los valores del logístico.
  Sale de dos espacios vacíos: **no lleva dato de ningún cliente**.
· Renumeración: **PASO 0 AUDITAR** entra delante; el intake pasa a PASO 1 y solo releva **el
  hueco que dejó la auditoría**.
· El **país vuelve a preguntarse siempre** (es de lo que solo sabe el dueño) y ahora además se
  cruza. Sin ese cruce la contradicción no se ve, porque el panel se ve perfecto.
· **Grados de personalización**: sin identidad → óptimo para cualquier nicho, sin inventarle
  rubro ni cifras; con productos → enfocado a esa familia; siempre → al país real.

**La bandera `is_template_field` de la plataforma NO sirve**: viene en falso en 9 de cada 10
campos. Se mide por el VALOR, nunca por lo que el sistema dice de sí mismo.

**Defecto propio cazado en la autoprueba:** el sabotaje del caso NFC/NFD escribía
`"pais": "colombia"` con espacios, y el JSON real viene sin ellos, así que no sustituía nada y
la prueba culpaba al auditor. Un banco no puede dar por hecho un formato que no midió.

## v1.8 · 2026-09-06 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

**Contexto.** FER pidió auditar seis skills de Chatea y no cerrar ninguna por debajo de 1000.
Esta fue la primera. Los dos validadores y la autoprueba estaban en VERDE (6 de 6) antes de
empezar: el hallazgo no salió de leerla, salió de **correrla contra casos que se sabían malos**.

### Los cuatro verdes que no medían nada (`scripts/auditar_espacio.py`)

1. 🔴 **El OK vacío del cruce de país.** Si ningún campo traía la llave `"pais"`, el informe
   imprimía *"OK el pais escrito coincide con el declarado (MEXICO)"* y salía **0** — sobre un
   espacio cuyo texto citaba el Estatuto del Consumidor colombiano. **Un OK que no comparó nada
   es peor que un silencio: cierra la puerta a que alguien mire.** Ahora, sin llave y sin señal,
   dice `EL CRUCE DE PAIS NO SE PUDO HACER` y sale en rojo.
2. 🔴 **El universo sin denominador.** Imprimía *"3 campos leidos"* y *"la plantilla tiene 61"*
   en líneas contiguas y **nunca los comparaba**. Es el fallo del 2026-09-06 (informar 10 de 61
   como si fueran todos) reencarnado **dentro del instrumento construido para no repetirlo**.
   Ley: **medir no es comparar; un número sin vara al lado no es un chequeo, es decoración.**
   Ahora `LECTURA INCOMPLETA` y rojo.
3. 🔴 **`KeyError: 'name'`.** Un registro sin nombre tumbaba la auditoría entera con una traza
   de Python. Ahora se cuenta y se denuncia; el resto del informe sigue.
4. 🔴 **El tope de paginación era mudo.** `while page <= 40` salía sin avisar al agotarse.
   Ahora avisa por stderr con el conteo leído.

### El error que cometí construyendo la cura, y por qué queda escrito

El detector de país en prosa nació con "código postal", "departamento", "colonia",
"paquetería", "coordinadora" y "envía" en la lista. Resultado medido: **marcó MÉXICO en la
plantilla colombiana** porque decía "código postal", y `\benvia\b` casa con el verbo *enviar* en
cada mensaje del bot. Es la ley de la casa que ya estaba escrita —**un detector de patrones
acusa al idioma**— cometida otra vez mientras se construía el detector.

**Criterio duro que queda:** una señal solo entra si nombra una **institución, una marca o un
país**. Nunca una cosa. El vocabulario es JERGA (dice *cómo* escribir), la identidad es *quién*
regula, *quién* transporta, *qué* prefijo y *qué* moneda.

### La prueba que medía por poderes

El caso 5 comprobaba NFC/NFD usando *"no hubo contradicción"* como sustituto de *"el acento no
rompió la comparación"*, sobre un campo cuyo texto seguía citando la ley colombiana. Al mirar la
prosa, el sustituto se cayó — **y tenía razón en caerse**. Se reescribió para medir la
normalización directamente. Autoprueba **6 → 12 casos**, los cuatro sabotajes incluidos.

### En `SKILL.md`

· El comando del PASO 0 usaba **ruta relativa**, cuando la propia skill enseña tres secciones
  más abajo que con ruta relativa el validador da fallo falso. Ahora es absoluta y dice por qué.
· El **checklist de "terminado" no mencionaba el PASO 0**, la fase estrella de v1.7: se cerraba
  sin obligación de haber mirado el espacio. Ahora es el primer punto, y exige la línea de
  COBERTURA sin `LECTURA INCOMPLETA`.
· Se declara la cobertura del cruce (6 familias de países) **y su límite**: fuera de ellas el
  texto no delata al país.

### Lo que NO se tocó y por qué

· `assets/plantilla-fabrica.json` lleva `¿` y `¡` y el validador los marca. **Es una huella md5
  de lo que escribe la plataforma, no texto nuestro**: corregirle los signos rompería la
  identidad byte a byte que hace funcionar toda la clasificación FÁBRICA/TOCADO. Excepción
  declarada, no descuido.

### Cierre de la v1.8 · dos huecos más, hallados al re-verificar

5. 🔴 **`--desde-json` con otra forma moría con `AttributeError`.** Un fichero que no fuera una
   lista de registros daba una traza que parece un bug del script y es un fichero equivocado.
   Ahora se rechaza con un mensaje que dice qué se esperaba, y **se acepta la envoltura
   `{'data': [...]}`** tal como responde `/flow/bot-fields`. Autoprueba **12 → 14**.

**Ejercida contra datos reales, no solo contra el banco.** Se reconstruyó un espacio de 61
campos con los valores de fábrica REALES medidos en el servidor y se corrió dos veces:
· declarando COLOMBIA → `OK`, **sin un solo falso positivo** sobre el texto real (que era el
  riesgo de meter un detector de prosa).
· declarando MEXICO → contradicción, con la llave `pais` **y 3 señales de texto en 3 campos**;
  dos de esos campos la llave sola no los veía. Ahí está lo que el detector aporta.

## 2026-09-07 · CUPO DE LA API: se lee, se avisa y se frena antes de gastarlo

**Pregunta de FER, y el desarrollador de Chatea tenía razón:** el API limita a **1.000 peticiones
por hora** y pasarse **bloquea una hora entera**. La respuesta trae el contador de las que quedan.

**MEDIDO contra la API viva** (una lectura real, no documentación):

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: 999

En inglés: **X-RateLimit-Limit** y **X-RateLimit-Remaining** — "las peticiones que quedan".

🔴 **Hasta hoy NINGUNA de las diez skills de la familia leía ese contador.** Se trabajaba a
ciegas: se arrancaba una operación cara sin saber si cabía, y el bloqueo aparecía **a mitad**, con
el inventario incompleto o la configuración escrita por la mitad.

**Coste medido de una auditoría completa: 137 peticiones** (espacio de referencia casi vacío: 61
bot fields, 6 agentes IA, 45 tareas IA; uno de cliente cuesta más). **Con 1.000/hora caben ~7.**

**Qué se cableó:**
· El contador se lee de **cada** respuesta — viaja gratis en la cabecera que ya llegó — y se
  **dice** al terminar, con cuántas operaciones más caben.
· **Comprobación previa** antes de una operación cara: cuesta 1 petición saberlo antes y cuesta
  una hora averiguarlo después.
· Ante un **429 no se reintenta**: reintentar sobre un bloqueo lo alarga. Se declara qué quedó a
  medias, porque ni el panel ni un inventario parcial lo delatan solos.
· Herramienta de casa nueva: **`golden-chatea-cupo [token] [--necesito N]`**, que responde en una
  sola petición si cabe lo que se va a hacer.

⚠️ **Límite declarado:** la respuesta **NO trae `x-ratelimit-reset`**. El servidor **no dice
cuándo** se repone el cupo. La ventana es de una hora; si es fija o deslizante **no está medido** y
no se afirma. Lo único seguro es el número que queda AHORA.


## Mudado del cuerpo del SKILL.md el 2026-09-18 (actas v1.9 y v1.10, literales)

<!-- skill v1.10 · 2026-09-13 · auditoría golden-skill-auditor (AUDITA+ARREGLA). Único hallazgo
real con evidencia: la description no tenía cláusula de frontera/derivación (rúbrica,
Activación −15) — un pedido ambiguo de "configurar ventas" o "configurar carritos" podía
competir sin que el description marcara a dónde ir. Se agregó "No configura VENTAS ni
CARRITOS: usa golden-chatea-pro-config-ventas-wp o -config-carritos." (918 → 1010 caracteres,
bajo el tope duro de 1024). Compuerta `validar_arsenal.py` exit 0 antes y después. Resto de la
skill (SKILL.md, changelog, script, plantilla) verificado sin hallazgos nuevos: 0 referencias
rotas, 0 huérfanos, autoprueba de `auditar_espacio.py` 16/16 ejecutada en vivo, sintaxis OK.
Reservas ya declaradas en "Lo que NO está verificado" y en el changelog (mapeo exacto
bot-field↔dato de intake, tope de Restricciones sin medir, topes caducables, mapa del panel
incompleto, sin prueba contra espacio de cliente desde el 08-sep) se mantienen intactas: cada
una nombra quién la cierra y no se inventó su cierre. -->
<!-- skill v1.9 · 2026-09-08 · QUÉ ES LA CONFIGURACIÓN, DICHO POR FER, Y UN TOPE QUE LLEVABA UN MES SIENDO FALSO.
FER grabó un vídeo de 98 s recorriendo el panel entero del asistente logístico y dijo lo que
esta skill hace y lo que no: "lo único que hace es entrar a esos JSON y llenarlos, no hay que
hacer nada más — pero llenarlos analizando lo que esa tienda maneja en determinado nicho. No
tienen que quedar igualitos todos". Eso entra al cuerpo como sección propia y con sus palabras.

Del vídeo salió el MAPA COMPLETO del panel: 4 pestañas (Configuración General · Confirmaciones ·
Seguimiento · Novedades) y sus 18 secciones, campo por campo. Vive en
`golden-chatea-auditoria/assets/campos-de-configuracion.json`, que es el denominador compartido
entre esta skill y la que audita: hasta hoy la configuración se definía por exclusión.

🔴 Y destapó un dato falso que esta skill llevaba desde el 07-ago: decía "el logístico NO tiene
tope en sus campos de texto" y nombraba los cuatro. El contador del panel marca 2.000 en tres de
ellos, y en el Método para evitar la cancelación marcaba 1.990/2.000 PINTADO EN NARANJA, o sea a
10 caracteres de cortarse. La fuente era `TOPES-NATIVOS-POR-CAMPO.md`, extraído del código de la
app un mes antes; se le puso aviso de caducidad ahí mismo, porque su sección de Carritos tiene
el mismo problema. LA CLASE: una medida contra el código de una app que se actualiza sola CADUCA
EN SILENCIO, y un negativo ("no hay tope") es lo que peor envejece — cuando la plataforma añade
el límite, el documento sigue diciendo que no lo hay y nadie lo revisa. El contador que pinta el
panel es la fuente autoritativa.

Topes medidos que entran al cuerpo: 250 (nombre y enlace de tienda, id de voz, api key,
recordatorios de oficina) · 2.000 (los siete textos de identidad y tiempos) · 3.000 (los tres
ganchos de venta) · 8.000 (el prompt de análisis de dirección, que es el de la skill hija) · 15
(id de producto de Dropi). `Restricciones` NO se midió y se declara sin medir, en vez de
asumirle 2.000 por parecerse a sus vecinos.

Sembradas dos pruebas: que el cuerpo no vuelva a AFIRMAR que no hay tope —anclada a la forma
afirmativa, porque el cuerpo cita la frase vieja al corregirla— y que declare los topes medidos
con su evidencia. Contraprueba: repuesto el párrafo viejo en una copia, la autoprueba baja de
16/16 a 14/16. Medido al cerrar: autoprueba 14 → 16 de 16. -->

## 2026-09-18 · v1.11 · fábrica en su chat (optimización de Golden)
Cuatro campos JSON y no dos · tiempos y recordatorios = estándar de FER, no se preguntan · intake del anticipo (monto, datos de pago buscados primero en la config viva, descuento del total) · emojis con estándar explícito · sección 'Lo aprendido optimizando Golden' · escritor por API `scripts/escribir_espacio.py` con autoprueba 7/7 y dos sabotajes que la tumban a 6/7 · regla del techo y regla del pago anticipado · reserva del tope de Restricciones cerrada (2.000) · actas v1.9/v1.10 mudadas aquí desde el cuerpo.

## 2026-09-22 · v1.12 · el PASO 0 deja de ser ciego
`auditar_espacio.py` pasa de mirar solo `[Logistico] Configuracion General` a revisar los 4 campos de configuración con siete comprobaciones de contenido (topes UTF-16, vacíos, tiempos iguales, transportadoras del gancho de oficina, emojis, pago anticipado de fábrica, regla contra ejemplo). Autoprueba 16 → 27 casos; tres sabotajes la bajan a 25/26, así que el banco muerde. Corregida la línea que decía 'COBERTURA: 86 de 61': el 61 es la plantilla de fábrica, que es la vara, no el denominador. Y nueva ley de FER: lo que no aparece en el panel no es configuración — `NO_ES_CONFIGURACION` con 6 campos que ya no cuentan como defecto aunque estén igual que de fábrica. Origen: esta fábrica reportó como 'sin adaptar' los mensajes por tipo de novedad, que el dueño no puede editar. Corrido en vivo contra Golden: 86 de 86 campos, 4 de 4 de configuración, 0 hallazgos.

## 2026-09-22 · v1.13 · la parte dinámica, y menos falsos positivos
Sección nueva **LA PARTE DINÁMICA**: los 10 datos que cambian de un espacio a otro (país, identidad, nombre del asesor, números, transportadoras, validaciones, anticipo, garantía, origen y modelo, plantillas del WABA) y la doctrina que NO cambia. Mandato de FER: la skill deja de reabrirse en cada cliente; si una corrida quiere cambiar algo fuera de esa lista, va al Centro de Mando.
Auditor: dos falsos positivos menos y un aviso real. Con el audio apagado, la voz vacía ya no se señala (era coherencia, no hueco); y 'parte del envío' elegido con el porcentaje vacío ahora se avisa, porque la opción pide ese número y la plataforma no tiene monto fijo. Autoprueba 27 → 31 casos, los cuatro nuevos en los dos sentidos.
Cuerpo: la LEY de no heredar datos y los campos [Meta] calientes se mudaron a `references/ley-datos-entre-espacios.md` (5.974 caracteres) dejando el resumen operativo y el puntero. 547 → 480 líneas, y el validador de la casa vuelve a 'sana' sin avisos.
Corrido en vivo contra Golden: 86 de 86 campos, 4 de 4 de configuración, 24 de 24 dentro de tope, 0 problemas y 1 aviso (el porcentaje del envío).
