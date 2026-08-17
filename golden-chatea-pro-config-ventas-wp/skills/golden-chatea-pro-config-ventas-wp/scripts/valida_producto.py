#!/usr/bin/env python3
"""
valida_producto.py — QA del Bot Field de producto ([Producto Ventas Wp] N)
del asistente de ventas WhatsApp de Chatea Pro, ANTES de pegarlo.

Recibe el JSON del producto ya lleno (copiado de
assets/template-botfield-producto.json, esquema nativo verificado 2026-07-09)
y verifica los DOS techos contra assets/limites.json:

    - que no queden {{PLACEHOLDERS}} sin llenar
    - TECHO A (bot field): total ESCAPADO = len(json.dumps(valor)[1:-1]) sobre el
      valor compacto. ≤19000 cabe en cualquier campo; >19000 avisa (solo LONG JSON);
      ≥500000 falla. NUNCA se mide en crudo.
    - TECHO B (topes nativos del formulario): nombre ≤100 · precio/id_dropi dígitos ·
      mensaje_inicial y pregunta_de_entrada ≤1000 · prompt_libre ≤12000 (avisa, no
      rechaza: por Bot Field puede ser mayor) · recordatorios ≤800 · remarketing ≤1000 ·
      upsells (si activos) título/desc/botón
    - el trigger (palabras_clave) SIN caracteres de 4 bytes (emoji): corrompen el bot
    - que el precio aparezca dentro del prompt_libre (la IA lo cita de ahí)
    - palabras_clave/ids_de_anuncio con formato de 7 slots por comas
    - sin ¿ ¡ en textos que ve el cliente (estándar Golden)

Con --registro además valida la entrada del Disparador de productos Extendido.

Uso:
    python3 valida_producto.py --in /ruta/<producto>_BOTFIELD.json \
        [--registro /ruta/<producto>_REGISTRO.json]

Escribe junto al archivo validado una copia *_LIMPIO.json sin claves _meta,
lista para pegar. Exit 0 si todo pasa, exit 1 si algo falla. Si un texto
excede, NO recortes a ciegas: regenera esa pieza con
golden-chatea-pro-prompt-ventas pidiendo la versión más corta.
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIMITES_PATH = os.path.join(SCRIPT_DIR, "..", "assets", "limites.json")

errores = []
avisos = []


def sin_meta(nodo):
    if isinstance(nodo, dict):
        return {k: sin_meta(v) for k, v in nodo.items() if not k.startswith("_")}
    if isinstance(nodo, list):
        return [sin_meta(x) for x in nodo]
    return nodo


def u16(texto):
    """Longitud en unidades UTF-16, como cuenta el formulario del panel (JS .length):
    cada emoji astral vale 2. Los topes nativos (Techo B) se miden así."""
    return len((texto or "").encode("utf-16-le")) // 2


def check_len(nombre, texto, limite):
    n = u16(texto)
    estado = "OK" if n <= limite else f"EXCEDE por {n - limite}"
    print(f"  {nombre}: {n} / {limite}  {estado}")
    if n > limite:
        errores.append(f"{nombre} excede el límite ({n} > {limite})")


def check_digitos(nombre, valor, max_digitos):
    v = str(valor or "")
    if not v.isdigit():
        errores.append(f"{nombre} debe ser solo números (recibido: '{v}')")
    elif len(v) > max_digitos:
        errores.append(f"{nombre} supera {max_digitos} dígitos ({len(v)})")
    else:
        print(f"  {nombre}: {v}  OK")


def check_slots(nombre, valor):
    if (valor or "").count(",") != 6:
        avisos.append(f"{nombre} no tiene el formato de 7 slots por comas (visto: '{valor}')")


def check_apertura(nombre, texto):
    if texto and ("¿" in texto or "¡" in texto):
        errores.append(f"{nombre} contiene ¿ o ¡ (estándar Golden: solo signo de cierre)")


def escapado(valor_str):
    """Caracteres ESCAPADOS del valor, como los cuenta el flujo (tilde 6, emoji 12)."""
    return len(json.dumps(valor_str)[1:-1])


def check_cuatro_bytes(nombre, texto):
    """El trigger (palabra clave) NO admite caracteres de 4 bytes (emoji fuera del
    BMP): corrompen el activador y el bot NO arranca. Se marca como error."""
    malos = [c for c in (texto or "") if ord(c) >= 0x10000]
    if malos:
        errores.append(
            f"{nombre} tiene {len(malos)} caracter(es) de 4 bytes (emoji: {' '.join(malos)}) — "
            "el trigger no los admite y el bot no arranca. Quítalos de la palabra clave."
        )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="entrada", required=True, help="JSON del Bot Field de producto lleno")
    p.add_argument("--registro", help="(opcional) JSON con la entrada del Disparador Extendido")
    a = p.parse_args()

    with open(LIMITES_PATH, encoding="utf-8") as f:
        _lim = json.load(f)
    lim = _lim["capa_nativa"]
    BOT = _lim["bot_field"]

    with open(a.entrada, encoding="utf-8") as f:
        prod = sin_meta(json.load(f))

    # Regex reparado (verificador 2026-08-08): [A-Z0-9_]+ dejaba pasar {{Hueco}},
    # {{hueco}}, {{ X }}, {{X-2}}, {{X 3}} y slots simples sin llenar {URL_TIENDA}.
    # Dobles: cualquier contenido. Simples: whitelist de las runtime de Chatea
    # (las de notificacion-venta-realizada.txt); todo lo demas es un slot colado.
    RUNTIME_LEGITIMAS = {"nombre_cliente", "nombre_producto", "porcentaje_entrega",
                         "telefono_cliente", "valor_venta"}
    texto_prod = json.dumps(prod, ensure_ascii=False)
    pendientes = sorted(set(re.findall(r"\{\{[^{}]*\}\}", texto_prod)))
    if pendientes:
        errores.append(f"Placeholders sin llenar: {', '.join(pendientes)}")
    simples = sorted({m for m in re.findall(
        r"(?<!\{)\{([A-Za-z0-9_][A-Za-z0-9_ .\-]*)\}(?!\})", texto_prod)
        if m not in RUNTIME_LEGITIMAS})
    if simples:
        errores.append(
            "Llave simple sin llenar o desconocida: " + ", ".join("{%s}" % s for s in simples)
            + " (runtime legitimas: " + ", ".join("{%s}" % s for s in sorted(RUNTIME_LEGITIMAS)) + ")")

    info = prod.get("informacion_de_producto", {})
    emb = prod.get("embudo_de_ventas", {})
    prompt = prod.get("prompt", {})
    rec = prod.get("recordatorios", {})
    rem = prod.get("remarketing", {})
    act = prod.get("activadores_del_flujo", {})
    ups = prod.get("upsells", {})

    meta = prod.get("meta_conversion", {})

    print("Límites por campo (Techo B, medidos en UTF-16 como el panel):")
    check_len("nombre", info.get("nombre"), lim["nombre"])
    check_digitos("precio", info.get("precio"), lim["precio_digitos"])
    check_digitos("id_dropi", info.get("id_dropi"), lim["id_dropi_digitos"])
    # descripción del producto = informacion_de_producto.dta_prompt (tope nativo 500);
    # si se pasa, el panel la corta al guardar (Techo B) y nadie más lo atrapa.
    if (info.get("dta_prompt") or ""):
        check_len("dta_prompt (descripción)", info.get("dta_prompt"), lim["descripcion_producto"])
    # pixel: meta_conversion.id / aud_id (tope nativo pixel_ids)
    for campo_px in ("id", "aud_id"):
        if (meta.get(campo_px) or ""):
            check_len(f"meta_conversion.{campo_px}", meta.get(campo_px), lim["pixel_ids"])
    check_len("mensaje_inicial", emb.get("mensaje_inicial"), lim["mensaje_inicial"])
    check_len("pregunta_de_entrada", emb.get("pregunta_de_entrada"), lim["pregunta_entrada"])
    # prompt_libre: el tope 12000 es de la PANTALLA de la UI, no del Bot Field. Por Bot Field
    # puede ser mayor (no se rechaza), pero se avisa: ese producto se edita SOLO por Bot Field.
    pl = prompt.get("prompt_libre") or ""
    print(f"  prompt_libre: {len(pl)} (UI corta en {lim['prompt_personalizado']})")
    if len(pl) > lim["prompt_personalizado"]:
        avisos.append(
            f"prompt_libre tiene {len(pl)} > {lim['prompt_personalizado']}: edítalo SOLO por Bot Field. "
            "La pantalla 'Prompt del producto' de la UI lo corta y su 'Guardar asistente' lo sobrescribe cortado."
        )
    for i in (1, 2):
        check_len(f"recordatorio mensaje_{i}", rec.get(f"mensaje_{i}"), lim["recordatorio"])
        check_len(f"remarketing prompt_{i}", rem.get(f"prompt_{i}"), lim["instruccion_remarketing"])

    # Upsells: si una tarjeta está activa, valida sus límites de la UI
    for n in ("1", "2"):
        u = ups.get(n, {}) if isinstance(ups, dict) else {}
        if str(u.get("activo", "no")).lower() == "si":
            check_len(f"upsell {n} titulo", u.get("titulo"), lim["upsell_titulo"])
            check_len(f"upsell {n} descripcion", u.get("descripcion"), lim["upsell_descripcion"])
            check_len(f"upsell {n} boton", u.get("boton"), lim["upsell_boton"])
            if not str(u.get("id_dropi") or "").isdigit():
                errores.append(f"upsell {n}: id_dropi debe ser numérico si la tarjeta está activa")

    # TECHO A — bot field medido ESCAPADO (tilde 6, emoji 12), sobre el valor COMPACTO
    compacto = json.dumps(prod, ensure_ascii=False, separators=(",", ":"))
    esc = escapado(compacto)
    if esc <= BOT["seguro_escapado"]:
        print(f"\nTECHO A (escapado): {esc} / {len(compacto)} crudos — OK (cabe en cualquier tipo de campo)")
    elif esc < BOT["longtext_escapado"]:
        print(f"\nTECHO A (escapado): {esc} / {len(compacto)} crudos")
        avisos.append(
            f"El bot field escapado tiene {esc} > {BOT['seguro_escapado']}: SOLO cabe si el campo es LONG JSON. "
            f"Si es JSON legacy se corta a {BOT['legacy_json_escapado']} escapados y el bot muere en silencio."
        )
    else:
        print(f"\nTECHO A (escapado): {esc} / {len(compacto)} crudos")
        errores.append(f"El bot field escapado ({esc}) supera el máximo de LONG JSON ({BOT['longtext_escapado']})")

    precio = str(info.get("precio") or "")
    if precio and precio not in (prompt.get("prompt_libre") or ""):
        avisos.append("El precio no aparece dentro del prompt_libre — la IA no lo va a citar bien")

    check_slots("palabras_clave", act.get("palabras_clave"))
    check_slots("ids_de_anuncio", act.get("ids_de_anuncio"))
    # El trigger (palabra clave) no admite emojis de 4 bytes: corrompen el activador
    check_cuatro_bytes("palabras_clave", act.get("palabras_clave"))

    for nombre, texto in [
        ("mensaje_inicial", emb.get("mensaje_inicial")),
        ("pregunta_de_entrada", emb.get("pregunta_de_entrada")),
        ("prompt_libre", prompt.get("prompt_libre")),
        ("recordatorio mensaje_1", rec.get("mensaje_1")),
        ("recordatorio mensaje_2", rec.get("mensaje_2")),
    ]:
        check_apertura(nombre, texto)

    if a.registro:
        with open(a.registro, encoding="utf-8") as f:
            reg = sin_meta(json.load(f))
        reg = reg.get("entrada_nueva", reg)
        print("\nEntrada del Disparador Extendido:")
        for clave in ("producto", "name", "keyW", "idAd", "estado"):
            if not reg.get(clave) and clave != "idAd":
                errores.append(f"registro: falta '{clave}'")
        if reg.get("producto") and reg.get("producto") != info.get("nombre"):
            avisos.append("registro.producto no coincide con informacion_de_producto.nombre")
        kw_prod = (act.get("palabras_clave") or "").strip(",")
        kw_reg = (reg.get("keyW") or "").strip(",")
        if kw_prod and kw_reg and kw_prod != kw_reg:
            errores.append("La palabra clave del registro NO coincide con la del producto")
        check_slots("registro.keyW", reg.get("keyW"))
        check_cuatro_bytes("registro.keyW", reg.get("keyW"))
        print(f"  producto={reg.get('producto')} · name={reg.get('name')} · estado={reg.get('estado')}")

    if avisos:
        print("\n⚠️  Avisos (no bloquean):")
        for m in avisos:
            print(f"   - {m}")
    if errores:
        print("\n❌ NO está listo para pegar:")
        for m in errores:
            print(f"   - {m}")
        sys.exit(1)

    limpio = a.entrada.replace(".json", "_LIMPIO.json")
    with open(limpio, "w", encoding="utf-8") as f:
        f.write(json.dumps(prod, ensure_ascii=False, indent=2))
    print(f"\n✅ Válido. Copia lista para pegar (sin _meta): {limpio}")
    sys.exit(0)


if __name__ == "__main__":
    main()
