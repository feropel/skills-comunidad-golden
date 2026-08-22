#!/usr/bin/env python3
"""Compara lo que el cliente pidió en el chat contra lo que se cargó en Dropi.

Si pidió rojo y amarillo y entró amarillo y amarillo, la orden se frena y se corrige
ANTES de despachar. Este módulo no imprime veredictos: devuelve una lista. Quien la
use decide qué decir, y lo dice a partir de la lista, nunca de una frase escrita a mano.

Uso como módulo:
    from cruzar_chat_orden import cruzar
    disc = cruzar(ordenes, contactos)      # lista de discrepancias, [] si no hay

Uso desde consola:
    python3 cruzar_chat_orden.py dropi.json chatea.json
"""
import json, os, re, sys, unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import tel10          # noqa: E402
from escritura import leer_json  # noqa: E402

# Los colores del catálogo. Se amplía por tienda; no hay nada específico de una marca
# en la lógica, solo en esta tabla.
# DE DONDE SALE EL COLOR EN DROPI (verificado en vivo, 3.094 ordenes, 2026-08-10):
#   `variation.values` -> VACIO en el 100% de las lineas. No sirve.
#   `variation_id`     -> NO decodifica: el mismo id 829674 aparece con diez colores
#                         distintos al intentar mapearlo. No sirve.
#   `notes`            -> SI: una linea por producto, "Bolso ...: Negro Azabache *** ".
# Leerlo de `variation.values` hacia que el cruce marcara 62 discrepancias de 63,
# porque "el chat pidio color y Dropi no tiene ninguno" se cumplia SIEMPRE.
COLORES = {
    "negro": ["negro", "azabache"],
    "rojo": ["rojo", "carmesi"],
    "palo de rosa": ["palo de rosa", "palo rosa", "rosa claro", "rosa"],
    "rosa oscuro": ["rosa oscuro", "fucsia"],
    "cafe": ["cafe", "caramelo", "marron"],
    "gris": ["gris"],
    "verde": ["verde"],
    "azul": ["azul"],
    "blanco": ["blanco"], "dorado": ["dorado"], "plateado": ["plateado"],
    "beige": ["beige"], "vinotinto": ["vinotinto", "vino tinto"],
}
# Lo que aparece en la línea del chat pero NO es una unidad de producto
# LO QUE EL FORMULARIO GUARDA EN «Productos escogidos» Y NO ES UN PRODUCTO.
#
# EL CASO, medido en la corrida de LOGISTICA GOLDEN del 2026-08-11 sobre 132 pedidos
# accionables: Chatea guarda las OPCIONES del formulario en el mismo campo que los
# productos. «y 1 Si eliges Pago Contra Entrega +» entraba como una linea mas, el
# contador sumaba 1+1=2 y salian **42 discrepancias de cantidad FALSAS sobre pedidos
# correctos**. Tres se verificaron a mano contra el valor de compra: los pedidos
# estaban bien; lo que estaba mal era el contador.
#
# Y AQUI NO SE AMPLIA LA LISTA QUEMADA, aunque seria lo rapido. Una lista literal
# dentro de un validador es la clase que esta misma skill legislo: refleja los
# formularios que su autor conocia el dia que la escribio. Golden tiene opciones que
# Dolce no tiene, y la tienda que entre mañana tendra otras. **Un formulario nuevo no
# puede exigir tocar el codigo.**
#
# Por eso: hay una BASE COMUN (lo que se ha visto en todas las tiendas) y cada tienda
# suma las suyas por CONFIG, con `opciones_no_producto`. Si el config no las declara,
# se usa solo la base y **el cruce lo dice en su salida** — no se calla que esta
# mirando con la lista corta.
BASE_NO_ES_PRODUCTO = [r"env[ií]o", r"domicilio", r"flete", r"prioritario"]
NO_ES_PRODUCTO = re.compile("|".join(BASE_NO_ES_PRODUCTO), re.I)


