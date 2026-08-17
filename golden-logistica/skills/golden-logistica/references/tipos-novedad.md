# Catálogo de tipos de novedad — rescate por tipo

Para cada tipo: qué significa, probabilidad de rescate (referencia), plantilla de WhatsApp
(1er toque + 2º toque) y la solución típica en plataforma. Personalizar SIEMPRE con: nombre
del cliente, producto y ciudad reales. `{campos}` se llenan con datos reales — jamás inventados.
Tono: cercano, servicial, UNA pregunta concreta. Nunca culpar. Sin signos de apertura.

---

## 1. Dirección errada / incompleta
**Qué es:** el mensajero no ubicó la dirección. **Rescate:** ALTA si el cliente responde.
- **1er toque:** "Hola {nombre}! 👋 Soy del equipo de {tienda}. Tu {producto} ya está en
  {ciudad} para entregarte 🎉 pero el mensajero no logró ubicar la dirección. Me confirmas
  la dirección completa (calle/carrera, número, barrio y alguna referencia)? Así te lo
  llevan hoy mismo."
- **2º toque (2-4h):** "Hola {nombre}, tu pedido sigue reservado para ti 📦 solo me falta
  confirmar la dirección para que salga en el próximo reparto. Me la envías por aquí?"
- **Plataforma:** responder la novedad con la dirección corregida + referencia. Verificar la
  dirección nueva con el patrón de validación (skill logístico) antes de reenviar.

## 2. Cliente no contesta / teléfono apagado
**Qué es:** intentaron llamar y no respondió. **Rescate:** MEDIA-ALTA (el WhatsApp entra
donde la llamada no).
- **1er toque:** "Hola {nombre}! Tu {producto} está en reparto en {ciudad} 🚚 La
  transportadora intentó llamarte para coordinar la entrega. A qué hora te queda bien
  recibirlo hoy o mañana?"
- **2º toque:** "{nombre}, no queremos que tu pedido se devuelva 🙏 el mensajero hace su
  último intento pronto. Me confirmas con un OK si lo recibes en {dirección}?"
- **Plataforma:** reprogramar con la franja confirmada; si dio otro teléfono, actualizarlo.

## 3. Rechazado por el cliente
**Qué es:** dijo que ya no lo quiere. **Rescate:** BAJA-MEDIA — vale UN intento con empatía
+ recordar el valor (no rogar, no presionar).
- **1er toque:** "Hola {nombre}, vi que hubo un inconveniente con la entrega de tu
  {producto}. Te escribo para entender qué pasó — si fue el momento o el valor, dime y
  buscamos la forma (por ejemplo te lo llevan otro día sin costo extra). Si definitivamente
  ya no lo necesitas, lo cancelo sin problema. Tú me dices 🙌"
- **Plataforma:** si acepta → reprogramar; si confirma rechazo → autorizar retorno YA (cada
  día de bodega también cuesta). Registrar el motivo para métricas.

## 4. No estaba en casa / destinatario ausente
**Qué es:** llegaron y no había quién recibiera. **Rescate:** LA MÁS ALTA — casi siempre es
tema de horario.
- **1er toque:** "Hola {nombre}! El mensajero pasó hoy con tu {producto} y no te encontró 😅
  Nada grave: me dices en qué horario estás en casa (mañana o tarde) y lo reprogramo de una?
  También puede recibirlo alguien más si me das su nombre."
- **Plataforma:** reprogramar con franja + nombre de quien recibe.

## 5. Zona de difícil acceso / no hay cobertura al punto
**Qué es:** la transportadora no llega hasta la dirección. **Rescate:** MEDIA — se salva con
punto de encuentro u oficina.
- **1er toque:** "Hola {nombre}! Tu {producto} llegó a {ciudad} 🎉 La transportadora no
  alcanza a llegar hasta tu dirección, pero puedes recogerlo en su punto/oficina más
  cercana, o coordinamos un punto de encuentro donde sí llegue el mensajero. Cuál te
  queda mejor?"
- **Plataforma:** marcar entrega en oficina/punto o nueva dirección de encuentro.

## 6. Dinero no disponible
**Qué es:** quería recibirlo pero no tenía el efectivo. **Rescate:** ALTA si se reprograma
al día de pago.
- **1er toque:** "Hola {nombre}, tranquilo/a que tu {producto} sigue apartado para ti 💛
  Dime qué día te sirve que pase el mensajero de nuevo y lo dejamos programado para esa
  fecha. Recuerda que son {valor} en efectivo al recibir." *(valor = dato real del pedido)*
- **Plataforma:** reprogramar a la fecha dicha. Si la plataforma/pasarela lo permite,
  mencionar pago anticipado como alternativa.

## 7. Reprogramación pedida por el cliente
**Qué es:** él mismo pidió otra fecha. **Rescate:** ALTA — solo confirmar y cumplir.
- **Toque único:** "Listo {nombre}! Quedó reprogramada la entrega de tu {producto} para
  {fecha}. Te llega entre {franja}. Cualquier cambio me escribes por aquí 🙌"
- **Plataforma:** reprogramar exactamente a esa fecha y anotarla para verificar cumplimiento.

## 8. Otro / novedad rara (guía saqueada, avería, ciudad errada del despacho)
- No hay plantilla mágica: leer el detalle, decidir si se rescata o se corta rápido, y
  documentar el caso. Si es pérdida/avería → reclamar a la transportadora por Dropi
  (indemnización) en vez de perseguir al cliente.

---

## Reglas transversales de los mensajes
1. Primer toque en cuanto se detecta la novedad (la mañana del rescate diario).
2. UNA pregunta por mensaje; fácil de responder desde el celular.
3. Máximo 2 toques + el del mensajero; más es spam y quema el número.
4. Todo dato del mensaje ({valor}, {dirección}, {fecha}) sale del pedido REAL.
5. Si el workspace tiene el asistente logístico de Chatea PRO, estos mensajes pueden
   automatizarse ahí; esta skill genera el contenido correcto por tipo.
