# Changelog · golden-chatea-pro-full-configuracion

> **Por qué existe este archivo (Centro de Mando, 2026-09-07).** Estas actas vivían dentro del
> `SKILL.md` como comentarios HTML: **14 bloques, 14.989 bytes, el 31% del archivo**. Un
> comentario HTML en el cuerpo **se paga en cada activación** aunque nadie lo lea — y esta es la
> skill que ARRANCA una instalación completa, así que ese peso se paga siempre. **El cuerpo se
> paga siempre, el acta solo cuando se consulta.** No se perdió una palabra: bajaron verbatim.

## CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las 

CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 908 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo.

## skill v1.8 · 2026-09-06 (auditoría golden-skill-auditor 950/1000 ORO → reparada) · 🟡 RUTA FRÁGI

skill v1.8 · 2026-09-06 (auditoría golden-skill-auditor 950/1000 ORO → reparada) · 🟡 RUTA
     FRÁGIL de la compuerta de verificación: PASO 3 mandaba correr `verificacion_final.py` desde
     `.../<colaborador>/PLANTILLA-MEXICO/`, la carpeta de trabajo de UN colaborador, no un sitio
     canónico compartido — si esa carpeta se archiva o se limpia, la compuerta OBLIGATORIA de
     todas las instalaciones futuras se cae en silencio, y de paso viaja un nombre propio de
     equipo dentro de una skill declarada compartible con la comunidad. Copiado el script a
     `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/verificacion_final.py` (sitio estable, sin dueño
     individual) y añadida degradación elegante: si la ruta no aparece, buscarlo antes de saltar
     el control, y si de verdad no está, la compuerta se sostiene con `golden-verificador` +
     relectura del servidor y el hueco se declara. Nada se borró: el original de un colaborador sigue
     intacto. Pendiente con dueño (no cerrado por esta ronda): la conversación real de prueba
     contra un bot instalado (heredado de la v1.7).

## PARA EL 1000 ME FALTA: una conversación real de prueba contra un bot instalado con esta skill (

PARA EL 1000 ME FALTA: una conversación real de prueba contra un bot instalado con esta skill (mandar el mensaje, ver que responda y que dispare el producto). Lo puede dar: FER, o una corrida real sobre un workspace de control desechable. No lo puedo cerrar yo.

## skill v1.6 · 2026-09-05 (chat de skills/infra, auditoría golden-skill-auditor 935/1000 PLATA → 

skill v1.6 · 2026-09-05 (chat de skills/infra, auditoría golden-skill-auditor 935/1000 PLATA → reparada) · 🔴 GEMELO DE PAÍSES: la regla de oro seguía diciendo "Solo 7 países" cuando el PASO 0 (fix F1 de la v1.5) ya había medido 10 contra el bundle — el fix corrigió un sitio y no buscó el gemelo; quien leía Reglas de oro rechazaba a Argentina/Brasil/Guatemala. Sincronizada. · Comilla suelta al final del cuerpo (artefacto de la migración de description del 2026-09-03) retirada. · JERARQUÍA: el detalle de Techo A/B (tablas medidas, JSON/LONG JSON, caveat de TOPES-NATIVOS) y toda la sección de API (paginación, llaves, gotchas, pares array/Extendido) BAJAN VERBATIM a references/api-y-techos.md con puntero de cuándo leerlo; el cuerpo conserva las reglas duras. Nada se borró: se mudó. · scripts/medir_techos.py NUEVO: mide crudo/escapado contra el techo A (<19.000), tope B opcional y caza caracteres de 4 bytes en triggers; probado contra caso malo conocido (muerde, exit 1) y caso bueno (exit 0). · Description: cláusula corta de derivación a hijas (queda ~974 de 1024). Cambios reportados al Centro de Mando (Estándar 9).

## adenda 2026-08-24 (centro de mando, barrido D del arsenal): (1) BASE DE RUTAS declarada — toda 

adenda 2026-08-24 (centro de mando, barrido D del arsenal): (1) BASE DE RUTAS declarada — toda ruta relativa PROYECTOS/... de esta skill se resuelve contra la carpeta PROYECTOS del Desktop MASTER de la casa (~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/🌐 PROYECTOS); un chat con otro cwd debe expandirla ahí. (2) Blindaje: la skill se re-blinda con chflags uchg al cerrar cada ronda.

