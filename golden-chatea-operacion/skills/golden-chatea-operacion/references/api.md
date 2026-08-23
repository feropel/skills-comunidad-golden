# API de Chatea Pro · lo que hace falta para operar el DÍA

Base: `https://chateapro.app/api` · mismo motor whitelabel de uChat que usa
`golden-chatea-auditoria` (OpenAPI 3.0.0, 215 endpoints en 21 categorías). Auth, cabeceras y
paginación son las mismas — se resumen aquí, el detalle vive en el `api.md` de la hermana.

```
Authorization: Bearer <token>
Accept: application/json
User-Agent: <de navegador>     ← sin esto, Cloudflare 1010
```

**El token está atado a UN flujo** y su identidad se confirma con `/me`, nunca con el nombre del
archivo. Depósito de tokens de Golden: `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/.secrets/`,
`chmod 600`. Una copia vieja que devuelve 401 no se resucita.

## Endpoints de esta skill

| Endpoint | Para qué | Trampa |
|---|---|---|
| `GET /flow/bot-users-count` | tamaño del universo del espacio | Da el total, no la ventana de fecha por sí solo — se cruza contra el listado de contactos. |
| listado de contactos con ventana de fecha | el universo del DÍA (el denominador) | **Confirmado contra un token real en UN espacio** (ESPACIO-REF, 2026-08-21): el endpoint que existe es `/subscribers` (sin prefijo `/subscriber` ni `/flow`), responde `200`, y el universo total que declaró en esa corrida fue 486 contactos. Confirmación de UN espacio, no universal — otro plan/versión de Chatea puede exponer un endpoint distinto; `extraer.py` prueba la lista de candidatos, usa el primero que responda `200` con una lista, y **declara en el DUMP cuál usó**. Si un espacio nuevo no calza con ninguno, se confirma viendo la pestaña de red del panel y se ajusta `CANDIDATOS_LISTADO` — no se corrige a ciegas. **F8 (corregido tras verificación 2026-08-22 — las dos frases siguientes antes afirmaban una medición sin artefacto que la respalde):** los otros tres candidatos (`/subscriber/list`, `/flow/subscribers`, `/subscriber/get-list`) **no se confirmó que dieran 404** contra ningún servidor real en esa corrida — se quedan como fallback declarado, sin la afirmación de que fallan. **Trampa medida (esta sí, confirmada):** `/subscribers` NO filtra por `from_date`/`to_date` en el servidor — pedir con y sin esos dos parámetros da el mismo total. Las otras variantes de nombre de parámetro (`date_from/date_to`, `start_date/end_date`, `subscribed_from/to`) **no se probaron contra un token real**; la cifra "4 variantes probadas" de una versión anterior de este documento no tenía artefacto que la respalde y se retira. `extraer.py` compensa paginando el universo COMPLETO y filtrando en cliente por `last_message_at` (con `last_interaction`/`subscribed` de respaldo), y declara en el DUMP qué campo decidió cada contacto. Limitación declarada: un contacto cuya conversación cruza más de un día, con `last_message_at` cayendo en un día POSTERIOR al pedido, no aparece en el universo de un día anterior aunque haya tenido mensajes ese día — el servidor no expone actividad por día, solo el último momento. **Desfase de reloj UTC↔local, con un mitigante DECLARADO, no cerrado del todo (tercera ronda de verificación, 2026-08-22):** `extraer.py` filtra el día comparando la fecha de `last_message_at` tal cual la declara el servidor (hora local, sin zona confirmada), mientras `clasificar.py` convierte todo `ts` a UTC (`_epoch_a_fecha`). Medido en los 4 DUMPs reales: desfase de **-5h EXACTAS y CONSTANTES en 161 de 161 pares comparables** (consistente con hora Colombia). Sin ajustar ese offset, `_mensajes_del_dia` (el filtro que acota R2/R3/R4/Q4 al día auditado, ver `clasificacion.md`) perdía 111 mensajes reales del día y colaba 78 de otro día — la MISMA clase de fallo que motivó ese control. Mitigado: `Clasificador` acepta `zona_horas` (default `ZONA_HORAS_DEFAULT_NO_CONFIRMADA = -5` en `clasificar.py`), declarado siempre en `universo['zona_horas_usada']`, nunca aplicado en silencio. **Lo que sigue sin cerrar:** ese -5 es la medición de UN espacio (Colombia); la plataforma sirve 7 países con offsets distintos, y no se confirmó contra el panel de Chatea cuál es la zona real que declara `last_message_at` — para un espacio de otro país, pasar `zona_horas=` explícito hasta confirmar el offset real de ese servidor. |
| listado — paginación | F9, corregido tras verificación 2026-08-22 | El bucle que pagina `/subscribers` (u otro candidato) tenía un tope de 500 páginas que cortaba en SILENCIO si un espacio algún día lo cruza; ahora `extraer.py` declara en el DUMP (`_listado_paginacion`) cuántas páginas se trajeron de verdad, si se truncó por el tope, y si el servidor no dio `meta.last_page` (en ese caso el bucle **no pagina**, limitación conocida y declarada, no implícita — se trae solo la primera página). `clasificar.py` convierte el truncado en un hallazgo `P-listado-truncado`/RIESGO. |
| `GET /subscriber/get-info?user_ns=<ns>` | el registro de un contacto | Trae `opted_in_through` (el marcador de si nació de la integración de Dropi) y los campos de usuario propios de ese contacto. Mismo endpoint que usa la hermana. |
| `GET /subscriber/chat-messages?user_ns=<ns>&include_bot=1&include_note=1&include_system=1&page=N` | el hilo COMPLETO de la conversación | Ver las 13 trampas abajo. Es el corazón de esta skill. **Pagina** (`meta.last_page`): un hilo largo sin agotar la paginación queda truncado con un `200 ok` que no lo delata — `extraer.py` pagina hasta `MAX_PAG_HILO=12` (medido por `golden-logistica-diaria`: con 5 se truncaba el 5% de los hilos) y declara el truncado en `_avisos_de_hilo` si lo hubo. |

