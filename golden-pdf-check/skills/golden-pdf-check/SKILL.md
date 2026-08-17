---
name: golden-pdf-check
description: >-
  Golden Group — estándar de PDF de Comunidad Golden. Audita y ARREGLA PDFs
  (o los construye desde cero) para que salgan con la identidad Golden y, sobre
  todo, para que NINGÚN prompt/bloque copiable se parta entre páginas: cada
  prompt ocupa una sola página y, si hace falta, se reduce para caber entero
  (copy-paste limpio). Revisa identidad de marca, colores, márgenes, paginación
  y estructura. Úsala SIEMPRE que el usuario quiera: crear, revisar, auditar,
  arreglar, maquetar o "dejar perfecto" un PDF para la comunidad o los alumnos;
  un PDF de prompts para copiar y pegar; un documento con la marca Golden Group;
  cuando diga "revisa este PDF", "este PDF se ve feo", "hazme un PDF de prompts",
  "que no se corten los bloques", "márgenes/colores/paginación del PDF", o pegue
  o mencione un archivo .pdf que haya que verificar o producir. También aplica
  cada vez que Claude vaya a generar un PDF entregable para Golden: ese PDF debe
  pasar por este estándar. NO es para editar temas Shopify ni analizar anuncios.
---

# golden-pdf-check · el estándar de PDF de Comunidad Golden

