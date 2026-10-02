---
name: golden-anuncios-niveles-de-conciencia
description: >-
  Golden Group — ANUNCIOS POR NIVELES DE CONCIENCIA (sistema Despliegue Creativo de Kevin). De
  un producto con su estudio de mercado saca los ángulos de venta, los ordena por nivel de
  consciencia de Schwartz, baja el nivel para llegar a público frío y arma la matriz de anuncios
  ESTÁTICOS ángulo por TOFU, MOFU y BOFU: una ficha por pieza con formato, por qué, texto literal,
  jerarquía, arte y el prompt de imagen listo para el motor. Úsala cuando digan: módulo 3,
  despliegue creativo, estáticos por nivel de conciencia, imágenes TOFU MOFU BOFU, validar un
  producto nuevo con estáticos, bajar el nivel de conciencia, un prompt por ángulo y etapa, qué
  estático hago para público frío. También ordena el paso siguiente: del estático ganador a
  guion, UGC y video IA. No investiga (lo pide a investigación de mercado), no genera la imagen,
  no escribe los textos largos de Meta y no monta campañas.
metadata:
  owner: "Golden Group"
---

**Fábrica:** chat «✅ SKILL golden-anuncios-niveles-de-conciencia»

# golden-anuncios-niveles-de-conciencia

<!-- skill v1.2 · 2026-10-02 · ronda contra golden-verificador (885/1000): validador reescrito (25 casillas, vocabularios cerrados, texto normalizado, todos los campos y el prompt, exit 2 ante forma inválida, autoprueba de 61 casos con dos sanas de vertical y país distintos); contradicción rostros/persona resuelta; estudio anterior a la Fase 3.5 cubierto; corrida real con el filtro de grifo. Detalle en references/changelog.md -->
<!-- skill v1.1 · 2026-10-02 · primera auditoría con golden-skill-auditor: fuera la carpeta .claude vacía que dejó el sandbox, evals a references/, relación 4:5 por defecto y 1:1 como pieza aparte (había contradicción entre SKILL y formatos), el 40% de "bajar el nivel" declarado como punto de partida sin medición, casilla 06 también con nombre_corto (antes solo veía el nombre completo). Detalle en references/changelog.md -->
<!-- skill v1.0 · 2026-10-02 · nace con aval de FER desde el chat «✅ SKILL golden-anuncios-niveles-de-conciencia». Método de Kevin Galeano (taller MBA 01-oct) + M13 de Alejo (30-sep) + 49 leyes de la casa. Decisión de FER: exige estudio de mercado mientras llega el archivo original de Kevin. Historial en references/changelog.md -->

Convierte un producto **con estudio de mercado** en una tanda de anuncios estáticos repartidos por
nivel de consciencia, lista para generar y para probar barato antes de gastar en video. Es el
sistema "Despliegue Creativo" de Kevin Galeano con las leyes de Golden. El nombre usa "conciencia"
porque así lo dicen FER y el mercado; el texto escribe "consciencia", que es la palabra exacta (ver
`references/niveles-de-consciencia.md`).

**Esta skill es el director creativo, no el fotógrafo.** Decide qué imagen hacer y por qué: ángulo,
nivel, etapa, texto exacto, plan de prueba. No genera ni un píxel: le entrega los prompts a
`golden-imagen-arena` o `golden-ecom-magic`, que deciden cómo hacerla. Se separaron a propósito: la
arena también hace fotos de ficha, galerías e infografías que no tienen embudo, y cambia cuando sale
un motor nuevo; esta cambia cuando cambia cómo se vende.

**Centro de Mando.** Quien ejecute esta skill reporta al Centro de Mando (la sesión cuyo título
contiene "CENTRO DE MANDO") cada corrida cerrada y cada cambio a la skill, con `golden-bandeja
<ruta-del-parte.md>`. Llamarla una sola vez por parte: escribe al llamarla.

## Por qué existe

