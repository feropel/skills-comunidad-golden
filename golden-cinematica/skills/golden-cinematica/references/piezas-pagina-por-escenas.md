# Página por escenas: 12 piezas y 5 reglas

Técnica distinta de la receta 7 de `recetas.md` (cámara 3D que avanza con el scroll, con Three.js).
Aquí **no hay librerías ni CDN**: escenas fijas con CSS `sticky`, canvas 2D y un solo HTML. Sirve para
propuestas comerciales, páginas de marca y presentaciones largas que se leen haciendo scroll.

**Esto es una caja de piezas, no una plantilla.** Cada página elige las que su historia necesita y
conserva su propia paleta, tipografía y ritmo. Copiar el conjunto entero en cada encargo produce
páginas iguales, que es justo lo contrario de lo que se busca.

Salieron de una propuesta comercial real, medida en computador y en iPhone, el 23 y 24-sep-2026. Los
números de cada pieza se encontraron probando: no se cambian sin volver a medir.

## 1 · Motor de escenas fijas por scroll
- Cada `<section data-scene="x">` mide de 260 a 460 vh de alto y contiene un `.pin` `sticky` de 100 svh.
- `prog(s)` devuelve el avance de la escena de 0 a 1. `frame()` solo llama a la función de una escena
  si está en pantalla (±50 px), así las demás no gastan.
- Helpers: `seg(p,a,b)` para cada fase, `lerp`, `ease`, `easeOut`.
- La ventana de visibilidad de cada texto es `min(seg(p,a,b), 1-seg(p,c,d))`, y al aparecer sube de 24 a 28 px.

## 2 · Entrada: un video real se congela y se quiebra como vidrio templado
Implementación de referencia en `scripts/referencia/vidrio_templado.js`. Su cabecera trae el contrato
COMPLETO: 11 nombres que la página tiene que proveer (medido con un barrido de identificadores libres),
entre ellos `dibujarObjeto()`, que es de cada página.
- Secuencia: el clip corre, se pausa en el cuadro del impacto, un objeto sale hacia la cámara, el cuadro
  se congela en un canvas, la telaraña de grietas se propaga, los fragmentos giran en 3D y caen con el
  cuadro recortado adentro, y sale el polvo de vidrio. Detrás aparece el título.
- **Geometría:** 22 rayos irregulares × 12 anillos,
  `RAD=[0,.018,.045,.085,.14,.21,.3,.41,.55,.72,.93,1.2]`. Las aristas son dentadas y **cada una la
  comparten los dos fragmentos que separa**, así no quedan huecos. Anillos visibles parciales: 97 % en
  los internos, 60 % en los medios, 28 % en los externos.
- **Refracción:** cada fragmento se dibuja desplazado ±2,4 px con un tinte de ±0,09. La grieta es una
  línea de sombra con 0,8 px de desfase más un filo de luz de 0,7 a 1,3 px.
- **Tiempos:** acercamiento 450 ms (620 sin video) · grieta 170 ms · rompe a los +420 ms · los fragmentos
  vuelan 950 ms con un retraso por distancia de 230 ms.
- **Seguros, obligatorios:** `setTimeout(terminar, 9000)` libera la pantalla pase lo que pase;
  `try/catch` en cada cuadro; si el video no arranca, se usa el póster.
- 🔴 **Trampa:** el clip debe empezar DESPUÉS de cualquier cambio de plano. Un recorte que cae a un
  cuadro del corte deja una imagen equivocada en el primer cuadro. Se revisa la hoja de contactos del
  clip completo, no cuatro fotogramas.
- 🔴 **Trampa:** el navegador pausa los videos mudos que no se ven, para ahorrar energía. Sin póster de
  respaldo, la entrada queda en negro.

## 3 · Objeto real (foto) reutilizable en todo el sitio
- La foto del producto se recorta con máscara circular y se pinta **una sola vez** en un canvas de
  256 px con la luz de la escena: gradiente de sombra `source-atop` más un borde de acento.
- Una función la rota en cada cuadro. Si la foto no ha cargado, se dibuja una versión vectorial.

## 4 · Objeto que cruza entre secciones
- En cada frontera entre secciones con `data-cruce`, el objeto cruza la pantalla en arco, alternando de
  izquierda a derecha, y un elemento en el borde hace el gesto de lanzarlo (animación CSS por lado).
- La zona activa mide 0,9 vh centrada en la frontera; el arco sube 0,3 del alto de pantalla.

## 5 · Globo de puntos (continentes)
Generador en `scripts/puntos_globo.py`, que usa `land-110m.json` de world-atlas (Natural Earth):
`python3 scripts/puntos_globo.py <land-110m.json> <sitio/globo-puntos.json>`. Probado el 24-sep con el
archivo de `cdn.jsdelivr.net/npm/world-atlas@2`: 9.005 puntos, 78.694 bytes y los tres controles bien
(Bogotá y Madrid caen en tierra, el Atlántico no). Si un control sale al revés, sale con código 1.
- Proyección ortográfica de unos 9.000 puntos de tierra, con atmósfera, brillo en el borde, ruta en arco
  (slerp elevado 22 %), un cometa, marcas que laten y rutas locales.
