#!/usr/bin/env python3
"""
brecha_mercados.py — ¿este PROBLEMA ya está validado afuera y sigue libre aquí?

Por qué existe. Circula un método ("deja de buscar productos virales, busca problemáticas
validadas"): contar anuncios activos de un problema afuera y aquí, y si afuera hay 14.000 y aquí
8, declararlo "servido en bandeja". La idea de partir del PROBLEMA es buena y la skill no la
tenía. La regla, medida el 2026-09-19 con la Ad Library de Meta, NO se sostiene tal cual:

1. **Tamaño.** EE.UU. + Canadá + Reino Unido son ~9 veces la población de Colombia y pautan más
   por persona. Medido: corrector de postura 2.637 contra 337 (7,8×), fascitis plantar 12.330
   contra 492 (25×), ronquidos 17.705 contra 671 (26×), tinnitus 7.066 contra 321 (22×). Un 8×
   es lo NORMAL, no una brecha: la brecha empieza donde el múltiplo se dispara sobre eso.
2. **El conteo de aquí no es competencia de aquí.** En 50 de los 671 anuncios de "ronquidos" en
   Colombia: 25 cobran en pesos, 15 en dong vietnamita, 9 en dólares y 1 en reales. La mitad del
   número es ruido extranjero (trampa 6: el país mal asignado).
3. **Un anuncio no es un vendedor de producto.** En esa misma muestra, detrás de los 25 en pesos
   hay ~7 tiendas y 2 clínicas: servicios, no producto.

Por eso aquí NO se compara "anuncios contra anuncios": se compara el múltiplo observado contra el
múltiplo esperado por tamaño de mercado, y el conteo local se corrige por la proporción de
anuncios que sí cobran en la moneda del país.

Uso:
  python3 brecha_mercados.py --problema "ronquidos" --afuera 17705 --aqui 671 \\
      --muestra-aqui aqui.json [--paises-afuera US,CA,GB] [--pais CO]
  python3 brecha_mercados.py --autoprueba
`aqui.json` es la respuesta de ads_library_search del país (limit 50 sirve) guardada tal cual:
de ahí sale qué proporción cobra en la moneda local. Sin ella, el resultado se marca SIN DEPURAR.

Salida: múltiplo observado, múltiplo esperado por población, índice de brecha (observado /
esperado) y un veredicto que NUNCA dice "oportunidad" solo: dice qué falta medir después
(demanda real en Dropi, proveedor, plata y compuertas de salud).
Solo biblioteca estándar de Python 3.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

# Población en millones (Banco Mundial 2024, redondeada) y moneda. Es un DENOMINADOR, no una
# medida de mercado publicitario: se declara como aproximación.
MERCADOS = {
    "US": (335.0, "USD"), "CA": (40.0, "CAD"), "GB": (68.0, "GBP"), "AU": (27.0, "AUD"),
    "ES": (48.0, "EUR"), "MX": (129.0, "MXN"), "CO": (52.0, "COP"), "CL": (19.5, "CLP"),
    "PE": (34.0, "PEN"), "EC": (18.0, "USD"), "GT": (18.0, "GTQ"), "AR": (46.0, "ARS"),
}
BRECHA_CLARA = 2.0   # el múltiplo observado dobla al esperado por tamaño
BRECHA_FUERTE = 4.0


class ErrorDeEntrada(Exception):
    pass


def proporcion_local(muestra, moneda):
    """Qué parte de los anuncios de la muestra cobra en la moneda del país. Devuelve
    (proporción, leídos, por_moneda) o (None, 0, {}) si la muestra no trae monedas."""
    filas = muestra
    if isinstance(muestra, dict):
        filas = muestra.get("ads") or muestra.get("data") or []
        if isinstance(muestra.get("results"), str):  # ads_library_search devuelve un JSON dentro
            try:
                filas = json.loads(muestra["results"]).get("ads", [])
            except ValueError:
                filas = []
    if not isinstance(filas, list) or not filas:
        return None, 0, {}
    por = {}
    for a in filas:
        if isinstance(a, dict):
            por[str(a.get("currency") or "(sin moneda)")] = por.get(str(a.get("currency") or "(sin moneda)"), 0) + 1
    leidos = sum(por.values())
    if not leidos:
        return None, 0, {}
    return por.get(moneda, 0) / leidos, leidos, por


def analizar(problema, afuera, aqui, paises_afuera=("US", "CA", "GB"), pais="CO", muestra_aqui=None):
    if comun.numero(afuera) is None or comun.numero(aqui) is None:
        raise ErrorDeEntrada("--afuera y --aqui son conteos de anuncios (números)")
    afuera, aqui = comun.numero(afuera), comun.numero(aqui)
    if afuera < 0 or aqui < 0:
        raise ErrorDeEntrada("los conteos no pueden ser negativos")
    if pais not in MERCADOS:
        raise ErrorDeEntrada("no hay población declarada para %s: agrégala a MERCADOS y dilo" % pais)
    faltan = [p for p in paises_afuera if p not in MERCADOS]
    if faltan:
        raise ErrorDeEntrada("no hay población declarada para %s" % ", ".join(faltan))

    pob_afuera = sum(MERCADOS[p][0] for p in paises_afuera)
    pob_aqui, moneda = MERCADOS[pais]
    esperado = pob_afuera / pob_aqui
    avisos = []

    aqui_depurado, prop, leidos, por_moneda = aqui, None, 0, {}
    if muestra_aqui is not None:
        prop, leidos, por_moneda = proporcion_local(muestra_aqui, moneda)
        if prop is None:
            avisos.append("la muestra de %s no trae monedas: el conteo local queda SIN DEPURAR" % pais)
        else:
            aqui_depurado = round(aqui * prop)
            avisos.append("muestra de %d anuncio(s) de %s: %.0f%% cobra en %s; el resto es de otro país (trampa 6)"
                          % (leidos, pais, prop * 100, moneda))
    else:
        avisos.append("sin muestra de %s: el conteo local queda SIN DEPURAR y el múltiplo se sobreestima" % pais)

    if aqui_depurado <= 0:
        observado = None
        avisos.append("0 anuncios locales tras depurar: puede ser hueco real o que nadie lo compre; hay que medir demanda antes de concluir")
    else:
        observado = afuera / aqui_depurado
    indice = (observado / esperado) if observado else None

    if indice is None:
        nivel = "SIN ÍNDICE"
    elif indice >= BRECHA_FUERTE:
        nivel = "BRECHA FUERTE"
    elif indice >= BRECHA_CLARA:
        nivel = "BRECHA"
    else:
        nivel = "SIN BRECHA (el múltiplo es el normal por tamaño de mercado)"

    return {
        "problema": problema,
        "paises_afuera": list(paises_afuera),
        "pais": pais,
        "anuncios_afuera": int(afuera),
        "anuncios_aqui_reportados": int(aqui),
        "anuncios_aqui_depurados": int(aqui_depurado),
        "proporcion_moneda_local": None if prop is None else round(prop, 3),
        "monedas_en_la_muestra": por_moneda,
        "multiplo_observado": None if observado is None else round(observado, 1),
        "multiplo_esperado_por_poblacion": round(esperado, 1),
        "indice_de_brecha": None if indice is None else round(indice, 2),
        "veredicto": nivel,
        "siguiente_paso": ("no es un producto todavía: hay que encontrar QUÉ producto resuelve el problema, "
                           "medir si en %s alguien lo compra (DropKiller: ventas depuradas y proveedores), "
                           "correr la plata (viabilidad_cod.py) y pasar las compuertas de salud (reglas 5, 6 y 8). "
                           "Pocos anuncios aquí también puede ser que no se venda." % pais),
        "avisos": avisos + ["la población es un denominador aproximado, no el tamaño del mercado publicitario",
                            "un anuncio no es un vendedor: varias páginas de una misma tienda inflan los dos lados"],
    }


def autoprueba():
    casos, fallos = 0, []
    def chequeo(n, ok):
        nonlocal casos
        casos += 1
        if not ok:
            fallos.append(n)
    # Medido 2026-09-19: ronquidos 17.705 afuera contra 671 aquí, muestra 50 con 25 en COP
    muestra = {"ads": [{"currency": c} for c in ["COP"] * 25 + ["VND"] * 15 + ["USD"] * 9 + ["BRL"]]}
    r = analizar("ronquidos", 17705, 671, ("US", "CA", "GB"), "CO", muestra)
    chequeo("depura el conteo local por moneda", r["anuncios_aqui_depurados"] == 336)
    chequeo("múltiplo esperado por población ~8,5", 8 <= r["multiplo_esperado_por_poblacion"] <= 9)
    chequeo("ronquidos da brecha", r["veredicto"].startswith("BRECHA"))
    # Corrector de postura: 2.637 contra 337; aunque no se depure, 7,8× está por debajo de 8,5×
    r2 = analizar("corrector de postura", 2637, 337, ("US", "CA", "GB"), "CO")
    chequeo("sin depurar se declara", any("SIN DEPURAR" in a for a in r2["avisos"]))
    chequeo("7,8× no es brecha", r2["veredicto"].startswith("SIN BRECHA"))
    # Un problema con 0 locales no se declara oportunidad
    r3 = analizar("x", 5000, 0, ("US",), "CO")
    chequeo("cero local no concluye", r3["indice_de_brecha"] is None and "medir demanda" in " ".join(r3["avisos"]))
    # El veredicto nunca dice solo "oportunidad"
    chequeo("siempre dice qué falta medir", all("no es un producto todavía" in x["siguiente_paso"] for x in (r, r2, r3)))
    for mala in ((None, 10), (10, "abc"), (-5, 10)):
        try:
            analizar("x", mala[0], mala[1])
            fallos.append("conteo inválido %r: debía dar error" % (mala,))
        except ErrorDeEntrada:
            pass
        casos += 1
    try:
        analizar("x", 10, 10, ("XX",), "CO")
        fallos.append("país sin población: debía dar error")
    except ErrorDeEntrada:
        pass
    casos += 1
    for f in fallos:
        print("FALLA", f)
    print("AUTOPRUEBA %d de %d" % (casos - len(fallos), casos))
    return 1 if fallos else 0


def arg(bandera, defecto=None):
    if bandera not in sys.argv:
        return defecto
    i = sys.argv.index(bandera)
    if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
        raise ErrorDeEntrada("%s necesita un valor" % bandera)
    return sys.argv[i + 1]


def main():
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    try:
        if "--afuera" not in sys.argv or "--aqui" not in sys.argv:
            print(__doc__)
            sys.exit(2)
        m = arg("--muestra-aqui")
        muestra = None
        if m:
            try:
                muestra = json.load(open(m, encoding="utf-8"))
            except (OSError, ValueError) as e:
                raise ErrorDeEntrada("--muestra-aqui %s: %s" % (m, e))
        paises = tuple(x.strip().upper() for x in arg("--paises-afuera", "US,CA,GB").split(",") if x.strip())
        print(json.dumps(analizar(arg("--problema", "(sin nombre)"), arg("--afuera"), arg("--aqui"),
                                  paises, arg("--pais", "CO").upper(), muestra), ensure_ascii=False, indent=1))
    except ErrorDeEntrada as e:
        print("ERROR DE ENTRADA: %s" % e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print("ERROR: dato con forma inesperada (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
