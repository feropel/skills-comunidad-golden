---
name: golden-empaque-3d
description: >-
  Golden Group — MESA DE EMPAQUE EN 3D: publica una página donde el empaque se ve en 3D, se
  gira, se DESARMA cara por cara y se despliega como plano de troquel. El visor queda fijo
  arriba y debajo se cambia todo en vivo: colores, tipografías, medidas, textos y acabados,
  con el costo que cada acabado suma. Trae botón que le pide a Claude una revisión del diseño
  dentro de la misma página.
  Úsala SIEMPRE que se quiera VER o DECIDIR cómo queda un empaque antes de mandarlo a imprimir:
  "hazme un mockup", "quiero verlo en 3D", "cómo se vería la caja", "muéstrame cómo queda",
  "quiero mover el diseño", "cambiar los colores y las letras", "armar y desarmar la caja",
  "el plano de troquel", "un simulador del empaque", "qué color le pongo", "necesito ver el
  frasco", "una página donde yo pueda ir cambiando el diseño". Sirve para caja plegadiza,
  frasco, etiqueta, bolsa y display. NO es para foto de producto ya fabricado
  (golden-imagen-arena) ni para páginas de venta (golden-shopify).
---

# Golden Empaque 3D — el empaque se decide viéndolo, no imaginándolo

**Versión:** `GE3D-1.0` · **Fábrica:** chat «✅ SKILL golden-empaque-3d».

Un empaque se aprueba o se rechaza por cómo se ve, y hoy esa decisión se toma mirando un PDF
plano o imaginándose la caja. Esta skill entrega una **mesa de trabajo**: el empaque en 3D
arriba, siempre visible, y debajo todos los controles. El usuario escribe, mueve un deslizador
o elige un color, y lo ve al instante sin perder de vista la pieza.

## Qué trae la mesa

- **Tres vistas**: armada, desarmada cara por cara y **plano de troquel real** —la tira con
  pestaña de pegue, solapas y fondo automático, que es lo que va al impresor—, y gira en las tres
- **Color** de franja, cuerpo y tinta, esta última automática por contraste o forzada a mano,
  más cuatro fondos de estudio
- **Catorce tipografías** de Google Fonts en tres selectores independientes: logotipo, nombre
  de variante y texto secundario, con tamaño, grosor, interletra y orientación
- **Medidas en centímetros**, acercamiento con rueda y deslizador, y botón de centrar
- **Un campo por cada texto visible**, incluida la cara trasera completa
- **Acabados con su precio**: repujado, reserva UV y plastificado, cada uno mostrando cuánto
  suma por unidad, con el margen recalculándose contra el precio de venta
- **Versiones guardadas** en el navegador, ficha copiable y botón de volver al empaque impreso hoy
- **Opinión de Claude** dentro de la página: revisar lo que hay o proponer tres alternativas

## 🔴 Las cinco leyes de esta skill

Estas cinco se incumplen solas si no se vigilan. Cada una está aquí porque su ausencia se paga.

1. **El visor va ARRIBA y FIJO** (`position: sticky`), los controles debajo. Nunca al lado.
   Medido con FER el 22-sep-2026: con el panel al lado, en pantalla angosta hay que bajar a
   escribir y se pierde de vista la pieza, que es justamente lo que se está decidiendo.
2. **Todo lo que se ve se puede cambiar.** Si en la pieza hay un color, un texto, una medida o
   una tipografía y no existe su control, la mesa está incompleta. No se entrega a medias.
3. **Se gira en TODAS las vistas**, también armada, desarmada y en plano. Bloquear la rotación
   en alguna vista es un defecto, no una simplificación.
4. **El costo va pegado a los acabados.** Cuando se marca repujado o reserva UV, la mesa dice
   ahí mismo cuánto sube la unidad y qué margen queda. Un acabado sin su precio es una decisión
   a ciegas.
5. **CSS 3D, nunca Three.js** para piezas de caras planas. Ver `references/motor.md`: el texto
   queda real y nítido, las fuentes cambian sin regenerar texturas y el plano de troquel sale
   solo. Three.js solo entra si la pieza tiene curvatura real (frasco, tubo, doypack).

