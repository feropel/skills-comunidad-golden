# Changelog — GOLDEN ADS

## G4.6 — 2026-07-27 — CORRECCIÓN DE FONDO: Golden NO es solo contra entrega
Corregido por FER, que aclaró que además del catálogo COD tiene **marcas propias con pago
anticipado** — clientes que ya conocen el portal y pagan directo. La skill asumía COD en todo:
**72 menciones a contra entrega contra 1 a pago anticipado** (medido antes del arreglo).

**El error que producía, con números.** Mismo producto, margen bruto 54.900:
COD al 65% de entrega → breakeven CPA Meta **35.685**. Pago anticipado → **54.900**.
Una campaña con CPA 43.000 **pierde en COD y gana en pago anticipado**. Aplicar la fórmula COD a
una marca propia bajaba el techo un 54% y hacía **pausar campañas rentables**.

Cambios: `12-unit-economics.md` abre con la tabla comparativa de los dos modelos y trae las dos
fórmulas separadas más el ejemplo lado a lado (incluye comisión de pasarela y cuotas sin interés,
que solo existen en prepago) · `07-benchmarks-kpis.md` corrige que **`InitiateCheckout` sí existe
en pago anticipado** y es la mejor señal temprana (antes afirmaba en seco que no existe, cierto
solo en COD con Releasit) · regla de oro 9 reescrita: preguntar el modelo de pago ANTES de calcular ·
el rol del SKILL.md ya no dice "e-commerce COD LatAm" a secas.

## G4.4 — 2026-07-18 — ACLARACIÓN: la data/histórico es la EXCEPCIÓN; producto nuevo = Modo B por default
Ajuste ADITIVO fino (autorizado por el dueño; solo aclara, no borra ni desoptimiza). Las secciones de G4.3
sobre "cruzar con data de pedidos" (`01 §D`) y "segmentar por comprador real" (`16 §C`) podían leerse como
si SIEMPRE fuera a existir histórico. Se marcan explícitamente como CONDICIONALES:
- **Nota nueva al inicio de `01-fuentes-datos.md` §D** y de **`16-segmentacion.md` §C**: "Aplica SOLO si hay
  data real/histórico (la excepción: producto ya vendido o relanzamiento a otro país). Para producto NUEVO
  sin datos — el caso normal — el default es **Modo B (testeo)** y NO se pide ni se asume métricas."
- Título de `01 §D` suavizado: "Cruza SIEMPRE con la data de PEDIDOS" → "Cuando HAYA data de PEDIDOS, cruza".
- **La lógica Modo A / Modo B existente NO se tocó** (ya estaba bien). Sello `GAE_VERSION` → **G4.4**.

## G4.3 — 2026-07-18 — Aprendizajes de campo Le'côterra (COD cuidado personal, Colombia)
Horneados 6 aprendizajes de un caso real, todos ADITIVOS (nada se reescribió ni se quitó):
- **`16-segmentacion.md` (§C nueva)**: segmentar por el **COMPRADOR REAL** de cada creativo/producto, no
  por la etiqueta ni "abierto a ciegas"; **fondear todos los segmentos** (el error caro es subfinanciar
  uno y decir "no funciona"). Caso: la cuenta marcaba "90% mujeres" solo por correr puro Vanilla; el
  comprador real era Vanilla 76% M, Bergamot 90% H, Athletix 50/50.
- **`01-fuentes-datos.md` (§D nueva)**: la demografía de la cuenta está contaminada (self-fulfilling) →
  **cruzar SIEMPRE con la data de PEDIDOS** (Dropi/Chatea/CRM, vía `golden-dropi-analisis`): género por
  nombre, mezcla de producto, combo attach, geo, entrega por transportadora. El pedido manda sobre la impresión.
- **`08-creativos-testeo.md` (§3 ampliada + §6 nueva)**: rankear creativos por **compras y ROAS, nunca por
  CTR ni gasto** (el mayor CTR dio ROAS 1,95; el campeón real ROAS 2,78 no era el de mejor CTR). Y **ruteo
  video→destino**: video de 1 producto → su variante (combo de refuerzo); video de línea/dúo → combo primero.
- **`07-benchmarks-kpis.md` (sección de edad nueva)**: patrón COD LatAm cuidado personal — 18–24 el más
  flojo (cortar), **25–44 el núcleo**, 45–54 aceptable, 55+ buen ROAS poco volumen. Arrancar 25–44.
