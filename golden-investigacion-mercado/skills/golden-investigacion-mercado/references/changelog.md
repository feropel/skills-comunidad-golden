# Changelog — GOLDEN INVESTIGACIÓN DE MERCADO

## Índice (orden cronológico DESCENDENTE — más reciente arriba)
G5.21.1 · G5.21 · G5.20 · G5.19 · G5.18 · G5.17 · G5.16 · G5.15 · G5.14 · G5.13 · G5.12 · G5.11 · G5.10 · G5.9 · G5.8.1 · G5.8 · G5.7 · G5.6 · G5.5 · G5.4 · G5.3 · G5.2 · G5.1 · G5.0 · G4.3
· G4.2.1 · G4.2 · G4.1 · G4.0 · G3.10 · G3.9 · G3.8 · G3.7 · G3.6 · G3.5 · G3.4 · G3.3 · G3.2 · G3.1
· G3.0 · G2.5 · G2.4 · G2.3 · G2.2 · G2.1 · G2.0 · G1.0

## G5.21.1 — 2026-09-24 — El candado de scraping deja de descartar páginas buenas por una tilde (CENTRO DE MANDO)

**El fallo, medido por el chat de Colágeno el 23-sep:** `candado_scraping.py`, CHECK 4, solo hacía
`.lower()`. `--pedi "PEPTEA serum"` daba **DESCARTAR** sobre la página correcta "PEPTÉA Sérum", y
`--pedi "colageno glow"` solo casaba "glow". Es la clase `coterra` contra `côterra`, fallando hacia el
ROJO: tiraba datos buenos.

**El arreglo, hecho para no provocar el fallo simétrico** (en otra skill, plegar tildes arregló 1
nombre y rompió 20 sanos): `_plegar()` quita tildes y pasa a minúsculas **solo dentro de la
comparación**. No toca `textos`, el JSON ni nada que salga del candado. Riesgo declarado en el propio
script: plegar la ñ hace que "año" case con "ano", lo que en una pregunta de pertinencia puede dar un
PASA falso en un caso raro.

**De paso salió un segundo defecto que nadie había visto:** con texto en forma NFD (la ñ o la é como
letra más tilde suelta, que es como llegan muchos textos pegados en macOS), `\w+` partía la palabra en
la tilde: "PEPTÉA" daba la clave `pepte`, que casaba por accidente. `_plegar` normaliza antes de
partir, así que la clave vuelve a ser `peptea`.

**Verificación:**
- Línea base: candado viejo contra nuevo sobre **14 respuestas reales guardadas × 5 pedidos: 0 de 70
  veredictos cambian.** El arreglo no mueve nada que no tenga tilde.
- Banco de 5 casos (tilde en el pedido, tilde en la página, las dos palabras, y dos controles
  negativos con otro producto): nuevo 5 de 5. El viejo falla 2 de 5.
- La prueba vive dentro del script: `candado_scraping.py --autoprueba`. Un mutante con el
  comportamiento viejo la hace fallar (3 de 5, exit 1).

**Lo que NO entra en esta versión:** los 11 fallos del verificador sobre G5.21 y las decisiones de FER
del 22 y 23-sep (5 ángulos, 12 plataformas, casilla en PRODUCTO.json, Dropkiller, inventario de tres
fuentes, excepción PDF). Siguen en `STACK-GOLDEN/VERIFICACION-G5.21-HALLAZGOS-22SEP2026.md` para la
pasada única, que espera a que FER cierre el método desde el chat de Colágeno.

**Orden del archivo:** la entrada de G5.21 estaba al final, fuera del orden descendente que declara el
índice, y el índice no la nombraba. Se movió aquí debajo sin tocar su texto.

## G5.21 — 2026-09-22 — Ampliación de FER: los ÁNGULOS (horneada por el CENTRO DE MANDO)

**Quién:** el Centro de Mando. Esta skill no tiene fábrica declarada en
`STACK-GOLDEN/REGISTRO-FABRICAS.md`, así que por ley el dueño es el CdM.

**Por qué:** FER dio la orden el 22-sep-2026 (llegó por el chat 📦 COLAGENO, que pidió expresamente
propagarla a esta skill "para TODOS los productos, no solo el mío"). La orden amplía el mandato
anterior —*"no vendemos productos, solucionamos problemas"*— en cuatro puntos medibles.

**Qué cambió:**
1. **SKILL.md** — nueva **FASE 3.5 · LOS ÁNGULOS**, entre la Fase 3 y la Fase 2. De 3 a 10 ángulos,
   2 creativos por ángulo, investigación global, criterio de LIKES, comparación de motores.
   Candado: menos de 3 ángulos sostenidos con fuente = la fase no cierra.
2. **references/03-mercado-en-vivo.md** — nueva **§3.6** con el detalle operativo: las dos vetas
   (replicar lo que paga en otro país / tomar el hueco), el filtro de likes con `yt-dlp`, la lista
   completa de fuentes (entran **Alibaba** y **Temu**, que faltaban) y la ficha de entrega de cada
   ángulo, incluida la columna de qué debe recoger el prompt del bot.
3. **Sello** GIM_VERSION → G5.21.

**Lo que NO cambió:** las 13 reglas de oro, el esquema de `PRODUCTO.json`, los scripts y el
blindaje (`scripts/fuentes_baseline.json` sigue sin flag, a propósito).

