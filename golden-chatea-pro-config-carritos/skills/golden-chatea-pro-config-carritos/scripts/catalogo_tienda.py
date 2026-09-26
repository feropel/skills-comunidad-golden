#!/usr/bin/env python3
"""Lee el CATALOGO PUBLICO de una tienda Shopify (id -> titulo, sin token) y lo cruza con el cache.

POR QUE EXISTE. El cache de productos del asistente se juzgaba solo por su FORMA (que tuviera
fecha e id). Medido: habia entradas bien formadas que describian un perfume como producto "para
agricultores" y una recarga de fibra capilar como "servicio de recarga digital". La forma no dice
si el texto es verdad. El catalogo si: cada entrada del cache lleva el ID del producto y el
catalogo publico devuelve ese id con su titulo real.

COMO DECIDE, y por que asi (corregido tras la 2a verificacion adversarial, 22-sep):
  · compara PALABRAS normalizadas (sin tildes, sin mayusculas) de 3 letras o mas, MAS los numeros,
    porque "Kit #2" y "Kit #3" solo se distinguen por el numero;
  · CRITICA cuando no comparten ninguna palabra, o cuando los numeros se contradicen
    (el caso Kit #2 descrito como Kit #3: comparten casi todo y son productos distintos);
  · AVISO cuando la coincidencia es debil: menos de la mitad del MAS CORTO de los dos nombres.
    Se mide contra el mas corto a proposito, porque un nombre corto que calza entero ('Fijador'
    dentro de 'Fijador Marca | Spray de Larga Duracion') es correcto y acusarlo seria un falso positivo;
  · la clave del cache se normaliza a texto, porque el campo vivo guarda unos ids como numero.

LIMITES DECLARADOS: compara NOMBRE, no la descripcion entera — un titulo que calza no garantiza
que el resto sea cierto, por eso la auditoria sigue imprimiendo cada entrada para leerla a mano.
Solo sirve en tiendas Shopify con catalogo publico. Si el catalogo viene vacio, no acusa a nadie:
avisa de que el dominio no sirve.
"""
import json
import re
import unicodedata
import urllib.request

POR_PAGINA = 250
MAX_PAG = 40


class CatalogoVacio(Exception):
    """La tienda respondio pero no publico ni un producto: el cruce no se puede hacer."""


def catalogo(dominio, max_pag=MAX_PAG):
    """{id: titulo} del catalogo publico. Devuelve tambien si la paginacion se agoto."""
    dominio = dominio.replace("https://", "").replace("http://", "").strip("/")
    out, completo = {}, True
    for p in range(1, max_pag + 1):
        url = f"https://{dominio}/products.json?limit={POR_PAGINA}&page={p}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 golden-carritos"})
        with urllib.request.urlopen(req, timeout=30) as r:
            prods = json.loads(r.read().decode()).get("products", [])
        if not prods:
            break
        for x in prods:
            out[str(x["id"])] = x.get("title", "")
        if p == max_pag:
            completo = False
    if not out:
        raise CatalogoVacio(f"{dominio} no publica productos (tienda con clave, catalogo cerrado "
                            f"o dominio equivocado)")
    return out, completo


def _norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return set(re.findall(r"[a-z]{3,}|\d+", s))


def nombre_en_cache(info):
    """El nombre que el cache le dice al bot, venga en su linea o en prosa."""
    m = re.search(r"Nombre(?: del producto)?:\s*(.+)", str(info), re.I)
    return (m.group(1) if m else str(info)[:120]).strip()


def comparar(cache, cat):
    """(huerfanas, discrepantes, debiles, no_evaluables). Nada se salta en silencio."""
    huerfanas, discrepantes, debiles, no_evaluables = [], [], [], []
    for k, e in cache.items():
        clave = str(k)
        info = e.get("info", "") if isinstance(e, dict) else e
        if not isinstance(info, str) or not info.strip():
            no_evaluables.append((clave, "la entrada no trae texto legible"))
            continue
        nom = nombre_en_cache(info)
        if clave not in cat:
            huerfanas.append((clave, nom))
            continue
        pal_cache, pal_cat = _norm(nom), _norm(cat[clave])
        if not pal_cat:
            no_evaluables.append((clave, "el titulo de la tienda no tiene palabras comparables"))
            continue
        comunes = pal_cache & pal_cat
        num_cache = {x for x in pal_cache if x.isdigit()}
        num_cat = {x for x in pal_cat if x.isdigit()}
        if not comunes:
            discrepantes.append((clave, nom, cat[clave], "no comparten ni una palabra"))
        elif num_cache and num_cat and not (num_cache & num_cat):
            discrepantes.append((clave, nom, cat[clave], "el numero del producto no coincide"))
        elif len(comunes) / min(len(pal_cat), len(pal_cache) or 1) < 0.5:
            debiles.append((clave, nom, cat[clave]))
    return huerfanas, discrepantes, debiles, no_evaluables


