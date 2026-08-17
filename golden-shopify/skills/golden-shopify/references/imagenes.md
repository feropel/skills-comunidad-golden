# Imágenes — cómo dejar la página "todo listo"

La meta: entregar la página con el máximo "listo" posible, sin inventar el producto.

## Modo imágenes — PREGUNTAR al usuario (2 opciones)
Al construir, ofrecer explícitamente:
> **Quieres que genere las imágenes decorativas (requiere herramienta de imágenes
> conectada y puede tener costo de API), o las pones tú / vamos sin imágenes?**
- **Opción A — Con imágenes:** verificar si hay herramienta de imagen conectada (p.ej.
  `mcp__stitch__generate_design_asset` / Gemini, o Canva). Si SÍ → generar lo **decorativo**
  (las infografías de producto van por `golden-imagen-arena`). Si NO →
  **avisar que no es posible porque no hay API/herramienta de imágenes conectada**, dar
  2-3 sugerencias breves (abajo) y **seguir igual** con slots/placeholders.
- **Opción B — Sin generación (el cliente ya tiene imágenes):** **pedir las URLs/links**, o
  **reutilizar la galería/multimedia del producto** (leer el media del producto por el MCP de
  Shopify y usar esas URLs en los bloques). No inventar; no tocar la descripción.
Luego continuar con el resto de preguntas normales.

**Dónde van las imágenes (decisión por defecto):** **bloques de la landing + galería/multimedia
del producto**. La descripción nativa se mantiene oculta (recreada en bloques) → las imágenes NO
van dentro del texto de la descripción.

> ⚠️ **REGLA DE ORO ESCALERA/CINE (G3.3, lección de la página real de verrugas):** los componentes
> **Escalera** (`P1_IMG…P5_IMG`) y **Cine** (fondo) usan **URLs NUEVAS dedicadas**, NUNCA las
> `<img>` de la **descripción** (el cliente maneja **infografías** ahí → se duplicarían y la página
> se ve rota). Reusar la **galería oficial** solo es válido para el HERO. Sin URL propia, la escalera
> queda como **tarjeta de solo texto** (limpia) y el cine con **gradiente de marca** — nunca vacío.
> Specs: WebP <150 KB, con width/height + alt, `loading="lazy"` bajo el pliegue (sin CLS).

## Pipeline AUTOMÁTICO probado (Nano Banana Pro → Shopify) — v1.20
Cuando el usuario elige **CON generación** y hay API de Gemini conectada, este flujo deja TODO
integrado solo (probado en tienda demo / producto demo, jun 2026):

**0. Conexión = la mejor forma, estable.** Generar con **Gemini API key** del proyecto del
usuario, modelo **`gemini-3-pro-image` (Nano Banana Pro)**. NO depender del conector
"stitch/Antigravity" (su token pierde el `project_id` y se cae). La key va en `~/.gemini_key`
(el usuario la crea en aistudio.google.com/apikey; **nunca** pegarla en el chat). Verificar con
`GET generativelanguage.googleapis.com/v1beta/models?key=…`.

