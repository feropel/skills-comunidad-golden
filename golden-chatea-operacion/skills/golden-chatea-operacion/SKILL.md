---
name: golden-chatea-operacion
description: >-
  Golden Group — OPERACIÓN DIARIA DE UN ESPACIO DE CHATEA PRO. Barre las conversaciones de
  ayer (o la ventana que se pida), reconstruye cada hilo con `include_bot=1` y clasifica:
  quién habló de último, en qué paso del embudo murió, si el bot respondió tarde o
  incoherente, qué preguntó el cliente que el prompt no cubre, y por cuál anuncio llegó.
  Entrega COBERTURA medida (N de N del día), con "la empresa se fue de último" primero.
  Úsala SIEMPRE que el usuario quiera saber qué pasó ayer con el bot: "cómo le fue al bot
  hoy", "qué chats se quedaron sin contestar", "quién habló de último", "qué preguntas no
  supo responder el bot", "el bot está diciendo cosas raras", "audita las conversaciones de
  ayer", "revisa el desempeño del asistente", "por cuál anuncio están llegando", "el bot
  mencionó pago anticipado cuando no debía", o pida la corrida diaria centrada en LO QUE
  DIJO EL BOT. Aplica a cualquier workspace y a los 10 países. Solo lee: no escribe en
  Chatea.
---

**Fábrica:** chat «✅ SKILL golden-chatea-operacion»
# golden-chatea-operacion · qué pasó ayer con el bot

## 📋 Requisitos: qué necesita del usuario antes de arrancar

- **Token API del espacio de Chatea Pro** · BLOQUEANTE. Se crea en el panel del espacio (*Settings → API Keys*, según el propio código) y va **atado al Bot**; si no, la API responde 404 "Flow not found". Se guarda en `<carpeta del cliente>/.secrets/<espacio>.token`. Cupo: 1.000 llamadas por hora (no está medido si es por token o por espacio; se mira con `golden-chatea-cupo`).
- **La etiqueta del espacio y la fecha a revisar** (AAAA-MM-DD) · BLOQUEANTES: son los argumentos de `extraer.py`.
- **`--modo cod|prepago`** · DEGRADABLE: sin él los hallazgos bajan a DUDA, así que se pregunta.
- **`--zona-horas` o `--pais`** fuera de Colombia · DEGRADABLE: por defecto usa la hora de Colombia (-5).
- Esta skill **no usa Dropi ni Shopify**: la confirmación contra el pedido real es de `golden-logistica-diaria`.

**Si falta algo BLOQUEANTE: no se hace lo que depende de él** (si es de toda la skill, se PARA antes de tocar nada) y se pide con nombre propio: qué es, dónde se saca y dónde se pone. **Si falta algo DEGRADABLE: se pide y se sigue**, dejando marcado como DUDA en todo lo que depende de él. Nunca se presenta como completo.

<!-- skill v1.13 · 2026-09-27 · CdM: bloque de REQUISITOS al principio (ley de FER del 02-sep). -->
<!-- skill v1.12 · 2026-09-22 · auditoría golden-skill-auditor (AUDITA+ARREGLA): único hallazgo real — este comentario H1 seguía marcado "v1.10" pese a que `references/changelog.md` ya tenía una acta v1.11 (2026-09-13) que corrigió la línea **Versión:** de aquí abajo (GCO1.9 → GCO1.10); el propio comentario que sirve de puntero de versión no se había actualizado tras esa corrección — la misma clase de fallo que esa acta v1.11 ya había corregido una vez, reaparecida en el OTRO marcador de versión del mismo archivo. Corregido: este comentario ahora cita v1.12. Verificado tras el arreglo: inventario.sh sin rotas/huérfanas/dudosos, validar_arsenal.py sano sin aviso, autoprueba.py 67/67 (cambio de solo texto, sin tocar código). Sin blindar — sigue abierto el pendiente de zona horaria con dueño (FER/Golden). Historial completo en references/changelog.md. -->
<!-- skill v1.10 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): retirado el nombre de un orquestador PLANEADO que se citaba como si existiera —el validador de la casa lo marcaba como aviso desde días, y un nombre en el cuerpo se lee como una skill que existe—; el hueco pasa a declararse como hueco, con dueño en el CdM. Y el changelog (6 actas, 21.526 B, el 58% del archivo, el peor caso de la familia) baja a references/changelog.md. Historial completo allí. -->

