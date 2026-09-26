# Historial de golden-chatea-pro-validacion-direcciones

<!-- skill v2.6 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): RETIRADAS DOS PUERTAS DE PAÍS en prosa ('avisa que Chatea Pro no lo acepta antes de generar nada'), en la skill a la que el logístico delega. La forma de la dirección pasa a INVESTIGARSE, no a preguntársele al negocio. Y sección nueva para RECIBIR el pack propuesto que el padre entrega: no existía, así que la investigación se hacía y se perdía. Historial en references/changelog.md. -->

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.


## v2.12 · 2026-09-22 · lo que encontró la SEGUNDA verificación adversarial, y una fila de otro chat

Tras cerrar la v2.11 con la sección "Sincronización multi-agente", una segunda ronda de
verificación adversarial (pedida por el propio mandato: "si no es mil, vuelve y se automejora")
encontró que el cierre anterior tenía fallos reales, algunos irónicos: corregí una clase de
defecto en un sitio y la dejé viva 25 líneas más abajo. Y en paralelo llegó una FILA de otro chat
(proyectos-69, "📍 PROMPT VALIDACIONES PAISES", que FER decidió consolidar en este el mismo día)
con un hallazgo real sobre `chile.md`. Las dos cosas se cerraron en la misma ronda.

### La fila de proyectos-69: chile.md en molde compacto viejo

`chile.md` era el único de los 23 packs en la estructura de la v2.3 (encabezado "CONTEXTO
OPERATIVO" en vez de "VALIDACIÓN DE DIRECCIONES ·"), 4.376 caracteres frente al rango 6.176-7.847
del resto, sin la cláusula de "dirección acumulada" ni la referencia GPS que los otros 22 sí
tienen, y sin sección de ambigüedades frecuentes. Verificado de forma independiente antes de
tocar nada: los cuatro datos de la fila (tamaño, ausencia de "acumulada", ausencia de GPS,
encabezado distinto) se confirmaron exactos. Reconstruido sobre la estructura canónica de
`colombia.md`, usando el contenido chileno real (comuna como dato rey, "la altura" = número,
paradero de micro, población/villa/block/depto, rural con parcela/fundo/sector/camino) que la
fila aportó desde `VALIDACION-DIRECCIONES/_historico/02-CHILE-v100.md` — pero **sin heredar sus
transportadoras nominales** (Blue Express/Veloces/Starken/Wiilog): la doctrina de `[PENDIENTE]`
se mantuvo, tal como la propia fila pedía respetar.

La misma fila entregó `VALIDACION-DIRECCIONES/transportadoras-golden.json`: los couriers reales
de Golden por país (12 medidos contra el panel Dropi de FER, España sin medir), con la lección
medida de que ningún courier "lógico" acertó nunca (Panamá no era Veloces sino Servientrega+HL
Express; Perú no era Olva/Shalom sino Urbano+Fenix; Argentina no era Andreani/OCA sino
Fixy+Urbano). **No se incorporó a ningún pack**: es la fuente que se le pasa a esta skill al
generar un prompt PARA GOLDEN específicamente, nunca un default del país — exactamente lo que la
doctrina de esta skill ya exige.

### Lo que encontró la verificación adversarial sobre el cierre v2.11

**F1 — declaré "sincronizado" antes de que ocurriera.** El launchd que publica (`com.golden.skills-sync`,
cada 15 min) aún no había corrido cuando escribí "v2.11 — sincronizada, git log confirma push del
mismo día". La tabla ahora dice que hay que medir el HEAD en el momento, no de memoria, y que
"lo subí" y "está publicado" pueden estar hasta 15 minutos separados.

**F2 — había CINCO copias, no cuatro.** `SKILLS-COMUNIDAD/golden-chatea-pro-validacion-direcciones`
—v2.4, 8 packs, sin `scripts/`, con una carpeta `references 2` (firma de duplicado de iCloud sin
resolver)— no estaba en la tabla. Añadida como fila, sin tocarla: no tiene dueño claro.

**F3 — la reescritura de rutas del espejo Codex apunta a un directorio que no existe.**
`~/.agents/skills/.../SKILL.md` reescribe sus propios comandos a `~/.Codex/skills/…`, pero ese
directorio no existe (`~/.Codex/skills/` solo tiene `.system`): los 6 comandos ejecutables que
trae el espejo fallan si Codex los corre tal cual. Además el diff con la canónica no era "solo
cosmético" como yo había escrito: `changelog.md` difiere en 40 líneas (las dos actas que el
espejo nunca recibió). Corregido el texto para no declarar logrado lo que solo estaba declarado.

