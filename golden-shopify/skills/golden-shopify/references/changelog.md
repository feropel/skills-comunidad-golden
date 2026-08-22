# Changelog — GOLDEN SHOPIFY

Registro de versiones de la skill. Cada vez que se absorbe una mejora de una página
real, se sube una versión aquí (ver el ritual de auto-mejora en SKILL.md).

## G4.0 — 2026-07-25 — PERFILES + embudo de 24 secciones (absorción de la página real en producción)
**Versión mayor: cambia la arquitectura, no solo el detalle.** Motivo: la skill documentaba un embudo
de 17 secciones mientras la página real que ya estaba corriendo iba en **24** y con otra estructura.
La skill se había quedado atrás de su propia producción. Se absorbió leyendo el `product.json` VIVO,
no una memoria (ver la regla de inventarios desde archivo vivo).

**1. Sistema de PERFILES — un solo motor, dos formas de vender.** Nuevo `references/perfiles.md`
y flag `PERFIL = "marca" | "catalogo"` en el config center. Decisión de diseño explícita: **NO se
bifurca en dos plantillas**, porque dos fuentes de verdad garantizan que una se quede atrás (que es
exactamente el problema que originó esta versión). El perfil solo cambia qué secciones entran, en
qué orden y con qué tono; el motor (Releasit, precio, sticky, candado, tickers, reglas de oro,
estándares de código) es único.
- `marca` → manifiesto, historia/origen, línea de productos. Vende identidad y recompra.
- `catalogo` → escalera de combos, demostración y comparativa **obligatorias**; fuera el manifiesto
  y la historia (suenan falsos en producto de catálogo); reglas de copy de dropshipping activas.
- Nueva pregunta inicial #2 (perfil), antes del país y los colores.

**2. Embudo canónico 17 → 24 secciones.** Candado, Ignition y WhatsApp **salen del main y pasan a
secciones sueltas** (son overlays: su orden no afecta el layout y así el cliente los apaga sin entrar
a los bloques del producto). Entran dolor segmentado por público, seguridad/objeción #1, demostración,
modo de uso, combos, envío+garantía y schema. Tres tickers en vez de dos.

**3. `sec-bloque-alternado.liquid` — el patrón dominante del cuerpo de la landing.** Imagen + texto
con el lado alternando; móvil apilado, PC dos columnas, imagen con `srcset`/`sizes`/`width`/`height`
(sin CLS) y float sutil solo en PC. Es el componente con el que se construye la mayor parte del
embudo: menos texto, más imagen.

**4. REGLA #6 — ninguna animación puede esconder lo que vende.** Caso real: el revelado al scroll
dejó secciones en blanco cuando el observer no disparó. Nuevo `efx-reveal-seguro.liquid`:
el CTA, el sticky y las imágenes quedan FUERA del revelado con `!important`; red de seguridad que
a los 1.2 s fuerza visible todo lo pendiente; `rootMargin` de 1200 px; re-escaneos para contenido
inyectado tarde; y opt-in por clase en `<html>` para que sin JS la página se vea completa.

**5. `sec-cta-suelto.liquid` reemplaza a `sec-cta-mid.liquid`.** El mismo CTA sirve para las puertas
2, 3 y 4. Un solo listener delegado para todos los botones de la página, y **fallback**: si el botón
principal no existe, hace scroll al precio en vez de quedarse mudo.

**6. `sec-seo-aio-schema.liquid` — el JSON-LD se muda a su propia sección invisible** (altura 0).
Antes vivía dentro del FAQ: si el cliente lo apagaba o lo movía, se perdía el SEO. Ahora sobrevive.
Se mantiene la regla de G2.2: `aggregateRating` solo con conteo REAL y verificable.

**7. `efx-video-lazy.liquid` — demostración en video sin matar la velocidad.** `data-src` +
`preload="none"` + poster WebP; el src se asigna solo al acercarse al viewport. Un MP4 con src
directo se descarga aunque esté al final de la página.

**8. `sec-seguridad.liquid` y `sec-dolor-segmentado.liquid`.** La primera resuelve la objeción #1
ANTES de las features (cuando el cliente llega al FAQ ya decidió que no). La segunda parte el dolor
en dos secciones cuando hay dos públicos con dolores distintos — con el criterio de cuándo NO usarla
(si hay un público dominante, segmentar diluye).

**9. Estado por defecto en producción:** countdown, garantía-bloque y descripción nativa se apagan
cuando ya hay una sección que hace ese trabajo mejor. Duplicar resta.

⚠️ **Pendiente de esta versión:** `assets/product.base.json` sigue con el order de 17 secciones.
Hasta regenerarlo, la referencia de orden canónica es la tabla de `SKILL.md`, no el base.

## G3.17 — 2026-07-18 — Aprendizajes de un build real (product.json tema Shrine)
Cinco lecciones absorbidas de un build en vivo, todas ADITIVAS (nada se reescribió ni cambió comportamiento):
- **Panel de Shopify = campo `"name"` del JSON:** el rótulo/número que el editor muestra para cada sección
  y bloque sale del `"name"` del `product.json`, NO del schema ni de comentarios. Para numerar/nombrar
  ("5 TICKER TOP", "0 CONFIG CENTER") se edita ese `"name"`. Error a no repetir: crear `sections/lc-NN-*.liquid`
  solo para renombrar el panel es innecesario. → `sistema.md`.
- **Marquee/ticker SIN HUECOS en PC ancho:** con pocos ítems, el loop `translateX(0→-50%)` deja blanco si
  cada mitad es más corta que un viewport PC (~1920px). Regla: repetir el contenido hasta que cada mitad
  supere ~1920px, con 2 mitades idénticas para que -50% sea continuo. → `efectos-premium.md` (sección tickers).
- **Contraste de emoji vs su fondo:** ningún emoji del mismo color que el fondo donde va (💚 sobre CTA verde
  se pierde) → emoji contrastante, regla para toda la página. → `estandares-liquid.md` (accesibilidad) + `reglas-de-oro.md`.
- **No repetir el mismo claim en bloques ADYACENTES:** cada bloque dice algo nuevo; los términos núcleo
  (envío gratis, contra entrega) se repiten solo en puntos de decisión, no pegados. → `reglas-de-oro.md` (Regla 0-D).
- **Reseñas de ejemplo con caras IA:** placeholders reemplazables (retratos tipo selfie, NO ecom-magic),
  marcados como EJEMPLO. → `reglas-de-oro.md`. Sellos → **G3.17**.

## G3.16 — 2026-07-10 — Overlays re-parentados al body + verificación PC/TABLET/MÓVIL siempre
Continuación del build real (mismo día): en PC el intro se veía como un CUADRITO. Causa: el bloque ignition
vivía dentro del main de Dawn y un ancestro con `transform` ancla `position:fixed` al contenedor. Fix de raíz:
- `sec-ignition.liquid`: **re-parent al `<body>`** como primera línea del script (igual que sticky/WhatsApp).
  Punto 0 nuevo en la REGLA DE SALIDA + fila nueva en la tabla de errores.
- **Regla del usuario (innegociable)**: el render real se verifica SIEMPRE en los 3 escenarios — móvil ~390px,
  tablet ~768px y PC ~1440-1920px — sin scroll horizontal, nada cortado, overlays a viewport completo
  (`rect = innerWidth×innerHeight`). Actualizado el paso 3 del RENDER REAL en `auto-check.md`. Sellos → **G3.16**.

## G3.15 — 2026-07-10 — Ignition a prueba de todo + imágenes que encajan (build real Dawn, vertical sueño)
Dos lecciones de un build real, absorbidas de raíz:
- **IGNITION**: la salida del intro dependía 100% de `animation … forwards` (CSS) → si la pestaña abre en
  segundo plano o algo resetea animaciones, el overlay queda MONTADO. `sec-ignition.liquid` ahora trae motor
  de salida JS multi-vía (timer + interacción + visibilitychange + failsafe `removeChild` a los 7s + una vez
  por sesión) y `prefers-reduced-motion → display:none` (eliminado el "bypass" que forzaba animaciones).
  Regla nueva en `ignition-variantes.md` (REGLA DE SALIDA) + check #20 en `auto-check.md`.
- **IMÁGENES QUE ENCAJAN**: infografías con texto quemado se decapitaban en slots `object-fit:cover`.
  Regla: crop fotográfico exacto al ratio del slot o imagen completa a proporción natural. Filas nuevas en
  la tabla de errores de `reglas-de-oro.md` + ítem obligatorio del render real en `auto-check.md`.
- El RENDER REAL ahora exige probar el ciclo de vida del intro (aparece → desaparece del DOM, incluso con
  pestaña en segundo plano) y el encaje de imágenes ANTES de entregar. Sellos → **G3.15**.

## G3.14 — 2026-07-06 — Auditoría golden-skill-auditor (informe → reparación)
Hallazgos con evidencia, todos arreglados:
- **Referencia rota:** un archivo premium retirado citado 3 veces en `efectos-premium.md` pero no existe
  (archivo retirado en una versión vieja) → re-apuntado a `references/componentes/`, ejemplos y
  `related-products.premium.css.txt` (que SÍ existen).
- **Signos de apertura** (interrogación/exclamación invertidas) en 12 docs + `examples/demo-dawn.json` (regla GLOBAL del usuario:
  solo signo de cierre) → eliminados en todos.
- **Línea de versión bajo el H1** de SKILL.md (patrón de la casa) → añadida.
- Confirmado por inventario: cero datos privados, cero componentes huérfanos reales (los 38 citados),
  sin scripts rotos. Sellos → **G3.14**.

