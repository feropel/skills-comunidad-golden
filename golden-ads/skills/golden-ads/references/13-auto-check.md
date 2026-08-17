# Auto-check de cierre (correr ANTES de entregar cualquier diagnóstico o plan)

Objetivo: que los errores ya vistos (dar veredicto sin economics, campo inválido, activar sin OK,
confundir moneda) sean imposibles de entregar. Verifica cada punto; si alguno falla, NO entregues.

## Diagnóstico (Modo A)
- [ ] Cuenta confirmada por `ads_get_ad_accounts` (id, **moneda**, estado, mcp_enabled, queryable).
- [ ] Métricas leídas con **campos válidos** (chuleta `11`) y **rango de fechas** explícito.
- [ ] **Unit economics resueltos** (`12`) o marcados `[PENDIENTE]` — y el veredicto absoluto se dio
      SOLO si están; si no, se entregó ranking **relativo** + se pidió precio/costo/entrega.
- [ ] **ROAS descontado por tasa de entrega** (COD): se reportó ROAS Meta Y ROAS pagado estimado.
- [ ] Semáforo por campaña/creativo contra el breakeven (no contra un número genérico).
- [ ] 3 listas explícitas: **QUÉ PAUSAR / QUÉ ESCALAR / QUÉ AJUSTAR**, cada una con su número.
- [ ] Banderas revisadas: nombres duplicados, ROAS "Not available" con gasto, overlap de subasta.
- [ ] Se miró **retargeting** (`06`): existe o es solo prospecting? (oportunidad si falta).
- [ ] Moneda correcta en TODAS las cifras (no asumir USD; CP8 era COP).

## Testeo (Modo B)
- [ ] Insumos de investigación (ángulos, persona, objeciones, oferta) presentes.
- [ ] Estructura definida (campaña/conjuntos=ángulos/creativos) + presupuestos ≥ mínimo de cuenta.
- [ ] **Criterios de matar/escalar escritos ANTES** de lanzar (`07`).
- [ ] Pixel/CAPI + evento de Compra verificados como prerrequisito.

## Publicación (si aplica)
- [ ] Todo creado **PAUSED**. Resumen mostrado (objetivo/público/presupuesto/evento/creativos).
- [ ] Activación **solo con OK explícito** del usuario. Se le recordó que activar = gasto real.
- [ ] Reglas CBO/ABO respetadas (no budget en campaña Y conjunto a la vez).

## Entrega
- [ ] Guardado en `PROYECTOS/<PRODUCTO>/ADS/` (`DIAGNOSTICO.md` / `TEST-PLAN.md` / `META-ADS.md`...).
- [ ] Cada afirmación de métrica con su fuente (MCP/informe). Nada inventado.
