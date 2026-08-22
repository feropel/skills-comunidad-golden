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

**Versión:** `GCO1.4` · `GCO1.0` inicial declarada el 2026-08-20, nace hermana de
`golden-chatea-auditoria` (`GCA1.0`), mismo patrón de versionado: número + fecha. F11 (corregido
tras verificación 2026-08-22 — esta frase antes decía "sin CHANGELOG" para las dos skills, y ya
no es cierto para ninguna de las dos): `golden-chatea-auditoria` SÍ lleva changelog, en
comentario HTML sobre su línea `Versión` (ver su `SKILL.md`); esta skill también lo lleva, en
prosa dentro de esta misma sección de versión, desde `GCO1.1`.
`GCO1.1` (2026-08-21) agrega el control `R6` — coherencia intra-chat (sin Dropi): compara lo
que el cliente pidió sobre un atributo concreto (color/talla/cantidad) contra el resumen final
de pedido que redacta el bot, dentro del mismo hilo, sin tocar Dropi ni Shopify.
`GCO1.2` (2026-08-21) quita dos signos de apertura `¿` que se habían colado en ejemplos citados
de `references/informe.md` e `references/clasificacion.md` (estándar Golden de escritura);
verificado de nuevo en esta auditoría (`golden-skill-auditor`, 2026-08-22): los dos archivos
siguen limpios de `¿`, y la autoprueba real corrida hoy da **44/44** (no 41/41 — la cifra
anterior quedó desactualizada frente a los controles agregados después; corregida aquí con la
corrida real, no reescrita a ciegas) y sintaxis de los tres scripts verificada.
`GCO1.3` (2026-08-22, misma auditoría) sincroniza la documentación con `extraer.py`, que había
avanzado más rápido que `SKILL.md`/`references/api.md` (evidencia: la línea de versión de
`extraer.py` declaraba haberse actualizado con el hallazgo del endpoint real, mientras
`SKILL.md`/`references/api.md` seguían con los tres candidatos originales sin confirmar — no
se cita el mtime del archivo como evidencia, ya que un mtime cambia con cualquier edición
posterior y deja de servir como registro de cuándo pasó algo; la evidencia es el propio
changelog):
el endpoint de listado de contactos por fecha **sí quedó confirmado contra un token real**
(espacio LIBIDOUP, 2026-08-21) — es `/subscribers`, no ninguno de los tres candidatos
originales, y ese endpoint no filtra por fecha en el servidor (`extraer.py` compensa
paginando el universo completo y filtrando en cliente; detalle en `references/api.md`).
Pendiente real que sigue sin cerrar: esa confirmación es de UN espacio — otro
plan/versión de Chatea Pro puede exponer un endpoint distinto, por eso `CANDIDATOS_LISTADO`
se mantiene como lista de candidatos y no se reduce a un literal fijo; se reconfirma en la
primera corrida real contra cada espacio nuevo.
`GCO1.4` (2026-08-22) cierra los 11 hallazgos (F1-F11) de una verificación adversarial corrida
contra 4 DUMPs reales de producción del espacio LIBIDO-UP (165 conversaciones, `ts` epoch en el
100% de los mensajes medidos), y luego una SEGUNDA ronda de verificación adversarial sobre el
resultado de la primera encontró 6 fallas nuevas (numeradas FALLA 1-6 más abajo), todas
corregidas y remedidas contra los mismos 4 DUMPs. Cifras de esta sección: las de la corrida
FINAL (después de las dos rondas), no las intermedias.

**F1** `parse_fecha` ahora lee `ts` epoch (segundos o milisegundos, detectado por magnitud)
además de los formatos de texto — de los 31 hallazgos `R1` que antes caían en `🟠 RIESGO` por
"gap no medible", los 31 pasaron a su severidad real (`🔴 MUERTO`, gap medido entre 156 y 818
minutos, todos ≥ el umbral de 2h). **F2** la autoprueba invirtió los casos que exigían que
epoch fuera "no parseable" y suma fixtures nuevas con epoch real; los fixtures que usaban
`direction` como si fuera el campo primario ahora usan `type` (el campo real medido contra
producción). **F3** los patrones de redacción de credenciales ya no viven duplicados entre
`extraer.py` y `clasificar.py`: los dos importan de `scripts/secretos.py` (17 familias, umbral
de `SanctumBearer` unificado en `{20,}`), y la autoprueba prueba las familias contra el camino
real de `extraer.py` (`redactar()`/`quedan_secretos()`), no solo contra
`clasificar.redactar_texto`. **F4** el vocabulario de cantidad se amplió — ver FALLA 2 más
abajo, la primera versión de este arreglo tuvo un defecto real que la segunda ronda corrigió.
**F5** la compuerta de cordura ahora tiene lado bajo: 0% de cierre con universo de 10+
conversaciones no-dropi genera un hallazgo `🟠 RIESGO` declarado (sin abortar la corrida, a
diferencia del lado alto) — se activó en 3 de los 4 días reales medidos (0%, 0%, 0%; el cuarto
día, 6.67%, no activa el umbral). **F6** `SKILL.md` y `references/informe.md` ahora describen
los TRES estados del denominador de la Fase 1 (antes solo describían el aborto). **F7** el
comando documentado de `clasificar.py` ahora incluye `--modo cod|prepago`. **F8** las dos
afirmaciones sin artefacto ("los tres candidatos dan 404", "4 variantes de fecha probadas") se
reescribieron para decir solo lo que el DUMP real respalda. **F9** el listado de contactos
declara en el DUMP (`_listado_paginacion`) si se truncó en el tope de 500 páginas y si el
servidor no dio `meta.last_page` — ver también FALLA 3 más abajo. **F10** medido de nuevo tras
F1: los 6 de 56 hilos del 08-21 que llegaban en orden no descendente ahora se ordenan
correctamente (confirmado con `invertir_hilo` sobre los 6 hilos reales). **F11** esta sección
corrige la afirmación de que ninguna de las dos skills lleva changelog.

