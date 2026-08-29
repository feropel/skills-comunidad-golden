---
name: golden-chatea-auditoria
description: |
  Golden Group — AUDITORÍA DE SALUD DE UN ESPACIO DE CHATEA PRO. Entra por API al workspace,
  inventaria TODO (bot fields, asistentes, disparadores, subflujos, interruptores, integraciones,
  campos de usuario) y dictamina campo por campo y producto por producto qué está sano y qué está
  roto o a punto de romperse en silencio. Entrega COBERTURA medida (N de N revisados) y las fallas
  con evidencia, nunca un "quedó perfecto".
  Úsala SIEMPRE que el usuario quiera auditar, revisar o diagnosticar Chatea Pro o un asistente:
  "revisa mi chatea", "qué está mal en el bot", "el bot dejó de responder",
  "por qué no arranca este producto", "revisa la instalación", "audita el espacio de X",
  "está bien configurado", "revisa los prompts de los productos", "qué le falta a mi chatea",
  "el asistente no dispara", "revisa que no se haya roto nada", o antes y después de tocar la
  configuración de un espacio. Dispara aunque no diga "auditar": basta con sospechar que algo de
  Chatea no funciona. Aplica a cualquier workspace y a los 7 países de la plataforma.
  FRONTERAS: escribir la config = familia golden-chatea-pro-config-*; el prompt de venta =
  golden-chatea-pro-prompt-ventas; las CONVERSACIONES del día = golden-chatea-operacion; pedidos y
  novedades = golden-logistica-diaria. Esta skill audita LA INSTALACIÓN, no el día.
---

# golden-chatea-auditoria · la salud de un espacio de Chatea Pro

