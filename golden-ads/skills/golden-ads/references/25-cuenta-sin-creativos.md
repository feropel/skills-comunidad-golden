# 25 · Cuenta publicitaria SIN creativos — meter el medio, analizarlo y escribir el copy que le corresponde

**Orden de FER (2026-09-03):** *"si la cuenta publicitaria no tiene creativos, podamos montarlo,
una vez te lo dé el chat, analices el video y crees los copys que corresponden al video y que sea
coherente"*.

Origen: montando `LECOTERRA - VENTA - OPEN 1` en GOLDEN CP6 COL se reutilizaron videos viejos y
**no se subió material nuevo**. FER lo notó. Este archivo cierra ese hueco.

**La regla que gobierna todo el archivo:** el copy **nace del creativo**, nunca al revés. Un copy
escrito sin haber **visto Y ESCUCHADO** el video es copy inventado, aunque suene bien.

---

## PASO 0 — Medir si la cuenta tiene creativos (no suponerlo)

```
ads_get_ad_videos(ad_account_id)     → videoteca
ads_get_ad_images(ad_account_id)     → banco de imágenes
```

Ambas devuelven **resultados parciales**: sin `video_ids`/`hashes` solo traen `id`+`title` y
`hash`+`name`. Un campo ausente **no significa vacío** — hay que repreguntar por id.

⚠️ **"Cuenta vacía" casi nunca es cierto.** GOLDEN CP6 se creía vacía y su biblioteca ya traía
videos de Toppik y Fibra. Medir antes de pedirle archivos al usuario: quizá ya están.

---

## PASO 1 — Meter el medio en la cuenta · TRES VÍAS, con sus topes MEDIDOS (2026-09-03)

La herramienta vigente es **`ads_creative_upload_media`**. `ads_creative_upload_image` y
`ads_creative_upload_video` están **DEPRECADAS**: no usarlas.

| Vía | Cómo | Lo hace Claude solo? |
|---|---|---|
| **A · URL pública** | `upload_source: URL` + `media_type: IMAGE\|VIDEO` + `media_url` + `name` | **SÍ**, de punta a punta |
| **B · Archivo del Mac** | `upload_source: LOCAL_FILE` | **NO** — abre un selector; **el usuario elige el archivo** |
| **C · Video que ya vive en OTRA cuenta** | referenciar el `video_id` en `ads_create_creative` | **SÍ** — Meta lo copia solo |

**Vía A** sirve con el CDN de Shopify (`cdn.shopify.com/...`), el sitio del cliente o cualquier
enlace directo. **NO sirve** con Google Drive, Dropbox ni Canva cuando piden sesión o devuelven
una página HTML en vez de los bytes.

**Vía B es un tope real, no pereza:** desde el disco del Mac el archivo lo escoge el usuario en el
selector. Decírselo de una, sin prometer que se sube solo.

**Vía C es la que más ahorra:** basta el `video_id` de otra cuenta del mismo BM con la página
compartida; **no hay que resubir nada**. Los thumbnails caducan: sacarlos frescos con
`ads_get_ad_videos(..., fields:["picture"])` sobre la cuenta origen.

Tras subir por A, **releer la biblioteca** y confirmar que el `video_id`/`hash` existe antes de
construir el creativo.

---

## PASO 2 — 🔴 ANALIZAR el creativo ANTES de escribir una sola línea

> ⚡ **Si el encargo viene de `golden360`, el teardown YA ESTÁ HECHO — LÉELO, no lo repitas.**
> Su **Fase 5B** (R2.0, 2026-09-03) pasa cada video por `golden-video-teardown` entre producir los
> creativos y escribir los copys, y llega con **beat sheet segundo a segundo, ángulo, hook y el copy
> quemado en pantalla**. Rehacerlo cuesta tiempo y créditos, y arriesga contradecir el análisis que
> ya guió la producción. Búscalo en el expediente del producto antes de analizar nada; si está, la
> ficha de abajo se rellena con él y se pasa directo al Paso 3.

**Prohibido escribir copy de un video que no se ha escuchado.** Mirar fotogramas no basta: en un
reel hablado los subtítulos quemados salen **una palabra por cuadro** y la lectura visual devuelve
basura (`"Le vas"`, `"para"`, `"diciéndole"`). Medido sobre 9 videos.
Ver `reference_videos_watch_y_transcripcion_local`.

**Herramienta según la profundidad que pida el caso:**

| Necesidad | Herramienta |
|---|---|
| Teardown completo (beat sheet, hook, oferta, riesgo de baneo, fórmula replicable) | skill **`golden-video-teardown`** |
| Cuadros por cambio de escena | skill **`watch`** (`--resolution 1024` si hay texto en pantalla) |
| Voz, en local y gratis | `~/.golden/bin/golden-transcribe <archivo> es` |
| Imagen fija | leerla directamente: qué muestra, producto fiel, texto quemado, gancho visual |

**De cada pieza hay que salir con esta ficha antes de redactar:**

