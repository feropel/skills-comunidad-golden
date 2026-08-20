# Catálogo de controles · operación diaria de Chatea Pro

Se recorre **entero**. Revisar "lo importante" está prohibido: o se corren todos los controles,
o se declara en el informe cuáles no se corrieron y por qué.

Cada control lleva: qué mide · cómo se mide · por qué existe · severidad si falla. Columna
**auto**: `A` lo corre `clasificar.py`, `H` es lectura humana obligatoria.

---

## Bloque P · Trampas de parseo y extracción (P1-P13)

Son las 13 trampas medidas del encargo, convertidas en control ejecutable. El detalle de cada
una y el caso real que la pagó está en `api.md`. Aquí solo el criterio de clasificación:

| # | auto | Control |
|---|---|---|
| P1 | A | **`include_bot=1` fue usado.** Se verifica que el hilo de cada contacto contenga al menos un mensaje saliente (`direccion == "empresa"`), salvo que el contacto tenga cero mensajes en absoluto. Un contacto con solo mensajes entrantes y ninguno saliente en TODO el día es sospechoso de extracción sin `include_bot=1` y se reporta como DUDA, no como "abandonado", hasta confirmar contra el servidor. |
| P2 | A | **Estructural, en `extraer.py`.** La función de descarga de hilo usa `user_ns` en la URL, nunca `subscriber_id`. Se verifica leyendo la firma de la función, no con un dato del DUMP. |
| P3 | A | **El hilo queda en orden cronológico** (viejo→nuevo) tras `invertir_hilo`. Se verifica comparando el primer y el último `ts` parseado del hilo ya invertido: el primero debe ser ≤ el último cuando ambos existen. |
| P4 | A | **Fallback explícito cuando `ts` es `None`.** Si NINGÚN mensaje del hilo trae `ts`, `invertir_hilo` invierte la lista tal cual llegó en vez de intentar un `sort` que no mueve nada. Se verifica que el resultado con todos los `ts` en `None` sea la lista literalmente invertida, byte a byte. |
| P5 | A | **`type == "note"` se excluye** (campo primario, confirmado por medición de producción; `msg_type == "note"` es el respaldo si `type` no vino) antes de cualquier clasificación de dirección o de contenido. Se verifica contando cuántas notas había en el DUMP crudo y confirmando que ninguna sobrevive en el hilo clasificado. |
| P6 | A | **El mensaje predefinido del botón del anuncio se detecta y se excluye** de la lista de mensajes del cliente usada para calcular objeciones y motivo de no-compra. Detección MEDIDA, no una regex fija (mismo criterio validado en `golden-logistica-diaria`, que perdía en las dos direcciones con una regex): una frase que aparece **idéntica en 3 o más contactos distintos**, o que domina por frecuencia sobre el corpus de "primer mensaje de cada contacto", es la plantilla del botón — nadie teclea la misma frase exacta por coincidencia. Una regex fija se equivoca en ambas direcciones: se traga texto tecleado detrás del botón, y falla si cambia un signo de apertura. |
| P7 | A | **El motivo de no-compra se calcula SOLO sobre mensajes con `direccion == "cliente"`**, excluyendo el mensaje automático del anuncio (P6). Nunca se busca la palabra de objeción en el hilo completo. |
| P8 | A | **Audio usa `payload.transcribed_text`, no `content`.** Un mensaje `msg_type == "audio"` con `content` vacío y `transcribed_text` presente se clasifica con el texto transcrito, nunca como mensaje vacío. `msg_type == "feed"` se clasifica como comentario de Facebook, no como chat privado, y no cuenta en el denominador de conversación privada salvo que se declare aparte. |
| P9 | A | **Toda comparación de fecha usa `parse_fecha`**, nunca comparación de cadena. Se verifica con un par de fechas donde la comparación textual y la parseada dan resultados opuestos (una con espacio más reciente que una con `T` en texto, pero más vieja en tiempo real) y se exige que el clasificador use la parseada. |
| P10 | A | **`parse_dinero` distingue el formato ANTES de limpiar.** `142.800` se lee como miles (142800) y `74900.00` se lee como decimal (74900.00); nunca se le quita el punto a ciegas. Se verifica con ambos formatos en la misma corrida. |
| P11 | A | **Los contactos con `opted_in_through == "dropi"` se excluyen del DENOMINADOR de conversión** — de la tasa de `cierra_con_cliente` (incluida la que alimenta la compuerta de cordura) y de cualquier otra tasa que esta skill calcule —, y la exclusión se declara en el informe con su conteo (nunca en silencio). Van en `excluidos_dropi` y siguen contando en el universo total de contactos del día; lo único de lo que salen es del denominador de las tasas. |
| P-desc | A | **Un mensaje cuya dirección no calza con ningún campo conocido (`type`/`direction`/`sender`/`is_bot`) se declara `desconocido` y genera un hallazgo propio**, nunca se cuenta en silencio como si no existiera. Un cambio de nombre de campo en el proveedor debe hacerse VISIBLE, no convertir la skill en una que calla. |
| INV | A | **El denominador de la Fase 1 se verifica antes de clasificar.** Si `extraer.py` declaró `traidos != declarados_por_servidor` en `_conteos.contactos_del_dia`, el clasificador NO produce el informe normal: emite un único hallazgo `INV` MUERTO y se detiene (mismo criterio que "el informe se detiene" de `golden-chatea-auditoria` cuando la paginación no cuadra). |
| P12 | A | **Ningún campo autollenado por el anuncio se usa como evidencia de conversación real** sin declararlo. Concretamente, `Productos escogidos` (si aparece en `get_info`) no se usa para decidir producto de interés o intención de compra; se prefiere lo que el cliente escribió o `Cantidad de productos` si está presente, y se declara la fuente usada en cada caso. |
| P13 | A | **Compuerta de cordura.** Ver más abajo — sección propia porque aborta la corrida entera. |