<!-- skill v1.8 (GCA1.8) — 2026-08-26 — SIMULACION DE DIAS en vez de esperar los dias.
El ciclo de vigilancia (auditoria → decision → cambio → re-medicion) se iba a validar dejandolo
correr unos dias reales; eso cuesta dias y descubre los fallos EN PRODUCCION. Se construyo
`scripts/simular_dias.py`, que corre el ciclo sobre un espacio que EVOLUCIONA (alguien corta un
campo desde el panel, un campo cruza el techo, se borra un campo, la API falla un dia, se
enciende pauta). Encontro el fallo de fondo el primer intento: **`reabrir_si` era PROSA que
nadie evaluaba** — solo se imprimia. La decision de los huerfanos dice "reabre si se les carga
un id de anuncio" y el dia que se cargara habria seguido silenciada: la promesa de que el libro
no es una alfombra no la sostenia nada. Arreglo: la decision guarda `evidencia_al_decidir`, la
foto de la situacion ese dia, y **CADUCA sola cuando la evidencia cambia** — cubre el caso
general (se cargo un anuncio, el campo crecio, aparecio otro producto) sin inventar un lenguaje
de condiciones que nadie escribiria bien. Las decisiones sin esa foto se avisan: no pueden
caducar. LECCION DEL PROPIO BANCO: el dia 7 pasaba con el arreglo SABOTEADO, porque registraba
el producto y el hallazgo desaparecia — la comprobacion se auto-aprobaba por una via que no
probaba nada. Se reescribio para que el hallazgo PERSISTA y solo cambie su evidencia. Medido:
7 de 7 dias con el arreglo vivo, 6 de 7 con el sabotaje, y el que se cae es el de la caducidad. -->
<!-- skill v1.7 (GCA1.7) — 2026-08-26 — auditoria fresca (el numero v1.6 ya
lo habia tomado otro chat el mismo dia con sus propios cambios; esta entrada es POSTERIOR). Tres defectos, dos de ellos de la
MISMA clase que la skill ya habia arreglado en otro sitio y cuyo GEMELO nadie busco.
(1) 🔴 LA SEVERIDAD IGNORABA EL `estado` DE LA ENTRADA: 8 de los 14 hallazgos del bloque D
gritaban sin mirarlo, 5 de ellos en rojo. Medido en Golden y reportado por la verificacion
adversarial: 4 de las 5 entradas del disparador de Remarketing estan `inactivo` en el servidor y
salieron en 🔴 igual — la evidencia hasta imprimia "estado 'inactivo'" y el codigo no lo leia. El
cuadro real no era "el disparador entero roto" sino UNA entrada activa mal cableada y cinco
apagadas de basura. Es el gemelo exacto de la regla que ya existia para los huerfanos (la
severidad la decide el negocio, no la estructura). Helpers `activa` / `sev_segun_estado` /
`nota_estado`, y las entradas al vacio se separan en ACTIVAS (rojo) e INACTIVAS (duda de
limpieza). (2) 🔴 EL LIBRO DE DECISIONES SE ROMPIO HACIA ATRAS EN SILENCIO: la huella corta
`::hash` que se anadio para que una decision no silenciara 5 hallazgos a la vez cambio la forma
de la clave, y 4 de las 6 decisiones ya escritas dejaron de casar — sus hallazgos volvieron a
gritar como si nadie los hubiera resuelto. Una clave que cambia de forma con una mejora del
codigo no es una clave estable, y el libro entero vale por su estabilidad. Ahora se aceptan las
DOS formas: FINA (`control|campo::huella`, silencia uno) y AMPLIA (`control|campo`, silencia
todos los de ese campo), y el informe AVISA cuando una decision amplia silencia mas de uno.
(3) 🟡 A4 leia mal su propio endpoint: `/workspace-settings/channels` dice que canales estan
DISPONIBLES en el plan (1/0), no si estan conectados. `apple: 0` — un canal que el plan de
Golden no incluye y que ningun asistente usa — salia en 🔴 MUERTO. Ahora solo dispara si falta
un canal REQUERIDO (whatsapp, whatsapp_cloud, facebook, instagram) y declara que la conexion
viva se mira en el panel, que es lo que ya dice A5. Autoprueba: 30 defectos + 12 pruebas de
comportamiento (EST y LIB nuevas). -->
<!-- skill v1.6 (GCA1.6) — 2026-08-25 — verificacion adversarial (golden-verificador) contra el
espacio REAL de Golden Colombia (fXXXXXX): ocho hallazgos, los ocho con su caso malo sembrado
en autoprueba.py ANTES de arreglar el codigo. (1) A4 no evaluaba NINGUN canal real: el endpoint
real trae enteros anidados bajo `data` (`{"data":{"whatsapp":1,...}}`) y el codigo solo
reconocia booleanos o strings "connected/active/ok" — lo unico que disparaba era el
`status:"ok"` del SOBRE HTTP, no un canal. Corregido para leer la forma real, con el fixture
reproduciendola. (2) E3 (credencial de voz heredada) NUNCA podia disparar contra un DUMP real:
comparaba `api_key` contra el string YA REDACTADO por extraer.py (`<<REDACTADO...>>`), que
siempre falla esa condicion — el fixture viejo probaba una forma en claro que el auditor real
jamas recibe. Ahora el control juzga si HABIA algo que redactar, no si sigue en claro. (3) El
paquete `--handoff` filtraba por "¿tiene `accion`?" ANTES de mirar la severidad: 22 de 39
hallazgos abiertos no llegaban al paquete en la corrida real, 5 de ellos rojos de un solo
disparador y 11 fugas de credenciales. Ahora todo 🔴 o 🟠 entra siempre, tenga o no `accion`.
(4) La clave del libro de decisiones (`control|objetivo`) no era unica cuando un mismo campo
acumulaba varios hallazgos distintos sin `objetivo` explicito (`D3|[Remarketing IA]...` cubria
5 hallazgos de una sola vez; `F3|[Producto Ventas Wp] 8` mezclaba un rojo con un azul bajo la
misma clave): una decision del dueno podia silenciar mas de uno sin que nadie lo notara. Se
afina con una huella corta de la evidencia cuando no hay `objetivo` (los agregados deliberados,
como `huerfanos-con-pauta`, siguen con su clave estable de siempre). (5) El diff (`--anterior`,
J1) mostraba el largo crudo del JSON prominente y solo el DELTA como "escapados": un campo cerca
del techo no tenia forma de leer su escapado absoluto real. Ahora muestra el escapado real
primero (`ea → en escapados`) y el crudo aparte, marcado. (6) Varios controles se declaraban
"corrido" sin denominador o sin ejecutar su medida real: B2 (el limite de campos de usuario no
lo expone la API — ahora NO_VERIFICADO siempre, nunca "corrido"), A1 (sin denominador, ahora
`1 endpoint`), B4 (contaba objetos sin declarar cuantos ni cuales, ahora lo declara), G2 (solo
hacia una pregunta y se marcaba "corrido" como si hubiera verificado algo — ahora NO_VERIFICADO
con la evidencia encontrada). Y F4/F12/I1 estaban en `A` en controles.md pero el codigo los
reporta NO_VERIFICADO (lectura humana): sincronizados a `H`. (7) Cifras de la autoprueba
desincronizadas entre SKILL.md y controles.md: quedan en **30 defectos + 11 pruebas de
comportamiento** en los dos lugares (las 4 nuevas: J1b escapado real, CLV colision de claves,
HO2 severidad en el handoff, I3B4 sincronia de la lista de endpoints auditados). (8) La lista
`auditadas` de I3 (bloque_i) vivia hardcodeada y desincronizada de lo que B4 realmente audita:
decia que subflows/tags/ai-agents/ai-tasks/inbound-webhooks/segments/agents no tenian control
cuando B4 ya los contaba — 7 falsos positivos. Ahora ambas comparten la constante
`ENDPOINTS_B4`, una sola lista para los dos lectores. -->
<!-- skill v1.5 (GCA1.5) — 2026-08-22 — PRIMERA lectura profunda de los 12 prompts de
producto en campo: los controles F4/F9/F10/F11/F12 estaban escritos desde el primer dia y NUNCA
se habian ejercido. Encontraron un defecto REAL en produccion que el auditor no veia:
`[Producto Ventas Wp] 8` (Tag Recede, ACTIVO y registrado en el disparador) llevaba
`[AQUI VAN LOS DATOS DE PAGO ANTICIPADO: Nequi/Daviplata + titular]` en pleno paso de cobro. La
lista de placeholders conocidos (`[NOMBRE`, `TU_TOKEN`...) no lo cazaba — el mismo modo de fallo
que esta skill le prohibe a los demas: el detector solo mira donde le sembraron el defecto.
Ahora F3 caza la CLASE, en DOS niveles de confianza MEDIDOS contra los 12 productos reales:
verbo de encargo (AQUI VA, PONER, FALTA, COMPLETAR, REEMPLAZAR) = rojo si el producto esta
activo; corchete en mayusculas sostenidas = DUDA, porque 3 de cada 4 eran plantilla viva del
motor de Producto en Segundos ([CATEGORIA], [NOMBRE ASESORA]) y un auditor que acusa 3 falsos de
4 le ensena al dueno a ignorarlo. El corchete de variable en minusculas ([total]) no dispara.
F3 mira las HOJAS DE TEXTO, no el JSON crudo: aplicado al crudo, el `[` que abre un array
fabricaba falsos positivos en los dos disparadores. Mismo criterio en la zona de agentes y
tareas de IA. Autoprueba: 30 defectos + 7 pruebas de comportamiento.
NOTA DE PROCESO: el turno que iba a escribir esta entrada se corto por un AbortError del canal
de permisos, y la skill quedo con el codigo de GCA1.5 y el SKILL.md diciendo GCA1.4 — el censo
diario no habria visto la edicion. Leccion: la version se escribe en el MISMO comando que el
ultimo cambio de codigo, no en uno posterior. -->
<!-- skill v1.4 (GCA1.4) — 2026-08-22 — auditoria golden-skill-auditor (850 PLATA), pasada
fresca. Lo grave era del MISMO tipo que esta skill le prohibe a los demas: (1) B7 y J2 estaban
declarados en el catalogo como controles automaticos y NO aparecian en la tabla de cobertura —
invisibles en el informe, gemelo exacto del hallazgo I4 que arreglo el Centro de Mando en
GCA1.1; ahora los dos se declaran, y J2 dice cuantos hallazgos silencio el libro. (2) La
plantilla de references/informe.md estaba VIEJA respecto al codigo: no contemplaba las secciones
"que cambio desde la corrida anterior" ni "ya decidido por el dueno", asi que quien la siguiera
entregaba un informe sin el diff ni las decisiones. (3) El helper `escapado()` estaba muerto Y
media DISTINTO que el codigo real (doble codificacion) — un helper que mide distinto es una
trampa para el proximo editor, no una comodidad: borrado, con la formula unica documentada.
(4) La cifra de la autoprueba decia 29 en SKILL.md y en controles.md y son 30 + 6. (5) El ns
real del espacio de Golden salio de los ejemplos (estandar 5: nada de IDs de cuenta en una skill
que se comparte) y la receta del libro de decisiones dejo de estar duplicada: vive solo en el
bloque J. (6) Nueva seccion "Conexion con el ecosistema" (estandar 9): cada cierre se reporta al
Centro de Mando, haya hallazgos o no, y se declaran las dependencias. (7) La cobertura se
imprime ordenada por control, e `import subprocess` muerto fuera. -->
<!-- skill v1.3 (GCA1.3) — 2026-08-21 — re-auditoria: los arreglos de GCA1.2 metieron sus
propios defectos, encontrados probando la skill contra casos que se saben malos. (1) ROBUSTEZ:
un endpoint que respondia con error (dict en vez de lista) tumbaba la auditoria entera con un
traceback — un 500 puntual de la API costaba el informe completo; ahora se declara la zona como
no medida y se sigue (control B7). (2) El asset de asistentes esperados ausente reventaba igual:
ahora degrada. (3) La regla escrita "una decision sin motivo y sin fecha no se acepta" NO la
aplicaba el codigo: se aceptaba en silencio y se imprimia "(sin motivo)". Ahora detiene la
corrida, y avisa de las decisiones sin `reabrir_si`. (4) El handoff descartaba las dudas
accionables: 5 hallazgos con accion concreta quedaban fuera del paquete; ahora abren el
documento como "preguntas que hay que contestar antes de tocar", con su clave para el libro.
Autoprueba: 30 defectos + 6 pruebas de comportamiento. -->
<!-- skill v1.2 (GCA1.2) — 2026-08-21 — auditoria golden-skill-auditor (874/1000) mas
simulacion de cliente: la skill diagnosticaba bien y COMUNICABA mal. Seis arreglos.
(1) LIBRO DE DECISIONES `--decisiones`: cada hallazgo tiene clave estable control|objetivo y lo
que el dueno ya resolvio sale aparte con motivo y fecha — antes cada corrida repetia los mismos
40 hallazgos, incluido uno que FER ya habia descartado. (2) SEVERIDAD POR NEGOCIO: un producto
huerfano CON anuncios es rojo y SIN anuncios es duda; era el criterio del dueno y no estaba en
codigo. (3) DIFF `--anterior`: que se movio desde la corrida pasada, con alerta si un campo
cruzo el techo. (4) B6 asistentes ESPERADOS contra instalados (assets/asistentes-esperados.json),
que es lo unico que contesta "esta completa esta instalacion". (5) HANDOFF `--handoff`: paquete
de correccion agrupado por la skill duena de cada campo. (6) Cerrada la contradiccion del techo
entre SKILL.md, controles.md y el codigo — una sola verdad, con los dos umbrales medidos — y
documentados los dos assets. Autoprueba de 29 a 30 defectos mas 4 pruebas de comportamiento
(negocio, libro, diff). -->
<!-- skill v1.1 (GCA1.1) — 2026-08-21 — auditoría golden-skill-auditor: I4 (controles.md:122,
"ausencia no es prueba") estaba definido pero auditar.py nunca lo reportaba en la cobertura —
quedaba invisible en el informe final, justo el modo de fallo que esta skill le prohíbe al
bloque D. Se agregó self.cubre("I4", ...) en bloque_i. También se documentó B1b en
controles.md (existía en el código sin entrada en el catálogo) y se reordenó F12/F13 a orden
numérico. Ver detalle completo debajo. -->
<!-- skill v1.0 (GCA1.0) — 2026-08-20 — versión inicial declarada por el Centro de Mando: la
skill nació sin CHANGELOG y sin número, y sin versión el censo diario no puede ver que alguien
la editó. -->

