# El método del `rela` — cómo se construyen los disparadores

`rela` es una **cadena de texto con fragmentos separados por comas**. No es un array. El
asistente compara el texto del comentario y del post contra esos fragmentos para decidir a qué
producto pertenece.

Es la llave que más se subestima y la que decide si el asistente sirve. Sin ella no hay nada más:
**el asistente de comentarios no tiene campo de ID de anuncio** (verificado en vivo el
2026-08-07), así que no existe una segunda vía de anclaje.

---

## Las 5 capas · un `rela` completo las tiene todas

Escribe las capas en este orden. El orden no cambia el emparejamiento, pero hace el campo legible
para quien lo mantenga dentro de seis meses.

### Capa 1 · El nombre, en todas sus formas
El nombre comercial, **con tilde y sin tilde**, junto y separado, con y sin apóstrofo.

```
Frescalia, Frescalía, Frescalia Spray, frescalia
```

Las tildes importan de verdad: la gente comenta desde el teclado del celular y casi nadie las
pone. Un `rela` que solo trae la forma bonita del nombre pierde la mitad de los comentarios.

### Capa 2 · Los errores de escritura reales
Cómo lo escribe mal la gente, no cómo debería escribirlo.

**Banco de patrones** — aplícalos al nombre y quédate con los 3 o 4 que suenen plausibles. No
hacen falta veinte erratas: hacen falta las que alguien escribiría de verdad.

| Patrón | Ejemplo sobre un nombre inventado |
|---|---|
| Letras que suenan igual: b/v, s/c/z, ll/y, g/j, h muda | `Vellux` → `belux`, `bellux` |
| Doble letra que se pierde (o que se dobla de más) | `Vellux` → `velux`, `vellucks` |
| El nombre en inglés escrito como se oye | `Fit Band` → `fit ban`, `fitban` |
| Junto y separado | `Nordika Fit Band` → `nordikafitband`, `nordika fitband` |
| Terminación castellanizada | `Nordika` → `nordica` |
| Tilde puesta donde no va (el corrector del celular) | `Tera` → `terá` |

```
frescalia, fresalia, frescalía, frezcalia, fresca lia
```

**Estas erratas SÍ pueden ir sueltas aunque sean cortas.** Es la única excepción a la regla del
disparador genérico de más abajo, porque una variante ortográfica de la marca no existe en otros
contextos. El validador las reconoce y no las marca: no las estropees añadiéndoles la categoría
(`velux depiladora`), porque quien escribe mal la marca casi nunca añade la categoría.

### Capa 3 · Los sinónimos y la categoría
Cómo llama la gente al producto cuando no recuerda la marca, y **el problema que viene a
resolver**, que es como lo escriben en los comentarios.

```
spray íntimo, spray intimo, frescura íntima, mal olor, olor íntimo, neutralizador de olores
```

Aquí también entran las **variantes o líneas** (sabores, colores, presentaciones), porque la gente
comenta preguntando por una en concreto.

### Capa 4 · Los hooks LITERALES de los anuncios que están corriendo
Esta es la capa que más rinde y la que más se olvida. Copia **textualmente** la primera línea de
cada copy activo — la que el usuario ve justo encima del comentario — más los títulos y las
frases de cierre.

```
Neutraliza el mal olor hasta 48 horas, no tapa el olor lo neutraliza, elige tu aroma
```

