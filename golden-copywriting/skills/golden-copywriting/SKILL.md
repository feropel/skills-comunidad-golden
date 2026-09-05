---
name: golden-copywriting
description: >-
  Golden Group — Copywriting de respuesta directa para TODOS los canales: anuncios de Meta
  (Facebook e Instagram), TikTok Ads, y mensajes orgánicos para WhatsApp, Facebook e
  Instagram. Escribe hooks, primary text, headlines, descripciones, guiones de video (UGC y
  TikTok), captions y secuencias de mensajes, con ángulos de venta, frameworks probados
  (AIDA, PAS, BAB, 4U) y tono LatAm que convierte tanto en contra entrega como en pago
  anticipado. Úsala SIEMPRE que el usuario quiera: escribir o mejorar copy de anuncios,
  hooks, textos para Meta o TikTok, guiones de reels o UGC, captions para redes, mensajes de
  WhatsApp u orgánicos, "hazme el copy de", "dame ángulos de venta", "ganchos para este
  producto", "textos para vender X". Aplica a cualquier producto y país. Trae el estándar
  MEDIDO de largos de Meta (125/40/25, bimodal, ventana visible de 125) y una bitácora de
  tendencias que se refresca cada 8 días, así que sirve también para "cuántos caracteres
  debe tener" y "qué copy funciona ahora".
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 999 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare · (4) Esta skill estaba SIN BLINDAR: se le puso 'uchg' y se comprobo que el candado muerde. Para editarla: chflags -R nouchg <ruta>, y al cerrar chflags -R uchg.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden Group — Copywriting Multicanal
<!-- skill GCW1.6.0 · 2026-09-01 (corrida 5 de copywriting-tendencias-8-dias) · TRES cambios de base y UNA corrección grande. (1) SE REFUTA el titular de la corrida 4: el "hueco estructural de la API de lectura" era TRANSITORIO — GOLDEN CP6 pasó de 0% a 98,8% de cobertura y BLUE CP1 de 4,7% a 99,8% con el mismo método ocho días después; la regla de cuadrar cobertura NO se deroga, se refuerza a chequeo de cada corrida. (2) SUBE A LA BASE: WhatsApp le gana a SHOP_NOW con el mismo texto byte por byte, 1,7x-2,3x, TRES mediciones independientes (29 vs 16 vs 12 compras la última, mapeo creativo→anuncio verificado con ads_get_creative_ads). (3) SUBE A LA BASE: la oferta logística va al TÍTULO, no forzada en los 125 — 0 de 5 cuerpos del mercado la meten en 125, 4 de 5 la ponen en título o descripción. (4) Se retira "cabe en 40 = 79-87% estable" que afirmó la corrida 4: el rango real de cinco corridas es 79-93%; lo que aguanta es el enunciado, no la cifra. Hallazgo limpio nuevo: el emoji del título va al principio o al final, NUNCA en el medio (66 de 66). Censo de cuentas: 76 (eran 74). Cita nueva del artículo canónico 223409425500940 que respalda el 5+5+5 con opciones cargadas por el anunciante, y hueco declarado: placement asset customization no está en la skill. -->
<!-- skill GCW1.5.0 · 2026-08-27 (chat FILTRO) · NUEVO references/anatomia-del-hook.md. ORIGEN: 00_CONTEXTO_MAESTRO.md del Agente Generador de Hooks v1.3 que trajo FER. HUECO MEDIDO: golden-ads ya sabe MEDIR el hook (17 menciones de hook rate, 15 de hold rate) pero ESTA skill, que los escribe, tenia 0 menciones de scroll-stop, snapback, context lean, trigger words, la regla de los 3 segundos y el 85% sin sonido. Se trajo el METODO, NO el pipeline de video del documento (Gemini+Seedance+ElevenLabs, ~1.52 USD/set): no esta instalado y duplicaria golden-imagen-arena, golden-ugc-avatar y golden-video-editor. Conecta con Andromeda: 4 hooks del mismo angulo con otras palabras cuentan como UNO para Meta. -->
<!-- skill GCW1.4.0 · 2026-08-25 (corrida 4 de copywriting-tendencias-8-dias): la lectura por API NO cubre el gasto de la cuenta (GOLDEN CP6 y BLUE CP5 devuelven vacío con gasto real; BLUE CP1 al 4,7%) → regla nueva de cuadre de cobertura en estandar-meta-medido.md; se corrige la afirmación de 3 corridas de que la media del título era estable (lo estable es "cabe en 40", 79-87%); dos citas oficiales nuevas (la descripción de 25 es para info NO esencial; el generador de variantes de Meta soporta español); el banco de pruebas del reparto 2+3 se apagó. -->
<!-- skill GCW1.3.9 · 2026-08-24 (centro de mando, remediación del verificador de cierre): línea de RUTA del cerebro en el Paso 0 (las lectoras ordenaban LÉELO PRIMERO sin decir dónde — un chat limpio no podía ejecutar la orden) + bump que las ediciones del 23-24 dejaron sin subir. -->
<!-- GCW1.3.8 — 2026-08-24 · Barrido total del arsenal (pluma delegada del CdM). POLÍTICA DE BLINDAJE DECLARADA: esta skill va SIN BLINDAR (sin uchg, chmod 644) por decisión del CdM — la tarea copywriting-tendencias-8-dias le escribe cada 8 días y el flag venía produciendo el ciclo documentado en la bitácora (corridas encontrándola desblindada, choque de dos manos el 21-ago). La protección es la regla de manos autorizadas, no el flag. Se encontró blindada en 5 de 6 nodos contra esa política → liberada. Además: aviso DATO LOCAL agregado al puntero de tendencias-vivas.md (el rótulo existía solo dentro del archivo — quien empaque la skill leyendo SKILL.md no se enteraba de excluirlo), typo "premita"→"premia" y mini-índice en estandar-meta-medido.md, ruta de la fuente Panamá precisada en la referencia externa. tendencias-vivas.md NO se tocó (DATO LOCAL: solo la tarea de 8 días escribe ahí; su encabezado "¿Argumento en 125?" viola la regla de la casa de signos de apertura — queda reportado para que la próxima corrida lo corrija). -->
<!-- adenda 2026-08-23 (centro de mando, hallazgo del chat FILTRO DE HERRAMIENTAS): 7 de 12 skills de contenido no leian el cerebro de marca — esta entra a la familia que SI lo lee. Bloque identico en las 6 del CdM + fila a la fabrica de golden-web. Caso origen: carrusel HUSK 'every other skill reads this first'. -->
<!-- GCW1.3.7 — Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

