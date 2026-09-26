#!/usr/bin/env python3
"""
competencia.py — quién anuncia el producto HOY, quién ya lo abandonó y a cuánto lo venden.

Por qué existe (medido 2026-09-18 con el nivel láser y la caja montessori):
1. Contar anunciantes por PALABRA CLAVE en la Ad Library falla cuando la palabra es ambigua
   ("nivel láser" trajo 850 anuncios de depilación). semantic_search_ads con la IMAGEN SOLA
   tampoco sirve: 0 de 13 anuncios eran del producto. Con IMAGEN + una DESCRIPCIÓN corta:
   14 de 14 relevantes en los dos productos.
2. Un anunciante que ya no se ve no es competencia: es CEMENTERIO. La vigencia se lee en
   lastSeenActiveAt (trampa 5): visto en los últimos 7 días = activo.
3. El precio de la competencia estaba "no visto" en la primera corrida. Las landings de
   Shopify publican /products/<handle>.json: 7 de 7 se leyeron gratis, sin raspar.

Uso:
  python3 competencia.py canal anuncios.json [--incluir REGEX] [--hoy AAAA-MM-DD] [--canal landing|whatsapp]
  python3 competencia.py precios anuncios.json [--pvp-minimo 138662] [--incluir REGEX]
  python3 competencia.py --autoprueba
anuncios.json = la respuesta de semantic_search_ads guardada tal cual ({"data":[...]}).
"precios" hace una llamada HTTP por landing distinta (máximo 8), solo a tiendas Shopify.
Solo biblioteca estándar de Python 3.
"""
import json
import os
import re
import statistics
import sys
import urllib.request
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

DIAS_ACTIVO = 7        # trampa 5: "ACTIVE" con fecha vieja no es activo hoy
MAX_LANDINGS = 8


class ErrorDeEntrada(Exception):
    pass


def cargar(ruta):
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise ErrorDeEntrada("no se pudo leer %s: %s" % (ruta, e))
    filas = d.get("data") if isinstance(d, dict) else d
    if not isinstance(filas, list):
        raise ErrorDeEntrada("la respuesta no trae una lista de anuncios")
    return [f for f in filas if isinstance(f, dict)]


def dia(iso):
    try:
        return datetime.fromisoformat(str(iso).replace("Z", "+00:00")).date()
    except ValueError:
        return None


# Dominios que comparten tiendas distintas: no identifican a nadie (verificador, 2026-09-18).
DOMINIOS_COMPARTIDOS = ("wa.me", "api.whatsapp.com", "whatsapp.com", "web.whatsapp.com", "wa.link",
                        "linktr.ee", "facebook.com", "m.facebook.com", "l.facebook.com", "instagram.com",
                        "l.instagram.com", "fb.me", "bit.ly", "tiktok.com", "linkin.bio", "beacons.ai")
WHATSAPP = ("wa.me", "api.whatsapp.com", "whatsapp.com", "web.whatsapp.com", "wa.link")
# Un nombre genérico no identifica aunque traiga el país ("Tienda Online CO" = "Tienda Online").
NOMBRES_GENERICOS = {"tienda online", "tienda", "shop", "store", "tienda virtual", "ofertas", "(sin nombre)",
                     "online shop", "mi tienda", "la tienda", "tu tienda"}
PAISES = r"\b(co|col|colombia|mx|mexico|ec|pe|cl|gt|oficial|official)\b"


def host(url):
    """Host sin www ni puerto. Lee cualquier esquema: 'whatsapp://send' es WhatsApp, 'wa.me/57...'
    sin esquema es wa.me, 'wa.me:443' es wa.me (el verificador encontró los tres uniendo tiendas)."""
    from urllib.parse import urlsplit
    t = url.strip() if isinstance(url, str) else ""
    if not t:
        return None
    if re.match(r"whatsapp:", t, re.I):
        return "wa.me"
    if not re.match(r"[a-z][a-z0-9+.-]*://", t, re.I):
        t = "https://" + t
    try:
        h = (urlsplit(t).hostname or "").lower()
    except ValueError:
        return None
    return re.sub(r"^www\.", "", h) or None


