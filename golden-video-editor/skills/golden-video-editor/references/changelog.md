# Historial de golden-video-editor

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 854 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill GVE1.9 · 2026-08-31 (CdM) · compuerta de la congelacion de Higgsfield (estandar de FER 30-ago repartido por el CdM): tecnica 2 remite el movimiento a HyperFrames (0 creditos), video de Higgsfield CONGELADO, costo-antes para imagenes. Reversible al levantar la congelacion. -->

<!-- skill GVE1.8 · 2026-08-31 (CdM, fila del FILTRO) · SEGUNDA COSECHA de la MISMA fuente externa:
GVE1.7 tomo la estructura del carrusel; GVE1.8 toma la capa numerica del brief PDF completo (6 pag)
que llego despues. No es duplicado — son dos entregas del mismo autor con niveles de detalle distintos.
13 criterios numericos instalados donde cada uno trabaja (intake, corte, subtitulos, b-roll, sonido,
render, fallos). La prueba del sonido apagado cierra el par asimetrico del 85%: copywriting lo sabia
(5 menciones), el editor casi no (1) — ahora el lado que MONTA tambien lo ejecuta. -->

<!-- skill GVE1.7 · 2026-08-31 (CdM, fila del FILTRO — origen externo declarado: carrusel de edicion
con IA; se toma la PIEZA, no el archivo) · LEY DE ORDEN instalada VIVA antes del pipeline: cortar →
subtitular → ilustrar → sonorizar con el porque de cada posicion (dependencias, no estilo), las 4
instrucciones textuales de maquina, y el bloque "lo que la maquina NO decide". Reglas de b-roll (donde
se nombra, objeto sobre negro, NO stock) y sfx-desacoplado ancladas en los Pasos 3 y 4. Hueco medido
antes: orden 0, subtitular 0, b-roll 0. El pipeline ya tenia el macro-orden correcto; esto le da el
porque y el lenguaje de instruccion. -->

<!-- skill GVE1.6 · 2026-08-27 (chat FILTRO) · FIX: multicamara-una-camara.md quedo DORMIDO en GVE1.5 — citado en el sello pero SIN disparador en el cuerpo, o sea invisible para el flujo. Lo cazo el detector golden-capacidad-huerfana, que estrena chequeo de RECURSOS DORMIDOS a peticion del CdM tras el mismo fallo en golden-web (catalogo-de-estilos). Mismo error mio dos veces la misma noche. Disparador puesto en el Paso 2, que es donde se cortan. Barrido del ecosistema: 1 dormido de 243 referencias — este. -->

<!-- skill GVE1.5 · 2026-08-26 (chat FILTRO, autoridad de FER) · NUEVO references/multicamara-una-camara.md. Destilado de 2 PDFs de NinoDirector que FER envio el 16-ago y llevaba 10 dias en DESTILADOS sin que ninguna skill lo nombrara. Barrido previo: capacidad NUEVA, 0 de 89 skills mencionaban multicamara, punch-in ni encuadre. Numeros: cambio de encuadre ~1min30, nunca cada 10s, punch-in 113% con tope duro 125%, ventana de silencio 1,5s y si no hay silencio NO se corta. Regla que lo hace funcionar: el frontal SE GUARDA para el CTA. Enlaza con golden-imagen-arena para generar los 3 fondos. -->

<!-- skill GVE1.4.1 · 2026-08-24 (centro de mando): bump que la reparación del barrido B dejó sin subir — 5 skills editadas sin bump las veía intactas el censo (verificador de cierre). -->

<!-- skill versión GVE1.4 · 2026-08-23: Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->

<!-- skill versión GVE1.3 · auditoría golden-skill-auditor 2026-08-21: cierra la inconsistencia de versión (el cuerpo ya traía los cambios de GVE1.2 pero la línea "Versión:" y el Changelog se habían quedado en GVE1.1 — ahora coinciden); documenta el blindaje (chflags uchg) en el propio SKILL.md, no solo en el filesystem; completa el ejemplo de tts con --output -->

<!-- skill versión GVE1.2 · auditoría 2026-07-25: transcribe SIN --output (ese flag es solo para sidecar SRT/VTT; el transcript.json se escribe solo); añadido el andamio real del pipeline (npx hyperframes init --video y npx hyperframes render con quality/fps/format), que era el esqueleto que faltaba; voz em_alex marcada como no verificada; puntero a transcript-guide.md para filtrar tokens basura -->


## CENTRO DE MANDO · 2026-09-27 · GVE1.12 · LEY DE LOS REQUISITOS DEL USUARIO

Ley de FER del 02-sep: declarar ANTES lo que la skill necesita del usuario y pedirlo AL CORRER si falta. Desde golden-skill-auditor v1.22 la ley tiene casilla en `validar_arsenal.py`. Se agregó al principio el bloque "Requisitos", redactado con lo que esta skill USA de verdad (medido en su cuerpo y en sus scripts), sin agregar requisitos de más, y con qué hacer si falta: parar y pedirlo con nombre propio. A la fábrica se le informa por la bandeja: una fila no bloquea.
