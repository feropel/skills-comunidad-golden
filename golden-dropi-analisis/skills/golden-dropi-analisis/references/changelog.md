# Historial de golden-dropi-analisis

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.

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
