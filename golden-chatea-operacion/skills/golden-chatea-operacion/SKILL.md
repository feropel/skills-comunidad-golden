---
name: golden-chatea-operacion
description: |
  Golden Group — OPERACIÓN DIARIA DE UN ESPACIO DE CHATEA PRO. Barre las conversaciones de ayer
  (o la ventana que se pida), reconstruye cada hilo con `include_bot=1` y clasifica: quién habló
  de último, en qué paso del embudo murió, si el bot respondió tarde o incoherente, qué preguntó
  el cliente que el prompt no cubre, y por cuál anuncio llegó. Entrega COBERTURA medida (N de N
  del día), con "la empresa se fue de último" primero.
  Úsala SIEMPRE que el usuario quiera saber qué pasó ayer con el bot: "cómo le fue al bot hoy",
  "qué chats se quedaron sin contestar", "quién habló de último", "qué preguntas no supo
  responder el bot", "el bot está diciendo cosas raras", "audita las conversaciones de ayer",
  "revisa el desempeño del asistente", "por cuál anuncio están llegando", "el bot mencionó pago
  anticipado cuando no debía", o pida la corrida diaria centrada en LO QUE DIJO EL BOT.
  Aplica a cualquier workspace y a los 7 países. Solo lee: no escribe en Chatea.
  FRONTERAS: el PEDIDO (qué se despacha, qué se frena, direcciones, duplicados) =
  golden-logistica-diaria, y lo que aparezca de eso se le pasa en una línea; la INSTALACIÓN
  (campos, disparadores, topes, interruptores) = golden-chatea-auditoria. Esta mira el DÍA: si
  FUNCIONÓ de verdad, con la evidencia de lo que el bot escribió.
---

# golden-chatea-operacion · qué pasó ayer con el bot

<!-- skill v1.7 (GCO1.7) — 2026-08-22 — TERCERA auditoría golden-skill-auditor, en frío,
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
el último pendiente. -->
<!-- skill v1.6 (GCO1.6) — 2026-08-22 — SEGUNDA auditoría golden-skill-auditor, en frío,
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
pendiente, no antes. -->
<!-- skill v1.5 (GCO1.5) — 2026-08-22 — auditoría golden-skill-auditor: (1) ANONIMIZADO el
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
  GCO1.4 ronda 3). -->

**Versión:** `GCO1.7` (2026-08-22, tercera auditoría `golden-skill-auditor`, en frío) —
historial completo de `GCO1.0` a `GCO1.6` en el comentario HTML arriba. Autoprueba real:
**63 de 63** controles confirmados (13 trampas del encargo + 5 calidad + 9 fixes ronda 1 + 8
fixes ronda 2 + 5 control R6 + 3 fixes verificación R6 + 7 fixes GCO1.4 + 4 fixes GCO1.4
ronda 2 + 2 fixes GCO1.4 ronda 3 + 7 fixes segunda auditoría) — cifra sin cambios en esta
tercera pasada, no se agregó ningún caso nuevo porque no se encontró ningún defecto de
comportamiento nuevo, solo un hueco de documentación (ver changelog GCO1.7 arriba).

## Conexión con el ecosistema

Cambios relevantes de esta skill (nuevas versiones, hallazgos que cambian el estándar de
trabajo, defectos reparados) se reportan a 🧠 GOLDEN - CENTRO DE MANDO — igual que ya hacen
`golden-skill-auditor` y `golden360`. Esta skill no le habla directo a las demás skills del
ecosistema (`golden-logistica-diaria`, `golden-chatea-auditoria`, `golden-chatea-pro-prompt-
ventas`): cuando algo de aquí les afecta, se avisa al Centro de Mando y es él quien decide si
se retransmite.

**Pendiente real, NO cerrado** (declarado, no silencioso): el offset horario por defecto
(`ZONA_HORAS_DEFAULT_NO_CONFIRMADA = -5`, usado por `_mensajes_del_dia` para acotar R2/R3/R4/Q4
al día auditado) es una medición de UN solo espacio (Colombia) — no está confirmado contra el
panel de Chatea (solo contra la relación interna `last_message_at` ↔ `ts` dentro de los DUMPs
medidos), no cubre horario de verano (irrelevante para Colombia, relevante para otros países
de la plataforma que sí lo observan), y solo acepta offsets enteros de horas. La plataforma
sirve 7 países; para un espacio de otro país se debe pasar `--zona-horas` explícito hasta
confirmar el offset real de ese servidor.

