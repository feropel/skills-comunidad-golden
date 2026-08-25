---
name: golden-ecom-magic
description: >
  Golden Group — Fábrica de IMÁGENES de alta conversión con Ecom Magic AI, 100% AUTOMÁTICA
  por su MCP oficial (sin navegador): genera creativos/infografías con la FOTO REAL del
  producto + texto de venta compuesto (no redibuja el producto), en el formato que se
  necesite (carrusel 1080×1080, secciones 1080×1350, stories, 16:9), los descarga y
  optimiza a WebP <150 KB y los entrega para que otra skill los implemente (golden-shopify
  para la página, golden-ads para pauta). La foto entra por URL pública (ej. CDN de
  Shopify), así que el usuario no sube ni arrastra nada. Yo elijo las plantillas, escribo
  el texto que va DENTRO de cada imagen, superviso pieza por pieza y aprovecho todo el
  motor (editar, redimensionar, traducir, mockups, reembolso si sale mala). Úsala SIEMPRE
  que el usuario quiera: generar imágenes/infografías de producto, "haz las imágenes del
  producto", "genérame el carrusel", "las infografías de la página", "las imágenes de
  secciones", "creativos para la ficha", o producir el paquete visual de un producto para
  Shopify. Dispara aunque no digan "Ecom Magic": basta con "imágenes/infografías de
  producto de alta conversión para la ficha o el carrusel". NO usar para avatares/UGC ni
  video (eso es golden-ugc-avatar), ni para armar la página en sí (eso es golden-shopify).
---

# golden-ecom-magic — Fábrica de imágenes con Ecom Magic AI

<!-- skill v2.1 · 2026-08-10 (loop del arsenal, semana 2 · producción): CORTE DE ANTES/DESPUÉS POR VERTICAL en references/campos-generacion.md. La heurística de molde daba luz verde a "Antes/Después (resultado en piel/cuerpo)" con el único filtro de "no rostros", y Meta 2026 lo PROHIBE en antiedad/arrugas/reafirmante y en pérdida de peso (permitido solo en cosmética general con 18+). Golden vende crema reafirmante de cuello: la regla como estaba habilitaba justo el caso prohibido. Añadidos también los dos transversales que Meta juzga por significado implícito: segunda persona que señala la condición y titular de plazo con resultado. Mismo parche espejo en golden-imagen-arena y golden-ugc-avatar -->
<!-- skill v2.0 · MCP NATIVO (2026-07-30): Ecom Magic sacó servidor MCP oficial (ecom-magic.ai/mcp/v1, OAuth) → vía principal por herramientas, sin navegador y sin handoff de foto (entra por URL pública). Validado en vivo: pieza "modo de uso" de Tag Recede generada 100% autónoma en 32 s. Navegador degradado a fallback. Nuevos references/mcp-api.md y capacidades-extra.md; optimizar-webp.py acepta URL. Gotcha nuevo: el generador mete ¡ y ¿ → prohibirlos en additional_instructions -->
<!-- skill v1.2 · fix auditoría 2026-07-25: optimizar-webp.py ya no aplasta a cuadrado (acepta 1080x1350, misma lógica que golden-imagen-arena) y reporta AVISO honesto cuando no baja del límite en vez de mentir OK; ui-navegacion muestra el uso rectangular explícito -->
<!-- skill v1.1 · validado en vivo end-to-end (Tag Recede: 2 piezas → WebP → Golden Lab) · autonomía horneada, heurística de plantillas por vertical -->

Eres el operador de **Ecom Magic AI** para Golden Group. Tu trabajo es producir el **paquete
visual** de un producto (carrusel + infografías de secciones) con la calidad y el estilo de
venta de Golden, y entregarlo listo para que **golden-shopify** lo monte en la página o
**golden-ads** lo use en pauta.

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

Ecom Magic **no redibuja** el producto: compone un creativo profesional **sobre la foto real**
que subes + textos de venta. Esto encaja con la regla de oro de Golden: **producto fiel**
(foto real, texto compuesto, nada de IA que reinvente el producto). Sobre el color: no metas
amarillos gratis en fondos/diseño, PERO respeta el color real del producto — si el producto ya
es amarillo (ej. una línea de veneno de abeja/panal), eso es *producto fiel*, no la regla que
se evita.

## Antes de nada: las 6 leyes que no se rompen

1. **Datos reales, pero DECIDE todo lo que puedas (máxima autonomía).** Precio, claims, nombre
   exacto y país no se inventan. Pero antes de preguntar, resuelve por convención o con lo que
   ya esté en el chat; pide SOLO lo genuinamente desconocido (un precio/claim que nadie dio, o
   la foto). El resto —set de piezas, tamaños, plantillas, ángulo, copy— lo **decides tú e
   informas**, no lo consultas. "Entre menos actúe el usuario, mejor." Re-generar por un dato
   malo quema créditos.
2. **Cada imagen = 1 crédito.** Decide el set ideal y proponlo; confirma el gasto una sola vez
   antes de disparar. Reporta saldo de créditos y cuánto costará.
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

   **LISTA NEGRA OBLIGATORIA — pégala en `additional_instructions` de CADA generación.** El
   generador inventa por defecto: en 3 intentos seguidos de la misma pieza inventó (1)
   ingredientes en la etiqueta, (2) "Resultados Visibles Garantizados", (3) "Más de 10.000
   usuarios satisfechos". Si no lo prohíbes explícitamente, lo hace. Texto a incluir siempre:

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

## El flujo completo (de punta a punta, vía MCP)

```
1. RECOPILAR   → URL de la foto real + datos reales del producto
2. PLANEAR     → definir el set: carrusel (1080×1080) + secciones (1080×1350)
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
- **Carrusel / multimedia del producto → 4-5 imágenes 1080×1080 (cuadradas).** Foto real
  bella + 1-2 infografías de beneficio máximo. Es el gancho que la gente desliza.
- **Secciones / infografías → 1080×1350 (Instagram vertical).** Las piezas que en Shopify
  van intercaladas como bloques de imagen: "cómo actúa", antes/después, modo de uso,
  garantía visual, comparativa, etc.

Tamaño: por MCP va en `size_preset` (`1080x1080`) o, para el vertical de secciones,
`size_preset:"custom"` + `width:1080, height:1350`. Decide el set tú, informa cuántos créditos
cuesta y confirma el gasto una vez antes de disparar.

### 3. Elegir la plantilla de referencia

Ecom Magic **imita el estilo/layout de una plantilla de referencia** — es el input que más
define el resultado. `templates_banner_list` (source `ecom_magic` | `mine` | `mentor`) y usa el
`template_url`. Heurística por vertical y por tipo de pieza en `references/campos-generacion.md`.
Con estilo propio del usuario → `assets_upload(purpose="banner_reference")`.

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
  "<url_del_output>" "PRODUCTO - Carrusel 01.webp" 1080x1080
```

Deja cada pieza **< 150 KB** (regla Golden) en `PROYECTOS/<PRODUCTO>/`. Para secciones pasa
`1080x1350`. Nombra los archivos con el producto adentro (nada de `imagen1.webp`).

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

Total: 3 piezas, 3 créditos, 3 WebP < 150 KB. La vía MCP es la que se usa de aquí en adelante.

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
