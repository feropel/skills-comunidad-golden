---
name: golden-chatea-pro-config-comentarios
description: >-
  Genera el JSON de configuración GENERAL del asistente de COMENTARIOS de Chatea Pro para
  una tienda (moderación de comentarios negativos, respuesta pública tipo community manager
  y venta conversacional que cierra en el mismo chat), con los prompts ya afinados y
  adaptados por país. Úsalo SIEMPRE que el usuario quiera montar o configurar el asistente
  de COMENTARIOS de Chatea Pro, generar o armar el JSON de comentarios, de respuesta pública
  o de venta conversacional, o diga cosas como "configura el asistente de comentarios",
  "arma el json de comentarios de chatea pro", "monta la respuesta pública de mi tienda",
  "necesito el config de comentarios". Dispara aunque no diga "JSON": basta con que quiera
  que el bot responda o modere los comentarios de sus publicaciones.
  Dispara tambien con la palabra VIP ("configura la chatea VIP de este cliente"): la
  configuracion es UNA SOLA para todos, VIP o no, y el VIP solo afecta a los productos.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 770 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare · (4) Esta skill estaba SIN BLINDAR: se le puso 'uchg' y se comprobo que el candado muerde. Para editarla: chflags -R nouchg <ruta>, y al cerrar chflags -R uchg.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
<!-- skill v1.21.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v1.18 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): el cuerpo estampaba v1.16 mientras el acta ya iba por v1.17 — la skill mentía sobre su propia versión. Y el mensaje de error del script ordenaba PREGUNTARLE al negocio la forma de la dirección, que es justo lo que la ley de FER del 06-sep prohíbe: se INVESTIGA. La doc de Argentina/Brasil describía el bug reparado como si fuera el comportamiento actual. Historial en references/changelog.md. -->
<!-- skill v1.19 · 2026-09-22 · REMEDICION DEL TECHO Y BASE UNICA (orden de FER). El tope de 20.000 se estaba tratando como ESCAPADOS cuando se mide en CRUDOS: de ahi salio un "techo practico de ~17.000 crudos" heredado de OTRO campo, y un gate que RECHAZABA con exit 1 configuraciones que la plataforma acepta sin problema. Medido en vivo: 19.617 crudos = 21.457 escapados entran y se releen identicos; 20.811 crudos dan error 500. Se derogo la via VIP de la configuracion general (la plantilla vieja no cabia y por eso existia la bifurcacion; la nueva cabe entera respetando los nueve topes). Se derogo la orden de convertir el campo a LONG JSON, que no se puede ni hace falta. El guardarrail dejo de citar NOMBRES de producto: ahora satura, y 1.000 productos pesan lo mismo que 20. Historial en references/changelog.md. -->
<!-- skill v1.20 · 2026-09-22 · fila de golden-chatea-pro-producto-comentarios. Se DEROGA lo que esta skill afirmaba del par array/Extendido ("en workspaces migrados el array esta vacio"): remedido hoy, los TRES campos espejo estan poblados y sincronizados, asi que escribir uno solo los desincroniza. La afirmacion vieja se dedujo por descarte de un caso con el array vacio, y deducir de un caso no es medir. Se anaden los topes del formulario de PRODUCTO (nombre 255, descripcion 500 confirmada en vivo, y rela topa en 10 ETIQUETAS, que es cantidad y no caracteres). NO se acepto del parte el techo "JSON = 20.000 ESCAPADOS": medido hoy en este mismo espacio, 21.457 escapados VIVEN en un campo array; la unidad es el CRUDO. Historial en references/changelog.md -->
<!-- skill v1.21 · 2026-09-22 · EL BANCO TAMBIEN SE VERIFICA. Medido: 9 de las 35 pruebas miraban el TEXTO de un mensaje y tres lo hacian con `not in`, que es el modo de fallo peor (un `in` roto da rojo y se ve; un `not in` roto da VERDE y no se ve). Las 18, 19 y 20 se reanclaron a la BANDERA --despectivo, que es interfaz y no prosa, y al contenido del resultado, en cobertura cruzada con la 17. Nace scripts/contraprueba.py, que corre sobre una COPIA en tmpdir y mide las dos direcciones: TOLERA que se reescriba la redaccion de dos avisos (35 de 35 en verde) y MUERDE cuando se rompe la conducta (2 pruebas en rojo). El primer sabotaje NO saboteaba: envolvia DATOS_POR_PAIS en un defaultdict y el script decide con `clave in`, asi que una clave nunca insertada sigue sin pertenecer; el banco se quedo verde y TENIA RAZON. Un sabotaje que no sabotea acusa al banco de un fallo que no tiene, asi que se verifico el sabotaje antes de acusar. El que muerde reintroduce el fallo real de septiembre: un pais sin pack heredando la direccion de Colombia. La prueba 20 se puso roja al reescribirla porque yo asumi exit 0 para guatemala y son 2 (el detector de colombianismos salta): el banco mordiendo a quien lo escribe. Historial en references/changelog.md -->
<!-- Historial de versiones COMPLETO en references/changelog.md (se saco del cuerpo el 2026-09-05: eran 25.710 caracteres, la mitad del SKILL.md, cargandose en cada activacion). Nada se borro. -->
# Chatea Pro — Config del asistente de comentarios

