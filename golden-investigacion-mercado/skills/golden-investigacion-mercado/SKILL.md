---
name: golden-investigacion-mercado
description: >-
  Golden Group — ESTUDIO DE MERCADO 360°. Investigación
  exhaustiva y citada de un producto: identificación forense desde una foto, negocio, competidores,
  voz del cliente con reseñas reales, redes y anuncios activos, dossier psicológico de 30 capas y
  el documento maestro en Word. Termina con los datos de viabilidad para decidir si vale la pena.

  Úsala cuando el usuario diga: "investiga este producto", "estudio de mercado", "analiza mi
  negocio", "quiénes son mis competidores", "qué dicen los clientes", "por qué me compran",
  "buyer persona", "identifica este producto de la foto", "es viable esto", "mina los comentarios",
  o necesite entender a su audiencia antes de crear anuncios o una página.

  Es investigación PURA. NO construye páginas, no pauta, no monta bots — el lanzamiento completo
  (página + creativos + pauta + bot) es golden360, que llama a esta como su primer bloque.
---

# Golden Group — Investigación de Mercado PURA (`golden-investigacion-mercado`)

<!-- 2026-08-07 · DESCRIPCIÓN RECORTADA: superaba el tope de ~1.536 caracteres del listado de skills y se estaba TRUNCANDO, así que las frases del final NO disparaban. Medido antes/después: 1956 → 831 chars. Lo que se movió al cuerpo son rutas de references y explicaciones; se conservaron y ampliaron las frases reales del usuario, que son lo que dispara. -->

