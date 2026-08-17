# Criterios de decisión

## Prepago (SIN RECAUDO): manda el precio

El cliente ya pagó, así que se entrega casi siempre. Verificado en la operación de Golden:
**9 de 9 prepagos resueltos se entregaron, cero devoluciones.** Con la probabilidad de entrega
prácticamente igualada entre empresas, lo único que queda por optimizar es el flete.

**Regla:**
1. Descartar las que estén a más de **3 puntos de efectividad** por debajo de la mejor disponible.
2. Entre las que quedan, la **más barata**.
3. **Excepción:** si una con mejor efectividad cuesta **menos de $1.500 más**, se prefiere esa.

Sin comisión de recaudo y sin costo de retorno.

> Ejemplo real: Guarne, Antioquia. Interrapidísimo $19.119 al 91,45% contra Envía $20.303 al
> 96,65%. Son $1.184 más por 5 puntos: va Envía.

## Contra entrega: manda el valor esperado

```
EV = p × (ticket − costo − flete) − (1 − p) × (flete + retorno)
```

- `ticket` = `VALOR DE COMPRA EN PRODUCTOS` del export.
- `costo` = `TOTAL EN PRECIOS DE PROVEEDOR`.
- `flete` = **el de la cotización en vivo**, no el de la tabla.
- `retorno` = `flete × fracción medida` de esa transportadora (`COSTO-RETORNO.json`).
- **Comisión de recaudo = 0** para Golden (plan SUPPLIER PREMIUM, verificado en 125 entregados).

## Cómo se calcula `p`

Dos correcciones bayesianas encadenadas sobre la efectividad del departamento. La idea: la zona es
una **suposición inicial** que la evidencia del cliente va corrigiendo, y cuanta más evidencia hay,
más manda ella.

```python
p = base_zona / 100                              # Torre Logística, departamento × transportadora
if total_cliente > 0:                            # historial GLOBAL del cliente
    p = (entregadas_pct/100 * total + 10*p) / (total + 10)
n = entregas_con_esa + devoluciones_con_esa       # historial con ESA transportadora
if n > 0:
    p = (entregas_con_esa + 3*p) / (n + 3)
```

Los pesos `10` y `3` son cuántos envíos "vale" la suposición previa. El global necesita muchos
pedidos para mover la zona; **el historial con esa transportadora manda casi de inmediato**, que es
justamente lo que se quería: si al cliente ya le funcionó la barata, se queda la barata.

**Funciona en los dos sentidos, y eso es la mitad de su valor.** Si al cliente le fue mal con una
empresa, esa empresa pierde aunque sea la más barata y la mejor de la zona.

> Ejemplos reales del 2026-08-01:
> - **Riosucio** — cliente 3 de 3 con Envía y 4 de 4 con Interrapidísimo. Envía es la más barata:
>   se queda Envía, aunque Coordinadora tenga mejor efectividad de zona.
> - **Valledupar** — cliente 9 entregas y 6 devoluciones con Envía, 6 de 6 con Interrapidísimo.
>   Vale pagar $3.888 más por sacarlo de Envía.
> - **El Bagre** — Coordinadora es $4.180 más barata, pero al cliente le devolvieron su único envío
>   con ella. Se queda Interrapidísimo.

## Evidencia fuerte y evidencia delgada

El modelo produce recomendaciones con muy poca evidencia detrás. **Antes de recomendar pagar más,
mirar cuántos envíos la respaldan.**

| Situación | Qué hacer |
|---|---|
| La recomendada es **más barata Y** entrega igual o mejor | Recomendar sin reservas |
| Paga más, con **5 o más envíos** del cliente respaldándolo | Recomendar, diciendo el respaldo |
| Paga más, con **1 o 2 envíos** de respaldo | **No recomendar.** Mostrarla como mirada y descartada |
| La transportadora casi no tiene envíos propios de Golden | Recomendar, **avisando que el respaldo es de plataforma, no propio** |

## Separar el ahorro del valor esperado

**Nunca sumarlos en una sola cifra.** El ahorro de flete es plata inmediata y cierta; el valor
esperado incluye devoluciones que quizá no habrían pasado. Reportar dos columnas.

## Semáforo del cliente

| Color | Cuándo | Acción |
|---|---|---|
| 🔴 Rojo | Dropi lo marca `Incierta`, o 5+ pedidos con 40%+ de devolución | Pedir anticipo |
| 🟠 Naranja | 5+ pedidos con 25-40% de devolución, o 1-2 pedidos y devolvió | Confirmar por WhatsApp |
| 🟡 Amarillo | 15-25% de devolución | Despachar, con la mejor entrega |
| 🟢 Verde | Menos de 15% | Despachar |
| ⚪ Sin dato | Sin registro en Dropi, o no se pudo leer | Decirlo, no asumir |

**Con márgenes sanos casi ningún pedido conviene rechazar.** Con el margen real de Golden
(~$47.000 sobre un ticket de ~$103.000), incluso un cliente que devuelve la mitad de las veces deja
plata. La palanca no es rechazar: es **confirmar antes de despachar**, que sube `p` y cuesta un
mensaje.

## Umbrales que hay que revisar con datos nuevos

Estos son los que se calibraron el 2026-08-01. Si un export nuevo los contradice, se cambian aquí:

- Pesos bayesianos `10` (global) y `3` (por transportadora).
- Piso de 3 puntos y umbral de $1.500 en prepago.
- Fracción de retorno por transportadora (`COSTO-RETORNO.json`).
- El flete escala con la cantidad: ×0,97 a 1 unidad, ×1,07 a 2, ×1,27 a 3, ×1,29 a 4 — medido
  contra la tabla de 1 unidad. Solo aplica cuando no hay cotización en vivo.
