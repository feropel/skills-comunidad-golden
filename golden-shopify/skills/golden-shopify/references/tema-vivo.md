# PROTOCOLO TEMA VIVO + MEDIA (version completa)

El resumen duro de 9 puntos vive en `SKILL.md` y es obligatorio ANTES de escribir a cualquier tema.
Aqui esta el detalle con el porque de cada punto y los casos reales que lo originaron.

1. **Verificar QUÉ tema es MAIN antes de tocar nada** (`{themes{nodes{name role id}}}`): el tema
   vivo puede cambiar entre sesiones sin aviso (pasó: otro chat publicó Dawn y los parches se
   estaban subiendo al borrador). Nunca asumir el tema por memoria.
2. **Escritura fiable**: `themeFilesUpsert` con body `{type:"BASE64"}`; tras escribir, RELEER el
   archivo y comparar contenido (no fiarse del OK ni del tamaño). Una sola sesión escribe por tema.
3. **Caché del storefront**: tras cambiar plantillas o media, la página pública puede servir el
   render VIEJO 15-60 min (por URL, incluso con cache-buster). Si un fix "no aparece": verificar
   el ARCHIVO del tema, no re-subir a ciegas; esperar la purga.
4. **Borrar media de producto = romper URLs**: los product media viven en `/files/` y otros
   consumidores los incrustan (plantillas, constructores, config de upsells de Releasit, renders
   cacheados). ANTES de borrar: inventariar referencias y reemplazarlas; el archivo borrado se
   puede rescatar del caché del CDN re-subiéndolo con el MISMO filename (la URL revive).
5. **Galería estándar Golden**: mínimo 5 imágenes por producto, TODAS cuadradas 1:1 (portada
   packshot + tarjetas de beneficios + macros; reutilizables entre productos de la familia).
   La portada va posición 1 en Admin (colecciones/búsqueda); si el tema trae
   `galeria_portada_al_final` (Dawn Golden), la ficha abre con los creativos y el packshot
   cierra — es diseño aprobado, NO "corregirlo".
6. **CSS prohibido**: jamás `html,body{overflow-x:clip}` (clip contagia el otro eje y MATA el
   scroll vertical). Un desborde horizontal se arregla en el elemento culpable (ej. ticker
   marquee con `overflow:hidden;max-width:100%`), nunca en html/body.
7. **Sticky/Releasit**: nunca desactivar el Sticky Bar en el panel de Releasit (rompe el botón en
   silencio); se oculta por CSS (`_rsi-buy-now-button-floating`) y toda ficha conserva SIEMPRE un
   CTA fijo propio. Probar el botón DE VERDAD (abrir el modal), no solo que exista.
