# Changelog — GOLDEN SHOPIFY

Registro de versiones de la skill. Cada vez que se absorbe una mejora de una página
real, se sube una versión aquí (ver el ritual de auto-mejora en SKILL.md).

## G4.20 — 2026-09-04 — El tema se declara ANTES de generar (y el candado deja de asumir Dawn)
FER compartio las skills al grupo VIP y varios **no usan Dawn**. Esta skill construye sobre el tema
de OTRA persona, asi que asumir familia es el fallo de instalacion mas caro: si encaja a medias
parece que funciona.
- **Que ya teniamos** (medido antes de tocar): `references/temas.md` ya decia *"preguntar SIEMPRE
  cual es"*, ya separaba las **2 familias** (clasica Dawn/Shrine/Sense, donde el `product.json` pega,
  y nueva Horizon/Pitch, donde NO pega y va por Custom Liquid) y ya tenia fallback generico, mas
  `horizon-bloques.md`. El conocimiento estaba.
- **Que faltaba, y es de ORDEN:** eso vivia en un archivo de referencia, **no en la compuerta de
  arranque**. El Paso 0 obligatorio solo exigia el cerebro de marca. Y el protocolo de tema vivo dice
  "verificar QUE tema es MAIN" **por API** — que un VIP con la skill en su propio Claude puede no
  tener. Sin API y sin compuerta, se cae en asumir Dawn.
- **Paso 0-A (compuerta):** el tema queda DECLARADO antes de escribir una linea. Y la primera via no
  es preguntar: es **MEDIRLO desde la URL publica**. `Shopify.theme.schema_name` da la **familia
  real** aunque el dueno haya renombrado el tema — `name` es solo el rotulo. Verificado en tienda
  real: rotulo "GOLDEN 3D · Dawn (atrib WhatsApp)" vs `schema_name` **"Dawn"** 15.5.0.
- 🔴 **El candado asumia la familia Dawn.** Sus 13 selectores son todos Dawn/Shrine; en Debut,
  Impulse, Prestige, Booster o Ella **no ocultaba nada**, y falla **en SILENCIO**: la pagina se ve
  perfecta y el cliente igual puede irse al home. Anadidos los selectores de esas familias **y una
  verificacion medida obligatoria** (`getComputedStyle(header).display === 'none'`), porque ninguna
  lista cubre todos los temas: lo que no se puede garantizar por lista, se mide en la tienda.

