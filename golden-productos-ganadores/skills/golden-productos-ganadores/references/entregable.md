# El entregable — ficha, ángulos, precios, índice y modo lote

La validación no termina en un score: termina en algo que se pueda **usar mañana**. Este archivo
define qué se entrega y en qué orden.

## 1 · Ficha de Producto Ganador

```
🏆 PRODUCTO: <nombre>
🏷️ Modelo evaluado: <catálogo COD | marca propia anticipado>   ← define la columna de la rúbrica
📊 Score Ganador: <0-100>   ·   Confianza: <Alta | Media | Baja>
🌎 País objetivo: <país>
💰 Costo aprox: <$>  ·  Precio venta sugerido: <$>  ·  Margen: <x>

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
- **Piso**: si el más barato del mercado está por debajo de tu costo × 3, el margen no da y el
  producto muere en la rúbrica aunque la demanda sea buena.

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
