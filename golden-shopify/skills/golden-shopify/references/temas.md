# Adaptador de temas

La regla de oro: **los bloques `custom-liquid` funcionan en cualquier tema sin
cambios.** Solo se adapta lo nativo. Esta tabla es lo único que cambia entre temas.

**Temas soportados (preguntar SIEMPRE cuál es). 2 familias:**
- **Familia clásica (product.json pega):** **Dawn** (base) · **Shrine / Shrine Pro** · **Sense**.
- **Familia NUEVA (product.json NO pega → bloques Custom Liquid):** **Horizon** · **Pitch**.
- **Otro:** fallback genérico; si parece OS 2.0 clásico trátalo como Dawn/Sense, si parece
  nuevo (estilo Horizon) trátalo como Horizon/Pitch.

## ⚠️ HORIZON y PITCH — arquitectura NUEVA de Shopify (NO es como Dawn!)
Horizon, **Pitch** y su familia (2024+) usan una **arquitectura distinta**: el `product.json`
estilo Dawn/Shrine **NO encaja** (otra estructura de secciones/bloques, otro esquema). NO
intentes pegar nuestro `product.json` completo en un tema Horizon/Pitch.

> Detalle de la arquitectura block-based de Horizon (theme blocks nativos, `@theme`/`@app`,
> `block.shopify_attributes`, presets anidados, cuándo entregar como theme block vs `custom_liquid`)
> en **`references/horizon-bloques.md`**. Aquí solo va el adaptador general entre temas.

**Cómo entregar en Horizon / Pitch:**
- **Entregar por BLOQUES Custom Liquid sueltos**, no como product.json completo. El usuario
  agrega secciones/bloques "Custom Liquid" en el editor de Horizon y pega cada componente.
- Todos nuestros `componentes/*.liquid` siguen sirviendo (son HTML/CSS/JS portables) → se
  pegan uno por uno en bloques Custom Liquid de Horizon.
- El config center va primero (un Custom Liquid arriba) para que los tokens `:root` apliquen.
- Tickers, footer override, relacionados: usar los `custom-liquid` (no asumir clases de Dawn).
- Releasit COD funciona igual (depende de la app, no del tema).
- **Avisar al usuario**: en Horizon/Pitch se entrega "por piezas" para pegar en el editor, no
  un único archivo de plantilla. (Ver memoria del proyecto del suplemento en tema Pitch/Horizon.)
- Si dudas de un selector nativo de Horizon/Pitch, **inspeccionar / preguntar**, no asumir Dawn.

## Tabla maestra

| Pieza | **Dawn** (base) | **Shrine / Shrine Pro** | **Sense** | **Otro / desconocido** |
|---|---|---|---|---|
| Tickers | sección `custom-liquid` (`dawn-ticker.liquid`) | sección nativa `horizontal-ticker` | como Dawn (`custom-liquid`) | `custom-liquid` |
| Título | `custom-liquid` (`dawn-titulo.liquid`) o bloque `title` nativo | bloque `title` nativo (con `title_highlight_color`, etc.) | bloque `title` nativo o custom | bloque `title` nativo si existe, si no custom |
| Footer override (CSS) | `.footer` | `.shopify-section-group-footer-group` | `.footer` | inspeccionar; probar `.footer`, `footer`, `.shopify-section-group-footer-group` |
| Descripción | bloque `description` nativo | bloque `description` nativo | nativo | nativo |
| Relacionados | sección `related-products` nativa | `related-products` nativa | nativa | nativa |
| Color scheme | `"scheme-1"` | esquema de Shrine | `"scheme-1"` | el default del tema |

## Settings que son SOLO de Shrine (ignóralos/quítalos en Dawn/Sense)
`title_highlight_color`, `arrows_color_scheme`, `transparent_arrows`, y la sección
`horizontal-ticker`. En Dawn/Sense producen warnings o se ignoran. Si migras de
Shrine → Dawn, **borra esos settings** y reemplaza los `horizontal-ticker` por
secciones `custom-liquid` con `dawn-ticker.liquid`.

## Qué SOBREVIVE cualquier migración (no tocar al cambiar de tema)
- Todos los bloques/secciones `custom-liquid` (propuesta, oferta, countdown,
  verificado, precio, botón, garantía, logística, sticky, cómo actúa, reseñas,
  manifiesto, FAQ, beneficios).
- El override de colores de Releasit (depende de la app, no del tema).
- El brillo del botón, el sticky, el JSON-LD.
- El config center.

## Qué se ROMPE al migrar Shrine → Dawn (los puntos a arreglar)
1. `type: "horizontal-ticker"` no existe en Dawn → reemplazar por sección
   `custom-liquid` con `dawn-ticker.liquid`.