Kevin lo dijo mirando 9 anuncios de un alumno rotulados TOFU, MOFU y BOFU: *"todo enfocado
directamente al BOFU… no veo un nivel de educación del cliente"* (taller 01-oct, 01:56:45). El
mercado entero le habla a quien ya quiere comprar y nadie educa al que todavía no sabe que tiene el
problema. Y desde Andromeda, Meta agrupa los anuncios parecidos y los hace competir como uno solo:
cinco versiones del mismo mensaje son una sola apuesta. Repartir por nivel de consciencia produce
conceptos distintos de verdad, y el estático lo prueba barato antes de pagar un video.

## Antes de empezar: lo que TÚ tienes que poner

| Requisito | Tipo | Cómo se consigue | Si falta |
|---|---|---|---|
| Producto: foto real, link o nombre exacto | Bloqueante | El usuario | Se pide en la única tanda de intake |
| **Estudio de mercado con sus ángulos** (`PROYECTOS/<PRODUCTO>/`: `PRODUCTO.json` + `00-ESTUDIO-*.md` o `.docx` con la Fase 3.5) | **Bloqueante** | `golden-investigacion-mercado` | Se lanza esa skill y se espera el estudio. **No se inventan ángulos.** Decisión de FER (02-oct-2026) |
| Foto real y limpia del producto, sin logo del proveedor | Bloqueante para generar; degradable para la matriz | Ficha de Shopify, proveedor o muestra | La matriz sale; esas piezas quedan `"foto_real": "PENDIENTE"` y `"generar": false` |
| Empresa dueña del canal | Bloqueante | El usuario | Las cuatro empresas no se mezclan; la venta es del canal que la hace |
| País | Degradable | Estudio o usuario | **Colombia** por defecto, declarado en la entrega (la skill original usa Guatemala) |
| Modelo de pago | Degradable | Usuario | **Contraentrega** por defecto |
| Oferta (unidad, combo o kit) y precios | Degradable | Sistema vivo (Shopify o Dropi) | El precio va siempre como variable `{PRECIO_X}`; nunca un número |
| Módulo | Degradable | Usuario | Sin métricas: **módulo 3**. Con un estático que ya tiene métricas: módulo 1 |

Todo lo bloqueante se pide **una sola vez**, al inicio. Lo degradable se decide por convención y se
informa.

## Los 4 módulos (orden natural 3, 1, 4, 2)

| Módulo | Qué hace | Quién lo ejecuta |
|---|---|---|
| **3 · Estáticos** | Valida ángulos barato con imagen. Punto de partida de todo producto nuevo o sin anuncios para modelar | **Esta skill, completo** |
| **1 · Estático validado a guion** | Del estático ganador, con métricas reales, saca el guion de video | `golden-copywriting` (guion), con el traspaso de `references/traspaso-modulos-1-4-2.md` |
| **4 · UGC** | Video grabado con personas | `golden-ugc-avatar` o `golden-video-editor` |
| **2 · Video IA** | Video generado sin grabar | `hyperframes` o `golden-video-editor` (0 créditos). El video de Higgsfield está congelado por FER |

El orden y los módulos están confirmados en la pantalla de arranque de la skill original de Kevin
(`vertex-despliegue-creativo`, taller 01-oct, 02:18:20).

## Las reglas que no se rompen

1. **Sin estudio no hay matriz.** El ángulo sale de la investigación, nunca del catálogo ni de una
   IA preguntada al azar: un ángulo sin cita del cliente es una opinión, y la pauta no paga
   opiniones. Si en la conversación aparecen ángulos de Gemini o ChatGPT (como hizo Kevin en
   vivo), entran solo si una cita del estudio los sostiene.
2. **El producto es el real, grande y protagonista.** La foto real entra como Image 1 en cada
   prompt; la IA nunca dibuja el envase. Achicarlo hace que el motor redibuje la etiqueta (medido
   en la casa, 4 de 4).
3. **El texto se dicta literal y en positivo.** Prohibir una frase en el prompt hace que el
   generador la escriba: "PROHIBIDO antes y después" produjo el titular "El antes y después que
   habla solo". Por eso el prompt nunca lista claims prohibidos; los controla el texto literal.
   Los negativos solo son genéricos: sin logo del proveedor, sin marco, sin deformar el producto.
4. **Nada de promesas que el producto no cumple.** Claims solo de la etiqueta. Sin cifras, reseñas
   ni testimonios inventados (`{RESEÑA_REAL}` sin reseña real = pieza en reserva). Urgencia y
   escasez solo si son reales. Sin antes/después en belleza ni salud, tampoco disfrazado de
   "con/sin". Detalle por categoría en `references/politicas-y-promesas.md`.
