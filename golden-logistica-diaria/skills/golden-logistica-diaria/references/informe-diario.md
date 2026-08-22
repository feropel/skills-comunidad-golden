# CONTRATO DEL INFORME DIARIO · golden-logistica-diaria

**Versión de la skill: la que declara `SKILL.md` (hoy `GLD1.28`). Este contrato no lleva número propio: tenía uno y quedó tres versiones atrás.** Construido y corrido contra datos reales de Dolce.

## EL FORMATO ES CORTO · construido, no pendiente

FER tenía dos versiones del mismo día en el Escritorio, una de 2 páginas y otra de 6, y
conservó la de 2. A las siete de la mañana necesita **acciones**, no cobertura.

Ya está implementado: tabla de acciones primero, **una sección es bloque solo cuando TIENE
hallazgos**, los mensajes en anexo aparte — pesaban el 42% del documento — y la cobertura al
final en una tabla. Medido: un día cargado da 4 páginas, **un día limpio da 1**.

Este documento ya no es una propuesta. Dice, sección por sección, **qué produce hoy el
generador y qué todavía no**. Cada sección lleva su estado, y el estado es verificable
corriendo `scripts/generar_informe_diario.py`.

## Reglas del entregable

- **El WhatsApp va primero y sin espacios**, con el 57 delante. Listo para copiar y pegar.
- **Cobertura, no veredicto.** Cada sección dice cuántos de cuántos se revisaron y con qué método.
- **Un cero siempre dice de dónde sale.** "No hay discrepancias" y "no se pudo comparar nada"
  son frases distintas y el informe nunca las confunde. Esta es la regla que más veces se ha
  roto en esta skill: primero mintió la prosa, después mintió la variable.
- **Un mensaje copiable jamás se trunca.** Si es largo, se parte en líneas; nunca con puntos
  suspensivos, porque se pega tal cual en WhatsApp.
- **Regla de negocio = pregunta, no veredicto.** Si el bot dice una cosa y la config dice otra,
  el informe pregunta si es diseño o error.
- **Cero datos inventados.** Lo que no se obtuvo va como no obtenido, con el pedido nombrado.

## Semáforos

| | Qué significa | Qué hago yo | Qué haces tú |
| --- | --- | --- | --- |
| 🔴 | Se pierde hoy si no se toca | Lo dejo listo, no lo ejecuto | Decides y yo aplico |
| 🟡 | Urge pero aguanta | Preparo el mensaje o el cambio | Apruebas |
| 🟢 | Va bien, sigue solo | Nada | Nada |

## LA FORMA · dos partes, y en este orden

**Parte 1 · el asistente de WhatsApp.** Todos los contactos, el embudo, dónde se quedó cada
quien y por qué no compró. **De primera, antes que nada: los que hablaron de último y nadie
les contestó.** Ahí el que se fue no fue el cliente, fue la empresa — y esa lista es la plata
más caliente que hay en el día.

**Parte 2 · la logística.** Pedidos, transportadoras, precios, efectividad por municipio,
huella y decisión pedido a pedido.

Dentro de cada parte manda «acciones primero». Lo produce `scripts/informe_360.py`, que hereda
**todas** las leyes del generador corto: cero honesto, veredicto de variable, la invariante de
decisiones, anti-pisado del PDF y nombre canónico del chat.

**El motivo de no compra se lee SOLO de lo que escribió el cliente.** El bot menciona precio y
envío en todas las conversaciones; buscar «caro» en el hilo completo clasificaría al 100% como
objeción de precio.

**Y el hilo se pide con `include_bot=1`.** Sin ese parámetro el endpoint devuelve solo los
mensajes entrantes, y «el bot nunca respondió» se ve igual que «el bot respondió y el cliente
se fue». Medido en un hilo real: 2 mensajes del bot sin el parámetro, 55 con él.

## Las secciones que SE GENERAN HOY

### Resumen · el orden en que se cierran las ventanas
Tabla de conteos con semáforo. Lo que no se pudo mirar aparece como **"no se pudo mirar"**,
nunca como cero.

