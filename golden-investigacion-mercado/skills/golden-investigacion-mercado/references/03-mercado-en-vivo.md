# Fase 3 — El mercado EN VIVO: países, oferta, página y creativos

Las Fases 0 y 1 dicen qué ES el producto y qué SIENTE el cliente. Esta dice **cómo se está vendiendo
ahora mismo, con qué oferta, en qué países y con qué piezas** — y, sobre todo, **qué NO está haciendo
nadie**, que es donde vive el dinero.

Cuatro bloques. Ninguno es opcional; el que no se pueda hacer se declara con su motivo, nunca se omite
en silencio (REGLA 5). **Todo dato de aquí lleva FECHA DE MEDICIÓN**: precios, ofertas y saturación se
mueven en semanas, y un dato sin fecha envejece sin que nadie lo note.

## 3.1 · MAPA DE MERCADOS — el producto no vive en un país, vive en varios

El error que esta fase corrige: investigar solo el país destino y creer que se vio el mercado. El mismo
producto lleva años vendiéndose en otros lados con ángulos, precios y ofertas ya probados por otros.

**Cómo se arma la lista de países** (no se barre el planeta a ciegas):
1. **Origen** — dónde se fabrica y dónde se vende masivo (suele ser China, y ahí están las reseñas
   con foto real y el precio de origen).
2. **Mercado maduro** — Estados Unidos y España casi siempre: llevan más tiempo, así que sus ángulos
   ya pasaron por selección natural y su oferta ya se optimizó.
3. **Vecinos COD** — los países de operación de la casa: es donde el hallazgo se puede copiar mañana.
4. **El destino** — donde se va a lanzar.

**Qué se mide en CADA país** (una fila por país, y la tabla es el entregable):

| País | Quién lo vende | Precio (moneda local + USD) | Oferta y combos | Modelo de pago | Anuncios activos | Desde cuándo | Fuente y fecha |

(la columna **Anuncios activos** se escribe `N` si el conteo cerró, o `N+` si quedó abierto — y una
columna con `N+` **no se ordena de mayor a menor**: los abiertos no son comparables entre sí)
|---|---|---|---|---|---|---|---|

**Cómo se levanta cada columna:**
- **Anuncios activos y desde cuándo** → las tres bibliotecas (`scraping-firecrawl.md` §Bibliotecas).
  Meta por MCP; **Google con `scripts/google_ads_transparency.py --paises CO,MX,CL --contar`**, que
  además trae **cuántos días lleva corriendo cada anuncio**; TikTok solo Europa, para LatAm el
  Creative Center con sesión.
- **Precio** → la página del vendedor, no el marketplace ajeno. Se anota en moneda local **y** en USD
  al cambio del día, o dos países no se pueden comparar.
- **Quién lo vende** → dominios propios, marketplaces y redes. Un producto que solo aparece en
  marketplace y en ninguna tienda propia es una señal: nadie ha construido marca encima todavía.

**Lo que la tabla tiene que dejar decidido:**
- **Dónde está saturado y dónde no.** Diez anunciantes con seis meses de antigüedad en un país y cero
  en el vecino no es "no hay demanda" en el vecino: suele ser que nadie ha llegado.
- **El delta de precio entre países**, que es lo que dice si el precio objetivo local es caro o barato
  contra el mundo, no contra la intuición del dueño.
- **Qué ángulo viaja y cuál no.** Un ángulo que funciona en tres países distintos es estructura;
  uno que solo aparece en uno puede ser cultural.

> 🚨 **Trampa medida (2026-09-08):** un conteo de anuncios que llega redondo y repetido —cinco países,
> cinco veces 40— **es el límite de la herramienta, no un dato**. Cualquier conteo entra a la tabla
> **cerrado** (la última página vino incompleta) o marcado `N+ (abierto)`. Un número sin esa marca no
> se escribe, porque de él sale la lectura de saturación y con ella la decisión de lanzar o matar.
>
> 🚨🚨 **Y AHORA LA TRAMPA GEMELA, que nace de la cura anterior: DOS `N+` NO SE COMPARAN ENTRE SÍ.**
> Dos competidores marcados `100+` pueden ser **101 y 4.000**. Leerlos como parejos es exactamente el
> error de los cinco cuarentas **un piso más arriba**, y con la misma consecuencia: de ahí sale la
> saturación del nicho. Un conteo abierto solo autoriza a decir **"al menos N"**. **NUNCA ordena, nunca
> rankea, nunca mide saturación, nunca entra en un "X pauta más que Y".**
> **Si una decisión de lanzar o matar necesita comparar dos competidores: se cierran los dos conteos,
> o no se comparan.** Un `N+` que se compara vale menos que no tener el dato, porque parece que lo hay.