## G3.13 — 2026-07-02 — Anonimización para compartir con la comunidad
Auditoría de privacidad de toda la skill (para publicarla). Confirmado CERO: WhatsApp real (solo el
placeholder falso 573001234567), rutas /Users, emails, IDs/theme-IDs de Shopify. Anonimizado:
- **Dominio real** eliminado → "la tienda en vivo".
- **Marcas/tiendas reales** de builds anteriores → descriptores genéricos de categoría (p. ej.
  la marca del producto demo → "PRODUCTO DEMO"; nombres de otros productos → "un sérum facial (ejemplo)",
  "un producto de salud (ejemplo)", etc.). Sin nombrar ninguna marca real en el registro.
- Se mantienen términos de CATEGORÍA/ingrediente (verrugas, veneno de abeja) como ejemplos genéricos
  (no privados) por decisión del usuario. Sellos → **G3.13**.

## G3.12 — 2026-07-02 — Orquestación de imágenes: golden-shopify = CEREBRO
Integración con la fábrica de imágenes. golden-shopify NO genera imágenes: decide el plan y reparte.
- **Nuevo `references/imagenes-orquestacion.md`:** reparto (golden-ecom-magic = infografías foto real+texto
  por navegador, SOLO imágenes · golden-ugc-avatar/Higgsfield = GIF/video · Nano Banana = photoreal),
  el **BRIEF VISUAL** como contrato de sincronización entre skills (yo doy el QUÉ, cada generadora sabe el CÓMO),
  y matriz de formatos por ubicación (galería 1080×1080 · descripción 1-3 infografías 1080×1350 · escalera 1:1 · cine 16:9/video).
- **Descripción liviana:** solo 1-3 infografías clave (no 8-12); el resto de la historia visual la cargan
  las secciones (escalera/cine/video) + bloques nativos (SEO/editable/liviano). Alineado con la estrategia de ecom-magic.
- **Playbook Paso 3** reescrito: producir el BRIEF e invocar la skill generadora correcta. Sellos → **G3.12**.
- **Cómo piensa Ecom Magic (mapeo brief→campos):** documentado que imita una PLANTILLA de referencia
  y compone sobre foto real; qué PUEDE (arquetipos grilla/pack/testimonio/antes-después/cómo-actúa,
  redimensionar/traducir/editar) y qué NO (video/GIF, tamaños ≠ 1080×1080/1080×1350, layouts sin
  plantilla → van a Higgsfield/Nano Banana). Tabla de mapeo brief→campos para cero conflictos.
- **CORRECCIÓN (dato del usuario):** Ecom Magic NO está limitado a 1080×1080/1080×1350 — tiene MUCHOS
  formatos y **tamaño PERSONALIZADO (ilimitado)**; esos dos son solo el estándar Golden más usado.
  Nunca descartar Ecom Magic por tamaño (sí puede 16:9 del cine, etc.). El único límite real: video/GIF
  (→Higgsfield) y foto photoreal sin texto/plantilla (→Nano Banana). Corregido en imagenes-orquestacion.md.


## G3.11 — 2026-07-01 — Paddings THEME-SAFE (fin del error "must be a step in the range")
Al pegar en Shrine, el tema rechazó al guardar: **"Setting 'padding_top' must be a step in the range"**
(las secciones de fusión traían padding_top/bottom = 36/24/10, y Shrine solo acepta pasos válidos de
su rango). Arreglado de raíz:
- **`product.base.json` y ejemplos:** eliminados TODOS los `padding_top`/`padding_bottom` de las
  secciones → el tema aplica su default (nunca rechaza al guardar; sirve igual en Shrine y Dawn).
- **auto-check #19:** falla si alguna sección trae padding_top/bottom.
- Sellos → **G3.11**.

## G3.10 — 2026-07-01 — Test final en producto (PRODUCTO DEMO/verrugas generado desde cero)
Se generó la página de verrugas DESDE CERO con la skill (no a mano) para el test de cierre. El test
CAZÓ un fósil que ningún check anterior veía:
- **`RELEASIT_BUTTON_CONFIG.text = "QUIERO MI PRODUCTO DEMO"`** — el texto del botón de compra vive
  dentro de un objeto JS, NO en un `{% assign %}`, así que la reescritura por-variable no lo tocaba.
  Corregido en la página + horneado: **auto-check #18** (texto DEMO VISIBLE fuera de comentarios,
  incluye configs JS) + nota en el PLAYBOOK Paso 1 (reescribir Releasit/sticky, no solo los assign).
- Resto del test: la skill reprodujo la página aprobada con copy coherente (spray→rocía, veneno de
  abeja protagonista, sin lunares, WhatsApp real, INVIMA con enfoque positivo, reseñas de verrugas).
- Sellos → **G3.10**.

## G3.9 — 2026-07-01 — Pasada de perfección: componentes limpios, a11y universal, playbook 0→1000
Auditoría exhaustiva de los ~40 componentes (no solo la base):
- **Fósiles en 4 componentes fuente** neutralizados: `01-propuesta` ("máxima energía"), `sec-ignition`
  ("potencia desbloqueada"), `sec-beneficios` ("energía y vitalidad"), `sec-faq` (copy de bebida
  energética: tapa-vaso/Borojó/Guaraná). **Cero fósiles en toda la skill.**
- **prefers-reduced-motion UNIVERSAL:** la capa global `gfs-a11y` pasó de lista de clases a reset
  `*,*::before,*::after` → cubre los 11 componentes que animaban sin guardia + todo lo demás, de una.
  Inyectada también en el ejemplo Dawn (que no tenía capa a11y global).
