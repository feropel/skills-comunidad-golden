# Changelog — GOLDEN ADS

## G6.10 — 2026-09-19 — CdM: la ley del flete derogada seguía en la tabla de modelos de pago
`references/12-unit-economics.md`, tabla COD contra pago anticipado: el costo de devolución decía
"flete de ida y vuelta". La ley vigente del dueño es de **un solo flete**: la devolución cuesta el
flete de devolución, igual o menor al de ida y nunca mayor, según la transportadora. Lo destapó
golden-verificador al convertir el agente golden-finanzas en skill, y la misma clase se encontró en
6 archivos del arsenal. Aquí era la única ocurrencia (barrido de "vuelta", "doble flete" y "dos fletes"
sobre la skill entera). Los scripts no la aplicaban: no hay flete multiplicado por dos.

## G6.9 — 2026-09-06 — Auditoría golden-skill-auditor: la cifra retractada seguía viva en el auto-check
**Hallazgo real con evidencia (auditoría AUDITA+ARREGLA), y era conocido:** G5.7 (2026-09-02) ya había
detectado y anotado como "hallazgo fuera de dominio, va a la bandeja" que `13-auto-check.md` seguía
pidiendo verificar *"Similarity >60% = supresión"* de Andromeda pese a que **G5.6 (2026-08-31) retractó
ese umbral** contra la fuente primaria de Meta (no aparece en su blog de ingeniería) y `23-salud-de-
senal-y-andromeda.md` ya lo tenía corregido desde entonces. Cuatro versiones (G5.7→G6.8) pasaron sin
que se cerrara el pendiente — la clase exacta que esta casa combate: *un número retractado en un
archivo y vivo en otro es una contradicción interna real, no cosmética*, porque un checklist de cierre
que sigue citando un umbral inexistente puede llevar a diagnosticar mal la diversidad de creativos de
una cuenta real.
- **`13-auto-check.md`**: retirado *"Similarity >60% = supresión"* de la lista de verificación; se deja
  explícito que ese umbral NO existe (retractado en G5.6) y no se usa de corte en ningún diagnóstico.
  Aprovechado el mismo cambio para quitar el único signo de interrogación de apertura del ítem (regla
  de escritura de la casa: cero signos de apertura en todo texto que la skill contenga).
- Verificado con un barrido de esos dos signos sobre toda la skill: **0 ocurrencias** tras el cambio
  (antes: 1).
- **Segundo hallazgo, misma auditoría:** el `SKILL.md` afirma en su propia sección "Sello de versión"
  que el número *"vive SOLO aquí y en el comentario GAE_VERSION"* — pero el texto visible decía
  `G5.7`/2026-09-02 mientras el comentario ya iba en `G6.8`. Reincidencia de la clase que G4.7 y G5.2
  ya habían cerrado antes (desfase entre el sello impreso y el real). Sincronizados los dos a `G6.9`.
- Auditoría ejecutada por `golden-skill-auditor`: inventario, lectura completa de los 36 archivos,
  validador oficial `agentskills validate` (exit 0) y `validar_arsenal.py` (COBERTURA 1 de 1, sana).
  Sello → **G6.9**.

## G6.8 — 2026-09-05 — Probar en los DOS sentidos delató mi propio arreglo
El Centro de Mando trajo la ley de la madrugada: **un detector hecho de patrones acusa al idioma, no
al defecto**, y por eso **se prueba en los dos sentidos: debe MORDER el caso malo y CALLAR ante el
bueno**. Aplicada al contador de columnas de G6.7, encontró que seguía roto.

- **Lo que se midió**: cuatro casos sobre una copia. `A` limpio → 5/40 ✅. `B` prosa inocente nueva →
  5/40 ✅ (calla). `C` una nota escrita con el mismo formato `**Etiqueta:**` que los bloques →
  **6/42** 🔴 sin que cambiara un solo dato. `D` columna sembrada → muerde ✅.
- 🔑 **La lección sobre mi propio arreglo**: en G6.7 detecté ese fallo y lo "arreglé" **reescribiendo
  mi nota**. Eso cura el síntoma en UN archivo y deja el instrumento roto para el siguiente que
  escriba al lado de la lista. *El arreglo es el instrumento, no el texto que lo esquiva.*
- **El arreglo real**: la lista va encerrada entre `<!-- COLUMNAS:INICIO -->` y `<!-- COLUMNAS:FIN -->`,
  y la cuenta **`scripts/contar-columnas.py`** — primer script de esta skill. Trae `--test` con los
  tres casos: prosa nueva, nota disfrazada y columna sembrada. Corrido: **calla en los dos buenos,
  muerde en el malo**. El script es LA FUENTE del número; la prosa solo lo repite.
- **Dos guardarraíles de edición escritos en el SKILL.md** (§AUTO-MEJORA), porque las 38 fábricas
  están editando sus `description` esta noche y este es el momento exacto de romperlo:
  1. La `description` mide **1000 de 1024**: quedan **24 caracteres**. Nombra tres plataformas, así
     que añadir disparadores de una desborda el total aunque el párrafo parezca corto. Validar
     **después** de tocarla, con RUTA ABSOLUTA. **1024 valida (duro) · ~1536 trunca (runtime)**.
  2. Toda cifra se cita desde la fuente que la mide, nunca a mano.

Validador oficial (ruta ABSOLUTA): **Valid skill, exit 0**.

## G6.7 — 2026-09-05 — La regla de la cifra se aplica a la propia skill (barrido completo)
Segunda vuelta del bucle de autocalificación. En G6.6 se escribió la ley *"donde haya cifra, se cita
la fuente que la mide"*. Aquí se **corrió esa ley sobre la skill entera**, y encontró cosas.

**Barrido de cifras vivas (todas medidas contra su lista, no contra la memoria):**
- ✅ **"40 columnas · 5 bloques"** (`19-golden-pro-preset.md`) — **CONFIRMADO**: 10+17+3+6+4 = 40.
  El archivo ahora lleva en la cabecera **cómo** se cuenta (los 17 salen de 15 nombres donde dos
  traen `(+costo)`; los 4 del bloque 5 son 3 clasificaciones + el identificador). El SKILL.md ya
  **no repite el número**: apunta a la lista.
- 🔴 **"26 columnas personalizadas + 6 mejoras"** (`18-columnas-ads-manager.md`) — **NO CUADRABA**.
  Medido: la lista tiene **36 entradas, 8 marcadas ➕**. El "26+6" venía heredado del PDF original;
  la lista creció y el encabezado no. Se sustituye por la lista y se deja la nota de que manda ella.
- 🔴 **"citada en 13 archivos de esta skill"** (`golden-copywriting`) — medido: **14**. Fuera el número.
- ✅ **"6 pruebas de coherencia"** — CONFIRMADO (`25-cuenta-sin-creativos.md`, PASO 4, "estas seis"),
  y ahora la mención en `26` **apunta al archivo**, que antes no lo hacía.

**Dos clases que salieron del propio trabajo:**
1. 🔑 **El contador se prueba SEMBRANDO.** Antes de creerle el "40", se metió una columna falsa en
   una copia: el conteo subió a 41. Un número limpio de un instrumento no probado no es un dato.
2. 🔑 **El instrumento se mide a sí mismo si se le deja.** La primera versión de la nota de conteo
   usaba el mismo formato `**Etiqueta:**` que los bloques, y el contador la leyó como un bloque más:
   devolvía **6 bloques y 43 columnas**. Se reescribió la nota sin ese formato. *Al medir algo,
   revisar que lo que escribes sobre la medición no entre en la medición.*

Validador oficial (ruta ABSOLUTA): **Valid skill, exit 0**.

## G6.6 — 2026-09-05 — El historial sale del cuerpo y caen tres numeros clavados
Mandato de FER de autocalificarse y automejorar. El Centro de Mando midió el defecto: **127 de 417
líneas del SKILL.md (30%) eran comentarios de historial** — actas que se cargan en CADA activación
sin decidir nada.

- **Migración**: todos los bloques `GAE_VERSION` históricos se archivaron **verbatim** en este
  changelog (sección "ARCHIVO · sellos GAE_VERSION históricos"); en el cuerpo queda **solo el sello
  vigente**. SKILL.md **417 → 300 líneas**, comentarios **127 → 10**.
- **Tres números clavados que la migración destapó** (y que ya no cuadraban):
  1. "17 reglas" en `reglas-de-oro.md` — **son 21**.
  2. **"15 copys" como estándar** en el SKILL.md y en `26-intake-montar-campana.md` — el techo
     **MEDIDO** de la interfaz es **5 textos + 5 títulos + 1 descripción = 11**, y ese techo se midió
     en "Crear anuncio y mensaje": en otro objetivo **se vuelve a medir, no se supone** (`29`).
  3. Un conteo de líneas mal reportado al CdM (dije 183, son **181**).
- 🔑 **LA CLASE:** *el acta que no se activa no vive en el cuerpo* — y **un número escrito a mano
  caduca solo**. Donde haya una cifra, se cita **la fuente que la mide**, no la cifra.
- Validador oficial `agentskills validate` (ruta ABSOLUTA): **Valid skill, exit 0**.

## G6.5 — 2026-09-05 — La regla del navegador se vuelve una CLASE
Ajuste pedido por el Centro de Mando al asumir su parte del choque, **y su observación resultó valer
más que el ajuste**. La regla 20 ya decía "avisar que se suelta", pero como coletilla. Ahora:

- **El turno es de DOS TIEMPOS explícitos**: preguntar antes de abrir, y 🔴 **DECIR que se suelta al
  terminar**. El segundo es el que se olvida — y sin él **el turno nunca se cierra**, que es
  exactamente como ocurrió el choque.
- 🔑 **LA CLASE, en palabras del CdM:** *el reparto se hace sobre el recurso que tiene NOMBRE, y el
  que no lo tiene queda sin repartir.* Se repartió "la cuenta de pauta" (que tiene id) y **nadie
  repartió "el navegador"**, que no lo tiene. → Antes de trabajar en paralelo, **listar los recursos
  compartidos SIN nombre propio** y repartirlos igual: navegador, sesión de Shopify, token de un
  workspace, terminal, archivo que dos rutinas escriben. **Si un recurso no aparece en el reparto,
  no está libre: es que nadie lo miró.**

Aplica mucho más allá de la pauta, y por eso se escribe como clase y no como caso.

**Candida: NO se reescriben los copys** — decisión del CdM con criterio que se registra: la campaña
está ARCHIVED con gasto cero, FER la declaró prueba y la cerró él mismo. Rehacer 60 copys para una
campaña archivada es trabajo con destino inexistente, **y además se harían contra un creativo que va
a cambiar** (las cuatro imágenes llevan jengibre, que no está en la fórmula). **Condicionado, no
cancelado:** si FER relanza, se rehacen en el mismo movimiento que las piezas, con la compuerta de
`29` puesta y **contra el creativo nuevo**. Sello → **G6.5**.

## G6.4 — 2026-09-05 — Lecciones de la prueba Candida/CP6 (5 fallas + los aciertos blindados)
**FER declaró que toda la corrida de Candida en CP6 era una PRUEBA de esta skill** y pidió aciertos,
fallas y que no se repitan. Fila del Centro de Mando. **La prueba cerró con gasto CERO.**

**FALLA 1 · Se degradó de MCP a navegador SIN ejecutar el intento.** Se afirmó *"el conector no
expone `asset_feed_spec`"* **leyendo el schema, no lanzando la llamada**, y se pasó al navegador.
→ **REGLA 19**: ejecutar el intento, **pegar el error del servidor**, y **declararle el bloqueo al
usuario** en vez de auto-degradarse en silencio. Un atajo no declarado convierte una limitación
**supuesta** en un hecho que nadie vuelve a cuestionar.

**FALLA 2 · Los copys salieron malos.** Palabras de FER: *"colocaste unos copies muy malos, sin
emojis, corticos, y así no debe ser"*. Causa: **no se invocó `golden-copywriting` ni se declaró** que
se iba sin ella — pese a que esta skill ya lo exigía. Salió ficha técnica ("Apoyo digestivo diario",
"60 cápsulas por frasco"). → **`29-compuerta-de-copys.md` (NUEVO)** con 4 compuertas:
`golden-copywriting` **OBLIGATORIO** · **emojis obligatorios** (cero emojis = no entregable) · **hook
en los primeros ~40 caracteres** (lo que se ve antes del "ver más") · **125/40/25 es TECHO, no
objetivo** — escribir corto para cumplir es el error.

**FALLA 3 · El "estándar de 15 copys" NO existe en la interfaz.** MEDIDO por DOM, tipo "Crear anuncio
y mensaje": "Agregar opción" llega a **5 en Texto principal** y **5 en Título**, y en **Descripción
ese botón NO EXISTE**. Techo real: **5+5+1 = ONCE**. → Corregido en `25`, `26`, el checklist y la
regla 21. ⚠️ **Escrito que NO se generaliza a otros objetivos sin medirlos allí** — generalizar sin
medir es justo lo que creó la regla equivocada.