def es_whatsapp(url):
    h = host(url) or ""
    return h in WHATSAPP or "whatsapp" in h or h in ("walink.co", "wa.link")


def compartido(h):
    """Un host que no identifica a una tienda: mensajería, redes y acortadores."""
    return (h in DOMINIOS_COMPARTIDOS or "whatsapp" in h or h in ("m.me", "walink.co", "messenger.com")
            or h.endswith(".facebook.com") or h.endswith(".instagram.com"))


def generico(nom):
    """'Tienda Online (CO)', 'Tienda-Online', 'TiendaOnline 2' y 'Tienda Online.' son genéricos:
    se compara sin puntuación, sin dígitos, sin espacios y sin el país."""
    n = re.sub(PAISES, " ", comun.clave(nom))
    pegado = re.sub(r"[^a-z]", "", n)
    return pegado in {g.replace(" ", "") for g in NOMBRES_GENERICOS}


def dominio(url):
    d = host(url)
    return None if not d or compartido(d) else d


PACK = re.compile(r"(\b\d+\s*x\s*\d+\b|\bx\s*[2-9]\b|\b[2-9]\s*x\b|\bpack\b|\bcombo\b|\bkit\b|\bd[uú]o\b|\b[2-9]\s*unidades\b)", re.I)


def filtrar(anuncios, incluir):
    if not incluir:
        return anuncios, 0
    try:
        patron = re.compile(incluir, re.I)
    except re.error as e:
        raise ErrorDeEntrada("--incluir no es una expresión válida: %s" % e)
    dentro = [a for a in anuncios if patron.search(" ".join(str(a.get(k) or "") for k in ("title", "description", "landingUrl")))]
    return dentro, len(anuncios) - len(dentro)


