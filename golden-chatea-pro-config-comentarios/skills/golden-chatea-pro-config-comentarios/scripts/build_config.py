#!/usr/bin/env python3
"""
build_config.py
Arma el JSON de configuración de Chatea Pro para una tienda.

Los prompts (comentarios negativos, respuesta pública, venta conversacional)
son FIJOS: se toman tal cual de assets/template.json y NUNCA se modifican.
Lo único que cambia por tienda es la información del negocio, que el skill
PREGUNTA al ejecutarse:
    1. pais
    2. contacto (página / WhatsApp / correo, solo referencia)
    3. t_envio  (tiempos de envío)
    4. info_extra (info adicional del negocio)

Además, el script genera el campo `datos_req` dentro de venta_conversacional
(en Chatea Pro: "datos que la IA debe solicitar al cliente para completar la
compra"). Esta lista se ARMA SEGÚN EL PAÍS y su nomenclatura de direcciones:
    - Colombia: Nombre completo; Número de WhatsApp; Dirección exacta;
                Barrio o punto de referencia; Ciudad; Departamento
    - Otros países (México y similares): Nombre completo; Número de WhatsApp;
                Dirección exacta; Colonia; Ciudad / Municipio; Estado;
                Código Postal
Se puede forzar una lista manual con --datos-cliente.

Cantidad y precios NO se piden aquí: van en la ficha del producto dentro de
Chatea Pro, no en esta configuración general.

Uso:
    python3 build_config.py \
        --pais "colombia" \
        --contacto "WhatsApp: +57 ..." \
        --t-envio "Ciudad principal: 2 a 3 días ..." \
        --info-extra "Empresa colombiana ..." \
        --out /ruta/salida_CONFIG.json

También acepta un archivo de intake JSON:
    python3 build_config.py --intake intake.json --out salida.json
"""
import argparse
import json
import os
import sys

# El tope lo pone el TIPO del Bot Field, no la plataforma (medido por API 2026-07-25):
#   tipo JSON (var_type text/array) = 20.000   ·   tipo LONG JSON (longtext) = 500.000
# El campo se crea LONG JSON. LIMITE_JSON queda para avisar cuando el campo del
# cliente todavía sea del tipo viejo. Pasarse NO da error: la API responde 200 ok
# y guarda el JSON CORTADO, así que siempre hay que releer y comparar.
LIMITE_JSON = 20000
LIMITE_TOTAL = 500000
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(SCRIPT_DIR, "..", "assets", "template.json")

# Datos que la IA debe pedirle al cliente para completar la compra,
# por país y según su nomenclatura de direcciones.
DATOS_COLOMBIA = ("Nombre completo; Número de WhatsApp; Dirección exacta; "
                  "Barrio o punto de referencia; Ciudad; Departamento")
DATOS_INTERNACIONAL = ("Nombre completo; Número de WhatsApp; Dirección exacta; "
                       "Colonia; Ciudad / Municipio; Estado; Código Postal")

# Países que usan el esquema "Estado / Colonia / Código Postal".
PAISES_ESTADO_CP = {
    "mexico", "méxico", "argentina", "venezuela", "peru", "perú",
    "chile", "ecuador", "guatemala", "panama", "panamá",
    "estados unidos", "usa", "eeuu",
}


def datos_req_por_pais(pais, override=None):
    """Devuelve la lista de datos a solicitar al cliente según el país.

    Si se pasa `override`, se usa tal cual (lista manual del usuario).
    """
    if override:
        return override.strip()
    clave = (pais or "").strip().lower()
    if clave in {"colombia", "co"}:
        return DATOS_COLOMBIA
    if clave in PAISES_ESTADO_CP:
        return DATOS_INTERNACIONAL
    # Por defecto, si no se reconoce el país, se asume esquema internacional
    # (Estado / Colonia / Código Postal) para no quedarnos con campos de Colombia.
    return DATOS_INTERNACIONAL


