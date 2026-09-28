# Historial de golden-dropkiller-productos-ganadores

> Se llamó `golden-productos-ganadores` hasta el 2026-09-22 (GPG1.24). Las actas de abajo
> conservan el nombre que la skill tenía cuando se escribieron.

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.

## GPG1.25.1 · 2026-09-27 · P59 · entrega_golden cuenta lo que descarta

Aplicado por el chat 🧰 ARSENAL Y SKILLS (bloque 3 del Centro de Mando, orden de FER), con la fila enviada a esta fábrica.

- **El fallo (`scripts/entrega_golden.py:96`):** los pedidos sin ID o sin PRODUCTO ID se tiraban sin contarse, y un pedido REPETIDO en dos informes con OTRO estatus se quedaba con el primero que aparecía. El verificador midió con 5 filas: tasa de **100%** donde la real era **40%**. Esa tasa entra al PVP mínimo.
- **El arreglo:**
  - Los sin-ID y los repetidos se cuentan (`descartados` en el JSON y una línea DESCARTADOS en `construir`).
  - Un estatus terminal (ENTREGADO o DEVOLUCIÓN) le gana a «otros».
  - Dos terminales distintos NO se adivinan: se declaran en `conflicto_terminal`.
  - Los `.xlsx` de la carpeta sin «por producto» en el nombre se NOMBRAN. La selección no cambia.
- **CIFRA REAL, antes → después**, con los informes de Golden (`⭐️ GOLDEN/COLOMBIA/🟠 INFORMES DROPI`):
  - Tasa general **72,7% → 72,7%**, y **0 de 103 productos** cambian su tasa.
  - Ahora se ven 1.396 filas repetidas, ninguna con otro estatus, y 33 `.xlsx` que no se leen (comisiones, cartera…).
  - El caso del verificador pasa de 100% a 40%.
- **Autoprueba:** 17 → **21 de 21**. La línea del SKILL.md pasa a «21 chequeos».

## GPG1.25.1 · 2026-09-27 · Limpieza de datos internos para el repo público (aplicó el CENTRO DE MANDO)

La compuerta de publicación bloqueaba la skill por nombres internos: el nombre del chat y de la empresa de un espacio ajeno, y el código de un espacio real. Se cambiaron por formulaciones genéricas con el mismo sentido; la excepción operativa que nombraba espacios concretos vive ahora en la memoria del proyecto. Solo prosa y comentarios; ninguna regla cambió.

## GPG1.25.1 · 2026-09-27 · Ley de los requisitos del usuario (aplicó el CENTRO DE MANDO)

Se añadió el bloque de requisitos del SKILL.md: qué tiene que tener el usuario antes de arrancar, cada requisito marcado BLOQUEANTE o DEGRADABLE y qué pasa si falta (doctrina del CdM del 27-sep). Lo redactó el chat 🧰 ARSENAL Y SKILLS (fila P49, 4 pasadas del golden-verificador adversarial; en la última, ninguna falla nueva grave) y lo aplicó el CdM sin numerar: el número lo pone la fábrica al ratificar. Solo inserción: 0 líneas quitadas.

## GPG1.25 — 2026-09-23 · LA COMISIÓN DE RECAUDO ERA UN COBRO DUPLICADO: pasa a 0 y MEDIDA

**De dónde viene.** Fila del Centro de Mando con una frase de FER del 23-sep: *"Dropi no cobra
nada. Las transportadoras cobran un 5% del flete de base, pero eso ya está incluido cuando
hacemos la orden en Dropi, ya lo cobran ahí."* La skill restaba, además, un 4% del PVP.

**El error, nombrado:** no era un supuesto flojo, era un **cobro contado dos veces**, y la segunda
vez sobre la base equivocada — un porcentaje del **precio de venta** en lugar del **flete**. Por eso
el error crecía con el precio: $2.926 de PVP mínimo de más en un producto de $10.000 y $4.593 en
uno de $50.000.

**Lo que se comprobó antes de escribirlo** (no se tomó la fila por buena): se contó la columna
COMISION en los **17 informes "por pedido" de Golden Colombia, 18.792 filas**. Resultado: **1 pedido
entregado de 11.669 (0,0086%)** trae comisión > 0, y los valores distintos de cero que existen en
esa columna están en pedidos **CANCELADOS** de un solo informe de 2024. La lectura vieja decía
"la columna viene vacía, de aquí no sale": **la columna no estaba vacía por falta de dato, estaba
vacía porque no se cobra aparte.** Caveat declarado: dos de los 17 informes cubren Mar-Abr 2026
desde las dos cuentas (Gmail y Hotmail), así que ese bimestre puede ir repetido en los 11.669; el
resultado es 0 en los dos.

**Qué cambió.** `comision_recaudo` sale de `supuestos_no_medidos` y entra en `medidos` con valor
**0**, su fuente (la cita de FER con fecha) y la comprobación. `supuestos_no_medidos` queda vacío:
**ya no hay ningún número sin medir**; lo que se sigue declarando en cada veredicto es que el CPA
es un PISO. La tabla de multiplicadores se recalculó con la fórmula, no a mano:

| Costo | Antes (con 4%) | Ahora | PVP mínimo |
|---|---|---|---|
| $10.000 | 7,31× | **7,02×** | $73.141 → $70.215 |
| $20.000 | 4,18× | **4,01×** | $83.558 → $80.215 |
| $30.000 | 3,13× | **3,01×** | $93.974 → $90.215 |
| $50.000 | 2,30× | **2,20×** | $114.808 → $110.215 |

**El término NO se borró de la fórmula.** Si algún día una transportadora cobra el recaudo por
fuera del flete, `--comision` lo revive, y la señal para enterarse es esa misma columna del informe.

**Lo que aprendió el banco de pruebas.** El caso "usa la COMISIÓN (cambiarla mueve el resultado)"
se habría vuelto un **verde barato**: con la comisión en 0, sabotearla a 0 no prueba nada y el caso
pasaba solo. Se invirtió — ahora se le pone el 4% y se exige que mueva — y se añadieron dos casos:
que la comisión vigente sea 0 y venga de `medidos`, y que quitarla **no** vuelva viable un producto
que antes no lo era ($80.000 sobre costo $30.000 pasa de −$1.860 a $492, y el piso son $8.000).
El banco pasó de 19 a **21 casos**. La sección ROBUSTEZ del informe comparaba "con comisión" contra
"sin comisión": habría impreso **dos líneas idénticas** y un aviso falso, así que ahora mueve lo que
sí puede moverse (CPA +20% y +50%, entrega 76,5%).

**Verificación de que el banco sirve** (regla de la casa: si da verde a la primera, sospecha del
script): se sembró el caso malo en una copia —devolver la comisión al 4%— y el banco marcó **8 de
21 en rojo con salida 1**. Los casos históricos (los dos errores que se compensaban, 2,99× contra
3,13×) se fijaron a la comisión **de aquel día**: calcularlos con la de hoy habría borrado la
lección sin que nadie se enterara.

**Lo que este cambio NO resuelve:** el 5% del flete base no se puede aislar dentro del flete medido
($15.664) con los informes que hay; se sabe que está adentro porque el flete es lo que Dropi cobró,
no una estimación.

## GPG1.24 — 2026-09-22 · LA SKILL SE LLAMA AHORA golden-dropkiller-productos-ganadores

