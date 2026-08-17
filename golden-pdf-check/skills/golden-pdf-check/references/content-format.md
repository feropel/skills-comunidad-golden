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

## Página de CONTENIDO (automática · norma FER v5.4)

**No la escribas.** `build_pdf.py` la genera sola justo después de la portada, leyendo los `##` y
`###` del documento y contando las tarjetas copiables de cada sección. Consecuencia práctica: los
encabezados son el índice, así que escríbelos **descriptivos y en orden de ejecución**
(`### Copy 7 · Bloque de honestidad`, `### Prompt 3 · IMG-03 Comparativa de ahorro`).
Se apaga solo con `--no-index`, y solo para documentos de una sola pieza.

## Bloques

| Escribes | Se convierte en |
|---|---|
| `## Texto` / `### Texto` | Encabezado de sección |
| Texto normal | Párrafo (soporta `**negrita**`, `*cursiva*`, `` `código` ``, `[link](url)`) |
| `- item` / `1. item` | Lista |
| `---` | Separador |
| ` ``` ` … ` ``` ` | **Tarjeta de prompt** monoespaciada (atómica, copiable) |
| `::: prompt Título` … `:::` | **Tarjeta de prompt** en prosa (atómica, copiable) |
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
