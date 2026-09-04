---
name: golden-archivos
description: >-
  Golden Group — ORGANIZADOR DE BIBLIOTECAS DE ARCHIVOS. Toma control de carpetas caóticas
  (productos, creativos, marca, informes) y las deja coherentes: clasifica por tipo, pone
  nombres auto-descriptivos con el producto adentro, separa el material WEB listo para subir
  de los originales HD, aplica la regla anti-mezcla (ninguna carpeta con archivos sueltos al
  lado de subcarpetas), reubica lo que está en el producto equivocado y elimina duplicados
  reales, todo con log reversible y verificación VISUAL antes de borrar. Úsala SIEMPRE que
  el usuario quiera organizar, ordenar, limpiar, clasificar o auditar archivos y carpetas:
  "organiza mi escritorio", "acomódame estas carpetas", "esto está hecho un desastre",
  "tengo archivos duplicados", "no sé qué es este archivo", "revisa que todo esté en su
  sitio", "clasifica estas fotos o videos", "separa lo que subo a Shopify de los
  originales", "hay imágenes repetidas", "esto no va en esa carpeta", o cuando arrastre una
  carpeta suelta pidiendo que la ubique.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1004 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden Archivos — orden de bibliotecas de archivos

<!-- skill v1.6 · auditoría golden-skill-auditor 2026-08-23 (947→): TRES hallazgos, todos de la MISMA CLASE — trabajo que se calla sin error. (1) nombrar.sh ALLOW seguía sin `mkv` pese a que el changelog de v1.5 declaraba las listas "alineadas": clasificar.sh lo manda a VIDEOS y nunca recibía prefijo; verificado ahora por diff programático de ambas listas (huecos restantes: 0) — la lección es que "alineadas" se demuestra con un diff, no se afirma. (2) hoja-contactos.sh solo intentaba 8 formatos (jpg jpeg png webp gif heic mp4 mov): tiff/bmp/heif/webm/m4v/avi/mkv/svg/psd no se intentaban siquiera, así que no salían en el mosaico NI en la línea "no se pudo leer" — medido en sandbox: 4 archivos → "1 pieza". Eso contradecía la regla propia de la skill ("un mosaico que calla piezas invalida la verificación") en la herramienta de la fase 6, que es el corazón del método. Ahora la lista MEDIA_EXTS cubre todo lo que clasificar.sh trata como media, y el cierre imprime SIEMPRE "N de M piezas renderizadas" más un aviso si M>N y otro con los archivos no-media: el censo hace imposible la omisión silenciosa. (3) Sección "Conexión con el ecosistema" (estándar 9): los cambios y hallazgos relevantes se reportan a 🧠 GOLDEN - CENTRO DE MANDO — un criterio descubierto organizando (ej. dos marcas que son el mismo producto físico) le sirve a la tienda, la pauta y el bot, y si se queda en el chat se pierde. Blindaje: chflags -R uchg re-aplicado al cierre. -->
<!-- skill v1.5 · auditoría golden-skill-auditor 2026-08-21, verificada corriendo los 8 scripts contra un sandbox sintético (clasificar, nombrar DRY+real, separar-web dry+aplicar, duplicados, eliminar ok/rechazo, hoja-contactos con imágenes reales, deshacer): nombrar.sh ALLOW list (scripts/nombrar.sh:21) le faltaban 22 extensiones que clasificar.sh SÍ clasifica (svg, psd, ai, eps, tiff, bmp, numbers, tsv, zip, rar, 7z, rtf, txt, md, ppt, key, pages, hevc) — un logo .svg o un .zip de datos quedaban correctamente ubicados en su carpeta pero NUNCA se les anteponía el prefijo del producto, en silencio; ahora ambas listas están alineadas. Documentado en SKILL.md el formato real que escribe eliminar.sh con FORCE (dos md5 distintos separados por "!=", no un solo hash) — antes el ejemplo de formato del log no cubría ese caso. Blindaje: chflags -R uchg (mecanismo confirmado y re-aplicado al cierre de esta auditoría). -->
<!-- skill v1.4 · fix auditoría 2026-07-25: separar-web.sh es_generica ahora pliega casing y tilde (nocasematch + IMÁGENES explícito), así "Fotos"/"Canva"/"IMÁGENES" del usuario sí se reconocen — antes daba "0 piezas" en silencio con carpetas en casing natural; auditar.sh usa emojis en las cabeceras en vez de rayas de caja (regla global sin separadores de rayas) -->
<!-- skill v1.3 · ejercida en fuego real 2026-07-23 (986→1000): duplicados.sh sobre biblioteca real (1515 archivos), separar-web.sh exige que TODA la ascendencia entre unidad y archivo sea genérica (ruta_solo_generica) -->
<!-- skill v1.2 · auditoría 2026-07-23 (931→): eliminar.sh (el formato RM de ELIMINADOS.log se exigía pero ningún script lo producía y la corrida real ya se había desviado; ahora verifica md5 y se niega si no coinciden), separar-web.sh (la fase 4 no tenía herramienta y se escribía a mano cada vez, con criterios distintos entre imágenes y videos; corre en seco por defecto), auditar.sh chequeo 3 ahora aplica EXCL como los otros 5, hoja-contactos avisa y sugiere tandas cuando el mosaico pasa de 8 filas. CRÍTICO: auditar.sh daba falsos ✅ — usaba los filtros de exclusión como texto sin comillas, el shell los glob-expandía y find fallaba en silencio; ahora es array (un auditor que miente en verde es peor que no tenerlo). El detector de UUID pasó de "4 guiones" a la forma hex real 8-4-4-4-12: atrapaba nombres claros como "2026-07 (Jul-Ago) - por pedido.xlsx" y ahogaba los hallazgos reales en ruido -->
<!-- skill v1.1 · auditoría 2026-07-23: deshacer.sh portable a macOS (tac no existe en Darwin → tail -r, mv -n, resumen), log OBLIGATORIO y verificado escribible ANTES de mover en clasificar/nombrar (mover sin registro = irreversible), modo DRY de nombrar.sh documentado, hoja-contactos con filas automáticas (mosaico corto callaba piezas) y chequeo de ffmpeg, formato exacto de ELIMINADOS.log, duplicados.sh exige argumento y limpia temporales, auditar.sh cableado al flujo (apertura + QA de cierre) -->
<!-- skill v1.0 · GA1.0 original: 5 scripts + flujo de 9 fases, conocimiento de campo del ordenamiento MASTER (TOPPIK, LE'CÔTERRA, Logos Golden) -->

Tu trabajo es convertir carpetas caóticas en una biblioteca donde FER encuentre cualquier cosa en segundos y **nunca dude de qué es un archivo**. No es mover archivos por mover: es entender qué es cada pieza y ponerla donde tiene sentido.

## El principio que manda sobre todos

**Nunca clasifiques por el nombre del archivo. Ábrelo y míralo.**

Esta regla nació de errores reales y caros:
- Seis archivos llamados `Video 1 Shopify`…`Video 6 Shopify` parecían carpetas de un proyecto. Eran MP4 sin extensión, y al mirar un fotograma resultaron ser videos de **fibra capilar** — pertenecían a TOPPIK.
- Seis GIFs de 14-50 MB dentro de una carpeta llamada "Logos Golden" no eran logos: eran **tarjetas de presentación animadas del equipo**, con el nombre y cargo de cada persona.
- Un archivo llamado `Proyecto-Creador-de-Contenido.png` era el **logo de otra marca** (Feropel), no de Golden.

El nombre miente. El contenido no. Si vas a decidir el destino de un archivo, míralo primero.

## Antes de tocar nada: los límites duros

Estas carpetas se ven, se reportan, pero **no se reorganizan**:

- **Código y proyectos**: repos, `node_modules`, `.git`, temas Shopify (`.liquid`, `.json`, `settings_data`), builds. Renombrar ahí rompe cosas.
- **Datos de aplicaciones**: CapCut, JianyingPro, librerías de Photos. Son bases de datos internas.
- **Personal**: fotos familiares, eventos, documentos privados. Aunque estén desordenados, no son material de trabajo.

Si dudas si algo es código o creativo: los creativos son `jpg png webp gif mp4 mov pdf docx xlsx csv`. Todo lo demás, déjalo quieto.

## Flujo de trabajo

Trabaja en este orden. Cada fase asume la anterior hecha.

### 0. Infraestructura de seguridad (siempre primero)

Crea la carpeta de control y el log **antes del primer movimiento**:

```
<raíz>/_ORGANIZACION-PRODUCTOS/
├── movimientos.log      ← cada operación, formato: MV<TAB>origen<TAB>destino
├── ELIMINADOS.log       ← cada borrado, formato: RM<TAB>ruta-borrada<TAB>ruta-del-sobreviviente<TAB>md5
│                          (con FORCE el cuarto campo es md5-borrado!=md5-sobreviviente: dos hashes distintos,
│                           prueba de que NO era un duplicado exacto — ver scripts/eliminar.sh)
└── LEEME.md             ← acta de qué se hizo y cómo revertir
```

Todo movimiento y renombrado se registra. Nada se borra sin quedar anotado junto a su sobreviviente: el md5 compartido en la línea RM es la prueba de que lo borrado y lo conservado eran el mismo contenido, y la ruta del sobreviviente es la recuperación (copiar de vuelta). Esto es lo que permite decir con certeza "esto no lo perdí yo" cuando el usuario pregunte — y esa pregunta llega.

Los scripts que mueven (`clasificar.sh`, `nombrar.sh`) exigen el log y verifican que sea escribible ANTES del primer movimiento: si el log no se puede escribir, no se mueve nada. Nunca los invoques sin log — un movimiento sin registro es un movimiento que no se puede deshacer.

`scripts/deshacer.sh "<log>"` revierte todo en orden inverso (nunca sobrescribe; reporta al final cuántos revirtió y cuáles no encontró).

### 1. Reconocimiento

**Empieza siempre por `scripts/auditar.sh "<raíz>"`.** Es de solo lectura y en una pasada te da la lista de trabajo completa: carpetas que mezclan archivos con subcarpetas, carpetas vacías, basura de descargas, nombres crípticos que hay que mirar, copias sueltas y carpetas donde el material web está revuelto con los masters. Lo que sale con ✅ ya está sano y no hay que tocarlo — eso evita trabajo inútil y movimientos de riesgo.

Al cerrar, vuelve a correrlo: es la prueba objetiva de que el trabajo quedó bien.

Mide también el tamaño del terreno:

```bash
find "<raíz>" -type f ! -path '*/node_modules/*' ! -path '*/.git/*' | wc -l
du -sh "<raíz>"/*/ | sort -rh
```

Identifica las **unidades de producto** (cada carpeta que representa un producto o marca) y separa lo que es material de trabajo de lo que es personal/código. Reporta el mapa al usuario antes de mover masivamente.

### 2. Clasificación por tipo

`scripts/clasificar.sh "<carpeta>" "<log>"` mueve los archivos **sueltos de esa carpeta** (no entra en subcarpetas) a:

`IMÁGENES · VIDEOS · GIFS · LOGOS Y MARCA · DOCUMENTOS · DATOS Y EXCEL · OTROS`

Aplícalo solo a carpetas **planas y revueltas**. Si una carpeta ya tiene una estructura pensada (por orientación: `Img Cuadradas`/`Img Verticales`; por tamaño: `1080x1080`; por propósito: `ADS`, `ANTES Y DESPUES`), **respétala** — esa organización suele ser mejor que la genérica y aplanarla destruye trabajo del usuario.

Si algo cae en `OTROS`, revísalo a mano: es señal de que el clasificador no supo qué era.

### 3. Nombrado auto-descriptivo

`scripts/nombrar.sh "<carpeta-unidad>" "<log>" [DRY]` antepone el nombre del producto. Con el tercer argumento `DRY` solo imprime lo que haría sin tocar nada — úsalo SIEMPRE en la primera pasada de una unidad nueva para revisar el prefijo resultante antes de renombrar en masa:

```
VIDEO 8.mov        →  ACEITE ANTI HONGOS - VIDEO 8.mov
_prompt_a_2025…mp4 →  SERUM 7DAYS - _prompt_a_2025…mp4
```

**Conserva el nombre original, no renumeres desde cero.** Es contraintuitivo pero importante: en un caso real la secuencia era VIDEO 1,2,3,4,5,8 — renumerar habría convertido el 8 en 6 y **ocultado que faltaban dos videos**. El hueco es información. Preservarlo permitió demostrar que la ausencia era anterior a nuestro trabajo.

El script solo renombra creativos y documentos; nunca código ni configuración.

**Nombres crípticos** (`IMG_4924`, UUIDs, `RPReplay_Final…`): esos sí merecen nombre nuevo, pero **solo después de mirar el contenido**. `IMG_4924.GIF` se convirtió en `Tarjeta - Nombre Apellido (Gerente Comercial).GIF` porque abrimos el archivo y leímos el nombre y el cargo del integrante.

### 4. Separar WEB de HD/master

El usuario necesita saber, sin pensar, qué sube y qué no.

- **WebP y MP4 liviano (<10 MB)** = web, listo para subir → carpeta `🌐 WEB SHOPIFY` del producto
- **PNG/JPG pesados, `.mov`, 4K** = master/original → se quedan en las carpetas de estudio

Regla operativa: abre `🌐 WEB SHOPIFY` y todo lo que hay ahí es subible. Lo demás es material de trabajo.

`scripts/separar-web.sh "<carpeta-unidad>" "<log>" [APLICAR]` lo hace por ti: sin `APLICAR` corre en seco y lista lo que movería. Corre siempre en seco primero — este paso reubica material que el dueño reconoce de memoria, y leer la lista antes evita sustos.

Solo toca carpetas-librería **genéricas** (`IMÁGENES`, `FOTOS`, `VIDEOS`, `CANVA`). No arrastra sets creativos deliberados (piezas de pauta por orientación, infografías con nombre propio): son creativos de anuncios, no assets de ficha de producto, y mezclarlos rompe el criterio de "todo lo que hay aquí se sube".

### 5. Regla anti-mezcla

**Ninguna carpeta debe tener archivos sueltos al lado de subcarpetas.** Al abrirla, o ves solo archivos, o ves solo carpetas. Detecta las infractoras:

```bash
find "<raíz>" -type d | while IFS= read -r d; do
  f=$(find "$d" -maxdepth 1 -type f ! -name '.*' | wc -l | tr -d ' ')
  s=$(find "$d" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')
  [ "$f" -gt 0 ] && [ "$s" -gt 0 ] && echo "[$f archivos + $s carpetas] $d"
done
```

Para cada una, agrupa los sueltos según **lo que son**, con un nombre que lo diga: scripts y configs → `_MOTOR`; informes PDF → `INFORMES`; documentos de un producto → `DOCUMENTOS`; videos que comparten origen → `Biblioteca de Anuncios`, `Videos Fibra`. El nombre de la subcarpeta debe explicar por qué esos archivos están juntos.

### 6. Coherencia de contenido

Aquí es donde de verdad aportas valor: **abre las carpetas y verifica que lo de adentro pertenezca ahí**.

Usa `scripts/hoja-contactos.sh "<carpeta>" "<salida.png>"` para generar un mosaico y **verlo todo de un golpe**. Luego lee la imagen. Es rapidísimo comparado con abrir archivo por archivo, y es como se cazan los intrusos. Si no pasas filas, el script las calcula para que entren TODAS las piezas — un mosaico que calla piezas invalida la verificación. Requiere ffmpeg (`brew install ffmpeg`); si no está, verifica abriendo los archivos uno a uno con Read — más lento, pero la verificación visual no se salta jamás.

Qué buscar:
- Material de **otro producto** (un banner de TOPPIK viviendo en la carpeta de banners de marca)
- Material de **otra marca** (el logo de Feropel entre los logos de Golden)
- Archivos que **no son lo que dice la carpeta** (tarjetas de presentación entre logos)
- Basura: `.crdownload` (descargas a medias), `.DS_Store`, carpetas vacías

Cuando dos productos son **el mismo producto físico con distinto nombre comercial**, el criterio es la marca visible: un creativo que no muestre marca sirve para ambos; si la muestra, pertenece a esa marca. Pregunta al usuario por estas equivalencias — no las adivines.

### 7. Duplicados

`scripts/duplicados.sh "<carpeta>" [...]` encuentra duplicados **exactos** agrupando primero por tamaño y hasheando solo los que colisionan (sobre bibliotecas de decenas de GB, esto es la diferencia entre segundos y colgarse).

**Antes de borrar cualquier cosa, míralas lado a lado.** La detección por similitud visual produce falsos positivos que destruyen material único. Casos reales que *parecían* duplicados y no lo eran:

- La **misma pieza en dos idiomas** (español / inglés)
- El **mismo producto en dos tonos** (IVORY / NATURE)
- El **mismo logo en dos colores** (beige / verde)
- **Fragancias distintas** de la misma línea, con arte casi idéntico
- Un **GIF animado** y su fotograma fijo
- La **versión web y la master** de la misma imagen — ambas se necesitan

Solo elimina cuando sea **el mismo archivo byte a byte**, o la misma imagen en menor resolución teniendo la mayor. Conserva siempre la de mayor calidad y la que esté mejor ubicada.

**Borra siempre con `scripts/eliminar.sh "<a-borrar>" "<sobreviviente>" "<ELIMINADOS.log>"`**, nunca con `rm` suelto. El script se niega a borrar si los md5 no coinciden y escribe la línea exacta que el log promete. Eso importa por dos razones: exige nombrar al sobreviviente (borrar sin saber qué queda es como no tener respaldo), y deja el md5 compartido como prueba de que lo borrado y lo conservado eran el mismo contenido. Para el caso legítimo de "misma imagen en menor resolución", añade `FORCE` como cuarto argumento — queda registrado con los dos md5 distintos para que se vea que no fue un duplicado exacto.

Ante la duda: no borres. Repórtalo y deja que el usuario decida.

**Atajo para copias sueltas.** Los archivos que aparecen en el Escritorio o en Descargas con prefijo `Copia de …`, ` (1)`, ` copy` casi siempre salieron de una carpeta ya organizada. Quítale el prefijo al nombre, busca ese nombre exacto en la biblioteca y compara md5:

```bash
orig="${f#Copia de }"
match=$(find "<biblioteca>" -type f -name "$orig" | head -1)
[ "$(md5 -q "$f")" = "$(md5 -q "$match")" ] && echo "duplicado exacto: borrar"
```

Si coinciden byte a byte y el original está bien ubicado, la copia suelta es basura segura de eliminar. Es el caso más limpio de deduplicado: cero riesgo, cero ambigüedad. Aun así se registra: línea `RM` en `ELIMINADOS.log` con la copia borrada, el original que sobrevive y el md5 compartido.

### 8. Cierre

Re-corre `scripts/auditar.sh "<raíz>"` — el mismo diagnóstico del inicio, ahora como QA: todo punto debe salir en ✅ o estar justificado en el reporte. Verifica y reporta:
- Cero carpetas mezcladas
- Cero carpetas vacías — salvo las que representen un producto real sin material aún (consérvalas a propósito y dilo)
- Cobertura de nombrado al 100%
- Total de operaciones reversibles

Actualiza `LEEME.md` con lo hecho, lo que dejaste intacto **y por qué**.

## Trampas técnicas que cuestan horas

**Renombrar mientras `find` recorre.** Si haces `find … | while read f; do mv …; done`, el recorrido se desincroniza y **se salta archivos en silencio**. Pasó de verdad: la primera pasada dejó LE'CÔTERRA con 5 de 126 archivos renombrados y no dio ningún error. Toma la lista completa primero (a un temporal), después renombra. Los scripts de esta skill ya lo hacen.

**Verifica cobertura, no confíes en el contador.** Después de una pasada masiva, cuenta cuántos archivos quedaron sin procesar. Un "1388 renombrados" suena a éxito y puede esconder un 20% saltado.

**Colisiones de nombre.** Al mover a una carpeta común, dos archivos pueden llamarse igual. Nunca sobrescribas: agrega ` (2)`.

**Rutas con emojis, tildes y espacios.** Son la norma aquí (`⭐️ MASTER ⭐️`, `LE'CÔTERRA`, `🌐 WEB SHOPIFY`). Entrecomilla siempre las variables e usa `IFS= read -r`.

**Mosaicos con ffmpeg.** Usa `format=rgb24` — mezclar PNG con transparencia y JPG hace fallar el filtro `tile` y devuelve un mosaico vacío. No uses `drawtext` para numerar: sin fuente configurada el filtro se cae en silencio; imprime el índice por consola y mapea número → nombre.

## Cómo reportar

FER decide rápido si le das evidencia, no adjetivos. En cada reporte:
- **Qué encontraste**, con números (`16 web + 9 master revueltos`)
- **Qué hiciste**, agrupado por decisión
- **Qué dejaste intacto y por qué** — esto genera tanta confianza como lo que tocaste
- **Qué queda pendiente** o necesita su criterio

Si el usuario sospecha que perdiste algo, no te defiendas: **ve al log y demuéstralo** con datos (`311 operaciones, todas MV, cero borrados`).

## Conexión con el ecosistema

Los cambios relevantes de esta skill — y los hallazgos que deje una corrida grande (una biblioteca reorganizada, una clase de error nueva, un criterio que FER dictó) — se reportan a **🧠 GOLDEN - CENTRO DE MANDO**. Quien ejecuta la skill hace ese reporte al cerrar; esta skill no tiene mensajería propia ni la necesita. El motivo es que el ecosistema decida como un solo sistema: un criterio de organización que se descubre aquí (ej. "Marbella y Candy Bella son el mismo producto físico") le sirve a la tienda, a la pauta y al bot, y si se queda en este chat se pierde.

## Referencias

- `references/estructura.md` — léela ANTES de crear o reorganizar cualquier carpeta de producto (fases 2 a 5): trae la anatomía estándar, la regla de nombrado, WEB vs MASTER y las reglas de identidad entre productos

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — ORGANIZADOR DE BIBLIOTECAS DE ARCHIVOS. Toma control de carpetas caóticas (productos, creativos, marca, informes) y las deja coherentes: clasifica por tipo, pone nombres auto-descriptivos con el producto adentro, separa el material WEB listo para subir de los originales HD/master, aplica la regla anti-mezcla (ninguna carpeta con archivos sueltos al lado de subcarpetas), reubica lo que está en el producto equivocado y elimina duplicados reales — todo con log reversible y verificación VISUAL antes de borrar. Úsala SIEMPRE que el usuario quiera organizar, ordenar, limpiar, clasificar o auditar archivos y carpetas — "organiza mi escritorio", "acomódame estas carpetas", "esto está hecho un desastre", "tengo archivos duplicados", "no sé qué es este archivo", "revisa que todo esté en su sitio", "clasifica estas fotos/videos", "separa lo que subo a Shopify de los originales", "hay imágenes repetidas", "esto no va en esa carpeta" — o cuando arrastre una carpeta suelta pidiendo que la ubique. Dispara aunque no diga "organizar": basta con desorden de archivos, duplicados, nombres crípticos (IMG_4924, UUID, "Video 1") o material de producto mezclado. NO para código/repos, datos de ventas (golden-dropi-analisis) ni generar imágenes (golden-imagen-arena).

