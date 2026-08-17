# Modos de entrega (con MCP vs sin MCP)

Según haya o no conexión en vivo a la cuenta, hay dos formas de entregar. En AMBOS el contenido es el
mismo (estructura completa); cambia si lo montamos nosotros o lo monta el cliente con un instructivo.

## Detectar
- La cuenta responde por MCP? (`ads_get_ad_accounts` → `is_ads_mcp_enabled` + `is_queryable`). Y el
  usuario quiere que lo montemos, o solo quiere el plan?

## A) CON MCP y con OK → montar en vivo (EN PAUSA)
Crea campaña→conjunto→creativo→anuncio por MCP (`05-publicar-mcp.md`), todo PAUSED, y activa solo con OK.

## B) SIN MCP (o cuenta ajena / cliente externo) → INFORME FULL para pegar
Entrega un documento `PROYECTOS/<PRODUCTO>/ADS/META-ADS.md` **tan detallado que el cliente solo copia y
pega** en su Ads Manager, sin decidir nada. Debe traer TODO, campo por campo:

### Estructura del informe
1. **Resumen y objetivo** (qué se monta y por qué) + **unit economics/breakeven** (`12`) + ROAS pagado.
2. **NIVEL CAMPAÑA**: objetivo (OUTCOME_SALES…), CBO/ABO, presupuesto (moneda de la cuenta), spend cap,
   nombre exacto (convención), categorías especiales.
3. **NIVEL CONJUNTO** (uno por ángulo): evento de conversión/optimización, público (Advantage+ o
   detallado con **la segmentación por histórico** `16`: sexo/edad/ubicación exactos), presupuesto,
   puja, ubicaciones, programación. **Copia-pega-able**: valores literales, no "elige tú".
4. **NIVEL ANUNCIO**: formato, identidad (página/IG), destino/URL o WhatsApp, y por cada creativo:
   la pieza (o su prompt/libreto `15`) + **5 hooks + 5 títulos + 5 descripciones** + CTA.
5. **Qué activar/desactivar** (Advantage+ placements/creativo, CAPI, etc.).
6. **Retargeting** (`06`), **criterios de matar/escalar** (`07`) y **higiene de aprendizaje** (`14`:
   controlar gasto con topes, NO apagados).
7. **Checklist de lanzamiento** (pixel/CAPI, breakeven, todo listo).

> Regla: el informe sin MCP debe poder ejecutarlo alguien que NO sabe de pauta. Nada de "según tu
> criterio": valores exactos, con el porqué en una línea. Es el mismo rigor que montarlo nosotros.

## Nota para TikTok/Google
Siempre van por informe (no hay MCP en vivo): usa este mismo formato en `TIKTOK-ADS.md` / `GOOGLE-ADS.md`
(ver `09`/`10`).
