## v1.14 · 2026-09-28 · auditoría golden-skill-auditor (AUDITA+ARREGLA) — FILA P59 (par vía CdM)

**Hallazgo, ya confirmado por el par leyendo el código en vivo antes de encargar el arreglo:**
`scripts/extraer.py`, función `pedir()` (línea ~170): en cualquier error HTTP (incluido un 429
de cupo agotado a mitad de una paginación) devuelve `{"_ERROR_HTTP": codigo, "_detalle": "..."}`
— un dict SIN clave `"data"`. Dos bucles de paginación usaban el mismo patrón y no distinguían
"error HTTP a mitad de camino" de "se acabaron los datos reales":

1. `listar_contactos_del_dia` (bucle de páginas 2+ del listado): `lote2 = r2.get("data")`,
   `if not isinstance(lote2, list) or not lote2: break` — un error a mitad de la paginación del
   LISTADO se veía exactamente igual que "no hay más contactos". Solo se declaraban
   `trunco_por_tope_500` y `sin_meta_last_page_no_pagina`, ninguno de los dos cubría "se cortó
   por un error real".
2. `descargar_hilo` (bucle `for pagina in range(2, ...)`): mismo patrón de corte. Un hilo cortado
   por un error HTTP se veía igual que un hilo que ya terminó; solo se declaraba `truncado`
   (comparado contra `MAX_PAG_HILO`), no un error real.

**Arreglo (antes → después, con evidencia archivo:línea):**

- `scripts/extraer.py:255-286` (`listar_contactos_del_dia`): ANTES el bucle solo miraba
  `r2.get("data")`. AHORA, antes de leer `"data"`, se comprueba
  `isinstance(r2, dict) and ("_ERROR" in r2 or "_ERROR_HTTP" in r2)`; si es cierto, se declara
  `parcial_por_error = {"pagina": ..., "codigo_http": ..., "detalle": ...}` y se rompe el bucle
  SIN sumarlo a "paginas_traidas". Ese campo se agrega a `_listado_paginacion` (nueva clave
  `parcial_por_error`, `None` cuando no aplica), distinto de `truncado_por_tope_500` y de
  `sin_meta_last_page_no_pagina`.
- `scripts/extraer.py:349-372` (`descargar_hilo`): mismo patrón. ANTES `lote = r.get("data")`
  sin distinguir error de fin de datos. AHORA se detecta el error antes de leer `"data"` y se
  declara `parcial_por_error` en el aviso devuelto (`_avisos_de_hilo`), con razón explícita
  ("esto NO es 'el hilo terminó ahí'").
- `scripts/clasificar.py:1291-1324` (bloque `_avisos_de_hilo`): ANTES `sev_aviso = "RIESGO" if
  "TRUNC" in razon.upper() else "DUDA"`, sin caso para error real. AHORA, si el aviso trae
  `parcial_por_error`, el hallazgo `P-hilo-truncado` sale con severidad `MUERTO` (más alta que
  el `RIESGO` de un truncado normal por `MAX_PAG_HILO`), con evidencia del código HTTP y la
  página donde se cortó.
- `scripts/clasificar.py:1370-1399` (bloque `_listado_paginacion`): se agrega un bloque nuevo que
  lee `paginacion_listado.get("parcial_por_error")` y, si está presente, emite
  `P-listado-truncado`/`MUERTO` — distinto del `RIESGO` que ya existía para
  `truncado_por_tope_500`. La nota de `self.cubre("P-listado-truncado", ...)` ahora declara
  también `parcial_por_error=True/False`.

**Severidad elegida (criterio propio, pedido explícitamente por el encargo):** un truncado
normal (tope de 500 páginas, o `MAX_PAG_HILO` en un hilo) es 🟠 RIESGO — "seguimos pero
avisamos". Un corte por error real es 🔴 MUERTO — el mismo criterio que ya usa `pedir()` para el
429 general ("este barrido está INCOMPLETO, no lo informes como el día entero"), aplicado aquí
puntual por listado o por hilo: el universo/hilo queda CONFIRMADO incompleto desde esa página en
adelante, no solo "puede estar incompleto".