def fijar_opciones_no_producto(extra):
    """Suma las opciones de ESTA tienda a la base. Devuelve (base, extra, medido).

    TRES ESTADOS, NO DOS — y es la ley del cero honesto aplicada a una bandera:
      · `None` (la clave NO esta en el config) -> **nadie miro el formulario**. El
        cruce avisa: si esa tienda guarda opciones ahi, van a salir discrepancias
        falsas y nadie lo sabra.
      · `[]` (declarada vacia)                 -> **se miro, se midio, no hay ninguna**.
        El aviso calla, y en su lugar queda la constancia de que se midio: un silencio
        que no dice por que es indistinguible de un descuido.
      · lista con opciones                     -> se filtran.
    Tratar `None` y `[]` igual condena a las tiendas limpias a llevar para siempre un
    aviso que en su caso es FALSO. **Un aviso cierto que grita donde no aplica es el que
    se ignora a los dos dias** — y ahi muere la compuerta, no el dia que se rompe.
    """
    global NO_ES_PRODUCTO
    medido = extra is not None
    extra = [x for x in (extra or []) if str(x).strip()]
    NO_ES_PRODUCTO = re.compile("|".join(BASE_NO_ES_PRODUCTO + [re.escape(str(x)) for x in extra]),
                                re.I)
    return (len(BASE_NO_ES_PRODUCTO), len(extra), medido)