## Cómo se construye

### Paso 1 — Inventariar la pieza ANTES de escribir nada

No se empieza por el código. Se levanta la ficha, y lo que no se sepa **se pregunta**:

| Dato | Por qué se necesita |
|---|---|
| Tipo de pieza | caja, frasco, etiqueta, bolsa o display: define el motor (`references/motor.md`) |
| Medidas reales en cm | la mesa trabaja a escala, no a ojo |
| Qué dice cada cara | frente, revés, laterales, tapa y fondo: seis textos distintos |
| Colores actuales en hex | el punto de partida es lo que YA está impreso, para comparar |
| Tipografías actuales | si no se sabe, se mira una foto y se elige la más cercana del catálogo |
| Acabados y su costo | repujado, UV, plastificado, estampado: cada uno con su valor por unidad |
| Precio de venta y costo | para que la mesa calcule margen |

**Si hay fotos del empaque, se miran antes de construir.** El punto de partida de la mesa es la
pieza real, no una caja genérica: así el usuario compara contra lo que tiene, que es la única
comparación que le sirve.

### Paso 2 — Partir de la plantilla, no de cero

`assets/mesa-caja-plegadiza.html` es una mesa **completa y funcionando** para caja plegadiza.
Se copia y se adapta.

🔴 **La plantilla es NEUTRA a propósito.** Todos sus textos, variantes y cifras de costo son de
ejemplo, y las cifras están puestas redondas (500, 1.000) para que se note que son falsas.
Decisión del Centro de Mando del 22-sep-2026, con precedente medido: la plantilla de fábrica de
Chatea Pro quedó acoplada a Colombia y hoy limpiarla es el paso 0 obligatorio de cada
instalación. Una plantilla con datos reales se vuelve la base de todo lo que venga después, sus
cifras caducan dentro de una skill blindada que nadie revisa, y quien adapte con prisa publica
sin querer los números de otro cliente.

Lo que hay que tocar está marcado en `references/controles.md`:

1. El contenido de las seis caras
2. Los presets de referencia (variantes del producto)
3. El modelo de costo (`COST`, `CAJA_BASE`, `FIN`)
4. El `BRIEF` que Claude recibe para opinar
5. El título y la marca

🔴 **Estado real de los formatos, hoy.** Hay **una sola plantilla lista: la caja plegadiza.**
Frasco, etiqueta, bolsa doypack y display **se construyen** con la geometría y el criterio de
motor que trae `references/formatos.md`, pero no hay un archivo listo para copiar. La
`description` los nombra a los cinco a propósito, porque la skill sí sabe hacerlos y tiene que
dispararse cuando se pidan; esta línea existe para que nadie busque un asset que no está.
Cuando se construyan las otras cuatro plantillas, esta advertencia sobra.

### Paso 3 — Los controles mínimos, sin excepción

Ninguna mesa se entrega sin estos ocho grupos. `references/controles.md` los detalla:

| Grupo | Qué debe incluir |
|---|---|
| **Referencia** | presets de variantes, nombre, contenido |
| **Medidas** | ancho, fondo, alto en cm y acercamiento |
| **Color** | franja, cuerpo, tinta (automática o manual) y fondo del estudio |
| **Franja** | dónde va (arriba, abajo, ambas, ninguna) y grosor |
| **Tipografía** | fuente del logotipo, de la variante y del texto; tamaño, grosor, interletra, orientación |
| **Textos** | un campo por cada texto visible, incluida la cara trasera |
| **Acabados y costo** | cada acabado con su efecto visual Y su precio, más el margen |
| **Versiones** | guardar, cargar, copiar la ficha y volver al original |

Más el bloque de **Opinión de Claude**, con dos botones: revisar lo que hay y proponer
alternativas.

### Paso 4 — La opinión dentro de la página

La mesa declara `capabilities: {sample: {}}` y usa `await claude.use('sample')`. El `BRIEF`
que se le manda **no es genérico**: lleva el producto, el precio, la categoría contra la que
compite y los riesgos ya detectados. Una opinión sin ese contexto es un horóscopo.