5. **Disruptivo sí, aludir a la situación de quien mira no.** "Todos tenemos rachas" pasa; "Estás
   en la mala?" viola la política de atributos personales de Meta.
6. **El rótulo no hace la etapa.** Una pieza TOFU no lleva el nombre del producto en el titular ni
   un llamado de compra; si los lleva, es BOFU aunque diga TOFU.
7. **Cada ángulo en un concepto visual distinto.** Misma plantilla con otro titular = un solo
   anuncio para Meta.
8. **El precio es una variable leída del sistema vivo**, y la imagen con precio nunca va a la
   landing ni a la ficha: solo a pauta o WhatsApp.
9. **Nunca diseños infantiles**: cero confeti, burbujas, globos, stickers o tipografía de juguete.
   "Alegre" es luz y color del producto.
10. **Cobertura, no veredicto.** La entrega dice N de N revisado, qué se ejecutó y qué quedó sin
    verificar. Prohibido "quedó perfecto", "todo bien", "está listo" y "debería funcionar".

## El flujo del módulo 3

### Paso 0 · Intake, inventario y enrutamiento
1. Pide en una sola tanda lo bloqueante de la tabla de requisitos.
2. Busca el estudio en `PROYECTOS/<PRODUCTO>/`. Si no está, invoca `golden-investigacion-mercado`
   y **no sigas** hasta tener su Fase 3.5 (de 3 a 10 ángulos con ficha). Si esa skill no está
   instalada, para y dilo: no hay plan B que fabrique ángulos con evidencia. Mientras el estudio se
   hace, no entregues ángulos ni prompts; al llegar, retoma en el paso 1 en la misma conversación.
   **Estudio anterior a la Fase 3.5** (no tiene sección de ángulos, como los de agosto de 2026): toma
   los ángulos de "Estrategia de mensaje" y de los huecos, cada uno con la cita que lo sostiene. Si así
   no salen al menos 3 ángulos con cita, pide a `golden-investigacion-mercado` que corra solo la Fase
   3.5 sobre el estudio existente; no rehace el estudio entero.
3. Inventaría lo que ya existe en la carpeta del producto (imágenes, copys, matrices anteriores) y
   marca qué sirve y qué no, y por qué. Material con marca, WhatsApp o idioma ajeno no es nuestro.
4. Elige el módulo. Si es 1, 4 o 2, salta a `references/traspaso-modulos-1-4-2.md`.

### Paso 1 · Ficha de producto
Lee del estudio los 10 campos de la ficha de Kevin (identificación, ángulo principal, dolor o
deseo, promesa con semáforo, mecanismo, beneficios en lenguaje del cliente, objeciones, atributo y
público, CTA y gatillo, compliance). Lo que el estudio no trae se marca **"(por confirmar)"** y no
se nombra en ningún texto: ni material, ni medida, ni certificación. Plantilla en
`references/ficha-de-estatico.md`.

### Paso 2 · Matriz de referencias
Lee `references/matriz-de-referencias.md` antes de este paso. Toma de la Fase 3.5 y del inventario
de creativos del estudio los anuncios de la competencia y arma la tabla Referente · Ángulo ·
Formato · Por qué funciona · Semáforo · Versión adaptada. **En rojo se rescata solo la estructura y
el mensaje se reescribe entero.** Cierra con dos recuadros: "Dónde está el hueco" y "Lo que domina,
no pelear de frente". Si el estudio no trae inventario de creativos, busca en la Biblioteca de
anuncios de Meta (`ads_library_search`) y declara que el scraping por texto no ve las imágenes.

### Paso 3 · Ángulos por nivel y bajar el nivel
Lee `references/niveles-de-consciencia.md`. A cada ángulo del estudio asígnale nivel (vocabulario
cerrado: `unaware`, `problem_aware`, `solution_aware`, `product_aware`, `most_aware`) y la
sofisticación del mercado (1 a 5).
- Si menos del 40% de los ángulos está en `unaware` o `problem_aware`, **baja el nivel**: deriva
  ángulos nuevos de nivel 1 y 2 desde las citas del estudio, con al menos uno disruptivo. Cada
  derivado lleva la cita que lo sostiene; sin cita, no entra. El 40% es el punto de partida de la
  casa, no una cifra medida: Kevin y los operadores coinciden en que el mercado se queda arriba,
  pero nadie midió la proporción. Se ajusta con la primera tanda real.