## skill v1.5 · 2026-08-28 (verificación ADVERSARIAL con el agente golden-verificador: 54 de 67 re

skill v1.5 · 2026-08-28 (verificación ADVERSARIAL con el agente golden-verificador: 54 de 67 requisitos del briefing cubiertos, 16 fallas → reparadas). Regla que confirma esta ronda: quien construye no verifica. Todo lo de abajo lo encontró un tercero que solo vio el estado final. 🔴 F1 "la plataforma acepta SOLO 7 países" era FALSO — el bundle vivo de la app enumera 10 (COLOMBIA, ARGENTINA, BRASIL, CHILE, ECUADOR, GUATEMALA, MEXICO, PANAMA, PARAGUAY, PERU), los tres "prohibidos" con metadata de primera clase: la skill hacía RECHAZAR instalaciones que la plataforma sí soporta, y de paso acusaba a validacion-direcciones de tener un guatemala.md ilegítimo que resultó legítimo. El briefing está desactualizado ahí. 🔴 F7 "vaciar SIEMPRE [Integraciones] Datos de integracion" no estaba acotado al modo: ejecutado en MODO B le borra al cliente sus tokens vivos de Dropi/Shopify/Meta y le tumba el bot, además de destruir la fuente de verdad que la propia skill usa para identificar su tienda — ahora vale SOLO al clonar hacia un espacio nuevo, JAMÁS en producción. 🔴 F2 "el Logístico no tiene tope en sus campos de texto" era FALSO: pago_anticipado.estrategia_persuasion tiene maxLength 2000 + slice(0,2000) — es la clase de truncado silencioso que la skill enseña a temer, y el validador de la casa ya lo sabía y la contradecía. 🔴 F8 la LEY mandaba grep de marca de origen y "si aparece algo NO se escribe", lo que prohibía escribir Le'côterra, que el encargo EXIGE: la excepción de la LEY ahora es también excepción del barrido (--excepcion). 🔴 F9 la skill mandaba correr verificacion_final.py sin argumentos: son 4 controles (no 5) y el de INTERRUPTORES solo corre con --referencia; sin él sale verde sin auditar ni uno. 🔴 F6 la sección de interruptores del briefing estaba en 0 de 2 y el único texto de la skill decía lo contrario ("respeta los booleans") — un prompt perfecto detrás de un evaluar_direccion:"no" no corre; nuevo PASO 2 bis. 🔴 F11 la sección "reinstalar rompe los disparadores" estaba en 0 de 3, incluida la palabra clave que vive en DOS bot fields y no arranca si difieren en un acento (informacion vs información) — que es justo el trabajo de coherencia del maestro. 🟡 F3/F4 topes 12.000 y 4.000 presentados como "extraídos del código" cuando no existen en el bundle (vienen de capturas), y el 500 atribuido a Comentarios cuando es de Ventas; ahora separados en MEDIDOS / NO MEDIDOS / SIN DOCUMENTAR, con los de Comentarios que faltaban (10.000 y 8.000). 🟡 F5 contradicción interna sobre si el tipo de un campo se cambia (UI vs crear nuevo) → regla única. 🟡 F10 tres umbrales para la misma regla: el validador NO falla a 19.000, solo avisa — el corte operativo lo aplica el orquestador. 🟡 F12 el par array/Extendido estaba en su versión ya desmentida (puede estar poblado de los DOS lados). 🟡 F16 el "60% / mínimo 3 órdenes" era cifra sin fuente y chocaba con feedback_efectividad_sin_umbral. 🟡 F14 el frontmatter no parseaba con YAML estándar (comentario HTML dentro del bloque --- y ": " en un escalar sin comillas) — 7 de 91 skills de la casa comparten el defecto. Añadido además el puente Dropi→Chatea (ficha de operación: novedades reales reescriben el prompt de captura; nunca el export crudo en un bot field) y declarados 3 pendientes con dueño del entregable (img del producto-ejemplo imposible solo por API, valor literal de estado inactivo, orden vaciar/cargar). PENDIENTES DE FUENTE, no de esta skill: TOPES-NATIVOS-POR-CAMPO.md arrastra F2 y F3, y BRIEFING-PARA-SKILLS.md arrastra F1 — hay que remedirlos, y las 6 hermanas que copiaron esa tabla también.

