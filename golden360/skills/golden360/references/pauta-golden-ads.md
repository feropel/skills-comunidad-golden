# FASE 7 · Pauta completa (handoff a `golden-ads`)

## Regla
La estrategia de pauta **NO se escribe aquí**. Se delega ENTERA en **`golden-ads`** (el centro de
comando de pauta: Meta + TikTok + Google), leído en vivo y en su última versión. `golden-ads` es la
**única fuente de verdad** de ads — esta skill solo le pasa contexto y recibe el entregable.
(Por eso ya NO existen aquí playbooks de Meta/TikTok/Google: vivían duplicados y se movieron a `golden-ads`.)

## Qué le pasa el expediente a golden-ads (del Bloque 1 y las Fases 3–5)
- **Producto + oferta + precio + COSTO/margen + país/moneda + modelo** (COD/anticipado) y
  **PRESUPUESTO disponible** — son los inputs obligatorios que golden-ads espera (su `01-fuentes-datos.md`
  detecta además la fuente: Meta MCP en vivo / informe / sin datos).
- **Buyer personas** (edades, sexos, ubicaciones, intereses) → segmentación.
- **Ángulos** (5–8) → un conjunto/ad set por ángulo en el testeo.
- **Objeciones + diferenciales + voz del cliente** (frases textuales) → copys y creativos.
- **Inteligencia de anuncios** de la investigación (qué corre la competencia) → benchmarks/diferenciación.
- **Recursos visuales de la FASE 5** (imágenes/GIF/videos ya producidos) → creativos reutilizables.
  Sin creativos no se arma campaña: la Fase 5 es puerta dura y va ANTES que esta.

## Qué detecta y entrega golden-ads
1. **Fuente de datos**: Meta EN VIVO por MCP / informe Excel-CSV exportado / SIN datos (testeo).
2. **Modo CON métricas** → diagnóstico (unit economics, qué pausar/escalar, benchmarks, fatiga) +
   reestructuración. **Modo SIN métricas** → estructura de testeo ganadora desde el estudio.
3. Para **Meta, TikTok y Google**: estructura campaña/conjunto/anuncio campo por campo, objetivo,
   presupuesto/pujas, segmentación (edades/sexos/ubicaciones/Advantage+), evento de conversión,
   ubicaciones, **qué activar/desactivar**, retargeting/full-funnel, y por creativo **5 hooks +
   5 títulos + 5 descripciones** + prompts de imagen/video.
4. **Publicación**: en Meta puede crear campañas/conjuntos/anuncios por MCP **en PAUSA** (activa solo
   con tu OK). En TikTok/Google entrega la config exacta para pegar (no hay MCP en vivo).

## Salida de la fase
`golden-ads` produce el `PAUTA.md` (Meta + TikTok + Google) que se guarda en `PROYECTOS/<PRODUCTO>/`.
Esta skill solo verifica que esté completo y lo enlaza en el paquete final (**Fase 9**).
El seguimiento posterior (Fase 10) también es de `golden-ads`:
`~/.claude/skills/golden-ads/references/20-seguimiento.md`.

> El orgánico de redes (no es pauta) se queda en `references/organico-redes.md` (**Fase 6**, va ANTES
> que la pauta: calienta audiencia y baja el CPA).