**F4 — la misma clase de "número quemado" que corregí en §Operación (v2.10) seguía viva en
§Herramientas.** Decía "cuatro casos… cazó 5 de 5"; el script real tiene 9 casos + 1 control =
10 de 10. Corregido, y con nota explícita de la ironía.

**F5 — enumeración de países-sin-CP quemada de la era de 8 packs.** Decía "Colombia, Chile,
Ecuador, Panamá, Perú y Paraguay" (6); son 9 — faltaban Guatemala, Venezuela y Costa Rica. La
misma clase que ya se había corregido una vez y volvió a quedar vieja tras la expansión a 23.
Corregida y remitida a `limites.json` como dato vivo en vez de volver a quemar el número.

**F6 — el detector de higiene no cazaba un teléfono local sin `+` ni una frase de negocio en
prosa libre.** Inyectado "Transportadoras habilitadas de este negocio: …, PROHIBIDA: …, Teléfono
de la bodega: 3105551234" en una copia de `colombia.md`: pasaba con exit 0, y el barrido de
publicación también daba cero (ese barrido cubre credenciales y dominios, no esta clase — no se
tocó, no tiene fábrica declarada, se reportó al Centro de Mando). Añadido un patrón de teléfono
local (10 dígitos, sin `+`, acotado para no comerse un CEP o un CP con guion) y dos patrones de
frase de negocio. Ahora **falla**, no solo avisa.

**F7 — el criterio de código postal se defendía con "opcional"/"omitirlo" sin ser cazado.**
Inyectado "El código postal es OPCIONAL en España… puedes omitirlo" en una copia de `espana.md`,
que YA tenía su frase correcta de "REQUERIDO": seguía dando "sano". La causa era doble: (a) faltaban
esas formas en `NIEGA`, y (b) la lógica de decisión tenía una "mutua exclusión" — si el pack tenía
AMBAS señales (la genuina y la inyectada), ninguna disparaba el fallo porque se cancelaban entre
sí. Corregido: ahora CUALQUIER señal en la dirección equivocada es fallo por sí sola, tenga o no
compañía. Ese cambio rompió 13 de 23 packs reales con un falso positivo nuevo: la frase compartida
"NO pidas de más: si ya trae … y el código postal, es válida" (presente en los 23 packs, sobre no
repetir un dato ya dado) quedaba en la misma oración que el token del CP y disparaba "no pidas"
como si negara el requisito. Se cambió la ventana de caracteres fijos a **oración/viñeta completa**
(no cruza a la viñeta siguiente) y se añadió una excepción quirúrgica solo para el modismo
"no pidas de más" (no para la palabra "no pidas" en general, que Costa Rica sí usa como negación
real). Verificado: los 23 packs reales vuelven a dar 0 fallos, y las dos mutaciones (F6 y F7)
siguen cazadas. **Declarado sin cerrar del todo**: esto sigue siendo vocabulario cerrado por
palabras clave, no comprensión semántica — un parafraseo que nadie anticipó puede seguir colándose.

**F8 — el banco de casos cubría 16 de 23 países.** Siete (Croacia, Ecuador, Eslovaquia,
Guatemala, Panamá, Paraguay, Perú) no tenían ni un caso, así que nunca podían bajar del 100%.
Añadido un caso real por cada uno, con marca tomada literal del cuerpo entregable del pack
(verificada contra el archivo antes de escribirla, no inventada). Cobertura ahora: 33 de 33
casos, 23 de 23 países con al menos uno.