**Orden directa de FER:** "RE NOMBRA LA SKILL QUE CONTENGA DROPKILLER E INFORMA A TODO EL
ECOSISTEMA". El nombre pasa de `golden-productos-ganadores` a
`golden-dropkiller-productos-ganadores`, que es como FER la busca desde que el conector entró.

**Qué se movió:** la carpeta instalada, el `name` del frontmatter, las 29 menciones internas del
nombre (rutas de scripts, comandos de blindaje, preset de la rutina diaria) y el título de la
sesión-fábrica. **Las actas anteriores de este changelog conservan el nombre viejo a propósito:**
era el nombre real cuando se escribieron, y reescribirlas sería falsear la historia.

**Lo que NO se tocó, y va como fila al Centro de Mando** (territorio de otras fábricas): 5 skills
hermanas nombran la skill vieja y sus dueños deben actualizarla — `golden360` (SKILL.md y
`scripts/candado.py`, que mapea el nombre), `golden-investigacion-mercado` (SKILL.md y 4
references), `golden-finanzas` (la frontera, dentro de su description), `golden-chatea-pro-config-carritos`
(ruta a `viabilidad_cod.py`) y `golden-ugc-avatar`. También quedan sin tocar los documentos
históricos del stack (censos, vigilancia, revisiones fechadas): son fotos de su día.

**Marketplace:** `MARKETPLACE-GOLDEN/golden-sync.sh` lleva el nombre en su lista; se actualizó.
El repositorio `skill-golden-productos-ganadores` no existe en disco, así que el sincronizador
saltaba esta skill y el rename no rompe nada publicado.

## GPG1.23 — 2026-09-20 · RUTA R7: el problema validado afuera

FER mandó la transcripción de un video que vende un bot con esta tesis: "las apps te muestran lo
que ya está saturado; busca problemáticas validadas que casi nadie ataca", y como regla, contar
anuncios activos afuera contra los de tu país (su ejemplo: 14.000 contra 8). La idea de partir
del PROBLEMA es buena y la skill no la tenía. La regla, medida el 2026-09-19 con la Ad Library,
no se sostiene tal cual, y así queda en `scripts/brecha_mercados.py` (11 chequeos, 2 sabotajes):
1. **Se corrige por tamaño de mercado.** US+CA+GB ~9× la población de Colombia. Corrector de
   postura 2.637 contra 337 = 7,8×, por debajo de lo normal → SIN BRECHA (con la regla del video
   habría sido "oportunidad"). Fascitis plantar 25× y ronquidos 26× → BRECHA.
2. **El conteo local se depura por moneda.** De 50 anuncios de "ronquidos" en Colombia, 25 cobran
   en pesos; 15 en dong, 9 en dólares, 1 en reales. La mitad del número es de otro país (trampa 6).
3. **La salida nunca dice "oportunidad" y ya.** Dice qué falta: encontrar el producto que
   resuelve el problema, medir en DropKiller si aquí alguien lo compra (el backtest v2 midió que
   lo que casi no se mueve muere el 92%), correr la plata y pasar las compuertas de salud.
Menú: opción 11G. Guía: `dropkiller-caza.md` §5 pasa a 7 rutas.

## GPG1.22 — 2026-09-20 · openpyxl NO está solo en /usr/bin/python3

`entrega_golden.py` y el SKILL.md repetían la trampa del CLAUDE.md raíz ("openpyxl solo existe en
/usr/bin/python3"). Medido el 2026-09-20 en los tres intérpretes del Mac: **openpyxl 3.1.5
responde en `python3` (3.14.7), `/opt/homebrew/bin/python3` (3.14.7) y `/usr/bin/python3`
(3.9.6)**. Corregido el uso a `python3` y añadida la instrucción de comprobarlo con
`python3 -c "import openpyxl"` en vez de creerle a la línea. El Centro de Mando corrigió con esta
misma medición el CLAUDE.md raíz y `reference_archivar_ordenes_dropi`: era un dato caduco en la
pieza que lee toda sesión que abra la carpeta.

## GPG1.21 — 2026-09-20 · LA DECLARACIÓN DE FÁBRICA, EN EL LITERAL QUE SE LEE

El chat FILTRO midió que `REGISTRO-FABRICAS.md` decía "CENTRO DE MANDO (por ley: sin fábrica
declarada)" mientras el SKILL.md sí nombraba una fábrica. Revisado el generador: **no está
roto**. `registro-arsenal.py` rechaza a propósito las declaraciones en prosa e indexicales
("este chat"), porque tres casos medidos enseñaron que un regex difuso fabrica dueños
equivocados. El defecto era de esta skill: su línea 22 describía la fábrica por su encargo y su
fecha ("el chat de FER abierto el 2026-09-18"), que ninguna otra sesión puede resolver, y además
la fecha era la del encargo de DropKiller, no la de apertura del chat (2026-09-05).
Ahora dice `Fábrica: chat «✅ SKILL golden-productos-ganadores»`, el literal que el registro lee,
con el recordatorio de que la fábrica EJECUTA y la autoridad es FER → CdM → skill.
Aparte: al regenerar el registro el 2026-09-20 se pisó una corrección que el CdM había hecho a
mano sobre esa fila. Un archivo que se genera no guarda ediciones manuales: la corrección tiene
que ir a la FUENTE (el SKILL.md), que es lo que se hizo.

## GPG1.20 — 2026-09-18 · CIERRE DE LA CUARTA PASADA

La cuarta pasada del verificador (36 subcasos) encontró 7 de 10 fallas cerradas, 2 con variantes
vivas, 1 parcial y 1 viva, más 11 nuevas. Corregido:
- **La viva:** `entrega_golden.py` normalizaba por su cuenta (y SKILL.md decía lo contrario). Ahora
  usa `comun.py`; su ident quita ceros a la izquierda; la marca se busca en el nombre SOLO LETRAS
  ("Lecoterra2", "lecoterra_spray", "SPRAYLECOTERRA" se fugaban); `consultar` valida la tasa. El
  agregado reconstruido es idéntico al anterior. `seguimiento.py` lee fechas con `comun`.
- **Tasas sin rango:** `comun.tasa()` exige una fracción en (0, 1]; `correr_lote.py` valida el
  agregado al cargarlo (una tasa de 73.5 o -0.2 daba un PVP mínimo negativo que salía LISTA) y una
  entrega propia de 0% va a FUERA en vez de reventar.
- **Números:** "30,000" y "1,500" son miles (formato inglés); `--costo-min/max` con `comun`.
- **Fechas:** "2026-09-01garbage" y "T25:00" ya no son fechas.
- **Enlaces:** parser de URL (esquema, puerto): `whatsapp://`, `chat.whatsapp.com`, `walink.co`,
  `wa.me:443` y `m.me` ya no unen tiendas; nombres genéricos sin puntuación ni dígitos.
- **Dato que falta:** status vacío o "active" en minúscula cuenta ACTIVO (antes apagaba al
  proveedor y el criterio 2 aprobaba).
- **Menores:** `--registro` sobre archivo de solo lectura o carpeta; contador de duplicados que
  pasaba de una llamada a otra; `soldUnits: False` aceptado como 0; `dropi_id` con "../".
- **La lista:** la caída de stock del brasier se citó mal (9.199 en 12 días del 21-ago al 9-sep,
  no "9.000 entre el 25 y el 26"); el encabezado prometía que todo salía del script.
