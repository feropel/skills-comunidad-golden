---
name: golden-pdf-check
description: >-
  Golden Group — estándar de PDF de Comunidad Golden. Audita y ARREGLA PDFs
  (o los construye desde cero) para que salgan con la identidad Golden y, sobre
  todo, para que NINGÚN prompt/bloque copiable se parta entre páginas: cada
  prompt ocupa una sola página y, si hace falta, se reduce para caber entero
  (copy-paste limpio). Revisa identidad de marca, colores, márgenes, paginación
  y estructura. Úsala SIEMPRE que el usuario quiera: crear, revisar, auditar,
  arreglar, maquetar o "dejar perfecto" un PDF para la comunidad o los alumnos;
  un PDF de prompts para copiar y pegar; un documento con la marca Golden Group;
  cuando diga "revisa este PDF", "este PDF se ve feo", "hazme un PDF de prompts",
  "que no se corten los bloques", "márgenes/colores/paginación del PDF", o pegue
  o mencione un archivo .pdf que haya que verificar o producir. También aplica
  cada vez que Claude vaya a generar un PDF entregable para Golden: ese PDF debe
  pasar por este estándar. NO es para editar temas Shopify ni analizar anuncios.
---

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1005 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# golden-pdf-check · el estándar de PDF de Comunidad Golden

<!-- skill v6.1 · 2026-09-02 (reporte del chat del Cartel, verificado línea por línea, encaminado por el CdM) · LA IDENTIDAD SE PIDE, NO SE HEREDA. La skill sale de casa, y hasta v6.0 el valor POR DEFECTO de la marca era la de FER: quien la usara sin `--tema` firmaba SUS documentos como Comunidad Golden. No es un fallo de código — el código hacía exactamente lo que decía; el problema era lo que decía. Un documento sin sello es neutro; un documento con el sello de otro es una ATRIBUCIÓN FALSA, y esa no la caza ninguna prueba de maquetación porque el PDF sale perfecto.
     El reporte señalaba UN punto (el kicker, línea 377). Al ir al código eran CINCO: kicker, autor, dos defaults de `footer_label`, el flag `--footer`… y el LOGO, que no venía en el reporte y es el peor de todos, porque un pie vacío con el emblema Golden encima sigue firmando por FER. Vale la pena decirlo tal cual: el reporte era correcto y aun así se quedaba corto, y la diferencia la hizo ir a mirar el árbol entero en vez de arreglar la línea que me daban.
     Todo pasa a NEUTRO. Sin identidad no se rellena: se AVISA por stderr y se dice cómo pedirla (`--tema comunidad-golden`). La marca de Golden no se perdió, se mudó a su tema, que es justo lo que v6.0 construyó. Los huecos se OMITEN en vez de quedar vacíos: un `<div class="logo">` vacío reservaba su alto igual y un autor vacío con fecha imprimía un "·" suelto.
     PRUEBA 21 · NEUTRALIDAD POR DEFECTO, guardián de CLASE: construye SIN tema y falla si aparece cualquier marca de la casa, texto o logo. Y aquí la regla de higiene de FER cobró de verdad: la primera versión de esa prueba PASÓ EN VERDE con el defecto repuesto a propósito. Estaba ciega — el kicker se imprime en VERSALITAS, así que el PDF dice "COMUNIDAD GOLDEN" y yo comparaba contra "Comunidad Golden". Un guardián que parece trabajar es peor que ninguno. Corregida a comparación en mayúsculas y re-probada rompiendo los CUATRO vectores por separado: 4 de 4 cazados.
     DAÑO COLATERAL QUE DESTAPÓ EL ARREGLO: la prueba 12 (figuras) exigía ">= 2 imágenes" y pasaba porque contaba el logo que se colaba solo. Su umbral medía dos cosas distintas: la figura del documento y una marca del motor. Ahora mide lo suyo.
     LÍMITE DECLARADO, no lo tapo: lo que se neutralizó es la ATRIBUCIÓN (logo, kicker, autor, pie). La HOJA DE ESTILO por defecto sigue siendo la de Golden — fondo crema y dorados. Eso ya no dice de quién es el documento, pero sigue pareciéndose a Golden. Neutralizar también la paleta significa diseñar un tema base neutro y cambiaría el aspecto de todo PDF construido sin `--tema`: es decisión de FER, no mía, y queda planteada. Autoprueba 23/23. -->

