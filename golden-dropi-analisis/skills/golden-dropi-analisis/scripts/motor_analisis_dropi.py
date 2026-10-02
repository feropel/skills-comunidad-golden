# -*- coding: utf-8 -*-
"""
MOTOR DE ANÁLISIS DROPI — skill golden-dropi-analisis
Lee los exports crudos de Dropi (por pedido = 63 cols, por producto = 53 cols),
los agrupa por cuenta/periodo y genera 2 maestros Excel en <base>/Analisis/:
    MAESTRO_LOGISTICA.xlsx   (KPIs de entrega, transportadoras, ciudades, novedades, evolución)
    MAESTRO_CONTACTOS.xlsx   (clientes dedup por teléfono, % efectividad, segmentos, enriquecido)

USO:
    python3 motor_analisis_dropi.py "<carpeta_base>"
  <carpeta_base> = carpeta que contiene los exports. Puede tener:
    - subcarpetas por cuenta (ej. Hotmail/, Gmail/, Cliente-A/) con los .xlsx dentro, o
    - los .xlsx sueltos directamente (se tratan como una sola cuenta "General").
  Si no se pasa carpeta, usa el directorio actual.

CONFIG OPCIONAL — <base>/_config_dropi.json:
    {
      "test_phones": ["3001234567"],           # teléfonos de prueba a excluir (dueño/tester)
      "test_name_keywords": ["PRUEBA","TEST"],  # nombres a excluir
      "currency": "$"
    }

ENRIQUECIMIENTO OPCIONAL (si existen, se usan; si no, se omiten sin error) en
<base>/Analisis/_FUENTES/:
    - "Etiquetas *.csv" / "Contactos *.csv"  (export de WhatsApp con columnas phone, labels, saved_name)
    - "NO CLIENTES*.csv"                       (leads de un bot tipo Chatea/ManyChat)
    - "BASE*.xlsx" con una hoja que contenga "POSIBLE" (lista para mensaje masivo)

Requiere: openpyxl.
"""
import glob, os, re, csv, sys, json
from datetime import datetime

from collections import defaultdict, Counter
try:
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    sys.exit("Falta la librería 'openpyxl'. Instálala con:  pip install openpyxl")

# ------------------------------------------------------------------ config
BASE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
OUT  = os.path.join(BASE, "Analisis")
SRC  = os.path.join(OUT, "_FUENTES")
os.makedirs(OUT, exist_ok=True)

HOY = datetime.now()
CFG = {"test_phones": [], "test_name_keywords": ["PRUEBA", "TEST"], "currency": "$",
       "gasto_publicidad": None, "negocio": ""}
_cfgp = os.path.join(BASE, "_config_dropi.json")
if os.path.exists(_cfgp):
    try: CFG.update(json.load(open(_cfgp, encoding="utf-8")))
    except Exception as e: print("Aviso: _config_dropi.json no se pudo leer:", e)
CUR = CFG.get("currency", "$")
NEGOCIO = str(CFG.get("negocio") or "").strip()
def titulo(base, cola):
    """'RESUMEN EJECUTIVO - <Negocio> - DROPI', o sin el tramo del negocio si no lo pusieron."""
    return f"{base} \u2014 {NEGOCIO} \u00b7 {cola}" if NEGOCIO else f"{base} \u00b7 {cola}"
TEST_PHONES = set(re.sub(r"\D", "", str(p))[-10:] for p in CFG.get("test_phones", []))
TEST_KW = [k.upper() for k in CFG.get("test_name_keywords", ["PRUEBA", "TEST"])]

# ------------------------------------------------------------------ helpers
def g(r, i): return r[i] if (i is not None and i < len(r)) else None
def up(x): return str(x).strip().upper() if x is not None else ""
def parse_date(v):
    if isinstance(v, datetime): return v
    if v is None: return None
    s = str(v).strip()
    for f in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try: return datetime.strptime(s[:10], f)
        except: pass
    return None
MONEY_ILEGIBLES = []   # celdas de dinero que no se pudieron leer: se cuentan, no se callan
def money(v):
    """Lee una celda de dinero. Cada rama de aqui nacio de un formato que daba una cifra
    FALSA sin avisar, que es el peor fallo posible en una skill cuyo producto son cifras:

      '8E+04'      Excel escribe asi al exportar     -> daba 804, no 80.000
      '(20.000)'   negativo contable                 -> daba +20.000, con el signo al reves
      '20,000.50'  formato US                        -> daba 20,0005, dividido por mil
      '20000.00'   decimales con punto               -> daba 2.000.000, multiplicado por cien

    Lo que no se puede leer se CUENTA en MONEY_ILEGIBLES y se declara al final de la corrida;
    nunca se convierte en un 0 silencioso, porque un 0 se lee como un dato."""
    if v is None: return 0.0
    if isinstance(v, (int, float)): return float(v)
    t = str(v).strip()
    if not t: return 0.0
    neg = False
    # negativo contable: (1.234) es -1234. Sin esto el signo se invertia en silencio.
    nucleo = t.replace(" ", "")
    if nucleo.startswith("(") and nucleo.endswith(")"):
        neg = True; t = nucleo[1:-1]
    # notacion cientifica: Excel exporta 8E+04 y hay que leerlo como 80000, no como 804
    cient = re.fullmatch(r"\s*-?\$?\s*(\d+(?:[.,]\d+)?[eE][+-]?\d+)\s*", t)
    if cient:
        try:
            r = float(cient.group(1).replace(",", "."))
            if t.lstrip().lstrip("$").lstrip().startswith("-"): r = -r
            return -r if neg else r
        except ValueError:
            MONEY_ILEGIBLES.append(t[:30]); return 0.0
    if t.lstrip().startswith("-"): neg = True
    s = re.sub(r"[^\d,\.]", "", t)
    if not s or s in (".", ","):
        MONEY_ILEGIBLES.append(t[:30]); return 0.0
    if "," in s and "." in s:
        # Estan los dos separadores: el que aparece MAS A LA DERECHA es el decimal.
        # Asi '74.900,50' (LatAm) y '20,000.50' (US) se leen bien los dos.
        dec = "," if s.rfind(",") > s.rfind(".") else "."
        mil = "." if dec == "," else ","
        s = s.replace(mil, "").replace(dec, ".")
    else:
        sep = "," if "," in s else ("." if "." in s else None)
        if sep:
            p = s.split(sep)
            # Un unico separador con 1 o 2 digitos detras es DECIMAL ('20000.00', '1500,25').
            # Con 3 digitos es separador de MILES, que es la convencion de Dropi en LatAm.
            s = (p[0] + "." + p[1]) if (len(p) == 2 and 1 <= len(p[1]) <= 2) else "".join(p)
    try:
        r = float(s)
    except ValueError:
        MONEY_ILEGIBLES.append(t[:30]); return 0.0
    return -r if neg else r
def _cantidad(v, arch=""):
    """CANTIDAD de una linea de producto. Sin dato se asume 1 (una linea es al menos una
    unidad); un 0 o un negativo NO se maquillan a 1 — se declaran y se respetan, porque
    'or 1' convertia en una unidad lo que el export decia que eran cero."""
    if v is None or str(v).strip() == "": return 1.0
    c = money(v)
    if c <= 0: CANT_RARA.append((str(v)[:12], arch))
    return c
def phone_key(v):
    d = re.sub(r"\D", "", str(v or ""))
    if len(d) > 10 and d.startswith("57"): d = d[2:]
    return d[-10:] if len(d) >= 10 else d
EXCLUIDOS = []      # lo descartado se CUENTA y se NOMBRA en la salida
_TEST_RX = [None]
def _test_rx():
    if _TEST_RX[0] is None:
        alt = "|".join(re.escape(k) for k in TEST_KW if k)
        # palabra COMPLETA: por subcadena, "MARIA TESTA" y "JUAN PROTESTA" salian de las
        # ventas y de la efectividad sin que nadie los contara.
        _TEST_RX[0] = re.compile(r"(?<![0-9A-ZÁÉÍÓÚÑ])(?:" + alt +
                                 r")(?![0-9A-ZÁÉÍÓÚÑ])") if alt else False
    return _TEST_RX[0]
