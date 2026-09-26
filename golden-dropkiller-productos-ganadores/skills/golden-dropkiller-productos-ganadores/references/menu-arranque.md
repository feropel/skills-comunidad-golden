# Menú de arranque: qué quieres hacer hoy

Se muestra **una sola vez al inicio** de cada invocación en la que el usuario no dijo ya qué
quiere. Una sola pregunta, con todas las opciones escritas, para que responda en una línea
(por ejemplo `1A, 2 todos, 3 CO, 4 B, 5 no sé`). **Nunca se gotean preguntas después.**

**Regla del "no sé":** cualquier filtro que el usuario deje en blanco o conteste "no sé" toma el
valor de la columna **Si no sabe**. Si contesta "no sé" a todo, la corrida es: todas las rutas,
todas las categorías, Colombia, catálogo contra entrega, 10 productos. No se vuelve a preguntar.

**Cuándo NO se muestra el menú:** si el mensaje ya trae el encargo ("valida este producto",
"dame 10 ganadores de mascotas en México", una foto de un producto) se arranca directo y se
declara en una línea qué valores se asumieron. Si la corrida es la tarea diaria programada,
tampoco: usa el preset guardado en el prompt de la tarea.

## El mensaje que se muestra (copiar tal cual, sin signos de apertura)

```
Qué quieres hacer hoy. Responde con los números y letras, o "no sé" en lo que no tengas claro.

1. OBJETIVO
   A. Encontrar productos ganadores nuevos (caza)
   B. Validar un producto que ya tengo en mente (mándame nombre, link o foto)
   C. Espiar una tienda o un competidor (mándame el dominio)
   D. Sacar creativos y ángulos de un producto que ya vendo
   E. Dejar programada la búsqueda diaria de ganadores

2. NICHO (puedes elegir varios). Filtra las categorías de DropKiller; salud y belleza
   traen más ventas pero piden etiqueta, alérgenos y cuidado con lo que se promete.
   salud y bienestar · belleza · hogar · cocina · aseo · tecnología · herramientas ·
   automotriz · mascotas · niños y bebés · deportes · moda · otros
   → no sé: todos

3. PAÍS DONDE VENDES. Cambia los proveedores que se miran, la tabla de etapas (hay tabla
   de practicante, NO medida, para CO, EC y GT; los demás usan la de CO y se avisa) y el tope de
   proveedores (también heredado, sin verificar).
   CO Colombia · MX México · EC Ecuador · PE Perú · CL Chile · GT Guatemala · PA Panamá ·
   CR Costa Rica · PY Paraguay · AR Argentina · ES España · otro
   → no sé: Colombia

4. MODELO
   A. Catálogo contra entrega (Dropi, sin marca)
   B. Marca propia con pago anticipado (aquí manda la recompra)
   → no sé: A

5. QUÉ TAN PROBADO QUIERES EL PRODUCTO (ventas totales sumando todos los proveedores)
   A. Nuevo, casi nadie lo vende (menos de 100 ventas): más riesgo, más aire. NO cumple el
      criterio 1 del método (100 ventas): sale marcado "sin validar"
   B. Validado sin escalar (100 a 3.000 en Colombia): el punto dulce del método
   C. Escalando (3.000 a 8.000): solo si vas a importar para competir por precio
   → no sé: B. Si B no alcanza, se entregan menos, no se rellena con A

6. RITMO DE VENTA EN LOS ÚLTIMOS 7 DÍAS
   A. 10 a 30 (despacio: en el backtest murió el 42% a los 60 días; bajo 10, el 92%)
   B. 31 o más (prudente: murió 1 de 15; es un indicio, no una prueba)
   C. solo más de 120 (caliente: la demanda persiste, pero hay que medir la competencia)
   → no sé: B. Lo que va FRENANDO sale con aviso (dato, no filtro: no se distinguió del nivel bajo)

7. CUÁNTO LLEVAN CORRIENDO LOS ANUNCIOS QUE LO PRUEBAN
   A. Nuevos, 7 días o menos (tendencia, más riesgo)
   B. Validados, 7 a 30 días
   C. Evergreen, más de 30 días (la señal más fuerte)
   → no sé: B y C. En el lote se aplica como "algún anuncio del producto corrió al menos N
   días" (A: 0, B y C: 7, solo C: 30); no hay techo, así que B no excluye los de más de 30.

8. COMPETENCIA QUE ACEPTAS
   Proveedores:  A. 1 a 2   B. hasta 5 (en MX 4; en GT y PE 2)   C. no importa
      (topes de practicante, SIN VERIFICAR: DropKiller no da proveedores por fecha para medirlos)
   Anunciantes en tu canal:  A. 0 a 3   B. hasta 6   C. no importa
   Contados como páginas distintas que anuncian ESE producto, no como anuncios.
   → no sé: proveedores B, anunciantes A

9. CANAL DONDE VAS A VENDER. Los anunciantes se cuentan solo en ese canal: si todos
   mandan a WhatsApp, la landing está libre, y al revés (son públicos distintos).
   A. Landing o Shopify   B. WhatsApp   C. el que esté más libre (se cuentan los dos y se
   dice cuál ganó)
   → no sé: C. Ojo con C: casi todo lo que se pauta en Meta lleva a una landing, así que
   WhatsApp sale libre muy seguido y el filtro de anunciantes se vuelve permisivo. Si vas a
   vender por landing, elige A.

10. PRECIO Y STOCK
   Costo del proveedor:  mínimo ____ · máximo ____   → no sé: sin límite
   Stock mínimo del proveedor:  → no sé: 80 unidades
   Solo proveedores verificados (Dropi los marca por cumplimiento de despacho):
   sí / no   → no sé: no, pero cada proveedor sale marcado verificado o no

11. DE DÓNDE SACO LOS CANDIDATOS
   A. Lo que ya vende sin escalar en tu país
   B. Lo recién creado que ya vende (últimos 7 a 30 días)
   C. Nuevo sin competencia (creado hace menos de 3 meses, 500 a 2.000 ventas)
   D. Lo que funciona en otro país y aquí está virgen
   E. Tiendas de otros países que están pautando fuerte
   F. TikTok Shop de Estados Unidos
   G. Un problema validado afuera que aquí esté libre (sale un problema, no un producto:
      después hay que encontrar qué producto lo resuelve y pasarlo por el embudo)
   → no sé: todas

12. CUÁNTOS PRODUCTOS. Es un tope, no una meta: si pasan menos, se entregan menos y se
   dice qué filtro cortó más.
   → no sé: 10
```

