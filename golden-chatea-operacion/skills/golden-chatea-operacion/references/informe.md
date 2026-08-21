# Formato del informe

El entregable es un informe de **cobertura**, no un veredicto. Mismo patrón que la hermana. Se
escribe en un archivo con el espacio y la fecha operada en el nombre:
`OPERACION-<espacio>-<AAAA-MM-DD>.md`, en la carpeta del proyecto, sobre el mismo archivo si se
vuelve a correr el mismo día (estado vivo, nunca respaldos numerados).

**Frases prohibidas:** "quedó perfecto", "todo bien", "está listo", "debería funcionar".

## Esqueleto

```markdown
# Operación de Chatea Pro · <NOMBRE DEL ESPACIO> · <fecha operada>
<fecha y hora de la corrida> · espacio medido `<user_ns>` · token `<archivo>` · API respondió <código>

## 1. Universo del día
| Objeto | N |
|---|---|
| Contactos según /flow/bot-users-count en la ventana | N |
| Hilos efectivamente descargados | N de N |
| Hilos que no se pudieron traer | N (con el motivo de cada uno) |
| Contactos excluidos del denominador de conversión (`opted_in_through: dropi`) | N |
| Mensajes totales en el día (excluidas notas de pixel) | N |

## 2. La empresa se fue de último — PRIMERO, siempre
Lista completa, no muestra. Un contacto por fila: nombre/`user_ns`, último mensaje del cliente
citado, hace cuánto (parseado, no de texto), paso del embudo donde quedó, si preguntó algo sin
cobertura.

## 3. Cobertura
| Bloque | Controles | Corridos | Conversaciones revisadas | Sin verificar |
|---|---|---|---|---|
| P · trampas de parseo | 13 | N | — | — |
| Q · clasificación | 6 | N | N de N | Q2 es heurística, declarada |
| R · calidad de respuesta | 6 | N | N de N | R5 (necesita ficha de producto real) · R6 solo intra-chat, sin Dropi |

**Lo que NO se verificó y por qué** — lista explícita.

## 4. Hallazgos
Ordenados por severidad. Uno por caso, con esta forma:

### 🔴 MUERTO · R1 · Cliente sin respuesta 3h40 después de preguntar por el precio
**Qué pasa:** `user_ns f...` preguntó "cuánto cuesta con envío?" a las 14:02 y no hay ningún
mensaje de la empresa después, hasta el corte del día a las 17:42.
**Evidencia:** hilo citado, mensaje del cliente y hora parseada, último evento del hilo.
**Consecuencia:** cliente caliente probablemente perdido.
**Qué habría que hacer:** contactar hoy. Si además la dirección que dio parece mala, se remite
a `golden-logistica-diaria` en una línea aparte, no se desarrolla aquí.
**Confianza:** medido contra el hilo real del <fecha>.

Un hallazgo `R6` (coherencia intra-chat) va con la misma forma, con dos reglas propias que no
se omiten al escribirlo: (1) el campo **Consecuencia** siempre incluye la advertencia de que
puede ser un aviso legítimo de que el cliente cambió de opinión más tarde en el chat — nunca se
redacta como si el resumen del bot estuviera confirmado mal; (2) el campo **Qué habría que
hacer** siempre nombra la frontera: "solo chat, sin Dropi — con Dropi conectado,
`golden-logistica-diaria` hace la confirmación definitiva contra el pedido real".

## 5. Preguntas sin cobertura en el prompt (para golden-chatea-pro-prompt-ventas)
Lista agrupada por producto, con la pregunta real citada y cuántas veces se repitió en el día.
Esto es materia prima, no una edición ya hecha.

## 6. Atribución por anuncio
Tabla `source_id` → N conversaciones → N con "empresa se fue de último" → N sin atribución
(orgánico). No se cruza contra el gasto de Meta aquí — eso es de otra skill si se pide.

## 7. Calidad de la respuesta — frases prohibidas dichas por el bot
Cada mención citada con su hilo, nunca un conteo sin evidencia. Si no se declaró el modo de
pago del espacio (`--modo cod`/`--modo prepago`), cada mención queda como 🔵 DUDA explícita.

## 8. Lo que está sano y cómo se comprobó
Se nombra lo verificado con su método, sin adjetivos: "de 84 conversaciones, 79 tuvieron
respuesta de la empresa en menos de 10 minutos, medido con parse_fecha sobre el hilo real".

## 9. Frontera — hallazgos pasados a otras skills
Lista corta: qué se detectó, a cuál skill se remite, en una línea cada uno.

## 10. Preguntas para FER
Los hallazgos 🔵 DUDA.

## 11. Verificación adversarial
Resultado de `golden-verificador`: qué intentó romper, qué encontró, qué declaró como no
verificable.
```

## Si se activó la compuerta de cordura (o el denominador de la Fase 1 no cuadra)

El informe normal **no se escribe, y `clasificar.py` tampoco lo IMPRIME**: `imprimir()`
verifica el aborto antes de tocar la sección de hallazgos, así que ni la evidencia citada del
hilo ni la cobertura completa salen a pantalla en este modo — solo el universo y el aviso de
aborto. Es a propósito: una salida que mezclara "no se publica nada" con el detalle completo de
20 hallazgos sería, en la práctica, publicar el informe que se dijo que no se iba a publicar.

Para que un humano pueda revisar el porcentaje sin reconstruir la corrida, se deja un archivo
mínimo (`OPERACION-<espacio>-<fecha>-COMPUERTA.md`) con: el porcentaje medido, cuántas
conversaciones entraron en `cierra_con_cliente == True` (ya excluidos los contactos `dropi`),
tres `user_ns` para que un humano abra esas conversaciones EN CHATEA y juzgue si el patrón de
cierre está mal calibrado o si el día es real (no se citan aquí, para no reintroducir por la
puerta de atrás la evidencia que la compuerta impidió imprimir), y la recomendación de no
publicar hasta revisar `clasificar.py` o esas conversaciones.

## Reglas de escritura

- **Cada hallazgo lleva evidencia citada del hilo real**, con la hora parseada, nunca solo "el
  bot no respondió".
- **Los números llevan su denominador.** "40 hilos sin cobertura" no dice nada; "40 de 213
  conversaciones del día" sí.
- **Nunca se pega una credencial**, aunque el cliente la haya escrito en el chat por error.
- **La moneda no se convierte.** Si el espacio es COP, el informe es en COP; `parse_dinero`
  declara qué formato detectó en cada cifra citada.
- **Cuando aparece un fallo, se busca LA CLASE, no el caso.** Si un producto tiene 5 preguntas
  sin cobertura sobre el mismo tema, el informe dice que es un hueco de prompt, no cinco fallos
  sueltos.
- **Un hallazgo de pedido no se desarrolla aquí.** Se nombra, se remite a
  `golden-logistica-diaria`, se sigue.

## Después del informe

- Las preguntas sin cobertura se pasan a `golden-chatea-pro-prompt-ventas` como materia prima.
- Las sospechas de configuración rota (interruptor apagado, disparador que no entra) se remiten
  a `golden-chatea-auditoria` para que las confirme contra la instalación real — esta skill no
  las corrige ni las declara probadas por sí sola.
- Si el hallazgo cambia el estándar de trabajo, se registra en memoria canónica y se avisa al
  Centro de Mando.