- Excepción: si el producto ya está posicionado o quemado en ese país (el estudio lo mide), puede
  ir directo a BOFU. Kevin lo hace con un producto que ya vende en Guatemala.
- Elige de **2 a 3 ángulos** para la tanda, con nombre memorable, nivel y patrón creativo. Al menos
  uno de nivel bajo y al menos uno disruptivo.

### Paso 4 · Briefs y prompts
Lee `references/formatos-de-estatico.md` y `references/prompts-de-imagen.md`. Produce dos salidas:
- **Matriz ángulo × etapa**: cada ángulo elegido en TOFU, MOFU y BOFU. Con 3 ángulos salen 9 fichas.
- **Batería por formato** (opcional, cuando el usuario quiere más amplitud): hasta 10 prompts que
  cubren formatos distintos, como la de Kevin.

Cada pieza sale en la ficha de `references/ficha-de-estatico.md`: código, formato, etapa, ángulo,
por qué (con la cita), texto literal, jerarquía de lectura, arte, foto real, destino, relación
(4:5 a 1080×1350 por defecto, o 1440×1800 si el motor lo da; 1:1 solo cuando el destino lo pida,
como pieza aparte en la matriz) y el prompt completo en su bloque de código.

### Paso 5 · Validar la matriz
Escribe la matriz en `PROYECTOS/<PRODUCTO>/DESPLIEGUE/matriz.json` (esquema en
`references/ficha-de-estatico.md`) y córrela:

```bash
python3 ~/.claude/skills/golden-anuncios-niveles-de-conciencia/scripts/validar_matriz.py "PROYECTOS/<PRODUCTO>/DESPLIEGUE/matriz.json" > "$TMPDIR/vm.txt" 2>&1; echo "exit=$?"; cat "$TMPDIR/vm.txt"
```

Exit 0 = pasa las 25 casillas. Exit 1 = arregla lo que nombra y vuelve a correr; no entregues con
fallos. Exit 2 = el JSON no se pudo leer o su forma está mal (falta un `id`, un booleano escrito como
texto): corrige la forma antes que el contenido. Si una casilla marca algo que no es lo que parece
(una cifra con unidad leída como precio), arregla el texto (escribe la unidad), nunca la casilla.
Antes de la primera corrida de la sesión, corre `--autoprueba`: si no da PASADA, el validador está
roto y no juzga nada. Las casillas que el script no puede ver (lo que muestra la imagen generada)
las revisa quien ejecuta, con la lista de `references/ficha-de-estatico.md`.

### Paso 6 · Plan de testeo y entrega
Lee `references/plan-de-testeo.md`. Entrega el plan para que `golden-ads` lo monte **en pausa**:
máximo 3 piezas por conjunto, presupuesto parejo entre ángulos, nombre del anuncio
`ANGULO-ETAPA-FORMATO-v1`, MOFU y BOFU con `"estado": "PENDIENTE: requiere públicos"` si la cuenta
no tiene públicos ni píxel (`"cuenta": {"publicos": false}`), y `"edad_minima": 18` en belleza y
salud. Si no sabes si la cuenta tiene públicos, márcalo `false`: es el lado seguro. La imagen la genera `golden-imagen-arena` (o `golden-ecom-magic` con su
`awareness_level`), y esa skill pide el costo antes de gastar.

### Paso 7 · Cierre
1. Imprime en el chat cada prompt completo en su propio bloque de código (el archivo es respaldo).
2. Guarda la entrega en `PROYECTOS/<PRODUCTO>/DESPLIEGUE/`.
3. Para piezas que importan, pide el cierre a `golden-verificador` con solo el estado final y este
   estándar.
4. Reporta al Centro de Mando con `golden-bandeja`.
5. Indica el siguiente paso: lanzar, apagar los ángulos flojos y volver con el ganador y sus 4
   métricas (días activo, CTR, CPA y ventas) para el módulo 1.

