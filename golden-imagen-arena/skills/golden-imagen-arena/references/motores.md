# Catálogo de motores (MCP Higgsfield)

Verificado en vivo con `models_explore {action:"list", type:"image"}` el **2026-07-21**.
Si algo no cuadra, vuelve a listar: el catálogo cambia sin aviso.

## Cómo se llama a un motor

```
generate_image {
  params: {
    model: "<id>",
    prompt: "<prompt maestro>",
    aspect_ratio: "1:1" | "4:5" | ...,
    count: 1,
    medias: [{ value: "<media_id>", role: "image" | "image_references" }],
    <parámetros propios del modelo van al MISMO nivel: resolution, quality, variant...>
  }
}
```

- `medias[].value` es SIEMPRE un `media_id` (de `media_import_url` / `media_upload`) o un
  `job_id` de una generación previa. **Nunca una URL https://**.
- El `role` varía por modelo. Los de Google/Higgsfield suelen usar `image`; los de
  Bytedance/BFL/OpenAI-Hazel usan `image_references`. Ante la duda:
  `models_explore {action:"get", model_id:"<id>"}` y mira `medias[].roles`.
- `get_cost: true` devuelve el costo sin generar. Úsalo en el preflight.
- La generación es **asíncrona**: `generate_image` devuelve un job. Consulta
  `job_status {job_id}` hasta `completed` para obtener las URLs de resultado
  (manejo de `failed`/moderación: paso 4 del SKILL.md).

## Los que sirven para ecom de producto

| id | Nombre | Proveedor | Resoluciones | Fuerte en | Cuándo lo pongo |
|---|---|---|---|---|---|
| `nano_banana_pro` | Nano Banana Pro | Google | 1k/2k/4k | texto, diagramas, fotorrealismo | **Favorito por defecto.** Infografía con texto en español y producto fiel |
| `nano_banana_2` | Nano Banana 2 | Google | 1k/2k/4k | rápido, alta calidad | Tandas grandes donde el costo importa |
| `nano_banana_2_lite` | Nano Banana 2 Lite | Google | 1k (`thinking` MINIMAL/HIGH) | sonda barata | Probar el prompt antes de la arena cara |
| `openai_hazel` | OpenAI Hazel | OpenAI | quality low/med/high | **el mejor texto**, logos, infografía | Retador fijo cuando la pieza vive de la tipografía |
| `gpt_image_2` | GPT Image 2 | OpenAI | 1k/2k/4k + quality | tipografía, edición | El mismo motor que ofrece Ecom Magic, pero por API |
| `seedream_v5_pro` | Seedream 5.0 Pro | Bytedance | 1k/1.5k/2k | edición por instrucción, razonamiento visual | Retador cuando hay que respetar mucho la foto |
| `seedream_v4_5` | Seedream 4.5 | Bytedance | basic 4K / high ~6K | transformaciones, alta resolución | Piezas sin texto que necesiten resolución grande |
| `flux_2` | FLUX.2 | Black Forest Labs | 1k/2k, variant pro/flex/max | obediencia literal al prompt | Cuando el prompt es muy específico y los demás improvisan |
| `flux_kontext` | Flux Kontext | Black Forest Labs | — | edición contextual, style transfer | Replicar el estilo de una pieza de referencia |
| `recraft_v4_1` | Recraft V4.1 | Recraft | 1k/2k | vector, logos, íconos, mockups, **paleta hex fija** | Íconos de beneficios, sellos, badges de garantía |
| `kling_omni_image` | Kling O1 Image | Kling | 1k/2k | fotorrealismo versátil | Alternativa de fondo/escena |
| `grok_image` | Grok Image | xAI | 1k/2k | alto contraste, expresivo | Creativos agresivos de pauta fría |
| `z_image` | Z Image | Tongyi-MAI | — | rapidísimo, estilizado | Bocetos desechables |
| `image_auto` | Auto | Higgsfield | — | enruta solo | Cuando no importa el control |

## Los de "estudio" (con contexto de marca)

- **`marketing_studio_image`** — anuncios de producto de un clic. Acepta la foto como
  `medias` y da 1k/2k/4k. Útil como cuarto competidor genérico.
- **`ms_image` (DTC Ads)** — el más potente para marca, pero exige protocolo:
  1. `show_marketing_studio {type:"image_style"}` y que **el usuario elija un `style_id`**
     (es obligatorio, sin él la llamada falla, y el estilo domina el resultado).
  2. Opcional `brand_kit_id` (kit con logo, colores, fuentes y tono, en estado
     `completed`) y hasta 4 `product_ids` de productos ya cargados en Marketing Studio.
  3. `batch_size` 1-20 en un solo job (el costo escala lineal, ojo con los créditos).

## Utilidades de post (no son "motores", son herramientas)

