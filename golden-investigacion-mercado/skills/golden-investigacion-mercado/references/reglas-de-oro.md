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

## 9. 🚨 CANDADO ANTI-CONTAMINACIÓN — cuando corren VARIOS estudios en paralelo (incidente real, G5.10)
**Qué pasó (2026-08-22, corrida de 5 productos en paralelo):** un agente reconstruyendo el `.docx`
de un producto usó una carpeta de trabajo temporal (`unpacked/`, `extracted/` o similar con nombre
fijo) que otro agente — corriendo el mismo minuto, mismo tipo de tarea — también estaba usando. El
segundo agente pisó los archivos del primero a mitad de proceso. El resultado: un documento final
guardado en el Escritorio con el nombre correcto pero el CONTENIDO de otro producto por dentro (143
menciones de un ingrediente que no era el del título, 12 del que sí). Pasó el candado de "abrí el
archivo y vi texto real" porque el XML era válido — la corrupción no rompe el formato, solo mezcla
el contenido. **Nadie lo hubiera detectado sin abrir el XML y contar menciones por producto.**
- **Causa raíz:** nombre de carpeta de trabajo NO único entre agentes concurrentes sobre el mismo
  scratchpad de sesión.
- **CANDADO OBLIGATORIO desde ahora, sin excepción, cuando el flujo edite o reconstruya un `.docx`:**
  1. La carpeta de trabajo para desempacar/editar el `.docx` **DEBE** incluir un sufijo único e
     impredecible por ejecución (PID, timestamp con milisegundos, o `mktemp -d`) — **nunca** un
     nombre fijo tipo `unpacked/`, `extracted/`, `tmp/`.
  2. **Antes de tocar nada**: verificar que la carpeta de trabajo está vacía o es recién creada —
     si aparece contenido de otro producto ahí, es la señal de colisión; abortar esa carpeta y
     crear una nueva, no seguir sobre lo que ya está contaminado.
  3. **Después de guardar, SIEMPRE, sin excepción** (esto es lo que faltó): extraer el XML del
     `.docx` final y contar menciones del nombre/ingrediente del producto correcto vs. de los otros
     4-N productos que puedan estar corriendo en paralelo en la misma sesión. Si las menciones del
     producto correcto no superan ampliamente a cualquier otro producto, **NO declarar terminado** —
     repetir desde una carpeta nueva. Un vistazo al tamaño de archivo o "el XML es válido" **NO ES
     SUFICIENTE** — la corrupción de este incidente pasaba ambas pruebas.
  4. Quien orquesta varias corridas en paralelo (varios `Agent`/subagentes sobre esta skill al mismo
     tiempo) debe advertir explícitamente en el prompt de cada agente: *"vas a correr junto a otros
     N agentes de esta misma skill sobre otros productos — usa una carpeta de trabajo con sufijo
     único, y verifica con grep/conteo antes de guardar que tu documento no tiene contenido de los
     otros productos."*
  5. 🚨 **EL CONTEO SOLO NO BASTA — "injerto de párrafo" (incidente real, G5.11).** Auditoría
     adversarial (23-ago-2026, `golden-verificador`) encontró un párrafo COMPLETO de Magnesium
     Complex pegado literalmente dentro del estudio de Resveratrol (9 líneas idénticas carácter por
     carácter, incluida una frase citando el nombre de otro producto). El conteo de menciones
     de la regla 9 **pasaba en verde** porque un párrafo ajeno de 9 líneas casi no mueve el conteo
     de 197 menciones propias contra 4 ajenas. **El conteo detecta pisadas de archivo completo, NO
     detecta injertos de párrafo.**
     **Verificación adicional obligatoria, además del conteo:** buscar bloques de texto de más de
     60 caracteres que aparezcan LITERALMENTE IDÉNTICOS entre el documento final y cualquier otro
     estudio de la misma corrida (intersección de párrafos/oraciones, no solo de palabras sueltas).
     Prestar especial atención a las secciones de "condiciones", "cobertura declarada", "handoff" y
     "próximos pasos" — es donde vive la plantilla que un agente reutiliza sin darse cuenta de que
     pertenece a otro producto.

