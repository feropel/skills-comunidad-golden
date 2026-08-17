# Rúbrica del jurado

Mira cada imagen con el tool `Read` (no juzgues por el prompt, juzga por el píxel).
El veredicto es **holístico 1-1000**: una lectura del TODO, no la suma de casillas. Los
seis ejes de abajo son las lentes con las que miras, no una calculadora.

## Descalificación inmediata (la pieza no compite, da igual lo demás)

1. **Producto adulterado** — envase deformado, logo cambiado, etiqueta reinventada, color
   distinto al real, texto falso impreso sobre el empaque.
2. **Botón o CTA clickeable dibujado** — rompe la ley 3 y frustra al comprador que le da
   clic a un dibujo.
3. **WhatsApp incrustado** — número, ícono verde o keyword dentro de la imagen.
4. **Claim inventado** — cualquier promesa que el dueño del negocio no dio.
5. **Texto ilegible o cortado** por el borde, o en un idioma que no es el del mercado.

## Los seis ejes

| Eje | Qué miro | Señal de que está mal |
|---|---|---|
| **Fidelidad del producto** | Es el mismo producto de la foto, sin retoques inventados? | Envase "mejorado", etiqueta borrosa o rehecha |
| **Legibilidad a 390 px** | Achica mentalmente a ancho de celular: se lee el titular de un vistazo? | Titular fino, bajo contraste, más de 7 palabras |
| **Jerarquía visual** | El ojo va hook → producto → beneficio, en ese orden? | Todo del mismo tamaño, ruido, tres focos compitiendo |
| **Limpieza** | Cero elementos que finjan ser interfaz? | Cajas con sombra tipo botón, flechas de UI |
| **Coherencia de marca** | Paleta, tono y estética calzan con el cliente? | Look "IA genérica", degradados morados de stock |
| **Fuerza del ángulo** | Ataca un dolor real o solo describe el producto? | "Producto de calidad" en vez del dolor concreto |

## Bandas del veredicto

- **900-1000** — se publica hoy tal cual. Producto fiel, texto que vende y se lee, marca
  coherente. Reservado para lo que de verdad no tiene nada que arreglar.
- **750-899** — buena, se publica con un retoque menor (recorte, un texto).
- **500-749** — sirve de base pero hay que regenerarla con instrucciones concretas.
- **250-499** — falla en algo estructural (jerarquía o ángulo). Cambiar motor o prompt.
- **1-249** — descalificada o inservible.

## Cómo se entrega el veredicto

Un ranking, del ganador al último, y por cada pieza:

```
🥇 <motor> — <puntaje>/1000
   Gana porque: <2 líneas concretas, señalando lo que se ve>
   Le falta: <lo que habría que retocar, si algo>
```

Cierra con:
- **Motor default de este producto:** cuál queda fijado para las siguientes piezas.
- **Qué ajustar en el prompt** para la próxima ronda (aprendizaje, no solo resultado).
- **Créditos gastados y saldo.**

Sé duro. Un ranking donde todos son buenos no sirve para decidir, y el objetivo de la
arena es cerrar la decisión, no repartir diplomas.
## v1.2 — 2026-07-29 — Regla dura: dato duro en imagen se verifica letra por letra contra la fuente (caso Mambut/Matribust, motor descalificado).