## Bloque Q · Clasificación de cada conversación

| # | auto | Control |
|---|---|---|
| Q1 | A | **Quién habló de último.** Sobre el hilo ya limpio de notas (P5), se mira la dirección del último mensaje. Si es `cliente`, la EMPRESA se fue de último y esa conversación entra a la lista que abre el informe. Si es `empresa`, se evalúa además si ese último mensaje cierra la conversación (Q6) o si solo fue el último turno de un intercambio que sigue abierto. |
| Q2 | A | **Paso del embudo donde murió.** Heurística por palabras clave del último mensaje de la EMPRESA antes del silencio: saludo/inicio, pidiendo datos (dirección, teléfono, ciudad), confirmando pedido, cierre. **Se declara como heurística (`🔵 DUDA`)**, no como hecho verificado contra la config real del producto — cruzar contra el prompt exacto es trabajo de lectura humana o de `golden-chatea-auditoria`. |
| Q3 | A | **Si el bot respondió, tardó o fue incoherente.** Ver Bloque R. |
| Q4 | A | **Preguntas del cliente sin cobertura.** Un mensaje de `cliente` que contiene signo de interrogación (o palabra interrogativa: qué, cómo, cuándo, dónde, cuánto) seguido de una respuesta de la EMPRESA que es una plantilla de fallback genérica (frase corta, o repite el saludo inicial) se marca como pregunta sin cobertura. Se junta la lista completa para pasarla a `golden-chatea-pro-prompt-ventas`. |
| Q5 | A | **Atribución por anuncio.** `payload.referral.source_id` del primer mensaje del hilo que lo traiga. Sin `referral`, se declara "orgánico o sin atribución", nunca se asume un anuncio por defecto. |
| Q6 | A | **"Cierra con el cliente".** El último mensaje es de la EMPRESA y su contenido coincide con un patrón de cierre real (confirmación de pedido, agradecimiento post-venta, respuesta afirmativa a una pregunta concreta del cliente) — no basta con que el bot haya hablado último. Ver la compuerta de cordura, que usa exactamente esta definición. |

## Bloque R · Calidad real de la respuesta

**`config sana ≠ bot diciendo lo correcto`.** Este bloque mide lo que el bot escribió, palabra
por palabra, no lo que la configuración sugiere que va a decir.