## Paso 0 · Cerebro de marca (obligatorio antes de generar)

Si la marca tiene CEREBRO creado por `golden-brand-brain` (marca.md, productos.md, avatares.md,
competidores.md, anuncios-ganadores.md, cambios-recientes.md), LÉELO PRIMERO y genera con esa voz
— jamás re-preguntar lo que el cerebro ya sabe. Si NO existe, ofrece crearlo con `golden-brand-brain`
antes de continuar; si el usuario pide seguir sin cerebro, se declara en la entrega que el contenido
se generó sin voz de marca cargada.



**Versión:** `GCW1.6.0` · **Fábrica: el CENTRO DE MANDO** (chat "🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR").

> 🔓 **Política de blindaje (CdM, 2026-08-24): esta skill va SIN blindar.** La tarea
> `copywriting-tendencias-8-dias` le escribe cada 8 días; el flag `uchg` solo producía choques de
> manos (ver bitácora, corridas 2 y 3). Al cerrar cualquier edición se deja `chmod 644`, sin
> `uchg`. La protección real es la regla de manos autorizadas de abajo.

> 🏭 **Quién puede editar esta skill.** No tiene chat-fábrica propio, y por la regla de la casa
> *skill sin chat-fábrica = su fábrica es el Centro de Mando*. Manos autorizadas, solo dos:
> el **Centro de Mando**, y la tarea **`copywriting-tendencias-8-dias`** como **brazo delegado**
> —la única mano automática que puede escribir aquí, siempre con el ritual completo y dejando
> parte en la bandeja del CdM.
>
> **`loop-auditoria-arsenal-golden` la LEE pero no la toca.** Cualquier otra sesión que encuentre
> algo que arreglar aquí **lo lleva a la bandeja del Centro de Mando, no lo edita**: dos manos
> editando la misma skill se pisan en silencio.

Copy que vende en LatAm por los **dos modelos de Golden**: catálogo contra entrega y marcas
propias con pago anticipado. Directo, emocional, orientado a la acción. Nada de relleno corporativo.

El cerebro vive en `PROYECTOS/BRAND-BRAINS/<MARCA>/` — la resolución exacta (buscar con find ANTES de crear, naming MAYÚSCULAS-CON-GUIONES) la declara `golden-brand-brain`: ante cualquier duda de ruta, invócala en vez de adivinar.

## Reglas de oro
1. **El hook lo es todo.** Los primeros 3 segundos / la primera línea deciden. Siempre entrega 5+ variantes de hook.
   **Y no se escriben a ojo: `references/anatomia-del-hook.md` trae el método.** Fórmula de 3 pasos
   (context lean → scroll-stop → snapback, ≤14 palabras), los 4 ángulos × 6 formatos con el default
   de COD LatAm, el banco de palabras que disparan y las prohibidas, y los 5 controles antes de dar
   un hook por bueno. Dos datos que cambian cómo se escribe: **el 85% de las vistas en Meta son sin
   sonido** (texto quemado siempre) y **ningún hook lleva CTA** — el hook abre, no cierra.
2. **Un ángulo por pieza.** No mezclar dolores. Elige el ángulo más fuerte para el avatar.
3. **Habla como el cliente, no como la marca.** Lenguaje del país, beneficios > características, prueba > promesa.
4. **CTA único y claro**, acorde al canal **y al modelo de pago** (ver la sección de abajo).
5. **Pregunta lo mínimo** (producto, país, oferta/precio, avatar/dolor **y CÓMO COBRA**) y produce.
   Si hay investigación previa, úsala.

## 💳 El modelo de pago cambia el EJE del copy (preguntarlo siempre)

No es un detalle de la ficha: decide qué objeción estás demoliendo. Golden opera los dos.

