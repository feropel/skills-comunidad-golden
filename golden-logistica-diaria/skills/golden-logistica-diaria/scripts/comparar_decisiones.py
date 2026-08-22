#!/usr/bin/env python3
"""Compara DOS corridas del motor pedido por pedido.

POR QUE EXISTE: se afirmo "cero pedidos cambian" tras corregir el factor de la tienda,
y era FALSO. El conteo agregado daba identico — 27 CAMBIAR antes y 27 despues — pero
por dentro un pedido habia cambiado de transportadora, y a peor: {CLIENTA_A} salia
asignada a una que le habia fallado 5 de 8 veces.

LA REGLA QUE NACIO DE AHI: **"no cambio nada" se prueba con diff por elemento, jamas
con el conteo.** Dos conjuntos del mismo tamaño pueden no tener nada en comun.

  python3 comparar_decisiones.py antes.json despues.json [--json salida.json]
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json


def accion(x):
    """LO QUE SE HACE con el pedido. Si esto cambia, cambia la operacion."""
    return (x.get("rec"), (x.get("elegida") or {}).get("t"))


def explicacion(x):
    """POR QUE se hace. Puede cambiar sin que cambie nada de lo que se hace."""
    return x.get("criterio")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("antes")
    ap.add_argument("despues")
    ap.add_argument("--json", help="escribe el diff a un archivo")
    a = ap.parse_args()

    A = {x["id"]: x for x in leer_json(a.antes)}
    B = {x["id"]: x for x in leer_json(a.despues)}

    solo_a = sorted(set(A) - set(B))
    solo_b = sorted(set(B) - set(A))
    comunes = sorted(set(A) & set(B))
    # Dos niveles, porque no son lo mismo: que cambie la ACCION mueve un paquete;
    # que cambie solo la EXPLICACION no mueve nada, pero avisa de que la regla que
    # decide es otra y eso puede esconder algo.
    dif = [i for i in comunes if accion(A[i]) != accion(B[i])]
    solo_expl = [i for i in comunes if accion(A[i]) == accion(B[i])
                 and explicacion(A[i]) != explicacion(B[i])]

    print(f"antes {len(A)} pedidos · despues {len(B)} · en ambos {len(comunes)}")
    if solo_a:
        print(f"  solo en la primera: {len(solo_a)} -> {solo_a[:8]}")
    if solo_b:
        print(f"  solo en la segunda: {len(solo_b)} -> {solo_b[:8]}")

    if not dif:
        print(f"\nCERO pedidos cambian de ACCION, verificado uno por uno sobre {len(comunes)}.")
    else:
        print(f"\n{len(dif)} pedidos CAMBIAN LO QUE SE HACE con ellos:\n")
        for i in dif:
            x, y = A[i], B[i]
            ta = (x.get("elegida") or {}).get("t")
            tb = (y.get("elegida") or {}).get("t")
            print(f"  {i} · {x.get('cliente','')[:22]} · {x.get('ciudad')}")
            print(f"      antes:   {x.get('rec')} -> {ta}  ({x.get('criterio')})")
            print(f"      despues: {y.get('rec')} -> {tb}  ({y.get('criterio')})")
            # la huella del cliente con cada una, que es donde se ve si el cambio es sano
            for c in (y.get("cands") or []):
                if c["t"] in (ta, tb):
                    hh = c.get("huella")
                    txt = (f"{hh['ent']}/{hh['n']} = {100*hh['ent']/hh['n']:.0f}%"
                           if hh else "sin historial")
                    print(f"        {c['t']:16s} costo ${c['costo']:,}  este cliente: {txt}")
            print()

    if solo_expl:
        print(f"\nOtros {len(solo_expl)} mantienen la misma accion pero la decide OTRA regla:")
        for i in solo_expl:
            print(f"  {i} · {A[i].get('cliente','')[:22]} · {A[i].get('ciudad')} · "
                  f"{explicacion(A[i])} -> {explicacion(B[i])} "
                  f"(sigue {accion(B[i])[0]} -> {accion(B[i])[1]})")
        print("\nEso no mueve ningun paquete, pero conviene mirarlo: si la regla que decide "
              "cambia, puede estar escondiendo un caso que antes se veia.")

    if a.json:
        escribir_json(a.json, {"antes": a.antes, "despues": a.despues,
                   "comunes": len(comunes),
                   "cambian_accion": len(dif), "ids_accion": dif,
                   "cambian_solo_explicacion": len(solo_expl), "ids_explicacion": solo_expl,
                   "detalle": [{"id": i, "antes": accion(A[i]) + (explicacion(A[i]),),
                                "despues": accion(B[i]) + (explicacion(B[i]),)}
                               for i in dif + solo_expl]},
                  )
        print(f"diff escrito en {a.json}")
    sys.exit(1 if dif else 0)


if __name__ == "__main__":
    main()
