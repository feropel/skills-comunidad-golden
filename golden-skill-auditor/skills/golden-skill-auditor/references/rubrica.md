# Rúbrica Golden de skills — 1000 puntos, 7 dimensiones

Cada dimensión parte de su puntaje máximo y se resta por hallazgo, con la evidencia al lado (archivo:línea o ausencia concreta). Las restas sugeridas son guía: un mismo defecto repetido 10 veces se cobra como patrón (una resta grande), no 10 veces.

Regla de oro del calificador: la pregunta nunca es "está bonito", es **"un Claude que lee esto por primera vez, en un chat limpio, produce el resultado correcto sin ayuda"**.

---

## 1. Activación — 120 pts

El description del frontmatter es el ÚNICO mecanismo de disparo. Si no dispara, la skill no existe.

| Chequeo | Resta si falla |
|---|---|
| Dice QUÉ hace la skill en la primera frase | −15 |
| Dice CUÁNDO usarla con frases reales del usuario ("dispara cuando diga...") | −25 |
| Es "pushy": cubre sinónimos, español coloquial, casos donde el usuario no nombra la skill | −15 |
| Dice cuándo NO usarla / a qué skill hermana derivar (desambiguación) | −20 |
| No promete nada que el cuerpo no entregue, ni oculta capacidades que sí tiene | −20 |
| `name:` coincide con el nombre de la carpeta | −15 |
| Longitud sana: ni una línea seca ni un ensayo que entierra los triggers | −10 |

Señal de excelencia (para llegar a 120): el description compite bien contra las skills hermanas — un pedido ambiguo cae en la skill correcta porque cada description marca su frontera.

## 2. Estructura — 140 pts

Divulgación progresiva de 3 niveles: metadata siempre en contexto → cuerpo al disparar → references solo cuando se necesitan.

| Chequeo | Resta si falla |
|---|---|
| SKILL.md ≤500 líneas (si se pasa, falta un nivel de jerarquía) | −25 |
| Todo lo que no se necesita en CADA invocación vive en references/, no en el cuerpo | −25 |
| Cada reference tiene puntero desde SKILL.md con CUÁNDO leerla ("lee X antes de Y") | −25 |
| References >300 líneas traen tabla de contenido | −10 |
| Organización por variante cuando aplica (un archivo por país/tema/plataforma, se carga solo el relevante) | −15 |
| Sin archivos huérfanos (existen pero ningún archivo los menciona) | −15 |
| Sin duplicación entre archivos (la misma tabla/regla en dos lugares se desincroniza) | −15 |
| Frontmatter YAML válido, solo campos reales (name, description; opcional compatibility) | −10 |

## 3. Instrucciones — 200 pts

La dimensión más pesada: es donde vive la calidad del resultado.

| Chequeo | Resta si falla |
|---|---|
| Imperativas y dirigidas al ejecutor ("haz X"), no descripciones vagas ("se podría X") | −20 |
| Explican el PORQUÉ de lo importante (el porqué generaliza; el MUST pelado se rompe en el caso 11) | −30 |
| Cero contradicciones internas (regla A dice una cosa, ejemplo B hace otra) | −35 |
| Formatos de salida definidos con plantilla exacta cuando el output es estructurado | −25 |
| Ejemplos concretos entrada→salida de los pasos no obvios | −25 |
| Cubre casos borde reales del dominio (qué hacer cuando falta el dato, cuando la plataforma cambia, cuando el resultado sale malo) | −25 |
| Sin sobreajuste al ejemplo con que se desarrolló (nombres/cifras del producto de prueba fosilizados como si fueran regla) | −20 |
| Términos ambiguos definidos (si dice "optimizado", dice contra qué se mide) | −20 |

## 4. Proceso y flujo — 180 pts

