---
name: golden-dropi-analisis
description: >-
  Golden Group — analiza los informes de Dropi (COD, contra entrega) y genera 2 maestros
  Excel listos para decidir: MAESTRO_LOGISTICA (porcentaje de entrega global y por producto,
  transportadora, departamento y ciudad; mejor transportadora por ciudad; novedades;
  evolución en el tiempo) y MAESTRO_CONTACTOS (todos los clientes sin duplicados, con
  porcentaje de efectividad, segmento VIP o riesgo, etiquetas de WhatsApp, leads del bot y
  lista de posibles para mensaje masivo). Úsala SIEMPRE que el usuario quiera analizar sus
  ventas o entregas de Dropi, procesar los reportes o exports de Dropi, saber qué
  transportadora le entrega mejor, bajar devoluciones, sacar su base de clientes o segmentar
  para remarketing; o diga "analiza mis Dropi", "informe de entregas", "reporte de Dropi",
  "mejor transportadora", "cuánto entrego", "mi base de clientes de Dropi", "clientes VIP",
  "por qué me devuelven", "consolida mis órdenes", o suba archivos ordenes_*.xlsx u
  ordenes_productos_*.xlsx.
---

**Fábrica:** chat «✅ SKILL golden-dropi-analisis»
<!-- skill v1.8 · 2026-09-19 · CdM: la sección de rentabilidad decía "flete de ida y vuelta" (ley derogada); el motor ya calculaba bien con COSTO DEVOLUCION FLETE. Anterior: v1.7 · 2026-09-13 · auditoría golden-skill-auditor: faltaba la línea de versión bajo el H1 (Estándar 7 de la casa) — el comentario solo apuntaba al changelog sin declarar la versión vigente, quedando desincronizado con la última acta (v1.6.1). Se agrega el número aquí; historial completo de esta skill: references/changelog.md (1 actas, mudadas el 2026-09-05). El cuerpo se paga en cada activación; el acta no. Cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR (Estándar 9). -->
# golden-dropi-analisis


Convierte los exports crudos de Dropi en **dos archivos maestros que se leen solos** y en
**decisiones**: con qué transportadora enviar en cada ciudad, qué productos entregan mejor,
a qué clientes venderles de nuevo y a quiénes solo con pago anticipado.

No lo hagas a mano: hay un motor probado en `scripts/motor_analisis_dropi.py` que lee todo,
clasifica y arma los dos Excel con formato. Tu trabajo es organizar los archivos, correr el
motor y **entregar los hallazgos accionables**, no recalcular en tu cabeza.

## Qué produce (en `<carpeta>/Analisis/`)

- **RESUMEN_EJECUTIVO.pdf** — EL documento que el dueño lee primero: en qué estado está cada
  orden (entregada/cobrada · en camino · en camino a devolución · devuelta/perdida ·
  cancelada), el P&L (ganancia realizada − costo de devoluciones − gasto de publicidad =
  **utilidad neta**) y el **veredicto RENTABLE / NO RENTABLE**. Sin gasto de publicidad no hay
  veredicto: el número entra por `_config_dropi.json` (o se pide/consulta). Un análisis sin este
  resumen "no sirve" — es lo primero que se entrega.
- **MAESTRO_LOGISTICA.xlsx** — hojas: `RESUMEN EJECUTIVO` (el mismo P&L, primera hoja),
  `RESUMEN` (KPIs globales y por cuenta), `EVOLUCIÓN` (por periodo, cronológico),
  `POR PRODUCTO`, `POR TRANSPORTADORA`, `POR DEPARTAMENTO`, `MEJOR TRANSP x CIUDAD` (la joya: a
  quién enviar en cada ciudad), `NOVEDADES` (causas de no-entrega).
- **MAESTRO_CONTACTOS.xlsx** — hojas: `RESUMEN`, `CLIENTES` (dedup por teléfono, con %
  efectividad, productos, segmento y etiqueta WP), `LEADS NO CLIENTES (bot)` y
  `POSIBLES (msj masivo)` cuando existan las fuentes.