## G4.19 — 2026-09-03 — La doc no decia como correr los validadores (ocho versiones rota)
Salio de comprobar si mi documentacion ensenaba la trampa de la tuberia. No la ensenaba, pero al
mirar aparecio algo peor: **`auto-check.md` no traia NINGUN comando**. Decia "correr este script"
y a continuacion "(el codigo vive en scripts/autocheck.py)", sin decir como.
- **Causa medida:** en G4.10 el encabezado nuevo se inserto con un patron que decia
  "Auto-verificacion" mientras el archivo dice **"Auto-verificación" con tilde**. La ley del grep
  con tilde, esta vez dentro de mi propio horneado. El otro reemplazo del mismo comando (el bloque
  ```python) si caso, porque no llevaba tildes — asi que medio cambio entro y medio no.
- **Lo grave no es el fallo, es que no dio la cara:** un `re.sub` que no casa **no falla, no hace
  nada**. El comando termino con exito, el changelog de G4.10 dio por hecho que la doc explicaba el
  uso, y asi paso por **ocho versiones** — mientras esta misma skill se auditaba a fondo cada hora.
- **Regla nueva en 0-H:** tras editar, **verificar que el texto nuevo ESTA**, no que el comando
  salio sin error. Un cambio que no se aplico es indistinguible de uno aplicado si nadie mira.
- Encabezado ya puesto, con los cuatro comandos, el aviso de la tuberia y la regla de los dos casos.

## G4.18 — 2026-09-03 — Angulares en la description, y el validador que nadie corria
Fila del Centro de Mando, verificada aqui ejecutando antes de aceptarla: la `description` contenia
`product.<tema>.json` y **la spec de publicacion prohibe los angulares**. No era longitud: 1010
caracteres de 1024. El arreglo son dos caracteres → `product.tema.json`, y el disparador no pierde
nada.
- 🔴 **La causa de fondo vale mas que el arreglo:** esta skill revisaba con 29 checks el
  `product.json` que PRODUCE, y **no se revisaba a si misma como artefacto publicable** — aunque se
  publica al marketplace de la comunidad. El fallo lo caza el validador **oficial** que trae
  `skill-creator` (`scripts/quick_validate.py`), la fuente autoritativa de publicacion, y **ninguna
  de nuestras herramientas lo corria**. Un validador propio muy pulido no sustituye al de la
  plataforma que publica: valida lo que TU decidiste mirar, no lo que la plataforma exige.
- **La autoprueba ahora lo ejecuta sobre esta skill**, con la distincion de la refinacion 2:
  **BLOQUEA** si el validador existe y falla (el fallo esta en nuestro SKILL.md) y **AVISA** si no
  se encuentra (vive fuera de nuestro arbol y lo mantiene otro).
- **Nota de medicion propia:** al comprobar la fila lei el codigo de salida a traves de un `head` y
  me dio 0 — el mismo error que el CdM habia confesado horas antes con un `tail`. Repetido bien:
  salida **1**. Y con **control conocido** (`golden-pdf-check` → 0, "Skill is valid!"), que es la
  refinacion 4 de la ley funcionando el mismo dia que se escribio.

## G4.17b — 2026-09-02 — Un falso positivo destapo una clase: la funcion de "texto visible"
El check 27 (rayas) dio falso positivo en su primera corrida y el caso bueno lo cazo. La causa no
era el check: era **la funcion que decide que texto se PUBLICA**, que solo quitaba `{% comment %}`
y dejaba pasar dos cosas muy frecuentes aqui — `{%- comment -%}` (con guiones de control de
espacios, como escribe media skill) y los comentarios de JavaScript `/* ... */`.
- **Lo que marcaba:** los separadores decorativos que los componentes usan para orientar a quien
  EDITA el codigo (`/* ═══ EDITAR LAS RESEÑAS AQUI ═══ */`). Nunca se publican.
- **La usaban CUATRO checks**: DEMO visible, apertura ¿¡, rayas y lenguaje de tienda. Un solo
  arreglo (`solo_visible()`, que ahora quita comentarios Liquid con y sin guiones, JS/CSS y HTML)
  corrige los cuatro. **Buscar la CLASE, no el caso.**
- **Caso bueno nuevo**: un separador dentro de un comentario de codigo NO debe fallar.
- Nota de metodo: el caso bueno lo cazo porque mide sobre la plantilla real. Si lo hubiera probado
  solo contra el fragmento inyectado, el falso positivo entra a produccion sin ruido.

## G4.17 — 2026-09-02 — Las SEIS reglas duras, antes de repartir la fila
Coherencia elemental: el CdM va a repartir una fila preguntando a cada fabrica **"tu validador
comprueba las seis reglas duras de la casa?"** — propuesta que salio de aqui — y esta skill
comprobaba **dos**. No se reparte una vara que uno mismo no pasa.
- **Check 27 · rayas separadoras** (3+ seguidas o `<hr>`). Caso bueno: **una raya em suelta en prosa
  es correcta** ("natural — sin quimicos") y marcarla empujaria a escribir peor.
- **Check 28 · lenguaje de TIENDA** (`nuestra/la/esta/mi tienda`). Caso bueno: **"tiendas fisicas"
  sin posesivo no es el vicio** que la regla persigue — es un dato de distribucion.
- **Check 29 · credenciales en el entregable** (sk-, ghp_, shpat_, Bearer, AIza). La skill se comparte
  con la comunidad y el JSON se pega en tiendas de clientes: un token filtrado **viaja con la
  plantilla**. Se buscan formas inequivocas de credencial y **NO correos**: el correo de contacto de
  una marca es legitimo en una ficha. Caso bueno: **una clase CSS larga no es un token**.
- Los tres **FALLAN**, ninguno avisa. Cada uno con su caso en las dos direcciones, que en estos era
  el riesgo entero: los tres tienen una version legitima muy parecida a la prohibida.
- **6 de 6 reglas duras comprobadas** · 29 checks · **29/29 pruebas**.

## G4.16 — 2026-09-02 — El validador no comprobaba NINGUNA regla dura de FER
FER amplio la ley a **cada skill, cada agente y cada proceso**, sin la frontera que le habiamos
puesto. Al aplicarla aqui salio un hueco peor que el que veniamos persiguiendo.
- **Medido: cero menciones de los signos de apertura y de los acentos**, ni en `scripts/autocheck.py`
  ni en `references/auto-check.md` — mientras la nota del proyecto afirmaba que el auto-check de 19
  puntos incluia "apertura ¿¡". La documentacion daba por cubierta una regla que **nadie comprobaba**.
- Sale de la clase que `golden-verificador` midio en `golden-presenta`: los validadores degradan
  reglas duras a AVISO y devuelven exit 0 — **gana el script**, que es quien da el semaforo verde.
  Aqui ni siquiera hubo degradacion: no existia el check.
- **Check 25** (apertura ¿ ¡ en texto VISIBLE, fuera de comentarios) y **check 26** (acentos rotos /
  mojibake). Los dos **FALLAN, nunca avisan**.
- **Casos en las DOS direcciones**, que es donde estaba el riesgo real de estos dos:
  · un `¿` **dentro de un comentario Liquid** no se publica → NO debe fallar;
  · **las tildes correctas NO son mojibake** → NO deben fallar. Este es el falso positivo que mas
    dano haria, porque empujaria a quitar acentos correctos del copy, justo al reves de la regla.
  Por eso el check 26 busca las secuencias inequivocas de UTF-8 mal decodificado y **no** la ausencia
  de tildes: exigir tildes daria falsos positivos en marcas y siglas. **23/23.**
- Regla 0-H ampliada: regla dura → FALLA. Con la distincion explicita frente al registro de fabricas,
  que avisa por una razon legitima y distinta (otro escritor, ventana normal). Sin ventana, falla.

## G4.15 — 2026-09-02 — Escritor unico del registro, y por que ese chequeo NO debe bloquear
El Centro de Mando zanjo una contradiccion que salio de este mismo ciclo: esta fabrica editaba su
fila del registro y `golden-pdf-check` no la tocaba (el archivo dice "no editar a mano") — los dos
con argumento, pero **dos escritores sin coordinacion es exactamente la carrera que describimos
aqui**, y que un dia se salvo solo por el orden de llegada.
- **Zanjado: escritor unico = el CdM.** La fabrica sella y reporta; el CdM escribe la fila. Un
  escritor unico elimina la carrera de raiz, que es mejor que un acuerdo de tener cuidado entre dos.
  Esta skill deja de editar `REGISTRO-FABRICAS.md`.
- **La consecuencia, que es la parte fina:** entre sellar aqui y que el CdM regenere hay una
  **ventana de desfase LEGITIMA**. Si `sellos.py` fallara ahi, saltaria durante algo normal — el
  detector agresivo que la Regla 0-H persigue, y el camino mas corto a que la gente ignore la
  salida entera. Asi que `revisar()` ahora devuelve **(caras, fallos, avisos)**:
  **BLOQUEA** el sello y el changelog (viven dentro del arbol, los toca el mismo ritual, un desfase
  ahi nunca es legitimo) y **AVISA** por el registro, siempre visible, sin romper la corrida.
- **Los casos se actualizaron con el mismo criterio**, y S2 gano una exigencia extra: el desfase del
  registro debe aparecer en avisos **y NO contaminar los fallos**, o volveria a ser bloqueante por
  la puerta de atras. S4 y S5 siguen probando que un registro ausente o sin la fila **no se da por
  bueno** — ahora avisando. **19/19.**
- Patron general que deja: **lo que vive dentro de tu arbol y solo tu tocas, bloquea; lo que
  comparte escritor con otro, avisa.** Confundirlos produce o falsos positivos o silencios.

## G4.14 — 2026-09-02 — `sellos.py` tenia el defecto que su propia ley prohibe
Lo cazo el Centro de Mando y el punto es contra mi: **hornee un validador nuevo (`sellos.py`) el
mismo dia que consagre la Regla 0-H, y nacio sin una sola prueba**. La autoprueba pasaba 14/14 con
cero menciones de sellos. Tercera vez en el dia que 0-H se aplica a si misma.
- **El modo de fallo era silencioso, que es lo grave:** si un regex dejaba de casar y el codigo
  tratara "no encontre version" como "coinciden", `sellos.py` saldria 0 **siempre** y nadie se
  enteraria. El verde eterno que la propia regla persigue. Hoy solo se le habia visto pasar.
- **Refactor:** `revisar()` separado de `main()` y con rutas inyectables, para que las pruebas
  corran sobre **copias temporales** y jamas toquen `REGISTRO-FABRICAS.md`. Un validador que para
  probarse tiene que escribir en produccion no es un validador, es un riesgo. Ademas `None`
  (no se pudo leer) ya nunca se confunde con "coincide": es un fallo con nombre.
- **5 casos nuevos**: (S1) tres caras iguales → sin fallos, que de paso garantiza que **GFS_VERSION
  distinta NO cuenta como desfase** — si alguien "sincroniza" eso, rompe el otro eje; (S2) registro
  desfasado, el caso que el CdM regalo ya corrido; (S3) sello != changelog; (S4) registro ausente
  → falla en vez de dar por bueno; (S5) registro presente pero sin la fila, mismo trato. **19/19.**
- **Higiene de parte, tambien anotada:** mande al CdM una huella md5 y segui horneando despues, asi
  que la huella nacio vieja y no le cuadro al verificar. El parte se manda **al cerrar de verdad**,
  no a mitad de ronda.

## G4.13b — 2026-09-02 — La cuarta cara tiene DOS escritores (condicion de carrera observada)
Apunte corto pero con consecuencia. El Centro de Mando tambien corrige `REGISTRO-FABRICAS.md`
cuando detecta desfase, asi que esa cara tiene **dos escritores sin coordinacion**. Hoy escribimos
casi a la vez: el CdM la puso en G4.12 mientras aqui se ponia en G4.13. Medido despues del cruce,
quedo G4.13 — pero **se salvo por el orden de llegada**: si la escritura vieja hubiera aterrizado
de ultima, el registro habria RETROCEDIDO y el desfase volveria en silencio, porque nadie relee esa
cara por su cuenta. De ahi la regla practica: se MIDE al cerrar version con `scripts/sellos.py`, y
**con mas razon cuando otro chat dice haberla corregido** — que es justo cuando uno baja la guardia.

## G4.13 — 2026-09-02 — La cuarta cara de la version (y por que se desfasa sola)
Aviso del Centro de Mando: `REGISTRO-FABRICAS.md` declaraba **G4.7** mientras el disco iba por
**G4.11b** — cuatro versiones de desfase justo en la cara que leen los OTROS chats para saber en
que va esta skill. El CdM la corrigio, y **al medirla aqui ya estaba desfasada otra vez** (registro
G4.11b vs disco G4.12), en cuestion de minutos.
- **El diagnostico no es descuido, es estructura:** tres caras de la version viven dentro de la
  skill y el ritual de blindaje las toca; **la cuarta vive fuera del arbol**, en STACK-GOLDEN, asi
  que ningun bump la alcanza y nada avisa. Un fallo que se repite solo no se arregla acordandose
  mejor: se arregla con un instrumento.
- **`scripts/sellos.py`**: compara sello de SKILL.md, changelog y registro, y sale con codigo 1 si
  divergen. Respeta que **GFS_VERSION es el OTRO eje** (solo sube si cambia lo que la pagina
  produce): tratarlo como desfase y "sincronizarlo" a ciegas seria el error contrario. Si no
  encuentra el registro NO lo da por bueno: avisa y falla (ausencia no es prueba).
- Regla 0-H ampliada con la cuarta cara. Es la segunda vez en el dia que 0-H se aplica a si misma:
  primero con el WhatsApp corregido en el componente pero no en el generador, ahora con la version.

## G4.12 — 2026-09-02 — La prueba se llama `autoprueba.py` (y ahora caza falsos positivos)
Correccion del Centro de Mando sobre un error MIO de medicion, y es de clase, no de dato: en el
barrido de G4.10 busque **"selftest"** para contar cuantas skills prueban su validador, y conte 2.
Buscando tambien **"autoprueba"** son **SEIS**: golden-pdf-check, golden-chatea-auditoria,
golden-chatea-operacion, golden-skill-auditor y esta. **Esta casa nombra sus pruebas en espanol**,
asi que mi instrumento estaba ciego al idioma — el mismo fallo que la ley del grep con tilde.
- **`scripts/selftest.py` → `scripts/autoprueba.py`.** No es cosmetico: un archivo con nombre en
  ingles es invisible al proximo censo del arsenal, incluido el mio. Se arregla el instrumento, no
  el acuerdo.
- **Cambia la historia de la mejora:** esto no era inventar un patron, era **generalizar lo que 5
  skills de la casa ya hacian**. Hay arte previo del que copiar
  (`golden-chatea-auditoria/scripts/autoprueba.py`, 521 lineas, sabotea con casos CON y SIN tilde).
- **CASOS BUENOS anadidos** — el hueco que quedaba: la autoprueba solo verificaba que el validador
  CAZA lo malo, nunca que **deja pasar lo bueno**. Un check demasiado agresivo marca contenido
  legitimo y nadie se entera. Ahora se exige que NO dispare con: disparador correcto **con** tilde,
  disparador correcto **sin** tilde (Chatea admite ambas grafias) y mensaje libre a atencion.
  Un falso positivo entrena a ignorar la salida entera: es tan grave como no cazar.
- Nota de coherencia, cazada en la misma corrida: al renombrar el archivo quedo el `print` de
  cabecera anunciandose todavia como "selftest" — una cara sin tocar del mismo cambio, que es
  justo lo que la Regla 0-H prohibe. Corregido antes de cerrar la version.

## G4.11b — 2026-09-02 — El check 24 daba falso positivo: "block" contiene "lock"
Reparacion en caliente, cazada por el selftest en la primera corrida del check que acababa de
escribir. El check 24 buscaba `"lock" in bk.lower()` sobre los ids de bloque, y **"block" contiene
"lock" como substring**: cualquier id tipo `releasit_cod_form_button_app_block_ajGjx3` se leia como
candado, asi que el generador ya limpio seguia marcado como duplicado. Corregido con `(?<!b)lock`
en el check y en el sabotaje del selftest.
Vale dejarlo escrito: es exactamente la trampa de substring de la FAMILIA DE TRAMPAS DE CONTEO, y
la cometio quien acababa de escribir la regla que obliga a probar los validadores. Un check sin su
caso de prueba habria entrado a la skill mintiendo, y el falso positivo habria entrenado a ignorar
la salida — que es justo lo que la Regla 0-H prohibe.

## G4.11 — 2026-09-02 — Candado duplicado en el generador (lo destapo el selftest de G4.10)
La Regla 0-H estrenandose el mismo dia que se escribio. Al arreglar un caso de prueba que fallaba,
salio a la luz que **`assets/product.base.json` traia el candado DOS VECES**: el bloque
`custom_liquid_lock` dentro de `main` (1.005 bytes, sello **G3.14**, activo y en `block_order`) y
la seccion suelta `sec_lock` (2.128 bytes, version vigente) — con contenidos **distintos**.
- **Por que estaba:** G4.0 saco candado/ignition/whatsapp del main a secciones sueltas, pero el
  bloque viejo nunca se borro. Fosil de cuatro versiones atras.
- **Por que importa aunque no rompa nada:** ambos hacen `display:none`, asi que la pagina se veia
  bien — por eso sobrevivio. Pero son **dos fuentes de verdad**: quien edite el candado toca una y
  deja la otra viva con el comportamiento anterior, que es como nacen los bugs que nadie explica.
  Ademas cada pagina generada cargaba ~1 KB de CSS repetido.
- **Check 24** (candado duplicado) + su caso en el selftest, que reintroduce el fosil y exige que
  se cace. **11 de 11 pruebas pasan.**
- Corregido tambien el caso de prueba del candado ausente: apagaba una sola de las dos senales que
  mira el check. Era fallo del CASO, no del validador — y conviene dejarlo escrito, porque un caso
  de prueba mal hecho da una falsa tranquilidad identica a la de no tener prueba.

## G4.10 — 2026-09-02 — El auto-check pasa de prosa a HERRAMIENTA (+ Regla 0-H)
Salido de un barrido del arsenal instalado con denominador medido: **236 SKILL.md** (187 en
~/.claude/skills, 25 de ellos symlinks que un grep ingenuo no ve, + 49 de plugins). De esas,
**38 tienen scripts ejecutables y golden-shopify tenia 0**: sus checks vivian como un bloque
de codigo dentro de `references/auto-check.md` con la ruta escrita a mano.
- **`scripts/autocheck.py`** (23 checks, argumento de ruta, codigo de salida 0/1, flag `--base`).
- **`scripts/selftest.py`** — patron copiado de `golden-pdf-check` (`selftest.py`, "una prueba
  por cada version que cambio"): sabotea la plantilla base REAL con cada bug ya pagado
  (fuga `{# #}`, padding que Shrine rechaza, texto DEMO, candado ausente, tope de 50 KB en
  bytes UTF-8, disparador que no casa, WhatsApp placeholder, related encendido, hex huerfano)
  y exige que el validador los cace.
- 🔴 **Lo que encontro al primer intento** (por eso existe): (a) **4 falsos positivos** del check
  de colores — marcaba como huerfanos la DEFINICION de la paleta y los fallbacks de
  `var(--brand-*,#hex)`, que son el patron que la skill EXIGE; un validador que siempre grita en
  falso ensena a ignorar su salida. (b) **Un fallo real a medias: G4.9 corrigio el mensaje de
  WhatsApp en `componentes/whatsapp-flotante.liquid` pero NO en `assets/product.base.json`**, que
  es lo que de verdad genera las paginas — cada pagina habria nacido con el mensaje que no casa
  con ningun disparador. Corregido aqui.
- **Regla 0-H**: todo fallo que se paga se convierte en check + su caso de prueba; el validador
  se ejecuta y ademas se prueba; cero falsos positivos; buscar la CLASE, no el caso; y al tocar
  una regla, revisar TODAS sus caras (el fallo de arriba es la prueba).

## G4.9 — 2026-09-02 — El mensaje del boton es un DISPARADOR, no un texto (correccion de G4.8)
Precision del Centro de Mando sobre la Regla 0-G, verificada aqui contra la fuente autoritativa (las
skills de Chatea) antes de aplicarla: la formula real del disparador es
`Hola quiero información y precio de <PRODUCTO>` — **sin coma tras "Hola" y CON "y precio"** — y casa
**byte a byte** (gotcha D1: un emoji de 4 bytes corrompe el trigger).
- 🔴 **Defecto propio corregido:** el componente que hornee en G4.8 generaba
  `"Hola, quiero informacion de <producto>"` → **no casaba con ningun disparador**. Un cliente que
  pulsara ese boton caia en "Producto/Servicio no encontrado" → tablero **"No automatizado"**, que no
  mira nadie. Peor que no tener bot.
- ⚠️ **Hallazgo propio, mas fino que la fila:** el nombre del disparador es el **REGISTRADO EN CHATEA**,
  que casi nunca coincide con `product.title` de Shopify (titulo "Marca Spray | Frescura que Dura 48
  Horas" vs disparador "Marca"). Es decir: **tomar el titulo automaticamente era justo lo que rompia el
  byte a byte**. Ahora `WA_PRODUCTO` se copia A MANO del bot field; `product.title` queda solo para el
  mensaje de ATENCION, que lo lee una persona y admite texto libre.
- **Componente rehecho con destino explicito** `WA_DESTINO = "bot" | "atencion"`, dos numeros separados
  y **default seguro en "atencion"**: si no se puede comprobar el disparador, atencion — con atencion
  contesta una persona, con el bot mal apuntado el cliente escribe a un tablero muerto.
- **Regla corta anadida a 0-G:** boton CON contexto de producto → bot; boton GENERICO → atencion. Por eso
  la burbuja del TEMA (generica por diseno, sin product.title) va a atencion y nunca al bot.

## G4.8 — 2026-09-02 — Regla 0-G: canal humano siempre visible (WhatsApp en toda la tienda)
Regla dictada por FER: toda la tienda debe tener boton de WhatsApp — al bot de Chatea o, en su defecto,
a atencion al cliente. Un COD sin canal para preguntar pierde la venta en la duda.
- **Hueco medido:** la skill ya ponia el WhatsApp en la ficha y lo listaba como obligatorio, pero **no
  decia NADA sobre el duplicado con el tema**. Si el tema pone su burbuja para toda la tienda (que es lo
  que la regla exige) y la ficha pone la suya → **dos burbujas en la pagina de producto**.
- **Regla 0-G**: dos capas que no se pisan — el TEMA cubre toda la tienda (fuera de esta skill), la FICHA
  lleva la suya y manda ahi porque su mensaje sale con `product.title` (el bot/asesor sabe de que hablan
  sin preguntar). Nunca dos burbujas: `WA_SUPRIMIR_OTRAS = true` oculta las de tema/apps solo en la ficha.
- **`whatsapp-flotante.liquid` mejorado**: mensaje con el nombre del producto (antes era generico
  "informacion del producto") + bloque anti-duplicado apagable + nota de verificar en render real.
- Verificado: el candado landing NO afecta la burbuja (es position:fixed, no vive en header/footer).
- Numeracion censada antes de numerar: 0 a 0-F ocupados, sin duplicados → 0-G.
- FUERA DE ALCANCE de esta skill (fila para el chat del TEMA): poner la burbuja en home, colecciones,
  carrito y politicas. Esta skill solo hace la ficha de producto.

## G4.7 — 2026-08-28 — Regla 0-F: umbral de rentabilidad antes de la escalera (capacidad asimetrica)
Fila del Centro de Mando (analisis de capacidad asimetrica): esta skill **escribe precios y arma la
escalera de combos** pero tenia **CERO menciones de breakeven** (medido: 0 apariciones en los 76
archivos), mientras `golden-ads` lo calcula en cada cuenta. Consecuencia: la skill podia proponer un
"3 unidades por X" bajo el punto de equilibrio, y eso **no se descubre en la pagina — se descubre con
la pauta ya pagada**. Misma familia que G4.6 (plata que se pierde despues de pagar el clic), pero al
reves: alli el pedido no se podia despachar; aqui se despacha y se pierde en cada uno.
- **Nuevo `references/breakeven-combos.md`**: el criterio se HEREDA de golden-ads (breakeven CPA =
  margen bruto por unidad; breakeven ROAS = precio / margen bruto, ajustado por tasa de entrega en COD)
  — no se reinventa formula. Aporte propio: la aritmetica de la ESCALERA en COD, que es lo que golden-ads
  no cubre porque no arma precios: **el flete se paga por PEDIDO, no por unidad** (por eso la 2a y 3a
  unidad dejan mas margen — ese es el motor real del combo), pero **la devolucion golpea el pedido
  completo** (por eso el ajuste por entrega pega mas fuerte en el escalon mas descontado).
- **Regla 0-F** en reglas-de-oro.md + **umbral en la cabecera de `sec-combos.liquid`**: sin costo, flete
  y tasa de entrega reales, los precios quedan en `[confirmar]` y la seccion NO se publica.
- Los 3 chequeos por escalon: margen > 0 ajustado por entrega · sube el margen absoluto por pedido ·
  deja aire para el CPA. El que no pasa, sube de precio o se elimina.
- Se entrega el **CPA maximo rentable por escalon**, para que la pauta arranque con la linea trazada.
- Numeracion censada antes de numerar (ley del numero de regla): 0 a 0-E ocupados, sin duplicados → 0-F.
- 🟡 Auto-hallazgo del turno: el sello de G4.6 y su entrada citaban "Regla 0-D" cuando la regla quedo
  numerada **0-E** tras la auto-correccion — un puntero que manda al numero equivocado hace la regla
  invisible igual que un duplicado. Corregido DENTRO de este turno (norma del CdM: reparar lo propio
  antes de devolver el turno va con el MISMO numero). Clase: **la ley del numero de regla no termina al
  numerar — hay que repasar quien CITA ese numero.**

## G4.6 — 2026-08-28 — REGLA 0-E: la orden tiene que poder despacharse (cosecha de produccion)
Hallazgo REAL medido sobre ordenes en vivo de una tienda COD: paginas que convierten pero generan
ordenes que el fulfillment RECHAZA ("no se pueden agregar variaciones duplicadas del mismo producto").
Dos causas distintas, ambas verificadas en las lineas de las ordenes:
1. **Misma variante en dos lineas separadas** (mismo variant id, mismo precio) porque el order bump
   crea linea nueva en vez de sumar cantidad → debe ser UNA linea con cantidad 2.
2. **Dos productos distintos compartiendo el mismo SKU** (un producto suelto y una variante del
   multi-variante) → aguas abajo se leen como el mismo item duplicado.
Causa de fondo: Shopify permite el mismo producto en varias lineas; los sistemas COD modelan la orden
como UNA fila por (producto, variacion) con cantidad. Horneado como **Regla 0-E** en reglas-de-oro.md
+ advertencia operativa en la cabecera de `sec-combos.liquid` (que es SOLO visual: quien materializa
el combo es Releasit/el bump, y ahi es donde se decide si la orden se puede despachar).
🟡 Auto-hallazgo del mismo turno: la regla nueva nacio como **0-D**, numero que YA ocupaba otra regla
vigente (claims en bloques adyacentes, G3.17, escrita por otro chat) → renumerada a **0-E** antes de
cerrar el turno; la anterior conserva su numero por antiguedad. Y la fecha del caso estaba escrita a
mano (26) cuando la medida era otra → corregida con `date`. Clase: **antes de numerar una regla, mirar
que numeros ya existen** — el mismo defecto que la ley del numero de version, un nivel mas abajo.
Regla practica: **un combo = una variante con SKU propio**, el bump SUMA CANTIDAD, y ningun SKU se
comparte entre productos. Nota: fusionar lineas en una orden ya creada la destraba pero genera orden
FANTASMA en el fulfillment (cambia el id, la vieja cuenta doble) — por eso se previene en la pagina.

## G4.5e — 2026-08-26 — Titularidad de la fábrica declarada en el SKILL.md
- 🟡 **La fábrica de esta skill vivía SOLO en memoria** (`project_golden_shopify_chat_fabrica`) y el
  SKILL.md no la declaraba → `REGISTRO-FABRICAS.md` la listaba como "sin fábrica declarada / titularidad
  del CdM", lo que bajo la **Ley del Cambio Único** habría convertido a su propia fábrica en "fábrica
  ajena" (obligada a entregar filas en vez de reparar) y habría dejado creer a cualquier otro chat que
  podía editarla. Arbitrado por el CdM: manda la regla de FER. **Declarado en el SKILL.md:**
  `Fábrica: chat ✅ SKILL golden-shopify` + "solo la fábrica numera esta skill" (ley del número de versión).
- 🟡 Auto-hallazgo del mismo bump: la nota de los DOS EJES declaraba una foto ("Hoy: skill G4.5d · "
  "GFS_VERSION G4.5") que el propio bump a G4.5e dejó vieja al instante → reescrita **version-agnóstica**
  (cada eje se lee de su fuente, no de la nota). Una nota que cita versiones envejece sola: la clase es
  *no guardar fotos de estado en texto durable*.
- Adopción de la **Ley del Cambio Único**: bump de versión en el MISMO comando que el cambio (esta
  entrada y el sello se escribieron en un solo comando), y reporte al CdM con md5 + conteo + hora medida.

## G4.5d — 2026-08-24 — Dos filas del verificador de cierre
- 🔴 **FECHA MENTIDA en el sello:** SKILL.md y el changelog declaraban "2026-08-23" para rondas que se
  escribieron el **2026-08-24 22:13** (medido por mtime). **Causa raíz:** la fecha se tomó del contexto
  de la sesión en vez de MEDIRLA con `date` — la sesión cruzó de un día al otro y el sello se quedó en
  el día viejo. Corregido con la fecha real de cada ronda: el trabajo del base fue el 23 (03:09) y la
  reestructura + G4.5b/c el 24 → G4.5 queda como 23/24, G4.5b y G4.5c como 24.
  **Regla que deja:** la fecha de un sello se MIDE (`date` / mtime), nunca se hereda del contexto ni se
  copia de la entrada anterior.
- 🟡 **El Paso 0 del cerebro ordenaba "LÉELO PRIMERO" sin decir DÓNDE vive** → añadida la línea de la
  familia: el cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` y la resolución exacta la declara
  `golden-brand-brain` (ante duda de ruta, invocarla en vez de adivinar).

## G4.5c — 2026-08-24 — Dos filas del barrido D del Centro de Mando (verificadas y cerradas)
- 🟡 **`references/horizon/_golden-trust.liquid` era huérfano REAL:** existía y ningún texto vivo lo
  citaba (solo el changelog, que es historia) → un modelo trabajando Horizon no sabía que ya tenía un
  theme block escrito y probado. **Citado desde `references/horizon-bloques.md` §3.1** con su
  cuándo-usarlo, cómo instalarlo (`/blocks/_golden-trust.liquid`), por qué ya sirve y cómo clonarlo
  como molde de los demás bloques nativos.
- 🟡 **`examples/` vivía fuera de las carpetas canónicas** (references/scripts/assets/agents) y el
  inventario la marcaba como material que viajaría al marketplace tal cual. Los 3 ejemplos SÍ estaban
  citados, así que se eligió MOVER en vez de declarar excepción: ahora `references/examples/` y las
  **17 citas reescritas** en SKILL.md y references. Árbol de primer nivel: solo `assets/` + `references/`.
- Origen: pasada de contraste del CdM (955 ORO). Ambas verificadas de forma independiente en la fábrica
  antes de tocar nada (0 citas vivas del starter; 3 carpetas de primer nivel).

## G4.5 — 2026-08-23/24 — Auditoría golden-skill-auditor: se cierra la DEUDA del base + reestructura
Hallazgos con evidencia, todos reparados:
- 🔴 **DEUDA G4.x CERRADA:** `assets/product.base.json` seguía en el orden viejo de 17 secciones mientras
  el embudo canónico documentado iba en 24 — el GENERADOR contradecía a su propia documentación.
  **Regenerado a las 24** (21 del embudo + 3 de sistema) con los componentes que ya existían:
  sec-dolor-segmentado, sec-cta-suelto ×3 (puertas 2/3/final), sec-seguridad, ticker medio,
  sec-bloque-alternado (variantes + modo de uso), sec-combos, envío+garantía, sec-seo-aio-schema,
  y candado/ignition/whatsapp como secciones sueltas. Condicionales (dolor público B, variantes)
  y ruido (autoridad, ficha técnica, related) quedan apagados por defecto.
- 🔴 **Sellos desincronizados en 3 versiones distintas a la vez:** SKILL.md G4.4 · config-center G4.3 ·
  base.json **G3.14** (15 versiones atrás) → toda página generada salía sellada con una versión falsa.
  Los 3 orígenes sincronizados a **G4.5**.
- 🔴 **`## Paso 0 · Cerebro de marca` quedó ENCIMA del H1** (una adenda se insertó entre el frontmatter y
  el título): el documento abría con una sección antes de su propio nombre → movido bajo el H1.
- 🔴 **SKILL.md 623 líneas** (tope de la rúbrica: 500), con el PROTOCOLO TEMA VIVO **duplicado** (resumen
  duro arriba + versión completa abajo) → la versión completa sale a `references/tema-vivo.md` y la tabla
  del embudo a `references/embudo-canonico.md`; índice de archivos compactado. **623 → 491.**
- 🟡 **Puntero muerto:** el resumen mandaba a "la línea ~460" para el detalle, que ya vivía en la 520 →
  ahora apunta a un ARCHIVO, no a un número de línea (los números bailan con cada versión).
- 🟡 **Contradicción interna:** el mismo bloque decía que Ignition sale del main (G4.0) y la línea
  "Bloques del main" seguía listándolo → corregido.
- ✅ Verificado: cero datos privados, cero referencias rotas (`scraping-firecrawl.md` es cita válida a
  la skill hermana golden-investigacion-mercado), JSON válidos.

## G4.4 — 2026-08-22 — Cierre de auditoría golden-skill-auditor (críticos reparados)
Auditoría verificó 9 hallazgos críticos contra el archivo real; los 9 se confirmaron y se repararon:
1. **GFS_VERSION desincronizado** — el config center declaraba `"G3.14"` (~15 versiones atrás de la
   skill real, entonces G4.3) en `assets/config-center.liquid` y `references/componentes/00-config-center.liquid`.
   Corregido a `"G4.3"`.
2. **`imagenes.md` enseñaba el bug de comentario Liquid** — el ejemplo de "convención de slot de
   imagen" usaba `{# ... #}`, que NO es un comentario válido en Liquid (se imprime como texto) y es
   exactamente lo que caza `auto-check.md` check #17. Corregido a `{% comment %}...{% endcomment %}`
   con nota de advertencia explícita.
3. **`checklist-producto.md` con instrucción fósil de Ignition** — decía que vivía embebido en
   `01-propuesta.liquid`; desde G4.0 es `sec-ignition.liquid`, bloque independiente. Corregido, junto
   con el mismo lenguaje "bloque 1" fósil en los comentarios de `auto-check.md`.
5. **`sistema.md` con el inventario incompleto** — le faltaban 18 de los 46 `.liquid` reales de
   `references/componentes/` (incluyendo obligatorios de G4.0/G4.3: sec-seguridad, sec-disclaimer,
   sec-es-para-ti, sec-combos, sec-seo-aio-schema, sec-cta-suelto, sec-lock-landing, efx-reveal-seguro,
   efx-video-lazy, sec-bloque-alternado, sec-cine, sec-dolor-segmentado, sec-escenas, sec-ficha-tecnica,
   sec-fondo-cine, sec-timeline, sec-ya-lo-intentaste, 05b-rating-simple). Tabla completada a 46/46.
6. **Fallback real a `/cart/add` ausente** — REGLA #2 del SKILL.md y `releasit-cod.md` (desde G4.2)
   describían el fallback como si ya estuviera implementado, pero `08-boton-compra.liquid` solo
   disparaba el botón de Releasit si existía (`if(r) r.click();`) y no hacía nada si no aparecía.
   Implementado de verdad: reintento de 1.5s buscando el botón de Releasit y, si sigue sin aparecer,
   `POST /cart/add.js` con el `variant id` actual + redirect a `/cart`.
7. **`12-sticky-bar.liquid` con `aria-hidden="true"` fijo** — el JS solo alternaba la clase visual
   `gfs-visible` al hacer scroll, nunca el atributo de accesibilidad: el CTA quedaba inalcanzable por
   teclado/lector de pantalla cuando SÍ estaba visible (bug WCAG 2.2). Corregido: `aria-hidden`/`inert`
   ahora se togglean junto con la visibilidad real.
8. **Colisión de CSS `.gfs-why`** — `sec-beneficios.liquid` y `sec-por-que-elegir.liquid` usaban el
   mismo prefijo con marcado distinto; si un `product.json` cargaba ambos bloques, los estilos se
   pisaban. `sec-beneficios.liquid` renombrado a `.gfs-bnf` (y sumado a los selectores de layout PC /
   `content-visibility` del config center para no perder el tratamiento de escritorio).
9. **5 secciones reinventaban su propio `IntersectionObserver` sin red de seguridad** —
   `sec-cine`, `sec-escalera`, `sec-escenas`, `sec-manifiesto`, `sec-ya-lo-intentaste` arrancan con
   `opacity:0` y solo se revelan si su observer local dispara; a diferencia de
   `efx-reveal-seguro.liquid` no tenían el timeout de ~1.2s que fuerza la visibilidad si el observer
   falla, así que el contenido podía quedar invisible para siempre. Se les agregó el mismo patrón de
   red de seguridad por tiempo (no se migró el motor completo a `efx-reveal-seguro.liquid` porque cada
   sección tiene su propia coreografía de stagger — eso queda como mejora futura, no crítico).

**Sin cerrar en esta pasada (mejorables, no críticos):** `changelog.md` sin tabla de contenido (839+
líneas); orden de lectura de `reglas-de-oro.md` (0-C/0-D antes que 0-A/0-B "PRIORIDAD MÁXIMA" y que la
Regla 0 base); mayoría de `.liquid` usan `var(--brand-*)` sin fallback (si falta el bloque Paleta,
rompen); `sec-piramide.liquid` y `dawn-titulo.liquid` con color fijo `#0F6F5C` fuera del sistema de
Paleta; `content-visibility:auto` del config center solo cubre 7 clases (faltan `.gfs-cmb`, `.gfs-tl`,
`.gfs-sc`, `.gfs-try`, `.gfs-cine`, `.gfs-alt`, `.gfs-spec`, `.gfs-ship`, `.gfs-fit`).

## G4.0 — 2026-07-25 — PERFILES + embudo de 24 secciones (absorción de la página real en producción)
**Versión mayor: cambia la arquitectura, no solo el detalle.** Motivo: la skill documentaba un embudo
de 17 secciones mientras la página real que ya estaba corriendo iba en **24** y con otra estructura.
La skill se había quedado atrás de su propia producción. Se absorbió leyendo el `product.json` VIVO,
no una memoria (ver la regla de inventarios desde archivo vivo).

**1. Sistema de PERFILES — un solo motor, dos formas de vender.** Nuevo `references/perfiles.md`
y flag `PERFIL = "marca" | "catalogo"` en el config center. Decisión de diseño explícita: **NO se
bifurca en dos plantillas**, porque dos fuentes de verdad garantizan que una se quede atrás (que es
exactamente el problema que originó esta versión). El perfil solo cambia qué secciones entran, en
qué orden y con qué tono; el motor (Releasit, precio, sticky, candado, tickers, reglas de oro,
estándares de código) es único.
- `marca` → manifiesto, historia/origen, línea de productos. Vende identidad y recompra.
- `catalogo` → escalera de combos, demostración y comparativa **obligatorias**; fuera el manifiesto
  y la historia (suenan falsos en producto de catálogo); reglas de copy de dropshipping activas.
- Nueva pregunta inicial #2 (perfil), antes del país y los colores.

**2. Embudo canónico 17 → 24 secciones.** Candado, Ignition y WhatsApp **salen del main y pasan a
secciones sueltas** (son overlays: su orden no afecta el layout y así el cliente los apaga sin entrar
a los bloques del producto). Entran dolor segmentado por público, seguridad/objeción #1, demostración,
modo de uso, combos, envío+garantía y schema. Tres tickers en vez de dos.

**3. `sec-bloque-alternado.liquid` — el patrón dominante del cuerpo de la landing.** Imagen + texto
con el lado alternando; móvil apilado, PC dos columnas, imagen con `srcset`/`sizes`/`width`/`height`
(sin CLS) y float sutil solo en PC. Es el componente con el que se construye la mayor parte del
embudo: menos texto, más imagen.

**4. REGLA #6 — ninguna animación puede esconder lo que vende.** Caso real: el revelado al scroll
dejó secciones en blanco cuando el observer no disparó. Nuevo `efx-reveal-seguro.liquid`:
el CTA, el sticky y las imágenes quedan FUERA del revelado con `!important`; red de seguridad que
a los 1.2 s fuerza visible todo lo pendiente; `rootMargin` de 1200 px; re-escaneos para contenido
inyectado tarde; y opt-in por clase en `<html>` para que sin JS la página se vea completa.

**5. `sec-cta-suelto.liquid` reemplaza a `sec-cta-mid.liquid`.** El mismo CTA sirve para las puertas
2, 3 y 4. Un solo listener delegado para todos los botones de la página, y **fallback**: si el botón
principal no existe, hace scroll al precio en vez de quedarse mudo.

**6. `sec-seo-aio-schema.liquid` — el JSON-LD se muda a su propia sección invisible** (altura 0).
Antes vivía dentro del FAQ: si el cliente lo apagaba o lo movía, se perdía el SEO. Ahora sobrevive.
Se mantiene la regla de G2.2: `aggregateRating` solo con conteo REAL y verificable.

**7. `efx-video-lazy.liquid` — demostración en video sin matar la velocidad.** `data-src` +
`preload="none"` + poster WebP; el src se asigna solo al acercarse al viewport. Un MP4 con src
directo se descarga aunque esté al final de la página.

**8. `sec-seguridad.liquid` y `sec-dolor-segmentado.liquid`.** La primera resuelve la objeción #1
ANTES de las features (cuando el cliente llega al FAQ ya decidió que no). La segunda parte el dolor
en dos secciones cuando hay dos públicos con dolores distintos — con el criterio de cuándo NO usarla
(si hay un público dominante, segmentar diluye).

**9. Estado por defecto en producción:** countdown, garantía-bloque y descripción nativa se apagan
cuando ya hay una sección que hace ese trabajo mejor. Duplicar resta.

⚠️ **Pendiente de esta versión:** `assets/product.base.json` sigue con el order de 17 secciones.
Hasta regenerarlo, la referencia de orden canónica es la tabla de `SKILL.md`, no el base.

## G3.17 — 2026-07-18 — Aprendizajes de un build real (product.json tema Shrine)
Cinco lecciones absorbidas de un build en vivo, todas ADITIVAS (nada se reescribió ni cambió comportamiento):
- **Panel de Shopify = campo `"name"` del JSON:** el rótulo/número que el editor muestra para cada sección
  y bloque sale del `"name"` del `product.json`, NO del schema ni de comentarios. Para numerar/nombrar
  ("5 TICKER TOP", "0 CONFIG CENTER") se edita ese `"name"`. Error a no repetir: crear `sections/lc-NN-*.liquid`
  solo para renombrar el panel es innecesario. → `sistema.md`.
- **Marquee/ticker SIN HUECOS en PC ancho:** con pocos ítems, el loop `translateX(0→-50%)` deja blanco si
  cada mitad es más corta que un viewport PC (~1920px). Regla: repetir el contenido hasta que cada mitad
  supere ~1920px, con 2 mitades idénticas para que -50% sea continuo. → `efectos-premium.md` (sección tickers).
- **Contraste de emoji vs su fondo:** ningún emoji del mismo color que el fondo donde va (💚 sobre CTA verde
  se pierde) → emoji contrastante, regla para toda la página. → `estandares-liquid.md` (accesibilidad) + `reglas-de-oro.md`.
- **No repetir el mismo claim en bloques ADYACENTES:** cada bloque dice algo nuevo; los términos núcleo
  (envío gratis, contra entrega) se repiten solo en puntos de decisión, no pegados. → `reglas-de-oro.md` (Regla 0-D).
- **Reseñas de ejemplo con caras IA:** placeholders reemplazables (retratos tipo selfie, NO ecom-magic),
  marcados como EJEMPLO. → `reglas-de-oro.md`. Sellos → **G3.17**.

## G3.16 — 2026-07-10 — Overlays re-parentados al body + verificación PC/TABLET/MÓVIL siempre
Continuación del build real (mismo día): en PC el intro se veía como un CUADRITO. Causa: el bloque ignition
vivía dentro del main de Dawn y un ancestro con `transform` ancla `position:fixed` al contenedor. Fix de raíz:
- `sec-ignition.liquid`: **re-parent al `<body>`** como primera línea del script (igual que sticky/WhatsApp).
  Punto 0 nuevo en la REGLA DE SALIDA + fila nueva en la tabla de errores.
- **Regla del usuario (innegociable)**: el render real se verifica SIEMPRE en los 3 escenarios — móvil ~390px,
  tablet ~768px y PC ~1440-1920px — sin scroll horizontal, nada cortado, overlays a viewport completo
  (`rect = innerWidth×innerHeight`). Actualizado el paso 3 del RENDER REAL en `auto-check.md`. Sellos → **G3.16**.

## G3.15 — 2026-07-10 — Ignition a prueba de todo + imágenes que encajan (build real Dawn, vertical sueño)
Dos lecciones de un build real, absorbidas de raíz:
- **IGNITION**: la salida del intro dependía 100% de `animation … forwards` (CSS) → si la pestaña abre en
  segundo plano o algo resetea animaciones, el overlay queda MONTADO. `sec-ignition.liquid` ahora trae motor
  de salida JS multi-vía (timer + interacción + visibilitychange + failsafe `removeChild` a los 7s + una vez
  por sesión) y `prefers-reduced-motion → display:none` (eliminado el "bypass" que forzaba animaciones).
  Regla nueva en `ignition-variantes.md` (REGLA DE SALIDA) + check #20 en `auto-check.md`.
- **IMÁGENES QUE ENCAJAN**: infografías con texto quemado se decapitaban en slots `object-fit:cover`.
  Regla: crop fotográfico exacto al ratio del slot o imagen completa a proporción natural. Filas nuevas en
  la tabla de errores de `reglas-de-oro.md` + ítem obligatorio del render real en `auto-check.md`.
- El RENDER REAL ahora exige probar el ciclo de vida del intro (aparece → desaparece del DOM, incluso con
  pestaña en segundo plano) y el encaje de imágenes ANTES de entregar. Sellos → **G3.15**.

## G3.14 — 2026-07-06 — Auditoría golden-skill-auditor (informe → reparación)
Hallazgos con evidencia, todos arreglados:
- **Referencia rota:** un archivo premium retirado citado 3 veces en `efectos-premium.md` pero no existe
  (archivo retirado en una versión vieja) → re-apuntado a `references/componentes/`, ejemplos y
  `related-products.premium.css.txt` (que SÍ existen).
- **Signos de apertura** (interrogación/exclamación invertidas) en 12 docs + `references/examples/demo-dawn.json` (regla GLOBAL del usuario:
  solo signo de cierre) → eliminados en todos.
- **Línea de versión bajo el H1** de SKILL.md (patrón de la casa) → añadida.
- Confirmado por inventario: cero datos privados, cero componentes huérfanos reales (los 38 citados),
  sin scripts rotos. Sellos → **G3.14**.

## G3.13 — 2026-07-02 — Anonimización para compartir con la comunidad
Auditoría de privacidad de toda la skill (para publicarla). Confirmado CERO: WhatsApp real (solo el
placeholder falso 573001234567), rutas /Users, emails, IDs/theme-IDs de Shopify. Anonimizado:
- **Dominio real** eliminado → "la tienda en vivo".
- **Marcas/tiendas reales** de builds anteriores → descriptores genéricos de categoría (p. ej.
  la marca del producto demo → "PRODUCTO DEMO"; nombres de otros productos → "un sérum facial (ejemplo)",
  "un producto de salud (ejemplo)", etc.). Sin nombrar ninguna marca real en el registro.
- Se mantienen términos de CATEGORÍA/ingrediente (verrugas, veneno de abeja) como ejemplos genéricos
  (no privados) por decisión del usuario. Sellos → **G3.13**.

## G3.12 — 2026-07-02 — Orquestación de imágenes: golden-shopify = CEREBRO
Integración con la fábrica de imágenes. golden-shopify NO genera imágenes: decide el plan y reparte.
- **Nuevo `references/imagenes-orquestacion.md`:** reparto (golden-ecom-magic = infografías foto real+texto
  por navegador, SOLO imágenes · golden-ugc-avatar/Higgsfield = GIF/video · Nano Banana = photoreal),
  el **BRIEF VISUAL** como contrato de sincronización entre skills (yo doy el QUÉ, cada generadora sabe el CÓMO),
  y matriz de formatos por ubicación (galería 1080×1080 · descripción 1-3 infografías 1080×1350 · escalera 1:1 · cine 16:9/video).
- **Descripción liviana:** solo 1-3 infografías clave (no 8-12); el resto de la historia visual la cargan
  las secciones (escalera/cine/video) + bloques nativos (SEO/editable/liviano). Alineado con la estrategia de ecom-magic.
- **Playbook Paso 3** reescrito: producir el BRIEF e invocar la skill generadora correcta. Sellos → **G3.12**.
- **Cómo piensa Ecom Magic (mapeo brief→campos):** documentado que imita una PLANTILLA de referencia
  y compone sobre foto real; qué PUEDE (arquetipos grilla/pack/testimonio/antes-después/cómo-actúa,
  redimensionar/traducir/editar) y qué NO (video/GIF, tamaños ≠ 1080×1080/1080×1350, layouts sin
  plantilla → van a Higgsfield/Nano Banana). Tabla de mapeo brief→campos para cero conflictos.
- **CORRECCIÓN (dato del usuario):** Ecom Magic NO está limitado a 1080×1080/1080×1350 — tiene MUCHOS
  formatos y **tamaño PERSONALIZADO (ilimitado)**; esos dos son solo el estándar Golden más usado.
  Nunca descartar Ecom Magic por tamaño (sí puede 16:9 del cine, etc.). El único límite real: video/GIF
  (→Higgsfield) y foto photoreal sin texto/plantilla (→Nano Banana). Corregido en imagenes-orquestacion.md.


## G3.11 — 2026-07-01 — Paddings THEME-SAFE (fin del error "must be a step in the range")
Al pegar en Shrine, el tema rechazó al guardar: **"Setting 'padding_top' must be a step in the range"**
(las secciones de fusión traían padding_top/bottom = 36/24/10, y Shrine solo acepta pasos válidos de
su rango). Arreglado de raíz:
- **`product.base.json` y ejemplos:** eliminados TODOS los `padding_top`/`padding_bottom` de las
  secciones → el tema aplica su default (nunca rechaza al guardar; sirve igual en Shrine y Dawn).
- **auto-check #19:** falla si alguna sección trae padding_top/bottom.
- Sellos → **G3.11**.

## G3.10 — 2026-07-01 — Test final en producto (PRODUCTO DEMO/verrugas generado desde cero)
Se generó la página de verrugas DESDE CERO con la skill (no a mano) para el test de cierre. El test
CAZÓ un fósil que ningún check anterior veía:
- **`RELEASIT_BUTTON_CONFIG.text = "QUIERO MI PRODUCTO DEMO"`** — el texto del botón de compra vive
  dentro de un objeto JS, NO en un `{% assign %}`, así que la reescritura por-variable no lo tocaba.
  Corregido en la página + horneado: **auto-check #18** (texto DEMO VISIBLE fuera de comentarios,
  incluye configs JS) + nota en el PLAYBOOK Paso 1 (reescribir Releasit/sticky, no solo los assign).