| | **Contra entrega (catálogo)** | **Pago anticipado (marca propia)** |
|---|---|---|
| Quién lee | no te conoce, nunca te compró | **ya te conoce, ya te compró o te sigue** |
| La objeción real | *"y si pago y no llega"* | *"y si no me sirve a mí"* |
| Eje del copy | **eliminar el riesgo de pagar** | **pertenencia, resultado y recompra** |
| CTA típico | "Pídelo y paga al recibir" | "Pídelo ahora" · "Vuelve a pedir el tuyo" · "Entra a la lista" |
| Prueba que pesa | que el producto llega y funciona | **testimonios de gente que repitió** |
| Escasez que funciona | unidades del lote | lanzamiento, edición, lista de espera |

> ⚠️ **El error caro: poner "paga al recibir" en una marca propia.** Ahí el cliente **ya
> confía** — recordarle que podría no pagar le **siembra una duda que no tenía**. Es hablarle
> de riesgo a quien ya decidió. El mismo copy que multiplica en catálogo, en marca propia resta.
>
> Y al revés: vender **pertenencia y recompra** a alguien que te ve por primera vez en un
> anuncio frío no significa nada, porque todavía no hay a qué pertenecer.

**Si el usuario no dice el modelo, pregúntalo antes de escribir.** Si no responde, entrega las
dos versiones del CTA y márcalo, nunca asumas contra entrega por ser LatAm.

## Guardrails de formato (obligatorios)
Reglas globales del dueño. Aplican a TODO texto que entregue esta skill.
1. **Sin signos de apertura.** Nunca `¿` ni `¡`; solo el signo de cierre (`?`, `!`).
2. **Sin líneas separadoras de rayas.** Jamás `━━━`, `---` ni `===` dentro de los copys ni entre bloques. Separar con títulos o emojis.
3. **Todo texto para copiar va en bloque de código** (con su ícono de copiar), listo para pegar sin editar.

## Guardrails de posicionamiento y compliance (obligatorios)
1. **Respetar el posicionamiento del producto que dé el usuario.** El copy no puede contradecir lo acordado. Ejemplo Le'côterra: es spray de FRESCURA (no antitranspirante), no se mencionan axilas, y los resultados son inmediatos sin prometer timelines. Si el usuario define reglas de posicionamiento, mandan sobre cualquier ángulo.
2. **Compliance Meta (atributos personales / salud).** El **texto líder** de cada anuncio debe ser aspiracional, en 1ª persona y orientado al beneficio — NUNCA un gancho acusatorio en 2ª persona ("tu zona íntima huele", "tú tienes tal problema"). Esos ganchos fuertes se permiten solo como **variantes de rotación**, jamás como líder.
3. **"Unisex sutil" cuando el producto lo pida.** Liderar por aroma o beneficio, sin gritar el género; usar frases puente que no contradigan el empaque ni el posicionamiento.

## Ángulos de venta (elige según avatar)
Dolor/miedo · Deseo/aspiración · Antes-después/transformación · Novedad/curiosidad · Prueba social/autoridad · Escasez/urgencia · Objeción-demolida · Comparación/"deja de usar X".

## Frameworks
- **PAS** (Problema → Agitación → Solución) — el caballo de batalla en **contra entrega**, donde
  hay que crear la necesidad desde cero ante alguien que no te conoce.
- **BAB** (Antes → Después → Puente) — mejor en **marca propia**: el cliente ya conoce el problema
  y a ti; lo que quiere ver es el resultado y cómo llegar, no que le agiten el dolor otra vez.
- **AIDA** (Atención → Interés → Deseo → Acción).
- **4U** para headlines (Útil, Urgente, Único, Ultra-específico).
- **Hook–Retención–Pago** para guiones de video corto.

## 🎙️ Los hooks no se inventan a ciegas: mínalos del AUDIO de lo que ya vende
Si existen videos ganadores (propios o de competidores), se transcriben EN LOCAL antes de
escribir una sola línea: los hooks validados salen de la locución real de los anuncios que ya
funcionan, no de la imaginación. Receta canónica (whisper local, gratis, sin que el material
salga del equipo — medido 7,5 min de audio en 29 s) en `golden-investigacion-mercado` →
`references/01-investigacion-360.md` §1.6; el desglose segundo a segundo lo hace
`golden-video-teardown`. Ojo de campo: en reels el subtítulo va quemado UNA PALABRA POR
FOTOGRAMA — leerlo de la imagen devuelve basura; sin transcripción un video hablado es ilegible.

## Entregables por canal

### Meta Ads (FB/IG)
Estándar **5+5+5**. Por cada concepto/video entrega SIEMPRE:
- **5 textos principales / primary text** — **2 cortos (<50 car.) + 3 largos (250-500 car.)**
- **5 titulares / headlines** (**≤40 car.**) — 3 de beneficio + 2 de oferta
- **5 descripciones** (**≤25 car.**, no 30)
- **CTA** sugerido
> Nunca menos de 5/5/5: son 5 textos principales, 5 titulares y 5 descripciones por cada concepto o video, cada uno anclado a un ángulo/dolor y compliant.
> Para validar conteo exacto de caracteres por ubicación, apóyate en `claude-ads:copy-writer`.

#### 📏 Los largos NO son libres — lee `references/estandar-meta-medido.md`