## skill v1.4.1 · 2026-08-24 (centro de mando): bump por las adendas del 24 (base de rutas + blind

skill v1.4.1 · 2026-08-24 (centro de mando): bump por las adendas del 24 (base de rutas + blindaje) que quedaron sin subir versión.

## skill v1.4 · 2026-08-23 (auditoría golden-skill-auditor 804/1000 BRONCE → reparada) · alineació

skill v1.4 · 2026-08-23 (auditoría golden-skill-auditor 804/1000 BRONCE → reparada) · alineación con el BRIEFING-PARA-SKILLS del 2026-08-07, que la skill no había absorbido. 🔴 CRÍTICO 1: el método cien de cien mandaba llenar "al 90-95%, ~18000-19000 crudos" — el techo real son 20.000 ESCAPADOS (~17.000 crudos, tilde=6 chars, emoji=12) y está MEDIDO que 19.922 crudos = 23.266 escapados = el asistente NO arranca, con la API respondiendo 200 ok y guardando cortado: la skill instruía exactamente el rango que mata la instalación. Reescrito como DOS TECHOS con tabla medida y la fórmula len(json.dumps(v)[1:-1]) < 19.000. 🔴 CRÍTICO 2: faltaba por completo el Techo B (tope NATIVO de cada campo del formulario, extraído del código de la app) — escribir por encima funciona por API pero el panel corta el texto al guardar; añadidos los topes más apretados + puntero a TOPES-NATIVOS-POR-CAMPO.md. 🔴 CRÍTICO 3: la definición de terminado era un checklist que llenaba quien construyó — la causa medida de seis fallas seguidas; nuevo PASO 3 COMPUERTA DE VERIFICACIÓN con el agente golden-verificador (adversarial, recibe solo el estado final), verificacion_final.py y relectura del servidor, reportando COBERTURA y nunca "quedó perfecto". 🔴 CRÍTICO 4: mandaba configurar [Logistico] Plantillas de mensaje, campo MUERTO (relleno "namespace":"string"; las plantillas reales viven dentro de Confirmaciones/Seguimiento/Novedad). 🔴 CRÍTICO 5: afirmaba un censo fijo de campos ("los 79", "~69-79") ya falso tres veces (56/69/79/82 según espacio y fecha) — reemplazado por "re-extrae paginando y clasifica lo que HAY". Añadidos: los 7 países que acepta la plataforma con lo que cambia de verdad entre ellos (código postal obligatorio en México, sin recogida en oficina, domicilio=casa) y la advertencia de que un pack clonado hereda el criterio equivocado; Le'côterra siempre inactivo (enseña, no vende); el encargo típico de instalación a cliente con su definición de terminado; la fuga menos obvia al clonar (nombres de producto y paquetería DENTRO de los ganchos de venta del logístico) y la lista de campos a vaciar; gotchas de API (llave data si no 400, create-bot-field con var_type+value si no 422, paginación con per_page ignorado, ensure_ascii/separators, trigger sin caracteres de 4 bytes, cada llave conserva su tipo, producto de Comentarios de 5 llaves exactas, pares array/Extendido donde array vacío NO significa sin productos, img de Comentarios que solo nace subiendo en el panel); valores por defecto que NO son defectos (comparar contra un workspace que funcione, no contra lo que uno supone); description ampliada al disparo real (instalar a un cliente con token, arreglar un espacio heredado).

## skill v1.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): camb

skill v1.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.

## skill v1.2 · 2026-08-21 (auditoría golden-skill-auditor 918/1000 PLATA → reparada) · 🔴 el mapa 

skill v1.2 · 2026-08-21 (auditoría golden-skill-auditor 918/1000 PLATA → reparada) · 🔴 el mapa de hijas declaraba "Dos asistentes tienen skill hija" y omitía por completo `golden-chatea-pro-producto-comentarios` (el hijo de Comentarios, equivalente a prompt-ventas para Ventas: existe, está instalado, y config-comentarios ya lo cita como su propio hijo) — el orquestador dejaba huérfano el paso de cargar la ficha de cada producto en el asistente de Comentarios. Corregido en la tabla de asistentes, en el párrafo de hijas (ahora TRES), en PASO 1 (Comentarios invoca a producto-comentarios por cada producto) y en el mapa de derivación; sumado un chequeo de coherencia de producto entre Ventas/Carritos/Comentarios en PASO 2.