- **Signo de apertura /** eliminado del ejemplo Dawn.
- **PLAYBOOK DE GENERACIÓN (0→1000)** nuevo en SKILL.md: receta de 5 pasos (datos reales → config →
  copy por sección → imágenes → coherencia → auto-check + render real). Cierra la brecha "genera esqueleto".
- **`imagenes.md`:** regla de oro escalera/cine (URLs nuevas, nunca las infografías de la descripción).
- Ejemplos re-sincronizados. Sellos → **G3.9**.

## G3.8 — 2026-07-01 — Ejemplos de referencia al día + FAQ demo de-fosilizado
Los ejemplos que la skill usa como referencia estaban VIEJOS (demo-shrine en G2.8, 0/6 secciones de
fusión) → engañaban la generación. Sincronizados a la arquitectura G3.7:
- **`examples/demo-shrine.json`** = snapshot de `product.base.json` (embudo canónico, 17 secciones).
- **`examples/demo-dawn-v2.json`** llevado al embudo canónico: 6 secciones de fusión añadidas como
  custom-liquid `scheme-1`, `sec_autoridad` off, **candado landing** insertado y **FAQ accesible**.
- **FAQ demo de la BASE** tenía copy de bebida energética (tapa-vaso, "energía y vigor", Borojó/
  Guaraná/Chontaduro) → **de-fosilizado** a copy product-agnostic. Ambos ejemplos pasan el auto-check.
- Sellos → **G3.8**. (Pendiente 1000: validar Dawn renderizado en vivo + QA móvil + flujo de imágenes.)

## G3.7 — 2026-07-01 — Coherencia de producto (auditoría "como cliente" de verrugas → 870/1000)
Leída la página entera como cliente. Estructura 10/10; bajaba por INCOHERENCIAS de copy. Reglas nuevas
(Regla 0-C) + scrub ampliado:
- **Fósiles de energía en intro/hero:** la base traía `IGN_SUBTITLE="POTENCIA DESBLOQUEADA"`,
  `⚡ PRODUCTO DEMO ⚡` y un acento cian huérfano `#0bd4fd`. Neutralizados en `product.base.json`.
  Añadidos al auto-check: "potencia desbloqueada" (scrub demo) y `#0bd4fd` (colores huérfanos).
- **Regla 0-C — coherencia de producto:** la FORMA manda el verbo (spray→rocía, gotero→gota…);
  liderar con la USP/ingrediente estrella (no "naturales" genérico); no vender lo que el producto NO
  trata (lunares); un solo WhatsApp real; claims legales solo si son reales (enfoque positivo).
- (En la página en vivo se aplicó todo: spray, veneno de abeja como protagonista, intro re-tematizado,
  ticker sin "lunares", WhatsApp real, INVIMA fuera con enfoque positivo. Eso es específico del producto,
  no de la skill; lo que se hornea son las REGLAS de arriba.)

## G3.6 — 2026-07-01 — Reingeniería de arquitectura: embudo canónico + 6 secciones de fusión en la base
El cliente: "se ve fea, no convierte, dos bloques grandotes al final, quiero el ticker después de la
descripción." Rediseño como product-page profesional (neuroventa). Cambios horneados:
- **Orden canónico NUEVO** (Regla 0-A en reglas-de-oro.md): Ticker → HERO+CTA#1 → **Ticker tras
  descripción** → PROBLEMA → AGITAR → SOLUCIÓN → **CTA#2** → BENEFICIOS → **VISIÓN+CTA#3** → RESEÑAS →
  EXPECTATIVAS → ES-PARA-TI → COMPARACIÓN → FAQ → **MANIFIESTO+CTA#4** → disclaimer.
- **La base generaba plantillas INCOMPLETAS:** faltaban 6 secciones (el usuario las metía a mano).
  Ahora horneadas en `product.base.json` desde sus componentes: `sec_escenas`, `sec_ya`,
  `sec_cine`, `sec_timeline`, `sec_esparati`, `sec_disclaimer`. Order de la base: 14 → **17 visibles**.
- **Se separaron los dos bloques oscuros del final** (VISIÓN "cine" + MANIFIESTO): la visión sube a
  mitad de embudo (future-pacing tras beneficios), el manifiesto queda como cierre. Ya no van pegados.
- **Ruido fuera por defecto:** `seccion_autoridad` (cifras placeholder = prueba social falsa) apagada;
  ficha técnica y related-products siguen off.
- **Cadencia de CTA**: gate cada 2-3 secciones (hero / tras-mecanismo / tras-beneficios / cierre).
- **Ticker = respiro visual** entre secciones pesadas (regla de ritmo). Sellos → **G3.6**.

## G3.5 — 2026-07-01 — Fin de "las letras": fuga de comentarios {# #} + nombres de bloques
Auditoría de la página en vivo (screenshot real de verrugas). Bugs REALES horneados:
- **`{# ... #}` se imprimía como TEXTO en la página** (encima de la Escalera y la Ficha Técnica salía
  todo el bloque `{# === COMPONENTE: ... === #}`). Causa: `{# #}` NO es comentario válido en Liquid
  (el válido es `{% comment %}`) → cuando queda dentro de un `custom_liquid` se renderiza literal.
  Arreglado: (1) `product.base.json` — quitados los `{# #}` de todos los custom_liquid; (2) los 38
  componentes de `references/componentes/` convertidos de `{# #}` → `{% comment %}...{% endcomment %}`;
  (3) auto-check nuevo (#17) que falla si aparece `{# ` o ` #}` en un custom_liquid. (Cuidado: en CSS
  `{#id{…}` es válido y NO debe marcarse → el check exige `{#`+espacio o el cierre ` #}`.)
- **Ficha Técnica se veía con `[confirmar]`** (specs sin llenar) → se confirma apagada por defecto;
  solo se enciende si el producto es gadget/kit Y se llenan specs reales.
- **5 bloques del main sin nombre** ("custom liquid" a secas en el editor) → nombrados: HERO, INTRO
  ignition, EFECTO HEADER, SEO+carrito, COLOR FOOTER. Y **header_efx + footer_efx apagados por
  defecto** (con el candado landing puesto, pintan sobre header/footer ocultos = fantasmas).
- Badge hero fósil "MÁXIMA ENERGÍA" eliminado (scrubber ampliado). Sellos → **G3.5**.

## G3.4 — 2026-07-01 — Landing bloqueada + fin del copy demo fósil + relacionados off
Hallazgos de la prueba "todo activado" sobre verrugas. Tres defectos reales, horneados:
- **Copy DEMO fósil en los tickers:** los 2 `horizontal-ticker` traían texto hardcodeado del
  PRODUCTO DEMO (suplemento): "ENERGÍA Y VITALIDAD EN CADA USO", "VITALIDAD Y ENERGÍA…". No están
  conectados al centro de control → nunca se adaptaban al producto. **Neutralizados** a copy COD
  product-agnostic (satisfacción / resultados / compra segura / garantía). Regla nueva: el texto de
  ticker SIEMPRE se reescribe por producto (cero "energía/vitalidad" salvo que el producto lo sea).
- **Nuevo bloque `custom_liquid_lock` (CANDADO LANDING):** oculta header + announcement + footer del
  tema con `display:none` (NO saca del DOM → el tema sigue inicializando su JS y las secciones
  animadas aparecen; ocultar el header desde el editor SÍ las rompía). El cliente ya no puede irse al
  home. Va justo después de PALETA en el `main`. Apagable con `LOCK = false`. Componente:
  `references/componentes/sec-lock-landing.liquid`. **Default: ON** de aquí en adelante.
- **Relacionados apagados por defecto** (`related-products` disabled:true) — confirmado en base. Solo
  se muestran las secciones que diseñamos; el usuario los desoculta manual si quiere.
- Sellos `GFS_VERSION` → **G3.4** en los 3 orígenes.

## G3.3 — 2026-06-29 — Correcciones de la página real (verrugas en vivo) — todo horneado
Auditoría de la página en vivo (la tienda en vivo (producto de salud/estética), tema Shrine)
tras el primer build. Bugs REALES encontrados y corregidos en la skill:
- **Escalera duplicaba las infografías del cliente:** `sec-escalera` tenía un fallback que jalaba
  `product.images` (que en muchas tiendas SON las infografías de la galería/descripción) → salían 2-3
  veces. **Eliminado.** Ahora, sin `P#_IMG` propia, el panel queda como tarjeta de solo texto (limpia).
  Para imágenes en la escalera: URLs NUEVAS, no las de la galería. (component + base.json)
- **"Por qué elegir" duplicada:** el `base.json` traía DOS secciones (`seccion_por_que_elegir` +
  `custom_liquid_Q4zb89` legacy). **Eliminado el duplicado** del order y de sections.
- **Motor COD se inyectaba 3× (3 listeners):** añadido **guard de idempotencia**
  `if(window.gfsFireCOD)return;` en los 3 orígenes → un solo listener aunque se inyecte varias veces.
- **Puntuación:** regla GLOBAL nueva del usuario → **nunca ``/`` de apertura**. Quitados de TODO el
  copy (componentes + base + config) y documentado en `reglas-de-oro.md`.
- Sellos `GFS_VERSION` → **G3.3** en los 3 orígenes. (Lección de generación: incluir SIEMPRE
  `seccion_whatsapp` en el order y NO dejar paddings en 0 —dan secciones apretadas—.)

## G3.2 — 2026-06-29 — FUSIÓN con "GOLDEN FULL" · Fases 2 y 3 (motor COD + secciones premium)
Se completa la fusión: lo mejor de la línea `cc-` reconstruido en `gfs-` tokenizado y accesible.
- **Fase 2 — Motor COD robusto (`gfsFireCOD`)** en el config center (3 orígenes): cualquier elemento
  con `data-cod` dispara el **botón Releasit correcto** (cascada de selectores), **evita** el botón
  que vive dentro del modal, y **reintenta** con timeout si Releasit aún no inyectó. Coexiste con los
  botones existentes (no los rompe). Más confiable que un `.click()` simple.
- **Fase 3 — 5 secciones premium nuevas** (todas gfs- tokenizadas, accesibles, apagables,
  respetan `prefers-reduced-motion`):
  · `sec-escenas.liquid` — "te suena?" (identificación por escenas, reveal escalonado).
  · `sec-ya-lo-intentaste.liquid` — demoledor de objeciones (X animadas sobre alternativas fallidas + CTA data-cod).
  · `sec-timeline.liquid` — "qué esperar paso a paso" (maneja expectativas, baja devoluciones).
  · `sec-cine.liquid` — sección cine full-bleed oscura (contraste emocional + CTA).
  · `sec-fondo-cine.liquid` — fondo cinematográfico parallax (orbes de marca + puntos, off en móvil).
- **PADDINGS THEME-SAFE (lección real):** un build falló en Shrine con *"Setting 'padding_top' must
  be a step in the range"*. Se **clampeó** todo padding de sección del `base.json` a **≤36** (16
  valores) y se documentó la regla en `temas.md` (Shrine/temas con rango menor: no exceder 36, o
  no fijar padding y dejar el default; recipe de "quitar paddings" si un tema los rechaza).
- Sellos `GFS_VERSION` → **G3.2** en los 3 orígenes. JSON revalidado. Con esto golden-shopify
  **alcanza y supera** a la línea GOLDEN FULL: tiene su persuasión + legal + COD **Y** conserva
  tokens + accesibilidad + embudo sistemático.

## G3.1 — 2026-06-29 — FUSIÓN con "GOLDEN FULL" · Fase 1: protección legal (salud)
Descubrimiento: las páginas premium de producción (Vantta verrugas, etc.) NO se hicieron con esta
skill sino con una línea hermana **"GOLDEN FULL SHOPIFY" (clases `cc-`)** que evolucionó aparte y
se especializó en persuasión + seguridad legal + motor COD robusto — mientras golden-shopify (`gfs-`)
se especializó en tokens + embudo + accesibilidad. Plan: **fusionar** lo mejor de la FULL, pero
reconstruido en `gfs-` tokenizado y accesible (no copiar su código, que hardcodea colores y tiene
FAQ no accesible). **Fase 1 (lo crítico, protección legal):**
- **Nuevo `componentes/sec-disclaimer.liquid`:** disclaimer legal (cosmético ≠ medicamento +
  contraindicaciones). Flag `SHOW_REGISTRO` (INVIMA/aval) SOLO si es REAL (REGLA #3). Tokenizado.
- **Nuevo `componentes/sec-es-para-ti.liquid`:** "es para ti?" (califica al cliente) + columna de
  **seguridad/contraindicaciones** (cuándo NO usar / consultar antes). Accesible, tokenizado.
- **Ambos declarados OBLIGATORIOS para vertical SALUD/estética** en SKILL.md (protección legal).
- Sellos `GFS_VERSION` → **G3.1**. Fases siguientes: **F2** = motor COD robusto (estilo `ccFireCOD`:
  elige el botón Releasit correcto, evita el del modal, reintenta) → generalizado a `gfs-`;
  **F3** = secciones premium (fondo cinematográfico parallax, "te suena?", "ya lo intentaste" con X,
  timeline de resultados, sección cine full-bleed), reconstruidas en `gfs-` tokenizado + accesible.

## G3.0 — 2026-06-29 — Pase de PERFECCIÓN: la skill ahora CUMPLE lo que predica
Objetivo: cerrar la brecha "predica accesibilidad/calidad pero sus bloques no la cumplían". Ahora el
generador (`product.base.json`) **pasa sus propias 6 verificaciones de estándares** (antes se
auto-reprobaba). Cambios:
- **FAQ accesible (WCAG 2.2):** la pregunta pasó de `<div>` clickeable a **`<button aria-expanded
  aria-controls>`**; la respuesta es `role="region"` con `aria-labelledby`. Operable por teclado
  (Tab + Enter/Espacio), foco visible, y respeta `prefers-reduced-motion`. Aplicado en
  `componentes/sec-faq.liquid` y en el bloque `seccion_faq` del `product.base.json`.
- **Capa GLOBAL de accesibilidad `<style id="gfs-a11y">`** en el config center (3 orígenes): **foco
  visible** en TODOS los CTA/enlaces (`:focus-visible`) + **red de seguridad `prefers-reduced-motion`**
  que calma toda animación `gfs-`/`pe-`/`mb-`/`zbx` de la página aunque un bloque lo olvide. Un solo
  bloque cubre foco + movimiento de toda la página.
- **Tokens con fallback** en los componentes tocados (`var(--brand-primary,#…)`) para que no
  dependan del config center si se usan sueltos.
- **Auto-verificado:** `product.base.json` corre las 6 checks de estándares (FAQ aria, img lazy/alt/
  dimensiones, reduced-motion, BEM) → **0 fallos** (antes fallaba a11y).
- **Bloque HORIZON NATIVO de arranque:** nuevo `references/horizon/_golden-trust.liquid` — theme
  block real (schema + `block.shopify_attributes` + `t:` + tokens + a11y). Horizon deja de ser solo
  doc: ya hay un template nativo de referencia.
- **Render REAL (procedimiento repetible)** documentado en `auto-check.md`: subir a tema no
  publicado → preview → verificar móvil+PC (foco/teclado, CLS, CTA, secciones sin vacíos) → screenshot.
- **Ejemplo al día:** `examples/demo-shrine.json` regenerado desde el base actual (accesible). **Limpieza:**
  eliminado `INSTALAR.txt` (ya se instala por el marketplace de Comunidad-Golden). Sellos → **G3.0**.
- Residual honesto (fuera del archivo de skill, es del entorno/producto): un render 100% headless
  automático (depende de una tienda Shopify en vivo) y un tema Horizon nativo COMPLETO (aquí va el starter).

## G2.8 — 2026-06-29 — Poder full: estándares Liquid (vG staging) + arquitectura Horizon
Se hornearon a la skill los DOS references originales preparados en staging (escritos para Golden,
nada copiado de las skills oficiales de Shopify) → golden-shopify queda autosuficiente en calidad de
código Y en temas de nueva generación:
- **`references/estandares-liquid.md` (reemplazado por la versión de staging):** "código sano" para
  todo bloque/sección — arquitectura sección/bloque/snippet + cuándo cada uno; schema JSON correcto
  (tipos, `range`, presets, `enabled_on`/`disabled_on`, límites, validez); traducciones/patrón
  "EDITAR AQUÍ" (texto nunca hardcodeado); **CSS** BEM con prefijo único + tokens con **fallback**
  (`var(--brand-primary,#f7a540)`) + CSS defensiva + `!important` documentado; **JS** mínimo,
  progressive enhancement, Web Components, sin librerías; **rendimiento** (enlaza `rendimiento.md`,
  no duplica): `content-visibility`, `lazy`+dimensiones sin CLS, animar solo `transform`/`opacity`,
  `prefers-reduced-motion`; **accesibilidad WCAG 2.2** por componente (FAQ `<details>`/`aria-expanded`,
  carrusel, cart drawer/modal `role="dialog"`, `aria-live` para precio/stock, sticky); checklist de 10.
- **Nuevo `references/horizon-bloques.md`:** arquitectura block-based del tema **Horizon** (theme
  blocks nativos, `@theme`/`@app`, `block.shopify_attributes` obligatorio, presets con bloques
  anidados, claves `t:`), cómo lo aprovecha Golden (custom_liquid para Dawn/Shrine/Sense · theme
  blocks nativos para tiendas nuevas/migración), tabla "cuándo Horizon vs clásico" y nota de licencia.
  Enlaza con `temas.md` (adaptador general) y `estandares-liquid.md` — sin duplicar.
- **SKILL.md:** REGLA DE INGENIERÍA ampliada ("bloque o sección" + remitir a `horizon-bloques.md`
  para Horizon/tiendas nuevas); ambos references añadidos a la lista. `temas.md` apunta a
  `horizon-bloques.md` para el detalle de Horizon (una sola fuente de verdad).
- **`auto-check.md`:** +3 verificaciones (total 6 de estándares) — `<img>` sin `alt`, `<img>` sin
  dimensiones (CLS), y clases genéricas sin prefijo BEM (colisión con el tema).
- Sellos `GFS_VERSION` → **G2.8** en los 3 orígenes. JSON revalidado; script de auto-check compila.

## G2.7 — 2026-06-29 — Estándares de código Liquid horneados (skill autosuficiente)
golden-shopify ya NO depende de skills externas para la calidad del código. Se añadió un reference
**original** (conocimiento redactado de cero, nada copiado de las skills oficiales de Shopify):
- **Nuevo `references/estandares-liquid.md`** — "Estándares de código Liquid Golden". Cubre:
  arquitectura section/block/snippet + cuándo cada uno; schema JSON correcto (tipos de settings,
  presets, enabled_on/disabled_on, límites); LiquidDoc en snippets; `{% render %}` (nunca
  `{% include %}`); traducciones/locales y el patrón Golden "EDITAR AQUI" (texto nunca hardcodeado);
  **CSS** BEM con prefijo único anti-colisión + design tokens `var(--brand-*)`/`var(--cta)` + CSS
  defensiva + `!important` solo para overrides documentados; **JS** mínimo, progressive enhancement,
  Web Components, `defer`, idempotente, sin librerías; **rendimiento de código** (enlaza
  `rendimiento.md`, no duplica): `content-visibility`, `lazy`+sin CLS, animar solo
  `transform`/`opacity`, `prefers-reduced-motion`; **accesibilidad WCAG 2.2** por componente
  (carrusel, cart drawer, modal, acordeón FAQ, sticky), foco, contraste AA, `alt`, labels,
  `aria-live`; y una **checklist "código sano"** de 10 puntos.
- **SKILL.md cableado:** (1) REGLA DE INGENIERÍA dura tras "Convención de código": antes de escribir
  CUALQUIER bloque `custom_liquid`, cumplir `estandares-liquid.md` (sano + accesible + rápido);
  (2) añadido a la lista de Referencias con su línea descriptiva.
- **`auto-check.md`:** +3 verificaciones de cierre — FAQ con `aria-expanded`/role (a11y), `<img>` sin
  `loading="lazy"` (CLS), y animaciones sin `prefers-reduced-motion`.
- Sellos `GFS_VERSION` → **G2.7** en los 3 orígenes. JSON revalidado.

## G2.6 — 2026-06-25 — FAQ baja al cierre (embudo optimizado para VENDER)
Ajuste estratégico del embudo a pedido del usuario ("quiero vender, no solo educar"). La FAQ deja
de ir en la posición 3 (justo tras la descripción, G2.4) y baja a **antes del manifiesto/cierre**.
- **Principio:** las objeciones solo importan cuando ya hay deseo. El FAQ es manejo de objeciones →
  va abajo, tras la prueba social (reseñas/autoridad/por qué elegir) y JUSTO antes del último CTA,
  para quitar el último "pero" cuando la persona ya lo quiere. Subirlo arriba plantaba dudas antes
  de crear el antojo.
- **La fricción COD inmediata NO se mueve:** garantía + "pagas al recibir" + barra logística siguen
  arriba dentro de `main` (Riesgo→0 pegado al CTA #1), así que el comprador caliente no necesita la
  FAQ arriba. Solo se reubicó la FAQ; el resto del embudo de 3 puertas (G2.5) queda intacto.
- **Nuevo `order` en `assets/product.base.json`:** ticker → main → cómo actúa → escalera → ficha
  técnica *(off)* → CTA#2 → reseñas → autoridad → por qué elegir? → **FAQ** → manifiesto+CTA#3 →
  ticker → por qué elegir? legacy → relacionados. Documentado en SKILL.md (tabla del embudo).
- Sellos `GFS_VERSION` → **G2.6** en los 3 orígenes. JSON revalidado.

## G2.5 — 2026-06-25 — Reestructura a EMBUDO DE CONVERSIÓN de 3 puertas
Cambio estratégico: la página deja de ser una lista de secciones y pasa a ser un **embudo** donde
cada fase pide la venta y la siguiente recupera al que no compró, atacando su objeción. Decisión del
usuario tras analizar los 17 bloques del main + 7 secciones + el arsenal de componentes apagados.
- **Nuevo orden canónico (embudo)** en `assets/product.base.json`: Ticker → **PRODUCTO+CTA#1** → FAQ →
  Cómo actúa → **Escalera** → Ficha técnica *(off)* → **CTA#2** → Reseñas → **Autoridad** →
  **Por qué elegir?** → **Manifiesto+CTA#3** → Ticker → WhatsApp → Relacionados.
- **3 puertas de cierre** (antes solo 1): CTA#1 Releasit temprano (comprador caliente), CTA#2
  `sec-cta-mid` tras la demostración, CTA#3 verde del manifiesto (cierre emocional). Los 3 disparan
  `#custom-releasit-btn`.
- **Activadas por defecto** (antes apagadas o sueltas al fondo): `sec-escalera`, `sec-cta-mid`,
  `sec-autoridad`, `sec-por-que-elegir`, y el CTA del manifiesto (`CTA_TEXT` = "QUIERO EL MÍO AHORA").
  Reseñas/autoridad/por-qué-elegir suben desde el fondo a su punto de máximo impacto.
- **REGLA #3 aplicada a los componentes activados** (nada se envía vacío ni con placeholder visible):
  `sec-autoridad` pierde los `[N]` → cifras de EJEMPLO reemplazables (+12.000 clientes, +30.000
  entregados); `sec-escalera` y `sec-por-que-elegir` pasan de texto-instrucción ("Describe aquí…")
  a copy genérico presentable y reemplazable. `sec-ficha-tecnica` queda **incluida pero apagada**
  (`disabled`) porque sus specs son datos duros `[confirmar]` (no se inventan, REGLA #3).
- Documentado el embudo en `SKILL.md` ("Estructura canónica = EMBUDO DE 3 PUERTAS"). Sellos
  `GFS_VERSION` → **G2.5** en los 3 orígenes. JSON revalidado; auditoría: 0 placeholders en
  secciones activas, 3/3 CTAs presentes.

## G2.4 — 2026-06-25 — FAQ tras descripción · reseñas de ejemplo · ficha técnica (build Banda, Dawn, Colombia)
Cambios de SISTEMA absorbidos de un build real (banda para dormir Bluetooth). El copy del producto
NO se absorbe; la skill queda genérica/anónima.
- **Orden canónico nuevo — FAQ inmediatamente después de la descripción del producto.** Decisión
  del usuario. `assets/product.base.json` reordenado: ticker → main → **faq** → cómo-actúa → reseñas →
  manifiesto → ticker → whatsapp → related. Documentado en SKILL.md ("Estructura canónica"): la
  referencia de orden es SIEMPRE el `product.base.json`, no `examples/demo-dawn-v2.json` (desfasado
  desde v1.31, aún con el FAQ al fondo). Esto cierra la duda base-vs-ejemplo.
- **REGLA #3 invertida (reseñas/rating): nunca dejar vacío.** Si el cliente no tiene reseñas/rating,
  se INVENTAN ejemplos buenos (5–6 reseñas variadas con nombres locales y alguna de 4★ + rating
  creíble tipo `4.8 · 127 reseñas`), marcados `EJEMPLO — reemplazar por reales`. Prohibido placeholder
  visible (`[RATING]`, "sé el primero", arrays vacíos, `0.0/5`). La **honestidad se mantiene solo en
  datos de riesgo legal**: precios, tiempos de entrega, claims médicos/INVIMA y specs duras (mAh,
  voltajes, medidas) → se confirman, no se inventan. El **JSON-LD `aggregateRating`** sigue condicional
  al conteo REAL (los ejemplos son visuales en página, no estructura para Google — se preserva el fix G2.2).
  Aplicado en `componentes/sec-resenas.liquid` (default 5–6 reseñas + salvaguarda que oculta la sección
  si quedara vacía), `05-verificado-google.liquid` (4.8) y `05b-rating-simple.liquid` (4.8 · 127).
- **Nuevo `componentes/sec-ficha-tecnica.liquid`:** grid de specs (ícono + label + valor), 1 col móvil /
  2 col desktop, config-driven S1..S6, hereda `var(--brand-*)`, patrón EDITAR AQUI / NO TOCAR, apagable.
  Los VALORES nacen en `[confirmar]` (specs duras = REGLA #3). Añadido al set mínimo y a la matriz de
  arquetipos (útil en D Gadget/Demo y E Kit).
- **`componentes/sec-escalera.liquid`:** fallback automático — si un `P#_IMG` va vacío y el producto
  tiene galería, usa `product.images[idx]` (modulo) a 800px. La escalera nunca queda en blanco (refuerza REGLA #3).
- **`componentes/sec-manifiesto.liquid`:** CTA verde de cierre OPCIONAL (`#gfs-mani-cta`, `var(--cta)`,
  shine + pulse, aparece al hacer scroll con clase `pe-show`) que dispara `#custom-releasit-btn`. Variable
  `CTA_TEXT` editable; vacío = oculto. Respeta `prefers-reduced-motion`.
- Sellos `GFS_VERSION` → **G2.4** en `assets/config-center.liquid`, `componentes/00-config-center.liquid`
  y `assets/product.base.json` (JSON revalidado con `json.loads`).

## G2.3 — 2026-06-25 — Absorción del build un producto de salud/digestivo (ejemplo) (Dawn, salud/digestivo)
Analizado el `product.zero-breath.dawn.json` completo (build Dawn en G2.2). La mayoría de mecánicas
ya estaban en la skill (sticky→body, reveal `pe-revealed`, why-cards, hide del floating). Se
absorbió SOLO lo genuinamente nuevo y product-agnóstico (el copy de un producto de salud/digestivo (ejemplo) NO se absorbe):
- **Nueva variante de Ignition #9 "Respiración / Bloom"** (`references/ignition-variantes.md`): núcleo
  que respira + anillos + partículas que se elevan + título letra por letra + barrido diagonal.
  De-brandeada (las letras del título se setean por producto). Vertical: salud/bienestar/digestivo.
- **Nuevo componente `componentes/05b-rating-simple.liquid`**: rating liviano con reseñas REALES
  ("5.0/5 · N reseñas verificadas"), sin logo de Google ni medias estrellas. Alternativa honesta a
  `05-verificado-google` y alineada a REGLA #3 (lleva el conteo real; si no hay, no se muestra).
- **Manifiesto con partículas que se elevan** (`references/efectos-premium.md` §5): capa de partículas
  auto-contenida (heredan `--brand-light`, suben atravesando el bloque) — variante del manifiesto.
- **Botón**: oculta también `._rsi-buy-now-button-product-floating` (algunos temas Dawn muestran ese
  flotante extra de Releasit). Aplicado en `componentes/08-boton-compra.liquid` y `product.base.json`.
- Sellos `GFS_VERSION` → G2.3. Confirmado que el build Dawn ya nace con todo G2.2 (cta-center,
  desktop-apple, schema condicional, tickers custom-liquid scheme-1, descripción nativa oculta).

## G2.2 — 2026-06-25 — Absorción de la última versión del build de verrugas (PRODUCTO DEMO)
Se extrajeron y absorbieron los cambios de SISTEMA de la última versión del `product.json` de Tag
Recede (el copy específico del producto NO se absorbe; la skill queda genérica):
- **Nueva capa `<style id="gfs-cta-center">`** en el config center: centra el texto de TODOS los CTA
  (botón Releasit principal, sticky, doble CTA y el botón del **cart drawer** de Releasit
  `._rsi-buy-now-button-cart` / `._rsi-modal-submit-button`). Apagable. Evita textos de botón
  descentrados cuando el tema/Releasit los alinea a la izquierda.
- **Schema SEO condicional (REGLA #3):** el `aggregateRating` del JSON-LD ahora solo se renderiza si
  `SCHEMA_REVIEWS` tiene un conteo REAL. El default pasa de `"150"` (inventado) a `""` (vacío), con
  comentario guía. Antes inyectaba 150 reseñas falsas en Google en cada build.
- **Limpieza:** eliminado el keyframe muerto `gfsCartGlow` (no se usaba). `content-visibility` ahora
  incluye `.gfs-lad` (la escalera) para mejor rendimiento de render.
- Aplicado en los 3 orígenes: `assets/config-center.liquid`, `references/componentes/00-config-center.liquid`,
  `references/componentes/efx-seo-cart.liquid` y el `assets/product.base.json` (JSON revalidado).
  Sellos `GFS_VERSION` → G2.2.

## G2.1 — 2026-06-24 — Capa desktop "Apple" consolidada (absorbida de build real)
Absorbida del build más evolucionado de un chat de producción (PRODUCTO DEMO, Golden Colombia): se
reemplaza la capa de layout escritorio básica de v1.31 (solo `max-width`) por la capa
**`<style id="gfs-desktop-apple">`** mucho más fina y centralizada en el config center. En PC (≥990px):
- Secciones a `max-width:1140px` (≥1280px → 1240px), centradas; títulos a 40px con tracking.
- **Escalera → rejilla de 2 columnas** (`display:grid`) en vez de filas largas con lados vacíos.
- FAQ ancha y legible (920px, q/a más grandes); reseñas con más padding y texto 15.5px.
- Bloques de la columna de compra (garantía, envío, countdown, doble CTA) acotados para que no se
  vean "móvil estirado" en PC; doble CTA con `min-height:60px` y 18px.
- Se conserva `.pe-pyramid` en los caps de ancho (la versión absorbida no lo incluía → no degradar).
- Capa **apagable**: quitar el `<style id="gfs-desktop-apple">` devuelve el layout mobile-first.
- Aplicada en los 3 orígenes del config center: `assets/config-center.liquid`,
  `references/componentes/00-config-center.liquid` y el bloque paleta de `assets/product.base.json`
  (JSON revalidado). Sellos `GFS_VERSION` → G2.1.
- NO se absorbieron (decisión del usuario, este pase): motores `.py` de build/recolor ni la receta
  de port a Dawn — quedan como candidatos para un pase futuro.

## G2.0 — 2026-06-19 — 🎉 RELEASE ESTABLE
Primer release mayor. La skill GOLDEN SHOPIFY queda consolidada como sistema completo y blindado:
- **Arquitectura modular:** cada efecto/función es un bloque independiente y apagable (REGLA #5);
  Ignition propio y distinto por página (8 variantes); base tokenizada (recolor = 1 variable).
- **4 reglas innegociables** (#1 distinta · #2 CTA verde #1D9E06 · #3 no inventar · #4 completa) + #5 bloques.
- **6 temas** en 2 familias (clásica: Dawn/Shrine/Shrine Pro/Sense · nueva: Horizon/Pitch).
- **Pipeline de imágenes** Nano Banana Pro → Shopify; specs de galería/infografías; auto-check de cierre.
- **Anónima** (sin nombres reales) y **read-only / canónica** (solo se edita en la fábrica con OK del usuario).
De aquí en adelante el versionado parte de 2.0 (2.1, 2.2…).

## v1.33 — 2026-06-19 — Candado: skill CANÓNICA solo-lectura
- La skill se protege en **read-only** (`chmod -R a-w`) para que **NINGÚN proceso externo**
  (otras sesiones de Claude, linters, absorciones automáticas) la modifique. Se puede LEER libremente.
- Motivo: se detectaron ediciones concurrentes desde fuera de la fábrica (entradas de changelog y
  builds que no se escribieron aquí). Nota: el FS no distingue "chat", todas las sesiones son el mismo
  usuario; el candado bloquea por permisos, no por identidad.
- **Protocolo de edición:** solo en la fábrica (este chat) → desbloquear (`chmod -R u+w`) → editar →
  re-bloquear (`chmod -R a-w`). Aviso CANÓNICA / solo-lectura añadido al tope de SKILL.md.

## v1.32 — 2026-06-19 — Bloques INDEPENDIENTES + Ignition único (REGLA #5)
- **Desempaquetado el mega-bloque "propuesta" (18 KB, 5 cosas en 1)** en 5 bloques propios:
  `01-propuesta` (hero) · `sec-ignition` (intro) · `efx-header-cine` · `efx-seo-cart` (SEO+carrito)
  · `efx-footer-color`. Cada uno se apaga/prende solo desde el editor de Shopify. Contenido
  preservado 100%, base parsea. block_order del main pasó de 13 a 17 bloques.
- **REGLA #5:** cada efecto = su propio bloque; nada de bloques abiertos para rellenar con código
  (si hace falta video/imagen → sección NATIVA del tema, no slot de Liquid).
- **Ignition único por página:** nuevo `references/ignition-variantes.md` con 8 variantes
  cinematográficas 100% CSS; regla de no repetir intro entre páginas, elegir por vertical.

## v1.31 — 2026-06-19 — Layout ESCRITORIO (PC) — adiós "franja central"
La plantilla era mobile-first y en PC se veía como una columna angosta centrada con los lados
vacíos. Se añadió una **capa de layout para escritorio centralizada en el config center** (aplica
a toda página de la skill, sin tocar 15 componentes):
- `@media(min-width:990px)`: las secciones de ancho completo (`.gfs-lad` escalera, `.gfs-steps`
  cómo actúa, `.gfs-reviews`, `.gfs-why`, `.pe-pyramid`) suben a **max-width 1140px**; FAQ a 920px
  (ancho de lectura); doble CTA a 560px. `@media(min-width:1400px)`: 1280px en pantallas grandes.
- Con `!important` para ganarle a los max-width estrechos de cada componente, así llenan el ancho.
- Las bandas (autoridad, manifiesto, tickers) ya eran full-width. Los bloques del producto
  (precio, garantía, logística…) siguen en la columna del producto (no se ensanchan, correcto).
- Aplicado a `assets/config-center.liquid`, a la plantilla `examples/demo-dawn-v2.json` y al
  entregable real `product.producto-demo.json`. Sello → v1.31. Resultado: se ve bien en **móvil Y PC**.

## v1.30 — 2026-06-19 — Plantilla PRO v2 (Dawn, máximo impulso de compra) + fixes de componentes
Absorbido del build real **tienda-demo / producto-demo** (página entregada e integrada por API).
Es la evolución del esqueleto Dawn a "plantilla profesional persuasiva" lista para vender:
- **Nueva plantilla de referencia `examples/demo-dawn-v2.json`** (anonimizada, tokenizada,
  con slots de imagen `REEMPLAZA-TU-CDN`): embudo COMPLETO de impulso →
  ticker · producto (eyebrow + oferta + **countdown activo** + rating + precio dinámico +
  **CTA verde** + garantía + barra logística) · **escalera de venta con imágenes reales** ·
  cómo actúa · **doble CTA a media página** · reseñas · por qué elegir? · banda de autoridad ·
  manifiesto · FAQ · ticker · WhatsApp. Es la base Dawn recomendada de aquí en adelante.
- **Fixes de componentes (propagan a todo build):**
  - `12-sticky-bar.liquid` → **sticky anclado al `<body>`** (`appendChild`): `position:fixed`
    siempre relativo al viewport; corrige el bug de "sticky pegado arriba" cuando un ancestro
    tiene `transform`.
  - `whatsapp-flotante.liquid` → mismo anclaje al `<body>`.
  - **Nuevo `sec-cta-mid.liquid`** → doble CTA verde a media página, **sombra suave** (sin el
    "escalón" `0 6px 0` que se veía mal).
- **Énfasis de persuasión/impulso por defecto:** countdown evergreen activo, doble CTA,
  escalera demostrativa con fotos reales, escasez/urgencia, prueba social y CTA en 1ª persona.

## v1.29 — 2026-06-19 — Renombrada a GOLDEN SHOPIFY
- Skill renombrada `golden-full-shopify` → **`golden-shopify`** (dir + frontmatter + título +
  sello en cada página + rutas internas). Variable interna `GFS_VERSION` se conserva. La vieja
  archivada pasó a `golden-shopify-DEPRECATED-2024` para evitar colisión de nombre.

## v1.28 — 2026-06-19 — 6 temas oficiales en 2 familias
- Temas confirmados por el usuario: **Dawn, Shrine, Shrine Pro, Sense, Horizon, Pitch.**
- Agrupados en 2 familias: **clásica** (Dawn/Shrine/Shrine Pro/Sense — el product.json pega) y
  **nueva** (Horizon + **Pitch** — product.json NO pega → bloques Custom Liquid sueltos).
  Pitch añadido junto a Horizon en `temas.md` e intake.

## v1.27 — 2026-06-19 — Auto-verificación + tema Horizon + fijar Ignition
- **Auto-verificación de cierre (`references/auto-check.md`):** script que valida el product.json
  antes de entregar (JSON parsea, sin color demo viejo, rating≠0.0, var(--cta), sello, Ignition,
  Releasit) + checks visuales. Enganchado en Paso 6.
- **Tema HORIZON añadido (`temas.md`):** arquitectura nueva de Shopify; el product.json NO pega →
  entregar por **bloques Custom Liquid sueltos** para pegar en el editor. Intake ahora ofrece
  Dawn/Shrine/Sense/**Horizon**/otro y la skill adapta TODO el código al tema indicado.