**FALLA 4 · No se inventarió lo que el anuncio YA tenía.** Los cuatro traían un texto y un título
puestos por API; al agregar encima, el viejo quedó de opción 1 y no se declaró hasta el final.
→ Obligación de inventariar antes de escribir y **decir qué copys quedan FUERA** cuando el techo
obliga a elegir.

**FALLA 5 · Escritor único del NAVEGADOR** (falla que el CdM asumió como suya y que igual entra
aquí): dos sesiones entraron por el mismo Chrome. Se destruyó el grupo de pestañas **4 veces**, costó
**2 borradores** de anuncio, y en un reintento un texto se insertó DENTRO de otro dejando la frase
partida — **un anuncio quedó sin copys**. → **REGLA 20**: preguntar si otra sesión está usando el
navegador y avisar cuando se suelta. **Ahí no hay bloqueo ni aviso**: la otra sesión simplemente se
queda sin pestañas.

**✅ ACIERTOS BLINDADOS en `29` (lo que funciona también se pierde si no se escribe):**
- **Presupuesto COP ×1 releído del servidor**: $1.000.000/día correcto, sin el error de los centavos.
- **Multianunciante OFF** aplicado y verificado en los cuatro anuncios.
- **El copy nació del CREATIVO REAL** abierto en vista previa, **no del nombre del conjunto** — por
  eso el de la pieza antes/después habla de transformación y el de la mixta nombra a ellos y ellas.
- **El ingrediente falso también entra por la IMAGEN** (jengibre en las cuatro piezas de un producto
  que no lo lleva): la imagen se revisa con el mismo rigor que el texto.

**Aviso lateral horneado:** una cuenta publicitaria **puede tener campañas de otros proyectos** —
CP6 tenía archivadas de otro producto, varias CON gasto. Al barrer una cuenta, **no asumir que lo que
hay dentro es del producto que se trabaja**. Sello → **G6.4**.

## G6.3 — 2026-09-03 — El teardown de `golden360` se CONSUME, no se repite
**Aviso del Centro de Mando, verificado en la hermana antes de hornear:** `golden360` **R2.0**
(2026-09-03) tiene una **Fase 5B** real — `golden-video-teardown` entra en la ruta **entre producir
los creativos (Fase 5) y escribir los copys (6-7)**. Comprobado en su `SKILL.md:216` y su tabla de
hijas; no se aceptó de palabra.

**Qué cambia para esta skill:** cuando el encargo llega por la ruta 360, el video **ya viene
desarmado** (beat sheet segundo a segundo, ángulo, hook y copy quemado en pantalla). Repetir el
análisis cuesta tiempo y créditos y, peor, **arriesga contradecir el análisis que guió la
producción del creativo**.

- **`25-cuenta-sin-creativos.md` Paso 2**: nota al inicio — buscar el teardown en el expediente del
  producto **ANTES** de analizar nada; si está, la ficha del creativo se rellena con él y se pasa
  directo al Paso 3 (escribir los copys).
- **Bloque de requisitos del `SKILL.md`**: la fila de `golden-video-teardown` lo dice, y se anota la
  ruta real del binario **`golden-transcribe` (`~/.golden/bin/`)**.

> La regla de fondo no cambia, se refuerza: **el copy nace del video que se escuchó.** Lo nuevo es
> que a veces ya lo escuchó una hermana, y entonces se le cree a ella en vez de volver a empezar.

**De paso**, los 3 avisos que este chat devolvió al validador del CdM quedaron arreglados en origen
(resolver contra `~/.golden/bin/`, descontar nombres de archivo y anclas de índice) y **horneados en
su autoprueba, que pasó de 23 a 26 casos** — un arreglo sin su caso de prueba vuelve en tres
versiones. golden-ads: **1 de 1, cero avisos**. Sello → **G6.3**.

## G6.2 — 2026-09-03 — Requisitos DECLARADOS (la skill deja de asumir a sus hermanas)
**Fila del Centro de Mando**, bajo la ley que dictó FER: *todo lo que la skill necesite del usuario
o del entorno se declara ANTES, cerca del principio del SKILL.md, y se pide AL CORRER si falta*.

**El hueco, medido:** la skill citaba hermanas en decenas de archivos y **declaraba CERO requisitos**
(`grep -i "requisito|dependencia" SKILL.md` = 0). Conteo real de citas:
`golden-copywriting` **13 archivos** · `watch` 7 · `golden-investigacion-mercado` 6 ·
`golden-ugc-avatar` 6 · `golden-video-teardown` 5 · `golden-dropi-analisis` 4 ·
`golden-meta-ads-analysis` 3. Quien instalara golden-ads suelta se quedaba con una skill que pide
otra que no tiene, **y lo descubría a mitad de un encargo**.

**Nuevo bloque "QUÉ NECESITA ESTA SKILL"**, justo después del rol y antes de las reglas de oro:
- **Del entorno:** MCP de Meta (si falta → informe o testeo, y `27` para conectarlo; nunca inventar
  que la cuenta respondió) y los datos del negocio para el breakeven (si faltan → `[PENDIENTE]` y
  ranking relativo, no veredicto absoluto).
- **Las 6 hermanas**, cada una con **qué aporta** y **qué pasa si no está**. Ninguna bloquea.

**Matiz que aportó el CdM y se consagra:** una dependencia entre skills **NO es una API key**. No se
le pide al usuario que la pegue: se le dice **cuál hermana falta y con qué se degrada el trabajo**.
Caso concreto de `golden-copywriting`: sin ella se escriben **los 15 copys igual** (respetando
125/40/25 y compliance) pero **sin framework**, y **se declara** — *"copys escritos sin el motor de
frameworks"*. **Prohibido fingir que se aplicó un framework que no se pudo leer.**

**Para el reparto:** `golden-copywriting` **va junto con** `golden-ads`. Es la única cuya ausencia se
nota en casi todos los encargos, porque los 15 copys aparecen en casi todos. Sello → **G6.2**.

## G6.1 — 2026-09-03 — La `description` vuelve DENTRO de la especificación (1.444 → 1.000)
**Hallazgo de arsenal**, medido en este chat y **confirmado por el Centro de Mando con medición
independiente**: de las ~188 skills instaladas, **34 pasan del tope de 1.024 caracteres** que fija la
especificación de Agent Skills — y **32 de esas son de la casa**. Que las diez peores del arsenal
entero sean todas nuestras es el dato que más dice. `golden-ads` estaba en **1.444**.

**Límites verificados en vivo** (agentskills.io/specification, no de memoria): `description` **1–1024
obligatorio** · `name` 1–64, minúsculas, sin guion inicial/final ni dobles, **debe coincidir con la
carpeta** · `compatibility` 1–500 · **el cuerpo NO tiene tope duro** ("under 500 lines" y los 5.000
tokens son recomendaciones).

**Qué se hizo:** description recortada a **1.000** con el criterio del CdM — **los DISPARADORES
primero**, porque los del final son los que se pierden, y **lo explicativo BAJA AL CUERPO**, que no
tiene tope. La instrucción de *"si te pasan un video, súbelo, analízalo viéndolo Y escuchándolo, y
escribe los copys de ESE video, nunca genérico"* pasó del disparador al bloque de montar campaña.
Se conservaron los 15 disparadores en las palabras reales de FER.

**Distinción honesta que aportó el CdM y se adopta** (para no vender certezas):
- **1.024 = tope de VALIDACIÓN** de la spec.
- **~1.536 = TRUNCADO EN RUNTIME**, medido por esta misma skill el 2026-08-07.
- Son **mecanismos distintos**: las dos mediciones son ciertas a la vez.
- Que un ZIP sea **rechazado al distribuir** es **plausible y NO medido**.
- El **"tope de 200 en claude.ai"** que circuló **no se adopta**: sin fuente verificada es rumor, no
  límite (el CdM lo buscó en memoria y no está registrado en ningún lado).

**CAUSA RAÍZ del fallo de detección** (ya en manos del CdM, que es el dueño): `golden-skill-auditor`
**MIDE** la description (`inventario.sh:293-295`) pero **NUNCA la compara** — `1024` aparece **cero
veces** en sus scripts y cero en `rubrica.md` / `estandares-golden.md`. Por eso skills selladas ORO
pasaron fuera de norma sin que saltara nada. Es `reference_familia_trampas_de_conteo` en su forma más
pura: **el arreglo es el INSTRUMENTO, no la buena intención** — el mismo patrón que el presupuesto
×100 de hoy (se medía, no se comparaba). El arreglo de clase que tomará el CdM es **adoptar el
validador oficial `skills-ref validate`**, no codificar el número a mano: así los topes futuros
llegan gratis en vez de envejecer con nuestra interpretación. Sello → **G6.1**.

## G6.0 — 2026-09-03 — Los 3 objetivos de campaña, resueltos de una vez
**Reclamo directo de FER:** *"objetivo son: tráfico, interacción, venta. Tú ya debes saber todo esto,
no debería estar diciendo esto"*. Tenía razón: es dato de plataforma, no algo que se le pregunte.

**El hueco, medido:** la skill nombraba `OUTCOME_SALES`/`OUTCOME_ENGAGEMENT`/`OUTCOME_TRAFFIC` de
pasada en `05-publicar-mcp.md`, sin tabla ni criterio — y el intake de `26` reducía el objetivo a
**dos** opciones ("venta web o conversaciones de WhatsApp"), **dejando TRÁFICO fuera**.

**`28-objetivos-de-campana.md` (NUEVO)** — tabla de decisión: lo que dice el usuario → `objective` →
`optimization_goal` → `promoted_object`/destino → la métrica con que se mide. Más:
- **VENTA** es el default cuando el pixel tiene señal de Compra (requisito duro).
- **INTERACCIÓN** optimiza a **que escriban, no a que compren**: el costo por conversación puede
  verse hermoso y el negocio perder si el bot no cierra → Chatea PRO debe **devolver la conversión a
  Meta** o Meta aprende de chats, no de ventas.
- **TRÁFICO** es el más barato y el que menos vende: para probar creativo o calentar pixel. Si
  alguien pide tráfico esperando ventas, **hay que decírselo**.
- `LANDING_PAGE_VIEWS` antes que `LINK_CLICKS` (el clic dice que tocaron; la LPV, que cargó).
- **Cambiar el objetivo obliga a REHACER la campaña**, no a editarla (editar reinicia el aprendizaje).
- Los otros 3 enums (`LEADS`, `AWARENESS`, `APP_PROMOTION`) quedan declarados como existentes y fuera
  del default de Golden.

Enums verificados hoy contra la Marketing API de Meta (`ad-campaign-group`). `26` corregido para
ofrecer los **tres**. Sello → **G6.0**.

## G5.9 — 2026-09-03 — Conectar el MCP de Meta + 🔒 candado de presupuesto
**Origen:** aviso del chat "🎯 EL CARTEL DEL CHAT" (FER reparte la skill en el bootcamp).
**Verificado por esta fábrica contra la fuente autoritativa ANTES de hornear** — nada se aceptó de
palabra: `developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/*`
(actualizado 14-jul-2026) y `facebook.com/business/help/1456422242197840`, leídas en vivo hoy.

**`27-conectar-mcp-meta.md` (NUEVO)** — la skill asumía "el MCP está conectado" y nunca decía cómo:
- URL oficial **`https://mcp.facebook.com/ads`** (confirmada en las dos páginas).
- **Vía A sin app propia** (Meta ads AI connectors, la del alumno) y **Vía B con app propia** con el
  **comando exacto de Claude Code**: `claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads`.
- Los **7 permisos textuales** (`ads_mcp_management`, `ads_read`, `ads_management`,
  `catalog_management`, `business_management`, `pages_show_list`, `instagram_basic`).
- El paso de **verificación** que nadie hace: preguntarle al agente qué herramientas tiene.

**🔒 HALLAZGO PROPIO (no venía en el aviso) y es lo que más plata protege:** Meta permite fijar
**reglas por cuenta en Business Suite → Settings → Integrations → Ads MCP server**, y **el servidor
MCP las hace cumplir**: bloquear "Create campaigns", bloquear "Edit or set budget", y sobre todo
**"Budgets set above this amount" = un TECHO MÁXIMO**. Con un techo puesto, el incidente del mismo
día ($50.000 pedidos → $5.000.000 puestos) **habría sido rechazado por Meta**. Se recomienda dejar
techo en toda cuenta operativa. Es el cinturón que acompaña al airbag de `reglas-de-oro.md` §5.

**Meta confirma dos doctrinas de la casa:** *"All ads are paused by default until you set them
live"* y *"any actions taken on your behalf require your authorization"*. Y desmiente el miedo al
baneo: usar el MCP no pone la cuenta en riesgo; los baneos vienen de violar políticas de anuncios.