**Citas que sostienen el cambio** (de FER, mismo día):
- *"Un solo ángulo no es conveniente porque a lo mejor funciona y fue coincidencia."*
- *"La investigación de mercado tiene que abarcar todo el mercado, no solo Colombia."*
- *"Leer los comentarios que deja la gente… y mirar si tienen likes."*
- *"No te preocupes por las imágenes, si me toca comprar más crédito lo compro."*
- *"No importa lo que te demores, no importa los recursos que necesites."*

**Memoria canónica:** `feedback_investigacion_antes_de_generar_creativos.md`.

## G5.20 — 2026-09-20 — Auditoría golden-skill-auditor: blindaje PARCIAL reparado, referencias rotas reportadas ya no existen

Corrida de `golden-skill-auditor` con la orden de FER (Fase 0 obligatoria de esa skill). Dos verificaciones:

**(1) Blindaje.** `inventario.sh` midió 20 de 21 nodos con `chflags uchg` — el nodo suelto era
`scripts/fuentes_baseline.json` (editado el 2026-09-08 sin re-blindar). Reparado: `chflags -R uchg`
sobre el árbol completo, ahora 21 de 21.

**(2) Las tres referencias rotas del encargo** (`references/estructura-campanas.md`,
`references/estructura-reporte.md`, `references/copies-cumplimiento.md`, marcadas antes como "no existe
y no dice de quien es"). Verificado con `grep -rn` sobre TODO el árbol de esta skill (SKILL.md, los 11
references, los 6 scripts): **cero coincidencias de los tres nombres**, en ningún archivo, ni siquiera en
el changelog. Estas rutas no fueron citadas por ningún G5.x ni por ningún G2.x-G4.x visible hoy: el
pipeline vigente usa `03-mercado-en-vivo.md`, `producto-json.md`, `dossier-psicologico.md`,
`compliance-por-vertical.md` — ninguno se llamó nunca así. Conclusión: el hallazgo del validador
correspondía a una corrida sobre una versión anterior a la rearquitectura G2.2 (2026-06-25), que ya
eliminó y renombró varios references (`04-meta-ads.md`, `05-tiktok-ads.md`, `google-ads.md`,
`06-creativos-copy-prompts.md`) — la cita viva ya no está en el disco desde entonces. `inventario.sh` y
`validar_arsenal.py` corridos de nuevo hoy confirman 0 rotas, 0 huérfanos, 0 dudosos.

## G5.19 — 2026-09-08 — La trampa GEMELA: dos `N+` no se comparan (la creó la cura de G5.17)

Detectado por el Centro de Mando al revisar la Fase 3 **antes de que se usara**, y es el caso más fino
de la serie: **el arreglo de una trampa de conteo fabricó otra un piso más arriba.**

G5.17 curó que "40" no era un conteo, obligando a marcar los conteos como cerrados o `N+ (abierto)`.
Pero **dos competidores marcados `100+` pueden ser 101 y 4.000**, y leerlos como parejos es exactamente
el error de los cinco cuarentas — con la misma consecuencia, porque ese número alimenta la saturación
del nicho, que es uno de los 5 datos de viabilidad.

**La regla, ahora en los tres sitios donde alguien la puede leer:** un conteo abierto autoriza a decir
**"al menos N"** y nada más. **Nunca ordena, nunca rankea, nunca mide saturación, nunca entra en un "X
pauta más que Y".** Si una decisión de lanzar o matar necesita comparar dos competidores: **se cierran
los dos conteos, o no se comparan.** Un `N+` comparado vale menos que no tener el dato, porque parece
que lo hay. Escrito en `03-mercado-en-vivo.md` (junto a la tabla de países, con el aviso de que una
columna con `N+` no se ordena), en las reglas de coherencia de `producto-json.md`, y **en el propio
script**, que ahora lo dice en pantalla en vez de dejarlo en la prosa.

**Y con banco que muerde: `scripts/banco_google_transparency.py`.** La regla no se queda en un aviso
escrito — se prueba. Tres casos, en los dos sentidos: (1) servidor que siempre llena la página → dos
países abiertos → **debe** avisar; (2) servidor con 7 anuncios → la página viene incompleta → cierra →
**no debe** avisar (falso positivo); (3) un solo país abierto → marca el `N+` pero **no** grita sobre
comparaciones que nadie puede hacer. **3 de 3.** Y probado contra sabotaje: desactivando el guarda, el
banco falla con `exit 1` y nombra el caso — un banco que no muerde ante el sabotaje de la pieza que
vigila no prueba nada (el archivo se restauró y se verificó byte a byte).

**Lo que esta ronda enseña sobre corregir:** una corrección mueve un criterio, y el error simétrico
aparece del otro lado. La cura de "no confundas el tope con un conteo" invita a usar `N+` como si fuera
un número comparable. Por eso una corrección se cierra **midiendo los dos sentidos**, no solo el que
falló.

**Sigue PARCIAL, sin cambios:** el script no está verificado de punta a punta contra la red — Google
mantiene el 302 por auto-bloqueo. Pendiente añadido por el CdM para cuando ceda: **medir el tope máximo
que acepta el endpoint.** Si corta en 100, cualquier anunciante grande saldrá siempre `100+` y el
conteo cerrado solo existirá para los pequeños — eso cambia cómo se lee la saturación y hay que saberlo
antes de que alguien decida con ese número.

## G5.18 — 2026-09-08 — FASE 3: el mercado EN VIVO, y los huecos como entregable

Encargo de FER, literal: *"todo es todo, hasta lo que no se están sembrando"*. La skill sabía qué ES el
producto (Fase -1) y qué SIENTE el cliente (Fase 1), pero no **cómo se está vendiendo ahora mismo**. Se
cierran los cuatro huecos que la auditoría del 06-sep había medido y dejado abiertos.