def es_prueba(nombre, telefono=None):
    n = up(nombre); rx = _test_rx()
    if rx and n and rx.search(n):
        EXCLUIDOS.append((n[:40], phone_key(telefono), "nombre de prueba")); return True
    if telefono is not None and phone_key(telefono) in TEST_PHONES:
        EXCLUIDOS.append((n[:40], phone_key(telefono), "telefono de prueba")); return True
    return False
def sin_tilde(s):
    """Quita SOLO tildes de vocales y dieresis, para COMPARAR. La N con virgulilla se respeta:
    normalizar de mas rompe los valores sanos."""
    for a, b in (("Á","A"), ("É","E"), ("Í","I"), ("Ó","O"), ("Ú","U"), ("Ü","U")):
        s = s.replace(a, b)
    return s

def classify(estatus):
    """Clasifica el ESTATUS de Dropi en entregado / devolucion / cancelado / transito.

    El universo son decenas de estados y Dropi agrega mas con el tiempo, asi que se compara
    SIN TILDES y por subcadena, nunca por igualdad exacta: con igualdad, SINIESTRO y
    GUIA_ANULADA caian en transito y el porcentaje de entrega salia inflado, y REEXPEDICION
    acentuada no casaba con el patron sin tilde.
    Medido contra los 41 estados reales de 19.336 ordenes."""
    e = sin_tilde(up(estatus))
    if not e: return "transito"
    # ENTREGADO A TRANSPORTADORA es entrega al COURIER, no al cliente: la plata NO ha entrado.
    if "ENTREGADO A TRANSPORTADORA" in e: return "transito"
    if e == "ENTREGADO" or "ENTREGADO AL CLIENTE" in e: return "entregado"
    # perdida definitiva: la plata no vuelve
    if ("DEVOLUC" in e or "REEXPED" in e or "SINIESTRO" in e or "PERDID" in e
            or "EXTRAVI" in e): return "devolucion"
    # nunca llego a ruta -> fuera del denominador del % de entrega
    if "CANCELAD" in e or "RECHAZAD" in e or "ANULAD" in e: return "cancelado"
    # DECLARADO, pendiente de criterio del dueno: INDEMNIZADA / EN PROCESO DE INDEMNIZACION
    # quedan en transito (ni entregadas ni perdidas). No se cambia sin decision suya.
    return "transito"

def pipeline(estatus, clase):
    """Estado de FLUJO/caja: dónde está la plata de esta orden hoy."""
    if clase == "entregado": return "realizado"      # cobrado
    if clase == "devolucion": return "devuelto"       # perdido: un solo flete, el de devolución (COSTO DEVOLUCION FLETE)
    if clase == "cancelado": return "cancelado"       # nunca salió, no cuenta
    e = up(estatus)                                    # clase == transito
    if any(w in e for w in ("DEVOLUC", "REEXPED", "RECOGIDA FALLIDA")): return "en_camino_devol"
    return "en_camino"                                 # potencial, aún sin definir

def load_rows(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True); ws = wb[wb.sheetnames[0]]
    rows = [r for r in ws.iter_rows(values_only=True) if any(x is not None for x in r)]
    wb.close()
    if not rows: return [], {}
    h = [str(x).strip() if x else "" for x in rows[0]]
    return rows[1:], {c: i for i, c in enumerate(h)}

SALTADOS = []   # (archivo, motivo) — un export que desaparece sin avisar borra ventas enteras
SIN_ID  = []    # filas sin ID: NO se deduplican entre si, o se fundirian en una sola
CANT_RARA = []  # CANTIDAD 0 o negativa: se declara, no se maquilla
FECHA_RARA = [] # fechas ilegibles o futuras: una de 2099 entraba en el P&L sin avisar
def discover(base):
    """Devuelve dos listas de (path, cuenta). Clasifica por columnas, y APUNTA lo que salta."""
    peds, prods = [], []
    for root, dirs, fns in os.walk(base):
        b = os.path.basename(root)
        if b in ("Analisis", "_FUENTES", "__MACOSX"): dirs[:] = []; continue
        rel = os.path.relpath(root, base)
        cuenta = "General" if rel == "." else rel.split(os.sep)[0]
        for fn in sorted(fns):
            if fn.startswith("~$") or fn.startswith("_"): continue
            path = os.path.join(root, fn)
            if not fn.lower().endswith(".xlsx"):
                if fn.lower().endswith((".xls", ".csv")):
                    SALTADOS.append((os.path.join(cuenta, fn),
                        "formato " + fn.rsplit(".", 1)[-1].upper() + ": el motor solo lee .xlsx. "
                        "Vuelve a exportarlo, o ábrelo y guárdalo como .xlsx"))
                continue
            try:
                wb = openpyxl.load_workbook(path, read_only=True, data_only=True); ws = wb[wb.sheetnames[0]]
                head = [str(x).strip().upper() if x else "" for x in next(ws.iter_rows(values_only=True))]
                wb.close()
            except Exception as ex:
                SALTADOS.append((os.path.join(cuenta, fn), "no se pudo abrir: " + str(ex)[:60]))
                continue
            if "ESTATUS" not in head or "ID" not in head:   # no es export Dropi
                falta = [c for c in ("ESTATUS", "ID") if c not in head]
                SALTADOS.append((os.path.join(cuenta, fn),
                    "no parece export de Dropi: le faltan las columnas " + ", ".join(falta) +
                    ". Si Dropi renombró columnas, revisa references/esquema-dropi.md"))
                continue
            (prods if "PRODUCTO" in head else peds).append((path, cuenta))
    return peds, prods

def period_label(path, fecha_min):
    m = re.search(r"(\d{4})-(\d{2})", os.path.basename(path))
    if m: return m.group(0)
    return f"{fecha_min:%Y-%m}" if fecha_min else "0000-00"

# ------------------------------------------------------------------ carga
peds_f, prods_f = discover(BASE)
if not peds_f and not prods_f:
    print("No se encontraron exports de Dropi en:", BASE); sys.exit(1)

ped, prod = [], []
for path, acc in peds_f:
    rows, idx = load_rows(path)
    fmin = min((parse_date(g(r, idx.get("FECHA"))) for r in rows if parse_date(g(r, idx.get("FECHA")))), default=None)
    bl = period_label(path, fmin)
    for r in rows:
        if es_prueba(g(r, idx.get("NOMBRE CLIENTE")), g(r, idx.get("TELÉFONO"))): continue
        est = g(r, idx.get("ESTATUS"))
        _cl = classify(est)
        _oid = g(r, idx.get("ID")); _oid = str(_oid).strip() if _oid is not None else ""
        if not _oid or _oid.upper() == "NONE": SIN_ID.append(os.path.basename(path)); _oid = ""
        _f = parse_date(g(r, idx.get("FECHA"))); _fcruda = g(r, idx.get("FECHA"))
        if _f is None and _fcruda not in (None, ""):
            FECHA_RARA.append((str(_fcruda)[:14], "no se pudo leer", _oid or "sin ID"))
        elif _f is not None and _f.year > HOY.year + 1:
            FECHA_RARA.append((f"{_f:%d-%m-%Y}", "en el futuro", _oid or "sin ID"))
        ped.append(dict(cuenta=acc, bimestre=bl, oid=_oid,
            fecha=parse_date(g(r, idx.get("FECHA"))), estatus=up(est), clase=_cl,
            flujo=pipeline(est, _cl),
            trans=up(g(r, idx.get("TRANSPORTADORA"))) or "(SIN DATO)",
            depto=up(g(r, idx.get("DEPARTAMENTO DESTINO"))) or "(SIN DATO)",
            ciudad=up(g(r, idx.get("CIUDAD DESTINO"))) or "(SIN DATO)",
            ganancia=money(g(r, idx.get("GANANCIA"))), flete=money(g(r, idx.get("PRECIO FLETE"))),
            costo_dev=money(g(r, idx.get("COSTO DEVOLUCION FLETE"))),
            valor=money(g(r, idx.get("VALOR FACTURADO"))), novedad=up(g(r, idx.get("NOVEDAD"))),
            telefono=phone_key(g(r, idx.get("TELÉFONO")) or g(r, idx.get("TELEFONO"))),
            nombre=str(g(r, idx.get("NOMBRE CLIENTE")) or "").strip()))
