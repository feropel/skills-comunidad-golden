# Plantilla de teardown (rellenar una por video, luego síntesis)

## Encabezado del análisis
- Producto · país · modelo de pago (COD/anticipado) · moneda.
- Archivos analizados (nombre, duración, resolución, audio sí/no).
- Fecha del análisis · fuente (ffmpeg frames + STT si aplica).
- Rendimiento conocido (de golden-meta-ads-analysis): CPA/ROAS/compras por creativo si existe.

---

## VIDEO <n> — "<etiqueta del ángulo>" <🥇/🥈/🟡/🔴>
Duración Xs. Rendimiento (si se conoce): CPA $… · ROAS … · compras ….

**Beat sheet (segundo a segundo):**
- 0–3s · **GANCHO.** [texto en pantalla literal] + [descripción visual] → [por qué engancha].
- 3–Xs · [beat] · [texto] · [visual].
- … (un renglón por cada beat, hasta el final; no omitir ninguno).
- …–fin · **CTA/OFERTA.** [texto literal de la oferta].

**Hook (0-3s):** tipo (problema real / pregunta / autoridad / demo / miedo) · por qué funciona.
**Ángulo / enfoque:** [problema-solución · testimonio · autoridad-experta · demo satisfactorio · miedo/educación · mecanismo-ingrediente · comparación-vs-alternativa].
**Copy / guion:** tono, palabras clave, estilo de subtítulos; oferta y garantía.
**Fortalezas:** qué hace bien (replicable).
**Debilidades / riesgos:** qué resta rendimiento o arriesga baneo (marca de agua ajena, CTA en inglés, empaque de otra marca, español automático, claims médicos, precio prematuro, fatiga por frecuencia).
**Veredicto:** REPLICAR ADN / RESCATAR solo el <hook|ángulo|animación> / DESCARTAR — con la acción concreta.

---

## SÍNTESIS (cuando hay varios videos)

**Tabla de estado:** | Video | Veredicto | Acción |

**ADN ganadores comunes:** los 2-3 patrones que más rinden (con su porqué).

**Obligatorios:** elementos que todo video nuevo debe llevar (hook 0-3s, ingrediente héroe, demo, cierre COD localizado, formato 9:16, subtítulos ES).

**Prohibidos:** lo que baña Meta o rinde menos (CTA en inglés, marcas de agua ajenas, empaque de otra marca, español automático, precio desde el segundo 1, reusar cara hasta fatiga, claims médicos).

**Briefs de video nuevo (2-3):** por cada uno → ángulo, hook (texto exacto 0-3s), texto en pantalla clave, estructura de beats, oferta/CTA. Listos para pasar a golden-ugc-avatar / golden-ads.

**Pendientes para veredicto de rentabilidad:** los datos que faltan (p. ej. costo del producto) para cruzar con golden-meta-ads-analysis.

---

## Ejemplo real (entrada → salida) — para calibrar nivel de detalle

Entrada: un video UGC de 22s de un sérum capilar, subtítulos quemados en español, sin locución transcrita (sin STT disponible).

Salida esperada (fragmento del beat sheet, mismo nivel de detalle que se espera en cada video real):

```
## VIDEO 1 — "testimonio antes/después" 🥇
Duración 22s. Rendimiento: no informado.

**Beat sheet (segundo a segundo):**
- 0–3s · GANCHO. ["Esto me pasó en 3 semanas"] + mujer sostiene mechón de cabello frente a cámara,
  luz natural, primer plano del cuero cabelludo → engancha por dolor visible + promesa de tiempo corto.
- 3–8s · PROBLEMA. ["Llevaba 2 años perdiendo cabello y nada funcionaba"] + toma de cepillo lleno de pelo
  sobre lavamanos, tono resignado.
- 8–14s · DEMO. ["Lo uso 2 veces al día, se absorbe rápido"] + aplica el sérum con gotero sobre raíz,
  primer plano del frasco con etiqueta legible.
- 14–19s · RESULTADO. ["A las 3 semanas ya no se me caía tanto"] + comparación lado a lado antes/después,
  mismo ángulo de cámara.
- 19–22s · CTA/OFERTA. ["Está en descuento hoy, el link está abajo"] + banner de precio en pantalla.

**Hook (0-3s):** tipo demo/dolor real · funciona porque muestra la evidencia (mechón) antes de decir nada.
**Ángulo / enfoque:** testimonio + demo satisfactorio.
**Copy / guion:** tono cercano, primera persona, sin tecnicismos; oferta al cierre, sin garantía explícita
(riesgo: falta mención de garantía o devolución).
**Fortalezas:** hook visual fuerte, demo del producto real (no genérico), comparación honesta.
**Debilidades / riesgos:** sin garantía verbalizada; sin subtítulos en los primeros 2s (el gancho hablado
llega antes que el texto en pantalla, riesgo si se ve sin audio).
**Veredicto:** REPLICAR ADN — el hook de mechón + demo de aplicación es el patrón a reusar; agregar
garantía verbalizada en el brief nuevo.
```

Este es el nivel de detalle esperado: texto literal citado entre corchetes, un renglón por beat sin
saltarse segundos, diagnóstico (no solo descripción) en cada campo.
