---
name: golden-ebook
description: >-
  Golden Group — crea EBOOKS de valor para regalarle al cliente mientras su pedido viaja, entre la
  guía generada y la entrega. Detecta el producto, elige un TEMA ADYACENTE que cautiva sin hablar
  del producto, investiga con fuentes reales citadas, escribe el libro y lo construye en PDF para
  celular con portada, logo y nombre de la empresa. Un verificador revisa claims prohibidos, citas,
  ortografía, legibilidad y portada antes de entregarlo. Úsala SIEMPRE que pidan "hazme un ebook",
  "un ebook de este producto", "un libro digital para mis clientes", "un regalo para el que compró",
  "contenido para la espera del envío", "algo para mantener caliente al cliente", "un bonus
  post-compra", "un PDF de valor para la guía generada" o "un libro de regalo con el pedido".
  Dispara aunque no digan ebook si quieren un documento largo de valor para clientes. NO es para
  informes o PDFs de prompts (golden-pdf-check), estudios de mercado (golden-investigacion-mercado)
  ni presentaciones (golden-presenta).
---

# golden-ebook · el libro que acompaña al pedido

<!-- skill EB1.4 · 2026-09-20 · auditoría golden-skill-auditor: SKILL.md citaba "68 de 68" fijo
     mientras autoprueba.py ya corría 89/89 (crece con cada sabotaje nuevo) — la instrucción
     literal de la Fase 0 ("si no, no construyas") habría bloqueado toda corrida futura. El número
     se dejó de fijar en el texto. Paso 5b no mencionaba scripts/guardar_fuentes.py: el flujo
     mandaba a revision_fuentes.py directo a fuentes-verificadas.md, pero C25 compara la
     cita_fuente contra EBOOK/fuentes-texto/<id>.txt, que solo existe si guardar_fuentes.py corrió
     antes. Se agregó el paso y su entrada en Archivos de apoyo. Cambios relevantes de esta skill
     se reportan a GOLDEN - CENTRO DE MANDO.
     El acta completa vive en references/changelog.md. -->

Un cliente que compra contra entrega pasa de 2 a 6 días esperando, y en esa espera se enfría: duda,
se arrepiente, o no contesta cuando llega el mensajero. Esta skill le manda, en ese momento, un libro
corto que le enseña algo que le importa. **No habla del producto: habla de la vida de quien lo
compró.** El producto aparece en la carta de bienvenida y en el cierre, y el resto del libro hace
que la empresa parezca un experto y no una tienda.

**Fábrica:** chat «✅ SKILL golden-ebook»

## Antes de correr nada · el intérprete

Los scripts necesitan `playwright` (con Chromium), `pdfplumber`, `pypdf` y `Pillow`. En el Mac de
Golden viven en el entorno de PDFs:

```bash
PY=~/.golden/pdfenv/bin/python; [ -x "$PY" ] || PY=python3; echo "$PY"
```

Si falta alguna: `$PY -m pip install playwright pdfplumber pypdf pillow && $PY -m playwright install chromium`.
Para la portada en PNG hace falta `pdftoppm` (`brew install poppler`); sin él el PDF se construye
igual y solo falta la imagen. Antes de construir el primer ebook de la sesión, comprueba que la
skill está sana:

```bash
$PY ~/.claude/skills/golden-ebook/scripts/autoprueba.py
```

Debe imprimir `TODO OK · N de N` (el mismo N en las dos partes; el número de casos crece con
cada sabotaje nuevo, no está fijo). Si dice `HAY FALLOS` o el N no coincide en las dos partes,
no construyas: el verificador no es confiable.

## Paso 1 · Intake (una sola vez, al inicio)

Reúne todo antes de escribir. **Busca primero, pregunta solo lo que falte.**

| Dato | Dónde buscarlo primero | Si no aparece |
|---|---|---|
| Producto: nombre, qué hace, claims permitidos y prohibidos | `PRODUCTO.json` de la carpeta del producto, dossier de `golden-investigacion-mercado`, ficha de la tienda | pregúntalo; sin producto no hay tema |
| Empresa: nombre legal o comercial | cerebro de marca `BRAND-BRAINS/<MARCA>/marca.md` (skill `golden-brand-brain`) | pregúntalo: **la identidad se pide, no se hereda** |
| Logo | carpeta de marca del proyecto (`RECURSOS-MARCA/`, `marca/`) | el motor pone el nombre en tipografía y lo avisa; nunca inventes un logo |
| Colores (primario, acento, acento de texto, fondo, texto) | cerebro de marca o tema de marca ya medido | pregúntalos; no los inventes |
| País | la carpeta del producto | Colombia |
| Enlace del botón final (tienda o WhatsApp) | cerebro de marca | la web de la marca; si tampoco hay, pregúntalo |
| Tema | lo decide la skill (Paso 2) | solo se usa el del usuario si lo trae |

