# Horizon y bloques de nueva generación

> Reference original de golden-shopify. Explica la arquitectura "block-based" del tema
> Horizon (Shopify, nueva generación) y cómo aprovecharla en páginas Golden de alta conversión.
> Base de referencia local: `PROYECTOS/HORIZON-BASE` (42 secciones · 95 bloques · 121 snippets).
> Para la adaptación general entre temas (Shrine→Dawn/Sense/fallback) ver `references/temas.md`;
> este doc cubre SOLO lo específico de Horizon (no lo dupliques con temas.md).

## 🔴 ADVERTENCIA DURA — 3 límites no documentados de Horizon/Pitch (G4.2, chat Insulinum 2026-08-07)

Descubiertos con **3 `FileSaveError` consecutivos en una tienda real** (tema Pitch, familia
Horizon), uno por intento. Ninguno aparece en la documentación oficial. LEER ANTES de tocar
un `product.json` de un tema Horizon:

| # | Límite | Mensaje exacto de Shopify |
|---|---|---|
| 1 | **`product-information` NO acepta bloques ajenos en su primer nivel**: su esquema no declara `@theme`. Aplica a **cualquier** bloque que intentes declararle desde el template, **incluido `custom-liquid`**. | *"Valor no válido para el tipo en el bloque X. El tipo @theme debe estar definido en el esquema para poder aceptar bloques de temas."* |
| 2 | **Los bloques privados del tema** (prefijo `_`, ej. `_product-media-gallery`) **no se pueden declarar desde fuera** (desde el JSON del template). | mismo mensaje, con el nombre del bloque privado |
| 3 | **Cada setting `custom_liquid` tiene tope de 50 KB** (bytes UTF-8). | *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"* |

⚠️ **El límite 3 NO es exclusivo de Pitch/Horizon: aplica a TODOS los temas.** Por eso vive
también como punto 9 del RESUMEN DURO del SKILL.md y como check obligatorio (nro. 21) en
`references/auto-check.md`. Los límites 1 y 2 significan que **en Horizon/Pitch no se pelea
con la sección nativa de producto: se la rodea** — ver la receta probada de abajo.

## 🟠 RECETA PROBADA Horizon/Pitch (G4.2 — funcionó en tienda real, chat Insulinum)

Patrón nuevo, probado, con el que **ninguno de los 3 errores puede darse**:

1. **Plantilla 100% secciones `custom-liquid`, CERO bloques**, sin tocar `product-information`.
   No se declara nada dentro de la sección nativa ni se intenta reutilizar sus bloques privados.
2. **Galería propia en Liquid** leyendo `product.images` (foto grande + miniaturas, con clic,
   teclado y deslizar), porque la galería nativa es un bloque privado (`_product-media-gallery`)
   inalcanzable desde el template.
3. **Rejilla de 2 columnas armada por JS moviendo el DOM** (foto a la izquierda con `sticky` +
   columna de venta al lado), con **re-armado en el evento `shopify:section:load`** para que no
   se descuadre mientras se edita en el editor de temas.
4. **UNA sección por pieza** — respeta la REGLA #5 (todo apagable con el "ojo" del editor) *y*
   esquiva el tope de 50 KB por setting. El límite terminó empujando hacia la arquitectura
   correcta: piezas chicas, independientes y togglables.
5. **Fallback del CTA** (regla permanente en TODA página, no solo Horizon — ver REGLA #2 del
   SKILL.md y `references/releasit-cod.md`): si Releasit no está en la página, el botón espera
   ~1,5 s por si la app inyecta tarde y luego cae al formulario nativo `/cart/add`. Antes, sin
   Releasit, el botón no hacía nada.
6. **Product JSON-LD propio**: al no usar la sección nativa se pierde el schema de producto que
   ponía el tema. Hay que reponerlo a mano (sección de schema propia, invisible — mismo criterio
   que `sec-seo-aio-schema`).