## Rentabilidad: la pregunta que el dueño hace ("soy rentable o no")
El motor separa cada orden por **estado de flujo de caja** — realizado (entregado = cobrado),
en camino (potencial, aún sin definir), en camino a devolución (en riesgo), devuelto (perdido:
se paga UN solo flete, el de devolución, que es la columna `COSTO DEVOLUCION FLETE` del informe
por pedido; igual o menor al de ida, nunca mayor), cancelado (no cuenta). Con eso arma el P&L:
`utilidad Dropi = ganancia realizada − costo de devoluciones`, y `utilidad neta = utilidad Dropi
− gasto de publicidad`. **El gasto de publicidad (Meta) NO está en los exports de Dropi**: es el
único dato externo. Ponlo en `_config_dropi.json` con la clave `gasto_publicidad` (del mismo
periodo que los informes), o pídelo/consúltalo. Si falta, el documento se entrega igual con todo
el lado Dropi y marca claro "falta gasto de publicidad para el veredicto" — nunca inventes ese
número, un veredicto de rentabilidad equivocado hace perder plata. Si el dueño tiene un tablero
de gasto (diario/semanal/quincenal), ese P&L por periodo es el destino natural para alimentar.

## Flujo de trabajo

### 1. Ubica y organiza los exports
Cada corte de Dropi baja 2 archivos: `ordenes_*.xlsx` (**por pedido**, 63 columnas) y
`ordenes_productos_*.xlsx` (**por producto**, 53 columnas). El motor **detecta el tipo por
las columnas**, no por el nombre, así que no es obligatorio renombrar. Pero para que ordenen
solos y para separar cuentas, la convención recomendada es:

```
<carpeta base>/
├── <Cuenta A>/                     # una subcarpeta por cuenta de Dropi (opcional)
│   ├── 2025-11 (Nov-Dic) - por pedido.xlsx
│   └── 2025-11 (Nov-Dic) - por producto.xlsx
├── <Cuenta B>/
│   └── ...
└── Analisis/                       # lo genera el motor
    └── _FUENTES/                   # insumos de enriquecimiento (opcional)
```

Reglas de nombrado (si el usuario quiere orden cronológico por nombre): prefijo numérico de
fecha **`YYYY-MM`** (mes de inicio del bimestre) + etiqueta legible, sin numeración correlativa.
Ej.: `2026-01 (Ene-Feb) - por pedido.xlsx`. Si hay **varias cuentas** (p. ej. el negocio cambió
de cuenta de Dropi), pon cada una en su subcarpeta; el motor las reporta por separado y
combinadas. Si los archivos están sueltos en la carpeta, se tratan como una sola cuenta.

Antes de analizar, si hay exports crudos `ordenes_*` sin ubicar: identifícalos (tipo + rango
de fechas leyendo la columna FECHA), renómbralos con la convención y ponlos en la cuenta que
corresponda. Si hay descargas repetidas (mismo periodo, mismos IDs), quédate con la más
completa/fresca y descarta la otra. Si un archivo no encaja (columnas raras, Dropi cambió el
formato o dudas de si es "por pedido" o "por producto"), lee `references/esquema-dropi.md`: trae
el mapa de columnas de ambos tipos y cómo el motor clasifica cada ESTATUS.

### 2. Configura lo local (opcional pero recomendado)
Crea `<carpeta base>/_config_dropi.json` para excluir data de prueba y fijar moneda:
```json
{ "test_phones": ["3001234567"], "test_name_keywords": ["PRUEBA","TEST"], "currency": "$" }
```
`test_phones` = números del dueño/tester que ensucian (sus pruebas del flujo COD). El motor
también excluye por defecto cualquier nombre con PRUEBA/TEST. Este archivo es **local del
cliente**: nunca lo metas en la skill ni pongas datos privados en el código.

