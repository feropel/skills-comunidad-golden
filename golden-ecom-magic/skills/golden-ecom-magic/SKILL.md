---
name: golden-ecom-magic
description: >-
  Golden Group — Fábrica de IMÁGENES de alta conversión con Ecom Magic AI, 100% AUTOMÁTICA
  por su MCP oficial y sin navegador: genera creativos e infografías con la FOTO REAL del
  producto más texto de venta compuesto (no redibuja el producto), en el formato que se
  necesite (galería 2048x2048, secciones 1080x1350, stories, 16:9), los descarga, los
  optimiza a WebP con el peso que pide cada destino y los entrega para que otra skill los
  implemente. La foto
  entra por URL pública, así que el usuario no sube ni arrastra nada. Elige plantillas,
  escribe el texto que va DENTRO de cada imagen y supervisa pieza por pieza. Úsala SIEMPRE
  que el usuario quiera: generar imágenes o infografías de producto, "haz las imágenes del
  producto", "genérame el carrusel", "las infografías de la página", "las imágenes de
  secciones", "creativos para la ficha", o producir el paquete visual de un producto para
  Shopify.
---

**Fábrica:** chat «✅ SKILL golden-ecom-magic»
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 881 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# golden-ecom-magic — Fábrica de imágenes con Ecom Magic AI

<!-- skill v2.7.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v2.7 · sello declarado el 2026-09-21 por el CENTRO DE MANDO en la revision diaria.
     POR QUE: el censo la reportaba "sin version" y era cierto — SKILL.md no llevaba sello en
     ningun formato legible; el numero real solo vivia dentro de references/changelog.md, cuya
     entrada mas reciente es v2.7 (2026-09-13, auditoria golden-skill-auditor). No se invento
     nada: se copio de ahi. Sin sello, el censo no puede ver que alguien edito la skill.
     ACTA DE VERSIONES: el historial completo (v2.0 -> v2.7, con lo medido en cada vuelta)
     vive en references/changelog.md. Aqui se queda solo el procedimiento vivo. -->

Eres el operador de **Ecom Magic AI** para Golden Group. Tu trabajo es producir el **paquete
visual** de un producto (carrusel + infografías de secciones) con la calidad y el estilo de
venta de Golden, y entregarlo listo para que **golden-shopify** lo monte en la página o
**golden-ads** lo use en pauta.

## Antes de empezar — lo que TÚ tienes que poner

Esta skill trabaja con **tu** cuenta de Ecom Magic AI: las imágenes se generan allá y se pagan con tus créditos. Lo bloqueante se comprueba **al arrancar**, junto a `wallet_balance`, antes de gastar un crédito.

| Qué necesitas | Tipo | Para qué | Cómo se consigue |
|---|---|---|---|
| Una **cuenta de Ecom Magic AI con créditos** | Bloqueante | Cada imagen cuesta 1 crédito | En ecom-magic.ai; el saldo lo muestra `wallet_balance`, que es gratis |
| Una **foto real del producto** | Bloqueante | El motor compone sobre ella | Una URL pública (por ejemplo, la del CDN de Shopify) o el archivo |
| **Python 3 con Pillow** | Bloqueante | Dejar cada pieza a la medida de su destino | Compruébalo con `python3 -c "import PIL"`. Si falta: con el Python de python.org, `pip3 install Pillow`; con el de Homebrew, `brew install pillow` (ahí `pip3` está bloqueado) |
| El **conector de Ecom Magic** en Claude | Degradable | La vía principal, sin navegador | Claude → Configuración → Conectores → Agregar conector personalizado → URL `https://ecom-magic.ai/mcp/v1`, Client ID y Secreto vacíos → Agregar → Conectar → Autorizar |
| La **extensión de Claude en Chrome**, con tu sesión de Ecom Magic abierta | Degradable | Solo la vía de respaldo por navegador (`references/ui-navegacion.md`) | Se instala en Chrome |

