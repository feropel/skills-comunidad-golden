#!/usr/bin/env python3
"""
seguimiento.py — ¿la caza acierta? Relee lo que la skill dijo de cada candidato y lo compara
con lo que el producto hizo DESPUÉS.

Por qué existe (propuesta del chat par, 2026-09-18): sin esto la skill nunca sabe si acierta y
los umbrales se quedan heredados para siempre. correr_lote.py --registro deja una línea por
candidato visto (LISTA, CASI, FUERA); aquí se cierra el ciclo.

Uso:
  python3 seguimiento.py <_registro.jsonl> <carpeta_historiales> --dias 30 [--hoy AAAA-MM-DD]
  python3 seguimiento.py --autoprueba
<carpeta_historiales> tiene un archivo <dropi_id>.json por producto: la respuesta de
get_product_history desde la fecha del registro hasta hoy, guardada tal cual.

Definiciones (las MISMAS del backtest, references/calibracion.md, llevadas a la ventana):
  GANÓ   = ventas depuradas ≥ 10 por día en la ventana
  MURIÓ  = ventas depuradas < 1 por día
  MEDIO  = el resto
Salida: por estado (LISTA / CASI / FUERA), cuántos ganaron y cuántos murieron. Si LISTA no gana
más que CASI y FUERA, los filtros no están separando y hay que recalibrar.
"""
import json
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ventas_reales as vr  # noqa: E402
import comun  # noqa: E402


class ErrorDeEntrada(Exception):
    pass


def fecha(x):
    iso = comun.fecha_iso(x)  # una sola forma de leer fechas (comun.py)
    return date.fromisoformat(iso) if iso else None


def clasificar(depuradas, dias):
    if depuradas >= 10 * dias:
        return "GANÓ"
    if depuradas < dias:
        return "MURIÓ"
    return "MEDIO"


