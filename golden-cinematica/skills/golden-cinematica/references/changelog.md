# Historial de golden-cinematica

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## GC1.6 · 2026-09-27 · Ley de los requisitos del usuario (aplicó y numeró el CENTRO DE MANDO, que es su fábrica)

Se añadió el bloque de requisitos del SKILL.md: qué tiene que tener el usuario antes de arrancar, cada requisito marcado BLOQUEANTE o DEGRADABLE y qué pasa si falta (doctrina del CdM del 27-sep). Lo redactó el chat 🧰 ARSENAL Y SKILLS (fila P49, 4 pasadas del golden-verificador adversarial; en la última, ninguna falla nueva grave) y lo aplicó el CdM sin numerar: el número lo pone la fábrica al ratificar. Solo inserción: 0 líneas quitadas.

## GC1.5.1 · 2026-09-24 · Lo que el verificador encontró en GC1.5

El `golden-verificador` revisó GC1.5 sin ver cómo se construyó y encontró dos fallas reales:

- **`barrido_encimes.js` daba verde falso sin `<main>`.** Solo buscaba en `main *, nav *, .brand`. La
  misma página sin `<main>` salía con 0 textos revisados y "encimes: []". Ahora barre todo el body
  (sin script, style, noscript ni template) y devuelve error si no encuentra ningún texto. Probado en
  Chromium sin ventana: sin `<main>`, a 390 y a 1280, encuentra el par montado y la escena huérfana.
- **`vidrio_templado.js` tenía un contrato incompleto y vocabulario de su página.** Declaraba 6 de
  los 11 nombres que usa. Faltaban `seg`, `ease`, `easeOut`, `dibujarObjeto` e `introK` como
  variable. Se midió el contrato real con un barrido de identificadores libres y se renombró lo que
  era del negocio de origen (ids de video, la función que dibuja el objeto, comentarios). Prueba en
  Chromium con SOLO el contrato declarado: la entrada corre (introK 0,77 a los 3,5 s). Sin `seg`, el
  try/catch de cada cuadro la salta en silencio (introK = 1 al instante). Esa trampa quedó escrita en
  la cabecera: tras adaptarla, se mira la consola, no la pantalla.
- `data-rally` pasó a `data-cruce` en la pieza 4.

## GC1.5 · 2026-09-24 · Página por escenas

Origen: una propuesta comercial por escenas hecha para un cliente (23 y 24-sep), medida en
computador y en iPhone. El CdM decidió el 24-sep que ese método vive aquí y no en golden-presenta, que
conserva las diapositivas. Paquete armado en `STACK-GOLDEN/HORNEADO-PENDIENTE/golden-cinematica/`, con
el barrido de datos del cliente en 0 menciones sobre 4 de 4 archivos, y aplicado cuando FER pasó la
sesión del CdM a "Omitir permisos".

Qué entró: `references/piezas-pagina-por-escenas.md` (12 piezas y 5 reglas),
`scripts/barrido_encimes.js`, `scripts/puntos_globo.py` y `scripts/referencia/vidrio_templado.js`.

Lo que se corrigió al entrar, porque venía cableado a su página:
- `barrido_encimes.js` llamaba a `{ hero, coleccion, preventa, jugada }` por nombre fijo: en cualquier
  otra página daba ReferenceError. Ahora usa `window.ESCENAS` o `window[nombre]`, declara las escenas sin
  función, mide sola la barra fija y respeta `data-barrido-ignorar`. 🔴 Además se colgaba en silencio con
  la pantalla oculta: `innerHeight` vale 0, el paso también, y el bucle nunca avanzaba. Ahora se niega.
  Prueba en los dos sentidos sobre una página hecha para eso: 1 par montado encontrado, 0 falsos, la
  escena huérfana declarada.
- `puntos_globo.py` leía y escribía en rutas de su proyecto (`../sitio/`). Ahora recibe entrada y salida
  por argumento y sale con código 1 si falla un control. Corrido contra world-atlas@2: 9.005 puntos,
  Bogotá y Madrid en tierra, el Atlántico en mar, y el mapa de control mirado.

