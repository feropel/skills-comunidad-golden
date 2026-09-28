---
name: golden-cinematica
description: >-
  Golden Group — WEB CINEMATOGRÁFICA 3D nivel awwwards. Construye páginas con escenas 3D
  reales (partículas que ondulan, objetos cromados, nubes que siguen el cursor, cabezas de
  puntos, orbes de vidrio), preloader con contador y cortina de revelado, fondo de video
  pre-renderizado y movimiento lento de cine. Método: TOKENS NUMÉRICOS EXACTOS
  (milisegundos, grados, radios, hex), jamás adjetivos. Úsala SIEMPRE que el usuario pida:
  una página "espectacular", "como las de awwwards", "con 3D", "futurista", "robótica",
  "cinematográfica", "que se vea cara", "con partículas", "con un objeto que gire", "que se
  mueva sola", "tipo Apple", "que la gente pregunte qué agencia la hizo", una página que se
  lea haciendo scroll por escenas; o cuando muestre
  de referencia un sitio con escena 3D, fondo animado o preloader. Dispara también para el
  HERO de una web que ya existe si el encargo es "súbele el nivel visual". No sirve para
  producto Shopify COD ni sitio corporativo simple.
---
<!-- Historial completo de esta skill: references/changelog.md. El cuerpo se paga en cada activación; el acta no. -->

# Golden Cinemática — el salto de "página" a "experiencia"

## Antes de empezar — lo que TÚ tienes que tener

Para construir la página **no necesitas cuentas ni llaves**. Lo que sí hace falta es para verificarla, y la vara de calidad no deja entregar sin eso. Por eso esta skill lo pregunta al arrancar y no al final.

| Qué necesitas | Tipo | Para qué | Cómo se consigue |
|---|---|---|---|
| **Un navegador que Claude maneje, a la vista** | Bloqueante para entregar | Correr `scripts/barrido_encimes.js` a 390 y a 1280 y mirar la consola. Con la pantalla oculta no corren las animaciones y el barrido se niega (su mensaje acepta emular 390x844) | El navegador de la app, visible, o Claude en Chrome |
| **Un celular de gama media** | Bloqueante para entregar | Medir los 60 fps del hero, como exige la vara de calidad: se miden en el celular, no en el Mac | El tuyo o uno prestado. Lo mides tú en el celular, con la página publicada o servida en tu red local, y le pasas el resultado a Claude. La skill todavía no fija el método: mientras no haya una cifra de fps, la entrega dice «60 fps NO medidos» (aunque una revisión a ojo no muestre saltos) y la página no se declara terminada |
| **Los colores de tu marca en hex**, o tu logo | Degradable | Los tokens de la fase 2: no se inventan colores | Se piden una vez al inicio con la plantilla de `references/vocabulario.md`; si no los tienes, se sacan del logo o de la paleta que ya tenga el proyecto |
| **Conexión a internet** | Degradable | Three.js se carga desde unpkg con la versión fijada en `references/recetas.md`, y el scroll cinemático carga GSAP desde cdn.jsdelivr.net | Si el CDN no responde, se reintenta una vez y se entrega el HTML con el importmap correcto, diciendo el corte |
| *Opcional:* el **cerebro de marca** (`golden-brand-brain`) | Degradable | La voz de la marca en los textos de la página | Si no existe, se ofrece crearlo; si sigues sin él, la entrega lo declara |
| *Opcional:* **un render o video para el fondo del hero** | Degradable | El mecanismo 5 | Lo pones tú, o sale de `golden-imagen-arena` o Higgsfield, que gastan créditos. Sin él, se arranca con la escena WebGL sola y queda como pendiente |
| *Opcional:* **tu hosting** | Degradable | Publicar la página (lo normal es un HTML en Vercel, con `all-deploy`) | Tu cuenta. Sin ella se entrega el HTML listo para publicar |
| *Opcional:* **Python 3 con Pillow** | Degradable | Solo el globo de puntos (`scripts/puntos_globo.py`) | Compruébalo con `python3 -c "import PIL"`. Si falta: con el Python de python.org, `pip3 install Pillow`; con el de Homebrew, `python3 -m venv ~/venv-cine`, `~/venv-cine/bin/pip install pillow`, y el script se corre con `~/venv-cine/bin/python3`. El mapa `land-110m.json` se descarga de cdn.jsdelivr.net, no viaja en la skill |