## Cómo cada respuesta se vuelve un filtro de DropKiller

| Opción | Filtro | Herramienta |
|---|---|---|
| 2 nicho | `categories` (slugs de `list_product_filters`: salud-bienestar, belleza, hogar-deco, cocina, aseo-limpieza, tecnologia, herramientas, automotriz, mascotas, ninos-bebes, deportes-outdoor, moda-ropa, otros) | search_products, find_winning_products |
| 3 país | `countryCode` + `platformType` DROPI (en PE también ALICLICK; en CR/GT/HN/SV, SOYDROP) | todas |
| 5 A / B / C | `minTotalSold` = piso de la etapa (A: sin piso). El techo NO se pide a DropKiller (`maxTotalSold` no existe y se ignora callado, trampa 9): lo aplica `consolidar_mercado.py --etapa NUEVO\|VALIDACION\|ESCALADO` (campo `etapa_es_la_pedida`) | search_products + script |
| 6 A / B / C | A: `minSold7d` 10 y `maxSold7d` 30, y `correr_lote.py --min-7d 10 --max-7d 30` · B: `minSold7d` 31 y `--min-7d 31` · C: `minSold7d` 121 y `--min-7d 121`. El script usa las ventas DEPURADAS, no las de DropKiller. Más de 120 sale con aviso CALIENTE | search_products + correr_lote |
| 7 A / B / C | Al buscar: `broadcastDuration` new / validated / evergreen. En el lote: `correr_lote.py --antiguedad-min 0` (A) · `7` (B, por defecto) · `30` (C): un producto sin NINGÚN anuncio que haya corrido esos días va a CASI | semantic_search_ads + correr_lote |
| 8 proveedores | `correr_lote.py --max-proveedores 2` (A) · sin la bandera usa el tope del país (B) · `--max-proveedores 999` (C). Topes heredados, sin verificar | correr_lote |
| 8 anunciantes | `correr_lote.py --max-anunciantes 3` (A, por defecto) · `6` (B) · `999` (C); cuenta los ACTIVOS de `competencia.py canal` (imagen + descripción). Confirmar por nombre de página en la Ad Library | semantic_search_ads + correr_lote |
| 9 canal | `correr_lote.py --canal landing` (A) · `--canal whatsapp` (B) · sin la bandera (C): cuenta los dos y la tarjeta dice cuántos van a cada uno | correr_lote |
| 10 | Al buscar: `minPrice`/`maxPrice`, `minStock`, `verifiedProvider`. En el lote: `--costo-min`, `--costo-max`, `--min-stock 80` (por defecto; mira el stock de la última lectura del historial) y `--solo-verificados` (necesita `"verificado": true` en `ficha.json`) | search_products + correr_lote |
| 11 A…G | las 7 rutas R1…R7 de `dropkiller-caza.md` §5 | varias · R7 usa `ads_library_search` + `brecha_mercados.py` |

**Opción 4 B (marca propia):** la rúbrica cambia de columna (la RECOMPRA pesa 20) y la ruta F
(TikTok Shop) y E (tiendas de marca: 1 a 40 productos, 100 o más anuncios) suben de prioridad,
porque lo que no está en Dropi es candidato a MAQUILA, no descarte.

## Lo que la corrida le debe al menú

Cada respuesta es un **filtro que se aplica**, no una preferencia. En la lista de caza:
- Un producto que rompe un filtro elegido (o su valor por defecto) **no entra a la lista**: va a
  la sección "Casi" de la lista con el filtro que rompió y por cuánto.
- Un filtro que no se pudo aplicar (una ruta sin correr, un canal sin medir) **se declara en la
  cabecera**. Decir "todos no sé" y correr la mitad de las rutas es cobertura falsa (medido en la
  primera corrida real, 2026-09-18: se corrieron R1-R3 de R1-R6 y no se dijo).
