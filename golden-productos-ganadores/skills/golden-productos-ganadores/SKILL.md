---
name: golden-productos-ganadores
description: >-
  Golden Group — Búsqueda y validación de PRODUCTOS GANADORES para dropshipping
  COD / marca propia en LatAm. Cruza la Meta Ad Library (anuncios activos de la
  competencia) con los contadores de ventas reales de AliExpress y Amazon, reseñas
  y tendencias de búsqueda para encontrar y puntuar productos con demanda real, y
  entrega una FICHA DE PRODUCTO GANADOR lista para investigar a fondo y montar la página.
  Úsala SIEMPRE que el usuario quiera: buscar productos ganadores, validar un
  producto, saber si un producto vende, encontrar productos en tendencia,
  "qué vendo", "dame productos winner", analizar la demanda de un producto,
  espiar qué está pautando la competencia, o decidir qué producto lanzar. También cuando mande
  VARIOS productos de una (modo LOTE: valida cada uno y entrega un ranking comparativo), pregunte
  "está saturado este producto", "cuánta competencia hay", "quién lo está vendiendo ya", o quiera
  el índice de anuncios de la competencia con links para espiar creativos.
  NO usar para analizar pauta propia (eso es golden-meta-ads-analysis) ni para
  construir la página (eso es golden-shopify).
---

# Golden Group — Productos Ganadores

<!-- skill GPG1.7 · 2026-08-02 · AMAZON RESUCITA POR NAVEGADOR y cae la afirmacion no verificada. GPG1.6 dijo "para Temu y Amazon usar Chrome MCP" SIN PROBARLO — se escribio por deduccion, el mismo error que esta skill corrige en todas partes. Medido hoy: (a) AMAZON POR NAVEGADOR ✅ es la MEJOR fuente del scanner — 48 tarjetas, 34 con "comprados el mes pasado" (71%), 46 con precio, 45 con rating, total "155 resultados", precios en COP y envio a Colombia detectados solos; da mas que AliExpress. Receta con selectores en el cuerpo. (b) TEMU ❌ por ninguna via: muro de SESION ("Email o numero de telefono"), no es JS es autenticacion; solo saldria con claude-in-chrome si FER ya tiene sesion — preguntar, no asumir. (c) MERCADOLIBRE CO ❌ nuevo: por Firecrawl da CAPTCHA y el extractor inventa "Producto 1..8" con precios y ratings falsos CON metadata.title poblado (modo 4, rompe el check 2); por navegador, muro de sesion. (d) DESCRIPCION corregida: prometia "TikTok Creative Center" que no se puede leer — ahora nombra AliExpress y Amazon, que si. (e) COMPUERTA nueva: pasar todo scrape por candado_scraping.py antes de puntuar -->
<!-- skill GPG1.5 · 2026-07-27 · AUDITORIA con golden-skill-auditor tras pregunta de FER ("por que no lo habias descubierto"): la causa raiz fue auditar el TEXTO de la skill y nunca EJECUTAR la herramienta que recomienda. Ahora medido en vivo: (a) CEMENTERIO nuevo — comparar ad_active_status ACTIVE vs ALL con limit:1 da la tasa de supervivencia de la categoria (fibra capilar CO: 1.496 activos / 2.014 historicos = 74,3%; <40% = bandera roja aunque hoy se vean tiendas activas). Supera al metodo de terceros, que lo planteaba como chequeo manual opcional. (b) CORRECCION de GPG1.4: el sesgo de recencia solo aplica cuando el total SUPERA el limit; si es menor se recibe todo, historico incluido (medido: 9 de 9, uno de 36 dias). La redaccion anterior era imprecisa. (c) ESTRUCTURA: de 295 lineas en un solo archivo a SKILL.md + 2 references (divulgacion progresiva). (d) Del metodo ajeno se adapto lo que faltaba: mapa de angulos con HUECOS y hooks, lectura de precios (techo/piso), MODO LOTE con ranking y lectura transversal, fast-flags, y la regla de entregar el informe tambien cuando el veredicto es NO -->
<!-- skill GPG1.4 · 2026-07-27: filtro de un metodo de validacion de terceros (Vertex Digital, otra empresa — se extrajo el METODO, nada de su marca). Aporte propio MEDIDO: los 2 sesgos del MCP ads_library_search — tope duro de 50 sin paginacion (cobertura 3,3% sobre 1.496 reportados) y devuelve LOS MAS RECIENTES (los 50 de la prueba cubrian 4,5 horas del mismo dia), asi que NUNCA muestra el anuncio de 30+ dias que esta misma skill declara señal reina: contradiccion interna real, ahora documentada con su workaround por navegador. Del metodo ajeno se horneo: minimo 8 keywords en 4 capas con permutaciones, REGISTRO DE COBERTURA obligatorio (0 encontradas != no revisadas), filtrado de ruido y dedup por tienda, curva de saturacion numerica (0=riesgo no oportunidad, 1-3 punto dulce, 4-7 competido, 8+ saturado), señales por competidor y indice de anuncios con link directo por ID -->
<!-- skill GPG1.3 · 2026-07-27: corregido por FER — Golden opera COD Y pago anticipado, y el producto ganador es DISTINTO en cada uno. Regla 2 partida en dos, rubrica ahora con dos columnas y criterio RECOMPRA nuevo (20 pts) que solo existe en marca propia: un consumible aburrido saca 55 como catalogo y 78 como marca propia -->
<!-- skill GPG1.2 · 2026-07-25: filtro del paquete RECURSOS EGS — umbral duro de antigüedad (≥60 días = máximo, <14 no concluyente), rankear Ad Library por GASTO estimado y no por número de anunciantes, y sección SOURCING LOCAL nueva (grupos mayoristas con el texto de publicación, grilla de 6 factores, señales de alarma, adaptado a San Victorino/El Restrepo/El Hueco) -->
<!-- skill GPG1.1 · 2026-07-25: nueva fuente SCANNER DE VOLUMEN VISIBLE (Temu/AliExpress/Amazon por navegador, contadores de órdenes como señal de demanda dura) — patrón destilado de las extensiones de WiFi Money; se replica con el MCP de Chrome sin instalar código ajeno -->
<!-- skill GPG1.0 · creación: Ad Library como prueba reina + rúbrica 0-100 + ficha entregable -->

