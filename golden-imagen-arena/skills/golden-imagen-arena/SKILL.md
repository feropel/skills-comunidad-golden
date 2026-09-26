---
name: golden-imagen-arena
description: >-
  Golden Group — ARENA DE IMÁGENES por API. Genera la MISMA pieza de ecommerce en VARIOS
  motores de IA a la vez (Nano Banana Pro y 2, OpenAI Hazel, GPT Image 2, Seedream 5 Pro,
  FLUX.2, Recraft, DTC Ads con brand kit) por el MCP de Higgsfield, con la FOTO REAL del
  producto como referencia, las descarga, las optimiza a WebP en la medida de su DESTINO
  (galería de ficha 2048, descripción y pauta 1080) sin deformar el producto, y las CALIFICA
  con una rúbrica de conversión para decir cuál ganó y por qué. Sin navegador y sin
  arrastrar archivos: la foto entra por URL (CDN de Shopify) o por subida directa desde el
  Mac. Úsala SIEMPRE que el usuario quiera: comparar modelos de imagen, "cuál IA hace mejor
  esta imagen", "genérame esta imagen en varios modelos", "hazlo automático por API",
  "prueba nano banana", "cuál motor uso para este producto", generar creativos o infografías
  de producto sin navegador, o producir el paquete visual de una ficha Shopify de forma
  desatendida. Dispara aunque no nombren un modelo.
---

**Fábrica:** chat «✅ SKILL golden-imagen-arena»
<!-- skill v1.18 · 2026-09-20 (auditoría golden-skill-auditor) · agregada la declaración de conexión con el Centro de Mando en el propio SKILL.md (antes solo vivía en references/changelog.md y references/prompt-maestro.md; la regla de la casa exige que el archivo que se activa en cada corrida cargue el dato, no solo el histórico). Sin cambios funcionales. -->
<!-- skill v1.17 · 2026-09-08 (fábrica golden-imagen-arena, cierre del ciclo) · añadida la sección "Lo que NO está verificado", forma tomada de golden-ads / golden-copywriting / golden-chatea-pro-config-ventas-wp: las seis reservas tipo (B) vivían en el informe del chat y no en la skill, que es el mismo defecto que esta skill le achaca a los demás · y su propio modo de fallo cerrado por estructura (aviso del CdM): una sección de reservas VACÍA es peor que ninguna porque parece que alguien miró, así que CADA reserva nombra QUIÉN la cierra — una que no puede nombrar a su cerrador o ya está cerrada o nadie la pensó. Ver v1.16 para los tres defectos medidos del ciclo. Historial completo: references/changelog.md. Cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO. -->
# golden-imagen-arena — Varias IAs compiten, una gana


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

## 🔴 REGLA DURA — EL TAMAÑO DE SUBIDA ES UN TECHO PERMANENTE (medido 2026-09-08)

**Shopify REDUCE al servir, pero NUNCA AGRANDA.** Medido contra el CDN real con una imagen de
600 px de la tienda: `?width=400` devolvió 400; `?width=1024`, `2048` y `4000` devolvieron los
600 originales, sin error y sin aviso. **Subir la galería a 1080 condena el zoom de esa ficha a
1080 para siempre**, y no se arregla con un parámetro: se arregla volviendo a subir.

Por eso **el tamaño se decide POR DESTINO, nunca con una cifra única**:

| Destino | Medida | Peso | Por qué |
|---|---|---|---|
| **Galería de ficha Shopify** | **2048×2048** | ~300 KB | Es el techo de zoom. El CDN ya sirve la variante liviana al móvil |
| **Infografía de la descripción** | 1080×1350 | **< 150 KB** | Va al HTML **sin transformación**: aquí el peso sí lo paga el comprador |
| Pauta | según la red | < 150 KB | `references/formato-por-destino.md` |

Esta skill arrastró durante meses la regla plana *"1080 y < 150 KB para todo"*. **Una sola cifra
para todo optimiza el caso equivocado** y le ponía techo de nitidez a todas las fichas de la casa.

