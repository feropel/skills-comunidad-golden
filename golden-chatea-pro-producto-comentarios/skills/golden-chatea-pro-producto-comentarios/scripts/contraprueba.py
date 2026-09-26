#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contraprueba.py — la prueba DEL BANCO. Porque un banco tambien se verifica.

POR QUE EXISTE
`autoprueba.py` llego a comprobar el TEXTO de los mensajes de error con `in`. El 2026-09-22 se
puso en rojo solo porque se reescribio un mensaje, sin que nada se hubiera roto. Un banco que
mide la redaccion da falsos rojos, y un falso rojo entrena a ignorar el banco. Se reescribio
sobre `--json` para medir CONDUCTA. Esta contraprueba comprueba que ese arreglo funciona, en
las DOS direcciones:

  A · copia intacta            -> el banco pasa
  B · redaccion reescrita      -> el banco SIGUE en verde   (tolera)
  C · conducta rota            -> el banco se pone ROJO     (muerde)

DOS DEFENSAS QUE ESTE SCRIPT NECESITA, y que en su v1 NO TENIA
1. `sustituye()` FALLA RUIDOSAMENTE si no encuentra el texto. Con un `str.replace` pelado, un
   texto que ya no existe no reemplaza nada, la copia queda INTACTA y el paso B pasa en verde
   "tolerando la re-redaccion" que nunca ocurrio. La prueba mentiria sin dar un solo error.
2. El paso C VERIFICA QUE EL SABOTAJE SABOTEA antes de juzgar al banco. Un sabotaje inerte
   produce exactamente la misma senal que un banco decorativo —todo en verde— y llevan a
   conclusiones OPUESTAS: en un caso se culpa al banco por nada, en el otro se le absuelve
   estando roto. (Leccion de la fabrica de config-comentarios, que envolvio un dict en un
   defaultdict creyendo que saboteaba y no saboteaba: `clave in defaultdict` sigue siendo False
   para una clave que nunca se inserto.)

USO
  python3 contraprueba.py      ·  0 = el banco tolera la redaccion y muerde la conducta
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sustituye(texto, viejo, nuevo, motivo):
    """Reemplaza, y REVIENTA si no encontro nada. Un reemplazo que no reemplaza deja esta
    prueba mintiendo en verde, que es peor que no tenerla."""
    if viejo not in texto:
        print(f"  🔴 ABORTADA: no se encontro el texto a sustituir ({motivo}).")
        print("     El fichero cambio y esta prueba ya no mide lo que dice medir.")
        sys.exit(2)
    return texto.replace(viejo, nuevo, 1)


def copia():
    """Copia la skill a un temporal DONDE SE PUEDA ESCRIBIR.

    MEDIDO EL 2026-09-22: una skill terminada vive BLINDADA (`chflags -R uchg`), y `copytree`
    arrastra ese flag a la copia. El `chmod` de abajo chocaba con `PermissionError` y esta
    contraprueba reventaba ANTES del primer caso. O sea: la herramienta que verifica el banco
    no se podia correr en el unico estado en que la skill de verdad vive. Por eso se quitan
    los flags de macOS ADEMAS de los permisos, y en los directorios tambien -- un directorio
    con `uchg` impide crear y borrar dentro aunque los ficheros ya esten sueltos."""
    d = os.path.join(tempfile.mkdtemp(), "skill")
    shutil.copytree(SRC, d)
    suelta(d)
    return d


def suelta(raiz_arbol):
    """Quita flags y permisos de solo-lectura de TODO el arbol, EMPEZANDO POR SU RAIZ.

    La raiz no es un detalle: `os.walk` nunca la entrega como entrada, asi que un primer
    arreglo que solo recorria el contenido dejo el directorio de arriba con `uchg`, y el
    `rmtree` del final seguia reventando -- el fallo se habia MOVIDO, no resuelto."""
    rutas = [raiz_arbol]
    for raiz, directorios, ficheros in os.walk(raiz_arbol):
        rutas += [os.path.join(raiz, n) for n in ficheros + directorios]
    for ruta in rutas:
        if hasattr(os, "chflags"):
            try:
                os.chflags(ruta, 0)
            except OSError:
                pass
        try:
            os.chmod(ruta, 0o755 if os.path.isdir(ruta) else 0o644)
        except OSError:
            pass