- **Del banco:** un comentario en la misma línea se había tragado dos claves del diccionario de
  la autoprueba del lote (dejaban de revisarse en silencio); un caso de ruta no mordía su sabotaje.
Autopruebas: 43, 52, 19, 28, 29, 17, 12 y 21.

## GPG1.19 — 2026-09-18 · UNA SOLA FORMA DE NORMALIZAR (cuarta pasada)

La tercera pasada del verificador (76 casos) confirmó lo grueso: los 12 estados de la lista
coinciden con `correr_lote.py`, los 7 PVP mínimos cuadran, el backtest v2 se reproduce idéntico y
su muestra no mira el resultado, y no quedan reglas derogadas vigentes. Encontró fallos de
robustez por CLASE, y se atacaron las clases:
1. **Normalización desigual entre scripts** → `scripts/comun.py` (clave, ident, numero,
   fecha_iso) y los 7 scripts la usan. "30.000" ya es treinta mil en todos lados; " 2233043" y
   "2233043" son la misma ficha; "Évora  Home" y "evora home", el mismo proveedor. La prueba de
   `viabilidad_cod.py` encontró que "0.727" se leía 727: ahora "0.x" es siempre decimal y las
   fracciones se leen sin miles.
2. **Verdad de Python sobre números** (`or 99`, `if tasa`): un 0% de entrega es un dato, no un
   vacío; 0 proveedores ordena primero, no último.
3. **Banderas validadas por rango, no solo por tipo** (negativos, 0, NaN, 3.5 proveedores, canal
   desconocido, `--dias 0`, piso negativo, costo 0).
4. **Cualquier forma rara del JSON** sale con error controlado (salida 2) en los 7 scripts.
5. **Dato que falta y aprobaba:** una ficha sin cifra de ventas ya no deja aprobar la etapa.
6. **Menú contra script:** 9C "el canal más libre" implementado (se cuentan landing y WhatsApp y
   el tope se mide en el más libre; se avisa que con Meta suele salir WhatsApp); 7A/7B y el
   verificado declarados como se aplican de verdad.
7. **Empresas:** la exclusión de Le'côterra pasa a ser por PRODUCTO ID (más el nombre
   normalizado antes de recortar); el agregado se reconstruye idéntico (103 productos, 72,7%).
8. **La lista del día sale del script:** `_corrida-2026-09-18/armar_lote.py` rearma los 12
   candidatos desde los crudos; `corrida_correr_lote.json` es la fuente; `_registro.jsonl` tiene
   los 12 para el seguimiento. Se guardaron los anuncios del nivel láser y la Montessori, que la
   lista citaba sin respaldo, y se borraron los `precios.json` viejos que la contradecían.
9. **calibracion.md:** "~200 por semana para ganar" era una extrapolación de la mediana y se
   presentaba como medida; se declara que el backtest midió fichas, no mercados consolidados.
Autopruebas: 43, 49, 19, 28, 29, 16, 11 y 16 (comun).

## GPG1.18 — 2026-09-18 · LA CALIBRACIÓN SE REHÍZO (tercera pasada del verificador)

El verificador adversarial corrió 91 casos contra la GPG1.17 y encontró 28 fallas. La más grave
era de MÉTODO: el backtest v1 estratificó la muestra por las ventas de los últimos 30 días, que
caían dentro del periodo de resultado. Se rehízo (backtest v2, muestra por fecha de creación, 144
historiales, 112 en VALIDACIÓN) y cambió lo que la GPG1.17 había escrito como medido:
- Se sostiene: piso de 10 en 7 días (bajo 10 murió el 92%, p < 0,001); el nivel predice mejor
  que la aceleración (0,74 contra 0,58).
- Indicio: 31 o más (murió 1 de 15, p = 0,06). Queda como valor PRUDENTE por defecto, no ley.
- Se cae: "más de 120 gana" (v1: 10 de 11; v2: 1 de 5, sin diferencia) y "31-120 gana ~25%".
- Sin medir: frenando (se confunde con el nivel bajo) → AVISO, no filtro; reabastecimientos
  (N = 2) → fuera del ranking; tope de proveedores y etapas → heredados, declarados.
Resto de lo corregido, por clase:
1. **Mezcla de empresas:** el agregado de entrega de Golden traía 6 productos de Le'côterra (sus
   sprays íntimos, 657 filas) vendidos por la misma cuenta de Dropi. `entrega_golden.py` los
   excluye por marca (`--excluir`) y los lista en el JSON; a quién pertenecen lo decide el CdM.
2. **Normalización:** fechas DD-MM-AAAA (38 de 109 productos salían con la primera fecha después
   de la última), estados con tilde o "EN BODEGA", IDs con espacio o ".0", etapa con tilde en el
   lote, dominios compartidos (wa.me, linktr.ee), nombres genéricos ("Tienda Online").
3. **Errores sin control:** 7 tracebacks en el lote, 6 en el seguimiento, 3 en entrega y 1 en
   ventas; ahora error de entrada con salida 2, y un candidato roto no tumba el lote.
4. **Datos que faltan y aprobaban:** historial viejo, sin costo, stock bajo, fecha de anuncio
   ilegible (ahora cuenta ACTIVO), historial que no cubre la ventana (INCOMPLETO en seguimiento).
5. **Filtros del menú sin pieza en el script:** `--max-7d`, `--min-stock`, `--canal`,
   `--costo-min/max`, `--solo-verificados`, `--antiguedad-min`; salida con `filtros_aplicados`.
6. **Cifras escritas a mano que no cuadraban:** tasa general (el lote usaba 73,5% del asset y la
   lista decía 72,9%; ahora usa la del agregado, 72,7%, y la imprime), "32 informes" (son 17
   "por producto"), orden del ranking distinto en guía y script, conteos de autopruebas.
7. **Moneda:** un precio menor de $1.000 no se compara (trampa 6).
Autopruebas: 41, 42, 19, 23, 23, 13 y 9; cada regla nueva tiene un sabotaje que muerde.

## GPG1.17 — 2026-09-18 · CALIBRADA CON HISTORIA REAL (8 propuestas del chat par)

El chat "Skill ganadora Drop Killer MCP" revisó la GPG1.16 y propuso 8 mejoras. Se midió cada
una antes de escribirla:
1. **Backtest** (`references/calibracion.md`): 100 historiales, 72 productos en VALIDACIÓN al
   19-jul, resultado a 60 días. El tope heredado "7 días ≤120" apuntaba al revés (más de 120: 10
   de 11 siguieron vendiendo; bajo 31 murió el 51-85%; frenando, 82%). **Ritmo por defecto: 7
   días ≥31, sin techo; frenando = alarma.** El nivel predice mejor que la aceleración (0,77
   contra 0,51); reabastecer 2+ veces, 43% contra 11%. Reproducido por la fábrica con el script
   del backtest. Datos y script en `PROYECTOS/CAZA-DIARIA-GANADORES/_backtest-2026-09-18/`.
2. **Entrega propia** (`scripts/entrega_golden.py`): 17 informes "por producto" de Dropi de Golden (de 32 en total: los otros 15 son "por pedido" y no traen producto) → 109
   productos, 16.616 pedidos terminados, entrega 72,9%, de 58,9% a 96,8% por producto. Si la
   empresa ya vendió el PRODUCTO ID (= externalId de DropKiller) con 30+ terminados, el PVP mínimo
   usa su tasa. El agregado vive FUERA de la skill (`_entrega_golden.json`), sin datos de clientes.
