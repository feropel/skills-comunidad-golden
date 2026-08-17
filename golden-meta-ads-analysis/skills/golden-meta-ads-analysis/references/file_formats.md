# Formatos de archivo de Meta Ads

Meta Ads Manager permite descargar reportes en distintos formatos. Cada uno tiene estructura diferente.

## Formato 1: Creative Reporting

Generalmente vienen así:
- Una sola hoja llamada `Creative Reporting`
- Header en la fila 0 (sin offset)
- Columnas estándar: Nombre de la campaña, Nombre del conjunto de anuncios, Nombre del anuncio, Edad, Sexo, Importe gastado, Resultados, CPA, ROAS, etc.

Las filas contienen registros por combinación de adset + ad + edad + sexo + ubicación (según el desglose seleccionado).

**Nivel de la entrega**: campaign, adset, ad — indica nivel jerárquico de la fila.

## Formato 2: Raw Data Report

Similar al anterior pero con más columnas y datos crudos. A veces tiene header en fila 2 o 8 según versión de Meta.

## Formato 3: Formatted Report

Versión "bonita" del reporte, con estilos. El header está típicamente en la fila 2 (header=2 al leer con pandas).

```python
df = pd.read_excel(file, sheet_name='Formatted Report', header=2)
```

## Formato 4: Estructura jerárquica con NaN

Algunos reportes vienen con jerarquía rellenada:
- Fila campaña: tiene nombre campaña, NaN en adset y ad
- Fila adset: tiene nombre adset, NaN en ad
- Fila ad: tiene todo

Para procesarlos hay que hacer forward-fill:

```python
df['Campaña'] = df['Nombre de la campaña'].ffill()
df['Adset'] = df['Nombre del conjunto de anuncios'].ffill()
```

## Columnas estándar que aparecen (puede variar idioma)

### Identificación
- `Nombre de la campaña` / `Campaign name`
- `Nombre del conjunto de anuncios` / `Ad set name`
- `Nombre del anuncio` / `Ad name`
- `Identificador del anuncio` / `Ad ID`
- `Nivel de la entrega` (campaign, adset, ad)
- `Estado de la entrega` (active, inactive, archived, not_delivering)

### Tiempo
- `Inicio del informe` / `Reporting starts`
- `Fin del informe` / `Reporting ends`

### Demografía (si hay desglose)
- `Edad` / `Age` (18-24, 25-34, 35-44, 45-54, 55-64, 65+, Unknown, All)
- `Sexo` / `Gender` (male, female, unknown, All)

### Ubicación (si hay desglose)
- `País` / `Country`
- `Región` / `Region`
- `Ciudad` / `City`

### Plataforma y ubicación (si hay desglose)
- `Plataforma` / `Platform` (facebook, instagram, audience_network, messenger, threads, whatsapp)
- `Ubicación` / `Placement` (Feed, Reels, Stories, Marketplace, Search results, Audience Network native, etc.)
- `Dispositivo` / `Device` (mobile, desktop)

### Métricas de inversión
- `Importe gastado (COP)` o `(USD)` — moneda según cuenta
- `Frecuencia`
- `Impresiones`
- `Alcance` / `Reach`

### Métricas de resultado
- `Resultados` — métrica del objetivo de la campaña (compras si es Sales)
- `Tipo de resultado` — qué cuenta como "resultado" (Compras en el sitio web, Conversaciones por mensaje, etc.)
- `Costo por resultado` — CPA
- `Compras` — compras específicas (cuando objetivo es Sales)
- `ROAS de compras` / `Purchase ROAS`
- `Valor de conversión de compras` / `Purchase conversion value`
- `Ticket Promedio $` — algunas cuentas lo calculan

### Métricas del embudo
- `Clics en el enlace` / `Link clicks`
- `CTR único (porcentaje de clics en el enlace)`
- `CPC (costo por clic en el enlace)`
- `CPM (costo por mil impresiones)`
- `Visitas a la página de destino` / `Landing page views`
- `Velocidad Carga de la pagina` — solo si CAPI configurada
- `Pagos iniciados` / `Initiated checkouts`
- `Adiciones al carrito` / `Adds to cart`