- **`12-unit-economics.md` (2 secciones nuevas)**: **combo = palanca de rentabilidad** (con flete fijo la
  unidad suelta pierde; empuja combo si el attach es ~1,0–1,1) y **entrega por transportadora** cambia el
  breakeven (Envia 11,6% dev < Veloces 18,2% < Interrapidísimo 23,7% → enrutar a la de menor devolución).
- Sello → **G4.3**.

## G4.2 — 2026-07-09 — Auditoría A-Z + playbook de SEGUIMIENTO post-lanzamiento
Auditoría completa de los 23 archivos (pedida por el usuario: "revisa la skill y mejora"):
- **`20-seguimiento.md` (NUEVO)**: el hueco que faltaba — la skill sabía crear y diagnosticar pero no
  tenía el ritmo post-activación. Calendario día 0 (checklist técnico) / día 1 (señales rápidas:
  CTR/hook/CPC) / día 2–3 (corte de embudo, arreglar el eslabón no la campaña) / día 4–7 (primer
  veredicto con semáforo vs breakeven) / semanal (3 listas + fatiga + activity log). Cuándo tocar y
  cuándo NO (aprendizaje), escalado 20–30% vertical/horizontal, rutina MCP, y "nunca" de seguimiento.
  Enlazado en description (triggers "ya la activé, qué miro"), mapa de archivos y checklist de cierre.
- **Fixes de la auditoría**: sello visible sincronizado (decía G3.9/2026-06-25 siendo G4.1 — el texto
  visible quedó atrás dos versiones); reglas de oro reordenadas (13 aparecía antes que 12; números
  intactos para no romper "REGLA #13"); description apuntaba al `18` para columnas → ahora GOLDEN PRO
  (`19`) es el oficial también en el disparador. Sello → **G4.2**.

## G4.1 — 2026-07-02 — 🚀 Replicación GOLDEN PRO por URL (validada en vivo en CP1/CP5/CP6)
Descubierto y ejecutado EN VIVO: Ads Manager acepta `columns=<lista de campos en orden>` en la URL.
- **`19-golden-pro-preset.md` + URL MAESTRA**: pegar la URL cambiando `act=<ID>` aplica las 40 columnas
  en el ORDEN EXACTO del embudo en cualquier cuenta; luego "Guardar como valor predefinido" (3 clics).
  Adiós al marcado manual y a los arrastres (que eran in-automatizables a larga distancia).
- **Diccionario de tokens** horneado: las 9 custom de negocio con su `custom_derived_metrics:<id>` +
  los tokens estándar (omni_purchase, unique_website_ctr:link_click, quality_score_*, video_p50/75/100…).
- **Truco para extraer la URL de cualquier vista**: eliminar/mover UNA columna por el menú del encabezado
  → la URL se reescribe con el columns= completo. El menú ▾ también permite "Mover a la izquierda/derecha"
  (ordenar sin arrastrar).
- **Hallazgos honestos**: `column_preset=<id>` NO viaja entre cuentas (preset = por cuenta); `columns=` SÍ.
  El preset viejo de CP1 tenía el orden revuelto + 2 columnas extra (Acciones, Interacción con la página)
  y le faltaban 5 (CTR único, costo por vis./carrito, y las que Meta omitió) → se reconstruyó perfecto
  desde la URL y se re-guardó como GOLDEN PRO (nuevo id). Replicado: CP1, CP5, CP6 (ids en `19`).
  Sello → **G4.1**.

## G4.0 — 2026-07-02 — 🚦 Semáforo de metas por métrica + guía imprimible GOLDEN PRO v1.1
Nace del entregable real pedido por el usuario (guía .docx/.pdf de las 40 columnas):
- **`19-golden-pro-preset.md` + sección 🚦 SEMÁFORO DE METAS**: umbral 🟢/🔴 por métrica (CPA < breakeven
  = escalar · Frecuencia <2/>3 · CTR >1%/<0.5% · carga >80%/<60% · conv compras >1–2% · Hook >25%/<15% ·
  Hold >20%/<10% · rankings ≥ promedio · FTIR alto/bajando · compras ≥15–30 para decidir). Honestidad:
  CPM/CPC sin umbral universal (histórico propio); alcance/impresiones/carritos = contexto de embudo.
  Umbrales = punto de partida COD LatAm, calibrar con datos reales de la cuenta cuando haya volumen.
