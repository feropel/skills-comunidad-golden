#!/usr/bin/env python3
"""Validador de la matriz de golden-anuncios-niveles-de-conciencia (v2).

Uso:
  python3 validar_matriz.py RUTA/matriz.json   -> 0 pasa · 1 falla alguna casilla · 2 estructura inválida o no se puede leer
  python3 validar_matriz.py --autoprueba       -> dos matrices sanas (deben pasar) y un banco de sabotajes (deben fallar)

Solo usa la librería estándar de Python 3. El esquema está en references/ficha-de-estatico.md,
sección "El archivo matriz.json"; las casillas, en la sección siguiente.

Por qué v2: la v1 dejaba pasar una matriz vacía y 31 de 33 matrices malas construidas fuera de su
banco (golden-verificador, 02-oct-2026). Las tres causas de clase: listas de palabras exactas sin
normalizar, casillas que miraban un solo campo y guardas que volvían verde lo vacío.
"""
import copy
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata

# ---------- vocabularios cerrados ----------
NIVELES = {"unaware", "problem_aware", "solution_aware", "product_aware", "most_aware"}
NIVELES_BAJOS = {"unaware", "problem_aware"}
ETAPAS = ("TOFU", "MOFU", "BOFU")
PAGOS = {"contraentrega", "anticipado", "ambos"}
VERTICALES = {"belleza", "salud", "esoterico", "hogar", "moda", "tecnologia", "mascotas", "otro"}
VERTICALES_PERSONA = {"belleza", "salud"}
DESTINOS = {"pauta", "whatsapp", "organico", "landing", "ficha"}
DESTINOS_CON_PRECIO = {"pauta", "whatsapp"}
RELACIONES = {"4:5", "1:1"}
CAMPOS_TEXTO = ("titular", "apoyo", "callouts", "sello", "cta")
CAMPOS_IMAGEN = ("titular", "apoyo", "callouts", "sello")
PLACEHOLDERS = {"", "n/a", "na", "-", "x", "pendiente", "por confirmar", "tbd", "none", "null", "?"}


def norm(s):
    """minúsculas, sin tildes, espacios simples: para COMPARAR, nunca para corregir texto."""
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.lower()).strip()


def tiene_palabra(texto, frase):
    """frase completa con frontera de palabra, sobre texto normalizado."""
    return re.search(r"(?<![a-z0-9])" + re.escape(norm(frase)) + r"(?![a-z0-9])", norm(texto)) is not None


# ---------- listas (normalizadas al comparar) ----------
CTA_COMPRA = ["pidelo", "pide ya", "pide el tuyo", "pidela", "compra ya", "compralo", "comprala", "compra ahora",
              "comprar", "ordenalo", "ordenala", "ordena ya", "ordena el tuyo", "llevalo", "llevatelo", "llevala",
              "quiero mi", "quiero el mio", "shop now", "buy now", "order now", "agregalo al carrito",
              "aprovecha la oferta", "ultimas unidades"]
SELLO = {
    "contraentrega": ["contra entrega", "contraentrega", "pagas al recibir", "paga al recibir", "pago al recibir",
                      "pagas cuando lo recibes", "pagas cuando llegue", "pagas en casa", "paga en casa"],
    "anticipado": ["pago seguro", "pago en linea", "paga en linea", "pago con tarjeta", "paga con tarjeta", "pse",
                   "nequi", "daviplata", "transferencia"],
}
SELLO["ambos"] = SELLO["contraentrega"] + SELLO["anticipado"]
ANTES_DESPUES = [r"antes\s*(y|/|-|&)\s*despues", r"before\s*(and|&|/|-)\s*after", r"\bcon\b[^/|]{0,40}/\s*sin\b",
                 r"\bcon\s*/\s*sin\b"]
INFANTIL = [r"\bconfet+[ia]s?\b", r"\bburbujas?\b", r"\bbubbles?\b", r"\bglobos?\b", r"\bballoons?\b",
            r"\bstickers?\b", r"\bpegatinas?\b", r"\bglitter\b", r"\bescarcha\b"]
NEGATIVO_DE_CLAIM = [r"\bno\s+(health\s+|money\s+|luck\s+)?claims?\b", r"\bwithout\s+claims?\b",
                     r"\bno\s+promet(e|er|as)\b", r"\bno\s+promises?\b", r"\bno\s+(diga|digas|decir)\b",
                     r"\bprohibid[oa]s?\b.{0,60}\b(diga|digan|decir|escrib\w*|texto|palabras?|claims?|frases?)\b",
                     r"\b(evita|evitar|nunca)\s+(decir|escribir|poner|usar|mencionar)\b",
                     r"\bdo\s+not\s+(write|say|use|mention)\b", r"\bavoid\b.{0,40}\b(claims?|words?|wording|text)\b"]
