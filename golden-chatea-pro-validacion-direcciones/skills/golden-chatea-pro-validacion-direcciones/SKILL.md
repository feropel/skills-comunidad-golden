---
name: golden-chatea-pro-validacion-direcciones
description: Golden Group — Genera el PROMPT de validación de direcciones del asistente logístico de Chatea Pro (es el "hijo" de golden-chatea-pro-config-logistico, equivalente a lo que prompt-ventas es para ventas-wp). Valida la dirección del cliente antes del envío contra entrega (COD) para minimizar devoluciones: lee la dirección como la escribe la gente (con errores, emojis, mezclada con nombre y teléfono) y decide si un mensajero puede entregar sin llamar. Salida en UNA sola línea (dirección correcta / falta que proporcione [dato]). Trae packs de los 7 países que acepta la plataforma (Colombia = patrón oro; México, Chile, Ecuador, Panamá, Perú, Paraguay; Guatemala quedó como histórico fuera de plataforma). Úsala cuando el usuario quiera el PROMPT de validación en sí, probar cómo se lee una dirección concreta, o adaptar la validación a un país nuevo. Para la CONFIG general del asistente logístico (transportadoras, tiempos, recogida en oficina) usa el padre golden-chatea-pro-config-logistico.
---

# Golden · Chatea Pro — Validación de Direcciones (hijo del logístico)

<!-- skill v2.1.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v2.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → otra marca 2026-08-08 (se colaron una credencial, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. -->
<!-- skill v2.0 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat CONFIG CHATEA KEVIN MX) · REFORMA DE PAÍSES: la plataforma solo acepta 7 (COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY) — creados los packs de Panamá, Perú y Paraguay (transportadoras en [PENDIENTE], se preguntan al negocio, jamás se inventan) y Guatemala marcada FUERA DE PLATAFORMA/histórico sin borrar el archivo. Revisión anti-clon país por país: México decía "NUNCA exijas código postal" — criterio de Colombia clonado y FALSO (en México el CP es REQUERIDO, define la zona de reparto); corregido en todo el pack. Chile y Ecuador revisados: su "sin CP" es criterio local válido (comuna/distrito e intersección mandan), anotado en cada pack; precisado lo de "Santiago no es comuna" en Chile (sí existe la comuna Santiago Centro, pero a secas es ambiguo). La regla global "nunca pide código postal" del contrato de salida se volvió por-país. -->
<!-- v1.x · sin sello previo (5 packs: Colombia, Guatemala, Chile, México, Ecuador) -->

## LEY: NUNCA HEREDAR DATOS ENTRE ESPACIOS (FER 2026-08-08)

Al basarse en una cuenta guía (Golden o cualquier otra) se hereda **estructura, prompts y
configuración de asistentes** — JAMÁS datos, en ninguna dirección, ni entre marcas propias:

- **APIs y tokens** de cualquier tipo: ElevenLabs, OpenAI, Dropi, Shopify, el token del propio bot.
- **Plantillas de WhatsApp**: `name`, `namespace`, `lang` y `status` van atados al WABA de cada
  espacio; copiarlas rompe el destino (llama plantillas que su WABA no tiene o que Meta no aprobó).
- **Datos personales y de marca**: teléfonos, correos, dominios, nombre de la empresa, firmas en
  mensajes al cliente.
- **Productos** y sus disparadores.
- **Claims y cifras de negocio**: años en el mercado, número de clientes, porcentajes de
  entrega, premios. Heredarlos no rompe nada técnico — ningún barrido de llaves los detecta —
  pero ponen al bot a MENTIRLE al cliente con datos de otra empresa. Caso real (2026-08-08): la
  plantilla maestra clonada traía "Más de 100.000 clientes atendidos en Colombia" (dato de
  Golden) a punto de quedar en boca del bot de otro espacio.

**Única excepción autorizada:** Le'côterra como producto-ejemplo en los espacios de trabajo
(asistente de WhatsApp y de comentarios), para que la gente vea cómo se configura un producto.

**La guía tampoco puede llevar nada de eso adentro**: un material de referencia con una llave o un
dato personal ya está mal, aunque nadie lo copie.

**Método obligatorio al escribir en un espacio ajeno** — ANTES de escribir, barrer lo que se va a
escribir buscando `sk_`, `shpat_`, `eyJ`, teléfonos, correos, dominios, nombres de plantilla y de
marca del origen; si aparece algo, NO se escribe. DESPUÉS de escribir: releer del servidor y barrer
otra vez. Herramienta encadenable del barrido:
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (correrla ANTES de escribir y DESPUÉS releyendo del
servidor; sale con código 3 si encuentra algo CRITICA).

**LA MARCA VIVE TAMBIÉN EN PROSA LIBRE, no solo en campos estructurados.** Preservar las
llaves de identidad del destino NO basta: el nombre de la marca de origen viaja escondido dentro
de ganchos posventa, agradecimientos y plantillas de prompt. Al método de barrido se le añade el
paso `grep -i` por el NOMBRE de la marca de origen sobre TODO el texto que se va a escribir —
así se cazaron 10 menciones de la marca origen en 3 campos del destino que el mapeo de llaves
no vio.

Origen: 2026-08-08, al clonar la config de Golden a otro espacio se colaron la llave de ElevenLabs,
el teléfono, la plantilla de notificación y agradecimientos firmados con la marca del origen.
Revertido el mismo día desde respaldo.

Genera el **prompt de validación de direcciones**: el cerebro del asistente logístico. Su trabajo es leer la dirección que escribió el cliente y decidir si un mensajero podría **entregar sin llamar**. Si sí → la aprueba. Si falta algo → pide exactamente el dato faltante.

