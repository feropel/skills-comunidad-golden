# Bitácora de la skill

Las actas de versión anteriores a la v1.7, mudadas desde el `SKILL.md` el 2026-09-22
porque el cuerpo pasó de 500 líneas y eso encarece la activación en cada disparo.

**Antes de mudarlas se comprobó que ninguno de sus artefactos ejecutables —topes, comandos,
banderas, rutas— viviera solo aquí.** Todos existen en el `SKILL.md`, en una referencia o en
el validador. Un acta es memoria de por qué se hizo algo; el dato operativo nunca vive solo
en ella.

Las dos actas vigentes (v1.7 y v1.8) siguen en el `SKILL.md`.

---

CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 958 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '🔴 **CUPO DE LA API: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.**
Medido contra la API viva el 2026-09-07: cada respuesta trae **`x-ratelimit-remaining`** (en
inglés *X-RateLimit-Remaining*, "las que quedan") y `x-ratelimit-limit`. **Se repone cada hora**,
pero **no viene `x-ratelimit-reset`**: el servidor no dice a qué minuto empezó la ventana, así que
si te bloqueas se espera una **hora completa** y se comprueba **mirando** el contador
(`golden-chatea-cupo [--necesito N]`), nunca calculándolo.

**Cuándo te afecta aquí:** al escribir el campo `[Comentarios] Productos` por API. Recuerda que se
escribe con **PUT** (`POST` devuelve `200` y **no escribe**) y que la **relectura es obligatoria**,
así que cada carga son al menos dos peticiones. Si cargas muchos productos de golpe, cuenta el
total antes: quedarte sin cupo a mitad deja el array de productos **escrito por la mitad**, y el
panel no lo delata.

## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo.

---

skill v1.6 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): validar_producto.py son 449 líneas y 19 chequeos que deciden si el campo de un cliente real está bien, y NO tenía banco — nadie había comprobado que mordiera. Nace scripts/autoprueba.py (14 de 14, sabotaje por pieza, con contraprueba).

---

skill v1.5 · 2026-09-06 (corrida semanal golden-skill-auditor): limpieza de
     scripts/__pycache__/validar_producto.cpython-314.pyc — bytecode compilado que quedó
     sobre la skill (huérfano potencial en inventario.sh, material que no debe viajar al
     marketplace). Borrado; sin efecto en el validador porque Python lo regenera solo si
     hace falta. Validador de arsenal en verde antes y después (exit 0). Sin más hallazgos
     con evidencia: la description mide 958/1024, las 5 referencias están citadas y vivas,
     scripts/validar_producto.py sintaxis OK, sin secretos, sin material intruso adicional.
     Cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.

---

skill v1.4 · 2026-09-05 (fábrica, mandato de autocalificación del CdM) · TRES COSAS.
     (1) 🔴 PAÍSES: la corrección del 29-ago cambió los CONTEOS del SKILL.md y NUNCA abrió paises.md,
     que seguía titulado "Los 7 países" y NEGABA literalmente Argentina y Guatemala — o sea rechazaba
     clientes instalables. Remedido de PRIMERA MANO hoy contra el bundle vivo index-BS1l9mqS.js
     (501.151 bytes, sha256 e792b3a3…), constante `me` + tabla `DA`: 10 países con su moneda
     (COLOMBIA COP, ARGENTINA ARS, BRASIL BRL, CHILE CLP, ECUADOR USD, GUATEMALA GTQ, MEXICO MXN,
     PANAMA USD, PARAGUAY PYG, PERU PEN); Bolivia/Uruguay/Venezuela/Costa Rica = 0. paises.md
     reescrito con los 10, y hallazgo nuevo: BRASIL ES PORTUGUÉS — la desc y el rela se escriben en
     el idioma en que comenta el cliente, y traducir un rela palabra por palabra no empareja.
     Además, medición cruzada sin cerrar: el bundle guarda el valor del campo País en minúscula y un
     workspace real lo tiene en MAYÚSCULA y funciona — regla honesta: no lo toques si ya está puesto.
     (2) FILA 2 del CdM · COMPUERTA POR VÍA: `--via` es ahora OBLIGATORIA y el validador se niega a
     correr sin ella. La misma desc de 675 es ERROR que bloquea por `formulario` (el panel corta) y
     AVISO aceptable por `json` (Campos de Bot). Probada en las tres direcciones: sin vía se niega,
     formulario exit 1, json exit 0 con aviso. Y cuando va por json pasado de 500, se entregan DOS
     versiones (completa + la de 500 para el día que alguien abra el formulario).
     (3) FILA 1 del CdM · EL ANUNCIO DE VARIAS IMÁGENES ROMPE LA CAPA 4: con contenido dinámico Meta
     solo pasa la palabra clave, el copy y el ID de la PRIMERA imagen; los comentarios de las demás
     llegan sin texto reconocible. No es un rela mal escrito, es el FORMATO del anuncio — la casa
     tenía escrito que el disparador se rompe por el NOMBRE, también se rompe por el FORMATO. Salida:
     copiar el hook de TODAS las imágenes, contar con el genérico, y COSECHAR el tablero de "no
     automatizados" de Chatea, que es la mejor fuente de capa 4 porque son fallos reales de la cuenta.
     El escape por ID de anuncio existe en VENTAS, no aquí (medido 2026-08-07 sobre los 5 bot fields).
     (4) Sección "Cuándo NO soy yo" con la frontera en una línea: si cambia CÓMO HABLA el asistente
     no soy yo; si cambia DE QUÉ PRODUCTO habla, sí.