VEREDICTO = ["quedo perfecto", "quedo perfecta", "todo bien", "esta listo", "esta lista", "quedo listo",
             "quedo lista", "listo para lanzar", "lista para lanzar", "deberia funcionar"]
UNIDADES = r"(anos?|dias?|horas?|minutos?|mah|ml|gr?|kg|mg|cm|mm|m|l|w|v|capas?|%|x|veces|clientes?|personas?|unidades?)"
MONEDA_ANTES = r"(\$|cop|gtq|usd|mxn|pen|clp|us\$|s/)"
MONEDA_DESPUES = r"(cop|gtq|usd|mxn|pen|clp|pesos?|quetzales?|soles?|dolares?|mil)"
RX_TEL = re.compile(r"(?<!\d)(\+?\d{2,3}[\s.-]?)?3\d{2}[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)|(?<!\d)\d{4}[\s.-]\d{4}(?!\d)")
RX_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
RX_CUENTA = re.compile(r"\bact_\d{6,}\b")


def hay_precio(texto, pais=""):
    """True si el texto trae un precio escrito como número (no como variable {PRECIO_X})."""
    t = norm(RX_TEL.sub(" ", str(texto)))
    t = re.sub(r"\{[a-z_0-9]+\}", " ", t)
    t = re.sub(r"coenzima\s?q\s?10", " ", t)  # la Q de la coenzima no es quetzal
    if re.search(MONEDA_ANTES + r"\s?\d", t):
        return True
    if pais.upper() == "GT" and re.search(r"(?<![a-z0-9])q\s?\d{2,}", t):
        return True
    for mm in re.finditer(r"(?<![\w.,])(\d{1,3}(?:[.,]\d{3})+|\d{3,7})(?![\w])", t):
        despues = t[mm.end():mm.end() + 14]
        if re.match(r"\s?" + UNIDADES + r"(?![a-z])", despues):
            continue
        if re.match(r"\s?" + MONEDA_DESPUES + r"(?![a-z])", despues):
            return True
        antes = t[max(0, mm.start() - 25):mm.start()]
        if re.search(r"(precio|por solo|solo|desde|vale|cuesta|a solo|por|x2|2x|oferta)\s*$", antes) and \
                (len(mm.group(1).replace(".", "").replace(",", "")) >= 4):
            return True
        if re.search(r"[.,]\d{3}", mm.group(1)) and not re.match(r"\s?" + UNIDADES, despues):
            return True
    if re.search(r"(?<![a-z0-9])\d{1,3}\s?mil(?![a-z])", t) and not re.search(r"\d{1,3}\s?mil\s" + UNIDADES, t):
        return True
    return False


def es_placeholder(v):
    return norm(v) in PLACEHOLDERS or norm(v).startswith("pendiente")


def resolver(ruta, base):
    if not ruta or es_placeholder(ruta):
        return None
    cands = [ruta, os.path.join(os.getcwd(), ruta)]
    d = base
    for _ in range(8):
        cands.append(os.path.join(d, ruta))
        d = os.path.dirname(d)
    for c in cands:
        if os.path.exists(os.path.expanduser(c)):
            return c
    return None


# ---------- estructura (exit 2) ----------
def estructura(m):
    e = []
    if not isinstance(m, dict):
        return ["la raíz no es un objeto JSON"]
    for k in ("angulos", "piezas"):
        if not isinstance(m.get(k), list):
            e.append(f"'{k}' falta o no es una lista")
    for k in ("producto", "empresa", "canal", "pais", "pago", "vertical", "estudio"):
        if not isinstance(m.get(k), str):
            e.append(f"'{k}' falta o no es texto")
    if e:
        return e
    for i, a in enumerate(m["angulos"]):
        if not isinstance(a, dict) or not isinstance(a.get("id"), str):
            e.append(f"ángulo #{i + 1} sin 'id' de texto")
            continue
        if not isinstance(a.get("disruptivo"), bool):
            e.append(f"ángulo {a['id']}: 'disruptivo' debe ser true o false, no texto")
    for i, p in enumerate(m["piezas"]):
        if not isinstance(p, dict) or not isinstance(p.get("id"), str):
            e.append(f"pieza #{i + 1} sin 'id' de texto")
            continue
        for b in ("generar", "persona", "precio_en_imagen"):
            if not isinstance(p.get(b), bool):
                e.append(f"pieza {p['id']}: '{b}' debe ser true o false, no texto")
    if "plan" in m and not isinstance(m.get("plan"), dict):
        e.append("'plan' no es un objeto")
    return e