- Resto del test: la skill reprodujo la página aprobada con copy coherente (spray→rocía, veneno de
  abeja protagonista, sin lunares, WhatsApp real, INVIMA con enfoque positivo, reseñas de verrugas).
- Sellos → **G3.10**.

## G3.9 — 2026-07-01 — Pasada de perfección: componentes limpios, a11y universal, playbook 0→1000
Auditoría exhaustiva de los ~40 componentes (no solo la base):
- **Fósiles en 4 componentes fuente** neutralizados: `01-propuesta` ("máxima energía"), `sec-ignition`
  ("potencia desbloqueada"), `sec-beneficios` ("energía y vitalidad"), `sec-faq` (copy de bebida
  energética: tapa-vaso/Borojó/Guaraná). **Cero fósiles en toda la skill.**
- **prefers-reduced-motion UNIVERSAL:** la capa global `gfs-a11y` pasó de lista de clases a reset
  `*,*::before,*::after` → cubre los 11 componentes que animaban sin guardia + todo lo demás, de una.
  Inyectada también en el ejemplo Dawn (que no tenía capa a11y global).
- **Signo de apertura /** eliminado del ejemplo Dawn.
- **PLAYBOOK DE GENERACIÓN (0→1000)** nuevo en SKILL.md: receta de 5 pasos (datos reales → config →
  copy por sección → imágenes → coherencia → auto-check + render real). Cierra la brecha "genera esqueleto".
- **`imagenes.md`:** regla de oro escalera/cine (URLs nuevas, nunca las infografías de la descripción).
- Ejemplos re-sincronizados. Sellos → **G3.9**.

## G3.8 — 2026-07-01 — Ejemplos de referencia al día + FAQ demo de-fosilizado
Los ejemplos que la skill usa como referencia estaban VIEJOS (demo-shrine en G2.8, 0/6 secciones de
fusión) → engañaban la generación. Sincronizados a la arquitectura G3.7:
- **`references/examples/demo-shrine.json`** = snapshot de `product.base.json` (embudo canónico, 17 secciones).
- **`references/examples/demo-dawn-v2.json`** llevado al embudo canónico: 6 secciones de fusión añadidas como
  custom-liquid `scheme-1`, `sec_autoridad` off, **candado landing** insertado y **FAQ accesible**.
- **FAQ demo de la BASE** tenía copy de bebida energética (tapa-vaso, "energía y vigor", Borojó/
  Guaraná/Chontaduro) → **de-fosilizado** a copy product-agnostic. Ambos ejemplos pasan el auto-check.
- Sellos → **G3.8**. (Pendiente 1000: validar Dawn renderizado en vivo + QA móvil + flujo de imágenes.)

## G3.7 — 2026-07-01 — Coherencia de producto (auditoría "como cliente" de verrugas → 870/1000)
Leída la página entera como cliente. Estructura 10/10; bajaba por INCOHERENCIAS de copy. Reglas nuevas
(Regla 0-C) + scrub ampliado:
- **Fósiles de energía en intro/hero:** la base traía `IGN_SUBTITLE="POTENCIA DESBLOQUEADA"`,
  `⚡ PRODUCTO DEMO ⚡` y un acento cian huérfano `#0bd4fd`. Neutralizados en `product.base.json`.
  Añadidos al auto-check: "potencia desbloqueada" (scrub demo) y `#0bd4fd` (colores huérfanos).
- **Regla 0-C — coherencia de producto:** la FORMA manda el verbo (spray→rocía, gotero→gota…);
  liderar con la USP/ingrediente estrella (no "naturales" genérico); no vender lo que el producto NO
  trata (lunares); un solo WhatsApp real; claims legales solo si son reales (enfoque positivo).
- (En la página en vivo se aplicó todo: spray, veneno de abeja como protagonista, intro re-tematizado,
  ticker sin "lunares", WhatsApp real, INVIMA fuera con enfoque positivo. Eso es específico del producto,
  no de la skill; lo que se hornea son las REGLAS de arriba.)

## G3.6 — 2026-07-01 — Reingeniería de arquitectura: embudo canónico + 6 secciones de fusión en la base
El cliente: "se ve fea, no convierte, dos bloques grandotes al final, quiero el ticker después de la
descripción." Rediseño como product-page profesional (neuroventa). Cambios horneados:
- **Orden canónico NUEVO** (Regla 0-A en reglas-de-oro.md): Ticker → HERO+CTA#1 → **Ticker tras
  descripción** → PROBLEMA → AGITAR → SOLUCIÓN → **CTA#2** → BENEFICIOS → **VISIÓN+CTA#3** → RESEÑAS →
  EXPECTATIVAS → ES-PARA-TI → COMPARACIÓN → FAQ → **MANIFIESTO+CTA#4** → disclaimer.
- **La base generaba plantillas INCOMPLETAS:** faltaban 6 secciones (el usuario las metía a mano).
  Ahora horneadas en `product.base.json` desde sus componentes: `sec_escenas`, `sec_ya`,
  `sec_cine`, `sec_timeline`, `sec_esparati`, `sec_disclaimer`. Order de la base: 14 → **17 visibles**.
- **Se separaron los dos bloques oscuros del final** (VISIÓN "cine" + MANIFIESTO): la visión sube a
  mitad de embudo (future-pacing tras beneficios), el manifiesto queda como cierre. Ya no van pegados.
- **Ruido fuera por defecto:** `seccion_autoridad` (cifras placeholder = prueba social falsa) apagada;
  ficha técnica y related-products siguen off.
- **Cadencia de CTA**: gate cada 2-3 secciones (hero / tras-mecanismo / tras-beneficios / cierre).
- **Ticker = respiro visual** entre secciones pesadas (regla de ritmo). Sellos → **G3.6**.

## G3.5 — 2026-07-01 — Fin de "las letras": fuga de comentarios {# #} + nombres de bloques
Auditoría de la página en vivo (screenshot real de verrugas). Bugs REALES horneados:
- **`{# ... #}` se imprimía como TEXTO en la página** (encima de la Escalera y la Ficha Técnica salía
  todo el bloque `{# === COMPONENTE: ... === #}`). Causa: `{# #}` NO es comentario válido en Liquid
  (el válido es `{% comment %}`) → cuando queda dentro de un `custom_liquid` se renderiza literal.
  Arreglado: (1) `product.base.json` — quitados los `{# #}` de todos los custom_liquid; (2) los 38
  componentes de `references/componentes/` convertidos de `{# #}` → `{% comment %}...{% endcomment %}`;
  (3) auto-check nuevo (#17) que falla si aparece `{# ` o ` #}` en un custom_liquid. (Cuidado: en CSS
  `{#id{…}` es válido y NO debe marcarse → el check exige `{#`+espacio o el cierre ` #}`.)
- **Ficha Técnica se veía con `[confirmar]`** (specs sin llenar) → se confirma apagada por defecto;
  solo se enciende si el producto es gadget/kit Y se llenan specs reales.
- **5 bloques del main sin nombre** ("custom liquid" a secas en el editor) → nombrados: HERO, INTRO
  ignition, EFECTO HEADER, SEO+carrito, COLOR FOOTER. Y **header_efx + footer_efx apagados por
  defecto** (con el candado landing puesto, pintan sobre header/footer ocultos = fantasmas).
- Badge hero fósil "MÁXIMA ENERGÍA" eliminado (scrubber ampliado). Sellos → **G3.5**.

## G3.4 — 2026-07-01 — Landing bloqueada + fin del copy demo fósil + relacionados off
Hallazgos de la prueba "todo activado" sobre verrugas. Tres defectos reales, horneados:
- **Copy DEMO fósil en los tickers:** los 2 `horizontal-ticker` traían texto hardcodeado del
  PRODUCTO DEMO (suplemento): "ENERGÍA Y VITALIDAD EN CADA USO", "VITALIDAD Y ENERGÍA…". No están
  conectados al centro de control → nunca se adaptaban al producto. **Neutralizados** a copy COD
  product-agnostic (satisfacción / resultados / compra segura / garantía). Regla nueva: el texto de
  ticker SIEMPRE se reescribe por producto (cero "energía/vitalidad" salvo que el producto lo sea).
- **Nuevo bloque `custom_liquid_lock` (CANDADO LANDING):** oculta header + announcement + footer del
  tema con `display:none` (NO saca del DOM → el tema sigue inicializando su JS y las secciones
  animadas aparecen; ocultar el header desde el editor SÍ las rompía). El cliente ya no puede irse al
  home. Va justo después de PALETA en el `main`. Apagable con `LOCK = false`. Componente:
  `references/componentes/sec-lock-landing.liquid`. **Default: ON** de aquí en adelante.
- **Relacionados apagados por defecto** (`related-products` disabled:true) — confirmado en base. Solo
  se muestran las secciones que diseñamos; el usuario los desoculta manual si quiere.
- Sellos `GFS_VERSION` → **G3.4** en los 3 orígenes.

## G3.3 — 2026-06-29 — Correcciones de la página real (verrugas en vivo) — todo horneado
Auditoría de la página en vivo (la tienda en vivo (producto de salud/estética), tema Shrine)
tras el primer build. Bugs REALES encontrados y corregidos en la skill:
- **Escalera duplicaba las infografías del cliente:** `sec-escalera` tenía un fallback que jalaba
  `product.images` (que en muchas tiendas SON las infografías de la galería/descripción) → salían 2-3
  veces. **Eliminado.** Ahora, sin `P#_IMG` propia, el panel queda como tarjeta de solo texto (limpia).
  Para imágenes en la escalera: URLs NUEVAS, no las de la galería. (component + base.json)
- **"Por qué elegir" duplicada:** el `base.json` traía DOS secciones (`seccion_por_que_elegir` +
  `custom_liquid_Q4zb89` legacy). **Eliminado el duplicado** del order y de sections.
- **Motor COD se inyectaba 3× (3 listeners):** añadido **guard de idempotencia**
  `if(window.gfsFireCOD)return;` en los 3 orígenes → un solo listener aunque se inyecte varias veces.
- **Puntuación:** regla GLOBAL nueva del usuario → **nunca ``/`` de apertura**. Quitados de TODO el
  copy (componentes + base + config) y documentado en `reglas-de-oro.md`.
- Sellos `GFS_VERSION` → **G3.3** en los 3 orígenes. (Lección de generación: incluir SIEMPRE
  `seccion_whatsapp` en el order y NO dejar paddings en 0 —dan secciones apretadas—.)

## G3.2 — 2026-06-29 — FUSIÓN con "GOLDEN FULL" · Fases 2 y 3 (motor COD + secciones premium)
Se completa la fusión: lo mejor de la línea `cc-` reconstruido en `gfs-` tokenizado y accesible.
- **Fase 2 — Motor COD robusto (`gfsFireCOD`)** en el config center (3 orígenes): cualquier elemento
  con `data-cod` dispara el **botón Releasit correcto** (cascada de selectores), **evita** el botón
  que vive dentro del modal, y **reintenta** con timeout si Releasit aún no inyectó. Coexiste con los
  botones existentes (no los rompe). Más confiable que un `.click()` simple.
- **Fase 3 — 5 secciones premium nuevas** (todas gfs- tokenizadas, accesibles, apagables,
  respetan `prefers-reduced-motion`):
  · `sec-escenas.liquid` — "te suena?" (identificación por escenas, reveal escalonado).
  · `sec-ya-lo-intentaste.liquid` — demoledor de objeciones (X animadas sobre alternativas fallidas + CTA data-cod).
  · `sec-timeline.liquid` — "qué esperar paso a paso" (maneja expectativas, baja devoluciones).
  · `sec-cine.liquid` — sección cine full-bleed oscura (contraste emocional + CTA).
  · `sec-fondo-cine.liquid` — fondo cinematográfico parallax (orbes de marca + puntos, off en móvil).
- **PADDINGS THEME-SAFE (lección real):** un build falló en Shrine con *"Setting 'padding_top' must
  be a step in the range"*. Se **clampeó** todo padding de sección del `base.json` a **≤36** (16
  valores) y se documentó la regla en `temas.md` (Shrine/temas con rango menor: no exceder 36, o
  no fijar padding y dejar el default; recipe de "quitar paddings" si un tema los rechaza).
- Sellos `GFS_VERSION` → **G3.2** en los 3 orígenes. JSON revalidado. Con esto golden-shopify
  **alcanza y supera** a la línea GOLDEN FULL: tiene su persuasión + legal + COD **Y** conserva
  tokens + accesibilidad + embudo sistemático.

## G3.1 — 2026-06-29 — FUSIÓN con "GOLDEN FULL" · Fase 1: protección legal (salud)
Descubrimiento: las páginas premium de producción (Vantta verrugas, etc.) NO se hicieron con esta
skill sino con una línea hermana **"GOLDEN FULL SHOPIFY" (clases `cc-`)** que evolucionó aparte y
se especializó en persuasión + seguridad legal + motor COD robusto — mientras golden-shopify (`gfs-`)
se especializó en tokens + embudo + accesibilidad. Plan: **fusionar** lo mejor de la FULL, pero
reconstruido en `gfs-` tokenizado y accesible (no copiar su código, que hardcodea colores y tiene
FAQ no accesible). **Fase 1 (lo crítico, protección legal):**
- **Nuevo `componentes/sec-disclaimer.liquid`:** disclaimer legal (cosmético ≠ medicamento +
  contraindicaciones). Flag `SHOW_REGISTRO` (INVIMA/aval) SOLO si es REAL (REGLA #3). Tokenizado.
- **Nuevo `componentes/sec-es-para-ti.liquid`:** "es para ti?" (califica al cliente) + columna de
  **seguridad/contraindicaciones** (cuándo NO usar / consultar antes). Accesible, tokenizado.
- **Ambos declarados OBLIGATORIOS para vertical SALUD/estética** en SKILL.md (protección legal).
- Sellos `GFS_VERSION` → **G3.1**. Fases siguientes: **F2** = motor COD robusto (estilo `ccFireCOD`:
  elige el botón Releasit correcto, evita el del modal, reintenta) → generalizado a `gfs-`;
  **F3** = secciones premium (fondo cinematográfico parallax, "te suena?", "ya lo intentaste" con X,
  timeline de resultados, sección cine full-bleed), reconstruidas en `gfs-` tokenizado + accesible.

## G3.0 — 2026-06-29 — Pase de PERFECCIÓN: la skill ahora CUMPLE lo que predica
Objetivo: cerrar la brecha "predica accesibilidad/calidad pero sus bloques no la cumplían". Ahora el
generador (`product.base.json`) **pasa sus propias 6 verificaciones de estándares** (antes se
auto-reprobaba). Cambios:
- **FAQ accesible (WCAG 2.2):** la pregunta pasó de `<div>` clickeable a **`<button aria-expanded
  aria-controls>`**; la respuesta es `role="region"` con `aria-labelledby`. Operable por teclado
  (Tab + Enter/Espacio), foco visible, y respeta `prefers-reduced-motion`. Aplicado en
  `componentes/sec-faq.liquid` y en el bloque `seccion_faq` del `product.base.json`.
- **Capa GLOBAL de accesibilidad `<style id="gfs-a11y">`** en el config center (3 orígenes): **foco
  visible** en TODOS los CTA/enlaces (`:focus-visible`) + **red de seguridad `prefers-reduced-motion`**
  que calma toda animación `gfs-`/`pe-`/`mb-`/`zbx` de la página aunque un bloque lo olvide. Un solo
  bloque cubre foco + movimiento de toda la página.
- **Tokens con fallback** en los componentes tocados (`var(--brand-primary,#…)`) para que no
  dependan del config center si se usan sueltos.
- **Auto-verificado:** `product.base.json` corre las 6 checks de estándares (FAQ aria, img lazy/alt/
  dimensiones, reduced-motion, BEM) → **0 fallos** (antes fallaba a11y).
- **Bloque HORIZON NATIVO de arranque:** nuevo `references/horizon/_golden-trust.liquid` — theme
  block real (schema + `block.shopify_attributes` + `t:` + tokens + a11y). Horizon deja de ser solo
  doc: ya hay un template nativo de referencia.
- **Render REAL (procedimiento repetible)** documentado en `auto-check.md`: subir a tema no
  publicado → preview → verificar móvil+PC (foco/teclado, CLS, CTA, secciones sin vacíos) → screenshot.
- **Ejemplo al día:** `references/examples/demo-shrine.json` regenerado desde el base actual (accesible). **Limpieza:**
  eliminado `INSTALAR.txt` (ya se instala por el marketplace de Comunidad-Golden). Sellos → **G3.0**.
- Residual honesto (fuera del archivo de skill, es del entorno/producto): un render 100% headless
  automático (depende de una tienda Shopify en vivo) y un tema Horizon nativo COMPLETO (aquí va el starter).

## G2.8 — 2026-06-29 — Poder full: estándares Liquid (vG staging) + arquitectura Horizon
Se hornearon a la skill los DOS references originales preparados en staging (escritos para Golden,
nada copiado de las skills oficiales de Shopify) → golden-shopify queda autosuficiente en calidad de
código Y en temas de nueva generación:
- **`references/estandares-liquid.md` (reemplazado por la versión de staging):** "código sano" para
  todo bloque/sección — arquitectura sección/bloque/snippet + cuándo cada uno; schema JSON correcto
  (tipos, `range`, presets, `enabled_on`/`disabled_on`, límites, validez); traducciones/patrón
  "EDITAR AQUÍ" (texto nunca hardcodeado); **CSS** BEM con prefijo único + tokens con **fallback**
  (`var(--brand-primary,#f7a540)`) + CSS defensiva + `!important` documentado; **JS** mínimo,
  progressive enhancement, Web Components, sin librerías; **rendimiento** (enlaza `rendimiento.md`,
  no duplica): `content-visibility`, `lazy`+dimensiones sin CLS, animar solo `transform`/`opacity`,
  `prefers-reduced-motion`; **accesibilidad WCAG 2.2** por componente (FAQ `<details>`/`aria-expanded`,
  carrusel, cart drawer/modal `role="dialog"`, `aria-live` para precio/stock, sticky); checklist de 10.
- **Nuevo `references/horizon-bloques.md`:** arquitectura block-based del tema **Horizon** (theme
  blocks nativos, `@theme`/`@app`, `block.shopify_attributes` obligatorio, presets con bloques
  anidados, claves `t:`), cómo lo aprovecha Golden (custom_liquid para Dawn/Shrine/Sense · theme
  blocks nativos para tiendas nuevas/migración), tabla "cuándo Horizon vs clásico" y nota de licencia.
  Enlaza con `temas.md` (adaptador general) y `estandares-liquid.md` — sin duplicar.
- **SKILL.md:** REGLA DE INGENIERÍA ampliada ("bloque o sección" + remitir a `horizon-bloques.md`
  para Horizon/tiendas nuevas); ambos references añadidos a la lista. `temas.md` apunta a
  `horizon-bloques.md` para el detalle de Horizon (una sola fuente de verdad).
- **`auto-check.md`:** +3 verificaciones (total 6 de estándares) — `<img>` sin `alt`, `<img>` sin
  dimensiones (CLS), y clases genéricas sin prefijo BEM (colisión con el tema).
- Sellos `GFS_VERSION` → **G2.8** en los 3 orígenes. JSON revalidado; script de auto-check compila.

## G2.7 — 2026-06-29 — Estándares de código Liquid horneados (skill autosuficiente)
golden-shopify ya NO depende de skills externas para la calidad del código. Se añadió un reference
**original** (conocimiento redactado de cero, nada copiado de las skills oficiales de Shopify):
- **Nuevo `references/estandares-liquid.md`** — "Estándares de código Liquid Golden". Cubre:
  arquitectura section/block/snippet + cuándo cada uno; schema JSON correcto (tipos de settings,
  presets, enabled_on/disabled_on, límites); LiquidDoc en snippets; `{% render %}` (nunca
  `{% include %}`); traducciones/locales y el patrón Golden "EDITAR AQUI" (texto nunca hardcodeado);
  **CSS** BEM con prefijo único anti-colisión + design tokens `var(--brand-*)`/`var(--cta)` + CSS
  defensiva + `!important` solo para overrides documentados; **JS** mínimo, progressive enhancement,
  Web Components, `defer`, idempotente, sin librerías; **rendimiento de código** (enlaza
  `rendimiento.md`, no duplica): `content-visibility`, `lazy`+sin CLS, animar solo
  `transform`/`opacity`, `prefers-reduced-motion`; **accesibilidad WCAG 2.2** por componente
  (carrusel, cart drawer, modal, acordeón FAQ, sticky), foco, contraste AA, `alt`, labels,
  `aria-live`; y una **checklist "código sano"** de 10 puntos.
- **SKILL.md cableado:** (1) REGLA DE INGENIERÍA dura tras "Convención de código": antes de escribir
  CUALQUIER bloque `custom_liquid`, cumplir `estandares-liquid.md` (sano + accesible + rápido);
  (2) añadido a la lista de Referencias con su línea descriptiva.
- **`auto-check.md`:** +3 verificaciones de cierre — FAQ con `aria-expanded`/role (a11y), `<img>` sin
  `loading="lazy"` (CLS), y animaciones sin `prefers-reduced-motion`.
- Sellos `GFS_VERSION` → **G2.7** en los 3 orígenes. JSON revalidado.

## G2.6 — 2026-06-25 — FAQ baja al cierre (embudo optimizado para VENDER)
Ajuste estratégico del embudo a pedido del usuario ("quiero vender, no solo educar"). La FAQ deja
de ir en la posición 3 (justo tras la descripción, G2.4) y baja a **antes del manifiesto/cierre**.
- **Principio:** las objeciones solo importan cuando ya hay deseo. El FAQ es manejo de objeciones →
  va abajo, tras la prueba social (reseñas/autoridad/por qué elegir) y JUSTO antes del último CTA,
  para quitar el último "pero" cuando la persona ya lo quiere. Subirlo arriba plantaba dudas antes
  de crear el antojo.
- **La fricción COD inmediata NO se mueve:** garantía + "pagas al recibir" + barra logística siguen
  arriba dentro de `main` (Riesgo→0 pegado al CTA #1), así que el comprador caliente no necesita la
  FAQ arriba. Solo se reubicó la FAQ; el resto del embudo de 3 puertas (G2.5) queda intacto.
- **Nuevo `order` en `assets/product.base.json`:** ticker → main → cómo actúa → escalera → ficha
  técnica *(off)* → CTA#2 → reseñas → autoridad → por qué elegir? → **FAQ** → manifiesto+CTA#3 →
  ticker → por qué elegir? legacy → relacionados. Documentado en SKILL.md (tabla del embudo).
- Sellos `GFS_VERSION` → **G2.6** en los 3 orígenes. JSON revalidado.

## G2.5 — 2026-06-25 — Reestructura a EMBUDO DE CONVERSIÓN de 3 puertas
Cambio estratégico: la página deja de ser una lista de secciones y pasa a ser un **embudo** donde
cada fase pide la venta y la siguiente recupera al que no compró, atacando su objeción. Decisión del
usuario tras analizar los 17 bloques del main + 7 secciones + el arsenal de componentes apagados.
- **Nuevo orden canónico (embudo)** en `assets/product.base.json`: Ticker → **PRODUCTO+CTA#1** → FAQ →
  Cómo actúa → **Escalera** → Ficha técnica *(off)* → **CTA#2** → Reseñas → **Autoridad** →
  **Por qué elegir?** → **Manifiesto+CTA#3** → Ticker → WhatsApp → Relacionados.
- **3 puertas de cierre** (antes solo 1): CTA#1 Releasit temprano (comprador caliente), CTA#2
  `sec-cta-mid` tras la demostración, CTA#3 verde del manifiesto (cierre emocional). Los 3 disparan
  `#custom-releasit-btn`.
- **Activadas por defecto** (antes apagadas o sueltas al fondo): `sec-escalera`, `sec-cta-mid`,
  `sec-autoridad`, `sec-por-que-elegir`, y el CTA del manifiesto (`CTA_TEXT` = "QUIERO EL MÍO AHORA").
  Reseñas/autoridad/por-qué-elegir suben desde el fondo a su punto de máximo impacto.
- **REGLA #3 aplicada a los componentes activados** (nada se envía vacío ni con placeholder visible):
  `sec-autoridad` pierde los `[N]` → cifras de EJEMPLO reemplazables (+12.000 clientes, +30.000
  entregados); `sec-escalera` y `sec-por-que-elegir` pasan de texto-instrucción ("Describe aquí…")
  a copy genérico presentable y reemplazable. `sec-ficha-tecnica` queda **incluida pero apagada**
  (`disabled`) porque sus specs son datos duros `[confirmar]` (no se inventan, REGLA #3).
- Documentado el embudo en `SKILL.md` ("Estructura canónica = EMBUDO DE 3 PUERTAS"). Sellos
  `GFS_VERSION` → **G2.5** en los 3 orígenes. JSON revalidado; auditoría: 0 placeholders en
  secciones activas, 3/3 CTAs presentes.

## G2.4 — 2026-06-25 — FAQ tras descripción · reseñas de ejemplo · ficha técnica (build Banda, Dawn, Colombia)
Cambios de SISTEMA absorbidos de un build real (banda para dormir Bluetooth). El copy del producto
NO se absorbe; la skill queda genérica/anónima.
- **Orden canónico nuevo — FAQ inmediatamente después de la descripción del producto.** Decisión
  del usuario. `assets/product.base.json` reordenado: ticker → main → **faq** → cómo-actúa → reseñas →
  manifiesto → ticker → whatsapp → related. Documentado en SKILL.md ("Estructura canónica"): la
  referencia de orden es SIEMPRE el `product.base.json`, no `references/examples/demo-dawn-v2.json` (desfasado
  desde v1.31, aún con el FAQ al fondo). Esto cierra la duda base-vs-ejemplo.
- **REGLA #3 invertida (reseñas/rating): nunca dejar vacío.** Si el cliente no tiene reseñas/rating,
  se INVENTAN ejemplos buenos (5–6 reseñas variadas con nombres locales y alguna de 4★ + rating
  creíble tipo `4.8 · 127 reseñas`), marcados `EJEMPLO — reemplazar por reales`. Prohibido placeholder
  visible (`[RATING]`, "sé el primero", arrays vacíos, `0.0/5`). La **honestidad se mantiene solo en
  datos de riesgo legal**: precios, tiempos de entrega, claims médicos/INVIMA y specs duras (mAh,
  voltajes, medidas) → se confirman, no se inventan. El **JSON-LD `aggregateRating`** sigue condicional
  al conteo REAL (los ejemplos son visuales en página, no estructura para Google — se preserva el fix G2.2).
  Aplicado en `componentes/sec-resenas.liquid` (default 5–6 reseñas + salvaguarda que oculta la sección
  si quedara vacía), `05-verificado-google.liquid` (4.8) y `05b-rating-simple.liquid` (4.8 · 127).
- **Nuevo `componentes/sec-ficha-tecnica.liquid`:** grid de specs (ícono + label + valor), 1 col móvil /
  2 col desktop, config-driven S1..S6, hereda `var(--brand-*)`, patrón EDITAR AQUI / NO TOCAR, apagable.
  Los VALORES nacen en `[confirmar]` (specs duras = REGLA #3). Añadido al set mínimo y a la matriz de
  arquetipos (útil en D Gadget/Demo y E Kit).
- **`componentes/sec-escalera.liquid`:** fallback automático — si un `P#_IMG` va vacío y el producto
  tiene galería, usa `product.images[idx]` (modulo) a 800px. La escalera nunca queda en blanco (refuerza REGLA #3).
- **`componentes/sec-manifiesto.liquid`:** CTA verde de cierre OPCIONAL (`#gfs-mani-cta`, `var(--cta)`,
  shine + pulse, aparece al hacer scroll con clase `pe-show`) que dispara `#custom-releasit-btn`. Variable
  `CTA_TEXT` editable; vacío = oculto. Respeta `prefers-reduced-motion`.
- Sellos `GFS_VERSION` → **G2.4** en `assets/config-center.liquid`, `componentes/00-config-center.liquid`
  y `assets/product.base.json` (JSON revalidado con `json.loads`).

## G2.3 — 2026-06-25 — Absorción del build un producto de salud/digestivo (ejemplo) (Dawn, salud/digestivo)
Analizado el `product.zero-breath.dawn.json` completo (build Dawn en G2.2). La mayoría de mecánicas
ya estaban en la skill (sticky→body, reveal `pe-revealed`, why-cards, hide del floating). Se
absorbió SOLO lo genuinamente nuevo y product-agnóstico (el copy de un producto de salud/digestivo (ejemplo) NO se absorbe):
- **Nueva variante de Ignition #9 "Respiración / Bloom"** (`references/ignition-variantes.md`): núcleo
  que respira + anillos + partículas que se elevan + título letra por letra + barrido diagonal.
  De-brandeada (las letras del título se setean por producto). Vertical: salud/bienestar/digestivo.
- **Nuevo componente `componentes/05b-rating-simple.liquid`**: rating liviano con reseñas REALES
  ("5.0/5 · N reseñas verificadas"), sin logo de Google ni medias estrellas. Alternativa honesta a
  `05-verificado-google` y alineada a REGLA #3 (lleva el conteo real; si no hay, no se muestra).
- **Manifiesto con partículas que se elevan** (`references/efectos-premium.md` §5): capa de partículas
  auto-contenida (heredan `--brand-light`, suben atravesando el bloque) — variante del manifiesto.
- **Botón**: oculta también `._rsi-buy-now-button-product-floating` (algunos temas Dawn muestran ese
  flotante extra de Releasit). Aplicado en `componentes/08-boton-compra.liquid` y `product.base.json`.
- Sellos `GFS_VERSION` → G2.3. Confirmado que el build Dawn ya nace con todo G2.2 (cta-center,
  desktop-apple, schema condicional, tickers custom-liquid scheme-1, descripción nativa oculta).

## G2.2 — 2026-06-25 — Absorción de la última versión del build de verrugas (PRODUCTO DEMO)
Se extrajeron y absorbieron los cambios de SISTEMA de la última versión del `product.json` de Tag
Recede (el copy específico del producto NO se absorbe; la skill queda genérica):
- **Nueva capa `<style id="gfs-cta-center">`** en el config center: centra el texto de TODOS los CTA
  (botón Releasit principal, sticky, doble CTA y el botón del **cart drawer** de Releasit
  `._rsi-buy-now-button-cart` / `._rsi-modal-submit-button`). Apagable. Evita textos de botón
  descentrados cuando el tema/Releasit los alinea a la izquierda.
- **Schema SEO condicional (REGLA #3):** el `aggregateRating` del JSON-LD ahora solo se renderiza si
  `SCHEMA_REVIEWS` tiene un conteo REAL. El default pasa de `"150"` (inventado) a `""` (vacío), con
  comentario guía. Antes inyectaba 150 reseñas falsas en Google en cada build.
- **Limpieza:** eliminado el keyframe muerto `gfsCartGlow` (no se usaba). `content-visibility` ahora
  incluye `.gfs-lad` (la escalera) para mejor rendimiento de render.
- Aplicado en los 3 orígenes: `assets/config-center.liquid`, `references/componentes/00-config-center.liquid`,
  `references/componentes/efx-seo-cart.liquid` y el `assets/product.base.json` (JSON revalidado).
  Sellos `GFS_VERSION` → G2.2.

## G2.1 — 2026-06-24 — Capa desktop "Apple" consolidada (absorbida de build real)
Absorbida del build más evolucionado de un chat de producción (PRODUCTO DEMO, Golden Colombia): se
reemplaza la capa de layout escritorio básica de v1.31 (solo `max-width`) por la capa
**`<style id="gfs-desktop-apple">`** mucho más fina y centralizada en el config center. En PC (≥990px):
- Secciones a `max-width:1140px` (≥1280px → 1240px), centradas; títulos a 40px con tracking.
- **Escalera → rejilla de 2 columnas** (`display:grid`) en vez de filas largas con lados vacíos.
- FAQ ancha y legible (920px, q/a más grandes); reseñas con más padding y texto 15.5px.
- Bloques de la columna de compra (garantía, envío, countdown, doble CTA) acotados para que no se
  vean "móvil estirado" en PC; doble CTA con `min-height:60px` y 18px.
- Se conserva `.pe-pyramid` en los caps de ancho (la versión absorbida no lo incluía → no degradar).
- Capa **apagable**: quitar el `<style id="gfs-desktop-apple">` devuelve el layout mobile-first.
- Aplicada en los 3 orígenes del config center: `assets/config-center.liquid`,
  `references/componentes/00-config-center.liquid` y el bloque paleta de `assets/product.base.json`
  (JSON revalidado). Sellos `GFS_VERSION` → G2.1.
- NO se absorbieron (decisión del usuario, este pase): motores `.py` de build/recolor ni la receta
  de port a Dawn — quedan como candidatos para un pase futuro.

## G2.0 — 2026-06-19 — 🎉 RELEASE ESTABLE
Primer release mayor. La skill GOLDEN SHOPIFY queda consolidada como sistema completo y blindado:
- **Arquitectura modular:** cada efecto/función es un bloque independiente y apagable (REGLA #5);
  Ignition propio y distinto por página (8 variantes); base tokenizada (recolor = 1 variable).
- **4 reglas innegociables** (#1 distinta · #2 CTA verde #1D9E06 · #3 no inventar · #4 completa) + #5 bloques.
- **6 temas** en 2 familias (clásica: Dawn/Shrine/Shrine Pro/Sense · nueva: Horizon/Pitch).
- **Pipeline de imágenes** Nano Banana Pro → Shopify; specs de galería/infografías; auto-check de cierre.
- **Anónima** (sin nombres reales) y **read-only / canónica** (solo se edita en la fábrica con OK del usuario).
De aquí en adelante el versionado parte de 2.0 (2.1, 2.2…).

## v1.33 — 2026-06-19 — Candado: skill CANÓNICA solo-lectura
- La skill se protege en **read-only** (`chmod -R a-w`) para que **NINGÚN proceso externo**
  (otras sesiones de Claude, linters, absorciones automáticas) la modifique. Se puede LEER libremente.
- Motivo: se detectaron ediciones concurrentes desde fuera de la fábrica (entradas de changelog y
  builds que no se escribieron aquí). Nota: el FS no distingue "chat", todas las sesiones son el mismo
  usuario; el candado bloquea por permisos, no por identidad.
- **Protocolo de edición:** solo en la fábrica (este chat) → desbloquear (`chmod -R u+w`) → editar →
  re-bloquear (`chmod -R a-w`). Aviso CANÓNICA / solo-lectura añadido al tope de SKILL.md.

## v1.32 — 2026-06-19 — Bloques INDEPENDIENTES + Ignition único (REGLA #5)
- **Desempaquetado el mega-bloque "propuesta" (18 KB, 5 cosas en 1)** en 5 bloques propios:
  `01-propuesta` (hero) · `sec-ignition` (intro) · `efx-header-cine` · `efx-seo-cart` (SEO+carrito)
  · `efx-footer-color`. Cada uno se apaga/prende solo desde el editor de Shopify. Contenido
  preservado 100%, base parsea. block_order del main pasó de 13 a 17 bloques.
- **REGLA #5:** cada efecto = su propio bloque; nada de bloques abiertos para rellenar con código
  (si hace falta video/imagen → sección NATIVA del tema, no slot de Liquid).
- **Ignition único por página:** nuevo `references/ignition-variantes.md` con 8 variantes
  cinematográficas 100% CSS; regla de no repetir intro entre páginas, elegir por vertical.

## v1.31 — 2026-06-19 — Layout ESCRITORIO (PC) — adiós "franja central"
La plantilla era mobile-first y en PC se veía como una columna angosta centrada con los lados
vacíos. Se añadió una **capa de layout para escritorio centralizada en el config center** (aplica
a toda página de la skill, sin tocar 15 componentes):
- `@media(min-width:990px)`: las secciones de ancho completo (`.gfs-lad` escalera, `.gfs-steps`
  cómo actúa, `.gfs-reviews`, `.gfs-why`, `.pe-pyramid`) suben a **max-width 1140px**; FAQ a 920px
  (ancho de lectura); doble CTA a 560px. `@media(min-width:1400px)`: 1280px en pantallas grandes.
- Con `!important` para ganarle a los max-width estrechos de cada componente, así llenan el ancho.
- Las bandas (autoridad, manifiesto, tickers) ya eran full-width. Los bloques del producto
  (precio, garantía, logística…) siguen en la columna del producto (no se ensanchan, correcto).
- Aplicado a `assets/config-center.liquid`, a la plantilla `references/examples/demo-dawn-v2.json` y al
  entregable real `product.producto-demo.json`. Sello → v1.31. Resultado: se ve bien en **móvil Y PC**.

## v1.30 — 2026-06-19 — Plantilla PRO v2 (Dawn, máximo impulso de compra) + fixes de componentes
Absorbido del build real **tienda-demo / producto-demo** (página entregada e integrada por API).
Es la evolución del esqueleto Dawn a "plantilla profesional persuasiva" lista para vender:
- **Nueva plantilla de referencia `references/examples/demo-dawn-v2.json`** (anonimizada, tokenizada,
  con slots de imagen `REEMPLAZA-TU-CDN`): embudo COMPLETO de impulso →
  ticker · producto (eyebrow + oferta + **countdown activo** + rating + precio dinámico +
  **CTA verde** + garantía + barra logística) · **escalera de venta con imágenes reales** ·
  cómo actúa · **doble CTA a media página** · reseñas · por qué elegir? · banda de autoridad ·
  manifiesto · FAQ · ticker · WhatsApp. Es la base Dawn recomendada de aquí en adelante.
- **Fixes de componentes (propagan a todo build):**
  - `12-sticky-bar.liquid` → **sticky anclado al `<body>`** (`appendChild`): `position:fixed`
    siempre relativo al viewport; corrige el bug de "sticky pegado arriba" cuando un ancestro
    tiene `transform`.
  - `whatsapp-flotante.liquid` → mismo anclaje al `<body>`.
  - **Nuevo `sec-cta-mid.liquid`** → doble CTA verde a media página, **sombra suave** (sin el
    "escalón" `0 6px 0` que se veía mal).
- **Énfasis de persuasión/impulso por defecto:** countdown evergreen activo, doble CTA,
  escalera demostrativa con fotos reales, escasez/urgencia, prueba social y CTA en 1ª persona.

## v1.29 — 2026-06-19 — Renombrada a GOLDEN SHOPIFY
- Skill renombrada `golden-full-shopify` → **`golden-shopify`** (dir + frontmatter + título +
  sello en cada página + rutas internas). Variable interna `GFS_VERSION` se conserva. La vieja
  archivada pasó a `golden-shopify-DEPRECATED-2024` para evitar colisión de nombre.

## v1.28 — 2026-06-19 — 6 temas oficiales en 2 familias
- Temas confirmados por el usuario: **Dawn, Shrine, Shrine Pro, Sense, Horizon, Pitch.**
- Agrupados en 2 familias: **clásica** (Dawn/Shrine/Shrine Pro/Sense — el product.json pega) y
  **nueva** (Horizon + **Pitch** — product.json NO pega → bloques Custom Liquid sueltos).
  Pitch añadido junto a Horizon en `temas.md` e intake.

## v1.27 — 2026-06-19 — Auto-verificación + tema Horizon + fijar Ignition
- **Auto-verificación de cierre (`references/auto-check.md`):** script que valida el product.json
  antes de entregar (JSON parsea, sin color demo viejo, rating≠0.0, var(--cta), sello, Ignition,
  Releasit) + checks visuales. Enganchado en Paso 6.
- **Tema HORIZON añadido (`temas.md`):** arquitectura nueva de Shopify; el product.json NO pega →
  entregar por **bloques Custom Liquid sueltos** para pegar en el editor. Intake ahora ofrece
  Dawn/Shrine/Sense/**Horizon**/otro y la skill adapta TODO el código al tema indicado.
