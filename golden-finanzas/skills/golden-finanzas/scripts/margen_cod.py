#!/usr/bin/env python3
"""Utilidad real por pedido en contra entrega (COD), con sensibilidad de ±20 %.

Ley del flete COD: se paga UN solo flete. El entregado paga el de ida; la devolución
pierde el flete de DEVOLUCIÓN (flete de ida × ratio, con 0 <= ratio <= 1: nunca mayor);
cancelado y rechazado no cuestan flete. La comisión de recaudo es una proporción del
precio y SOLO se paga en lo entregado (sin entrega no hay recaudo). La pauta (CPA) se paga
por cada pedido generado.

    utilidad por pedido = e·(P − C − F − P·k) − d·(F·r) − CPA

Si el flete va incluido en el precio ("envío gratis"), P es lo que paga el cliente y F el
flete real: la fórmula es la misma.

Acepta montos en formato colombiano (79.900 o $79.900) y fracciones con coma (0,62).

Uso:
  python3 margen_cod.py --precio 79.900 --costo 22.000 --flete 14.000 \\
      --entrega 0,62 --devolucion 0,25 --ratio 0,85 --cpa 9.000 --comision 0,05 --piso 10.000
  python3 margen_cod.py --autoprueba
"""
import io
import math
import re
import sys
from contextlib import redirect_stdout

CAMPOS = ("precio", "costo", "flete", "entrega", "devolucion", "ratio", "cpa")
OPCIONALES = ("comision", "piso")
ETIQUETA = {"precio": "precio", "costo": "costo", "flete": "flete", "entrega": "entrega",
            "devolucion": "devolución", "ratio": "ratio", "cpa": "CPA", "comision": "comisión",
            "piso": "piso"}
TOPE_MONTO = 1e12  # un billón de pesos: por encima es un error de digitación, no un pedido


class DatoInvalido(ValueError):
    pass


FRACCIONES = ("entrega", "devolucion", "ratio", "comision")


def numero(texto, nombre):
    """Lee un número sin adivinar. FRACCIONES (entrega, devolución, ratio, comisión): punto o coma
    son decimales ('0.735', '0,735', '1.000' = 1). MONTOS en pesos: el punto solo se acepta como
    separador de miles en grupos de tres ('79.900', '1.234.567', '50.000,00'); un punto que no
    forma grupos de tres ('12.34', '79.9') es ambiguo y se rechaza, porque un dígito de más o de
    menos cambia la magnitud por mil. Un monto entre 0 y 1 peso también se rechaza."""
    t = str(texto).strip().replace("$", "").replace(" ", "")
    if not t:
        raise DatoInvalido(f"{ETIQUETA[nombre]} vacío")
    if nombre in FRACCIONES:
        t = t.replace(",", ".")
    elif "." in t:
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", t):
            t = t.replace(".", "").replace(",", ".")
        else:
            raise DatoInvalido(f"{ETIQUETA[nombre]} ambiguo: '{texto}'. Escribe 79.900 o 79900")
    else:
        t = t.replace(",", ".")
    try:
        v = float(t)
    except ValueError:
        raise DatoInvalido(f"{ETIQUETA[nombre]} no es un número: '{texto}'")
    if nombre not in FRACCIONES and 0 < v < 1:
        raise DatoInvalido(f"{ETIQUETA[nombre]} de menos de un peso: '{texto}' parece una fracción en un campo de pesos")
    return v


def validar(p, c, f, e, d, r, cpa, k=0.0):
    for nombre, v in (("precio", p), ("costo", c), ("flete", f), ("entrega", e),
                      ("devolucion", d), ("ratio", r), ("cpa", cpa), ("comision", k)):
        if not math.isfinite(v):
            raise DatoInvalido(f"{ETIQUETA[nombre]} no es un número finito")
        if v < 0:
            raise DatoInvalido(f"{ETIQUETA[nombre]} negativo: no existe en este modelo")
        if v > TOPE_MONTO:
            raise DatoInvalido(f"{ETIQUETA[nombre]} fuera de rango (más de un billón)")
    if e + d > 1 + 1e-9:  # con ambas >= 0, esto ya rechaza entrega > 1 o devolución > 1 por separado
        raise DatoInvalido("entrega y devolución son fracciones y su suma no pasa de 1")
    if r > 1:
        raise DatoInvalido("ratio de devolución > 1: la devolución NUNCA cuesta más que la ida")
    if k >= 1:
        raise DatoInvalido("comisión de recaudo es una fracción del precio, menor que 1")


