---
name: golden-chatea-pro-validacion-direcciones
description: >-
  Golden Group — Genera el PROMPT de validación de direcciones del asistente logístico de
  Chatea Pro (es el "hijo" de golden-chatea-pro-config-logistico, equivalente a lo que
  prompt-ventas es para ventas-wp). Valida la dirección del cliente antes del envío contra
  entrega (COD) para minimizar devoluciones: lee la dirección como la escribe la gente (con
  errores, emojis, mezclada con nombre y teléfono) y decide si un mensajero puede entregar
  sin llamar. Salida en UNA sola línea (dirección correcta / falta que proporcione [dato]).
  Trae packs listos de 23 países: los 11 de LatAm (Colombia es el patrón oro), Brasil y los
  11 de Europa (España, Portugal, Rumanía, Polonia, Hungría, Eslovenia, Eslovaquia, Croacia,
  Grecia, Bulgaria y Chequia). El país es parámetro, no puerta: sin pack se INVESTIGA y se
  genera igual, nunca se rechaza. Úsala cuando el usuario quiera el PROMPT de validación en
  sí, probar cómo se lee una dirección concreta, o llevar la validación a un país nuevo.
---
<!-- skill v2.12 · 2026-09-22 · chile.md reconstruido sobre el molde canonico (fila de otro chat, proyectos-69, consolidado este dia) · segunda verificacion adversarial: corrigio 8 fallos (numeros quemados en la propia seccion de herramientas, un detector de higiene que no cazaba telefono local ni frase de negocio, el criterio de CP evadible con parrafo opcional/omitir, banco de casos con 7 paises sin cobertura, la tabla de sincronizacion con una copia faltante y una afirmacion falsa sobre el espejo Codex). Acta completa en references/changelog.md. -->
<!-- Historial completo de esta skill: references/changelog.md. El cuerpo se paga en cada activación; el acta no. -->
# Golden · Chatea Pro — Validación de Direcciones (hijo del logístico)


## LEY: NUNCA HEREDAR DATOS ENTRE ESPACIOS (FER 2026-08-08)

Al basarse en una cuenta guía (Golden o cualquier otra) se hereda **estructura, prompts y
configuración de asistentes** — JAMÁS datos, en ninguna dirección, ni entre marcas propias:

- **APIs y tokens** de cualquier tipo: ElevenLabs, OpenAI, Dropi, Shopify, el token del propio bot.
- **Plantillas de WhatsApp**: `name`, `namespace`, `lang` y `status` van atados al WABA de cada
  espacio; copiarlas rompe el destino (llama plantillas que su WABA no tiene o que Meta no aprobó).
- **Datos personales y de marca**: teléfonos, correos, dominios, nombre de la empresa, firmas en
  mensajes al cliente.
- **Productos** y sus disparadores.
- **Claims y cifras de negocio**: años en el mercado, número de clientes, porcentajes de
  entrega, premios. Heredarlos no rompe nada técnico — ningún barrido de llaves los detecta —
  pero ponen al bot a MENTIRLE al cliente con datos de otra empresa. Caso real (2026-08-08): la
  plantilla maestra clonada traía "Más de 100.000 clientes atendidos en Colombia" (dato de
  Golden) a punto de quedar en boca del bot de otro espacio.

**Única excepción autorizada:** Le'côterra como producto-ejemplo en los espacios de trabajo
(asistente de WhatsApp y de comentarios), para que la gente vea cómo se configura un producto.

**La guía tampoco puede llevar nada de eso adentro**: un material de referencia con una llave o un
dato personal ya está mal, aunque nadie lo copie.

**Método obligatorio al escribir en un espacio ajeno** — ANTES de escribir, barrer lo que se va a
escribir buscando `sk_`, `shpat_`, `eyJ`, teléfonos, correos, dominios, nombres de plantilla y de
marca del origen; si aparece algo, NO se escribe. DESPUÉS de escribir: releer del servidor y barrer
otra vez. Herramienta encadenable del barrido (ruta del proyecto Golden, fuera de esta skill —
si no existe en el entorno actual, hazlo a mano con el mismo criterio de patrones):
`PROYECTOS/STACK-GOLDEN/barrido-datos-ajenos.py` (correrla ANTES de escribir y DESPUÉS releyendo del
servidor; sale con código 3 si encuentra algo CRITICA).

