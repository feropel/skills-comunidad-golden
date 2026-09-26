---
name: golden-blindaje
description: >-
  Golden Group — AUDITORÍA DE SEGURIDAD DEL PROPIO ENTORNO DE AGENTES. Revisa ~/.claude
  completo: credenciales escritas a mano en skills y agentes, reglas de permiso demasiado
  abiertas, hooks inyectables o con salida de red, MCP con tokens en texto plano, blindaje
  de las skills golden y caché de sesión que guardó secretos devueltos por una API. Corre
  100% LOCAL, sin salida de red y sin subir nada a ningún servidor. Úsala SIEMPRE que el
  usuario quiera: auditar la seguridad de su Claude o de sus agentes, "revisa mi
  configuración", "tengo tokens expuestos", "es seguro mi setup", "auditá mis MCP", "revisá
  mis permisos", "qué tan expuesto estoy", "limpia la caché de sesiones", o antes de
  compartir/sincronizar skills al marketplace o de darle acceso a alguien más al equipo.
  Dispara también de forma preventiva tras conectar un MCP nuevo, instalar una herramienta
  de terceros o agregar un hook.
---
<!-- Historial completo de esta skill: references/changelog.md (1 actas, mudadas el 2026-09-05). El cuerpo se paga en cada activación; el acta no. -->
# Golden Blindaje — auditoría del entorno de agentes


**Versión:** `GB1.10` · Fábrica: chat centro de mando. Blindaje propio: `chflags uchg` (estándar de la casa).

Hay una capa que ninguna herramienta de seguridad de código mira: **la configuración
con la que corren los agentes**. Ahí viven los tokens de Shopify, Meta, Stripe y
Supabase, los permisos que deciden qué se auto-aprueba, y los hooks que se ejecutan
solos antes de cada comando. Esta skill audita esa capa.

## Por qué es propia y no una herramienta de terceros

Se evaluaron las dos alternativas conocidas (jul-2026) y **se descartaron las dos**:

- Una manda el contenido íntegro de tus archivos de configuración a una API externa
  si activas una bandera cuyo nombre no lo sugiere.
- La otra exige token, no tiene modo sin conexión y **ejecuta los comandos de tu
  configuración MCP**, o sea que levanta tus servidores con los tokens vivos.

El problema de fondo: **una herramienta que busca secretos es el vehículo perfecto
para sacarlos**. Por eso esta corre local por construcción.

> **Garantía de diseño:** `chequeo.py` no importa `requests`, `urllib`, `http` ni
> `socket`. No hay forma de que mande nada afuera. Verificable en 5 segundos:
> `grep -nE "^import |^from " scripts/chequeo.py`

## Cómo se usa

```bash
python3 ~/.claude/skills/golden-blindaje/scripts/chequeo.py
```

Opciones:

| Bandera | Para qué |
|---|---|
| `--json` | Salida estructurada, para encadenar con otra skill o guardar histórico |
| `--cache-dias N` | Umbral de caché vieja (por defecto 15) |

Termina en `0` si no hay nada ALTO, en `1` si sí. Sirve para automatizarlo.

**Si el script falla en vez de correr** (python3 no está en el PATH, permiso denegado, error de
sintaxis tras una edición): no te detengas. Audita a mano con lo que ya sabe esta skill —
`grep -rnE` de los patrones de la tabla de `SECRET_PATTERNS` (arriba en `scripts/chequeo.py`)
sobre `skills/ agents/ commands/ hooks/`, más lectura directa de `settings.json` y
`settings.local.json` para las reglas de `permissions.allow` y los `hooks`. Es más lento, pero
el chequeo manual cubre las mismas 6 áreas.

## Flujo (qué hace el agente, en orden)

1. **Corre el script** con el comando de arriba. Si el usuario no dio bandera, corre sin
   `--json` (reporte legible); usa `--json` solo si el resultado se va a encadenar con otra
   skill o guardar histórico.
2. **Verifica cada ALTO abriendo el archivo o la regla señalada** antes de reportarlo como real
   — el reporte da tipo y ubicación, nunca el valor; el valor solo se ve abriendo el archivo. Un
   hallazgo sin verificar se reporta como "por confirmar", no como hecho.
3. **Presenta el reporte completo con la tabla de triage** (ALTO/MEDIO/BAJO/DESCARTADO, ver más
   abajo) — nunca resumas solo los ALTO: los MEDIO y BAJO sin mostrar son la fuga #2 de "Los 5
   errores" más abajo.