3. **Lote y registro** (`scripts/correr_lote.py`): todos los candidatos de una corrida en una
   pasada, estado LISTA / CASI / FUERA / INCOMPLETO, y una línea por candidato VISTO en
   `_registro.jsonl`. **Seguimiento** (`scripts/seguimiento.py`): a los 30 días compara LISTA contra
   CASI y FUERA; si no separan, recalibrar.
4. **Aceleración** en `ventas_reales.py` (7 días DEPURADOS contra el promedio semanal): dato y
   alarma de frenado; en el ranking va detrás del nivel y de los reabastecimientos.
5. **Canal por imagen** (`scripts/competencia.py canal`): imagen SOLA = 0 de 13 anuncios del
   producto; imagen + descripción = 14 de 14 y luego 6 productos más. Separa activos (vistos en 7
   días) del CEMENTERIO. El conteo por título inflaba: sopladora ~8 por título, 0 activos.
6. **Precio de la competencia** (`competencia.py precios`): `/products/<handle>.json` de Shopify,
   gratis; Firecrawl estaba sin créditos. Cambió dos veredictos: el nivel láser NO cierra ($84.900
   contra $85.641) y la olla tampoco (mediana $75.000 contra $114.808).
7. **Un solo juicio**: el estado de la caza manda sobre la rúbrica 0-100.
8. **Video 40 sin subtítulos**: sin Whisper instalado; descargar un modelo lo decide FER. Pendiente.

**Fallos encontrados construyendo (y arreglados):** Cabuco Store contado activo y en el cementerio
a la vez (dos páginas) y Anturio / Anturio Care como dos tiendas (misma landing) → identidad por
nombre O dominio; `precios` ignoraba `--incluir`; un pack de 2 comparado con el mínimo de 1 daba
"CIERRA" al shampoo; un ID de pedido 0 se perdía en `entrega_golden.py`; la aceleración contaba
picos ya recortados. Cada uno tiene su caso en la autoprueba y su sabotaje muerde.
**Declarado:** Firecrawl sin créditos el 2026-09-18 (AliExpress en ⚠️); el tope de 5 proveedores
sigue SIN VERIFICAR (DropKiller no da proveedores por fecha).
**Lista del día rehecha (v3):** brasier, sábana navideña y sopladora en la lista; 5 en CASI; el
cinturón y las luces pasan a "sin medir con el método nuevo".

## GPG1.16 — 2026-09-18 · LO QUE ROMPIÓ EL VERIFICADOR ADVERSARIAL

El agente golden-verificador (solo vio el estado final y el estándar) ejecutó 64 casos propios
y encontró 35 fallas. Todas se corrigieron o se declaran abajo. La CLASE de fallo, no el caso:

1. **Un dato que falta aprobaba.** `consolidar_mercado.py` reescrito: sin `createdAt` en algún
   espejo no se cree al alto; dos espejos que no cuadran dan el menor y lo dicen; un espejo en 0
   junto a otros con ventas se descarta como lectura perdida y se avisa; sin `stock` el proveedor
   cuenta como activo; sin nombre cada ficha es un proveedor distinto; sin `externalId` no hay
   espejo; un mercado vacío no pasa ningún criterio. Banco `banco_consolidacion.json` de 16 a 42
   chequeos (casos V1-V10 con las entradas exactas del verificador); 3 sabotajes muerden.
2. **`ventas_reales.py`**: "stock final en 1" ya no condena una caída de menos de 20 (un lento que
   agota sus 5 últimas); tras un hueco de lectura de ≥3 días el pico se mide a 3× la base, no a 5×
   (un vaciado de 300 escondido en 16 días pasaba entero); 4+ caídas idénticas muy por encima del
   resto = DUDOSO (vaciado por lotes); el pico de exactamente 50 se recorta; ventas negativas
   cuentan como 0 y se avisa. Banco adversarial de 13 a 18 casos, autoprueba 39/39; 5 sabotajes
   muerden. La expectativa del caso V2 era errada (conté 15 días de hueco y son 16): corregida
   con la razón escrita en el banco.
3. **Entradas rotas** (data null, fila corta, fecha numérica, regex inválido, `--pais` sin valor,
   fecha sin zona, ventas en texto): error de entrada claro con salida 2, sin traceback.
4. **`viabilidad_cod.py`** acepta tasas solo como fracción: `--entrega 73.5` o `--comision 4`
   daban PVP mínimos falsos (uno negativo) sin avisar. **`metricas_saturacion.py`**: con Meta
   reportando 0 ya no dice "100% Alta".
5. **El menú ofrecía lo que el script no aplicaba**: `--etapa` y `--max-proveedores` nuevos;
   "NUEVO con 100 o más" (imposible por definición) sale del preset diario y de la guía; las
   opciones 2, 3, 9, 10 y 12 ahora explican qué cambian; sección nueva "Lo que la corrida le
   debe al menú": un filtro elegido se aplica o se declara no aplicado.
6. **Números viejos**: "8 chequeos" (eran 16, ahora 42), y el blindaje declarado como "chmod puro,
   sin chflags" cuando el disco tiene `uchg` en todos los nodos (lo pone golden-blindaje). Ya no
   se escribe el número de nodos.
7. **Reglas derogadas vivas**: "flete de ida y vuelta" en la rúbrica y "costo × 3" en
   sourcing-local.md (con su ejemplo recalculado: la camiseta sola necesita $75.224; el 3×2 pasa).
8. **Goteo de preguntas** en Temu/MercadoLibre y en la lista de keywords de la Ad Library: ahora
   se declara y se sigue.
9. **La ficha** lleva la línea de afiliación; **la regla 8** nombra los productos para adultos
   (política de Meta), que la lista descartó sin regla que lo apoyara.
10. **La lista de caza** (§7) pide: línea "No aplicado", ventas de 7 días, avisos del script,
    PVP solo en pesos, sección CASI para lo que rompe un filtro, ninguna cifra sin fuente, y
    "0 vistos" con pocas keywords = no medido.

**Sin corregir, declarado:** el esquema real de DropKiller (nombres de filtros) no lo pudo mirar
el verificador; `assets/economia-cod-golden.json` trae cifras de Golden (pauta y pedidos) y va
como fila al Centro de Mando antes de cualquier publicación de la skill a un repositorio público.

## GPG1.15 — 2026-09-18 · LO QUE ENSEÑÓ LA PRIMERA CORRIDA REAL

Corrida de prueba del modo CAZA en Colombia con todos los filtros en "no sé" (lista en
`PROYECTOS/CAZA-DIARIA-GANADORES/2026-09-18-CO.md`): 35 candidatos, 6 descartados a la vista, 12
por el embudo completo, 8 en la lista (17 sin revisar, declarados). Lo que la corrida rompió y se arregló:
1. **`maxTotalSold` no existe** en `search_products` y se ignora sin error (trampa 9). El menú
   lo mandaba pedir. Ahora el techo de etapa lo pone `consolidar_mercado.py`.
2. **Espejos que no cuadran** (trampa 10): tomar el máximo daba al brasier 2.324 cuando dos de
   tres espejos decían 1.193. `consolidar_mercado.py` toma la mediana, salvo que el espejo alto
   sea también el más viejo por >7 días (tablero LED de impor house, legítimo). Si falta
   `createdAt`, el aviso lo dice. Banco `banco_consolidacion.json` 16/16; los dos sabotajes
   (siempre el máximo, ignorar la fecha) lo bajan a 14/16.