### 3. Corre el motor
Usa la ruta absoluta del motor (el cwd en un chat real es la carpeta del cliente, no la de la skill):
```bash
python3 ~/.claude/skills/golden-dropi-analisis/scripts/motor_analisis_dropi.py "<ruta de la carpeta base>"
```
El argumento es la carpeta que contiene los exports (con o sin subcarpetas por cuenta); si se
omite, el motor usa la carpeta actual. Requiere **`openpyxl`** (obligatorio: sin él el motor no
arranca, `pip install openpyxl`, avisa claro si falta) y **`reportlab`** (`pip install reportlab`)
para generar **RESUMEN_EJECUTIVO.pdf** — el documento que se entrega primero. Si falta
`reportlab`, el motor NO falla: crea igual los 2 maestros Excel (el mismo contenido del PDF
queda en la hoja `RESUMEN EJECUTIVO`) y solo imprime un aviso. No dejes pasar ese aviso: instala
`reportlab` y vuelve a correr el motor para tener el PDF, o si de verdad no se puede instalar,
dile explícitamente al usuario que el resumen quedó solo en Excel. Imprime cuántas filas cargó
y las rutas de los archivos generados (2 o 3 según si hubo PDF).

### 4. Entrega el documento + hallazgos, no solo archivos
Lo primero que se entrega es **RESUMEN_EJECUTIVO.pdf** con el veredicto de rentabilidad (o, si
falta el gasto de publicidad, todo el lado Dropi y la petición de ese único dato). Luego abre el
`RESUMEN` y las hojas clave y dile al usuario, en lenguaje claro:
- **% de entrega global** y por cuenta, y ganancia neta vs. costo de devoluciones.
- **Peor y mejor transportadora** (la de menor % y mayor costo de devolución es la primera a
  recortar).
- **Ciudades/departamentos problemáticos** (candidatos a solo-anticipado).
- **Clientes VIP** (recurrentes confiables → remarketing) y **en riesgo** (mucha devolución →
  venderles solo con pago anticipado).
- **Evolución**: si el negocio sube, baja o cambió de cuenta.
Cierra con 2-3 **acciones concretas**, no con un volcado de tablas. Así se ve una entrega bien
hecha (cifras reales del cliente, no de este ejemplo):

> Analicé tus 17.775 órdenes (mar-2024 a jul-2026). Entregas **73,2%** global.
> - 🚚 **Interrapidísimo es tu fuga**: 68,4% de entrega y el mayor costo de devolución. Muévele
>   volumen a Envía/Veloces (~75%).
> - 👑 **440 clientes VIP** para remarketing; **4.344 en riesgo** → a esos, solo pago anticipado.
> - 📍 Nariño y Atlántico devuelven >32% → ahí también anticipado.
> Los dos maestros quedaron en `Analisis/`. Siguiente: quieres que arme la campaña de remarketing.

### Definición de terminado
La corrida está completa cuando: (1) el motor imprimió las rutas de los 2 maestros Excel sin
error, (2) **confirmaste si `RESUMEN_EJECUTIVO.pdf` se generó** — si el motor avisó "sin
'reportlab' no se generó el PDF", instala `reportlab` y vuelve a correr antes de dar por cerrado
(es el documento que se entrega primero; solo se omite si de verdad no se puede instalar, y en
ese caso se lo dices al usuario explícitamente), (3) abriste el `RESUMEN` de cada maestro y
confirmaste que el % de entrega y el nº de clientes son coherentes (no 0, no NaN), y (4)
entregaste los hallazgos + acciones al usuario. Si el % global se ve absurdo (p. ej. 100% o 0%),
sospecha de un teléfono/nombre de prueba sin excluir o de un solo estado presente: revisa
`_config_dropi.json` y la hoja `NOVEDADES` antes de dar por cerrado.

## Metodología (para poder explicarla)
- **% de entrega = ENTREGADO / (ENTREGADO + DEVOLUCIÓN)**. Se excluyen del denominador los
  `CANCELADO`/`RECHAZADO` (no llegaron a ruta) y los que siguen en tránsito, porque aún no son
  un resultado. Así el número refleja efectividad real de entrega, no ruido de estados abiertos.
