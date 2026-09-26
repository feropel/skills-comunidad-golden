# El motor: CSS 3D contra Three.js

## La decisión, y por qué

Para una pieza de **caras planas** (caja plegadiza, display, estuche), CSS 3D gana. No es
preferencia: es medible.

| | CSS 3D | Three.js |
|---|---|---|
| El texto | DOM real: nítido a cualquier zoom, seleccionable | textura de canvas: se pixela, hay que regenerar |
| Cambiar una fuente | una variable CSS, instantáneo | regenerar la textura y volver a subirla a la GPU |
| Cambiar un texto | `textContent`, instantáneo | redibujar el canvas completo |
| Plano de troquel | cambiar seis transformaciones | hay que construir otra escena |
| Dependencias | ninguna | una librería de CDN que puede fallar |
| Peso | cero | ~600 KB |

**Three.js entra solo cuando hay curvatura real**: frasco cilíndrico, tubo, bolsa doypack,
botella con hombros. Ahí CSS 3D no alcanza y hay que ir a geometría de verdad. Ver
`formatos.md`.

## Cómo se arma el sólido en CSS 3D

Tres capas, y el orden importa:

```
.stage  { perspective: 1500px; perspective-origin: 50% 44%; }
.box    { transform-style: preserve-3d; }
.face   { position: absolute; left:50%; top:50%; backface-visibility: hidden; }
```

Cada cara se centra con márgenes negativos de la mitad de su tamaño, y desde ahí se empuja a
su sitio. Con ancho `W`, fondo `D` y alto `H`:

| Cara | Tamaño | Transformación |
|---|---|---|
| Frente | W × H | `translateZ(D/2)` |
| Revés | W × H | `rotateY(180deg) translateZ(D/2)` |
| Derecha | D × H | `rotateY(90deg) translateZ(W/2)` |
| Izquierda | D × H | `rotateY(-90deg) translateZ(W/2)` |
| Tapa | W × D | `rotateX(90deg) translateZ(H/2)` |
| Fondo | W × D | `rotateX(-90deg) translateZ(H/2)` |

**Desarmar** es sumarle un hueco al `translateZ` de cada cara: `translateZ(D/2 + GAP)`, con
`GAP = 46`. Las seis se separan por su propia normal y la pieza se abre como una explosión
ordenada. **Ese hueco tiene que entrar en el cálculo de la escala** (ver más abajo), o las
caras se salen del visor.

## 🔴 El plano de troquel es una TIRA, no una cruz

La cruz de seis caras es didáctica y **no es el plano que va al impresor**. Una caja
plegadiza se troquela en una sola tira:

```
[pegue] [FRENTE] [lateral] [REVÉS] [lateral]
```

con solapas arriba y, abajo, el **fondo automático**: cuatro solapas cortadas en diagonal
que se traban solas al levantar la caja. Eso es lo que hace que llegue plana y se arme de
un gesto, lista para meter el producto.

Con pestaña `TAB` de 18 px y el conjunto centrado, `total = TAB + 2W + 2D` y `x0 = -total/2`:

| Pieza | Centro en X | Tamaño |
|---|---|---|
| Pestaña de pegue | `x0 + TAB/2` | TAB × H |
| Frente | `x0 + TAB + W/2` | W × H |
| Lateral | `x0 + TAB + W + D/2` | D × H |
| Revés | `x0 + TAB + W + D + W/2` | W × H |
| Lateral | `x0 + TAB + W + D + W + D/2` | D × H |

Las solapas van a `∓(H/2 + h/2)` sobre su panel, con `hT = D·0,92` arriba y `hB = D·0,68`
abajo. **Las caras `top` y `bottom` del 3D se ocultan en esta vista**: en un troquel real
la tapa y el fondo son solapas de los paneles, no caras sueltas.

Las formas se recortan con `clip-path`, y cada una dice qué pieza es:

```css
.die-dust  {clip-path:polygon(7% 0, 93% 0, 100% 100%, 0 100%)}          /* solapa de polvo */
.die-tuck  {clip-path:polygon(0 14%, 5% 0, 95% 0, 100% 14%, 100% 100%, 0 100%)}  /* tapa con lengüeta */
.die-lock-a{clip-path:polygon(0 0, 100% 0, 100% 58%, 55% 100%, 0 100%)} /* fondo automático */
.die-lock-b{clip-path:polygon(0 0, 100% 0, 100% 100%, 45% 100%, 0 58%)}
.die-lock-s{clip-path:polygon(0 0, 100% 0, 74% 100%, 0 100%)}
```