**Lo bloqueante para lo que depende de él:** sin el navegador a la vista o sin el celular, la página se puede construir, pero no se entrega como terminada; se dice qué falta medir. **Lo degradable se pide y se sigue** con lo que manda "Cuando algo falla o falta", y lo que quede sin hacer se marca como pendiente. Si no tienes algo, dime y te guío paso a paso.

## Paso 0 · Cerebro de marca (obligatorio antes de generar)

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.


**Versión:** `GC1.6` · Fábrica: chat centro de mando.

Esta skill existe por una razón concreta: las páginas Golden nombraban las librerías
correctas y aun así salían genéricas. El diagnóstico fue que **conocer el nombre de la
librería no produce nada**. Lo que produce es la receta con sus números.

El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta (buscar con find ANTES de crear, naming MAYÚSCULAS-CON-GUIONES) la declara `golden-brand-brain`: ante cualquier duda de ruta, invócala en vez de adivinar.

## La ley que manda sobre todas

> **Números, no adjetivos.**

"Un preloader elegante" no construye nada. Esto sí:

```
Preloader: HOLD_AT 90 · MIN_VISIBLE_MS 1300 · REVEAL_END 145 · REVEAL_FEATHER 14
Anillo r=46 · 14 cometas · ángulo π*0.28
Gradiente: linear-gradient(104.458deg, #ffe5ac 10.028%, #97bdde 100%)
Acentos de tinta: #ffd75a / #6ccfff
```

Ese bloque es de un sitio real de referencia. **Cada valor está decidido.** Cuando algo
se deja "a criterio", sale el promedio — y el promedio es exactamente el 10 de 100.

**Regla de ejecución:** antes de escribir una línea de código, escribe el bloque de
tokens de esa página: paleta en hex, duraciones en ms, curvas de easing, radios,
cantidades de partículas, grados de rotación. Ese bloque va en `:root` del CSS y como
constantes arriba del JS. Si un número no está decidido, la pieza no está diseñada.

## Los 7 mecanismos del "wow"

Verificados frame a frame en sitios que sí lo logran. Una página cinematográfica usa
**3 o 4 de estos**, nunca los 7 (eso es ruido).

1. **Preloader con contador 0→100 y cortina que barre.** Lo primero que se ve. Mínimo
   1.300 ms garantizados aunque cargue antes: es un ritual de entrada, no un spinner.
2. **Un solo objeto 3D protagonista**, centrado, sobre negro absoluto, con **una** luz
   cálida y bloom. Nada más compite por atención.
3. **Campo de partículas emisivas que ondula en loop infinito.** Movimiento permanente
   sin que el usuario toque nada — la página está viva antes de que hagas scroll.
4. **Elemento volumétrico que persigue el cursor con inercia y estela**, cambiando de
   tinte según la zona.
5. **Video o render pre-hecho como fondo del hero**, con las capas de UI y partículas
   encima. Calidad de cine sin costo de GPU: lo caro se pre-renderiza, no se calcula.
6. **Wireframe blanco de 1px** (esferas, órbitas, retículas) sobre el objeto 3D. Le da
   lectura de instrumento técnico en vez de adorno.
7. **Choque tipográfico:** display enorme (serif itálico o grotesca pesada) contra
   microcopy de 10px con tracking abierto, numeración de sección `(026)` y reloj en
   vivo con ciudad en el header.

## Cómo se entrega (la decisión que casi siempre se falla)

