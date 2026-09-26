# Escritura y esquema del ebook.json

Lee este archivo en el **Paso 4**, antes de escribir la primera línea. Aquí están la estructura, la
voz, los bloques disponibles y el esquema exacto que lee el motor.

## Estructura fija del libro

El motor arma siempre este orden; tú solo llenas el contenido.

| Página | Sale de | Para qué |
|---|---|---|
| Portada | `meta`, `portada`, `marca` | se ve como miniatura en WhatsApp: título, empresa y logo |
| Carta de bienvenida | `bienvenida` | "tu pedido va en camino y esto es para el viaje"; única mención natural del producto al inicio |
| En este libro | `capitulos[].titulo` | la lista de capítulos, con enlace a cada uno |
| Apertura de cada capítulo | `titulo` + `gancho` | página llena de color con el número grande |
| Cuerpo de cada capítulo | `bloques` + `cierre` | el contenido |
| Para cerrar | `cierre` | recapitula y conecta con el producto; botón a la tienda o al WhatsApp |
| Fuentes | `fuentes` | lista numerada con enlaces que se pueden tocar |
| Contraportada | `marca`, `aviso` | logo, empresa, web, aviso legal y nota de uso de IA |

## Medidas (formato móvil)

| Pieza | Medida | Por qué |
|---|---|---|
| Libro completo | 2.500 a 7.000 palabras, 4 a 9 capítulos | 11 a 30 minutos de lectura a 230 palabras por minuto (C12, C1) |
| Carta de bienvenida | 90 palabras o menos | es una sola página; más, desborda (C16) |
| Cierre | 80 palabras o menos | una sola página con su botón (C16) |
| Gancho de capítulo | 1 a 2 frases, 35 palabras máximo | va en la página de apertura |
| Capítulo | 250 a 1.000 palabras | 2 a 7 pantallas (C23) |
| Párrafo | 3 a 5 líneas en pantalla, unas 60 palabras | en celular un párrafo largo parece un muro |
| Título del libro | 3 a 8 palabras, 45 caracteres o menos | legible en la miniatura (C22 mide el largo; P7, el tamaño de la letra) |

En formato `a5` (tableta o impresión) caben más palabras por página: los topes de carta y cierre
suben a 170 y 150.

## Voz

- Toma la voz del cerebro de marca si existe (`BRAND-BRAINS/<MARCA>/marca.md`). Si no, la de
  Golden: cercana, directa, tuteo, español latinoamericano natural, cero relleno.
- **El ebook es un documento: va con ortografía completa, incluidos los signos de apertura ¿ y ¡.**
  Es la regla de FER por canal: sin signos de apertura cuando se simula a una persona escribiendo
  (chat, WhatsApp, anuncios); con ellos en documentos y presentaciones. El verificador lo exige (C9).
  Los mensajes de entrega por WhatsApp de `entrega.md` van al revés: sin signos de apertura.
- Nada de líneas de rayas separadoras (C10).
- Lenguaje de empresa, no de tienda: "nuestro equipo", "la empresa", no "la tiendita". El botón
  final tampoco dice "tienda": "Conocer más de nuestra empresa".
- Habla del lector ("tu pelo", "tu casa"), no del producto.

## Anatomía de un capítulo

1. **Gancho** (en la apertura): una pregunta implícita o un dato que sorprende. Abre una brecha
   de curiosidad que el capítulo cierra.
2. **Primer párrafo**: entra con una escena o una creencia común, no con una definición.
3. **Cuerpo**: 2 a 4 ideas, cada una con su dato y su fuente. Alterna párrafo con un bloque visual
   (dato, mito, lista) cada 2 o 3 párrafos: en celular el ojo necesita dónde descansar.
4. **Pruébalo hoy**: uno por capítulo, de 2 a 6 acciones concretas que el lector puede hacer esta
   semana, sin comprar nada (C24).
5. **Cierre**: una frase que abre la pregunta del capítulo siguiente. El motor la pega al último
   bloque para que nunca quede sola en una página.

Ejemplo de gancho flojo contra gancho que funciona:

| Flojo | Funciona |
|---|---|
| "En este capítulo hablaremos del estrés y el cabello." | "¿Te ha pasado que un día empiezas a ver más pelo en la ducha y no entiendes por qué? La respuesta casi nunca está en lo que pasó esa semana." |

## Marcado dentro del texto

| Escribes | Sale |
|---|---|
| `**palabra**` | negrita |
| `*palabra*` | cursiva |
| `[3]` o `[1, 4]` | número de fuente, que enlaza a la lista del final |
| una línea en blanco (`\n\n`) | párrafo nuevo |

## Bloques disponibles

| `tipo` | Campos | Úsalo para |
|---|---|---|
| `parrafo` | `texto` | el cuerpo |
| `subtitulo` | `texto` | dividir un capítulo largo |
| `dato` | `cifra`, `texto`, `fuente` (obligatoria) | una cifra que merece ser titular |
| `mito` | `mito`, `realidad`, `fuente` (obligatoria) | desmontar una creencia; el mito sale tachado |
| `cita` | `texto`, `autor` | una frase textual corta, con autor y número de fuente |
| `lista` | `titulo` (opcional), `items` | pasos, señales, causas |
| `prueba_hoy` | `titulo`, `items` | las acciones del final del capítulo (salen con casillas) |
| `nota` | `titulo`, `texto` | un recuadro de contexto o de matiz |
| `imagen` | `ruta`, `pie`, `credito` | una imagen con licencia verificada (ver `cumplimiento.md`) |

## Esquema completo

```json
{
  "meta": {"titulo": "", "subtitulo": "", "anio": 2026, "idioma": "es-CO",
           "formato": "movil", "palabras_clave": []},
  "marca": {"nombre": "", "logo": "ruta/relativa/al/json.png", "web": "",
            "colores": {"primario": "#", "acento": "#", "acento_texto": "#",
                        "fondo": "#", "texto": "#"},
            "fuente_de_verdad": "de qué archivo salieron nombre, logo y colores"},
  "producto": {"nombre": "", "alias": [], "claims_prohibidos": []},
  "tema": {"titulo_tema": "", "familia": "", "puente": ""},
  "portada": {"kicker": "", "imagen": "opcional", "credito_imagen": "opcional"},
  "bienvenida": {"kicker": "Antes de empezar", "titulo": "", "texto": "", "firma": ""},
  "capitulos": [{"titulo": "", "gancho": "", "bloques": [], "cierre": ""}],
  "cierre": {"kicker": "Para cerrar", "titulo": "", "texto": "",
             "cta": {"texto": "", "url": "https://"}},
  "fuentes": [{"id": 1, "titulo": "", "editor": "", "anio": 2026, "url": "https://",
               "nivel": "A", "consultado": "AAAA-MM-DD",
               "nivel_porque": "solo si es nivel A y el dominio no es .gov, .edu, .int ni doi.org"}],
  "aviso": "",
  "nota_ia": "opcional: reemplaza la nota de uso de IA por defecto"
}
```

Colores:

- `primario` es el fondo de portada, aperturas, recuadros "Pruébalo hoy" y contraportada.
- `acento` es el color gráfico: filetes, números grandes sobre fondo oscuro, botón.
- `acento_texto` es el acento que se LEE sobre el fondo claro. Muchos acentos de marca (dorados,
  amarillos) no llegan a 4,5:1 sobre fondo claro; la marca suele tener un tono oscuro del mismo
  color. Si no lo trae, el verificador lo acusa (C13) y le propones a la marca un tono medido.

La muestra completa y válida está en `assets/muestra/ebook.json`: cópiala como punto de partida.
