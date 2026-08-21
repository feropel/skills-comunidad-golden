---
name: golden-meta-ads-analysis
description: >-
  Diagnóstico ejecutable de un EXCEL o CSV exportado del Administrador de anuncios de Meta, con
  unit economics en COP: ranking de campañas y creativos, demografía, plataformas, ubicaciones,
  landings, benchmarks por objetivo y plan de acción campo por campo. Aplica a marca propia,
  dropshipping, contra entrega, pago anticipado y mixto.

  EL DISPARADOR ES EL ARCHIVO: úsala cuando el usuario suba o comparta un Excel, un CSV, un
  informe de pauta exportado o un reporte del Ads Manager, y diga "analiza estos resultados" o
  "revisa mi CPA / ROAS / breakeven" sobre ese archivo.

  DIAGNOSTICA y recomienda; no monta, no publica y no ejecuta cambios. Sin archivo de por medio,
  las preguntas sobre la cuenta en vivo entran por golden-ads, que es el centro de comando y
  delega aquí cuando lo que hay sobre la mesa es un export.
---

# Golden Group — Análisis de Meta Ads

**Versión:** `GMA1.1` · **Última modificación:** 2026-08-21 (auditoría golden-skill-auditor: CSV soportado + limpieza) · versión declarada el 2026-08-19 por el Centro de Mando para que el censo diario pueda detectar ediciones

<!-- 2026-08-07 · DESCRIPCIÓN RECORTADA: superaba el tope de ~1.536 caracteres del listado de skills y se estaba TRUNCANDO, así que las frases del final NO disparaban. Medido antes/después: 1565 → 821 chars. Lo que se movió al cuerpo son rutas de references y explicaciones; se conservaron y ampliaron las frases reales del usuario, que son lo que dispara. -->
<!-- adenda 2026-08-20 (centro de mando, autoevalúo del ecosistema): resuelta la contradicción tarjeta/cuerpo — la description declara EL DISPARADOR ES EL ARCHIVO y el cuerpo ordenaba empezar SIEMPRE en vivo, ignorando el archivo que el usuario trajo. Regla nueva: con archivo sobre la mesa, el archivo manda y el vivo se ofrece como contraste; sin archivo, vivo. Coherente con la frontera declarada por golden-ads. -->
<!-- skill v1.1 · 2026-08-21 · auditoría golden-skill-auditor: (1) 🔴 CSV realmente NO cargaba — analyze_meta_report.py solo usaba openpyxl/read_excel pese a que description y SKILL.md prometen "Excel o CSV"; agregado _load_csv_report() con detección de encoding/header, probado en vivo (CSV + XLSX corren el mismo pipeline sin error, incluida la generación del .docx); (2) corregida la línea que decía "Modo EN VIVO (camino por defecto)" contradiciendo "EL DISPARADOR ES EL ARCHIVO" de la description y la propia sección 1B; (3) movidas las Reglas duras COD Colombia y los Análisis adicionales de valor a references/reglas_duras_colombia.md (SKILL.md bajó de 506 a 449 líneas, bajo el tope de 500); (4) corregido el docstring de analyze_meta_report.py que decía "6 capas" — el script automatiza 4, las capas 5-8 se calculan inline y ahora lo dice; (5) assets/report_template.md no reflejaba generate_report.py real (P&L histórico era subsección 1.4 y es sección propia "2.", faltaba "Ranking de Campañas" y "Embudo de conversión", y "KPIs de monitoreo" no existe como sección aparte) — reescrito para calzar con el código; (6) eliminado .gitignore suelto en la raíz (material intruso detectado por el inventario del auditor). -->

Método estándar de Golden Group para analizar informes de Meta Ads de cualquier producto y modelo de negocio. Produce diagnósticos accionables con configuración exacta de campañas nuevas.

---

## 1. CUÁNDO USAR ESTE SKILL