**Versión:** `GPG1.7` · Fábrica: este chat.

Objetivo: pasar de "no sé qué vender" a una **ficha de producto validado con evidencia**, en minutos, usando solo herramientas ya conectadas (sin pagar spy tools).

## Reglas de oro
1. **Nunca recomiendes un producto sin evidencia de demanda activa.** Mínimo: anuncios corriendo HOY en la competencia (Meta Ad Library) o tendencia clara.
2. **PREGUNTA PRIMERO PARA QUÉ MODELO ES.** Golden opera los dos y **el producto ganador es distinto
   en cada uno**:
   - **Catálogo / contra entrega** → producto de **impulso**, problema-solución visible en 3s de
     video, ligero y no frágil (la devolución cuesta flete doble), precio venta ≥ 3× costo.
     Es venta **única**: el producto tiene que ganar en la primera compra o no gana.
   - **Marca propia / pago anticipado** → aquí manda la **RECOMPRA**. Un consumible que se acaba en
     30-60 días vale más que un ganador de impulso que se compra una vez, porque el segundo pedido
     no cuesta pauta. Aguanta ticket más alto y menos "wow", pero exige **calidad sostenida y
     reposición asegurada**: una marca propia que se queda sin stock pierde al cliente recurrente,
     no solo la venta.
3. **Cierra siempre con la ficha** y el siguiente paso (investigación → golden-shopify).