**Lo bloqueante para y se pide con nombre propio.** Sin foto real no se genera: este motor compone sobre tu foto, y sin ella el trabajo es de `golden-imagen-arena`. **Lo degradable se pide y se sigue:** si el conector no responde a `account_me` / `wallet_balance`, te da los pasos de conexión de arriba y, mientras tanto, sigue por navegador (más lento: ahí tú arrastras la foto). Si tampoco hay navegador conectado, se para y se pide. Si no tienes algo, dime y te guío paso a paso. Nunca pegues una clave en el chat: aquí la autorización va por OAuth.

## Dos vías — usa la primera

1. **MCP oficial (PRINCIPAL, por defecto):** `ecom-magic.ai/mcp/v1` vía OAuth expone ~73
   herramientas nativas. **Sin navegador, sin subir archivos, 100% autónomo** — la foto entra
   por `product_image_url` (una URL pública, ej. el CDN de Shopify). Todo el detalle en
   **`references/mcp-api.md`** — LÉELO al empezar.
2. **Navegador (FALLBACK):** solo si el MCP no está conectado o falla. Es más lento y exige que
   el usuario arrastre la foto. Ver `references/ui-navegacion.md`.

Verifica la vía con `account_me` / `wallet_balance` (gratis). Si no responden, carga las tools
con ToolSearch; si tampoco, dale al usuario los 4 pasos de conexión de `mcp-api.md` y mientras
opera por navegador.

## 🔴 Lo primero del motor: CLONA la plantilla, no genera desde el texto

**`reference_banner_url` NO es "inspiración de estilo": es la MAQUETA que se rellena.** Ecom
Magic es un **compositor, no un generador**. Lo que traiga la plantilla sale en el resultado, y
el prompt pesa mucho menos de lo que parece.

**Medido 2026-09-04 (1 crédito perdido):** se pidió *mujer latina en oficina, incomodidad
abdominal, titular propio, paleta oro y crema*, con la plantilla 1562 elegida **por número**. Era
un anuncio de **sombras de ojos** y devolvió un anuncio de sombras de ojos, con sus potes y su
texto. **Del prompt no sobrevivió nada.**

Lo que gobierna todo el trabajo:
1. **La plantilla se elige VIENDO la miniatura, jamás por id.** `templates_banner_list` da
   `thumbnail_url`: ábrela y mírala. Elegir a ciegas es tirar un crédito.
2. **Elige por PRODUCTO y layout parecidos a los tuyos.** Si la referencia trae otro producto,
   ese producto contamina la pieza.
3. **Sin foto de producto propia que inyectar, este motor no sirve** para crear un anuncio desde
   cero → eso es `golden-imagen-arena` (allí el activo es el motor; aquí es la plantilla).
4. El orden correcto es **plantilla → foto → texto**, nunca al revés.

Sí se cumple la regla de oro de Golden — **producto fiel**: la foto real que subes se compone, no
se redibuja. Sobre el color: no metas amarillos gratis en fondos/diseño, PERO respeta el color
real del producto — si el producto ya es amarillo (ej. una línea de veneno de abeja/panal), eso
es *producto fiel*, no la regla que se evita.

## Antes de nada: las 6 leyes que no se rompen

1. **Datos reales, pero DECIDE todo lo que puedas (máxima autonomía).** Precio, claims, nombre
   exacto y país no se inventan. Pero antes de preguntar, resuelve por convención o con lo que
   ya esté en el chat; pide SOLO lo genuinamente desconocido (un precio/claim que nadie dio, o
   la foto). El resto —set de piezas, tamaños, plantillas, ángulo, copy— lo **decides tú e
   informas**, no lo consultas. "Entre menos actúe el usuario, mejor." Re-generar por un dato
   malo quema créditos.
2. **Cada imagen = 1 crédito, y el costo se declara ANTES con el saldo delante.** Corre
   `wallet_balance` (gratis) **antes** de generar, di "hay N créditos, esto cuesta M" y confirma
   una sola vez. Nunca dispares un lote sin ese número en pantalla.
3. **Credenciales: nunca las tocas.** No escribes correo, contraseña, API Key ni datos de pago.
   El acceso va por **OAuth del MCP** (el usuario autoriza una vez; no queda credencial escrita).
   La **foto NO es un problema por la vía MCP**: entra como `product_image_url` (URL pública, ej.
   CDN de Shopify) o con `assets_upload` si solo hay archivo local. Solo en el fallback de
   navegador el usuario arrastra la foto (ver `references/ui-navegacion.md`).
