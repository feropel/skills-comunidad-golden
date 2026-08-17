# Trampas

Cada una de estas ya produjo un dato falso o una recomendación que habría costado plata. Están aquí
para no repetirlas.

## 1 · El modal de huella se queda en caché

Abrir el siguiente antes de que cargue devuelve la huella del cliente anterior, y se ve válida.
**Reportó que una clienta tenía 33 pedidos cuando tenía 5.**

→ Verificar que el teléfono del modal, **en su posición exacta**, sea el de la fila.

## 2 · El verificador que se valida solo

El primer chequeo buscaba el teléfono de la fila en todo el `innerText` de la página. Como la tabla
también contiene ese teléfono, **siempre daba positivo** y dejó pasar dos huellas contaminadas.

→ Comparar contra la cuarta línea del bloque del modal, no contra el texto de la página.

## 3 · Recomendar sacar un pedido de su oficina de retiro

Cuatro pedidos decían "Oficina InterRapidísimo" y se recomendó cambiarlos a otra transportadora.
**Habrían sido cuatro devoluciones seguras.**

→ Leer la dirección **antes** de proponer cualquier cambio de transportadora.

## 4 · Decidir con la tabla de fletes en vez de la cotización en vivo

La tabla de barrido es de un momento, de una unidad y con recaudo. **El flete escala con la
cantidad** (+7% a 2 unidades, +27% a 3) y baja sin recaudo.

→ La tabla prioriza; la cotización en vivo decide.

## 5 · Construir una regla sobre un solo caso

Se asumió que Coordinadora y Veloces no cobran el retorno porque en un caso de cada una salió $0.
Eso infló su valor esperado y produjo **cuatro recomendaciones equivocadas**.

→ Fracción de retorno solo con confianza alta o media; para el resto, asumir 1,00.

## 6 · Un umbral que ignoraba evidencia buena

La huella por transportadora solo contaba con 4 o más envíos. Un cliente con **3 de 3** con la
transportadora más barata quedaba fuera y se recomendaba una más cara.

→ Pesa desde el primer envío, con corrección bayesiana.

## 7 · Creerle a la cotización sobre la cobertura real

Dropi cotizaba Coordinadora a La Hormiga con precio y todo. **La bodega la rechazó igual.**
El veto vive en la bodega, no en Dropi, y ningún dato de Dropi lo revela.

→ Cruzar contra `RECHAZOS-FULFILLMENT.json` antes de recomendar.

## 8 · Agrupar por ID de orden

**Dropi le cambia el ID a la orden cuando se edita.** Agrupar historial o buscar un pedido por ID
falla justo después de hacer un cambio.

→ El teléfono es la llave. Va en todos los informes, al lado del ID.

## 9 · Un pedido que califica bien y aun así es devolución

Cliente sin historial malo, flete razonable, transportadora correcta… y el cliente ya había pedido
lo mismo tres días antes por el mismo valor.

→ Duplicados **primero**, antes de calificar cualquier otra cosa.

## 10 · Contar sin paginar

`Mostrar 10` con 32 pedidos en la cola da un conteo falso y un "no hay más" que es mentira.

→ `Mostrar 500` y **comprobar que `Siguiente` quedó deshabilitado** antes de afirmar un total.

## 11 · Timers congelados en segundo plano

Con la pestaña atrás, Chrome frena `setTimeout` y el proceso parece colgado cuando solo está
estrangulado. Se perdieron varios intentos diagnosticando el problema equivocado.

→ Reloj con `MessageChannel`, lotes cortos, y consultar el progreso en vez de asumir que murió.

## 12 · Mapear por índice después de recargar

El orden de las filas puede cambiar entre cargas. Mapear `filas[i]` contra una lista guardada
asigna la huella de un cliente a otro pedido.

→ Releer el ID de cada fila en vivo.

## 13 · Recomendar una transportadora que la bodega nunca ha usado

Dropi cotiza diez empresas. **Suppli solo ha generado guías con cuatro**, y Coordinadora es apenas
el 3% de ellas. Se recomendaron siete cambios a Coordinadora apoyados en datos de plataforma, y la
bodega rechazó dos en cinco días. Estuve a punto de recomendar Domina y TCC, con **cero guías** en
toda la historia de la cuenta.

→ Contar guías generadas por transportadora en el export **antes** de calcular nada. Lo que la
bodega no ha despachado nunca, no se recomienda aunque gane el cálculo.