**Versión:** `GCO1.13.1` (2026-09-07, auditoría golden-skill-auditor: retira el nombre del
orquestador de diagnóstico PLANEADO —el hueco queda declarado sin bautizar, con dueño en el
Centro de Mando— y baja el changelog completo a `references/changelog.md`, 21.526 B que se
pagaban en cada activación) — historial completo de `GCO1.0` a `GCO1.9` en
`references/changelog.md`. El contenido de esta skill no cambió desde GCO1.10; las auditorías
`v1.11` (2026-09-13) y `v1.12` (2026-09-22, ver comentario H1 arriba y `references/changelog.md`)
solo corrigieron sus propios punteros de versión. Autoprueba real: **67 de 67** controles
confirmados (13 trampas del encargo + 5 calidad + 9 fixes ronda 1 + 8 fixes ronda 2 + 5 control
R6 + 3 fixes verificación R6 + 7 fixes GCO1.4 + 4 fixes GCO1.4 ronda 2 + 2 fixes GCO1.4 ronda 3 +
7 fixes segunda auditoría + 4 fixes `--pais`) — cifra sin cambios respecto a GCO1.9, confirmada
de nuevo en vivo el 2026-09-22.

🔴 **CUPO DE LA API: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.**
Medido contra la API viva el 2026-09-07: cada respuesta trae **`x-ratelimit-remaining`** (en
inglés *X-RateLimit-Remaining*, "las que quedan") y `x-ratelimit-limit`. **Se repone cada hora**,
pero **no viene `x-ratelimit-reset`**: el servidor no dice a qué minuto empezó la ventana, así que
si te bloqueas se espera una **hora completa** y se comprueba **mirando** el contador
(`golden-chatea-cupo [--necesito N]`), nunca calculándolo.

🔴 **Esta skill es la MÁS CARA de la familia, y su coste NO es una constante.** Las hermanas leen
una configuración de tamaño fijo (61 bot fields). Esta barre **conversaciones**: el listado pagina
de 10 en 10 y **además cada hilo pide sus mensajes aparte**. Un día flojo son decenas de
peticiones; un día de campaña pueden ser cientos. Por eso `extraer.py` **cuenta lo que gastó y lo
dice al terminar**, en vez de prometer un número que cambiaría con cada día.

🔴 **Si el cupo se agota a mitad del barrido, el día queda INCOMPLETO y hay que decirlo.** Un
barrido cortado informado sin aviso se lee como "el día entero" — y el informe diría que **nadie
quedó sin contestar** cuando sí. **Los hilos que faltan no son hilos sin novedad.**

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
sirve 10 países; para un espacio de otro país se debe pasar `--zona-horas` explícito hasta
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
para los otros 9 países que sirve la plataforma (actualizado 2026-09-05: la corrección CdM del
2026-08-29 subió el conteo de 7 a 10 países; esta línea seguía citando el número viejo). Para
un espacio de otro país, se declara
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
parseo. 🔴 **No hay orquestador que una las dos, y el hueco tiene dueño: el Centro de Mando.** Hasta el
2026-09-07 aquí se citaba esa pieza por un nombre de trabajo "planeado", y un nombre que vive
semanas en el cuerpo **es una promesa que nadie asume**: quien lea busca la skill, no la
encuentra, y no sabe si falta o si se renombró. El validador de la casa lo marcaba como aviso
—*"una excusa de prosa no la hace existir"*—. **Mientras ese hueco siga abierto, la lista de
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

Cuando esta skill y `golden-chatea-auditoria` estén sanas y probadas, tiene sentido un
orquestador que corra las dos y entregue la **cadena causa-efecto**: una falla de instalación
explicando una pérdida del día. Eso **no existe y no se le pone nombre aquí**.

🔴 **Por qué no se le pone nombre:** hasta el 2026-09-07 esta sección bautizaba a esa pieza
por un nombre de trabajo, con la honestidad de aclarar que no estaba construida. No bastó: **un nombre
en el cuerpo se lee como una skill que existe**, y el validador de la casa lo marcó como aviso
durante días. Un hueco se declara como hueco y **se registra donde se reparte el trabajo** —
`STACK-GOLDEN/REGISTRO-FABRICAS.md` y la lista de pendientes del Centro de Mando—, no se bautiza
en la prosa de la skill que lo echa de menos.

**Ojo con no confundirlo con `golden-chatea-pro-full-configuracion`**, que sí existe: aquel
orquesta la **instalación** de los cuatro asistentes; esto sería un orquestador de
**diagnóstico**, que cruza cómo quedó instalado contra cómo está operando. Son piezas distintas.

## Fronteras y desambiguacion

FRONTERAS: el PEDIDO (qué se despacha, qué se frena, direcciones, duplicados) = golden-logistica-diaria, y lo que aparezca de eso se le pasa en una línea; la INSTALACIÓN (campos, disparadores, topes, interruptores) = golden-chatea-auditoria. Esta mira el DÍA: si FUNCIONÓ de verdad, con la evidencia de lo que el bot escribió.