Operar aquí significa **medir lo que el bot escribió de verdad contra lo que debía pasar**, no
leer la configuración y suponer que si está bien montada el bot se comportó bien. `config sana
≠ bot diciendo lo correcto`. El informe se entrega en cobertura (universo del día, N de N
conversaciones clasificadas, hallazgos con evidencia citada del hilo), jamás en veredicto.

**Frases prohibidas en todo lo que salga de esta skill:** "quedó perfecto", "todo bien",
"está listo", "debería funcionar".

## Lo que esta skill mide, y lo que no

| Mide | No mide |
|---|---|
| Lo que el bot RESPONDIÓ, hilo por hilo, del día | Si el campo que sostiene esa respuesta está bien configurado (eso es `golden-chatea-auditoria`) |
| Quién habló de último, dónde murió el embudo, atribución por anuncio | Si la dirección del pedido es válida, si está duplicado (eso es `golden-logistica-diaria`) |
| Preguntas del cliente sin cobertura en el prompt (materia prima para `golden-chatea-pro-prompt-ventas`) | Corregir el prompt — esta skill no escribe nada |
| Calidad real de la respuesta contra frases prohibidas y objeciones reales del cliente | Saldo o consumo de Chatea (la API no lo expone — ver `references/api.md`) |

## Regla de oro de esta skill

**La configuración dice qué DEBERÍA pasar. El hilo dice qué PASÓ.** Un producto con el prompt
impecable puede tener, el día de ayer, 40 clientes a los que el bot les mintió sobre el pago o
los dejó sin respuesta 6 horas. Esta skill nunca sustituye la lectura del hilo real por la
lectura de la config: **se mide lo que el bot DIJO**, no lo que la config sugiere que diría.

## Las cinco fases

### Fase 1 · INVENTARIO antes de tocar (el denominador)

Se corre el extractor y se cuenta el universo del día. Ese número es el denominador de todo el
informe.

```bash
python3 ~/.claude/skills/golden-chatea-operacion/scripts/extraer.py <ruta-al-token> <etiqueta> <fecha-AAAA-MM-DD> [carpeta-salida]
```

Deja `DUMP-<etiqueta>-<fecha>.json` con el universo de contactos de la ventana pedida y el hilo
COMPLETO de cada uno, con las credenciales que pudieran aparecer en el texto **redactadas**.

Antes de seguir, comprobaciones que no son opcionales:

1. **La identidad sale del servidor**, no del nombre del archivo del token — se confirma con
   `/me`, igual que la hermana.
2. **El universo se declara**: N contactos en la ventana según `/flow/bot-users-count` y su
   listado, N hilos efectivamente descargados, N que no se pudieron traer (con el motivo).
3. El denominador de la Fase 1 tiene **TRES estados**, no dos (F6, corregido tras verificación
   2026-08-22 — la versión anterior de este párrafo solo describía dos): `cuadra` (los hilos
   descargados coinciden con el universo declarado por el servidor) — sigue sin aviso;
   `no_cuadra` (ambos números existen y son distintos) — **el informe se detiene**, un
   denominador incompleto invalida todo lo demás; `no_medible` (el servidor no declara un
   total con el que comparar, caso real del endpoint `/subscribers` — ver `references/api.md`)
   — **NO se detiene** (no hay con qué decidir si falta algo), pero tampoco se lee como sano:
   se avisa con un hallazgo `INV`/`DUDA` declarado y la corrida sigue. Detalle exacto en
   `references/clasificacion.md` (control `INV`).

### Fase 2 · CONSTRUIR midiendo contra el estándar

El estándar vive en `references/`, y se mide mientras se clasifica, no después:

- `references/clasificacion.md` — el catálogo completo de controles de clasificación. **Es la
  columna vertebral: se recorre entero.**
- `references/api.md` — endpoints de conversación y las 13 trampas de parseo/clasificación ya
  medidas contra el servidor real (la 14ª es documental: la API no da saldo).
- `references/informe.md` — el formato exacto del entregable.

### Fase 3 · TRES FUENTES antes de cualquier veredicto

