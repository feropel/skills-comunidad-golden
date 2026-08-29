# Umbral de rentabilidad ANTES de escribir la escalera (G4.7)

Esta skill escribe PRECIOS. Un precio de combo mal puesto no se descubre en la pagina: se descubre
semanas despues, con la pauta ya pagada. Por eso el umbral se calcula ANTES de proponer la escalera,
no despues.

## El criterio manda desde golden-ads (fuente autoritativa)
No inventamos formula: `golden-ads` es quien mide esto en cuentas reales. Su criterio, tal cual:
- **Breakeven CPA = margen bruto por unidad** = precio - costo - envio/COD - devoluciones.
- **Breakeven ROAS = precio / margen bruto**; en COD se ajusta por la **tasa de entrega efectiva**.
- Un CPA "bueno" no es un numero generico: es el que queda **debajo del breakeven**.
Ante duda de calculo o de que dato usar, se consulta `golden-ads` — no se adivina aqui.

## Lo que cambia en una ESCALERA de combos (aritmetica propia del COD)
Dos hechos que casi nadie mete en la cuenta y que definen si la escalera gana o pierde:
1. **El flete se paga por PEDIDO, no por unidad.** La 2a y la 3a unidad no pagan flete nuevo, asi que
   su margen marginal es MAYOR que el de la primera. **Ese es el motor real del combo en COD** — no
   "vender mas barato", sino que el envio ya esta pago.
2. **La devolucion golpea el pedido COMPLETO.** Si el combo x3 se devuelve, pierdes flete de ida y
   vuelta de las 3 unidades. A mayor ticket, mayor perdida por pedido no entregado → **el ajuste por
   tasa de entrega pega MAS FUERTE en los escalones altos**, justo donde el descuento es mayor.
El punto (1) da permiso para descontar; el (2) pone el piso. La escalera vive entre esos dos.

## Datos de entrada (se PIDEN, no se estiman)
Sin estos cuatro, la escalera NO se publica (queda en `[confirmar]`, REGLA #3):
1. **Costo por unidad** (lo que te cuesta el producto puesto en bodega).
2. **Flete por pedido** — y el de la devolucion, si el operador cobra ida y vuelta.
3. **Tasa de entrega efectiva REAL** de esa tienda/producto (la que hay; si hay un solo envio, ese es
   el dato — no se aplican umbrales minimos inventados).
4. **Comision de pasarela / plataforma**, si el modelo es pago anticipado.

## Umbral de publicacion (los 3 chequeos)
Cada escalon debe pasar los tres antes de que su precio se escriba en la pagina:
- [ ] **Margen bruto del pedido > 0** tras costo + flete, y **ajustado por la tasa de entrega**.
- [ ] **El escalon SUBE el margen absoluto por pedido** frente al escalon anterior. Un combo que
      vende mas unidades pero deja MENOS plata por pedido no es una escalera: es una fuga.
- [ ] **El escalon deja aire para el CPA**: el margen del pedido tiene que poder pagar el costo de
      adquisicion objetivo y sobrar. Margen que empata con el CPA = trabajar gratis.
Si un escalon no pasa, se sube su precio o se elimina ese escalon — nunca se publica "a ver que pasa".

## Que se le entrega al usuario junto con la escalera
Una linea por escalon, explicita: precio, margen por pedido ajustado por entrega y **CPA maximo
rentable** de ese escalon. Asi el dueno sabe con que numero comparar cuando prenda la pauta, y
`golden-ads` recibe el breakeven ya calculado desde la pagina en vez de reconstruirlo.
