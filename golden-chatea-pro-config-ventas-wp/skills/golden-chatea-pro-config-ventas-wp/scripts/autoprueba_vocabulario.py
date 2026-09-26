#!/usr/bin/env python3
"""autoprueba_vocabulario.py — banco del mapa vocabulario_direccion_por_pais.

Comprueba EJERCIENDO (no leyendo) que el mapa sigue siendo lo que dice ser: una copia de los
packs de golden-chatea-pro-validacion-direcciones, no una traduccion ni una herencia de Colombia.

  A. cada entrada cita al pack y la cita sigue LITERAL en el pack (si el pack cambio, rojo)
  B. las entradas derivadas se recomputan desde su cita y dan lo mismo que lo guardado
  C. build_config.py construye los 4 textos de CADA pais del mapa dentro de los techos
  D. ninguna palabra propia de Colombia (barrio, departamento) se cuela en un pais cuyo pack
     no la usa (la herencia silenciosa, medida)
  E. un pais SIN pack cae al generico declarado y no hereda a Colombia
  F. la clave del pais se normaliza (España = ESPANA, costa-rica = COSTA RICA)
  G. el banco MUERDE: una cita alterada se detecta
  H. el roster de paises esta ANCLADO POR NOMBRE (PAISES_MAPA, no solo un numero) y todo
     `origen` esta en el conjunto cerrado ORIGENES_VALIDOS
  I. CONTENIDO contra el pack completo (no solo la cita): cero avisos sobre el mapa real, para
     las 23 entradas, incluidas las DOS a mano
  J. el banco MUERDE LOS TRES SABOTAJES MEDIDOS por el Centro de Mando el 21-sep -- reproducidos
     literalmente, uno por uno, sobre una copia (nunca sobre el mapa real):
       1. campos_memoria alterado (Colombia "departamento" -> "provincia")
       2. aclaracion alterada (Colombia -> "Da igual el barrio.")
       3. origen borrado en un parafraseado (Chile)
     Los tres pasaban en 100% verde antes de esta correccion; los tres deben salir ROJOS ahora.
     Cada uno se protege con un `in` antes de indexar (si el pais anclado ya falta, se declara
     NO EJECUTADO, nunca un traceback).
  K. la excepcion de A_MANO queda ATADA AL PAIS: meter "estado" (la excepcion de MEXICO) en
     COLOMBIA se rechaza -- no es una puerta lateral para cualquier pais (hallazgo del CdM,
     segunda vuelta, 21-sep).
  L. BORRAR UN PAIS ENTERO se nombra, no truena: quitar CHILE del mapa se reporta como "falta
     CHILE" contra el roster, sin KeyError ni traceback (mismo hallazgo, punto 5); y un pais
     fuera del roster ("MARTE") se nombra como "sobra".

Uso: PYTHONDONTWRITEBYTECODE=1 python3 scripts/autoprueba_vocabulario.py   (0 = todo verde)
Si la skill hermana golden-chatea-pro-validacion-direcciones no esta instalada, A, B, I, J, K y
L se declaran NO EJECUTADOS (no verdes) y el resto corre.
"""
import copy, json, os, subprocess, sys, tempfile, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import generar_vocabulario as G  # noqa: E402

LIM = json.load(open(os.path.join(AQUI, "..", "assets", "limites.json"), encoding="utf-8"))
VOC = {k: v for k, v in LIM["vocabulario_direccion_por_pais"].items() if not k.startswith("_")}
PACKS = G.PACKS_DEFECTO
BUILD = os.path.join(AQUI, "build_config.py")
TMP = tempfile.mkdtemp(prefix="autoprueba_voc_")
PM = os.path.join(TMP, "pm.txt")
open(PM, "w", encoding="utf-8").write("Prompt maestro de prueba para el banco.")
ok = fallos = 0
no_ejecutados = []


def check(nombre, cond, detalle=""):
    global ok, fallos
    if cond:
        ok += 1
    else:
        fallos += 1
        print(f"  ✗ {nombre} {detalle}")