## skill v1.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª cate

skill v1.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio).

## skill v1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "

skill v1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta.

## v1.0 · sin sello previo

v1.0 · sin sello previo


## v1.8 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

### 1 · 🔴 EL ORQUESTADOR NO CONOCÍA LA PLANTILLA DE FÁBRICA

Medido antes de tocar: **cero menciones** de la plantilla de fábrica, del PASO 0 de auditoría o
del detector, en los tres archivos de la skill.

Es el hallazgo más caro de esta ronda porque es **de ecosistema, no de archivo**: el 06-sep se
midió que la plataforma instala los cuatro asistentes con **61 de 61 campos idénticos byte a byte**
entre un espacio de Colombia y uno creado eligiendo México —nace colombiana elijas lo que elijas—
y las cuatro hijas de config incorporaron su PASO 0 AUDITAR. **El que las coordina no se enteró.**

Con eso, el orquestador mandaba a las hijas a configurar sobre campos que **parecen configurados y
son de fábrica**: dos biografías falsas y contradictorias (5 años en el logístico, 7 años y 3.000
clientes en comentarios, en el mismo espacio), un asesor que ya se llama Santiago, teléfono de
relleno, la ley colombiana en la garantía de un negocio peruano, y `pais: colombia` en los campos
de Carritos.

**Nace el PASO 0·A**, y va **delante del encuadre**: se audita antes de preguntar nada. No
reimplementa el detector — usa el de la hermana logística, que está probado — y **lee su línea de
COBERTURA** antes de creerle: si dice `LECTURA INCOMPLETA` o `EL CRUCE DE PAIS NO SE PUDO HACER`,
eso no es el universo y se resuelve antes de repartir.

### 2 · Y la auditoría ahora VIAJA a las hijas, que es la razón de ser de esta skill

`PASO 1` pasaba a cada hija *"país + VÍA + datos base"*. Ahora pasa también la clasificación
**FÁBRICA / TOCADO / VACÍO**. El motivo no es ahorrar: si cada hija relee los 61 campos por su
cuenta, **dos pueden clasificar distinto el mismo campo** cuando el espacio cambia entre lecturas,
y entonces una respeta un dato que la otra pisa. Esta skill existe para preguntar una vez y
repartir; medir una vez y repartir es lo mismo.

Escrito además que **lo TOCADO manda sobre cualquier respuesta del intake**: es dato que el negocio
ya puso, y si el intake dice otra cosa se le pregunta cuál vale, no se sobrescribe en silencio.

### 3 · El último resto de la puerta de país

La sección de países decía *"remídelo contra el bundle antes de **rechazar a un cliente por su
país**"*. La medición era buena; la frase dejaba el rechazo sobre la mesa. Reescrita: aquí no se
rechaza a nadie por su país. Si no está en la lista se investiga lo que falte y se configura igual;
si además la plataforma no lo ofrece, eso se dice **como dato, no como negativa**.

### 4 · El 31% del SKILL.md era changelog en comentarios HTML

13 bloques, **14.989 bytes de 48.277**. Un comentario HTML en el cuerpo se paga en cada activación
aunque nadie lo lea — y esta skill es la que **arranca una instalación completa**, así que ese peso
se paga siempre. Bajaron verbatim a este archivo. SKILL.md: 48.277 → **36.912 bytes**, y eso
incluyendo las dos secciones nuevas.


## 2026-09-07 · barrido de publicación: el NOMBRE DE UN COLABORADOR salía en un acta

El acta de la v1.5 citaba una ruta de trabajo real, `.../<nombre>/PLANTILLA-MEXICO/`, para explicar
un defecto correcto: el PASO 3 mandaba correr un script **desde la carpeta de trabajo de una
persona**, no desde una ruta del sistema. El defecto estaba bien cazado; **el ejemplo llevaba el
nombre**, y vivía dentro del `SKILL.md` como comentario HTML.

