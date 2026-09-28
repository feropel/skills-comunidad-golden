---
name: golden-pdf-check
description: >-
  Golden Group — estándar de PDF para material que la gente copia, pega y lee en
  serio. Construye PDFs desde cero, audita los existentes y los ARREGLA
  reconstruyéndolos. Ningún prompt ni bloque copiable se parte entre páginas:
  cada uno cabe entero en una sola. Hace informes VISUALES (KPI, barras, escalas
  contra meta, comparativas, pasos, QR) y le pone a cada documento la identidad
  de quien lo firma. Úsala SIEMPRE que se quiera crear, revisar, auditar o
  "dejar perfecto" un PDF; un PDF de prompts para copiar y pegar; un informe con
  gráficas, estadísticas o esquemas; o cuando digan "revisa este PDF", "se ve
  feo", "hazme un PDF de prompts", "que no se corten los bloques", "un informe
  con datos que se vea profesional", "ponle la marca de X", o peguen un .pdf que
  haya que verificar o producir. También cada vez que Claude vaya a generar un
  PDF entregable para Golden. NO edita temas Shopify ni analiza anuncios.
---

# golden-pdf-check · el estándar de PDF de Comunidad Golden

<!-- skill v6.7.1 · 2026-09-27 · ronda de numeracion del Centro de Mando (orden de FER: «que todas las skills esten perfectamente corregidas y actualizadas»): da numero a los cambios del 27-sep que quedaron sin numero. Detalle en references/changelog.md -->
<!-- skill v6.7 · 2026-09-06 · autoprueba 26/26 · EL ACTA COMPLETA VIVE EN references/changelog.md.
     Auditoría golden-skill-auditor: `scripts/visuales.py` (el motor de los componentes
     visuales — KPI, barras, escala, comparativa, pasos, QR — que `build_pdf.py` importa
     en la línea 39) no aparecía citado en ningún lugar del cuerpo, así que el inventario
     lo marcaba como huérfano potencial. Añadida su fila en "Archivos de apoyo" abajo.
     Ningún comportamiento cambió.

     Se movió de aquí por la ley del acta que no se activa: el cuerpo se paga en CADA activación
     y la historia no hace falta para construir un PDF. Medido al migrarla: 24.025 caracteres,
     el 58% de este archivo. Esta línea se queda en el formato de siempre a propósito, porque la
     prueba 22 y el censo del arsenal leen el sello justo de aquí: al migrar el acta se perdió y
     la autoprueba imprimió "disco ?" — el número de versión es interfaz, no decoración. -->

Este skill garantiza que todo PDF que Golden entrega se vea profesional, lleve la
identidad de quien lo firma y — lo más importante — que los **prompts copiables
nunca se partan entre páginas**. La gente copia y pega esos prompts; un bloque
cortado a la mitad es inaceptable.

Regla operativa: **siempre que leas o generes un PDF para Golden, déjalo con esta
perfección.** No entregues un PDF "a mano" si este skill puede hacerlo bien.

## REGLA INVIOLABLE · el texto no se toca

Este skill **solo cambia la estructura, la maquetación y la arquitectura visual**
del PDF. **NUNCA modifica el contenido.** El texto del usuario es sagrado y va tal
cual: mismas palabras, misma ortografía, misma puntuación, mismo orden, mismos
saltos de línea dentro de cada prompt. No se corrige, no se "mejora", no se
resume, no se reescribe, no se traduce, no se le quitan ni añaden signos. Lo único
permitido es envolverlo en tarjetas, secciones y portada, y ajustar
tamaños/márgenes/paginación.

La única excepción es texto que el usuario te pida **crear desde cero** (p.ej. un
subtítulo de portada si no lo dio). Eso sí sigue el estilo Golden. Pero el
contenido que ya existe — sobre todo los prompts — se preserva carácter por
carácter. Ante la duda, no lo cambies.

## Qué hace

1. **Construye** un PDF desde contenido (Markdown-Golden), con portada, tarjetas
   atómicas, figuras, tablas y **componentes visuales** (gráficas, KPI, escalas).
