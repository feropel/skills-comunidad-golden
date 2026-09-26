#!/usr/bin/env python3
"""
Centro de Transparencia de Google — anuncios activos de un anunciante, por PAIS.
Gratis, sin llave y sin cookies: llama al mismo RPC que usa su web.

POR QUE ESTE SCRIPT EXISTE Y NO UNA RECETA EN PROSA (G5.17/G5.18, 2026-09-08):
la receta escrita a mano invitaba a leer el tamano de la pagina como si fuera un conteo.
Cinco paises devolvieron "40" y el 40 era el limite pedido. Aqui un conteo o CIERRA (la
ultima pagina vino incompleta) o sale marcado "N+ (ABIERTO)". Un numero sin esa marca no
sale de aqui.

Y LA TRAMPA GEMELA, que nace de esa misma cura: DOS "N+" NO SE COMPARAN ENTRE SI. Dos
competidores en "100+" pueden ser 101 y 4.000. Un conteo abierto solo autoriza a decir
"al menos N": nunca ordena, nunca rankea, nunca mide saturacion de nicho. Para comparar
dos competidores hay que CERRAR los dos conteos, o no comparar.

LO QUE ESTA MEDIDO (2026-09-08):
  · El pais SI filtra: CO(2170) y ES(2724) sobre el mismo dominio, 0 ids en comun.
  · El tope del cuerpo manda: pediendo 40 llegan 40; pidiendo 100 llegan 100.
  · El offset NO pagina: repetir con offset 40 devuelve LOS MISMOS 40 ids. Por eso el
    conteo se cierra subiendo el TOPE, no avanzando un offset. La respuesta trae ademas un
    cursor en la clave "2" cuyo sitio en la peticion aun NO se descubrio (pendiente).
  · Cada anuncio trae PRIMERA y ULTIMA vez visto (claves 6 y 7, timestamps unix) → el
    TIEMPO ACTIVO, que es la senal de que un anuncio funciona: el que no se apaga, convierte.
  · `--buscar` busca ANUNCIANTES Y DOMINIOS, no palabras del anuncio: "faja reductora"
    devuelve 0 y "temu" devuelve la lista. Para un producto se entra por el dominio del
    competidor, no por el nombre del producto.
  · ⚠️ RATE LIMIT REAL: tras ~15 llamadas en pocos minutos, Google responde 302 y deja de
    servir. Este script espera entre llamadas y avisa. Si sale AUTO-BLOQUEO: parar, esperar
    y volver — insistir solo empeora el bloqueo.

Uso:
  python3 google_ads_transparency.py --buscar "temu" --pais CO
  python3 google_ads_transparency.py --dominio temu.com --pais CO --contar
  python3 google_ads_transparency.py --dominio temu.com --paises CO,MX,CL --json salida.json
  python3 google_ads_transparency.py --parsear respuesta.json     # sin red, para probar
"""
import argparse, json, subprocess, sys, time, datetime as dt

RPC = "https://adstransparency.google.com/anji/_/rpc/SearchService/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
PAUSA = 4  # segundos entre llamadas: barato contra el 302

# Criterios geograficos de Google Ads. ✔ = respuesta real medida el 2026-09-08.
PAISES = {"CO": 2170, "MX": 2484, "AR": 2032, "CL": 2152, "ES": 2724,      # ✔ los cinco
          "PE": 2604, "EC": 2218, "PA": 2591, "GT": 2320, "CR": 2188,
          "DO": 2214, "BO": 2068, "PY": 2600, "UY": 2858, "VE": 2862,
          "BR": 2076, "US": 2840, "PT": 2620, "IT": 2380, "FR": 2250}


class Bloqueado(RuntimeError):
    """Google dejo de servir (302 o cuerpo vacio): auto-bloqueo por ritmo."""


