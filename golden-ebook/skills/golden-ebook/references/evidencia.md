# De dónde sale cada decisión de la skill

Lee este archivo cuando alguien pregunte **por qué** la skill hace algo como lo hace, o antes de
cambiar un número (tamaño de página, letra, peso, largo). Cada fila dice si la decisión está
**medida**, viene de una **norma**, de un **blog** o de un **cálculo propio**. Investigación hecha
el 2026-09-17: las cifras de plataformas cambian, así que lo marcado "verificar en vivo" se vuelve
a comprobar antes de citarlo a un tercero.

## Formato y lectura en el celular

| Decisión | Base | Tipo |
|---|---|---|
| Página 108 x 192 mm (proporción 9:16, "una pantalla por página") | NN/g documenta que el PDF en celular obliga a "pellizcar, ampliar y entrecerrar los ojos"; una página del tamaño de la pantalla elimina el zoom. [nngroup.com/articles/pdf-unfit-for-human-consumption](https://www.nngroup.com/articles/pdf-unfit-for-human-consumption/) | medido (NN/g, 2020) + diseño propio |
| Cuerpo de 13 pt = 16,6 px a 390 px de ancho | Apple usa 17 pt de cuerpo en iOS. Cálculo: 13 pt = 4,59 mm; 4,59 / 108 x 390 = 16,6 px. El verificador exige 16 px o más (P4). | norma de plataforma + cálculo |
| Interlineado de 1,55 | WCAG 2.2, criterio 1.4.12, pide que el texto soporte interlineado de 1,5. [w3.org/WAI/WCAG22/Understanding/text-spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) | norma |
| Contraste de texto de 4,5:1 o más | WCAG 2.2, criterio 1.4.3 (C13) | norma |
| Peso de 5 MB o menos (aviso), 15 MB tope (falla) | WhatsApp acepta documentos grandes (la API de la nube topa en 100 MB, verificar en vivo), pero el cliente abre el archivo con datos móviles. 5 MB es criterio propio. | norma de plataforma + criterio |
| Portada legible a 600 px | WhatsApp muestra la página 1 como miniatura del documento; el ancho aproximado de 600 px sale de un reporte técnico y conviene confirmarlo enviando un PDF real. P7 mide título (24 px) y empresa (12 px); P13 exige un logo de 24 mm o más, porque con 17 mm la palabra "ENTERPRISE" del logo no se leía | blog técnico + medido, verificar en vivo |
| 2.500 a 7.000 palabras, 4 a 9 capítulos | Rango de blogs de herramientas (2.000 a 5.000 palabras, 10 a 25 páginas); **no se encontró el estudio original**. Se deja ancho y como aviso, no como falla. | blog, sin verificar |

## Por qué un ebook en la ventana de envío

| Hecho | Fuente | Tipo |
|---|---|---|
| En contra entrega el rechazo crece con los días de espera: 22 % si se entrega en 1 a 2 días, 35 % si pasan más de 5 (India, año fiscal 2025) | ShipNotes de Shipway, citado por Amazon Shipping India: [shipping.amazon.in/blog/what-is-rto-how-to-reduce-return-to-origin](https://shipping.amazon.in/blog/what-is-rto-how-to-reduce-return-to-origin) | medido, otro país |
| En Colombia no hay una tasa de rechazo publicada por un gremio o por Dropi; los blogs de transportadoras hablan de 10 a 30 % | [blog.envioclick.com](https://blog.envioclick.com/pago-contra-entrega-en-colombia-por-que-cada-rechazo-te-cuesta-mas-de-lo-que-ganaste/) | blog |
| **No existe un estudio que mida el efecto de un contenido de valor sobre el rechazo.** | búsqueda del 2026-09-17 | hueco declarado |
| En Colombia, en ventas a distancia hay 5 días hábiles de retracto contados desde la entrega (Ley 1480, art. 47) | [consumoteca.com.co/articulo-47-de-la-ley-1480](https://www.consumoteca.com.co/articulo-47-de-la-ley-1480-estatuto-del-consumidor/) | norma |

Consecuencia: la skill **no promete** que el ebook baje el rechazo. Propone medirlo (ver
`entrega.md`, "Cómo saber si funciona").

## Narrativa

| Hecho | Fuente | Tipo |
|---|---|---|
| La curiosidad nace de la brecha entre lo que uno sabe y lo que quiere saber | Loewenstein (1994), *Psychological Bulletin* 116(1), desarrollado en Golman y Loewenstein (2014): [cmu.edu/dietrich/sds/docs/golman/golman_loewenstein_curiosity.pdf](https://www.cmu.edu/dietrich/sds/docs/golman/golman_loewenstein_curiosity.pdf) | académico |
| "Efecto avestruz": se evita la información sobre lo que desagrada, por eso el tema va con valencia positiva | mismo trabajo de 2014 | académico |
| Capítulos cortos y un "pruébalo hoy" por capítulo | práctica editorial, **sin dato medido** | criterio |

## Render

| Hecho | Fuente | Tipo |
|---|---|---|
| Chromium numera páginas en los márgenes (`@bottom-right`) y respeta páginas con nombre (`page:`) | Chrome 131 lo anunció; **probado en este Mac** con Chromium 151 el 2026-09-17 | probado en vivo |
| Chromium arma los marcadores del PDF comiéndose el espacio donde el título salta de línea ("tecontó") | medido en el primer ebook real; por eso el motor los arma desde el JSON (P11) | probado en vivo |
| `@page { background }` pinta el margen de cada página en Chromium 151 (antes salía blanco alrededor del fondo crema) | probado en este Mac el 2026-09-18 | probado en vivo |
| Chromium no hace índice con número de página ni notas al pie; WeasyPrint sí | documentación de Chrome y de WeasyPrint; Paged.js está congelado en npm desde 2024 | documentación |
| Fuentes estáticas, nunca variables | golden-pdf-check midió que Chrome convierte las variables en Type 3 y rompe el copiar y pegar; P10 lo vigila | probado en vivo (skill hermana) |
