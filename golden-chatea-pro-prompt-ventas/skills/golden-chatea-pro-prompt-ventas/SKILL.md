---
name: golden-chatea-pro-prompt-ventas
description: >-
  Monta un PRODUCTO en el asistente de ventas por WhatsApp de Chatea PRO: el campo del producto Y su paquete
  de venta juntos — saludo, multimedia, pregunta de entrada, prompt de venta, recordatorios, remarketing y
  activador — y TAMBIÉN MEJORA prompts que el usuario ya tenga. Úsalo SIEMPRE que quiera crear, armar, cargar,
  optimizar, auditar o MEJORAR un producto o un prompt de ventas para Chatea PRO, un asistente/bot/agente de
  ventas por WhatsApp, venta contra entrega o pago anticipado, o diga cosas como "monta este producto en
  ventas", "carga este producto en el asistente", "hazme el prompt de [producto]", "necesito un agente de
  ventas para WhatsApp", "arma el asistente de Chatea PRO", "ya tengo un prompt, mejóralo", "revisa el prompt
  de mi bot", "este prompt no me vende", "configura la venta conversacional" — o cuando PEGUE un prompt de
  ventas existente pidiendo opinión o mejora. Si dudas, dispáralo: un prompt sin esta estructura convierte
  menos.
---

**Versión viva:** v3.65.0 · 2026-09-29 · el acta completa en `references/changelog.md` (no se lee para trabajar).
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1010 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO (actualizado v3.46.1): la compuerta que MANDA es el validador OFICIAL de la especificacion, ya instalado:
         agentskills validate ~/.claude/skills/golden-chatea-pro-prompt-ventas     (salida 0 = en norma)
     El chequeo propio 'validar_arsenal.py' SIGUE SIRVIENDO para las reglas de FER, pero NO es autoridad sobre la especificacion: corrido sobre esta skill devolvia 0 mientras IMPRIMIA "VALIDADOR OFICIAL: NO INSTALADO (se usa el chequeo propio, equivalente pero no oficial)". Un verde que se apoya en un sustituto no es un verde. Para publicar, el oficial.
     Y OJO CON EL PIPE: 'agentskills validate ... | head' devuelve el codigo del head, no el del validador. Captura el exit ANTES de cualquier tuberia — esta trampa ya costo dos falsos veredictos en esta misma skill.
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->

# Constructor de Prompts de Venta para Chatea PRO v2
<!-- skill v3.53.0 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): esta skill tenía DOS validadores y NINGÚN banco — nadie había comprobado nunca que mordieran. Nace scripts/autoprueba.sh (15 de 15, sabotaje por pieza). El validador no miraba la contaminación de la plantilla de fábrica (asesor 'Santiago', biografía '5 años de experiencia') ni tenía canal de AVISOS: era binario, bloquea o pasa. Y le faltaba sk-ant- entre las credenciales. Historial completo en references/changelog.md. -->

**Fábrica: chat ✅ SKILL golden-chatea-pro-prompt-ventas** — solo esa fábrica numera versiones y edita; cualquier otro chat entrega FILA al Centro de Mando (Ley del Cambio Único, FER 2026-08-25).

## 📋 Requisitos: qué necesita del usuario antes de arrancar

- **El producto, el país y el precio de 1 unidad** · BLOQUEANTES: son los tres obligatorios del intake (`references/intake-inteligente.md`). Si falta uno, se pregunta antes de construir.
- **Combos, variantes, beneficios y modelo de pago** · DEGRADABLES: se deduce lo posible y para lo que falte se propone un valor por defecto, marcado en el borrador como supuesto. La transportadora y los tiempos de entrega no se preguntan: van por defecto según el país.
- **El nombre del asesor** · DEGRADABLE: se pregunta en cada caso, porque es de tu negocio. Si no lo das, el prompt queda marcado como pendiente de ese nombre: nunca se inventa ni se hereda de otro espacio.
- **Garantía, regalo o bono, envío discreto, producto original** · DEGRADABLES: se preguntan una vez; si no existen, se omiten y se dice. Jamás se inventan: el bot se los prometería a un cliente real.
- **Las cuentas del pago anticipado** (titular, entidad, número y tipo de cuenta), si el producto lo usa · DEGRADABLES: se preguntan; si no las tienes a mano, el prompt queda con el marcador `[AQUÍ VAN LOS DATOS DE PAGO ANTICIPADO]` y se avisa que falta. Nunca se inventan ni se heredan de otro espacio (LEY NUNCA HEREDAR).
- **Un espacio de Chatea PRO con el asistente de ventas ya instalado, y su token de API** · BLOQUEANTES para montar el campo del producto. El token se crea en el panel del espacio, va atado al Bot y se guarda en `<carpeta del cliente>/.secrets/`, como en `golden-chatea-pro-full-configuracion`; jamás va dentro del prompt. Si el asistente no está instalado, eso es `golden-chatea-pro-config-ventas-wp`. Sin espacio con token se entrega el bloque copiable listo para pegar, que se entrega SIEMPRE de todos modos.
- **bash y Python 3**, que usa `scripts/validar.sh` para medir los techos de cada campo · DEGRADABLES: sin `python3` el script no corre, los caracteres se cuentan a mano y la entrega avisa que esa medición no la verificó el script.
- **El perfil de WhatsApp del negocio** (foto, descripción, datos de contacto y enlaces) · DEGRADABLE: vive en tu negocio y no en el prompt, pero el cliente lo ve antes de leer una palabra; la skill lo verifica antes de entregar (`references/estructura-disparo.md`, apartado 0). Si no está listo, se dice.
- **Upsell, envío gratis y revisión del paquete** · DEGRADABLES: si hay upsell y a qué precio, si está activo el módulo de Upsells nativo de Chatea, desde qué cantidad el envío es gratis y si el cliente puede revisar el paquete antes de pagar. Lo del módulo nativo se pregunta siempre: con él activo el bot no hace su propio ofrecimiento (variante A) y sin él sí (variante B). Si no hay respuesta, la entrega dice qué variante se aplicó.
- **Las URLs de las imágenes del flujo** · DEGRADABLES: se piden; si no las tienes, se generan o se entrega el prompt de imagen, y el prompt se cierra cuando las subas a Chatea PRO (manifiesto de imágenes).
- **Las plantillas de WhatsApp de los remarketing** · DEGRADABLES: la skill entrega cada plantilla completa para crearla en tu WhatsApp Business, pero la aprueba Meta, no la skill. Mientras no esté aprobada, no se da por montada.
- **La foto del producto y el cerebro de marca** (`golden-brand-brain`) · DEGRADABLES: sin foto se trabaja con los datos escritos; sin cerebro se ofrece crearlo, y si sigues sin él la entrega lo declara.
- **Firecrawl, la biblioteca de anuncios de Meta, un generador de imagen y `golden-pdf-check`** · DEGRADABLES: si uno no está, se dice y se sigue a mano (sección "Conexiones"). Sin Firecrawl se piden los datos al vendedor; sin la biblioteca se usa `references/objeciones.md`; sin generador se entrega el prompt de imagen; sin `golden-pdf-check` no hay PDF del paquete.

**Si falta algo BLOQUEANTE: no se hace lo que depende de él** y se pide con nombre propio: qué es, dónde se saca y dónde se pone. **Si falta algo DEGRADABLE: se pide y se sigue**, dejando marcado como pendiente o como supuesto todo lo que depende de él. Nunca se presenta como completo. Si no tienes algo, dime y te guío paso a paso.

## Paso 0 · Cerebro de marca (obligatorio antes de generar)

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.

El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta (buscar con find ANTES
de crear, naming MAYÚSCULAS-CON-GUIONES) la declara `golden-brand-brain`: ante cualquier duda de ruta,
invócala en vez de adivinar.


## LEY: NUNCA HEREDAR DATOS ENTRE ESPACIOS (FER 2026-08-08)

Al basarse en una cuenta guía (Golden o cualquier otra) se hereda **estructura, prompts y
configuración de asistentes** — JAMÁS datos, en ninguna dirección, ni entre marcas propias:

- **APIs y tokens** de cualquier tipo: ElevenLabs, OpenAI, Dropi, Shopify, el token del propio bot.
- **Plantillas de WhatsApp**: `name`, `namespace`, `lang` y `status` van atados al WABA de cada
  espacio; copiarlas rompe el destino (llama plantillas que su WABA no tiene o que Meta no aprobó).
- **Datos personales y de marca**: teléfonos, correos, dominios, nombre de la empresa, firmas en
  mensajes al cliente.
- **Productos** y sus disparadores.
- **Claims y cifras de negocio**: años en el mercado, número de clientes, porcentajes de
  entrega, premios. Heredarlos no rompe nada técnico — ningún barrido de llaves los detecta —
  pero ponen al bot a MENTIRLE al cliente con datos de otra empresa. Caso real (2026-08-08): la
  plantilla maestra clonada traía "Más de 100.000 clientes atendidos en Colombia" (dato de
  Golden) a punto de quedar en boca del bot de otro espacio.

**Única excepción autorizada:** Le'côterra como producto-ejemplo en los espacios de trabajo
(asistente de WhatsApp y de comentarios), para que la gente vea cómo se configura un producto.