**Nueva `references/03-mercado-en-vivo.md`** con cuatro bloques y una salida:

**(a) Mapa de mercados.** La investigación dejaba de ser de un solo país. La lista no se arma a ciegas:
**origen** (donde se fabrica y están las reseñas con foto real), **mercado maduro** (EEUU y España: sus
ángulos ya pasaron por selección natural), **vecinos COD** (donde el hallazgo se copia mañana) y
**destino**. Una fila por país con vendedores, precio en moneda local **y en USD** —sin eso dos países
no se comparan—, oferta, modelo de pago, anuncios activos y antigüedad. Lo que la tabla deja decidido:
dónde está saturado, el delta de precio real contra el mundo, y **qué ángulo viaja entre países**, que
es la diferencia entre estructura y casualidad cultural.

**(b) Matriz de oferta y combos.** El hueco más caro que tenía la skill: *casi nadie compite en
producto, todos compiten en oferta*. Competidor por competidor: 1, 2 y 3 unidades con el precio por
escalón, regalo, envío, garantía, ancla, urgencia y modelo de pago. Salida accionable, no descriptiva:
el escalón que todos ignoran, el punto de precio vacío y la garantía que nadie da.

**(c) Autopsia de página.** Sobre las 2-3 páginas de los que **más llevan anunciando**, que es el
filtro honesto de "a quién copiar". Se anota el ORDEN de las secciones, porque el orden es la
estrategia, más el stack técnico por `rawHtml` + `grep` (tema, apps de upsell, píxeles) — la vía más
honesta que hay, porque no pasa por ningún extractor que pueda inventar.

**(d) Inventario de creativos.** Se capturaba el copy y se perdían **las piezas**. Ahora una fila por
creativo con formato, **días activo**, gancho de los 3 primeros segundos, qué muestra y texto en
pantalla, **ordenado por días activo**: la pieza vieja que sigue viva es la que paga. El video se
desarma con `golden-video-teardown`, no se resume de memoria.

**(e) §3.5 LOS HUECOS, que es para lo que existen los otros cuatro.** Ocho familias: dolores que nadie
nombra, públicos sin atacar, ángulos ausentes, escalones de precio vacíos, secciones de página y
formatos de creativo que nadie usa, países con demanda y sin oferta, objeciones sin responder, usos
secundarios. **Cada hueco lleva dos líneas: la evidencia de que está vacío Y por qué podría estarlo** —
a veces nadie lo hace porque no funciona, y decirlo vale tanto como el hueco. Un hueco sin la segunda
línea es una corazonada.

**Nuevo `scripts/google_ads_transparency.py`** — la receta de Google deja de ser prosa y pasa a ser
herramienta, precisamente porque la prosa ya falló una vez (G5.17). Barre `--paises CO,MX,CL`, y el
conteo **cierra** (la última página vino incompleta) o sale marcado **`N+ (ABIERTO)`**: la trampa de
leer el tope de página como conteo ya no se puede cometer. Extrae además **los días que lleva corriendo
cada pieza** desde las claves 6 y 7 de la respuesta, verificadas contra el reloj: primera vez
2026-09-01 02:52, última 2026-09-08 10:22 — 7,3 días, coherente con el momento de la medición.

**Tres cosas medidas mientras se construía, que van al manual:**
- **El offset NO pagina.** Repetir la llamada con offset 40 devuelve **los mismos 40 ids**. Por eso el
  conteo se cierra subiendo el TOPE. La respuesta trae un cursor en la clave "2" cuyo sitio en la
  petición **no se descubrió**: queda declarado como pendiente, no disimulado.
- **`--buscar` busca MARCAS y DOMINIOS, no productos.** "faja reductora" devuelve 0 y "temu" devuelve
  la lista. Se entra por el dominio del competidor. Sin esto, alguien concluiría "no hay anunciantes".
- **Rate limit real:** tras ~15 llamadas en pocos minutos Google responde **302** y deja de servir. El
  script pausa entre llamadas, lo detecta y **para**, en vez de insistir en bucle. Es el mismo patrón
  de auto-bloqueo que la suite de fuentes ya tenía documentado para AliExpress: sondear dispara las
  defensas que se están midiendo.

**Enganchado en todo el circuito**, que es lo que evita que una fase nueva quede huérfana: Fase 3 en el
flujo del `SKILL.md`, puente desde la puerta de la Fase 1, **sección 8.bis del documento maestro** y
bloque **`mercado_en_vivo`** en el expediente `PRODUCTO.json`, con sus reglas de coherencia:
`medido_el` obligatorio, `anuncios_activos` siempre acompañado de `conteo_cerrado`, y los precios de
esta fase rotulados como REFERENCIA — el precio de venta lo fija solo el dueño (REGLA 11).

**Sigue abierto:** las cuatro llaves que dependen de FER (sesión de TikTok Ads, app de Mercado Libre,
Ahrefs y SimilarWeb, y la decisión sobre el histórico de TikTok). Sin ellas, un estudio sale con tres
huecos declarados: TikTok en LatAm, Mercado Libre y el tráfico de los competidores.

## G5.17 — 2026-09-08 — La receta de Google traía una TRAMPA DE CONTEO, puesta por mí en G5.16

Salió de una pregunta de FER —"funcionó bien o queda algún arreglo"— que obligó a probar lo que en
G5.16 se había dejado como **razonamiento y no como medida**: "el país es un número, así que barre el
mundo" era una deducción sobre una sola corrida con un solo país.

