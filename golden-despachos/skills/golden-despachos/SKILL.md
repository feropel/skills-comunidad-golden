---
name: golden-despachos
description: >-
  Golden Group — CALIFICACIÓN DE PEDIDOS ANTES DE DESPACHAR (Dropi, COD y prepago). Toma la
  cola en PENDIENTE CONFIRMACION y PENDIENTE y, antes de que se genere la guía, dictamina
  uno por uno: si está DUPLICADO, si la DIRECCIÓN permite entregar, qué dice la HUELLA del
  cliente en Dropi (incluida su historia con cada transportadora), si la bodega VETÓ esa
  transportadora, y cuál conviene por balance de precio y efectividad real. Entrega semáforo
  por pedido, la transportadora recomendada con la plata que gana o pierde, y el mensaje
  exacto para pedirle al cliente lo que falta. NO ejecuta: recomienda y el usuario aprueba.
  Úsala SIEMPRE que el usuario quiera: "revisa los pendientes", "califica estos pedidos",
  "qué cambio antes de despachar", "cuál transportadora le pongo", "este cliente sirve",
  "analiza las direcciones", "hay pedidos duplicados", "me rechazaron un pedido", "por dónde
  mando este envío", o suba un export de órdenes de Dropi. Novedades ya
  despachadas: golden-logistica.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 944 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden Despachos — calificar antes de que se genere la guía