- **Intro IGNITION fijado como obligatorio:** vive embebido en `01-propuesta-valor.liquid` (no se
  quitó nunca); ahora la checklist y el auto-check verifican que `gfs-ignition` esté presente para
  que no se caiga al reescribir el bloque 1.

## v1.26 — 2026-06-19 — Adelgazar SKILL.md (progressive disclosure)
- Movido el detalle operativo a nuevo `references/operacion.md`: (A) Modo actualización/upgrade,
  (B) sello + nota interna, (C) ritual de absorción. En SKILL.md quedan punteros cortos.
- Condensados Paso 2 (tokenización → `sistema.md`) y Estructura/Arquetipos (→ `arquetipos.md`).
- SKILL.md: 373 → 316 líneas (sin perder nada; todo el detalle vive en referencias). Base parsea.

## v1.25 — 2026-06-19 — Re-sanitización (privacidad) + auditoría
- **Fix de regresión de privacidad:** al absorber v1.19–v1.24 se recolaron nombres reales de
  producto/competencia (gadget perfumador, cubre-rayones, espejo LED, sérum facial, mascarilla
  verde, tratamiento capilar, fibras capilares, tienda demo). Re-anonimizados a descriptores
  genéricos. Verificado: 0 nombres de producto reales (solo quedan menciones del prefijo de
  código en la narración histórica del changelog). Regla reforzada: al absorber mejoras, NO
  reintroducir nombres reales — usar descriptor de categoría.