4. **No apliques ningún arreglo sin que el usuario lo pida explícitamente.** Esta skill
   DIAGNOSTICA; no rota credenciales, no edita `settings.json`, no borra hooks ni caché por su
   cuenta — son cambios de seguridad/configuración del propio agente y el estándar de la casa
   exige permiso explícito para tocarlos (ver protocolo de triage: cada nivel dice la ventana,
   no autoriza el arreglo automático). Si el usuario pide "arréglalo", aplica el arreglo
   concreto que ya trae cada hallazgo y muéstrale el diff antes de guardarlo (regla #1 de
   "Los 5 errores").
5. **Si algo se descarta por falso positivo, documenta el porqué** en la respuesta (archivo +
   motivo) — un descarte sin razón escrita obliga a re-investigar el mes siguiente.

**Definición de terminado:** el script corrió hasta el final (exit 0 o 1, nunca se cortó a
medias), el usuario vio los hallazgos de los 3 niveles con su ventana, cada ALTO quedó verificado
o marcado "por confirmar", y ningún arreglo se aplicó sin pedirlo el usuario.

## Qué revisa (6 áreas)

### 1 · Secretos escritos a mano
Busca credenciales con **formato real** (prefijo + longitud) en skills, agentes,
comandos, hooks, plugins y tareas programadas: Shopify, Stripe, GitHub, OpenAI,
Anthropic, Google, AWS, Slack, Meta y JWT.

**Es el chequeo más importante**, porque las skills golden se sincronizan al
marketplace: un token adentro **se publica con la skill**.

### 2 · Permisos
Detecta reglas que auto-aprueban sin confirmación (`Bash(*)`, `sudo`, `rm`,
descargar-y-ejecutar, `Write(*)`), y avisa si el modo sin confirmaciones está activo
sin guardián que lo respalde.

### 3 · Hooks
Los hooks **corren solos** antes o después de cada herramienta: es el punto más
sensible del sistema, porque no necesitan que el modelo coopere. Se revisa que
ninguno haga salida de red, que ninguno descargue-y-ejecute, que apunten a archivos
que existan, y que **no sean escribibles por otro usuario** del equipo.

### 4 · MCP
Verifica que el archivo de credenciales sea `600` (solo tú lo lees), busca tokens en
texto plano y detecta servidores que descarguen algo al arrancar.

### 5 · Blindaje
Cuenta cuántas skills `golden*` (SIN exigir guion: golden360 también se juzga) están con `chflags uchg` y cuáles quedaron abiertas.
Una skill abierta mientras se edita es normal; olvidada, no.

**Excepciones por diseño** (`SIN_BLINDAJE_POR_DISENO` en `scripts/chequeo.py` — esa lista en el
código es LA fuente de verdad; esta prosa la resume): una skill que una rutina programada
ESCRIBE sola, o que su fábrica decidió dejar abierta, va sin `uchg` a propósito. Blindarla no la
protege: hace que la rutina falle en silencio. Hoy la lista tiene DOS entradas:
`golden-copywriting` (la rutina `copywriting-tendencias-8-dias` le escribe su propio
`~/.claude/skills/golden-copywriting/references/tendencias-vivas.md` cada 8 días — ese archivo
vive en golden-copywriting, no en esta skill) y `golden-chatea-operacion` (política de su
fábrica, 22-ago: sin blindar hasta validar el offset horario contra un país distinto de
Colombia; la primera corrida real de otro país levanta la excepción). Para esas skills el
chequeo invierte el semáforo: avisa en ALTO si aparecen blindadas. Cuando una rutina nueva
empiece a escribir dentro de una skill (o una fábrica declare su excepción), añádela al conjunto
del script Y a esta prosa — las dos listas se desincronizan en silencio si solo se toca una.

**La SEGUNDA tabla de excepción es `EXCEPCIONES_PARCIALES`** (vive SOLO en `chequeo.py` — no hay
cuerpo gemelo `censo-ligero.py`: ese archivo nunca se construyó y GB1.7/GB1.8 lo dejaron pendiente
sin cerrarlo; GB1.9 retira la promesa falsa en vez de seguir arrastrándola): archivos SUELTOS
escribibles por diseño dentro de skills que SÍ van blindadas — hoy,
`golden-investigacion-mercado/scripts/fuentes_baseline.json` (el baseline que su propio script
actualiza; su exención está declarada también en el sello G5.12 de esa skill — regla de los dos
lugares, la de la skill DUEÑA del archivo, que sigue vigente). Al agregar una excepción nueva,
tócala en `EXCEPCIONES_PARCIALES` y en esta prosa. Límite declarado del medidor: el directorio RAÍZ
de una skill no se juzga (los subdirectorios sí) — una inyección en raíz abierta la caza la corrida
siguiente.

