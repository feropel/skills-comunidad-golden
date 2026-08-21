---
name: golden-agenda-citas
description: >-
  Golden Group — Agendamiento automático de CITAS para negocios de servicios
  (consultorios odontológicos, estética, clínicas, salones, asesorías, spas,
  entrenadores). Toma una solicitud de cita, consulta la disponibilidad real
  en Google Calendar, propone horarios libres, agenda el evento, lo confirma
  y prepara el recordatorio. Pensado para ofrecerse como SERVICIO a empresas
  y para gestionar la agenda propia (asesorías Golden, VIP, mentorías).
  Úsala SIEMPRE que el usuario quiera: agendar una cita, gestionar la agenda
  de un negocio, montar un sistema de reservas, "agéndame con", "qué horarios
  hay libres", "reserva para el paciente/cliente", confirmar, mover o
  cancelar citas, avisar de un choque de horario, o configurar el
  agendamiento de un consultorio/negocio. Se apoya en el MCP de Google
  Calendar (list_calendars, list_events, suggest_time, create_event,
  update_event, delete_event, get_event) — si esas tools no responden, la
  skill lo declara en vez de inventar disponibilidad.
  NO usar para: automatizar el cruce entre varias apps (Shopify/Dropi/Sheets)
  o webhooks — eso es golden-automatizacion; montar el bot de WhatsApp que
  recibe la solicitud del paciente antes de que llegue aquí — eso es la
  familia golden-chatea-pro-*; cobrar el setup/mensualidad del servicio —
  eso es golden-cobros / golden-finanzas.
---

# Golden Group — Agenda de Citas

<!-- skill v1.1 · 2026-08-21 · auditoría golden-skill-auditor: quitó el emoji 🦷 fijo (fosilizado a odontología pese a declarar negocio genérico), agregó casos borde (sin huecos, MCP caído, choque de horario, cliente sin contacto, zona horaria ambigua), manejo de error por paso, checklist de "terminado", ejemplo end-to-end, y delegación explícita a golden-automatizacion / golden-chatea-pro-* / golden-cobros. Reserva declarada: aún sin corrida en vivo contra un Google Calendar real con datos de un consultorio — validar el primer caso real y anotar aquí el resultado. -->
<!-- skill v1.0 · fábrica de este chat · primera versión -->

Convierte solicitudes de cita en eventos confirmados en Google Calendar, con disponibilidad real verificada antes de crear nada. Doble uso: **agenda propia** (asesorías/VIP de Golden) y **servicio vendible** a consultorios/clínicas/salones.

**Reserva de campo:** esta skill no se ha corrido todavía punta a punta contra un calendario real de producción (solo diseñada y auditada). El primer uso real es la prueba — si algo del flujo no encaja con la plataforma real (nombres de campos, franjas, invitados), corrígelo aquí mismo y sube la versión.

## Herramientas (MCP Google Calendar)

Asume que el MCP ya está conectado. Antes del primer paso de cada sesión, confirma con un `list_calendars` que responde — si falla o no hay MCP de Calendar en las tools disponibles, dilo de inmediato ("no tengo conexión al calendario de Google en esta sesión; conéctalo o dime qué horarios están libres y yo preparo el evento cuando lo actives") y NO inventes disponibilidad ni horarios.

- `list_calendars` — elegir el calendario del negocio (si hay más de uno, pregúntalo en el intake, no en cada cita).
- `list_events` — ver ocupación real de un rango antes de proponer u ofertar horas.
- `suggest_time` — proponer huecos libres dentro del horario de atención.
- `create_event` — agendar (con invitado por email si el cliente lo dio).
- `update_event` / `delete_event` — reprogramar / cancelar.
- `get_event` — consultar detalle de una cita ya creada.

## Reglas de oro (con el porqué)

