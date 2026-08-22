#!/usr/bin/env python3
"""Banco de la escritura atomica. Prueba QUE QUEDA EN DISCO SI EL CODIGO NO TERMINA.

Esa es la pregunta que ningun otro banco de esta skill hacia. Los demas comprueban
que hace el codigo **cuando termina**; este mata la escritura a la mitad y mira el
disco. La formulacion es del chat LOGISTICA DOLCE, que lo reporto despues de perder
datos con el comando que esta misma fabrica habia recomendado.

  python3 prueba_escritura.py
"""
import json, os, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import escritura as E

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def sobrantes(carpeta):
    return [f for f in os.listdir(carpeta) if f.startswith(".tmp-")]


def main():
    print("banco de la escritura atomica\n")

    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "dato.json")

        # 1 · escribe bien lo normal
        E.escribir_json(ruta, {"v": 1})
        juzgar("escribe y se lee", json.load(open(ruta)) == {"v": 1})

        # 2 · LA PRUEBA DE LA CLASE: muere a media escritura
        #     El escritor revienta despues de haber escrito algo al temporal.
        def a_medias(f):
            f.write('{"v": 2, "a med')
            raise RuntimeError("el proceso se murio escribiendo")

        try:
            E._escribir(ruta, a_medias)
        except RuntimeError:
            pass
        vivo = None
        try:
            vivo = json.load(open(ruta))
        except Exception as e:
            vivo = f"CORRUPTO: {type(e).__name__}"
        juzgar("muerte a media escritura: el archivo ANTERIOR sigue intacto",
               vivo == {"v": 1}, f"quedo {vivo}")
        juzgar("muerte a media escritura: no deja basura", not sobrantes(d),
               f"sobrantes {sobrantes(d)}")

        # 3 · el destino nunca existe a medias: o viejo entero o nuevo entero
        E.escribir_json(ruta, {"v": 3})
        juzgar("tras una muerte, la siguiente escritura si entra",
               json.load(open(ruta)) == {"v": 3})

        # 4 · texto igual que json
        t = os.path.join(d, "informe.md")
        E.escribir_texto(t, "hola")
        def texto_a_medias(f):
            f.write("mitad")
            raise RuntimeError("corte")
        try:
            E._escribir(t, texto_a_medias)
        except RuntimeError:
            pass
        juzgar("texto: el anterior sobrevive al corte", open(t).read() == "hola",
               repr(open(t).read()))

        # 5 · el temporal vive en el MISMO directorio (si no, replace no es atomico)
        # El temporal tiene que nacer en el MISMO directorio que el destino: si cae
        # en otro sistema de archivos, os.replace deja de ser atomico y vuelve a
        # existir la ventana en la que el archivo esta a medias.
        sub = os.path.join(d, "sub")
        visto = {}
        def espia(f):
            visto["tmps"] = sobrantes(sub)
            f.write("x")
        E._escribir(os.path.join(sub, "x.txt"), espia)
        juzgar("el temporal se crea en el directorio del destino",
               len(visto.get("tmps") or []) == 1, str(visto.get("tmps")))

        # 6 · salida == insumo se rechaza ANTES de tocar nada
        murio = False
        try:
            E.exigir_salida_distinta(ruta, ruta)
        except SystemExit:
            murio = True
        juzgar("salida == insumo: muere antes de escribir", murio)
        juzgar("y el archivo sigue ahi", json.load(open(ruta)) == {"v": 3})
        murio2 = False
        try:
            E.exigir_salida_distinta(ruta, os.path.join(d, "otro.json"), None)
        except SystemExit:
            murio2 = True
        juzgar("salida != insumo: deja pasar", not murio2)

    # ------------------------------------------------------------------
    # TODOS LOS SCRIPTS TIENEN QUE ARRANCAR COMO SCRIPT.
    # Nacio de un fallo real: al inyectar el import del helper, dos archivos
    # quedaron sin `sys` o sin `os` y reventaban al ejecutarlos. La regresion no
    # lo cazo porque probaba los modulos IMPORTANDOLOS desde otro proceso que si
    # los tenia — o sea, probaba una forma de uso que no es la que se usa.
    # (Este archivo se excluye a si mismo: la primera version se llamaba en bucle.)
    # ------------------------------------------------------------------
    print()
    aqui = os.path.dirname(os.path.abspath(__file__))
    import subprocess
    yo = os.path.basename(os.path.abspath(__file__))
    # `auditar_cierre.py` NO se corre aqui: es un ORQUESTADOR que ejecuta los bancos,
    # incluido este. Correrlo desde aqui produjo una recursion infinita — banco llama a
    # auditor, auditor llama a banco — que se colgo a los 120 segundos.
    # LA CLASE: **un comprobador que ejecuta "todos los scripts" tiene que excluir a los
    # que ejecutan comprobadores**, o el grafo se muerde la cola. Y el sintoma no es un
    # error: es que no termina nunca, que es la forma mas cara de fallar en una corrida
    # de las siete de la mañana.
    for f in sorted(x for x in os.listdir(aqui)
                    if x.endswith(".py") and x not in (yo, "auditar_cierre.py")):
        r = subprocess.run([sys.executable, os.path.join(aqui, f)],
                           capture_output=True, text=True, timeout=90)
        malo = any(e in (r.stdout + r.stderr)
                   for e in ("NameError", "ImportError", "SyntaxError", "ModuleNotFound"))
        juzgar(f"{f} arranca como script", not malo,
               (r.stdout + r.stderr).strip().splitlines()[-1][:70] if malo else "")

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + ", ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas de escritura atomica pasaron")


if __name__ == "__main__":
    main()
