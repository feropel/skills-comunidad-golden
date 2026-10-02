# Historial de golden-dropi-analisis

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.

## v2.2 · 2026-09-29 · La autoprueba MENTÍA, y otras diez fallas que destapó un adversario

La 2.1 se selló con todo en verde. Un verificador adversarial —que solo vio el estado final y el
estándar, nunca cómo se construyó— corrió 7 exports propios, leyó los entregables celda a celda
y encontró **once fallas con evidencia ejecutada**. La peor no estaba en el motor:

🔴 **La autoprueba mentía.** Le sembró dos roturas reales y las dos pasaron en verde, 36 de 36:
clasificar `ENTREGADO A TRANSPORTADORA` como venta cobrada, y descontar automáticamente las
candidatas a orden fantasma. Las dos violan reglas explícitas del estándar. Las causas, medidas:

- el banco **no tenía ni una fila** con `ENTREGADO A TRANSPORTADORA` (`grep -c` → 0), el estado
  con la trampa más cara del universo de Dropi;
- la única comprobación sobre fantasmas miraba que apareciera un **texto** en la salida, y ese
  texto se imprime **antes** de cualquier descuento: borrar una orden no cambiaba el mensaje;
- las 6 mutaciones eran las 6 regresiones que ya tenían aserción propia. **Un test de mutación
  que solo confirma los tests que ya existen no prueba nada.**
- `--mutar` mutaba el motor de **producción in situ** dentro de `~/.claude/skills` y reventaba
  con `PermissionError` en el sandbox; un corte a mitad dejaba la skill instalada mutada.

**Las diez del motor y los entregables:**

1. **Dinero con tres formatos que daban cifras falsas y se declaraban legibles.** `8E+04` (lo
   que Excel escribe al exportar) daba **804** en vez de 80.000; `(20.000)` daba **+20.000**,
   con el signo invertido; `20,000.50` daba **20,0005**. En su fixture, $80.000,50 reales
   salían como **$20.824** y el veredicto decía RENTABLE.
2. **Un ID vacío se volvía la cadena `"None"`** y el dedup fundía todas esas filas en una: dos
   ventas entregadas desaparecían, y el aviso mandaba a buscar un archivo duplicado inexistente.
3. **"Me quedo con la más reciente" era falso:** se quedaba con la última en orden **alfabético**
   de nombre de archivo. Con dos exports del mismo periodo, el veredicto lo decidía el nombre.
4. **`MAESTRO_CONTACTOS` salía con 0 clientes sin un solo aviso** cuando falta el export por
   producto — y SKILL.md prometía literalmente que "se dice". No se decía.
5. **El PDF fusionaba dos empresas sin una palabra.** La consola avisaba; el documento que se
   entrega, no. `'no se suman' in texto` → False.
6. **`CANTIDAD` 0 se convertía en 1** por un `or 1`, una negativa se publicaba como unidades, y
   un nombre de producto en blanco sobrevivía al `or` y salía como celda vacía.
7. **Una fecha en 2099 entraba completa en el P&L** sin una alerta.
8. **Contradicción dentro del mismo Excel:** `RESUMEN` decía "Ganancia neta acumulada $60.000"
   sumando órdenes no cobradas, mientras `RESUMEN EJECUTIVO` decía "$0 realizada".
9. **El PDF solo se verificaba por existencia**, sin abrir ni comprobar una cifra.
10. **Los avisos vivían solo en stdout**, que se pierde al cerrar el chat.

**Lo corregido:** `money()` entiende notación científica, negativo contable y formato US, y
decide el decimal por el separador más a la derecha; las filas sin ID llevan clave propia y se
declaran; el aviso del dedup dice la verdad y explica qué hacer; falta del export por producto,
fechas raras, cantidades raras y dinero ilegible se declaran; la ganancia del `RESUMEN` es solo
la **cobrada**; y **todo lo que quedó fuera va a la hoja `COBERTURA` del Excel y al bloque final
del PDF**, construido en un solo sitio para que un aviso nuevo no se pueda olvidar en un
entregable.

**La autoprueba pasa de 36 a 56 comprobaciones y de 6 a 10 mutaciones**, cuatro de ellas
atacando reglas del estándar que antes no cubría ninguna: `ENTREGADO A TRANSPORTADORA`, el
no-descuento de fantasmas, el ID vacío y la ganancia no cobrada. La fantasma ya no se comprueba
por un texto sino **contando las órdenes**. El PDF se verifica por **contenido** (cifra, acentos
en el render, bloque de cobertura), y si no hay con qué extraer el texto el caso se declara
OMITIDO, nunca por bueno. `--mutar` trabaja sobre una copia en un temporal y no toca la skill.

