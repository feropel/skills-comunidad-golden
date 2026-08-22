#!/usr/bin/env python3
"""Banco de la VENTANA ACCIONABLE y de lo que todavia se puede reasignar.

DOS DEFECTOS REALES DEL CANONICO, medidos el 2026-08-17 sobre el volcado oficial de
Dolce (3.458 ordenes, `accionables: null`):

  1. `acc = set(D.get("accionables") or []); if acc:` — con `null` el filtro NO dispara
     y el informe barre la cuenta entera: **124 «direcciones malas», 120 de pedidos ya
     CERRADOS**. Con la ventana derivada por negacion: **4**.
     Y lo que hace este caso valioso de verdad: **dos fabricas midieron 124 y 2 con el
     MISMO codigo y ninguna mentia** — cada una uso un volcado distinto (el de navegador
     puebla `accionables`, el de API lo declara null). Cuando dos capas dan distinto, el
     tercer factor suele ser el insumo, no el codigo.

  2. La seccion de novedades proponia «pasar a otra transportadora» a pedidos que **ya
     habian despachado**: los 5 en NOVEDAD tenian guia y 3 llevaban esa instruccion.
     Dictado de FER: un informe que propone lo imposible **invita al error**.

LOS FIXTURES VAN SINTETICOS. El volcado real trae telefonos de clientas y no entra en la
skill; lo que este banco necesita es la FORMA (accionables null / poblado / vacio), no
las personas.

  python3 prueba_ventana.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import (ventana_accionable, se_puede_reasignar,   # noqa: E402
                   aviso_default_bodega)

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def volcado(accionables):
    """Mismo universo siempre: 3 vivos y 4 cerrados. Solo cambia como se declaran."""
    ords = [{"id": 1, "status": "PENDIENTE"}, {"id": 2, "status": "NOVEDAD"},
            {"id": 3, "status": "GUIA_GENERADA"}, {"id": 4, "status": "ENTREGADO"},
            {"id": 5, "status": "CANCELADO"}, {"id": 6, "status": "DEVOLUCION"},
            {"id": 7, "status": "RECHAZADO"}]
    return {"ordenes": ords, "accionables": accionables}


def main():
    print("banco de la ventana accionable y de la reasignacion\n")

    # ---- LOS TRES ESTADOS DEL CAMPO `accionables` ----
    ids, origen = ventana_accionable(volcado(None))
    juzgar("null -> se DERIVA por negacion, no se barre la cuenta",
           ids == {1, 2, 3}, f"{sorted(ids)} · {origen}")
    juzgar("y el origen lo DICE, para que el informe pueda declararlo",
           "DERIVADOS" in origen and "4 cerrados fuera" in origen, origen)

    ids, origen = ventana_accionable(volcado([]))
    juzgar("lista VACIA se trata igual que null (era el tercer caso)",
           ids == {1, 2, 3}, f"{sorted(ids)}")

    ids, origen = ventana_accionable(volcado([1, 2]))
    juzgar("lista poblada: se respeta lo que declara el volcado", ids == {1, 2})
    juzgar("y el origen dice que los declaro el volcado",
           "declarados por el volcado" in origen, origen)

    # EL CASO QUE PRUEBA QUE ESTO SIRVE: sin el arreglo, `null` devolvia TODO.
    ids, _ = ventana_accionable(volcado(None))
    juzgar("con null NO entran los cerrados (el defecto original)",
           not ({4, 5, 6, 7} & ids), f"colados: {sorted({4,5,6,7} & ids)}")

    # UN ESTADO QUE NADIE PREVIO CAE DEL LADO VISIBLE, no del silencioso.
    d = volcado(None); d["ordenes"].append({"id": 8, "status": "UN ESTADO NUEVO"})
    ids, _ = ventana_accionable(d)
    juzgar("un estado desconocido entra a la ventana (se ve, no se pierde)", 8 in ids)

    # ---- LO QUE YA NO SE REASIGNA ----
    juzgar("sin guia: se cambia", se_puede_reasignar({"status": "PENDIENTE"})[0])
    juzgar("guia recien generada: todavia se cambia",
           se_puede_reasignar({"status": "GUIA_GENERADA", "guia": "123"})[0])
    juzgar("preparado para transportadora: todavia se cambia",
           se_puede_reasignar({"status": "PREPARADO PARA TRANSPORTADORA", "guia": "1"})[0])

    # EL CASO DE FER, textual del canonico: NOVEDAD con guia -> jamas «pasar a X».
    ok, porque = se_puede_reasignar({"status": "NOVEDAD", "guia": "AB123"})
    juzgar("NOVEDAD con guia: NO se reasigna", not ok, porque)
    juzgar("y dice que hay que llamar", "llama" in porque, porque)

    for est in ("RECLAME EN OFICINA", "EN REPARTO", "EN TRANSITO", "DESPACHADA",
                "EN TERMINAL DESTINO", "INTENTO DE ENTREGA", "UN ESTADO NUEVO"):
        juzgar(f"{est} con guia: NO se reasigna",
               not se_puede_reasignar({"status": est, "guia": "X1"})[0])

    # El campo se llama `guia` en las decisiones y `guide` en el volcado. Las dos
    # familias lo nombran distinto, y olvidarse de una es el bug de siempre.
    juzgar("reconoce la guia venga como `guia` o como `guide`",
           not se_puede_reasignar({"status": "NOVEDAD", "guide": "X1"})[0])

    # ---- EL AVISO DEL DEFAULT DE BODEGA, Y SOBRE TODO QUE SE RETIRA SOLO ----
    #
    # El 2026-08-17 se escribieron 1.027 preferencias por municipio en la cuenta de
    # Golden. La skill no las lee, asi que en los 42 municipios donde el motor difiere,
    # el informe parece contradecir al panel. El aviso convierte esa contradiccion muda
    # en una advertencia declarada.
    #
    # LO QUE MAS IMPORTA PROBAR NO ES QUE APAREZCA: es que **DESAPAREZCA SOLO**. Un
    # aviso que sobrevive a su motivo es ruido, y el ruido no se va porque alguien se
    # acuerde de borrarlo — se va porque su condicion deja de cumplirse. Si esto se
    # hubiera atado a una fecha o a una bandera manual, seguiria ahi dentro de un ano.
    av = aviso_default_bodega({"tienda": "X"})
    juzgar("el aviso aparece cuando la skill NO lee el default", bool(av))
    juzgar("y nombra la fecha en que el default se escribio", "2026-08-17" in av)
    juzgar("y dice que una diferencia puede NO ser un error",
           "puede ser el default y no un error" in av)
    sin = aviso_default_bodega({"tienda": "X", "preferencia_municipio": "PREFERENCIAS.json"})
    juzgar("y DESAPARECE solo en cuanto el config declara que ya lo lee",
           sin == "", repr(sin)[:60])

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + "; ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas de la ventana accionable pasaron")


if __name__ == "__main__":
    main()
