# Taxonomía de campañas Meta Ads

## Cómo clasificar campañas

Meta Ads tiene varios tipos de estructura. Para analizar correctamente, hay que reconocer qué tipo es cada campaña. Esto se infiere del nombre de la campaña (los equipos suelen incluir el tipo en el nombre) y del comportamiento de los datos.

## Tipos de campaña Meta

### A. Por objetivo principal

**1. Sales / Compras (Conversión)**
- Optimiza para compras (eventos del pixel)
- Es el tipo dominante para e-commerce
- Detectar por: "VENTA", "WEB", "Compras", o por tipo de resultado "Compras en el sitio web"

**2. Traffic / Tráfico**
- Optimiza para clics o sesiones de página
- NO genera ventas atribuibles directas (aunque algunas se cuelen)
- Detectar por: "TRAFICO", "TRÁFICO", "Tráfico Instagram", "Link clicks"
- **Anti-patrón conocido**: Tráfico a Instagram con objetivo "visitas al perfil" no genera ventas atribuibles en e-commerce

**3. Messages / Mensajes (WhatsApp/Messenger)**
- Lleva al cliente a un chat
- En múltiples operaciones de e-commerce Colombia, este tipo de campaña históricamente pierde plata (CPA 2-3x mayor que retargeting web)
- Detectar por: "WPP", "WHATSAPP", "MSG", "CHATEA", "CHATBOT"

**4. Awareness / Reconocimiento, Engagement / Interacciones, Video Views, Reach**
- Casi nunca producen ventas. Filtrarlos antes del análisis principal.

### B. Por estructura de presupuesto

**ABO (Adset Budget Optimization)**
- Presupuesto se define a nivel adset
- Da control para leer performance por adset
- Detectar por: "ABO" en el nombre, o porque hay múltiples adsets con presupuestos distintos
- **Recomendado** cuando se quiere segmentar y leer claramente qué público funciona

**CBO (Campaign Budget Optimization)**
- Presupuesto se define a nivel campaña, Meta distribuye entre adsets
- Tiende a concentrar gasto en 1-2 adsets, los demás casi no gastan
- Detectar por: "CBO" en el nombre
- Difícil leer qué adset funciona porque Meta decide

**Advantage+ Shopping Campaign (ASC)**
- Estructura simplificada: 1 audiencia abierta, Meta decide todo
- Funciona bien con productos de margen alto y volumen
- Detectar por: "ADVANTAGE+", "AD+", "ASC", "Advantage+ Shopping"

### C. Por audiencia

**OPEN / Frío**
- Público sin intereses, sin LAL, sin remarketing
- El motor de adquisición de nuevos clientes
- Detectar por: "OPEN", "Frío", "Público abierto", "Cold", o ausencia de intereses

**Intereses**
- Adset con intereses específicos seleccionados
- Suele tener CPA mayor que OPEN porque Meta tiene menos libertad
- Detectar por: nombre con intereses (ej. "Belleza", "Skincare", "Maquillaje")

**LAL (Lookalike)**
- Audiencia similar a compradores existentes
- Detectar por: "LAL", "Lookalike", "Similar"

**Retargeting**
- Personas que ya interactuaron (visitaron, vieron video, agregaron al carrito)
- Suele tener CPA significativamente menor que frío
- Detectar por: "RETARGETING", "RT", "REMARKETING", "Caliente", "Tibio"

**Custom Audience**
- Lista de clientes, suscriptores de email, etc.

### D. Marcadores del equipo

Los equipos de marketing suelen anotar el estado de la campaña en el nombre:
- ✅ = Funcionó / activa
- ❌ = Falló / pausada
- 🔥 = Top performer
- ⭐ = Favorita
- "BACK UP" = respaldo si las principales se saturan

Estos marcadores son útiles para identificar lo que el equipo ya validó como ganador.

## Naming convention estándar (formato típico)

El formato más común que usan los equipos de marketing para nombrar campañas:

```
[PRODUCTO]/[TIPO]/[ESTRUCTURA]/[FECHA]

Ejemplos ilustrativos:
- PRODUCTO A - VENTA - OPEN 1
- PRODUCTO B - VENTA - ADVANTAGE+ 25-03
- PRODUCTO C - VENTA - OPEN - HOMBRE
- PRODUCTO D - RETARGETING - CALIENTES - WEB - CBO - 8-ABRIL
- PRODUCTO E - TRAFICO - CHATEA PRO - ABO
```

Patrón típico:
- Producto al inicio
- Tipo de campaña (VENTA, TRAFICO, RETARGETING)
- Tipo de público o estructura (OPEN, ADVANTAGE+, HOMBRE, MUJER, CALIENTES, TIBIOS)
- Fecha o número de versión

## Cómo agrupar para análisis

Cuando hagas el análisis por tipo de campaña, agrupa así:

```python
def clasificar_campaña(nombre):
    n = nombre.upper() if nombre else ''
    
    # Por objetivo
    if 'WPP' in n or 'WHATSAPP' in n or 'CHATEA' in n or 'CHATBOT' in n:
        return 'TRAFICO_WPP'
    if 'TRAFICO' in n or 'TRÁFICO' in n or 'TRAFFIC' in n:
        return 'TRAFICO_WEB'
    if 'RETARGETING' in n or 'REMARKETING' in n:
        return 'RETARGETING'
    if 'ADVANTAGE' in n or 'AD+' in n or 'ASC' in n:
        return 'ADVANTAGE_PLUS'
    if 'CATALOG' in n or 'CATÁLOGO' in n or 'DPA' in n:
        return 'CATALOG_DPA'
    if 'BACK UP' in n or 'BACKUP' in n:
        return 'BACKUP'
    if 'OPEN' in n or 'VENTA' in n or 'WEB' in n:
        return 'VENTA_OPEN'
    return 'OTRO'
```

## Patrones validados en e-commerce Colombia

### Productos COD con margen medio-alto
- **Ganador**: VENTA OPEN con segmentación demográfica + RETARGETING WEB
- **Perdedor**: TRAFICO_WPP, ADVANTAGE+ cuando el margen no lo soporta
- Mix recomendado: 60-70% Open Sales, 20-25% Retargeting, 5-10% Backup

### Productos e-commerce pago anticipado con margen bajo
- **Ganador**: VENTA con bundles/kits + Retargeting WEB CALIENTE/TIBIO
- **Perdedor**: TRAFICO_WPP, RETARGETING_WPP, Tráfico a perfil de redes sociales
- Mix recomendado: 60% frío con bundles, 40% retargeting web

### Reglas duras
- **Catalog Ads en frío** generalmente pierden plata. Solo en retargeting.
- **WhatsApp como destino** consistentemente da CPA 2-3x peor.
- **Foto estática** vs video: video gana ~70% de las veces en estos nichos.
