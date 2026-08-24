# Vocabulario de foto Golden — cómo pedir una imagen de producto

Nació de una evaluación del chat FILTRO: la guía "Higgsfield director de arte" vendía como método
propio traducir un encargo en español a especificación técnica de foto. Al medirlo, el método ya
existía en casa (`golden-cinematica`, ley de tokens exactos), pero su vocabulario es 100% web y 3D
y no tiene una sola línea de fotografía. El hueco medido con grep sobre esta skill: **0 menciones
de distancia focal, 0 de softbox o difusor**. Esta tabla llena ese hueco con el patrón de la casa.

**Cómo se usa:** FER dice la frase de la columna izquierda. Claude escribe el token de la derecha
dentro del bloque `[1 ESCENA]` del prompt maestro. Si el encargo llega vago ("hazme la foto del
frasco bonita, elegante"), **se abre esta tabla y se le devuelven 3 opciones concretas para que
elija** — nunca se adivina.

**Por qué importa:** "luz suave de estudio" es un adjetivo y cada motor lo interpreta distinto, así
que la arena termina midiendo interpretaciones en vez de motores. "Softbox de 120 cm a 45 grados,
relleno por rebote blanco, relación 1:2" es la misma foto en los cinco motores.

## Lente y distancia focal

| Lo que quieres decir | Término técnico |
|---|---|
| Que el frasco se vea cercano y el fondo quede lejos y suave | **85 mm f/2.8**, compresión de fondo, profundidad de campo corta |
| Que se vea el producto y también el ambiente donde se usa | **35 mm f/5.6**, plano de contexto |
| Que se vea como lo ve el ojo, sin deformar nada | **50 mm f/4**, perspectiva neutra |
| Detalle de la textura, la crema, el gotero, muy de cerca | **macro 100 mm f/8**, foco apilado si hace falta todo nítido |
| Foto de catálogo, recta, sin distorsión, tipo marketplace | **100 mm f/11**, cámara a la altura media del producto |
| Que el envase se vea alargado y esbelto | **135 mm**, cámara alejada (el tele estiliza; el gran angular engorda) |

> Regla dura: **nunca gran angular (menos de 35 mm) para producto**. Curva las etiquetas rectas y
> es la causa número uno de que un frasco se vea barato.

## Esquemas de luz — tamaño, ángulo y relación de relleno

La relación de relleno (**ratio**) es la diferencia entre el lado iluminado y el lado en sombra.
1:1 es plano, 1:8 es dramático. Sin ratio, el motor decide y no se repite entre piezas.

| Lo que quieres decir | Término técnico |
|---|---|
| Luz suave que envuelve, sombra tenue, aspecto premium | **softbox 120 cm a 45 grados**, relleno por rebote blanco, ratio 1:2 |
| Sombra marcada y dura, dramático, con carácter | **luz directa sin difusión a 60 grados**, sin relleno, ratio 1:8 |
| Como luz de ventana por un lado, natural | **softbox 1x2 m lateral a 90 grados**, relleno 1:4, sin cenital |
| Sin sombras, plano, fondo blanco, tipo Amazon | **frontal difusa + dos laterales**, ratio 1:1, fondo blanco puro sobreexpuesto |
| Que el vidrio o el metal brillen por los bordes | **dos luces de borde a 135 grados** + banderas negras al frente (el brillo del vidrio es reflejo, no luz frontal) |
| Sombra larga de sol de tarde | **luz dura puntual a 20 grados de altura**, temperatura cálida 3200 K |
| Ambiente limpio de laboratorio o farmacia | **luz cenital difusa amplia**, ratio 1:1.5, temperatura neutra 5600 K |
| Que se sienta de noche, íntimo | **una sola luz cálida lateral**, resto en caída a negro, ratio 1:8 |

> El vidrio y los envases cromados **no se iluminan, se reflejan**: se les pone una superficie
> blanca grande al lado para que la reflejen. Pedir "más luz" sobre un frasco transparente lo
> quema sin darle forma.

## Materiales y superficies

| Lo que quieres decir | Término técnico |
|---|---|
| Que se vea caro, de marca cara | **mármol pulido**, reflejo especular tenue, sin vetas fuertes que compitan |
| Natural, orgánico, artesanal | **madera sin tratar**, veta visible, tono medio |
| Que el frasco se refleje debajo, tipo estudio | **acrílico negro**, reflejo especular al 30 por ciento |
| Limpio, clínico, sin distracción | **acrílico blanco mate**, cero reflejo |
| Con sensación de frescura o hidratación | **microgotas de condensación** sobre el envase, no charco alrededor |
| Cálido, de casa, cotidiano | **lino o algodón sin planchar**, pliegues suaves |
| Que flote, sin superficie | **fondo infinito** con sombra proyectada suave debajo |

## Ángulo de cámara

| Lo que quieres decir | Término técnico |
|---|---|
| De frente, como se ve en la estantería | **altura del producto, 0 grados** |
| Todo el conjunto desde arriba | **cenital 90 grados** (flat lay) |
| Como lo ve alguien de pie frente a la mesa | **30 grados sobre la horizontal** |
| Que se vea imponente y grande | **contrapicado, 15 grados por debajo** de la base |
| Con volumen, que se vean dos caras | **tres cuartos: 45 grados horizontal, 20 vertical** |

## Lo que esta tabla NO decide

Esta tabla escribe el bloque `[1 ESCENA]`. **No toca nada más del prompt maestro:**

- El **producto** sigue viniendo de la imagen de referencia, y si la etiqueta lleva texto se aplica
  el método del paso 1.5 (placa de fondo + `componer.py`). Ningún ajuste de luz arregla que un
  motor invente microtexto.
- El **texto de la imagen** lo sigue escribiendo una persona, entre comillas.
- El bloque `[5 PROHIBIDO]` y las reglas de compliance por vertical **mandan sobre esta tabla**.
  Si el vertical es salud, ninguna elección de luz o ángulo autoriza un antes/después ni algo que
  parezca aval médico.

## Cuando el encargo llega vago

Ejemplo real, para calibrar. Encargo: *"hazme la foto del frasco bonita, elegante"*.

Respuesta correcta: abrir esta tabla y devolver 3 opciones nombradas, no un prompt.

1. **Editorial oscura** — 85 mm f/2.8, softbox 120 cm a 45 grados, ratio 1:8, acrílico negro con
   reflejo al 30 por ciento, tres cuartos.
2. **Clínica limpia** — 100 mm f/11, cenital difusa amplia, ratio 1:1.5, acrílico blanco mate,
   frontal a 0 grados.
3. **Luz de ventana cálida** — 50 mm f/4, softbox 1x2 m a 90 grados, ratio 1:4, madera sin tratar,
   30 grados sobre la horizontal.

FER elige una y ese es el bloque `[1 ESCENA]`. Las tres son la misma foto en los cinco motores de
la arena, que es justo lo que la arena necesita para medir motores y no interpretaciones.
