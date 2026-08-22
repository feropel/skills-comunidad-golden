#!/usr/bin/env python3
"""Banco del lector de la Torre. Los dos contratos reales + uno inventado que MUERE.

EL CASO ES UNA ROTURA EN PRODUCCION del 2026-08-16, y de las caras: la rutina que
regenera `TORRE-MUNICIPIOS.json` migro a la API FENIX y cambio la forma de las filas
**sin version de esquema y sin avisar**. El motor canonico murio con
`TypeError: list indices must be integers or slices, not str` dentro de un dict
comprehension — **para cualquier tienda**, y sin nombrar el archivo, ni la fecha, ni la
fila. Un insumo externo cambia cuando quiere; el que lo lee es quien tiene que estar
preparado, y quien tiene que hablar cuando ya no entiende lo que le dan.

TRES CASOS, Y EL TERCERO ES EL QUE IMPORTA. Aceptar los dos formatos conocidos es la
parte facil: cualquier `try/except` amplio la aprueba. Lo que este banco exige es que la
forma DESCONOCIDA **muera con un mensaje que nombre el archivo, la fecha y la fila** — o
sea, que la proxima vez que esto pase, el que llegue a las siete de la manana sepa en
diez segundos que paso. Un lector tolerante que se traga lo que no entiende no es
robusto: es el mismo fallo, callado.

  python3 prueba_torre.py
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decidir_transportadora import fila_torre   # noqa: E402

SK = os.path.dirname(os.path.abspath(__file__))
FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def main():
    print("banco del lector de la Torre · dos contratos reales + uno que debe morir\n")

    # 1 · LA FILA-OBJETO (contrato viejo, textual del insumo canonico del 11-ago)
    vieja = {"t": "ENVIA", "pct": 81.93, "ent": 38353, "dev": 8457,
             # La cola decimal va RECORTADA a proposito: copiada literal de la Torre real,
             # sus digitos contenian una secuencia que el detector de privacidad lee como
             # telefono. Es un falso positivo — pero se arregla el FIXTURE, no el patron:
             # un guardia que estorba y se afloja para que pase una prueba muere apagado,
             # no derrotado. Y un banco solo necesita la FORMA del dato, nunca su cola.
             "dias": 2.82, "flete": 18712.6}
    f = fila_torre(vieja)
    juzgar("fila-objeto: nombre y porcentaje", f["t"] == "ENVIA" and f["pct"] == 81.93)
    juzgar("fila-objeto: `n` es la SUMA de ent+dev", f["n"] == 38353 + 8457, str(f["n"]))
    juzgar("fila-objeto: conserva ent/dev y dias", f["ent"] == 38353 and f["dias"] is not None)

    # 2 · LA FILA-LISTA (contrato nuevo, textual del archivo del 16-ago)
    nueva = ["INTERRAPIDISIMO", 71.67, 7629]
    f = fila_torre(nueva)
    juzgar("fila-lista: nombre y porcentaje", f["t"] == "INTERRAPIDISIMO" and f["pct"] == 71.67)
    juzgar("fila-lista: `n` es el total que ya viene sumado", f["n"] == 7629, str(f["n"]))
    juzgar("fila-lista: ent/dev quedan en None, NO en cero",
           f["ent"] is None and f["dev"] is None, f"ent={f['ent']}")
    # ESTE ES EL QUE EVITA EL NUMERO FALSO. Con `m.get("dias", 0)` el informe habria
    # impreso «0 dias de entrega» para toda la cuenta: un dato inventado con cara de
    # medido, que es peor que la caida.
    juzgar("fila-lista: `dias` es None, NUNCA 0", f["dias"] is None, f"dias={f['dias']}")

    # 3 · LA FORMA DESCONOCIDA MUERE
    for mala, que in ((["ENVIA", "73.83"], "lista de 2"),
                      (["ENVIA", 73.83, 149568, 4.1], "lista de 4"),
                      ({"nombre": "ENVIA", "entrega": 73.83}, "objeto con otras claves"),
                      (["ENVIA", "COORDINADORA", "VELOCES"], "lista de 3 toda de textos"),
                      ("ENVIA", "un texto suelto"), (None, "nulo")):
        try:
            fila_torre(mala)
            juzgar(f"forma desconocida ({que}) muere", False, "la acepto en silencio")
        except (ValueError, TypeError):
            juzgar(f"forma desconocida ({que}) muere", True)

    # 4 · Y EL MOTOR ENTERO MUERE HABLANDO, no con un TypeError crudo.
    #     Sin esto, el banco probaria la funcion y no la compuerta: el fallo de produccion
    #     no fue que `fila_torre` no existiera — fue que el mensaje no decia nada.
    tmp = tempfile.mkdtemp()
    torre = os.path.join(tmp, "torre.json")
    with open(torre, "w", encoding="utf-8") as fh:
        json.dump({"generado": "2026-09-01", "rango": "una ventana cualquiera",
                   "fuente": "un formato que nadie ha visto",
                   "TC": {"AMAZONAS|LETICIA": [{"transportadora": "ENVIA", "entrega": 71.6}]}}, fh)
    # LOS DEMAS INSUMOS VAN VALIDOS A PROPOSITO. La primera version de este caso los
    # dejo en "x" y el motor murio ANTES, al abrir el volcado — o sea que el banco no
    # llegaba a tocar la compuerta que venia a probar. Lo dijo en vez de darse verde
    # («NO SE PUDO JUZGAR»), que es justo para lo que existe esa rama; pero un caso que
    # nunca alcanza su objetivo no prueba nada, asi que se arregla el caso.
    def _j(nombre, dato):
        ruta = os.path.join(tmp, nombre)
        with open(ruta, "w", encoding="utf-8") as fh:
            json.dump(dato, fh)
        return ruta

    cfg = _j("cfg.json", {
        "torre": torre,
        "dropi": _j("dropi.json", {"cosecha_completa": True, "ordenes": [],
                                   "accionables": [], "couriers": {}}),
        "fletes": _j("fletes.json", {"R": []}),
        "retorno": _j("retorno.json", {"medido_2026-01-01": {}}),
        "calibracion": _j("cal.json", {"factor": 1.0, "_calculado": "2026-01-01"}),
        "operativas": ["ENVIA"], "margen": 0.6, "salida": os.path.join(tmp, "out.json")})
    r = subprocess.run([sys.executable, os.path.join(SK, "decidir_transportadora.py"),
                        "--config", cfg], capture_output=True, text=True, timeout=60)
    salida = (r.stdout or "") + (r.stderr or "")
    juzgar("el motor NO revienta con un TypeError crudo",
           "TypeError" not in salida or "ESQUEMA DESCONOCIDO" in salida,
           salida.strip().splitlines()[-1][:70] if salida.strip() else "sin salida")
    # El mensaje tiene que servirle a quien llega a las 7am: archivo, fila y fecha.
    if "ESQUEMA DESCONOCIDO" in salida:
        juzgar("el mensaje nombra el ARCHIVO", torre in salida)
        juzgar("el mensaje muestra la FILA que no entendio", "transportadora" in salida)
        juzgar("el mensaje da la FECHA en que se genero", "2026-09-01" in salida)
    else:
        # Puede morir antes por el volcado inexistente: es legitimo, pero entonces este
        # banco NO ha probado la compuerta y lo dice en vez de dar verde.
        juzgar("NO SE PUDO JUZGAR el mensaje de la compuerta (murio antes, por otro insumo)",
               False, salida.strip().splitlines()[-1][:70] if salida.strip() else "sin salida")

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + "; ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del lector de la Torre pasaron")


if __name__ == "__main__":
    main()
