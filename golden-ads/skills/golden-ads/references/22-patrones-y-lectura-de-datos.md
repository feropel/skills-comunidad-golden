# Leer PATRONES (no números sueltos) — el método analítico

Un número solo no dice nada: `CPA 38.000` no es bueno ni malo. Lo que decide es el **patrón**: contra
qué se compara, hacia dónde va, si se repite y si es real o azar. Este archivo es el "cómo se piensa"
que va antes de cualquier veredicto de `02` y de cualquier revisión de `20`.

## 1. Los 4 marcos de comparación (un número siempre se lee contra algo)
| Marco | Pregunta | Cuidado |
|---|---|---|
| **Contra sí mismo (tiempo)** | mejor o peor que la semana pasada | ojo con ciclos y estacionalidad (§3) |
| **Contra su hermano** | mejor o peor que el otro conjunto/creativo | solo si ambos tuvieron presupuesto real (`16` §C) |
| **Contra el objetivo** | por debajo o encima del breakeven (`12`) | es el ÚNICO marco absoluto: gana o pierde |
| **Contra el mercado** | vs benchmark de industria (`07`, `ads_insights_industry_benchmark`) | orienta, no dictamina |
> Sin marco de comparación no hay análisis, hay lectura de números en voz alta.

## 2. Tendencia vs ruido (lo que más plata cuesta confundir)
Todo dato diario oscila. Antes de reaccionar a un movimiento:
- **Mira 3+ puntos, no 2.** Dos días no hacen tendencia. Una tendencia es la MISMA dirección sostenida.
- **Usa promedio móvil de 3–7 días**, no el día suelto. En COD el día suelto es casi siempre ruido.
- **Magnitud vs volumen**: con poco volumen, un CPA salta solo porque entró o no entró una venta.
  Una compra más o menos con 8 ventas mueve el CPA ~12%: eso es aritmética, no rendimiento.
- **Regla de las 72 horas** (ya vigente en la skill): una alerta debe **sostenerse 3 días** antes de
  convertirse en veredicto. Antes de eso solo justifica vigilar.
- **Ventanas asimétricas en COD**: ayer y 7 días SIEMPRE subestiman (la compra se confirma tarde y
  Meta la atribuye hacia atrás) → el veredicto se da con **mes corrido + lifetime**.

## 3. Ciclos: separar el patrón del calendario del patrón real
Antes de declarar "está empeorando", descarta que sea el calendario:
- **Ciclo semanal**: fines de semana y lunes se comportan distinto por vertical. Compara **semana
  completa contra semana completa**, nunca lunes contra sábado.
- **Ciclo de quincena** (clave en LatAm COD): los días de pago mueven la conversión. Un CPA malo el
  día 20 puede ser normal.
- **Estacionalidad** (`21` §4): la temporada cambia el problema, la demanda y el CPM de la subasta.
- **Ciclo de vida del creativo**: todo creativo decae. Un CPA que sube con frecuencia subiendo y CTR
  bajando NO es "la campaña se dañó", es **fatiga** → se refresca creativo (`08`), no se pausa la campaña.

## 4. Correlación no es causa (el error de análisis más común)
"Subí el presupuesto y bajó el ROAS" → puede ser el presupuesto… o el reinicio de aprendizaje que
provocó el cambio, o que entró temporada alta y subió el CPM, o que se quemó el creativo.
**Método para no equivocarse:**
1. Escribe **3 hipótesis** de por qué pasó, no una.
2. Busca cuál explica **también** el resto de los números (si es fatiga, la frecuencia subió y el
   hook bajó; si es la landing, la caída está entre clic y LPV; si es subasta, subió el CPM de todos).
3. Revisa **qué cambió y cuándo** (`ads_account_get_activity_logs`) antes de culpar al algoritmo.
4. La que explique más señales gana. Si dos empatan, **se prueba**, no se adivina (test A/B `05`).

## 5. Patrones que SIEMPRE se buscan (checklist de lectura)
- **Concentración**: el 80% del gasto está en el 20% que gana, o al revés. Si un perdedor se come el
  presupuesto, ese es el hallazgo #1.
- **Divergencia embudo**: métrica alta arriba y baja abajo (CTR alto, compras bajas = clickbait o
  landing mala; muchos chats, pocas ventas = cierre/bot).
- **Duplicados y solapamiento**: mismo nombre repetido, o conjuntos peleando la misma subasta (`11`).
- **Cero absoluto**: gasto con CERO señal en un escalón (0 LPV, 0 carritos, ROAS "Not available") =
  bandera técnica, casi siempre pixel/CAPI o destino roto — no es "no funciona la campaña".
- **Outlier de un día**: un pico que no se repite = investigar antes de extrapolar (a veces es una
  venta grande, a veces un error de registro).
- **Cohorte**: comparar por fecha de INICIO (los conjuntos nuevos siempre se ven peor: están aprendiendo).

## 6. Salida obligatoria de todo análisis de patrón
1. **El patrón en una frase**: "el CPA subió 40% en 5 días sostenidos, con frecuencia de 1,8 a 3,2".
2. **La causa más probable** (de las 3 hipótesis) y qué señales la respaldan.
3. **La acción** concreta (REGLA 6) — una, la que más mueve la aguja.
4. **El nivel de confianza** del dato (REGLA 12) y qué haría falta para confirmarlo.