def cargar_template():
    with open(TEMPLATE, encoding="utf-8") as f:
        return json.load(f)


def construir(pais, contacto, t_envio, info_extra, datos_cliente=None):
    cfg = cargar_template()
    # Solo se reemplaza la información del negocio. Los prompts quedan intactos.
    cfg["informacion_del_negocio"]["pais"] = pais
    cfg["informacion_del_negocio"]["contacto"] = contacto
    cfg["informacion_del_negocio"]["t_envio"] = t_envio
    cfg["informacion_del_negocio"]["info_extra"] = info_extra
    # Datos que la IA debe solicitar al cliente, según el país.
    cfg["venta_conversacional"]["datos_req"] = datos_req_por_pais(pais, datos_cliente)
    return cfg


def reporte(cfg):
    out = json.dumps(cfg, ensure_ascii=False, indent=4)
    total = len(out)
    print(f"JSON total: {total} / {LIMITE_TOTAL}", "OK" if total <= LIMITE_TOTAL else f"EXCEDE por {total - LIMITE_TOTAL}")
    ib = cfg["informacion_del_negocio"]
    print(f"  pais:       {len(ib['pais'])}")
    print(f"  contacto:   {len(ib['contacto'])} / 200")
    print(f"  t_envio:    {len(ib['t_envio'])} / 200")
    print(f"  info_extra: {len(ib['info_extra'])} / 500")
    print(f"  datos_req:  {cfg['venta_conversacional']['datos_req']}")
    if total > LIMITE_TOTAL:
        print()
        print(f"⚠️  El JSON supera {LIMITE_TOTAL} — ni LONG JSON aguanta esto.")
        print(f"    Sobran {total - LIMITE_TOTAL} caracteres.")
    elif total > LIMITE_JSON:
        print()
        print(f"ℹ️  El JSON usa {total} caracteres: cabe en un campo LONG JSON (500.000)")
        print(f"    pero NO en uno tipo JSON ({LIMITE_JSON}).")
        print("    → Verifica que el Bot Field sea LONG JSON antes de pegarlo. Si es")
        print("      tipo JSON, la plataforma lo corta EN SILENCIO y responde 'ok'.")
        print("    → Si no puedes cambiar el tipo: NO recortes los prompts, acorta los")
        print("      campos de negocio (contacto / t_envio / info_extra).")
    return out, total


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--intake", help="Archivo JSON con pais, contacto, t_envio, info_extra")
    p.add_argument("--pais")
    p.add_argument("--contacto")
    p.add_argument("--t-envio", dest="t_envio")
    p.add_argument("--info-extra", dest="info_extra")
    p.add_argument("--datos-cliente", dest="datos_cliente",
                   help="Lista manual de datos a pedir al cliente (separados por ;). "
                        "Si se omite, se genera según el país.")
    p.add_argument("--out", required=True, help="Ruta del JSON de salida")
    a = p.parse_args()

    if a.intake:
        with open(a.intake, encoding="utf-8") as f:
            d = json.load(f)
        pais = d.get("pais", a.pais)
        contacto = d.get("contacto", a.contacto)
        t_envio = d.get("t_envio", a.t_envio)
        info_extra = d.get("info_extra", a.info_extra)
        datos_cliente = d.get("datos_cliente", a.datos_cliente)
    else:
        pais, contacto, t_envio, info_extra = a.pais, a.contacto, a.t_envio, a.info_extra
        datos_cliente = a.datos_cliente

    faltan = [n for n, v in [("pais", pais), ("contacto", contacto), ("t_envio", t_envio), ("info_extra", info_extra)] if not v]
    if faltan:
        print("Faltan datos del intake:", ", ".join(faltan))
        print("El skill debe preguntarlos antes de armar el JSON.")
        sys.exit(1)

    cfg = construir(pais, contacto, t_envio, info_extra, datos_cliente)
    out, total = reporte(cfg)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"\nGuardado en: {a.out}")


if __name__ == "__main__":
    main()
