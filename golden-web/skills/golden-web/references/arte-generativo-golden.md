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
- Templates originales de la skill rescatados en `arte-generativo-templates/`.
