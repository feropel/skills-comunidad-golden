# Cumplimiento: claims, imágenes y citas

Lee este archivo en el **Paso 2** (para calificar la seguridad de claims del tema) y otra vez en el
**Paso 4** antes de escribir. Aplica a Colombia; si el ebook es para otro país, verifica su norma en
vivo y dilo en el informe.

## El ebook es publicidad, aunque no nombre el producto

En Colombia el anunciante responde por la publicidad engañosa (Ley 1480, art. 30), y lo que la
empresa le entrega al cliente junto con su pedido es comunicación de la marca. Si un capítulo dice
que algo "causa X" y el cierre dice que el producto "ayuda con X", **el conjunto se lee como una
proclama**, aunque ninguna frase suelta lo diga.

## Cosméticos (el caso más común en Golden)

- La Decisión 833 de la CAN, vigente en Colombia vía INVIMA, prohíbe que un cosmético declare
  indicaciones terapéuticas (art. 3) y que su publicidad le atribuya propiedades que excedan la
  función cosmética (art. 48).
  [normograma.invima.gov.co](https://normograma.invima.gov.co/compilacion/docs/decision_comisioncandina_dec833.htm)
- El INVIMA hoy no autoriza previamente la publicidad de cosméticos, pero prohíbe las proclamas
  curativas y **las bondades que no estén notificadas en la NSO** (verificar en vivo, las reglas
  cambian). [invima.gov.co](https://www.invima.gov.co/cosmeticos-aseo-plaguicidas/preguntas-frecuentes)

Traducido al ebook:

| Sí | No |
|---|---|
| "cubre al instante", "se ve", "aporta volumen visual" (lo que el producto hace a la vista) | "hace crecer", "cura", "trata", "detiene la caída", "regenera" |
| "los dermatólogos recomiendan X hábito" | "este producto hace lo que recomiendan los dermatólogos" |
| "si notas X, consulta a un dermatólogo" | "con este producto ya no necesitas al dermatólogo" |
| un aviso al final que dice qué es y qué no es el producto | letra chica que contradice lo que dice el texto |

**Suplementos, alimentos y dispositivos** tienen normas propias (no verificadas en esta skill). Si el
producto no es cosmético ni artículo general, busca la norma vigente antes del Paso 4 y declara en
el informe qué revisaste.

## Qué se puede decir del producto, y dónde

El producto aparece en la carta y en el cierre, y ahí **solo se dice de él lo que está en los
claims permitidos de su ficha, con esas palabras**. Un efecto cosmético visual permitido ("cubre al
instante las zonas ralas") no es una proclama: es lo que el producto hace a la vista. Lo que queda
prohibido es el efecto que la ficha no permite y el puente terapéutico entre un problema descrito
en un capítulo y el producto como su solución.

El verificador vigila esos campos, y toda frase del libro que nombre el producto o diga "este
producto" o "nuestro producto", con una regla más dura: ahí cualquier verbo de efecto ("recupera",
"soluciona", "protege", "repara", "mejora", "previene", "combate", "garantiza") y cualquier promesa
sobre el agua ("agua potable", "agua pura") es FALLA en C7, porque junto al producto se lee como
promesa. Lejos del producto, "un derecho garantizado" o "parece un milagro" no son proclamas; el
adjetivo ("remedio milagroso", "resultados garantizados") sí lo es en cualquier parte.

## De dónde salen los claims prohibidos

En este orden: `PRODUCTO.json` (`claims.prohibidos`), el dossier de `golden-investigacion-mercado`,
el cerebro de marca. Cópialos a `producto.claims_prohibidos` del `ebook.json`: el verificador los
busca en todo el texto (C7), en TODAS sus apariciones, junto con una lista de proclamas genéricas.

**Alcance declarado de C7:** la lista genérica cubre proclamas curativas, absolutas ("garantizado",
"100 % efectivo", "milagroso") y las más comunes de cosméticos, suplementos y bienestar
("adelgaza", "quema grasa", "desintoxica"). No conoce todas las categorías: la lista del producto es
la que hace el trabajo fino, por eso no puede quedar vacía. Y ningún detector de palabras ve una
proclama implícita armada entre dos capítulos: esa revisión es tuya, leyendo el cierre contra los
capítulos. Si el producto no trae la lista, escríbela tú a partir de su categoría y dilo en el
informe.

**El verificador acusa la frase prohibida aunque sea para desmentirla fuera de un bloque de mito.**
Medido en el primer ebook real: la carta de bienvenida citaba el mito "afeitarse hace crecer el pelo"
y cayó en C7. La salida correcta no fue silenciar el chequeo sino reescribir la frase ("afeitarse
vuelve el pelo más grueso"). Para desmentir una creencia con sus palabras, usa el bloque `mito`,
que el verificador sabe leer.

## Aviso obligatorio

Todo ebook de salud, belleza o bienestar lleva en `aviso` una frase que diga que es informativo, que
no reemplaza al profesional y qué es exactamente el producto. Ejemplo:

> Este libro es de carácter informativo y educativo. No reemplaza la consulta, el diagnóstico ni el
> tratamiento de un médico dermatólogo. [Producto] es un producto cosmético de efecto visual
> inmediato: no trata, no cura ni previene [condición].

La contraportada añade sola la nota de uso de IA (Google pide transparencia en temas de salud:
[developers.google.com](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)).

## Imágenes

Por defecto la portada es **arte vectorial generado por el motor**: cero costo, cero riesgo de
derechos. Si se quiere foto:

| Fuente | Uso comercial | Cuidado |
|---|---|---|
| Unsplash | sí, sin atribución | no revender la imagen sin cambios |
| Pexels | sí, sin atribución | **no insinuar que la persona de la foto respalda el producto** |
| Wikimedia Commons | según la licencia de CADA archivo | CC BY-SA exige autor, licencia y compartir igual |
| Motores de IA (Higgsfield, Gemini) | según el motor | cuesta créditos: **di el costo antes** y pide el sí |

Nunca uses fotos de personas reales con un "antes y después" ni la foto de un cliente sin su permiso.
La foto del producto, si aparece, es la foto REAL, nunca redibujada por IA.

## Citas textuales

La Ley 23 de 1982 (art. 31) permite citar pasajes necesarios con el nombre del autor y el título de
la obra, sin que la suma equivalga a reproducir la obra. En la práctica de la skill: **una cita
textual por capítulo como máximo**, corta, con autor y con su número de fuente. Todo lo demás se
cuenta con tus palabras.