- **`02-diagnostico.md`**: el diagnóstico del embudo (Modo A) ahora usa ese semáforo como vara de cada
  escalón — deja de ser juicio a ojo.
- **Receta del doc imprimible** horneada en `19` (tabla 7 col: # · ES · EN · Tipo · Fórmula · Meta
  objetivo · Qué mide; custom en dorado, metas en verde) — generado real en Desktop (.docx + .pdf v1.1).
- **`SKILL.md`**: GOLDEN PRO promovido a preset ÚNICO oficial en la ruta "a pedido" y añadido al mapa
  de archivos (faltaba). Sello → **G4.0**.

## G3.9 — 2026-06-25 — GOLDEN PRO: preset único construido EN VIVO (Hook/Hold rate creadas)
El usuario decidió un solo set con TODAS las métricas (web + WhatsApp) llamado **GOLDEN PRO**, en orden
de embudo (decisión primero → diagnóstico). Construido en vivo en CP1:
- **`references/19-golden-pro-preset.md`** (NUEVO): el preset definitivo — 5 bloques (gano? → embudo web
  → embudo WhatsApp → creativo/video → subasta) + las fórmulas de todas las métricas custom.
- **Creadas EN VIVO 2 métricas de fórmula** a nivel NEGOCIO (sirven en todas las cuentas): **Hook Rate %**
  (`video 3s ÷ impresiones`) y **Hold Rate %** (`video 100% ÷ video 3s`). Se documentó también la fórmula
  real de FTIR (`Alcance ÷ Impresiones`, creada por el usuario).
- **Orden = decisión primero**: presupuesto/gasto/ventas/CPA/Tasa CPA/ticket/ROAS arriba (para decidir
  escalar), luego el embudo para hallar dónde se cae. Guía de diagnóstico incluida.
- Aprendizaje horneado: el preset es POR CUENTA (replicar = re-marcar; ahora rápido porque las custom son
  de negocio); el MCP no fija columnas (es UI) → se hace por navegador. Sello → **G3.9**.

## G3.8 — 2026-06-25 — FTIR + realidad de presets por-cuenta (auditoría en vivo CP1/CP5/CP6)
Revisadas EN VIVO por navegador 3 cuentas del usuario. Hallazgos absorbidos en `18-columnas`:
- **FTIR añadido al Set Maestro** (faltaba: el PDF de 26 no lo tenía; el preset live FER 2026 sí). FTIR =
  First Time Impression Ratio (frescura vs saturación de audiencia) — clave para escalar COD.
- **Los presets de columnas son POR CUENTA, no se comparten**: CP6=`FER 2026` (32 col, con FTIR),
  CP1=`Fer 2025` (27, sin FTIR), CP5=`GOLDEN 2026`/`GOLDEN 2025`. Nombres inconsistentes y desactualizados.
- **Regla experta nueva**: estandarizar por OBJETIVO de la cuenta (web/COD → Set 1 con FTIR; WhatsApp →
  Set 3 con costo por conversación), mismo nombre en todas, y revisar que esté ACTIVO el preset correcto
  (muchas tienen el viejo puesto teniendo el nuevo — a CP5 se le activó su GOLDEN 2026 sin usar).
- **ROAS pagado COD** aclarado: NO es columna de Ads Manager (necesita % entrega) → cálculo en el análisis.
  Sello → **G3.8**.

## G3.7 — 2026-06-25 — Set Maestro Golden (columnas reales del usuario absorbidas + mejoradas)
El usuario compartió su preset real de Meta ("Metricas Golden.pdf" 09.2025, 26 columnas personalizadas).
Se absorbió como fuente autoritativa:
- **`18-columnas-ads-manager.md`**: nuevo **⭐ SET MAESTRO GOLDEN** = las 26 columnas reales (Tasa de CPA %,
  Ticket promedio, Velocidad de carga, CTR único, Tasa conversión WhatsApp/compras, CPA final, video
  3s/50/100%…) + **6 mejoras** (➕ Hook rate, Hold rate, ThruPlay, Agregar al carrito, Costo por
  conversación WhatsApp, Clasificaciones, ROAS pagado COD), ordenado por embudo.
