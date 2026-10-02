# Fichas, esquema de matriz.json y revisión visual

Se lee en los pasos 1, 4 y 5. El formato de ficha viene del documento del módulo 3 de Kevin (taller
01-oct, 02:32:36) y de la captura que FER compartió; los campos de la casa (foto real, destino,
relación, variables) vienen de las leyes de imagen de Golden.

## 1. Ficha de producto (10 campos)

Se llena desde el estudio. Lo que el estudio no trae se escribe **"(por confirmar)"** y **no se nombra
en ningún texto** de las piezas: ni material, ni medida, ni certificación. Kevin: *"no se menciona
'obsidiana' ni 'plata' en ningún copy hasta tenerlo"*.

| # | Campo | Qué lleva |
|---|---|---|
| 1 | Identificación | Qué es, unidad o combo, descripción visual, material confirmado o "(por confirmar)" |
| 2 | Ángulo o gran concepto | El principal y los alternos, del estudio |
| 3 | Dolor o deseo | Cuál, y cuál se descarta a propósito y por qué |
| 4 | Promesa y contundencia | 🟢 hechos del producto · 🟡 lo que se dice con cuidado · 🔴 lo que no se afirma |
| 5 | Mecanismo | Por qué funciona; si no hay mecanismo causal, se dice |
| 6 | Beneficios en lenguaje del cliente | Frases como las diría quien compra |
| 7 | Objeciones | Cada una con su respuesta honesta, o "no responder hasta tener el dato" |
| 8 | Atributo bandera y público | Marcado como inferencia si no viene medido |
| 9 | CTA y gatillo | Modelo de pago, envío, CTA, `{PRECIO_X}` |
| 10 | Compliance | Qué no se afirma, de `politicas-y-promesas.md` |

## 2. Ficha de pieza

```
<código> · <formato> · <etapa> · ángulo "<nombre>" (<nivel>)
Por qué: <la razón, atada a una cita del estudio o al hueco de la matriz de referencias>
Texto literal (se copia carácter por carácter):
  TITULAR: "<...>"
  APOYO: "<...>"
  CALLOUTS: "<...>", "<...>"
  SELLO: "<pago y envío del país>"
  CTA del anuncio (va fuera de la imagen): "<...>"
Jerarquía: 1º <...> · 2º <...> · 3º <...> · 4º <...>
Arte: <fondo, paleta, tipografía, luz> · <lo que NO lleva, en positivo cuando se pueda>
Producto: foto_real = <ruta o URL> · conservar forma, color, etiqueta y escala sin cambios
Destino: <pauta | whatsapp> · <4:5 a 1080×1350 (o 1440×1800) | 1:1 a 1080×1080>
Motor: golden-imagen-arena (o golden-ecom-magic con awareness_level=<nivel>)
Prompt: [bloque de código completo, ver prompts-de-imagen.md]
```

Ejemplo resuelto (combo del taller, Guatemala; los textos son del documento de Kevin):

```
B2 · Oferta apilada · BOFU · ángulo "El set completo" (product_aware)
Por qué: el mercado vende un 2×1 del mismo brazalete; el combo de dos piezas distintas es el hueco
Texto literal:
  TITULAR: "2 piezas, 1 solo pedido"
  APOYO: "Pulsera Pixiu + Anillo de Monedas"
  SELLO: "{PRECIO_COMBO} · Pago contra entrega · Envío a todo Guatemala"
  CTA del anuncio: "Quiero mi set"
Jerarquía: 1º precio grande · 2º piezas apiladas con "+" · 3º titular arriba · 4º sello abajo
Arte: fondo navy profundo, dorado y cian en el sello, luz cálida; producto grande y protagonista
Producto: foto_real = fotos/pulsera-limpia.jpg + fotos/anillo.jpg
Destino: pauta · 4:5 a 1080×1350
```

El ejemplo muestra la forma, no la regla: los colores, el país y los textos salen de cada producto.

## 3. El archivo matriz.json

Se guarda en `PROYECTOS/<PRODUCTO>/DESPLIEGUE/matriz.json` y lo lee `scripts/validar_matriz.py`.

```json
{
  "producto": "nombre exacto del producto",
  "nombre_corto": ["cada nombre con que se lo menciona en un titular", "en un combo, el de cada pieza"],
  "empresa": "la empresa dueña del canal",
  "canal": "la tienda o canal que vende",
  "pais": "CO",
  "pago": "contraentrega | anticipado | ambos",
  "vertical": "belleza | salud | esoterico | hogar | moda | tecnologia | mascotas | otro",
  "estudio": "ruta al 00-ESTUDIO (relativa a la matriz o a PROYECTOS/)",
  "cuenta": {"publicos": true},
  "angulos": [
    {"id": "A1", "nombre": "...", "nivel": "unaware", "patron": "disruptivo",
     "origen": "estudio | derivado", "cita": "cita textual + fuente + likes", "disruptivo": true}
  ],
  "piezas": [
    {"id": "P1", "angulo": "A1", "etapa": "TOFU | MOFU | BOFU", "formato": "...",
     "titular": "...", "apoyo": "...", "callouts": "...", "sello": "...", "cta": "...",
     "precio_en_imagen": false, "destino": "pauta | whatsapp | organico | landing | ficha",
     "relacion": "4:5 | 1:1", "foto_real": "ruta o URL | PENDIENTE", "generar": true, "persona": false,
     "estado": "PENDIENTE: requiere públicos (solo si la cuenta no los tiene)",
     "resena_fuente": "de dónde sale la reseña (solo si la pieza muestra estrellas o testimonio)",
     "prompt": "el prompt completo, con el titular literal adentro"}
  ],
  "plan": {"edad_minima": 18, "conjuntos": [{"nombre": "...", "piezas": ["P1", "P2"]}]},
  "entrega": "el texto de la entrega al usuario"
}
```