def seguir(registro, carpeta, dias=30, hoy=None):
    hoy = hoy or date.today()
    if not isinstance(dias, int) or dias < 1:
        raise ErrorDeEntrada("--dias debe ser un entero de 1 en adelante (con 0, un producto sin ventas salía GANÓ)")
    tabla = {}
    sin_historial, pendientes, ilegibles, duplicados, incompletos = [], 0, 0, 0, 0
    vistos = set()
    try:
        lineas = open(registro, encoding="utf-8").read().splitlines()
    except OSError as e:
        raise ErrorDeEntrada("no se pudo leer el registro %s: %s" % (registro, e))
    for linea in lineas:
        if not linea.strip():
            continue
        try:
            r = json.loads(linea)
            f0 = fecha(r.get("fecha"))
        except ValueError:
            r, f0 = None, None
        if not isinstance(r, dict) or f0 is None or "estado" not in r:
            ilegibles += 1
            continue
        if (hoy - f0).days < dias:
            pendientes += 1
            continue
        pid = comun.ident(r.get("dropi_id"))
        clave = (pid or comun.clave(r.get("nombre")), str(f0))
        if clave in vistos:
            duplicados += 1  # se cuenta y se dice: nada desaparece en silencio
            continue
        vistos.add(clave)
        # Un ID es letras, dígitos o guiones: "../x" armaba una ruta fuera de la carpeta.
        valido = bool(pid) and all(ch.isalnum() or ch in "-_" for ch in pid)
        ruta = os.path.join(carpeta, "%s.json" % pid) if valido else ""
        if not valido or not os.path.exists(ruta):
            sin_historial.append(r.get("nombre") or r.get("dropi_id"))
            continue
        try:
            filas = vr.normalizar(json.load(open(ruta, encoding="utf-8")))
        except (OSError, ValueError, vr.ErrorDeEntrada):
            sin_historial.append(str(r.get("nombre") or r.get("dropi_id")) + " (historial ilegible)")
            continue
        ini, fin = str(f0), (f0 + timedelta(days=dias)).isoformat()
        ventana = [f for f in filas if ini < f[0][:10] <= fin]
        # Un historial que cubre 5 de 30 días no dice si el producto ganó o murió: INCOMPLETO.
        dias_leidos = len({f[0][:10] for f in ventana})
        if dias_leidos < 0.8 * dias:
            res = "INCOMPLETO"
            incompletos += 1
        else:
            ev = vr.evaluar(ventana)
            res = clasificar(ev.get("vendidas_depuradas") or 0, dias)
        t = tabla.setdefault(r["estado"], {"N": 0, "GANÓ": 0, "MURIÓ": 0, "MEDIO": 0, "INCOMPLETO": 0})
        t[res] += 1
        if res != "INCOMPLETO":
            t["N"] += 1
    for t in tabla.values():
        t["gano_pct"] = round(100 * t["GANÓ"] / t["N"]) if t["N"] else None
    aviso = []
    for n, txt in ((ilegibles, "línea(s) del registro ilegibles (sin fecha, sin estado o no es JSON)"),
                   (duplicados, "registro(s) duplicados (mismo producto y fecha): se contó el primero"),
                   (incompletos, "historial(es) que no cubren el 80% de la ventana: INCOMPLETO, no se juzgan")):
        if n:
            aviso.append("%d %s" % (n, txt))
    if sin_historial:
        aviso.append("%d candidato(s) sin historial guardado: no entran (%s)" % (len(sin_historial), ", ".join(map(str, sin_historial[:5]))))
    l, c = tabla.get("LISTA"), tabla.get("CASI")
    if l and c and l["N"] >= 5 and c["N"] >= 5:
        aviso.append("LISTA gana %s%% contra CASI %s%%: %s" % (l["gano_pct"], c["gano_pct"],
                     "los filtros separan" if l["gano_pct"] > c["gano_pct"] else "los filtros NO separan: recalibrar (references/calibracion.md)"))
    else:
        aviso.append("menos de 5 por estado: sin muestra para juzgar los filtros todavía")
    return {"ventana_dias": dias, "hoy": str(hoy), "por_estado": tabla, "pendientes_por_madurar": pendientes, "avisos": aviso}