def utilidad(p, c, f, e, d, r, cpa, k=0.0):
    validar(p, c, f, e, d, r, cpa, k)
    return e * (p - c - f - p * k) - d * (f * r) - cpa


def cop(x):
    s = f"{abs(x):,.0f}".replace(",", ".")
    return f"-${s}" if round(x) < 0 else f"${s}"


def dec(x, n=2):
    return f"{x:.{n}f}".replace(".", ",")


def multiplo(p, c):
    """Precio ÷ costo TRUNCADO (no redondeado): 2,995 se muestra 2,99, nunca 3,00."""
    return math.floor(p / c * 100) / 100


def sensibilidad(v):
    """Filas de ±20 % moviendo UNA variable. Al mover la entrega, la devolución queda fija:
    lo que sube la entrega sale de cancelados y rechazados; si topa en 1 − devolución, se avisa."""
    filas = {}
    for etiqueta, clave in (("precio", "p"), ("entrega", "e"), ("CPA", "cpa")):
        fila = []
        for mult in (0.8, 1.0, 1.2):
            w = dict(v)
            w[clave] = v[clave] * mult
            nota = ""
            if clave == "e" and w["e"] > 1 - w["d"]:
                w["e"] = 1 - w["d"]
                nota = " (topa)"
            fila.append((int(round(mult * 100)), utilidad(**w), nota))
        filas[etiqueta] = fila
    return filas


def informe(a):
    """a: dict con los campos ya convertidos; comision y piso pueden ser None."""
    k = a.get("comision")
    v = dict(p=a["precio"], c=a["costo"], f=a["flete"], e=a["entrega"], d=a["devolucion"],
             r=a["ratio"], cpa=a["cpa"], k=k or 0.0)
    base = utilidad(**v)
    lineas = []
    mult = f" ({dec(multiplo(a['precio'], a['costo']))}x el costo)" if a["costo"] >= 1 else " (costo menor a un peso: sin múltiplo)"
    lineas.append(f"Precio {cop(a['precio'])} · costo {cop(a['costo'])}{mult} · flete {cop(a['flete'])}")
    com = f"comisión de recaudo {dec(k * 100, 1)} % (solo en entregados)" if k is not None \
        else "comisión de recaudo NO incluida [PENDIENTE: comisión]"
    lineas.append(f"Entrega {dec(a['entrega'] * 100, 1)} % · devolución {dec(a['devolucion'] * 100, 1)} % · "
                  f"ratio de devolución {dec(a['ratio'], 3)} · CPA {cop(a['cpa'])} · {com}")
    piso = a.get("piso")
    if piso is None:
        veredicto = "sin veredicto: [PENDIENTE: piso] (se lee de la regla de viabilidad del negocio)"
    else:
        # Se compara al peso, igual que se muestra: 13.680,9999 es $13.681 y no puede decir NO PASA.
        veredicto = f"piso {cop(piso)}: {'PASA' if round(base) >= round(piso) else 'NO PASA'}"
    lineas.append(f"UTILIDAD POR PEDIDO GENERADO: {cop(base)}  ({veredicto})")
    lineas.append("")
    lineas.append("Sensibilidad ±20 % (una variable a la vez; al mover la entrega, la devolución queda fija):")
    for etiqueta, fila in sensibilidad(v).items():
        lineas.append(f"  {etiqueta:8} " + " · ".join(f"{m} %: {cop(u)}{n}" for m, u, n in fila))
    return base, lineas