def construir(pais, tag, extra=()):
    pref = os.path.join(TMP, tag)
    cmd = [sys.executable, BUILD, "--pais", pais, "--url-tienda", "https://ejemplo.test",
           "--nombre-bot", "Ana", "--nombre-tienda", "Empresa Uno", "--modelo", "dropshipping",
           "--prompt-maestro", PM, "--out-prefix", pref] + list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ,
                       "PYTHONDONTWRITEBYTECODE": "1"})
    txt = ""
    for suf in ("_BOTFIELD_1.json", "_BOTFIELD_2.json"):
        if os.path.exists(pref + suf):
            txt += open(pref + suf, encoding="utf-8").read()
    return r.returncode, r.stdout + r.stderr, txt


def texto_pack(v):
    ruta = os.path.join(PACKS, v["fuente"])
    return open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else None


# ── A y B: contra el pack ──────────────────────────────────────────────────
hay_packs = os.path.isdir(PACKS)
if not hay_packs:
    no_ejecutados.append("A y B (la skill hermana golden-chatea-pro-validacion-direcciones no esta)")
else:
    for k, v in sorted(VOC.items()):
        t = texto_pack(v)
        check(f"A {k}: existe el pack {v.get('fuente')}", t is not None)
        if t is None:
            continue
        citas = list(v.get("citas_pack", []))
        for c in ("cita_estructura", "cita_aclaracion"):
            if c in v:
                citas.append(v[c])
        check(f"A {k}: tiene al menos una cita", bool(citas))
        for c in citas:
            check(f"A {k}: cita literal en el pack", c in t, f"-> {c[:70]!r}")
        if v.get("origen", "").startswith("derivado"):
            check(f"B {k}: campos_memoria = derivado de su cita",
                  v["campos_memoria"] == G.campos_desde_estructura(
                      v["cita_estructura"].split(":", 1)[1].strip()))
            check(f"B {k}: aclaracion = derivada de su cita",
                  v["aclaracion"] == G.aclaracion_desde_linea(v["cita_aclaracion"]))
            check(f"B {k}: aclaracion_corta = derivada de su cita",
                  v["aclaracion_corta"] == G.corta_desde_linea(v["cita_aclaracion"]))

# ── C y D: construir CADA pais del mapa ────────────────────────────────────
PALABRAS_COLOMBIA = ("barrio", "departamento")
for k, v in sorted(VOC.items()):
    extra = ["--flete-max", "1"]
    if k not in LIM.get("moneda_por_pais", {}):
        extra += ["--moneda", "USD"]
    rc, out, txt = construir(k, k.replace(" ", "_"), extra)
    check(f"C {k}: build_config sale 0 dentro de los techos", rc == 0, out[-200:])
    if rc:
        continue
    check(f"C {k}: campos_memoria esta en el rol", v["campos_memoria"] in json.loads(
        json.dumps(txt)) or v["campos_memoria"].replace('"', '\\"') in txt)
    check(f"C {k}: la aclaracion esta en las restricciones",
          v["aclaracion"] in txt or v["aclaracion"].replace('"', '\\"') in txt)
    propio = (v["campos_memoria"] + " " + v["aclaracion"] + " " + v["aclaracion_corta"]).lower()
    for w in PALABRAS_COLOMBIA:
        if w not in propio:
            check(f"D {k}: '{w}' no se cuela (su pack no la usa)", w not in txt.lower())

# ── E: pais sin pack = generico declarado, sin herencia ───────────────────
rc, out, txt = construir("BOLIVIA", "bolivia", ["--flete-max", "1", "--moneda", "BOB"])
check("E BOLIVIA (sin pack) construye", rc == 0, out[-200:])
check("E BOLIVIA declara que no tiene vocabulario", "[DECLARADO]" in out)
check("E BOLIVIA no hereda 'departamento' de Colombia", "departamento" not in txt.lower())

