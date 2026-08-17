# Modo A — Optimizar / reestructurar desde los datos

Del diagnóstico (`02`) salen 3 listas. Aquí se ejecutan, en orden de impacto y riesgo.

## 1. Cortar pérdidas (🔴 PAUSAR) — primero, libera presupuesto
- Pausa conjuntos/anuncios que gastaron ≥ 1–2× CPA objetivo sin compra, o con CPA > breakeven sostenido.
- Pausa creativos fatigados (frecuencia alta + CTR cayendo + CPA subiendo).
- Consolida conjuntos con **overlap de subasta** (compiten entre sí) en uno solo.
- **Pausa DEFINITIVA, no en bucle.** Matar = apagar una vez lo que ya perdió. Prohibido reglas que
  apaguen/prendan por umbral de gasto (reinician el aprendizaje y encarecen — REGLA 11, `14`).

## 1b. Higiene de aprendizaje (antes de tocar presupuestos)
- Si el diagnóstico halló **churn de encendido/apagado** o reglas de "apagar al gastar X": quítalas y
  reemplázalas por **tope de presupuesto / `campaign_spend_cap`**. Deja correr para salir de learning.
- Control de gasto = TOPES, no apagados. Detalle en `14-fase-aprendizaje.md`.

## 2. Escalar ganadores (🟢) — con cuidado de no resetear aprendizaje
- Sube presupuesto del ganador **20–30% cada 2–3 días** (subidas bruscas reinician el learning).
- Duplica el ganador a CBO / Advantage+ Shopping para darle más subastas.
- Abre **Lookalike de compradores** (`ads_create_custom_audience` subtype LOOKALIKE, ratio 1–3%)
  a partir del público de compra. Mantén un conjunto amplio (Advantage+) corriendo en paralelo.
- Refresca creativos del ganador (mismas pruebas de ángulo que funcionaron, nuevas variantes).

## 3. Optimizar los 🟡 (límite) antes de matarlos
- **Creativo**: nuevo hook/ángulo (de los que ganan), mejor primeros 3s, formato video si era imagen.
- **Segmentación**: probar Advantage+ Audience si estaba en público estrecho, o acotar si era ruido.
- **Puja/optimización**: corregir evento de conversión (optimizar a Compra, no a clics), revisar
  ventana de atribución, pasar de límite de costo a "highest volume" si ahogaba la entrega.
- **Ubicaciones**: apagar las de bajo rendimiento si manual; o pasar a Advantage+ Placements.

## 4. Higiene de señal (a menudo el mayor arreglo)
- Verifica **Pixel + CAPI** (Conversions API) activos y el evento de Compra disparando bien. Sin
  señal limpia, ninguna optimización pega. (Eventos de pixel: `ads_pixel_event_*` por MCP.)
- Revisa atribución (7-day click / 1-day view) y dominio verificado (AEM).

## 5. Plan de reestructura (entregable)
Documento `ADS-OPTIMIZACION.md` con:
- Acciones inmediatas (pausar X, escalar Y a $Z, consolidar A+B).
- Nueva estructura propuesta (campañas/conjuntos/anuncios) con su porqué.
- Calendario de escalado (subidas %/días) y umbrales de re-evaluación.
- Si el usuario aprueba ejecutar en vivo → `05-publicar-mcp.md` (todo en pausa, activar con OK).
