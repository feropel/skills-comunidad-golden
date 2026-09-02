# Atmósferas — el fondo vivo, y por qué ninguna presentación se repite

Un deck sin fondo es una hoja de papel con letras. La atmósfera es lo que separa
"diapositiva" de "experiencia", y es lo primero que hace que alguien pregunte con qué
está hecho.

**La regla que manda:** una presentación de un tema NO puede parecerse a la de otro tema.
Se elige atmósfera, paleta y tipografía por el asunto del que se habla, no por costumbre.

## Índice
1. Las 8 atmósferas
2. El mapa: de qué hablas → cómo se ve
3. Cómo se elige cuando el cliente no sabe
4. Reglas de uso
5. Por qué WebGL puro y no Three.js
6. Rendimiento y degradación

## 1 · Las 8 atmósferas

Todas se tiñen solas con los tokens de marca del deck (`--accent`, `--accent-2`, `--bg`).
Cambiar la paleta cambia el fondo: no hay un solo color escrito en el motor.

| Nombre | Motor | Qué se ve | Sensación que deja |
|---|---|---|---|
| `nebulosa` | WebGL | Flujo de tinta lento, orgánico, reacciona al puntero | Caro, sereno, de marca |
| `aurora` | WebGL | Bandas verticales que respiran, tipo aurora boreal | Amplio, formativo, optimista |
| `pulso` | WebGL | Anillos de interferencia que laten desde dos focos | Energía, evento, urgencia |
| `enjambre` | Canvas 2D | Nodos unidos por líneas; el puntero abre la red | Comunidad, conexión, red |
| `reticula` | Canvas 2D | Malla de puntos que se hunde bajo el cursor | Técnico, preciso, de panel |
| `duna` | Canvas 2D | Campo en perspectiva que ondula, crestas encendidas | Producto, materia, oficio |
| `viaje` | Canvas 2D | Estrellas con dolly hacia el espectador | Lanzamiento, visión, futuro |
| `ninguna` | — | Sin fondo | Sobrio, institucional, serio |

Se activa con un atributo, y nada más:
```html
<body data-atmosfera="nebulosa">
```
En caliente: `Atmosfera.usar('enjambre')` · `Atmosfera.apagar()`

## 2 · El mapa: de qué hablas → cómo se ve

Esta tabla es el corazón de la skill. **Se consulta siempre antes de maquetar.**

| Si el deck habla de… | Atmósfera | Carácter de paleta | Display | Receta de apoyo |
|---|---|---|---|---|
| **El Cartel del Chat**, evento en vivo, bootcamp | `pulso` | Rojo y ámbar sobre negro cálido | Condensada pesada | `balenciaga-post-2017` |
| **Comunidad Golden, MBA**, formación | `aurora` | Verde y dorado sobre verde muy oscuro | Serif humanista | `stripe-press` |
| **Propuesta comercial**, agencia, servicios | `nebulosa` | La del cliente sobre fondo profundo | Serif transitional | `pentagram` |
| **Marca personal de Fer**, charla, keynote | `nebulosa` o `ninguna` | Neutro, acento gris claro | Serif editorial | `monocle-magazine` |
| **Producto físico**, cosmética, cuidado personal | `duna` | Cálida, tierra, un solo acento | Serif clásica | `aesop` |
| **Panel de datos**, reporte, logística, pauta | `reticula` | Fría, azul o verde de instrumento | Grotesca neutra | `tufte-dataink` · `bloomberg-terminal` |
| **Comunidad, alumnos, red, networking** | `enjambre` | Acento vivo sobre oscuro | Grotesca moderna | `linear` |
| **Lanzamiento, visión, apertura de año** | `viaje` | Alto contraste, un acento | Display grande | `active-theory` |
| **Corporativo serio**, legal, institucional | `ninguna` | Sobria, poco acento | Grotesca suiza | `vignelli-swiss-helvetica` |
| **Producto digital, software, herramienta** | `reticula` | Un acento eléctrico | Grotesca de interfaz | `raycast` · `vercel-mesh` |

Las recetas de apoyo viven en `~/.claude/skills/web-design-engineer/references/style-recipes/`
(26 archivos). Cada una trae paleta con hex, tipografía con pesos, escala de espaciado,
carácter de movimiento y **su propia lista de prohibiciones**.

**Se lee UNA receta, no el catálogo.** Cargar las 26 es el antipatrón que ese catálogo
existe para evitar.

