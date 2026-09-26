# Los cinco formatos y su geometría

La plantilla de `assets/` resuelve la caja plegadiza. Los otros cuatro se construyen sobre la
misma mesa: mismo visor fijo, mismos ocho grupos de controles, mismo bloque de opinión. Lo
único que cambia es cómo se dibuja la pieza.

## 1. Caja plegadiza · CSS 3D

Es la plantilla. Seis caras planas, desarme por normales, plano de troquel en cruz.
Ver `motor.md`.

Controles propios: ancho, fondo, alto, posición y grosor de franja.

## 2. Etiqueta sobre frasco cilíndrico · CSS 3D con curvatura fingida

No hace falta Three.js. Un cilindro se finge con **rebanadas verticales**: entre 24 y 36
tiras, cada una rotada un poco más sobre su eje Y y empujada hacia afuera por el radio.

```js
var N = 32, R = 90;               // rebanadas y radio en px
for (var i = 0; i < N; i++) {
  var a = (360 / N) * i;
  slice.style.transform = 'rotateY(' + a + 'deg) translateZ(' + R + 'px)';
  slice.style.width = (2 * Math.PI * R / N + 1) + 'px';   // +1 tapa la costura
}
```

La etiqueta se dibuja como una imagen de fondo desplazada por rebanada
(`background-position-x`), así el arte se ve curvado. El `+1 px` de ancho es obligatorio: sin
él aparecen líneas del fondo entre tira y tira.

Controles propios: alto y diámetro del frasco, alto de la etiqueta, posición vertical, color
de la tapa y del líquido.

## 3. Frasco con hombros y válvula · Three.js

Aquí sí. Un frasco real tiene curvatura variable y no se finge con rebanadas planas.

- `LatheGeometry` con el perfil del frasco dibujado como puntos
- La etiqueta va como textura sobre un `CylinderGeometry` un pelo más grande
- Luz: una `DirectionalLight` más una `HemisphereLight`, sin luces de colores
- Material: `MeshPhysicalMaterial` con `transmission` para el plástico translúcido

**El texto de la etiqueta se genera en un canvas** y se aplica como textura. Eso significa que
cada cambio de tipografía obliga a redibujar el canvas y marcar `texture.needsUpdate = true`.
Es más lento que CSS 3D y por eso solo se usa cuando la curvatura lo exige.

Three.js se carga de cdnjs, build clásico con global `THREE`, versión fijada:
`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`

`OrbitControls` **no** viene en el núcleo. No se intenta cargar el complemento: se escriben
veinte líneas de arrastre propio, igual que en la plantilla de caja.

## 4. Bolsa doypack · CSS 3D con deformación

Una doypack es un trapecio con fuelle. Se arma con cuatro caras:

- Frente y revés como trapecios, usando `clip-path: polygon(...)`
- Dos laterales estrechos que hacen el fuelle
- Un fondo que se ve solo cuando la bolsa está de pie

```css
.doypack-front {
  clip-path: polygon(6% 0, 94% 0, 100% 88%, 88% 100%, 12% 100%, 0 88%);
}
```

El brillo del laminado se finge con un degradado diagonal encima, de baja opacidad, que **no**
se mueve al girar: si se moviera parecería un reflejo real y no lo es.

Controles propios: alto, ancho, profundidad del fuelle, redondeo de las esquinas y zipper.

## 5. Display de mostrador · CSS 3D

Una bandeja con fondo vertical y dos costados. Cinco caras planas, sin tapa. Se construye
igual que la caja quitando la cara superior y rotando el fondo.

Lo específico del display: **debe poder mostrar el producto adentro**. Se meten de tres a seis
copias reducidas de la caja dentro de la bandeja, con `translate3d` para acomodarlas en
filas. Eso es lo que el cliente quiere ver: no el display vacío, sino lleno.

## Cómo se escoge

| La pieza tiene | Motor |
|---|---|
| Solo caras planas | CSS 3D |
| Un cilindro recto | CSS 3D con rebanadas |
| Curvatura variable, hombros, cuello | Three.js |
| Contornos irregulares planos | CSS 3D con `clip-path` |

**Ante la duda, CSS 3D.** Es más rápido de construir, el texto queda real y no hay librería
que falle. Three.js se justifica cuando sin él la pieza se ve falsa.