**La guía tampoco puede llevar nada de eso adentro**: un material de referencia con una llave o un
dato personal ya está mal, aunque nadie lo copie.

**Método obligatorio al escribir en un espacio ajeno** — ANTES de escribir, barrer lo que se va a
escribir buscando `sk_`, `shpat_`, `eyJ`, teléfonos, correos, dominios, nombres de plantilla y de
marca del origen; si aparece algo, NO se escribe. DESPUÉS de escribir: releer del servidor y barrer
otra vez. Herramienta encadenable del barrido (referencia interna del ecosistema Golden, ruta
relativa al proyecto del dueño, NO viaja dentro de esta skill):
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (correrla ANTES de escribir y DESPUÉS releyendo del
servidor; sale con código 3 si encuentra algo CRITICA). **Si esa herramienta no existe en el
entorno** (skill compartida fuera del ecosistema Golden): haz el mismo barrido a mano con grep por
esos patrones + el nombre de la marca de origen sobre TODO el texto antes y después de escribir —
el método manual descrito arriba es el fallback, nunca te saltes el barrido por falta del script.

**LA MARCA VIVE TAMBIÉN EN PROSA LIBRE, no solo en campos estructurados.** Preservar las
llaves de identidad del destino NO basta: el nombre de la marca de origen viaja escondido dentro
de ganchos posventa, agradecimientos y plantillas de prompt. Al método de barrido se le añade el
paso `grep -i` por el NOMBRE de la marca de origen sobre TODO el texto que se va a escribir —
así se cazaron 10 menciones de la marca origen en 3 campos del destino que el mapeo de llaves
no vio.

Origen: 2026-08-08, al clonar la config de Golden a otro espacio se colaron la llave de ElevenLabs,
el teléfono, la plantilla de notificación y agradecimientos firmados con la marca del origen.
Revertido el mismo día desde respaldo.

### CAMPOS [Meta] = VALORES CALIENTES, NO INTERRUPTORES

Los bot fields `[Meta] Ver Contenido`, `[Meta] Agregar al carrito` y demás eventos de pixel los
**MUEVE EL FLUJO en tiempo real** mientras corren contactos — no son configuración estable. Caso
real (2026-08-08): se leyeron como "apagados" y cambiaron solos minutos después sin escritura de
nadie; la conclusión "el evento Comprar está apagado" tuvo que retractarse. **PROHIBIDO sacar
conclusiones de pauta o diagnóstico de una lectura suelta de esos campos**: se observan en ventana
(varias lecturas separadas en el tiempo) o se diagnostica el pixel en Meta directamente. Detalle:
memoria `reference_chatea_clonar_config_entre_espacios`.


Este skill convierte cualquier producto en un paquete de venta completo y listo para pegar en Chatea PRO v2, siguiendo una estructura probada en campo (referencias con 50+ ventas/día). El objetivo siempre es el mismo: **convertir conversaciones de WhatsApp en ventas confirmadas.**

## Flujo de Chatea PRO v2 (contexto obligatorio)

El asistente se dispara así:
```
palabra clave → SALUDO INICIAL → MULTIMEDIA → PREGUNTA DE ENTRADA → (cliente responde) → se activa el PROMPT
```
Todo lo que diseñes debe encajar en esa secuencia. Además existen RECORDATORIOS (dentro de la ventana de 24h) y REMARKETING (plantillas que reabren la conversación después de horas).

## 🔴 CUPO DE LA API: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.
Medido contra la API viva el 2026-09-07: cada respuesta trae **`x-ratelimit-remaining`** (en
inglés *X-RateLimit-Remaining*, "las que quedan") y `x-ratelimit-limit`. **Se repone cada hora**,
pero **no viene `x-ratelimit-reset`**: el servidor no dice a qué minuto empezó la ventana, así que
si te bloqueas se espera una **hora completa** y se comprueba **mirando** el contador
(`golden-chatea-cupo [--necesito N]`), nunca calculándolo.

**Cuándo te afecta aquí:** esta skill produce TEXTO —el prompt y su paquete— y no toca la red. El
cupo entra cuando ese prompt **se escribe** en el bot field del producto. Es barato (una escritura
más su relectura), pero **se suma al de la instalación completa** si estás montando varios
productos seguidos: diez productos son al menos veinte peticiones, más las del resto de la
instalación.

## Fronteras y desambiguación (esto vive AQUÍ y no en la description, que tiene tope duro de 1.024)
La description lleva **solo lo que dispara**. El alcance, las capacidades y las fronteras van en el cuerpo, que no tiene tope. Si algún día hay que meter un disparador nuevo y no cabe, lo que sale es de aquí arriba — nunca una frase que la gente dice de verdad.

**ALCANCE.** Cualquier producto físico, cualquier modelo de pago (contra entrega o anticipado), en los **10 países que acepta la plataforma** (pack completo para 8; ver `references/paises.md`). Servicios e intangibles: cubiertos a medias y declarado en `references/intake-inteligente.md`.

**CAPACIDAD DE MEJORA.** Cuando llega un prompt existente, no se comenta: se **evalúa /100 y /1000**, se marca lo crítico con evidencia y se **reconstruye a nivel superior**.

**LOS TRES CASOS SE DERIVAN DE LO QUE LLEGA — NO SE PREGUNTA CUÁL ES.** Preguntarlo es hacerle al usuario el trabajo de clasificar su propio encargo:
1. **Llega un producto Y hay espacio con token** → se monta el campo del producto y su paquete de venta.
2. **Llega un producto SIN espacio** → se entrega el bloque copiable, listo para pegar.
3. **Pegan un prompt existente** → es mejora: se evalúa y se reconstruye.
⛔ **El bloque copiable se entrega SIEMPRE**, se haya montado o no. Así el usuario nunca se queda sin la versión pegable, y la pregunta "¿me lo das para copiar?" deja de existir.

**FRONTERAS CON LAS HERMANAS.** Instalar el asistente por primera vez en una tienda (una sola vez, sin producto) → `golden-chatea-pro-config-ventas-wp`. La rama de comentarios tiene su propio par: `golden-chatea-pro-producto-comentarios` monta un producto de comentarios igual que esta monta uno de ventas.

## DOS MODOS DE USO

**Modo CONSTRUCCIÓN (por defecto):** el usuario quiere un prompt nuevo. Sigue PASO 0 → 4 (0 intake · 1 entrevista · 2 construir · 2.5 PDF · 3 y 3.1 auto-evaluación · 4 medición). Nota: los "PASO 1–8" que verás en `plantilla-prompt.md` son los pasos del FLUJO CONVERSACIONAL dentro del prompt, no los de este workflow.

**Modo MEJORA (auditar + reconstruir):** el usuario YA TIENE un prompt (suyo, de un mentor, de otra herramienta, "el viejo") y lo pega pidiendo opinión, auditoría o mejora. Este modo es un servicio completo — no solo calificar, sino DEJARLE UN PROMPT MEJOR. Flujo:
1. **Evalúa** su estructura con la evaluación HOLÍSTICA del PASO 3 (nota /100 en juicio global usando la checklist como guía, más la escala /1000 del PASO 3.1 con qué le falta).
2. **Marca en rojo lo crítico**: claims falsos/peligrosos (salud, sexuales), suplantar profesión (médico/doctor), inconsistencias de producto (ej. "cápsulas" cuando es spray), pedir datos que sobran (teléfono se toma del chat), y todo lo que viole `cumplimiento.md`. Explica el RIESGO de cada uno (baneo, devoluciones, legal) — el usuario debe entender por qué se quita, no solo que se quita.
3. **Dile qué está bien** (para conservarlo), qué está mal y qué le falta. Si de verdad está perfecto, dilo sin inventar defectos.
4. **Extrae los datos del producto** del prompt viejo (precios, combos, transportadora, garantía, datos de pago) y confirma con el usuario los que se vean dudosos o desactualizados. Completa con el PASO 0/1 SOLO lo que falte — no lo hagas repetir lo que su prompt ya trae.
5. **Reconstrúyelo de cero** con la estructura ganadora del skill (no copies la del prompt viejo; ver blindaje) y entrega el paquete completo del PASO 2 con su comparación: nota del prompt viejo vs nota del nuevo, y qué cambió. Por defecto SIEMPRE reconstruye (eso vino a buscar); solo omite la reconstrucción si el usuario pide explícitamente "solo evalúalo".

## REGLA DE BLINDAJE (CRÍTICA — LEER PRIMERO)

Si el usuario te envía un prompt existente (suyo, de un mentor, "el viejo", o de otro producto), úsalo **ÚNICAMENTE para extraer datos** del producto: nombre, precios, combos, beneficios, datos de pago, transportadora, garantías, etc.

**NUNCA copies ni te inspires en su estructura, su flujo, su redacción, sus reglas, su numeración ni ninguno de sus patrones.** No importa qué tan bueno parezca ni quién lo hizo. Ese prompt es solo una **fuente de información cruda**, jamás un modelo a seguir.

