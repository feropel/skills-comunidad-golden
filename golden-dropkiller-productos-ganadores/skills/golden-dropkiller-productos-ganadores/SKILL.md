---
name: golden-dropkiller-productos-ganadores
description: >-
  Golden Group — Caza y validación de PRODUCTOS GANADORES para dropshipping COD y marca
  propia en LatAm. Pregunta qué quieres hacer hoy con todos los filtros a la vista (nicho,
  país, ventas, antigüedad de anuncios, competencia, canal) y, si no sabes, busca todo. Caza
  con DropKiller separando ventas reales de ajustes de stock y sumando proveedores, cruza la
  Meta Ad Library, AliExpress y Amazon, y calcula el PVP mínimo que deja plata. Entrega una
  LISTA DE CAZA verificada o una FICHA DE PRODUCTO GANADOR. Úsala SIEMPRE que diga: "qué
  vendo", "dame productos ganadores", "dame 10 winners de mascotas", "busca en DropKiller",
  "qué se está vendiendo en Dropi", "productos sin escalar", "valida este producto", "está
  quemado", "cuántos proveedores lo tienen", "está saturado", "quién lo está vendiendo", "a
  cuánto lo vendo", "me deja plata", "espía esta tienda", "sácame creativos de este producto" o
  "prográmame ganadores todos los días". También en LOTE con ranking comparativo.
---
<!-- Historial completo de esta skill: references/changelog.md. El cuerpo se paga en cada activación; el acta no. -->
<!-- skill GPG1.25 · 2026-09-23 · la comisión de recaudo era un cobro DUPLICADO (ya va dentro del flete): pasa a 0 y de supuesta a medida, comprobada en 17 informes (1 entregado de 11.669 con comisión > 0); la tabla de multiplicadores baja a 7,02x/4,01x/3,01x/2,20x; el término sigue vivo tras --comision; banco de 19 a 21 casos. GPG1.24: renombrada a golden-dropkiller-productos-ganadores por orden de FER (antes golden-productos-ganadores). GPG1.23: ruta R7: problema validado afuera contra el de aquí, con el múltiplo corregido por tamaño de mercado y el conteo local depurado por moneda. GPG1.22: openpyxl está en los tres intérpretes (medido); la skill decía que solo en uno. GPG1.21: la declaración de fábrica pasa al literal que el registro sí lee. GPG1.20 (2026-09-18): quinta pasada: entrega_golden sobre comun, tasas con rango, coma de miles, enlaces por parser de URL, status que falta = activo. GPG1.19: cuarta pasada: comun.py unifica identidades, números y fechas; rangos en todas las banderas; canal más libre (9C); exclusión de empresa por ID; la lista del día sale de correr_lote.py y se reproduce. GPG1.18: calibración rehecha con backtest v2 sin sesgo de resultado (piso 10 firme, 31 prudente, techo 120 sin evidencia, frenando = aviso), empresas separadas en la entrega, errores controlados, filtros del menú con bandera. GPG1.17: entrega propia de Golden, lote + registro + seguimiento, canal por imagen+descripción con cementerio, precio de competencia por Shopify JSON, un solo juicio. GPG1.16: 35 fallas del verificador adversarial corregidas (datos que faltan nunca aprueban, menú que el script sí aplica, blindaje real, reglas derogadas fuera). GPG1.15: primera corrida real: trampas 9 (maxTotalSold no existe) y 10 (espejos que no cuadran → mediana salvo el más viejo). Base GPG1.14: MODO CAZA CON DROPKILLER, por orden directa de FER ("una skill poderosa, mucho más que la de Juan, que me pregunte qué quiero hacer hoy con todos los filtros explícitos, y si no sé, que busque todo; 10 ganadores todos los días"). Base: 39 de 40 videos leídos completos (21 del cofundador de DropKiller) y el conector medido herramienta por herramienta. Aporte propio MEDIDO: 9 de los 20 "ganadores" de DropKiller en Colombia eran ventas FANTASMA (ajustes de stock) → scripts/ventas_reales.py; el mismo producto aparece hasta 4 veces por plataformas espejo → scripts/consolidar_mercado.py; conteo de reabastecimientos que DropKiller no da. Además: leyes del caso Candida (ETIQUETA y ALÉRGENOS), economía COD mudada a references/economia-cod.md con la contradicción del CPA corregida, y dos reglas de "costo × 3" que sobrevivían en entregable.md alineadas con viabilidad_cod.py. Detalle en references/changelog.md. -->
# Golden Group — Productos Ganadores


