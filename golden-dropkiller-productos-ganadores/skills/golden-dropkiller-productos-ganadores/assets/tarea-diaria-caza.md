# Prompt de la rutina diaria de caza (modo RUTINA)

Este archivo es el texto que se pega como prompt de la tarea programada. **La tarea solo se
crea con un sí explícito del usuario en el chat**, con hora, país y destino confirmados: es
configuración persistente. Antes de crearla, correr la rutina UNA vez a mano con este mismo
prompt y comprobar que dejó el archivo de salida (una rutina se prueba por su ARTEFACTO y su
duración, no por el "succeeded" del programador).

Valores que se reemplazan al crearla: `<PAIS>` (CO por defecto), `<N>` (10), `<NICHOS>` (todos),
`<MODELO>` (catálogo COD).

```
Usa la skill golden-dropkiller-productos-ganadores en modo RUTINA. No muestres el menú: el preset es este.
País <PAIS> · plataforma DROPI · nichos <NICHOS> · modelo <MODELO> · <N> productos · etapa
VALIDACIÓN (100 a 3.000 ventas en CO) · ritmo 7 días 31 o más (prudente; el piso medido es 10) · anuncios validados y evergreen ·
proveedores hasta el tope del país (CO 5, MX 4, GT y PE 2; heredados) · canal el más libre · stock mínimo 80 · rutas R1 a R6.

1. Antes de la primera llamada a DropKiller, lee references/dropkiller-caza.md.
2. Si no aparece la herramienta find_winning_products del conector DropKiller, NO sigas con
   otra fuente: escribe en el archivo de salida "SIN CONECTOR DROPKILLER EN LA RUTINA" con la
   hora, y termina. Una lista sin DropKiller no es la lista que se pidió.
3. Corre el embudo completo de la sección 6 EN LOTE: una carpeta por candidato y
   scripts/correr_lote.py <corrida> --pais <PAIS> --precios --registro
   PROYECTOS/CAZA-DIARIA-GANADORES/_registro.jsonl --entrega-golden
   PROYECTOS/CAZA-DIARIA-GANADORES/_entrega_golden.json. Anunciantes por imagen + descripción
   (semantic_search_ads), nunca la imagen sola. Nunca cifras crudas. Cobertura: todos los
   candidatos y las 6 rutas, o se declara cuál faltó y por qué.
4. Antes de armar la lista, lee las listas de los últimos 7 días en
   PROYECTOS/CAZA-DIARIA-GANADORES/ y marca los repetidos con el cambio de sus ventas.
5. Escribe la LISTA DE CAZA (references/entregable.md §7) con la herramienta Write en
   PROYECTOS/CAZA-DIARIA-GANADORES/<AAAA-MM-DD>-<PAIS>.md. El texto va en el archivo, nunca
   dentro de un comando de shell.
6. Si pasan menos de <N>, entrega los que pasen y di qué ruta se agotó. No rellenes.
7. SEGUIMIENTO (cierra el ciclo): para cada línea de PROYECTOS/CAZA-DIARIA-GANADORES/_registro.jsonl
   con fecha de hace 30 días, guarda get_product_history desde esa fecha en
   PROYECTOS/CAZA-DIARIA-GANADORES/_seguimiento/<dropi_id>.json y corre
   scripts/seguimiento.py _registro.jsonl _seguimiento --dias 30. Si dice "los filtros NO
   separan", dilo arriba de la lista: los umbrales hay que recalibrarlos (references/calibracion.md).
8. Termina con un resumen de 3 líneas: los 3 primeros, el fantasma más grande que descartaste
   y cuántos candidatos entraron al embudo.
```

## Por qué cada paso

- **Paso 2:** una rutina que "funciona" con la fuente equivocada es peor que una que falla: nadie
  revisa de dónde salió la lista. Los conectores de claude.ai pueden no estar disponibles en una
  sesión programada; eso se descubre en la corrida de prueba, no se supone.
- **Paso 4:** un producto que repite día tras día y crece es la mejor señal de la semana, y lo
  único que la rutina ve y una búsqueda suelta no.
- **Paso 5:** los comandos de shell con un informe adentro revientan el analizador de permisos y
  la rutina se queda pidiendo permiso en cada corrida (ley de escritura de la casa).
