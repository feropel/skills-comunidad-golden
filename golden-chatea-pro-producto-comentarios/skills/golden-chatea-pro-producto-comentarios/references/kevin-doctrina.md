# La doctrina de Kevin Galeano, con cita y con sus huecos

**Fuente única:** clase M7 · Venta por Comentarios del MBA, 2026-09-02, 2:34:33 de grabación,
`https://youtu.be/2i9jgXdxH8g`. Habla el 94% de la clase (24.722 palabras medidas). Extraído y
medido por el chat 🎓 MBA con `buscar.py` y `dump_ponente.py` sobre la transcripción; el
documento completo vive en `PROYECTOS/MBA-YOUTUBE/DOCTRINA-KEVIN-GALEANO-COMENTARIOS.md`.

Crédito: **Kevin Galeano · @Kevin_steven96**.

> **Por qué este archivo separa lo citado de lo derivado.** Lo que el bot escriba sale de aquí y
> se lee en público. Una regla inventada y atribuida a Kevin es peor que no tener regla: nadie la
> cuestiona porque lleva su nombre. Por eso cada bloque dice si es **CITA** (con minuto), **HUECO**
> (no lo dijo) o **DERIVADO** (lectura de un principio suyo aplicada a otra cosa).

## 1 · El `rela` es un IDENTIFICADOR ÚNICO, no una lista descriptiva

Esta es su tesis y lo cambia todo. El criterio para aceptar una etiqueta **no** es "describe bien
el producto", es **"solo este producto puede reclamarla"**.

**CITA · 1:50:24**, montándolo en vivo: *"por qué no ponemos solamente magnesio? Chicos, en
nuestra tienda vendemos 3 tipos de magnesio. Si yo solo le pongo magnesio, el bot se me va a
enloquecer sin saber a cuál de los 3 responder."* Va el nombre distintivo completo:
`Magnesio Complex 8 en 1`.

**CITA · misma escena**, descartando una etiqueta que parecía buena: *"le voy a poner dormir… NO,
dormir no le puedo poner, porque tengo otro magnesio de 12 ingredientes que también sirve para
dormir."*

De ahí sale la regla operativa: **una etiqueta que un segundo producto del catálogo pueda
reclamar, no entra.** Y fíjate que el descarte no es por genérica —"dormir" describe muy bien el
producto— sino por **compartida**.

**CITA · 2:15:02**, y el ejemplo no es de suplementos: *"yo estoy montando una camisa GAP… y luego
mandan un anuncio de camisetas blancas, pero a todos le ponen camisa. Te va a mezclar los 2."* Su
salida no es afinar la etiqueta: es **diferenciar el NOMBRE COMERCIAL** (`Magnesio Complex 8 en 1`
contra `Magnesio 2 en 1`).

### Los genéricos, con su caso medido en contra

**CITA · 2:16:40:** *"no pongan disparadores genéricos como precio, información, porque la IA
queda loca y va a disparar cualquier producto… a veces yo le ponía 20 disparadores y eran tan
genéricos que me los confundía. Así diga precio en diferentes productos, 4 veces precio, ahí ya va
a comenzar a confundirse."*

**HUECO — no da un número óptimo de etiquetas.** Lo que da es el caso en contra: 20 genéricas le
rompieron el sistema. Los rangos que maneja esta skill (**15-30 disparadores**, mínimo 8) son
**criterio de la casa, no de Kevin**, y el tope de **10 del formulario es de la herramienta**, no
suyo. No se los atribuyas.

## 2 · 🔴 El `rela` NO se valida solo: se valida contra el COPY del anuncio

La regla más accionable de la clase, y él mismo la atribuye a otro — dice que se la dio *"el viejo
Miguel, de Chatea"*.

**CITA · 2:14:54:** *"trata siempre que dentro de ese copy diga el NOMBRE EXACTO CON EL MISMO
DISPARADOR que estás utilizando en Chatea Pro… me pasaba que la IA me generaba el copy pero me
decía magnesio, no Magnesio Complex 8 en 1, entonces a veces no lograba relacionarlo. Y desde que
lo corregí, dejó de fallarme."*