1. **Nunca agendes encima de algo ocupado.** Verifica con `list_events` (y `suggest_time`) ANTES de `create_event`. Un doble booking no se revierte solo con "lo siento" — el negocio pierde la cita o el paciente llega y no lo atienden.
2. **Confirma los 4 datos antes de crear:** servicio/motivo, fecha-hora, duración, datos del cliente (nombre + email o teléfono — al menos uno de los dos, para poder recordar o reprogramar). Crear sin esto produce eventos huérfanos que nadie puede contactar si hay que mover la cita.
3. **Respeta horario y reglas del negocio** (horas de atención, duración por tipo de cita, buffer entre citas). Pregúntalas UNA vez en el intake y reutilízalas — repreguntar cada vez es la fuga que la regla de autonomía Golden prohíbe.
4. **Zona horaria explícita, siempre.** El sistema corre en LatAm con varios países/ciudades posibles; si el negocio y el cliente pueden estar en zonas distintas, confírmalo antes de proponer horas — una hora sin zona clara agenda a la hora equivocada y nadie se entera hasta que uno de los dos falta.
5. Tras crear, **devuelve la confirmación** con el resumen y, si aplica, el texto de recordatorio listo para copiar y enviar por WhatsApp/email.
6. **Verifica lo que quedó creado.** Después de `create_event`, haz un `get_event` (o revisa la respuesta de la tool) y confirma que fecha, hora y duración coinciden con lo pactado antes de decirle al cliente "confirmado" — es el paso de QA de esta skill; sin él, un evento mal creado se reporta como éxito.

## Configuración del negocio (intake — pregunta 1 sola vez, al inicio)

```
Negocio: <nombre>  ·  Tipo: <odontología/estética/salón/asesoría/spa/entrenador/...>
Calendario: <cuál, si hay varios>  ·  Zona horaria: <ciudad/país>
Horario de atención: <ej. L-V 9-18, Sáb 9-13>
Tipos de cita y duración: <ej. Valoración 30min, Limpieza 45min, Sesión 60min>
Buffer entre citas: <ej. 10 min>
Ícono/emoji para la confirmación (opcional): <ej. 🦷 odontología, 💆 spa, 📋 asesoría — si no lo da, usa 📅 genérico>
```

Si el usuario no completa un campo, usa el default sano por convención e INFORMA qué asumiste (ej. sin buffer indicado → asume 10 min y dilo); solo lo que nadie más que el dueño del negocio sabe (horario real, duración real por tipo de cita) se pregunta, nunca se inventa.

## Flujo de una cita

1. **Capturar** motivo + preferencia de día/franja del cliente.
2. **Elegir calendario** (si el intake reportó más de uno; si es uno solo, úsalo directo sin preguntar).
3. **Buscar huecos** con `list_events` + `suggest_time`, dentro del horario de atención y la duración del tipo de cita, respetando el buffer.
   - **Si no hay huecos** en la franja pedida: amplía el rango (mismo día más tarde, o próximos 2-3 días hábiles) y ofrécelo — nunca respondas solo "no hay disponibilidad" sin alternativa.
4. **Proponer** 2–3 opciones concretas con fecha, hora y zona horaria explícitas.
5. **Confirmar** la opción elegida + los 4 datos del cliente (regla 2).
6. **Crear** con `create_event`: título `<Servicio> — <Cliente>`, descripción con teléfono/notas, invitado si hay email, duración y buffer ya incorporados al bloque.
7. **Verificar (QA)** con `get_event` que lo creado coincide con lo pactado (regla 6).
8. **Entregar** confirmación + recordatorio listo para enviar:

```
✅ CITA CONFIRMADA
<ícono del negocio o 📅>  <Servicio>
📅 <día, fecha>  ⏰ <hora> (<zona horaria>)
👤 <cliente>  ·  📞/✉️ <contacto>
📍 <dirección o enlace de la reunión>
```

