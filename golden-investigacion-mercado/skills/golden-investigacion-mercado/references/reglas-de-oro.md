# Reglas de oro — Investigación de Mercado PURA

(Reescritas en G5.1 para el rol post-split: esta skill INVESTIGA y entrega la verdad del producto.
La ejecución — página, creativos, pauta, bot, montaje — vive en `golden360` y sus especialistas.)

## 1. Anti-invención + fuentes (la regla que más valor protege)
- **Cada dato lleva su fuente** (URL, nombre del sitio, fecha de consulta). Reseñas, competidores,
  precios, tamaño de mercado, claims, cifras: todo citado.
- Lo que **no se pudo verificar** se escribe como *"hipótesis (sin fuente confirmada)"* — nunca como
  hecho. Un estudio que mezcla datos reales con inventados es peor que no tener estudio.
- **Reseñas y comentarios reales**: se transcriben textuales con su origen (los de otro idioma,
  traducidos y marcados *(traducida)*). Si no se hallan, se dice "no se hallaron" y se propone cómo
  conseguirlos — jamás se inventan.
- **La ficha vieja es FUENTE CONTAMINADA**: sus specs/claims entran como `claims.no_verificables`
  hasta contrastar con etiqueta/INCI del fabricante (detalle e incidente real en
  `00-identificacion-forense.md`).
- 🚨 **EL SCRAPER TAMBIÉN INVENTA — y falla de 3 formas distintas.** No basta con no inventar tú:
  la herramienta lo hace sola, y `statusCode: 200` no prueba nada. Los 3 modos, todos medidos:
  1. **Alucinación** — página hueca → el extractor **inventa** un resultado completo. Medido
     (2026-07-31): la ficha de un removedor de verrugas en AliExpress devolvió *"Smart TV 55\" 4K
     LED, $499.99, rating 4.5, 150 reseñas"*. Todo falso. *Tell: `metadata.title` vacío.*
  2. **Señuelo** — redirige y te entrega el menú de otra página. Medido (2026-08-01): buscando
     "wart remover" en Temu devolvió **72 categorías de ropa** con precio "N/A".
     ⚠️ *Aquí `title` viene POBLADO: la verificación del modo 1 pasa en verde.*
     *Tell: `metadata.url` ≠ `sourceURL`, valores "N/A" en masa.*
  3. **Muro anti-bot** — Amazon: la respuesta **no trae campo `json`**, con title poblado Y sin
     redirección. *Tell: no existe `json`.*

  **Verificación obligatoria antes de usar CUALQUIER dato scrapeado — las 4, en orden:**
  existe el campo `json`? · `metadata.title` poblado? · `metadata.url` == `sourceURL`? ·
  **🎯 el dato responde a lo que pedí?** (la única que caza los tres modos).
  Si falla una: descartar, no citar, no meter en `PRODUCTO.json`. Se escribe "no obtenido" y se
  propone otra vía. **Excepción:** `formats:["rawHtml"]` no pasa por el extractor → inmune a los
  modos 1 y 2; si solo necesitas buscar una cadena, pide rawHtml y usa `grep`.
  📖 Manual completo: `scraping-firecrawl.md` (matriz de fuentes medida, recetas, coste).

## 2. Exhaustividad: no omitir, complementar
- Si un elemento relevante no fue pedido, **se investiga igual**. Antes de cerrar cada fase:
  *"qué le falta a esto para que alguien construya y venda sin volver a preguntarme nada?"*