## Terminado significa

- [ ] Estudio leído, con ruta, y ningún ángulo sin cita.
- [ ] De 2 a 3 ángulos elegidos, con al menos uno de nivel bajo y uno disruptivo.
- [ ] Cada ángulo en TOFU, MOFU y BOFU, y cada pieza con su ficha completa.
- [ ] `validar_matriz.py` con exit 0 (25 casillas), y su autoprueba PASADA en la sesión.
- [ ] Cada prompt en su bloque de código en el chat.
- [ ] Plan de testeo con máximo 3 piezas por conjunto, para montar en pausa.
- [ ] Entrega con cobertura N de N, lo no verificado y su dueño, y el parte al Centro de Mando.

## Lo que esta skill NO hace

| Pedido | Va a |
|---|---|
| Investigar el producto, sus clientes o la competencia | `golden-investigacion-mercado` |
| Los 5 textos, títulos y descripciones de Meta, hooks sueltos, guiones | `golden-copywriting` |
| Generar, comparar motores o descargar imágenes | `golden-imagen-arena` · `golden-ecom-magic` |
| Montar, analizar o escalar campañas | `golden-ads` |
| Video UGC o avatar | `golden-ugc-avatar` |
| Editar o generar video | `golden-video-editor` · `hyperframes` |
| Lanzar un producto completo (página, creativos, pauta, bot) | `golden360` |
| Matriz de contenido orgánico viral | `golden-matriz-viral` |

Si falta una skill hermana, se dice y se entrega la matriz con la pieza en
`[PENDIENTE: <skill>]`; nunca se reemplaza su trabajo con una versión improvisada.

## Lo que NO está verificado en esta skill

| Reserva | Quién la cierra |
|---|---|
| El archivo original de Kevin (`vertex-despliegue-creativo`) no se ha leído: el método sale de su demostración y de su documento en pantalla | Kevin lo prometió a los alumnos (01-oct, 02:58:13). Se compara contra esta skill al llegar |
| No hay umbral medido en Golden para declarar ganador un estático con contraentrega; los de Kevin y Alejo son referencia | La primera tanda real que monte `golden-ads` |
| Creativos por conjunto: la casa midió máximo 3; Alejo lanza 10 o más | El Centro de Mando, con datos de la primera tanda |
| Corrida real hecha una sola vez (filtro de grifo, hogar, Colombia, 02-oct-2026): matriz válida y control malo atrapado, pero **sin render** porque el producto no tenía foto en disco. Falta una corrida con render y otra en belleza o salud | La próxima tanda real, con los casos de `references/evals.json` |

## Archivos de referencia

| Archivo | Cuándo leerlo |
|---|---|
| `references/niveles-de-consciencia.md` | Paso 3: niveles, regla de titular, sofisticación, cómo bajar el nivel, 36 hipótesis |
| `references/matriz-de-referencias.md` | Paso 2 |
| `references/ficha-de-estatico.md` | Pasos 1, 4 y 5: ficha de producto, ficha de pieza, esquema de `matriz.json`, revisión visual |
| `references/formatos-de-estatico.md` | Paso 4: formatos por nivel, anatomía, medidas y zonas seguras |
| `references/prompts-de-imagen.md` | Paso 4: estructura del prompt por motor |
| `references/politicas-y-promesas.md` | Pasos 1 a 4, siempre que haya claims |
| `references/plan-de-testeo.md` | Paso 6 |
| `references/traspaso-modulos-1-4-2.md` | Paso 0 si el módulo no es 3, y paso 7 |
| `references/fuentes-kevin.md` | Cuando haya duda sobre qué dijo Kevin y qué es de la casa |
| `references/changelog.md` | Al editar la skill |
| `references/evals.json` | Al probar o mejorar la skill |

## Operación

```bash
python3 ~/.claude/skills/golden-anuncios-niveles-de-conciencia/scripts/validar_matriz.py --autoprueba
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-anuncios-niveles-de-conciencia
```

El script usa solo la librería estándar de Python 3, sin instalar nada. Si `python3` no está, la
matriz se revisa a mano con la tabla de casillas de `references/ficha-de-estatico.md` y la entrega
lo declara.