**Regla de conducta que acompaña la receta:** nunca adivinar la estructura interna del `main`
de un tema ajeno (costó dos ciclos de error en tienda real). Dos caminos, no tres: **(1)** pedir
el `templates/product.json` REAL de la tienda, o **(2)** ir 100% `custom-liquid` y no depender
del tema. Jamás reconstruir de memoria la estructura nativa (emparenta con la regla de estado
vivo: leer del servidor, nunca de un respaldo).

---

## 1. Qué cambia con Horizon

- Es **100% block-based**: casi todo es un **theme block** reutilizable, no markup fijo dentro de la sección.
- Las secciones declaran qué bloques aceptan en su schema; los merchants **anidan** bloques (varios niveles).
- Texto siempre por **claves de traducción** (`t:...`) → multi-idioma desde el día 1.
- Incluye **generador de bloques con IA** en el editor (describes el bloque y lo crea).
- Mantiene foco en **velocidad** (es la evolución de Dawn).

## 2. Cómo se declaran los bloques en una sección

En el `{% schema %}` de la sección, el array `blocks` admite:

```json
"blocks": [
  { "type": "@theme" },   // acepta CUALQUIER theme block del tema
  { "type": "@app" },     // acepta bloques de apps
  { "type": "text" },     // o tipos específicos por nombre
  { "type": "button" }
]
```

- `"@theme"` = libertad total: el merchant mete cualquier bloque del tema dentro de la sección.
- Bloques propios viven en `/blocks/_nombre.liquid` (prefijo `_`), cada uno con su `{% schema %}`.
- Un bloque puede **anidar** otros bloques (definidos en `blocks` + `block_order` dentro de `presets`).

## 3. Anatomía de un theme block

```liquid
{% assign block_settings = block.settings %}
<div class="mi-bloque" {{ block.shopify_attributes }}>
  ...HTML usando block_settings...
</div>
{% schema %}
{
  "name": "t:names.mi_bloque",
  "settings": [ /* ... */ ],
  "presets": [
    {
      "name": "t:names.mi_bloque",
      "blocks": { "text-1": { "type": "text", "settings": { ... } } },
      "block_order": ["text-1"]
    }
  ]
}
{% endschema %}
```

- `{{ block.shopify_attributes }}` es **obligatorio** en el nodo raíz (lo necesita el editor).
- `presets` con bloques anidados por defecto = el merchant lo arrastra y ya viene armado.
- Usa `t:` para nombres y textos por defecto.

## 4. Cómo lo aprovecha Golden (alta conversión COD)

- **Para tiendas en Dawn/Shrine/Sense:** seguimos con bloques `custom_liquid` portables (no cambia el flujo).
- **Para tiendas nuevas o que migren a Horizon:** podemos entregar piezas como **theme blocks nativos**
  (mejor integración con el editor + generador IA), respetando los mismos componentes de conversión
  Golden (ticker, garantía, barra logística, countdown, FAQ, manifiesto, prueba social, sticky CTA).
- **Reaprovecha la librería local** `HORIZON-BASE/blocks` y `/snippets` como punto de partida
  (carrusel, acordeón, card, etc.) y encima aplica la capa Golden (paleta, copy COD, Releasit).
- Mantén SIEMPRE los estándares de `references/estandares-liquid.md` (accesible, rápido, BEM, tokens).

## 5. Cuándo usar Horizon vs el flujo clásico

| Situación | Recomendación |
|---|---|
| Tienda existente en Dawn/Shrine/Sense | Bloques `custom_liquid` Golden (no migrar por migrar) |
| Tienda nueva, quiere lo más moderno | Base Horizon + theme blocks Golden |
| Merchant que editará mucho solo | Horizon (editor + generador IA de bloques) |
| Máxima portabilidad entre temas | `custom_liquid` (independiente del tema) |

## 6. Nota de licencia (importante)

- Horizon es de Shopify, gratis y open-source para **construir tiendas**.
- Temas **derivados** de Horizon NO son elegibles para vender en la Shopify Theme Store
  (no afecta a Golden: montamos tiendas para vender productos, no para revender temas).
- No redistribuir el código de Horizon como si fuera propio; usarlo como base/referencia.
