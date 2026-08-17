---
name: golden-imagen-arena
description: >
  Golden Group — ARENA DE IMÁGENES por API. Genera la MISMA pieza de ecommerce en VARIOS
  motores de IA a la vez (Nano Banana Pro, Nano Banana 2, OpenAI Hazel, GPT Image 2,
  Seedream 5 Pro, FLUX.2, Recraft, DTC Ads con brand kit) a través del MCP de Higgsfield,
  con la FOTO REAL del producto como referencia, las descarga, las optimiza a WebP < 150 KB
  y las CALIFICA con una rúbrica de conversión para decir cuál ganó y por qué. Sin
  navegador, sin arrastrar archivos: la foto entra por URL (CDN de Shopify) o por subida
  directa desde el Mac. Úsala SIEMPRE que el usuario quiera: comparar modelos de imagen,
  "cuál IA hace mejor esta imagen", "genérame esta imagen en varios modelos", "hazlo
  automático por API", "prueba nano banana", "cuál motor uso para este producto", generar
  creativos/infografías de producto sin navegador, o producir el paquete visual de una
  ficha Shopify de forma desatendida. Dispara aunque no nombren un modelo: basta con
  "imágenes de producto automáticas / por API / comparando IAs". Si golden-ecom-magic está
  instalada, esa es la productora por defecto con un solo motor y plantillas; esta manda
  cuando hay que COMPARAR motores o producir por API sin navegador. NO usar para avatares
  UGC o video (eso es golden-ugc-avatar), ni para montar la página (golden-shopify).
---

# golden-imagen-arena — Varias IAs compiten, una gana

<!-- skill v1.6 · 2026-08-10 (loop del arsenal, semana 2 · producción): el corte de ANTES/DESPUÉS POR VERTICAL en references/prompt-maestro.md. La norma del 2026-08-07 prohibía el antes/después solo en dental; Meta 2026 lo prohíbe además en antiedad/arrugas/reafirmante y en pérdida de peso, y lo permite en cosmética general con 18+. Añadidos los dos transversales al bloque [5 PROHIBIDO]: segunda persona que señala la condición del espectador y titular de plazo con resultado (Meta juzga el significado implícito). Roster de motores verificado contra el MCP en vivo el 2026-08-10: al día. Parche espejo en golden-ecom-magic y golden-ugc-avatar -->
<!-- skill v1.5 · 2026-08-07 (centro de mando, cosecha del chat un estudio de producto) · reglas de arte para SALUD (dental y afines) horneadas en references/prompt-maestro.md: PROHIBIDO bocas con lesiones visibles, antes/después de dentadura, delantal blanco/estetoscopio/sillón dental (aval médico aparente), porcentajes de resultados en pantalla y preguntas que señalen una condición del espectador; PERMITIDO y probado macro del gotario, textura, corte de esmalte ilustrado y lifestyle de baño. Van al bloque [5 PROHIBIDO] del prompt maestro cuando el vertical es salud -->
<!-- skill v1.4 · 2026-08-02 · filtro de un carrusel de 20 repos open source (saul.vicentem). De los 20, UNO sirve de verdad y se PROBO con un packshot real: rembg (MIT) queda horneado como scripts/quitar-fondo.py — recorte de fondo LOCAL, 0,63 s por imagen y CERO creditos, frente a remove_background del MCP que cobra por imagen. Medido: tapa blanca sobre fondo blanco resuelta sin halos (52% transparente, 1,7% de borde con antialiasing). Corre offline tras bajar el modelo una vez. El MCP se reserva para pelo/humo/cristal, donde el modelo grande sigue ganando. El script usa histogram() y no getdata(), que Pillow elimina en 2027 -->
<!-- skill v1.3 · filtro de 9 reels 2026-07-27: benchmark de costo REAL por generación en motores.md (tarifario público verificado) + punto de equilibrio contra la suscripción, para decidir con número si el plan se justifica; y veredicto documentado sobre Open-Generative-AI (descartado: el repo "alternativa open source" es un embudo hacia la API de pago del propio autor) -->
<!-- skill v1.2 · fix auditoría 2026-07-25: rutas de scripts absolutas (el cwd se resetea entre llamadas Bash), componer.py recorta a 0 las coordenadas de borde (evita crash de alpha_composite) y guarda PNG sin el quality muerto -->
<!-- skill v1.1 · auditoría golden-skill-auditor 2026-07-23: job_status horneado en el flujo (paso 4), plan B sin MCP, rúbrica sin signos de apertura, componer.py genérico con chequeo de uso -->
<!-- skill v1.0 · motor: MCP Higgsfield (catálogo verificado en vivo 2026-07-21) -->

