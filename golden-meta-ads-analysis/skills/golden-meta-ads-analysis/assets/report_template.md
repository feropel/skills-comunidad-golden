# Template de Reporte Word — Estructura estándar

Cada análisis genera un documento Word con esta estructura exacta. Es la plantilla estándar de análisis para campañas de Meta Ads.

## Especificaciones de formato

- Fuente: Arial, tamaño 11 (size 22 en docx units)
- Tamaño página: Carta (8.5 × 11 pulgadas)
- Márgenes: 1 pulgada en cada lado
- Colores corporativos:
  - Primary (azul): `1F4E79`
  - Accent (rojo): `C00000`
  - Green: `548235`
  - Amber: `BF8F00`
  - Gray: `595959`
  - Light backgrounds: `E7EEF5` (azul claro), `E2EFDA` (verde claro), `FCE4D6` (rojo claro), `FFF2CC` (amarillo claro)
- Tablas: borde gris claro `BFBFBF`, header con fill primary, filas alternas con fill light

## Estructura del documento (en orden)

### 1. Portada
- Título grande: "ANÁLISIS DE CAMPAÑAS" (color primary, centrado)
- Subtítulo: NOMBRE DEL PRODUCTO en mayúsculas (color accent, centrado)
- Tagline: descripción corta del análisis
- Línea con: Periodo · Inversión · Compras
- Línea con: Precio · Costo · Flete · Tasas
- Page break

### 2. Unit Economics
**1.1 Flujo real de 100 órdenes Meta**
Tabla con columnas: Estado | Cantidad | % del total | Ingresos | Costo flete

**1.2 P&L sobre 100 órdenes**
Tabla con columnas: Concepto | Cálculo | Valor

Destacar el CPA breakeven en un párrafo centrado con tamaño 36 y color verde.

**1.3 CPA objetivo según margen neto deseado**
Tabla con columnas: Margen deseado | CPA máximo | ROAS objetivo | Ganancia por 100 órdenes
Filas con colores: breakeven amarillo, demás verde gradient

### 2. P&L histórico real de la cuenta
Sección propia (no subsección de Unit Economics — `generate_report.py` la genera como
bloque independiente porque responde una pregunta distinta: no "cuál es el breakeven" sino
"esta cuenta ganó o perdió plata de verdad"). Tabla mostrando si la cuenta perdió o ganó
plata aplicando los unit economics al gasto real, con veredicto GANÓ/PERDIÓ destacado.

### 3. Ranking de Campañas (si aplica)
Tabla maestra por tipo de campaña (Capa 1): tipo | gasto | compras | CPA | ROAS | % compras.
Filas con colores según tier.

### 4. Ranking de Creativos
**4.1 Tabla maestra**
Columnas: Video | Inversión | Compras | CPA | ROAS | Veredicto
Filas con colores según tier (verde/amarillo/rojo)

**4.2 Detalle de los top 3-4 ganadores**
Para cada uno: tabla con métricas clave (gasto, compras, CPA, ROAS, CTR, CPC, hold rate, view through, mejor demografía, mejor ubicación)

**4.3 Videos a descartar**
Lista breve con razón

### 5. Demografía
**5.1 Distribución por sexo**
Tabla: Sexo | % Compras | % Inversión | CPA | ROAS | Lectura

**5.2 Distribución por edad**
Tabla: Edad | % Compras | CPA | ROAS | Veredicto

**5.3 Combinaciones edad x sexo más rentables**
Tabla solo con combos con CPA bajo breakeven

### 6. Plataformas y Ubicaciones (si aplica)
**6.1 Por plataforma**
Tabla: Plataforma | Inversión | Compras | CPA | ROAS | % compras

**6.2 Por ubicación específica**
Tabla con top ubicaciones ordenadas por volumen

**6.3 Ubicaciones secretas con mejor ROAS**
Las 3-5 ubicaciones con ROAS más alto aunque tengan poco volumen

### 7. Landing destino (si aplica)
**7.1 Performance global por landing**
Tabla comparando todas las landings

**7.2 Mismo video en diferentes landings**
Comparativa cuando el mismo creativo va a múltiples landings

**7.3 Regla landing → creativo**
Patrón identificado

### 8. Embudo de conversión (si aplica)
Tabla: Etapa | Tasa actual | Benchmark | Veredicto — una fila por etapa del embudo
(Impresiones → Clics → Visitas LP → Pagos iniciados → Compras), coloreada por tier.

### 9. PLAN DE ACCIÓN (la sección más importante)

**A. QUÉ PAUSAR HOY MISMO**
Tabla con: Nombre exacto | Razón | Pérdida acumulada

**B. QUÉ CONTINUAR Y ESCALAR**
Tabla con: Nombre exacto | Presupuesto sugerido | CPA objetivo

**C. QUÉ NUEVAS CAMPAÑAS LANZAR**
Estructura completa de cada campaña/adset/anuncio nuevo

**D. CÓMO REPLICAR EN OTRA CUENTA DEL MISMO BM**
- Setup técnico
- Materiales a transferir
- Plan día por día primera semana

**E. CÓMO REPLICAR EN OTRO BM**
- Calentamiento de cuenta
- Checklist técnico
- Riesgos a vigilar

### 10. Síntesis Ejecutiva
Tabla numerada con 7-10 conclusiones clave (`sintesis_ejecutiva` en el config).

Párrafo de cierre con recomendación final.

### 11. Producción creativa recomendada (si aplica)
Bloque clave/valor (`produccion_creativa` en el config) con: ángulo ganador, duración
recomendada, casting, hook y landing por tipo de creativo — ver
`references/reglas_duras_colombia.md` para el detalle de cada uno. Aquí es donde van
las palancas de margen y cualquier prueba adicional sugerida, como parte del punto final
del bloque.

No hay una sección separada de "KPIs de monitoreo" en el documento generado: los
semáforos por KPI viven dentro de cada tabla (Ranking de campañas, Creativos, Demografía,
Ubicaciones, Embudo) coloreados fila por fila — no como una tabla de referencia aparte.

## Reglas de redacción

- **Tono**: directo, ejecutable, sin filler. "Pausar X campaña" no "Considera pausar X campaña".
- **Idioma**: español de Colombia. Usar "pauta" no "publicidad", "anuncio" no "creativo" (aunque "creativo" sí es ok).
- **Nombres exactos**: cuando menciones una campaña/adset/ad, usar el nombre EXACTO del archivo, no parafrasear.
- **Sin claims médicos**: para productos cosméticos no usar "trata", "cura", "elimina" — usar "mejora", "ayuda a", "suaviza".
- **Sin separadores visuales**: no usar "═════" ni "━━━━" ni emojis decorativos repetidos.
- **No incluir frases como**: "cópialo y pégalo", "espero que te sirva", "déjame saber si necesitas algo más".
- **Sí incluir**: el resumen ejecutivo al final con la pregunta más relevante respondida concretamente.

## Estilo de las tablas

### Tabla de tipo "veredicto" (con colores por fila)
Usar fills:
- Verde claro (`E2EFDA`) para tier 🟢
- Amarillo claro (`FFF2CC`) para tier 🟡
- Rojo claro (`FCE4D6`) para tier 🔴

### Tabla informativa
Filas alternas: `FFFFFF` y `E7EEF5` (light blue)

### Tabla destacada (highlights)
Header en color accent (`C00000`) en lugar de primary

## Numeración de secciones

Usar numeración 1.0, 1.1, 1.2... 2.0, 2.1... para que el usuario pueda referenciar.

## Página breaks

Insertar page break entre las secciones principales (1, 2, 3, 4, 5, 7, 8) para que el documento sea navegable.
