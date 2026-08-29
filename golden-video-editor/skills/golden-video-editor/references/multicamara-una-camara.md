# Multicámara con una sola cámara

Destilado por el chat FILTRO de dos PDFs de NinoDirector / La Fábrica (ago-2026). Llevaba desde el
**16-ago** en `STACK-GOLDEN/DESTILADOS/` sin que ninguna skill lo nombrara. Barrido previo con
`sinapsis.py`: **capacidad nueva, 0 de 89 skills** mencionaban multicámara, punch-in ni encuadre.

## El diagnóstico (por qué esto importa)

> *"El video se cae y tú revisas el guion. Casi nunca es el guion. Es que debajo de las cards, los
> cutaways y los capítulos hay un solo encuadre, y cada vez que una capa se quita, el espectador
> vuelve exactamente al mismo cuadro."*

Meter más gráficos **compra tiempo hasta el próximo corte**, no arregla nada: la capa siempre se
levanta. Lo que arregla es que **el encuadre cambie cuando cambia la idea**, no cuando el editor
se aburre.

## Las tres cámaras (son POSICIONES, no equipos)

| Cámara | Cómo se ve | Para qué bloque |
|---|---|---|
| **Frontal** | ojo al lente, altura de ojos, plano medio | **Habla al espectador**: hook, promesa, CTA |
| **Lateral** | tres cuartos, más lejos, pared del costado a la vista, **nunca mira al lente** | La narración |
| **Closeup** | más bajo, más cerca, fondo desenfocado | La frase corta que quieres que repitan |

**La prueba de que la cámara se movió NO es la distancia**: es que **cambia la pared que se ve y
entran o salen objetos**. Recortar más cerca y llamarlo cámara nueva se nota a la segunda vez. El
lateral debe enseñar la pared del costado —invisible en las otras dos— y meter algo que antes no
estaba: una puerta, el borde de una ventana, un mueble.

**Lo que NO cambia:** misma luz, mismos muebles, un solo color de acento. *Cambia la posición, no
el mundo.*

## El reparto va sobre el GUION, no sobre el video

Un bloque = una idea. Cuando termina la idea, termina la cámara.

```
bloque 1: frontal   ← hook, mira al lente
bloque 2: frontal   ← promesa, sigue de frente
bloque 3: lateral   ← empieza la historia, deja de mirarte
bloque 4: lateral   ← la historia sigue
bloque 5: lateral   ← el giro
bloque 6: frontal   ← vuelve a ti para pedirte algo
```

**El frontal SE GUARDA para cuando te habla a ti.** Si toda la narración va de frente al lente, el
CTA no tiene con qué distinguirse y el espectador no siente el cambio de registro.

**El closeup no se reparte: se pide.** Uno cada ~3 minutos vale; uno cada 30 segundos deja de
significar nada.

## Los números

| Regla | Valor |
|---|---|
| Cambio de encuadre | cuando cambia la idea · referencia **~1 min 30 s** |
| Demasiado rápido | cada 10 s **no es ritmo, es ruido** |
| Punch-in | entra al **113%**, tope duro **125%** |
| Por encima del tope | se ve el grano de la ampliación y el truco se descubre |
| Ventana para buscar el silencio | hasta **1,5 s** |

**El corte cae en el SILENCIO más cercano, no donde el reparto lo pidió.** Un corte a mitad de
palabra se oye aunque la imagen sea impecable. **Si en esa ventana de 1,5 s no hay silencio, NO se
corta**: es mejor no cortar que cortar mal.

## Dos trampas de montaje

1. **Nunca un cutaway a pantalla completa justo encima de un cambio de cámara.** El espectador no
   ve el cambio, ve el gráfico; y cuando el gráfico se va, el sujeto aparece en otro sitio sin
   transición. Los cambios de posición van **detrás** de los gráficos.
2. **Si el editor ya hace punch-ins por su cuenta, apágalos.** Dos sistemas acercándose sobre el
   mismo metraje se pelean: zoom encima de zoom.

## Si los fondos se generan con IA

Este bloque va **idéntico** arriba de los tres prompts; es lo que hace que el generador repita la
misma habitación:

```
Photoreal interior of a [tu cuarto], EMPTY of people.
ONE dominant light source enters from a side window or an overhead LED panel,
warm temperature (~3200K), with a second, dim fill light that never competes.
ONE accent color only: [hex]. It appears on no more than two objects in the room.
Same room, same furniture, same light in every shot.
No text, no logos, no on-screen graphics.
```

**`EMPTY of people` es el detalle que todos se saltan.** Sin declararlo, el generador mete una
persona en el cuarto, y esa persona no eres tú.

Los tres fondos los produce `golden-imagen-arena`, y su `references/vocabulario-foto.md` traduce
"luz cálida de ventana" a la especificación exacta (tamaño de fuente, ángulo, relación de relleno,
temperatura). Aquí el prompt da la INTENCIÓN; ese vocabulario da los NÚMEROS.

## Zona honesta (del propio autor, y por eso el material es creíble)

- *"No graba por ti. Recorta el video que tú ya grabaste."*
- ***"Sin fotos por cámara NO hay cambio de cámara: hay reencuadre, y se dice así."***
- *"No arregla un guion sin bloques: si la idea no cambia, no hay dónde cortar."*
- *"No salva un video aburrido. Un plano fijo aburrido, cortado, sigue aburrido."*
- Sobre su dato de retención: *"Una sola fuente, interna. Tómalo como pista, no como ley."*

## Cómo se sabe si funcionó

**El minuto en el que la gente se iba antes.** Si ese minuto se corre hacia adelante, el método
sirve en ese canal. Si no se mueve, **el problema estaba en el guion** y esto no lo iba a arreglar.

## Nota comercial, declarada

Los PDFs son lead magnets de una comunidad de pago. **El método está completo en ellos** y se
ejecuta a mano con una cámara y un trípode; lo que venden es el comando que lo automatiza. **No
hace falta comprar nada para aplicar esto.**
