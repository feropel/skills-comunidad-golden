# Changelog — GOLDEN INVESTIGACIÓN DE MERCADO

## G5.7 — 2026-08-07 — Cosecha del chat "ESTUDIO 360 DENTAL CAVITY HEALING (Chile)" (6 ítems)
Repartido por el Centro de Mando desde la bandeja (orden de FER: "sin omitir detalle"). Todo salió
de una corrida real de la skill sobre `rayoshopchile.com/products/dental-cavity-healing` (gotas
dentales COD, Chile):
- **Compuerta de IDENTIDAD DEL PRODUCTO** (`00-identificacion-forense.md`, paso duro): la versión
  local puede declarar OTRA fórmula que la marca original — el frasco chileno declaraba glicerina,
  pantenol y PCA de sodio (humectantes) mientras la marca original (Amazon B0DB2ZBXZD, US$69)
  declara nano-hidroxiapatita. Regla: rastrear el original (Amazon/eBay/AliExpress) para costo
  real, ml e ingredientes, y PROHIBIDO escribir un claim de ingrediente sin la foto macro de la
  etiqueta del frasco que el dueño va a despachar.
- **El NOMBRE del producto es un ítem de compliance** (forense + compliance): "Dental Cavity
  Healing" promete curación y era el mayor pasivo legal del negocio; ninguna revisión lo detectaba
  porque el mapa miraba el copy, no el nombre. Si promete cura → proponer renombre (caso real:
  "Dental Shield / Escudo Dental").
