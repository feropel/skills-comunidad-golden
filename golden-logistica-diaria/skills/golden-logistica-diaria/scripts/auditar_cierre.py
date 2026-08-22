#!/usr/bin/env python3
"""Audita el REPORTE DE CIERRE contra el disco, reclamo por reclamo.

POR QUE EXISTE, y el caso es de la ronda 19: mi reporte de congelacion declaro tres
cosas cerradas que **no estaban en el disco**:
  · «prueba_cosecha.js citado 3 → 1» — seguian 2 citas
  · «los 3 no-cerrados quedan declarados» — cero apariciones en el estado final;
    estaban declarados EN EL MENSAJE, otra vez
  · «la seccion duplicada se elimina» — el `re.sub` buscaba un titulo que no existia:
    9.597 caracteres antes y despues, cirugia en el aire

LA CLASE: **un reporte de cierre ES un conjunto de afirmaciones**, y esta skill exige
que toda afirmacion se mida contra su artefacto. Esa exigencia no puede detenerse justo
en el documento donde digo que ya termine — que es, ademas, el que mas se lee y el que
nadie contrasta. Un "cerrado" sin comando y sin resultado es una opinion.

Cada reclamo se escribe como (que dije, comando, lo que tiene que dar). Si el disco no
lo respalda, NO SE CONGELA.

  python3 auditar_cierre.py            # corre los reclamos de la ronda actual
"""
import os, re, subprocess, sys

SK = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(SK)
FALLOS = []


def juzgar(reclamo, comando, ok, evidencia):
    print(f"  {'CUMPLE ' if ok else 'NO CUMPLE'}  {reclamo}")
    print(f"      $ {comando}")
    print(f"      -> {evidencia}")
    if not ok:
        FALLOS.append(reclamo)


def cuenta(patron, ruta):
    """Cuantas veces aparece `patron` en un archivo del paquete."""
    p = os.path.join(RAIZ, ruta)
    if not os.path.exists(p):
        return None
    return len(re.findall(patron, open(p, encoding="utf-8").read()))