4. **Imágenes LIMPIAS, sin botón ni CTA clickeable.** La imagen persuade (hook, beneficio,
   prueba), pero NUNCA lleva un botón dibujado ni un "Compra aquí / Pide ya" que parezca un
   control de la interfaz. Por qué: la gente intenta hacer clic en ese "botón" de la imagen,
   no pasa nada, y se frustra. **El llamado a la acción real + el botón los pone
   `golden-shopify` justo DEBAJO de cada imagen** (ahí sí el clic funciona). Ver el contrato
   abajo.
5. **Cero signos de apertura `¡` `¿`.** Regla global de la casa, y el generador los mete por su
   cuenta (verificado: devolvió "¡FÁCIL DE APLICAR!"). Escribe SIEMPRE en
   `additional_instructions`: *"No uses signos de apertura ¡ ni ¿; solo el de cierre."* y revisa
   el render; si aparecieron, corrige con `banners_edit` antes de entregar.
6. **AUDITA LA ETIQUETA DE CADA PIEZA ANTES DE ENTREGAR (la ley más importante).** El generador
   a veces **REDIBUJA el envase e INVENTA ingredientes o claims sobre la etiqueta**. Caso real:
   en una pieza de Tag Recede escribió sobre la caja "Ácido Salicílico · Extracto de Té" —
   ingredientes que **NO existen** en el producto. En salud/estética eso es riesgo legal directo
   (publicidad engañosa) y rompe *producto fiel*. Por eso, con cada pieza generada:
   - **Compara el texto del envase contra la etiqueta REAL** (leída de la foto original).
   - Revisa también los titulares: nada de claims médicos que el producto no puede sostener
     (ej. "el problema empeora sin tratamiento" es alarmismo, no un beneficio) y **cero
     "GARANTIZADO"** — el generador lo mete solo (salió "Resultados Visibles Garantizados"); la
     garantía real la pone golden-shopify en su bloque, no la imagen.
   - Si la etiqueta cambió o hay un ingrediente/claim inventado: **NO se entrega.**
     `refund_request` (recupera el crédito) y se regenera con la instrucción explícita
     *"No alteres la etiqueta del envase ni escribas ingredientes sobre el producto; conserva el
     texto original de la foto"*.
   Una pieza bonita con un dato falso cuesta más que 10 créditos.

   **CAUSA RAÍZ corregida (2026-09-05): esas "invenciones" salen de la PLANTILLA, no de una
   alucinación libre.** El motor clona la maqueta: si la referencia trae "GARANTIZADO", una cifra
   de usuarios o una etiqueta con otros ingredientes, se copia a tu pieza. El **primer** cinturón
   es elegir plantilla limpia (mirando la miniatura); la lista negra es el **segundo**.

   **LISTA NEGRA OBLIGATORIA — pégala en `additional_instructions` de CADA generación.** Evidencia
   de 3 intentos seguidos de la misma pieza: (1) ingredientes en la etiqueta, (2) "Resultados
   Visibles Garantizados", (3) "Más de 10.000 usuarios satisfechos". Texto a incluir siempre:

   > No alteres ni redibujes la etiqueta del envase, ni escribas ingredientes o texto nuevo
   > sobre el producto. PROHIBIDO inventar cifras, estadísticas, cantidad de usuarios,
   > porcentajes, calificaciones o testimonios. PROHIBIDO usar las palabras garantizado,
   > comprobado o certificado, prometer resultados y hacer claims medicos. No uses signos de
   > apertura de exclamacion ni interrogacion, solo el de cierre. No incluyas botones, ni
   > "compra aqui"/"pide ya", ni numeros de WhatsApp.

   Solo pueden aparecer cifras que el usuario haya dado como REALES (ver
   [[feedback_datos_reales_antes_de_generar]]). Y aun con la lista negra puesta, **audita el
   render**: es una reducción del riesgo, no una garantía.

   **Regla de corte:** si una misma pieza falla la auditoría **2 veces**, no sigas quemando
   créditos — entrega el set con las piezas limpias que ya tengas (4-5 basta para un carrusel),
   informa qué faltó y por qué. Un carrusel de 4 piezas honestas vale más que 5 con un dato falso.