- El usuario sube o comparte un archivo Excel (.xlsx) o CSV exportado de Ads Manager (**Modo ARCHIVO** — manda cuando hay archivo sobre la mesa, ver sección 1B)
- El usuario quiere **conectar su cuenta de Meta y que bajes los informes tú** sin traer archivo (**Modo EN VIVO** — el camino cuando no hay archivo, ej. llegaste por derivación de `golden-ads`)
- Pide analizar campañas, revisar performance, entender qué pausar o escalar
- Menciona CPA, CPL, ROAS, costo por conversación, creativos, segmentación, demografía, plataformas, landings
- La campaña NO es de ventas (leads, mensajes, reconocimiento) — se usan benchmarks por objetivo + 3 Q's
- Quiere replicar campañas en otras cuentas publicitarias o Business Managers
- Pregunta sobre unit economics, margen, breakeven de un producto
- Frases conversacionales como "por qué no funcionan mis anuncios", "qué pauso", "qué escalo"

**Frontera con golden-ads:** esta skill DIAGNOSTICA (lee y recomienda). Para MONTAR, ejecutar o gestionar pauta en vivo (crear campañas, cambiar presupuestos, activar/pausar por MCP) → `golden-ads`.

---

## 1B. CÓMO ENTRAN LOS DATOS — EN VIVO por defecto, ARCHIVO de respaldo

El motor de análisis (unit economics, capas, veredicto, Word) es idéntico: solo cambia de dónde salen los números. **El archivo manda cuando hay archivo:** si el usuario trajo un Excel/CSV, ese archivo es el disparador y su expectativa — se analiza EL ARCHIVO, y el modo en vivo se OFRECE como contraste de frescura si hay MCP disponible. Solo cuando no hay archivo de por medio (llegaste por derivación de golden-ads) se empieza por el modo en vivo.

### ✅ Modo EN VIVO (por defecto) — extracción directa de la Meta Marketing API
El usuario no exporta nada: tú traes los datos con los scripts `fetch_*.py`. Al inicio, ofrécelo así:
> "Puedo conectarme a tu cuenta de Meta y bajar los informes yo mismo (solo-lectura, no toco nada de tu pauta). Necesito un Access Token de solo lectura una sola vez. Lo generamos o ya tienes uno?"

**🔒 PASO DE SEGURIDAD OBLIGATORIO — antes de bajar cualquier dato:**
1. Guarda el token en `.env` (`META_ACCESS_TOKEN=...`).
2. Corre **`python3 scripts/check_token.py`**. Este preflight consulta `/debug_token` de Meta y **ABORTA si el token tiene permiso de escritura** (`ads_management`), si expiró, o si le falta `ads_read`. NO continúes con ningún `fetch_*` hasta que este chequeo pase con "✅ Token solo-lectura verificado".
3. Si aborta, guía al usuario a regenerar el token con SOLO `ads_read` + `business_management` (ver `references/extraccion_en_vivo.md`).

Con el token ya verificado, sigue el flujo completo de `references/extraccion_en_vivo.md` (negocios → campañas → insights → adsets → anuncios, con auto-detección de tipo). Luego entras al MISMO motor: si es `ventas` COD sigues desde el Paso 2 (unit economics); si es otro objetivo usas `references/benchmarks_por_objetivo.md`.

### 🗂️ Modo ARCHIVO (respaldo) — Excel/CSV exportado
Úsalo cuando: el usuario ya trae el archivo y lo prefiere, no tiene acceso API, tiene rol restringido en la BM, o el API falla (token vencido, rate limit, cambio de versión). Es el modo más seguro (cero credenciales). El usuario sube el archivo y sigues el workflow de la sección 4 desde el Paso 1.

> **Por qué el archivo se queda:** es la red de seguridad sin credenciales. Nunca lo presentes como el camino principal, pero nunca lo quites — garantiza que la skill funcione para todos y en cualquier condición.

**Método de las 3 Q's (marco narrativo del diagnóstico, ambos modos):** 1️⃣ Qué pasó? (resultado vs objetivo/breakeven) · 2️⃣ Por qué pasó? (embudo + calidad, señala el paso más débil) · 3️⃣ Qué haremos? (en COD = qué pausar / qué escalar / cómo configurar y replicar). Detalle y tablas por objetivo en `references/benchmarks_por_objetivo.md`. Basado en el trabajo de Felipe Vergara.

**Antes de recomendar pausar cualquier adset o anuncio** (cualquier modo) aplica SIEMPRE `references/efecto_desglose.md` — evita romper el aprendizaje del algoritmo.

---

## 2. PRINCIPIOS IRRENUNCIABLES