2. **Audita** un PDF existente y reporta fallos de marca, márgenes, colores y
   paginación (bloques al filo del borde = riesgo de corte).
3. **Arregla**: extrae el contenido del PDF viejo, lo pasa al formato Golden y lo
   regenera con bloques atómicos. Así el arreglo es garantizado, no cosmético.

## Cuándo usar cada camino

- **"Hazme un PDF de estos prompts" / no hay PDF todavía** → construir (paso A).
- **"Revisa/arregla este PDF"** → auditar (paso B) y, si algo falla o si el
  usuario quiere el resultado perfecto, reconstruir (paso C).
- Ante la duda, **audita primero** para diagnosticar y luego decide.

---

## Antes de correr nada · el intérprete

Los scripts necesitan `playwright`, `pdfplumber`, `Pillow` y `pypdf`. **No existe
el binario `python` en el Mac de Golden** (solo `python3`), y las dependencias
viven en un entorno propio. Resuelve el intérprete UNA vez y úsalo en todos los
comandos de esta skill:

```bash
PY=~/.golden/pdfenv/bin/python; [ -x "$PY" ] || PY=python3; echo "$PY"
```

Ese es el `$PY` que aparece en los comandos de abajo. El entorno `~/.golden/pdfenv`
es el oficial de Golden para PDFs; si algún día no está, `python3` sirve mientras
tenga las cuatro dependencias. Si falta alguna:

```bash
$PY -m pip install playwright pdfplumber pillow pypdf && $PY -m playwright install chromium
```

Escribir `python` a secas falla con `command not found` — por eso los comandos de
esta skill nunca lo usan.

## Conexión con el ecosistema

**Fábrica: chat ✅ SKILL golden-pdf-check.** Ahí se repara esta skill; los demás chats
reportan defectos medidos en vez de editarla (REGISTRO-FABRICAS lee esta línea para
resolver el dueño, y los actores de auditoría masiva la respetan). Se declara AQUÍ, en el
archivo, y no solo en memoria: una fábrica que vive solo en la memoria del ecosistema
desaparece si alguien reformula esa nota.

Los cambios relevantes (defectos medidos en producción, normas nuevas de FER sobre
la maquetación) se reportan a **🧠 GOLDEN - CENTRO DE MANDO**, que decide si la
lección se retransmite. Varias versiones nacieron así: un chat construyendo un
entregable real midió el defecto y lo mandó a la fábrica.

---

## LA IDENTIDAD SE PIDE, NO SE HEREDA

**Sin `--tema`, el documento sale NEUTRO**: sin logo, sin kicker, sin autor y sin
pie. La marca de Comunidad Golden vive en su tema y se pide:

```bash
$PY scripts/build_pdf.py contenido.md salida.pdf --tema comunidad-golden
```

El porqué, que vale para cualquier herramienta que salga de casa: hasta v6.0 la
marca de Golden era el valor por defecto, así que **cualquiera que usara la skill
firmaba SUS documentos con la marca de FER sin enterarse**. Un documento sin sello
es neutro; **un documento con el sello de otro es una atribución falsa**, y esa no
la caza ninguna prueba de maquetación porque el PDF sale perfecto. Cuando no hay
identidad, el motor no rellena: **avisa** por stderr y dice cómo pedirla.

Cada identidad es un archivo en `assets/temas/<id>.json` con colores, kicker,
autor, pie, logo y paleta de series. **Todo tema debe declarar `source_of_truth`**
(de qué archivo real salieron esos valores) o la construcción avisa a gritos.

| Tema | Estado |
|---|---|
| `comunidad-golden` | anclado a `GASTO-GOLDEN/app/globals.css` |
| `cartel-del-chat` | 🔴 **PROVISIONAL**, `source_of_truth: null` — valores inventados para demostrar el mecanismo, sirven de demo y NO de marca |

Para crear un tema nuevo, copia uno existente, cambia los valores y **rellena
`source_of_truth` con el archivo del que salieron**. Si no tienes ese archivo,
pídeselo al chat dueño de esa marca por el Centro de Mando: inventar colores de
otro es el mismo defecto que heredarlos.

