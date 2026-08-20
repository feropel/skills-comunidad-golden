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

**Versión:** `GCA1.0` · Versión inicial declarada el 2026-08-20 por el Centro de Mando: la skill nació sin CHANGELOG y sin número, y sin versión el censo diario no puede ver que alguien la editó.

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
python3 ~/.claude/skills/golden-chatea-auditoria/scripts/autoprueba.py   # primero SIEMPRE
python3 ~/.claude/skills/golden-chatea-auditoria/scripts/auditar.py <DUMP.json> [--json salida.json]
```

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
| 🔴 **MUERTO** | Algo no está funcionando ahora mismo | Producto activo sin entrada en el disparador · campo por encima del techo escapado · palabra clave que difiere en un acento · token de Meta caído |
| 🟠 **MUERTE ANUNCIADA** | Funciona hoy y se rompe solo | Campo sobre el 90% del techo · campo por encima del tope nativo (se corta cuando alguien abra el panel y guarde) · par array/Extendido ambiguo |
| 🟡 **FUGA** | Funciona pero está mal | Llave de otra cuenta heredada · nombre de otra tienda dentro de un prompt · placeholder sin reemplazar · ortografía rota |
| 🔵 **DUDA** | No se pudo verificar, o hay que preguntarle a FER | Valor que difiere de la referencia sin saber cuál es el correcto |

**Un hallazgo contra la configuración no es un bug hasta contrastarlo con FER.** Si la config
dice una cosa y el negocio hace otra, puede ser que el negocio cambió y la config está bien.
Se reporta como DUDA y se pregunta, no se "arregla".

## Lo que esta skill NO hace

**No escribe.** Audita y reporta. Cuando hay que corregir, el hallazgo se pasa a la skill de
configuración que corresponde, con el campo exacto y el valor propuesto. La razón es dura y
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
- Como revisión periódica, para ver los campos que se van acercando al techo.
