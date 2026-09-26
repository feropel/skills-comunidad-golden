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

    --pais            El pais donde OPERA el negocio. NO es una puerta: si no esta
                      entre los que tienen pack conocido se avisa y se sigue igual
                      (los que hoy tienen pack: colombia, ecuador, chile, mexico,
                      panama, peru, paraguay, guatemala, argentina, brasil).
                      Va en minuscula en el JSON. La lista viva esta en
                      assets/limites.json -> paises_validos.
    --moneda          Moneda (ej: COP). OPCIONAL: si falta se DERIVA del pais
                      contra assets/limites.json y se informa cual se uso.
    --flete-max       El CORTE que dijo el cliente: desde que valor un flete ya es demasiado
                      caro (dato 7 del intake; el corte de "cliente no calificado"). Acepta
                      "25000", "25.000" o "$25 000". Si el cliente no supo responder se OMITE y
                      se usa el promedio nativo del pais (assets/limites.json ->
                      flete_max_por_pais). Un pais sin promedio y sin corte se detiene y lo pide.
                      Sin Dropi (--dropi no) el JSON queda con "0" (el flujo espera la clave).
    --plantilla-notif OPCIONAL. Nombre de la plantilla de Meta aprobada para el aviso.
                      Sin ella el aviso solo sale dentro de la ventana de 24 h.
    --plantilla-ns    Namespace de esa plantilla (del panel de Meta).
    --whatsapp-notif  OPCIONAL. WhatsApp de la empresa, que recibe el aviso de venta (+57 3XX...).
                      Va de ULTIMO en el intake y despues del pago: si el cliente aun no lo tiene,
                      se monta igual, la notificacion queda apagada y se informa; se conecta luego.
    --url-tienda      URL de la tienda (redirige productos no configurados)
    --dropi           si | no (default: si)
    --prompt-maestro  (OBLIGATORIO: el template trae {{PROMPT_MAESTRO}} — sin esta bandera el script falla con exit 1) .txt con el prompt maestro de Producto en Segundos
    --out-prefix      Prefijo de salida; escribe <prefix>_BOTFIELD_1.json y _2.json

Uso:
    python3 build_config.py --pais "colombia" --moneda "COP" \
        --flete-max "25000" --whatsapp-notif "+57 3001234567" \
        --url-tienda "https://mitienda.co" \
        --prompt-maestro /ruta/prompt_maestro.txt \
        --out-prefix /ruta/<negocio>