**Reserva declarada:** lo neutralizado es la ATRIBUCIÓN (logo, kicker, autor,
pie). La hoja de estilo por defecto sigue siendo la de Golden — fondo crema y
dorados. Un documento ajeno ya no dice de quién es, pero se le parece.

---

## Paso A · Construir un PDF

1. Prepara el contenido en **Markdown-Golden**. Lee `references/content-format.md`
   antes de escribir el primer bloque: ahí está la tabla completa de sintaxis.
   Lo esencial: cada prompt que se copia va dentro de una tarjeta:
   - bloque ` ``` ` … ` ``` ` (monoespaciado), o
   - bloque `::: prompt Título` … `:::` (prosa).
   Añade front matter con `title`, `subtitle`, `kicker`, `author` para la portada.

2. Genera el PDF:
   ```bash
   $PY scripts/build_pdf.py contenido.md salida.pdf --tema comunidad-golden
   ```
   El script arma el HTML con `assets/golden-print.css`, corre el auto-fit
   (`assets/autofit.js`) y renderiza. Al terminar corre una **compuerta verbatim**:
   re-extrae el texto del PDF y confirma que cada prompt salió idéntico. El JSON de
   salida trae `engine`, `cards`, `verbatim: {ok, fails}` y `fit_warnings` (prompts
   que quedaron muy reducidos: conviene partirlos en el contenido). Con `--strict`
   falla (exit 3) si el texto no coincide; con `--no-verify` se omite.

3. Verifica el resultado (ver "Verificación"). Si un prompt salió con el tipo muy
   reducido, probablemente convenga **partirlo en dos** (decisión de contenido) —
   avísale al usuario en vez de dejarlo microscópico.

### Contenido que se ve, no solo que se lee

Un informe de párrafos no se lee. Estos bloques producen gráficos vectoriales
dentro del PDF, y **todos llevan la cifra escrita al lado** — en papel no hay
cursor que pasar por encima, así que la etiqueta directa es obligatoria, no
opcional. La sintaxis completa de cada uno está en `references/content-format.md`.

| Bloque | Para qué |
|---|---|
| `::: kpi` | 3-4 cifras de cabecera con su variación |
| `::: barras` | comparar magnitudes entre categorías |
| `::: escala` | avance real contra una meta |
| `::: comparativa` | antes y después por fila |
| `::: pasos` | un proceso numerado |
| `::: qr` | código QR a un enlace, con su pie |

Además: **figuras** (`![Pie](ruta.svg){60%}` en una línea sola — imagen incrustada
más pie numerado, atómicos como las tarjetas), **tablas** (`| a | b |` con línea
`| --- |`, se parten con la cabecera repetida), **enlaces** que quedan clicables, y
**bloques con estilo** `::: nota Título` … `:::` para que un documento largo no se
lea apelmazado (a diferencia de la tarjeta de prompt, el contenido de adentro SÍ se
procesa como Markdown).

Elige la forma por el TRABAJO del dato, no por gusto: magnitud entre categorías →
barras; avance contra objetivo → escala; una cifra sola que es el titular → KPI;
un proceso → pasos. Si el dato no tiene trabajo, no lleva gráfico.

### El mapa es opt-in

El documento **no lleva índice** salvo que se pida con `--mapa`, y entonces sale
solo el primer nivel, a una columna, titulado "EN ESTE DOCUMENTO".

La norma anterior (v5.4) mandaba abrir todo PDF con una página de CONTENIDO que
listara cada sección y subsección. **FER la revocó** midiendo al lector, no al
documento: *"la gente no lee los índices, eso no es un libro"*. Un mapa dice dónde
estás; un índice de dos niveles a tres columnas es una pared de texto en la
portada. Úsalo solo en documentos largos de consulta salteada; en un entregable
que se lee de corrido, no.

Los números de página del mapa son **reales**: se calculan en una segunda pasada
sobre el PDF ya construido y se repite hasta que el mapa se estabiliza.