def _post(metodo, freq):
    r = subprocess.run(
        ["curl", "-s", "--compressed", "--max-time", "40", "-A", UA, "-w", "\n@@%{http_code}",
         "-X", "POST", RPC + metodo + "?authuser=",
         "-H", "Content-Type: application/x-www-form-urlencoded;charset=UTF-8",
         "--data-urlencode", "f.req=" + json.dumps(freq, separators=(",", ":"))],
        capture_output=True, timeout=60)
    bruto = r.stdout.decode("utf-8", errors="replace")
    cuerpo, _, code = bruto.rpartition("\n@@")
    if code.startswith("3") or not cuerpo.strip():
        raise Bloqueado(f"Google no sirvio (HTTP {code or '?'}). AUTO-BLOQUEO por ritmo: "
                        "esperar unos minutos y repetir. No insistir en bucle.")
    try:
        d = json.loads(cuerpo)
    except json.JSONDecodeError:
        raise RuntimeError("respuesta no es JSON: " + cuerpo[:160])
    # Error del propio RPC: trae texto de excepcion y NINGUNA lista de resultados.
    if "1" not in d and isinstance(d.get("2"), str) and "Exception" in d.get("2", ""):
        raise RuntimeError(f"el RPC rechazo la peticion: {d['2'][:140]}")
    return d


def _fecha(campo):
    try:
        return dt.datetime.fromtimestamp(int(campo["1"]))
    except Exception:
        return None


def parsear_creativos(d):
    """Convierte la respuesta cruda en piezas legibles. Funcion PURA: se prueba sin red."""
    piezas = []
    for a in d.get("1", []):
        desde, hasta = _fecha(a.get("6") or {}), _fecha(a.get("7") or {})
        dias = round((hasta - desde).total_seconds() / 86400, 1) if desde and hasta else None
        piezas.append({
            "id": a.get("2"),
            "anunciante": a.get("12"),
            "anunciante_id": a.get("1"),
            "dominio": a.get("14"),
            "primera_vez": desde.strftime("%Y-%m-%d") if desde else None,
            "ultima_vez": hasta.strftime("%Y-%m-%d") if hasta else None,
            "dias_activo": dias,
        })
    return piezas


def anunciantes(termino, pais):
    d = _post("SearchSuggestions", {"1": termino, "2": 10, "3": 10, "4": [pais], "5": {"1": 1}})
    out = []
    for it in d.get("1", []):
        if "1" in it:
            a = it["1"]
            out.append({"tipo": "anunciante", "nombre": a.get("1"), "id": a.get("2"),
                        "pais_registro": a.get("3")})
        elif "2" in it:
            out.append({"tipo": "dominio", "nombre": it["2"].get("1")})
    return out


def creativos(dominio, pais, tope):
    d = _post("SearchCreatives",
              {"2": tope, "3": {"8": [pais], "12": {"1": dominio, "2": True}},
               "7": {"1": 1, "2": 0, "3": pais}})
    return parsear_creativos(d)


def contar(dominio, pais, escalones=(40, 100, 250, 600)):
    """
    Cuenta subiendo el TOPE (el offset no pagina, medido). Cierra cuando una pagina vuelve
    incompleta: esa es la unica prueba de que se vio todo.
    """
    piezas = []
    for i, tope in enumerate(escalones):
        if i:
            time.sleep(PAUSA)
        piezas = creativos(dominio, pais, tope)
        if len(piezas) < tope:
            return {"total": len(piezas), "cerrado": True, "tope_usado": tope, "piezas": piezas}
    return {"total": len(piezas), "cerrado": False, "tope_usado": escalones[-1], "piezas": piezas}


def resolver(p):
    if p.upper() in PAISES:
        return PAISES[p.upper()], p.upper()
    if p.isdigit():
        return int(p), p
    sys.exit(f"pais '{p}' desconocido. Conocidos: {', '.join(sorted(PAISES))}, o el numero de Google.")