**1. Generar.** POST a
`…/v1beta/models/gemini-3-pro-image:generateContent?key=KEY` con
`{"contents":[{"parts":[{"text":PROMPT}{, inlineData del frasco si aplica}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"4:3"}}}`.
La imagen vuelve en `candidates[0].content.parts[].inlineData.data` (base64) → guardar PNG.
- **Producto real (REGLA #3):** para tomas del frasco, pasar la foto real como `inlineData` y
  pedir *"keep the label intact"* → compone sin inventar el envase.
- Set base salud/COD (5): problema (persona), confianza, fórmula (frasco real), modo de uso,
  frescura/ingrediente. Prompts en inglés rinden mejor; siempre *"no text, no logos"*.

**2. Optimizar <300 KB.** Pillow: resize ~1200px, JPG progresivo q=85 (baja q hasta <295 KB).

**3. Subir a Shopify Files por API (deja la URL exacta que espera la plantilla):**
   a. `stagedUploadsCreate(input:[{resource:IMAGE,filename:"01_problema.jpg",mimeType,httpMethod:POST}])` → `url`+`parameters`+`resourceUrl`.
   b. POST multipart a `url` con TODOS los `parameters` + `file=@local` (curl) → 201.
   c. `fileCreate(files:[{originalSource:resourceUrl,contentType:IMAGE,filename:"01_problema.jpg",duplicateResolutionMode:REPLACE,alt}])`.
   d. URL final = `cdn.shopify.com/s/files/1/<storeid>/files/<filename>` (carga sin `?v=`).
   🔑 **Truco:** nombrando `01_problema.jpg`…`05_frescura.jpg`, las URLs son **predecibles** →
   se escriben en el JSON ANTES de subir y todo encaja solo.

**4. Galería del producto:** `productCreateMedia(productId, media:[{originalSource:<cdn url>,mediaContentType:IMAGE,alt}])`.

**5. Tema:** la plantilla referencia esas URLs en los bloques. ⚠️ El MCP de Shopify **BLOQUEA
escribir el tema LIVE/MAIN** (seguridad) → el `product.json` final lo **pega el usuario** en
*Editar código → templates* (o se sube a un tema borrador). Las imágenes y la galería SÍ se
cargan por API; solo el theme file live es manual.

### Errores reales y su fix (no repetir)
| Síntoma | Causa | Fix |
|---|---|---|
| `Antigravity project ID not found` | conector stitch pierde el project | usar **API key** directa, no stitch |
| `insufficient authentication scopes` | token gcloud sin scope de la API | usar **API key** (`?key=`), no OAuth |
| Vertex 403 `aiplatform … disabled` | Vertex no habilitado | usar **generativelanguage** (Gemini API) |
| `429 prepayment credits depleted` | proyecto sin saldo | el usuario **recarga** (centavos/imagen) |
| Botón COD muerto | producto **agotado** | inventario>0 o "seguir vendiendo agotado" |
| Sticky pegado arriba | ancestro con `transform` rompe `position:fixed` | `document.body.appendChild(bar)` |

## Portabilidad / seguridad (importante al COMPARTIR la skill)
La skill son **solo archivos de texto**: NO contiene API keys ni conexiones. Si el usuario
comparte la skill, **la otra persona NO hereda su API** — debe conectar la suya. Por eso, si
alguien elige "generar imágenes" y no tiene herramienta conectada, la skill debe decir, en
**1 línea general** (sin tutorial largo): "No hay una herramienta de imágenes conectada en tu
espacio. Para activarla puedes conectar un MCP de imágenes (ej. Gemini/stitch, Canva o similar)
desde la configuración de tu Claude; mientras tanto seguimos con slots para que pegues tus
imágenes." No explicar más de eso (mantener la skill ligera).

## Regla de oro de imágenes (alinea con REGLA #3 anti-invención)
- **El producto REAL lo aporta el usuario** (fotos del proveedor/dropshipping). La IA
  **NO inventa** el frasco/caja/producto desde texto: saldría un producto falso. Si el
  usuario da 1 foto real, se puede *mejorar/componer* (fondo estudio, lifestyle), no crear.
- **Las infografías NO van como imagen**: se construyen en **HTML/CSS** dentro de la página
  (cómo funciona, ingredientes, antes-después, pasos, comparativa, beneficios). Ventaja:
  editable, rápido, SEO. (Es justo lo que hacen los componentes de la skill.)
- **La IA SÍ genera lo decorativo**: fondos, hero de ambiente, íconos, patrones, texturas,
  ilustraciones de ingredientes — porque no representan al producto real.

## Qué necesita la skill para una página completa
1. **Fotos reales del producto** (el usuario las da): al menos hero + 2-3 (en uso, detalle,
   empaque). Si no las tiene, **PREGUNTAR** y dejar slots marcados; no inventar.
2. **Assets decorativos** (opcional): generables con IA si se quieren (ver herramientas).
3. **Hosting**: toda imagen referenciada en el JSON va por URL → subir a **Shopify →
   Configuración → Archivos** (o vía el MCP de Shopify que sube a la CDN) y pegar la URL.

## SET DE IMÁGENES DE LANDING GANADORA (specs del usuario + patrón real)

### Specs técnicas (del usuario — respetar SIEMPRE)
- **Galería multimedia (arriba, fotos del producto):** **4–6 imágenes CUADRADAS 1080×1080**,
  cada una **< 300 KB**. Optimizar peso (WebP/compresión) sin perder nitidez.
- **Infografías de la DESCRIPCIÓN:** formato **VERTICAL 1080×1350** (4:5). ~8–10 paneles.
- Se producen con **golden-imagen-arena** o el usuario las aporta. La skill las
  **coloca y ordena**, NO las duplica en HTML (ver [[no duplicar infografías]]).

### Galería (1080×1080) — qué suele ir (4–6)
1. Producto principal (PNG real sobre fondo limpio). 2. Banner de gancho/beneficio.
3. Beneficios clave. 4. Antes/después o resultado. 5. Ingredientes/fórmula. 6. Banner promo.

### Descripción (1080×1350) — orden narrativo GANADOR (patrón PAS, ~10 infografías)
1. **Hook / dolor** identificable ("escondes la mano", "te da pena").
2. **Problema agravado**: intentos fallidos ("ya intentaste casi todo…").
3. **Mecanismo / por qué fallan los demás** (ej. "no lo atacaste desde la raíz").
4. **Beneficio emocional** (la promesa: "piel libre, sin esa verruga").
5. **Usos / para qué sirve** (manos, pies, etc.).
6. **Contraindicaciones / advertencias** (embarazo, piel sensible…) → da confianza.
7. **Comparativa** vs alternativas (sin cirugía, sin dolor, sin cicatrices).
8. **Ingredientes / activo estrella** (natural).
9. **Garantía / confianza** (pago contra entrega, sellado, original).
10. **CTA final** ("PEDIR AHORA" + beneficio).

Adaptar el guion al producto (REGLA #1: distinto por producto), pero mantener el **arco
PAS**: dolor → problema → mecanismo → prueba → ingredientes → garantía → CTA.

### Cómo lo usa la skill
- Deja **slots** para galería (`[IMG 1080x1080: ...]` ×4-6) y para las infografías de
  descripción (`[INFO 1080x1350: hook]`, etc.) en el orden de arriba.
- En las **secciones en código** NO repite lo que la infografía ya dice; complementa
  (countdown, precio dinámico, sticky, reseñas editables, FAQ, garantía).

## Herramientas disponibles (según el entorno)
- **`mcp__stitch__generate_design_asset`** (Gemini): hero, background, illustration, icon,
  pattern. Ideal para lo decorativo y fondos. Soporta quitar fondo (logos/íconos).
- **Canva `generate-design`** (`infographic`, `poster`, etc.): piezas gráficas con texto.
  Ojo: el texto dentro de imagen puede salir mal → preferir HTML para texto clave.
- **MCP de Shopify (imágenes)**: subir imágenes a la CDN de Shopify para obtener URL.
- Si ninguna está conectada, generar los assets aparte y subirlos a Shopify → Archivos.

## Flujo "todo listo"
1. **Construir la página** (JSON) con infografías en HTML y **slots de imagen marcados**
   con placeholder evidente: `[IMG: hero del producto]`, `[IMG: producto en uso]`, etc.
2. **Fotos del producto:** el usuario las sube a Shopify → Archivos y pega las URLs en los
   slots (o usa la galería nativa del producto para el hero).
3. **Decorativo (opcional):** generar con IA fondos/íconos/ilustraciones, subir a Shopify,
   pegar URLs.
4. **Avisar** qué quedó pendiente de imagen (slots sin URL) — nunca dejar un slot con una
   imagen inventada del producto.

## Convención de slot de imagen en los componentes
Cuando un bloque necesite una imagen real, dejar la variable Liquid arriba y un placeholder
visible si está vacía, p.ej.:
```liquid
{% assign IMG_HERO = "" %}  {# pega aquí la URL de Shopify Archivos #}
...
{% if IMG_HERO != "" %}<img src="{{ IMG_HERO }}" alt="..." loading="lazy" decoding="async" width="..." height="...">
{% else %}<div class="img-slot">[IMG: hero del producto — pega la URL]</div>{% endif %}
```
Así la página queda lista y el usuario solo pega URLs, sin imágenes falsas.

## Lo que NO se hace
- No generar una foto "realista" del producto desde texto (inventa el producto).
- No meter el copy importante dentro de una imagen (mata SEO y edición) — va en HTML.
- No dejar slots con stock genérico que no es el producto, haciéndolo pasar por real.