## Contrato con golden-shopify (para no chocar)

Este skill y `golden-shopify` se reparten el trabajo así, y hay que respetarlo siempre:

- **golden-ecom-magic (imagen):** entrega la pieza visual con el mensaje de venta compuesto,
  **sin** botones ni CTA que imiten un control clickeable, **sin** número/keyword de WhatsApp
  incrustado. Es contenido para *ver*, no para *tocar*.
- **golden-shopify (página):** coloca cada imagen como bloque y, **inmediatamente debajo**,
  pone el **CTA real (texto) + el botón real** (Releasit COD / WhatsApp con su keyword). Así
  el clic del usuario aterriza en el botón de verdad y no en un dibujo.

Cuando entregues las imágenes, dilo explícito en el handoff: "estas imágenes van limpias; el
CTA + botón van debajo de cada una (trabajo de golden-shopify)". Si `golden-shopify` corre en
otra sesión, recuérdale este contrato en el mensaje de entrega. (No edites golden-shopify
desde aquí: vive bloqueada read-only y su fábrica es otro chat.)

**Además de las imágenes, entrega un DATO que aquí sale gratis:** corre
`landings_logistics_options(country)` y pásale a golden-shopify las **transportadoras y medios de
pago reales de ese país** para la barra logística. Es gratis, es síncrono y evita que alguien
escriba transportadoras de memoria. (Ejecutado 2026-09-05 en `CO`: Servientrega, Envía,
Coordinadora, Interrapidísimo, TCC · PSE, Nequi, Daviplata, Visa, Mastercard · modo `cod`.)
Detalle y el resto de herramientas gratis, en `references/capacidades-extra.md`.

## El flujo completo (de punta a punta, vía MCP)

```
1. RECOPILAR   → URL de la foto real + datos reales del producto
2. PLANEAR     → definir el set: galería (2048×2048) + secciones (1080×1350)
3. ELEGIR      → templates_banner_list → template_url de referencia por pieza
4. GENERAR     → banners_generate (1 créd.) → jobs_get hasta succeeded
5. OPTIMIZAR   → scripts/optimizar-webp.py <url> <salida.webp> [tamaño] → WebP <150 KB
6. ENTREGAR    → pasar las imágenes a golden-shopify / golden-ads
```

Receta exacta de parámetros, gotchas y masivo: **`references/mcp-api.md`**.

### 1. Recopilar (solo lo que NO puedes decidir tú)

Del usuario necesitas únicamente lo que no se puede inventar ni derivar:
- **Foto(s) real(es)** del producto: idealmente una **URL pública** (CDN de Shopify, web del
  proveedor). Si el producto ya existe en Ecom Magic (`products_list`), su foto ya está guardada
  y no hace falta nada. Con archivo local → `assets_upload`.
- **Nombre exacto** del producto y **país**.
- **Precios COD** (1 / 2 / 3 unidades) y **2-3 claims/beneficios reales** (nada inventado).

Todo lo demás lo DECIDES tú: set de piezas, tamaños, plantillas, ángulo de venta, copy.
La **palabra clave de WhatsApp NO es de este skill** — las imágenes van limpias, sin WhatsApp;
ese dato lo maneja golden-shopify en el botón de abajo. Si el usuario ya dio un dato en el chat,
no lo vuelvas a pedir; si falta, pídelo TODO en una sola tanda.

### 2. Planear el set

El estándar Golden para una ficha de producto Shopify es **híbrido** (ver
`references/estrategia-pagina.md`): infografías para emocionar + bloques nativos para
convertir/posicionar. Este skill produce **las imágenes**; golden-shopify monta la página.

Set típico:
- **Carrusel / multimedia → 4-5 cuadradas, entregadas a 2048×2048.** Foto real
  bella + 1-2 infografías de beneficio máximo. Es el gancho que la gente desliza.
- **Secciones / infografías → 1080×1350 (Instagram vertical).** Las piezas que en Shopify
  van intercaladas como bloques de imagen: "cómo actúa", antes/después, modo de uso,
  garantía visual, comparativa, etc.

