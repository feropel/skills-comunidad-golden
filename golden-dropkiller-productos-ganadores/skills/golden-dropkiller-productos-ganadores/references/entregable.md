# El entregable — ficha, ángulos, precios, índice, modo lote y lista de caza

La validación no termina en un score: termina en algo que se pueda **usar mañana**. Este archivo
define qué se entrega y en qué orden.

## 1 · Ficha de Producto Ganador

```
🏆 PRODUCTO: <nombre>
🏷️ Modelo evaluado: <catálogo COD | marca propia anticipado>   ← define la columna de la rúbrica
📊 Score Ganador: <0-100>   ·   Confianza: <Alta | Media | Baja>
🌎 País objetivo: <país>
💰 Costo del proveedor: <$>  ·  PVP mínimo (viabilidad_cod.py): <$>  ·  Precio de la competencia visible: <$ o "no visto">
   Utilidad por pedido GENERADO al PVP propuesto: <$> (CPA <medido/supuesto>)   ← en pesos, nunca un multiplicador

📦 Ventas reales (DropKiller depurado): <N depuradas de M reportadas · veredicto REAL/DUDOSO> · ritmo <X/día> · reabastecimientos <n>
🏭 Mercado consolidado: <ventas totales sumadas · etapa NUEVO/VALIDACIÓN/…> · <P> proveedores activos (<espejos descartados>)
📣 Canal más libre: <landing | WhatsApp> · anunciantes por canal: landing <a> · WhatsApp <w>
🧪 Ficha técnica: <"tomada de la ETIQUETA del producto que se despacha" | "PENDIENTE: pedir foto de etiqueta al proveedor">
⚠️ Alérgenos del envase: <lista | "ninguno declarado en la etiqueta" | "PENDIENTE: sin etiqueta no se publica">

🔥 Competencia: <N tiendas CONFIRMADAS + ~M posibles sin validar>
🪦 Cementerio: <A activos / T históricos = S% supervivencia>  ← ver ad-library-metodo §2
📈 Cobertura: <X revisados de ~Y que reporta Meta = Z%>
🔑 Keywords buscadas: <lista completa; marcar las NO buscadas>

🎯 Ángulo dominante del mercado: <...>
🕳️ HUECOS de ángulo: <2-4 que el producto sostiene y NADIE usa en ese país>
👤 Avatar rápido: <quién compra>
📹 Hook sugerido: <gancho para el hueco #1>
⚠️ Riesgos: <saturación / cementerio / logística / compliance>
➡️ Siguiente paso: <investigación de mercado + página según el modelo>
💼 Afiliación: <si la ficha usa cifras de DropKiller o lo recomienda: "FER tiene enlace de afiliado de DropKiller (15%)"; si no, se omite>
```

## 2 · Mapa de ángulos (lo que casi nadie hace, y es donde está el dinero)

De los copies y creativos observados, tres listas:

**Ángulos EN USO** — cada uno con: nombre, qué tienda lo usa, **cita corta real** del anuncio y el
marco aparente (dolor/agitación vs aspiración). La cita textual es obligatoria: sin ella es opinión.

**Ángulos SATURADOS** — los que usan 3+ tiendas. Entrar ahí exige un creativo claramente superior,
no solo "uno más".

**HUECOS** 🕳️ — ángulos que el producto **puede sostener con verdad** y que **nadie** está usando en
ese país. Esto es el oro del informe: 2-4 huecos concretos, cada uno con un hook sugerido.

> **Un hueco no es "nadie lo dice".** Es "nadie lo dice **y el producto lo cumple**". Un ángulo que
> el producto no puede respaldar no es un hueco, es un claim falso esperando a que Meta lo tumbe.

Los hooks sugeridos salen con las reglas de la casa: segunda persona, dolor cotidiano, máximo ~15
palabras, y **verbos de compliance** — "ayuda a", "favorece", nunca "cura", "elimina" ni "garantiza".
Para desarrollarlos: `golden-copywriting`.

## 3 · Lectura de precios

Tabla con los precios visibles en los anuncios de la competencia contra el precio previsto.
Sirve para dos decisiones concretas:

- **Techo**: lo que cobran las cadenas grandes marca el máximo creíble aunque no compitan en COD.
- **Piso**: si el más barato del mercado está por debajo del **PVP mínimo que calcula
  `scripts/viabilidad_cod.py`**, el margen no da y el producto muere en la compuerta aunque la
  demanda sea buena. (Antes decía "costo × 3": esa regla de pulgar solo es cierta cerca de un
  costo de $30.000; un producto de $10.000 necesita 7,02×. Ver `references/economia-cod.md`.)

Si el usuario no dio precio previsto, se entrega igual el rango observado y se le pide.

## 4 · Índice de anuncios de la competencia

Cada anuncio observado como **link abierto**, para ver el creativo y el copy sin volver a buscar.
El formato sale del `id` que devuelve el MCP (o del campo `ad_snapshot_url`, que ya viene armado):

```
https://www.facebook.com/ads/library/?id=<ID_DEL_ANUNCIO>
```

| Tienda | Tipo | Ángulo | Empezó | Antigüedad | Ver anuncio |
|---|---|---|---|---|---|
| <página> | exacto / similar / cadena | <ángulo corto> | dd-mmm | X días | <link> |

**Reglas:** dedup por ID (un anuncio sale una vez aunque aparezca en varias keywords) · orden por
relevancia competitiva, los directos primero · si una tienda corre 20 versiones casi iguales, lista
las representativas — **siempre la más antigua** y una por ángulo — y anota "corre N+ versiones" ·
**nunca inventes un ID**: solo se linkea lo que se vio. El link es público, no pide sesión.

Cerrar con el total: "N anuncios indexados".

## 5 · MODO LOTE (varios productos de una)

