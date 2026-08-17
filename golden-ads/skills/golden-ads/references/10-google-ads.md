# Google Ads — gestión y optimización (report-based)

⚠️ **No hay MCP en vivo de Google** en este entorno. Trabajas con informe exportado de Google Ads
(Modo A) o sin datos (Modo B), y entregas la **configuración exacta para pegar**. Playbook de
referencia: `claude-ads:ads-google`. Google **capta demanda existente** (complementa a Meta/TikTok
que la crean): quien ya busca el producto está más abajo en el embudo.

## Fuente de datos
- **A) Informe** (export de Google Ads): pide por campaña/grupo/keyword: impresiones, clics, CTR, CPC,
  costo, conversiones, CPA, ROAS, **Search impression share**, Quality Score. Cruza con breakeven.
- **C) Sin datos**: Modo B — keywords del nicho (volumen/intención), competidores (Auction Insights).

## Tipos de campaña (elige por etapa/objetivo)
- **Search** (intención alta): captura "comprar [producto]". Estructura: campaña → grupos temáticos
  ajustados → keywords (exact/phrase) + **negativas** (clave para no quemar presupuesto).
- **Performance Max (PMax)**: cobertura total (Search/Display/YouTube/Gmail/Maps) con asset groups +
  catálogo (Merchant Center). Para e-commerce con catálogo. Vigila el reparto y las búsquedas.
- **Demand Gen / YouTube / Discovery**: crear demanda con video/imagen (más parecido a Meta).
- **Shopping**: requiere Merchant Center + feed (conecta Shopify).

## Anuncios (RSA) y assets
- **RSA**: hasta **15 títulos + 4 descripciones** (los genera `golden-copywriting`, compliant). Fija
  1–2 títulos clave si hace falta. **Todas las extensiones/assets**: sitelinks, callouts, snippets
  estructurados, llamada, ubicación, precios, promoción, imagen.

## Optimización (Modo A) — qué activar/desactivar
ACTIVAR: conversiones mejoradas + etiqueta de conversión correcta (Compra), pujas automáticas
(tCPA/tROAS) cuando haya datos, negativas continuas, audiencias de remarketing/observación. 
VIGILAR/DESACTIVAR: Search Partners y Display Expansion si traen tráfico basura; "maximizar clics"
cuando el objetivo es compra; PMax sin exclusiones (puede canibalizar marca). Revisa Quality Score
(relevancia/landing) y Search terms (sangrado de keywords irrelevantes → negativas).

## Decisión (usa `07`, adaptado)
Pausar keyword/grupo con CPA > breakeven y volumen; subir puja/tCPA en los que convierten bajo
breakeven; mover presupuesto a campañas con mejor CPA. Remarketing (visitantes/carrito) = CPA bajo.

## Entregable
`PROYECTOS/<PRODUCTO>/ADS/GOOGLE-ADS.md`: estructura (tipo de campaña, grupos, keywords + negativas,
pujas), RSA (15 títulos/4 descripciones) + extensiones, y criterios de decisión.