# ---------- casillas (exit 1) ----------
def validar(m, base="."):
    fallos = []

    def f(c, d):
        fallos.append((c, d))

    angulos = {a["id"]: a for a in m["angulos"]}
    piezas = m["piezas"]
    pais = str(m.get("pais", ""))
    pago = norm(m.get("pago", ""))
    vertical = norm(m.get("vertical", ""))
    nombres = [n for n in [m.get("producto", "")] + list(
        m.get("nombre_corto", []) if isinstance(m.get("nombre_corto"), list) else [m.get("nombre_corto", "")])
               if norm(n)]
    cuenta = m.get("cuenta", {}) if isinstance(m.get("cuenta"), dict) else {}
    plan = m.get("plan", {}) if isinstance(m.get("plan"), dict) else {}

    # 01 vocabularios cerrados de la matriz
    if pago not in PAGOS:
        f("01 vocabulario", f"pago '{m.get('pago')}' fuera de {sorted(PAGOS)}")
    if vertical not in VERTICALES:
        f("01 vocabulario", f"vertical '{m.get('vertical')}' fuera de {sorted(VERTICALES)}")
    for a in angulos.values():
        if a.get("nivel") not in NIVELES:
            f("01 vocabulario", f"ángulo {a['id']} con nivel '{a.get('nivel')}' fuera de los 5 valores")
    for p in piezas:
        if p.get("etapa") not in ETAPAS:
            f("01 vocabulario", f"pieza {p['id']} con etapa '{p.get('etapa')}'")
        if norm(p.get("destino", "")) not in DESTINOS:
            f("01 vocabulario", f"pieza {p['id']} con destino '{p.get('destino')}' fuera de {sorted(DESTINOS)}")
        if str(p.get("relacion", "")).strip() not in RELACIONES:
            f("01 vocabulario", f"pieza {p['id']} con relación '{p.get('relacion')}' (estático = 4:5 o 1:1)")
    # 02 mínimos
    if not 2 <= len(angulos) <= 3:
        f("02 mínimos", f"{len(angulos)} ángulos en la tanda (deben ser de 2 a 3)")
    # 03 etapas por ángulo
    for aid in angulos:
        etapas = [p.get("etapa") for p in piezas if p.get("angulo") == aid]
        for e in ETAPAS:
            if e not in etapas:
                f("03 etapas", f"ángulo {aid} sin pieza {e}")
    # 04 mezcla de niveles
    if not any(a.get("nivel") in NIVELES_BAJOS for a in angulos.values()):
        f("04 mezcla", "ningún ángulo de nivel 1 o 2 (unaware o problem_aware)")
    if not any(a.get("disruptivo") is True for a in angulos.values()):
        f("04 mezcla", "ningún ángulo disruptivo")
    # 05 evidencia
    for a in angulos.values():
        cita = str(a.get("cita", ""))
        if es_placeholder(cita) or len(cita.strip()) < 15:
            f("05 evidencia", f"ángulo {a['id']} sin cita del estudio que lo sostenga")
        if not norm(a.get("nombre", "")):
            f("05 evidencia", f"ángulo {a['id']} sin nombre")
    # 06 estudio
    if not resolver(str(m.get("estudio", "")), base):
        f("06 estudio", f"el estudio '{m.get('estudio')}' no existe en disco")
    # 07 empresa y canal
    for k in ("empresa", "canal"):
        if es_placeholder(m.get(k, "")):
            f("07 empresa y canal", f"falta '{k}'")

    titulares = {}
    for p in piezas:
        pid, et = p["id"], p.get("etapa")
        en_imagen = " ".join(str(p.get(k, "")) for k in CAMPOS_IMAGEN)
        todo = " ".join(str(p.get(k, "")) for k in CAMPOS_TEXTO)
        prompt = str(p.get("prompt", ""))
        # 20 ángulo existente
        if p.get("angulo") not in angulos:
            f("20 ángulo", f"pieza {pid} apunta a un ángulo que no existe")
        # 08 TOFU sin precio
        if et == "TOFU" and (p.get("precio_en_imagen") or "{precio" in norm(todo + prompt)
                             or hay_precio(todo, pais) or hay_precio(prompt, pais)):
            f("08 tofu sin precio", f"pieza {pid} TOFU con precio")
        # 09 TOFU no vende
        if et == "TOFU":
            for n in nombres:
                if tiene_palabra(en_imagen, n):
                    f("09 tofu no vende", f"pieza {pid} TOFU nombra el producto ('{n}') en la imagen")
            for c in CTA_COMPRA:
                if tiene_palabra(todo, c):
                    f("09 tofu no vende", f"pieza {pid} TOFU con llamado de compra ('{c}')")
        # 10 BOFU con sello de pago dentro de la imagen
        if et == "BOFU" and not any(tiene_palabra(en_imagen, s) for s in SELLO.get(pago, [])):
            f("10 bofu confianza", f"pieza {pid} BOFU sin sello de pago ({pago}) dentro de la imagen")
        # 11 precio como variable
        if hay_precio(todo, pais) or hay_precio(prompt, pais):
            f("11 precio vivo", f"pieza {pid} con un precio escrito como número; va como variable {{PRECIO_X}}")
        # 12 producto real
        fr = str(p.get("foto_real", ""))
        if p.get("generar") and (es_placeholder(fr) or not re.search(r"[/\\]|\.(jpe?g|png|webp|heic)$|^https?://", fr, re.I)):
            f("12 producto real", f"pieza {pid} marcada para generar sin ruta o URL de foto real ('{fr}')")
        # 13 texto literal dentro del prompt
        tit = str(p.get("titular", "")).strip()
        if not tit:
            f("13 texto literal", f"pieza {pid} sin titular")
        elif p.get("generar") and norm(tit) not in norm(prompt):
            f("13 texto literal", f"pieza {pid}: el prompt no lleva el titular literal '{tit}'")
        # 14 prompt sin antes/después, sin infantil, sin negativos de claim
        for rx in ANTES_DESPUES:
            if re.search(rx, norm(prompt)) or re.search(rx, norm(todo)):
                f("14 prompt", f"pieza {pid} con antes/después o con/sin")
                break
        for rx in INFANTIL:
            if re.search(rx, norm(prompt)):
                f("14 prompt", f"pieza {pid} con diseño infantil en el prompt")
                break
        for rx in NEGATIVO_DE_CLAIM:
            if re.search(rx, norm(prompt)):
                f("14 prompt", f"pieza {pid} lista claims en negativo (prohibir una frase hace que el generador la escriba)")
                break
        # 15 signos de apertura en cualquier texto
        if re.search("[\u00bf\u00a1]", todo + prompt):
            f("15 signos", f"pieza {pid} con signos de apertura")
        # 16 destino con precio
        if (p.get("precio_en_imagen") or "{precio" in norm(todo)) and norm(p.get("destino", "")) not in DESTINOS_CON_PRECIO:
            f("16 destino", f"pieza {pid} con precio y destino '{p.get('destino')}' (solo pauta o whatsapp)")
        # 17 reseña real
        if re.search(r"\{resen[a]_real\}", norm(todo + prompt)) and p.get("generar"):
            f("17 reseña", f"pieza {pid} marcada para generar con {{RESEÑA_REAL}} sin reemplazar")
        if re.search("[★⭐]|\\b5 estrellas\\b", todo) and es_placeholder(p.get("resena_fuente", "")):
            f("17 reseña", f"pieza {pid} con estrellas o testimonio sin 'resena_fuente'")
        # 18 datos privados
        for rx in (RX_TEL, RX_EMAIL, RX_CUENTA):
            if rx.search(todo + " " + prompt):
                f("18 privados", f"pieza {pid} con teléfono, correo o cuenta en el texto o el prompt")
                break
        # 19 públicos
        if cuenta.get("publicos") is False and et in ("MOFU", "BOFU") and "requiere publicos" not in norm(p.get("estado", "")):
            f("19 públicos", f"pieza {pid} {et} sin 'estado': 'PENDIENTE: requiere públicos' (la cuenta no los tiene)")
        if norm(tit):
            titulares.setdefault(norm(tit), []).append(pid)
    # 21 titular único
    for t, ids in titulares.items():
        if len(ids) > 1:
            f("21 titular único", f"titular repetido en {', '.join(ids)}")
    # 22 diversidad: dos ángulos no repiten formato en la misma etapa
    for e in ETAPAS:
        vistos = {}
        for p in piezas:
            if p.get("etapa") == e:
                fm = norm(p.get("formato", ""))
                if fm in vistos and vistos[fm] != p.get("angulo"):
                    f("22 diversidad", f"{e}: los ángulos {vistos[fm]} y {p.get('angulo')} usan el mismo formato '{fm}'")
                vistos.setdefault(fm, p.get("angulo"))
    # 23 plan: existe, ≤3 por conjunto, cubre todas las piezas
    conjuntos = plan.get("conjuntos")
    if not isinstance(conjuntos, list) or not conjuntos:
        f("23 plan", "sin plan de testeo con conjuntos")
    else:
        en_plan = set()
        ids = {p["id"] for p in piezas}
        for c in conjuntos:
            ps = c.get("piezas", []) if isinstance(c, dict) else []
            if len(ps) > 3:
                f("23 plan", f"conjunto '{c.get('nombre')}' con {len(ps)} piezas (máximo 3)")
            for x in ps:
                if x not in ids:
                    f("23 plan", f"conjunto '{c.get('nombre')}' nombra la pieza {x}, que no existe")
            en_plan.update(ps)
        faltan = ids - en_plan
        if faltan:
            f("23 plan", f"piezas fuera del plan: {', '.join(sorted(faltan))}")
    # 24 belleza y salud: persona y 18+
    if vertical in VERTICALES_PERSONA:
        if not any(p.get("persona") is True for p in piezas):
            f("24 belleza y salud", "ninguna pieza con persona usando el producto")
        try:
            edad = int(plan.get("edad_minima", 0))
        except (TypeError, ValueError):
            edad = 0
        if edad < 18:
            f("24 belleza y salud", "el plan no fija 'edad_minima' de 18 o más")
    # 25 frases de veredicto en la entrega o en cualquier texto
    ent = " ".join([str(m.get("entrega", ""))] + [" ".join(str(p.get(k, "")) for k in CAMPOS_TEXTO) for p in piezas])
    for v in VEREDICTO:
        if tiene_palabra(ent, v):
            f("25 veredicto", f"aparece '{v}'")
    return fallos


