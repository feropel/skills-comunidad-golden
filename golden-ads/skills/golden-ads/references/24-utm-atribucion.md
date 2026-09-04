# UTM y atribución — de dónde vino la venta (regla dura, no opcional)

Un anuncio sin UTM entrega tráfico ciego: la venta llega y **nadie puede decir qué anuncio la
produjo**. En Golden eso cuesta plata dos veces — se escala lo que no vende y se mata lo que sí.
Por eso: **ningún anuncio que apunte a una LANDING se entrega ni se activa sin UTM.**

Esta regla vivía solo en la memoria de la casa y en los documentos de montaje; se bajó al archivo
el 2026-09-02 por orden directa de FER ("colocamos un UTM para que pueda enviar esa información de
dónde vino la venta, debe estar en la skill de Meta Ads"). Medido antes de escribirla: `grep -i utm`
sobre toda la skill daba **0 reglas** (solo dos menciones de pasada en changelog y en la referencia
externa de Panamá).

---

## 1. El esquema oficial (se pega tal cual, con macros)

Va en **Parámetros de URL** a nivel ANUNCIO, en los 10 anuncios de la tanda:

```
utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}&utm_id={{ad.id}}
```

**Fuente:** `PROYECTOS/LECOTERRA/campanas/MONTAJE-CP1-2026-07-25.md` y
`MONTAJE-CP1-OPEN7-2026-08-14.md`, que lo declaran verificado en vivo ("las macros entraron sin
doble-encodear"). Es lo que **está puesto hoy en las campañas de Golden**, no una propuesta.

| Parámetro | Qué lleva | Para quién |
|---|---|---|
| `utm_id` | `{{ad.id}}` — **LA LLAVE MÁQUINA** | el panel, el resolver, el cruce con Meta |
| `utm_content` | `{{ad.name}}` — dice **qué video vendió** | ojos humanos |
| `utm_campaign` / `utm_term` | nombre de campaña / conjunto | ojos humanos |
| `utm_source` | `{{site_source_name}}` (fb, ig, msg…) | de qué red llegó |
| `utm_medium` | `paid_social` fijo | separa pago de orgánico |

### 🔴 El ID va en `utm_id`, NUNCA en `utm_content`

Un contrato anterior del Centro de Mando (2026-08-14) ponía `utm_content={{ad.id}}`. **No es lo que
se montó.** La divergencia costó un fallo real: el 26-ago la orden 86907080 (Le'côterra) llegó con
`(ref:adOPEN 7 - V6 Bergamot)` — el lector buscaba el id donde vive el NOMBRE, y quedó una venta de
$259.801 colgando de un anuncio inexistente. Dos piezas correctas por separado, con contratos
distintos. **Manda este archivo: el id es `utm_id`.** Si cambias el esquema, cambia también el
lector (`GASTO-GOLDEN/atribucion-whatsapp/snippet-theme-liquid.html`, que hoy toma el primer valor
NUMÉRICO entre `utm_id`, `ad_id`, `utm_content`) — y al revés.

Regla que se deriva del incidente: **un id de anuncio de Meta es numérico y largo. Si lo que llega
no es numérico, no se guarda.** Un vacío honesto es reparable; un id falso no se vuelve a mirar.

---

## 2. Cómo se pone (y por qué no por MCP)

- **Ads Manager (UI), nivel anuncio → "Parámetros de URL"**. Es la vía buena hoy.
- ❌ **El MCP de Meta NO expone `url_tags` al crear.** Verificado contra los esquemas vivos de
  `ads_create_ad` y `ads_create_creative` (2026-09-02, relectura del esquema real; ya se había
  medido igual el 2026-08-14). Ninguno acepta `url_tags`. **Si montas por MCP (`05-publicar-mcp.md`),
  el anuncio nace SIN UTM** — y hay que pegarlo a mano en la UI antes de activar. Dilo en el
  entregable, no lo des por hecho.
- 🟡 **Candidato SIN VERIFICAR:** `ads_update_entity` con `entity_type:"ad"` y
  `fields:{"url_tags":"..."}` — `url_tags` sí es campo real del objeto Ad en la Marketing API, pero
  el MCP rechaza campos que no reconoce y **esto no se ha probado nunca**. Si lo pruebas: hazlo en
  UN anuncio, vuelve a LEER el anuncio para comprobar que quedó escrito, y anota aquí el resultado.
  Hasta entonces no se promete que funcione.
- **Sin MCP / informe full (`17-entrega.md`):** el bloque UTM va copiado en el informe, con la
  instrucción de dónde pegarlo. Es campo obligatorio del informe, no un extra.

---

## 3. Las dos rutas de la venta (no se confunden)

| Ruta | Cómo llega la atribución | Necesita UTM |
|---|---|---|
| **CTWA** (anuncio directo a WhatsApp) | Meta entrega el ad id dentro del primer mensaje (`payload.referral.source_id`). Cero configuración. | **NO** |
| **Landing** (anuncio → página → botón WhatsApp, o compra web) | El UTM viaja en la URL; el snippet del tema lo lee y lo estampa | **SÍ** |

Corrección de FER (2026-08-26), confirmada corriendo el resolver: *"todos los pedidos que entran por
Chatea traen el ID del anuncio, así no tenga UTM. La UTM que configuramos era para los pedidos que
vienen por Shopify, por internet."* Medido en 21 pedidos: 3 capturas, **las 3 por el campo nativo**,
0 por UTM. **No mezcles los dos sistemas**: si un negocio pauta 100% CTWA, el UTM no le arregla nada;
si manda tráfico a una página, sin UTM está ciego.

**Hueco declarado (no resuelto):** una venta cerrada por WhatsApp **sin pasar por Chatea** no tiene
quién lea el ref — vive en el texto de la conversación y solo la API de Chatea lo lee. Para cubrirlo
hay que guardar el ad id **en la orden** (atributo de carrito / campo oculto del formulario COD), no
en la conversación. Trabajo del lado tienda, fuera de esta skill.

---

## 4. Verificar (no se declara puesto sin esto)

1. Abrir la URL de destino con el UTM ya resuelto y confirmar que llega **el número**, no el nombre.
2. `ads_get_ad_entities` o la UI: leer los anuncios y confirmar que **los 10** traen el parámetro.
   Uno sin UTM en una tanda de diez es un agujero, no un detalle.
3. Que el consumidor esté vivo: el snippet corregido tiene que estar **pegado en `layout/theme.liquid`
   de la tienda**, no solo en el archivo fuente. Si ves llegar `(ref:ad<algo no numérico>)`, el
   despliegue no se hizo.
4. Reportar **cobertura**: cuántos anuncios de cuántos llevan UTM y cuáles no. Nunca "quedó listo".

**Estado medido a 2026-09-02:** la captura positiva por el camino **LANDING sigue SIN VERIFICAR** —
lo único comprobado contra la API de Meta es el camino nativo CTWA (ad `120249805036590118`).
No lo cantes como funcionando.

---

## 5. Quién consume esto (para no romperlo al tocarlo)

- `GASTO-GOLDEN/atribucion-whatsapp/snippet-theme-liquid.html` — lee la URL, estampa `(ref:ad<id>)`
  en el botón wa.me. (v2 añade `(src:google|organic|…)` para lo que no es Meta; pendiente de alta.)
- `DROPI-LOGISTICA/scripts/resolver_atribucion.py` — tarea diaria
  `resolver-atribucion-whatsapp-diario`; lee la conversación de Chatea y escribe el ad en la base.
- `GASTO-GOLDEN/lib/atribucion.ts` — el cruce y el panel.

Cambiar el esquema UTM sin avisar a estos tres rompe la cadena en silencio. Va a la bandeja del
Centro de Mando antes de tocarse.
