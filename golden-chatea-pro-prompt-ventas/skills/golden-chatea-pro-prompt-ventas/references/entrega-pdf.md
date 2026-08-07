# Entregable PDF (PASO 2.5) · con golden-pdf-check

Además del paquete copy-paste en el chat, genera un **PDF profesional** del paquete completo usando la skill `golden-pdf-check` (estándar Golden, bloques atómicos anti-corte, compuerta verbatim). Hazlo por defecto cuando el usuario quiera un documento para guardar/compartir/configurar, y SIEMPRE que lo pida.

## Qué lleva el PDF (orden sugerido)
1. **Portada** (front matter): kicker "Comunidad Golden · Chatea PRO", título del producto, subtítulo (marca · país · modelo de pago), autor, fecha.
2. **Mapa de configuración** (tabla): qué pieza va en qué sección de Chatea PRO (ver `guia-configuracion-chatea.md`).
3. **Saludo inicial** — tarjeta copiable.
4. **Plan de multimedia inicial** — lista (no es copiable; son instrucciones).
5. **Pregunta de entrada** — tarjeta copiable.
6. **Prompt de venta** — en tarjetas "Parte 1 de N…" (ver regla de partición abajo).
7. **Recordatorios 1 y 2** — cada uno su tarjeta.
8. **Remarketing 1 y 2** — datos de la plantilla Meta + tarjeta del cuerpo {{1}} + tarjeta de la instrucción especial (Campo 3).
9. **Activador** (palabra clave) — tarjeta.
10. **Manifiesto de imágenes** — tabla (qué imagen, dónde va, cómo obtenerla) + **una tarjeta por cada prompt de imagen** (ver `recursos-visuales.md`).
11. **Estado y pendientes** — qué falta por completar (URLs, prueba social si quedó como marcador, etc.).

## Regla de partición del prompt (CRÍTICA)
El prompt de venta suele pasar de 9.000 caracteres y **no cabe legible en una sola página**. Por eso:
- Pártelo en tarjetas tituladas **"Prompt de venta — Parte 1 de N", "Parte 2 de N"…**, cortando en límites naturales de sección (entre bloques, nunca a media frase).
- Avisa en el texto (fuera de las tarjetas) que **las partes van SEGUIDAS, en orden, dentro del MISMO campo** (Prompt del producto → Prompt personalizado). No son prompts distintos: es UN prompt repartido para que quepa legible.
- **El texto no cambia ni un carácter** entre el prompt original y las tarjetas (la compuerta verbatim de golden-pdf-check lo verifica).
- Si el build reporta `fit_warnings` con tipo < ~8pt en alguna parte, **parte esa tarjeta en dos** (más partes, cada una legible). En la práctica un prompt de ~11.500 caracteres queda bien en 4 partes.

## Cómo construirlo (mecánica) — delegando en golden-pdf-check
Esta skill NO trae motor de PDF propio: **invoca la skill `golden-pdf-check`**, que aporta su formato Markdown-Golden, su `build_pdf.py`, su `audit_pdf.py` y la compuerta verbatim. Tú solo preparas el contenido y le pasas el archivo. Ninguna de esas rutas de script vive en esta skill.
1. Arma un archivo Markdown-Golden con el front matter + las secciones anteriores; cada pieza copiable dentro de ` ``` Título ... ``` ` (el formato exacto lo define la propia skill golden-pdf-check en su archivo de formato de contenido; si no lo recuerdas, ábrela y léelo). Ese archivo NO vive en esta skill.
2. Invoca `golden-pdf-check` en modo construir, pasándole el archivo de contenido y la ruta de salida (`PROYECTOS/<PRODUCTO o MARCA>/…​.pdf`). Ella corre su `build_pdf.py` y devuelve el JSON: confirma `verbatim.ok=true` y `fit_warnings=[]` (si hay warnings de tipo < ~8pt, parte esa tarjeta y reconstruye).
3. Deja que `golden-pdf-check` corra su `audit_pdf.py`: entrega el PDF solo si el veredicto es **APROBADO** (sin bloques cortados) y la compuerta verbatim pasó.
4. Guarda el PDF en la carpeta del proyecto y entrégaselo al usuario.
Fallback si golden-pdf-check no está disponible: entrega el paquete solo como copy-paste en el chat e infórmale al usuario que el PDF requiere esa skill.

## Notas
- Los emojis del prompt renderizan a color y se copian bien (la compuerta verbatim preserva el texto exacto).
- Marca del PDF = Golden (portada/pie), pero **el contenido del prompt no lleva rastros de Golden**: dice la marca del cliente. Son cosas distintas (el envoltorio del documento vs. el texto que se pega en Chatea).