<!-- skill v6.0 · 2026-09-02 (encargo de FER: "no fue la estructura del PDF, sino el CONTENIDO") · Hasta v5.18 la skill sabía maquetar sin cortar y copiar sin corromper, y eso ya estaba medido. Lo que NO sabía era DIBUJAR: entregaba párrafos correctos donde hacía falta un esquema. Tres frentes nuevos.
     (1) COMPONENTES VISUALES (`scripts/visuales.py`): KPI, barras, escala contra meta, comparativa, pasos y QR, escritos con el método de la skill `dataviz` — la forma se elige por el TRABAJO del dato, el color se asigna después y la paleta se VALIDA con script, nunca a ojo. Una desviación deliberada del método y su razón: en pantalla la etiqueta directa es SELECTIVA porque el hover rescata lo demás; en un PDF impreso no hay hover, ni tooltip, ni vista de tabla, así que aquí la etiqueta directa es OBLIGATORIA en todo componente. Serie `--s1..--s6` validada; ningún dato queda a merced de distinguir dos tonos.
     (2) IDENTIDAD POR CHAT (`assets/temas/*.json` + `--tema`): el mismo .md sale con la marca de quien lo firma — colores, pie, rótulos. Con un cerrojo: cada tema declara `source_of_truth` (de qué archivo real salieron los valores) y, si no lo trae, la construcción AVISA A GRITOS. `comunidad-golden` está anclado a `GASTO-GOLDEN/app/globals.css`; `cartel-del-chat` va marcado PROVISIONAL con `source_of_truth: null` porque sus valores los inventé yo para demostrar el mecanismo — sirven de demo, no de marca, y hay que pedírselos a su chat por el CdM.
     (3) EL ÍNDICE DEJA DE SER OBLIGATORIO. La v5.4 mandaba abrir TODO PDF con una página CONTENIDO; FER la revocó midiendo lo que nadie mide, al lector: "la gente no lee los índices, eso no es un libro". Ahora es opt-in (`--mapa`), solo primer nivel, una columna y se llama "EN ESTE DOCUMENTO". Un mapa dice dónde estás; un índice de dos niveles a tres columnas es una pared de texto en la portada.
     DEFECTO CAZADO EN ESTE MISMO TURNO, y es de clase, no de caso: el rótulo del mapa estaba escrito A MANO en DOS sitios — el que lo dibuja y el que lo busca en la segunda pasada. Al renombrarlo aquí mismo ("ÍNDICE DEL DOCUMENTO" -> "EN ESTE DOCUMENTO") el detector dejó de reconocer su propia página EN SILENCIO: la búsqueda arrancaba en la hoja del mapa y la primera entrada salía con el número de esa hoja. Medido 1 de 8 mal, y solo 1 porque el cursor monotónico tapaba las otras 7 — un fallo que se disfraza de casi-acierto. Arreglo: `MAPA_TITULO`, una sola constante para las dos puntas, más el bucle acotado a la RACHA INICIAL de páginas (antes tomaba la ÚLTIMA página con la firma, así que un documento cuyo CUERPO mencionara esas palabras se habría llevado el cursor al final). Prueba diferencial: con la firma vieja 1 de 8 mal, con la constante 0 de 8.
     Autoprueba 22/22 (dos nuevas: componentes visuales con etiqueta directa, e identidad por tema comprobando que el MISMO .md sale distinto). Sin verificar todavía: la ruta de arreglar un PDF ajeno (Canva/Word) nunca se ha ejercitado, y los valores del tema del Cartel no son suyos. -->