# ---------- autoprueba ----------
def _pieza(i, a, et, fmt, tit, sello="", cta="Ver más", precio=False, persona=False, apoyo="Hecho para tu rutina"):
    return {"id": i, "angulo": a, "etapa": et, "formato": fmt, "titular": tit, "apoyo": apoyo, "callouts": "",
            "sello": sello, "cta": cta, "precio_en_imagen": precio, "destino": "pauta", "relacion": "4:5",
            "foto_real": "fotos/producto.jpg", "generar": True, "persona": persona,
            "prompt": f'Ultra-realistic photo, product EXACTLY as Image 1. Headline: "{tit}". Clean composition.'}


def sana_belleza():
    return {
        "producto": "Sérum Ejemplo", "nombre_corto": ["Ejemplo"], "empresa": "Empresa A", "canal": "Tienda A",
        "pais": "CO", "pago": "contraentrega", "vertical": "belleza", "estudio": "00-ESTUDIO.md",
        "cuenta": {"publicos": True},
        "angulos": [
            {"id": "A1", "nombre": "El espejo de las 7", "nivel": "unaware", "patron": "disruptivo",
             "origen": "derivado", "cita": "«me miro y no me reconozco» (reseña, 120 likes)", "disruptivo": True},
            {"id": "A2", "nombre": "Piel que se nota", "nivel": "solution_aware", "patron": "infografía",
             "origen": "estudio", "cita": "«quiero algo que se note sin maquillaje» (comentario, 45 likes)",
             "disruptivo": False},
        ],
        "piezas": [
            _pieza("P1", "A1", "TOFU", "nota de iPhone", "Lo que nadie te dice a los 40", persona=True),
            _pieza("P2", "A1", "MOFU", "callouts", "Tres pasos y una rutina", cta="Ver opiniones"),
            _pieza("P3", "A1", "BOFU", "oferta apilada", "El par para tu rutina",
                   "{PRECIO_2} · Pago contra entrega · Envío a todo Colombia", "Pídelo contra entrega", precio=True),
            _pieza("P4", "A2", "TOFU", "metáfora", "La luz de las 7 de la mañana"),
            _pieza("P5", "A2", "MOFU", "comparativa", "Rutina larga o un paso", cta="Ver opiniones"),
            _pieza("P6", "A2", "BOFU", "garantía", "Tu rutina completa", "Pagas al recibir · Envío a todo Colombia",
                   "Pídelo contra entrega"),
        ],
        "plan": {"edad_minima": 18, "conjuntos": [{"nombre": "TOFU", "piezas": ["P1", "P4"]},
                                                  {"nombre": "MOFU", "piezas": ["P2", "P5"]},
                                                  {"nombre": "BOFU", "piezas": ["P3", "P6"]}]},
        "entrega": "Cobertura: 6 de 6 piezas revisadas; sin generar todavía.",
    }