**Desblindar son dos pasos, no uno** (medido el 2026-08-19): con el directorio inmutable,
`chflags -R nouchg` no alcanza. El orden que funciona es
`chflags nouchg <skill> && chflags -R nouchg <skill> && chmod -R u+w <skill>`; el blindaje
también deja los archivos en modo `444`, así que sin el `chmod` la escritura sigue fallando.

### 6 · Caché de sesión ← el punto ciego real
Los resultados de herramientas se guardan **tal cual llegan de la API**. Si una
consulta devolvió un token, ese token queda en disco. Ninguna herramienta de terceros
mira acá porque no lo considera "configuración".

## Las excepciones se conceden al ARCHIVO, nunca al FORMATO

`es_falso_positivo()` filtra ruido, y todo filtro de ruido puede convertirse en alfombra.
La regla dura, con su banco: **una credencial con prefijo del emisor** (`shpat_`,
`sk_live_`, `ghp_`, `sk-ant-`, `AKIA`, `xox…`, `AIza`, `EAA`) **no se silencia jamás por
el contexto** — ni por vivir en un `.md`, ni por estar en `/references/`, ni por tener
cerca una etiqueta HTML o la palabra "detecta". Solo dos cosas la callan, y las dos miran
al valor mismo, no a lo que lo rodea: que esté dentro de un `data:image/…;base64` (dato
binario, prueba dura) o que el valor sea relleno declarado (`PLACEHOLDER`).

**El ORDEN es parte de la regla, no un detalle de implementación.** La guarda va en
segundo lugar y solo detrás de una prueba DURA: que el valor esté *dentro* de un blob
base64. Una **mención** de imagen (`logo.png`, `@font-face`) no prueba nada sobre un
token que aparece 200 caracteres después. Mientras la guarda corrió detrás de ese filtro,
un simple enlace Markdown a un `.png` dos líneas más arriba la apagaba entera — y 45 de
los 599 `.md` del arsenal traen ese contexto. **Una guarda declarada infalible que corre
detrás de un filtro de contexto no es infalible: se apaga con ese filtro.**

Los patrones **sin** prefijo de emisor también quedan cubiertos: `sk-` de OpenAI, y el
**JWT con firma entera** (43 caracteres en base64url) — un ejemplo de documentación
trunca la firma, un JWT vivo no. Importa porque un `service_role` de Supabase *es* un
JWT: salta RLS y da acceso total a la base.

Medido el 2026-09-05: antes de esta guarda, **12 de 12 tokens vivos sembrados en un `.md`
quedaban silenciados**; y con la guarda mal ordenada, otros **12 de 12** volvían a
silenciarse con un enlace a una imagen cerca. Importa aquí más que en ninguna otra skill, porque las skills SON
`.md` y **el repo es PÚBLICO**: este es el chequeo que impide publicar un token.

`DOC_CONTEXT` sigue vivo, pero ya solo alcanza a los patrones sin prefijo de emisor
(JWT y familia), que son los que de verdad aparecen como ejemplo en material didáctico.

Banco de regresión: `python3 scripts/autoprueba_falsos_positivos.py` (30 casos, salida
0 = pasa). **Se corre después de tocar `DOC_CONTEXT`, `PLACEHOLDER` o
`FALSE_POSITIVE_CONTEXT`.** Nunca se ensancha una de esas listas para que un hallazgo
real deje de aparecer: eso se resuelve con un control, no con una excepción.

## Los dos falsos positivos que ya están resueltos

Un reporte con ruido se deja de leer, y entonces no protege nada. Estos dos se
detectaron en la primera corrida real y están filtrados:

1. **Imágenes en base64.** Un PNG incrustado contiene la secuencia `EAA`, que es el
   prefijo de los tokens de Meta. Sin filtro, cada logo se reporta como credencial.
