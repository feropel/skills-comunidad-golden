# Método Ad Library — cómo se mide de verdad la competencia

Todo lo de este archivo está **medido**, no supuesto. Las cifras entre paréntesis son de pruebas
reales corridas el 2026-07-27 contra Colombia. Léelo entero antes de dar un veredicto de saturación:
los tres errores que produce saltárselo son los que hacen lanzar un producto muerto o descartar uno
bueno.

## 1 · Los dos sesgos del MCP `ads_library_search`

### Sesgo A — el tope de 50, y es silencioso

`limit` tiene máximo **50** y **no hay paginación**. La respuesta trae `estimated_total_count`, que
es el número real de Meta, pero **nada te avisa de lo que falta**.

> Medido: `"fibra capilar"` · CO · ACTIVE → `estimated_total_count: 1496`, devueltos **50**.
> **Cobertura: 3,3%.**

**Regla: lee y reporta SIEMPRE el `estimated_total_count`.** Un conteo de tiendas sin ese número al
lado no es un dato, es una anécdota.

### Sesgo B — cuando hay más que el tope, el corte es por RECENCIA

Si `estimated_total_count > limit`, lo que recibes son **los más nuevos**, no una muestra.

> Medido: los 50 de "fibra capilar" cubrían **4,5 horas del mismo día**.

Consecuencia grave: **el anuncio de 30+ días, que es la señal reina de rentabilidad, queda fuera
del corte.** Y una tienda que lleva meses vendiendo bien pero no publicó creativos nuevos hoy
**aparece como si no existiera**. Un "mercado vacío" puede ser un mercado maduro que dejó de testear.

**Precisión importante:** cuando el total es MENOR que el límite, no hay sesgo — recibes todo,
histórico incluido. *(Medido: "removedor de verrugas" · CO → 9 de 9, y entre ellos uno de 36 días.)*
O sea el sesgo **no es del MCP siempre, es del corte**. Por eso la regla se formula así:

> **Si `estimated_total_count` ≤ `limit` → la muestra es completa, se puede leer antigüedad.
> Si es mayor → NO uses el MCP para juzgar antigüedad ni para contar tiendas. Solo sirve para
> ver quién está activo hoy y sacar IDs.**

### Qué hacer cuando el corte manda