## Fuentes (todas ya disponibles)
- **Meta Ad Library** → herramienta `ads_library_search` del MCP de Meta. Es la prueba reina: ves los
  anuncios ACTIVOS de cualquier competidor/país, antigüedad y variantes. Nadie deja corriendo un
  anuncio que pierde plata, así que la antigüedad **es** la validación.

  > ### ⛔ ANTES DE CONTAR NADA: los 2 sesgos del MCP (medidos 2026-07-27)
  > **1 · `limit` tope 50, sin paginación, y en silencio.** Medido: "fibra capilar" · CO →
  > `estimated_total_count: 1496`, devueltos 50. **Cobertura 3,3%.** Lee y reporta SIEMPRE ese total.
  > **2 · Si el total supera el límite, el corte es por RECENCIA** (los 50 cubrían 4,5 horas del
  > mismo día) → **el anuncio de 30+ días, que es la señal reina, queda fuera**. Si el total es
  > MENOR que el límite no hay sesgo y sí se puede leer antigüedad.
  > **Método completo, cementerio de anunciantes, keywords y cobertura → `references/ad-library-metodo.md`.
  > Es lectura obligatoria antes de dar un veredicto de saturación.**

  Dos criterios duros:
  - **≥60 días con el mismo anuncio corriendo = puntuación máxima de antigüedad.** Menos de 14 días
    no es concluyente: puede ser un test que están a punto de matar.
  - **Rankea por GASTO estimado, no por número de anunciantes.** Un anunciante quemando presupuesto
    fuerte es mejor señal que diez pequeños con el mismo producto. Contar anunciantes mide presencia;
    el gasto mide convicción.
- **Firecrawl** (`firecrawl_search`, `firecrawl_scrape`, `firecrawl_map`) → AliExpress
  (precio costo + contador de ventas), tendencias, blogs de winning products.
  📖 **Manual verificado de uso:** `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`
  — recetas medidas, coste por llamada y trampas. Leerlo antes de scrapear en serie.

  > ### ⛔ REGLA CERO — el scrape puede ser BASURA con `statusCode: 200` (medido 2026-07-31/08-01)
  > Se midieron **3 modos de fallo distintos, y ninguna verificación sola los caza todos:**
  > **1 · Alucinación.** Página hueca → el extractor **inventa**. Devolvió *"Smart TV 55\" 4K LED,
  > $499.99, 150 reseñas"* para una página de removedor de verrugas. *Tell: `metadata.title` vacío.*
  > **2 · Señuelo.** Redirige y te da el menú. Temu con "wart remover" devolvió **72 categorías de
  > ropa** con precio "N/A". *Tell: `metadata.url` ≠ `sourceURL`, valores "N/A" en masa.*
  > **`title` viene POBLADO: el check del modo 1 pasa en verde.**
  > **3 · Muro anti-bot.** Amazon: **la respuesta no trae campo `json`**, title poblado y sin
  > redirección. *Tell: no existe `json`.*
  > **🎯 La verificación que sí caza los tres: EL DATO RESPONDE A LO QUE PEDÍ?** Si buscaste
  > verrugas y llegan vestidos, es basura. Un producto fantasma puntuado en la rúbrica manda a
  > testear algo que no existe, con presupuesto real.
