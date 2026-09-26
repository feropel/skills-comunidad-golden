## skill v4.17 · 2026-09-22 · Centro de Mando reverifico v4.16 EN VIVO, doble negativo aclarado

El CdM releyo del servidor de Golden y del disco (no confio en mi acta): 86 campos, Disparador
Extendido con 12 entradas y 2.735 caracteres, cero campos de remarketing (el borrado quedo limpio).
Confirmo tambien que los 5 arreglos de v4.16 estan realmente en el codigo, no solo en el acta; su
primera alarma sobre push_config.py resulto ser un grep que pesco mi PROPIO comentario explicativo
("comparar guardado == d[\"value\"] daba un..."), no el codigo real -- la retiro el mismo, con
evidencia.

Dos preguntas quedaron, y las dos se verificaron contra el servidor antes de contestar:

1. Doble negativo en "[WhatsApp IA] Desactivar consulta de recordatorios". El nombre invita a
   confusion: es un negativo (Desactivar) sobre la CONSULTA, no sobre el recordatorio. false NO es
   "recordatorios apagados" -- es "la consulta de estado del producto NO esta desactivada", o sea
   la consulta esta ACTIVA (el recordatorio SI revisa el producto antes de enviarse, mas exacto,
   mas lento). true es el que apaga la consulta. El valor false que quedo en Golden es el correcto
   (el estandar de la propia skill, campos-sueltos.json linea del `valor_por_defecto`); releido del
   servidor ahora mismo, sigue en false. Sumada `_trampa_doble_negativo` en campos-sueltos.json
   para que el siguiente que lea el campo no lo invierta por el nombre solo.
2. `[Ventas Wp] Disparador de productos` (sin Extendido) vacio: ya estaba documentado por diseno en
   SKILL.md, seccion de casos borde ("Par Disparador / Disparador Extendido"): Chatea migro, el
   campo viejo queda VACIO a proposito, el vivo es el Extendido. Se confirma que sigue ahi y se le
   senala al CdM la linea exacta.

Bancos re-corridos tras la nota: `autoprueba_auditor` 26/26 · `autoprueba_push` 12/12 ·
`autoprueba_d1` 9/9, sin cambio de conducta (la nota es metadata, no afecta a build_config.py ni a
push_config.py).

## skill v4.16 · 2026-09-22 · AUDITORIA golden-skill-auditor AUDITA+ARREGLA + retirado el puntero a remarketing

Pedido de FER: "que se automejore... y se autoevalue hasta que llegue a mil de mil". Primera
pasada (AUDITA, sin tocar archivos) dio 890/1000 PLATA con 5 hallazgos. Reparados los 5:

1. Argentina y Brasil quedaban con vocabulario "sin pack" en SKILL.md, references/paises.md y
   assets/limites.json (`_paises`), pese a que el propio mapa de 23 paises (v4.13) ya los cubre
   desde hace 2 dias. Corregido en los 3 sitios, con el rastro dejado a proposito para que se
   vea la clase de fallo (dato que caduca solo).
