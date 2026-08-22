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

**Versión:** `GCA1.2`

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

**La autoprueba va primero y no se salta.** Fabrica un espacio que se SABE roto (29 defectos
sembrados, entre ellos los cinco falsos negativos que una verificación adversarial encontró) y
exige que el auditor los encuentre todos. Un auditor que sale en verde contra un
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
sí escribe. La razón es dura y
está medida: escribir con POST en vez de PUT devuelve `200` con un mensaje que no contiene la
palabra "error", y pasarse del techo devuelve `200 ok` guardando el contenido cortado. Una skill
que audita y escribe en la misma pasada puede reportar "corregido" sobre algo que nunca se
escribió. Si el usuario pide corregir, se corrige con la skill dueña y **se vuelve a auditar
desde el DUMP nuevo**, releyendo del servidor y comparando.

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

```json
{"espacio": "f218311", "decisiones": [
  {"clave": "D3|huerfanos-sin-pauta",
   "motivo": "sin pauta activa no llegan mensajes; se registran cuando se les ponga",
   "fecha": "2026-08-20",
   "reabrir_si": "se les carga un id de anuncio"}]}
```

`reabrir_si` es lo que impide que el libro se vuelva una alfombra para esconder hallazgos: dice
en qué condición la decisión deja de valer. **Sin motivo y sin fecha no se acepta una decisión**,
porque dentro de tres meses nadie sabría si sigue vigente. El detalle está en el bloque J de
`references/controles.md`.