**Lo que apareció al probar cinco países.** Colombia, México, Argentina, España y Chile devolvieron
**40, 40, 40, 40 y 40**. Ese 40 no es un conteo: es el `"2":40` que pide la propia llamada. Puesto en
100, devuelve 100. **La redacción de G5.16 decía "40 anuncios activos de temu.com en Colombia" y eso
era falso.** El daño no es cosmético: de ese número sale la lectura de **saturación del nicho**, que es
uno de los 5 datos de viabilidad — o sea, alimenta la decisión de lanzar o matar un producto. Un
competidor con 40 y otro con 40 se habrían leído como empatados cuando ninguno de los dos fue contado.
Corregido, con la forma de contar de verdad: **paginar subiendo el tope hasta que una página devuelva
menos que el límite pedido**.

**Lo que sí quedó probado, y era la duda de fondo:** el filtro por país **no se está ignorando**.
Colombia (2170) y España (2724) sobre el mismo dominio devolvieron **0 ids en común, 40 contra 40**. Si
el parámetro se ignorara, las dos listas serían idénticas. Esa comparación queda escrita como la
comprobación obligatoria antes de fiarse de cualquier filtro geográfico. Códigos verificados con
respuesta real: CO 2170 · MX 2484 · AR 2032 · CL 2152 · ES 2724.

**La lección, que es de la casa y ya tiene familia:** un número que llega redondo y repetido —cinco
países, cinco veces 40— casi nunca es un dato; es el límite de la herramienta mirándote de frente.
Y el que lo escribió fui yo, en la ronda anterior, midiendo de verdad **una** vez y generalizando a
partir de ahí. Medir una vez y extender es el mismo error que este manual corrige en todas partes.

## G5.16 — 2026-09-08 — Las TRES bibliotecas de anuncios, y una sonda que gritaba en falso

Turno dado por el Centro de Mando (esta skill no tiene fábrica declarada: la lleva el CdM). Origen:
auditoría contra el estándar de exhaustividad de FER — "que vaya a cada país y a cada biblioteca de
anuncios; si algo no se puede, se dice y se hace posible".

**(a) Google · Centro de Transparencia: de "ni se nombraba" a receta ejecutable, gratis.** La skill
solo conocía dos bibliotecas de anuncios. Se probó scrapear la web y devuelve la portada (los
resultados los pinta JavaScript). Se capturó el cuerpo real de su RPC envolviendo `window.fetch` y
`XMLHttpRequest.prototype.send` en la página, y se reprodujo por curl **sin llave, sin cookies**:
**40 anuncios activos de `temu.com` en Colombia en una sola petición.** El país es un NÚMERO
(Colombia = 2170), así que la misma llamada **barre país por país** — es la vía más barata al mapa
mundial que pide FER. Horneado en `scraping-firecrawl.md` §Bibliotecas de anuncios y en la Fase 1.7.
Vale por dos: **la técnica de capturar el `f.req` sirve para cualquier sitio que "no se pueda
scrapear"** — con el cuerpo inventado responde `400 BadRequestException`; con el capturado, los datos.

**(b) La Ad Library de TikTok es SOLO EUROPA — límite legal, no técnico.** Se leyó su selector de país
completo: los 27 de la UE más Reino Unido, Suiza, Noruega, Islandia, Liechtenstein y Turquía. **No
existen Colombia, México, LatAm ni Estados Unidos.** Por eso `region=CO` devuelve "Total de anuncios:
0". Antes de esto, ese cero se habría reportado como bloqueo o como "no hay competencia": las dos
lecturas son falsas y las dos dañan una decisión de lanzamiento. Regla nueva: **antes de dar por rota
una fuente que devuelve cero, mirar si el país está en su lista.** Para TikTok LatAm, Creative Center
con sesión iniciada (sin login se ve recortado; su API sin sesión responde `40101 no permission`).

**(c) La sonda de TikTok de `verificar_fuentes.py` daba FALSO POSITIVO.** Reportaba "no genero
.info.json (la extraccion se rompio)" sobre una herramienta sana. Medido: TikTok resuelve un reto JS
y **falla de forma intermitente** — en seis corridas seguidas del mismo video, dos fallaron y cuatro
devolvieron 54.000 vistas y 1.118 likes. La sonda hacía **un solo intento** y concluía rotura. Ahora
reintenta 3 veces y **reporta la intermitencia en vez de esconderla**. Es el mismo daño que la suite
existe para evitar: un detector que grita en falso se termina ignorando, y ahí muere en silencio.

**(d) Amazon: la alarma era real y la vía NO estaba rota.** La suite marcó CAMBIO (de 1.716.438 b a
~173.000-245.000 b por HTTP plano, y desapareció `anti-csrftoken`). Re-verificado con la herramienta
real el mismo día: **48 tarjetas, 30 con contador de compras, 44 con precio, total 145 resultados**.
Cambió lo que Amazon le sirve a un curl desnudo, no lo que ve un navegador. Caso de manual de por qué
el veredicto es CAMBIO / IGUAL y nunca FUNCIONA / NO FUNCIONA. Matriz actualizada con la fecha.

**Lección de proceso, y esta duele:** el parte que arrancó esta ronda reportaba el crash de
`verificar_fuentes.py` **como si siguiera abierto**. Estaba medido de verdad, pero sobre **G5.14**, y
`golden-skill-auditor` ya lo había arreglado en **G5.15** ese mismo día. Un hallazgo verdadero
envejece en horas cuando el arsenal se repara solo: **antes de transmitir un fallo, se re-mide contra
el estado vivo, no contra la libreta.** Lo cazó el Centro de Mando corriendo el script.