**Fábrica:** chat «✅ SKILL golden-chatea-pro-config-comentarios»
<!-- corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto. -->
<!-- v1.1 · 2026-08-07 (centro de mando, cosecha del chat ESTUDIO 360 DENTAL [producto de cliente] Chile) · build_config.py parcheado: ahora IMPRIME SIEMPRE el largo final del JSON generado y da ERROR visible (banner + exit code 2) si supera el tope del campo tipo JSON (20.000), recordando crear/convertir el Bot Field a LONG JSON y releer tras escribir. Motivo real: con datos de Chile el script generó 20.074 caracteres (74 sobre el tope) y el aviso genérico no gritó — un campo tipo JSON habría guardado el config CORTADO en silencio con la API respondiendo ok. Probado: caso normal exit 0, caso excedido banner ERROR + exit 2 con el archivo igualmente guardado. -->
<!-- v1.0 · sin sello previo (nota bandeja 2026-08-07: quedó en 1.0.0 por defecto en el repo público) -->

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
otra vez. Herramienta encadenable del barrido:
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (correrla ANTES de escribir y DESPUÉS releyendo del
servidor; sale con código 3 si encuentra algo CRITICA).

**LA MARCA VIVE TAMBIÉN EN PROSA LIBRE, no solo en campos estructurados.** Preservar las
llaves de identidad del destino NO basta: el nombre de la marca de origen viaja escondido dentro
de ganchos posventa, agradecimientos y plantillas de prompt. Al método de barrido se le añade el
paso `grep -i` por el NOMBRE de la marca de origen sobre TODO el texto que se va a escribir —
así se cazaron 10 menciones de la marca origen en 3 campos del destino que el mapeo de llaves
no vio.

Origen: 2026-08-08, al clonar la config de Golden a otro espacio se colaron la llave de ElevenLabs,
el teléfono, la plantilla de notificación y agradecimientos firmados con la marca del origen.
Revertido el mismo día desde respaldo.

Cómo clonar sin romper el destino (qué se copia, qué se preserva del destino, por qué las plantillas jamás viajan): memoria `reference_chatea_clonar_config_entre_espacios`.

### CAMPOS [Meta] = VALORES CALIENTES, NO INTERRUPTORES

Los bot fields `[Meta] Ver Contenido`, `[Meta] Agregar al carrito` y demás eventos de pixel los
**MUEVE EL FLUJO en tiempo real** mientras corren contactos — no son configuración estable. Caso
real (2026-08-08): se leyeron como "apagados" y cambiaron solos minutos después sin escritura de
nadie; la conclusión "el evento Comprar está apagado" tuvo que retractarse. **PROHIBIDO sacar
conclusiones de pauta o diagnóstico de una lectura suelta de esos campos**: se observan en ventana
(varias lecturas separadas en el tiempo) o se diagnostica el pixel en Meta directamente. Detalle:
memoria `reference_chatea_clonar_config_entre_espacios`.

Genera el JSON de configuración del asistente de **comentarios** de una tienda en Chatea Pro. Trae fijos y ya afinados: el clasificador de comentarios negativos, el prompt de respuesta pública (community manager + copywriter de la marca) y el prompt de venta conversacional (9 etapas, modo captura, objeciones, cierre en el mismo chat). Todo en español colombiano, humanizado y con precios en `$`.

**Guardarraíl anti-dolencias (obligatorio, viene en el template):** el clasificador trae la "REGLA QUE MANDA SOBRE TODAS LAS DEMAS" — un comentario que nombra la dolencia que el producto trata PREGUNTANDO si le sirve es un CLIENTE interesado y jamás se borra; solo se modera si la dolencia la CAUSÓ el producto ya usado o si ataca la reputación. Existe porque el clasificador stock borraba compradores que mencionaban su dolencia (bug real corregido en el bot vivo de Golden el 2026-08-08). El template trae los placeholders de DOBLE LLAVE `{{LISTA_DOLENCIAS}}` y `{{LISTA_PRODUCTOS_DOLENCIAS}}` (doble llave = los llena `build_config.py`; llave simple tipo `{DESCRIPCION_PRODUCTO}` = los llena Chatea en runtime — no confundirlos). Se rellenan pasando `--producto "Nombre:dolencia que trata"` (repetible, mínimo 1) con los productos de LA TIENDA DESTINO — nunca los de otra (ley de no-herencia, arriba); el script da ERROR DURO si algún `{{...}}` queda sin llenar.

Lo único que cambia entre tiendas es la **información del negocio**, que se pregunta al ejecutar.

## Autoprueba

Antes de entregar cualquier config, y siempre despues de tocar la skill:
`python3 ~/.claude/skills/golden-chatea-pro-config-comentarios/scripts/autoprueba.py`

Requisito de la autoprueba: PyYAML (`pip install pyyaml`), para leer la description en las pruebas 23 y 24.
35 pruebas, exit 0 = todo pasa. Cubre la base unica, el guardarrail anti-baneo, a quien NO
se borra, los topes que corta el Save del panel, el techo MEDIDO del campo, el catalogo de
1.000 productos y la integridad de la salida.