- **deep-research** (skill) → cuando el usuario quiere un barrido profundo multi-fuente verificado de un nicho.
- **Scanner de volumen visible** → las tiendas muestran el contador de ventas en el listado
  ("5K+ vendidos este mes", "10K+ bought"). Esa cifra es demanda DURA al nivel de producto —
  complementa la Ad Library (que prueba que alguien PAUTA, no que vende).

  **Qué fuente responde de verdad (MEDIDO 2026-08-01 — no asumir, está probado una por una):**

  | Tienda | Estado | Cómo |
  |---|---|---|
  | **AliExpress** | ✅ **Funciona** | **Firecrawl.** Medido: 8 productos con "480 sold", "3,000+ sold" |
  | **Amazon** | ✅ **Funciona** | **NAVEGADOR** (por Firecrawl no: muro anti-bot). Ver receta abajo |
  | **Temu** | ❌ **No funciona** | Firecrawl: devuelve categorías de ropa. Navegador: **muro de sesión** |
  | **MercadoLibre CO** | ❌ **No funciona** | Firecrawl: **captcha → inventa "Producto 1..8"**. Navegador: muro de sesión |
  | **TikTok Creative Center** | ❌ No funciona | App JS tras redirección; solo devuelve el menú |

  - **Receta AliExpress:** `firecrawl_scrape` con `formats:["json"]`, `proxy:"stealth"`,
    `location:{country:"CO"}` y esquema {titulo, precio, unidades_vendidas} — **sin `actions`**.
    El listado ya trae 8-12 en el HTML inicial. 9 créditos.
  - **Más resultados:** `formats:["markdown"]` + `actions` de scroll (`wait 3000` → `scroll down`
    → `wait 2000`, repetido). El scroll infinito SÍ se resuelve. Medido: 182 KB con los contadores
    dentro. ⚠️ Volcar a archivo y `grep`, o a subagente — jamás entero al hilo.
  - ⚠️ **Nunca combinar `json` + `actions`:** timeout (probado 3 de 3).
  - 🏆 **Receta AMAZON por navegador (MEDIDA 2026-08-02 — la mejor fuente del scanner).**
    Navegar a `amazon.com/s?k=<producto>` y extraer del DOM:
    ```js
    document.querySelectorAll('[data-component-type="s-search-result"]')
    // contador de demanda: /([\d.,]+\s*K?\+?)\s+comprados el mes pasado/
    // precio: /COP\s?([\d.,]+)/   ·   rating: /([\d.]+) de 5 estrellas/
    // total de la categoría: /1 a \d+ de ([\d.,]+) resultados/
    ```
    Medido: 48 tarjetas, **34 con contador de ventas (71%)**, 46 con precio, 45 con rating, total
    "155 resultados". Muestra real: `1 K+`, `10 K+`, `300+`. **Amazon detecta Colombia y convierte
    a COP solo** — no hay que forzar país. Da más que AliExpress: ventas + rating + reseñas + total.
  - **Temu y MercadoLibre: NO hay vía sin cuenta.** Los dos exigen inicio de sesión incluso para
    ver resultados de búsqueda. Solo saldrían con `claude-in-chrome` si el usuario **ya tiene
    sesión abierta** en su Chrome. **Preguntárselo, no asumirlo.** Si no la tiene: decir que esa
    fuente no está disponible y seguir con AliExpress + Amazon. Jamás rellenar el hueco a ojo.

  Filtro sugerido: ≥5K órdenes/mes = señal fuerte; cruzar SIEMPRE contra Ad Library del país
  objetivo (que venda en USA/China no prueba que venda COD en Colombia).
- **golden-investigacion-mercado** → para el deep-dive de audiencia una vez elegido el producto.

## Flujo
1. **Encuadre (pregunta si falta):** país, nicho/categoría o producto semilla, **MODELO (catálogo COD / marca propia anticipado)** — define qué columna de la rúbrica se usa — y presupuesto/ticket objetivo.
2. **Barrido de demanda:**
   - `ads_library_search` por palabra clave/categoría en el país → lista anunciantes activos, cuántos anuncios, desde cuándo.
   - `firecrawl_search` para tendencias y precio de costo (AliExpress) + volumen de reseñas.
   - **Scanner de volumen** (si el nicho lo amerita o el usuario pide "escanea la categoría"):
     **dos fuentes, las dos verificadas** — `firecrawl_scrape` con esquema JSON **sobre AliExpress**
     (`proxy:"stealth"` + `location:{country:<país>}`), y **Amazon por navegador** (mejor: da ventas,
     rating, reseñas y el total de la categoría). Rankear por contador de ventas visible.
     Temu y MercadoLibre exigen cuenta: preguntar si hay sesión, y si no, declararlos no disponibles.
   - **Compuerta obligatoria antes de puntuar:** pasar la respuesta por el candado
     `python3 ~/.claude/skills/golden-investigacion-mercado/scripts/candado_scraping.py resp.json
     --pedi "<lo que buscabas>"`. Si dice DESCARTAR, ese producto **no entra a la rúbrica**.
   - **Verificación anti-fantasma (las 4, antes de puntuar):** existe el campo `json`? ·
     `metadata.title` poblado? · `metadata.url` == `sourceURL`? · **el dato responde a lo que pedí?**
     Cualquiera que falle = fuera de la rúbrica, y se reporta "no obtenido" en vez de inventar.
