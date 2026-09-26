# Changelog de golden-ebook

## EB1.4 · 2026-09-20 · tercera auditoría (golden-skill-auditor)

Dos hallazgos reales, sin sabotaje adversarial de por medio, solo de leer el SKILL.md contra lo
que el disco realmente hace:

1. **Número fijo que ya no era cierto.** SKILL.md citaba `68 de 68` en cuatro sitios; correr
   `autoprueba.py` hoy da `89 de 89` (el conteo crece con cada sabotaje nuevo que se añade al
   arreglar un caso real). El texto decía además, literal: "Si no [imprime 68 de 68], no
   construyas" — una instrucción que, leída al pie de la letra, bloquea toda corrida futura en
   cuanto el conteo avanza. Se cambió a `N de N` (mismo N en las dos partes) en vez de fijar la
   cifra.
2. **Un paso del flujo sin su script.** El Paso 5b mandaba a `revision_fuentes.py` y a abrir
   `fuentes-verificadas.md`, pero nunca a `scripts/guardar_fuentes.py` — pese a que C25 (la
   compuerta que exige la hoja del Paso 5b) compara la `cita_fuente` contra el texto literal de
   `EBOOK/fuentes-texto/<id>.txt`, que solo existe si ese script corrió antes. El propio mensaje
   de FALLA de C25 ya decía "corre scripts/guardar_fuentes.py", así que el flujo se recuperaba
   solo en la práctica, pero un modelo que sigue el SKILL.md de punta a punta sin tropezar antes
   no tenía por qué saber que ese script existía. Se agregó como paso explícito antes de
   `revision_fuentes.py` y su fila en "Archivos de apoyo".

Verificado: `validar_arsenal.py` exit 0, inventario.sh sin referencias rotas ni huérfanos nuevos,
`autoprueba.py` 89/89 tras el cambio (el motor y el verificador no se tocaron, solo la
documentación). Sin blindar: la skill sigue sin dueño de fábrica declarado.

## EB1.3 · 2026-09-18 · segunda auditoría (885/1000) y segunda verificación adversarial

Diez casos malos del calificador y once de doce sabotajes del verificador pasaban; cinco casos
sanos se acusaban en falso. La conclusión que cambió el diseño: **un detector de palabras nunca es
completo**, falla en los dos sentidos. Se hicieron dos cosas:

1. **La revisión humana pasó a ser una compuerta verificable.** `revision_fuentes.py` arma la hoja
   con TODAS las frases del libro; C25 no aprueba sin la hoja completa, con nota por frase, el
   puente revisado y el sha256 del JSON actual. En los dos ebooks reales, esa lectura encontró más
   de veinte frases que decían más que su fuente o que no tenían ninguna (entre ellas "las dos
   pruebas toman minutos", falsa: la del medidor dura dos horas).
2. **El piso automático se endureció por clase:** el aviso legal ya no está exento; negación solo de
   alcance inmediato (dos palabras) y "no solo" no niega; caracteres invisibles; marcadores
   genéricos `[MAYÚSCULAS]` y `<MAYÚSCULAS>`; homógrafos fuera de la lista de tildes y regla "-ción";
   abreviaturas que no cortan frase; inglés por frase, fuera de las cursivas; "garantizado" y
   "milagro" solo junto al producto, pero el ADJETIVO ("milagroso", "resultados garantizados") en
   todo el libro (al moverlos se perdió "remedio milagroso": fallo simétrico, cazado por el caso 4);
   verbos de efecto en toda frase que hable del producto; cifras en palabras, con miles y "veces";
   datos privados (C20); fecha y nivel de las fuentes (C6, C21); sello del JSON en el PDF (P12);
   tamaño del logo (P13); largo del título, del capítulo y "Pruébalo hoy" (C22 a C24); un 404 de
   Crossref es FALLA, no aviso.
3. **Motor:** fondo de marca en el margen de cada página y logo de hasta 26 mm.
4. **Contenido:** el ebook del filtro dejó de presentar datos de Bogotá como si fueran de todo el
   país, y su capítulo 6 dejó de armar el puente "ahorrar agua en la cocina → filtro". Los mensajes
   de entrega ya no dicen "el favorito de muchos": dicen los minutos reales del capítulo.

Autoprueba: 42 → 68 casos.

## EB1.2 · 2026-09-17 · verificación adversarial: 14 de 22 sabotajes se colaban

El agente golden-verificador coló 14 sabotajes en ENTREGABLE. Se arreglaron por CLASE, no por caso,
y cada sabotaje quedó como caso de la autoprueba: los 14 que se colaron más dos variantes (doble puntuación y catálogo de 5 menciones) son los casos 24 a 39, y el 40 es un falso positivo de C3 que cazó el segundo ebook real al cortar frases en el punto y coma (total 42):

- **Campos visibles sin revisar.** `textos()` enumeraba campos a mano y dejó fuera los rótulos de
  carta y cierre: un "CURA LA ALOPECIA HOY" salió impreso en un PDF aprobado. Ahora recorre el JSON
  ENTERO y excluye solo lo que no se imprime (`NO_VISIBLES`).
- **Claims por lista literal.** "frena la caída", "detener la caída", "trata tu alopecia" pasaban.
  Ahora se buscan por raíz sobre el texto sin tildes, y junto al producto (carta, cierre, botón,
  rótulos) cualquier verbo de efecto es FALLA.
- **Negación demasiado ancha.** "No lo dudes más: esto hace crecer el pelo" se eximía. La negación
  vale solo dentro de la misma cláusula (sin puntuación de por medio, 30 caracteres).
- **Checks nuevos:** C9 en los dos sentidos y sin doble puntuación; C3 exige [n] a todo porcentaje;
  C6 exige URL completa; C11 pasa a FALLA con 5 menciones y avisa alusiones al pedido; C17 palabras
  sin tilde; C18 texto en inglés; C19 tipos de bloque. P7 mide también el nombre de la empresa en
  la miniatura. W1 confirma los DOI en Crossref (probado: muerde un DOI inventado con 404).
- **Render:** la cita se pega a su palabra y el % a su número (se separaban de línea); los rótulos
  en versales ya no se parten con guion; la portada lleva el nombre de la empresa más grande.
- **Contenido del primer ebook:** seis frases decían más que su fuente (asociación como causa,
  "más de" por "unos o más", "cada" por "al menos cada", un síntoma añadido, una conclusión que los
  autores no escribieron). Se corrigieron y nació el **Paso 5b** (leer el texto contra sus fuentes),
  porque esa clase de fallo no la ve ningún detector de palabras.
- **Decisión de estándar:** en carta y cierre se dice del producto solo lo que está en sus claims
  permitidos, con esas palabras. "Cubre al instante" es un efecto visual permitido, no una proclama.

## EB1.1 · 2026-09-17 · primera auditoría (870/1000) y sus arreglos

La auditoría con golden-skill-auditor dio 870 (PLATA) y un hallazgo crítico. Arreglos, cada uno
con su caso en la autoprueba (15 → 25 casos):

- 🔴 C7 solo miraba la PRIMERA aparición de un claim del producto: "Ningún champú detiene la caída.
  Pero este producto detiene la caída" salía ENTREGABLE. Ahora recorre todas (caso 15).
- El acento se pinta como texto sobre el primario y nadie lo medía: C13 exige 4,5:1 también ahí (16).
- Un N/D (falta una librería) terminaba en ENTREGABLE. Ahora es NO VERIFICADO, código 3 (23).
- Portada sin logo: el motor lo avisa por pantalla y P6 da AVISO (21). La muestra trae un logo de
  demostración para probar también el camino con logo (0b).
- Casos nuevos para C1, C5, C12, C16 y P11 (17 a 22). La autoprueba borra su carpeta temporal.
- C7 gana patrones de suplementos y bienestar y declara su alcance en `cumplimiento.md`.
- Description sin "lead magnet" ni "guía descargable": son captación antes de la compra y la
  skill hace el regalo después. Regla de empate única. Lenguaje apto para la comunidad.
- **Blindaje:** la skill queda SIN blindar mientras está en obra; al cerrarla, el mecanismo previsto
  es `chflags -R uchg` sobre la carpeta, como las demás skills estables de la casa.

## EB1.0 · 2026-09-17 · nacimiento

Pedido de FER: una skill que haga ebooks para mantener caliente al cliente entre la guía generada y
la entrega, sobre un tema adyacente al producto, con portada, logo y nombre de la empresa, para usar
en Golden y compartir con la comunidad.

**Inventario previo:** 184 skills en disco, ninguna de ebooks. `anthropics/skills` tampoco trae una
(19 skills revisadas); la más cercana de la comunidad (`ebook-publishing-skill`, MIT) está pensada
para vender libros, no para un bonus de marca. Se reutilizan: el entorno `~/.golden/pdfenv` y la
lección de fuentes estáticas de `golden-pdf-check`, las fuentes OFL de `canvas-design` y la
convención de cerebros de `golden-brand-brain`.

**Por qué un motor propio y no `golden-pdf-check`:** esa skill es el estándar de informes y PDFs de
prompts (A4, tarjetas atómicas, texto del usuario intocable). Un ebook necesita otra cosa: página del
tamaño de una pantalla, portada y aperturas a sangre, y un contenido que la skill ESCRIBE. Se
declara al Centro de Mando porque la regla global dice que todo PDF entregable pasa por
`golden-pdf-check`.

**Lo que midió el primer ebook real** (Fibra Capilar, Golden Group Enterprise, 6 capítulos, 10
fuentes verificadas leyendo el original, 40 páginas, 0,74 MB):

1. Las líneas del arte de portada cruzaban el título. El arte se movió al tercio superior con una
   máscara que se desvanece antes del texto.
2. Chromium partía títulos con guion ("ca-mino"). Títulos sin separación silábica.
3. La frase de cierre de un capítulo caía sola en una página (3 de 40). El cierre viaja pegado al
   último bloque.
4. Chromium arma los marcadores del PDF comiéndose el espacio del salto de línea ("tecontó"). El
   motor los arma desde el JSON y P11 compara el título exacto.
5. Carta y cierre desbordaban por unas pocas líneas: nació C16 (90 y 80 palabras en móvil). Probado
   en los dos sentidos: acusó la versión de 108 y 106 palabras y dejó pasar la de 76 y 67.
6. La carta citaba el mito "afeitarse hace crecer el pelo" y cayó en C7. Se corrigió el texto, no
   el chequeo: para citar un mito está el bloque `mito`.

**Defectos del propio verificador, cazados al correrlo contra el caso real:**

- `TODO` como marcador acusaba la palabra "todo" 7 veces. Los marcadores en mayúscula se buscan
  respetando la caja (caso 12 de la autoprueba).
- Acusaba acentos "perdidos" que eran rótulos en VERSALES y palabras partidas por guion. Compara en
  minúscula y une los guiones de fin de línea.
- No reconocía el enlace del botón porque Chromium le añade una barra final a la URL.
- "Ningún cosmético cura la alopecia" caía como claim: faltaba "ningún" entre las negaciones
  (caso 11). Al arreglarlo se probó añadir "sin" y se descartó: dejaría pasar "Sin duda, cura la
  alopecia" (caso 14).

**Investigación de base:** informe en la carpeta del primer ebook y resumen anclado en
`references/evidencia.md`.
