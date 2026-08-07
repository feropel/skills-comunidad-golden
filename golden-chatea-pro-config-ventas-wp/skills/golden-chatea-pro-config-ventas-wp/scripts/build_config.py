#!/usr/bin/env python3
"""
build_config.py — Genera los 2 Bot Fields JSON NATIVOS de la configuración
general del asistente de ventas WhatsApp de Chatea Pro (esquema verificado
contra un workspace real el 2026-07-09).

En Chatea Pro la configuración general vive en 2 Bot Fields de tipo JSON
(tipo LONG JSON, máx 500000 caracteres cada uno, carpeta del agente de ventas):
    Campo 1 "[Ventas Wp] Configuracion general"   → Dropi, validaciones,
              Producto en Segundos, notificaciones
    Campo 2 "[Ventas Wp] Configuracion general 2" → comportamiento de la IA
              (división, rol, restricciones, análisis de palabra clave)

El flujo del bot lee las claves por NOMBRE: no se renombran. Los prompts del
motor viven en assets/prompts/ y NUNCA se recortan; lo que cambia por tienda
es el intake:

    --pais            País del workspace, va en minúscula (ej: colombia)
    --moneda          Moneda (ej: COP)
    --flete-max       Flete máximo para validar la orden (ej: 23000)
    --whatsapp-notif  WhatsApp que recibe las notificaciones (+57 3XX...)
    --url-tienda      URL de la tienda (redirige productos no configurados)
    --dropi           si | no (default: si)
    --prompt-maestro  (opcional) .txt con el prompt maestro de Producto en
                      Segundos (se genera con golden-chatea-pro-prompt-ventas)
    --out-prefix      Prefijo de salida; escribe <prefix>_BOTFIELD_1.json
                      y <prefix>_BOTFIELD_2.json

Uso:
    python3 build_config.py --pais "colombia" --moneda "COP" \
        --flete-max "23000" --whatsapp-notif "+57 3001234567" \
        --url-tienda "https://mitienda.co" \
        --prompt-maestro /ruta/prompt_maestro.txt \
        --out-prefix /ruta/<negocio>

Valida contra assets/limites.json: el total de cada Bot Field ≤ el tope de su
TIPO (LONG JSON = 500000; JSON antiguo = 20000) y cada
prompt dentro de su límite de la UI (así el mismo texto sirve también por la
vía manual de Entrenar). Exit 1 si algo excede.
"""
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SCRIPT_DIR, "..", "assets")
PROMPTS = os.path.join(ASSETS, "prompts")

with open(os.path.join(ASSETS, "limites.json"), encoding="utf-8") as _f:
    _lim = json.load(_f)
LIMITES = _lim["capa1"]
MAX_BOT_FIELD = _lim["bot_fields"]["max_por_campo"]


def leer_prompt(nombre):
    with open(os.path.join(PROMPTS, nombre), encoding="utf-8") as f:
        return f.read().strip()


def leer_template(nombre):
    with open(os.path.join(ASSETS, nombre), encoding="utf-8") as f:
        return json.load(f)


def sin_meta(nodo):
    """Elimina recursivamente las claves _meta de documentación del template."""
    if isinstance(nodo, dict):
        return {k: sin_meta(v) for k, v in nodo.items() if not k.startswith("_")}
    if isinstance(nodo, list):
        return [sin_meta(x) for x in nodo]
    return nodo


def construir(a):
    campo1 = sin_meta(leer_template("template-botfield-1-configuracion.json"))
    campo2 = sin_meta(leer_template("template-botfield-2-comportamiento.json"))

    campo1["conexion_con_dropi"]["conectar"] = a.dropi
    campo1["conexion_con_dropi"]["pais"] = a.pais.lower()
    flete = campo1["acciones_especiales"]["validaciones_orden"]["validar_flete"]
    flete["flete_minimo"] = a.flete_max
    flete["moneda"] = a.moneda
    if a.dropi == "no":
        campo1["acciones_especiales"]["validaciones_orden"]["subida_automatica"] = "no"

    ps = campo1["producto_segundos"]
    ps["prompt_datos"] = leer_prompt("reglas-estructura-producto.txt")
    if a.prompt_maestro:
        with open(a.prompt_maestro, encoding="utf-8") as f:
            ps["prompt_prompt"] = f.read().strip()

    notif = campo1["notificaciones"]["notificacion_1"]
    notif["whatsapp"] = a.whatsapp_notif
    notif["mensaje"] = leer_prompt("notificacion-venta-realizada.txt")

    comp = campo2["comportamiento_ia"]
    comp["rol"] = leer_prompt("rol-general.txt")
    comp["restricciones"] = leer_prompt("restricciones.txt")
    comp["analizar_palabra"]["prompt"] = leer_prompt(
        "analisis-palabra-clave.txt"
    ).replace("{{URL_TIENDA}}", a.url_tienda)
    return campo1, campo2