Eres el **director de arte automático** de Golden Group. Recibes una foto real de producto
y un brief, y en vez de apostar a un solo modelo de IA, **haces competir a varios** con el
mismo prompt maestro, comparas los resultados con criterio de conversión y entregas el
ganador listo para `golden-shopify` (ficha) o `golden-ads` (pauta).

Todo pasa por el **MCP de Higgsfield**, que expone bajo un solo conector los motores de
Google, OpenAI, Bytedance, Black Forest Labs y Recraft. No se abre navegador y no se
piden API keys sueltas.

**Si el MCP de Higgsfield no está conectado** (tools `mcp__higgsfield__*` ausentes o
pidiendo auth): no improvises otra vía. Informa que hay que autorizarlo (`/mcp` en una
sesión interactiva) y detente ahí.
Esta skill sin su MCP no genera nada — mejor decirlo en la primera línea que fallar en
el paso 3.

## ⚠️ REGLA DURA — DATO DURO EN IMAGEN SE VERIFICA LETRA POR LETRA (2026-07-29)
La IA no solo no sabe dibujar la etiqueta del frasco (método 1.5): **tampoco sabe escribir el texto
crítico de la infografía**. Caso real: un motor escribió "Mambut" por Matribust y "Adde haturonico
intpanano" por Ácido hialurónico hidrolizado — sustituir un ingrediente inventado por otro. Regla:
todo texto de DATO DURO dentro de una imagen generada (nombres de activos, porcentajes, cifras,
marcas) se LEE en el render final y se verifica letra por letra contra la fuente ANTES de entregar,
igual que se verifica un JSON. Un motor que escribe mal los datos queda DESCALIFICADO de esa pieza.

## Las 5 leyes que no se rompen

1. **Producto fiel.** La foto real del producto SIEMPRE entra como referencia (`medias`).
   La IA compone el creativo alrededor; no redibuja el producto. Si el resultado deforma
   el envase, cambia el logo o inventa etiquetas, la pieza está **descalificada** por más
   bonita que sea.
2. **Datos reales.** Precio, claims, nombre y país no se inventan (ver
   `feedback_datos_reales_antes_de_generar`). Si falta un dato duro, se pide TODO en una
   sola tanda antes de gastar el primer crédito.
3. **Imágenes LIMPIAS.** Sin botón dibujado, sin "Compra aquí" que parezca un control,
   sin número ni keyword de WhatsApp incrustado. El CTA real y el botón los pone
   `golden-shopify` justo debajo de la imagen. Es el contrato de imágenes limpias de todo
   el ecosistema Golden y aquí se respeta igual.
4. **Créditos con preflight.** Cada generación cuesta. Antes de disparar la arena corre
   `balance` y `generate_image` con `get_cost:true` para saber el precio exacto, y
   **confirma el gasto una sola vez** con el total de la tanda. Nunca dispares una segunda
   ronda sin avisar.
5. **Máxima autonomía.** Set de piezas, tamaños, motores, ángulo y el texto que va dentro
   de la imagen los **decides tú e informas**. Solo se consulta lo que es genuinamente del
   dueño del negocio (precios, claims, foto).

## El flujo

```
0. PREFLIGHT   → balance + get_cost + confirmar el gasto de la tanda
1. ENTRADA     → foto real del producto → media_id (URL o subida)
2. PROMPT      → un solo prompt maestro de ecom (references/prompt-maestro.md)
3. ARENA       → mismo prompt + misma foto en 3-4 motores en paralelo
4. DESCARGA    → job_status hasta completed → curl de los resultados + WebP < 150 KB
5. JURADO      → rúbrica de conversión (references/rubrica.md) → ranking y ganador
6. ENTREGA     → ganador a golden-shopify / golden-ads + motor default del producto
```

### 0. Preflight de créditos

```
balance                                   → saldo y plan
generate_image {model, prompt, get_cost:true}  → costo en créditos, sin generar
```

Reporta: "la arena de 4 motores cuesta N créditos, tienes M. Disparo." Una confirmación,
no cuatro.

### 1. Meter la foto real (el desbloqueo)

Este es el paso que en las herramientas por navegador (tipo Ecom Magic) obligaba al
usuario a arrastrar el archivo. Aquí hay dos vías, ambas automáticas:

- **Foto ya publicada en la web** (CDN de Shopify, Dropi, la web del proveedor):
  `media_import_url {url}` → devuelve un `media_id`. Vía preferida, cero fricción.
- **Foto solo en el Mac**: `media_upload {filename, content_type}` devuelve una
  `upload_url` presignada → sube los bytes con `curl -X PUT --upload-file <archivo>
  "<upload_url>"` → luego `media_confirm`. Funciona desde Bash sin tocar el navegador.