def imprimir(nombre, cod, dominio, r):
    if r["cerrado"]:
        cabeza = f"{r['total']} creativos activos"
    else:
        cabeza = (f"{r['total']}+ creativos — ⚠️ CONTEO ABIERTO: la pagina vino llena al tope "
                  f"{r['tope_usado']}, NO es un total. Vale como 'AL MENOS {r['total']}' y NADA mas: "
                  "no lo compares con otro abierto ni lo uses como saturacion del nicho")
    print(f"\n{nombre} ({cod}) · {dominio}: {cabeza}")
    vivos = [p for p in r["piezas"] if p["dias_activo"] is not None]
    if vivos:
        vivos.sort(key=lambda p: p["dias_activo"], reverse=True)
        print("   los que mas llevan corriendo (el que no se apaga, convierte):")
        for p in vivos[:5]:
            print(f"     {p['dias_activo']:>6} dias  {p['primera_vez']} → {p['ultima_vez']}  {p['id']}")
    if r["piezas"]:
        p = r["piezas"][0]
        print(f"   ver una pieza: https://adstransparency.google.com/advertiser/"
              f"{p['anunciante_id']}/creative/{p['id']}?region={nombre}")


def main():
    ap = argparse.ArgumentParser(description="Anuncios activos de Google por pais (gratis, sin llave).")
    ap.add_argument("--buscar", help="nombre de MARCA o DOMINIO (no sirve el nombre del producto)")
    ap.add_argument("--dominio", help="dominio o id de anunciante del que listar creativos")
    ap.add_argument("--pais", default="CO")
    ap.add_argument("--paises", help="lista separada por comas: barrido pais por pais")
    ap.add_argument("--contar", action="store_true", help="subir el tope hasta cerrar el conteo")
    ap.add_argument("--tope", type=int, default=40)
    ap.add_argument("--json", help="volcar el resultado a un archivo")
    ap.add_argument("--parsear", help="leer una respuesta cruda de disco y parsearla (sin red)")
    a = ap.parse_args()

    if a.parsear:
        cruda = json.load(open(a.parsear, encoding="utf-8"))
        if "1" not in cruda:
            # Un archivo de ERROR no puede leerse como "cero anuncios": son cosas distintas.
            print("🔴 el archivo NO trae lista de resultados (clave '1'). "
                  f"Parece una respuesta de error o de muro: {str(cruda)[:120]}")
            return
        piezas = parsear_creativos(cruda)
        print(f"parseadas {len(piezas)} piezas del archivo")
        for p in piezas[:5]:
            print(f"   {p['id']}  {p['anunciante']}  {p['primera_vez']}→{p['ultima_vez']}  "
                  f"{p['dias_activo']} dias")
        return

    if not a.buscar and not a.dominio:
        ap.error("hace falta --buscar o --dominio")

    objetivo = [resolver(x) for x in (a.paises.split(",") if a.paises else [a.pais])]
    salida = {}
    for i, (cod, nombre) in enumerate(objetivo):
        if i:
            time.sleep(PAUSA)
        try:
            if a.buscar:
                r = anunciantes(a.buscar, cod)
                print(f"\n{nombre} ({cod}) · '{a.buscar}': {len(r)} coincidencias"
                      + ("   (recuerda: busca MARCAS y DOMINIOS, no nombres de producto)" if not r else ""))
                for x in r:
                    print(f"   {x['tipo']:11} {x['nombre']}" + (f"  [{x['id']}]" if x.get("id") else ""))
                salida[nombre] = r
            else:
                if a.contar:
                    r = contar(a.dominio, cod)
                else:
                    piezas = creativos(a.dominio, cod, a.tope)
                    r = {"total": len(piezas), "cerrado": len(piezas) < a.tope,
                         "tope_usado": a.tope, "piezas": piezas}
                imprimir(nombre, cod, a.dominio, r)
                salida[nombre] = r
        except Bloqueado as e:
            print(f"\n{nombre} ({cod}): 🔴 {e}")
            salida[nombre] = {"error": "auto-bloqueo"}
            break
        except RuntimeError as e:
            print(f"\n{nombre} ({cod}): NO OBTENIDO — {e}")
            salida[nombre] = {"error": str(e)}

    abiertos = [k for k, v in salida.items()
                if isinstance(v, dict) and v.get("cerrado") is False]
    if len(abiertos) > 1:
        print(f"\n🚨 {len(abiertos)} conteos quedaron ABIERTOS ({', '.join(abiertos)}): "
              "NO los compares entre si ni los ordenes — dos '100+' pueden ser 101 y 4.000. "
              "Para comparar, cierra los dos.")

    if a.json:
        json.dump(salida, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\nvolcado a {a.json}")


if __name__ == "__main__":
    main()