2. `push_config.py` comparaba el TEXTO crudo tras un push, contradiciendo lo que
   references/espacio-existente.md documenta ("comparar el JSON PARSEADO, la API recorta el
   \n final"). Corregido: compara `json.loads(guardado) == json.loads(enviado)`.
   `autoprueba_push.py` gano la promesa 5 (12/12): un archivo con salto de linea final ya no
   se reporta como TRUNCADA.
3. `auditar_espacio.py` solo sabia detectar fuga de vocabulario COLOMBIANO (hardcodeado
   "departamento"/"barrio", y "barrio" ni siquiera es unico de Colombia). Generalizado a los
   23 paises: `TERMINOS_PROPIOS_POR_PAIS` deriva, por pais, los terminos de su
   `campos_memoria` que NINGUN otro pais usa. Dos bugs propios cazados por el banco antes de
   sellar: (a) un termino generico ("tipo", de "tipo de via" en el pack de Guatemala) colaba
   un DEFECTO falso sobre la base limpia de Mexico ("tipo de producto" en
   reglas-estructura-producto.txt) -- corregido con `GENERICOS`, una lista de espanol comun
   excluida con su porque; (b) el `break` de "ya se encontro" y el de "es mi propio pais" eran
   el MISMO break, asi que auditar un espacio de ARGENTINA nunca llegaba a comparar contra
   ningun otro pais (A es la primera letra del roster ordenado). Separados en `continue`/`break`.
   Sabotaje nuevo cruzado (Mexico -> Argentina, no solo Colombia -> Mexico) prueba la
   generalizacion.
4. `valida_producto.py`: `check_apertura` (signos de apertura) no cubria `remarketing.prompt_1/2` (misma clase
   de prompt-instruccion que los recordatorios, que si se cubrian) ni los textos de upsell
   (titulo/descripcion/boton, visibles al cliente) ni `dta_prompt` (descripcion del producto).
   Sumados los tres. Sabotaje nuevo en autoprueba_auditor.py prueba el caso remarketing.
5. `references/espacio-existente.md` decia "18 campos sueltos"; se "corrigio" a mano a 16
   (contando solo booleanos+textos de campos-sueltos.json) y esa correccion estaba MAL: la
   categoria "interruptores" del auditor de verdad toca 18 campos (13 booleanos + 2
   `[WhatsApp IA]` por valor + 3 textos por existencia). El "18" original era correcto para
   lo que el codigo hace; la version SKILL.md "16 Bot Fields sueltos" es una definicion
   DISTINTA (el total estructural de campos-sueltos.json, sin los 2 de WhatsApp IA). Corregido
   con la cifra exacta y que criterio aplica a cada bloque, no un numero suelto.

Bancos, antes -> despues: `autoprueba_push` 10/10 -> 12/12 · `autoprueba_auditor` 24/24 ->
26/26 (16 clases de fallo, antes 14) · `autoprueba_d1` 9/9 sin cambio · `autoprueba_vocabulario`
299/299 sin cambio · `verificar_pais_no_es_puerta.sh` 4/4 sin cambio.

Tambien, fila del Centro de Mando (orden directa de FER): la skill `golden-chatea-pro-config-remarketing`
salio del ecosistema (borrada del disco, memoria y registro de fabricas). Retirado el puntero
en "Conexiones (skills hermanas)". El campo `Producto Remarketing` DE ESTA skill (recordatorios
y paquete de venta por producto) es distinto y no se toco -- FER lo confirmo explicitamente.

## skill v4.15 · 2026-09-21 · REVERIFICACION del Centro de Mando: 7 de 7 sabotajes detectados, un pulido

El CdM reverifico v4.14 sobre una copia con SUS PROPIOS sabotajes (no los mios): 295/295 limpio y
7 de 7 detectados -- los tres del 21-sep mas cuatro nuevos, entre ellos el mas delicado: meter
"estado" (la excepcion nombrada de MEXICO) en COLOMBIA. La rechaza: la excepcion de A_MANO queda
atada al pais, no abre una puerta lateral.

Un pulido, no urgente: borrar un pais entero del mapa (probo quitando CHILE) no fallaba limpio,
reventaba con `KeyError: 'CHILE'` y traceback -- salia distinto de cero (la compuerta cumplia)
pero el mensaje no decia que paso.

Hecho: `PAISES_MAPA`, el roster ANCLADO por NOMBRE (23 paises, no solo el numero que ya anclaba
`PAISES_ESPERADOS`, que ahora se LEE de este roster). `diferencias_de_roster()` compara el mapa
contra el roster y dice "falta CHILE" o "sobra X" antes de que nada mas lo indexe a ciegas.
`scripts/autoprueba_vocabulario.py` sumo K (la excepcion atada al pais: "estado" en Colombia se
rechaza) y L (borrar un pais se nombra, no truena; un pais fuera del roster se nombra como
"sobra"), y J se protegio con un `in` antes de indexar para no repetir el mismo defecto sobre
otro pais ausente. Probado end to end: borrar CHILE de una copia completa de la skill y correr
el script da un aviso limpio ("faltan ['CHILE']"), sin traceback, exit 1.

299/299 verdes sobre el mapa real. Con esto el Centro de Mando dio cerrada la extension del
vocabulario de direccion. Los otros 4 bancos, sin tocar: `autoprueba_push` 10/10 ·
`autoprueba_d1` 9/9 · `autoprueba_auditor` 24/24 · `verificar_pais_no_es_puerta.sh` 4/4.

## skill v4.14 · 2026-09-21 · TRES PUNTOS CIEGOS DEL BANCO DE VOCABULARIO, medidos por el Centro de Mando

El CdM verifico v4.13 en una copia (267/267, 23 paises, sus dos condiciones se sostienen) y ademas
la someti a tres sabotajes que el banco anterior dejaba en 100% VERDE:
1. `campos_memoria` alterado (Colombia "departamento" -> "provincia") -> 268/268 verdes. El peor:
   ese es el campo que termina en el prompt del asistente, y el banco solo comprobaba que la CITA
   siguiera literal, nunca el campo derivado. El total tambien subio solo porque el banco derivaba
   sus casos del propio contenido que revisaba.
2. `aclaracion` alterada (Colombia -> "Da igual el barrio.") -> 267/267.
3. `origen` borrado en un parafraseado (Chile) -> 267/267.

Hecho: `scripts/generar_vocabulario.py` gano `validar_contenido_contra_pack()`, que exige que CADA
termino de 4+ letras de `campos_memoria`, `aclaracion` y `aclaracion_corta` -de las 23 entradas,
incluidas las DOS a mano- este tambien en el TEXTO COMPLETO de su pack (no solo en su cita), y
`ORIGENES_VALIDOS`, un conjunto cerrado de tres valores que toda entrada debe declarar. Unica
excepcion, nombrada y documentada: "departamento" (Colombia) y "estado" (Mexico) -termino por
termino, no en bloque- porque `campos_memoria` es la ficha completa que recuerda el asistente de
VENTAS (incluye la division administrativa superior) y el pack de validacion-direcciones valida
solo la CALLE, que no necesita nombrarla. El total de paises quedo ANCLADO en `PAISES_ESPERADOS`
(23), no vuelve a salir de contar el mapa.

`scripts/autoprueba_vocabulario.py` sumo H (total anclado + origen cerrado), I (contenido contra
el pack sobre el mapa real: cero avisos, control positivo) y J (reproduce LITERAL los tres
sabotajes del CdM sobre una copia y prueba que los tres salen rojos). Probado tambien end to end:
los tres sabotajes aplicados a una copia completa de la skill hacen salir el script con exit 1.
295/295 verdes sobre el mapa real. Los otros 4 bancos, sin tocar: `autoprueba_push` 10/10 ·
`autoprueba_d1` 9/9 · `autoprueba_auditor` 24/24 · `verificar_pais_no_es_puerta.sh` 4/4.

## skill v4.13 · 2026-09-20 · MAPA DE VOCABULARIO DE DIRECCION DE 23 PAISES (autorizado por el Centro de Mando)

Hasta hoy solo Colombia y Mexico tenian vocabulario de direccion propio; los demas caian al generico
neutro. El Centro de Mando autorizo extenderlo desde los packs de golden-chatea-pro-validacion-direcciones
con dos condiciones: que el pack sea la fuente y no una traduccion mia, y que un pais sin pack se quede
sin vocabulario en vez de heredar el de Colombia.

Hecho: `scripts/generar_vocabulario.py` copia del pack, sin interpretar (campos_memoria de la linea
"Bien estructurada", aclaracion de la linea "no es direccion: pide") y guarda `fuente` y la cita literal
en `assets/limites.json`. 23 paises en el mapa: 2 escritos a mano y anclados al pack (Colombia, Mexico;
Colombia sigue saliendo byte a byte igual al espacio real de Golden), 18 derivados mecanicamente y 3
parafraseados con cita (Chile, Guatemala, Panama: sus packs no traen la linea limpia; marcados
`origen: parafraseado del pack`). Ecuador toma la variante Sierra/general.
`build_config.py` normaliza la clave del pais (Espana, costa-rica, Costa Rica) porque los packs viven sin
acentos. Nuevo banco `scripts/autoprueba_vocabulario.py` (267/267; probado que muerde: una herencia de
Colombia y una cita alterada se ponen en rojo).

Sin cambio: `paises_validos` (10) y `moneda_por_pais` (10) siguen igual; el pais es parametro, no puerta.
Un pais fuera del mapa cae al generico declarado. Los promedios de flete de los otros 9 paises siguen
sin existir en disco (solo Colombia 25000).

Tambien: dato 6 del intake lleva la ley de credenciales del Centro de Mando (guardado temporal solo en
`<PROYECTO>/.secrets/` con permisos 600; nunca en .md, JSON ni en la skill, repositorio publico).

## skill v4.12 · 2026-09-19 · INTAKE AL CLIENTE Y FLETE (estandar de FER, via Centro de Mando)

Cambio de estandar autorizado por FER el 19-sep y trasladado por el Centro de Mando. Vale igual para
instalacion nueva y para optimizacion de un espacio en uso.

**Intake, SIETE datos al cliente:** 1 nombre y link de la tienda · 2 pais · 3 dropshipping, marca propia
o los dos · 4 nombre del asesor · 5 WhatsApp de la empresa · 6 correo y contrasena del espacio · 7 desde
que valor un flete ya es demasiado caro. Salen: el NICHO (se lee de la web; en catalogo va sin nicho) y el
NUMERO DE SERVICIO AL CLIENTE. El WhatsApp va de ULTIMO y despues del pago: sin el se monta igual con la
notificacion apagada. El dato 6 es ACCESO y no un campo (excepcion autorizada a "todo lo que se pregunta
cae en un campo"): nunca se escribe en archivos ni se repite, la API va por token y el asistente no teclea
contrasenas en formularios.

**Flete = promedio nativo del pais + el corte del cliente.** Antes el flete "se derivaba del pais" y
punto. Ahora el promedio del pais es el valor nativo (`flete_max_por_pais`) y el corte que dice el cliente
(`--flete-max`, acepta "25.000" o "$25 000") manda encima; quien no sabe responder se queda con el nativo.
Si el ticket promedio subio, el tope lo sube Golden o se consulta; NO se deriva del ticket ignorando el
promedio del pais. Pais sin promedio y sin corte: se detiene y pide el dato al Centro de Mando.

**Optimizacion: al cliente no se le consulta nada mas** (salvo el flete). Las DECISIONES del auditor las
resuelve Golden, no el cliente.

DECLARADO: el promedio de flete de los otros NUEVE paises no esta en ningun archivo que la skill pueda
leer (solo Colombia, 25000); se anaden cuando el Centro de Mando los entregue. Hasta entonces un pais sin
promedio necesita el corte del cliente por `--flete-max`.

## skill v4.11 · 2026-09-18 · IDENTIDAD REAL, PAIS DERIVADO Y AUDITORIA REPETIBLE

Sesion de fabrica con el espacio real de Golden (Colombia) como referencia y un espacio de Mexico
como contraste. Todo lo de abajo se EJECUTO; lo que no, esta declarado al final.

**Intake, 7 datos**: pais · nombre de la empresa · dropshipping / marca propia / mixto · nicho
(OPCIONAL) · URL · numero de servicio · nombre del bot. El nicho depende del modelo: en un catalogo
una muestra de productos cargados NUNCA prueba una especialidad (error medido: se derivo "cuidado
capilar y bienestar" de 12 productos de un dia y la empresa vendia mucho mas); en marca propia si
se puede derivar.

**Vocabulario de direccion por pais, derivado y no escrito a mano.** Habia TRES assets con jerga
colombiana horneada (rol, restricciones y `reglas-estructura-producto.txt`); un espacio de Mexico
salia con "departamento" y "barrio". Mapa nuevo `vocabulario_direccion_por_pais` en limites.json
(fuente: las packs de `golden-chatea-pro-validacion-direcciones`) y huecos `{{CAMPOS_DIRECCION}}`,
`{{ACLARACION_DIRECCION}}`, `{{ACLARACION_CORTA}}`. Pais sin entrada: NO bloquea, cae a un generico
neutro y lo declara. El tercer asset lo destapo el auditor nuevo en su primera corrida.

**`--modelo mixto` (nuevo).** Su primera version NUNCA genero: la regla de pago era mas larga y las
restricciones pasaban el tope por 14 caracteres, y ademas emitia los interruptores de recaudo AL
REVES. Corregido: contra entrega por defecto, anticipo como excepcion, como opera Golden en vivo.

**Interruptores.** `assets/campos-sueltos.json`: 13 booleanos + 3 textos + 2 de `[WhatsApp IA]`
(7 campos de ESTADO del bot quedan marcados NO_TOCAR, 1 pendiente declarado). Oficina se deriva del
pais, Solo Con/Sin Recaudo del modelo. Se emiten en `<prefijo>_CAMPOS_SUELTOS.txt`.

**Validador de producto.** `--registro` acepta el array REAL del Disparador (antes reventaba con un
AttributeError crudo); el precio se busca tambien como "$74.900" / "74,900" (el falso positivo saltaba
en 12 de 12 productos de un catalogo real).

**push_config.** El filtro `name` de la API casa por coincidencia PARCIAL (medido en vivo: pedir
"...Configuracion general" devuelve tambien "...general 2"); `read` y `backup` ahora avisan.

**NUEVO `scripts/auditar_espacio.py`** (solo lectura, nota medida sobre 1000, DEFECTO / DECISION /
AVISO) y su banco `autoprueba_auditor.py` (18 de 18: cuatro bases limpias que deben dar 1000 y 14
sabotajes con el hallazgo exacto). Corrido contra el espacio real de Golden dio 930 con 0 defectos y
9 decisiones del dueño.

**Guardarrail roto y arreglado.** `verificar_pais_no_es_puerta.sh` gritaba "volvio la puerta" porque
sus llamadas a build_config tenian la firma vieja (un banco roto se ve igual que una herramienta
rota). Actualizado, 4 de 4.

DECLARADO, no oculto: (1) la ESCRITURA de `push_config.py` sigue sin probarse contra la API real (en
esta sesion solo se ejercieron `read` y `backup`); (2) `golden-blindaje` no sigue `assets/prompts/`,
asi que sus pares subcuentan lo que cambio; (3) el auditor valida los JSON, no la conversacion real.

## skill v4.10 · 2026-09-08 · MEDIDA CONTRA EL ESPACIO REAL

🔴 **DEFECTO 2 DEROGADO el 2026-09-08 por FER:** *"plantillas no necesitamos para nada"*. El hallazgo de abajo es correcto como MEDICION —el espacio vivo de Golden si lleva una plantilla aprobada, y sin plantilla el aviso no sale fuera de la ventana de 24 h— pero la DECISION es no usarlas. `notificacion_1.plantilla` queda vacia y no se pregunta. Las banderas `--plantilla-notif` y `--plantilla-ns` siguen en el script, sin usarse en el flujo normal. El DEFECTO 1 (tope de 50 en el NOMBRE del campo) sigue VIGENTE.

skill v4.10 — 2026-09-08 — MEDIDA CONTRA EL ESPACIO REAL, no contra la idea del espacio.
FER pego las capturas del panel y los DOS JSON completos de su espacio vivo (Golden Group).
Primera vez que esta skill se compara contra produccion en vez de contra su propia plantilla.

LO QUE CONFIRMO, y es la mejor noticia: **24 de 24 llaves, coincidencia EXACTA**. La plantilla
cubre justo las mismas llaves que el JSON real, ni una de mas ni una de menos. La estructura
estaba bien. Las diferencias estaban en los VALORES, que es donde nadie mira.

🔴 DEFECTO 1 · EL NOMBRE DEL CAMPO TIENE TOPE Y NO ESTABA CONTADO. Las capturas lo enseñan:
"[Ventas Wp] Configuracion general" marca **33/50** y "...general 2" marca **35/50**. Es un
TERCER techo, y el peor de los tres: el flujo lee las claves POR NOMBRE, asi que un nombre
cortado deja al bot sin encontrar su propio campo. Añadido `nombre_campo: 50` a limites.json y
comprobado en build_config, que ahora imprime `[33/50]` y `[35/50]` — los mismos numeros que el
panel, verificado contra la captura.

🔴 DEFECTO 2 · LA PLANTILLA DE META SALIA VACIA. El JSON real de FER lleva name
(`golden2_venta_asistente_wp`) y namespace de una plantilla aprobada; esta skill escribia los
tres campos en "". **WhatsApp solo deja texto libre dentro de la ventana de 24 h, y un aviso de
venta casi siempre cae fuera: sin plantilla NO SALE.** La notificacion queda `activa: si`, con
el numero correcto, y no llega — se ve configurada y esta muerta. Patron ANUNCIADA del auditor,
el mismo del tercer recordatorio de carritos.
Cableado `--plantilla-notif` y `--plantilla-ns` (opcionales, los da Meta y son de CADA cuenta:
no se derivan ni se inventan). Sin ellos, el script **lo DECLARA** en vez de callarse. Pregunta
4b del intake.

VERIFICADO EJECUTANDO: con WhatsApp y sin plantilla se imprime el aviso rojo · con plantilla se
escribe `{"lang":"es","name":...,"namespace":...}` · los nombres salen 33/50 y 35/50 · las tres
pruebas siguen en verde (9/9, 10/10, 4/4).

LO QUE NO SE TOCO Y SE DECLARA: el mensaje de la notificacion difiere en estilo del de FER
("Tu asistente virtual ha procesado" contra "Chatea PRO proceso"), pero **las cinco variables
son identicas** y ninguna esta rota. No es defecto, es redaccion; se deja.
Y el `prompt_prompt` real de FER resulto ser una PLANTILLA MAESTRA con marcadores ([CATEGORIA],
[P1], [P2], [P3], objeciones), no un guion cerrado: **ahi vive la identidad de la tienda** (el
nombre de la asesora, la marca, la web, las transportadoras). Es el campo de 12.000 y es el
sitio correcto. Esta skill lo recibe hecho de `golden-chatea-pro-prompt-ventas`; la frontera se
mantiene.

## skill v4.9 · 2026-09-08 · EL INTAKE, ANCLADO AL CAMPO

🔴 NOTA DE 2026-09-18: esta acta es HISTORICA y dos de sus afirmaciones ya no son ciertas: el intake dejo de ser 'cuatro preguntas' (hoy son siete datos, ver SKILL.md) y las restricciones ya NO son 'ni una linea depende del negocio' (la regla de pago se deriva del modelo).

skill v4.9 — 2026-09-08 — EL INTAKE, DICHO POR FER Y ANCLADO AL CAMPO.
FER, revisando pregunta por pregunta: *"todo lo que pregunte, por favor, en el campo"*. El intake
anterior mezclaba preguntas de PRODUCTO (que trae la caja, variantes, objeciones, upsell) con las
del ASISTENTE. Ninguna de esas cae en `[Ventas Wp] Configuracion general` ni en `general 2`: son
de `golden-chatea-pro-prompt-ventas`. Fuera.

QUEDAN CUATRO, y cada una tiene su llave:
 1 PAIS donde opera la tienda        -> conexion_con_dropi.pais
 2 TIENE TIENDA si/no + URL          -> analizar_palabra.prompt, y se LEE para el prompt maestro
 3 SUBE SOLO A DROPI si/no           -> validaciones_orden.subida_automatica
 4 WHATSAPP DE AVISOS (OPCIONAL)     -> notificaciones.notificacion_1.whatsapp

LO QUE DEJA DE PREGUNTARSE, con su motivo:
· FLETE MAXIMO. FER: *"eso ya lo debes saber, esta en el prompt del pais"*. Se DERIVA del pais,
  igual que la moneda. Mapa nuevo `flete_max_por_pais` en limites.json, **Colombia 25.000**.
  🔴 Los otros 9 paises NO estan medidos y NO se inventan: si el pais no esta en el mapa, el
  script EXIGE --flete-max y dice cual falta. Copiar el de Colombia seria heredar un dato entre
  paises, que es justo lo que esta casa persigue. Probado en las dos ramas.
· Todo lo de producto. No es de esta skill.

DOS CAMBIOS DE COMPORTAMIENTO, no de texto:
· **--whatsapp-notif pasa a OPCIONAL.** FER: *"eso es una notificacion, es si quiere; pero seria
  bueno tenerlo"*. Sin numero NO se deja el hueco: se APAGA la notificacion (activa='no') y se
  informa. Un aviso activo apuntando a un numero vacio se ve configurado y no le llega a nadie.
· **Recomendacion de FER para la 3**, que la skill le da al cliente: si apenas esta iniciando,
  subida automatica en NO y los pedidos se pasan a mano hasta tomar confianza.

MEDIDO Y NO SUPUESTO: las restricciones se leyeron enteras y son 100% doctrina — no negociar
precio, no prometer curaciones, no decir que eres bot, el barrio no es la ciudad. **Ni una linea
depende del negocio**, asi que no generan ninguna pregunta.

VERIFICADO EJECUTANDO: Colombia sin --flete-max deriva 25000 y escribe 25000 en el JSON · Mexico
sin --flete-max se detiene y nombra el pais que falta · sin --whatsapp-notif el JSON sale con
whatsapp='' y activa='no' · autoprueba_d1 9/9 · autoprueba_push 10/10 · verificar_pais 4/4.

LO QUE NO SE PUDO HACER Y SE DECLARA: FER pidio tambien preguntar el **numero de servicio al
cliente**. En este asistente NO HAY CAMPO donde ponerlo: el unico numero de `[Ventas Wp]` es el
de notificaciones. El de contacto vive en COMENTARIOS (`informacion_del_negocio.contacto`).
Preguntarlo aqui seria pedir un dato sin destino, contra su propia ley.

## skill v4.8 · 2026-09-06 · RETIRADA LA PUERTA DE PAIS

skill v4.8 · 2026-09-06 · auditoria golden-skill-auditor (AUDITA+ARREGLA, orden de FER): RETIRADA LA PUERTA DE PAIS, que estaba viva y ejecutable en build_config.py:227 y rechazaba El Salvador y Bolivia por escrito. Nuevo guardarrail scripts/verificar_pais_no_es_puerta.sh (4 de 4, con contraprueba). Historial completo en references/changelog.md.

## skill v4.7 · 2026-09-06 (auditoría golden-skill-auditor, 925→945)

skill v4.7 · 2026-09-06 (auditoría golden-skill-auditor, 925→945) · DOS hallazgos reales con evidencia, sin relleno. (1) 🟡 Robustez: SKILL.md no tenía la línea de versión/changelog en comentario HTML bajo el H1 (patrón de la casa, estándar 7) — `inventario.sh` lo marcó explícito: "Sin línea de versión/changelog bajo el H1". Corregido: se agregó `<!-- skill v4.7 · ... -->` justo bajo el H1. (2) 🟡 Estructura/Recursos: `scripts/__pycache__/build_config.cpython-314.pyc` viajaba en el árbol de la skill como huérfano — bytecode compilado sin razón de estar versionado junto al código fuente, señalado por `inventario.sh` como "existe pero nadie lo menciona". Eliminado el directorio completo; no afecta ejecución (Python lo regenera localmente si hace falta y nunca se leyó desde ahí). Verificado tras el cambio: `validar_arsenal.py` sigue en 0 (compuerta dura sana), `autoprueba_d1.py` 9/9, `autoprueba_push.py` 10/10, `build_config.py` y `valida_producto.py` corridos contra casos buenos y malos (país inválido, sin prompt maestro, sin Dropi, D1 roto) con el comportamiento documentado. PENDIENTE CON DUEÑO (no cambia con esta reparación): la prueba de `push_config.py` contra la API REAL de Chatea Pro en un workspace desechable — techo declarado 985/1000 hasta que FER la habilite; hoy el banco solo SIMULA la API.

# Changelog · actas de sello de golden-chatea-pro-config-ventas-wp

Aqui viven las 19 actas de version que antes iban como comentarios HTML dentro de SKILL.md.
Se mudaron el 2026-09-05 por peso: 12.660 caracteres (33% del archivo, ~3.100 tokens) que se
pagaban en cada activacion de la skill sin aportar nada a la ejecucion. **Nada se borro: se mudo.**
El texto de cada acta esta copiado VERBATIM del propio archivo, con UNA excepcion declarada: el 2026-09-05 se sustituyo el NOMBRE DEL CLIENTE del incidente D1 por su descriptor operativo ("incidente de campo del 2026-08-23 en un espacio VIP"), porque este arbol se publica en un repo publico. La leccion queda entera; la identidad no viaja.

Las REGLAS VIVAS que solo existian dentro de estas actas (compuerta `agentskills validate`, tope
de 1024 de la description con `validar_arsenal.py`, Estandar 9 de reporte al Centro de Mando, y
el porque de `division.limite` = 2) NO se mudaron a ciegas: subieron al cuerpo de SKILL.md,
seccion "## Compuertas de esta skill". Un acta es historia; una regla es procedimiento vivo.

Orden: de lo mas nuevo a lo mas viejo, tal como estaban en el archivo.

## CENTRO DE MANDO · 2026-09-03

CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 979 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo.

## skill v4.6 · 2026-09-05 (bucle de autocalificacion, mandato v2)

skill v4.6 · 2026-09-05 (bucle de autocalificacion, mandato v2) · ALFOMBRA PROPIA ELIMINADA: en el banco autoprueba_push.py que yo mismo escribi en v4.5, la asercion de la llave `data` era `... or True` — NO PODIA FALLAR NUNCA. Una prueba que siempre pasa no es prueba, es decoracion, y ademas inflaba el conteo (9 de 9 incluia una falsa). Ahora el servidor simulado RECUERDA las llaves de nivel superior del PUT y se afirma que sean exactamente ["data"]: si push_config volviera a mandar `bot_fields` (el bug que da 400 en la API real) la prueba FALLA. Sumada una CONTRAPRUEBA que demuestra que el banco muerde: un PUT con `bot_fields` debe ser rechazado con 400. 10 de 10 en verde. Compuerta oficial: `agentskills validate <RUTA ABSOLUTA>` -> "Valid skill" (con "." da falso fallo, confirmado).

## skill v4.5 · 2026-09-05 (auditoría golden-skill-auditor, 910→)

skill v4.5 · 2026-09-05 (auditoría golden-skill-auditor, 910→) · DOS cosas. (1) 🔴 CONTRADICCIÓN VIVA: la description ya decía "10 países" (corrección CdM del 29-ago) pero assets/limites.json seguía con 7 y build_config RECHAZABA guatemala, argentina y brasil — la skill prometía 10 y entregaba 7. Probado antes: los 3 salían "Pais no valido". Corregido en los TRES soportes (limites.json, references/paises.md, cuerpo de SKILL.md) y probado después: 10 de 10 aceptados, bolivia/costarica/venezuela rechazados. Además queda DECLARADO el hueco: Argentina y Brasil los acepta la plataforma pero la hermana de direcciones aún no tiene pack — sus datos geográficos se le preguntan al negocio, y Brasil va en portugués. (2) 🟢 CERRADA LA RESERVA MÁS VIEJA: push_config.py llevaba meses "confirmado solo por lectura de código" porque probarlo exigía escribir en una cuenta viva. Nuevo scripts/autoprueba_push.py levanta un servidor local que IMITA la API de Chatea y ejerce sus 4 promesas contra casos que se saben malos (llave `data`, dry-run que no escribe, relectura, y la TRUNCADA SILENCIOSA que responde 200 ok y guarda cortado). 9 de 9 en verde; el banco mordió en su primera corrida (una aserción propia buscaba "integro" sin tilde). LÍMITE DECLARADO: simula la API, no la prueba en vivo — un cambio de contrato del servidor real seguiría sin verse; para eso hace falta un workspace de control desechable.

## corrección CdM 2026-08-29

corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto.

## skill v4.4 · 2026-08-23 (auditoría golden-skill-auditor, PLATA→reparada)

skill v4.4 · 2026-08-23 (auditoría golden-skill-auditor, PLATA→reparada) · TRES fallas cazadas por EJECUCIÓN, no por lectura: (1) 🔴 D1 NO era byte a byte — valida_producto comparaba las palabras clave con .strip(","), así que producto "TOPPIK,,,,,," y registro ",TOPPIK,,,,," (misma palabra en OTRO slot, bytes distintos) pasaban como ✅ Válido; justo la clase que la adenda D1 declaró crítica tras ese incidente de campo. Ahora comparación exacta, con repr de ambos lados en el error, y línea "D1 OK" cuando coincide. (2) 🔴 build_config ESCRIBÍA los 2 BOTFIELD aunque un tope DURO se excediera (solo salía exit 1): quedaba en disco un archivo con pinta de pegable que, pegado, se guarda CORTADO y mata al bot en silencio — el fallo que esta skill existe para evitar. Ahora compuerta gemela de la de huecos: si un tope duro falla, NO se escribe nada. (3) 🟡 tres tracebacks de Python crudos (--prompt-maestro inexistente, --in inexistente, JSON corrupto) → errores legibles; el gemelo makedirs ya se había arreglado en v4.1.3 y estos quedaron. Además: aviso explícito cuando se corre el validador SIN --registro (sin él no hay chequeo D1) y D1 sumado al checklist de Terminado.

## skill v4.3 · 2026-08-23 (Estándar 9, golden-skill-auditor)

skill v4.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR.

## skill v4.2 · 2026-08-21 (auditoría golden-skill-auditor, PLATA→verificar)

skill v4.2 · 2026-08-21 (auditoría golden-skill-auditor, PLATA→verificar) · DOS CONTRADICCIONES reales cazadas por ejecución (no por lectura): (1) SKILL.md Intake #6 decía "(Opcional)" el prompt maestro, pero build_config.py YA fallaba con exit 1 sin él desde v4.1.4 — el docstring se corrigió entonces pero el cuerpo de SKILL.md quedó desincronizado; ahora dice EXIGE y por qué. (2) build_config.py tenía --flete-max con required=True SIEMPRE, contradiciendo el caso borde documentado "Negocio sin Dropi... el flete no se pregunta" — probado en vivo: --dropi no sin --flete-max tiraba error de argparse (exit 2). Ahora --flete-max solo es obligatorio si --dropi si (el default); sin Dropi se omite y el JSON queda con "0". Probado: dropi=si sin flete-max → exit claro pidiendo el dato; dropi=no sin flete-max → exit 0, JSON con flete_minimo="0".

## skill v4.1.4 · 2026-08-08 (centro de mando, spot-check final)

skill v4.1.4 · 2026-08-08 (centro de mando, spot-check final) · docstring de scripts/build_config.py: --prompt-maestro re-etiquetado de '(opcional)' a OBLIGATORIO (el código lo volvió bloqueante en v4.1.3 y el docstring quedó sin corregir — la lección 'todos los soportes' aplicada al soporte que la incumplía).

## skill v4.1.3 · 2026-08-08 (centro de mando, verificación final, bloqueante F2)

skill v4.1.3 · 2026-08-08 (centro de mando, verificación final, bloqueante F2) · scripts/build_config.py entregaba {{PROMPT_MAESTRO}} LITERAL con exit 0 cuando faltaba --prompt-maestro (solo un aviso ⚠️) — la clase exacta que v4.1.2 declaró cerrada, viva en el script que nadie miró. Ahora valida la SALIDA con el mismo validador de huecos que valida_producto (dobles {{[^{}]*}} + llaves simples fuera de la whitelist runtime) y ante cualquier hueco da exit 1 SIN escribir archivo, con mensaje que manda a generar el prompt maestro con golden-chatea-pro-prompt-ventas. También: --out-prefix con directorio inexistente da error legible (makedirs). Probado: sin --prompt-maestro exit 1 y cero archivos; con él exit 0 y los 2 BOTFIELD escritos.

## skill v4.1.2 · 2026-08-08 (centro de mando, hallazgo del golden-verificador en la auditoría de la hermana config-comentarios)

skill v4.1.2 · 2026-08-08 (centro de mando, hallazgo del golden-verificador en la auditoría de la hermana config-comentarios) · FIX PUNTUAL en scripts/valida_producto.py: el regex de placeholders \{\{[A-Z0-9_]+\}\} solo cazaba mayúsculas puras — {{Hueco}}, {{hueco}}, {{ X }}, {{HUECO-2}}, {{HUECO 3}} y los slots de llave SIMPLE sin llenar ({URL_TIENDA}, {ID_DROPI}...) viajaban LITERALES al bot del cliente. Ahora: dobles con \{\{[^{}]*\}\} (cualquier contenido) + llaves simples contra whitelist de las 5 runtime legítimas de Chatea (las de notificacion-venta-realizada.txt: nombre_cliente, nombre_producto, porcentaje_entrega, telefono_cliente, valor_venta) con error ante cualquier otra. Probado: 5 variantes dobles plantadas cazadas, slot simple colado cazado, producto lleno con {valor_venta} runtime sin falso positivo.

## skill v4.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre))

skill v4.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio).

## skill v4.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08)

skill v4.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat CHATEA DOLCE COL 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta.

## skill v4.0 · 2026-08-07

skill v4.0 · 2026-08-07 · BRIEFING de instalación (aprobado por FER, verificado en vivo contra dos workspaces reales). FIX MAYOR: los 2 TECHOS. (A) el bot field se mide ESCAPADO — len(json.dumps(valor)[1:-1]), cada tilde 6, cada emoji 12 — no en crudo; salida COMPACTA (separators). (B) topes NATIVOS del formulario extraídos del CÓDIGO de la app (rol/restr/analisis 2000, prompt_datos 4000, notif 400, prompt_libre 12000, mensaje_inicial/pregunta 1000, remarketing 1000, descripcion 500, token Dropi 1200). PAÍSES: solo 7 válidos (COLOMBIA/ECUADOR/CHILE/MEXICO/PANAMA/PERU/PARAGUAY), build_config los valida; references/paises.md con deltas (MX: CP requerido, sin oficina, "domicilio"=casa). Gotchas API: llave `data`, var_type+value al crear, listado PAGINA, trigger sin 4-bytes (validado, rompe el bot), releer siempre. Sección "no se hereda al clonar" (incl. nombres de producto/paquetería en los ganchos).

## skill v3.2 · 2026-07-12

skill v3.2 · 2026-07-12 · prompts del motor endurecidos tras test de campo (3 prioridades, memoria del pedido, única confirmación, URLs blindadas, sin 2 preguntas/mensaje); division.limite 3→2 (con 3 la IA responde en ráfagas robot; 2 cubre imagen-URL + texto)

## skill v3.1 · 2026-07-09

skill v3.1 · 2026-07-09 · PRODUCTOS también nativos: 1 Bot Field JSON por producto ([Producto Ventas Wp] N) + entrada en el índice "[Ventas Wp] Disparador de productos Extendido" (Long JSON); template-botfield-producto.json con esquema real (recordatorios=prompt-instrucción EVENTO/35 palabras, remarketing=rol por fase, keyW/idAd=7 slots por comas), valida_producto.py con cruce producto↔registro y copia _LIMPIO; interruptores Boolean del workspace documentados

## skill v3.0 · 2026-07-09

skill v3.0 · 2026-07-09 · FORMATO NATIVO descubierto y verificado: la config general vive en 2 Bot Fields JSON (<20000 c/u, carpeta del agente); templates con el esquema real (claves intocables), build_config.py emite los 2 campos copy-paste (estructura IDÉNTICA a producción); prompts del motor pulidos ≤ límites de la UI

## skill v2.1 · 2026-07-09

skill v2.1 · 2026-07-09 · auditoría golden-skill-auditor 838→990: sin ¿¡ en prompts horneados, limites.json fuente única, casos borde + checklist

## skill v2.0 · 2026-07-08

skill v2.0 · 2026-07-08 · reconstruida sobre el mapa levantado en vivo de la UI de Entrenar

## adenda 2026-08-23 (centro de mando, incidente de campo en espacio VIP

adenda 2026-08-23 (centro de mando, incidente de campo en un espacio VIP reportado por la cuenta PRO de Chatea): gotcha D1 horneado — la edición de texto que toca palabras_clave rompe el disparador byte a byte; excluir el subcampo o verificar D1 tras escribir.


## v4.8 · 2026-09-06 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

**El defecto principal: la puerta de país estaba VIVA Y EJECUTABLE.** No era una frase vieja en
la prosa; era `build_config.py:227`, un `sys.exit`. Medido antes de tocar nada:

    $ build_config.py --pais "el salvador" --moneda "USD" ...
    Pais 'el salvador' no valido. Chatea Pro SOLO acepta: COLOMBIA, ECUADOR, ...

El Salvador es literalmente el ejemplo que puso FER al dictar la regla. Bolivia, igual. La skill
no generaba nada y salía en error.

**Mandato de FER (2026-09-06):** *"Hoy son diez, mañana doce, pasado treinta. El país se pide
para saber cómo enfocarlo, cuál es la jerga, cuál es la validación de direcciones, pero no para
prohibir."*

**Por qué se retiró la puerta en vez de ampliar la lista.** Una lista de países dentro de una
skill es un dato que **caduca solo** — y esta ya caducó una vez: decía 7 cuando eran 10, y con eso
rechazó por escrito a Guatemala, Argentina y Brasil. Vigilar la cifra deja el trabajo abierto para
siempre y falla en silencio el día que nadie mire. **Retirar la puerta se lleva la clase entera.**

### Qué cambió

· `scripts/build_config.py:227` — el `sys.exit` pasa a ser un aviso por stderr que dice qué se
  investiga (jerga, transportadoras, forma de la dirección, moneda) y **sigue**.
· La moneda sin mapa ya no es un frenazo de país sino un **dato que falta**, con la instrucción
  exacta: se investiga el ISO-4217, no se le pregunta al negocio, y se añade a `limites.json`
  para que el siguiente no repita el trabajo.
· `scripts/verificar_pais_no_es_puerta.sh` **(nuevo)** — guardarraíl de DOCTRINA. No comprueba
  que la lista esté completa: comprueba **que no vuelva a ser una puerta**, ejerciendo con El
  Salvador, verificando que ningún `sys.exit` cuelgue de la pertenencia a la lista, que Colombia
  siga funcionando, y **con contraprueba que repone la puerta a propósito para ver morder al
  detector**. 4 de 4.
· `SKILL.md` — la puerta se anunciaba en **cuatro sitios más**: la `description`, la regla
  "1 workspace = 1 país (10 válidos)", el primer punto del checklist de terminado y la sección
  "Países (10 válidos)". Los cuatro reencuadrados: la lista dice **dónde ya no hay que
  investigar**, no a quién se puede configurar.
· `references/paises.md` — decía *"`build_config.py` rechaza cualquier otro"*. Era cierto y dejó
  de serlo con este cambio: **una referencia que miente sobre el código es peor que ninguna.**

### Un defecto que introduje y corregí en la misma corrida

Al reescribir la `description` la dejé en **1007/1024**: 17 de margen, cuando la regla de la casa
son 40-60. Un tope que se roza hoy se pasa mañana con dos palabras, y lo primero que se pierde al
truncar son los disparadores del final, que son los más nuevos. Recortada a **943/1024, margen 81**,
sin perder un solo disparador.

### Verificación

· `verificar_pais_no_es_puerta.sh` 4 de 4 · `autoprueba_d1.py` 9 de 9 · `autoprueba_push.py` 10 de 10
· Regresión medida: Colombia sigue generando los dos bot fields y **derivando la moneda sola**.
· El Salvador con `--moneda USD` genera los dos bot fields, exit 0.
· Validador oficial "Valid skill" · `validar_arsenal.py` sin fallo · compuerta de publicación
  CERO hallazgos sobre 19 ficheros.

### Reserva que sigue abierta, y no la cierra el código

`push_config.py` está verificado contra un simulador escrito por la misma mano que el código.
Un cambio de contrato del servidor real no se vería. Lo cierra una corrida contra un workspace
de control desechable, con credencial. Por eso el techo declarado sigue siendo **985**.

## 2026-09-07 · CUPO DE LA API: se lee, se avisa y se frena antes de gastarlo

**Pregunta de FER, y el desarrollador de Chatea tenía razón:** el API limita a **1.000 peticiones
por hora** y pasarse **bloquea una hora entera**. La respuesta trae el contador de las que quedan.

**MEDIDO contra la API viva** (una lectura real, no documentación):

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: 999

En inglés: **X-RateLimit-Limit** y **X-RateLimit-Remaining** — "las peticiones que quedan".

🔴 **Hasta hoy NINGUNA de las diez skills de la familia leía ese contador.** Se trabajaba a
ciegas: se arrancaba una operación cara sin saber si cabía, y el bloqueo aparecía **a mitad**, con
el inventario incompleto o la configuración escrita por la mitad.

**Coste medido de una auditoría completa: 137 peticiones** (espacio de referencia casi vacío: 61
bot fields, 6 agentes IA, 45 tareas IA; uno de cliente cuesta más). **Con 1.000/hora caben ~7.**

**Qué se cableó:**
· El contador se lee de **cada** respuesta — viaja gratis en la cabecera que ya llegó — y se
  **dice** al terminar, con cuántas operaciones más caben.
· **Comprobación previa** antes de una operación cara: cuesta 1 petición saberlo antes y cuesta
  una hora averiguarlo después.
· Ante un **429 no se reintenta**: reintentar sobre un bloqueo lo alarga. Se declara qué quedó a
  medias, porque ni el panel ni un inventario parcial lo delatan solos.
· Herramienta de casa nueva: **`golden-chatea-cupo [token] [--necesito N]`**, que responde en una
  sola petición si cabe lo que se va a hacer.

⚠️ **Límite declarado:** la respuesta **NO trae `x-ratelimit-reset`**. El servidor **no dice
cuándo** se repone el cupo. La ventana es de una hora; si es fija o deslizante **no está medido** y
no se afirma. Lo único seguro es el número que queda AHORA.