### Estado al cerrar

23 de 23 packs · **18 sanos, 5 con aviso de margen, 0 fallos** · autoprueba **10 de 10** · banco
**33 de 33**, 23 de 23 países cubiertos · doctrina de país 8 comprobaciones · barrido de
publicación cero, probado · `agentskills validate` exit 0 · description 977/1024 · chile.md
reconstruido sobre el molde canónico, transportadoras siguen en `[PENDIENTE]`.

**Sigue sin cerrar, declarado y no tapado:** el tope de 8.000 sigue sin medición propia contra el
panel vivo; el criterio de CP por palabra clave (F7) puede evadirse con un parafraseo nuevo; los
packs europeos no llegan a tres fuentes por país; nadie ha probado un pack contra el modelo real
en WhatsApp; el espejo Codex tiene comandos con ruta muerta y no es mío arreglarlo; la copia
`SKILLS-COMUNIDAD` (5ª fila) no tiene dueño claro.


## v2.11 · 2026-09-20 · citas completas, no tokens sueltos

Auditoría `golden-skill-auditor`, corrida automática. `inventario.sh` marcaba **DUDOSOS** los 23
nombres de pack citados en la tabla del paso 2 (`colombia.md`, `espana.md`…): estaban cubiertos
solo por el token desnudo `references/` de la frase anterior a la tabla, no por una cita con el
segmento canónico completo. El inventario no podía confirmar que cada nombre apuntara de verdad a
`references/<pais>.md`.

**Corregido:** se antepuso `references/` a los 23 nombres de la tabla (América y Europa). Cero
cambio de contenido o de doctrina — solo la forma de la cita. Reverificado en vivo: DUDOSOS bajó
de 23 a 0.