**Lo que significa para esta skill:** un `rela` puede estar perfecto y no disparar nunca, porque el
fallo está del otro lado. **Revisar el `rela` sin mirar el copy del anuncio es media revisión.**
Cuando audites un producto que "no reconoce comentarios", pide el copy que está corriendo y
comprueba que el disparador aparezca **literal** ahí dentro.

**Plan B cuando no relaciona (CITA):** responder el comentario a mano y arrancar el interno con
*"Hola, te interesa nuestro producto X"*; ahí el asistente toma el flujo.

### ⏳ Fecha de caducidad declarada por él mismo

**CITA · 2:15:02:** llama al `rela` *"un plan de contingencia"*, porque *"en la versión 3 se va a
hacer conexión con el POST ID del anuncio"*. **Si la v3 ya salió, todo este capítulo se remide
antes de usarlo.** El campo `[Comentarios] Versión` de la cuenta dice qué versión corre.

## 3 · El método del "ejemplo": cómo se supera el tope de 500

Él no pelea con el tope, lo rodea. Y lo hace en cámara.

**CITA · 1:43:20:** *"pero mire qué pasó: solamente tenemos 500 caracteres. Cómo vamos a vender
con tan poquitos caracteres, que ahí no nos alcanza para beneficios, ingredientes, objeciones?"*

**El método, paso a paso como lo ejecuta:**

1. Crear el producto **en el formulario**, con el nombre real y la descripción puesta
   literalmente como la palabra **"ejemplo"**. Guardar.
2. Ir a **Contenido → Campos del bot → el JSON "producto extendido"**, **RECARGAR**, y bajar al
   final: ahí está el último producto creado.
3. Reemplazar **solo el `desc`**, respetando la estructura JSON.
4. Volver al formulario y **recargar**.

**Resultado medido en cámara:** el contador pasó de 500 a **1.895** para ese producto. Y comparando
con su tienda de producción: *"vos tenés uno de 3.000"*.

**El cupo total, con su propia cuenta (CITA · 1:45:04):** *"hasta la última actualización solamente
nos dejaba crear máximo 4 o 5 productos y tocaba estar eliminando… Chatea nos amplió a 500.000
caracteres. Si esta base gasta 3.000, divido 500.000 en 3.000: nos deja crear 166 productos."*

### Las tres trampas del JSON, las tres falladas en vivo

- **La coma separa productos, pero el ÚLTIMO va SIN coma.** Le falló dos veces en cámara.
- **El corchete** *"abre todo el ecosistema y cierra el ecosistema"*: si se pierde, no hay lista.
- 🔴 **Editar sin recargar es editar contra un estado viejo.** **CITA · 2:11:27:** borró un
  producto en el formulario y seguía apareciendo en el JSON — *"por qué? Porque no le dio
  actualizar a la página."*

**HUECO:** el tope de **255 del nombre** no lo menciona nunca. Ese lo midió esta skill en el
contador del panel (ver `SKILL.md`), no viene de la clase.

## 4 · Criterios de corte de la ficha

**El semáforo de encaje · CITA · 1:55:42.** Cada uso posible del producto se clasifica:

| | Qué significa | Qué se hace |
|---|---|---|
| 🟢 verde | la promesa se cumple y se nota rápido | va al frente de la ficha |
| 🟡 amarillo | funciona, pero necesita uso continuado | va con su "con uso constante" |
| 🔴 rojo | no hay efecto directo | **no se menciona como promesa de valor** |

Su ejemplo textual: magnesio y colesterol alto es **rojo**, *"no tiene efecto directo sobre los
lípidos, el encaje real es hacia el calambre"*. Aplícalo antes de escribir los bullets de
**Lo que puedes esperar**: si un beneficio es rojo, no entra aunque suene bien.

**Mínimos de materia prima (CITA):** *"no nos va a poner 4 ni 3 beneficios, los va a poner 15 como
mínimo"* y *"mínimo 10 ángulos de venta"*, organizados por nivel de conciencia TOFU / MOFU / BOFU.
Eso es el material del que se eligen los 5 o 6 que caben en la ficha.

