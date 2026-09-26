# Historial de golden-critico

Acta completa. Se mudó aquí desde el cuerpo del SKILL.md el 2026-09-05 por el Centro de Mando: **el cuerpo se paga en CADA activación y el acta no se consulta al trabajar.** Nada se borró, todo está literal.



## Mudado del cuerpo del SKILL.md el 2026-09-05

<!-- skill v1.2 (GC1.2) · 2026-08-23 (Estándar 9, golden-skill-auditor) · Estándar 9 (Centro de Mando): cambios relevantes de esta skill se reportan a 🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. -->

## Mudado del cuerpo del SKILL.md el 2026-09-06 (auditoría golden-skill-auditor, GC1.3)

Hallazgo real: el comentario de arriba decía "el cuerpo se paga en cada activación; el acta no",
pero el cuerpo seguía cargando el `## Changelog` completo (GC1.0-GC1.2) y la entrada de bitácora
del `## 🔄 AUTO-MEJORA` en cada invocación — la mudanza de 2026-09-05 solo copió UNA acta aquí y
dejó las demás duplicadas/sin mover en el cuerpo. Se completa la mudanza: las tres actas y la
entrada de bitácora bajan aquí íntegras; el cuerpo se queda con el comentario HTML de versión
(patrón de la casa) y el mandato de AUTO-MEJORA (que sí es instrucción activa, no historia).

- **GC1.2** (2026-08-23) — Estándar 9 (Centro de Mando, golden-skill-auditor): comentario HTML
  bajo el H1 declarando que los cambios relevantes de esta skill se reportan a
  🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. Cambio puntual, sin tocar el resto del contenido.
- **GC1.1** (2026-08-21) — Auditoría golden-skill-auditor: añadida sección "Qué recibe y qué
  entrega" (intake único al inicio, degradación elegante sin brand-brain/datos/skills hermanas),
  Plantilla de salida con esqueleto exacto de markdown, y ejemplo corto entrada→salida ilustrativo
  (no fosiliza cifras de un producto real). Blindaje: `chflags uchg` (quitar con
  `chflags -R nouchg`, reponer con `chflags -R uchg`) — mecanismo documentado aquí por primera vez.
- **GC1.0** (2026-07-11) — Creación. Método Fable de 5 pasos: objetivo real → supuestos →
  6 frentes de riesgo → pre-mortem → veredicto (matar/pivotar/seguir con condiciones) + top 3.
- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección
  **AUTO-MEJORA** (mandato global de FER, autorización permanente). Sin esta sección la skill no
  se auto-calificaba al cerrar corrida. Contenido operativo intacto. Backup:
  `_backups/2026-08-02-loop-arsenal-s1/`.

## GC1.3 (2026-09-06) — auditoría golden-skill-auditor, AUDITA+ARREGLA

Dos hallazgos reales con evidencia, reparados:

1. **Duplicación cuerpo↔acta (Estructura).** Ver arriba: se completó la mudanza que la v1.2 dejó
   a medias. El cuerpo cae de 195 a ~165 líneas y ya no repite lo que este archivo ya dice.
2. **Version stamp fuera del patrón de la casa (Robustez).** El cuerpo marcaba la versión con una
   línea en negrita (`**Versión:** GC1.2`) y el comentario de mudanza vivía ANTES del H1, no
   debajo — estándares-golden.md #7 exige el comentario HTML `<!-- skill vX.Y · ... -->` bajo el
   H1, como usan las demás skills golden-*. Corregido: el H1 va primero, el comentario de versión
   baja inmediatamente debajo con el resumen de esta acta y el puntero a este archivo.
3. **Loop de autocrítica con lenguaje ajeno al dominio (Instrucciones).** La sección hablaba de
   "la variante más débil del lote" y de revisar "modelo de pago" y "posicionamiento del
   producto" — vocabulario de una skill de copys/producto (varios entregables por corrida), pero
   golden-critico entrega SIEMPRE un solo documento de crítica, nunca un lote de variantes, y su
   dominio es cualquier decisión de negocio, no solo producto con modelo de pago. Reescrito para
   auto-chequear las 5 secciones de la Plantilla de salida (cuál quedó floja/genérica) y las
   reglas de estilo propias de esta skill (signos de apertura, crueldad performática, evidencia
   real vs inventada) en vez de conceptos de otro dominio.

Blindaje: sigue `chflags uchg` (mismo mecanismo, re-aplicado al cerrar esta reparación).