def canal(anuncios, incluir=None, hoy=None, solo_canal=None):
    hoy = hoy or date.today()
    anuncios, fuera = filtrar(anuncios, incluir)
    if solo_canal in ("landing", "whatsapp"):
        antes = len(anuncios)
        anuncios = [a for a in anuncios if (es_whatsapp(a.get("landingUrl")) or not a.get("landingUrl")) == (solo_canal == "whatsapp")]
        fuera += antes - len(anuncios)
    # Identidad = componente conexo por NOMBRE de página o DOMINIO de landing: una tienda con dos
    # nombres (Anturio / Anturio Care) o dos páginas, con o sin landing, es UN anunciante.
    padre = {}
    def raiz(x):
        while padre.setdefault(x, x) != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    def unir(a, b):
        padre[raiz(a)] = raiz(b)
    ids = []
    for a in anuncios:
        nom = comun.clave(a.get("advertiserName"))
        if generico(nom):
            nom = ""  # "Tienda Online (CO)" no identifica: dos tiendas con ese nombre no son una
        llaves = [k for k in (("n:" + nom) if nom else None, ("d:" + dominio(a.get("landingUrl"))) if dominio(a.get("landingUrl")) else None) if k]
        if not llaves:
            llaves = ["p:" + str(a.get("publisherId") or id(a))]
        for k in llaves[1:]:
            unir(llaves[0], k)
        ids.append(llaves[0])
    por = {}
    for a, primera in zip(anuncios, ids):
        # Una marca puede anunciar con varias páginas (Cabuco Store usa dos publisherId: medido
        # 2026-09-18). Se agrupa por NOMBRE; el publisherId solo cuando no hay nombre.
        clave = raiz(primera)
        visto = dia(a.get("lastSeenActiveAt"))
        p = por.setdefault(clave, {"anunciante": a.get("advertiserName") or "(sin nombre)",
                                   "anuncios": 0, "ultimo_visto": None, "max_dias_activo": 0,
                                   "landings": set(), "canal": set()})
        p["anuncios"] += 1
        if visto and (p["ultimo_visto"] is None or visto > p["ultimo_visto"]):
            p["ultimo_visto"] = visto
        dias_act = a.get("activeDays")
        dias_act = dias_act if isinstance(dias_act, (int, float)) and not isinstance(dias_act, bool) else 0
        p["max_dias_activo"] = max(p["max_dias_activo"], dias_act)
        if a.get("landingUrl"):
            p["landings"].add(str(a["landingUrl"]).split("?")[0])
        p["canal"].add("WhatsApp" if es_whatsapp(a.get("landingUrl")) or not a.get("landingUrl") else "landing")
        if visto is None:
            p["sin_fecha"] = True
    activos, cementerio = [], []
    for p in por.values():
        fila = dict(p, ultimo_visto=str(p["ultimo_visto"]) if p["ultimo_visto"] else None,
                    landings=sorted(p["landings"]), canal=sorted(p["canal"]))
        # Sin fecha legible se cuenta ACTIVO: un dato que falta nunca baja la competencia.
        vivo = p.get("sin_fecha") or (p["ultimo_visto"] and (hoy - p["ultimo_visto"]).days <= DIAS_ACTIVO)
        (activos if vivo else cementerio).append(fila)
    avisos = []
    if fuera:
        avisos.append("%d anuncio(s) fuera por --incluir (no son de este producto)" % fuera)
    sin_fecha = sum(1 for p in por.values() if p.get("sin_fecha"))
    if sin_fecha:
        avisos.append("%d anunciante(s) sin lastSeenActiveAt legible: contados como ACTIVOS" % sin_fecha)
    if not por:
        avisos.append("ningún anuncio del producto: NO es canal libre, es canal SIN MEDIR (probar otra descripción)")
    por_canal = {"landing": sum(1 for a in activos if "landing" in a["canal"]),
                 "whatsapp": sum(1 for a in activos if "WhatsApp" in a["canal"])}
    return {"anunciantes_activos": len(activos), "anunciantes_en_cementerio": len(cementerio),
            "activos_por_canal": por_canal,
            "canal_mas_libre": min(por_canal, key=lambda k: (por_canal[k], k != "landing")),
            "activos": activos, "cementerio": cementerio, "anuncios_leidos": len(anuncios),
            "hoy": str(hoy), "avisos": avisos + ["activo = visto en los últimos %d días (lastSeenActiveAt)" % DIAS_ACTIVO]}


def url_json(landing):
    base = landing.split("?")[0].split("#")[0].rstrip("/")
    if "/products/" not in base:
        return None
    return base + ".json"


def leer_precio(landing, abrir=None):
    u = url_json(landing)
    if not u:
        return {"landing": landing, "precio": None, "motivo": "no es una ficha de producto Shopify: mirarla a mano"}
    abrir = abrir or (lambda url: urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read())
    try:
        p = json.loads(abrir(u))["product"]
        precios = sorted({float(v["price"]) for v in p.get("variants", []) if v.get("price")})
        if precios and precios[0] < 1000:
            # Un precio de 29,99 no es en pesos (trampa 6: país mal asignado). No se compara.
            return {"landing": landing, "precio": None, "motivo": "precio %s: parece otra moneda (trampa 6), no se compara" % precios[0]}
        tachados = sorted({float(v["compare_at_price"]) for v in p.get("variants", []) if v.get("compare_at_price")})
    except Exception as e:  # red, 404, tienda que no es Shopify, JSON raro: se dice, no se inventa
        return {"landing": landing, "precio": None, "motivo": "no legible (%s): mirarla a mano" % type(e).__name__}
    if not precios:
        return {"landing": landing, "precio": None, "motivo": "la ficha no trae precio"}
    titulos = " ".join([p.get("title") or ""] + [str(v.get("title") or "") for v in p.get("variants", [])])
    return {"landing": landing, "titulo": p.get("title"), "precio": precios[0],
            "precio_max": precios[-1], "tachado": tachados[-1] if tachados else None,
            # Un pack de 2 no se compara con el mínimo de 1 (shampoo: 2 barras a $79.900 contra el
            # mínimo de UNA a $70.276 salía "CIERRA": medido 2026-09-18). Se marca, no se adivina.
            "posible_pack": bool(PACK.search(titulos))}