### Campos confirmados dentro de cada mensaje del hilo

Medidos contra el servidor real por `golden-logistica-diaria/scripts/barrer_chats.py` y
`analizar_conversaciones.py`, que barren este mismo endpoint (6.911 mensajes medidos en un
espacio):

| Campo | Qué es | Nota |
|---|---|---|
| `type` | dirección del mensaje | valores confirmados: `in` (cliente), `out` (empresa/bot), `note` (evento de pixel de Meta) — **es el campo primario** para P5 y para "quién habló de último" |
| `content` | el texto | — |
| `ts` | el momento del mensaje | **único campo de tiempo confiable** — `created_at` y `date` llegan vacíos, medido 6.911 de 6.911 mensajes en el espacio de referencia; no son un fallback útil, son ruido |
| `msg_type` | de qué está hecho el mensaje | valores del encargo original de esta skill: `text`, `audio`, `feed` (comentario de Facebook), `button_template` — es un eje DISTINTO al de `type`: uno dice quién habla, el otro de qué está hecho. `golden-logistica-diaria` no lo guarda (lo declara como hueco propio); esta skill lo lee y por eso resuelve el caso del audio mudo que esa skill no puede. |
| `payload.transcribed_text` | transcripción de un audio | ver trampa 8 |
| `payload.referral` | atribución del anuncio | `source_id`, `headline`, `body`, `ctwa_clid` |

`clasificar.py` usa `type`/`content`/`ts` como detección PRIMARIA (con `direction`/`sender`/
`is_bot` como respaldo secundario para DUMPs de otra integración tipo uChat, nunca al revés). Un
mensaje que no calza con ninguna forma conocida se declara `desconocido` con un hallazgo propio
(`P-desconocidos`) — nunca se cuenta en silencio como si no existiera.

## Las 13 trampas de conversación · ya medidas, no se vuelven a pagar

Numeración igual a la del encargo original (`ENCARGO-golden-chatea-operacion.md`), con el
código de control que usa `clasificar.py` entre paréntesis. La trampa 14 del encargo (la API no
da saldo ni consumo) es documental y no tiene control de código — queda declarada abajo.