**Versión:** `GPG1.25.1` (ver `references/changelog.md`) ·
**Fábrica:** chat «✅ SKILL golden-dropkiller-productos-ganadores» (abierto el 2026-09-05 por
orden de FER, renombrado con la skill el 2026-09-22;
ejecuta, no manda: la autoridad es FER → Centro de Mando → skill, y el CdM puede cambiarlo).
El literal va en esta forma exacta porque `registro-arsenal.py` **rechaza la prosa a propósito**:
la versión anterior decía "el chat de FER abierto el 2026-09-18", que ninguna otra sesión puede
resolver, y el registro la leyó —con razón— como "sin fábrica declarada".
· **Blindaje:** `golden-blindaje` (chmod `0444`/`0555` y encima `chflags uchg`; medido el
2026-09-18: `uchg` en todos los nodos). Abrir con `golden-blindaje golden-dropkiller-productos-ganadores`,
cerrar con `golden-blindaje golden-dropkiller-productos-ganadores --cerrar`. `chmod` solo NO abre.

Objetivo: pasar de "no sé qué vender" a **productos validados con evidencia**, en minutos: una
**lista de caza** verificada cuando se buscan candidatos, y una **ficha** cuando se valida uno.
Herramientas: Meta Ad Library, DropKiller (conector de pago, plan Advance), Firecrawl y el
navegador.

## Antes de empezar — lo que TÚ tienes que tener

Cada modo usa fuentes distintas. Lo bloqueante para lo que depende de él; lo demás se sigue con lo que haya, y lo que falte se dice en una línea al arrancar.

| Qué necesitas | Tipo | Para qué | Cómo se consigue |
|---|---|---|---|
| **DropKiller**, en un plan que incluya su **conector MCP**, conectado a Claude | Bloqueante para CAZA, CREATIVOS y RUTINA · degradable para ESPIAR | Ventas por producto de Dropi y otras plataformas, anuncios y tiendas. En ESPIAR queda la Ad Library por dominio | Tu cuenta en DropKiller. La skill se midió con el plan Advance: revisa el precio vigente en su web. Declaración: el autor de esta skill (FER, de Golden Group) tiene enlace de afiliado de DropKiller (15%) |
| **La biblioteca de anuncios de Meta**: el MCP de Meta con `ads_library_search`, o la biblioteca abierta en el navegador | Degradable · sin ninguna de las dos vías, bloqueante para la ruta R7 | En VALIDAR da hasta 35 de los 100 puntos (Demanda activa): sin ella quedan 65 y hay que sacar 60 en el resto, y la Regla de oro 1 exige al menos una tendencia clara, declarada. R7 depende entera de ella. En CAZA confirma la competencia que DropKiller ya contó | El MCP, con tu cuenta de Meta conectada a Claude. Si no, la biblioteca es pública y no pide sesión: se abre en el navegador con la URL completa de `references/ad-library-metodo.md` |
| **Python 3** y conexión a internet | Bloqueante | Las ventas de DropKiller nunca se usan crudas (`scripts/ventas_reales.py`) y el precio se calcula (`scripts/viabilidad_cod.py`). Esos scripts solo usan lo que trae Python; `competencia.py precios` lee las páginas de la competencia por internet | Compruébalo con `python3 --version`; si no está, en python.org |
| **Firecrawl** conectado y con créditos | Degradable | AliExpress: costo y contador de ventas | Tu cuenta de Firecrawl. Se prueba una llamada antes de contar con él |
| **El navegador de Claude** | Degradable | Amazon (contador de ventas, precio y rating), que por Firecrawl no sale, y la antigüedad de los anuncios en la Ad Library cuando el total pasa de 50 | Viene con la app; o Claude en Chrome |
| *Opcional:* **sesión abierta en Temu y en MercadoLibre**, en tu Chrome con Claude en Chrome | Degradable | Esas dos tiendas piden iniciar sesión hasta para buscar | Se te pregunta al arrancar, no se asume |
| *Opcional:* la skill **`golden-investigacion-mercado`** | Degradable | Su `candado_scraping.py` es la compuerta anti-fantasma antes de puntuar | Entre tus skills. Sin ella se aplican a mano las 4 verificaciones de la Regla Cero y se dice en el informe |
| *Opcional:* **los informes por producto de Dropi de tu empresa** y **`openpyxl`** | Degradable | La tasa de entrega real de un producto que ya vendiste (`scripts/entrega_golden.py construir`) | El nombre del archivo tiene que contener `por producto`: el nombre con que lo baja Dropi (`ordenes_productos_*.xlsx`) no lo encuentra, así que se renombra. `python3 -c "import openpyxl"`; si falta: con el Python de python.org, `pip3 install openpyxl`; con el de Homebrew, `python3 -m venv ~/venv-caza`, `~/venv-caza/bin/pip install openpyxl`, y `construir` se corre con `~/venv-caza/bin/python3` |
| **Tu sí explícito**, con hora, país y destino | Bloqueante para RUTINA | La tarea diaria no se crea sin eso, y antes se corre una vez a mano para ver que el conector responde en una sesión programada | Se te pregunta (`assets/tarea-diaria-caza.md`) |