| Si el entregable es… | Motor | Cómo |
|---|---|---|
| **Un HTML publicado en Vercel** (lo normal en Golden) | **Three.js por importmap** | Un solo archivo, sin build, sin npm. Ver `references/recetas.md` |
| Un proyecto Next/React ya existente | **React Three Fiber + drei** | `@react-three/fiber`, `@react-three/drei`, `@react-three/postprocessing` |
| El cliente no toca código y quiere editar la escena | **Spline** | Escena en spline.design embebida con `<spline-viewer>` |
| **Página por escenas** (se lee haciendo scroll: propuesta, marca, presentación larga) | **Sin librerías** | CSS `sticky` + canvas 2D en un HTML. 12 piezas y 5 reglas en `references/piezas-pagina-por-escenas.md` |

**Error histórico que esta skill corrige:** recomendar React Three Fiber cuando el
entregable real es un archivo HTML. R3F necesita build de React — si vas a publicar un
HTML, R3F no aplica y la página termina cayendo a gradientes CSS. **Decide el motor
ANTES de diseñar.**

## Orden de trabajo (5 fases)

Destilado de un método público de 8 prompts, reordenado y con la disciplina de tokens
que a ese método le faltaba.

**1 · Plano.** Define en un solo documento: arquitectura de secciones, identidad visual
con hex exactos, cuál es el objeto 3D protagonista, el lenguaje de movimiento (duración
y easing por tipo de interacción) y el presupuesto de rendimiento. **Justifica cada
animación:** si no sirve a la historia, se borra.

**2 · Tokens.** Escribe el bloque `:root` completo y las constantes JS. Nada de "azul
oscuro": `#0B1E3D`. Nada de "rápido": `380ms cubic-bezier(.22,1,.36,1)`.

**3 · Escena.** Construye el objeto 3D protagonista con la receta que corresponda
(`references/recetas.md`). Primero que se vea bien quieto; después se anima.

**4 · Movimiento y conversión.** Preloader, scroll, cursor, reveals. Y la pregunta que
salva la página: **dónde el 3D construye confianza y dónde estorbaría la conversión.**
El formulario y el precio no se animan: se leen.

**5 · Publicar.** 60fps, peso, accesibilidad, `prefers-reduced-motion`, SEO. La lista
completa abajo.

## Vara de calidad — no se entrega si falla algo de esto

- **60fps sostenidos** en el hero, medidos en móvil de gama media, no en el Mac
- **El first paint no espera al 3D:** el bundle de la escena carga aparte (dynamic import)
- **Fallback real:** con `prefers-reduced-motion` o en gama baja se muestra un render
  estático de alta calidad de la MISMA escena. Nunca un hueco negro
- **Una sola escena WebGL protagonista por página.** `dpr` limitado a `[1, 2]`
- **La escena se pausa fuera del viewport** (`IntersectionObserver`) — no quema batería
- **Texto legible sobre la escena:** contraste AA real, no "se alcanza a leer"
- **El CTA se ve sin hacer scroll** y no compite con la animación
- Modelos comprimidos (draco/meshopt), texturas ≤ 2k, video de fondo ≤ 3 MB y `muted loop playsinline`
- **Cero letras montadas:** `scripts/barrido_encimes.js` corrido a 390 y a 1280, con la pantalla
  visible, y su lista de encimes vacía. Una captura no lo demuestra
- **`overflow-x:clip` en html y body, nunca `hidden`**: `hidden` rompe el `sticky` en Safari iOS
- **Verificado en un navegador VISIBLE**, con accesos de prueba en `window`: en un panel oculto no
  corren `requestAnimationFrame` ni `IntersectionObserver`, y las capturas mienten
- **Toda cifra en pantalla con su fuente consultada y fechada**, enlazada en la página
- **Todo video lleva póster**

## Referencias de esta skill
- `references/vocabulario.md` — **cómo pedir cada efecto por su nombre.** 25 términos en
  español con su equivalente técnico. Empieza SIEMPRE aquí cuando el encargo venga vago
- `references/recetas.md` — código real y probado: preloader con cortina, partículas que
  ondulan, cromado con reflejos, cursor con inercia, wireframe, scroll cinemático
- `references/piezas-pagina-por-escenas.md` — la página por escenas sin librerías: 12 piezas con sus
  números medidos y las 5 reglas. Es una caja de piezas, no una plantilla: cada página elige las suyas
