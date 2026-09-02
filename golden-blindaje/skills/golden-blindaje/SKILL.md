---
name: golden-blindaje
description: >-
  Golden Group — AUDITORÍA DE SEGURIDAD DEL PROPIO ENTORNO DE AGENTES. Revisa
  ~/.claude completo: credenciales escritas a mano en skills y agentes, reglas
  de permiso demasiado abiertas, hooks inyectables o con salida de red, MCP con
  tokens en texto plano, blindaje de las skills golden y caché de sesión que
  guardó secretos devueltos por una API. Corre 100% LOCAL, sin salida de red y
  sin subir nada a ningún servidor.
  Úsala SIEMPRE que el usuario quiera: auditar la seguridad de su Claude o de
  sus agentes, "revisa mi configuración", "tengo tokens expuestos", "es seguro
  mi setup", "auditá mis MCP", "revisá mis permisos", "qué tan expuesto estoy",
  "limpia la caché de sesiones", o antes de compartir/sincronizar skills al
  marketplace o de darle acceso a alguien más al equipo. Dispara también de
  forma preventiva tras conectar un MCP nuevo, instalar una herramienta de
  terceros o agregar un hook.
  NO usar para: auditar el código de una app o web (eso es cyber-neo), calificar
  la calidad de una skill (golden-skill-auditor), ni para revisar la seguridad
  de una tienda Shopify o un portal (eso va por su chat correspondiente).
---

# Golden Blindaje — auditoría del entorno de agentes
<!-- skill GB1.6.1 · 2026-08-30 (CdM, verificacion externa del FILTRO sobre GB1.6) · documentado el
MATIZ SEMANTICO en el docstring de candado_muerde (muerde = "no se puede escribir", no "tiene uchg";
un 444 sin uchg tambien muerde — mejor para el proposito, pero explicado para el depurador futuro) y
simplificada la tupla redundante (PermissionError subclase de OSError). El FILTRO verifico ademas el
caso duro: huella intacta en 4 skills incl. 2 ABIERTAS donde el open SI tiene exito, y leyo que el
probe solo corre tras os.path.exists (no crea SKILL.md fantasma). Sin cambio funcional. -->
<!-- skill GB1.6 · 2026-08-30 (CdM, propuesta del FILTRO) · EL CHEQUEO PASA DE LEER EL CANDADO A
PROBARLO: nueva funcion candado_muerde() en chequeo.py — append de CERO bytes (open 'ab' sin
escribir) sobre toda skill que uchg_arbol juzgue blindada; si el open NO es rechazado = hallazgo
ALTO "FALSO CANDADO". Motivo: el lote del 29-ago aplico chflags que no mordia y el chequeo por
flags no lo vio (ley: el candado se prueba, no se pone). El probe no puede tocar contenido (cero
bytes; demostrado con huella intacta sobre skill abierta). uchg_arbol NO se toco (paridad de
gemelos intacta); el censo diario sigue pasivo — el mordisco vive solo en este chequeo profundo.
Probado en ambas direcciones: copywriting (abierta) no muerde, shopify (blindada) muerde. -->
<!-- skill GB1.5.2 · 2026-08-25 (centro de mando, cierre R6): la 'prosa de las DOS listas' del sello GB1.5.1 vivía SOLO en el sello — ahora EXCEPCIONES_PARCIALES está nombrada en la sección operativa Excepciones por diseño, con su ejemplo, la regla de los dos gemelos y el límite del dir raíz. Afirmación verificada por grep antes de sellar (receta R6). -->
<!-- skill GB1.5.1 · 2026-08-25 (centro de mando, remediación R5): re-blindaje del propio chequeo.py (había quedado 644 sin uchg tras la edición de las 23:23 — la skill del blindaje era la única sin blindar del arsenal, cazada por sus DOS instrumentos); prosa actualizada a las DOS listas de excepción; uchg_arbol juzga también DIRECTORIOS (con archivos uchg y carpeta abierta se podía inyectar un archivo sin resistencia — latente, con caso al banco); guardia de paridad ahora falla CERRADO y cubre también la tabla de excepciones. -->
<!-- skill GB1.5 · 2026-08-25 (centro de mando, remediación R3/R4 del verificador de cierre): chequeo.py CAMBIÓ DE SEMÁNTICA — esto supersede al claim 'INTACTO' del sello GB1.4 y al 'sin cambios de comportamiento', que eran ciertos a su hora y quedaron viejos el mismo día: (1) blindaje por N de M nodos del árbol con la función uchg_arbol de cuerpo BYTE-IDÉNTICO al del censo (stat por archivo, SIGUE symlinks, falla CERRADO); (2) filtro golden* sin guion (golden360 entró al juicio); (3) denominador impreso ('de N juzgadas'); (4) EXCEPCIONES_PARCIALES para escribibles por diseño (fuentes_baseline.json de investigación — regla de los dos lugares); (5) shebang restaurado a la línea 1. -->