<!-- skill v5.18 · 2026-09-02 (fila del CdM tras correr la autoprueba en una máquina sin pypdf) · TRES ESTADOS, no dos: `ok=None` = NO SE PUDO VERIFICAR. Antes, correr la autoprueba en un intérprete sin pypdf imprimía [FAIL] y cerraba con 'HAY FALLOS' — quien la corriera concluía que el estándar de PDF estaba roto cuando lo que faltaba era una librería. Es el FALSO ROJO, que por la regla de la casa es el que nadie audita porque parece que el detector trabaja. Ahora imprime [N/D] y cierra con 'TODO OK en lo medido · N sin verificar (falta dependencia, no es un fallo)', declarando el denominador. FRONTERA IMPORTANTE, que NO contradice el fallar-cerrado: si un chequeo no resuelve algo DEL ARTEFACTO (token renombrado, fondo no declarado) eso sigue siendo FALLO — es señal sobre lo que mide; `None` es solo cuando el ENTORNO no permite medir, y ahí el chequeo no tiene nada que decir del PDF. Verificado en los dos intérpretes: con pypdf 20/20 TODO OK; sin pypdf, [N/D] en la prueba de fuentes y veredicto honesto, exit 0. ADEMÁS: audit_pdf.py daba un TRACEBACK crudo de Python cuando el PDF no existía (medido al correrlo contra una ruta borrada); ahora dice qué archivo no encuentra y recuerda mirar el directorio, exit 2. -->
<!-- skill v5.17 · 2026-09-02 (cierre del turno v5.16 · aviso del CdM sobre la CUARTA CARA) · La versión de una skill vive también FUERA de su árbol: la fila del REGISTRO-FABRICAS, que leen los otros chats y que ningún bump ni ritual de blindaje alcanza. Medido al recibir el aviso: registro v5.15 contra disco v5.16 — desfasada, tal cual advirtieron (a golden-shopify le pasó dos veces el mismo día y una vez RETROCEDIÓ). No la edito: el registro dice 'no editar a mano' y tiene dos escritores; se REPORTA al CdM y él regenera. PRUEBA 19 (informativa, no bloqueante): la autoprueba compara su sello con la fila del registro y lo dice — informativa a propósito porque entre sellar y regenerar hay una ventana de desfase legítima, y hacerla fallar ahí sería el detector agresivo que la prueba 18 existe para evitar. PRUEBA 20 · COHERENCIA DEL SELLO: compara las comprobaciones DECLARADAS en la docstring contra las que la corrida imprime de verdad. Existe porque ya falló dos veces (decía 13 corriendo 14; decía 15 corriendo 14) y las dos las cazó un ojo externo, no yo. Y en su primera versión salió DESFASADA POR UNO ella misma — declaraba 19 sobre una salida de 20 porque no se contaba la línea informativa: se movió al FINAL para que cuente todo, incluida ella. La comprobación de coherencia saliendo incoherente es la mejor prueba de que hacía falta. Autoprueba 20/20. -->
<!-- skill v5.16 · 2026-09-02 (fila del CdM · higiene del arsenal) · RENOMBRADO scripts/selftest.py → scripts/autoprueba.py y assets/selftest-sample.md → assets/autoprueba-muestra.md. El porqué es MEDIDO, no estético: de las 5 skills del arsenal con autoprueba, 4 ya usaban el nombre en español y esta era la última en inglés — mientras siguiera así, todo censo del arsenal tenía que ser bilingüe o perdía una skill (le pasó a golden-shopify, que no se veía en su propio censo). El instrumento se arregla antes que el dato. Actualizadas TODAS las caras vivas: los comandos del SKILL.md, la docstring, la cabecera que imprime (=== AUTOPRUEBA ===), el prefijo del tmpdir, el nombre del PDF de trabajo, brand.md y golden-brand.json. El CHANGELOG HISTÓRICO NO se reescribe: las entradas v4 a v5.15 nombran `selftest.py` porque así se llamaba cuando ocurrieron, y falsificar el acta para que cuadre con el presente sería peor que la incomodidad — quien lea una entrada vieja debe saber que **selftest.py es el nombre anterior de autoprueba.py**. PRUEBA 18 NUEVA (refinación de la ley del validador que se prueba, aportada por golden-shopify): probar en las DOS direcciones. Tenía cubierto el 'no dispara con lo bueno' en paginación y en el aviso de líneas largas, pero el detector de COLOR solo se probaba contra un PDF feo — si alguien apretaba la tolerancia, mis propios PDFs saldrían marcados y ninguna prueba lo cazaría. Un detector demasiado agresivo daña tanto como uno ciego y es más difícil de notar, porque parece que trabaja. Autoprueba 18/18. -->
<!-- skill v5.15 · 2026-08-30 (fila del chat APUNTES GOFEST; REPRODUCIDA antes de aceptar el diagnóstico) · Una bitácora de 53 págs pasó mi auditoría (APROBADO) y FER la rechazó al leerla: "no se entiende, se ve muy pequeño, no tiene un mapa para entender el paso a paso, toca uno adivinar". El chat de origen lo diagnosticó como hueco de guía de contenido; al reproducirlo (bitácora equivalente, 132 líneas de índice, 23 págs) aparecieron DOS defectos MÍOS que su diagnóstico no nombraba: (1) el índice automático NO tenía números de página — con 132 líneas no es un mapa, es una lista, y eso es literalmente "toca adivinar"; (2) el nivel .toc.dense-4 comprimía el índice a 4 columnas de 7.4pt con insignias de 6.2pt: ilegible, eso era "se ve muy pequeño". ARREGLADO: números de página REALES por doble pasada con PUNTO FIJO (localiza cada encabezado en el PDF construido y repite hasta converger — añadir los números puede empujar el índice a otra hoja y correr todo el cuerpo: el error clásico de las TOC; si no converge, avisa y no sella); saltando las páginas del propio índice al buscar (sin eso todos los números salían '1', bug medido y corregido); dense-4 eliminado y piso de tipo del índice subido; el PIE pasa de 6.0pt a 7.5pt porque era el ÚNICO texto del PDF bajo el piso — se sube en vez de exceptuarlo, un piso con un violador no es un piso. Prueba 17: documento largo → números del índice CORRECTOS contra las páginas reales + ningún texto bajo 7pt en NINGUNA página (clase completa, por nota del CdM). Verificado: 12 de 12 secciones con el número correcto. DESCARTADO CON MOTIVO: el heurístico bullets/prosa que proponía la fila — sería policía de estilo con alto falso positivo, y convertir notas telegráficas en prosa es AUTORÍA de quien escribe, no de la skill; en su lugar, guía de los DOS tipos de documento (entregable de prompts vs informe narrativo) en content-format.md. DOS BUGS QUE CAZÓ LA PROPIA PRUEBA antes de sellar: (a) la 2ª pasada no reiniciaba FIG_COUNTER y un documento de dos figuras sacaba los pies como 'Figura 3 / Figura 4' — el reinicio vive ahora DENTRO de build_html, no en main(), para que no dependa de recordarlo en cada llamada; (b) mi propia prueba 17 asumía que el índice ocupa 2 páginas y reportaba mal 2 de 8 secciones que estaban bien — la extensión del índice se DERIVA por su firma: un test que asume el layout miente en los dos sentidos. Piso de legibilidad medido en TODAS las páginas, sin excepciones (nota del CdM: cazar la clase, no el caso). Selftest 17/17. -->
<!-- skill v5.14 · 2026-08-26 (fila del chat FILTRO DE HERRAMIENTAS; método tomado de la skill dataviz: verificar contraste con NÚMERO, no a ojo) · CONTRASTE: los dorados de marca no pasan WCAG para texto — #d4af37=2.00:1 y #b8912a=2.80:1 sobre el fondo #faf9f5 (mínimo 4.5:1), verificado con aritmética propia. No era regla faltante sino DEFECTO VIVO: el CSS pintaba texto dorado en 6 sitios que la gente lee (kicker de portada, TODOS los enlaces, kicker e insignias del índice, títulos de bloque, y el pie con #9a7b1e=3.81:1). Token nuevo --gold-text #8a6d1f (4.65:1) SOLO para texto; el dorado de marca queda intacto en todo uso GRÁFICO (filetes, gradientes, bordes, banda de tarjeta): la identidad se ve igual, verificado con render antes/después. Regla medida en brand.md + brand.json, y PRUEBA 16 en el selftest que calcula el ratio de cada color de texto contra su fondo y FALLA bajo 4.5:1 — la regla queda ejecutable, no declarativa. Selftest 16/16. Corrección al reporte de origen: decían 14.97:1 sobre negro; contra el negro REAL de la paleta (#1a1508) son 8.65:1 (pasa igual). La prueba 16 FALLA-CERRADO por condición del CdM: si un token no se resuelve (renombrado, color heredado, fondo no declarado) eso es FALLO, no un par que se salta en silencio — un chequeo que se apaga cuando no entiende lo que mira da un verde mentiroso. Probado rompiendo el token a propósito: la prueba muerde con 'NO SE PUDO CALCULAR'. Informe antes/después para FER en ~/Desktop/INFORMES/2026-08-26-contraste-dorado-golden-pdf-check/ (los dos PDFs + comparación + LEEME). LLAVE DE FER: cambia el tono visible del dorado en textos pequeños; revertible con un token si prefiere el brillo. -->
<!-- skill v5.13 · 2026-08-23 (barrido D del CdM, ojo externo solo-lectura) · CIFRA SELLADA NO REPRODUCIBLE: el sello v5.12 decía 15/15 pero una corrida sana imprimía 14 — la prueba "Salida JSON válida" solo hacía results.append DENTRO del except, así que en el camino feliz no se registraba. Una prueba que solo existe cuando falla no se puede contar. Arreglado: el PASS se registra en los DOS caminos → 15/15 medido y reproducible, el sello v5.12 pasa a ser cierto. De paso la docstring decía "13 comprobaciones" (le faltaban esta y la del fixture ejemplar): corregida a 15 con la lista completa y la regla de contar en la salida, nunca de memoria. Ley de la casa aplicada a sí misma: una cifra mal contada es peor que ninguna. -->
<!-- skill v5.12 · 2026-08-23 (auditoría golden-skill-auditor v1.16, corrida desde el chat de Chatea Pro comentarios) · HALLAZGO CRÍTICO ENCONTRADO CORRIENDO LA SKILL COMO ESTÁ DOCUMENTADA (`python scripts/selftest.py`): el `from pypdf import PdfReader` de la prueba 6 vivía FUERA del try, así que un intérprete sin esa dependencia OPCIONAL mataba el self-test con un ModuleNotFoundError y se perdían las otras 14 comprobaciones — el reporte no salía nunca. Ahora los imports opcionales (pypdf, pdfplumber de la prueba de figuras) van DENTRO del try: la prueba que no se puede correr sale [FAIL] con el motivo y el resto sigue. MEDIDO en los dos intérpretes: sin pypdf → 14 PASS + 1 FAIL con motivo (antes: traceback, 0 resultados); con todas las deps → 15/15 TODO OK. Además: dependencias declaradas por script en la sección de self-test (cuál necesita qué y que todas degradan), `assets/selftest-sample.md` citada por nombre con la advertencia de no editar el fixture, y se retiró una prueba de líneas largas que quedó DUPLICADA por trabajo simultáneo de otra sesión el mismo día. -->
<!-- skill v5.11 · 2026-08-23 (auditoría golden-skill-auditor, segunda pasada del día) · CRÍTICO: los 5 comandos documentados decían `python`, binario que NO existe en el Mac de Golden — un chat limpio recibía `command not found`. Ahora la skill declara el intérprete ($PY = ~/.golden/pdfenv/bin/python con fallback a python3, sección 'Antes de correr nada') y todos los comandos lo usan: el conocimiento vivía en la memoria del ecosistema, no en la skill. Además: golden-brand.json declaraba card_max_mm=250 (el real lo DERIVA build_pdf.py = 246) y la tipografía del sistema en vez de las fuentes incrustadas — dos datos desfasados en el archivo que el SKILL.md señala como el sitio de tokens; se corrigieron con nota de quién manda. CSS muerto .note-card retirado (v5.7 la reemplazó por .block). El fixture propio violaba la regla ≤76 y disparaba el aviso en CADA corrida (efecto 'cry wolf'): re-envuelto con las MISMAS palabras + 2 casos nuevos en selftest (el aviso dispara cuando debe / la muestra oficial no lo dispara) = 13 pruebas. Conexión con el Centro de Mando declarada (estándar 9). -->
<!-- skill v5.10 · 2026-08-23 (auditoría golden-skill-auditor v1.16, 919→ORO) · (1) v5.9 quedaba SIN DECLARAR: sus dos cambios vivían solo en comentarios del CSS — se declaran abajo; (2) `::: nombre Título` (bloques con estilo, v5.7) faltaba en references/content-format.md, el archivo que enseña el formato: agregado a la tabla y con sección propia; (3) geometry.card_max_mm de golden-brand.json decía 250 cuando el valor real derivado es 246 (área útil − colchón de 20mm) — corregido y marcado como derivado; (4) `.note-card` era CSS muerto desde v5.7 (nada lo genera; lo reemplazó `.block`) — retirado; (5) el puntero al logo naranja `PROYECTOS/SKOOL/logo-comunidad-golden.svg` estaba MUERTO (esa carpeta ya no existe) en 3 archivos — corregido; (6) selftest 11→13: prueba de bloque con estilo (v5.7) y prueba de que el aviso de líneas largas (v5.8) se dispara — antes esas versiones no tenían red de regresión; (7) ORDEN FER declarado en Verificación: auditar el PDF CANDIDATO y solo instalarlo si dice APROBADO; (8) docstrings al día (selftest 1-4→13 pruebas, audit_pdf --palette). Conexión: los cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO. -->
<!-- skill v5.9 · 2026-08 (declarada retroactivamente en v5.10; vivía solo en el CSS) · (a) `code.inline` con break-inside:avoid + white-space:nowrap — un span de código en línea que caía en el borde se partía a la mitad de la palabra (medido: informe un cliente, pág 12→13, "SIN MOVIMIENTOS" rebanado); (b) rediseño de tablas: el oro pasa de RELLENO de cada th a ACENTO (borde inferior 2px) + filas alternas y más padding — 24 tablas de un informe inundaban la hoja de amarillo y se veía aglomerado (medido por FER sobre el PDF real) -->
<!-- skill v5.8 · 2026-08-07 (centro de mando, cosecha del chat ESTUDIO 360 DENTAL un producto de cliente Chile) · LÍNEAS LARGAS EN TARJETAS: dentro de una tarjeta monoespaciada, una línea de más de ~76 caracteres se ENVUELVE al renderizar y la compuerta verbatim la reporta como "espaciado/orden alterado" (pasó con dos prompts de imagen; se resolvió reescribiéndolos a 72-84 chars/línea). Regla de redacción "líneas de tarjeta ≤ 76 caracteres" en content-format.md + build_pdf.py AVISA antes de renderizar con tarjeta y línea exactas (⚠️ LÍNEAS LARGAS EN TARJETAS por stderr) -->
<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): references/brand.md quedó citada desde el SKILL.md — era el único componente de la skill sin cita (hueco genuino confirmado por el inventario v1.8 del auditor); util, se cita, no se retira. -->
<!-- skill v5.7 · TEMAS: `--css tema.css` anexa una hoja que solo redefine variables/colores (la identidad Golden queda intacta por defecto) y `--palette paleta.json` hace que audit_pdf.py juzgue con OTRA paleta permitida. Ademas bloques con estilo `::: nombre Titulo … :::` -> <div class="block nombre"> con el contenido procesado como Markdown (para que un documento largo respire: destacados, avisos, tablas de datos). Origen: manual M3 del MBA con la identidad naranja/cian del programa -->
<!-- skill v5.6 · FIGURAS: `![Pie](ruta.svg){60%}` en una línea sola = figura atómica (imagen + pie numerado que nunca se separan ni se parten entre páginas), incrustada en base64, ruta relativa al .md, SVG como vector. Origen: manual M3 del MBA (Meta Business Manager, 2026-08-04) — un manual de pasos sin pantallas no enseña. Cubierto por 2 pruebas nuevas en selftest.py (11/11) -->
<!-- skill v5.5 · 4 defectos medidos en producción (guía logística 27 págs, 2026-08-03): (1) CRÍTICO ligaduras de JetBrains Mono corrompían el copy-paste (>> salía como <>, // como </) → font-variant-ligatures:none + "liga" 0,"calt" 0 en .prompt-body y code.inline, trampas >> // https:// <<X>> horneadas en selftest-sample; (2) norma FER portada COMPACTA: título+índice en la MISMA hoja (adiós hoja 70% vacía que "da pereza leer"); (3) tablas largas SÍ se parten con thead repetido y filas enteras; (4) colchón de tarjeta 8→20mm (el encabezado precedente comía el margen y el propio auditor tumbaba PDFs del motor); extra: compuertas ignoran selectores de variación de emoji U+FE0F (falso "no idéntico" con ⚠️) -->
<!-- skill v5.4 · norma FER: TODO PDF Golden abre con página de CONTENIDO (índice línea por línea de todo lo que trae el documento + cuántos textos copiables tiene cada parte). Se genera SOLA desde los encabezados en build_pdf.py (outline + build_index, CSS .toc, flag --no-index para la excepción). Origen: PDF Dental un producto de cliente 2026-07-25 -->
<!-- skill v5.3 · norma FER: copys/prompts múltiples = tarjetas numeradas separadas (jamás párrafo corrido); marcadores [PENDIENTE] en negrita, no backticks (mono inline cruza páginas). Origen: PDF Libido UP 2026-07-25 -->
<!-- skill v5.2 · verbatim_check ahora despoja front matter/encabezados/pipes para comparar bien contra .md (adiós falsos positivos); referencia a logo-golden.svg.orig eliminada (no existía) — si se re-sube un logo nuevo, redimensionarlo igual antes de incrustarlo -->
<!-- skill v5.1 · logo oficial optimizado 1.4MB→195KB (PNG 444px cuantizado con alfa, idéntico a la vista a 74px) -->
<!-- skill v5 · auditor sin falsos positivos (dos tarjetas seguidas ≠ corte; texto normal al borde = aviso, no tumba veredicto), normalización tipográfica compartida en las dos compuertas (elipsis/comillas/guiones), logo oficial = emblema Golden Group Community, selftest 9/9 -->
<!-- v4 · fuentes OFL incrustadas (estáticas anti-Type3), compuerta verbatim con doble chequeo, PDF etiquetado, tablas, selftest adversarial -->

Este skill garantiza que todo PDF que Golden entrega a su comunidad se vea
profesional, tenga la identidad de marca y — lo más importante — que los
**prompts copiables nunca se partan entre páginas**. La gente copia y pega
esos prompts; un bloque cortado a la mitad es inaceptable.

Regla operativa: **siempre que leas o generes un PDF para Golden, déjalo con
esta perfección.** No entregues un PDF "a mano" si este skill puede hacerlo bien.

## NORMA FER · todo PDF abre con una página de CONTENIDO (v5.4)

Después de la portada va **SIEMPRE** una página de **CONTENIDO** que dice, **línea por línea, todo
lo que hay en el documento**: cada sección y cada subsección en el orden en que aparecen, con un
número al lado que indica **cuántos textos copiables** trae esa parte. Quien abre el PDF entiende de
un vistazo todo lo que compró: investigación, precios, estructura de ads, prompts de imágenes,
prompt de Chatea, y lo que sea que traiga.

- **Se genera SOLA** en `build_pdf.py` (`outline()` + `build_index()`), leyendo los `##` y `###` del
  Markdown y contando las tarjetas de prompt de cada sección. **Nadie la escribe a mano** y por eso
  nunca queda desactualizada cuando el contenido cambia.
- Por eso los encabezados del contenido tienen que ser **descriptivos y en orden de ejecución**:
  ese texto es exactamente el que se ve en el índice. Un `### Copy 7 · Bloque de honestidad` se lee
  perfecto en el índice; un `### Otro más` no.
- Cabe en **una página** en la mayoría de documentos (dos columnas, tipo compacto). Si el documento
  es enorme, fluye a la siguiente página sin cortar ninguna línea.
- **Excepción única:** `--no-index` para documentos de una sola pieza (un PDF de un solo prompt,
  una carta). En entregables de proyecto, informes, paquetes de lanzamiento y PDFs de prompts, va.

## REGLA INVIOLABLE · el texto no se toca

Este skill **solo cambia la estructura, la maquetación y la arquitectura visual**
del PDF para que se vea perfecto. **NUNCA modifica el contenido.** El texto del
usuario es sagrado y va tal cual: mismas palabras, misma ortografía, misma
puntuación, mismo orden, mismos saltos de línea dentro de cada prompt. No se
corrige, no se "mejora", no se resume, no se reescribe, no se traduce, no se le
quitan ni añaden signos. Lo único permitido es envolverlo en tarjetas, secciones
y portada, y ajustar tamaños/márgenes/paginación.

La única excepción es texto que el usuario te pida **crear desde cero** (p.ej. un
subtítulo de portada si no lo dio). Eso sí sigue el estilo Golden. Pero el
contenido que ya existe — sobre todo los prompts — se preserva carácter por
carácter. Ante la duda, no lo cambies.

## Qué hace

1. **Construye** un PDF Golden desde contenido (Markdown-Golden) — para cuando
   aún no hay PDF o cuando el existente hay que rehacerlo. Incluye **portada +
   página de CONTENIDO automática** (norma FER v5.4) + tarjetas atómicas.
2. **Audita** un PDF existente y reporta fallos de marca, márgenes, colores y
   paginación (bloques al filo del borde = riesgo de corte).
3. **Arregla**: extrae el contenido del PDF viejo, lo pasa al formato Golden y
   lo regenera con bloques atómicos. Así el arreglo es garantizado, no cosmético.

## Cuándo usar cada camino

- **"Hazme un PDF de estos prompts" / no hay PDF todavía** → construir (paso A).
- **"Revisa/arregla este PDF"** → auditar (paso B) y, si algo falla o si el
  usuario quiere el resultado perfecto, reconstruir (paso C).
- Ante la duda, **audita primero** para diagnosticar y luego decide.

---

## Antes de correr nada · el intérprete

Los scripts necesitan `playwright`, `pdfplumber`, `Pillow` y `pypdf`. **No existe
el binario `python` en el Mac de Golden** (solo `python3`), y las dependencias
viven en un entorno propio. Resuelve el intérprete UNA vez y úsalo en todos los
comandos de esta skill:

```bash
PY=~/.golden/pdfenv/bin/python; [ -x "$PY" ] || PY=python3; echo "$PY"
```

Ese es el `$PY` que aparece en los comandos de abajo. El entorno `~/.golden/pdfenv`
es el oficial de Golden para PDFs; si algún día no está, `python3` sirve mientras
tenga las cuatro dependencias. Si falta alguna:

```bash
$PY -m pip install playwright pdfplumber pillow pypdf && $PY -m playwright install chromium
```

Escribir `python` a secas falla con `command not found` — por eso los comandos de
esta skill nunca lo usan.

## Conexión con el ecosistema

**Fábrica: chat ✅ SKILL golden-pdf-check.** Ahí se repara esta skill; los demás chats
reportan defectos medidos en vez de editarla (REGISTRO-FABRICAS lee esta línea para
resolver el dueño, y los actores de auditoría masiva la respetan). Se declara AQUÍ, en el
archivo, y no solo en memoria: una fábrica que vive solo en la memoria del ecosistema
desaparece si alguien reformula esa nota.

Los cambios relevantes de esta skill (defectos medidos en producción, normas
nuevas de FER sobre la maquetación) se reportan a **🧠 GOLDEN - CENTRO DE MANDO**,
que es quien decide si la lección se retransmite a otros chats. Varias versiones
de esta skill nacieron así: un chat construyendo un entregable real midió el
defecto y lo mandó a la fábrica. Ese circuito es el que la mantiene viva.

---

## Paso A · Construir un PDF Golden

1. Prepara el contenido en **Markdown-Golden**. Lee `references/content-format.md`.
   Lo esencial: cada prompt que se copia va dentro de una tarjeta:
   - bloque ` ``` ` … ` ``` ` (monoespaciado), o
   - bloque `::: prompt Título` … `:::` (prosa).
   Añade un front matter con `title`, `subtitle`, `kicker`, `author` para la portada.

2. Genera el PDF:
   ```bash
   $PY scripts/build_pdf.py contenido.md salida.pdf
   ```
   El script arma el HTML con la identidad Golden (`assets/golden-print.css`),
   corre el auto-fit (`assets/autofit.js`) y renderiza a PDF. Al terminar corre
   una **compuerta verbatim**: re-extrae el texto del PDF y confirma que cada
   prompt salió idéntico. El JSON de salida trae `engine`, `cards`,
   `verbatim: {ok, fails}` y `fit_warnings` (prompts que quedaron muy reducidos
   o escalados: conviene partirlos en el contenido; salen también por stderr).
   Con `--strict` el script falla (exit 3) si el texto no coincide 100%; con
   `--no-verify` se omite la comprobación.

   **Bloques con estilo (v5.7):** `::: nota Título` … `:::` produce un
   contenedor atómico con clase propia. Sirve para que un documento largo no
   se lea apelmazado: destacados, avisos, tarjetas de datos. A diferencia de
   la tarjeta de prompt, el contenido de adentro SÍ se procesa como Markdown.

   **Documentos que NO se emiten bajo la marca Comunidad Golden** (el MBA es el
   caso: su emisor formal es la empresa, y la comunidad no se nombra en material
   externo) usan `--logo ruta/al/sello.png` para la portada y `--footer "Texto"`
   para el pie, y `--css tema.css` para la paleta. El tema es una hoja que se
   anexa DESPUÉS de la de marca y solo redefine variables y colores, así que la
   identidad Golden nunca se toca. Para auditarlos, `audit_pdf.py --palette
   paleta.json` con los hex permitidos de esa marca. Sin esos flags, todo sigue
   siendo Golden.

   El PDF sale **etiquetado/accesible** (StructTreeRoot) con Playwright. El
   contenido soporta encabezados, listas, separadores, **tablas** (`| a | b |`
   con línea `| --- |`), **figuras** (`![Pie](ruta.svg){60%}` en una línea sola:
   imagen incrustada + pie numerado, atómicos como las tarjetas) y las dos
   formas de tarjeta de prompt. El texto de las
   tarjetas se escapa literal SIEMPRE (nunca se aplica markdown al prompt).

   **Fuentes de marca incrustadas:** el documento usa Inter (títulos/cuerpo) y
   JetBrains Mono (prompts), incrustadas en base64 desde `assets/fonts/` (OFL),
   así se ve idéntico en cualquier equipo. Son estáticas y con el Área Privada
   del cmap eliminada a propósito: si se usara la versión variable, Chrome las
   convierte en Type 3 y mapea mal caracteres como los corchetes `[ ]`,
   corrompiendo el copiar-pegar. No reemplaces estas fuentes por las variables.

3. Verifica el resultado (ver "Verificación" abajo). Si un prompt salió con el
   tipo muy reducido, probablemente convenga **partirlo en dos** (decisión de
   contenido) — avísale al usuario en vez de dejarlo microscópico.

### Motor de render

- **Preferido y ya instalado: Playwright (Chromium).** Da numeración de página
  en el pie ("Comunidad Golden · Página X de Y") y ejecuta el auto-fit midiendo
  al ancho exacto del PDF. Es el motor por defecto. Si algún día falta:
  ```bash
  $PY -m pip install playwright && $PY -m playwright install chromium
  ```
- **Fallback: Chrome headless** (el script lo detecta solo). Mantiene bloques
  atómicos y ahora mide al ancho correcto (`--window-size`), pero sin numeración
  en el pie. Si solo hay este, avísale al usuario que para la numeración conviene
  Playwright.

---

## Paso B · Auditar un PDF existente

```bash
$PY scripts/audit_pdf.py documento.pdf --json informe.json
```

Revisa:
- **Márgenes** invadidos.
- **Bloques cortados**: (a) contenido pegado al borde inferior del área útil en
  una página que no es la última; (b) **detección de bloques monoespaciados
  (prompts/código) que continúan de una página a la siguiente** — lo peor para
  copiar y pegar. Esto sí atrapa un prompt partido en un PDF ajeno.
- **Colores fuera de marca** por **muestreo de píxeles** (renderiza el PDF a
  imagen y mide el % de área con color fuera de la paleta). Funciona con
  cualquier PDF (Canva, Word, Chrome), no depende de cómo se codificó el color.
  Reporta los tonos foráneos dominantes.

Imprime un informe en Markdown y guarda el JSON. Requiere `pdfplumber`; la
auditoría de color por píxeles usa `Pillow` + `pdftoppm` (poppler) — si faltan,
cae al análisis por objeto. Con solo `pypdf` hace un análisis básico.

**Semántica del veredicto:** solo tumban el veredicto los problemas REALES de
copy-paste — un bloque mono cortado entre páginas (`mono_split`) o un bloque de
prompt al filo del borde (`bottom_risk` con `mono: true`). El texto normal
(párrafos) que termina cerca del margen es paginación normal y sale como
**aviso no bloqueante**. Dos tarjetas en páginas seguidas NO son un corte: el
auditor detecta la cabecera "PROMPT · COPIAR" de la página siguiente y las
distingue.

El auditor es **heurístico y advisory**: señala síntomas. No puede garantizar
por sí solo que un bloque no se corte — eso solo se garantiza reconstruyendo.
Preséntale al usuario el veredicto y las 2-3 cosas más importantes a arreglar,
no un volcado crudo del JSON.

---

## Paso C · Arreglar (reconstruir) un PDF

Cuando la auditoría marca problemas o el usuario quiere el resultado perfecto:

1. Extrae el contenido del PDF viejo (texto por página). Usa `pdfplumber`
   (`page.extract_text()`) o, si el usuario tiene la fuente original, pídela.
2. Reescríbelo en Markdown-Golden: identifica qué partes son **prompts
   copiables** y enciérralas en tarjetas ` ``` ` / `:::`. Respeta el contenido
   textual del usuario — no lo reinventes, solo lo reestructuras.
3. Reconstruye con `build_pdf.py` (Paso A) y verifica.
4. **Compuerta verbatim obligatoria:** compara el texto del PDF viejo contra el
   nuevo para garantizar que no cambió ni una palabra:
   ```bash
   $PY scripts/verbatim_check.py --old viejo.pdf --new nuevo.pdf
   ```
   Exit 0 = idéntico; exit 3 = hay diferencias (te lista qué segmentos). Si hay
   diferencias, NO entregues: revisa la extracción y corrige. Nunca alteres el
   texto para "cuadrar" la comparación.
5. Entrega el PDF nuevo junto a un resumen corto de qué se corrigió (solo
   estructura/maquetación, nunca contenido).

---

## Verificación (siempre antes de entregar)

**ORDEN OBLIGATORIO (norma FER):** *la skill revisa, aprueba, y ahí mismo sí se
entrega.* La auditoría va **ANTES** de instalar el PDF en su destino, no después
de anunciarlo. El flujo correcto es: `autoprueba.py` (la skill está sana) →
renderizar a un **PDF candidato** en una carpeta temporal → `audit_pdf.py` sobre
ese candidato → **solo si dice APROBADO** se copia al destino final y se avisa.
Nunca sobrescribas el PDF bueno con uno sin auditar, ni digas "listo" antes del
veredicto.

Confirma que el PDF quedó bien:

- **Bloques atómicos:** audita el PDF nuevo con `audit_pdf.py`; el veredicto
  debe ser APROBADO (`mono_split` vacío y sin bloques de prompt al filo). Los
  avisos de texto normal cerca del borde no bloquean. Si un PROMPT sí roza el
  borde, sube su prioridad para partirlo en contenido.
- **Marca:** portada con logo y kicker "Comunidad Golden", dorado presente,
  fondo claro, pie "Comunidad Golden … Página X de Y".
- **Márgenes:** nada tocando el borde.
- Si puedes, abre el PDF (o su HTML intermedio con `--save-html`) para una
  revisión visual rápida.

### Prueba de regresión (self-test)

Si tocas el CSS, el parser o el auto-fit, corre el self-test antes de dar por
buena la skill. Construye una muestra y verifica build + verbatim + anti-corte:

```bash
$PY scripts/autoprueba.py
```

Debe imprimir `TODO OK`. Si algo sale FAIL, arréglalo antes de usar la skill en
material real. La muestra que construye es `assets/autoprueba-muestra.md`, que trae
horneadas las trampas de copy-paste (`>>`, `//`, `https://`, `<<X>>`, un emoji y
una tarjeta larga): **no edites ese texto**, es el fixture de regresión.