- `scripts/barrido_encimes.js` — detecta textos montados, escena por escena (contrato en su cabecera)
- `scripts/puntos_globo.py` — genera los puntos de tierra del globo desde Natural Earth
  (requisito: Pillow; cómo instalarlo según el Python, en la tabla de requisitos; el TopoJSON se descarga, no viaja en la skill)
- `scripts/referencia/vidrio_templado.js` — entrada de vidrio que se quiebra. Es de REFERENCIA:
  su cabecera trae el contrato completo (11 nombres que la página provee) y la advertencia de que
  un nombre faltante no revienta, se salta la entrada en silencio: tras adaptarla, mirar la consola

## Encadena con
- `golden-web` → estructura y blueprints por perfil, con su propia
  `golden-web/references/estilo-agencia-premium.md` (tipografía display + springs + aire). Esta skill
  es su capa 3D
- `golden-web/references/estandar-movimiento.md` → **el estándar NUMÉRICO de cómo se mueve todo**:
  curva por tipo de movimiento, duración de UI bajo 300 ms, nunca `scale(0)`, origen en el disparador,
  interrumpibilidad y por qué solo se animan `transform` y `opacity`. Esta skill pone el EFECTO; ese
  archivo pone los NÚMEROS. Misma ley: tokens exactos, jamás adjetivos.
- `three` · `gsap` (ScrollTrigger) · `apple-design` (easing físico) · `emil-design-eng`
  (pulido invisible) · `improve-animations` (auditar una web ya hecha)
- `golden-imagen-arena` / Higgsfield → generar el render pre-hecho del fondo del hero
- `all-deploy` → publicar · `cyber-neo` → si la página lleva formularios o datos

## Cuando algo falla o falta (degradación, no bloqueo)

- **El CDN de unpkg no responde o el import falla:** no inventes una versión distinta a la
  fijada en `references/recetas.md`. Informa el corte, reintenta una vez, y si sigue caído
  entrega igual el HTML con el `<script type="importmap">` correcto — el sitio funcionará
  en cuanto el CDN vuelva. Nunca se degrada a gradientes CSS por un corte temporal.
- **No hay foto/render para el fondo del hero (mecanismo 5):** delega a
  `golden-imagen-arena` o Higgsfield para producirlo; si tampoco están disponibles, arranca
  con la escena WebGL sola (mecanismos 2-4) y dilo explícitamente como pendiente — no se
  inventa un video de stock genérico.
- **El 60fps no se sostiene en móvil de gama media (vara de calidad):** en este orden,
  antes de tocar el diseño: baja `COLS`/`ROWS` de la malla de partículas (receta 2), baja
  el `dpr` cap de `[1,2]` a `[1,1.5]`, apaga el bloom, y solo si sigue sin llegar, reduce a
  3 mecanismos en vez de 4. Nunca se sacrifica el fallback de `prefers-reduced-motion` para
  ganar fps: ese camino ya es la salida de emergencia.
