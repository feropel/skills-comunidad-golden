# Historial de golden-meta-ads-analysis

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## GMA1.3.2 · 2026-09-27 · Ley de los requisitos del usuario (aplicó el CENTRO DE MANDO)

Se añadió el bloque «Antes de empezar» del SKILL.md: qué tiene que tener el usuario antes de arrancar, cada requisito marcado BLOQUEANTE o DEGRADABLE y qué pasa si falta (doctrina del CdM del 27-sep). Lo redactó el chat 🧰 ARSENAL Y SKILLS (4 pasadas del golden-verificador adversarial, 0 fallas nuevas en la última) y lo aplicó el CdM sin numerar: el número lo pone la fábrica al ratificar. Solo inserción: 0 líneas quitadas.

## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- skill GMA1.3.1 · 2026-08-24 (centro de mando, remediación del verificador de cierre): el gemelo VIVO del umbral Pago→Compra (semaforos.md:174 decía <12% contra la fuente única <10%) — quinta reaparición de la clase regla-en-una-rama; alineado. -->

<!-- skill v1.3 · 2026-08-24 · Barrido total del arsenal (auditoría fresca golden-skill-auditor, CdM). Reparado con evidencia:
(1) GEMELOS VIVOS de la contradicción que la adenda 2026-08-20 dio por resuelta — el título de §1B seguía diciendo "EN VIVO por defecto, ARCHIVO de respaldo", el heading "Modo EN VIVO (por defecto)" y la nota "Nunca lo presentes como el camino principal" contradecían "EL DISPARADOR ES EL ARCHIVO" de la description; los cuatro corregidos y los modos etiquetados A/B igual que en references.
(2) UMBRALES DEL EMBUDO TRIPLICADOS Y CONTRADICTORIOS pese a la "fuente única" declarada: Clic→Visita era ≥80/<65 en SKILL.md, ≥70/<50 en semaforos.md y >70/<50 en benchmarks_por_objetivo.md; Pago→Compra tenía CUATRO versiones (≥30/<18, ≥25/<15, ≥20/<12, >30/<10 — dos de ellas dentro del propio semaforos.md). Consolidado: benchmarks_por_objetivo.md manda donde la métrica exista, semaforos.md se alineó y declara el dueño de cada umbral, SKILL.md dejó de duplicar la tabla.
(3) SEMÁFORO CPA: evaluar_cpa() cortaba DESCARTAR en 1.3× breakeven mientras SKILL.md y semaforos.md decían 1.5× — probado ejecutando (CPA a 1.4× daba ⚫ por código y 🔴 por docs). Código alineado a 1.5× (el valor documentado en dos lugares) y re-ejecutado: 1.4×→🔴 PIERDE, 1.6×→⚫ DESCARTAR. La tabla del Paso 5 ahora refleja los 7 tiers exactos del código (el código es la fuente).
(4) MIGRACIÓN DE VÍA SIN LIMPIAR: extraccion_en_vivo.md ordena "NUNCA le pidas al usuario que pegue el JSON" pero los 5 fetch_* imprimían "Pega el contenido en Claude" — los 5 prints corregidos al flujo automatizado (Claude lee con Read). También retirados los separadores ═ de los scripts (el propio principio 3 los prohíbe) y el docstring de analyze_all_layers que aún decía "6 capas" (gemelo del fix v1.1).
(5) extraccion_en_vivo.md: aclarado que read_insights no bloquea (check_token.py solo bloquea escritura).
Pipeline re-verificado ejecutando: unit economics + evaluar_cpa + trm_resolver + generación real de .docx (37.8KB). Cambios reportados al Centro de Mando por el agente del barrido. -->

<!-- skill v1.2 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v1.1 · 2026-08-21 · auditoría golden-skill-auditor: CSV soportado + limpieza (historial completo conservado abajo). -->

<!-- 2026-08-07 · DESCRIPCIÓN RECORTADA: superaba el tope de ~1.536 caracteres del listado de skills y se estaba TRUNCANDO, así que las frases del final NO disparaban. Medido antes/después: 1565 → 821 chars. Lo que se movió al cuerpo son rutas de references y explicaciones; se conservaron y ampliaron las frases reales del usuario, que son lo que dispara. -->

<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): resuelta la contradicción tarjeta/cuerpo — la description declara EL DISPARADOR ES EL ARCHIVO y el cuerpo ordenaba empezar SIEMPRE en vivo, ignorando el archivo que el usuario trajo. Regla nueva: con archivo sobre la mesa, el archivo manda y el vivo se ofrece como contraste; sin archivo, vivo. Coherente con la frontera declarada por golden-ads. -->

<!-- skill v1.1 · 2026-08-21 · auditoría golden-skill-auditor: (1) 🔴 CSV realmente NO cargaba — analyze_meta_report.py solo usaba openpyxl/read_excel pese a que description y SKILL.md prometen "Excel o CSV"; agregado _load_csv_report() con detección de encoding/header, probado en vivo (CSV + XLSX corren el mismo pipeline sin error, incluida la generación del .docx); (2) corregida la línea que decía "Modo EN VIVO (camino por defecto)" contradiciendo "EL DISPARADOR ES EL ARCHIVO" de la description y la propia sección 1B; (3) movidas las Reglas duras COD Colombia y los Análisis adicionales de valor a references/reglas_duras_colombia.md (SKILL.md bajó de 506 a 449 líneas, bajo el tope de 500); (4) corregido el docstring de analyze_meta_report.py que decía "6 capas" — el script automatiza 4, las capas 5-8 se calculan inline y ahora lo dice; (5) assets/report_template.md no reflejaba generate_report.py real (P&L histórico era subsección 1.4 y es sección propia "2.", faltaba "Ranking de Campañas" y "Embudo de conversión", y "KPIs de monitoreo" no existe como sección aparte) — reescrito para calzar con el código; (6) eliminado .gitignore suelto en la raíz (material intruso detectado por el inventario del auditor). -->