**Sigue abierto** (reparto del CdM, no cabe en esta ronda): barrido multipaís como fase propia, matriz
de combos (1/2/3 unidades con precio, regalo, envío y garantía), autopsia de landing y product page
del competidor, e inventario de las imágenes y videos de los anuncios. Y cuatro llaves que dependen de
FER: sesión de TikTok Ads, app de Mercado Libre, autorizar Ahrefs y SimilarWeb, y decidir si se paga
histórico de TikTok.

## G5.15 — 2026-09-06 — verificar_fuentes.py ya no crashea con fuentes no-UTF-8

Auditoría `golden-skill-auditor`. Al correr `python3 scripts/verificar_fuentes.py` en vivo (evidencia,
no lectura), el script murió con `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in
position 1: invalid start byte`. Causa: `huella()` llama `subprocess.run(["curl", ...],
capture_output=True, text=True, ...)` — `text=True` fuerza a Python a decodificar el stdout de curl
como UTF-8, y una de las 5 fuentes de la matriz devolvió contenido que no lo es (gzip sin
descomprimir o codificación distinta). El resultado: el chequeo MENSUAL completo tumbado por una
sola fuente, con traceback, en vez de marcar solo esa fila como `{"error": ...}` y seguir con las
demás — exactamente el fallo que este script existe para evitar (un dato caído en silencio).

Arreglo (`scripts/verificar_fuentes.py`, función `huella()`): se quita `text=True` de la llamada a
`subprocess.run` y se decodifica el stdout a mano con `.decode("utf-8", errors="replace")`. Verificado
re-corriendo el script completo contra las 5 fuentes de la matriz: ya no crashea, entrega el informe
final con las 4 recetas de scraping/navegador tal como antes.

No se tocó nada más: los dos avisos del inventario de `golden-skill-auditor` (blindaje "parcial" en
`scripts/fuentes_baseline.json` y un `¿` dentro de un comentario bash de `SKILL.md:151`) son
excepciones ya declaradas explícitamente en el propio `SKILL.md` — el primero porque el script
regraba ese archivo y blindarlo lo dejaría escribiendo en el vacío, el segundo porque vive dentro de
un comentario de código para quien lee el bloque `bash`, no en texto que la skill le entregue al
cliente.

## G5.14 — 2026-09-05 — El acta sale del cuerpo: 2.780 tokens que se pagaban en cada activación

Fila del Centro de Mando, medida y **confirmada por mí antes de actuar**: el `SKILL.md` tenía
**11.120 caracteres de comentario de sello — el 47% del archivo, ~2.780 tokens pagados en CADA
activación** para cargar un historial que nadie consulta mientras trabaja. Sobre el arsenal completo
eran 234.666 caracteres (22% del corpus de los SKILL.md).

**Nada se borró: se mudó**, y en este orden, que es el que evita perder texto:
1. Se comprobó que los hechos del sello YA estaban en este changelog (muestreo de cadenas exactas:
   `BLACK WALNUT`, `importlib`, `2560×1920`, `drawtext`, `homónimo`, `143 menciones`,
   `nano-hidroxiapatita`, `Toppik` — todas presentes).
2. **Se cazó la excepción**: el tope del `description` (`~1.536` caracteres) aparecía **0 veces** en
   el changelog. Era una **regla viva** escondida en un comentario, no un acta. Se convirtió en la
   **regla 14 de `reglas-de-oro.md`** (1024 valida, ~1536 trunca, 879 hoy, cómo medirla) y se releyó
   del disco para confirmar que llegó **antes** de tocar el `SKILL.md`.
3. Solo entonces se reemplazó el sello largo por uno de una línea que apunta aquí.

Lección de método, aplicable a cualquier skill: **un comentario puede contener una regla operativa
disfrazada de historia**. Mudar sellos a ciegas habría borrado el único sitio donde vivía el límite
que hace que esta skill dispare o no.

También de esta ronda, cerrado desde fuera por el Centro de Mando y verificado aquí: dos hermanas
(`golden-copywriting`, `golden-blindaje`) citaban ficheros míos con rutas a secas
(`references/01-investigacion-360.md`), no copiables desde otra carpeta. Ya están cualificadas a
`golden-investigacion-mercado/...` y **comprobadas en disco**. Corolario adoptado: **una ruta se
escribe completa desde la raíz del arsenal — copiable, no deducible.**

## G5.13 — 2026-09-05 — La ficha sale de la ETIQUETA: el alérgeno que nadie amplió

**El incidente (madrugada del 05-sep, suplemento COD).** Se publicó una ficha con **cinco
ingredientes falsos** y un **ALÉRGENO sin declarar — nuez negra —** durante horas. Causa: los
ingredientes se copiaron de la **página de un COMPETIDOR** que vendía otra formulación **con el
mismo nombre comercial**. La fuente correcta llevaba días dentro del material del cliente: impresa
en la etiqueta del frasco, legible **ampliando un fotograma de un video del proveedor**.

**Qué encontré al medirme contra el caso (grep, no impresión):** la skill tenía la compuerta de
identidad y la regla de "ficha vieja contaminada", pero **cero cobertura de esta clase concreta**:
0 hits de "mismo nombre comercial/homónimo", 0 de "alérgeno", 0 de "ampliar el envase", 0 de "el
error es tuyo". Cubría al *revendedor* y a la *ficha vieja*; no al **competidor homónimo**, y no
tenía **ningún** mecanismo para sacar el dato de una foto.