La pestaña de pegue va rayada a 45° con `repeating-linear-gradient`, y los pliegues son
bordes `dashed`. Sin esas dos señales, el troquel parece un despiece y no un plano.

**La tira es ancha y baja**, así que la escala tiene que encajar contra el ancho del visor
además del alto, o se sale de lado:

```js
if(view === 'plano'){
  var ancho = TAB + 2*W + 2*D + 30;
  fit = Math.min(fit, (shell.clientWidth - 30) / (ancho * base));
}
```

## Que se vea sólido, no plano

Sin sombreado, seis rectángulos del mismo color se leen como papel, no como caja. Cada cara
lleva un `::after` a pantalla completa que la oscurece o aclara según hacia dónde mira:

```css
.f-left::after   { background: linear-gradient(90deg, rgba(0,0,0,.17), rgba(0,0,0,.03)); }
.f-right::after  { background: linear-gradient(90deg, rgba(0,0,0,.03), rgba(0,0,0,.17)); }
.f-back::after   { background: rgba(0,0,0,.10); }
.f-top::after    { background: linear-gradient(180deg, rgba(255,255,255,.3), rgba(255,255,255,0)); }
.f-bottom::after { background: rgba(0,0,0,.22); }
```

Más una sombra en el piso: una elipse borrosa bajo la pieza, con `radial-gradient` y `blur`.
Se atenúa al desarmar, porque una pieza abierta ya no se apoya en nada.

## La escala: se calcula, no se fija

Si la escala es un número fijo, al subir el alto a 20 cm la pieza se sale del visor. La escala
sale de comparar lo que la pieza necesita contra lo que el visor tiene:

```js
var GAP = 46;                       // el hueco entre caras al desarmar
function fitScale(){
  var base = view==='plano' ? 0.52 : (view==='explotada' ? 0.82 : 1);
  var room = shell.clientHeight || 400;
  // la altura que de verdad ocupa cada vista, no una estimacion
  var need = view==='plano'     ? (H + 2*D + 24)
           : view==='explotada' ? (H + 2*GAP + D)
           :                      (H * 1.35);
  var fit  = Math.min(1, (room - 34) / (need * base));
  return base * fit * zoom;
}
```

🔴 **La rama de `explotada` no es opcional.** La primera versión usaba `H * 1.35` para todo lo
que no fuera plano: para H=286 eso da 386, cuando la altura real desplegada es
`H + 2*GAP + D` = 504. Dos caras quedaban fuera de cuadro. Es un defecto que **no se ve
leyendo el código**, solo abriendo la pieza y mirándola.

Y se vuelve a aplicar en `resize`, o al girar el teléfono la pieza queda cortada.

## Girar, acercar, centrar

- **Girar**: `pointerdown/move/up` con `setPointerCapture`. El eje X se limita a ±85° para que
  la pieza no se voltee sobre sí misma.
- **Acercar**: `wheel` con `preventDefault` y `{passive:false}`, más un deslizador que refleja
  el mismo valor.
- **Giro automático**: `requestAnimationFrame`, y **se apaga solo en cuanto el usuario arrastra**.
  Pelear con una pieza que gira sola mientras se intenta mirar un detalle es irritante.
- **Centrar**: devuelve rotación y acercamiento al punto de partida.

Durante el arrastre se quita la clase de transición (`.animated`), o cada movimiento del mouse
arranca una animación de 0,7 s y el giro se siente pegajoso. Se vuelve a poner al soltar.

## Texto vertical

**Nunca** `transform: rotate(90deg)`. El bloque rotado conserva su caja original para el
posicionamiento, se sale de la cara y toca parchar con posiciones mágicas que se rompen al
cambiar el tamaño de letra.

```css
.logoblock.vertical { writing-mode: vertical-rl; text-orientation: mixed; }
```

Con `vertical-rl` las líneas se apilan de derecha a izquierda: la **primera** del DOM queda a
la derecha. Para que el logotipo quede a la izquierda y la variante a su derecha, en el HTML va
primero la variante y después el logotipo.