---

corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto.

---

skill v1.3.3 · 2026-08-23 (Estándar 9, golden-skill-auditor): Estándar 9 (Centro de Mando):
     cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.

---

skill v1.3.2 · 2026-08-21 (auditoría golden-skill-auditor, 960 ORO → 1000): 🟡 escritura-api.md
     tenía una frase telegráfica ("16.882/19.895 dispara; 19.922/23.266 no") que exigía reconstruir
     el criterio del techo con el número al lado; reescrita en dos viñetas explícitas (pasa con
     aviso / no pasa, techo). Verificado en vivo: el validador corrido contra el ejemplo horneado
     de `ejemplo-completo.md` reproduce exacto 461/500 desc, 24 disparadores, 1.146/1.272 —
     y corrido contra un caso plantado malo (desc vacía, estado en mayúscula, rela genérico y
     repetido entre productos) cae con los 5 errores esperados y exit 1. Sin hallazgos críticos:
     cero secretos, cero referencias rotas, las 8 skills hermanas citadas existen hoy.

---

skill v1.3.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio).

---

skill v1.3 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta.

---

skill v1.2 · 2026-08-07 · auditoría independiente golden-skill-auditor (762 BRONCE → reparada): 🔴 el medidor del techo usaba ensure_ascii=False, con lo que una tilde contaba 1 en vez de 6 y un emoji 2 en vez de 12 — certificaba en verde campos por encima de 20.000 (corregido en escapado() y en escritura-api.md); 🔴 el detector de genéricos dejaba pasar hongos/brillo y las preguntas de capa 5 sin producto (reescrito: marca dentro, o 2 palabras con contenido, o una de 7+; categorías nunca solas ni estando en el nombre); regla de la coma en los hooks; el tercer campo espejo (TOON) sube al camino principal; plan B si la compuerta no puede correr; --medir excluyente del posicional; el 500 anclado con honestidad a su fuente; techos desduplicados a una sola fuente

---

skill v1.1 · 2026-08-07 · pruebas en seco (producto nuevo MX + reparación de JSON roto CO): añadido el modo AUDITAR con tabla síntoma→causa, la compuerta de entrega, la regla de tildes, el presupuesto por producto, el catálogo de reglas de marca por categoría y el banco fonético; --medir en el validador; contención de disparadores y excepción de erratas de marca; resuelta la contradicción marcador-de-img vs validador

---

skill v1.0 · 2026-08-07 · fábrica: chat "✅ SKILL golden-chatea-pro-producto-comentarios" · cubre el hueco declarado en _BANDEJA-CENTRO-DE-MANDO.md (2026-08-07): config-comentarios decía "esto es referencia, no lo genera este skill" sobre la ficha de producto. Fuentes: BRIEFING-PARA-SKILLS.md + TOPES-NATIVOS-POR-CAMPO.md + dos workspaces vivos de referencia (uno propio con 7 productos, uno de plantilla)

---

