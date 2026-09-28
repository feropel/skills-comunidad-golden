#!/usr/bin/env python3
"""Limpia el cache de productos del asistente de carritos ([Carritos IA] Información de productos #N).

POR QUE. El bot consulta ese cache antes de responder sobre un producto. Medido en un espacio
real (18-sep): 11 entradas de la busqueda web, sin fecha y con ids inventados en serie, que
describian la empresa con giros que no son suyos; mas entradas solo con una URL, vacias o con
"Nombre del producto: No disponible". Como el id ya existe, el webhook NUNCA las reescribe:
la basura se queda para siempre si nadie la quita.

Ademas, --quitar id1,id2 quita entradas que un HUMANO leyo y encontro FALSAS. La forma de una
entrada no dice si es verdad: medido 18-sep, entradas con fecha e id describian un producto
capilar como "promueve el cultivo" y una recarga de fibra como "servicio de recarga digital".
La maquina caza la forma; el contenido se lee a mano contra el catalogo.

Se QUITA una entrada sin fecha, sin id, vacia, solo-URL o "No disponible". Se REPARA una entrada
que quedo aplanada en la raiz del campo (fecha/id/info sueltas). Lo demas no se toca.
La busqueda web tiene que quedar APAGADA, o la basura vuelve.

Los campos de cache se DESCUBREN por prefijo (#1, #2, #3...). Antes se recorria una lista fija de
dos nombres: un cache #3 quedaba invisible y la corrida podia decir "el cache ya esta limpio"
mientras la auditoria lo marcaba con basura.

Uso:  python3 limpiar_cache_productos.py --token-file RUTA --tienda "Nombre" --respaldo-dir DIR
          [--quitar id1,id2] [--escribir]
      python3 limpiar_cache_productos.py --autoprueba   (no toca la red)
      (sin --escribir solo muestra lo que haria)
"""
import argparse
import datetime
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from chatea_api import Api, CAMPO, valor, campos_cache  # noqa: E402
from auditar_carritos import motivo_basura  # noqa: E402


SUELTAS = ("fecha", "id", "info")


def limpiar(v, quitar=()):
    """(limpio, lineas). Funcion PURA para poder tener banco de pruebas sin red.
    Las llaves sueltas de la raiz solo se funden en una entrada si estan las TRES; si hay solo
    una parte, se CONSERVAN y se dice, porque antes se borraban del servidor sin una sola linea."""
    limpio, lineas = {}, []
    sueltas = [k for k in SUELTAS if k in v]
    if len(sueltas) == len(SUELTAS):
        rid = str(v["id"])
        lineas.append(f"REPARA entrada aplanada en la raiz -> llave {rid}")
        limpio[rid] = {"fecha": v["fecha"], "id": rid, "info": v["info"]}
    elif sueltas:
        for k in sueltas:
            limpio[k] = v[k]
            lineas.append(f"CONSERVA la llave suelta '{k}' de la raiz: esta incompleta para armar "
                          f"una entrada y NO se borra")
    for k, e in v.items():
        if k in SUELTAS:
            continue
        m = "revisada a mano: contenido falso" if k in quitar else motivo_basura(e)
        if m:
            lineas.append(f"QUITA {k}: {m}")
        else:
            limpio[k] = e
    return limpio, lineas


