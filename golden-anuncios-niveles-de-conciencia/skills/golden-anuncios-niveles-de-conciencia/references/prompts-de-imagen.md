# Prompts de imagen para estáticos

Se lee en el paso 4. Fuentes: guía oficial de Google para Nano Banana (05-mar-2026), Cookbook de
OpenAI para GPT Image 2 (21-abr-2026), estructura del prompt de Kevin en pantalla (01-oct, 02:38) y la
lección medida de la casa sobre negativos. Esta skill escribe el prompt; la generación la hace
`golden-imagen-arena` o `golden-ecom-magic`.

## Estructura (una por pieza)

```
<Tipo de pieza>, <relación y medida>, anuncio estático para celular.
Image 1: foto real del producto. Reproduce el producto EXACTAMENTE como Image 1: misma forma, color,
etiqueta, proporción y escala. No lo redibujes ni lo simplifiques.
ESCENA: <dónde, quién, qué hace, narrado como una escena continua>.
COMPOSICIÓN: <encuadre; el producto grande y protagonista; jerarquía 1º, 2º, 3º>.
TEXTO EN LA IMAGEN (español, copiar carácter por carácter, con tildes y ñ, una sola vez):
- Titular: "<...>"
- Apoyo: "<...>"
- Callouts: "<...>"
- Sello: "<...>"
ESTILO: <paleta con códigos, tipografía, luz>.
CÁMARA: <ángulo, profundidad de campo>.
NEGATIVOS: sin logo del proveedor, sin marco ni destellos, sin famosos ni personas reales
identificables, sin logos de terceros, sin deformar el producto.
```

Una persona generada usando el producto **sí va** cuando la pieza la pide (en belleza y salud es
obligatoria en al menos una pieza): el negativo excluye a famosos y a personas reales identificables,
no a la persona de la escena.

## Las reglas, con su porqué

1. **La foto real como Image 1 y la lista de conservación repetida en cada ronda.** Sin referencia el
   generador inventa un producto genérico (documento de Kevin; guía de OpenAI: "preserve product
   geometry and label legibility exactly").
2. **El texto va entre comillas, con tipografía y posición, y "una sola vez".** Así lo piden Google y
   OpenAI. El texto de la imagen sale de la ficha, no se describe.
3. **Los negativos son solo genéricos.** Los prompts de Kevin listan los claims prohibidos en un bloque
   de negativos ("no claims of attracting money…"). La casa midió lo contrario: nombrar una frase
   prohibida hace que el generador la escriba. El claim se controla dictando el texto literal; en
   negativos solo van defectos visuales.
4. **Escena narrada, no lista de palabras.** Google: una lista de palabras clave no basta.
5. **Sin texto en la imagen si el motor rompe los acentos.** Se genera sin texto y el texto se monta
   encima (Kevin lo usa con Canva; la casa lo midió en Higgsfield el 30-ago).
6. **El prompt va en español o en inglés**, pero el texto en pantalla siempre en el español del país.

## Ejemplo completo (TOFU, combo del taller, ya sin promesa)

```
Fotografía publicitaria ultrarrealista, vertical 4:5 a 1080×1350, anuncio estático para celular.
Image 1: foto real de la pulsera. Image 2: foto real del anillo. Reproduce las dos piezas EXACTAMENTE
como Image 1 e Image 2: misma forma, color, grabado y escala. No las redibujes.
ESCENA: una fila de fichas de dominó cayendo sobre una mesa de madera oscura; al final de la fila, la
pulsera y el anillo detienen la caída. Luz cálida lateral de tarde.
COMPOSICIÓN: las dos piezas grandes en el tercio inferior derecho; el titular arriba; el sello abajo.
TEXTO EN LA IMAGEN (español, copiar carácter por carácter, con tildes, una sola vez):
- Titular: "TODOS TENEMOS RACHAS"
- Apoyo: "Hay quien las lleva con un símbolo de la tradición oriental."
ESTILO: negro, dorado y madera; sans-serif condensada blanca para el titular; contraste alto.
CÁMARA: 35 mm a la altura de la mesa, profundidad de campo corta sobre las piezas.
NEGATIVOS: sin logo del proveedor, sin marco ni destellos, sin rostros, sin deformar las piezas.
```

Es TOFU: no nombra el producto en el titular, no lleva precio ni llamado de compra y no le habla a la
situación de quien mira.