def precios(anuncios, pvp_minimo=None, abrir=None, incluir=None):
    anuncios, _ = filtrar(anuncios, incluir)
    landings = []
    for a in anuncios:
        l = a.get("landingUrl") if isinstance(a.get("landingUrl"), str) else ""
        l = l.split("?")[0]
        if l and l not in landings:
            landings.append(l)
    omitidas = max(len(landings) - MAX_LANDINGS, 0)
    filas = [leer_precio(l, abrir) for l in landings[:MAX_LANDINGS]]
    packs = [f for f in filas if f.get("posible_pack")]
    vistos = [f["precio"] for f in filas if f.get("precio") and not f.get("posible_pack")]
    r = {"landings": len(landings), "leidas": len(vistos), "filas": filas, "avisos": []}
    if packs:
        r["avisos"].append("%d landing(s) parecen pack o combo y NO entran a la comparación: %s"
                           % (len(packs), ", ".join((f.get("titulo") or f["landing"])[:40] for f in packs)))
    if omitidas:
        r["avisos"].append("%d landing(s) sin leer por el tope de %d" % (omitidas, MAX_LANDINGS))
    if not vistos:
        r["avisos"].append("ningún precio legible de UNA unidad: la competencia queda NO VISTA, no se supone")
        return r
    r["precio_min"], r["precio_mediana"], r["precio_max"] = min(vistos), statistics.median(vistos), max(vistos)
    if len(vistos) == 1:
        r["avisos"].append("un solo precio visto: referencia débil, no veredicto firme")
    if pvp_minimo:
        r["pvp_minimo"] = pvp_minimo
        r["holgura_sobre_mediana"] = round(r["precio_mediana"] / pvp_minimo - 1, 3)
        r["plata"] = ("CIERRA" if r["precio_min"] >= pvp_minimo else
                      "NO CIERRA" if r["precio_mediana"] < pvp_minimo else
                      "JUSTA: la mediana cierra, el más barato no")
    return r


