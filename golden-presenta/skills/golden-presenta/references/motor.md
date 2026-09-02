# El motor — coordenadas, atajos y la bitácora de lo que se rompió

## Índice
1. Cómo funciona la cámara
2. Colocar láminas en el lienzo
3. Atajos de teclado y navegación
4. Añadir un tipo de lámina nuevo
5. Los dos modos
6. Bitácora: los 6 fallos del motor
7. Bitácora del fondo vivo: 3 fallos más

## 1 · Cómo funciona la cámara

No se mueven las láminas: se mueve el lienzo. Esa es toda la idea, y es la misma de Prezi.

`#stage` está anclado en el centro del viewport con `transform-origin: 0 0`. Para encuadrar
la lámina que está en `(x, y)` con rotación `r`, el motor aplica la transformación inversa:

```js
stage.style.transform =
  'scale(' + k + ') rotate(' + (-r) + 'deg) translate(' + (-x) + 'px,' + (-y) + 'px)';
```

El orden importa. En CSS las transformaciones se aplican de derecha a izquierda: primero el
`translate` lleva el punto `(x, y)` al origen, después el `rotate` compensa el giro de la
lámina, y al final el `scale` ajusta el zoom.

El factor `k` se calcula para que la lámina quepa siempre con aire:
```js
var fit = Math.min(window.innerWidth / sw, window.innerHeight / sh) * 0.88;
var k   = fit / z;    // z es data-scale
```
El `0.88` es el margen de respeto. Subirlo a 1 hace que la lámina toque los bordes y el
deck se sienta apretado.

Las láminas se colocan con `disponerLienzo()`, que aplica `left`, `top` y
`translate(-50%,-50%)` a cada una para que su CENTRO caiga en su coordenada.

## 2 · Colocar láminas en el lienzo

Cada lámina lleva:

| Atributo | Qué hace | Por defecto |
|---|---|---|
| `data-x` | Coordenada horizontal del centro, en px de lienzo | obligatorio |
| `data-y` | Coordenada vertical del centro | obligatorio |
| `data-scale` | Zoom de cámara. 1 normal, 0.6 la cámara se acerca, 1.8 se aleja | 1 |
| `data-rot` | Giro en grados | 0 |
| `data-notas` | Notas del presentador | obligatorio en la práctica |

### Disposición por defecto: serpentina

Filas de 4, separación 1560 en x y 900 en y, con la fila par en sentido inverso:

```
(0,0)      (1560,0)    (3120,0)    (4680,0)
(0,900)    (1560,900)  (3120,900)  (4680,900)
   8           7           6           5
```

El recorrido 1 a 8 queda continuo: derecha, derecha, derecha, abajo, izquierda, izquierda,
izquierda. Sin saltos absurdos y con un movimiento vertical en el medio que rompe la
monotonía.

**Por qué serpentina y no una fila recta.** Medido **a 1280x800**: 8 láminas en fila ocupan
12.200 px de lienzo y la vista general las encuadra en `scale 0.0902`, una tira ilegible. La
serpentina 4x2 ocupa 5.960 x 1.620 y queda en `scale 0.1847`, que sí funciona como mapa.

El viewport importa y por eso se declara: a 1920x1080 los mismos lienzos dan `0.135` y
`0.277`. Lo que no cambia con el tamaño de la pantalla es la proporción entre ambos, que es
el argumento: **la serpentina duplica la escala del mapa.**

### Rotación: con cuentagotas
Dos o tres láminas giradas 2 o 3 grados en todo el deck. Es el condimento que hace que se
note que no son diapositivas. Más de eso marea y se ve amateur.

### Zoom dramático
Para un golpe de efecto, una lámina con `data-scale="0.55"` hace que la cámara se meta
dentro. Funciona bien en una cifra sola o en una frase corta. Una vez por deck.

## 3 · Atajos de teclado y navegación