- `remove_background` — recorte / fondo transparente para componer. **Cuesta créditos por imagen.**

  > 🆓 **Para lotes usa el recortador LOCAL: `scripts/quitar-fondo.py`** (rembg, MIT, corre en tu
  > máquina). Medido el 2026-08-02 con un packshot 1080×1080 de Golden: **0,63 s por imagen, cero
  > créditos**, y resolvió bien el caso difícil — tapa blanca sobre fondo blanco — sin halos ni
  > bordes duros (52% transparente, 1,7% de borde con antialiasing sano).
  > Instalación una sola vez: `python3 -m venv ~/.golden-rembg` y
  > `~/.golden-rembg/bin/pip install "rembg[cpu]"`. La primera corrida baja el modelo (~176 MB) y
  > después **funciona sin conexión**: esa descarga es su única salida a internet.
  > Acepta carpeta entera y avisa si el borde salió duro o si no recortó casi nada.
  > **Cuándo seguir usando el MCP:** cuando el recorte tenga que respetar pelo, humo, cristal o
  > transparencias reales — ahí el modelo grande gana. Para packshots de frasco, caja o producto
  > sólido, el local basta y el ahorro en un catálogo es real.
- `outpaint_image` — expandir el encuadre (pasar un 1:1 a 4:5 sin recortar el producto).
- `upscale_image` / `topaz_image` — subir a 2K/4K la pieza ganadora si se va a imprimir o
  usar en pantalla grande. Para web NO hace falta: la meta es WebP < 150 KB.

## Cuánto cuesta DE VERDAD una generación (benchmark de mercado)

Los créditos de Higgsfield no dicen si el plan vale la pena. Esta es la referencia en
dólares del mercado abierto, verificada el **2026-07-27** en el tarifario público de
Muapi (agregador de pago por generación, sin suscripción). Sirve para **una sola cosa**:
saber si la suscripción se justifica con el volumen real del mes.

| Pieza | Modelo de referencia | Precio por generación |
|---|---|---|
| Imagen | Seedream 5.0 Pro | **$0,045** |
| Imagen | Z-Image turbo (boceto) | **$0,007** |
| Imagen | Ideogram v3 texto a imagen | **$0,02** |
| Video | Wan 2.2 imagen a video | **$0,30** |
| Video | LTX-2 Pro imagen a video | **$0,46** |
| Video | Veo3 fast | **$0,60** |
| Video | Veo3 completo | **$2,50** |
| Lipsync | sync / veed / latent-sync | **$0,04** |

**El punto de equilibrio contra Higgsfield Plus ($47/mes, ilimitado):**

| Si el mes lleva… | …el equivalente pagando por generación |
|---|---|
| 1.044 imágenes Seedream Pro | $47 (empatan) |
| 156 videos Wan 2.2 | $47 (empatan) |
| 102 videos LTX-2 Pro | $47 (empatan) |
| 78 videos Veo3 fast | $47 (empatan) |

Lectura: **por debajo de ~100 videos o ~1.000 imágenes al mes, la suscripción se está
pagando de más**; por encima, el ilimitado gana con holgura. Un catálogo de 30 productos
con paquete visual completo cae normalmente en la zona baja, así que **revisa el consumo
real antes de renovar**. Si el mes fue flojo, dilo con este número, no con una sensación.

> Esto es un **termómetro de precio, no una recomendación de migrar.** Higgsfield está
> integrado por MCP y dos skills viven encima de él; cambiar de proveedor cuesta más que
> la diferencia salvo que el desfase sea enorme y sostenido.

## Lo que NO está aquí

- **Ecom Magic** (el sitio ecom-magic.ai) no tiene API ni MCP (verificado en la cuenta y
  en su web). Solo navegador; por eso quedó fuera de esta arena.
- **Open-Generative-AI** (`Anil-matcha/Open-Generative-AI`, 24,9k ⭐, MIT) se vende en
  redes como "la alternativa open source que mata a Higgsfield". **Auditado y descartado
  el 2026-07-27**, por tres razones verificadas:
  1. **No es gratis ni es alternativa: es un embudo.** El autor declara `company: muapi.ai`
     en su propio perfil de GitHub, y muapi.ai es de **Vadoo Internet Services**. El repo
     regala la interfaz y te cobra por la API que él mismo vende. Lo "gratis" es el envase.
  2. **Los commits recientes son marketing, no código** ("cross-links a proyectos
     relacionados", "cambiar el video destacado"). Las estrellas no miden el software.
  3. **Su argumento de venta es "sin filtros de contenido"** e incluye modelos `spicy`
     explícitos. Para una marca que pauta en Meta y enseña a alumnos, eso es riesgo de
     cuenta y riesgo reputacional a cambio de cero ventaja técnica.
  Lo único que se rescató es su tarifario, que quedó arriba como benchmark.
- **Gemini API directa** (Nano Banana con key propia de AI Studio) se descartó a propósito:
  la key vieja se rotó el 2026-06-29 y solo se conservó la de Chatea PRO. Abrir otra sería
  otra factura y otro secreto que cuidar para llegar al mismo modelo que Higgsfield ya
  sirve. No re-sugerir salvo que Higgsfield deje de alcanzar.
