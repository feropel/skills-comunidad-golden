# Anatomía del hook: cómo se escribe el primer segundo

Destilado 2026-08-27 por el chat FILTRO de `00_CONTEXTO_MAESTRO.md` (Agente Generador de Hooks
v1.3), que FER trajo el 27-ago. **Del documento se toma el MÉTODO de escritura; no se trae su
pipeline de video** (Gemini + Seedance + ElevenLabs, ~1,52 USD por set), que no está montado en
el Mac y es otra discusión.

**Hueco medido antes de escribir esto:** `golden-ads` ya sabe MEDIR el hook (17 menciones de
*hook rate*, 15 de *hold rate*), pero esta skill, que es la que los ESCRIBE, tenía **0 menciones**
de scroll-stop, snapback, context lean, trigger words, la regla de los 3 segundos y el dato de que
la mayoría los ve sin sonido.

## Por qué esto pesa tanto

| Dato | Fuente |
|---|---|
| 73% de los video ads de ecommerce fallan en los primeros 3 s | Motion 2025 |
| 90% abandona si no enganchas en 3 s | Sovran / Zeely |
| 90% del recuerdo del anuncio se captura en los primeros 6 s | TikTok for Business |
| 80% del rendimiento del anuncio viene del hook | Xwork / Callaway |
| **85% de las vistas en Meta son SIN SONIDO** | — |
| 88% de usuarios de TikTok dicen que el sonido es vital | — |

Las dos últimas juntas dan la regla operativa: **texto quemado en pantalla siempre, y voz que
funcione sola**. El hook tiene que entenderse mudo y tiene que entenderse a ciegas.

El algoritmo además castiga el abandono temprano con menos entrega y CPM más alto, así que un hook
flojo no solo convierte peor: **encarece todo lo demás**.

## Los 4 componentes (y cuál manda)

Un hook no es una frase. Son cuatro cosas que deben decir **lo mismo** dentro de una variante y ser
**distintas** entre variantes:

1. **Visual** — lo que se ve en el primer fotograma y los 2-3 s siguientes
2. **Hablado** — lo que dice quien aparece
3. **Texto en pantalla** — el rótulo quemado
4. **Ambiente** — luz, ritmo, música, tipografía

> *"Los ojos procesan de 10 a 100 veces más información por segundo que los oídos. El espectador
> no escucha el video: primero VE, después oye, y vuelve al visual a confirmar."*

**Implicación para escribir:** primero se decide **qué se va a ver**, y el guion se escribe alrededor
de ese visual. Escribir la frase primero y buscarle imagen después es el orden equivocado.

## La fórmula de 3 pasos (la plantilla canónica)

```
1 · CONTEXT LEAN (1-2 líneas)
    De qué va el video + terreno común, dolor o metáfora

2 · SCROLL-STOP (1 línea)
    Palabra de contraste: "pero", "mira esto", "espera", "lo loco es"
    Es el SETUP, no el golpe

3 · CONTRARIAN SNAPBACK (el golpe)
    Frase OPUESTA a lo que abriste. Sigue en tema, pero pivota al espectador.
    Cuanto mayor el contraste, mayor el efecto.
```

Ejemplo real (8 millones de vistas):
> **Lean:** "La tecnología del Vegas Sphere es brutal, la pantalla más grande del mundo."
> **Scroll-stop:** "Pero mira esto:"
> **Snapback:** "La pantalla es lo MENOS impresionante. El audio te va a volar la mente."

**Tope duro: `context_lean` + `snapback` juntos ≤ 14 palabras.**

## Los 4 ángulos × 6 formatos

El **ángulo** define qué emoción dispara. El **formato** define qué promesa narrativa hace.
Son ortogonales: cualquier ángulo se ejecuta en cualquier formato.

| Ángulo | Emoción | Cuándo |
|---|---|---|
| **A · Shock visual** | sorpresa | audiencia saturada |
| **B · Pregunta-problema** | identificación | el dolor está claro |
| **C · Resultado por delante** | deseo | hay transformación visible |
| **D · Confesión íntima** | confianza | producto sensible o testimonial |

| Formato | Promesa |
|---|---|
| **Adivino** | presente contra futuro |
| **Experimentador** | "lo probé 30 días y mira" |
| **Maestro** | "tres cosas que aprendí" |
| **Mago** ⭐ | "mira esto" + visual rápido (se combina con cualquiera) |
| **Investigador** | "nadie habla de esto" |
| **Contrario** | "estás haciendo X mal" |

