---
name: golden-chatea-pro-config-logistico
description: >-
  Golden Group — AUDITA y OPTIMIZA el asistente LOGÍSTICO de Chatea Pro (el PADRE). El espacio
  llega ya instalado y con plantilla de fábrica: primero se audita qué campos siguen siendo de
  fábrica, cuáles tocó el negocio y en qué país opera de verdad; después se optimizan
  (transportadoras de domicilio y de oficina, prohibidas, tiempos por zona) y se arma el prompt
  que valida la dirección antes del envío contra entrega (COD), delegando en su skill HIJA
  golden-chatea-pro-validacion-direcciones. El país no bloquea: sin pack se optimiza igual,
  investigando lo que falte. Úsala SIEMPRE que quiera montar, auditar u optimizar el asistente
  logístico o de direcciones de Chatea Pro, "configurar logística de chatea pro", "revisa cómo
  quedó mi logístico", "el bot que revisa direcciones antes de despachar", "el bot valida mal
  las direcciones", "configura las transportadoras del bot", "el asistente que evita
  devoluciones". No configura VENTAS ni CARRITOS: usa golden-chatea-pro-config-ventas-wp o
  -config-carritos.
---

**Fábrica:** chat «✅ SKILL golden-chatea-pro-config-logistico»
# Golden · Chatea Pro — Asistente Logístico (padre)

## 📋 Requisitos: qué necesita del usuario antes de arrancar

- **Token API del espacio de Chatea Pro** · BLOQUEANTE. Se crea en el panel del espacio (*Settings → API Keys*, según el propio código) y va **atado al Bot**; si no, la API responde 404 "Flow not found". Se guarda en `<carpeta del cliente>/.secrets/<espacio>.token`. Cupo: 1.000 llamadas por hora (no está medido si es por token o por espacio; se mira con `golden-chatea-cupo`).
- **País del espacio** · BLOQUEANTE y SE PREGUNTA SIEMPRE: la plantilla nace colombiana sin importar el país. Sin pack del país se optimiza igual, investigando lo que falte.
- **Lo que se pregunta** (transportadoras de domicilio y prohibidas, identidad: tienda, WhatsApp y web) · DEGRADABLES: un campo sin dato se declara pendiente.
- **Monto del anticipo** · DEGRADABLE: si no lo da, se propone el flete completo. **Datos de pago con titular**, si hay anticipado · BLOQUEANTES para ese campo: se preguntan; nunca se inventan.
- **Validaciones de la orden** · no se preguntan: se relevan del espacio y **se respetan las que puso el cliente**.
- **La hija `golden-chatea-pro-validacion-direcciones`** y acceso a internet para el PASO 1-bis · DEGRADABLE: sin ella se entrega con el pendiente declarado.

**Si falta algo BLOQUEANTE: no se hace lo que depende de él** (si es de toda la skill, se PARA antes de tocar nada) y se pide con nombre propio: qué es, dónde se saca y dónde se pone. **Si falta algo DEGRADABLE: se pide y se sigue**, dejando declarado como pendiente en todo lo que depende de él. Nunca se presenta como completo.

<!-- skill v1.15 — 2026-09-28 — sello unificado. Recoge: el bloque de Requisitos del CdM (27-sep, ley de FER del 02-sep), la sección LA PARTE DINÁMICA (v1.13) y la fila P59 del CdM (v1.14: exclusiones silenciosas nombradas en los dos scripts, 429 y 401 explicados). 🔴 El número 1.12 quedó usado DOS veces —la fábrica el 22-sep y el CdM el 27-sep— y por eso el cuerpo decía 1.12 mientras el changelog iba por 1.14: se sella por encima de ambas y se numera una sola vez. Historial: references/changelog.md. -->
<!-- skill v1.11 — 2026-09-18 — fábrica en su chat (optimización de Golden): cuatro campos JSON, tiempos y recordatorios estándar de FER, intake del anticipo, escritor por API con autoprueba 7/7, regla del techo y del pago anticipado. Historial completo: references/changelog.md (2 actas, mudadas el 2026-09-05; el cuerpo se paga en cada activación, el acta no). Auditoría golden-skill-auditor 2026-09-20: agregada esta línea de versión bajo el H1, que faltaba (inventario.sh la marcaba ausente); sin otros hallazgos con evidencia. Cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO. -->

## QUÉ ES CONFIGURAR ESTE ASISTENTE, en palabras de FER (2026-09-08)

> *"La skill que configura los asistentes lo único que hace es entrar a esos JSON y llenarlos.
> No hay que hacer nada más. Esa es la única configuración que se hace. Pero llenarlos
> analizando lo que esa tienda maneja en determinado nicho. No tienen que quedar igualitos
> todos: si es Colombia se supone que queda muy parecido, pero no necesariamente idéntico,
> porque una tienda de un nicho específico puede que su identidad cambie y varíe."*

