# Embudo completo: prospecting + retargeting (donde está el ROAS barato)

La mayoría solo hace prospecting (frío) y deja el dinero en la mesa. El retargeting (tibio/caliente)
suele traer el CPA más bajo. Diseña SIEMPRE las 3 etapas.

## TOF · Prospecting (frío) — crear demanda
- Público amplio (Advantage+ Audience / LAL de compradores 1–3%). Objetivo Compra.
- Creativos de gancho fuerte (ángulos de la investigación). Es el grueso del presupuesto.
- KPI guía: CPA y CTR (ver `07`). Aquí se testea (ver `08`).

## MOF · Retargeting medio (tibio) — consideración
Públicos (custom audiences):
- Engagement de IG/FB (90 días), reproductores de video (≥50/75%), visitantes web (`ViewContent`).
- Mensaje: prueba social, comparativa, manejo de objeciones, reseñas. CTA "conoce más / pruébalo".
- En Meta MCP: `ads_create_custom_audience` subtype `ENGAGEMENT` (IG/Page/video) o `WEBSITE` (pixel).

## BOF · Retargeting bajo (caliente) — cierre
Públicos de alta intención:
- Add-to-cart / Initiate-checkout SIN compra (carrito abandonado), visitantes de producto 7–14 días.
- **DPA / catálogo** (`ads_catalog_*` + product set): muestra el producto exacto que vieron + oferta/urgencia.
- Mensaje: oferta directa, garantía COD, envío, escasez real. CTA "compra ahora". CPA más bajo del embudo.
- Excluir compradores recientes (salvo cross-sell/recompra).

## Reglas del embudo
- **Exclusiones**: cada etapa excluye a las inferiores para no competir (BOF excluye compradores;
  MOF excluye BOF; TOF excluye web visitors si el volumen lo permite).
- Presupuesto orientativo: ~70% TOF / 20% MOF / 10% BOF al inicio; ajusta según CPA por etapa.
- Sin píxel/CAPI con eventos ViewContent/AddToCart/Purchase NO hay retargeting → es prerrequisito.
- DPA requiere catálogo conectado (Shopify → catálogo Meta). Si no existe, márcalo como pendiente.