Si trabajas con varias empresas, cada una lleva SU nombre, SU logo y SUS colores: jamás se
mezclan, ni siquiera en la firma de la carta. Del contacto se usan solo los canales PÚBLICOS de la
empresa (web, WhatsApp de ventas): un ebook se reparte, y C20 bloquea celulares, correos personales,
cédulas, direcciones y números de pedido.

Trabaja en la carpeta del producto, dentro de una subcarpeta `EBOOK/`. Los ebooks de clientes van
en la carpeta del cliente, nunca dentro de la skill.

## Paso 2 · Elegir el tema adyacente

**Lee `references/tema-adyacente.md` antes de proponer un solo tema.** Resumen: lees al comprador
(qué trabajo le hace el producto, en qué momento lo compra, qué le preocupa, qué mitos cree),
generas 5 candidatos de 5 familias distintas, los calificas sobre 42 puntos con seis criterios y
gana el más alto. **Uno que obligue a prometer lo que el producto no puede se descarta aunque sume
más.** Lee también `references/cumplimiento.md` para calificar ese criterio.

Guarda la tabla en `EBOOK/decision-tema.md`. Decide e informa: el empate lo resuelve la regla
de `tema-adyacente.md`, no una pregunta al usuario.

## Paso 3 · Investigar

**Lee `references/investigacion.md`.** Mínimo 5 fuentes con 1 de nivel A; lo recomendado son 8 con
3 de nivel A. **Cada dato sale de una fuente que abriste y leíste**, no del resumen del buscador.
Guarda en `EBOOK/fuentes-verificadas.md` la frase exacta de cada fuente y el dato que sale de ella.

Si no hay red, no inventes: construye solo con lo verificado en disco y declara el hueco.

## Paso 4 · Escribir el ebook.json

**Lee `references/escritura.md`**: estructura fija, medidas, voz, bloques y esquema. Parte de
`assets/muestra/ebook.json`. Lo que más se olvida:

- Carta de bienvenida y cierre caben en una sola página cada uno (topes en `escritura.md`; C16).
- Cada `dato` y cada `mito` con su `fuente`; cada número del texto con su `[n]`.
- Ortografía completa con ¿ y ¡: el ebook es un documento.
- `producto.claims_prohibidos` copiado de la ficha del producto.
- `tema.puente` en una o dos frases.

## Paso 5 · Construir, revisar contra las fuentes y verificar

**5a · Construir.**

```bash
$PY ~/.claude/skills/golden-ebook/scripts/construir_ebook.py EBOOK/ebook.json EBOOK/candidato.pdf --portada-png EBOOK/portada.png
```

El motor devuelve un JSON con los contrastes medidos y si el logo necesitó una placa clara; si no
hay logo, lo avisa por pantalla. Además sella el PDF con el sha256 del `ebook.json` que usó.

**5b · Leer cada frase contra su fuente.** Ningún script ve una frase que **dice más que su
fuente**, y es el fallo más probable: en los dos primeros ebooks reales aparecieron más de veinte,
con y sin cita, en textos que ya pasaban todas las comprobaciones automáticas. Primero guarda el
texto real de cada fuente (C25 compara la cita literal contra ESTE archivo, no contra tu memoria
ni contra el resumen de `fuentes-verificadas.md`):

```bash
$PY ~/.claude/skills/golden-ebook/scripts/guardar_fuentes.py EBOOK/ebook.json
```

Crea `EBOOK/fuentes-texto/<id>.txt`, uno por fuente (por DOI vía Crossref/PubMed, PDF o navegador
Chromium según la URL). Si alguna queda "sin_leer" en la salida, pega tú tras el texto y anótalo en
la primera línea del archivo. Después arma la hoja del Paso 5b:

```bash
$PY ~/.claude/skills/golden-ebook/scripts/revision_fuentes.py EBOOK/ebook.json
```

