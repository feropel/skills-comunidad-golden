---
name: golden-chatea-pro-config-ventas-wp
description: Golden Group — Configura el asistente de VENTAS POR WHATSAPP de Chatea Pro (la "Experta en ventas por WhatsApp", el bot/agente de ventas) de punta a punta con los Bot Fields JSON NATIVOS listos para COPIAR Y PEGAR — 2 campos de configuración general (Dropi, validaciones de orden, Producto en Segundos con prompt maestro, notificaciones, comportamiento de la IA), 1 campo por producto ([Producto Ventas Wp] N: información, embudo con multimedia, prompt de venta, voz, recordatorios, remarketing, activadores, pixel) y su entrada en el Disparador de productos Extendido — con los prompts del motor afinados y validadores de límites reales (500000 por campo en tipo LONG JSON, con verificación de truncada silenciosa). Úsala SIEMPRE que el usuario quiera montar, configurar o replicar el asistente/agente/bot de ventas de WhatsApp de Chatea Pro para una tienda o cliente, "configurar ventas whatsapp", "montar el asistente de ventas", "el JSON del asistente de ventas", "genera los bot fields de ventas", "configura la experta en ventas", o cargar/validar un producto nuevo en ese asistente. La promo/prompt de venta de cada producto se genera con golden-chatea-pro-prompt-ventas; para comentarios, logístico o carritos usa sus skills hermanas; para los 4 a la vez, golden-chatea-pro-full-configuracion.
---

# Golden · Chatea Pro — Asistente de Ventas WhatsApp

<!-- skill v3.3 · 2026-08-06 · SINCRONIZACIÓN (golden-skill-auditor): changelog al día con el trabajo de otros chats. Tope real = TIPO de campo, LONG JSON = 500000 (medido por API 2026-07-25/29, truncada silenciosa) — todo campo nuevo se crea LONG JSON; carga por API con push_config.py (read→backup→push→releer y comparar). FIX validador: prompt_libre >12000 avisa (no rechaza) porque por Bot Field es legítimo (un producto real=14125) y la UI v2 lo corta+sobrescribe. Upsells DESBLOQUEADOS (2026-07-12): límites titulo/desc/botón validados; si activos, el prompt no hace pitch propio. Gotcha par Disparador/Disparador Extendido (array viejo vacío = flujo lee vacío). division.limite=2 (v3.2). -->
<!-- skill v3.2 · 2026-07-12 · prompts del motor endurecidos tras test de campo (3 prioridades, memoria del pedido, única confirmación, URLs blindadas, sin 2 preguntas/mensaje); division.limite 3→2 (con 3 la IA responde en ráfagas robot; 2 cubre imagen-URL + texto) -->
<!-- skill v3.1 · 2026-07-09 · PRODUCTOS también nativos: 1 Bot Field JSON por producto ([Producto Ventas Wp] N) + entrada en el índice "[Ventas Wp] Disparador de productos Extendido" (Long JSON); template-botfield-producto.json con esquema real (recordatorios=prompt-instrucción EVENTO/35 palabras, remarketing=rol por fase, keyW/idAd=7 slots por comas), valida_producto.py con cruce producto↔registro y copia _LIMPIO; interruptores Boolean del workspace documentados -->
<!-- skill v3.0 · 2026-07-09 · FORMATO NATIVO descubierto y verificado: la config general vive en 2 Bot Fields JSON (<20000 c/u, carpeta del agente); templates con el esquema real (claves intocables), build_config.py emite los 2 campos copy-paste (estructura IDÉNTICA a producción); prompts del motor pulidos ≤ límites de la UI -->
<!-- skill v2.1 · 2026-07-09 · auditoría golden-skill-auditor 838→990: sin ¿¡ en prompts horneados, limites.json fuente única, casos borde + checklist -->
<!-- skill v2.0 · 2026-07-08 · reconstruida sobre el mapa levantado en vivo de la UI de Entrenar -->

Configura la **Experta en ventas por WhatsApp** de un workspace de Chatea Pro.