1. **Sin unit economics no hay análisis.** Antes de juzgar cualquier CPA, el modelo financiero del producto debe estar claro. Si el usuario no lo da, preguntar con `ask_user_input_v0`.

2. **Todo el output en pesos colombianos (COP).** Si el informe está en USD (cuenta publicitaria en dólares), convertir a COP antes de presentar nada. Nunca mostrar cifras en USD en el análisis ni en el Word. Ver Paso 1.5 para el flujo de conversión.

3. **Español directo, sin filler.** Sin "espero que te ayude", sin separadores visuales (═══, ───), sin "podrías considerar". Decisiones, no sugerencias. No usar "cópialo y pégalo".

4. **Conservar nombres exactos.** Nunca parafrasear ni abreviar el nombre de campañas, adsets o anuncios. Copiarlos tal como están en el archivo, incluyendo emojis (✅, ❌), espacios y mayúsculas.

5. **Responder 3 preguntas.** Qué pausar hoy? Qué continuar y escalar? Cómo configurar las campañas nuevas y replicarlas?

6. **El P&L histórico real siempre.** Es la métrica más importante — dice si la cuenta ganó o perdió plata real, no solo si el ROAS se ve bien.

7. **No claims médicos en cosméticos.** Nunca recomendar "trata", "cura", "elimina" — usar "ayuda a", "mejora", "suaviza".

8. **Cada análisis es independiente.** No comparar entre productos a menos que el usuario lo pida explícitamente. Cada Excel = análisis nuevo.

---

## 3. NOMBRE DEL ARCHIVO DE SALIDA

```
Analisis de [Nombre del producto] [YYYY-MM-DD].docx
```

`[YYYY-MM-DD]` = fecha en que se corre el análisis (no la del informe).

Ejemplo: `Analisis de Serum 7 Days 2026-05-12.docx`

Nunca incluir "versión corregida", "v2", "actualizado", "final" en el nombre.

La función `build_output_filename(producto)` en `scripts/generate_report.py` genera este nombre.

---

## 4. WORKFLOW DEL ANÁLISIS (9 pasos)

> **Nota de entorno (portabilidad).** Los helpers `ask_user_input_v0`, `present_files` y las rutas `/mnt/user-data/uploads` · `/mnt/user-data/outputs/` son del runtime de claude.ai. En **Claude Code / local** usa el equivalente: pregunta directamente en el chat, lee el archivo desde la ruta donde el usuario lo tenga (o el directorio de trabajo), guarda el `.docx` en el directorio de trabajo y comparte la ruta con un enlace. El resto del workflow es idéntico en ambos entornos.

### Paso 1 — Inspeccionar el archivo

Al recibir el Excel, usar `scripts/analyze_meta_report.py`:

```python
from analyze_meta_report import load_meta_report, detect_currency
df = load_meta_report("/mnt/user-data/uploads/archivo.xlsx")
moneda, col_gasto = detect_currency(df)
```

Detectar automáticamente:
1. Hojas disponibles (`Creative Reporting`, `Raw Data Report`, `Formatted Report`)
2. Fila real de headers (puede ser 0, 1, 2 u 8)
3. Columnas presentes
4. Moneda: `Importe gastado (COP)` vs `Importe gastado (USD)`
5. Niveles de entrega: campaña / adset / anuncio
6. Desgloses presentes: Edad, Sexo, Plataforma, Ubicación, URL de destino
7. Periodo: `min(Inicio del informe)` → `max(Fin del informe)`
8. Conteo: campañas únicas, adsets únicos, anuncios únicos
9. Marcadores del equipo en nombres: ✅ ❌ 🔥 ⭐
10. Total invertido y total compras

Leer `references/file_formats.md` para los distintos formatos.

**Reportar al usuario qué desgloses tiene y qué le falta:**
- ✅ / ❌ Desglose por edad y sexo
- ✅ / ❌ Desglose por plataforma
- ✅ / ❌ Desglose por ubicación
- ✅ / ❌ URL de destino del anuncio

### Paso 1.5 — Conversión USD → COP (si aplica)

**Si la moneda detectada es USD**, antes de cualquier cálculo:

1. **Intentar consultar la TRM real del día con `web_search`** usando query como "dólar a peso colombiano hoy" o "TRM Colombia hoy".