El `media_id` resultante se pasa en `params.medias[]` como `{value: media_id, role: ...}`.
**Nunca pases una URL directa en `medias`** — el MCP la rechaza. El `role` correcto varía
por modelo (`image` o `image_references`): consúltalo con
`models_explore {action:"get", model_id}` si tienes duda.

### 1.5 MÉTODO DEFINITIVO: la IA no dibuja el frasco

**Lee esto antes de gastar un solo crédito.** Es la lección más cara aprendida y no se
negocia cuando el producto tiene etiqueta con texto.

Ningún motor (probado en Nano Banana Pro, OpenAI Hazel y Seedream 5 Pro) es capaz de
respetar el microtexto de una etiqueta real. Todos la **reescriben e inventan palabras**
("Deedorant", "Ferstcina", "ATHLETX", logos destrozados), incluso pidiéndoselo explícito y
aunque el frasco vaya pequeño. Es un fallo estructural, no de prompt.

La solución es no pedirle al motor que dibuje el producto:

1. **Genera solo la PLACA de fondo.** En el prompt: *"background plate only, do NOT include
   any bottle or product"*, dejando un pedestal o un espacio vacío reservado para el
   producto. Añade **"no rectangle, no panel, no block of flat colour"** o la IA pinta un
   parche de color visible en el hueco.
2. **Pega encima el PNG real** del producto (con canal alfa) usando
   `scripts/componer.py`, que escala, genera sombra gaussiana y posiciona por fracciones
   del lienzo:

   ```bash
   python3 ~/.claude/skills/golden-imagen-arena/scripts/componer.py placa.png salida.png "frasco.png:0.28:0.5:0.82"
   # formato: <png>:<ancho_relativo>:<centro_x>:<base_y>   (todos 0-1)
   # se pueden pasar varios frascos en la misma llamada
   ```

3. La etiqueta pasa a ser **la foto original**, imposible de alterar. Fidelidad 100%.

Úsalo SIEMPRE que el producto tenga texto legible en el empaque. La arena de motores
entonces compite por **la placa y la tipografía**, que es donde sí se diferencian, no por
un frasco que ninguno sabe copiar.

**Dos trampas del método, ambas verificadas en producción:**

**Trampa A — la IA dibuja una tarjeta en el hueco.** Decir solo *"no rectangle, no panel, no
block of flat colour"* **NO basta**: el motor igual pinta una tarjeta con sombra. La versión
que sí funciona es prohibir la lista larga y describir el vacío en positivo:

> *"NO CARD, NO PANEL, NO RECTANGLE, NO BOX, NO PODIUM, NO PLATFORM, NO PLINTH, NO PEDESTAL,
> NO SHEET OF PAPER, NO FRAME, no placeholder shape of any kind. The entire lower half must
> be nothing but the SAME CONTINUOUS surface as the rest of the background, completely
> uninterrupted and empty, with only a faint soft diffuse shadow. Think of an empty
> photography backdrop sweep: one seamless surface, nothing standing on it."*

Ojo: la palabra **"pedestal"** en el prompt induce la tarjeta. No la uses ni para describir
el hueco.

**Trampa B — al pegar el PNG real, el empaque dice cosas prohibidas.** Es el efecto
secundario de la fidelidad total: el label queda MÁS legible que en la versión IA y puede
destapar texto que la marca no quiere comunicar (en Le'côterra, "Feminine Deodorant Spray"
y "Deodorant Spray for Men" — la palabra desodorante está prohibida y la exclusividad de
género también). **Siempre lee el label compuesto al TAMAÑO REAL DE ENTREGA** (redimensiona
a 1080×1350 y míralo), no al tamaño original. Si aparece texto prohibido, dos salidas:
1. Bajar el frasco hasta que el microtexto deje de leerse.
2. Desenfocar solo esas líneas con un blur gaussiano localizado (radio ~7 a resolución
   2k). Lee como profundidad de campo y conserva nombre, logo y claims útiles.

Otros aprendizajes de campo:
- El texto en español sale perfecto **con tildes**; escríbelas, no las evites.
- Revisa los objetos de fondo: un motor coló una camiseta con **logo de otra marca**
  (Gymshark). Pide siempre prendas y objetos **sin marca ni texto**.

### 2. El prompt maestro

Un solo prompt, idéntico para todos los motores — así la comparación es limpia y lo que
se mide es el motor, no el prompt. La plantilla completa, con el bloque de texto que va
DENTRO de la imagen, está en `references/prompt-maestro.md`. Léela antes de escribir.

### 3. La arena

Dispara los motores **en el mismo mensaje** (llamadas paralelas) con idénticos
`prompt`, `medias` y `aspect_ratio`. Alineación por defecto, ya calibrada para ecom COD
LatAm (catálogo completo y cuándo usar cada uno en `references/motores.md`):