def autoprueba():
    hoy = date(2026, 9, 18)
    def ad(pub, visto, landing=None, titulo="caja montessori", plataformas=None):
        return {"publisherId": pub, "advertiserName": pub, "lastSeenActiveAt": visto + "T00:00:00Z",
                "landingUrl": landing or "https://%s.co/products/a" % pub, "title": titulo, "description": "", "activeDays": 10,
                "platforms": plataformas or ["FACEBOOK"]}
    casos = 0
    fallos = []
    def chequeo(nombre, ok):
        nonlocal casos
        casos += 1
        if not ok:
            fallos.append(nombre)
    # montessori medido: 1 activo (Cabuco, visto 16-sep) y 4 en cementerio
    m = [ad("cabuco", "2026-09-16"), ad("cabuco", "2026-09-05"), ad("polar", "2026-08-09"),
         ad("todito", "2026-08-06"), ad("dixon", "2026-07-17"), ad("pagaal", "2026-08-17")]
    r = canal(m, hoy=hoy)
    chequeo("activos por lastSeenActiveAt", r["anunciantes_activos"] == 1)
    chequeo("cementerio", r["anunciantes_en_cementerio"] == 4)
    chequeo("un anunciante con dos anuncios cuenta una vez", len(r["activos"]) == 1 and r["activos"][0]["anuncios"] == 2)
    # --incluir saca lo que no es del producto (el masajeador que trajo la imagen sola)
    r = canal(m + [ad("orbita", "2026-09-17", titulo="masajeador 4D")], incluir="montessori", hoy=hoy)
    chequeo("--incluir filtra ajenos", r["anunciantes_activos"] == 1)
    r = canal([ad("p1", "2026-09-16"), dict(ad("p2", "2026-08-01"), advertiserName="p1", landingUrl=None)], hoy=hoy)
    chequeo("una marca con dos páginas es un anunciante, activo", r["anunciantes_activos"] == 1 and r["anunciantes_en_cementerio"] == 0)
    # Anturio y Anturio Care: dos NOMBRES, la misma landing (medido 2026-09-18)
    r = canal([ad("anturio", "2026-09-16", "https://www.anturiocare.com/products/olla"),
               ad("anturio care", "2026-08-01", "https://anturiocare.com/products/olla")], hoy=hoy)
    chequeo("dos nombres con el mismo dominio son una tienda", r["anunciantes_activos"] == 1 and r["anunciantes_en_cementerio"] == 0)
    # WhatsApp: cuatro tiendas distintas que mandan a wa.me son cuatro, y su canal es WhatsApp
    wa = [dict(ad("t%d" % i, "2026-09-17"), landingUrl="https://wa.me/57300000000%d" % i) for i in range(4)]
    r = canal(wa, hoy=hoy)
    chequeo("wa.me no une tiendas distintas", r["anunciantes_activos"] == 4)
    chequeo("wa.me es canal WhatsApp", all(a["canal"] == ["WhatsApp"] for a in r["activos"]))
    r = canal(wa + [ad("landing1", "2026-09-17")], hoy=hoy, solo_canal="landing")
    chequeo("--canal landing cuenta solo landing", r["anunciantes_activos"] == 1)
    r = canal([dict(ad("x", "2026-09-17"), advertiserName="Tienda Online"), dict(ad("y", "2026-09-17"), advertiserName="Tienda Online")], hoy=hoy)
    chequeo("dos 'Tienda Online' con dominios distintos son dos", r["anunciantes_activos"] == 2)
    r = canal([dict(ad("z", "2026-09-17"), lastSeenActiveAt="18-09-2026")], hoy=hoy)
    chequeo("fecha ilegible cuenta ACTIVO", r["anunciantes_activos"] == 1 and any("sin lastSeenActiveAt" in a for a in r["avisos"]))
    def abrir_usd(u):
        return json.dumps({"product": {"title": "x", "variants": [{"price": "29.99"}]}})
    r = precios([{"landingUrl": "https://usd.co/products/x"}], 78870, abrir_usd)
    chequeo("precio en otra moneda no se compara", "precio_min" not in r and "otra moneda" in r["filas"][0]["motivo"])
    r = canal([dict(ad("q", "2026-09-17"), activeDays="diez")], hoy=hoy)
    chequeo("activeDays en texto no revienta", r["anunciantes_activos"] == 1)
    wa2 = [dict(ad("w%d" % i, "2026-09-17"), landingUrl=u) for i, u in enumerate(
        ["https://web.whatsapp.com/send?phone=1", "https://wa.link/abc", "https://l.facebook.com/x", "wa.me/573001",
         "whatsapp://send?phone=2", "https://chat.whatsapp.com/xyz", "https://walink.co/q", "https://wa.me:443/5", "https://m.me/tienda"])]
    r = canal(wa2, hoy=hoy)
    chequeo("enlaces de mensajería o redes no unen tiendas distintas", r["anunciantes_activos"] == 9)
    chequeo("wa.me sin esquema es WhatsApp", r["activos_por_canal"]["whatsapp"] >= 3)
    gen = ["Tienda Online CO", "tienda  online co", "Tienda Online (CO)", "Tienda-Online", "TiendaOnline 2", "Tienda Online."]
    r = canal([dict(ad("g%d" % i, "2026-09-17"), advertiserName=n) for i, n in enumerate(gen)], hoy=hoy)
    chequeo("nombres genéricos con puntuación, dígitos o país no unen tiendas", r["anunciantes_activos"] == len(gen))
    r = canal([dict(ad("n", "2026-09-17"), landingUrl=12345)], hoy=hoy)
    chequeo("landingUrl que no es texto no revienta", r["anunciantes_activos"] == 1)
    mix = [ad("l1", "2026-09-17"), ad("l2", "2026-09-17")] + [dict(ad("z%d" % i, "2026-09-17"), landingUrl="https://wa.me/5730%d" % i) for i in range(2)]
    r = canal(mix, hoy=hoy)
    chequeo("conteo por canal y el más libre", r["activos_por_canal"] == {"landing": 2, "whatsapp": 2} and r["canal_mas_libre"] == "landing")
    r = canal([], hoy=hoy)
    chequeo("cero anuncios = SIN MEDIR, no libre", any("SIN MEDIR" in a for a in r["avisos"]))
    # precios con red falsa: 5 landings reales medidas el 18-sep
    tabla = {"https://a.co/products/x.json": 159900, "https://b.co/products/x.json": 149900,
             "https://c.co/products/x.json": 169900, "https://d.co/products/x.json": 159900}
    def abrir(u):
        if u not in tabla:
            raise OSError("404")
        return json.dumps({"product": {"title": "x", "variants": [{"price": str(tabla[u]), "compare_at_price": "199900"}]}})
    anuncios = [{"landingUrl": "https://%s.co/products/x?utm=1" % k} for k in "abcde"] + [{"landingUrl": "https://f.co/"}]
    r = precios(anuncios, 138662, abrir)
    chequeo("lee 4 de 6 y dice cuáles no", r["leidas"] == 4 and r["landings"] == 6)
    chequeo("mediana", r["precio_mediana"] == 159900)
    chequeo("plata CIERRA", r["plata"] == "CIERRA")
    r = precios(anuncios, 155000, abrir)
    chequeo("plata JUSTA", r["plata"].startswith("JUSTA"))
    r = precios(anuncios, 165000, abrir)
    chequeo("plata NO CIERRA", r["plata"] == "NO CIERRA")
    def abrir_pack(u):
        titulo = "Shampoo en barra x2" if "pack" in u else "Shampoo en barra"
        return json.dumps({"product": {"title": titulo, "variants": [{"price": "79900"}]}})
    r = precios([{"landingUrl": "https://pack.co/products/x"}, {"landingUrl": "https://uno.co/products/x"}], 70276, abrir_pack)
    chequeo("el pack no entra a la comparación", r["leidas"] == 1 and any("pack" in a for a in r["avisos"]))
    chequeo("un solo precio se avisa como débil", any("un solo precio" in a for a in r["avisos"]))
    r = precios([{"landingUrl": "https://a.co/products/x", "title": "olla de vidrio"},
                 {"landingUrl": "https://b.co/products/x", "title": "olla multifuncion"}], 100000, abrir, "vidrio")
    chequeo("precios respeta --incluir", r["landings"] == 1)
    r = precios([{"landingUrl": "https://z.co/"}], 1000, abrir)
    chequeo("sin precio = NO VISTA, sin inventar", "precio_min" not in r and any("NO VISTA" in a for a in r["avisos"]))
    for f in fallos:
        print("FALLA", f)
    print("AUTOPRUEBA %d de %d" % (casos - len(fallos), casos))
    return 1 if fallos else 0