**Correcciones al aviso recibido (se documentan para no propagar el error):**
- La `description` **medida** son **1.766 caracteres**, no 350 — error de factor 5.
- Clientes soportados **oficialmente por Meta**: ChatGPT, Claude, Claude Code y Perplexity.
  **Cursor y Codex NO aparecen** en la lista oficial.
- **No se encontró** en las páginas oficiales ni la advertencia de *prompt injection* ni los alcances
  llamados "Read"/"Manage". Quedan **rotulados como no verificados** en el archivo, en vez de
  atribuírselos a Meta. Lo que sí existe es el control por ACCIÓN descrito arriba.

**Description recortada de 1.766 → 1.442 caracteres.** La propia skill documentó el 2026-08-07 un
tope de ~1.536 y que pasarse **trunca las frases finales** (que dejan de disparar); había vuelto a
pasarse al ir sumando triggers. Se conservaron todos los disparadores clave y se sumó
"cómo conecto mi cuenta de Meta". **No se adoptó** la versión de 172 caracteres propuesta para el
ZIP: degradaría el disparo en Claude Code, que es donde se usa a diario. Sello → **G5.9**.

## G5.8 — 2026-09-03 — INTAKE del pedido "crea una campaña de X con presupuesto Y"
Encargo directo de FER tras **3 fallas de campo el mismo día**: presupuesto puesto 100 veces más
alto, campaña entregada sin los 15 copys, y creativo que nunca se subió al anuncio.

**Diagnóstico honesto antes de tocar nada** (grep sobre la skill):
- El **presupuesto** ya estaba arreglado (`reglas-de-oro.md` §5 + `13-auto-check`, mismo 2026-09-03).
- El **creativo + 15 copys** ya estaban cubiertos por `25-cuenta-sin-creativos.md` (mismo día).
- **El hueco REAL era el INTAKE**: cero menciones en toda la skill. Cada chat improvisaba qué pedir.

**Cambios:**
- **`26-intake-montar-campana.md` (NUEVO)**: los 3 campos obligatorios (objetivo · producto ·
  presupuesto) que **se preguntan juntos, una sola vez, si faltan**; qué NO se pregunta (autonomía:
  ABO/CBO, edades, público, naming) y qué se deduce solo (cuenta, moneda, pixel, página); la
  compuerta del presupuesto resumida con su testigo; el enlace con la **investigación previa** (los
  ángulos = los conjuntos, adaptados al creativo); y el ORDEN completo hacia `25` → `05` → `24` → `13`.
- **SKILL.md**: bloque visible arriba (antes de "RUTA SEGÚN DATOS") + entrada en el mapa.
- **Escrito el tope MEDIDO que explica "no me sube los 15 copys"**: `ads_create_creative` no expone
  `asset_feed_spec` → por API salen **1+1+1**; los 15 se entregan igual y se cargan en el panel,
  y **se reporta como pendiente**, nunca se callan ni se recortan.

**Descartado en el camino (se documenta para que no se repita):** se empezó un
`23-montar-campana-completa.md` que (a) **colisionaba de número** con `23-salud-de-senal-y-andromeda.md`,
(b) duplicaba `25`, y (c) citaba `ads_creative_upload_image`/`_video`, **deprecadas**. Se borró antes
de sellar. Lección: en una skill que editan varios chats, **listar `references/` antes de crear un
archivo numerado** y leer el vecino antes de escribir doctrina nueva. Sello → **G5.8**.

> Fuente única de versión/fecha de la skill (ver reconciliación en G4.7). `SKILL.md` solo refleja el
> número vigente en su sello; el detalle completo de cada cambio vive aquí.