**Lo que el adversario dejó sin verificar, y sigue sin verificarse:** no hay ningún export REAL
de Dropi en este entorno, así que los formatos raros de dinero y de cantidad son plausibles, no
medidos contra un export de verdad. Tampoco se ejercitó la rama de enriquecimiento opcional
(etiquetas de WhatsApp, leads del bot, posibles). Y de los ~41 estados reales de Dropi, el banco
cubre 9: los demás no están probados ni una vez.

## v2.1 · 2026-09-28 · Tratar "no se sabe" como "cero": dos veredictos falsos más

La 2.0 se selló con las cifras cuadrando. Estos dos no salieron de leer el código: salieron de
**generar el PDF y mirarlo**, que es el paso que se salta siempre.

**Caso: un negocio que acaba de empezar a despachar.** Tres órdenes en ruta, ninguna cerrada
todavía, $120.000 de publicidad gastados. El resumen decía:

- **`% ENTREGA 0,0%`** — no hay denominador. La verdad es que aún no se puede medir. Un dueño
  lee "0,0%" como "no entrego nada".
- **`NO RENTABLE`**, en rojo, en el banner del documento que él lee primero. Sus órdenes siguen
  vivas: el resultado no existe todavía, no es que esté perdiendo.
- **`Ganancia potencial en camino: $0`** — con tres órdenes en camino. Era "no hay con qué
  estimarla", no "cero".

**La clase es una sola: tratar la ausencia de dato como un dato en cero.** Las tres decían algo
falso con total serenidad, y ninguna daba error. Ahora: `s/d (nada cerrado aún)`, el veredicto
`SIN VEREDICTO: NINGUNA ORDEN CERRADA TODAVÍA`, `no estimable`, y las filas de transportadora,
departamento y ciudad marcadas `sin cerrar`. La "Definición de terminado" ya avisaba de que un
0% es sospechoso, pero lo dejaba en manos del lector en vez de resolverlo en el motor.

**También:** el texto nuevo del PDF salió sin acentos ("Todavia", "asi", "aun") y el banner en
mayúsculas sin tilde. Se ven en el RENDER, no en el fuente, y ahí es donde se corrigieron.

**Autoprueba:** sube a 36 comprobaciones y 6 mutaciones, con dos nuevas que vigilan justo esto
(que no vuelva el 0,0% y que no vuelva el NO RENTABLE sin una sola orden cerrada). Las 6 se cazan.

**Cobertura de esta pasada:** autoprueba 36 de 36 en verde con reportlab presente; 7 casos
extremos ejecutados (carpeta vacía, cero filas, una sola orden, todo en tránsito, fechas y campos
basura, xlsx corrupto junto a uno bueno, ganancia negativa) y ninguno revienta — el corrupto se
salta declarando el motivo y la corrida sigue. PDF verificado abriéndolo y mirándolo.

## v2.0 · 2026-09-27 · La FÁBRICA: el motor daba cifras infladas, medido y corregido

Auditoría de la fábrica con el mandato de autocalificación. **No es un repaso de estilo: seis de
las cifras que esta skill produce estaban mal**, y todas fallaban en silencio. Medido corriendo el
motor contra un banco de exports con defectos sembrados y verdad calculada a mano.

**Lo que salía mal, con el número medido (banco de 16 órdenes):**

| Cifra | Verdad | Antes | Después |
|---|---|---|---|
| Ganancia realizada | $225.000 | **$2.185.000** | $225.000 |
| % de entrega global | 64,3% | 72,7% | 64,3% |
| Canceladas | 1 | 0 | 1 |
| Órdenes cargadas | 16 | 15 | 16 |
| Transportadoras en la tabla | 4 | 1 | 4 |

**Las causas, una clase cada una:**

1. **`classify()` comparaba por igualdad exacta.** `SINIESTRO` (paquete perdido) y `GUIA_ANULADA`
   caían en "tránsito", así que salían del denominador e **inflaban el % de entrega**; y
   `REEXPEDICIÓN` con tilde no casaba con el patrón `REEXPEDICION` sin tilde — mientras
   `pipeline()` sí la reconocía con un patrón más corto, o sea que las dos funciones
   discrepaban. Ahora se compara por subcadena y sin tildes, contra el universo real de estados.
2. **`money()` multiplicaba por cien.** `"20000.00"` (dinero guardado como texto) se leía como
   2.000.000, porque el punto se quitaba a ciegas como separador de miles. Una sola celda así
   infló la ganancia **casi diez veces** y, con gasto de publicidad configurado, habría dado un
   RENTABLE falso. Ahora un único punto con 1 o 2 dígitos detrás es decimal.
3. **El filtro de prueba borraba clientes reales.** Buscaba TEST/PRUEBA por subcadena: "Maria
   Testa" y "Juan Protesta" salían de las ventas y de la efectividad **sin que nadie los
   contara**. Ahora es palabra completa, y lo excluido se lista con nombre y teléfono.
