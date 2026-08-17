# Changelog — GOLDEN 360

## R1.7 — 2026-08-11 — El Bloque 1 ahora mina la LOCUCIÓN de los videos (aviso de la red sináptica)
- Encargo del Centro de Mando: la transcripción local existía en `golden-video-editor` desde hacía
  tiempo sin propagarse; ya está en la investigación (G5.8), matriz-viral, video-teardown, ads y
  copywriting. Faltaba que la ruta la RECOGIERA en su orquestación.
- **Lo que el CdM pidió revisar no existía:** esta skill nunca dijo "el texto del video no se puede
  leer" ni equivalente — simplemente no mencionaba el video como fuente. No había limitación vieja
  que borrar; había un hueco que llenar. Se reporta así en vez de inventar el hallazgo.
- **Verificado EJECUTANDO, no citando** (protocolo Golden, fase 4), en esta máquina el 2026-08-11:
  `yt-dlp` 2026.07.04 ✅ · `ffmpeg` ✅ · `whisper-cli` ✅ · modelo `ggml-small.bin` presente.
  Prueba real: 6,8 s de audio en español → **1,9 s** de transcripción, texto correcto. La cadena
  corre; no se escribió "operativo" de oídas.
- **Se apunta, no se duplica:** la receta vive en
  `~/.claude/skills/golden-investigacion-mercado/references/01-investigacion-360.md` §1.6. Duplicarla aquí la
  envejecería en dos sitios, que es exactamente el fallo que la ley de red neuronal quiere evitar.
- **Regla nueva en el Bloque 1:** el guion hablado de los 3–5 videos con más vistas es una oferta ya
  validada por el mercado; baja al Bloque 2 (hero, escalera, guiones de Fase 5) y al Bloque 3 (hooks
  de pauta y orgánico). **Estudio sin la locución de los ganadores = estudio incompleto, se pide
  antes de la Compuerta 1.** Y en la Fase 5 el guion UGC parte de esa locución, adaptada a
  `claims.permitidos` — jamás copiada.
- Descripción NO tocada a propósito: el 2026-08-07 se recortó por tope del listado, y volver a
  engordarla la truncaría justo donde viven las fronteras con las hermanas.
- **Corrección del mismo día, aportada por el Centro de Mando:** reporté como "falso positivo del
  inventario" dos referencias que el auditor marcaba rotas, pero mi comprobación solo barrió el
  SKILL.md y hablé como si cubriera la skill entera. En el changelog SÍ había 3 menciones a la
  hermana en forma corta (`golden-investigacion-mercado/references/…`, sin el prefijo de ruta), una
  de ellas escrita ese mismo día por mí. Ya lleva ruta completa; las otras dos son entradas
  históricas de otras sesiones y se dejan como están. **Lección, que es de método y no de este
  archivo: el alcance de lo que se afirma no puede ser mayor que el alcance de lo que se revisó.**
  Un grep a un archivo no autoriza a decir "en la skill no existe".

## R1.6b — 2026-08-07 — Descripción recortada (registrado a posteriori el 2026-08-11)
- El cambio se hizo en el SKILL.md y quedó documentado en su propio comentario HTML, pero **sin
  entrada aquí**. Se registra ahora para que el changelog no tenga huecos: la descripción pasó de
  2.197 a ~1.150 caracteres porque superaba el tope de ~1.536 del listado de skills y se truncaba por
  el final, justo donde estaban las fronteras con las hermanas. El detalle de los 3 bloques se movió
  al cuerpo. Las frases reales de FER, que son lo que dispara la skill, se conservaron íntegras.

## R1.6 — 2026-08-02 — La compuerta anti-fantasma se vuelve EJECUTABLE
- R1.5 tapó el agujero de los 3 modos escribiendo las 4 verificaciones. Sigue dependiendo de que
  alguien las recuerde en el momento. **Ahora hay un candado que se corre:**
  `python3 ~/.claude/skills/golden-investigacion-mercado/scripts/candado_scraping.py resp.json
  --pedi "<lo pedido>"` → PASA / REVISAR / DESCARTAR, con código de salida encadenable.
- **Cuarto modo de fallo** incorporado: muro de **captcha** (MercadoLibre) que inventa datos **con
  `metadata.title` poblado** — pasaba los checks 1 y 2 en verde. Para un orquestador esto importa
  el doble: el Bloque 1 alimenta al 2 y al 3, y un producto fantasma se convierte en página,
  creativos y presupuesto de pauta antes de que nadie lo cuestione.
- **Fuentes del Bloque 1, estado medido:** AliExpress ✅ (Firecrawl) · Amazon ✅ (navegador) ·
  Temu ❌ y MercadoLibre ❌ (exigen cuenta) · Reddit ❌ · comentarios solo de YouTube.
  Detalle en `golden-investigacion-mercado/references/scraping-firecrawl.md` (SF3.0).

## R1.5 — 2026-08-01 — La compuerta anti-fantasma tenía un agujero: 2 de 3 modos la pasaban
- R1.4 verificaba solo `metadata.title` vacío. Probadas 3 fuentes más el 2026-08-01, **dos modos de
  fallo la cruzaban en verde**: Temu (redirige y devuelve 72 categorías de ropa, con title poblado)
  y Amazon (muro anti-bot, sin campo `json`, title poblado y sin redirección).
