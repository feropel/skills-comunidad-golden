# Marca blanca — un bloque de tokens cambia toda la identidad

Toda la identidad del deck vive en el bloque `:root` de `assets/deck-base.html`. No se
toca nada más. Ese es el mecanismo que permite entregar el mismo motor a un cliente, a la
comunidad y a la marca personal de FER sin reescribir una línea del motor.

## Índice
1. El bloque que se rellena
2. Los 4 perfiles de Golden
3. Cómo se saca la paleta de un cliente
4. Tipografía
5. Reglas de marca blanca

## 1 · El bloque que se rellena

```css
:root{
  --bg:        #07080B;   /* fondo del lienzo, detrás de las láminas */
  --surface:   #10131A;   /* fondo de la lámina */
  --ink:       #F4F6FB;   /* texto principal */
  --muted:     #8B93A7;   /* texto secundario */
  --accent:    #FFC637;   /* acento de marca: cifras, viñetas, CTA */
  --accent-2:  #6CCFFF;   /* acento secundario, uso escaso */
  --line:      #232833;   /* bordes y retícula */
  --curtain:   #FFC637;   /* barra del preloader */
}
```

## LA LISTA COMPLETA · se sustituyen TODOS, no los obvios

Este es el fallo medido el 2026-09-03: un deck del Cartel del Chat salió con el acento
correcto pero **chasis gris ajeno**, porque solo se cambiaron 4 tokens y quedaron de fábrica
`--surface`, `--muted`, `--line` y `--curtain` (que seguía amarillo Golden). Y la tipografía
se quedó en Georgia serif, que es lo contrario de lo que pedía la marca.

**Checklist. Si uno se queda de fábrica, el deck lleva marca ajena.**

| Token | Qué pinta | Se olvida a menudo |
|---|---|---|
| `--bg` | Fondo del lienzo, detrás de todo | |
| `--surface` | **Fondo de cada lámina** | 🔴 sí, y es media pantalla |
| `--ink` | Texto principal | |
| `--muted` | **Texto secundario, etiquetas, pies** | 🔴 sí |
| `--accent` | Cifras, viñetas, CTA, tiñe la atmósfera | |
| `--accent-2` | Acento secundario, tiñe la atmósfera | 🔴 sí |
| `--line` | **Bordes, retícula, separadores** | 🔴 sí |
| `--curtain` | Barra del preloader | 🔴 sí, se queda amarillo Golden |
| `--font-display` | **Titulares** | 🔴 sí, se queda en Georgia |
| `--font-body` | Cuerpo de texto | |
| `--font-mono` | Microtipografía, contadores, etiquetas | |
| `--vidrio` | Opacidad de la lámina sobre el fondo (72% por defecto) | |
| `--logo-alto` / `--logo-alto-portada` | Tamaño del logo | |

Comprobación de un vistazo, antes de dar por buena la marca:

```bash
grep -E "^\s+--(bg|surface|ink|muted|accent|accent-2|line|curtain|font-display):" deck.html
```

Si alguno sigue con el valor de la tabla de abajo (`#10131A`, `#8B93A7`, `#232833`,
`#FFC637`, `Georgia`), **no se cambió**.

## El logo, que no es opcional en un deck de marca

Un deck de cliente sin su logo se lee como plantilla. Va en dos sitios:

1. **Portada**, encima del título: `<img class="marca-logo" src="DATA_URI" alt="Marca">`
2. **HUD**, sustituyendo al nombre escrito: descomentar el `<img class="marca-logo">` del
   HUD y añadir la clase `con-logo` al `<div id="hud">`

El logo va **incrustado como data URI**, nunca como ruta a un archivo: el deck es UN archivo
y tiene que abrir desde WhatsApp o un USB.

```bash
python3 ~/.claude/skills/golden-presenta/scripts/incrustar_recurso.py imagen /ruta/logo.png
```

