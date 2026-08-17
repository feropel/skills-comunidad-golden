# TikTok Ads — gestión y optimización (report-based)

⚠️ **No hay MCP en vivo de TikTok** en este entorno. Trabajas con: informe exportado del TikTok Ads
Manager (Modo A) o sin datos para testear (Modo B), y entregas la **configuración exacta para pegar**
en el gestor. Para playbook de referencia, `claude-ads:ads-tiktok`. Copys ← `golden-copywriting`.

## Fuente de datos
- **A) Informe** (export del Ads Manager): pide columnas gasto, impresiones, CTR, CPC, CPM, conversiones,
  CPA, ROAS, **retención de video** (2s/6s, watched %), frecuencia. Cruza con breakeven (REGLA 2).
- **C) Sin datos**: Modo B (testeo) con la investigación + TikTok Creative Center (top ads del nicho).

## Estructura (campaña → grupo → anuncio)
- **Campaña**: objetivo **Ventas/Conversiones** (Pixel + Events API) o Leads/Tráfico-WhatsApp según modelo.
  Manual para testear; **Smart+** (Smart Performance Campaign) para escalar. CBO vs ABO igual que Meta.
- **Grupo**: optimización a Compra; público **amplio + targeting automático** (TikTok rinde con amplio);
  edades por rango TikTok (18–24/25–34/35–44/45–54/55+), sexo por persona, país con cobertura COD;
  ubicaciones automáticas (revisar Pangle). Custom/Lookalike para retargeting y escala.
- **Anuncio**: **video vertical 9:16 nativo**, **hook <2s**, sonido en tendencia, subtítulos quemados,
  UGC > producción pulida. **Spark Ads** (impulsar orgánico propio/creador) = más confianza/CTR.

## Optimización (Modo A) — qué activar/desactivar
ACTIVAR: Pixel+Events API, targeting automático/amplio, Smart+ para escalar, Spark Ads, comentarios
moderados (prueba social). DESACTIVAR/VIGILAR: Pangle si trae basura, audiencias demasiado estrechas
(TikTok castiga el alcance), creativos tipo "anuncio de TV". 
- Lee **retención de video** (no solo CTR): hook que no retiene = no convierte. Refresca creativos
  MÁS seguido que en Meta (fatiga alta — ver `08`).

## Decisión (usa `07`, ajustado a TikTok)
Matar grupo/creativo sin retención ni compras tras ~1.5–2× CPA objetivo; escalar el de CPA≤breakeven
subiendo presupuesto gradual. Retargeting (ver `06`): engagers de video, visitantes, carrito.

## Entregable
`PROYECTOS/<PRODUCTO>/ADS/TIKTOK-ADS.md`: estructura campo por campo lista para pegar + creativos/guiones
+ criterios de decisión. (Compliance TikTok: más estricto en salud/peso/finanzas.)