## 10. 🚨 NO DECLARAR UNA HERRAMIENTA "NO DISPONIBLE" SIN HABERLA PROBADO (incidente real, G5.10)
**Qué pasó:** varios agentes declararon `[PENDIENTE]` la minería de comentarios de YouTube
(`yt-dlp --write-comments`) y la transcripción local (`whisper-cli`) con la frase *"el entorno no
tiene acceso a esas herramientas de scraping"* — **sin ejecutar `which yt-dlp` ni `which
whisper-cli` primero**. Verificado en la máquina real: **ambas SÍ están instaladas** —
`yt-dlp` en `/opt/homebrew/bin/yt-dlp` (v2026.07.04) y `whisper-cli` en
`/opt/homebrew/bin/whisper-cli` (paquete `whisper-cpp` 1.9.1), con el modelo ya cacheado en
`~/.cache/hyperframes/whisper/models/ggml-small.bin`. El hueco no era de la máquina: era que el
agente **asumió** en vez de **verificar**.
- **CANDADO OBLIGATORIO:** antes de escribir `[PENDIENTE]` por "herramienta no disponible", correr
  `which yt-dlp` y `which whisper-cli` (o el comando equivalente de la herramienta en cuestión) y
  pegar la salida real en el documento. Solo si el comando falla de verdad se marca `[PENDIENTE]`
  con la salida del error como evidencia — nunca por suposición.
- Nota aparte (esto SÍ es un límite real, medido, no una suposición — ver tabla de la sección 3):
  yt-dlp trae CERO comentarios de TikTok (solo metadatos), Reddit lo bloquea Firecrawl, y
  MercadoLibre bloquea por captcha/sesión tanto a Firecrawl como al navegador sin login. Esos SÍ
  se marcan `[PENDIENTE]` legítimamente — la diferencia es que ahí ya se probó y falló, con
  evidencia, no que no se intentó.

## 10.5 🚨 NO DECLARAR "PENDIENTE" SIN HACER `ls` DE LA CARPETA DEL PROYECTO PRIMERO (incidente real, G5.11)
**Qué pasó:** el estudio de Beevana declaró `[PENDIENTE]` la foto de etiqueta del producto ("no se
encontró una etiqueta oficial... ningún claim puede usarse hasta tener la foto macro") mientras esa
misma foto (`Beevana-imagen-producto.jpg`) YA estaba guardada en la carpeta del proyecto — con datos
que contradicen el propio documento: la etiqueta real dice 60 g y el estudio costeó todo (proveedor,
margen, flete) sobre una presentación de 30 g. El frente del envase dice "ARTHRITIS" (ítem de
compliance de primer orden) y el estudio nunca lo señaló.
- **CANDADO OBLIGATORIO:** antes de escribir `[PENDIENTE]` por falta de un insumo (foto, PDF, dato
  del dueño), correr `ls -la` de la carpeta del proyecto y de cualquier carpeta hermana relevante.
  Un insumo disponible que se declara faltante es tan grave como inventar un dato — es lo contrario
  exacto de "no inventar": es "no mirar".

## 10.6 🚨 UNA ACTUALIZACIÓN QUE TOCA UN DATO DE VIABILIDAD RESCRIBE EL VEREDICTO, NO SE ANEXA (G5.11)
**Qué pasó:** varios estudios recibieron una sección nueva al final (minería de video, proveedores)
que contradice datos del cuerpo original — y el resumen ejecutivo y el veredicto de la sección 10
NO se actualizaron. Ejemplo real: Beevana sección 11 concluye "a esa escala el negocio NO es
rentable" y "Golden NO puede abastecer HOY", pero el veredicto de la sección 10 sigue diciendo
"margen amplio de proveedor" y "LANZAR CON CONDICIONES" sin tocar esos dos datos.
- **CANDADO OBLIGATORIO:** si una sección nueva o una actualización cambia CUALQUIERA de los 5 datos
  de viabilidad (demanda, saturación, proveedor, margen, riesgo regulatorio), el resumen ejecutivo Y
  el veredicto final DEBEN reescribirse en el mismo momento — nunca queda un veredicto viejo
  conviviendo con evidencia nueva que lo contradice dentro del mismo documento.
- Corolario: **"N de N secciones completadas"** solo es válido si N es el número de secciones que
  EXIGE `02-documento-maestro.md` (10), no el número de secciones que el documento efectivamente
  escribió. Declarar "9 de 9" cuando el estándar exige 10 y faltan Buyer Personas o Estrategia de
  Mensaje es cobertura falsa — cambiar el denominador para que cierre en 100% no es honestidad.