- **Ángulo real** — qué promete el video (no lo que uno querría que prometiera).
- **Hook 0–2 s** — la frase o imagen exacta con la que abre.
- **A quién le habla** — comprador y usuario pueden no ser la misma persona.
- **Qué se ve en pantalla** — producto, demo, testimonio, precio, ciudad.
- **Claims dichos en voz** — precio, duración, garantía, envío. Se citan textual.
- **CTA que ya trae el video** y en qué segundo.
- **Riesgos de política** — atributos personales en 2ª persona, claims médicos, antes/después.

---

## PASO 3 — Escribir los copys PEGADOS a ese creativo

Motor: **`golden-copywriting`** + `golden-copywriting/references/estandar-meta-medido.md`.

Por cada pieza: **5 textos principales + 5 títulos + 5 descripciones**, cargados como
**opciones múltiples del mismo anuncio** (`asset_feed_spec`), no como cinco anuncios.

Largos medidos: **125 / 40 / 25**. Los 125 son la **ventana visible** del texto principal: lo que
va después queda tras "ver más".

⚠️ **Tope del MCP (medido 2026-09-03):** `ads_create_creative` expone `message`, `headline` y
`description` **en singular** — **no expone `asset_feed_spec`**. Por API salen **1+1+1**. Los 15
se cargan en el panel. **Decirlo en el reporte como pendiente**, no callarlo.

**El ángulo es la unidad creativa, no el archivo.** Cinco redacciones del MISMO ángulo son
variaciones; cinco ángulos distintos son cinco creativos (ver `23`).

---

## PASO 4 — PRUEBA DE COHERENCIA (la que pidió FER)

Antes de crear el creativo, cada copy pasa estas seis. **Si una falla, se reescribe.**

1. **Dice lo mismo que el video?** Si el video muestra Bergamot, el copy no habla de Vanilla.
2. **Le habla a quien el video le habla?** Si el video le habla a la mujer sobre su pareja, el
   copy no puede tutear al hombre.
3. **No repite lo que ya dice la imagen o el audio.** El copy **aporta**, no subtitula.
4. **Los datos coinciden** con los del video y con los reales de la tienda: precio, combos,
   duración, envío, garantía. Un precio distinto entre video y copy mata la venta.
5. **Respeta las reglas de marca del producto.** Las palabras prohibidas y el posicionamiento
   viven en la memoria del producto — **leerla antes de redactar**, no después.
   Ejemplo Le'côterra: jamás "desodorante" ni "antitranspirante"; Athletix nunca liderando por
   "pies/calzado/objetos" ni en zona íntima.
6. **Compliance Meta:** sin atributos personales en 2ª persona ("tu zona íntima huele"), sin
   claims médicos, sin antes/después engañoso. Reformular a 1ª persona y aspiracional.

🔴 **Si un creativo no pasa la 5, NO se publica con el copy viejo.** Se reescribe o se deja fuera
de la tanda y se reporta. Pasó el 2026-09-03: los dos anuncios de Athletix quedaron fuera porque
sus copys guardados lideraban con "pies, calzado y objetos".

---

## PASO 5 — Montar y VERIFICAR con los ojos

1. `ads_create_creative` — video: `video_id` + `image_url` (miniatura) + `link_url` + CTA.
   Imagen: `image_hash` (preferido) o `image_url`.
2. `ads_create_ad` con `creative_id` + `conversion_domain`.
3. 🔴 **`ads_get_ad_preview`** sobre el anuncio creado (`INSTAGRAM_STORY` / `MOBILE_FEED_STANDARD`)
   y **mirar el render**. Es la fase 4 del protocolo: lo no ejecutado no se da por bueno.
   **Entregar el `preview_url` al usuario**, que es su prueba.
4. Releer `effective_status`. `IN_PROCESS` / `PENDING_REVIEW` es normal recién creado: Meta tarda
   minutos en procesar el video. **No es un fallo, y hay que avisarlo** — si no, el usuario abre
   el panel, no ve miniatura y cree que no se montó nada (pasó el 2026-09-03).

---

## Topes del MCP medidos el 2026-09-03 (no reintentar contra ellos)

- **Creativos click-to-WhatsApp: NO se pueden crear.** Con `link_url` → *"Too many parameters in
  Call To Action: remove parameter link"*. Sin `link_url` → el CTA se descarta **en silencio** (el
  creativo vuelve sin `call_to_action_type`) y el anuncio se cae con *"You can use Replies
  optimization only with Ads driving traffic to Messenger"*. La salida es promocionar una
  publicación orgánica existente (`object_story_id`), que es como corre CP1, o armarlo en el panel.
- **`description` (link_description) exige un CTA con enlace.** En creativos de video sin enlace,
  omitir `description`.
- **`asset_feed_spec` no está expuesto** → 1+1+1 por API (ver Paso 3).
- **UTM no se pone por API** → se pegan en el panel antes de activar (`24`). CTWA exento.

---

Relacionado: `15-creativos-produccion.md` (árbol TIENE/NO TIENE media y generación con IA) ·
`23-salud-de-senal-y-andromeda.md` (el ángulo como unidad) · `24-utm-atribucion.md` ·
`reglas-de-oro.md` §5 (presupuesto: COP ×1) · skills `golden-video-teardown`, `watch`,
`golden-copywriting`.