skill v1.7 · 2026-09-22 (fábrica, encargo de FER) · TRES TOPES DEL FORMULARIO, LEIDOS DE SUS
     PROPIOS CONTADORES en la pantalla "Agregar nuevo producto" del agente de comentarios
     (cuenta 236245). Ninguno estaba en la familia de skills:
     · 🔴 `rela` topa en 10 ETIQUETAS ("7/10 etiquetas"). Es el hallazgo gordo y es un tope de
       CANTIDAD, no de caracteres. La doctrina de esta skill pide 15-30 disparadores, o sea que
       UN PRODUCTO BIEN HECHO NO CABE POR FORMULARIO: se recorta a 10 y lo que se pierde es la
       COLA, que es justo la capa 4 (los hooks del anuncio). Medido contra el campo vivo de
       Golden: un producto con 71 etiquetas perdería 61.
     · `name` topa en 255 ("36/255 caracteres").
     · `desc` topa en 500 ("481/500 caracteres", en rojo) — esto CIERRA la reserva declarada en
       desc-plantilla.md, que decía que el 500 venía del briefing y no de una medición del
       formulario de Comentarios. Ya está medido de primera mano, con fecha.
     Y el TECHO DEL CAMPO NO ES DE LA PLATAFORMA, ES DEL TIPO: `JSON` = 20.000 escapados,
     `LONG JSON` = 500.000 (lo dice el propio panel al abrir `[Comentarios] Productos extendido`).
     Por eso el `array` aprieta y el extendido no. Bandera nueva `--long-json`.
     EL BANCO SE AMPLIO, NO SE APAGO: el tope de 10 rompió el caso 1 del banco, y con razón —
     su fixture "bien formado" lleva 16 disparadores y corría por formulario. Se separó en dos
     (el de la doctrina va por JSON, y uno recortado a 10 prueba que por formulario un producto
     bien hecho SI pasa, para que el validador no pueda estar bloqueando todo sin que el banco se
     entere) y entraron 4 sabotajes nuevos: 15 (rela >10 bloquea por formulario), 16 (el mismo
     avisa por JSON), 17 (name >255), 18 (el techo cambia con --long-json). 19 de 19 muerden.
     PENDIENTE CON DUEÑO, sin cerrar: cuál de los tres campos espejo lee de verdad el flujo de
     comentarios. Preguntado al Centro de Mando el 2026-09-22, sin respuesta al sellar.

---

skill v1.8 · 2026-09-22 (fábrica) · LO QUE DEVOLVIERON EL CdM Y EL CHAT MBA, y una
     retractación propia.
     · 🔴 DEROGADO "el flujo lee el array". Venía de agosto y se dedujo POR DESCARTE: entonces el
       `extendido` tenía datos y el `array` estaba VACÍO. El CdM midió los dos hoy en un espacio
       real y están POBLADOS Y SINCRONIZADOS (array 7 productos / 7.249 car.; extendido los MISMOS
       7 / 7.061 car., verificado nombre por nombre). El descarte ya no decide nada y escribir uno
       solo los DESINCRONIZA. Pasa a INCÓGNITA ABIERTA con compuerta: no escribir ninguno de los
       tres por API hasta cerrarla, y la prueba que la cierra NO es de disco (se comenta en un post
       y se mira qué responde). Lo hace el dueño del espacio, no esta skill.
     · API fechada, no refirmada entera: el CdM corrió HOY el GET paginado y el
       PUT set-bot-fields-by-name (releído y comparado como JSON parseado). `create-bot-field` y
       el "POST al editar devuelve 200 y no escribe" quedan marcados como medidos en 2026-08-07 y
       NO reverificados. Y no hay registro de ninguna "API nueva" de Chatea: no se inventa cuál es.
     · references/kevin-doctrina.md NUEVO, con minuto y cita de la clase M7 (2026-09-02, 2:34:33),
       y separando CITA / HUECO / DERIVADO. Lo que aporta de verdad: el `rela` es un IDENTIFICADOR
       ÚNICO y una etiqueta se descarta por COMPARTIDA, no por genérica (descartó "dormir", que
       describe bien, porque otro de sus magnesios también sirve para dormir); el `rela` NO se
       valida solo, se valida contra el COPY del anuncio, que debe repetir el disparador LITERAL;
       el método del "ejemplo" para superar los 500 (crear en el formulario con desc="ejemplo",
       editar el JSON extendido, recargar — medido en cámara: 500 → 1.895); las tres trampas del
       JSON, incluida "editar sin recargar es editar contra un estado viejo"; y el SEMÁFORO DE
       ENCAJE verde/amarillo/rojo como criterio de corte de los beneficios.
     · 🔴 RETRACTACIÓN MÍA: yo había citado a Kevin la "regla de la abuela" ("si tu abuela no
       entiende el beneficio en 5 segundos, está mal escrito"). El chat MBA la buscó en LAS 16
       GRABACIONES: sale dos veces y NINGUNA es Kevin ni habla de fichas. Venía de una nota de la
       casa. Corregida y marcada como criterio de la casa. Lección horneada en kevin-doctrina.md:
       antes de hornear una regla atribuida a alguien, BÚSCALA — esa sobrevivió meses sin que
       nadie lo hiciera.
     · También quedan marcados como criterio de la CASA y no de Kevin: el rango de 15-30
       disparadores (él no da número óptimo) y el tope de 10 del formulario (es de la herramienta).
     · HUECO declarado por el MBA: Kevin no dice qué hacer con "dosis diaria" en un producto que se
       aplica. La sustitución por su equivalente está marcada como DERIVADO, no como cita suya.
     · FECHA DE CADUCIDAD: él llama al `rela` "un plan de contingencia" porque "en la versión 3 se
       va a hacer conexión con el POST ID del anuncio". Si la v3 sale, este capítulo se remide.

---
