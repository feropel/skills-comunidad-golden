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

## 14 · Un detector de patrones acusa el lenguaje, no el defecto

`analiza_dir` marcaba `BLOQUEO` cualquier dirección con la palabra **oficina**, aunque fuera la
oficina propia del cliente con nomenclatura completa (`Calle 17 # 2E-30 oficina EMNFC SAS`). Daba
`INCOMPLETA` a las nomenclaturas de **dos letras** (`# 100 AB - 03`, `# 65 GG - 22`, `# 23AN-45`),
que son normales en Medellín, Bogotá y el norte de Cali, porque el patrón admitía una sola letra. Y
le pedía **número de puerta a una vereda**, donde no existe ni existirá.

Doce direcciones de 895 (1,3%) mal clasificadas, todas en el sentido que nadie había probado: el de
los casos BUENOS. Un banco que solo verifica que el detector muerda mide la mitad del detector.

→ Todo detector de patrones se prueba en los **dos sentidos**: los casos que debe morder y los que
debe dejar pasar, estos últimos tomados de datos reales. Y al escribir el caso hay que comprobar
que **alcance la rama** que dice proteger: uno de los casos de este mismo banco resultó decorativo
(la dirección traía puerta completa, así que la rama rural nunca se ejecutaba) y solo se descubrió
saboteando el código a propósito y viendo que el banco seguía en verde.

## 15 · Una exclusión correcta que no se declara no se distingue de un olvido

Diez sitios de esta skill descartaban datos en silencio (FILA P59 del Centro de Mando). El peor:
la transportadora **asignada** se buscaba DENTRO de las candidatas ya filtradas, así que si alguno
de los cinco filtros la había excluido, la columna ACTUAL imprimía un guion y la columna GANA decía
**«queda igual»** — sobre un pedido asignado a una transportadora que el fulfillment rechaza, o que
la bodega no ha usado nunca. El informe recomendaba no hacer nada justo en los pedidos que había que
corregir a la fuerza.

Y un `except Exception: continue` hacía que un `COSTO-RETORNO-<NEGOCIO>.json` roto cayera al
genérico sin una palabra: la LEY DE NO-HEREDAR se rompía en silencio, con el archivo correcto ahí
mismo en el disco.

→ Toda herramienta que **descarte** un dato del usuario tiene que **contarlo y nombrarlo** en su
salida, aunque el descarte sea obvio y correcto. Y cuando se descarta por varios motivos a la vez,
se reporta el que de verdad bloquea: decir «sin efectividad medida» de una transportadora vetada
esconde el veto.

## 16 · Un chequeo que busca en TODO el documento encuentra su propia respuesta

El verificador de integración de la trampa 15 comprobaba que la razón de la exclusión apareciera
con `razon in salida`, sobre el texto completo del informe. Pero el informe ya trae un resumen al
pie que nombra cada motivo, así que **quitar la razón de la fila del pedido no movía el veredicto**:
dos de los cinco sabotajes pasaron en verde. Es la misma trampa del modal de huellas (trampa 1),
cometida en el instrumento en vez de en el dato.

→ Un chequeo se acota al **sitio exacto** donde el dato debe aparecer: la fila del pedido y su línea
de continuación, no el documento entero. Si el sabotaje de lo que el caso dice cuidar no pone el
banco en rojo, el caso es decoración.
