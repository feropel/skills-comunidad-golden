# Vía MCP (PRINCIPAL) — Ecom Magic por herramientas, sin navegador

Ecom Magic AI expone **servidor MCP oficial** (`https://ecom-magic.ai/mcp/v1`, OAuth 2.1).
Conectado = ~73 herramientas nativas. Esta es la vía por defecto: **cero navegador, cero
handoff de foto, 100% autónoma**. El navegador queda solo como fallback (`ui-navegacion.md`).

## Conexión (una sola vez, la hace el usuario)

Claude → Configuración → Conectores → Agregar conector personalizado → URL
`https://ecom-magic.ai/mcp/v1`, Client ID y Secreto **vacíos** → Agregar → Conectar →
Autorizar. **Nunca pidas ni manejes una API Key**: OAuth no deja credenciales escritas
(regla de cero datos privados). Si el conector no aparece en la sesión, reiniciar la app.

Si las herramientas no están disponibles, cárgalas con ToolSearch (`banners`, `products`,
`jobs`, `templates`) y verifica con `account_me` / `wallet_balance`. Si el usuario no lo tiene
conectado, dale los 4 pasos de arriba; mientras, puedes operar por navegador.

## Herramientas clave (nombres cortos; el prefijo del servidor varía por sesión)

| Área | Tools | Notas |
|---|---|---|
| Cuenta | `account_me`, `wallet_balance`, `wallet_usage` | gratis; reporta créditos |
| Manual | `help(tool="...")` | **manual oficial con TODOS los inputs. GRATIS. Léelo antes de un campo dudoso** |
| Productos | `products_list`, `products_get`, `products_create`, `products_update` | guardan foto + contexto de marketing reutilizable |
| Plantillas | `templates_banner_list(source: ecom_magic\|mine\|mentor)` | `template_url` va directo como referencia |
| **Imágenes** | **`banners_generate`** (1 créd.), `banners_mass_generate` (2-30) | asíncrono → `job_id` |
| Piezas | `banners_list`, `banners_get`, `banners_download`, `banners_edit`, `banners_resize`, `banners_translate`, `banners_delete` | |
| Jobs | `jobs_get(job_id)` | polling cada 3-5 s |
| Assets | `assets_upload(purpose: banner_reference\|product_image)` | para archivos propios |
| Crédito | `refund_request` | si una pieza sale inservible |
| Extra | `logos_*`, `mockups_*`, `landings_*`, `research_*`, `spy_*`, `keyword_*`, `financial_*`, `video_*` | ver `capacidades-extra.md` |

## Flujo autónomo (el estándar)

1. `wallet_balance` → reporta créditos.
2. `products_list` → si el producto existe, **reutiliza su `id`**: trae foto y campos de
   marketing guardados (ahorra trabajo y mantiene coherencia). Si no, `products_create`.
3. `templates_banner_list` → elige `template_url` de referencia (heurística en
   `campos-generacion.md`). Para repetir un estilo que ya funcionó, reutiliza la misma URL de
   referencia (la ves con `banners_get` de una pieza previa).
4. `banners_generate` con los parámetros de abajo → devuelve `job_id`.
5. `jobs_get(job_id)` en bucle (3-5 s) hasta `succeeded`; el `output.url` es la imagen.
6. `curl` la URL → optimiza a **WebP < 150 KB** con `scripts/optimizar-webp.py` → entrega.

**La foto entra por URL pública** (`product_image_url`) — ej. el CDN de Shopify. Aquí está la
gran ventaja: **no hay que subir ni arrastrar nada**. Si solo hay archivo local, `assets_upload`.

## Parámetros de `banners_generate` (los que usamos)

**Obligatorio:** `reference_banner_url` (estilo a imitar).
**Foto:** `product_image_url` (+ `_2_url`, `_3_url`, hasta 3) o `product_id`.
**Formato:** `size_preset` — `1080x1080` (carrusel) · `1080x1920` (stories) · `1920x1080` (16:9
del cine) · `original` · `custom` (+`width`/`height` 64-4096). **Ojo: `1080x1350` NO es preset;
para vertical de secciones usa `size_preset:"custom", width:1080, height:1350`.**
**Idioma:** `language: "Spanish"`. **Motor:** `model: "ecomagic"` (default) o `"gpt-image-2"`.
**Calidad:** `thinking_mode: "advanced"` para piezas clave (vale la pena; mismo costo).
**Contexto:** `product_details`, `sales_angle`, `specific_problem`, `target_avatar`,
`ideal_solution`, `unique_mechanism`, `desired_outcome`, `additional_instructions`.
**Personajes:** `character_nationality` (ej. colombian), `character_sex`, `character_age_range`.
**Ángulo por IA:** `research_generic_angle` (GRATIS) devuelve ángulo + mecanismo + resultado.