Se activa cuando el usuario manda 2+ productos. **No es una versión ligera**: cada producto recibe
la validación completa —las 8 keywords, su registro de cobertura, su cementerio y su score—. Lo que
agrega el lote es el **ranking**.

**Flujo:**
1. **Una sola confirmación al inicio.** Identifica todos los productos, muestra la lista numerada y
   el país, y deja que el usuario corrija o descarte ANTES de empezar. No interrumpas producto por
   producto después.
2. **Uno a la vez** y **entrega cada ficha apenas esté lista**, con una línea de veredicto. Así el
   usuario ve avance real aunque vuelva a mitad del lote. No acumules todo para el final.
3. **Si uno falla** (bloqueo, keywords sin resolver), no se cae el lote: se marca
   "⚠️ no validado — motivo", sigue el siguiente y se reintenta una vez al final.
4. Al cerrar, el **ranking comparativo**.

**Ranking comparativo:**

| # | Producto | Score | Tiendas (conf + ~sin validar) | Supervivencia | Señal | Hueco #1 | Confianza |
|---|---|---|---|---|---|---|---|

Y debajo, lo que **solo se ve con el lote completo** y justifica el modo:

- **Tiendas que se repiten entre productos.** Una tienda que vende 3 de tus 5 candidatos no es
  casualidad: es un **competidor de catálogo directo**, y eso cambia la estrategia de los cinco.
- **Nichos ya calientes** en ese país.
- **Ángulos que funcionan en toda la categoría**, no solo en un producto.

Cierra con el orden de lanzamiento sugerido y su porqué — score, hueco y presión competitiva, no
solo el número.

## 6 · Regla de entrega

**El informe se entrega SIEMPRE, aunque el veredicto sea descartar.** Un "no" documentado con sus
números ahorra plata y evita volver a evaluar el mismo producto dentro de tres meses. Guardar en
`PROYECTOS/<PRODUCTO>/` como manda el estándar de la casa.

## 7 · LISTA DE CAZA (modo caza y tarea diaria)

La caza no entrega fichas completas: entrega una **lista corta y verificada** para decidir qué
se investiga a fondo. La ficha completa (sección 1) se hace después, solo del que se elige.

**Cabecera obligatoria** (sin ella la lista no se entrega):

```
🎯 CAZA <fecha> · <país> · <plataforma> · modelo <COD | marca propia>
Filtros: <los del menú, en una línea, marcando cuáles fueron "no sé">
No aplicado: <rutas no corridas (p. ej. R4-R6), canal sin medir, candidatos sin pasar por el embudo; "nada" solo si es cierto>
Embudo: <C> candidatos → <F> fantasma fuera → <S> saturados o con muchos proveedores fuera →
        <R> descartados por riesgo → <N> en la lista
Fuente: DropKiller (MCP beta) + Ad Library de Meta. Ventas DEPURADAS, no las reportadas.
Afiliación: FER tiene enlace de afiliado de DropKiller (15%).
```

**Una tarjeta por producto, en orden de ranking:**

```
#<n> <PRODUCTO> · <proveedor> <✔ verificado>
   Ventas reales: <depuradas> (<reportadas> reportadas) · 7 días <n> · <X>/día · tendencia <acelerando | estable | frenando> (<aceleración>) · etapa <…> · <P> proveedores · <n> reabastecimientos
   Mercado consolidado: <total> · avisos del script: <espejos que no cuadran, datos que faltaron | ninguno>
   Plata: costo <$> → PVP mínimo <$> (en pesos, nunca un multiplicador) · competencia vende a <mín a máx, N landings leídas | no visto> → <CIERRA | JUSTA | NO CIERRA>
   Canal: <a> anunciantes activos hoy · <c> en el cementerio (lo soltaron) · <landing | WhatsApp> · medido por imagen + descripción
   Afuera: <país> corre <N> anuncios, el más viejo <D> días · ángulo: "<cita corta del anuncio>"
   Ruta: <R1…R6>  ·  Riesgo: <ninguno | salud: pedir etiqueta y alérgenos | …>
   Ver: <link del producto en DropKiller o id de Dropi, nunca una ruta de archivo temporal> · <link del anuncio más fuerte>
```

**Debajo de la lista, la sección CASI:** productos que pasan los criterios 1 y 2 pero rompen un
filtro del menú (ritmo de 7 días, tope de anunciantes, precio o stock), con el filtro y por cuánto
("7 días: 19, piso 31" o "anunciantes activos: 5, tope 3"). No son ganadores del día: son los que alguien mira si cambia el filtro.

**Debajo, siempre, la lista de DESCARTADOS con su motivo en una línea** (el producto fantasma
del día, el quemado que parecía nuevo, la marca ajena). Es lo que evita que mañana alguien
lo encuentre en el top de DropKiller y lo testee.

**Reglas de la lista:**
- Nunca se rellena para llegar al número pedido. Si solo 6 pasan, se entregan 6 y se dice
  por qué no hubo 10 (qué ruta se agotó, qué filtro cortó más).
- Lo DUDOSO solo entra al final y marcado, si no alcanzan los REAL.
- Ninguna cifra sin fuente: "la categoría se vende por debajo" sin una landing vista es opinión y no
  se escribe. "0 anunciantes vistos" con 2 o 3 keywords por título es "no medido", no "libre".
- Guardar en `PROYECTOS/CAZA-DIARIA-GANADORES/<AAAA-MM-DD>-<país>.md` y decir en el chat
  los 3 primeros con una línea cada uno. El archivo es respaldo; lo importante se dice en el chat.
- Si un producto de la lista ya salió en una caza anterior, se marca "repetido desde <fecha>"
  con el cambio de sus ventas: un producto que repite y crece es la mejor señal de la semana.