### Motor de render

- **Preferido y ya instalado: Playwright (Chromium).** Da numeración de página en
  el pie y ejecuta el auto-fit midiendo al ancho exacto del PDF. Si algún día falta:
  ```bash
  $PY -m pip install playwright && $PY -m playwright install chromium
  ```
- **Fallback: Chrome headless** (el script lo detecta solo). Mantiene bloques
  atómicos y mide al ancho correcto (`--window-size`), pero **sin numeración en el
  pie**. Si solo hay este, dilo: para la numeración conviene Playwright.

**Fuentes de marca incrustadas:** Inter (títulos/cuerpo) y JetBrains Mono
(prompts), en base64 desde `assets/fonts/` (OFL), para que se vea idéntico en
cualquier equipo. Son estáticas y con el Área Privada del cmap eliminada **a
propósito**: la versión variable la convierte Chrome en Type 3 y mapea mal los
corchetes `[ ]`, corrompiendo el copiar-pegar. **No las reemplaces por las
variables.** El PDF sale etiquetado/accesible (StructTreeRoot).

---

## Paso B · Auditar un PDF existente

```bash
$PY scripts/audit_pdf.py documento.pdf --json informe.json
```

Revisa:
- **Márgenes** invadidos.
- **Bloques cortados**: (a) contenido pegado al borde inferior del área útil en una
  página que no es la última; (b) **bloques monoespaciados (prompts/código) que
  continúan de una página a la siguiente** — lo peor para copiar y pegar. Esto sí
  atrapa un prompt partido en un PDF ajeno.
- **Colores fuera de marca** por **muestreo de píxeles** (renderiza a imagen y mide
  el % de área con color fuera de la paleta). Funciona con cualquier PDF (Canva,
  Word, Chrome), no depende de cómo se codificó el color. Para auditar material de
  otra marca, `--palette paleta.json` con sus hex permitidos.

Requiere `pdfplumber`; la auditoría de color usa `Pillow` + `pdftoppm` (poppler) —
si faltan, cae al análisis por objeto. Con solo `pypdf` hace un análisis básico. Si
el archivo no existe, dice cuál no encuentra y sale con código 2, sin traza cruda.

**Semántica del veredicto:** solo tumban el veredicto los problemas REALES de
copy-paste — un bloque mono cortado entre páginas (`mono_split`) o un bloque de
prompt al filo del borde (`bottom_risk` con `mono: true`). El texto normal que
termina cerca del margen es paginación normal y sale como **aviso no bloqueante**.
Dos tarjetas en páginas seguidas NO son un corte: el auditor detecta la cabecera
"PROMPT · COPIAR" de la siguiente y las distingue.

El auditor es **heurístico y advisory**: señala síntomas. No puede garantizar por sí
solo que un bloque no se corte — eso solo se garantiza reconstruyendo. Preséntale al
usuario el veredicto y las 2-3 cosas más importantes, no un volcado del JSON.

---

## Paso C · Arreglar (reconstruir) un PDF

Cuando la auditoría marca problemas o el usuario quiere el resultado perfecto:

1. Extrae el contenido del PDF viejo (texto por página) con `pdfplumber`
   (`page.extract_text()`) o, si el usuario tiene la fuente original, pídela.