**Y el banco tambien se verifica, porque un verde no demuestra que sirva:**
`python3 .../scripts/contraprueba.py` — corre sobre una COPIA en tmpdir y mide las dos
direcciones: que TOLERE que se reescriba la redaccion de un aviso (si se pone rojo, mide
prosa) y que MUERDA cuando se rompe la conducta (si sigue verde, es decoracion). El
sabotaje reintroduce el fallo real de septiembre: un pais sin pack heredando la direccion
de Colombia. 3 de 3.

🔴 **Por que existe:** medido el 2026-09-22, 9 de las pruebas miraban el TEXTO de un
mensaje, y tres con `not in`, que es el modo de fallo peor — un `in` roto da rojo, que se
ve; un `not in` roto da **verde**, que no se ve. Ya habia pasado: hasta el 06-sep dos
pruebas comprobaban que se hubiera IMPRESO un aviso y pasaban en verde mientras el JSON
salia con el pack colombiano para Argentina. **Un banco que comprueba el mensaje certifica
la intencion, no la conducta.** Las tres se reanclaron a la BANDERA (interfaz) y al
contenido del resultado, en cobertura cruzada con la 17, que exige que el aviso SI aparezca.

## BASE ÚNICA: se acabó el VIP en la configuración general (FER, 2026-09-22)

**Hay UNA sola configuración y sirve para Colombia y para todos los países.** No preguntes por la
vía, no hay vía que elegir. `--vip` sigue aceptándose para no romper llamadas viejas, pero está
**derogado**: no cambia la salida y solo imprime un aviso.

**Por qué desapareció.** El VIP existía por un problema de espacio, no de categoría de cliente: la
plantilla vieja **no cabía** (respuesta pública 3.895 sobre un tope de 3.000, venta 10.771 sobre
8.000, ~22.7k en total). Como no cabía, hubo que inventar una variante recortada para quien pega
en el formulario y dejar la completa para quien pega el JSON.

La plantilla actual **cabe entera respetando los nueve topes nativos**, medido en producción el
2026-09-22: 19.617 crudos escritos por API y releídos idénticos. Una base que cabe sirve igual por
formulario que por JSON, así que la bifurcación perdió su razón de ser. Menos caminos, menos sitios
donde equivocarse.

**Dónde sí sigue existiendo el VIP:** en el manejo de **productos**, que es otra skill
(`golden-chatea-pro-producto-comentarios`). El panel muestra 500 por descripción de producto, pero
eso es validación del formulario: medido el 2026-09-22, un campo `[Comentarios] Productos` real
carga 7.249 caracteres. Exceder ese 500 por API es deliberado y **solo se hace para clientes VIP**.

**Lo que se conservó INTACTO de los prompts**, y no se toca aunque haya que ganar caracteres:

- Las **4 estructuras flexibles** y las **6 técnicas de persuasión** de respuesta pública. Son el
  guardarraíl anti-baneo, no estilo (ver la REGLA DURA de este mismo SKILL.md).
- El **máximo de 40 palabras**, que es medido.
- Toda la doctrina de venta: no saludar, cerrar aquí, sin emojis, moneda local, prohibida la
  palabra "descuento", no inventar nada fuera de la descripción del producto, releer la
  conversación y reconocer los datos ya enviados, pedir de a UNO por su nombre, responder la
  pregunta antes de pedir datos, salud fuera de la descripción remite al médico, eco una sola vez,
  tras confirmar no repetir, devoluciones con número de guía, mensajes de 1 a 3 líneas, y las
  **9 etapas completas** del flujo.

**De dónde salieron los caracteres:** de la redundancia, no de la doctrina. Las mismas reglas
estaban dichas hasta tres veces (en REGLAS, otra vez dentro de cada etapa y otra vez en el
checklist final) y los ejemplos venían de a tres donde uno basta.

### Si hay que ganar espacio, este es el orden

Se recorta **por orden de menor valor**, y ese orden no es opinión: lo primero que sale es lo que
no cambia ninguna decisión del bot.

1. **Justificación económica escrita para humanos.** El clasificador solo responde Si o No; saber
   cuánto encarece el costo por venta un comentario negativo no le cambia la respuesta.
2. **Ejemplos atados a NOMBRES de producto.** Además de pesar, caducan: el día que la tienda saca
   ese producto el prompt sigue citándolo sin dar error. Van sin marca.
3. **Repeticiones literales**, como la misma lista de datos escrita tres veces.
4. **Campos de negocio**: contacto, tiempos de envío, información extra.

Nunca se recorta la rotación anti-baneo ni los criterios de borrado.

## 🔴 LO ÚNICO QUE CAMBIA ENTRE ESPACIOS: la parte dinámica

**Los prompts son FIJOS. No se rediseñan por cliente.** Esta es la base de todos los espacios de
Chatea Pro (FER, 2026-09-22), y lo que se toca de un espacio a otro es solo esto:

| Qué | Dónde vive | Cómo entra |
|---|---|---|
| **País de operación** | `informacion_del_negocio.pais` y toda la nomenclatura de direcciones | `--pais` |
| **Nombre del negocio** | el ROL del clasificador (así el bot sabe de quién habla) | `--negocio` |
| **Cifras del negocio** (años, clientes, sede, garantía) | `info_extra` | `--info-extra` |
| **Contacto** | `contacto` | `--contacto` |
| **Tiempos de envío** | `t_envio` | `--t-envio` |
| **Dolencias que resuelve su catálogo** | guardarraíl del clasificador | `--producto` (repetible) |
| **Palabra despectiva local** | criterio 13 del clasificador | `--despectivo` |
| **Autorizaciones de venta** | `aut_link_pub`, `aut_precio_pub` | `--aut-link`, `--aut-precio` |

**El nombre de la asesora o del bot NO se configura aquí.** Es un ajuste del espacio, uno solo por
workspace, y vive fuera de esta configuración. Si el negocio lo pide, se cambia en el panel del
espacio, no en estos prompts. Ponerlo dentro de un prompt lo duplica y luego los dos se
contradicen.

**Los prompts pueden ajustarse al nicho** (una tienda de suplementos y una de electrodomésticos no
hablan igual), pero la **estructura no se toca**: ni la rotación anti-baneo, ni NEUTRO, ni el
criterio de a quién apunta la molestia, ni las 9 etapas de venta.

## Qué preguntar al usuario (intake)

Pregunta estos 5 datos, **uno a la vez** y en este orden. No los pidas todos de golpe.
1. **País** donde opera la tienda (ej: colombia), en el campo `[Comentarios IA] País`, MAYÚSCULA y sin acentos. **El país NO decide a quién se configura: decide CÓMO** — la jerga, las frases de envío y los campos de una dirección.
   **Ocho tienen pack de direcciones propio** en `build_config.py`: Colombia, Ecuador, Chile, México, Panamá, Perú, Paraguay y Guatemala. **A cualquier otro país no se le rechaza ni se le hereda un pack ajeno**: el script se niega a fabricar la lista y te manda a **INVESTIGARLA** —no a preguntársela al
   negocio— para volver con `--datos-cliente`. 🔴 **Ley de FER (06-sep):** *"La jerga y la
   configuración de las direcciones no se le pregunta a la gente, porque precisamente para eso
   es la skill. Tú tienes que ir a Internet, revisar, estudiar, analizar, extraer esa información
   y configurarla."* Se investiga con tres fuentes independientes del país; lo que no se confirme
   se marca NO VERIFICADO y **solo eso** se le confirma al negocio, diciéndole por qué.
   🔴 **Por qué se niega en vez de rellenar** (medido el 06-sep): las dos ramas avisaban de que heredar la nomenclatura de otro país produce direcciones no entregables **y a dos líneas devolvían el pack de Colombia**. Argentina y Bolivia salían pidiendo *Barrio, Ciudad, Departamento* — y en Argentina no hay departamentos. Un hueco declarado se llena; una dirección fabricada llega mal y nadie sabe por qué.
2. **Contacto**: una página web, un WhatsApp **o** un correo. Solo uno; es dato de referencia, no para mandar al cliente a otro canal.
3. **Tiempos de envío**: cuánto demora la entrega (ej: ciudad principal 2-3 días, intermedia 3-4, rural 5-7). Este dato **se pregunta siempre**, no se asume.
4. **Información adicional del negocio**: una o dos líneas de respaldo (sede, pago contra entrega, originalidad; si el usuario aporta años o clientes, que sean los REALES de SU negocio — jamás los del template ni los de otra tienda).
5. **Productos y su dolencia** (para el guardarraíl anti-dolencias): la lista de productos de la tienda con la dolencia/problema que trata cada uno, formato `Nombre:dolencia` (ej: `Serum X:hongos en las uñas`). Mínimo 1. Sin esto el clasificador no sabe qué dolencias son señal de compra y el script no genera.

### Datos que la IA le pide al cliente (campo `datos_req`) — se genera solo

En Chatea Pro existe el campo **"datos que la IA debe solicitar al cliente para completar la compra"** (en el JSON: `venta_conversacional.datos_req`). **No lo preguntes en el intake**: el script lo arma automáticamente según el **país** y su nomenclatura REAL de direcciones (8 de los 10 tienen pack propio; ya no existe el esquema "internacional" con Estado/Colonia/CP para todos, que era un criterio de México clonado y falso en Chile, Ecuador, Perú, Panamá y Paraguay):