**2 pruebas nuevas en `scripts/autoprueba.py`** (`LISTADO-CORTE-POR-ERROR`,
`HILO-CORTE-POR-ERROR`, familia `FIXES_P59_2026_09_28`): ambas llaman al CAMINO REAL de
`extraer.listar_contactos_del_dia` / `extraer.descargar_hilo` con `extraer.pedir` monkeypatcheado
(página 1 responde 200 con datos, página 2 responde `{"_ERROR_HTTP": 429, ...}`) — no un DUMP
sintético armado a mano. Cada una confirma: (a) `parcial_por_error` se declara con la página y el
código correctos, (b) `truncado_por_tope_500`/`truncado` siguen en `False` (no fue el tope el que
cortó), (c) el hallazgo `P-listado-truncado`/`P-hilo-truncado` sale con severidad `MUERTO`.

**Sabotaje manual confirmado en las DOS capas antes de dar las pruebas por buenas:**
1. Se desactivó la detección de error en `extraer.py` (`if False and ...`) en ambos bucles →
   las 2 pruebas nuevas FALLARON (`parcial_por_error` quedaba `None`, hallazgo MUERTO no salía).
2. Restaurado `extraer.py`; se desactivó la elevación de severidad en `clasificar.py` (`if False
   and parcial_por_error`) en ambos bloques → las 2 pruebas volvieron a FALLAR (`extraer.py` sí
   detectaba el error, pero `clasificar.py` no lo convertía en MUERTO) — confirma que las pruebas
   ejercen las dos capas, no solo una.
3. Restaurado todo. Autoprueba real: **69 de 69** (antes del fix: 67/67; con cualquiera de los
   dos sabotajes activo: 67/69, ambas nuevas en FALLA).

**Matiz sobre el hallazgo original del par:** el hallazgo estaba correcto en ambos puntos citados
(función, línea, patrón). Un matiz que el encargo dejaba a criterio: para el listado, el error se
puede dar tanto en el bucle de páginas 2+ (cubierto aquí) como, en teoría, en la primera página —
pero esa primera falla ya la maneja `main()` con `sys.exit` antes de llegar a construir el DUMP
(no hay universo que declarar incompleto: no hay universo). Este fix cubre el caso real que el
par señaló: el corte A MITAD de una paginación que ya había empezado a traer datos reales.

**Verificado:** `python3 -c "import ast; ast.parse(...)"` limpio en los 4 scripts ·
`inventario.sh` sin rotas/huérfanas/dudosos · `validar_arsenal.py` (compuerta dura): **1 de 1
revisada, sana, 0 con fallo**. Backup antes de tocar nada:
`~/.claude/skill-backups/golden-chatea-operacion-20260928-010058/`. Sin blindar — sigue abierto
el pendiente de zona horaria con dueño (FER/Golden), política de esta skill.

## v1.12 · 2026-09-22 · auditoría golden-skill-auditor (AUDITA+ARREGLA)