Abrir la Ad Library en el navegador (`claude-in-chrome`), que sí deja scrollear el histórico:

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CO&q=<keyword>&search_type=keyword_unordered&media_type=all
```

- **`media_type` SIEMPRE en `all`.** El filtro de formato de Meta es poco fiable y esconde anuncios
  de imagen perfectamente válidos: puede hacer ver vacío un mercado lleno. Si el encargo pide "solo
  estáticos", NO toques la URL — filtra leyendo cada creativo.
- Verifica **en pantalla** que el filtro de país quedó puesto antes de contar nada. Un conteo con
  el país equivocado invalida el informe entero.
- La biblioteca es pública: no pide sesión. **Nunca uses curl/wget/scripts contra Facebook** —
  navegador o nada.

## 2 · El CEMENTERIO: quién probó el producto y lo apagó

Esta es la señal que casi nadie mira, y se saca con **dos llamadas de `limit:1`** comparando solo
los totales. Barata y muy informativa.

```
ads_library_search(search_terms=X, countries=[PAIS], ad_active_status="ACTIVE", limit=1)  → A
ads_library_search(search_terms=X, countries=[PAIS], ad_active_status="ALL",    limit=1)  → T
```

- **Apagados = T − A**
- **Tasa de supervivencia = A / T**

> Medido: "fibra capilar" · CO → ACTIVE **1.496**, ALL **2.014**. Apagados **518**, supervivencia
> **74,3%** → categoría sana, la gente que entra se queda.
> Medido: "removedor de verrugas" · CO → 9 y 9. Supervivencia 100%, pero **muestra chica: no
> concluyas nada con menos de ~30 históricos.**

| Supervivencia | Lectura |
|---|---|
| **>70%** | categoría sana: quien entra, se queda. Buena señal |
| **40-70%** | normal, hay rotación de testeo |
| **<40%** | 🚩 **cementerio**: mucha gente probó y apagó. Bandera roja fuerte aunque hoy veas tiendas activas |
| muestra <30 históricos | **no concluir**: el ratio no es significativo |

**Por qué importa:** un producto puede tener 3 tiendas activas hoy (parece punto dulce) y 200
anuncios apagados detrás (todos los que se quemaron). El activo solo te muestra a los que aún no
se han rendido.

## 3 · Keywords: mínimo 8, en 4 capas

La Ad Library hace match por **el texto del anuncio**, no por producto. Quien escribe "cinturilla"
no aparece si buscas "faja cinturilla". Buscar con 2-3 términos y concluir "no hay competencia" es
casi siempre un problema de keywords, no de mercado.

1. **Exactas** — nombre del producto y su versión en inglés si se anuncia así.
2. **Permutaciones** — la capa que evita los falsos "no hay": reordenar, quitar o agregar la palabra
   de categoría, sinónimos, diminutivos.
   *faja cinturilla · cinturilla · cinturilla ajustable · faja reloj de arena · moldeador de cintura.*
3. **Genéricas de categoría** — cómo lo llamaría una tienda de catálogo cualquiera.
4. **De dolor o sustituto** — con qué compiten los que atacan el mismo problema. Capturan la
   **saturación indirecta**: un mercado puede estar vacío del producto exacto y tapizado de
   sustitutos, y eso satura igual.

Ajusta el vocabulario al país. **Muestra la lista al usuario antes de buscar** para que corrija: es
el momento más barato de arreglar una validación.

## 4 · Registro de cobertura (obligatorio en la ficha)

Un "no hay tiendas" con cobertura parcial es una mentira cara. Se anota **en el momento**, por
keyword, nunca de memoria al final:

| Keyword | Reporta Meta | Revisados | Sin revisar | Tiendas nuevas | Estado |
|---|---|---|---|---|---|
| fibra capilar | ~1.496 | 50 | ~1.446 | 18 | ⚠️ parcial (3%) |
| fibras capilares | — | — | — | — | ⬜ no buscada |

Y debajo: **cobertura total en %**, **tiendas confirmadas** (vistas una a una) y **estimado sin
validar** con su razonamiento. Si en lo revisado las mismas tiendas se repetían, el estimado extra
es bajo; **si cada pantalla traía tiendas nuevas, la cobertura es insuficiente para dar veredicto**
— sigue buscando o baja la confianza y dilo.

> **"0 encontradas" y "no revisadas" son cosas distintas.** El número de cabecera siempre tiene dos
> partes: *"N confirmadas + ~M posibles sin validar"*. Nunca solo la primera.

**Confianza:** Alta ≥70% de cobertura · Media 40-69% · Baja <40%. Se declara junto al score.

## 5 · Filtrar el ruido antes de contar

El match por texto trae mucho que no compite.

> Medido: buscando "fibra capilar" salieron salones de belleza, insumos cosméticos y tratamientos
> capilares que solo comparten la palabra ("rellena tu fibra capilar con proteína pura"). **Ninguno
> vende el producto.** De 18 tiendas en pantalla, las que compiten de verdad eran un puñado.

- **Deduplica por tienda**: la unidad de medida es la **tienda única**, no la aparición. La misma
  tienda sale en varias keywords y con muchos anuncios.
- **Aparta a las cadenas grandes** (farmacias, retail): no compiten en contra entrega, pero **sí
  marcan el techo de precio** y eso va al informe.
- **Descarta el homónimo**: mismo término, otro producto. Si no vende lo que validas, no cuenta.

## 6 · Fast-flags (avisar apenas se detecten, sin esperar al informe)

- **8+ tiendas exactas escalando** → saturación dura. Decirlo temprano y ofrecer acortar.
- **Supervivencia <40%** → cementerio. Bandera roja antes de seguir gastando análisis.
- **Categoría que Meta restringe** (adelgazantes agresivos, claims médicos) → riesgo de rechazo de
  cuenta; se avisa aunque el producto valide comercialmente.
- **0 resultados en TODAS las keywords** → revisar primero si las keywords están mal elegidas.
  **Antes de escribir "mercado vacío", confirma que buscaste con `media_type=all` y con las 8.**

## 7 · Apify: la fuente que faltaba para el volumen de ventas (EVALUADA, sin conectar)

El scanner de volumen por navegador (Temu/AliExpress/Amazon con scroll infinito) funciona pero es
lento y frágil. **Apify** hace lo mismo por API con scrapers ya construidos.

| | |
|---|---|
| Qué es | catálogo de ~56.000 scrapers listos, con conector para Claude (`mcp.apify.com`) |
| Coste | **plan gratuito de $5/mes en créditos, sin tarjeta**. Starter $29, Scale $199 |
| Lo que sirve aquí | **Amazon · MercadoLibre · Shopify** (precio, stock, reseñas) y **TikTok · Instagram** (qué formato viraliza de verdad) |
| Estado | **evaluada el 2026-08-05, NO conectada.** Requiere cuenta y credenciales: es decisión del dueño |

**Por qué vale la pena:** el contador de ventas visible es demanda dura al nivel de producto y hoy
se saca a mano. Por API se saca de una categoría entera y se cruza contra la Ad Library sin
depender de que el scroll cargue.

⚠️ **Aplica la Regla Cero igual que con Firecrawl:** un scraper también devuelve basura plausible.
Ningún precio, stock o reseña entra a una ficha sin comprobar que el dato responde a lo que se pidió.

> 📌 **Hay un tercer uso, aplazado por decisión de FER (2026-08-05):** el scraper de **Google Maps**
> permite listar negocios locales con su WhatsApp y filtrar los que tienen muchas reseñas y **no
> tienen web** — el cliente exacto del Asistente Golden. FER lo quiere, pero **no ahora**:
> *"todavía no me dedico a esa parte, pero lo voy a hacer"*. Recordatorio programado para el
> 2026-08-12. No arrancar antes.