### Métricas de video
- `Reproducciones de video de 3 segundos`
- `Reproducciones de video hasta el 25%`
- `Reproducciones de video hasta el 50%`
- `Reproducciones de video hasta el 75%`
- `Reproducciones de video hasta el 100%`
- `Tiempo de reproducción promedio`

### Clasificaciones de Meta
- `Clasificación de calidad` — above_average, average, below_average
- `Clasificación del porcentaje de interacción`
- `Clasificación del porcentaje de conversiones`

## Detectar moneda y tipo de cambio

```python
# Buscar columna con "Importe gastado"
for col in df.columns:
    if 'Importe gastado' in str(col) or 'Amount spent' in str(col):
        if 'USD' in str(col):
            moneda = 'USD'
        elif 'COP' in str(col):
            moneda = 'COP'
        else:
            moneda = 'desconocida'
```

Si la moneda es USD pero los datos parecen COP (números muy grandes), revisar el ticket promedio para confirmar.

### Conversión USD → COP

Cuando el reporte viene en USD y la operación es en Colombia (COP), hay que convertir. Seguir este orden de prioridad:

1. **PRIMERO: buscar la tasa actual en internet** usando `web_search` con query "dólar a peso colombiano hoy" o "USD COP tasa hoy". Usar el valor del día.
2. **Si no se puede acceder a internet**: usar $4,000 COP/USD como referencia conservadora y decir explícitamente al usuario que se aplicó esta tasa de referencia, no la tasa real del día.
3. **Si el usuario provee su propia tasa**: usar la que él diga.

NUNCA asumir una tasa fija sin intentar primero buscarla en internet. La diferencia entre $4,000 y $4,300 COP/USD puede mover el CPA breakeven varios miles de pesos.

## Detectar tipo de campaña por columna "Tipo de resultado"

```python
df['Tipo de resultado'].value_counts()
```

Valores típicos:
- `Compras en el sitio web` — campañas Sales (las que importan)
- `Conversaciones por mensaje iniciadas` — Tráfico WhatsApp
- `Clics en el enlace` — Tráfico web
- `Visitas a la página de destino` — Tráfico LP
- `ThruPlays` — Video views
- `Interacción con la publicación` — Engagement

**Para análisis de ventas, filtrar solo `Compras en el sitio web`.**

## Filtrar filas válidas

Algunas filas pueden ser totales agregados sin identificador. Para análisis a nivel ad:

```python
# Solo filas con identificador y nivel ad
ads = df[
    (df['Identificador del anuncio'].notna()) & 
    (df['Nivel de la entrega'] == 'ad')
]
```

## Detectar duplicación por desglose

Cuando el reporte trae desglose por demografía + ubicación, el mismo ad ID puede aparecer 3-5 veces (1 por combo). Para análisis consolidado:

```python
# Si hay desglose por edad/sexo, filas con Edad='All' y Sexo='All' son los totales
total_ads = df[(df['Edad']=='All') & (df['Sexo']=='All')]
```

Si no existe la opción 'All', deduplicar:

```python
ads_unique = ads.drop_duplicates(
    subset=['Identificador del anuncio', 'Edad', 'Sexo', 'Nombre del conjunto de anuncios']
)
```

## Casos especiales

### Reporte vacío o casi vacío
Si tiene <10 filas o ningún `Importe gastado` > 0, decir al usuario que el reporte no tiene data útil.

### Reporte solo con totales sin desglose
Útil para overview pero no permite análisis demográfico o por ubicación. Recomendar al usuario descargar versión con desglose.

### Múltiples productos en el mismo archivo
Si las campañas mencionan productos distintos (ej: PRODUCTO_A y PRODUCTO_B en el mismo Excel), preguntar al usuario si quiere análisis combinado o separado.