3. **Criterio 3 por título es ruidoso**: se cuentan páginas distintas del producto, no anuncios,
   y se declara que no separa landing de WhatsApp.
4. "8 trampas" pasa a "10 trampas" en SKILL.md y en `dropkiller-caza.md`.

## GPG1.14 — 2026-09-18 · MODO CAZA CON DROPKILLER (orden directa de FER)

**El encargo, en palabras de FER:** ver el video de Juan Vargas y muchos más de él y de
DropKiller, analizar cada uno y hacer "una skill poderosa, mucho más que la que él tiene, con
muchos más filtros, que cuando la invoque me diga qué quiero hacer hoy; si no sé, que busque
todo; 10 productos ganadores todos los días".

**Corpus:** 40 videos listados, **39 leídos completos** (transcripción deduplicada), 1 sin
subtítulos (SmartFinder 2.0, 1:17). 18 del canal de Juan Vargas, 3 clases suyas en comunidades
(Armando Soto, Black Lions, Prana), 13 del canal oficial de DropKiller, 5 de practicantes
(Marcio Barahona, Naider Ortiz ×2, Jonathan Rengifo, Keiner Chará). Juan Vargas es
**cofundador** de DropKiller: fuente interesada, método bueno, cifras sin fuente.

**Conector medido herramienta por herramienta** (30 herramientas, 18-sep-2026). Hallazgos que
ningún video dice y que cambian el resultado:
1. **Ventas FANTASMA.** DropKiller deriva las ventas de la caída de stock (probador de
   inyectores: 500 − 378 = 122, exacto). Top 20 de `find_winning_products` en Dropi Colombia:
   **9 de 20 eran ajustes de inventario**, entre ellos el #1 (turkesterone, 2.961 en un día,
   stock final 1) y el #2 (virex, 3.000 → 300 = "2.700 vendidos"). → `scripts/ventas_reales.py`.
2. **Espejos de plataforma.** El mismo producto sale una vez por plataforma que refleja Dropi
   (DROPI, WINPY, DROPLATAM, SEVENTY_BLOCK), mismo `externalId` y mismo historial. Aplicar al pie
   de la letra "suma todos los proveedores" (la regla central de Juan) contaba Dr. Melaxin 4
   veces. Consolidado bien: 19.049 ventas, QUEMADO, y es el #6 "ganador". →
   `scripts/consolidar_mercado.py`.
3. **Días sin lectura** con stock 0, precio 0 y ventas 0 (antes de crear el producto y el día en
   curso). Tomados como lectura, un producto sano parecía vaciado.
4. **"ACTIVE" no es activo hoy** (anuncio con fin 21-ago), **país mal asignado** (córdobas
   marcado Colombia), **"con stock" = 1 unidad** (3 de 8), **ingresos de tiendas retirados por
   el propio conector** el 2026-07-02.
5. **Reabastecimientos:** Juan pide contarlos y reconoce que DropKiller no los da ("anótala");
   se cuentan desde el mismo historial.

**Verificación de los scripts (no a la primera):** `ventas_reales.py` dio 21/21 contra el banco
real a la primera; por la regla de la casa se sospechó del script y se escribió un banco
adversarial: salieron **2 fallos reales** (un producto lento marcado fantasma; un vaciado
partido en dos lecturas que pasaba como real) y un tercero que pasaba por suerte (hueco de 5
días). Corregidos con piso absoluto, línea base robusta sin el 20% alto y ritmo por días
transcurridos. Final: **34/34** y **6 sabotajes que muerden** (sin línea base robusta, sin
normalizar huecos, sin piso de 100, sin regla de constancia, sin descartar días sin lectura,
umbral de reabastecimiento). `consolidar_mercado.py`: **8/8** y 3 sabotajes que muerden.
Dos sabotajes NO mordieron la primera vez (huecos y días sin lectura): el banco solo miraba el
veredicto; se agregaron las cifras depuradas y el caso exacto donde el día sin lectura decide.

**Lo nuevo en la skill:** `references/menu-arranque.md` (el menú de "qué quieres hacer hoy" con
todas las opciones y su valor por defecto), `references/dropkiller-caza.md` (método, trampas,
3 criterios, etapas por país, 6 rutas, embudo, lo que se rechaza), sección 7 de
`entregable.md` (LISTA DE CAZA), `assets/tarea-diaria-caza.md` (rutina; se crea solo con el sí
del usuario), cinco modos en el cuerpo (CAZA, VALIDAR, ESPIAR, CREATIVOS, RUTINA).

**Lo que se rechazó de los videos:** testimonios "reales" fabricados con IA y "testimonio de
supuesto doctor" (Kj_-5bTr-6I), bot que se hace pasar por especialista que "cura el hormigueo"
(y-OWDawyb2c), marcas ajenas en catálogo público. Van escritos como prohibidos.

**Mandato del 2026-09-05 (caso Candida Cleanse) que seguía pendiente:** reglas 5 a 9 del cuerpo
(ficha técnica de la ETIQUETA, alérgenos publicados, el error por defecto es tuyo, mirar qué
producto sale en cámara, piezas prohibidas, un cero se prueba). 0 menciones antes; ahora en el
cuerpo y en la plantilla de la ficha.

**Correcciones de consistencia encontradas de paso:** (a) el cuerpo decía a la vez "CPA
$21.428 medido" y "CPA $14.000 supuesto, mientras no se mida"; corregido y la economía COD
mudada completa a `references/economia-cod.md` (cuerpo de 356 a ~290 líneas antes de agregar
lo nuevo); (b) `entregable.md` pedía "Margen: <x>" y juzgaba el piso con "costo × 3", las dos
reglas que GPG1.12 había derogado; alineadas con `viabilidad_cod.py`.

**Fábrica:** el chat de FER abierto el 2026-09-18 para integrar DropKiller, por orden directa de
FER en ese chat. Su título se parecía al nombre de una skill que NO existe: no hay skill aparte
de DropKiller, todo vive aquí. Se informa al Centro de Mando; `REGISTRO-FABRICAS.md` se regenera con su script.

## GPG1.13 — 2026-09-13 · auditoría golden-skill-auditor (dos hallazgos reales, verificados a mano)

**1 · Puntero de versión desincronizado.** El comentario HTML bajo el H1 del SKILL.md decía
GPG1.11 mientras el campo Versión ya decía GPG1.12 y la entrada más reciente de verdad de
esta acta es GPG1.12-d (2026-09-06, cuarta corrección del CPA el mismo día). Un lector que
solo abriera el tope del archivo creía que lo último fue la mudanza del changelog (GPG1.11)
cuando en realidad el reescrito completo de la economía COD (GPG1.12, con sus cuatro
correcciones a/b/c/d) es posterior y es el que está vigente en `scripts/viabilidad_cod.py` y
`assets/economia-cod-golden.json`. Corregido: el comentario del tope pasa a ser el puntero
vigente.

