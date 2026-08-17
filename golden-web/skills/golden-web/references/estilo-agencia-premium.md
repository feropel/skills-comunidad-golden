# Estilo Agencia Premium — receta Golden

Destilado 2026-07 de una agencia creativa de referencia (textura.agency, estudio con menciones Awwwards). La referencia se analizó a nivel de código (HTML crudo, CSS, chunks JS) y desaparece: esto es una RECETA Golden replicable para cualquier cliente, no una copia. Prohibido reutilizar sus textos, marca o assets.

## 1. El diagnóstico — por qué se siente "carísima"

Siete mecanismos concretos, verificados en el código:

1. **Contraste tipográfico extremo**: serif display clásica en peso 400 para titulares GIGANTES (11vw a 18vw el wordmark del hero) + sans en pesos ULTRA livianos (100 y 300) para el cuerpo. Ese choque serif-enorme vs sans-pluma ES el look; no hay bold en ningún lado.
2. **Física de resorte en el texto, no fades**: cada titular se parte en letras/palabras y cada pieza entra con un resorte físico independiente (tension 120-280, friction 12-26, mass 1). El texto "aterriza amortiguado" — se percibe como materia, no como opacidad.
3. **Un solo gradiente firma sobre casi-negro**: fondos #050505/#0f0f0f/#1d1d1d y UN acento repetido con cuentagotas: `linear-gradient(241deg, #FFAB98 -68%, #A1ECFF 155%)` (durazno → azul hielo). Todo lo demás es blanco, gris y aire. Proporción real: ~90% fondo oscuro, ~8% texto claro, ~2% acento.
4. **Video como textura, no como contenido**: video de fondo en streaming adaptativo (hls.js, master.m3u8) en el hero, y un video POR servicio con variante desktop y mobile — siempre `muted loop playsinline` con `translateZ(0)`. La página respira sola sin que nada "reproduzca".
5. **Scroll con inercia global (Lenis)** + reveals ligados al progreso de scroll. Nada aparece de golpe; todo llega frenado.
6. **Copy de una frase con voz humana**: saludo inesperado como hook, UNA frase de misión emocional, servicios en 1-2 palabras, y un único CTA repetido de principio a fin ("agenda una reunión", no "contáctanos"). Cero párrafos de relleno.
7. **Prueba social de élite comprimida**: contadores que suben (años, proyectos, satisfacción), logos de clientes, y premios con año (Awwwards). Números y nombres, no testimonios largos.

Extras que suman: `mix-blend-mode: difference` en nav/cursor sobre cualquier fondo, tarjetas de vidrio con `backdrop-filter: blur(10px)`, y labels de links apilados en triple para el hover de "rodillo" (el texto rueda hacia arriba y entra su gemelo).

## 2. Stack técnico detectado (y su equivalente Golden)

| Referencia | Qué hace | Cómo lo logramos nosotros |
| --- | --- | --- |
| Next.js + styled-components | base SPA con SSR | Next + Tailwind (nuestro stack estándar) |
| Lenis | smooth scroll con inercia | `lenis` (npm, gratis) — 3 líneas de init |
| Motor propio de texto con springs (split en líneas/palabras/letras) | titulares que entran con física | skill `gsap` (SplitText-like manual + stagger) o skill `animejs` (spring easing + stagger por letra); criterio físico con `emil-design-eng` y `apple-design` |
| Hook propio de scroll-trigger | reveals mapeados a scroll | skill `gsap` (ScrollTrigger, `scrub`) o IntersectionObserver + skill `waapi` |
| hls.js + videos por sección | video adaptativo de fondo | mp4/webm cortos optimizados (HLS solo si el video pasa de ~15s); HyperFrames para generarlos |
| Swiper | carruseles de trabajos | Swiper (gratis) o scroll-snap CSS con skill `css-animations` |
| next/font (Google fonts self-host) | fuentes sin FOUT con fallback `size-adjust` | igual: next/font o @font-face self-host con fallback ajustado |
| Sin GSAP, sin three.js en la home | el 3D vive en subsitios de proyectos | lección: la home puede sentirse "wow" SIN WebGL — tipografía + springs + video bastan; skill `three` solo si el proyecto lo amerita |

Auditoría de movimiento de un build ya hecho: skill `improve-animations`. Para nombrar un efecto exacto al pedirlo: `animation-vocabulary`.

## 3. Tokens de diseño (receta)