| Tecla | Qué hace |
|---|---|
| Flecha derecha, espacio, N, AvPág | Siguiente |
| Flecha izquierda, P, RePág | Anterior |
| Inicio / Fin | Primera / última |
| O | Vista general del lienzo completo |
| S | Modo presentador (notas + cronómetro) |
| Esc | Salir de vista general o del presentador |

También responde a: rueda del ratón con freno de 620 ms, deslizamiento táctil de más de
48 px, clic en una lámina durante la vista general, y los tres botones del HUD.

**Deep-link:** la URL lleva `#3` y abrir esa URL arranca en la lámina 3. Sirve para mandar a
alguien directo a la lámina del precio.

## 4 · Añadir un tipo de lámina nuevo

1. Se añade la clase CSS en la sección 5 del `<style>`, junto a los otros `t-*`.
2. Se marca cada bloque que deba aparecer escalonado con `data-reveal`.
3. Los retardos van por `nth-child` y llegan hasta 6 hijos. Si el tipo nuevo tiene más de
   6 elementos revelados, hay que ampliar esa lista, o el séptimo aparece sin retardo.
4. Se documenta en `arquitectura-narrativa.md` con su criterio de uso. Un tipo sin criterio
   documentado se usa mal.

## 5 · Los dos modos

| Modo | Cuándo | Comportamiento |
|---|---|---|
| **Lienzo** | ancho >= 900 px | Cámara que viaja, láminas en posición absoluta, vista general, presentador |
| **Flujo** | ancho < 900 px | Cámara apagada, láminas apiladas, scroll nativo, HUD compacto |

El modo flujo no es una degradación: es la decisión correcta. Una lámina de 1280 px
escalada a 375 deja el título a 9 px. Prezi en móvil también sufre esto; la diferencia es
que aquí se resolvió a propósito en vez de dejarlo pasar.

El motor cambia de modo solo, con `ResizeObserver`, `resize` y `orientationchange`.

## 6 · Bitácora: los 6 fallos medidos y por qué importan

Todos salieron de **abrir el deck en un navegador**. Ninguno lo detectó el verificador
estático, y ninguno se habría encontrado razonando sobre el código. Esta lista es el
argumento de por qué la fase de ejecución no se salta.

### 1 · Las láminas nunca se colocaban en el lienzo
El JS leía `data-x` y `data-y` para mover la cámara, pero nadie aplicaba esa posición al
DOM. Todas las láminas quedaban apiladas en el origen y la portada salía descentrada hacia
abajo a la derecha. **Arreglo:** `disponerLienzo()`.
**Clase del fallo:** encuadrar una posición que nadie aplicó.

### 2 · El preloader se congelaba en segundo plano
El contador sumaba `n += paso` en un `setInterval` de 40 ms. El navegador ralentiza los
temporizadores de una pestaña que no está al frente: medido, 19 segundos de vida de página
y el contador seguía en 84, con el deck sin arrancar. En una sala real es el caso normal:
se abre el deck, se prepara el proyector, se vuelve, y sigue "cargando".
**Arreglo:** el progreso se calcula leyendo el reloj (`performance.now()`), con
`requestAnimationFrame`, más un `setTimeout` de garantía y un `visibilitychange`.
**Clase del fallo:** contar ticks en vez de leer el reloj.

### 3 · El cronómetro del presentador tenía el mismo defecto
`cronoSeg++` cada segundo miente en cuanto la pestaña pierde el foco, y el tiempo de
exposición es justo el dato que no puede mentir. **Arreglo:** diferencia contra `Date.now()`.
**Clase del fallo:** la misma que el 2. Cuando aparece un fallo, se busca la clase.

### 4 · El arranque pisaba la navegación del usuario
Si alguien pulsaba una tecla mientras el preloader seguía visible, al cerrarse el preloader
su `arrancar()` devolvía el deck a la lámina 1 y borraba la acción.
**Arreglo:** bandera `usuarioInteractuo`; el arranque respeta lo que el usuario ya hizo.
**Clase del fallo:** la inicialización asíncrona sobreescribe la intención del usuario.