for path, acc in prods_f:
    rows, idx = load_rows(path)
    fmin = min((parse_date(g(r, idx.get("FECHA"))) for r in rows if parse_date(g(r, idx.get("FECHA")))), default=None)
    bl = period_label(path, fmin)
    for r in rows:
        if es_prueba(g(r, idx.get("NOMBRE CLIENTE")), g(r, idx.get("TELÉFONO"))): continue
        est = g(r, idx.get("ESTATUS"))
        _oid = g(r, idx.get("ID")); _oid = str(_oid).strip() if _oid is not None else ""
        if not _oid or _oid.upper() == "NONE": SIN_ID.append(os.path.basename(path)); _oid = ""
        prod.append(dict(cuenta=acc, bimestre=bl, oid=_oid,
            fecha=parse_date(g(r, idx.get("FECHA"))), clase=classify(est),
            trans=up(g(r, idx.get("TRANSPORTADORA"))) or "(SIN DATO)",
            depto=up(g(r, idx.get("DEPARTAMENTO DESTINO"))) or "(SIN DATO)",
            ciudad=up(g(r, idx.get("CIUDAD DESTINO"))) or "(SIN DATO)",
            producto=(str(g(r, idx.get("PRODUCTO")) or "").strip() or "(SIN DATO)"),
            variacion=str(g(r, idx.get("VARIACION")) or "").strip(),
            sku=str(g(r, idx.get("SKU")) or "").strip(),
            cantidad=_cantidad(g(r, idx.get("CANTIDAD")), os.path.basename(path)),
            telefono=phone_key(g(r, idx.get("TELÉFONO"))),
            nombre=str(g(r, idx.get("NOMBRE CLIENTE")) or "").strip(),
            direccion=str(g(r, idx.get("DIRECCION")) or "").strip(),
            ganancia=money(g(r, idx.get("GANANCIA")))))

# ------------------------------------------------------------------ red de seguridad: duplicados
# Si el mismo export se descargó dos veces (o un mes aparece en dos archivos), la misma orden
# entraría doble y TODAS las cifras se inflarían en silencio. Se deduplica por ID de orden
# quedándose con la ÚLTIMA aparición (el archivo más reciente trae el estatus más actualizado)
# y se AVISA cuánto se unió, para que el usuario sepa que tenía archivos repetidos.
_antes = len(ped)
# Las filas SIN ID no se pueden deduplicar entre si: cada una lleva su propia clave. Antes
# todas compartian la cadena "None" y se fundian en una, borrando ventas reales en silencio.
_vistos = {}
for _i, _x in enumerate(ped):
    _k = (_x["cuenta"], _x["oid"]) if _x["oid"] else ("__sin_id__", _i)
    _vistos[_k] = _x
ped = list(_vistos.values())
if len(ped) < _antes:
    print(f"⚠️ Duplicados detectados: {_antes - len(ped)} órdenes con el mismo ID en la misma "
          f"cuenta, en los exports 'por pedido'. Me quedé con la ÚLTIMA que aparece al recorrer "
          f"los archivos por nombre — ojo, es orden de NOMBRE, no de fecha: si dos exports del "
          f"mismo periodo traen estados distintos para una orden, borra el viejo o renómbralo "
          f"para que el bueno quede de último.")
_antes = len(prod)
# En 'por producto' una orden trae una fila por producto: el ID se repite legítimamente.
# El duplicado real es la MISMA fila (cuenta + orden + producto) otra vez.
_vistosP = {}
for _i, _x in enumerate(prod):
    _k = ((_x["cuenta"], _x["oid"], _x["producto"], _x["variacion"], _x["sku"])
          if _x["oid"] else ("__sin_id__", _i))
    _vistosP[_k] = _x
prod = list(_vistosP.values())
if len(prod) < _antes:
    print(f"⚠️ Duplicados detectados: {_antes - len(prod)} filas con la misma orden, producto, "
          f"variación y SKU en los exports "
          f"'por producto'. Las uní — revisa si descargaste un archivo dos veces.")

# enriquecimiento WhatsApp (opcional)
wp_label = defaultdict(set); wp_name = {}
if os.path.isdir(SRC):
    for fp in glob.glob(os.path.join(SRC, "*.csv")):
        base_fn = os.path.basename(fp).upper()
        if not (base_fn.startswith("ETIQUETA") or base_fn.startswith("CONTACTO")): continue
        with open(fp, encoding="utf-8", errors="replace") as f:
            for row in csv.DictReader(f):
                k = phone_key(row.get("phone"))
                if not k: continue
                lab = (row.get("labels") or "").strip()
                if lab:
                    for l in lab.split(","): wp_label[k].add(l.strip())
                nm = (row.get("saved_name") or row.get("public_name") or "").strip()
                if nm and k not in wp_name: wp_name[k] = nm

# ============================ INVENTARIO DE LA CORRIDA ============================
# Un informe vale por su denominador. Aqui se declara QUE se leyo, QUE se salto y QUE se
# excluyo: un export que desaparece en silencio borra ventas enteras sin dar ningun error.
print("\n" + "=" * 68)
print("INVENTARIO DE LA CORRIDA")
print("=" * 68)
print(f"Archivos LEÍDOS: {len(peds_f) + len(prods_f)}  "
      f"({len(peds_f)} por pedido, {len(prods_f)} por producto)")
for _p, _c in peds_f:  print(f"   [por pedido ] {_c}/{os.path.basename(_p)}")
for _p, _c in prods_f: print(f"   [por producto] {_c}/{os.path.basename(_p)}")
if SALTADOS:
    print(f"\n\u26a0\ufe0f  Archivos SALTADOS: {len(SALTADOS)} (no entraron en NINGUNA cifra)")
    for _f, _m in SALTADOS: print(f"   - {_f}: {_m}")
else:
    print("Archivos saltados: 0")
_EXCL_U = sorted(set(EXCLUIDOS))   # el mismo export bajado dos veces doblaba este conteo
if _EXCL_U:
    print(f"\n\u26a0\ufe0f  Registros EXCLUIDOS por ser prueba: {len(_EXCL_U)}")
    for _n, _t, _m in _EXCL_U[:20]: print(f"   - {_n} ({_t}) por {_m}")
    if len(_EXCL_U) > 20: print(f"   ... y {len(_EXCL_U) - 20} mas")
    print("   Si alguno es un CLIENTE REAL, quita esa palabra de 'test_name_keywords'.")
else:
    print("Registros excluidos por prueba: 0")
if SIN_ID:
    from collections import Counter as _C0
    print(f"\n\u26a0\ufe0f  Filas SIN columna ID: {len(SIN_ID)}. Se conservan todas (no se pueden "
          f"deduplicar entre sí), pero revisa el export: una orden sin ID no se puede cruzar "
          f"con Dropi.")
    for _f, _n in _C0(SIN_ID).most_common(5): print(f"   - {_f}: {_n} fila(s)")
if FECHA_RARA:
    print(f"\n\u26a0\ufe0f  Fechas sospechosas: {len(FECHA_RARA)}. Una fecha futura entra igual en "
          f"el periodo y en el P&L, asi que revisa el export antes de creerle al resumen.")
    for _v, _m, _o in FECHA_RARA[:10]: print(f"   - {_v} ({_m}) en la orden {_o}")
    if len(FECHA_RARA) > 10: print(f"   ... y {len(FECHA_RARA) - 10} mas")
if CANT_RARA:
    from collections import Counter as _C1
    print(f"\n\u26a0\ufe0f  CANTIDAD en cero o negativa: {len(CANT_RARA)} linea(s). Se respetan tal "
          f"cual (no se maquillan a 1), pero las unidades por producto las reflejan.")
    for (_v, _a), _n in _C1(CANT_RARA).most_common(5): print(f"   - {_v!r} en {_a}: {_n} vez/veces")
