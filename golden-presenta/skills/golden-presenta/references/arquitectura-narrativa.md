# Arquitectura narrativa — el esquema antes del diseño

Empieza SIEMPRE aquí. El motor mueve la cámara; esta referencia decide qué se mueve.

## Índice
1. La regla del esquema
2. Frameworks por tipo de encargo
3. Los 11 tipos de lámina: 8 de texto y 3 visuales
4. Densidad: cuánto texto cabe de verdad
5. Errores de estructura que se repiten

## 1 · La regla del esquema

Antes de escribir HTML se entrega al usuario una lista así, y se ajusta ahí:

```
01 · portada      Nombre del proyecto y para quién es
02 · frase        El problema en una sola oración
03 · dato         La cifra que lo prueba
04 · tarjetas     Las 3 piezas de la propuesta
05 · comparación  Antes contra después
06 · proceso      Los 4 pasos de implementación
07 · dato         Lo que cuesta no hacerlo
08 · cita         Un cliente real diciéndolo
09 · cierre       El único paso siguiente
```

Cambiar una lámina aquí cuesta una línea. Cambiarla después de maquetada cuesta media hora.

**Una idea por lámina.** Si al escribir la frase de una lámina necesitas la palabra "y"
dos veces, son dos láminas.

## 2 · Frameworks por tipo de encargo

### Propuesta comercial a un cliente (8 a 12 láminas)
El framework es **PAS con prueba**, y el orden importa porque el cliente decide en la 3.

```
portada · frase(dolor) · dato(tamaño del dolor) · frase(agitación)
tarjetas(la solución en 3) · proceso(cómo se implementa) · comparación(con y sin)
cita(prueba social) · dato(inversión y retorno) · cierre(un solo paso)
```

Lo que más se falla: poner "quiénes somos" en la lámina 2. A nadie le importa quién eres
hasta que demuestras que entendiste su problema. La credencial va después de la prueba,
nunca antes.

### Clase o módulo formativo (12 a 20 láminas)
```
portada · frase(qué vas a saber hacer al terminar) · proceso(el mapa del módulo)
[por cada concepto: frase(la idea) + tarjetas(los componentes) + comparación(bien/mal)]
dato(el error más común, con su costo) · cierre(la tarea concreta)
```

Regla del MBA: cada concepto cierra con un **ejemplo real de una tienda de verdad**, nunca
con un ejemplo inventado. Si no hay ejemplo real, el concepto no está listo para enseñarse.

### Charla o keynote (10 a 16 láminas)
Aquí el deck acompaña, no explica. Más frases sueltas, menos tarjetas.
```
frase(la afirmación incómoda) · dato(que la sostiene) · frase(la vuelta de tuerca)
cita · tarjetas(solo una vez, para lo accionable) · cierre
```
En una charla, una lámina de puro texto grande vale más que tres de viñetas.

### Reporte de resultados (8 a 14 láminas)
```
portada · dato(el titular del período) · comparación(objetivo contra real)
tarjetas(los 3 aprendizajes) · proceso(qué se hace el mes que viene) · cierre(la decisión que se pide)
```
Un reporte que no termina pidiendo una decisión es un informe, no una presentación.

## 3 · Los 11 tipos de lámina

| Tipo | Clase CSS | Para qué sirve | Cuándo NO usarlo |
|---|---|---|---|
| Portada | `t-portada` | Abrir. Nombra a la audiencia, no a ti | Nunca falta |
| Frase | `t-frase` | Una idea sola, con silencio alrededor | Si tienes que explicarla, no es una frase |
| Dato | `t-dato` | Un número que decide algo | Si el número no cambia una decisión, sobra |
| Tarjetas | `t-tarjetas` | Listas visuales de 2 a 4 piezas | Con 5 o más: parte en dos láminas |
| Comparación | `t-comparacion` | Antes/después, con/sin, nosotros/ellos | Si un lado tiene 1 punto y el otro 6, es propaganda, no comparación |
| Proceso | `t-proceso` | 3 a 5 pasos en secuencia | Si los pasos no son secuenciales, son tarjetas |
| Cita | `t-cita` | Prueba social verificable | **Jamás una cita inventada.** Sin fuente real, se borra la lámina |
| Cierre | `t-cierre` | Un solo paso siguiente | Si ofreces dos opciones, no ofreciste ninguna |

### Los 3 tipos VISUALES