**Segunda ronda de verificación adversarial (mismo día, mismos 4 DUMPs), 6 fallas encontradas
y corregidas:**
**FALLA 1** el hilo que descarga `extraer.py` trae el histórico COMPLETO del contacto, no solo
el día pedido — `R2`/`R3`/`R4`/`Q4` recorrían ese histórico entero y podían acusar al bot de una
demora, un bucle o una frase de OTRO DÍA (medido: los 7 hallazgos `R2` de la corrida anterior
citaban gaps de días distintos al auditado, uno de 818 minutos). Corregido con
`_mensajes_del_dia` (filtra por `_fecha` del DUMP) antes de correr esos cuatro controles; `R1`
y `R6` siguen usando el hilo completo a propósito (frontera declarada en
`references/clasificacion.md`). Tras el fix: `R2` = 0, `R4` = 2 (bajó de 3, una mención era de
otro día) en la corrida final contra los 4 DUMPs.
**FALLA 2** el vocabulario de cantidad ampliado por F4 (ronda 1) aceptaba "número + CUALQUIER
palabra de 4+ letras en cualquier parte del mensaje" — contra los 625 mensajes de cliente
reales, 13 de 17 disparos (76%) eran números de DIRECCIÓN, no cantidad de producto. Corregido:
el patrón de "producto implícito" ahora exige que la LÍNEA COMPLETA del mensaje sea "número +
palabra" — una dirección nunca cumple esa forma. Tras el fix: 5 de 5 disparos reales son
cantidades genuinas, 0 falsos positivos de dirección; `R6` bajó de 10 (con el ruido) a **2**
(cifra final, sin ruido) contra los 4 DUMPs.
**FALLA 3** cuando el DUMP no traía la clave `_listado_paginacion` (los 4 DUMPs reales de
LIBIDO-UP, extraídos con una versión de `extraer.py` anterior a que este campo existiera), la
primera versión de este fix declaraba `listado_truncado_por_tope_500: False` — ausencia de dato
leída como "no se truncó", la misma regla I4 que esta skill prohíbe en el control `INV`.
Corregido: ahora se declara `"no_medible"` con un hallazgo `P-listado-truncado`/`🔵 DUDA`
propio cuando la clave no viene, distinto de `False` cuando sí viene y confirma que no hubo
truncado.
**FALLA 4** tres frases citadas como "ejemplo sintético" en comentarios de `clasificar.py`
(y una dirección sintética de prueba en `autoprueba.py`) resultaron ser texto literal — o casi
literal — de clientes reales de LIBIDO-UP presentes en los DUMPs, violando la regla del
encargo de nunca copiar mensajes literales hacia la skill. Reescritas con paráfrasis genéricas
sin ningún fragmento reconocible del texto real; confirmado con un barrido de colisión de
frases de 3 y 5 palabras contra los 625 mensajes de cliente de los 4 DUMPs — 0 colisiones de
5+ palabras tras la corrección.
**FALLA 5** esta misma sección (entrada `GCO1.2`) citaba "44/44" como la autoprueba real
corrida, pero al agregar controles en `GCO1.4` esa cifra no se actualizó — el mismo defecto que
esa entrada decía haber corregido. La cifra vigente es la de la autoprueba real corrida al
cierre de esta versión (ver más abajo).
**FALLA 6** (párrafo escrito en la segunda ronda; **SUPERADO por la tercera ronda, ver abajo —
no se borra para no perder el rastro, pero lo que sigue en este párrafo ya no describe el
estado actual**) `extraer.py` filtra el día del listado de contactos comparando la fecha de
`last_message_at` (hora del servidor, sin husos declarados) contra `_epoch_a_fecha` en
`clasificar.py` (que convierte `ts` siempre a UTC) — un desfase de reloj no declarado en
ninguna parte. Se escribió aquí como "pendiente real, no cerrado" y "no cambia ninguna
severidad hoy" — la tercera ronda de verificación (párrafo siguiente) encontró que SÍ cambiaba
evidencia real (111 mensajes perdidos, 78 colados) en cuanto se construyó `_mensajes_del_dia`
sobre esa misma fecha sin ajustar el desfase, y se corrigió ahí.