## 3.2 · MATRIZ DE OFERTA Y COMBOS — casi nadie compite en producto, todos compiten en OFERTA

Dos tiendas con el mismo producto y el mismo precio unitario venden distinto por cómo arman la escalera.
Esto se levanta **competidor por competidor**, con captura o cita de la página.

| Competidor | 1 unidad | 2 unidades | 3 o más | Regalo | Envío | Garantía | Ancla o tachado | Urgencia | Pago |
|---|---|---|---|---|---|---|---|---|---|

De cada fila se extrae, y esto es lo que se usa después:
- **Precio por unidad en cada escalón** — el descuento real por volumen, no el que anuncian.
- **Dónde ponen el ancla** (el precio tachado) y **cuánto descuento declaran**.
- **Qué regalan** y si el regalo es del producto o accesorio.
- **Quién paga el envío** y desde qué monto.
- **Qué garantía dan** y en cuántos días.
- **Modelo de pago**: contra entrega, anticipado o los dos.

**La salida es una oferta propia, no una descripción.** Con la matriz delante:
1. **El escalón que todos ignoran** (casi siempre el de 3, o el de 2 con regalo).
2. **El punto de precio vacío** — si todos están en 89.900 y 149.900, el hueco está en medio o arriba.
3. **La garantía que nadie da**, que es la forma más barata de romper la objeción de riesgo.
4. **El ancla honesta**: precio de referencia real, jamás inventado (los precios del estudio son
   REFERENCIA; el precio lo decide solo el dueño — REGLA 11).

## 3.3 · AUTOPSIA DE PÁGINA — cómo está construida la página del que ya vende

No basta el precio del competidor: hay que ver **cómo lo presenta**. Se hace sobre las 2 o 3 páginas
de los competidores que más llevan anunciando (los que no se apagan, convierten).

**Se recorre de arriba abajo y se anota el ORDEN**, porque el orden es la estrategia:
1. **Primera pantalla**: titular, subtítulo, imagen o video, precio visible sí o no, CTA.
2. **Secuencia de secciones**: dolor, mecanismo, prueba, comparativa, oferta, garantía, FAQ, cierre.
3. **Prueba social**: cuántas reseñas, con foto o sin foto, dónde aparecen, si hay video.
4. **La oferta**: dónde entra el combo y si repite abajo.
5. **El formulario**: cuántos campos, si pide ciudad, si es contra entrega, si hay upsell antes o
   después de enviar.
6. **Lo técnico**, por `rawHtml` y `grep`: plataforma, tema, apps de upsell, temporizadores, píxeles.
   Es la vía más honesta que hay, porque no pasa por ningún extractor que pueda inventar.

**Lo que se extrae:** qué secciones tienen TODOS (son el estándar de la categoría, hay que tenerlas),
qué tiene solo el que más lleva corriendo (probablemente su ventaja), y **qué no tiene ninguno**.

## 3.4 · INVENTARIO DE CREATIVOS — las piezas, no solo el texto

La skill ya capturaba el copy del anuncio. Faltaban **las imágenes y los videos**, que es lo que
realmente para el dedo.

Para cada competidor con anuncios activos, una fila por pieza:

| Pieza | Formato | Días activo | Gancho de los 3 primeros segundos | Qué muestra | Quién aparece | Texto en pantalla | Cierre |
|---|---|---|---|---|---|---|---|

- **Días activo** sale directo de las bibliotecas (Google lo trae en cada creativo; Meta, por su fecha
  de inicio). **Ordena el inventario por ese número**: la pieza más vieja que sigue viva es la que
  paga, y es la que hay que estudiar primero.
- **El video se descarga y se desarma** con `golden-video-teardown`; no se resume de memoria ni se
  deduce del título.
- **La imagen se mira**, y se anota qué hay: producto solo, producto en uso, antes y después, texto
  grande, cara, mano, comparativa.

**Lo que se extrae:** los 3 o 4 **formatos dominantes** de la categoría, el **gancho repetido** (si
todos abren igual, el mercado ya enseñó qué funciona), y **el formato ausente**.

## 3.5 · LA SALIDA DE ESTA FASE: LOS HUECOS

Los cuatro bloques anteriores son para llegar aquí. **"Todo" incluye lo que nadie está sembrando**, y
eso solo se ve después de mirar a todos:

1. **Dolores que nadie nombra** — están en los comentarios (Fase 1.6) y en ningún anuncio.
2. **Públicos sin atacar** — la capa 30 del dossier lista todos los que se benefician; cruzarla con a
   quién le hablan los anuncios reales.
