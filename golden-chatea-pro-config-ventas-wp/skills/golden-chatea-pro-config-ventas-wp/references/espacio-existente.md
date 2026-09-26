# Espacio que ya existe: cómo se audita y se corrige

Para un espacio que llega ya configurado (contrato de optimización, o el propio de la casa). Es
distinto de instalar: aquí no se parte de cero, se compara contra lo que la skill produciría para el
**país y el modelo de ese espacio** y se corrige solo lo que está roto.

## 1. Auditar (solo lectura)
`python3 scripts/auditar_espacio.py --token-file <ruta> --guardar-volcado <archivo>`. El volcado queda
como respaldo del estado anterior (chmod 600, **fuera de la carpeta de la skill**, que es pública).
País y modelo se leen del propio espacio (`conexion_con_dropi.pais` y `Solo Con Recaudo`).

## 2. La rúbrica (1000 puntos, cada resta se imprime con su motivo)
| Categoría | Pesa | Qué mide |
|---|---|---|
| estructura | 150 | los 2 campos existen, JSON válido, las 24 llaves de la plantilla |
| prompts | 300 | topes UTF-16, huecos `{{}}` y `(Producto N)`, sin ¿¡, vocabulario del país, identidad |
| operativa | 150 | moneda del país, flete y validaciones válidos, notificación con número, división 2 |
| interruptores | 100 | 18 campos (13 booleanos + 2 `[WhatsApp IA]` por valor, 3 textos por existencia); solo 3 (Oficina, Con/Sin Recaudo) varían por país y modelo, el resto es fijo |
| productos | 300 | cada producto pasa `valida_producto.py`, D1 byte a byte, Disparador sin huérfanos ni duplicados |

**DECISIÓN no es defecto.** Un interruptor distinto del estándar, o un producto activo sin entrada en
el Disparador, puede ser una elección legítima del negocio. Se resta poco y se reporta con la propuesta
ya validada; **la resuelve Golden (FER) con su criterio y no se escribe por cuenta propia**. En un
espacio de cliente **no se le consulta al cliente** (estándar del 2026-09-19): lo único que se le
pregunta es el corte de flete. El 1000 con decisiones abiertas lo cierra esa resolución, no una suposición.

## 3. Corregir
Respaldo (`push_config.py backup`) → escribir → **releer del servidor y comparar el JSON PARSEADO**
(la API recorta el `\n` final y da un falso "TRUNCADA" si se compara el texto) → auditar de nuevo.

## 4. Trampas de la API medidas en vivo
- **El filtro `name` casa por coincidencia PARCIAL.** Pedir `[Ventas Wp] Configuracion general`
  devuelve también `... general 2`, y el primero de la lista es el equivocado. Emparejar SIEMPRE por
  nombre exacto (`push_config.py` ya avisa en `read` y `backup`).
- **Python necesita User-Agent.** Sin él, Cloudflare devuelve 403; `curl` pasa.
- **Un espacio "en blanco" en el panel puede estar intacto en el servidor.** Leer por API antes de
  restaurar. Causas vistas: workspace equivocado (un espacio nuevo se ve exactamente así), caché del
  navegador, selector de bot cambiado, JSON inválido en uno de los dos campos.
- **Los campos `[WhatsApp IA]` de estado los escribe el bot mientras opera** (contadores del día):
  escribir sobre ellos destruye datos de venta reales. Están listados como NO_TOCAR.
