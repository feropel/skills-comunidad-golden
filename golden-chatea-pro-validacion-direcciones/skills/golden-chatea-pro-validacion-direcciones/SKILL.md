---
name: golden-chatea-pro-validacion-direcciones
description: Golden Group — Genera el PROMPT de validación de direcciones del asistente logístico de Chatea Pro (es el "hijo" de golden-chatea-pro-config-logistico, equivalente a lo que prompt-ventas es para ventas-wp). Valida la dirección del cliente antes del envío contra entrega (COD) para minimizar devoluciones: lee la dirección como la escribe la gente (con errores, emojis, mezclada con nombre y teléfono) y decide si un mensajero puede entregar sin llamar. Salida en UNA sola línea (dirección correcta / falta que proporcione [dato]). Trae packs por país (Colombia = patrón oro; Guatemala, Chile, México, Ecuador). Úsala cuando el usuario quiera el prompt de validación de direcciones en sí, "el bot que revisa direcciones", validar una dirección, o adaptar la validación a un país nuevo. Para la CONFIG general del asistente logístico (transportadoras, tiempos, recogida en oficina) usa el padre golden-chatea-pro-config-logistico.
---

# Golden · Chatea Pro — Validación de Direcciones (hijo del logístico)

Genera el **prompt de validación de direcciones**: el cerebro del asistente logístico. Su trabajo es leer la dirección que escribió el cliente y decidir si un mensajero podría **entregar sin llamar**. Si sí → la aprueba. Si falta algo → pide exactamente el dato faltante.

Esta skill es el **hijo** de `golden-chatea-pro-config-logistico` (el padre configura el asistente logístico completo; esta genera el prompt de validación que va dentro). Es el análogo de `golden-chatea-pro-prompt-ventas` dentro de `golden-chatea-pro-config-ventas-wp`.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. El prompt se genera con el pack del país del workspace.

## Contrato de salida (obligatorio, una sola línea)

El asistente responde **exactamente** uno de dos casos, sin saludos, sin explicaciones, sin emojis extra:

- **Entregable** → la frase literal (señal interna de "validada"): `dirección correcta`
- **Falta info** → la pide en registro local cordial: `Para completar su envío, nos regala [el dato que falta]?`

Evalúa SIEMPRE la dirección **completa acumulada** en la conversación; responde `dirección correcta` solo cuando ya no quede duda operativa. Nunca pide código postal como requisito.

## Principio rector

> Si un mensajero/repartidor puede llegar sin llamar → **válida**. Si hay riesgo real de devolución → **falta info**.

Dos capacidades del prompt:
1. **Interpretar** cómo escribe la gente (nomenclatura, barrios, conjuntos/torres, rural, GPS), aun con errores.
2. **Pedir** el dato faltante en el registro de atención del país (en Colombia: trato de usted, "nos regala…?").

## Cómo generar el prompt (flujo)

1. **Pregunta el país** del workspace.
2. **Carga el pack del país** desde `references/` y úsalo como base:
   - 🇨🇴 Colombia → `references/colombia.md` **(patrón oro: estructura, tono y exigencia de referencia)**
   - 🇬🇹 Guatemala → `references/guatemala.md`
   - 🇨🇱 Chile → `references/chile.md`
   - 🇲🇽 México → `references/mexico.md`
   - 🇪🇨 Ecuador → `references/ecuador.md`
3. **Confirma con el usuario los datos operativos del negocio** que el pack necesita (no los inventes) — o recíbelos del padre `golden-chatea-pro-config-logistico`:
   - **Transportadoras habilitadas** para domicilio y para recogida en oficina (varían por negocio).
   - Si hay **recogida en oficina** y con qué transportadoras.
   - Cualquier transportadora **prohibida** (ej. en el pack de Colombia, Servientrega no se usa).
   - Si conserva los emojis de estado (✅/⚠️) o no.
4. **Entrega el prompt final** listo para pegar en el campo de validación del asistente logístico de Chatea Pro.

## País nuevo (no está en references/)

Si el país no tiene pack, **constrúyelo tomando Colombia como patrón oro** y adaptando:
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