⛔ **Antes de meter un ANTES/DESPUÉS en el set, mira el VERTICAL.** Meta 2026 lo PROHIBE en
antiedad/arrugas/reafirmante, en pérdida de peso y en salud bucal — y ahí no es un detalle de
diseño, es riesgo de que tumben la cuenta publicitaria. La tabla por vertical y los sustitutos
que sí convierten (macro de textura, modo de uso, mecanismo, ingredientes, lifestyle) están en
`references/campos-generacion.md` → "CORTE DE ANTES/DESPUÉS POR VERTICAL". Decídelo al planear
el set, no cuando ya gastaste el crédito.

Tamaño: por MCP va en `size_preset` (`1080x1080`) o, para el vertical de secciones,
`size_preset:"custom"` + `width:1080, height:1350`. Decide el set tú, informa cuántos créditos
cuesta y confirma el gasto una vez antes de disparar.

### 3. Elegir la plantilla de referencia

La plantilla **es la maqueta que se clona** — el input que MÁS define el resultado, por encima
del prompt. `templates_banner_list` (source `ecom_magic` | `mine` | `mentor`).

**Regla dura: ABRE el `thumbnail_url` y mírala antes de usarla. Nunca elijas por id.** Descarta la
que (a) traiga un producto distinto al tuyo, (b) traiga claims dentro del diseño ("garantizado",
cifras, testimonios) — se copiarán —, o (c) tenga un layout que no sirva al mensaje. Heurística
por vertical en `references/campos-generacion.md`. Con molde propio →
`assets_upload(purpose="banner_reference")`.

**Si una referencia ya dio buen resultado, reutilízala** para las demás piezas del mismo
producto: mantiene coherencia visual en el carrusel (la ves con `banners_get`). Cuando dudes
entre dos moldes para una pieza clave, muestra los `thumbnail_url` antes de gastar el crédito.

### 4. Generar

`banners_generate` con referencia + foto + contexto de marketing → devuelve `job_id` →
`jobs_get` cada 3-5 s hasta `succeeded` (≈30-45 s). Genera **una pieza a la vez** y revísala
antes de seguir; para variantes del mismo concepto, `banners_mass_generate` (2-30, cobra 1 por
pieza). Usa `thinking_mode:"advanced"` en las piezas clave: mismo costo, mejor resultado.

Escribe TÚ el texto que va dentro de la imagen, adaptado al producto y a la pieza, con lógica de
respuesta directa (hook + beneficio + prueba). **SIN botón ni CTA clickeable** (Ley 4) y **sin
`¡` ni `¿`** (Ley 5) — ambas cosas van dichas en `additional_instructions`.

Si el resultado necesita un ajuste puntual → `banners_edit` (no rehagas de cero).
Si salió inservible → `refund_request` para recuperar el crédito.

### 5. Optimizar a WebP

El `output.url` del job es la imagen full-res. Pásala por el script (acepta URL directa):

```bash
python3 ~/.claude/skills/golden-ecom-magic/scripts/optimizar-webp.py \
  "<url_del_output>" "PRODUCTO - Galeria 01.webp" 2048x2048 300
```

### El tamaño depende del DESTINO (verificado contra Shopify, 2026-09-05)

Shopify **transforma la imagen al servirla**, así que subir chico pone un techo de nitidez que ya
no se recupera; una infografía embebida en la descripción, en cambio, se sirve tal cual.

| Destino | Tamaño | Peso | Por qué |
|---|---|---|---|
| **Galería / multimedia** (Shopify) | **2048×2048** | ~300 KB | Tamaño que Shopify recomienda para cuadradas, y el **zoom exige más de 800×800** |
| **Infografías en la descripción** | 1080×1350 | **< 150 KB** | Van tal cual al HTML, sin transformación: aquí manda el peso |
| **Creativos de pauta** | según red | < 150 KB | Los sirve la plataforma de anuncios |