| Chequeo | Resta si falla |
|---|---|
| El flujo cubre de punta a punta: qué recibe, qué produce, y TODOS los pasos intermedios | −30 |
| Cada punto de decisión tiene default por convención (autonomía Golden: decide e informa; solo pregunta lo que únicamente el usuario sabe) | −30 |
| Manejo de error por paso: qué hacer si el script falla, el MCP no está, el archivo no existe | −25 |
| Paso de verificación/QA antes de entregar (la skill se revisa a sí misma) | −25 |
| Definición de "terminado" explícita (checklist o criterio medible) | −20 |
| Orden lógico sin dependencias circulares ni pasos que asumen resultados aún no producidos | −20 |
| Los datos de entrada requeridos se piden UNA vez al inicio (intake), no goteados a lo largo del flujo | −15 |
| Declara qué NO hace y a dónde delegar (frontera con skills hermanas) | −15 |

## 5. Recursos — 120 pts

| Chequeo | Resta si falla |
|---|---|
| Scripts pasan chequeo de sintaxis (bash -n / ast.parse, nunca py_compile: escribe bytecode y falla en skills blindadas) y sus rutas internas existen | −30 |
| Cero referencias rotas: todo archivo mencionado existe (y viceversa, ver huérfanos en Estructura) | −30 |
| Trabajo determinista repetido está en scripts/, no reinventado en prosa cada vez | −20 |
| Assets usados por el flujo (plantillas, fuentes, JSON de marca) presentes y vigentes | −15 |
| Dependencias de scripts declaradas (librerías, binarios) con instrucción de instalación o fallback | −15 |
| Cero secretos en el código (keys, tokens, contraseñas — ni siquiera "de prueba") | −10 (y 🔴 crítico automático) |

## 6. Estándares Golden — 120 pts

Detalle completo en `estandares-golden.md`. Resumen de cobro:

| Chequeo | Resta si falla |
|---|---|
| Prefijo `golden-` en skills propias (name: y carpeta y referencias cruzadas) | −20 |
| Cero signos de apertura ¿ ¡ en TODO texto que la skill genere o contenga como plantilla | −15 |
| Cero datos privados de FER o clientes (teléfonos, cuentas, keys, URLs internas con tokens) | −25 (y 🔴 crítico) |
| Autonomía máxima: la skill no pregunta lo que puede resolver por convención | −20 |
| Referencias a skills hermanas por nombre vigente y "a prueba de versiones" (no citan versión interna de la otra) | −15 |
| Datos reales antes de generar: si el output cuesta render/créditos, exige los datos reales (precio, WhatsApp) antes de producir | −15 |
| Blindaje coherente: si es pública/estable está blindada; el mecanismo (uchg vs chmod) está documentado en su memoria o changelog | −10 |

En skills de terceros (no golden-): se evalúan solo datos privados, secretos y autonomía; el resto de esta dimensión se prorratea sobre esos chequeos.

## 7. Robustez — 120 pts

| Chequeo | Resta si falla |
|---|---|
| Versión + changelog visibles (patrón de la casa: comentario HTML bajo el H1) | −20 |
| Consistencia interna total: misma cifra, mismo nombre, mismo formato en todos los archivos | −25 |
| Degradación elegante: si falta un MCP/tool/skill hermana, hay plan B declarado | −25 |
| Portabilidad: sin rutas hardcodeadas frágiles (las rutas a ~/.claude/skills/... propias sí valen) | −15 |
| Sin fechas/datos perecederos sin marcar (precios "de hoy", UIs de plataformas que cambian — deben decir "verificar en vivo") | −20 |
| El conocimiento de campo está anclado (de dónde salió la regla: probado en vivo, doc oficial, lección de campaña) | −15 |

---

## Cálculo y veredicto

- Puntaje = suma de las 7 dimensiones tras restas (mínimo 0 por dimensión).
- **ORO** 950–1000 · **PLATA** 850–949 · **BRONCE** 700–849 · **EN OBRA** <700.
- Un 🔴 crítico (secretos, datos privados, referencia rota en el camino principal, contradicción que cambia el resultado) impide veredicto ORO aunque el número alcance.