Description: se quitó "Motor: Three.js por importmap…" (ya está en "Cómo se entrega") y se añadió
"una página que se lea haciendo scroll por escenas". No se usa la palabra "propuesta", que dispara
golden-presenta.

## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 952 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->

<!-- skill GC1.4.3 · 2026-08-26 (chat FILTRO, autoridad de FER) · puntero a golden-web/references/estandar-movimiento.md, destilado de review-animations (skill instalada que ninguna Golden nombraba). Esta skill tenia el EFECTO pero no los NUMEROS: medido, 0 menciones de ease-out, scale(0, transform-origin, @starting-style y springs. Solo se anadio el puntero: nada mas tocado. -->

<!-- skill GC1.4.2 · 2026-08-26 (chat FILTRO, autoridad de FER; golden-cinematica es del CENTRO DE MANDO por REGISTRO-FABRICAS) · references/vocabulario.md: +1 fila, HORIZONTAL SCROLL (seccion con overflow hidden + pista movida por translateX() atada a ScrollTrigger). ORIGEN: carrusel de gowtham_techie con 6 efectos de scroll. MEDIDO antes de tocar: 5 de los 6 ya estaban cubiertos entre esta skill y golden-web (scroll trigger 5/5, pin 13/7, parallax 1/7, scroll progress 0/2, scroll-linked 3/4) y el stack completo tambien (gsap 14, scrolltrigger 10, lenis 5, three 54). El unico en CERO era horizontal scroll. Aporte real del carrusel: 1 de 6, no 6 de 6. Nada mas tocado. -->

<!-- skill GC1.4.1 · 2026-08-24 (centro de mando, remediación del verificador de cierre): línea de RUTA del cerebro en el Paso 0 (las lectoras ordenaban LÉELO PRIMERO sin decir dónde — un chat limpio no podía ejecutar la orden) + bump que las ediciones del 23-24 dejaron sin subir. -->

<!-- skill GC1.4 (2026-08-23) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->

<!-- skill GC1.3 (2026-08-21) · auditoría golden-skill-auditor: (1) desambigua la cita a `references/estilo-agencia-premium.md` — vive en golden-web, no localmente, se escribía sin dueño y se leía como archivo propio; (2) suma sección "Cuando algo falla o falta" con plan de degradación explícito (CDN caído, sin render de fondo, 60fps no alcanzado en móvil, tokens no entregados por el usuario) — antes no había manejo de error declarado; (3) TOC en references/recetas.md (309 líneas, pasaba el umbral de 300 sin índice). Blindaje: chflags uchg (quitar con chflags -R nouchg, reponer con chflags -R uchg) — mecanismo documentado aquí por primera vez -->

<!-- skill GC1.2 (2026-08-02) · filtro de 2 reels de efectos (code.xr OTP v5 · code_and_chill MENISCUS): dos familias NUEVAS que el vocabulario no tenia — ESTADOS (success state animado, carga en el boton, validacion en vivo, progreso por segmentos) con la nota de que en contra entrega la confirmacion NO es decoracion sino la venta (el cliente dio sus datos sin pagar y la duda reaparece como cancelacion al confirmar por WhatsApp), y NAVEGACION (morphing dock por path SVG y tangentes, sticky compacto, desplazamiento por vecindad). Ninguno de los 2 reels publica el codigo (piden comentar), asi que se documenta el PATRON, no la receta -->

<!-- skill GC1.1 (2026-07-27) · filtro de 9 reels: 5 términos nuevos al vocabulario de entrada y revelado (pixel/entrance reveal por grid, smooth loader con máscara, stacked sticky sections, fondo ligado al scroll) con la nota de que se hacen a mano en CSS/JS y no hace falta Framer -->

<!-- skill GC1.0 (2026-07-25) · nace de un diagnóstico de FER: "las páginas que me has hecho son 10 de 100". Destilado del análisis frame a frame de 6 sitios de Textura Agency (@textura.eu / getlayers.ai), donde se capturó el PROMPT REAL con sus tokens numéricos. El hallazgo central: la diferencia entre 10/100 y 100/100 no es la librería, es que el encargo lleva milisegundos, grados, radios y hex exactos en vez de adjetivos -->