## Índice
- [G6.5 — 2026-09-05 · La regla del navegador se vuelve una clase](#g65--2026-09-05--la-regla-del-navegador-se-vuelve-una-clase)
- [G6.4 — 2026-09-05 · Lecciones de la prueba Candida/CP6](#g64--2026-09-05--lecciones-de-la-prueba-candidacp6-5-fallas--los-aciertos-blindados)
- [G6.3 — 2026-09-03 · Consumir el teardown de golden360](#g63--2026-09-03--el-teardown-de-golden360-se-consume-no-se-repite)
- [G6.2 — 2026-09-03 · Requisitos declarados (dependencias entre skills)](#g62--2026-09-03--requisitos-declarados-la-skill-deja-de-asumir-a-sus-hermanas)
- [G6.1 — 2026-09-03 · description dentro de la spec (1.444 → 1.000)](#g61--2026-09-03--la-description-vuelve-dentro-de-la-especificación-1444--1000)
- [G6.0 — 2026-09-03 · Los 3 objetivos de campaña](#g60--2026-09-03--los-3-objetivos-de-campaña-resueltos-de-una-vez)
- [G5.9 — 2026-09-03 · Conectar el MCP de Meta + candado de presupuesto](#g59--2026-09-03--conectar-el-mcp-de-meta--candado-de-presupuesto)
- [G5.8 — 2026-09-03 · INTAKE del pedido de campaña](#g58--2026-09-03--intake-del-pedido-crea-una-campaña-de-x-con-presupuesto-y)
- [G5.7 — 2026-09-02 · UTM y atribución bajan al archivo (REGLA 18 + references/24)](#g57--2026-09-02--utm-y-atribución-bajan-al-archivo-regla-18--references24)
- [G5.6 — 2026-08-31 · Corrección Andromeda verificada contra fuente primaria](#g56--2026-08-31--corrección-andromeda-verificada-contra-la-fuente-primaria-de-meta)
- [G5.5 — 2026-08-27 · Corrección medida EMQ (sellada en SKILL.md)](#g55)
- [G5.4 — 2026-08-26 · references/23 salud de señal + Andromeda (sellada en SKILL.md)](#g54)
- [G5.3 — 2026-08-24 · Barrido total del arsenal (CdM)](#g53--2026-08-24--barrido-total-del-arsenal-ordenado-por-fer-vía-centro-de-mando)

## G5.7 — 2026-09-02 · UTM y atribución bajan al archivo (REGLA 18 + references/24)

**Encargo directo de FER**, textual: *"Nosotros estamos haciendo unas campañas y colocamos un UTM
para que pueda enviar esa información de dónde vino la venta. Debe estar en la skill de MetaAds"*.
Ratificación retroactiva por la vía de `reference_skill_sin_fabrica_dueno_centro_mando`: encargo
directo de FER + sección AUTO-MEJORA presente + ritual completo con escritura de prueba rechazada.
Fábrica de esta skill = CENTRO DE MANDO (`REGISTRO-FABRICAS.md`, "por ley").

### El hueco, medido antes de escribir
`grep -rn -i "utm\|url_tags"` sobre toda la skill: **0 reglas**. Solo dos menciones de pasada —
`changelog.md` G5.3 y `referencia-externa-ctwa-cod-panama.md`— y ambas dicen lo mismo: que la ley
del UTM *"vive en la memoria Golden, no en este SKILL.md"*. O sea que la propia skill llevaba desde
el 24-ago documentando su propio hueco sin taparlo. Regla hermana que lo obliga: **"la regla de
entorno baja al archivo"** (canonizada 2026-08-23) — una norma que solo vive en memoria debe estar
escrita DENTRO de la skill que la ejecuta.

Consecuencia práctica del hueco: `05-publicar-mcp.md` montaba campaña→conjunto→creativo→anuncio sin
nombrar el UTM una sola vez. **Todo anuncio montado con esta skill nacía ciego** y nadie lo notaba
al entregar, porque tampoco estaba en el auto-check ni en el checklist de cierre.

### Qué se hizo
- **NUEVO `references/24-utm-atribucion.md`** — esquema oficial con macros, tabla de qué lleva cada
  parámetro y para quién, las dos rutas (CTWA vs landing), cómo se pone, cómo se verifica y quién lo
  consume aguas abajo (snippet del tema, `resolver_atribucion.py`, `lib/atribucion.ts`).
- **REGLA 18** en `reglas-de-oro.md` (canónica, 17 → 18) y en el resumen de reglas del `SKILL.md`.
- Citas operativas donde de verdad se dispara: `05-publicar-mcp.md` (paso 4 + "Nunca"),
  `13-auto-check.md` (Publicación), `17-entrega.md` (nivel anuncio del informe full), checklist de
  cierre y mapa de archivos del `SKILL.md`.

### La fuente del esquema: los montajes reales, NO el contrato viejo
Se consagra lo que **está puesto hoy en las campañas** (`PROYECTOS/LECOTERRA/campanas/
MONTAJE-CP1-2026-07-25.md` y `MONTAJE-CP1-OPEN7-2026-08-14.md`, declarados verificados en vivo):

    utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}&utm_id={{ad.id}}

**El id va en `utm_id`; `utm_content` lleva el NOMBRE del anuncio, a propósito** ("dice qué video
vendió"). Un contrato anterior del CdM (2026-08-14) decía `utm_content={{ad.id}}` y **no es lo que
se montó**; la divergencia es exactamente el incidente `adOPEN` del 26-ago (orden 86907080, $259.801
acreditados a un anuncio inexistente). El archivo lo deja explícito para que nadie "corrija" el
montaje hacia el contrato muerto, y ata el cambio del esquema al cambio del lector.

### Verificado hoy contra la fuente autoritativa
Relectura de los **esquemas vivos del MCP de Meta**: ni `ads_create_ad` ni `ads_create_creative`
exponen `url_tags`. Confirma la medición del 14-ago y hace que la advertencia sea presente, no
histórica: **por MCP el anuncio nace sin UTM y hay que pegarlo en la UI antes de activar.**

### Rotulado SIN VERIFICAR (no se promete)
- `ads_update_entity` con `entity_type:"ad"` y `fields:{"url_tags":"..."}` como vía por MCP:
  `url_tags` sí es campo real del objeto Ad en la Marketing API, pero el MCP rechaza campos que no
  reconoce y **esto nunca se ha probado**. Escrito como candidato a probar en UN anuncio y releer.
- **La captura positiva por el camino LANDING sigue sin verificarse.** Lo único comprobado contra la
  API de Meta es el camino nativo CTWA (ad `120249805036590118`).
- Que el snippet corregido esté pegado en el `theme.liquid` VIVO: no se pudo comprobar, la conexión
  de Shopify está caída (switch-shop revocado).

### Hallazgo fuera de dominio (va a la bandeja, no se toca aquí)
`13-auto-check.md` todavía pide verificar *"Similarity >60% = supresión"* de Andromeda — **G5.6 lo
retractó** por no estar en la fuente primaria de Meta, pero solo lo corrigió en `23` y en el sello;
el auto-check quedó sin sincronizar. Es la misma clase de desfase que el ledger ya castigó tres
veces. No se corrige en esta corrida: no es el dominio de este encargo.

## G5.6 — 2026-08-31 · Corrección Andromeda verificada contra la fuente primaria de Meta
**Origen:** hallazgo del chat FILTRO, que fue a la fuente primaria; el CdM (dueño por ley de golden-ads) la leyó
en vivo y ejecutó la corrección. **Fuente:** blog de ingeniería de Meta, "Meta Andromeda", 2026-12-02, leída
entera el 2026-08-31.
- **RETIRADO** el "Similarity Score >60% = supresión de recuperación" que traía `references/23` (control 6) y el
  sello GAE_VERSION G5.4. Ese umbral NO aparece en el blog de Meta; venía de terceros (agencias / `claude-ads`).
- **CONSAGRADO** lo que la fuente SÍ sostiene: Andromeda es RECUPERACIÓN (primera etapa), selecciona de decenas
  de millones a unos pocos miles → **decide quién compite, no quién gana** (el ranking posterior decide el ganador);
  cada anuncio es un embedding precomputado del creativo en un índice jerárquico → el creativo determina elegibilidad.
- **Cifras de Meta añadidas con su condición:** +6% recall, +8% calidad, +22% ROAS (SOLO anunciantes que no usaban
  Advantage+ creative y activaron targeting por IA), +7% conversiones con generación de imagen, 1M+ anunciantes /
  15M anuncios en un mes.
- **NO consagrado:** "el primer frame es targeting" — plausible pero no está en la fuente primaria; queda como
  observación de mercado marcada, en ninguna skill como criterio.
- **Alineación de sello:** G5.4 (GAE_VERSION) y G5.5 (comentario de EMQ) estaban desalineados con la línea Versión
  (que seguía en G5.4). Este cambio lleva las tres caras a G5.6 y añade al índice del changelog las entradas G5.4 y
  G5.5 que faltaban.

- [G5.2 — 2026-08-24 · Sello único + rescates](#g52--2026-08-24--auditoría-golden-skill-auditor-sello-único--rescates)
- [G5.1 — 2026-08-23 · Estándar 9 (Centro de Mando)](#g51--2026-08-23--estándar-9-centro-de-mando)
- [G5.0 — 2026-08-21 · Auditoría: examples/ → references/, ledger fusionado](#g50--2026-08-21--auditoría-golden-skill-auditor-examples--references-ledger-fusionado)
- [G4.9 — 2026-08-18 · CAPA HUMANA parte 2](#g49--2026-08-18--capa-humana-parte-2-redes-patrones-y-sondeo-de-producto)
- [G4.8 — 2026-08-18 · CAPA HUMANA](#g48--2026-08-18--capa-humana-audiencia-momento-y-mensaje-con-corazón)
- [G4.7 — 2026-08-11 · RED SINÁPTICA + reconciliación de sello](#g47--2026-08-11--red-sináptica-puente-a-la-transcripción-local-de-creativos--reconciliación-de-sello)
- [G4.5 — 2026-08-07 · Cosecha dental Chile](#g45--2026-08-07--cosecha-del-chat-estudio-360-dental-cavity-healing-chile-vía-centro-de-mando)
- [Notas menores — 2026-07-30 / 2026-08-02](#notas-de-versión-menores-no-selladas--2026-07-30-y-2026-08-02)
- [G4.6 — 2026-07-27 · Golden NO es solo contra entrega](#g46--2026-07-27--corrección-de-fondo-golden-no-es-solo-contra-entrega)
- [G4.4 — 2026-07-18 · Aclaración Modo A/B](#g44--2026-07-18--aclaración-la-datahistórico-es-la-excepción-producto-nuevo--modo-b-por-default)
- [G4.3 — 2026-07-18 · Aprendizajes Le'côterra](#g43--2026-07-18--aprendizajes-de-campo-lecôterra-cod-cuidado-personal-colombia)
- [G4.2 — 2026-07-09 · Auditoría A-Z + seguimiento](#g42--2026-07-09--auditoría-a-z--playbook-de-seguimiento-post-lanzamiento)
- [G4.1 — 2026-07-02 · Replicación GOLDEN PRO por URL](#g41--2026-07-02--replicación-golden-pro-por-url-validada-en-vivo-en-cp1cp5cp6)
- [G4.0 — 2026-07-02 · Semáforo de metas](#g40--2026-07-02--semáforo-de-metas-por-métrica--guía-imprimible-golden-pro-v11)
- [G3.9 → G3.0 — 2026-06-25 · construcción del preset y validación en vivo](#g39--2026-06-25--golden-pro-preset-único-construido-en-vivo-hookhold-rate-creadas)
- [G2.0 — 2026-06-25 · rename + Meta/TikTok/Google + full-funnel](#g20--2026-06-25--rename-a-golden-ads--metatiktokgoogle-completos--full-funnel)
- [G1.0 — 2026-06-25 · versión inicial](#g10--2026-06-25--versión-inicial-centro-de-comando-de-pauta)

## G5.8 — 2026-09-03 — Cuenta sin creativos: subir el medio, analizar el video, copy coherente

**Orden de FER:** *"si la cuenta publicitaria no tiene creativos, podamos montarlo, una vez te lo
dé el chat, analices el video y crees los copys que corresponden al video y que sea coherente"*.

**Hueco que lo motivó:** montando `LECOTERRA - VENTA - OPEN 1` en GOLDEN CP6 COL se reutilizaron
videos viejos y **no se subió nada nuevo**; FER lo notó. `15-creativos-produccion.md` ya tenía el
árbol TIENE/NO TIENE media, pero **no decía cómo meter el medio en la cuenta**, ni con qué
herramienta analizar el video, ni cómo comprobar que el copy le corresponde.

**NUEVO `references/25-cuenta-sin-creativos.md`:**
- **Paso 0** — medir la biblioteca (`ads_get_ad_videos` / `ads_get_ad_images`; resultados
  parciales: campo ausente ≠ vacío). "Cuenta vacía" casi nunca es cierto — CP6 no lo estaba.
- **Paso 1** — las **3 vías** para meter el medio con `ads_creative_upload_media` (las herramientas
  `upload_image`/`upload_video` están DEPRECADAS): URL pública (Claude solo), archivo del Mac
  (**el usuario elige en un selector** — tope real), y referenciar un `video_id` de otra cuenta
  (Meta lo copia sin resubir).
- **Paso 2** — 🔴 **analizar antes de redactar**: mirar fotogramas NO basta, en un reel hablado los
  subtítulos quemados salen una palabra por cuadro. `golden-video-teardown` / `watch` +
  `golden-transcribe`. Ficha obligatoria de 7 campos antes de escribir.
- **Paso 3** — 5+5+5 pegados a esa pieza, con el estándar 125/40/25.
- **Paso 4** — **prueba de coherencia de 6 puntos** (mismo producto, mismo interlocutor, aporta en
  vez de subtitular, datos que coinciden, reglas de marca del producto, compliance Meta).
- **Paso 5** — `ads_get_ad_preview` y **entregar el `preview_url`**; avisar que
  `IN_PROCESS`/`PENDING_REVIEW` es normal (si no, el usuario cree que no se montó nada).
- **Topes del MCP medidos**: CTWA no se puede crear por API (con `link` lo rechaza, sin `link`
  descarta el CTA en silencio); `description` exige CTA con enlace; `asset_feed_spec` no expuesto
  → 1+1+1; UTM solo en el panel.

**Enganchado** desde el `description` (nuevos disparadores: "te paso el video", "monta este video
como anuncio", "la cuenta está vacía"), el índice de referencias, el flujo de build, un aviso al
inicio de `15-creativos-produccion.md` y un control nuevo en el auto-check.

## G5.7 — 2026-09-03 — 🔴 La trampa de los "centavos": COP va ×1, no ×100

**Incidente medido, no teórico.** Montando `LECOTERRA - VENTA - OPEN 1` en GOLDEN CP6 COL, FER
pidió $50.000 COP/día y se mandó `daily_budget: 5000000` → el conjunto quedó en **$5.000.000
COP/día, 100 veces**. No se gastó (estaba PAUSED). Orden de FER: *"este error no puede pasar
nunca más, revisa la skill y corrige para siempre"*.

**Causa raíz en ESTA skill:** `reglas-de-oro` §5 decía *"la API usa centavos del currency de la
cuenta"*. Es **falso para las monedas de cero decimales** — COP, CLP y PYG, tres países donde
Golden opera. El parámetro se llama `..._cents` y el nombre miente.

**Corregido en tres sitios:**
- `reglas-de-oro.md` §5 — reescrita: tabla de multiplicador por moneda, el testigo
  (`min_daily_budget_cents`: USD `100` → ×100; COP `3076` → ×1) y el procedimiento obligatorio.
- `13-auto-check.md` — control duro en Publicación: **releer el `daily_budget` del servidor** y
  comparar el texto renderizado con lo pedido. Sin esa relectura no se reporta el montaje.
- `SKILL.md` — regla 5 y checklist de entrega.

**La clase, no el caso:** un presupuesto que no se leyó de vuelta del servidor no está verificado.
El arreglo es el instrumento (la relectura), no la intención de multiplicar bien.
Memoria: `reference_presupuesto_meta_cop_x1_no_centavos`.

## G5.3 — 2026-08-24 — Barrido total del arsenal ordenado por FER, vía Centro de Mando
Auditoría fresca `golden-skill-auditor` (lote AUDITA+ARREGLA del CdM). Hallazgos con evidencia, reparados:
- **El ledger volvía a estar incompleto** (tercera reincidencia de la clase que G4.7 y G5.2 dieron por
  cerrada): el sello G5.2 del `SKILL.md` afirmaba "changelog completado con G5.0/G5.1/G5.2" pero este
  archivo terminaba en G4.9 (mtime 2026-08-21, sin tocar en la corrida del 24). Se añadieron las tres
  entradas, reconstruidas desde los sellos reales conservados en los backups
  `golden-ads-20260823-025937` y `golden-ads-20260824-215040`, y se marca la lección de clase: **"el
  ledger quedó completo" solo se sella tras releer este archivo del disco, no desde la intención.**
- **La cita prometida en `07` no existía**: el sello G5.2 decía que `referencia-externa-ctwa-cod-panama.md`
  quedaba "citada desde `07`"; grep en `07-benchmarks-kpis.md` dio cero. Cita añadida de verdad (línea de
  contraste externo bajo la tabla orientativa).
- **Plugin fantasma `3qs:3qs`**: citado en `SKILL.md` (Relación con otras skills) y `01-fuentes-datos.md`
  como delegado de análisis de informes; verificado contra `~/.claude/plugins` (installed_plugins.json +
  grep del cache): NO está instalado. Se retiró la cita; la delegación queda en `golden-meta-ads-analysis`.
- **Tool inexistente `ads_targeting_search`** en `16-segmentacion.md` §A: el MCP de Meta conectado no la
  expone (lista de tools del entorno verificada). Reescrito: los IDs de interés se buscan en la UI de Ads
  Manager (o no se usan intereses; en COD amplio rinde más).
- **`referencia-externa-ctwa-cod-panama.md` atribuía al SKILL.md reglas que no contiene** (multianunciante
  OFF, 15 copys, asset_feed_spec, UTM — grep 0 matches en la skill): esas son leyes de la casa que viven
  en la memoria Golden, no reglas de este SKILL.md. Redacción corregida sin perder la advertencia; ruta
  final de la fuente ajustada a la carpeta real `PROYECTOS/PANAMA - OPERACION/`.
- Re-blindada con su mecanismo histórico (`chflags -R uchg`; la corrida del 24 la había dejado escribible).
Cambios relevantes reportados a 🧠 GOLDEN - CENTRO DE MANDO (estándar 9). Sello → **G5.3**.

## G5.2 — 2026-08-24 — Auditoría golden-skill-auditor: sello único + rescates
*(Entrada reconstruida en G5.3 desde el sello impreso del SKILL.md de esa corrida; la corrida original
no escribió este ledger.)* Sello ÚNICO (había dos GAE_VERSION contradictorios, G5.1 arriba y G5.0 abajo —
reincidencia del desfase que G4.7 dio por cerrado); `referencia-externa-ctwa-cod-panama.md` rescatada del
olvido (82 líneas huérfanas, ahora en el mapa; la cita desde `07` que este sello prometía la materializó
recién G5.3); resumen de reglas renumerado a la numeración CANÓNICA de `reglas-de-oro.md`; mapa reordenado;
`3qs` → `3qs:3qs` (revertido en G5.3: el plugin no existe instalado).

## G5.1 — 2026-08-23 — Estándar 9 (Centro de Mando)
*(Entrada reconstruida en G5.3 desde el sello del backup `golden-ads-20260824-215040`.)* Se declara la
conexión con el ecosistema: los cambios relevantes de esta skill se reportan a
🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.

## G5.0 — 2026-08-21 — Auditoría golden-skill-auditor: examples/ → references/, ledger fusionado
*(Entrada reconstruida en G5.3 desde el sello del backup `golden-ads-20260823-025937`.)*
(1) `examples/EJEMPLO-diagnostico.md` y `examples/PRESET-columnas-golden-09.2025.md` movidos a
`references/` (la carpeta `examples/` no es empaque válido de marketplace; los 2 punteros del cuerpo
actualizados); (2) el `CHANGELOG.md` de la raíz (duplicaba y desincronizaba con `references/changelog.md`,
faltaban G4.5 y G4.7 en el ledger) fusionado aquí — este archivo pasa a ser la ÚNICA fuente de
versión/fecha, con índice al inicio; (3) reconciliadas 2 notas de versión aplicadas sin bump de
GAE_VERSION en 2026-07-30 y 2026-08-02.

## G4.9 — 2026-08-18 — CAPA HUMANA parte 2: redes, patrones y sondeo de producto
Segunda pasada sobre la misma clase de FER, buscando lo que había quedado como frase y no como doctrina:
- **`21` §3-bis · comportamiento POR RED SOCIAL** (era su punto "saber el comportamiento de las redes"
  y no estaba): tabla FB feed / IG feed / Reels-TikTok / Stories / WhatsApp / Audience Network con el
  estado mental con que llega la persona, qué creativo funciona y la trampa de cada una. Regla operativa:
  un creativo por LENGUAJE de red (mínimo 9:16 + 1:1/4:5), Advantage+ por defecto pero revisando el
  breakdown por ubicación, y los comentarios/mensajes como voz de cliente en crudo.
- **`21` §6-bis · sondeo del PRODUCTO en el mercado** (pedía marca **y producto**; solo estaba marca):
  6 criterios con evidencia (demanda, saturación de pauta, madurez del mercado, diferencial defendible,
  precio vs rango, evidencia de que ya vende) + **matriz cruzada marca × producto** que define la
  estrategia (el peor cuadrante: marca invisible con producto saturado → no forzar pauta, cambiar oferta).
- **`22-patrones-y-lectura-de-datos.md` (NUEVO)** — su "analizar los datos y PATRONES" convertido en
  método: los 4 marcos de comparación (un número siempre se lee contra algo), tendencia vs ruido
  (3+ puntos, promedio móvil, regla de 72 h, ventanas asimétricas COD), ciclos (semanal, quincena/día de
  pago LatAm, estacional, ciclo de vida del creativo = fatiga no falla), **correlación ≠ causa** con el
  método de 3 hipótesis, 6 patrones que siempre se buscan (concentración, divergencia de embudo,
  duplicados, cero absoluto, outlier, cohorte) y la salida obligatoria en 4 puntos.
- Enganchado en `02-diagnostico` (nota antes del semáforo), regla 8 del SKILL y mapa de archivos. → **G4.9**

## G4.8 — 2026-08-18 — 🫀 CAPA HUMANA: audiencia, MOMENTO y mensaje con corazón
Cosecha de la clase de análisis de datos que tomó FER. La skill era fortísima en mecánica de cuenta
(CPA, breakeven, columnas, MCP) y floja en lo que los números NO dan: a quién le hablamos de verdad,
cuándo llegarle y CÓMO decírselo.
- **`21-audiencia-momento-humanidad.md` (NUEVO, 188 líneas)**:
  - **Filtro anti-parálisis**: 3 preguntas antes de mirar una métrica + lista de las que DECIDEN vs las
    que solo describen (impresiones, likes, seguidores) + regla "una decisión por revisión".
  - **Audiencia real** desde 6 fuentes vivas cruzadas (breakdowns Meta, pedidos Dropi, chats de Chatea,
    reseñas, cerebro de marca, Ad Library) y **segmento por SECTOR/contexto de vida, no solo por edad**,
    con nombre propio ("Karen, 34, oficinista…"), 3–5 segmentos, todos fondeados de verdad.
  - **Embudo de COMPORTAMIENTO** (7 etapas: descubre → reconoce → considera → decide → compra → usa →
    repite) con qué necesita la persona en cada una. Mismo copy para las 7 = error #1 de la cuenta que
    ya no escala.
  - **MOMENTO en 3 capas**: disparador de vida, **temporada** (sol y sudor / frío / diciembre-regalo /
    vuelta a clases) anticipando 3–4 semanas para que el algoritmo aprenda antes del pico, y hora/día
    (el más débil; nada de dayparting en aprendizaje). Retargeting = herramienta pura de momento.
  - **Mensaje humano ejecutable**: escribir para UNA persona, usar SUS palabras literales de reseñas y
    chats, nombrar el sentimiento, empatía sin culpa (choca además con la política de atributos
    personales), honestidad radical (el claim inflado destruye el % de entrega en COD = destruye el ROAS
    pagado), prueba humana antes que argumento, cierre con calma. **Checklist humano de 4 puntos** por
    creativo, con el mismo peso que el técnico de `13`.
  - **Sondeo de marca 1–10** (huella digital): rúbrica de 10 criterios con evidencia obligatoria por
    punto + qué estrategia toca según el tramo (1–3 invisible → confianza primero; 9–10 fuerte →
    defender marca y escalar por temporada).
  - **Fidelización/LTV**: segmentar la base, excluir compradores recientes del prospecting, campaña de
    recompra con voz de conocido, y medir LTV (si recompra 2–3 veces el breakeven real es más alto y
    puedes pagar más por el cliente que la competencia). La entrega es parte del marketing.
- **Reglas de oro 16 y 17** (numeradas después de las 14/15 que ya existían — CREATIVOS PRIMERO y copys
  normalizados): "el dato decide QUÉ, la empatía decide CÓMO" y "llegar en el MOMENTO vale más que
  llegar a muchos".
- **Conectado en 4 puntos** del SKILL: resumen de reglas (punto 8), Modo B (audiencia ideal por sector),
  checklist de cierre (capa humana obligatoria) y mapa de archivos. Sello → **G4.8**.
> Nota de fábrica: al editar se detectó que otros chats habían subido la skill a G4.7; este aporte se
> montó ENCIMA sin pisar nada (reglas renumeradas a 16/17 para no chocar con las 14/15 existentes).

## G4.7 — 2026-08-11 — RED SINÁPTICA: puente a la transcripción LOCAL de creativos + reconciliación de sello
Entra el puente a la transcripción LOCAL de creativos en "Relación con otras skills" — los hooks de los
anuncios ganadores se minan del audio con whisper local (gratis, el material no sale del equipo). Receta
canónica en `golden-investigacion-mercado` → `references/01-investigacion-360.md` §1.6 (no se duplica
aquí para que no envejezca en dos sitios); el desglose segundo a segundo lo hace `golden-video-teardown`.
Propagado por el Centro de Mando tras el hallazgo del chat FILTRO (la capacidad existía en
`golden-video-editor` y nunca circuló).
**Además, reconciliado un DESFASE DE SELLO** encontrado en esta misma edición: el ledger (este archivo)
decía **G4.5 (2026-08-07)** para la cosecha del chat dental, mientras el sello impreso en `SKILL.md`
decía **G4.6 con fecha 2026-07-25** para el mismo tramo de trabajo — versión dictada ≠ versión impresa.
Desde esta edición ambos dicen **G4.7** y este ledger (`references/changelog.md`) queda como fuente única
de verdad de versión/fecha; `SKILL.md` solo refleja el número vigente. Sello → **G4.7**.

## G4.5 — 2026-08-07 — Cosecha del chat "ESTUDIO 360 DENTAL CAVITY HEALING" (Chile), vía Centro de Mando
> Nota de reconciliación (ver G4.7 arriba): este tramo de trabajo quedó registrado con doble numeración
> en su momento (ledger decía G4.5, sello impreso decía G4.6/2026-07-25). El contenido abajo es real y
> vive hoy en `12-unit-economics.md`; el número de versión que manda es el de este ledger.
- `12-unit-economics.md` — la escalera de rentabilidad ahora se calcula **POR ESCALÓN DE COMBO**:
  breakeven CPA por 1u/2u/3u presentados juntos (caso real Chile: costo $8.500, envío/recaudo $4.500,
  entrega 65% → breakeven $9.744 / $12.019 / $13.000). El veredicto "sin combo no cierra" solo aparece
  viendo los tres escalones a la vez. Entregable: tabla por escalón + veredicto explícito de viabilidad
  de la unidad suelta.
- Misma reference: **PALANCA DE PRECIO** como recomendación estándar de media buyer cuando el margen
  queda apretado — subir del piso al techo del mismo rango de mercado ($27.990→$29.990 = $2.000 más de
  margen = 13% más de techo de CPA). Siempre recomendación, nunca imposición: el precio lo fija el dueño.
- Fuente: bandeja del Centro de Mando, entrada 2026-08-07 del chat dental (orden de FER: "sin omitir
  detalle"). Backup de esa edición: `~/.claude/skill-backups/golden-ads-2026-08-07-dental.tgz`.

## Notas de versión menores no selladas — 2026-07-30 y 2026-08-02
> Estos dos cambios se aplicaron entre G4.4 y G4.6 sin bump explícito de `GAE_VERSION` en su momento
> (gap detectado y cerrado en la auditoría `golden-skill-auditor` de 2026-08-21). Contenido verificado
> presente en la skill; se documentan aquí para que el ledger quede completo.
- **2026-07-30** — AGREGADO `references/referencia-externa-ctwa-cod-panama.md`: material de masterclass
  de terceros (Leyendas E.C.O.M + Ecom Founders, data de Dropi Panama) sobre embudo COD por Click-to-WhatsApp.
  Marcado explícitamente como **REFERENCIA OPCIONAL, NO REGLA** — no modifica `SKILL.md` ni ninguna regla
  dura de la skill.
- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección **🔄 AUTO-MEJORA**
  (mandato global de FER, autorización permanente) al cierre de `SKILL.md` — auto-calificación al cerrar
  cada corrida real, horneado de lecciones de sistema, autocorrección proactiva de huecos propios.

## G4.6 — 2026-07-27 — CORRECCIÓN DE FONDO: Golden NO es solo contra entrega
Corregido por FER, que aclaró que además del catálogo COD tiene **marcas propias con pago
anticipado** — clientes que ya conocen el portal y pagan directo. La skill asumía COD en todo:
**72 menciones a contra entrega contra 1 a pago anticipado** (medido antes del arreglo).

**El error que producía, con números.** Mismo producto, margen bruto 54.900:
COD al 65% de entrega → breakeven CPA Meta **35.685**. Pago anticipado → **54.900**.
Una campaña con CPA 43.000 **pierde en COD y gana en pago anticipado**. Aplicar la fórmula COD a
una marca propia bajaba el techo un 54% y hacía **pausar campañas rentables**.

Cambios: `12-unit-economics.md` abre con la tabla comparativa de los dos modelos y trae las dos
fórmulas separadas más el ejemplo lado a lado (incluye comisión de pasarela y cuotas sin interés,
que solo existen en prepago) · `07-benchmarks-kpis.md` corrige que **`InitiateCheckout` sí existe
en pago anticipado** y es la mejor señal temprana (antes afirmaba en seco que no existe, cierto
solo en COD con Releasit) · regla de oro 9 reescrita: preguntar el modelo de pago ANTES de calcular ·
el rol del SKILL.md ya no dice "e-commerce COD LatAm" a secas.

## G4.4 — 2026-07-18 — ACLARACIÓN: la data/histórico es la EXCEPCIÓN; producto nuevo = Modo B por default
Ajuste ADITIVO fino (autorizado por el dueño; solo aclara, no borra ni desoptimiza). Las secciones de G4.3
sobre "cruzar con data de pedidos" (`01 §D`) y "segmentar por comprador real" (`16 §C`) podían leerse como
si SIEMPRE fuera a existir histórico. Se marcan explícitamente como CONDICIONALES:
- **Nota nueva al inicio de `01-fuentes-datos.md` §D** y de **`16-segmentacion.md` §C**: "Aplica SOLO si hay
  data real/histórico (la excepción: producto ya vendido o relanzamiento a otro país). Para producto NUEVO
  sin datos — el caso normal — el default es **Modo B (testeo)** y NO se pide ni se asume métricas."
- Título de `01 §D` suavizado: "Cruza SIEMPRE con la data de PEDIDOS" → "Cuando HAYA data de PEDIDOS, cruza".
- **La lógica Modo A / Modo B existente NO se tocó** (ya estaba bien). Sello `GAE_VERSION` → **G4.4**.

## G4.3 — 2026-07-18 — Aprendizajes de campo Le'côterra (COD cuidado personal, Colombia)
Horneados 6 aprendizajes de un caso real, todos ADITIVOS (nada se reescribió ni se quitó):
- **`16-segmentacion.md` (§C nueva)**: segmentar por el **COMPRADOR REAL** de cada creativo/producto, no
  por la etiqueta ni "abierto a ciegas"; **fondear todos los segmentos** (el error caro es subfinanciar
  uno y decir "no funciona"). Caso: la cuenta marcaba "90% mujeres" solo por correr puro Vanilla; el
  comprador real era Vanilla 76% M, Bergamot 90% H, Athletix 50/50.
- **`01-fuentes-datos.md` (§D nueva)**: la demografía de la cuenta está contaminada (self-fulfilling) →
  **cruzar SIEMPRE con la data de PEDIDOS** (Dropi/Chatea/CRM, vía `golden-dropi-analisis`): género por
  nombre, mezcla de producto, combo attach, geo, entrega por transportadora. El pedido manda sobre la impresión.
- **`08-creativos-testeo.md` (§3 ampliada + §6 nueva)**: rankear creativos por **compras y ROAS, nunca por
  CTR ni gasto** (el mayor CTR dio ROAS 1,95; el campeón real ROAS 2,78 no era el de mejor CTR). Y **ruteo
  video→destino**: video de 1 producto → su variante (combo de refuerzo); video de línea/dúo → combo primero.
- **`07-benchmarks-kpis.md` (sección de edad nueva)**: patrón COD LatAm cuidado personal — 18–24 el más
  flojo (cortar), **25–44 el núcleo**, 45–54 aceptable, 55+ buen ROAS poco volumen. Arrancar 25–44.
- **`12-unit-economics.md` (2 secciones nuevas)**: **combo = palanca de rentabilidad** (con flete fijo la
  unidad suelta pierde; empuja combo si el attach es ~1,0–1,1) y **entrega por transportadora** cambia el
  breakeven (Envia 11,6% dev < Veloces 18,2% < Interrapidísimo 23,7% → enrutar a la de menor devolución).
- Sello → **G4.3**.

## G4.2 — 2026-07-09 — Auditoría A-Z + playbook de SEGUIMIENTO post-lanzamiento
Auditoría completa de los 23 archivos (pedida por el usuario: "revisa la skill y mejora"):
- **`20-seguimiento.md` (NUEVO)**: el hueco que faltaba — la skill sabía crear y diagnosticar pero no
  tenía el ritmo post-activación. Calendario día 0 (checklist técnico) / día 1 (señales rápidas:
  CTR/hook/CPC) / día 2–3 (corte de embudo, arreglar el eslabón no la campaña) / día 4–7 (primer
  veredicto con semáforo vs breakeven) / semanal (3 listas + fatiga + activity log). Cuándo tocar y
  cuándo NO (aprendizaje), escalado 20–30% vertical/horizontal, rutina MCP, y "nunca" de seguimiento.
  Enlazado en description (triggers "ya la activé, qué miro"), mapa de archivos y checklist de cierre.
- **Fixes de la auditoría**: sello visible sincronizado (decía G3.9/2026-06-25 siendo G4.1 — el texto
  visible quedó atrás dos versiones); reglas de oro reordenadas (13 aparecía antes que 12; números
  intactos para no romper "REGLA #13"); description apuntaba al `18` para columnas → ahora GOLDEN PRO
  (`19`) es el oficial también en el disparador. Sello → **G4.2**.

## G4.1 — 2026-07-02 — 🚀 Replicación GOLDEN PRO por URL (validada en vivo en CP1/CP5/CP6)
Descubierto y ejecutado EN VIVO: Ads Manager acepta `columns=<lista de campos en orden>` en la URL.
- **`19-golden-pro-preset.md` + URL MAESTRA**: pegar la URL cambiando `act=<ID>` aplica las 40 columnas
  en el ORDEN EXACTO del embudo en cualquier cuenta; luego "Guardar como valor predefinido" (3 clics).
  Adiós al marcado manual y a los arrastres (que eran in-automatizables a larga distancia).
- **Diccionario de tokens** horneado: las 9 custom de negocio con su `custom_derived_metrics:<id>` +
  los tokens estándar (omni_purchase, unique_website_ctr:link_click, quality_score_*, video_p50/75/100…).
- **Truco para extraer la URL de cualquier vista**: eliminar/mover UNA columna por el menú del encabezado
  → la URL se reescribe con el columns= completo. El menú ▾ también permite "Mover a la izquierda/derecha"
  (ordenar sin arrastrar).
- **Hallazgos honestos**: `column_preset=<id>` NO viaja entre cuentas (preset = por cuenta); `columns=` SÍ.
  El preset viejo de CP1 tenía el orden revuelto + 2 columnas extra (Acciones, Interacción con la página)
  y le faltaban 5 (CTR único, costo por vis./carrito, y las que Meta omitió) → se reconstruyó perfecto
  desde la URL y se re-guardó como GOLDEN PRO (nuevo id). Replicado: CP1, CP5, CP6 (ids en `19`).
  Sello → **G4.1**.

## G4.0 — 2026-07-02 — 🚦 Semáforo de metas por métrica + guía imprimible GOLDEN PRO v1.1
Nace del entregable real pedido por el usuario (guía .docx/.pdf de las 40 columnas):
- **`19-golden-pro-preset.md` + sección 🚦 SEMÁFORO DE METAS**: umbral 🟢/🔴 por métrica (CPA < breakeven
  = escalar · Frecuencia <2/>3 · CTR >1%/<0.5% · carga >80%/<60% · conv compras >1–2% · Hook >25%/<15% ·
  Hold >20%/<10% · rankings ≥ promedio · FTIR alto/bajando · compras ≥15–30 para decidir). Honestidad:
  CPM/CPC sin umbral universal (histórico propio); alcance/impresiones/carritos = contexto de embudo.
  Umbrales = punto de partida COD LatAm, calibrar con datos reales de la cuenta cuando haya volumen.
- **`02-diagnostico.md`**: el diagnóstico del embudo (Modo A) ahora usa ese semáforo como vara de cada
  escalón — deja de ser juicio a ojo.
- **Receta del doc imprimible** horneada en `19` (tabla 7 col: # · ES · EN · Tipo · Fórmula · Meta
  objetivo · Qué mide; custom en dorado, metas en verde) — generado real en Desktop (.docx + .pdf v1.1).
- **`SKILL.md`**: GOLDEN PRO promovido a preset ÚNICO oficial en la ruta "a pedido" y añadido al mapa
  de archivos (faltaba). Sello → **G4.0**.

## G3.9 — 2026-06-25 — GOLDEN PRO: preset único construido EN VIVO (Hook/Hold rate creadas)
El usuario decidió un solo set con TODAS las métricas (web + WhatsApp) llamado **GOLDEN PRO**, en orden
de embudo (decisión primero → diagnóstico). Construido en vivo en CP1:
- **`references/19-golden-pro-preset.md`** (NUEVO): el preset definitivo — 5 bloques (gano? → embudo web
  → embudo WhatsApp → creativo/video → subasta) + las fórmulas de todas las métricas custom.
- **Creadas EN VIVO 2 métricas de fórmula** a nivel NEGOCIO (sirven en todas las cuentas): **Hook Rate %**
  (`video 3s ÷ impresiones`) y **Hold Rate %** (`video 100% ÷ video 3s`). Se documentó también la fórmula
  real de FTIR (`Alcance ÷ Impresiones`, creada por el usuario).
- **Orden = decisión primero**: presupuesto/gasto/ventas/CPA/Tasa CPA/ticket/ROAS arriba (para decidir
  escalar), luego el embudo para hallar dónde se cae. Guía de diagnóstico incluida.
- Aprendizaje horneado: el preset es POR CUENTA (replicar = re-marcar; ahora rápido porque las custom son
  de negocio); el MCP no fija columnas (es UI) → se hace por navegador. Sello → **G3.9**.

## G3.8 — 2026-06-25 — FTIR + realidad de presets por-cuenta (auditoría en vivo CP1/CP5/CP6)
Revisadas EN VIVO por navegador 3 cuentas del usuario. Hallazgos absorbidos en `18-columnas`:
- **FTIR añadido al Set Maestro** (faltaba: el PDF de 26 no lo tenía; el preset live FER 2026 sí). FTIR =
  First Time Impression Ratio (frescura vs saturación de audiencia) — clave para escalar COD.
- **Los presets de columnas son POR CUENTA, no se comparten**: CP6=`FER 2026` (32 col, con FTIR),
  CP1=`Fer 2025` (27, sin FTIR), CP5=`GOLDEN 2026`/`GOLDEN 2025`. Nombres inconsistentes y desactualizados.
- **Regla experta nueva**: estandarizar por OBJETIVO de la cuenta (web/COD → Set 1 con FTIR; WhatsApp →
  Set 3 con costo por conversación), mismo nombre en todas, y revisar que esté ACTIVO el preset correcto
  (muchas tienen el viejo puesto teniendo el nuevo — a CP5 se le activó su GOLDEN 2026 sin usar).
- **ROAS pagado COD** aclarado: NO es columna de Ads Manager (necesita % entrega) → cálculo en el análisis.
  Sello → **G3.8**.

## G3.7 — 2026-06-25 — Set Maestro Golden (columnas reales del usuario absorbidas + mejoradas)
El usuario compartió su preset real de Meta ("Metricas Golden.pdf" 09.2025, 26 columnas personalizadas).
Se absorbió como fuente autoritativa:
- **`18-columnas-ads-manager.md`**: nuevo **⭐ SET MAESTRO GOLDEN** = las 26 columnas reales (Tasa de CPA %,
  Ticket promedio, Velocidad de carga, CTR único, Tasa conversión WhatsApp/compras, CPA final, video
  3s/50/100%…) + **6 mejoras** (➕ Hook rate, Hold rate, ThruPlay, Agregar al carrito, Costo por
  conversación WhatsApp, Clasificaciones, ROAS pagado COD), ordenado por embudo.
- **`examples/PRESET-columnas-golden-09.2025.md`** (NUEVO): el preset original tal cual, como referencia.
- **Honestidad clave confirmada en la práctica**: el MCP NO lee ni fija la vista de columnas guardada de
  una cuenta (es UI); las columnas del usuario vinieron de su PDF, no de la API. El preset es el mismo
  para todas sus cuentas (CP1/5/6/8…), así que un PDF cubre todas. Sello → **G3.7**.

## G3.6 — 2026-06-25 — Columnas/métricas como entregable a pedido (NO skill aparte)
Decisión del usuario (le recomendé no duplicar): las columnas/métricas quedan DENTRO de golden-ads como
fuente única (`18-columnas-ads-manager.md`), no una skill separada (evita drift + ambigüedad de disparo).
- Se agregaron **disparadores** en la descripción del SKILL ("dame las columnas", "qué métricas debo
  poner", "configúrame las columnas", "métricas para landing / WhatsApp por objetivo") → genera el
  documento de columnas (3 sets en orden de embudo).
- Pointer en el cuerpo del SKILL. Sello → **G3.6**. (Si algún día se quiere como producto para vender/
  compartir, se haría una micro-skill delgada que LEA de golden-ads, no que copie.)

## G3.5 — 2026-06-25 — Escalera de rentabilidad + columnas por embudo + criterio proactivo
Ideas del usuario, horneadas:
- **Escalera de rentabilidad** en `12-unit-economics.md`: no solo el breakeven suelto, sino "hasta aquí
  es rentable" → CPA máximo, CPA objetivo sano (50–70%), **ROAS objetivo en rango**, y tabla "si tu CPA
  es X, ganas/pierdes Y por venta y con 5/20 ventas/día". Traduce el número a decisión.
- **`references/18-columnas-ads-manager.md`** (NUEVO): las columnas que debe tener cada cuenta en
  **orden de embudo**, en 3 sets: **venta web/COD**, **landing con video** (hook rate/hold/retención) y
  **WhatsApp/mensajes (Chatea PRO → Meta)** (conversaciones iniciadas + costo por conversación + la
  compra que Chatea reporta a Meta por CAPI). Con nombres de Ads Manager + campos MCP. **Honestidad:**
  el MCP NO puede fijar la vista de columnas guardada (es UI) → se entrega el preset para guardar + se
  pueden sacar los datos ya en ese orden. A pedido, genera un documento con los 3 sets.
- **REGLA DE ORO #13 (criterio proactivo)**: opinar y sugerir mejoras como media buyer senior, no
  esperar a que el usuario lo sepa todo. Cableado en `02-diagnostico` (leer en orden de embudo). Sello → **G3.5**.

## G3.4 — 2026-06-25 — Aclarado el rol de los unit economics (breakeven, no P&L)
Pregunta del usuario: "para qué me pides precio/costo? Esto monta/analiza ads, no es ganancia/pérdida."
Tenía razón — se afinó REGLA #2 para no pedir economics de más:
- Los datos de economics sirven SOLO para el **breakeven** (CPA/ROAS máximo rentable = línea de
  pausar/escalar), **NO son un P&L** ni contabilidad.
- **Para dar veredicto** sobre campañas existentes → se necesita (si no, solo ranking relativo).
- **Para montar un test** → NO es bloqueante; se marca `[PENDIENTE]` y se sigue.
- Aplicado en `reglas-de-oro.md` (REGLA #2), `SKILL.md` y cabecera de `12-unit-economics.md`. Sello → **G3.4**.

## G3.3 — 2026-06-25 — Libreto de video, informe sin-MCP, y regla de significancia
Tres refuerzos pedidos por el usuario:
- **Libreto de video segundo a segundo** en `15-creativos-produccion.md`: cuando no hay media, además
  del prompt de imagen se entrega un LIBRETO ultra-detallado (tabla 0–3s hook / 3–8s problema / 8–15s
  producto+cómo actúa / 15–22s prueba / 22–28s oferta+garantía COD / 28–35s CTA) + tomas/b-roll,
  texto en pantalla, 3 variantes de hook, compliance. No un "guion vago".
- **`references/17-entrega.md`** (NUEVO): dos modos de entrega. CON MCP → montar en pausa. SIN MCP
  (cuenta ajena / cliente externo / solo quiere el plan) → **INFORME FULL copia-pega-able** (`META-ADS.md`)
  con campaña/conjunto/anuncio campo por campo, valores exactos, ejecutable por alguien que no sabe de
  pauta. Mismo rigor que montarlo nosotros.
- **REGLA DE ORO #12 (significancia)** + sección 0 en `02-diagnostico`: las métricas son un punto de
  dato, NO verdad absoluta. Sin volumen (≥2–3× CPA de gasto, ≥15–30 compras, ≥3–4 días) = señal
  temprana, no veredicto → basarse en lo que de verdad convertiría (histórico amplio + investigación +
  CTR/hook rate/CPC). Reportar nivel de confianza por campaña.
- SKILL.md: sección "Entregar/Publicar" con los 2 modos; file list; sello → **G3.3**.

## G3.2 — 2026-06-25 — golden-ads produce creativos+copys, y segmenta por histórico
Aclarado y horneado el flujo de montaje (Modo B) que pidió el usuario:
- **`references/15-creativos-produccion.md`** (NUEVO): golden-ads **SÍ hace los copys** (con
  `golden-copywriting` de motor). Árbol de decisión: (A) el cliente tiene media → **analizarla**
  (imágenes se leen; videos con `video_analysis_create`/`virality_predictor`) y escribir copys desde
  ahí; (B) no tiene pero tenemos APIs → **generar** imagen/video (Higgsfield/`golden-ugc-avatar`, producto
  fiel) y luego los copys; (C) sin saldo → **prompts perfectos** + slots. Copy = 5 hooks/5 títulos/5
  descripciones por creativo, emparejados a la pieza. El copy se escribe DESPUÉS de ver el creativo.
- **`references/16-segmentacion.md`** (NUEVO): sin histórico → recomendar (Advantage+ + persona); **con
  histórico → basar la segmentación en QUIÉN COMPRA** (sexo/edad/ubicación/plataforma) leyendo los
  `breakdowns` del MCP (`gender`/`age`/`region`/`publisher_platform`/`platform_position`) sobre
  **compras**, no impresiones, + Custom Audience de compradores y su Lookalike.
- SKILL.md: Modo B y Publicar ahora dicen que los creativos/copys los produce este skill; file list y
  sello → **G3.2**.

## G3.1 — 2026-06-25 — Higiene de la fase de aprendizaje (lección de un caso real)
El usuario contó que en CP8 puso una regla que **apagaba la campaña al gastar $35.000**; cada
apagado/encendido **reiniciaba el aprendizaje** y le encareció todo (luego borró las campañas). Se
horneó esa lección para que la skill lo detecte y lo evite:
- **`references/14-fase-aprendizaje.md`** (NUEVO): qué es la fase de aprendizaje, qué la reinicia
  (apagar/prender, saltos de presupuesto >20–30%, editar conjunto), la alternativa correcta
  (**tope de presupuesto / `campaign_spend_cap`**, NO apagados), y cómo **detectarlo en el activity log**.
- **Nueva REGLA DE ORO #11**: controla el gasto con TOPES, no con apagados.
- Cableado: `02-diagnostico` (revisar activity log por churn de encendido/apagado), `11-mcp-meta-recipe`
  (bandera de reinicios de aprendizaje), `03-build-con-metricas` (pausa definitiva, no en bucle; higiene
  antes de tocar presupuestos). Sello `GAE_VERSION` → **G3.1**.

## G3.0 — 2026-06-25 — VALIDADA EN VIVO (cuenta Meta real) + 4 refuerzos horneados
Estrenada contra una cuenta Meta real (COD, COP) por MCP en solo-lectura. El rodaje destapó fallos y
aprendizajes que se hornearon para llevar la skill hacia 1000/1000:
- **`references/11-mcp-meta-recipe.md`** (NUEVO): receta exacta de lectura por MCP + **chuleta de
  campos válidos** (compras = `actions:omni_purchase`, ROAS = `purchase_roas`, `results`/`cost_per_result`
  — NO `purchases`/`cost_per_purchase`, que tumbó una llamada real). Incluye orden de tools, parseo del
  formato real (montos con moneda, `results` anidado, "Not available"), y banderas (nombres duplicados,
  ROAS sin señal, cuentas DISABLED/UNSETTLED).
- **`references/12-unit-economics.md`** (NUEVO): calculadora de **breakeven COD** con la regla clave
  descubierta — **ROAS de Meta ≠ ROAS pagado**: `ROAS pagado ≈ ROAS Meta × tasa de entrega` (~55–75%);
  `CPA real = CPA Meta ÷ entrega`. Fórmulas + ejemplo. Nueva REGLA DE ORO #9.
- **`references/13-auto-check.md`** (NUEVO): checklist ejecutable de cierre (no entregar sin economics,
  sin ROAS pagado, con campo inválido, con moneda asumida, o activando sin OK).
- **`examples/EJEMPLO-diagnostico.md`** (NUEVO): diagnóstico modelo (caso real anonimizado CP8) = el
  estándar de cómo se ve una entrega (economics → semáforo vs breakeven → 3 listas → banderas).
- **Nuevas reglas de oro**: #2b (ROAS pagado COD), #9 (ROAS Meta ≠ pagado), #10 (verificar campos MCP +
  respetar moneda). SKILL.md (Paso 0 apunta a la receta; cierre corre el auto-check) y `02-diagnostico`
  actualizados. Sello `GAE_VERSION` → **G3.0**. Skill ahora **validada en vivo**, no solo teórica.

## G2.0 — 2026-06-25 — Rename a `golden-ads` + Meta/TikTok/Google completos + full-funnel
- **Renombrada** `golden-ads-estratega` → **`golden-ads`** (carpeta + `name:` + sello). Pedido del usuario.
- **Alcance a 3 plataformas**: Meta (MCP en vivo), **TikTok** (`09`) y **Google** (`10`) — estas dos
  report-based (no hay MCP en vivo), entregando configuración exacta para pegar en el gestor.
- **+ `06-retargeting-fullfunnel.md`**: embudo completo TOF/MOF/BOF + carrito abandonado + DPA/catálogo
  con exclusiones por etapa (el hueco #2 del diagnóstico 80/100).
- **+ `07-benchmarks-kpis.md`**: tabla de umbrales por etapa (CTR/CPM/CVR/frecuencia/CPA/ROAS) + reglas
  de matar/escalar escritas antes de lanzar.
- **+ `08-creativos-testeo.md`**: matriz ángulo×hook, lectura de ganadores por retención, fatiga y refresco.
- **SKILL.md**: Paso 1 (elegir plataforma), **checklist de cierre**, convención de entrega
  `PROYECTOS/<PRODUCTO>/ADS/` (regla de oro #8). Sello `GAE_VERSION` → **G2.0**. Blindada (chflags uchg).
- Verificado anti-duplicado: análisis de Excel sigue en `golden-meta-ads-analysis`; lanzamiento 360°
  en `golden-investigacion-mercado`; esta skill = media buying / optimización / publicación.

## G1.0 — 2026-06-25 — Versión inicial (Centro de Comando de Pauta)
Skill nueva, exclusiva de ads, separada del orquestador 360° (`golden-investigacion-mercado`).
- **Detección de fuente de datos** (Paso 0): conexión EN VIVO a Meta por MCP (preferida), informe
  Excel/CSV exportado (delega en `golden-meta-ads-analysis`), o sin datos (producto a testear).
- **Modo A · CON métricas**: diagnóstico con datos reales (unit economics + breakeven, semáforo,
  tendencia, anomalías, benchmarks de industria y subasta, opportunity score, activity log) →
  veredicto QUÉ PAUSAR/ESCALAR/AJUSTAR → reestructura/optimización con calendario de escalado.
- **Modo B · SIN métricas**: estructura de testeo (1 campaña, N conjuntos = N ángulos, público amplio
  Advantage+, 2–3 creativos, ABO) + criterios de matar/escalar definidos ANTES de lanzar.
- **Publicar por MCP**: crear campaña/conjunto/creativo/anuncio/públicos/A-B test EN PAUSA con reglas
  CBO/ABO, evento de conversión y pixel; activar SOLO con confirmación del usuario.
- **Reglas de oro**: no inventar métricas, unit economics primero, confirmar antes de gastar,
  compliance, país/moneda, no solapar audiencias.
- Verificado contra el MCP de Meta real conectado (server con `ads_get_ad_accounts`, `ads_insights_*`,
  `ads_create_*`, `ads_activate_entity`, etc.).
- Playbooks: reglas-de-oro · 01-fuentes-datos · 02-diagnostico · 03-build-con-metricas ·
  04-build-sin-metricas · 05-publicar-mcp.

---

## ARCHIVO · sellos GAE_VERSION históricos (migrados del SKILL.md el 2026-09-05)

> Estos bloques vivían como comentarios HTML dentro de `SKILL.md` y se cargaban en CADA activación
> (127 de 417 líneas = 30% del cuerpo). Se migran aquí íntegros, sin borrar una palabra, por la LEY
> DEL ACTA QUE NO SE ACTIVA: el acta va al changelog; el cuerpo se paga cada vez.

```
<!-- GAE_VERSION: G6.5 — 2026-09-05 — REGLA 20 completada con LA CLASE que el CdM identifico al
asumir su fallo: "el reparto se hizo sobre el recurso que tenia NOMBRE y no sobre el que no lo
tenia" — se repartio la cuenta de pauta (con id) y nadie repartio el navegador (sin id). La regla
pasa a DOS TIEMPOS explicitos (preguntar antes / DECIR que se suelta al terminar; el segundo es el
que se olvida y por el que nunca se cierra el turno) y se generaliza: antes de trabajar en paralelo,
LISTAR los recursos compartidos sin nombre propio (navegador, sesion de Shopify, token de workspace,
terminal, archivo que dos rutinas escriben) y repartirlos igual — si un recurso no aparece en el
reparto no esta libre, es que nadie lo miro. Vale para mucho mas que la pauta. — El bloque de abajo
es el historico G6.4:
GAE_VERSION: G6.4 — 2026-09-05 — LECCIONES DE LA PRUEBA CANDIDA/CP6 (FER la declaro prueba de
esta skill y pidio aciertos, fallas y que no se repitan; fila del CdM). 5 fallas horneadas: (1) se
DEGRADO de MCP a navegador SIN ejecutar el intento — se dedujo del schema en vez de lanzar la
llamada; regla 19: ejecutar, pegar el error del servidor y DECLARARLO. (2) copys rechazados por FER
("muy malos, sin emojis, corticos") porque no se invoco golden-copywriting NI se declaro que se iba
sin ella; NUEVO references/29-compuerta-de-copys.md con las 4 compuertas: copywriting OBLIGATORIO,
emojis obligatorios, hook en los primeros 40 caracteres, y 125/40/25 es TECHO no objetivo.
(3) CORREGIDO el estandar de "15 copys" que esta skill repetia: MEDIDO por DOM que el techo de carga
en "Crear anuncio y mensaje" es 5+5+1 = ONCE (Descripcion NO tiene "Agregar opcion") — y escrito que
NO se generaliza a otros objetivos sin medirlos, porque generalizar sin medir fue justo lo que creo
la regla equivocada. (4) obligacion de INVENTARIAR los copys que el anuncio ya tiene antes de
escribir encima y declarar cuales quedan fuera. (5) regla 20: escritor unico tambien del NAVEGADOR
(dos sesiones en el mismo Chrome destruyeron el grupo de pestanas 4 veces y costaron 2 borradores;
ahi no hay bloqueo ni aviso). ACIERTOS BLINDADOS en el 29: presupuesto COP x1 releido, multianunciante
OFF verificado, el copy nace del CREATIVO REAL abierto en vista previa y no del nombre del conjunto,
y el ingrediente falso tambien entra por la IMAGEN. Nota anadida: una cuenta puede tener campanas de
otros proyectos — no asumir que lo que hay dentro es del producto que se trabaja. La prueba cerro con
gasto CERO. — El bloque de abajo es el historico G6.3:
GAE_VERSION: G6.3 — 2026-09-03 — CONSUMIR el teardown de golden360 en vez de repetirlo (aviso
del CdM, verificado por mi en la skill hermana antes de hornear: golden360 R2.0 tiene FASE 5B real,
con golden-video-teardown entre producir los creativos y escribir los copys). Cuando el encargo llega
por la ruta 360, el video YA viene desarmado — beat sheet segundo a segundo, angulo, hook y copy
quemado en pantalla. Rehacerlo cuesta tiempo y creditos y arriesga CONTRADECIR el analisis que guio
la produccion. Nota en 25-cuenta-sin-creativos Paso 2 (buscar el teardown en el expediente ANTES de
analizar; si esta, rellenar la ficha con el y saltar al Paso 3) y en la fila de golden-video-teardown
del bloque de requisitos. Tambien anotada la ruta real del binario golden-transcribe
(~/.golden/bin/), que el validador del CdM confundia con una skill. — El bloque de abajo es el
historico G6.2:
GAE_VERSION: G6.2 — 2026-09-03 — REQUISITOS DECLARADOS (fila del CdM bajo la ley de FER: todo
lo que la skill necesite del usuario o del entorno se declara ANTES, cerca del principio, y se pide
AL CORRER si falta). MEDIDO: la skill citaba hermanas en decenas de archivos y declaraba CERO
requisitos (grep = 0) — golden-copywriting en 13 archivos, watch en 7, golden-investigacion-mercado
y golden-ugc-avatar en 6 cada una. Quien la instalara suelta lo descubria a mitad de un encargo.
NUEVO bloque "QUE NECESITA ESTA SKILL" tras el rol: entorno (MCP de Meta, datos del negocio) y las
6 hermanas, cada una con QUE APORTA y QUE PASA SI NO ESTA. Matiz que aporto el CdM y se consagra:
una dependencia entre skills NO es una API key — no se le pide al usuario que la pegue, se le dice
cual hermana falta y con que se degrada; y si falta golden-copywriting se escriben los 15 copys
igual (125/40/25 + compliance) pero SIN framework y SE DECLARA, nunca fingir que se aplico uno que
no se pudo leer. Al repartir, golden-copywriting va con golden-ads. — El bloque de abajo es el
historico G6.1:
GAE_VERSION: G6.1 — 2026-09-03 — DESCRIPTION DENTRO DE LA SPEC. Hallazgo de arsenal medido hoy
en este chat y confirmado por el CdM con medicion independiente: 34 skills instaladas pasan del tope
de 1024 caracteres que fija la especificacion de Agent Skills (agentskills.io/specification, leida en
vivo), y 32 de esas son de la casa. golden-ads estaba en 1.444. Recortada a <=1024 con el criterio
del CdM: los DISPARADORES primero (los del final son los que se pierden) y lo explicativo BAJA AL
CUERPO, que no tiene tope duro — la instruccion de "si te pasan un video, subelo, analizalo viendolo
Y escuchandolo, y escribe los copys de ESE video" ahora vive en el bloque de montar campana, no en el
disparador. DISTINCION HONESTA que aporto el CdM y se adopta: 1024 es el tope de VALIDACION de la
spec; el ~1536 que esta skill midio el 2026-08-07 es TRUNCADO EN RUNTIME — mecanismos distintos, las
dos mediciones son ciertas. Que un ZIP sea rechazado al distribuir es PLAUSIBLE Y NO MEDIDO: no se
vende como certeza. El "tope de 200 en claude.ai" que circulo NO se adopta: sin fuente verificada es
rumor, no limite. CAUSA RAIZ del fallo de deteccion (ya en manos del CdM): golden-skill-auditor MIDE
la description en inventario.sh:295 pero NUNCA la compara — "1024" aparece cero veces en sus scripts
y cero en rubrica.md/estandares-golden.md; el arreglo de clase sera adoptar el validador oficial
`skills-ref validate`, no codificar el numero a mano. Familia reference_familia_trampas_de_conteo:
el arreglo es el INSTRUMENTO, no la buena intencion. — El bloque de abajo es el historico G6.0:
GAE_VERSION: G6.0 — 2026-09-03 — OBJETIVOS DE CAMPANA (reclamo directo de FER: "objetivo son
trafico, interaccion, venta; tu ya debes saber todo esto, no deberia estar diciendo esto"). El hueco
era real: la skill nombraba OUTCOME_* de pasada en 05-publicar-mcp y el intake del 26 reducia el
objetivo a DOS opciones (venta web / WhatsApp), dejando fuera TRAFICO. NUEVO
references/28-objetivos-de-campana.md: tabla de decision con los 3 de Golden — que dice el usuario ->
enum ODAX -> optimization_goal -> promoted_object/destino -> por que metrica se mide; el criterio de
cual elegir; la advertencia de que INTERACCION optimiza a que escriban, no a que compren (y que
Chatea PRO debe devolver la conversion a Meta); LANDING_PAGE_VIEWS antes que LINK_CLICKS; y que
cambiar el objetivo obliga a REHACER la campana, no a editarla. Enums verificados contra la
Marketing API de Meta (ad-campaign-group) hoy. — El bloque de abajo es el historico G5.9:
GAE_VERSION: G5.9 — 2026-09-03 — CONEXION MCP + candado de presupuesto (aviso del chat EL
CARTEL DEL CHAT, verificado por mi contra la fuente autoritativa de Meta antes de hornear). NUEVO
references/27-conectar-mcp-meta.md: URL oficial https://mcp.facebook.com/ads, las DOS vias (con y
sin app propia), el comando exacto de Claude Code, los 7 permisos textuales, y el paso de
verificacion. HALLAZGO PROPIO que el aviso no traia y es lo que mas plata protege: Meta permite
fijar REGLAS POR CUENTA en Business Suite > Integrations > Ads MCP server que el servidor hace
cumplir, incluido un TECHO MAXIMO DE PRESUPUESTO ("Budgets set above this amount" = Blocked) — con
eso puesto, el incidente de los $5.000.000 habria sido RECHAZADO por Meta. CORRECCIONES al aviso: la
description medida son 1.766 chars, no 350 (factor 5); los clientes oficiales son ChatGPT/Claude/
Claude Code/Perplexity, NO Cursor ni Codex; y NO se encontro en las paginas oficiales ni la
advertencia de prompt injection ni los alcances "Read/Manage" — rotulado como no verificado en vez
de atribuirselo a Meta. ADEMAS: description recortada de 1.766 a ~1.500 chars, porque la propia
skill documento en 2026-08-07 un tope de ~1.536 y habia vuelto a pasarse (las frases del final NO
disparaban). — El bloque de abajo es el historico G5.8:
GAE_VERSION: G5.8 — 2026-09-03 — INTAKE (encargo directo de FER tras 3 fallas de campo:
presupuesto puesto 100x, campana entregada sin los 15 copys, creativo que no se subio). NUEVO
references/26-intake-montar-campana.md: portero del pedido "crea una campana de [objetivo] de
[producto] con presupuesto de [valor]" — los 3 campos se PREGUNTAN si faltan (juntos, una sola vez),
compuerta del presupuesto (escribir el renglon del calculo ANTES de mandarlo + releer del servidor),
y el ORDEN que enlaza investigacion previa -> creativo (25) -> 15 copys coherentes -> montaje (05)
-> UTM (24) -> verificacion (13). Enganchado arriba del SKILL.md y en el mapa. HALLAZGO: el hueco
real era el INTAKE (grep 0 matches); lo del creativo/copys YA estaba cubierto por 25 y lo del
presupuesto por reglas-de-oro §5 (ambos del 2026-09-03, posteriores al incidente de FER). Se
DESCARTO un 23-montar-campana-completa.md que se habia empezado: colisionaba de numero con
23-salud-de-senal, duplicaba 25 y citaba ads_creative_upload_image/_video que estan DEPRECADAS.
Y se deja escrito el tope MEDIDO que explica "no me sube los 15 copys": ads_create_creative NO
expone asset_feed_spec -> por API salen 1+1+1, los 15 se cargan en el panel y se REPORTA como
pendiente. — El bloque de abajo es el historico G5.7:
GAE_VERSION: G5.7 — 2026-09-02 (encargo directo de FER: "colocamos un UTM para que pueda enviar esa informacion de donde vino la venta, debe estar en la skill de MetaAds"). HUECO MEDIDO: grep -i "utm" sobre toda la skill daba 0 reglas (2 menciones de pasada). NUEVO references/24-utm-atribucion.md + REGLA 18 (reglas-de-oro.md y resumen del SKILL.md) + citas operativas en 05-publicar-mcp (paso 4 y "Nunca"), 13-auto-check (Publicacion), 17-entrega (nivel anuncio) y el checklist de cierre. Esquema tomado de la FUENTE REAL de los montajes (LECOTERRA MONTAJE-CP1-2026-07-25 y -OPEN7-2026-08-14), no del contrato viejo del CdM: el id va en utm_id y utm_content lleva el NOMBRE — confundirlos fue el incidente "adOPEN" del 26-ago. VERIFICADO HOY contra los esquemas vivos del MCP: ads_create_ad y ads_create_creative NO exponen url_tags, o sea que por MCP el anuncio nace sin UTM. SIN VERIFICAR y asi rotulado: ads_update_entity con url_tags, y la captura positiva por el camino LANDING. Detalle en changelog G5.7. — El bloque de abajo es el historico G5.6:
GAE_VERSION: G5.6 — 2026-08-31 (CdM) · CORRECCION ANDROMEDA verificada contra la fuente primaria de Meta (blog de ingenieria, 2-dic-2024, leido en vivo): se RETIRA el "Similarity >60% = supresion" (NO esta en Meta, venia de terceros/claude-ads) y se consagra lo estructural: Andromeda es RECUPERACION, decide quien COMPITE no quien gana; el creativo determina elegibilidad via embedding en indice jerarquico. Cifras reales de Meta anadidas con su condicion. "El primer frame es targeting" NO se consagra (no esta en la fuente). Detalle en changelog G5.6. — El bloque de abajo es el historico G5.4:
HERRAMIENTAS autorizado por FER en directo) — NUEVO references/23-salud-de-senal-y-andromeda.md:
7 controles de CALIDAD DE SEÑAL que faltaban (0 menciones previas medidas por grep): CAPI activo,
deduplicación >=90% por event_id, EMQ >=8.0 con palanca COD (mandar por CAPI el teléfono/ciudad
que ya están en Dropi/Chatea), Learning Limited <30% de conjuntos, presupuesto del conjunto >=5x
CPA objetivo (<2x = falla — PENDIENTE medirlo producto por producto), ANDROMEDA (⟶ el "Similarity >60%" fue RETRACTADO en G5.6: no está en la fuente primaria de Meta; lo que queda es que el ÁNGULO es la unidad creativa, no el archivo — matiza el 5+5+5: cinco redacciones
del mismo ángulo cuentan como UNA), y la redefinición de link clicks de feb-2025 (CTR cae sin que
el creativo empeore). +3 controles en 13-auto-check.md ANTES de leer rendimiento. 07-benchmarks-kpis
INTACTO (md5 idéntico verificado): sus umbrales COD siguen mandando en RENDIMIENTO; el 23 mide
SEÑAL. Offline Conversions API discontinuada may-2025. El FILTRO informó sin bump ni huella; el
CdM (dueño por ley) completa el sello. -->

<!-- GAE_VERSION: G5.3 — 2026-08-24 — Barrido total del arsenal (CdM): el ledger volvía a estar
incompleto pese a lo que afirmaba el sello G5.2 (le faltaban G5.0/G5.1/G5.2 — tercera reincidencia
de la clase de desfase; entradas añadidas, reconstruidas desde los backups); la cita a
`referencia-externa-ctwa-cod-panama.md` desde `07` que G5.2 prometía no existía — ahora sí existe;
retirado el plugin fantasma `3qs:3qs` (verificado NO instalado); `ads_targeting_search` (tool
inexistente en el MCP) corregida en `16`; la advertencia de la referencia externa ya no atribuye al
SKILL.md reglas que viven en la memoria de la casa. Estándar 9 (Centro de Mando) vigente desde
G5.1: los cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.
Detalle en `references/changelog.md`. -->

<!-- skill G5.5 · 2026-08-27 (chat FILTRO) · CORRECCION MEDIDA en 23-salud-de-senal: yo habia escrito que en COD el EMQ tendria techo bajo por el 1,7% de consentimiento. FALSO para el Purchase: medido en el pixel 375426632099018, EMQ 9.3 con cobertura 100% en las 13 claves. AddPaymentInfo 8.7. Lo que SI falla es el embudo previo: Search 4.4, ViewContent 6.1, PageView 6.2, AddToCart 6.4, todos bajo el umbral 8.0. Ademas: InitiateCheckout EXISTE en este pixel (167 en 7 dias) cuando benchmarks dice que en COD no existe — no se usa de corte hasta saber por que. Y el Purchase aparece partido en dos entradas (63 y 60): NO es prueba de doble conteo, la herramienta no da tasa de dedup. Origen: pendiente #1 que llevaba meses guardado en memoria. -->

<!-- skill v: 2026-08-26 (chat FILTRO, autoridad de FER) · NUEVO references/23-salud-de-senal-y-andromeda.md + 3 controles en el auto-check. ORIGEN: extraccion de claude-ads v2.4.0 (33 MB instalados en el Mac y NUNCA corridos). HUECO MEDIDO con grep sobre golden-ads: 0 menciones de EMQ, deduplicacion, Learning Limited, Andromeda y la regla de presupuesto >=5x CPA. NO se toco 07-benchmarks-kpis.md: sus umbrales COD son MAS exigentes que los del auditor generico (CTR >1.5% vs 1.0%, frecuencia <2 vs <3) y siguen mandando sobre rendimiento. El archivo nuevo mide otra cosa: la calidad de la senal que Meta recibe. Hallazgo a verificar: Andromeda suprime creativos con Similarity >60%, lo que choca con producir 5+5+5 variaciones del mismo angulo. (⟶ RESUELTO en G5.6: verificado contra la fuente primaria de Meta — el umbral 60% NO aparece en el blog; se retracta. Lo estructural (recuperacion, elegibilidad por creativo) SI se sostiene.) -->

<!-- 2026-08-07 · DESCRIPCIÓN RECORTADA: superaba el tope de ~1.536 caracteres del listado de skills y se estaba TRUNCANDO, así que las frases del final NO disparaban. Medido antes/después: 2211 → 991 chars. Lo que se movió al cuerpo son rutas de references y explicaciones; se conservaron y ampliaron las frases reales del usuario, que son lo que dispara. -->
```
