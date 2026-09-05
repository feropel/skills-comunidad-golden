---
name: golden-shopify
description: >-
  Construye, adapta y recolorea páginas de producto Shopify de alta conversión para venta
  CONTRA ENTREGA (COD con Releasit COD Form) y para pago anticipado. Plantilla base =
  PRODUCTO DEMO (el build más completo, sobre Shrine Pro), adaptable a Dawn ("plantilla
  down", el tema que se enseña o se regala), Sense y cualquier tema, porque la mayoría de
  bloques son custom-liquid y portables. Trabaja con DOS PERFILES sobre un mismo motor:
  "marca propia" y "catálogo o dropshipping". Úsala SIEMPRE que el usuario quiera: crear o
  mejorar una landing o página de producto, armar un product.json o product.tema.json,
  adaptar la página de un cliente a otro tema, cambiar la marca o los colores de una
  plantilla, agregar countdown, sticky bar, garantía, barra logística, reseñas, FAQ,
  manifiesto, combos, pirámide o "cómo actúa", precio dinámico, botón Releasit, o resolver
  dudas de carrito, Releasit o COD. También cuando venda un producto de Dropi o de catálogo
  público y necesite diferenciarse por oferta y por página.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1010 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# GOLDEN SHOPIFY (`golden-shopify`)
<!-- skill G4.20 · 2026-09-04 (la skill se comparte y corre sobre el tema de OTRA persona): el tema ya estaba cubierto en references/temas.md ('preguntar SIEMPRE', 2 familias) pero NO era compuerta de arranque — el Paso 0 solo exigia el cerebro de marca — y el protocolo asumia acceso por API, que un VIP en su propio Claude puede no tener. Nuevo Paso 0-A: el tema se DECLARA antes de generar, y se MIDE desde la URL publica (Shopify.theme.schema_name da la familia real aunque el tema este renombrado) antes que preguntarlo. Ademas el candado asumia la familia Dawn: sus 13 selectores no cubrian Debut/Impulse/Prestige/Booster/Ella y fallaba EN SILENCIO. -->
<!-- skill G4.19 · 2026-09-03: la doc no decia COMO correr los validadores. En G4.10 el encabezado nuevo nunca entro porque el patron buscaba 'Auto-verificacion' y el archivo dice 'Auto-verificación' CON TILDE: el reemplazo no fallo, simplemente no hizo nada, y el changelog lo dio por hecho. Ocho versiones con la doc rota. Regla nueva en 0-H: tras editar se verifica que el texto nuevo ESTA, no que el comando salio sin error. -->
<!-- skill G4.18 · 2026-09-03 (fila del CdM): la description llevaba `product.<tema>.json` y la spec de publicacion PROHIBE los angulares — no era longitud (1010 de 1024). El arreglo son dos caracteres; la causa de fondo no: esta skill validaba a fondo el product.json que PRODUCE y no se validaba A SI MISMA como artefacto publicable, aunque se publica al marketplace. La autoprueba ahora corre el validador OFICIAL de skill-creator sobre esta skill. -->
<!-- skill G4.17b · 2026-09-02: el check 27 recien horneado dio falso positivo y destapo una CLASE — la funcion de "texto visible" solo quitaba {% comment %} y dejaba pasar {%- comment -%} (con guiones) y los comentarios JS /* */, asi que los separadores que orientan a quien EDITA el codigo se leian como rayas publicadas. La usaban CUATRO checks: DEMO visible, apertura, rayas y lenguaje de tienda. Un arreglo, cuatro checks. -->
<!-- skill G4.17 · 2026-09-02: coherencia antes de repartir. Iba a salir una fila preguntando a cada fabrica si comprueba las SEIS reglas duras de la casa, y esta skill solo comprobaba DOS. Checks 27 (rayas separadoras), 28 (lenguaje de tienda) y 29 (credenciales en el entregable), los tres FALLA, cada uno con su caso bueno: una raya em en prosa es correcta, «tiendas fisicas» sin posesivo no es el vicio, y una clase CSS larga no es un token. 6 de 6 reglas duras comprobadas. 29 checks, 29/29 pruebas. -->
<!-- skill G4.16 · 2026-09-02 (FER amplia la ley a cada skill, agente y proceso): el validador NO comprobaba NINGUNA regla dura de FER — cero menciones de los signos de apertura y de los acentos en el codigo Y en la doc, mientras la nota del proyecto daba por hecho que el auto-check los cubria. Checks 25 (apertura ¿¡ en texto visible) y 26 (acentos rotos/mojibake), ambos FALLA nunca aviso, con casos en las dos direcciones: un ¿ dentro de un comentario no se publica y las tildes correctas NO son mojibake. 23/23. -->
<!-- skill G4.15 · 2026-09-02 (protocolo zanjado por el CdM): el registro de fabricas lo escribe SOLO el CdM — la fabrica sella y reporta. Un escritor unico mata la carrera de raiz. Consecuencia horneada: entre sellar y que el CdM regenere hay ventana de desfase LEGITIMA, asi que sellos.py separa BLOQUEANTE (sello y changelog, dentro del arbol, sin segundo escritor) de INFORMATIVO (el registro). Lo de fuera avisa, lo de dentro para. 19/19. -->
<!-- skill G4.14 · 2026-09-02 (0-H aplicandose a si misma, 3a vez, cazada por el CdM): sellos.py nacio SIN autoprueba el mismo dia que se consagro la ley de que todo validador se prueba. Su modo de fallo era silencioso: si un regex dejaba de casar y 'no encontre version' se tratara como 'coinciden', saldria 0 SIEMPRE. Refactorizado con revisar() separado de main() para poder probarlo sobre COPIAS temporales (nunca el registro real) + 5 casos en la autoprueba: caras iguales, registro desfasado, sello!=changelog, registro ausente y registro sin la fila. 19 de 19. -->
<!-- skill G4.13b · 2026-09-02: la cuarta cara (REGISTRO-FABRICAS.md) tiene DOS escritores — esta fabrica y el CdM. Hoy escribimos casi a la vez (el puso G4.12 mientras aqui iba G4.13) y solo el orden de llegada evito que el registro RETROCEDIERA. Documentado en sellos.py y en la regla 0-H: esa cara se MIDE al cerrar, y con mas razon cuando otro chat dice haberla corregido. Medido tras el cruce: las 3 caras en G4.13. -->
<!-- skill G4.13 · 2026-09-02 (0-H aplicandose a si misma, 2a vez): la version tiene CUATRO caras y la cuarta (REGISTRO-FABRICAS.md) vive FUERA de la skill, asi que el ritual de blindaje no la toca. Se desfaso 4 versiones, el CdM la corrigio, y VOLVIO a desfasarse en minutos con el bump siguiente: no es descuido, es estructural. Nuevo scripts/sellos.py que compara las caras y falla si divergen (respetando que GFS_VERSION es otro eje). -->
<!-- skill G4.12 · 2026-09-02 (correccion del CdM, error de IDIOMA en mi propio censo): busque "selftest" en un arsenal que nombra sus pruebas "autoprueba" y conte 2 skills donde hay SEIS (chatea-auditoria, chatea-operacion, skill-auditor, pdf-check y esta). Mismo error que la ley del grep con tilde. selftest.py -> scripts/autoprueba.py, para que el proximo censo la vea. Ademas: CASOS BUENOS en la autoprueba (disparador correcto con y sin tilde, mensaje libre a atencion) — sin ellos un check agresivo marca lo legitimo y nadie se entera. 14 de 14. -->
<!-- skill G4.11b · 2026-09-02 (el selftest cazando a su propio autor, a los dos minutos): el check 24 recien escrito daba FALSO POSITIVO porque "block" contiene "lock" como substring, y marcaba como candado cualquier id tipo `..._app_block_xxx`. Corregido a regex (?<!b)lock en el check y en el sabotaje. La leccion es la Regla 0-H entera: el validador que no se prueba miente, y el que lo escribe no es la excepcion. -->
<!-- skill G4.11 · 2026-09-02 (Regla 0-H estrenandose): el selftest recien horneado destapo un CANDADO DUPLICADO en el generador — G4.0 saco el candado del main a seccion suelta pero el bloque viejo G3.14 (1.005 bytes) se quedo activo junto a la seccion sec_lock (2.128 bytes) con contenido DISTINTO: dos fuentes de verdad para la misma regla. Fosil quitado + check 24 que lo caza + su caso en el selftest. 11 de 11 pruebas pasan. -->
<!-- skill G4.10 · 2026-09-02 (barrido del arsenal: 236 skills censadas, 38 con validador ejecutable y esta tenia 0): el auto-check dejo de ser un bloque de codigo dentro de un .md con la ruta escrita a mano y pasa a scripts/autocheck.py EJECUTABLE (23 checks, codigo de salida) + scripts/selftest.py que lo prueba contra los bugs ya pagados (patron de golden-pdf-check). En su PRIMERA corrida el selftest cazo 4 falsos positivos del propio check y un fallo real: G4.9 arreglo el mensaje de WhatsApp en el componente pero NO en product.base.json, que es lo que genera las paginas. REGLA 0-H: todo fallo pagado se convierte en check con su caso de prueba. -->
<!-- skill G4.9 · 2026-09-02 (precision del CdM + hallazgo propio): el mensaje del boton de WhatsApp NO es texto, es el DISPARADOR de Chatea y casa BYTE A BYTE (formula 'Hola quiero información y precio de <PRODUCTO>'); si no casa cae en el tablero No automatizado que nadie mira. Y el nombre del disparador es el REGISTRADO EN CHATEA, NO product.title — usar el titulo de Shopify era justo lo que rompia el byte a byte. Boton con contexto → bot; generico → atencion; ante duda, atencion. -->
<!-- skill G4.8 · 2026-09-02 (regla de FER): REGLA 0-G — canal humano siempre visible. Toda la tienda lleva WhatsApp (bot de Chatea o atencion al cliente): el TEMA lo pone en toda la tienda, la FICHA lleva el suyo con el nombre del producto en el mensaje, y NUNCA hay dos burbujas (WA_SUPRIMIR_OTRAS en el componente). -->
<!-- skill G4.7 · 2026-08-28 (fila del CdM, capacidad asimetrica): REGLA 0-F — umbral de rentabilidad ANTES de escribir la escalera de combos. La skill escribia precios con CERO menciones de breakeven mientras golden-ads lo mide en cada cuenta: un combo bajo el punto de equilibrio se descubria con la pauta ya pagada. Nuevo references/breakeven-combos.md (criterio heredado de golden-ads + aritmetica COD: flete por pedido, devolucion golpea el pedido completo) + umbral en sec-combos.liquid. -->
<!-- skill G4.6 · 2026-08-28 (cosecha de produccion): REGLA 0-E — la orden tiene que poder DESPACHARSE. Combos = variante con SKU propio, el bump SUMA CANTIDAD y ningun SKU se comparte entre productos: los sistemas COD modelan una fila por (producto,variacion) y rechazan variaciones duplicadas. Advertencia operativa tambien en sec-combos.liquid. -->
<!-- skill G4.5e · 2026-08-26 (turno concedido por el CdM, Ley del Cambio Unico): la titularidad de la fabrica se declara en el propio SKILL.md ('Fabrica: chat SKILL golden-shopify') y ya no vive solo en memoria — cierra el hueco que tenia el registro listado como fila abierta. -->
<!-- skill G4.5d · 2026-08-24 (verificador de cierre): fechas de sello corregidas con mtime MEDIDO (la ronda cruzó de día: base el 23, reestructura el 24) y el Paso 0 ya declara DÓNDE vive el cerebro (PROYECTOS/BRAND-BRAINS/<MARCA>/, resolución exacta por golden-brand-brain). Regla que deja: la fecha de un sello se MIDE, nunca se hereda del contexto. -->
<!-- DOS EJES DE VERSIÓN (no confundir, no son desincronía): (a) VERSIÓN DE LA SKILL = este sello + references/changelog.md, con sufijos a/b/c/d por ronda de auditoría; (b) GFS_VERSION = lo que se estampa en la PÁGINA GENERADA (config-center + componentes/00 + product.base.json), y solo sube cuando cambia lo que la página produce. La versión VIGENTE de cada eje se lee de su fuente, no de esta nota: la de la skill en el sello de arriba + references/changelog.md, y GFS_VERSION en assets/config-center.liquid. Al bumpear, tocar TODAS las caras del eje que cambió (y ninguna del otro). -->
<!-- skill G4.5c · 2026-08-24 (barrido D del CdM): starter Horizon _golden-trust.liquid dejó de ser huérfano (citado en horizon-bloques.md §3.1) y examples/ se movió a references/examples/ con sus 17 citas reescritas — árbol de primer nivel ya canónico. -->
<!-- skill G4.5b · 2026-08-24 (auditoría golden-skill-auditor, reparación): DEUDA CERRADA — product.base.json regenerado del orden viejo de 17 al embudo canónico de 24 (21 + 3 de sistema) con los componentes ya existentes; sellos GFS_VERSION sincronizados (estaban en 3 versiones a la vez: SKILL G4.4 / config G4.3 / base G3.14 → todos G4.5); '## Paso 0 Cerebro de marca' estaba ENCIMA del H1 → movido debajo; SKILL.md 623→491 líneas sacando el PROTOCOLO TEMA VIVO duplicado a references/tema-vivo.md y la tabla del embudo a references/embudo-canonico.md; puntero muerto a 'línea ~460' → apunta a archivo; contradicción Ignition-en-el-main corregida. Detalle en references/changelog.md G4.5. -->
<!-- skill G4.5 · 2026-08-23: Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
<!-- skill G4.4 · 2026-08-22 (auditoría golden-skill-auditor, cierre de reparación): GFS_VERSION del
config center estaba desincronizado en "G3.14" (~15 versiones atrás) → corregido a G4.3 en
assets/config-center.liquid y references/componentes/00-config-center.liquid; imagenes.md enseñaba
`{# ... #}` como convención de slot (es justo el bug que auto-check.md check #17 caza) → corregido a
`{% comment %}`; checklist-producto.md decía que Ignition vive embebido en 01-propuesta.liquid,
fósil de antes de G4.0 (ya es sec-ignition.liquid independiente) → corregido, igual que el lenguaje
"bloque 1" en auto-check.md; sistema.md le faltaban 18 de 46 componentes reales (sec-seguridad,
sec-disclaimer, sec-es-para-ti, sec-combos, sec-seo-aio-schema, sec-cta-suelto, efx-reveal-seguro,
efx-video-lazy y 10 más) → tabla completada; 08-boton-compra.liquid NO tenía el fallback real a
`/cart/add` que REGLA #2/releasit-cod.md exige y que este mismo changelog ya daba por hecho en
G4.2 → implementado de verdad (retry 1.5s + POST /cart/add.js + redirect /cart); 12-sticky-bar.liquid
tenía `aria-hidden="true"` fijo aunque el JS lo hacía visible al scrollear (CTA inalcanzable por
teclado/lector de pantalla, WCAG 2.2) → ahora aria-hidden/inert se togglean con la visibilidad real;
colisión de nombre `.gfs-why` entre sec-beneficios.liquid y sec-por-que-elegir.liquid (mismo prefijo,
marcado distinto, se pisaban si un product.json cargaba ambos) → sec-beneficios.liquid renombrado a
`.gfs-bnf`; sec-cine/sec-escalera/sec-escenas/sec-manifiesto/sec-ya-lo-intentaste reinventaban su
propio IntersectionObserver sin la red de seguridad ~1.2s de efx-reveal-seguro.liquid (si el observer
fallaba, el contenido quedaba invisible para siempre) → se les agregó el mismo patrón de red de
seguridad por tiempo; detalle completo en references/changelog.md · G4.3 · 2026-08-07 (centro de mando, cosecha del chat ESTUDIO 360 DENTAL un producto de cliente Chile): componente estándar "LO QUE ESTE PRODUCTO NO HACE" para verticales de SALUD, descrito junto a sec-disclaimer/sec-es-para-ti como obligatorio-recomendado — declara el límite del producto con honestidad (ej. "no repara una caries ya formada; sí cuida el esmalte") y convierte la objeción "es estafa" en razón de compra en categorías donde los competidores usan avales inventados y estadísticas sin estudio; el mismo mensaje se replica en pauta y en la respuesta pública de comentarios · G4.2 · 2026-08-07 (fuente: chat un producto de cliente/un producto de cliente): TOPE 50 KB por setting custom_liquid (punto 9 del RESUMEN DURO + check obligatorio en auto-check.md) + límites duros y RECETA PROBADA Horizon/Pitch (horizon-bloques.md) + fallback permanente del CTA a /cart/add si Releasit falta (REGLA #2 + releasit-cod.md) + nota [DEUDA] product.base.json en 17 vs 24 secciones; G4.1 · fix 2026-07-27: resumen del PROTOCOLO TEMA VIVO subido al tope (un chat recibió la skill truncada y trabajó sin él — lo crítico va ARRIBA); G4.0 · PERFILES (marca propia | catálogo-dropshipping) + embudo canónico de 24 secciones + bloque alternado imagen-texto + revelado seguro (el CTA nunca se oculta) + video lazy + srcset + schema SEO-AIO en sección propia; historial completo en references/changelog.md -->

> 🔒 **SKILL CANÓNICA — SOLO-LECTURA.** Estos archivos están protegidos (read-only) a propósito.
> Se pueden LEER y usar libremente, pero **NO se editan desde fuera de la "fábrica"** (el chat del
> usuario dedicado a mejorar la skill). Prohibido a otras sesiones/linters/absorciones modificarla.
> Para cambiarla: el usuario la desbloquea en la fábrica, se edita, y se vuelve a bloquear.
> **Fábrica: chat `✅ SKILL golden-shopify`** — titularidad declarada aquí, no solo en memoria
> (REGISTRO-FABRICAS.md). Solo la fábrica numera esta skill (ley del número de versión).

<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->
## Paso 0-A · QUE TEMA ES (compuerta: no se genera nada sin esto)
Esta skill construye **sobre el tema de OTRA persona**. Si se asume Dawn y la tienda corre otra
familia, lo que se entrega no encaja — y en el peor caso encaja a medias, que es peor porque parece
bien. **Antes de escribir una sola linea, el tema queda DECLARADO.** Tres vias, en este orden:

1. **MEDIRLO desde la tienda publica** (no hace falta API ni permisos: basta la URL). En el HTML de
   cualquier tienda Shopify vive `Shopify.theme`, y lo que manda es **`schema_name`**, no `name`:
   `name` es el rotulo que le puso el dueno ("Mi tienda v2") y no dice nada; **`schema_name` dice la
   FAMILIA real** aunque lo hayan renombrado.
   ```js
   // pegar en la consola de la tienda, o leerlo del HTML publico
   ({familia: Shopify.theme.schema_name, version: Shopify.theme.schema_version, rotulo: Shopify.theme.name})
   ```
2. **Por API**, si hay MCP/credencial: `{themes{nodes{name role id}}}` — y ademas el tema MAIN cambia
   entre sesiones sin avisar, asi que se relee cada vez (`references/tema-vivo.md`).
3. **Preguntarle al usuario**, si no hay ni URL ni API: *"Que tema usa la tienda? Si no lo sabes,
   mandame la URL y lo miro yo."*

**Nunca se asume Dawn.** Si las tres vias fallan, se dice en la entrega que el build se hizo a ciegas
sobre familia clasica y que hay que verificarlo antes de publicar. El reparto por familia y las
diferencias de cada una estan en `references/temas.md` (clasica: Dawn/Shrine/Sense, el product.json
pega · nueva: Horizon/Pitch, NO pega y va por bloques Custom Liquid).

## Paso 0 · Cerebro de marca (obligatorio antes de generar)
El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta de la ruta la declara
`golden-brand-brain`: ante duda de ruta, invócala en vez de adivinar.

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.


## 🚨 PROTOCOLO TEMA VIVO + MEDIA — RESUMEN DURO (leer ANTES de escribir a cualquier tema)
*Detalle completo en `references/tema-vivo.md` (si este archivo te llegó cortado, léelo del disco).*
1. **Verificar QUÉ tema es MAIN** antes de tocar nada (`{themes{nodes{name role id}}}`) — el vivo cambia entre sesiones sin aviso.
2. **Escritura**: `themeFilesUpsert` body `{type:"BASE64"}`; tras escribir, RELEER y comparar contenido. UNA sola sesión escribe por tema.
3. **Caché storefront**: la página pública puede servir el render viejo 15-60 min — verificar el ARCHIVO del tema, no re-subir a ciegas.
4. **NUNCA borrar media de producto sin inventariar referencias** (`/files/` lo incrustan plantillas, Releasit, renders); un borrado se rescata re-subiendo con el MISMO filename.
5. **Galería**: mínimo 5 imágenes 1:1; `galeria_portada_al_final` (Dawn Golden) es diseño APROBADO, no "corregirlo".
6. **CSS prohibido**: jamás `html,body{overflow-x:clip}` — mata el scroll vertical; el desborde se arregla en el elemento culpable.
7. **Releasit**: el Sticky Bar NUNCA se desactiva en el panel (se oculta por CSS) y el botón se prueba PULSÁNDOLO (abrir el modal).
8. **Media de la ficha vive en el TEMA y en la DESCRIPCIÓN del producto** (descriptionHtml) — un barrido/parche de media mira ambos. **Video de contenido: `poster` OBLIGATORIO** (sin poster + sin autoplay = recuadro en blanco que simula sección vacía) y el autoplay se comprueba con play() o teléfono real, nunca desde el panel del navegador. GIF pesado (>1 MB) → convertir a MP4 `<video autoplay muted loop playsinline>` (caso real: 23,5 MB → 3,3 MB).
9. **TOPE DURO: cada setting `custom_liquid` admite máximo 50 KB** — aplica a TODOS los temas, no solo a Horizon/Pitch. Al pasarse, el guardado revienta con *"Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"* (descubierto con `FileSaveError` en tienda real, chat un producto de cliente 2026-08-07). Medir CADA valor en **bytes UTF-8, no caracteres**, antes de entregar (verificación obligatoria en `references/auto-check.md`); si una pieza se acerca al tope, partirla en secciones más pequeñas (una sección por pieza, REGLA #5).

Sistema para generar páginas de producto Shopify de alta conversión COD. Nació
del proyecto interno "plantilla down" (tema **Dawn**) y se probó en dos productos
reales: **MARCA DEMO** (perfume, Dawn) y **PRODUCTO DEMO** (vitalidad, Shrine Pro).

**Idea central:** NO es "clonar un archivo". Es un sistema de **componentes
`custom-liquid` portables** + un **adaptador de tema** para las pocas piezas
nativas que cambian entre Dawn / Shrine / Sense. Por eso ~80% del trabajo sirve
igual en cualquier tema; solo se adapta el ~20% nativo (tickers, footer, bloques
`title`/`description`/`related-products`).

**Plantilla BASE = PRODUCTO DEMO** (`assets/product.base.json`). Es el archivo más evolucionado
del sistema (config center "PALETA & MARCA", `PRICE_CONFIG`, `RELEASIT_BUTTON_CONFIG`,
override de color Releasit con MutationObserver). Está construido sobre **Shrine Pro**;
para Dawn/Sense se adapta con `references/temas.md`. Todo producto nuevo PARTE de esta
base, sin importar el tema final.

> ✅ **`assets/product.base.json` regenerado al embudo canónico de 24 (G4.5)** — vuelve a ser la
> referencia de ORDEN ya construida, además del motor (config center, Releasit, precio).

## ⚠️ REGLA #1 — Cada página DEBE ser distinta (innegociable)
Dos productos NUNCA quedan como la misma página con otro color/fotos. La base PRODUCTO DEMO
aporta el **motor** (Releasit, precio, config center, convención), NO el **aspecto**.
El diseño visible se **rediseña por producto**: distinto orden/selección de secciones,
sección educativa única, hero distinto, tipografía por vertical, paleta propia del
producto, efectos repartidos, layouts de reseñas/FAQ variados. Antes de entregar, aplica
el **chequeo antiespejo** de `references/diferenciacion.md` (si quitando color e imágenes
se parece a una página previa, cambia al menos 3 palancas). Lo que sí se mantiene
constante: motor COD, convención de código, config-driven, reglas de oro y calidad.

## ⚠️ REGLA #2 — El botón de compra SIEMPRE sobresale (innegociable)
El botón de compra (CTA principal) tiene que ser el **elemento más visible y de mayor
contraste** de toda la página: debe destacar sobre TODOS los colores (secciones, fondos,
botones secundarios). Reglas permanentes:
- **COLOR FIJO: verde ganador `#1D9E06`** (`CTA_BG` del config center; oscuro `#157A04`).
  Es SIEMPRE este verde, en todo producto, salvo que el usuario pida otro expresamente.
  Aplica al botón principal y al sticky. (Excepción a la paleta por-producto: el resto de
  la página cambia de color según el producto, pero el CTA se mantiene en este verde porque
  es el que más convierte.)
- Más grande, peso fuerte, con su `shine sweep`/realce; el sticky inferior repite ese
  mismo color para que el cliente lo identifique al instante.
- Botones secundarios (ver más, info) en estilo discreto, jamás compiten con el CTA.
- **Chequeo de 1 vistazo:** el ojo va directo al botón de compra? Si no, súbele
  contraste/tamaño. Aplica también en móvil.
- **El CTA siempre FUNCIONA, aunque Releasit falte (regla permanente G4.2, toda página, no solo
  Horizon):** el botón de compra lleva **fallback al formulario nativo `/cart/add`**. Si Releasit
  no está presente en la página (app desinstalada, bloqueada o que no inyectó), el clic espera
  ~1,5 s por si la app inyecta tarde y luego agrega el producto por `/cart/add` y lleva al carrito.
  Antes, sin Releasit, el botón no hacía nada — un CTA muerto en la última puerta. Detalle e
  implementación en `references/releasit-cod.md`.

**CTA verde vs WhatsApp verde (resuelto):** el CTA es verde ganador `#1D9E06` (vivo/oscuro)
y el WhatsApp es verde `#25D366` (más claro) — son **tonos distintos** y además difieren en
forma/tamaño/posición/ícono (CTA = barra grande con texto; WhatsApp = burbuja redonda
flotante). NO se confunden. Mantener el WhatsApp siempre `#25D366` (convención) y no pegarlo
justo al lado del CTA.

## ⚠️ REGLA #3 — Nunca dejar vacío: reseñas de ejemplo SÍ; datos de riesgo se confirman (innegociable)
La página SIEMPRE se entrega **llena y funcionando**. Está PROHIBIDO dejar cualquier sección o
bloque **vacío o con placeholder visible** (`[RATING]`, `[N] reseñas`, "sé el primero", arrays
vacíos, `0.0/5`). Nada en blanco llega al cliente.

**MATIZ PAUTA (2026-07-29, gaceta 4f punto 3):** en fichas que reciben pauta, el rating/reseñas del
display propio SE QUEDAN (doctrina de FER), pero JAMÁS: porcentajes tipo "X% de usuarias/satisfacción"
presentados como dato de estudio, testimonios quemados en IMÁGENES con nombre/estrellas, ni atribución
a terceros ("verificado por Google/nadie externo").

**Reseñas y rating (cuando el cliente NO los tiene todavía) → INVENTAR ejemplos buenos:**
- 5–6 reseñas variadas, con **nombres locales** y **alguna de 4★** para que se vean creíbles.
- Un **rating creíble** (ej. `4.8 · 127 reseñas`).
- TODO marcado en comentario como `EJEMPLO — reemplazar por reales`, para que el cliente los
  cambie cuando tenga los suyos. Nunca se deja la sección de reseñas vacía ni el rating en placeholder.

**Honestidad SOLO en datos de riesgo legal** — estos se **CONFIRMAN, no se inventan** como reales:
- **Precios, descuentos, `compare_at_price`** (se leen del producto; no hardcodear).
- **Tiempos de entrega** (dependen del país — ver `paises-entrega.md`).
- **Claims médicos / resultados / certificaciones / INVIMA / ingredientes.**
- **Specs duras** (mAh, voltajes, medidas, materiales) — ej. la `sec-ficha-tecnica`.
Para estos: preguntar de forma concreta y, mientras falte, dejar un placeholder evidente
(`[confirmar]`) **solo en ese dato puntual** — nunca un número de riesgo que parezca real.

La línea es clara: las **reseñas de ejemplo** no son un riesgo legal (se marcan reemplazables);
los **datos de arriba** sí lo son. El **JSON-LD `aggregateRating`** (lo que Google indexa) se
mantiene condicional al conteo REAL — los ejemplos de reseñas son solo visuales en la página,
no se inyectan como estructura a Google (fix de G2.2).

## ⚠️ REGLA #4 — Completitud: NUNCA entregar algo mediocre o incompleto (innegociable)
El usuario parte normalmente DE CERO y quiere una plantilla **hiper ganadora**, no una ficha.
Toda página entregada DEBE traer **TODO el sistema** — todos los bloques y secciones que
manejamos — sin que falte ninguno. La variación (REGLA #1) está en el **orden, estilo,
layout y copy**, NUNCA en quitar piezas de conversión.

**Set mínimo OBLIGATORIO en cada página** (presentación distinta, pero presentes siempre):
config center · propuesta/hero · título · oferta · **countdown real** (evergreen ~15 min) ·
**verificado/rating lleno** (ejemplo reemplazable si no hay real — REGLA #3) · **precio dinámico** ·
botón Releasit (motor, oculto) · **CTA verde + doble CTA** · **garantía COD en humano** · barra
logística (país correcto) · descripción · **sticky** · sección educativa propia del producto ·
**escalera de venta / demo** · **reseñas llenas** (5–6, ejemplos reemplazables si no hay reales) ·
manifiesto (si aplica al arquetipo) · FAQ · **por qué elegir?** · **banda de autoridad** ·
ficha técnica (en gadget/kit) · tickers · **botón flotante WhatsApp** · sello + nota interna.
(Ver checklist de página ganadora en `references/arquetipos.md` y `references/checklist-producto.md`.)

- Los **arquetipos** cambian el ÉNFASIS y el orden, no si los bloques existen. "Salud lean"
  = estilo sobrio, NO = página incompleta.
- **Prohibido** declarar una página "lista/100" si le falta cualquiera de estos elementos o
  si no la viste renderizada (Regla 0 / render visual).
- Si algo no aplica de verdad a ese producto, **dilo explícitamente** ("omito X porque…"),
  no lo dejes faltando en silencio.

## ⚠️ REGLA #5 — Bloques independientes y apagables; nada abierto (innegociable)
Mucha gente que usará la plantilla NO sabe editar código. Por eso:
- **Cada efecto/función = SU PROPIO bloque.** Prohibido meter 2-3 cosas en un solo bloque
  (ej. el viejo "propuesta" traía hero+ignition+header+cart+SEO → se separó en 5 bloques).
  Así cada uno se **apaga/prende solo** desde el editor de Shopify (el "ojo" del bloque).
- **Nada de bloques "abiertos"** que el usuario tenga que rellenar con Liquid/HTML o "pega tu
  video aquí". Todo bloque llega **funcionando y completo**. Si se necesita un video/imagen,
  usar una **sección NATIVA del tema** (que cualquiera sabe usar), NUNCA un slot de código.
- **El intro IGNITION** es bloque propio, **apagable**, y **distinto en cada página**
  (cinematográfico, 100% CSS) — ver `references/ignition-variantes.md`. Nunca el mismo dos veces.
- Al construir, numera y nombra los bloques claro para que el usuario los identifique y togglee.

## ⚠️ REGLA #6 — Ninguna animación puede esconder lo que vende (innegociable, G4.0)
Aprendido en producción: una página con revelado al scroll dejó secciones enteras invisibles
porque el `IntersectionObserver` no disparó, y el cliente se quedó mirando huecos en blanco.
- **El botón de compra, el sticky y las imágenes NUNCA entran en el revelado.** Van marcados
  con `!important` fuera de la animación. Si todo lo demás falla, el cliente igual puede comprar.
- **Toda animación de entrada lleva red de seguridad por tiempo:** a los ~1.2 s, lo que no se
  haya revelado se fuerza visible. Nunca se depende solo del observer.
- **Sin JS, la página se ve completa.** El revelado es opt-in por una clase en `<html>` que
  pone el propio script; si el script no corre, no se oculta nada.
- Mismo principio que la salida del Ignition (nunca solo-CSS) y que el sticky anclado al `<body>`.
Motor listo en `componentes/efx-reveal-seguro.liquid`. Ninguna página nueva escribe su propio
revelado: usa ese.

## Modo landing sin distracciones (recomendado para COD)
Para que el visitante no se vaya y solo pueda comprar, **ocultar el menú del header y el
footer** en la página de producto (solo en el PDP, no en toda la tienda). Usar
`componentes/landing-sin-distracciones.liquid` (oculta menú/header/footer, desactiva el
link del logo al home, y oculta el "Ir directamente al contenido"). Útil sobre todo
cuando el home aún no está configurado. Nota: el "skip to content" solo lo ve quien
navega con teclado/editor, no el cliente con mouse.

## Cuándo usar cada modo

1. **Producto nuevo desde cero** → clonar un ejemplo base y rellenarlo.
2. **Adaptar la página de un cliente** que ya viene en otro tema → detectar el
   tema, conservar lo suyo, inyectar/ajustar nuestros componentes.
3. **Solo recolorear / cambiar marca** de una plantilla existente.
4. **Agregar UN componente** (countdown, garantía, etc.) a una página existente.
5. **Actualizar una página a la versión actual** (upgrade pass) — ver abajo.

Pregunta al usuario qué modo necesita si no es obvio.

## Modo actualización (UPGRADE PASS)
Para poner al día un `product.json` ya generado (*"actualiza este JSON a la última versión"*):
leer su sello `GFS_VERSION` → diff contra la skill → aplicar solo lo que falta sin romper lo
que sirve → subir el sello → entregar un solo archivo. **Pasos detallados en `references/operacion.md` (A).**

## Preguntas iniciales (pedir SIEMPRE antes de construir)

1. **Tema** de la tienda — 2 familias (adapto TODO el código al que indiques):
   - **Clásica (product.json pega):** Dawn · Shrine / Shrine Pro · Sense.
   - **Nueva (product.json NO pega → bloques Custom Liquid sueltos):** Horizon · Pitch.
   - Otro → fallback genérico. Detalle y reglas por tema en `references/temas.md`.
2. **PERFIL — marca propia o catálogo público?** (CRÍTICO, define secciones y tono):
   - **`marca`** → el producto es tuyo o de un cliente con marca real. Entran manifiesto,
     historia/origen y línea de productos. Vendes identidad y recompra.
   - **`catalogo`** → viene de un catálogo público (Dropi y similares) y otras tiendas
     venden lo mismo. La **escalera de combos es obligatoria**, la demostración es la
     protagonista, y aplican las reglas de copy de dropshipping (nunca "original"/"réplica").
   Si no lo dice y no se deduce, **pregúntalo**. Detalle completo en `references/perfiles.md`.
3. **Producto**: nombre + **URL** (ver regla "La URL es CONTEXTO" abajo).
   Pregunta también: **la URL es tu tienda o es una referencia/competencia?** (cambia el
   anti-duplicado).
4. **PAÍS de venta** (CRÍTICO — define los tiempos de entrega de la landing).
   Guatemala / Colombia / otro. Ver `references/paises-entrega.md`. Si el país no
   está en la tabla, **pregúntale al cliente** los tiempos reales. NUNCA poner fechas
   de un país en otro (ej. no usar los 1-4 días de Guatemala para Colombia).
5. **Colores**: pregunta si el cliente tiene color de marca.
   - Si lo tiene → úsalo de `primary` y deriva dark/bright/light.
   - Si NO, o pide recomendación → **recomienda tú** un color enfocado al producto:
     el que más vende / más persuade / más genera impulso de compra para ese vertical
     (ver `references/colores-conversion.md`). Propón 1 recomendado + 1 alternativa.
6. **Modo de pago**: `ambos` (default) / `contraentrega` / `anticipado`.
7. **WhatsApp**: número con código de país — se integra al **botón flotante de WhatsApp**
   (`componentes/whatsapp-flotante.liquid`) y al config center.
8. **Reviews** (cantidad + rating) si los tiene.
9. **Imágenes — PREGUNTAR SIEMPRE: CON o SIN generación?** (define todo el flujo de assets)
   - **CON generación:** genero imágenes reales con **Nano Banana Pro** (Gemini API key,
     modelo `gemini-3-pro-image`), optimizo a **<300 KB**, las subo a Shopify Files por API y
     las dejo en **bloques de la landing + galería/multimedia del producto**.
   - **SIN generación (el cliente ya tiene imágenes):** pedir las **URLs/links** o **reutilizar
     la galería/multimedia del producto**. No tocar la descripción.
   - Si pide generar y NO hay API/herramienta conectada → avisar en 1 línea y seguir con slots.
   - El **producto REAL nunca se inventa** (REGLA #3): el frasco se *compone* desde su foto real.
   Pipeline completo + troubleshooting en `references/imagenes.md`.

Si falta alguno de estos datos, **pregúntalo explícitamente** antes de construir.

## Workflow

### Paso 0 — PLAN DE DIFERENCIACIÓN (obligatorio, ANTES de escribir JSON)
Para que cada producto tenga su propia cara (REGLA #1), antes de construir **declara
explícitamente** este plan y muéstralo en una línea por punto:
- **Arquetipo** elegido (A Perfume / B Salud lean / C Vitalidad full) y por qué encaja.
- **Orden y selección de secciones** (distinto del flujo por defecto cuando se pueda).
- **Hero** (image_banner / propuesta full / título XXL / otro).
- **Sección educativa** específica de ESTE producto (pirámide / cómo actúa / comparativa /
  antes-después / pasos / ingredientes…).
- **Pairing tipográfico** (según vertical, ver `efectos-premium.md`).
- **Set de efectos** que SÍ se usan (no meter siempre los mismos).
- **Color primario + color del CTA** (justificado por conversión, REGLA #2).

Reglas del plan:
- **Compara contra los ejemplos** (`references/examples/demo-dawn-v2.json` ⭐ la plantilla PRO recomendada,
  `references/examples/demo-shrine.json`, `references/examples/demo-dawn.json`)
  y contra cualquier página que el usuario te muestre o que esté en
  `~/.claude/SHOPIFY BY CLAUDE/PLANTILLAS/`. El plan DEBE divergir de ellas.
- Si construyes **varios productos en una misma sesión**, cada plan debe pulsar **palancas
  distintas** a los anteriores (no repetir arquetipo+orden+hero idénticos).
- Si el usuario arma productos en chats separados, **pídele** (o revisa en PLANTILLAS) las
  páginas previas para no repetirlas.
Solo después de fijar el plan, sigue al Paso 1. Ver `references/diferenciacion.md`.

### Paso 0.0 — La URL es CONTEXTO, NO tu página (clave)
Cuando el usuario manda una URL, **no asumas que es suya ni que es el diseño a copiar**.
Puede ser **su tienda, la de un competidor, o solo una referencia** para que entiendas el
producto. Úsala SOLO para extraer **contexto del producto**: qué es, para qué sirve,
beneficios, ingredientes, público, objeciones, ángulo de venta → para **adaptar el copy** con
información real (apoya la REGLA #3 anti-invención).
- **NUNCA** clones el diseño de esa URL, ni limites/bajes la calidad de la plantilla a lo que
  esa página tenga. Tú construyes **desde cero** una plantilla completa y ganadora (REGLA #4).
- **NUNCA** copies reseñas/claims de un competidor como si fueran del usuario.
- Si es competencia, además sirve para **diferenciarte y superarla**, no para imitarla.

### Paso 0.1 — Anti-duplicado (solo si la URL ES la tienda del usuario)
Si la URL **es del usuario** y su descripción nativa YA trae landing completo (hero,
comparativas, "cómo usar", reseñas, garantía), **no dupliques** ese contenido: cambia el
ángulo o desactiva esa sección nuestra; reseñas propias = personas distintas. Si la URL es
**referencia/competencia**, esto no aplica: construyes la página completa desde cero.

### Paso 1 — Partir de la base PRODUCTO DEMO y adaptar al tema
SIEMPRE parte de `assets/product.base.json` (la base PRODUCTO DEMO, la más completa). Luego:
- Tema **Shrine / Shrine Pro** → ya estás en el tema nativo de la base, sigue directo.
- Tema **Dawn** → aplica el adaptador de `references/temas.md` (tickers→custom-liquid,
  footer `.footer`, quita settings Shrine-only). Usa `references/examples/demo-dawn.json`
  como referencia viva de cómo queda en Dawn.
- Tema **Sense / otro** → como Dawn, + fallback genérico de `temas.md`.

Lee `references/temas.md` para saber exactamente qué cambia entre temas.

### Paso 2 — Config center + recolorear (TOKENIZADO)
Inserta el **config center** como primer bloque del main (`BRAND_NAME`, colores `BRAND_*` +
`*_RGB`, `CTA_BG`, WhatsApp, reviews). **Recolorear = cambiar esas variables** (los componentes
leen `var(--brand-*)` / `var(--cta)` del `:root`; sin search-replace). CTA fijo `#1D9E06`.
Recalcula los `*_RGB` al cambiar un color. Detalle y tokenización de páginas viejas en `references/sistema.md`.

### Paso 3 — Config-driven blocks
Ajusta los bloques que SÍ tienen config propia:
- **Precio** → `window.PRICE_CONFIG` (`06-precio-dinamico.liquid`).
- **Botón Releasit + sticky** → `window.RELEASIT_BUTTON_CONFIG` (override de
  colores de los botones de la app). Ver `references/releasit-cod.md`.
- **Garantía / Compra Segura** → variable `MODE` = `ambos|contraentrega|anticipado`.

### Paso 4 — Contenido por producto
Antes de escribir copy, lee `references/reglas-de-oro.md` (copy emocional COD, qué
NUNCA decir en perfumes/dropshipping, garantía por proceso). Para agregar o reforzar
efectos visuales, usa `references/efectos-premium.md`. Reescribe el copy específico:
- Propuesta de valor (`01-propuesta.liquid`).
- Sección educativa: "Cómo actúa" / pirámide olfativa / etc.
  (`sec-como-actua.liquid`) → **siempre se reemplaza por producto**.
- Reseñas (`sec-resenas.liquid`, array `window.GFS_REVIEWS`).
- FAQ (`sec-faq.liquid`), manifiesto, beneficios.

### Paso 5 — Activar/desactivar y ordenar
- **Countdown**: oculto por defecto (`disabled: true`).
- **Releasit COD app block**: SIEMPRE incluido pero **oculto** (`disabled: true`)
  — es el MOTOR del COD, NO se borra. Lo dispara nuestro botón custom.
- **Productos relacionados**: última posición, desactivado por defecto.
- **Compra Segura**: `MODE="ambos"` por defecto.
- Numera bloques (1..N) y secciones (1..N) consecutivos.

### Paso 6 — Entregar UN solo archivo
Entrega un único `product.<slug>.json` (o `product.<slug>.<tema>.json`). **Regla
del usuario: un solo archivo por producto.** No crear variantes `.MEJORADO`,
`.LEAN`, etc. Si pide cambios, editar el mismo archivo y reentregar.

Antes de entregar: corre la **auto-verificación** de `references/auto-check.md` (script que
atrapa JSON roto, color viejo, rating 0.0, sin sello, sin Ignition, sin Releasit) **y** la
**checklist** de `references/checklist-producto.md`. No declares la página lista si algo falla.

## Convención de código en cada bloque (mantener SIEMPRE)
Cada bloque `custom-liquid` separa lo editable de lo que no se toca:
```liquid
{% comment %} 📝 EDITAR AQUI {% endcomment %}
{% assign VARIABLE = "valor" %}
{% comment %} ═══ ↓ NO TOCAR DE AQUI HACIA ABAJO ↓ ═══ {% endcomment %}
<style>...</style><div>...</div>
```
Cualquier bloque nuevo sigue este patrón. El usuario edita arriba; el motor vive abajo.

> ⚠️ **REGLA DE INGENIERÍA (innegociable):** antes de escribir CUALQUIER bloque o sección,
> cumple **`references/estandares-liquid.md`** — código **sano** (scope con prefijo único BEM +
> tokens de la Paleta con fallback, nada hardcodeado), **accesible** (WCAG 2.2: roles/ARIA, foco,
> contraste, `alt`, labels, `aria-live`) y **rápido** (`content-visibility`, `lazy`+dimensiones sin
> CLS, animar solo `transform`/`opacity`, `prefers-reduced-motion`, JS vanilla con progressive
> enhancement). Ningún bloque se entrega sin pasar su **checklist "código sano"**. Para **temas
> Horizon o tiendas nuevas**, consulta además **`references/horizon-bloques.md`** (arquitectura
> block-based + theme blocks nativos).

## Estructura canónica = EMBUDO CON RITMO (G4.0 — 24 secciones, 4 puertas, PAS)
La página NO es una lista de secciones: es un **embudo con ritmo** donde cada fase pide la venta.
**24 = 21 secciones del embudo + 3 de sistema** (candado, ignition, WhatsApp: overlays `position:fixed`,
su orden no afecta al layout). **4 puertas de compra:** HERO (CTA#1) · tras el dolor (CTA#2) ·
pico de convicción (CTA#3) · cierre (CTA final). Blueprint de neuroventa: `references/reglas-de-oro.md` (Regla 0-A).

> 📖 **Tabla fila por fila, perfiles (`marca` | `catalogo`), estado por defecto y cadencia de CTA:**
> **`references/embudo-canonico.md`**. Ese orden ya viene CONSTRUIDO en `assets/product.base.json`.

## PLAYBOOK DE GENERACIÓN (0 → 1000) — la receta para una página PERFECTA
No entregues un esqueleto con copy demo. Una página 1000 tiene TODO el copy escrito para ESTE
producto y coherente de arriba a abajo. Sigue estos pasos SIEMPRE:

**Paso 0 · Datos reales primero (nunca inventar — REGLA del usuario).** Antes de generar, ten:
nombre del producto, forma (spray/gotero/crema/parche…), ingrediente/USP estrella, precio y precio
tachado, WhatsApp real con código de país, país (tiempos de entrega), rating+nº reseñas, y si tiene
o no aval legal real. Si falta algo que cuesta render o es un claim, **PREGUNTA** (no inventes).

**Paso 1 · Centro de control (PALETA & MARCA).** Cambia BRAND_NAME, los 4 colores de marca
(BRAND_PRIMARY/DARK/BRIGHT/LIGHT + sus RGB), WHATSAPP_NUMBER real, REVIEW_COUNT y RATING_VALUE.
El CTA se queda VERDE (Regla #2). Toda la página hereda estos tokens.
⚠️ **OJO con los textos que NO son `{% assign %}`:** el botón Releasit (`RELEASIT_BUTTON_CONFIG.text`)
y el sticky traen el nombre del producto **dentro de un objeto JS** (ej. "QUIERO MI PRODUCTO DEMO").
Reescríbelos con el nombre real o quedan como fósil demo (el auto-check #18 lo caza).

**Paso 2 · Reescribe el copy de CADA sección para el producto** (cero copy demo — auto-check lo caza):
- **Tickers:** 3 beneficios COD/producto por ticker (envío gratis, contra entrega, USP). Nada de
  "energía/vitalidad"; nada que el producto NO haga (ej. "lunares" si no trata lunares).
- **Hero:** badge-gancho + subtítulo con la promesa y la USP ("con [ingrediente estrella]…").
- **Te suena / Ya lo intentaste:** 4 escenas del dolor real + 4 alternativas que ya falló (PAS).
- **Cómo actúa:** 3 pasos con el VERBO correcto de la forma (spray→rocía) y la USP en el paso 2.
- **Escalera:** 5 paneles problema→solución→beneficio→USP→resultado. Kickers variados (no repetir).
- **Cine:** 3-4 líneas de future-pacing ("imagina…") + CTA.
- **Reseñas:** 3-6 testimonios CREÍBLES con nombre, específicos del producto (nunca vacío — inventa
  ejemplos buenos si no hay reales, y ponlos a reemplazar).
- **Timeline:** qué esperar por etapas, realista ("varía según la persona").
- **Es para ti:** 4 SÍ + 4 "consulta antes" (incluye lo que NO trata → baja devoluciones + da confianza).
- **Por qué elegir / FAQ / Manifiesto:** comparación, 5 objeciones reales, cierre emocional identitario.
- **Disclaimer:** cosmético/legal. Claims (INVIMA/registro) solo si son REALES; si no lo necesita,
  enfoque positivo ("por sus características no requiere registro"), nunca "no tiene registro".

**Paso 3 · Imágenes — golden-shopify es el CEREBRO (ver `references/imagenes-orquestacion.md`).**
Tú decides el plan visual y **repartes** cada pieza al generador correcto (no las generas aquí):
- **Infografía (foto real + texto de venta) → `golden-imagen-arena`** (MCP de Higgsfield por API; SOLO imágenes).
- **GIF / video / demo / persona → `golden-ugc-avatar`** (Higgsfield).
- **Foto photoreal / escena sin texto → Nano Banana** (pipeline de `imagenes.md`).
Produce un **BRIEF VISUAL** (tabla: slot · ubicación · formato · generador · foto fuente · TEXTO dentro ·
propósito), confirma el set con el usuario (cada pieza gasta créditos de Higgsfield) e invoca la skill
generadora con SUS filas — ella sabe CÓMO, tú le das el QUÉ. Formatos: galería **1080×1080**,
descripción **solo 1-3** infografías **1080×1350**, escalera `P#_IMG` **1:1**, cine fondo **16:9**/video.
Escalera y Cine usan **URLs NUEVAS**, nunca las infografías de la descripción (se duplicarían). El resto
de la venta = **bloques nativos** (SEO + editable + liviano). WebP <150KB, con width/height + alt (sin CLS).

**Paso 4 · Coherencia de producto (Regla 0-C).** La forma manda el verbo en TODAS las secciones;
la USP lidera el mecanismo; no vender lo que no trata; un solo WhatsApp; claims solo si reales.

**Paso 5 · Cierre.** Corre `references/auto-check.md` (JSON válido, cero fósiles, candado, FAQ a11y,
relacionados off, sin fugas `{# #}`). Luego **RENDER REAL** (subir a tema no publicado + screenshot
móvil Y escritorio) antes de decir "listo". Nunca "1000/1000" sin verla con ojos.

## Sello de versión + NOTA INTERNA (OBLIGATORIO en cada página)
Cada página lleva: (1) **sello arriba** en el config center (`GFS_VERSION` + comentario HTML
con versión/marca/fecha) y (2) **nota interna al FINAL** (comentario HTML invisible con la
fecha y hora REALES de generación, fijas, dentro del último bloque — NUNCA tras el `}` final).
**Formato exacto y reglas en `references/operacion.md` (B).**

## PROTOCOLO TEMA VIVO + MEDIA — version completa
El **resumen duro de 9 puntos esta al inicio de este archivo** (obligatorio antes de escribir a un tema).
Detalle completo, con el porque de cada punto y los casos reales: **`references/tema-vivo.md`**.

## Auto-mejora — RITUAL DE ABSORCIÓN
Cuando el usuario diga *"absorbe las mejoras de esta página"* o pegue un `product.json` que le
gustó: parsear → diff contra base+componentes → extraer lo nuevo/mejor como componente → subir
versión en `changelog.md` → confirmar en una línea. **Nunca degradar, un componente por función,
y NUNCA reintroducir nombres reales** (usar descriptores de categoría; la skill es anónima).
**Pasos detallados en `references/operacion.md` (C).**

## Archivos de esta skill
- `references/breakeven-combos.md` — **Regla 0-F: umbral de rentabilidad ANTES de escribir la escalera de combos (criterio de golden-ads + aritmetica COD)**
- `references/reglas-de-oro.md` — copy/legal + 12 reglas de oro + tabla de errores
- `references/perfiles.md` — G4.0: los 2 perfiles (marca propia | catálogo-dropshipping): qué secciones entran en cada uno, qué tono y
- `references/diferenciacion.md` — REGLA #1: palancas para que cada página sea distinta + chequeo antiespejo.
- `references/ignition-variantes.md` — REGLA #5: intro Ignition distinto por página (8 variantes CSS).
- `references/arquetipos.md` — 3 arquetipos de página + matriz de componentes por vertical.
- `references/paises-entrega.md` — tiempos de entrega por país (Guatemala/Colombia)
- `references/colores-conversion.md` — cómo recomendar el color que más vende por vertical.
- `references/estandares-liquid.md` — ESTÁNDARES DE CÓDIGO LIQUID (original): arquitectura section/block/snippet + schema, CSS BEM/tokenizado c
- `references/horizon-bloques.md` — arquitectura block-based del tema HORIZON (theme blocks nativos, `@theme`/`@app`, `block.shopify_attribut
- `references/rendimiento.md` — velocidad de carga: fuentes, imágenes, JS, CSS + checklist
- `references/imagenes.md` — imágenes: producto real (lo da el usuario) vs infografías-en-HTML vs decorativo-IA; hosting en Shopify; s
- `references/imagenes-orquestacion.md` — CEREBRO de imágenes: reparto golden-imagen-arena (infografías) / golden-ugc-avatar (video/GIF) / Nano Ban
- `references/sistema.md` — el sistema de componentes + estado del config center.
- `references/temas.md` — adaptador Shrine (base PRODUCTO DEMO) → Dawn / Sense / fallback.
- `references/releasit-cod.md` — override de botones Releasit, MODE, MutationObserver.
- `references/efectos-premium.md` — catálogo de snippets (3D, glass, partículas, manifiesto, tilt, contadores).
- `references/checklist-producto.md` — checklist final antes de entregar.
- `references/auto-check.md` — auto-verificación ejecutable de cierre (script)
- `references/changelog.md` — historial de versiones / mejoras absorbidas.
- `references/operacion.md` — detalle de: modo actualización (A), sello + nota interna (B), ritual de absorción (C).
- `references/componentes/*.liquid` — cada componente real, listo para pegar
- `assets/product.base.json` — PLANTILLA BASE (PRODUCTO DEMO), el master a clonar.
- `assets/config-center.liquid` — el bloque config center para insertar.
- `assets/related-products.premium.css.txt` — CSS premium para featured-collection.
- `references/examples/demo-dawn-v2.json` — ⭐ PLANTILLA PRO v2 (Dawn) — la referencia recomendada: embudo
- `references/examples/demo-dawn.json` — referencia previa de adaptación a Dawn (v1).
- `references/examples/demo-shrine.json` — copia de la base en Shrine Pro.

## Roadmap v2 (fuera de v1, no implementar salvo que lo pidan)
- **Trust badges** como fila de sellos reutilizable.
- **TICKER_CONFIG** para parametrizar textos de los tickers.
- **Tema "Golden"** (custom, en desarrollo) — documentar sus selectores cuando exista.
- ✅ ~~Tokenizar colores~~ HECHO en v1.14 (recolorear = cambiar variables del config center).

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Construye, adapta y recolorea páginas de producto Shopify de alta conversión para venta CONTRA ENTREGA (COD con Releasit COD Form) y/o pago anticipado. Plantilla base = PRODUCTO DEMO (el build más completo, sobre Shrine Pro), adaptable a Dawn ("plantilla down", el tema que se enseña/regala), Sense y cualquier tema (la mayoría de bloques son custom-liquid y portables). Trabaja con DOS PERFILES sobre un mismo motor: "marca propia" y "catálogo/dropshipping". Úsala SIEMPRE que el usuario quiera: crear o mejorar una landing/página de producto, armar un product.json o product.<tema>.json, adaptar una página de un cliente a otro tema, cambiar la marca/colores de una plantilla, agregar countdown, sticky bar, garantía, barra logística, reseñas, FAQ, manifiesto, combos/bundles, pirámide/"cómo actúa", precio dinámico, botón Releasit, o resolver dudas de carrito/Releasit/COD. También cuando venda un producto de Dropi o de catálogo público y necesite diferenciarse por oferta y por página. Dispara aunque no digan "plantilla down": basta con "página de producto", "landing de producto Shopify", "tema Dawn/Shrine/Sense", "contra entrega", "Releasit", "COD", o que peguen un product.json con bloques custom_liquid. NO usar para análisis de anuncios ni temas no-Shopify.