**Definición de "terminado":** la cita cuenta como agendada solo cuando (a) `create_event` respondió sin error, (b) el `get_event` de verificación muestra los mismos datos pactados, y (c) el usuario recibió el bloque de confirmación de arriba. Si falta cualquiera de los tres, la cita NO está lista — dilo explícitamente en vez de dar la confirmación por hecha.

## Casos borde

- **El MCP de Calendar no responde o no está conectado:** dilo de inmediato, no ofrezcas horarios inventados ni crees el evento "a ciegas". Pide al usuario que lo conecte o confirma que reintentarás cuando esté disponible.
- **`create_event` falla** (permiso, calendario equivocado, conflicto detectado por Google): repórtalo tal cual devuelve la tool, no lo traduzcas a "listo" — vuelve al paso 3 con el hueco siguiente.
- **El cliente no tiene ni email ni teléfono:** no crees el evento sin al menos un contacto (regla 2) — explica por qué hace falta (no se puede recordar ni reprogramar a nadie) y pide uno de los dos antes de continuar.
- **El cliente pide una hora ya ocupada:** no la agendes ni la "acomodes" moviendo otra cita sin permiso; ofrece las alternativas más cercanas libres.
- **Zona horaria ambigua** (negocio y cliente en países distintos, o el cliente no la menciona): confírmala explícitamente antes de proponer horas — nunca asumas que ambos están en la misma.
- **El negocio tiene más de un calendario y no dijo cuál:** pregúntalo una vez en el intake (paso de Configuración), no lo adivines por el nombre del servicio.

## Reprogramar / Cancelar

1. Localiza la cita con `get_event` (si tienes el id) o `list_events` (buscando por cliente/fecha aproximada).
2. **Reprogramar:** repite pasos 3–7 del Flujo para encontrar el nuevo hueco, luego `update_event` con la nueva fecha/hora — nunca sobreescribas sin haber verificado que el nuevo horario está libre.
3. **Cancelar:** `delete_event`, y entrega confirmación de cancelación al cliente (mismo formato que la confirmación de creación, marcando "❌ CITA CANCELADA").
4. Reconfirma con el cliente el resultado final en ambos casos (QA de la regla 6 aplica también aquí).

## Ejemplo end-to-end

```
Usuario: "Agenda una limpieza para María López el jueves en la tarde,
su celular es 300-000-0000."

1. Intake ya hecho (negocio: consultorio Sonrisa Sana, L-V 9-18, Limpieza=45min, buffer=10min, zona=Bogotá).
2. list_events del jueves → ocupado 14:00-15:00 y 16:00-16:45.
3. suggest_time devuelve libres: 15:10, 17:00.
4. Propuesta: "Tengo jueves 15:10 o 17:00 (hora Bogotá), 45 min. Cuál prefieres."
5. Usuario elige 15:10. Confirmo datos: María López, 300-000-0000, Limpieza.
6. create_event: "Limpieza — María López", jueves 15:10-15:55 (+10min buffer hasta 16:05),
   descripción "Tel: 300-000-0000".
7. get_event confirma: mismo horario, mismo título. OK.
8. Entrego:
   ✅ CITA CONFIRMADA
   🦷 Limpieza
   📅 Jueves, [fecha]  ⏰ 15:10 (Bogotá)
   👤 María López  ·  📞 300-000-0000
   📍 [dirección del consultorio]
```

## Vender esto como servicio

Modelo: cobrar setup + mensualidad por gestionar la agenda del consultorio (recepcionista IA) — la propuesta comercial y el precio los arma **golden-finanzas**, y el cobro recurrente **golden-cobros**. Combínalo con un bot de WhatsApp para que el paciente agende solo: el flujo conversacional lo monta la familia **golden-chatea-pro-***, y si hace falta cruzar esto con otras apps (Sheets, CRM, notificaciones) eso es **golden-automatizacion**. Ofrece al usuario armar ese embudo completo cuando lo pida — esta skill solo pone el calendario a funcionar, no reemplaza a esas skills hermanas.
