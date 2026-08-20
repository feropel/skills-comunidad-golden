# API de Chatea Pro · lo que hace falta para auditar

Base: `https://chateapro.app/api` · el whitelabel expone el mismo motor que uChat
(OpenAPI 3.0.0, **215 endpoints en 21 categorías**).

## Autenticación y cabeceras

```
Authorization: Bearer <token>
Accept: application/json
User-Agent: <de navegador>     ← sin esto, Cloudflare 1010
```

**El token está atado a UN flujo.** Un token no ve otro espacio. Y el **nombre del archivo del
token no prueba a qué espacio pertenece**: la identidad se pregunta al servidor.

Depósito de tokens de Golden: `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/.secrets/`, `chmod 600`.
Se apunta al depósito; una copia vieja que devuelve 401 no se resucita.

## Lectura · lo que usa la auditoría

| Endpoint | Para qué | Trampa |
|---|---|---|
| `GET /me` | identidad de la cuenta | — |
| `GET /flow/bot-fields?page=N` | la configuración completa | **PAGINA de 10 en 10 e ignora `per_page`.** Comparar contra `meta.total`. |
| `GET /flow/user-fields` | campos de usuario y su límite | pagina |
| `GET /flow/subflows` | subflujos vivos (para cruzar disparadores) | pagina |
| `GET /flow/tags` · `/flow/segments` · `/flow/custom-events` | segmentación | paginan |
| `GET /flow/ai-agents` · `/flow/ai-tasks` | agentes y tareas de IA | el prompt completo sale del detalle: `POST /flow/ai-agent-info` y `/flow/ai-task-info` con su `ns` |
| `GET /workspace-settings/channels` | canales conectados | — |
| `GET /integration/<servicio>` | estado de las integraciones | **devuelve las llaves en TEXTO PLANO** |
| `GET /flow/bot-users-count` | tamaño del espacio | — |
| `GET /subscriber/get-info` | el registro de un contacto | es lo que distingue "atendido" de "abandonado" |
| `GET /subscriber/chat-messages?user_ns=<ns>&include_bot=1` | el hilo COMPLETO | sin `include_bot` devuelve **solo entrantes** · con `subscriber_id` devuelve 422 |

## Escritura · esta skill no escribe, pero audita lo escrito

Se documenta porque explica por qué un campo puede estar mal sin que nadie lo note:

- **Crear:** `POST /flow/create-bot-field` con `{name, var_type, value, description}`. Usa
  `var_type` (no `type`) y **exige `value`**, aunque sea vacío. Con otra llave, 422.
- **Editar uno:** `PUT /flow/set-bot-field` con `{var_ns, value}`.
- **Editar por lote:** `PUT /flow/set-bot-fields-by-name` con la llave **`data`**:
  `{"data":[{"name","value"}]}`. Con `bot_fields` responde 400.
- 🔴 **Editar con POST devuelve `{"message":"The POST method is not supported… Supported
  methods: PUT."}` — un 200 con un mensaje que NO contiene la palabra "error".** Quien valide
  buscando "error" da por escrito algo que nunca se escribió. Caso real: 7 campos reportados
  "ok" y los 7 con el valor viejo.
- 🔴 **La truncada es silenciosa.** Pasarse del tope responde `200 {"status":"ok"}` y guarda el
  contenido **cortado**.
- **Regla:** escribir → **releer del servidor** → comparar valor y longitud. La respuesta de
  escritura no prueba nada.
- **El `var_ns` NO se conserva** al borrar y recrear un campo. Como los flujos referencian por
  `var_ns`, borrar y recrear **rompe el flujo**.

## Tipos de campo y sus techos

| tipo | tope | UI |
|---|---|---|
| `text` | 20.000 | Text |
| `array` | 20.000 | JSON |
| **`longtext`** | **500.000** | **Long JSON** |

El tipo de un campo existente es **inmutable**: el selector está deshabilitado en el modal de
edición y no hay endpoint. Migrar = campo nuevo + repuntar la referencia.

**Todo campo NUEVO de configuración se crea `longtext`.**

## Lo que la API NO da

- **No hay saldo ni consumo.** 40 rutas probadas; `/flow/conversations/data` responde 200 y
  viene vacío. Un informe de gasto de Chatea por API no se puede hacer hoy.
- **No crea nodos ni subflujos.** Clonar es plantilla + `generate-one-time-link`.
- **No hay webhooks salientes** (los entrantes sí se listan).
- **No hay endpoint de subida de imágenes.** Las URL `media.chateapro.app` solo nacen subiendo
  el archivo en el panel.

## Lo que sí da y vale oro

- El mensaje de entrada trae `payload.referral` con `source_id` (**el ID del anuncio de Meta**),
  `headline`, `body` y `ctwa_clid`: la atribución sin tocar la API de Meta.
- Cada mensaje trae `msg_type` (`text`, `audio`, `feed` = comentario de Facebook,
  `button_template`) y, cuando es voz, `payload.transcribed_text` **con la transcripción ya
  hecha**. Guardar solo `content` convierte un audio en una comilla vacía.
- `[General] Payload del Agente` guarda la **última** respuesta del agente en el propio contacto.

## Seguridad

`GET /integration/openai|shopify|woocommerce|s3storage|calude|xai` devuelven las credenciales
**en texto plano**. Cualquiera con un token de bot lee todas las llaves del workspace. El
extractor de esta skill las redacta siempre. Nunca se pega una llave en un informe, ni en un
chat, ni en un archivo de trabajo.

Gotcha heredado del motor: la integración de Claude tiene **typo en la API oficial** —
`/integration/calude`. En el whitelabel `/integration/claude` da 404 y `/integration/calude` da 200.