**Es el segundo caso idéntico del mismo día** (el otro fue en `config-carritos`), y por eso el
patrón queda escrito como clase, no como caso:

🔴 **Un dato escondido en un comentario HTML está igual de publicado que uno a la vista, y encima
nadie lo audita** — al revisar la skill nadie lee los comentarios, pero el repo se los lleva. La
compuerta `golden-barrido-publicacion` sí los mira ("árbol entero, comentarios HTML incluidos"), y
en los dos casos el nombre solo salió a la luz **al mover las actas fuera del cuerpo y correr la
compuerta como parte del cierre**. Mover el changelog no creó el problema: lo hizo visible.

**Regla:** la compuerta se corre **antes de cerrar cualquier skill**, no solo antes de publicar.
Sustituido por una referencia neutra; el nombre no vuelve aunque se cite el acta.

### 5 · `medir_techos.py` tampoco tenía banco, y es el que decide si un asistente vive

Es el tercer validador de la familia sin autoprueba encontrado el mismo día (los otros dos:
`validar.sh` de prompt-ventas y `validar_producto.py` de producto-comentarios). Mide los DOS
techos —el escapado de 19.000 y el nativo del panel— y pasarse **no da error**: la API responde
`200 ok`, guarda cortado y el asistente muere sin un solo mensaje.

Banco nuevo, **7 de 7**, con contraprueba: al desactivar el límite en una copia cae a 5 de 7
nombrando los dos casos correctos.

**Su caso clave es el 3, y explica para qué existe el script:** 4.000 tildes son 4.000 caracteres
crudos y **~24.000 escapados**. Un valor que en crudo cabe de sobra revienta el campo por escapado.
Si ese caso deja de morder, el script está midiendo crudos y no sirve para nada.

## 2026-09-07 · CUPO DE LA API repartido a toda la familia (orden de FER)

**Dato de FER vía el desarrollador de Chatea, verificado contra la API viva:** el límite es
**1.000 peticiones por HORA**, pasarse **bloquea una hora entera**, y la respuesta trae el contador:

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: <las que quedan>

En inglés **X-RateLimit-Limit** y **X-RateLimit-Remaining**. **Se repone cada hora.**

🔴 **La trampa está en el CUÁNDO, no en el cuánto.** No viene `x-ratelimit-reset`: el servidor no
dice a qué minuto empezó la ventana. Observado por nuestro lado: dentro de la misma hora el
contador **solo baja** — no gotea crédito, se repone de golpe. Por eso, si te bloqueas, se espera
una **hora completa** desde ese momento y se comprueba **mirando** el contador
(`golden-chatea-cupo`, 1 petición), nunca calculándolo.

**Hasta hoy ninguna de las diez skills leía ese contador.** Se trabajaba a ciegas y el bloqueo
aparecía a mitad de la operación.

**Reparto, y cada bloque está escrito para SU skill** —lo que cambia entre ellas es cuánto cuesta
y qué se rompe si el cupo se agota a mitad; un bloque idéntico en diez sitios sería ruido:

· **Con CÓDIGO** (leen el contador de cada respuesta, avisan y no reintentan ante un 429):
  `chatea-auditoria` (comprueba antes de arrancar sus 137 peticiones y se niega si no caben),
  `chatea-operacion` (cuenta lo gastado; su coste **no es constante**),
  `config-logistico` (el PASO 0 de las cuatro hijas y el orquestador),
  `config-ventas-wp` (**el que escribe**, donde un 429 a mitad deja la config a medias).
· **Con DOCTRINA en el cuerpo** (producen texto o JSON que otro escribe por API):
  `config-carritos`, `config-comentarios`, `full-configuracion`, `producto-comentarios`,
  `prompt-ventas`, `validacion-direcciones`.

**Cobertura: 10 de 10.** Herramienta de casa: `golden-chatea-cupo [token] [--necesito N]`.

## v1.9 · 2026-09-09 · MANDATO DE ARQUITECTA (FER) + el censo de hijas estaba VIEJO

