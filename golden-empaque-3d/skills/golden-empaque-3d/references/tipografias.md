# Catálogo de tipografías

Catorce familias de Google Fonts, elegidas para que cada una diga algo distinto sobre el
producto. No es una lista de fuentes bonitas: es un rango de posicionamientos.

## Las catorce

| Familia | Carácter | Le queda bien a |
|---|---|---|
| **Bodoni Moda** | Didone de alto contraste, remates finísimos | Perfumería y cosmética de lujo. Es la opción para marcas con logotipo tipo didone |
| **Italiana** | Serif muy fina y alta, muy espaciada | Piezas altas y estrechas, alta gama silenciosa |
| **Playfair Display** | Serif editorial, contrastada pero robusta | Marcas que quieren verse establecidas |
| **Cormorant Garamond** | Garalda clásica, elegante y ligera | Artesanal, botánico, herbolario |
| **DM Serif Display** | Serif de titular, con peso | Cuando el nombre tiene que pesar en una cara pequeña |
| **Marcellus** | Romana serena, inspirada en capitulares | Atemporal, farmacéutico de gama alta |
| **Cinzel** | Capitulares romanas, todo mayúsculas | Lujo declarado, perfumería masculina |
| **Spectral** | Serif de lectura, cómoda en texto chico | Cara trasera, ingredientes, modo de uso |
| **Tenor Sans** | Sans elegante con aire de serif | Puente entre lo clásico y lo moderno |
| **Jost** | Geométrica tipo Bauhaus | Limpio, funcional, dermocosmético |
| **Outfit** | Sans geométrica muy limpia | Marcas nuevas, tono directo |
| **Josefin Sans** | Art déco, x pequeña | Retro, artesanal, femenino sin ser dulce |
| **Syne** | Contemporánea, formas raras | Marcas jóvenes que quieren romper |
| **Archivo** | Grotesca sólida, muy legible | Etiquetas técnicas, textos de norma |

## Cómo se cargan

Una sola etiqueta `<link>`, con las familias separadas por `&family=` y los pesos acotados.
No se cargan todos los pesos de todo: catorce familias con todos sus pesos son varios megas.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500;6..96,700&...&display=swap">
```

`display=swap` es obligatorio: sin él la pieza aparece sin texto mientras cargan las fuentes,
y lo primero que ve el usuario es una caja en blanco.

**Google Fonts es el único servidor de tipografías que el sandbox de Artifacts permite.** Una
fuente de cualquier otro origen se cae en silencio y el navegador usa la de respaldo sin
avisar. Por eso toda declaración lleva su pila de respaldo real:

```js
["'Bodoni Moda', serif", "Bodoni Moda — didone de moda"]
```

Nunca `font-family: 'Bodoni Moda'` a secas.

## Cómo se escoge para un producto

1. **Mirar el empaque actual.** Si ya hay un logotipo impreso, la primera opción del selector
   debe ser la más cercana, para que el punto de partida sea reconocible.
2. **El logotipo y el texto secundario no deben ser la misma familia.** Si lo son, la cara se
   ve plana. La plantilla los separa en tres selectores justamente para eso.
3. **La cara trasera pide una serif de lectura o una grotesca**, nunca una display. A 4,5 px
   de tamaño simulado, una Bodoni desaparece.
4. **Lo que decide es el precio.** Una Archivo en un producto de $80.000 lo hace ver de
   $20.000; una Cinzel en uno de $20.000 lo hace ver pretencioso. La tipografía es el ancla de
   categoría más barata que hay, junto con el descriptor.

## Los tres tamaños que importan

| Variable | Rango útil | Qué pasa fuera de rango |
|---|---|---|
| `--logosize` | 14 a 52 px | Bajo 14 no se lee en el visor; sobre 52 se sale de la cara |
| `--varsize` | 8 a 30 px | Debe quedar entre 45% y 60% del logotipo, o compiten |
| `--logotrack` | -0,06 a 0,16 em | Las didone piden interletra negativa; las sans en mayúsculas, positiva |

Regla práctica que la plantilla aplica sola: el tamaño de la variante arranca en 52% del
tamaño del logotipo.