**Versión:** `GCA1.8`

Auditar aquí significa **medir el estado real del servidor contra el estándar**, no leer la
configuración y opinar. Nada se da por bueno sin haberlo contado, y el informe se entrega en
cobertura (universo, revisados, fallas), jamás en veredicto.

**Frases prohibidas en todo lo que salga de esta skill:** "quedó perfecto", "todo bien",
"está listo", "debería funcionar". Si algo no se pudo verificar, se declara como no verificado.

## Lo que esta skill audita, y lo que no

| Audita | No audita |
|---|---|
| La INSTALACIÓN: campos, asistentes, disparadores, interruptores, integraciones | Las conversaciones del día (eso es `golden-chatea-operacion`) |
| El CONTENIDO de cada prompt de producto, su ortografía y su coherencia | Escribir o corregir la config (eso es la familia `golden-chatea-pro-config-*`) |
| Lo que la config DICE que va a pasar | Lo que el bot respondió de verdad ayer |

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
python3 $S/autoprueba.py                      # primero SIEMPRE
python3 $S/auditar.py <DUMP.json> \
    --decisiones <espacio>-decisiones.json \  # lo ya resuelto no se vuelve a gritar
    --anterior   <DUMP-de-la-corrida-pasada.json> \
    --handoff    paquete-correccion.md \
    --json       hallazgos.json
```

Las cuatro banderas son opcionales y ninguna es decorativa:

| Bandera | Para qué |
|---|---|
| `--decisiones` | El **libro de decisiones**. Lo que ya resolviste sale aparte, con su motivo y su fecha, y no vuelve a contarse entre lo pendiente. Sin esto, la corrida número tres son los mismos 40 hallazgos y dejas de leerla. |
| `--anterior` | **Qué se movió** desde la última auditoría: campos creados, borrados y editados con su delta. Es lo que convierte la foto en vigilancia. |
| `--handoff` | El **paquete de corrección** agrupado por la skill dueña de cada campo, listo para pasarlo al chat que sí escribe. |
| `--json` | Todo en crudo, para encadenar con otra herramienta. |

**La autoprueba va primero y no se salta.** Fabrica un espacio que se SABE roto (**30 defectos
sembrados más 11 pruebas de comportamiento**, entre ellos los falsos negativos que dos
verificaciones adversariales encontraron) y exige que el auditor los encuentre todos. Un auditor que sale en verde contra un
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