Crea `EBOOK/revision-fuentes.json` con TODAS las frases que ve el lector (menos títulos, rótulos y
firmas). Abre cada `EBOOK/fuentes-texto/<id>.txt` (usa `fuentes-verificadas.md` como guía rápida de
qué fuente es cuál) y, frase por frase, escribe `"estado": "fiel"` con
lo que dice la fuente, o `"sin afirmacion"` si es transición, instrucción u opinión rotulada; la
`nota` va siempre (15 caracteres o más). Si una frase no es fiel, **corrige el texto del
`ebook.json`**, vuelve a correr el script (conserva lo ya revisado de las frases que no cambiaron) y
revisa las nuevas. Estas son las formas de exagerar que más aparecieron:

| La fuente dice | El texto exagerado dice |
|---|---|
| "se asoció con", "may have" | "causa", "tiene que venir de" |
| "unos 100.000 o más", "56,2 frente a 10" | "más de cien mil", "seis veces" |
| "al menos cada 2 a 3 semanas" | "cada 2 a 3 semanas" |
| un síntoma, un dato de una ciudad | otro síntoma que no nombra, el dato de esa ciudad dicho a todo el país |
| nada (la frase no tiene fuente) | "el mito más repetido", "casi nadie lo sabe", "toma minutos" |

Por último, el **puente**: lee el cierre contra los capítulos. Si un capítulo describe un problema de
salud y el cierre ofrece el producto para ese problema, reescribe el cierre aunque cada frase suelta
sea legal. En la carta y el cierre, del producto se dice solo lo que está en sus claims permitidos.
Cuando esté leído, `"puente": {"estado": "revisado", "nota": "por qué no hay puente"}`.

**5c · Verificar.**

```bash
$PY ~/.claude/skills/golden-ebook/scripts/verificar_ebook.py EBOOK/ebook.json EBOOK/candidato.pdf --json EBOOK/verificacion.json --online
```

Corre 38 comprobaciones (C1 a C25 sobre todo texto que se imprime, P1 a P13 sobre el PDF) y 39 con
`--online` (W1: las fuentes existen; los DOI se confirman en Crossref). Termina en **ENTREGABLE**
(código 0), **NO ENTREGAR** (1, hay fallas) o **NO VERIFICADO** (3, algo quedó N/D).

| Si sale... | Haz esto |
|---|---|
| FALLA en C2, C3, C7, C8, C9, C10, C17, C18 | corrige el **texto** del `ebook.json`, nunca el verificador |
| FALLA en C11 (catálogo) o C19 (bloque desconocido) | saca el producto de los capítulos; usa solo los bloques de `escritura.md` |
| FALLA en C13 (contraste) | pide a la marca un tono oscuro de su acento o propón uno medido; no inventes colores |
| FALLA en C20 (datos privados) | quita cédulas, celulares, correos personales, direcciones y números de pedido: un ebook se reparte |
| FALLA en C25 (Paso 5b) | la hoja falta, tiene frases sin revisar o es de otra versión: vuelve a 5b |
| FALLA en P12 (sello) | el JSON cambió después de construir: reconstruye (5a) y revisa lo nuevo (5b) |
| FALLA en P4 (letra) o P1 (página) | revisa que `meta.formato` sea `movil` o `a5` |
| FALLA en P6 o P13 (portada, logo) | falta el nombre, el título o el logo, o el logo quedó chico: pide uno de mejor proporción |
| FALLA en W1 (fuente que no existe) | el sitio o Crossref respondió 404: esa fuente no existe, cámbiala |
| AVISO en W1 (403) | bloqueo de robots: ábrela con WebFetch y déjalo anotado en `fuentes-verificadas.md` |
| AVISO en C21 (nivel A) | escribe en `nivel_porque` qué la hace A, o bájala de nivel |
| AVISO en C16, C22, C23, C24, P5 | medidas de lectura (carta, título, capítulo, "Pruébalo hoy", páginas casi vacías): ajusta el texto |
| AVISO en P6 (sin logo) | pídele el logo a la marca; nunca lo dibujes tú |
| NO VERIFICADO (código 3) | falta una librería: usa `~/.golden/pdfenv/bin/python` o instálala, y vuelve a correr |
| El motor sale con código 2 | lee el mensaje: dice qué dato falta (marca, color, logo, imagen) |

**Repite 5a a 5c hasta cero fallas.** Si una FALLA parece un error del verificador y no del texto,
demuéstralo con un caso y arréglalo en el script con su prueba en `autoprueba.py`: así nació buena
parte de sus casos (el acta con la cifra exacta de cada versión vive en `references/changelog.md`).

**5d · Ábrelo y míralo.** Ningún script ve un arte que pisa el título o una página que se ve rara:

