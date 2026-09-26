"""Banco: el aviso de conteos abiertos debe MORDER cuando toca y CALLAR cuando no."""
import importlib.util, io, sys, contextlib, os

ruta = os.path.expanduser("~/.claude/skills/golden-investigacion-mercado/scripts/google_ads_transparency.py")
spec = importlib.util.spec_from_file_location("gat", ruta)
gat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gat)
gat.PAUSA = 0  # sin esperas en el banco


def pieza(i):
    return {"1": "AR1", "2": f"CR{i}", "12": "X S.A.", "14": "x.com",
            "6": {"1": "1788249140"}, "7": {"1": "1788880951"}}


def correr(cuantos_devuelve, argv):
    """cuantos_devuelve(tope) -> cuantas piezas simula el servidor."""
    gat._post = lambda metodo, freq: {"1": [pieza(i) for i in range(cuantos_devuelve(freq["2"]))]}
    buf = io.StringIO()
    sys.argv = ["gat"] + argv
    with contextlib.redirect_stdout(buf):
        gat.main()
    return buf.getvalue()


fallos = []

# CASO 1 · servidor que SIEMPRE llena la pagina -> los dos paises quedan ABIERTOS -> debe avisar
s1 = correr(lambda tope: tope, ["--dominio", "x.com", "--paises", "CO,MX", "--contar"])
if "conteos quedaron ABIERTOS" not in s1:
    fallos.append("CASO 1: dos conteos abiertos y NO avisó (el guarda no muerde)")
if "no lo compares" not in s1.lower() and "NO los compares" not in s1:
    fallos.append("CASO 1: no dijo que no se comparan")

# CASO 2 · servidor con 7 anuncios -> la primera pagina viene incompleta -> CIERRA -> NO debe avisar
s2 = correr(lambda tope: min(7, tope), ["--dominio", "x.com", "--paises", "CO,MX", "--contar"])
if "ABIERTOS" in s2:
    fallos.append("CASO 2: conteos cerrados y avisó igual (falso positivo)")
if "7 creativos activos" not in s2:
    fallos.append("CASO 2: no reportó el total cerrado de 7")

# CASO 3 · un solo pais abierto -> "al menos N", pero sin el aviso de comparacion (no hay con quien)
s3 = correr(lambda tope: tope, ["--dominio", "x.com", "--pais", "CO", "--contar"])
if "CONTEO ABIERTO" not in s3:
    fallos.append("CASO 3: no marcó el conteo como abierto")
if "conteos quedaron ABIERTOS" in s3:
    fallos.append("CASO 3: avisó de comparación con un solo país (ruido)")

print("=== RESULTADO DEL BANCO ===")
if fallos:
    for f in fallos:
        print("  ❌", f)
    sys.exit(1)
print("  ✅ 3 de 3: muerde con dos abiertos, calla con conteos cerrados, y no hace ruido con uno solo")
print("\n--- lo que imprime en el caso 1 ---")
print("\n".join(l for l in s1.splitlines() if "🚨" in l or "ABIERTO" in l))
