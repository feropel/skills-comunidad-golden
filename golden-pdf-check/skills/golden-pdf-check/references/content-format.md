# Formato de contenido · Markdown-Golden

`build_pdf.py` acepta un Markdown ligero con una idea central: **todo lo
que la comunidad debe copiar y pegar va dentro de una tarjeta de prompt**,
y esas tarjetas nunca se parten entre páginas.

## Front matter (portada)

```
---
kicker: Comunidad Golden
title: 50 Prompts para vender por WhatsApp
subtitle: Copia, pega y adapta. Sin vueltas.
author: Golden Group
date: Julio 2026
---
```

Todos los campos son opcionales; si falta `title` se usa "Documento".

## DOS tipos de documento (leer ANTES de escribir el Markdown)

La skill maqueta bien lo que le entregas, pero **no puede arreglar contenido
escrito en el formato equivocado**. Un documento de 53 páginas pasó la auditoría
técnica entera — marca, márgenes, cortes, colores — y FER lo rechazó al leerlo:
*"no se entiende, no tiene un mapa para entender el paso a paso, toca uno
adivinar"*. Eran notas telegráficas volcadas tal cual. El auditor mide
estructura; la comprensión no la mide nadie salvo quien escribe.

| | **Entregable de prompts** | **Informe o bitácora narrativa** |
|---|---|---|
| Para qué | copiar y pegar | leer de corrido |
| Bullets | bien: son la unidad | mal: fragmentan el hilo |
| Cuerpo | tarjetas atómicas | **párrafos en prosa** que explican |
| Autonomía | cada prompt se usa solo | **cada sección se entiende sola**, sin haber leído las anteriores ni haber estado ahí |
| Apertura | el índice basta | además, un párrafo de **"qué es este documento y cómo leerlo"** |

Regla práctica para el segundo tipo: si una sección son cinco bullets de tres
palabras, no está lista — eso son *tus* notas, no un documento que otro pueda
leer. Reescríbela en prosa antes de construir el PDF. La skill no te lo va a
avisar porque no puede distinguir un bullet legítimo de una nota cruda, y un
detector heurístico de eso daría más falsos positivos que ayuda.

## Página de CONTENIDO (automática · norma FER v5.4)

**No la escribas.** `build_pdf.py` la genera sola justo después de la portada, leyendo los `##` y
`###` del documento y contando las tarjetas copiables de cada sección. Consecuencia práctica: los
encabezados son el índice, así que escríbelos **descriptivos y en orden de ejecución**
(`### Copy 7 · Bloque de honestidad`, `### Prompt 3 · IMG-03 Comparativa de ahorro`).
Se apaga solo con `--no-index`, y solo para documentos de una sola pieza.

**Números de página (v5.15).** El índice trae el número REAL de cada sección,
medido sobre el PDF ya construido en una segunda pasada (y repetida hasta que
converge, porque añadir los números puede empujar el índice a otra hoja y correr
todo el cuerpo). Sin números, un índice de 130 líneas no es un mapa: el lector ve
los títulos y no puede ir a ninguno. Si no se pueden localizar, el índice sale sin
números y el script avisa — nunca con números inventados.

## COMPONENTES VISUALES (v6.0) — usa estos antes que un párrafo con cifras

Un informe con datos en prosa se lee como un muro. Los mismos datos en una barra
o una escala se entienden de un vistazo. **Si estás escribiendo números en un
párrafo, casi siempre hay un componente mejor.**

    ::: kpi
    Pedidos entregados | 1.847 | +18% vs julio | bien
    Devoluciones       | 214   | 11,6% del total | mal
    :::

`etiqueta | valor | nota | tono` — el tono (`bien`/`mal`) solo colorea la nota.
Úsalo cuando el dato ES el titular: a veces la respuesta no es un gráfico.

    ::: barras Entregas al primer intento
    unidad | %
    Envía | 92
    TCC   | 58
    :::

    ::: escala Meta trimestral
    actual: 4820
    meta: 6000
    unidad: pedidos
    :::

    ::: comparativa Antes y después del cambio
    unidad | %
    Cali | 61 | 88
    :::

    ::: pasos Cómo se decide una transportadora
    Revisar la cola | Todos los pedidos pendientes del día.
    Validar dirección | Si falta el barrio, se pregunta antes.
    :::

    ::: qr
    https://comunidadgolden.com | Escanea para ver el tablero
    :::

**Los enlaces normales de Markdown ya quedan CLICABLES en el PDF** — verificado:
`[texto](https://…)` produce una anotación de enlace real, no texto azul.

### Las reglas del dibujo, y por qué

La paleta se validó con el script de la skill `dataviz` (los seis checks: banda
de luminosidad, croma, separación para daltonismo, visión normal y contraste).
**La primera candidata fue RECHAZADA** — tres colores leían gris y olivo/terracota
eran indistinguibles para deuteranopía. No se eligen colores a ojo.

Y una diferencia del medio que endurece el método: `dataviz` asume pantalla, con
hover, tooltip y vista de tabla. **Un PDF impreso no tiene nada de eso**, así que
aquí las etiquetas directas no son opcionales: cada dato lleva su número visible,
y ninguna serie se distingue solo por color.

## IDENTIDAD POR CHAT (v6.0)