def sana_hogar_gt():
    """Segunda sana, a propósito incómoda: GT, pago ambos, cifras que NO son precio, CTA 'Ordena tu cocina'."""
    m = {
        "producto": "Organizador Luz", "nombre_corto": ["Ola"], "empresa": "Empresa B", "canal": "Tienda B",
        "pais": "GT", "pago": "ambos", "vertical": "hogar", "estudio": "00-ESTUDIO.md",
        "cuenta": {"publicos": False},
        "angulos": [
            {"id": "A1", "nombre": "La cocina que se esconde", "nivel": "problem_aware", "patron": "problema nombrado",
             "origen": "estudio", "cita": "«no encuentro nada en la alacena» (comentario, 80 likes)", "disruptivo": True},
            {"id": "A2", "nombre": "Diez segundos", "nivel": "product_aware", "patron": "demostración",
             "origen": "estudio", "cita": "«lo armé en diez segundos» (reseña Amazon 5 estrellas)", "disruptivo": False},
            {"id": "A3", "nombre": "Tradición de orden", "nivel": "unaware", "patron": "símbolo",
             "origen": "derivado", "cita": "«mi abuela tenía todo en su lugar» (comentario, 33 likes)", "disruptivo": False},
        ],
        "piezas": [
            _pieza("P1", "A1", "TOFU", "titular audaz", "Un método con 2.000 años de historia", cta="Ordena tu cocina"),
            _pieza("P2", "A1", "MOFU", "infografía", "Batería de 4.000 mAh y luz cálida"),
            _pieza("P3", "A1", "BOFU", "oferta apilada", "Dos niveles en un pedido", "{PRECIO_2} · Pago contra entrega",
                   "Quiero el mío", precio=True),
            _pieza("P4", "A2", "TOFU", "nota de iPhone", "Hola, alacena nueva"),
            _pieza("P5", "A2", "MOFU", "macro de detalle", "Coenzima Q10 no: madera y acero"),
            _pieza("P6", "A2", "BOFU", "garantía", "Garantía de cambio real", "Pago seguro con tarjeta o Pagas al recibir",
                   "Pídelo hoy"),
            _pieza("P7", "A3", "TOFU", "metáfora", "La luz de las 7 en la cocina"),
            _pieza("P8", "A3", "MOFU", "comparativa", "Tres capas de orden"),
            _pieza("P9", "A3", "BOFU", "regalo con significado", "Un regalo para la casa", "Pagas cuando lo recibes",
                   "Pídelo"),
        ],
        "plan": {"conjuntos": [{"nombre": "TOFU", "piezas": ["P1", "P4", "P7"]},
                               {"nombre": "MOFU", "piezas": ["P2", "P5", "P8"]},
                               {"nombre": "BOFU", "piezas": ["P3", "P6", "P9"]}]},
        "entrega": "Cobertura: 9 de 9 piezas revisadas.",
    }
    for p in m["piezas"]:
        if p["etapa"] in ("MOFU", "BOFU"):
            p["estado"] = "PENDIENTE: requiere públicos"
    return m