### 5 · El modo no se recuperaba al cambiar el tamaño de la ventana
El deck decidía lienzo o flujo una sola vez al arrancar. Si el viewport nacía estrecho y
luego se ensanchaba, quedaba en modo flujo con la cámara sin transform y ninguna tecla de
lienzo respondía. **Esto es el caso central de una herramienta de presentaciones: conectar
el proyector cambia el tamaño de la ventana.** Girar el teléfono, también.
**Arreglo:** `ResizeObserver` sobre `documentElement`, más `resize` y `orientationchange`.
**Clase del fallo:** decidir una vez algo que cambia durante la vida de la página.

### 6 · El HUD se apelmazaba a 375 px
Con la marca y el título de lámina puestos, el HUD se partía en tres líneas y hasta el
contador "01 / 08" salía roto en tres renglones, tapando el texto de la lámina.
**Arreglo:** en móvil el HUD solo lleva contador y botones.
**Clase del fallo:** microtipografía con tracking abierto en un ancho que no se probó.

### Y uno del propio verificador
El auditor contaba 9 láminas donde había 8: estaba leyendo una `<section class="slide">`
que vivía dentro de un **comentario HTML** de la plantilla, y esa lámina fantasma se tragaba
todo el CSS (12.320 caracteres de "texto"). **Arreglo:** todas las comprobaciones de
contenido corren sobre una vista sin comentarios.
**Clase del fallo:** el auditor lee lo que el navegador ignora.

## 7 · Bitácora del fondo vivo (GP2.0, 2026-09-02)

Tres fallos más, los tres hallados en Chrome real con Playwright y ninguno visible para el
script.

### 7 · El título salía como "MBA Comunidad Golden_TARJETAS"
Al generar decks por sustitución de marcadores, `GP_TITULO` se reemplazaba antes que
`GP_TITULO_TARJETAS`. Como el primero es **prefijo** del segundo, se comía la cabeza y
dejaba `_TARJETAS` colgando en mitad de un titular.
**Arreglo:** sustituir siempre de la clave MÁS LARGA a la más corta. Y un check nuevo que
caza fragmentos en mayúsculas con guion bajo, porque el check de placeholders no veía nada:
ya no quedaba ningún `GP_` que buscar.
**Clase del fallo:** un marcador que es prefijo de otro se sustituye a medias, y el
detector mira justo lo que ha desaparecido.

### 8 · Las láminas salían borrosas en móvil
El desenfoque de profundidad de campo (`filter: blur(3px)` en las láminas no activas) es
del modo lienzo. En modo flujo todas se leen con scroll, así que ninguna puede estar
desenfocada. Se arregló dos veces: primero el `filter` del `.slide`, y al recargar seguía
borroso porque el culpable real era el `filter: blur(7px)` del **revelado escalonado**
(`[data-reveal]`), que solo se anulaba para opacidad y transformación.
**Clase del fallo:** un estado visual del modo lienzo se filtra al modo flujo. Cada vez que
se añade una propiedad al revelado hay que anularla en los DOS bloques: móvil y movimiento
reducido.

### 9 · El auditor acusaba a sus propias constantes
El check nuevo de "restos de sustitución" marcaba `_CANVAS` y `_VISIBLE`, que salían de
`MODO_CANVAS_PX` y `MIN_VISIBLE_MS` dentro del JS del motor.
**Arreglo:** los checks de redacción corren sobre el contenido sin `<style>` ni `<script>`.
**Clase del fallo:** el auditor lee código como si fuera prosa. Hermano del fallo del
comentario HTML de GP1.0.

Moraleja que vale para cualquier skill: **si tu script dice que todo está bien a la primera,
sospecha del script.** Este dijo 26 de 26 mientras el deck tenía cinco defectos de render, y
más tarde 29 de 29 con un titular roto en pantalla.