2. **Documentación sobre secretos.** Una skill que enseña a detectar credenciales
   (`cyber-neo`) lleva ejemplos y expresiones regulares en sus referencias. No son
   fugas, son el material didáctico.

**Regla al leer el reporte:** verifica el hallazgo **abriendo el archivo** antes de
rotar una llave o borrar algo. Un dato mal leído hace tomar decisiones equivocadas.

## Regla de oro del reporte

**Nunca se imprime el VALOR de un secreto, solo su TIPO y DÓNDE está.** Un reporte
que contiene las credenciales es tan peligroso como las credenciales.
Por lo mismo: si guardas la salida con `--json`, trátala como archivo sensible y
bórrala al terminar.

## Qué hacer con cada nivel (protocolo de triage)

La ventana es **dura, no orientativa**. Un hallazgo sin fecha de arreglo es un hallazgo
que no se arregla.

| Nivel | Significa | Ventana | Qué se hace |
|---|---|---|---|
| **ALTO** | Credencial expuesta o puerta abierta | **menos de 24 h** | rotar la credencial y cerrar la puerta hoy. Si algo está publicado o en producción, esto va antes que cualquier otra tarea del día |
| **MEDIO** | Riesgo real que depende del contexto | **esta semana** | es explotable pero necesita condiciones específicas. Se agenda con fecha, no "cuando se pueda" |
| **BAJO** | Higiene y acumulación | **este mes** | reduce superficie de ataque. Se hace en bloque, no de a uno |
| **DESCARTADO** | Falso positivo verificado | — | **se documenta el porqué**, con archivo y motivo. Un descarte sin razón escrita obliga a volver a investigarlo el mes siguiente |

### Los 5 errores que hacen inútil una auditoría

1. **Aplicar arreglos sin leer el diff.** El parche se revisa entero antes de aplicarlo,
   incluso el que propone Claude. Sobre todo el que propone Claude.
2. **Ignorar los MEDIO y BAJO.** Se acumulan y terminan siendo el camino de entrada.
3. **Correr la auditoría solo cuando hay una entrega.** Si solo se corre antes de publicar,
   se convierte en un trámite que se aprueba solo.
4. **No documentar lo que se descartó.** Ver la fila DESCARTADO de arriba.
5. **Creer que esta skill lo cubre todo.** Es **una sola capa**: revisa el ENTORNO.
   No revisa el código de una app (eso es `cyber-neo`) ni prueba la app corriendo.
   Leer el código dice dónde *podría* fallar; solo probarlo dice si *falla*.

## MCPs y addons de terceros: las dos preguntas antes de conectar

Todo servidor MCP corre con tus permisos. Antes de añadir uno al ecosistema:

**1 · A dónde manda datos.** Abrir el fuente y buscar `requests`, `urllib`, `http`,
`telemetry`, `posthog`, `analytics`. Ojo con el **fail-open**: no basta con que el
consentimiento venga en `default=False`, hay que verificar qué pasa cuando la preferencia
**no se puede leer**. Caso real (`blender-mcp`, auditado 2026-07-27): declara
`telemetry_consent default=False`, pero su bloque de respaldo asigna `consent = True` si
no encuentra las preferencias. **La única forma segura de apagarlo es la variable de
entorno**, no la casilla de la interfaz.

**2 · Si ejecuta código arbitrario.** Buscar `exec(`, `eval(`, `subprocess`, `os.system`.
Si lo hace (y muchos MCP útiles lo hacen), no se descarta por eso — se le ponen barandas:
nunca sobre un archivo de producción, siempre con copia guardada antes, y jamás apuntando
a una carpeta con datos del negocio.

## Cuándo correrla

- **Antes de sincronizar skills al marketplace** — es lo que las publica a los alumnos
- Después de **conectar un MCP nuevo** o instalar algo de terceros
- Después de **agregar un hook**
- Mensualmente, como rutina

## Encadena con
- `cyber-neo` → audita el CÓDIGO de una app; esta audita el ENTORNO. Se complementan.
- `golden-skill-auditor` → califica la CALIDAD de una skill; esta revisa su seguridad.
- `golden-archivos` → si la limpieza de caché se vuelve un tema de orden general.