if MONEY_ILEGIBLES:
    from collections import Counter as _C
    print(f"\n\u26a0\ufe0f  Celdas de dinero ILEGIBLES: {len(MONEY_ILEGIBLES)} (contadas como 0)")
    for _v, _n in _C(MONEY_ILEGIBLES).most_common(10): print(f"   - {_v!r} x{_n}")

print(f"\nCargado: {len(ped)} filas pedido | {len(prod)} filas producto | "
      f"{len(wp_label)} tel con etiqueta WP")
if not prod:
    print("\n\u26a0\ufe0f  NO se cargó ningún informe POR PRODUCTO. La base de clientes y la hoja "
          "POR PRODUCTO salen SOLO de ese archivo: MAESTRO_CONTACTOS va a quedar con 0 clientes, "
          "y ese 0 significa 'no se pudo medir', no 'no tienes clientes'. Descarga el export "
          "'por producto' del mismo corte y vuelve a correr el motor.")
if not ped:
    print("\n\u26a0\ufe0f  NO se cargó ningún informe POR PEDIDO. El dinero, el P&L y el veredicto de "
          "rentabilidad salen de ese archivo: sin él, todas esas cifras serían $0 y el veredicto "
          "sería falso. Se generan las hojas que sí tienen respaldo y el P&L queda SIN VEREDICTO.")
cuentas = sorted(set(x["cuenta"] for x in ped) | set(x["cuenta"] for x in prod))
if len(cuentas) > 1:
    print(f"\n\u26a0\ufe0f  Hay {len(cuentas)} cuentas: {', '.join(cuentas)}. El bloque GLOBAL las SUMA.")
    print("   Eso solo vale si son cuentas del MISMO negocio. Empresas distintas no se suman "
          "jamás: si lo son, corre el motor una vez por carpeta y lee solo su bloque de cuenta.")

# ---------------------- ORDENES FANTASMA (candidatas, NO veredicto) ----------------------
# Al EDITAR una orden, Dropi le cambia el ID: la vieja desaparece de su panel pero sobrevive
# en cualquier export bajado antes, y la MISMA venta se cuenta dos veces. El dedup por ID no
# la ve, porque los dos IDs son distintos. La huella es (telefono, mismo monto, pocos dias).
# 🔴 CANDIDATA NO ES FANTASMA: un cliente puede pedir dos veces de verdad. La unica autoridad
# es el DETALLE de la API de Dropi, que esta skill NO consulta. Por eso se AVISA y NO se borra:
# declarar fantasmas a ciegas ya produjo una tanda entera de falsos positivos.
FANTASMA_DIAS = 7
_term = ("entregado", "devolucion", "cancelado")
_pares = defaultdict(list)
for x in ped:
    if x["telefono"] and x["valor"] > 0: _pares[(x["telefono"], round(x["valor"]))].append(x)
CAND = []
for _k, _g in _pares.items():
    if len(_g) < 2: continue
    _g = sorted([y for y in _g if y["fecha"]], key=lambda y: y["fecha"])
    for _a, _b in zip(_g, _g[1:]):
        if (_b["fecha"] - _a["fecha"]).days <= FANTASMA_DIAS and _a["clase"] not in _term:
            CAND.append((_a, _b))
if CAND:
    print(f"\n\u26a0\ufe0f  Posibles ÓRDENES FANTASMA: {len(CAND)} par(es) con el mismo teléfono y el "
          f"mismo monto en <= {FANTASMA_DIAS} días, con la más vieja aún sin cerrar.")
    for _a, _b in CAND[:15]:
        print((f"   - tel {_a['telefono']} {CUR}" + f"{_a['valor']:,.0f}".replace(",", ".") +
               f": id {_a['oid']} ({_a['estatus']}, {_a['fecha']:%d-%m-%Y}) vs "
               f"id {_b['oid']} ({_b['estatus']}, {_b['fecha']:%d-%m-%Y})"))
    if len(CAND) > 15: print(f"   ... y {len(CAND) - 15} mas")
    print("   NO se descontaron de ninguna cifra: puede ser un cliente que pidió dos veces.")
    print("   Para confirmar hay que mirar el detalle de cada orden en Dropi; la que ya no exista")
    print("   ahí es fantasma y esa venta está contada dos veces.")
else:
    print("\nPosibles órdenes fantasma: 0 par(es) con esa huella")
# ------------------------- LO QUE QUEDO FUERA, EN UN SOLO SITIO -------------------------
# Se arma aqui una vez y lo reutilizan la hoja COBERTURA y el PDF. Antes cada aviso vivia
# suelto en un print y el entregable —que es lo unico que sobrevive— no llevaba ninguno.
AVISOS = []
if len(cuentas) > 1:
    AVISOS.append(("Varias cuentas sumadas en el bloque GLOBAL",
        "El GLOBAL suma " + ", ".join(cuentas) + ". Eso solo vale si son cuentas del MISMO "
        "negocio. Si son empresas distintas, sus ventas no se suman jamás: corre el motor una "
        "vez por carpeta y lee solo el bloque de cada cuenta."))
if SALTADOS:
    AVISOS.append((f"{len(SALTADOS)} archivo(s) no se pudieron leer",
        "No entraron en ninguna cifra: " + "; ".join(f for f, _m in SALTADOS[:4]) +
        ("; y más" if len(SALTADOS) > 4 else "") + ". Resuélvelos y vuelve a correr."))
if _EXCL_U:
    AVISOS.append((f"{len(_EXCL_U)} registro(s) excluidos por parecer prueba",
        "Si alguno es un cliente real, quita esa palabra de test_name_keywords: " +
        "; ".join(f"{n} ({t})" for n, t, _m in _EXCL_U[:4]) +
        ("; y más" if len(_EXCL_U) > 4 else "") + "."))
if CAND:
    AVISOS.append((f"{len(CAND)} posible(s) orden(es) fantasma",
        "Mismo teléfono y mismo monto con pocos días entre medias, la huella de una orden "
        "editada en Dropi. NO se descontaron de estas cifras, porque un cliente puede pedir dos "
        "veces de verdad: están en la hoja POSIBLES FANTASMA para confirmarlas una a una."))
if SIN_ID:
    AVISOS.append((f"{len(SIN_ID)} fila(s) sin columna ID",
        "Se conservan todas, pero una orden sin ID no se puede cruzar con Dropi ni deduplicar."))
if FECHA_RARA:
    AVISOS.append((f"{len(FECHA_RARA)} fecha(s) sospechosa(s)",
        "Ilegibles o en el futuro. Una fecha futura entra igual en el periodo y en el P&L: " +
        "; ".join(f"{v} ({m})" for v, m, _o in FECHA_RARA[:4]) + "."))
if CANT_RARA:
    AVISOS.append((f"{len(CANT_RARA)} línea(s) con CANTIDAD cero o negativa",
        "Se respetan tal cual en las unidades por producto, no se maquillan a 1."))
if MONEY_ILEGIBLES:
    AVISOS.append((f"{len(MONEY_ILEGIBLES)} celda(s) de dinero ilegibles",
        "Contadas como 0, así que el dinero de esas filas NO está en el P&L: " +
        "; ".join(repr(v) for v in MONEY_ILEGIBLES[:5]) + "."))
if not prod:
    AVISOS.append(("No se leyó ningún informe POR PRODUCTO",
        "La base de clientes sale solo de ahí: el 0 de MAESTRO_CONTACTOS significa 'no se pudo "
        "medir', no 'no tienes clientes'."))
if not ped:
    AVISOS.append(("No se leyó ningún informe POR PEDIDO",
        "Es de donde sale el dinero: por eso no hay veredicto de rentabilidad."))
print("=" * 68 + "\n")