- **El usuario no da los hex/tokens exactos:** no se inventan colores "bonitos" a ciegas —
  se piden UNA vez al inicio con la plantilla de `references/vocabulario.md`, y si el
  usuario no los tiene, se extraen del logo o la paleta de marca ya existente del proyecto
  (nunca un genérico #000/#fff sin decisión).

## Changelog

- **GC1.6** (2026-09-27) — Ley de los requisitos del usuario: tabla «Antes de empezar» con cada requisito BLOQUEANTE o DEGRADABLE (redactada por 🧰 ARSENAL Y SKILLS, fila P49; aplicada y numerada por el CdM, que es su fábrica). El `pip install pillow` suelto de la línea del globo remite ahora a la tabla (falla con el Python de Homebrew). Queda abierto P53: la vara de 60 fps no tiene método de medida; hasta fijarlo, la entrega dice «60 fps NO medidos».
- **GC1.5.1** (2026-09-24) — Dos fallas del golden-verificador sobre GC1.5. El barrido buscaba
  textos solo dentro de `<main>`: en una página sin `<main>` daba 0 textos y "sin encimes", un
  verde falso. Ahora barre el body y se niega si no encuentra textos. La referencia del vidrio
  declaraba 6 de los 11 nombres que usa ("seg is not defined") y traía vocabulario de la página de
  origen. Contrato completo medido con un barrido de identificadores libres, nombres genéricos y
  prueba en Chromium: con el contrato la entrada corre, y sin `seg` se salta en silencio.
- **GC1.5** (2026-09-24) — Página por escenas como estándar (decisión del CdM del 24-sep: el método
  de la página por escenas vive aquí, no en golden-presenta). Nuevos `references/piezas-pagina-por-escenas.md`
  (12 piezas y 5 reglas) y tres scripts. Al entrar se generalizaron dos que venían cableados a su
  página: `barrido_encimes.js` llamaba a cuatro funciones por nombre fijo y fallaba en cualquier otra
  página, y `puntos_globo.py` escribía en una carpeta `../sitio` que aquí no existe. El barrido se colgaba
  sin avisar con la pantalla oculta (innerHeight 0); ahora se niega. Probados los dos en los dos
  sentidos. Description: sale la frase del motor y entra el disparador de la página por escenas.
- **GC1.4.4** (2026-09-13) — Auditoría golden-skill-auditor: la description no declaraba
  frontera explícita ("NO usar para") pese a que el cuerpo sí la tiene en "Fronteras y
  desambiguacion" — dimensión Activación de la rúbrica lo exige en el frontmatter, que es
  el único mecanismo de disparo. Se añadió "No sirve para producto Shopify COD ni sitio
  corporativo simple." al final de la description (952→1016 caracteres, dentro del tope
  duro de 1024). Verificado con `validar_arsenal.py`: exit 0.
- **GC1.4.1** (2026-08-24): bump de las ediciones del 24 (verificador de cierre R2: la version vive en 4 caras — sello, linea Version, Changelog y REGISTRO — y el bump anterior toco solo el sello).
- **GC1.4** (2026-08-23) — Adenda del Centro de Mando: entra a la familia que lee el CEREBRO DE
  MARCA (`golden-brand-brain`) — bloque "Paso 0 · Cerebro de marca" bajo el H1, idéntico en las
  6 skills de contenido del CdM. Además, Estándar 9: cambios relevantes se reportan a 🧠 GOLDEN -
  CENTRO DE MANDO - NO BORRAR. (Entrada añadida en el barrido del arsenal 2026-08-24: ambos
  cambios existían solo como sellos en comentario; en el mismo barrido se renumeró el índice de
  `references/recetas.md`, que no calzaba con los encabezados reales de las recetas.)
- **GC1.3** (2026-08-21) — Auditoría golden-skill-auditor: desambigua la cita a
  `estilo-agencia-premium.md` (vive en golden-web), suma la sección de degradación
  ("Cuando algo falla o falta") y el índice de `references/recetas.md`.
- **GC1.2** (2026-08-02) — Vocabulario de ESTADOS (confirmación en contra entrega) y
  NAVEGACIÓN (morphing dock), del filtro de 2 reels de efectos.
- **GC1.1** (2026-07-27) — 5 términos nuevos de entrada y revelado, del filtro de 9 reels.
- **GC1.0** (2026-07-25) — Creación. Diagnóstico de FER ("10 de 100") + análisis frame a
  frame de 6 sitios de referencia. Aporta lo que faltaba: la disciplina de tokens
  numéricos, la ruta HTML por importmap (el entregable real de Golden), las recetas con
  código y el vocabulario para encargar.

## Fronteras y desambiguacion

NO usar para: página de producto Shopify COD (golden-shopify), sitio funcional sencillo o corporativo estándar (golden-web), ni imágenes sueltas de producto (golden-imagen-arena).

Con `golden-presenta`: las presentaciones tipo diapositivas (láminas, modo presentador, cámara que
viaja por un lienzo) son de ella. **Las páginas que se leen haciendo scroll por escenas vienen aquí**,
aunque el encargo diga "propuesta para un cliente".

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-cinematica
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-cinematica
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-cinematica`

Historial completo en `references/changelog.md`.