**Único hallazgo real, con evidencia:** el comentario H1 de `SKILL.md` (el puntero de versión
que encabeza el archivo) seguía citando `v1.10` (2026-09-07) pese a que la acta `v1.11`
(2026-09-13, justo abajo) ya documentaba una corrección hecha ESE día a la línea **Versión:**
del cuerpo (`GCO1.9` → `GCO1.10`). La acta v1.11 arregló el síntoma (la línea Versión: visible)
pero no el propio marcador que la precede — la misma clase de fallo ("un puntero de versión que
no se actualiza tras el cambio que describe") reapareciendo en el OTRO puntero del mismo
archivo. Corregido: el comentario H1 ahora dice `v1.12` y resume qué cambió. Verificado tras el
arreglo (cambio de solo texto, sin tocar ningún script): `inventario.sh` sin rotas/huérfanas/
dudosos, `validar_arsenal.py` sano sin aviso, `autoprueba.py` 67/67 (cifra sin cambios, como se
esperaba de un fix que no toca código). Sin blindar — sigue abierto el pendiente de zona
horaria con dueño (FER/Golden), política de esta skill.

## v1.11 · 2026-09-13 · auditoría golden-skill-auditor (AUDITA+ARREGLA)

**Único hallazgo real, con evidencia:** la línea `**Versión:**` visible bajo el H1 (`SKILL.md`)
seguía citando `GCO1.9` (2026-09-06, "retira un carácter suelto") pese a que el propio
comentario HTML de changelog un poco más arriba y la última acta de este archivo ya declaraban
`v1.10` (2026-09-07: retiro del nombre del orquestador planeado + changelog movido aquí) — la
línea de versión nunca se actualizó tras ese cambio. Corregido: ahora dice `GCO1.10` y resume el
contenido real de esa versión. Verificado tras el arreglo: `autoprueba.py` 67/67,
`validar_arsenal.py` sano sin aviso, inventario.sh sin rotas/huérfanos/dudosos. Sin blindar —
sigue abierto el pendiente de zona horaria con dueño (FER/Golden), política de esta skill.

# Changelog · golden-chatea-operacion

> **Por qué existe este archivo (Centro de Mando, 2026-09-07).** Estas actas vivían dentro del
> `SKILL.md` como comentarios HTML: **21.526 bytes, el 58% del archivo** — el peor caso de toda
> la familia Chatea. Un comentario HTML en el cuerpo **se paga en cada activación** aunque nadie
> lo lea. No se perdió una palabra: bajaron verbatim.

## CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las 

CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 963 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare · (4) Esta skill estaba SIN BLINDAR: se le puso 'uchg' y se comprobo que el candado muerde. Para editarla: chflags -R nouchg <ruta>, y al cerrar chflags -R uchg.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo.

## skill v1.8 (GCO1.8) — 2026-09-05 — mejora sin datos nuevos sobre el pendiente de zona horaria (

skill v1.8 (GCO1.8) — 2026-09-05 — mejora sin datos nuevos sobre el pendiente de zona
horaria (a pedido de FER: "busca la forma de automejorarte y ser mil"). Investigado antes de
tocar nada: el pendiente real (offset -5h solo confirmado en Colombia) NO se puede cerrar sin
un DUMP real de otro país — no se fabricó esa evidencia. Lo que SÍ se pudo mejorar sin datos
nuevos: (1) agregado `--pais <nombre>` en `clasificar.py` (atajo sobre `--zona-horas`, tabla
`PAISES_ZONA_HORAS` con el offset ESTÁNDAR PÚBLICO de los 10 países de la plataforma, con
aviso de horario de verano para Chile/Paraguay/parte de Brasil y de ambigüedad de zona para
México/Brasil — declarado como estándar público, no como medición de Chatea, para no fingir
una confirmación que no existe); (2) 5 menciones desactualizadas de "7 países"/"otros 6"
(sobrevivientes a la corrección CdM del 2026-08-29 que subió el conteo a 10) corregidas en
SKILL.md, `references/api.md` y `clasificar.py` — las que estaban dentro de comentarios de
changelog FECHADOS se dejaron intactas (eran ciertas el día que se escribieron); (3) la
mención de `golden-chatea-360` en "Orquestación futura" aclarada como PLANEADO, no construido
— `validar_arsenal.py` la marcaba con aviso por no resolver a nada existente. 4 pruebas nuevas
en `autoprueba.py` (resuelve offset correcto, país desconocido no inventa uno, `--pais` y
`--zona-horas` son excluyentes, el cableado real de `_parsear_argv` funciona) — las 4
saboteadas a mano antes de sellar (confirmado: cambiar el offset de México en la tabla tumba
`PAIS-RESUELVE-OFFSET`, restaurado después). Autoprueba real corrida en vivo tras el cambio:
**67 de 67** confirmados. **Lo que esto NO hace:** no confirma el offset de ningún país contra
un servidor real de Chatea — la pregunta de fondo (¿reporta `last_message_at` en la hora local
de cada espacio, o en una zona fija?) sigue exactamente igual de abierta que antes. El
pendiente sigue con dueño (FER/Golden) y la skill sigue sin blindar por esa razón, no por esta
mejora.

## corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble med

corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto.

## skill v1.7 (GCO1.7) — 2026-08-22 — TERCERA auditoría golden-skill-auditor, en frío, sobre GCO1.

skill v1.7 (GCO1.7) — 2026-08-22 — TERCERA auditoría golden-skill-auditor, en frío,
sobre GCO1.6 (protocolo completo, sin reutilizar la memoria de la auditoría anterior, tal
como manda la regla v1.15 del auditor). Inventario limpio (0 rotas, 0 huérfanos, 0 dudosos,
sintaxis OK en los 4 scripts), autoprueba real corrida en vivo: **63 de 63** confirmados
(cifra idéntica a la declarada, sin drift). Grep confirmó que ningún nombre de cliente o
producto real está colado en ningún archivo (ESPACIO-REF sigue siendo el único identificador
del espacio de validación). Dos sabotajes a mano sobre hallazgos críticos de rondas
anteriores (desempate de `ts` en `invertir_hilo`, y `direccion()` con `is_bot` como texto
booleano) — los dos tumbaron la autoprueba como se esperaba, y el archivo se restauró
idéntico al original tras cada uno (diff limpio). Único hallazgo nuevo real: (1) 🟡
**SKILL.md no declaraba la conexión con el Centro de Mando de forma incondicional** — la
única mención existente (línea "si un informe de esta skill y uno de `golden-logistica-
diaria` del mismo día se contradicen... se avisa al Centro de Mando") es condicional a un
caso concreto, no la declaración general que exige la Fase 7 punto 2 del auditor. Corregido:
se agrega la sección "Conexión con el ecosistema" más abajo. Blindaje: sigue SIN blindar,
igual que en GCO1.6 — el pendiente de zona horaria (offset -5h, un solo espacio confirmado)
sigue abierto con dueño (FER/Golden), y la política de esta skill es blindar solo al cerrar
el último pendiente.

## skill v1.6 (GCO1.6) — 2026-08-22 — SEGUNDA auditoría golden-skill-auditor, en frío, sobre GCO1.

skill v1.6 (GCO1.6) — 2026-08-22 — SEGUNDA auditoría golden-skill-auditor, en frío,
sobre GCO1.5 (sin reutilizar la memoria de la primera pasada, tal como manda la Fase 6):
inventario limpio (0 rotas, 0 huérfanos, 0 dudosos, sintaxis OK en los 4 scripts), grep
confirmó que el nombre real del cliente que la primera auditoría anonimizó (ver "ESPACIO-REF"
más abajo) no reaparece en ningún archivo, y el pendiente declarado de zona
horaria (offset -5h, un solo espacio confirmado) sigue siendo honesto — nada nuevo lo
contradice ni lo cierra. Dos hallazgos NUEVOS reales, reparados con evidencia:
(1) COBERTURA: `P-sin-fecha-auditada` y `P-listado-truncado` SIEMPRE se evalúan dentro de
`Clasificador.correr()`, pero antes solo dejaban rastro en `self.cobertura` cuando
disparaban un hallazgo — un DUMP SANO (fecha bien formada, listado sin truncar) hacía que
la tabla de cobertura de la Fase 3 del informe no los mencionara en absoluto, aunque el
control sí se hubiera corrido y confirmado que todo estaba bien. Corregido: los dos se
declaran SIEMPRE en `self.cobertura`, con su estado real ("corrido" en el caso sano).
Sabotaje verificado a mano (monkeypatch de `cubre()` simulando el comportamiento anterior)
antes de sellar el fix, y nuevo test `test_cobertura_declara_sin_fecha_y_paginacion_siempre`
(`COBERTURA-SIEMPRE-DECLARA`) lo guarda en la autoprueba. (2) SECRETOS SIN EJERCER: de las
17 familias que declara `secretos.py`, 6 (ElevenLabs, JWT, Meta, Shopify, xAI, Google) nunca
se ejercían en NINGUNA prueba de `autoprueba.py` — confirmado con grep antes de tocar nada.
El docstring de `test_credenciales_extraer_py_camino_real` ya afirmaba "las 17 familias" sin
que el código lo cumpliera. Corregido: las 6 familias se agregaron a
`test_credenciales_ampliadas_en_evidencia` y a `test_credenciales_extraer_py_camino_real`,
con un valor por familia verificado a mano contra su regex real en `secretos.py` antes de
sembrarlo (no adivinado).

Cierre obligatorio: `golden-verificador` (adversarial, solo vio el estado tras estos dos
arreglos y el estándar, no cómo se construyó) encontró **7 fallas reales más**, con evidencia
citada — todas reparadas antes de sellar esta versión, ninguna dejada para después sin dueño:
(3) 🔴 **`invertir_hilo` invertía "quién habló de último" en un empate de `ts`** —
`sorted()` es estable; dos mensajes con el MISMO epoch (en segundos, la forma real medida)
conservaban el orden de entrada del servidor (descendente), dejando al mensaje MÁS NUEVO de
un empate ANTES del más viejo. Medido por el verificador end-to-end: 12 hallazgos R1/MUERTO
falsos sobre 13 contactos donde el bot SÍ cerró en el mismo segundo. Corregido con desempate
por índice original (P3: índice mayor = mensaje más viejo). (4) 🔴 **El test `P2` se
satisfacía con un comentario** — buscaba `"user_ns=user_ns"`/`"include_bot=1"` como substring
de TODO el archivo, no del código real de `descargar_hilo`; el verificador borró las tres
llamadas reales y dejó un comentario mentiroso, y la prueba anterior seguía en verde.
Corregido: ahora lee el código FUENTE REAL de `descargar_hilo` (`inspect.getsource`, sin
comentarios) y exige además que `subscriber_id` esté AUSENTE. Sabotaje verificado a mano
(mutación idéntica a la del verificador) antes de sellar: ahora sí falla. (5) 🟠
**`_avisos_de_hilo` (hilo truncado o sin `ts`) nunca llegaba al informe** — `extraer.py` lo
declaraba, pero ningún archivo fuera de `extraer.py` lo leía (0 apariciones, confirmado con
grep). Corregido: `clasificar.py` convierte cada aviso en un hallazgo `P-hilo-truncado`
(RIESGO si truncado, DUDA si es por `ts` faltante) y lo declara siempre en la cobertura. De
paso, `descargar_hilo` ahora distingue "el servidor declaró 1 página" de "el servidor no
declaró `meta.last_page`" (antes colapsaba los dos en el mismo número, igual que el hueco
que F9 ya había cerrado para el listado de contactos, pero sin el equivalente para el hilo).
(6) 🟠 **Un nombre de producto/marca real sobrevivió a la anonimización de GCO1.5** —
`clasificar.py` (comentario de `CANON_COLOR`) nombraba el producto y la marca vendidos en el
espacio real cuyo nombre GCO1.5 sí anonimizó a `ESPACIO-REF`; anonimización inconsistente en
un artefacto compartible. Generalizado a "producto capilar", sin nombrar la marca. (7) 🟠
**`redactar()` solo actuaba por nombre de llave sensible si el valor era `str`** — un secreto
bajo una llave como `token`/`api_key`/`password` que llegara como lista, dict o número
escapaba sin redactar (medido con los 3 casos). Corregido: cualquier valor no vacío bajo una
llave sensible se redacta sin importar su tipo. (8) 🟠 **`direccion()` leía cualquier texto
no vacío en `is_bot`/`from_bot` como verdadero** — `bool("0")` es `True` en Python; un
`is_bot: "0"` (serialización habitual de una API PHP/Laravel) clasificaba a un CLIENTE como
empresa, en silencio (no caía en `desconocido`, así que `P-desc` nunca lo delataba).
Corregido con un intérprete de texto→booleano ('0'/'false'/'no'/'null'/'none' = falso). (9)
🟡 **`_fecha_de` reventaba con `TypeError` si `last_message_at` llegaba como número** (epoch)
en vez de texto — tumbaba toda la Fase 1 sin capturar. Corregido: un valor no-texto se trata
como "no utilizable para este campo" (prueba el siguiente respaldo) en vez de adivinar o
reventar. Dos hallazgos del verificador quedan **declarados, no cerrados** (ver "Pendiente
real" más abajo y `references/informe.md`/`clasificacion.md`): el bloque P documentaba "13"
controles en `informe.md` cuando el catálogo real tiene 17 (corregido el número en la tabla),
y `api.md` afirmaba que la plantilla del anuncio se detecta también "por coincidencia contra
`payload.referral`" — el código nunca lo hace (`referral` solo alimenta la atribución, Q5);
corregida la frase para no prometer una verificación que no existe.

Autoprueba tras los nueve arreglos: **63 de 63** controles confirmados (57 de la primera
mitad de esta auditoría + 6 nuevos: empate de `ts` con 2 pruebas, booleano-como-texto,
avisos de hilo, `redactar` no-str, `_fecha_de` con epoch). Cada arreglo del detector se
sabotajó a mano (mutación real, no hipotética) antes de sellar, confirmando que el test
correspondiente sí muerde. Backup antes de tocar nada:
`~/.claude/skill-backups/golden-chatea-operacion-20260822-202209/`. Blindaje: se deja SIN
blindar — el pendiente de zona horaria (offset -5h confirmado en un solo espacio, sin cubrir
horario de verano ni los otros 6 países) sigue abierto con dueño (FER/Golden, cuando haya un
DUMP real de otro país), y la política de esta skill es blindar solo al cerrar el último
pendiente, no antes.

## skill v1.5 (GCO1.5) — 2026-08-22 — auditoría golden-skill-auditor: (1) ANONIMIZADO el nombre de

skill v1.5 (GCO1.5) — 2026-08-22 — auditoría golden-skill-auditor: (1) ANONIMIZADO el
nombre del espacio real usado como fuente de validación ("ESPACIO-REF" en vez del nombre real
del cliente) en SKILL.md, references/api.md, references/clasificacion.md y los tres scripts —
19 menciones. Estándar Golden #5 (cero datos de cliente en una skill que se comparte con la
comunidad) no distingue entre skill propia y cliente propio: el nombre de un negocio real no
va hardcodeado en un artefacto shareable, aunque el cliente sea de Golden. Las cifras medidas
(165 conversaciones, 486 contactos, offset -5h, 161/161 pares, etc.) se conservan intactas —
son evidencia cuantitativa, no dato identificable. (2) REESTRUCTURADO: el changelog de las
cuatro rondas de verificación adversarial de GCO1.4 (antes ~150 líneas de prosa visible entre
el H1 y la primera sección operativa) se movió a este comentario HTML, el mismo patrón que ya
usa la hermana `golden-chatea-auditoria` (ver su `SKILL.md`) y que esta skill decía seguir sin
seguirlo. Un lector nuevo llegaba a "Las cinco fases" después de wadear ~44% del archivo en
historia de reparación; ahora el cuerpo visible lleva solo la versión vigente, el pendiente
real abierto y las frases prohibidas. Ningún hallazgo ni cifra se perdió — está todo aquí abajo.
Autoprueba re-confirmada en esta auditoría: 56/56 en vivo, igual que antes del cambio.

GCO1.0 (2026-08-20) versión inicial, hermana de `golden-chatea-auditoria` (GCA1.0), mismo
patrón de versionado (número + fecha).
GCO1.1 (2026-08-21) agrega el control R6 — coherencia intra-chat (sin Dropi): compara lo que
el cliente pidió sobre un atributo concreto (color/talla/cantidad) contra el resumen final de
pedido que redacta el bot, dentro del mismo hilo, sin tocar Dropi ni Shopify.
GCO1.2 (2026-08-21) quita dos signos de apertura ¿ que se habían colado en ejemplos citados de
references/informe.md e references/clasificacion.md.
GCO1.3 (2026-08-22) sincroniza la documentación con extraer.py, que había avanzado más rápido:
el endpoint de listado de contactos por fecha quedó confirmado contra un token real (espacio
ESPACIO-REF, 2026-08-21) — es /subscribers, no filtra por fecha en el servidor; extraer.py
compensa paginando el universo completo y filtrando en cliente (detalle en references/api.md).
Pendiente: esa confirmación es de UN espacio — otro plan/versión de Chatea puede exponer un
endpoint distinto, CANDIDATOS_LISTADO se mantiene como lista, no como literal fijo.
GCO1.4 (2026-08-22) cierra 11 hallazgos (F1-F11) de una verificación adversarial contra 4 DUMPs
reales de producción del espacio ESPACIO-REF (165 conversaciones, ts epoch en el 100% de los
mensajes medidos), y luego tres rondas MÁS de verificación adversarial encontraron y cerraron
6+2+2 fallas nuevas contra los mismos 4 DUMPs.
  F1 parse_fecha lee ts epoch (segundos/ms por magnitud) además de texto — 31 hallazgos R1 que
  caían en RIESGO por "gap no medible" pasaron a su severidad real (MUERTO, gap 156-818 min).
  F2 fixtures de autoprueba invertidos a epoch real, usan `type` como campo primario (no
  `direction`). F3 SEGURIDAD: los patrones de redacción de credenciales dejaron de vivir
  duplicados entre extraer.py y clasificar.py — los dos importan de scripts/secretos.py (17
  familias, umbral SanctumBearer unificado en {20,}). F4 vocabulario de cantidad ampliado (ver
  FALLA 2 abajo). F5 compuerta de cordura con lado bajo: 0% de cierre con 10+ conversaciones
  no-dropi genera RIESGO declarado sin abortar — se activó en 3 de los 4 días reales medidos
  (0%, 0%, 0%; el cuarto, 6.67%, no activa el umbral). F6 SKILL.md/informe.md describen los TRES
  estados del denominador de la Fase 1. F7 el comando documentado incluye --modo cod|prepago.
  F8 dos afirmaciones sin artefacto ("los tres candidatos dan 404", "4 variantes de fecha
  probadas") se retiraron por no tener medición real que las respalde. F9 el listado declara en
  el DUMP (_listado_paginacion) si se truncó en el tope de 500 páginas. F10 los 6 de 56 hilos
  del 08-21 en orden no descendente ahora se ordenan bien. F11 corrige la afirmación de que
  ninguna de las dos skills lleva changelog (la hermana sí lo llevaba).

  Segunda ronda (mismo día, mismos 4 DUMPs), 6 fallas: FALLA 1 el hilo trae el histórico
  COMPLETO del contacto, no solo el día pedido — R2/R3/R4/Q4 podían acusar al bot de algo de
  OTRO día (7 hallazgos R2 citaban gaps de días distintos, uno de 818 min). Corregido con
  `_mensajes_del_dia` (filtra por _fecha) antes de esos cuatro controles; R1 y R6 siguen usando
  el hilo completo a propósito. Tras el fix: R2=0, R4=2 en la corrida final. FALLA 2 el
  vocabulario de cantidad ampliado por F4 aceptaba "número + CUALQUIER palabra de 4+ letras en
  cualquier parte" — 13 de 17 disparos reales (76%) eran números de DIRECCIÓN. Corregido:
  exige que la LÍNEA COMPLETA sea "número + palabra". Tras el fix: 5/5 disparos genuinos, 0
  falsos positivos; R6 bajó de 10 (con ruido) a 2 (cifra final). FALLA 3 sin la clave
  `_listado_paginacion` en el DUMP, la versión anterior declaraba `False` (ausencia leída como
  "no se truncó", la misma regla I4 que el control INV prohíbe) — ahora declara "no_medible"
  con hallazgo DUDA propio. FALLA 4 tres frases "ejemplo sintético" en comentarios resultaron
  casi literales de clientes reales — reescritas con paráfrasis genéricas, confirmado sin
  colisiones de 5+ palabras contra los 625 mensajes reales. FALLA 5 la cifra "44/44" de GCO1.2
  quedó desactualizada al agregar controles en GCO1.4 — corregida con la corrida real. FALLA 6
  (SUPERADA por la tercera ronda, no se borra para no perder el rastro) desfase de reloj
  UTC↔local sin declarar entre `last_message_at` y `ts` — se escribió como "no cambia ninguna
  severidad hoy"; la tercera ronda encontró que SÍ cambiaba evidencia real.

  Tercera ronda encontró un defecto real del fix de la FALLA 1: `_mensajes_del_dia` comparaba
  la fecha del ts (UTC) contra `_fecha` (hora LOCAL del servidor) sin ajustar el desfase —
  medido: -5h exactas y constantes en 161 de 161 pares de los 4 DUMPs, con 111 mensajes reales
  del día perdidos y 78 de otro día colados. Corregido: `Clasificador` acepta `zona_horas`
  (CLI --zona-horas), default `ZONA_HORAS_DEFAULT_NO_CONFIRMADA = -5` (medido SOLO en el
  espacio de Colombia validado), siempre visible en `universo['zona_horas_usada']`. Si el DUMP
  no trae `_fecha`, ahora declara hallazgo P-sin-fecha-auditada/DUDA en vez de desactivarse en
  silencio. La fila de R6 en clasificacion.md ahora declara que NO se acota al día (a
  diferencia de R2/R3/R4), misma frontera que R1.

  Cuarta ronda confirmó el fix de zona horaria (offset -5h exacto, 161/161; 111/78 exactos) y
  encontró dos fallas nuevas: ROTO NUEVO 5a una `_fecha` PRESENTE pero mal formada (no
  AAAA-MM-DD) filtraba TODO a una lista vacía con `acotado_al_dia_activo=True` (engañoso) —
  2 hallazgos R4/MUERTO reales desaparecían en silencio. Corregido: fecha mal formada se trata
  igual que ausente. ROTO NUEVO 5b `parse_fecha` devolvía naive para epoch pero aware para ISO
  con offset — mezclar ambas formas reventaba con TypeError no capturado. Corregido: toda
  fecha ISO con offset se normaliza a UTC/naive igual que el epoch.

  Autoprueba real corrida al cierre de GCO1.4 (tras las cuatro rondas): 56 de 56 controles
  confirmados (13 trampas del encargo + 5 calidad + 9 fixes ronda 1 + 8 fixes ronda 2 + 5
  control R6 + 3 fixes verificación R6 + 7 fixes GCO1.4 + 4 fixes GCO1.4 ronda 2 + 2 fixes
  GCO1.4 ronda 3).


## v1.10 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

### 1 · 🔴 Citaba un orquestador PLANEADO como si fuera una skill hermana

Era **la única skill de la familia Chatea con AVISO** del validador de la casa, y el aviso decía
exactamente lo que había que oír: *"cita una skill golden que NO existe en el arsenal — una excusa
de prosa no la hace existir"*.

El texto era honesto: aclaraba "PLANEADO, no construido todavía" e incluso daba la fecha en que se
comprobó que no estaba en `~/.claude/skills/`. **No bastó, y ese es el aprendizaje.** Un nombre
escrito en el cuerpo de una skill **se lee como una skill que existe**: quien lo encuentre va a
buscarla, no la va a hallar, y no va a saber si falta, si se renombró o si nunca se hizo. La
aclaración vive en el párrafo; el nombre viaja solo.

**Un nombre planeado que lleva semanas en el cuerpo es una promesa que nadie asume.** El hueco
pasa a declararse **como hueco, sin bautizar**, con su dueño donde se reparte el trabajo
(`REGISTRO-FABRICAS.md` y la lista de pendientes del CdM), no en la prosa de la skill que lo echa
de menos.

Se dejó escrito además el matiz que evita el error contrario: **no confundir esa pieza con
`golden-chatea-pro-full-configuracion`**, que sí existe. Aquella orquesta la **instalación** de los
cuatro asistentes; esto sería un orquestador de **diagnóstico**, que cruza cómo quedó instalado
contra cómo está operando. Son piezas distintas.

### 🔴 Y me pasó a mí mientras lo arreglaba

La primera corrección retiró las cuatro citas... y **el validador siguió avisando**, porque mis
propias explicaciones de por qué se había quitado **volvían a escribir el nombre**. Tres veces.
El detector no distingue una orden de su explicación —igual que el guardarraíl de país de
`validacion-direcciones`, el mismo día—, y aquí la regla del detector es la correcta: **el nombre
no se escribe, ni siquiera para contar que se quitó.** Se describe.

### 2 · El 58% del SKILL.md era changelog: el peor caso de la familia

**21.526 bytes de 37.000**, en 6 bloques de comentario HTML que se pagan en cada activación aunque
nadie los lea. Bajaron verbatim aquí. SKILL.md: ~37.000 → **17.899 bytes, un 52% menos**.

### Verificación

`autoprueba.py` **67 de 67 controles** · validador oficial "Valid skill" · validador de la casa
**sano, sin aviso** por primera vez. Y su propia advertencia, que se respeta y se repite aquí:
*"esto valida el DETECTOR contra casos que se saben rotos, no valida ningún día real"*.

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


## CENTRO DE MANDO · 2026-09-27 · <!-- skill v1.13 · 2026-09-27 · CdM: blo · LEY DE LOS REQUISITOS DEL USUARIO

Ley de FER del 02-sep: declarar ANTES lo que la skill necesita del usuario y pedirlo AL CORRER si falta. Desde golden-skill-auditor v1.22 la ley tiene casilla en `validar_arsenal.py`. Se agregó al principio el bloque "Requisitos", redactado con lo que esta skill USA de verdad (medido en su cuerpo y en sus scripts), sin agregar requisitos de más, y con qué hacer si falta: parar y pedirlo con nombre propio. A la fábrica se le informa por la bandeja: una fila no bloquea.

## GCO1.13.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER)

Cambios del 27-sep que no tenian acta propia (limpieza de datos privados en origen, bloque de requisitos o sincronizacion). Este numero solo avisa a quien ya la instalo de que la version publicada cambio; el detalle esta en el diff del repo.
