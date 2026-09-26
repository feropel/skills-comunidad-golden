# Capacidades extra del MCP (más allá de las imágenes)

El MCP de Ecom Magic trae mucho más que `banners_*`. Esta skill **manda en imágenes de
producto**; para el resto, la regla es: **úsalo si evita trabajo, pero respeta la frontera de la
skill dueña del tema** (no dupliques). Antes de usar cualquiera, `help(tool="...")` — gratis.

## Lo que SÍ es de esta skill

| Tool | Para qué | Costo |
|---|---|---|
| `banners_*` | **el núcleo**: imágenes de producto (ver `mcp-api.md`) | 1 créd./pieza |
| `mockups_generate` | producto sobre soporte físico (empaque, escena de mockup) | ver `help` |
| `banners_resize` | misma pieza en otro tamaño sin rehacer el diseño | ver `help` |
| `banners_translate` | versión en otro idioma (útil para vender el mismo producto en otro país) | ver `help` |
| `banners_edit` | corregir una pieza ya generada (quitar texto, cambiar color, sacar un `¡`) | ver `help` |
| `assets_upload` | subir referencia propia o foto local | gratis |
| `refund_request` | recuperar el crédito de una pieza inservible | gratis |

## Lo que pertenece a OTRA skill (delegar, no competir)

| Tool del MCP | Tema | Skill dueña |
|---|---|---|
| `landings_*` | páginas/landings de producto | **golden-shopify** (Liquid, Releasit, embudo COD). Las `landings_*` de Ecom Magic son de su propio formato, no del tema Shopify: no las uses para la ficha COD. **PERO no descartes el módulo entero:** ver `landings_logistics_options` abajo. |
| **`landings_logistics_options`** | transportadoras y medios de pago REALES por país | **de esta skill, como DATO para el handoff.** GRATIS y sin IA (lo dice su propio manual). Devuelve, por país ISO-2, los `carriers`, los `payment_methods` y el `default_payment_mode`. **Ejecutado 2026-09-05, `country:"CO"` → Servientrega · Envía · Coordinadora · Interrapidísimo · TCC; PSE · Nequi · Daviplata · Visa · Mastercard; modo por defecto `cod`.** Esa es exactamente la barra logística de la ficha COD: **córrelo y pásale la lista a golden-shopify** en vez de que alguien escriba transportadoras de memoria. Sin `country` devuelve los 20 países (útil para Panamá, México, Chile). |
| `logos_generate` | identidad de marca | uso puntual; la identidad vive en el proyecto de marca |
| `spy_meta_search`, `spy_google_*`, `spy_tiktok_shop_search` | espionaje de anuncios de la competencia | **golden-ads** (pauta) y **golden-dropkiller-productos-ganadores** (validación) |
| `research_product`, `research_avatar`, `research_sales_angles`, `keyword_research` | investigación de mercado / avatar / keywords | **golden-investigacion-mercado**. EXCEPCIÓN útil: `research_generic_angle` es **gratis** y devuelve ángulo + mecanismo + resultado listos para los campos de `banners_generate` — eso sí úsalo aquí. |
| `financial_analyze` | unit economics | **golden-ads** / golden-finanzas mandan en la DECISIÓN de precio. Pero el instrumento es **GRATIS, SÍNCRONO y sin IA** (manual oficial: "NO consume créditos") — no es un job, responde de una. Con `analysis_type:"cod"` + `country` + `cost_per_unit` devuelve precio de venta para 1/2/3 unidades con `breakEvenROAS`, `cpaObjetivo` y el desglose de flete, comisión de recaudo, cancelaciones, devoluciones, garantías y chargebacks. **Córrelo cuando te sirva y entrega el número; lo que no haces aquí es decidir el precio.** |
| `video_transcribe`, `video_translate` | video | **golden-video-teardown** (análisis) / **golden-ugc-avatar** (producción) |

Cuando detectes que el usuario quiere algo de la columna derecha, **dilo y pasa la posta** a la
skill dueña (puedes mencionar que el MCP de Ecom Magic tiene una herramienta que ayuda).

## Nota de créditos

Todo lo que genera **una pieza** cuesta créditos. Es GRATIS: `*_list`, `*_get`, `help`,
`account_me`, `wallet_balance`, `assets_upload`, `refund_request`, `research_generic_angle`,
**`financial_analyze`** y **`landings_logistics_options`**. Confirma el gasto antes de un lote y
reporta saldo al terminar (`wallet_balance`).

🔴 **No supongas que algo cuesta.** Estas dos últimas estaban delegadas sin decir que eran
gratis, y "todo lo que genera cuesta créditos" las hacía parecer caras: una calculadora y un
listado de transportadoras quedaron sin usar por una frase, no por una medición. Ante la duda,
`help(tool="...")` dice el costo y no cobra nada. **Verificado 2026-09-05: `wallet_balance`
antes y después de correr `help` + `landings_logistics_options` = 394 y 394.**