Esta skill es el **hijo** de `golden-chatea-pro-config-logistico` (el padre configura el asistente logístico completo; esta genera el prompt de validación que va dentro). Es el análogo de `golden-chatea-pro-prompt-ventas` dentro de `golden-chatea-pro-config-ventas-wp`.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. El prompt se genera con el pack del país del workspace.
> **La plataforma solo acepta 7 países** (campo `[Comentarios IA] País`, en MAYÚSCULA y sin acentos): COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY. Nada de Guatemala, Argentina, Bolivia ni Costa Rica. Si piden un país fuera de la lista, avisa que Chatea Pro no lo acepta antes de generar nada.

## Contrato de salida (obligatorio, una sola línea)

El asistente responde **exactamente** uno de dos casos, sin saludos, sin explicaciones, sin emojis extra:

- **Entregable** → la frase literal (señal interna de "validada"): `dirección correcta`
- **Falta info** → la pide en registro local cordial: `Para completar su envío, nos regala [el dato que falta]?`

Evalúa SIEMPRE la dirección **completa acumulada** en la conversación; responde `dirección correcta` solo cuando ya no quede duda operativa.

**El código postal es criterio POR PAÍS, no global** (trampa que ya nos mordió: el pack de México heredó de Colombia un "NUNCA exijas código postal" que en México es falso): en **México el CP es REQUERIDO** — define la zona de reparto de la paquetería; en Colombia, Chile, Ecuador, Panamá, Perú y Paraguay **no se pide** (mandan barrio/comuna/distrito/corregimiento y las referencias). Cualquier país clonado de otra plantilla hereda el criterio equivocado: al tocar un pack, revisar criterio por criterio contra el país real, no asumir.

## Principio rector

> Si un mensajero/repartidor puede llegar sin llamar → **válida**. Si hay riesgo real de devolución → **falta info**.

Dos capacidades del prompt:
1. **Interpretar** cómo escribe la gente (nomenclatura, barrios, conjuntos/torres, rural, GPS), aun con errores.
2. **Pedir** el dato faltante en el registro de atención del país (en Colombia: trato de usted, "nos regala…?").

## Cómo generar el prompt (flujo)

1. **Pregunta el país** del workspace.
2. **Carga el pack del país** desde `references/` y úsalo como base (los 7 que acepta la plataforma):
   - 🇨🇴 Colombia → `references/colombia.md` **(patrón oro: estructura, tono y exigencia de referencia)**
   - 🇲🇽 México → `references/mexico.md` (CP REQUERIDO; sin recogida en oficina; emojis ✅/⚠️)
   - 🇨🇱 Chile → `references/chile.md` (la comuna es el dato rey)
   - 🇪🇨 Ecuador → `references/ecuador.md` (Servientrega SÍ habilitada; agencia en [PENDIENTE])
   - 🇵🇦 Panamá → `references/panama.md` (transportadoras en [PENDIENTE]: preguntarlas al negocio)
   - 🇵🇪 Perú → `references/peru.md` (el distrito manda; transportadoras en [PENDIENTE])
   - 🇵🇾 Paraguay → `references/paraguay.md` (esquinas c/ y e/; transportadoras en [PENDIENTE])
   - ⛔ Guatemala → `references/guatemala.md` **(HISTÓRICO, fuera de plataforma: Chatea Pro no acepta Guatemala; no usar para configurar)**
3. **Confirma con el usuario los datos operativos del negocio** que el pack necesita (no los inventes) — o recíbelos del padre `golden-chatea-pro-config-logistico`:
   - **Transportadoras habilitadas** para domicilio y para recogida en oficina (varían por negocio).
   - Si hay **recogida en oficina** y con qué transportadoras.
   - Cualquier transportadora **prohibida** (ej. en el pack de Colombia, Servientrega no se usa).
   - Si conserva los emojis de estado (✅/⚠️) o no.
4. **Entrega el prompt final** listo para pegar en el campo de validación del asistente logístico de Chatea Pro.

## País nuevo (no está en references/)

Los 7 países que acepta la plataforma ya tienen pack. Si piden otro (Guatemala, Argentina, Bolivia, Costa Rica…), **primero avisa que Chatea Pro no lo acepta**: un pack para un país fuera de plataforma solo se construye si el usuario lo quiere para otro uso, o si la plataforma llega a aceptarlo. En ese caso, **constrúyelo tomando Colombia como patrón oro** y adaptando:
- Nomenclatura de dirección local (calles/avenidas/colonias/comunas/etc.).
- Transportadoras reales del país (pregúntalas, no las inventes).
- Registro de cortesía local (usted/tú, muletillas de servicio).
- Reglas de vivienda colectiva, rural y recogida en oficina equivalentes.
Mantén SIEMPRE el contrato de salida de una sola línea y el principio rector. Guarda el nuevo pack en `references/<pais>.md` para reutilizarlo.

## Reglas de oro
- **Nunca inventes transportadoras ni datos del negocio:** se preguntan/confirman por país y por tienda.
- **No pidas de más:** si la dirección ya trae puerta, apto, torre, bloque, barrio claro o referencia fuerte, es válida. Solo pide ante duda operativa real.
- **Una sola línea de salida, siempre.** El bot ya saludó; este prompt no saluda ni explica.

## Conexiones
- 📦 Padre (config del asistente logístico) → `golden-chatea-pro-config-logistico`
- 🛒 Asistente de ventas (dispara el logístico al pedir la dirección) → `golden-chatea-pro-config-ventas-wp`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Los packs de país traen lógica y ejemplos genéricos. Nunca hornees datos de un negocio real (transportadoras contratadas, tienda, cuentas). Se preguntan en cada uso.
