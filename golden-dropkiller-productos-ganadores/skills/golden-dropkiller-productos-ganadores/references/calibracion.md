# Calibración de los umbrales de caza

Los umbrales del método de Juan Vargas son "deducidos", no medidos. Este archivo dice qué se
MIDIÓ contra historia real, con qué fuerza, y cómo repetirlo. Un umbral que no aparece aquí como
medido es heredado y se declara así.

## Vigente: backtest v2 del 2026-09-18 (Colombia, Dropi)

**Diseño.** Productos de DropKiller creados entre el 1-mar y el 20-jun de 2026 con 100 o más
ventas (población 4.065). La muestra NO depende de lo que pasó después: el rango de creación se
partió en 12 ventanas de ~9 días y de cada una se tomaron 12 productos por orden de creación
(144 en total, 0 duplicados, ponderados por el tamaño de su ventana). Se leyeron los 144
historiales (0 errores). **Corte T = 2026-07-19**; 112 estaban entre 100 y 3.000 ventas en T.
Resultado a 60 días con ventas DEPURADAS (`ventas_reales.py`): GANÓ ≥ 600, MURIÓ < 60, MEDIO el
resto. Salieron 3 ganadores, 25 medios y 84 muertos.

**Por ventas de 7 días en T:**

| 7 días | N | Ganó | Medio | Murió | % murió | Mediana vendida en 60 días |
|---|---|---|---|---|---|---|
| 0 a 9 | 85 | 1 | 6 | 78 | 92% | 0 |
| 10 a 30 | 12 | 1 | 6 | 5 | 42% | 62 |
| 31 a 60 | 4 | 0 | 3 | 1 | sin muestra suficiente | 90 |
| 61 a 120 | 6 | 0 | 6 | 0 | 0% | 296 |
| más de 120 | 5 | 1 | 4 | 0 | 0% | 490 |

**Lo que se sostiene (con su fuerza):**
- **Piso firme de 10 ventas en 7 días.** Bajo 10 murió el 92% (78 de 85); de 10 para arriba, el
  22% (6 de 27). Fisher p < 0,001. Es la única regla de ritmo medida con fuerza.
- **31 o más: indicio, no prueba.** De 31 para arriba murió 1 de 15; entre 10 y 30, 5 de 12
  (p = 0,06, N chico). Por eso 31 es el valor PRUDENTE por defecto del menú y no una ley.
- **El nivel predice mejor que la aceleración:** correlación con lo vendido después 0,74 (N 112)
  contra 0,58 (N 67); en los mismos 67 productos el nivel da 0,75. En el ranking va el nivel.
- **Cuánto dura:** en los 60 días siguientes el producto MEDIANO vende unas 3 semanas de su ritmo
  en T. Es una mediana, no una regla: de los 3 que ganaron, uno tenía 0 ventas en 7 días en T.
- **Qué se midió exactamente:** la etapa y el ritmo de UNA ficha de proveedor, no del mercado
  consolidado de `consolidar_mercado.py` (el backtest no sumó proveedores ni colapsó espejos).
  La skill aplica los umbrales al mercado consolidado: se asume que se trasladan, no se midió.

**Lo que NO se sostiene o no se pudo medir:**
- **"Más de 120 = descarte" (el techo heredado): sin evidencia.** Tampoco hay evidencia para
  preferirlos: más de 120 ganó 1 de 5, de 10 a 120 ganó 1 de 22 (p = 0,34). Queda el aviso
  CALIENTE (medir competencia sí o sí), sin premio ni castigo en el ranking.
- **"Frenando" como alarma: no se distingue del nivel bajo.** Murió el 78%, pero 35 de sus 40
  productos vendían menos de 10. Con 31 o más solo hubo 1 caso. Queda como AVISO, no filtro.
- **Reabastecer 2 o más veces:** N = 2. Sin evidencia: dato de la tarjeta, no del ranking.
- **Tope de proveedores (5 en CO):** SIN VERIFICAR; DropKiller no da proveedores por fecha.
- **Etapas por ventas totales (CO, EC, GT):** tabla de practicante, no medida.
- **Mercados distintos de Colombia:** nada medido; se usan los de CO y se declara.

**Sesgos que quedan:** solo productos que DropKiller sigue listando; el total en T se reconstruye
(DropKiller a veces repite un día); dentro de cada ventana se toman los primeros 12 por fecha de
creación (no puramente aleatorio) y 402 productos en los bordes de las ventanas no entraron;
DropKiller salta días y los días sin lectura cuentan 0; 3 ganadores es poco para comparar
"ganó"; una sola fecha de corte, una temporada, un país. Y un defecto de la señal: el ritmo de 7
días se mide desde el último día CON dato; en 17 de 112 ese día era anterior al 13-jul. Sin esos
17 (N 95) ninguna conclusión cambia. En la caza en vivo, `correr_lote.py` marca el historial
viejo.

**Cómo repetirlo:** `PROYECTOS/CAZA-DIARIA-GANADORES/_backtest-2026-09-18-v2/` tiene la muestra,
los 144 historiales, `backtest_v2.py` (importa la skill INSTALADA; su autoprueba corre 19 casos)
y `resultado.md`. Reproducido por la fábrica desde esa carpeta. **Recalibrar cada trimestre**, con
otra fecha de corte y el mismo diseño, o antes si `seguimiento.py` dice que LISTA no gana más que
CASI.

## Superado: backtest v1 del 2026-09-18 (se guarda como lección)

El v1 (`_backtest-2026-09-18/`) armó la muestra en tres grupos por las ventas de los ÚLTIMOS 30
días, una ventana que caía DENTRO del periodo de resultado: estratificó por el resultado. Un
grupo casi no podía morir y otro casi no podía ganar. De ahí salieron dos conclusiones falsas
que llegaron a la GPG1.17: "más de 120: 10 de 11 ganaron" (en el v2, 1 de 5) y "31 a 120 gana
~25%" (en el v2, 0 de 10). Lo encontró el verificador adversarial, no la fábrica. La lección:
**una muestra para medir un resultado no se elige mirando ese resultado.**
