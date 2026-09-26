# Changelog — GOLDEN 360

## R2.3 — 2026-09-05 — Ciclo del mandato v2: lo tipo A cerrado, lo tipo B declarado
- **Mi propio barrido de acentos había corrompido 3 palabras POR DENTRO.** El par
  `formula → fórmula` se aplicó como SUBSTRING y se pegó dentro de palabras más largas:
  **"fábricante"** en la REGLA 2 (la innegociable de veracidad de etiqueta), **"fórmulario COD"**
  en la Compuerta 4 y **"lecciónes"** en el changelog. Corregidas; barrido de verificación con cero
  daño restante. **La clase es real: un reemplazo de acentos aplicado como substring corrompe las
  palabras que CONTIENEN la corta.**
  **ALCANCE MEDIDO DESPUÉS, y corrige lo que yo insinué:** avisé de esto como si hubiera que repartirlo
  al arsenal. El Centro de Mando lo midió — **1.131 ficheros, 38 skills, CERO corrupciones vivas**: el
  daño quedó contenido en esta casa y este ciclo ya lo cerró. Las únicas apariciones restantes eran mis
  propias actas citando la palabra rota para explicar que la había arreglado. **La clase valía; el
  alcance era cero, y yo lo di por extendido sin medirlo.** Un aviso urgente se reparte DESPUÉS de
  medirlo: repartirlo antes habría puesto a 38 fábricas a buscar un daño inexistente.
- **Dos falsos positivos de mi propio detector:** marcó "ángulos" como corrupto y es plural legítimo.
  Un detector de daño también necesita saber qué NO es daño. El CdM llegó al fondo de esto midiendo
  cuatro veces con instrumentos distintos (24 → 38 → 20 → 1 → 0 skills, sin que cambiara un byte del
  arsenal) y dejó la ley: **un detector hecho de patrones acusa al IDIOMA, no al defecto** — páginas,
  números, ángulos, críticos, análisis son formas correctas que ningún patrón morfológico distingue de
  una corrupta. Lo que hay que enumerar son las formas ROTAS, una por una.
- **Ley aplicada a mi propio detector, y verificada aquí:** el de fronteras se probó con tres
  redacciones legítimas distintas y CALLA en las tres; el control sin desambiguación MUERDE. Hasta hoy
  solo lo había probado por el lado malo, que es exactamente el error que la ley describe.