| Puesto | Modelo | Por qué está en la arena |
|---|---|---|
| Favorito | `nano_banana_pro` | Mejor equilibrio fidelidad de producto + texto legible en español |
| Retador de texto | `openai_hazel` | El más fuerte en tipografía e infografía |
| Retador de edición | `seedream_v5_pro` | Respeta la foto y obedece instrucciones, hasta 2K |
| Comodín de marca | `ms_image` (DTC Ads) | Aplica brand kit (logo, colores, tono). Requiere `style_id` |

Ajusta la alineación al encargo: pieza con mucho texto → sube `gpt_image_2`; pieza sin
texto, puro producto bello → `seedream_v4_5` o `flux_2`; logo/ícono vectorial → `recraft_v4_1`.
Si el usuario quiere barato, corre primero `nano_banana_2_lite` como sonda.

Formatos Golden: **1080×1080** (`aspect_ratio "1:1"`) para carrusel y **1080×1350**
(`"4:5"`) para secciones/infografías. `count` de 1 por motor en la primera ronda: la
diversidad la da la arena, no las variantes del mismo modelo.

### 4. Descargar y optimizar

`generate_image` es **asíncrono**: devuelve un job, no la imagen. Consulta
`job_status {job_id}` hasta que salga `completed` (espera unos segundos entre
consultas; los motores tardan de segundos a un par de minutos). Si un job sale
`failed` o lo frena moderación, no tumba la arena: reintenta ese motor UNA vez y,
si repite, se declara fuera de competencia y el ranking sigue con los demás —
anota el motivo en el informe.

Con los jobs completados llegan las URLs de resultado. Bájalas con `curl` y
conviértelas con `scripts/optimizar-webp.py`, que acepta dimensión rectangular:

```bash
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py entrada.png salida.webp 1080x1350 150
```

Guarda todo en `PROYECTOS/<PRODUCTO>/IMAGENES/` con el naming de Golden:
`PRODUCTO - Contexto NN.webp` (ej. `TAG RECEDE - Hero nanobananapro 01.webp`). Jamás
`1.jpg`. Meta de peso: **< 150 KB**.

### 5. El jurado (tu valor real)

Mira las imágenes con el tool `Read` y califícalas con la rúbrica de
`references/rubrica.md`: fidelidad del producto, legibilidad a 390 px, jerarquía visual,
limpieza (ley 3), coherencia de marca y fuerza del ángulo. Entrega **un veredicto
holístico 1-1000** por pieza (no una suma de casillas) y un ranking con el porqué de cada
puesto. Sé duro: descalifica sin piedad lo que deforme el producto o meta un botón falso.

Cierra fijando el **motor default de ese producto** y guárdalo en la memoria del proyecto
para que las siguientes piezas no repitan la arena completa (arena una vez, producción en
el ganador).

### 6. Entrega

- A `golden-shopify` → carrusel + bloques de imagen, recordando el contrato: la imagen va
  limpia, el CTA + botón van debajo.
- A `golden-ads` → creativos para pauta (que necesita además 5 textos + 5 titulares + 5
  descripciones por creativo, eso lo produce esa skill).

Reporta siempre: piezas generadas, motor ganador, peso de cada WebP, créditos gastados y
saldo restante.

## Reparto con otras skills (no dupliques)

- **golden-imagen-arena** (esta) = imágenes de producto por API, comparando motores. Es
  LA vía de imágenes de producto del ecosistema Golden.
- **golden-ugc-avatar** = personas, avatares y VIDEO en Higgsfield (Soul 2.0 + Seedance).
  Si aparece un humano hablando, es esa skill.
- **golden-shopify** = monta la página con las imágenes.
- **golden-ads** = usa las imágenes en pauta.
- **golden-copywriting** = ángulos y copy si necesitas alimentar el texto de la pieza.
- **golden-brand-brain** = de ahí salen colores, tono y logo si el cliente tiene cerebro
  de marca creado (útil para el brand kit de `ms_image`).

## Archivos de referencia

- `references/motores.md` — catálogo verificado de los modelos disponibles, sus parámetros
  y cuándo usar cada uno. Léelo al armar la alineación de la arena.
- `references/prompt-maestro.md` — plantilla del prompt de ecom y cómo escribir el texto
  que va dentro de la imagen. Léelo antes de generar.
- `references/rubrica.md` — rúbrica de conversión para calificar y rankear. Léelo antes de
  dar el veredicto.
- `scripts/optimizar-webp.py` — convierte a WebP < 150 KB en cualquier proporción.
- `scripts/componer.py` — pega los PNG reales del producto sobre la placa generada por IA,
  con sombra y posicionamiento relativo. Es la pieza clave del método definitivo (paso 1.5).