2. Reescríbelo en Markdown-Golden: identifica qué partes son **prompts copiables**
   y enciérralas en tarjetas ` ``` ` / `:::`. Respeta el contenido textual — no lo
   reinventes, solo lo reestructuras.
3. Reconstruye con `build_pdf.py` (Paso A) y verifica.
4. **Compuerta verbatim obligatoria:** compara el texto del PDF viejo contra el nuevo:
   ```bash
   $PY scripts/verbatim_check.py --old viejo.pdf --new nuevo.pdf
   ```
   Exit 0 = idéntico; exit 3 = hay diferencias (te lista qué segmentos). Si hay
   diferencias, **NO entregues**: revisa la extracción y corrige. Nunca alteres el
   texto para "cuadrar" la comparación.
5. Entrega el PDF nuevo con un resumen corto de qué se corrigió (solo
   estructura/maquetación, nunca contenido).

### 🔴 EL PUNTO CIEGO DEL PASO C · léelo antes de arreglar un PDF ajeno

**La compuerta verbatim compara EXTRACCIÓN contra EXTRACCIÓN.** Garantiza *"no
cambié lo que leí"*, **NO** *"lo que leí es lo que el documento decía"*. Es cierto
por construcción: si el extractor se equivoca, los dos lados traen el mismo error
y la comparación da OK con el daño dentro.

**Honestidad sobre esto:** el caso que se creyó haber medido en v6.2 resultó ser
un error del fixture, no del extractor (ver v6.4 en el changelog). **No hay
ninguna corrupción de extracción medida en esta skill.** El riesgo es real por
construcción, no por observación, y por eso se cubre con una instrucción y no con
un detector: un guardián contra un fallo imaginario acusa a quien escribe bien.

Qué hacer, en orden:

1. **Pide la fuente original** (el .docx, el Google Doc, el Canva). Si existe,
   reconstruye desde ahí y la pregunta ni se plantea.
2. Si solo hay el PDF, **abre el PDF viejo y el nuevo y compara con los ojos los
   bloques copiables**, sobre todo los que traen símbolos: corchetes, comillas,
   operadores. Es donde falla la extracción cuando falla.
3. Si el documento original existe pero no puedes verlo, **dilo al entregar**:
   qué no pudiste comprobar y por qué. No lo des por bueno en silencio.

**Reserva que sigue abierta:** este camino se ha ejercido de punta a punta contra
un PDF ajeno **fabricado para la prueba** (Chrome, Georgia + Courier, prompt
partido entre páginas: el auditor lo cazó, la reconstrucción salió APROBADA y los
56 segmentos se conservaron). **No se ha ejercido contra un PDF real de un cliente**
salido de Canva, Word o InDesign, que traen columnas, tablas y cajas de texto que
el extractor puede devolver en otro orden. La primera vez que ocurra, verifica con
más cuidado del normal y reporta lo que falle a la fábrica.

---

## Verificación (siempre antes de entregar)

**ORDEN OBLIGATORIO (norma FER):** *la skill revisa, aprueba, y ahí mismo sí se
entrega.* La auditoría va **ANTES** de instalar el PDF en su destino, no después de
anunciarlo. El flujo correcto es: `autoprueba.py` (la skill está sana) → renderizar
a un **PDF candidato** en carpeta temporal → `audit_pdf.py` sobre ese candidato →
**solo si dice APROBADO** se copia al destino y se avisa. Nunca sobrescribas el PDF
bueno con uno sin auditar, ni digas "listo" antes del veredicto.

Confirma que quedó bien:

- **Bloques atómicos:** el veredicto de `audit_pdf.py` debe ser APROBADO
  (`mono_split` vacío y sin bloques de prompt al filo). Los avisos de texto normal
  cerca del borde no bloquean. Si un PROMPT roza el borde, súbelo a prioridad para
  partirlo en contenido.
- **Identidad:** la que se pidió, no la que se supone. Con `--tema comunidad-golden`
  se espera logo, kicker y pie de Comunidad Golden; **sin tema se espera que NO
  haya ninguno de los tres** — un documento neutro con marca es el defecto, no el
  documento neutro.
- **Márgenes:** nada tocando el borde.
- **ÁBRELO Y MÍRALO.** Renderiza al menos la primera página a imagen
  (`pdftoppm -png -r 60 -f 1 -l 1 salida.pdf /tmp/v`) y obsérvala. Los defectos que
  más duelen — un logo gigante, un hueco a media portada, un gráfico ilegible — no
  los caza ningún script, y ninguno de los que se colaron en producción se habría
  colado si alguien hubiera abierto el archivo.

### Prueba de regresión

Si tocas el CSS, el parser, el auto-fit o los componentes, corre esto antes de dar
por buena la skill:

```bash
$PY scripts/autoprueba.py
```

Debe imprimir `TODO OK` con **26 de 26**. La muestra que construye es
`assets/autoprueba-muestra.md`, que trae horneadas las trampas de copy-paste
(`>>`, `//`, `https://`, `<<X>>`, un emoji y una tarjeta larga): **no edites ese
texto**, es el fixture de regresión.

