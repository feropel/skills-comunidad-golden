# GOLDEN PRO — el preset ÚNICO de columnas de Golden (construido en vivo)

Preset maestro definitivo del usuario, construido y validado EN VIVO en su Ads Manager (CP1, 2026-06-25).
**Un solo set** que sirve para campañas WEB (COD) y de WHATSAPP a la vez (el usuario usa ambas). Reemplaza
los presets viejos e inconsistentes por cuenta (FER 2026 / GOLDEN 2026 / GOLDEN 2025 / Fer 2025).

## Principio de ORDEN: decisión primero → embudo diagnóstico
Se lee de arriba: **gano? escalo?** (bloque 1) y luego **dónde se rompe?** (embudo). Cada caída
en el embudo señala el culpable (creativo / landing / checkout / cierre del bot).

## Los 5 bloques (orden exacto)
**🟩 1 · GANO? (decisión escalar/pausar):** Entrega · Presupuesto · Importe gastado · Resultados ·
Compras · Costo por resultado · CPA (final) · Tasa de CPA % · Ticket Promedio $ · ROAS de compras.
**🟦 2 · EMBUDO WEB (dónde se cae):** Alcance · Impresiones · CPM · Frecuencia · FTIR · Clics únicos
enlace · CTR único · CTR · CPC · Visitas a la página (LPV) · Velocidad de carga % · Visualizaciones de
contenido (+costo) · Artículos agregados al carrito (+costo) · Pagos iniciados · Tasa Conv Compras %.
**🟨 3 · EMBUDO WHATSAPP:** Conversaciones iniciadas · Costo por conversación · Tasa Conv WP %.
**🟪 4 · CREATIVO/VIDEO:** Video 3s · Hook Rate % · Video 50% · Video 75% · Video 100% · Hold Rate %.
**⬜ 5 · SUBASTA:** Clasif. de calidad · Clasif. de interacción · Clasif. de conversiones. — **Ident:** ID anuncio.

## Métricas de fórmula (CUSTOM, creadas a nivel NEGOCIO → sirven en TODAS las cuentas)
Se crean en Personalizar columnas → "Crear métrica personalizada", acceso "Todas las personas con
acceso a Negocio", formato %:
- **FTIR** = `Alcance ÷ Impresiones` (% que ve por 1ª vez; bajo = saturación). *(ya existía)*
- **Hook Rate %** = `Reproducciones de video de 3 s ÷ Impresiones` (fuerza del gancho). *(creada en vivo)*
- **Hold Rate %** = `Reproducciones de video hasta el 100% ÷ Reproducciones de video de 3 s` (retención real). *(creada en vivo)*
- **Tasa de CPA %** = `CPA ÷ Ticket promedio` (% del ingreso que se va en adquirir ≈ inverso ROAS).
- **Ticket Promedio $** = `Valor de conversión de compras ÷ Compras`.
- **Velocidad de carga %** = `Visitas a la página de destino ÷ Clics en el enlace`.
- **Tasa Conv WP %** = `Eventos WhatsApp ÷ Clics en el enlace` · **Tasa Conv Compras %** = `Compras ÷ Clics`.
- **CPA (final)** = `Importe gastado ÷ Compras`.

## 🚀 REPLICACIÓN POR URL — el método OFICIAL (validado en vivo CP1/CP5/CP6, 2026-07-02)
Ads Manager acepta el parámetro `columns=` en la URL con la lista de campos EN ORDEN. Pegar la URL
en cualquier cuenta del negocio aplica la vista completa (las custom resuelven porque son de negocio);
luego 3 clics para dejarla fija: **Columnas → Personalizar columnas → "Guardar como valor predefinido
de columna" → nombre `GOLDEN PRO` → Guardar**. NO hay que marcar ni arrastrar nada.

**URL MAESTRA GOLDEN PRO** (reemplazar `<ACT_ID>` por el ID de la cuenta y `<BUSINESS_ID>` por el
ID del business; las métricas custom `<MDX_...>` son IDs propios de CADA negocio — se obtienen con
el método "Cómo obtener la URL de una vista" de abajo):
```
https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=<ACT_ID>&business_id=<BUSINESS_ID>&columns=name%2Cdelivery%2Cbudget%2Cspend%2Cresults%2Cactions%3Aomni_purchase%2Ccost_per_result%2Ccustom_derived_metrics%3A<MDX_CPA>%2Ccustom_derived_metrics%3A<MDX_TASA_CPA>%2Ccustom_derived_metrics%3A<MDX_TICKET>%2Cpurchase_roas%3Aomni_purchase%2Creach%2Cimpressions%2Ccpm%2Cfrequency%2Ccustom_derived_metrics%3A<MDX_FTIR>%2Cunique_actions%3Alink_click%2Cunique_website_ctr%3Alink_click%2Cwebsite_ctr%3Alink_click%2Ccost_per_action_type%3Alink_click%2Cactions%3Alanding_page_view%2Ccustom_derived_metrics%3A<MDX_VEL_CARGA>%2Cactions%3Aomni_view_content%2Ccost_per_action_type%3Aomni_view_content%2Cactions%3Aomni_add_to_cart%2Ccost_per_action_type%3Aomni_add_to_cart%2Cactions%3Aomni_initiated_checkout%2Ccustom_derived_metrics%3A<MDX_CONV_COMPRAS>%2Cactions%3Aonsite_conversion.messaging_conversation_started_7d%2Ccost_per_action_type%3Aonsite_conversion.messaging_conversation_started_7d%2Ccustom_derived_metrics%3A<MDX_CONV_WP>%2Cactions%3Avideo_view%2Ccustom_derived_metrics%3A<MDX_HOOK>%2Cvideo_p50_watched_actions%3Avideo_view%2Cvideo_p75_watched_actions%3Avideo_view%2Cvideo_p100_watched_actions%3Avideo_view%2Ccustom_derived_metrics%3A<MDX_HOLD>%2Cquality_score_organic%2Cquality_score_ectr%2Cquality_score_ecvr%2Cad_id&attribution_windows=default
```

