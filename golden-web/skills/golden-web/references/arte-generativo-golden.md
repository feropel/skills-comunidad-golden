# Arte generativo para fondos y efectos Golden (rescatado de algorithmic-art, 2026-07-13)

Para piezas de la GALERÍA GOLDEN (/galeria: fondos y efectos por nicho) y canvas decorativos de webs premium.

## Método (2 fases)
1. **Filosofía algorítmica** (antes de codear): nombra el "movimiento" (1-2 palabras, ej. "Turbulencia Dorada"), escribe 3-4 líneas de qué expresa mediante procesos computacionales: comportamiento emergente, belleza matemática, caos controlado.
2. **Código p5.js**: 90% generación algorítmica / 10% parámetros esenciales. SIEMPRE con `randomSeed(s)` + `noiseSeed(s)` para reproducibilidad — la misma semilla regenera la misma pieza; variar semilla = variaciones infinitas de la misma identidad.

## Bloques que funcionan
- **Flow fields**: `noise(x*esc, y*esc)` → ángulo → partículas que siguen el campo (los fondos "orgánicos").
- **Sistemas de partículas** con fuerzas (atracción/repulsión a puntos dorados).
- **Variación paramétrica**: exponer 3-5 sliders máximo (densidad, escala de ruido, paleta, velocidad).
- Paleta Golden: #e8b84b / #f7e3a1 / #b8860b sobre #060606 (o marfil #f2ecdf en modo día).

## Reglas Golden
- Canvas theme-aware: leer `document.documentElement.classList.contains('day')` en el loop.
- NO atar animación decorativa a prefers-reduced-motion (lección barra GOLDEN GROUP).
- Toda pieza nueva entra como tarjeta en /galeria (regla de FER).

## Cómo usar los templates (`arte-generativo-templates/`)

Dos archivos de arranque, léelos SOLO cuando vayas a construir una pieza generativa nueva (no en cada invocación de golden-web):

- **`generator_template.js`** — el esqueleto de un sketch p5.js puro (sin UI): organización de
  `params`, semilla reproducible (`randomSeed`/`noiseSeed`), ciclo de vida `setup()/draw()`,
  estructura de clase `Entity` para sistemas de partículas/agentes, utilidades (mapeo, easing,
  exportar PNG). Úsalo como checklist de estructura cuando el efecto vaya embebido directo en la
  web (sin panel de controles separado) — copia los bloques que apliquen a TU algoritmo, no lo
  pegues entero: los métodos vienen vacíos a propósito ("fill this in"), son puntos de partida,
  no una pieza terminada.
- **`viewer.html`** — visor standalone con sidebar de controles (semilla, sliders de parámetros,
  color pickers) + canvas p5.js, para cuando el cliente/alumno quiere EXPLORAR variaciones de la
  pieza (probar semillas, mover sliders) antes de fijar la versión final que va embebida en la
  web. Ya trae la paleta Golden en `:root` (`--golden-dark/--golden-light/--golden-gold...`,
  ver arriba) y el patrón de navegación de semilla (Prev/Next/Random) — mantenlos. Personaliza
  título, parámetros y el algoritmo (`initializeSystem`, `generateFlowField`, `draw`, clase
  `Particle`) para la pieza real; si la pieza es para un cliente con marca propia, sustituye el
  acento dorado por su color de marca (dorado solo si es la marca del cliente).

Ambos se rescataron de una skill base de arte generativo y llevan la paleta y el idioma
adaptados a Golden — si alguna vez ves un token o comentario en inglés/Anthropic que se coló de
nuevo (por edición futura descuidada), corrígelo antes de usar el archivo como base de un
entregable de cliente.