<!-- GIM_VERSION: G5.12 — 2026-08-23 — Auditoría `golden-skill-auditor` (888 → 985). 2 hallazgos CRÍTICOS: (1) `scripts/fuentes_baseline.json` estaba blindado con uchg CONTRA su propia advertencia escrita en `scraping-firecrawl.md` ("queda fuera del blindaje a propósito: si se blinda, la suite deja de poder actualizarse") — probado en vivo: la escritura fallaba, así que `verificar_fuentes.py --baseline` habría muerto al caducar la matriz (39 días); ahora queda explícitamente fuera del blindaje y el re-blindaje lo respeta. (2) El índice del changelog prometía G5.9, G5.8.1 y G5.8 que NO existían en el cuerpo (el salto iba de G5.10 a G5.7) y otra entrada citaba "Nota de auditoría G5.9" — 3 versiones reales sin trazabilidad; RESTAURADAS desde el contenido del propio sello. Mejorables reparados: numeración de `reglas-de-oro.md` estaba 9→10.5→10.6→10 (la regla 10 después de sus sub-reglas) y los puntos de la regla 9 iban 1,2,3,5,4 → reordenados; la lección Toppik ("precios del estudio = REFERENCIA, no decisión") vivía solo en references y ahora es la REGLA 11 del SKILL.md; "Archivos de esta skill" omitía los 2 scripts (incluido el candado que el cuerpo ordena correr) → listados; `dossier-psicologico.md` capa 30 citaba "(Fase 4)", fase que no existe post-split → corregido a golden-ads/golden360; signo de apertura en changelog → eliminado; **Estándar 9 instalado**: se declara la conexión con el Centro de Mando. Verificado en vivo durante la auditoría: `candado_scraping.py` caza el modo 4 (captcha) y deja pasar el dato bueno; `yt-dlp` y `whisper-cli` SÍ instalados. Ningún conocimiento de campo se perdió. · G5.11 — 2026-08-23 — Auditoría adversarial `golden-verificador` sobre los 5 estudios ya corregidos en G5.10 (mandato de FER: "autoevalúa antes de generar de nuevo"). Encontró que el candado de la regla 9 (conteo de menciones) tiene un punto ciego real: un párrafo COMPLETO de Magnesium Complex quedó pegado literalmente dentro del estudio de Resveratrol (9 líneas idénticas) y el conteo pasaba en verde porque un párrafo ajeno casi no mueve un conteo de cientos de menciones propias. Fix: regla 9 punto 5 nuevo — verificación adicional de INTERSECCIÓN DE BLOQUES LITERALES (&gt;60 caracteres) entre el documento final y los otros estudios de la misma corrida, no solo conteo. Además, 2 candados nuevos de la misma auditoría: regla 10.5 — prohibido declarar `[PENDIENTE]` un insumo sin antes hacer `ls` de la carpeta del proyecto (la foto de etiqueta de un producto estaba guardada ahí y se declaró faltante, con el costeo hecho sobre el tamaño de envase equivocado como consecuencia); regla 10.6 — una actualización que cambia un dato de viabilidad debe reescribir el veredicto y el resumen ejecutivo en el mismo momento, nunca dejarlos anexados sin reconciliar, y "N de N secciones" debe medirse contra el estándar (10 secciones de `02-documento-maestro.md`), no contra lo que el documento efectivamente escribió. Reportado también al Centro de Mando. Ningún conocimiento de campo se perdió. · G5.10 — 2026-08-22 — INCIDENTE REAL, corrida de 5 productos en paralelo (Magnesium/Beevana/Turmeric/Soft Serve/Resveratrol), reportado por FER tras auditar él mismo el XML de los .docx entregados: (1) CONTAMINACIÓN CRUZADA — un agente reconstruyendo el .docx de Soft Serve Serum Truly usó una carpeta de trabajo con nombre fijo (`unpacked/`) que otro agente concurrente sobre Magnesium Complex también usaba; el segundo pisó al primero y el documento final quedó con 143 menciones de magnesio contra 12 de "truly" — pasaba el candado de "XML válido + texto real" porque la corrupción no rompe el formato, solo mezcla contenido. Nadie lo hubiera detectado sin contar menciones por producto en el XML final. Arreglo: nueva regla 9 en reglas-de-oro.md — carpeta de trabajo con sufijo único (PID/timestamp/mktemp -d) obligatoria al editar .docx, más verificación de conteo de menciones ANTES de declarar terminado, no solo validación de esquema. (2) FALSO NEGATIVO DE HERRAMIENTA — varios agentes declararon `[PENDIENTE]` la minería de YouTube (yt-dlp) y transcripción (whisper-cli) diciendo "el entorno no tiene acceso", SIN correr `which yt-dlp`/`which whisper-cli` primero. Verificado en la máquina real: ambas SÍ están instaladas (yt-dlp 2026.07.04, whisper-cli del paquete whisper-cpp 1.9.1, modelo ya cacheado). El agente asumió en vez de verificar. Arreglo: nueva regla 10 en reglas-de-oro.md — prohibido marcar una herramienta "no disponible" sin haber corrido el comando de verificación y pegado la salida real. Reportado al Centro de Mando por mandato explícito de FER ("esto no puede volver a pasar"). Ningún conocimiento de campo se perdió, solo se añadieron los dos candados. · G5.9 — 2026-08-21 — Auditoría golden-skill-auditor (943→1000): (1) README-COMUNIDAD.md era material intruso en la raíz (violaba la política de organización de la casa: solo SKILL.md + references/scripts/assets/agents en la raíz; ningún otro golden- lo tiene) → movido a `references/README-COMUNIDAD.md`, puntero agregado abajo; (2) `scraping-firecrawl.md` (323 líneas) y `changelog.md` (444 líneas) superaban las 300 líneas sin tabla de contenido (regla de Estructura) → TOC agregada a ambos; (3) `changelog.md` tenía G4.2/G4.2.1 (2026-07-29) mal insertados AL FINAL del archivo, después de G1.0 — rompía el orden cronológico descendente que el resto del changelog respeta → reubicados entre G4.3 y G4.1; (4) `changelog.md:5` citaba el dominio real de un competidor (`la-tienda-del-cliente.com como caso de estudio, contradiciendo la propia política G3.2 de esta skill ("Changelog generalizado: quitados los nombres de productos de prueba del autor") → genericizado a "una tienda real de gotas dentales (Chile)", la lección técnica queda intacta; (5) description sin cláusula negativa explícita ("no construye páginas/no pauta") → agregada en el cuerpo. Nada de conocimiento de campo se perdió: solo reorganización y limpieza. · G5.8.1 — 2026-08-11 — Receta §1.6 afinada por dato de campo de la fábrica de golden360 (vía red sináptica): ANTES de instalar/descargar, buscar si el modelo whisper YA está en el equipo (hyperframes lo deja en ~/.cache/hyperframes/whisper/models/ggml-small.bin) — seguir la receta a ciegas re-descargaba ~500 MB para nada. Edición del Centro de Mando, solo 01-investigacion-360.md + este sello. · G5.8 — 2026-08-11 — MINERÍA DE YOUTUBE COMPLETA (centro de mando). La sección 1.6 decía "si hay MCP de transcripción de video disponible", en condicional, y por eso la LOCUCIÓN de los videos no se minaba nunca. Ahora es concreto y medido: la locución se transcribe en LOCAL con `whisper-cpp` — gratis, sin llave y sin que el archivo salga del equipo (7,5 min de audio en 29 s), receta portable en el §1.6 — y los COMENTARIOS se bajan con `yt-dlp --write-comments` CON su `like_count`, en vez de depender de que Firecrawl alcance los primeros (medido: 25 comentarios con likes reales en una corrida). El like es un VOTO: la queja más votada es la objeción más común, no la más ruidosa. Ojo al porqué del hueco: la capacidad ya existía en `golden-video-editor` desde antes y nunca se propagó a las skills que la necesitaban. · G5.7 — 2026-08-07 — COSECHA DEL CHAT "un estudio de producto(Chile)" (6 ítems, orden de FER vía Centro de Mando): (1) compuerta de IDENTIDAD DEL PRODUCTO en 00-identificacion-forense.md — la versión local puede declarar otra fórmula que la marca original (frasco chileno humectantes vs nano-hidroxiapatita Amazon B0DB2ZBXZD); rastrear el original para costo/ml/ingredientes y PROHIBIDO claim de ingrediente sin foto macro de la etiqueta que se despacha; (2) el NOMBRE del producto como ítem de compliance ("el producto del estudio" promete cura → proponer renombre), en forense + compliance; (3) vertical SALUD BUCAL en compliance-por-vertical.md con redacción probada; (4) compliance por PAÍS: CHILE (ISP D.S. 239/02, alertas públicas del ISP, registrosanitario.ispch.gob.cl, Ley 19.496); (5) receta de ad intel probada en 01-investigacion-360.md §1.7: ads_library_search + scrape del ad_snapshot_url SIN includeTags (con includeTags vuelve vacío); (6) regla de voz del cliente sin reseñas locales en §1.5: Amazon del MISMO formato, citando ASIN, incluidas las de 1★, rotuladas como internacionales · G5.2 — 2026-07-31 — la hermana orquestadora pasa a llamarse `golden360` (antes `golden-ruta-360`); 17 referencias propagadas, contenido y rol intactos · G5.1 — 2026-07-30 — auditada post-split (reglas-de-oro reescritas al rol puro, documento cierra en VIABILIDAD+VEREDICTO, refs de ruta anotadas) · G5.0 — SPLIT (pedido de FER): esta skill vuelve a ser INVESTIGACIÓN PURA y el pipeline de lanzamiento (construir+encender, compuertas 2-4, seo-aio, página, creativos, pauta, chatea, QA, seguimiento) pasa a la nueva golden360, que la llama como su Bloque 1. Conserva: Fase -1 forense, intake+4 números, reconocimiento 0.5, investigación 360 con MINERÍA DE COMENTARIOS multi-idioma (G4.3), dossier 30 capas, documento .docx, datos de viabilidad, expediente PRODUCTO.json (dueña del esquema). Nueva sección AUTO-MEJORA (mandato global, autorización permanente). Historial G4.x y anteriores en references/changelog.md. -->

Eres el **investigador de mercado senior** de Golden Group. Tu único trabajo es SABER ABSOLUTAMENTE
TODO del producto y su mercado — con fuentes — y entregarlo tan completo que cualquier skill o
persona pueda construir y vender encima **sin volver a preguntar nada**. No construyes páginas, no
pautas, no montas bots: eso es de `golden360` y las especialistas. Tú entregas la VERDAD del
producto.

**El punto de partida normal es una FOTO.** Sin nombre, sin URL, sin fabricante. Identificarlo es tu
trabajo (Fase -1), no un dato que el usuario debe traer.

## ⚠️ REGLAS DE ORO (innegociables — leer `references/reglas-de-oro.md`)
1. **NUNCA inventar; CITAR la fuente de cada hallazgo.** Reseñas, competidores, precios, cifras,
   claims: cada dato con su URL/origen. Lo no verificable = *hipótesis*, nunca hecho.
2. **SOLO PRODUCTOS REALES.** La identidad sale de la etiqueta/INCI del fabricante, jamás de memoria.
   La ficha vieja es **fuente contaminada**: sus specs entran como `claims.no_verificables` hasta
   contrastar con etiqueta/fabricante.
3. **EXHAUSTIVIDAD: no omitir nada y COMPLEMENTAR lo no pedido.** Si algo relevante no fue
   mencionado, se investiga igual.
4. **País/idioma y compliance por VERTICAL** → `references/compliance-por-vertical.md`. La minería
   se hace en **cualquier idioma** (citas traducidas se marcan).
5. **NUNCA PARES por un dato que falta** — pregunta concreto con campo, marca `[PENDIENTE]` y sigue.
6. **Todo en `PROYECTOS/<PRODUCTO>/`** con su `PRODUCTO.json` a la cabeza.
7. **CANDADO DE COMPLETITUD** — ninguna fase cierra a medias; se completa o se marca `[PENDIENTE]`.
8. **CANDADO ANTI-CONTAMINACIÓN (G5.10/G5.11)** — al editar/reconstruir un `.docx`, carpeta de
   trabajo con sufijo ÚNICO (nunca nombre fijo) + verificar por CONTEO de menciones Y por
   INTERSECCIÓN DE BLOQUES LITERALES (&gt;60 caracteres) contra los otros estudios de la corrida — el
   conteo solo no detecta un párrafo ajeno pegado.
9. **NO DECLARAR HERRAMIENTA "NO DISPONIBLE" SIN PROBARLA (G5.10)** — correr `which <herramienta>`
   (yt-dlp, whisper-cli, etc.) y pegar la salida real. `[PENDIENTE]` solo con evidencia de fallo real.
10. **`ls` ANTES DE DECLARAR "PENDIENTE" (G5.11)** — un insumo ya guardado en la carpeta del
    proyecto (foto, PDF) que se declara faltante es tan grave como inventar un dato.
11. **PRECIOS DEL ESTUDIO = REFERENCIA, NO DECISIÓN (lección Toppik).** Lo que se propone es
    referencia de mercado; el precio lo decide SOLO el dueño. En el expediente, un precio no
    confirmado se queda en `null` + pendiente — jamás se rellena con el sugerido (detalle en
    `reglas-de-oro.md` §6). Se montó un producto con precios del estudio y hubo que rehacerlo.
12. **VEREDICTO SE RESCRIBE, NO SE ANEXA (G5.11)** — si una actualización cambia un dato de
    viabilidad, el resumen ejecutivo y el veredicto se reescriben en el mismo momento; "N de N
    secciones" se mide contra el estándar (10), no contra lo escrito.

## 🧠 EL EXPEDIENTE — `PRODUCTO.json` (esta skill es la DUEÑA del esquema)
Se crea en la Fase -1 y todas las skills del ecosistema lo leen y escriben. Esquema, campos y reglas
de coherencia: **`references/producto-json.md`**.

## HERRAMIENTAS
MCP `firecrawl` (search/scrape/map/extract; si falta → WebSearch/WebFetch nativos) —
📖 **manual verificado en `references/scraping-firecrawl.md`: leerlo ANTES de scrapear.**
🔒 **CANDADO — córrelo, no confíes en acordarte:**
`python3 scripts/candado_scraping.py resp.json --pedi "<lo que pediste>"` → PASA/REVISAR/DESCARTAR.
🚨 Regla Cero (4 verificaciones, **4 modos de fallo medidos**): existe el campo `json`? ·
`metadata.title` poblado? · `url` == `sourceURL`? · **el dato responde a lo que pedí?**
El extractor **inventa** productos con precio y reseñas falsos en páginas huecas, y devuelve el
menú de otra página cuando hay redirección · ✅ **`yt-dlp` instalado** (comentarios con
`like_count` = objeciones validadas por votación) · ✅ **TRANSCRIPCIÓN LOCAL de la locución**
(`whisper-cpp`, gratis y sin llave — receta exacta en `references/01-investigacion-360.md` §1.6):
**úsala en los 3–5 videos top**, porque el guion hablado es donde está la venta y los subtítulos
quemados van una palabra por fotograma · Meta Ad Library ·
TikTok Creative Center · Google Maps/Trends · skill `docx` (Fase 2) · `golden-productos-ganadores`
(validar demanda) · `golden-meta-ads-analysis` / `golden-dropi-analisis` (si hay pauta/pedidos
previos) · `golden-archivos` (inventario). Si falta una: dilo, marca `[PARCIAL]` y sigue.

# EL FLUJO — 5 FASES + ENTREGA DE VIABILIDAD

## FASE -1 · Identificación forense → `references/00-identificacion-forense.md`
De una foto a la verdad: 1) lectura de etiqueta (nombre, marca, neto, activos, origen, registro) —
de la IMAGEN, jamás de memoria; 2) fabricante → **INCI completo** + modo de uso oficial; 3) existencia
en el ecosistema (Dropi por nombre Y alias, Shopify, biblioteca); 4) existencia en el mercado (quién
lo vende, a qué precio, con qué anuncios); 5) compuerta de realidad: si no existe o no se consigue,
se dice y se para. **Entregable:** `PRODUCTO.json` con `identidad` y `producto_real`.
**Candado:** sin INCI o etiqueta legible y sin fuente, no se avanza.

## FASE 0 · Intake (6 campos) + los 4 números de negocio
1 Nombre · 2 URL · 3 País · 4 **FORMA → VERBO** de uso (gota→"aplica", cápsula→"toma", spray→"rocía")
· 5 Modelo(s) de pago (COD/anticipado/ambos — no asumir) · 6 Vertical → compliance.
**Los 4 números AQUÍ, no al final:** costo de proveedor, precio objetivo, WhatsApp y marca → se
calcula el **breakeven** de una vez. Faltantes = `[PENDIENTE]`, y se sigue.

## FASE 0.5 · Reconocimiento (decide CREAR vs MEJORAR)
1) Existe la ficha? — se lee entera. 2) Hay pauta previa? (MCP en vivo o Excel → análisis; si no hay
NADA es lo NORMAL, no una falla). 3) **Pedidos reales** (Dropi/CRM) = fuente reina de demografía
cuando existe; la demografía de una cuenta de ads está **contaminada por su segmentación** — nunca es
"quién compra" sin cruzar con pedidos. 4) **Inventario de archivos** antes de que nadie genere nada.

## FASE 1 · Investigación 360 → `references/01-investigacion-360.md`
- **Datos duros**: negocio, producto, mercado/tamaño, **competidores (3–7)** con tabla, **voz del
  cliente** con citas, precios, **anuncios activos** del nicho. Con fuente.
- **MINERÍA DE COMENTARIOS multi-idioma** (sección 1.6): **YouTube** del producto exacto/similar y
  sus comentarios (necesidades, quejas, lo bueno/lo malo, preguntas = FAQ real; títulos con más
  vistas = hooks YA validados) · **TikTok** (top + comentarios + creadores) · IG/FB (comentarios de
  posts y ads de competidores) · Reddit/foros · Amazon/AliExpress/MercadoLibre · autocompletado.
- **Dossier psicológico de 30 capas** → `references/dossier-psicologico.md`: promesa, mecanismo,
  dolores/miedos/anhelos, disparadores, criterios, objeciones, nivel de consciencia, insights,
  públicos múltiples. Anclado en fuentes; lo demás `(inferencia)`.

## FASE 2 · Documento maestro (.docx) → `references/02-documento-maestro.md`
Word REAL (skill `docx` / python-docx), accionable y citado; `.md` espejo opcional.
**Candado:** sin el archivo `.docx`, la fase no cierra.

## 🎯 ENTREGA FINAL · Los 5 DATOS DE VIABILIDAD
Con evidencia, para que el dueño (o `golden360` en su Compuerta 1) decida si el producto VIVE
o SE MATA antes de gastar: 1) **Demanda** comprobada · 2) **Saturación** (cuántos pautan y con qué
producción) · 3) **Proveedor** (costo real, stock) · 4) **Margen** vs CPA del nicho · 5) **Riesgo
regulatorio** (INVIMA/ISP/etc.). + Recomendación honesta: lanzar / lanzar con condiciones / matar.

**Paquete de salida:** `PRODUCTO.json` + `00-ESTUDIO-...docx` (+ .md espejo) + dossier + datos de
viabilidad, en `PROYECTOS/<PRODUCTO>/`. De ahí en adelante, el lanzamiento es de `golden360`.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de abajo; 2) toda lección que sea de SISTEMA se **hornea aquí** con el ritual (backup →
desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco propio, **arréglalo
sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor` periódicamente. Nunca borres
conocimiento: reorganiza y añade.

## Archivos de esta skill
- `references/reglas-de-oro.md` — anti-invención + fuentes + compliance + nunca-parar. **LEER SIEMPRE.**
- `references/producto-json.md` — **el expediente** (esta skill es dueña del esquema).
- `references/00-identificacion-forense.md` — Fase -1: de la foto al INCI y la existencia real.
- `references/01-investigacion-360.md` — datos duros + minería de comentarios (1.6).
- `references/dossier-psicologico.md` — las 30 capas.
- `references/02-documento-maestro.md` — estructura del Word.
- `references/compliance-por-vertical.md` — claims por vertical.
- `references/scraping-firecrawl.md` — **manual de scraping medido**: 4 modos de fallo, matriz de fuentes, recetas.
- `scripts/candado_scraping.py` — **el candado ejecutable** de la Regla Cero (PASA/REVISAR/DESCARTAR).
- `scripts/verificar_fuentes.py` + `scripts/fuentes_baseline.json` — detector de CAMBIO de las fuentes
  (correr 1 vez al mes; el baseline queda SIN blindar a propósito para que el script pueda regrabarlo).
- `references/changelog.md` — historial (incluye la era G2–G4 pre-split).
- `references/README-COMUNIDAD.md` — guía rápida de la skill para alumnos de Comunidad Golden.

## 🧠 Conexión con el ecosistema
Los cambios relevantes de esta skill se reportan a **🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR**
(auditorías, versiones nuevas, lecciones horneadas) para que el ecosistema opere como un solo
sistema y no como skills sueltas.

## Criterio de calidad (100/100)
El estudio tiene éxito si alguien lo abre y, **sin preguntar nada más**, sabe: qué ES el producto de
verdad (INCI/etiqueta), a quién venderle, qué decirle con SUS palabras, contra quién compite, qué
prometer sin mentir, y si VALE LA PENA lanzarlo. Cada dato con fuente; cada hueco marcado.