### Herramienta nueva: `scripts/etiqueta_desde_video.py`
Convierte la lección en un paso mecánico. Video del cliente → N fotogramas repartidos por la
duración → recorte opcional del panel → ampliado ×2–×8 con Lanczos → PNG que el modelo **abre con
Read** y transcribe. Declara lo que NO hace: no es OCR y **ampliar no inventa nitidez** (lo ilegible
se marca `[ILEGIBLE]` y se pide otra foto).

**Probado, no supuesto** — y la prueba encontró un bug que la lectura no vio: `importlib.util`
usado sin importar, que hacía reventar la comprobación de Pillow (`AttributeError`). Corregido y
re-corrido. Medido el 2026-09-05: de un video 640×480, **4 fotogramas a 2560×1920** (×4 real);
recorte + ×6 → 2262×552; y al abrir ese PNG **se leyó literal `CONTAINS: BLACK WALNUT (nuez
negra)`** — la cadena exacta del incidente. Muerde con archivo inexistente (`No existe`) y con
extensión no soportada. Dato de entorno hallado de paso: **el ffmpeg de este equipo no trae el
filtro `drawtext`** (hubo que generar la etiqueta de prueba con Pillow).

### Doctrina horneada
- **Regla 11** — la ficha técnica sale de la **etiqueta del producto que se despacha**, jamás de un
  competidor aunque venda lo mismo con el mismo nombre; un competidor solo sirve para precio,
  oferta y ángulo. **Todo alérgeno del envase se transcribe literal y se publica** (lo único de una
  ficha que puede causar daño físico). **Ampliar el envase es un paso**, no un extra. Y: **si el
  material del cliente contradice tu trabajo, la hipótesis por defecto es que el error es TUYO** —
  en el incidente, dos veces el proveedor tuvo razón y dos veces se asumió que se equivocaba él.
- **Regla 12** — **un CERO se prueba, no se cree**: "no hay reseñas/competidores/alérgenos" exige
  método, términos, fecha y cobertura, igual que un hallazgo.
- **Regla 13** — **un dato medido caduca**: fecha de medición al lado de cada cifra.
- **Expediente**: `alergenos`, `alergenos_verificados`, `fuente_etiqueta`. Lista vacía con
  `verificados:false` significa "no comprobado", **no** "no tiene", y bloquea publicar.
- **Documento maestro** §2 exige ingredientes de etiqueta + alérgenos literales.
- **Compliance**: bloque de alérgenos transversal a todo vertical ingerible o tópico.

Compuerta oficial `agentskills validate` (ruta absoluta): **exit 0**. SKILL.md creció solo 14
líneas — la doctrina vive en references y el acta aquí, porque el cuerpo se paga en cada activación.

## G5.12 — 2026-08-23 — Auditoría `golden-skill-auditor` (888 → 985): la skill se aplicó a sí misma lo que predica

Dos hallazgos CRÍTICOS, ambos del mismo tipo — **afirmaciones propias que nadie había verificado**,
que es justo el error que esta skill enseña a evitar:

**1. El candado de auto-verificación estaba desactivado por el propio blindaje.**
`scraping-firecrawl.md` declara textualmente que `scripts/fuentes_baseline.json` *"queda fuera del
blindaje a propósito: el script tiene que poder reescribirlo. Si se blinda, la suite deja de poder
actualizarse."* Estado real medido: tenía `uchg` (17 de 17 nodos) y la escritura fallaba. Cuando la
matriz caducara (60 días desde el 2026-08-02, faltaban 39), `verificar_fuentes.py --baseline` habría
muerto y la skill habría perdido su detector de cambio de fuentes sin que nadie se enterara.
Fix: el baseline queda fuera del blindaje y el ritual de re-blindaje lo respeta explícitamente.

**2. El índice del changelog prometía 3 versiones que no existían.** El índice listaba
G5.9 · G5.8.1 · G5.8, pero el cuerpo saltaba de G5.10 a G5.7 — y otra entrada citaba "Nota de
auditoría G5.9", una referencia a una sección inexistente. Las tres son versiones reales (su
contenido sobrevivía resumido en el sello `GIM_VERSION` del SKILL.md): la auditoría 943→1000, la
minería de YouTube completa con `yt-dlp` + `whisper-cpp`, y el afinado del modelo ya cacheado.
**Restauradas** desde ese contenido; índice y cuerpo ahora coinciden 1 a 1 (verificado por script).

Mejorables reparados: numeración de `reglas-de-oro.md` iba 9 → 10.5 → 10.6 → 10 (la regla 10
aparecía DESPUÉS de sus propias sub-reglas) y los puntos de la regla 9 iban 1,2,3,5,4 → reordenados ·
la lección Toppik ("los precios del estudio son REFERENCIA, no decisión") vivía solo en references y
ahora es la **REGLA 11 del SKILL.md**, que es lo único que siempre se lee · "Archivos de esta skill"
omitía los 2 scripts, incluido el candado que el propio cuerpo ordena correr → listados ·
`dossier-psicologico.md` capa 30 citaba "(Fase 4)", fase que no existe post-split → corregido ·
signo de apertura eliminado · **Estándar 9 instalado**: la skill declara su conexión con el Centro
de Mando.