# ------------------------------------------------------------------ estilos
HDR = Font(bold=True, color="FFFFFF", size=10); HDRF = PatternFill("solid", fgColor="1F2A44")
TIT = Font(bold=True, size=14, color="1F2A44"); SUB = Font(bold=True, size=11, color="B8860B")
thin = Side(style="thin", color="DDDDDD"); BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c); cell.font = HDR; cell.fill = HDRF
        cell.alignment = Alignment(horizontal="center", vertical="center"); cell.border = BORD
def pct(x): return f"{x*100:.1f}%"
def pct_c(x, cerradas):
    """Porcentaje de entrega. Sin ninguna orden cerrada NO es 0%: es que aun no se sabe.
    Un 0,0% sereno en el resumen se lee como 'no entregas nada', que es falso."""
    return f"{x*100:.1f}%" if cerradas else "s/d (nada cerrado aún)"
def cop(v): return f"{CUR}" + f"{v:,.0f}".replace(",", ".")  # separador de miles con punto (Colombia)
def eff(counter):
    ent = counter["entregado"]; dev = counter["devolucion"]; act = ent + dev
    return ent, dev, act, (ent / act if act else 0.0)
def agg_status(records, keyfn):
    d = defaultdict(Counter); extra = defaultdict(lambda: defaultdict(float))
    for x in records:
        k = keyfn(x); d[k][x["clase"]] += 1
        for f in ("ganancia", "flete", "costo_dev", "valor"): extra[k][f] += x.get(f, 0)
    return d, extra

# ================================================================ LOGÍSTICA
wbL = Workbook(); wbL.remove(wbL.active)
ws = wbL.create_sheet("RESUMEN")
ws["B2"] = "MAESTRO LOGÍSTICA — DROPI"; ws["B2"].font = TIT
fechas = [x["fecha"] for x in ped if x["fecha"]]
ws["B3"] = (f"Periodo: {min(fechas):%b-%Y} a {max(fechas):%b-%Y}  |  Cuentas: {', '.join(cuentas)}"
            if fechas else "Periodo: s/d")
ws["B3"].font = Font(italic=True, color="666666")
scopes = [("GLOBAL", ped)] + [(f"Cuenta {c}", [x for x in ped if x["cuenta"] == c]) for c in cuentas] \
         if len(cuentas) > 1 else [("GLOBAL", ped)]
r = 5
for scope, recs in scopes:
    c = Counter(x["clase"] for x in recs); ent, dev, act, e = eff(c)
    # Solo lo ENTREGADO esta cobrado. Antes esta linea sumaba la ganancia de todas las ordenes,
    # incluidas las que van en ruta, y la llamaba "neta acumulada": la hoja de al lado decia $0
    # de ganancia realizada para los mismos datos. Dos cifras contradictorias en un mismo archivo.
    gan = sum(x["ganancia"] for x in recs if x["clase"] == "entregado")
    cdev = sum(x["costo_dev"] for x in recs)
    ws.cell(r, 2, scope).font = SUB; r += 1
    for lab, val in [("Órdenes totales", len(recs)), ("Activas (entreg+devol)", act),
                     ("Entregadas", ent), ("Devoluciones", dev),
                     ("Canceladas/Rechazadas", c["cancelado"]), ("En tránsito", c["transito"]),
                     ("% ENTREGA", pct_c(e, act)), ("Ganancia cobrada (solo entregadas)", cop(gan)),
                     ("Costo devoluciones (flete)", cop(cdev))]:
        ws.cell(r, 2, lab); ws.cell(r, 4, val)
        if lab == "% ENTREGA":
            ws.cell(r, 2).font = Font(bold=True); ws.cell(r, 4).font = Font(bold=True, size=12, color="B8860B")
        r += 1
    r += 1
ws.column_dimensions["B"].width = 32; ws.column_dimensions["D"].width = 22

ws = wbL.create_sheet("EVOLUCIÓN")
ws["A1"] = "EVOLUCIÓN POR PERIODO (cronológico)"; ws["A1"].font = TIT
ws.append([]); hd = ["Periodo", "Cuenta", "Órdenes", "Activas", "Entregadas", "Devol.", "% Entrega", "Ganancia cobrada"]
ws.append(hd); style_header(ws, 3, len(hd))
by = defaultdict(list)
for x in ped: by[(x["bimestre"], x["cuenta"])].append(x)
for k in sorted(by):
    recs = by[k]; c = Counter(x["clase"] for x in recs); ent, dev, act, e = eff(c)
    ws.append([k[0], k[1], len(recs), act, ent, dev, pct_c(e, act),
               round(sum(x["ganancia"] for x in recs if x["clase"] == "entregado"))])
for col, w in zip("ABCDEFGH", [12, 12, 10, 10, 11, 9, 11, 16]): ws.column_dimensions[col].width = w

dP, _ = agg_status(prod, lambda x: x["producto"])
unitsP = defaultdict(float)
for x in prod: unitsP[x["producto"]] += x["cantidad"]
ws = wbL.create_sheet("POR PRODUCTO")
ws["A1"] = "DESEMPEÑO POR PRODUCTO"; ws["A1"].font = TIT
ws.append([]); hd = ["Producto", "Líneas activas", "Entregadas", "Devol.", "% Entrega", "Unidades"]
ws.append(hd); style_header(ws, 3, len(hd))
for prd, c in sorted(dP.items(), key=lambda kv: -(kv[1]["entregado"] + kv[1]["devolucion"])):
    ent, dev, act, e = eff(c)
    if act == 0 and unitsP[prd] == 0: continue
    ws.append([prd[:55], act, ent, dev, pct_c(e, act), round(unitsP[prd])])
ws.column_dimensions["A"].width = 50
for col in "BCDEF": ws.column_dimensions[col].width = 13

dT, eT = agg_status(ped, lambda x: x["trans"])
ws = wbL.create_sheet("POR TRANSPORTADORA")
ws["A1"] = "DESEMPEÑO POR TRANSPORTADORA"; ws["A1"].font = TIT
ws.append([]); hd = ["Transportadora", "Activas", "Entregadas", "Devol.", "% Entrega", "% Devol.", "Costo devol.", "Muestra"]
ws.append(hd); style_header(ws, 3, len(hd))
for t, c in sorted(dT.items(), key=lambda kv: -(kv[1]["entregado"] + kv[1]["devolucion"])):
    ent, dev, act, e = eff(c)
    ws.append([t, act, ent, dev, pct_c(e, act), pct_c(dev / act if act else 0, act),
               round(eT[t]["costo_dev"]),
               "sin cerrar" if act == 0 else ("dato flaco" if act < 5 else "")])
ws.column_dimensions["A"].width = 22
for col in "BCDEFG": ws.column_dimensions[col].width = 13

dD, _ = agg_status(ped, lambda x: x["depto"])
ws = wbL.create_sheet("POR DEPARTAMENTO")
ws["A1"] = "DESEMPEÑO POR DEPARTAMENTO"; ws["A1"].font = TIT
ws.append([]); hd = ["Departamento", "Activas", "Entregadas", "Devol.", "% Entrega", "% Devol.", "Muestra"]
ws.append(hd); style_header(ws, 3, len(hd))
for d, c in sorted(dD.items(), key=lambda kv: -(kv[1]["entregado"] + kv[1]["devolucion"])):
    ent, dev, act, e = eff(c)
    ws.append([d, act, ent, dev, pct_c(e, act), pct_c(dev / act if act else 0, act),
               "sin cerrar" if act == 0 else ("dato flaco" if act < 3 else "")])
ws.column_dimensions["A"].width = 24
for col in "BCDEF": ws.column_dimensions[col].width = 13

ct = defaultdict(Counter)
for x in ped: ct[(x["ciudad"], x["trans"])][x["clase"]] += 1
city_best = {}; city_tot = Counter()
for (city, tr), c in ct.items():
    ent, dev, act, e = eff(c); city_tot[city] += act
    if act >= 1 and (city not in city_best or e > city_best[city][2]
                     or (e == city_best[city][2] and act > city_best[city][1])):
        city_best[city] = (tr, act, e)