⚠️ **Y el reverso, que es la misma trampa disfrazada de solución: agrandar no es subir de
resolución.** Si el motor entregó 1K y tú pides `galeria-shopify`, sale un archivo de 2048 con
1024 de detalle real: el fichero dice 2K y el zoom sigue siendo de 1K, pero ahora nadie vuelve a
mirarlo porque el número ya se ve bien. El script lo delata con un aviso 🔴 AGRANDADO; cuando
salte, **regenera en 2K desde el motor** (`resolution` 2k), no lo estires aquí.

## 🔴 REGLA DURA — NO SE DEFORMA EL PRODUCTO NI AL ENTREGARLO (medido 2026-09-08)

La Ley 1 descalifica una pieza por envase deformado. **El script de entrega de esta misma skill
lo deformaba un 20%**: `optimizar-webp.py` estiraba hasta la medida pedida sin mirar la
proporción de origen. Control conocido (círculo perfecto 1024×1024 → 1080×1350): salió óvalo de
relación **0,800**. Como los motores entregan 1:1 o 2K cuadrado y la ficha pide 4:5, **el caso
deformado era el caso normal**: el jurado castigaba al motor por lo que hacía el script.

Ya no puede pasar — el script escala conservando proporción y recorta (`cover`) o rellena
(`contain`). **Compruébalo antes de confiar en él:** `optimizar-webp.py --autoprueba` (6 casos,
muerde el estirón conocido y calla ante los buenos).

## 🔴 LEY DEL INSTRUMENTO — esta skill COMPARA, así que se audita a sí misma primero

**Cuando dos mediciones discrepan, se audita el INSTRUMENTO antes que el resultado**, y se busca
un control con resultado conocido. Sin control no es una medición, es una lectura.

No es teoría: en la vuelta del 08-sep esta skill traía **dos cifras para una sola corrida de
rembg** (0,63 s en `motores.md`, 0,86 s en el propio script, mismo día y mismo packshot), y un
chat hermano reportó "rembg no está instalado" porque buscó en el Python del sistema y no en el
venv aislado. Ninguno de los dos hallazgos era sobre rembg: los dos eran sobre el instrumento.

Aplícalo también al jurado: si un motor puntúa raro, mira primero si la pieza pasó por un paso
tuyo que la alteró.

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
   sola tanda antes de gastar el primer crédito. Si la alineación va a incluir `ms_image`
   (DTC Ads), el `style_id` se pide en esa MISMA tanda, no al llegar al paso 3: es un dato
   que solo decide el dueño de la marca (ver `models_explore {action:"list", type:"image_style"}`
   en `references/motores.md`) y goteado a mitad de la arena rompe la regla de intake único.
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
4. DESCARGA    → jobs_wait hasta completed → curl de los resultados + WebP en la medida
                 de SU DESTINO (galería 2048 · HTML y pauta 1080), sin deformar
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

**En el mismo preflight se fijan el DESTINO, la RELACIÓN DE ASPECTO y la RESOLUCIÓN**, porque
regenerar en otra medida cuesta una arena entera. Pregunta a dónde va la pieza y saca las tres
de `references/formato-por-destino.md`: galería de ficha 1:1 **en 2K**, infografía de
descripción 4:5 en 1K, feed de Instagram 4:5, reel o TikTok 9:16, LinkedIn 1:1. Si no te lo
dicen, el default de Golden es **4:5 en 1K**.

**El destino no es un detalle de entrega, es una decisión de generación:** si la pieza va a
galería y la sacas en 1K, el techo de zoom de esa ficha queda clavado en 1K para siempre.

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

Formatos Golden: `aspect_ratio "1:1"` para carrusel y galería, `"4:5"` para secciones e
infografías. `count` de 1 por motor en la primera ronda: la diversidad la da la arena, no las
variantes del mismo modelo.