Reglas del `BRIEF`, medidas con FER:
- Español de Colombia, **sin signos de apertura** `¿` `¡`, sin emojis, sin rayas separadoras
- Tope de palabras explícito, o se va por las ramas
- Estructura pedida: qué funciona, qué falla y por qué, **un** cambio concreto
- Si `use('sample')` devuelve `null`, se avisa en la página y se ofrece el chat. Nunca se falla
  en silencio

### Paso 5 — Verificar antes de entregar, con LOS TRES validadores

🔴 **Pasar el validador propio no dice nada de los otros dos.** Medido el 22-sep-2026: la
mesa daba 42 de 42 en el validador de esta skill y el validador oficial rechazaba la skill
por una `description` de 1382 caracteres sobre un tope de 1024. Y la trampa que lo hace
difícil de ver: **la skill cargaba igual**, porque el truncado del harness ocurre más tarde,
cerca de 1536. Funcionaba, disparaba, y aun así no pasaba la compuerta.

```
python3 ~/.claude/skills/golden-empaque-3d/scripts/verificar_mesa.py <archivo.html>
agentskills validate <carpeta de la skill>
~/.golden/bin/golden-barrido-publicacion <carpeta de la skill>
```

| Validador | Qué mide |
|---|---|
| `verificar_mesa.py` | la mesa: 5 leyes, 23 controles, 14 de higiene, más la `description` de la skill |
| `agentskills validate` | la especificación oficial: topes, llaves del frontmatter |
| `golden-barrido-publicacion` | rutas y datos privados antes de publicar |

### Menciones de una marca real: la regla es dónde, no cuántas

Quedan menciones del nombre de cliente que aparece en el docstring de `buscar_marca.py`. Son
deliberadas: son la evidencia de un fallo, no un dato operativo. La lección es sobre **esa
cadena exacta con ese carácter exacto**, y un ejemplo inventado no enseñaría nada.

**La regla que se comprueba es esta, y es la única que importa:**

```
python3 scripts/buscar_marca.py assets "Nombre de la Marca"   ->   TOTAL: 0
```

**Cero en `assets/`**, que es lo que se copia y se adapta. En la documentación, las que hagan
falta para enseñar.

🔴 **Por qué no se fija un número total.** Se intentó y no se pudo: el párrafo que contaba las
menciones era él mismo una mención, así que escribirlo subió la cuenta de 8 a 9, y reescribirlo
la bajó a 8. **Un invariante que cambia cuando lo escribes no es un invariante.** La regla
buena no cuenta ocurrencias en un documento vivo: **acota el sitio donde no puede haber
ninguna**, y ese sitio no se edita al documentarlo.

### 🔴 Lo que cada instrumento NO ve

La pregunta al terminar un validador no es "pasa", sino **qué clase de porquería seguiría
pasando con esto puesto**. Los ángulos ciegos conocidos, para que el siguiente que mire sepa
dónde no ha mirado nadie:

| Instrumento | Da verde sobre | Su ángulo ciego |
|---|---|---|
| `verificar_mesa.py` | estructura y controles del HTML | si la mesa **se ve bien**, si los textos caben, si los colores contrastan |
| `verificar_promesas.py` | que lo prometido exista | si lo que existe **funciona**, y las promesas que nadie escribió |
| `buscar_marca.py` | rastros de una **marca** | datos que caducan en otro formato: **cifras**, teléfonos, URLs, nombres de cliente. Ya mordió una vez |
| `agentskills validate` | forma del frontmatter | si el contenido tiene sentido |
| `golden-barrido-publicacion` | secretos y rutas | ficheros binarios, que no lee |
| Los cinco juntos | el archivo en reposo | **todo lo que solo aparece ejecutando**: acentos rotos, encuadre, una vista que entra girada |

Los tres fallos que costaron más caro el 22-sep-2026 no los vio ninguno de los cinco: los
encontró abrir la página y moverla. **Ningún número de comprobaciones sustituye la fase de
ejecutar.**

Y al adaptar la mesa para un producto, antes de devolver la skill al arsenal:

```
python3 scripts/buscar_marca.py <carpeta de la skill> "Nombre de la Marca"
```