def autoprueba():
    """Los dos sentidos: que quite la basura y que NO toque lo bueno."""
    corridas, fallos = [], []

    def check(t, ok, ev=""):
        corridas.append(t)
        print(f"  {'OK   ' if ok else 'FALLA'} · {t}")
        if not ok:
            fallos.append(t)
            print("        ", ev)

    bueno = {"1": {"fecha": "2026-09-01T10:00:00-05:00", "id": "1", "info": "Nombre: Producto Uno"}}
    limpio, lineas = limpiar(bueno)
    check("0 · cache sano no cambia ni dice nada (control negativo)",
          limpio == bueno and not lineas, f"{limpio} {lineas}")

    d = dict(bueno, x={"fecha": "", "id": "", "info": ""})
    limpio, lineas = limpiar(d)
    check("1 · entrada sin fecha ni id -> QUITA con su linea",
          "x" not in limpio and any(x.startswith("QUITA x") for x in lineas), f"{limpio} {lineas}")

    limpio, lineas = limpiar(dict(bueno), quitar={"1"})
    check("2 · --quitar saca la entrada que un humano leyo",
          limpio == {} and any("contenido falso" in x for x in lineas), f"{limpio} {lineas}")

    d = {"fecha": "2026-09-01T10:00:00-05:00", "id": "7", "info": "Nombre: Siete"}
    limpio, lineas = limpiar(d)
    check("3 · las TRES llaves sueltas se funden en una entrada",
          limpio == {"7": {"fecha": d["fecha"], "id": "7", "info": d["info"]}}, f"{limpio}")

    d = dict(bueno, id="9")
    limpio, lineas = limpiar(d)
    check("4 · una llave suelta INCOMPLETA se conserva y se nombra (antes se borraba callada)",
          limpio.get("id") == "9" and any("CONSERVA la llave suelta 'id'" in x for x in lineas),
          f"{limpio} {lineas}")

    d = dict(bueno, dos={"fecha": "2026-09-02T10:00:00-05:00", "id": "2", "info": "Fijador"})
    limpio, lineas = limpiar(d)
    check("5 · una info de UNA palabra no se toma por URL y no se borra",
          "dos" in limpio, f"{limpio} {lineas}")

    print(f"\n  COBERTURA: {len(corridas) - len(fallos)} de {len(corridas)} pruebas en verde")
    return 0 if not fallos else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token-file")
    p.add_argument("--tienda")
    p.add_argument("--respaldo-dir")
    p.add_argument("--autoprueba", action="store_true")
    p.add_argument("--escribir", action="store_true")
    p.add_argument("--quitar", default="", help="ids revisados a mano y encontrados falsos, separados por coma")
    a = p.parse_args()
    if a.autoprueba:
        sys.exit(autoprueba())
    for req in ("token_file", "tienda", "respaldo_dir"):
        if not getattr(a, req):
            p.error(f"falta --{req.replace('_', '-')}")

    api = Api(a.token_file)
    campos = api.campos()
    tienda = valor(campos[CAMPO]).get("datos_tienda", {}).get("nombre_tienda")
    if tienda != a.tienda:
        sys.exit(f"ABORTA: el espacio dice tienda={tienda!r}, se esperaba {a.tienda!r}")

    quitar = {x.strip() for x in a.quitar.split(",") if x.strip()}
    cache = campos_cache(campos)
    print(f"campos de cache descubiertos: {len(cache)} -> {', '.join(x[-2:] for x in cache) or 'ninguno'}")
    if not cache:
        print("este espacio no tiene campos de cache de productos: nada que limpiar")
        return
    nuevos, cambia = {}, False
    for c in cache:
        v = valor(campos[c]) or {}
        limpio, lineas = limpiar(v, quitar)
        for x in lineas:
            print(f"  {c[-2:]} {x}")
        print(f"{c}: {len(v)} llaves -> {len(limpio)} entradas")
        cambia |= limpio != v
        nuevos[c] = limpio

    if not cambia:
        print("el cache ya esta limpio")
        return
    if not a.escribir:
        print("modo muestra: no se escribio nada (pasar --escribir)")
        return

    os.makedirs(a.respaldo_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta = os.path.join(a.respaldo_dir, f"carritos-cache-ANTES-{ts}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({c: campos[c] for c in nuevos}, f, ensure_ascii=False, indent=2)
    print("respaldo:", ruta)
    api.escribir(nuevos)
    time.sleep(3)
    c2 = api.campos()
    ok = all(valor(c2[c]) == nuevos[c] for c in nuevos)
    intacta = valor(c2[CAMPO]) == valor(campos[CAMPO])
    print(f"VERIFICADO DEL SERVIDOR: cache {'igual' if ok else 'DIFIERE'} · config intacta: "
          f"{intacta} · cupo: {api.cupo}")
    sys.exit(0 if ok and intacta else 1)


if __name__ == "__main__":
    main()
