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

**Versión:** `GCO1.1` · `GCO1.0` inicial declarada el 2026-08-20, nace hermana de
`golden-chatea-auditoria` (`GCA1.0`), mismo patrón de versionado: número + fecha, sin CHANGELOG.
`GCO1.1` (2026-08-21) agrega el control `R6` — coherencia intra-chat (sin Dropi): compara lo
que el cliente pidió sobre un atributo concreto (color/talla/cantidad) contra el resumen final
de pedido que redacta el bot, dentro del mismo hilo, sin tocar Dropi ni Shopify.
`GCO1.2` (2026-08-21, auditoría `golden-skill-auditor`) quita dos signos de apertura `¿` que se
habían colado en ejemplos citados de `references/informe.md` e `references/clasificacion.md`
(estándar Golden de escritura); autoprueba corrida (41/41) y sintaxis de los tres scripts
verificada como parte del cierre. Pendiente real, no cerrable con código: el endpoint de listado
de contactos por fecha (`CANDIDATOS_LISTADO` en `extraer.py`) sigue sin confirmar contra un
token vivo — se confirma en la primera corrida real.

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
3. Si el número de hilos descargados no cuadra contra el universo declarado, **el informe se
   detiene**: un denominador incompleto invalida todo lo demás.

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
python3 ~/.claude/skills/golden-chatea-operacion/scripts/clasificar.py <DUMP.json> [--json salida.json]
```

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