**Para Golden el default es `A · Shock × Mago`**, que es el que el documento asigna a *COD impulse
LatAm* — el negocio exacto de la casa. Le'côterra y cuidado personal admiten además
`C · Resultado × Experimentador`, que es el de mayor tasa esperada.

## Palabras que disparan, y las prohibidas

| Categoría | Ejemplos |
|---|---|
| Pérdida | **estafa** (la más fuerte según Dara Denney), desperdiciado, quebrado |
| Identidad | POV, si eres, para ti que, mamás como tú |
| Tiempo | en X minutos, mientras duermes, en X días |
| Autoridad | secreto, nadie habla de, por qué nadie me dijo |
| Cifras | $X al día, X g de proteína, X% menos |
| Corte verbal | pero mira esto, espera, lo loco es |

**Prohibidas** (el cerebro las filtra como ruido publicitario): mejorar, crecimiento, mejor,
increíble, "hola chicos", "el mejor de todos".

⚠️ **Las coloquiales cambian por país.** "La neta" es México, no Colombia. En una skill que trabaja
7 países, la palabra familiar se elige por mercado o no se usa.

## Los cinco controles antes de dar un hook por bueno

1. **Filtro de 4 errores** — *Demora*: ¿el tema está en la primera frase? · *Confusión*: ¿lo
   entiende alguien de sexto grado? · *Irrelevancia*: ¿habla de "tú" y no de "yo"? · *Desinterés*:
   ¿hay contraste?
2. **Un solo sujeto, una sola pregunta** — si alguien puede malinterpretar de qué va, o si deja
   varias preguntas abiertas, se reescribe.
3. **Alineación de los 4 componentes** — coherentes dentro de la variante, distintos entre variantes.
4. **Palabra disparadora** — al menos una, y ninguna de las prohibidas.
5. **Leerlo en voz alta tres veces** — si suena forzado, se reescribe.

## Reglas duras

- Los 4 ángulos se cubren en orden A → B → C → D
- Cada variante en **locación distinta**
- Ninguna frase copia textualmente la del anuncio original
- **Ningún hook lleva CTA** ("compra ya", "haz clic"): el hook abre, no cierra
- El producto aparece **solo en el ángulo C**

## Dónde encaja con el resto del ecosistema

- **`golden-ads` ya tiene las reglas de matar** que cierran este ciclo: *hook rate* por debajo de
  30% en Meta o 35% en TikTok se mata, y *hold rate* por debajo de 20% también. No se espera al
  ROAS. Esta skill escribe el hook; `golden-ads` decide si vivió.
- **Andromeda, y esto es lo importante:** el documento pide que los 4 componentes sean distintos
  entre variantes "porque Meta marca duplicados". Es la misma ley que `golden-ads` documenta en
  `23-salud-de-senal-y-andromeda.md`: **más de 60% de similitud dentro de un conjunto provoca
  supresión**. Cuatro hooks del mismo ángulo con otras palabras cuentan como **uno**. Por eso los
  ángulos se cubren en orden y no se repiten.
- **`golden-matriz-viral`** trabaja los ángulos de video; esta fórmula es el molde de la frase.
- **`golden-video-editor`** ejecuta el corte: su `multicamara-una-camara.md` pide cambio de encuadre
  cuando cambia la idea, y aquí el dato que lo aterriza al hook es que **el primer corte va entre
  0,8 y 1,2 segundos** y luego un cambio visual cada 1,5-3 s durante los primeros 12.

## Lo que NO se trajo, y por qué

El documento original describe un pipeline que **genera** los 4 videos: Gemini analiza el anuncio,
Gemini img2img fabrica los fotogramas, Seedance los anima, ElevenLabs pone la voz y ffmpeg
ensambla. Cuesta ~1,52 USD por set y tarda 6-10 minutos.

**Nada de eso está instalado en el Mac** (ni la skill `hooks-agent`, ni los helpers, ni el `.env`
con las llaves de Kie y Gemini). Y buena parte de lo que hace ya lo cubren `golden-imagen-arena`
(imagen por API, incluida Seedance vía el MCP de Higgsfield), `golden-ugc-avatar` (voz y avatar) y
`golden-video-editor` (ensamble). **Montarlo entero sería duplicar tres skills.**

Lo que no está cubierto y sí valdría evaluar aparte: **cortar el hook viejo de un anuncio que ya
funciona y pegarle uno nuevo**, que es una operación de ffmpeg sobre metraje propio. Eso es
`golden-video-editor`, no esta skill.