🔴 **Si la pieza va a la GALERÍA de una ficha, genera en 2K desde el motor** (`resolution` 2k
en los que lo aceptan: Nano Banana Pro/2, GPT Image 2, Seedream, FLUX.2, Recraft). Sale más
barato que descubrir después que la galería quedó con techo de 1080, porque **eso solo se
arregla regenerando**: el CDN de Shopify reduce pero nunca agranda. Para infografía de
descripción y para pauta, 1K basta y sobra.

### 4. Descargar y optimizar

`generate_image` es **asíncrono**: devuelve un job, no la imagen. **No existe un tool
`job_status`** (verificado contra el schema vivo del MCP el 2026-08-24; los motores tardan
de segundos a un par de minutos). Para esperar los resultados de la tanda usa
`jobs_wait` con los ids de los jobs (espera bloqueante), o consulta uno puntual con
`job_display {job_id}` / navega el historial con `show_generations`. Si un job sale
`failed` o lo frena moderación, no tumba la arena: reintenta ese motor UNA vez y,
si repite, se declara fuera de competencia y el ranking sigue con los demás —
anota el motivo en el informe.

Con los jobs completados llegan las URLs de resultado. Bájalas con `curl` y
conviértelas con `scripts/optimizar-webp.py`, que acepta dimensión rectangular:

```bash
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py entrada.png salida.webp 1080x1350 150
```

El tercer argumento es el **DESTINO por su nombre**, no una cifra suelta: el script ya trae la
medida y el peso de cada uno (`galeria-shopify` 2048/300 KB · `ficha-html` 1080×1350/150 KB ·
`ig-feed` · `ig-reel` · `cuadrado` · `youtube` · `pinterest`). La tabla vive en
`references/formato-por-destino.md`.

**El script no deforma**: escala conservando proporción y recorta por el centro (`cover`, el
default, correcto para packshot centrado) o rellena el borde (`--modo contain`, cuando recortar
se comería producto o texto). Si dudas de él, córrele `--autoprueba` antes de entregar.

Si hay que llevar una pieza YA hecha a otro formato manda esa misma tabla: recortar es gratis y
`outpaint_image` cuesta créditos, y para VIDEO `reframe` no soporta 4:5 ni 2:3.

Guarda todo en `PROYECTOS/<PRODUCTO>/IMAGENES/` con el naming de Golden:
`PRODUCTO - Contexto NN.webp` (ej. `TAG RECEDE - Hero nanobananapro 01.webp`). Jamás
`1.jpg`. **El peso meta lo pone el destino, no una cifra única:** ~300 KB la galería de ficha
(donde manda la nitidez, porque el CDN nunca agranda), < 150 KB lo que va al HTML y a pauta.

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

**Definición de "terminado"** (checklist antes de entregar):
- [ ] Cada pieza pasó la regla dura de dato-duro-en-imagen (texto verificado letra por letra).
- [ ] Ninguna pieza ganadora está descalificada por la rúbrica (producto adulterado, botón
  falso, WhatsApp incrustado, claim inventado, texto ilegible).
- [ ] Cada WebP salió en la medida de SU destino (galería 2048 · descripción y pauta 1080), no
      todos con la misma cifra, y lleva el naming `PRODUCTO - Contexto NN.webp`.
- [ ] Ninguna pieza salió deformada: si el motor entregó una proporción distinta a la del
      destino, se recortó o se rellenó — nunca se estiró. Ante la duda, `--autoprueba`.
- [ ] El motor default del producto quedó fijado y anotado para la próxima ronda.
- [ ] El reporte final trae piezas, ganador, pesos, créditos gastados y saldo restante.
Si falta cualquier casilla, la arena no está lista para pasar a `golden-shopify` / `golden-ads`.

## Lo que NO está verificado en esta skill

Forma tomada de `golden-ads`, `golden-copywriting` y `golden-chatea-pro-config-ventas-wp`, que
ya la usaban (barrido del CdM, 2026-09-08). **Va aquí y no en un informe** porque una reserva que
vive solo en la memoria de un chat no es un guardarraíl, es un recuerdo.