- **Intro IGNITION fijado como obligatorio:** vive embebido en `01-propuesta-valor.liquid` (no se
  quitó nunca); ahora la checklist y el auto-check verifican que `gfs-ignition` esté presente para
  que no se caiga al reescribir el bloque 1.

## v1.26 — 2026-06-19 — Adelgazar SKILL.md (progressive disclosure)
- Movido el detalle operativo a nuevo `references/operacion.md`: (A) Modo actualización/upgrade,
  (B) sello + nota interna, (C) ritual de absorción. En SKILL.md quedan punteros cortos.
- Condensados Paso 2 (tokenización → `sistema.md`) y Estructura/Arquetipos (→ `arquetipos.md`).
- SKILL.md: 373 → 316 líneas (sin perder nada; todo el detalle vive en referencias). Base parsea.

## v1.25 — 2026-06-19 — Re-sanitización (privacidad) + auditoría
- **Fix de regresión de privacidad:** al absorber v1.19–v1.24 se recolaron nombres reales de
  producto/competencia (gadget perfumador, cubre-rayones, espejo LED, sérum facial, mascarilla
  verde, tratamiento capilar, fibras capilares, tienda demo). Re-anonimizados a descriptores
  genéricos. Verificado: 0 nombres de producto reales (solo quedan menciones del prefijo de
  código en la narración histórica del changelog). Regla reforzada: al absorber mejoras, NO
  reintroducir nombres reales — usar descriptor de categoría.