1. **Algo equivalente que YA funciona en producción.** Un patrón de respuesta que se repite
   igual en un espacio que factura no es un fallo por sí solo: se contrasta antes de acusarlo.
2. **La fuente autoritativa del sistema.** El hilo real que devuelve el servidor con
   `include_bot=1`, no lo que la config dice que debería contestar.
3. **El validador corrido.** `clasificar.py` sobre el DUMP, con su autoprueba pasada.

### Fase 4 · EJECUTAR O SIMULAR (la fase que más se salta)

```bash
python3 ~/.claude/skills/golden-chatea-operacion/scripts/autoprueba.py     # primero SIEMPRE
python3 ~/.claude/skills/golden-chatea-operacion/scripts/clasificar.py <DUMP.json> --modo cod|prepago [--json salida.json] [--zona-horas N]
```

`--modo` no es opcional en la práctica (F7, corregido tras verificación 2026-08-22 — el comando
documentado aquí antes lo omitía): sin declararlo, cualquier mención de pago anticipado en boca
del bot baja de `🔴 MUERTO` a `🔵 DUDA` — un hallazgo real de "pago anticipado" mencionado en un
espacio contra entrega puede quedar enterrado como duda en vez de mostrarse como el fallo que es.
Se declara siempre antes de correr: `cod` si el espacio vende contra entrega, `prepago` si vende
con pago anticipado.

`--zona-horas` (tercera ronda de verificación, 2026-08-22) declara el offset UTC del espacio,
en horas, para que R2/R3/R4/Q4 acoten correctamente al día auditado. El default sin declararlo
es `-5` (hora Colombia) — **medido SOLO contra el espacio de Colombia validado**, no confirmado
para los otros 6 países que sirve la plataforma. Para un espacio de otro país, se declara
explícitamente hasta confirmar el offset real de ese servidor contra el panel de Chatea (ver
`references/api.md`).

**La autoprueba va primero y no se salta.** Fabrica un día que se SABE roto — con las 13
trampas de clasificación sembradas a la vez (hilos invertidos, `ts` en `None`, notas de pixel al
final, mensajes automáticos del anuncio, audios sin texto separado, fechas con espacio y con
`T`, dinero en los dos formatos, contactos `dropi` mezclados, el caso que debe activar la
compuerta de cordura) — y exige que `clasificar.py` las detecte TODAS. Un clasificador que sale
en verde a la primera contra un día real no prueba que el día esté sano: prueba que no mira.

Además, lo que el código no puede juzgar se ejecuta a mano:

- **La lista de "la empresa se fue de último" se lee entera**, contacto por contacto, contra el
  hilo real — es la que abre todo informe.
- **Las preguntas sin cobertura se contrastan contra el prompt vigente** del producto (leído
  desde `golden-chatea-auditoria` si hay un DUMP reciente, o declarado como no cruzado si no lo
  hay).
- **Toda mención de precio/pago en las respuestas del bot se lee en su contexto**, no solo se
  cuenta por palabra clave.

### Fase 5 · REPORTAR COBERTURA, NO VEREDICTO

El informe se arma con `references/informe.md`. Lleva siempre: universo, N de N conversaciones
clasificadas, método, fuentes, qué se ejecutó, qué falla con evidencia citada del hilo (nunca
una credencial), y qué quedó sin verificar y por qué. Los hallazgos que en realidad son un
PEDIDO (dirección mala, duplicado) se pasan a `golden-logistica-diaria` en una línea, sin
desarrollarlos aquí.

**Cierre obligatorio:** el agente `golden-verificador` recibe el estado final y el estándar, sin
saber cómo se construyó, e intenta romperlo. Su veredicto entra al informe.

## Severidades

| Nivel | Significa | Ejemplos |
|---|---|---|
| 🔴 **MUERTO** | Un cliente se quedó sin respuesta o el bot dijo algo falso | Última palabra del cliente sin respuesta > 2 horas · bot afirmando pago anticipado en un espacio COD |
| 🟠 **RIESGO** | Funcionó pero mal, y se repite | Bot en bucle (misma respuesta 3+ veces) · respuesta tardía sistemática en un paso del embudo |
| 🟡 **HUECO DE PROMPT** | El cliente preguntó algo que el prompt no cubre | Pregunta real sin cobertura — materia prima para `golden-chatea-pro-prompt-ventas` |
| 🔵 **DUDA** | No se pudo verificar, o hay que preguntarle a FER | Clasificación de "paso del embudo" es heurística y no se pudo cruzar contra la config real |

