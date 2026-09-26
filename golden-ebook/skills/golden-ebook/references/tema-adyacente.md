# Cómo elegir el tema adyacente

Lee este archivo en el **Paso 2**, antes de investigar. Aquí está la decisión que más pesa en la
calidad del ebook: un tema bien elegido se lee entero; uno flojo se abre y se olvida.

## La regla de fondo

**El ebook no habla del producto. Habla de la vida de quien lo compró.**
El producto aparece en la carta de bienvenida y en el cierre. Dentro de los capítulos lo esperado
es cero menciones; el verificador (C11) avisa desde la tercera, contando también "este producto" o
"nuestro producto", y falla desde la quinta.

El porqué: el cliente ya compró. Lo que hay que sostener entre la guía generada y la entrega no es
el deseo de comprar, sino la **confianza en haber comprado bien** y las ganas de recibirlo. Un
catálogo disfrazado de libro se nota en la página dos y quema esa confianza. Un libro que le enseña
algo que no sabía, sobre algo que le importa, hace que la marca parezca un experto y no una tienda.

## Paso a paso

### 1. Lee al comprador, no al producto

Del producto saca cuatro cosas, en este orden de preferencia de fuente: dossier de
`golden-investigacion-mercado` si existe, `PRODUCTO.json` o ficha de la tienda, cerebro de marca,
y por último la foto o el nombre.

| Pregunta | Ejemplo con una fibra capilar |
|---|---|
| Qué TRABAJO le hace el producto (su resultado, no su función) | "que no se me note la zona rala" |
| En qué MOMENTO de su vida lo compra | antes de una cita, un evento, cansado de usar gorra |
| Qué le PREOCUPA de fondo | que lo descubran, perder más pelo, qué es normal |
| Qué CREE saber y probablemente es mito | la gorra deja calvo, afeitarse engrosa el pelo |

### 2. Genera 5 candidatos, uno por familia

Cada candidato sale de una familia distinta, para no quedarte con la primera idea:

| Familia | Qué hace | Ejemplo |
|---|---|---|
| **Mitos contra evidencia** | desmonta creencias de la categoría | "Lo que nadie te contó de tu pelo" |
| **Ciencia curiosa** | explica el porqué de algo cotidiano | "Por qué el sol del trópico quema distinto" |
| **Ritual y maestría** | enseña a sacarle el máximo a la categoría | "El arte de la taza perfecta en casa" |
| **Estilo de vida adyacente** | un tema vecino que el comprador vive | "Dormir mejor en una ciudad que no duerme" |
| **Historia y cultura** | el origen y las anécdotas de la categoría | "Del faraón al barbero: 5.000 años de peinados" |

Ejemplos por vertical, para no fosilizar el caso del cabello:

| Producto | Tema adyacente posible | Familia |
|---|---|---|
| Crema para manchas | "La ciencia del sol a 2.600 metros" | ciencia curiosa |
| Faja postparto | "Los primeros 90 días: lo que nadie te cuenta del posparto" | estilo de vida |
| Cafetera | "De la finca a tu taza: el viaje del café colombiano" | historia y cultura |
| Masajeador de cuello | "El cuello de la pantalla: posturas que cansan y cómo evitarlas" | estilo de vida |
| Perfume capilar | "El olfato y la memoria: por qué un aroma te devuelve a un lugar" | ciencia curiosa |
| Juguete didáctico | "Jugar para aprender: lo que la ciencia sabe de los primeros años" | ciencia curiosa |

### 3. Califica cada candidato de 0 a 3 en seis criterios

| Criterio | 3 puntos cuando... | Peso |
|---|---|---|
| **Curiosidad** | el título abre una pregunta que el lector quiere cerrar | x3 |
| **Relevancia** | le habla a la preocupación de fondo del paso 1 | x3 |
| **Seguridad de claims** | no obliga a prometer lo que el producto no puede (ver `cumplimiento.md`) | x3 |
| **Investigable** | hay fuentes de nivel A accesibles (revistas, entidades médicas u oficiales) | x2 |
| **Puente natural** | el cierre puede mencionar el producto sin forzar | x2 |
| **Valencia positiva** | deja al lector con más control, no con más miedo | x1 |

Puntaje máximo: 42. **Gana el más alto. Si empatan, gana el de mayor seguridad de claims; si
también empatan ahí, el de mayor relevancia.** No se le pregunta al usuario: la regla decide.
Un candidato con 0 en seguridad de claims se descarta aunque sume más: es el que expone a la marca.

La valencia positiva no es adorno: la teoría de la brecha de información (Loewenstein, 1994) explica
por qué una pregunta abierta engancha, y el desarrollo de Golman y Loewenstein (2014) describe el
"efecto avestruz": la gente evita la información sobre lo que le desagrada. Un libro que asusta
sobre la caída del pelo se deja de leer; uno que da criterio se termina. Fuentes en `evidencia.md`.

### 4. Registra la decisión

Escribe en la carpeta del proyecto un `decision-tema.md` con la tabla de los 5 candidatos y sus
puntajes, y copia en `ebook.json` el campo `tema.puente`: una o dos frases que dicen por qué ESTE
tema le sirve a ESTE comprador. Si no puedes escribir el puente en dos frases, el tema no es el
correcto.

**Decide e informa, no preguntes.** En el informe final muestra el ganador y el segundo con sus
puntajes: si el usuario prefiere el segundo, lo dirá, y el cambio cuesta reconstruir, no rehacer.

## Cuándo el usuario ya trae el tema

Úsalo tal cual, pero pásalo igual por la tabla del paso 3. Si su tema saca 0 en seguridad de
claims, díselo con el ejemplo concreto de la frase que obligaría a escribir, y propón el candidato
seguro más cercano.

## Título

- De 3 a 8 palabras y 45 caracteres o menos (C22), porque la portada se ve como miniatura de unos
  600 px en WhatsApp. "Lo que nadie te contó de tu pelo" tiene 8 palabras y 32 caracteres.
- Promete algo que el lector gana (saber, entender, evitar), no algo que el producto hace.
- Formas que funcionan: "Lo que nadie te contó de...", "La ciencia de...", "X mitos de... frente a
  la evidencia", "Guía para...". Evita el signo de pregunta en el título: se corta mal en la miniatura.