- Auditoría completa: base parsea, 23 componentes tokenizados (incl. los nuevos), 13 referencias.

## v1.24 — 2026-06-18 — Generación de imágenes AUTOMÁTICA end-to-end (Nano Banana Pro → Shopify)
Absorbido del proyecto real **tienda demo / producto demo**. Pasa el "modo imágenes" de *preguntar +
slots* a un **pipeline probado que integra todo solo**:
- **Pregunta #8 reforzada (SKILL.md):** SIEMPRE **CON o SIN generación?** CON = **Nano Banana Pro**
  (`gemini-3-pro-image` vía Gemini API key); SIN (ya tiene imágenes) = pedir URLs o **reutilizar la
  galería/multimedia del producto**.
- **Ubicación por defecto (confirmada por el usuario):** **bloques de la landing + galería del
  producto**. La descripción NO lleva imágenes (va oculta/recreada en bloques).
- **`imagenes.md` — "Pipeline AUTOMÁTICO probado":** API key en `~/.gemini_key` (no usar
  stitch/Antigravity, su token pierde el project); generación que **compone el frasco real desde su
  foto** (REGLA #3); optimizar <300 KB (Pillow); **subida por API a Shopify Files**
  (`stagedUploadsCreate` → POST multipart 201 → `fileCreate` con `filename` exacto → **URL
  predecible** `cdn…/files/<nombre>.jpg` que la plantilla ya espera); `productCreateMedia` para la
  galería. + **tabla de errores reales y su fix.**
- **Límite documentado:** el MCP de Shopify **bloquea escribir el tema LIVE/MAIN** → el `product.json`
  final lo pega el usuario; imágenes y galería sí entran por API. Botón COD muerto = inventario
  (agotado); sticky roto = ancestro con `transform` → `appendChild(body)`.

## v1.23 — 2026-06-17
- **Modo imágenes opcional (preguntar):** la skill ofrece 2 opciones — generar imágenes
  decorativas (si hay herramienta/API de imágenes conectada; puede tener costo) o sin imágenes
  con slots. Si pide generar y NO hay herramienta conectada, avisa en 1 línea + sugerencia breve.
- **Portabilidad/seguridad documentada:** la skill son archivos de texto, NO lleva API keys; al
  compartirla, el receptor NO hereda la API del usuario (conecta la suya). Nota general, sin inflar.

## v1.22 — 2026-06-17
- **Set de imágenes de landing ganadora** en `imagenes.md` (de página real + specs del usuario):
  galería = 4-6 cuadradas 1080×1080 <300KB; descripción = infografías verticales 1080×1350,
  ~10 paneles en arco PAS (hook→problema→mecanismo→beneficio→usos→contraindicaciones→comparativa
  →ingredientes→garantía→CTA). Las hace Ecom Magic AI / las aporta el usuario; la skill las
  coloca, ordena y NO duplica en HTML; complementa con secciones en código.

## v1.21 — 2026-06-17
- **Imágenes / "todo listo" (`references/imagenes.md`).** Regla: el producto REAL lo aporta
  el usuario (la IA no lo inventa); las infografías van en HTML (no como imagen); lo decorativo
  (fondos/íconos/ilustraciones) sí lo genera la IA (stitch/Gemini, Canva). Hosting en Shopify
  Archivos/CDN. Convención de slots `[IMG: ...]` con placeholder visible si falta la URL.

## v1.20 — 2026-06-17
- **La URL es CONTEXTO, no la página del usuario (Paso 0.0).** La URL puede ser suya, de la
  competencia o solo referencia. Se usa SOLO para entender el producto y adaptar el copy con
  info real; NUNCA clonar ese diseño, copiar sus reseñas, ni bajar la calidad a lo que tenga.
  El usuario parte de cero. Intake pregunta si la URL es suya o referencia (cambia anti-duplicado).
- **REGLA #4 — Completitud obligatoria.** Nunca entregar algo mediocre/incompleto: toda página
  trae TODO el sistema (set mínimo obligatorio listado en SKILL.md), siempre distinta (REGLA #1)
  pero sin que falte ningún bloque/sección. Los arquetipos cambian énfasis/orden, no si los
  bloques existen. Prohibido decir "lista/100" si falta algo o no se vio renderizada.

## v1.19 — 2026-06-17 — Auditoría de la tienda real (16 productos)
Recorrí los 16 productos de la tienda real y absorbí el patrón de las páginas GANADORAS
(Fibra/Kit capilar completo, sérum facial, espejo LED, gadget perfumador) vs las crudas (mascarilla verde, tratamiento capilar).
Hallazgo central: el motor de la skill YA cubría los fundamentos (timeline de envío, ahorro
en pesos, garantía COD "en la puerta de tu casa", badge Google, CTA "QUIERO MI… 🔥"). Lo que
faltaba eran las **secciones de persuasión narrativa** y la **estrategia de copy/ángulo**:
- **3 componentes nuevos:**
  - `sec-escalera.liquid` — storytelling alternado imagen+texto (3–9 paneles, 1 beneficio =
    1 objeción / re-cierre, reveal-on-scroll, alterna lado, soporta GIFs). El motor de venta
    de las páginas de demostración. Tokenizado.
  - `sec-por-que-elegir.liquid` — trust-grid de 4 íconos **personalizable al beneficio del
    producto** (no la grid genérica de tienda). Tokenizado.
  - `sec-autoridad.liquid` — banda/marquesina de prueba social de marca, tokenizada y con
    PLACEHOLDERS evidentes (REGLA #3: nada de "+100 mil" inventado sin confirmar).
- **`reglas-de-oro.md`:** presets de tono por ángulo (lujo/DIY/belleza/salud), reframe de
  categoría, eyebrow de beneficio, CTA primera persona + doble CTA, y **guía de copy
  compliant para verticales sensibles** (íntimo cómplice, antiedad clínico-light, hongos/
  antifúngico → versión cosmética por defecto por riesgo Meta/INVIMA).
- **`arquetipos.md`:** 2 arquetipos nuevos — **D) Gadget/Demostración** y **E) Kit/escalera
  de valor** (compone productos, ancla precio = suma de partes; distinto del bundle 2x/3x del
  Releasit form). Matriz ampliada con los componentes nuevos. **Checklist de página ganadora**
  (los 5 elementos que separan vender de no vender).
- **`checklist-producto.md`:** bloque "Página ganadora" (countdown real, garantía COD humana,
  escalera con GIFs, doble CTA, kit, tono por ángulo, compliance de verticales sensibles).
- **FIX de la base (`assets/product.base.json`):** el config center embebido estaba
  desincronizado con `assets/config-center.liquid` — NO emitía los tokens `--cta/--cta-dark/
  --cta-rgb` ni el sello `GFS_VERSION`. Resultado: el botón verde (`var(--cta)`) salía sin
  fondo. Añadidos `CTA_BG/CTA_BG_DARK/CTA_BG_RGB` (verde #1D9E06) + tokens en `:root` y el
  sello v1.19. Detectado al generar los 17 product.json de la tienda real (los agentes lo
  parchearon en cada salida). Base revalidada: parsea OK.

## v1.18 — 2026-06-17
- **Bundles 2x/3x = en el formulario de Releasit, NO en la página.** Documentado en
  `releasit-cod.md`: las ofertas por cantidad las maneja el Releasit COD Form (quantity offers);
  la página solo dispara el form y puede mencionar el ahorro en el copy. "Bundle" sale del roadmap.

## v1.17 — 2026-06-17
- **PRIVACIDAD / ANONIMIZACIÓN (para compartir la skill):** removidos TODOS los nombres de
  producto, marca y tienda reales y neutralizado el código. Reemplazos: nombres → "PRODUCTO
  DEMO"/"MARCA DEMO", tiendas → "tutienda-demo.com"/"Tienda Demo"; prefijo de código `x10`→`gfs`,
  `X10_BRAND`→`GFS_BRAND`, `X10_REVIEWS`→`GFS_REVIEWS`, `x10_cd_end`→`gfs_cd_end`; ejemplos
  renombrados a `demo-shrine.json` / `demo-dawn.json` y sanitizados. Verificado: 0 nombres
  reales, 0 `x10`, los 3 JSON parsean. Backup en `SHOPIFY BY CLAUDE/_backup-skill-pre-sanitizado`.
- **Regla 0 (prioridad máxima) en `reglas-de-oro.md`:** la instrucción explícita de color
  del usuario PISA las reglas genéricas (REGLA #2 del CTA, "badges en rojo"). Armonía:
  máximo 2 colores fuertes y un solo color de acción; un único acento de urgencia.
- **`colores-conversion.md`:** aclarado que "destacar" = brillo/tamaño/sombra, no cambio de
  matiz (CTA verde profundo sobre verde claro basta) + tope de 2 colores fuertes.
- **`checklist-producto.md`:** nuevo bloque "Render visual OBLIGATORIO" — ver la página
  renderizada (screenshot) antes de declararla lista; chequeo de armonía de paleta.
- **`03-oferta-destacada.liquid`:** borde 3px→2px + aviso de no duplicar el acento de
  urgencia y preferir relleno suave en vez de caja hueca con borde grueso.
- **Lección absorbida (Producto Demo de salud, Tienda Demo):** apilar verde+naranja+rojo y declarar
  "100/100" sin ver la página renderizada produjo un resultado "horrible". Corregido a paleta
  verde monocromática con CTA verde profundo.

## v1.16 — 2026-06-02
- **Fix rating 0.0/5.** El contador animado ahora arranca con su valor final como texto y
  tiene fallback (si el observer no dispara, queda en el número real, nunca en 0.0).
  Checklist con chequeo de calificación. (#3 del camino a 100.)

## v1.15 — 2026-06-02
- **Optimización de rendimiento en la base PRODUCTO DEMO.** Removido el *killer* global de animaciones
  (`@media prefers-reduced-motion{*...}`) que congelaba animaciones en móvil (preferencia del
  usuario). Añadido `content-visibility:auto` + `contain-intrinsic-size` a las secciones largas
  (.gfs-reviews/.gfs-faq/.gfs-manifesto/.gfs-steps/.gfs-why/.pe-pyramid) vía CSS global del
  config center → el navegador no renderiza esas secciones hasta acercarse (LCP/scroll más rápidos).
  Verificado: base parsea OK, 0 killers, content-visibility activo. (Fuentes e imágenes de la base
  ya estaban OK: sin @import, imgs con lazy.)

## v1.14 — 2026-06-02
- **TOKENIZACIÓN DE COLORES (mejora mayor).** Los componentes y la base PRODUCTO DEMO ahora leen
  `var(--brand-*)` / `var(--cta)` del config center en vez de hex hardcodeados. **Recolorear
  = cambiar las variables del config center** (mata el search-replace y los bugs de color viejo).
  CTA = `var(--cta)` (verde fijo), separado de la marca. Verificado: 0 hex de marca fuera del
  config center, base.json parsea OK. Añadidos tokens `--cta/--cta-dark/--cta-rgb` al :root.
  Actualizados SKILL.md (Paso 2), sistema.md, checklist. Roadmap: tokenizar = HECHO.

## v1.13 — 2026-06-02
- **Auditoría de la skill + 2 mejoras grandes.**
- Nuevo `references/rendimiento.md`: velocidad de carga (fuentes con preconnect+swap sin
  @import, imágenes lazy/fetchpriority/width-height anti-CLS, JS consolidado, backdrop-filter
  y content-visibility, quitar killer de prefers-reduced-motion). + checklist de rendimiento.
- **REGLA #3 (anti-invención):** prohibido inventar reseñas/rating/precios/tiempos/claims;
  si falta info, PREGUNTAR; si se sigue, placeholder evidente, nunca dato falso. + checklist.

## v1.12 — 2026-06-02
- **CTA con color FIJO: verde ganador `#1D9E06`** (oscuro `#157A04`) en todo producto, salvo
  orden expresa. Añadido `CTA_BG`/`CTA_BG_DARK`/`CTA_BG_RGB` al config center; notas en los
  componentes botón y sticky; REGLA #2 y colores-conversion.md actualizados (la guía por
  vertical aplica a marca/acentos, no al CTA). Distinto del verde WhatsApp `#25D366`.

## v1.11 — 2026-06-02
- **Nota interna al final de cada página:** comentario HTML invisible en el último bloque
  con la **fecha y hora reales de generación** del JSON (fijas, no Liquid `now`). Para el
  usuario, no para el cliente. NUNCA después del `}` final (rompería el JSON). Suma al sello
  de versión de arriba (v1.7). Documentado en SKILL.md + checklist.

## v1.10 — 2026-06-02
- **Paso 0 obligatorio: PLAN DE DIFERENCIACIÓN.** Antes de escribir JSON, la skill declara
  arquetipo, orden de secciones, hero, sección educativa, tipografía, efectos y color CTA,
  y DEBE divergir de los ejemplos y de las páginas previas (PLANTILLAS / las que muestre el
  usuario). Si arma varios en una sesión, cada uno pulsa palancas distintas. Convierte la
  REGLA #1 de "ojalá" a paso verificable. Anti-duplicado pasa a Paso 0.1.

## v1.9 — 2026-06-02
- **Matiz REGLA #2:** el WhatsApp va SIEMPRE verde `#25D366` (convención). El CTA puede ser
  verde también — no se confunden por forma/tamaño/posición/ícono. Si ambos verdes: CTA en
  verde de marca distinto y no pegados. Lo innegociable sigue: el CTA destaca sobre TODA la
  página (secciones/fondos/secundarios). Actualizado SKILL.md, colores-conversion.md, checklist.

## v1.8 — 2026-06-02
- **Modo actualización (UPGRADE PASS):** flujo formal para tomar un product.json ya
  generado y ponerlo al día con la versión actual de la skill (lee el sello, hace diff,
  aplica solo lo que falta sin romper lo que sirve, sube el sello). Documentado en SKILL.md.

## v1.7 — 2026-06-02
- **Sello de versión obligatorio:** el config center ahora inyecta un comentario HTML
  `<!-- Generado con GOLDEN SHOPIFY vX.Y · marca · fecha -->` (vars `GFS_VERSION`/`GFS_DATE`).
  Permite abrir cualquier página y saber con qué versión de la skill se hizo.
- Regla del sello documentada en SKILL.md. Al subir versión, actualizar `GFS_VERSION` por defecto.

## v1.6 — 2026-06-02
- Nuevo `componentes/landing-sin-distracciones.liquid`: oculta menú/header/footer y
  desactiva el link del logo, solo en el PDP, para retener al visitante (modo COD).
  También oculta el "skip to content". Documentado "Modo landing sin distracciones" en SKILL.md.

## v1.5 — 2026-06-02
- **REGLA #2 permanente:** el botón de compra SIEMPRE sobresale — máximo contraste,
  distinto del fondo/secciones y del botón de WhatsApp (verde). Marca verde → CTA rojo/naranja.
- Añadida "Jerarquía del CTA" en `colores-conversion.md` (mapa marca→CTA, realce, test de 1 vistazo).
- Chequeo del CTA agregado a `checklist-producto.md`.

## v1.4 — 2026-06-02
- **Preguntas iniciales ampliadas:** ahora pide PAÍS (define entrega), colores (con
  recomendación si el cliente no tiene), y WhatsApp para el botón.
- Nuevo `references/paises-entrega.md`: tiempos Guatemala (1-4 días) vs Colombia (3-7,
  con desglose preparación/tránsito/entrega). Regla: nunca mezclar países; preguntar si falta.
- Nuevo `references/colores-conversion.md`: recomendar el color que más vende por vertical
  (impulso de compra), 1 recomendado + 1 alternativa.
- Nuevo `componentes/whatsapp-flotante.liquid`: botón flotante WhatsApp real (sale del roadmap v2).

## v1.3 — 2026-06-02
- **REGLA #1 de diferenciación** añadida como principio central en SKILL.md.
- Nuevo `references/diferenciacion.md`: 8 palancas para que cada página sea distinta
  + chequeo antiespejo. Cada producto debe rediseñarse, no clonar el aspecto.
- Chequeo antiespejo agregado a `checklist-producto.md`.

## v1.2 — 2026-06-02
- **Análisis comparativo de las 5 plantillas** (producto-demo, marca-demo, Producto Demo, Producto Demo, verrugas).
- Añadido `references/arquetipos.md`: 3 arquetipos (Perfume / Salud lean / Vitalidad full)
  + matriz de qué componente activar por vertical.
- Extraído `references/componentes/sec-piramide.liquid` (pirámide olfativa 3D con tilt).
- Añadido `assets/related-products.premium.css.txt` (featured-collection premium de Producto Demo).
- Documentado el hero nativo `image_banner` (de Producto Demo) como opción de layout.
- Añadido este changelog + el ritual de auto-mejora en SKILL.md.

## v1.1 — 2026-06-02
- Consolidación: absorbió el oro de `golden-shopify` (archivada).
- Añadido `references/reglas-de-oro.md` (12 reglas + copy/legal COD + errores).
- Añadido `references/efectos-premium.md` (catálogo de snippets).

## v1.0 — 2026-06-02
- Creación. Base = PRODUCTO DEMO (`assets/product.base.json`). 17 componentes, adaptador de temas,
  releasit-cod, sistema, checklist. Ejemplos producto-demo (Shrine) + marca-demo (Dawn).

## G4.1 (2026-07-27, centro de mando)
- Fix de gobernanza: el chat COLAGENO recibió la skill TRUNCADA al invocarla (el contenido servido terminaba antes de la sección PROTOCOLO TEMA VIVO + MEDIA de la línea ~459) y trabajó toda la sesión sin el protocolo — incumplió el punto 4 (borró media sin inventariar; sin daño, por suerte). Solución: RESUMEN DURO de los 7 puntos insertado al TOPE del SKILL.md (tras el aviso de solo-lectura), con puntero a la sección completa. Lección de arquitectura: lo crítico va ARRIBA del archivo; el final puede no llegar.
## G4.1b — 2026-07-29 — Media: tema+descripción, poster obligatorio, GIF→MP4 (lección chat TOPPIK, parche 23,5→3,3 MB)
## G4.1c — 2026-07-29 — REGLA #3 con matiz PAUTA: display propio se queda; porcentajes-estudio, testimonios en imagen y atribución a terceros jamás (gaceta 4f p.3).

## G4.2 — 2026-08-07 — Límites duros de Shopify + receta Horizon/Pitch + fallback del CTA (fuente: chat INSULINUM/Nuut)
Paquete de hallazgos horneado por el Centro de Mando desde la entrada del chat Insulinum en la bandeja
(3 `FileSaveError` consecutivos en tienda real descubrieron límites que no están en la documentación oficial).
- **TOPE 50 KB por setting `custom_liquid` (aplica a TODOS los temas):** el guardado del template revienta
  con *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"*. Entró como
  punto 9 del RESUMEN DURO del SKILL.md y como **check obligatorio nro. 21 en `auto-check.md`**: medir cada
  valor `custom_liquid` en BYTES UTF-8 (no caracteres) y fallar si alguno llega a 50.000 (aviso desde 45.000).
- **Horizon/Pitch — 2 límites más (`horizon-bloques.md`, advertencia dura al tope):** `product-information`
  NO acepta bloques ajenos en su primer nivel (su esquema no declara `@theme`; ni `custom-liquid`, ni bloques
  privados con prefijo `_` declarados desde fuera). Se descubre solo con `FileSaveError` al guardar.
- **RECETA PROBADA Horizon/Pitch (`horizon-bloques.md`):** plantilla 100% secciones `custom-liquid` sin
  bloques · galería propia leyendo `product.images` · rejilla de 2 columnas por JS moviendo el DOM con
  re-armado en `shopify:section:load` · UNA sección por pieza (REGLA #5 + esquiva el tope de 50 KB) ·
  Product JSON-LD propio (la sección nativa ya no lo pone). Más la regla de conducta: nunca adivinar la
  estructura interna del `main` de un tema ajeno — pedir el `product.json` real o ir 100% custom-liquid.
- **REGLA PERMANENTE para TODA página (REGLA #2 del SKILL.md + `releasit-cod.md`):** el CTA lleva fallback
  al formulario nativo `/cart/add` si Releasit no está presente (espera ~1,5 s por inyección tardía y luego
  cae al flujo nativo). El botón siempre sobresale... y siempre FUNCIONA aunque la app falte.
- **Nota [DEUDA] visible en el SKILL.md (dos menciones de la base):** `assets/product.base.json` sigue en
  el orden de 17 secciones vs las 24 del embudo canónico G4.0 — pendiente de sesión dedicada. Hasta
  regenerarlo, el ORDEN canónico es la tabla del SKILL.md, no el base.

## G4.3 — 2026-08-07 — Componente "LO QUE ESTE PRODUCTO NO HACE" (cosecha del chat ESTUDIO 360 DENTAL CAVITY HEALING, Chile)
Repartido por el Centro de Mando desde la bandeja (orden de FER: "sin omitir detalle"). Invención del
estudio dental y probablemente lo más valioso que salió de él:
- **Componente estándar para verticales de SALUD**, descrito en el SKILL.md junto a `sec-disclaimer` /
  `sec-es-para-ti` como **obligatorio-recomendado**: una sección que declara el LÍMITE del producto con
  honestidad ("No repara una caries ya formada — eso lo hace el dentista. Sí cuida el esmalte y apoya la
  remineralización").
- **Racional probado en campo:** en una categoría donde los 5 competidores usaban odontólogo inventado,
  logos de Cruz Verde/Salcobrand/Paris como "distribuidores oficiales" y estadísticas sin estudio
  (95%/96%/97%/100%), **declarar el límite convierte la objeción "esto es una estafa" en la razón para
  comprar**: el único vendedor honesto de la categoría se queda con el cliente escéptico.
- **Funciona en tres soportes con el mismo mensaje:** sección de página, ángulo completo de pauta
  (5 textos) y respuesta pública en comentarios. Se maqueta como `custom-liquid` con el patrón de lista
  ❌ "no hace" / ✅ "sí hace" de `sec-es-para-ti`.
