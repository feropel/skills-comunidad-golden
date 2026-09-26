# Economía COD de Golden: por qué el margen se CALCULA y no se estima

Mudado del cuerpo del SKILL.md el 2026-09-18 (GPG1.14): el cuerpo se paga en cada activación y
esta historia solo hace falta cuando se discute un precio. Nada se borró. La regla operativa que
queda en el cuerpo es una: **correr `scripts/viabilidad_cod.py` y llevar a la ficha el PVP mínimo
en pesos**. Lee este archivo cuando alguien pregunte por qué no sirve "costo × 3", cuando un
número de la cuenta parezca raro, o antes de cambiar `assets/economia-cod-golden.json`.

## La compuerta: antes de puntuar nada

```bash
python3 scripts/viabilidad_cod.py --costo <costo> --pvp <pvp>
```
**Si no pasa el piso, el producto se DESCARTA aunque saque 95 en todo lo demás.** Un ganador
con demanda, wow y logística perfecta que deja $492 por pedido generado (un producto de
$30.000 vendido a $80.000, que se puede reproducir con el script) no es un ganador:
es trabajo gratis con riesgo. La puntuación mide qué tan bueno es el producto; la compuerta
mide si el negocio existe.

**Por qué dejó de estimarse.** Decía *"≥3× = puntos llenos"*, una regla de pulgar heredada de
un curso que usa **números prestados**. Medidos contra **18.391 pedidos reales de Dropi**:
entrega **73,5%** (el curso asume 75), flete **$15.664** (asume $12.000), **pedido fallido
$12.518** (asume $8.000) y **CPA $21.428**. Los cuatro medidos.

**El fallido es UN SOLO cobro y siempre MENOR que el flete de ida** — de 0,73 a 1,00 según
transportadora, y Servientrega es la única que cobra igual. Si el pedido se devuelve no hubo
recaudo, así que no se paga la gestión de cobro. **No hay flete de ida y flete de vuelta.**

🔴 **Este número ya estuvo mal una vez: no volver a $29.182.** Ese salía del informe *por
producto*, donde la columna solo la llena una transportadora (37% de las filas) y además
inflada. Exigía **$6.258 de PVP de más a cualquier costo**. Los buenos salen de los informes
*por pedido*: 4.074 de 4.120 devoluciones, el 99%, todas las transportadoras.

**El CPA ya está medido: $21.428 por pedido generado** (pauta Meta mensual contra pedidos
creados, 2026). El supuesto anterior de $14.000 **se quedaba 53% corto**.

🔴 **Pero es un PISO, no un punto.** El denominador incluye pedidos que no vinieron de anuncio
—orgánico, WhatsApp, recompra— y un mes puede estar incompleto. **El CPA real es igual o mayor**,
así que todo veredicto de aquí sale optimista por construcción.

Por eso el script no se queda en un sí o un no: dice **cuánto CPA aguanta el producto**. Ese
número es derivado, no inventado, y es lo que de verdad separa un margen real de uno de papel —
si un producto aguanta $23.000 de CPA y el piso medido es $21.428, ese margen puede no existir.

🔴 **La comisión de recaudo es 0, y no porque nadie la cobre: porque ya está dentro del flete.**
La transportadora cobra alrededor del 5% del flete base por recaudar, y Dropi ya lo incluye
cuando se genera la orden (FER, 2026-09-23). El flete medido de $15.664 sale de lo que Dropi
**cobró de verdad**, así que esa gestión ya está adentro. Restarle además un 4% del PVP era
cobrarla **dos veces**, y la segunda sobre la base equivocada: el precio de venta en vez del flete.

Hasta el 2026-09-23 este archivo decía que era "el único número sin medir" porque la columna
COMISION venía vacía. **La columna no estaba vacía por falta de dato: estaba vacía porque no se
cobra aparte.** Comprobado sobre los 17 informes "por pedido" de Golden Colombia (18.792 filas):
**1 pedido entregado de 11.669 trae comisión > 0 (0,0086%)**, y los valores distintos de cero que
existen en esa columna están en pedidos CANCELADOS de un solo informe de 2024.

El término sigue vivo en la fórmula: si algún día una transportadora cobra el recaudo **por
fuera** del flete, se revive con `--comision`. La señal para darse cuenta es esa misma columna.

**El 2,5× que el curso ofrece como red de seguridad no alcanza ni de lejos.** Ese producto
necesita **3,01×**, y uno de $10.000 necesita **7,02×**. A ojo esa diferencia no se ve.

⚠️ **Esta tabla se ha movido CUATRO VECES**: 2,99 → 2,78 → 3,13 en un solo día (06-sep) y 3,01
el 23-sep, al quitar la comisión duplicada. Es la prueba de por qué **a la ficha va el piso en
pesos y nunca una cifra de multiplicador**.

🔴 **Y el aviso que más vale de todo esto: los dos errores se compensaban.** Con el fallido
inflado (que sube el mínimo) y el CPA supuesto en $14.000 (que lo baja) salía **2,99×**. Con los
dos corregidos sale **3,13×** (las dos cifras de aquel día, con la comisión al 4%; hoy son
3,01×). Casi el mismo número por dos errores en direcciones opuestas —
**arreglar solo uno habría empeorado la regla creyendo que se mejoraba.**

#### 🔴 El multiplicador NO es constante, y por eso no puede vivir como cifra
La regla corta dice "3x". **Medido con la propia fórmula, "3x" solo es cierto alrededor de un
costo de $30.000** — que casualmente es el ejemplo del curso:

| Costo del producto | Multiplicador mínimo |
|---|---|
| $10.000 | **7,02×** |
| $20.000 | 4,01× |
| $30.000 | **3,01×** |
| $50.000 | 2,20× |

**Por qué:** el flete, el pedido fallido y el CPA son costos **fijos por pedido** y no escalan
con el costo del producto. Cuanto más barato el producto, más veces su costo hay que cobrar
para pagar los mismos fijos.

**Consecuencia para el bootcamp y para nosotros: los productos baratos son mucho más difíciles
de lo que parecen.** Un producto de $10.000 que se vende a $50.000 suena a negocio redondo —
5× el costo— y pierde plata. Es el error más caro que puede cometer un alumno.

**Lo que se lleva a la ficha es el piso de $8.000 por pedido generado, no un multiplicador.**
El multiplicador se calcula por producto y se dice; nunca se cita de memoria.

**Se cuenta por pedido GENERADO, no por entregado.** La pauta se paga por cada pedido que
entra, llegue o no; contar solo los entregados esconde el 26,6% que cuesta y no paga.

✅ **Ya no queda ningún número supuesto: los cinco están medidos.** El CPA dejó de ser supuesto
en GPG1.12-d ($21.428 MEDIDO como piso, ver arriba) y la comisión de recaudo el 2026-09-23
(0, porque ya va dentro del flete). Hasta GPG1.13 este párrafo seguía diciendo "CPA $14.000
supuesto, mientras no se mida": contradecía al de arriba y se corrigió el 2026-09-18.

**Lo que sí se sigue declarando en cada veredicto es que el CPA medido es un PISO, no un punto**:
el real es igual o mayor, así que todo veredicto que salga de aquí es optimista por construcción.
Los cinco viven en `assets/economia-cod-golden.json` y se sobreescriben por parámetro
(`--cpa`, `--comision`, `--entrega`, `--piso`).

