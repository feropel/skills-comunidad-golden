# FASE 4 · Destino de venta (página/sitio)

> Numeración canónica del pipeline R1.0 (SKILL.md y el mapa espejo mandan): 3 SEO · **4 destino de
> venta** · 5 creativos · 6 orgánico · 7 pauta · 8 bot · 9 paquete. Las compuertas son 1 VIABILIDAD,
> 2 VERACIDAD, 3 MONTAJE, 4 QA — no llevan número de fase.

## Elegir destino por perfil (no asumir — detectarlo del estudio)
- **Producto dropshipping / COD** → `golden-shopify` (sigue TODA esta guía).
- **Marca propia / creador de contenido / empresa / captación de leads** (no es producto COD) →
  **`golden-web`** (sitio/landing por perfil, deploy Vercel + dominio). Aliméntala con los mismos
  hallazgos del estudio (persona, ángulos, objeciones, diferenciales).
- **Negocio de SERVICIOS** que vende citas → suma **`golden-agenda-citas`** (Google Calendar).

## Regla absoluta (caso Shopify/COD)
La página se genera **SÍ O SÍ con `golden-shopify`** (la más actual, leída en vivo). NUNCA a mano,
nunca improvisada, nunca con una versión recordada de otro chat.

Antes de construir:
1. Lee `~/.claude/skills/golden-shopify/` → sello `GFS_VERSION`, `references/changelog.md` (últimas
   2-3 entradas) y **la plantilla/ejemplo que SU PROPIO SKILL.md recomiende en ese momento** (no
   asumas un archivo ni un embudo fijo: golden-shopify evoluciona rápido y su embudo canónico manda).
2. Confirma datos reales que cuestan render (REGLA 4 del orquestador): **precio, WhatsApp (el mensaje
   del botón de WhatsApp debe ser la PALABRA CLAVE que dispara el bot de Chatea PRO — pídela
   siempre), modelo COD/anticipado, país (tiempos de entrega)**. Si aún no los da, la página se GENERA
   igual con los valores marcados `[PROPUESTO]`/`[PENDIENTE]` — pero NO se monta en la tienda: el
   precio definitivo lo entrega el dueño en la **COMPUERTA 3 · MONTAJE** del SKILL.md.

## Qué le pasas a golden-shopify (de la investigación, Bloque 1)
- Buyer persona + **citas textuales** → para el copy de hero, escalera y reseñas.
- Objeciones → para FAQ y garantía. Diferenciales → para la sección "por qué elegir".
- Ángulo principal → hero/manifiesto. Oferta/ancla → bloque de oferta + precio dinámico.
- Color por vertical (golden-shopify recomienda el que más vende).

## Imágenes / GIF / video (cuando se necesiten)
- **Imágenes de producto e infografías** → **`golden-imagen-arena`** (varios motores por API vía Higgsfield): compone
  sobre la **FOTO REAL** del producto + texto de venta — carrusel 1080×1080 y secciones 1080×1350,
  descarga **WebP <150KB**. Nada de IA que redibuje el producto; evitar fondos amarillos saturados.
  Entrega directo a golden-shopify (ficha) y golden-ads (pauta).
- **Infografías/beneficios alternativa** → componer en HTML (lo hace golden-shopify) o imagen ligera.
- **Video/UGC demostrativo** → `golden-ugc-avatar` (Higgsfield: Soul 2.0 imagen, Seedance 2.0 video
  con audio nativo). Útil para la escalera de venta y como creativo reutilizable en ads.
- Si no hay saldo/créditos para generar → entrega los **prompts/specs** listos y deja slots en la página.

## Salida de la fase
- `product.<tema>.json` (o el JSON del tema) generado por golden-shopify, guardado en
  `PROYECTOS/<PRODUCTO>/`, + enlace de preview si aplica.
- Lista de imágenes/videos usados y los pendientes por generar.

> El detalle de embudo, bloques, Releasit/COD y recoloreo vive DENTRO de golden-shopify. Aquí solo
> orquestas: investigación → golden-shopify → recursos visuales.