**Tercera ronda de verificación adversarial (mismo día, mismos 4 DUMPs)** encontró un defecto
real introducido por el fix de la FALLA 1 de la ronda 2, y dos huecos de documentación:
**ROTO NUEVO** `_mensajes_del_dia` comparaba la fecha del `ts` (siempre convertida a UTC por
`_epoch_a_fecha`) contra `_fecha` (hora LOCAL del servidor) sin ajustar el desfase — medido:
-5h exactas y constantes en 161 de 161 pares comparables de los 4 DUMPs, con 111 mensajes
reales del día perdidos y 78 de otro día colados, la MISMA clase de fallo que la ronda 2 decía
haber cerrado. Corregido: `Clasificador` acepta `zona_horas` (CLI: `--zona-horas`), con default
declarado `ZONA_HORAS_DEFAULT_NO_CONFIRMADA = -5` (medido SOLO en el espacio de Colombia
validado, no universal a los 7 países — ver `references/api.md`), siempre visible en
`universo['zona_horas_usada']`. Además: si el DUMP no trae `_fecha`, el acotado se desactivaba
en silencio (misma clase que ya se corrigió para `_listado_paginacion`) — ahora declara un
hallazgo `P-sin-fecha-auditada`/DUDA y `universo['acotado_al_dia_activo'] = False`. Y la fila
de `R6` en `clasificacion.md` no declaraba explícitamente que R6 (a diferencia de R2/R3/R4)
NO se acota al día — corregido con la misma frontera que ya tenía R1.

**Cuarta ronda de verificación adversarial (mismo día, mismos 4 DUMPs)** confirmó el fix de
zona horaria (offset -5h reproducido exacto, 161/161 pares; 111/78 reproducidos exacto) y
encontró dos fallas nuevas del mismo fix: **ROTO NUEVO 5a** una `_fecha` PRESENTE pero con
formato distinto a `AAAA-MM-DD` (DUMP corrompido o de otra fuente) hacía que
`_mensajes_del_dia` filtrara TODO a una lista vacía, con `acotado_al_dia_activo` declarado
`True` (formalmente cierto, engañoso — el acotado estaba "activo" pero inútil): medido, 2
hallazgos `R4`/MUERTO reales desaparecían en silencio total. Corregido: `_fecha` se valida por
formato al construir `Clasificador`; una `_fecha` malformada se trata IGUAL que una ausente
(mismo hallazgo `P-sin-fecha-auditada`/DUDA, `acotado_al_dia_activo=False`). **ROTO NUEVO 5b**
`parse_fecha` devolvía datetime *naive* para `ts` epoch pero *aware* para ISO con offset (ej.
terminado en `Z`) — un DUMP que mezclara ambas formas (nunca visto en producción, pero
declarado como aceptado por la función) hacía que cualquier resta entre las dos reventara con
`TypeError` no capturado, tumbando toda la corrida. Corregido: toda fecha ISO con offset se
normaliza a UTC y se vuelve naive antes de devolverse, igual que el epoch. También se cerraron
dos huecos de documentación: la contradicción interna de este mismo archivo (el párrafo FALLA
6 de arriba, que decía "sin corregir" un defecto que la tercera ronda ya había corregido —
marcado como superado en vez de borrado, para no perder el rastro) y la ausencia total de
mención a la zona horaria en `references/clasificacion.md`.

Autoprueba real corrida al cierre de `GCO1.4` (tras las cuatro rondas): **56 de 56** controles
confirmados (13 trampas del encargo + 5 calidad + 9 fixes ronda 1 + 8 fixes ronda 2 + 5 control
R6 + 3 fixes verificación R6 + 7 fixes GCO1.4 + 4 fixes GCO1.4 ronda 2 + 2 fixes GCO1.4 ronda
3). **Pendiente real, NO cerrado** (declarado, no silencioso): el offset -5h es un default
medido en UN solo espacio (Colombia); no está confirmado contra el panel de Chatea (solo
contra la relación interna `last_message_at` ↔ `ts` dentro de los DUMPs), no cubre horario de
verano (irrelevante para Colombia, relevante para otros países de la plataforma que sí lo
observan), y solo acepta offsets enteros de horas. Para un espacio de otro país se debe pasar
`--zona-horas` explícito hasta confirmar el offset real de ese servidor.

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
