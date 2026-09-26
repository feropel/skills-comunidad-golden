---
name: golden-brand-brain
description: >
  Golden Group — CEREBRO DE MARCA (Brand Brain). Crea y mantiene una carpeta viva de
  conocimiento por cada marca/cliente (voz, productos, avatares de cliente, competidores,
  anuncios ganadores, cambios recientes) para que TODO lo que se genere — anuncios, copy,
  páginas, videos UGC, bots de WhatsApp — suene como esa marca y venda como esa marca,
  sin re-explicar el negocio cada vez. Úsala SIEMPRE que el usuario quiera: crear o montar
  el cerebro de una marca, "brand brain", "carga mi marca", "alimenta a Claude con mi negocio",
  "que todo suene como mi marca", registrar un anuncio ganador o actualizar datos de la marca,
  o cuando otra skill necesite el contexto de marca ("lee el cerebro de X y trabaja").
  También al arrancar assets para una marca que YA tiene cerebro: leerlo PRIMERO.
  NO es el estudio de mercado (eso es golden-investigacion-mercado, que ALIMENTA este cerebro);
  tampoco genera los assets (eso lo hacen golden-ads/copywriting/shopify/ugc leyendo de aquí).
---

**Fábrica:** chat «✅ SKILL golden-brand-brain»
<!-- Historial completo de esta skill: references/changelog.md (4 actas + bitácora AUTO-MEJORA, migración completada 2026-09-20). El cuerpo se paga en cada activación; el acta no. -->
<!-- skill BB1.4 — 2026-09-20 — auditoría golden-skill-auditor (AUDITA+ARREGLA): la mudanza de changelog del 2026-09-05 había quedado a medias — el cuerpo seguía cargando la sección "## Changelog" completa (BB1.0-BB1.3) Y el AUTO-MEJORA traía una entrada fechada suelta, mientras references/changelog.md solo tenía 2 de 4 actas en forma resumida (contradice su propia frase "todo está literal"). Se completa el acta con las 4 versiones + la bitácora AUTO-MEJORA, literales, y se trimma el cuerpo al puntero — el patrón que ya usan las demás skills mudadas el 2026-09-05. Contenido y estructura operativos intactos. -->

# Golden Brand Brain — el cerebro vivo de cada marca


**Versión:** `BB1.4` · Un setup, todos los assets on-brand.

La idea: en vez de re-explicar tu negocio en cada chat, cada marca tiene UNA carpeta de
conocimiento que yo leo antes de generar cualquier cosa. Se monta una vez, se actualiza
con la operación, y todas las skills Golden beben de ahí.

## Dónde viven los cerebros (convención)

```
PROYECTOS/BRAND-BRAINS/<MARCA>/
├── marca.md                → identidad, voz, tono, qué dice y qué JAMÁS dice
├── productos.md            → catálogo: nombre, precio REAL, ángulo, best-sellers
├── avatares.md             → los 2-3 clientes tipo (dolores, deseos, objeciones)
├── competidores.md         → quiénes son, qué prometen, cómo nos diferenciamos
├── anuncios-ganadores.md   → hooks/creativos que YA funcionaron (con métricas)
└── cambios-recientes.md    → lo nuevo: precios, ofertas, restocks, aprendizajes
```

Un cerebro por marca: Golden Group Enterprise, Organic Bless, Lecoterra, cada cliente/alumno.
Si la carpeta no existe cuando se necesita, ofrécete a crearla (Modo 1) — no trabajes a ciegas.

**Cómo se resuelve la ruta en cualquier entorno (contrato para un chat sin memoria):**
1. `PROYECTOS/` es la carpeta raíz de proyectos del usuario — normalmente el propio directorio
   de trabajo del chat o una carpeta directa dentro de él. No adivines: verifícalo con `ls`.
2. Antes de crear `BRAND-BRAINS/`, **busca si ya existe una** (ej.
   `find <raíz de proyectos> -maxdepth 2 -type d -name "BRAND-BRAINS"`). Dos carpetas
   BRAND-BRAINS = dos cerebros de la misma marca divergiendo en silencio; es el peor fallo posible.
3. El nombre de la carpeta de marca va en `MAYÚSCULAS-CON-GUIONES` (ej. `GOLDEN-GROUP`),
   igual que su carpeta de proyecto si la tiene.
4. Si tras buscar no aparece ni la carpeta ni la marca, eso NO es error: es Modo 1 (ofrecer crearla).

**Contrato de consumo (para las skills que leen el cerebro — el "Paso 0" de las 7 de contenido):**
`ls <raíz>/BRAND-BRAINS/` → carpeta de la marca → leer los 6 archivos completos (son cortos) →
generar con esa voz. Un campo `[PENDIENTE]` leído se respeta: se pregunta o se declara, jamás se
rellena inventando.

