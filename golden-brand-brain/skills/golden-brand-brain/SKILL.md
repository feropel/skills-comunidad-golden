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

# Golden Brand Brain — el cerebro vivo de cada marca

**Versión:** `BB1.1` · Un setup, todos los assets on-brand.

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

## Changelog
- **BB1.1** (2026-08-21) — Auditoría `golden-skill-auditor`: Modo 1 ahora revisa PRIMERO si el
  cerebro ya existe parcial antes de escribir (no sobrescribe archivos con datos reales), define
  qué hacer cuando no hay ninguna fuente (arranca en `[PENDIENTE]`, no se detiene), y ata el
  checklist de `plantilla-cerebro.md` como criterio explícito de "terminado" antes de informar.
  Contenido y estructura originales intactos.
- **BB1.0** (2026-07-11) — Creación. Concepto adaptado y mejorado del patrón "Brand Brain"
  (AI CMO/Nu Reach, visto en redes): carpeta viva por marca + 3 modos (crear/actualizar/usar)
  + convención PROYECTOS/BRAND-BRAINS/ + encadenado al ecosistema Golden completo.

## 🔄 AUTO-MEJORA (mandato global — autorización permanente de FER)
Al cerrar cada corrida real: 1) **auto-califícate** (1–1000, honesto, con evidencia) contra el
criterio de calidad de esta skill; 2) toda lección que sea de SISTEMA se **hornea aquí** con el
ritual (backup → desbloquear → arreglar → changelog+sello → re-blindar); 3) si detectas un hueco
propio, **arréglalo sin esperar que lo pidan** e informa; 4) pasa `golden-skill-auditor`
periódicamente. Nunca borres conocimiento: reorganiza y añade.

- **2026-08-02** — LOOP DEL ARSENAL (semana 1, skills de negocio): se hornea la sección **AUTO-MEJORA** (mandato global de FER, autorización permanente). Sin esta sección la skill no se auto-calificaba al cerrar corrida. Contenido operativo intacto. Backup: `_backups/2026-08-02-loop-arsenal-s1/`.
