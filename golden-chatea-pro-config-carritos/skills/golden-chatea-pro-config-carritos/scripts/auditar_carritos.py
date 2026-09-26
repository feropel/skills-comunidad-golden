#!/usr/bin/env python3
"""AUDITORIA del asistente de carritos de un espacio, por API y SOLO LECTURA.

Mira lo que un humano no alcanza a mirar en el panel y lo reporta con cobertura:
  1. el campo [Carritos] Configuracion contra validar_config.py (llaves, topes UTF-16, doctrina)
  2. el ESTADO de las plantillas seleccionadas (existen y estan APPROVED). El CONTENIDO de las
     plantillas no se califica: no es configuracion (regla de FER, 18-sep).
  3. el nombre del asesor contra los asistentes hermanos (es UNO por espacio)
  4. el cache de productos: entradas basura que el webhook ya no va a reescribir
  5. la busqueda web: encendida, vuelve a meter basura al cache
  6. el cache contra el CATALOGO PUBLICO de la tienda (--dominio): producto que ya no existe o
     cuyo nombre no coincide con el titulo real. La forma no dice si el texto es verdad.
  7. la FRESCURA del cache: si la entrada mas nueva es vieja, el webhook puede estar mudo

Uso:  python3 auditar_carritos.py --token-file RUTA [--dominio tienda.com] [--dias 45]
          [--guardar respaldo.json]
Sale: 0 sin criticas · 1 hay criticas.
"""
import argparse
import datetime
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from chatea_api import Api, CAMPO, CACHE, valor  # noqa: E402
from validar_config import validar  # noqa: E402
from catalogo_tienda import catalogo, comparar, CatalogoVacio  # noqa: E402
from chatea_api import campos_cache  # noqa: E402


