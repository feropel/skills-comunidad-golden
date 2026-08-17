# Orquestación de imágenes — golden-shopify = CEREBRO (G3.12)

golden-shopify **decide** todo el plan visual de la página y **reparte** cada pieza al generador
correcto. No genera imágenes por sí misma: las pide a las skills especializadas con un **BRIEF
VISUAL**. Cada generadora ya sabe CÓMO operar su herramienta; golden-shopify le da el **QUÉ**.

## Reparto de skills (no duplicar)
| Skill | Genera | Herramienta |
|---|---|---|
| **golden-shopify** (esta) | NADA — es el cerebro: plan, formato, TEXTO dentro de cada pieza, y a quién se manda. Monta la página. | — |
| **golden-imagen-arena** | Infografías/creativos con **foto real + texto** (composición, no redibuja) | MCP de Higgsfield por API — varios motores compiten y gana el mejor. SOLO imágenes |
| **golden-ugc-avatar** | **GIF, video, UGC / persona hablando** | Higgsfield (Soul + Seedance) |
| **Nano Banana (Gemini)** | Fotos **photoreal / lifestyle / escenas** cuando no hay plantilla que calce | Gemini `gemini-3-pro-image` (ver `imagenes.md`) |

Regla: si la pieza es **infografía con texto de venta → golden-imagen-arena**. Si es **video/GIF/demo →
Higgsfield**. Si es **foto realista de escena/modelo sin texto → Nano Banana**.

## El contrato: BRIEF VISUAL (cómo se sincronizan las skills)
golden-shopify produce una tabla; cada fila = una pieza. Luego invoca la skill generadora
pasándole SUS filas.

```
| slot        | ubicación   | formato    | generador     | foto fuente | TEXTO dentro de la imagen           | propósito              |
|-------------|-------------|------------|---------------|-------------|-------------------------------------|------------------------|
| gal-1       | galería     | 1080×1080  | imagen-arena  | frasco.jpg  | (foto hero, sin texto)              | gancho de deslizar     |
| gal-2       | galería     | 1080×1080  | imagen-arena  | frasco.jpg  | "ADIÓS VERRUGAS · veneno de abeja"  | beneficio máximo       |
| desc-1      | descripción | 1080×1350  | imagen-arena  | mano.jpg    | "CÓMO ACTÚA · 3 pasos"              | mecanismo (emocionar)  |
| esc-P2      | escalera    | 1080×1080  | nano-banana   | —           | (escena piel limpia, sin texto)     | future-pacing panel    |
| cine-bg     | cine        | 16:9       | higgsfield    | —           | (video 6s piel libre)               | visión emocional       |
```

- El **TEXTO dentro de la imagen** lo escribe golden-shopify (respuesta directa: hook + beneficio),
  con apoyo de `golden-copywriting` si hace falta ángulos.
- Confirmar con el usuario el **set exacto** antes de generar (cada pieza gasta créditos de
  Higgsfield; imagen-arena corre su preflight de costo y confirma el total UNA sola vez).

## Cómo piensa golden-imagen-arena (para NO pedirle imposibles)
golden-imagen-arena **no parte de cero: compone sobre la FOTO REAL** del producto (que entra por
URL del CDN de Shopify o por subida directa desde el Mac) y dispara el MISMO prompt maestro en
varios motores a la vez (Nano Banana Pro, GPT Image 2, Seedream, FLUX.2, Recraft...), califica
los resultados con rúbrica de conversión y entrega la pieza ganadora en WebP < 150 KB.

**SÍ puede (pídele esto):** arquetipos de infografía (**grilla de beneficios, pack de precios,
testimonio, antes/después, cómo actúa, garantía**) · componer sobre 1-3 fotos reales · poner
texto/precio/CTA con la jerarquía que le dictes · qué NO poner · adaptar personajes (nacionalidad/
sexo/edad) · colores (sin amarillo) · **redimensionar (outpaint) · quitar fondo · escalar** una
pieza · re-disparar en otro motor si la estética no convence.

**TAMAÑOS = ILIMITADOS.** Los motores de la arena aceptan el ratio que pidas. 1080×1080 /
1080×1350 son solo el **estándar Golden más usado**, no un tope. Puede hacer el **16:9 del cine**,
verticales, horizontales, el ratio que necesite el slot. **Nunca descartes imagen-arena por tamaño.**