**Un hallazgo contra el bot no es un bug hasta contrastarlo con la config o con FER.** Se
reporta con su evidencia citada del hilo y se pregunta, no se "corrige" — esta skill no escribe.

## Compuerta de cordura (obligatoria, no se apaga)

Si más del 90% de las conversaciones del día se clasifican como "cierra con el cliente" (el bot
tuvo la última palabra en una conversación resuelta), el resultado es absurdo de cara: ningún
espacio real cierra así de bien. **No se publica nada. Se aborta sin escribir el informe** y se
reporta la anomalía como hallazgo de la propia corrida (posible bug de clasificación o de
extracción, nunca "el bot tuvo un día perfecto"). Definición exacta y ejemplo en
`references/clasificacion.md`.

## Nota honesta sobre la frontera con `golden-logistica-diaria` (hallada en verificación)

`golden-logistica-diaria/scripts/analizar_conversaciones.py` **ya calcula "quién habló de
último" y "motivo de no-compra"** contra el mismo endpoint, para decidir a quién llamar por el
PEDIDO. Esta skill calcula las mismas dos señales para decidir si el BOT falló. Es una
superposición real del ecosistema, no resuelta por esta skill en solitario: las dos
implementaciones pueden dar listas distintas sobre el mismo día si divergen en algún detalle de
parseo. Mientras no exista `golden-chatea-360` (el orquestador que las une), **la lista de
`golden-logistica-diaria` es la que manda para decidir a quién llamar** (tiene el contexto de
Dropi y de compra real); la de esta skill sirve para diagnosticar AL BOT — por qué se quedó
callado, no a quién marcar. Si un informe de esta skill y uno de `golden-logistica-diaria` del
mismo día se contradicen, se declara la discrepancia y se avisa al Centro de Mando en vez de
elegir una en silencio.

## Lo que esta skill NO hace

**No escribe en Chatea.** Lee, clasifica y reporta. Las preguntas sin cobertura se pasan a
`golden-chatea-pro-prompt-ventas` como materia prima, no como una edición ya hecha. Los
hallazgos de pedido se pasan a `golden-logistica-diaria` en una línea.

**No vuelve a auditar la instalación.** Si un hallazgo del día apunta a un interruptor apagado
o a un disparador roto, se nombra la sospecha y se remite a `golden-chatea-auditoria` para que
lo confirme contra la config — esta skill no lee bot-fields de configuración.

**No inventa saldo ni consumo.** La API no lo expone (documentado en `references/api.md`,
trampa 14 del encargo original); un informe de gasto de Chatea por API no se puede hacer hoy.

**`R6` (coherencia intra-chat) no reemplaza la confirmación contra Dropi.** Sin Dropi
conectado, `R6` cubre PARCIALMENTE lo que `golden-logistica-diaria` confirma con el pedido
real — compara lo que el cliente pidió contra el resumen final del bot usando solo el chat,
una heurística por palabra clave declarada como tal. Con Dropi conectado, `golden-logistica-
diaria` sigue siendo la fuente definitiva: cruza el chat contra el pedido real ya cargado, no
contra otro mensaje del mismo hilo. `R6` es la versión que funciona sin esa integración —
útil para quien no la tiene montada (por ejemplo, alumnos).

## Cuándo correrla

- Todos los días, sobre las conversaciones del día anterior.
- Cuando FER pregunte "qué pasó con el bot ayer/hoy" o reporte un cliente perdido.
- Después de un cambio grande de prompt, para medir el efecto real (no la config nueva, la
  respuesta real).
- Antes de pedirle a `golden-chatea-pro-prompt-ventas` una mejora: esta skill trae las preguntas
  reales sin cobertura, no una lista inventada.

## Orquestación futura

Cuando esta skill y `golden-chatea-auditoria` estén sanas y probadas, se monta
`golden-chatea-360`, que corre las dos y entrega la cadena causa-efecto (una falla de
instalación explicando una pérdida del día). Ese orquestador se construye **después**, no antes.