def reporte(campo1, campo2):
    ok = True
    print("Prompts vs límites de la UI (sirven también por la vía Entrenar):")
    campos = {
        "reglas_estructura": (campo1["producto_segundos"]["prompt_datos"], "reglas_estructura"),
        "prompt_maestro": (campo1["producto_segundos"]["prompt_prompt"], "prompt_maestro"),
        "mensaje_notificacion": (campo1["notificaciones"]["notificacion_1"]["mensaje"], "mensaje_libre"),
        "rol": (campo2["comportamiento_ia"]["rol"], "rol_general"),
        "restricciones": (campo2["comportamiento_ia"]["restricciones"], "restricciones_generales"),
        "prompt_analisis": (campo2["comportamiento_ia"]["analizar_palabra"]["prompt"], "prompt_analisis"),
    }
    for nombre, (texto, clave) in campos.items():
        lim = LIMITES[clave]
        n = len(texto)
        estado = "OK" if n <= lim else f"EXCEDE por {n - lim}"
        if n > lim:
            ok = False
        print(f"  {nombre}: {n} / {lim}  {estado}")

    print(f"\nTotal por Bot Field (límite duro de Chatea Pro: {MAX_BOT_FIELD}):")
    for nombre, campo in (("BOTFIELD_1", campo1), ("BOTFIELD_2", campo2)):
        n = len(json.dumps(campo, ensure_ascii=False, indent=2))
        estado = "OK" if n < MAX_BOT_FIELD else f"EXCEDE por {n - MAX_BOT_FIELD + 1}"
        if n >= MAX_BOT_FIELD:
            ok = False
        print(f"  {nombre}: {n} / <{MAX_BOT_FIELD}  {estado}")

    if "{{PROMPT_MAESTRO}}" in campo1["producto_segundos"]["prompt_prompt"]:
        print("\n⚠️  Prompt maestro pendiente: genéralo con golden-chatea-pro-prompt-ventas")
        print("    (prompt de negocio) y vuelve a correr con --prompt-maestro.")
    if not ok:
        print("\n⚠️  Algo excede. NO recortes los prompts fijos: acorta el prompt maestro")
        print("    o lo variable del intake.")
    return ok


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pais", required=True)
    p.add_argument("--moneda", required=True)
    p.add_argument("--flete-max", dest="flete_max", required=True)
    p.add_argument("--whatsapp-notif", dest="whatsapp_notif", required=True)
    p.add_argument("--url-tienda", dest="url_tienda", required=True)
    p.add_argument("--dropi", choices=["si", "no"], default="si")
    p.add_argument("--prompt-maestro", dest="prompt_maestro")
    p.add_argument("--out-prefix", dest="out_prefix", required=True)
    a = p.parse_args()

    campo1, campo2 = construir(a)
    ok = reporte(campo1, campo2)
    for sufijo, campo in (("_BOTFIELD_1.json", campo1), ("_BOTFIELD_2.json", campo2)):
        ruta = a.out_prefix + sufijo
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(json.dumps(campo, ensure_ascii=False, indent=2))
        print(f"Guardado: {ruta}")
    print('\nPegar en Chatea Pro → Bot Fields → carpeta del agente de ventas:')
    print('  _BOTFIELD_1.json → campo "[Ventas Wp] Configuracion general"')
    print('  _BOTFIELD_2.json → campo "[Ventas Wp] Configuracion general 2"')
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