Cada PDF puede salir con la marca del chat que lo emite. No es un color suelto:
es voz, kicker, autor, pie, logo y paleta declarados juntos.

    $PY scripts/build_pdf.py informe.md salida.pdf --tema comunidad-golden
    $PY scripts/build_pdf.py informe.md salida.pdf --tema cartel-del-chat

Las identidades viven en `assets/temas/<id>.json`. Para crear una nueva, copia
una y cambia sus valores — **incluida `--s1..--s6`, y re-corre el validador**:
el orden importa, porque mide pares adyacentes.

| Identidad | Marca | Cuándo |
|---|---|---|
| `comunidad-golden` | Comunidad Golden, dorado | entregables de la comunidad, PDFs de prompts |
| `cartel-del-chat` | El Cartel del Chat, violeta | material donde FER va como Fer, sin Golden Group |

## Bloques

| Escribes | Se convierte en |
|---|---|
| `## Texto` / `### Texto` | Encabezado de sección |
| Texto normal | Párrafo (soporta `**negrita**`, `*cursiva*`, `` `código` ``, `[link](url)`) |
| `- item` / `1. item` | Lista |
| `---` | Separador |
| ` ``` ` … ` ``` ` | **Tarjeta de prompt** monoespaciada (atómica, copiable) |
| `::: prompt Título` … `:::` | **Tarjeta de prompt** en prosa (atómica, copiable) |
| `::: nombre Título` … `:::` | **Bloque con estilo** atómico (destacado, aviso, ficha de datos) |
| `![Pie](ruta/img.svg)` | **Figura** atómica: imagen + pie numerado, nunca se parten |

### Figuras (v5.6)

Una línea sola con `![Pie de figura](ruta/imagen.svg)` se convierte en una figura:
la imagen se **incrusta en base64** (el PDF queda autocontenido), el pie se
numera solo (`Figura 1`, `Figura 2`…) y la imagen **nunca se separa de su pie**
ni se parte entre páginas.

- La ruta se resuelve **contra la carpeta del `.md`**, no contra el directorio
  desde el que corres el script.
- Formatos: `.svg` `.png` `.jpg` `.gif` `.webp`. **Prefiere SVG**: se incrusta
  como vector, se ve nítido a cualquier zoom y pesa una fracción del PNG.
- Ancho opcional entre llaves: `![Pie](img/pantalla.svg){60%}`. Sin él, la figura
  usa el ancho disponible y se limita sola para caber en una página.
- Las figuras **no cuentan** como textos copiables en la página de CONTENIDO:
  ese número es solo de prompts.
- Si la ruta no existe, el script avisa por stderr y deja el hueco visible — no
  falla en silencio.

### Tarjeta de prompt monoespaciada

El texto tras los backticks de apertura se usa como título de la tarjeta:

    ``` Prompt de bienvenida
    Actúa como asesor de ventas de mi tienda. Saluda al cliente por su
    nombre, pregunta qué busca y ofrece 2 opciones con precio.
    ```

### Bloque con estilo (v5.7)

Cualquier nombre que no sea `prompt` produce un contenedor atómico con clase
propia — `::: nota` → `<div class="block nota">`. Sirve para que un documento
largo respire: destacados, avisos, fichas de datos.

    ::: nota Antes de empezar
    Ten a la mano el **catálogo** y los precios actualizados.
    Sin eso, el resto del módulo no se puede completar.
    :::

Diferencia clave con la tarjeta de prompt: **el contenido de adentro SÍ se
procesa como Markdown** (negritas, listas, tablas). Por eso no sirve para texto
copiable literal — para eso están las tarjetas. El bloque nunca se parte entre
páginas. Es neutro por defecto; un tema (`--css`) le puede dar color a la clase
que use.

### Tarjeta de prompt en prosa

    ::: prompt Guion de objeción de precio
    Cuando el cliente diga que está caro, valida su preocupación,
    recuerda el beneficio principal y ofrece el pago contra entrega.
    :::

## Reglas de oro

- **Un prompt = una tarjeta = una página como máximo.** Si un prompt es
  larguísimo, el auto-fit reduce el tipo para que quepa entero. Si aun al
  mínimo no cabe, se escala. Nunca se corta.
- Si un prompt es tan largo que al reducirse queda incómodo de leer,
  conviene **partirlo en dos prompts** con títulos "Parte 1 / Parte 2".
  Esa decisión es de contenido, no de maquetación.
- No metas capturas de pantalla dentro de una tarjeta de prompt: rompen
  el copiar-pegar. Ponlas como imagen aparte.
- **Líneas de tarjeta ≤ 76 caracteres (regla de redacción, v5.8 · chat dental
  Chile 2026-08-07).** Dentro de una tarjeta monoespaciada, una línea de más de
  ~76 caracteres se ENVUELVE al renderizar y la compuerta verbatim la reporta
  como "espaciado/orden alterado" (pasó con dos prompts de imagen; se resolvió
  reescribiéndolos a 72-84 caracteres por línea). `build_pdf.py` ahora AVISA
  antes de renderizar, con la tarjeta y la línea exactas — el arreglo correcto
  es reescribir el contenido con saltos de línea propios, nunca confiar en el
  envoltorio del render.