**Lo bloqueante para lo que depende de él:** sin el conector de DropKiller, CAZA, CREATIVOS y RUTINA no corren. En CAZA se dice y se ofrece VALIDAR (Ad Library, AliExpress y Amazon) y la extensión gratuita de DropKiller en Chrome (`references/dropkiller-caza.md`, apartado 8); la rutina se detiene y lo deja escrito en su archivo de salida. Sin la biblioteca de anuncios, ni por MCP ni por navegador, no corre R7, y en VALIDAR la ficha lo declara y exige al menos una tendencia clara. **Lo degradable se pide y se sigue:** la fuente que no responde se declara NO DISPONIBLE en la ficha y jamás se rellena a ojo; sin informes propios, se usa la tasa de entrega general y se dice. Si no tienes algo, dime y te guío paso a paso.

## Arranque: qué quieres hacer hoy
Si el usuario no dijo ya el encargo, **muestra el menú de `references/menu-arranque.md` en UN
solo mensaje** (objetivo, nicho, país, modelo, etapa, ritmo, antigüedad de anuncios,
competencia, canal, precio y stock, rutas, cuántos). Lo que conteste "no sé" toma el valor por
defecto de esa tabla, y no se vuelve a preguntar. Si el encargo ya viene claro, arranca y
declara en una línea qué supusiste. Los cinco modos:

| Modo | Cuándo | Cómo |
|---|---|---|
| **CAZA** | "dame ganadores", "qué vendo", nicho sin producto | DropKiller → `references/dropkiller-caza.md` → **lista de caza** (`entregable.md` §7) |
| **VALIDAR** | un producto concreto (nombre, link, foto) o varios (LOTE) | el **Flujo** de abajo → **ficha** (`entregable.md` §1) |
| **ESPIAR** | un dominio o una tienda competidora | `brief_store` + `store_tech_report` de DropKiller y la Ad Library por dominio |
| **CREATIVOS** | "ángulos y anuncios de un producto que ya vendo" | `semantic_search_ads` por imagen, otros países, ≥7 días, más duplicados |
| **RUTINA** | "todos los días", "déjalo programado" | `assets/tarea-diaria-caza.md`: crear la tarea SOLO con el sí explícito del usuario |

## Reglas de oro
1. **Nunca recomiendes un producto sin evidencia de demanda activa.** Mínimo: anuncios corriendo HOY en la competencia (Meta Ad Library) o tendencia clara.
2. **EL MODELO DEFINE EL GANADOR** (se pregunta en el menú de arranque; si no sabe: catálogo COD,
   declarado). Golden opera los dos y **el producto ganador es distinto en cada uno**:
   - **Catálogo / contra entrega** → producto de **impulso**, problema-solución visible en 3s de
     video, ligero y no frágil (**cada pedido fallido cuesta $12.518 medidos**, un solo cobro).
     El precio NO se juzga a ojo: **se calcula** con `scripts/viabilidad_cod.py`.
     Es venta **única**: el producto tiene que ganar en la primera compra o no gana.
   - **Marca propia / pago anticipado** → aquí manda la **RECOMPRA**. Un consumible que se acaba en
     30-60 días vale más que un ganador de impulso que se compra una vez, porque el segundo pedido
     no cuesta pauta. Aguanta ticket más alto y menos "wow", pero exige **calidad sostenida y
     reposición asegurada**: una marca propia que se queda sin stock pierde al cliente recurrente,
     no solo la venta.
3. **Cierra siempre con el entregable** (lista de caza o ficha) y el siguiente paso
   (investigación → golden-shopify).
