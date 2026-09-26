#!/usr/bin/env python3
"""Mide un valor de bot field contra los DOS techos de Chatea Pro.

Techo A (bot field JSON legacy): el flujo copia la config ESCAPADA — regla dura de la casa
escapado < 19.000 (medido 2026-08-07: 19.895 escapados arranca, 23.266 muere en silencio con
la API respondiendo 200). Techo B: tope NATIVO del campo del panel (opcional, --tope N):
escribir por encima funciona por API pero el panel corta al guardar.

Uso:
  python3 medir_techos.py archivo.json            # el archivo ES el valor del campo
  python3 medir_techos.py archivo.txt --texto     # texto plano (prompt suelto)
  python3 medir_techos.py archivo.json --tope 8000
  python3 medir_techos.py --autoprueba              # el banco (7 casos, los dos sentidos)
Salida 0 = dentro de los techos · 1 = VIOLA un techo (no escribir) · 2 = no se pudo leer.
Detalle de tablas y gotchas: references/api-y-techos.md.
"""
import json, sys

LIMITE_ESCAPADO = 19000  # regla dura de la casa (mas estricta que el fallo real en 20.000)


def autoprueba():
    """Banco de los DOS sentidos. Antes del 2026-09-07 este script no lo tenia: media los
    techos que deciden si un asistente vive o muere en silencio, y nadie habia comprobado que
    mordiera. Ley de la casa: si tu script dice que todo esta bien a la primera, sospecha del
    script -- pruebalo contra un caso que sepas malo."""
    import os
    import subprocess
    import tempfile
    casos, ok = [], 0
    yo = os.path.abspath(__file__)

    def corre(contenido, extra=None, texto=False):
        suf = ".txt" if texto else ".json"
        with tempfile.NamedTemporaryFile("w", suffix=suf, delete=False,
                                         encoding="utf-8") as f:
            f.write(contenido if texto else json.dumps(contenido, ensure_ascii=False))
            ruta = f.name
        try:
            cmd = [sys.executable, yo, ruta] + (["--texto"] if texto else []) + (extra or [])
            r = subprocess.run(cmd, capture_output=True, text=True)
            return r.returncode, r.stdout + r.stderr
        finally:
            os.unlink(ruta)

    # 1 · un valor pequeno pasa. Un medidor que siempre bloquea tampoco discrimina.
    ec, _ = corre({"a": "x" * 100})
    casos.append(("un valor pequeno PASA", ec == 0))

    # 2 · un valor por encima del techo A tiene que MORDER
    ec, sal = corre({"a": "x" * 25000})
    casos.append(("muerde el TECHO A (escapado > 19.000)", ec == 1))

    # 3 · 🔴 LA TRAMPA QUE ESTE SCRIPT EXISTE PARA CAZAR: el escapado no es el crudo.
    #     Cada tilde ocupa 6 caracteres escapados y cada emoji 12. Un valor que en CRUDO cabe
    #     de sobra puede reventar el campo por escapado, y la API responde 200 y guarda
    #     cortado. Si este caso no muerde, el script mide crudos y no sirve para nada.
    tildes = {"a": "á" * 4000}          # 4.000 crudos · ~24.000 escapados
    ec, sal = corre(tildes)
    casos.append(("🔴 muerde por ESCAPADO lo que en CRUDO cabria (4.000 tildes)", ec == 1))

    # 4 · el techo B (tope nativo del panel), que es opcional
    ec, _ = corre({"a": "x" * 500}, ["--tope", "100"])
    casos.append(("muerde el TECHO B cuando se pasa --tope", ec == 1))

    # 5 · y NO inventa un techo B cuando no se le pide
    ec, _ = corre({"a": "x" * 500})
    casos.append(("sin --tope NO inventa techo B", ec == 0))

    # 6 · modo texto plano
    ec, _ = corre("hola " * 10, texto=True)
    casos.append(("modo --texto funciona con un prompt suelto", ec == 0))

    # 7 · fichero ilegible se declara, no revienta
    ec, _ = corre("{esto no es json valido", texto=False) if False else (None, "")
    import os as _os
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        f.write("{esto no es json")
        mala = f.name
    try:
        r = subprocess.run([sys.executable, yo, mala], capture_output=True, text=True)
        casos.append(("un JSON invalido sale con codigo propio, sin traza",
                      r.returncode == 2 and "Traceback" not in (r.stdout + r.stderr)))
    finally:
        _os.unlink(mala)

    print("  === AUTOPRUEBA · los dos sentidos ===")
    for n, b in casos:
        ok += b
        print(f"   {'OK ' if b else '🔴 '} {n}")
    print(f"\n  {ok} de {len(casos)}")
    return 0 if ok == len(casos) else 1

def main():
    args = [a for a in sys.argv[1:]]
    if "--autoprueba" in args:
        return autoprueba()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); return 2
    ruta = args[0]
    es_texto = "--texto" in args
    tope = None
    if "--tope" in args:
        try:
            tope = int(args[args.index("--tope") + 1])
        except (IndexError, ValueError):
            print("ERROR: --tope necesita un numero"); return 2
    try:
        crudo_txt = open(ruta, encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: no se pudo leer {ruta}: {e}"); return 2
    if es_texto:
        valor = crudo_txt
    else:
        try:
            valor = json.loads(crudo_txt)
        except json.JSONDecodeError as e:
            print(f"ERROR: el archivo no es JSON valido ({e}); si es texto plano usa --texto")
            return 2
    serial = valor if isinstance(valor, str) else json.dumps(valor, ensure_ascii=False, separators=(",", ":"))
    crudo = len(serial)
    escapado = len(json.dumps(serial, ensure_ascii=True)[1:-1])
    cuatro_bytes = [c for c in serial if ord(c) >= 0x10000]
    print(f"crudo:    {crudo:>7}")
    print(f"escapado: {escapado:>7}  (regla dura < {LIMITE_ESCAPADO})")
    fallo = False
    if escapado >= LIMITE_ESCAPADO:
        print(f"🔴 VIOLA TECHO A: {escapado} escapados >= {LIMITE_ESCAPADO}. NO escribir: la API "
              f"responde 200, guarda cortado y el asistente muere en silencio.")
        fallo = True
    if tope is not None:
        print(f"tope nativo (Techo B): {tope}")
        if crudo > tope:
            print(f"🔴 VIOLA TECHO B: {crudo} crudos > {tope}. El panel corta el campo al guardar.")
            fallo = True
    if cuatro_bytes:
        print(f"⚠️ contiene {len(cuatro_bytes)} caracteres de 4 bytes (emojis): PROHIBIDOS en un "
              f"trigger — el bot no arranca nunca. En prompts son legales pero pesan 12 escapados c/u.")
    if not fallo:
        print("dentro de los techos medidos (esto NO verifica contenido ni coherencia)")
    return 1 if fallo else 0

if __name__ == "__main__":
    sys.exit(main())
