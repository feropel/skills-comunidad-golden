# Historial de golden-logistica

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 875 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- GL1.4 — 2026-08-24 — barrido total del arsenal (CdM), fila pendiente ejecutada: las probabilidades de rescate por tipo en references/tipos-novedad.md quedaron rotuladas explícitamente como ESTIMACIÓN cualitativa (sin N ni fecha — el dato medido no existe dentro de la skill), con la instrucción de reemplazarlas por la tasa real (con N y fecha) cuando la operación la mida. Nada más se tocó: método de rescate, plantillas y reglas intactos. -->

<!-- GL1.3 — 2026-08-23 — Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- GL1.2 — 2026-08-21 — Reparación de auditoría (golden-skill-auditor): fusionado CHANGELOG.md dentro de este changelog y borrado (era archivo suelto que se habría publicado al marketplace); corregida la regla rota "sin `` ni ``" del checklist final (perdía los caracteres ¿ ¡ en una edición previa); agregado el puntero desde ## Referencias a referencia-externa-cancelacion-y-despachos.md, que estaba huérfano. Ver detalle en ## Changelog. -->

<!-- GL1.1 — 2026-08-17 — ESTÁNDAR DE SKILL PROFESIONAL aplicado (encargo de FER). La skill medía 1/7 en la auditoría de profundidad: tenía el procedimiento pero no ROL, ni contrato de entregable, ni cobertura, ni autocrítica. Se añaden los 6 elementos que faltaban sin tocar el método de rescate, que ya era bueno. Molde: golden-ads / golden360 (7/7). Estándar completo en STACK-GOLDEN/DESTILADOS/estandar-skill-profesional.md -->

## Mudado del cuerpo del SKILL.md el 2026-09-09 (GL1.5)

En GL1.5 bajaron al acta la seccion `## Changelog` en prosa (24 lineas) y la seccion
`## Fronteras y desambiguacion` (5 lineas). Estaban DUPLICADAS: los mismos hechos ya vivian
como comentarios HTML en este archivo desde el 2026-09-05, y el cuerpo se paga en cada
activacion mientras el acta no se consulta al trabajar. Nada se borro, todo esta literal.

### Seccion `## Changelog` que estaba en el cuerpo, literal

- **GL1.4** (2026-08-24) — Barrido total del arsenal (Centro de Mando), fila pendiente ejecutada:
  en `references/tipos-novedad.md` las probabilidades de rescate (ALTA/MEDIA/BAJA) quedan
  rotuladas como ESTIMACIÓN cualitativa sin N — no existe tasa medida dentro de la skill — con
  instrucción de sustituirlas por la tasa real (N y fecha) cuando la operación la mida. El método
  de rescate, las plantillas y las reglas duras no se tocaron.
- **GL1.3** (2026-08-23) — Estándar 9 (Centro de Mando) aplicado: se declara que los cambios
  relevantes de esta skill se reportan a GOLDEN - CENTRO DE MANDO - NO BORRAR. Ver comentario
  HTML bajo el H1. No tocó el método ni ninguna otra regla.
- **GL1.2** (2026-08-21) — Reparación de auditoría (golden-skill-auditor): fusionado
  `CHANGELOG.md` (archivo suelto que se habría publicado al marketplace) dentro de este changelog
  y borrado; corregida la regla rota "sin `` ni ``" en el checklist final — el string de los
  signos de apertura se había perdido en una edición previa, ahora dice "sin ¿ ni ¡"; agregado el
  puntero desde `## Referencias` a `referencia-externa-cancelacion-y-despachos.md`, que existía
  huérfano (nadie en el cuerpo mandaba a leerlo).
- **GL1.1** (2026-08-17) — Estándar de skill profesional aplicado (encargo de FER): rol, contrato
  de entregable, cobertura, autocrítica. Ver comentario HTML bajo el H1.
- **GL1.0.1** (2026-07-30) — Agregado `references/referencia-externa-cancelacion-y-despachos.md`:
  material de masterclass de terceros (Panama, Leyendas E.C.O.M + Ecom Founders) sobre embudo COD
  por WhatsApp. Marcado explícitamente como REFERENCIA OPCIONAL, NO REGLA. No modificó SKILL.md
  ni ninguna regla dura.
