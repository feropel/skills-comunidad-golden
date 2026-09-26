# Modo CAZA con DropKiller: encontrar candidatos y separar los reales de los falsos

Lee este archivo entero antes de la primera llamada a DropKiller en una corrida. Todo lo que
dice está **medido** contra el conector el 2026-09-18 o sale de una fuente con nombre. El
método base viene de 39 videos leídos completos (21 del cofundador de DropKiller, Juan Vargas,
más el canal oficial y 7 practicantes); lo que aquí se agrega es lo que ellos no verifican.

## Contenido
1. Qué es DropKiller y de quién es la fuente
2. Las 30 herramientas del conector: cuáles se usan y para qué
3. Las 10 trampas medidas (por qué el top de DropKiller no se puede usar tal cual)
4. Los 3 criterios del catálogo público y las etapas del producto
5. Las 6 rutas de caza
6. El embudo de una corrida (qué se llama, en qué orden, qué se descarta)
7. Lo que se rechaza aunque lo enseñen los videos
8. Si el conector falla

## 1 · Qué es DropKiller y de quién es la fuente

Software colombiano de investigación de productos para dropshipping en LatAm: ventas por
producto de Dropi y otras plataformas, biblioteca de anuncios (AdsKiller), radar de tiendas
Shopify y TikTok Shop. Conector MCP en **fase beta** (dicho por su cofundador el 17-sep-2026).
Exige plan **Advance** (USD 24,99/mes; el básico de 19,99 solo trae Productos).

🔴 **Conflicto de interés, dos veces:**
- **Juan Vargas es cofundador de DropKiller.** Sus 21 videos venden la herramienta. Su método
  es bueno; sus cifras ("100% real", "3 de 5 testeos ganan") no traen fuente.
- **FER tiene enlace de afiliado de DropKiller** (15%). Toda ficha que recomiende pagar la
  herramienta lo declara en una línea. Callarlo sería presentar publicidad como consejo.

## 2 · Las herramientas que usa esta skill

| Herramienta | Para qué | Devuelve historial |
|---|---|---|
| `find_winning_products` | candidatos rápidos: ventana `7d`, `30d` o `trending`, país, plataforma, categoría, precio máximo | no |
| `search_products` | candidatos con TODOS los filtros (ventas 7d/30d min-max, totales SOLO mínimo (el máximo no existe, trampa 9), stock, precio, creado después de, proveedor verificado, orden) | no |
| `semantic_search_products` | **consolidar el mercado**: mismo producto por IMAGEN o por texto, con filtro de país | **sí (`history30d`)** |
| `get_product_history` | historial día a día de UN producto (hasta 400 filas) | sí |
| `list_product_filters` | países, plataformas y categorías válidas (llamar si hay duda) | — |
| `search_ads` / `semantic_search_ads` | **creativos y ángulos**: anuncios de ese producto en OTROS países, por texto o imagen, con `broadcastDuration` (new ≤7 · validated 7-30 · evergreen ≥30) | — |
| `analyze_ad` | si UN anuncio funciona comparado con el promedio del anunciante | — |
| `brief_store` / `store_tech_report` | radiografía de una tienda por dominio | — |
| `search_stores` | radar de tiendas por país (ingresos y visitas: **estimados viejos**, ver trampa 8) | — |
| `search_tiktok_products` / `list_tiktok_product_ads` | lo que vende TikTok Shop EE.UU. | — |
| `daily_radar` / `save_item` | seguimiento de productos guardados | — |

**Lo que el conector NO trae** aunque la interfaz sí lo muestre: el "índice de saturación", el
"winner score" de producto y cuántos usuarios rastrean un producto. No inventarlos.

## 3 · Las 10 trampas medidas