def main():
    print("AUDITORIA DEL REPORTE DE CIERRE contra el disco\n")

    # --- los tres reclamos que la ronda 19 dio por cerrados y no lo estaban ---
    n = cuenta(r"prueba_cosecha\.js", "SKILL.md")
    juzgar("prueba_cosecha.js se cita UNA sola vez en SKILL.md",
           "grep -c 'prueba_cosecha.js' SKILL.md", n == 1, f"{n} citas")

    n = cuenta(r"pdfplumber", "SKILL.md")
    juzgar("los no-cerrados estan ESCRITOS en SKILL.md (no solo en el mensaje)",
           "grep -c 'pdfplumber' SKILL.md", (n or 0) >= 1, f"{n} apariciones")

    n = cuenta(r"sustituir_exigiendo", "scripts/informe_360.py")
    juzgar("la cirugia del duplicado ASEVERA que coincidio",
           "grep -c 'sustituir_exigiendo' scripts/informe_360.py",
           (n or 0) >= 2, f"{n} usos")

    # --- el alcance del verificador, DENTRO del artefacto ---
    n = cuenta(r"FUERA DE ALCANCE", "scripts/verificar_informe.py")
    juzgar("el alcance del verificador esta declarado DENTRO del script",
           "grep -c 'FUERA DE ALCANCE' scripts/verificar_informe.py",
           (n or 0) >= 1, f"{n} apariciones")

    # --- privacidad: cero datos de personas ---
    #
    # UN GUARDIA NO PUEDE SER SU PROPIO TESTIGO, y esta funcion lo fue de dos maneras
    # a la vez. Aqui vivian escritos, como literales, **el telefono real de una clienta
    # y tres nombres propios** — o sea: el detector de fugas de privacidad ERA la fuga.
    # GLD1.19 y 1.20 dejaron el telefono en cero; GLD1.21 lo reintrodujo dentro del
    # guardia y nadie lo vio.
    #
    # Y no se vio por una razon que da vertigo: el patron con frontera de palabra
    # `\b<numero>\b` **no casa en su propio archivo**, porque el caracter que precede al
    # numero es la letra `b` de
    # la secuencia `\b`, asi que la frontera de palabra nunca se cumple. El detector era
    # literalmente ciego a si mismo — no por descuido, sino por la forma del patron.
    #
    # DOS CORRECCIONES, y son de clase:
    #   1. Los patrones viven FUERA de la skill (`~/.golden/patrones-privacidad.txt`).
    #      Lo que se persigue no se escribe en el cuerpo del que persigue.
    #   2. El barrido INCLUYE este archivo en su universo. Un validador que se excluye
    #      del conjunto que valida da verde sobre si mismo por construccion.
    # Y si el archivo de patrones falta, esto MUERE: no poder comprobar la privacidad
    # no es lo mismo que estar limpio.
    PAT = os.path.expanduser("~/.golden/patrones-privacidad.txt")
    if not os.path.exists(PAT):
        print(f"NO SE PUEDE AUDITAR LA PRIVACIDAD: falta {PAT}\n"
              "  Ahi viven los patrones de datos personales, fuera de la skill a "
              "proposito.\n"
              "  Sin ese archivo no se sabe si hay fugas — y no saber no es estar limpio.",
              file=sys.stderr)
        sys.exit(1)
    patrones = [l.strip() for l in open(PAT, encoding="utf-8")
                if l.strip() and not l.startswith("#")]
    malos = []
    for r, _, fs in os.walk(RAIZ):
        if "__pycache__" in r:
            continue
        for f in fs:
            if not f.endswith((".py", ".js", ".md")):
                continue
            t = open(os.path.join(r, f), encoding="utf-8", errors="ignore").read()
            for pat in patrones:
                for m in re.findall(pat, t):
                    malos.append(f"{f}: {m}")
    juzgar("cero datos de personas reales en los archivos de la skill "
           "(este archivo incluido)",
           f"{len(patrones)} patrones de {PAT} sobre los .py/.js/.md",
           not malos, str(sorted(set(malos))[:6]) if malos else "limpio")

    # --- los bancos corren y pasan ---
    for banco in ("prueba_verificador.py", "prueba_denominador.py", "prueba_escritura.py",
                  "prueba_oficina.py", "prueba_torre.py",
                  "prueba_oficinas_inter.py", "prueba_ventana.py",
                  "prueba_contratos.py"):
        r = subprocess.run([sys.executable, os.path.join(SK, banco)],
                           capture_output=True, text=True, timeout=180)
        juzgar(f"{banco} pasa entero", f"python3 scripts/{banco}",
               r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[-1][:70])

    # --- EL RECLAMO DE COMPLETITUD, CON EL UNIVERSO SACADO DEL ARTEFACTO ---
    #
    # LA PRIMERA VERSION COMPARABA CONTRA UNA LISTA ESCRITA A MANO, y esa lista era el
    # punto ciego: tenia ocho entradas, el noveno pendiente que yo acababa de declarar
    # nunca entro, y esta comprobacion dijo **«8 de 8 CUMPLE»**. Fallo exactamente por
    # el motivo que ese pendiente describia — el flanco se demostro a si mismo en la
    # primera corrida del sistema que venia a vigilarlo, y el sistema dio verde.
    #
    # LA REGLA: **toda comprobacion de completitud extrae su universo DEL ARTEFACTO**,
    # jamas de una lista que alguien mantiene. Una lista refleja lo que su autor
    # recordaba el dia que la escribio, y lo que no recordaba es justo lo que hay que
    # vigilar. Aqui el universo son LAS FILAS de la tabla de pendientes de SKILL.md.
    #
    # Y SE PARSEAN FILAS, no se busca subcadena: una fila convertida en prosa seguiria
    # dando CUMPLE con un `in`. Una comprobacion que dice "fila" tiene que mirar filas.
    skill = open(os.path.join(RAIZ, "SKILL.md"), encoding="utf-8").read()
    # LA CABECERA SE RECONOCE POR SU SITIO, NO POR SU TEXTO.
    #
    # Aqui se excluia con `not celdas_f[0].startswith("**Qué")`: una exclusion escrita a
    # mano para UNA cabecera concreta. Medido el 2026-08-18: **2 de las 43 «filas con
    # estado» eran cabeceras** — «Prometido | Estado» y «Qué falta | Qué pasa hoy» —, y
    # colaban porque su segunda celda no esta vacia, asi que para el chequeo «toda fila
    # declara su estado» pasaban con nota. El conteo salia inflado y la comprobacion
    # daba verde sobre filas que ni siquiera son pendientes.
    #
    # ES LA MISMA CLASE QUE ESTE ARCHIVO YA PERSIGUE, aplicada a si mismo: una lista
    # escrita a mano refleja lo que su autor recordaba el dia que la escribio. La
    # cabecera de una tabla markdown es SIEMPRE la linea justo antes del separador
    # `| --- |`; eso es estructura, y ninguna cabecera nueva puede escaparse por venir
    # redactada distinta.
    filas, en_tabla, anterior = [], False, None
    lineas = skill.split("\n")
    for i, linea in enumerate(lineas):
        if linea.startswith("## "):
            en_tabla = "PENDIENTES DECLARADOS" in linea or "NO SE VERIFICA" in linea
            continue
        if not en_tabla or not linea.startswith("|"):
            continue
        if re.match(r"^\|[\s|:-]+\|?$", linea):
            continue
        siguiente = lineas[i + 1] if i + 1 < len(lineas) else ""
        if re.match(r"^\|[\s|:-]+\|?$", siguiente):
            continue          # es la cabecera: la delata el separador que viene detras
        celdas_f = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas_f) >= 2 and celdas_f[0]:
            filas.append(celdas_f)
    con_estado = [f for f in filas if len(f) >= 2 and f[1].strip()]
    juzgar("los pendientes salen de LAS FILAS de la tabla, no de una lista a mano",
           "parseo de las filas de PENDIENTES en SKILL.md",
           len(con_estado) >= 8, f"{len(con_estado)} filas con estado")
    sin_estado = [f[0][:40] for f in filas if len(f) < 2 or not f[1].strip()]
    juzgar("toda fila de pendiente declara su estado",
           "columna 2 de cada fila", not sin_estado, str(sin_estado) if sin_estado else "todas")
    # Y el pendiente que estreno la clase tiene que estar entre ellas.
    juzgar("el pendiente de la lista-a-mano existe como fila",
           "busqueda de la fila en la tabla parseada",
           any("LISTA escrita a mano" in f[0] for f in filas),
           "presente" if any("LISTA escrita a mano" in f[0] for f in filas) else "AUSENTE")

    print()
    if FALLOS:
        print(f"NO SE CONGELA · {len(FALLOS)} reclamos sin respaldo en el disco:")
        for f in FALLOS:
            print("  · " + f)
        sys.exit(1)
    print("todos los reclamos del cierre estan respaldados por el disco")


if __name__ == "__main__":
    main()