3. **Ángulos ausentes** — de los 5 a 8 del mapa, cuáles no usa ni un competidor.
4. **Escalones de oferta vacíos** y **puntos de precio libres** (3.2).
5. **Secciones de página que nadie tiene** (3.3) y **formatos de creativo que nadie usa** (3.4).
6. **Países con demanda y sin oferta** (3.1).
7. **Objeciones sin responder** — las preguntas repetidas que ninguna página contesta.
8. **Momentos y usos secundarios** — el regalo, la temporada, el caso de uso que el dueño no había
   pensado y que el cliente ya menciona solo.

Cada hueco se escribe con **la evidencia de que está vacío** (qué se revisó y dónde) y con **por qué
podría estar vacío**: a veces nadie lo hace porque no funciona, y decirlo es tan valioso como el hueco.
Un hueco sin esa segunda línea es una corazonada, no un hallazgo.

> **PUERTA de la fase:** no se cierra sin la tabla de países, la matriz de ofertas, la autopsia de al
> menos 2 páginas, el inventario de creativos ordenado por días activo, y la lista de huecos con su
> evidencia. Lo que no se pudo levantar va como `[PENDIENTE]` con el motivo y la vía que se intentó.

## 3.6 · LOS ÁNGULOS — cómo se construyen y cómo se entregan (FER, 22-sep-2026)

Los HUECOS de §3.5 dicen qué está vacío. Esta sección convierte eso —y lo que YA funciona en otros
países— en el entregable que consumen las imágenes, los copys y el prompt del bot.

### Cuántos: de 3 a 10, con 2 creativos cada uno

Un ángulo solo no prueba nada: si vende, no se sabe si fue el ángulo o la suerte; si no vende, no se
sabe si fue el ángulo o la pieza. Por eso el mínimo es **3 ángulos** y cada uno lleva **2 conceptos
de imagen distintos**. El máximo (10) lo fija la evidencia disponible, no el cansancio.

### De dónde salen — las dos vetas, siempre las dos

1. **REPLICAR lo que ya paga en cualquier país.** El barrido es global: México, Guatemala, Perú,
   Argentina, Estados Unidos, España, y el que aparezca. La señal dura es la pieza con más **días
   activo** (§3.4): nadie paga meses por un anuncio que no vende. Si un ángulo lleva 90 días vivo en
   México y aquí nadie lo usa, ese ángulo se copia y se adapta al habla local.
2. **TOMAR el hueco.** El dolor que la gente nombra en comentarios y que ningún anuncio recoge.
   Más riesgo, más ventaja, y hay que escribir **por qué podría estar vacío** (a veces nadie lo hace
   porque no funciona, o porque no se puede decir por compliance).

### El filtro que separa el dato del ruido: LIKES

Un comentario sin likes es una opinión. Un comentario con cien likes es un dolor que cien personas
reconocieron como propio antes que tú. **El like es la validación social que convierte una frase en
evidencia de mercado.** Operativamente: `yt-dlp` ya trae `like_count`; los comentarios se **ordenan
por likes**, no por fecha, y el ángulo cita el número junto a la frase. Un ángulo sostenido solo en
comentarios de cero likes se entrega marcado `(señal débil)`.

### Las fuentes, todas

Facebook · Instagram · YouTube (video y **comentarios**) · TikTok y TikTok Ads (ojo: su Ad Library
**solo cubre Europa**) · MercadoLibre · Amazon · **Alibaba** · **Temu** · AliExpress · Meta Ad
Library · Google Centro de Transparencia. Las reseñas de marketplace sirven doble: dolor y objeción.

### Ficha de cada ángulo (esto es lo que se entrega)

| campo | qué lleva |
|---|---|
| Nombre | corto, memorable, en lenguaje de cliente |
| Dolor | **cita textual** + fuente + likes |
| Quién | a quién le duele (no "todos") |
| Promesa | qué cambia en su vida, sin claim prohibido |
| Origen | país · pieza · días activo (replicado) **o** hueco + por qué estaría vacío |
| Evidencia | URLs, fecha de medición |
| 2 imágenes | concepto A y concepto B, distintos de verdad |
| Bot | qué dolor debe recoger el prompt para que el chat no contradiga al anuncio |

### Recursos y motores

No hay límite de crédito (palabras de FER: *"tenemos el plan más grande, no te limites"*). Para el
MISMO ángulo se genera en **Ecom Magic, Higgsfield y los motores gratuitos**, se comparan y se
entrega el que gana. Se reporta con qué motor salió cada pieza.

**Candado de la sección:** menos de 3 ángulos con fuente = no cierra. Cada ángulo, su evidencia y su
fecha de medición.
