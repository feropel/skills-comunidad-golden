#!/usr/bin/env python3
"""¿El banco de pruebas SIRVE? Un verde no lo demuestra.

Un banco también se verifica, y se verifica en DOS direcciones:

  A. TOLERA la redacción. Si alguien mejora el texto de un aviso sin tocar la
     conducta, el banco debe seguir en verde. Si se pone rojo, mide prosa.
  B. MUERDE el comportamiento. Si se rompe lo que el script HACE, el banco debe
     ponerse rojo. Si sigue verde, es decoración.

Por qué existe: el 2026-09-22 se midió que 9 de las pruebas de esta skill miraban
el texto de un mensaje, y tres de ellas con `not in`, que es el modo de fallo peor
— un `in` roto da rojo, que se ve; un `not in` roto da VERDE, que no se ve. Ya había
pasado antes: hasta el 06-sep dos pruebas comprobaban que se hubiera IMPRESO un
aviso, y pasaban en verde mientras el JSON salía con el pack de Colombia para
Argentina. Un banco que comprueba el mensaje certifica la intención, no la conducta.

Corre sobre una COPIA en un directorio temporal. Nunca toca la skill instalada.

Uso:  python3 contraprueba.py        exit 0 = el banco sirve
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

SKILL = pathlib.Path(__file__).resolve().parent.parent


def corre_banco(raiz):
    r = subprocess.run([sys.executable, str(raiz / "scripts" / "autoprueba.py")],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sustituye(ruta, viejo, nuevo):
    """Falla ruidosamente si el texto no está: un sabotaje que no sabotea nada
    haría pasar la contraprueba por la razón equivocada."""
    t = ruta.read_text(encoding="utf-8")
    if viejo not in t:
        sys.exit(f"ABORTA: no se encontró {viejo!r} en {ruta.name}. "
                 "El sabotaje no habría saboteado nada y la contraprueba mentiría.")
    ruta.write_text(t.replace(viejo, nuevo), encoding="utf-8")


fallos = []


def paso(n, nombre, cond, detalle=""):
    print(f"[{'OK  ' if cond else 'FALLA'}] {n}. {nombre}" + (f"  ·  {detalle}" if detalle else ""))
    if not cond:
        fallos.append(nombre)


print("=" * 68)
print("CONTRAPRUEBA · ¿el banco mide conducta o redacción?")
print("=" * 68)

with tempfile.TemporaryDirectory() as tmp:
    base = pathlib.Path(tmp) / "skill"
    shutil.copytree(SKILL, base)
    for f in base.rglob("*"):
        if f.is_file():
            f.chmod(0o644)

    # ---------- A. la copia intacta pasa ----------
    rc, out = corre_banco(base)
    total = out.rsplit("RESULTADO:", 1)[-1].strip().splitlines()[0] if "RESULTADO:" in out else "?"
    paso(1, "La copia intacta pasa el banco", rc == 0, total)
    if rc != 0:
        sys.exit("Sin una copia verde no se puede medir nada más.")

    # ---------- B. TOLERA que se reescriba la redacción ----------
    # Se cambian dos textos de aviso SIN tocar lo que el script hace.
    bc = base / "scripts" / "build_config.py"
    sustituye(bc, "AVISO: la palabra despectiva local de",
                  "OJO: el termino despectivo local de")
    sustituye(bc, "ERROR: la via NO VIP fue derogada",
                  "ERROR: ese modo ya no existe")
    rc_red, out_red = corre_banco(base)
    total_red = (out_red.rsplit("RESULTADO:", 1)[-1].strip().splitlines()[0]
                 if "RESULTADO:" in out_red else "?")
    paso(2, "TOLERA que se reescriba la redacción de los avisos",
         rc_red == 0, total_red if rc_red == 0 else "se puso rojo: mide prosa, no conducta")

    # ---------- C. MUERDE cuando se rompe la conducta ----------
    # Sabotaje real: que el pack de direcciones de CUALQUIER país devuelva el de
    # Colombia. Es el fallo que de verdad llegó a producción en septiembre, y manda
    # direcciones no entregables sin dar un solo error.
    shutil.rmtree(base)
    shutil.copytree(SKILL, base)
    for f in base.rglob("*"):
        if f.is_file():
            f.chmod(0o644)
    # 🔴 EL SABOTAJE TIENE QUE SABOTEAR DE VERDAD, y esto costó un intento.
    # El primero envolvía DATOS_POR_PAIS en un defaultdict, y NO cambiaba nada: el
    # script decide con `clave in DATOS_POR_PAIS`, y en un defaultdict una clave que
    # nunca se insertó sigue sin pertenecer. El banco se quedó verde y tenía razón.
    # Un sabotaje que no sabotea acusa al banco de un fallo que no tiene.
    # Este otro sí muerde: reintroduce el fallo REAL de septiembre — un país sin pack
    # cae al de Colombia en vez de negarse, y sale con "Barrio; Ciudad; Departamento"
    # para Argentina, donde no hay departamentos. No da error: da direcciones malas.
    bc = base / "scripts" / "build_config.py"
    sustituye(bc,
              "    if clave in DATOS_POR_PAIS:\n        return DATOS_POR_PAIS[clave]\n",
              "    if clave in DATOS_POR_PAIS:\n        return DATOS_POR_PAIS[clave]\n"
              "    return DATOS_POR_PAIS['colombia']\n")
    rc_rot, out_rot = corre_banco(base)
    rojos = [l for l in out_rot.splitlines() if l.startswith("  - ")]
    paso(3, "MUERDE cuando un pais sin pack hereda la direccion de Colombia",
         rc_rot != 0,
         f"{len(rojos)} pruebas en rojo" if rc_rot != 0
         else "siguió VERDE con el fallo dentro: el banco es decoración")
    if rojos:
        for l in rojos[:4]:
            print("        " + l.strip())

print("=" * 68)
if fallos:
    print(f"LA CONTRAPRUEBA FALLA: {len(fallos)} de 3")
    for f in fallos:
        print("  - " + f)
    sys.exit(1)
print("3 de 3 · el banco tolera la redacción y muerde la conducta")
sys.exit(0)
