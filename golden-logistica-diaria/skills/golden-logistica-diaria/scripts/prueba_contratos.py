#!/usr/bin/env python3
"""Banco de los CONTRATOS entre piezas: la forma de los insumos y los nombres de salida.

TRES DEFECTOS REALES, reportados por LOGISTICA GOLDEN tras su corrida del 2026-08-18 y
verificados linea por linea. Los tres son de la misma familia — **no fallan al calcular,
fallan al entenderse entre piezas** — y por eso ninguno lo caza un banco de logica:

  1. El universo de contactos venia como `data` = **diccionario ns->contacto**, y el
     lector hacia `_u.get("contactos") or _u.get("data") or []`. Un dict no es falso,
     asi que pasaba el `or`; despues se iteraba y un dict devuelve **las claves**, o sea
     cadenas. Moria con `AttributeError: 'str' object has no attribute 'get'` a tres
     funciones de distancia de la causa. **Un `or` encadenado no valida: elige el
     primero que no sea falso.**

  2. `cruzar()` devolvia `campos_contradictorios` (un int) y `banderas` (la lista), y
     NADA llamado `contradictorios`. Quien leyera `X["contradictorios"]` obtenia `[]`
     mientras el conteo decia 2. **No es un error de calculo: es una trampa de nombres**,
     y ya mordio a un integrador.

  3. `fallos_barrido` venia recortada a 20 con el total aparte. Quien hiciera
     `len(fallos_barrido)` publicaba **20 cuando eran 64**. La lista recortada usada como
     total, otra vez — ahora el nombre grita que es una muestra.

  python3 prueba_contratos.py
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analizar_conversaciones import _universo_como_lista   # noqa: E402
from cruzar_chat_orden import cruzar                        # noqa: E402
from comun import recortar                                  # noqa: E402

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


C1 = {"id": 1, "phone": "3001112233"}
C2 = {"id": 2, "phone": "3004445566"}


def main():
    print("banco de los contratos entre piezas\n")

    # ---- 1 · EL UNIVERSO, EN SUS TRES FORMAS REALES ----
    juzgar("universo como LISTA pelada",
           _universo_como_lista([C1, C2], "x.json") == [C1, C2])
    juzgar("universo con 'contactos' como lista",
           _universo_como_lista({"contactos": [C1, C2]}, "x.json") == [C1, C2])
    # ESTE ES EL QUE MATABA: `data` como diccionario ns->contacto.
    d = _universo_como_lista({"data": {"ns_a": C1, "ns_b": C2}}, "x.json")
    juzgar("universo con 'data' como DICCIONARIO ns->contacto (el que mataba)",
           d == [C1, C2], str(d)[:60])
    juzgar("y devuelve CONTACTOS, no las claves",
           all(isinstance(x, dict) for x in d), str([type(x).__name__ for x in d]))
    juzgar("universo con 'subscribers'",
           _universo_como_lista({"subscribers": [C1]}, "x.json") == [C1])

    # ---- Y LO QUE NO SE ENTIENDE MUERE HABLANDO, no tres funciones despues ----
    for basura, que in (({"otra_cosa": [C1]}, "objeto con otra clave"),
                        ("una cadena", "una cadena"),
                        ({"data": ["no", "son", "contactos"]}, "lista de cadenas"),
                        (None, "nulo")):
        cod = ("import sys; sys.path.insert(0, %r); "
               "from analizar_conversaciones import _universo_como_lista as f; "
               "f(%r, 'EL-ARCHIVO.json')" % (os.path.dirname(os.path.abspath(__file__)), basura))
        r = subprocess.run([sys.executable, "-c", cod], capture_output=True, text=True, timeout=60)
        sal = (r.stdout or "") + (r.stderr or "")
        juzgar(f"basura ({que}) muere nombrando el archivo",
               r.returncode != 0 and "EL-ARCHIVO.json" in sal,
               sal.strip().splitlines()[-1][:60] if sal.strip() else "sin salida")
        juzgar(f"basura ({que}) NO muere con AttributeError crudo",
               "AttributeError" not in sal)

    # ---- 2 · CONTEO Y LISTA, CON LA MISMA CONVENCION ----
    # `cruzar` recibe DOS LISTAS. La primera version de este caso le pasaba los
    # contactos como diccionario por telefono y murio con el MISMO AttributeError que
    # el defecto 1 — la trampa de forma es tan facil de pisar que la pise escribiendo
    # su propio banco. Queda anotado: no es torpeza, es que la firma no se defiende.
    ORD = [{"id": 9, "phone": "3001112233", "status": "PENDIENTE",
            "lineas": [{"nombre": "Bolso Negro", "cantidad": 1}]}]
    CH = [{"phone": "3001112233",
           "user_fields": [{"name": "Productos escogidos", "value": "2 Bolso Rojo"},
                           # El campo dice 5 y el texto dice 2: los campos del chat se
                           # PELEAN entre si, que es lo unico que levanta una bandera.
                           # La primera version de este caso no producia ninguna, asi
                           # que comparaba 0 contra 0 — un banco que no puede fallar no
                           # prueba nada, y este existe justo para cazar que el conteo y
                           # la lista se separen.
                           {"name": "Cantidad de productos", "value": "5"}]}]
    out = cruzar(ORD, CH)
    juzgar("cruzar() expone 'contradictorios' como LISTA",
           isinstance(out.get("contradictorios"), list), type(out.get("contradictorios")).__name__)
    juzgar("y 'n_contradictorios' como numero",
           isinstance(out.get("n_contradictorios"), int), type(out.get("n_contradictorios")).__name__)
    juzgar("el conteo y el largo de la lista COINCIDEN",
           out["n_contradictorios"] == len(out["contradictorios"]),
           f"{out['n_contradictorios']} contra {len(out['contradictorios'])}")
    juzgar("y el nombre viejo sigue vivo para los consumidores que ya existen",
           out.get("campos_contradictorios") == out["n_contradictorios"])

    # ---- 3 · LA MUESTRA SE LLAMA MUESTRA ----
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analizar_conversaciones.py")
    src = open(p, encoding="utf-8").read()
    juzgar("la salida ya no se llama 'fallos_barrido' a secas",
           '"fallos_barrido"' not in src)
    juzgar("se llama 'muestra_fallos_barrido'", '"muestra_fallos_barrido"' in src)
    juzgar("y el total sigue publicandose aparte", '"n_fallos_barrido"' in src)


    # ---- 4 · EL RECORTE QUE SE DECLARA SOLO ----
    #
    # Barrido propio del 2026-08-18: la skill tenia CUATRO tablas que recortaban filas y
    # **dos declaraban el corte y dos no**. «Clientes potenciales sin cerrar» imprimia 20
    # filas de una lista mas larga sin decirlo en ninguna parte. No es un fallo de
    # calculo: es un numero arriba y otro abajo sin nada que explique la diferencia, y en
    # ese hueco caben dos lecturas —«hay mas» y «se filtraron»— que llevan a acciones
    # distintas.
    #
    # LA CORRECCION VA A LA CLASE: el recorte y su nota salen de la MISMA llamada, asi
    # que ya nadie puede recortar sin declararlo. Dos de cuatro se olvidaron cuando
    # declararlo era un renglon aparte.
    vis, nota = recortar(list(range(50)), 20)
    juzgar("recorta a 20 y DECLARA el total", len(vis) == 20 and "de **50**" in nota, nota)
    vis, nota = recortar(list(range(20)), 20)
    juzgar("si cabe entero no recorta y no inventa una nota", len(vis) == 20 and nota == "", repr(nota))
    vis, nota = recortar([], 20)
    juzgar("lista vacia: ni recorte ni nota", vis == [] and nota == "")
    juzgar("y la nota lleva el TOPE y el TOTAL, no solo uno",
           "20" in recortar(list(range(99)), 20)[1] and "99" in recortar(list(range(99)), 20)[1])

    # NINGUNA TABLA PUEDE VOLVER A RECORTAR A MANO. Este es el chequeo que impide que
    # la clase renazca en la proxima tabla que alguien escriba.
    for f in ("informe_360.py", "generar_informe_diario.py"):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f),
                   encoding="utf-8").read()
        import re as _re
        crudos = _re.findall(r"for \w+ in [^\n]*\[:\s*\d+\s*\]:", src)
        juzgar(f"{f}: ningun bucle recorta filas a mano", not crudos, str(crudos)[:70])


    # ---- 5 · LA PUERTA DE `--chats`, QUE SE HABIA QUEDADO SIN COMPUERTA ----
    #
    # Encontrado el 2026-08-19 CORRIENDO EL RUNBOOK paso a paso, no leyendo codigo: el
    # paso 5 murio con `TypeError: list indices must be integers` en `CH["chats"]`.
    # Lo grave no es el fallo: es que **la compuerta para esta misma clase se habia
    # escrito el dia anterior** para `--contactos-universo` y se aplico a UNA puerta.
    # De las cuatro entradas del script, dos tenian compuerta, una a medias y esta
    # ninguna. Arreglar una entrada y no su familia es como no arreglarla.
    import subprocess as _sp
    _aqui = os.path.dirname(os.path.abspath(__file__))
    _tmp = tempfile.mkdtemp()

    def _j(nombre, dato):
        r = os.path.join(_tmp, nombre)
        json.dump(dato, open(r, "w"))
        return r

    _dropi = _j("d.json", {"cosecha_completa": True, "ordenes": [], "accionables": []})
    _cont = _j("c.json", [C1])
    for mal, que in ((["no", "soy", "chats"], "una lista"),
                     ({"otra": {}}, "objeto sin 'chats'"),
                     ({"chats": []}, "'chats' como lista en vez de diccionario")):
        _mal = _j("mal.json", mal)
        r = _sp.run([sys.executable, os.path.join(_aqui, "analizar_conversaciones.py"),
                     "--chats", _mal, "--contactos", _cont, "--dropi", _dropi,
                     "--salida", os.path.join(_tmp, "out.json")],
                    capture_output=True, text=True, timeout=60)
        sal = (r.stdout or "") + (r.stderr or "")
        juzgar(f"--chats con {que}: muere nombrando el archivo",
               r.returncode != 0 and _mal in sal,
               sal.strip().splitlines()[-1][:58] if sal.strip() else "sin salida")
        juzgar(f"--chats con {que}: NO muere con TypeError crudo",
               "TypeError" not in sal and "KeyError" not in sal)

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + "; ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas de los contratos pasaron")


if __name__ == "__main__":
    main()
