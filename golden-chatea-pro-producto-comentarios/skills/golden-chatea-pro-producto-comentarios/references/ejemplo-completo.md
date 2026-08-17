# Ejemplo horneado de punta a punta (producto FICTICIO)

Producto inventado para la skill. Ningún dato es de un negocio real. Úsalo como **vara de
calidad**: tu salida debe tener este nivel de detalle y estas medidas.

**Encargo simulado:** *"Súbeme el serum de vitamina C al asistente de comentarios. Es Colombia,
$89.900 la unidad y $149.900 dos. Los anuncios que están corriendo dicen 'Manchas más claras en
21 días' y 'la rutina de una sola gota'."*

---

## El objeto final (este es el que se copia)

```json
[
  {
    "img": "https://cdn.ejemplo-ficticio.com/aurelia-glow-portada.webp",
    "name": "Aurelia Glow | Serum de Vitamina C para Manchas (30 ml)",
    "desc": "Aurelia Glow es un serum facial de vitamina C al 15% con ácido hialurónico.\nAclara manchas y unifica el tono. Cosmético de uso externo, 30 ml.\n\nPRECIOS\n1 unidad: $89.900 con envío gratis\n2 unidades: $149.900 con envío gratis\n\nEnvío a todo el país. Pago contra entrega. Producto original.\n\nREGLAS DE MARCA\nNo prometas curar ni tratar condiciones médicas: es un cosmético, no un medicamento.\nNo inventes ingredientes, tiempos ni resultados distintos a esta ficha.",
    "rela": "Aurelia Glow, aurelia glow, Aurelia, aurelía, aurelia gloow, aurelia glou, serum de vitamina C, serum vitamina c, serum para manchas, manchas en la cara, manchas oscuras, paño en el rostro, pano en el rostro, piel opaca, tono disparejo, ✨ Manchas más claras en 21 días, Manchas más claras en 21 días, Manchas mas claras en 21 dias, la rutina de una sola gota, tu piel amanece distinta, precio del serum Aurelia Glow, cuánto vale el Aurelia Glow, hacen envíos de Aurelia Glow, cómo pido el Aurelia Glow",
    "estado": "activo"
  }
]
```

**Medidas** (salida real del validador, no estimadas): `desc` 461/500 · `rela` 24 disparadores ·
campo **1.146 crudos / 1.272 escapados** de 20.000 · cero avisos, cero errores.

Fíjate en la distancia entre los dos números: 1.146 crudos pesan 1.272 escapados. Son las tildes y
el emoji. Por eso el techo se mide escapado y no con `len()`.

---

## Lo que la skill resolvió sola

| Dato | De dónde salió |
|---|---|
| Moneda y formato `$89.900` | COLOMBIA en `paises.md` — punto de miles, sin decimales |
| Vocabulario: *envío a todo el país*, contra entrega | pack Colombia |
| `estado: "activo"` | tiene pauta corriendo |
| Reglas de marca | catálogo por categoría, base **cosmético** |
| Los 24 disparadores | las 5 capas de `rela-metodo.md` sobre el nombre y los dos hooks |

Solo hizo falta preguntar el país, el nombre y el precio. Los hooks los aportó el vendedor sin que
se los pidieran de a uno.

---

## El desglose del `rela`

| Capa | Disparadores |
|---|---|
| 1 · nombre | `Aurelia Glow, aurelia glow, Aurelia, aurelía` |
| 2 · erratas | `aurelia gloow, aurelia glou` |
| 3 · categoría y problema | `serum de vitamina C, serum vitamina c, serum para manchas, manchas en la cara, manchas oscuras, paño en el rostro, pano en el rostro, piel opaca, tono disparejo` |
| 4 · hooks literales | `✨ Manchas más claras en 21 días` + la misma sin emoji + la misma sin tildes + `la rutina de una sola gota, tu piel amanece distinta` |
| 5 · preguntas | `precio del serum Aurelia Glow, cuánto vale el Aurelia Glow, hacen envíos de Aurelia Glow, cómo pido el Aurelia Glow` |

Detalles que no son casualidad:

- El hook va en **tres formas**: con emoji, sin emoji y sin tildes. El emparejamiento no debe
  depender de un carácter de 4 bytes ni de que alguien acentúe desde el celular.
- `paño` va con y sin tilde por lo mismo.
- No hay ningún `serum` suelto: con dos serums en el catálogo, esa palabra sola secuestraría los
  comentarios del otro.
- **Las cuatro preguntas de la capa 5 llevan la MARCA dentro**, no la categoría. `hacen envíos`
  a secas colisiona con cualquier producto, y `hacen envíos del serum` colisionaría el día que
  entre el segundo serum al catálogo.
- La capa 4 es la que responde el comentario genérico (*"precio?"*), porque ancla por el texto del
  post y no por el del comentario.

---

## El error que hubo por el camino (y cómo se corrigió)

El primer borrador de la `desc` medía **553**. Se veía perfecto y habría entrado por API sin un
solo aviso — para desaparecer meses después, el día que alguien abriera el producto en el panel.

Así se midió, sin adivinar:

```bash
python3 scripts/validar_producto.py --medir borrador.txt
```

```
  desc: 553 / 500 caracteres
  SE PASA POR 53. Recorta en este orden:
    1. adjetivos del bloque descriptivo
    2. la linea de confianza (envio / pago / original)
    3. la regla de marca menos especifica
```

Lo que se fue: *"de vitamina C estabilizada"* → *"de vitamina C"*; *"Uso cosmético externo"* →
*"Cosmético de uso externo"*; *"Envío a todo el país con transportadora"* → *"Envío a todo el
país"*; y la tercera regla de marca, que era la menos específica. Los precios y las dos reglas
duras no se tocaron. Resultado: **461**.

---

## Lo que se entrega junto al JSON

1. El **bloque copiable** con el JSON compacto que imprime el validador.
2. **Dónde va:** bot field `[Comentarios] Productos` (tipo `array`) — y si existe
   `[Comentarios] Productos extendido`, la **misma** copia también ahí.
3. Las **medidas** y el veredicto del validador (`--json` si otra skill va a consumirlo).
4. **Lo que quedó pendiente:** la URL de `img` verificada, si el cliente aún no la tiene.
5. **El recordatorio de mantenimiento**, siempre: *cuando cambien los copys de Meta de este
   producto, hay que volver y actualizar la capa 4 del `rela`, o el bot dejará de reconocer sus
   comentarios.*