Reglas de forma (si fallan, el validador sale con **exit 2** y no corre las casillas): la raíz es un
objeto; `angulos` y `piezas` son listas; cada ángulo y cada pieza tienen `id` de texto;
`producto`, `empresa`, `canal`, `pais`, `pago`, `vertical` y `estudio` son texto; `disruptivo`,
`generar`, `persona` y `precio_en_imagen` son `true` o `false`, nunca `"false"` entre comillas.

## 4. Las 25 casillas del validador

Todas las listas de palabras se comparan **normalizadas** (sin tildes, sin mayúsculas, por palabra
completa), y las casillas de texto miran **todos** los campos: titular, apoyo, callouts, sello, CTA y,
donde aplica, el prompt.

| # | Falla si |
|---|---|
| 01 | `pago`, `vertical`, `nivel`, `etapa`, `destino` o `relacion` está fuera de su vocabulario cerrado |
| 02 | La tanda no tiene de 2 a 3 ángulos (una matriz vacía falla aquí) |
| 03 | Un ángulo no tiene su TOFU, su MOFU y su BOFU |
| 04 | No hay ángulo de nivel 1 o 2, o no hay ninguno disruptivo |
| 05 | Un ángulo no trae cita (o la cita es de relleno: "N/A", "pendiente") o no tiene nombre |
| 06 | El estudio no existe en disco |
| 07 | Falta empresa o canal |
| 08 | Una pieza TOFU trae precio, en cualquier campo o en el prompt |
| 09 | Una pieza TOFU nombra el producto (completo o corto) en la imagen, o lleva un llamado de compra |
| 10 | Una pieza BOFU no lleva el sello del modelo de pago dentro de la imagen |
| 11 | Hay un precio escrito como número ("$89.900", "89900 pesos", "89 mil", "89,900", "Q199" en GT) |
| 12 | Una pieza para generar no tiene ruta o URL de foto real |
| 13 | Una pieza sin titular, o un prompt que no lleva el titular literal |
| 14 | Antes/después o con/sin, diseño infantil, o claims listados en negativo en el prompt |
| 15 | Signos de apertura en cualquier texto o prompt |
| 16 | Una pieza con precio va a orgánico, landing o ficha |
| 17 | `{RESEÑA_REAL}` sin reemplazar en una pieza para generar, o estrellas sin `resena_fuente` |
| 18 | Un teléfono, correo o cuenta publicitaria en el texto o el prompt |
| 19 | Cuenta sin públicos y una pieza MOFU o BOFU sin `estado` "PENDIENTE: requiere públicos" |
| 20 | Una pieza apunta a un ángulo que no existe |
| 21 | El mismo titular en dos piezas |
| 22 | Dos ángulos usan el mismo formato en la misma etapa (misma plantilla = un solo anuncio para Meta) |
| 23 | No hay plan, un conjunto tiene más de 3 piezas, nombra una pieza que no existe o deja piezas fuera |
| 24 | Belleza o salud sin ninguna pieza con persona, o sin `edad_minima` de 18 |
| 25 | "Quedó perfecto", "todo bien", "está listo", "listo para lanzar" o "debería funcionar", con cualquier tilde o mayúscula |

**Lo que no distingue:** cifras que no son precio se reconocen por su unidad ("2.000 años", "4.000
mAh", "3 capas"); una cifra suelta sin unidad ni moneda junto a "precio", "desde" o "solo" se trata
como precio. Si el validador marca algo que no es precio, se escribe la unidad, no se apaga la casilla.

## 5. Revisión visual (lo que el script no ve)

Después de cada render, quien ejecuta revisa y escribe lo que vio, no un "OK":
1. Nombre del producto legible, de frente y completo.
2. Escala real contra la mano o la persona.
3. Recorte limpio, sin halo.
4. Texto leído letra por letra contra el texto literal, con acentos y ñ. Si el motor los rompe, la
   imagen se genera sin texto y el texto se monta encima.
5. Sin antes/después: se tapa media imagen y, si la otra mitad pierde el sentido, es antes/después.
6. Lo importante fuera de la zona segura (ver `formatos-de-estatico.md`).
