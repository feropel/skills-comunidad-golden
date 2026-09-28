---
name: golden-chatea-auditoria
description: >-
  Golden Group — AUDITORÍA DE SALUD DE UN ESPACIO DE CHATEA PRO. Entra por API al workspace,
  inventaria TODO (bot fields, asistentes, disparadores, subflujos, interruptores,
  integraciones, campos de usuario) y dictamina campo por campo qué está sano y qué está roto o
  a punto de romperse en silencio. Entrega COBERTURA medida (N de N revisados) y las fallas con
  evidencia, nunca un "quedó perfecto". Úsala SIEMPRE que el usuario quiera auditar, revisar o
  diagnosticar Chatea Pro o un asistente: "revisa mi chatea", "qué está mal en el bot", "el bot
  dejó de responder", "revisa la instalación", "audita el espacio de X", "está bien
  configurado", "qué le falta a mi chatea", "el asistente no dispara", "revisa que no se haya
  roto nada", o antes y después de tocar la configuración de un espacio. Dispara aunque no diga
  "auditar": basta con sospechar que algo de Chatea no funciona. Audita la CONFIGURACIÓN; los
  productos solo si se piden. No mira conversaciones del día: eso es golden-chatea-operacion.
---

**Fábrica:** chat «✅ SKILL golden-chatea-auditoria»
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1013 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# golden-chatea-auditoria · la salud de un espacio de Chatea Pro

## 📋 Requisitos: qué necesita del usuario antes de arrancar

- **Token API del espacio de Chatea Pro** · BLOQUEANTE. Se crea en el panel del espacio (*Settings → API Keys*, según el propio código) y va **atado al Bot**; si no, la API responde 404 "Flow not found". Se guarda en `<carpeta del cliente>/.secrets/<espacio>.token`. Cupo: 1.000 llamadas por hora (no está medido si es por token o por espacio; se mira con `golden-chatea-cupo`).
- **Cupo libre para la auditoría completa** · BLOQUEANTE: `extraer.py` se niega a arrancar si no cabe. Se mira antes con `golden-chatea-cupo`.
- **`python3` y red hacia `chateapro.app`** · BLOQUEANTES.
- **Alcance** · opcional: por defecto `config`; los productos solo si se piden.
- **Plantilla de fábrica de `golden-chatea-pro-config-logistico`**, que lee el control F14 · DEGRADABLE: sin ella, F14 se declara no corrido.

**Si falta algo BLOQUEANTE: no se hace lo que depende de él** (si es de toda la skill, se PARA antes de tocar nada) y se pide con nombre propio: qué es, dónde se saca y dónde se pone. **Si falta algo DEGRADABLE: se pide y se sigue**, dejando marcado como NO CORRIDO en todo lo que depende de él. Nunca se presenta como completo.