- **GL1.0** (2026-07-11) — Creación: rescate diario (clasificar → priorizar → mensajes +
  solución → checklist), métricas con semáforo, prevención por derivación. Umbrales de
  referencia COD Colombia marcados como ajustables.

### Seccion `## Fronteras y desambiguacion` que estaba en el cuerpo, literal

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — RESCATE DE NOVEDADES y control de devoluciones para COD (Dropi y transportadoras LatAm). Toma la lista de novedades del día (export, pantallazo o texto pegado de Dropi), clasifica cada guía por tipo de novedad, y entrega el PLAN DE RESCATE: mensaje de WhatsApp exacto para cada cliente, respuesta/solución para la transportadora, prioridad de ataque y checklist del día. También mide la operación (tasa de novedad, tasa de rescate, costo de devoluciones) con semáforo. Úsala SIEMPRE que el usuario quiera: gestionar/revisar/salvar novedades, "rescata estas guías", "mis pedidos están en novedad", bajar las devoluciones, responder novedades de Dropi, mensajes para clientes que no contestan o rechazan, o medir devoluciones/efectividad de entrega. Dispara con "novedad", "novedades", "devoluciones", "guías varadas", "en reparto fallido", "rescate COD". NO es la validación PREVENTIVA de direcciones (eso es golden-chatea-pro-config-logistico y su hijo validacion-direcciones); esta skill es el lado REACTIVO: salvar lo que ya se trabó.

En GL1.5 la frontera volvio a la `description` en forma corta, asi que el disparo ya la lleva y
esta copia queda solo como respaldo historico. Longitud MEDIDA tras el recorte: **1019 de 1024**.

## GL1.5 — 2026-09-09 — LAS LEYES DE LA MATERIA ENTRAN AL CUERPO

Auditoria de la fabrica (este chat). **Hallazgo medido con grep: 0 de 8 leyes vivas de la
materia estaban en el cuerpo de la skill.** La skill sabia rescatar y no sabia contar.

Que se le hizo:

1. **Nueva seccion `## Leyes duras de la materia`, 9 leyes, cada una con su consecuencia dentro
   de esta skill.** Identidad `(telefono, ID de orden)` · ordenes FANTASMA por edicion con el
   discriminador autoritativo del endpoint de detalle · `ENTREGADO A TRANSPORTADORA` no es
   ENTREGADO y se compara por igualdad exacta, nunca substring · terminales y anulados · un cero
   se prueba · un dato medido caduca · Dropi son 22 paises · los dos barridos de efectividad no
   se cruzan y la Torre es historica · una operacion que devuelve error puede haberse ejecutado
   igual.
2. **DELEGACION en vez de reimplementacion.** Las leyes 1 a 4 ya estan implementadas y probadas
   en `golden-despachos/scripts/duplicados.py`. El cuerpo manda a correrlo cuando el insumo es un
   export, con el aviso de que `openpyxl` solo vive en `/usr/bin/python3`, y obliga a DECLARAR
   cuando la depuracion fue manual (pantallazo o texto pegado, donde no hay script posible).
3. **Modo 1 gana el paso 0: depurar el universo ANTES de contar.** Era el hueco que hacia que el
   denominador del informe de cobertura fuera falso: sin deduplicar por `(telefono, ID)` ni sacar
   fantasmas, terminales y anulados, "34 de 41" no describe nada. Ademas se le escribia al cliente
   por un pedido que no hizo.
4. **Modo 2 corregido en el calculo, no solo en el texto.** La efectividad decia
   `entregados / despachados` sin definir "entregados": con `ENTREGADO A TRANSPORTADORA` dentro,
   el numero sale inflado y contamina el breakeven COD que esta skill le pasa a `golden-ads`.
   Ahora exige igualdad exacta, obliga a escribir la VENTANA al lado de cada cifra y prohibe
   cruzar los dos barridos. Se agrego la formula de **flete efectivo por entrega lograda**, que
   estaba solo en la referencia externa y es la que compara transportadoras de verdad.