- 🔴 **El número que costó:** al pasar el TopoJSON a raster hay que **desenvolver las longitudes** de
  cada anillo (`p + (lon - p + 180) % 360 - 180`), dibujar cada polígono con desplazamientos de −360, 0 y
  +360, y **cerrar por el polo** el anillo de la Antártida. Si no, aparecen bandas horizontales falsas
  en el meridiano 180. Controles: dos ciudades deben caer en tierra y un punto del océano en agua.
- Densidad pareja: paso de 1,15°, con `n = 360·cos(lat)/paso` puntos por fila.

## 6 · Carrusel horizontal fijo
- Alto de la sección: `track.scrollWidth - vw + 1,2 vh`.
- Cada tarjeta gira en Y según su distancia al centro (±38°). El nombre de fondo solo se ve en la tarjeta
  central (`opacity = 1 - |d|·2,6`), para que los nombres vecinos no se monten.

## 7 · Contador que acelera de uno en uno
- Sube de 1 en 1 con un intervalo de `12 + 95·(1 - n/N)^2,2` ms (unos 2,6 s para N = 63), con un golpe de
  escala en cada número. Arranca con IntersectionObserver y deja un acceso de prueba en `window`.

## 8 · Mano de demostración que toca sola
- Un cursor SVG va a tres opciones y les hace `click()`, con una onda en cada toque. Umbral 0,25.
- 🔴 **La detiene un `click` con `isTrusted`, NO un `pointerdown`.** En el celular, poner el dedo para
  hacer scroll dispara `pointerdown` y la apagaba sin que nadie quisiera.
- Deja un acceso de prueba en `window`.

## 9 · Visor de cámara grabando sobre un video desenfocado
- Esquinas, REC titilando, código de tiempo en vivo a 60 fps (solo corre en pantalla), formato, un
  cuadro de enfoque que salta y un destello de obturador.
- Enfoque y obturador duran 5,5 s; el destello cae en el 44 % y el 79 %.
- En el celular se oculta el cuadro de enfoque porque tapa el título.

## 10 · Estrellas de fondo
- 240 puntos con profundidad `z`, titilando con `|sin|`, parallax de 0,04 respecto al scroll; un 8 %
  con el color de acento. El cielo va en z-index 0; `main` y `footer` en 1.

## 11 · Botón de WhatsApp que late
- Latido doble: 1 → 1,16 → 1,02 → 1,12 en el tramo 0 a 40 % de un ciclo de 1,6 s, más dos ondas
  desfasadas 0,4 s. Respeta `safe-area-inset` en el iPhone.

## 12 · Precio que baja del de lista al de oferta
- El precio de lista va grande y tachado con una línea de 0,09 em; el número cuenta hacia abajo:
  `v = desde + (meta - desde)·easeOut(t)`.
- 🔴 El precio que se muestra lo fija el dueño del negocio. Un precio sugerido por el estudio es
  referencia, no decisión, y no se publica como si fuera el definitivo.

## Las 5 reglas (son parte de la vara de calidad)

1. **Barrido de letras montadas:** `scripts/barrido_encimes.js` (su cabecera trae el contrato: escenas
   por `data-scene`, `prog()` global, funciones en `window.ESCENAS` o por nombre, y
   `data-barrido-ignorar` para adornos). Probado el 24-sep en los dos sentidos sobre una página de
   prueba: encontró el único par montado, no acusó el sano y declaró la escena sin función. Con la
   pantalla oculta (0x0) se niega en voz alta; antes se colgaba sin avisar. Baja de media en media pantalla, fuerza
   las escenas llamando a sus funciones y cruza las cajas de todos los textos visibles, sin contar la
   barra superior de 64 px. Se corre a 390 y a 1280. En la página de origen encontró 4 clases de fallo
   que ninguna captura mostraba.
2. **El panel de pruebas de la sesión está oculto:** ahí no corren IntersectionObserver ni
   requestAnimationFrame, y `setTimeout` no va a tiempo normal. Las capturas mienten. Hay que dejar
   accesos de prueba en `window` y verificar en un navegador VISIBLE.
3. **Toda cifra en pantalla sale de una fuente consultada y fechada**, con su enlace visible. Si la API
   recorta (la Biblioteca de Meta devuelve el detalle de 50 de N), se declara en la página.
4. **Publicar:** con la receta de Vercel del CLAUDE.md (`NODE_USE_ENV_PROXY=1` dentro del sandbox),
   siempre desde la carpeta del sitio, y comparando el SHA local contra el servido.
5. **Celular primero:**
   - `overflow-x:clip` en html y body, **nunca `hidden`**: `hidden` rompe el `sticky` en Safari iOS y las
     escenas se quedan congeladas;
   - rehacer el layout solo si el ancho o el alto cambian más de 140 px, porque la barra de direcciones
     del iPhone dispara `resize` al hacer scroll;
   - todo video de fondo lleva póster;
   - los títulos gigantes llevan `padding-bottom: .17em`: con interlineado 0,88 la caja de la última
     línea invade el párrafo siguiente;
   - la barra superior fija necesita una franja oscura con desenfoque, o el contenido se ve pasar entre
     sus letras.