🔴 **Regla de esta sección, porque tiene su propio modo de fallo: una sección de reservas VACÍA
es peor que ninguna, porque parece que alguien miró.** Para que no pueda vaciarse en silencio,
**cada reserva nombra QUIÉN la cierra** — un hecho externo concreto, no una intención. Una
reserva que no puede nombrar a su cerrador no es una reserva: o ya está cerrada y sobra, o nadie
la ha pensado. Y si algún día esta sección dice *"todo revisado"* sin nombrar el instrumento con
el que se revisó, **está mintiendo**: bórrala y vuelve a llenarla midiendo.

Si trabajas con esta skill, esto es lo que todavía no puedes dar por bueno:

- **La arena completa no se ha corrido de punta a punta desde el 2026-09-08.** Lo verificado esa
  fecha fue la mitad de ENTREGA (scripts, medidas, CDN); el preflight, la subida de la foto y los
  motores en paralelo **no se ejecutaron** porque el MCP de Higgsfield no estaba conectado. Si
  algo del paso 0 al 3 no cuadra con lo escrito aquí, **gana lo que veas en vivo**.
  → **LO CIERRA:** el MCP de Higgsfield conectado y una corrida real con un producto.
- **El 2048 de galería nunca se ha subido a una ficha real.** Está medido que Shopify **nunca
  agranda** — de ahí sale la regla —, pero **no** que subir 2048 mejore el zoom que percibe el
  comprador.
  → **LO CIERRA:** `golden-shopify`, que es quien sube, contra una ficha viva.
- **`outpaint_image` sigue sin costo conocido.** Exige un `image_id` real ya confirmado y no
  acepta estimación en seco. No lo ofrezcas con una cifra.
  → **LO CIERRA:** una corrida sobre una pieza de verdad.
- **El saldo de créditos escrito en los references está CADUCADO** (223,5 el 30-ago) y otros
  chats gastan de la misma cuenta. **Nunca lo cites.**
  → **LO CIERRA:** `balance`, en cada preflight. Este caduca solo: no lo escribas fijo.
- **Las zonas seguras por red** (cuánto tapa la interfaz de TikTok o Instagram) no están
  verificadas. Lo que hay es una regla provisional, no un número.
  → **LO CIERRA:** la documentación oficial de cada plataforma.
- **El catálogo de motores se verificó el 2026-07-21** y cambia sin aviso.
  → **LO CIERRA:** `models_explore`, que manda sobre `references/motores.md` ante cualquier duda.

**Lo que sí está verificado y con qué:** el techo de nitidez, contra el CDN en vivo con imagen
real de la tienda · la no-deformación y el aviso de agrandado, contra `--autoprueba` de 6 casos
que muerde los dos casos malos y calla ante los buenos · la instalación de rembg, abriendo el
venv. Todo lo demás de este archivo es doctrina acumulada, no medición de hoy.

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
- `references/vocabulario-foto.md` — **cómo pedir la foto por su nombre técnico.** Frase en
  español a la izquierda, token exacto a la derecha (lente, luz con ángulo y ratio, superficie,
  ángulo de cámara). Ábrelo SIEMPRE que el encargo llegue vago y devuelve 3 opciones concretas.
- `references/motores-y-plan-b.md` — **cuándo NO usar esta arena** (Ecom Magic hace anuncio sobre
  plantilla, sección de landing, logística por país y la calculadora COD gratis), los **4 motores
  pagados que el MCP no lista** (Veo 3.1 entre ellos) y el **plan B por API directa** si el MCP cae.
- `references/prompt-maestro.md` — plantilla del prompt de ecom y cómo escribir el texto
  que va dentro de la imagen. Léelo antes de generar.
