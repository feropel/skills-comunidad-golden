# Estándares Golden — la vara de la casa

Reglas globales del ecosistema de FER / Golden Group. Toda skill propia se mide contra esto en la dimensión 6 de la rúbrica. Vienen de decisiones ya tomadas y confirmadas — no se re-litigan en cada auditoría, se verifican.

## 1. Marca y nombres

- Toda skill propia se llama `golden-<algo>`: en la carpeta, en el `name:` del frontmatter y en cada referencia cruzada desde otras skills. Un renombre que no propagó las referencias rompe a las hermanas en silencio — al auditar, grep del nombre viejo en TODO ~/.claude/skills.
- Dos niveles de marca: lo interno/empresa = "Golden Group"; lo que se comparte con alumnos/comunidad = "Comunidad Golden".

## 2. Escritura

- Cero signos de apertura `¿` y `¡` en todo texto que la skill genere, contenga como plantilla o entregue al usuario final. Solo el signo de cierre. Aplica a ejemplos, plantillas de mensajes, prompts horneados — todo.
- Español directo y humano, imperativo para instrucciones al modelo.

## 3. Autonomía máxima

- La skill decide todo lo decidible por convención/defaults e INFORMA lo que decidió. No pregunta lo que puede resolver. "Entre menos actúe FER, mejor."
- La excepción legítima: datos que SOLO el usuario tiene (precio real, número de WhatsApp, claims permitidos, etiquetas exactas de una plataforma cerrada). Eso se pide UNA vez, al inicio (intake), nunca goteado.

## 4. Datos reales antes de generar

- Si el output cuesta créditos/render/dinero (imágenes, video, PDFs finales, campañas), la skill exige los datos reales ANTES de producir. Inventar precio o WhatsApp y re-renderizar es pagar dos veces.

## 5. Cero datos privados

- Ninguna skill contiene: teléfonos reales, API keys, tokens, contraseñas, IDs de cuentas publicitarias, URLs con credenciales, datos de clientes. Las skills se comparten con la comunidad; lo privado vive en la memoria de Claude o se pide en el intake.
- Si la skill necesita apuntar a algo privado, usa un puntero abstracto ("el número que el usuario entregue en el intake").

## 6. Blindaje

- Skills públicas/estables se blindan read-only. Dos mecanismos en uso — al reparar, restaurar el MISMO que tenía:
  - `chflags uchg`: quitar con `chflags -R nouchg`, reponer con `chflags -R uchg`.
  - `chmod` dirs 0555 / archivos 0444: quitar con `chmod -R u+w`, reponer con `chmod -R a-w`.
  - Cuál mecanismo tiene cada hermana se verifica EN VIVO con `ls -ldO` al momento de auditar — este documento no afirma el estado de terceros porque cambia con cada reparación (foto fechada 2026-08-21: golden-ads y golden-investigacion-mercado estaban en uchg ese día; no asumir que sigue así).
- El pedido explícito del usuario de arreglar/mejorar ES la autorización para desbloquear. Auditar (solo leer) nunca requiere desbloquear.
- Blindaje NUEVO (skill que no estaba blindada): el estándar por defecto es `chflags -R uchg`. Una skill golden- que cierra reparación en 1000 sin pendientes con dueño se blinda automáticamente — lo perfecto se protege. Terceros nunca se blindan (rompe sus actualizaciones).
- Cada skill tiene (idealmente) un chat-fábrica dueño. Reparar desde otro chat es válido con pedido del usuario; el informe final debe recordar cuál es la fábrica si se conoce.

## 7. Versionado y anclaje

- Patrón de la casa para versión/changelog: comentario HTML bajo el H1 de SKILL.md, ej. `<!-- skill v3.0 · rúbrica de pesos + validador + ... -->`. Versiones tipo vX.Y o GX.Y.
- Conocimiento de campo anclado: cuando una regla salió de una prueba en vivo o una lección de campaña, la skill lo dice ("validado en vivo", "lección CP8"). Eso le dice al próximo editor qué NO puede tocar sin re-verificar.
- Referencias entre skills a prueba de versiones: se cita a la hermana por nombre y capacidad ("golden-shopify, su versión más actual"), nunca por número de versión interna de la otra.

## 8. Ecosistema y delegación

- Cada tool/skill nueva se adapta al ecosistema: trigger preciso, se encadena SOLO donde potencia, documentada. No llamar por llamar.
- Fronteras conocidas del ecosistema (para verificar delegaciones): páginas de producto Shopify → golden-shopify · imágenes de producto → golden-imagen-arena · video UGC → golden-ugc-avatar · pauta → golden-ads · PDFs → golden-pdf-check · investigación 360° → golden-investigacion-mercado · Chatea PRO → familia golden-chatea-pro-* (orquestador full-configuracion + 4 asistentes + 2 hijas).
- Popups y CTAs sin texto negativo ("No gracias" prohibido) — aplica a skills que generen UI o copys.