def corre_banco(d):
    r = subprocess.run([sys.executable, os.path.join(d, "scripts/autoprueba.py")],
                       capture_output=True, text=True, env=ENV)
    linea = (r.stdout or "").strip().splitlines()
    return r.returncode, (linea[-1].strip() if linea else "(sin salida)")


def errores_del_validador(d, productos, via="json"):
    """Errores que devuelve el validador de ESA copia. Sirve para comprobar si un sabotaje
    cambio la conducta DE VERDAD, en vez de darlo por hecho."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False)
        ruta = f.name
    try:
        r = subprocess.run([sys.executable, os.path.join(d, "scripts/validar_producto.py"),
                            ruta, "--via", via, "--json"],
                           capture_output=True, text=True, env=ENV)
        sal = r.stdout or ""
        try:
            return json.loads(sal[sal.index("{"):sal.rindex("}") + 1]).get("errores", [])
        except (ValueError, json.JSONDecodeError):
            return []
    finally:
        os.unlink(ruta)


# Un producto al que le falta `estado`: es lo que mira el sabotaje del paso C.
CUATRO_LLAVES = [{"img": "https://cdn.ejemplo.com/x.jpg", "name": "Serum Aurora",
                  "desc": "x REGLAS DE MARCA y",
                  "rela": ("serum aurora, aurora, manchas en la cara, melasma, "
                           "hiperpigmentacion, tono desigual, aclarar manchas, precio del "
                           "serum Aurora, cuanto vale el serum Aurora, hacen envios de Aurora")}]

print("  === CONTRAPRUEBA · el banco tolera la redaccion y muerde la conducta? ===")
ok = {}
raiz_tmp = None

# ── A ──────────────────────────────────────────────────────────────────────
d = copia()
raiz_tmp = os.path.dirname(d)
ec, linea = corre_banco(d)
print(f"   A · copia intacta          {linea}  (exit {ec})")
ok["A"] = ec == 0
if not ok["A"]:
    print("  🔴 El banco ya falla sin tocar nada. Arregla eso antes de seguir.")
    suelta(raiz_tmp)
    shutil.rmtree(raiz_tmp)
    sys.exit(1)

# ── B · solo REDACCION ─────────────────────────────────────────────────────
val = os.path.join(d, "scripts/validar_producto.py")
t = open(val, encoding="utf-8").read()
t = sustituye(t, "FALTAN llaves {faltan} — con 4 llaves el panel no interpreta el producto",
              "al objeto le faltan estas claves {faltan}, el panel lo ignora",
              "mensaje de llaves faltantes")
t = sustituye(t, "NO VA A GUARDAR ENTERO: {crudo} crudos sobre {TECHO}",
              "EXCEDE LA ESCRITURA: {crudo} crudos sobre {TECHO}",
              "mensaje del techo de guardado")
open(val, "w", encoding="utf-8").write(t)

antes = len(errores_del_validador(SRC, CUATRO_LLAVES))
ahora = len(errores_del_validador(d, CUATRO_LLAVES))
ec, linea = corre_banco(d)
print(f"   B · redaccion reescrita    {linea}  (exit {ec})")
print(f"       conducta intacta? errores {antes} -> {ahora}  "
      + ("si" if antes == ahora else "🔴 cambio: el paso B no aisla la redaccion"))
ok["B"] = (ec == 0) and (antes == ahora)

# ── C · CONDUCTA rota, comprobando ANTES que el sabotaje sabotea ────────────
t = open(val, encoding="utf-8").read()
t = sustituye(t, "    if faltan:\n        err(", "    if False:\n        err(",
              "rama que detecta llaves faltantes")
open(val, "w", encoding="utf-8").write(t)

roto = len(errores_del_validador(d, CUATRO_LLAVES))
sabotea = roto < ahora
print(f"       el sabotaje sabotea? errores {ahora} -> {roto}  "
      + ("si" if sabotea else "🔴 NO — sabotaje INERTE, con el no se puede juzgar al banco"))
ec, linea = corre_banco(d)
print(f"   C · conducta rota          {linea}  (exit {ec})")
ok["C"] = sabotea and ec != 0

suelta(raiz_tmp)
shutil.rmtree(raiz_tmp)
print()
if all(ok.values()):
    print("  VEREDICTO: el banco TOLERA la re-redaccion y MUERDE el cambio de conducta")
    sys.exit(0)
print(f"  🔴 VEREDICTO: falla — {', '.join(k for k, v in ok.items() if not v)}")
sys.exit(1)