def leer_args(argv):
    datos, i = {}, 0
    conocidos = set(CAMPOS) | set(OPCIONALES)
    while i < len(argv):
        tok = argv[i]
        if not tok.startswith("--"):
            raise DatoInvalido(f"argumento suelto sin nombre: '{tok}'")
        clave, _, valor = tok[2:].partition("=")
        if clave not in conocidos:
            raise DatoInvalido(f"argumento desconocido: --{clave}")
        if not valor:
            i += 1
            if i >= len(argv):
                raise DatoInvalido(f"--{clave} sin valor")
            valor = argv[i]
        if clave in datos:
            raise DatoInvalido(f"--{clave} repetido: no se elige en silencio cuál vale")
        datos[clave] = numero(valor, clave)
        i += 1
    piso = datos.get("piso")
    if piso is not None and (not math.isfinite(piso) or piso < 0 or piso > TOPE_MONTO):
        raise DatoInvalido("piso inválido: tiene que ser un monto finito, positivo y menor que un billón")
    return datos


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    if argv[:1] == ["--autoprueba"]:
        if len(argv) > 1:
            print("DATO INVÁLIDO: --autoprueba no lleva más argumentos")
            return 2
        return autoprueba()
    try:
        datos = leer_args(argv)
    except DatoInvalido as err:
        print(f"DATO INVÁLIDO: {err}")
        return 2
    faltan = [ETIQUETA[n] for n in CAMPOS if n not in datos]
    if faltan:
        print("[PENDIENTE: " + ", ".join(faltan) + "]: no se modela con datos inventados")
        return 2
    try:
        _, lineas = informe(datos)
    except DatoInvalido as err:
        print(f"DATO INVÁLIDO: {err}")
        return 2
    except OverflowError:
        print("DATO INVÁLIDO: los montos desbordan el cálculo")
        return 2
    print("\n".join(lineas))
    return 0


def _rechaza(**kw):
    try:
        utilidad(**kw)
        return False
    except DatoInvalido:
        return True