Si el logo es SVG, mejor pegarlo **inline** dentro de `<figure class="marco limpio">`: pesa
menos y puede heredar el color del deck con `fill="currentColor"`.

Ocho valores de color. Nada más se toca para cambiar de marca, pero **se tocan los ocho**.

**Verificación obligatoria:** el script calcula el contraste WCAG real entre `--ink` y
`--surface` (mínimo 4.5) y entre `--muted` y `--surface`. Una paleta bonita que no llega a
AA no se lee al fondo de una sala, y eso no es una opinión de diseño: es una medición.

## 2 · Los 4 perfiles de Golden

### Perfil A · Golden Group (interno, arsenal, propuestas propias)
```css
--bg:#07080B; --surface:#10131A; --ink:#F4F6FB; --muted:#8B93A7;
--accent:#FFC637; --accent-2:#6CCFFF; --line:#232833; --curtain:#FFC637;
```
Oscuro con dorado. Es la identidad del arsenal.

### Perfil B · Comunidad Golden y MBA (material formativo)
```css
--bg:#0A0C10; --surface:#141821; --ink:#F5F7FA; --muted:#949CAD;
--accent:#FFC637; --accent-2:#7DD3A0; --line:#262C38; --curtain:#FFC637;
```
Igual de oscuro pero con la lámina un punto más clara: el material formativo se lee más
rato y el descanso visual importa. El verde del secundario marca los aciertos en las
láminas de comparación.

### Perfil C · Marca personal de FER (charlas, bootcamp, El Cartel del Chat)
```css
--bg:#0B0B0C; --surface:#151517; --ink:#FAFAFA; --muted:#9A9A9E;
--accent:#E8E8E8; --accent-2:#FFC637; --line:#282829; --curtain:#E8E8E8;
```
Neutro y sobrio, con el dorado relegado a secundario. FER expone como "Fer", no como
Golden: la marca corporativa no debe aparecer en el escenario.

### Perfil D · Cliente (marca blanca)
Los ocho tokens salen de la identidad del CLIENTE. Golden no firma ninguna lámina, salvo
que el cliente lo pida por escrito. Ver el punto 3 para sacarlos.

**Versión clara**, cuando el cliente tiene identidad clara y no acepta fondo oscuro:
```css
--bg:#EFEFF2; --surface:#FFFFFF; --ink:#12141A; --muted:#5C6373;
--accent:<el color del cliente>; --accent-2:<su secundario>;
--line:#DFE2E8; --curtain:<el color del cliente>;
```
Aviso medido: en fondo claro el acento del cliente casi nunca pasa AA como texto. Se usa
para fondos de botón y viñetas, y el texto encima va en `--ink`, nunca en el acento.

### Contraste medido de los 4 perfiles

Calculado con `scripts/verificar_deck.py` el 2026-09-02. Mínimo AA: 4.5 para texto,
3.0 para el acento.

| Perfil | ink/surface | muted/surface | accent/surface |
|---|---|---|---|
| A · Golden Group | 17.19 | 6.04 | 11.84 |
| B · Comunidad y MBA | 16.55 | 6.44 | 11.32 |
| C · FER personal | 17.47 | 6.50 | 14.88 |
| D · Cliente claro | 18.41 | 6.02 | **1.57 no pasa** |

El perfil D confirma la advertencia con un número: sobre fondo blanco, un dorado de marca
da 1.57 y no se puede usar para texto. Sirve de fondo de botón con `--ink` encima, y de
viñeta. Esto no es cuestión de gusto: es la razón por la que el verificador lo mide.

## 3 · Cómo se saca la paleta de un cliente

En este orden, y sin inventar:

1. **El cerebro de marca** (`golden-brand-brain`) si existe. Ahí ya está decidido.
2. **Su web o su tienda:** se abre y se leen los hex reales del CSS, no se estiman a ojo.
3. **Su logo:** se extraen los colores dominantes del archivo.
4. **Preguntar UNA vez**, con esta plantilla exacta:

```
Para que el deck salga con su identidad necesito 3 datos:
1. El color principal de la marca en hex (ejemplo #FFC637)
2. Si prefiere el deck en fondo oscuro o fondo claro
3. El logo en PNG o SVG con fondo transparente
```

Nunca se elige un color "bonito" a ciegas. Un deck con la marca equivocada es peor que uno
en blanco y negro.

## 4 · Tipografía

El motor viene con pila del sistema a propósito: **cero dependencias que se puedan caer**.
Un deck que carga tipografías de Google se rompe si la sala no tiene internet, y eso pasa
justo el día de la presentación.

```css
--font-display: "Georgia", "Times New Roman", serif;   /* serif con carácter */
--font-body:    system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-mono:    ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace;
```

### Tipografía de marca sin salir a la red

**Antes de pensar en Google Fonts, mirar lo que ya está en el Mac.** `canvas-design` trae
una carpeta de fuentes con licencia OFL (libre para incrustar y distribuir):

```bash
python3 ~/.claude/skills/golden-presenta/scripts/incrustar_recurso.py catalogo
```

Las que importan para presentaciones:

| Fuente | Peso | Para qué |
|---|---|---|
| **Big Shoulders Bold** | 92 KB | Condensada display. **La más cercana a Anton.** Eventos, carteles |
| Boldonse | 75 KB | Display pesada, con carácter. Un titular que grite |
| Erica One | 24 KB | Display gorda. Carteles |
| Outfit Bold | 54 KB | Grotesca geométrica limpia. Corporativa moderna |
| Gloock | 93 KB | Serif display de contraste alto. Editorial cara |
| Young Serif | 103 KB | Serif con peso. Marca de producto |

Se incrusta en base64 y queda dentro del archivo:

```bash
python3 .../incrustar_recurso.py fuente ".../BigShoulders-Bold.ttf" \
    --nombre "Big Shoulders" --peso 700
```

El bloque `@font-face` que devuelve se pega arriba del `<style>`, y en `:root`:
`--font-display: "Big Shoulders", "Arial Narrow", sans-serif;`

**Pila de respaldo del sistema**, si no se quiere incrustar y se acepta el riesgo: para
condensada, `"DIN Condensed", "Impact", "Haettenschweiler", "Arial Narrow", sans-serif`.
Funciona en macOS; en el portátil de la sala puede no estar. **Incrustar es lo seguro.**

Si el cliente exige su tipografía corporativa, hay dos caminos y se elige explícitamente:

- **Incrustarla en el archivo** como base64 dentro de `@font-face`. El deck sigue siendo un
  solo archivo y sigue funcionando sin internet. Suma peso (una fuente ronda 40 a 120 KB).
- **Cargarla desde Google Fonts.** Más ligero, pero se cae sin conexión. Si se toma este
  camino, la pila de respaldo tiene que ser real, no `sans-serif` a secas.

Regla que no cambia: **el choque tipográfico es lo que hace que se vea caro.** Display
grande contra microtipografía de 11 px con tracking abierto. Un deck todo en la misma
fuente y el mismo tamaño se ve barato aunque los colores sean perfectos.

## 5 · Reglas de marca blanca

1. **El deck de un cliente lleva la marca del cliente.** En el HUD, en el preloader, en el
   pie. Se reemplaza `GP_MARCA` por su nombre, no por Golden Group.
2. **Nada de "hecho con" ni firmas ocultas.** Si Golden quiere crédito, se pide y se acuerda.
3. **El `<title>` es el nombre del proyecto del cliente**, porque es lo que se ve en la
   pestaña y en la vista previa del enlace cuando lo comparte internamente.
4. **Revisar que no quede contenido de otro cliente.** Es el error clásico al reutilizar un
   deck. El verificador atrapa los placeholders `GP_`, pero no atrapa el nombre de otro
   cliente ya escrito: eso se revisa leyendo.
5. **Los dos WhatsApp y los dos correos de Golden no van en un deck de cliente.** Ese dato
   es interno.