Cuando un comentario no trae palabra clave (que es lo normal: *"info"*, *"precio"*, *"cuánto
vale"*), lo único que el asistente tiene para anclar es el **texto del post**. Si ese texto no
está en ningún `rela`, sale *"comentario NO automatizado"* aunque los productos estén cargados.

> **Esto obliga a un paso de mantenimiento:** cada vez que se cambian, rotan o reescriben los
> copys de Meta de ese producto, hay que volver y actualizar esta capa. Es parte del montaje de
> campañas. Un anuncio nuevo con copy nuevo y `rela` viejo es un producto invisible.

⚠️ **Un hook con coma no se puede pegar literal.** El separador del campo ES la coma, así que
*"No tapa el olor, lo neutraliza"* se parte en dos fragmentos y la frase completa deja de existir.
Los copys de Meta llevan comas a diario, y esta es la capa que más rinde: es justo donde no
conviene perder filo. Qué hacer, en este orden:

1. **Parte el hook a propósito** y quédate con las mitades que se sostienen solas. En
   *"No tapa el olor, lo neutraliza"*, `no tapa el olor` es un fragmento literal del post y
   empareja bien; `lo neutraliza` es demasiado corto y genérico, así que se descarta.
2. **Añade además la frase entera sin la coma** (`no tapa el olor lo neutraliza`), por si el
   emparejamiento va por texto corrido. Así cubres las dos formas sin depender del separador.

Lo que no se hace: pegar el hook con la coma y darlo por cargado.

### Capa 5 · Las preguntas típicas del comentario
Lo que la gente escribe cuando pregunta — **siempre atado al producto**.

```
precio del spray Frescalia, cuánto vale Frescalia, hacen envíos de Frescalia, cómo pido el Cítrico 36
```

> ⚠️ **Esta capa es la que fabrica colisiones si la escribes en genérico.** `hacen envíos` y
> `cómo lo pido` valen para cualquier producto: en cuanto hay dos en el campo, esos disparadores
> están repetidos y el bot elige uno distinto cada vez. Con un solo producto no se nota; el día
> que entra el segundo, empieza a responder mal.
>
> **Y no basta con atarla a la categoría: hay que meter la MARCA.** `hacen envíos de la crema`
> colisiona el día que entre la segunda crema, y `cómo pido el serum` el día que entre el segundo
> serum. Categorías como crema, spray, serum, base, kit o banda no distinguen a nadie ni aunque
> estén en el nombre del producto. El validador marca las que se te pasen.

---

## Cuántos disparadores

**Entre 15 y 30** para un producto con pauta corriendo. Menos de 8 es un producto que va a fallar.

No hay tope propio del `rela`, pero **todo el campo comparte el techo del bot field** (la física
está en `escritura-api.md`; el validador la mide). Lo que importa aquí: si el campo se acerca al
techo, **recorta primero las `desc`, nunca los `rela`**. La `desc` la usa el bot *después* de
reconocer el producto; el `rela` es lo que decide si llega a reconocerlo.

---

## Lo que NUNCA va en un `rela`

**Palabras genéricas sueltas.** Un token corto que existe en mil contextos secuestra comentarios
de otros productos y de otros posts.

| ❌ Secuestra | ✅ Distingue |
|---|---|
| `base` | `base coreana, cushion, base hidratante` |
| `crema` | `crema reafirmante de cuello` |
| `spray` | `spray íntimo, spray para pies` |
| `hongos` | `hongos en las uñas, uñas con hongos` |
| `brillo` | `brillo en el rostro, control de brillo facial` |

**La regla, tal como la aplica el validador:** un disparador vale si trae **la marca dentro**, o
**dos palabras con contenido**, o **una sola muy específica** (7 letras o más). Palabras como
`envío`, `precio`, `info`, `hacen` o `cómo` no cuentan como contenido: aparecen en cualquier
comentario de cualquier producto.

Y una categoría suelta (`crema`, `spray`, `serum`, `base`, `kit`, `banda`) **no distingue ni
aunque esté en el nombre del producto**: el día que entre el segundo producto de esa categoría,
los dos se pelean por ella.

Única excepción: las **erratas de la marca** de la capa 2 sí pueden ir sueltas y cortas, porque no
existen en otros contextos. El validador las reconoce.

**Disparadores repetidos entre dos productos del mismo campo.** Si `spray` está en dos productos,
el bot elige uno y elige distinto cada vez.

**Y disparadores CONTENIDOS en el de otro producto.** `entrenar en casa` dentro de
`entrenar en casa sin excusas` engancha igual que un duplicado exacto, y es más difícil de ver.
Antes de entregar, cruza los `rela` de todos los productos; el validador caza los dos casos.

Dentro del **mismo** producto la contención sí es normal y deseable: el hook con emoji y el mismo
hook sin emoji, o con y sin tilde. Eso no es colisión, es cobertura.

**Nombres o marcas de otro negocio.** En cuentas heredadas de una plantilla aparecen la marca del
profesor y transportadoras de otro país metidas en los ganchos. La IA los imita.

---

## Emojis en el `rela`

Los `rela` en producción **sí llevan emojis** cuando el hook del anuncio los lleva, y emparejan
bien. Esto es distinto del **activador / palabra clave del asistente de Ventas WhatsApp**, donde
un emoji (4 bytes) corrompe el trigger y el bot no arranca jamás.

Aun así, dos cautelas:

1. **Un emoji pesa 12 contra el techo escapado, no 1.** Un `rela` cargado de emojis consume el
   presupuesto del campo entero muy rápido. Mídelo con el validador, no a ojo.
2. **Emparejar no debería depender de un emoji.** Si copias un hook con emoji, incluye también la
   **misma frase sin él**. Así el disparador funciona aunque el comentarista escriba el texto a
   mano o la plataforma normalice el carácter.

```
🌸 Neutraliza el mal olor hasta 48 horas, Neutraliza el mal olor hasta 48 horas
```

---

## Cómo se ve un `rela` completo (producto ficticio)

```
Aurelia Glow, aurelia glow, Aurelia, aurelía, aurelia gloow, aurelia glou,
serum de vitamina C, serum vitamina c, serum para manchas, manchas en la cara,
manchas oscuras, paño en el rostro, pano en el rostro, piel opaca, tono disparejo,
✨ Manchas más claras en 21 días, Manchas más claras en 21 días,
Manchas mas claras en 21 dias, la rutina de una sola gota, tu piel amanece distinta,
precio del serum Aurelia Glow, cuánto vale el Aurelia Glow,
hacen envíos de Aurelia Glow, cómo pido el Aurelia Glow
```

24 disparadores, las 5 capas presentes, el hook con emoji / sin emoji / sin tildes, las erratas de
marca sueltas (legítimas), y **ninguna pregunta genérica**: las cuatro de la capa 5 llevan el
producto dentro.

---

## El límite honesto del método

Ni el mejor `rela` cubre un comentario totalmente genérico — *"de dónde viene el nombre"*,
*"cuánto vale"* a secas, *"info"* — en un post que tampoco aporta texto reconocible. Eso se
resolvería anclando el comentario al ID del anuncio, y **ese campo no existe en el asistente de
comentarios**. Mientras Chatea no lo exponga, un comentario genérico es una lotería entre los
productos `activo` y el `rela` es la única defensa.

Dos consecuencias prácticas que sí puedes controlar:

- **Menos productos en `activo`, menos lotería.** Un producto sin pauta corriendo no gana nada
  estando `activo`, y sí empeora el emparejamiento de los demás. Ponlo en `inactivo`.
- **Cubre el texto del post, no solo el del comentario.** Es lo que hace la capa 4, y es la que
  convierte un comentario genérico en un acierto.