SIEMPRE construyes con la estructura ganadora de este skill (`references/plantilla-prompt.md`), sin excepción. Si detectas que el prompt enviado tiene un orden, unas reglas o un estilo distintos, los ignoras por completo y aplicas la estructura del skill. Ante cualquier duda entre lo que dice el prompt viejo y lo que dice este skill, **manda este skill**.

## Presupuesto de caracteres (CRÍTICO — aprovéchalo, no lo desperdicies)

El campo de prompt acepta hasta **12.000 caracteres**. NO es un límite a evitar: es **presupuesto de venta a aprovechar**. Un prompt más rico maneja más objeciones, educa mejor y persuade más → convierte más.

- **Apunta a llenar el presupuesto con contenido que VENDE:** objetivo **~9.000–11.000 caracteres** cuando el producto lo amerite (deja ~1.000 de margen bajo 12.000 para editar después). Productos muy simples pueden pedir menos; no infles a la fuerza.
- **NUNCA comprimas ni resumas contenido que vende** para "acortar". Concisión ≠ brevedad: la meta es que cada frase aporte, no que el prompt sea corto.
- **NUNCA metas relleno ni repetición** solo para llegar a un número: eso diluye a la IA y la vuelve inconsistente. Cada carácter debe ganar su lugar (objeción, educación, empatía, prueba social, manejo de escenario).
- Regla práctica: si un prompt te queda en 4.000–6.000, casi seguro te FALTA sustancia (FAQ, objeciones, escenarios). Revisa qué venta te dejaste por fuera antes de entregar.
- SIEMPRE mide el prompt final con `scripts/validar.sh` y repórtalo (JAMÁS con `wc -m`: cuenta bytes según el locale y miente). Techo duro del campo: 12.000.
- **EL SEGUNDO TECHO (el que mata en silencio): el bot field guarda el valor ESCAPADO.** El campo JSON aguanta 20.000 caracteres ESCAPADOS, no crudos: cada tilde ocupa 6 y cada emoji 12, así que el techo práctico ronda ~17.000 crudos para el bot field completo (probado en vivo: 16.882 crudo/19.895 escapado dispara; 19.922/23.266 NO — y el producto muere sin error visible, el fallo solo sale en Panel → Registros de errores). Un prompt de 11.000 lleno de tildes y emojis puede reventar el campo aunque quepa en 12.000. Mide el escapado con `len(json.dumps(valor)[1:-1])` y déjalo bajo 19.000 (validar.sh lo calcula). MATIZ del techo escapado: el tope de 20.000 escapados aplica a los bot fields legacy tipo JSON; los campos LONG JSON aguantan 500.000 (todo campo NUEVO se crea LONG JSON) — pero el tope NATIVO del formulario (12.000 el prompt) rige igual porque el panel corta al guardar. Tabla completa de topes por campo: `CHATEA-PRO-ASISTENTES-MAPA/TOPES-NATIVOS-POR-CAMPO.md` (referencia interna del ecosistema Golden; los topes operativos ya están reproducidos aquí).
- **Topes de los campos vecinos** (no solo el prompt) — **cada uno tiene su modo en el validador: `validar.sh --campo saludo|pregunta|remarketing|recordatorio|prompt-datos|notificacion <archivo>`**: mensaje inicial (saludo) 1.000 · pregunta de entrada 1.000 · instrucción de remarketing 1.000 c/u · recordatorio 800 · prompt_datos del Producto en Segundos 4.000 · notificaciones 400. Escribir por API sobre el tope no da error, pero el día que alguien abra el formulario en el panel y guarde, el campo SE CORTA.

## PASO 0 — Intake inteligente (recolecta e investiga; ver `references/intake-inteligente.md`)

Antes de construir, hazle la vida fácil al vendedor. **Intake CONVERSACIONAL: UNA PREGUNTA A LA VEZ (modo por defecto, orden de FER 2026-08-26):**
- Haz **UNA sola pregunta, espera la respuesta, y con ella pasa a la siguiente**. Nada de mandar el cuestionario completo de golpe: un muro de preguntas abruma y la gente abandona o responde a medias. Sé cálido y humano, como un chat de verdad.
- Empieza por el PRODUCTO (pidiendo URL o foto, que es lo que más acelera), sigue por el PAÍS, y de ahí en adelante pregunta solo lo que aún falte.
- **Relleno inteligente:** con lo que responda, la skill DEDUCE lo que pueda (moneda/indicativo del país, tono por producto, beneficios de la URL/foto) y PROPONE defaults sensatos para lo que falte, marcándolos como supuestos. Solo REPREGUNTA si falta un **OBLIGATORIO** (precio de 1 unidad, país, producto). Todo lo demás no bloquea: se propone y se confirma en el borrador.
Pregunta TODO lo que mejora el prompt, pero UNA COSA A LA VEZ, esperando cada respuesta (orden de FER 2026-08-26). Nunca en bloque.
- Excepción: si el vendedor pega varios datos juntos por su cuenta, o pide explícitamente que le mandes todo de una, agrúpalo — se respeta su ritmo. Ese es el único caso del formulario completo; jamás el arranque por defecto.
- Aplica **el gate de pago**: "Vas a solicitar pago anticipado?" → si SÍ, pide los datos de la cuenta; si NO, no preguntes nada de anticipado.
- Acepta el producto como venga: **URL(s)** (scrapéalas), **foto** (analízala con visión) o **nada** (investiga producto y competidores en la web / Meta Ad Library). Con eso arma un borrador de ficha.
- Pregunta SOLO lo condicional que aplique (variantes solo si el producto las tiene; datos de anticipado solo si dijo que sí; imágenes según `recursos-visuales.md`).
- Confirma el borrador (precio, combos, claims) con el cliente ANTES de construir. Lo investigado acelera; el precio real y los claims SIEMPRE se confirman, nunca se inventan.

## PASO 1 — Entrevista (completa lo que falte del intake, antes de construir)

⛔ **Solo los BLOQUEANTES detienen la construcción: producto, país y precio de 1 unidad** (ver "Requisitos" arriba). Todo lo demás de esta lista es **DEGRADABLE**: se deduce lo que se pueda, se propone un default y se marca como supuesto en el borrador. Esta línea decía "no construyas nada hasta tener estos datos" y contradecía la regla de degradables, que es la vigente: con un dato degradable ausente **sí se construye**, declarando el supuesto. Esta lista es el INVENTARIO de lo que hay que averiguar, NO un cuestionario para mandar de golpe: se recorre UNA PREGUNTA A LA VEZ (PASO 0), esperando cada respuesta. Si el usuario ya dio algunos en la conversación o en la URL/foto, no los preguntes: dalos por resueltos, confírmalos en el borrador y pregunta solo lo que falte.

REGLA DE DATOS POR NEGOCIO (CRÍTICA — este skill es genérico y se comparte con otras tiendas/usuarios): el **nombre del asesor/a** y los **datos de pago anticipado** son SIEMPRE específicos del negocio para el que se construye el prompt. Pregúntalos en cada caso; nunca los heredes de otro negocio ni los dejes hardcodeados en el skill. ⛔ **LOS TIEMPOS DE ENTREGA Y LA TRANSPORTADORA NO SE PREGUNTAN** (regla de FER, y esta línea decía lo contrario hasta el 2026-09-27): van **por defecto según el país** (`references/paises.md`), se muestran en el borrador **marcados como supuesto**, y se ajustan solo si el vendedor los corrige. Son igual de específicos del negocio que los demás —así que tampoco se heredan de otro espacio—, pero la forma de resolverlos es el default por país, no una pregunta más al vendedor. Para el pago: primero confirma si el negocio quiere cobrar **anticipado** (además de o en vez de contra entrega); si dice que sí, pídele los datos (Nequi/Daviplata/banco + titular + número + llave). Excepción: si por contexto o memoria ya conoces estos datos del **dueño de esta copia del skill**, úsalos solo para él; jamás para terceros.

**Sobre el producto:**
1. Qué producto es? (nombre, qué hace, para quién)
2. Tiene variantes/líneas? (sabores, colores, modelos). Y OJO: el combo se vende **por unidad** o **por cantidad fija** (ej. combo de 12/docena)? Si es por cantidad, esas unidades **se pueden mezclar entre variantes** o van de una sola? (ver "combos por cantidad" en `plantilla-prompt.md`).
3. Beneficios reales (qué gana el cliente, emocional + funcional)
4. Algún dato sensible? (no es medicamento, sin registro sanitario, etc.)

**Sobre precio y oferta:**
5. Precio por 1, 2 y 3 (unidades **o combos**, según cómo venda; di cuántas unidades trae cada combo). **El precio de al menos 1 (unidad o combo) es OBLIGATORIO para generar el prompt.**
6. Hay upsell post-venta? A qué precio? Y CRÍTICO: está activo el módulo Upsells NATIVO de Chatea (tarjetas automáticas con imagen y botón tras la compra)? Si SÍ, el prompt NO hace pitch propio — solo procesa las tarjetas (variante A del PASO 8 en plantilla-prompt.md); si NO, el bot hace el pitch (variante B). Verifica también que la suma de tarjetas cuadre con la tabla de combos.
7. Envío gratis? Desde qué cantidad?