ws = wbL.create_sheet("MEJOR TRANSP x CIUDAD")
ws["A1"] = "MEJOR TRANSPORTADORA POR CIUDAD (sin umbral: la muestra se muestra)"; ws["A1"].font = TIT
ws.append([]); hd = ["Ciudad", "Total órdenes", "Mejor transportadora", "Órdenes", "% Entrega", "Recomendación", "Muestra"]
ws.append(hd); style_header(ws, 3, len(hd))
def reco(e, cerradas=1):
    if not cerradas: return "sin datos todavía (nada cerrado)"
    if e >= 0.85: return "EXCELENTE — enviar sin dudar"
    if e >= 0.70: return "BUENA — usar"
    if e >= 0.55: return "REGULAR — vigilar"
    return "MALA — evitar / solo anticipado"
for city in sorted(city_best, key=lambda c: -city_tot[c]):
    tr, act, e = city_best[city]
    ws.append([city, city_tot[city], tr, act, pct_c(e, act), reco(e, act),
               "sin cerrar" if act == 0 else ("dato flaco" if act < 4 else "")])
ws.column_dimensions["A"].width = 24; ws.column_dimensions["C"].width = 20; ws.column_dimensions["F"].width = 30
for col in "BDE": ws.column_dimensions[col].width = 13

nov = Counter(x["novedad"] for x in ped if x["novedad"] and x["novedad"] != "NONE")
totnov = sum(nov.values())
ws = wbL.create_sheet("NOVEDADES")
ws["A1"] = "PRINCIPALES NOVEDADES (causas de no-entrega)"; ws["A1"].font = TIT
ws.append([]); hd = ["Novedad", "Casos", "% del total"]; ws.append(hd); style_header(ws, 3, len(hd))
for n, c in nov.most_common(30):
    ws.append([n[:60], c, pct(c / totnov if totnov else 0)])
ws.column_dimensions["A"].width = 55; ws.column_dimensions["B"].width = 10; ws.column_dimensions["C"].width = 12

# ---- RESUMEN EJECUTIVO / RENTABILIDAD (primera hoja + insumo del PDF) ----
def suma(campo, filtro): return sum(x.get(campo, 0) for x in ped if filtro(x))
gan_realizada = suma("ganancia", lambda x: x["flujo"] == "realizado")
gan_en_camino = suma("ganancia", lambda x: x["flujo"] in ("en_camino", "en_camino_devol"))
if gan_en_camino <= 0:   # Dropi solo contabiliza ganancia al entregar; estimar en-camino con el promedio entregado
    _nreal = sum(1 for x in ped if x["flujo"] == "realizado")
    _avg = (gan_realizada / _nreal) if _nreal else 0
    gan_en_camino = _avg * sum(1 for x in ped if x["flujo"] in ("en_camino", "en_camino_devol"))
costo_dev     = suma("costo_dev", lambda x: x["flujo"] in ("devuelto", "en_camino_devol"))
util_dropi    = gan_realizada - costo_dev
n_flujo = Counter(x["flujo"] for x in ped)
gasto_pub = CFG.get("gasto_publicidad")
try: gasto_pub = float(gasto_pub) if gasto_pub not in (None, "") else None
except: gasto_pub = None
util_final = (util_dropi - gasto_pub) if gasto_pub is not None else None
_cerradas = n_flujo["realizado"] + n_flujo["devuelto"]
if not ped:
    # Sin el informe por pedido no hay dinero que analizar: un "NO RENTABLE" aqui seria falso.
    veredicto, color = "SIN VEREDICTO: FALTA EL INFORME POR PEDIDO", "B8860B"
    util_final = None
elif _cerradas == 0:
    # Todas las ordenes siguen en ruta: no hay ni una venta cobrada ni una perdida. Dictaminar
    # NO RENTABLE aqui es tratar "no se sabe" como "cero" y decirle al dueno que pierde plata
    # cuando su resultado aun no existe.
    veredicto, color = "SIN VEREDICTO: NINGUNA ORDEN CERRADA TODAVÍA", "B8860B"
    util_final = None
elif util_final is None:    veredicto, color = "FALTA GASTO DE PUBLICIDAD PARA EL VEREDICTO", "B8860B"
elif util_final > 0:        veredicto, color = "RENTABLE", "1E7A34"
else:                       veredicto, color = "NO RENTABLE", "B00020"

wsE = wbL.create_sheet("RESUMEN EJECUTIVO", 0)
wsE["B2"] = titulo("RESUMEN EJECUTIVO", "DROPI"); wsE["B2"].font = Font(bold=True, size=16, color="1F2A44")
wsE["B3"] = (f"Periodo: {min(fechas):%d-%b-%Y} a {max(fechas):%d-%b-%Y}" if fechas else "Periodo: s/d")
wsE["B3"].font = Font(italic=True, color="666666")
def _row(ws, r, lab, val, bold=False, col="000000", size=11):
    ws.cell(r, 2, lab).font = Font(bold=bold, size=size)
    c = ws.cell(r, 4, val); c.font = Font(bold=bold, size=size, color=col)
    c.alignment = Alignment(horizontal="right")
r = 5
wsE.cell(r, 2, "ESTADO DE TUS ÓRDENES (dónde está la plata hoy)").font = SUB; r += 1
_row(wsE, r, "✅ Entregadas (cobradas)", n_flujo["realizado"]); r += 1
_row(wsE, r, "🚚 En camino (aún sin definir)", n_flujo["en_camino"]); r += 1
_row(wsE, r, "⚠️ En camino a devolución", n_flujo["en_camino_devol"]); r += 1
_row(wsE, r, "❌ Devueltas (perdidas)", n_flujo["devuelto"]); r += 1
_row(wsE, r, "🚫 Canceladas/Rechazadas (no cuentan)", n_flujo["cancelado"]); r += 2
wsE.cell(r, 2, "RENTABILIDAD").font = SUB; r += 1
_row(wsE, r, "Ganancia realizada (de lo entregado)", cop(gan_realizada), bold=True, col="1E7A34"); r += 1
_row(wsE, r, "(−) Costo de devoluciones (flete)", f"-{cop(costo_dev)}", col="B00020"); r += 1
_row(wsE, r, "(=) Utilidad Dropi (antes de publicidad)", cop(util_dropi), bold=True); r += 1
_row(wsE, r, "(−) Gasto de publicidad (Meta)",
     f"-{cop(gasto_pub)}" if gasto_pub is not None else "← FALTA (ponlo en _config_dropi.json o pásalo)",
     col="B00020"); r += 1
_row(wsE, r, "(=) UTILIDAD NETA FINAL",
     cop(util_final) if util_final is not None else "—", bold=True, size=13,
     col=("1E7A34" if (util_final or 0) > 0 else "B00020")); r += 1
_row(wsE, r, "Ganancia potencial en camino (estimada)",
     cop(gan_en_camino) if gan_en_camino else "no estimable (aun no hay entregas)",
     col="666666"); r += 2
wsE.cell(r, 2, "VEREDICTO").font = Font(bold=True, size=12)
vc = wsE.cell(r, 4, veredicto); vc.font = Font(bold=True, size=13, color=color); vc.alignment = Alignment(horizontal="right")
wsE.column_dimensions["B"].width = 42; wsE.column_dimensions["D"].width = 34

wsC0 = wbL.create_sheet("COBERTURA")
wsC0["A1"] = "QUÉ QUEDÓ FUERA DE ESTAS CIFRAS"; wsC0["A1"].font = TIT
wsC0["A2"] = ("Un informe vale por su denominador. Aquí está todo lo que no entró en las cifras "
              "de este archivo, o entró con una salvedad.")
wsC0["A2"].font = Font(italic=True, color="666666")
wsC0.append([]); _hdC = ["Qué", "Qué significa y qué hacer"]
wsC0.append(_hdC); style_header(wsC0, 4, len(_hdC))
if AVISOS:
    for _t, _d in AVISOS: wsC0.append([_t, _d])
else:
    wsC0.append(["Sin salvedades", "Todos los archivos se leyeron, no se excluyó ningún "
                 "registro y no se detectaron órdenes fantasma ni celdas ilegibles."])
