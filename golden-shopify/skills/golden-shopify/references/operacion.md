# Operación y mantenimiento de la skill

Detalle de 3 flujos que en SKILL.md van resumidos: actualizar páginas, el sello/nota,
y el ritual de auto-mejora.

## A) Modo actualización (UPGRADE PASS)
Cuando el usuario tenga un `product.json` ya generado y pida ponerlo al día con la
skill (ej. *"actualiza este JSON a la última versión de la skill"*), hacer:
1. **Parsear** el JSON (quitar comentario `/* */`, `json.loads(strict=False)`).
2. **Leer su sello** `GFS_VERSION` (config center). Si no tiene sello, es pre-v1.7.
3. **Diff contra la skill actual** (changelog + reglas + componentes). Detectar qué le
   falta de cada versión posterior a la suya. Checklist mínima de upgrade:
   - Botón flotante WhatsApp (`whatsapp-flotante.liquid`) si el número existe.
   - Modo sin distracciones (`landing-sin-distracciones.liquid`) si aplica.
   - REGLA #2: el botón de compra sobresale y es verde `#1D9E06` (no igual al WhatsApp).
   - País correcto en barra logística / tiempos de entrega (`paises-entrega.md`).
   - Calificación real (`RATING_VALUE`/`REVIEW_COUNT`), nunca 0.0/5.
   - Diferenciación (REGLA #1), completitud (REGLA #4) y sello actualizado.
4. **Aplicar SOLO lo que falta**, sin romper copy/contenido/diseño que ya funciona ni
   cambiar el producto. Respetar la convención EDITAR/NO TOCAR.
5. **Subir el sello** `GFS_VERSION` a la versión actual.
6. **Entregar UN solo archivo** y listar en una línea qué se actualizó.
Antes de entregar, correr `checklist-producto.md`.

## B) Sello de versión + NOTA INTERNA (obligatorio en cada página)
Toda página generada DEBE llevar:
1. **Sello arriba** (config center): `GFS_VERSION` + comentario HTML
   `<!-- Generado con GOLDEN SHOPIFY vX.Y · marca · fecha -->`. Pon la **versión
   actual** (tope de `changelog.md`).
2. **Nota interna al FINAL** (dentro del ÚLTIMO bloque, p.ej. el sticky), comentario HTML
   invisible para el cliente:
   ```html
   <!-- ════════ NOTA INTERNA (no visible para el cliente) ════════
        Generado: AAAA-MM-DD HH:MM (hora local) · GOLDEN SHOPIFY vX.Y · <producto>
        ════════════════════════════════════════════════════════════ -->
   ```
Reglas:
- Fecha y hora **FIJAS** del momento real de generación (NO `{{ 'now' | date }}`: eso marca
  cuándo el cliente abre, no cuándo se generó). Obtener la hora real del entorno al construir.
- La nota va **dentro** del último bloque como `<!-- -->`. NUNCA después del `}` final (rompe JSON).
- No afecta diseño/SEO/rendimiento; solo se ve en "Ver código fuente".
- Al subir versión de la skill, actualizar `GFS_VERSION` por defecto en
  `assets/config-center.liquid` y `componentes/00-config-center.liquid`.

## C) Auto-mejora — RITUAL DE ABSORCIÓN
Cuando el usuario diga *"absorbe las mejoras de esta página"*, *"métele esto a la skill"*,
o pegue/señale un `product.json` que le gustó:
1. **Parsear** ese JSON (`json.loads(strict=False)`).
2. **Diff contra la skill** (`product.base.json` + `componentes/`): identificar lo NUEVO o MEJOR.
3. **Extraer** cada pieza como `componentes/<nombre>.liquid` (convención EDITAR/NO TOCAR), o
   snippet en `efectos-premium.md`, o asset suelto.
4. **Si mejora la base**, actualizar `assets/product.base.json`.
5. **Documentar** en `arquetipos.md` (si es patrón) y SIEMPRE **subir versión en `changelog.md`**.
6. **No duplicar:** mejorar lo existente, no crear otro componente para la misma función.
7. Confirmar al usuario en una línea qué se absorbió y la nueva versión.

Reglas del ritual:
- Nunca degradar lo que funciona; solo añadir/mejorar. Un solo componente por función.
- ⚠️ **NUNCA reintroducir nombres reales** de productos/marcas/tiendas (la skill es anónima
  para compartir, ver v1.17). Usar **descriptores de categoría** ("gadget perfumador", "sérum
  facial", "tienda demo"). Tras absorber, verificar con `grep -riE 'nombre-real' <skill>` → 0.