1. **(P1) `chat-messages` sin `include_bot=1` devuelve SOLO entrantes.** `extraer.py` lo
   codifica como literal fijo en la URL, nunca como parámetro opcional. Medido: un clasificador
   basado en "el bot no respondió" marcó 529 de 576 como abandonados, incluidos los 31 que sí
   compraron.
2. **(P2) El parámetro de contacto es `user_ns`, no `subscriber_id`.** Con `subscriber_id`
   devuelve `422`. `extraer.py` usa `user_ns` en la firma de su función de descarga de hilo.
3. **(P3) El hilo llega del MÁS RECIENTE al más viejo.** `clasificar.py` lo invierte a orden
   cronológico antes de clasificar. Sin invertir, "lo último que dijo el cliente" queda primero
   y la detección de preguntas sin responder nunca dispara.
4. **(P4) Ordenar por `ts` cuando todos los `ts` son `None` es un no-op silencioso.** El
   fallback es explícito: con tiempo se ordena por tiempo parseado, sin tiempo se INVIERTE la
   lista tal cual llegó (asumiendo que el servidor la entregó en orden reciente→viejo). Nunca se
   deja un `sort` que no mueve nada sin que el código lo note.
5. **(P5) Las entradas `type == "note"` (con `msg_type == "note"` como respaldo si `type` no vino) no son conversación.** Son eventos de pixel de Meta
   que se disparan después del último mensaje real e invierten la señal de quién habló de
   último. Se excluyen del hilo antes de cualquier clasificación.