<!-- skill v5.8 · 2026-08-07 (centro de mando, cosecha del chat ESTUDIO 360 DENTAL CAVITY HEALING Chile) · LÍNEAS LARGAS EN TARJETAS: dentro de una tarjeta monoespaciada, una línea de más de ~76 caracteres se ENVUELVE al renderizar y la compuerta verbatim la reporta como "espaciado/orden alterado" (pasó con dos prompts de imagen; se resolvió reescribiéndolos a 72-84 chars/línea). Regla de redacción "líneas de tarjeta ≤ 76 caracteres" en content-format.md + build_pdf.py AVISA antes de renderizar con tarjeta y línea exactas (⚠️ LÍNEAS LARGAS EN TARJETAS por stderr) -->
<!-- skill v5.7 · TEMAS: `--css tema.css` anexa una hoja que solo redefine variables/colores (la identidad Golden queda intacta por defecto) y `--palette paleta.json` hace que audit_pdf.py juzgue con OTRA paleta permitida. Ademas bloques con estilo `::: nombre Titulo … :::` -> <div class="block nombre"> con el contenido procesado como Markdown (para que un documento largo respire: destacados, avisos, tablas de datos). Origen: manual M3 del MBA con la identidad naranja/cian del programa -->
<!-- skill v5.6 · FIGURAS: `![Pie](ruta.svg){60%}` en una línea sola = figura atómica (imagen + pie numerado que nunca se separan ni se parten entre páginas), incrustada en base64, ruta relativa al .md, SVG como vector. Origen: manual M3 del MBA (Meta Business Manager, 2026-08-04) — un manual de pasos sin pantallas no enseña. Cubierto por 2 pruebas nuevas en selftest.py (11/11) -->
<!-- skill v5.5 · 4 defectos medidos en producción (guía logística 27 págs, 2026-08-03): (1) CRÍTICO ligaduras de JetBrains Mono corrompían el copy-paste (>> salía como <>, // como </) → font-variant-ligatures:none + "liga" 0,"calt" 0 en .prompt-body y code.inline, trampas >> // https:// <<X>> horneadas en selftest-sample; (2) norma FER portada COMPACTA: título+índice en la MISMA hoja (adiós hoja 70% vacía que "da pereza leer"); (3) tablas largas SÍ se parten con thead repetido y filas enteras; (4) colchón de tarjeta 8→20mm (el encabezado precedente comía el margen y el propio auditor tumbaba PDFs del motor); extra: compuertas ignoran selectores de variación de emoji U+FE0F (falso "no idéntico" con ⚠️) -->
<!-- skill v5.4 · norma FER: TODO PDF Golden abre con página de CONTENIDO (índice línea por línea de todo lo que trae el documento + cuántos textos copiables tiene cada parte). Se genera SOLA desde los encabezados en build_pdf.py (outline + build_index, CSS .toc, flag --no-index para la excepción). Origen: PDF Dental Cavity Healing 2026-07-25 -->
<!-- skill v5.3 · norma FER: copys/prompts múltiples = tarjetas numeradas separadas (jamás párrafo corrido); marcadores [PENDIENTE] en negrita, no backticks (mono inline cruza páginas). Origen: PDF Libido UP 2026-07-25 -->
<!-- skill v5.2 · verbatim_check ahora despoja front matter/encabezados/pipes para comparar bien contra .md (adiós falsos positivos); referencia a logo-golden.svg.orig eliminada (no existía) — si se re-sube un logo nuevo, redimensionarlo igual antes de incrustarlo -->
<!-- skill v5.1 · logo oficial optimizado 1.4MB→195KB (PNG 444px cuantizado con alfa, idéntico a la vista a 74px) -->
<!-- skill v5 · auditor sin falsos positivos (dos tarjetas seguidas ≠ corte; texto normal al borde = aviso, no tumba veredicto), normalización tipográfica compartida en las dos compuertas (elipsis/comillas/guiones), logo oficial = emblema Golden Group Community, selftest 9/9 -->
<!-- v4 · fuentes OFL incrustadas (estáticas anti-Type3), compuerta verbatim con doble chequeo, PDF etiquetado, tablas, selftest adversarial -->

Este skill garantiza que todo PDF que Golden entrega a su comunidad se vea
profesional, tenga la identidad de marca y — lo más importante — que los
**prompts copiables nunca se partan entre páginas**. La gente copia y pega
esos prompts; un bloque cortado a la mitad es inaceptable.

Regla operativa: **siempre que leas o generes un PDF para Golden, déjalo con
esta perfección.** No entregues un PDF "a mano" si este skill puede hacerlo bien.

## NORMA FER · todo PDF abre con una página de CONTENIDO (v5.4)

Después de la portada va **SIEMPRE** una página de **CONTENIDO** que dice, **línea por línea, todo
lo que hay en el documento**: cada sección y cada subsección en el orden en que aparecen, con un
número al lado que indica **cuántos textos copiables** trae esa parte. Quien abre el PDF entiende de
un vistazo todo lo que compró: investigación, precios, estructura de ads, prompts de imágenes,
prompt de Chatea, y lo que sea que traiga.

- **Se genera SOLA** en `build_pdf.py` (`outline()` + `build_index()`), leyendo los `##` y `###` del
  Markdown y contando las tarjetas de prompt de cada sección. **Nadie la escribe a mano** y por eso
  nunca queda desactualizada cuando el contenido cambia.
- Por eso los encabezados del contenido tienen que ser **descriptivos y en orden de ejecución**:
  ese texto es exactamente el que se ve en el índice. Un `### Copy 7 · Bloque de honestidad` se lee
  perfecto en el índice; un `### Otro más` no.
- Cabe en **una página** en la mayoría de documentos (dos columnas, tipo compacto). Si el documento
  es enorme, fluye a la siguiente página sin cortar ninguna línea.
- **Excepción única:** `--no-index` para documentos de una sola pieza (un PDF de un solo prompt,
  una carta). En entregables de proyecto, informes, paquetes de lanzamiento y PDFs de prompts, va.

## REGLA INVIOLABLE · el texto no se toca

Este skill **solo cambia la estructura, la maquetación y la arquitectura visual**
del PDF para que se vea perfecto. **NUNCA modifica el contenido.** El texto del
usuario es sagrado y va tal cual: mismas palabras, misma ortografía, misma
puntuación, mismo orden, mismos saltos de línea dentro de cada prompt. No se
corrige, no se "mejora", no se resume, no se reescribe, no se traduce, no se le
quitan ni añaden signos. Lo único permitido es envolverlo en tarjetas, secciones
y portada, y ajustar tamaños/márgenes/paginación.

La única excepción es texto que el usuario te pida **crear desde cero** (p.ej. un
subtítulo de portada si no lo dio). Eso sí sigue el estilo Golden. Pero el
contenido que ya existe — sobre todo los prompts — se preserva carácter por
carácter. Ante la duda, no lo cambies.

## Qué hace

1. **Construye** un PDF Golden desde contenido (Markdown-Golden) — para cuando
   aún no hay PDF o cuando el existente hay que rehacerlo. Incluye **portada +
   página de CONTENIDO automática** (norma FER v5.4) + tarjetas atómicas.
2. **Audita** un PDF existente y reporta fallos de marca, márgenes, colores y
   paginación (bloques al filo del borde = riesgo de corte).
3. **Arregla**: extrae el contenido del PDF viejo, lo pasa al formato Golden y
   lo regenera con bloques atómicos. Así el arreglo es garantizado, no cosmético.

## Cuándo usar cada camino

- **"Hazme un PDF de estos prompts" / no hay PDF todavía** → construir (paso A).
- **"Revisa/arregla este PDF"** → auditar (paso B) y, si algo falla o si el
  usuario quiere el resultado perfecto, reconstruir (paso C).
- Ante la duda, **audita primero** para diagnosticar y luego decide.

---

## Paso A · Construir un PDF Golden

1. Prepara el contenido en **Markdown-Golden**. Lee `references/content-format.md`.
   Lo esencial: cada prompt que se copia va dentro de una tarjeta:
   - bloque ` ``` ` … ` ``` ` (monoespaciado), o
   - bloque `::: prompt Título` … `:::` (prosa).
   Añade un front matter con `title`, `subtitle`, `kicker`, `author` para la portada.

2. Genera el PDF:
   ```bash
   python scripts/build_pdf.py contenido.md salida.pdf
   ```
   El script arma el HTML con la identidad Golden (`assets/golden-print.css`),
   corre el auto-fit (`assets/autofit.js`) y renderiza a PDF. Al terminar corre
   una **compuerta verbatim**: re-extrae el texto del PDF y confirma que cada
   prompt salió idéntico. El JSON de salida trae `engine`, `cards`,
   `verbatim: {ok, fails}` y `fit_warnings` (prompts que quedaron muy reducidos
   o escalados: conviene partirlos en el contenido; salen también por stderr).
   Con `--strict` el script falla (exit 3) si el texto no coincide 100%; con
   `--no-verify` se omite la comprobación.

   **Bloques con estilo (v5.7):** `::: nota Título` … `:::` produce un
   contenedor atómico con clase propia. Sirve para que un documento largo no
   se lea apelmazado: destacados, avisos, tarjetas de datos. A diferencia de
   la tarjeta de prompt, el contenido de adentro SÍ se procesa como Markdown.

   **Documentos que NO se emiten bajo la marca Comunidad Golden** (el MBA es el
   caso: su emisor formal es la empresa, y la comunidad no se nombra en material
   externo) usan `--logo ruta/al/sello.png` para la portada y `--footer "Texto"`
   para el pie, y `--css tema.css` para la paleta. El tema es una hoja que se
   anexa DESPUÉS de la de marca y solo redefine variables y colores, así que la
   identidad Golden nunca se toca. Para auditarlos, `audit_pdf.py --palette
   paleta.json` con los hex permitidos de esa marca. Sin esos flags, todo sigue
   siendo Golden.

   El PDF sale **etiquetado/accesible** (StructTreeRoot) con Playwright. El
   contenido soporta encabezados, listas, separadores, **tablas** (`| a | b |`
   con línea `| --- |`), **figuras** (`![Pie](ruta.svg){60%}` en una línea sola:
   imagen incrustada + pie numerado, atómicos como las tarjetas) y las dos
   formas de tarjeta de prompt. El texto de las
   tarjetas se escapa literal SIEMPRE (nunca se aplica markdown al prompt).

   **Fuentes de marca incrustadas:** el documento usa Inter (títulos/cuerpo) y
   JetBrains Mono (prompts), incrustadas en base64 desde `assets/fonts/` (OFL),
   así se ve idéntico en cualquier equipo. Son estáticas y con el Área Privada
   del cmap eliminada a propósito: si se usara la versión variable, Chrome las
   convierte en Type 3 y mapea mal caracteres como los corchetes `[ ]`,
   corrompiendo el copiar-pegar. No reemplaces estas fuentes por las variables.

3. Verifica el resultado (ver "Verificación" abajo). Si un prompt salió con el
   tipo muy reducido, probablemente convenga **partirlo en dos** (decisión de
   contenido) — avísale al usuario en vez de dejarlo microscópico.

### Motor de render

- **Preferido y ya instalado: Playwright (Chromium).** Da numeración de página
  en el pie ("Comunidad Golden · Página X de Y") y ejecuta el auto-fit midiendo
  al ancho exacto del PDF. Es el motor por defecto. Si algún día falta:
  ```bash
  pip install playwright && python -m playwright install chromium
  ```
- **Fallback: Chrome headless** (el script lo detecta solo). Mantiene bloques
  atómicos y ahora mide al ancho correcto (`--window-size`), pero sin numeración
  en el pie. Si solo hay este, avísale al usuario que para la numeración conviene
  Playwright.

---

## Paso B · Auditar un PDF existente

```bash
python scripts/audit_pdf.py documento.pdf --json informe.json
```

Revisa:
- **Márgenes** invadidos.
- **Bloques cortados**: (a) contenido pegado al borde inferior del área útil en
  una página que no es la última; (b) **detección de bloques monoespaciados
  (prompts/código) que continúan de una página a la siguiente** — lo peor para
  copiar y pegar. Esto sí atrapa un prompt partido en un PDF ajeno.
- **Colores fuera de marca** por **muestreo de píxeles** (renderiza el PDF a
  imagen y mide el % de área con color fuera de la paleta). Funciona con
  cualquier PDF (Canva, Word, Chrome), no depende de cómo se codificó el color.
  Reporta los tonos foráneos dominantes.

Imprime un informe en Markdown y guarda el JSON. Requiere `pdfplumber`; la
auditoría de color por píxeles usa `Pillow` + `pdftoppm` (poppler) — si faltan,
cae al análisis por objeto. Con solo `pypdf` hace un análisis básico.

**Semántica del veredicto:** solo tumban el veredicto los problemas REALES de
copy-paste — un bloque mono cortado entre páginas (`mono_split`) o un bloque de
prompt al filo del borde (`bottom_risk` con `mono: true`). El texto normal
(párrafos) que termina cerca del margen es paginación normal y sale como
**aviso no bloqueante**. Dos tarjetas en páginas seguidas NO son un corte: el
auditor detecta la cabecera "PROMPT · COPIAR" de la página siguiente y las
distingue.

El auditor es **heurístico y advisory**: señala síntomas. No puede garantizar
por sí solo que un bloque no se corte — eso solo se garantiza reconstruyendo.
Preséntale al usuario el veredicto y las 2-3 cosas más importantes a arreglar,
no un volcado crudo del JSON.

---

## Paso C · Arreglar (reconstruir) un PDF

Cuando la auditoría marca problemas o el usuario quiere el resultado perfecto:

1. Extrae el contenido del PDF viejo (texto por página). Usa `pdfplumber`
   (`page.extract_text()`) o, si el usuario tiene la fuente original, pídela.
2. Reescríbelo en Markdown-Golden: identifica qué partes son **prompts
   copiables** y enciérralas en tarjetas ` ``` ` / `:::`. Respeta el contenido
   textual del usuario — no lo reinventes, solo lo reestructuras.
3. Reconstruye con `build_pdf.py` (Paso A) y verifica.
4. **Compuerta verbatim obligatoria:** compara el texto del PDF viejo contra el
   nuevo para garantizar que no cambió ni una palabra:
   ```bash
   python scripts/verbatim_check.py --old viejo.pdf --new nuevo.pdf
   ```
   Exit 0 = idéntico; exit 3 = hay diferencias (te lista qué segmentos). Si hay
   diferencias, NO entregues: revisa la extracción y corrige. Nunca alteres el
   texto para "cuadrar" la comparación.
5. Entrega el PDF nuevo junto a un resumen corto de qué se corrigió (solo
   estructura/maquetación, nunca contenido).

---

## Verificación (siempre antes de entregar)

Confirma que el PDF quedó bien:

- **Bloques atómicos:** audita el PDF nuevo con `audit_pdf.py`; el veredicto
  debe ser APROBADO (`mono_split` vacío y sin bloques de prompt al filo). Los
  avisos de texto normal cerca del borde no bloquean. Si un PROMPT sí roza el
  borde, sube su prioridad para partirlo en contenido.
- **Marca:** portada con logo y kicker "Comunidad Golden", dorado presente,
  fondo claro, pie "Comunidad Golden … Página X de Y".
- **Márgenes:** nada tocando el borde.
- Si puedes, abre el PDF (o su HTML intermedio con `--save-html`) para una
  revisión visual rápida.

### Prueba de regresión (self-test)

Si tocas el CSS, el parser o el auto-fit, corre el self-test antes de dar por
buena la skill. Construye una muestra y verifica build + verbatim + anti-corte:

```bash
python scripts/selftest.py
```

Debe imprimir `TODO OK`. Si algo sale FAIL, arréglalo antes de usar la skill en
material real.

## Personalización de marca

Todo vive en `assets/`:
- `golden-brand.json` — tokens (colores, geometría, paleta permitida para el auditor).
- `golden-print.css` — estilo de impresión (portada, tarjetas, tablas).
- `logo-golden.svg` — **emblema oficial Golden Group Community** (el círculo
  dorado/negro con las GG; es el PNG oficial incrustado en un envoltorio SVG).
  El naranja de comunidad vive en `PROYECTOS/SKOOL/logo-comunidad-golden.svg`.
- `autofit.js` — lógica anti-corte. El alto máximo por tarjeta (`--card-max-mm`,
  variable CSS) lo **deriva build_pdf.py de la geometría real** (única fuente de
  verdad: área útil − colchón) y lo inyecta; el valor escrito en el CSS es solo
  el fallback si el HTML se usa suelto. No es un flag de línea de comandos.

## Estilo de textos (marca Golden)

Cualquier texto que redactes para estos PDFs sigue las reglas de Golden:
- **Nunca** signos de apertura `¿` ni `¡`; solo el de cierre. Suena más humano.
- Tono claro y directo, sin relleno.
- El contenido de los prompts es del usuario: respétalo literal, no lo adornes.

## Norma de FER: copys y prompts SIEMPRE numerados en tarjetas separadas (2026-07-25)

Cuando el contenido trae VARIOS elementos copiables de la misma familia (5 copys de anuncio,
5 titulares, varios prompts de imagen, guiones), la maquetación obligatoria es:
- **Cada texto principal = SU PROPIA tarjeta numerada** con título en el fence
  (` ``` Texto principal 1 `, ` ``` Texto principal 2 `…). Uno abajo del otro, bien separados.
- Elementos de una línea (titulares, descripciones) SÍ pueden ir juntos en UNA tarjeta,
  pero **uno por línea, numerados** (`1. …` `2. …`), jamás en párrafo corrido.
- **PROHIBIDO** el párrafo que une varios copys con "· 1. … 2. … 3. …": mata el copy-paste,
  ahoga los números y da pereza leerlo. Si el autor del contenido lo trae así, la skill lo
  reestructura en tarjetas (es maquetación, no cambio de texto — el contenido queda idéntico).
- Marcadores tipo `[PENDIENTE …]` en texto corrido van en **negrita**, no en backticks: el
  monoespaciado en línea puede cruzar de página y el auditor lo marca como prompt cortado.
- Ojo autor: la skill garantiza tarjetas atómicas, pero QUÉ es tarjeta lo decide quien escribe
  el Markdown-Golden. Ante lista de copys, la decisión correcta es SIEMPRE una tarjeta por copy.