- Auditoría completa: base parsea, 23 componentes tokenizados (incl. los nuevos), 13 referencias.

## v1.24 — 2026-06-18 — Generación de imágenes AUTOMÁTICA end-to-end (Nano Banana Pro → Shopify)
Absorbido del proyecto real **tienda demo / producto demo**. Pasa el "modo imágenes" de *preguntar +
slots* a un **pipeline probado que integra todo solo**:
- **Pregunta #8 reforzada (SKILL.md):** SIEMPRE **CON o SIN generación?** CON = **Nano Banana Pro**
  (`gemini-3-pro-image` vía Gemini API key); SIN (ya tiene imágenes) = pedir URLs o **reutilizar la
  galería/multimedia del producto**.
- **Ubicación por defecto (confirmada por el usuario):** **bloques de la landing + galería del
  producto**. La descripción NO lleva imágenes (va oculta/recreada en bloques).
- **`imagenes.md` — "Pipeline AUTOMÁTICO probado":** API key en `~/.gemini_key` (no usar
  stitch/Antigravity, su token pierde el project); generación que **compone el frasco real desde su
  foto** (REGLA #3); optimizar <300 KB (Pillow); **subida por API a Shopify Files**
  (`stagedUploadsCreate` → POST multipart 201 → `fileCreate` con `filename` exacto → **URL
  predecible** `cdn…/files/<nombre>.jpg` que la plantilla ya espera); `productCreateMedia` para la
  galería. + **tabla de errores reales y su fix.**
- **Límite documentado:** el MCP de Shopify **bloquea escribir el tema LIVE/MAIN** → el `product.json`
  final lo pega el usuario; imágenes y galería sí entran por API. Botón COD muerto = inventario
  (agotado); sticky roto = ancestro con `transform` → `appendChild(body)`.

## v1.23 — 2026-06-17
- **Modo imágenes opcional (preguntar):** la skill ofrece 2 opciones — generar imágenes
  decorativas (si hay herramienta/API de imágenes conectada; puede tener costo) o sin imágenes
  con slots. Si pide generar y NO hay herramienta conectada, avisa en 1 línea + sugerencia breve.
- **Portabilidad/seguridad documentada:** la skill son archivos de texto, NO lleva API keys; al
  compartirla, el receptor NO hereda la API del usuario (conecta la suya). Nota general, sin inflar.

## v1.22 — 2026-06-17
- **Set de imágenes de landing ganadora** en `imagenes.md` (de página real + specs del usuario):
  galería = 4-6 cuadradas 1080×1080 <300KB; descripción = infografías verticales 1080×1350,
  ~10 paneles en arco PAS (hook→problema→mecanismo→beneficio→usos→contraindicaciones→comparativa
  →ingredientes→garantía→CTA). Las hace Ecom Magic AI / las aporta el usuario; la skill las
  coloca, ordena y NO duplica en HTML; complementa con secciones en código.

## v1.21 — 2026-06-17
- **Imágenes / "todo listo" (`references/imagenes.md`).** Regla: el producto REAL lo aporta
  el usuario (la IA no lo inventa); las infografías van en HTML (no como imagen); lo decorativo
  (fondos/íconos/ilustraciones) sí lo genera la IA (stitch/Gemini, Canva). Hosting en Shopify
  Archivos/CDN. Convención de slots `[IMG: ...]` con placeholder visible si falta la URL.

## v1.20 — 2026-06-17
- **La URL es CONTEXTO, no la página del usuario (Paso 0.0).** La URL puede ser suya, de la
  competencia o solo referencia. Se usa SOLO para entender el producto y adaptar el copy con
  info real; NUNCA clonar ese diseño, copiar sus reseñas, ni bajar la calidad a lo que tenga.
  El usuario parte de cero. Intake pregunta si la URL es suya o referencia (cambia anti-duplicado).
- **REGLA #4 — Completitud obligatoria.** Nunca entregar algo mediocre/incompleto: toda página
  trae TODO el sistema (set mínimo obligatorio listado en SKILL.md), siempre distinta (REGLA #1)
  pero sin que falte ningún bloque/sección. Los arquetipos cambian énfasis/orden, no si los
  bloques existen. Prohibido decir "lista/100" si falta algo o no se vio renderizada.

## v1.19 — 2026-06-17 — Auditoría de la tienda real (16 productos)
Recorrí los 16 productos de la tienda real y absorbí el patrón de las páginas GANADORAS
(Fibra/Kit capilar completo, sérum facial, espejo LED, gadget perfumador) vs las crudas (mascarilla verde, tratamiento capilar).
Hallazgo central: el motor de la skill YA cubría los fundamentos (timeline de envío, ahorro
en pesos, garantía COD "en la puerta de tu casa", badge Google, CTA "QUIERO MI… 🔥"). Lo que
faltaba eran las **secciones de persuasión narrativa** y la **estrategia de copy/ángulo**:
- **3 componentes nuevos:**
  - `sec-escalera.liquid` — storytelling alternado imagen+texto (3–9 paneles, 1 beneficio =
    1 objeción / re-cierre, reveal-on-scroll, alterna lado, soporta GIFs). El motor de venta
    de las páginas de demostración. Tokenizado.
  - `sec-por-que-elegir.liquid` — trust-grid de 4 íconos **personalizable al beneficio del
    producto** (no la grid genérica de tienda). Tokenizado.
  - `sec-autoridad.liquid` — banda/marquesina de prueba social de marca, tokenizada y con
    PLACEHOLDERS evidentes (REGLA #3: nada de "+100 mil" inventado sin confirmar).
- **`reglas-de-oro.md`:** presets de tono por ángulo (lujo/DIY/belleza/salud), reframe de
  categoría, eyebrow de beneficio, CTA primera persona + doble CTA, y **guía de copy
  compliant para verticales sensibles** (íntimo cómplice, antiedad clínico-light, hongos/
  antifúngico → versión cosmética por defecto por riesgo Meta/INVIMA).
- **`arquetipos.md`:** 2 arquetipos nuevos — **D) Gadget/Demostración** y **E) Kit/escalera
  de valor** (compone productos, ancla precio = suma de partes; distinto del bundle 2x/3x del
  Releasit form). Matriz ampliada con los componentes nuevos. **Checklist de página ganadora**
  (los 5 elementos que separan vender de no vender).
- **`checklist-producto.md`:** bloque "Página ganadora" (countdown real, garantía COD humana,
  escalera con GIFs, doble CTA, kit, tono por ángulo, compliance de verticales sensibles).
- **FIX de la base (`assets/product.base.json`):** el config center embebido estaba
  desincronizado con `assets/config-center.liquid` — NO emitía los tokens `--cta/--cta-dark/
  --cta-rgb` ni el sello `GFS_VERSION`. Resultado: el botón verde (`var(--cta)`) salía sin
  fondo. Añadidos `CTA_BG/CTA_BG_DARK/CTA_BG_RGB` (verde #1D9E06) + tokens en `:root` y el
  sello v1.19. Detectado al generar los 17 product.json de la tienda real (los agentes lo
  parchearon en cada salida). Base revalidada: parsea OK.

## v1.18 — 2026-06-17
- **Bundles 2x/3x = en el formulario de Releasit, NO en la página.** Documentado en
  `releasit-cod.md`: las ofertas por cantidad las maneja el Releasit COD Form (quantity offers);
  la página solo dispara el form y puede mencionar el ahorro en el copy. "Bundle" sale del roadmap.

## v1.17 — 2026-06-17
- **PRIVACIDAD / ANONIMIZACIÓN (para compartir la skill):** removidos TODOS los nombres de
  producto, marca y tienda reales y neutralizado el código. Reemplazos: nombres → "PRODUCTO
  DEMO"/"MARCA DEMO", tiendas → "tutienda-demo.com"/"Tienda Demo"; prefijo de código `x10`→`gfs`,
  `X10_BRAND`→`GFS_BRAND`, `X10_REVIEWS`→`GFS_REVIEWS`, `x10_cd_end`→`gfs_cd_end`; ejemplos
  renombrados a `demo-shrine.json` / `demo-dawn.json` y sanitizados. Verificado: 0 nombres
  reales, 0 `x10`, los 3 JSON parsean. Backup en `SHOPIFY BY CLAUDE/_backup-skill-pre-sanitizado`.
- **Regla 0 (prioridad máxima) en `reglas-de-oro.md`:** la instrucción explícita de color
  del usuario PISA las reglas genéricas (REGLA #2 del CTA, "badges en rojo"). Armonía:
  máximo 2 colores fuertes y un solo color de acción; un único acento de urgencia.
- **`colores-conversion.md`:** aclarado que "destacar" = brillo/tamaño/sombra, no cambio de
  matiz (CTA verde profundo sobre verde claro basta) + tope de 2 colores fuertes.
- **`checklist-producto.md`:** nuevo bloque "Render visual OBLIGATORIO" — ver la página
  renderizada (screenshot) antes de declararla lista; chequeo de armonía de paleta.
- **`03-oferta-destacada.liquid`:** borde 3px→2px + aviso de no duplicar el acento de
  urgencia y preferir relleno suave en vez de caja hueca con borde grueso.
- **Lección absorbida (Producto Demo de salud, Tienda Demo):** apilar verde+naranja+rojo y declarar
  "100/100" sin ver la página renderizada produjo un resultado "horrible". Corregido a paleta
  verde monocromática con CTA verde profundo.

## v1.16 — 2026-06-02
- **Fix rating 0.0/5.** El contador animado ahora arranca con su valor final como texto y
  tiene fallback (si el observer no dispara, queda en el número real, nunca en 0.0).
  Checklist con chequeo de calificación. (#3 del camino a 100.)

## v1.15 — 2026-06-02
- **Optimización de rendimiento en la base PRODUCTO DEMO.** Removido el *killer* global de animaciones
  (`@media prefers-reduced-motion{*...}`) que congelaba animaciones en móvil (preferencia del
  usuario). Añadido `content-visibility:auto` + `contain-intrinsic-size` a las secciones largas
  (.gfs-reviews/.gfs-faq/.gfs-manifesto/.gfs-steps/.gfs-why/.pe-pyramid) vía CSS global del
  config center → el navegador no renderiza esas secciones hasta acercarse (LCP/scroll más rápidos).
  Verificado: base parsea OK, 0 killers, content-visibility activo. (Fuentes e imágenes de la base
  ya estaban OK: sin @import, imgs con lazy.)

## v1.14 — 2026-06-02
- **TOKENIZACIÓN DE COLORES (mejora mayor).** Los componentes y la base PRODUCTO DEMO ahora leen
  `var(--brand-*)` / `var(--cta)` del config center en vez de hex hardcodeados. **Recolorear
  = cambiar las variables del config center** (mata el search-replace y los bugs de color viejo).
  CTA = `var(--cta)` (verde fijo), separado de la marca. Verificado: 0 hex de marca fuera del
  config center, base.json parsea OK. Añadidos tokens `--cta/--cta-dark/--cta-rgb` al :root.
  Actualizados SKILL.md (Paso 2), sistema.md, checklist. Roadmap: tokenizar = HECHO.

## v1.13 — 2026-06-02
- **Auditoría de la skill + 2 mejoras grandes.**
- Nuevo `references/rendimiento.md`: velocidad de carga (fuentes con preconnect+swap sin
  @import, imágenes lazy/fetchpriority/width-height anti-CLS, JS consolidado, backdrop-filter
  y content-visibility, quitar killer de prefers-reduced-motion). + checklist de rendimiento.
- **REGLA #3 (anti-invención):** prohibido inventar reseñas/rating/precios/tiempos/claims;
  si falta info, PREGUNTAR; si se sigue, placeholder evidente, nunca dato falso. + checklist.

## v1.12 — 2026-06-02
- **CTA con color FIJO: verde ganador `#1D9E06`** (oscuro `#157A04`) en todo producto, salvo
  orden expresa. Añadido `CTA_BG`/`CTA_BG_DARK`/`CTA_BG_RGB` al config center; notas en los
  componentes botón y sticky; REGLA #2 y colores-conversion.md actualizados (la guía por
  vertical aplica a marca/acentos, no al CTA). Distinto del verde WhatsApp `#25D366`.

## v1.11 — 2026-06-02
- **Nota interna al final de cada página:** comentario HTML invisible en el último bloque
  con la **fecha y hora reales de generación** del JSON (fijas, no Liquid `now`). Para el
  usuario, no para el cliente. NUNCA después del `}` final (rompería el JSON). Suma al sello
  de versión de arriba (v1.7). Documentado en SKILL.md + checklist.

## v1.10 — 2026-06-02
- **Paso 0 obligatorio: PLAN DE DIFERENCIACIÓN.** Antes de escribir JSON, la skill declara
  arquetipo, orden de secciones, hero, sección educativa, tipografía, efectos y color CTA,
  y DEBE divergir de los ejemplos y de las páginas previas (PLANTILLAS / las que muestre el
  usuario). Si arma varios en una sesión, cada uno pulsa palancas distintas. Convierte la
  REGLA #1 de "ojalá" a paso verificable. Anti-duplicado pasa a Paso 0.1.

## v1.9 — 2026-06-02
- **Matiz REGLA #2:** el WhatsApp va SIEMPRE verde `#25D366` (convención). El CTA puede ser
  verde también — no se confunden por forma/tamaño/posición/ícono. Si ambos verdes: CTA en
  verde de marca distinto y no pegados. Lo innegociable sigue: el CTA destaca sobre TODA la
  página (secciones/fondos/secundarios). Actualizado SKILL.md, colores-conversion.md, checklist.

## v1.8 — 2026-06-02
- **Modo actualización (UPGRADE PASS):** flujo formal para tomar un product.json ya
  generado y ponerlo al día con la versión actual de la skill (lee el sello, hace diff,
  aplica solo lo que falta sin romper lo que sirve, sube el sello). Documentado en SKILL.md.

## v1.7 — 2026-06-02
- **Sello de versión obligatorio:** el config center ahora inyecta un comentario HTML
  `<!-- Generado con GOLDEN SHOPIFY vX.Y · marca · fecha -->` (vars `GFS_VERSION`/`GFS_DATE`).
  Permite abrir cualquier página y saber con qué versión de la skill se hizo.
- Regla del sello documentada en SKILL.md. Al subir versión, actualizar `GFS_VERSION` por defecto.

## v1.6 — 2026-06-02
- Nuevo `componentes/landing-sin-distracciones.liquid`: oculta menú/header/footer y
  desactiva el link del logo, solo en el PDP, para retener al visitante (modo COD).
  También oculta el "skip to content". Documentado "Modo landing sin distracciones" en SKILL.md.

## v1.5 — 2026-06-02
- **REGLA #2 permanente:** el botón de compra SIEMPRE sobresale — máximo contraste,
  distinto del fondo/secciones y del botón de WhatsApp (verde). Marca verde → CTA rojo/naranja.
- Añadida "Jerarquía del CTA" en `colores-conversion.md` (mapa marca→CTA, realce, test de 1 vistazo).
- Chequeo del CTA agregado a `checklist-producto.md`.

## v1.4 — 2026-06-02
- **Preguntas iniciales ampliadas:** ahora pide PAÍS (define entrega), colores (con
  recomendación si el cliente no tiene), y WhatsApp para el botón.
- Nuevo `references/paises-entrega.md`: tiempos Guatemala (1-4 días) vs Colombia (3-7,
  con desglose preparación/tránsito/entrega). Regla: nunca mezclar países; preguntar si falta.
- Nuevo `references/colores-conversion.md`: recomendar el color que más vende por vertical
  (impulso de compra), 1 recomendado + 1 alternativa.
- Nuevo `componentes/whatsapp-flotante.liquid`: botón flotante WhatsApp real (sale del roadmap v2).

## v1.3 — 2026-06-02
- **REGLA #1 de diferenciación** añadida como principio central en SKILL.md.
- Nuevo `references/diferenciacion.md`: 8 palancas para que cada página sea distinta
  + chequeo antiespejo. Cada producto debe rediseñarse, no clonar el aspecto.
- Chequeo antiespejo agregado a `checklist-producto.md`.

## v1.2 — 2026-06-02
- **Análisis comparativo de las 5 plantillas** (producto-demo, marca-demo, Producto Demo, Producto Demo, verrugas).
- Añadido `references/arquetipos.md`: 3 arquetipos (Perfume / Salud lean / Vitalidad full)
  + matriz de qué componente activar por vertical.
- Extraído `references/componentes/sec-piramide.liquid` (pirámide olfativa 3D con tilt).
- Añadido `assets/related-products.premium.css.txt` (featured-collection premium de Producto Demo).
- Documentado el hero nativo `image_banner` (de Producto Demo) como opción de layout.
- Añadido este changelog + el ritual de auto-mejora en SKILL.md.

## v1.1 — 2026-06-02
- Consolidación: absorbió el oro de `golden-shopify` (archivada).
- Añadido `references/reglas-de-oro.md` (12 reglas + copy/legal COD + errores).
- Añadido `references/efectos-premium.md` (catálogo de snippets).

## v1.0 — 2026-06-02
- Creación. Base = PRODUCTO DEMO (`assets/product.base.json`). 17 componentes, adaptador de temas,
  releasit-cod, sistema, checklist. Ejemplos producto-demo (Shrine) + marca-demo (Dawn).

## G4.1 (2026-07-27, centro de mando)
- Fix de gobernanza: el chat COLAGENO recibió la skill TRUNCADA al invocarla (el contenido servido terminaba antes de la sección PROTOCOLO TEMA VIVO + MEDIA de la línea ~459) y trabajó toda la sesión sin el protocolo — incumplió el punto 4 (borró media sin inventariar; sin daño, por suerte). Solución: RESUMEN DURO de los 7 puntos insertado al TOPE del SKILL.md (tras el aviso de solo-lectura), con puntero a la sección completa. Lección de arquitectura: lo crítico va ARRIBA del archivo; el final puede no llegar.
## G4.1b — 2026-07-29 — Media: tema+descripción, poster obligatorio, GIF→MP4 (lección chat TOPPIK, parche 23,5→3,3 MB)
## G4.1c — 2026-07-29 — REGLA #3 con matiz PAUTA: display propio se queda; porcentajes-estudio, testimonios en imagen y atribución a terceros jamás (gaceta 4f p.3).

## G4.2 — 2026-08-07 — Límites duros de Shopify + receta Horizon/Pitch + fallback del CTA (fuente: chat un producto de cliente/un producto de cliente)
Paquete de hallazgos horneado por el Centro de Mando desde la entrada del chat un producto de cliente en la bandeja
(3 `FileSaveError` consecutivos en tienda real descubrieron límites que no están en la documentación oficial).
- **TOPE 50 KB por setting `custom_liquid` (aplica a TODOS los temas):** el guardado del template revienta
  con *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"*. Entró como
  punto 9 del RESUMEN DURO del SKILL.md y como **check obligatorio nro. 21 en `auto-check.md`**: medir cada
  valor `custom_liquid` en BYTES UTF-8 (no caracteres) y fallar si alguno llega a 50.000 (aviso desde 45.000).
- **Horizon/Pitch — 2 límites más (`horizon-bloques.md`, advertencia dura al tope):** `product-information`
  NO acepta bloques ajenos en su primer nivel (su esquema no declara `@theme`; ni `custom-liquid`, ni bloques
  privados con prefijo `_` declarados desde fuera). Se descubre solo con `FileSaveError` al guardar.
- **RECETA PROBADA Horizon/Pitch (`horizon-bloques.md`):** plantilla 100% secciones `custom-liquid` sin
  bloques · galería propia leyendo `product.images` · rejilla de 2 columnas por JS moviendo el DOM con
  re-armado en `shopify:section:load` · UNA sección por pieza (REGLA #5 + esquiva el tope de 50 KB) ·
  Product JSON-LD propio (la sección nativa ya no lo pone). Más la regla de conducta: nunca adivinar la
  estructura interna del `main` de un tema ajeno — pedir el `product.json` real o ir 100% custom-liquid.
- **REGLA PERMANENTE para TODA página (REGLA #2 del SKILL.md + `releasit-cod.md`):** el CTA lleva fallback
  al formulario nativo `/cart/add` si Releasit no está presente (espera ~1,5 s por inyección tardía y luego
  cae al flujo nativo). El botón siempre sobresale... y siempre FUNCIONA aunque la app falte.
- **Nota [DEUDA] visible en el SKILL.md (dos menciones de la base):** `assets/product.base.json` sigue en
  el orden de 17 secciones vs las 24 del embudo canónico G4.0 — pendiente de sesión dedicada. Hasta
  regenerarlo, el ORDEN canónico es la tabla del SKILL.md, no el base.

## G4.3 — 2026-08-07 — Componente "LO QUE ESTE PRODUCTO NO HACE" (cosecha del chat ESTUDIO 360 DENTAL un producto de cliente, Chile)
Repartido por el Centro de Mando desde la bandeja (orden de FER: "sin omitir detalle"). Invención del
estudio dental y probablemente lo más valioso que salió de él:
- **Componente estándar para verticales de SALUD**, descrito en el SKILL.md junto a `sec-disclaimer` /
  `sec-es-para-ti` como **obligatorio-recomendado**: una sección que declara el LÍMITE del producto con
  honestidad ("No repara una caries ya formada — eso lo hace el dentista. Sí cuida el esmalte y apoya la
  remineralización").
- **Racional probado en campo:** en una categoría donde los 5 competidores usaban odontólogo inventado,
  logos de Cruz Verde/Salcobrand/Paris como "distribuidores oficiales" y estadísticas sin estudio
  (95%/96%/97%/100%), **declarar el límite convierte la objeción "esto es una estafa" en la razón para
  comprar**: el único vendedor honesto de la categoría se queda con el cliente escéptico.
- **Funciona en tres soportes con el mismo mensaje:** sección de página, ángulo completo de pauta
  (5 textos) y respuesta pública en comentarios. Se maqueta como `custom-liquid` con el patrón de lista
  ❌ "no hace" / ✅ "sí hace" de `sec-es-para-ti`.
