# POR QUÉ SE DECIDE POR MUNICIPIO

**Corregido dos veces el 2026-08-10, y las dos por el mismo error de método.**

La primera versión decía que el dato departamental **está inflado**. Falso. La segunda lo
corrigió pero **midió con dos archivos que tampoco eran el mismo barrido**: comparó
`TORRE-MUNICIPIOS` contra `T90-DEPARTAMENTO`. La dirección de la conclusión aguantó; las cifras
publicadas, no. Esta tercera versión mide con el par correcto y publica **esas**.

## La prueba de un minuto que delata dos archivos distintos

**Un departamento de un solo municipio tiene que cuadrar consigo mismo.** Amazonas solo tiene
Leticia:

| Fuente | Interrapidísimo en Leticia | Coordinadora |
| --- | --- | --- |
| `T90-DEPARTAMENTO` (Amazonas) | 3.870 envíos | 164 |
| `EFECTIVIDAD-PLATAFORMA-CIUDAD` (Leticia) | **3.870** | **164** |
| `TORRE-MUNICIPIOS` (Leticia) | 1.961 | 24 |

Los dos primeros son idénticos: **mismo barrido**. El tercero es la mitad: **otro barrido**.
Esta comprobación cuesta un minuto y habría evitado las dos versiones anteriores de este
documento. Hacerla siempre antes de cruzar dos fuentes.

## La medición, con el par homogéneo

`EFECTIVIDAD-PLATAFORMA-CIUDAD` contra `T90-DEPARTAMENTO`, ambos rescatados del panel el
2026-08-03, mínimo 50 envíos en el municipio. Artefacto:
`DROPI-LOGISTICA/datos/MEDICION-MUNICIPIO-VS-DEPARTAMENTO.json`.

| | |
| --- | --- |
| Pares comparables | **965** |
| El municipio entrega **más** que su departamento | **590 (61%)** |
| Diferencia municipio − departamento, mediana | **+1,16 puntos** |
| Rango de esa diferencia | **−72,5 a +20,7 puntos** |

**Límite declarado:** ese archivo de ciudad cubre **20 de 33 departamentos** — se cortó
alfabéticamente en Magdalena. La medición vale para esos veinte.

## La razón verdadera: granularidad, no inflación

El departamento no está inflado; **está ciego**. Su mediana se desvía poco — un punto y pico —
pero su **rango llega a noventa y tres puntos de amplitud**. Un promedio que casi siempre acierta
en la mediana y se equivoca en setenta puntos en la cola es peor que inútil: parece fiable.

| Municipio | Transportadora | Municipio | Departamento | Diferencia |
| --- | --- | --- | --- | --- |
| Boyacá (municipio) | Interrapidísimo | 10,0% | 82,5% | −72,5 |
| Puebloviejo | Envía | 47,0% | 80,2% | −33,2 |
| Ayapel | Envía | 51,0% | 82,3% | −31,3 |
| Mingueo | Interrapidísimo | 91,0% | 70,3% | +20,7 |
| Zipacón | Interrapidísimo | 95,0% | 79,0% | +16,0 |
| Quipile | Interrapidísimo | 94,0% | 79,0% | +15,0 |

Con el promedio departamental, al municipio de Boyacá se le asigna Interrapidísimo creyendo que
entrega 82 cuando entrega **10**. Ese solo caso justifica bajar a municipio.

## El filtro de volumen, que es la otra mitad

Bajar a municipio sin filtrar la muestra cambia un problema por otro peor. La Torre daba Envía
al **100% en Leticia con 4 envíos**, y en vivo esa transportadora ni siquiera cubría; la buena
era Interrapidísimo con **1.961**. Por eso una transportadora solo entra a la comparación si
tiene **≥50 envíos y ≥5% del total del municipio** — `min_envios_muni` y `min_cuota_muni`.

Municipio sin filtro es ruido. Departamento con filtro es promedio. **Municipio con filtro** es
el único de los tres que decide algo.

## La efectividad propia de la tienda

Por municipio **no decide nada**. Con pocos envíos por municipio los intervalos de confianza
pasan de 20 puntos: Medellín con Envía daba 60,5% con un rango real de 50 a 71, y Barranquilla
con Veloces daba 33% con un rango de 0 a 87. Se usa solo agregada, para el factor de tienda.

## El factor de tienda

La tienda entrega por debajo de su municipio, y eso sí es medible en agregado. Corrige el
**nivel**, no el **orden**: se aplica igual a todas las candidatas.

**El número no se escribe en este documento.** Vive en `CALIBRACION-DOLCE.json`, con sus
insumos al lado y — desde el 2026-08-10 — **con su fuente declarada dentro del archivo**.

Esa declaración nació de este mismo error. El factor se había calculado contra
`EFECTIVIDAD-PLATAFORMA`, que predice 95,19%, en vez de contra la Torre municipal, que predice
84,29%. El resultado era **0,746** cuando lo correcto es **0,858**.

**Y aquí vino el segundo error, que es el que enseña.** Se afirmó que el cambio no movía
ninguna decisión, y se probó comparando **conteos agregados**: 27 cambios antes, 27 después.
Idéntico. Pero el conteo no prueba nada — dos conjuntos del mismo tamaño pueden no tener nada
en común. Con el diff **pedido por pedido** apareció que {CLIENTA_A} sí cambiaba de
transportadora, y a una que le había fallado 5 de 8 veces.

El razonamiento también era falso: el factor **no** reescala uniforme. En la fórmula del costo
esperado, el término de la utilidad perdida escala con él y **ensancha** las diferencias, así
que puede sacar un par de la banda de empate y cambiar qué regla decide.

De ahí salieron dos cosas. Una herramienta, `scripts/comparar_decisiones.py`, que compara dos
corridas por id y separa lo que cambia **la acción** de lo que solo cambia **la explicación**.
Y una regla: **"no cambió nada" se prueba con diff por elemento, jamás con el conteo.**

**La regla:** el motor lee el archivo, y si falta, **muere con mensaje**. No cae a 1,0 en
silencio — asumir 1,0 infla la efectividad y mueve pedidos por una diferencia que no existe.

Cada tienda mide el suyo. No se hereda.

## La clase, para no repetirla

**Dos fuentes que miden lo mismo no se cruzan aunque las cifras de cada una sean ciertas.** Las
cifras del documento eran reales y la conclusión era falsa, porque venían de barridos distintos.
El archivo que lo advertía llevaba la advertencia escrita adentro, en `_OJO`, y aun así se cruzó
— dos veces.

**Y un número escrito en prosa envejece.** Este documento llegó a tener tres cifras distintas
para el mismo conteo y una cifra de ahorro que ya no era la de la corrida del día. Los números
que cambian con cada corrida no se escriben aquí: se apunta al script que los produce.
