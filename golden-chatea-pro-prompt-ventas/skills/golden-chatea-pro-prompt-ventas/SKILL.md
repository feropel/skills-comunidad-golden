---
name: golden-chatea-pro-prompt-ventas
description: Crea el paquete completo de venta para un asistente de WhatsApp en Chatea PRO v2 — saludo inicial, plan de multimedia, pregunta de entrada, prompt de venta, recordatorios y remarketing — Y TAMBIÉN MEJORA prompts que el usuario ya tenga (los evalúa /100 y /1000, marca lo crítico y los reconstruye a nivel superior). Úsalo SIEMPRE que el usuario quiera crear, armar, optimizar, auditar o MEJORAR un prompt de ventas para Chatea PRO, un asistente/bot de ventas por WhatsApp, un agente conversacional de venta, venta por WhatsApp contra entrega o pago anticipado, o diga cosas como "hazme el prompt de [producto]", "necesito un agente de ventas para WhatsApp", "arma el asistente de Chatea PRO", "optimiza este prompt de venta", "ya tengo un prompt, mejóralo", "revisa el prompt de mi bot", "este prompt no me vende", "configura la venta conversacional" — o cuando PEGUE un prompt de ventas existente (suyo, de un mentor o de otra herramienta) pidiendo opinión o mejora. Aplica a cualquier producto (cosméticos, salud, ropa, suplementos, accesorios), cualquier país y cualquier modelo de pago. Si dudas, dispáralo, porque un prompt sin esta estructura convierte menos.
---

# Constructor de Prompts de Venta para Chatea PRO v2