**Orden de FER, verbatim:** *"Ya le hago instrucciones a todas las Skill de Chatea Pro, y tú eres
la última, porque tú eres la que básicamente configuras todo Chatea Pro. Entonces, cuando yo
quiera hacer una configuración, yo te voy a llamar a ti para que lo hagas, o sea, que comunícate
con las Skill, con el centro de mando y toma todas las instrucciones, pero tú eres el arquitecto
de todas las Skill de Chatea Pro."*

### 1 · Se hornea el MANDATO en el cuerpo, no en el changelog
Sección nueva justo bajo el H1: `## MANDATO: soy la ARQUITECTA de la familia Chatea Pro`. Va en el
CUERPO a propósito: un mandato que solo viva en un acta no cambia la conducta de la próxima
activación, que es donde se decide si esta skill se comporta como puerta de entrada o como una
hija más. Seis reglas, y ninguna inventa autoridad nueva:
1. **Es la puerta de entrada** de cualquier configuración de Chatea Pro.
2. **Va de última** en la cola de instrucciones: recoge lo que FER ya repartió a las hermanas.
3. **Se pone al día REMIDIENDO** y consultando al Centro de Mando **antes** de molestar a FER.
4. **Recoge y reparte como FILA**: no edita skills ajenas por su cuenta.
5. **Informa SIEMPRE al Centro de Mando**, aunque FER la haya autorizado directo.
6. **La autoridad no cambia: FER → Centro de Mando → skill.** Arquitecta es quien COORDINA y
   REPARTE, no quien manda. Ser la última en la cola no la pone por encima de nadie.

### 2 · 🔴 El mapa de hijas decía 7 y en disco hay 8
Medido el 2026-09-09 con `ls -d ~/.claude/skills/golden-chatea-*`: faltaba
**`golden-chatea-pro-config-remarketing`**, que apareció después de que este mapa se escribiera. El
orquestador habría repartido una instalación completa **sin el remarketing**, y nada habría dado
error: se entrega un bot que simplemente no le vuelve a escribir a quien ya compró.

**LA CLASE, que es lo que importa: una enumeración cerrada que nunca se remide.** Es el mismo
fallo que ya se pagó dos veces con la lista de países (decía 7 cuando eran 10). Un número de
hermanas dentro de una skill **caduca solo**, porque la familia crece por fuera de este archivo.
**La cura no es corregir el 7 por un 8** —eso caduca igual el día que nazca la novena—: el mapa
queda declarado **foto fechada** y lleva encima la orden de **remedir antes de repartir**. Se
reparte contra lo que HAY en disco, no contra lo que este archivo recuerda.

### 3 · Frontera declarada: hijas ≠ hermanas de OPERACIÓN
`golden-chatea-auditoria` (audita la INSTALACIÓN) y `golden-chatea-operacion` (audita el DÍA) no
son hijas y no se llaman en un reparto de configuración. Estaban sueltas en el mismo directorio y
un censo hecho con `ls` las habría adoptado como hijas — el remedio del punto 2 creaba este riesgo,
así que se cierra en el mismo acto.

### Cobertura de esta ronda
Universo: 3 archivos tocados de los 4 de la skill (`SKILL.md`, `references/changelog.md`;
`references/api-y-techos.md` y `scripts/medir_techos.py` **sin cambios**, y se dice para que no se
lea como que se revisaron). Método: censo medido contra disco, no de memoria. **Sin verificar:**
sigue pendiente lo de siempre — una conversación real contra un bot instalado (ver más abajo
"PARA EL 1000 ME FALTA"). Este acta no lo cierra.

## v1.10 · 2026-09-21 · FILA del CdM aplicada: se cae la autorización del cliente en MODO B

**Origen:** cambio de estándar autorizado por FER el 19-sep en el chat "Datos para instalación y
optimización de Chatea Pro", repartido por el Centro de Mando como FILA a esta fábrica el
2026-09-21. La misma fila fue a `golden-chatea-pro-config-ventas-wp` por su intake.

**Qué cambió (MODO B, puntos 5 y 6):**
1. Se retira el paso de **"diagnóstico al dueño ANTES de tocar... el dueño autoriza"**. El
   diagnóstico interno se sigue haciendo — es la base de la cobertura medida — pero ya no se
   pausa a esperar el visto bueno del cliente antes de corregir identidad y comportamiento.