**Sobre la operación:**
8. Modelo de pago: contra entrega, anticipado o ambos?
9. Si hay anticipado: datos completos de la cuenta (titular + banco/entidad + número/llave + TIPO de cuenta)
10. Si permite revisar el paquete antes de pagar (política del negocio). La TRANSPORTADORA no se pregunta: default del país (paises.md), solo se registra si el vendedor la nombra o excluye por su cuenta
11. País y nomenclatura de dirección (Colombia: barrio/ciudad/departamento · México: colonia/municipio/estado/CP · etc.)
12. ~~Tiempos de entrega~~ — NO SE PREGUNTAN (regla de FER): default por país en paises.md, mostrados como supuesto en el borrador
12b. (OPCIONAL) **ID del producto en Dropi** (solo números) y si el producto **tiene variaciones**. Son para la sección "Información del producto" y se pueden agregar después; NO son necesarios para generar el prompt.

REGLA DE OBLIGATORIOS Y NO BLOQUEO:
- **OBLIGATORIO (sin esto NO se genera el prompt):** el precio de al menos **1 (unidad o combo)**. Un agente de ventas sin precio no sirve. Los precios de 2 y 3 (unidades o combos) son deseables pero opcionales; si solo hay el de 1, trabaja con ese y arma el prompt igual. Si vende por combo de cantidad fija, di cuántas unidades trae cada combo.
- **OPCIONAL (no bloquea):** ID de Dropi, precio del campo "Información del producto" y las URLs de imágenes. Pregúntalos una vez; si el usuario no los tiene, sigue adelante y deja nota de que se agregan después.
- **URLs/imágenes:** si el usuario aún no tiene los enlaces, NO bloquees. Inserta en el prompt un **marcador claro y etiquetado** en el punto exacto donde va cada imagen, nombrando qué imagen es **según el producto**. Ejemplos: `[AQUÍ VA LA URL DE LA IMAGEN DE COLORES]`, `[AQUÍ VA LA URL DE LA IMAGEN DE MODO DE USO]`, `[AQUÍ VA LA URL DE LA IMAGEN DE ANTES/DESPUÉS]`, `[AQUÍ VA LA URL DE LA TABLA DE PRECIOS]`, `[AQUÍ VA LA URL DE TESTIMONIOS]`. Tú decides qué imagen corresponde a cada momento del flujo según el producto; el usuario solo pega el enlace cuando lo tenga.

**Sobre la marca y el tono:**
13. Nombre del asistente y personalidad (cálida, directa, etc.)
14. Prueba social real (nº de clientes, reseñas, testimonios)
15. URLs de multimedia disponibles (ver `references/checklist-multimedia.md`)
16. Tiempos deseados de recordatorios y remarketing

**Sobre confianza (clave para cerrar):**
17. El envío es discreto? (vital en productos íntimos o sensibles)
18. Hay garantía de CAMBIO? (JAMÁS devolución de dinero — regla v3.7: la política de la tienda manda)
19. Hay algún regalo o bono por la compra?
20. Es producto original (anti-réplica)?

Si el usuario no sabe alguno, propón un valor sensato y márcalo como supuesto para que lo confirme.

## PASO 2 — Construir el paquete

Genera SIEMPRE estas piezas, en este orden. Usa `references/plantilla-prompt.md` como esqueleto del prompt y `references/estructura-disparo.md` para saludo, multimedia, pregunta, recordatorios y remarketing. Aplica el pack del país del negocio (`references/paises.md`) para dirección/transportadora/pago, e inserta las objeciones que apliquen desde `references/objeciones.md`. Toma `references/ejemplo-completo.md` como vara de calidad de la salida.

1. **Saludo inicial** (cálido, con nombre del asistente, crea expectativa) — ⛔ SIN PREGUNTA. Chatea envía en secuencia automática saludo → multimedia → pregunta de entrada; el saludo NUNCA pregunta (si no, el cliente responde antes de la multimedia y luego se le vuelve a preguntar). La única pregunta que espera respuesta es la pregunta de entrada.
2. **Plan de multimedia** (qué piezas y qué texto en cada una)
3. **Pregunta de entrada** (segmenta al cliente en los caminos que el prompt sabe responder)
4. **Prompt completo** (estructura ganadora, bajo el límite de caracteres)
5. **Recordatorio 1 (2h) y 2 (6h)** — suaves, SIN plantilla ni instrucción de IA (solo el mensaje; van dentro de la ventana de 24h).
6. **Remarketing 1 (3h) y 2 (8h)** — cada uno con ángulo nuevo. En Chatea cada remarketing tiene 3 campos: **Tiempo** (3h/8h), **Plantilla Mensaje** (desplegable: se elige una plantilla de Meta aprobada o "No enviar plantilla"), e **Instrucción especial del remarketing** (un campo ≤1000 caracteres con el MENSAJE + la [Instrucción IA] juntos). La skill entrega los tres: el texto del campo de instrucción (copy-paste) + la plantilla de Meta completa para crear/seleccionar (nombre_minúsculas, categoría Marketing, español, imagen, cuerpo con {{1}}=nombre, pie, botón mapeado como "botón de remarketing"). Ver `estructura-disparo.md`.

FUENTE DE VERDAD de los 4 tiempos fijos (Recordatorio 1=2h, Recordatorio 2=6h, Remarketing 1=3h, Remarketing 2=8h — RM2 a 8h para no COLISIONAR con R2, que cae a las 6h): los dos puntos anteriores (5 y 6). Se repiten en `estructura-disparo.md` y `guia-configuracion-chatea.md` para que cada archivo se lea solo; si algún día cambian, edita los 3 a la vez (grep `2 horas\|2 horas\|3 Horas\|6 Horas` en `references/`).
7. **Activador — NORMA DE DOS ACTIVADORES por producto** (aprobada por el Centro de Mando 2026-08-07, chat dental Chile): se registran **DOS** palabras clave por producto:
   - **(1) La FRASE COMPLETA del anuncio/botón** (ej. "Hola quiero información y precio de [PRODUCTO]"), con el nombre del producto. Cubre los canales donde el enlace **precarga** el mensaje (botón de la página, CTA de WhatsApp en Meta).
   - **(2) UNA palabra corta ÚNICA y propia del producto** (ej. estilo "SONRISA" para gotas dentales, "HONGOS" para antihongos). Cubre **TikTok, estados de WhatsApp y comentarios**, donde NADA precarga y el cliente escribe a mano: sin ella el bot no dispara y la venta se pierde en silencio. Esa palabra corta se usa en **todo CTA escrito** ("escribe SONRISA").
   - **VERIFICACIÓN obligatoria de la palabra corta**: compararla contra TODAS las palabras clave de los demás productos del bot para que no se cruce. **JAMÁS palabras genéricas** ("información", "precio", "promo"): con varios productos disparan el bot equivocado.
   - **SIN NINGÚN EMOJI ni símbolo raro en ningún activador** — los de 4 bytes están PROBADOS: la base de Chatea los vuelve `�` y el trigger no coincide jamás (incidente 2026-07-26); los de 3 bytes (✨ ✅ ‼ ⁉ ℹ) no están probados contra la base, así que el default seguro es CERO. Y sin punto final. Texto crudo para copiar y pegar, sin prefijos ni comillas. **LA validación es `bash scripts/validar.sh --activador <archivo>`** (lista permitida: solo letras, números y puntuación básica; bloquea cualquier emoji de 3 o 4 bytes y el BOM) — la fórmula manual de 4 bytes NO basta, deja pasar ✨ y vecinos.

IMPORTANTE — DÓNDE VA CADA PIEZA: el paquete NO va todo en un solo campo. Cada pieza va en una sección distinta de Chatea. Entrega SIEMPRE el mapa de ubicación al usuario (ver `references/guia-configuracion-chatea.md`) y etiqueta cada pieza con la sección donde va, para que cualquier persona lo configure sin enredarse. No presentes la numeración como un orden secuencial dentro de un solo campo.

ENTREGA COPY-PASTE POR CAMPO (crítico — cada campo SEPARADO): cada pieza va con su **título como encabezado FUERA del bloque copiable**, y el **bloque copiable contiene ÚNICAMENTE el texto exacto que se pega** (nada de título, nada de anotaciones adentro). Así, cuando el vendedor copia el bloque, obtiene solo el texto, sin el título.
- Recordatorio 1 y Recordatorio 2 = CADA UNO su propio título + su propio bloque separado (no los juntes en un solo bloque).
- Remarketing 1 y Remarketing 2 = igual, cada campo de la plantilla claramente separado (nombre, cuerpo, pie, botón, instrucción IA).
- Etiquetas LIMPIAS, solo el nombre del campo, SIN paréntesis ni descripciones ("RECORDATORIO 1", no "R1 (2h)"; "REMARKETING 1", no "RM1 (confianza)"). El tiempo (2h/6h/3h/6h) va en el texto del informe, no dentro del bloque copiable.
- Palabras clave / mensajes: texto crudo dentro del bloque, sin "Palabra clave:" ni comillas.
El vendedor solo copia y pega. Debajo de todo va el MANIFIESTO DE IMÁGENES (no dentro del prompt).

