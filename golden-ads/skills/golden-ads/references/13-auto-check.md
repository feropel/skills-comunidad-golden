# Auto-check de cierre (correr ANTES de entregar cualquier diagnóstico o plan)

Objetivo: que los errores ya vistos (dar veredicto sin economics, campo inválido, activar sin OK,
confundir moneda) sean imposibles de entregar. Verifica cada punto; si alguno falla, NO entregues.

## Diagnóstico (Modo A)
- [ ] **SALUD DE SEÑAL revisada ANTES que el rendimiento** (`23`): CAPI activo, dedup ≥90%,
      EMQ ≥8.0, <30% de conjuntos en Learning Limited, presupuesto del conjunto ≥5x CPA. Si la
      señal está rota, TODO lo demás se está midiendo sobre datos falsos y hay que decirlo primero.
- [ ] **Andromeda** (`23`): ¿los creativos del conjunto son CONCEPTOS distintos o variaciones del
      mismo ángulo? Similarity >60% = supresión. Menos de 10 conceptos genuinos = bandera.
- [ ] Si se declaró **fatiga por caída de CTR**: se verificó que no coincida con la redefinición
      de link clicks de feb-2025 (`23`), que bajó el CTR sin empeorar el creativo.
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

## 🔴 ANTES DE CONSTRUIR — inventario y método (fallos medidos el 2026-09-03, GOLDEN CP6)
- [ ] **Se LEYÓ `05-publicar-mcp.md` antes de crear nada por MCP.** No improvisar la receta desde
      la memoria: la skill ya trae el orden, el CBO/ABO, el `advantage_audience=0` y el aviso de
      que el MCP **no acepta `url_tags`**. Improvisar hizo "descubrir" a golpes cosas ya escritas.
- [ ] **INVENTARIO COMPLETO de la cuenta, las CUATRO listas**: `ads_get_ad_entities` (campañas),
      **`ads_get_creatives`**, `ads_get_ad_videos`, `ads_get_ad_images`.
      🔴 **Prohibido decir "la cuenta está vacía" habiendo mirado solo las campañas.** CP6 tenía
      **0 campañas y 12+ creativos de Le'côterra del 14-ago** que nadie miró; se construyó desde
      cero reutilizando videos de julio y se ignoró una oferta viva ("la segunda en $60.000").
- [ ] **La vía recomendada se verificó CONSTRUIBLE antes de recomendarla.** No proponer un embudo
      (p. ej. click-to-WhatsApp) y descubrir a mitad del montaje que el MCP no lo puede crear:
      obliga a rehacer y deja basura. Ver los topes en `25`.
- [ ] **Largos medidos ANTES de crear el creativo** (125 / 40 / **25**). 🔴 **Los creativos son
      INMUTABLES**: una descripción de 60 caracteres no se corrige después — hay que rehacer el
      creativo Y el anuncio. El 2026-09-03 entraron 9 creativos con descripciones de 49-88 que
      Meta trunca en silencio.
- [ ] **Sin creativos huérfanos**: si se cambió de plan a mitad del montaje, los creativos que
      quedaron sin anuncio se borran o se reportan. No dejarlos regados en la cuenta.

## Testeo (Modo B)
- [ ] Insumos de investigación (ángulos, persona, objeciones, oferta) presentes.
- [ ] Estructura definida (campaña/conjuntos=ángulos/creativos) + presupuestos ≥ mínimo de cuenta.
- [ ] **Criterios de matar/escalar escritos ANTES** de lanzar (`07`).
- [ ] Pixel/CAPI + evento de Compra verificados como prerrequisito.

## Publicación (si aplica)
- [ ] 🔴 **UTM puesto en TODOS los anuncios a landing** (`24`, REGLA 18), con el id en `utm_id`.
      Se reporta cobertura (N de N). El MCP no lo pone: si se montó por MCP, se pegó en la UI
      ANTES de activar. Sin UTM no se activa. (CTWA exento: ad id nativo.)
- [ ] 🔴 **CREATIVOS: el copy nace del creativo ANALIZADO.** Si se subió o recibió media, el video
      se **vio Y escuchó** (`golden-video-teardown` / `watch` + `golden-transcribe`) antes de
      redactar, y cada copy pasó la **prueba de coherencia de 6 puntos** (`25`). Se corrió
      `ads_get_ad_preview` y **se entregó el `preview_url`** al usuario. Se avisó que
      `IN_PROCESS`/`PENDING_REVIEW` es normal y no es un fallo.
- [ ] 🔴 **PRESUPUESTO RELEÍDO DEL SERVIDOR.** Tras crear/actualizar, `ads_get_ad_entities` sobre
      el conjunto y comparar el `daily_budget` **renderizado** (`"$ 50.000 COP"`) contra la cifra
      que pidió el usuario. **Monedas sin decimales (COP/CLP/PYG) van ×1, no ×100** — el parámetro
      dice "cents" y miente (`reglas-de-oro` §5). Sin esta relectura no se reporta el montaje.
      Incidente que lo obliga: 2026-09-03, GOLDEN CP6 COL, $50.000 pedidos → $5.000.000 puestos.
- [ ] Todo creado **PAUSED**. Resumen mostrado (objetivo/público/presupuesto/evento/creativos).
- [ ] Activación **solo con OK explícito** del usuario. Se le recordó que activar = gasto real.
- [ ] Reglas CBO/ABO respetadas (no budget en campaña Y conjunto a la vez).

## Entrega
- [ ] Guardado en `PROYECTOS/<PRODUCTO>/ADS/` (`DIAGNOSTICO.md` / `TEST-PLAN.md` / `META-ADS.md`...).
- [ ] Cada afirmación de métrica con su fuente (MCP/informe). Nada inventado.
