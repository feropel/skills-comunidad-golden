---
name: golden-agenda-citas
description: >-
  Golden Group — Agendamiento automático de CITAS para negocios de servicios
  (consultorios odontológicos, estética, clínicas, salones, asesorías). Toma una
  solicitud de cita, consulta la disponibilidad real en Google Calendar, propone
  horarios libres, agenda el evento, lo confirma y prepara el recordatorio. Pensado
  para ofrecerse como SERVICIO a empresas y para gestionar la agenda propia.
  Úsala SIEMPRE que el usuario quiera: agendar una cita, gestionar la agenda de un
  negocio, montar un sistema de reservas, "agéndame con", "qué horarios hay libres",
  "reserva para el paciente/cliente", confirmar o mover citas, o configurar el
  agendamiento de un consultorio. Se apoya en el MCP de Google Calendar.
  NO usar para automatizaciones de apps externas entre sí (eso es n8n).
---

# Golden Group — Agenda de Citas

**Versión:** `GAC1.0` · Fábrica: este chat.

Convierte solicitudes de cita en eventos confirmados en Google Calendar, con disponibilidad real. Doble uso: **agenda propia** y **servicio vendible** a consultorios/clínicas.

## Herramientas (MCP Google Calendar, ya conectado)
- `list_calendars` — elegir el calendario del negocio.
- `list_events` — ver ocupación de un rango.
- `suggest_time` — proponer huecos libres.
- `create_event` — agendar (con invitado por email si se da).
- `update_event` / `delete_event` — reprogramar / cancelar.
- `get_event` — consultar detalle.

## Reglas de oro
1. **Nunca agendes encima de algo ocupado.** Verifica disponibilidad con `list_events`/`suggest_time` ANTES de crear.
2. **Confirma los 4 datos** antes de crear: servicio/motivo, fecha-hora, duración, datos del cliente (nombre + email/teléfono).
3. **Respeta horario y reglas del negocio** (horas de atención, duración por tipo de cita, buffer entre citas). Pregúntalas una vez y recuérdalas en el evento.
4. **Zona horaria explícita** (el sistema corre en LatAm; confirma país/ciudad).
5. Tras crear, **devuelve la confirmación** con el resumen y, si aplica, el texto de recordatorio para enviar por WhatsApp.

## Configuración del negocio (pregunta 1 vez)
```
Negocio: <nombre>  ·  Tipo: <odontología/estética/...>
Calendario: <cuál>  ·  Zona horaria: <...>
Horario de atención: <L-V 9-18, Sáb 9-13...>
Tipos de cita y duración: <ej. Valoración 30min, Limpieza 45min>
Buffer entre citas: <ej. 10 min>
```

## Flujo de una cita
1. **Capturar** motivo + preferencia de día/franja del cliente.
2. **Buscar huecos** con `suggest_time` / `list_events` dentro del horario de atención y duración del tipo de cita.
3. **Proponer** 2–3 opciones concretas.
4. **Confirmar** la elegida + datos del cliente.
5. **Crear** con `create_event` (título `<Servicio> — <Cliente>`, descripción con teléfono/notas, invitado si hay email).
6. **Entregar** confirmación + recordatorio listo para enviar:
```
✅ CITA CONFIRMADA
🦷 <Servicio>
📅 <día, fecha>  ⏰ <hora> (<zona>)
👤 <cliente>  ·  📞 <teléfono>
📍 <dirección/enlace>
```

## Reprogramar / Cancelar
Localiza con `get_event`/`list_events`, usa `update_event` (mover) o `delete_event` (cancelar), y reconfirma.

## Vender esto como servicio
Modelo: cobrar setup + mensualidad por gestionar la agenda del consultorio (recepcionista IA). Combínalo con un bot de WhatsApp (WhatsApp Cloud API + n8n) para que el paciente agende solo. Ofrece al usuario armar ese embudo cuando lo pida.