def arg(bandera):
    if bandera not in sys.argv:
        return None
    i = sys.argv.index(bandera)
    if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
        raise ErrorDeEntrada("%s necesita un valor" % bandera)
    return sys.argv[i + 1]


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 3 or sys.argv[1] not in ("canal", "precios"):
        print(__doc__)
        sys.exit(2)
    try:
        anuncios = cargar(sys.argv[2])
        if sys.argv[1] == "canal":
            h = arg("--hoy")
            hoy = date.fromisoformat(h) if h else None
            c = arg("--canal")
            if c is not None and c not in ("landing", "whatsapp"):
                raise ErrorDeEntrada("--canal debe ser landing o whatsapp (vino %r)" % c)
            out = canal(anuncios, arg("--incluir"), hoy, c)
        else:
            m = arg("--pvp-minimo")
            pv = comun.numero(m) if m is not None else None
            if m is not None and (pv is None or pv <= 0):
                raise ErrorDeEntrada("--pvp-minimo debe ser un precio mayor que 0 (vino %r)" % m)
            out = precios(anuncios, pv, None, arg("--incluir"))
        print(json.dumps(out, ensure_ascii=False, indent=1))
    except (ErrorDeEntrada, ValueError) as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 — forma rara del JSON: error controlado, no traza
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
