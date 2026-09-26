"""Banco de sabotajes de margen_cod.py: se corre después de CADA edición del script.
Cada sabotaje debe hacer FALLAR la autoprueba (exit != 0). El control NEUTRO debe pasar (exit 0):
si el neutro 'se detecta', el arnés inventa detecciones."""
import os
import subprocess
import sys
import tempfile

ORIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "margen_cod.py")
SAB = [
    ("rechaza ratio 1", "if r > 1:", "if r >= 1:"),
    ("miles con coma", '.0f}".replace(",", ".")', '.0f}".replace(",", ",")'),
    ("sens precio mueve costo", '(("precio", "p"), ("entrega"', '(("precio", "c"), ("entrega"'),
    ("PASA invertido", "'PASA' if round(base) >= round(piso) else 'NO PASA'", "'NO PASA' if round(base) >= round(piso) else 'PASA'"),
    ("ida y vuelta", "- d * (f * r) - cpa", "- d * (f * 2) - cpa"),
    ("acepta negativos", "        if v < 0:", "        if v < -1e9:"),
    ("acepta NaN", "        if not math.isfinite(v):", "        if False:"),
    ("tope silencioso", 'nota = " (topa)"', 'nota = ""'),
    ("veredicto sin piso", "    if piso is None:", "    if False:"),
    ("sens CPA mueve costo", '("CPA", "cpa")):', '("CPA", "c")):'),
    ("dec sin coma", 'return f"{x:.{n}f}".replace(".", ",")', 'return f"{x:.{n}f}"'),
    ("veredicto con >", "round(base) >= round(piso)", "round(base) > round(piso)"),
    ("PENDIENTE sale 0", 'no se modela con datos inventados")\n        return 2', 'no se modela con datos inventados")\n        return 0'),
    ("DATO INVALIDO sale 0", '    except DatoInvalido as err:\n        print(f"DATO INVÁLIDO: {err}")\n        return 2\n    faltan',
     '    except DatoInvalido as err:\n        print(f"DATO INVÁLIDO: {err}")\n        return 0\n    faltan'),
    ("informe flete=costo", "flete {cop(a['flete'])}", "flete {cop(a['costo'])}"),
    ("múltiplo sobre flete", "multiplo(a['precio'], a['costo'])", "multiplo(a['precio'], a['flete'])"),
    ("acepta entrega>1 sola (quita la suma)", "if e + d > 1 + 1e-9:", "if d > 1 + 1e-9:"),
    ("main ignora piso", '    piso = a.get("piso")', "    piso = None"),
    ("comisión en devolución", "- d * (f * r) - cpa", "- d * (f * r + p * k) - cpa"),
    ("múltiplo redondeado", "math.floor(p / c * 100) / 100", "round(p / c, 2)"),
    ("no lee miles colombianos", '        t = t.replace(".", "")', "        pass"),
    ("piso NaN aceptado", "(not math.isfinite(piso) or piso < 0", "(piso < 0"),
    # Los 16 que se escaparon en la tercera pasada, adaptados al código actual
    ("K: CPA faltante asume 0", "    faltan = [ETIQUETA[n] for n in CAMPOS if n not in datos]",
     '    datos.setdefault("cpa", 0.0)\n    faltan = [ETIQUETA[n] for n in CAMPOS if n not in datos]'),
    ("M: piso 0 por defecto en CLI", '    piso = datos.get("piso")\n    if piso is not None and', '    piso = datos.setdefault("piso", 0.0)\n    if piso is not None and'),
    ("F: informe ignora comisión", "r=a[\"ratio\"], cpa=a[\"cpa\"], k=k or 0.0)", "r=a[\"ratio\"], cpa=a[\"cpa\"], k=0.0)"),
    ("L: comisión 0 por defecto", '    k = a.get("comision")', '    k = a.get("comision", 0.0) or 0.0'),
    ("W: veredicto sin redondeo", "'PASA' if round(base) >= round(piso) else 'NO PASA'", "'PASA' if base >= piso + 1e-6 else 'NO PASA'"),
    ("A: tolerancia 1,05", "if e + d > 1 + 1e-9:", "if e + d > 1.05:"),
    ("S: etiquetas cruzadas", "f\"Entrega {dec(a['entrega'] * 100, 1)} % · devolución {dec(a['devolucion'] * 100, 1)} % · \"",
     "f\"Entrega {dec(a['devolucion'] * 100, 1)} % · devolución {dec(a['entrega'] * 100, 1)} % · \""),
    ("Q: comisión mostrada x10", "comisión de recaudo {dec(k * 100, 1)} %", "comisión de recaudo {dec(k * 1000, 1)} %"),
    ("R: ratio mostrado 1-r", "ratio de devolución {dec(a['ratio'], 3)}", "ratio de devolución {dec(1 - a['ratio'], 3)}"),
    ("E: precio +25 %", "        for mult in (0.8, 1.0, 1.2):", "        for mult in ((0.8, 1.0, 1.25) if clave == 'p' else (0.8, 1.0, 1.2)):"),
    ("E2: entrega +30 %", "        for mult in (0.8, 1.0, 1.2):", "        for mult in ((0.8, 1.0, 1.3) if clave == 'e' else (0.8, 1.0, 1.2)):"),
    ("V: columna 100 % corrupta", "fila.append((int(round(mult * 100)), utilidad(**w), nota))",
     "fila.append((int(round(mult * 100)), utilidad(**w) + (1000 if mult == 1.0 else 0), nota))"),
    ("D: muestra -$0", 'return f"-${s}" if round(x) < 0 else f"${s}"', 'return f"-${s}" if x < 0 else f"${s}"'),
    ("N2: no lee 50.000,00", r'(\.\d{3})+(,\d+)?", t)', r'(\.\d{3})+", t)'),
    ("O: no lee 79 900", '.replace("$", "").replace(" ", "")', '.replace("$", "")'),
    ("X: faltante con KeyError", '    faltan = [ETIQUETA[n] for n in CAMPOS if n not in datos]\n    if faltan:',
     '    faltan = []\n    if faltan:'),
    ("lee fracción 0.735 como miles", "    if nombre in FRACCIONES:\n        t = t.replace", "    if False:\n        t = t.replace"),
    ("acepta monto ambiguo 12.34", '            raise DatoInvalido(f"{ETIQUETA[nombre]} ambiguo', '            t = t.replace(",", "."); pass  # DatoInvalido(f"{ETIQUETA[nombre]} ambiguo'),
    ("repetido pisa en silencio", "        if clave in datos:\n", "        if False:\n"),
    ("costo 0,4 con múltiplo", 'if a["costo"] >= 1 else', 'if a["costo"] > 0 else'),
]
NEUTRO = ("NEUTRO (comentario)", "TOPE_MONTO = 1e12", "TOPE_MONTO = 1e12  # neutro")

src = open(ORIG, encoding="utf-8").read()
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
det = ciegas = 0
with tempfile.TemporaryDirectory() as d:
    for nombre, viejo, nuevo in SAB + [NEUTRO]:
        if src.count(viejo) != 1:
            print(f"NO APLICA ({src.count(viejo)} coincidencias): {nombre}")
            ciegas += 1
            continue
        f = os.path.join(d, "s.py")
        open(f, "w", encoding="utf-8").write(src.replace(viejo, nuevo))
        rc = subprocess.run([sys.executable, f, "--autoprueba"], capture_output=True, env=env).returncode
        if nombre.startswith("NEUTRO"):
            print(f"{'neutro OK (pasa)' if rc == 0 else 'NEUTRO DETECTADO: arnés roto'}")
            continue
        if rc == 0:
            print(f"CIEGA: {nombre}")
            ciegas += 1
        else:
            print(f"detectado: {nombre}")
            det += 1
print(f"RESULTADO: {det} de {len(SAB)} sabotajes detectados")
sys.exit(0 if det == len(SAB) else 1)
