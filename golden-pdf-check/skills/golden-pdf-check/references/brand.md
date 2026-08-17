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
- Original naranja de comunidad: `PROYECTOS/SKOOL/logo-comunidad-golden.svg`.
  Si algún día se cambia la identidad, se ajustan `golden-brand.json`,
  `golden-print.css` y `logo-golden.svg`.

## Geometría

- Página A4, márgenes 15mm, pie reservado 16mm.
- Radio de tarjetas 14–16px.
- Numeración en el pie: "Comunidad Golden … Página X de Y".
