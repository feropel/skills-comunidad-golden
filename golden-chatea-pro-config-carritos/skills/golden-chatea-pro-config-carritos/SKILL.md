---
name: golden-chatea-pro-config-carritos
description: >-
  Golden Group — Audita y configura el asistente de CARRITOS ABANDONADOS de Chatea Pro (el que
  recupera por WhatsApp los checkouts que el cliente dejó a medias en la tienda online). Lee el
  espacio por API, califica el campo [Carritos] Configuracion (29 casillas, 38 hojas de JSON) contra los topes del
  panel medidos en UTF-16 y contra la doctrina de la casa, reescribe los textos (adaptación del
  lenguaje, anticancelación, ubicación, tiempos, transportadoras, agradecimiento, correo, pago
  anticipado), limpia el caché de productos y revisa el ESTADO de las plantillas de Meta. Entrega
  cada campo en texto plano listo para pegar en el panel, o lo escribe por API y lo relee del
  servidor. Úsala SIEMPRE que el usuario quiera montar, revisar, calificar o corregir el asistente
  de carritos de Chatea Pro: "configura carritos", "revisa mi asistente de carritos", "recuperar
  carritos abandonados", "califica carritos", "deja carritos en mil", "mensajes de carrito
  abandonado", "arregla la configuración de carritos".
---
# Golden · Chatea Pro — Asistente de Carritos Abandonados

<!-- skill v3.2 · 2026-09-20 · auditoría golden-skill-auditor: scripts/chatea_api.py (la librería
     común que importan auditar_carritos.py, escribir_config.py, limpiar_cache_productos.py y
     validar_config.py) no aparecía mencionada en ninguna parte del cuerpo — inventario.sh la
     marcaba "huérfana potencial" (solo vivía citada por nombre en references/changelog.md,
     que es historia y no cuenta como cita viva). Se agregó una línea en la sección de
     validar_config.py explicando qué es y quién la usa. Sin cambios de comportamiento. -->
**Versión:** v3.5 · 2026-09-22 · blindada (chflags uchg + chmod 0444, estándar de la casa)
**Fábrica:** chat ✅ SKILL golden-chatea-pro-config-carritos
<!-- v3.0: la skill deja de ser "redactora de plantillas" y pasa a CONFIGURAR el espacio, con lo
aprendido afinando carritos de Golden el 18-sep. Historial completo en references/changelog.md. -->

Este asistente recupera por WhatsApp a quien dejó el checkout a medias. **Configurarlo es
llenar bien el campo `[Carritos] Configuracion`**: identidad, datos de la tienda, logística,
mensajes fijos y correo. Los mensajes de recuperación son **plantillas de Meta** que ya vienen
instaladas o que diseña el dueño: se seleccionan, no se redactan aquí.

## Lo que se aprendió y manda sobre todo lo demás (FER, 18-sep-2026)

1. **El techo no es un defecto.** El tope del panel es una compuerta: pasarse bloquea, y 1.999
   de 2.000 pasa. **Nunca se recorta contenido útil para ganar margen** ni se reporta "poco
   margen" como problema. Cuando algo se pasa, se quita **lo que se repite, lo que se contradice
   o lo que es falso**, no lo que sirve.
2. **Se mide como mide el panel: UTF-16.** Cada emoji astral vale 2. Python `len()` da otro
   número (medido: 248 contra los 249 del panel por un 🚛).
3. **Las plantillas de Meta NO son configuración.** No se reescriben ni se califican por su
   contenido. Solo se revisa su **ESTADO**: que cada casilla tenga una plantilla que exista y
   esté APPROVED, porque una no aprobada hace fallar ese paso en silencio. Crear plantillas por
   API se puede (`POST /whatsapp-template/create`, Meta las aprueba), **solo si el dueño lo pide**.
   Guía para ese caso: `references/plantillas-meta-solo-si-lo-piden.md`.
4. **El nombre del asesor es UNO por espacio.** Es el mismo en todos los asistentes. Se lee de
   los hermanos (ventas, logístico) y no se vuelve a preguntar. Solo se pregunta si ninguno lo tiene.
5. **El pago anticipado se decide POR ASISTENTE.** Carritos y logístico pueden tenerlo distinto.
   Se le pregunta al cliente junto con el resto de la configuración, y sus datos (medio, titular,
   número, llave) **solo los da el dueño**. El envío gratis sigue siendo la oferta: el anticipo es
   una excepción, así que "envío gratis" no choca con él.