Tres reglas medidas que mandan sobre cualquier intuición. El detalle, las fuentes y cómo
volver a levantarlas están en ese archivo; aquí va lo que no se negocia:

1. **El rendimiento de Meta es BIMODAL** (43,9M de anuncios): gana **<50 caracteres**, segundo
   pico **250-500**, y el **peor rango es 50-125** — justo donde escribe casi todo el mercado.
   Por eso los 5 textos van **2 cortos + 3 largos**: cubren los dos picos y esquivan el valle.
   Si entregas los 5 del mismo largo, estás dejando la mitad del rango sin cubrir.
2. **Los primeros 125 caracteres son el anuncio entero.** Ahí cae el "Ver más" y la mayoría no lo
   abre. En todo texto largo, el argumento de venta (precio, duración, envío gratis, prueba
   social) **tiene que caber dentro de esos 125**. Es la clase de fallo más común al auditar
   copys largos: el gancho se come la ventana y el argumento queda escondido. **Revísalo uno
   por uno antes de entregar.**
3. **Reparte niveles de consciencia** (Schwartz) entre los 5, en vez de cinco versiones del mismo
   mensaje: el algoritmo empareja mejor con un conjunto diverso que con cinco clones.

**Molde de los largos en COD LatAm** (el que están corriendo los anunciantes colombianos):
una idea por línea, línea en blanco entre bloques, emoji al inicio de cada línea, bloque de
beneficios con ✅, línea de envío 🚚, línea de pago 💵, cierre 👉.

**Antes de entregar, mide.** No estimes a ojo: cuenta los caracteres de cada pieza y comprueba
la ventana de 125. Un contador que aprueba todo a la primera es sospechoso — pruébalo contra un
copy que sepas malo.

#### 🔄 Qué está vendiendo AHORA — `references/tendencias-vivas.md`

Bitácora que la tarea programada **`copywriting-tendencias-8-dias`** refresca cada 8 días con
(a) lo que está corriendo en el mercado y (b) el rendimiento real de las campañas de Golden.
🔒 **Es DATO LOCAL — NO DISTRIBUIBLE** (CPA reales de cuentas Golden con nombre): si esta skill
se publica o comparte con alumnos, ese archivo se EXCLUYE o se reemplaza por cifras de ejemplo.
**Léela siempre antes de escribir copy de Meta**: `estandar-meta-medido.md` es la base estable,
`tendencias-vivas.md` es lo que se mueve. Si la entrada más reciente trae números y fuente que
contradicen la base, manda la reciente; si es una impresión sin medir, manda la base.

### TikTok Ads / UGC
- **Guion de 15–30s**: Hook (0–3s) → Problema → Demostración/uso → Prueba → CTA.
- Indicaciones de cámara/texto en pantalla. 3 variantes de hook hablado.

### Reels / Captions orgánicos (IG/FB)
- Caption con gancho + valor + CTA suave + hashtags relevantes (no spam).
- 3 variantes de primera línea.

### WhatsApp / orgánico directo
- Mensaje de apertura, manejo de 1–2 objeciones, y cierre **según el modelo**: en COD se cierra
  confirmando dirección y "paga al recibir"; en pago anticipado se cierra **enviando el link de
  pago**, sin mencionar riesgo.
- Tono cercano, 1 idea por mensaje, emojis con criterio.
> Si es para configurar el bot completo, deriva a `golden-chatea-pro-full-configuracion` (o `golden-chatea-pro-prompt-ventas` para solo el prompt de venta).

#### 💬 Si el destino del anuncio es un chat (Click to WhatsApp), no una landing
Cuando el CTA del anuncio abre una conversación de WhatsApp en vez de llevar a una página, el
copy **no vende el producto, gana el mensaje** — el cierre pasa al chat. Lee
`references/referencia-externa-copy-click-to-whatsapp.md` antes de escribir ese caso: estructura
de 3 pasos (dolor → validación/prueba social → CTA que invita a conversar, no a comprar), y por
qué sobre-vender en el anuncio quema el clic. Es material de terceros marcado como referencia
opcional, no regla dura — los 5 copys por rubro siguen siendo obligatorios.

## Formato de salida
Agrupa por canal con encabezados claros. Marca el ángulo de cada variante: `[Dolor]`, `[Deseo]`, etc. Respeta siempre los guardrails de formato (sin signos de apertura, sin líneas de rayas, todo copy en bloque de código). Cierra ofreciendo: «Quieres que adapte el ganador a otro canal o genere los creativos con `claude-ads` / Higgsfield?»


## 🔁 Loop de autocrítica antes de entregar (obligatorio)

Una sola pasada entrega lo primero que salió, que casi nunca es lo mejor que podías. **Antes de
mostrar nada, critica tu propio trabajo N veces** — 3 pasadas mínimo, 5 si la pieza va a producción:

1. **Pasada 1 · el encargo.** Cumple lo que pidieron, o cumple lo que era más cómodo escribir?
2. **Pasada 2 · lo flojo.** Señala tú mismo la variante más débil del lote y di por qué. Si no
   encuentras ninguna, no buscaste: siempre hay una que solo está para llenar.
3. **Pasada 3 · las reglas de la casa.** Sin signos de apertura, sin líneas de rayas, compliance,
   modelo de pago correcto, y el posicionamiento del producto respetado.