def norm(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def color_de(texto):
    """UN color por trozo. Gana el alias mas largo: 'rosa claro' le gana a 'rosa'."""
    t = norm(texto)
    mejor, largo = None, 0
    for canon, alias in COLORES.items():
        for a in alias:
            na = norm(a)
            if na in t and len(na) > largo:
                mejor, largo = canon, len(na)
    return mejor


def colores_notas(notes):
    """Multiconjunto de colores segun Dropi. Una entrada por producto."""
    out = Counter()
    for trozo in (notes or "").split("***"):
        trozo = trozo.strip()
        if not trozo or ":" not in trozo:
            continue
        c = color_de(trozo.split(":")[-1])
        if c:
            out[c] += 1
    return out


def colores_chat(escogidos):
    """Multiconjunto segun el chat, respetando el numero que encabeza cada item."""
    out = Counter()
    texto = re.sub(r"\([^)]*\)", "", escogidos or "")
    for parte in re.split(r"\s+y\s+|,\s*", texto):
        if not parte.strip() or NO_ES_PRODUCTO.search(parte):
            continue
        m = re.match(r"\s*(\d+)\b", parte)
        n = int(m.group(1)) if m else 1
        c = color_de(parte)
        if c:
            out[c] += n
    return out


def cantidad_chat(escogidos):
    """Suma el número que encabeza cada ítem. El paréntesis explica, no suma.
    Probado contra casos conocidos en autoprueba()."""
    if not escogidos:
        return None
    texto = re.sub(r"\([^)]*\)", "", escogidos)
    total, vistos = 0, 0
    for parte in re.split(r"\s+y\s+|,\s*", texto):
        if NO_ES_PRODUCTO.search(parte):
            continue
        m = re.match(r"\s*(\d+)\b", parte)
        if m:
            total += int(m.group(1))
            vistos += 1
    return total if vistos else None


def uf(contacto, nombre):
    for x in contacto.get("user_fields", []):
        if x["name"] == nombre:
            return (x.get("value") or "").strip()
    return ""


_PROBADO = None


def _exigir_autoprueba():
    """F1: la guardia tiene que correr EN EL CAMINO QUE PRODUCE EL ENTREGABLE.

    Antes vivía solo bajo __main__: generar_informe importaba `cruzar` y nunca la
    llamaba, asi que un extractor roto pasaba y el informe decia "no hay
    discrepancias" sobre una orden que SI las tenia. Ahora cualquiera que llame a
    cruzar() paga el peaje, venga de la consola o de un import.
    """
    global _PROBADO
    if _PROBADO is None:
        _PROBADO = autoprueba(silencio=True)
    if not _PROBADO:
        raise RuntimeError(
            "El extractor de cantidad no pasa su propia autoprueba. "
            "No se cruza nada: un cruce con el extractor roto miente en silencio.")


def _describir(lineas, notas):
    """Lo que quedo cargado en Dropi, en texto, sin reventar por un None."""
    if notas and notas.strip():
        return notas.strip()[:160]
    if not lineas:
        return "(la orden no trae lineas de producto)"
    trozos = []
    for l in lineas:
        c = l.get("cantidad")
        cant = f"{c:.0f} x " if isinstance(c, (int, float)) else ""
        # B1: `valores` puede traer None DENTRO de la lista, y join revienta.
        # Y `producto` puede ser None explicito, que .get(k,'') no atrapa.
        vals = [str(v) for v in (l.get("valores") or []) if v]
        col = "/".join(vals) or "color no registrado"
        prod = l.get("producto") or "producto sin nombre"
        trozos.append(f"{cant}{prod} {col}".strip())
    return "; ".join(trozos)


def cruzar(ordenes, contactos, estados_modificables=None, opciones_no_producto=None):
    """Devuelve un dict con las discrepancias Y la cobertura real.

    Nunca devuelve solo la lista: quien la reciba tiene que poder distinguir
    "no hay discrepancias" de "no se pudo comparar nada".
    """
    _exigir_autoprueba()
    n_base, n_extra, medido = fijar_opciones_no_producto(opciones_no_producto)
    if estados_modificables is None:
        estados_modificables = ["PENDIENTE", "PENDIENTE CONFIRMACION",
                               "PREPARADO PARA TRANSPORTADORA"]
    # el teléfono manda sobre el id: Dropi cambia el id al editar una orden
    por_tel = {}
    for c in contactos:
        t = tel10(c.get("phone"))
        if t:
            por_tel.setdefault(t, []).append(c)

    disc, banderas, comparadas, saltadas = [], [], 0, []
    modificables = comp_cant = comp_col = sin_cant = sin_col = contradictorios = 0
    for o in ordenes:
        if o.get("status") not in estados_modificables:
            continue
        modificables += 1
        tel = tel10(o.get("phone"))
        cs = por_tel.get(tel, [])
        if not cs:
            saltadas.append({"orden": o.get("id"), "razon": "no hay contacto de Chatea con ese telefono"})
            continue
        # el contacto con datos de pedido, si hay varios con el mismo teléfono
        c = max(cs, key=lambda x: len(uf(x, "Productos escogidos")))
        escogidos = uf(c, "Productos escogidos")
        if not escogidos:
            saltadas.append({"orden": o.get("id"), "razon": "el contacto no tiene 'Productos escogidos'"})
            continue

        lineas = o.get("lineas") or []
        fallos = []

        # --- cantidad ---
        # B3: Chatea guarda TRES señales de cantidad y a veces se contradicen entre si.
        # Caso real ({CLIENTA_B}, orden {PEDIDO_EJEMPLO_2}): el campo decia 2, el texto decia 1 y el
        # valor de la compra era el de una unidad. La conversacion — el unico arbitro —
        # decia "amor son dos, el negro y como el marroncito": el campo tenia razon y
        # las otras dos señales mentian. Pero eso NO se puede saber desde los campos.
        # Por eso, cuando las señales del chat no coinciden entre si, esto NO dictamina:
        # levanta la bandera para que un humano lea la conversacion.
        cant_dropi = o.get("cantidad_dropi")
        if cant_dropi is None:
            cs = [l.get("cantidad") for l in lineas]
            cant_dropi = sum(c for c in cs if c is not None) if any(c is not None for c in cs) else None
        cant_campo = None
        crudo = uf(c, "Cantidad de productos")
        if str(crudo).strip():
            try:
                cant_campo = int(float(str(crudo).strip()))
            except ValueError:
                cant_campo = None
        cant_chat = cant_campo if cant_campo is not None else cantidad_chat(escogidos)
        cant_texto = cantidad_chat(escogidos)
        contradice = (cant_campo is not None and cant_texto is not None
                      and cant_campo != cant_texto)
        if contradice:
            # B3 completo: una bandera NO es una discrepancia. Si entra en `disc` y en
            # `comparadas`, el informe dice "2 no coinciden" un dia con CERO
            # discrepancias reales, y se contradice a si mismo: "no llevan veredicto"
            # arriba y "hay que frenarlos y corregirlos" dos lineas despues.
            # Va a su propia lista, con su propio conteo, y NO cuenta como comparada.
            contradictorios += 1
            banderas.append({
                "orden": o.get("id"), "status": o.get("status"), "tel": "57" + tel,
                "cliente": f"{o.get('name','')} {o.get('surname','')}".strip(),
                "ciudad": o.get("city"), "total": o.get("total") or 0,
                "chat": escogidos, "dropi": _describir(lineas, o.get("notes")),
                "campo": cant_campo, "texto": cant_texto, "en_dropi": cant_dropi,
                "que_hacer": "no se decide desde los campos: hay que leer la conversacion"})
            # Un pedido con los campos peleados NO esta comparado: esta en cuarentena.
            continue
        comparadas += 1
        if cant_chat is not None and cant_dropi is not None:
            comp_cant += 1
            if abs(cant_chat - cant_dropi) > 0.01:
                fallos.append({"tipo": "CANTIDAD", "chat": cant_chat, "dropi": cant_dropi})
        else:
            sin_cant += 1

        # --- color: de las NOTAS, que es donde vive ---
        notas = (o.get("notes") or "").strip()
        cd, cc = colores_notas(notas), colores_chat(escogidos)
        if cd and cc:
            comp_col += 1
            if cd != cc:
                fallos.append({"tipo": "COLOR", "chat": sorted(cc.elements()),
                               "dropi": sorted(cd.elements())})
        else:
            sin_col += 1

        if fallos:
            disc.append({
                "orden": o.get("id"), "status": o.get("status"),
                "tel": "57" + tel, "cliente": f"{o.get('name','')} {o.get('surname','')}".strip(),
                "ciudad": o.get("city"), "total": float(o.get("total") or 0),
                "chat": escogidos,
                # B1: `cantidad` puede ser None (el listado de Dropi no la trae) y un
                # f-string con :.0f revienta. El informe moria justo el dia que tenia
                # algo que decir. Se formatea con guardia y se dice "cantidad desconocida".
                "dropi": _describir(lineas, o.get("notes")),
                "fallos": fallos,
            })
    # F2: `comparadas` cuenta lo REALMENTE comparado, no lo que era candidato.
    # Antes se devolvia el numero de modificables y el informe decia "se compararon 5"
    # habiendo comparado una, o cero.
    return {"modificables": modificables, "comparadas": comparadas,
            # De donde salio la lista de "esto no es un producto". Con cero opciones
            # propias, el cruce esta mirando con la lista corta y hay que saberlo:
            # las discrepancias falsas de Golden salieron exactamente de ahi.
            "opciones_no_producto_base": n_base,
            "opciones_no_producto_de_la_tienda": n_extra,
            "opciones_no_producto_medidas": medido,
            "_estado_opciones": (
                f"{n_extra} opciones propias declaradas, ademas de las {n_base} comunes"
                if n_extra else
                "medidas, ninguna: el formulario de esta tienda no guarda opciones en "
                "«Productos escogidos»" if medido else
                "SIN MEDIR: el config no declara `opciones_no_producto`"),
            "_aviso_opciones": ("el config no declara `opciones_no_producto`: se cruza solo "
                                "con la lista comun. Si el formulario de esta tienda guarda "
                                "opciones en «Productos escogidos», van a contarse como "
                                "productos y saldran discrepancias de cantidad FALSAS")
            if not medido else "",
            "comparadas_cantidad": comp_cant, "comparadas_color": comp_col,
            "sin_dato_cantidad": sin_cant, "sin_dato_color": sin_col,
            # EL CONTEO Y LA LISTA, CON LA MISMA CONVENCION `n_X` / `X`.
            # Salia `campos_contradictorios` (un int) y `banderas` (la lista), y NADA
            # llamado `contradictorios`: un integrador que leyera X["contradictorios"]
            # obtenia [] mientras el conteo decia 2. No es un fallo de calculo, es una
            # trampa de nombres — y ya mordio a LOGISTICA GOLDEN. `banderas` se
            # conserva porque hay consumidores vivos; `campos_contradictorios` tambien.
            "campos_contradictorios": contradictorios,
            "n_contradictorios": contradictorios,
            "contradictorios": banderas,
            "banderas": banderas,
            "saltadas": saltadas, "disc": disc}


def autoprueba(silencio=False):
    """El extractor se prueba contra casos que se saben antes de creerle."""
    casos = [
        ("1 Bolso Negro y 1 Bolso Rojo", 2),
        ("2 Bolso Billetera manos libre Negro", 2),
        ("1 Bolso Rosa, 1 Bolso Negro, 1 Bolso Gris", 3),
        ("2 Bolsos Luxury Girl (1 en color negro y 1 en café caramelo)", 2),
        ("1 Bolso Rosa Claro y 2 Bolso Negro", 3),
        ("1 LipoBlue Boost y 1 Envío Prioritario", 1),
        ("Bolso Negro", None),
    ]
    casos_col = [
        # (notas de Dropi, texto del chat, se espera discrepancia?)
        ("Bolso: Negro Azabache *** Bolso: Palo de Rosa ***",
         "1 Bolso Negro y 1 Bolso Rosa Claro", False),
        ("Bolso: Negro Azabache *** Bolso: Negro Azabache ***",
         "1 Bolso Rojo y 1 Bolso Negro", True),      # el caso que describio FER
        ("Bolso: Cafe Caramelo ***", "1 Bolso Cafe Caramelo", False),
        ("Bolso: Negro Azabache ***", "2 Bolso Negro", True),
        ("Bolso: Rosa Oscuro ***", "1 Bolso Rosa Claro", True),
    ]
    # la tercera categoria tambien se prueba: campo 2 contra texto 1 debe CONTRADECIR
    if cantidad_chat("1 Bolso Billetera portacelular manos libre Negro") != 1:
        print("  FALLA: el texto de {CLIENTA_B} deberia leerse como 1")
    malos = [(t, e, cantidad_chat(t)) for t, e in casos if cantidad_chat(t) != e]
    for notas, chat, esperado in casos_col:
        if (colores_notas(notas) != colores_chat(chat)) != esperado:
            malos.append((chat, esperado, dict(colores_notas(notas))))
    if not silencio:
        for t, e, r in malos:
            print(f"  FALLA esperado={e} obtuvo={r} · {t}")
        total = len(casos) + len(casos_col)
        print(f"autoprueba del extractor: {total-len(malos)}/{total} correctos")
    return not malos


if __name__ == "__main__":
    if not autoprueba():
        sys.exit("El extractor de cantidad está malo. No se sigue.")
    if len(sys.argv) < 3:
        sys.exit("uso: cruzar_chat_orden.py <dropi.json> <chatea.json>")
    D = leer_json(sys.argv[1])
    C = leer_json(sys.argv[2])
    r = cruzar(D.get("ordenes") or [], C)
    print(f"\nmodificables {r['modificables']} · comparadas de verdad {r['comparadas']} · "
          f"saltadas {len(r['saltadas'])}")
    print(f"discrepancias encontradas: {len(r['disc'])}")
    for x in r["disc"]:
        print(f"\n  #{x['orden']} · {x['cliente']} · {x['tel']} · {x['ciudad']} · [{x['status']}]")
        print(f"     chat : {x['chat'][:90]}")
        print(f"     dropi: {x['dropi'][:90]}")
        for f in x["fallos"]:
            print(f"     >>> {f['tipo']}: chat {f['chat']} vs dropi {f['dropi']}")
