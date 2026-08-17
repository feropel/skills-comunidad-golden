---
name: golden-logistica
description: >
  Golden Group — RESCATE DE NOVEDADES y control de devoluciones para COD (Dropi y
  transportadoras LatAm). Toma la lista de novedades del día (export, pantallazo o texto
  pegado de Dropi), clasifica cada guía por tipo de novedad, y entrega el PLAN DE RESCATE:
  mensaje de WhatsApp exacto para cada cliente, respuesta/solución para la transportadora,
  prioridad de ataque y checklist del día. También mide la operación (tasa de novedad, tasa
  de rescate, costo de devoluciones) con semáforo. Úsala SIEMPRE que el usuario quiera:
  gestionar/revisar/salvar novedades, "rescata estas guías", "mis pedidos están en novedad",
  bajar las devoluciones, responder novedades de Dropi, mensajes para clientes que no
  contestan o rechazan, o medir devoluciones/efectividad de entrega. Dispara con "novedad",
  "novedades", "devoluciones", "guías varadas", "en reparto fallido", "rescate COD".
  NO es la validación PREVENTIVA de direcciones (eso es golden-chatea-pro-config-logistico y
  su hijo validacion-direcciones); esta skill es el lado REACTIVO: salvar lo que ya se trabó.
---

# Golden Logística — rescate de novedades y control de devoluciones (COD)

**Versión:** `GL1.0` · Fábrica: este chat.

En COD la devolución cuesta doble (flete ida + vuelta, sin venta). Casi toda devolución
empieza como una **novedad** — y una novedad atendida en las primeras horas se salva. Esta
skill convierte la lista de novedades del día en un plan de rescate ejecutable.

## Regla de oro operativa
**Las novedades se atienden TODOS los días, temprano.** Una novedad sin gestionar 48h es una
devolución casi segura. La transportadora suele hacer 1-3 intentos; cada ciclo perdido acerca
el retorno. Velocidad > perfección.

## Modo 1 — RESCATE DIARIO (el principal)

**Entrada:** lo que el usuario tenga — export de Dropi (CSV/Excel), pantallazos del panel de
novedades, o texto pegado. No exigir formato: leer lo que llegue. Datos útiles por guía:
número de guía, cliente, teléfono, ciudad, producto, valor, tipo de novedad, intentos, fecha.

**Proceso:**
1. **Clasifica** cada guía por tipo de novedad usando `references/tipos-novedad.md`
   (dirección errada/incompleta · no contesta · rechazado · no estaba · zona de difícil
   acceso · dinero no disponible · reprogramación pedida · otro).
2. **Prioriza** el ataque: 1º mayor valor de pedido, 2º más intentos consumidos/próximas a
   vencer, 3º tipos con mayor probabilidad de rescate (no estaba > no contesta > rechazado).
3. **Genera por cada guía** (tabla o lista clara):
   - 📱 **Mensaje de WhatsApp para el cliente** — usar la plantilla del tipo (tono cercano,
     UNA pregunta concreta, sin culpar al cliente). Si el workspace tiene Chatea PRO,
     recordar que el mensaje puede salir por ahí; si no, listo para copiar y pegar.
   - 🚚 **Solución para la transportadora/Dropi** — qué marcar o responder en la novedad
     (reprogramar con fecha, corregir dirección con el dato nuevo, confirmar que sí recibe,
     cambiar teléfono). Las etiquetas EXACTAS del panel varían: **VERIFICAR EN VIVO** en el
     panel del usuario la primera vez y a partir de ahí usar sus nombres reales.
   - ⏰ **Si el cliente no responde en ~2-4h** → segundo toque (plantilla de urgencia suave).
4. **Cierra con el checklist del día:** cuántas guías, cuántas gestionadas, cuáles quedaron
   esperando respuesta del cliente y a qué hora re-tocar.

**Reglas:**
- Datos reales siempre: jamás inventar números de guía, teléfonos ni respuestas del cliente.
  Lo que falte se marca `[PENDIENTE]` y se sigue con el resto.
- Máxima autonomía: clasifica y decide por defaults e informa; pregunta solo lo que bloquee
  el rescate (ej. no hay teléfono del cliente).
- El mensaje al cliente NUNCA amenaza ni culpa; rescatar es servicio, no cobranza.

## Modo 2 — MÉTRICAS (semáforo de la operación)

Con los datos que haya (export de Dropi, resumen del mes, o números que dé el usuario):
- **Tasa de novedad** = guías con novedad / guías despachadas → 🟢 <15% · 🟡 15-25% · 🔴 >25%
- **Tasa de rescate** = novedades entregadas / novedades totales → 🟢 >60% · 🟡 40-60% · 🔴 <40%
- **Efectividad de entrega** = entregados / despachados → 🟢 >75% (CO) · 🟡 65-75% · 🔴 <65%
- **Costo de devoluciones** = devoluciones × (flete ida + retorno) → mostrarlo en plata, junto
  al margen que se salvó con los rescates del periodo.
Umbrales = referencia general COD Colombia; ajustarlos con los datos reales del usuario cuando
existan (sus números mandan). Cierra con las 2-3 acciones que más moverían la aguja.

## Modo 3 — PREVENCIÓN (bajar la novedad desde el origen)

No duplicar lo que ya existe — derivar:
- **Validación de direcciones ANTES del despacho** → `golden-chatea-pro-config-logistico` +
  `golden-chatea-pro-validacion-direcciones` (el patrón oro preventivo).
- **Confirmación del pedido por WhatsApp** antes de despachar (dirección + disponibilidad de
  pago) → recorta no-contesta y rechazos. Coordinar con el asistente de ventas de Chatea PRO.
- Revisar en métricas qué CIUDADES/zonas concentran novedad → despacho selectivo o anticipado.

## Encadenado al ecosistema
- Recibe de: la operación Dropi del usuario (exports/pantallazos) y de [[GASTO-GOLDEN]] si hay
  P&L. Complementa (no reemplaza) la validación preventiva de Chatea PRO.
- Entrega a: `golden-ads` (la efectividad de entrega alimenta el breakeven COD real) y al
  tablero de P&L del usuario.

## Referencias
- `references/tipos-novedad.md` — catálogo de tipos de novedad con: qué significa, probabilidad
  de rescate, plantilla de WhatsApp (1er y 2º toque) y solución típica en plataforma.

## Pendiente-con-dueño
- Etiquetas y flujo EXACTOS del panel de novedades de Dropi (primera sesión en vivo los
  verifica y esta skill se actualiza con los nombres reales).

## Changelog
- **GL1.0** (2026-07-11) — Creación: rescate diario (clasificar → priorizar → mensajes +
  solución → checklist), métricas con semáforo, prevención por derivación. Umbrales de
  referencia COD Colombia marcados como ajustables.