**Toda versión que cambie comportamiento entra con su prueba**, y la prueba se
verifica **rompiendo a propósito lo que vigila**. No es ceremonia: un guardián de
esta misma skill pasó en verde con el defecto repuesto porque comparaba la caja del
texto y el PDF lo imprime en versalitas. **Un guardián que parece trabajar es peor
que ninguno**, porque da permiso para dejar de mirar.

**Dependencias por script** (para que un FAIL se lea bien): `build_pdf.py` y
`audit_pdf.py` necesitan `pdfplumber` y `playwright`; la auditoría de color usa
`Pillow` + `pdftoppm`; `autoprueba.py` además usa `pypdf`. Todas son **opcionales
con degradación**: si falta una, esa comprobación sale **N/D** (no verificable por
el entorno) y el resto sigue. **N/D no es FAIL**: un rojo falso hace que quien lo
lea concluya que el estándar está roto cuando lo que falta es una librería. Pero si
lo que no se resuelve es algo **del artefacto** (un token renombrado, un fondo no
declarado), eso sí es FALLO.

## Personalización de marca

Todo vive en `assets/`:
- `temas/<id>.json` — las identidades (ver "La identidad se pide").
- `golden-brand.json` — tokens de Golden (colores, geometría, paleta permitida para
  el auditor). El porqué de cada valor y la fuente de verdad están en
  `references/brand.md`.
- `golden-print.css` — estilo de impresión (portada, tarjetas, tablas, componentes).
- `logo-golden.svg` — emblema oficial Golden Group Community. Solo se usa si un
  tema o `--logo` lo pide.
- `autofit.js` — lógica anti-corte. El alto máximo por tarjeta (`--card-max-mm`) lo
  **deriva build_pdf.py de la geometría real** y lo inyecta; el valor del CSS es
  solo el fallback si el HTML se usa suelto. No es un flag de línea de comandos.

**Contraste:** los dorados de marca NO pasan WCAG para texto; existe
`--gold-text` solo para texto y el dorado queda intacto en uso gráfico. Los
números y el porqué, en `references/brand.md`. La prueba 16 lo calcula y falla
por debajo de 4.5:1, así que la regla es ejecutable.

## Estilo de textos (marca Golden)

Cualquier texto que redactes para estos PDFs sigue las reglas de Golden:
- **Nunca** signos de apertura de interrogación ni de exclamación; solo el de
  cierre. Suena más humano.
- Tono claro y directo, sin relleno.
- El contenido de los prompts es del usuario: respétalo literal, no lo adornes.

## Norma de FER · una tarjeta por copy

Cuando el contenido trae VARIOS elementos copiables de la misma familia (5 copys,
5 titulares, varios prompts), **cada texto principal va en SU PROPIA tarjeta
numerada**, jamás varios en un párrafo corrido: eso mata el copy-paste. Las reglas
completas, con los casos borde, están en `references/content-format.md` bajo
"Norma de FER · una tarjeta por copy". Reestructurar así es maquetación, no cambio
de texto: el contenido queda idéntico.

## Archivos de apoyo

| Archivo | Cuándo leerlo |
|---|---|
| `references/content-format.md` | **antes de escribir el Markdown**: sintaxis completa de tarjetas, figuras, tablas, componentes visuales y temas |
| `references/brand.md` | antes de tocar colores, fuentes o geometría: de dónde sale cada valor |
| `references/changelog.md` | para saber por qué una regla existe, o antes de deshacer algo que parece raro |
| `scripts/visuales.py` | no se invoca directo: es el motor que `build_pdf.py` importa para dibujar los componentes visuales (KPI, barras, escala, comparativa, pasos, QR) |
