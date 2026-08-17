# Reglas de oro: copy, legal y errores conocidos

Conocimiento acumulado (ex-`golden-shopify`). Esto es lo que más rompe páginas o
mata conversión. Léelo antes de escribir copy o entregar.

## Regla 0-C — COHERENCIA DE PRODUCTO (el copy tiene que describir ESTE producto)
Aprendido auditando verrugas como cliente (870/1000 por incoherencias, no por estructura).
- **La FORMA del producto manda en el verbo.** Spray → "rocía"; gotero → "aplica una gota"; crema →
  "aplica una capa"; parche → "coloca". NUNCA quede "aplica una gota" en un spray. Revisa cómo-actúa,
  FAQ, timeline y es-para-ti: todos deben usar el MISMO verbo de aplicación.
- **Lidera con la USP / ingrediente estrella.** Si el producto tiene un activo diferenciador (veneno de
  abeja, ácido X, colágeno…), es el protagonista del mecanismo (hero + cómo-actúa + escalera), no un
  genérico "ingredientes naturales". El diferenciador es lo que vende.
- **Coherencia de alcance.** Lo que el producto NO trata (ej. lunares/rostro) no puede aparecer como
  beneficio en tickers/hero. Si es-para-ti dice "NO es para lunares", el ticker no dice "adiós lunares".
- **Intro/ignition y hero badge = copy del producto, cero fósil.** Prohibido "POTENCIA DESBLOQUEADA",
  "⚡ energía", o un acento de color huérfano (ej. cian `#0bd4fd`) heredado del demo. Usar var(--brand-*).
- **Un solo número de WhatsApp REAL** en config + botón flotante (nunca `[WHATSAPP-CON-CODIGO-PAIS]`).
- **Claims legales:** no afirmar registro/aval (INVIMA, etc.) si no es real. Si no lo necesita, enfoque
  POSITIVO ("por sus características no requiere registro sanitario"), nunca "no tiene registro".

## Regla 0-D — NO repetir el mismo claim en bloques ADYACENTES (G3.17)
Cada bloque tiene que **ganarse su lugar diciendo algo NUEVO**; si dos bloques pegados repiten el mismo
claim, el segundo sobra y la página se siente rellena.
- **No repitas el mismo mensaje en bloques adyacentes.** Ej.: los sellos ARRIBA del precio = producto
  natural / origen / entrega 48h; la garantía DEBAJO del botón = pago seguro + producto sellado; el cierre
  = invitación emocional (no volver a listar logística). Cada uno aporta un ángulo distinto.
- **Los términos NÚCLEO sí pueden repetirse a lo largo del embudo** (envío gratis, contra entrega): pero
  solo en **puntos de decisión** (hero, tras-mecanismo, cierre, sticky), **no pegados** en bloques vecinos.
- **Contraste de emoji vs su fondo** (ver también `estandares-liquid.md`): ningún emoji del mismo color que
  el fondo donde va (💚 sobre CTA verde se pierde) → elige uno contrastante. Regla para toda la página.

### Reseñas de ejemplo con caras (placeholder, opcional)
Las fotos de las **reseñas de ejemplo** se pueden generar con IA (retratos tipo selfie) — van aparte
del brief de infografías de `imagen-arena` — como **placeholders reemplazables**. Márcalas siempre como EJEMPLO (nunca como reseña real
verificada) para que el usuario las sustituya por clientes reales cuando los tenga.

## Regla 0-A — ARQUITECTURA DE CONVERSIÓN (el orden manda, PRIORIDAD MÁXIMA)
Aprendido rediseñando la página real de verrugas (se veía "fea, no convierte"). Una product-page
que vende NO es una lista de bloques bonitos: es un **embudo con ritmo**. Orden canónico (G3.6):

