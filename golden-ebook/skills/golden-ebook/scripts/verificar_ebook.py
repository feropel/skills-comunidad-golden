#!/usr/bin/env python3
"""verificar_ebook.py · golden-ebook

Compuerta de entrega: revisa el ebook.json (contenido) y el PDF construido
(render) y dice qué pasa, qué falla y qué no se pudo verificar.

Uso:
    $PY scripts/verificar_ebook.py ebook.json ebook.pdf [--json informe.json]
                                   [--online]

--online  abre cada URL de fuentes y acusa las que no respondan (requiere red).

Códigos: 0 ENTREGABLE (puede haber avisos) · 1 NO ENTREGAR (hay fallas) · 2 error de uso
        · 3 NO VERIFICADO (algo quedó N/D: falta una librería y esa parte no se midió).
Cada comprobación sale OK, AVISO, FALLA o N/D. N/D no dice que el ebook esté mal, pero
tampoco lo aprueba: instala lo que falta y vuelve a correr.

Lo que NINGÚN detector de palabras ve: una proclama implícita armada entre capítulos, o
una frase que exagera su fuente. Esa lectura es del Paso 5b de la skill, no de este script.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from construir_ebook import FORMATOS, TIPOS_BLOQUE, contraste, texto_sobre, hex_rgb, REF  # noqa: E402

PT_MM = 0.352778
JSON_RUTA = ""  # la fija main(): P12 compara el sello del PDF con este archivo

# Los marcadores en MAYÚSCULA se buscan sin ignorar la caja: "TODO" es un marcador,
# "todo" es una palabra del español (medido: 7 falsos positivos en el primer ebook real).
MARCADORES = [r"\[PENDIENTE", r"(?-i:\bTODO\b)", r"\blorem ipsum\b", r"(?-i:\bXXX+\b)", r"\{\{",
              r"\[WHATSAPP", r"\[PRECIO", r"\[COSTO", r"\[FOTOS", r"(?-i:\bINSERTAR\b)",
              # genéricos: la segunda verificación coló "<NUMERO DE WHATSAPP>" y "[NOMBRE DEL ASESOR]"
              r"(?-i:\[[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ _/-]{3,}\])", r"(?-i:<[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ _/-]{2,}>)"]
# Caracteres invisibles (guion suave, espacios de ancho cero): se usan para partir una palabra
# prohibida sin que se vea ("cre\u00adcer"). Un texto limpio no los necesita.
INVISIBLES = re.compile("[\u00ad\u200b\u200c\u200d\u2060\ufeff]")
# Letras de otros alfabetos que se parecen a las latinas ("cura" con "а" cirílica): en un texto en
# español no tienen por qué estar, y sirven para esquivar cualquier detector de palabras.
HOMOGLIFOS = re.compile("[\u0370-\u03ff\u0400-\u04ff\u0500-\u052f]")
# Plantillas de números o enlaces sin llenar ("57XXXXXXXXXX").
MARCADORES.append(r"(?-i:X{4,})")

# Proclamas que un cosmético o un artículo de hogar no puede hacer (Decisión 833 de la CAN,
# arts. 3 y 48; Ley 1480 art. 30). Se escriben SIN tildes porque se buscan sobre el texto
# normalizado, y por RAÍZ, no por frase exacta: la primera versión buscaba "hace crecer" y
# dejaba pasar "estimula el crecimiento" y "frena la caída" (verificación adversarial).
TERAPEUTICOS = [
    r"\bcur(?:a|an|ar|ara|acion)\b",
    # El ADJETIVO es proclama en cualquier parte ("remedio milagroso", "resultados garantizados");
    # el sustantivo usado como figura ("parece un milagro") no lo es.
    r"\bmilagros[oa]s?\b", r"\bresultados? garantizad\w*", r"\bgarantia de resultados\b",
    r"\b100\s?%\s?(?:efectiv|garantiz|segur)", r"\belimina\w* (?:para siempre|definitivamente)",
    r"\bsin efectos secundarios\b", r"\bclinicamente (?:probado|comprobado)",
    r"\btrat\w* (?:tu|la|el|su|sus|tus) (?:alopecia|acne|psoriasis|dermatitis|calvicie|caida)",
    r"\bhace\w* crecer\b", r"\bestimul\w* (?:el |tu )?crecimiento", r"\bregener\w* (?:el |tu )?(?:cabello|pelo)",
    r"\bfren\w* (?:la |tu )?caida", r"\bdet(?:ien|en)\w* (?:la |tu )?caida", r"\brecuper\w* (?:el |tu |su )(?:pelo|cabello)",
    r"\bsoluciona\w* para siempre", r"\bpotabiliz\w*", r"\bpurific\w* (?:el |tu )?agua",
    r"\b(?:combat\w*|acab\w* con|lucha\w* contra|adios a|dile adios a)\b[^.]{0,25}"
    r"(?:calvicie|caida|alopecia|acne|manchas|arrugas|celulitis|grasa|bacterias|virus)",
    r"\belimina\w* (?:bacterias|virus|metales|contaminantes)",
    # suplementos, bienestar y dispositivos
    r"\badelgaz\w*", r"\bquema\w* grasa", r"\breduce\w* medidas\b", r"\bdesintoxic\w*", r"\bdetox\b",
    r"\bsustituye (?:al|el) (?:medico|tratamiento)",
]
# Verbos de EFECTO: prohibidos solo donde aparece el producto (carta, cierre, rótulos,
# subtítulo, botón). Ahí cualquier "recupera", "soluciona" o "protege" se lee como promesa.
VERBOS_EFECTO = re.compile(
    r"\b(?:solucion\w*|recuper\w*|elimin\w*|deten\w*|detien\w*|fren\w*|cura(?:r|n)?\b|trata(?:r|n)?\b(?! de)|"
    r"mejora(?:r|n)?\b|previen\w*|preven\w*|proteg\w*|repar\w*|fortalec\w*|regener\w*|estimul\w*|"
    r"purific\w*|potabiliz\w*|potabl\w*|combat\w*|garantiz\w*|milagro\w*|alivi\w*|"
    r"calma(?:r|n)?\b|desinflam\w*|reduce\w* (?:la )?inflamacion|sana(?:r|n)?\b|"
    r"agua (?:segura|pura|limpia))")
CAMPOS_CON_PRODUCTO = ("bienvenida", "cierre", "meta.subtitulo", "portada", "aviso")
# Frases que hablan del producto sin nombrarlo: también las vigila C7 y las cuenta C11.
PRODUCTO_GENERICO = r"\b(?:este|nuestro|el|nuestra|esta) (?:producto|articulo|formula|accesorio)\b"
# La negación exime solo dentro de la MISMA cláusula: "No lo dudes más: la fibra hace
# crecer" se coló con la regla vieja de 40 caracteres a través de los dos puntos.
# "No solo cura" AFIRMA que cura: esas locuciones no niegan (caso de la segunda auditoría).
NEGACION = re.compile(r"\b(?:no(?!\s+(?:solo|solamente|unicamente|nada mas|dud\w*|cabe duda|hay duda|te preocupes|"
                      r"esperes mas|lo pienses)\b)|ni|nunca|jamas|tampoco|"
                      r"ningun|ninguna|ninguno)\b(?:\s+[^\s.,;:!?¡¿]+){0,2}\s*$")
RAYAS = re.compile(r"^\s*(?:[-_=—–*━─═~·•]\s*){3,}\s*$", re.M)
# Palabras que en español SIEMPRE llevan tilde: si aparecen sin ella, el texto se escribió
# sin acentos (el render no lo puede ver porque copia lo que recibe).
EXTRA_TILDE = r"|proxim[oa]s?|sera|seran|estan|estaran|tendra|tendran|podra|podran|habra|haran|sabras|vendra"
SIN_TILDE = re.compile(r"\b(?:tambien|despues|asi|aqui|alli|facil|dificil|rapido|informacion|ademas|"
                       r"traves|segun|ultimo|ultima|util|utiles|caida|numero|articulo|medico|medica|"
                       r"telefono|dia|dias|pagina|capitulo|habitos|metodo|proposito|"
                       r"razon|corazon|todavia|podria|deberia|podrias|deberias|"
                       r"\w+[cs]ion|economic[oa]|opcion" + EXTRA_TILDE + r")\b")
# Inglés por FRASE: dos palabras inglesas y ninguna palabra funcional del español. El umbral
# viejo (3 de una lista corta) dejó pasar "Stay confident every single day."
INGLES = re.compile(r"\b(?:the|and|of|to|is|your|with|for|this|that|you|are|every|day|stay|get|our|"
                    r"best|more|now|just|can|will|it|be|at|by|from|have|was|were|my|we|they|single|"
                    r"confident|care|hair|skin|water|free|new|all|how|why|what)\b", re.I)
ESPANOL = re.compile(r"\b(?:de|la|que|el|en|y|los|las|del|por|con|para|una|un|es|se|su|tu|lo|al|como|"
                     r"mas|pero|sus|le|ya|o|este|esta|muy|sin|sobre|todo)\b", re.I)
ABREVIATURAS = re.compile(r"\b(?:EE\. ?UU|Dr|Dra|Sr|Sra|etc|p\. ?ej|pág|núm|aprox|a\. ?m|p\. ?m|vs|No|Nro|Cía|S\.A\.S|S\.A)\.")
# Cuantificadores que afirman algo aunque no traigan número: una frase con ellos no puede
# marcarse "sin afirmacion" en la hoja del Paso 5b (tercera verificación adversarial).
CUANTIFICADORES = re.compile(r"\b(?:casi nadie|nadie|todo el mundo|la mayoria|la mitad|el doble|miles de|"
                             r"millones de|cientos de|decadas|siglos?|el mas|la mas|los mas|las mas|"
                             r"\w+isim[oa]s?|nunca antes|siempre)\b")
_NUM = r"(?:\d+|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)"
CIFRA = re.compile(r"\d+(?:[.,]\d+)?\s?%|\b" + _NUM + r" de cada " + _NUM + r"\b|\b\d+(?:[.,]\d+)? por ciento\b|"
                   r"(?<![$\d.])(?<!\$ )\b\d{1,3}(?:\.\d{3})+\b|\b\d+(?:[.,]\d+)? (?:millones|mil millones|veces)\b|"
                   r"\bla mitad de\b|\bel doble de\b|\b(?:cientos|miles|millones) de personas\b", re.I)
# Datos privados: un libro que se reparte no lleva cédulas, celulares, correos personales,
# direcciones ni números de pedido (segunda auditoría: cinco de ellos pasaron juntos).
PRIVADOS = [(r"\b3\d{2}[\s.-]?\d{3}[\s.-]?\d{4}\b|\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}",
             "teléfono"),
            (r"[\w.+-]+@[\w-]+\.[\w.]+", "correo"),
            (r"\bc[eé]dula\b|\bc\.\s?c\.", "cédula"),
            (r"\b(?:calle|carrera|cra|kr|cl|cll|avenida|av|transversal|tv|diagonal|dg)\.?\s+\d+\w*\s*(?:#|no\.?\s)",
             "dirección"),
            (r"\bpedido\s*(?:n[°º.o]?\s*)?#?\s*\d{3,}", "número de pedido")]
DOMINIOS_A = (".gov", ".gov.co", ".edu", ".edu.co", ".int", ".mil", "doi.org", "ncbi.nlm.nih.gov")
URL_VALIDA = re.compile(r"^https://[^/\s.]+(?:\.[^/\s.]+)+(?:/\S*)?$")

# Llaves que NO se imprimen. Todo lo demás del JSON se trata como texto visible: la regla
# vieja enumeraba campos a mano y dejó sin revisar los rótulos de carta y cierre.
NO_VISIBLES = {"url", "id", "nivel", "consultado", "logo", "colores", "fuente_de_verdad", "formato",
               "idioma", "palabras_clave", "ruta", "imagen", "producto", "tema", "anio", "fuente",
               "tipo", "_nota"}


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def norm(t):
    return sin_tildes(INVISIBLES.sub("", t)).casefold()


class Informe:
    def __init__(self):
        self.filas = []

    def add(self, estado, cid, desc, detalle=""):
        self.filas.append({"estado": estado, "id": cid, "desc": desc, "detalle": detalle})

    def ok(self, cid, desc, detalle=""):
        self.add("OK", cid, desc, detalle)

    def aviso(self, cid, desc, detalle):
        self.add("AVISO", cid, desc, detalle)

    def falla(self, cid, desc, detalle):
        self.add("FALLA", cid, desc, detalle)

    def nd(self, cid, desc, detalle):
        self.add("N/D", cid, desc, detalle)


# ---------------------------------------------------------------- recorrido del texto
def textos(e):
    """(ruta, campo, texto, con_fuente) de TODO texto que se imprime.

    Se recorre el JSON entero y se excluye solo lo que no se imprime (NO_VISIBLES).
    `con_fuente` marca los campos de un bloque dato o mito que ya declara su fuente.
    """
    out = []

    def andar(nodo, ruta, campo, con_fuente):
        if isinstance(nodo, dict):
            cf = con_fuente or (nodo.get("tipo") in ("dato", "mito") and nodo.get("fuente") is not None)
            for k, v in nodo.items():
                if k in NO_VISIBLES:
                    continue
                andar(v, f"{ruta}.{k}" if ruta else k, k, cf)
        elif isinstance(nodo, list):
            for i, v in enumerate(nodo, 1):
                andar(v, f"{ruta}[{i}]", "item" if isinstance(v, str) else campo, con_fuente)
        elif isinstance(nodo, str) and nodo.strip():
            out.append((ruta, campo, nodo, con_fuente))

    andar({k: v for k, v in e.items() if k != "fuentes"}, "", "", False)
    for f in e.get("fuentes", []):
        for k in ("titulo", "editor"):
            if f.get(k):
                out.append((f"fuentes[{f.get('id')}].{k}", "fuente", str(f[k]), True))
    return out


def es_de_producto(ruta):
    return ruta.startswith(CAMPOS_CON_PRODUCTO)


def frases(t):
    # Una frase termina en . ? o !, no en ; ni en : (medido: "subió del 50 % al 60 %; en las
    # ciudades se estancó [6]" se partía en el punto y coma y el porcentaje quedaba sin su cita).
    # Las abreviaturas ("EE. UU.", "Dr.") no cierran frase: se protegen antes de cortar.
    t = ABREVIATURAS.sub(lambda m: m.group(0).replace(".", "\u2024"), t)
    return [f.replace("\u2024", ".") for f in re.split(r"(?<=[.?!])\s+|\n+", t) if f.strip()]


def frases_a_revisar(e):
    """(ruta, frase, [fuentes]) que el Paso 5b debe leer contra su fuente.

    Entran TODAS las frases que el lector ve, menos títulos, rótulos, firmas y autores de cita;
    cada bloque dato o mito va completo y con su fuente.
    La usan revision_fuentes.py (para armar la hoja) y C25 (para exigirla completa).
    """
    caps = e.get("capitulos", [])
    out = []
    for ruta, campo, t, cf in textos(e):
        if campo == "fuente":
            continue
        if cf:
            m = re.match(r"capitulos\[(\d+)\]\.bloques\[(\d+)\]", ruta)
            if not m or campo in ("cifra", "mito"):
                continue
            bl = caps[int(m.group(1)) - 1]["bloques"][int(m.group(2)) - 1]
            frase = f"{bl.get('cifra', '')} {t}".strip() if bl.get("tipo") == "dato" else \
                f"Mito: {bl.get('mito', '')} Evidencia: {t}"
            out.append((ruta, frase, [str(bl.get("fuente"))]))
            continue
        if campo in ("firma", "autor", "nombre", "web") or (campo == "kicker" and len(t.split()) <= 3):
            continue
        # TODAS las frases, no solo las citadas: una frase sin [n] también afirma cosas, y en
        # el primer ebook las exageraciones sin cita pasaron igual que las citadas.
        for fr in frases(t):
            refs = [i.strip() for m in REF.finditer(fr) for i in m.group(1).split(",")]
            out.append((ruta, fr.strip(), refs))
    return out


# Las fuentes escriben muchas cifras en letras ("six to nine months"): también cuentan como número.
NUMERO_PALABRA = re.compile(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|"
                            r"forty|fifty|hundred|thousand|million|billion|half|dozen|uno|una|dos|tres|cuatro|"
                            r"cinco|seis|siete|ocho|nueve|diez|cien|mil|millon|millones|mitad)\b")


def datos_de(frase):
    """La frase sin sus marcas de cita [n] ni referencias internas ("capítulo 4"): lo que queda
    con dígitos es un dato. Medido: "[2]" contaba como número y exigía un número en la cita."""
    return re.sub(r"cap[ií]tulos? \d+", "", REF.sub("", frase), flags=re.I)


def plano_cita(t):
    """Texto normalizado para buscar una cita: sin tildes, minúsculas, comillas y guiones unificados,
    espacios colapsados. Así una cita copiada de la página se encuentra aunque cambie el formato."""
    t = norm(t).replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    t = re.sub(r"[\u2010-\u2015]", "-", t)
    return re.sub(r"\s+", " ", t).strip()


def excepciones_de_hoja(e):
    """Frases que la hoja marca con una excepción de claim revisada (solo si la hoja es de ESTE JSON)."""
    if not JSON_RUTA:
        return {}
    import hashlib
    ruta = os.path.join(os.path.dirname(os.path.abspath(JSON_RUTA)), "revision-fuentes.json")
    try:
        hoja = json.load(open(ruta, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if hoja.get("ebook_sha256") != hashlib.sha256(open(JSON_RUTA, "rb").read()).hexdigest():
        return {}
    return {norm(f.get("frase", "")): f["excepcion_claim"] for f in hoja.get("frases", [])
            if len(str(f.get("excepcion_claim", ""))) >= 30}


def revisar_hoja(e, inf):
    """C25 · la hoja del Paso 5b existe, está completa y es de ESTA versión del ebook.json."""
    desc = "Paso 5b: cada frase del libro leída contra su fuente (revision-fuentes.json)"
    if not JSON_RUTA:
        return
    import hashlib
    hoja_ruta = os.path.join(os.path.dirname(os.path.abspath(JSON_RUTA)), "revision-fuentes.json")
    if not os.path.exists(hoja_ruta):
        inf.falla("C25", desc, "no existe: corre scripts/revision_fuentes.py y complétala")
        return
    try:
        hoja = json.load(open(hoja_ruta, encoding="utf-8"))
    except json.JSONDecodeError as ex:
        inf.falla("C25", desc, f"la hoja no es JSON válido: {ex}")
        return
    actual = hashlib.sha256(open(JSON_RUTA, "rb").read()).hexdigest()
    esperadas = [f for _, f, _ in frases_a_revisar(e)]
    en_hoja = [f.get("frase") for f in hoja.get("frases", [])]
    problemas = []
    if hoja.get("ebook_sha256") != actual:
        problemas.append("es de otra versión del ebook.json: vuelve a correr revision_fuentes.py")
    if sorted(esperadas) != sorted(en_hoja):
        problemas.append(f"no cubre las frases actuales ({len(en_hoja)} en la hoja, {len(esperadas)} en el libro)")
    carpeta = os.path.join(os.path.dirname(os.path.abspath(JSON_RUTA)), "fuentes-texto")
    textos_f = {}
    for f in e.get("fuentes", []):
        ruta_f = os.path.join(carpeta, f"{f.get('id')}.txt")
        if os.path.exists(ruta_f):
            textos_f[str(f.get("id"))] = plano_cita(open(ruta_f, encoding="utf-8").read())
    faltan_txt = [str(f.get("id")) for f in e.get("fuentes", []) if str(f.get("id")) not in textos_f]
    if faltan_txt:
        problemas.append("falta el texto guardado de las fuentes " + ", ".join(faltan_txt) +
                         ": corre scripts/guardar_fuentes.py")
    permitidos = plano_cita(" | ".join((e.get("producto") or {}).get("claims_permitidos", []) +
                                       [(e.get("producto") or {}).get("modo_uso", "")]))
    sin_revisar, sin_cita, mal_sin, citas = [], [], [], []
    for f in hoja.get("frases", []):
        fid, frase, est = str(f.get("id")), str(f.get("frase", "")), f.get("estado")
        if est not in ("fiel", "sin afirmacion"):
            sin_revisar.append(fid)
            continue
        nf = norm(frase)
        if est == "sin afirmacion":
            # Una frase con número, cita o cuantificador sí afirma algo: no puede ir aquí.
            # "capítulo 4" es una referencia interna del libro, no un dato.
            if re.search(r"\d", datos_de(frase)) or REF.search(frase) or CUANTIFICADORES.search(nf):
                mal_sin.append(fid)
            continue
        cita = plano_cita(str(f.get("cita_fuente", "")))
        usada = str(f.get("fuente_usada", ""))
        base = permitidos if usada == "producto" else textos_f.get(usada, "")
        refs = [i.strip() for m in REF.finditer(frase) for i in m.group(1).split(",")]
        ok = (len(cita) >= 20 and base and cita in base and (not refs or usada in refs or usada == "producto")
              and (not re.search(r"\d", datos_de(frase)) or re.search(r"\d", cita) or NUMERO_PALABRA.search(cita)
                   or usada == "producto"))
        if not ok:
            sin_cita.append(fid)
        else:
            citas.append(cita)
    if sin_revisar:
        problemas.append(f"{len(sin_revisar)} frases sin revisar: {', '.join(sin_revisar[:10])}")
    if mal_sin:
        problemas.append(f"{len(mal_sin)} frases con número, cita o cuantificador marcadas 'sin afirmacion': "
                         + ", ".join(mal_sin[:10]))
    if sin_cita:
        problemas.append(f"{len(sin_cita)} frases 'fiel' sin una cita literal (20+ caracteres) que exista en el "
                         f"texto guardado de su fuente, o sin su número: {', '.join(sin_cita[:10])}")
    if citas and len(set(citas)) / len(citas) < 0.5:
        problemas.append(f"las citas se repiten ({len(set(citas))} distintas para {len(citas)} frases): "
                         "cada frase se contrasta con SU pasaje, no con un resumen de la fuente")
    pu = hoja.get("puente") or {}
    if pu.get("estado") != "revisado" or len(str(pu.get("nota", ""))) < 15:
        problemas.append("falta revisar el puente capítulos → cierre")
    if problemas:
        inf.falla("C25", desc, "; ".join(problemas))
    else:
        inf.ok("C25", desc, f"{len(en_hoja)} de {len(esperadas)} frases revisadas y el puente")


# ---------------------------------------------------------------- contenido
def revisar_contenido(e, inf):
    caps = e.get("capitulos", [])
    n = len(caps)
    if n < 3 or n > 12:
        inf.falla("C1", "capítulos entre 3 y 12", f"tiene {n}")
    elif n < 4 or n > 9:
        inf.aviso("C1", "capítulos entre 4 y 9", f"tiene {n}: fuera del rango recomendado")
    else:
        inf.ok("C1", "capítulos entre 4 y 9", f"{n}")

    todos = textos(e)
    espanol = [t for t in todos if t[1] != "fuente"]

    fuentes = e.get("fuentes", [])
    ids = {str(f.get("id")) for f in fuentes}
    citadas, rotas = set(), []
    for ruta, _, t, _ in todos:
        for m in REF.finditer(t):
            for i in m.group(1).split(","):
                i = i.strip()
                citadas.add(i)
                if i not in ids:
                    rotas.append(f"[{i}] en {ruta}")
    sin_fuente = []
    for i, c in enumerate(caps, 1):
        for j, bl in enumerate(c.get("bloques", []), 1):
            if bl.get("tipo") in ("dato", "mito"):
                f = bl.get("fuente")
                if f is None:
                    sin_fuente.append(f"cap{i}.b{j} ({bl['tipo']})")
                else:
                    citadas.add(str(f))
                    if str(f) not in ids:
                        rotas.append(f"fuente {f} en cap{i}.b{j}")
    # Cifras sueltas: un porcentaje o un "X de cada Y" sin [n] en su frase es un dato sin fuente.
    for ruta, campo, t, con_fuente in espanol:
        if con_fuente or campo in ("kicker", "titulo") and ruta.startswith(("meta", "portada")):
            continue
        for fr in frases(t):
            if CIFRA.search(fr) and not REF.search(fr):
                sin_fuente.append(f"cifra sin [n] en {ruta}: '{fr.strip()[:50]}'")
    inf.falla("C2", "toda cita remite a una fuente listada", "; ".join(rotas)) if rotas else \
        inf.ok("C2", "toda cita remite a una fuente listada", f"{len(citadas)} fuentes citadas")
    inf.falla("C3", "todo dato, mito y porcentaje lleva fuente", "; ".join(sin_fuente[:8])) if sin_fuente else \
        inf.ok("C3", "todo dato, mito y porcentaje lleva fuente")
    huerf = sorted(ids - citadas, key=lambda x: int(x) if x.isdigit() else 0)
    inf.aviso("C4", "toda fuente listada se cita", "sin citar: " + ", ".join(huerf)) if huerf else \
        inf.ok("C4", "toda fuente listada se cita")

    total, nivel_a = len(fuentes), sum(1 for f in fuentes if f.get("nivel") == "A")
    malas_url = [str(f.get("id")) for f in fuentes if not URL_VALIDA.match(str(f.get("url", "")))]
    if total < 5 or nivel_a == 0:
        inf.falla("C5", "al menos 5 fuentes y una de nivel A", f"{total} fuentes, {nivel_a} de nivel A")
    elif total < 8 or nivel_a < 3:
        inf.aviso("C5", "8 fuentes o más, 3 de nivel A", f"{total} fuentes, {nivel_a} de nivel A")
    else:
        inf.ok("C5", "8 fuentes o más, 3 de nivel A", f"{total} fuentes, {nivel_a} de nivel A")
    import datetime
    hoy = datetime.date.today().isoformat()
    for f in fuentes:
        c = str(f.get("consultado", ""))
        try:
            real = datetime.date.fromisoformat(c).isoformat() == c
        except ValueError:
            real = False
        if not real or c > hoy:
            malas_url.append(f"{f.get('id')} (fecha de consulta '{c}' inválida o futura)")
    inf.falla("C6", "cada fuente con URL https completa y fecha de consulta real",
              "; ".join(malas_url)) if malas_url else \
        inf.ok("C6", "cada fuente con URL https completa y fecha de consulta real")
    # Nivel A declarado: se cree si el dominio es oficial o académico, o si la fuente dice por qué.
    dudosas = []
    for f in fuentes:
        if f.get("nivel") != "A" or f.get("nivel_porque"):
            continue
        host = re.sub(r"^https://([^/]+).*$", r"\1", str(f.get("url", "")))
        if not any(host == d.lstrip(".") or host.endswith(d if d.startswith(".") else "." + d) or host == d
                   for d in DOMINIOS_A):
            dudosas.append(f"{f.get('id')} ({host})")
    inf.aviso("C21", "el nivel A de cada fuente está justificado",
              "dominio no oficial ni académico, falta nivel_porque: " + ", ".join(dudosas)) if dudosas else \
        inf.ok("C21", "el nivel A de cada fuente está justificado")

    # C7 · claims: los del producto (por frase, todas las apariciones), los genéricos por raíz
    # y los verbos de efecto donde aparece el producto.
    prohib = [p for p in (e.get("producto") or {}).get("claims_prohibidos", []) if p]
    hall = []
    excep = excepciones_de_hoja(e)
    exceptuadas = []
    for ruta, campo, t, _ in espanol:
        if campo == "mito":
            continue
        # Cada frase exceptuada en la hoja (con motivo) sale del conteo de FALLA pero se lista.
        for fr in frases(t):
            if norm(fr.strip()) in excep:
                exceptuadas.append(f"{ruta}: '{fr.strip()[:50]}' ({excep[norm(fr.strip())][:60]})")
                t = t.replace(fr, " ")
        nt = norm(t)
        for p in prohib:
            for m in re.finditer(re.escape(norm(p)), nt):
                if not NEGACION.search(nt[:m.start()]):
                    hall.append(f"'{p}' en {ruta}")
                    break
        for pat in TERAPEUTICOS:
            for m in re.finditer(pat, nt):
                if not NEGACION.search(nt[:m.start()]):
                    hall.append(f"'{m.group(0)}' en {ruta}")
        nombres_p = [norm(x) for x in [(e.get("producto") or {}).get("nombre")] +
                     (e.get("producto") or {}).get("alias", []) if x]
        for fr in ([nt] if es_de_producto(ruta) else [
                f for f in frases(nt) if re.search(PRODUCTO_GENERICO, f) or
                any(re.search(r"\b" + re.escape(x) + r"\b", f) for x in nombres_p)]):
            for m in VERBOS_EFECTO.finditer(fr):
                if not NEGACION.search(fr[:m.start()]):
                    hall.append(f"verbo de efecto '{m.group(0)}' junto al producto en {ruta}")
    if hall:
        inf.falla("C7", "sin claims prohibidos ni terapéuticos", "; ".join(list(dict.fromkeys(hall))[:10]))
    elif exceptuadas:
        inf.aviso("C7", "sin claims prohibidos ni terapéuticos",
                  f"{len(exceptuadas)} excepciones revisadas en la hoja: " + "; ".join(exceptuadas[:4]))
    else:
        inf.ok("C7", "sin claims prohibidos ni terapéuticos",
               f"{len(prohib)} del producto + {len(TERAPEUTICOS)} raíces + verbos de efecto junto al producto")

    marc = [f"{pat} en {ruta}" for ruta, _, t, _ in todos for pat in MARCADORES if re.search(pat, t, re.I)]
    marc += [f"carácter invisible en {ruta}" for ruta, _, t, _ in todos if INVISIBLES.search(t)]
    marc += [f"letra de otro alfabeto en {ruta}" for ruta, _, t, _ in todos if HOMOGLIFOS.search(t)]
    urls = [str(f.get("url", "")) for f in e.get("fuentes", [])] + \
        [str(((e.get("cierre") or {}).get("cta") or {}).get("url", ""))]
    marc += [f"{pat} en una URL" for u in urls for pat in MARCADORES if re.search(pat, u, re.I)]
    inf.falla("C8", "sin marcadores por llenar", "; ".join(marc)) if marc else inf.ok("C8", "sin marcadores por llenar")

    # C9 · ortografía de documento, en los dos sentidos, y sin doble puntuación.
    orto = []
    for ruta, _, t, _ in espanol:
        for fr in frases(t):
            for cierre_, apertura in (("?", "¿"), ("!", "¡")):
                if (cierre_ in fr) != (apertura in fr):
                    orto.append(f"'{fr.strip()[:45]}' en {ruta}")
        if re.search(r"[?!]\.|(?<!\.)\.\.(?!\.)|\s[.,;:](?!\d)", t):
            orto.append(f"puntuación doble o suelta en {ruta}")
    inf.falla("C9", "signos de apertura y cierre completos, sin doble puntuación", "; ".join(orto[:8])) if orto else \
        inf.ok("C9", "signos de apertura y cierre completos, sin doble puntuación")

    rayas = [r for r, _, t, _ in todos if RAYAS.search(t)]
    inf.falla("C10", "sin líneas de rayas separadoras", ", ".join(rayas)) if rayas else \
        inf.ok("C10", "sin líneas de rayas separadoras")

    prod = e.get("producto") or {}
    nombres = [x for x in [prod.get("nombre")] + prod.get("alias", []) if x]
    menciones, alusiones = 0, []
    for ruta, _, t, _ in espanol:
        if not ruta.startswith("capitulos"):
            continue
        nt = norm(t)
        menciones += sum(len(re.findall(r"\b" + re.escape(norm(x)) + r"\b", nt)) for x in nombres)
        menciones += len(re.findall(PRODUCTO_GENERICO, nt))
        if re.search(r"\b(?:tu pedido|en camino|tu compra|lo que compraste|ya tienes algo)\b", nt):
            alusiones.append(ruta)
    if not nombres:
        inf.aviso("C11", "los capítulos no son un catálogo", "falta producto.nombre: no se pudo medir")
    elif menciones > 4:
        inf.falla("C11", "los capítulos no son un catálogo", f"el producto se nombra {menciones} veces en los capítulos")
    elif menciones > 2 or alusiones:
        inf.aviso("C11", "los capítulos no son un catálogo",
                  f"{menciones} menciones del producto; alusiones al pedido en {', '.join(alusiones) or 'ninguna'}")
    else:
        inf.ok("C11", "los capítulos no son un catálogo", f"{menciones} menciones del producto en capítulos")

    palabras = sum(len(t.split()) for _, c, t, _ in espanol)
    if palabras < 1500:
        inf.falla("C12", "largo entre 2.500 y 7.000 palabras", f"{palabras}: demasiado corto para ser un libro")
    elif palabras < 2500 or palabras > 7000:
        inf.aviso("C12", "largo entre 2.500 y 7.000 palabras", f"{palabras}")
    else:
        inf.ok("C12", "largo entre 2.500 y 7.000 palabras", f"{palabras} (~{round(palabras / 230)} min de lectura)")

    col = (e.get("marca") or {}).get("colores") or {}
    try:
        for k in ("primario", "acento", "fondo", "texto"):
            hex_rgb(col[k])
        c_txt = contraste(col["texto"], col["fondo"])
        c_ac = contraste(col.get("acento_texto") or col["acento"], col["fondo"])
        c_prim = contraste(texto_sobre(col["primario"], ("#FFFFFF", col["texto"], "#111111")), col["primario"])
        # El acento se pinta como TEXTO sobre el primario: rótulo de portada, título de
        # "Pruébalo hoy", web de la contraportada. También necesita 4,5:1.
        c_acp = contraste(col["acento"], col["primario"])
        malos = [f"{n} {v:.2f}:1" for n, v in (("texto/fondo", c_txt), ("acento de texto/fondo", c_ac),
                                               ("texto sobre primario", c_prim),
                                               ("acento/primario", c_acp)) if v < 4.5]
        inf.falla("C13", "contraste de texto 4.5:1 o más (WCAG)", "; ".join(malos)) if malos else \
            inf.ok("C13", "contraste de texto 4.5:1 o más (WCAG)",
                   f"texto {c_txt:.1f} · acento {c_ac:.2f} · portada {c_prim:.1f} · acento/primario {c_acp:.2f}")
    except (KeyError, ValueError) as ex:
        inf.falla("C13", "contraste de texto 4.5:1 o más (WCAG)", f"colores incompletos o inválidos: {ex}")

    puente = (e.get("tema") or {}).get("puente")
    inf.ok("C14", "el tema declara su puente con el producto") if puente else \
        inf.aviso("C14", "el tema declara su puente con el producto", "falta tema.puente")
    cta = ((e.get("cierre") or {}).get("cta") or {}).get("url", "")
    inf.ok("C15", "el cierre trae una llamada a la acción con URL") if URL_VALIDA.match(cta) else \
        inf.aviso("C15", "el cierre trae una llamada a la acción con URL", "falta cierre.cta.url https completa")

    # Carta y cierre son páginas únicas: en el formato móvil caben ~120 palabras por
    # página y el título se come ~30. Medido en el primer ebook real: 110 palabras de
    # carta y 115 de cierre desbordaron y dejaron dos páginas casi vacías.
    tope = {"movil": (90, 80), "a5": (170, 150)}.get((e.get("meta") or {}).get("formato", "movil"), (90, 80))
    largos = []
    for k, lim in (("bienvenida", tope[0]), ("cierre", tope[1])):
        nw = len(str((e.get(k) or {}).get("texto", "")).split())
        if nw > lim:
            largos.append(f"{k} {nw} palabras (máx. {lim})")
    inf.aviso("C16", "carta y cierre caben en una página", "; ".join(largos)) if largos else \
        inf.ok("C16", "carta y cierre caben en una página")

    tildes = [f"'{m.group(0)}' en {r}" for r, _, t, _ in espanol for m in SIN_TILDE.finditer(t)]
    inf.falla("C17", "sin palabras que pierdan su tilde", "; ".join(tildes[:8])) if tildes else \
        inf.ok("C17", "sin palabras que pierdan su tilde")

    ingles = []
    for r_, _, t, _ in espanol:
        for fr in frases(t):
            fuera = re.sub(r"\*[^*]+\*", "", fr)
            # Un título de obra en cursiva dentro de una frase en español es legítimo; una frase
            # entera en inglés metida en cursiva, no (tercera auditoría).
            evaluar = fuera if ESPANOL.search(fuera) else fr
            if len(INGLES.findall(evaluar)) >= 2 and not ESPANOL.search(evaluar):
                ingles.append(f"{r_}: '{fr.strip()[:40]}'")
    inf.falla("C18", "todo el texto visible está en español", "posible inglés en " + ", ".join(ingles[:6])) if ingles else \
        inf.ok("C18", "todo el texto visible está en español")

    web = re.sub(r"^(?:https?://)?(?:www\.)?", "", norm((e.get("marca") or {}).get("web", ""))).split("/")[0]
    privados = []
    for ruta, _, t, _ in todos:
        for pat, que in PRIVADOS:
            for m in re.finditer(pat, t, re.I):
                if que == "correo" and web and m.group(0).lower().rstrip(".").endswith("@" + web):
                    continue
                privados.append(f"{que} en {ruta}")
    inf.falla("C20", "sin datos privados (cédula, celular, correo, dirección, pedido)",
              "; ".join(dict.fromkeys(privados))) if privados else \
        inf.ok("C20", "sin datos privados (cédula, celular, correo, dirección, pedido)")

    tit = (e.get("meta") or {}).get("titulo", "")
    nt_ = len(tit.split())
    inf.aviso("C22", "título de 3 a 8 palabras y 45 caracteres o menos (miniatura)",
              f"{nt_} palabras, {len(tit)} caracteres") if not (3 <= nt_ <= 8 and len(tit) <= 45) else \
        inf.ok("C22", "título de 3 a 8 palabras y 45 caracteres o menos (miniatura)", f"{nt_} palabras")
    fuera, sin_prueba = [], []
    for i, c in enumerate(caps, 1):
        w = sum(len(t.split()) for r_, _, t, _ in espanol if r_.startswith(f"capitulos[{i}]"))
        if not 250 <= w <= 1000:
            fuera.append(f"cap{i} {w}")
        pruebas = [b for b in c.get("bloques", []) if b.get("tipo") == "prueba_hoy"]
        if len(pruebas) != 1 or not 2 <= len(pruebas[0].get("items", [])) <= 6:
            sin_prueba.append(f"cap{i}")
    inf.aviso("C23", "capítulos de 250 a 1.000 palabras", "; ".join(fuera)) if fuera else \
        inf.ok("C23", "capítulos de 250 a 1.000 palabras")
    inf.aviso("C24", "cada capítulo con un 'Pruébalo hoy' de 2 a 6 acciones", ", ".join(sin_prueba)) if sin_prueba \
        else inf.ok("C24", "cada capítulo con un 'Pruébalo hoy' de 2 a 6 acciones")

    estructura = []
    for i, c in enumerate(caps, 1):
        for j, bl in enumerate(c.get("bloques", []), 1):
            if bl.get("tipo") not in TIPOS_BLOQUE:
                estructura.append(f"cap{i}.b{j}: tipo '{bl.get('tipo')}' no existe")
    inf.falla("C19", "bloques de tipos que el motor conoce", "; ".join(estructura)) if estructura else \
        inf.ok("C19", "bloques de tipos que el motor conoce")


# ---------------------------------------------------------------- pdf
def revisar_pdf(e, pdf, inf):
    fmt = (e.get("meta") or {}).get("formato", "movil")
    F = FORMATOS.get(fmt, FORMATOS["movil"])
    try:
        import pdfplumber
    except ImportError:
        inf.nd("P*", "revisión del PDF", "falta pdfplumber: usa ~/.golden/pdfenv/bin/python")
        return
    peso = os.path.getsize(pdf)
    with pdfplumber.open(pdf) as d:
        pags = d.pages
        n = len(pags)
        w_mm, h_mm = pags[0].width * PT_MM, pags[0].height * PT_MM
        if abs(w_mm - F["w"]) > 1 or abs(h_mm - F["h"]) > 1:
            inf.falla("P1", f"página de {F['w']}x{F['h']} mm ({fmt})", f"mide {w_mm:.1f}x{h_mm:.1f} mm")
        else:
            inf.ok("P1", f"página de {F['w']}x{F['h']} mm ({fmt})")
        if n < 10:
            inf.falla("P2", "entre 10 y 48 páginas", f"{n}")
        elif n > 48:
            inf.aviso("P2", "entre 10 y 48 páginas", f"{n}: largo para leer en el celular")
        else:
            inf.ok("P2", "entre 10 y 48 páginas", f"{n}")
        mb = peso / 1e6
        if mb > 15:
            inf.falla("P3", "peso de 5 MB o menos", f"{mb:.1f} MB")
        elif mb > 5:
            inf.aviso("P3", "peso de 5 MB o menos", f"{mb:.1f} MB: pesado para datos móviles")
        else:
            inf.ok("P3", "peso de 5 MB o menos", f"{mb:.2f} MB")

        # Legibilidad: el tamaño de letra más frecuente es el cuerpo.
        tallas = {}
        texto_total = []
        vacias = []
        for i, p in enumerate(pags):
            chars = p.chars
            for c in chars:
                if c["text"].strip():
                    k = round(c["size"], 1)
                    tallas[k] = tallas.get(k, 0) + 1
            texto_total.append(p.extract_text() or "")
            util = [c for c in chars if c["text"].strip() and c["bottom"] < p.height - F["m"][2] / PT_MM + 2]
            if i not in (0, n - 1) and util:
                alto = max(c["bottom"] for c in util) - F["m"][0] / PT_MM
                area = p.height - (F["m"][0] + F["m"][2]) / PT_MM
                if 0 < alto / area < 0.35 and len(util) < 260:
                    vacias.append(str(i + 1))
        cuerpo = max(tallas, key=tallas.get) if tallas else 0
        px = cuerpo * PT_MM / F["w"] * F["viewport_px"]
        px_cel = cuerpo * PT_MM / F["w"] * 390
        # El libro se lee en el celular: A5 se mide en su pantalla (768) para aprobar, pero si a
        # 390 px no llega a 16 se avisa (medido: A5 da 10 px en el celular).
        if px < 16:
            inf.falla("P4", f"cuerpo legible a {F['viewport_px']} px de ancho (16 px o más)",
                      f"cuerpo {cuerpo} pt = {px:.1f} px")
        elif px_cel < 16:
            inf.aviso("P4", "cuerpo legible en el celular (16 px a 390)",
                      f"formato {fmt}: {px_cel:.1f} px en un celular; usa movil si se manda por WhatsApp")
        else:
            inf.ok("P4", "cuerpo legible en el celular (16 px a 390)", f"cuerpo {cuerpo} pt = {px_cel:.1f} px")
        inf.aviso("P5", "sin páginas casi vacías", "páginas " + ", ".join(vacias) +
                  ": ajusta el texto de esa sección") if vacias else inf.ok("P5", "sin páginas casi vacías")

        # Portada: nombre de la marca, título y logo.
        p1 = norm(texto_total[0]).replace("\n", " ")
        marca = norm((e.get("marca") or {}).get("nombre", ""))
        tit = norm((e.get("meta") or {}).get("titulo", ""))
        faltan = []
        if marca and re.sub(r"\s+", "", marca) not in re.sub(r"\s+", "", p1):
            faltan.append("nombre de la empresa")
        if tit and re.sub(r"\s+", "", tit) not in re.sub(r"\s+", "", p1):
            faltan.append("título")
        if (e.get("marca") or {}).get("logo") and not pags[0].images:
            faltan.append("logo (declarado pero no aparece)")
        if faltan:
            inf.falla("P6", "portada con título, empresa y logo", ", ".join(faltan))
        elif not (e.get("marca") or {}).get("logo"):
            inf.aviso("P6", "portada con título, empresa y logo",
                      "sin logo: la portada lleva el nombre en tipografía. Pídele el logo a la marca")
        else:
            inf.ok("P6", "portada con título, empresa y logo")

        # P13 · el logo tiene que leerse en la miniatura: su lado mayor, 24 mm o más
        # (unos 130 px a 600 px de ancho). Medido: con 17 mm de alto "ENTERPRISE" no se leía.
        desc13 = "logo legible en la portada (lado mayor 24 mm o más, lado menor 8 mm o más)"
        pg0 = pags[0]
        logos = [x for x in pg0.images if x["top"] < pg0.height * 0.4 and (x["x1"] - x["x0"]) < pg0.width * 0.8]
        if not (e.get("marca") or {}).get("logo"):
            inf.aviso("P13", desc13, "sin logo")
        elif not logos:
            inf.falla("P13", desc13, "no hay imagen de logo en la franja superior de la portada")
        else:
            im = max(logos, key=lambda x: (x["x1"] - x["x0"]) * (x["bottom"] - x["top"]))
            lados = sorted([(im["x1"] - im["x0"]) * PT_MM, (im["bottom"] - im["top"]) * PT_MM])
            if lados[1] >= 24 and lados[0] >= 8:
                inf.ok("P13", desc13, f"{lados[1]:.0f} x {lados[0]:.0f} mm")
            else:
                inf.falla("P13", desc13, f"{lados[1]:.0f} x {lados[0]:.0f} mm")
        # Miniatura: WhatsApp muestra la página 1 a unos 600 px de ancho. Se miden el
        # título (lo más grande) y el nombre de la empresa (el pie de portada): la primera
        # versión solo medía el título y el nombre no se leía en la miniatura.
        tallas_p1 = [c["size"] for c in pags[0].chars if c["text"].strip()]
        tpx = max(tallas_p1, default=0) * PT_MM / F["w"] * 600
        letras = set(re.sub(r"\s+", "", (e.get("marca") or {}).get("nombre", "")).casefold())
        pie = [c["size"] for c in pags[0].chars if c["text"].strip() and c["text"].casefold() in letras
               and c["top"] > pags[0].height * 0.8]
        mpx = (min(pie) if pie else 0) * PT_MM / F["w"] * 600
        desc7 = "portada legible a 600 px: título 24 px o más, empresa 12 px o más"
        if tpx < 24 or mpx < 12:
            inf.falla("P7", desc7, f"título {tpx:.0f} px · empresa {mpx:.0f} px")
        else:
            inf.ok("P7", desc7, f"título {tpx:.0f} px · empresa {mpx:.0f} px")

        # Acentos en el render: las palabras con tilde del JSON deben salir iguales en el PDF.
        # Se compara en minúscula (los rótulos salen en VERSALES por CSS) y se unen las
        # palabras partidas por el guion de fin de línea que pone la separación silábica.
        plano = re.sub(r"[-\u2010\u00ad]\s*\n", "", "\n".join(texto_total))
        plano = re.sub(r"\s+", " ", plano).casefold()
        con_tilde = set()
        for _, campo, t, _ in textos(e):
            if campo == "fuente":
                continue
            for w in re.findall(r"\w+", t):
                if len(w) >= 4 and w != sin_tildes(w):
                    con_tilde.add(w)
        if con_tilde:
            perdidas = [w for w in con_tilde if w.casefold() not in plano]
            frac = 1 - len(perdidas) / len(con_tilde)
            if frac < 0.9:
                inf.falla("P8", "acentos intactos en el render", f"{frac:.0%} de {len(con_tilde)}; ej.: "
                          + ", ".join(sorted(perdidas)[:6]))
            else:
                inf.ok("P8", "acentos intactos en el render", f"{frac:.0%} de {len(con_tilde)} palabras con tilde")
        else:
            inf.nd("P8", "acentos intactos en el render", "el texto no trae palabras con tilde")

        cta = ((e.get("cierre") or {}).get("cta") or {}).get("url")
        if not cta:
            inf.aviso("P9", "el botón de cierre es un enlace que se puede tocar", "el ebook no trae botón")
        if cta:
            links = [a.get("uri", "").rstrip("/") for p in pags for a in (p.hyperlinks or []) if a.get("uri")]
            inf.ok("P9", "el botón de cierre es un enlace que se puede tocar") if cta.rstrip("/") in links else \
                inf.falla("P9", "el botón de cierre es un enlace que se puede tocar", f"{cta} no está enlazado")

    try:
        from pypdf import PdfReader
        r = PdfReader(pdf)
        tipos, sin_incrustar = set(), set()
        for p in r.pages:
            fonts = (p.get("/Resources") or {}).get("/Font") or {}
            for f in fonts.values():
                f = f.get_object()
                tipos.add(str(f.get("/Subtype")))
                desc = f.get("/FontDescriptor")
                if desc is None and f.get("/DescendantFonts"):
                    desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
                if desc is not None:
                    desc = desc.get_object()
                    if not any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                        sin_incrustar.add(str(desc.get("/FontName")))
        if "/Type3" in tipos or sin_incrustar:
            inf.falla("P10", "fuentes incrustadas y sin Type 3",
                      f"Type3: {'/Type3' in tipos} · sin incrustar: {', '.join(sorted(sin_incrustar))}")
        else:
            inf.ok("P10", "fuentes incrustadas y sin Type 3", ", ".join(sorted(tipos)))
        # P12 · el PDF lleva el sello del JSON con que se construyó. Sin esto, un PDF viejo
        # con claims pasaba verificado contra un JSON limpio (segunda auditoría).
        import hashlib
        sello = str((r.metadata or {}).get("/EbookJSONSHA256", ""))
        actual = hashlib.sha256(open(JSON_RUTA, "rb").read()).hexdigest() if JSON_RUTA else ""
        if not sello:
            inf.falla("P12", "el PDF se construyó con este mismo ebook.json", "el PDF no trae sello: reconstrúyelo")
        elif sello != actual:
            inf.falla("P12", "el PDF se construyó con este mismo ebook.json",
                      "el JSON cambió después de construir el PDF: reconstruye y vuelve a verificar")
        else:
            inf.ok("P12", "el PDF se construyó con este mismo ebook.json")
        # P14 · el sello se puede poner a mano: se busca además en el TEXTO del PDF toda proclama
        # que no venga, palabra por palabra, del JSON (tercera verificación: PDF sellado a mano).
        solo = lambda t: re.sub(r"[^a-z0-9]", "", norm(t))  # noqa: E731
        blob_json = solo(" ".join(t for _, _, t, _ in textos(e)))
        texto_pdf = norm(re.sub(r"[-\u2010\u00ad]\s*\n", "", "\n".join((pg.extract_text() or "") for pg in r.pages)))
        ajenas = []
        for pat in TERAPEUTICOS + [re.escape(norm(x)) for x in (e.get("producto") or {}).get("claims_prohibidos", []) if x]:
            for m in re.finditer(pat, texto_pdf):
                ventana = solo(texto_pdf[max(0, m.start() - 25): m.end() + 25])
                if ventana and ventana[5:-5] not in blob_json:
                    ajenas.append(texto_pdf[max(0, m.start() - 20): m.end() + 10].replace("\n", " "))
        inf.falla("P14", "el texto del PDF no trae proclamas ajenas al JSON", "; ".join(ajenas[:4])) if ajenas else \
            inf.ok("P14", "el texto del PDF no trae proclamas ajenas al JSON")
        # Marcadores: uno por capítulo y con el título EXACTO. Chromium los generaba
        # comiéndose el espacio del salto de línea ("tecontó"); por eso se comparan.
        titulos = [x.title for x in r.outline if not isinstance(x, list)]
        esperados = [c["titulo"] for c in e.get("capitulos", [])]
        faltan = [t for t in esperados if t not in titulos]
        if not titulos:
            inf.aviso("P11", "marcadores de capítulo con su título exacto", "el PDF no trae marcadores")
        elif faltan:
            inf.falla("P11", "marcadores de capítulo con su título exacto", "no coinciden: " + "; ".join(faltan[:4]))
        else:
            inf.ok("P11", "marcadores de capítulo con su título exacto", f"{len(esperados)} de {len(esperados)}")
    except ImportError:
        inf.nd("P10", "fuentes incrustadas y sin Type 3", "falta pypdf")
        inf.nd("P11", "marcadores de capítulo con su título exacto", "falta pypdf")
        inf.nd("P12", "el PDF se construyó con este mismo ebook.json", "falta pypdf")
        inf.nd("P14", "el texto del PDF no trae proclamas ajenas al JSON", "falta pypdf")


def revisar_online(e, inf):
    import urllib.request
    caidas, inexistentes, leidas_navegador = [], [], []
    for f in e.get("fuentes", []):
        url = f.get("url", "")
        # Un DOI se confirma en Crossref, que es el registro oficial: las revistas bloquean
        # a los robots con 403 y eso no dice nada de si el artículo existe (medido: 3 de 10).
        if url.startswith("https://doi.org/"):
            url = "https://api.crossref.org/works/" + url[len("https://doi.org/"):]
        try:
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status >= 400:
                    caidas.append(f"{f.get('id')}: HTTP {resp.status}")
        except Exception as ex:  # noqa: BLE001
            codigo = getattr(ex, "code", "")
            # Un 403 a robots no dice nada si el navegador sí la leyó: guardar_fuentes.py dejó su
            # texto en disco, con el método en la primera línea. Esa es la prueba de que existe.
            guardada = os.path.join(os.path.dirname(os.path.abspath(JSON_RUTA or ".")), "fuentes-texto",
                                    f"{f.get('id')}.txt")
            if codigo == 403 and os.path.exists(guardada) and "navegador" in open(guardada, encoding="utf-8").readline():
                leidas_navegador.append(str(f.get("id")))
                continue
            (inexistentes if codigo in (404, 410) else caidas).append(
                f"{f.get('id')}: {type(ex).__name__} {codigo}".strip())
    n = len(e.get("fuentes", []))
    if inexistentes:
        # Un 404 del registro (o del sitio) dice que la fuente NO EXISTE, no que bloquee robots.
        inf.falla("W1", "las fuentes existen y responden", "no existen: " + "; ".join(inexistentes))
    elif caidas:
        inf.aviso("W1", "las fuentes existen y responden", "; ".join(caidas) +
                  " (bloqueo de robots: ábrelas con WebFetch antes de concluir)")
    else:
        nota = f" ({', '.join(leidas_navegador)} bloquean robots y se leyeron con navegador)" if leidas_navegador else ""
        inf.ok("W1", "las fuentes existen y responden", f"{n} de {n}{nota}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ebook_json")
    ap.add_argument("pdf")
    ap.add_argument("--json")
    ap.add_argument("--online", action="store_true")
    a = ap.parse_args()
    for ruta in (a.ebook_json, a.pdf):
        if not os.path.exists(ruta):
            print(f"no existe {ruta}", file=sys.stderr)
            sys.exit(2)
    try:
        with open(a.ebook_json, encoding="utf-8") as f:
            e = json.load(f)
    except json.JSONDecodeError as ex:
        print(f"ebook.json inválido: {ex}", file=sys.stderr)
        sys.exit(2)

    global JSON_RUTA
    JSON_RUTA = a.ebook_json
    inf = Informe()
    revisar_contenido(e, inf)
    revisar_hoja(e, inf)
    revisar_pdf(e, a.pdf, inf)
    if a.online:
        revisar_online(e, inf)

    for fila in inf.filas:
        det = f" · {fila['detalle']}" if fila["detalle"] else ""
        print(f"{fila['estado']:<6} {fila['id']:<4} {fila['desc']}{det}")
    cuenta = {k: sum(1 for x in inf.filas if x["estado"] == k) for k in ("OK", "AVISO", "FALLA", "N/D")}
    total = len(inf.filas)
    # Un N/D no es falla del ebook, pero tampoco es aprobación: sin medir no se entrega.
    veredicto = "NO ENTREGAR" if cuenta["FALLA"] else ("NO VERIFICADO" if cuenta["N/D"] else "ENTREGABLE")
    print(f"\n{total} comprobaciones · {cuenta['OK']} OK · {cuenta['AVISO']} avisos · "
          f"{cuenta['FALLA']} fallas · {cuenta['N/D']} N/D → {veredicto}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"veredicto": veredicto, "cuenta": cuenta, "filas": inf.filas}, f,
                      ensure_ascii=False, indent=2)
    sys.exit(1 if cuenta["FALLA"] else (3 if cuenta["N/D"] else 0))


if __name__ == "__main__":
    main()