- **REFINAMIENTO DE golden-ads (vía CdM) QUE ME ENCONTRÓ UN FALSO NEGATIVO:** el lado bueno de una
  prueba no es prosa inocente, es el **CASO DISFRAZADO** — texto que SE PARECE al dato. Probado: una
  description que solo CITA la frontera dentro de un acta ("en R2.1 se repuso el bloque que decía
  NO es para una pieza suelta…") o dentro de un ejemplo **pasaba en VERDE**. Mi detector medía la
  presencia de unas palabras, no que la regla estuviera ENUNCIADA. Arreglado: la cita se delata por ir
  entrecomillada o por narrar en vez de enunciar. **6 casos ahora: 3 redacciones legítimas aceptadas,
  2 disfraces mordidos, 1 control mordido.**
- **TERCER DISFRAZ, el de AUTORIDAD (golden-presenta vía CdM), medido y cazado:** un texto puede tener
  la forma EXACTA de una frontera y no mandar sobre nadie aquí — *"Catálogo del arsenal: golden-shopify
  NO es para pauta, deriva a golden-ads"* pasaba en verde. Su formulación cierra la mía y es mejor:
  **no basta preguntar "cómo está escrito", hay que preguntar "esto MANDA sobre alguien"**. Resuelto
  por ESTRUCTURA, no por catálogo de palabras (que acusaría al idioma, contra la ley del CdM): una
  hermana como SUJETO de la negación es regla ajena; como DESTINO, es regla propia. **Banco de 7:
  3 legítimas aceptadas, 3 disfraces mordidos, 1 control mordido.**
  Y el aviso que viene con ella, que me parece el más fino de la noche: acusar un bloque cercado o una
  cita **castiga justo a quien documenta el error**. Un validador que muerde a las actas empuja a no
  escribirlas.
- **BANCO COMPLETO CORRIDO TRAS ESTRECHAR DOS VECES (aviso de golden-shopify vía CdM):** quitar
  falsos positivos **consiste** en estrechar el criterio, y estrechar es justo el mecanismo que
  fabrica falsos negativos — él lo midió: arregló 3 disfraces y el mismo arreglo le dejó el caso malo
  sin morder, 36 de 37. Así que corrí **el lado malo ENTERO**, no solo el disfraz nuevo:
  **8 de 8 muerden** (3 disfraces · sin frontera · description >1024 · sello sin changelog · name
  distinto de la carpeta · hija inexistente), y los 4 buenos siguen aceptados. **Banco de 12, los dos
  lados.** Sin defecto: los dos estrechamientos de hoy no rompieron nada. Se registra la verificación
  aunque saliera limpia, porque "lo corrí y salió bien" solo vale si dice CUÁNTOS y CUÁLES.
- **MIRAR LA COSA, NO EL VECINDARIO — el fallo del CdM aplicado a mí, y me encontró DOS.** Él midió
  que probaba el placeholder contra el CONTEXTO en vez de contra el VALOR, y 4 de 5 credenciales
  reales quedaban sin detectar. Aquí pasaba lo simétrico: mis señales miraban TODO el texto, así que
  una frontera propia y sana **MORÍA** si en otra frase aparecía "se repuso" o el nombre de una
  hermana. Medido: 2 de 3 fronteras legítimas mordidas. Arreglado juzgando **cada aparición por sí
  misma**, y basta UNA limpia: un texto no deja de establecer su frontera porque además cite la de
  otro. Tercera vez en la noche que el mismo principio aparece desde un terreno distinto.
- **Y al ampliar el criterio metí un CRASH que el lado malo no podía ver.** Añadí "NO para" a la
  lista de marcas y dejé una línea que solo conocía dos de las tres: `ValueError` con una frontera
  legítima. **Un crash sale con exit 1, exactamente igual que "muerde bien"** — por el lado malo era
  invisible; lo destapó el lado BUENO. Ahora el banco **mira el traceback, no solo el código de
  salida**, y la posición se busca con la misma lista MARCAS: dos fuentes de verdad para una lista es
  la deuda que se paga así.
- **Mi banco volvió a mentir, y por segunda vez en la noche.** Nombré las carpetas de prueba `g0`,
  `g1`… y los 6 casos buenos "fallaron": el validador oficial exige que la carpeta se llame como el
  `name`, así que reprobaba TODO sin que hubiera nada roto. **Un banco mal montado se lee igual que
  un detector roto.** Las copias se llaman `golden360` desde ahora.
- **Banco final de 14, los dos lados y sin crashes: 6 buenos aceptados, 8 malos mordidos.**
- **Y el chequeo declara su límite al pasar**, en vez de dar un verde ciego: mide PRESENCIA de la
  frontera, no que esté bien redactada. Una cita disfrazada de regla se caza; una regla mal escrita,
  no. Decir lo que un validador NO cubre es parte de lo que valida.
- **Sobre el md5 que el CdM no pudo verificar:** el número era reproducible, con la receta canónica de
  la casa que vive en `golden-skill-auditor` Fase 5 — `find . -type f | sort | xargs md5 -q | md5 -q`
  —, y reproduce exacto. Su diagnóstico ("el mandato nunca dijo QUÉ se hashea") es correcto sobre el
  mandato, pero la casa **ya tenía receta escrita**: el hueco no era que faltara, era que el mandato no
  la citó y la búsqueda no llegó hasta donde estaba. Es la misma familia que "preguntar lo ya guardado
  es un fallo de proceso", aplicada a una regla de verificación.
- **Alineación del `--autochequeo` con el oficial, comprobada CORRIENDO y no leyendo:** se saboteó el
  `name:` para que `agentskills validate` fallara por una causa que este script no implementa
  (nombre distinto de la carpeta) y el autochequeo la propagó con exit 1. La delegación es real, no
  decorativa: caza fallos que yo nunca programé, que es justo el punto de delegar.
- **Arsenal re-derivado ejecutando, no citado:** 15 hijas + 2 auxiliares, 0 faltantes hoy.
  Compuerta oficial con ruta absoluta: **Valid skill, exit 0**.
- **PARA EL 1000 ME FALTA: una corrida real de punta a punta — una foto entrando por el Bloque 1 y
  saliendo por la Compuerta 4, con las 4 compuertas dictando sobre un producto que existe. Lo puede
  dar: FER (una corrida real). No lo puedo cerrar yo.**
  Techo alcanzable hoy: **985**. Borrar esa reserva para escribir 1000 sería inflar el número en vez
  de mejorar la skill, que es exactamente lo que el mandato v2 prohíbe.

## R2.2 — 2026-09-05 — El tope estaba equivocado: la skill estaba INVÁLIDA y mi validador lo tapaba
- **Lo cazó el Centro de Mando; lo confirmé ejecutando el oficial antes de aceptarlo:**
  `agentskills validate` → código 1, *"Description exceeds 1024 character limit (1276 chars)"*.
- **El error, en una línea:** R2.1 usó **~1536** como tope. Ese número es el **truncado de RUNTIME**
  (donde el motor corta el listado al cargar). El que decide si la skill es válida es **1024, el
  límite de VALIDACIÓN de la especificación**. Son dos mecanismos distintos y los mezclé.
- **Lo grave no fue el número, fue dónde lo puse:** lo horneé en `--autochequeo`. Un validador con el
  umbral mal puesto da VERDE sobre una skill inválida — es peor que no tener validador, porque
  además tranquiliza. Ahora el autochequeo **corre el `agentskills validate` oficial** y solo usa el
  conteo propio como respaldo si el binario no está en PATH.
- **Recorte hecho donde no duele:** 1.276 → **1.004** caracteres sin tocar las FRONTERAS. Se fue la
  enumeración de las seis hermanas una a una (cara, y el usuario no las nombra al invocar) y los
  sinónimos repetidos de invocación. La desambiguación queda entera y al 38% del texto.
  Oficial: **Valid skill, exit 0**.
- **Un falso rojo propio, corregido:** el detector de fronteras exigía el carácter `→`. Al recortar
  desapareció la flecha y gritó rojo sobre una frontera que estaba perfectamente. Ahora las reconoce
  por SENTIDO (un "NO es para X" que además dice a dónde va lo que no es de esta skill), no por un
  carácter tipográfico. **Atar un chequeo a un símbolo es atarlo a la moda de quien redacta.**
- **Probado contra sabotaje**, como manda la higiene: description de 1.180 → oficial exit 1 y
  autochequeo exit 1. El primer intento de sabotaje NO mordió porque el patrón de reemplazo no casó
  y el relleno nunca entró — o sea el sabotaje falló, no el detector; se rehizo sin depender del
  texto exacto. Un banco de pruebas también se verifica.
- **DOS TECHOS, escritos ya en el SKILL.md** para que nadie los vuelva a mezclar: 1024 valida,
  ~1536 trunca.

## R2.1 — 2026-09-05 — Automejora: lo que se rompía en prosa ahora es candado ejecutable
- Pedido de FER: *"qué te falta para ser mil"*. Se midió, se cerró lo cerrable y se declara lo que no.
- **Las FRONTERAS de la description habían desaparecido.** El recorte del 3-sep (de 1.344 a 998
  caracteres) se llevó el bloque "NO es para una pieza suelta — deriva a…". En un ORQUESTADOR que
  compite con ocho hermanas, esa es la línea que evita que se dispare cuando pedían solo la página o
  solo la pauta. Repuestas, y **reubicadas al 32% del texto**: el truncado del listado muerde por el
  final, así que la desambiguación ya no puede volver a caerse por ahí. 1.276 de 1.536 caracteres.
- **Es la SEGUNDA vez que pasa** (7-ago y 3-sep), así que se atacó la clase, no el caso:
  **`candado.py --autochequeo`** verifica ahora que la description conserve las fronteras y quepa en
  el tope, que el sello más nuevo tenga entrada en el changelog, y que toda hija declarada exista en
  disco. Una regla que no se puede correr no es una regla: es un buen propósito.
- **El validador se probó contra casos malos** (higiene de FER: si pasa a la primera, sospecha del
  script). Con las fronteras borradas → falla, exit 1. Con un sello R9.9 sin entrada de changelog →
  falla, exit 1. Muerde.
- **SIMULACRO del camino feliz**, que en cinco meses nunca se había corrido: se armó un paquete
  completo de fixture (expediente con las 2 compuertas, .docx, PAUTA, ORGANICO, CHATEA-PRO con sus 2
  piezas, README con la ruta del cerebro, /creativos con GIF y PDF) → **PAQUETE COMPLETO, exit 0**.
  Hasta hoy el candado solo se había visto FALLAR; un script probado en una sola dirección puede
  tener el camino feliz roto y nadie lo sabría.
- **Acentos:** la entrada R2.0 y su sello venían sin tildes (escribia, organico, angulo, leccion,
  autorizacion, fabrica, acompana, enseno) — 26 correcciones, sin tocar el contenido.
- **Lo que NO se cierra con código, y por eso no hay mil:** la ruta sigue **sin correrse entera con un
  producto real**. Está auditada, simulada y blindada; no estrenada. Esa reserva la cierra un producto,
  no un commit.

## R2.0 — 2026-09-03 — FASE 5B · Teardown de los creativos (encargo de FER)

- **El copy se escribía sin haber desarmado el video.** La ruta iba Fase 5 (creativos) → Fase 6
  (orgánico) → Fase 7 (pauta), y en ninguna parada alguien miraba el video segundo a segundo antes
  de escribir el texto que lo iba a acompañar. Textual de FER: *"ya tengo los videos, entonces voy a
  analizar cada video y analizar cada imagen, y con la skill de copywriting voy a crearle sus copys
  a cada anuncio"*.
- **Nace la FASE 5B**, entre la Compuerta 2 y el Bloque 3: cada video pasa por `golden-video-teardown`
  y su ficha (beat sheet, ángulo, copy quemado, fórmula) entra al contexto de `golden-copywriting` y
  `golden-ads`. El argumento en una frase: **escribir el copy sin ver el video es narrar un partido
  por radio sin verlo.**
- **Se tocaron las CUATRO caras**, que es la lección que dejó R1.9 cuando una dependencia obligatoria
  "no existía para el sistema" por estar solo en la prosa: la fase en el cuerpo, la fila en la tabla
  REQUISITOS, la entrada en `HIJAS` de `candado.py` y este changelog con su sello.
- **Frontera declarada:** el rendimiento en números (CPA, ROAS, qué pausar) sigue siendo de
  `golden-meta-ads-analysis` en la Fase 10; 5B es lectura del creativo, no de la cuenta.
- Ejecutado por el **Centro de Mando** con autorización expresa de FER, por estar cerrada la fábrica
  (chat exclusivo golden360). Origen del hallazgo: chat EL CARTEL DEL CHAT, preparando la charla.

## R1.9 — 2026-08-24 — Auditoría fresca (918 base · 903 con reserva → PLATA, reparada)
- **La dependencia obligatoria del Paso 0 no existía para el sistema.** El bloque "Cerebro de marca"
  que el Centro de Mando instaló el 23-ago exige `golden-brand-brain` ANTES de generar nada, pero esa
  skill no estaba ni en la tabla REQUISITOS ni en `HIJAS` de `candado.py`. Consecuencia medida:
  `candado.py --skills` decía "✅ ecosistema completo" aunque faltara justo la skill del Paso 0 — el
  chequeo de dependencias daba verde sobre un hueco. Ya está en las dos listas.
- **"Pasa la ruta del cerebro" era una orden sin destino.** No decía dónde vive el cerebro ni dónde se
  anota, y el esquema `PRODUCTO.json` no tiene campo para ella. Ahora: el cerebro es de la MARCA (vive
  fuera de `PROYECTOS/<PRODUCTO>/`, su ruta la declara `golden-brand-brain`) y se escribe en la
  **cabecera del `README.md`** del paquete — con su fila ya en la plantilla de la Fase 9 — más el
  encargo de cada hija. Un dato que solo vive en la conversación se pierde en el próximo chat.
  📌 Elevado al Centro de Mando: añadir `marca.cerebro_ruta` al esquema. Es ESTÁNDAR TRANSVERSAL y por
  la convivencia de esta skill no se toca sin su aviso previo.
- **El sello R1.8 declaraba una cifra falsa.** Decía "`candado.py --skills` corrido de verdad → 15/15
  hijas instaladas + 2 auxiliares": ejecutado hoy son **13 hijas** + 2 auxiliares + 1 extra. Las 15
  líneas verdes se leyeron como 15 hijas y los auxiliares se contaron dos veces. Corregido en el sello.
  Un "verificado en vivo" con la cifra mal contada es peor que no dar cifra: la siguiente auditoría la
  copia. (Con `golden-brand-brain` la lista pasa hoy a 14 hijas.)
- **Dos cambios sin entrada de changelog**, la misma falla que R1.6b ya había registrado a posteriori
  el 11-ago — o sea la clase se repitió: la auditoría R1.8 (21-ago) y la adenda del cerebro (23-ago).
  Ambas quedan registradas abajo. Quien lea el historial ya ve el estado real.
- **Sellos reagrupados:** R1.2/R1.1/R1.0 habían quedado DEBAJO de la sección "Los 3 bloques", partiendo
  el bloque de versión en dos con contenido vivo en medio — la sección quedaba expuesta a irse en la
  próxima poda de sellos. Ahora los 6 sellos van juntos bajo el H1, como manda el patrón de la casa.
- Menores: `seo-aio-producto.md` citaba `claude-seo-ai` a secas cuando el SKILL.md ya lo precisó como
  `claude-seo-ai:audit` (es un PLUGIN); y la adenda del CdM venía sin tildes ("no leian", "identico",
  "fábrica") — corregidas sin tocar su contenido.
- Verificado ejecutando, no citando: `ast.parse` limpio · `candado.py --skills` corrido → ecosistema
  completo con la hija nueva · inventario 0 rotas / 0 huérfanas / 0 dudosos · blindaje 12 de 12 nodos ·
  sin secretos · sin signos de apertura.
- **Reserva que NO cierra con código y baja el puntaje con honestidad:** la ruta sigue sin correrse
  entera con un producto real. Está auditada, no estrenada.

## R1.8b — 2026-08-23 — Paso 0 · Cerebro de marca (registrado a posteriori el 2026-08-24)
- El Centro de Mando instaló el bloque "Cerebro de marca" tras el hallazgo del chat FILTRO DE
  HERRAMIENTAS: 7 de 12 skills de contenido no leían el cerebro. Bloque idéntico en 6 skills del CdM.
  Quedó en el SKILL.md con su adenda propia, pero **sin entrada aquí**. Se registra ahora.

## R1.8 — 2026-08-21 — Auditoría golden-skill-auditor 959 → 1000 (registrada a posteriori el 2026-08-24)
- Se selló en el SKILL.md pero **no se escribió aquí**. Lo que hizo: (1) concordancia de género en la
  línea disparadora del description ("este skill" → "esta skill"); (2) la Fase 9 exigía `README.md` en
  `candado.py` y en el texto pero sin plantilla, así que cada corrida inventaba su formato — se agregó
  la plantilla exacta (índice + compuertas + pendientes) bajo la Fase 9.

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
