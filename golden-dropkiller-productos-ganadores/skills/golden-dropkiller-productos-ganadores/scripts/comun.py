#!/usr/bin/env python3
"""
comun.py — UNA sola forma de normalizar identidades, números y fechas para los 7 scripts.

Por qué existe (tercera pasada del verificador, 2026-09-18): cada script normalizaba a su
manera. " 2233043" y "2233043" eran dos fichas en consolidar_mercado y una en entrega_golden;
"évora home" y "Évora  Home" dos proveedores; "30.000" era $30 en viabilidad_cod y $30.000 en
correr_lote; un 0% de entrega caía a la tasa general porque `if tasa` trata el 0 como vacío.
La regla: toda comparación de identidad pasa por clave(), todo número por numero(), toda fecha
por fecha_iso(), y un número se pregunta con `is None`, nunca con su verdad.
  python3 comun.py --autoprueba
"""
import math
import re
import sys
import unicodedata
from datetime import date, datetime


def sin_tildes(x):
    return "".join(c for c in unicodedata.normalize("NFD", str(x)) if unicodedata.category(c) != "Mn")


def clave(x):
    """Identidad de texto: sin tildes, minúsculas, un solo espacio, sin espacios en los bordes.
    'Évora  Home', 'evora home' y ' EVORA HOME ' son la misma."""
    if x is None:
        return ""
    return re.sub(r"\s+", " ", sin_tildes(x)).strip().lower()


def ident(x):
    """ID como texto limpio: ' 123298', 123298.0 y '123298' son el mismo."""
    if x is None or isinstance(x, bool):
        return ""
    if isinstance(x, float):
        if not math.isfinite(x):
            return ""
        if x.is_integer():
            x = int(x)
    t = str(x).strip()
    return t[:-2] if re.fullmatch(r"\d+\.0", t) else t


def numero(x, miles=True):
    """Número real o None. Con miles=True (pesos, unidades) lee '30.000' y '1.193.000' como miles
    (punto de miles); '30000.5' y '30000,5' tienen decimales; '0.727' es SIEMPRE decimal. Con
    miles=False (fracciones: entrega, comisión) el punto es siempre decimal. Rechaza bool, NaN,
    inf y texto. Medido: '0.727' se leía 727 y hacía fallar --entrega (lo encontró la prueba)."""
    if isinstance(x, bool) or x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x) if math.isfinite(x) else None
    t = str(x).strip().replace("$", "").replace(" ", "")
    if not t:
        return None
    if miles and re.fullmatch(r"-?[1-9]\d{0,2}(\.\d{3})+", t):   # 30.000 · 1.193.000 → miles (no '0.727')
        t = t.replace(".", "")
    elif miles and re.fullmatch(r"-?[1-9]\d{0,2}(,\d{3})+", t):    # 30,000 · 1,500 → miles (formato inglés)
        t = t.replace(",", "")
    elif miles and re.fullmatch(r"-?[1-9]\d{0,2}(\.\d{3})+,\d+", t):  # 30.000,50
        t = t.replace(".", "").replace(",", ".")
    elif miles and re.fullmatch(r"-?[1-9]\d{0,2}(,\d{3})+\.\d+", t):  # 30,000.50
        t = t.replace(",", "")
    elif re.fullmatch(r"-?\d+,\d+", t):                   # 30000,5
        t = t.replace(",", ".")
    try:
        v = float(t)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def fecha_iso(x):
    """AAAA-MM-DD o None. Acepta date, datetime, 'AAAA-MM-DD...', 'DD-MM-AAAA' y 'DD/MM/AAAA'."""
    if isinstance(x, datetime):
        return x.strftime("%Y-%m-%d")
    if isinstance(x, date):
        return x.isoformat()
    t = str(x or "").strip()
    # ISO con hora: la hora también tiene que ser válida ("2026-09-01T25:00" no es fecha).
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}([T ].*)?", t):
        try:
            return datetime.fromisoformat(t.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except ValueError:
            return None
    # Sin basura al final: "2026-09-01garbage" no es fecha. DD-MM-AAAA es el formato de Dropi.
    for f, patron in (("%d-%m-%Y", r"\d{2}-\d{2}-\d{4}"), ("%d/%m/%Y", r"\d{2}/\d{2}/\d{4}")):
        if re.fullmatch(patron, t):
            try:
                return datetime.strptime(t, f).strftime("%Y-%m-%d")
            except ValueError:
                return None
    return None


def tasa(x):
    """Fracción en (0, 1] o None: una tasa de entrega de 73.5, -0.2, True o NaN no es una tasa
    (un agregado mal escrito daba un PVP mínimo NEGATIVO que salía LISTA: verificador)."""
    v = numero(x, miles=False)
    return v if v is not None and 0 < v <= 1 else None


def autoprueba():
    casos = [
        ("clave con tildes y espacios", clave("Évora  Home ") == clave("evora home")),
        ("ident con espacio", ident(" 2233043 ") == "2233043"),
        ("ident 123298.0", ident(123298.0) == "123298" and ident("123298.0") == "123298"),
        ("ident bool", ident(True) == ""),
        ("numero 30.000 son miles", numero("30.000") == 30000),
        ("numero 1.193.000", numero("1.193.000") == 1193000),
        ("numero 30000.5 decimal", numero("30000.5") == 30000.5),
        ("numero 30000,5 decimal", numero("30000,5") == 30000.5),
        ("numero 0.727 es decimal", numero("0.727") == 0.727),
        ("numero sin miles: 1.500 es 1,5", numero("1.500", miles=False) == 1.5),
        ("numero NaN", numero(float("nan")) is None and numero("nan") is None and numero("inf") is None),
        ("numero bool", numero(True) is None),
        ("numero texto", numero("abc") is None),
        ("fecha DD-MM-AAAA", fecha_iso("01-09-2026") == "2026-09-01"),
        ("fecha ISO con hora", fecha_iso("2026-09-01T05:00:00Z") == "2026-09-01"),
        ("fecha ilegible", fecha_iso("31-02-2026") is None),
        ("fecha con basura", fecha_iso("2026-09-01garbage") is None and fecha_iso("2026-09-01T25:00") is None),
        ("numero 30,000 son miles", numero("30,000") == 30000 and numero("1,500") == 1500),
        ("numero 30000,5 sigue decimal", numero("30000,5") == 30000.5),
        ("tasa fuera de rango", tasa(73.5) is None and tasa(-0.2) is None and tasa(True) is None and tasa("nan") is None and tasa(0) is None),
        ("tasa válida", tasa(0.727) == 0.727 and tasa("0,727") == 0.727 and tasa(1) == 1),
    ]
    fallos = [n for n, ok in casos if not ok]
    for f in fallos:
        print("FALLA", f)
    print("AUTOPRUEBA %d de %d" % (len(casos) - len(fallos), len(casos)))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(autoprueba() if "--autoprueba" in sys.argv else (print(__doc__) or 2))