def sabotajes():
    S = []

    def mut(casilla, base, fn, nota):
        m = copy.deepcopy(base())
        fn(m)
        S.append((casilla, m, nota))
    B, H = sana_belleza, sana_hogar_gt
    P = lambda m, i: m["piezas"][i]
    mut("01 vocabulario", B, lambda m: m["angulos"][0].update(nivel="frio"), "nivel fuera de vocabulario")
    mut("01 vocabulario", B, lambda m: m.update(vertical="Cosmetica"), "vertical fuera de vocabulario")
    mut("01 vocabulario", B, lambda m: m.update(pago="contra entrega"), "pago escrito distinto")
    mut("01 vocabulario", B, lambda m: P(m, 0).update(relacion="9:16"), "relación de video")
    mut("02 mínimos", B, lambda m: (m.update(angulos=m["angulos"][:1]),
                                    m.update(piezas=[p for p in m["piezas"] if p["angulo"] == "A1"]),
                                    m["plan"].update(conjuntos=[{"nombre": "x", "piezas": ["P1", "P2", "P3"]}])), "1 ángulo")
    mut("02 mínimos", H, lambda m: m["angulos"].append(dict(m["angulos"][0], id="A4")), "4 ángulos")
    mut("02 mínimos", B, lambda m: (m.update(angulos=[], piezas=[]), m["plan"].update(conjuntos=[])), "matriz vacía")
    mut("03 etapas", B, lambda m: m.update(piezas=[p for p in m["piezas"] if p["id"] != "P2"]), "falta un MOFU")
    mut("04 mezcla", B, lambda m: [a.update(disruptivo=False) for a in m["angulos"]], "sin disruptivo")
    mut("04 mezcla", B, lambda m: m["angulos"][0].update(nivel="product_aware"), "sin nivel bajo")
    mut("05 evidencia", B, lambda m: m["angulos"][1].update(cita=""), "cita vacía")
    mut("05 evidencia", B, lambda m: m["angulos"][1].update(cita="N/A"), "cita de relleno")
    mut("06 estudio", B, lambda m: m.update(estudio="N/A"), "estudio de relleno")
    mut("06 estudio", B, lambda m: m.update(estudio="NO-EXISTE/estudio.md"), "estudio inexistente")
    mut("07 empresa y canal", B, lambda m: m.update(empresa=""), "sin empresa")
    mut("08 tofu sin precio", B, lambda m: P(m, 0).update(apoyo="Desde {PRECIO_1}"), "variable de precio en TOFU")
    mut("08 tofu sin precio", B, lambda m: P(m, 0).update(prompt=P(m, 0)["prompt"] + " Price tag {PRECIO_1}."), "precio en el prompt TOFU")
    mut("09 tofu no vende", B, lambda m: P(m, 3).update(titular="Sérum Ejemplo para tu piel"), "nombre completo en titular")
    mut("09 tofu no vende", B, lambda m: P(m, 0).update(apoyo="Ejemplo te cambia la mañana"), "nombre corto en el apoyo")
    mut("09 tofu no vende", B, lambda m: P(m, 0).update(titular="Cómpralo hoy"), "compra en el titular")
    mut("09 tofu no vende", B, lambda m: P(m, 3).update(cta="Shop now"), "compra en inglés")
    mut("09 tofu no vende", B, lambda m: P(m, 3).update(cta="Llévatelo"), "compra con tilde")
    mut("10 bofu confianza", B, lambda m: P(m, 5).update(sello="Envío a todo Colombia"), "sin sello de pago")
    mut("11 precio vivo", B, lambda m: P(m, 2).update(titular="$89.900 el par"), "precio con $")
    mut("11 precio vivo", B, lambda m: P(m, 2).update(titular="89900 pesos el par"), "precio sin formato")
    mut("11 precio vivo", B, lambda m: P(m, 2).update(titular="Solo 89 mil el par"), "precio en mil")
    mut("11 precio vivo", H, lambda m: P(m, 2).update(titular="89,900 el par"), "precio con coma")
    mut("11 precio vivo", H, lambda m: P(m, 2).update(titular="Solo Q199 el par"), "precio en quetzales")
    mut("12 producto real", B, lambda m: P(m, 1).update(foto_real=""), "sin foto")
    mut("12 producto real", B, lambda m: P(m, 1).update(foto_real="N/A"), "foto de relleno")
    mut("13 texto literal", B, lambda m: P(m, 1).update(prompt="Ultra-realistic photo, product as Image 1."), "prompt sin el titular")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + " no antes y después"), "antes y después")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + " before & after"), "before & after")
    mut("14 prompt", B, lambda m: P(m, 1).update(apoyo="con el sérum / sin el sérum"), "con/sin")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + " one sticker"), "sticker en singular")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + " NEGATIVES: no claims of money"), "negativo de claim")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + ' PROHIBIDO cualquier texto que diga "purifica"'),
        "prohibido que diga (prompt real de la casa, CREATIVOS.md del filtro, 1.4)")
    mut("14 prompt", B, lambda m: P(m, 1).update(prompt=P(m, 1)["prompt"] + " Avoid health claims wording."), "avoid claims")
    mut("15 signos", B, lambda m: P(m, 0).update(titular="\u00bfEstás en la mala?"), "apertura en el titular")
    mut("16 destino", B, lambda m: P(m, 2).update(destino="landing"), "precio a la landing")
    mut("16 destino", B, lambda m: P(m, 2).update(destino="organico"), "precio en orgánico")
    mut("17 reseña", B, lambda m: P(m, 4).update(apoyo="{RESEÑA_REAL}"), "reseña sin reemplazar")
    mut("17 reseña", B, lambda m: P(m, 4).update(apoyo="{RESENA_REAL}"), "reseña sin ñ")
    mut("17 reseña", B, lambda m: P(m, 4).update(apoyo="★★★★★ Me cambió la piel"), "estrellas sin fuente")
    mut("18 privados", B, lambda m: P(m, 2).update(sello=P(m, 2)["sello"] + " · WhatsApp 322 555 0199"), "teléfono")
    mut("19 públicos", H, lambda m: P(m, 1).pop("estado"), "MOFU sin marca de públicos")
    mut("20 ángulo", B, lambda m: P(m, 0).update(angulo="A9"), "ángulo inexistente")
    mut("21 titular único", B, lambda m: P(m, 3).update(titular="Lo que nadie te dice a los 40",
                                                        prompt=P(m, 0)["prompt"]), "mismo titular, misma etapa")
    mut("22 diversidad", B, lambda m: P(m, 4).update(formato="callouts"), "mismo formato en MOFU")
    mut("23 plan", B, lambda m: m.pop("plan"), "sin plan")
    mut("23 plan", B, lambda m: m["plan"]["conjuntos"][0].update(piezas=["P1", "P4", "P2", "P5"]), "4 en un conjunto")
    mut("23 plan", B, lambda m: m["plan"]["conjuntos"][2].update(piezas=["P3"]), "pieza fuera del plan")
    mut("24 belleza y salud", B, lambda m: [p.update(persona=False) for p in m["piezas"]], "sin persona")
    mut("24 belleza y salud", B, lambda m: m["plan"].pop("edad_minima"), "sin 18+")
    mut("25 veredicto", B, lambda m: m.update(entrega="Quedó listo, todo está bien"), "veredicto variante")
    mut("25 veredicto", B, lambda m: m.update(entrega="LISTO PARA LANZAR"), "veredicto en mayúsculas")
    return S