- **Colombia**: Nombre completo; Número de WhatsApp; Dirección exacta; Barrio o punto de referencia; Ciudad; Departamento. (Sin código postal: no se exige.)
- **México**: Nombre completo; Número de WhatsApp; Dirección exacta; Colonia; Ciudad / Municipio; Estado; **Código Postal** (en México el CP es REQUERIDO: define la zona de reparto).
- **Chile**: Nombre completo; Número de WhatsApp; Dirección exacta (calle y número); **Comuna** (el dato rey); Región o referencia. (Sin código postal.)
- **Ecuador**: Nombre completo; Número de WhatsApp; Dirección exacta (calle principal y secundaria, o Mz y Villa/Solar); Barrio, ciudadela o referencia; Ciudad; Provincia.
- **Panamá**: Nombre completo; Número de WhatsApp; Dirección exacta o referencia clara; Barriada / urbanización o PH y apartamento; Corregimiento; Distrito; Provincia.
- **Perú**: Nombre completo; Número de WhatsApp; Dirección exacta (calle/jirón y número, o Mz y Lote); Urbanización o AA.HH.; **Distrito**; Provincia; Departamento.
- **Paraguay**: Nombre completo; Número de WhatsApp; Dirección (calle y entre qué calles o casi qué esquina); Barrio; Ciudad; Departamento; Referencia.
- **Guatemala**: Nombre completo; Número de WhatsApp; Dirección exacta con **ZONA** (ej. 5a avenida 12-34, Zona 10); Colonia, residenciales o aldea si es área rural; Municipio; Departamento. (Guatemala se ordena por zonas, no por barrio/carrera — pack tomado de `golden-chatea-pro-validacion-direcciones`, que lo tiene medido.)
- **Argentina y Brasil**: aceptados por la plataforma pero **AÚN SIN pack propio** en esta skill.
  🔴 **El script NO genera nada** para ellos sin `--datos-cliente`: sale con **exit 1 y sin archivo**.
  (Esta línea decía *"usa el de Colombia como placeholder — no lo entregues así"*. Eso era el
  **defecto**, corregido el 06-sep: heredar la nomenclatura colombiana producía direcciones no
  entregables —Argentina no tiene departamentos— y la doc se quedó describiendo el bug como si
  fuera el comportamiento. **Una doc que describe el fallo reparado es peor que ninguna**: hace
  que quien lea busque un archivo que no existe.) La forma de la dirección se **INVESTIGA** y se
  pasa con `--datos-cliente "campo1; campo2; ..."`.

Si el usuario quiere una lista distinta a la del país, pásala manualmente con `--datos-cliente "campo1; campo2; ..."` y el script la usa tal cual. `datos_req` tiene tope nativo de **200** caracteres.

**Qué cubre `--pais` HOY (sin ambigüedad):** solo (1) la lista `datos_req` del país y (2) la coherencia interna del prompt de venta (checklist, orden y confirmación de datos de envío salen del MISMO pack que `datos_req`). **Lo que NO cubre:** moneda (los prompts dicen pesos colombianos y $90.000), medios de pago (Nequi, Daviplata), ciudades de referencia (Bogotá, Medellín...) y jerga colombiana. Con `--pais` distinto de colombia el script GREPEA el resultado por esos colombianismos e imprime la checklist de **ADAPTACIÓN MANUAL PENDIENTE** con exit 2: no entregues sin adaptarla. El rediseño multipaís completo es proyecto aparte (bandeja del centro de mando).

### Lo que NO se pregunta aquí

No pidas **descripción, cantidades ni precios** de los productos: eso va **en la ficha de cada producto dentro de Chatea Pro**, no en esta configuración general (el prompt de venta conversacional lo lee por la variable `{DESCRIPCION_PRODUCTO}` que Chatea llena producto por producto). OJO, esto NO contradice el punto 5 del intake: la lista `Nombre:dolencia` SÍ se pregunta — es para el guardarraíl del clasificador, no una ficha de producto.

## Cómo generar el JSON

Con los 5 datos del intake, corre el script. Los prompts no se tocan: solo se reemplaza la información del negocio.

```bash
python3 scripts/build_config.py \
  --pais "colombia" \
  --contacto "<lo que dio el usuario>" \
  --t-envio "<tiempos de envío del usuario>" \
  --info-extra "<info del negocio del usuario>" \
  --producto "<Nombre:dolencia que trata>" \
  --producto "<OtroNombre:su dolencia>" \
  --out <negocio>_CONFIG.json \
  --destino longjson   # SOLO tras verificar EN EL SERVIDOR que el campo es longtext
```

**`--destino`:** por defecto es `array`, que es lo que son los campos de Comentarios y lo que
**no hay que cambiar**. El gate mide **CRUDOS contra 20.000**, con 400 de margen; si se pasa, da
exit 1 SIN archivo. Pasa `--destino longjson` solo si verificaste en el servidor que ese campo
concreto es longtext.

El campo `datos_req` (datos que la IA le pide al cliente) se genera solo según `--pais`. Solo agrega `--datos-cliente "campo1; campo2; ..."` si el usuario pide una lista distinta a la estándar del país.

**Semántica de exit codes (actualizada v1.19):** `0` = config **entregable**: placeholders llenos,
los nueve topes nativos respetados y el total por debajo de 19.600 crudos, que es lo que cabe en el
bot field. `1` = **error duro y NO se escribe archivo**: placeholder sin llenar, llave simple
desconocida, sin productos, producto malformado, un tope nativo excedido, o el total pasado del
techo del campo — jamás truncar en silencio ni entregar algo que el guardado va a rechazar.
`2` = exceso que muta la entrega, archivo sí escrito: colombianismos pendientes con `--pais`
distinto de colombia.

## 🔴 EL TECHO DEL CAMPO SE MIDE EN CRUDOS. Remedido el 2026-09-22