2. **Pasar el valor a `scripts/trm_resolver.py`**:
   ```python
   from trm_resolver import resolve_trm, convertir_dataframe_usd_a_cop

   # Si pudiste consultar:
   trm = resolve_trm(valor_de_web_search=4180)  # el valor que sacaste

   # Si NO pudiste (sin internet, tool no disponible):
   trm = resolve_trm()  # usa fallback $4,000 COP/USD

   # Si el usuario explícitamente dio la TRM:
   trm = resolve_trm(valor_provisto_usuario=4150)
   ```

3. **Mostrarle al usuario qué TRM se aplicó** usando `trm["mensaje_usuario"]`. Especialmente importante cuando es fallback — el usuario debe saber que NO es la tasa del día.

4. **Convertir todas las columnas monetarias del DataFrame**:
   ```python
   convertir_dataframe_usd_a_cop(df, ["Importe gastado (USD)", "CPC", "CPM"], trm)
   ```

5. **Renombrar columnas** para que digan COP en todo el reporte.

**NUNCA mostrar USD en el output final**, ni siquiera entre paréntesis. Todo va en COP.

### Paso 2 — Capturar unit economics

Si el usuario no proveyó los datos económicos, preguntarlos con `ask_user_input_v0` (máximo 3 preguntas por turno, hasta 3 turnos). Prioridad:

**Turno 1 — Lo crítico:**
- Precio de venta al cliente?
- Marca propia o dropshipping?
- Costo del producto?

**Turno 2 — Logística:**
- Flete cuando la orden SE ENTREGA?
- Costo cuando devuelven?
- Costo cuando cancelan antes de despacho?

**Turno 3 — Tasas operativas:**
- % cancelación antes de envío
- % devolución sobre despachados
- Producto recuperable? (vuelve a bodega o se pierde)

Si el usuario no sabe, usar referencias Colombia COD:
- Cancelación: 10%
- Devolución: 20% sobre despachados
- Producto recuperable: SÍ
- Flete devolución: $15,000 COP
- Flete cancelación: $0

Leer `references/unit_economics.md` para los 4 escenarios típicos.

### Paso 3 — Calcular CPA breakeven

Usar `scripts/calculate_unit_economics.py`:

```python
from calculate_unit_economics import calculate_unit_economics, print_summary

ue = calculate_unit_economics(
    precio=79900,
    costo_producto=12000,
    flete_entregada=15000,
    flete_fallida=15000,
    tasa_cancelacion=0.10,
    tasa_devolucion=0.20,
    producto_recuperable=True,
    costo_cancelacion=0,
)
print_summary(ue)
```

Reporta CPA breakeven, ROAS breakeven, tabla CPA por margen (5%, 10%, 15%, 20%, 25%, 30%).

### Paso 4 — Análisis estructural en 8 capas

Analizar en este orden estricto (cada capa responde una pregunta distinta). Antes de leer los
resultados, aplica las reglas de campo de `references/reglas_duras_colombia.md` — son el
conocimiento validado que separa un CPA alto normal de uno que hay que apagar.

**Capa 1 — Tipos de campaña.** Agrupar por tipo (VENTA OPEN, ADVANTAGE+, RETARGETING, CATALOG, TRAFICO/CHATEA, etc.). CPA y ROAS de cada tipo. Identificar estructura ganadora. Ver `references/campaign_taxonomy.md`.

**Capa 2 — Creativos (anuncios).** Agrupar por anuncio. Tratar sufijos -HOMBRE/-MUJER/-MIX como variantes separadas. Métricas: CPA, ROAS, CTR, CPC, hold 50%, view 100%, CR clic→compra. Semáforo verde/amarillo/rojo. Identificar 3-5 ganadores absolutos.

**Capa 3 — Demografía (edad × sexo).** Tabla edad × sexo. Identificar núcleo rentable (>15% compras Y CPA < breakeven). Detectar segmentos ocultos rentables. Combos con <5 compras: no concluir.

**Capa 4 — Plataformas y ubicaciones.** Tabla por plataforma (FB, IG, AN, Messenger, Threads) y por ubicación específica (Feed, Reels, Stories, Marketplace, Resultados de búsqueda, AN nativo). Identificar ubicaciones con ROAS sorpresa. Recomendar exclusiones.