<!-- skill v3.14.1 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08 (2ª ronda: 5ª categoría + prosa libre)) · QUINTA CATEGORÍA VETADA en la ley: claims y cifras de negocio (años en el mercado, clientes atendidos, porcentajes de entrega, premios) — no rompen nada técnico ni los caza un barrido de llaves, pero el bot termina mintiendo con datos de otra empresa (caso real: "Más de 100.000 clientes atendidos en Colombia" a punto de heredarse). Y regla operativa LA MARCA VIVE TAMBIÉN EN PROSA LIBRE: al barrido se añade grep -i por el nombre de la marca origen sobre todo el texto a escribir (cazó 10 menciones en 3 campos que el mapeo de llaves no vio). -->
<!-- skill v3.14 · 2026-08-08 (centro de mando, chat otro espacio de Chatea 2026-08-08) · horneada la LEY "NUNCA HEREDAR DATOS ENTRE ESPACIOS": al basarse en una cuenta guía se hereda estructura/prompts/config, JAMÁS datos (APIs, plantillas de WhatsApp, teléfonos, correos, dominios, marca, productos y disparadores); única excepción Le'côterra como producto-ejemplo; método de barrido obligatorio antes y después de escribir en espacio ajeno. Origen: incidente Golden → otra marca 2026-08-08 (se colaron una credencial, teléfono, plantilla de notificación y firmas de la marca origen; revertido el mismo día). La ley entra como PREVENCIÓN, no reparación: línea base pre-horneado verificada por verificador externo — 8/8 skills sin credenciales (CRITICA=0); únicos hallazgos 3 teléfonos de relleno legítimos (+57 300 de ejemplo) que se conservan. ADEMÁS (chat otro espacio de Chatea 2026-08-08, retractación pixel): regla CAMPOS [Meta] = VALORES CALIENTES — los eventos de pixel los mueve el flujo en vivo, prohibido diagnosticar con una lectura suelta. -->
<!-- skill v3.13.2 · 2026-08-07 · TERCERA RONDA del verificador: el activador pasa de lista-de-emojis a LISTA PERMITIDA (whitelist: letras, números y puntuación básica) — cierra la CLASE entera (caza ‼ ⁉ ℹ keycaps ㊗ que el rango manual dejaba pasar) y elimina el falso positivo de ≤ → en prompts (el contador 3B por rango se retiró del modo prompt); checklist del prompt ya NO se imprime en modo activador; doc corregida en los 3 sitios que enseñaban la fórmula de 4 bytes como "la validación" (es parcial: el script es la validación); id de workspace de tercero retirado del changelog. DECISIÓN DELIBERADA: las marcas propias de la casa en changelogs históricos (productos públicos de la tienda) se conservan como trazabilidad de lecciones de campo; no son datos de terceros. ABIERTO (requiere plataforma viva): probar si la base tolera emojis de 3 bytes en el trigger, y los pares 19.895/23.266 con escritura+relectura en un producto desechable -->
<!-- skill v3.13.1 · 2026-08-07 · SEGUNDA RONDA del verificador adversarial (9/11 resistían, cazó huecos nuevos): validar.sh ahora también bloquea EMOJIS DE 3 BYTES en el activador (✨⛔✅❤☕⭐ pasaban el filtro de 4 bytes — la regla es SIN emojis, no solo sin 4B), BOM invisible (rompe el match del trigger; utf-8-sig detectado y bloqueado en activador), archivo de solo-espacios, y argumentos inválidos con mensaje de uso. DOC SINCRONIZADA con el script real: eliminadas las 3 menciones a wc -m que autorizaban el método defectuoso, modo --activador ahora descubrible en PASO 7 + VALIDADOR + estructura-disparo + guía. ejemplo-completo: encabezado y RM2 alineados a envío prioritario, upsell con totales explícitos. Packs PA/PY completados (transportadoras default + vocabulario, sin inventar operadores). Privacidad: economía real y ruta de disco retiradas de referencia-externa; ledger des-marcado. NOTA ABIERTA: si la base de Chatea tolera o no emojis de 3 bytes en el trigger NO está probado contra la plataforma (la hermana usa el mismo filtro de 4B); el default seguro es 0 emojis de cualquier tipo -->
<!-- skill v3.13 · 2026-08-07 · REPARACIÓN TRAS golden-verificador (11 clases de fallo cazadas): validar.sh REESCRITO — ahora BLOQUEA (exit!=0) en vez de imprimir: conteo por python (wc -m contaba BYTES bajo locale C, +22% fantasma), techo escapado ENFORCED <19.000 con la fórmula del briefing (ensure_ascii default), archivo vacío=fallo, no-UTF8=fallo con aviso (antes degradaba en silencio), modo --activador que exige 0 caracteres de 4 bytes, rúbrica-suma eliminada del script (quedaba viva contra la norma holística), default 12.000 alineado. "Garantía Golden" DESMARCADA de la plantilla (viajaba al bot de terceros). guia-configuracion-chatea.md actualizada a la NORMA DE DOS ACTIVADORES + validación 4 bytes (se había quedado en la norma vieja: clase de fallo "changelog que no enumeró todos los archivos"). ejemplo-completo.md alineado (saludo sin pregunta, multimedia sin pregunta, envío nunca cobrado, tiempos 3-5, dos activadores). Guardas de país en OFICINA (México no existe) en plantilla/objeciones/compuerta. Intake 18 = garantía de CAMBIO. Tope recordatorio 800 añadido. Matiz LONG JSON 500k vs legacy 20k. Lecciones de campo des-marcadas (otra marca → lección de campo). SKILL.md refs = 7 países -->
<!-- skill v3.12 · 2026-08-07 (tarea Centro de Mando aprobada por FER, briefing CHATEA-PRO-ASISTENTES-MAPA/BRIEFING-PARA-SKILLS.md leído completo) · (1) TOPES NATIVOS confirmados y completados: prompt_libre 12.000 ✓ + vecinos que faltaban (mensaje inicial 1.000, pregunta de entrada 1.000, instrucción remarketing 1.000 c/u, prompt_datos 4.000, notificaciones 400; escribir por API sobre el tope no falla pero el panel CORTA al guardar); tabla completa en TOPES-NATIVOS-POR-CAMPO.md. (2) SEGUNDO TECHO: el bot field guarda ESCAPADO (tilde=6, emoji=12) → 20.000 escapados ≈ ~17.000 crudos; probado 19.895 dispara / 23.266 muere SIN error; medir len(json.dumps(v)[1:-1])<19.000 — validar.sh ahora lo calcula + cuenta 4-bytes. (3) PAÍSES: solo los 7 de la plataforma (COLOMBIA/ECUADOR/CHILE/MEXICO/PANAMA/PERU/PARAGUAY); Guatemala ELIMINADO de paises.md; packs Panamá y Paraguay añadidos; México enriquecido (CP REQUERIDO define zona de reparto, NO existe oficina, zonificación metropolitana/interior/alejadas, PROFECO, vocabulario paquetería/pedido/dinero/repartidor). (4) Trigger: fórmula dura de validación 4 bytes en estructura-disparo §6. (5) "DOMICILIO": en CO es el pedido, en MX es la casa — vocabulario por país en paises.md. Referencia viva: prompt Le'côterra 11.985/12.000 verificado por SHA256 contra el workspace plantilla externo (id en la memoria del ecosistema, no aquí) -->
<!-- skill v3.11 · 2026-08-07 (centro de mando, cosecha del chat un estudio de producto) · (1) NORMA DE DOS ACTIVADORES por producto, APROBADA por el Centro de Mando: frase completa del botón (canales con mensaje precargado) + UNA palabra corta ÚNICA del producto (TikTok/estados/comentarios donde nadie precarga; ej. estilo SONRISA/HONGOS), verificada contra TODAS las demás del bot para no cruzarse y JAMÁS genérica ("información"/"precio"); actualizados el paso 7 del SKILL.md y estructura-disparo.md §6. Misma familia del bug Libido UP ("escribe RITUAL" y el activador era otro). (2) Bloque "LÍMITE ÉTICO Y LEGAL" obligatorio dentro del prompt para verticales de SALUD (plantilla-prompt.md + cumplimiento.md): qué jamás afirma el bot + respuesta honesta ya redactada a la pregunta crítica ("me tapa la caries?" → "No. Si ya hay un hoyo, eso lo repara el dentista; esto cuida el esmalte"); evita devolución COD y reclamo, y en salud vende más que prometer. -->
<!-- skill v3.10 · 2026-08-07 · INTAKE APROBADO POR FER ítem por ítem: País/Producto/Precio/Asesor SÍ · Pago gate SÍ con datos COMPLETOS si anticipado (titular + banco/entidad + número/llave + TIPO de cuenta) · ENTREGA NO SE PREGUNTA (tiempos y transportadora = default por país en paises.md, mostrados como supuesto en el borrador, solo cambian si el vendedor corrige solo) · "Confianza" renombrada "Para cerrar mejor" (opcional, no bloquea) · URL de tienda marcada opcional (solo si tiene tienda). Formulario, PASO 1 y paises.md sincronizados -->
<!-- skill v3.9.1 · 2026-08-07 · pasada golden-skill-auditor: referencia-externa-embudo-whatsapp-cod.md registrada en Archivos de referencia (era huérfana: existía desde 2026-07-30 —masterclass COD de terceros, OPCIONAL no-regla, backup en _backups/2026-07-30-masterclass-panama— pero nada la mencionaba y ningún Claude la leería); CHANGELOG.md suelto fusionado aquí y eliminado (estándar: changelog en comentarios del SKILL.md; era material intruso de cara al marketplace) -->
<!-- skill v3.9 · 2026-08-01 (centro de mando) · La verificación de v3.8 (title vacío) solo cazaba 1 de 3 modos de fallo: Temu falla con title POBLADO (redirige y devuelve 72 categorias de ropa) y Amazon con title poblado Y sin redireccion (muro anti-bot, sin campo json). Ahora son 4 checks, y el que caza los tres es "el dato responde a lo que pedi?". Aqui el riesgo es el mas directo del ecosistema: el dato falso se lo dice el BOT AL CLIENTE en WhatsApp -->
<!-- skill v3.8 · 2026-07-31 (centro de mando) · SCRAPING QUE MIENTE: firecrawl_scrape con formats:["json"] sobre una página que no carga NO falla — el extractor ALUCINA producto, precio y reseñas y los entrega con statusCode 200 (medido 2026-07-31: devolvió "Smart TV 55\" 4K LED, $499.99, 150 reseñas" para una página de removedor de verrugas). Aquí es especialmente grave: un precio o un "4.5 estrellas" falso se lo dice el BOT AL CLIENTE REAL por WhatsApp. Verificación obligatoria: metadata.title no vacío, o pedirle los datos al vendedor. Manual: golden-investigacion-mercado/references/scraping-firecrawl.md -->
<!-- skill v3.7 · 2026-07-29 (centro de mando) · GARANTÍA: la plantilla enseñaba 'te devolvemos tu dinero' → corregida a garantía de CAMBIO; orden de FER: la política de Shopify manda, nunca devolución de dinero en ninguna pieza. -->
<!-- skill v3.6 · 2026-07-27 (centro de mando) · activador SIN EMOJI EN NINGUNA PARTE (no solo al final): los emojis son 4 bytes y la base de Chatea los convierte en `�` → el trigger nunca coincide (incidente real 2026-07-26 con el 👋 inicial); ejemplos de trigger corregidos en SKILL.md + 3 references. Fuente de verdad de triggers vivos: memoria reference_botones_whatsapp_golden. v3.5.1 · 2026-07-25 · sin emoji al final. Detalle en estructura-disparo.md §6 -->
<!-- skill v3.5 · 2026-07-14 · Chatea DESHABILITÓ el módulo Upsells del asistente de Ventas WhatsApp (verificado en vivo: sección gris) → VARIANTE B (upsell DENTRO del prompt, pitch del bot) pasa a ser la POR DEFECTO; variante A queda condicionada a verificar el módulo en la UI. Variante B endurecida: totales post-cierre con números explícitos, un solo mensaje, un solo intento -->
<!-- skill v3.4.1 · 2026-07-13 · 4º test de campo: REGLA DEL NÚMERO QUE MANDAN (el cliente escribió su celular y el bot respondió "Lo siento, no lo necesito" — cortante); ahora se agradece con calidez y se avanza, jamás rechazo seco. Lección: nunca hacer sentir mal al cliente por dar un dato de más -->
<!-- skill v3.4 · 2026-07-13 · 3er test de campo: VALIDACIÓN reescrita como COMPUERTA DEL RESUMEN (si falla un punto, el resumen NO existe; como texto suelto el bot la ignoraba: imprimió "[tu referencia]" y aceptó dirección sin nomenclatura) + REGLA DE PLANTILLA endurecida (dato ausente → volver a la compuerta, jamás rellenar). Lección de arquitectura: toda regla crítica se enuncia como COMPUERTA con condición-bloqueo, no como recomendación -->
<!-- skill v3.3.1 · 2026-07-13 · 2º test de campo (5 bugs cazados en vivo): REGLA DE PLANTILLA anti-corchetes (el bot imprimía placeholders literales), WhatsApp = texto fijo "el de este chat", Dirección = UNA sola opción (no "dir / OFICINA"), referencia obligatoria + nomenclatura de dirección completa antes del resumen, entrega PERSONALIZADA por ciudad (jamás recitar las 3 franjas), y fallback de upsell si las tarjetas nativas no disparan + totales post-cierre con ejemplos numéricos -->
<!-- skill v3.3 · 2026-07-12 · horneada tras TEST DE CAMPO real (fibra capilar CO) + teardown de prompt ganador (otra marca): plantilla con REGLA DE INTENCIÓN DE COMPRA + CLIENTE DIRECTO + MEMORIA DEL PEDIDO + bloque IMÁGENES/URLS obligatorio (apaga el fallback documentado de Chatea que reenvía la multimedia inicial) + única confirmación (resumen+SÍ) + captura solo-campos-faltantes + validación sin (Pendiente)/barrio≠ciudad + REGLA DE ENTRADA A-G + PASO 8 en 2 variantes (upsells nativos con precio fijo post-cierre y copy de tarjetas / pitch del bot) + LÓGICA DE COMBOS con frontera del cierre + save-the-sale + filtro de efectividad COD + personalización con nombre + objeción revisar-paquete = política del negocio (intake ítem 10) + intake pregunta si upsells nativos activos (ítem 6) -->
<!-- skill v3.2.1 · auditada golden-skill-auditor 2026-07-10 (1000 ORO): entrega-pdf.md DELEGA en golden-pdf-check (no rutas de script locales, cero refs rotas) + rango de workflow aclarado (PASO 0→4, distinto de los PASO 1–8 del flujo conversacional) + obligatorio = "1 unidad o combo" (consistente con combos por cantidad) -->
<!-- skill v3.2 · intake por FORMULARIO de una vez (más rápido, no cansa; país 1º, obligatorio vs opcional, relleno inteligente) + combos POR CANTIDAD/docena con variantes mezclables (upsell por combo, campo de sabores que suma la cantidad) + entregable PDF con golden-pdf-check (prompt en tarjetas atómicas que van SEGUIDAS en el mismo campo) + recetario de prompts de imagen (set hero/grilla/prueba social/headers + video pull) -->
<!-- skill v3.2 · Modo MEJORA como servicio completo: dispara con "ya tengo un prompt, mejóralo" (description ampliado), extrae datos del prompt viejo sin hacer repetir al usuario, reconstruye POR DEFECTO y entrega comparación nota vieja vs nueva -->
<!-- v3.1 · auditada con golden-skill-auditor: modo auditoría alineado a evaluación holística (/100 + /1000), residuos de la rúbrica de pesos eliminados -->
<!-- v3.0 · validador + medición/ledger + objeciones + packs por país + cumplimiento + ejemplo horneado + intake conversacional + plantilla Meta remarketing + conexiones/privacidad -->

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
otra vez. Herramienta encadenable del barrido:
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