Este acta se escribe el 2026-09-22, dos días después del cambio: la edición original solo dejó un
comentario HTML de una línea en el cuerpo del SKILL.md, sin mudar el detalle aquí. Es el mismo
defecto que esta skill lleva corrigiendo desde la v2.9 en OTROS sitios (números quemados, criterios
en prosa): una convención que el propio changelog declara ("el cuerpo se paga en cada activación, el
acta no") se incumplió consigo misma durante dos versiones. Corregido con este acta y con el
recorte del comentario en el cuerpo a un puntero de una línea.

## v2.10 · 2026-09-13 · el número quemado sobrevivió a su propia corrección

Auditoría `golden-skill-auditor` (AUDITA+ARREGLA). La sección **"Operación de esta skill"** del
SKILL.md seguía escribiendo, en prosa, `"6 de 6"` y `"los 8 packs prometidos existen"` — la salida
literal que el guardarraíl `verificar_pais_no_es_puerta.sh` daba ANTES de que la v2.9 le corrigiera
la lista quemada de 8 países por una lectura en vivo de `limites.json` (ver v2.9 más abajo: *"el
guardarraíl decía los 8 packs prometidos existen… ahora la lee de limites.json"*).

**La clase de defecto es exacta y se repitió en el lugar exacto donde no se la buscó:** el número
se corrigió DENTRO del script, pero la PROSA que describe al script —en el propio SKILL.md, para
uso humano— seguía citando la salida vieja. Corregir el instrumento no corrige el texto que habla
del instrumento; son dos superficies distintas y hay que revisarlas las dos.

**Corregido tras correr el guardarraíl en vivo** (8 comprobaciones OK, 23 packs confirmados): la
prosa pasa a decir `"8 de 8"` y `"23 packs (número leído en vivo, no quemado)"`. Sin otros hallazgos
en esa corrida.

Este acta se escribe el 2026-09-22, el mismo día que la de v2.11, por el motivo de arriba: ninguna
de las dos ediciones automáticas mudó su detalle al changelog en su momento.


## v2.7 · 2026-09-08 · el tope de 8.000 del campo destino

EL CAMPO DONDE ATERRIZA ESTE PROMPT TIENE TOPE Y LA SKILL NO LO SABIA.
Del video del panel logistico que grabo FER: `Prompt de analisis de direccion` corta en 8.000 y
el espacio de referencia marcaba 7.833/8.000 -- 167 de margen. Esta skill no mencionaba NINGUN
tope, ni ese ni el del bot field, y un prompt de direcciones bien hecho ya ronda esa cifra: la
proxima mejora que le anada un parrafo lo pasa, y pasarse NO da error (se guarda cortado y el
panel se ve normal). El dano no es ruidoso: un prompt de validacion cortado valida peor y deja
pasar direcciones malas, que es justo lo que esta skill existe para evitar. Se anade la medicion
antes de entregar y la regla de que se recorta CONTENIDO, nunca el contrato de salida. Y se deja
dicho que este 8.000 es la ultima medida y no una garantia: el "no hay tope" del logistico fue
verdad en agosto y falso en septiembre.


## v2.9 · 2026-09-08 · lo que encontró el verificador adversarial

La v2.8 se cerró con "23 de 23 packs, 0 fallos, autoprueba 5 de 5". El verificador
adversarial —que solo vio el estado final y el estándar— **desmontó tres de esas
comprobaciones con mutaciones**, y encontró datos de negocio que la ronda anterior no
había mirado. Esto es lo que estaba mal y cómo quedó.

### El fallo de método que lo explica casi todo

Fabriqué 15 packs y los verifiqué uno por uno. **Los 8 que ya existían no los audité**:
asumí que estaban bien porque el barrido de publicación daba cero. Eso es revisar "lo
importante" en vez de revisar todo, que es justo lo que el protocolo prohíbe. Los dos
defectos más graves estaban en esos 8.

### Lo grave: datos de un negocio real en un repo público

- `mexico.md` traía **cinco paqueterías nominales** como "las únicas" y un "México es 100%
  entrega a domicilio", en primera persona. `guatemala.md` traía **dos mensajerías y un veto
  nominal a otras cuatro**. Eran los **únicos 2 packs de 23 sin `[PENDIENTE]`**.
- `chile.md` tenía una sección entera titulada con el nombre de una transportadora, mientras
  su propio bloque de transportadoras decía `[PENDIENTE]`: **la excepción se había aplicado a
  medias dentro del mismo archivo**.
- `ecuador.md` y el `SKILL.md` nombraban el veto de una operación concreta **dentro del cuerpo
  que se pega en el bot de otro cliente**. Eso es la marca viajando en prosa libre.
- Clase: **una excepción que se arregla en un pack y nadie propaga a sus hermanos.** El arreglo
  que Colombia recibió en la v2.4 (mover la lista a `[PENDIENTE]`) no llegó a México ni a
  Guatemala, y llegó a medias a Chile.
- Estado: **0 nombres de transportadora en todo el árbol fuera del changelog**, medido.

### Tres comprobaciones que NO PODÍAN FALLAR

1. **La señal se buscaba con `in`.** `"dirección correcta" in "✅ dirección correcta"` es
   verdadero, así que México pasaba con la señal de máquina contaminada por un emoji. Ahora se
   comprueba que no haya emoji pictográfico pegado — y solo pictográfico: contar la flecha `→`
   de "llegar sin llamar → dirección correcta" produjo 23 falsos positivos de 23 antes de
   afinarlo.
2. **El criterio de CP se apoyaba en frases quemadas**, y una entrada era `"pidelo"`: tan laxa
   que Brasil pasaba por ella y no por su frase real. Una negación parafraseada ("No lo
   solicites nunca") no la cazaba nadie. Ahora se decide por **proximidad al token del código
   postal**, no por lista de frases. Dos afinados que costaron: mirar la frase entera daba 11
   falsos positivos (porque "NO pidas de más… y el código postal" cabe en una sola frase), y
   `"no hace falta"` contiene `"hace falta"`, que estaba en la lista de obligación — con dos
   `if` la ventana marcaba las dos cosas y se anulaban.
3. **El "control inverso" del banco de casos era una expresión constante** que no ejecutaba
   nada del banco. Ahora muta un pack real en memoria y vuelve a entrar por la misma función.

### El banco comprobaba vocabulario, no criterio

El verificador borró la regla real de Costa Rica y dejó una frase decorativa con las palabras
"una cuadra": el banco siguió diciendo 26 de 26. Las marcas eran **palabras sueltas**. Ahora son
**frases de la regla**, y el banco caza esa mutación exacta. Al endurecerlas apareció un falso
positivo propio: la marca de Chile estaba copiada de su nota HTML y no del cuerpo. **Las marcas
salen del cuerpo entregable, nunca de la nota.**

### La higiene no podía tumbar la corrida

`check_higiene` solo devolvía avisos, y su patrón `sk_[A-Za-z0-9]{8,}` no cazaba `sk_live_`,
`sk-proj-` ni `sk_test_`. Una clave metida a propósito en un pack pasaba la corrida con exit 0.
Ahora **falla**, y con los formatos reales. El cero del barrido de publicación tampoco cubría
esta clase: cubre credenciales y dominios, no nombres de transportadora contratada.

### El guardarraíl de doctrina se evadía con formato de cita

Bastaba escribir la orden precedida de `>` para que el script dijera "doctrina viva": el filtro
descartaba toda línea de cita con esa frase, y su contraprueba añadía el sabotaje al fichero
**ya filtrado**, así que jamás ejercitaba el filtro, que es donde estaba el agujero. Ahora una
cita solo se descarta si su contexto dice que la frase se **retiró**, la contraprueba entra por
la puerta principal y se corre **en dos formas**, llana y cita.

### Ruido que tapaba señal

Los 23 packs terminaban en "aviso" por el `[PENDIENTE]`, que es diseño. Un estado que siempre
sale amarillo deja de leerse. El hueco pasó a ser **columna informativa** y los avisos quedaron
en 5, todos de margen de techo real.

### Números corregidos

- La señal negativa tiene **17 formas**, no 2 como decía `limites.json`. Doce son traducciones
  legítimas; en español hay **6 variantes entre países hermanos** sin regla que lo explique.
  Es deriva de haberse copiado en momentos distintos: no rompe nada hoy, queda declarada y sin
  decidir.
- El guardarraíl decía "los 8 packs prometidos existen" con la lista quemada. Ahora la lee de
  `limites.json` y dice 23, con contraprueba de pack ausente.
- México se pasó a **8.009** por mis propias ediciones de esta ronda y el validador lo cazó.
  Recortado a 7.803.

### Estado al cerrar

23 de 23 packs · **18 sanos, 5 con aviso de margen, 0 fallos** · autoprueba **10 de 10** ·
banco **26 de 26**, probado con la mutación exacta que antes lo derribaba · doctrina de país
**8 comprobaciones**, contraprueba en dos formas · barrido de publicación cero, probado ·
`agentskills validate` exit 0 · description 977/1024.

**Sigue sin verificar** y está declarado en `limites.json`: el tope de 8.000 viene de un vídeo
del panel, no de una medición propia; qué señal negativa espera el flujo por texto; y que los
packs europeos **no llegan a tres fuentes por país ni los ha revisado un hablante nativo**.


## v2.8 · 2026-09-08 · EUROPA, y el criterio de país deja de vivir en la prosa

Encargo de FER a esta fábrica: *"la validación del asistente logístico de todos los países donde
se opere, Europa incluida. Los que no tengas, fabrícalos de una vez con el contexto de cómo habla
la gente, cuál es la jerga, cómo son las ubicaciones, cómo debe llegar."*

**Universo real, no el de la plataforma.** Quien limita dónde se opera es la LOGÍSTICA, no el bot:
WhatsApp no tiene fronteras. Dropi opera en 22 países (11 LatAm + 11 Europa) y Chatea ofrece
además Brasil. Universo = **23**. Había 8 packs. Se fabricaron **15**: Argentina, Brasil,
Venezuela, Costa Rica, España, Portugal, Rumanía, Polonia, Hungría, Eslovenia, Eslovaquia,
Croacia, Grecia, Bulgaria y Chequia.

### El defecto de clase que este trabajo cierra

El código postal se negaba en prosa ("NUNCA pides código postal"), heredado del pack de Colombia.
**En los 11 países de Europa y en Brasil el CP es OBLIGATORIO**, y en Argentina y México también.
Fabricar Europa clonando Colombia habría roto doce países de una sola vez — la misma trampa que
ya mordió con México, multiplicada. Por eso el criterio deja de ser prosa:

- `references/limites.json` — DATO DURO: por país, si el CP se pide y con qué formato, el dato rey
  de última milla, el idioma y el contrato de salida. Formatos verificados contra la tabla de
  códigos postales de Wikipedia; Costa Rica además contra prensa y fuentes culturales.
- `scripts/validar_pack.py` — lo EJERCE. Un pack que niegue el CP donde es requerido **falla**.

### Lo que se midió (no lo que se supuso)

- **El tope de 8.000 se confirmó como el constraint de diseño.** Colombia va a 7.696 (304 de
  margen), México a 7.679, Guatemala a 7.507: los tres bajo el margen sano de 600. Los 11 packs
  europeos se fabricaron a 6.162–6.882 justamente para no nacer al borde.
- **El validador cazó un fallo en el trabajo de esta misma acta**: Costa Rica salió a 8.265,
  por encima del tope. Se habría guardado CORTADO y sin error — el daño exacto que esta skill
  existe para evitar. Recortado a 7.847.
- **`TOPES-NATIVOS-POR-CAMPO.md` (07-ago) está caducado** para el logístico: decía "no hay tope
  de caracteres en los campos de texto". La medición del panel del 08-sep lo desmiente. Un dato
  medido caduca.

### El molde de país no hispanohablante

Se probó primero escribiendo Brasil entero en portugués. **El validador dio un fallo falso**: el
pack sí exigía el CEP, pero los detectores de criterio están en español. La lección no es
parchear el detector para ocho idiomas, es al revés: **el prompt se escribe en español —lengua
en la que esta skill se mantiene y se audita— y solo la frase que ve el cliente va en el idioma
local.** Un prompt en polaco o en griego deja la skill inauditable: nadie de la casa puede
revisar su criterio. Brasil se rehízo con ese molde y los 11 europeos nacieron con él.

### 🔴 La señal positiva no se traduce

`dirección correcta` es señal de MÁQUINA, no un mensaje al cliente: el flujo del logístico la lee
para avanzar, y el prompt de producción trae una "CAPA 2 — COMPORTAMIENTO EN FLUJO" que actúa
sobre esa salida. Escrita `endereço correto` o `adres poprawny`, el flujo no la reconoce y **el
pedido se queda parado sin dar ningún error**. Los 12 packs no hispanohablantes lo dicen dentro,
y el validador lo comprueba.

### Divergencia declarada y NO resuelta

El JSON de producción de Golden usa como señal negativa `falta que proporcione [dato]`; el patrón
oro y sus derivados usan `Para completar su envío, nos regala…?`; la `description` de esta skill
trae la de producción. Las tres coinciden en la POSITIVA, que es la única verificablemente
crítica: el validador exige esa y acepta ambas negativas. **Cuál espera el flujo por texto no se
puede saber sin entrar a un espacio vivo.** Queda anotado en `limites.json`, no tapado.

### El banco de casos (fase 4: ejecutar, no suponer)

`references/casos.json` — 26 direcciones trampa reales, con la regla que cada una exige: el
"200 metros norte" tico sin punto de partida, el "300 metros" que son tres cuadras y no una
medida, la referencia al negocio que ya cerró, el orden inverso húngaro, la dirección búlgara
completa que no lleva calle, la quinta venezolana que se identifica por nombre y no por número,
el "PB" argentino que es piso y no dato faltante. `--casos` comprueba que la regla está escrita.
**Probado quitándole reglas a dos packs en copia: cazó las dos.** Y `--autoprueba` caza 5 de 5,
control inverso incluido.

### Estado al cerrar

23 de 23 packs revisados · 0 fallos · 22 con aviso (el `[PENDIENTE]` de transportadoras es por
diseño; 4 van bajo el margen de 600 y están anotados) · 26 de 26 casos con su regla escrita ·
`agentskills validate` exit 0 · description 977/1024.

Fábrica: este chat (antes el Centro de Mando). Se actualiza `REGISTRO-FABRICAS.md` y se informa
al CdM, que reparte.




## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- Fábrica: CENTRO DE MANDO (chat 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR) — sin fábrica de chat propia; turnos y filas van a la bandeja del CdM. -->

<!-- corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto. -->

<!-- skill v2.4 · 2026-08-26 (Centro de Mando, fila de un espacio VIP de Colombia) · DESHORNEADAS
LAS TRANSPORTADORAS DE NEGOCIOS REALES: colombia.md traía la operación logística completa de
Golden (7 transportadoras, veto a Servientrega) violando la propia ley de la skill ("nunca
hornees datos de un negocio real"); misma clase en chile.md (Starken/Blue Express) y ecuador.md
(Gintracom "preferida"). Los tres bloques pasan a hueco [PENDIENTE — confirmar con el negocio]
como ya hacían Panamá/Perú/Paraguay; la lista de Golden se movió a
PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/GOLDEN-TRANSPORTADORAS-COLOMBIA.md (solo espacios Golden).
El patrón oro de Colombia declara la excepción por diseño en su cabecera. Guatemala (histórico
fuera de plataforma) se conserva intacto, declarado. Ejemplos con marcas reales generalizados a
[Transportadora]. -->

<!-- skill v2.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando):
cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v2.2 · 2026-08-21 (auditoría golden-skill-auditor) · añadido paso 4 de VERIFICACIÓN/QA
del prompt antes de entregarlo (contrato de salida, transportadoras no inventadas, ningún
[PENDIENTE] suelto) y DEFINICIÓN DE "TERMINADO" explícita en el flujo (Proceso y flujo);
el intake del paso 3 ahora pide también qué hacer si el negocio no puede confirmar un dato en
el momento; aclarada la ruta del script de barrido como externa a esta skill con fallback manual
si no existe en el entorno (Robustez/portabilidad). Cero bugs de contenido encontrados en los 8
packs de país tras verificación cruzada línea por línea del contrato de salida (emojis, código
postal, transportadoras) — solo huecos de proceso, ya cerrados. -->

<!-- skill v2.1.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->

<!-- skill v2.1 · 2026-08-08 (centro de mando, chat CHATEA DOLCE COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → Dolce Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. -->

<!-- skill v2.0 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat configuración de un espacio de México) · REFORMA DE PAÍSES: la plataforma acepta 10 países (remedido 2026-08-29 contra el bundle vivo: se sumaron ARGENTINA, BRASIL y GUATEMALA). Revisión anti-clon país por país: México decía "NUNCA exijas código postal" — criterio de Colombia clonado y FALSO (en México el CP es REQUERIDO, define la zona de reparto); corregido en todo el pack. Chile y Ecuador revisados: su "sin CP" es criterio local válido (comuna/distrito e intersección mandan), anotado en cada pack; precisado lo de "Santiago no es comuna" en Chile (sí existe la comuna Santiago Centro, pero a secas es ambiguo). La regla global "nunca pide código postal" del contrato de salida se volvió por-país. -->

<!-- v1.x · sin sello previo (5 packs: Colombia, Guatemala, Chile, México, Ecuador) -->
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 954 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

## v2.6 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

Esta skill **no tiene código: su comportamiento ES su texto.** Por eso una frase mal puesta aquí
vale lo mismo que un `sys.exit` en una hermana — y había dos.

### 1 · 🔴 DOS PUERTAS DE PAÍS, en la skill a la que el logístico DELEGA

· En la regla de arriba: *"Si piden un país fuera de esos 10, **avisa que Chatea Pro no lo acepta
  antes de generar nada**"*.
· En §País nuevo: *"Si piden un país que la plataforma NO acepta (Bolivia, Costa Rica…),
  **primero avisa que Chatea Pro no lo acepta**"*.

El padre `config-logistico` retiró su puerta el 06-sep y **delega aquí el prompt de validación**.
Con estas dos frases, la puerta seguía cerrada un piso más abajo: el padre decía "adelante" y la
hija rechazaba. Retiradas. La lista de 8 packs pasa a decir **dónde ya no hay que investigar**,
no a quién se le genera.

### 2 · 🔴 "preguntando los datos operativos al negocio"

Así estaba escrito el flujo de país nuevo, y así lo repetía la `description`. Contra la ley de FER
del 06-sep: *"La jerga y la configuración de las direcciones no se le pregunta a la gente, porque
precisamente para eso es la skill."* Reescrito: se **INVESTIGA** con tres fuentes independientes
—servicio postal, webs de las transportadoras, sitios donde gente real escribe direcciones— y se
**pregunta solo** lo que vive en la cabeza del dueño: qué transportadoras tiene contratadas.

### 3 · 🔴 El padre le entregaba un pack investigado y ella no tenía dónde recibirlo

`config-logistico` dice, desde ayer: *"se propone, no se escribe solo: quien adopta un pack es la
skill dueña"*. La dueña es esta, **y no tenía sección para adoptarlo**. La investigación se hacía y
se perdía, y el siguiente negocio del mismo país obligaba a repetirla entera. Sección nueva
**"Recibir un PACK PROPUESTO"**, con los cuatro requisitos para adoptarlo: sus tres fuentes, lo NO
VERIFICADO marcado, el criterio del código postal decidido por ese país (nunca heredado — la
trampa que ya mordió con México) y cero datos de negocio dentro.

### 4 · Guardarraíl nuevo: `scripts/verificar_pais_no_es_puerta.sh` (6 de 6)

La skill no tenía ni un script. Este comprueba la doctrina **en dos sentidos**: que la afirmativa
esté escrita, y que **ninguna orden de rechazo** aparezca en texto vivo. Trae contraprueba que
repone la puerta a propósito para ver morder al detector, y comprueba que los 8 packs prometidos
existan de verdad.

### 🔴 Dos errores míos construyendo el guardarraíl, y los dos ya conocidos

1. **El filtro tiraba la línea de la doctrina.** Descartaba toda línea de cita con comillas — y la
   línea que DECLARA "el país es parámetro, no puerta" cita a FER, así que se iba con ella. El
   guardarraíl acusaba de "falta la doctrina" a un documento que la tenía escrita dos líneas antes.
   Ahora filtra por **contenido** (solo la cita de la frase retirada), no por forma.
2. **`grep` por bytes otra vez.** `PARAMETRO` no casa nunca con `PARÁMETRO` sin locale UTF-8. Se
   normaliza el texto una vez, en Python, y se busca sobre eso. Es la tercera vez hoy que esta
   trampa muerde en tres skills distintas.

### Reserva declarada

**El límite del guardarraíl está escrito dentro de él:** distinguir una orden de su cita se hace
por forma, así que un texto que ordene el rechazo **con otras palabras** no lo caza. Por eso el
bloque afirmativo pesa tanto como el negativo: si alguien reescribe la doctrina, ahí muerde.

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