- `references/formato-por-destino.md` — **la tabla que manda: en qué medida y con qué peso sale
  cada pieza según su DESTINO** (galería de ficha, infografía de descripción, cada red), la
  medición del techo de nitidez contra el CDN de Shopify, cuándo recortar gratis y cuándo pagar
  por rellenar, qué formatos NO cubre `reframe` en video, y el costo medido del reencuadre.
  **Léelo en el preflight**, antes de disparar la arena: aquí el destino decide la generación.
- `references/rubrica.md` — rúbrica de conversión para calificar y rankear. Léelo antes de
  dar el veredicto.
- `scripts/optimizar-webp.py` — lleva la pieza a la medida de su DESTINO por nombre
  (`galeria-shopify`, `ficha-html`, `ig-feed`, `ig-reel`, `cuadrado`, `youtube`, `pinterest`)
  **sin deformar nunca**: recorta (`cover`) o rellena (`--modo contain`), y **avisa si tuvo que
  AGRANDAR**, que es el techo de nitidez disfrazado. Trae `--autoprueba` de 6 casos en los dos
  sentidos.
- `scripts/componer.py` — pega los PNG reales del producto sobre la placa generada por IA,
  con sombra y posicionamiento relativo. Es la pieza clave del método definitivo (paso 1.5).
- `scripts/quitar-fondo.py` — recorta el fondo EN LOCAL con rembg, sin gastar créditos.
  Alternativa gratis a `remove_background` del MCP para lotes de packshots de frasco, caja
  o producto sólido (para pelo, humo o cristal sigue ganando el modelo del MCP). Detalle en
  `references/motores.md`, sección "Utilidades de post".

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera).

⚠️ **Es una CITA HISTÓRICA, no la norma vigente.** Dice *"las optimiza a WebP < 150 KB"*, que es
justo la regla plana derogada el 2026-09-08 por el techo de nitidez: hoy manda el tamaño POR
DESTINO (galería 2048, HTML y pauta 1080). Se conserva solo por sus **fronteras** — el reparto
con `golden-ecom-magic`, `golden-ugc-avatar` y `golden-shopify` —, que siguen vigentes.

> Golden Group — ARENA DE IMÁGENES por API. Genera la MISMA pieza de ecommerce en VARIOS motores de IA a la vez (Nano Banana Pro, Nano Banana 2, OpenAI Hazel, GPT Image 2, Seedream 5 Pro, FLUX.2, Recraft, DTC Ads con brand kit) a través del MCP de Higgsfield, con la FOTO REAL del producto como referencia, las descarga, las optimiza a WebP < 150 KB y las CALIFICA con una rúbrica de conversión para decir cuál ganó y por qué. Sin navegador, sin arrastrar archivos: la foto entra por URL (CDN de Shopify) o por subida directa desde el Mac. Úsala SIEMPRE que el usuario quiera: comparar modelos de imagen, "cuál IA hace mejor esta imagen", "genérame esta imagen en varios modelos", "hazlo automático por API", "prueba nano banana", "cuál motor uso para este producto", generar creativos/infografías de producto sin navegador, o producir el paquete visual de una ficha Shopify de forma desatendida. Dispara aunque no nombren un modelo: basta con "imágenes de producto automáticas / por API / comparando IAs". Si golden-ecom-magic está instalada, esa es la productora por defecto con un solo motor y plantillas; esta manda cuando hay que COMPARAR motores o producir por API sin navegador. NO usar para avatares UGC o video (eso es golden-ugc-avatar), ni para montar la página (golden-shopify).

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-imagen-arena
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-imagen-arena
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

El script de entrega se comprueba solo, y hay que correrlo cuando se toque:
```bash
python3 ~/.claude/skills/golden-imagen-arena/scripts/optimizar-webp.py --autoprueba
```
6 casos **en los dos sentidos**: debe MORDER el estirón conocido (relación 0,800) y CALLAR ante
cover, contain y el destino de galería. Un banco que solo prueba el lado bueno no prueba nada —
esta skill vivió meses con un script que deformaba el producto y nada mordió.

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-imagen-arena`

Historial completo en `references/changelog.md`.