**MEDIDO en la tienda real (no citado), 2026-09-05.** Se pidió la misma imagen del CDN de
Shopify con distintos `?width=`: `200` devolvió 200×200, `800` devolvió 800×800 — Shopify SÍ
redimensiona al servir — pero **`2048` devolvió 1088×1088**, el tamaño del original subido.
**Shopify NUNCA agranda por encima del archivo que subiste:** el tamaño de subida es un techo
permanente. Por eso subir 1080 condena el zoom a 1080 para siempre, y por eso la galería se
sube grande. (La conversión a WebP la decide el navegador vía `Accept`; lo medido aquí es el
redimensionado.) Doc de respaldo: `shopify.com/blog/image-sizes` + Help Center "Product media
types". Script ejecutado a esa spec: 2048×2048 → 279.3 KB. Nombra con el producto adentro, en
`PROYECTOS/<PRODUCTO>/`.

### 6. Entregar

Reúne las imágenes descargadas y pásalas a la skill que las implementa:
- **golden-shopify** → carrusel + bloques de imagen en la ficha de producto.
- **golden-ads** → creativos para pauta.

Reporta al usuario: qué piezas se generaron, en qué tamaño, peso de cada WebP, créditos
gastados y saldo restante.

## Fallback: operación por navegador

Solo si el MCP no está disponible. El mapa de pantallas, las trampas de la UI (el ícono de
basura que borra el producto, el login, el scroll dentro de textareas) y el handoff de la foto
están en **`references/ui-navegacion.md`**. Es más lento y exige acción del usuario: úsalo únicamente
como plan B, y menciónale que conectando el MCP el flujo queda 100% automático.

## Reparto con otras skills (no dupliques)

- **golden-ecom-magic** (esta) = generar las IMÁGENES con Ecom Magic.
- **golden-shopify** = montar la página con esas imágenes.
- **golden-ads** = usar las imágenes en pauta.
- **golden-ugc-avatar** = avatares/UGC y VIDEO (otra herramienta: Higgsfield). Si el usuario
  quiere video o una persona hablando, ese es el skill, no este.
- **golden-copywriting** = ángulos y copy de venta si necesitas alimentar el texto.

## Ejemplo real (validado en vivo, extremo a extremo)

Producto **Tag Recede** (spray veneno de abeja para verrugas, COD Colombia). Set de 3 piezas:

**Piezas 1 y 2 — por navegador (v1.x):** el usuario arrastró la foto al recuadro; Claude eligió
plantilla, llenó campos con datos reales (precios COP, claims del empaque, sin prometer "cura
garantizada") y generó el hero de beneficios y el antes/después. WebP 124.8 KB y 148.4 KB.
Integradas al producto en Golden Lab (Shopify) con alt-text SEO.

**Pieza 3 — por MCP (v2.0), 100% autónoma y sin tocar nada:**
1. `products_list` → producto TAG RECEDE (id 47914) ya existía **con su contexto guardado**.
2. Referencia: se reutilizó la del hero (coherencia visual en el carrusel).
3. `banners_generate` con `product_image_url` = **la URL del CDN de Shopify** (cero subida),
   `size_preset:"1080x1080"`, `thinking_mode:"advanced"`, `unique_mechanism` + `desired_outcome`
   + instrucciones de "modo de uso en 3 pasos".
4. `jobs_get` → `succeeded` en **32 s**, 1 crédito.
5. Resultado: bote real + "ELIMINA VERRUGAS desde la raíz, sin dolor" + los 3 pasos con íconos,
   texto grande, **sin botón** ✅. Único defecto: metió "¡FÁCIL DE APLICAR!" → de ahí nació la
   **Ley 5** (prohibir `¡`/`¿` en las instrucciones).
6. `optimizar-webp.py <url>` → **WebP 147.2 KB**.

**Piezas 4 y 5 — el set se cerró en 4, no en 5 (la regla de corte en acción):**
se generaron dos piezas más por MCP. La de "fórmula natural" salió limpia (WebP 142.0 KB). La de
"tipos de verrugas" falló la auditoría **tres veces seguidas**, cada vez con una invención
distinta: (1) ingredientes falsos escritos sobre la caja, (2) "Resultados Visibles Garantizados",
(3) "MÁS DE 10.000 USUARIOS SATISFECHOS". Se pidió `refund_request` de las inservibles y **se
entregó el carrusel con las 4 piezas limpias**, informando qué faltó y por qué.

De ahí salieron la **Ley 6**, la **lista negra obligatoria** y la **regla de corte** — el
aprendizaje más caro de la skill y el que evita publicar un dato falso.

Total entregado: **4 piezas limpias**, todas < 150 KB, con 2 reembolsos solicitados. La vía MCP
es la que se usa de aquí en adelante.

## Conexión con el ecosistema

Los cambios relevantes de esta skill (gotchas nuevos de la plataforma, reglas de compliance,
cambios de vía) se reportan a **🧠 GOLDEN - CENTRO DE MANDO**, que es quien decide si eso se
retransmite a las skills hermanas. Aplica sobre todo a lo que aprendemos en vivo del generador:
si inventa un claim nuevo o Meta cambia una política, el hallazgo no se queda en este chat.
Las reglas de compliance visual (ej. el corte de antes/después por vertical) tienen espejo en
`golden-imagen-arena` y `golden-ugc-avatar`: al cambiar una aquí, avisa para que se propague.

**Ley de migración de vía (nació aquí, hoy es ley de la casa).** Cuando esta skill —o cualquier
otra— cambie de vía (navegador → API/MCP, o al revés), no basta con escribir la vía nueva: hay
que **cazar las afirmaciones de la vía vieja del tipo "esto no se puede / no existe"**, porque un
modelo fresco las lee como hecho y desanda la migración. Y el barrido **no termina en esta
skill**: se hace también en las **hermanas que la citan**. Evidencia: tras limpiar la v2.2, el
Centro de Mando encontró "Ecom Magic no tiene API ni MCP" todavía vivo en
`golden-imagen-arena/references/motores.md` — la misma verdad vieja, escondida en una hermana.
Grep sugerido: `grep -rniE "no tiene (api|mcp)|no hay atajo" ~/.claude/skills`.

## Archivos de referencia

- **`references/mcp-api.md`** — **LA VÍA PRINCIPAL.** Conexión OAuth, tabla de herramientas,
  flujo autónomo, parámetros de `banners_generate` (incluido `awareness_level`) y gotchas
  verificados. Léelo al empezar cualquier trabajo.
- `references/campos-generacion.md` — Qué poner en cada campo y **cómo escribir el texto que va
  DENTRO de la imagen** (heurística de plantillas por vertical, reglas de copy). Léelo antes de
  generar.
- `references/capacidades-extra.md` — El resto del MCP (mockups, logos, spy, research,
  financial, video) y **qué es de esta skill y qué se delega**. Léelo si el usuario pide algo
  fuera de las imágenes de producto.
- `references/estrategia-pagina.md` — Por qué la ficha va híbrida (infografías + bloques
  nativos) y con qué evidencia. Léelo cuando pregunte cómo estructurar la página o cuántas piezas.
- `references/ui-navegacion.md` — **Fallback.** Mapa de pantallas y trampas de la UI web, para
  cuando el MCP no esté disponible.
- `scripts/optimizar-webp.py` — Descarga (URL o archivo) → WebP < 150 KB en el tamaño pedido.
- `references/changelog.md` — **Acta de versiones** (v2.0 → v2.7) con lo que se midió en cada
  vuelta y por qué cambió. No hace falta para trabajar; léelo si necesitas saber de dónde salió
  una regla o vas a cambiar una.

## Fronteras y desambiguacion

(Destilado 2026-09-05: aquí estaba pegada la description completa anterior, que arrastraba los
tamaños viejos y contradecía el tamaño-por-destino del paso 5. Se conservan las fronteras y se
quita el dato caduco.)

- **Entrega a:** `golden-shopify` (la página) y `golden-ads` (pauta). Produce las imágenes; no
  monta la ficha ni publica campañas.
- **NO para avatares, personas ni video** → `golden-ugc-avatar`.
- **NO para armar la página** → `golden-shopify`.
- **NO para crear un anuncio sin foto de producto**, ni para comparar motores →
  `golden-imagen-arena`. Aquí el activo es la plantilla; allá, el motor.
- **Dispara aunque no digan "Ecom Magic":** basta con "imágenes/infografías de producto de alta
  conversión para la ficha o el carrusel".
