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
| `landings_*` | páginas/landings de producto | **golden-shopify** (Liquid, Releasit, embudo COD). Las `landings_*` de Ecom Magic son de su propio formato, no del tema Shopify: no las uses para la ficha COD. |
| `logos_generate` | identidad de marca | uso puntual; la identidad vive en el proyecto de marca |
| `spy_meta_search`, `spy_google_*`, `spy_tiktok_shop_search` | espionaje de anuncios de la competencia | **golden-ads** (pauta) y **golden-productos-ganadores** (validación) |
| `research_product`, `research_avatar`, `research_sales_angles`, `keyword_research` | investigación de mercado / avatar / keywords | **golden-investigacion-mercado**. EXCEPCIÓN útil: `research_generic_angle` es **gratis** y devuelve ángulo + mecanismo + resultado listos para los campos de `banners_generate` — eso sí úsalo aquí. |
| `financial_analyze` | unit economics | **golden-ads** / golden-finanzas |
| `video_transcribe`, `video_translate` | video | **golden-video-teardown** (análisis) / **golden-ugc-avatar** (producción) |

Cuando detectes que el usuario quiere algo de la columna derecha, **dilo y pasa la posta** a la
skill dueña (puedes mencionar que el MCP de Ecom Magic tiene una herramienta que ayuda).

## Nota de créditos

Todo lo que genera **cuesta créditos**; consultar (`*_list`, `*_get`, `help`, `account_me`,
`wallet_balance`, `research_generic_angle`) es gratis. Confirma el gasto antes de un lote y
reporta saldo al terminar (`wallet_balance`).