**Capa 5 — Landings.** Si el archivo trae URL de destino: agrupar por landing, comparar mismo creativo en diferentes destinos. Si NO trae URL: inferir por nombre del anuncio (`-MIX` → página mix, nombre de producto → landing específica) y preguntar al usuario para confirmar.

**Capa 6 — Tipo de creativo y formato.** Video vs imagen vs carrusel vs catalog. Para videos: hold rate como proxy de calidad del hook. Catalog en frío: pierde.

**Capa 7 — Embudo de conversión.** Tasas: Impresiones → Clics → Visitas LP → Pagos iniciados → Compras. Diagnóstico por etapa. Si trae `Velocidad Carga de la página`, reportarla (<1s excelente, >2s problema).

**Benchmarks Colombia e-commerce Meta:**
| Etapa | 🟢 Verde | 🟡 Amarillo | 🔴 Rojo |
|-------|---------|------------|--------|
| Clic → Visita LP | ≥80% | 65-79% | <65% |
| Visita → Pago iniciado | ≥12% | 8-11% | <8% |
| Pago → Compra | ≥30% | 18-29% | <18% |
| Clic → Compra global | ≥3.5% | 2-3.4% | <2% |

**Capa 8 — Tendencia temporal.** Si los datos cubren >30 días: el CPA está subiendo, bajando o estable? Múltiples versiones de campaña (OPEN 1, OPEN 2, OPEN 3): las recientes mejor o peor? Fatiga creativa. Si no hay datos temporales suficientes, omitir y decirlo.

### Paso 5 — Veredicto

| Símbolo | Veredicto | CPA vs breakeven | Acción |
|---------|-----------|-----------------|--------|
| 🟢 | ESCALAR | < CPA margen 10% | +20-30% presupuesto cada 3 días |
| 🟢 | CONTINUAR | < breakeven | Mantener |
| 🟡 | REVISAR | Breakeven ±15% | Vigilar, no escalar |
| 🔴 | PAUSAR | > breakeven | Pausar si lleva >$120K COP gastados |
| ⚫ | DESCARTAR | >1.5× breakeven | Apagar hoy |

La función `evaluar_cpa(cpa_real, ue)` en `calculate_unit_economics.py` hace este mapeo.

### Paso 6 — Plan de acción

**A. QUÉ PAUSAR HOY.** Tabla: nombre exacto / tipo / razón con cifras / gasto acumulado COP.

**B. QUÉ CONTINUAR Y ESCALAR.** Tabla: nombre exacto / CPA actual COP / presupuesto sugerido COP/día / CPA objetivo / instrucción de escalado.

**C. CONFIGURACIÓN DE CAMPAÑAS NUEVAS — campo por campo.**

```
NOMBRE CAMPAÑA: [Producto] - [TIPO] - [ESTRUCTURA] - [fecha]
OBJETIVO: Ventas (Sales)
TIPO: ASC / OPEN Manual / Retargeting
PRESUPUESTO: $XXX,XXX COP/día
ESTRATEGIA DE PUJA: Mayor volumen de conversiones
PAÍS: Colombia

  ADSET:
    Presupuesto, Público, Sexo, Edad (basado en demografía del archivo),
    País: Colombia — todas las ciudades (no geosegmentar),
    Placements INCLUIR: Feed FB+IG, Reels FB+IG, Stories FB+IG,
                       AN nativo, Resultados de búsqueda FB,
    Placements EXCLUIR: Messenger Inbox, Columna derecha FB,
                       Notificaciones FB, Threads, WhatsApp Status,
                       AN banner, AN intersticial,
    Optimización: Compra,
    Atribución: 7d clic + 1d vista,

    ANUNCIO:
      Formato: Video/Imagen,
      Landing: [URL exacta — basada en Capa 5],
      CTA: Comprar ahora
```

**D. REPLICAR EN OTRA CUENTA DEL MISMO BM.** Pixel, eventos CAPI, creativos a transferir, presupuesto inicial.

**E. REPLICAR EN BM NUEVO.** Verificación BM, dominio nuevo, pixel nuevo, calentamiento 5-7 días.

Ver `references/replication_playbook.md` para los pasos técnicos.

### Paso 7 — Generar el Word