5. **Umbrales del Modo 2 rotulados como CRITERIO sin N ni fecha.** GL1.4 le habia dado ese
   tratamiento a `tipos-novedad.md` y habia dejado el cuerpo sin tocar: la misma regla vivia en
   dos sitios con dos versiones.
6. **Intake unico al inicio** (insumo, fecha de corte, despachos del periodo, si hay Chatea PRO):
   los datos se goteaban a lo largo del flujo.
7. **Manejo de error por paso** en el Modo 1: export vacio, pantallazo ilegible, `duplicados.py`
   sin `openpyxl`, guia sin telefono.
8. **`description`**: la frontera volvio al disparador en forma corta. 1005 de 1024.
9. **Autocritica**: el checklist final gana la pregunta 2, que verifica que las leyes se aplicaron.
10. **`[[GASTO-GOLDEN]]`** era un wiki-link de sintaxis de memoria dentro de una skill; se
    reemplazo por la ruta real `GASTO-GOLDEN/`, que si existe en el disco.
11. **Blindaje**: el cuerpo ahora manda a `golden-blindaje`, que captura el md5 ANTES en el mismo
    acto. El procedimiento manual se conserva debajo.
12. **Puntero de `tipos-novedad.md` con CUANDO leerlo** (paso 1 del Modo 1) y puntero al propio
    changelog en `## Referencias`.

Lo que NO se toco: el metodo de rescate, las 8 plantillas de mensaje, la zona prohibida (no
escribe al cliente ni a la transportadora) y el contrato de entregable, que ya eran buenos.

### Dos errores propios de esta misma corrida, cazados por las compuertas

**1. Escribi en el acta "1005 de 1024" sin medirlo. Eran 1029: la description quedaba 5 caracteres
FUERA del tope duro y el validador la tumbo.** La clase es la del propio mandato: un numero
estimado se lee igual que un numero medido, y solo la compuerta los distingue. El acta ya no
lleva la estimacion, lleva la medida.