Verificado EN VIVO durante la auditoría, no asumido: `candado_scraping.py` caza el modo 4 (captcha
con title poblado) y deja pasar el dato bueno; `yt-dlp` y `whisper-cli` responden a `which`.
Ningún conocimiento de campo se perdió — todo fue orden, trazabilidad y desbloqueo.

## G5.11 — 2026-08-23 — Auditoría adversarial encuentra el punto ciego del candado G5.10

FER pidió, antes de entregar la ronda de 5 estudios ya corregida en G5.10, una autoevaluación
adversarial con `golden-verificador` (solo ve el resultado final y el estándar, no cómo se
construyó). El verificador confirmó que el trabajo de G5.10 fue real (dossier 30/30 en los 5,
compliance INVIMA contrastado palabra por palabra contra la fuente oficial, precios de competidor
exactos al peso, minería de YouTube genuina) — pero encontró 3 fallas nuevas de sistema:

**1. El candado de la regla 9 (conteo de menciones) no detecta un "injerto de párrafo".** Un
párrafo completo de Magnesium Complex (9 líneas, incluida una frase citando el nombre del otro
producto) quedó pegado literalmente dentro del estudio de Resveratrol. Pasaba el candado porque el
conteo era 197 menciones propias contra 4 ajenas — un párrafo pegado no mueve ese número lo
suficiente para disparar la alarma. Fix: regla 9 punto 5 — verificación adicional obligatoria de
intersección de bloques de texto literal (&gt;60 caracteres) contra los otros estudios de la corrida,
con atención especial a las secciones de "condiciones"/"cobertura"/"handoff", que es donde vive la
plantilla reutilizada sin darse cuenta de a quién pertenece.

**2. `[PENDIENTE]` declarado sobre un insumo que ya estaba en la carpeta.** El estudio de Beevana
declaró faltante la foto de etiqueta del producto mientras esa foto ya estaba guardada en la carpeta
del proyecto — con datos que contradicen el costeo del propio documento (etiqueta real: 60 g; el
estudio costeó proveedor/margen/flete sobre 30 g) y un ítem de compliance no señalado (el envase
dice "ARTHRITIS"). Fix: regla 10.5 — `ls -la` de la carpeta del proyecto obligatorio antes de
escribir cualquier `[PENDIENTE]` por insumo faltante.

**3. Veredicto y resumen ejecutivo no se reconcilian con secciones nuevas que los contradicen.**
Beevana sección 11 concluye "el negocio NO es rentable a esa escala" y la sección 10 (veredicto)
sigue diciendo "margen amplio, lanzar con condiciones" — sin tocarse entre sí. Fix: regla 10.6 —
toda actualización que cambie un dato de viabilidad reescribe veredicto y resumen ejecutivo en el
mismo momento; y "N de N secciones completadas" se mide contra las 10 secciones del estándar
(`02-documento-maestro.md`), no contra lo que el documento efectivamente escribió (3 de 5 estudios
declaraban "9 de 9" o "10 de 10" cuando les faltaban Buyer Personas y/o Estrategia de Mensaje).

Reportado al Centro de Mando junto con G5.10. Ningún conocimiento de campo se perdió — solo se
añadieron los candados 9.5, 10.5 y 10.6 sobre lo que ya existía.

> Nota de auditoría G5.9: G4.2 y G4.2.1 (2026-07-29) vivían mal insertadas al final del archivo,
> después de G1.0 — rompían el orden cronológico descendente que respeta el resto del changelog.
> Reubicadas aquí, entre G4.3 (2026-07-30) y G4.1 (2026-07-27), que es donde su fecha las ubica.

## G5.10 — 2026-08-22 — Incidente real: contaminación cruzada entre agentes + falso negativo de herramienta

Corrida real de 5 estudios en paralelo (Magnesium Complex, Beevana, Turmeric Curcumin, Soft Serve
Serum, Resveratrol Complex — nombres genéricos, no hay dueño de marca en ninguno). FER auditó él
mismo los `.docx` entregados abriendo el XML y contando menciones por producto — y encontró que uno
de los cinco estaba mal, algo que ni la propia corrida ni el reporte del agente habían detectado.

**Incidente 1 — contaminación cruzada por carpeta de trabajo compartida.** Un agente reconstruyendo
el `.docx` de Soft Serve Serum Truly usó una carpeta de trabajo con nombre fijo (`unpacked/`) sobre
el scratchpad compartido de la sesión. Otro agente, corriendo en paralelo sobre Magnesium Complex,
usaba una carpeta con el mismo nombre. Se pisaron. El documento final en el Escritorio tenía el
título correcto ("Soft Serve Serum Truly") pero 143 menciones de magnesio/magnesium contra solo 12
de "truly" por dentro — el contenido real era casi todo de otro producto. El candado que ya existía
("el XML es válido? hay texto real?") **pasaba en verde** porque la corrupción no rompe el
formato del documento, solo mezcla el contenido de dos investigaciones distintas.
- Fix: **regla 9 nueva en `reglas-de-oro.md`** — toda carpeta de trabajo para editar/reconstruir un
  `.docx` debe llevar un sufijo único e impredecible por ejecución (PID, timestamp con milisegundos,
  o `mktemp -d`), nunca un nombre fijo. Y, más importante: **después de guardar**, contar menciones
  del producto correcto vs. cualquier otro producto que pueda estar corriendo en paralelo — si no
  hay un margen claro, no se declara terminado, se repite desde una carpeta limpia.