4. **Pasadas 4-5 (si va a producción).** Léelo como lo leería el cliente, no como quien lo escribió.

**Entrega solo lo que sobrevive**, y di qué descartaste y por qué. Un lote de 5 donde 2 son relleno
vale menos que uno de 3 donde los 3 pelean — porque el relleno se cuela a producción cuando nadie
lo señala.

## Changelog

- **GCW1.6.0** (2026-09-01) — **Quinta corrida de la tarea de 8 días.** Cobertura: **76 cuentas**
  inventariadas (eran 74 en las corridas 2-4), **59 barridas una por una**, 15 con gasto, 5 bajadas
  a nivel anuncio (100 anuncios), 21 creativos con cuerpo completo. Mercado: 3 términos, 150
  anuncios, 52 páginas, 132 títulos, **5 de 5 cuerpos leídos** (primera vez sin vacíos). Tres
  scripts con autotest y casos negativos deliberados; el primero **falló a la primera y el fallo era
  mío** (esperaba 26 caracteres donde había 25, por contar el emoji como si ocupara dos).
  **(1) SE REFUTA el titular de la corrida 4.** Su "hueco estructural de la API de lectura" era
  **transitorio**: mismas cuentas, mismo método, ocho días después → GOLDEN CP6 **0% → 98,8%**,
  BLUE CP1 **4,7% → 99,8%**, GOLDEN CP1 23% → 93,9%, Le'côterra CP2 46% → 81,5%. La medición del
  25-ago fue real; la conclusión no. **La regla de cuadrar cobertura NO se deroga: se refuerza** a
  chequeo obligatorio de cada corrida, justamente porque puede caer a 0% y volver sin avisar.
  **(2) SUBE A LA BASE (§6): WhatsApp le gana a SHOP_NOW con el mismo texto byte por byte**, entre
  **1,7x y 2,3x**, en **tres mediciones independientes** (21-ago, 25-ago, 01-sep). Última: 29 vs 16
  vs 12 compras, con el mapeo creativo→anuncio **verificado** con `ads_get_creative_ads`, no
  inferido del nombre. Límite declarado: el video no es idéntico, la dirección es de fiar, el número
  exacto no.
  **(3) SUBE A LA BASE (§3): la oferta logística va al TÍTULO, no forzada en los 125.** Medido con
  script: **0 de 5** cuerpos del mercado la meten en los primeros 125 (la más temprana en el
  carácter 172); **4 de 5** la ponen en título o descripción del enlace, que nunca se truncan.
  **(4) Corrección a la corrida 4 (§4):** afirmó que "cabe en 40" era la cifra estable en 79-87%.
  **El rango real de cinco corridas es 79-93%.** Lo que aguanta es el enunciado —cuatro de cada
  cinco títulos o más caben en 40—, no el porcentaje. Se añade tabla de las 6 métricas de título con
  su rango de 5 corridas y su veredicto de usable/no usable.
  **(5) Hallazgo estructural limpio:** de 66 títulos con emoji, **45 al principio, 21 al final, CERO
  en el medio**, con tres formas distintas de deduplicar.
  **(6) §1, cita nueva del artículo canónico 223409425500940** que respalda el 5+5+5 con **opciones
  que carga el anunciante** (hasta ahora se apoyaba en el artículo de generación por IA). Límites
  **125/40/25 confirmados por quinta vez.** Hueco declarado: **`placement asset customization`** no
  se menciona en la skill. **(7) §4, dos mecanismos nuevos del mercado:** la pregunta que hace
  ELEGIR (no asentir) y los hashtags al cierre; y la prueba social numérica ya no va en el cuerpo,
  va en título o descripción.
  **Blindaje: NO se re-blindó, a propósito** — segunda corrida seguida que lo reporta: la política
  del CdM (GCW1.3.8) derogó el `uchg` y el mandato de la tarea todavía lo ordena. Respaldo previo:
  `RESPALDOS-SKILLS/golden-copywriting_2026-09-01_pre-corrida5.tar.gz`.
  **Nota de higiene encontrada:** el changelog **no tiene entrada para GCW1.5.0** (el sello del
  27-ago la trae, el changelog salta de 1.4.0 a 1.3.9). No la invento — va a la bandeja.
