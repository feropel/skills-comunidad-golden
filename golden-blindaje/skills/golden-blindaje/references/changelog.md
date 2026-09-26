# Historial de golden-blindaje

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 896 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill GB1.6.1 · 2026-08-30 (CdM, verificacion externa del FILTRO sobre GB1.6) · documentado el
MATIZ SEMANTICO en el docstring de candado_muerde (muerde = "no se puede escribir", no "tiene uchg";
un 444 sin uchg tambien muerde — mejor para el proposito, pero explicado para el depurador futuro) y
simplificada la tupla redundante (PermissionError subclase de OSError). El FILTRO verifico ademas el
caso duro: huella intacta en 4 skills incl. 2 ABIERTAS donde el open SI tiene exito, y leyo que el
probe solo corre tras os.path.exists (no crea SKILL.md fantasma). Sin cambio funcional. -->

<!-- skill GB1.6 · 2026-08-30 (CdM, propuesta del FILTRO) · EL CHEQUEO PASA DE LEER EL CANDADO A
PROBARLO: nueva funcion candado_muerde() en chequeo.py — append de CERO bytes (open 'ab' sin
escribir) sobre toda skill que uchg_arbol juzgue blindada; si el open NO es rechazado = hallazgo
ALTO "FALSO CANDADO". Motivo: el lote del 29-ago aplico chflags que no mordia y el chequeo por
flags no lo vio (ley: el candado se prueba, no se pone). El probe no puede tocar contenido (cero
bytes; demostrado con huella intacta sobre skill abierta). uchg_arbol NO se toco (paridad de
gemelos intacta); el censo diario sigue pasivo — el mordisco vive solo en este chequeo profundo.
Probado en ambas direcciones: copywriting (abierta) no muerde, shopify (blindada) muerde. -->

<!-- skill GB1.5.2 · 2026-08-25 (centro de mando, cierre R6): la 'prosa de las DOS listas' del sello GB1.5.1 vivía SOLO en el sello — ahora EXCEPCIONES_PARCIALES está nombrada en la sección operativa Excepciones por diseño, con su ejemplo, la regla de los dos gemelos y el límite del dir raíz. Afirmación verificada por grep antes de sellar (receta R6). -->

<!-- skill GB1.5.1 · 2026-08-25 (centro de mando, remediación R5): re-blindaje del propio chequeo.py (había quedado 644 sin uchg tras la edición de las 23:23 — la skill del blindaje era la única sin blindar del arsenal, cazada por sus DOS instrumentos); prosa actualizada a las DOS listas de excepción; uchg_arbol juzga también DIRECTORIOS (con archivos uchg y carpeta abierta se podía inyectar un archivo sin resistencia — latente, con caso al banco); guardia de paridad ahora falla CERRADO y cubre también la tabla de excepciones. -->

<!-- skill GB1.5 · 2026-08-25 (centro de mando, remediación R3/R4 del verificador de cierre): chequeo.py CAMBIÓ DE SEMÁNTICA — esto supersede al claim 'INTACTO' del sello GB1.4 y al 'sin cambios de comportamiento', que eran ciertos a su hora y quedaron viejos el mismo día: (1) blindaje por N de M nodos del árbol con la función uchg_arbol de cuerpo BYTE-IDÉNTICO al del censo (stat por archivo, SIGUE symlinks, falla CERRADO); (2) filtro golden* sin guion (golden360 entró al juicio); (3) denominador impreso ('de N juzgadas'); (4) EXCEPCIONES_PARCIALES para escribibles por diseño (fuentes_baseline.json de investigación — regla de los dos lugares); (5) shebang restaurado a la línea 1. -->

<!-- skill GB1.4 · 2026-08-24 · barrido total del arsenal (CdM): la prosa de "Excepciones por diseño" estaba desincronizada del código — decía "Hoy la lista es golden-copywriting" (una sola) cuando chequeo.py lleva DOS exentas desde el 22-ago (golden-copywriting + golden-chatea-operacion); la prosa ahora nombra las dos, declara al script como fuente de verdad y exige actualizar ambos lugares al agregar una excepción. chequeo.py INTACTO (corrido completo hoy: exit 0, 1672 archivos, 0 ALTO). -->

<!-- skill GB1.3 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->

<!-- skill GB1.2 · 2026-08-21 · auditoría golden-skill-auditor: agrega Fase 0 (flujo explícito paso a paso: correr, verificar ALTO abriendo el archivo, presentar triage, pedir permiso antes de tocar seguridad) con definición de terminado y manejo de error si el script no corre; blindaje propio documentado (chflags uchg); cita a tendencias-vivas.md desambiguada como archivo de golden-copywriting, no local -->

<!-- skill GB1.1 · 2026-07-27 · filtro del PDF Claude Security y de blender-mcp, protocolo de triage con ventanas duras, 5 errores que hacen inútil una auditoría, sección MCPs de terceros -->

<!-- skill GB1.0 · 2026-07-23 · auditoría local de ~/.claude sin salida de red · 6 áreas (secretos, permisos, hooks, MCP, blindaje, caché) -->