**NO puede (mándalo a otra skill):**
- **Video / GIF** → **golden-ugc-avatar / Higgsfield**.
- Redibujar/reinventar el producto (siempre foto real) · inventar precios/claims.
- La landing en sí NO la genera: la página la construye golden-shopify.

**Cuándo NO es imagen-arena (por PROPÓSITO, no por tamaño):** video/GIF → Higgsfield · foto
photoreal de escena/modelo SIN texto → Nano Banana. Todo lo demás (infografía con foto real +
texto, cualquier tamaño) → golden-imagen-arena.

### Mapeo BRIEF → entradas de golden-imagen-arena (cero conflictos)
| Fila del brief | Entrada en imagen-arena |
|---|---|
| arquetipo / plantilla | arquetipo descrito dentro del **prompt maestro** |
| formato | **tamaño/ratio del job** (preset O personalizado — cualquier ratio) |
| foto fuente | **medias** (URL del CDN de Shopify o subida directa, 1-3 fotos reales) |
| TEXTO dentro + precio + jerarquía + "no poner" + color | **prompt maestro** (texto compuesto + reglas negativas) |
| personaje | prompt maestro (nacionalidad/sexo/edad del personaje) |

Regla: en el brief, las filas `imagen-arena` se describen por **arquetipo + tamaño + texto**. Si la
pieza es video o foto photoreal sin texto, **cambia de generador** — no se lo pidas a la arena.

## Arquitectura visual por ubicación (matriz de formatos)
| Ubicación | Cuántas | Formato | Generador por defecto | Notas |
|---|---|---|---|---|
| **Galería / multimedia** (arriba, junto al carrito) | 4-5 | **1080×1080** (cuadrada) | imagen-arena | foto hero + 3-4 infografías de beneficio. 5+ imágenes ≈ +60% conversión |
| **Descripción** (body_html) | **solo 1-3 CLAVE** | **1080×1350** (vertical IG) | imagen-arena | NO metas 8-12; solo "cómo actúa" / antes-después / lo que una imagen vende mejor que el texto. Alt-text SIEMPRE (SEO) |
| **Escalera** (`P#_IMG`, nuestras secciones) | 3-5 | **1080×1080** (1:1) | imagen-arena o Nano Banana | 1:1 calza al lado del texto en desktop y apila en móvil. URLs NUEVAS, nunca las de la descripción |
| **Cine / visión** (fondo full-bleed) | 1 | **16:9** (o video) | imagen-arena / Nano Banana (estático) · Higgsfield (video) | la arena SÍ hace 16:9 (ratio custom). Escena lifestyle o video corto. Sin texto (el texto es HTML encima) |
| **Bloques nativos entre secciones** | según haga falta | vertical **9:16** / cuadrado | **Higgsfield** (GIF/video) o imagen-arena (estático) | modo de uso GIF, demo, antes-después animado |

## Regla híbrida (hereda de `imagenes.md`)
- **Infografías para EMOCIONAR, bloques nativos para CONVERTIR y posicionar** (SEO, editable, liviano).
- Quedan SIEMPRE como **texto nativo** (no imagen): título, precio, reseñas, FAQ, botón COD.
- **Descripción liviana:** 1-3 infografías; el resto de la historia visual la cargan NUESTRAS secciones
  (escalera, cine, bloques de video). Menos peso, más SEO, edición sin regenerar créditos.
- **WebP < 150 KB**, con width/height + alt (sin CLS). Producto FIEL (foto real, nada de amarillo).

## Cómo se invoca (handoff)
1. golden-shopify arma el **BRIEF VISUAL** (tabla de arriba) con el usuario y confirma el set.
2. Para las filas `imagen-arena` → invocar **golden-imagen-arena** con esas filas (foto real + textos + formato).
3. Para las filas `higgsfield` → invocar **golden-ugc-avatar**.
4. Para las filas `nano-banana` → pipeline de `imagenes.md`.
5. Las imágenes vuelven (WebP <150KB) → golden-shopify las coloca: galería en el multimedia del
   producto (Shopify Files/MCP), descripción en body_html, `P#_IMG`/cine en las secciones.