**Diccionario de tokens (las métricas custom son POR NEGOCIO — crea las tuyas y toma sus IDs con
el método de abajo):** CPA=`<MDX_CPA>` · Tasa de CPA %=`<MDX_TASA_CPA>` · Ticket Promedio $=
`<MDX_TICKET>` · FTIR=`<MDX_FTIR>` · Velocidad Carga=`<MDX_VEL_CARGA>` · Tasa Conv WP %=
`<MDX_CONV_WP>` · Tasa Conv Compras %=`<MDX_CONV_COMPRAS>` · Hook Rate %=`<MDX_HOOK>` ·
Hold Rate %=`<MDX_HOLD>`. Estándar clave (universal, igual en todo negocio): compras=`actions:omni_purchase`, CPC=
`cost_per_action_type:link_click`, CTR=`website_ctr:link_click`, CTR único=`unique_website_ctr:link_click`,
conversaciones=`actions:onsite_conversion.messaging_conversation_started_7d`, clasificaciones=
`quality_score_organic/_ectr/_ecvr`, video=`actions:video_view` + `video_p50/75/100_watched_actions:video_view`.

> **Trabajando en el negocio GOLDEN:** los IDs reales (business, cuentas CP1-CP6, métricas custom y
> la URL maestra ya armada) viven en el archivo privado local
> `PROYECTOS/STACK-GOLDEN/GOLDEN-ADS-PRIVADO.md` — leerlo ANTES de armar vistas. Ese archivo NO se
> distribuye; si no existe (instalación de un alumno), usar los placeholders con los IDs propios.

**Cómo obtener la URL de una vista (para otro negocio/cliente):** con la vista activa, eliminar o mover
UNA columna por el menú del encabezado (▾ → Columnas → Eliminar columna) → Ads Manager pasa a modo
"Personalizado" y reescribe la URL con el `columns=` completo → copiarla. (El menú ▾ del encabezado
también tiene "Mover a la izquierda/derecha": ajustes de orden SIN arrastrar.)

**Estado replicado (2026-07-02):** presets GOLDEN PRO ya fijados en varias cuentas del negocio Golden
(IDs de presets y de cuentas en el archivo privado `GOLDEN-ADS-PRIVADO.md`, no en esta skill).
> El MCP no puede fijar la vista de columnas (es UI); este método por URL es el camino. `column_preset=<id>`
> NO viaja entre cuentas (el preset es por cuenta); `columns=` SÍ.

## Diagnóstico (para qué sirve el orden)
Gasto alto + pocas ventas → baja por el embudo: **Impresiones OK, pocos clics** = creativo/ángulo ·
**clics OK, poca LPV** = landing lenta · **LPV OK, poco carrito/checkout** = página/precio/confianza ·
**checkout OK, poca compra** = checkout/COD · **(WA) muchas conversaciones, pocas ventas** = cierre/bot.

## 🚦 SEMÁFORO DE METAS (umbral por métrica — usar SIEMPRE al diagnosticar)
Punto de partida COD LatAm; calibrar con el histórico real de la cuenta cuando exista (≥15–30 compras).
| Métrica | 🟢 Buena señal | 🔴 Alarma / acción |
|---|---|---|
| Entrega | Activa | "Limitada" / aprendizaje eterno → revisar presupuesto-pixel |
| Importe gastado | ≥ 3× CPA antes de juzgar | Juzgar con menos gasto = decidir sin datos |
| Compras | ≥ 15–30 para decidir en firme | Menos = señal, no verdad (regla significancia) |
| CPA (final) | < breakeven → ESCALAR | > breakeven sostenido → pausar/ajustar |
| Tasa de CPA % | Cuanto más baja mejor | Subiendo = margen comiéndose |
| ROAS compras | ROAS Meta ≥ breakeven ÷ %entrega | Debajo = pierde plata aunque Meta se vea "bien" |
| Frecuencia | < 2 ideal | > 3 = fatiga → refrescar creativo |
| FTIR | Alto y estable | Bajando = saturación (deja de llegar gente nueva) |
| CTR (enlace) | > 1% | < 0.5% = creativo/ángulo débil |
| Velocidad de carga % | > 80% | < 60% = landing lenta o incoherente con el anuncio |
| Tasa Conv Compras % | > 1–2% | Bajo con clics OK = la landing no cierra |
| Hook Rate % | > 25% | < 15% = cambiar el gancho (primeros 3s) |
| Hold Rate % | > 20% | < 10% = video flojo; CTR alto + Hold bajo = clickbait |
| Clasificaciones subasta | Promedio o superior | "Por debajo del promedio" → calidad=creativo · conversión=landing |
> CPM y CPC **no llevan umbral fijo** (dependen de país/vertical): compararlos contra el histórico propio.
> Alcance, impresiones, carritos, checkouts = contexto: se leen en relación entre sí (embudo), no solos.

## 📄 Documento entregable para el usuario/cliente
Existe guía imprimible con las 40 columnas + fórmulas + semáforo: `GOLDEN PRO - Guia de Metricas y
Columnas` (.docx y .pdf, Desktop del usuario, v1.1). Si piden "el documento de las métricas" o hay que
re-generarlo: tabla de 7 columnas (# · Español · English · Tipo · Fórmula · Meta objetivo · Qué mide),
horizontal, 5 bloques con intro cada uno, custom en dorado, metas en verde, notas COD al final.