**Cuatro campos JSON, y ya.** La configuración del asistente logístico vive en
`[Logistico] Configuracion General`, `[Logistico] Confirmaciones`, `[Logistico] Seguimiento`
(ganchos de venta, tiempos, pedidos en oficina) y `[Logistico] Novedad` (tiempos y días de
ofrecimiento). El panel es la vista; esos campos son el dato. *(Hasta el 18-sep esta skill decía
"dos campos": en Golden se optimizaron tres y los ganchos de Seguimiento tenían los peores
defectos.)* 🔴 **Y LO QUE NO ES CONFIGURACIÓN NO SE AUDITA COMO SI LO FUERA (FER, 2026-09-22).** El panel
del logístico tiene 4 pestañas y 18 secciones: **lo que no se puede señalar ahí, el dueño no lo
puede cambiar, y "igual a fábrica" ahí NO es un defecto.** Quedan fuera: `[Logistico] Plantillas
de mensaje` (las plantillas vivas se eligen en Confirmaciones, Seguimiento y Novedad),
`[Novedades] Mensajes por tipo de novedad` (en novedad el bot **solo envía plantillas
aprobadas**), `[Logístico] Versión de bot`, `[Logistica] Token de integración` (credencial) y los
dos interruptores de plataforma. Origen: esta fábrica reportó como "sin adaptar" los 11 mensajes
por tipo de novedad, y FER lo paró en seco — ni aparecen en el panel ni se pueden editar. La
lista vive en `scripts/auditar_espacio.py` (`NO_ES_CONFIGURACION`) y el auditor los aparta antes
de contar defectos. **Antes de señalar un campo, se comprueba que el dueño pueda tocarlo.**

**La lógica interna del asistente no se toca** — viene con Chatea y no es nuestra.

**Y el encargo real no es rellenar: es DECIDIR con criterio de ese negocio.** Rellenar los cuatro
campos con el mismo texto para todos es exactamente lo que hace la plantilla de fábrica, y por
eso hay una skill y no una plantilla. Dos tiendas colombianas bien configuradas **se parecen y
no son idénticas**; dos idénticas byte a byte delatan un clon sin adaptar. Lo que cambia por
negocio: la identidad y el tono, la garantía y sus plazos, los tiempos de entrega por zona, el
umbral de flete en su moneda, la jerga del nicho y los ganchos de venta. Lo que no cambia: la
estructura de llaves del JSON.

**El mapa completo del panel —las 4 pestañas, sus 18 secciones, campo por campo y con sus topes
medidos— vive en `golden-chatea-auditoria/assets/campos-de-configuracion.json`, bajo
`asistentes.logistico`.** Ahí está el denominador: qué existe, qué es configuración y qué no.
Se lee antes de tocar; no se reconstruye de memoria ni se deduce del panel de otro cliente.

**Lo que la auditoría comprueba después** no es el parecido con una plantilla, sino tres cosas:
que los campos estén **completos**, que tengan **coherencia entre sí** (los tiempos de entrega
que promete el mensaje de agradecimiento contra los de la sección Tiempos de envío; el saludo
del asesor contra la existencia real de un asesor humano), y que estén **optimizados para ese
país y ese nicho** (la ley que se cita en la garantía, la moneda del flete, la nomenclatura de
direcciones, las categorías de zona de la transportadora local).

## LA PARTE DINÁMICA: lo único que cambia de un espacio a otro (FER, 2026-09-22)

🔴 **La doctrina ya está cerrada y no se renegocia en cada cliente.** De un espacio al siguiente
solo cambian los datos de abajo. Si una corrida quiere cambiar algo que NO está en esta lista,
eso no es adaptar: es reabrir la skill, y va al Centro de Mando.

**LO QUE CAMBIA (se releva por espacio):**
1. **País.** Es parámetro, no puerta. De él salen la jerga, la nomenclatura de direcciones, la ley
   que cita la garantía, la moneda del flete y si existe recogida en oficina.
2. **Identidad:** nombre de la empresa, enlace y ubicación. Los claims (años en el mercado,
   número de clientes) son del dueño: si no los da, no se inventan ni se heredan.
3. **Nombre del asesor humano** del saludo. Uno por espacio, y nunca el de otra cuenta.
4. **Números de contacto:** el WhatsApp que aparece en la garantía y el de notificaciones.
5. **Transportadoras:** las de domicilio, las que hacen recogida en oficina y las prohibidas.
6. **Validaciones de la orden:** porcentaje mínimo de entregas, mínimo de órdenes y flete máximo,
   en la moneda de ese país.
7. **Anticipo:** monto, medios y datos de pago con titular, y si se descuenta del total. Los datos
   de pago se buscan primero en la configuración viva de ventas y carritos de ESE espacio.
8. **Garantía:** plazos y la ley que se cita, según el país.
9. **Origen de datos** (Shopify o Dropi) y **modelo de IA** que ofrezca el panel.
10. **Plantillas de Meta:** las aprobadas en el WABA de ese espacio. **Nunca se copian** de otro.

**LO QUE NO CAMBIA (doctrina de la casa, igual en todos los países):**
· Tiempos de entrega 2-3 / 3-4 / 5-7 días hábiles y "de 1 a 2 días en ciudades principales y 2 a 3
  días en ciudades no principales"; recordatorios de confirmación a 1 y 2 horas.
· El tono, las restricciones y el "nunca vuelvas a pedir un dato que el cliente ya dio".
· Emojis: la IA no los genera; los llevan los mensajes fijos y los ganchos.
· Sin signos de apertura de interrogación ni de admiración.
· La estructura de los cuatro ganchos y su formato (frase entre asteriscos, un emoji al final,
  transportadora real en el de oficina).
· El contrato de salida del prompt de dirección, de una sola línea. El vocabulario del país lo
  pone la skill hija, no esta.
· El pago anticipado se plantea como COBRO, nunca como beneficio opcional.
· Que la regla y el ejemplo digan lo mismo.

## Lo que NO está verificado en esta skill (al 2026-09-08)

Vive **dentro de la skill** a propósito: una reserva escrita en el informe de un chat es un
recuerdo, se va con el chat y quien active la skill mañana no la lee.

**Cada reserva nombra
QUIÉN la cierra.** Una que no puede nombrar a su cerrador o ya está cerrada y sobra, o nadie la
ha pensado — y así la sección no se puede vaciar en silencio.