## 3. Apoyos de investigación (leídos EN VIVO, última versión)
| Necesidad | Apoyo | Si falta |
|---|---|---|
| Validar demanda | `golden-productos-ganadores` | Ad Library + TikTok Creative Center a mano |
| Pauta previa del dueño | `golden-meta-ads-analysis` | leer el export a mano, marcar `(estimado)` |
| Pedidos reales (COD) | `golden-dropi-analisis` | pedir el export y leerlo directo |
| Inventario de archivos | `golden-archivos` | listar la carpeta a mano |
| Documento Word | skill `docx` / python-docx | el .docx sigue siendo OBLIGATORIO |
| Búsqueda/scraping | MCP `firecrawl` (📖 `scraping-firecrawl.md`) | WebSearch/WebFetch nativos |
| Comentarios de **YouTube** | ✅ `yt-dlp --write-comments` (instalado y probado; trae `like_count`) | Chrome MCP (scrollear y leer) o pegado del usuario |
| Comentarios de **TikTok** | ❌ **yt-dlp da CERO** (medido 2026-08-02: metadatos sí — 49.400 vistas, 986 likes — comentarios no) | Chrome MCP o pegado del usuario. **Decirlo, no simular que se minaron** |
| Comentarios de **Reddit** | ❌ Firecrawl lo rechaza (*"we do not support this site"*) y el navegador lo bloquea por política | Solo pegado del usuario |
| Reseñas de **Amazon** | ✅ **por NAVEGADOR** (por Firecrawl: muro anti-bot) | Medido: rating + nº de reseñas + "comprados el mes pasado" |
| Reseñas de **MercadoLibre** | ❌ captcha por Firecrawl (inventa datos), muro de sesión por navegador | Pegado del usuario |
| **Verificar cualquier scrape** | 🔒 `python3 scripts/candado_scraping.py resp.json --pedi "<lo pedido>"` | Correr las 4 verificaciones a mano (`scraping-firecrawl.md`) |
| **Saber si la matriz sigue vigente** | 🔁 `python3 scripts/verificar_fuentes.py` (detector de CAMBIO; base 2026-08-02) | Re-probar las fuentes a mano antes de fiarse de la matriz |
La EJECUCIÓN (golden-shopify, golden-ads, golden-imagen-arena, golden-ugc-avatar, familia
golden-chatea-pro) **no se llama desde aquí**: la orquesta `golden360` con este estudio como insumo.

## 4. País + compliance por vertical
- **Todo por país** (tiempos de entrega, precios, regulación — INVIMA/ISP/FDA). Nunca mezclar países.
- La minería y las citas van en **cualquier idioma**; el análisis aterriza al país destino.
- Claims sensibles → `compliance-por-vertical.md`: márcalos desde la investigación para que la
  ejecución no herede promesas ilegales ("sufres de…?" prohibido, sin curas, sin % garantizados).

## 5. Nunca parar por un dato que falta (pregunta concreto y sigue)
- Falta un dato real (costo, WhatsApp, claims, foto del reverso): **pregúntalo con campo**
  (ej. "Costo del proveedor: ____"). Si no lo tiene, **AVANZA** con marcador (`[PENDIENTE]`) y
  anótalo en `estado.pendientes` del expediente. El estudio se entrega completo con huecos
  marcados, no a medias. Un marcador honesto NO es una invención.

## 6. Los precios del estudio son REFERENCIA, no decisión (lección Toppik 2026-07-09)
- El estudio propone precios/ofertas como referencia de mercado; **la decisión es SOLO del dueño**.
- En el expediente, un precio no confirmado se queda en `null` + pendiente — jamás se rellena con el
  sugerido. (Quien monte encima — golden360 — tiene prohibido usar precios del estudio; aquí nace
  esa protección: se rotulan siempre "referencia de mercado".)

## 7. Candado de completitud (ninguna fase cierra a medias)
- **Fase -1** no cierra sin INCI o etiqueta legible + fuente. **Fase 0** sin los 6 campos y los 4
  números pedidos (los que falten, `[PENDIENTE]` explícito). **Fase 1** sin datos duros + minería +
  dossier. **Fase 2** sin el archivo **`.docx` REAL**.
- **Entrega final** sin los **5 datos de viabilidad + veredicto** (lanzar / condicionar / matar), no
  se considera terminada. Un `[PENDIENTE]` explícito es válido; un hueco silencioso NO.

## 8. Organización + expediente
- Todo en `PROYECTOS/<PRODUCTO>/` (MAYÚSCULA), con `PRODUCTO.json` a la cabeza (esquema:
  `producto-json.md` — esta skill es la dueña). Nada suelto.