# ── F: normalizacion de la clave ───────────────────────────────────────────
_, _, a = construir("España", "n1", ["--flete-max", "1", "--moneda", "EUR"])
_, _, b = construir("ESPANA", "n2", ["--flete-max", "1", "--moneda", "EUR"])
check("F 'España' == 'ESPANA' (mismo texto)", a != "" and a == b)
_, _, c = construir("costa-rica", "n3", ["--flete-max", "1", "--moneda", "CRC"])
_, _, d = construir("Costa Rica", "n4", ["--flete-max", "1", "--moneda", "CRC"])
check("F 'costa-rica' == 'Costa Rica' (mismo texto)", c != "" and c == d)

# ── G: el banco MUERDE (cita) ──────────────────────────────────────────────
if hay_packs:
    v = VOC["ARGENTINA"]
    tp = texto_pack(v)
    citas = [v["cita_estructura"], v["cita_aclaracion"]]
    alterada = citas[0].replace("altura", "alturaX")
    check("G cita alterada se detecta (esperado: NO esta en el pack)", alterada not in tp)

# ── H: roster ANCLADO por NOMBRE (no solo por numero) y `origen` de un conjunto cerrado ──
faltan_h, sobran_h = G.diferencias_de_roster(VOC)
check(f"H el mapa tiene los {G.PAISES_ESPERADOS} paises del roster anclado PAISES_MAPA "
      "(por NOMBRE, no solo por numero)", not faltan_h and not sobran_h,
      f"-> faltan {faltan_h} · sobran {sobran_h}")
for k, v in sorted(VOC.items()):
    check(f"H {k}: origen esta en ORIGENES_VALIDOS", v.get("origen") in G.ORIGENES_VALIDOS,
          f"-> {v.get('origen')!r}")

# ── I: CONTENIDO contra el pack completo, sobre el mapa REAL (control positivo) ──
# Reusa la MISMA funcion que usa el generador (no una copia): si el generador cambia el
# criterio, este chequeo cambia con el, no diverge.
if hay_packs:
    avisos_reales = G.validar_contenido_contra_pack(VOC, PACKS, G.excepciones_desde_a_mano())
    check("I el mapa REAL tiene cero avisos de contenido-contra-pack (control positivo, "
          "sin esto una prueba que muerde sobre datos malos no dice nada de los buenos)",
          not avisos_reales, f"-> {avisos_reales}")
else:
    no_ejecutados.append("I (la skill hermana no esta)")

# ── J: reproducir LITERAL los sabotajes medidos por el Centro de Mando 21-sep ──
# Cada uno sobre una COPIA de VOC, nunca sobre el mapa real, y cada uno se juzga SOLO -- no
# se deja que un sabotaje tape a otro. Cada mutacion se protege con un `in` antes de indexar:
# un pais que YA falta (lo marcaria H) no debe reventar J con un KeyError -- esa fue justo la
# segunda vuelta del CdM (punto 5: borrar CHILE entero disparaba traceback, no un aviso).
if hay_packs:
    base = copy.deepcopy(VOC)

    if "COLOMBIA" in base:
        m1 = copy.deepcopy(base)
        m1["COLOMBIA"]["campos_memoria"] = "ciudad, provincia, dirección, barrio"
        av1 = G.validar_contenido_contra_pack(m1, PACKS, G.excepciones_desde_a_mano())
        check("J1 campos_memoria 'departamento'->'provincia' (Colombia) se detecta",
              any("COLOMBIA" in a and "campos_memoria" in a for a in av1), f"-> {av1}")
        check("J el total de casos NO se mueve con un contenido malo (sigue anclado a H, "
              "no a lo que el propio dato traiga)", len(m1) == len(base) == G.PAISES_ESPERADOS)
    else:
        no_ejecutados.append("J1 (falta COLOMBIA en el mapa; ya lo marca H)")

    if "COLOMBIA" in base:
        m2 = copy.deepcopy(base)
        m2["COLOMBIA"]["aclaracion"] = "Da igual el barrio."
        av2 = G.validar_contenido_contra_pack(m2, PACKS, G.excepciones_desde_a_mano())
        check("J2 aclaracion 'Da igual el barrio.' (Colombia) se detecta",
              any("COLOMBIA" in a and "aclaracion" in a for a in av2), f"-> {av2}")
    else:
        no_ejecutados.append("J2 (falta COLOMBIA en el mapa; ya lo marca H)")

    if "CHILE" in base:
        m3 = copy.deepcopy(base)
        m3["CHILE"].pop("origen", None)  # pop, no del: robusto si ya venia sin 'origen'
        av3 = G.validar_contenido_contra_pack(m3, PACKS, G.excepciones_desde_a_mano())
        check("J3 origen borrado (Chile, parafraseado) se detecta",
              any(a.startswith("CHILE") and "origen" in a for a in av3), f"-> {av3}")
    else:
        no_ejecutados.append("J3 (falta CHILE en el mapa; ya lo marca H)")