**Incidente 2 — falso negativo de herramienta.** Varios de los 5 agentes declararon `[PENDIENTE]`
la minería de comentarios de YouTube (`yt-dlp --write-comments`) y la transcripción local
(`whisper-cli`) con la frase "el entorno no tiene acceso a esas herramientas de scraping" — **sin
correr `which yt-dlp` ni `which whisper-cli`** para comprobarlo. Verificado después, en la máquina
real: ambas SÍ están instaladas (`yt-dlp` 2026.07.04 en `/opt/homebrew/bin/`, `whisper-cli` del
paquete `whisper-cpp` 1.9.1, con el modelo `ggml-small.bin` ya cacheado por `hyperframes`). El
"hueco de cobertura" reportado en los 5 estudios para este punto era una suposición del agente, no
una limitación real del entorno.
- Fix: **regla 10 nueva en `reglas-de-oro.md`** — prohibido escribir `[PENDIENTE]` por "herramienta
  no disponible" sin haber corrido el comando de verificación (`which <herramienta>`) y citado la
  salida real. Solo un fallo real, con evidencia, justifica el `[PENDIENTE]`.

**Reportado al Centro de Mando** por mandato explícito de FER ("esto no puede volver a pasar, avísale
al centro de mando"). Ningún conocimiento de campo se perdió — solo se añadieron los dos candados
(reglas 9 y 10) sobre lo que ya existía.

## G5.9 — 2026-08-21 — Auditoría golden-skill-auditor (943 → 1000)

Cinco hallazgos con evidencia, todos reparados en su momento:
- **`README-COMUNIDAD.md` era material intruso en la raíz** (la política de la casa deja en la raíz
  solo `SKILL.md` + `references/scripts/assets/agents`; ninguna otra skill golden- lo tenía suelto)
  → movido a `references/README-COMUNIDAD.md`, con su puntero en la lista de archivos.
- **`scraping-firecrawl.md` y `changelog.md` superaban las 300 líneas sin tabla de contenido**
  (regla de Estructura de la rúbrica) → índice agregado a ambos.
- **G4.2 y G4.2.1 (2026-07-29) estaban insertadas AL FINAL del archivo, después de G1.0** — rompían
  el orden cronológico descendente → reubicadas entre G4.3 y G4.1, que es donde su fecha las pone.
- **Se citaba el dominio real de un competidor** como caso de estudio, contra la propia política
  G3.2 de esta skill (changelog generalizado, sin nombres de terceros) → genericizado a "una tienda
  real de gotas dentales (Chile)"; la lección técnica quedó intacta.
- **description sin cláusula negativa explícita** ("no construye páginas, no pauta") → agregada.

Ningún conocimiento de campo se perdió: fue reorganización y limpieza.

## G5.8.1 — 2026-08-11 — El modelo de whisper ya estaba en el equipo (afinado desde la fábrica de golden360)

Dato de campo llegado por la red sináptica: seguir la receta de transcripción a ciegas
**re-descargaba ~500 MB para nada**, porque `hyperframes` ya deja el modelo en
`~/.cache/hyperframes/whisper/models/ggml-small.bin`. La receta del §1.6 de
`01-investigacion-360.md` ahora **mira primero si el modelo existe** y solo descarga si falta.
Edición mínima: ese archivo y el sello.

## G5.8 — 2026-08-11 — MINERÍA DE YOUTUBE COMPLETA: la locución también se mina

La sección 1.6 decía *"si hay MCP de transcripción de video disponible"* — en condicional — y por
eso **la locución de los videos no se minaba nunca**. Ahora es concreto y medido:
- **Comentarios** con `yt-dlp --write-comments`, **con su `like_count`**, en vez de depender de que
  Firecrawl alcanzara los primeros. El like es un **voto**: la queja más votada es la objeción más
  común del mercado, no la más ruidosa. *Medido: 25 comentarios con likes reales en una corrida.*
- **Locución** transcrita en **LOCAL** con `whisper-cpp` — gratis, sin llave y sin que el archivo
  salga del equipo. *Medido: 7,5 min de audio en 29 s.* Receta portable en el §1.6.
- Instrucción dura: **transcribir los 3–5 videos top**, porque el guion hablado es el argumento de
  venta que ya le funciona a alguien, y los subtítulos quemados no se leen del fotograma (van una
  palabra por cuadro).

Porqué del hueco, para que no se repita: la capacidad ya existía en `golden-video-editor` desde
antes y **nunca se propagó** a las skills que la necesitaban.

## G5.7 — 2026-08-07 — Cosecha del chat "ESTUDIO 360 DENTAL CAVITY HEALING (Chile)" (6 ítems)
Repartido por el Centro de Mando desde la bandeja (orden de FER: "sin omitir detalle"). Todo salió
de una corrida real de la skill sobre una tienda real de gotas dentales COD en Chile (dominio
omitido a propósito — no es información que aporte a la lección técnica):
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

## G4.2.1 — 2026-07-29 — Compuerta 2 ampliada: universo real de piezas + criterio de transformación
El universo son plantilla+descripción+GALERÍA+pósters (227 piezas, no 99) y el criterio es texto O
TRANSFORMACIÓN (un antes/después sin letras ES el claim). + cruce render vs producto físico.

## G4.2 — 2026-07-29 — Compuerta 2 incluye IMÁGENES
Los claims viven quemados en los pixels, no solo en el texto: hoja de contactos + revisión visual
obligatoria antes de cerrar la compuerta, y el gotcha del `\/` escapado en JSON de plantilla.
Origen: claims eliminados del texto que seguían publicados en banners (GoPure/Tag Recede/Organic
Bless) — la compuerta de texto solo no los cazaba.

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
