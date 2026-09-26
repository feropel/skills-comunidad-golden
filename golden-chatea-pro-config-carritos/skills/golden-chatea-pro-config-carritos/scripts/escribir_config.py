#!/usr/bin/env python3
"""Escribe en [Carritos] Configuracion SOLO las llaves que cambian, y lo demuestra releyendo.

Vía API = espacio propio de FER o VIP (o cuando FER lo pide). La instalación normal se entrega
campo por campo para pegar en el panel.

Orden, y ninguno se salta:
  1. lee en vivo  2. verifica que el espacio es el esperado (--tienda)  3. respalda
  4. parchea SOLO las llaves de la propuesta sobre el valor vivo  5. mide cada texto en UTF-16
     contra su tope  6. PUT  7. relee del servidor y compara el JSON PARSEADO (la API recorta el
     salto de linea final)  8. comprueba que el resto del campo no se movio

La propuesta es un JSON {"seccion.llave": valor}, p. ej.
  {"datos_logisticos.transportadoras_disponibles": "Sin X. A, B (tambien oficina), C."}

Uso:  python3 escribir_config.py --token-file RUTA --tienda "Nombre exacto" --propuesta p.json \
          --respaldo-dir DIR [--seco]
"""
import argparse
import datetime
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from chatea_api import Api, CAMPO, valor, get, put, u16  # noqa: E402
from validar_config import validar  # noqa: E402

with open(os.path.join(AQUI, "..", "assets", "limites.json"), encoding="utf-8") as _f:
    TOPES = json.load(_f)["capa_nativa"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token-file", required=True)
    p.add_argument("--tienda", required=True, help="nombre_tienda que DEBE tener el espacio")
    p.add_argument("--propuesta", required=True)
    p.add_argument("--respaldo-dir", required=True)
    p.add_argument("--seco", action="store_true", help="mide y muestra, no escribe")
    p.add_argument("--dueño-confirmo-datos-de-pago", dest="dueno", action="store_true",
                   help="obligatorio si la propuesta toca datos_pago_anticipado")
    a = p.parse_args()

    api = Api(a.token_file)
    campos = api.campos()
    if CAMPO not in campos:
        sys.exit(f"ABORTA: no existe {CAMPO}")
    vivo = valor(campos[CAMPO])
    tienda = vivo.get("datos_tienda", {}).get("nombre_tienda")
    if tienda != a.tienda:
        sys.exit(f"ABORTA: el espacio dice tienda={tienda!r}, se esperaba {a.tienda!r}")

    with open(a.propuesta, encoding="utf-8") as f:
        prop = json.load(f)
    nuevo = json.loads(json.dumps(vivo))
    cambian = []
    for k, v in prop.items():
        try:
            actual = get(vivo, k)
        except (KeyError, TypeError):
            sys.exit(f"ABORTA: llave desconocida {k}")
        tope = TOPES.get(k.split(".")[-1])
        if isinstance(v, str) and tope and u16(v) > tope:
            sys.exit(f"ABORTA: {k} mide {u16(v)} y su tope es {tope}")
        if actual != v:
            cambian.append(k)
            put(nuevo, k, v)
        print(f"  {'CAMBIA' if actual != v else 'igual '} {k}"
              + (f"  {u16(v)}/{tope}" if isinstance(v, str) and tope else ""))
    if any(k.endswith("datos_pago_anticipado") for k in cambian) and not a.dueno:
        sys.exit("ABORTA: la propuesta cambia datos_pago_anticipado. Lleva medio de pago, titular y "
                 "numero: solo lo da el DUEÑO de este espacio. Confirmalo y pasa "
                 "--dueño-confirmo-datos-de-pago.")
    criticas, avisos = validar(nuevo, dueno_confirmo=True)
    for x in avisos:
        print("  🟠", x)
    if criticas:
        for x in criticas:
            print("  🔴", x)
        sys.exit("ABORTA: el resultado tendria criticas. No se escribe una configuracion rota.")
    if not cambian or a.seco:
        print("nada que escribir" if not cambian else "modo seco: no se escribe")
        return

    os.makedirs(a.respaldo_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta = os.path.join(a.respaldo_dir, f"carritos-ANTES-{ts}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(campos[CAMPO], f, ensure_ascii=False, indent=2)
    print("respaldo:", ruta)

    api.escribir({CAMPO: nuevo})
    time.sleep(3)
    srv = valor(api.campos()[CAMPO])
    ok = 0
    for k in cambian:
        s, e = get(srv, k), get(nuevo, k)
        igual = (s.rstrip("\n") == e.rstrip("\n")) if isinstance(e, str) else s == e
        ok += igual
        print(f"  {'OK ' if igual else 'MAL'} {k}")
    x, y = json.loads(json.dumps(srv)), json.loads(json.dumps(vivo))
    for k in cambian:
        put(x, k, None)
        put(y, k, None)
    print(f"VERIFICADO DEL SERVIDOR: {ok} de {len(cambian)} · resto intacto: {x == y} · "
          f"cupo: {api.cupo}")
    print("Recordar al dueño: recargar la pestaña del panel ANTES de guardar ahí.")
    sys.exit(0 if ok == len(cambian) and x == y else 1)


if __name__ == "__main__":
    main()
