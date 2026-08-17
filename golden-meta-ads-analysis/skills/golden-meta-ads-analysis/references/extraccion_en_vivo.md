# Modo B — Extracción de datos EN VIVO por la Meta Marketing API

Alternativa al Excel exportado (Modo A). En vez de que el usuario exporte a mano desde Ads Manager, tú traes los datos directo de la API con los scripts `fetch_*.py`. El motor de análisis (unit economics, capas, veredicto, Word) es **el mismo**: solo cambia de dónde salen los números.

Flujo exacto:

```
Access Token → Negocios → Cuenta → Campañas → Insights → [Conjuntos → Anuncios]
```

## Automatización — el usuario NO edita archivos ni pega JSON

Tú ejecutas todo. El usuario SOLO da: (1) el Access Token una vez, (2) el número de la opción que elige cuando le muestras listas.

> 🔒 **Antes de cualquier `fetch_*`, corre `python3 scripts/check_token.py`.** Verifica contra `/debug_token` que el token sea solo-lectura y ABORTA si trae escritura (`ads_management`), expiró, o le falta `ads_read`. No sigas hasta que pase con "✅ Token solo-lectura verificado". Esto protege sobre todo a la comunidad.

En cada paso que requiera credenciales o IDs:
1. Escribe/actualiza el archivo `.env` (en el directorio de trabajo) con el valor. Usa `Edit` si ya existe (para no pisar el token), `Write` si no. Formato:
   ```
   META_ACCESS_TOKEN=EAA...
   AD_ACCOUNT_ID=act_123456789
   CAMPAIGN_ID=123456789
   ADSET_ID=123456789
   DATE_PRESET=last_30d
   ```
2. Ejecuta el script con `Bash` (`python3 scripts/fetch_*.py`). Si falta `requests`, corre `pip install requests` automáticamente.
3. Lee el JSON resultante con `Read` (usa `Glob` si el timestamp es incierto). NUNCA le pidas al usuario que lo pegue.

## ⚠️ Reglas anti-ban del token (aplícalas ANTES de pedirlo)

Meta banea cuentas por mal uso de la API. Exige siempre:
- **System User Token** (no expira), NO token personal del Explorador de API Graph.
- **Developer App en una Business Manager SEPARADA** de producción (crear la app en la misma BM de las cuentas de producción es causa frecuente de baneo).
- **Scopes mínimos solo-lectura:** `ads_read` + `business_management`. NUNCA `ads_management` ni `read_insights`.
- Nada de scraping de UI ni MCPs no oficiales.

Si el usuario trae token personal, adviértele:
> "Este token es personal. Si Meta marca la actividad, tu cuenta personal queda restringida. Te recomiendo generar un System User Token (5 min). Seguimos con el personal o lo generamos?"

### Generar un System User Token (guía si no tiene)
1. Crear la Developer App: https://developers.facebook.com/apps/ → "Crear app" → caso de uso "Medir/Administrar anuncios con la API de Marketing" → seleccionar el **portafolio comercial SEPARADO** (no el de producción).
2. Business Manager → Configuración de la empresa → Usuarios → **Usuarios del sistema** → Añadir (rol Empleado) → Asignar activos: las cuentas de producción con permiso **solo Ver rendimiento** → **Generar token** con la app de arriba → marcar SOLO `ads_read` + `business_management` → token permanente.

## Pasos

| Paso | Script | .env que actualizas | Salida a leer |
|------|--------|---------------------|---------------|
| **0. 🔒 Preflight de seguridad (OBLIGATORIO)** | `check_token.py` | `META_ACCESS_TOKEN` | `token_check.json` |
| 1. Negocios y cuentas | `fetch_businesses.py` | `META_ACCESS_TOKEN` | `businesses.json` |
| 2. Campañas | `fetch_campaigns.py` | `AD_ACCOUNT_ID` | `campaigns.json` |
| 3. Insights (auto-detecta tipo) | `fetch_insights.py` | `CAMPAIGN_ID`, `DATE_PRESET` | `insights_{id}_{periodo}_*.json` |
| 4. Conjuntos | `fetch_adsets.py` | `CAMPAIGN_ID` | `adsets_{id}.json` |
| 5. Anuncios | `fetch_ads.py` | `ADSET_ID` | `ads_{id}.json` (trae `desglose_warnings` y `spend_pct_of_adset` precalculados) |

Muestra las listas con íconos de estado (🟢 ACTIVA / 🔴 PAUSADA / ⚫ ARCHIVADA) y pide al usuario que responda con el número. Si no dio periodo, pregunta (7, 14, 30 o 90 días).

## Tipo de campaña detectado automáticamente

`fetch_insights.py` mapea el `objective` de Meta a un tipo interno (campo `campaign_type` del JSON):

| Objetivo Meta | Tipo interno |
|---------------|--------------|
| OUTCOME_SALES, CONVERSIONS, PRODUCT_CATALOG_SALES | `ventas` |
| OUTCOME_ENGAGEMENT, OUTCOME_TRAFFIC, MESSAGES, POST_ENGAGEMENT, PAGE_LIKES | `interaccion` |
| OUTCOME_LEADS, LEAD_GENERATION | `cp_formularios` (→ `cp_sitio_web` si el destino es sitio web) |
| OUTCOME_STORE_TRAFFIC, OUTCOME_AWARENESS | `tiendas_fisicas` / `reconocimiento` |
| (otro) | `desconocido` → pregunta al usuario qué objetivo tiene |

Con el tipo detectado, aplica la tabla de benchmarks correspondiente de `references/benchmarks_por_objetivo.md`.

## Puente con el motor Golden

Una vez tienes los insights en vivo:
- Si es **`ventas` en COD** → sigue el workflow completo de Modo A desde el Paso 2 (unit economics → CPA breakeven → 8 capas → veredicto → Word). El breakeven calculado MANDA sobre cualquier benchmark genérico.
- Si es **otro objetivo** (leads, mensajes, reconocimiento) → usa los benchmarks por objetivo + las 3 Q's de `references/benchmarks_por_objetivo.md`, porque ahí no hay "compra" que llevar a P&L.
- Para decidir pausar/escalar a nivel conjunto o anuncio → aplica SIEMPRE `references/efecto_desglose.md` primero.

## Errores comunes de la API

- Rate limit (códigos 4/17/32/613): los scripts reintentan con backoff. Si insiste, esperar.
- Token expirado (code 190): el usuario renueva el token.
- Permisos insuficientes (code 200): el token necesita `ads_read` + `business_management`.
- ROAS vacío: el píxel no tiene eventos de compra configurados.