2b. **Keywords, cobertura y cementerio** → aplica `references/ad-library-metodo.md` completo:
   mínimo **8 keywords en 4 capas** (la biblioteca busca por TEXTO: quien escribe "cinturilla" no
   sale si buscas "faja cinturilla"), **registro de cobertura** por keyword ("0 encontradas" no es
   lo mismo que "no revisadas") y el **cementerio** (activos vs históricos = tasa de supervivencia).
   Deduplica por tienda y descarta el ruido antes de contar.

3. **Puntuación** — Score Ganador 0–100 (ver rúbrica). Descarta lo que no pase el umbral (≥60).
4. **Ficha de Producto Ganador** (formato abajo) para los 1–3 mejores.
5. **Siguiente paso:** ofrecer correr `golden-investigacion-mercado` sobre el elegido y luego `golden-shopify` para la página.

## Rúbrica Score Ganador (0–100) — **usa la columna del modelo que corresponda**

| Criterio | **Catálogo / COD** | **Marca propia / anticipado** | Qué mide |
|---|---|---|---|
| **Demanda activa** | 35 | 35 | anunciantes + antigüedad en Ad Library |
| **Margen** | 25 | 20 | precio venta / costo. ≥3× = full. En COD además debe aguantar el flete de las devoluciones |
| **Factor wow / problema visible** | 20 | 10 | se entiende en 3s de video? En marca propia pesa menos: el cliente ya te conoce |
| **Saturación (inverso)** | 10 | 10 | **la curva, abajo**. Ojo: vacío NO es punto dulce |
| **Logística** | 10 | 5 | ligero, no frágil, sin tallas complejas, no restringido. En COD pesa el doble porque la devolución cuesta flete de ida y vuelta |
| **RECOMPRA** 🆕 | — | **20** | se acaba y se vuelve a pedir? Consumible de 30-60 días = full. Compra única = 0 |

**Umbral de descarte: <60 en la columna que aplique.** Ojo con el error de leer la columna
equivocada: un consumible aburrido puede sacar 55 como producto de catálogo y 78 como marca propia,
y al revés un gadget de impulso puede sacar 80 en catálogo y 45 en marca propia porque nadie lo
compra dos veces.

### La curva de saturación (leer el número de tiendas, no solo tenerlo)

| Tiendas activas con el producto | Lectura | Puntos |
|---|---|---|
| **0** | **demanda NO demostrada.** Nadie lo está vendiendo con éxito ahí, y eso no es un hueco: es riesgo. Solo se lanza con presupuesto de test que puedes perder | **3-4, nunca 10** |
| **1-3** | **punto dulce.** Alguien ya probó que vende y todavía hay aire | **8-10** |
| **4-7** | competido. Entrar exige un ángulo o una oferta claramente mejor | **5-7** |
| **8+** | saturado. O el dolor está tapizado de sustitutos con jugadores escalando | **1-4** |

**Vacío no es punto dulce.** Es el error más caro de esta rúbrica: leer "0 competidores" como
"mercado libre" cuando casi siempre significa que ya lo probaron y no funcionó, o que tus keywords
estaban mal. Antes de puntuar un 0, vuelve al registro de cobertura: **si la cobertura es baja, el
0 no es un dato, es un hueco de método.**