Usar `scripts/generate_report.py` (Python puro con `python-docx`):

```python
from generate_report import generate_word_report, build_output_filename

filename = build_output_filename("Serum 7 Days")  # → "Analisis de Serum 7 Days 2026-05-12.docx"
output_path = f"/mnt/user-data/outputs/{filename}"

cfg = {
    "producto": "Serum 7 Days",
    "periodo": "25 abril - 10 mayo 2026",
    "moneda_original": "COP",        # o "USD" si hubo conversión
    "trm_aplicada": None,             # solo si moneda_original == "USD"
    "trm_fuente": None,
    "totales": {"gasto_cop": ..., "compras": ..., "cpa_promedio": ...},
    "unit_economics": ue,             # del paso 3
    "pyl_historico": pyl,             # de calcular_pyl_historico()
    "campañas_ranking": [...],
    "creativos_ranking": [...],
    "demografia_tabla": [...],
    "ubicaciones_tabla": [...],
    "landings_tabla": [...],          # si aplica
    "embudo": {...},
    "plan_accion": {
        "pausar": [...], "escalar": [...], "campañas_nuevas": [...],
        "replicar_mismo_bm": [...], "replicar_bm_nuevo": [...]
    },
    "sintesis_ejecutiva": [...],
    "produccion_creativa": {...},
}
generate_word_report(cfg, output_path)
```

Cada sección del config es opcional — si falta data, esa sección se omite automáticamente.

Leer `assets/report_template.md` para detalle de cada sección.

Presentar con `present_files`.

### Paso 8 — Resumen en chat

Después del Word, resumen ejecutivo breve:

1. **CPA breakeven** del producto en COP
2. **3-5 hallazgos críticos** con datos exactos
3. **Top 3 acciones inmediatas** (qué pausar, qué escalar, qué crear)
4. **Si hay replicación**, los 3 pasos esenciales

### Paso 9 — Validación final antes de entregar

Antes de cerrar, verificar:

- [ ] Todo el reporte está en COP (cero USD)
- [ ] Si hubo conversión, el reporte dice qué TRM se aplicó y de qué fuente
- [ ] Los nombres de campañas/adsets/anuncios están copiados exactos del Excel
- [ ] El P&L histórico real está calculado y reportado
- [ ] El plan de acción tiene A, B, C completos
- [ ] El nombre del archivo es `Analisis de [Producto] [YYYY-MM-DD].docx`

---

## 5. REGLAS DURAS — VALIDADAS EN COLOMBIA COD

Conocimiento de campo (logística, demografía, campañas, creativos, ubicaciones, landings)
validado en operaciones reales COD en Colombia. Léelo en `references/reglas_duras_colombia.md`
antes del Paso 4 (análisis en 8 capas) y del Paso 6 (plan de acción) — ahí también están las
"Análisis adicionales de valor" (clasificaciones de calidad Meta, producción creativa
recomendada, sensibilidad de margen y palancas de margen).

---

## 6. MANEJO DE INFORMACIÓN FALTANTE

| Situación | Cómo manejar |
|-----------|-------------|
| Informe en USD | Aplicar Paso 1.5: web_search TRM → resolve_trm → convertir → reporte en COP. |
| Sin desglose demográfico | Decirlo. Dar instrucciones de Ads Manager para exportar con desglose. |
| Sin URL de destino | Inferir por nombre del anuncio + preguntar al usuario. |
| Múltiples productos en la cuenta | Separar por producto. Unit economics por separado. |
| Múltiples tickets | Preguntar ticket promedio ponderado. |
| Dropshipping + marca propia | Calcular 2 escenarios en paralelo. |
| <30 compras totales | Analizar con advertencia. Sugerir extender periodo. |
| Marcadores ❌ en nombres | Reportar en Qué pausar con gasto acumulado. |
| Marcadores ✅ en nombres | Priorizar en Qué escalar. |

---

## 7. ANTI-PATRONES (NUNCA hacer)

