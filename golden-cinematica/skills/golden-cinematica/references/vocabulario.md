# Vocabulario Golden Cinemática — cómo pedir cada efecto

Nació de una pregunta literal de FER: *"dime cómo me expreso para que me hagas páginas así"*.

**Cómo se usa:** FER dice la frase de la columna izquierda. Claude ejecuta el término
técnico de la derecha. Si el encargo llega vago ("algo futurista"), se abre esta tabla y
se le devuelven 3 opciones concretas para que elija.

## Entrada y revelado

| Lo que quieres decir | Término técnico |
|---|---|
| Pantalla de carga con número que sube y una cortina de color que barre | **preloader con counter 0→100 + reveal curtain (clip-path wipe)** |
| Que el hero aparezca lento por partes después de cargar | **staggered reveal on load** con `MIN_VISIBLE_MS` garantizado |
| Que el texto aparezca letra por letra con rebote suave | **split text por letra + spring (tension 120-280, friction 12-26)** |
| Que la imagen se arme con cuadritos que van apareciendo en desorden | **pixel reveal / entrance reveal por grid** (celdas con `transition-delay` aleatorio o por patrón) |
| Que el logo se dibuje solo y luego se abra la página | **smooth loader**: máscara sobre el logo + salida en `clip-path` (no un spinner) |
| Que al bajar el scroll una sección tape a la anterior | **stacked / sticky sections** (`position: sticky` + z-index escalonado) |
| Que el fondo cambie de color según la sección donde voy | **scroll-linked background transition** por `IntersectionObserver` |

**Ojo con los tres primeros:** en los reels salen hechos en Framer, que es una herramienta
de arrastrar. Aquí se hacen a mano con CSS y JS puros, y quedan igual o mejor, porque el
efecto es geometría y tiempo, no una plantilla. No sirve de excusa "eso es de Framer".

## Estados: cuando la interfaz responde a una acción

Esta familia no existía en el vocabulario y es la que más pesa en conversión, porque vive
justo en el momento en que el cliente ya hizo lo difícil.

| Lo que quieres decir | Término técnico |
|---|---|
| Que al enviar el pedido salga una confirmación que se dibuja sola, no un texto plano | **success state animado**: círculo que se expande + marca dibujada con `stroke-dasharray` + micro-partículas · 600-900 ms y se queda quieto |
| Que el botón muestre que está trabajando sin que parezca colgado | **estado de carga en el propio botón** (el texto se sustituye, el ancho no cambia) |
| Que un campo avise del error sin recargar ni gritar | **validación en vivo**: borde y mensaje aparecen bajo el campo, nunca un popup |
| Que se sienta que faltan pocos pasos | **indicador de progreso por segmentos**, no barra continua |

> ⚠️ **En contra entrega el estado de confirmación NO es decoración, es la venta.** El cliente
> acabó de dar nombre, teléfono y dirección **sin pagar nada**, y si la pantalla no le confirma con
> claridad que el pedido quedó, se va con la duda — y esa duda reaparece cuando lo llaman a
> confirmar por WhatsApp, convertida en cancelación. La confirmación debe decir **qué pasó, qué
> sigue y cuándo**: "pedido recibido · te escribimos hoy por WhatsApp · pagas al recibir".

## Navegación y barras

| Lo que quieres decir | Término técnico |
|---|---|
| Que la barra se deforme alrededor de la pestaña activa en vez de que un fondo se deslice | **morphing dock**: la barra es UN path SVG y la muesca se recalcula por tangentes · no hay pastilla que viaje |
| Que el menú se pegue arriba al bajar y se encoja | **sticky header con estado compacto** por umbral de scroll |
| Que el icono activo suba y los demás se aparten | **desplazamiento por vecindad** (efecto dock de macOS) |

## Partículas y nubes de puntos

| Lo que quieres decir | Término técnico |
|---|---|
| Nube de puntitos que forma una figura (una cara, un objeto) | **point cloud / particle system** (`THREE.Points`) |
| Ola o duna de partículas que ondula sola sin parar | **flow field**: desplazamiento por ruido (simplex o senos apilados), loop infinito |
| Que las partículas brillen como brasas | **material emisivo + bloom** (post-processing `UnrealBloomPass`) |
| Que la figura se desarme en polvo | **dissolve / disintegration** por densidad variable |
| Cara o figura hecha de cuadritos | **dot-matrix / halftone 3D** |