def _corre(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(argv)
    return rc, buf.getvalue()


def autoprueba():
    base = dict(p=80000, c=25000, f=15000, e=0.6, d=0.3, r=0.8, cpa=10000)
    ok_args = ["--precio", "80000", "--costo", "25000", "--flete", "15000", "--entrega", "0.6",
               "--devolucion", "0.3", "--ratio", "0.8", "--cpa", "10000"]
    casos = []
    # Fórmula, calculada a mano: 0,6·40000 − 0,3·12000 − 10000 = 10400
    casos.append(("fórmula a mano", abs(utilidad(**base) - 10400) < 1e-6))
    # Ratio 1 (cobra la devolución completa): 0,7·34900 − 0,2·15000 − 12000 = 9430
    casos.append(("ratio 1 ACEPTADO y bien calculado",
                  abs(utilidad(p=79900, c=30000, f=15000, e=0.7, d=0.2, r=1.0, cpa=12000) - 9430) < 1e-6))
    casos.append(("ratio 0 aceptado (no cobra retorno)", abs(utilidad(**{**base, "r": 0}) - 14000) < 1e-6))
    casos.append(("entrega + devolución = 1 aceptado", not _rechaza(**{**base, "e": 0.7, "d": 0.3})))
    casos.append(("cancelado no cuesta flete", utilidad(**{**base, "e": 0, "d": 0}) == -10000))
    # Comisión SOLO en entregados: 0,6·(40000 − 3200) − 3600 − 10000 = 8480. Si tocara la devolución daría otro número.
    casos.append(("comisión solo en entregados", abs(utilidad(**base, k=0.04) - 8480) < 1e-6))
    casos.append(("comisión con entrega 0 no cuesta", utilidad(**{**base, "e": 0, "d": 0.3}, k=0.04) == utilidad(**{**base, "e": 0, "d": 0.3})))
    # Controles negativos: cada frontera se rechaza
    casos.append(("ratio > 1 rechazado", _rechaza(**{**base, "r": 1.01})))
    casos.append(("ratio negativo rechazado", _rechaza(**{**base, "r": -0.1})))
    casos.append(("entrega > 1 sola rechazada", _rechaza(**{**base, "e": 1.5, "d": 0})))
    casos.append(("entrega + devolución > 1 rechazado", _rechaza(**{**base, "e": 0.8})))
    casos.append(("montos negativos rechazados", _rechaza(**{**base, "p": -1}) and _rechaza(**{**base, "cpa": -1})))
    casos.append(("NaN e infinito rechazados", _rechaza(**{**base, "r": float("nan")}) and _rechaza(**{**base, "p": float("inf")})))
    casos.append(("comisión ≥ 1 rechazada", _rechaza(**base, k=1.0)))
    casos.append(("un flete, no ida y vuelta", utilidad(**base) > 0.6 * 40000 - 0.3 * (15000 * 2) - 10000))
    # Formato
    casos.append(("miles con punto", cop(1234567) == "$1.234.567" and cop(-7015) == "-$7.015"))
    casos.append(("decimales con coma", dec(0.85) == "0,85" and dec(62.5, 1) == "62,5"))
    casos.append(("múltiplo truncado, no redondeado", multiplo(59900, 20000) == 2.99))
    casos.append(("lee formato colombiano", numero("79.900", "precio") == 79900 and numero("$1.234.567", "precio") == 1234567
                  and numero("0,62", "entrega") == 0.62 and numero("0.62", "entrega") == 0.62))
    # Sensibilidad: cada fila mueve SU variable
    sens = sensibilidad(base)
    casos.append(("sensibilidad de precio mueve el PRECIO", abs(sens["precio"][0][1] - utilidad(**{**base, "p": 64000})) < 1e-6))
    casos.append(("sensibilidad de CPA mueve el CPA", abs(sens["CPA"][2][1] - utilidad(**{**base, "cpa": 12000})) < 1e-6))
    casos.append(("sensibilidad de entrega mueve la ENTREGA", abs(sens["entrega"][0][1] - utilidad(**{**base, "e": 0.48})) < 1e-6))
    casos.append(("entrega topada se avisa", sens["entrega"][2][2] == " (topa)"))
    # Informe
    d = dict(precio=80000, costo=25000, flete=15000, entrega=0.6, devolucion=0.3, ratio=0.8, cpa=10000)
    _, l0 = informe(d)
    casos.append(("informe muestra costo, múltiplo y flete correctos",
                  "costo $25.000 (3,20x el costo) · flete $15.000" in l0[0]))
    casos.append(("sin comisión se avisa PENDIENTE", "PENDIENTE: comisión" in l0[1]))
    casos.append(("sin piso no hay veredicto", "PENDIENTE: piso" in l0[2] and "PASA" not in l0[2]))
    _, l1 = informe({**d, "piso": 7500})
    _, l2 = informe({**d, "piso": 12000})
    _, l3 = informe({**d, "piso": 10400})
    casos.append(("PASA y NO PASA en su sitio", "PASA)" in l1[2] and "NO PASA" in l2[2]))
    casos.append(("utilidad igual al piso PASA", "NO PASA" not in l3[2] and "PASA" in l3[2]))
    _, l4 = informe({**d, "costo": 0})
    casos.append(("costo 0 no revienta", "sin múltiplo" in l4[0]))
    # Línea de comandos: códigos de salida y que el piso llegue
    rc, out = _corre(ok_args)
    casos.append(("CLI completo sale 0", rc == 0 and "UTILIDAD" in out))
    rc, out = _corre(ok_args + ["--piso", "12000"])
    casos.append(("CLI respeta --piso", rc == 0 and "NO PASA" in out))
    rc, out = _corre(ok_args[:6])
    casos.append(("CLI con faltantes sale 2 y con tildes", rc == 2 and "PENDIENTE" in out and "devolución" in out))
    rc, out = _corre(ok_args + ["--ratio", "1,5"])
    casos.append(("CLI dato imposible sale 2", rc == 2 and "DATO INVÁLIDO" in out))
    rc, _ = _corre(ok_args + ["--piso", "nan"])
    rc2, _ = _corre(ok_args + ["--piso", "-50000"])
    casos.append(("CLI piso NaN o negativo sale 2", rc == 2 and rc2 == 2))
    rc, out = _corre(["--precio", "79.900", "--costo", "22.000", "--flete", "14.000", "--entrega", "0,62",
                      "--devolucion", "0,25", "--ratio", "0,85", "--cpa", "9.000"])
    casos.append(("CLI lee 79.900 como setenta y nueve mil", rc == 0 and "Precio $79.900" in out))
    rc, out = _corre(["--precio", "1.7e308", "--costo", "1", "--flete", "1", "--entrega", "0.5",
                      "--devolucion", "0.1", "--ratio", "0.5", "--cpa", "1"])
    casos.append(("CLI monto absurdo sale 2 sin traceback", rc == 2 and "DATO INVÁLIDO" in out))
    # SALIDA COMPLETA, letra por letra, contra un resultado calculado A MANO (no generado por el
    # script), con comisión 5 %: base 0,6·(80.000−25.000−15.000−4.000) − 0,3·12.000 − 10.000 = 8.000.
    # Precio 80 %: 0,6·(64.000−40.000−3.200) − 13.600 = −1.120 · 120 %: 0,6·51.200 − 13.600 = 17.120.
    # Entrega 80 %: 0,48·36.000 − 13.600 = 3.680 · 120 %: topa en 0,7 → 25.200 − 13.600 = 11.600.
    # CPA 80 %: 21.600 − 3.600 − 8.000 = 10.000 · 120 %: 6.000.
    esperado = "\n".join([
        "Precio $80.000 · costo $25.000 (3,20x el costo) · flete $15.000",
        "Entrega 60,0 % · devolución 30,0 % · ratio de devolución 0,800 · CPA $10.000 · "
        "comisión de recaudo 5,0 % (solo en entregados)",
        "UTILIDAD POR PEDIDO GENERADO: $8.000  (piso $7.000: PASA)",
        "",
        "Sensibilidad ±20 % (una variable a la vez; al mover la entrega, la devolución queda fija):",
        "  precio   80 %: -$1.120 · 100 %: $8.000 · 120 %: $17.120",
        "  entrega  80 %: $3.680 · 100 %: $8.000 · 120 %: $11.600 (topa)",
        "  CPA      80 %: $10.000 · 100 %: $8.000 · 120 %: $6.000",
    ]) + "\n"
    rc, out = _corre(ok_args + ["--comision", "0,05", "--piso", "7.000"])
    casos.append(("SALIDA COMPLETA idéntica a la calculada a mano", rc == 0 and out == esperado))
    # Cada campo obligatorio que falte, por separado, sale 2 y se nombra
    faltantes_ok = True
    for i in range(0, len(ok_args), 2):
        parcial = ok_args[:i] + ok_args[i + 2:]
        rc, out = _corre(parcial)
        nombre = ETIQUETA[ok_args[i][2:]]
        faltantes_ok &= rc == 2 and f"PENDIENTE: {nombre}]" in out
    casos.append(("cada campo faltante, uno por uno, sale 2 y se nombra", faltantes_ok))
    rc, out = _corre(ok_args)
    casos.append(("CLI sin piso: sin veredicto", rc == 0 and "PENDIENTE: piso" in out and "PASA" not in out))
    casos.append(("CLI sin comisión: PENDIENTE a la vista", "PENDIENTE: comisión" in out))
    rc, out = _corre(ok_args + ["--piso", "10.400"])
    casos.append(("CLI utilidad igual al piso PASA", rc == 0 and "NO PASA" not in out and "PASA)" in out))
    rc, out = _corre(["--precio", "80000", "--costo", "25000", "--flete", "15000", "--entrega", "0,72",
                      "--devolucion", "0,3", "--ratio", "0,8", "--cpa", "10000"])
    casos.append(("entrega + devolución = 1,02 rechazado", rc == 2 and "DATO INVÁLIDO" in out))
    # Lectura de números: fracciones con 3 decimales y montos ambiguos
    lectura = [("entrega", "0.735", 0.735), ("ratio", "0.926", 0.926), ("ratio", "1.000", 1.0),
               ("ratio", "0,850", 0.85), ("precio", "50.000,00", 50000), ("precio", "79 900", 79900),
               ("precio", "12.345", 12345)]
    casos.append(("fracciones con 3 decimales y montos con miles se leen bien",
                  all(abs(numero(s, n) - v) < 1e-9 for n, s, v in lectura)))
    ambiguos_ok = True
    for s in ("12.34", "79.9", "1.00", "0,5", ".5"):
        try:
            numero(s, "precio")
            ambiguos_ok = False
        except DatoInvalido:
            pass
    casos.append(("montos ambiguos o de menos de un peso se rechazan", ambiguos_ok))
    rc, out = _corre(ok_args + ["--precio", "1"])
    rc2, _ = _corre(ok_args + ["--piso", "7500", "--piso", "99999"])
    casos.append(("argumento repetido sale 2", rc == 2 and "repetido" in out and rc2 == 2))
    rc, _ = _corre(["--autoprueba", "--x"])
    casos.append(("--autoprueba con basura sale 2", rc == 2))
    _, l5 = informe({**d, "costo": 0.4})
    casos.append(("costo menor a un peso: sin múltiplo", "sin múltiplo" in l5[0]))
    casos.append(("sin -$0", cop(-0.4) == "$0"))
    ok = 0
    for nombre, paso in casos:
        print(f"  {'OK   ' if paso else 'FALLA'} · {nombre}")
        ok += bool(paso)
    print(f"\nCOBERTURA: {ok} de {len(casos)} pruebas en verde")
    return 0 if ok == len(casos) else 1


if __name__ == "__main__":
    sys.exit(main())