### CAMPOS [Meta] = VALORES CALIENTES, NO INTERRUPTORES

Los bot fields `[Meta] Ver Contenido`, `[Meta] Agregar al carrito` y demás eventos de pixel los
**MUEVE EL FLUJO en tiempo real** mientras corren contactos — no son configuración estable. Caso
real (2026-08-08): se leyeron como "apagados" y cambiaron solos minutos después sin escritura de
nadie; la conclusión "el evento Comprar está apagado" tuvo que retractarse. **PROHIBIDO sacar
conclusiones de pauta o diagnóstico de una lectura suelta de esos campos**: se observan en ventana
(varias lecturas separadas en el tiempo) o se diagnostica el pixel en Meta directamente. Detalle:
memoria `reference_chatea_clonar_config_entre_espacios`.


Este skill convierte cualquier producto en un paquete de venta completo y listo para pegar en Chatea PRO v2, siguiendo una estructura probada en campo (referencias con 50+ ventas/día). El objetivo siempre es el mismo: **convertir conversaciones de WhatsApp en ventas confirmadas.**

## Flujo de Chatea PRO v2 (contexto obligatorio)

El asistente se dispara así:
```
palabra clave → SALUDO INICIAL → MULTIMEDIA → PREGUNTA DE ENTRADA → (cliente responde) → se activa el PROMPT
```
Todo lo que diseñes debe encajar en esa secuencia. Además existen RECORDATORIOS (dentro de la ventana de 24h) y REMARKETING (plantillas que reabren la conversación después de horas).

## DOS MODOS DE USO

**Modo CONSTRUCCIÓN (por defecto):** el usuario quiere un prompt nuevo. Sigue PASO 0 → 4 (0 intake · 1 entrevista · 2 construir · 2.5 PDF · 3 y 3.1 auto-evaluación · 4 medición). Nota: los "PASO 1–8" que verás en `plantilla-prompt.md` son los pasos del FLUJO CONVERSACIONAL dentro del prompt, no los de este workflow.

**Modo MEJORA (auditar + reconstruir):** el usuario YA TIENE un prompt (suyo, de un mentor, de otra herramienta, "el viejo") y lo pega pidiendo opinión, auditoría o mejora. Este modo es un servicio completo — no solo calificar, sino DEJARLE UN PROMPT MEJOR. Flujo:
1. **Evalúa** su estructura con la evaluación HOLÍSTICA del PASO 3 (nota /100 en juicio global usando la checklist como guía, más la escala /1000 del PASO 3.1 con qué le falta).
2. **Marca en rojo lo crítico**: claims falsos/peligrosos (salud, sexuales), suplantar profesión (médico/doctor), inconsistencias de producto (ej. "cápsulas" cuando es spray), pedir datos que sobran (teléfono se toma del chat), y todo lo que viole `cumplimiento.md`. Explica el RIESGO de cada uno (baneo, devoluciones, legal) — el usuario debe entender por qué se quita, no solo que se quita.
3. **Dile qué está bien** (para conservarlo), qué está mal y qué le falta. Si de verdad está perfecto, dilo sin inventar defectos.
4. **Extrae los datos del producto** del prompt viejo (precios, combos, transportadora, garantía, datos de pago) y confirma con el usuario los que se vean dudosos o desactualizados. Completa con el PASO 0/1 SOLO lo que falte — no lo hagas repetir lo que su prompt ya trae.
5. **Reconstrúyelo de cero** con la estructura ganadora del skill (no copies la del prompt viejo; ver blindaje) y entrega el paquete completo del PASO 2 con su comparación: nota del prompt viejo vs nota del nuevo, y qué cambió. Por defecto SIEMPRE reconstruye (eso vino a buscar); solo omite la reconstrucción si el usuario pide explícitamente "solo evalúalo".

## REGLA DE BLINDAJE (CRÍTICA — LEER PRIMERO)

Si el usuario te envía un prompt existente (suyo, de un mentor, "el viejo", o de otro producto), úsalo **ÚNICAMENTE para extraer datos** del producto: nombre, precios, combos, beneficios, datos de pago, transportadora, garantías, etc.

**NUNCA copies ni te inspires en su estructura, su flujo, su redacción, sus reglas, su numeración ni ninguno de sus patrones.** No importa qué tan bueno parezca ni quién lo hizo. Ese prompt es solo una **fuente de información cruda**, jamás un modelo a seguir.