**Dependencias por script** (para que un FAIL se lea bien): `build_pdf.py` y
`audit_pdf.py` necesitan `pdfplumber` (compuerta verbatim y auditoría) y
`playwright` (motor con numeración); la auditoría de color usa `Pillow` +
`pdftoppm`; `autoprueba.py` además usa `pypdf` para leer las fuentes incrustadas.
Todas son **opcionales con degradación**: si falta una, esa comprobación sale
FAIL con el motivo y el resto sigue — ninguna tumba la corrida. Si el intérprete
del sistema no las tiene, corre los scripts con uno que sí (un venv propio) en
vez de asumir que la skill quedó mal.

## Personalización de marca

Todo vive en `assets/`:
- `golden-brand.json` — tokens (colores, geometría, paleta permitida para el auditor). El porqué de cada valor y la fuente de verdad de la identidad están en `references/brand.md`.
- `golden-print.css` — estilo de impresión (portada, tarjetas, tablas).
- `logo-golden.svg` — **emblema oficial Golden Group Community** (el círculo
  dorado/negro con las GG; es el PNG oficial incrustado en un envoltorio SVG).
  (El naranja de comunidad que se usó de origen ya NO está en disco: la carpeta
  `PROYECTOS/SKOOL/` fue retirada. Si algún día se quiere volver a él, hay que
  re-subir el archivo; no queda copia dentro de la skill.)
