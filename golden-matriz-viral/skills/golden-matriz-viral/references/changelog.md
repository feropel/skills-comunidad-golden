# Historial de golden-matriz-viral

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 947 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill GMV1.8.1 · 2026-08-24 (centro de mando, remediación del verificador de cierre): línea de RUTA del cerebro en el Paso 0 (las lectoras ordenaban LÉELO PRIMERO sin decir dónde — un chat limpio no podía ejecutar la orden) + bump que las ediciones del 23-24 dejaron sin subir. -->

<!-- skill v1.8 · 2026-08-24 · Barrido total del arsenal (auditoría fresca golden-skill-auditor,
CdM): (1) entra el bloque Paso 0 · Cerebro de marca BAJO el H1 — el estándar de la familia de
contenido del CdM (adenda 2026-08-23) que esta skill no traía: leía el brand-brain goteado en las
Fases 2-3 pero sin el paso obligatorio inicial, con lo que una corrida podía arrancar la ingesta y
la matriz sin cargar la voz de la marca; (2) sellos reordenados al patrón de la casa (más nuevo
ARRIBA — estaban v1.6 encima de v1.7, la misma clase de desfase que produjo el doble sello de
golden-ads); (3) la receta de comentarios declara `jq` como dependencia con fallback en python3.
Cambios reportados a 🧠 GOLDEN - CENTRO DE MANDO (estándar 9). -->

<!-- skill v1.7 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se
reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v1.6 · 2026-08-21 · golden-skill-auditor: (1) Versión desincronizada — la etiqueta decía
GMV1.4 mientras el Changelog ya iba en GMV1.5 (la transcripción local con whisper-cpp de la Fase 1
ya estaba en el cuerpo pero la versión no lo reflejaba); corregido a GMV1.6, único número en todo
el archivo. (2) El description no mencionaba la Fase 5 CALENDARIZAR (capacidad real que la skill
ya entrega) — se agregaron trigger y frase de disparo. (3) Se agregó un ejemplo concreto
entrada→salida de un renglón de matriz y un guion (Fase 2/3) para que el primer uso no dependa de
inferir el formato. (4) Se agregó definición explícita de "terminado" por fase. (5) Blindaje:
`chflags uchg` — mecanismo documentado aquí y en el registro de golden-skill-auditor. -->