### Señal por competidor (qué está haciendo cada uno)

- 🔥 **Escalando** — 10+ anuncios activos del mismo producto, o un creativo repetido muchas veces.
  Alguien está metiendo plata en serio, y eso solo se hace cuando el producto devuelve.
- ✅ **Estable** — anuncios con **30+ días corriendo**. La mejor señal individual que existe: nadie
  paga anuncios un mes de algo que pierde. **Ojo: el MCP no te la va a mostrar** (ver los dos sesgos
  arriba) — esta señal solo se ve abriendo la Ad Library en el navegador.
- 🧪 **Testeando** — pocos anuncios, todos de menos de 14 días. Ni valida ni satura todavía.

## Entregable → `references/entregable.md`

Ahí vive el formato completo: **ficha** de producto (con cementerio, cobertura y confianza),
**mapa de ángulos** con los HUECOS que nadie usa y sus hooks, **lectura de precios** (techo de las
cadenas, piso del margen), **índice de anuncios** con link directo por ID, y el **MODO LOTE** con
ranking comparativo cuando llegan varios productos a la vez.

**El informe se entrega SIEMPRE, aunque el veredicto sea descartar:** un "no" documentado con sus
números ahorra plata y evita re-evaluar lo mismo en tres meses.

## 🏭 SOURCING LOCAL (cuando el producto NO está en Dropi)

Para dropshipping puro el catálogo de Dropi resuelve. Para **marca propia** hay que conseguir
proveedor, y ahí el margen se define: comprar bien es la mitad del negocio.

**Regla de precio:** `costo × 3 = precio de venta mínimo`. Con eso el combo funciona — camiseta a
$12.000 mayorista → venta $36.000 → 3x2 a $108.000 y el cliente percibe que ahorra $36.000.

### Método 1 · Grupos de mayoristas en Facebook (ropa, calzado, accesorios)
Únete sin filtrar a los grupos grandes de tu país. En **Colombia**: busca por las zonas mayoristas
reales — **San Victorino** y **El Restrepo** (Bogotá), **El Hueco** (Medellín) — más "Mayoristas
Colombia", "Proveedores Colombia al por mayor". Los buenos tienen decenas de miles de miembros.
Facebook permite publicar en **hasta 10 grupos a la vez**.

Texto de publicación (funciona por tres razones deliberadas):

```
Busco 10 docenas de [PRODUCTO]. Pago al mejor precio mayorista.
Enviar precio por docena al privado. NO respondo comentarios.
Mucha cantidad disponible = prioridad.
```

- **"10 docenas"** señala volumen y filtra de entrada al que vende al detal.
- **"NO respondo comentarios"** fuerza el privado y evita que la competencia vea el hilo.
- **"mucha cantidad = prioridad"** invierte la relación de poder: el proveedor compite por ti.

### Método 2 · Búsqueda asistida (gadgets, tecnología, hogar)
Pide proveedores **locales** excluyendo explícitamente AliExpress y Alibaba, con precio de
referencia, enlace y WhatsApp. Para cosmética y limpieza, lo mismo pero pidiendo **laboratorios
de marca blanca** con precio por unidad, cantidad mínima y tiempo de producción.

> ⚠️ **Verificación obligatoria.** Aquí es exactamente donde un modelo inventa proveedores,
> teléfonos y precios que no existen. **Ningún proveedor devuelto por IA entra a una ficha sin
> confirmarse** por Firecrawl o por llamada. Regla global de datos reales antes de generar.

### Cómo se evalúa un proveedor (6 factores)
Precio con escala por volumen · stock actual real · capacidad de **reposición y continuidad**
(un ganador sin reposición es un problema, no una oportunidad) · si despacha a la transportadora
o solo entrega en bodega · tiempos de entrega · calidad de la comunicación.