SIEMPRE construyes con la estructura ganadora de este skill (`references/plantilla-prompt.md`), sin excepción. Si detectas que el prompt enviado tiene un orden, unas reglas o un estilo distintos, los ignoras por completo y aplicas la estructura del skill. Ante cualquier duda entre lo que dice el prompt viejo y lo que dice este skill, **manda este skill**.

## Presupuesto de caracteres (CRÍTICO — aprovéchalo, no lo desperdicies)

El campo de prompt acepta hasta **12.000 caracteres**. NO es un límite a evitar: es **presupuesto de venta a aprovechar**. Un prompt más rico maneja más objeciones, educa mejor y persuade más → convierte más.

- **Apunta a llenar el presupuesto con contenido que VENDE:** objetivo **~9.000–11.000 caracteres** cuando el producto lo amerite (deja ~1.000 de margen bajo 12.000 para editar después). Productos muy simples pueden pedir menos; no infles a la fuerza.
- **NUNCA comprimas ni resumas contenido que vende** para "acortar". Concisión ≠ brevedad: la meta es que cada frase aporte, no que el prompt sea corto.
- **NUNCA metas relleno ni repetición** solo para llegar a un número: eso diluye a la IA y la vuelve inconsistente. Cada carácter debe ganar su lugar (objeción, educación, empatía, prueba social, manejo de escenario).
- Regla práctica: si un prompt te queda en 4.000–6.000, casi seguro te FALTA sustancia (FAQ, objeciones, escenarios). Revisa qué venta te dejaste por fuera antes de entregar.
- SIEMPRE mide el prompt final con `scripts/validar.sh` y repórtalo (JAMÁS con `wc -m`: cuenta bytes según el locale y miente). Techo duro del campo: 12.000.
- **EL SEGUNDO TECHO (el que mata en silencio): el bot field guarda el valor ESCAPADO.** El campo JSON aguanta 20.000 caracteres ESCAPADOS, no crudos: cada tilde ocupa 6 y cada emoji 12, así que el techo práctico ronda ~17.000 crudos para el bot field completo (probado en vivo: 16.882 crudo/19.895 escapado dispara; 19.922/23.266 NO — y el producto muere sin error visible, el fallo solo sale en Panel → Registros de errores). Un prompt de 11.000 lleno de tildes y emojis puede reventar el campo aunque quepa en 12.000. Mide el escapado con `len(json.dumps(valor)[1:-1])` y déjalo bajo 19.000 (validar.sh lo calcula). MATIZ del techo escapado: el tope de 20.000 escapados aplica a los bot fields legacy tipo JSON; los campos LONG JSON aguantan 500.000 (todo campo NUEVO se crea LONG JSON) — pero el tope NATIVO del formulario (12.000 el prompt) rige igual porque el panel corta al guardar. Tabla completa de topes por campo: `CHATEA-PRO-ASISTENTES-MAPA/TOPES-NATIVOS-POR-CAMPO.md` (referencia interna del ecosistema Golden; los topes operativos ya están reproducidos aquí).
- **Topes de los campos vecinos** (no solo el prompt): mensaje inicial (saludo) 1.000 · pregunta de entrada 1.000 · instrucción de remarketing 1.000 c/u · recordatorio 800 · prompt_datos del Producto en Segundos 4.000 · notificaciones 400. Escribir por API sobre el tope no da error, pero el día que alguien abra el formulario en el panel y guarde, el campo SE CORTA.

## PASO 0 — Intake inteligente (recolecta e investiga; ver `references/intake-inteligente.md`)

Antes de construir, hazle la vida fácil al vendedor. **Intake por FORMULARIO de una vez (modo por defecto):**
- Manda **UN solo mensaje con TODAS las preguntas agrupadas y numeradas** (país primero, marcando cuáles son OBLIGATORIAS y cuáles OPCIONALES). El cliente responde de corrido lo que tenga; no lo obligues a un ida-y-vuelta pregunta por pregunta (eso cansa). Sé cálido, pero eficiente: una sola tanda.
- **Relleno inteligente:** con lo que responda, la skill DEDUCE lo que pueda (moneda/indicativo del país, tono por producto, beneficios de la URL/foto) y PROPONE defaults sensatos para lo que falte, marcándolos como supuestos. Solo REPREGUNTA si falta un **OBLIGATORIO** (precio de 1 unidad, país, producto). Todo lo demás no bloquea: se propone y se confirma en el borrador.
- Pregunta **TODO lo que mejora el prompt** (no lo mínimo): nombre del asesor, país, producto, beneficios, precios/combos, tiempos/transportadora, prueba social, garantía, confianza, etc. — pero JUNTO, en el formulario. Lo único que no se pregunta es lo condicional que no aplica o lo que ya se pudo investigar/deducir de la URL/foto.
- Alternativa **por bloques** (solo si el cliente lo prefiere o parece abrumado): 2-3 tandas por tema (1 producto · 2 precio y oferta · 3 operación y negocio). El "uno por uno" queda como último recurso, no como default.
- Aplica **el gate de pago**: "Vas a solicitar pago anticipado?" → si SÍ, pide los datos de la cuenta; si NO, no preguntes nada de anticipado.
- Acepta el producto como venga: **URL(s)** (scrapéalas), **foto** (analízala con visión) o **nada** (investiga producto y competidores en la web / Meta Ad Library). Con eso arma un borrador de ficha.
- Pregunta SOLO lo condicional que aplique (variantes solo si el producto las tiene; datos de anticipado solo si dijo que sí; imágenes según `recursos-visuales.md`).
- Confirma el borrador (precio, combos, claims) con el cliente ANTES de construir. Lo investigado acelera; el precio real y los claims SIEMPRE se confirman, nunca se inventan.

## PASO 1 — Entrevista (completa lo que falte del intake, antes de construir)

No construyas nada hasta tener estos datos. Preséntalos como el FORMULARIO de una vez del PASO 0 (todos juntos, numerados, país primero, obligatorio vs opcional). Si el usuario ya dio algunos en la conversación o en la URL/foto, no los vuelvas a preguntar: inclúyelos ya resueltos y pide solo lo que falte. Esta lista es el contenido del formulario, NO un guion de preguntas de a una.

REGLA DE DATOS POR NEGOCIO (CRÍTICA — este skill es genérico y se comparte con otras tiendas/usuarios): el **nombre del asesor/a**, los **tiempos de entrega** y los **datos de pago anticipado** son SIEMPRE específicos del negocio para el que se construye el prompt. Pregúntalos en cada caso; nunca los heredes de otro negocio ni los dejes hardcodeados en el skill. Para el pago: primero confirma si el negocio quiere cobrar **anticipado** (además de o en vez de contra entrega); si dice que sí, pídele los datos (Nequi/Daviplata/banco + titular + número + llave). Excepción: si por contexto o memoria ya conoces estos datos del **dueño de esta copia del skill**, úsalos solo para él; jamás para terceros.

**Sobre el producto:**
1. Qué producto es? (nombre, qué hace, para quién)
2. Tiene variantes/líneas? (sabores, colores, modelos). Y OJO: el combo se vende **por unidad** o **por cantidad fija** (ej. combo de 12/docena)? Si es por cantidad, esas unidades **se pueden mezclar entre variantes** o van de una sola? (ver "combos por cantidad" en `plantilla-prompt.md`).
3. Beneficios reales (qué gana el cliente, emocional + funcional)
4. Algún dato sensible? (no es medicamento, sin registro sanitario, etc.)

