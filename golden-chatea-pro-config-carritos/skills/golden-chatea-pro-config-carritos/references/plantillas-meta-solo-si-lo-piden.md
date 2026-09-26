# Plantillas de Meta para carritos · SOLO si el dueño lo pide

> **Regla de FER (18-sep-2026): las plantillas NO son configuración.** Vienen al instalar el
> asistente o las diseña el dueño. En una configuración normal **solo se revisa su estado**
> (existen y están APPROVED). Este archivo es para el caso contrario: el dueño pide que le
> redactemos o creemos plantillas nuevas.

## Cuándo se usa

- El dueño pide plantillas nuevas, o
- la auditoría encontró una casilla sin plantilla aprobada y el dueño quiere reponerla.

Crear por API se puede: `POST /whatsapp-template/create`. Meta las revisa como si las mandara el
dueño. **Nada se envía a Meta sin su visto bueno sobre el texto.**

## Por qué todo va por plantilla

El cliente dejó el checkout en la tienda y casi nunca escribió al WhatsApp: es un contacto frío,
sin ventana de 24 h abierta. Por eso **el primer toque exige plantilla**, y en este módulo el
panel no tiene campo de texto libre para los recordatorios: cada paso es un par (tiempo,
plantilla). El panel muestra **dos pares** más el mensaje de recuperación con imagen.

## Ángulos, uno distinto por casilla

| Casilla | Ángulo |
|---|---|
| Mensaje de recuperación (lleva imagen) | Recordatorio suave: retoma el producto y ofrece terminar en segundos |
| Recordatorio 1 | Resolver la objeción: contra entrega, envío gratis, garantía |
| Recordatorio 2 | Último intento, con el incentivo si existe y es viable |

La urgencia o escasez solo entra si es **cierta y confirmada por el dueño**.

## Formato de cada plantilla

- **Nombre:** `minusculas_con_guion_bajo`.
- **Categoría:** Marketing. **Idioma:** español.
- **Cuerpo:** con variables `{{1}}`, `{{2}}` (lo que el módulo pase: producto, valor). Tiene que
  funcionar aunque falte un dato.
- **Botones:** respuesta rápida (p. ej. "Confirmar pedido", "Hablar con soporte").
- **Doctrina:** sin signos de apertura; sin cifras de negocio ni beneficios que el dueño no haya
  confirmado ("envío prioritario", "despacho más rápido", "atención preferencial" solo si son
  reales); beneficio, no reproche; una sola pregunta.

## Después de crear

1. Esperar la aprobación de Meta.
2. En el panel: **Recargar Plantillas** y seleccionar cada una en su casilla.
3. Correr `scripts/auditar_carritos.py` y comprobar el estado APPROVED de las tres.