<!-- skill v3.5 (GCA3.5) — 2026-09-28 — FILA P66: LA EXTRACCION SE CORTABA Y EL DIFF
INVENTABA CAMBIOS. El CdM lo midio en una corrida real: `/flow/bot-fields` se cayo DOS veces con
IncompleteRead a mitad de la paginacion (30 de 89 campos y 10 de 89). Tal como estaba, esas 30
filas se guardaban como si fueran el universo y el diff contra la corrida anterior habria
reportado "76 cambios" -- los 59 que no llegaron, como si alguien los hubiera borrado. Un diff con
datos a medias no sale pobre: sale FALSO, y un cambio inventado manda a alguien a arreglar lo que
no esta roto. Clase ya conocida: urllib corta respuestas y curl no.
Tres arreglos: (1) `pedir()` usa CURL como via principal y urllib solo de respaldo, reintentando
una vez ante IncompleteRead; la llave viaja por STDIN en un fichero de configuracion de curl,
nunca en argv -- lo que hay en argv lo ve cualquier `ps` de la maquina. (2) `todas_las_paginas()`
devuelve si quedo PARCIAL, y detecta los DOS modos: la pagina que falla y la que no falla pero
deja menos filas de las que el servidor declara. El DUMP lo declara en `_PARCIAL`. (3) `comparar()`
se NIEGA a comparar un DUMP parcial: J1 sale NO CORRIDO con el motivo, en vez de un diff falso.
Dos trampas del sandbox, medidas de paso y documentadas en el codigo: `dump-header = /dev/stderr`
hace fallar a curl con el codigo 23, y el proxy añade su propio bloque de cabeceras, asi que con
`include` llegan DOS y hay que pelarlos o el JSON no parsea.
Probado en las dos direcciones y EN VIVO, no solo en el simulador: banco propio del extractor con
un corte simulado a mitad (y su control negativo, que una paginacion completa no se marque
parcial), y 3 comprobaciones contra la API real por 2 peticiones del cupo. Medido al cerrar:
autoprueba 34 defectos + 30 pruebas, extractor 2 de 2, simulador 7 de 7, compuerta 0. -->
<!-- skill v3.4 (GCA3.4) — 2026-09-28 — LA COMPUERTA DEL REPO PARO LA PUBLICACION, Y EL HUECO
DE LOS NOMBRES SE CERRO. La compuerta `golden-barrido-publicacion` freno GCA3.3 con 4 hallazgos en
3 ficheros: el nombre de una empresa usado como prosa de comentario y de changelog ("medido sobre
X", "el chat de X"). Ninguno era fixture del banco, asi que no habia prueba que romper: salio el
nombre, se quedo la leccion. Compuerta en CERO probado.
Lo de fondo: es la SEGUNDA vez que un nombre se cuela, y las dos las cazo la compuerta del repo,
no el guardia propio -- que decia, literalmente, "NO VERIFICADO por codigo: los NOMBRES. Eso se
lee". Declarar un hueco es honesto pero no es cerrarlo, y un hueco que depende de que alguien lea
se cuela otra vez. Ahora `sin_datos_de_cliente.py` DELEGA los nombres en el vigilante de la casa,
que es quien tiene la lista; la lista NO se copia a la skill a proposito (copiarla seria meter
aqui justo el dato que no debe estar, y naceria desactualizada). Y si el vigilante no esta, la
corrida NO da el OK: devuelve 1 y lo declara, la misma regla que P59 impuso para los archivos
ilegibles. La autoprueba del guardia comprueba las DOS direcciones sin escribir ningun nombre
real: con el vigilante ausente exige "NO VERIFICADO", con el presente muestra su veredicto.
Medido al cerrar: compuerta 0 hallazgos, guardia muerde y da 0, autoprueba 34 defectos + 29
pruebas, simulador 7 de 7, validador sin fallos ni avisos. -->
<!-- skill v3.3 (GCA3.3) — 2026-09-27 — FILA P59 DEL CENTRO DE MANDO: SEIS DESCARTES
SILENCIOSOS. Orden de FER via ARSENAL: "que todas las skills esten perfectamente corregidas", con
la regla de que si se descarta algo, se CUENTA y se NOMBRA en la salida. Los seis casos que
ARSENAL midio en esta skill, cerrados:
(1) GRAVE · el guardia de privacidad saltaba en silencio los archivos que no son UTF-8 y devolvia
"0 datos" -- medido, un .md en latin-1 con un correo adentro daba limpio. Ahora un archivo que no
se puede leer es un HALLAZGO propio, sale como NO REVISADO y bloquea el OK: un guardia que no
puede mirar no puede absolver.
(2) GRAVE · A4 calculaba los canales requeridos por los que estaban en `no_disponibles`, asi que
un requerido AUSENTE de la respuesta o en null salia PRESENTE (medido: `whatsapp=None` daba
"requeridos presentes 4 de 4"). Ahora son dos cosas distintas: el que el plan NO incluye sigue en
🔴 y el que no se pudo COMPROBAR sale en 🔵 con las hojas ilegibles nombradas.
(3) Control D9 nuevo: una entrada del disparador que no es objeto se sumaba a las entradas
revisadas de D2/D5/D6 sin revisarse ni nombrarse, y un `keyW` o `idAd` que no es texto se saltaba
de D5. El denominador crecia sin denominar. Ahora cada una sale con su indice, su tipo y su valor.
(4) C3 declara cuantas rutas se quedaron sin tope conocido, como ya hacia L5 con los campos fuera
del esquema.
(5) L2 acusa la llave de texto cuyo valor es null o numero: antes una cadena vacia SI se acusaba y
un null no, y al saltarla tampoco entraba en `comparables`, con lo que falseaba la proporcion con
la que L3 decide si hay espejo.
Y el acta y el cuerpo volvieron a decir lo mismo: estaban en v3.2 y GCA3.1, y lo caco la propia
autoprueba. Orden respetado: los cinco casos malos sembrados primero, comprobado que FALLAN (el
guardia dio "El guardia esta roto"), arreglo despues. Una prueba propia estaba mal escrita -- miraba
la evidencia cuando el nombre del campo va en el titulo -- y fue el tercer instrumento mio que fallo
en esta corrida: se corrigio antes de concluir. Medido al cerrar: autoprueba 34 defectos + 29
pruebas, simulador 7 de 7, guardia de privacidad muerde y da 0, validador sin fallos ni avisos. -->
**Versión:** `GCA3.5`  ·  historia completa en `references/changelog.md`

Auditar aquí significa **medir el estado real del servidor contra el estándar**, no leer la
configuración y opinar. Nada se da por bueno sin haberlo contado, y el informe se entrega en
cobertura (universo, revisados, fallas), jamás en veredicto.

**Frases prohibidas en todo lo que salga de esta skill:** "quedó perfecto", "todo bien",
"está listo", "debería funcionar". Si algo no se pudo verificar, se declara como no verificado.

## Lo que esta skill audita, y lo que no

| Audita | No audita |
|---|---|
| La INSTALACIÓN: campos, asistentes, disparadores, interruptores, integraciones | Las conversaciones del día (eso es `golden-chatea-operacion`) |
| El CONTENIDO de un prompt de producto **solo con `--alcance productos` o `todo`** | Escribir o corregir la config (eso es la familia `golden-chatea-pro-config-*`) |
| Lo que la config DICE que va a pasar | Lo que el bot respondió de verdad ayer |

## El alcance: esta skill es de CONFIGURACIÓN (ley de FER, 2026-09-05)

Palabras de FER: *"esta skill es exclusivamente para analizar configuración, configuración de
asistentes, no vemos productos"*. Por eso **el alcance por defecto de `auditar.py` es `config`**
y el de producto hay que pedirlo.

| bandera | qué juzga |
|---|---|
| *(nada)* = `--alcance config` | la **configuración de los asistentes**: estructura, techos de los campos generales, disparadores y su cableado, interruptores, integraciones, agentes y tareas de IA, credenciales |
| `--alcance productos` | **solo** el contenido de los campos de producto |
| `--alcance todo` | el catálogo entero, que es lo que ejercita la autoprueba |

**Qué cuenta como campo de producto lo declara `assets/campos-de-producto.json`**, no el
criterio del momento: `[Producto Ventas Wp] N`, `[Comentarios] Productos*`, los TOON de
Comentarios y `[Carritos IA] Información de productos`. **El disparador NO entra ahí**: nombra
productos, pero es cableado del asistente, o sea configuración — que fue justo la distinción
que se aplicó en el paquete del 28-ago.

**Lo que el alcance aparta se DECLARA, con su severidad y su conteo, en la cabecera del
informe** ("N hallazgos quedaron FUERA DE ALCANCE · no se juzgan aquí y NO están resueltos").
Recortar es legítimo; esconder es lo que convierte un auditor en adorno. Un 🔴 de producto sigue
siendo un 🔴: sale contado, y se lee entero con `--alcance todo`.

El filtro se aplica **sobre el hallazgo, no sobre la lectura de los campos**: todos los
controles siguen corriendo sobre el universo completo, así que los conteos del inventario y de
la cobertura no cambian con el alcance. Si el recorte se hiciera al leer, el informe diría que
el espacio tiene 78 campos cuando tiene 95, y eso ya sería una mentira medida.

## 🔴 QUÉ ES CONFIGURACIÓN, y hasta dónde puede mirar un control

**La ley de FER:** esta skill es **exclusivamente de configuración de asistentes**. Los productos
solo con `--alcance productos`, y eso lo pide él, no el operador.

**Dónde está escrito qué es cada cosa:**
· `assets/campos-de-configuracion.json` — **qué SÍ es configuración**, asistente por asistente,
  mapeado contra las capturas del panel vivo que FER entregó el 2026-09-08. Ventas WhatsApp está
  completo; los otros tres esperan sus capturas.
· `assets/campos-de-producto.json` — qué es contenido de producto.
· **Un campo que no esté en ninguno de los dos NO se asume configuración: se DECLARA como sin
  clasificar.** Hasta el 08-sep la configuración se definía por exclusión —solo existía la lista
  de producto— y por eso "auditar la configuración" no tenía denominador.

🔴 **LA FRONTERA, que es donde se cae todo el mundo** (dos chats el mismo día, 2026-09-08):

> **Un control de configuración que APUNTA a un campo de producto mira el CABLEADO del campo,
> JAMÁS su CONTENIDO.**

· **CABLEADO (sí se juzga, y se nombra la RANURA):** si `[Producto Ventas Wp] N` está registrada
  en el disparador, si su palabra clave coincide **byte a byte** entre los dos sitios, si está
  activa, cuánto ocupa el campo, si lleva una credencial dentro.
· **CONTENIDO (no se abre):** qué producto es, su marca, su precio, sus imágenes, si sus anuncios
  viven o están borrados. **Abrir el JSON del producto para "confirmar" un hallazgo de
  configuración es exactamente donde se cae** — y no hace falta: D3 se resuelve mirando el
  disparador.

**El filtro lo aplica el código por CONTROL, no por nombre de campo** (`CABLEADO` en
`auditar.py`). Hasta el 08-sep casaba el nombre, y con eso **le ocultaba a FER parte de su propia
configuración**: medido en el banco, **8 de 12 hallazgos apartados eran cableado suyo**, incluido
un desajuste de palabra clave que deja un producto sin arrancar.

**Lo apartado se declara con CONTEO Y NADA MÁS** — cuántos son y que existe `--alcance productos`.
Sin severidades, sin nombres, sin desarrollo, por grave que parezca. Para decir "hay un 🔴
apartado" habría que haberlo juzgado, que es justo lo prohibido.

## 🔴 CUPO DE LA API: 1.000 peticiones por hora, y una auditoría cuesta 137

**Medido el 2026-09-07 contra la API viva**, no leído en una documentación:

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: <las que quedan>

En inglés se llaman **X-RateLimit-Limit** y **X-RateLimit-Remaining**. Pasarse **bloquea una hora
entera**.

🔴 **Una extracción completa cuesta 137 peticiones** (medido contra un espacio de referencia casi
vacío: 61 bot fields, 6 agentes IA, 45 tareas IA). Un espacio de cliente con más productos y
suscriptores **cuesta más**. Con 1.000 por hora **caben unas 7 auditorías, no más** — y si alguien
corre la octava, se queda sin API una hora, incluidas las instalaciones que estén en curso.

**Lo que hace el extractor ahora:**
· **Comprueba ANTES de arrancar** (1 petición) y **se niega** si no caben las 137: empezar sin
  cupo deja el DUMP incompleto Y gasta lo que quedaba.
· Lee el contador de cada respuesta —viaja gratis en la cabecera que ya llegó— y **dice cuánto
  queda al terminar**, con cuántas auditorías más caben.
· Ante un **429 no reintenta** (reintentar sobre un bloqueo lo alarga) y marca el DUMP como
  incompleto: *"no lo audites como si fuera todo"*.

**Para saber el cupo sin correr nada:** `golden-chatea-cupo [token] [--necesito N]`.

**El reset: cada hora** (dato del desarrollador de Chatea, vía FER). Observado por nuestro lado:
dentro de la misma hora el contador **solo baja** — no gotea crédito, se repone de golpe.

🔴 **La trampa está en el CUÁNDO.** La respuesta **no trae `x-ratelimit-reset`**, así que el
servidor **no dice a qué minuto empezó la ventana**. Por eso: si te bloqueaste, espera una **hora
completa desde ese momento** —suponer que "ya casi" es como se pierde la siguiente tanda—; y para
saber si ya se repuso **mira el contador** (1 petición con `golden-chatea-cupo`), no lo calcules.
Planifica dentro de la hora **que ya empezó**: si quedan 300, cuenta con 300.

## Qué NO vive en esta skill (ley de FER, 2026-09-05)

Palabras de FER: *"en esta skill no puede haber información de ningún VIP, ningún miembro ni
mío... aquí no debería haber información de alumnos ni de nada que corrió. Eso es en cada
chat."*

**Aquí vive el ESTÁNDAR**: cómo se instala cada asistente, qué campos firma tiene, cuáles son
los dos techos, qué controles se corren y cómo se ve una auditoría completa. **La identidad de
quien se auditó no vive aquí**: ni el `user_ns` del espacio, ni el dominio de la tienda, ni
correos, teléfonos o credenciales, ni el nombre del cliente, del alumno o de la marca — tampoco
los del propio dueño de la skill. Eso vive en el chat de ese cliente y en el Centro de Mando.

Cuando un hallazgo real enseñe algo que valga para todos, **entra la lección y sale la
identidad**: "un espacio en producción traía el mismo asistente escrito de dos formas", no
"el espacio de tal cliente, con su identificador".

**Lo comprueba un instrumento, no la buena voluntad** — una regla sin instrumento es decoración:

```bash
python3 $S/sin_datos_de_cliente.py              # 0 = limpia
python3 $S/sin_datos_de_cliente.py --autoprueba # el guardia contra casos malos
```

Corre además dentro de `autoprueba.py` (prueba **PRIV**), así que un dato de cliente que entre
por descuido rompe el banco antes de que la skill se dé por buena.

**Los NOMBRES ya no son un hueco declarado: se DELEGAN.** Un nombre propio no tiene forma
reconocible, pero sí tiene dueño — `~/.golden/bin/golden-barrido-publicacion`, el vigilante de la
casa, que lleva la lista y la contrasta contra el mapa de proyectos. El guardia lo llama y reporta
su veredicto. **La lista no se copia aquí a propósito:** copiarla sería meter en la skill justo el
dato que la skill no debe llevar, y encima nacería desactualizada. **Y si el vigilante no está, la
corrida NO da el OK** y lo dice — un guardia que no puede mirar no puede absolver, la misma regla
que se aplicó a los archivos ilegibles.

## Lo que NO está verificado en esta skill (al 2026-09-08)

Esta sección vive **dentro de la skill** a propósito. Una reserva escrita en el informe de un
chat es un recuerdo: se pierde cuando el chat se cierra, y quien active la skill mañana no la
lee. Aquí la lee siempre.

**Y cada reserva nombra QUIÉN la cierra**, idea de la fábrica de
`golden-imagen-arena`: una reserva que no puede nombrar a su cerrador o ya está cerrada y sobra,
o nadie la ha pensado. Además hace que la sección **no se pueda vaciar en silencio** — vaciarla
obliga a borrar cerradores concretos, no a ablandar un adjetivo. Si algún día esto dice "todo
revisado" sin nombrar instrumento, está mintiendo.

**🔴 EL ESQUEMA SALE DE UN SOLO ESPACIO, Y L1 DEPENDE DE ÉL.** · **La cierra:** la primera
lectura por API de un SEGUNDO espacio bien configurado. Las 156 llaves de
`assets/esquema-configuracion.json` se leyeron del espacio de referencia y **de ninguno más**.
No está comprobado que otro espacio bien configurado tenga esas mismas llaves. Si Chatea versiona
la configuración —si un espacio instalado en otra fecha, o con otros asistentes, trae un JSON con
otra forma— **L1 marcaría en rojo decenas de llaves "ausentes" que en realidad nunca existieron
en ese espacio**. Ese es el modo de falla que hay que vigilar en la primera corrida contra un
cliente: si L1 dispara con números grandes en un espacio que se ve sano, sospechar del esquema
antes que del espacio. La cura, cuando haya un segundo espacio bien configurado: leerlo y quedarse
con la INTERSECCIÓN como obligatorio y la diferencia como opcional.

**Nada de lo cerrado el 08-sep se ha corrido contra un espacio real.** · **La cierra:** una
corrida completa contra un espacio de cliente, con su cupo reservado (~200 peticiones). Los tres controles nuevos
(L1, L2, L3) y las cuatro reparaciones de ese día (el paquete que escondía hallazgos, la cabecera
de lo apartado, la cobertura de la zona IA y la declaración de J1) están probados **contra el
banco**, con contraprueba una por una. Eso valida el detector, no valida ningún espacio.

**El umbral del 15% de L2 es una elección, no una medición.** · **La cierra:** contar los
falsos positivos de L2 en esa primera corrida real y mover el umbral con ese número. Se escogió para que solo salte lo
que es de otra escala. No hay medida de cuántos falsos positivos produce en un espacio real.

**L3 compara LARGOS, no textos.** · **La cierra:** nadie por ahora, y es a propósito —
confirmar un espejo exige leer el texto, y eso lo hace una persona, no el script. Detecta la firma de un clon —muchos campos midiendo exactamente
lo mismo— y por eso es DUDA y no defecto. Confirmarlo exige comparar el texto, y eso no lo hace
el script.

**F14 depende de un asset que vive en otra skill** · **La cierra:** el control CAT el día que
cruce también los assets externos, no solo los controles. **Hoy no lo hace.** · (`golden-chatea-pro-config-logistico/assets/
plantilla-fabrica.json`). Si esa skill se mueve o se renombra, F14 se declara NO CORRIDO — no se
calla, pero deja de cubrir.

**Los topes nativos del panel caducan solos.** · **La cierra:** nadie de forma permanente; se
re-mide en el panel en cada configuración. Es vigilancia, no una tarea que se termine. Los que esta skill conoce se midieron el 08-sep
contra el contador que pinta Chatea. Chatea se actualiza sin avisar: en agosto se midió "el
logístico no tiene tope" contra el código de la app y en septiembre era falso. Se mira el
contador, no se cree este documento.

## Regla de oro de esta skill

**Un prompt perfecto detrás de un interruptor apagado no hace nada, y un producto perfecto sin
entrada en el disparador no arranca nunca.** El contenido es la última capa que se mira, no la
primera. El orden es: llega el disparo → el interruptor está encendido → el campo cabe en los dos
techos → el contenido es correcto. Una falla en cualquiera de las tres primeras deja muerto un
contenido impecable, y ningún chequeo de texto lo detecta.

## Las cinco fases

### Fase 1 · INVENTARIO antes de tocar (el denominador)

Se corre el extractor y se cuenta el universo. Ese número es el denominador de todo el informe.

```bash
python3 ~/.claude/skills/golden-chatea-auditoria/scripts/extraer.py <ruta-al-token> <etiqueta> [carpeta-salida]
```

Deja `DUMP-<etiqueta>.json` con TODO lo que la API expone, con las credenciales **redactadas**
(guarda solo si hay valor y de qué largo, nunca el valor).

Antes de seguir, tres comprobaciones que no son opcionales:

1. **La identidad sale del servidor, no del nombre del archivo del token.** El nombre de un
   archivo de token no prueba a qué espacio pertenece. Se confirma con lo que devuelve
   `/me` y con el prefijo `user_ns` de los campos.
2. **La paginación se agotó.** `GET /flow/bot-fields` pagina de 10 en 10 e ignora `per_page`.
   Leer solo la primera página deja fuera el 90%. El extractor lo hace, pero el conteo se
   compara contra `meta.total` y si no cuadra, el informe se detiene.
3. **El universo se declara en el informe**: N campos de bot, N campos de usuario, N subflujos,
   N productos ocupados, N asistentes detectados.

### Fase 2 · CONSTRUIR midiendo contra el estándar

El estándar vive en `references/`. Se mide mientras se revisa, no después:

- `references/controles.md` — el catálogo completo de controles, bloque por bloque. **Es la
  columna vertebral de la skill: se recorre entero, no "lo importante".**
- `references/api.md` — endpoints, autenticación, paginación y las trampas de escritura y lectura.
- `references/topes.md` — los DOS techos, con la tabla de topes nativos por campo.
- `references/estandar-prompts.md` — qué debe tener el prompt de un producto para estar sano.
- `references/informe.md` — el formato exacto del entregable.

Y dos datos que viven fuera del código a propósito, para que un cambio de versión de Chatea se
arregle editando un JSON y no un script:

- `assets/topes-nativos.json` — los dos techos y el tope de cada campo del formulario.
- `assets/asistentes-esperados.json` — los campos firma de cada asistente, que es lo que permite
  detectar el que **falta**, no solo los que hay.

### Fase 3 · TRES FUENTES antes de cualquier veredicto

Ningún hallazgo se publica con una sola fuente:

1. **Algo equivalente que YA funciona en producción.** El espacio de referencia es Golden
   Colombia, que vende a diario. Para una instalación nueva, la referencia es la plantilla
   verificada. Un valor que parece raro pero es idéntico en un espacio que factura **no es un
   fallo**: es el default de fábrica.
2. **La fuente autoritativa del sistema.** El servidor, no lo que "se supone". Si la duda es un
   tope del formulario, sale del código de la app, no de la memoria.
3. **El validador corrido.** `auditar.py` sobre el DUMP, con su autoprueba pasada.

### Fase 4 · EJECUTAR (la fase que más se salta)

```bash
S=~/.claude/skills/golden-chatea-auditoria/scripts   # scripts/autoprueba.py y scripts/auditar.py
python3 $S/autoprueba.py                      # primero SIEMPRE · ella dice cuantas corre
python3 $S/simular_dias.py                    # y el ciclo sobre 7 dias que cambian
python3 $S/auditar.py <DUMP.json> \
    --decisiones <espacio>-decisiones.json \  # lo ya resuelto no se vuelve a gritar
    --anterior   <DUMP-de-la-corrida-pasada.json> \
    --handoff    paquete-correccion.md \
    --json       hallazgos.json
```

Las cinco banderas son opcionales y ninguna es decorativa:

| Bandera | Para qué |
|---|---|
| `--incluir-excluidos` | Audita también lo que **FER sacó del ecosistema** (hoy: Remarketing IA, sus campos y su agente de IA). Sin ella, eso se aparta al cargar y el informe lo declara contado en el universo, con el motivo. Se usa solo cuando FER pide revisar ese asistente en un espacio concreto, y eso no lo vuelve esperado para los demás. |
| `--decisiones` | El **libro de decisiones**. Lo que ya resolviste sale aparte, con su motivo y su fecha, y no vuelve a contarse entre lo pendiente. Sin esto, la corrida número tres son los mismos 40 hallazgos y dejas de leerla. |
| `--anterior` | **Qué se movió** desde la última auditoría: campos creados, borrados y editados con su delta. Es lo que convierte la foto en vigilancia. |
| `--handoff` | El **paquete de corrección** agrupado por la skill dueña de cada campo, listo para pasarlo al chat que sí escribe. |
| `--json` | Todo en crudo, para encadenar con otra herramienta. |

**La autoprueba va primero y no se salta.** Fabrica un espacio que se SABE roto (**los defectos sembrados
más las pruebas de comportamiento** — ella misma imprime cuántos de cada uno al terminar, para
que la cifra no viva a mano en un documento y desincronice el día que se añade una prueba;
entre ellas, los falsos negativos que dos verificaciones adversariales encontraron) y exige que el auditor los encuentre todos. Un auditor que sale en verde contra un
espacio sano no prueba nada: prueba que no mira. Si la autoprueba falla, el auditor está roto y
no se corre contra datos reales.

Además, lo que el código no puede juzgar se ejecuta a mano:

- **Los prompts se leen enteros**, uno por uno, contra `references/estandar-prompts.md`. No se
  muestrean. Si son doce productos, son doce prompts leídos completos.
- **Los acentos se verifican EN EL RENDER**, no en el archivo: el mojibake vive en el valor
  guardado y se ve al imprimirlo.
- **Las URLs de multimedia se piden** (HTTP 200 o el hallazgo dice qué devolvió).
- **Todo lo que entra al DUMP se audita o se declara.** Un endpoint extraído sin control es una
  zona sobre la que el informe no puede decir nada, y su silencio parece salud.
- 🔴 **Lo que FER sacó del ecosistema NO se lee a mano tampoco.** Hoy es **Remarketing IA**
  (sus campos `[Remarketing IA] …` y el "Agente de Remarketing"): el código los aparta y los
  declara, y la lectura manual no los reabre por la puerta de atrás. Se declara en el informe
  ("N campos apartados por decisión de FER") y se sigue. Distinto es el **remarketing de cada
  producto** de Ventas WhatsApp (`remarketing.prompt_1/2`), que sí se lee y se audita.
- **La simulación de disparo**: para cada producto activo, se compara byte a byte la palabra
  clave de sus dos sitios. Si difieren, ese producto no arranca, y eso es una falla de severidad
  máxima aunque el prompt sea impecable.

### Fase 5 · REPORTAR COBERTURA, NO VEREDICTO

El informe se arma con `references/informe.md`. Lleva siempre: universo, N de N revisados,
método, fuentes, qué se ejecutó, qué falla con su evidencia, y **qué quedó sin verificar y por
qué**. Los hallazgos van ordenados por severidad, con la falla que deja algo muerto arriba.

**Cierre obligatorio:** el agente `golden-verificador` recibe el estado final y el estándar, sin
saber cómo se construyó, e intenta romperlo. Su lista de "no verificado" entra al informe.

## Severidades

| Nivel | Significa | Ejemplos |
|---|---|---|
| 🔴 **MUERTO** | Algo no está funcionando ahora mismo | Producto **con pauta activa** fuera del disparador · campo por encima de 19.895 escapados, el último tamaño que se vio disparar · palabra clave principal que difiere en un acento · canal caído |
| 🟠 **MUERTE ANUNCIADA** | Funciona hoy y se rompe solo | Campo sobre el 90% del techo · campo por encima del tope nativo (se corta cuando alguien abra el panel y guarde) · par array/Extendido ambiguo |
| 🟡 **FUGA** | Funciona pero está mal | Llave de otra cuenta heredada · nombre de otra tienda dentro de un prompt · placeholder sin reemplazar · ortografía rota |
| 🔵 **DUDA** | No se pudo verificar, o hay que preguntarle a FER | Valor que difiere de la referencia sin saber cuál es el correcto |

**Un hallazgo contra la configuración no es un bug hasta contrastarlo con FER.** Si la config
dice una cosa y el negocio hace otra, puede ser que el negocio cambió y la config está bien.
Se reporta como DUDA y se pregunta, no se "arregla".

## Lo que esta skill NO hace

**No escribe.** Audita y reporta. Cuando hay que corregir, `--handoff` deja el paquete
agrupado por la skill dueña de cada campo, con la evidencia y la acción, listo para el chat que
sí escribe.

La razón de no escribir es dura y está medida: escribir con POST en vez de PUT devuelve `200` con un mensaje que no contiene la
palabra "error", y pasarse del techo devuelve `200 ok` guardando el contenido cortado. Una skill
que audita y escribe en la misma pasada puede reportar "corregido" sobre algo que nunca se
escribió. Si el usuario pide corregir, se corrige con la skill dueña y **se vuelve a auditar
desde el DUMP nuevo**, releyendo del servidor y comparando.

## Conexión con el ecosistema

**Cada cierre de esta skill se reporta al Centro de Mando** (`🧠 GOLDEN - CENTRO DE MANDO - NO
BORRAR`), haya hallazgos o no. Lo reporta quien la EJECUTA, no la skill: al terminar una
auditoría se manda qué espacio se midió, la cobertura (N de N), qué está muerto, qué se decidió
y desde qué chat se corrió. Una corrida limpia también se reporta — confirma que el ecosistema
está sano, y sin ese dato el Centro de Mando no puede coordinar.

Los cambios a esta skill se reportan igual, con su número de versión.

**Dependencias:** `python3` (solo librería estándar, sin paquetes externos) y acceso de red a
`chateapro.app`. El token del espacio lo entrega el usuario o vive en el depósito de secretos
del proyecto; esta skill nunca lo trae horneado.

## Cuándo correrla

- Antes y después de tocar cualquier configuración de un espacio.
- Después de reinstalar un asistente (reinstalar recrea los subflujos con `ns` nuevo y deja los
  disparadores apuntando al viejo, en silencio).
- Al recibir un workspace de cliente, antes de prometer nada.
- Cuando algo "dejó de responder" sin error visible.
- Como revisión periódica, para ver los campos que se van acercando al techo. A partir de la
  segunda vez, **siempre con `--anterior` y `--decisiones`**: sin ellas el informe repite lo que
  ya sabes y entierra lo nuevo.

## Cómo se responde un hallazgo

Cuando dictaminas sobre un hallazgo — "eso no es problema", "eso es a propósito" — la respuesta
**se escribe en el libro de decisiones**, no se deja en el chat. Un chat se cierra; el libro
viaja con el espacio.

El formato exacto, la guarda de espacio y las reglas de `motivo`, `fecha` y `reabrir_si` viven
en **el bloque J de `references/controles.md`** — ahí y en un solo sitio, para que no se
desincronicen. Lo que hay que retener aquí:

- **Sin `motivo` y sin `fecha` el código DETIENE la corrida.** Silenciar un hallazgo sin dejar
  rastro de quién lo decidió ni cuándo es el abuso que el libro podría habilitar.
- **`reabrir_si` dice en qué condición la decisión deja de valer.** Sin él la decisión se acepta,
  pero el informe avisa que ese hallazgo queda silenciado para siempre.
- **El libro es de UN espacio.** Si su `espacio` no coincide con el del DUMP, la corrida se
  detiene: un libro ajeno silenciaría fallas reales.

El archivo se llama `<espacio>-decisiones.json` y vive junto a los DUMP de ese espacio.

## Fronteras y desambiguacion

🔴 **Aquí NO se guarda una copia de la `description`.** Había una, con el rótulo de
conservarla "para no perder ningún matiz". Esa clase de copia **envejece y acaba
contradiciendo a la description viva** — es como se coló el dato falso de "7 países" en una
hermana de esta familia, y es el mismo defecto que se encontró el mismo día en
`golden-chatea-pro-producto-comentarios`. Por eso la frontera **no se repite aquí**: vive en
una sola versión, arriba, en la tabla `Lo que esta skill audita, y lo que no` y en la sección
`Lo que esta skill NO hace`. Resumen para quien solo lee este párrafo:

- **Conversaciones del día** (qué respondió el bot ayer) → `golden-chatea-operacion`, no esta.
- **Escribir o corregir la configuración** → la familia `golden-chatea-pro-config-*`, no esta.
- **Contenido de producto** → solo con `--alcance productos` o `todo`, nunca por defecto.