- ❌ Mostrar valores en USD en el output final
- ❌ Versión corregida, v2, actualizado, final en el nombre del archivo
- ❌ Parafrasear o abreviar nombres de campañas/adsets/anuncios
- ❌ Recomendar Advantage+ sin verificar margen ≥40% primero
- ❌ Separadores visuales (═══, ───)
- ❌ Podrías considerar o sería bueno explorar — dar decisiones
- ❌ Lanzar más creativos para probar sin filtrar por unit economics primero
- ❌ Asumir comportamiento del consumidor sin data — el archivo manda
- ❌ Omitir el P&L histórico real
- ❌ Sacar conclusiones de segmentos con <5 compras sin advertirlo
- ❌ Geosegmentar por ciudad para distribución nacional
- ❌ Asumir TRM fija $4,000 sin intentar primero `web_search`
- ❌ Aplicar claims médicos a productos cosméticos

---

## 8. OUTPUT ESPERADO

1. **Documento Word:** `Analisis de [Producto] [YYYY-MM-DD].docx` en `/mnt/user-data/outputs/`, presentado con `present_files`.
2. **Resumen ejecutivo en chat** con las 3 acciones inmediatas.

Si el usuario pide refinamientos (simplifica tabla, calcula con otro precio, enfócate en un creativo), adaptar sin rehacer todo el análisis.

---

## 9. RECURSOS DEL SKILL

**Scripts — Modo A (análisis de Excel o CSV, requieren pandas/openpyxl/python-docx preinstalados):**
- `scripts/analyze_meta_report.py` — Carga el Excel (.xlsx/.xls) o CSV, detecta formato y fila de header, clasifica campañas, automatiza capas 1-4 (ver docstring del script para el detalle de qué automatiza y qué se calcula inline).
- `scripts/calculate_unit_economics.py` — CPA breakeven, ROAS breakeven, tabla CPA por margen, semáforo, P&L histórico.
- `scripts/trm_resolver.py` — Resuelve TRM USD→COP con fallback. Usar SIEMPRE que la moneda sea USD.
- `scripts/generate_report.py` — Genera el .docx con todas las secciones. `build_output_filename(producto)` da el nombre estándar.

**Scripts — Modo EN VIVO (extracción por API, solo requieren `requests`):**
- `scripts/check_token.py` — **🔒 Preflight de seguridad OBLIGATORIO.** Verifica con `/debug_token` que el token sea solo-lectura; ABORTA si tiene `ads_management`, expiró o le falta `ads_read`. Correr ANTES de cualquier `fetch_*`.
- `scripts/_common.py` — Helpers de la Graph API: carga de `.env`, `api_get()` con paginación y reintentos ante rate limits, formateo.
- `scripts/fetch_businesses.py` · `fetch_campaigns.py` · `fetch_insights.py` (auto-detecta tipo) · `fetch_adsets.py` · `fetch_ads.py` — el pipeline negocios → campañas → insights → conjuntos → anuncios.

**References (consultar según el caso):**
- `references/extraccion_en_vivo.md` — **Modo B**: token System User anti-ban, `.env`, flujo de los `fetch_*` y auto-detección de tipo.
- `references/benchmarks_por_objetivo.md` — Tablas 🔴🟡🟢 por objetivo (ventas, interacción, leads, sitio, reconocimiento) + 3 Q's + fuente única de benchmarks.
- `references/efecto_desglose.md` — Reglas de pausado a nivel adset/anuncio (algoritmo de entrega de Meta). Aplicar SIEMPRE antes de pausar.
- `references/unit_economics.md` — Fórmulas y 4 escenarios típicos (COD, pago anticipado, etc.).
- `references/campaign_taxonomy.md` — Cómo clasificar cada tipo de campaña Meta.
- `references/file_formats.md` — Formatos de exportación de Ads Manager.
- `references/semaforos.md` — Tiers verde/amarillo/rojo y benchmarks.
- `references/replication_playbook.md` — Replicar en otra cuenta / BM nuevo.
- `references/reglas_duras_colombia.md` — Reglas de campo COD Colombia (logística, demografía, campañas, creativos, ubicaciones, landings) + clasificaciones de calidad, producción creativa, sensibilidad y palancas de margen. Leer antes del Paso 4 y del Paso 6.

---

## Créditos

El método de las **3 Q's** (Qué pasó? / Por qué pasó? / Qué haremos?) está basado en el trabajo de **Felipe Vergara** (📺 https://www.youtube.com/@FelipeVergara).

**Assets:**
- `assets/report_template.md` — Estructura y estilos del Word de salida.
