# Cómo sacar la cola y las huellas del panel de Dropi

## Por qué no hay API

El panel pide los pedidos a `GET https://api.dropi.co/api/orders/myorders/v2` (host `api.dropi.co`,
**no** `api-v2`) con params `status`, `from`, `until`, `result_number`, `start`, `textToSearch`,
`filter_date_by`, `supplier_id`, `tag_id`, `warranty`, `seller`, `invoiced`, `exportAs`. Manda tres
cabeceras: `X-Authorization`, **`x-captcha-token`** y `Accept`.

Ningún token de `localStorage` sirve para esa ruta (`401 Token is Invalid`; el token real vive en
memoria del Angular). Y **replicar el `x-captcha-token` sería saltarse la detección de bots: no se
hace.** La vía limpia es manejar la interfaz, que genera sus propias credenciales.

La calculadora de fletes `api-v2.dropi.co/logistic/freight-calculator` sí acepta el `DROPI_token`
de localStorage, pero suele responder `Token is Expired` — se refresca al iniciar sesión.

## Traer la cola

1. `app.dropi.co/dashboard/orders`
2. Botón verde de filtro → `Estado` → seleccionar `PENDIENTE CONFIRMACION` y `PENDIENTE` → `Ok`
3. `Mostrar` = 500
4. **Verificar que el botón `Siguiente` quedó deshabilitado.** Un conteo sin paginar es falso.

Columnas útiles de la tabla: `td[1]` orden, `td[2]` fecha, `td[3]` cliente + dirección + `Tel:`,
`td[4]` estatus, `td[5]` transportadora, `td[6]` tipo de envío. El nombre del producto y la bodega
solo aparecen en el `innerText` de la fila, no en un `td` propio. **El valor del pedido no está en
la tabla**: sale del export o de la cotización.

## Traer la huella del cliente

Cada fila trae `span.buyer-history-icon`. Al hacer click abre "Historial del comprador" con:
tipo de comprador, teléfono, total de pedidos, **en tu tienda vs en otras tiendas**, probabilidad
de entrega, entregadas y devoluciones con %, y el desglose **por transportadora**, por tipo de
envío y por rango de precio. También existe el estado "Sin registro · Este cliente no ha realizado
órdenes en Dropi", que se lee del texto de la fila sin abrir nada.

### La verificación obligatoria

**El modal se queda en caché.** Si se abre el siguiente antes de que cargue, devuelve la huella del
cliente anterior y se ve perfectamente válida.

Verificar comparando el teléfono **en su posición exacta dentro del modal** (la cuarta línea del
bloque que empieza en "Historial del comprador"), NO buscándolo en todo el texto de la página: el
teléfono de la fila también está en la tabla, así que un `includes()` sobre el body se valida solo
y deja pasar la contaminación.

```js
const t = document.body.innerText, k = t.indexOf('Historial del comprador');
const seg = t.slice(k, k+3000);
const telModal = seg.split('\n').map(s=>s.trim())[3];
if (telModal === telDeLaFila) { /* recién ahora es válida */ }
```

Al terminar, **auditar el lote completo** con esa misma comparación antes de usar los datos.

## Trampas técnicas del navegador

- **Timers estrangulados.** Con la pestaña en segundo plano Chrome frena `setTimeout` y un lote de
  30 modales tarda una eternidad o parece colgado. Usar un reloj que no dependa de timers:
  ```js
  const tick = () => new Promise(r => { const c = new MessageChannel(); c.port1.onmessage = () => r(); c.port2.postMessage(0); });
  const wait = async ms => { const end = Date.now()+ms; while (Date.now() < end) await tick(); };
  ```
- **Lotes cortos.** Cada modal tarda 3-6 s. Ir de 3 a 5 por llamada; un lote largo revienta el
  timeout de la herramienta aunque el JavaScript siga corriendo (se puede consultar el progreso).
- **La página no siempre hace scroll** en este contexto, y `scrollTop` se queda en 0. No depender de
  scroll para llegar a las filas de abajo: el click sintético funciona igual.
- **El orden de las filas puede cambiar entre cargas.** Nunca mapear por índice después de recargar:
  releer el ID de la fila en vivo.

## Cotizar en vivo

`Editar Orden` (ícono de persona con lápiz) → bajar a `Seleccione una transportadora`. Tarda unos
segundos en cotizar; hay que esperar a que aparezcan precios y no quedarse con
"Para cotizar, selecciona ciudad de destino".

Da el precio real por empresa **y el motivo exacto cuando no hay cobertura**:
"no se tiene configurada tarifa de Cali a X", "la ciudad de destino X no tiene habilitado el método
de envío CON RECAUDO", "no se encontró la ciudad de operación con el código …".

El resumen de la orden trae además `Total a recaudar`, `Precio proveedor`, `Precio de envío`,
`Comisión de la plataforma` y `Ganancias`.

**Salir SIN guardar:** `Cancelar`, y otra vez `Cancelar` en el "Estás seguro de cancelar?".
Son dos clics. Si algo queda trabado, recargar la página descarta sin guardar.

## De la cosecha a los archivos que leen los scripts

La cosecha del navegador (`scripts/huellas-consola.js` → `descargar()` → `huellas-dropi.json`)
trae el TEXTO crudo de cada modal. Antes de calificar hay que transcribirlo a un `.psv` en
`DROPI-LOGISTICA/datos/huellas/` (separador `|`, un pedido por fila, `calificar.py` y
`decidir_vivo.py` toman el más reciente). Cabecera real (tomada de una corrida en vivo):

```
orden|tel|cliente|destino|transp|recaudo|direccion|dropi_norm|tipo|total|prob|entP|devP|por_transportadora
```

Los scripts leen por NOMBRE de columna (`csv.DictReader`), así que el orden no importa, pero estas
son obligatorias: `orden` (ID de la fila), `tipo` (tipo de comprador), `total` (pedidos en Dropi),
`entP`/`devP` (% entregadas y devueltas), `prob` (probabilidad que pinta Dropi) y
`por_transportadora` = desglose `EMPRESA:entregadas/devoluciones` separado por `;`
(ej. `ENVIA:10/3;VELOCES:5/0`). Sin registro → `total=0` y el resto vacío. Las demás columnas
(cliente, destino, transp, recaudo, direccion) son contexto para leer el informe a ojo.

Las cotizaciones del Paso 5 se registran a mano en `DROPI-LOGISTICA/datos/COTIZACIONES-VIVO.json`
con esta forma (solo las empresas que SÍ cotizaron; la que no tiene cobertura no se anota):

```json
{ "84309999": { "ENVIA": 12900, "INTERRAPIDISIMO": 14200 } }
```

## El export de órdenes

Reportes → Descargas. Dos archivos, y hacen falta los dos:

- **órdenes** — trae `VALOR DE COMPRA EN PRODUCTOS` (el ticket), `PRECIO FLETE`,
  `COSTO DEVOLUCION FLETE`, `COMISION`, `TOTAL EN PRECIOS DE PROVEEDOR` (el costo), `ESTATUS`,
  `TIPO DE ENVIO`, `DIRECCION`, `TELÉFONO`, `NOTAS`.
- **órdenes con productos** — una fila por producto: `CANTIDAD`, `PRECIO PROVEEDOR`, `VARIACION`.

Ojo: `VALOR FACTURADO` viene vacío mientras no haya factura; el ticket es
`VALOR DE COMPRA EN PRODUCTOS`.