**Versionado (CITA):** un documento con versión 1, 2 (editada por quien sea), y si la 4 falló se
anota *"esta versión no funcionó"* y se vuelve a la 3.

**🔴 HUECO Y CORRECCIÓN DE ATRIBUCIÓN: la "regla de la abuela" NO es del MBA.** La frase *"si tu
abuela no entiende el beneficio en 5 segundos, está mal escrito"* circulaba en la casa atribuida a
Kevin. Se buscó "abuela" y "abuelita" en **las 16 grabaciones**: aparece dos veces y **ninguna es
Kevin Galeano ni habla de escribir fichas**. No se la atribuyas. Como criterio de brevedad sigue
siendo útil, pero es de la casa.

## 5 · El bloque "Confianza en {PAÍS} — Más de {NÚMERO} clientes"

**HUECO, y este importa.** **CITA · 2:09:48**, repasando qué edita el alumno: *"en qué país vamos a
venderlo, Guatemala o Colombia? Sí, más de tantos clientes… clientes en países como Guatemala,
Colombia. Precios de un frasco, de 2 frascos, de 3 frascos. Tienda oficial, pues el nombre de la
tienda."*

Va en la misma lista que país, precios y URL: **es un campo que el alumno rellena, y en toda la
clase nadie dice que el número tenga que ser verificable.** O sea: **la clase no respalda ese
número, es relleno de plantilla.**

**Qué hace esta skill con eso:** o va la cifra real del negocio, o el bloque no va. Y hay doctrina
del propio Kevin para sostenerlo, aunque él la aplique a otras cosas: *"la cita textual, si no se
encontró dentro de la fuente, no va a improvisar"* (1:27:30) · *"nada con fines médicos"* · el
prompt *"no va a crear una urgencia artificial sin una base real"* · y corrigiéndose en vivo sobre
prueba social: *"clientes como tú descubrieron que consumiendo el colágeno pueden mejorar los
dolores articulares. Bueno, no exactamente van a mejorar, porque ese tipo de palabras no las vamos
a utilizar."* Hay línea clara contra inventar efectos; no la extiende a la cifra, pero es el mismo
principio.

## 6 · 🔴 LOS BLOQUES: sí los enumera, pero en el prompt de INVESTIGACIÓN

**Corregido el 2026-09-22 releyendo la transcripción entera.** Este archivo decía antes que Kevin
no recorre los bloques en cámara. **Los recorre**, uno por uno, entre **1:26:14 y 1:28:59** — lo
que no hace es recorrerlos sobre la `desc`. Los recorre sobre el **prompt de investigación**, que
es la pieza anterior: el que *"desarma el producto por completo"*. La `desc` es el volcado de esa
investigación, y por eso la investigación manda su forma.

**CITA · 1:26:14:** *"Tu trabajo es desarmar un producto por completo. Qué es, qué resuelve, qué
contiene, a quién le sirve, qué objeciones tiene el producto."*

Lo que dicta que tiene que salir, en su orden y con su minuto:

| # | Bloque | Minuto | Lo que exige |
|---|---|---|---|
| 1 | Qué es y para qué sirve | 1:26:36 | |
| 2 | **Mecanismo** — cómo funciona | 1:26:36 | el porqué, no solo el qué |
| 3 | Beneficios | 1:26:36 | *"no nos va a poner 4 ni 3, los va a poner 15 como MÍNIMO"* |
| 4 | Principales vs. secundarios | 1:26:48 | separados, no revueltos |
| 5 | Ingredientes → **CARACTERÍSTICAS** | 1:27:05 | la variación, dicha por él |
| 6 | **Punto de dolor** | 1:27:21 | *"el problema ANTES de comprar"* |
| 7 | Público objetivo | 1:27:30 | sale de la fuente, no de la imaginación |
| 8 | **A quién le puede apoyar** | 1:27:40 | *"una lista extensa de perfiles, condiciones y situaciones"* |
| 9 | Quién **NO** debería tomarlo | 1:28:09 | |
| 10 | **Objeciones y cómo romperlas** | 1:28:19 | en CUATRO partes, ver abajo |
| 11 | Mínimo **10 ángulos de venta** | 1:28:28 | |
| 12 | Resumen ejecutivo | 1:28:28 | |
| 13 | Reglas generales | 1:28:28 | lenguaje de apoyo · lo prohibido · **no improvisar citas** · *"nada con fines médicos"* |