```bash
mkdir -p EBOOK/paginas && pdftoppm -png -r 45 EBOOK/candidato.pdf EBOOK/paginas/p
```

Mira la portada completa y al menos una apertura, una página de cuerpo con bloques y la de fuentes.
Solo entonces renombra `candidato.pdf` al nombre final (por ejemplo `ebook-<tema>.pdf`).

## Paso 6 · Entregar

**Lee `references/entrega.md`**: el ebook se manda al generarse la guía, desde el gancho "Guía
Generada" del asistente logístico, con los textos que trae ese archivo. Esta skill no configura
Chatea: entrega el PDF, la portada, los dos mensajes y el plan para medir si funciona.

## Terminado es

- [ ] `autoprueba.py` en `TODO OK` en esta sesión.
- [ ] `decision-tema.md` con los 5 candidatos y sus puntajes.
- [ ] `fuentes-verificadas.md` con una línea por fuente.
- [ ] `revision-fuentes.json` completo: N de N frases leídas contra su fuente y el puente revisado.
- [ ] `verificar_ebook.py --online` en **ENTREGABLE**, con el conteo de avisos explicado.
- [ ] Páginas renderizadas y miradas: portada, una apertura, una de cuerpo, fuentes.
- [ ] PDF final, `portada.png` y los dos mensajes de `entrega.md` en la carpeta `EBOOK/`.

El informe al usuario dice **cobertura, no veredicto**: el tema y su puntaje, cuántas fuentes y de
qué nivel, el conteo del verificador (N de N, avisos, fallas), qué páginas miraste y qué quedó sin
verificar (por ejemplo, la miniatura real en WhatsApp o si el ebook baja el rechazo). Nunca "quedó
perfecto".

## Lo que esta skill no hace

| Pedido | Skill |
|---|---|
| Un PDF de prompts, un informe con gráficas o arreglar un PDF existente | `golden-pdf-check` |
| El estudio del producto, su avatar y su voz del cliente | `golden-investigacion-mercado` (su dossier alimenta el Paso 2) |
| Crear o actualizar el cerebro de una marca | `golden-brand-brain` |
| Configurar el mensaje en Chatea Pro | `golden-chatea-pro-config-logistico` |
| Medir la tasa de entrega con y sin ebook | `golden-dropi-analisis` o `golden-logistica-diaria` |
| Una imagen de portada generada con IA | `golden-imagen-arena` (cuesta créditos: el costo se dice antes) |
| Un deck o una presentación | `golden-presenta` |

## Archivos de apoyo

| Archivo | Cuándo |
|---|---|
| `references/tema-adyacente.md` | Paso 2: el método para elegir el tema, con ejemplos por vertical |
| `references/cumplimiento.md` | Pasos 2 y 4: claims en Colombia, aviso obligatorio, imágenes y citas |
| `references/investigacion.md` | Paso 3: jerarquía de fuentes, PubMed por API, qué se puede afirmar |
| `references/escritura.md` | Paso 4: estructura, medidas, voz, bloques y esquema del `ebook.json` |
| `references/entrega.md` | Paso 6: cuándo se manda, dónde se aloja, mensajes y cómo medirlo |
| `references/evidencia.md` | cuando pregunten por qué la skill decide algo, o antes de cambiar un número |
| `references/changelog.md` | antes de deshacer algo que parece raro: ahí está por qué existe |
| `scripts/construir_ebook.py` | construye el PDF y la portada desde el `ebook.json` |
| `scripts/revision_fuentes.py` | arma la hoja del Paso 5b con todas las frases del libro; C25 la exige completa |
| `scripts/verificar_ebook.py` | la compuerta de entrega: 38 comprobaciones, 39 con `--online` |
| `scripts/autoprueba.py` | prueba motor y verificador en las dos direcciones (el conteo crece con cada sabotaje nuevo; ver `TODO OK · N de N` al correrlo) |
| `scripts/guardar_fuentes.py` | Paso 5b: baja y guarda en `EBOOK/fuentes-texto/<id>.txt` el texto real de cada fuente, para que `revision_fuentes.py` y C25 puedan comprobar la `cita_fuente` contra el texto guardado y no contra la memoria de quien escribió |
| `assets/muestra/ebook.json` y `logo-demo.png` | ebook completo y válido de una marca de demostración: punto de partida y fixture de la autoprueba (no editar su texto) |
| `assets/fuentes/` | Lora (cuerpo), Outfit (rótulos) y Gloock (títulos), estáticas, con licencia OFL |
