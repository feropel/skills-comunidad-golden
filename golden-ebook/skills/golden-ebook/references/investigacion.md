# Protocolo de investigación

Lee este archivo en el **Paso 3**. La regla que lo gobierna: **ningún número entra al libro sin
una fuente que lo diga, leída por ti, no por el buscador.**

## Por qué se lee el original

El resumen del buscador inventa con facilidad. Medido al construir esta skill: una búsqueda
devolvió "una revisión de 2015 en el Journal of the American Academy of Dermatology" que no aparece
en ninguna fuente primaria; al leer el estudio real (gemelos idénticos, 2013) la conclusión era
otra y más interesante. Un resumen de buscador es una pista para encontrar la fuente, **nunca** la
fuente.

## Jerarquía de fuentes

| Nivel | Qué es | Ejemplos |
|---|---|---|
| **A** | Revista científica revisada por pares, entidad médica u oficial, norma | PubMed, DOI de revistas, OMS, INVIMA, academias médicas (AAD, AAP), ministerios |
| **B** | Hospital o universidad que divulga | Cleveland Clinic, Mayo Clinic, UAMS, sitios .edu |
| **C** | Medio de salud o divulgación con revisión médica declarada | Medical News Today, Healthline |
| No sirve | Blog de marca que vende el producto, foros, redes, contenido sin autor | tiendas, "clínicas" que venden el tratamiento |

Mínimo que el verificador exige (C5): **5 fuentes y al menos 1 de nivel A**. Lo recomendado:
**8 o más y 3 de nivel A**. Si el tema no da para eso, el tema está mal elegido: vuelve al
Paso 2 antes de rellenar con fuentes flojas.

## Herramientas, en orden

1. **WebSearch** para encontrar candidatos, restringiendo dominios cuando sepas cuál es la
   autoridad (`allowed_domains: ["aad.org"]`).
2. **WebFetch** para leer la página y extraer la frase exacta que sostiene el dato.
3. **PubMed por su API oficial** cuando la web de PubMed pide cookies (medido: WebFetch no la lee):
   ```bash
   E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
   curl -s -G "$E/esearch.fcgi" --data-urlencode "db=pubmed" --data-urlencode "retmode=json" \
     --data-urlencode "term=identical twins alopecia"
   curl -s -G "$E/efetch.fcgi" --data-urlencode "db=pubmed" --data-urlencode "id=PMID" \
     --data-urlencode "rettype=abstract" --data-urlencode "retmode=text"
   ```
4. **Crossref** para confirmar que un artículo viejo existe y sacar su DOI:
   `curl -s "https://api.crossref.org/works?query.bibliographic=TITULO+AUTOR&rows=3"`
5. Si están conectados, `firecrawl_search` y las herramientas `firecrawl_research_*` sirven para
   literatura biomédica.

**Plan B sin red:** si ninguna herramienta web responde, no escribas datos. Construye el libro solo
con lo que ya esté verificado en el disco (dossier de `golden-investigacion-mercado`, estudios
guardados) y declara en el informe cuántas fuentes quedaron sin verificar. Un ebook con datos
inventados es peor que no mandar ebook.

## La ficha de cada fuente

Cada fuente entra al `ebook.json` así:

```json
{"id": 3, "titulo": "Título original, sin traducir",
 "editor": "Autores o entidad, revista y volumen", "anio": 2013,
 "url": "https://doi.org/...", "nivel": "A", "consultado": "AAAA-MM-DD"}
```

- Para artículos científicos, usa el enlace `https://doi.org/...`: no se rompe cuando la revista
  cambia de web.
- `consultado` es la fecha en que TÚ la leíste, en formato AAAA-MM-DD (C6 rechaza fechas futuras).
- Si marcas nivel A una fuente cuyo dominio no es oficial ni académico (.gov, .edu, .int, doi.org),
  escribe en `nivel_porque` qué la hace A ("academia médica profesional", "instituto público de
  investigación"). Sin eso C21 avisa: el nivel es lo que más se infla al escribir con prisa.
- El título va en su idioma original. El texto del libro sí va en español.

## Qué se puede decir con cada tipo de dato

| El estudio dice | En el libro se escribe | Nunca se escribe |
|---|---|---|
| una encuesta | "una encuesta encontró que el X % ..." y quién la hizo | "el X % de las personas" a secas |
| un estudio con N personas | el N y el país si importa | "está comprobado" |
| una recomendación de una entidad | "la Academia X recomienda" | "los expertos dicen" sin nombrar |

Las formas de exagerar que más aparecieron están en el Paso 5b del SKILL.md: ahí se revisan
frase por frase.

Nombrar la fuente dentro de la frase ("según la Academia Americana de Dermatología") además del
número entre corchetes le da al lector confianza sin obligarlo a ir al final del libro.

## Antes de pasar al Paso 4

Guarda en la carpeta del proyecto un `fuentes-verificadas.md` con una línea por fuente: la frase
exacta que leíste y el dato que sale de ella. Es tu control: si una frase del libro no tiene su
línea aquí, no entra.