4. **Umbrales de muestra que el dueño había derogado** (`act<5` transportadora, `act<3`
   departamento, `act>=4` ciudad): escondían justo las plazas nuevas. Fuera los cuatro; entra
   una columna `Muestra` que marca `dato flaco`. La muestra se muestra, no se filtra.
5. **Las órdenes fantasma eran invisibles.** Al editar una orden Dropi le cambia el ID, así que
   el dedup por ID nunca las ve y la misma venta se cuenta dos veces. Peor: `ped` ni siquiera
   guardaba el teléfono, así que la clave (teléfono, ID de orden) era imposible. Ahora se buscan
   por su huella y se listan en `POSIBLES FANTASMA`. **No se descuenta ninguna**: una candidata
   no es una fantasma y declararlas a ciegas ya produjo una tanda entera de falsos positivos.
6. **Los archivos que no se podían leer desaparecían sin una palabra** (`.csv`, `.xls`, columna
   renombrada, fichero corrupto): esas ventas simplemente no existían para el informe. Ahora el
   motor abre con un `INVENTARIO DE LA CORRIDA` que lista lo leído y lo saltado con el motivo.

**Además:** el resumen de cualquier cliente salía titulado con la marca de otro negocio, y el PDF
llevaba dentro una frase de contexto interno. El motor corría sin el informe por pedido y daba
$0 con un **NO RENTABLE falso**: ahora eso es `SIN VEREDICTO`. Las dos líneas clave del P&L
(`= Utilidad Dropi` y `= UTILIDAD NETA FINAL`) empezaban por `=`, así que Excel las guardaba como
**fórmula** y al abrir el archivo **se quedaban sin etiqueta**; ahora usan `(=)`. El dedup por
producto se comía líneas legítimas del mismo producto con SKU distinto. Y el PDF cierra con
"Qué quedó fuera de estas cifras".

**Un septimo defecto, encontrado DESPUES de instalar, por seguir probando casos extremos:** con
todas las ordenes aun en ruta y ninguna cerrada, el resumen decia **`% ENTREGA 0,0%`**. No hay
denominador: la verdad es que todavia no se sabe. Un dueno que abre ese informe lee "no entrego
nada" y es una conclusion de negocio falsa. Ahora dice `s/d (nada cerrado aun)` y esas filas van
marcadas `sin cerrar`. La propia "Definicion de terminado" ya avisaba de que un 0% es sospechoso,
pero lo dejaba en manos del lector en vez de resolverlo en el motor.

**Lo que impide que vuelva a pasar:** `scripts/autoprueba_motor.py`, con 13 defectos sembrados y
35 comprobaciones contra la verdad a mano, controles **en los dos sentidos** (que siga cazando
pruebas de verdad y duplicados reales; que **no** invente fantasmas donde hay compras legítimas)
y un modo `--mutar` que rompe el motor a propósito para comprobar que la autoprueba lo caza.
Se corre obligatoriamente después de tocar el motor.

**Medido en este equipo:** `reportlab` no está en el `python3` de Homebrew, así que hoy la skill
**no genera su entregable principal** hasta que el usuario monte el entorno aislado que ya
describe el bloque de requisitos. El PDF se verificó generándolo en un entorno aparte y
**mirándolo**: acentos correctos en el render, una sola página, sin marca ajena.

## v1.9 · 2026-09-27 · Ley de los requisitos del usuario (redactó ARSENAL, aplicó el CdM)

Se añadió el bloque "Antes de empezar — lo que TÚ tienes que tener": cada requisito marcado
BLOQUEANTE o DEGRADABLE y qué pasa si falta. Lo redactó el chat ARSENAL Y SKILLS (fila P49, 4
pasadas del verificador adversarial) y lo aplicó el Centro de Mando sin numerar, a la espera de
que la fábrica lo ratificara. **La fábrica lo ratifica aquí como v1.9.** Solo inserción: 0 líneas
quitadas. Dos de los riesgos que ese bloque documentaba (el NO RENTABLE falso sin informe por
pedido, y reportlab ausente en Homebrew) están ahora además **resueltos en el motor**: la
documentación advertía, pero el código seguía dando el veredicto falso.

## [ratificada como v1.9] · 2026-09-27 · Ley de los requisitos del usuario (aplicó el CENTRO DE MANDO)

Se añadió el bloque de requisitos del SKILL.md: qué tiene que tener el usuario antes de arrancar, cada requisito marcado BLOQUEANTE o DEGRADABLE y qué pasa si falta (doctrina del CdM del 27-sep). Lo redactó el chat 🧰 ARSENAL Y SKILLS (fila P49, 4 pasadas del golden-verificador adversarial; en la última, ninguna falla nueva grave) y lo aplicó el CdM sin numerar: el número lo pone la fábrica al ratificar. Solo inserción: 0 líneas quitadas.

