# Unit economics + breakeven (la calculadora que valida todo veredicto)

**Esto NO es un P&L / informe de ganancias.** Es solo para calcular el **breakeven** (CPA/ROAS máximo
rentable): la línea que decide pausar vs escalar. Sin él, "ROAS 3,2" no dice si ganas o pierdes.
- **VEREDICTO** sobre campañas existentes → se necesita (si no, solo ranking relativo).
- **MONTAR un test** → NO bloquea; marca `[PENDIENTE]` y sigue (luego fija los topes con el breakeven).
Pide los datos concreto; si falta uno, márcalo y avanza.

## 🚦 PRIMERA PREGUNTA, ANTES DE CUALQUIER CÁLCULO: qué modelo de pago es

**Golden opera los DOS.** Catálogo y dropshipping van contra entrega; las **marcas propias**
(clientes que ya conocen el portal y compran directo) van con **pago anticipado**. No asumas.

| | **Contra entrega (COD)** | **Pago anticipado** |
|---|---|---|
| Cuándo se cobra | al entregar, si el cliente recibe | **al comprar, siempre** |
| Tasa de entrega | 55–75%, castiga el breakeven | **100% — no se descuenta nada** |
| Costo de devolución | sí, flete de ida y vuelta | no |
| Comisión | recaudo del operador | **pasarela (Stripe / Mercado Pago), ~3–4% + fijo** |
| Evento de checkout | **no existe** `InitiateCheckout` | **sí existe**, y es señal temprana valiosa |
| Fórmula del breakeven | margen × % de entrega | **margen, sin multiplicar** |

> ⚠️ **El error de aplicar la fórmula equivocada cuesta plata en las dos direcciones.**
> Con el ejemplo de abajo (margen cobrado 54.900): en COD al 65% el techo es **35.685**; con pago
> anticipado el techo real es **54.900**, un **54% más alto**. Usar el cálculo COD en una marca
> propia te hace **pausar campañas que sí ganaban**. Y al revés, usar el de pago anticipado en COD
> te hace escalar campañas que pierden, y no te enteras hasta 3 semanas después.
> **Pregunta el modelo de pago antes de calcular. Siempre.**

## ⚠️ Regla de oro COD: el ROAS de Meta ≠ ROAS pagado
**(Esta sección aplica SOLO a contra entrega. En pago anticipado el ROAS de Meta ya es el real.)**
`purchase_roas` de Meta se calcula sobre **órdenes puestas** (evento del pixel), NO sobre **entregadas
y cobradas**. En COD LatAm la **tasa de entrega efectiva** es ~55–75%. Por eso:
> **ROAS pagado ≈ ROAS Meta × tasa de entrega.** Un ROAS Meta de 3,0 con 65% de entrega ≈ **1,95 real**.
Siempre descuenta por entrega antes de declarar rentabilidad. Igual para el CPA: el CPA real por venta
**cobrada** = CPA Meta ÷ tasa de entrega.

## Datos de entrada (pídelos)
- **Precio de venta** (lo que paga el cliente): `[PRECIO]`
- **Costo del producto** (COGS, con importación): `[COSTO]`
- **Costo de envío / logística COD** (ida; y devolución de no-entregados): `[ENVIO]`
- **Tasa de entrega efectiva** (% de órdenes que se cobran): `[ENTREGA %]` (si no la sabe: usar 65% como supuesto marcado)
- **Comisión pasarela / plataforma / recaudo** (si aplica): `[COMISION]`
- **Otros** (empaque, operador, WhatsApp): `[OTROS]`

## Cálculos

**Base, igual para los dos modelos:**
```
Margen bruto por venta cobrada = PRECIO − COSTO − ENVIO − COMISION − OTROS
```

**Si es CONTRA ENTREGA** — se castiga por lo que no se cobra:
```
Breakeven CPA (por venta ENTREGADA)   = Margen bruto
Breakeven CPA (por compra en META)    = Margen bruto × ENTREGA%   ← contra esto comparas el CPA de Meta
Breakeven ROAS (Meta)                 = PRECIO / (Margen bruto × ENTREGA%)
```

**Si es PAGO ANTICIPADO** — no hay nada que descontar, la venta ya está cobrada:
```
Breakeven CPA (por compra en META)    = Margen bruto        ← sin multiplicar por nada
Breakeven ROAS (Meta)                 = PRECIO / Margen bruto
```
Ojo con dos cosas propias del prepago: la **comisión de pasarela** va dentro de COMISION (Stripe o
Mercado Pago, ~3–4% + fijo por transacción, calcúlala sobre el PRECIO), y si ofreces **cuotas sin
interés** el costo lo asume el comercio — súmalo también o el margen sale inflado.

- **Compara el `cost_per_result` (CPA Meta) contra el "Breakeven CPA por compra en Meta".**
  CPA Meta < breakeven → gana; > → pierde. Así el veredicto es real, no a ojo.

## Ejemplo lado a lado (mismo producto, los dos modelos)
Datos: PRECIO 89.900 · COSTO 18.000 · ENVIO 12.000 · COMISION 3.000 · OTROS 2.000
→ **Margen bruto = 54.900** en ambos casos.

| | Contra entrega (65%) | Pago anticipado |
|---|---|---|
| Breakeven CPA Meta | **35.685** | **54.900** |
| Breakeven ROAS Meta | **2,52** | **1,64** |
| CPA objetivo sano (50–70%) | 21.000–25.000 | 27.000–38.000 |