wsC0.column_dimensions["A"].width = 46; wsC0.column_dimensions["B"].width = 104
for _r in range(5, wsC0.max_row + 1):
    wsC0.cell(_r, 1).alignment = Alignment(vertical="top", wrap_text=True)
    wsC0.cell(_r, 2).alignment = Alignment(vertical="top", wrap_text=True)

if CAND:
    wsF = wbL.create_sheet("POSIBLES FANTASMA")
    wsF["A1"] = "POSIBLES ÓRDENES FANTASMA (candidatas: NO se descontaron de las cifras)"
    wsF["A1"].font = TIT
    wsF["A2"] = ("Al editar una orden, Dropi le cambia el ID y la vieja sigue contando en los "
                 "exports bajados antes. Huella: mismo teléfono, mismo monto, pocos días y la "
                 "vieja sin cerrar. Un cliente puede pedir dos veces de verdad: confirma cada "
                 "una en el detalle de Dropi antes de descontarla.")
    wsF["A2"].font = Font(italic=True, color="666666")
    wsF.append([]); _hd = ["Teléfono", "Monto", "ID vieja", "Estado vieja", "Fecha vieja",
                           "ID nueva", "Estado nueva", "Fecha nueva", "Dias"]
    wsF.append(_hd); style_header(wsF, 4, len(_hd))
    for _a, _b in CAND:
        wsF.append([_a["telefono"], round(_a["valor"]), _a["oid"], _a["estatus"],
                    f"{_a['fecha']:%Y-%m-%d}", _b["oid"], _b["estatus"],
                    f"{_b['fecha']:%Y-%m-%d}", (_b["fecha"] - _a["fecha"]).days])
    for _c, _w in zip("ABCDEFGHI", [14, 14, 12, 26, 13, 12, 26, 13, 7]):
        wsF.column_dimensions[_c].width = _w

pathL = os.path.join(OUT, "MAESTRO_LOGISTICA.xlsx"); wbL.save(pathL)
print("OK ->", pathL)