- El **dinero y el conteo de órdenes** se toman del archivo **por pedido** (una fila = una
  orden) para no doblar montos; el **desempeño por producto y la base de clientes** se toman del
  **por producto** (que sí trae producto, cantidad y se puede agrupar por teléfono).
- **Teléfono** se normaliza a los últimos 10 dígitos para cruzar Dropi con WhatsApp y deduplicar.
- **Segmentos**: VIP = ≥3 pedidos y ≥70% efectividad; RIESGO = <50% efectividad; el resto BUENO/NEUTRO.

## Enriquecimiento opcional (si el cliente lo tiene)
En `<carpeta>/Analisis/_FUENTES/` el motor busca, sin fallar si no están:
- CSV de WhatsApp cuyo nombre empiece por `Etiqueta` o `Contacto` (columnas `phone`, `labels`,
  `saved_name`) → agrega la etiqueta de WhatsApp a cada cliente.
- CSV cuyo nombre empiece por `NO CLIENTE` (export de un bot tipo Chatea/ManyChat) → hoja de leads.
- Un `.xlsx` con una hoja que contenga "POSIBLE" → hoja de posibles para mensaje masivo.

## Cortes recurrentes
Dropi se suele cerrar por periodos (p. ej. bimestral). Cuando llegue un corte nuevo: ubica y
nombra los 2 crudos en su cuenta, y **vuelve a correr el motor** — regenera los 2 maestros
completos. No hay estado que mantener; el motor siempre lee todo desde cero.

## Estándar Golden
- Autonomía máxima: decide por defaults e informa; no preguntes lo que puedes resolver leyendo
  los archivos (tipo, fechas, duplicados). Pregunta solo lo que no está en la data (p. ej. si un
  teléfono con muchísimos pedidos es del dueño/prueba, o el costo real de un producto).
- Cero datos privados en la skill: teléfonos de prueba, rutas y monedas van en `_config_dropi.json`
  del cliente, nunca en el código.
- Puntuación en español sin signos de apertura (`¿`/`¡`): usa solo el de cierre.
- Esta skill es el ANÁLISIS agregado + base de datos. Para montar pauta con estos datos, pasa a
  golden-ads; para redactar los mensajes de rescate uno a uno, a golden-logistica.

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — analiza los informes de Dropi (COD/contra entrega) y genera 2 maestros Excel listos para decidir: MAESTRO_LOGISTICA (% de entrega global y por producto, transportadora, departamento y ciudad; mejor transportadora por ciudad; novedades; evolución en el tiempo) y MAESTRO_CONTACTOS (todos los clientes sin duplicados, con % de efectividad, segmento VIP/riesgo, etiquetas de WhatsApp, leads del bot y lista de posibles para mensaje masivo). Úsala SIEMPRE que el usuario quiera analizar sus ventas o entregas de Dropi, procesar los reportes/exports de Dropi, saber qué transportadora le entrega mejor, bajar devoluciones, sacar su base de clientes o segmentar para remarketing; o diga "analiza mis Dropi", "informe de entregas", "reporte de Dropi", "mejor transportadora", "cuánto entrego", "mi base de clientes de Dropi", "clientes VIP", "por qué me devuelven", "consolida mis órdenes", o suba archivos ordenes_*.xlsx / ordenes_productos_*.xlsx. Dispara aunque no diga "Dropi": basta con exports de órdenes COD por pedido (63 columnas) o por producto (53 columnas), o varias cuentas de Dropi que haya que unir. NO es para pauta (usa golden-ads) ni para rescatar novedades una por una (usa golden-logistica): esta skill es el ANÁLISIS agregado y la base de datos.

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-dropi-analisis
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-dropi-analisis
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-dropi-analisis`

Historial completo en `references/changelog.md`.