**CERRADA 2026-09-18: el tope de `Restricciones` es 2.000.** Captura del panel de Golden: 1.990/2.000.
**Sin medir todavía: el prompt de persuasión del Pago Anticipado** (`estrategia_persuasion`). · **La cierra:** mirar su
contador en el panel al pegarlo. No se le asume 2.000 por parecerse a sus vecinos.

**Los topes que sí están medidos caducan solos.** · **La cierra:** nadie de forma permanente —
es vigilancia. El contador del panel manda sobre esta lista, siempre. Se leyeron el 08-sep del contador que pinta
Chatea. La plataforma se actualiza sin avisar: en agosto se midió contra su código que "el
logístico no tiene tope" y en septiembre era falso, con un campo a diez caracteres de cortarse.
Las cifras de aquí son la última medida, no una garantía.

**El mapa del panel sale de un vídeo, no de la API.** · **La cierra:** un segundo vídeo o unas
capturas de esas cuatro secciones. El ESQUEMA de llaves ya no lo necesita. Cuatro secciones no se llegaron a ver
—Reinstalación de mensajes, Tiempos de envío de Seguimiento, Pago Anticipado y el pie de
Ubicaciones—. El ESQUEMA de llaves sí es de la API y está completo
(`golden-chatea-auditoria/assets/esquema-configuracion.json`); lo que falta es la
correspondencia pantalla ↔ llave, que es para el humano que configura.

**Nada de esto se ha corrido contra un espacio de cliente desde los cambios del 08-sep.** ·
**La cierra:** la primera configuración real que FER autorice, con su cupo reservado. La
autoprueba valida el detector, no valida ningún espacio.

## LEY: NUNCA HEREDAR DATOS ENTRE ESPACIOS (FER 2026-08-08)

Al basarse en una cuenta guía se hereda **estructura, prompts y configuración** — JAMÁS datos:
llaves y tokens, plantillas de WhatsApp (van atadas al WABA de cada espacio), teléfonos, correos,
dominios, nombre de la marca, productos y **claims de negocio** (años en el mercado, clientes
atendidos: no rompen nada técnico y ponen al bot a mentir con datos de otra empresa).

**Método obligatorio al escribir en un espacio ajeno:** barrer ANTES lo que se va a escribir
buscando `sk_`, `shpat_`, `eyJ`, teléfonos, correos, dominios y nombres de plantilla, más un
`grep -i` por el NOMBRE de la marca de origen, porque **la marca viaja escondida en prosa libre**
(así se cazaron 10 menciones en 3 campos que el mapeo de llaves no vio). Herramienta:
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (sale con código 3 si encuentra algo CRÍTICO).
DESPUÉS de escribir: releer del servidor y barrer otra vez.

**El detalle completo —las cinco categorías vetadas, el caso real del 2026-08-08 y la regla de los
campos `[Meta]` como valores calientes— vive en `references/ley-datos-entre-espacios.md`.**

## Los dos techos (antes de escribir cualquier campo)

- **Techo A — el bot field: 20.000 ESCAPADOS, no crudos.** Al ejecutarse, el flujo copia la configuración escapada: cada tilde ocupa 6 caracteres y cada emoji 12. El techo práctico en crudos queda en ~17.000. Pasarse NO da error: la API responde `200 ok`, guarda el JSON cortado y el asistente muere en silencio (el error solo aparece en Panel → Registros de errores). Medir siempre: `escapado = len(json.dumps(valor)[1:-1])` y que quede bajo 19.000. **Nivel B — LONG JSON:** el tope de 20.000 es del campo tipo JSON legacy; si el bot field se crea o convierte a **LONG JSON**, el techo sube a 500.000 escapados (ley de dos niveles medida en las hermanas config-comentarios y config-ventas-wp). Con configuraciones grandes, convertir el campo a LONG JSON antes de escribir.
- 🔴 **Techo B — el campo nativo SÍ tiene tope, y son 2.000.** Medido el 2026-09-08 en el panel vivo: `Adaptación del lenguaje` marcaba **1.786/2.000**, `Método para evitar la cancelación` **1.990/2.000 pintado en NARANJA**, `Políticas de garantía` **1.219/2.000**. El contador lo pinta la propia plataforma encima del campo: es la fuente autoritativa y se lee antes de escribir. **Hasta hoy esta skill decía justo lo contrario** —"el logístico NO tiene tope en sus campos de texto"— citando `TOPES-NATIVOS-POR-CAMPO.md`, extraído del código de la app el **2026-08-07**. Un mes después es falso: o Chatea añadió el límite, o la extracción no encontró el chunk. **La clase, que importa más que el caso: una medida contra el código de una app que se actualiza sola CADUCA EN SILENCIO** — nadie avisa, y el dato viejo se sigue leyendo como hecho. Con la regla vieja, esta skill escribía 5.000 caracteres de personalidad convencida de que cabían, y el panel los cortaba sin decir nada.

  **Los topes nativos medidos, por campo** (todos del contador del panel, 2026-09-08):

  | Tope | Campos |
  |---|---|
  | **250** | Nombre de la tienda · Enlace de la tienda · ID de voz · API Key de ElevenLabs · cada recordatorio personalizado de oficina |
  | **2.000** | Ubicación de la tienda · Políticas de garantía · Adaptación del lenguaje · Mensaje de saludo del asesor · Método para evitar la cancelación · Tiempos de entrega · Mensaje de agradecimiento |
  | **3.000** | Los tres ganchos de venta (Guía Generada · Reparto · Pedido en Oficina) |
  | **8.000** | Prompt de análisis de dirección |
  | **15** | ID de producto de Dropi, en los dos bloques de Mensajes Personalizados |

  `Restricciones` (Limitaciones generales) **no se midió**: la sección se ve en el vídeo y su contador no llegó a verse. No se le asume 2.000 por parecerse a sus vecinos — se mira el contador antes de escribir.

  **Y los dos techos no se sustituyen, se suman:** el nativo corta ese campo, el del bot field (Techo A) corta la configuración entera. Hay que pasar los dos.

  🔴 **Estar cerca del techo NO es un defecto (FER, 2026-09-18).** El tope es una compuerta binaria: pasarse bloquea, 1.999/2.000 pasa sin comentario. Nunca se reporta "naranja" o "poco margen" como hallazgo, y nunca se recorta contenido útil para ganar espacio: se recorta solo lo que sobra por contenido (repetición, contradicción, dato falso). Si un caso real necesita más texto, se añade aunque llene el campo. Origen: el 08-sep esta fábrica recortó tres campos de Golden "por margen" y tuvo que devolver argumentos de venta.

