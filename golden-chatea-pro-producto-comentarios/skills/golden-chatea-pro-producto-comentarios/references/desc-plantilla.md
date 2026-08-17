# La `desc` — 500 caracteres y ni uno más

`desc` es todo lo que el bot sabe del producto. Alimenta la variable `{DESCRIPCION_PRODUCTO}` que
usan el prompt de respuesta pública y el de venta conversacional del asistente.

**Tope: 500 caracteres.** Por API entra más y no da error — hasta que alguien abre ese producto en
el panel y guarda, y ahí se corta. Ya pasó: una `desc` de 3.928 caracteres tuvo que recortarse a
483 conservando la regla dura.

> **De dónde sale el 500, con honestidad.** Lo fija `BRIEFING-PARA-SKILLS.md` (2026-08-07) para la
> descripción del producto de Comentarios. La extracción del código de la app
> (`TOPES-NATIVOS-POR-CAMPO.md`) ancla ese `maxLength` de 500 al formulario de producto de **Ventas
> WhatsApp**, y su tabla "definitiva" de los 9 campos de Comentarios **no incluye** la descripción
> del producto. O sea: el número viene del briefing, no de la extracción de código. Trátalo como
> tope firme —es el criterio vigente de la casa y equivocarse por arriba se paga— pero si alguna
> vez alguien mide el formulario en vivo, que anote aquí la fecha y el valor.

**Va con tildes.** Es el texto con el que el bot escribe en público; un acento comido se ve. Cada
tilde pesa 6 contra el techo del campo (ver `escritura-api.md`), pero en 500 caracteres eso son
~150 de 20.000: no es donde se ahorra.

500 caracteres es poco, y esa es la idea. Lo que no cabe **no es que sobre espacio: es que está en
el sitio equivocado**.

---

## Qué va aquí y qué va en el prompt de ventas

| Va en la `desc` de comentarios | Va en el prompt de Ventas WhatsApp (12.000) |
|---|---|
| Qué es y qué hace, en una línea | El descubrimiento y el espejeo del dolor |
| Las variantes o líneas, si las hay | El manejo de objeciones una por una |
| La escalera de precios | El flujo de etapas, la captura de datos, la validación |
| Envío y modelo de pago, en una línea | El resumen y el cierre |
| Las reglas de marca | La prueba social larga, el FAQ, el modo de uso detallado |

Un comentario público se responde en dos o tres frases y se arrastra al privado. Todo el arsenal
de venta vive del otro lado.

---

## Esqueleto (producto ficticio, 461 caracteres)

```
Aurelia Glow es un serum facial de vitamina C al 15% con ácido hialurónico.
Aclara manchas y unifica el tono. Cosmético de uso externo, 30 ml.

PRECIOS
1 unidad: $89.900 con envío gratis
2 unidades: $149.900 con envío gratis

Envío a todo el país. Pago contra entrega. Producto original.

REGLAS DE MARCA
No prometas curar ni tratar condiciones médicas: es un cosmético, no un medicamento.
No inventes ingredientes, tiempos ni resultados distintos a esta ficha.
```

Cuatro bloques, en este orden: **qué es → precios → confianza → reglas de marca**. Los títulos en
mayúscula sin dos puntos gastan menos y se leen igual.

---

## Cómo se recorta (y cómo NO)

Recortar a ojo cuesta cuatro intentos. Mide:

```bash
python3 scripts/validar_producto.py --medir borrador.txt
```

Te dice por cuántos caracteres te pasas y **qué línea pesa más**, que es lo que hay que atacar.

**Orden de recorte, de lo primero a lo último:**

1. **Adjetivos del bloque descriptivo.** "recargable por USB con batería de larga duración, apta
   para todo tipo de piel" → "recargable por USB". El bot no vende aquí, reconoce y responde corto.
2. **La línea de confianza.** "Envío a todo el país con transportadora. Pago contra entrega.
   Producto original con garantía de 30 días" → "Envío a todo el país. Pago contra entrega."
3. **La regla de marca menos específica.** Si tienes tres y una es genérica, esa se va.

**Nunca se recortan:** los precios, ni las dos reglas de marca duras (la frontera legal de la
categoría y la excepción de la oferta). Son las dos cosas que se pagan caro.

Presupuesto orientativo dentro de los 500: descripción ~140 · precios ~110 · confianza ~70 ·
reglas ~150 · margen ~30.

---

## El bloque de reglas de marca no es decorativo

Es lo que evita que la IA rellene los huecos sola, y **viaja con el producto** aunque lo copien a
otro asistente o a otra cuenta. Sin él, la IA completa lo que no sabe — y lo que rellena te lo
reclama el cliente, en público, delante del regulador.

Escribe las reglas **en negativo y concretas**. Dos o tres bien elegidas valen más que seis
genéricas, y aquí el espacio se paga caro.

### Catálogo por categoría · elige la base y adáptala

Cubre el 90% de los productos COD. Toma las dos líneas de tu categoría y añade una tercera
específica del producto si hace falta.

**Cosmético / cuidado de la piel**
```
No prometas curar ni tratar condiciones médicas: es un cosmético, no un medicamento.
No inventes ingredientes, concentraciones, tiempos ni resultados distintos a esta ficha.
```

**Aparato eléctrico / de belleza (depiladora, masajeador, plancha)**
```
Nunca digas que cura, trata o elimina ninguna condición de la piel: es un aparato, no un tratamiento.
No prometas que es indoloro ni que el resultado es permanente.
```

**Suplemento / ingerible**
```
No prometas curar, tratar ni prevenir ninguna enfermedad, ni reemplazar un medicamento.
No des dosis, tiempos de resultado ni recomendaciones médicas: remite a su médico.
```

**Accesorio deportivo / fitness**
```
No prometas bajar de peso, marcar músculo ni resultados en un tiempo determinado: es un accesorio, no un tratamiento.
No inventes material, medidas ni niveles de resistencia fuera de esta ficha.
```

**Ropa / calzado / accesorio**
```
No inventes tallas, materiales, colores ni disponibilidad que no estén en esta ficha.
No prometas equivalencias de talla entre marcas: remite a la tabla de tallas.
```

### La regla que se olvida siempre: la excepción de la oferta

Si una opción de la escalera **no** lleva envío gratis, o no lleva el regalo, **dilo aquí**:

```
El precio de 3 unidades no incluye envío gratis.
```

Es el error que más se comete al improvisar, y el cliente lo reclama con el comentario público
delante.

### Y cualquier criterio que la IA no adivinaría

La palabra prohibida de la marca (`desodorante`, `medicamento`, `réplica`), que las variantes no
se asignan por género, que no se ofrecen descuentos fuera de la lista. Una línea cada uno.

---

## Errores que ya se pagaron

- **Meter el brief de venta completo.** Funciona hoy por API y desaparece el día que alguien
  guarde desde el panel.
- **Un claim médico dentro de la ficha.** Una depiladora que decía "curamos la foliculitis y
  eliminamos los hongos". El bot lo repite en público, donde lo lee el regulador.
- **Precios que no coinciden** con los del mismo producto en Ventas WhatsApp. El cliente ve un
  precio en el comentario y otro en el privado, en la misma conversación.
- **Precio crudo sin formato** (`59900` en vez de `$59.900`). El bot lo lee tal cual.
- **Enlace muerto.** Si la `desc` lleva un link, verifica que responda. Un asistente estuvo meses
  mandando clientes a un handle que devolvía `null` porque el producto se había renombrado.
