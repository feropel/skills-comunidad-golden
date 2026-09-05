---
name: golden-chatea-pro-validacion-direcciones
description: >-
  Golden Group — Genera el PROMPT de validación de direcciones del asistente logístico de
  Chatea Pro (es el "hijo" de golden-chatea-pro-config-logistico, equivalente a lo que
  prompt-ventas es para ventas-wp). Valida la dirección del cliente antes del envío contra
  entrega (COD) para minimizar devoluciones: lee la dirección como la escribe la gente (con
  errores, emojis, mezclada con nombre y teléfono) y decide si un mensajero puede entregar
  sin llamar. Salida en UNA sola línea (dirección correcta / falta que proporcione [dato]).
  La plataforma acepta 10 países (remedido 2026-08-29). Trae packs de 8: Colombia (patrón
  oro), México, Chile, Ecuador, Panamá, Perú, Paraguay y Guatemala; Argentina y Brasil son
  soportados por la plataforma pero AÚN SIN PACK — hueco declarado, se preguntan los datos
  al negocio. Úsala cuando el usuario quiera el PROMPT de validación en sí, probar cómo se
  lee una dirección concreta, o adaptar la validación a un país nuevo.
---
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (1) FRONTMATTER YAML INVALIDO, arreglado: la description estaba escrita como escalar PLANO en una linea y su texto contenia 'dos puntos + espacio', que YAML lee como una clave nueva. Un parser estricto NO podia leer esta skill. Pasa a bloque '>-', que es inmune. No se cambio una sola palabra: cambio la FORMA de escribirla · (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 954 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden · Chatea Pro — Validación de Direcciones (hijo del logístico)

<!-- Fábrica: CENTRO DE MANDO (chat 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR) — sin fábrica de chat propia; turnos y filas van a la bandeja del CdM. -->
<!-- corrección CdM 2026-08-29 · CAMBIO DE ESTÁNDAR países: la plataforma acepta 10, no 7 (doble medición contra el bundle vivo index-BrZVg7KW.js, sha256 2c947877…; deroga 'solo 7' y 'Guatemala fuera de plataforma'; detalle en la gaceta). Menciones del conteo viejo actualizadas a 10; el resto intacto. -->
<!-- skill v2.4 · 2026-08-26 (Centro de Mando, fila de CHATEA VICENTE VIP · Zolva) · DESHORNEADAS
LAS TRANSPORTADORAS DE NEGOCIOS REALES: colombia.md traía la operación logística completa de
Golden (7 transportadoras, veto a Servientrega) violando la propia ley de la skill ("nunca
hornees datos de un negocio real"); misma clase en chile.md (Starken/Blue Express) y ecuador.md
(Gintracom "preferida"). Los tres bloques pasan a hueco [PENDIENTE — confirmar con el negocio]
como ya hacían Panamá/Perú/Paraguay; la lista de Golden se movió a
PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/GOLDEN-TRANSPORTADORAS-COLOMBIA.md (solo espacios Golden).
El patrón oro de Colombia declara la excepción por diseño en su cabecera. Guatemala (histórico
fuera de plataforma) se conserva intacto, declarado. Ejemplos con marcas reales generalizados a
[Transportadora]. -->
<!-- skill v2.3 · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando):
cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->
<!-- skill v2.2 · 2026-08-21 (auditoría golden-skill-auditor) · añadido paso 4 de VERIFICACIÓN/QA
del prompt antes de entregarlo (contrato de salida, transportadoras no inventadas, ningún
[PENDIENTE] suelto) y DEFINICIÓN DE "TERMINADO" explícita en el flujo (Proceso y flujo);
el intake del paso 3 ahora pide también qué hacer si el negocio no puede confirmar un dato en
el momento; aclarada la ruta del script de barrido como externa a esta skill con fallback manual
si no existe en el entorno (Robustez/portabilidad). Cero bugs de contenido encontrados en los 8
packs de país tras verificación cruzada línea por línea del contrato de salida (emojis, código
postal, transportadoras) — solo huecos de proceso, ya cerrados. -->
<!-- skill v2.1.1 · 2026-08-08 (centro de mando, chat CHATEA un cliente COL 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v2.1 · 2026-08-08 (centro de mando, chat CHATEA un cliente COL 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → un cliente Incanto 2026-08-08 (se colaron llave ElevenLabs, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. -->
<!-- skill v2.0 · 2026-08-07 (centro de mando, briefing BRIEFING-PARA-SKILLS.md de CHATEA-PRO-ASISTENTES-MAPA, cosecha del chat CONFIG CHATEA KEVIN MX) · REFORMA DE PAÍSES: la plataforma acepta 10 países (remedido 2026-08-29 contra el bundle vivo: se sumaron ARGENTINA, BRASIL y GUATEMALA). Revisión anti-clon país por país: México decía "NUNCA exijas código postal" — criterio de Colombia clonado y FALSO (en México el CP es REQUERIDO, define la zona de reparto); corregido en todo el pack. Chile y Ecuador revisados: su "sin CP" es criterio local válido (comuna/distrito e intersección mandan), anotado en cada pack; precisado lo de "Santiago no es comuna" en Chile (sí existe la comuna Santiago Centro, pero a secas es ambiguo). La regla global "nunca pide código postal" del contrato de salida se volvió por-país. -->
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
otra vez. Herramienta encadenable del barrido (ruta del proyecto Golden, fuera de esta skill —
si no existe en el entorno actual, hazlo a mano con el mismo criterio de patrones):
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
> **La plataforma acepta 10 (remedido 2026-08-29) países** (campo `[Comentarios IA] País`, en MAYÚSCULA y sin acentos): COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY. Nada de Guatemala, Argentina, Bolivia ni Costa Rica. Si piden un país fuera de la lista, avisa que Chatea Pro no lo acepta antes de generar nada.

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
   - 🇪🇨 Ecuador → `references/ecuador.md` (transportadoras en [PENDIENTE]; el veto a Servientrega es criterio de Golden-Colombia, no clonarlo)
   - 🇵🇦 Panamá → `references/panama.md` (transportadoras en [PENDIENTE]: preguntarlas al negocio)
   - 🇵🇪 Perú → `references/peru.md` (el distrito manda; transportadoras en [PENDIENTE])
   - 🇵🇾 Paraguay → `references/paraguay.md` (esquinas c/ y e/; transportadoras en [PENDIENTE])
   - ⛔ Guatemala → `references/guatemala.md` **(HISTÓRICO, fuera de plataforma: Chatea Pro no acepta Guatemala; no usar para configurar)**
3. **Confirma con el usuario los datos operativos del negocio** que el pack necesita (no los inventes) — o recíbelos del padre `golden-chatea-pro-config-logistico`. Pídelos TODOS de una vez (intake único, no goteado):
   - **Transportadoras habilitadas** para domicilio y para recogida en oficina (varían por negocio).
   - Si hay **recogida en oficina** y con qué transportadoras.
   - Cualquier transportadora **prohibida** por el negocio (ej.: Golden prohíbe Servientrega en su operación de Colombia — dato que vive FUERA de la skill, en CHATEA-PRO-ASISTENTES-MAPA/GOLDEN-TRANSPORTADORAS-COLOMBIA.md).
   - Si conserva los emojis de estado (✅/⚠️) o no.
   - Si el negocio no puede confirmar algún dato en el momento (caso típico: Panamá, Perú, Paraguay con transportadoras en `[PENDIENTE]`), dilo explícitamente en el entregable como pendiente con dueño — nunca inventes ni dejes el placeholder sin avisar.
4. **Verifica el prompt antes de entregarlo** (paso de QA, no te lo saltes): relee el prompt armado y confirma que cumple el contrato de salida (una sola línea, sin saludos, sin explicaciones, con o sin emoji SEGÚN el país), que las transportadoras que puso el usuario quedaron en la lista y no quedó ninguna inventada, y que ningún `[PENDIENTE]` llegó al texto final sin que el usuario lo haya resuelto o aceptado dejarlo así.
5. **Entrega el prompt final** listo para pegar en el campo de validación del asistente logístico de Chatea Pro.

**Definición de "terminado":** el prompt entregado (a) usa el pack del país correcto, (b) trae solo transportadoras confirmadas por el usuario — ninguna inventada ni heredada de otro país, (c) respeta el contrato de una sola línea de salida con el registro de cortesía del país, y (d) no contiene ningún `[PENDIENTE]` que el usuario no haya resuelto o aceptado conscientemente. Si falta cualquiera de los cuatro, no está listo para pegar.

## País nuevo (no está en references/)

Los 10 países que acepta la plataforma ya tienen pack. Si piden otro (Guatemala, Argentina, Bolivia, Costa Rica…), **primero avisa que Chatea Pro no lo acepta**: un pack para un país fuera de plataforma solo se construye si el usuario lo quiere para otro uso, o si la plataforma llega a aceptarlo. En ese caso, **constrúyelo tomando Colombia como patrón oro** y adaptando:
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

## Fronteras y desambiguacion

Para la CONFIG general del asistente logístico (transportadoras, tiempos, recogida en oficina) usa el padre golden-chatea-pro-config-logistico.