6. **No se inventa nada.** Ni identidad (nombre del bot, tienda, URL), ni promesas comerciales.
   La clase de error medida: frases que suenan bien y nadie confirmó ("despacho el mismo día
   antes de las 2", "importador directo", "legalmente constituida", "lo procesamos hoy",
   "reservado por tiempo limitado"). Sin dato real, se pide o se declara que falta.
7. **La regla y el ejemplo dicen lo mismo.** El bot imita el ejemplo más que la regla. Si la
   regla dice "sin ¿" y el ejemplo trae "¿", gana el ejemplo. Se lee cada ejemplo contra cada
   regla, a mano.

## Doctrina de los textos (vigente en todos los asistentes del espacio)

Carritos no puede contradecir lo que ya dicen ventas y logístico:

- **Tono:** humano, profesional y cercano. Frases resolutivas ("claro, te explico", "te indico
  el paso siguiente"). Nunca "estoy aquí para ayudarte". Breve para chat.
- **Emojis:** **la IA no los genera** en sus respuestas. Los mensajes FIJOS (agradecimiento,
  tiempos) sí pueden llevarlos, porque se envían tal cual.
- **Signos:** sin signos de apertura ¿ ¡ en WhatsApp, solo los de cierre.
- **No inventar** precios, promociones, tiempos, estados, stock ni urgencias. **No prometer**
  entregas exactas ni respuestas inmediatas.
- **Calma** aunque el cliente esté molesto. **No insistir** más de dos veces.
- **Nunca volver a pedir un dato** que el cliente ya dio.
- **Privacidad:** nada de otros clientes ni de procesos internos.
- **Anticancelación:** primero entender el motivo; recordar el beneficio del pedido; la objeción
  de precio se explica por las **promociones** (varias unidades, volumen, adicionales, condiciones
  especiales); un solo intento; respetar la decisión final.
- **Mensajes fijos que salen en TODO pedido** (el agradecimiento) **no asumen un medio de pago**:
  si el anticipado está activo, "pagas en efectivo al recibir" le miente a quien ya pagó.
- **Los datos de la empresa son UNO por espacio**, como el nombre del asesor: si ventas dice
  "sede física" y carritos "100% virtual", o una cifra de clientes distinta, el cliente lo nota.
  Se comparan con los hermanos y la contradicción se le lleva al dueño; no se elige una sola.

**El único aviso de margen que existe es el del CAMPO ENTERO** (el JSON completo contra su tope
de escapados), no el de una casilla: ahí pasarse guarda cortado con un `200 ok`. Para las casillas
sigue mandando la regla del techo: cerca del tope pasa y no se recorta nada útil.

`scripts/validar_config.py` vigila estas reglas: signos de apertura, prompts que permiten emojis,
promesas sin confirmar, agradecimiento que asume contra entrega. **Ninguna máquina reemplaza leer
el texto completo**: el validador caza la clase conocida, no la siguiente.

`scripts/catalogo_tienda.py` lee el catálogo público de la tienda (id → título, sin token) y es
lo que le permite a la auditoría juzgar el CONTENIDO del caché y no solo su forma.

`scripts/chatea_api.py` es la pieza común que hablan con la API: `auditar_carritos.py`,
`escribir_config.py`, `limpiar_cache_productos.py` y `validar_config.py` la importan para leer y
escribir bot fields, paginar plantillas y contar caracteres como el panel (UTF-16). No se invoca
sola; es la librería compartida detrás de las demás.

## 🔴 COMPUERTA · sin el cable de la tienda no llega ni un carrito

Los carritos entran por un **webhook de la plataforma de la tienda**. Se pueden dejar las 29
llaves perfectas y no recuperar uno solo, sin ningún error. **Primero se pregunta en qué
plataforma está la tienda**, y la compuerta depende de la respuesta:

**Si es Shopify** (la única medida hasta hoy), tres comprobaciones:
1. La integración de Shopify aparece **conectada** en el panel.
2. El Access Token empieza por **`shpat_`** (el Secret es `shpss_`; los dos empiezan por `sh` y es
   el error número uno).
3. `acciones_especiales.origen_datos` es Shopify (el panel lo guarda con mayúscula; se compara sin
   distinguir mayúsculas).

Si falta el cable: `references/integracion-shopify-paso-menos-uno.md` y los 24 permisos en
`assets/permisos-shopify-24.txt`. Quien no es DUEÑO de la tienda no puede instalar la app: se
pregunta antes de empezar.

**Si es otra plataforma** (Tienda Nube, WooCommerce u otra): lo primero es **confirmar que Chatea
Pro recibe carritos abandonados desde esa plataforma**. Para Tienda Nube está **NO VERIFICADO**
(18-sep: no se encontró integración nativa; no se da por negativo con una sola búsqueda; lo
confirma un beta tester de Chatea). Mientras no se confirme:
- **no se declara el asistente "mal instalado"**: se declara **"no aplica todavía en este
  espacio"**, que es distinto;
- la venta y el despacho pueden funcionar igual por otras vías (Dropi sí integra Tienda Nube);
  lo que queda en duda es solo la recuperación de carritos;
- si Chatea no recibe carritos de esa plataforma, **el asistente no sirve ahí** y se dice así, en
  vez de configurar 29 casillas que nunca van a disparar.

## PASO 0 · Auditar el espacio antes de preguntar nada

```bash
python3 ~/.claude/skills/golden-chatea-pro-config-carritos/scripts/auditar_carritos.py \
    --token-file <PROYECTO>/.secrets/<espacio>.token --guardar <respaldo.json>
```

Solo lectura. Revisa **7 frentes** y reporta cobertura (con `--dominio <tienda.com>` para el
cruce contra el catálogo):
1. el campo contra `validar_config.py` (29 casillas, topes UTF-16, doctrina);
2. el **estado** de las plantillas seleccionadas (lista con `POST /whatsapp-template/list`; con GET
   la API da 405);
3. el nombre del asesor contra los hermanos;
4. el **caché de productos** (`[Carritos IA] Información de productos #N`);
5. la **búsqueda web** (`[Carritos IA] Habilitar búsqueda web`), que si está encendida vuelve a
   llenar el caché con basura;
6. el caché contra el **catálogo público de la tienda** (`/products.json`, sin token): entradas de
   productos que ya no existen y entradas cuyo nombre no coincide con el título real;
7. la **frescura** del caché: hace cuánto no entra un producto nuevo por el webhook. No prueba que
   el cable esté mudo (un carrito de un producto ya cacheado no deja rastro), pero si se cayó, se
   ve así.

Para saber qué es de FÁBRICA y qué tocó el negocio, el detector de la hermana logística:
`python3 ~/.claude/skills/golden-chatea-pro-config-logistico/scripts/auditar_espacio.py --token-file <ruta>`.
Lo de fábrica no se hereda; lo TOCADO es del negocio y manda. Si un script no corre, **se dice y
se sigue a mano**, nunca se da por bueno.

## LA PARTE DINÁMICA · lo único que cambia de un espacio a otro

**Esto es lo que hace que la skill no se tenga que rehacer en cada instalación.** Todo lo demás
—doctrina, topes, estructura de las 29 casillas, forma de los textos, orden de trabajo— es igual
para todos los espacios y ya está resuelto aquí.

El molde está en `assets/datos-del-espacio.json`. Se llena una vez por cliente:

| Qué | De dónde sale |
|---|---|
| País del espacio | Se lee del campo; si no está, se pregunta. Define jerga, transportadoras y pack de direcciones |
| Plataforma de la tienda y su dominio | Se pregunta. Decide la compuerta y permite cruzar el caché con el catálogo |
| Nombre de la empresa y su URL | Se lee del espacio |
| Nombre del asesor | Se lee de los asistentes hermanos: es UNO por espacio |
| Ciudad de despacho y frase de respaldo | Las da el dueño; nunca se inventan |
| Tiempos por zona | Los da el dueño, tal cual |
| Transportadoras: domicilio, oficina, prohibida | Las da el dueño. La prohibida va PRIMERO |
| Contra entrega y anticipado, con sus datos y su monto | Los da el dueño. El anticipado se decide POR ASISTENTE |
| Descuento e incentivo | Los decide el dueño. Default apagado |
| Números del negocio (clientes, años) | Los da el dueño. Se usan tal como él los escribió |

**Todo lo que no está en esa tabla no se pregunta y no se discute otra vez:** ya está decidido en
esta skill, y cambiarlo es cambiar el estándar, no configurar un cliente.

## Intake: preguntar lo mínimo

**Se LEE, no se pregunta** (del espacio y de los hermanos): nombre del asesor, tono, país,
empresa, URL, ubicación, tiempos por zona, transportadoras, modelo de pago de ventas.

**Solo lo sabe el dueño, y se pregunta una cosa a la vez:**
1. **Vía de entrega.** Default: **texto por campo para pegar en el panel**, con los topes del
   panel. Por API solo en el espacio de FER, en VIP o cuando el dueño lo pide.
2. **Pago anticipado en carritos: sí o no.** Si sí, **sus datos** (medio, titular, número, llave)
   y el **monto del anticipo** (un valor fijo que decide el dueño). Si no da monto, se propone **un
   flete completo**: con el cliente que rechaza se pierden casi dos fletes (ida y devolución), el
   50% cubre una cuarta parte y deja de proteger.
3. **Incentivo / descuento.** 🔴 Un 10% cuesta entre $4.234 y $8.467 por pedido GENERADO según el
   PVP, contra un piso de $8.000. Antes de encenderlo se corre
   `golden-dropkiller-productos-ganadores/scripts/viabilidad_cod.py`. Default recomendado: **apagado**.
4. **Prueba social real** (clientes, años, reseñas), solo si el negocio la confirma. Nunca una
   cifra inventada.

El país es **parámetro, nunca como puerta**: decide jerga, transportadoras y pack de direcciones
(`golden-chatea-pro-validacion-direcciones`). No tenerlo en ninguna lista nuestra jamás bloquea: se
investiga lo que falte y se configura igual. El país en el JSON va en minúscula (`colombia`).

## EL CAMPO · `[Carritos] Configuracion`, 29 casillas = 38 hojas

Molde: `assets/template-botfield-configuracion.json`. Topes: `assets/limites.json`. **Las claves
no se renombran**: el flujo las lee por nombre.

**Por qué dos números.** Se configuran **29 casillas**, pero el JSON tiene **38 hojas**, porque
cada plantilla de Meta ocupa cuatro (`name`, `lang`, `namespace`, `status`) y son tres plantillas:
29 − 3 + 12 = 38. El validador cuenta hojas, que es lo que se escribe; el panel muestra casillas. **Los productos NO van aquí**: entran por el webhook.

| Sección | Llave | Tope panel | Cómo se llena |
|---|---|---|---|
| identidad | nombre_asesor | 50 | El del espacio (hermanos) |
| identidad | adaptacion_lenguaje | 2000 | Contexto de carrito + doctrina completa (este asistente no tiene campo de restricciones: van aquí) |
| identidad | metodo_anticancelacion | 2000 | Causa → respuesta: desconfianza, precio (promociones), tiempo, duda, postergación |
| tienda | nombre_tienda | 80 | Nombre de la empresa, real |
| tienda | ubicacion_tienda | 200 | Texto del dueño; si el del logístico no cabe, se queda la frase que dice ciudad, envío y respaldo real |
| tienda | pais | desplegable | Minúscula |
| tienda | ofrecer_descuento · descuento_maximo · mensaje_descuento | — · — · 200 | Según la economía; apagado por defecto |
| logística | tiempos_envio | 150 | El bloque estándar del dueño, tal cual |
| logística | metodo_pago (contraentrega, anticipado, datos_pago_anticipado) | — · — · 300 | Datos SOLO del dueño; se cierran con "envía el comprobante" |
| logística | transportadoras_disponibles | **100** | **La prohibida primero**, después las de domicilio y cuáles también entregan en oficina. **Sin repetir el nombre del campo adentro** |
| recuperación | posicion_imagen · 3 plantillas · tiempos · mensaje_agradecimiento | — · — · — · **300** | Plantillas: solo estado. Agradecimiento: fijo, puede llevar emojis, sin asumir medio de pago |
| correos | activar_envio · asunto · contenido | — · 80 · 500 | Quitar el riesgo (contra entrega, envío gratis) y decir cuándo llega. Sin urgencia inventada |
| acciones | subida_automatica · imagenes_producto · origen_datos | — | La plataforma real de la tienda |
| raíz | onboarding_completed | — | true |

**Campos auxiliares `[Carritos IA] *`** (búsqueda web, automatizar pago anticipado, automatizar
creados manualmente, ofrecer descuento si se creó con uno, retraso de validación, tipo de
actividad, versión): se leen y se reportan; **cuál manda sobre el anticipado del JSON no está
medido**. No se tocan sin saberlo.

**Recordatorios, visto en el panel el 18-sep:** hay **dos pares** (tiempo, plantilla),
Recordatorio 1 y Recordatorio 2, más el mensaje de recuperación con imagen. El JSON trae además
`tiempo_recordatorio_3`, **una llave sin casilla en el panel**: si tiene valor, se deja vacía.
**Posición de la imagen:** tiene que existir y no ser GIF, o el envío falla.

### Los fallos que ya se midieron en espacios reales (todos silenciosos)

- **Transportadoras por encima de 100.** Medido dos veces en el espacio de referencia: 132 y 116, y las dos veces
  porque alguien escribió "Transportadoras disponibles:" dentro del campo. Al guardar desde el
  panel se corta en el 100 y se pierde el final: justo la transportadora prohibida.
- **`datos_pago_anticipado` heredado de otro espacio.** Manda el dinero a otra persona. El
  validador no pasa sin `--dueño-confirmo-datos-de-pago`.
- **Caché de productos con basura.** 11 entradas de la búsqueda web, sin fecha y con ids en serie,
  que describían la empresa con un giro que no era suyo; más entradas solo-URL, vacías o "No
  disponible". Como el id ya existe, **el webhook nunca las reescribe**. Se limpian con
  `scripts/limpiar_cache_productos.py` y la búsqueda web se deja apagada.
- **Producto retirado que sigue en el caché.** Medido el 22-sep en un espacio real: 3 entradas de
  productos que ya no se publican, que el bot seguía describiendo y vendiendo. **Se limpiaron ese
  mismo día**, así que hoy ese espacio da cero: el hallazgo es la CLASE, no un estado vigente. El
  cruce contra el catálogo las caza.
- **Caché con forma correcta y contenido FALSO.** Entradas con fecha e id que describían un
  producto capilar como "promueve el cultivo" y una recarga de fibra como "servicio de recarga
  digital". **La forma no dice si es verdad:** la auditoría lista cada entrada y se lee a mano
  contra el catálogo; las falsas se quitan con `--quitar id1,id2`. Precios guardados en el caché
  también caducan: se revisan. El cruce automático (`scripts/catalogo_tienda.py`, con su autoprueba)
  compara NOMBRE contra el título real: un nombre que calza no garantiza que el resto del texto
  sea cierto, así que la lectura a mano sigue.
- **Tercer tiempo de recordatorio sin casilla.** Ver arriba.

## Techos y vías

- **Instalación normal → topes del panel** (tabla de arriba). Es el default y no se pregunta.
- **Espacio de FER y VIP → se puede escribir por API**, que aguanta 20.000 escapados en el campo
  (500.000 si es LONG JSON). Aun así, **si el campo pasa su tope del panel, el día que alguien
  guarde desde el panel se corta**: por eso lo recomendado es respetar el tope también por API.
- **Cupo de la API: 1.000 peticiones por hora**; pasarse bloquea una hora. Cada escritura son
  varias peticiones (lectura, escritura, relectura). Mirar `x-ratelimit-remaining`.
- **Al clonar a otro cliente:** leer ANTES `references/ley-datos-entre-espacios.md`. Se hereda
  estructura, jamás datos (pago, plantillas, teléfonos, marca, cifras). El caché de productos se
  vacía.

## Escribir por API (solo espacio de FER, VIP o a pedido)

```bash
python3 ~/.claude/skills/golden-chatea-pro-config-carritos/scripts/escribir_config.py \
    --token-file <ruta> --tienda "<nombre_tienda exacto>" --propuesta propuesta.json \
    --respaldo-dir <PROYECTO>/backup-config [--seco]
```

La propuesta es `{"seccion.llave": valor}`. El script lee en vivo, **aborta si la tienda no es
la esperada**, respalda, cambia **solo** las llaves que difieren, mide UTF-16 contra el tope,
escribe, **relee del servidor** y comprueba que el resto del campo no se movió (la API recorta el
salto de línea final: se compara el JSON parseado). El token vive en `.secrets/` del proyecto,
**nunca en el chat ni en la skill**.

🔴 **Después de escribir, el dueño recarga la pestaña del panel antes de guardar ahí.** Si guarda
con la vista vieja, pisa lo escrito.

## Entrega

- **Cada campo completo, en texto plano, uno por uno, listo para pegar**, con su medida
  `N/tope` y qué cambió y por qué fuera del bloque. Nunca "ya te lo di arriba".
- Lo que **no se tocó y por qué** (decisiones del dueño pendientes).
- **Casos duros** antes de dar algo por bueno: cliente molesto, dato ya dado, cancelación,
  objeción de precio, desconfianza. Se declara si fue **simulación por lectura o corrida real**.
- **Cobertura, no veredicto**: N de N campos revisados, qué se ejecutó, qué quedó sin verificar.
  La prueba final es abandonar un carrito real y ver qué llega.
- Vara de calidad: `references/ejemplo-completo.md`.

### QA antes de entregar

- [ ] Plataforma de la tienda preguntada. Si es Shopify, los tres puntos de la compuerta; si es otra, confirmado que Chatea recibe sus carritos o declarado "no aplica todavía".
- [ ] `auditar_carritos.py` corrido: 0 críticas, y cada aviso explicado.
- [ ] Cada texto medido en UTF-16 contra su tope. Cerca del tope **pasa**.
- [ ] Ningún prompt le permite emojis a la IA; ningún texto de WhatsApp trae ¿ ¡.
- [ ] Ninguna promesa comercial sin confirmar por el dueño; ninguna identidad inventada.
- [ ] Ejemplos leídos contra reglas, a mano.
- [ ] Nombre del asesor igual al de los hermanos.
- [ ] Transportadoras: prohibida primero, oficina señalada, ≤ 100, sin el nombre del campo.
- [ ] Agradecimiento sin asumir medio de pago si el anticipado está activo.
- [ ] Datos de pago confirmados por el dueño de ESTE espacio.
- [ ] Plantillas seleccionadas existen y están APPROVED (contenido: no se califica).
- [ ] `tiempo_recordatorio_3` vacío. Caché sin basura de forma, **cruzado contra el catálogo**
      (`--dominio`) **y leído a mano**. Búsqueda web apagada.
- [ ] Frescura del caché revisada: si hace semanas que no entra un producto nuevo, se comprueba el
      cable con un carrito de prueba antes de declarar nada.
- [ ] Si fue por API: releído del servidor, resto intacto, y aviso al dueño de recargar el panel.
- [ ] `bash ~/.claude/skills/golden-chatea-pro-config-carritos/scripts/verificar_pais_no_es_puerta.sh` en verde.
- [ ] `python3 ~/.claude/skills/golden-chatea-pro-config-carritos/scripts/validar_config.py --autoprueba` en verde.
- [ ] `python3 ~/.claude/skills/golden-chatea-pro-config-carritos/scripts/catalogo_tienda.py --autoprueba` en verde.
- [ ] Las autopruebas se corren con `PYTHONDONTWRITEBYTECODE=1`, para no dejar `__pycache__` dentro de la skill.

## Qué NO es (límite con Ventas)

- **Carritos (esta skill):** el disparador es un checkout abandonado en la tienda. El contacto es
  frío: no hay ventana de 24 h abierta, por eso todo toque de recuperación va por plantilla.
- **Remarketing de una conversación de venta que se enfrió:** `golden-chatea-pro-prompt-ventas`.

## Conexiones

- 🛒 Ventas WhatsApp (oferta, pago, nombre del asesor) → `golden-chatea-pro-config-ventas-wp`
- 📦 Logístico (toma la dirección al cerrar; también decide su propio anticipo) → `golden-chatea-pro-config-logistico`
- 🗺️ Jerga y direcciones por país → `golden-chatea-pro-validacion-direcciones`
- 🎬 Los cuatro asistentes a la vez → `golden-chatea-pro-full-configuracion`

Si una hermana no está instalada, se entrega igual y se avisa qué pieza queda por conectar.
Los hallazgos de campo se reportan al 🧠 CENTRO DE MANDO, que decide si se retransmiten a las
hermanas.

## Privacidad (skill compartible)

Ningún dato real vive en esta skill: ni cuentas de pago, ni tiendas, ni nombres, ni tokens. Se
leen o se preguntan en cada uso y viven solo en el espacio del cliente y en sus respaldos. Los
ejemplos son ficticios.