def autoprueba():
    """Los DOS sentidos: que cace la mentira y que CALLE con el cache sano."""
    cat = {"1": "Brisa Nativa Spray | Frescura que Dura",
           "2": "Kit Aurora #2 | Polvo Capilar + Fijador",
           "3": "Café Orgánico Instantáneo"}
    corridas, fallos = [], []

    def check(t, ok, ev=""):
        corridas.append(t)
        print(f"  {'OK   ' if ok else 'FALLA'} · {t}")
        if not ok:
            fallos.append(t)
            print("        ", ev)

    sano = {"1": {"info": "Nombre del producto: Brisa Nativa Spray, frescura que dura"},
            "2": {"info": "Kit Aurora #2 con polvo capilar y fijador"}}
    h, d, w, n = comparar(sano, cat)
    check("0 · cache que calza no dice nada (control negativo)",
          not (h or d or w or n), f"{h} {d} {w} {n}")

    h, d, w, n = comparar({"1": {"info": "Nombre del producto: Abono para cultivos"}}, cat)
    check("1 · nombre sin nada que ver -> discrepante", len(d) == 1, str(d))

    h, d, w, n = comparar({"2": {"info": "Kit Aurora #3, atomizador y fijador"}}, cat)
    check("2 · MISMA familia y OTRO numero (Kit #2 descrito como #3) -> discrepante",
          len(d) == 1 and "numero" in d[0][3], f"{d} {w}")

    h, d, w, n = comparar({"99": {"info": "Nombre del producto: Retirado"}}, cat)
    check("3 · id que ya no esta en el catalogo -> huerfana", len(h) == 1, str(h))

    h, d, w, n = comparar({"3": {"info": "Cafe Organico Instantaneo en polvo"}}, cat)
    check("4 · mismo nombre SIN tildes no dispara (plegado de acentos)",
          not (d or w), f"{d} {w}")

    h, d, w, n = comparar({"2": {"info": "Nombre del producto: Kit Aurora"}}, cat)
    check("5 · nombre corto que calza entero -> NO dispara (falso positivo evitado)",
          not (d or w), f"{d} {w}")

    h, d, w, n = comparar({"2": {"info": "Kit de maquillaje tono claro, cobertura media, brillo"}}, cat)
    check("5b · nombre largo que comparte casi nada -> AVISO debil, no critica",
          len(w) == 1 and not d, f"{d} {w}")

    h, d, w, n = comparar({"2": "BASURA TOTAL DE OTRO PLANETA"}, cat)
    check("6 · entrada que no es diccionario se evalua igual, no se salta",
          len(d) == 1, f"{d} {n}")

    h, d, w, n = comparar({2: {"info": "Kit Aurora #2 con polvo capilar"}}, cat)
    check("7 · id guardado como NUMERO no se acusa de huerfano", not h, str(h))

    h, d, w, n = comparar({"1": {"info": ""}}, cat)
    check("8 · entrada vacia -> no evaluable, y se cuenta", len(n) == 1, str(n))

    try:
        catalogo("ejemplo-que-no-existe-golden.myshopify.com", max_pag=1)
        check("9 · dominio que no responde -> excepcion", False, "no lanzo excepcion")
    except CatalogoVacio:
        check("9 · dominio que responde sin productos -> CatalogoVacio, no acusa al cache", True)
    except Exception as e:  # noqa: BLE001
        check("9 · dominio que no responde -> excepcion, no acusa al cache", True, type(e).__name__)

    print(f"\n  COBERTURA: {len(corridas) - len(fallos)} de {len(corridas)} pruebas en verde")
    return 0 if not fallos else 1


if __name__ == "__main__":
    import sys
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    c, completo = catalogo(sys.argv[1])
    print(f"{len(c)} productos publicados en {sys.argv[1]} · catalogo completo: {completo}")