else:
    no_ejecutados.append("J (la skill hermana no esta)")

# ── K: la excepcion de A_MANO queda ATADA AL PAIS, no es una puerta lateral ──
# Hallazgo del CdM (segunda vuelta, 21-sep): meter "estado" (la excepcion nombrada de MEXICO)
# en COLOMBIA. Si la excepcion no estuviera atada por pais, esto pasaria en verde.
if hay_packs and "COLOMBIA" in VOC:
    m4 = copy.deepcopy(VOC)
    m4["COLOMBIA"]["campos_memoria"] = "ciudad, departamento, estado, dirección, barrio"
    av4 = G.validar_contenido_contra_pack(m4, PACKS, G.excepciones_desde_a_mano())
    check("K 'estado' (excepcion de MEXICO) metido en COLOMBIA se rechaza -- la excepcion "
          "no abre una puerta lateral para otro pais",
          any("COLOMBIA" in a and "estado" in a for a in av4), f"-> {av4}")
else:
    no_ejecutados.append("K (falta COLOMBIA o la skill hermana)")

# ── L: BORRAR UN PAIS ENTERO no revienta -- se nombra, no truena ──
# Hallazgo del CdM (segunda vuelta, 21-sep, punto 5): quitar CHILE reventaba con
# `KeyError: 'CHILE'` en el primer sitio que lo indexara directo. Ahora el roster lo nombra
# ANTES de que nada mas lo intente indexar.
if hay_packs:
    m5 = copy.deepcopy(VOC)
    m5.pop("CHILE", None)
    try:
        faltan5, sobran5 = G.diferencias_de_roster(m5)
        reboto = False
    except Exception as e:  # el punto que se prueba: que NO reviente
        faltan5, sobran5, reboto = [], [], e
    check("L borrar CHILE del mapa no revienta (se compara contra el roster, no se indexa "
          "a ciegas)", reboto is False, f"-> exception: {reboto}")
    check("L borrar CHILE del mapa se nombra por NOMBRE ('falta CHILE', no un traceback)",
          reboto is False and "CHILE" in faltan5, f"-> faltan {faltan5}")

    m6 = copy.deepcopy(VOC)
    m6["MARTE"] = dict(m6.get("COLOMBIA", {}))  # un pais que no esta en el roster
    _, sobran6 = G.diferencias_de_roster(m6)
    check("L un pais fuera del roster ('MARTE') se nombra como 'sobra', no se cuela mudo",
          "MARTE" in sobran6, f"-> sobran {sobran6}")
else:
    no_ejecutados.append("L (la skill hermana no esta)")

shutil.rmtree(TMP, ignore_errors=True)
total = ok + fallos
print(f"\n  autoprueba_vocabulario: {ok}/{total} verdes · {len(VOC)} paises en el mapa")
for n in no_ejecutados:
    print(f"  NO EJECUTADO: {n}")
sys.exit(1 if fallos or no_ejecutados else 0)