2. `.shopify-section-group-footer-group` (footer Shrine) → en Dawn es `.footer`.
3. `title_highlight_color`/`arrows_color_scheme`/`transparent_arrows` → quitar.
4. El bloque `title` nativo existe en ambos pero con settings distintos → revisar.

## Fallback para tema desconocido
1. Mete TODOS los `custom-liquid` tal cual (entran en cualquier tema vía secciones
   `custom-liquid` y bloques `custom_liquid` del `main-product`).
2. Para lo nativo, usa los selectores estándar de Shopify y prueba `.footer` /
   `footer` para el override.
3. **Avisa al usuario** qué piezas nativas no pudiste confirmar y pídele una captura
   o que te diga el nombre del tema para afinar.

## Cómo detectar el tema de un cliente

### A) Desde la URL en vivo (HACER SIEMPRE antes de construir)
Si tienes la URL del producto/tienda, detecta el tema del HTML — no lo asumas. El marcador
más fiable es el objeto `Shopify.theme` que Shopify inyecta en toda página. Receta:
1. Trae el **HTML crudo** (firecrawl `rawHtml` con `onlyMainContent:false`, o `curl -s URL`).
   El HTML es enorme; si excede el límite, guárdalo a archivo y usa `grep` (no lo leas entero).
   > ✅ **`rawHtml` es la vía honesta y hay que mantenerla así.** No pasa por el extractor de
   > Firecrawl, así que es **inmune** a la Regla Cero (que con `formats:["json"]` puede devolver
   > datos **inventados** o el menú de otra página, con `statusCode: 200` — medido 2026-08-01).
   > Aquí lo que ves en el `grep` está literalmente en el HTML. **Nunca cambies este paso a `json`**
   > para "que sea más cómodo": perderías esa garantía justo donde importa (detectar el tema mal
   > lleva a construir la ficha sobre bloques que no existen).
   > 📖 `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`
2. Busca, en orden de fiabilidad:
   - `Shopify.theme = {"name":"…","schema_name":"…"}` → el `schema_name` dice el tema
     (ej. `"Shrine"`, `"Dawn"`, `"Sense"`). Es la fuente de verdad.
   - Clases de esquema de color: `color-background-1` → **Shrine**; `color-scheme-1` → **Dawn/Sense**.
   - `horizontal-ticker` en el HTML → sección **exclusiva de Shrine**.
   - `_rsi-buy-now` → confirma que Releasit COD está instalado.

   Comandos útiles (sobre el archivo guardado):
   ```bash
   grep -o 'Shopify.theme = {[^}]*}' archivo.html | head -1
   grep -oiE 'shrine|dawn|sense' archivo.html | sort | uniq -c | sort -rn
   grep -oE 'color-(background-[0-9]|scheme-[0-9])' archivo.html | sort | uniq -c
   ```
3. Mapea el resultado al adaptador: **Shrine** → construyes directo sobre la base PRODUCTO
   DEMO (es su tema nativo, SIN adaptador). **Dawn/Sense** → aplica la conversión de arriba.

### B) Desde un `product.json` pegado
- Busca `type: "horizontal-ticker"` o `.shopify-section-group-footer-group` → es **Shrine**.
  Si los tickers son `custom-liquid` y el footer es `.footer` → **Dawn/Sense**.

### C) Otras vías
- Si da acceso al admin / nombre del tema, úsalo directo.
- Ante la duda, pregúntale: "Qué tema usa la tienda?".

## Paddings THEME-SAFE (evita "Setting 'padding_top' must be a step in the range") — G3.2
Cada tema define su propio **rango y paso** para `padding_top`/`padding_bottom` de las secciones.
Shrine (y algunos temas) usan un rango MENOR que Shrine Pro/Dawn → un valor como `40` los rompe al
guardar el `product.json`.
- **Regla:** en las secciones, no fijes paddings mayores a **36** ni valores que no sean múltiplos de 4.
  El `base.json` ya viene clampeado a ≤36. Si dudas, **no fijes `padding_top`/`padding_bottom`** y deja
  que el tema use su default (nunca falla).
- **Si un tema los rechaza igual** (rango aún menor), quita esos ajustes de TODAS las secciones:
  ```python
  import json
  j=json.loads(open("product.json").read().split("*/\n",1)[-1])
  for s in j["sections"].values():
      s.get("settings",{}).pop("padding_top",None); s.get("settings",{}).pop("padding_bottom",None)
  ```
  El contenido no cambia; solo el espaciado lo pone el tema.