## Modo 1 — CREAR el cerebro (setup, una vez)

0. **Revisa si la carpeta ya existe antes de escribir nada.** Si `PROYECTOS/BRAND-BRAINS/<MARCA>/`
   ya tiene alguno de los 6 archivos, esto NO es un setup limpio: es un cerebro parcial. No
   sobrescribas lo que ya está lleno — completa solo los archivos faltantes y los campos
   `[PENDIENTE]` que ya existan, tal como en Modo 2. Sobrescribir un archivo con datos reales
   por una plantilla vacía es la forma más rápida de perder trabajo ya hecho.
1. **Fuentes primero, preguntas después.** Reúne de lo que ya existe:
   - Dossier de `golden-investigacion-mercado` si lo hay (avatares, competidores, voz del cliente).
   - La tienda/web real (URL), reseñas, redes.
   - Datos de la operación: best-sellers, anuncios que funcionaron (pedir métricas reales).
   Si ninguna fuente existe (marca 100% nueva), no te detengas: pasa al paso 2 y arranca los 6
   archivos casi todo en `[PENDIENTE]` — un cerebro incompleto que existe es más útil que uno
   perfecto que nunca se creó.
2. **Pregunta SOLO lo que falte** y con campo para llenar (precio real: ____, WhatsApp: ____).
   Lo que no esté, se marca `[PENDIENTE]` y se sigue — preguntar no es bloquear.
3. **Escribe los archivos que falten** con la plantilla de `references/plantilla-cerebro.md`.
   Concreto y usable: frases de la voz real del cliente, números reales, nada de relleno.
4. **Verifica contra el checklist de setup** (al final de `references/plantilla-cerebro.md`)
   antes de dar por terminado: los 6 archivos existen, los datos duros son reales o están
   marcados `[PENDIENTE]` a la vista, hay al menos 3 frases reales de clientes en avatares.md.
   Terminado = ese checklist en verde o con sus huecos declarados, nunca "quedó listo" a ojo.
5. **Informa** el resumen: qué quedó cargado, qué quedó `[PENDIENTE]`, y si el checklist cerró
   completo o con pendientes.

## Modo 2 — ACTUALIZAR el cerebro (mantenimiento)

Disparos típicos: "ganó este anuncio", "cambió el precio", "nuevo producto", "aprendimos que…".
- Anuncio ganador → `anuncios-ganadores.md` con hook, formato, métrica y por qué ganó.
- Cambios de oferta/precio/stock → `cambios-recientes.md` (con fecha) y `productos.md`.
- Mantén los archivos CORTOS: el cerebro es contexto de trabajo, no un archivo histórico.
  Lo viejo que ya no aplica se borra (regla Golden: borrado definitivo, no "por si acaso").

## Modo 3 — USAR el cerebro (el que más se repite)

Cuando se va a generar CUALQUIER asset para una marca con cerebro:
1. Lee la carpeta completa (6 archivos, son cortos).
2. Genera con ese contexto: la voz de `marca.md`, los dolores de `avatares.md`,
   la diferenciación de `competidores.md`, los hooks probados de `anuncios-ganadores.md`.
3. Deriva el trabajo a la skill que corresponde — este cerebro NO reemplaza a las skills:
   - Pauta/creativos → `golden-ads` · Copy → `golden-copywriting`
   - Página producto → `golden-shopify` · Web → `golden-web`
   - Imágenes → `golden-imagen-arena` · Video UGC → `golden-ugc-avatar`
   - Bot ventas WhatsApp → `golden-chatea-pro-prompt-ventas`
4. Si en el trabajo aparece un dato nuevo valioso (ángulo que convierte, objeción repetida),
   ofrece guardarlo en el cerebro (Modo 2). Así el cerebro aprende de la operación.

## Reglas de oro
1. **Datos reales o `[PENDIENTE]`** — jamás inventar precio, WhatsApp, claims o métricas.
2. **Sin datos privados dentro de esta skill** — los datos viven en la carpeta del cerebro
   de cada marca (PROYECTOS/), NUNCA aquí (esta skill se comparte con alumnos).
3. **Cerebro corto y vivo** — máximo ~1 página por archivo; se poda lo viejo.
4. **El cerebro alimenta, las skills ejecutan** — no dupliques aquí lo que ya hacen ellas.
5. **Compliance** — claims según la vertical (salud = prudencia); lo prohibido va en `marca.md`.

## Referencias
- `references/plantilla-cerebro.md` — plantilla completa de los 6 archivos, con ejemplos
  de formato y el checklist de setup. Leer al crear o reestructurar un cerebro.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

Historial completo en `references/changelog.md`.