**2 · Blindaje mal declarado.** Tanto el SKILL.md (sección "Operación de esta skill") como
`golden-skill-auditor/scripts/inventario.sh` decían "chflags uchg". Verificado a mano con
`stat -f "%Sp %Sf"` sobre los 12 nodos y con un intento real de escritura (`echo >> SKILL.md`
→ permission denied antes de tocar nada): **el mecanismo real es CHMOD 0444 (archivos) /
0555 (directorios), sin ningún chflags activo** (`flags=-` en los 12). La etiqueta anterior
nunca se había verificado contra el disco. Corregido en SKILL.md; el mecanismo real queda
documentado con el comando exacto de abrir/cerrar.

**Sin otros hallazgos con evidencia** tras esta ronda: `validar_arsenal.py` exit 0,
`viabilidad_cod.py --autoprueba` 19/19 (reproduce los casos ancla del FILTRO y muerde ante
el sabotaje de los 5 parámetros), sintaxis OK en los 2 scripts, `metricas_saturacion.py`
probado contra un caso malo conocido (activos > históricos → avisa, no concluye falso
125%), 0 referencias rotas ni huérfanas, y las 5 hermanas citadas
(golden-investigacion-mercado, golden-shopify, golden-copywriting,
golden-meta-ads-analysis, golden-skill-auditor) existen todas hoy en `~/.claude/skills`.
Re-blindada al cierre con el mecanismo real: `chmod -R a-w`.

## Mudado del cuerpo del SKILL.md el 2026-09-06 (auditoría golden-skill-auditor)

<!-- skill GPG1.11 · 2026-09-06 · la mudanza del 2026-09-05 se había declarado completa sin estarlo:
el cuerpo de SKILL.md seguía cargando en cada activación la sección `## Changelog` entera (versiones
GPG1.10, GPG1.8, GPG1.6, GPG1.4 verbatim), contradiciendo la línea de arriba y el principio de
divulgación progresiva. Y esta acta, que se decía "completa, nada se borró", en realidad NO tenía la
entrada GPG1.6 propia — solo aparecía citada de pasada dentro de GPG1.7. Arreglado: GPG1.6 migrada
íntegra a esta acta (ver entrada abajo, entre GPG1.7 y GPG1.5, en su orden cronológico) y el cuerpo
de SKILL.md se redujo a un puntero de 2 líneas a este archivo. Verificado con
`golden-skill-auditor/scripts/inventario.sh` y `validar_arsenal.py` tras el cambio: 0 referencias
rotas, 0 huérfanas, exit 0. -->

## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 984 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->

<!-- skill GPG1.10 · 2026-08-24 · Barrido total del arsenal (auditoría fresca golden-skill-auditor,
CdM): (a) 🔴 la fuente "deep-research (skill)" NO existe instalada — verificado con ls del arsenal;
reemplazada por la vía real (WebSearch + firecrawl_search/firecrawl_agent) sin perder el caso de uso;
(b) metricas_saturacion.py probado contra un caso malo NUEVO (activos > históricos): devolvía
"supervivencia 125% — categoría sana" en vez de gritar — guardia de totales inconsistentes agregada
y re-probada (ahora: no concluir, repetir las llamadas); los 3 casos medidos de siempre siguen dando
idéntico (3,3% · 74,3% · muestra<30); (c) el recordatorio Apify/Google Maps del 2026-08-12 ya venció
— anotado como APLAZADO vigente hasta orden explícita de FER, no arrancar solo -->

<!-- skill GPG1.9 · 2026-08-23 · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se
reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR -->

<!-- skill GPG1.8 · 2026-08-21 · auditoria golden-skill-auditor (880/1000 antes de reparar): (a)
SOURCING LOCAL sacado del cuerpo a references/sourcing-local.md — no hace falta en cada corrida,
solo cuando el producto no esta en Dropi; (b) fallback agregado si candado_scraping.py (script de la
hermana golden-investigacion-mercado) no existe o falla: verificacion manual de la Regla Cero, no se
detiene el flujo; (c) duplicado "el informe se entrega siempre" (aparecia en SKILL.md Y en
entregable.md) reducido a una sola fuente en entregable.md, SKILL.md solo apunta; (d) blindaje
documentado explicitamente: chflags uchg, coherente con el resto de skills golden- publicas -->

<!-- skill GPG1.7 · 2026-08-02 · AMAZON RESUCITA POR NAVEGADOR y cae la afirmacion no verificada. GPG1.6 dijo "para Temu y Amazon usar Chrome MCP" SIN PROBARLO — se escribio por deduccion, el mismo error que esta skill corrige en todas partes. Medido hoy: (a) AMAZON POR NAVEGADOR ✅ es la MEJOR fuente del scanner — 48 tarjetas, 34 con "comprados el mes pasado" (71%), 46 con precio, 45 con rating, total "155 resultados", precios en COP y envio a Colombia detectados solos; da mas que AliExpress. Receta con selectores en el cuerpo. (b) TEMU ❌ por ninguna via: muro de SESION ("Email o numero de telefono"), no es JS es autenticacion; solo saldria con claude-in-chrome si FER ya tiene sesion — preguntar, no asumir. (c) MERCADOLIBRE CO ❌ nuevo: por Firecrawl da CAPTCHA y el extractor inventa "Producto 1..8" con precios y ratings falsos CON metadata.title poblado (modo 4, rompe el check 2); por navegador, muro de sesion. (d) DESCRIPCION corregida: prometia "TikTok Creative Center" que no se puede leer — ahora nombra AliExpress y Amazon, que si. (e) COMPUERTA nueva: pasar todo scrape por candado_scraping.py antes de puntuar -->

<!-- skill GPG1.6 · 2026-08-01 · AUTOCORRECCIÓN de GPG1.4: había sobre-generalizado desde un solo sitio. GPG1.4 declaró el scanner de volumen "migrado a Firecrawl" para Temu/AliExpress/Amazon habiendo probado SOLO AliExpress. Ejecutadas las tres el 2026-08-01: AliExpress ✅ · Temu ❌ · Amazon ❌ · TikTok Creative Center ❌. Temu redirige la búsqueda a la portada y devuelve 72 categorías de ropa con precio "N/A"; Amazon responde con muro anti-bot y sin campo `json`; TikTok CC es una app JS que solo entrega su menú. Matriz de fuentes ahora en la skill, fuente por fuente, con su estado medido. Para Temu/Amazon vuelve el Chrome MCP — y se prohíbe simular que Firecrawl los cubre. Regla Cero ampliada de 1 a 3 modos de fallo: el check de metadata.title de GPG1.4 solo cazaba la alucinación total; Temu falla con title poblado (modo señuelo) y Amazon falla con title poblado y sin redirección (modo muro). Se añade la verificación que sí caza los tres: "el dato responde a lo que pedí?". Lección de método, la misma de GPG1.5: no basta con ejecutar la herramienta una vez — hay que ejecutarla contra cada fuente que la skill promete. (NOTA golden-skill-auditor 2026-09-06: esta entrada solo existía como texto vivo en el cuerpo de SKILL.md hasta esta reparación — el acta se declaraba "completa" y no lo era; movida aquí sin perder una palabra, y el cuerpo queda solo con el puntero.) -->
<!-- skill GPG1.5 · 2026-07-27 · AUDITORIA con golden-skill-auditor tras pregunta de FER ("por que no lo habias descubierto"): la causa raiz fue auditar el TEXTO de la skill y nunca EJECUTAR la herramienta que recomienda. Ahora medido en vivo: (a) CEMENTERIO nuevo — comparar ad_active_status ACTIVE vs ALL con limit:1 da la tasa de supervivencia de la categoria (fibra capilar CO: 1.496 activos / 2.014 historicos = 74,3%; <40% = bandera roja aunque hoy se vean tiendas activas). Supera al metodo de terceros, que lo planteaba como chequeo manual opcional. (b) CORRECCION de GPG1.4: el sesgo de recencia solo aplica cuando el total SUPERA el limit; si es menor se recibe todo, historico incluido (medido: 9 de 9, uno de 36 dias). La redaccion anterior era imprecisa. (c) ESTRUCTURA: de 295 lineas en un solo archivo a SKILL.md + 2 references (divulgacion progresiva). (d) Del metodo ajeno se adapto lo que faltaba: mapa de angulos con HUECOS y hooks, lectura de precios (techo/piso), MODO LOTE con ranking y lectura transversal, fast-flags, y la regla de entregar el informe tambien cuando el veredicto es NO -->