**La misma campaña con CPA 43.000 PIERDE en COD y GANA en pago anticipado.** Ese es el tamaño del
error: 43.000 está por encima de 35.685 pero por debajo de 54.900. Un solo dato mal asumido invierte
el veredicto. *(Cifras de ejemplo — usar SIEMPRE los datos reales del producto.)*

## Escalera de rentabilidad (SIEMPRE incluirla — al cliente le encanta y decide rápido)
No entregues solo un breakeven suelto: dale la **escalera** de "hasta aquí es rentable".
1. **CPA máximo (breakeven)** = `[Margen cobrado]`. Por encima → pierdes.
2. **CPA objetivo (sano)** = ~50–70% del breakeven → deja margen real. (ej. breakeven 35.685 → apunta a 21.000–25.000).
3. **ROAS objetivo (rango)**: de **breakeven ROAS** (piso, no perder) a **breakeven ROAS × 1,5** (sano).
   Ej. breakeven 2,52 → "tu ROAS Meta debe estar entre **2,5 y 3,8**" (recuerda: ROAS pagado = ×entrega).
4. **Escalera por ventas** (cuánto ganas/pierdes según el CPA al que compres):
   | Si tu CPA es… | vs breakeven | Ganancia por venta | Con 5 ventas/día | Con 20/día |
   |---|---|---|---|---|
   | 20.000 | 🟢 | +34.900 | +174.500 | +698.000 |
   | 30.000 | 🟢 | +24.900 | +124.500 | +498.000 |
   | 35.685 | ⚪ breakeven | 0 | 0 | 0 |
   | 45.000 | 🔴 | −9.315 | −46.575 | −186.300 |
   *(Cifras de ejemplo con margen 54.900; reemplazar por las reales.)* Así el cliente ve **exactamente**
   hasta qué CPA puede pagar y qué pasa a cada volumen. Traduce el número a decisión, no lo dejes abstracto.

## Combo = la palanca de rentabilidad en COD (mide el attach real)
Con **flete fijo por pedido**, la **unidad SUELTA suele PERDER**: cuando el CPA + flete supera el margen
de 1 unidad, cada pedido de una sola pieza sangra. La salida no es bajar el CPA a lo imposible, es **subir
las unidades por pedido (combo attach)**.
- Saca el **attach real** de la data de pedidos (`golden-dropi-analisis`): **unidades ÷ pedidos**.
- Si el attach es **~1,0–1,1**, la operación está sangrando → **empuja combo en la página y en el bot**
  (2x/3x con descuento, "lleva la línea completa", his&hers). El combo reparte el flete fijo entre más
  unidades y **mueve el breakeven a tu favor**. Recalcula el breakeven con el **ticket de combo**, no con
  el de 1 unidad.
- Caso Le'côterra: la venta suelta no cubría flete; el **combo (dúo/línea)** fue lo que volvió rentable la
  operación → por eso los creativos de línea/dúo rutean **al combo primero** (ver `08-creativos-testeo.md` §6).

### La escalera de rentabilidad se calcula POR ESCALÓN DE COMBO (obligatorio)
No basta un breakeven del ticket promedio: **calcula el breakeven CPA para cada escalón de la
oferta (1 unidad / combo x2 / combo x3)** y preséntalos JUNTOS. La conclusión operativa —
"sin combo esto no cierra" — **solo aparece cuando se ven los tres escalones a la vez**.

Caso real (estudio dental Chile, 2026-08-07): con costo estimado $8.500, envío/recaudo $4.500 y
entrega 65%, el breakeven CPA en Meta fue:
| Escalón | Breakeven CPA Meta |
|---|---|
| 1 unidad | **$9.744** |
| Combo x2 | **$12.019** |
| Combo x3 | **$13.000** |

Con CPAs reales del nicho por encima de $9.744, la unidad suelta era inviable y el negocio solo
cerraba desde el combo — veredicto invisible mirando un solo número. **Entregable: tabla de
breakeven por escalón + veredicto explícito de si la unidad suelta es viable.**

## Palanca de PRECIO — recomendación estándar cuando el margen queda apretado
Si el precio propuesto está en el **piso** del rango de mercado, **subirlo al techo del MISMO
rango es la decisión más rentable disponible**: no cambia el posicionamiento (sigue dentro de
donde ya compite todo el mundo) y cada peso extra va directo al margen.
- Caso real (Chile, 2026-08-07): de $27.990 a $29.990 son **$2.000 más de margen = 13% más de
  techo de CPA**, sin salir del rango donde competían los 5 rivales.
- Sácala **siempre que el margen quede apretado** tras calcular el breakeven, y **siempre como
  recomendación: el precio lo fija el dueño.**

## La ENTREGA por TRANSPORTADORA cambia el breakeven (elige la de menor devolución)
La **tasa de entrega efectiva** (§ Regla de oro) **no es única**: varía por transportadora, y cada punto de
devolución mueve el breakeven. Prefiere enrutar a la transportadora de **menor devolución** en cada
ciudad/zona (dato de `golden-dropi-analisis` / ver `17-entrega.md`).
- Caso real Le'côterra (devolución observada): **Envia 11,6%** < **Veloces 18,2%** < **Interrapidísimo 23,7%**.
  Con esos números, la MISMA campaña es rentable por Envia y pierde por Interrapidísimo — el CPA Meta no
  cambió, cambió la entrega. Descuenta SIEMPRE el CPA/ROAS por la **entrega de la transportadora que
  realmente reparte** ese pedido, no por un promedio de cuenta.

> Entregable: incluye la tabla de economics + la **escalera de rentabilidad** al inicio del `DIAGNOSTICO.md`
> / `META-ADS.md`, antes del semáforo. Es lo primero que el cliente necesita para decidir.