**⚠️ Los nombres de receta NUNCA salen al cliente.** Son vocabulario interno. Al cliente se
le presenta la dirección con nombre propio y se le describe por lo que hace, jamás por a
quién se parece. Un cliente que oye el nombre de otra marca entiende que le copiaron.

## 3 · Cómo se elige cuando el cliente no sabe

Se le enseñan **tres** direcciones de filas distintas de la tabla, cada una con su nombre
propio y una frase de qué transmite. Nunca se pregunta "qué colores te gustan", porque la
respuesta a esa pregunta produce el promedio.

```
Para tu presentación veo tres caminos:
1. SALA · fondo de pulsos rojos, tipografía condensada. Transmite urgencia y evento en vivo.
2. TALLER · verdes que respiran, serif humanista. Transmite aprendizaje y calma.
3. INSTRUMENTO · retícula técnica azul, tipografía de interfaz. Transmite precisión y datos.
```

Cuando el cliente ya tiene ancla ("quiero algo tipo Linear"), se va directo a esa receta.

## 4 · Reglas de uso

1. **Una atmósfera por deck.** Cambiar de fondo entre láminas marea y delata la plantilla.
   La excepción justificada es una sola lámina de clímax; se decide a propósito, no por
   inercia.
2. **El fondo nunca compite con el texto.** Si hay que entornar los ojos para leer, la
   atmósfera pierde: se sube `--vidrio`, se baja la opacidad del canvas, o se cambia de
   atmósfera. El verificador mide el contraste del texto, no la belleza del fondo.
3. **La atmósfera se elige por el TEMA, no por lo que se ve bonito hoy.** `pulso` en una
   propuesta legal es ruido; `ninguna` en un lanzamiento es un funeral.
4. **En móvil el fondo se atenúa solo** (opacidad 0.42) y las láminas se vuelven sólidas.
   No se toca: es lo que mantiene el texto legible cuando la lámina ocupa todo el ancho.
5. **`ninguna` es una elección legítima.** Un deck institucional con tipografía impecable y
   fondo liso puede ser más caro que uno con partículas. El efecto no sustituye al criterio.

## 5 · Por qué WebGL puro y no Three.js

Decisión medida, no preferencia:

- **La ley de la skill es cero dependencias de red.** Three.js entra por CDN, y un CDN
  caído el día de la presentación es el desastre completo. Con WebGL puro no hay ninguna
  petición: el deck corre desde un USB, sin wifi, en el portátil de la sala.
- **Hallazgo registrado en el Centro de Mando:** un fragment shader de ~1 KB, interactivo
  al puntero, sostiene el framerate en móvil donde una escena Three.js no. En tráfico móvil
  de Golden eso no es un detalle.
- **Coste real medido:** las 8 atmósferas juntas ocupan 17 KB dentro del archivo. Three.js
  solo, minificado, ronda los 600 KB.

`golden-cinematica` sigue siendo la skill cuando el encargo necesita una escena 3D de
verdad (un objeto cromado protagonista, un modelo que rota, un entorno HDRI). Aquí el fondo
acompaña; allí la escena ES la página.

## 6 · Rendimiento y degradación

El motor ya trae todo esto resuelto, y conviene saberlo antes de tocarlo:

- **Se pausa con la pestaña oculta** (`document.hidden`). No quema batería en segundo plano.
- **`prefers-reduced-motion`:** pinta UN fotograma y se detiene. Queda la textura, se va el
  movimiento. Nunca un fondo muerto.
- **DPR limitado a 1.5** y densidad reducida por debajo de 900 px de ancho.
- **Sin WebGL** (equipo viejo, driver bloqueado), las de shader caen a una 2D equivalente:
  `nebulosa`→`duna`, `aurora`→`reticula`, `pulso`→`enjambre`. Nunca a un hueco negro.
- **En impresión y PDF la atmósfera desaparece** y las láminas vuelven a ser sólidas.

Si aun así el equipo de la sala va justo, la salida ordenada es `data-atmosfera="ninguna"`,
no bajar la calidad del texto.

## Encadena con
- `web-design-engineer` → las 26 recetas de estilo. Una por deck, entera, prohibiciones incluidas
- `golden-cinematica` → cuando hace falta una escena 3D real y no un fondo
- `golden-brand-brain` → la paleta del cliente sale de ahí antes que de ningún sitio
- `golden-web/references/estandar-movimiento.md` → los números del movimiento de interfaz
