# Changelog · golden-finanzas

## GF1.3 · 2026-09-19
Tercera pasada de golden-verificador: la autoprueba de GF1.2 probaba funciones y no la salida real,
y dejó pasar 16 de 17 sabotajes nuevos. Además había tres fallas vivas:
- **Fracciones con tres decimales** (`0.735`, `0.926`, `1.000`, como las escribe la memoria) se leían
  como miles y se rechazaban con un mensaje falso. Ahora entrega, devolución, ratio y comisión se leen
  siempre como decimales. En los montos, el punto solo vale como separador de miles en grupos de
  tres; `12.34` es ambiguo y se rechaza, igual que un monto de menos de un peso.
- **Un argumento repetido** pisaba al anterior en silencio. Ahora sale `DATO INVÁLIDO`.
- **Costo de menos de un peso** mostraba un múltiplo absurdo. Ahora sale sin múltiplo.
- **Autoprueba de 36 a 48 pruebas:** la salida COMPLETA se compara letra por letra con un caso
  calculado a mano, cada dato obligatorio se prueba faltando por separado, y hay pruebas de regresión
  para cada arreglo declarado (utilidad igual al piso, sin piso, comisión, lectura de números).
  **Banco de sabotajes: 42 de 42 detectados**, con un control neutro que pasa.
- Las cifras del ejemplo coincidían con valores reales del negocio y se decía que eran
  "ilustrativas". Se cambiaron por cifras que sí lo son. Se quitaron del historial un volumen
  operativo y una fecha de aprobación.
- El CPA sale de golden-ads (cuenta en vivo) o de golden-meta-ads-analysis (exportado); antes se
  atribuía solo a la segunda. El ancla psicológica vuelve a ser regla general para toda oferta.

## GF1.2 · 2026-09-19
Cierre de las 15 fallas de la segunda pasada de golden-verificador:
- **Comisión de recaudo solo en entregados** (`--comision`, fracción del precio). GF1.1 mandaba
  sumarla al flete, y así la devolución la pagaba. Fuente: el activo de economía COD de
  golden-productos-ganadores, medido en producción: casi ninguna devolución lleva comisión. Si no se da, la salida
  avisa `[PENDIENTE: comisión]`.
- **Entrada en formato colombiano:** `79.900` se leía como 80 pesos; ahora es 79.900, y `0,62` se
  lee como fracción.
- **Piso validado** (NaN, infinito y negativos salen como `DATO INVÁLIDO`) y veredicto comparado al
  peso, igual a como se muestra: una utilidad de $13.681 con piso de $13.681 ya no dice NO PASA.
- Múltiplo precio ÷ costo **truncado**: 2,995 ya no aparenta 3,00 frente a la regla 3x.
- Mensajes en español con tildes; montos absurdos salen sin traceback.
- **Autoprueba de 17 a 36 pruebas**, incluida la línea de comandos y sus códigos de salida.
  Detectaba 22 de 22 sabotajes del banco de entonces (la tercera pasada mostró que no bastaba: ver GF1.3).
- Quitada la afirmación sin fuente de que golden360 usa esta skill. Nueva frontera con
  golden-productos-ganadores (cazar o validar un producto nuevo y su PVP mínimo).
- Recuperado lo que faltaba del agente: productos digitales y servicios por pasarela (comisión de
  pasarela e impuestos), "se exige el costo cargado completo", sin signos de apertura.

## GF1.1 · 2026-09-19
Cierre de las 20 fallas del golden-verificador sobre GF1.0:
- **Autoprueba de 5 a 17 pruebas.** Detecta 9 de 9 sabotajes; antes dejaba pasar 4, entre ellos
  "rechazar ratio 1", que es el caso real de una transportadora que cobra la devolución completa.
  Cubre cada frontera de la ley (ratio 0 y 1 aceptados, >1 y negativo rechazados, suma = 1 aceptada)
  y el informe (formato, veredicto, sensibilidad).
- **Validación de entradas:** negativos, NaN, infinito y costo 0 ya no revientan ni pasan en
  silencio. Salen como `DATO INVÁLIDO` con código 2, sin traceback.
- **Sin `--piso` no hay veredicto** (antes el piso 0 por defecto regalaba el "PASA").
- La sensibilidad avisa cuando la entrega topa y escribe su supuesto (la devolución queda fija).
- Salida con acentos y decimales con coma.
- **Recuperadas capacidades del agente** que se habían ido con los datos privados: flete incluido
  en el precio, escasez real como palanca, "la memoria es punto de partida, se verifica", decir lo
  aprendido al cerrar, contrato de entregable completo, precio de servicio en el cuerpo.
- Comisión de recaudo declarada como `[PENDIENTE]` y ejemplo de la calculadora marcado ilustrativo.
- **Description con la frontera de disparo** frente a golden-ads, golden-presenta,
  golden-copywriting y golden360.
- Quitado del comentario de versión el nombre propio del dueño (repositorio público).

## GF1.0 · 2026-09-19
- Nace de convertir el **agente** `golden-finanzas` en skill. Principio de
  Anthropic en su blog de agentes de comercio: un agente con skills rinde más que subagentes por
  dominio; cada traspaso a un subagente pierde contexto.
- **Corregida la fórmula del agente:** restaba el "flete ida y vuelta" en las devoluciones. En
  contra entrega se paga UN solo flete; la devolución cuesta el flete de devolución (ratio ≤ 1,
  variable por transportadora y por año).
- Nueva calculadora ejecutable `scripts/margen_cod.py`, con sensibilidad ±20 %, rechazo de datos
  faltantes y autoprueba que incluye controles negativos.
- Sacados del cuerpo los datos del negocio que el agente traía escritos (tiendas, cuentas,
  horarios): caducan y el repositorio es público. Ahora se leen de la memoria del proyecto.
- Propuestas comerciales movidas a `references/` (se cargan solo cuando el entregable es vender).