### Señales de que hay que salir corriendo
Sin fotos claras del producto · no da precio hasta que insistes tres veces · stock de 10-20
unidades (ese no es mayorista) · no hace envíos · tarda días en responder. **Si tarda días
contigo mientras te está vendiendo, imagina cuando ya te cobró.**

## Referencias de esta skill
- **`references/ad-library-metodo.md`** — cómo se mide de verdad: los 2 sesgos del MCP con sus
  cifras, el **cementerio** (activos vs históricos = supervivencia), keywords en 4 capas, registro
  de cobertura y filtrado de ruido. **Lectura obligatoria antes de un veredicto de saturación.**
- **`references/entregable.md`** — ficha, mapa de ángulos con HUECOS, lectura de precios, índice de
  anuncios con link por ID y el MODO LOTE con ranking comparativo.

## Cierre obligatorio
Tras entregar la ficha, pregunta: «Investigo a fondo el avatar con `golden-investigacion-mercado` y monto la página con `golden-shopify`?»

## Changelog
- **GPG1.6** (2026-08-01) — **AUTOCORRECCIÓN de GPG1.4: había sobre-generalizado desde un solo
  sitio.** GPG1.4 declaró el scanner de volumen "migrado a Firecrawl" para Temu/AliExpress/Amazon
  habiendo probado **solo AliExpress**. Ejecutadas las tres el 2026-08-01: **AliExpress ✅ ·
  Temu ❌ · Amazon ❌ · TikTok Creative Center ❌.** Temu redirige la búsqueda a la portada y
  devuelve 72 categorías de ropa con precio "N/A"; Amazon responde con muro anti-bot y **sin campo
  `json`**; TikTok CC es una app JS que solo entrega su menú. Matriz de fuentes ahora en la skill,
  fuente por fuente, con su estado medido. Para Temu/Amazon vuelve el Chrome MCP — y se prohíbe
  simular que Firecrawl los cubre.
  🚨 **Regla Cero ampliada de 1 a 3 modos de fallo.** El check de `metadata.title` de GPG1.4 solo
  cazaba la alucinación total. Temu falla con `title` **poblado** (modo señuelo) y Amazon falla con
  `title` poblado **y** sin redirección (modo muro). Se añade la verificación que sí caza los tres:
  **"el dato responde a lo que pedí?"**. Lección de método, la misma de GPG1.5: no basta con
  ejecutar la herramienta una vez — hay que ejecutarla contra **cada fuente que la skill promete**.
- **GPG1.4** (2026-07-31) — **Scanner de volumen migrado de Chrome MCP a Firecrawl** y Regla Cero
  anti-fantasma. Probado en vivo el mismo día: (1) el scroll infinito de AliExpress/Temu/Amazon
  **ya NO es un obstáculo** — `actions` de scroll + `proxy:"stealth"` lo sacan (182 KB reales con
  los contadores "480 sold" dentro), así que la limitación que esta skill documentaba quedó
  derogada; (2) la receta rápida es `json` + schema **sin actions** (8 productos reales con precio
  y unidades vendidas, 9 créditos) porque el listado ya trae 8-12 en el HTML inicial;
  (3) **nunca combinar `json` + `actions`**: timeout probado 2 de 2; (4) `location:{country:"CO"}`
  obligatorio o salen precios de USA. Chrome MCP baja a respaldo (solo si hace falta sesión).
  🚨 Y lo más importante: **el extractor INVENTA cuando la página viene hueca** — devolvió
  *"Smart TV 55\" 4K LED, $499.99, 150 reseñas"* para una página de removedor de verrugas con
  `statusCode: 200`. Un producto fantasma puntuado en la rúbrica manda a testear algo que no existe,
  con presupuesto real. Verificación obligatoria de `metadata.title` antes de puntuar.
  📖 Manual: `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección **AUTO-MEJORA** (mandato global de FER, autorización permanente). Sin esta sección la skill no se auto-calificaba al cerrar corrida. Contenido operativo intacto. Backup: `_backups/2026-08-02-loop-arsenal-s1/`.