# ---- DOCUMENTO PDF: Resumen Ejecutivo de Rentabilidad ----
pdf_ok = False
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                    KeepTogether)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    pathPDF = os.path.join(OUT, "RESUMEN_EJECUTIVO.pdf")
    doc = SimpleDocTemplate(pathPDF, pagesize=letter, topMargin=1.6*cm, bottomMargin=1.4*cm,
                            leftMargin=1.8*cm, rightMargin=1.8*cm)
    ss = getSampleStyleSheet()
    H = ParagraphStyle("H", parent=ss["Title"], fontSize=19, textColor=colors.HexColor("#1F2A44"), spaceAfter=2)
    Sb = ParagraphStyle("Sb", parent=ss["Normal"], fontSize=9.5, textColor=colors.HexColor("#666666"))
    Se = ParagraphStyle("Se", parent=ss["Heading2"], fontSize=12.5, textColor=colors.HexColor("#B8860B"), spaceBefore=12, spaceAfter=4)
    P = ParagraphStyle("P", parent=ss["Normal"], fontSize=10.3, leading=15)
    money_ = cop
    el = [Paragraph(titulo("Resumen Ejecutivo", "Dropi"), H),
          Paragraph((f"Periodo {min(fechas):%d-%b-%Y} a {max(fechas):%d-%b-%Y}  ·  "
                     f"Cuentas: {', '.join(cuentas)}  ·  Generado por golden-dropi-analisis") if fechas else "", Sb),
          Spacer(1, 8)]
    # Veredicto banner
    vb = Table([[veredicto]], colWidths=[17.4*cm])
    vb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#"+color)),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),("FONTSIZE",(0,0),(-1,-1),15),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    el += [vb, Spacer(1, 10)]
    tot = len(ped) or 1  # si solo hay export "por producto", ped=[]: evita ZeroDivision en los %
    est = [["Estado de las órdenes", "Cantidad", "% del total"],
           ["Entregadas (cobradas)", n_flujo["realizado"], f"{n_flujo['realizado']/tot*100:.1f}%"],
           ["En camino (sin definir)", n_flujo["en_camino"], f"{n_flujo['en_camino']/tot*100:.1f}%"],
           ["En camino a devolución", n_flujo["en_camino_devol"], f"{n_flujo['en_camino_devol']/tot*100:.1f}%"],
           ["Devueltas (perdidas)", n_flujo["devuelto"], f"{n_flujo['devuelto']/tot*100:.1f}%"],
           ["Canceladas/Rechazadas", n_flujo["cancelado"], f"{n_flujo['cancelado']/tot*100:.1f}%"]]
    t1 = Table(est, colWidths=[9*cm, 4.2*cm, 4.2*cm])
    t1.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F2A44")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9.5),("ALIGN",(1,0),(-1,-1),"RIGHT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F5F5F5")]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#DDDDDD")),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    el += [Paragraph("Dónde está tu plata hoy", Se), t1]
    pl = [["Rentabilidad", ""],
          ["Ganancia realizada (entregado)", money_(gan_realizada)],
          ["(−) Costo de devoluciones (flete)", "-"+money_(costo_dev)],
          ["(=) Utilidad Dropi (antes de publicidad)", money_(util_dropi)],
          ["(−) Gasto de publicidad (Meta)", ("-"+money_(gasto_pub)) if gasto_pub is not None else "FALTA"],
          ["(=) UTILIDAD NETA FINAL", money_(util_final) if util_final is not None else "—"],
          ["Ganancia potencial en camino (est.)",
           money_(gan_en_camino) if gan_en_camino else "no estimable"]]
    t2 = Table(pl, colWidths=[12*cm, 5.4*cm])
    t2.setStyle(TableStyle([("SPAN",(0,0),(1,0)),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#B8860B")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,3),(-1,3),"Helvetica-Bold"),("FONTNAME",(0,5),(-1,5),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),10),("FONTSIZE",(0,5),(-1,5),12),("ALIGN",(1,0),(1,-1),"RIGHT"),
        ("TEXTCOLOR",(1,1),(1,1),colors.HexColor("#1E7A34")),("TEXTCOLOR",(1,2),(1,2),colors.HexColor("#B00020")),
        ("TEXTCOLOR",(1,4),(1,4),colors.HexColor("#B00020")),
        ("TEXTCOLOR",(1,5),(1,5),colors.HexColor("#1E7A34") if (util_final or 0)>0 else colors.HexColor("#B00020")),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#DDDDDD")),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    el += [Paragraph("Rentabilidad", Se), t2]
    if gasto_pub is None:
        el += [Spacer(1,6), Paragraph("<b>Para cerrar el veredicto falta tu gasto de publicidad</b> del periodo "
            "(Meta). Ponlo en <font face='Courier'>_config_dropi.json</font> (clave "
            "<font face='Courier'>gasto_publicidad</font>) o pásalo, y el neto y el veredicto se calculan solos.", P)]
    cg = Counter(x["clase"] for x in ped); ent, dev, act, ef = eff(cg)
    el += [Paragraph("Contexto de entregas", Se),
           Paragraph((f"Efectividad de entrega: <b>{ef*100:.1f}%</b> ({ent:,} entregadas de "
                      f"{act:,} cerradas). " if act else
                      "Todavía no hay ninguna orden cerrada, así que aún no se puede medir la "
                      "efectividad de entrega. ") +
                     "El detalle por producto, transportadora, ciudad y las novedades está en "
                     "<b>MAESTRO_LOGISTICA.xlsx</b>; la base de clientes en "
                     "<b>MAESTRO_CONTACTOS.xlsx</b>.", P)]

    # Cobertura: un informe vale por su denominador. Lo que no entro se dice aqui, no se calla.
    _av = [f"<b>{_t}.</b> {_d}" for _t, _d in AVISOS]
    if _av:
        # KeepTogether: el bloque entero pasa de pagina junto, en vez de dejar una linea viuda.
        el += [KeepTogether([Paragraph("Qué quedó fuera de estas cifras", Se)] +
                            [Paragraph("\u00b7 " + _a, P) for _a in _av])]

    doc.build(el)
    print("OK ->", pathPDF); pdf_ok = True
except ImportError:
    print("Aviso: sin 'reportlab' no se generó el PDF (pip install reportlab). El RESUMEN EJECUTIVO está en el Excel.")

# ================================================================ CONTACTOS
cli = defaultdict(lambda: dict(nombre="", depto="", ciudad="", direccion="", prods=set(),
                               cuentas=set(), ordenes={}, fmin=None, fmax=None))
for x in prod:
    k = x["telefono"]
    if not k or len(k) < 7: continue
    c = cli[k]
    if x["nombre"] and (not c["nombre"] or (x["fecha"] and (c["fmax"] is None or x["fecha"] >= c["fmax"]))):
        c["nombre"] = x["nombre"]
    if x["ciudad"] != "(SIN DATO)": c["ciudad"] = x["ciudad"]; c["depto"] = x["depto"]
    if x["direccion"]: c["direccion"] = x["direccion"]
    if x["producto"] != "(SIN DATO)": c["prods"].add(x["producto"][:30])
    c["cuentas"].add(x["cuenta"])
    if x["oid"] not in c["ordenes"] or x["clase"] == "entregado": c["ordenes"][x["oid"]] = x["clase"]
    if x["fecha"]:
        c["fmin"] = x["fecha"] if c["fmin"] is None else min(c["fmin"], x["fecha"])
        c["fmax"] = x["fecha"] if c["fmax"] is None else max(c["fmax"], x["fecha"])
def segmento(np, e, resueltos):
    # Sin órdenes cerradas (todas en tránsito o canceladas) la efectividad es indefinida:
    # NEUTRO, no RIESGO. Antes marcaba "mucha devolución" a quien no tenía ni una devolución.
    if resueltos == 0: return "NEUTRO"
    if np >= 3 and e >= 0.7: return "VIP (recurrente confiable)"
    if e >= 0.7: return "BUENO"
    if e < 0.5: return "RIESGO (mucha devolución)"
    return "NEUTRO"

wbC = Workbook(); wbC.remove(wbC.active)
ws = wbC.create_sheet("CLIENTES")
ws["A1"] = "MAESTRO DE CONTACTOS — CLIENTES CON PEDIDOS (sin duplicados)"; ws["A1"].font = TIT
ws.append([]); hd = ["Teléfono", "Nombre", "Depto", "Ciudad", "Productos", "Pedidos", "Entregados",
      "Devol.", "% Efectividad", "Segmento", "Etiqueta WhatsApp", "Última compra", "Cuenta"]
ws.append(hd); style_header(ws, 3, len(hd))
rowsC = []
for k, c in cli.items():
    ents = sum(1 for v in c["ordenes"].values() if v == "entregado")
    devs = sum(1 for v in c["ordenes"].values() if v == "devolucion")
    npd = len(c["ordenes"]); den = ents + devs; e = (ents / den) if den else 0
    rowsC.append((k, c, npd, ents, devs, e))
rowsC.sort(key=lambda t: (-t[2], -t[5]))
for k, c, npd, ents, devs, e in rowsC:
    nombre = c["nombre"] or wp_name.get(k, "")   # fallback: nombre guardado en WhatsApp
    ws.append([k, nombre[:30], c["depto"], c["ciudad"], ", ".join(sorted(c["prods"]))[:60],
        npd, ents, devs, pct(e) if (ents + devs) else "-", segmento(npd, e, ents + devs),
        ", ".join(sorted(wp_label.get(k, [])))[:40], f"{c['fmax']:%Y-%m-%d}" if c["fmax"] else "",
        "+".join(sorted(c["cuentas"]))])
for col, w in zip("ABCDEFGHIJKLM", [13, 26, 16, 18, 40, 8, 10, 8, 12, 26, 26, 13, 12]):
    ws.column_dimensions[col].width = w

# leads del bot (opcional)
ws = wbC.create_sheet("LEADS NO CLIENTES (bot)")
ws["A1"] = "LEADS DEL BOT QUE NO COMPRARON"; ws["A1"].font = TIT
ws.append([]); hd = ["Teléfono", "Nombre", "Ciudad", "Producto interés", "Últi. interacción", "Etiqueta WP"]
ws.append(hd); style_header(ws, 3, len(hd)); nlead = 0
leadfp = None
if os.path.isdir(SRC):
    for fp in glob.glob(os.path.join(SRC, "*.csv")):
        if os.path.basename(fp).upper().startswith("NO CLIENTE"): leadfp = fp; break
if leadfp:
    with open(leadfp, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            k = phone_key(row.get("phone"))
            nm = (row.get("name") or row.get("first_name") or "").strip()
            city = (row.get("city") or row.get("Ciudad") or "").strip()
            inter = (row.get("Producto a activar") or row.get("interest") or row.get("Producto Remarketing") or "").strip()
            last = (row.get("last_interaction") or "").strip()[:10]
            ws.append([k, nm[:26], city[:20], inter[:30], last, ", ".join(sorted(wp_label.get(k, [])))[:35]]); nlead += 1
for col, w in zip("ABCDEF", [13, 26, 20, 30, 13, 35]): ws.column_dimensions[col].width = w

# posibles / mensaje masivo (opcional, de un BASE*.xlsx en _FUENTES con hoja "POSIBLE*")
nposibles = 0
if os.path.isdir(SRC):
    for bmp in glob.glob(os.path.join(SRC, "*.xlsx")):
        try: wbb = openpyxl.load_workbook(bmp, read_only=True, data_only=True)
        except Exception: continue
        sh = next((s for s in wbb.sheetnames if "POSIBLE" in s.upper()), None)
        if not sh: wbb.close(); continue
        wsp = wbC.create_sheet("POSIBLES (msj masivo)")
        wsp["A1"] = "POSIBLES / LEADS PARA MENSAJE MASIVO"; wsp["A1"].font = TIT
        rws = [r for r in wbb[sh].iter_rows(values_only=True) if any(x is not None for x in r)]
        hdr = [str(x).strip() if x else "" for x in rws[0]]
        wsp.append([]); wsp.append(hdr); style_header(wsp, 3, len(hdr)); seen = set()
        for r in rws[1:]:
            k = phone_key(g(r, 0))
            if k in seen or es_prueba(g(r, 1), g(r, 0)): continue
            seen.add(k); wsp.append([str(x).strip() if x is not None else "" for x in r]); nposibles += 1
        for col, w in zip("ABCDEFGHIJKL", [15, 24, 16, 16, 26, 10, 10, 10, 10, 10, 14, 12]):
            wsp.column_dimensions[col].width = w
        wbb.close(); break

ws = wbC.create_sheet("RESUMEN", 0)
ws["B2"] = "MAESTRO DE CONTACTOS — RESUMEN"; ws["B2"].font = TIT
segc = Counter(segmento(npd, e, ents + devs) for _, _, npd, ents, devs, e in rowsC)
r = 4
for lab, v in [("Clientes únicos (con pedido)", len(rowsC)),
               ("  · VIP recurrentes", segc["VIP (recurrente confiable)"]),
               ("  · Buenos", segc["BUENO"]), ("  · En riesgo (devolución)", segc["RIESGO (mucha devolución)"]),
               ("  · Neutros", segc["NEUTRO"]),
               ("Clientes con etiqueta WhatsApp", sum(1 for k, *_ in rowsC if k in wp_label)),
               ("Leads del bot sin compra", nlead), ("Posibles para mensaje masivo", nposibles)]:
    ws.cell(r, 2, lab); ws.cell(r, 4, v); r += 1
ws.column_dimensions["B"].width = 34; ws.column_dimensions["D"].width = 12

pathC = os.path.join(OUT, "MAESTRO_CONTACTOS.xlsx"); wbC.save(pathC)
print("OK ->", pathC)
print(f"Clientes únicos: {len(rowsC)} | Leads bot: {nlead} | Posibles: {nposibles}")