## Changelog
- **GB1.10** (2026-09-13, auditoría `golden-skill-auditor`) — GB1.9 retiró de `SKILL.md` la
  promesa falsa de que `EXCEPCIONES_PARCIALES` tenía un "cuerpo gemelo" `censo-ligero.py`,
  pero dejó sin tocar el mismo claim dentro del CÓDIGO: el docstring de `uchg_arbol` en
  `chequeo.py:151` seguía diciendo "CUERPO BYTE-IDENTICO en censo-ligero.py y chequeo.py" —
  archivo que `find` sobre `~/.claude` y `~/.golden` confirma que solo existe como respaldo
  (`skill-backups/censo-ligero.py.bak*`), nunca en producción. Se corrige el comentario para
  que `chequeo.py` quede declarado única implementación, igual que ya decía la prosa. Sin
  cambios de comportamiento: `autoprueba_falsos_positivos.py` sigue 30/30 y `chequeo.py`
  corrido completo hoy sigue en exit 0 (2636 archivos escaneados, 0 ALTO, 36 skills
  blindadas / 1 abierta, guardián activo). Nota aparte, sin tocar código: el inventario
  marca como "no existen" un puñado de rutas tipo carpeta/archivo que en realidad son
  nombres de prueba dentro del banco de casos de `autoprueba_falsos_positivos.py` (para
  simular dónde podría aparecer un token) — no son archivos que esta skill declare como
  propios, así que no hace falta crearlos ni tocarlos.
- **GB1.9** (2026-09-06, auditoría `golden-skill-auditor`) — Cierra el pendiente que GB1.7 dejó
  declarado y GB1.8 arrastró sin tocar: `EXCEPCIONES_PARCIALES` decía tener un "cuerpo gemelo"
  `censo-ligero.py` (en `SKILL.md` y en el docstring de `uchg_arbol` en `chequeo.py`), pero ese
  archivo NUNCA existió en disco (verificado con `find` sobre `~/.claude` y `~/.golden`) y ninguna
  autoprueba lo comparaba — la "regla de los dos lugares" no se estaba verificando por nada. Se
  retira la promesa falsa en vez de seguir citándola: `EXCEPCIONES_PARCIALES` queda declarada como
  única implementación en `chequeo.py`. También se borró la carpeta de bytecode compilado
  (`__pycache__`, dentro de `scripts`) — no debe vivir en una skill que se sincroniza al
  marketplace. Sin cambios de
  comportamiento en la detección: `autoprueba_falsos_positivos.py` sigue 30/30 y `chequeo.py`
  corrido completo hoy sigue en exit 0 con los mismos hallazgos reales del entorno.
- **GB1.8** (2026-09-05) — Cierra los tres huecos que el **verificador adversarial**
  encontró en GB1.7 el mismo día. (1) La guarda `PREFIJO_EMITIDO` corría en TERCER lugar,
  detrás de `FALSE_POSITIVE_CONTEXT`, cuyo patrón incluye `\.png`, `\.jpg`, `\.woff` y
  `@font-face`: un enlace Markdown a un `.png` dos líneas más arriba silenciaba **13 de 13
  patrones**, la guarda incluida, y 45 de los 599 `.md` del arsenal ya traen ese contexto
  hoy. Se sustituye por `EN_BLOB_BASE64`, prueba DURA (el valor está *dentro* del blob,
  no hay más que base64 entre el marcador y él), y la guarda sube a segundo lugar.
  (2) `sk-` de OpenAI estaba fuera de la guarda, que solo cubría `sk-ant-`. (3) El **JWT**
  quedaba exento en `.md` — y un `service_role` de Supabase es un JWT que salta RLS; ahora
  `JWT_CON_FIRMA` lo protege por FORMA (firma de 27+ caracteres: el ejemplo la trunca, el
  vivo no). `PLACEHOLDER` deja de correr antes de la guarda y se sustituye por
  `RELLENO_INEQUIVOCO`, del que se saca "TEST" (un token vivo puede llevarlo por azar;
  `sk_test_`/`pk_test_` se tratan por prefijo completo). Banco de 18 a **30 casos**: 12
  fallas antes, 0 después. **LA CLASE: una guarda declarada infalible que corre detrás de
  un filtro de contexto no es infalible — se apaga con ese filtro. El orden de evaluación
  es parte de la regla.**