## Gotchas de API (si la config se escribe por API)

- `PUT /flow/set-bot-fields-by-name` usa la llave **`data`**: `{"data":[{"name","value"}]}`. Con `bot_fields` responde 400.
- `POST /flow/create-bot-field` usa **`var_type`** (no `type`) y **exige `value`**. Con otra llave, 422.
- `GET /flow/bot-fields` **PAGINA** y `per_page` se ignora: recorrer todas las páginas antes de concluir que un campo no existe.
- El valor se guarda como string con `ensure_ascii=False, separators=(',',':')`; otro formato infla el conteo contra el techo sin cambiar el contenido.
- **El trigger no admite caracteres de 4 bytes:** un emoji lo corrompe y el bot no arranca nunca. Validar: `[c for c in texto if ord(c) >= 0x10000] == []`.
- **Cada llave conserva su tipo:** un array escrito como cadena se ve vacío y el panel lo deja en `[]` al guardar, sin error.
- **Escribir y RELEER siempre:** comparar el valor guardado contra el enviado es la única prueba real.

## Flujo: primero AUDITAR, luego OPTIMIZAR

### PASO 0 — AUDITAR el espacio (NUNCA se empieza en blanco)

🔴 **Aquí no se configura nada: se optimiza lo que ya existe.** El espacio siempre llega con
los cuatro asistentes instalados por su dueño, y la plataforma los instala **con una plantilla
de fábrica ya escrita**. Empezar preguntando es empezar mal: primero se mira qué hay.

```bash
python3 ~/.claude/skills/golden-chatea-pro-config-logistico/scripts/auditar_espacio.py \
  --token-file <ruta> --pais-declarado <PAIS>
```
**Desde el 2026-09-22 el PASO 0 no es ciego:** además de clasificar fábrica/tocado/vacío, revisa
a fondo **los 4 campos de configuración** y cruza siete cosas — topes del panel en UTF-16, llaves
vacías, tiempos de entrega iguales en los tres sitios donde se prometen, que el gancho de oficina
no nombre transportadoras que no hacen recogida, la contradicción de emojis, el pago anticipado
encendido con el prompt de fábrica, y la regla que pide asteriscos con ejemplos que no los traen.
Autoprueba: 27 casos en los dos sentidos (tres sabotajes la bajan a 25 y 26).

🔴 **Ruta ABSOLUTA, igual que el validador de abajo.** Con `scripts/…` solo corre si por
casualidad estás dentro de la carpeta de la skill, y fuera de ella falla con un "no such file"
que parece un problema del entorno y es un problema de la instrucción.

Clasifica los 61 campos en **FÁBRICA** (idéntico a lo que escribe la plataforma → se
reemplaza) · **TOCADO** (lo cambió el negocio → es suyo, se respeta) · **VACÍO** (se llena).

🔴 **CUPO DE LA API: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.**
Medido contra la API viva el 2026-09-07: cada respuesta trae `x-ratelimit-remaining` (en inglés
**X-RateLimit-Remaining**) y `x-ratelimit-limit`. El script lo lee y lo dice al final. Este PASO 0
lo corren las cuatro skills de config y el orquestador, así que es el camino más transitado: si
aquí se agota el cupo, se cae la instalación entera antes de empezar. **Si el cupo se agota a
mitad de la lectura, el script NO devuelve un inventario parcial: sale en rojo** — informar 20 de
61 campos como si fueran todos da un informe falso. Para saber cuánto queda antes de empezar:
`golden-chatea-cupo`. **Se repone cada hora** (dato del desarrollador), pero el servidor **no dice a qué minuto empezó la ventana**: si te bloqueas, espera una hora completa desde ese momento y comprueba mirando el contador, no calculando.

**Se mide por el VALOR, contra `assets/plantilla-fabrica.json`.** La bandera
`is_template_field` de la propia plataforma **no sirve**: viene en falso en 9 de cada 10
campos. Y un campo de fábrica **no se ve vacío, se ve configurado** — de ahí el peligro: si se
toma por dato real, el bot le entrega a un cliente de verdad un teléfono que no es de nadie.

#### 🔴 El cruce de país: siempre se pregunta en qué país OPERA
**La plantilla nace colombiana elijas el país que elijas** (medido el 06-sep en dos espacios
nuevos: 61 de 61 campos idénticos byte a byte entre uno de Colombia y uno creado eligiendo
México). Por eso el país del negocio **se pregunta siempre** —es de lo que solo sabe el
dueño— y se **cruza contra lo que está escrito en los campos**.