def estructuras_rotas():
    def sin_id(m):
        m["angulos"][0].pop("id")
    def bool_texto(m):
        m["piezas"][0]["generar"] = "false"
    out = [("lista en la raíz", [1, 2])]
    for nota, fn in (("ángulo sin id", sin_id), ("booleano como texto", bool_texto)):
        m = sana_belleza()
        fn(m)
        out.append((nota, m))
    return out


def autoprueba():
    ok = True
    tmp = tempfile.mkdtemp(prefix="vm-")
    try:
        open(os.path.join(tmp, "00-ESTUDIO.md"), "w").write("estudio de prueba")
        for nombre, sana in (("belleza CO", sana_belleza), ("hogar GT", sana_hogar_gt)):
            m = sana()
            e = estructura(m)
            got = e or validar(m, tmp)
            if got:
                ok = False
                print(f"FALLA: la sana {nombre} no pasa: {got}")
            else:
                print(f"ok  sana {nombre} pasa (0 fallos)")
        n = 0
        for casilla, m, nota in sabotajes():
            n += 1
            e = estructura(m)
            got = {c for c, _ in validar(m, tmp)} if not e else {"estructura"}
            if casilla in got:
                print(f"ok  {casilla} · {nota}")
            else:
                ok = False
                print(f"FALLA: {casilla} · {nota} NO detectado (vio: {sorted(got)})")
        for nota, m in estructuras_rotas():
            n += 1
            if estructura(m):
                print(f"ok  estructura · {nota} → exit 2")
            else:
                ok = False
                print(f"FALLA: estructura · {nota} no se detectó")
        total = n + 2
        print(f"AUTOPRUEBA: {'PASADA' if ok else 'FALLIDA'} · {total} casos (2 sanas, {n} que deben fallar)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--autoprueba":
        return autoprueba()
    ruta = sys.argv[1]
    try:
        with open(ruta, encoding="utf-8") as fh:
            m = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        print(f"NO SE PUEDE LEER: {e}")
        return 2
    e = estructura(m)
    if e:
        for x in e:
            print(f"ESTRUCTURA: {x}")
        print("COBERTURA: estructura inválida; no se corrieron las casillas")
        return 2
    fallos = validar(m, os.path.dirname(os.path.abspath(ruta)))
    for c, d in fallos:
        print(f"FALLA {c}: {d}")
    print(f"COBERTURA: {len(m['piezas'])} piezas · {len(m['angulos'])} ángulos · 25 casillas · {len(fallos)} fallos")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