- **Compuerta ahora de 4 verificaciones**, y la que caza los tres modos: **"el dato responde a lo
  que pedí?"**. Escrita en el SKILL.md con los tres incidentes medidos, para que se entienda por
  qué existe y no se relaje.
- ✅ `yt-dlp` instalado: la minería de comentarios que el Bloque 1 delega en
  `golden-investigacion-mercado` pasa de promesa a operativa, con `like_count` (objeciones
  ordenadas por validación real de la audiencia). Sube la calidad del insumo de los 3 bloques.
- Sin cambios de rol ni de reparto: la ruta orquesta, la investigación sigue siendo dueña del
  método de scraping (`scraping-firecrawl.md`, SF2.0).

## R1.4 — 2026-07-31 — Compuerta anti-fantasma: el scraper puede inventar el producto entero
- **Hallazgo medido en vivo (2026-07-31):** `firecrawl_scrape` con `formats:["json"]` sobre una
  página que no carga **no falla — alucina**. Devolvió *"Smart TV 55\" 4K LED, $499.99, 150 reseñas"*
  para una página de removedor de verrugas, con `statusCode: 200`.
- **Por qué es una compuerta de la ruta y no solo una nota de investigación:** el Bloque 1 alimenta
  al 2 y al 3. Un producto fantasma que entra en DECIDIR se convierte en página, creativos, copys y
  presupuesto de pauta. Sería el caso perfecto de las 4 compuertas pasando en verde sobre un dato falso.
- **Escrita en el SKILL.md junto al bloque MCP:** si `metadata.title` viene vacío, el dato NO pasa de
  bloque, no entra a `PRODUCTO.json` y no alimenta ejecución. Complementa a la COMPUERTA DE VERACIDAD
  (que valida claims contra etiqueta/INCI): esta valida que el **dato de origen exista**.
- 📖 Manual completo delegado en la dueña de la investigación:
  `golden-investigacion-mercado/references/scraping-firecrawl.md` (SF1.0). Coherente con el split:
  la ruta orquesta, la investigación es dueña del método.

## R1.3 — 2026-07-31 — Convivencia con el Centro de Mando, horneada en AUTO-MEJORA
- El Centro de Mando aceptó el reporte del renombre tras verificarlo en disco y reconoció a este
  chat-fábrica como dueño de la ruta y a `_SISTEMA/GOLDEN-360.md` como su documento maestro.
- **Regla de convivencia escrita en el SKILL.md** (antes vivía solo en un mensaje entre chats, que es
  donde el conocimiento se pierde): cambios de la ruta = cancha de la fábrica, con changelog y
  re-blindaje; cambios que tocan **estándares transversales** (protocolos, esquema `PRODUCTO.json`
  que otros chats escriben, numeración de fases/compuertas que verifica `candado.py`) = **aviso previo
  al Centro de Mando** para difusión; editar una hija a fondo = de su fábrica, aquí solo se detecta y
  se coordina.
- **Ley de sistema para splits y renombres (gaceta 5c-bis)**, nacida de la auditoría R1.1 de esta
  misma skill y ahora aplicable a TODA skill del ecosistema: numeración canónica declarada una vez en
  el SKILL.md · references nombradas por función, no por número · barrido de referencias cruzadas en
  todo `~/.claude/skills` antes de cerrar · stub de redirección en los paths viejos.

## R1.2 — 2026-07-31 — Renombrada: `golden-ruta-360` → `golden360`
- Pedido de FER: la skill se llama **Golden360**. El identificador (`name:` y carpeta) va en
  **minúscula** — `golden360` — porque el `name:` de una skill no admite mayúsculas; ninguna de las
  80 skills instaladas las usa. El nombre visible en el H1 sí es **GOLDEN 360**.
- Se propagaron las **22 referencias cruzadas** de una vez: 5 propias (name, H1, sello y las dos
  rutas a `scripts/candado.py`) y 17 en `golden-investigacion-mercado` (SKILL.md, README-COMUNIDAD,
  reglas-de-oro, producto-json, 00-identificacion-forense, 02-documento-maestro y su changelog).
  Un renombre que no propaga rompe a las hermanas en silencio: quedan apuntando a un nombre muerto.
- Disparadores nuevos por nombre: "Golden360", "golden 360", "corre la 360", "la ruta".
- **Nombre anterior: `golden-ruta-360`** (R1.0–R1.1), por si aparece en un chat viejo, en el mapa
  espejo o en un PROYECTOS/ ya creado.
- **Mapa espejo renombrado igual** (autorizado por FER desde este chat): `_SISTEMA/RUTA-PRODUCTO-360.md`
  → **`_SISTEMA/GOLDEN-360.md`** (R1.1), con un stub de redirección en el nombre viejo porque hay
  `PRODUCTO.json` y prompts de arranque de productos vivos que todavía lo nombran. De paso se corrigió
  allí la fila "Orquestador de todo", que seguía diciendo `golden-investigacion-mercado` desde antes
  del split del 2026-07-30.
