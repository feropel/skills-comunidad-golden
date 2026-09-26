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

Uso:  python3 limpiar_cache_productos.py --token-file RUTA --tienda "Nombre" --respaldo-dir DIR [--escribir]
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
from chatea_api import Api, CAMPO, CACHE, valor  # noqa: E402
from auditar_carritos import motivo_basura  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token-file", required=True)
    p.add_argument("--tienda", required=True)
    p.add_argument("--respaldo-dir", required=True)
    p.add_argument("--escribir", action="store_true")
    p.add_argument("--quitar", default="", help="ids revisados a mano y encontrados falsos, separados por coma")
    a = p.parse_args()

    api = Api(a.token_file)
    campos = api.campos()
    tienda = valor(campos[CAMPO]).get("datos_tienda", {}).get("nombre_tienda")
    if tienda != a.tienda:
        sys.exit(f"ABORTA: el espacio dice tienda={tienda!r}, se esperaba {a.tienda!r}")

    quitar = {x.strip() for x in a.quitar.split(",") if x.strip()}
    nuevos, cambia = {}, False
    for c in CACHE:
        if c not in campos:
            continue
        v = valor(campos[c]) or {}
        limpio = {}
        if all(k in v for k in ("fecha", "id", "info")):
            rid = str(v["id"])
            print(f"  REPARA {c[-2:]}: entrada aplanada -> llave {rid}")
            limpio[rid] = {"fecha": v["fecha"], "id": rid, "info": v["info"]}
        for k, e in v.items():
            if k in ("fecha", "id", "info"):
                continue
            m = "revisada a mano: contenido falso" if k in quitar else motivo_basura(e)
            if m:
                print(f"  QUITA  {c[-2:]} {k}: {m}")
            else:
                limpio[k] = e
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