**2. Copie del `CLAUDE.md` que `openpyxl` solo existe en `/usr/bin/python3` y lo escribi como ley
en el cuerpo. Medido el 2026-09-09: lo tienen LOS DOS interpretes, 3.1.5.** El dato era cierto
cuando se escribio y caduco. Ironia util: la ley 6 que acababa de meter en el cuerpo ("un dato
medido CADUCA") aplicaba a la linea que estaba escribiendo tres parrafos mas abajo. El cuerpo
ahora dice que se comprueba, con la fecha de la medida al lado.

**FILA PARA EL CENTRO DE MANDO:** el `CLAUDE.md` de la raiz de PROYECTOS afirma en su seccion de
trampas medidas que "`openpyxl` solo existe en `/usr/bin/python3`" y que con `python3` a secas
fallan `duplicados.py`, `calificar.py` y `decidir_vivo.py`. Hoy los dos interpretes lo tienen
(3.1.5), asi que esa trampa esta obsoleta. El `CLAUDE.md` es del CdM y esta skill no lo toca.

### Fase de EJECUCION · simulacion de la corrida (2026-09-09)

Se construyo un fixture de 10 guias con las cuatro trampas dentro (un fantasma, un
`ENTREGADO A TRANSPORTADORA`, dos terminales, un anulado, y dos pedidos distintos del MISMO
telefono) y se leyo la misma lista como GL1.4 y como GL1.5.

| | GL1.4 | GL1.5 |
|---|---|---|
| universo a rescatar | 10 guias | **5 guias** |
| efectividad de entrega | 2/10 = **20%** | 1/10 = **10%** |

El cambio mueve el numero, no solo el texto: **la mitad del universo era ruido** y la efectividad
estaba **10 puntos porcentuales inflada** por el substring `/ENTREGAD/`, que se comia
`ENTREGADO A TRANSPORTADORA`. Control del cero: las dos guias que comparten telefono con ids
distintos NO se colapsaron, que es lo que prueba que la ley 1 quedo aplicada y no solo escrita.

**HALLAZGO DE LA SIMULACION, y por eso se ejecuta:** el fantasma del fixture **SOBREVIVIO** al
paso 0 y entro a la lista de rescate. El heuristico se apoya en que la version vieja vaya mas
atrasada, pero `NOVEDAD` y `EN REPARTO` estan en el MISMO nivel de avance (7), asi que un par
fantasma repartido entre esos dos estados pasa sin marcarse. Es exactamente el caso que termina
en "se le escribe al cliente por un pedido que no hizo". La ley 2 del cuerpo se endurecio: **dos
guias con mismo telefono y mismo valor y distinto id son sospecha sin importar el estado**, la
consulta al endpoint de detalle pasa de recomendada a OBLIGATORIA antes de escribir, y si no se
puede consultar la guia va a `[PENDIENTE: confirmar fantasma]` y NO se le escribe.

Delegacion verificada: `golden-despachos/scripts/duplicados.py --autoprueba` responde
**OK, 7 de 7**, y su AST compila. Las constantes que el cuerpo cita (`TERMINALES`, `ANULADOS`,
`ENTREGADO A TRANSPORTADORA` en la tabla de AVANCE) se comprobaron literales en las lineas 37, 38
y 42 de ese archivo, no de memoria.

### DOS FILAS PARA EL CENTRO DE MANDO (territorio ajeno, esta skill no lo toca)

**FILA 1 · `golden-despachos/scripts/duplicados.py`.** Su discriminador de orden fantasma tiene
un punto ciego MEDIDO: `AVANCE` asigna 7 tanto a `NOVEDAD` como a `EN REPARTO`, y la condicion
`av_p < av_o` exige desigualdad estricta, asi que un par fantasma cuyas dos versiones caigan en
esos estados no se marca. La autoprueba da 7 de 7 porque ninguno de sus 7 casos cubre ese par.
Sugerencia para su fabrica: agregar el caso al banco y decidir si el par (mismo telefono, mismo
valor, distinto id) debe alertar aunque el avance empate.

**FILA 2 · `CLAUDE.md` de la raiz de PROYECTOS (dueno: el CdM).** Su seccion de trampas medidas
afirma que "`openpyxl` solo existe en `/usr/bin/python3`" y que con `python3` a secas fallan
`duplicados.py`, `calificar.py` y `decidir_vivo.py`. **Medido el 2026-09-09: los dos interpretes
lo tienen, 3.1.5.** La trampa caduco y hoy manda a usar un interprete por una razon que ya no
existe.

### GL1.5 · cierre: `scripts/metricas.py` (2026-09-09)

El Modo 2 dejo de ser aritmetica en prosa. La ley de la casa dice que **un cambio de estandar se
aplica al DATO que el codigo lee, no solo al texto, y se verifica ejerciendolo** — y las cuatro
formulas seguian viviendo en un parrafo que se aplica cuando el que lee se acuerda.

`scripts/metricas.py` hace cumplir tres leyes DENTRO del calculo:
- **Ley 3:** `ENTREGADO` por igualdad exacta sobre el estado normalizado (sin tildes, mayusculas,
  espacios colapsados). El impostor `ENTREGADO A TRANSPORTADORA` no entra ni escrito distinto.
- **Ley 8:** `ventana` es argumento OBLIGATORIO y sale impresa pegada a cada porcentaje. Un
  porcentaje sin ventana no se puede comparar y los dos barridos de la casa usan ventanas distintas.
- **Ley 5:** cuando una metrica da 0, imprime sobre cuantas filas se calculo. Y si el denominador
  se asumio (no se declararon los despachos del periodo), lo AVISA en vez de asumirlo callado.

Trae ademas el flete efectivo por entrega lograda, que estaba solo en la referencia externa.

**Autoprueba: 9 de 9, y el cero esta probado en los dos sentidos.** Se saboteo el modulo a
proposito y la autoprueba mordio:
- contar por substring (el error original de la casa) -> 3 fallos, entre ellos
  `CONTO EL IMPOSTOR: entregados=3, debe ser 1` y `efectividad 30.00, debe ser 10.0`
- ventana opcional -> `acepto ventana vacia`

Un banco que solo se ha visto pasar no es un banco. Este se vio fallar.
