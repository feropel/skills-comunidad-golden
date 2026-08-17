# Esquema de los exports de Dropi

Dropi exporta dos archivos por corte. El motor los distingue por sus columnas (no por el
nombre): si el encabezado contiene la columna `PRODUCTO`, es **por producto**; si tiene
`ESTATUS` + `ID` pero no `PRODUCTO`, es **por pedido**. Lee esto solo si un archivo no encaja
o Dropi cambió el formato.

## Archivo "por pedido" (típicamente 63 columnas) — una fila = una orden
Columnas clave que usa el motor:
- `ID` — identificador de la orden (para deduplicar y contar órdenes).
- `FECHA` — fecha de la orden (formato `dd-mm-aaaa`). Define el periodo.
- `ESTATUS` — estado de entrega (ver clasificación abajo).
- `TRANSPORTADORA`, `DEPARTAMENTO DESTINO`, `CIUDAD DESTINO` — logística.
- `NOMBRE CLIENTE`, `TELÉFONO`, `DIRECCION` — cliente.
- `GANANCIA`, `VALOR FACTURADO`, `PRECIO FLETE`, `COSTO DEVOLUCION FLETE` — dinero (nivel orden).
- `NOVEDAD` — causa de no-entrega cuando la hay.

## Archivo "por producto" (típicamente 53 columnas) — una fila = una línea de producto
Trae casi las mismas columnas de logística/cliente MÁS:
- `PRODUCTO`, `VARIACION`, `SKU`, `CANTIDAD` — el detalle de qué se vendió.
- `TOTAL DE LA ORDEN`, `PRECIO PROVEEDOR`, `PRECIO PROVEEDOR X CANTIDAD`.
Nota: el total de la orden se repite en cada línea del mismo pedido; por eso el dinero se suma
desde "por pedido", no desde aquí, para no doblar montos.

## Clasificación de ESTATUS
Dropi maneja decenas de estados. El motor los agrupa así:
- **entregado**: `ENTREGADO`.
- **devolucion**: cualquiera que contenga `DEVOLUC` (DEVOLUCION, DEVOLUCION EN BODEGA,
  EN PROCESO DE DEVOLUCION, TRANSITO A DEVOLUCION…) y `REEXPEDICION`.
- **cancelado**: `CANCELADO`, `RECHAZADO` (no llegaron a ruta → fuera del % de entrega).
- **transito**: todo lo demás (EN REPARTO, EN RUTA, NOVEDAD, BODEGA…, PENDIENTE) — resultado
  aún abierto, fuera del denominador.

El **% de entrega = entregado / (entregado + devolucion)**. Cancelados y en tránsito no cuentan
porque no son un resultado final de entrega.

## Multi-cuenta
Un negocio puede tener varias cuentas de Dropi (p. ej. cambió de cuenta al crecer). Cada cuenta
va en su subcarpeta bajo la carpeta base; el motor toma el nombre de la subcarpeta como nombre
de la cuenta y reporta cada una por separado y en el global. Los mismos IDs de orden no se
mezclan entre cuentas.

## Formato de fecha y moneda
- Fechas en `dd-mm-aaaa` o `dd/mm/aaaa`. El periodo (`YYYY-MM`) se toma del nombre del archivo
  si ya sigue la convención, o del dato (fecha mínima del archivo) si no.
- Montos en formato LatAm (punto = separador de miles, sin decimales para COP). El símbolo de
  moneda se fija en `_config_dropi.json` (`"currency"`).