> **CÓMO FUNCIONA DE VERDAD (verificado 2026-07-09):** la configuración general del
> asistente vive en **2 Bot Fields de tipo JSON** — se pega el JSON completo y listo.
> Ruta: Chatea Pro → **Bot Fields** → carpeta del agente de ventas (ej. "Agente de Ventas
> WhatsApp con IA") → click al campo → modal "Edit Bot Field" → pegar en **Valor**.
> Límite: depende del **TIPO** de campo, no de la plataforma. Tipo **JSON** = 20000. Tipo
> **LONG JSON** = **500000** (25x, medido por API el 2026-07-25). **Crea los campos como LONG
> JSON.** Y ojo: pasarse del tope **no da error** — la API responde `200 ok` y guarda el texto
> CORTADO, así que después de escribir hay que releer y comparar (`push_config.py` ya lo hace).
> Las claves del JSON las lee el flujo
> del bot por nombre → **NUNCA renombrar claves**; convenciones nativas: "si"/"no" en
> minúscula, país en minúscula, números como string, `activar: true` boolean.
> El esquema de referencia real vive en `PROYECTOS/CHATEA-PRO-VENTAS-WP/bot-fields-reales/`;
> el mapa de la UI de Entrenar (vía manual alterna) en `MAPA-ASISTENTE-VENTAS-WP.md`.

**Regla de Chatea Pro:** 1 workspace = 1 país.

## Las piezas

**Configuración general** (1 vez por tienda) → 2 Bot Fields:
- Campo `[Ventas Wp] Configuracion general` → `assets/template-botfield-1-configuracion.json`
  (Dropi, validaciones de orden, Producto en Segundos con prompt maestro, notificaciones)
- Campo `[Ventas Wp] Configuracion general 2` → `assets/template-botfield-2-comportamiento.json`
  (comportamiento de la IA: división de mensajes, rol, restricciones, análisis de palabra clave)

**Producto** (se repite por producto) → 2 piezas SIEMPRE juntas:
- Su Bot Field `[Producto Ventas Wp] N` → `assets/template-botfield-producto.json`
  (información, embudo de ventas, prompt libre, voz, recordatorios, remarketing,
  activadores, meta conversión, upsells)
- Su entrada en el índice `[Ventas Wp] Disparador de productos Extendido` (Long JSON,
  <500.000, UNO por workspace) → `assets/template-registro-disparador.json`. Se AÑADE al
  array existente sin borrar los demás productos.

**Interruptores del workspace** (Bot Fields Boolean, se dejan en su default salvo pedido):
Respuesta Múltiple=true · Oficina=false · Pedido programado=true · Intento de
cancelación=true · Solo Con Recaudo=true · Solo Sin Recaudo=false · Solo Pendiente
confirmación=false · Desactivar Skill Datos=false · Desactivar asignación=false.

## Prompts del motor (fijos, horneados en `assets/prompts/`)

Pulidos y genéricos — NUNCA se recortan ni se rehacen a mano. Se mantienen dentro de los
límites de la UI de Entrenar para que sirvan por las dos vías:

| Archivo | Va en | Límite UI |
|---|---|---|
| `assets/prompts/rol-general.txt` | campo 2 → `comportamiento_ia.rol` | 2000 |
| `assets/prompts/restricciones.txt` | campo 2 → `comportamiento_ia.restricciones` | 2000 |
| `assets/prompts/analisis-palabra-clave.txt` | campo 2 → `analizar_palabra.prompt` (lleva `{{URL_TIENDA}}`) | 2000 |
| `assets/prompts/reglas-estructura-producto.txt` | campo 1 → `producto_segundos.prompt_datos` | 4000 |
| `assets/prompts/notificacion-venta-realizada.txt` | campo 1 → `notificaciones...mensaje` (variables `{nombre_producto}` etc.) | 400 |

## Intake (pregunta solo lo que falte; el resto por defecto e INFORMA)

1. **País** del workspace (ej: colombia).
2. **Moneda** (ej: COP) y **flete máximo** para validar la orden (ej: 23000).
3. **WhatsApp** que recibe las notificaciones de venta.
4. **URL de la tienda** (para redirigir productos no configurados).
5. **Dropi** sí/no (default sí).
6. (Opcional) **Prompt maestro** de Producto en Segundos: el prompt de venta GENERAL del
   negocio (≤13000) que usa "Crea tu asistente en segundos". Si no existe, pídelo a
   `golden-chatea-pro-prompt-ventas` como prompt de negocio (catálogo completo).

Defaults sin preguntar: subida automática del pedido sí · validar entregas sí (mín 3
órdenes, 60%) · validar flete sí · división "varios" / **máx 2 mensajes** (con 3 la IA
responde en ráfagas de 3 burbujas que se sienten robot; 2 cubre el caso legítimo de
imagen-URL + texto) · análisis de palabra clave activado · notificación de Venta Realizada
activa sin plantilla Meta.

### Generar los 2 Bot Fields

```bash
python3 scripts/build_config.py \
  --pais "colombia" --moneda "COP" --flete-max "23000" \
  --whatsapp-notif "+57 3001234567" \
  --url-tienda "https://mitienda.co" \
  --prompt-maestro /ruta/prompt_maestro.txt \
  --out-prefix /ruta/<NEGOCIO>
```

Produce `<NEGOCIO>_BOTFIELD_1.json` y `<NEGOCIO>_BOTFIELD_2.json` (sin claves _meta),
inyecta los prompts fijos, reemplaza `{{URL_TIENDA}}` y valida contra `assets/limites.json`:
cada campo bajo el tope de su tipo (LONG JSON 500000) y cada prompt dentro de su límite de UI (exit 1 si algo excede — nunca
recortes los prompts fijos; acorta el prompt maestro o lo variable). La entrega al usuario
es: los 2 archivos + la instrucción de en cuál Bot Field va cada uno.

### Carga automática por API (opcional, recomendado para instalaciones en serie)

Chatea Pro es whitelabel de **UChat**: su API (base `https://chateapro.app/api`, Swagger en
`/api#/`, auth Bearer) permite **escribir los Bot Fields directamente**, sin pegar a mano — la
skill se vuelve una máquina de instalaciones para muchos clientes/países. Endpoints:
`GET /flow/bot-fields?name=` · `PUT /flow/set-bot-fields-by-name` con
`{ "data":[ {"name","value"}, ... ] }`.

`scripts/push_config.py` hace read → backup → push (dry-run por defecto; escribe solo con
`--confirm`). Token del workspace del cliente por `--token`, env `CHATEAPRO_TOKEN` o
`~/.chatea_pro_token`. Flujo seguro SIEMPRE: (1) `read` los 2 campos; (2) `backup` del estado
actual; (3) mostrar qué cambia y, con OK del usuario, `push --confirm`.

```bash
CHATEAPRO_TOKEN="<TOKEN_DEL_CLIENTE>" python3 scripts/push_config.py push \
  "[Ventas Wp] Configuracion general=/ruta/<NEGOCIO>_BOTFIELD_1.json" \
  "[Ventas Wp] Configuracion general 2=/ruta/<NEGOCIO>_BOTFIELD_2.json" \
  --confirm
```

**Gotchas verificados en vivo (2026-07-09):** (1) el token debe estar **atado al bot/flujo**
del asistente o la API responde 404 `"Flow not found"`; (2) Cloudflare bloquea urllib sin
User-Agent (error 1010) — `call()` ya manda UA de navegador, así funciona desde Bash directo;
(3) los pares `nombre=archivo` van ANTES de `--confirm`.

**Token = dato sensible**: no es de pagos pero da acceso a datos de suscriptores del cliente y
puede enviar mensajes. Scope mínimo ("Gestionar el flujo"), no hornearlo en la skill ni en git,
rotar/borrar al terminar. Un `push` a un workspace en vivo SIEMPRE se confirma antes de escribir.

## Producto (Bot Field por producto + registro)

División de responsabilidades: **esta skill pone la ESTRUCTURA** (JSON nativo, límites,
validación); **`golden-chatea-pro-prompt-ventas` pone los TEXTOS** (prompt de venta,
mensaje inicial, pregunta de entrada, recordatorios, prompts de remarketing).

1. Copia `assets/template-botfield-producto.json` y llena los `{{PLACEHOLDERS}}`:
   - **Datos duros** (preguntar, nunca inventar): nombre, precio (solo dígitos; repetirlo
     dentro del prompt: la IA lo cita desde ahí), ID Dropi (va en `id` Y en `id_dropi`),
     SIMPLE o VARIABLE, URL de imagen de portada, URLs de multimedia, palabra clave,
     IDs de anuncio si hay, API key + ID de voz si usa voz (si no: `habilitar: "no"` y
     vacíos).
   - **Textos de venta** (de `golden-chatea-pro-prompt-ventas`): OJO con el formato nativo —
     los recordatorios son PROMPT-instrucción ("EVENTO: el usuario no respondió...
     MÍNIMO 35 PALABRAS." + ejemplo), y el remarketing son ROLES por fase (1 = reactivación
     suave, 2 = último llamado con urgencia), no mensajes literales.
2. Llena `assets/template-registro-disparador.json` con el MISMO nombre, palabra clave e
   IDs de anuncio, y el `name` del campo (`[Producto Ventas Wp] N` — mira en Bot Fields el
   último N usado y suma 1).
3. **Valida SIEMPRE antes de entregar** (genera además la copia `_LIMPIO.json` sin _meta,
   lista para pegar):
   ```bash
   python3 scripts/valida_producto.py --in /ruta/<producto>_BOTFIELD.json \
     --registro /ruta/<producto>_REGISTRO.json
   ```

Defaults de producto: voz estabilidad 0.3 / similaridad 0.7 / estilo 0.5 / velocidad 1 /
speaker_boost false / responder audio con audio sí / máx 5 audios / probabilidad 100 ·
recordatorios 30 min y 2 horas · remarketing 3 horas y 23 horas · rango 06:00–22:00 ·
meta_conversion habilitado por defecto · **upsells desactivados por defecto** (el template
los deja `activo:"no"`, pero YA NO están bloqueados por plan — se activaron el 2026-07-12).

**Upsells nativos** (opcionales, 2 tarjetas que Chatea muestra tras "compra realizada"):
título ≤80, descripción ≤80, botón ≤20, precio, id_dropi. Si se activan, el **prompt del
producto NO hace su propio pitch de upsell** (se pisarían y el cliente vería doble
ofrecimiento): el prompt solo procesa la aceptación y cuadra el total. El texto de las
tarjetas lo produce `golden-chatea-pro-prompt-ventas`; el validador chequea sus límites.

## Casos borde (decide por convención e informa)

- **Negocio sin Dropi** → `--dropi no` (apaga también la subida automática); el flete no
  se pregunta pero el JSON conserva las claves (el flujo las espera).
- **Sin voz ElevenLabs** → `usar_voz: No` y se omiten API key, ID y parámetros.
- **Sin plantillas Meta aprobadas** → remarketing "No enviar plantilla"; solo recordatorios
  (ventana 24h) y avisar que el fuera-de-ventana queda apagado hasta aprobar plantillas.
- **Un texto excede su límite** → regenerar esa pieza con `golden-chatea-pro-prompt-ventas`
  en versión corta; los prompts fijos no se tocan.
- **Falta la skill hermana** → escribir los textos a mano respetando límites e informar.
- **La plataforma no coincide con este mapa** → Chatea Pro cambia sin aviso: re-verificar
  en vivo y actualizar `assets/limites.json` + la referencia del proyecto.
- **Nombres de los Bot Fields distintos** → si el workspace del cliente usa otra plantilla
  de bot, ubicar los campos JSON equivalentes en Bot Fields y pegar ahí (el contenido es
  el mismo); si no existen, crearlos con esos nombres dentro de la carpeta del agente.
- **Producto nuevo en workspace ajeno** → antes de asignar el `N` del campo, revisar en
  Bot Fields qué números ya existen; el registro del Disparador se EDITA añadiendo la
  entrada, jamás pegando un array que borre los productos anteriores.
- **Par `Disparador` / `Disparador Extendido` (gotcha crítico)** → Chatea migró: el campo
  viejo `[Ventas Wp] Disparador de productos` (tipo JSON/array) quedó **VACÍO** y el vivo es
  `[Ventas Wp] Disparador de productos Extendido` (LONG JSON). Un flujo que siga leyendo el
  array viejo lee vacío. Al auditar o instalar, escribir SIEMPRE en el campo con "Extendido"
  y verificar cuál lee el flujo; buscar siempre el par `X` / `X extendido`.
- **Prompt de producto >12000** → va SOLO por Bot Field (LONG JSON). La pantalla "Prompt del
  producto" de la UI v2 lo corta a 12000 y su "Guardar asistente" sobrescribe con la versión
  cortada: para esos productos, tratar esa pantalla como solo-lectura. El validador avisa.
- **Truncada silenciosa al cargar por API** → pasarse del tope del campo devuelve `200 ok`
  con el texto CORTADO; `push_config.py` relee y compara longitud. Nunca dar por buena una
  carga sin ver el "todo guardado íntegro".
- **Pendiente con dueño**: otros eventos del dropdown de notificaciones (falta pantallazo
  del dropdown abierto).

## Terminado = checklist

- [ ] `build_config.py` con exit 0 → 2 Bot Fields bajo el tope de su tipo y prompts dentro de límites.
- [ ] Campos creados como **LONG JSON** (no JSON) y `push_config.py` cerrando con "todo guardado íntegro".
- [ ] Por cada producto: `valida_producto.py --registro` con exit 0, sin `{{placeholders}}`,
  y entregada la copia `_LIMPIO.json`.
- [ ] Datos reales confirmados por el usuario (precio, WhatsApp, palabra clave, ID Dropi).
- [ ] Entregados los archivos con la instrucción exacta de dónde se pega cada uno:
  config general → campos 1 y 2 · producto → su campo `[Producto Ventas Wp] N` · registro →
  AÑADIR al Disparador de productos Extendido.
- [ ] Informados los defaults aplicados y los casos borde activados.

## Conexiones (skills hermanas)
- 🎯 Prompt/promo por producto y prompt maestro → `golden-chatea-pro-prompt-ventas`
- 💬 Asistente de comentarios → `golden-chatea-pro-config-comentarios`
- 📦 Asistente logístico → `golden-chatea-pro-config-logistico`
- 🔁 Asistente de carritos → `golden-chatea-pro-config-carritos`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales de un negocio (números de WhatsApp, cuentas de pago, API keys,
IDs de voz, URLs, precios, marcas) en los archivos de la skill: se preguntan en cada uso y
viven solo en los JSON entregados. Los prompts de `assets/prompts/` son genéricos por
diseño; los ejemplos reales viven fuera de la skill, en la carpeta del proyecto.
