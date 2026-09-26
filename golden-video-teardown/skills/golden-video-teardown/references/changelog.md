# Historial de golden-video-teardown

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- skill v1.6 · 2026-09-06 (auditoría golden-skill-auditor, 965→985/1000) · Único hallazgo real: la línea bajo el H1 apuntaba al historial pero no traía la versión vigente en el patrón de la casa `<!-- skill vX.Y · qué cambió -->`. Se corrige el comentario del H1 para que declare la versión de un vistazo, sin mover contenido de este archivo. Validador oficial: exit 0 antes y después. Blindaje: chflags uchg, restaurado al cierre. -->

<!-- skill v1.5 · 2026-08-23 (centro de mando) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

<!-- skill v1.4 · 2026-08-21 (auditoría golden-skill-auditor) · Reparación tras auditoría 840/1000 (BRONCE):
     (1) corregido el sobre-promesa de Instagram/Facebook en el description y el Paso 0 — antes sonaba
     verificado, ahora dice explícitamente que solo YouTube/TikTok están medidos; (2) nuevo Paso "Intake"
     al inicio (producto/país/moneda/rendimiento se piden UNA vez, no goteados); (3) nuevo Paso 5 de QA
     con checklist de "terminado" contra los 6 Principios, antes de guardar; (4) ejemplo real entrada→salida
     agregado a plantilla-teardown.md; (5) ruta de mlx-whisper ya no asume Python 3.9 hardcoded, se resuelve
     en vivo; (6) blindaje: chflags uchg (documentado aquí, no solo en el inventario). Blindada de nuevo al
     cierre de esta reparación. -->

<!-- skill v1.3 · 2026-08-02 (centro de mando) · ALCANCE REAL DE yt-dlp EN TIKTOK, medido sobre un video real: la DESCARGA funciona (bajo formato 1080p) y los METADATOS tambien (canal, 49.400 vistas, 986 likes), pero --write-comments devuelve comments: 0. El teardown segundo a segundo de un TikTok sale COMPLETO; la capa de comentarios no. Para esa: Chrome MCP o pegado. Instagram/Facebook siguen sin probar y se dice que no se probaron -->

<!-- skill v1.2 · 2026-08-01 (centro de mando) · yt-dlp 2026.07.04 INSTALADO Y PROBADO: el Paso 0 pasa de "pendiente-con-dueño" a operativo, flujo URL→teardown completo. + Se añade la descarga de COMENTARIOS con like_count (30 medidos): los más votados son objeciones/elogios ya validados por la audiencia, material directo para fortalezas/debilidades y para el brief. + Regla Cero ampliada a 3 modos de fallo (alucinación / señuelo con title poblado / muro anti-bot sin campo json): la verificación que caza los tres es "el dato responde a lo que pedi?" -->

<!-- skill v1.1 · 2026-07-31 (centro de mando) · ACEPTA URL: nuevo Paso 0 de descarga (yt-dlp para YouTube/TikTok/IG/FB) — antes solo aceptaba ruta local, así que un link no se podía analizar. yt-dlp YA ESTÁ INSTALADO (v2026.07.04, verificado el 2026-08-11 — el pendiente quedó resuelto); ffmpeg SÍ (v8.1.2). Mientras tanto, 3 salidas sin bloquear: metadatos por Firecrawl (YouTube da título/canal/vistas/likes reales, postprocesador nativo — pero NO el archivo), descarga manual, o Meta Ad Library. Regla Cero heredada: metadata.title vacío = json alucinado -->

<!-- skill v1.0 · teardown segundo a segundo + fórmula/brief · extract_frames.sh (ffmpeg) + STT opcional (hyperframes transcribe / mlx-whisper / openai-whisper) -->
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 937 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
