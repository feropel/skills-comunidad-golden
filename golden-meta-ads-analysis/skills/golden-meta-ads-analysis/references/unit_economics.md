# Unit Economics — Guía de cálculo

## Variables necesarias

Cada análisis necesita estos 7 datos. Si faltan, preguntar al usuario.

| Variable | Descripción | Ejemplo |
|---|---|---|
| `precio` | Precio de venta al cliente (con IVA si aplica) | $79,900 |
| `costo_producto` | Costo de producir o comprar 1 unidad | $18,000 |
| `flete_entregada` | Costo del envío cuando llega al cliente | $17,000 |
| `flete_fallida` | Costo cuando devuelven o cancelan | $12,000 |
| `tasa_cancelacion` | % de órdenes que se cancelan ANTES de envío | 5-15% |
| `tasa_devolucion` | % de las que llegan al cliente y son rechazadas | 15-35% |
| `producto_recuperable` | Si en devolución el producto vuelve usable | True/False |

## Pregunta importante: base de la tasa de devolución

La tasa de devolución puede ser:
- **Sobre el TOTAL de órdenes Meta** (incluye las canceladas)
- **Sobre las que llegan a entrega** (descontando canceladas)

Estos dos casos dan números muy distintos. Siempre preguntar.

## Fórmulas (flujo correcto)

### Caso A: Devolución es % sobre las que se ENVÍAN

```
canceladas = 100 × tasa_cancelacion
enviadas = 100 - canceladas
devueltas = enviadas × tasa_devolucion
entregadas = enviadas - devueltas
```

### Caso B: Devolución es % sobre el TOTAL

```
canceladas = 100 × tasa_cancelacion
devueltas = 100 × tasa_devolucion
entregadas = 100 - canceladas - devueltas
```

## P&L sobre 100 órdenes Meta

```
ingresos = entregadas × precio

# Producto consumido
if producto_recuperable:
    costo_prod = entregadas × costo_producto
else:
    costo_prod = (entregadas + devueltas) × costo_producto
    # Las canceladas no consumen producto porque nunca se enviaron

# Fletes
flete_cancel = canceladas × flete_fallida  # 0 si el usuario dijo "no pago nada"
flete_dev = devueltas × flete_fallida
flete_ent = entregadas × flete_entregada
fletes_total = flete_cancel + flete_dev + flete_ent

margen_pre_pauta = ingresos - costo_prod - fletes_total
CPA_breakeven = margen_pre_pauta / 100
```

## CPA según margen neto deseado

```
margen_deseado = ingresos × margen_pct  # ej 10% → ingresos × 0.10
pauta_max = margen_pre_pauta - margen_deseado
CPA_max = pauta_max / 100
ROAS_objetivo = ingresos / pauta_max
```

## Escenarios de referencia (ejemplos genéricos)

Estos son ejemplos ilustrativos para entender los tipos de operación más comunes. Los datos reales de cada producto siempre los provee el usuario en cada análisis — nunca asumir ni completar.

### Escenario A: COD con cancelaciones sin costo
- El cliente NO paga en línea — paga cuando recibe
- Las cancelaciones no generan costo de flete porque el producto no se envió
- Las devoluciones (rechazo al recibir) sí generan costo logístico
- Ejemplo representativo: precio ~$75K-$85K, costo producto variable, flete entregada ~$17K, flete devuelta ~$12K
- Tasas típicas en Colombia: cancelación 5-15%, devolución 15-35% sobre enviadas

### Escenario B: COD con flete en cancelación
- Similar al escenario A, pero la transportadora cobra una tarifa fija aunque el cliente no reciba
- El costo de cancelación puede ser entre $5K-$15K según transportadora
- Preguntar siempre: "pagas algo cuando el cliente cancela antes de que salga el paquete?"

### Escenario C: E-commerce pago anticipado sin flete propio
- El cliente paga antes de recibir (tarjeta, PSE, contra entrega digital)
- No hay cancelaciones operativas — si cancela, hay reembolso pero rara vez
- El flete lo paga el cliente o se incluye en el precio
- Devoluciones típicas en e-commerce Colombia: 2-5%
- Margen bruto del producto es la métrica clave (precio - costo)

### Escenario D: E-commerce pago anticipado con flete propio
- Igual al C pero el vendedor absorbe el costo de envío
- El flete reduce directamente el margen por venta
- Calcular: `CPA_breakeven = (precio × margen_pct - flete) × tasa_entrega / 100`

## Tabla de CPA objetivo (referencia rápida)

Para cada margen neto deseado, el CPA máximo permitido es:

```
margen 0% (breakeven) → CPA = margen_pre_pauta / 100
margen 5%             → CPA = (margen_pre_pauta - 5% × ingresos) / 100
margen 10%            → CPA = (margen_pre_pauta - 10% × ingresos) / 100
margen 15%            → CPA = (margen_pre_pauta - 15% × ingresos) / 100
margen 20%            → CPA = (margen_pre_pauta - 20% × ingresos) / 100
```

## P&L histórico real de una cuenta

Esto es lo más importante de calcular para saber si la cuenta perdió o ganó:

```
gasto_total_pauta = suma de "Importe gastado" de todas las campañas de venta
compras_meta = suma de "Compras" o "Resultados" (solo compras en sitio web)
CPA_promedio = gasto_total_pauta / compras_meta

# Calcular entregadas reales aplicando las tasas:
canceladas = compras_meta × tasa_cancelacion
enviadas = compras_meta - canceladas
devueltas = enviadas × tasa_devolucion
entregadas = enviadas - devueltas

# P&L
ingresos = entregadas × precio
costo_prod = entregadas × costo_producto  # (asumiendo recuperable)
fletes = canceladas × flete_fallida + devueltas × flete_fallida + entregadas × flete_entregada
margen_pre = ingresos - costo_prod - fletes
margen_neto = margen_pre - gasto_total_pauta
margen_pct = margen_neto / ingresos × 100
```

**Si margen_neto > 0**: la cuenta es rentable, escalar lo que funciona.
**Si margen_neto < 0**: la cuenta pierde plata, hay que reestructurar antes de escalar.

## Palancas para mejorar margen

Cuando el CPA está cerca del breakeven, hay 4 palancas (en orden de impacto):

1. **Subir precio** — cada $1,000 COP de subida = ~$700-$900 más de CPA tolerable
2. **Subir tasa de entrega** — cada 1 punto porcentual menos de devolución = ~$700-$900 más de CPA tolerable
3. **Bajar costo producto** — negociación con proveedor o marca propia
4. **Bajar costo logístico** — negociar con transportadora o cambiar a otra

La que más rinde con menor esfuerzo suele ser subir tasa de entrega con verificación post-compra por WhatsApp antes del despacho.