- **Vertical SALUD BUCAL** en `compliance-por-vertical.md` con la redacción probada en campo
  (❌ "sana caries"/"repara el diente"/antes-después/porcentajes/odontólogo firmando · ✅ "cuida el
  esmalte"/"apoya la remineralización"/gotario/"el control con el dentista igual va").
- **Compliance por PAÍS: CHILE** (`compliance-por-vertical.md`): autorización sanitaria del ISP
  (D.S. 239/02), el ISP publica alertas con nombre y dominio (alerta 5-mar-2025), registro en
  `registrosanitario.ispch.gob.cl`, publicidad engañosa bajo Ley 19.496. Aplica a cualquier
  producto vendido en Chile.
- **Receta de AD INTEL probada** (`01-investigacion-360.md` §1.7): `ads_library_search` con
  `countries` + `ad_active_status:"ACTIVE"` + término del nicho, y después scrape del
  `ad_snapshot_url` con firecrawl **SIN `includeTags`** (con `includeTags` vuelve VACÍO) →
  copy verbatim + dominio de la landing. 5 competidores levantados en minutos.
- **Regla de VOZ DEL CLIENTE sin reseñas locales** (§1.5): usar reseñas de Amazon del MISMO
  producto/formato, citando ASIN, incluidas las de 1★ y el bloque "Customers say", rotuladas como
  internacionales — jamás presentadas como locales.

## G5.6 — 2026-08-02 — La matriz de fuentes deja de ser una foto: `verificar_fuentes.py`
- **El problema que cerraba el ciclo.** G5.5 dejó una matriz de fuentes medida con rigor, pero
  medida **una sola vez**. Los sitios cambian defensas cada pocos meses y **nadie se enteraría**:
  la skill seguiría afirmando "Amazon funciona por navegador" con total seguridad hasta el día que
  no. La caducidad dependía de que alguien se acordara — el mismo tipo de dependencia que la Regla
  Cero tenía antes del candado.
- **`scripts/verificar_fuentes.py`** graba una huella por fuente (tamaño, redirección, marcas de
  muro, código HTTP) y la compara con la del día que se midió. Las sondas de `yt-dlp` son
  **definitivas** porque corren la herramienta real.
- **Honestidad de diseño, escrita en el propio script:** es un **detector de CAMBIO, no de
  funcionamiento**. Amazon devuelve firma anti-bot por HTTP plano y aun así funciona por navegador
  — una firma no prueba que algo esté roto. Por eso el veredicto es CAMBIO/IGUAL y nunca
  FUNCIONA/NO FUNCIONA. Lo que no puede correr (Firecrawl y navegador, que son MCP) lo emite como
  **checklist con parámetros exactos y resultado esperado**, en vez de fingir que lo cubre.
- **Probado el mismo día:** sin cambios reporta IGUAL; con la línea base falseada cazó los tres
  cambios simulados (tamaño de Temu, marcas de Amazon, redirección de MercadoLibre).
- Línea base grabada 2026-08-02. Avisa a los 60 días. ⚠️ `scripts/fuentes_baseline.json` queda
  **fuera del blindaje** a propósito: si se blinda, la suite no puede actualizarse.
- **La suite se auto-encontró un defecto mientras se probaba.** Al sondear AliExpress varias veces
  el mismo día, pasó de 640.990 b a 2.391 b con `captcha` — cinco sondas seguidas, idéntico. El
  sitio no había cambiado: **nos limitó a nosotros**. O sea, sondear dispara justo las defensas que
  la suite mide, y un detector que se corre a cada rato fabrica sus propios falsos positivos (la
  peor forma de fallar: un detector ruidoso se ignora). Se añadió la detección del patrón
  **PROBABLE AUTO-BLOQUEO** (desplome de tamaño + captcha nuevo) y la regla de **correrla una vez
  al mes**. Probado: ahora etiqueta ese caso como auto-bloqueo y no como cambio del sitio.

## G5.5 — 2026-08-02 — Modo 4 (captcha), el CANDADO ejecutable, y el alcance real de la minería
- **Cuarto modo de fallo, y es el que rompía la verificación existente.** MercadoLibre Colombia
  devuelve un **muro de captcha** y el extractor inventa `"Producto 1".."Producto 8"` con precios,
  ventas y ratings falsos — **con `metadata.title` POBLADO ("Seguridad — Mercado Libre") y campo
  `json` presente**. Los checks 1 y 2 pasaban en verde. Tells nuevos: `/captcha/` en la url, título
  de muro, valores secuenciales de plantilla. Escrito en `scraping-firecrawl.md` (SF3.0).
- 🔒 **`scripts/candado_scraping.py` — la Regla Cero deja de ser prosa.** Las 4 verificaciones
  pasan a ser un script que devuelve PASA/REVISAR/DESCARTAR con código de salida.
  **Probado contra los 4 fallos reales del manual: los caza los 4 y deja pasar el dato bueno.**
  Es la respuesta a un problema estructural: una regla escrita en 7 archivos depende de que alguien
  se acuerde; un candado que devuelve DESCARTAR, no.
- **Alcance REAL de la minería de comentarios (esta skill lo prometía de más).** Medido hoy:
  - **YouTube** ✅ con `like_count` — la jerarquía de objeciones votada por la audiencia
  - **TikTok** ❌ `yt-dlp` da **cero comentarios** (metadatos sí: 49.400 vistas, 986 likes)
  - **Reddit** ❌ Firecrawl lo rechaza de plano, el navegador lo bloquea por política
  - **Amazon** ✅ **por navegador** (rating, nº de reseñas, "comprados el mes pasado")
  - **MercadoLibre** ❌ captcha por Firecrawl, muro de sesión por navegador
  La tabla de apoyos de `reglas-de-oro.md` ahora los lista uno por uno con su estado medido, en vez
  de decir "YouTube/TikTok" en bloque. Lo que no se puede minar **se declara**, no se simula.

## G5.4 — 2026-08-01 — Regla Cero de 1 a 3 modos de fallo + minería de comentarios YA OPERATIVA
- **La verificación de G5.3 era insuficiente y se probó que sí.** El check de `metadata.title`
  vacío solo cazaba la alucinación total. Ejecutadas 3 fuentes más el 2026-08-01:
  **Temu** falla con `title` **poblado** (buscando "wart remover" devolvió 72 categorías de ropa
  con precio "N/A" — redirigió a la portada) y **Amazon** falla con `title` poblado **y sin
  redirección** (muro anti-bot: la respuesta **no trae campo `json`**). Dos de los tres modos
  pasaban en verde la verificación anterior.
- **Nueva verificación de 4 pasos** en `reglas-de-oro.md` §1, y la que caza los tres:
  **"el dato responde a lo que pedí?"**. Si buscaste verrugas y llegan vestidos, es basura aunque
  todos los metadatos estén bien.
- **✅ `yt-dlp` instalado y probado: la MINERÍA DE COMENTARIOS deja de ser una promesa.** G5.3
  documentó honestamente que Firecrawl no puede traerlos; ahora hay vía real. Medido: 30
  comentarios con `author`, `text` y **`like_count`**, de ~2.450.067 disponibles.
  🎯 El `like_count` es mejor de lo que se prometía: ordenar por likes da la **jerarquía real de
  objeciones y dolores, validada por votación de la audiencia** — no una lista que yo redacte.
  Eso alimenta directo la voz del cliente, el FAQ real y el dossier de 30 capas, con fuente.
- **Matriz de fuentes medida** en `scraping-firecrawl.md` (SF2.0): AliExpress ✅ · Temu ❌ ·
  Amazon ❌ · TikTok Creative Center ❌ · YouTube metadatos ✅. Además `firecrawl_map` verificado
  (con el aviso de que un map vacío **no prueba** que el sitio no tenga páginas — misma lógica que
  "un cero solo prueba si cubrió TODO") y `firecrawl_monitor` comprobado como disponible sin
  crear ninguno. + Nota: `rawHtml` no pasa por el extractor, así que es inmune a los modos 1 y 2.
- **Lección de método, la que vale más que el hallazgo:** SF1.0 dio por buenas tres tiendas
  habiendo probado una. No basta con ejecutar la herramienta — hay que ejecutarla **contra cada
  fuente que la skill promete**, una por una.

## G5.3 — 2026-07-31 — 🚨 EL SCRAPER TAMBIÉN INVENTA (Regla Cero) + manual de scraping verificado
- **Incidente medido en vivo, no teórico.** Probando `firecrawl_scrape` con `formats:["json"]`
  contra la ficha de un removedor de verrugas en AliExpress, la página redirigió a `.us` y sirvió
  HTML hueco. Firecrawl **no devolvió vacío ni error**: el extractor alucinó
  *"Smart TV 55\" 4K LED, $499.99, rating 4.5, 150 reseñas"* y lo entregó con `statusCode: 200`.
  Producto, precio y reseñas: los tres inventados, en formato de dato duro listo para citar.
- **Por qué importa aquí más que en ninguna skill:** esta es la dueña del `PRODUCTO.json` y de las
  citas con fuente. Un precio o un "150 reseñas" fantasma entra al expediente, viaja a la página,
  a los creativos y a la pauta, y nadie lo vuelve a cuestionar. La regla de la casa "solo productos
  REALES / datos reales antes de generar" se violaría **sin que nadie mienta**: mentiría la herramienta.
- **Regla Cero escrita en `reglas-de-oro.md` §1** (junto a la anti-invención, su casa natural):
  verificar que `metadata.title` NO esté vacío antes de usar CUALQUIER dato scrapeado. Vacío =
  descartar, no citar, no guardar; se escribe "no obtenido" y se propone otra vía.
- **Nuevo `references/scraping-firecrawl.md` (SF1.0)** — manual canónico de scraping de TODO el
  ecosistema Golden, con 7 hallazgos MEDIDOS el 2026-07-31: la alucinación en páginas huecas;
  `json`+`actions` se cae por timeout (2 de 2); el scroll infinito SÍ se resuelve con
  `actions`+`markdown`+`proxy:stealth` (182 KB reales de AliExpress); `json` sin actions es la
  receta buena (8 productos reales, 9 créditos); `location:{country}` evita salir con precios de
  USA; YouTube trae título/canal/vistas/likes exactos por postprocesador nativo pero **NO trae
  comentarios**; `yt-dlp` no está instalado y `ffmpeg` sí.
- **Minería de comentarios — corrección honesta:** la skill promete minería multi-idioma de
  YouTube/TikTok. Firecrawl **no puede** traer esos comentarios (medido: `comentarios: []` con y sin
  scroll). Se documentan las 3 vías reales por orden (yt-dlp → Chrome MCP → pegado) y se marca
  `yt-dlp` como pendiente-con-dueño (`brew install yt-dlp`). Antes la skill habría intentado y
  reportado "no se hallaron comentarios" sin saber que la herramienta simplemente no llega.

## G5.2 — 2026-07-31 — La hermana orquestadora se renombró: `golden-ruta-360` → `golden360`
- Pedido de FER. Esta skill la nombra en 17 lugares (SKILL.md, README-COMUNIDAD, reglas-de-oro,
  producto-json, 00-identificacion-forense, 02-documento-maestro y este changelog): todos
  actualizados en el mismo movimiento. Un renombre sin propagar deja a la hermana apuntando a un
  nombre muerto, y el handoff "corre golden-ruta-360 con este estudio" dejaría de disparar nada.
- No cambia NADA del contenido ni del rol de esta skill: sigue siendo investigación pura y dueña del
  esquema `PRODUCTO.json`.

## G5.1 — 2026-07-30 — Auditoría post-split (golden-skill-auditor 905→~985): fin del drift pre-split
El split G5.0 movió los playbooks pero dejó residuos del rol viejo. Hallazgos con evidencia, reparados:
- **`reglas-de-oro.md` REESCRITA para investigación pura** — la versión anterior era pre-split:
  tabla de skills de EJECUCIÓN que esta skill ya no llama, espejo de una "lista R3" inexistente,
  candado que exigía "Fase 6 Chatea" y el script `candado.py` (mudado a la 360 — ref rota), y la
  compuerta de montaje (mecánica de la ruta). Ahora: apoyos de investigación con fallbacks, candado
  propio (-1→entrega), "precios = referencia, no decisión" (lección Toppik) y frontera nítida con la 360.
- **`02-documento-maestro.md` §10**: el Word ya no cierra con fases de la ruta (Pauta F4/Orgánico F5/
  Chatea F6/F7.5) sino con **VIABILIDAD Y VEREDICTO** (5 datos + lanzar/condicionar/matar + handoff
  a golden360).
- Notas de transversalidad en `producto-json.md` (las Fases 3/5/8 y Compuertas 2–4 de su tabla son de
  la ruta) y `00-identificacion-forense.md` (rama B = fase de página de la ruta).
- README-COMUNIDAD: el flag de "material intruso" del inventario se acepta — es la guía deliberada
  para alumnos (patrón de la casa desde G3.2).

## G5.0 — 2026-07-30 — SPLIT: vuelve a ser INVESTIGACIÓN PURA; nace golden360 como orquestador
Pedido de FER: "una skill de investigación de mercado puro, absolutamente todo de la investigación;
y otra skill (la 360) que se encarga de unir todas las skills".
- Esta skill queda con TODO lo investigable: Fase -1 forense (foto→INCI→existencia), intake + 4
  números + breakeven, reconocimiento 0.5 (pedidos reales = fuente reina; demografía de pauta
  contaminada), investigación 360 con MINERÍA DE COMENTARIOS multi-idioma, dossier de 30 capas,
  documento .docx, y la ENTREGA de los 5 datos de viabilidad (la decisión de matar la toma el dueño
  o golden360 en su Compuerta 1). Sigue siendo la **dueña del esquema** `producto-json.md`.
- **Se mudan a `golden360`** (nada se pierde, se reubica): seo-aio-producto, 03-pagina-shopify,
  04-pauta-golden-ads, organico-redes, 07-chatea-pro-handoff, qa-pre-encendido y scripts/candado.py —
  es decir, los bloques CONSTRUIR y ENCENDER con las compuertas 2-4, el montaje, QA, seguimiento y retro.
- Nueva sección **AUTO-MEJORA** (mandato global de FER, autorización permanente): auto-calificarse al
  cerrar cada corrida, hornear lecciones con el ritual, arreglar huecos propios sin esperar pedido, y
  auditoría periódica con `golden-skill-auditor`. El mandato quedó también en memoria broadcast para
  que el centro de mando lo propague a TODAS las skills.
- Descriptions con frontera nítida en ambas: investigación/estudio → esta; lanzamiento completo →
  `golden360` (que la llama como su Bloque 1). Sello → **G5.0**.

## G4.3 — 2026-07-30 — MINERÍA DE COMENTARIOS multi-idioma (YouTube + TikTok + todas las redes)
Pedido del usuario: la investigación debe incluir los videos que hablan del producto exacto o similar
y TODOS sus comentarios — qué necesita la gente, de qué se quejan, lo bueno y lo malo — más TikTok y
cualquier red, en cualquier idioma. La sección 1.6 (antes 3 líneas de "redes sociales") se convierte
en la **minería de comentarios**:
- **YouTube**: búsquedas del producto exacto y similares (review / funciona / antes-después / "X meses
  después" / "no compres"); de los videos, los de más VISTAS = hooks ya validados; de los comentarios,
  necesidades, quejas, lo que funcionó, preguntas repetidas (= FAQ real de página y bot), citas textuales.
  Método honesto con fallbacks (scrape del watch-page → search site:youtube.com → transcripción por MCP
  si existe → declarar si no hay acceso, REGLA 5).
- **TikTok**: hashtags multi-idioma, videos top + comentarios (escepticismo típico), sonidos, creadores UGC.
- **IG/FB**: comentarios de posts y ANUNCIOS de competidores (objeciones gratis) + grupos del nicho.
- **Otros medios**: Reddit/foros/Quora, Amazon (Q&A + 1-2★/4-5★), AliExpress (reviews con fotos reales
  del origen), MercadoLibre, autocompletado de Google; y cualquier medio donde viva el nicho.
- **Regla multi-idioma**: país destino + inglés + portugués + idioma de origen del producto; citas
  traducidas se marcan *(traducida)*.
- **Tabla de extracción** (salida de 1.6): necesidades→ángulos · quejas→objeciones y qué NO prometer ·
  elogios→beneficios · preguntas→FAQ · lenguaje textual→hooks · títulos más vistos→formatos validados.
  Todo con fuente y volcado a 1.5 (voz del cliente) y al dossier (capas 7-13 y 21).
- SKILL.md Fase 1 actualizada para exigir la minería como parte de la fase. Sello → **G4.3**.

## G4.1 — 2026-07-27 — La ficha vieja es fuente contaminada
Regla dura añadida a `00-identificacion-forense.md`: cuando el producto ya tiene ficha, esa ficha
NO es fuente de verdad de ingredientes/specs — solo etiqueta o fabricante. Todo dato heredado entra
como `claims.no_verificables` hasta contrastar; si no se confirma, se elimina con barrido completo
y se deja `_incidente` en el expediente. Origen: el mismo día del despliegue de la ruta, un chat
re-publicó 4 specs heredadas de la descripción vieja que la etiqueta no respalda; la compuerta de
veracidad lo cazó al crear el PRODUCTO.json. Lección absorbida por el centro de mando.

## G4.0 — 2026-07-27 — RUTA PRODUCTO 360 (3 bloques + 4 compuertas)
La ruta lineal de 7 fases pasa a 3 BLOQUES (DECIDIR / CONSTRUIR / ENCENDER) con 4 COMPUERTAS DURAS.
Nuevo: Fase -1 identificación forense (arranque válido = una FOTO: etiqueta → INCI del fabricante →
existencia en Dropi/Shopify/mercado, ref `00-identificacion-forense.md`); expediente único
`PRODUCTO.json` como columna vertebral (ref `producto-json.md`); compuerta de VIABILIDAD (mata el
producto malo antes de gastar); compuerta de VERACIDAD DE ETIQUETA (origen: ficha que afirmaba
colágeno inexistente + imagen de galería con OTRA etiqueta); SEO como fase propia (ref
`seo-aio-producto.md`); los 4 números de negocio en la Fase 0; GIF y presupuesto de créditos;
compuerta de QA pre-encendido (ref `qa-pre-encendido.md`); fases 10-11 seguimiento y retro.
candado.py parcheado: exige PRODUCTO.json, compuertas viabilidad+veracidad pasadas, y nulls
críticos declarados en estado.pendientes. Mapa razonado: PROYECTOS/_SISTEMA/RUTA-PRODUCTO-360.md.
NO sincronizar al marketplace hasta estrenar con un producto real. Instalada por el centro de mando.



## G3.10 — 2026-07-25 — Candado de COHERENCIA TRANSVERSAL (Fase 7)
La auto-auditoría del PDF de Libido UP cazó que el orgánico decía "escribe RITUAL" mientras el activador
real del bot era la frase del botón: una clienta que escribiera RITUAL no disparaba nada. Nuevo candado
antes de cerrar Fase 7: keyword/CTA única e idéntica en página + ads + orgánico + bot (grep en todos los
archivos), precios idénticos en todas las piezas, verbo del producto consistente, un solo WhatsApp.
También: RSA de Google y todo set de copys multi-elemento sale en tarjetas numeradas (norma G3.9 aplica
a TODAS las plataformas, no solo Meta). Sello → **G3.10**.

## G3.9 — 2026-07-25 — ORDEN DE EJECUCIÓN DE FER + PDF ESTÁNDAR (caso Libido UP)
Correcciones dictadas por el dueño tras el 360 de Libido UP:
- **Nueva FASE 3.5 · CREATIVOS COMPLETOS (puerta dura):** "no se arma una campaña sin haberle creado
  el video o la foto". Cada imagen y video numerado con su archivo o su PROMPT de generación completo
  ANTES de orgánico y pauta. Candado: lista de creativos con estado (✅ archivo / 📝 prompt).
- **Swap de fases: FASE 4 = ORGÁNICO (capitaliza primero) · FASE 5 = PAUTA** (solo con 3.5 cerrada).
- **Checklist maestro exige el PDF Golden** (golden-pdf-check APROBADO + verbatim) con secciones en
  orden de ejecución y CADA copy/prompt en su tarjeta numerada separada — jamás párrafos corridos.
  El PDF es EL entregable; el .docx queda como fuente editable.
- Espejo horneado en golden-ads `reglas-de-oro.md` §14 (creativos primero) y §15 (copys normalizados),
  y en golden-pdf-check (estándar de copys numerados). Sello `GIM_VERSION` → **G3.9**.

## G3.8 — 2026-07-18 — ACLARACIÓN: la data de pedidos es la EXCEPCIÓN, no la regla (Fase 1.5.bis)
Ajuste ADITIVO fino (autorizado por el dueño; solo aclara, no borra ni desoptimiza). El aprendizaje de
G3.7 ("cruzar con data de pedidos") podía leerse como si SIEMPRE fuera a haber métricas. Se aclara que no:
- **Nota nueva al inicio de `1.5.bis`**: lo NORMAL es que el producto sea NUEVO y sin métricas → se
  investiga desde cero (Fase estándar) y la pauta va en **Modo B (testeo)**. La data de pedidos/CRM aplica
  **SOLO en la excepción**: producto ya vendido o relanzamiento a otro país. No pedir métricas como si
  siempre existieran; si no hay, se avanza sin frenar (todo `(estimado)`, REGLA 5).
- **Título suavizado**: "la fuente REINA, si existe" → "la fuente reina CUANDO existe, que es lo raro".
- Todo lo demás de G3.7 se mantiene intacto. Sello `GIM_VERSION` → **G3.8**.

## G3.7 — 2026-07-18 — DATA REAL DE PEDIDOS = FUENTE REINA (Fase 1.5.bis) + trampa de la demografía de pauta
Mejora ADITIVA sobre la voz del cliente / demografía (autorizada por el dueño; solo suma, no rompe flujo).
Lección de campo: la demografía que reporta una cuenta de anuncios NO es "quién compra" — está sesgada por
la segmentación que ya se aplicó (self-fulfilling). Caso real: una línea que vendía 50/50 según los pedidos
de Dropi aparecía como "90% mujeres" en Ads Manager, solo porque nunca se pauteó el creativo masculino.
- **Nueva sección `1.5.bis` en `references/01-investigacion-360.md`**: antes de estimar, preguntar si el
  dueño tiene DATA REAL de pedidos/CRM (export Dropi, Chatea PRO, hoja de ventas, pixel). Si la hay, MANDA
  sobre inferencias y sobre las impresiones de pauta: valida demografía real, mezcla de producto, combo
  attach y geo (cruza con `golden-dropi-analisis`). Sin data → marcar `(estimado)` y decirlo (REGLA 5).
- **Trampa explícita**: nunca tomar la demografía de una cuenta de ADS como "quién compra" sin cruzarla con
  pedidos reales (efecto self-fulfilling documentado con el caso de la cuenta 90% mujeres / 50-50 real).
- **Puntero en `1.8` (buyer personas)**: el demográfico se marca `(estimado)` o `VALIDADO` si hay data de
  pedidos; jamás copiado de la demografía de pauta sin cruzar.
- Sello `GIM_VERSION` → **G3.7**.

## G3.6 — 2026-07-09 — COMPUERTA DE MONTAJE (Fase 7.5): informe perfecto → preguntar → montar con datos del dueño
**+ Auditoría golden-skill-auditor del mismo día (935→1000):** candado.py ahora AVISA por dossier y
JSON de página (antes el exit 0 podía aprobar un paquete sin página) + imprime la compuerta 7.5;
README-COMUNIDAD con la fila 7.5 (la cara pública ya no promete montaje automático); 03-pagina-shopify
alineada (generar con [PROPUESTO] ≠ montar); header del pipeline e índice de archivos actualizados;
ruta rota histórica de google-ads.md anotada; sello legible por el detector del auditor.
Lección del caso real Toppik (feedback directo de FER): el paquete se entregó completo pero (a) no cerró
ofreciendo el montaje, y al corregir (b) se montó el producto con los PRECIOS PROPUESTOS por el estudio.
- **Nueva Fase 7.5 en SKILL.md**: toda entrega cierra SIEMPRE con "Deseas que lo monte?" + la lista de
  datos de negocio que solo el dueño decide (precios/combos, WhatsApp, costo, marca, anticipado).
- **Prohibición explícita**: jamás montar en plataformas con precios/ofertas del estudio (referencia de
  mercado ≠ decisión del negocio). Con OK + datos → se monta todo de una (Shopify DRAFT, Chatea señalado,
  Meta en PAUSA). Renders pagados mantienen su regla (foto real + OK de créditos).
- Punteros agregados: REGLA 5 del SKILL.md ("avanzar ≠ ENCENDER"), reglas-de-oro §8, criterio de calidad,
  y description del frontmatter (para que el comportamiento dispare desde la primera lectura).

## G3.5 — 2026-07-09 — Auditoría con golden-skill-auditor: 885 → 1000 (candado por SCRIPT + fósiles de fase)
Primera auditoría formal con la rúbrica de 1000 pts. Hallazgos con evidencia, todos reparados:
- **Nuevo `scripts/candado.py`** — el candado maestro de Fase 7 deja de ser prosa: script determinista
  que verifica artefactos del paquete (docx/PAUTA o ADS//ORGANICO/CHATEA-PRO/README/creativos), las
  2 piezas de Fase 6 dentro del CHATEA-PRO, y cuenta [PENDIENTE]. Modo `--skills` chequea las 11 hijas
  instaladas. **Validado contra 2 paquetes reales**: uno COMPLETO ✅ y uno viejo donde cazó exactamente
  el bug histórico (faltaba la pieza comentarios + el .docx). Acepta pauta en `PAUTA*.md` o carpeta `ADS/`.
- **Fósiles de fase corregidos** (críticos): `02-documento-maestro.md:44` decía "Meta Ads (Fase 4) ·
  TikTok Ads (Fase 5)" (pipeline muerto en G2.2) → índice real; `organico-redes.md:33` decía "Chatea
  PRO, Fase 8" → Fase 6.
- **Description con desambiguación negativa**: "NO usar cuando quiera solo una pieza suelta → deriva a
  golden-shopify / golden-ads / golden-ecom-magic / golden-ugc-avatar / prompt-ventas / productos-ganadores".
- **Sello bajo el H1** (patrón de la casa) — el comentario GIM_VERSION vivía al final del archivo.
- **Plan B por MCP faltante** en REQUISITOS (firecrawl→WebSearch/WebFetch; Chrome/Higgsfield→prompts
  listos [PARCIAL]; Meta→informe copia-pega). Intro corregida ("Meta, TikTok y Google" — omitía Google).
- **Numeración alineada**: reglas-de-oro "5.bis" → "7. Candado" (igual que la REGLA 7 del SKILL.md);
  nota espejo en §3 (la tabla de skills duplica R3 del SKILL — editar ambas). Barrido de signos de apertura
  en 8 puntos (README, 01, 03, compliance, dossier ×3, reglas-de-oro) — estándar Golden de escritura.
- Sello `GIM_VERSION` → **G3.5**.

## G3.4 — 2026-07-04 — Fase 6 acotada a las 2 piezas POR-PRODUCTO
Corrección de rumbo sobre G3.3: la Fase 6 no monta el workspace completo, sino solo lo que depende del **producto** investigado.
- Fase 6 ahora llama **solo 2 skills**: **`golden-chatea-pro-prompt-ventas`** (venta por WhatsApp) + **`golden-chatea-pro-config-comentarios`** (comentarios).
- **Por qué:** el estudio produce un PRODUCTO; venta y comentarios son por-producto. La config de **workspace** (logístico + validación de direcciones, carritos, config general, orquestador `golden-chatea-pro-full-configuracion`) se monta una sola vez por tienda/país, en un flujo aparte — no en cada lanzamiento de producto.
- Actualizados: SKILL.md (frontmatter, R3, tabla de skills, Fase 6, Fase 7, archivos, sello), `07-chatea-pro-handoff.md` (reescrito a 2 piezas), `reglas-de-oro.md` (tabla + candado), `README-COMUNIDAD.md`. Candado de completitud: la fase exige las **2 piezas** (antes 4 asistentes).
- Sello `GIM_VERSION` → **G3.4**.

## G3.3 — 2026-07-02 — Re-cableo Chatea PRO (el ecosistema se reestructuró; 3 refs rotas arregladas)
La familia Chatea PRO se reorganizó en un **orquestador maestro + hijos**. Las 3 skills que la Fase 6
llamaba dejaron de existir con esos nombres → referencias rotas (caso "cambio de nombre/estructura"
que el leer-en-vivo NO resuelve). Corregido:
- Fase 6 ahora **delega ENTERA en `golden-chatea-pro-full-configuracion`**, que monta los **4
  asistentes** (comentarios, logístico, ventas WhatsApp, carritos) vía sus hijas. Antes eran 3 piezas;
  ahora 4 (gana logístico = validación de direcciones y carritos = recuperación de abandonos).
- Nombres viejos reemplazados en SKILL.md (frontmatter, R3, requisitos, Fase 6, archivos),
  `07-chatea-pro-handoff.md` (reescrito, + arreglado un encabezado duplicado), `reglas-de-oro.md` y
  `README-COMUNIDAD.md`. Candado de completitud actualizado: la fase exige los 4 asistentes.
- Sello `GIM_VERSION` → **G3.3**.

## G3.2 — 2026-07-02 — Lista para COMUNIDAD (portabilidad + privacidad + dependencias claras)
Pasada final para poder compartir la skill sin que se rompa ni filtre nada privado:
- **Punteros a "memoria" incrustados:** 4 lugares (SKILL.md, 03-pagina-shopify ×2, 07-chatea) decían
  "ver memoria" — roto para quien no tenga las memorias del autor. Ahora el contenido está inline.
- **Sección REQUISITOS/dependencias** nueva en SKILL.md: tabla de qué skill hija necesita cada fase +
  MCP recomendados. Y **fallback en REGLA 3**: si una skill hija no está instalada, se declara explícito,
  se hace lo posible inline y se marca `[PARCIAL — requiere golden-Y]` (no se rompe ni finge).
- **Changelog generalizado:** quitados los nombres de productos de prueba del autor (se mantienen las
  lecciones técnicas). Cero datos privados en toda la skill (0 rutas/teléfonos/dominios/emails verificado).
- Sello `GIM_VERSION` → **G3.2**.

## G3.1 — 2026-07-02 — Auditoría A-Z pre-comunidad (skill + las 11 hijas verificadas en disco)
Auditoría exhaustiva con 3 agentes en paralelo leyendo TODAS las skills orquestadas. Hallazgos corregidos:
- **Descripción (frontmatter) reescrita a la realidad G3.x** — describía el pipeline viejo (fases Meta/
  TikTok propias, solo prompt-ventas); ahora refleja: intake 6 campos, dossier 30 capas, destino por
  perfil, pauta delegada en golden-ads (Meta+TikTok+Google), orgánico, trío Chatea PRO, checklist maestro.
- **`golden-ecom-magic` integrada** (skill nueva de imágenes): imágenes de producto/infografías sobre
  FOTO REAL (carrusel 1080×1080, secciones 1080×1350, WebP <150KB) → cableada en REGLA 3, Fase 3,
  orgánico y reglas-de-oro. golden-ugc-avatar queda para video/avatar UGC (Soul 2.0/Seedance 2.0).
- **Referencias a golden-shopify a prueba de versiones**: ya no se cita un archivo fijo (demo-dawn-v2);
  se lee GFS_VERSION + changelog + la plantilla que SU SKILL.md recomiende en el momento (evoluciona
  rápido: el agente la vio en G3.11 y horas después iba en G3.12).
- **Handoff a golden-ads completado**: se pasan también COSTO/margen, moneda y PRESUPUESTO disponible
  (inputs obligatorios que golden-ads G4.0 espera).
- **Fixes de consistencia**: orden físico de reglas (6 antes de 7), referencia rota "playbooks 04/05"
  eliminada (REGLA 4 ahora apunta a compliance-por-vertical + golden-ads e incluye Google), encabezado
  de `organico-redes.md` corregido (decía Fase 7, es Fase 5), nota del formato v3.0 de
  chatea-pro-prompt-ventas (copy-paste por campo; manifiesto de imágenes DEBAJO del prompt).
- Verificado: golden-web/agenda-citas existen (blueprint/wrapper), golden-copywriting GCW1.0,
  golden-productos-ganadores GPG1.0 y golden-meta-ads-analysis vigentes, sin duplicación entre skills.

## G3.0 — 2026-07-01 — Salto a 1000/1000: candado de completitud + .docx real + intake de 6 campos + compliance por vertical
Aplicados los 6 fixes del diagnóstico de 2 corridas reales de prueba (un suplemento de salud + un cosmético tópico):
- **#1 Candado de completitud (REGLA 7):** ninguna fase cierra a medias; cada fase tiene checklist de
  entregables; Fase 7 lleva **checklist maestro**. **Mata de raíz el bug de Chatea PRO** (Fase 6 debe
  entregar sus 3 piezas: config general + comentarios + agente de ventas; entregar solo 1 = fallo).
- **#2 .docx real:** Fase 2 DEBE generar el Word de verdad (skill `docx`), no solo `.md`.
- **#3 Forma del producto → verbo:** intake captura la FORMA (gota/cápsula/spray/gadget…) que fija el
  verbo de uso en TODO el copy (gota→"aplica", cápsula→"toma"). Detectado con un producto en gota tópica.
- **#4 Compliance por vertical:** nuevo `references/compliance-por-vertical.md` (suplemento/estética-
  cosmético/belleza/gadget/peso) cableado en REGLA 4. Suplemento="no cura"; cosmético tópico="no medicamento/no zonas prohibidas".
- **#5 Modelo(s) de pago:** intake detecta COD / anticipado / **ambos** (un producto de prueba ofrecía los dos), no asume COD.
- **#6 Método de ad intel honesto:** Ad Library → scrape → fallback a búsqueda → si no hay, declararlo (no inventar).
- Intake pasa de 3 a **6 campos**. Sello `GIM_VERSION` → **G3.0**.

## G2.5 — 2026-06-25 — REGLA #5 reescrita: nunca parar por un dato (pregunta concreto y sigue)
Feedback del usuario: no debo detener el pipeline por falta de un dato. Ahora la REGLA #5 dice:
- **Preguntar concreto + dar campo para llenar** (ej. "WhatsApp: ____"). Si lo tiene, se usa; si no,
  **se AVANZA igual** con marcador evidente (`[WHATSAPP PENDIENTE]`) y se anota en pendientes.
- **Jamás detener el pipeline** por un solo dato; el estudio se entrega completo con huecos marcados.
- Única excepción: el **render pagado** que dependa del dato espera (no quemar créditos); todo lo
  demás sigue (prompts, estructura, copys, slots). Aplicado en SKILL.md y `reglas-de-oro.md`. Sello → **G2.5**.

## G2.4 — 2026-06-25 — +Dossier psicológico de 30 capas (benchmark de una herramienta de investigación, mejorado con anclaje)
Analizado un informe real de una herramienta de investigación de producto del mercado (un suplemento
de salud, 58 págs): excelente en profundidad
psicológica/ángulos, pero **ciego en datos** (sin competidores, sin reseñas reales, sin ad intel, sin
fuentes — pura inferencia). Tomamos su fortaleza y la mejoramos con nuestro rigor:
- **Nuevo `references/dossier-psicologico.md`**: framework de **30 capas** (promesa, mecanismo,
  dolores/miedos/anhelos, resultado/transformación, naturaleza del valor, modo/errores de uso,
  categoría mental, criterios de decisión, disparadores, objeciones, barrera, **nivel de consciencia**,
  señales de credibilidad, evidencias, gratificación, oportunidades, insights, públicos múltiples).
- **Regla de anclaje (nuestra ventaja)**: cada capa se ancla en fuente real (reseñas/competidores/redes)
  y se marca `(inferencia)` lo que no tenga fuente — lo que al informe de referencia le falta (REGLA #1).
- **Wireado**: la Fase 1 ahora tiene 2 capas (datos duros + dossier); el documento (Fase 2) incluye una
  sección 4.bis con las 30 capas; mapa "capa → ejecución" (qué capa alimenta hook/objeción/segmentación).
- NO se eliminó nada de lo existente (se AÑADIÓ). Sello `GIM_VERSION` → **G2.4**.
- Resultado: el skill iguala a esas herramientas en psicología y las supera en datos + ejecución (página/ads/orgánico/WhatsApp).

## G2.3 — 2026-06-25 — Integración de skills nuevas (golden-web + trío Chatea PRO + agenda-citas)
El orquestador ahora aprovecha todo el arsenal Golden, no solo Shopify/ads:
- **Fase 3 ya no es solo Shopify**: elige destino por perfil → `golden-shopify` (producto COD),
  **`golden-web`** (marca propia / creador / empresa / leads), y **`golden-agenda-citas`** para
  negocios de servicios que venden citas.
- **Fase 6 (Chatea PRO) pasa de 1 a 3 piezas**: **`golden-chatea-pro-config`** (config general/JSON) +
  **`chatea-pro-comentarios-config`** (asistente de comentarios) + **`chatea-pro-prompt-ventas`**
  (agente de ventas WhatsApp). Palabra clave única en página/pauta/bot.
- Tablas de skills (SKILL.md R3) y playbooks 03/07 actualizados. Sello `GIM_VERSION` → **G2.3**.

## G2.2 — 2026-06-25 — Integración con `golden-ads` (la pauta se delega, fin de la duplicación)
Apareció el skill dedicado **`golden-ads`** (centro de comando de pauta: Meta+TikTok+Google, con/sin
métricas, publica por MCP). Para no duplicar y evitar drift, la investigación deja de reimplementar la
pauta y la **delega entera en `golden-ads`**:
- Las 3 fases de ads (Meta/TikTok/Google) se **consolidan en una sola Fase 4** que delega en `golden-ads`.
  El pipeline pasa de 9 a **7 fases**: Intake → Investigación → Documento → Shopify → **Pauta (golden-ads)**
  → Orgánico → Chatea PRO → Paquete.
- **Eliminados** (su contenido vive ahora en `golden-ads`, fuente única): `04-meta-ads.md`,
  `05-tiktok-ads.md`, `google-ads.md`, `06-creativos-copy-prompts.md`.
- **Nuevo** `references/04-pauta-golden-ads.md`: handoff — qué le pasa el estudio a `golden-ads` y qué
  devuelve. Tablas de skills (SKILL.md + reglas-de-oro) actualizadas: la pauta ahora apunta a `golden-ads`.
- El orgánico de redes (no es pauta) se queda en la skill. Sello `GIM_VERSION` → **G2.2**.

## G2.1 — 2026-06-25 — +Google Ads +Contenido orgánico de redes
Se amplía el pipeline de 7 a 9 fases:
- **Nueva Fase 6 · Google Ads** (playbook propio de Google, retirado en G2.2 — hoy vive en `golden-ads`): Search/PMax/Demand Gen/YouTube/Shopping,
  estructura campaña/grupo/anuncio, keywords + negativas, pujas, RSA (15 títulos + 4 descripciones),
  todas las extensiones y qué activar/desactivar. Vía `claude-ads:ads-google`.
- **Nueva Fase 7 · Contenido orgánico** (`references/organico-redes.md`): por canal (Facebook,
  Instagram, TikTok, WhatsApp y otros), formato de **feed** + **historias/efímero** + el copy
  correspondiente, con calendario de 7–14 días. Reaprovechamiento 1 idea → varios canales.
- Chatea PRO pasa a Fase 8 y el Paquete final a Fase 9 (ahora incluye `GOOGLE-ADS.md` y
  `ORGANICO-REDES.md`). Sello `GIM_VERSION` → **G2.1**.

## G2.0 — 2026-06-25 — Rearquitectura a ORQUESTADOR 360° (estudio → campañas ganadoras)
Salto mayor: la skill deja de ser solo "investigación + reporte" y pasa a ser el **orquestador
maestro** que entrega TODO el sistema para lanzar un producto. Pedido del usuario: estudio exhaustivo
que no omita nada y complemente lo no mencionado (estándar 100/100).
- **Nuevo pipeline de 7 fases** (cada una una puerta): Intake → Investigación 360° → Documento
  maestro (.docx) → Página Shopify (con golden-shopify + imágenes/GIF/video) → Meta Ads completo →
  TikTok Ads completo → Handoff Chatea PRO → Paquete final en `PROYECTOS/<PRODUCTO>/`.
- **REGLAS DE ORO nuevas**, incluida la que faltaba: **anti-invención + citar fuentes** (cada dato con
  su URL; lo no verificable = hipótesis). Exhaustividad/complementar; skills en vivo; país+compliance;
  datos reales antes de gastar créditos; organización en PROYECTOS.
- **Orquestación de skills reales** (verificadas en disco): `golden-shopify` (página, viva G2.8),
  `golden-copywriting` (copys), `claude-ads` (estructura Meta/TikTok), `golden-ugc-avatar` (imagen/
  video), `chatea-pro-prompt-ventas` (WhatsApp), `golden-productos-ganadores`, `golden-meta-ads-analysis`/`3qs`.
- **Playbooks añadidos** en `references/`: reglas-de-oro, 01-investigacion-360, 02-documento-maestro,
  03-pagina-shopify, 04-meta-ads, 05-tiktok-ads, 06-creativos-copy-prompts, 07-chatea-pro-handoff.
- **Meta Ads**: estructura campaña/conjunto/anuncio campo por campo, objetivo, CBO/ABO, segmentación
  (edades/sexos/ubicaciones/Advantage+), evento de conversión, ubicaciones, y **qué activar/desactivar**.
- **TikTok Ads**: equivalente nativo (Smart+, video 9:16/UGC, hook <2s, Spark Ads, fatiga creativa) +
  tabla de diferencias vs Meta, misma malla de segmentación, compliance TikTok.
- **Creativos**: por cada creativo, **5 hooks + 5 títulos + 5 descripciones** con emojis, frameworks
  (AIDA/PAS/4U/BAB), compliant; + **prompts de imagen/video** para cuando no haya saldo/API.
- Sello `GIM_VERSION` → **G2.0**.

## G1.0 — 2026-06-25 — Versión inicial (investigación + reporte .docx)
Investigación de negocio/competidores/reseñas/redes/anuncios → reporte Word. Regla obligatoria:
si deriva en página Shopify, generarla sí o sí con `golden-shopify`. Blindada read-only (chflags uchg).
## G4.2 — 2026-07-29 — Compuerta 2 incluye IMÁGENES: los claims viven quemados en los pixels; hoja de contactos + revisión visual obligatoria; gotcha del \/ escapado. Origen: claims eliminados del texto que seguían publicados en banners (GoPure/Tag Recede/Organic Bless).
## G4.2.1 — 2026-07-29 — Compuerta 2 ampliada: el universo son plantilla+descripción+GALERÍA+pósters (227, no 99) y el criterio es texto O TRANSFORMACIÓN (un antes/después sin letras ES el claim). + cruce render vs producto físico.