"""
import argparse
import json
import os
import re
import sys
import unicodedata

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
    if not a.moneda:
        mapa = _lim.get("moneda_por_pais", {})
        a.moneda = mapa.get(a.pais.upper())
        if not a.moneda:
            # No es una puerta de pais: es un DATO que falta. La diferencia importa -- aqui
            # no se rechaza a nadie, se dice exactamente que traer y de donde sale.
            sys.exit(f"Falta la moneda de '{a.pais}'. NO se le pregunta al negocio: se "
                     "INVESTIGA (codigo ISO-4217 del pais) y se pasa con --moneda. "
                     "Cuando lo tengas, anadelo tambien a moneda_por_pais en "
                     "assets/limites.json para que el siguiente no lo repita.")
        print(f"  moneda DERIVADA del pais: {a.moneda} (no se pregunto; "
              "pasa --moneda si el negocio factura en otra)")
    flete["moneda"] = a.moneda
    if a.dropi == "no":
        campo1["acciones_especiales"]["validaciones_orden"]["subida_automatica"] = "no"

    ps = campo1["producto_segundos"]
    ps["prompt_datos"] = leer_prompt("reglas-estructura-producto.txt")
    if a.prompt_maestro:
        try:
            with open(a.prompt_maestro, encoding="utf-8") as f:
                ps["prompt_prompt"] = f.read().strip()
        except OSError as e:
            sys.exit(f"ERROR: no se pudo leer --prompt-maestro '{a.prompt_maestro}': {e}\n"
                     "       Revisa la ruta. Si aun no existe, generalo con "
                     "golden-chatea-pro-prompt-ventas (prompt de negocio).")

    notif = campo1["notificaciones"]["notificacion_1"]
    # 🔵 EL WHATSAPP DE AVISOS ES OPCIONAL (ley de FER, 2026-09-08): "eso es una
    # notificacion, eso es si quiere, no tiene que tenerlo ahi. Pero seria bueno tenerlo."
    # Sin numero NO se inventa uno ni se deja el hueco: se APAGA la notificacion y se DICE.
    # Un aviso activo apuntando a un numero vacio es peor que no tenerlo: se ve configurado
    # y no le llega a nadie.
    if a.whatsapp_notif:
        notif["whatsapp"] = a.whatsapp_notif
    else:
        notif["whatsapp"] = ""
        notif["activa"] = "no"
        print("[opcional] sin --whatsapp-notif: la notificacion de venta queda APAGADA "
              "(activa='no'). El negocio no recibira aviso de las ventas hasta que se "
              "ponga un numero. Conviene tenerlo, no obliga a nada.", file=sys.stderr)

    # 🔴 LA PLANTILLA DE META, Y POR QUE NO BASTA CON EL NUMERO. Medido contra el espacio
    # real de FER el 2026-09-08: su notificacion lleva name y namespace de una plantilla
    # aprobada; la plantilla de esta skill los dejaba VACIOS.
    # WhatsApp solo deja enviar texto libre DENTRO de la ventana de 24 h desde el ultimo
    # mensaje del usuario. Una notificacion de venta casi siempre cae FUERA de esa ventana,
    # y sin plantilla aprobada NO SALE. Queda activa='si', apuntando a un numero correcto,
    # y no llega: se ve configurada y esta muerta. Es el patron ANUNCIADA del auditor.
    # El name y el namespace los da Meta y son de CADA cuenta: no se derivan ni se inventan.
    if a.whatsapp_notif:
        if a.plantilla_notif:
            notif["plantilla"]["name"] = a.plantilla_notif
            notif["plantilla"]["namespace"] = a.plantilla_ns or ""
            notif["plantilla"]["lang"] = "es"
            if not a.plantilla_ns:
                print("[aviso] --plantilla-notif sin --plantilla-ns: el namespace queda vacio. "
                      "Los dos salen del panel de plantillas de Meta.", file=sys.stderr)
        else:
            print("  [nota] notificacion sin plantilla de Meta, por decision de FER "
                  "(2026-09-08): no se usan plantillas. El aviso sale dentro de la "
                  "ventana de 24 h.")
    notif["mensaje"] = leer_prompt("notificacion-venta-realizada.txt")

    comp = campo2["comportamiento_ia"]
    if a.modelo == "dropshipping":
        pago = "contra entrega"
    elif a.modelo == "marca":
        pago = "con pago anticipado"
    else:  # mixto: NUNCA se afirma un modelo unico que seria falso para la mitad
        pago = "contra entrega por defecto; anticipo si el cliente lo pide o el producto lo exige"
    # 🔴 El nicho puede FALTAR: espacio nuevo sin productos cargados, cliente que no
    # lo dio. No se inventa y no se deja un parentesis vacio ("(). Venta...") — se
    # omite la coletilla completa. Si el espacio YA tiene productos, el nicho se
    # LEE de su web (ver Intake, "Nicho") en vez de preguntarse; ese valor se pasa aqui.
    nicho = (a.nicho or "").strip()
    if nicho:
        identidad = (f"Te llamas {a.nombre_bot}, asesora de {a.nombre_tienda} "
                     f"({nicho}). Venta {pago}.")
    else:
        identidad = f"Te llamas {a.nombre_bot}, asesora de {a.nombre_tienda}. Venta {pago}."
    # 🔴 El vocabulario de direccion (departamento/barrio en Colombia, estado/colonia/CP
    # en Mexico) NO se hereda de un pais a otro — ley de FER en references/paises.md. La
    # fuente unica es assets/limites.json -> vocabulario_direccion_por_pais, que a su vez
    # viene del pack autoritativo de golden-chatea-pro-validacion-direcciones. Un pais SIN
    # entrada NO bloquea (el pais se pide para enfocar, no para prohibir): cae a un
    # generico neutro que no asume division administrativa de ningun pais especifico.
    voc = _lim.get("vocabulario_direccion_por_pais", {}).get(a.pais.upper())
    if voc:
        campos_direccion = voc["campos_memoria"]
        aclaracion_direccion = voc["aclaracion"]
        aclaracion_corta = voc.get("aclaracion_corta", "la referencia no es la dirección")
    else:
        print(f"  [DECLARADO] sin vocabulario de direccion para {a.pais.upper()} en "
              "vocabulario_direccion_por_pais. Se usa un generico neutro; confirmar con "
              "el negocio su division administrativa real y anadirla al mapa.")
        campos_direccion = "ciudad, división administrativa, dirección, barrio o colonia"
        aclaracion_direccion = ("La referencia no reemplaza la dirección; confirma la "
                                 "división administrativa que pida el país.")
        aclaracion_corta = "la referencia no es la dirección"
    campo1["producto_segundos"]["prompt_datos"] = campo1["producto_segundos"]["prompt_datos"].replace(
        "{{ACLARACION_CORTA}}", aclaracion_corta)
    comp["rol"] = leer_prompt("rol-general.txt").replace(
        "{{IDENTIDAD}}", identidad).replace("{{CAMPOS_DIRECCION}}", campos_direccion)
    if a.modelo == "dropshipping":
        pago_regla = "No solicitar pago anticipado salvo que el cliente lo pida o lo elija."
    elif a.modelo == "marca":
        pago_regla = "El pago es anticipado: se cobra antes de despachar, nunca contra entrega."
    else:  # mixto: el metodo lo dice el producto, no una regla global
        pago_regla = ("Contra entrega por defecto; el anticipo solo si el cliente lo pide "
                       "o la ficha del producto lo exige.")
    comp["restricciones"] = leer_prompt("restricciones.txt").replace(
        "{{PAGO_REGLA}}", pago_regla).replace("{{ACLARACION_DIRECCION}}", aclaracion_direccion)
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


def emitir_campos_sueltos(pais, modelo, prefijo):
    """Escribe los 16 INTERRUPTORES del flujo, ya resueltos por pais y modelo.

    Dos de los booleanos NO son fijos y se derivan de los 7 datos:
      · 'Oficina' lo decide el PAIS (Mexico no tiene recogida en oficina).
      · 'Solo Con Recaudo' y su espejo 'Solo Sin Recaudo' los decide el MODELO.
    """
    ruta = os.path.join(ASSETS, "campos-sueltos.json")
    with open(ruta, encoding="utf-8") as f:
        cs = json.load(f)

    lineas = ["INTERRUPTORES DEL FLUJO · uno por Bot Field (NO son la configuracion:",
              "la configuracion son los 2 campos JSON)",
              f"pais={pais.upper()} · modelo={modelo}", ""]
    resueltos = {}
    for nombre, d in cs["booleanos"].items():
        if d.get("DERIVADO_DE") == "pais":
            val = "false" if pais.upper() == "MEXICO" else "true"
        elif d.get("DERIVADO_DE") == "modelo":
            # mixto = contra entrega POR DEFECTO con anticipo como excepcion: asi opera Golden en vivo
            # (Con Recaudo=true, Sin Recaudo=false) y vende tambien anticipado. Antes "mixto" caia
            # en la rama de marca propia y emitia los dos interruptores AL REVES, sin avisar.
            con_recaudo = modelo in ("dropshipping", "mixto")
            if "Con Recaudo" in nombre:
                val = "true" if con_recaudo else "false"
            elif "Sin Recaudo" in nombre:
                val = "false" if con_recaudo else "true"
            else:
                val = d.get("valor_por_defecto", "false")
        else:
            val = d["valor"]
        resueltos[nombre] = val
        marca = "  <- DERIVADO" if d.get("DERIVADO_DE") else ""
        lineas.append(f"{nombre}\n  {val}{marca}")

    # Compuerta: los dos de recaudo son ESPEJO. Si coinciden, el filtro no significa nada.
    con = resueltos.get("[Ventas Wp] Solo Con Recaudo")
    sin = resueltos.get("[Ventas Wp] Solo Sin Recaudo")
    if con == sin:
        sys.exit(f"ERROR: 'Solo Con Recaudo' y 'Solo Sin Recaudo' quedaron los dos en "
                 f"'{con}'. Son espejo: uno true y el otro false. NO se escribio nada.")

    lineas.append("")
    for nombre, d in cs["textos"].items():
        lineas.append(f"{nombre}\n{d['valor']}\n")

    # Interruptores REALES bajo [WhatsApp IA] (2 de 10; los otros 7 son estado del bot,
    # ver mas abajo) — mismos defaults declarados en campos-sueltos.json
    wia = cs.get("interruptores_operativos_whatsapp_ia", {})
    n_wia = 0
    for nombre, d in wia.items():
        if nombre.startswith("_"):
            continue
        lineas.append(f"{nombre}\n  {d['valor_por_defecto']}")
        n_wia += 1

    # Aviso explicito de lo que NUNCA se toca, para que quien pega los campos no
    # confunda un contador de ventas real con algo a configurar
    ntocar = cs.get("estado_del_bot_NO_TOCAR", {}).get("campos", [])
    if ntocar:
        lineas.append("")
        lineas.append("NO TOCAR (estado que escribe el bot, NO se pega ni se edita):")
        for nombre in ntocar:
            lineas.append(f"  {nombre}")

    pend = cs.get("_pendiente_declarado")
    if pend:
        lineas.append("")
        lineas.append(f"PENDIENTE (sin dato para decidir, no se inventa): {pend}")

    destino = f"{prefijo}_CAMPOS_SUELTOS.txt"
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"  {os.path.basename(destino)} -> {len(cs['booleanos'])} booleanos + "
          f"{len(cs['textos'])} textos + {n_wia} interruptores WhatsApp IA "
          f"(Oficina={resueltos['[Ventas Wp] Oficina 📦']} · Con Recaudo={con})")
    return destino


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pais", required=True)
    p.add_argument("--moneda")  # si falta, se DERIVA del pais (ver limites.json)
    p.add_argument("--flete-max", dest="flete_max")
    p.add_argument("--whatsapp-notif", dest="whatsapp_notif")   # OPCIONAL (FER 08-sep)
    p.add_argument("--plantilla-notif", dest="plantilla_notif")  # nombre de la plantilla de Meta
    p.add_argument("--plantilla-ns", dest="plantilla_ns")        # namespace de esa plantilla
    p.add_argument("--url-tienda", dest="url_tienda", required=True)
    p.add_argument("--nombre-bot", required=True,
                   help="Como se llama la asesora (va en el rol)")
    p.add_argument("--nombre-tienda", required=True,
                   help="Nombre de la tienda (va en el rol)")
    p.add_argument("--modelo", choices=["dropshipping", "marca", "mixto"], required=True,
                   help="dropshipping/catalogo = contra entrega · marca = anticipado")
    p.add_argument("--nicho", default="",
                   help="Nicho (va en el rol). OPCIONAL y NO se le pregunta al cliente: se LEE de "
                        "su web; si la web es de catalogo variado o no muestra una especialidad "
                        "clara, se omite.")
    p.add_argument("--dropi", choices=["si", "no"], default="si")
    p.add_argument("--prompt-maestro", dest="prompt_maestro")
    p.add_argument("--out-prefix", dest="out_prefix", required=True)
    a = p.parse_args()
    # Clave de pais: sin acentos, mayusculas, guion=espacio (costa-rica, España, ESPANA).
    # Los packs viven en <pais>.md sin acentos; el mapa de vocabulario usa la misma clave.
    a.pais = "".join(c for c in unicodedata.normalize("NFD", (a.pais or "").strip().replace("-", " "))
                      if unicodedata.category(c) != "Mn").upper()

    # 🔴 EL PAIS ES PARAMETRO, NO PUERTA (mandato de FER, 2026-09-06).
    # Hasta hoy estas tres lineas eran un sys.exit: 'el salvador' y 'bolivia' se rechazaban
    # POR ESCRITO, con exit != 0 y sin generar nada. Palabras de FER: "hoy son diez, manana
    # doce, pasado treinta; el pais se pide para saber COMO enfocarlo, no para prohibir".
    # Una lista de paises dentro de una skill es un dato que CADUCA SOLO -- y esta ya caduco
    # una vez (decia 7 cuando eran 10, y rechazo Guatemala, Argentina y Brasil por escrito).
    # La cura no es vigilar la cifra: es retirar la puerta, que se lleva la clase entera.
    if a.pais.upper() not in PAISES:
        print(f"  ⚠️ '{a.pais}' no esta entre los {len(PAISES)} paises con pack conocido en "
              "assets/limites.json.", file=sys.stderr)
        print("     ESO NO LO PROHIBE: la arquitectura de la config es la misma en todos, "
              "lo que cambia son los datos.", file=sys.stderr)
        print("     Lo del pais se INVESTIGA (jerga, transportadoras, forma de la direccion, "
              "moneda), no se le pregunta al negocio.", file=sys.stderr)
        print("     Al cerrar, entrega el pack investigado con sus fuentes para que el "
              "siguiente negocio de ese pais no repita el trabajo.", file=sys.stderr)

    # 🔴 FLETE (estandar de FER 2026-09-19, dato 7 del intake). El promedio del pais es el valor
    # NATIVO y el corte que dice el cliente ("desde que valor un flete ya es demasiado caro", el
    # corte de "cliente no calificado") manda ENCIMA. Quien no sabe responder se queda con el
    # promedio del pais. Lo que NO se hace: derivar el flete del ticket ignorando el promedio del
    # pais, ni copiar el de otro pais. Mapa: assets/limites.json -> flete_max_por_pais.
    import re as _re
    _mapa_flete = _lim.get("flete_max_por_pais", {})
    _pais_norm = (a.pais or "").strip().upper()
    _nativo = _mapa_flete.get(_pais_norm)
    if a.flete_max:
        _dig = _re.sub(r"[^\d]", "", str(a.flete_max))
        if not _dig or int(_dig) <= 0:
            sys.exit(f"ERROR: --flete-max '{a.flete_max}' no es un valor valido: se espera un "
                     "numero positivo (ej. 25000). NO se escribio ningun archivo.")
        a.flete_max = _dig
        if _nativo and int(_dig) != int(_nativo):
            print(f"[flete] corte del cliente: {_dig} · promedio nativo de {_pais_norm}: {_nativo}. "
                  "Manda el corte del cliente.", file=sys.stderr)
    elif a.dropi == "si":
        if _nativo:
            a.flete_max = str(_nativo)
            print(f"[derivado] flete de {_pais_norm}: {a.flete_max} (promedio nativo del pais; "
                  "el cliente no dio un corte).", file=sys.stderr)
        else:
            sys.exit(f"Falta --flete-max y el pais '{_pais_norm or '(sin pais)'}' no tiene promedio "
                     f"nativo en flete_max_por_pais de assets/limites.json (hoy solo: "
                     f"{', '.join(_mapa_flete) or 'ninguno'}). Si el cliente dio su corte (dato 7), "
                     "pasalo con --flete-max. Si no lo dio, el promedio de ese pais lo calcula el "
                     "Centro de Mando: pidelo y anadelo al mapa. NO se copia el de otro pais.")
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

    # COMPUERTA DE TOPES (gemela de la compuerta de huecos de v4.1.3): si un tope DURO
    # se excede, NO se escribe archivo. Antes se escribian los 2 BOTFIELD igual y solo
    # se salia con exit 1 — quedaba en disco un archivo con pinta de pegable que, si
    # alguien lo pegaba, se guardaba CORTADO y mataba al bot en silencio: exactamente
    # el fallo que esta skill existe para evitar.
    if not ok:
        print("!" * 62)
        print("ERROR: un tope DURO se excede (ver arriba). NO se escribio ningun archivo.")
        print("       Acorta el prompt maestro o lo variable del intake y vuelve a correr.")
        print("       Los prompts fijos de assets/prompts/ NO se recortan.")
        print("!" * 62)
        sys.exit(1)

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
    # 🔴 EL NOMBRE DEL CAMPO TAMBIEN TIENE TOPE: 50. Medido en el panel el 2026-09-08
    # (capturas de FER: 33/50 y 35/50). Es un tercer techo que no estaba contado, y el que
    # peor duele: el flujo lee las claves POR NOMBRE, asi que un nombre cortado deja al bot
    # sin encontrar su propio campo. Se comprueba aqui porque estos dos nombres son fijos y
    # de la casa; si alguien los cambia, el fallo salta antes de llegar al panel.
    TOPE_NOMBRE = NATIVO.get("nombre_campo", 50)
    NOMBRES = {"_BOTFIELD_1.json": "[Ventas Wp] Configuracion general",
               "_BOTFIELD_2.json": "[Ventas Wp] Configuracion general 2"}
    for _suf, _nom in NOMBRES.items():
        if len(_nom) > TOPE_NOMBRE:
            sys.exit(f"El nombre del campo '{_nom}' mide {len(_nom)} y el tope del panel es "
                     f"{TOPE_NOMBRE}. El flujo lee las claves POR NOMBRE: si se corta, el bot "
                     f"no encuentra su campo.")
    print('\nPegar en Chatea Pro -> Bot Fields -> carpeta del agente de ventas')
    print('  (crear los campos como tipo LONG JSON):')
    for _suf, _nom in NOMBRES.items():
        print(f'  {_suf} -> campo "{_nom}"  [{len(_nom)}/{TOPE_NOMBRE}]')
    emitir_campos_sueltos(a.pais, a.modelo, a.out_prefix)
    sys.exit(0)


if __name__ == "__main__":
    main()