🔴 **Busca la marca CON su acento, escrita exactamente como la escribe su dueño.** Medido el
22-sep-2026: se declaró "cero rastros" buscando `coterra` cuando la marca es **Le'côterra**,
con ô. La cadena sin acento no es subcadena de la cadena con acento, así que el patrón nunca
pudo encontrarla y el cero era real para ese patrón y falso para la pregunta. `buscar_marca.py`
pliega acentos, apóstrofos y espacios para que eso no vuelva a pasar, e **imprime siempre el
universo completo y los ficheros que no pudo leer**, porque un cero sobre un universo que no
se declara no es un cero.

**Reporta cobertura (N de N), nunca veredicto.**

Y después de publicar, se abre la página y se mueve de verdad: girar, desarmar, cambiar un
color, escribir un texto, pedir la opinión. Lo que no se ejecutó no se da por bueno.

## Lo que esta mesa resuelve y que un PDF no

- **Se compara contra lo impreso.** El botón "Volver al original" devuelve la caja que existe
  hoy, así que cada cambio se mide contra algo real.
- **El plano de troquel sale de la misma pieza**, sin volver a dibujar: es lo que va al impresor.
- **El costo se mueve con el diseño.** Quitar la reserva UV baja $200 por unidad y se ve ahí.
- **Las versiones se guardan** en el navegador y se comparan de una en una.

## Errores que ya se cometieron

| Error | Qué pasa | Cómo se evita |
|---|---|---|
| Panel de controles al lado del visor | En móvil hay que bajar a escribir y se pierde la pieza | Visor `sticky` arriba |
| Texto vertical con `transform: rotate(90deg)` | El bloque se sale de la cara y hay que parchar posiciones | `writing-mode: vertical-rl` |
| Bloquear la rotación en la vista de plano | El usuario quiere inclinar el troquel para verlo | Rotación libre en las tres vistas |
| Escala fija en píxeles | La pieza se sale del visor al cambiar las medidas | Escala calculada contra la altura del visor |
| Acabados sin precio | Se elige el más bonito sin saber que cuesta $316 por unidad | Costo pegado al interruptor |
| `localStorage` sin `try/catch` | La página revienta en ventana privada | Todo lectura y escritura envuelta |
| **Sin `<meta charset="utf-8">`** | Dentro del artifact no se nota porque el anfitrión lo inyecta. Fuera —abierta local, subida a un hosting, mandada al impresor— los acentos salen mojibake: `Le'cÃ´terra`, `TIPOGRAFÃA` | La plantilla lo lleva en la primera línea. Cuesta 30 bytes |
| Hueco de la vista desarmada sin contar en la escala | Las caras se salen del visor | `need = H + 2*GAP + D`, no una estimación |
| Plano de troquel que entra girado | Un troquel se mira de frente | Al entrar a plano: `rx=0, ry=0` y giro automático apagado |
| **Desplegar la caja en cruz y llamarlo troquel** | La cruz es didáctica; el impresor necesita la tira con pestaña de pegue y fondo automático. Un plano que no se puede imprimir no es un plano | Ver `motor.md`: tira de cuatro paneles, solapas y `clip-path` de crash-lock |

## Referencias

- `references/motor.md` — CSS 3D contra Three.js, y cómo se construye el sólido
- `references/controles.md` — los ocho grupos, qué tocar de la plantilla
- `references/formatos.md` — geometría de frasco, etiqueta, bolsa y display
- `references/tipografias.md` — las catorce fuentes del catálogo y para qué sirve cada una
- `assets/mesa-caja-plegadiza.html` — mesa completa, funcionando, lista para adaptar
- `scripts/verificar_mesa.py` — el validador de la mesa y de la propia skill
- `scripts/buscar_marca.py` — busca rastros de una marca sin que el acento la esconda
- `scripts/verificar_promesas.py` — comprueba que cada promesa de la `description` exista en el HTML

## Frontera con otras skills

- Foto de producto **ya fabricado** → `golden-imagen-arena`
- Página de venta del producto → `golden-shopify` o `golden-web`
- Presentación del empaque a un cliente → `golden-presenta`
- Costeo del empaque, sin diseño → el expediente de costos del proyecto