- **Autorización permanente de FER (2026-07-31):** este chat-fábrica puede modificar todo lo de
  `golden360` sin pedir permiso, siempre que MEJORE los procesos, y es el encargado de gestionar la
  unión de todas las skills. El Centro de Mando conserva la autoridad sobre todo y todos: los cambios
  se le comunican.

## R1.1 — 2026-07-31 — Primera auditoría con `golden-skill-auditor` (867/1000 PLATA → reparada)
- **Numeración fósil (hallazgo crítico).** El split heredó las references tal cual venían de la era
  G4.x: la página decía "Fase 3" cuando el SKILL.md R1.0 la puso en la 4; la pauta decía "Fase 4"
  siendo la 7; el bot "Fase 6" siendo la 8; y el montaje se citaba como **"Fase 7.5", un número que
  ya no existe** en el pipeline (es la COMPUERTA 3). `candado.py` arrastraba lo mismo en su docstring,
  sus etiquetas y su mensaje de cierre. Consecuencia real: un Claude que abre una reference a mitad
  de corrida escribe la fase equivocada en `estado.fase_actual` y busca una compuerta inexistente.
  Se alineó TODO con el SKILL.md y con el mapa espejo del Centro de Mando, y se agregó la lista
  canónica de numeración en el propio SKILL.md como fuente única.
- **References renombradas por FUNCIÓN**, no por número: `03-pagina-shopify.md` →
  `pagina-destino-venta.md`, `04-pauta-golden-ads.md` → `pauta-golden-ads.md`,
  `07-chatea-pro-handoff.md` → `chatea-pro-handoff.md`. El prefijo numérico fue justamente el que
  mintió durante el split; el nombre por función no puede desincronizarse.
- **REGLA 7 · RE-ENTRADA (hueco de proceso).** Un pipeline de 12 fases no cabe en una sesión y la
  investigación casi siempre viene de otro chat, pero nada decía cómo retomar. Ahora: si existe
  `PRODUCTO.json` se lee `estado.fase_actual` y se continúa ahí; solo se re-verifica lo perecedero
  (precio/stock, competencia, anuncios activos si el estudio pasa de 30 días). Evita reinvestigar y,
  sobre todo, evita un segundo juego de datos que contradiga al expediente.
- **`candado.py` verifica lo que el SKILL.md promete.** Antes no miraba dos ítems que la Fase 9
  declara del paquete: los **creativos de la Fase 5** (archivo o prompt completo) con su **GIF** de
  demostración, y el **PDF Golden**. Ambos entran como advertencia (un GIF entregado como prompt es
  válido mientras no haya créditos), y la Fase 5 totalmente vacía sí reprueba: sin creativo no hay
  campaña. Además cierra recordando la Compuerta 4, no solo la 3.
- **Auxiliares de Fase 0.5** (`golden-archivos`, `golden-dropi-analisis`) se reportan como opcionales
  en `--skills` en vez de omitirse; su ausencia no es un hueco.
- **Rutas de hermanas completas** (`~/.claude/skills/...`) para `producto-json.md` y
  `20-seguimiento.md`: existían, pero escritas a medias parecían references rotas de esta skill.
- Description: se sumaron disparadores coloquiales ("quiero vender esto", "de cero a ventas",
  "sácalo a la calle") y el caso de RETOMAR un lanzamiento a medias.

## R1.0 — 2026-07-30 — Nace del split (pedido de FER: investigación pura + orquestador aparte)
- `golden-investigacion-mercado` G4.3 contenía DOS trabajos: investigar y orquestar el lanzamiento.
  FER pidió separarlos: **investigación pura** por un lado, y esta skill — la **RUTA 360** — como el
  orquestador que une todas las skills Golden.
- Hereda INTACTOS de la G4.x: los 3 bloques / 12 fases / 4 compuertas, el expediente `PRODUCTO.json`,
  la compuerta de veracidad con imágenes, la compuerta de montaje, el QA pre-encendido, el
  seguimiento con trampa COD y la retro. Nada se perdió: se reubicó.
- **Bloque 1 (DECIDIR) ahora delega entero** en `golden-investigacion-mercado` (leída en vivo):
  forense, intake+4 números, reconocimiento, investigación 360 con minería de comentarios, dossier,
  documento .docx. La COMPUERTA 1 la decide este orquestador con los datos que ella entrega.
- Se lleva consigo: `seo-aio-producto.md`, `03-pagina-shopify.md`, `04-pauta-golden-ads.md`,
  `organico-redes.md`, `07-chatea-pro-handoff.md`, `qa-pre-encendido.md`, `scripts/candado.py`.
- Nueva sección **AUTO-MEJORA** (mandato global de FER, autorización permanente): auto-calificarse
  al cerrar cada corrida, hornear lecciones con el ritual, arreglar huecos propios sin esperar pedido,
  y auditoría periódica con `golden-skill-auditor`.
- El esquema del expediente (`producto-json.md`) queda en la investigación (quien lo CREA es dueña
  del esquema); esta skill lo lee en vivo.