REGLA DE MULTIMEDIA (crítica): hay dos tipos de audiovisuales y van en lugares distintos:
- Multimedia INICIAL (se envía al entrar) → va en "Contenido multimedia inicial", NO en el prompt.
- URLs que el AGENTE envía DURANTE el chat (modo de uso, tabla de precios, testimonios) → van ESCRITAS DENTRO del prompt, con la instrucción de cuándo enviarlas. En el prompt solo va la URL (o el marcador `[IMAGEN N — URL]` si aún no la hay).

SISTEMA DE IMÁGENES (ver `references/recursos-visuales.md`): además del prompt, entrega SIEMPRE un **MANIFIESTO DE IMÁGENES debajo del prompt** (nunca dentro). Por cada imagen conversacional (IMAGEN 1, 2, 3…): pregunta al cliente si tiene la URL; si la tiene, la pegas en el prompt; si NO la tiene, (a) **intenta generarla tú** si hay herramienta de imágenes conectada (Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch), o (b) entrégale un **prompt de imagen profesional** listo para pegar en cualquier IA; luego explícale que la suba a Chatea PRO para obtener la URL y te la pase, y tú finalizas el prompt con el enlace puesto. La skill intenta hacerlo todo; si no puede, dice exactamente cómo.

DATOS DE PAGO ANTICIPADO: si el negocio cobra anticipado, PREGÚNTALE al cliente (durante el desarrollo) los datos completos de la cuenta — titular + banco/entidad (Nequi/Daviplata/Bancolombia/etc.) + número/llave + TIPO de cuenta — y colócalos en la sección de anticipado del prompt. Nunca los inventes ni los dejes en blanco: si no los tiene a mano, deja el marcador `[AQUÍ VAN LOS DATOS DE PAGO ANTICIPADO]` y avísale que hay que completarlo.

## PASO 2.5 — Entregable PDF (recomendado; ver `references/entrega-pdf.md`)

Además de entregar el paquete copy-paste en el chat, **genera un PDF profesional** del paquete completo con la skill `golden-pdf-check` (estándar Golden, bloques atómicos anti-corte). Hazlo por defecto cuando el usuario quiera un documento para guardar, pasarle a un cliente o configurar sin depender del chat; y SIEMPRE que lo pida.