<!-- skill GPG1.4 · 2026-07-27: filtro de un metodo de validacion de terceros (Vertex Digital, otra empresa — se extrajo el METODO, nada de su marca). Aporte propio MEDIDO: los 2 sesgos del MCP ads_library_search — tope duro de 50 sin paginacion (cobertura 3,3% sobre 1.496 reportados) y devuelve LOS MAS RECIENTES (los 50 de la prueba cubrian 4,5 horas del mismo dia), asi que NUNCA muestra el anuncio de 30+ dias que esta misma skill declara señal reina: contradiccion interna real, ahora documentada con su workaround por navegador. Del metodo ajeno se horneo: minimo 8 keywords en 4 capas con permutaciones, REGISTRO DE COBERTURA obligatorio (0 encontradas != no revisadas), filtrado de ruido y dedup por tienda, curva de saturacion numerica (0=riesgo no oportunidad, 1-3 punto dulce, 4-7 competido, 8+ saturado), señales por competidor y indice de anuncios con link directo por ID -->

<!-- skill GPG1.3 · 2026-07-27: corregido por FER — Golden opera COD Y pago anticipado, y el producto ganador es DISTINTO en cada uno. Regla 2 partida en dos, rubrica ahora con dos columnas y criterio RECOMPRA nuevo (20 pts) que solo existe en marca propia: un consumible aburrido saca 55 como catalogo y 78 como marca propia -->

<!-- skill GPG1.2 · 2026-07-25: filtro del paquete RECURSOS EGS — umbral duro de antigüedad (≥60 días = máximo, <14 no concluyente), rankear Ad Library por GASTO estimado y no por número de anunciantes, y sección SOURCING LOCAL nueva (grupos mayoristas con el texto de publicación, grilla de 6 factores, señales de alarma, adaptado a San Victorino/El Restrepo/El Hueco) -->

<!-- skill GPG1.1 · 2026-07-25: nueva fuente SCANNER DE VOLUMEN VISIBLE (Temu/AliExpress/Amazon por navegador, contadores de órdenes como señal de demanda dura) — patrón destilado de las extensiones de WiFi Money; se replica con el MCP de Chrome sin instalar código ajeno -->

<!-- skill GPG1.0 · creación: Ad Library como prueba reina + rúbrica 0-100 + ficha entregable -->

## GPG1.12 — 2026-09-06 · El margen deja de estimarse: se calcula con los números de Golden

**Qué estaba mal.** La rúbrica puntuaba el margen con una regla de pulgar: *"PVP/costo ≥3× =
puntos llenos"*, heredada de un curso que usa **números de referencia prestados**. El chat
FILTRO los midió contra **18.391 pedidos reales de Dropi** (16 informes por producto,
mar-2024 a ago-2026) y no coinciden:

| | curso | Golden medido |
|---|---|---|
| tasa de entrega | 75% | **73,4%** (n=15.543 terminales) |
| flete de entrega | $12.000 | **$15.664** (n=11.409 entregas) |
| pedido FALLIDO | $8.000 | **$29.182** — 3,6 veces más |

El del fallido es el que rompe la cuenta. Con los números del curso, un producto de costo
$30.000 vendido a $80.000 parece dejar **$26.500** por pedido generado; con los de Golden deja
**$1.092**. La misma ficha, dos negocios distintos.

**Qué se añadió.**
· `assets/economia-cod-golden.json` — los cinco números en un solo sitio, con su n y su fuente,
  y **los dos no medidos marcados como SUPUESTO**: comisión de recaudo (4%) y **CPA ($14.000
  por pedido generado)**. El CPA real vive en `cm_gastos`, de Golden Group Enterprise.
· `scripts/viabilidad_cod.py` — la cuenta, **por pedido GENERADO** (la pauta se paga por cada
  pedido que entra, llegue o no; contar solo los entregados esconde el 26,6% que cuesta y no
  paga). Da veredicto contra el piso de $8.000, o el **PVP mínimo** si aún no hay precio.
· La compuerta entra en el **flujo (paso 2c)** y en la rúbrica: **lo que no pasa el piso no se
  puntúa**, por bueno que se vea en todo lo demás.

**Hallazgo propio al correr la fórmula contra varios costos: el multiplicador NO es constante.**
$10.000 → **6,90×** · $30.000 → 2,99× · $80.000 → **1,77×**. Flete, fallido y CPA son costos
FIJOS por pedido y no escalan con el costo del producto, así que **"3×" solo es cierto cerca de
$30.000, que es justo el ejemplo del curso**. Consecuencia práctica: **los productos baratos son
mucho más difíciles de lo que parecen** — uno de $10.000 vendido a $50.000 suena a 5× y pierde
plata. Por eso lo que se lleva a la ficha es **el piso de $8.000, no un multiplicador**, y hay
una prueba que caza a quien vuelva a clavar la cifra.

**Verificación.** Autoprueba 13 de 13: reproduce **al peso** los dos casos ancla del FILTRO
($89.804 → $8.000 y $80.000 → $1.092), comprueba que el despeje y la evaluación coinciden, y
**sabotea uno por uno los cinco números**: si cambiar cualquiera no mueve el resultado, ese
número no se estaba usando y la fórmula sería decorativa.

**Reconciliación que salió del ejercicio:** el FILTRO publicó los dos casos ancla pero no la
fórmula. Reproducirlos al peso obligó a despejar sus dos supuestos implícitos: **comisión 4% y
CPA $14.000**. Ahora están escritos y marcados como supuestos, en vez de vivir dentro de un
resultado que nadie podía auditar.

**Además:** `Fábrica: este chat` era un indexical sin referente —leído desde otra sesión no
nombra a nadie— y el registro de fábricas ya lo señalaba. Declarado literal: **CENTRO DE MANDO**.
Y en `references/ad-library-metodo.md` quedó escrito **por qué** `ad_type=all` no es decorativo:
sin él Meta cambia sola a anuncios políticos y devuelve vacío. Medido: 2.200 anuncios de
"taladro" en Colombia con la URL completa, **cero** con `?q=` pelado. De ahí sale la creencia de
que la Ad Library no acepta parámetros por URL.

### GPG1.12-b — corrección el mismo día · el costo del fallido pasa de MEDIDO a AMBIGUO

Escribí `$29.182` como dato medido, con la explicación de que la columna guardaba ida+vuelta.
**El chat FILTRO se corrigió y esa explicación era suya, no del dato.** FER la descartó por
conocimiento del acuerdo Dropi: hay un flete base y un porcentaje por gestión de cobro; si el
pedido se devuelve no hubo cobro, así que **es UN SOLO cobro, no ida y vuelta** — a veces la
devolución cuesta MENOS, precisamente porque no hubo recaudo.