Esta sección decía lo contrario y **por eso rechazaba trabajo bueno.** Durante semanas la skill
trató el tope de 20.000 como si fuera en escapados, dedujo de ahí un "techo práctico de ~17.000
crudos" y puso un gate que abortaba con exit 1. Ese número venía de mediciones hechas en campos
`[Producto Ventas Wp]`, **no en este campo**: era herencia, no medida.

**Lo medido en producción**, campo `[Comentarios] Configuracion General` (tipo `array`):

| valor | qué pasó |
|---|---|
| 13.004 crudos | guarda |
| **19.617 crudos = 21.457 escapados** | **guarda por API y se relee idéntico** |
| 20.811 crudos | **error 500** al guardar desde el panel |

Es decir: **21.457 escapados viven sin problema.** La unidad es el crudo, el tope está en 20.000
y se trabaja bajo 19.600. El escapado se sigue imprimiendo, pero como dato informativo.

**No hay que convertir nada a LONG JSON.** El campo es `array`, su tipo no se cambia por API, y no
hace falta: aguanta la configuración completa. La instrucción de "crear o convertir el campo a LONG
JSON" que vivía aquí quedó derogada — pedía algo que no se puede hacer para resolver un problema
que no existe.

### La costura que ningún contador del panel muestra

Los topes nativos por campo **suman 24.100** y el campo aguanta **20.000**. El panel valida caja
por caja y **nunca la suma**: se pueden llenar las nueve en verde, con sus contadores en azul, y
que el guardado reviente igual.

**El fallo NO es silencioso** en este caso, y eso corrige otra cosa que decía esta skill: el panel
devuelve `Request failed with status code 500` y **aborta el campo entero** — no lo trunca. El
campo que falló queda vacío en el servidor y los demás intactos. Aun así, **releer del servidor
después de escribir sigue siendo obligatorio**: es la única prueba de que entró lo que se mandó.

🔴 **CUPO DE LA API: 1.000 peticiones por HORA, y pasarse BLOQUEA una hora entera.**
Medido contra la API viva el 2026-09-07: cada respuesta trae **`x-ratelimit-remaining`** (en
inglés *X-RateLimit-Remaining*, "las que quedan") y `x-ratelimit-limit`. **Se repone cada hora**,
pero **no viene `x-ratelimit-reset`**: el servidor no dice a qué minuto empezó la ventana, así que
si te bloqueas se espera una **hora completa** y se comprueba **mirando** el contador
(`golden-chatea-cupo [--necesito N]`), nunca calculándolo.

**Cuándo te afecta aquí:** `build_config.py` **no toca la red** —genera el JSON y lo deja en un
archivo—, así que generar no gasta nada. El cupo entra cuando ese JSON **se escribe** en el espacio
por API. Cuenta siempre **la escritura MÁS la relectura**: releer del servidor y comparar es la
única prueba de que no se cortó, y pasarse devuelve `200 ok` con el asistente muerto en silencio.

## REGLA DURA: la variación de estructura es un guardarraíl de CUENTA, no de estilo

El prompt de respuesta pública trae cuatro ESTRUCTURAS FLEXIBLES y seis TÉCNICAS DE PERSUASIÓN
para rotar, además de la orden "nunca repitas la estructura". **Eso no es adorno de copywriter:
es lo único que impide que Meta lea al asistente como un bot y tumbe la página.**

Queda escrito aquí porque la regla vivía sin su porqué, y una regla sin porqué la borra el
siguiente que quiera "compactar el prompt".

**Evidencia medida** (clase M7 de Kevin Galeano, 2026-09-02, dicha en vivo):

