#!/usr/bin/env python3
"""
build_config.py — Genera los 2 Bot Fields JSON NATIVOS de la configuración
general del asistente de ventas WhatsApp de Chatea Pro.

En Chatea Pro la configuración general vive en 2 Bot Fields (carpeta del agente
de ventas), que se crean como tipo LONG JSON:
    Campo 1 "[Ventas Wp] Configuracion general"   -> Dropi, validaciones,
              Producto en Segundos, notificaciones
    Campo 2 "[Ventas Wp] Configuracion general 2" -> comportamiento de la IA
              (division, rol, restricciones, analisis de palabra clave)

El flujo del bot lee las claves por NOMBRE: no se renombran. Los prompts del
motor viven en assets/prompts/ y NUNCA se recortan; lo que cambia por tienda es
el intake.

LOS DOS TECHOS (ver assets/limites.json):
  A) BOT FIELD: el JSON se guarda ESCAPADO (cada tilde 6, cada emoji 12). Se mide
     con len(json.dumps(valor)[1:-1]), NUNCA en crudo. <=19000 cabe en cualquier
     campo; entre 19000 y 500000 solo en LONG JSON; pasarse guarda CORTADO con 200 ok.
  B) CAMPO NATIVO: cada texto respeta su tope de formulario (rol 2000, etc.) o el
     panel lo corta al guardar.
La salida es JSON COMPACTO (separators=(',',':')): otro formato infla el conteo.

    --pais            Uno de los 7 validos (colombia, ecuador, chile, mexico,
                      panama, peru, paraguay). Va en minuscula en el JSON.
    --moneda          Moneda (ej: COP)
    --flete-max       Flete maximo para validar la orden (ej: 23000). OBLIGATORIO
                      solo si --dropi si (el default); sin Dropi (--dropi no) se
                      omite y el JSON queda con "0" (el flujo espera la clave).
    --whatsapp-notif  WhatsApp que recibe las notificaciones (+57 3XX...)
    --url-tienda      URL de la tienda (redirige productos no configurados)
    --dropi           si | no (default: si)
    --prompt-maestro  (OBLIGATORIO: el template trae {{PROMPT_MAESTRO}} — sin esta bandera el script falla con exit 1) .txt con el prompt maestro de Producto en Segundos
    --out-prefix      Prefijo de salida; escribe <prefix>_BOTFIELD_1.json y _2.json

Uso:
    python3 build_config.py --pais "colombia" --moneda "COP" \
        --flete-max "23000" --whatsapp-notif "+57 3001234567" \
        --url-tienda "https://mitienda.co" \
        --prompt-maestro /ruta/prompt_maestro.txt \
        --out-prefix /ruta/<negocio>
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SCRIPT_DIR, "..", "assets")
PROMPTS = os.path.join(ASSETS, "prompts")

with open(os.path.join(ASSETS, "limites.json"), encoding="utf-8") as _f:
    _lim = json.load(_f)
NATIVO = _lim["capa_nativa"]
BOT = _lim["bot_field"]
PAISES = _lim["paises_validos"]


def escapado(valor_str):
    """Cuenta los caracteres ESCAPADOS del valor (como los cuenta el flujo):
    cada tilde 6, cada emoji 12, cada comilla interna +1."""
    return len(json.dumps(valor_str)[1:-1])


def u16(texto):
    """Longitud en unidades UTF-16, como cuenta el formulario del panel (JS .length):
    cada emoji astral vale 2. Para topes nativos (Techo B)."""
    return len((texto or "").encode("utf-16-le")) // 2


def cuatro_bytes(texto):
    """Devuelve los caracteres de 4 bytes (emoji fuera del BMP) que corrompen el
    trigger del bot. El activador de palabra clave NO los admite."""
    return [c for c in (texto or "") if ord(c) >= 0x10000]


def leer_prompt(nombre):
    with open(os.path.join(PROMPTS, nombre), encoding="utf-8") as f:
        return f.read().strip()


def leer_template(nombre):
    with open(os.path.join(ASSETS, nombre), encoding="utf-8") as f:
        return json.load(f)


def sin_meta(nodo):
    """Elimina recursivamente las claves _meta de documentacion del template."""
    if isinstance(nodo, dict):
        return {k: sin_meta(v) for k, v in nodo.items() if not k.startswith("_")}
    if isinstance(nodo, list):
        return [sin_meta(x) for x in nodo]
    return nodo


# Llaves simples runtime legitimas de Chatea (notificacion-venta-realizada.txt).
RUNTIME_LEGITIMAS = {"nombre_cliente", "nombre_producto", "porcentaje_entrega",
                     "telefono_cliente", "valor_venta"}


def validar_huecos(campo, nombre):
    """F2 (verificador 2026-08-08): este script entregaba {{PROMPT_MAESTRO}}
    LITERAL con exit 0 y solo un aviso. Mismo validador que valida_producto:
    dobles {{[^{}]*}} + simples fuera de whitelist => error duro, SIN archivo."""
    texto = json.dumps(campo, ensure_ascii=False)
    errs = []
    dobles = sorted(set(re.findall(r"\{\{[^{}]*\}\}", texto)))
    if dobles:
        errs.append(f"{nombre}: placeholders sin llenar: {', '.join(dobles)}")
    simples = sorted({m for m in re.findall(
        r"(?<!\{)\{([A-Za-z0-9_][A-Za-z0-9_ .\-]*)\}(?!\})", texto)
        if m not in RUNTIME_LEGITIMAS})
    if simples:
        errs.append(f"{nombre}: llave simple sin llenar o desconocida: "
                    + ", ".join("{%s}" % s for s in simples))
    return errs


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
    print("TECHO B — topes nativos del formulario (o el panel corta al guardar):")
    campos = {
        "reglas_estructura (prompt_datos)": (campo1["producto_segundos"]["prompt_datos"], "reglas_estructura"),
        "notificacion.mensaje": (campo1["notificaciones"]["notificacion_1"]["mensaje"], "mensaje_libre"),
        "comportamiento_ia.rol": (campo2["comportamiento_ia"]["rol"], "rol_general"),
        "comportamiento_ia.restricciones": (campo2["comportamiento_ia"]["restricciones"], "restricciones_generales"),
        "analizar_palabra.prompt": (campo2["comportamiento_ia"]["analizar_palabra"]["prompt"], "prompt_analisis"),
    }
    for nombre, (texto, clave) in campos.items():
        lim = NATIVO[clave]
        n = u16(texto)  # UTF-16, como cuenta el panel
        estado = "OK" if n <= lim else f"EXCEDE por {n - lim}"
        if n > lim:
            ok = False
        print(f"  {nombre}: {n} / {lim}  {estado}")

    print("\nTECHO A — bot field, medido ESCAPADO (cada tilde 6, cada emoji 12):")
    valores = {}
    for nombre, campo in (("BOTFIELD_1", campo1), ("BOTFIELD_2", campo2)):
        compacto = json.dumps(campo, ensure_ascii=False, separators=(",", ":"))
        esc = escapado(compacto)
        valores[nombre] = compacto
        if esc <= BOT["seguro_escapado"]:
            estado = "OK (cabe en cualquier tipo de campo)"
        elif esc < BOT["longtext_escapado"]:
            estado = f"AVISO: {esc} > {BOT['seguro_escapado']} — SOLO cabe si el campo es LONG JSON; si es JSON legacy se corta a {BOT['legacy_json_escapado']} y el bot muere"
            print(f"  ⚠️  {nombre}: {esc} escapados / {len(compacto)} crudos  {estado}")
            continue
        else:
            estado = f"EXCEDE el maximo de LONG JSON ({BOT['longtext_escapado']})"
            ok = False
        print(f"  {nombre}: {esc} escapados / {len(compacto)} crudos  {estado}")

    # Techo A: solo bloquea si supera el maximo de LONG JSON; entre seguro y longtext es aviso
    for nombre, compacto in valores.items():
        if escapado(compacto) >= BOT["longtext_escapado"]:
            ok = False

    if not ok:
        print("\n⚠️  Algo excede un tope duro. NO recortes los prompts fijos: acorta el")
        print("    prompt maestro o lo variable del intake.")
    return ok, valores


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pais", required=True)
    p.add_argument("--moneda", required=True)
    p.add_argument("--flete-max", dest="flete_max")
    p.add_argument("--whatsapp-notif", dest="whatsapp_notif", required=True)
    p.add_argument("--url-tienda", dest="url_tienda", required=True)
    p.add_argument("--dropi", choices=["si", "no"], default="si")
    p.add_argument("--prompt-maestro", dest="prompt_maestro")
    p.add_argument("--out-prefix", dest="out_prefix", required=True)
    a = p.parse_args()

    if a.pais.upper() not in PAISES:
        sys.exit(f"Pais '{a.pais}' no valido. Chatea Pro SOLO acepta: {', '.join(PAISES)}. "
                 "Ver references/paises.md para lo que cambia por pais.")

    # --flete-max solo es obligatorio si hay Dropi conectado (valida el pedido contra
    # el flete real). Sin Dropi (--dropi no) el flete no se pregunta (caso borde
    # documentado en SKILL.md); el JSON conserva la clave con "0" porque el flujo la
    # espera, pero validar_flete.esta_activo no se usa sin Dropi.
    if a.dropi == "si" and not a.flete_max:
        sys.exit("Falta --flete-max: obligatorio cuando hay Dropi conectado (--dropi si, "
                 "el default). Si el negocio no tiene Dropi, pasa --dropi no y --flete-max "
                 "se omite.")
    if not a.flete_max:
        a.flete_max = "0"

    campo1, campo2 = construir(a)

    errs = validar_huecos(campo1, "BOTFIELD_1") + validar_huecos(campo2, "BOTFIELD_2")
    if errs:
        print("!" * 62)
        for e in errs:
            print("ERROR: " + e)
        if any("{{PROMPT_MAESTRO}}" in e for e in errs):
            print("       Falta --prompt-maestro: generalo con golden-chatea-pro-prompt-ventas")
            print("       (prompt de negocio) y vuelve a correr. Sin el, el bot recibiria el")
            print("       placeholder literal en vez del prompt.")
        print("       NO se escribio ningun archivo.")
        print("!" * 62)
        sys.exit(1)

    ok, valores = reporte(campo1, campo2)

    # La salida es COMPACTA (ensure_ascii=False, separators): es lo que se guarda
    # y lo que minimiza el conteo contra el techo escapado.
    destino = os.path.dirname(os.path.abspath(a.out_prefix))
    try:
        os.makedirs(destino, exist_ok=True)
    except OSError as e:
        sys.exit(f"ERROR: no se pudo crear el directorio de salida {destino}: {e}")
    for sufijo, nombre in (("_BOTFIELD_1.json", "BOTFIELD_1"), ("_BOTFIELD_2.json", "BOTFIELD_2")):
        ruta = a.out_prefix + sufijo
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(valores[nombre])
        print(f"Guardado (compacto): {ruta}")
    print('\nPegar en Chatea Pro -> Bot Fields -> carpeta del agente de ventas')
    print('  (crear los campos como tipo LONG JSON):')
    print('  _BOTFIELD_1.json -> campo "[Ventas Wp] Configuracion general"')
    print('  _BOTFIELD_2.json -> campo "[Ventas Wp] Configuracion general 2"')
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