**Trampa 1 · VENTA FANTASMA (la más cara).** DropKiller calcula las ventas por **caída de stock
del proveedor**: el probador de inyectores bajó de 500 a 378 y "vendió" 122, exacto. Cuando el
proveedor vacía o corrige inventario, esa caída se cuenta como venta.
> Medido 2026-09-18, top 20 de `find_winning_products` en Dropi Colombia: **9 de 20 eran
> fantasma** (virex 3.000 → 300 = "2.700 vendidos"; turkesterone "2.961" en un día y stock final 1;
> tenis Adidas 1.360 → 1; Casio 976 → 1). El #1 y el #2 del ranking, los dos falsos.
> Cuatro fuentes independientes lo confirman: Juan ("22 ventas en un solo día no son
> acertadas"), Naider Ortiz dos veces ("el proveedor movió el stock"), y esta medición.

→ **Todo candidato pasa por `scripts/ventas_reales.py` antes de nada.** FANTASMA no entra;
DUDOSO no cuenta como validado; REAL entra con la cifra DEPURADA, no la reportada.

**Trampa 2 · ESPEJOS DE PLATAFORMA.** El mismo producto de Dropi aparece una vez por cada
plataforma que lo refleja (DROPI, WINPY, DROPLATAM, SEVENTY_BLOCK), con el mismo `externalId`,
el mismo proveedor y el historial idéntico.
> Medido: Dr. Melaxin salió 4 veces. "Sumar todos los proveedores" como enseña Juan daba
> ~37.000 ventas de un solo proveedor.

→ **Nunca sumar a mano. `scripts/consolidar_mercado.py`** colapsa espejos por `externalId`,
agrupa por proveedor y suma una vez.

**Trampa 3 · UN PROVEEDOR ENGAÑA.** Las ventas que muestra cada ficha son de ESE proveedor. El
mercado real es la suma de todos (Juan lo repite en 6 videos: antirronquio "900" → 30.000;
cámara espía "2.000" → 50.000; Bivenom "17" → 60.000). La búsqueda por imagen falla a veces y
la de texto trae homónimos: **se hacen las dos** y se filtra por nombre (`--incluir`).
> Medido: Dr. Melaxin crema consolidado = **19.049 ventas, QUEMADO**, y es el #6 de los
> "ganadores" de DropKiller.

**Trampa 4 · DÍA SIN LECTURA.** El historial rellena con stock 0, precio 0 y ventas 0 los días
anteriores a la creación del producto y el día en curso (Naider: "tiene un delay de 2 a 3
días"). No es un día sin ventas ni un vaciado. `ventas_reales.py` los descarta.

**Trampa 5 · "ACTIVO" NO ES ACTIVO HOY.** En `search_ads`, un anuncio sale `status: ACTIVE` con
`endDate` 2026-08-21 y visto por última vez el 22-ago. → La vigencia se lee en
`lastSeenActiveAt`: visto hace >7 días = no se cuenta como activo.

**Trampa 6 · PAÍS MAL ASIGNADO.** Anuncio que cobra en C$ (córdobas, Nicaragua) marcado como
Colombia. Su cofundador lo reconoce como bug "del tercero" y mira la moneda. → El país se
confirma por la **moneda** del texto o de la landing.

**Trampa 7 · "CON STOCK" = 1 UNIDAD.** `find_winning_products` exige stock ≥1: 3 de 8 tenían
stock 1. → Stock mínimo real **80** (curso oficial y canal de DropKiller: "para pautar
mañana"); si el usuario no dice otra cosa.

**Trampa 8 · CIFRAS DE TIENDAS VIEJAS.** El propio esquema del conector dice que los órdenes por
ingresos y visitas (SimilarWeb) se **retiraron el 2026-07-02 por fuente desactualizada**, y el
canal oficial: "son estimaciones, no 100% reales". → Ingresos de tiendas no entran a la ficha
como dato. `billing` de producto = precio de proveedor × unidades: **no** es lo que factura
una tienda (Juan quitó ese campo de la interfaz "porque no decía mucho").

**Trampa 9 · EL FILTRO QUE NO EXISTE SE IGNORA CALLADO.** `search_products` acepta
`minTotalSold` pero **no tiene** `maxTotalSold`: si se le pasa, no da error, lo ignora y devuelve
productos de 20.000 ventas mezclados con los de 300 (medido 2026-09-18, primera corrida real).
→ El techo de etapa **no se pide a DropKiller**: lo aplica `consolidar_mercado.py` sobre el
mercado consolidado. Antes de fiarse de un filtro nuevo, leer el esquema de la herramienta y
comprobar en la respuesta que el filtro cortó.

**Trampa 10 · ESPEJOS QUE NO CUADRAN.** Los espejos de un mismo `externalId` a veces reportan
cifras distintas: brasier 2.324 en DROPI contra 1.193 en WINPY y DROPLATAM (medido 2026-09-18).
Tomar el máximo inflaba el mercado al doble. → `consolidar_mercado.py` toma la **mediana** de
los espejos, salvo que el espejo alto sea también el más viejo por más de 7 días (`createdAt`):
ahí la diferencia es historia acumulada, no error, y se toma el alto (tablero LED de impor house:
1.981 en DROPI creado en 2025-11, legítimo). Por eso **al guardar la respuesta de la búsqueda
se conserva `createdAt`**; sin ese campo el script cae en la mediana y lo avisa.

## 4 · Los 3 criterios del catálogo público y las etapas

El núcleo del método de Juan (videos yTWqmR46vPE, hYpcanJ12fU, y-OWDawyb2c, repetido en 5
más). Un producto de catálogo público se testea si cumple los tres:

1. **Se vende, sin estar escalado:** ventas totales **consolidadas** (trampas 1-3) desde **100**
   hasta el techo de VALIDACIÓN del país. Porqué del techo: un proveedor trae 100 a 2.000
   unidades de un producto nuevo; pasar de ahí = ya reabasteció = ya tiene varios dropshippers.
   Porqué del piso: "si alguien convenció a 100 personas, se puede convencer a 1.000".
2. **Pocos proveedores activos:** Dropi reparte el catálogo al azar; un producto con 100
   proveedores le sale a todo el mundo en el feed, uno con 1 casi a nadie. Topes: CO ≤5,
   MX ≤4, GT y PE ≤2 (los demás: tope de CO, declarado). **Heredados, SIN VERIFICAR** (ver
   `calibracion.md`): DropKiller no da el número de proveedores por fecha y no se pudo medir.
3. **Pocos anunciantes EN EL CANAL que vas a usar.** El cofundador cuenta con la Ad Library de
   Meta ("100% exacta") y usa AdsKiller solo para sacar anuncios. Aquí se mide PRIMERO con
   `semantic_search_ads` por imagen + descripción y `competencia.py canal` (paso 6 del embudo),
   porque la Ad Library por palabra clave falla con palabras ambiguas (medido: "nivel láser" →
   850 anuncios de depilación) y no separa quién ya abandonó; la Ad Library queda para
   CONFIRMAR por nombre de página. Se cuentan **por canal** (`--canal landing|whatsapp`): si los
   5 anunciantes van a WhatsApp, la landing está libre, y al revés (Juan y Armando Soto: "son
   públicos distintos"). Topes del menú (pregunta 8): A 0 a 3 (por defecto) · B hasta 6 · C no
   importa. Juan usa "3 = pocos, 10 = ya no": heredado, sin medir.

**Etapas por ventas totales consolidadas** (Juan, hYpcanJ12fU: "las que yo he podido deducir";
son heurística de practicante, no medida publicada — así se declaran):

| País | NUEVO | VALIDACIÓN | ESCALADO | SATURACIÓN | QUEMADO |
|---|---|---|---|---|---|
| Colombia | <100 | 100 – 3.000 | 3.000 – 8.000 | 8.000 – 15.000 | >15.000 |
| Ecuador | <90 | 90 – 2.000 | 2.000 – 6.000 | 6.000 – 10.000 | >10.000 |
| Guatemala | <80 | 80 – 1.000 | 1.000 – 5.000 | 5.000 – 8.000 | >8.000 |

Los tramos que Juan no define (CO 5.000–8.000, EC 4.500–6.000, GT 3.000–5.000) quedan en
ESCALADO. Otros países: tabla de Colombia **declarada** como supuesto. Para catálogo público se
testea VALIDACIÓN; NUEVO solo si el usuario lo pide en el menú y sale marcado "sin validar" (menos
de 100 ventas no cumple el criterio 1); ESCALADO solo si se va a IMPORTAR para competir por precio.

**Ritmo (medido en parte, ver `references/calibracion.md`):** el preset "sin escalar" del canal
oficial pedía 7 días entre 10 y ~120. El backtest v2 (112 productos en VALIDACIÓN, muestra que no
depende del resultado) sostiene el **piso de 10** con fuerza (bajo 10 murió el 92%) y da un
**indicio** para 31 (de 31 para arriba murió 1 de 15; p = 0,06). **Por defecto: 7 días ≥ 31,
sin techo** (prudente, no ley). El techo de 120 no tiene evidencia ni a favor ni en contra: más
de 120 lleva el aviso CALIENTE y la competencia se mide sí o sí. "Frenando" (aceleración < 0,7)
es AVISO, no filtro: no se distinguió del nivel bajo. Fuera de Colombia nada está medido.

## 5 · Las 7 rutas de caza

Cada una sale de un video concreto. El menú de arranque (`references/menu-arranque.md`) deja
elegir una o todas.

| # | Ruta | Cómo | Fuente |
|---|---|---|---|
| R1 | **Validados sin escalar** en tu país | `search_products`: país + plataforma + `minTotalSold` 100 (el techo lo pone `consolidar_mercado.py`, trampa 9) + `minSold7d` 31 (calibrado, `calibracion.md`) + stock ≥80 | curso gEQbjW7-2HY, preset oficial T5-qgCBJIg8, backtest 2026-09-18 |
| R2 | **Recién creados que ya venden** | `search_products`: creado en los últimos 7 / 30 días + 7d ≥20 (+ 30d ≥60) + stock ≥80. Detecta temporada | oficial 0KI5rQLRUxs, AjH9S12x0Pg |
| R3 | **Nuevos sin competencia** | creado en los últimos 3 meses + ventas totales 500–2.000: alguien lo vende constante y nadie lo escaló | oficial 9GIZbo29IoM |
| R4 | **Del país grande al chico** | ventas totales 1.000–5.000 en Colombia → buscar por imagen en EC/GT/PE: lo probado allá, virgen acá | oficial WavYapQUCZY, vMhNOSS8Zig |
| R5 | **Tiendas de otro país → tu catálogo** | anuncios validados/evergreen en otros países (`search_ads`/`semantic_search_ads` con `countryCode` ≠ el tuyo) → producto → buscar por imagen en tu país → 1-2 proveedores | vMhNOSS8Zig, uYAcP56lXdA, 1tWYF-02D9o |
| R6 | **TikTok Shop EE.UU. → LatAm** | `search_tiktok_products` por ventas → buscar similar en tu país. Adelanto medido por Juan: ~5 meses (sebo Evil Goods, probiótico vaginal). Si NO existe en Dropi = oportunidad de MAQUILA (marca propia), no de catálogo | YYcl5aQyjRY, gEQbjW7-2HY |

| R7 | **Problema validado afuera → libre aquí** | `ads_library_search` con el problema en INGLÉS en US/CA/GB y en ESPAÑOL en tu país (limit 1 basta para el total; guarda una muestra de 50 del tuyo) → `scripts/brecha_mercados.py`: compara el múltiplo observado contra el que corresponde por tamaño de mercado y depura el conteo local por moneda. Sale un PROBLEMA, no un producto: después hay que encontrar qué producto lo resuelve y pasarlo por el embudo entero | método que circula en video (2026-09); corregido y medido aquí el 2026-09-19 |

**Sobre R7, lo medido el 2026-09-19** (y por qué la regla que circula NO se copia tal cual): el
método dice "si afuera hay 14.000 anuncios y aquí 8, es un hueco servido". Tres correcciones,
todas medidas con la Ad Library:
- **Tamaño.** US+CA+GB son ~9 veces la población de Colombia: un múltiplo de 8 es lo normal.
  Corrector de postura 2.637 contra 337 = 7,8× → SIN BRECHA. Fascitis plantar 25× y ronquidos
  26× → brecha de verdad.
- **El conteo local no es competencia local.** En 50 de los 671 anuncios de "ronquidos" en
  Colombia, 25 cobran en pesos; 15 en dong, 9 en dólares y 1 en reales (trampa 6). La mitad es
  ruido: el script lo depura con la muestra.
- **Un anuncio no es un vendedor de producto.** En esa misma muestra hay ~7 tiendas y 2 clínicas.
- **Pocos anuncios aquí también puede ser que no se venda.** El backtest midió que lo que casi no
  se mueve muere el 92% de las veces: la demanda en el país se comprueba con DropKiller, no se
  deduce del hueco. Y estos problemas suelen ser de SALUD: aplican las reglas 5, 6 y 8.

**Si el usuario da un nicho:** filtro `categories` en R1-R4 y `semantic_search_products` con la
descripción del nicho. **Si da un producto o una foto:** saltar a la consolidación (paso 3 del
embudo) directamente.

## 6 · El embudo de una corrida

Ordenado de lo barato a lo caro: cada paso descarta antes de gastar la llamada siguiente.

1. **Candidatos** (1-3 llamadas por ruta): pedir el triple de lo que se va a entregar.
2. **Ventas reales** (1 llamada por candidato: `get_product_history` desde hace 30 días, o el
   `history30d` si vino de la búsqueda semántica) → `ventas_reales.py`. Fuera FANTASMA.
   DUDOSO pasa solo si no hay suficientes REAL, marcado.
3. **Mercado consolidado** (1-2 llamadas: `semantic_search_products` con `imageUrl` del
   candidato y `countryCode`; si falla o trae poco, `search_products` con `q` = palabra clave
   corta del nombre) → guardar la respuesta en un archivo CON `createdAt` → `consolidar_mercado.py --pais XX
   --incluir "<regex del nombre>" [--etapa …] [--max-proveedores N]` con lo que se eligió en el
   menú (preguntas 5 y 8). Fuera lo que no pase los criterios 1 y 2. Los avisos del script
   (espejos que no cuadran, datos que faltaron) van a la tarjeta del producto, no se callan.
4. **Plata** (local): `viabilidad_cod.py --costo <salePrice del proveedor>` → PVP mínimo. Si
   ese PVP queda por encima de lo que cobra la competencia visible, se marca (Juan: "si lo
   venden más barato de lo que tu costeo aguanta, pasa al siguiente").
5. **Compuertas de riesgo** (local, ver sección 7): marca ajena, salud y claims, alérgenos.
6. **Anunciantes por canal, cementerio y precio** (1 llamada `semantic_search_ads` con
   `imageUrl` del producto + `query` = descripción corta + `countryCode`; guardar en
   `anuncios.json` → `scripts/competencia.py canal` y `precios`). Medido 2026-09-18: la imagen
   SOLA trajo 0 de 13 anuncios del producto (nivel láser → masajeadores y trampas); imagen +
   descripción trajo 6 de 6 y 8 de 8. El CEMENTERIO (anunciantes que dejaron de verse hace más de
   7 días) es señal propia: en la caja montessori 4 de 5 lo soltaron entre julio y agosto. Los
   precios salen de `/products/<handle>.json` de las landings Shopify (7 de 7 legibles, gratis):
   nivel láser, competencia a $84.900 contra un mínimo de $85.641 = NO CIERRA; montessori,
   $149.900 a $169.900 contra $138.662 = CIERRA. Complemento: Meta `ads_library_search`
   (2-3 keywords del producto) para confirmar por nombre de página; criterio 3.
   Para sacar el `imageUrl` de la ficha: `search_products` con el nombre corto falló en 5 de 6
   productos (medido 2026-09-18); funciona con `providerId` + una palabra clave, o con el
   `externalId` a la vista en la respuesta. `competencia.py` une anunciantes por NOMBRE o
   DOMINIO (una tienda con dos nombres de página es una), respeta `--incluir` también en
   `precios` y saca de la comparación los packs y combos (un pack de 2 no se compara con el
   mínimo de 1). Con un solo precio visto lo dice: referencia débil, no veredicto. En la corrida diaria se hace ligero (2-3 keywords) y se declara; el
   barrido de 8 keywords es para el producto que se elige testear. Se cuentan **páginas
   distintas**, no anuncios (una página corre 5 a 12 variantes del mismo), y solo las que
   anuncian ESE producto: en la corrida del 18-sep "nivel láser" trajo 850 anuncios de
   depilación y "amplificador de pantalla" trajo carros usados. Leer por título es aproximado
   y no separa landing de WhatsApp: se declara así en la lista.
7. **Creativos y ángulo** (1 llamada `semantic_search_ads` con la imagen, `broadcastDuration`
   validated/evergreen, países ≠ el tuyo): el ángulo que ya funciona afuera y nadie usa aquí.
   Duplicados altos y días activos ≥30 = creativo que imprime plata (Juan, koulVsm2sM8).
8. **Filtros del menú** (6 ritmo de 7 días, 8 proveedores y anunciantes, 10 precio y stock): el
   que rompe uno no entra a la lista; va a "Casi" con el filtro que rompió y por cuánto.
9. **Ranking** de lo que quedó, en este orden y sin saltárselo (es el que aplica
   `correr_lote.py`, `clave_ranking`): estado (LISTA antes que CASI) → proveedores activos (menos
   es mejor) → anunciantes activos en el canal (menos es mejor) → ventas de 7 días (más es
   mejor: el nivel es lo que mejor predijo lo vendido después, 0,74). Los reabastecimientos van
   a la tarjeta como dato: con N = 2 no se pudieron medir. Si se altera el orden por un motivo, se escribe el motivo
   en la tarjeta.

## 7 · Lo que se rechaza aunque lo enseñen los videos

- **Testimonios o avales inventados.** Juan (Kj_-5bTr-6I) sugiere "crear supuestos testimonios
  reales con ChatGPT" y pone de ejemplo un "testimonio de supuesto doctor". En Golden: prohibido.
- **Bots que se hacen pasar por especialista** y promesas de cura ("un especialista que te cure
  el hormigueo", y-OWDawyb2c). Prohibido.
- **Marcas de terceros en el catálogo público** (tenis Adidas, Casio, AirPods, Minecraft):
  riesgo de propiedad intelectual y de cierre de cuenta publicitaria. Se descartan de la lista
  diaria y se mencionan aparte como descartados.
- **Salud, suplementos, glucosa/diabetes, adelgazantes:** no se descartan solos, pero entran con
  tres banderas obligatorias: (a) categoría que Meta restringe, (b) la ficha técnica sale de la
  **ETIQUETA del producto que se despacha**, jamás de la descripción del proveedor ni de la de
  un competidor, (c) toda advertencia de **alérgeno** del envase se publica. En la lista diaria:
  4 de los 8 primeros "ganadores" de Colombia eran suplementos.
- **Copiar el embudo de tu MISMO país.** Solo se trae lo de otros países (Juan, 5 videos).
- **Descargar sin metadata "porque Meta penaliza la repetida":** afirmación de Juan sin fuente.
  No es criterio de esta skill.

## 8 · Si el conector falla

- Sin conector DropKiller (no aparece `find_winning_products`): decirlo en una línea, correr el
  modo VALIDAR de la skill (Ad Library + AliExpress + Amazon) y ofrecer la extensión gratuita
  de DropKiller en Chrome para ventas de 7 días dentro de Dropi.
- Error de plan ("requiere Advance"): decirlo; R1-R4 no se pueden hacer sin Productos.
- Si una ruta devuelve 0: probar la misma ruta con los topes del país más grande (CO) antes de
  decir "no hay". Un cero se prueba, no se cree.
