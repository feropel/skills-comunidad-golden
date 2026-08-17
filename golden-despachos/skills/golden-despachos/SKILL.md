---
name: golden-despachos
description: >
  Golden Group — CALIFICACIÓN DE PEDIDOS ANTES DE DESPACHAR (Dropi · COD y prepago). Toma la cola
  de pedidos en PENDIENTE CONFIRMACION y PENDIENTE, y antes de que se genere la guía dictamina uno
  por uno: si está DUPLICADO, si la DIRECCIÓN permite entregar, qué dice la HUELLA del cliente en
  Dropi (incluida su historia con cada transportadora), si la bodega VETÓ esa transportadora, y
  cuál transportadora conviene por balance de precio y efectividad real. Entrega semáforo por
  pedido, la transportadora recomendada con la plata que gana o pierde, y el mensaje exacto para
  pedirle al cliente lo que falta. NO ejecuta: recomienda y el usuario aprueba.
  Úsala SIEMPRE que el usuario quiera: "revisa los pendientes", "califica estos pedidos", "qué
  cambio antes de despachar", "cuál transportadora le pongo", "este cliente sirve", "analiza las
  direcciones", "hay pedidos duplicados", "me rechazaron un pedido", "por dónde mando este envío",
  o suba un export de órdenes de Dropi. Dispara aunque no diga "calificar": basta con pedidos
  pendientes, elección de transportadora, riesgo de devolución o direcciones malas.
  NO es el rescate de novedades ya trabadas (eso es golden-logistica, el lado reactivo); esta skill
  es el lado PREVENTIVO: decidir bien antes de que salga el paquete. Tampoco es la validación de la
  dirección mientras el bot la recoge en WhatsApp (eso es golden-chatea-pro-validacion-direcciones);
  aquí se auditan direcciones de pedidos YA creados en Dropi.
---

# Golden Despachos — calificar antes de que se genere la guía

<!-- skill GD1.2 · auditoría: los scripts aplican por fin el filtro de TRANSPORTADORAS-OPERATIVAS.json (la regla GD1.1 vivía solo en prosa; la corrida de prueba reprodujo el total equivocado) · retorno leído de COSTO-RETORNO.json por confianza (trampa 5) · scripts portables (DROPI_DATA + export por argumento/variable/Escritorio) · pipeline documentado (.psv de huellas y COTIZACIONES-VIVO.json) · frontera con golden-chatea-pro-validacion-direcciones también en el description · changelog deduplicado y dato de cliente anonimizado -->
<!-- skill GD1.1 · TRANSPORTADORAS-OPERATIVAS.json se antepone a todo cálculo; el protocolo de rechazo mira el patrón acumulado -->
<!-- skill GD1.0 · creación: seis criterios en orden, protocolo de rechazo, huella por transportadora, prepago por precio, duplicados, teléfono junto al ID -->

**Versión** `GD1.2` · Fábrica: chat «✅ SKILL golden-despachos» · Historial detallado en `CHANGELOG.md`.

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
`RECHAZOS-FULFILLMENT.json`, `EFECTIVIDAD-PROPIA.json`,
`COSTO-RETORNO.json`, `EFECTIVIDAD-PLATAFORMA.json`, `FLETES-CALI.json`. Si el usuario trae un
export nuevo de Dropi, **recalcular efectividad propia y costo de retorno con él** antes de decidir.

### Paso 1 · Traer la cola
Del panel de Dropi (`app.dropi.co/dashboard/orders`), filtro Estado = `PENDIENTE CONFIRMACION` y
`PENDIENTE`, `Mostrar 500`, y **confirmar que la paginación quedó cerrada** — un conteo sin paginar
es falso. El método de captura y sus trampas están en `references/captura-panel.md`.

### Paso 2 · Duplicados
`python3 scripts/duplicados.py <export.xlsx>`. Cruza por teléfono y por nombre+dirección contra
TODOS los pedidos no cancelados, no solo los pendientes. Nunca cancelar solo: **se le pregunta al
cliente si quiere un segundo producto o si fue un error.**

### Paso 3 · Direcciones
Aplicar `references/direcciones-colombia.md` a cada una. Salidas posibles: `OK`, `INCOMPLETA` (no
despachar), `REVISAR` (verificar antes), `OFICINA` (bloquea la transportadora), `BLOQUEO`
(transportadora no habilitada). Por cada problema, **entregar la pregunta exacta al cliente** en la
plantilla del país: trato de usted, una sola pregunta, sin saludo, sin explicaciones.

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

1. **Consultar la Torre Logística** (`EFECTIVIDAD-PLATAFORMA.json`): esa transportadora opera en
   ese departamento para el resto de la plataforma? con cuántos envíos y qué efectividad?
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
- **El teléfono manda sobre el ID.** Agrupar historial por ID es un error: Dropi lo cambia al editar.

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

El historial de versiones vive en `CHANGELOG.md` (una sola fuente: aquí solo el comentario de
versión bajo el título, para no desincronizar dos changelogs).
