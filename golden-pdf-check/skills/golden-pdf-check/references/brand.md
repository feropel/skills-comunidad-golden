# Identidad · Comunidad Golden (para PDFs)

Fuente de verdad: `PROYECTOS/GASTO-GOLDEN/app/globals.css`. Los valores
están horneados en `assets/golden-brand.json` y `assets/golden-print.css`.

## Marca

- **Dueño / empresa:** Golden Group.
- **Lo que se comparte con la comunidad:** *Comunidad Golden*. Estos PDFs
  son para la comunidad, así que el pie y el kicker dicen "Comunidad Golden"
  y el autor es "Golden Group".

## Paleta (documento claro, premium, imprimible)

| Rol | Hex |
|---|---|
| Fondo página | `#faf9f5` |
| Superficie / tarjeta | `#ffffff` |
| Tinta (texto) | `#17140d` |
| Texto atenuado | `#6b7280` |
| Línea/borde | `#e7e4dc` |
| **Dorado** (acento) | `#b8912a` / `#d4af37` |
| Dorado suave | `#e7c65a` |
| Tinte dorado (fondos) | `#fbf5e2` |
| Sobre dorado (texto) | `#1a1508` |

Gradiente de marca: `linear-gradient(145deg, #f4d67a, #d4af37 55%, #9a7b1e)`.

### Regla de uso del dorado (MEDIDA, no estética)

Los dorados de marca son de **acento**, no de texto. Medido contra el fondo
`#faf9f5`: `#d4af37` da **2.00:1** y `#b8912a` da **2.80:1**. El mínimo WCAG es
4.5:1 para texto y 3.0:1 para elemento gráfico — o sea que ni siquiera llegan al
umbral de gráfico.

| Uso | Color | Por qué |
|---|---|---|
| Filetes, gradientes, bordes, banda de las tarjetas, fondos | `#d4af37` / `#b8912a` | ahí no hay texto que leer: la identidad manda |
| **Texto** dorado sobre fondo claro (kicker, enlaces, índice, títulos de bloque, pie) | `--gold-text: #8a6d1f` (**4.65:1**) | mismo dorado con menos luminosidad: se lee igual de Golden y SÍ se puede leer |
| Texto sobre fondo oscuro | `#d4af37` | sobre el negro de marca `#1a1508` da 8.65:1, sin problema |

Otros tonos verificados por si algún día se quiere más contraste: `#7a5f1a`
(5.73:1), `#6b5215` (7.01:1), `#5c4611` (8.52:1).

Esto **no es opinión de diseño**: la prueba 16 del `autoprueba.py` calcula el
ratio de cada color de texto contra su fondo y falla por debajo de 4.5:1. Si
alguien vuelve a poner un dorado de acento en un color de texto, la autoprueba
lo caza. Origen: fila del chat FILTRO DE HERRAMIENTAS (2026-08-26), método
tomado de la skill `dataviz` — verificar con número, no a ojo.

Se eligió un tema **claro** (no el oscuro del dashboard) porque un PDF que
la gente imprime y del que copia-pega se lee mejor en claro y no desperdicia
tinta. El dorado se mantiene como acento premium.

## Tipografía

- Cuerpo/títulos: **Inter** (incrustada por build_pdf.py como GoldenSans; el
  sans del sistema queda de fallback en el CSS).
- Prompts: **JetBrains Mono** (incrustada como GoldenMono; SF Mono y ui-monospace
  de fallback) para que se vean como algo "para copiar".
- Las fuentes viven en `assets/fonts/` (OFL) y son ESTÁTICAS a propósito — ver
  SKILL.md: las variables corrompen el copy-paste de corchetes.
- Kicker: MAYÚSCULAS, `letter-spacing: 0.14em`, dorado.

## Logo

- Primario horneado: `assets/logo-golden.svg` = **emblema oficial Golden Group
  Community** (círculo dorado/negro con las GG; PNG oficial incrustado en un
  envoltorio SVG, elegido por FER el 2026-07-04).
- El original naranja de comunidad (`PROYECTOS/SKOOL/logo-comunidad-golden.svg`)
  **ya no está en disco**: esa carpeta fue retirada. No queda copia dentro de la
  skill, así que volver al naranja exige re-subir el archivo.
- Si algún día se cambia la identidad, se ajustan `golden-brand.json`,
  `golden-print.css` y `logo-golden.svg`.

## Geometría

- Página A4, márgenes 15mm, pie reservado 16mm.
- Radio de tarjetas 14–16px.
- Numeración en el pie: "Comunidad Golden … Página X de Y".
