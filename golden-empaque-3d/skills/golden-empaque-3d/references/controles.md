# Los ocho grupos de controles

Ninguna mesa se entrega sin los ocho. Si la pieza tiene algo visible que no se puede cambiar,
la mesa está incompleta.

## 1. Referencia

Los presets de variante son el atajo más usado: un clic pone nombre y color de golpe.

```js
var REFS = {
  uno:  {v:'Variante Uno',  b:'#E9C5A8'},
  dos:  {v:'Variante Dos',  b:'#E8A0AE'},
  tres: {v:'Variante Tres', b:'#C9D46A'}
};
```

Más: nombre libre de la variante y contenido declarado (`4 oz / 120 mL`).

## 2. Medidas

Ancho, fondo y alto en **centímetros**, no en píxeles. La constante `PX` traduce
(22 px por cm funciona bien para piezas de 5 a 20 cm). Más el acercamiento, que comparte
valor con la rueda del mouse.

Al cambiar una medida se vuelve a dimensionar cada cara y se recalcula la escala. Si solo se
recalcula una de las dos, la pieza se deforma o se sale.

## 3. Color

Cuatro controles, y el tercero es el que se olvida:

| Control | Nota |
|---|---|
| Franja | paleta de seis más selector libre |
| Cuerpo | blanco, hueso, kraft, negro mate, más libre |
| **Tinta** | automática por contraste, **con opción de forzarla a mano** |
| Fondo del estudio | claro, oscuro, arena, plano |

La tinta automática calcula luminancia relativa y devuelve tinta o blanco:

```js
function contrastInk(hex){
  var c = hex.replace('#','');
  if (c.length === 3) c = c[0]+c[0]+c[1]+c[1]+c[2]+c[2];
  function lin(u){ u/=255; return u<=0.03928 ? u/12.92 : Math.pow((u+0.055)/1.055, 2.4); }
  var L = 0.2126*lin(parseInt(c.substr(0,2),16))
        + 0.7152*lin(parseInt(c.substr(2,2),16))
        + 0.0722*lin(parseInt(c.substr(4,2),16));
  return L > 0.42 ? '#1A1917' : '#FFFFFF';
}
```

**El fondo del estudio no es adorno.** Una caja blanca sobre fondo blanco no se lee, y una
caja oscura sobre fondo oscuro tampoco. Sin ese control, la mitad de las combinaciones de
color quedan imposibles de evaluar.

## 4. Franja

Dónde va (arriba, abajo, ambas, ninguna) y grosor. El tamaño de letra de la franja se deriva
del grosor, no se fija aparte:

```css
.band { font-size: calc(var(--bandh) * .44); }
```

Así la franja nunca queda con letra que se sale al adelgazarla.

## 5. Tipografía

Tres selectores independientes: logotipo, nombre de la variante y texto secundario. Más
tamaño de cada uno, grosor, interletra y orientación del logotipo (vertical u horizontal).

La interletra va en centésimas de `em` en el deslizador y se convierte al aplicar:

```js
setVar('--logotrack', ($('i-logotrack').value / 100) + 'em');
```

Catálogo completo en `tipografias.md`.

## 6. Textos

**Un campo por cada texto visible.** Para una caja plegadiza son ocho: variante, contenido,
descriptor, claim en dos líneas, franja superior, franja inferior y cara trasera.

La cara trasera es un `textarea` y se parte por líneas en blanco; la primera línea de cada
bloque se vuelve el titulillo:

```js
String(v).split(/\n\s*\n/).forEach(function(blk){
  var lines = blk.split('\n'), d = document.createElement('div');
  var b = document.createElement('b');
  b.textContent = lines.shift() || '';
  d.appendChild(b);
  d.appendChild(document.createTextNode(lines.join(' ')));
  el.appendChild(d);
});
```

Sirve además para medir **cuánto texto cabe de verdad** en la cara trasera antes de mandar a
diagramar, que es una pregunta que siempre llega tarde.

Los atajos de texto (botones con el texto ya escrito) son el control que más se usa: ponen la
alternativa recomendada de un clic, sin escribirla.

## 7. Acabados y costo

Cada acabado hace **dos** cosas: cambia la pieza y mueve el precio.

| Acabado | Efecto visual |
|---|---|
| Repujado | `text-shadow` en dos direcciones |
| Reserva UV | degradado sobre el texto con `background-clip: text` |
| Plastificado mate | sombra interior suave en todas las caras |

El modelo de costo vive en tres constantes. **Las de la plantilla son cifras redondas de
ejemplo, deliberadamente falsas**, y se reemplazan por el costeo real del proyecto:

```js
// EJEMPLO. Reemplazar por el costeo del proyecto.
var COST = { termo:500, etiqueta:500, sellos:100, envase:500,
             formula:1000, mo:1000, gasolina:100, domicilio:100 };
var CAJA_BASE = 500.00, PLANCHAS = 100.00;
var FIN = { emboss:300.00, uv:200.00, matte:100.00 };
```

Se eligieron redondas a propósito: un número como `316,67` se ve medido y se copia sin
pensar; un `300,00` se ve de ejemplo y obliga a buscar el real.

Y el precio de venta es un campo editable, para que el margen se recalcule al probar precios.

## 8. Versiones

Guardar con nombre, cargar con un clic, borrar con clic derecho, copiar la ficha al
portapapeles y volver al original.

`localStorage` **siempre** envuelto:

```js
function readSlots(){ try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e){ return {}; } }
function writeSlots(o){ try { localStorage.setItem(KEY, JSON.stringify(o)); return true; } catch(e){ return false; } }
```

En ventana privada falla, y si no está envuelto la página entera se cae.

**"Volver al original" no es un botón de reinicio**: devuelve el empaque que está impreso hoy,
que es contra lo que se compara cada cambio.

## Qué tocar al adaptar la plantilla

| Dónde | Qué cambiar |
|---|---|
| `<title>` y `.brandmark` | nombre del producto |
| Las seis caras en el HTML | el contenido real de cada una |
| `REFS` | las variantes del producto |
| `ORIGINAL` | el estado que reproduce el empaque impreso hoy |
| `DEFAULT_BACK` | el texto real de la cara trasera |
| `COST`, `CAJA_BASE`, `PLANCHAS`, `FIN` | el costeo del proyecto |
| `BRIEF` | producto, precio, categoría y riesgos detectados |
| `KEY` | la clave de `localStorage`, distinta por producto |
| Las paletas de `bandsw` y `bodysw` | los colores de la marca |