- **`examples/PRESET-columnas-golden-09.2025.md`** (NUEVO): el preset original tal cual, como referencia.
- **Honestidad clave confirmada en la práctica**: el MCP NO lee ni fija la vista de columnas guardada de
  una cuenta (es UI); las columnas del usuario vinieron de su PDF, no de la API. El preset es el mismo
  para todas sus cuentas (CP1/5/6/8…), así que un PDF cubre todas. Sello → **G3.7**.

## G3.6 — 2026-06-25 — Columnas/métricas como entregable a pedido (NO skill aparte)
Decisión del usuario (le recomendé no duplicar): las columnas/métricas quedan DENTRO de golden-ads como
fuente única (`18-columnas-ads-manager.md`), no una skill separada (evita drift + ambigüedad de disparo).
- Se agregaron **disparadores** en la descripción del SKILL ("dame las columnas", "qué métricas debo
  poner", "configúrame las columnas", "métricas para landing / WhatsApp por objetivo") → genera el
  documento de columnas (3 sets en orden de embudo).
- Pointer en el cuerpo del SKILL. Sello → **G3.6**. (Si algún día se quiere como producto para vender/
  compartir, se haría una micro-skill delgada que LEA de golden-ads, no que copie.)

## G3.5 — 2026-06-25 — Escalera de rentabilidad + columnas por embudo + criterio proactivo
Ideas del usuario, horneadas:
- **Escalera de rentabilidad** en `12-unit-economics.md`: no solo el breakeven suelto, sino "hasta aquí
  es rentable" → CPA máximo, CPA objetivo sano (50–70%), **ROAS objetivo en rango**, y tabla "si tu CPA
  es X, ganas/pierdes Y por venta y con 5/20 ventas/día". Traduce el número a decisión.
- **`references/18-columnas-ads-manager.md`** (NUEVO): las columnas que debe tener cada cuenta en
  **orden de embudo**, en 3 sets: **venta web/COD**, **landing con video** (hook rate/hold/retención) y
  **WhatsApp/mensajes (Chatea PRO → Meta)** (conversaciones iniciadas + costo por conversación + la
  compra que Chatea reporta a Meta por CAPI). Con nombres de Ads Manager + campos MCP. **Honestidad:**
  el MCP NO puede fijar la vista de columnas guardada (es UI) → se entrega el preset para guardar + se
  pueden sacar los datos ya en ese orden. A pedido, genera un documento con los 3 sets.
- **REGLA DE ORO #13 (criterio proactivo)**: opinar y sugerir mejoras como media buyer senior, no
  esperar a que el usuario lo sepa todo. Cableado en `02-diagnostico` (leer en orden de embudo). Sello → **G3.5**.

## G3.4 — 2026-06-25 — Aclarado el rol de los unit economics (breakeven, no P&L)
Pregunta del usuario: "para qué me pides precio/costo? Esto monta/analiza ads, no es ganancia/pérdida."
Tenía razón — se afinó REGLA #2 para no pedir economics de más:
- Los datos de economics sirven SOLO para el **breakeven** (CPA/ROAS máximo rentable = línea de
  pausar/escalar), **NO son un P&L** ni contabilidad.
- **Para dar veredicto** sobre campañas existentes → se necesita (si no, solo ranking relativo).
- **Para montar un test** → NO es bloqueante; se marca `[PENDIENTE]` y se sigue.
- Aplicado en `reglas-de-oro.md` (REGLA #2), `SKILL.md` y cabecera de `12-unit-economics.md`. Sello → **G3.4**.

## G3.3 — 2026-06-25 — Libreto de video, informe sin-MCP, y regla de significancia
Tres refuerzos pedidos por el usuario:
- **Libreto de video segundo a segundo** en `15-creativos-produccion.md`: cuando no hay media, además
  del prompt de imagen se entrega un LIBRETO ultra-detallado (tabla 0–3s hook / 3–8s problema / 8–15s
  producto+cómo actúa / 15–22s prueba / 22–28s oferta+garantía COD / 28–35s CTA) + tomas/b-roll,
  texto en pantalla, 3 variantes de hook, compliance. No un "guion vago".
- **`references/17-entrega.md`** (NUEVO): dos modos de entrega. CON MCP → montar en pausa. SIN MCP
  (cuenta ajena / cliente externo / solo quiere el plan) → **INFORME FULL copia-pega-able** (`META-ADS.md`)
  con campaña/conjunto/anuncio campo por campo, valores exactos, ejecutable por alguien que no sabe de
  pauta. Mismo rigor que montarlo nosotros.
- **REGLA DE ORO #12 (significancia)** + sección 0 en `02-diagnostico`: las métricas son un punto de
  dato, NO verdad absoluta. Sin volumen (≥2–3× CPA de gasto, ≥15–30 compras, ≥3–4 días) = señal
  temprana, no veredicto → basarse en lo que de verdad convertiría (histórico amplio + investigación +
  CTR/hook rate/CPC). Reportar nivel de confianza por campaña.
- SKILL.md: sección "Entregar/Publicar" con los 2 modos; file list; sello → **G3.3**.

## G3.2 — 2026-06-25 — golden-ads produce creativos+copys, y segmenta por histórico
Aclarado y horneado el flujo de montaje (Modo B) que pidió el usuario:
- **`references/15-creativos-produccion.md`** (NUEVO): golden-ads **SÍ hace los copys** (con
  `golden-copywriting` de motor). Árbol de decisión: (A) el cliente tiene media → **analizarla**
  (imágenes se leen; videos con `video_analysis_create`/`virality_predictor`) y escribir copys desde
  ahí; (B) no tiene pero tenemos APIs → **generar** imagen/video (Higgsfield/`golden-ugc-avatar`, producto
  fiel) y luego los copys; (C) sin saldo → **prompts perfectos** + slots. Copy = 5 hooks/5 títulos/5
  descripciones por creativo, emparejados a la pieza. El copy se escribe DESPUÉS de ver el creativo.
- **`references/16-segmentacion.md`** (NUEVO): sin histórico → recomendar (Advantage+ + persona); **con
  histórico → basar la segmentación en QUIÉN COMPRA** (sexo/edad/ubicación/plataforma) leyendo los
  `breakdowns` del MCP (`gender`/`age`/`region`/`publisher_platform`/`platform_position`) sobre
  **compras**, no impresiones, + Custom Audience de compradores y su Lookalike.
- SKILL.md: Modo B y Publicar ahora dicen que los creativos/copys los produce este skill; file list y
  sello → **G3.2**.

## G3.1 — 2026-06-25 — Higiene de la fase de aprendizaje (lección de un caso real)
El usuario contó que en CP8 puso una regla que **apagaba la campaña al gastar $35.000**; cada
apagado/encendido **reiniciaba el aprendizaje** y le encareció todo (luego borró las campañas). Se
horneó esa lección para que la skill lo detecte y lo evite:
- **`references/14-fase-aprendizaje.md`** (NUEVO): qué es la fase de aprendizaje, qué la reinicia
  (apagar/prender, saltos de presupuesto >20–30%, editar conjunto), la alternativa correcta
  (**tope de presupuesto / `campaign_spend_cap`**, NO apagados), y cómo **detectarlo en el activity log**.
- **Nueva REGLA DE ORO #11**: controla el gasto con TOPES, no con apagados.
- Cableado: `02-diagnostico` (revisar activity log por churn de encendido/apagado), `11-mcp-meta-recipe`
  (bandera de reinicios de aprendizaje), `03-build-con-metricas` (pausa definitiva, no en bucle; higiene
  antes de tocar presupuestos). Sello `GAE_VERSION` → **G3.1**.

## G3.0 — 2026-06-25 — VALIDADA EN VIVO (cuenta Meta real) + 4 refuerzos horneados
Estrenada contra una cuenta Meta real (COD, COP) por MCP en solo-lectura. El rodaje destapó fallos y
aprendizajes que se hornearon para llevar la skill hacia 1000/1000:
- **`references/11-mcp-meta-recipe.md`** (NUEVO): receta exacta de lectura por MCP + **chuleta de
  campos válidos** (compras = `actions:omni_purchase`, ROAS = `purchase_roas`, `results`/`cost_per_result`
  — NO `purchases`/`cost_per_purchase`, que tumbó una llamada real). Incluye orden de tools, parseo del
  formato real (montos con moneda, `results` anidado, "Not available"), y banderas (nombres duplicados,
  ROAS sin señal, cuentas DISABLED/UNSETTLED).
- **`references/12-unit-economics.md`** (NUEVO): calculadora de **breakeven COD** con la regla clave
  descubierta — **ROAS de Meta ≠ ROAS pagado**: `ROAS pagado ≈ ROAS Meta × tasa de entrega` (~55–75%);
  `CPA real = CPA Meta ÷ entrega`. Fórmulas + ejemplo. Nueva REGLA DE ORO #9.
- **`references/13-auto-check.md`** (NUEVO): checklist ejecutable de cierre (no entregar sin economics,
  sin ROAS pagado, con campo inválido, con moneda asumida, o activando sin OK).
- **`examples/EJEMPLO-diagnostico.md`** (NUEVO): diagnóstico modelo (caso real anonimizado CP8) = el
  estándar de cómo se ve una entrega (economics → semáforo vs breakeven → 3 listas → banderas).
- **Nuevas reglas de oro**: #2b (ROAS pagado COD), #9 (ROAS Meta ≠ pagado), #10 (verificar campos MCP +
  respetar moneda). SKILL.md (Paso 0 apunta a la receta; cierre corre el auto-check) y `02-diagnostico`
  actualizados. Sello `GAE_VERSION` → **G3.0**. Skill ahora **validada en vivo**, no solo teórica.

## G2.0 — 2026-06-25 — Rename a `golden-ads` + Meta/TikTok/Google completos + full-funnel
- **Renombrada** `golden-ads-estratega` → **`golden-ads`** (carpeta + `name:` + sello). Pedido del usuario.
- **Alcance a 3 plataformas**: Meta (MCP en vivo), **TikTok** (`09`) y **Google** (`10`) — estas dos
  report-based (no hay MCP en vivo), entregando configuración exacta para pegar en el gestor.
- **+ `06-retargeting-fullfunnel.md`**: embudo completo TOF/MOF/BOF + carrito abandonado + DPA/catálogo
  con exclusiones por etapa (el hueco #2 del diagnóstico 80/100).
- **+ `07-benchmarks-kpis.md`**: tabla de umbrales por etapa (CTR/CPM/CVR/frecuencia/CPA/ROAS) + reglas
  de matar/escalar escritas antes de lanzar.
- **+ `08-creativos-testeo.md`**: matriz ángulo×hook, lectura de ganadores por retención, fatiga y refresco.
- **SKILL.md**: Paso 1 (elegir plataforma), **checklist de cierre**, convención de entrega
  `PROYECTOS/<PRODUCTO>/ADS/` (regla de oro #8). Sello `GAE_VERSION` → **G2.0**. Blindada (chflags uchg).
- Verificado anti-duplicado: análisis de Excel sigue en `golden-meta-ads-analysis`; lanzamiento 360°
  en `golden-investigacion-mercado`; esta skill = media buying / optimización / publicación.

## G1.0 — 2026-06-25 — Versión inicial (Centro de Comando de Pauta)
Skill nueva, exclusiva de ads, separada del orquestador 360° (`golden-investigacion-mercado`).
- **Detección de fuente de datos** (Paso 0): conexión EN VIVO a Meta por MCP (preferida), informe
  Excel/CSV exportado (delega en `golden-meta-ads-analysis`), o sin datos (producto a testear).
- **Modo A · CON métricas**: diagnóstico con datos reales (unit economics + breakeven, semáforo,
  tendencia, anomalías, benchmarks de industria y subasta, opportunity score, activity log) →
  veredicto QUÉ PAUSAR/ESCALAR/AJUSTAR → reestructura/optimización con calendario de escalado.
- **Modo B · SIN métricas**: estructura de testeo (1 campaña, N conjuntos = N ángulos, público amplio
  Advantage+, 2–3 creativos, ABO) + criterios de matar/escalar definidos ANTES de lanzar.
- **Publicar por MCP**: crear campaña/conjunto/creativo/anuncio/públicos/A-B test EN PAUSA con reglas
  CBO/ABO, evento de conversión y pixel; activar SOLO con confirmación del usuario.
- **Reglas de oro**: no inventar métricas, unit economics primero, confirmar antes de gastar,
  compliance, país/moneda, no solapar audiencias.
- Verificado contra el MCP de Meta real conectado (server con `ads_get_ad_accounts`, `ads_insights_*`,
  `ads_create_*`, `ads_activate_entity`, etc.).
- Playbooks: reglas-de-oro · 01-fuentes-datos · 02-diagnostico · 03-build-con-metricas ·
  04-build-sin-metricas · 05-publicar-mcp.