2. **Única pregunta que SÍ se le hace al cliente:** el corte de flete caro (desde qué valor un
   flete es "demasiado caro", el punto de "cliente no calificado"). Se suma al default de país
   ya calculado para los 10 países, nunca lo reemplaza.
3. **No se promete informe de cambios al cliente.** La verificación interna (el "Reporte
   obligatorio de cambios" que ya llevaba esta skill) sigue igual de obligatoria: es cobertura
   nuestra, nunca una promesa comercial.
4. Se deja anotado que lo único adicional que se le pide al cliente es **no entrar a configurar
   el espacio mientras se trabaja**.
5. **Verificado antes de tocar el archivo:** esta skill no menciona la promoción del segundo mes
   gratis en ningún punto (barrido con grep, cero coincidencias) — no había nada que retirar
   en ese frente, así que no se inventó un cambio donde no lo hay.

**Lo que NO se tocó, a propósito:** el punto 7 (nombre del asesor y datos de identidad JAMÁS se
cambian sin preguntar) sigue igual — esos datos vienen del intake de los siete datos que ya se le
piden al cliente al inicio, no de una autorización a mitad de instalación, así que no hay
contradicción con el punto 5 nuevo. Tampoco se tocó el intake interno del PASO 0·B (país, vía,
datos base de marca): es la pauta operativa de Golden para construir, no el mensaje que se le
manda al cliente — ese mensaje de los siete datos es propiedad de la fábrica que arma el intake
de cara al cliente, y la fila dice que ya se le entregó a `config-ventas-wp`.

**Compuertas:** `agentskills validate <ruta absoluta>` → exit 0. `validar_arsenal.py` → 1 de 1,
cero fallos, mismo aviso de siempre (cuerpo largo, ahora 555 líneas, encarece pero no falla).
md5 SKILL.md ANTES → DESPUÉS: `8eb951dec30f35a8eb839b8a4feebb03` → `be62e1c8d43fef305d4eaeee1ff32c95`
(1 artefacto cambiado, medido con `golden-blindaje --cerrar`, blindaje repuesto).

**Sin verificar:** sigue pendiente lo de siempre, una conversación real contra un bot instalado
con esta skill. Esta fila no lo cierra.

## v1.11 · 2026-09-21 · 2ª pasada de la misma fila: el cambio se había quedado a medias

**Origen:** el Centro de Mando verificó la v1.10 y encontró que la corrección solo tocó la
sección que nombraba el cambio (MODO B, puntos 5-6) y dejó **tres apariciones sueltas de
"autorización" contradiciéndolo** en el resto del cuerpo:

- `SKILL.md:109` (v1.10) — "se corrige con autorización", hablando del mismo MODO B.
- `SKILL.md:463` (v1.10) — un interruptor apagado "se enciende con autorización".
- `SKILL.md:523` (v1.10) — "identidad se mejora solo con autorización", en Reglas de oro.

**La clase, y esta skill ya la tenía escrita para el caso JSON-vs-prosa, solo que ahora le pasó a
la prosa contra la prosa:** *"Un cambio de estándar se aplica al DATO que el código lee, no solo
a la prosa."* Corregir una sección y dejar vivas otras tres que dicen lo contrario deja una skill
que se contradice según por dónde se abra — que es exactamente el defecto que el propio archivo
advierte contra el `limites.json` de países.

**Corrección:** se barrió `grep -in autoriz` sobre el archivo COMPLETO (12 apariciones) y se
clasificó una por una:
- **Cliente (corregidas, 3):** las tres líneas de arriba. `:109` ahora remite al punto 5 nuevo;
  `:463` distingue explícito "HALLAZGO de comportamiento, no valor de negocio del cliente" y
  quita la espera; `:523` queda "se mejoran con el criterio de Golden, sin esperar autorización"
  y conserva intacta la excepción del nombre del asesor.
- **FER → esta fábrica (intacta, 1):** línea 40, el mandato de arquitecta — no es del cliente.
- **Producto-ejemplo Le'côterra (intactas, 3):** líneas 63, 89, 500 — "autorizado" ahí describe
  la única excepción de dato heredado permitida, no autorización del cliente.

**Barrido adicional** de formas alternas (permiso, consulta, espera el visto/ok/aval, dueño
autoriza): cero coincidencias — no había una cuarta forma de decir lo mismo escondida en otra
palabra.

**Compuertas:** `agentskills validate` → exit 0. `validar_arsenal.py` → 1 de 1, cero fallos
(cuerpo ahora 557 líneas, mismo aviso de peso de siempre). md5 se captura al cerrar blindaje.

**Sin verificar, y esto no lo cierra:** sigue faltando una conversación real contra un bot
instalado. Corregir prosa no es lo mismo que ejercer el caso — no hay un "correr el caso que
antes fallaba" ejecutable para texto que instruye a un humano/agente, solo el barrido de
consistencia hecho arriba.

## v1.12 · 2026-09-22 · FILA del CdM: el remarketing sale del ecosistema

**Origen:** orden directa de FER (21-sep-2026). El CdM borró `golden-chatea-pro-config-remarketing`,
su memoria, respaldos y extracción, y regeneró el registro de fábricas (universo 41, cero sin
declarar). Repartió la fila a esta fábrica por ser el orquestador: el mapa de hijas y la ficha de
operación Dropi la citaban.

**Universo barrido:** `grep -in remarketing` sobre el archivo completo, 4 apariciones, las 4
clasificadas antes de tocar nada:
- `SKILL.md` (mapa de hijas, era línea 548 en v1.11) — la fila "🔄 Remarketing IA →
  `golden-chatea-pro-config-remarketing`" se RETIRÓ del mapa. Vuelve a ser 4 hijas de
  configuración (comentarios, logístico, ventas-wp, carritos).
- Tabla de la ficha Dropi (era línea 309) — `validaciones_orden` de Ventas, Logístico **y
  Remarketing** (los tres coherentes) → se quitó "y Remarketing", queda "de Ventas y Logístico
  (los dos coherentes)". Esa fila cruzaba contra un campo de un asistente que ya no existe.
- Sección del censo (era línea 538) — el ejemplo de "la familia crece" citaba
  `config-remarketing` por su nombre propio. Siguiendo el propio criterio del CdM en sus memorias
  ("la lección se queda, el nombre se va"), se reescribió sin el nombre propio y se AMPLIÓ la
  lección: no solo "la familia crece", **también se achica**, y el censo se remide en los dos
  sentidos, no solo cuando aparece una hija nueva.
- `[Carritos] ... con recordatorios y remarketing` (línea 145) — **NO se tocó**. Es el
  remarketing genérico de recuperación de carritos de `config-carritos`, no el asistente
  `[Remarketing IA]` retirado. Barrer la palabra a ciegas aquí habría sido el error que el CdM
  advirtió explícitamente.

**Doctrina nueva agregada** (no pedida palabra por palabra, pero necesaria para que la skill no
tropiece la próxima vez que alguien la use sobre un espacio que aún tiene el remarketing):
1. Si el encargo pide configurar remarketing, se dice que salió del ecosistema, no se inventa ni
   se busca una hija que no está.
2. El campo `Producto Remarketing` del asistente de **Ventas WhatsApp** y sus recordatorios NO
   son esto — se aclaró la frontera para que nadie los confunda ni los toque por error.
3. **Excepción viva, medida el 2026-09-21 por el CdM:** el asistente retirado sigue instalado en
   **Dolce Incanto** y **Le'côterra**, 9 campos cada uno, por decisión de FER. Si un MODO B de
   esta skill cae sobre uno de esos dos espacios, esos campos se IGNORAN: no se desinstalan ni se
   configuran. Sin esta línea, un MODO B futuro sobre esos dos espacios habría tratado esos
   campos como basura de plantilla a limpiar o como un asistente a configurar — ninguna de las
   dos cosas es correcta.

**Compuertas:** `agentskills validate` → exit 0. `validar_arsenal.py` → 1 de 1, cero fallos
(cuerpo ahora 570 líneas, mismo aviso de peso de siempre). md5 se captura al cerrar blindaje.

**Sin verificar:** no hubo forma de ejecutar esto contra un espacio real de Dolce Incanto o
Le'côterra en esta ronda — la excepción de "se ignoran" queda escrita pero no probada contra un
MODO B real sobre esos dos espacios. Sigue pendiente también lo de siempre: una conversación real
contra un bot instalado con esta skill.