<!-- skill GB1.4 · 2026-08-24 · barrido total del arsenal (CdM): la prosa de "Excepciones por diseño" estaba desincronizada del código — decía "Hoy la lista es golden-copywriting" (una sola) cuando chequeo.py lleva DOS exentas desde el 22-ago (golden-copywriting + golden-chatea-operacion); la prosa ahora nombra las dos, declara al script como fuente de verdad y exige actualizar ambos lugares al agregar una excepción. chequeo.py INTACTO (corrido completo hoy: exit 0, 1672 archivos, 0 ALTO). -->
<!-- skill GB1.3 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->
<!-- skill GB1.2 · 2026-08-21 · auditoría golden-skill-auditor: agrega Fase 0 (flujo explícito paso a paso: correr, verificar ALTO abriendo el archivo, presentar triage, pedir permiso antes de tocar seguridad) con definición de terminado y manejo de error si el script no corre; blindaje propio documentado (chflags uchg); cita a tendencias-vivas.md desambiguada como archivo de golden-copywriting, no local -->
<!-- skill GB1.1 · 2026-07-27 · filtro del PDF Claude Security y de blender-mcp, protocolo de triage con ventanas duras, 5 errores que hacen inútil una auditoría, sección MCPs de terceros -->
<!-- skill GB1.0 · 2026-07-23 · auditoría local de ~/.claude sin salida de red · 6 áreas (secretos, permisos, hooks, MCP, blindaje, caché) -->

**Versión:** `GB1.6.1` · Fábrica: chat centro de mando. Blindaje propio: `chflags uchg` (estándar de la casa).

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

**La SEGUNDA tabla de excepción es `EXCEPCIONES_PARCIALES`** (chequeo.py y censo-ligero.py, cuerpos
gemelos): archivos SUELTOS escribibles por diseño dentro de skills que SÍ van blindadas — hoy,
`scripts/fuentes_baseline.json` de golden-investigacion-mercado (el baseline que su propio script
actualiza; su exención está declarada también en el sello G5.12 de esa skill — regla de los dos
lugares). Igual que la lista de arriba: se toca en LOS DOS gemelos a la vez, y la autoprueba del
censo los compara en cada corrida. Límite declarado del medidor: el directorio RAÍZ de una skill
no se juzga (los subdirectorios sí) — una inyección en raíz abierta la caza la corrida siguiente.

**Desblindar son dos pasos, no uno** (medido el 2026-08-19): con el directorio inmutable,
`chflags -R nouchg` no alcanza. El orden que funciona es
`chflags nouchg <skill> && chflags -R nouchg <skill> && chmod -R u+w <skill>`; el blindaje
también deja los archivos en modo `444`, así que sin el `chmod` la escritura sigue fallando.

### 6 · Caché de sesión ← el punto ciego real
Los resultados de herramientas se guardan **tal cual llegan de la API**. Si una
consulta devolvió un token, ese token queda en disco. Ninguna herramienta de terceros
mira acá porque no lo considera "configuración".

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
