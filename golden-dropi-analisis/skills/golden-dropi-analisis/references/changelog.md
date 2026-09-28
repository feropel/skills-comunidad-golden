# Historial de golden-dropi-analisis

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.

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

**Lo que impide que vuelva a pasar:** `scripts/autoprueba_motor.py`, con 12 defectos sembrados y
31 comprobaciones contra la verdad a mano, controles **en los dos sentidos** (que siga cazando
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