Añadidos el 2026-09-03 tras un fallo medido: un deck de 18 láminas salió con **cero `<img>`
y cero `<svg>`**, y el veredicto fue "puro texto, muy plana". La causa raíz no era el autor:
**los 8 tipos de arriba son todos de texto**, así que se construyó exactamente lo que había.
Un deck de marca sin una sola imagen se lee como un documento proyectado.

| Tipo | Clase CSS | Para qué sirve | Cuándo NO usarlo |
|---|---|---|---|
| Visual | `t-visual` | Imagen o diagrama al lado del texto. **El caballo de batalla** | Si la imagen no aporta, es relleno |
| Galería | `t-galeria` | Rejilla de logos, capturas o resultados (`.g2` `.g3` `.g4`) | Con menos de 4 piezas: usa `t-visual` |
| Pantalla | `t-pantalla` | Una captura grande con marco de ventana | Si hay que señalar 5 cosas en ella: pártela |

`t-visual` acepta `img-izq` para invertir el lado: `class="slide t-visual img-izq"`.
Alternar el lado entre láminas evita el ritmo de plantilla.

**Regla de proporción:** en un deck de marca, **al menos 1 de cada 4 láminas lleva algo que
no sea texto.** Logo, captura, diagrama o gráfico. Si el deck entero es tipografía, o es una
charla de keynote muy deliberada, o está plano.

**Todo recurso va incrustado como data URI**, nunca como ruta:
`scripts/incrustar_recurso.py imagen /ruta/logo.png`. El deck es un archivo y tiene que
abrir sin red.

### Criterios que no se negocian

**El dato manda sobre su explicación.** En `t-dato` el número va primero y grande; el
contexto debajo y en gris. Al revés, nadie recuerda la cifra.

**En la comparación, el lado bueno va a la derecha.** El ojo termina el recorrido ahí y esa
es la última impresión. El motor ya lo trae: `.lado.bueno` lleva el acento de marca.

**Las tarjetas son 3.** Con 2 se ve pobre, con 4 se acepta, con 5 nadie recuerda ninguna.

**La cita lleva nombre y contexto real.** "Un cliente satisfecho" no es prueba social, es
relleno. Si no puedes nombrar la fuente, la lámina no va.

## 4 · Densidad: cuánto texto cabe de verdad

Medido sobre la lámina de 1280x720 con el padding de 84 px del motor:

| Elemento | Límite real | Qué pasa si te pasas |
|---|---|---|
| Título de portada | 28 caracteres | Se parte en 3 líneas y pierde el golpe |
| Frase (`t-frase`) | 90 caracteres | Baja de 64 px y deja de leerse de pie |
| Contexto de dato | 140 caracteres | Compite con la cifra |
| Descripción de tarjeta | 110 caracteres | La tarjeta crece y rompe la retícula |
| Paso de proceso | 90 caracteres | Los pasos dejan de leerse en paralelo |
| **Lámina completa** | **550 caracteres** | El verificador lo marca como FALLA y bloquea la entrega |

Regla de sala: **si el texto no se lee a 3 metros, no está en una presentación, está en un
documento.** Cuando el contenido no cabe, la salida no es encoger la letra: es partir la
lámina o mover el detalle a un anexo.

## 5 · Errores de estructura que se repiten

1. **Agenda en la lámina 2.** Nadie decidió nada por ver una agenda. Se borra y se empieza
   por el problema del cliente.
2. **"Quiénes somos" antes de la prueba.** La credencial solo pesa después de demostrar que
   entendiste el problema.
3. **Viñetas.** Si aparece una lista de puntos, es que faltó decidir la jerarquía. Se
   convierte en `t-tarjetas` o se parte en varias láminas.
4. **Dos llamadas a la acción.** "Contáctanos o agenda una demo" reparte la intención y no
   pasa ninguna de las dos. Un solo paso.
5. **Cifras sin fuente.** Un dato sin origen verificable en un deck de cliente es un riesgo
   comercial, no un adorno. Se cita o se quita.
6. **El deck que se lee en voz alta.** Si el presentador lee las láminas, las láminas
   sobran. El texto de la lámina es el titular; el desarrollo va en `data-notas`.

## Encadena con
- `golden-copywriting` para el texto de las láminas de venta
- `golden-finanzas` (**agente**, vive en `~/.claude/agents/`) si el deck lleva precios, márgenes o una propuesta económica
- `golden-investigacion-mercado` si hace falta la voz real del cliente para las citas