## v1.8 · 2026-09-19
CdM: la ley del flete derogada seguía escrita en dos sitios. SKILL.md (sección Rentabilidad) y un
comentario del motor decían que una devolución pierde "el flete de ida y vuelta". La ley vigente del
dueño es de **un solo flete**: la devolución cuesta el flete de devolución, igual o menor al de ida
y nunca mayor. **El cálculo ya estaba bien**, porque el motor suma la columna `COSTO DEVOLUCION FLETE`
del informe por pedido y no multiplica ningún flete por dos. El error era de texto, pero es el texto
que lee quien interpreta el P&L. Lo destapó golden-verificador al convertir el agente golden-finanzas
en skill; la misma clase apareció en 6 archivos del arsenal.

## v1.7 · 2026-09-13
Auditoría `golden-skill-auditor`: el comentario bajo el H1 de SKILL.md apuntaba al changelog pero
no declaraba la versión vigente (Estándar 7 de la casa: "comentario HTML bajo el H1 con la
versión"), y había quedado desincronizado tras mudar el historial completo aquí el 2026-09-05
(la última acta era v1.6.1 y el cuerpo no la reflejaba). Se agrega la línea de versión bajo el H1.
Sin cambios de contenido ni de motor. Re-verificado con `inventario.sh`: 0 referencias rotas,
0 huérfanos, `validar_arsenal.py` en exit 0.

## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 980 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill v1.6.1 · 2026-08-24 · barrido total del arsenal (CdM): fechada la entrada v1.6 del changelog (era la única sin fecha; formato uniforme para el próximo editor). Sin cambios de contenido ni de motor. Motor re-verificado hoy EJECUTÁNDOLO contra fixtures sintéticos con casos malos sembrados: dedup cazó 1 duplicado por-pedido y 1 por-producto y avisó, nombre PRUEBA excluido, TRANSITO A DEVOLUCION contado como devolución (regla FER v1.4 intacta), camino sin-reportlab degradó con aviso y generó los 2 Excel, y las cifras del RESUMEN EJECUTIVO (50% entrega, P&L $60.000−$18.000−$40.000=$2.000 RENTABLE) coincidieron con el cálculo a mano. -->

<!-- skill v1.6 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v1.5 · auditada golden-skill-auditor 923→1000 (2026-08-21): (1) reportlab declarado como dependencia junto a openpyxl — faltaba, y es la librería que produce RESUMEN_EJECUTIVO.pdf, el documento que esta misma skill llama "lo primero que se entrega"; sin declararla, un chat limpio sin reportlab instalado se queda sin el entregable principal y nadie lo nota; (2) "Definición de terminado" ahora exige confirmar que el PDF existe (o, si reportlab falta, instalarlo o avisar explícitamente que el resumen quedó solo en Excel) — antes el checklist solo pedía las 2 rutas de Excel, contradiciendo la sección "Qué produce"; (3) orden cronológico del changelog corregido (más nuevo arriba). Motor verificado en vivo con fixtures sintéticas: 200 filas por pedido + 200 por producto, dedup de 3 duplicados detectado y avisado correctamente, caso "solo archivo por producto" (sin por pedido) corrido sin ZeroDivision, cifras de RESUMEN EJECUTIVO y CLIENTES coherentes con la metodología documentada. -->

<!-- skill v1.4 · decisiones de FER 2026-07-25: (1) TRANSITO A DEVOLUCION se queda contando como DEVOLUCIÓN ("cien por ciento será una devolución" — si ya va en tránsito de vuelta, es pérdida); (2) red de seguridad de duplicados ACTIVA: dedup por (cuenta, ID) en por-pedido y (cuenta, ID, producto) en por-producto, quedándose con la aparición más reciente y AVISANDO cuántas unió (probado: 2 archivos iguales de 10 órdenes → 10 únicas + aviso) -->

<!-- skill v1.3 · fix auditoría 2026-07-25: (1) ZeroDivision resuelto cuando solo hay export "por producto" (tot = len(ped) or 1) — antes moría tras MAESTRO_LOGISTICA y no generaba CONTACTOS; (2) segmento() ya no marca RIESGO a clientes sin ninguna devolución (todo en tránsito = NEUTRO, no "mucha devolución"); (3) moneda con separador de miles LatAm (punto) vía helper cop(), sin colisionar con money() de parseo. -->

<!-- skill v1.2 · + RESUMEN EJECUTIVO de rentabilidad (hoja + RESUMEN_EJECUTIVO.pdf): estado de flujo por orden + P&L + veredicto RENTABLE/NO. gasto_publicidad va en _config_dropi.json -->

<!-- skill v1.1 · auditada golden-skill-auditor 921→1000: puntero a esquema-dropi.md, comando con ruta absoluta, wp_name usado como fallback de nombre, import openpyxl elegante, definición de terminado + ejemplo de entrega -->