**Sobre precio y oferta:**
5. Precio por 1, 2 y 3 (unidades **o combos**, según cómo venda; di cuántas unidades trae cada combo). **El precio de al menos 1 (unidad o combo) es OBLIGATORIO para generar el prompt.**
6. Hay upsell post-venta? A qué precio? Y CRÍTICO: está activo el módulo Upsells NATIVO de Chatea (tarjetas automáticas con imagen y botón tras la compra)? Si SÍ, el prompt NO hace pitch propio — solo procesa las tarjetas (variante A del PASO 8 en plantilla-prompt.md); si NO, el bot hace el pitch (variante B). Verifica también que la suma de tarjetas cuadre con la tabla de combos.
7. Envío gratis? Desde qué cantidad?

**Sobre la operación:**
8. Modelo de pago: contra entrega, anticipado o ambos?
9. Si hay anticipado: datos completos de la cuenta (titular + banco/entidad + número/llave + TIPO de cuenta)
10. Si permite revisar el paquete antes de pagar (política del negocio). La TRANSPORTADORA no se pregunta: default del país (paises.md), solo se registra si el vendedor la nombra o excluye por su cuenta
11. País y nomenclatura de dirección (Colombia: barrio/ciudad/departamento · México: colonia/municipio/estado/CP · etc.)
12. ~~Tiempos de entrega~~ — NO SE PREGUNTAN (regla de FER): default por país en paises.md, mostrados como supuesto en el borrador
12b. (OPCIONAL) **ID del producto en Dropi** (solo números) y si el producto **tiene variaciones**. Son para la sección "Información del producto" y se pueden agregar después; NO son necesarios para generar el prompt.

REGLA DE OBLIGATORIOS Y NO BLOQUEO:
- **OBLIGATORIO (sin esto NO se genera el prompt):** el precio de al menos **1 (unidad o combo)**. Un agente de ventas sin precio no sirve. Los precios de 2 y 3 (unidades o combos) son deseables pero opcionales; si solo hay el de 1, trabaja con ese y arma el prompt igual. Si vende por combo de cantidad fija, di cuántas unidades trae cada combo.
- **OPCIONAL (no bloquea):** ID de Dropi, precio del campo "Información del producto" y las URLs de imágenes. Pregúntalos una vez; si el usuario no los tiene, sigue adelante y deja nota de que se agregan después.
- **URLs/imágenes:** si el usuario aún no tiene los enlaces, NO bloquees. Inserta en el prompt un **marcador claro y etiquetado** en el punto exacto donde va cada imagen, nombrando qué imagen es **según el producto**. Ejemplos: `[AQUÍ VA LA URL DE LA IMAGEN DE COLORES]`, `[AQUÍ VA LA URL DE LA IMAGEN DE MODO DE USO]`, `[AQUÍ VA LA URL DE LA IMAGEN DE ANTES/DESPUÉS]`, `[AQUÍ VA LA URL DE LA TABLA DE PRECIOS]`, `[AQUÍ VA LA URL DE TESTIMONIOS]`. Tú decides qué imagen corresponde a cada momento del flujo según el producto; el usuario solo pega el enlace cuando lo tenga.

**Sobre la marca y el tono:**
13. Nombre del asistente y personalidad (cálida, directa, etc.)
14. Prueba social real (nº de clientes, reseñas, testimonios)
15. URLs de multimedia disponibles (ver `references/checklist-multimedia.md`)
16. Tiempos deseados de recordatorios y remarketing

**Sobre confianza (clave para cerrar):**
17. El envío es discreto? (vital en productos íntimos o sensibles)
18. Hay garantía de CAMBIO? (JAMÁS devolución de dinero — regla v3.7: la política de la tienda manda)
19. Hay algún regalo o bono por la compra?
20. Es producto original (anti-réplica)?

Si el usuario no sabe alguno, propón un valor sensato y márcalo como supuesto para que lo confirme.

## PASO 2 — Construir el paquete

Genera SIEMPRE estas piezas, en este orden. Usa `references/plantilla-prompt.md` como esqueleto del prompt y `references/estructura-disparo.md` para saludo, multimedia, pregunta, recordatorios y remarketing. Aplica el pack del país del negocio (`references/paises.md`) para dirección/transportadora/pago, e inserta las objeciones que apliquen desde `references/objeciones.md`. Toma `references/ejemplo-completo.md` como vara de calidad de la salida.

1. **Saludo inicial** (cálido, con nombre del asistente, crea expectativa) — ⛔ SIN PREGUNTA. Chatea envía en secuencia automática saludo → multimedia → pregunta de entrada; el saludo NUNCA pregunta (si no, el cliente responde antes de la multimedia y luego se le vuelve a preguntar). La única pregunta que espera respuesta es la pregunta de entrada.
2. **Plan de multimedia** (qué piezas y qué texto en cada una)
3. **Pregunta de entrada** (segmenta al cliente en los caminos que el prompt sabe responder)
4. **Prompt completo** (estructura ganadora, bajo el límite de caracteres)
5. **Recordatorio 1 (1h) y 2 (2h)** — suaves, SIN plantilla ni instrucción de IA (solo el mensaje; van dentro de la ventana de 24h).
6. **Remarketing 1 (3h) y 2 (6h)** — cada uno con ángulo nuevo. En Chatea cada remarketing tiene 3 campos: **Tiempo** (3h/6h), **Plantilla Mensaje** (desplegable: se elige una plantilla de Meta aprobada o "No enviar plantilla"), e **Instrucción especial del remarketing** (un campo ≤1000 caracteres con el MENSAJE + la [Instrucción IA] juntos). La skill entrega los tres: el texto del campo de instrucción (copy-paste) + la plantilla de Meta completa para crear/seleccionar (nombre_minúsculas, categoría Marketing, español, imagen, cuerpo con {{1}}=nombre, pie, botón mapeado como "botón de remarketing"). Ver `estructura-disparo.md`.
7. **Activador — NORMA DE DOS ACTIVADORES por producto** (aprobada por el Centro de Mando 2026-08-07, chat dental Chile): se registran **DOS** palabras clave por producto:
   - **(1) La FRASE COMPLETA del anuncio/botón** (ej. "Hola quiero información y precio de [PRODUCTO]"), con el nombre del producto. Cubre los canales donde el enlace **precarga** el mensaje (botón de la página, CTA de WhatsApp en Meta).
   - **(2) UNA palabra corta ÚNICA y propia del producto** (ej. estilo "SONRISA" para gotas dentales, "HONGOS" para antihongos). Cubre **TikTok, estados de WhatsApp y comentarios**, donde NADA precarga y el cliente escribe a mano: sin ella el bot no dispara y la venta se pierde en silencio. Esa palabra corta se usa en **todo CTA escrito** ("escribe SONRISA").
   - **VERIFICACIÓN obligatoria de la palabra corta**: compararla contra TODAS las palabras clave de los demás productos del bot para que no se cruce. **JAMÁS palabras genéricas** ("información", "precio", "promo"): con varios productos disparan el bot equivocado.
   - **SIN NINGÚN EMOJI ni símbolo raro en ningún activador** — los de 4 bytes están PROBADOS: la base de Chatea los vuelve `�` y el trigger no coincide jamás (incidente 2026-07-26); los de 3 bytes (✨ ✅ ‼ ⁉ ℹ) no están probados contra la base, así que el default seguro es CERO. Y sin punto final. Texto crudo para copiar y pegar, sin prefijos ni comillas. **LA validación es `bash scripts/validar.sh --activador <archivo>`** (lista permitida: solo letras, números y puntuación básica; bloquea cualquier emoji de 3 o 4 bytes y el BOM) — la fórmula manual de 4 bytes NO basta, deja pasar ✨ y vecinos.

