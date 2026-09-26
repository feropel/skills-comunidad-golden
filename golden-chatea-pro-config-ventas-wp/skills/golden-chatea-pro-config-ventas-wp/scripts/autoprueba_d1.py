#!/usr/bin/env python3
"""autoprueba_d1.py — Banco del chequeo D1 de valida_producto.py, en los DOS sentidos.

POR QUE EXISTE: el Disparador de productos Extendido es un ARRAY (ver
assets/template-registro-disparador.json), asi que pegar el campo REAL del workspace
en --registro reventaba con un AttributeError crudo y el chequeo D1 no llegaba a correr:
el usuario que hacia lo correcto era el que se estrellaba. Se arreglo el 2026-09-05 y este
banco lo fija: 9 casos, incluidos los que se SABEN malos (misma palabra en otro slot,
array vacio, palabra duplicada, entrada ausente) y las dos formas viejas, que no se rompen.

Uso:
    python3 autoprueba_d1.py     # exit 0 si las 9 estan en verde
"""
import io
import json
import os
import subprocess
import sys
import tempfile

# La skill se localiza desde la posicion de ESTE fichero, no con una ruta absoluta
# clavada (se rompe en otro equipo) ni con "~" en una cadena (Python NO lo expande:
# medido, rompio el banco entero). Derivar > clavar.
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAL = S + "/scripts/valida_producto.py"
TMP = tempfile.mkdtemp()

base = json.load(io.open(S + "/assets/template-botfield-producto.json", encoding="utf-8"))


def producto(kw, nombre="Producto Prueba"):
    p = json.loads(json.dumps(base))
    p["informacion_de_producto"]["nombre"] = nombre
    p["activadores_del_flujo"]["palabras_clave"] = kw
    return p


def escribir(nombre, obj):
    r = os.path.join(TMP, nombre)
    json.dump(obj, io.open(r, "w", encoding="utf-8"), ensure_ascii=False)
    return r


def correr(prod, reg):
    r = subprocess.run([sys.executable, VAL, "--in", prod, "--registro", reg],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


ENTRADA = {"producto": "Producto Prueba", "name": "[Producto Ventas Wp] 3",
           "keyW": "PRUEBA,,,,,,", "idAd": ",,,,,,", "estado": "activo"}
fallos = []


def check(nombre, cond, detalle=""):
    print(("  OK   " if cond else "  FALLA") + f" · {nombre}" +
          (f" :: {detalle}" if not cond else ""))
    if not cond:
        fallos.append(nombre)


print("BANCO D1 · registro en forma REAL (array)")

# 1 · ARRAY con la entrada correcta -> D1 identico, sin traceback
p = escribir("p1.json", producto("PRUEBA,,,,,,"))
r = escribir("r1.json", [{"keyW": "OTRO,,,,,,", "producto": "Otro", "name": "[Producto Ventas Wp] 1",
                          "estado": "activo"}, ENTRADA])
rc, out = correr(p, r)
check("array: encuentra la entrada y D1 sale identico", "D1: palabra clave identica" in out, out[-260:])
check("array: sin traceback de Python", "Traceback" not in out, out[-200:])

# 2 · ARRAY con la MISMA palabra en OTRO slot -> D1 ROTO (incidente de campo 2026-08-23)
p = escribir("p2.json", producto("PRUEBA,,,,,,"))
mal = dict(ENTRADA, keyW=",PRUEBA,,,,,")
r = escribir("r2.json", [mal])
rc, out = correr(p, r)
check("array: mismo texto en OTRO slot -> D1 ROTO", "D1 ROTO" in out, out[-260:])
check("array: y el exit es 1", rc == 1, f"rc={rc}")

# 3 · REGRESION: el objeto suelto de siempre sigue funcionando
p = escribir("p3.json", producto("PRUEBA,,,,,,"))
r = escribir("r3.json", ENTRADA)
rc, out = correr(p, r)
check("objeto suelto (forma vieja) sigue funcionando", "D1: palabra clave identica" in out, out[-260:])

# 4 · REGRESION: la envoltura entrada_nueva del template sigue funcionando
r = escribir("r4.json", {"_bot_field": "x", "entrada_nueva": ENTRADA})
rc, out = correr(p, r)
check("envoltura 'entrada_nueva' sigue funcionando", "D1: palabra clave identica" in out, out[-260:])

# 5 · ARRAY VACIO -> error LEGIBLE, no traceback
r = escribir("r5.json", [])
rc, out = correr(p, r)
check("array vacio -> error legible sin traceback",
      "Traceback" not in out and "ERROR" in out, out[-260:])

# 6 · DUPLICADO de palabra clave -> lo dice (el bot no sabria cual disparar)
r = escribir("r6.json", [ENTRADA, dict(ENTRADA, name="[Producto Ventas Wp] 9")])
rc, out = correr(p, r)
check("palabra clave duplicada -> lo denuncia", "MISMA" in out or "duplicad" in out.lower(), out[-260:])

# 7 · ARRAY sin la entrada de este producto -> error legible que dice que busco
p7 = escribir("p7.json", producto("AUSENTE,,,,,,", "Otro Nombre"))
r = escribir("r7.json", [dict(ENTRADA, keyW="X,,,,,,", producto="X"),
                         dict(ENTRADA, keyW="Y,,,,,,", producto="Y")])
rc, out = correr(p7, r)
check("entrada ausente -> error legible que nombra lo buscado",
      "Traceback" not in out and "no encuentro la entrada" in out, out[-260:])

print(f"\nCOBERTURA: {9 - len(fallos)} de 9 pruebas en verde")
if fallos:
    print("FALLAN: " + ", ".join(fallos))
    sys.exit(1)
sys.exit(0)