- **GB1.7** (2026-09-05) — Barrido de listas de excepción del arsenal (Centro de Mando).
  **Hallazgo enterrado, medido y cerrado:** la exención documental `DOC_CONTEXT` se
  concedía a CUALQUIER archivo `.md` o bajo `/references/`, y su patrón incluye piezas
  que en Markdown son constantes (`<[a-z_]+>` casa `<div>`/`<br>`, `\.\.\.` casa unos
  puntos suspensivos, `detect` casa "detecta"). Con eso, **12 de 12 credenciales VIVAS
  sembradas en un `.md` se silenciaban** — y las skills son `.md` en un repo público.
  Se instala la guarda `PREFIJO_EMITIDO`: un valor con prefijo del emisor nunca es falso
  positivo por contexto, y la guarda está puesta donde no se puede apagar ensanchando
  `DOC_CONTEXT`. Nace `scripts/autoprueba_falsos_positivos.py` (18 casos) y se corre
  antes y después: 12 fallas antes, 0 después. **LA CLASE: una exención se concede al
  archivo que la justifica, nunca a un formato entero; "es un .md" no es una razón.**
  Pendiente declarado en esta misma corrida: el SKILL.md cita `censo-ligero.py` como
  cuerpo gemelo de `chequeo.py` y una autoprueba que los compara — **ninguno de los dos
  existe en disco** (verificado con `find` sobre `~/.claude` y `~/.golden`). La regla de
  los dos lugares que la prosa promete NO está siendo verificada por nada.
- **GB1.4** (2026-08-24) — Barrido total del arsenal (Centro de Mando): sincronizada la prosa de
  "Excepciones por diseño" con `SIN_BLINDAJE_POR_DISENO` de `chequeo.py` — la prosa nombraba solo
  a `golden-copywriting` cuando el código lleva DOS exentas (se suma `golden-chatea-operacion`,
  política de su fábrica del 22-ago). El script queda declarado fuente de verdad y la regla nueva
  exige tocar ambos lugares al agregar excepciones. `chequeo.py` sin cambios (ejecutado completo
  hoy: exit 0, 1672 archivos escaneados, 0 hallazgos ALTO).
- **GB1.3** (2026-08-23) — Estándar 9 (Centro de Mando): agrega la declaración de que los cambios
  relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. Sin cambios de
  comportamiento en `chequeo.py`.
- **GB1.2** (2026-08-21) — Auditoría `golden-skill-auditor`: agrega la sección **Flujo** con los
  5 pasos explícitos del agente (correr, verificar cada ALTO abriendo el archivo, presentar el
  triage completo, no aplicar arreglos sin pedirlo el usuario, documentar descartes) y la
  **definición de terminado**; documenta qué hacer si el script no corre (chequeo manual con los
  mismos patrones); desambigua la cita a `tendencias-vivas.md` como archivo propio de
  `golden-copywriting`, no de esta skill; documenta el blindaje propio (`chflags uchg`). Sin
  cambios de comportamiento en `chequeo.py` más allá de un comentario aclaratorio.
- **GB1.1** (2026-07-27) — Filtro del PDF "Claude Security setup" (Joaco Cierra) y de la
  auditoría de `blender-mcp`. Se hornea el **protocolo de triage con ventanas duras**
  (ALTO menos de 24 h · MEDIO esta semana · BAJO este mes · DESCARTADO se documenta), los
  **5 errores que hacen inútil una auditoría**, y la sección de **MCPs de terceros** con
  las dos preguntas obligatorias (a dónde manda datos, si ejecuta código arbitrario) más
  el patrón **fail-open de consentimiento** encontrado en `blender-mcp`.
  La herramienta del PDF (Claude Security) NO se adoptó: su beta pública es solo para plan
  **Enterprise**, y su documentación oficial ahora **prohíbe** escanear repos de terceros
  u open source, que era justo el atajo gratuito que prometía el PDF.
- **GB1.0** (2026-07-23) — Creación. Nace de auditar dos herramientas de terceros
  (`agentshield` y `snyk/agent-scan`) y **descartar las dos** por enviar datos afuera:
  se conserva el método y se implementa local. En la primera corrida real sobre el
  entorno Golden encontró un JWT cacheado en un resultado de consulta y 82 archivos de
  caché con más de 15 días, con 0 hallazgos ALTOS tras filtrar los falsos positivos.

## Fronteras y desambiguacion

NO usar para: auditar el código de una app o web (eso es cyber-neo), calificar la calidad de una skill (golden-skill-auditor), ni para revisar la seguridad de una tienda Shopify o un portal (eso va por su chat correspondiente).

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-blindaje
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-blindaje
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-blindaje`

Historial completo en `references/changelog.md`.