Cuando no coinciden se dice, y se dice claro: *"me dices que operas en México, pero tienes los
cuatro asistentes montados para Colombia"*.

**Cómo cruza, y qué NO alcanza a ver** (medido el 06-sep con cuatro sabotajes):
· Cruza por la llave `"pais"` de los JSON **y** por las señales del texto —quién regula
  (Estatuto del Consumidor, Profeco, Indecopi, Sernac), qué transportadora se nombra, el
  prefijo telefónico y el código de moneda— de **6 países**: Colombia, México, Perú, Chile,
  Argentina y Ecuador.
· 🔴 **Una señal solo cuenta si nombra una institución, una marca o un país. Nunca una cosa.**
  El primer intento incluyó "código postal", "departamento", "colonia" y "paquetería", y
  marcó México en una plantilla colombiana: **un detector de patrones acusa al idioma.** El
  vocabulario es JERGA —dice cómo escribir, no en qué país se está—; la identidad es quién
  regula, quién transporta, qué prefijo y qué moneda.
· **Fuera de esas 6 familias el texto no delata al país**, y el cruce depende de la llave. El
  informe lo dice en su línea de COBERTURA: no se calla el límite.
· **Si no hay ni llave ni señal, el informe NO dice "OK": dice que el cruce no se pudo hacer**
  y sale en rojo. Un OK que no comparó nada cierra la puerta a que alguien mire. No es un detalle de forma: de ese campo salen la
jerga, los tiempos por zona, el prefijo del teléfono y **la ley que cita la garantía** — la
plantilla cita el Estatuto del Consumidor colombiano, que a un negocio de Perú o Argentina no
le aplica. Se corrige **antes** de optimizar nada.

#### Lo que la plantilla trae y hay que limpiar SIEMPRE, también en Colombia
· **Dos biografías falsas y contradictorias**: el logístico dice *"5 años de experiencia"* y el
  de comentarios *"7 años y más de 3.000 clientes satisfechos"*, en el mismo espacio.
· **El asesor ya se llama Santiago**, de fábrica, en el saludo.
· Teléfono `+57 300 123 4567`, tienda `.co` y tiempos con jerga colombiana.
· Restos de edición pegados al texto (comillas de cierre huérfanas) que viajan al prompt.

#### Con qué se optimiza
**Con lo que la casa ya sabe, no con lo que se le ocurra a la corrida.** El patrón es el
espacio de Golden Group, ya afinado. Y el grado de personalización lo marca lo que la auditoría
encontró, no el gusto:
· **Sin identidad ni productos** (todo de fábrica) → se deja **óptimo para cualquier nicho**:
  neutro, sin inventarle rubro, sin biografía, sin cifras.
· **Con productos o nicho identificables** → se enfoca a esa familia y a esa identidad.
· **Siempre** → al país real del negocio.
**Nada se llena por llenarlo, y nada se inventa.** Un campo sin dato se declara pendiente; es
preferible un hueco declarado a una cifra bonita que el negocio no puede sostener.