def autoprueba():
    import tempfile
    t = tempfile.mkdtemp()
    hist = os.path.join(t, "h")
    os.makedirs(hist)
    reg = os.path.join(t, "r.jsonl")
    lineas = []
    def prod(pid, estado, diario, fecha="2026-08-01"):
        lineas.append(json.dumps({"fecha": fecha, "nombre": pid, "dropi_id": pid, "estado": estado}))
        s, h = 10000, []
        for i in range(35):
            d = (date(2026, 8, 2) + timedelta(days=i)).isoformat()
            s -= diario
            h.append([d, s, diario, 20000])
        json.dump({"h": h}, open(os.path.join(hist, pid + ".json"), "w"))
    for i in range(5):
        prod("L%d" % i, "LISTA", 15)       # ganan
    for i in range(5):
        prod("C%d" % i, "CASI", 0 if i < 4 else 15)   # 4 mueren (0 ventas), 1 gana
    prod("F0", "FUERA", 3)                 # medio
    lineas.append(json.dumps({"fecha": "2026-09-15", "nombre": "nuevo", "dropi_id": "N", "estado": "LISTA"}))
    lineas.append(json.dumps({"fecha": "2026-08-01", "nombre": "sinh", "dropi_id": "X", "estado": "LISTA"}))
    lineas.append("esto no es json")
    lineas.append(json.dumps({"fecha": "01-08-2026", "nombre": "L0", "dropi_id": "L0", "estado": "LISTA"}))  # duplicado con fecha DD-MM
    lineas.append(json.dumps({"fecha": "2026-08-01", "nombre": "corto", "dropi_id": "K", "estado": "FUERA"}))
    json.dump({"h": [["2026-08-%02d" % d, 100 - d, 1, 1000] for d in range(2, 7)]}, open(os.path.join(hist, "K.json"), "w"))
    open(reg, "w").write("\n".join(lineas) + "\n")
    r = seguir(reg, hist, 30, date(2026, 9, 18))
    e = r["por_estado"]
    fallos = []
    if e["LISTA"]["GANÓ"] != 5: fallos.append("LISTA debía ganar 5")
    if (e["CASI"]["MURIÓ"], e["CASI"]["GANÓ"]) != (4, 1): fallos.append("CASI debía 4 muertos y 1 ganador")
    if e["FUERA"]["MEDIO"] != 1: fallos.append("FUERA medio")
    if r["pendientes_por_madurar"] != 1: fallos.append("el registro de hace 3 días no madura")
    if not any("sin historial" in a for a in r["avisos"]): fallos.append("debía avisar el que no tiene historial")
    if not any("los filtros separan" in a for a in r["avisos"]): fallos.append("debía juzgar que los filtros separan")
    if not any("ilegibles" in a for a in r["avisos"]): fallos.append("debía avisar la línea ilegible")
    if not any("duplicados" in a for a in r["avisos"]): fallos.append("debía avisar el duplicado (fecha DD-MM leída)")
    if e["FUERA"].get("INCOMPLETO") != 1: fallos.append("historial de 5 días en ventana de 30 debía ser INCOMPLETO")
    try:
        seguir(reg, hist, 0, date(2026, 9, 18))
        fallos.append("--dias 0 debía dar error (daba GANÓ a productos sin ventas)")
    except ErrorDeEntrada:
        pass
    open(reg, "a").write(json.dumps({"fecha": "2026-08-01", "nombre": "esp", "dropi_id": " L1 ", "estado": "LISTA"}) + "\n")
    r2 = seguir(reg, hist, 30, date(2026, 9, 18))
    if not any("duplicados" in a for a in r2["avisos"]) or r2["por_estado"]["LISTA"]["GANÓ"] != 5:
        fallos.append("un dropi_id con espacios debía encontrar su historial (y contarse como duplicado de L1)")
    for f in fallos:
        print("FALLA", f)
    # Un archivo REAL fuera de la carpeta de historiales: sin la regla se leería y contaría.
    json.dump({"h": [[(date(2026, 8, 2) + timedelta(days=i)).isoformat(), 9000 - 15 * i, 15, 1] for i in range(35)]},
              open(os.path.join(t, "fuera.json"), "w"))
    open(reg, "a").write(json.dumps({"fecha": "2026-08-01", "nombre": "ruta", "dropi_id": "../fuera", "estado": "LISTA"}) + "\n")
    r3 = seguir(reg, hist, 30, date(2026, 9, 18))
    if not any("sin historial" in a and "ruta" in a for a in r3["avisos"]):
        fallos.append("un dropi_id con '../' debía quedar sin historial, no armar una ruta fuera de la carpeta")
    print("AUTOPRUEBA %d de 12" % (12 - len(fallos)))
    return 1 if fallos else 0


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    try:
        def val(b):
            i = sys.argv.index(b)
            if i + 1 >= len(sys.argv):
                raise ErrorDeEntrada("%s necesita un valor" % b)
            return sys.argv[i + 1]
        try:
            dias = int(val("--dias")) if "--dias" in sys.argv else 30
            hoy = fecha(val("--hoy")) if "--hoy" in sys.argv else None
        except ValueError:
            raise ErrorDeEntrada("--dias debe ser un número entero")
        if "--hoy" in sys.argv and hoy is None:
            raise ErrorDeEntrada("--hoy debe ser una fecha AAAA-MM-DD")
        if not os.path.isdir(sys.argv[2]):
            raise ErrorDeEntrada("no existe la carpeta de historiales %s" % sys.argv[2])
        print(json.dumps(seguir(sys.argv[1], sys.argv[2], dias, hoy), ensure_ascii=False, indent=1))
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