- `autofit.js` — lógica anti-corte. El alto máximo por tarjeta (`--card-max-mm`,
  variable CSS) lo **deriva build_pdf.py de la geometría real** (única fuente de
  verdad: área útil − colchón) y lo inyecta; el valor escrito en el CSS es solo
  el fallback si el HTML se usa suelto. No es un flag de línea de comandos.

## Estilo de textos (marca Golden)

Cualquier texto que redactes para estos PDFs sigue las reglas de Golden:
- **Nunca** signos de apertura `¿` ni `¡`; solo el de cierre. Suena más humano.
- Tono claro y directo, sin relleno.
- El contenido de los prompts es del usuario: respétalo literal, no lo adornes.

## Norma de FER: copys y prompts SIEMPRE numerados en tarjetas separadas (2026-07-25)

Cuando el contenido trae VARIOS elementos copiables de la misma familia (5 copys de anuncio,
5 titulares, varios prompts de imagen, guiones), la maquetación obligatoria es:
- **Cada texto principal = SU PROPIA tarjeta numerada** con título en el fence
  (` ``` Texto principal 1 `, ` ``` Texto principal 2 `…). Uno abajo del otro, bien separados.
- Elementos de una línea (titulares, descripciones) SÍ pueden ir juntos en UNA tarjeta,
  pero **uno por línea, numerados** (`1. …` `2. …`), jamás en párrafo corrido.
- **PROHIBIDO** el párrafo que une varios copys con "· 1. … 2. … 3. …": mata el copy-paste,
  ahoga los números y da pereza leerlo. Si el autor del contenido lo trae así, la skill lo
  reestructura en tarjetas (es maquetación, no cambio de texto — el contenido queda idéntico).
- Marcadores tipo `[PENDIENTE …]` en texto corrido van en **negrita**, no en backticks: el
  monoespaciado en línea puede cruzar de página y el auditor lo marca como prompt cortado.
- Ojo autor: la skill garantiza tarjetas atómicas, pero QUÉ es tarjeta lo decide quien escribe
  el Markdown-Golden. Ante lista de copys, la decisión correcta es SIEMPRE una tarjeta por copy.
