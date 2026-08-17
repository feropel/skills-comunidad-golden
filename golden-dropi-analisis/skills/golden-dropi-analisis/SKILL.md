---
name: golden-dropi-analisis
description: >
  Golden Group — analiza los informes de Dropi (COD/contra entrega) y genera 2 maestros
  Excel listos para decidir: MAESTRO_LOGISTICA (% de entrega global y por producto,
  transportadora, departamento y ciudad; mejor transportadora por ciudad; novedades;
  evolución en el tiempo) y MAESTRO_CONTACTOS (todos los clientes sin duplicados, con %
  de efectividad, segmento VIP/riesgo, etiquetas de WhatsApp, leads del bot y lista de
  posibles para mensaje masivo). Úsala SIEMPRE que el usuario quiera analizar sus ventas
  o entregas de Dropi, procesar los reportes/exports de Dropi, saber qué transportadora
  le entrega mejor, bajar devoluciones, sacar su base de clientes o segmentar para
  remarketing; o diga "analiza mis Dropi", "informe de entregas", "reporte de Dropi",
  "mejor transportadora", "cuánto entrego", "mi base de clientes de Dropi", "clientes VIP",
  "por qué me devuelven", "consolida mis órdenes", o suba archivos ordenes_*.xlsx /
  ordenes_productos_*.xlsx. Dispara aunque no diga "Dropi": basta con exports de órdenes
  COD por pedido (63 columnas) o por producto (53 columnas), o varias cuentas de Dropi que
  haya que unir. NO es para pauta (usa golden-ads) ni para rescatar novedades una por una
  (usa golden-logistica): esta skill es el ANÁLISIS agregado y la base de datos.
---

# golden-dropi-analisis

<!-- skill v1.3 · fix auditoría 2026-07-25: (1) ZeroDivision resuelto cuando solo hay export "por producto" (tot = len(ped) or 1) — antes moría tras MAESTRO_LOGISTICA y no generaba CONTACTOS; (2) segmento() ya no marca RIESGO a clientes sin ninguna devolución (todo en tránsito = NEUTRO, no "mucha devolución"); (3) moneda con separador de miles LatAm (punto) vía helper cop(), sin colisionar con money() de parseo. -->
<!-- skill v1.4 · decisiones de FER 2026-07-25: (1) TRANSITO A DEVOLUCION se queda contando como DEVOLUCIÓN ("cien por ciento será una devolución" — si ya va en tránsito de vuelta, es pérdida); (2) red de seguridad de duplicados ACTIVA: dedup por (cuenta, ID) en por-pedido y (cuenta, ID, producto) en por-producto, quedándose con la aparición más reciente y AVISANDO cuántas unió (probado: 2 archivos iguales de 10 órdenes → 10 únicas + aviso) -->
<!-- skill v1.2 · + RESUMEN EJECUTIVO de rentabilidad (hoja + RESUMEN_EJECUTIVO.pdf): estado de flujo por orden + P&L + veredicto RENTABLE/NO. gasto_publicidad va en _config_dropi.json -->
<!-- skill v1.1 · auditada golden-skill-auditor 921→1000: puntero a esquema-dropi.md, comando con ruta absoluta, wp_name usado como fallback de nombre, import openpyxl elegante, definición de terminado + ejemplo de entrega -->

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
se paga el flete de ida y vuelta), cancelado (no cuenta). Con eso arma el P&L:
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
omite, el motor usa la carpeta actual. Requiere `openpyxl` (`pip install openpyxl` si falta; el
motor avisa claro si no está). Imprime cuántas filas cargó y las rutas de los 2 maestros.

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
La corrida está completa cuando: (1) el motor imprimió las 2 rutas sin error, (2) abriste el
`RESUMEN` de cada maestro y confirmaste que el % de entrega y el nº de clientes son coherentes
(no 0, no NaN), y (3) entregaste los hallazgos + acciones al usuario. Si el % global se ve
absurdo (p. ej. 100% o 0%), sospecha de un teléfono/nombre de prueba sin excluir o de un solo
estado presente: revisa `_config_dropi.json` y la hoja `NOVEDADES` antes de dar por cerrado.

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