IMPORTANTE — DÓNDE VA CADA PIEZA: el paquete NO va todo en un solo campo. Cada pieza va en una sección distinta de Chatea. Entrega SIEMPRE el mapa de ubicación al usuario (ver `references/guia-configuracion-chatea.md`) y etiqueta cada pieza con la sección donde va, para que cualquier persona lo configure sin enredarse. No presentes la numeración como un orden secuencial dentro de un solo campo.

ENTREGA COPY-PASTE POR CAMPO (crítico — cada campo SEPARADO): cada pieza va con su **título como encabezado FUERA del bloque copiable**, y el **bloque copiable contiene ÚNICAMENTE el texto exacto que se pega** (nada de título, nada de anotaciones adentro). Así, cuando el vendedor copia el bloque, obtiene solo el texto, sin el título.
- Recordatorio 1 y Recordatorio 2 = CADA UNO su propio título + su propio bloque separado (no los juntes en un solo bloque).
- Remarketing 1 y Remarketing 2 = igual, cada campo de la plantilla claramente separado (nombre, cuerpo, pie, botón, instrucción IA).
- Etiquetas LIMPIAS, solo el nombre del campo, SIN paréntesis ni descripciones ("RECORDATORIO 1", no "R1 (1h)"; "REMARKETING 1", no "RM1 (confianza)"). El tiempo (1h/2h/3h/6h) va en el texto del informe, no dentro del bloque copiable.
- Palabras clave / mensajes: texto crudo dentro del bloque, sin "Palabra clave:" ni comillas.
El vendedor solo copia y pega. Debajo de todo va el MANIFIESTO DE IMÁGENES (no dentro del prompt).

REGLA DE MULTIMEDIA (crítica): hay dos tipos de audiovisuales y van en lugares distintos:
- Multimedia INICIAL (se envía al entrar) → va en "Contenido multimedia inicial", NO en el prompt.
- URLs que el AGENTE envía DURANTE el chat (modo de uso, tabla de precios, testimonios) → van ESCRITAS DENTRO del prompt, con la instrucción de cuándo enviarlas. En el prompt solo va la URL (o el marcador `[IMAGEN N — URL]` si aún no la hay).

SISTEMA DE IMÁGENES (ver `references/recursos-visuales.md`): además del prompt, entrega SIEMPRE un **MANIFIESTO DE IMÁGENES debajo del prompt** (nunca dentro). Por cada imagen conversacional (IMAGEN 1, 2, 3…): pregunta al cliente si tiene la URL; si la tiene, la pegas en el prompt; si NO la tiene, (a) **intenta generarla tú** si hay herramienta de imágenes conectada (Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch), o (b) entrégale un **prompt de imagen profesional** listo para pegar en cualquier IA; luego explícale que la suba a Chatea PRO para obtener la URL y te la pase, y tú finalizas el prompt con el enlace puesto. La skill intenta hacerlo todo; si no puede, dice exactamente cómo.

DATOS DE PAGO ANTICIPADO: si el negocio cobra anticipado, PREGÚNTALE al cliente (durante el desarrollo) los datos completos de la cuenta — titular + banco/entidad (Nequi/Daviplata/Bancolombia/etc.) + número/llave + TIPO de cuenta — y colócalos en la sección de anticipado del prompt. Nunca los inventes ni los dejes en blanco: si no los tiene a mano, deja el marcador `[AQUÍ VAN LOS DATOS DE PAGO ANTICIPADO]` y avísale que hay que completarlo.

## PASO 2.5 — Entregable PDF (recomendado; ver `references/entrega-pdf.md`)

Además de entregar el paquete copy-paste en el chat, **genera un PDF profesional** del paquete completo con la skill `golden-pdf-check` (estándar Golden, bloques atómicos anti-corte). Hazlo por defecto cuando el usuario quiera un documento para guardar, pasarle a un cliente o configurar sin depender del chat; y SIEMPRE que lo pida.