**Tipografía**
- Display: serif clásica peso 400 (Gilda Display en la referencia; equivalentes libres: Playfair Display, Cormorant, Fraunces). SOLO peso 400 — el tamaño da la fuerza, no el bold.
- Cuerpo: sans geométrica/humanista en pesos 100-300-400 (Lato en la referencia; equivalentes: Inter con weight 300, Figtree Light). Nunca 600+.
- Escala: H1 hero `clamp(4rem, 11vw, 12rem)`; wordmark/momento firma hasta `18vw`; cuerpo 16-18px; labels 12-14px en mayúsculas con tracking.
- line-height del display: 0.9-1.0. Aire alrededor: mínimo 40% de la sección vacía.

**Color (modo oscuro por defecto)**
- Fondos: `#050505` base, `#0f0f0f` y `#1d1d1d` para capas/tarjetas.
- Texto: `#ffffff` titulares, `rgba(255,255,255,.6-.8)` cuerpo.
- Acento: UN gradiente de dos tonos complementarios cálido→frío, tipo `linear-gradient(241deg, TONO_CALIDO -68%, TONO_FRIO 155%)`. Se adapta a la marca del cliente (regla Golden: dorado solo si es su marca). Usos permitidos: texto clave con `background-clip: text`, un borde, un glow. Jamás bloques enteros.
- Vidrio: `rgba(255,255,255,.05-.1)` + `backdrop-filter: blur(10px)` + borde 1px translúcido.

**Espaciado y layout**
- Secciones de 100vh o cerca; una idea por pantalla.
- Grillas simples de 2-3 columnas; el resto es tipografía a lo ancho.
- Nav mínima (4-5 links) fija con `mix-blend-mode: difference` para que viva sobre claro y oscuro.

## 4. Estructura de secciones recomendada (agencia/estudio/servicio premium)

1. **Hero**: saludo hook (1-3 palabras inesperadas) → wordmark o titular gigante (11-18vw) → UNA frase de misión emocional → CTA "Agenda una reunión" → lista de servicios en palabras sueltas. Fondo: video textura o efecto Golden (Aurora/Nebulosa).
2. **Trabajos destacados**: 3-6 casos con video/imagen grande en hover, link "todos los trabajos".
3. **Servicios**: 3-4 bloques, titular de 1-2 palabras + párrafo de 2-3 líneas + media propia por bloque.
4. **Manifiesto**: una sola declaración larga que se revela palabra por palabra al hacer scroll, con una palabra clave en el gradiente firma (es el momento editorial de la página).
5. **Stats**: 4 contadores que suben al entrar en viewport (años, proyectos, satisfacción, %). Datos SIEMPRE reales (regla Golden).
6. **Equipo**: líder destacado + roster por rol. Nombres humanizan la agencia.
7. **Clientes + premios**: logos y reconocimientos con año. Compacto.
8. **Footer CTA**: repetir el titular gigante ("hablemos") + el MISMO CTA del hero + redes + email. El footer es un segundo hero, no una lista de links.

Regla de conversión: UN solo CTA en toda la página (agendar reunión) repetido en hero, nav y footer. Nada de formularios largos: botón directo a agenda (encaja con `golden-agenda-citas`).

## 5. Capa de movimiento — checklist de implementación

- [ ] Lenis activo (inercia global) + `prefers-reduced-motion` lo desactiva.
- [ ] Titulares split por palabra/letra con entrada de resorte escalonada (stagger 20-40ms). Springs: tension ~170-280, friction ~14-26 (traducción CSS: `linear()` spring o easing `cubic-bezier(.22,1,.36,1)` + overshoot leve).
- [ ] Links con hover "rodillo": dos copias apiladas del label, `translateY` al 100% al hover.
- [ ] Reveals por sección ligados al scroll (no solo al entrar: mapeados al progreso).
- [ ] Contadores animados en stats.
- [ ] Un momento sticky/cinemático (manifiesto o trabajos).
- [ ] Video de fondo muted/loop/playsinline con póster y variante móvil liviana.
- [ ] Solo se anima `transform`/`opacity`; canvas y video se pausan fuera del viewport.

## 6. Fórmula de copy

`[Saludo hook inesperado]` + `[Frase de misión: verbo emocional + a quién sirves + qué logras]` + `[Servicios en 1-2 palabras cada uno]` + `[CTA de agenda]`.

Patrón de la misión: "Hacemos X para Y — para que [efecto emocional en 3 verbos]". Corta, en primera persona plural, con un guion largo que parte la frase. El resto de la página son fragmentos: nada supera 3 líneas salvo el manifiesto.

## 7. Cuándo usar esta receta

Perfil Empresa/Creador de golden-web cuando el cliente vende servicios creativos, tecnología o marca personal premium y el objetivo es AGENDAR (no vender catálogo). Combina con: dirección GOLDEN LUXURY (paleta), EFECTOS GOLDEN (hero), Golden Cinemática 3D solo si el presupuesto/marca lo amerita. Para COD/producto sigue mandando golden-shopify.