### PASO 1 — Intake: SOLO el hueco que dejó la auditoría (UNA PREGUNTA A LA VEZ — decisión de FER 2026-08-26 — y no inventes nada)
Con la auditoría en la mano, releva **solo lo que quedó en hueco**, conversacionalmente, **una pregunta a la vez** ("en bloque se
abruma la gente" — FER). El bloque completo de una sola vez es la EXCEPCIÓN: solo cuando el
interlocutor ya pegó varios datos juntos (reconócelos todos y pregunta solo lo que falte) o
pida expresamente que se le mande todo de una. Lo que NO cambia: el conjunto se releva al
inicio y un dato ya dado JAMÁS se re-pregunta después.
🔴 **LEY DE FER (2026-09-06): no se pregunta lo que ya sabemos NI lo que podemos averiguar.**
*"Qué tal que el cliente se equivoque... eso no puede ir como regla."* · *"Tenemos que preguntar
lo menos posible de lo que nosotros ya sabemos configurar. La menor fricción es lo ideal."*
**Preguntar algo es entregarle a otro la autoridad de decidirlo**, y preguntar lo averiguable es
además cobrarle nuestro trabajo.

**La frontera de lo que sí se pregunta:** solo lo que **no existe en ninguna fuente** porque
vive en la cabeza del dueño — el nombre de su tienda, su país, su WhatsApp, su web, con qué
transportadoras trabaja. *"No puedo saber cómo se llama alguien si no le pregunto el nombre"*
(FER). Todo lo demás —jerga, forma de las direcciones, qué transportadoras existen, tiempos
típicos, moneda— **se averigua y se configura**; ver PASO 1-bis. Y hay un tercer caso: lo que
**se SUGIERE** —el nombre del bot, el tono— donde se proponen opciones y el dueño escoge:
*"podemos sugerir, mas no adivinar"*.

**SE PREGUNTA (3) — nadie más que el negocio lo sabe:**
1. **Transportadoras habilitadas para DOMICILIO** (las que tiene contratadas de verdad).
2. **Transportadoras PROHIBIDAS** (ej. en Colombia muchos negocios no usan una en concreto).
3. **Anticipo para clientes que no pasan las validaciones:** cuánto se cobra ("si el cliente
   tiene malas métricas, cuánto es el anticipo"). Si no lo da, se propone el flete completo.
4. **Medios y datos de pago del anticipo, con titular.** Antes de preguntar se buscan en su
   configuración viva de ventas y carritos (`datos_pago_anticipado`, prompts de producto): solo
   se pregunta lo que falte. Y si el anticipo se descuenta del total (estándar de la casa: sí).

**NO se pregunta — estándar de FER, igual en todos los países (2026-09-16):** tiempos de entrega
Ciudad Principal 2-3 · Ciudad Intermedia 3-4 · Zonas Rurales 5-7 días hábiles; desde reparto
"de 1 a 2 días en ciudades principales y 2 a 3 días en ciudades no principales"; recordatorios
de confirmación a 1 y 2 horas. Se traduce solo el término si el país usa otro para "zona rural".

**NO SE PREGUNTA — se trae, se deriva o se aplica:**
· **País** → **SÍ se pregunta** (es de lo que solo sabe el dueño) y se CRUZA contra lo escrito
  en los campos, PASO 0. Si el encuadre ya lo trajo, no se repregunta: se cruza igual.
· **Recogida en oficina** → **se DERIVA del pack de país**, no se pregunta a ciegas. En México
  no existe: todo va a domicilio. Preguntárselo a un negocio mexicano es ofrecerle algo que la
  operación de su país no tiene, y aceptar un "sí" ahí rompe la config.
  Donde el país SÍ la contempla, se pregunta con qué transportadoras — eso ya es identidad.
  *(Sin pack, si existe o no en ese país se AVERIGUA en el PASO 1-bis, no se pregunta.)*
· **Emojis** → estándar de Golden: la IA **no los genera** en lo que redacta; solo los mensajes
  fijos configurados y los ganchos de seguimiento (un emoji final, por diseño) los llevan. El
  prompt de dirección nunca los usa. **Es DOCTRINA de la casa, no una preferencia
  del cliente.** Se aplica el estándar y se INFORMA. Preguntarlo abre la puerta a que cada
  espacio hable distinto sin razón.

**Cómo se pregunta lo que sí toca:** una pregunta a la vez, conversacional — *"en bloque se
abruma la gente"* (FER, 26-ago). La excepción es cuando el interlocutor ya pegó varios datos
juntos: se reconocen todos y se pide solo lo que falte. **Un dato ya dado JAMÁS se re-pregunta.**

### PASO 1-bis — PAÍS SIN PACK: se INVESTIGA, no se pregunta

**Cuándo entra.** El país del workspace no está en `paises_validos`, o está pero la hija no
tiene pack. Ejemplos que ya se ven venir: El Salvador, o un país que la plataforma habilite el
mes que viene.

🔴 **LEY DE FER (2026-09-06): lo que se puede averiguar NO se pregunta.** *"La jerga y la
configuración de las direcciones no se le pregunta a la gente, porque precisamente para eso es
la skill. Eso ya lo tenemos, eso ya lo hacemos nosotros. Tú tienes que ir a Internet, revisar,
estudiar, analizar, extraer esa información y configurarla."*
**Preguntar lo averiguable es cobrarle al cliente nuestro trabajo** — y encima con el riesgo de
que conteste mal y esa respuesta mala quede escrita como regla. **La menor fricción posible.**

**La frontera, exacta.** No se pregunta lo que existe en alguna fuente; se pregunta lo que solo
vive en la cabeza del dueño:
· **Se PREGUNTA** (nadie más lo sabe): nombre de la tienda · país de operación · WhatsApp de
  servicio al cliente · página web · **las transportadoras que él tiene contratadas** y las que
  no quiere usar. El **nombre del bot se SUGIERE** — *"podemos sugerir, mas no adivinar"*—:
  se proponen opciones y él escoge, nunca se deja en blanco ni se inventa por él.
· **Se INVESTIGA** todo lo que es del país, porque el país no es un secreto de nadie.

**Qué se investiga antes de escribir una sola línea de config:**
1. **Cómo se ESCRIBE una dirección ahí**: qué campos la componen (estado / provincia /
   departamento / municipio, colonia o barrio, si hay código postal y si es obligatorio), en
   qué orden se escriben y cómo se abrevian.
2. **Cómo la gente EXPLICA cómo llegar** — esto es lo que decide si una dirección es
   entregable y es el corazón del pack: las referencias visuales y de trayecto (*"la casa
   roja"*, *"el balcón amarillo"*, *"frente a la iglesia"*, *"donde estaba la farmacia"*),
   cuándo esas referencias bastan y cuándo el mensajero va a tener que llamar.
3. **Jerga y modismos**: cómo le dicen a la transportadora, al pedido, al dinero y al
   repartidor. Es lo que evita el enredo de *"domicilio"* —en Colombia el pedido, en México la
   casa— multiplicado por cada país nuevo.
4. **Transportadoras que operan** en el país y **cuáles hacen contra entrega** (no todas).
5. **Tiempos de entrega típicos por zona** → se vuelven el default que se OFRECE al negocio
   para confirmar, igual que en los países que ya tienen pack. Nunca se le pide un número en
   blanco a alguien que no tiene por qué saberlo.
6. **Si existe la recogida en oficina o sucursal** en ese país.
7. **Moneda** y cómo se escribe un precio ahí.

**El listón de la investigación** (protocolo Golden, fase 3): **tres fuentes independientes**,
y no vale que las tres sean el mismo tipo de fuente. Sirven: los sitios de las transportadoras
del país, lugares donde gente real ESCRIBE direcciones de verdad (reseñas, foros, marketplaces
locales) y la documentación postal o de correos. **Lo que no se logre confirmar se marca como
NO VERIFICADO y solo entonces se le confirma al negocio**, diciéndole por qué se le pregunta.
Nada se inventa: una jerga inventada suena falsa en el primer mensaje y la gente lo nota.

**Al cerrar, el hueco se cierra para todos.** Lo investigado se entrega como **pack propuesto**
para `golden-chatea-pro-validacion-direcciones`, **con sus fuentes** y con lo no verificado
marcado. Se propone, no se escribe solo: quien adopta un pack es la skill dueña. Sin esto, el
siguiente negocio del mismo país obliga a repetir la investigación entera, y **el hueco deja de
ser un hueco para volverse una costumbre**.

### PASO 2 — Generar el prompt de validación (delega en la hija)
Con los datos del intake, **invoca `golden-chatea-pro-validacion-direcciones`** pasándole el país y las transportadoras confirmadas. La hija carga el pack del país (Colombia = patrón oro) y devuelve el prompt de validación con:
- Contrato de salida en **una sola línea** (`dirección correcta` / `Para completar su envío, nos regala [dato]?`).
- Interpretación de nomenclatura local, vivienda colectiva, rural y GPS.
- Principio rector: si un mensajero puede llegar sin llamar → válida; si hay riesgo de devolución → falta info.

**Si la hija no está instalada o no devuelve el pack del país pedido:** no inventes el prompt de validación a mano — es exactamente el trabajo que existe para no reinventarse en prosa cada vez. Informa al usuario que falta `golden-chatea-pro-validacion-direcciones`, entrega igual el resumen operativo del PASO 2 (transportadoras/tiempos, que sí es de esta skill) y deja pendiente explícito el prompt de validación con el motivo exacto (skill hija ausente / país sin pack todavía).

### PASO 3 — Entregar
Entrega al usuario: (a) el resumen de la config operativa (transportadoras/tiempos), y (b) el prompt de validación listo para pegar en el campo del asistente logístico de Chatea Pro.

**Definición de terminado (checklist):**
- [ ] **PASO 0 CORRIDO**, no leído: `auditar_espacio.py` ejecutado contra el espacio real, con
      `--pais-declarado`. El informe trae su línea de COBERTURA (N de 61) y **no dice LECTURA
      INCOMPLETA**. Si el cruce de país salió "NO SE PUDO HACER", se verificó a mano antes de
      seguir. 🔴 Este punto va primero porque es el que la versión anterior no tenía: sin él,
      el resto del checklist se ejecuta sobre un espacio que nadie miró.
- [ ] Los campos marcados **FÁBRICA** quedaron reemplazados y los **TOCADO** quedaron intactos.
- [ ] País del workspace confirmado — **para jerga y pack de direcciones, NO como filtro**.
      🔴 **Este punto no rechaza a nadie**, y por eso no lleva ninguna cifra: la llevó, era
      falsa, y el checklist es lo que se ejecuta al cerrar. Acta en `references/changelog.md`.
- [ ] Si el país no tiene pack, **se corrió el PASO 1-bis**: los 7 puntos del país se
      **INVESTIGARON** con tres fuentes independientes, no se preguntaron. Lo no confirmado
      está marcado como NO VERIFICADO. Falta de pack ≠ negativa, y tampoco ≠ interrogatorio.
- [ ] El **pack propuesto** para ese país quedó entregado a
      `golden-chatea-pro-validacion-direcciones` **con sus fuentes**, para que el siguiente
      negocio del mismo país no obligue a repetir la investigación.
- [ ] Transportadoras de domicilio, recogida en oficina y prohibidas confirmadas con el negocio (ninguna inventada).
- [ ] Tiempos de entrega por zona confirmados y coherentes con Ventas y Carritos.
- [ ] Prompt de validación recibido de la hija (o, si no, el pendiente queda declarado con motivo — ver PASO 1).
- [ ] Si la config se escribe por API: valor escrito releído del servidor y comparado contra el enviado (ver "Escribir y RELEER siempre").
- [ ] Barrido de datos ajenos corrido si el origen fue una cuenta guía o un espacio distinto al del cliente final.

## Lo aprendido optimizando Golden (2026-09-18) — se aplica en todo espacio

- **La regla y el ejemplo dicen lo mismo, o gana el ejemplo.** El bot imita los ejemplos. En
  Golden los ganchos pedían asteriscos y ningún ejemplo los tenía, prohibían comillas y los
  ejemplos iban entre comillas, pedían 15 palabras con ejemplos de 30, y el prompt de dirección
  ponía como *válido* un conjunto sin torre que su propia regla declaraba incompleto. Al terminar
  se lee cada campo completo a mano: un `grep` de la palabra clave no ve el ejemplo roto.
- **Ganchos de venta:** frase entre asteriscos con un emoji final fuera de ellos; el gancho de
  oficina nombra la transportadora REAL que llega en `{transportadora}` (el paquete puede estar
  retenido en una que no hace recogida); emojis y beneficios según la categoría real del producto,
  nunca solo de belleza en una empresa de catálogo.
- **Toda corrección se prueba contra el caso contrario.** Una regla "solo oficinas de las dos
  transportadoras de recogida" habría mandado a la oficina equivocada al cliente cuyo paquete
  quedó en otra. Corregir es mover un criterio: se revisa el lado que se abrió.
- **Se mide en UTF-16** (como el contador del panel): reprodujo 12 de 12 contadores; contar
  caracteres crudos casó 2 de 12. **Y se entrega en el formato de la vía:** texto plano campo por
  campo si el dueño pega en el panel; JSON solo si se escribe por API.
- **Casos duros antes de dar un campo por bueno:** cliente molesto, dato ya dado, cancelación,
  objeción de precio, dirección ambigua (conjunto sin apartamento, manzana y casa, kilómetro de
  vía, vereda con referencia). Se dice si fue simulación por lectura o corrida real.
- **El panel reescribe al guardar:** convierte comillas rectas en tipográficas (no es un cambio
  de contenido) y un campo numérico puede cambiar con la rueda del mouse (en un espacio real se
  guardó un valor distinto del escrito). Después de que el dueño guarda, se releen los números del servidor.
- **Escribir por API con `scripts/escribir_espacio.py`**, nunca subiendo un archivo entero: lee lo
  vivo, verifica que el token es del espacio esperado, respalda, escribe solo las llaves que
  difieren, relee y compara. Antes, `diff` para ver qué va a cambiar. Después, el dueño **recarga
  la pestaña del panel**: guardar con la vista vieja sobrescribe lo escrito.
- **Lo que es del prompt de dirección** (nomenclatura, casos de manzana, kilómetro, abreviaturas
  por país) es de la skill hija: se corrige en el espacio y se manda fila a su fábrica por el
  Centro de Mando, no se reescribe su pack desde aquí.

## Reglas de oro
- **Pago anticipado = SIEMPRE cobrar el flete (FER, 2026-09-18).** En `[Logistico] Confirmaciones` → `pago_anticipado`: `activo` si · `cliente_no_valido` si · `ofrecer_a_todos` no · `cobrar_envio.activo` si · `cobrar_pedido.activo` no. 🔴 **El anticipo es un DEPÓSITO FIJO, no un porcentaje del flete (FER, 2026-09-22).** Es el
número que el dueño decide cobrarle al pedido que **no pasa ninguna de sus validaciones** — las
que él mismo puso: mínimo de pedidos, porcentaje de entregas y flete máximo por encima del cual el
cliente no califica. Por eso **no se pasa a "envío completo" para "dejarlo coherente"**: eso
cobraría el flete real y traicionaría la decisión. El monto se pregunta por espacio ("si el
cliente tiene malas métricas, cuánto es el anticipo"); el monto se escribe también en el prompt, porque el panel no tiene opción de monto fijo (su valor auxiliar solo aplica si no se extrae el flete). `estrategia_persuasion` se reescribe como **cobro**: el pedido sale solo con el envío pagado, valor exacto del sistema, cómo pagar, pedir comprobante, nunca decirle al cliente que tiene mal historial ni nombrar reglas internas, insistir una sola vez. La plantilla de fábrica lo vende como "beneficio prioritario, no obligación": es el uso contrario. **Datos que solo da el dueño y nunca se inventan:** medios y datos de pago con titular (búscalos primero en su config viva de ventas y carritos), y si el anticipo se descuenta del total (estándar de la casa: sí, se resta del total y al recibir se paga la diferencia). El anticipo **premia** al cliente: alistamiento prioritario, envío prioritario sin costo y seguimiento VIP; la prioridad es de preparación y despacho, nunca una fecha de entrega. Nunca "esta vez sí te llega": delata su historial. Si la ubicación promete "envíos gratis", avisar del choque.
- **Nunca inventes transportadoras ni tiempos:** se preguntan/confirman por negocio y país.
- **Vocabulario por país:** en Colombia se dice transportadora, domicilio (= el pedido), plata, mensajero; en México paquetería, pedido, dinero, repartidor. Ojo con **domicilio**: en Colombia es el pedido, en México es la casa — "para recibir tu domicilio" no se entiende en México.
- **Al clonar a otro cliente, los ganchos de venta del logístico fugan datos:** nombres de producto y de paquetería dentro de los ejemplos son texto que la IA imita (en una cuenta heredada aparecieron transportadoras colombianas y la marca del profesor en el workspace de un alumno). Parametrizar siempre, nunca quemar: nombre de la tienda, URL, nombre de la asesora, WhatsApp, tiempos de entrega y políticas de garantía.
- **Ante la duda, comparar contra un workspace que funcione** (Golden vende a diario), no contra lo que uno supone que debería haber: hay defaults que no son defectos.
- **No reimplementes la validación:** el prompt lo hace la hija `golden-chatea-pro-validacion-direcciones`. Este padre solo aporta los datos operativos y coordina.
- **Tiempos de entrega coherentes** con Ventas (`golden-chatea-pro-config-ventas-wp`) y Carritos (`golden-chatea-pro-config-carritos`).

## Conexiones (skills hermanas)
- 🧭 Hijo — prompt de validación de direcciones → `golden-chatea-pro-validacion-direcciones`
- 🛒 Asistente de ventas (dispara el logístico al pedir la dirección) → `golden-chatea-pro-config-ventas-wp`
- 🔁 Asistente de carritos (mismos tiempos de entrega) → `golden-chatea-pro-config-carritos`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales (transportadoras contratadas, tienda, cuentas) en los archivos de la skill. Se preguntan en cada uso.

## Fronteras y desambiguacion

Para configurar TODOS los asistentes a la vez, usa golden-chatea-pro-full-configuracion; para el prompt de validación en sí (el cerebro que decide si la dirección es entregable), la skill hija golden-chatea-pro-validacion-direcciones se activa sola desde aquí — no hace falta llamarla aparte.

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-chatea-pro-config-logistico
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-chatea-pro-config-logistico
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
El escritor por API trae su propia autoprueba sin red (7 casos en los dos sentidos: escribe y
verifica, se niega con un token de otro espacio, con estructura distinta o con un tope pasado,
deja pasar 2.000 de 2.000 y detecta un `200 ok` que no guardó):
```bash
python3 ~/.claude/skills/golden-chatea-pro-config-logistico/scripts/escribir_espacio.py --autoprueba
```
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-chatea-pro-config-logistico`

Historial completo en `references/changelog.md`.