Reglas clave (detalle en `references/entrega-pdf.md`):
- Cada pieza copiable va en su propia **tarjeta** de prompt (` ``` `): saludo, pregunta de entrada, prompt, recordatorios, remarketing, activador, y los prompts de imagen.
- El **prompt de venta es largo** (suele pasar de 9.000 caracteres): no cabe legible en una página. **Pártelo en tarjetas "Parte 1 de N, Parte 2 de N…" y avisa que van SEGUIDAS, en orden, dentro del MISMO campo** (Prompt personalizado). El texto no cambia ni un carácter: solo se reparte. Apunta a que cada parte quede a tipo legible (si el build reporta `fit_warnings` con tipo < ~8pt, parte esa tarjeta en dos).
- Incluye la portada (marca), el mapa de configuración, el manifiesto de imágenes con los prompts de imagen, y una sección final de "qué falta por completar".
- Invoca `golden-pdf-check` (ella trae su propio motor: build + auditoría + compuerta verbatim; esta skill no tiene scripts de PDF). Entrega solo si el veredicto es APROBADO y el verbatim pasa (el prompt salió idéntico, copiable). Si esa skill no está disponible, entrega solo el copy-paste e infórmalo.

## PASO 3 — Auto-evaluación HOLÍSTICA (no entregues sin esto)

Antes de entregar, SIMULA tú mismo una conversación haciendo de **cliente difícil** (pregunta precio de entrada, objeta "está caro", desconfía, da datos incompletos/desordenados, elige pago anticipado y cambia un dato, pregunta por otro producto).

Luego **evalúa el prompt COMPLETO como un todo y califícalo del 1 al 100** — NO sumes puntos por ítems para llegar a 100. Es un juicio de calidad global: lee el prompt entero como si fueras un experto en venta conversacional y dale la nota honesta que merece. Si algo falla, la nota baja de verdad.

Usa esta lista como **guía de lo que debe tener un prompt excelente** (checklist para tu juicio, NO una suma):
- Da el precio de inmediato cuando lo piden, enmarcado, sin esconderlo.
- Pago anticipado blindado (nunca confirma sin comprobante válido).
- Captura de datos en un mensaje + validación anti-error.
- Objeciones reales cubiertas (caro, funciona, seguro, médico/legal sin claims, "lo pensaré", otro producto).
- Espeja el dolor antes de vender; no repite la pregunta de entrada.
- Conteo de combos correcto + matemática de upsell (costo incremental + beneficio).
- OFICINA según la política del negocio.
- Aprovecha el presupuesto (~9.000–11.000 con sustancia, sin relleno; techo 12.000).
- Tono humano (≤35 palabras, ≤2 emojis, sin signos de apertura de pregunta/admiración, nunca robótico, nunca dice que es IA).
- Upsell solo tras el cierre. FAQ/educación de producto. Cumplimiento (sin claims falsos).

REGLA DE ENTREGA: si la nota /100 no es sobresaliente, corrige lo que falle, vuelve a simular y repite hasta que el prompt sea excelente. Entrega mostrando: (a) la simulación del cliente difícil, (b) la **nota /100 con una justificación en prosa** (qué lo hace fuerte, qué se mejoró), y (c) el conteo de caracteres.

## PASO 3.1 — Escala 1 a 1000 (para llevarlo al máximo)

Después del /100, evalúa también **del 1 al 1000** y di explícitamente **qué le harías para llegar a 1000**. La escala /1000 es más exigente: mide qué tan cerca está del mejor prompt posible para ESE producto (profundidad de objeciones y FAQ, riqueza persuasiva, ángulos de la competencia, prueba social concreta, manejo de todos los escenarios de entrada, unit economics del upsell, etc.). Entrega el número /1000 + la lista concreta de mejoras que lo subirían.

VALIDADOR AUTOMÁTICO: guarda el bloque del prompt en un archivo y córrelo con `bash scripts/validar.sh <archivo.txt> [límite]`. El script mide con python (crudos + escapados + emojis + BOM) y BLOQUEA con exit distinto de 0 si excede un techo, está vacío o no es UTF-8 — no es informativo, es una compuerta. Además corre `bash scripts/validar.sh --activador <archivo>` sobre CADA activador: ahí exige 0 emojis de cualquier tipo y sin BOM. No estimes a ojo ni uses `wc -m`.

CUMPLIMIENTO OBLIGATORIO: antes de entregar, pasa también el checklist de `references/cumplimiento.md` (claims de salud, política de WhatsApp, datos personales). Un claim prohibido invalida la entrega aunque la nota sea 100.

CHECK DE DISPARO (además de la evaluación del prompt): verifica que el **saludo NO contenga pregunta** y que el texto de la multimedia tampoco; la ÚNICA pregunta que espera respuesta es la **pregunta de entrada**. Si el saludo pregunta algo, corrígelo antes de entregar.

## PASO 4 — Medición y versionado (cierra el bucle)

Un prompt no se "termina": se mejora con lo que pasa en campo. Al entregar, incluye SIEMPRE un bloque corto de seguimiento para que el usuario pueda medir y tú puedas mejorar la próxima versión:

1. **El versionado NO va en el prompt.** El header del prompt lleva SOLO `Producto · País · Compañía` (sin "v1", sin fecha). El número de versión y la fecha se llevan aparte, en el `resultados-ledger.md`. El prompt que se pega en Chatea queda limpio.
2. **Hipótesis de la versión:** una línea de qué apuesta hace esta versión (ej. "precio más temprano + garantía reforzada para bajar el 'lo pensaré'"). Va en el ledger, no en el prompt.
3. **3 métricas a vigilar** (el usuario las saca de Chatea PRO / su CRM): % que llega a captura de datos, % que confirma con SÍ, % de anticipados con comprobante. Si una está baja, indica qué punto de la checklist revisar.
4. **Prueba A/B sugerida:** propón UNA sola variable a testear en la siguiente versión (un hook, el orden del precio, la garantía), nunca varias a la vez.

Cuando el usuario vuelva con resultados, lee la versión anterior, ajusta la variable y entrega v+1 con su nueva hipótesis. Así el skill aprende del negocio real, no solo de la teoría.

REGISTRO DE RESULTADOS: lleva el historial en `references/resultados-ledger.md` (una fila por versión: hipótesis, métricas reales, qué A/B ganó, aprendizaje). Antes de construir una versión nueva, LEE el ledger de ese producto y parte de lo que ya ganó — nunca desde cero. Es lo que convierte al skill en un sistema que compone aprendizaje.

## Reglas de oro de la estructura ganadora

Estas vienen de los prompts con ventas reales comprobadas. Respétalas siempre:

- **Mensajes cortos** (máx 35 palabras), máx 2 emojis, UNA pregunta por mensaje, tono humano colombiano (o local), nunca robótico, nunca decir que es bot/IA.
- **Regla de precio prioritaria:** si preguntan precio en cualquier momento, darlo enmarcado de inmediato (beneficio + tabla + tranquilidad). Nunca esconderlo.
- **Intención de compra manda sobre el guion:** si el cliente dice "quiero comprar" o pide que no le pregunten más, se salta el descubrimiento y se va directo a precio/elección/datos. Jamás devolverlo a preguntas anteriores. (Validado en campo 2026-07: re-preguntar tras la intención de compra mata la venta.)
- **Memoria del pedido:** el prompt SIEMPRE incluye el bloque MEMORIA DEL PEDIDO (ficha actualizada por mensaje, audios incluidos, prohibido re-pedir un dato ya dado). Ver `plantilla-prompt.md`.
- **URLs blindadas:** todo prompt con imágenes conversacionales lleva el bloque IMÁGENES — REGLA CRÍTICA DE URLS (solo URLs etiquetadas de la lista, exactas; prohibido reutilizar URLs del historial; 1 imagen por mensaje; ante la duda, solo texto). La IA no ve imágenes: sin esto manda la equivocada.
- **Una sola confirmación:** el resumen respondido con SÍ; nunca "procedemos?"/"confirmo?" extra. Nunca un resumen con campos (Pendiente) o inventados. Tras un upsell aceptado, actualizar resumen sin volver a pedir datos.
- **Detectar antes de vender:** espejear el dolor del cliente con empatía antes de recomendar (solo con quien duda; no aplica a quien ya decidió).
- **Captura de datos en un solo mensaje** + validación anti-error (no avanzar con datos incompletos, ordenar lo desordenado, no repetir lo ya dado).
- **Resumen verificable** antes de confirmar; el cliente confirma con SÍ.
- **Anticipado blindado:** jamás confirmar sin comprobante válido.
- **Upsell solo después del cierre**, sin insistir si rechaza.
- **Matemática de upsell:** al sugerir 2/3 unidades (o combos), calcula y muestra el COSTO INCREMENTAL de la unidad/combo extra (delta = precio(n) − precio(n-1)) + el beneficio (envío prioritario, no interrumpir el proceso, repuesto/regalo). Nunca digas solo "quieres otra?": muéstrale cuánto gana. Ver `plantilla-prompt.md`.
- **Combos por cantidad (docena/pack) con variantes mezclables:** cuando cada combo trae N unidades fijas (ej. 12) y esas unidades se pueden mezclar entre sabores/colores, trátalo así: el "1/2/3" son COMBOS (no unidades sueltas), di siempre cuántas unidades trae cada uno, y en la captura agrega el campo de variante indicando que la suma por combo debe dar N (ej. "6 Pistacho, 3 Nucita, 3 Oreo = 12"). El upsell se calcula por COMBO extra. Ángulos que suben el ticket: regalar, evento, **revender**. Ver `plantilla-prompt.md`.
- **No insistir con la cantidad:** preguntarla una sola vez.
- **Máximo 2 intentos** de reactivación, sin desesperación.
- **Vender el beneficio (frescura, confianza, resultado), no el problema.**
- **Respuestas CONCRETAS, no ambiguas:** cuando el cliente pregunte algo medible (en cuántos días se ven resultados, cuánto rinde, cada cuánto se usa), responde con un **rango concreto** (ej. "muchas personas empiezan a notar cambios entre los 5 y 15 días con uso constante") + "varía en cada persona". Nunca respondas solo "depende" o "varía" sin dar un número. Sin prometer curas ni garantizar resultados.
- **Formato limpio del prompt:** header solo `Producto · País · Compañía` (sin versión). Usa saltos de línea simples; evita viñetas/tabulaciones decorativas innecesarias. Que se lea limpio.
- **La skill intenta hacerlo TODO por el cliente:** si algo lo puede resolver la skill (generar una imagen, calcular, redactar), lo hace; si no puede, le dice al cliente EXACTAMENTE cómo hacerlo y qué pegar. Nunca deja al cliente con un "hazlo tú" sin instrucciones.

## Conexiones (herramientas y skills hermanas)

Esta skill hace UNA cosa: el **prompt de ventas** (y sus piezas) para Chatea PRO. Se apoya en herramientas externas y se coordina con otras skills. Todas son OPCIONALES: si una no está conectada, la skill lo dice y ofrece el camino manual (nunca se rompe).

**Herramientas que usa (si están disponibles):**
- **Firecrawl** (`firecrawl_scrape` / `firecrawl_search`) → leer la URL del producto o de competidores, y buscar en la web. Si no está: pídele al vendedor que pegue los datos.
  🚨 **Verificación obligatoria — 4 checks, porque hay 3 modos de fallo y `statusCode: 200` no
  prueba nada:** existe el campo `json`? (Amazon devolvió muro anti-bot sin `json`) ·
  `metadata.title` poblado? (vacío → el extractor **inventa**: dio un Smart TV con precio y reseñas
  falsos para una página de verrugas) · `metadata.url` == `sourceURL`? (Temu redirigió y devolvió
  72 categorías de ropa, **con title poblado**) · **🎯 el dato responde a lo que pedí?**
  Si falla una: descartar y pedirle los datos al vendedor. **Aquí el riesgo es el más directo de
  todo el ecosistema:** un precio o un "4.5 estrellas" falso metido en el prompt se lo dice el bot
  **al cliente real**, en WhatsApp, como si fuera cierto — y ese cliente compra o se queja con base
  en eso.
  📖 `~/.claude/skills/golden-investigacion-mercado/references/scraping-firecrawl.md`
- **Visión** (nativa) → analizar la foto del producto que envíe el vendedor.
- **Meta Ad Library** → ver anuncios activos de la competencia para ángulos/objeciones reales. Si no está: usa la librería `objeciones.md`.
- **Generadores de imagen** (Higgsfield/Soul, Nano Banana, Magic, Gemini, Stitch) → crear multimedia e imágenes conversacionales. Si no hay ninguno: entrega el prompt de imagen para que el vendedor la genere (ver `recursos-visuales.md`).

**Skills hermanas (a qué derivar, sin reimplementar):**
- Config general del asistente de ventas / JSON de la tienda → `golden-chatea-pro-config-ventas-wp`.
- Asistente de COMENTARIOS de Chatea → `golden-chatea-pro-config-comentarios`.
- Asistente LOGÍSTICO (validación de direcciones) → `golden-chatea-pro-config-logistico`.
- Asistente de CARRITOS abandonados → `golden-chatea-pro-config-carritos`.
- Configurar TODOS los asistentes a la vez → `golden-chatea-pro-full-configuracion`.
- Copy de anuncios (Meta/TikTok), hooks, guiones → `golden-copywriting`.
- Imágenes/infografías de alta conversión → `golden-imagen-arena`.
- Avatares/UGC en video → `golden-ugc-avatar`.
- Página de producto Shopify (COD/Releasit) → `golden-shopify`.
- Análisis/armado de pauta → `golden-ads`.
- Entregable en PDF del paquete (bloques atómicos anti-corte) → `golden-pdf-check` (ver PASO 2.5 y `references/entrega-pdf.md`).
Esta skill NO hace pauta, ni página, ni la config general del bot: solo el prompt de ventas y sus piezas de disparo.

## Privacidad (skill compartible con la comunidad)

Esta skill se comparte. NUNCA hornees datos de un negocio real en sus archivos: nombres de asesor, precios, cuentas de pago (Nequi/Daviplata/banco), números, marcas o tiendas específicas se PREGUNTAN en cada uso y viven solo en el prompt que se entrega, jamás en la skill. Los ejemplos internos (FreshKlin, Valentina, etc.) son FICTICIOS. Si detectas un dato real incrustado en un archivo de la skill, es un error: quítalo.

## Archivos de referencia

- `references/guia-configuracion-chatea.md` — **Mapa de dónde va cada pieza en Chatea PRO** (saludo, multimedia, pregunta, prompt, recordatorios, remarketing, palabras clave). Entrégalo siempre al usuario para que configure sin enredarse.
- `references/plantilla-prompt.md` — Esqueleto completo del prompt de venta, bloque por bloque, con ejemplos. Léelo siempre antes de escribir el prompt.
- `references/ejemplo-completo.md` — **Ejemplo horneado de punta a punta** (producto resuelto con las 7 piezas + evaluación de calidad). Úsalo como vara de calidad: tu salida real debe igualar ese nivel de detalle.
- `references/estructura-disparo.md` — Plantillas de saludo, multimedia, pregunta de entrada, recordatorios, remarketing y activador.
- `references/checklist-multimedia.md` — Lista de las URLs/imágenes que conviene pedir al usuario y dónde se usan.
- `references/objeciones.md` — **Librería de objeciones** por categoría (precio, confianza, logística, salud/legal, decisión). Elige las que apliquen e insértalas en el bloque OBJECIONES.
- `references/paises.md` — **Packs por país** (los 7 de la plataforma: CO/MX/PE/CL/EC/PA/PY): nomenclatura de dirección, transportadoras, medios de pago y tono. Usa el del país del negocio.
- `references/cumplimiento.md` — **Guardarraíles legales/plataforma**. Checklist obligatorio antes de entregar.
- `references/resultados-ledger.md` — **Registro de resultados** para medir versiones y componer aprendizaje (PASO 4).
- `references/recursos-visuales.md` — **Sistema de imágenes/URLs**: cómo listar las imágenes conversacionales, generarlas (o dar el prompt de imagen), y el manifiesto que se entrega DEBAJO del prompt. En el prompt solo va la URL.
- `references/intake-inteligente.md` — **Intake inteligente (PASO 0)**: el FORMULARIO de una vez (país 1º, obligatorio vs opcional, relleno inteligente), el gate de anticipado, y cómo tomar el producto por URL (scrape), foto (visión) o investigándolo (competencia/web).
- `references/entrega-pdf.md` — **Entregable PDF (PASO 2.5)**: cómo generar el paquete como PDF con `golden-pdf-check`, con el prompt partido en tarjetas atómicas "Parte N de N" que van seguidas en el mismo campo.
- `references/referencia-externa-embudo-whatsapp-cod.md` — **REFERENCIA OPCIONAL, NO REGLA** (masterclass de terceros sobre embudo COD por WhatsApp). Consúltala solo para contrastar o enriquecer ángulos; JAMÁS sustituye la estructura obligatoria de esta skill ni el método FER. En conflicto, manda la skill.
- `scripts/validar.sh` — **Validador-compuerta**: mide crudos, escapados, emojis y BOM con python y BLOQUEA (exit != 0) si algo excede; modo `--activador` exige 0 emojis. Córrelo antes de entregar, también sobre cada activador.