| # | auto | Control |
|---|---|---|
| R1 | A | **Sin respuesta.** Un mensaje de `cliente` sin ningún mensaje de `empresa` después. Va SIEMPRE primero en la lista del informe. Severidad: 🔴 MUERTO si pasaron 2 horas o más entre ese mensaje y el corte del día (el `ts` más nuevo visto en todo el DUMP de esa corrida); 🟠 RIESGO si el gap es menor o no se pudo medir (falta `ts`). El umbral de 2 horas es el mismo que declara `SKILL.md`. |
| R2 | A | **Respuesta tardía.** Gap entre un mensaje de `cliente` y la siguiente respuesta de `empresa`, medido con `parse_fecha` (nunca con texto), contra un umbral configurable (`UMBRAL_TARDANZA_MIN`, por defecto 30 minutos). Se reporta el gap real en minutos, no solo "tardó". |
| R3 | A | **Bot en bucle.** Tres o más mensajes consecutivos de `empresa` con contenido idéntico (o casi idéntico, normalizado) sin un mensaje de `cliente` entre medio que lo justifique. Señal de que el flujo se rompió y quedó repitiendo el mismo nodo. |
| R4 | A | **Frases prohibidas dichas por el bot.** Lista configurable (`FRASES_PROHIBIDAS`, ejemplo: "pago anticipado", "pago adelantado", "transferencia antes de despachar") buscada SOLO en mensajes de `empresa`. Ejemplo medido en otro espacio: 238 de 597 respuestas mencionaban pago adelantado en un modelo que era 100% contra entrega. Sin un modo declarado (`--modo cod` o `--modo prepago`), cada mención se reporta como `🔵 DUDA` con el texto citado, nunca se asume cuál es el modelo de pago correcto. |
| R5 | H | **Coherencia con el producto real.** Si el bot promete un precio, un plazo o un contenido de paquete, se contrasta contra la ficha real — lectura humana, esta skill no tiene acceso a la ficha de producto (eso vive en `golden-chatea-auditoria` / Dropi). |

## Compuerta de cordura (P13 / Q6) — detalle

**Definición exacta de "cierra con el cliente":** el último mensaje del hilo es de la `empresa`
Y su contenido coincide con un patrón de cierre real (confirmación de pedido, agradecimiento
post-venta, respuesta afirmativa a la última pregunta concreta del cliente). No basta con que la
empresa haya hablado último — un mensaje de "¿sigues ahí?" sin respuesta no es un cierre.

**Regla:** si más del 90% de las conversaciones del día clasifican como `cierra_con_cliente ==
True`, el resultado es absurdo de cara — ningún espacio real cierra así de bien, todos los días,
sin excepción. **Se aborta la corrida sin escribir el informe de operación**, y en su lugar se
escribe un hallazgo único: "compuerta de cordura activada, revisar el clasificador o el patrón
de cierre antes de confiar en esta corrida". Esto protege contra un patrón de detección de
cierre demasiado laxo (falso positivo masivo) tanto como contra un día real anómalo — cualquiera
de los dos merece que un humano mire antes de publicar.

## Exclusión declarada de contactos `dropi`

Los contactos que `get-info` marca con `opted_in_through: "dropi"` nacen de un pedido que ya
existía (la integración los crea, no llegaron por conversación). Se excluyen del DENOMINADOR de
cualquier tasa de conversión o de respuesta que calcule esta skill, y se listan aparte con su
conteo — nunca desaparecen del universo declarado en la Fase 1, solo del cálculo de tasas.

## Frontera con `golden-logistica-diaria`

Si al clasificar aparece algo que es en realidad un problema de PEDIDO — una dirección que el
cliente dio y que se ve mal, un posible duplicado, una novedad de transportadora mencionada en
el chat — se anota en una línea dentro del hallazgo correspondiente y se remite a
`golden-logistica-diaria` por su nombre. No se desarrolla el análisis logístico aquí: esta skill
no tiene acceso a Dropi ni a las reglas de transportadora.