Reglas clave (detalle en `references/entrega-pdf.md`):
- Cada pieza copiable va en su propia **tarjeta** de prompt (` ``` `): saludo, pregunta de entrada, prompt, recordatorios, remarketing, activador, y los prompts de imagen.
- El **prompt de venta es largo** (suele pasar de 9.000 caracteres): no cabe legible en una página. **Pártelo en tarjetas "Parte 1 de N, Parte 2 de N…" y avisa que van SEGUIDAS, en orden, dentro del MISMO campo** (Prompt personalizado). El texto no cambia ni un carácter: solo se reparte. Apunta a que cada parte quede a tipo legible (si el build reporta `fit_warnings` con tipo < ~8pt, parte esa tarjeta en dos).
- Incluye la portada (marca), el mapa de configuración, el manifiesto de imágenes con los prompts de imagen, y una sección final de "qué falta por completar".
- Invoca `golden-pdf-check` (ella trae su propio motor: build + auditoría + compuerta verbatim; esta skill no tiene scripts de PDF). Entrega solo si el veredicto es APROBADO y el verbatim pasa (el prompt salió idéntico, copiable). Si esa skill no está disponible, entrega solo el copy-paste e infórmalo.

## PASO 3 — Auto-evaluación HOLÍSTICA (no entregues sin esto)

Antes de entregar, SIMULA tú mismo una conversación haciendo de **cliente difícil** (pregunta precio de entrada, objeta "está caro", desconfía, da datos incompletos/desordenados, elige pago anticipado y cambia un dato, pregunta por otro producto).

Luego **evalúa el prompt COMPLETO como un todo y califícalo del 1 al 100** — NO sumes puntos por ítems para llegar a 100. Es un juicio de calidad global: lee el prompt entero como si fueras un experto en venta conversacional y dale la nota honesta que merece. Si algo falla, la nota baja de verdad.

Usa esta lista como **guía de lo que debe tener un prompt excelente** (checklist para tu juicio, NO una suma):
- Da el precio de inmediato cuando lo piden, enmarcado, sin esconderlo.
- Pago anticipado blindado (nunca confirma sin comprobante válido).
- Captura de datos en un mensaje + validación anti-error.
- Objeciones reales cubiertas (caro, funciona, seguro, médico/legal sin claims, "lo pensaré", otro producto).
- Espeja el dolor antes de vender; no repite la pregunta de entrada.
- Da la RAZÓN DE PREFERENCIA (por qué a este negocio y no a otro) con diferenciales reales, en positivo, sin desprestigiar a nadie.
- Usa ANTES/DESPUÉS real cuando el cliente duda si funciona, con disclaimer y sin retoque.
- Pregunta la CAUSA del chat antes de recomendar, y construye la CONEXIÓN ASPIRACIONAL (deseo profundo + diferenciador + comparación de valor + casos reales) antes de dar precio.
- **Cero testimonios inventados:** si aparece un nombre o caso que el vendedor no entregó, el prompt está MAL y no se entrega, por buena que sea la nota en todo lo demás.
- **Suena a ASESOR, no a vendedor:** cada pregunta lleva su propósito declarado delante, entiende antes de ofrecer, recomienda con criterio (incluso la opción menor o un "esto no es para tu caso") y no presiona nunca. Si al leerlo se siente que empuja el producto, la nota baja fuerte por más que cumpla lo demás.
- Conteo de combos correcto + matemática de upsell (costo incremental + beneficio).
- OFICINA según la política del negocio.
- Aprovecha el presupuesto (~9.000–11.000 con sustancia, sin relleno; techo 12.000).
- Tono humano (≤35 palabras, ≤2 emojis, sin signos de apertura de pregunta/admiración, nunca robótico, nunca dice que es IA).
- Upsell solo tras el cierre. FAQ/educación de producto. Cumplimiento (sin claims falsos).

REGLA DE ENTREGA: la nota /100 es holística (no se suma por ítems), pero el piso de entrega SÍ es concreto: **por debajo de 90 no se entrega**. Si la nota queda bajo 90 (o si algo de la checklist falla aunque el puntaje total parezca alto), corrige lo que falle, vuelve a simular y repite hasta pasar el piso. Entrega mostrando: (a) la simulación del cliente difícil, (b) la **nota /100 con una justificación en prosa** (qué lo hace fuerte, qué se mejoró), y (c) el conteo de caracteres.

## PASO 3.1 — Escala 1 a 1000 (para llevarlo al máximo)

Después del /100, evalúa también **del 1 al 1000** y di explícitamente **qué le harías para llegar a 1000**. La escala /1000 es más exigente: mide qué tan cerca está del mejor prompt posible para ESE producto (profundidad de objeciones y FAQ, riqueza persuasiva, ángulos de la competencia, prueba social concreta, manejo de todos los escenarios de entrada, unit economics del upsell, etc.). Entrega el número /1000 + la lista concreta de mejoras que lo subirían.

🔴 **ANTES DE CONFIAR EN EL VALIDADOR, COMPRUEBA QUE MUERDE:** `bash scripts/autoprueba.sh`
(26 de 26). Siembra un sabotaje **por cada pieza** contra la vara mínima de la propia skill y
exige que cada uno produzca su bloqueo. Y el banco corre en los DOS sentidos: los casos 17 y 19
exigen que el detector **NO** muerda —"cuida tu corazón", "la reina del hogar", o un encabezado
`PROHIBIDO` con lo prohibido listado debajo—, porque un detector que acusa al idioma bloquea
trabajo bueno y se termina desactivando entero. ⛔ Y el banco **se niega a correr** si no tiene
carpeta temporal escribible o no pudo extraer la vara: sin esa compuerta, un banco roto imprime
veinte chequeos muertos y parece que la herramienta es la que falla (medido el 2026-09-27). Hasta el 2026-09-07 esta skill no tenía banco: dos
validadores, ninguna prueba de que funcionaran. **Si tocas `validar.sh` o
`validar-doctrina.sh`, el banco corre antes y después, y toda corrección nueva entra con su
sabotaje** — si no, la suite cubre lo que ya se arregló y nada de lo que se rompa después.

VALIDADOR AUTOMÁTICO: guarda el bloque del prompt en un archivo y córrelo con `bash scripts/validar.sh <archivo.txt> [límite]`. El script mide con python (crudos + escapados + emojis + BOM) y BLOQUEA con exit distinto de 0 si excede un techo, está vacío o no es UTF-8 — no es informativo, es una compuerta. Además corre `bash scripts/validar.sh --activador <archivo>` sobre CADA activador: ahí exige 0 emojis de cualquier tipo y sin BOM. No estimes a ojo ni uses `wc -m`. DEPENDENCIA: el script necesita `python3` en PATH (sin librerías externas, solo `json`/`sys` de la librería estándar). Si `python3` no está disponible en el entorno, el script no corre: cuenta los caracteres a mano con un contador de puntos de código Unicode (nunca `wc -m`, que cuenta bytes bajo locale C) y avísale al usuario que la medición fue manual, no verificada por script.

CUMPLIMIENTO OBLIGATORIO: antes de entregar, pasa también el checklist de `references/cumplimiento.md` (claims de salud, política de WhatsApp, datos personales). Un claim prohibido invalida la entrega aunque la nota sea 100.

CHECK DE DISPARO (además de la evaluación del prompt): verifica que el **saludo NO contenga pregunta** y que el texto de la multimedia tampoco; la ÚNICA pregunta que espera respuesta es la **pregunta de entrada**. Si el saludo pregunta algo, corrígelo antes de entregar.

## PASO 4 — Medición y versionado (cierra el bucle)

Un prompt no se "termina": se mejora con lo que pasa en campo. Al entregar, incluye SIEMPRE un bloque corto de seguimiento para que el usuario pueda medir y tú puedas mejorar la próxima versión:

1. **El versionado NO va en el prompt.** El header del prompt lleva SOLO `Producto · País · Compañía` (sin "v1", sin fecha). El número de versión y la fecha se llevan aparte, en el `resultados-ledger.md`. El prompt que se pega en Chatea queda limpio.
2. **Hipótesis de la versión:** una línea de qué apuesta hace esta versión (ej. "precio más temprano + garantía reforzada para bajar el 'lo pensaré'"). Va en el ledger, no en el prompt.
3. **Las métricas a vigilar** (el detalle y el método en `references/medicion.md`, que es la fuente) (el usuario las saca de Chatea PRO / su CRM): % que llega a captura de datos, % que confirma con SÍ, % de anticipados con comprobante. Si una está baja, indica qué punto de la checklist revisar.
4. **Prueba A/B sugerida:** propón UNA sola variable a testear en la siguiente versión (un hook, el orden del precio, la garantía), nunca varias a la vez.

Cuando el usuario vuelva con resultados, lee la versión anterior, ajusta la variable y entrega v+1 con su nueva hipótesis. Así el skill aprende del negocio real, no solo de la teoría.

REGISTRO DE RESULTADOS: lleva el historial en `references/resultados-ledger.md` (una fila por versión: hipótesis, métricas reales, qué A/B ganó, aprendizaje). Antes de construir una versión nueva, LEE el ledger de ese producto y parte de lo que ya ganó — nunca desde cero. Es lo que convierte al skill en un sistema que compone aprendizaje.

## Reglas de oro de la estructura ganadora
- **PRIMERO LA FICHA, DESPUÉS EL PROMPT.** Los 7 campos de `ficha-producto.md` se llenan antes de escribir una línea: el deseo profundo alimenta la conexión, el diferenciador el contraste y la comparación de valor el ancla. Si un campo queda vacío, ese es el trabajo pendiente — no se rellena con lo que suena razonable.
- **LA COMPARACIÓN DE VALOR ES UN NÚMERO REAL.** El múltiplo ("5 veces más barato que una sesión") se calcula con dos precios verificables y se dice contra qué se compara. Inventarlo es la mentira más fácil de desmontar: el cliente conoce el precio de la alternativa mejor que tú.
- **EL OBJETIVO ES PERSUADIR Y VENDER, no informar** (doctrina Golden, FER 2026-09-02 · `reference_estandar_venta_conversacional_golden`). Un prompt que responde bien y no cierra está MAL, por limpio que sea. Entrar en la mente del cliente, entender su caso, comunicar beneficios y cerrar con la convicción de que no hay mejor producto ni mejor empresa donde comprarlo.
- **LA IDENTIDAD VARÍA, LA CALIDAD DEL PROCESO NO.** Marca, tono, país y nicho DEBEN cambiar entre espacios — eso no es defecto, es diseño. Lo que no puede variar es el proceso persuasivo: diagnóstico, conexión, oferta, manejo de objeciones, cierre, tramo logístico y reactivación. **No hay un molde único: hay un estándar de calidad.** Nunca marques como error que un prompt suene distinto a otro; márcalo si le falta un tramo del proceso.
- **LA VENTA NO TERMINA EN EL PEDIDO.** En COD el cliente sigue tibio hasta que paga: confirmación, despacho y NOVEDADES son parte de la venta (una novedad sin rescatar es una venta perdida después de ganada), y tras la entrega viene la reactivación.
- **LA OFERTA HACE EL TRABAJO, NO LA PRESIÓN (FER 2026-09-01).** Arma cada oferta con los 9 elementos de `oferta-irresistible.md`: el valor percibido debe superar al precio APILANDO VALOR REAL (bonos que quitan obstáculos, garantía que quita riesgo, mecanismo único) y declarando el valor total ANTES del precio. ⛔ Jamás se le dice ni se le insinúa al cliente que sería tonto no comprar: eso es agresión y rompe el tono asesor. Los elementos 7 y 8 (urgencia y escasez) solo entran si son REALES.
- **ELIGE LA MECÁNICA DE OFERTA, NO USES SIEMPRE LA MISMA (2026-09-23).** Antes de escribir el PASO 0.9, decide CÓMO se presenta el valor: comparación de precios (Hoy vs Antes, el default), salto de valor, obsequios o por cantidad. **Se elige por dónde vive el valor de ESE producto** — si no hay un "Antes" real, la comparación de precios no la tienes, y forzarla obliga a inventar el precio anterior. El menú con su criterio está en `oferta-irresistible.md`. ⛔ El gancho por envío (cobrarlo en la opción 1) NO se usa: contradice la regla fija de envío y la escalera ya produce ese empuje sola.
- **NO SE ACOTA UN BENEFICIO PERMANENTE (clase de ofertas grand slam, lámina 15, 2026-09-29).** Acotar un claim lo hace creíble porque enciende **escasez** y **reciprocidad** y le da una razón lógica a la oferta — eso es lo que mata la sospecha de "demasiado bueno para ser verdad". ⛔ **Y por eso la acotación no puede ser falsa:** si el envío es gratis SIEMPRE, decir "por ser cliente nuevo" o "en tu primera compra" fabrica una exclusividad que no existe; el cliente vuelve, ve que era igual para todos, y se cae la credibilidad de TODA la oferta, no solo esa frase. Se acota donde hay un límite REAL; si el beneficio es permanente, se dice plano. `validar.sh` bloquea el prompt que declara el envío gratis siempre **y** lo ofrece como concesión, porque esa contradicción vive dentro del mismo texto y sí se puede medir.
- **DOS VARAS, DOS RANGOS (arbitraje del Centro de Mando 2026-09-01).** `ejemplo-minimo.md` = flujo núcleo, 4.000-6.000, para enseñar o para arrancar sin insumos — NUNCA como entrega final. `ejemplo-completo.md` = salida real, 9.000-11.800. Mide cada una con su modo: `validar.sh --minimo` y `validar.sh`.
- **⛔ LA URGENCIA ES REAL O NO EXISTE.** Prohibido "la promo es de hoy", "últimas unidades", "te lo aparto" o "el precio sube mañana" si no es cierto, y prohibido un precio "Antes" inflado para simular descuento. Es la misma mentira que un testimonio inventado y produce el mismo rechazo en COD. Urgencia válida: stock real confirmado, fecha real de fin, tiempos de despacho, rotativa honesta.
- **EL CIERRE SE CONSTRUYE DESDE EL PRIMER MENSAJE (FER 2026-09-01).** Detonadores repartidos —compromiso propio, reciprocidad, prueba social y autoridad reales, micro-síes, pérdida real, facilidad— para que llegue a la compra de forma intuitiva. Si al final hay que empujar, es que no se sembró antes.
- **SALTOS DE LÍNEA (FER 2026-09-01):** en WhatsApp un muro de texto no se lee. Precios, oferta, captura, resumen y confirmación van AIREADOS, una idea por línea y una línea en blanco entre bloques.
- **PRESENTACIÓN DE LA OFERTA (PASO 0.9):** las 3 opciones con Hoy vs Antes REAL, etiquetas ciertas ("la más pedida", "mayor ahorro" calculado), obsequio y envío solo si son de verdad, diferenciador con validaciones reales, y UNA pregunta al final.
- **RAZÓN DE PREFERENCIA: POR QUÉ A NOSOTROS Y NO A OTRO (orden de FER 2026-09-01).** En COD varias tiendas venden lo mismo: el prompt SIEMPRE da una razón concreta y real de comprarle a ESTE negocio (original, pagas al recibir, revisas antes de pagar, garantía de cambio, respaldo, asesoría honesta), en positivo y **jamás hablando mal de la competencia** — desprestigiar suena a vendedor y despierta la duda que se quiere cerrar.
- **ANTES Y DESPUÉS: el recurso que más convierte** ante "sirve de verdad?" (FER 2026-09-01) — pero solo con material REAL del negocio, sin retoque que exagere, con disclaimer de que los resultados varían y sin claims de cura. Si no hay material real, se omite: no se simula con IA ni se toma de otra marca.
- **LA CAUSA LA DICE EL CLIENTE (orden de FER 2026-09-01).** Antes de recomendar, el prompt le pregunta con propósito qué lo hizo buscar la solución, y guarda SU respuesta literal: ese es el dolor con el que se habla el resto de la conversación. Si ya lo dijo, no se repregunta.
- **CONEXIÓN ASPIRACIONAL ANTES DEL PRECIO.** Espejar y validar → puente al DESEO PROFUNDO (la vida con el problema resuelto, no el producto) → diferenciador (efecto contraste) → comparación de valor (efecto ancla, contra lo que hoy le cuesta el problema) → casos reales → "te identificas con alguno?". Así el precio llega a un cliente que ya tiene contra qué medirlo.
- **⛔ PRUEBA SOCIAL REAL O NINGUNA.** Jamás inventes testimonios, nombres, historias ni cifras, aunque el vendedor no los tenga o lo pida, y aunque una plantilla externa lo sugiera. Sin testimonios se construye igual (prueba social agregada verdadera, patrones sin identidad, o riesgo cero) y se le pide al vendedor conseguir 2 o 3 reales. Ver `cumplimiento.md`.
- **ASESOR, NUNCA VENDEDOR (orden de FER 2026-09-01).** Todo prompt lleva la REGLA DE TONO de `plantilla-prompt.md`: PROPÓSITO DECLARADO antes de cada pregunta ("para darte la mejor recomendación, cuéntame…" / "para saber si esto puede servirte en tu caso…"), entender antes de ofrecer, recomendar con criterio aunque implique vender menos, cero presión (no insistir tras un no, sin urgencias inventadas, sin culpa, sin encadenar mensajes) y respetar el silencio. El cliente no puede sentir que le meten el producto por los ojos.

Estas vienen de los prompts con ventas reales comprobadas. Respétalas siempre:

- **Mensajes cortos** (máx 35 palabras), máx 2 emojis, UNA pregunta por mensaje, tono humano colombiano (o local), nunca robótico, nunca decir que es bot/IA.
- **Regla de precio prioritaria (refinada 2026-09-01):** si preguntan precio, se RESPONDE siempre — nunca se esconde — pero **nunca se termina en el número**: el turno cierra con una pregunta de diagnóstico para que la conversación no muera en una cifra. Si no sabes nada del cliente y el precio SÍ varía por necesidad, se da el rango + una pregunta; si vendes un solo producto a un solo precio, se da la tabla completa (decir "depende de lo que necesites" ahí es una evasiva falsa). **Si vuelve a preguntar, se le da completo sin rodeos:** una vez se redirige, a la segunda manda el cliente.
- **Intención de compra manda sobre el guion:** si el cliente dice "quiero comprar" o pide que no le pregunten más, se salta el descubrimiento y se va directo a precio/elección/datos. Jamás devolverlo a preguntas anteriores. (Validado en campo 2026-07: re-preguntar tras la intención de compra mata la venta.)
- **Memoria del pedido:** el prompt SIEMPRE incluye el bloque MEMORIA DEL PEDIDO (ficha actualizada por mensaje, audios incluidos, prohibido re-pedir un dato ya dado). Ver `plantilla-prompt.md`.
- **URLs blindadas:** todo prompt con imágenes conversacionales lleva el bloque IMÁGENES — REGLA CRÍTICA DE URLS (solo URLs etiquetadas de la lista, exactas; prohibido reutilizar URLs del historial; 1 imagen por mensaje; ante la duda, solo texto). La IA no ve imágenes: sin esto manda la equivocada.
- **Una sola confirmación:** el resumen respondido con SÍ; nunca "procedemos?"/"confirmo?" extra. Nunca un resumen con campos (Pendiente) o inventados. Tras un upsell aceptado, actualizar resumen sin volver a pedir datos.
- **Detectar antes de vender:** espejear el dolor del cliente con empatía antes de recomendar (solo con quien duda; no aplica a quien ya decidió).
- **Captura de datos en un solo mensaje** + validación anti-error (no avanzar con datos incompletos, ordenar lo desordenado, no repetir lo ya dado).
- **Resumen verificable** antes de confirmar; el cliente confirma con SÍ.
- **Anticipado blindado:** jamás confirmar sin comprobante válido.
- **Upsell solo después del cierre**, sin insistir si rechaza.
- **Matemática de upsell:** al sugerir 2/3 unidades (o combos), calcula y muestra el COSTO INCREMENTAL de la unidad/combo extra (delta = precio(n) − precio(n-1)) + el beneficio (envío prioritario, no interrumpir el proceso, repuesto/regalo). Nunca digas solo "quieres otra?": muéstrale cuánto gana. Ver `plantilla-prompt.md`.
- **Combos por cantidad (docena/pack) con variantes mezclables:** cuando cada combo trae N unidades fijas (ej. 12) y esas unidades se pueden mezclar entre sabores/colores, trátalo así: el "1/2/3" son COMBOS (no unidades sueltas), di siempre cuántas unidades trae cada uno, y en la captura agrega el campo de variante indicando que la suma por combo debe dar N (ej. "6 Pistacho, 3 Nucita, 3 Oreo = 12"). El upsell se calcula por COMBO extra. Ángulos que suben el ticket: regalar, evento, **revender**. Ver `plantilla-prompt.md`.
- **No insistir con la cantidad:** preguntarla una sola vez.
- **Máximo 2 intentos** de reactivación, sin desesperación.
- **Vender el beneficio (frescura, confianza, resultado), no el problema.**
- **Respuestas CONCRETAS, no ambiguas:** cuando el cliente pregunte algo medible (en cuántos días se ven resultados, cuánto rinde, cada cuánto se usa), responde con un **rango concreto** (ej. "muchas personas empiezan a notar cambios entre los 5 y 15 días con uso constante") + "varía en cada persona". Nunca respondas solo "depende" o "varía" sin dar un número. Sin prometer curas ni garantizar resultados.
- **Formato limpio del prompt:** header solo `Producto · País · Compañía` (sin versión). Usa saltos de línea simples; evita viñetas/tabulaciones decorativas innecesarias. Que se lea limpio.
- **La skill intenta hacerlo TODO por el cliente:** si algo lo puede resolver la skill (generar una imagen, calcular, redactar), lo hace; si no puede, le dice al cliente EXACTAMENTE cómo hacerlo y qué pegar. Nunca deja al cliente con un "hazlo tú" sin instrucciones.

## Conexiones (herramientas y skills hermanas)

Esta skill hace UNA cosa: el **prompt de ventas** (y sus piezas) para Chatea PRO. Se apoya en herramientas externas y se coordina con otras skills. Todas son OPCIONALES: si una no está conectada, la skill lo dice y ofrece el camino manual (nunca se rompe).

**Herramientas que usa (si están disponibles):**
- **Firecrawl** (`firecrawl_scrape` / `firecrawl_search`) → leer la URL del producto o de competidores, y buscar en la web. Si no está: pídele al vendedor que pegue los datos.
  🚨 **Verificación obligatoria — 4 checks, porque hay 3 modos de fallo y `statusCode: 200` no
  prueba nada:** existe el campo `json`? (Amazon devolvió muro anti-bot sin `json`) ·
  `metadata.title` poblado? (vacío → el extractor **inventa**: dio un Smart TV con precio y reseñas
  falsos para una página de verrugas) · `metadata.url` == `sourceURL`? (Temu redirigió y devolvió
  72 categorías de ropa, **con title poblado**) · **🎯 el dato responde a lo que pedí?**
  Si falla una: descartar y pedirle los datos al vendedor. **Aquí el riesgo es el más directo de
  todo el ecosistema:** un precio o un "4.5 estrellas" falso metido en el prompt se lo dice el bot
  **al cliente real**, en WhatsApp, como si fuera cierto — y ese cliente compra o se queja con base
  en eso.
  📖 `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`
- **Visión** (nativa) → analizar la foto del producto que envíe el vendedor.
- **Meta Ad Library** → ver anuncios activos de la competencia para ángulos/objeciones reales. Si no está: usa la librería `objeciones.md`.
- **Generadores de imagen** (Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch) → crear multimedia e imágenes conversacionales. Si no hay ninguno: entrega el prompt de imagen para que el vendedor la genere (ver `recursos-visuales.md`).

**Skills hermanas (a qué derivar, sin reimplementar):**
- Config general del asistente de ventas / JSON de la tienda → `golden-chatea-pro-config-ventas-wp`.
- Asistente de COMENTARIOS de Chatea → `golden-chatea-pro-config-comentarios`.
- Asistente LOGÍSTICO (validación de direcciones) → `golden-chatea-pro-config-logistico`.
- Asistente de CARRITOS abandonados → `golden-chatea-pro-config-carritos`.
- Configurar TODOS los asistentes a la vez → `golden-chatea-pro-full-configuracion`.
- Copy de anuncios (Meta/TikTok), hooks, guiones → `golden-copywriting`.
- Imágenes/infografías de alta conversión → `golden-imagen-arena`.
- Avatares/UGC en video → `golden-ugc-avatar`.
- Página de producto Shopify (COD/Releasit) → `golden-shopify`.
- Análisis/armado de pauta → `golden-ads`.
- Entregable en PDF del paquete (bloques atómicos anti-corte) → `golden-pdf-check` (ver PASO 2.5 y `references/entrega-pdf.md`).
Esta skill NO hace pauta, ni página, ni la config general del bot: solo el prompt de ventas y sus piezas de disparo.

## Privacidad (skill compartible con la comunidad)

Esta skill se comparte. NUNCA hornees datos de un negocio real en sus archivos: nombres de asesor, precios, cuentas de pago (Nequi/Daviplata/banco), números, marcas o tiendas específicas se PREGUNTAN en cada uso y viven solo en el prompt que se entrega, jamás en la skill. Los ejemplos internos (FreshKlin, Valentina, etc.) son FICTICIOS. Si detectas un dato real incrustado en un archivo de la skill, es un error: quítalo.

## Archivos de referencia

- `references/guia-configuracion-chatea.md` — **Mapa de dónde va cada pieza en Chatea PRO** (saludo, multimedia, pregunta, prompt, recordatorios, remarketing, palabras clave). Entrégalo siempre al usuario para que configure sin enredarse.
- `references/plantilla-prompt.md` — Esqueleto completo del prompt de venta, bloque por bloque, con ejemplos. Léelo siempre antes de escribir el prompt.
- `references/sintaxis-del-prompt.md` — **Los 5 comandos que hacen que la IA obedezca**: `#`/`##` jerarquía · `" "` texto literal (el más importante: decide qué dice el bot palabra por palabra y qué parafrasea) · `( )` aclaraciones · `[ ]` variables · IMPORTANTE/NUNCA/SIEMPRE. Léelo cuando haya que ESCRIBIR o CORREGIR un prompt en caliente.
- `references/ficha-producto.md` — **El puente entre el intake y el prompt**: los 7 campos que se llenan ANTES de escribir (beneficio, público, dolor, deseo profundo, diferenciador, justificación de compra y comparación de valor como MÚLTIPLO real), la ficha técnica, las dos listas de claims y las fuentes en orden de riqueza. Llénala primero: sin ella cada build reinventa el diferenciador.
- `references/oferta-irresistible.md` — **La estructura ganadora de 9 elementos** (resultado deseado, producto, mecanismo único, bonos que eliminan obstáculos, prueba/autoridad, garantía, urgencia, escasez, precio anclado contra el valor total), adaptada a COD por WhatsApp y sujeta a las leyes de urgencia y prueba social reales. Trae además el **menú de mecánicas de oferta** con el criterio para elegir cuál usar según dónde vive el valor del producto, y la ley de que de un material ajeno se importa el criterio pero jamás la redacción. Léelo antes de armar el PASO 0.9.
- `references/ejemplo-minimo.md` — **Vara MÍNIMA VIABLE (4.000-6.000)**: el flujo núcleo sin extras, para enseñar la estructura o arrancar cuando el vendedor tiene muy pocos insumos. NO es el objetivo de entrega. Se valida con `validar.sh --minimo`.
- `references/ejemplo-completo.md` — **Ejemplo horneado de punta a punta** (producto resuelto con las 7 piezas + evaluación de calidad). Úsalo como vara de calidad: tu salida real debe igualar ese nivel de detalle.
- `references/estructura-disparo.md` — Plantillas de saludo, multimedia, pregunta de entrada, recordatorios, remarketing y activador.
- `references/checklist-multimedia.md` — Lista de las URLs/imágenes que conviene pedir al usuario y dónde se usan.
- `references/objeciones.md` — **Librería de objeciones** por categoría (precio, confianza, logística, salud/legal, decisión). Elige las que apliquen e insértalas en el bloque OBJECIONES.
- `references/paises.md` — **Packs por país** (los 10 que acepta la plataforma; pack completo para CO/EC/CL/MX/PA/PE/PY/GT — Argentina y Brasil soportados, pack pendiente): nomenclatura de dirección, transportadoras, medios de pago y tono. Usa el del país del negocio.
- `references/cumplimiento.md` — **Guardarraíles legales/plataforma**. Checklist obligatorio antes de entregar.
- `scripts/validar-doctrina.sh` — **Compuerta de la doctrina Golden**: mide un prompt contra los tramos del proceso persuasivo (diagnóstico · persuasión · precio/oferta · objeciones · cierre · captura como críticos; razón de preferencia · prueba · tramo logístico · postventa como esperados) y bloquea los antipatrones (urgencia inventada, testimonio fabricado, claim FDA). **NO evalúa identidad**: marca, tono y país deben variar. Uso: `bash scripts/validar-doctrina.sh --vara <archivo.md>` o sobre un .txt con el prompt.
- `references/medicion.md` — **Cómo saber si el prompt funcionó**: línea base de 7 días, las tasas del embudo y qué tramo del prompt señala cada una, dónde mueren los chats (20 bastan), qué se mide por pieza, y el criterio para decidir si un cambio sirvió sin engañarse. Léelo ANTES de entregar un prompt que reemplaza a otro.
- `references/resultados-ledger.md` — **Registro de resultados** para medir versiones y componer aprendizaje (PASO 4).
- `references/recursos-visuales.md` — **Sistema de imágenes/URLs**: cómo listar las imágenes conversacionales, generarlas (o dar el prompt de imagen), y el manifiesto que se entrega DEBAJO del prompt. En el prompt solo va la URL.
- `references/intake-inteligente.md` — **Intake inteligente (PASO 0)**: el modo conversacional UNA PREGUNTA A LA VEZ (orden, obligatorio vs opcional, relleno inteligente), el gate de anticipado, y cómo tomar el producto por URL (scrape), foto (visión) o investigándolo (competencia/web).
- `references/entrega-pdf.md` — **Entregable PDF (PASO 2.5)**: cómo generar el paquete como PDF con `golden-pdf-check`, con el prompt partido en tarjetas atómicas "Parte N de N" que van seguidas en el mismo campo.
- `references/psicologia-del-chat.md` — **POR QUÉ funciona el embudo** (método de JuanMa Gaviria, *Véndelo todo chateando*): el enemigo es la ATENCIÓN dividida · conecta/conversa/gana · el saludo va al PRODUCTO y nunca es "en qué te puedo ayudar" · **la diferenciación ES la conversación** (sin ella solo queda el precio y gana el más barato) · el ORDEN de los factores altera el resultado · la cadena cómodo→seguro→confianza→paga · el resultado es el proceso, no la frase de cierre. Léelo cuando un prompt no cierre: el arreglo casi nunca está en el mensaje final.
- `references/changelog.md` — **El acta completa de la skill** (63 versiones, v3.0 → hoy): qué cambió, por qué, y el fallo que lo motivó. **No se lee para trabajar** — se consulta cuando quieras saber por qué una regla es como es, o antes de "arreglar" algo que ya se arregló y se revirtió. Vivía dentro de este SKILL.md y costaba 81.697 caracteres en cada activación.
- `references/referencia-externa-embudo-whatsapp-cod.md` — **REFERENCIA OPCIONAL, NO REGLA** (masterclass de terceros sobre embudo COD por WhatsApp). Consúltala solo para contrastar o enriquecer ángulos; JAMÁS sustituye la estructura obligatoria de esta skill ni el método FER. En conflicto, manda la skill.
- `scripts/validar.sh` — **Validador-compuerta**: mide crudos, escapados, emojis y BOM con python y BLOQUEA (exit != 0) si algo excede; modo `--activador` exige 0 emojis. Córrelo antes de entregar, también sobre cada activador.

## Anexo · la description anterior, archivada (no es la sección de fronteras)

⚠️ Esta sección se llamaba también "Fronteras y desambiguacion", igual que la de arriba, y **dos
secciones con el mismo título hacen que la segunda se lea como la vigente**. No lo es: aquí solo
se guarda el texto viejo de la `description` para no perder matices. La sección que manda es
**"Fronteras y desambiguación (esto vive AQUÍ…)"**.

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Crea el paquete completo de venta para un asistente de WhatsApp en Chatea PRO v2 — saludo inicial, plan de multimedia, pregunta de entrada, prompt de venta, recordatorios y remarketing — Y TAMBIÉN MEJORA prompts que el usuario ya tenga (los evalúa /100 y /1000, marca lo crítico y los reconstruye a nivel superior). Úsalo SIEMPRE que el usuario quiera crear, armar, optimizar, auditar o MEJORAR un prompt de ventas para Chatea PRO, un asistente/bot/agente de ventas por WhatsApp, venta contra entrega o pago anticipado, o diga cosas como "hazme el prompt de [producto]", "necesito un agente de ventas para WhatsApp", "arma el asistente de Chatea PRO", "optimiza este prompt de venta", "ya tengo un prompt, mejóralo", "revisa el prompt de mi bot", "este prompt no me vende", "configura la venta conversacional" — o cuando PEGUE un prompt de ventas existente pidiendo opinión o mejora. Aplica a cualquier producto y modelo de pago, en los 10 países que acepta la plataforma (con pack completo para Colombia, Ecuador, Chile, México, Panamá, Perú, Paraguay y Guatemala; Argentina y Brasil soportados, pack pendiente). Si dudas, dispáralo, porque un prompt sin esta estructura convierte menos. NO uses esta skill para la config general/JSON de la tienda (`golden-chatea-pro-config-ventas-wp`), comentarios (`golden-chatea-pro-config-comentarios`), logístico (`golden-chatea-pro-config-logistico`), carritos (`golden-chatea-pro-config-carritos`), pauta (`golden-ads`) ni la página de producto Shopify (`golden-shopify`): esta skill SOLO construye el prompt de venta y sus piezas de disparo.