### `awareness_level` — palanca de copy (Eugene Schwartz)
`unaware` · `problem_aware` · `solution_aware` · `product_aware` · `most_aware` · `random`.
Cambia CÓMO se escribe, sin tocar el ángulo. Con `most_aware`/`random` son **obligatorios**
`maw_price` y `maw_offer` (texto REAL ya formateado, respetando decimales de la divisa: COP sin
centavos). Opcionales `maw_satisfaction_guarantee`, `maw_quality_guarantee`,
`maw_free_shipping`. **Nunca inventes precio, oferta ni garantía.** Para carrusel/secciones de
ficha, `product_aware` o `solution_aware` suelen ir mejor que `most_aware`.

## Gotchas verificados en vivo

- 🔴 **ETIQUETA ALTERADA / INGREDIENTES INVENTADOS (el peligro nº1).** El generador puede
  **redibujar el envase y escribirle ingredientes falsos**. Caso real: puso "Ácido Salicílico ·
  Extracto de Té" en la caja de un producto que no los tiene. Verifica el texto del envase
  contra la etiqueta real en CADA pieza; si cambió, `refund_request` y regenera con
  *"No alteres la etiqueta del envase ni escribas ingredientes sobre el producto; conserva el
  texto original de la foto"*. Ver Ley 6 del SKILL.md.
- ⚠️ **`awareness_level` puede endurecer el claim.** Con `problem_aware` salió el titular
  alarmista "EL PROBLEMA SÍ EMPEORA SIN TRATAMIENTO". En salud/estética prefiere
  `solution_aware` o `product_aware`, y revisa el titular contra lo que el producto puede
  sostener legalmente.
- 🔴 **INVENTA PRUEBA SOCIAL Y CLAIMS — siempre, si no se lo prohíbes.** Evidencia de 3
  intentos consecutivos de UNA misma pieza: 1º ingredientes falsos en la etiqueta, 2º
  "Resultados Visibles Garantizados", 3º "MÁS DE 10.000 USUARIOS SATISFECHOS". Cada arreglo
  destapó una invención nueva. **Solución: la LISTA NEGRA completa en `additional_instructions`
  desde la PRIMERA llamada** (texto exacto en la Ley 6 del SKILL.md) — cifras, usuarios,
  porcentajes, testimonios, "garantizado/comprobado/certificado", claims médicos. Y **regla de
  corte: 2 fallos en la misma pieza = se entrega el set sin ella.**
- ⚠️ **`banners_edit` re-renderiza TODO y degrada el texto pequeño.** Verificado: al corregir una
  línea, devolvió 2048×2048 y el texto fino de la etiqueta quedó ilegible (garabato). Sirve para
  cambios de bloques grandes (titular, un beneficio, color); **para piezas donde la etiqueta del
  producto se lee, es mejor REGENERAR** con las instrucciones corregidas que editar. Cobra 1
  crédito igual y crea una pieza nueva (no borra la original).
- **`¡` y `¿`:** el generador los mete por defecto (salió "¡FÁCIL DE APLICAR!"). La regla Golden
  los prohíbe → escribe SIEMPRE en `additional_instructions`: *"No uses signos de apertura ¡ ni
  ¿; solo el de cierre."* Verifica el render y usa `banners_edit` si aparecieron.
  (Nota: la instrucción funciona — las piezas siguientes salieron limpias.)
- **`size_preset` manda** sobre `size_mode`/`width`/`height` (salvo `custom`).
- Un `1080x1080` puede volver como **1024×1024**: se corrige al optimizar (el script redimensiona).
- **Asíncrono siempre:** nada de asumir que ya está; poll `jobs_get`. Cobra 1 crédito **al éxito**.
- Los campos de marketing quedan **guardados en el producto** — al reutilizar `product_id`
  heredas contexto (y también `saved_additional_instructions`: revísalo, puede traer
  instrucciones de OTRA pieza; sobreescríbelo explícitamente en cada llamada).

## Masivo

`banners_mass_generate` = 2-30 piezas con los MISMOS parámetros (cobra 1 por pieza). Útil para
variantes del mismo concepto. Para piezas **distintas**, llama `banners_generate` N veces.
Confirma el gasto total con el usuario antes de un lote.