1. **Ticker** (micro-confianza: envío gratis · contra entrega)
2. **HERO / main** (galería + promesa + oferta + countdown + precio + **CTA#1** + garantía + descripción)
3. **Ticker DESPUÉS de la descripción** (respiro visual + urgencia) ← pedido del cliente, ahora canónico
4. **PROBLEMA** — "Te suena?" (el cliente se reconoce)   ┐
5. **AGITAR** — "Ya lo intentaste" (demoler alternativas)  ┘ estructura PAS (Problema-Agitar-Solución)
6. **SOLUCIÓN** — "Cómo actúa" (el mecanismo, el "ajá")
7. **CTA#2** — justo cuando entiende que funciona (pico de convicción)
8. **BENEFICIOS** — escalera "por qué miles cambiaron"
9. **VISIÓN emocional** — "imagina tu piel/vida" full-bleed + CTA#3 (future-pacing)
10. **PRUEBA SOCIAL** — reseñas
11. **EXPECTATIVAS** — "qué esperar paso a paso" (baja la ansiedad de "me servirá?")
12. **CALIFICACIÓN** — "es para ti" (auto-selección → compromiso + menos devoluciones)
13. **COMPARACIÓN** — "por qué elegir"
14. **FAQ** — últimas objeciones
15. **CIERRE emocional** — manifiesto + **CTA#4 final**
16. **Disclaimer** legal (ligero)

Principios de neuroventa que NO se rompen:
- **Cadencia de CTA:** una oportunidad de compra cada 2-3 secciones (nunca 6 pantallas sin botón).
  Gates: hero → tras-mecanismo → tras-beneficios → cierre. + sticky siempre visible + WhatsApp flota.
- **Ritmo visual:** NUNCA dos bloques "grandotes/oscuros/full-bleed" seguidos (cansa, se ve feo).
  Intercalar denso/aireado, claro/oscuro. El **ticker es un respiro** entre secciones pesadas.
- **PAS antes de vender:** primero duele (problema+agitar), luego alivia (solución). Vender antes de
  agitar el dolor = no convierte.
- **Quita el ruido:** autoridad con cifras inventadas (placeholder) se APAGA — prueba social falsa
  destruye confianza. Related-products y ficha técnica vacía: fuera por defecto.
- **Termina en emoción + CTA**, no en dos bloques dramáticos apilados ni en legal.

## Regla 0-B — Landing bloqueada + cero copy demo (COD, PRIORIDAD MÁXIMA)
Aprendido en la prueba "todo activado" de verrugas.
- **LANDING BLOQUEADA por defecto.** Toda página COD lleva el bloque `custom_liquid_lock`
  (candado): oculta header + announcement + footer del tema con `display:none` para que el
  cliente NO pueda irse al home. NUNCA se logra ocultando el header desde el editor de Shopify
  (eso saca la sección del DOM y en Shrine mata el JS que inicializa las secciones animadas →
  "desaparece todo"). Ver `componentes/sec-lock-landing.liquid`. El usuario lo abre con `LOCK=false`.
- **Relacionados APAGADOS por defecto** (`related-products` disabled:true). Solo se muestran las
  secciones que diseñamos para ESE producto. El usuario los desoculta manual si quiere.
- **CERO copy demo fósil.** Prohibido que sobreviva texto del PRODUCTO DEMO/MARCA DEMO en una
  página real: `energía`, `vitalidad`, `Borojó`, `Guaraná`, `Chontaduro`, `tapa-vaso`, `máxima energía`, `la bebes`,
  `perfume` (si no aplica). El texto del **ticker** y del **FAQ** se reescribe SIEMPRE por producto
  — no son estáticos heredados. Si el producto no es de energía, no puede decir "energía".

## Regla 0 — La instrucción del usuario manda + armonía (PRIORIDAD MÁXIMA)
Aprendido en un sérum facial (ejemplo) (una tienda de pruebas): convertí una página verde coherente en
verde + naranja + rojo aplicando reglas genéricas al pie de la letra → se vio "horrible".
- **La instrucción explícita de color del usuario PISA toda regla genérica.** Si pidió
  "adapta todo al color del producto", el CTA NO se vuelve naranja/rojo: destaca con un
  tono **más oscuro/brillante del MISMO color** + sombra + tamaño. No importes un matiz
  que el usuario no pidió.
- **Máximo 2 colores fuertes en pantalla y UN solo color de acción (el CTA).** Prohibido
  apilar verde + naranja + rojo. Si ya hay un acento de urgencia (countdown), la caja de
  oferta y el badge de precio NO van de otro color distinto — se repite ESE acento o se
  dejan neutros/del color de marca.
- **Productos naturales / botánicos / salud:** paleta casi monocromática del color del
  producto + a lo sumo UN acento cálido pequeño. Nada de "alarma roja" sobre un producto calmado.
- **Mira la página RENDERIZADA (screenshot) antes de decir que está lista.** Nunca declarar
  "100/100" solo con el JSON validado: el "test de 1 vistazo" exige VERLA con los ojos.

## Las 12 reglas de oro (NUNCA fallar aquí)
1. **Tema correcto:** `color_scheme` debe coincidir → Shrine = `background-1`,
   Dawn/Sense = `scheme-1`. Valor equivocado = página rota / esquema sin color.
2. **Releasit click:** los botones de compra disparan
   `document.querySelector("#_rsi-buy-now-button-overwrite, ._rsi-buy-now-button").click()`.
3. **Ocultar Releasit flotante** SOLO con
   `#_rsi-buy-now-button-floating, ._rsi-buy-now-button-product-floating`.
   NUNCA `._rsi-buy-now-button` a secas (rompe el formulario interno).
4. **Bloque Releasit nativo** va `"disabled": true` — presente pero oculto. No eliminarlo.
5. **Botones secundarios** (sticky) hacen clic en `#custom-releasit-btn`, no en Releasit directo.
6. **Garantía basada en PROCESO**, no en resultados. Nunca prometer devolución de
   dinero ni "revisa el pedido antes de pagar" (las transportadoras en Colombia no
   permiten abrir paquetes antes de pagar).
7. **Copy de perfumes / dropshipping:** NO decir "original" ni "réplica". Hablar de
   "sellado", "presentación premium", "calidad", "inspirado en" (estándar de industria).
8. **Espaciado antes de emojis:** espacio normal + NBSP (carácter 160), no dobles espacios.
9. **`description` en featured-collection (Dawn)** debe ir envuelto en `<p>...</p>` (rich text).
10. **Reveal-on-scroll:** no incluir elementos arriba del fold (causa flash al cargar).
11. **Botones en móvil:** `min-height` (no `height`), `text-align:center`, `width:100%`, texto corto.
12. **Fuentes vía `@import`** en el bloque propuesta (primero en cargar):
    `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');`

## Copy para contra entrega (Colombia)

### Garantía: PROCESO, no resultados
- USAR: "Compra 100% Segura", "Pagas al recibir", "Producto sellado y en perfecto estado".
- NUNCA: "garantía de satisfacción", "te devolvemos tu dinero", "30 días de garantía".

### Texto por MODE de pago (default: `ambos`)
| MODE | Texto |
|---|---|
| `contraentrega` | **Pagas al recibir**, en la puerta de tu casa — sin transferencias ni pagos por adelantado. Producto sellado y en perfecto estado. |
| `anticipado` | **Pago 100% seguro** con tarjetas, PSE o transferencia. Producto sellado, entregado en perfecto estado. |
| `ambos` | Elige cómo pagar: **contra entrega** al recibir o **pago anticipado** seguro online. Producto sellado y en perfecto estado. |

### Perfumes / dropshipping (CRÍTICO)
- **NUNCA:** "original", "réplica", "imitación", "copia", "versión".
- **SÍ:** "sellado", "presentación premium", "calidad premium", "inspirado en grandes
  diseñadores", "fragancia/esencia/aroma" (sin marca), "larga duración", "alta fijación".
- Ejemplo FAQ: ❌ "Es original?" → ✅ "Cómo viene presentado? Llega en su empaque
  sellado y en perfecto estado, presentación elegante lista para estrenar o regalar."

### Expectativas realistas (reduce devoluciones)
Describe el producto por lo que ES. Ej: Producto Demo = fibra cosmética que **cubre**, NO
tratamiento de crecimiento. La precisión baja las devoluciones por malentendido.

### Copy emocional (deseo, no ficha técnica)
- ❌ "Fijación duradera. Aroma sofisticado." → ✅ "Para la mujer que no pasa desapercibida."
- ❌ "Notas de salida: bergamota…" → ✅ "El primer encuentro: bergamota…"
- Manifiesto (3 escalones + cierre):
  > Hay mujeres que pasan. / Hay mujeres que se notan. / Y hay mujeres que dejan
  > huella. / **Este perfume es para las terceras.**

### Tono
- Español de Colombia, cercano y directo. Mercado ~80% móvil.
- Botones con verbo + emoji: "LO QUIERO AHORA ✨", "PEDIR AHORA ✨".
- Urgencia REAL: countdown evergreen 15 min en `localStorage` (se reinicia solo).
- Prueba social en tickers: "+100 mil clientes", "+1 millón de productos vendidos".

## Copy avanzado — absorbido de la auditoría de la tienda real (v1.19)

### El ÁNGULO manda sobre la categoría (presets de tono)
El mismo esqueleto puede vestirse de tonos distintos según a quién le hablas. Elige el
registro ANTES de escribir y mantenlo en copy + emojis + CTA:
- **Lujo/estatus** (perfumes, gadgets premium tipo gadget perfumador): "experiencia", "elegancia",
  sensorial, aspiracional. Emojis sobrios (✨💎🖤).
- **DIY/ahorro** (herramientas, fix-it tipo cubre-rayones): empoderamiento, "hazlo tú mismo",
  contraste de costo vs alternativa cara. Emojis funcionales (🔧🛠️✅).
- **Belleza/femenino** (cosmética, espejo espejo LED): "luce perfecta", "femenino", deseo
  estético + identidad. Emojis 👑💄✨. (Nota: un gadget puede venderse con tono belleza si
  su comprador es ella — el ángulo manda, no la categoría real.)
- **Salud/técnico-cosmético** (skincare, suplementos): ingrediente con nombre + beneficio,
  mecanismo "clínico-light". Sobrio, sin gritar.

### Reframe de categoría (sube valor percibido)
Reencuadra el producto a una categoría superior para justificar precio:
"No es un ambientador, es un sistema de aromatización." / "No es solo un espejo, es un
accesorio de lujo." Técnica de una línea, va en la propuesta o en un panel de la escalera.

### Eyebrow / kicker de beneficio encima del título
Antes del nombre del producto, una línea-gancho con el BENEFICIO en mayúsculas:
"EFECTO PIEL PERFECTA AL INSTANTE", "ENERGÍA LIMPIA SIN CAÍDAS", "ADIÓS A LA CALVICIE".
Frame el resultado antes de que el cliente lea qué es. (En `dawn-titulo.liquid` / hero.)

### CTA en primera persona + doble CTA
- El CTA convierte más en **voz del cliente**: "QUIERO MI [PRODUCTO] 🔥" > "VER OFERTAS".
  Ya es el default del botón; personalízalo SIEMPRE al nombre corto del producto.
- **Doble CTA:** repite el botón de compra a media página (tras la escalera/descripción)
  con copy "PEDIR AHORA 🔥", además del CTA del hero y el sticky. Las páginas ganadoras
  de la tienda lo hacen; las crudas no.

### Verticales sensibles — copy que vende SIN riesgo legal (Meta/INVIMA)
- **Íntimo** (spray íntimo tipo Le'côterra): tono **cómplice/humor**, no clínico ni
  vergonzante. Encuadre "cuidado personal premium". CERO claim médico: "frescura",
  "control de olor", "fórmula natural", "uso diario". Recurso: GIFs de reacción para
  desdramatizar el problema sin señalar a la clienta.
- **Antiedad** (reafirmante tipo sérum facial): "clínico-light" sin prometer cura: "tecnología
  clínica", "eficacia clínica y origen natural", "sin procedimientos invasivos".
  Reencuadre amable del dolor: "no ignores tu cuello" en vez de "tienes el cuello feo".
- **Hongos / antifúngico** (reparador de uñas tipo un sérum facial (ejemplo)): ⚠️ "antifúngico/
  antihongos" es el claim MÁS riesgoso (rechazo de Meta + problema INVIMA). Genera por
  DEFECTO la versión **cosmética**: "repara, fortalece, mejora color y textura", apóyate
  en el ingrediente natural (jengibre). Deja el claim fuerte solo si el usuario lo decide
  conscientemente, avisándole del riesgo.

## Tabla de errores conocidos
| Síntoma | Causa | Solución |
|---|---|---|
| Página no carga / esquema roto (Shrine) | `color_scheme: "scheme-1"` (valor Dawn) | Usar `"background-1"` |
| `'horizontal-ticker' no hace referencia a una sección existente` (Dawn) | Dawn no tiene esa sección | Reemplazar con `custom-liquid` + marquee CSS |
| `El parámetro "description" no es válido` (Dawn) | `featured-collection.description` sin `<p>` | `"description": "<p>texto</p>"` |
| `JSONDecodeError: Extra data` | Notas escritas DESPUÉS del `}` final | Dejar solo JSON válido |
| Formulario Releasit sin botones | `._rsi-buy-now-button{display:none}` demasiado amplio | Solo `#_rsi-buy-now-button-floating, ._rsi-buy-now-button-product-floating` |
| Sticky pide doble clic / salta | Sticky busca el botón Releasit directo | Que clique `#custom-releasit-btn` |
| Botón cuadrado/descentrado en móvil | `height` fija + texto largo | `min-height`, `text-align:center`, `width:100%`, texto corto |
| Emojis pegados al texto | Dobles espacios colapsan en HTML | Espacio normal + NBSP (160) |
| MP4 rechazado en descripción | El subidor solo acepta imágenes | Subir a Config→Archivos y embeber `<video>`, o GIF optimizado |
| JSON inválido al pegar | HTML sin escapar en `custom_liquid` | `\n` saltos, `\"` comillas (`json.dumps` lo hace) |
| Botones custom dejan de funcionar | Se borró/desactivó mal el bloque Releasit | Bloque Releasit `disabled:true` + botón permanente activo solo oculto por CSS |
| Fuentes no se ven | No están cargadas | `@import` en `<style>` del bloque PROPUESTA |
| Título nativo no se centra (Dawn) | Dawn no tiene `title_alignment` | Reemplazar `title` por `custom_liquid` con `<h1>` centrado |
| Reveal-on-scroll hace flash | Elementos arriba del fold en la lista | Excluirlos o chequear `inView()` al cargar |
| Color viejo persiste tras recolorear | Bloques hardcodean hex (no leen `var(--brand-*)`) | Search-replace de los 4 hex en TODO el JSON (ver `sistema.md`) |
| Botón teal de Releasit no se repinta | Color inline `!important` de la app | Ocultarlo, o cambiar en Releasit app → Buy Now Button → color |
| **Botón de compra sale BLANCO/sin fondo** | El botón usa `var(--cta)` pero el token `--cta` no quedó definido en `:root` (config center desincronizado), o no resuelve en el contexto del botón Releasit | **HARDCODEAR el verde** en el botón y sticky: `#1D9E06` (oscuro `#157A04`, rgb `29,158,6`) en vez de `var(--cta)`. Es lo que hace el ejemplo que funciona. REGLA #2 = siempre ese verde, así que hardcodear es lo correcto y a prueba de fallos. |
| **Shopify dice "illegal characters" al guardar el template** | Caracteres **no-ASCII dentro del comentario `/* */` inicial** del JSON (ej. `·`, `—`, emojis) | El comentario de cabecera debe ser **ASCII puro** (reemplazar `·`/`—` por `-`). El contenido visible (copy, emojis, acentos) sí puede ser unicode; solo el comentario `/* */` de arriba debe ser ASCII. (Las cajas `═` dentro de `custom_liquid` NO son el problema: el ejemplo Shrine las usa y funciona.) |
| **`horizontal-ticker` no hace referencia a una sección existente** al importar | Estás importando un template **Shrine** en un tema **Dawn/Sense** (esa sección solo existe en Shrine) | Importa en el tema Shrine (ahí funciona nativo). Si de verdad vas a Dawn, reemplaza los 2 `horizontal-ticker` por secciones `custom-liquid` con `dawn-ticker.liquid`. |
| **El intro Ignition queda MONTADO tapando la página** ("no se ve nada") | La salida depende de `animation … forwards` (CSS): Chrome pausa animaciones en pestañas en segundo plano, u otra capa las resetea | Motor de salida **JS multi-vía** de `sec-ignition.liquid` (timer + interacción + visibilitychange + failsafe 7s con `removeChild`). NUNCA salida solo-CSS. Ver `ignition-variantes.md` REGLA DE SALIDA |
| **Overlay fixed se ve como un CUADRITO** (en PC no ocupa la pantalla) | El bloque vive dentro del main y un ancestro tiene `transform` (animaciones de Dawn/Shrine) → `position:fixed` se ancla al ancestro, no al viewport | **RE-PARENT al `<body>`** como primera línea del script del overlay (igual que sticky/WhatsApp). Verificar rect = viewport en PC, tablet y móvil |
| **Infografías decapitadas** en escalera/tarjetas (texto quemado cortado) | Imagen 2:3 con texto adentro metida en slot 16:10/4:3 con `object-fit:cover` | Crop FOTOGRÁFICO exacto al ratio del slot (solo la zona de foto, sin texto), o imagen completa a proporción natural (`height:auto`). El copy vive en el HTML, no en la imagen |

## Puntuación (regla GLOBAL del usuario, G3.3)
NUNCA usar signos de apertura `` ni `` en el copy. Solo el de cierre: `Es para ti?`, `Qué esperar`,
`Adiós verrugas!`. Es más humano y menos robótico. Aplica a TODA sección/título/FAQ/copy que genere la skill.