## Materiales (el look del objeto)

| Lo que quieres decir | Término técnico |
|---|---|
| Objeto cromado que refleja lo de alrededor | **chrome + environment map (HDRI)**, `metalness 1 / roughness 0.05` |
| Esferas de mercurio líquido | **liquid metal**, chrome con `roughness 0` y distorsión |
| Vidrio esmerilado translúcido | **frosted glass** — `MeshTransmissionMaterial`, refracción + `roughness 0.2` |
| Vidrio transparente que deforma lo que hay detrás | **refraction / transmission**, `ior 1.5`, `thickness` alto |
| Que brille desde adentro | **emissive material** + bloom |
| Cerámica mate sin brillo | **matte / ceramic**, `roughness 0.9 / metalness 0` |
| Que cambie de color según el ángulo | **iridiscencia / thin-film** |

## Luz y atmósfera

| Lo que quieres decir | Término técnico |
|---|---|
| Fondo negro con una sola luz cálida | **single key light sobre negro absoluto**, alto contraste |
| Rayos de luz atravesando el fondo | **god rays / luz volumétrica** |
| Halo alrededor de lo que brilla | **bloom** (con mesura: `strength 0.6-1.2`) |
| Que el fondo tenga profundidad borrosa | **depth of field (DOF)** |
| Neblina que oculta lo lejano | **fog exponencial** |

## Movimiento e interacción

| Lo que quieres decir | Término técnico |
|---|---|
| Que la nube o el objeto siga el mouse | **cursor-follow con lerp/damping** (inercia, factor 0.06-0.12) |
| Estela que deja al moverse | **trail / motion trail** |
| Que el objeto se arme o gire al hacer scroll | **scroll-driven 3D**: cámara sobre timeline (**GSAP ScrollTrigger**) |
| Que el scroll se sienta como una cámara de cine | **camera dolly + smooth scroll (Lenis)** |
| Que el fondo se mueva más lento que el frente | **parallax por capas** |
| Que todo se mueva lento y con clase | **easing suave**, `cubic-bezier(.22,1,.36,1)`, 800-1400 ms, **cero bounce** |
| Que reaccione al pasar el mouse por encima | **hover state con transición 200-320 ms** |

## Estructura y tipografía

| Lo que quieres decir | Término técnico |
|---|---|
| Letra gigante de titular | **display type**, máximo 2 líneas, 11-18vw |
| Letritas técnicas con espacio entre letras | **micro-label / eyebrow**, 10px, tracking amplio, mayúsculas |
| Numerito de sección tipo (026) | **section index / numeración editorial** |
| Reloj en vivo con la ciudad arriba | **live local time en el header** |
| Texto que baja en diagonal | **rotated section copy / layout inclinado** |
| Tarjetas de datos en cuadrícula | **bento grid** de métricas |
| Líneas blancas finas de esfera u órbitas | **wireframe overlay**, trazo de 1px |

## Fondo del hero

| Lo que quieres decir | Término técnico |
|---|---|
| Fondo de video pesado y bonito | **hero background video** en `<video muted loop playsinline>`, render pre-hecho |
| Que el fondo sea 3D de verdad | **escena WebGL a pantalla completa** detrás del contenido |
| Colores exactos de la marca | **bloque `:root` de design tokens** (hex + gradiente con grados y stops) |

## La frase que resume todo

> *"AI builds generic. We make it cinematic."*

Es de la agencia de referencia y describe el problema exacto: **lo genérico sale solo;
lo cinematográfico hay que pedirlo con números.**

## Plantilla de encargo (cópiala y llénala)

```
ESCENA: <objeto protagonista — ej. duna de partículas que ondula>
MATERIAL: <ej. puntos emisivos naranja→blanco>
FONDO: <ej. negro absoluto #000000>
LUZ: <ej. una sola fuente cálida abajo-centro + bloom 0.9>
PALETA: <hex exactos: fondo / acento 1 / acento 2 / texto>
MOVIMIENTO: <ej. loop infinito + cursor-follow con inercia 0.08>
ENTRADA: <ej. preloader contador 0→100, cortina naranja, mínimo 1300ms>
TIPOGRAFÍA: <display + micro-label>
RITMO: <lento cinematográfico / enérgico>
ENTREGABLE: <HTML de un archivo / proyecto Next>
```

Con esa plantilla llena, la página sale a la primera. Sin ella, sale el promedio.
