# Auto-verificación de cierre (correr ANTES de entregar)

Objetivo: que los errores que ya pasaron (rating 0.0, color viejo, sin sello, JSON roto)
sean IMPOSIBLES de entregar. Correr este script sobre el `product.json` generado.

⚠️ **G4.2 — verificación OBLIGATORIA en cada entrega:** el check 21 mide cada valor
`custom_liquid` del template en **bytes UTF-8** (no caracteres) y FALLA si alguno llega a
50.000 — el tope duro de Shopify en todos los temas. Sin pasar ese check, no se entrega.

_(el codigo vive en `scripts/autocheck.py`)_

Además, **SIEMPRE** (REGLA VISUAL — el JSON válido NO garantiza que se vea bien):
- [ ] **Vi la página renderizada** (screenshot), no solo el JSON. Prohibido decir "100/100" sin verla.
- [ ] País correcto en tiempos de entrega (Guatemala 1-4 / Colombia 3-7 — ver `paises-entrega.md`).
- [ ] Armonía de paleta (máx 2 colores fuertes, 1 acento de urgencia).

### Procedimiento de RENDER REAL (repetible, obligatorio antes de "listo")
El script de arriba es estático (regex/JSON): NO ejecuta Liquid ni ve el layout. Por eso, tras pasarlo:
1. **Sube el `product.json` a un tema NO publicado** (ej. el tema `golden` en Dawn, unpublished) con
   `themeFilesUpsert` por el MCP de Shopify → así no tocas la tienda en vivo.
2. **Abre el preview** (`preview_theme_id` / link de vista previa del tema) del producto real.
3. **Verifica en los 3 escenarios SIEMPRE — MÓVIL (~390px), TABLET (~768px) y PC (~1440-1920px)** (regla
   del usuario G3.16: "perfecto en todos los escenarios"; viewport del navegador, `preview_resize` o capturas
   independientes por dispositivo). En CADA tamaño: sin scroll horizontal, nada cortado ni encogido, y todo
   overlay `position:fixed` ocupa el viewport completo (`getBoundingClientRect()` = `innerWidth×innerHeight`,
   nunca un "cuadrito" — si falla, re-parent al body, ver tabla de errores):
   - El **CTA verde sobresale** al primer vistazo (REGLA #2); sticky visible al hacer scroll.
   - **FAQ:** abre/cierra con teclado (Tab + Enter) y el foco se ve (anillo). Lee bien con lector.
   - **Sin saltos de layout** (CLS) al cargar imágenes; nada tapado por el sticky/WhatsApp.
   - Ninguna sección vacía ni con placeholder `[...]` visible (REGLA #3/#4).
   - **INTRO IGNITION (ciclo de vida completo)**: con recarga limpia (borrar `gfs_ign_seen` del
     sessionStorage) el intro APARECE y a los ~3s DESAPARECE del DOM (`querySelector` = null).
     Probar también abriendo la pestaña en segundo plano (ahí es donde históricamente quedaba montado).
   - **IMÁGENES QUE ENCAJAN (G3.15)**: cada imagen llena su recuadro SIN cortar contenido — verificar
     `naturalWidth/naturalHeight` vs el ratio del contenedor. Infografías con TEXTO QUEMADO jamás van
     en slots con `object-fit:cover`: o crop fotográfico exacto al ratio del slot, o imagen completa a
     proporción natural (`height:auto`). El copy vive en el HTML, no dentro de la imagen.
4. **Screenshot** de la página completa (móvil) como prueba. Sin ese screenshot, NO es "listo".
> Un render headless 100% automático depende de una tienda/preview Shopify en vivo (es del entorno,
> no del archivo de skill): por eso este procedimiento es la forma correcta de cerrarlo cada vez.
