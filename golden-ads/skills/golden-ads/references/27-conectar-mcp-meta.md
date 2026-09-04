# 27 · Conectar el MCP de Meta (la ruta oficial) + el CANDADO de presupuesto

**Todo lo de este archivo está VERIFICADO contra la fuente autoritativa de Meta el 2026-09-03:**
`developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/*`
(actualizado 14-jul-2026) y `facebook.com/business/help/1456422242197840`. Nada aquí viene de
terceros ni de tutoriales.

La skill entera asume "el MCP de Meta está conectado" y **nunca decía cómo conectarlo**. Este es el
primer archivo que necesita alguien que instala la skill y todavía no tiene la cuenta enlazada.

---

## La URL del servidor (única, oficial, remota)

```
https://mcp.facebook.com/ads
```

Servidor **alojado por Meta**. Sirve para todos los clientes soportados.

**Clientes soportados oficialmente por Meta** (los que la propia página lista): **ChatGPT ·
Claude · Claude Code · Perplexity**. Fuera de esos cuatro, Meta manda a la documentación de
desarrollador. *(No confirmados por Meta: Cursor y Codex — no aparecen en la lista oficial.)*

---

## Vía A · SIN app de desarrollador (la normal, la que usa un alumno)
Es la ruta de **Meta ads AI connectors**. Se pega la URL en el panel de conectores del cliente y se
inicia sesión con la cuenta de Meta. No hace falta crear ninguna app.
→ Guía de Meta: `facebook.com/business/help/1456422242197840`

## Vía B · CON app propia (Claude Code, comando exacto)
1. Crear o reutilizar una app en `developers.facebook.com/apps` y añadirle el caso de uso
   **"Create & manage ads with ads MCP server"**.
2. Añadir el servidor:
```
claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads
```
3. Autenticación: **OAuth** (el cliente abre el diálogo de Facebook Login for Business; hay que tener
   configurada la *redirect URL* de la app) o **token de usuario** por
   `Authorization: Bearer <ACCESS_TOKEN>`.
4. Permisos que hay que conceder al pedir el token (lista textual de Meta):
   `ads_mcp_management` · `ads_read` · `ads_management` · `catalog_management` ·
   `business_management` · `pages_show_list` · `instagram_basic`

## VERIFICAR que quedó (el paso que nadie hace)
Pregúntale al agente **qué herramientas tiene**. Si lista las `ads_*`, quedó conectado. En esta skill
el equivalente es `ads_get_ad_accounts`: si responde con cuentas, hay conexión (ver `11`).
> Prompts de arranque que sugiere Meta: *"List my ad accounts"* · *"Summarize the top-spending
> campaigns in `<AD_ACCOUNT_ID>` over the last 30 days"*.

---

## 🔒 EL CANDADO DE PRESUPUESTO — la red de seguridad del error de los 100×

**Este es el hallazgo que más plata protege de todo el archivo.** Meta permite fijar **reglas por
cuenta publicitaria que el propio servidor MCP hace cumplir** — bloquean la acción del agente aunque
el agente se equivoque:

**Dónde:** Meta Business Suite → **Settings** → *Integrations* → **Ads MCP server** → elegir la
cuenta → permitir o bloquear acciones. *(Si no aparece la opción, la cuenta todavía no la tiene.)*

**Lo que se puede bloquear** (ejemplos textuales de Meta):
- **Create campaigns** → Blocked: el agente no puede crear campañas.
- **Edit or set budget** → Blocked: ningún cambio de presupuesto.
- 🔴 **"Budgets set above this amount"** → poner un **techo máximo**. Meta rechaza cualquier intento
  por encima de esa cifra.

> **Aplicación directa al incidente del 2026-09-03** (se pidieron $50.000/día y se pusieron
> $5.000.000): con un techo de, por ejemplo, $200.000 configurado ahí, **Meta habría rechazado el
> intento** en vez de aceptarlo. La regla de releer el presupuesto del servidor (`reglas-de-oro.md`
> §5) sigue siendo obligatoria — pero esto es el cinturón además del airbag.
> **Recomendación Golden: dejar un techo de presupuesto puesto en cada cuenta operativa.**

**Implicación de agencia:** quien recibe acceso de socio a una cuenta también puede fijar reglas del
MCP sobre las cuentas compartidas, y esas reglas aplican solo a sus propios usuarios.

---

## Lo que Meta confirma y refuerza de esta skill
- **"All ads are paused by default until you set them live"** — la doctrina de pausa-primero
  (REGLA 3) no es una manía de la casa: es el comportamiento oficial del servidor.
- **"Any actions taken on your behalf require your authorization"** — coincide con "confirmar antes
  de gastar".
- **Sobre el miedo al baneo:** Meta dice explícitamente que **usar el MCP no pone la cuenta en
  riesgo**; los baneos vienen de violar políticas de publicidad, no de conectar un agente. Útil para
  responderle a un alumno que pregunta si "lo van a banear por conectar Claude".

## Lo que este archivo NO afirma (por honestidad)
- **No hay evidencia** en las dos páginas oficiales leídas de alcances llamados "Read" / "Manage":
  lo que existe es el control por ACCIÓN en Business Suite descrito arriba. Si alguien cita esos
  nombres, pedir la fuente.
- **No se encontró** en esas páginas la advertencia sobre inyección de instrucciones vía contenido
  no confiable. La cautela sigue siendo buena práctica de la casa (y por eso todo nace en pausa),
  pero **no se le atribuye a Meta** mientras no aparezca en su documentación.

Relacionado: `01-fuentes-datos.md` (detectar si hay MCP) · `11-mcp-meta-recipe.md` (cómo leer sin
fallar) · `reglas-de-oro.md` §5 (presupuesto) · `05-publicar-mcp.md` (crear en pausa).
