#!/usr/bin/env python3
"""Banco del INCREMENTAL de barrer_chats.py. Red simulada, cero llamadas reales.

POR QUE EXISTE: el incremental es la pieza que decide si la Parte A es una rutina
diaria o no existe. Medido: 900 contactos a ritmo suave son ~5 horas, casi todas en
reintentos de 429, y sin incremental una corrida cortada se pierde ENTERA.

Lo que comprueba, y cada caso nacio de un modo real de fallar:
  1. Con --previo NO se vuelve a pedir lo que ya estaba. Si lo pidiera, el incremental
     no ahorra nada y solo añade una fuente de error.
  2. Acepta un previo PARCIAL (cosecha_completa=false). Rechazarlo tiraria a la basura
     el presupuesto de 429 ya gastado, que es justo lo que se quiere salvar.
  3. El archivo DECLARA la mezcla: cuanto vino del previo, cuanto fresco, y de cuando
     es el dato mas viejo. Un archivo de dos corridas son dos fotos y tiene que decirlo.
  4. `cosecha_completa` se DERIVA: reusados + frescos == pedidos y sin fallos.
  5. Un previo ilegible MATA la corrida con mensaje, en vez de rebarrer entero en
     silencio — que costaria horas de 429 sin que nadie lo pidiera.

  python3 prueba_previo.py [ruta de barrer_chats.py]
"""
import json, os, subprocess, sys, tempfile

RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "barrer_chats.py")

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def correr(tmp, contactos, previo=None):
    """Corre barrer_chats con un urllib falso. Devuelve (salida, ns_pedidos)."""
    co = os.path.join(tmp, "co.json")
    sa = os.path.join(tmp, "sa.json")
    tk = os.path.join(tmp, "tk.txt")
    pedidos = os.path.join(tmp, "pedidos.txt")
    json.dump(contactos, open(co, "w"))
    open(tk, "w").write("token-de-mentira")
    open(pedidos, "w").close()

    shim = f'''
import json, sys, urllib.request, re
PEDIDOS = {pedidos!r}
class _R:
    def __init__(s, b): s._b = b
    def read(s): return s._b
    def __enter__(s): return s
    def __exit__(s, *a): return False
def _fake(req, timeout=None):
    url = req.full_url if hasattr(req, "full_url") else str(req)
    ns = re.search(r"user_ns=([^&]+)", url).group(1)
    open(PEDIDOS, "a").write(ns + "\\n")
    msgs = [{{"type": "in", "content": "hola", "ts": 100}},
            {{"type": "out", "content": "buenas", "ts": 200}}]
    return _R(json.dumps({{"data": msgs, "meta": {{"last_page": 1}}}}).encode())
urllib.request.urlopen = _fake
sys.argv = {["barrer_chats.py", "--contactos", co, "--token", tk, "--salida", sa,
             "--hilos", "2", "--pausa", "0"] + (["--previo", previo] if previo else [])!r}
g = dict(globals()); g['__file__'] = {RUTA!r}; g['__name__'] = '__main__'
exec(compile(open({RUTA!r}).read(), {RUTA!r}, 'exec'), g)
'''
    r = subprocess.run([sys.executable, "-c", shim], capture_output=True, text=True)
    pedidos_ns = [l.strip() for l in open(pedidos).read().splitlines() if l.strip()]
    salida = json.load(open(sa)) if os.path.exists(sa) else None
    return salida, pedidos_ns, r


def main():
    print(f"banco del incremental · {RUTA}\n")
    contactos = [{"user_ns": f"ns{i}"} for i in range(6)]

    with tempfile.TemporaryDirectory() as tmp:
        # --- corrida limpia: los pide todos ---
        s0, p0, _ = correr(tmp, contactos)
        juzgar("sin previo pide los 6", len(p0) == 6, f"pidio {len(p0)}")
        juzgar("sin previo, cosecha_completa derivada true", s0 and s0["cosecha_completa"] is True)

    with tempfile.TemporaryDirectory() as tmp:
        # --- previo PARCIAL con 4 de 6 ---
        previo = os.path.join(tmp, "prev.json")
        json.dump({"generado": "2026-08-10T09:00:00", "cosecha_completa": False,
                   "chats": {f"ns{i}": [{"t": "in", "c": "viejo", "ts": 1}] for i in range(4)}},
                  open(previo, "w"))
        s1, p1, r1 = correr(tmp, contactos, previo)
        juzgar("con previo parcial solo pide los 2 que faltan", len(p1) == 2,
               f"pidio {len(p1)}: {p1}")
        juzgar("acepta un previo INCOMPLETO", s1 is not None)
        juzgar("no re-pide lo que ya estaba", all(x not in p1 for x in ("ns0", "ns1", "ns2", "ns3")))
        juzgar("reusa los 4 y suma los 2", s1 and len(s1["chats"]) == 6,
               f"{len(s1['chats']) if s1 else '?'} conversaciones")
        juzgar("DECLARA la mezcla: reusados",
               s1 and s1.get("reusados_del_previo") == 4, f"{s1.get('reusados_del_previo')}")
        juzgar("DECLARA la mezcla: frescos",
               s1 and s1.get("bajados_frescos") == 2, f"{s1.get('bajados_frescos')}")
        juzgar("DECLARA de cuando es el dato mas viejo",
               s1 and s1.get("dato_mas_viejo_reusado") == "2026-08-10T09:00:00")
        juzgar("marca que es incremental", s1 and s1.get("incremental") is True)
        juzgar("cosecha_completa se DERIVA y da true", s1 and s1["cosecha_completa"] is True)
        juzgar("el dato reusado NO se pisa con el fresco",
               s1 and s1["chats"]["ns0"][0].get("c") == "viejo")

    with tempfile.TemporaryDirectory() as tmp:
        # --- previo ilegible: muere con mensaje, NO rebarre entero ---
        malo = os.path.join(tmp, "malo.json")
        open(malo, "w").write("{esto no es json")
        s2, p2, r2 = correr(tmp, contactos, malo)
        juzgar("previo ilegible: no baja nada", len(p2) == 0, f"pidio {len(p2)}")
        juzgar("previo ilegible: muere con mensaje legible",
               "No se pudo leer el previo" in (r2.stdout + r2.stderr))

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + ", ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del incremental pasaron")


if __name__ == "__main__":
    main()