Y lo definitivo: **el informe 'por producto' no puede responder la pregunta.** `GANANCIA` está
en cero en 4.116 de 4.120 devoluciones, o sea que el impacto real del cobro no se registra ahí.
La columna sale 1,85× el flete con desviación mínima y nunca por debajo: es un campo
**calculado**, no un costo observado, y qué calcula no se sabe.

**Qué se hizo**: el número sale de `medidos` y entra en `ambiguos`, con las tres lecturas y su
detalle. El script ya no da el veredicto con un número elegido a dedo: **lo da contra las tres**,
y si no coinciden lo dice y entrega el rango en vez de un sí o un no. Por defecto usa la más
cara — si pasa con la más cara, pasa con todas.

**La regla se sostiene, y ahora mejor:** mínimo entre **2,80× y 2,99×** según la lectura, con
costo $30.000. A 2,5× se descarta en las tres. **El 2,5× del curso no alcanza bajo ninguna.**

Verificación: mi fórmula reproduce las tres cifras del FILTRO (2,82 · 2,99 · 2,80) sin tocar
nada más, lo que confirma por tercera vez los dos supuestos que despejé (comisión 4%, CPA
$14.000). Autoprueba **19 de 19**, con un caso que exige que el aviso **MUERDA** cuando las tres
no coinciden (PVP $87.000): un aviso que jamás se dispara pasa por bueno para siempre.

**Ley que queda:** *cuando una ambigüedad no cambia la decisión, se declara y se sigue.* Y la
otra, del FILTRO: *antes de decirle a FER que sus números no cuadran, preguntarse qué significa
de verdad la columna, y si el archivo puede siquiera responder la pregunta.*

### GPG1.12-c — tercera corrección del mismo día · el fallido estaba INFLADO al doble

**El número bueno es $12.518, no $29.182.** FER avisó de que *"hay dos informes"* y tenía razón:
en disco hay 16 informes **por producto** y 16 **por pedido**, y el FILTRO había inventariado
solo la primera familia. En los de *por producto* esa columna la llena **una sola transportadora**
(1.537 de 4.120 filas = 37%) y encima inflada; los 2.583 "ceros" que se habían leído como dato
faltante **eran las demás transportadoras**. Los de *por pedido* cubren **4.074 de 4.120 = 99%** y
todas las transportadoras.

**El modelo de FER queda confirmado transportadora por transportadora.** Un solo cobro, siempre
menor que el flete de ida: Coordinadora 0,73 · Envía 0,80 · JAMV 0,80 · Veloces 0,81 · TCC 0,86 ·
Interrapidísimo 0,87 · **Servientrega 1,00**. Él intuyó que había una que cobraba lo mismo y dijo
Interrapidísimo: **el fenómeno existía, le fallaba el nombre, no la regla.** Y solo 1 de 4.120
devoluciones tiene comisión > 0, lo que confirma que sin entrega no hay gestión de cobro.

**Qué cambió aquí:** entrega 73,4% → **73,5%**; el fallido sale de `ambiguos` y vuelve a
`medidos`; la tabla de multiplicadores se recalcula entera ($10.000 → **6,26×** · $30.000 →
**2,78×** · $80.000 → **1,69×**); y el bloque de robustez **no se borra: se muda**. La
incertidumbre no desapareció, se concentró en los dos supuestos que siguen sin medir, así que
ahora el veredicto se corre en **dos escenarios** (con supuestos y sin pauta) y si cambia entre
ellos el script **se niega a dar un sí o un no**. Borrar el bloque habría hecho parecer que ya no
queda nada estimado, que es lo contrario de lo que pasa.

Medido: el informe malo exigía **$6.258 más de PVP a cualquier costo** — un desplazamiento
constante, no proporcional. Hay una prueba que lo fija para que el número retirado no vuelva.

Autoprueba **19 de 19**, recalibrada: los seis multiplicadores de la tabla contra la fórmula, el
sabotaje de los cinco parámetros, y el caso que exige que el aviso de escenarios **muerda** cuando
el CPA decide el veredicto (PVP $80.000).

**La guarda que se validó sola:** el multiplicador se movió **dos veces en un día**. Llevar a la
ficha el **piso en pesos** y nunca una cifra de multiplicador dejó de ser una preferencia de
redacción y pasó a ser lo único que aguantó las dos correcciones.

**Ley que queda:** *cuando un directorio tiene FAMILIAS de archivos distintas, el inventario son
TODAS, no la que la memoria ya nombraba.* La fase 1 pide contar el universo antes de tocar, y
contar 16 de 32 produjo un número inflado al doble que ya estaba escrito en una skill.

### GPG1.12-d — cuarta corrección del día · el CPA se midió: $21.428, no $14.000

El supuesto **se quedaba 53% corto**. Medido sin tocar `cm_gastos`: pauta Meta mensual por cuenta
contra pedidos creados por mes, `_MOTOR/_pauta_mensual.csv`, agregado 2026 $97.605.767 / 4.555
pedidos. Mensual: ene $20.891 · feb $21.290 · mar $19.679 · abr $16.377 · may $22.616 · jun
$25.822 · jul $14.947.

🔴 **Es un PISO, no un punto**, y así queda escrito: el denominador son TODOS los pedidos creados
—incluidos orgánico, WhatsApp y recompra— y un mes puede estar incompleto. El sesgo va en una
sola dirección, hacia arriba. **Todo veredicto que salga de aquí es optimista por construcción.**

**Por eso el informe dejó de quedarse en un sí o un no y ahora dice CUÁNTO CPA AGUANTA el
producto.** Es un número derivado, no un supuesto inventado, y es lo que separa un margen real de
uno de papel: si un producto aguanta $23.000 y el piso medido es $21.428, ese margen puede no
existir. Comprobado que en su PVP mínimo el aguante da exactamente el CPA medido.

**Tabla vigente**: $10.000 → **7,31×** · $20.000 → 4,18× · $30.000 → **3,13×** · $50.000 → 2,30×.

🔴 **Lo más importante del episodio: los dos errores se compensaban.** Con el fallido inflado
(que sube el mínimo) y el CPA supuesto (que lo baja) salía **2,99×**; con los dos corregidos sale
**3,13×**. Casi el mismo número por dos errores en direcciones opuestas. **Arreglar solo uno
habría empeorado la regla creyendo que se mejoraba**, y nadie lo habría notado porque el número
final seguía pareciendo razonable. Hay una prueba que fija los tres valores para que se vea.

**Verificación cruzada, con una discrepancia reportada.** Los cuatro multiplicadores del FILTRO
se reproducen exactos. Su tercer número no: publicó que a PVP $80.000 el producto deja **−$4.104**,
y eso **no cuadra con su propio PVP mínimo** ($93.964). Desde ese mínimo, bajar a $80.000 son
$13.964 × 0,7056 = $9.853 menos, o sea **−$1.853**. La skill usa el valor coherente (−$1.860) y
la discrepancia se le devolvió.

Autoprueba **19 de 19**, recalibrada. El multiplicador va por su **tercer** valor en un día
(2,99 → 2,78 → 3,13), lo que confirma por tercera vez la decisión de llevar a la ficha el piso en
pesos y nunca una cifra.