### 🔴 1 · Frenar llamando a la bodega
Los que ya salieron y van mal. **Pregunta por TODOS los estados de decisión**, no solo por
"hay que cambiar": sin cobertura, sin transportadora asignada y — sobre todo — **sin decisión
calculada** también se marcan. Un pedido sin decisión salía antes como "va bien" aquí y como
"la bodega no despacha" tres secciones más abajo.
Cierra diciendo cuántos de los que salieron sí van bien.

### 🔴 2 · Novedades
Priorizadas por valor. Con la huella del cliente leída **sobre pedidos cerrados**: un pedido
en tránsito no es un fracaso todavía. Las que ya figuran como solucionadas se nombran aparte
para que nadie las busque.

### 🟡 3 · Esperando en oficina
Los que llegaron y nadie recoge. Se pierden en silencio.

### 🟡 4 · Cambiar transportadora antes de la guía
Solo los que todavía no tienen guía, donde el cambio es gratis. Con flete, efectividad en ese
municipio y el motivo. **Un cambio que sale más caro que dejarlo quieto no aparece aquí**: se va
a la sección 8.

### 🔴 5 · El chat contra la orden
Cantidad y color de lo pedido contra lo cargado. Dice **cuántos se compararon de verdad**, no
cuántos eran candidatos, y lista aparte por qué no se pudo comparar el resto.

### 🟡 6 · Direcciones que no sirven
Con la pregunta exacta para el cliente. Recoger en oficina **no** es una dirección mala.

### 🟡 7 · Embudo de Chatea
Contactos que dieron dirección, ciudad y producto y nunca se volvieron pedido. Con la cobertura:
cuántos se revisaron, cuántos se quedaron antes de la dirección, y cuántos no respondieron.

### 🟡 8 · Los que decides tú
Donde el cálculo no alcanza: sin cobertura, sin transportadora, cambios que salen más caros, y
pedidos que el motor no devolvió.

### 9 · Mensajes para copiar
Todos juntos al final, sin signos de apertura, sin truncar.

## Las secciones que TODAVÍA NO se generan

Están en el diseño original y **no están construidas**. Se declaran aquí para que nadie las dé
por hechas al leer la descripción de la skill.

| Sección del diseño | Estado | Qué falta |
| --- | --- | --- |
| **Plata parada** · pedidos que fallaron al subir a Dropi | NO CONSTRUIDA | Necesita leer el tablero de error de Chatea, no solo las órdenes de Dropi |
| **Tendencia** contra ayer y contra la semana | NO CONSTRUIDA | Necesita guardar el informe de cada día para comparar; hoy no hay serie |
| **Cabecera de ceguera** en una sola tabla | PARCIAL | Cada sección declara lo suyo, pero no hay todavía una tabla única al inicio |
| Ficha por pedido con huella por transportadora | PARCIAL | El dato existe y lo usa el motor; el informe lo resume, no lo despliega |

## Cómo se entrega

En **Markdown y en PDF**, siempre los dos. El PDF sale por `--pdf`, pasa por `golden-pdf-check`
y su veredicto se imprime. Los mensajes van en su **anexo aparte**, que también es Markdown y
también admite PDF.

**La política de sobrescritura es una sola y vive en `scripts/comun.py`** (aquí se citaba mal:
decía que el generador se niega siempre). Lo real: cuando esta skill escribe un PDF deja una
**marca de autoría** al lado. Si mañana hay un PDF en esa ruta **con la marca**, es suyo y se
archiva en `_archivo/` antes de escribir el nuevo — así la segunda corrida del día funciona.
Si **no tiene marca**, es de otro y **no se toca**: el generador se niega y lo dice.

## Qué pasa después del informe

- Lo 🟢 no necesita nada.
- Lo 🟡 lo dejo preparado y tú apruebas en bloque.
- Lo 🔴 se queda quieto hasta tu palabra.
- **Nada que le escriba a un cliente sale sin tu OK.**

## Lo que la skill NO hace

- **No genera guías ni confirma pedidos en Dropi por su cuenta.** Recomienda, tú apruebas.
- **No le escribe a ningún cliente sola.**
- **No decide reglas de negocio.** Cuando el bot diga una cosa y la config otra, pregunta.
- **No inventa el dato que falta.** Lo marca y sigue.
- **No corre sobre una cosecha incompleta.** Si el volcado no declara `cosecha_completa: true`,
  el motor y el informe se niegan los dos, por separado.