<!-- skill GD1.8 · auditoría golden-skill-auditor: la description no decía a dónde derivar las
     novedades ya trabadas (rúbrica, dimensión Activación — "dice cuándo NO usarla / a qué skill
     hermana derivar"), aunque el cuerpo ("## Fronteras y desambiguación") sí lo tenía por completo.
     Un pedido de novedades logísticas podía competir entre golden-despachos y golden-logistica sin
     que el disparador mismo marcara la frontera. Se agregó "Novedades ya despachadas:
     golden-logistica." al final de la description (944 → 988 de 1024, sigue con margen). Nada se
     quitó: los disparadores existentes quedaron intactos. Resto de la auditoría (inventario.sh,
     validar_arsenal.py, las tres autopruebas de scripts/) en verde sin cambios: 0 referencias rotas,
     0 huérfanos, sintaxis OK, sin secretos, blindaje 15/15 con chflags uchg. -->
<!-- skill GD1.7 · auditoría golden-skill-auditor (verificado EJECUTANDO, no leyendo):
     `scripts/calificar.py` moria con traceback crudo si faltaba `datos/FLETES-CALI.json`
     (linea sin try/except, a diferencia de COSTO-RETORNO y TRANSPORTADORAS-OPERATIVAS, que si
     lo tenian) — reproducido con DROPI_DATA apuntando a una carpeta vacia. `scripts/decidir_vivo.py`
     tenia la MISMA clase de hueco en TRES puntos: `datos/COTIZACIONES-VIVO.json`,
     `datos/RECHAZOS-FULFILLMENT.json` (este SI estaba guardado en calificar.py — la duplicacion
     entre los dos scripts habia desincronizado el guardia) y `salidas/salida-v3.json`. Los cuatro
     ahora terminan con `sys.exit` (o aviso + lista vacia, igual que su gemelo en calificar.py) y
     el nombre exacto de lo que falta, nunca un traceback. Verificado reproduciendo los cuatro
     casos antes (traceback) y despues (mensaje) del arreglo, y regresion contra los datos reales
     de Golden (895 ordenes, direcciones.py, duplicados.py y las tres autopruebas siguen en verde). -->
<!-- skill GD1.6 · las DIRECCIONES entran por su propia puerta (scripts/direcciones.py) con banco en los DOS sentidos, 27 casos. Se midio contra las 895 direcciones reales del export: 12 estaban mal clasificadas (1,3%) porque el detector acusaba el LENGUAJE y no el defecto — la palabra 'oficina' bloqueaba la oficina PROPIA del cliente, las nomenclaturas de DOS letras (# 100 AB - 03, # 65 GG - 22, # 23AN-45) salian INCOMPLETA, y a las veredas se les pedia numero de puerta. Nuevo estado RURAL. Las tres correcciones se vieron morder bajo sabotaje, y un caso del banco resulto DECORATIVO (no alcanzaba la rama que decia guardar): se reemplazo por uno que si la alcanza. -->
<!-- skill GD1.5 · la efectividad entra por UNA puerta (scripts/efectividad.py): cascada municipio/departamento/nacional SIN umbral, con muestra_envios y fuente_efectividad en el informe, y GUARDIA DE PROCEDENCIA que descarta el archivo sin _fuente (EFECTIVIDAD-PLATAFORMA.json tenia Envia 95,51% contra 81,09% real y decidia mal: la recomendacion #1 cambiaba de transportadora) · duplicados distingue FANTASMA de duplicado (editar cambia el id) y los cuatro estados terminales por igualdad exacta · COSTO-RETORNO por negocio con DROPI_NEGOCIO · dos bancos de autoprueba, ambos vistos morder bajo sabotaje -->
<!-- skill GD1.4 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
<!-- skill GD1.3 · auditoría golden-skill-auditor: decidir_vivo.py NO tenía rama prepago (calificaba TODOS los pedidos, prepago incluido, con el valor esperado de contra entrega — retorno y probabilidad de devolución que un prepago nunca paga; contradecía criterios-decision.md, que manda el precio en prepago). Ahora replica la lógica de calificar.py: descarta candidatas a más de 3 puntos de la mejor efectividad, elige la más barata salvo excepción de $1.500, retorno en cero, y la columna GANA reporta ahorro de flete (no valor esperado) para prepago. De paso: filtro explícito de HABILITADAS (antes solo vivía en calificar.py; Servientrega y otras no habilitadas podían colarse si alguna vez cotizaban), y se quitó un bucle muerto (`for c in x['cands']: pass`). CHANGELOG.md se movió a `references/changelog.md` (vivía suelto en la raíz: material que se publicaría tal cual al marketplace). Probado con fixtures sintéticos (un pedido prepago, uno contra entrega) contra el propio script: confirmado el cambio de comportamiento antes→después. -->
<!-- skill GD1.2 · auditoría: los scripts aplican por fin el filtro de TRANSPORTADORAS-OPERATIVAS.json (la regla GD1.1 vivía solo en prosa; la corrida de prueba reprodujo el total equivocado) · retorno leído de COSTO-RETORNO.json por confianza (trampa 5) · scripts portables (DROPI_DATA + export por argumento/variable/Escritorio) · pipeline documentado (.psv de huellas y COTIZACIONES-VIVO.json) · frontera con golden-chatea-pro-validacion-direcciones también en el description · changelog deduplicado y dato de cliente anonimizado -->
<!-- skill GD1.1 · TRANSPORTADORAS-OPERATIVAS.json se antepone a todo cálculo; el protocolo de rechazo mira el patrón acumulado -->
<!-- skill GD1.0 · creación: seis criterios en orden, protocolo de rechazo, huella por transportadora, prepago por precio, duplicados, teléfono junto al ID -->

**Versión** `GD1.8` · Fábrica: chat «✅ SKILL golden-despachos» · Historial detallado en
`references/changelog.md`.

En contra entrega la plata no se pierde en la venta, se pierde en el despacho. Un pedido mal
ruteado regala flete; una dirección incompleta regala una devolución completa; un duplicado regala
las dos cosas. **La ventana para arreglarlo se cierra cuando el pedido pasa a guía generada.**

## ⚙️ Antes de correr los scripts (una sola vez)

**Dependencia:** los scripts leen Excel, así que necesitan `openpyxl`. Sin él el error es
críptico (`ModuleNotFoundError`) y parece que la skill está rota cuando solo falta un paquete:

```bash
pip3 install openpyxl
```

**Los dos export de Dropi.** Se bajan de *Dropi > Órdenes > Exportar* y son **dos archivos**
(órdenes y órdenes-productos). Los scripts los encuentran solos si están en el Escritorio; si no,
se pasan por argumento o por variable de entorno:

```bash
python3 scripts/calificar.py <ordenes.xlsx> <ordenes_productos.xlsx>
```

Si faltan, el script lo dice con el nombre exacto de lo que espera — no falla en silencio.

**Dónde buscan el cerebro.** Los scripts localizan la carpeta de datos por la variable
`DROPI_DATA`; sin ella asumen `~/DROPI-LOGISTICA`. Si la carpeta vive en otra ruta (en el Mac de
Golden vive dentro de `PROYECTOS/`), exportarla una vez antes de correr:

```bash
export DROPI_DATA="/ruta/a/DROPI-LOGISTICA"
```

Si la ruta no existe, los scripts se detienen con ese mismo mensaje en vez de reventar con un
traceback.

## Dónde viven los datos

**El método está aquí; los datos viven en
`~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/🌐 PROYECTOS/DROPI-LOGISTICA/`.**
Esa carpeta es el activo que crece: registro de rechazos de la bodega, efectividad propia, costo
real de retorno, fletes, huellas ya consultadas. Tiene `git`, así que cada corrida deja historial.
Léela SIEMPRE al empezar y **escríbele al terminar**. Su `README.md` explica cada archivo.

## Regla de oro

**Nunca recomendar ni ejecutar sin haber mirado los seis criterios, y en este orden.** Los tres
primeros bloquean: si uno se dispara, no importa lo bien que califiquen los otros tres.

1. **Duplicado** — este cliente ya pidió esto mismo?
2. **Dirección** — un mensajero puede llegar sin llamar?
3. **Veto de bodega** — la bodega despacha por esa transportadora, y a ese destino?
   Se consulta `TRANSPORTADORAS-OPERATIVAS.json` **antes** que cualquier cálculo de precio:
   Dropi cotiza diez empresas y la bodega puede estar despachando solo por tres o cuatro.
   **Recomendar una que la bodega nunca ha usado es recomendar un rechazo.**
4. **Huella del cliente** — cómo le ha ido a ESTE cliente, y con CADA transportadora?
5. **Precio del flete** — el real, cotizado en vivo.
6. **Efectividad** — de la zona y, sobre todo, de ese cliente con esa transportadora.

## El proceso

### Paso 0 · Cargar el cerebro
Leer de `DROPI-LOGISTICA/datos/`: **`TRANSPORTADORAS-OPERATIVAS.json` primero**,
`RECHAZOS-FULFILLMENT.json`, `EFECTIVIDAD-PROPIA.json`, y los fletes (`FLETES-CALI.json`).

**La efectividad entra por UNA sola puerta: `scripts/efectividad.py`.** No se lee un archivo de
efectividad a mano. Ese módulo resuelve la cascada **municipio → departamento → nacional SIN
umbral** (orden de FER: si el municipio tiene un envío, ese es el dato) y devuelve siempre
`muestra_envios` y `fuente_efectividad`, que el informe imprime. Trae además una **guardia de
procedencia**: un archivo sin `_fuente` ni `_nota` se descarta con aviso y no entra al cálculo.
Nació de un caso real: `EFECTIVIDAD-PLATAFORMA.json` vivió semanas dentro de la fórmula con Envía
al 95,51% cuando la Torre madura da 76-81%, y nadie lo vio porque el número no traía de dónde
salía. Se prueba sola con `python3 scripts/efectividad.py --autoprueba` (6 casos, guardia incluida).

**El costo de retorno es de ESTA empresa, no se hereda.** Se prefiere `COSTO-RETORNO-<NEGOCIO>.json`
declarando `DROPI_NEGOCIO=GOLDEN`; sin esa variable cae al genérico y lo dice en el informe.

Si el usuario trae un export nuevo de Dropi, **recalcular efectividad propia y costo de retorno con
él** antes de decidir.

### Paso 1 · Traer la cola
Del panel de Dropi (`app.dropi.co/dashboard/orders`), filtro Estado = `PENDIENTE CONFIRMACION` y
`PENDIENTE`, `Mostrar 500`, y **confirmar que la paginación quedó cerrada** — un conteo sin paginar
es falso. El método de captura y sus trampas están en `references/captura-panel.md`.

### Paso 2 · Duplicados y órdenes fantasma
`python3 scripts/duplicados.py <export.xlsx>`. Cruza por teléfono y por nombre+dirección contra
TODOS los pedidos no anulados, no solo los pendientes. Nunca cancelar solo: **se le pregunta al
cliente si quiere un segundo producto o si fue un error.**

Distingue **duplicado** de **fantasma**, que no es lo mismo y confundirlos hace preguntarle al
cliente por un pedido que nunca hizo. Niveles: `EDICION` (sospecha de fantasma), `CRITICO`, `ALTO`,
`MEDIO`, `VIGILAR`. **Un cero se prueba, no se cree**: el script reporta el universo ("0 alertas
sobre N órdenes, M pendientes") y trae banco sembrado, `python3 scripts/duplicados.py --autoprueba`
(7 casos, con los falsos positivos que NO deben saltar).

### Paso 3 · Direcciones
**Entran por UNA sola puerta: `scripts/direcciones.py`.** Criterio en
`references/direcciones-colombia.md`. Salidas posibles: `OK`, `INCOMPLETA` (no despachar),
`REVISAR` (verificar antes), `RURAL` (vereda o kilómetro: se pide punto de referencia, **nunca**
número de puerta), `OFICINA` (bloquea la transportadora) y `BLOQUEO` (retiro en punto no
habilitado). Por cada problema, **entregar la pregunta exacta al cliente** en la plantilla del
país: trato de usted, una sola pregunta, sin saludo, sin explicaciones.

**Este detector acusa el LENGUAJE de la dirección, no el defecto, así que se prueba en los dos
sentidos** (`python3 scripts/direcciones.py --autoprueba`, 27 casos: 14 que deben morder y 13 que
NO). Medido sobre las 895 direcciones del export, tres clases estaban al revés: la palabra
«oficina» bloqueaba la oficina PROPIA del cliente, las nomenclaturas de dos letras
(`# 100 AB - 03`, `# 65 GG - 22`, `# 23AN-45`) salían incompletas, y a las veredas se les pedía un
número de puerta que allí no existe.

### Paso 4 · Huella del cliente
Del panel, ícono `.buyer-history-icon` en cada fila. Da tipo de comprador, total, **en tu tienda vs
en otras**, probabilidad de entrega, % entregadas y devueltas, y **el desglose por transportadora**,
que es el dato más valioso de todos. **Verificar SIEMPRE que el teléfono del modal sea el de la
fila**, o se cuela la huella del cliente anterior. La cosecha se hace pegando
`scripts/huellas-consola.js` en la consola del navegador (trae la verificación incorporada) y el
resultado se transcribe al `.psv` de `datos/huellas/` — formato y método en
`references/captura-panel.md`.

### Paso 5 · Cotizar en vivo
`Editar Orden` → `Seleccione una transportadora`. Da el precio real de ese pedido y **dice quién no
tiene cobertura**. Se cierra con `Cancelar` y otra vez `Cancelar` en la confirmación: no guarda
nada. La tabla de fletes en disco sirve para priorizar; **la decisión se toma con la cotización en
vivo**.

### Paso 6 · Decidir
El cálculo masivo del lote lo hace `scripts/calificar.py` (usa la tabla de fletes como prior y
produce `salidas/salida-v3.json`); la decisión final la hace `scripts/decidir_vivo.py`, que
re-decide con los precios reales de `datos/COTIZACIONES-VIVO.json` capturados en el Paso 5.
La fórmula completa, los pesos y los umbrales están en `references/criterios-decision.md`.
En corto:
- **Prepago (SIN RECAUDO): manda el precio.** El cliente ya pagó y se entrega. La más barata,
  descartando las que estén a más de 3 puntos de efectividad de la mejor, y si una con mejor
  entrega cuesta menos de $1.500 más, se prefiere esa.
- **Contra entrega: manda el valor esperado.** `p × (ticket − costo − flete) − (1−p) × (flete +
  retorno)`, donde `p` sale de la efectividad de la zona **corregida por la historia de ese cliente
  con esa transportadora**, y `retorno` es el costo medido de esa empresa.

### Paso 7 · Entregar
Informe priorizado con, por cada pedido: **ID y TELÉFONO** (el ID cambia cuando se edita la orden;
el teléfono no), semáforo, problema si lo hay, transportadora actual y recomendada con ambos
fletes, la plata que gana, y la acción concreta. Separar **ahorro de flete** (plata inmediata) de
**valor esperado** (probabilístico): no son lo mismo y confundirlos infla la cifra.

### Paso 8 · Cerrar el ciclo
Escribir en `DROPI-LOGISTICA/`: cotizaciones de la corrida, huellas nuevas, y `git commit`.
Si el usuario reporta un rechazo de la bodega, **ver el protocolo de abajo antes de registrarlo**.

## Protocolo de rechazo de bodega

Cuando el usuario diga "me rechazaron este pedido por X transportadora":

1. **Consultar la Torre Logística** por `scripts/efectividad.py` (municipio primero, luego
   departamento): esa transportadora opera en ese destino para el resto de la plataforma? con
   cuántos envíos y qué efectividad? La respuesta trae `muestra_envios`, así que se ve si el
   número se apoya en miles de envíos o en tres.
2. **Consultar la cotización**: Dropi la cotiza en ese municipio y en los vecinos?
3. **Dictaminar el alcance:**
   - Si funciona bien en la zona para todos → **es una restricción de la bodega**, alcance
     `CIUDAD`, y decirle al usuario que solo la bodega puede confirmar si aplica a todo el
     departamento. Sugerir preguntárselo.
   - Si tampoco opera ahí en la plataforma → es general, alcance `DEPARTAMENTO` o `NACIONAL`.
4. **Registrar** en `RECHAZOS-FULFILLMENT.json` con fecha, orden, alcance y alternativa usada, y
   `git commit`. A partir de ahí esa combinación no vuelve a salir recomendada.
5. **Mirar el patrón, no solo el caso.** Si la misma transportadora acumula rechazos, contar sus
   guías generadas en el export: puede que la bodega apenas la use. Dos rechazos sobre siete guías
   no es mala suerte, es que esa empresa no es de las suyas.

## Reglas duras

- **Datos reales siempre.** Jamás inventar un flete, una efectividad ni una huella. Lo que no se
  pudo obtener se marca como no obtenido y se dice cuál pedido quedó sin cubrir.
- **Verificar antes de afirmar.** Dos huellas idénticas, un cero, un "no hay cobertura": todos se
  comprueban antes de escribirlos. Ver `references/trampas.md`, que existe porque cada trampa de esa
  lista ya produjo un dato falso.
- **Separar evidencia fuerte de evidencia delgada.** Una recomendación que se apoya en uno o dos
  envíos se marca como tal y, si implica pagar más, no se recomienda.
- **No ejecutar.** Esta skill recomienda; el usuario cambia y aprueba en el panel. Abrir `Editar
  Orden` para leer la cotización es lectura; salir siempre por `Cancelar`.
- **La clave de identidad es (teléfono, ID de orden).** El teléfono manda para agrupar; el ID
  distingue pedido de pedido. Agrupar solo por ID pierde al cliente cuando Dropi le cambia el ID al
  editar; agrupar solo por teléfono borra del radar al comprador recurrente con una orden nueva viva.
- **Editar una orden le cambia el ID, y la vieja sigue en el export ya descargado.** Esa venta
  aparece dos veces. El discriminador autoritativo es el DETALLE, no el listado:
  `GET /integrations/orders/myorders/{id}` sobre la vieja responde `"Orden no encontrada"`, mientras
  que una real, incluso CANCELADA, responde `isSuccess:true`.
- **Cuatro estados terminales: ENTREGADO, DEVOLUCIÓN, CANCELADO, RECHAZADO** — y son terminales de
  ESA orden, no del cliente. `ENTREGADO A TRANSPORTADORA` **no** es una venta: es entrega al courier
  y la plata no ha entrado, así que los estados se comparan por igualdad exacta, nunca por substring.
- **Un dato medido caduca.** Si otro puede escribir mientras tanto, se relee en el momento de usarlo,
  no en el de reportarlo. Y una operación que devolvió error puede haberse ejecutado igual: se relee
  el estado, nunca se reintenta a ciegas.

## Encadenado al ecosistema

- **Recibe de:** el panel de Dropi y los exports de órdenes del usuario.
- **Entrega a:** `golden-logistica` (lo que se traba después pasa a rescate de novedades),
  `golden-ads` (la efectividad real alimenta el breakeven COD) y al P&L del usuario.
- **Comparte reglas con:** `golden-chatea-pro-validacion-direcciones` (el estándar preventivo de
  direcciones por país nace ahí; aquí se aplica a pedidos ya creados).

## Referencias

- `references/captura-panel.md` — cómo sacar la cola y las huellas del panel, y las trampas técnicas.
- `references/criterios-decision.md` — la fórmula, los pesos, los umbrales y por qué son esos.
- `references/direcciones-colombia.md` — qué hace entregable una dirección y qué preguntar cuando no.
- `references/trampas.md` — los errores que ya se cometieron, para no repetirlos.

Los scripts se prueban solos, y un validador que no se ha visto morder no vale:

```bash
python3 scripts/efectividad.py --autoprueba   # 6 casos: guardia, cascada, sin umbral
python3 scripts/duplicados.py  --autoprueba   # 7 casos: fantasma, duplicado real, falsos positivos
python3 scripts/direcciones.py --autoprueba   # 27 casos: 14 que muerden y 13 que NO deben morder
```

## Auto-mejora

Al cerrar cada corrida, esta skill **se autocalifica** sobre 100 contra estos seis criterios y
registra el resultado en el changelog:

| Criterio | Vale |
|---|---|
| Cubrió TODA la cola y lo demostró (paginación verificada) | 20 |
| Cero datos inventados; lo no obtenido quedó marcado | 20 |
| Los seis criterios aplicados en orden, con los bloqueantes primero | 20 |
| Decisión con cotización en vivo, no con tabla vieja | 15 |
| Evidencia fuerte separada de la delgada | 15 |
| El cerebro quedó actualizado y commiteado | 10 |

Si algo baja de 90, **arreglarlo en la misma corrida** con el ritual de fábrica (backup →
`chflags -R nouchg` → editar → subir versión y changelog → `chflags -R uchg`). Toda lección nueva
—una trampa, un umbral que falló, un criterio que faltaba— se hornea en `references/` antes de
cerrar. Auditoría periódica con `golden-skill-auditor`.

El historial de versiones vive en `references/changelog.md` (una sola fuente: aquí solo el
comentario de versión bajo el título, para no desincronizar dos changelogs).

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — CALIFICACIÓN DE PEDIDOS ANTES DE DESPACHAR (Dropi · COD y prepago). Toma la cola de pedidos en PENDIENTE CONFIRMACION y PENDIENTE, y antes de que se genere la guía dictamina uno por uno: si está DUPLICADO, si la DIRECCIÓN permite entregar, qué dice la HUELLA del cliente en Dropi (incluida su historia con cada transportadora), si la bodega VETÓ esa transportadora, y cuál transportadora conviene por balance de precio y efectividad real. Entrega semáforo por pedido, la transportadora recomendada con la plata que gana o pierde, y el mensaje exacto para pedirle al cliente lo que falta. NO ejecuta: recomienda y el usuario aprueba. Úsala SIEMPRE que el usuario quiera: "revisa los pendientes", "califica estos pedidos", "qué cambio antes de despachar", "cuál transportadora le pongo", "este cliente sirve", "analiza las direcciones", "hay pedidos duplicados", "me rechazaron un pedido", "por dónde mando este envío", o suba un export de órdenes de Dropi. Dispara aunque no diga "calificar": basta con pedidos pendientes, elección de transportadora, riesgo de devolución o direcciones malas. Fronteras: novedades ya trabadas → golden-logistica (lo reactivo); esta es la PREVENTIVA, decidir antes de que salga el paquete. Dirección que el bot recoge en WhatsApp → golden-chatea-pro-validacion-direcciones; aquí se auditan pedidos YA creados en Dropi.