6. **(P6) El botón del anuncio manda un texto PREDEFINIDO** ("Hola quiero información y precio
   de X"). Contarlo como palabra del cliente inventa objeciones: 64 falsas de precio en una
   muestra medida, y 39 de 84 "trabados" eran solo el mensaje automático. Se detecta por
   frecuencia + forma sobre el TEXTO del primer mensaje (`plantillas_de`, ver `clasificacion.md`
   control P6) — **corregido tras verificación adversarial 2026-08-22 (golden-verificador,
   re-auditoría):** esta línea afirmaba también "coincidencia contra `payload.referral`", pero
   el código nunca cruza el texto de la plantilla contra `referral` — ese campo solo alimenta la
   atribución por anuncio (Q5, `_atribucion`), un control distinto. Se retira la afirmación sin
   artefacto que la respalde; se excluye del cálculo de motivo de no-compra.
7. **(P7) El motivo de no-compra se lee SOLO de lo que escribió el CLIENTE.** El bot menciona
   precio y envío en casi toda conversación: buscar "caro" en el hilo completo (incluyendo al
   bot) clasifica el 100% como objeción de precio. Se filtra siempre por dirección `cliente`
   antes de buscar palabras de objeción.
8. **(P8) El hilo trae `msg_type` y `payload.transcribed_text`.** Guardar solo `content`
   convierte un audio en una comilla vacía. Caso real: una nota de voz salió como fila muda en
   la lista de calientes y nadie la abrió en ocho días. Los comentarios de Facebook llegan con
   `msg_type: feed` y se clasifican aparte, no como chat privado.
9. **(P9) Las fechas de Chatea llevan ESPACIO** (`2026-08-10 11:25:39`) y una marca ISO lleva
   `T`. Como el espacio (`0x20`) es menor que `T` (`0x54`), comparar como TEXTO deja todo
   contacto nuevo por debajo de la marca del incremental: reporta "no entró nadie nuevo" todos
   los días, para siempre, sin un solo error visible. Las fechas se comparan **parseadas**
   (`parse_fecha`), nunca como cadena.
10. **(P10) El dinero viene en DOS formatos a la vez** (`142.800` y `74900.00`). Quitar lo
    no-dígito antes de distinguir convierte el segundo en `7.490.000`. `parse_dinero` decide el
    formato ANTES de limpiar: dos decimales exactos tras el punto = decimal; grupos de tres
    dígitos tras el punto = miles.
11. **(P11) El denominador de conversión excluye los contactos que crea la integración de
    Dropi** (nacen de un pedido que ya existía; incluirlos infló una conversión de 32% a 68% en
    otro espacio medido). El marcador es `opted_in_through: "dropi"` en `/subscriber/get-info`.
    Se excluyen **declarados en el informe**, jamás en silencio.
12. **(P12) Campos que se autollenan con el anuncio, no con la conversación.** `Productos
    escogidos` lo llena el clic del anuncio (visto lleno en 92-100% de las etapas incluso sin
    ciudad ni dirección cargada), mientras `Cantidad de productos` sí refleja la conversación
    real. Antes de usar cualquier campo de `get-info` como evidencia de qué habló el cliente, se
    declara si ese campo se autollena o se actualiza con la charla — nunca se asume.
13. **(P13) Compuerta de cordura.** Si más del 90% de las conversaciones "cierran con el
    cliente", el resultado es absurdo de cara y no se publica. Detalle y definición exacta en
    `clasificacion.md`.

## Trampa 14 · lo que la API NO da (documental, sin control de código)

**No hay saldo ni consumo.** 40 rutas probadas por la hermana; `/flow/conversations/data`
responde `200` y viene vacío. Un informe de gasto de Chatea por API no se puede hacer hoy — si
FER lo pide, se declara como no disponible, no se estima ni se inventa.

## Lo que sí trae el mensaje y vale oro para esta skill

- `payload.referral` con `source_id` (el ID del anuncio de Meta), `headline`, `body` y
  `ctwa_clid` — la atribución sin tocar la API de Meta.
- `msg_type` distingue `text`, `audio`, `feed` (comentario de Facebook), `button_template`.
- Cuando es voz, `payload.transcribed_text` trae la transcripción ya hecha.

## Seguridad

Aunque esta skill lee conversaciones y no las integraciones con credenciales, un cliente puede
pegar por error un token o una contraseña dentro del chat. `extraer.py` y `clasificar.py`
corren el mismo barrido de redacción por patrón sobre el contenido de los mensajes antes de
escribir el DUMP y sobre toda evidencia citada en un hallazgo, con la misma compuerta final que
bloquea la escritura si queda un secreto reconocible.

**F3 (CRÍTICO SEGURIDAD, corregido tras verificación 2026-08-22):** esta lista **antes vivía
duplicada** en cada script (11 familias en `extraer.py`, 17 en `clasificar.py`, con el umbral de
`SanctumBearer` distinto en cada copia — `{32,}` vs `{20,}`) y este mismo párrafo afirmaba, en
una versión anterior, que estaban "mantenidas sincronizadas" — no era cierto, y el defecto real
(un secreto de una familia que `clasificar.py` sabía redactar podía llegar sin redactar al DUMP
que escribe `extraer.py`) no lo vio la autoprueba anterior porque su única prueba directa
importaba `redactar_texto` de `clasificar.py`, nunca del camino real que escribe a disco. Ahora
hay una **fuente única**: `scripts/secretos.py`, con las 17 familias (OpenAI, ElevenLabs, Stripe
secreto y webhook —live y test—, Mercado Pago, JWT, Meta, Shopify, xAI, Google, refresh token de
Google OAuth, bearer Sanctum con el umbral más estricto `{20,}`, GitHub —PAT clásico y
fine-grained—, AWS access key, Slack, SendGrid, y un bearer hexadecimal genérico de 64
caracteres como red de última malla), y los dos scripts la importan — no hay copia local que
pueda desincronizarse. `autoprueba.py` prueba las 17 familias contra `secretos.redactar_texto`
directamente, y por separado contra el camino real de un hallazgo (`Clasificador` → `falla()`) y
el camino real de `extraer.py` (`quedan_secretos`), para que un defecto en cualquiera de los dos
caminos sea visible. Nunca se pega una credencial en un informe, aunque el cliente la haya
escrito él mismo — y ninguna lista de patrones es exhaustiva por definición: si aparece una
familia nueva, se añade SOLO en `secretos.py`, nunca en los scripts que la importan.