4. **Las cifras de DropKiller NO se usan crudas.** Toda venta pasa por `scripts/ventas_reales.py`
   y todo mercado por `scripts/consolidar_mercado.py`. Medido el 2026-09-18: 9 de los 20
   "ganadores" de Colombia eran ajustes de stock (el #1 y el #2), y un mismo producto salía hasta
   4 veces por plataformas espejo. A la ficha van las ventas DEPURADAS, nunca las reportadas.
5. **La ficha técnica sale de la ETIQUETA del producto que se despacha**, jamás de la descripción
   del proveedor ni de la de un competidor: **dos tiendas pueden vender el mismo nombre comercial
   con fórmulas distintas**. Caso Candida Cleanse (2026-09-05): una ficha copiada de un
   competidor publicó cinco ingredientes que el frasco no tiene. **Ampliar el envase** (foto del
   frasco, fotograma del video del proveedor) es un paso de la investigación, no un extra: el
   dato estaba en la foto, no en el texto.
6. **Toda advertencia de ALÉRGENO del envase se publica.** Es lo único de una ficha que puede
   hacerle daño físico a una persona (en el caso Candida, nuez negra sin declarar en un
   suplemento). Sin etiqueta a la vista, ficha técnica y alérgenos se entregan **PENDIENTES**.
7. **Cuando el material del cliente contradice tu trabajo, la hipótesis por defecto es que el
   error es TUYO.** Y antes de dar por bueno material heredado, mira **qué producto sale en
   cámara**: en el caso Candida, 2 de 6 videos mostraban otro frasco; en contra entrega eso
   termina en el paquete rechazado en la puerta.
8. **Piezas prohibidas** en todo lo que salga de aquí, aunque lo enseñe un video: aval médico
   inventado, promesa de cura, testimonios fabricados, bot que se hace pasar por especialista,
   país quemado en la imagen, dominios de terceros, marcas ajenas en catálogo público, y productos
   para adultos (la política de Meta "Productos o servicios para adultos" no permite anunciar su
   venta: sin pauta no hay modelo COD).
9. **Un cero se prueba, no se cree. Sin costo del proveedor no hay PVP mínimo**, solo ranking
   relativo, y se dice. Donde haya cifra, se cita la fuente que la mide.

## Fuentes (todas conectadas)
- **DropKiller** (conector MCP, **beta**, plan Advance) → ventas por producto de Dropi y otras 9
  plataformas en 15 países, anuncios de Meta y TikTok, tiendas Shopify y TikTok Shop. Es la
  fuente del modo CAZA. **Método completo, las 30 herramientas y las 10 trampas medidas →
  `references/dropkiller-caza.md`. Lectura obligatoria antes de la primera llamada.**
  - 🔴 Sus "ventas" salen de la **caída de stock** del proveedor: un ajuste de inventario parece
    venta (9 de 20 en su propio top de Colombia). Nunca crudas: `ventas_reales.py`.
  - Encuentra candidatos y creativos. **No** cuenta competencia: los anunciantes se cuentan en la
    Ad Library de Meta (lo dice su propio cofundador: "AdsKiller no lo uso para eso").
  - 🔴 Conflicto de interés doble: el método viene del **cofundador** de la herramienta, y **FER
    tiene enlace de afiliado** (15%). Se declara en cada entregable que la recomiende.
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
- **Investigación profunda multi-fuente** (cuando el usuario quiere un barrido verificado de un
  nicho entero): `WebSearch` + `firecrawl_search` (y `firecrawl_agent` si está conectado). No hay
  skill "deep-research" instalada en el arsenal — verificado 2026-08-24; para el deep-dive de un
  producto YA elegido, la vía sigue siendo `golden-investigacion-mercado`.
- **Scanner de volumen visible** → las tiendas muestran el contador de ventas en el listado
  ("5K+ vendidos este mes", "10K+ bought"). Esa cifra es demanda DURA al nivel de producto —
  complementa la Ad Library (que prueba que alguien PAUTA, no que vende).

  **Qué fuente responde de verdad (MEDIDO 2026-08-01 — no asumir, está probado una por una):**

  | Tienda | Estado | Cómo |
  |---|---|---|
  | **DropKiller** | ✅ **Funciona, con 10 trampas** | **MCP** (medido 2026-09-18, 30 herramientas). Ventas depuradas con `ventas_reales.py` |
  | **AliExpress** | ⚠️ **Sin créditos el 2026-09-18** | **Firecrawl.** Medido antes: 8 productos con "480 sold", "3,000+ sold". El 18-sep `firecrawl_scrape` respondió "Insufficient credits" (1 llamada): probar una antes de contar con él; si falla, AliExpress se declara NO DISPONIBLE en la ficha. Los precios de competencia en Shopify no dependen de Firecrawl (`competencia.py precios`) |
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

## Flujo del modo CAZA (DropKiller)
Embudo de lo barato a lo caro; cada paso descarta antes de gastar la llamada siguiente. Detalle,
herramienta por herramienta, en `references/dropkiller-caza.md` §6.
1. **Candidatos**: las rutas R1-R7 que eligió el menú (`dropkiller-caza.md` §5), el triple de lo
   que se va a entregar. Stock mínimo 80 salvo que el usuario diga otra cosa. La R7 (problema
   validado afuera) entrega PROBLEMAS: cada uno necesita que se encuentre el producto que lo
   resuelve antes de entrar al paso 2, y se dice cuál se eligió y por qué.
2. **Ventas reales**: `get_product_history` (o el `history30d` de la búsqueda semántica)
   guardado en un archivo. **Con más de 3 candidatos, todo va en lote**: una carpeta por
   candidato (`ficha.json`, `historial.json`, `mercado.json`, `anuncios.json`) y
   `scripts/correr_lote.py <corrida> --pais XX --precios --registro
   PROYECTOS/CAZA-DIARIA-GANADORES/_registro.jsonl` pasa todos por los pasos 2 a 6 de una vez y
   registra CADA candidato visto, no solo los elegidos. Uno suelto →
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/ventas_reales.py <archivo>`.
   Fuera FANTASMA. DUDOSO solo entra si no alcanzan los REAL, marcado.
3. **Mercado consolidado**: `semantic_search_products` con la imagen y el país (y `search_products`
   con una palabra clave corta si la imagen trae poco) guardado en un archivo →
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/consolidar_mercado.py <archivo>
   --pais <XX> --incluir "<regex del nombre>" [--etapa …] [--max-proveedores N]`, con lo que
   eligió el menú. Fuera lo que no cumpla el criterio 1 (etapa) o el 2 (proveedores). El regex lo
   decide quien mira las fotos, no el script. Sus avisos van a la tarjeta, no se callan.
4. **Plata**: `viabilidad_cod.py --costo <salePrice>` → PVP mínimo. **Entrega propia primero**:
   si la empresa ya vendió ese PRODUCTO ID de Dropi (= `externalId` de DropKiller), su tasa real
   sale de `scripts/entrega_golden.py consultar PROYECTOS/CAZA-DIARIA-GANADORES/_entrega_golden.json
   --producto-id <id>` y se pasa con `--entrega`. Medido en los pedidos reales de Golden: va de
   58,9% a 96,8% según el producto, contra el 73,5% plano. Si no lo vendió, tasa general y se
   declara. El agregado se reconstruye con `python3 scripts/entrega_golden.py construir
   "<INFORMES DROPI de la empresa>" --salida <json>` (una empresa por archivo, nunca mezcladas;
   el JSON queda FUERA de la skill porque son datos internos). Si la competencia vende por
   debajo del mínimo, se marca y baja en el ranking.
5. **Riesgo**: marca ajena fuera; salud y suplementos con las banderas de etiqueta y alérgenos
   (reglas 5, 6 y 8).
6. **Anunciantes y precio de la competencia**: `semantic_search_ads` con la IMAGEN del producto
   + una DESCRIPCIÓN corta + el país (nunca la imagen sola: medido 0 de 13 relevantes; con
   descripción, 14 de 14) guardado en `anuncios.json` →
   `scripts/competencia.py canal anuncios.json` (activos hoy y CEMENTERIO: los que lo soltaron) y
   `scripts/competencia.py precios anuncios.json --pvp-minimo <$>` (lee el precio de las landings
   Shopify; medido 7 de 7). La Ad Library por palabra clave queda para confirmar por nombre de página.
7. **Creativos y ángulo** de otros países: `semantic_search_ads` con la imagen, validated o
   evergreen, más duplicados primero.
8. **Filtros del menú** (ritmo de 7 días, proveedores, anunciantes, precio, stock): el que rompe
   uno va a la sección CASI, no a la lista. Lo que no se aplicó se declara en la cabecera.
9. **Lista de caza** con el formato de `references/entregable.md` §7, rankeada con el orden de
   `dropkiller-caza.md` §6 paso 9, con su embudo, su sección CASI y sus descartados. Nunca se
   rellena para llegar al número.

## Flujo del modo VALIDAR (un producto o un lote)
1. **Encuadre (pregunta si falta):** país, nicho/categoría o producto semilla, **MODELO (catálogo COD / marca propia anticipado)** — define qué columna de la rúbrica se usa — y presupuesto/ticket objetivo.
2. **Barrido de demanda:**
   - `ads_library_search` por palabra clave/categoría en el país → lista anunciantes activos, cuántos anuncios, desde cuándo.
   - `firecrawl_search` para tendencias y precio de costo (AliExpress) + volumen de reseñas.
   - **Scanner de volumen** (si el nicho lo amerita o el usuario pide "escanea la categoría"):
     **dos fuentes, las dos verificadas** — `firecrawl_scrape` con esquema JSON **sobre AliExpress**
     (`proxy:"stealth"` + `location:{country:<país>}`), y **Amazon por navegador** (mejor: da ventas,
     rating, reseñas y el total de la categoría). Rankear por contador de ventas visible.
     Temu y MercadoLibre exigen cuenta: si no hay sesión abierta, declararlos no disponibles y seguir (no se pregunta a mitad de la corrida: el menú ya se hizo al arrancar).
   - **Compuerta obligatoria antes de puntuar:** pasar la respuesta por el candado
     `python3 ~/.claude/skills/golden-investigacion-mercado/scripts/candado_scraping.py resp.json
     --pedi "<lo que buscabas>"`. Si dice DESCARTAR, ese producto **no entra a la rúbrica**.
     **Si el script no existe o falla** (la skill hermana se movió o se renombró): no te detengas —
     aplica a mano las 4 verificaciones anti-fantasma de la Regla Cero (existe `json`? ·
     `metadata.title` poblado? · `metadata.url` == `sourceURL`? · el dato responde a lo que pedí?) y
     dilo en el informe: "compuerta automática no disponible, verificación manual aplicada".
   - **Verificación anti-fantasma (las 4, antes de puntuar):** existe el campo `json`? ·
     `metadata.title` poblado? · `metadata.url` == `sourceURL`? · **el dato responde a lo que pedí?**
     Cualquiera que falle = fuera de la rúbrica, y se reporta "no obtenido" en vez de inventar.
2b. **Keywords, cobertura y cementerio** → aplica `references/ad-library-metodo.md` completo:
   mínimo **8 keywords en 4 capas** (la biblioteca busca por TEXTO: quien escribe "cinturilla" no
   sale si buscas "faja cinturilla"), **registro de cobertura** por keyword ("0 encontradas" no es
   lo mismo que "no revisadas") y el **cementerio** (activos vs históricos = tasa de supervivencia).
   Deduplica por tienda y descarta el ruido antes de contar.
   **Calcula cobertura% y supervivencia% con el script, no a mano** (evita error de redondeo/memoria):
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/metricas_saturacion.py cobertura
   --reportado <N> --revisados <N>` y `python3
   ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/metricas_saturacion.py cementerio --activos <N>
   --historicos <N>`.

2c. 🔴 **COMPUERTA DE VIABILIDAD (COD)** — antes de puntuar, la cuenta:
   `python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/viabilidad_cod.py --costo <costo>
   --pvp <pvp>`. Sin `--pvp` devuelve el **PVP mínimo** y su multiplicador, que es lo que se le
   dice al usuario cuando aún no hay precio decidido. **Lo que no pasa el piso no entra a la
   rúbrica**, por bueno que se vea: con los números reales de Golden, un producto de costo
   $30.000 a $80.000 PIERDE $1.860 por pedido generado. **Siempre se declara que el CPA es un
   supuesto**, no un dato medido.

3. **Puntuación** — Score Ganador 0–100 (ver rúbrica). Descarta lo que no pase el umbral (≥60).
4. **Ficha de Producto Ganador** (formato abajo) para los 1–3 mejores.
5. **Siguiente paso:** ofrecer correr `golden-investigacion-mercado` sobre el elegido y luego `golden-shopify` para la página.

## Rúbrica Score Ganador (0–100) — **usa la columna del modelo que corresponda**

**Un solo juicio, no dos.** Si el producto pasó por la caza, su ESTADO de `correr_lote.py`
(LISTA / CASI / FUERA) manda sobre el puntaje: la rúbrica ordena y explica DENTRO de ese estado,
nunca lo contradice. Un FUERA no se rescata con puntos (un fantasma o un quemado con 90 sigue
FUERA) y un CASI lleva su motivo al lado del número. Si el producto llega directo a VALIDAR, se
corre primero `correr_lote.py` con él solo, para que tenga estado.

| Criterio | **Catálogo / COD** | **Marca propia / anticipado** | Qué mide |
|---|---|---|---|
| **Demanda activa** | 35 | 35 | anunciantes + antigüedad en Ad Library |
| **Margen** | 25 | 20 | **NO se estima: se corre `scripts/viabilidad_cod.py`.** Puntos = holgura sobre el piso de $8.000 por pedido generado. En COD es además COMPUERTA (abajo) |
| **Factor wow / problema visible** | 20 | 10 | se entiende en 3s de video? En marca propia pesa menos: el cliente ya te conoce |
| **Saturación (inverso)** | 10 | 10 | **la curva, abajo**. Ojo: vacío NO es punto dulce |
| **Logística** | 10 | 5 | ligero, no frágil, sin tallas complejas, no restringido. En COD pesa el doble porque cada devolución cuesta un pedido fallido (UN solo cobro, `economia-cod.md`) y no recauda |
| **RECOMPRA** 🆕 | — | **20** | se acaba y se vuelve a pedir? Consumible de 30-60 días = full. Compra única = 0 |

### 🔴 COMPUERTA DE VIABILIDAD (COD): antes de puntuar nada

```bash
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/viabilidad_cod.py --costo <costo> --pvp <pvp>
```
**Si no pasa el piso de $8.000 por pedido GENERADO, el producto se DESCARTA aunque saque 95 en
todo lo demás.** La puntuación mide qué tan bueno es el producto; la compuerta, si el negocio
existe. Sin `--pvp` devuelve el PVP mínimo. A la ficha va **el PVP mínimo en pesos, nunca un
multiplicador**: el "3×" solo es cierto cerca de un costo de $30.000 (un producto de $10.000
necesita 7,02×). Números medidos sobre 18.391 pedidos de Dropi: entrega 73,5%, flete $15.664,
pedido fallido $12.518 (un solo cobro), CPA $21.428 **medido como piso**, comisión de recaudo
**0** desde el 2026-09-23: la gestión de cobro ya va dentro del flete y restarla aparte la
cobraba dos veces. **Ya no queda ningún supuesto; lo que se declara en cada veredicto es que el
CPA es un PISO** y por tanto el veredicto es optimista. Historia completa, errores que se
compensaban y porqués → **`references/economia-cod.md`**.

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
cadenas, piso del margen), **índice de anuncios** con link directo por ID, el **MODO LOTE** con
ranking comparativo cuando llegan varios productos a la vez, la **regla de entrega** (aplica
siempre, incluso si el veredicto es descartar) y la **LISTA DE CAZA** del modo caza y de la
rutina diaria (§7: cabecera con el embudo, una tarjeta por producto y los descartados).

## 🏭 SOURCING LOCAL (cuando el producto NO está en Dropi)

Para dropshipping puro el catálogo de Dropi resuelve. Para **marca propia** hay que conseguir
proveedor, y ahí el margen se define: comprar bien es la mitad del negocio. Método completo (grupos
mayoristas, búsqueda asistida, los 6 factores para evaluar proveedor, señales de alarma) →
**`references/sourcing-local.md`. Léela solo cuando el flujo llegue a esta decisión** — no hace
falta en cada corrida.

## Referencias de esta skill
- **`references/ad-library-metodo.md`** — cómo se mide de verdad: los 2 sesgos del MCP con sus
  cifras, el **cementerio** (activos vs históricos = supervivencia), keywords en 4 capas, registro
  de cobertura y filtrado de ruido. **Lectura obligatoria antes de un veredicto de saturación.**
- **`references/entregable.md`** — ficha, mapa de ángulos con HUECOS, lectura de precios, índice de
  anuncios con link por ID, el MODO LOTE con ranking comparativo, y la **regla de entrega** (el
  informe se entrega siempre, hasta cuando el veredicto es descartar).
- **`references/sourcing-local.md`** — conseguir proveedor cuando el producto no está en Dropi:
  grupos mayoristas, búsqueda asistida, evaluación de proveedor, señales de alarma.
- **`references/menu-arranque.md`** — el menú de "qué quieres hacer hoy" con todas las opciones
  de cada filtro, su valor por defecto cuando el usuario no sabe y a qué filtro de DropKiller
  se traduce. **Léela al empezar cualquier invocación sin encargo claro.**
- **`references/calibracion.md`** — qué umbrales están MEDIDOS contra historia real y con qué
  fuerza (backtest v2 del 2026-09-18: piso de 10 firme, 31 indicio, techo de 120 sin evidencia,
  frenado y reabastecimientos sin medir) y cuáles siguen heredados; el v1 superado y por qué;
  cómo repetirlo. Léela antes de cambiar cualquier umbral.
- **`references/dropkiller-caza.md`** — las 30 herramientas del conector, las 10 trampas medidas,
  los 3 criterios del catálogo público con la tabla de etapas por país, las 6 rutas de caza, el
  embudo y lo que se rechaza aunque lo enseñen los videos. **Léela antes de la primera llamada
  a DropKiller.**
- **`references/economia-cod.md`** — por qué el margen se calcula y no se estima: los números
  medidos, el error de $29.182, los dos errores que se compensaban y la tabla de
  multiplicadores. **Léela cuando se discuta un precio o antes de tocar
  `assets/economia-cod-golden.json`.**
- **`assets/tarea-diaria-caza.md`** — el prompt de la rutina diaria (modo RUTINA).

## Cierre obligatorio
Tras entregar la ficha, pregunta: «Investigo a fondo el avatar con `golden-investigacion-mercado` y monto la página con `golden-shopify`?»
Tras entregar una lista de caza, pregunta cuál de la lista se valida a fondo (modo VALIDAR), y si
no está programada, ofrece la rutina diaria en una línea.

## Changelog
Historial completo, versión por versión, en `references/changelog.md` — el cuerpo se paga en
cada activación y el acta no; por eso vive ahí, no aquí (ver comentario bajo el H1).

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección **AUTO-MEJORA** (mandato global de FER, autorización permanente). Sin esta sección la skill no se auto-calificaba al cerrar corrida. Contenido operativo intacto. Backup: `_backups/2026-08-02-loop-arsenal-s1/`.

## Fronteras y desambiguacion

NO usar para analizar pauta propia (eso es golden-meta-ads-analysis) ni para construir la página (eso es golden-shopify).
El estudio de mercado 360° de un producto YA elegido (identificación forense por foto, voz del
cliente, dossier psicológico) es `golden-investigacion-mercado`; esta skill caza y valida, no
hace el estudio. Montar la campaña es `golden-ads`.

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-dropkiller-productos-ganadores
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-dropkiller-productos-ganadores
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.

Nueve de los diez scripts traen su autoprueba (`metricas_saturacion.py` no la tiene: es un cálculo de dos números). `comun.py` es la ÚNICA forma de normalizar IDs, nombres, números y fechas: los demás la importan (solo biblioteca estándar de Python 3). Si una sale con
fallo, ese script no se usa para juzgar productos hasta arreglarlo:
```bash
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/ventas_reales.py --autoprueba       # 43 casos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/consolidar_mercado.py --autoprueba  # 52 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/viabilidad_cod.py --autoprueba      # 21 casos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/competencia.py --autoprueba         # 28 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/correr_lote.py --autoprueba         # 29 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/entrega_golden.py --autoprueba       # 21 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/seguimiento.py --autoprueba          # 12 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/comun.py --autoprueba                # 21 chequeos
python3 ~/.claude/skills/golden-dropkiller-productos-ganadores/scripts/brecha_mercados.py --autoprueba     # 11 chequeos
```
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. Medido el 2026-09-18 con `stat -f %Sf`: **todos los nodos llevan `uchg`**, puesto por
`~/.golden/bin/golden-blindaje` (chmod `0444`/`0555` primero, `chflags uchg` después). La nota
anterior ("chmod puro, sin chflags", del 2026-09-13) era cierta ese día y dejó de serlo cuando la
herramienta de la casa pasó a sellar con `uchg`: por eso aquí no se escribe el número de nodos.
- abrir: `golden-blindaje golden-dropkiller-productos-ganadores` (captura el md5 ANTES y quita `uchg`)
- cerrar: `golden-blindaje golden-dropkiller-productos-ganadores --cerrar` (imprime los pares que cambiaron)
- `chmod -R u+w` solo NO abre: `uchg` sigue bloqueando la escritura.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-dropkiller-productos-ganadores`

Historial completo en `references/changelog.md`.