### 🔴 La objeción tiene CUATRO partes, no dos

Lo más accionable de la clase para escribir la `desc`, y lo más fácil de perder.

**CITA · 1:28:19:** *"Objeción textual, que la causa, respuesta que la desarme y la prueba que
necesito mostrar."*

Una objeción escrita como "pregunta y respuesta" se queda en la mitad:

| Parte | Qué es | Sin ella pasa que |
|---|---|---|
| **Objeción textual** | la frase como la dice el cliente, sin parafrasear | el bot no la reconoce cuando llega |
| **La causa** | por qué la piensa | se responde el síntoma y vuelve con otra |
| **Respuesta que la desarme** | el argumento | — |
| **La prueba** | qué se muestra para sostenerla | queda en palabra contra palabra |

Cuando una objeción **no tiene prueba honesta que mostrar, eso también es información**: la
respuesta concede en vez de prometer (es el semáforo de encaje aplicado a la objeción).

### Lo que sigue siendo HUECO

**No dice qué hacer con "dosis diaria" ni con "momento ideal de toma"** en un producto que se
aplica en vez de tomarse. Para eso vale el principio de sustitución de abajo, que es **DERIVADO**.

### La estructura de la IMAGEN (CITA · 1:33:06 y 2:06:29)

No es la `desc`, pero sale de la misma investigación: **título en forma de PREGUNTA-PROBLEMA**
(*"otra noche que el calambre te tumba en la cama"*) · foto del cliente que ilustra ese dolor ·
foto del producto como protagonista · **4 beneficios** (o características) · **oferta por volumen**
(*"llévate 2 por tal precio, 3 por tal precio"*) · **envío gratis y paga al recibir** · social proof
y sellos. **CITA · 1:33:34:** hoy admite **una sola** imagen; dice que Chatea le anunció 2-3
imágenes y un audio para una próxima actualización — dato que **caduca**.

**DERIVADO (no es cita suya sobre la ficha):** sí da un **principio de sustitución**, dicho dos
veces, pero sobre el prompt de *investigación*: *"si no van a vender un producto de ingredientes,
hagan una variación que en vez de ingredientes diga CARACTERÍSTICAS. Si yo vendo esta calculadora
no puedo decir ingredientes, pero sí características"* (1:25:49) y *"si fuese un TERMO, nos va a
dar las características del termo: cuánto es el contenido, medidas de largo, profundidad, de qué
material es"* (1:53:48).

Trasladado a la ficha: **el bloque no se borra, se sustituye por su equivalente** — contenido en
cápsulas → contenido en ml; dosis diaria → modo y frecuencia de aplicación. **Esto es lectura del
principio, no una frase suya sobre la `desc`.** Márcalo así si alguien pregunta.

## 7 · La validación que él da del método

**CITA · 2:11:27:** *"en los últimos 5 días hemos cerrado 337 ventas en asistente de comentarios"*,
y antes menciona 500 ventas semanales. Es su cifra, dicha por él sobre su propia operación: sirve
para saber que el método está probado en campo, no como estadística citable hacia afuera.

## Cómo remedir esto sin pedirle nada a nadie

En `PROYECTOS/MBA-YOUTUBE/` hay dos herramientas del chat MBA:

```bash
python3 buscar.py "<tema>"                    # tema → clase, minuto, frase literal y enlace al segundo
python3 dump_ponente.py "Sept 02" "MBA"       # todo lo que dijo una persona en una clase, con minuto
```

Si vas a hornear una regla nueva atribuida a alguien, **búscala primero**. La "regla de la abuela"
sobrevivió meses en la casa sin que nadie la buscara.