- A Kevin le inhabilitaron el ecosistema **tres veces**. La causa que aisló: la respuesta base de
  Chatea es siempre la misma frase ("Claro que sí, [nombre], el producto te sirve para X. Si
  deseas comprarlo, haz clic en el siguiente enlace"). Repetida comentario tras comentario, Meta
  la marca como automatización.
- Un alumno de la misma clase reportó **dos baneos**, ambos coincidiendo con encender el asistente
  de comentarios. Le duró **unos 15 minutos** respondiendo antes de caer, y se llevó por delante
  fanpage, BM y perfil personal, en ese orden.
- Kevin: *"Meta no banea por exceso de mensajes. Sí nos pueden inhabilitar la fanpage si
  utilizamos la misma estructura de comentarios para responder."* Tras meter las cuatro
  variaciones, dejaron de inhabilitarle las páginas.

**Qué NO se puede tocar del prompt de respuesta pública**, por este motivo:

- Las 4 estructuras flexibles (todas terminan en CTA; esa parte sí es fija).
- Las 6 técnicas de persuasión y la orden de rotar entre ellas.
- La línea "nunca repitas la misma estructura" de RESTRICCIONES y la de CHECKLIST.
- Los 4 ejemplos con la MISMA pregunta y distinto enfoque: son la demostración de la rotación.

Si hay que recortar caracteres, se recorta de los campos de negocio, nunca de aquí.

**El máximo de 40 palabras también es medido**, no una preferencia: probaron de 20 a 120 y 40 fue
el que mejor rindió. Es ajustable por tienda, pero quien lo cambie debe registrar el número que le
funcionó, no moverlo a ojo.

## Autorizaciones: dos interruptores que son decisiones de venta

Debajo del prompt de respuesta pública, el panel trae `Autorizaciones` con dos interruptores. Van
en el JSON como `respuesta_publica.aut_link_pub` y `respuesta_publica.aut_precio_pub`, y se
controlan con `--aut-link si|no` y `--aut-precio si|no`. El script los imprime SIEMPRE en el
reporte, porque un interruptor que nadie ve es uno que nadie revisa.

| Interruptor | Por defecto | Por qué |
|---|---|---|
| `aut_link_pub` (enlace) | **no** | Mandar al cliente a la web lo saca del anuncio y lo enfría. Con el enlace apagado, el asistente cierra en la misma conversación. Enciéndelo solo si el cierre real ocurre en la landing. |
| `aut_precio_pub` (precio) | **sí** | El precio filtra curiosos en público y no cuesta el lead: al responder el comentario, el asistente abre el privado por su cuenta y arranca la conversación igual. |

El default del enlace era `sí` hasta la v1.8 y **contradecía al propio prompt**, que en OBJETIVO DE
CANAL ordena no mandar al cliente a otro enlace. Corregido.

⚠️ Y un tercer interruptor, arriba del todo: si "respuesta pública automática" queda **apagado**,
el asistente **solo elimina y no responde nada**. Un cliente que comenta "precio" no recibe
respuesta. Encendido siempre, salvo que se quiera pura moderación.

## Cómo lo usa el usuario

El JSON resultante se pega en Chatea Pro. Aunque la respuesta pública y la venta conversacional superen su tope nativo por campo (3.000 y 8.000), al pegar el JSON completo el backend solo valida el total del campo, así que entra sin problema.

### Techo B — los topes NATIVOS del formulario (y por qué igual importan)

Escribir por API (o pegando el JSON) por encima del tope nativo funciona y no da error. Pero el día que alguien **abra ese formulario en el panel y pulse Guardar, el campo se corta y se pierde el texto**. Adviértelo siempre al entregar: si los prompts superan su tope nativo, nadie debe guardar desde el formulario de Comentarios sin revisar. Topes del panel de Comentarios (extraídos del código de la app, 2026-08-07 · `TOPES-NATIVOS-POR-CAMPO.md` de CHATEA-PRO-ASISTENTES-MAPA):

| Campo | Tope |
|---|---|
| `comentarios_negativos.prompt_general` | 10.000 |
| `venta_conversacional.prompt` | 8.000 |
| `respuesta_publica.prompt` | 3.000 |
| `ej_a_eliminar` · `ej_a_no_eliminar` | 1.000 c/u |
| `informacion_del_negocio.info_extra` | 500 |
| `contacto` · `t_envio` · `datos_req` | 200 c/u |
| descripción del producto de Comentarios | 500 |

Topes del formulario **de producto** (medidos en los contadores del panel el 2026-09-22 por
`golden-chatea-pro-producto-comentarios`, que es quien los usa): nombre **255** · descripción
**500** confirmado en vivo · y el que más duele, **`rela` topa en 10 ETIQUETAS**, que es un tope
de CANTIDAD, no de caracteres: un `rela` que funciona lleva 25-30 disparadores, así que por
formulario se pierde la cola, que es justo donde están los hooks del anuncio.

### Gotchas del asistente de Comentarios (si se escribe por API)

Cargar cada producto (con su `rela` de disparadores) NO es trabajo de este skill — es `golden-chatea-pro-producto-comentarios`. Lo de abajo es contexto para entender el terreno, no una tarea que este skill ejecute.

- El producto de Comentarios es un objeto de **5 llaves exactas**: `img`, `name`, `desc`, `rela`, `estado`. Con 4 llaves el panel no lo interpreta.
- El `img` del producto usa URLs `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` que **solo nacen subiendo la imagen en el panel** (en los 225 endpoints de la API no hay subida). Copiar la URL de otra cuenta apunta a la cuenta de origen.
- 🔴 **Par `array` / `Extendido`: DEROGADO lo que decía aquí (2026-09-22).** Esta línea afirmaba que en workspaces migrados el array está VACÍO y los productos viven solo en el Extendido. **Remedido hoy en un espacio real: los dos están POBLADOS y SINCRONIZADOS** (array 7.249 caracteres · extendido 7.061 · y un tercero, `TOON Productos`, 7.017). La afirmación vieja se dedujo por descarte de un caso donde el array estaba vacío, y deducir de un caso no es medir. **Consecuencia práctica: escribir uno solo de los tres los DESINCRONIZA.** Sigue siendo cierto que leer el array vacío y concluir "no hay productos" es un error, y que el tipo de un campo existente no se cambia. **Compuerta abierta:** nadie ha comprobado cuál de los tres lee el flujo en ejecución; hasta que alguien comente en un post de prueba y mire qué responde, no se escribe ninguno por API. Esta skill **no toca esos campos** — son de `golden-chatea-pro-producto-comentarios`.
- `PUT /flow/set-bot-fields-by-name` usa la llave **`data`** (con `bot_fields` responde 400); `POST /flow/create-bot-field` usa **`var_type`** y exige `value` (si no, 422); `GET /flow/bot-fields` **PAGINA** y `per_page` se ignora.
- Al escribir por API, el valor va como string con `ensure_ascii=False, separators=(',',':')` (compacto): otro formato infla el conteo contra el techo sin cambiar el contenido. El JSON con `indent` que genera el script es para PEGAR en el panel; para API, compactarlo.
- **Escribir y RELEER siempre:** comparar el valor guardado contra el enviado es la única prueba real.
- **Corchetes `[enfermedad]` y `[ ]` del template son ILUSTRATIVOS**, no rellenables: `[enfermedad]` enseña al bot de venta la clase de pregunta de salud, y los `[ ]` son la checklist del modo captura. No tocarlos. Lo rellenable usa DOBLE llave `{{...}}` y lo valida el script.
- **Al clonar a otro cliente:** vaciar `[Comentarios] Productos` y el Extendido (catálogo del dueño) y jamás arrastrar `[Integraciones] Datos de integracion` (llaves en texto plano). Si se carga un producto de ejemplo para enseñar, va siempre con `estado` inactivo: enseña, no vende.

## Después: la ficha del producto (aparte)

Esto es referencia, no lo genera este skill. Cada producto se carga aparte en Chatea Pro con este formato (es lo que llena `{DESCRIPCION_PRODUCTO}`):

```
✨ [Nombre del producto] ✨
[Descripción del beneficio principal + características]

💰 Precios:
1 unidad: $XX.XXX
2 unidades: $XX.XXX
3 unidades: $XX.XXX

🚚 Envío gratis | Pago contra entrega
👉 [link del producto]
```

Ahí van la cantidad y los precios. Una tienda se configura una sola vez con este skill; los productos se cargan tantas veces como productos haya.

## Conexiones (skills hermanas)

Este skill configura **solo** la parte GENERAL del asistente de comentarios (prompts, país, negocio). Deriva cuando el pedido sea más amplio o más puntual:

- **Todos los asistentes a la vez** (comentarios + logístico + ventas WhatsApp + carritos) → `golden-chatea-pro-full-configuracion` (orquestador).
- **Asistente de ventas por WhatsApp** (Bot Fields, embudo, prompt maestro) → `golden-chatea-pro-config-ventas-wp`.
- **Asistente logístico / novedades preventivas** → `golden-chatea-pro-config-logistico`.
- **Carritos abandonados** → `golden-chatea-pro-config-carritos`.
- **Los TEXTOS del prompt de venta por producto** (no la estructura) → `golden-chatea-pro-prompt-ventas`.
- **Cargar/editar UN producto dentro del asistente de comentarios** (el objeto de 5 llaves `img/name/desc/rela/estado` de `[Comentarios] Productos`, para que el bot reconozca de qué producto habla cada comentario) → `golden-chatea-pro-producto-comentarios`. Esta skill deja la config general lista; esa hermana carga cada producto encima, uno por uno.

## Privacidad (skill compartible)

Este skill se comparte. Los prompts son genéricos y la información del negocio se pregunta al ejecutar; **nunca** hornees dentro de la skill datos reales de un negocio o cliente (WhatsApp, nombre de tienda, sede, cifras). La plantilla base usa valores de ejemplo obviamente ficticios que el intake sobrescribe siempre.

## Fronteras y desambiguacion

**NO es esta skill si lo que se quiere es cargar UN producto suelto del asistente de comentarios** (el objeto de 5 llaves img/name/desc/rela/estado): eso lo hace `golden-chatea-pro-producto-comentarios`. Esta configura la tienda ENTERA una sola vez; la hermana se corre cada vez que entra un producto nuevo. La desambiguacion vive aqui abajo y no en la description porque arriba solo va lo que hace DISPARAR, y el tope de 1024 es duro: las dos skills hablan de comentarios y las dos estaban cerca del muro.

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Genera el JSON de configuración GENERAL del asistente de COMENTARIOS de Chatea Pro para una tienda (moderación de comentarios negativos, respuesta pública tipo community manager y venta conversacional que cierra en el mismo chat), con los prompts ya afinados y la nomenclatura de direcciones del país (la moneda y la jerga se adaptan a mano: el script avisa). Úsalo SIEMPRE que el usuario quiera montar o configurar el asistente de COMENTARIOS de Chatea Pro, generar o armar el JSON de comentarios/respuesta pública/venta conversacional, o diga cosas como "configura el asistente de comentarios", "arma el json de comentarios de chatea pro", "monta la respuesta pública de mi tienda", "necesito el config de comentarios". Si el usuario quiere configurar TODOS los asistentes a la vez (comentarios + logístico + ventas WhatsApp + carritos), eso lo hace golden-chatea-pro-full-configuracion; el asistente de VENTAS por WhatsApp lo hace golden-chatea-pro-config-ventas-wp; los TEXTOS de venta por producto los hace golden-chatea-pro-prompt-ventas; cargar o editar UN producto puntual dentro de Comentarios (el objeto img/name/desc/rela/estado, para que el bot sepa de qué producto habla cada comentario) lo hace golden-chatea-pro-producto-comentarios. NO sirve para configurar productos como cantidad y precios, que van en la ficha del producto y no en esta configuración general.