def motivo_basura(e):
    """Por que una entrada del cache de productos no sirve. None = sirve."""
    if not isinstance(e, dict):
        return "no es una entrada"
    info = str(e.get("info", "")).strip()
    if not e.get("fecha"):
        return "sin fecha (viene de la busqueda web)"
    if not str(e.get("id", "")).strip():
        return "sin id"
    if not info:
        return "info vacia"
    if re.fullmatch(r"https?://\S+|[\w.-]+\.\w{2,}/\S*", info):
        return "solo una URL"
    if re.search(r"nombre del producto:\s*no disponible", info, re.I):
        return "producto 'No disponible'"
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token-file", required=True)
    p.add_argument("--guardar", help="ruta donde dejar el respaldo del campo leido")
    p.add_argument("--dominio", help="dominio de la tienda Shopify para cruzar el cache con su catalogo")
    p.add_argument("--dias", type=int, default=45,
                   help="dias sin un producto nuevo en el cache que se consideran sospechosos")
    a = p.parse_args()

    api = Api(a.token_file)
    campos = api.campos()
    if CAMPO not in campos:
        print(f"🔴 el espacio no tiene {CAMPO}: el asistente de carritos no esta instalado")
        sys.exit(1)
    conf = valor(campos[CAMPO])
    if a.guardar:
        with open(a.guardar, "w", encoding="utf-8") as f:
            json.dump({n: campos[n] for n in [CAMPO] + CACHE if n in campos}, f,
                      ensure_ascii=False, indent=2)
        print("respaldo:", a.guardar)

    tienda = conf.get("datos_tienda", {}).get("nombre_tienda")
    print(f"ESPACIO: tienda = {tienda!r} · bot fields leidos: {len(campos)}"
          + (" · LECTURA PARCIAL" if getattr(api, "parcial", False) else ""))
    criticas, avisos = [], []
    parcial = getattr(api, "parcial", False)
    frentes = {"campo": True, "plantillas": False, "asesor": False, "cache": False,
               "busqueda_web": False, "catalogo": False, "frescura": False}

    # 1 · el campo
    anticipado_con_datos = bool(str(conf.get("datos_logisticos", {}).get("metodo_pago", {})
                                    .get("datos_pago_anticipado", "")).strip())
    c, v = validar(conf, dueno_confirmo=True)
    criticas += c
    avisos += v
    if anticipado_con_datos:
        avisos.append("datos_pago_anticipado trae contenido: confirmar con el DUEÑO que la cuenta "
                      "es suya (heredada de otro espacio manda el dinero a otra persona)")

    # 2 · plantillas: solo ESTADO
    try:
        meta = {t.get("name"): (t.get("status") or t.get("default_values", {}).get("status"))
                for t in api.plantillas()}
        sel = conf.get("mensajes_recuperacion", {}).get("carritos", {})
        for casilla, t in sel.items():
            n = t.get("name") if isinstance(t, dict) else None
            if not n:
                criticas.append(f"la casilla '{casilla}' no tiene plantilla seleccionada: ese paso "
                                f"no envia nada y el panel no avisa")
                continue
            if n not in meta:
                criticas.append(f"plantilla '{n}' ({casilla}) NO existe en la cuenta: ese paso no envia")
            elif meta[n] != "APPROVED":
                criticas.append(f"plantilla '{n}' ({casilla}) esta {meta[n]}: ese paso no envia")
        frentes["plantillas"] = True
        print(f"PLANTILLAS: {len(sel)} seleccionadas de {len(meta)} en la cuenta, revisado solo su estado")
    except Exception as e:  # noqa: BLE001
        avisos.append(f"no se pudo leer la lista de plantillas ({e}): estado SIN VERIFICAR")

    # 3 · nombre del asesor contra los hermanos
    propio = conf.get("identidad_asistente", {}).get("nombre_asesor", "")
    otros = set()
    # El nombre va en MAYUSCULA inicial: sin eso, "soy más directo" daba un asesor llamado "más".
    patron = re.compile(r"(?:Soy|soy|Eres|eres|Te llamas|te llamas)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}"
                        r"(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})?)")
    GENERICO = {"amable", "cercano", "cercana", "asesor", "asesora", "experto", "experta",
                "parte", "responsable", "bot"}
    # SOLO en las hojas de IDENTIDAD. Medido: buscar en todo el JSON traia nombres de EJEMPLOS de
    # mensajes de cliente ("soy María, vivo en Chapinero") y los reportaba como otro asesor.
    IDENTIDAD = ("nombre_asesor", "saludo", "rol", "identidad", "presentacion", "nombre_asistente")

    def hojas_identidad(o, ruta=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from hojas_identidad(v, f"{ruta}.{k}".lower())
        elif isinstance(o, str) and any(x in ruta for x in IDENTIDAD):
            yield o

    for n, f in campos.items():
        if n == CAMPO or "Configuracion" not in n.replace("ó", "o"):
            continue
        for texto in hojas_identidad(valor(f)):
            for x in patron.findall(texto):
                if x.split()[0].lower() not in GENERICO:
                    otros.add(x)
    prim = propio.split()[0].lower() if propio.split() else ""
    otros_prim = {x.split()[0].lower() for x in otros}
    if otros and prim and prim not in otros_prim:
        criticas.append(f"nombre_asesor '{propio}' no coincide con los hermanos {sorted(otros)}: "
                        f"el asesor es UNO por espacio")
    elif len(otros_prim) > 1:
        avisos.append(f"los hermanos se llaman distinto entre si {sorted(otros)}: revisar A MANO "
                      f"cual es el nombre real del espacio")
    frentes["asesor"] = bool(otros)
    if not otros:
        avisos.append("no se encontro el nombre del asesor en las hojas de identidad de los "
                      "hermanos: comparar A MANO")
    print(f"ASESOR: carritos={propio!r} · hermanos={sorted(otros) or 'no se encontro'}")

    # 4 · cache de productos
    basura = 0
    cache_campos = campos_cache(campos)
    for n in cache_campos:
        v = valor(campos[n]) or {}
        if isinstance(v, dict):
            if all(k in v for k in ("fecha", "id", "info")):
                basura += 1
            basura += sum(1 for k, e in v.items() if k not in ("fecha", "id", "info")
                          and motivo_basura(e))
    if basura:
        criticas.append(f"cache de productos con {basura} entradas basura: correr "
                        f"limpiar_cache_productos.py (el webhook no reescribe un id que ya existe)")
    frentes["cache"] = bool(cache_campos)
    if not cache_campos:
        avisos.append("este espacio no tiene campos de cache de productos: revisar A MANO en el panel")
    print(f"CACHE: {len(cache_campos)} campos · {basura} entradas basura por FORMA. El CONTENIDO se lee a mano contra el catalogo:")
    for n in cache_campos:
        for k, e in (valor(campos.get(n, {})) or {}).items():
            if isinstance(e, dict):
                print(f"   · {k} {str(e.get('fecha', ''))[:10]} | {str(e.get('info', '')).replace(chr(10), ' ')[:90]}")

    # 6 · el cache contra el catalogo real de la tienda
    entradas = {}
    for n in cache_campos:
        for k, e in (valor(campos.get(n, {})) or {}).items():
            if isinstance(e, dict):
                entradas[k] = e
    if a.dominio:
        try:
            cat, completo = catalogo(a.dominio)
            huerfanas, discrepantes, debiles, no_eval = comparar(entradas, cat)
            frentes["catalogo"] = True
            print(f"CATALOGO: {len(cat)} productos publicados · {len(huerfanas)} sin producto vivo · "
                  f"{len(discrepantes)} con nombre que no coincide · {len(debiles)} coincidencia "
                  f"debil · {len(no_eval)} no evaluables")
            if not completo:
                avisos.append("el catalogo se leyo hasta el tope de paginas: puede faltar producto, "
                              "asi que una 'huerfana' podria ser un falso positivo")
            if entradas and len(huerfanas) == len(entradas):
                avisos.append(f"TODAS las entradas salieron huerfanas: sospechar del dominio "
                              f"({a.dominio}) antes de tocar el cache")
            else:
                for k, nom in huerfanas:
                    avisos.append(f"cache {k} ('{nom[:40]}') no existe en el catalogo: producto "
                                  f"retirado o de otra tienda. Se quita con --quitar {k}")
            for k, nom, titulo, por in discrepantes:
                criticas.append(f"cache {k} dice '{nom[:40]}' y la tienda lo titula '{titulo[:40]}' "
                                f"({por}): el bot le describe al cliente otro producto")
            for k, nom, titulo in debiles:
                avisos.append(f"cache {k} ('{nom[:30]}') coincide poco con '{titulo[:30]}': leerlo")
            for k, por in no_eval:
                avisos.append(f"cache {k} no se pudo evaluar contra el catalogo ({por})")
        except CatalogoVacio as e:
            avisos.append(f"{e}: el cruce NO se hizo y el cache no queda acusado")
        except Exception as e:  # noqa: BLE001
            avisos.append(f"no se pudo leer el catalogo de {a.dominio} ({e}): cruce SIN hacer")
    else:
        avisos.append("sin --dominio: el cache NO se cruzo contra el catalogo de la tienda")

    # 7 · frescura: cuando entro el ultimo producto por el webhook
    fechas = sorted(str(e.get("fecha", ""))[:10] for e in entradas.values() if e.get("fecha"))
    if fechas:
        frentes["frescura"] = True
        ultima = fechas[-1]
        try:
            dias = (datetime.date.today() - datetime.date(*map(int, ultima.split("-")))).days
        except ValueError:
            frentes["frescura"] = False
            avisos.append(f"la fecha mas nueva del cache ('{ultima}') no es una fecha que se pueda "
                          f"leer: frescura SIN medir")
            dias = -1
        print(f"FRESCURA: ultimo producto cacheado el {ultima}"
              + (f" ({dias} dias)" if dias >= 0 else " (sin medir)"))
        if dias > a.dias:
            avisos.append(f"hace {dias} dias que no entra un producto nuevo al cache. No prueba que "
                          f"el webhook este mudo (un carrito de producto ya cacheado no deja rastro), "
                          f"pero si el cable se cayo, se ve asi. Comprobar con un carrito de prueba.")
    else:
        avisos.append("el cache no tiene fechas: no se puede medir si el webhook sigue entregando")

    # 5 · busqueda web
    bw_campo = campos.get("[Carritos IA] Habilitar búsqueda web")
    frentes["busqueda_web"] = bw_campo is not None
    if bw_campo is None:
        avisos.append("no existe el campo de busqueda web: verificar A MANO en el panel")
    elif str(bw_campo.get("value", "")).lower() in ("true", "1", "si"):
        avisos.append("busqueda web ENCENDIDA: vuelve a llenar el cache con descripciones genericas")

    print()
    for x in criticas:
        print("  🔴", x)
    for x in avisos:
        print("  🟠", x)
    if parcial:
        avisos.append("la lectura de bot fields se corto por tope de paginas: los frentes que "
                      "dependen de campos pueden estar incompletos")
    hechos = sum(frentes.values())
    faltan = [k for k, v in frentes.items() if not v]
    print(f"\nCOBERTURA: {hechos} de {len(frentes)} frentes verificados"
          + (f" (SIN verificar: {', '.join(faltan)})" if faltan else "")
          + f" · {len(criticas)} criticas · {len(avisos)} avisos"
          f" · cupo API restante: {api.cupo}")
    print("NO revisado aqui (se hace aparte): la conexion real de Shopify (compuerta del cuerpo) y "
          "una prueba con un carrito abandonado de verdad.")
    sys.exit(1 if criticas else 0)


if __name__ == "__main__":
    main()