- **GCW1.4.0** (2026-08-25) — **Cuarta corrida de la tarea de 8 días.** Cobertura: 74 cuentas
  inventariadas, **58 barridas — el censo completo de lo legible** (las corridas anteriores llegaban
  a 42), 16 con gasto, 6 bajadas a nivel anuncio, 13 creativos leídos, mercado de 150 anuncios /
  84 páginas / 142 títulos con script autotesteado (16 checks, 0 fallos), 4 de 5 cuerpos de mercado
  leídos. Cambios de fondo en `estandar-meta-medido.md`:
  **(1) Sección nueva "La OTRA cara de la trampa":** la API a veces **no devuelve el gasto pase lo
  que pase** — GOLDEN CP6 (3.171.690 COP) y BLUE CP5 (777,20 USD) devuelven lista vacía con filtro,
  sin filtro y a nivel campaña; BLUE CP1 cubre 4,7%. Se añade **regla dura de cuadre de cobertura
  antes de rankear copys**, con el caso medido que la justifica (el anuncio visible de BLUE CP1 se ve
  2,2x mejor que su propia campaña). Esto **relativiza las tablas anuncio-por-anuncio de las corridas
  1-3**, que nunca cuadraron cobertura.
  **(2) Corrección a §7:** llevaba tres corridas diciendo que la longitud media del título era la
  cifra estable. No lo es (30,1 → 29,6 → 30,0 → **32,5**, con la mediana cayendo a 25,5). Lo estable
  en cuatro corridas es **"cabe en 40": 79-87%**.
  **(3) §1, dos citas oficiales nuevas:** la descripción de 25 es *"only nonessential information"*
  (art. 497610041230617) y el generador de variantes de Meta **soporta español** (art. 180641596861873).
  Límites **125/40/25 confirmados por cuarta vez**, sin cambio.
  **(4) §2:** el banco de pruebas del reparto 2+3 se apagó (Le'côterra CP2 migró a catálogo), y la
  tanda corta viva muestra el mecanismo: cargadas como anuncios hermanos, el conjunto le dio
  166.697 / 436 / 9 COP — **cargar variantes como anuncios separados garantiza que no se midan**.
  Además: corregido el `¿Argumento en 125?` que GCW1.3.8 dejó anotado (regla de la casa, sin signos
  de apertura). **Blindaje: NO se re-blindó, a propósito** — la política del CdM (GCW1.3.8) derogó el
  `uchg` para esta skill y el mandato de la tarea programada todavía lo ordena; se respetó la fábrica
  declarada y la contradicción va a la bandeja. Respaldo previo:
  `RESPALDOS-SKILLS/golden-copywriting-GCW1.3.9-20260825-corrida4.tar.gz`.
- **GCW1.3.9** (2026-08-24): bump de las ediciones del 24 (verificador de cierre R2: la version vive en 4 caras — sello, linea Version, Changelog y REGISTRO — y el bump anterior toco solo el sello).
- **GCW1.3.8** (2026-08-24) — **Barrido total del arsenal (pluma delegada del CdM) + política de
  blindaje declarada.** La skill se encontró blindada en 5 de 6 nodos cuando la política del CdM
  para ella es SIN blindar (la tarea de 8 días le escribe; el flag producía el ciclo de choques que
  la propia bitácora documenta) → liberada y la política queda escrita arriba y en el ritual de
  AUTO-MEJORA. Gemelo del rótulo DATO LOCAL agregado al puntero de `tendencias-vivas.md` (el aviso
  vivía solo dentro del archivo). `estandar-meta-medido.md`: typo "premita"→"premia" y mini-índice
  (301 líneas ya pedían tabla de contenido). Ruta de la fuente Panamá precisada en la referencia
  CTWA. `tendencias-vivas.md` intacto (DATO LOCAL): su encabezado "¿Argumento en 125?" viola la
  regla de signos de apertura — reportado para que lo corrija la próxima corrida de la tarea, única
  mano autorizada ahí. Reportado al CdM (estándar 9).
- **GCW1.3.6** (2026-08-21, mismo día) — **CORRIGE A GCW1.3.5, que se publicó con un
  cherry-picking.** Al ampliar la cobertura a las 12 cuentas con gasto que la 1.3.5 había dejado
  fuera, apareció que `OPEN 7` (14-ago) y `OPEN 8` (19-ago) **no son una pieza suelta de copy
  corto: son una tanda entera corriendo en 8 cuentas** (32-52 caracteres, 8 creativos leídos).
  Con la muestra completa **el corto PIERDE: CPA 54.875 sobre 37 compras contra 44.743 del largo
  sobre 193 — 23% más caro** (la 1.3.5 había reportado el ROAS 3,62 de UNA pieza con 2 compras
  como si fuera la señal). **El hallazgo real es la dispersión: el mismo copy corto va de CPA
  17.037 a 123.710 entre cuentas, siete veces** — más grande que el 23% que se quiere medir, así
  que el experimento corto-vs-largo **no puede dar veredicto mientras la varianza entre cuentas
  mande**. Corregidos `tendencias-vivas.md` (bloque de corrección al frente de la entrada, la
  frase original queda tachada a la vista, no se borró) y `estandar-meta-medido.md` §2. Cobertura
  final: **17 de 17 cuentas con gasto bajadas a nivel anuncio** (la 1.3.5 llevaba 5), 27
  creativos leídos. Nota de gobierno: `golden-skill-auditor` editó esta skill a las 01:27, en
  mitad de esta corrida y con la skill blindada por mí a las 00:59 — no se perdió nada, pero es
  el choque de dos manos que el propio blindaje existe para evitar. Reportado a la bandeja.
  Respaldo previo: `RESPALDOS-SKILLS/golden-copywriting-GCW1.3.5-20260821-1130.tar.gz`.
- **GCW1.3.5** (2026-08-21) — **Tercera corrida de la tarea de 8 días.** La skill se encontró
  **desblindada por segunda corrida seguida**; esta vez con causa identificada (el CdM editó
  `tendencias-vivas.md` el 2026-08-20 11:32 para ponerle el rótulo "DATO LOCAL — NO DISTRIBUIBLE"
  y no volvió a blindar). Cuatro correcciones con número y fuente en `estandar-meta-medido.md`:
  **(1)** §3, la regla de los 125 se sostiene en **0 de 8** mayores vendedores y se reescribe su
  aplicación — la oferta va en el TÍTULO (nunca se corta) y solo si no cabe ahí se mete en los
  primeros 125 del cuerpo. **(2)** §2, **el polo corto YA salió al aire** (33 caracteres, ROAS
  3,62 sobre 2 compras) y el mecanismo de opciones múltiples queda documentado con fuente oficial
  de Meta (aplica solo a imagen/video único). **(3)** §4, la oferta emigró al titular y aparece la
  variante del MECANISMO leída en mercado. **(4)** §6 NUEVA — **el copy no es la variable
  dominante**: tres creativos con el mismo cuerpo byte por byte dan CPA de 14.794 a 119.346; §7
  NUEVA con qué del mercado es medible y qué no (emoji y MAYÚSCULAS eran ruido, corrige a la
  corrida 2). Los dos fallos de higiene de un cliente (negrita Unicode falsa, Markdown sin renderizar)
  siguen sin corregir y el de Markdown se replicó de 1 a 3 creativos; reportado otra vez a la
  bandeja del CdM, fuera de mi dominio ejecutarlo. Cobertura: 74 cuentas inventariadas / 42
  barridas (excl. BACK UP, +6 sin medio de pago que antes no se miraban) / 17 con gasto / 5 a
  nivel anuncio / 14 creativos leídos. Nueva entrada en `tendencias-vivas.md`. Respaldo previo:
  `RESPALDOS-SKILLS/golden-copywriting-GCW1.3.4-20260821-1050.tar.gz`.
  **Auditoría golden-skill-auditor (2026-08-21):** se fusionó `CHANGELOG.md` (duplicaba este
  changelog en formato más corto y ya había desincronizado — traía esta entrada y aquí faltaba)
  y se retiró el archivo suelto de la raíz; historial completo queda solo aquí. Se agregó el
  puntero que faltaba desde esta sección hacia
  `references/referencia-externa-copy-click-to-whatsapp.md` (existía sin que SKILL.md lo
  mencionara — huérfano funcional aunque el inventario no lo marcara roto). Ningún dato ni
  hallazgo de campo se borró: el histórico 2026-07-30 (masterclass Panama) y 2026-08-02
  (sección AUTO-MEJORA) que traía `CHANGELOG.md` ya vive como contenido vigente de esta skill
  (la sección AUTO-MEJORA de más abajo, y la referencia CTWA ahora enlazada).
- **GCW1.3.4** (2026-08-16) — **Segunda corrida de la tarea de 8 días.** Cobertura: 74 cuentas
  inventariadas, 36 revisadas (excluida BACK UP), 17 con gasto en 30 días (sube de 14); mercado:
  3 términos, 150 anuncios, 46 páginas, 60 títulos únicos, 4 cuerpos completos. Hallazgo mayor:
  **la regla de los 125 caracteres deja de ser ley dura** — 0 de 5 mayores vendedores medidos
  (Le'côterra, Tag Recede, un cliente por primera vez cruzada) meten el argumento en la ventana
  visible, y ya no es solo un vertical con restricción de claims. Actualizado
  `estandar-meta-medido.md` §3 con el número y la fuente. También: la skill se encontró
  **desblindada** al empezar esta corrida (sin forcejeo detectado); dos fallos de higiene
  hallados en copy PROPIO de un cliente (negrita Unicode falsa, asteriscos Markdown sin renderizar)
  reportados a la bandeja del CdM por estar fuera de mi dominio ejecutarlos. El reparto
  2 cortos + 3 largos sigue sin poder verificarse (van 2 corridas: la API no expone
  `asset_feed_spec`). Nueva entrada en `tendencias-vivas.md`. Respaldo previo:
  `RESPALDOS-SKILLS/golden-copywriting-GCW1.3.2-20260816-1255.tar.gz`.
- **GCW1.3.3** (2026-08-11) — **RED SINÁPTICA: los hooks se minan del AUDIO de lo que ya vende.**
  Sección nueva tras los frameworks: transcripción LOCAL de videos ganadores (whisper, receta
  canónica en `golden-investigacion-mercado` §1.6 — no se duplica aquí para que no envejezca en
  dos sitios) + puente a `golden-video-teardown` para el desglose. Origen: el chat FILTRO destapó
  que la capacidad existía en `golden-video-editor` y nunca se propagó; propagada por el Centro
  de Mando bajo la ley de red neuronal de FER (2026-08-11). Dato de campo que lo justifica: en
  reels el subtítulo va quemado una palabra por fotograma — sin transcribir, ilegible.
- **GCW1.3.2** (2026-08-10) — **Primera corrida de la tarea de 8 días.** Cobertura: 75 cuentas
  inventariadas, 36 revisadas, 14 con gasto analizadas a nivel anuncio; 57 títulos de mercado
  medidos con script. Cuatro correcciones al estándar medido, todas con número y fuente:
  **(1)** el reparto 2 cortos + 3 largos **va como opciones múltiples dentro de UN anuncio**, no
  como cinco anuncios — se descubrió que los 165 copys de Le'côterra salieron con un solo cuerpo
  de 332 caracteres y **ningún corto llegó a correr**, así que el estándar no falló: no se
  ejecutó. **(2)** Los títulos de mercado se remiden con script reproducible (media 30, 82% cabe
  en 40, 51% con emoji, 32% oferta) y se advierte que la brecha contra la medición a mano anterior
  es **de método, no de mercado**. **(3)** Se anota el contraejemplo de la regla de los 125:
  Tag Recede vende 43 unidades a 24.531 COP con 185 caracteres y sin oferta en el texto — la
  regla no aplica cuando el producto no puede prometer. **(4)** Se hornea la trampa de
  `effective_status`: filtrar solo por activos/pausados escondía la mayoría del gasto (GOLDEN CP1
  devolvía cero teniendo 3,29M COP), con la lista larga de estados y el cuadre obligatorio contra
  el total de la cuenta. Límites oficiales de Meta reverificados: **125/40/25 sin cambio**.
- **GCW1.3.1** (2026-08-10) — Sello de fábrica corregido por decisión del Centro de Mando: esta
  skill **no abre chat-fábrica propio**; por la regla *skill sin fábrica = su fábrica es el CdM*,
  el dueño es el Centro de Mando y `copywriting-tendencias-8-dias` queda como **brazo delegado**,
  única mano automática autorizada a escribir aquí. `loop-auditoria-arsenal-golden` la lee sin
  tocarla; hallazgo de cualquier otra sesión va a la bandeja del CdM, nunca a edición directa.
- **GCW1.3** (2026-08-10) — **Los largos dejan de ser a ojo: entra el estándar MEDIDO de Meta**
  (`references/estandar-meta-medido.md`, tres fuentes contrastadas). Hallazgos que cambian el
  entregable: la **descripción es 25 caracteres, no 30** (fuente oficial de Meta; medio internet
  repite 30 y Meta trunca en silencio); el rendimiento es **BIMODAL** sobre 43,9M de anuncios
  —gana <50, segundo pico 250-500, **el peor rango es 50-125**—, así que los 5 textos principales
  pasan a **2 cortos + 3 largos** en vez de cinco del mismo largo; y **los primeros 125 caracteres
  tienen que llevar el argumento de venta** porque ahí cae el "Ver más" (13 de 33 largos fallaban
  esto en el primer borrador de Le'côterra). Se hornea el **molde COD colombiano real** leído de
  anuncios activos y el reparto de títulos **3 beneficio + 2 oferta** (el 51% del mercado usa el
  título para la oferta). Nace `references/tendencias-vivas.md`, bitácora que la tarea
  `copywriting-tendencias-8-dias` refresca con mercado + campañas propias. Origen: chat Le'côterra.
- **GCW1.2** (2026-07-27) — Corregido por FER: Golden NO es solo contra entrega, tiene marcas
  propias con pago anticipado. El modelo de pago entra al intake mínimo y cambia el EJE del copy
  (tabla nueva): en COD la objeción es "y si pago y no llega", en marca propia es "y si no me
  sirve a mí". Poner "paga al recibir" en marca propia siembra una duda que el cliente no tenía.
  Framework BAB añadido para marca propia (PAS agita un dolor que ahí ya está reconocido).
- **GCW1.1** — Meta Ads pasa a estándar 5+5+5 (5 textos principales + 5 titulares + 5 descripciones, antes eran 2 descripciones). Se hornean guardrails de formato (sin signos de apertura, sin líneas de rayas, copy en bloque de código) y guardrails de posicionamiento/compliance (respetar posicionamiento del producto, texto líder aspiracional en 1ª persona, ganchos fuertes solo como rotación, "unisex sutil"). Aprendizaje de campo: caso Le'côterra (Meta Ads COD LatAm).
- **GCW1.0** — Versión inicial: copy multicanal (Meta, TikTok/UGC, orgánico, WhatsApp) con ángulos y frameworks.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → arreglar → changelog+sello → cerrar SIN blindar, chmod 644 — política CdM
2026-08-24 para esta skill, ver arriba); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — Copywriting de respuesta directa para TODOS los canales: anuncios de Meta (Facebook/Instagram), TikTok Ads, y mensajes orgánicos para WhatsApp, Facebook e Instagram. Escribe hooks, primary text, headlines, descripciones, guiones de video (UGC/TikTok), captions y secuencias de mensajes, con ángulos de venta, frameworks probados (AIDA, PAS, BAB, 4U) y tono LatAm que convierte tanto en contra entrega como en pago anticipado. Úsala SIEMPRE que el usuario quiera: escribir/mejorar copy de anuncios, hooks, textos para Meta o TikTok, guiones de reels/UGC, captions para redes, mensajes de WhatsApp/orgánicos, "hazme el copy de", "dame ángulos de venta", "ganchos para este producto", "textos para vender X". Aplica a cualquier producto/país. Trae el estándar MEDIDO de largos de Meta (125/40/25, rendimiento bimodal, la ventana visible de 125 caracteres) y una bitácora de tendencias que se refresca cada 8 días con el mercado y con las campañas reales, así que úsala también para "cuántos caracteres debe tener", "qué copy está funcionando ahora", "qué está vendiendo en el mercado". Para el PROMPT del bot de ventas usa golden-chatea-pro-prompt-ventas.

x