**LA MARCA VIVE TAMBIÉN EN PROSA LIBRE, no solo en campos estructurados.** Preservar las
llaves de identidad del destino NO basta: el nombre de la marca de origen viaja escondido dentro
de ganchos posventa, agradecimientos y plantillas de prompt. Al método de barrido se le añade el
paso `grep -i` por el NOMBRE de la marca de origen sobre TODO el texto que se va a escribir —
así se cazaron 10 menciones de la marca origen en 3 campos del destino que el mapeo de llaves
no vio.

Origen: 2026-08-08, al clonar la config de Golden a otro espacio se colaron la llave de ElevenLabs,
el teléfono, la plantilla de notificación y agradecimientos firmados con la marca del origen.
Revertido el mismo día desde respaldo.

Genera el **prompt de validación de direcciones**: el cerebro del asistente logístico. Su trabajo es leer la dirección que escribió el cliente y decidir si un mensajero podría **entregar sin llamar**. Si sí → la aprueba. Si falta algo → pide exactamente el dato faltante.

Esta skill es el **hijo** de `golden-chatea-pro-config-logistico` (el padre configura el asistente logístico completo; esta genera el prompt de validación que va dentro). Es el análogo de `golden-chatea-pro-prompt-ventas` dentro de `golden-chatea-pro-config-ventas-wp`.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. El prompt se genera con el pack del país del workspace.
> 🔴 **EL PAÍS ES PARÁMETRO, NO PUERTA** (mandato de FER, 2026-09-06: *"hoy son diez, mañana doce,
> pasado treinta; el país se pide para saber cómo enfocarlo, no para prohibir"*). Esta línea decía
> *"si piden un país fuera de esos 10, avisa que Chatea Pro no lo acepta antes de generar nada"*.
> **Eso era una puerta**, y encima en la skill a la que el logístico delega: bastaba para que un
> negocio real se quedara sin configurar.
>
> **Esta skill trae pack listo para 23 países** (la lista viva está en el paso 2 del flujo y, como
> dato duro, en `references/limites.json`; el número no se escribe dos veces a mano — esta línea
> decía "8 países" en la misma revisión en que pasaron a 23, y el número viejo sobrevivió a la edición). Esa lista dice **dónde ya no hay que
> investigar**, no a quién se le genera el prompt. **Para cualquier otro país se INVESTIGA y se
> genera igual** (§País nuevo). Si además la plataforma no lo ofrece en su desplegable, eso se
> **dice como dato**, no como negativa — y el prompt se entrega, porque el pack sirve el día que lo
> habiliten y porque el negocio puede necesitarlo por otra vía.

## 🔴 EL TOPE DEL CAMPO DONDE ATERRIZA ESTE PROMPT: 8.000 (medido 2026-09-08)

El prompt que genera esta skill va a un sitio concreto: **Configuración Asistente Logístico →
CONFIRMACIONES → Análisis de dirección → `Prompt de análisis de dirección`**. Ese campo tiene
tope nativo de **8.000 caracteres**, y el panel lo pinta encima: en el espacio de referencia
marcaba **7.833/8.000**, o sea **167 de margen**.

**Hasta hoy esta skill no mencionaba ningún tope**, ni ese ni el del bot field. Un prompt de
direcciones bien hecho ronda ya los 7.800 caracteres, así que la próxima mejora que le añada un
párrafo lo pasa — y **pasarse no da error**: se guarda cortado y el panel se ve normal. Un
prompt de validación cortado por la mitad no falla ruidosamente: valida peor y devuelve
direcciones malas como buenas, que es exactamente el daño que esta skill existe para evitar.

**Antes de entregar, medir:**

```python
assert len(prompt) <= 8000, f"{len(prompt)} caracteres: el campo corta en 8.000"
```

Y si no cabe: **se recorta contenido, no se recorta la estructura.** Lo primero que sobra son
los ejemplos repetidos de nomenclatura; lo último que se toca es el contrato de salida.

**El tope es del campo, no del prompt.** Si Chatea lo cambia, el número de aquí caduca en
silencio — como caducó el "no hay tope" del logístico, que fue verdad en agosto y falso en
septiembre. **Se mira el contador del panel antes de escribir**, siempre; este 8.000 es la
última medida, no una garantía.

## Contrato de salida (obligatorio, una sola línea)

El asistente responde **exactamente** uno de dos casos, sin saludos, sin explicaciones, sin emojis extra:

- **Entregable** → la frase literal: `dirección correcta`
- **Falta info** → la pide en registro local cordial: `Para completar su envío, nos regala [el dato que falta]?`

🔴 **`dirección correcta` es SEÑAL DE MÁQUINA y NO SE TRADUCE NUNCA**, ni en Brasil ni en los 11
de Europa. No es un mensaje al cliente: el flujo del logístico la lee para avanzar, y su propio
prompt de producción trae una "CAPA 2 — COMPORTAMIENTO EN FLUJO" que actúa sobre esa salida.
Escrita `endereço correto` o `adres poprawny`, el flujo no la reconoce y **el pedido se queda
parado sin dar ningún error**. Lo que sí va en el idioma del cliente es la petición del dato.

⚠️ **Divergencia declarada, no resuelta.** El JSON de producción de Golden usa como señal
negativa `falta que proporcione [dato]`; el patrón oro y los packs derivados usan la forma
cordial de arriba; la `description` de esta skill trae la de producción. La señal POSITIVA
coincide en las tres y es la única verificablemente crítica, así que el validador exige esa y
acepta las dos negativas. **Cuál de las dos espera el flujo por texto no se ha podido verificar
sin entrar a un espacio vivo** — está anotado en `limites.json`.

Evalúa SIEMPRE la dirección **completa acumulada** en la conversación; responde `dirección correcta` solo cuando ya no quede duda operativa.

**El código postal es criterio POR PAÍS, no global** (trampa que ya nos mordió: el pack de México heredó de Colombia un "NUNCA exijas código postal" que en México es falso): en **México, Argentina, Brasil y los 11 de Europa el CP es REQUERIDO** — 14 países; en **Colombia, Chile, Ecuador, Panamá, Perú, Paraguay, Guatemala, Venezuela y Costa Rica no se pide** — los otros 9 (mandan barrio/comuna/distrito/corregimiento/cantón y las referencias). El criterio vivo y verificable está en `references/limites.json`, campo `cp_requerido`; esta lista es prosa de apoyo y ya sobrevivió una vez a la expansión de 8 a 23 países sin actualizarse (hallado por verificación adversarial 2026-09-22: seguía enumerando solo 6). Cualquier país clonado de otra plantilla hereda el criterio equivocado: al tocar un pack, revisar criterio por criterio contra `limites.json`, no asumir.

## Principio rector

> Si un mensajero/repartidor puede llegar sin llamar → **válida**. Si hay riesgo real de devolución → **falta info**.

Dos capacidades del prompt:
1. **Interpretar** cómo escribe la gente (nomenclatura, barrios, conjuntos/torres, rural, GPS), aun con errores.
2. **Pedir** el dato faltante en el registro de atención del país (en Colombia: trato de usted, "nos regala…?").

## Cómo generar el prompt (flujo)

1. **Pregunta el país** del workspace.
2. **Carga el pack del país** desde `references/`. **Hay 23 packs.** Cualquier país que no esté va al flujo de §País nuevo, que lo construye — no lo rechaza:

   **América (12)** · 🇨🇴 `references/colombia.md` **(patrón oro: estructura, tono y exigencia de referencia)** · 🇲🇽 `references/mexico.md` (CP REQUERIDO) · 🇨🇱 `references/chile.md` (manda la comuna) · 🇪🇨 `references/ecuador.md` · 🇵🇦 `references/panama.md` · 🇵🇪 `references/peru.md` (manda el distrito) · 🇵🇾 `references/paraguay.md` (esquinas c/ y e/) · 🇬🇹 `references/guatemala.md` (manda la zona) · 🇦🇷 `references/argentina.md` (CP REQUERIDO, voseo) · 🇧🇷 `references/brasil.md` (CEP REQUERIDO, es el dato rey) · 🇻🇪 `references/venezuela.md` (manda la urbanización) · 🇨🇷 `references/costa-rica.md` **(el país más distinto: no hay calle ni número, se ubica por referencia + metros + rumbo)**

   **Europa (11)** · 🇪🇸 `references/espana.md` · 🇵🇹 `references/portugal.md` · 🇷🇴 `references/rumania.md` · 🇵🇱 `references/polonia.md` · 🇭🇺 `references/hungria.md` **(orden inverso: CP y ciudad primero)** · 🇸🇮 `references/eslovenia.md` · 🇸🇰 `references/eslovaquia.md` · 🇭🇷 `references/croacia.md` · 🇬🇷 `references/grecia.md` · 🇧🇬 `references/bulgaria.md` **(hay direcciones completas SIN calle: ж.к. + bloque)** · 🇨🇿 `references/chequia.md`

   🔴 **En los 11 de Europa y en Brasil el código postal es OBLIGATORIO; en Argentina y México también.** Clonar a Europa el "NUNCA pides código postal" de Colombia rompe doce países de una sola vez. El criterio de cada país vive en `references/limites.json` y lo comprueba el validador: no lo decidas de memoria.

3. **Confirma con el usuario los datos operativos del negocio** que el pack necesita (no los inventes) — o recíbelos del padre `golden-chatea-pro-config-logistico`. Pídelos TODOS de una vez (intake único, no goteado):
   - **Transportadoras habilitadas** para domicilio y para recogida en oficina (varían por negocio).
   - Si hay **recogida en oficina** y con qué transportadoras.
   - Cualquier transportadora **prohibida** por ese negocio. Los vetos son de UNA operación, nunca del país: no se heredan entre negocios ni entre países, y la lista concreta de cada operación vive fuera de esta skill.
   - Si conserva los emojis de estado (✅/⚠️) o no.
   - Si el negocio no puede confirmar algún dato en el momento (caso típico: Panamá, Perú, Paraguay con transportadoras en `[PENDIENTE]`), dilo explícitamente en el entregable como pendiente con dueño — nunca inventes ni dejes el placeholder sin avisar.
4. **Verifica el prompt antes de entregarlo** (paso de QA, no te lo saltes): relee el prompt armado y confirma que cumple el contrato de salida (una sola línea, sin saludos, sin explicaciones, con o sin emoji SEGÚN el país), que las transportadoras que puso el usuario quedaron en la lista y no quedó ninguna inventada, y que ningún `[PENDIENTE]` llegó al texto final sin que el usuario lo haya resuelto o aceptado dejarlo así.
5. **Entrega el prompt final** listo para pegar en el campo de validación del asistente logístico de Chatea Pro.

**Definición de "terminado":** el prompt entregado (a) usa el pack del país correcto, (b) trae solo transportadoras confirmadas por el usuario — ninguna inventada ni heredada de otro país, (c) respeta el contrato de una sola línea de salida con el registro de cortesía del país, y (d) no contiene ningún `[PENDIENTE]` que el usuario no haya resuelto o aceptado conscientemente. Si falta cualquiera de los cuatro, no está listo para pegar.

## País nuevo (no está en references/)

**Sin pack no se rechaza a nadie: se construye.** Veintitrés países ya lo tienen (arriba). Para
cualquier otro el pack **se construye en el momento**, tomando como base el pack más cercano en
forma de direccionar — no siempre Colombia: para un país que se ubique por referencias el patrón
es Costa Rica, y para uno europeo, España o el vecino más parecido.

🔴 **MOLDE DE PAÍS NO HISPANOHABLANTE** (Brasil y los 11 de Europa ya lo usan): el prompt se
escribe **en español**, que es la lengua en la que esta skill se mantiene y se audita, y **solo
la frase que ve el cliente** va en el idioma local. Escribir el prompt entero en polaco o en
griego deja la skill inauditable —nadie de la casa puede revisar su criterio— y además rompe el
validador, que compara criterios en español. Se probó primero al revés, con Brasil escrito
entero en portugués, y el validador dio un fallo falso: el pack sí exigía el CEP, pero los
detectores estaban en español.

🔴 **LO DEL PAÍS SE INVESTIGA, NO SE LE PREGUNTA AL NEGOCIO** (ley de FER, 2026-09-06). Esta
sección decía *"preguntando los datos operativos al negocio"*, y eso es cobrarle al cliente
nuestro trabajo — con el riesgo añadido de que conteste mal y esa respuesta quede escrita como
regla. Sus palabras: *"La jerga y la configuración de las direcciones no se le pregunta a la
gente, porque precisamente para eso es la skill. Tú tienes que ir a Internet, revisar, estudiar,
analizar, extraer esa información y configurarla."*

🔴 **LA FUENTE AUTORITATIVA DE ESTE DOMINIO ES LA UPU** (Unión Postal Universal), y hasta el
2026-09-08 esta skill no la nombraba. Su estándar **S42** define los componentes de una dirección
postal y publica **plantillas de dirección país por país** (SAFD, *Standardized Address Format
Description*), con más de 70 países conformes; su herramienta *Postal Addressing Systems* da el
formato correcto de cualquier país, y el *Universal POST\*CODE® Database* cubre los 192 miembros.
Empieza SIEMPRE por ahí: es la especificación del sistema, no lo que se supone que hace.
`https://www.upu.int/en/postal-solutions/programmes-services/addressing-solutions`
(las plantillas XML y la base de códigos postales piden credenciales o licencia; las SAFD y la
herramienta de consulta, no).

**Se INVESTIGA** (tres fuentes independientes, y no vale que las tres sean del mismo tipo — sirven
la UPU y el servicio postal del país, las webs de sus transportadoras, y sitios donde gente real
escribe direcciones de verdad: reseñas, foros, marketplaces locales):
- **Nomenclatura de dirección local**: qué campos la componen, en qué orden, cómo se abrevian, y
  si hay código postal y es obligatorio.
- **Cómo la gente EXPLICA cómo llegar** — las referencias visuales y de trayecto. Es el corazón
  del pack: lo que decide si una dirección es entregable o el mensajero va a tener que llamar.
- **Transportadoras que operan** en el país y cuáles hacen contra entrega (no todas).
- **Registro de cortesía local** (usted/tú, muletillas de servicio).
- **Reglas de vivienda colectiva, rural y recogida en oficina** equivalentes.

**Se PREGUNTA solo lo que vive en la cabeza del dueño**: cuáles de esas transportadoras tiene él
contratadas y cuáles no quiere usar.

**Lo que no se logre confirmar se marca NO VERIFICADO** y SOLO entonces se le confirma al negocio,
diciéndole por qué se le pregunta. Nada se inventa: una jerga inventada suena falsa en el primer
mensaje y la gente lo nota.
Mantén SIEMPRE el contrato de salida de una sola línea y el principio rector. Guarda el nuevo pack en `references/<pais>.md` para reutilizarlo.

## Recibir un PACK PROPUESTO (del padre o de una corrida anterior)

`golden-chatea-pro-config-logistico` investiga el país cuando no hay pack y **entrega aquí un pack
propuesto con sus fuentes**. Su texto lo dice: *"se propone, no se escribe solo: quien adopta un
pack es la skill dueña"* — la dueña es esta. Hasta el 2026-09-07 esta skill **no tenía dónde
recibirlo**, así que la investigación se hacía y se perdía, y el siguiente negocio del mismo país
obligaba a repetirla entera. **Un hueco que no se cierra deja de ser un hueco y se vuelve una
costumbre.**

**Qué se exige antes de adoptar un pack propuesto:**
1. **Sus fuentes**, las tres, y que no sean del mismo tipo.
2. **Lo NO VERIFICADO marcado como tal**, no rellenado.
3. **El criterio del código postal decidido POR ESE PAÍS**, nunca heredado (es la trampa que ya
   mordió: México heredó de Colombia un "nunca exijas código postal" que en México es falso).
4. **Cero datos de negocio dentro**: el pack es del país, no del cliente que lo motivó.

Con eso, se guarda como `references/<pais>.md` con la misma estructura que `colombia.md`, y se
anota en el flujo de arriba. Si le falta alguno de los cuatro puntos, **se adopta lo que sirva y
se declara qué quedó pendiente** — no se rechaza el trabajo entero ni se guarda a medias sin decirlo.

## Reglas de oro
- **Nunca inventes transportadoras ni datos del negocio:** se preguntan/confirman por país y por tienda.
- **No pidas de más:** si la dirección ya trae puerta, apto, torre, bloque, barrio claro o referencia fuerte, es válida. Solo pide ante duda operativa real.
- **Una sola línea de salida, siempre.** El bot ya saludó; este prompt no saluda ni explica.

## Cupo de la API (te afecta al ENTREGAR, no al generar)

🔴 **La API de Chatea limita a 1.000 peticiones por HORA y pasarse BLOQUEA una hora entera.** Cada
respuesta trae **`x-ratelimit-remaining`** (en inglés *X-RateLimit-Remaining*). Se repone cada hora,
pero **no viene `x-ratelimit-reset`**: el servidor no dice a qué minuto empezó la ventana, así que
se **mira** el contador con `golden-chatea-cupo`, no se calcula.

**Aquí no toca la red:** esta skill produce **texto** —el prompt de validación— y no escribe nada.
El cupo entra cuando ese prompt **se pega o se escribe** en el campo del asistente logístico. Es
barato (una escritura más su relectura obligatoria), pero **se suma** al de la instalación completa
si el padre está montando los cuatro asistentes seguidos.

## Fábrica

Fábrica: chat ✅ SKILL golden-chatea-pro-validacion-direcciones — este chat es su casa: aquí se
audita, se mejora y se sella, y nadie más la edita. Hasta el 2026-09-08 la fábrica era el Centro
de Mando. La fábrica **EJECUTA, no manda**: la autoridad es FER → Centro de Mando → skill, y lo
que llega aquí es FILA (turno de escritura), no permiso. Todo cambio se informa al CdM, que
reparte.

## Conexiones
- 📦 Padre (config del asistente logístico) → `golden-chatea-pro-config-logistico`
- 🛒 Asistente de ventas (dispara el logístico al pedir la dirección) → `golden-chatea-pro-config-ventas-wp`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## 🔴 Sincronización multi-agente (verificado en vivo 2026-09-22)

**Esta skill vive en más de una copia, y las copias NO se editan entre sí.** Antes de dar por
buena una corrida, o antes de tocar esta skill desde otro chat, conviene saber cuál copia es cuál
— confundirlas hizo perder una tarde entera reconstruyendo el mapa.

| Copia | Ruta | Rol | Estado medido 2026-09-22 |
|---|---|---|---|
| **Canónica** | `~/.claude/skills/golden-chatea-pro-validacion-direcciones` | La que este chat edita. Fuente de verdad. | v2.11 |
| **Publicada** | GitHub `Comunidad-Golden/skill-golden-chatea-pro-validacion-direcciones` | Lo que instalan los alumnos vía marketplace. Se sube SOLA: `com.golden.skills-sync` (launchd, `StartInterval` 900 = cada 15 min) empuja cualquier cambio de la canónica. | v2.11 en la corrida verificada — pero **el push tarda hasta 15 min**: una verificación adversarial midió esta misma fila "sincronizada" mientras el HEAD del repo aún era la versión anterior, y el launchd la alcanzó 7 minutos después, en plena auditoría. No declarar "publicado" sin comparar el HEAD real (`git log -1`) en el momento, no de memoria. |
| **Espejo Codex** | `~/.agents/skills/golden-chatea-pro-validacion-direcciones` | Mismo contenido, con las rutas internas reescritas a `~/.Codex/skills/…` para que el otro agente (Codex, de OpenAI) la lea con sus propias rutas. Se actualiza por un mecanismo fuera de esta skill — **no se edita a mano: un espejo generado se pisa sin avisar.** | v2.10, un paso por detrás. 🔴 **La reescritura de rutas apunta a un directorio que NO EXISTE**: `~/.Codex/skills/` solo contiene `.system` — los 6 comandos ejecutables que trae el espejo (validar_pack.py, --autoprueba, --casos, agentskills validate, validar_arsenal.py, verificar_pais_no_es_puerta.sh) fallan con "no existe el archivo" si Codex los corre tal cual. Hallado por verificación adversarial 2026-09-22; no lo arreglo aquí porque el espejo es generado y no es mío, pero quede dicho: el propósito de la reescritura no está logrado, solo declarado. Y el diff con la canónica no es solo el prefijo `references/` de la v2.11: `changelog.md` difiere además en 40 líneas (las actas de v2.10 y v2.11, que este espejo nunca recibió). |
| 🔴 **Plugin ya instalado** | `~/.claude/plugins/synced/…/golden-chatea-pro-validacion-direcciones` (y cualquier instalación equivalente en la máquina de un alumno) | La copia que un Claude Code se trajo la última vez que alguien instaló o actualizó el plugin. | **v2.4 (26-ago) — medida en esta misma máquina.** No se refresca sola cuando el repo cambia: quien instaló antes del 08-sep sigue generando prompts sin el tope de 8.000, sin los 23 países, con el país tratado como puerta. Nada en este repo avisa de que hay una versión nueva. |
| 🔴 **Resto muerto/duplicado** | `SKILLS-COMUNIDAD/golden-chatea-pro-validacion-direcciones` (carpeta de trabajo, no instalación activa) | Sin dueño claro: sin `scripts/`, con una carpeta `references 2` (firma de duplicado de iCloud sin resolver). | v2.4, 8 packs. Hallada por verificación adversarial 2026-09-22 — esta tabla decía "cuatro filas" y hay cinco. No se tocó: decidir si se borra o se actualiza es de quien mantenga esa carpeta. |

**Qué se sigue de las filas de arriba:** un alumno con el plugin instalado antes del 2026-09-08 no
se entera de ninguna mejora posterior a menos que reinstale o actualice el plugin a mano. Esta
skill no tiene forma de avisarle — el aviso, si se decide dar, es trabajo de quien administra la
comunidad (recordatorio de actualización, o un mecanismo de versión en el propio marketplace), no
de este archivo. Reportado al Centro de Mando el 2026-09-22 para que lo reparta.

**Antes de declarar un cambio "publicado" o "ya lo tienen los alumnos"**, la pregunta no es "¿lo
subí?" sino "¿cuántas de las cinco filas de arriba lo tienen, medidas ahora mismo?" — subir a
GitHub no actualiza el plugin ya instalado de nadie, y el propio push puede tardar hasta 15
minutos: "lo subí" y "está publicado" no son el mismo instante.

## Privacidad (skill compartible)
Los packs de país traen lógica y ejemplos genéricos. Nunca hornees datos de un negocio real (transportadoras contratadas, tienda, cuentas). Se preguntan en cada uso.

## Fronteras y desambiguacion

Para la CONFIG general del asistente logístico (transportadoras, tiempos, recogida en oficina) usa el padre golden-chatea-pro-config-logistico.

## Herramientas de esta skill (córrelas, no las supongas)

```bash
python3 ~/.claude/skills/golden-chatea-pro-validacion-direcciones/scripts/validar_pack.py
python3 ~/.claude/skills/golden-chatea-pro-validacion-direcciones/scripts/validar_pack.py --autoprueba
python3 ~/.claude/skills/golden-chatea-pro-validacion-direcciones/scripts/validar_pack.py --casos
```

- **Sin argumentos** recorre los 23 packs y da COBERTURA (N de N), no veredicto. Mide cada pack
  contra los 8.000 del campo y contra el bot field escapado, y **compara su criterio de código
  postal contra `references/limites.json`** — que es el dato duro, no la prosa. Ese cotejo es lo
  que mata la clase de defecto que ya mordió dos veces a esta familia.
- **`--autoprueba`** lo corre contra 9 casos que se SABEN malos (CP negado, CP negado con
  paráfrasis que la lista quemada no cazaba, CP exigido donde no se usa, pack mudo sobre el CP,
  señal positiva traducida, señal con emoji pegado, prompt por encima del tope, clave `sk_live_`
  y correo dentro del pack) más un control en sentido inverso que comprueba que un pack correcto
  no da falso positivo. **Si tu validador aprueba todo a la primera, sospecha del validador**:
  esto es lo que lo desmiente. Cazó 10 de 10 el 2026-09-22 (número leído en vivo, no quemado —
  esta línea decía "cuatro casos… cazó 5 de 5" tras la ronda del 08-sep y sobrevivió a que el
  banco creciera a 9+1; hallado por verificación adversarial: es la MISMA clase que la v2.10
  corrigió en §Operación y dejó viva 25 líneas más abajo, en esta misma sección).
- **`--casos`** corre el banco de `references/casos.json`: 33 direcciones trampa reales, con **al
  menos un caso por cada uno de los 23 países** (el "200 metros norte" tico sin punto de partida,
  el orden inverso húngaro, la dirección búlgara sin calle, la quinta venezolana que se identifica
  por nombre) y comprueba que la regla que resuelve cada una está ESCRITA en su pack. Hasta el
  2026-09-22 cubría 16 de 23 — siete países no tenían ni un caso y por eso nunca podían bajar del
  100%; corregido tras verificación adversarial. Probado quitándole una regla real a un pack en
  copia: el banco lo cazó.

**Al tocar cualquier pack, los tres se corren otra vez.** Un pack que crece 300 caracteres es
justo el que se pasa de 8.000, y el corte no avisa.

## Operación de esta skill

Comprobar que está en norma. **Ruta ABSOLUTA siempre: con `.` da fallo falso.**
```bash
agentskills validate ~/.claude/skills/golden-chatea-pro-validacion-direcciones
python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py ~/.claude/skills/golden-chatea-pro-validacion-direcciones
```
Salida 0 = en norma. Se corre **DESPUÉS** de tocar la `description`, no solo antes.

🔴 **Y el guardarraíl de DOCTRINA, que en esta skill vale tanto como el validador porque aquí
no hay código: el comportamiento ES el texto.**
```bash
bash ~/.claude/skills/golden-chatea-pro-validacion-direcciones/scripts/verificar_pais_no_es_puerta.sh
```
8 de 8. Comprueba en los dos sentidos que **el país sigue siendo parámetro y no puerta**: que la
doctrina afirmativa esté escrita, que ninguna orden de rechazo aparezca en texto vivo, y que los 23
packs declarados en `references/limites.json` existan (número leído en vivo, no quemado — hasta el
2026-09-08 este guardarraíl decía "8" a mano y siguió diciendo 8 el día que la skill pasó a 23).
Trae contraprueba que repone la puerta a propósito para verlo morder.
**Córrelo siempre que toques el texto del país o el flujo de país nuevo** — hasta la v2.5 esta
skill llevaba DOS puertas en prosa, y una frase mal puesta aquí vale lo mismo que un `sys.exit`
en una hermana.
Los dos techos NO son el mismo: **1024 VALIDA (duro) · ~1536 TRUNCA en runtime.**

Blindaje. `chflags uchg` y `chmod` conviven en el mismo árbol y **el orden importa**:
- abrir: `chflags nouchg <ruta>` **primero**, luego `chmod 644`
- cerrar: `chmod 444` **primero**, luego `chflags uchg`
- el **directorio** lleva su propio `uchg` + `555`, y hay que abrirlo para crear ficheros

Al revés, el `chmod` choca contra el flag ya puesto y la skill queda de solo lectura pero
borrable.

Antes de publicar, **el repo de skills es PÚBLICO**: `~/.golden/bin/golden-barrido-publicacion ~/.claude/skills/golden-chatea-pro-validacion-direcciones`

Historial completo en `references/changelog.md`.
