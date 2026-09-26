#!/usr/bin/env python3
"""
Validador del campo [Comentarios] Productos de Chatea Pro.

Comprueba lo que rompe en silencio: las 5 llaves exactas, los tipos, los topes del
formulario (name 255 · desc 500 · rela 10 ETIQUETAS), el techo de GUARDADO del campo
(~20.000 CRUDOS en tipo JSON, 500.000 en LONG JSON), las colisiones de disparadores entre
productos y los disparadores demasiado genericos.

El techo se mide en CRUDOS, no en escapados: hay produccion viva con 21.457 escapados que
guarda y se relee identica. El escapado se reporta como AVISO porque el limite de EJECUCION
del flujo es otro y mas estrecho. Detalle y las cinco mediciones en references/escritura-api.md.

Termina en 0 si no hay errores, en 1 si los hay. Los avisos no hacen fallar.

Uso:
    python3 validar_producto.py productos.json --via formulario   # se pega en el panel
    python3 validar_producto.py productos.json --via json         # entra por Campos de Bot
    python3 validar_producto.py productos.json --via json --json  # salida estructurada
    cat productos.json | python3 validar_producto.py - --via formulario

    # medir un texto suelto contra el tope de 500 mientras lo recortas (no valida nada mas)
    python3 validar_producto.py --medir borrador_desc.txt
    pbpaste | python3 validar_producto.py --medir -
"""

import argparse
import difflib
import json
import re
import sys
import unicodedata

LLAVES = ["img", "name", "desc", "rela", "estado"]

# TOPES DEL FORMULARIO DEL PANEL, leidos de sus propios contadores el 2026-09-22 en la
# pantalla "Agregar nuevo producto" del agente de comentarios (cuenta 236245):
#   "36/255 caracteres" bajo Nombre del producto
#   "481/500 caracteres" (en rojo) bajo Descripcion del producto
#   "7/10 etiquetas" bajo "Como relacionar el post", que es el campo `rela`
# Los tres BLOQUEAN por la via formulario y solo AVISAN por la via json.
TOPE_NAME = 255
TOPE_DESC = 500
TOPE_ETIQUETAS = 10

# 🔴 NO HAY UN TECHO: HAY DOS, y se observan con pruebas DISTINTAS. Contrastadas las cinco
# mediciones de la casa, ninguna hipotesis de techo unico las explica todas:
#
#   Observando GUARDAR y RELEER (config-comentarios, 2026-09-22, campo array de comentarios):
#     13.004 crudos                     -> guarda
#     19.617 crudos / 21.457 escapados  -> guarda y se relee IDENTICO byte a byte
#     20.811 crudos                     -> error 500 al guardar
#   Observando SI EL BOT DISPARA al ejecutarse (BRIEFING, 2026-08):
#     16.882 crudos / 19.895 escapados  -> dispara
#     19.922 crudos / 23.266 escapados  -> NO dispara
#
# El caso de 21.457 escapados GUARDADO Y FUNCIONANDO mata la idea de "20.000 escapados" como
# tope de guardado. Y el de 19.922 crudos que NO dispara mata la idea de que crudos explique
# el disparo. Conclusion honesta: el GUARDADO topa en ~20.000 CRUDOS (entre 19.617 que entra y
# 20.811 que revienta), y el EJECUTAR tiene un limite propio, mas estrecho, para el que la
# unica evidencia que hay esta en escapados.
#
# 🔴 Y OJO CON LA SEGUNDA MITAD, que es el fallo simetrico que casi se nos cuela: las dos
# observaciones de EJECUCION (19.895 dispara / 23.266 no) se midieron sobre campos
# [Producto Ventas Wp], que es EL MISMO CAMPO AJENO del que venia el error del guardado. O sea
# que la frontera de ejecucion es HEREDADA, no medida en el campo de comentarios: aqui no hay
# ni un "dispara" ni un "no dispara" observado. La ley que corrigio el primer numero se aplica
# igual al segundo.
#
# Por eso aqui: CRUDOS bloquea (medicion directa de escritura EN ESTE CAMPO) y ESCAPADO solo
# AVISA, Y EL AVISO DECLARA QUE SU FRONTERA ES HEREDADA. Poner error con un numero prestado es
# exactamente lo que ya nos mordio una vez.
TOPE_CRUDO = 20000
TOPE_CRUDO_LONG = 500000
OBJETIVO_CRUDO = 19000
AVISO_ESCAPADO = 20000
ESTADOS = {"activo", "inactivo"}

# LA VIA POR LA QUE ENTRA EL PRODUCTO. No es un detalle de forma: decide si el tope
# nativo de 500 BLOQUEA o solo avisa. Por eso es un dato de entrada obligatorio y no
# se supone (FILA 2 del Centro de Mando, 2026-09-05).
#   formulario = alguien lo pega en el formulario del panel  -> el campo CORTA en 500
#   json       = entra por Campos de Bot / API con el JSON   -> 500 es exceso aceptable
VIAS = ("formulario", "json")
VIA = "formulario"          # se fija en main(); el default es el estricto por si acaso
TECHO = TOPE_CRUDO          # se fija en main(); JSON por defecto, LONG JSON con --long-json

MIN_DISPARADORES = 8
IDEAL_DISPARADORES = 15
MAX_ACTIVOS_COMODOS = 6

# Un disparador distingue si trae una palabra de la marca, o dos palabras con contenido,
# o una sola muy especifica (>=7 letras). Las de abajo no aportan: existen en cualquier
# comentario de cualquier producto, y por eso no cuentan como palabra con contenido.
VACIAS = {
    # gramatica
    "de", "del", "la", "el", "los", "las", "un", "una", "al", "y", "o",
    "en", "con", "para", "por", "sin", "sobre", "mi", "tu", "su", "me", "te", "se", "lo",
    "les", "que", "cual", "cuales", "como", "cuanto", "cuanta", "donde", "cuando", "quien",
    "esto", "esta", "este", "eso", "ese", "hay", "muy", "mas", "menos", "todo", "toda",
    # verbos y sustantivos de la conversacion comercial: valen para cualquier producto
    "es", "son", "estan", "hacen", "hace", "tiene", "tienen", "quiero", "quisiera", "dame",
    "pido", "pide", "pedir", "comprar", "compro", "vale", "cuesta", "sirve", "ver", "envio",
    "envios", "envian", "entrega", "entregan", "precio", "precios", "valor", "costo",
    "info", "informacion", "disponible", "disponibles", "pedido", "producto", "unidad",
    "unidades", "hola", "buenas", "gracias", "porfa", "favor", "interesa", "interesado",
    "interesada", "garantia", "contraentrega", "ubicacion", "telefono", "whatsapp",
    "numero", "catalogo", "stock", "domicilio", "tallas", "colores",
}

# Categorias que NUNCA distinguen solas, aunque esten en el nombre del producto: dos cremas
# en el mismo campo se pelean por 'crema'. Van dentro de una frase o no van.
NUNCA_SOLAS = {
    "base", "crema", "spray", "serum", "gel", "aceite", "jabon", "polvo", "locion",
    "shampoo", "mascarilla", "pastillas", "capsulas", "gotas", "kit", "set", "pack",
    "combo", "banda", "faja", "aparato", "maquina", "hongos", "brillo", "manchas",
    "arrugas", "vello", "cabello", "piel", "olor", "dolor", "grasa", "verrugas",
}

# Marcador que la skill deja cuando el cliente todavia no subio la imagen.
RE_MARCADOR = re.compile(r"^\s*\[[^\]]*\]\s*$")

errores = []
avisos = []
notas = []


def err(msg):
    errores.append(msg)


def avi(msg):
    avisos.append(msg)


def normaliza(texto):
    """Minusculas y sin tildes: asi se comparan disparadores entre productos."""
    base = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn").strip()


def escapado(valor):
    """Lo que de verdad cuenta contra el techo: el string ya escapado por el flujo.

    OJO: aqui `json.dumps` va con `ensure_ascii` en su valor POR DEFECTO (True). Eso es lo
    que convierte cada tilde en `\\u00e1` (6 caracteres) y cada emoji en un par subrogado
    (12). Con `ensure_ascii=False` una tilde contaria 1 y la medicion queda apagada: un
    campo de 20.345 se reportaria como 10.769 y saldria en verde.

    No confundir con la SERIALIZACION del valor que se manda a la API, que si va con
    `ensure_ascii=False` (ver `references/escritura-api.md`). Se guarda sin escapar, se
    mide escapado.
    """
    return len(json.dumps(valor)[1:-1])


def disparadores(rela):
    return [t.strip() for t in rela.split(",") if t.strip()]


def palabras_del_nombre(nombre):
    """Formas de la marca contra las que se reconoce una errata legitima en el rela.

    Ademas de las palabras sueltas incluye los pares pegados y el nombre entero sin
    espacios, porque la gente escribe la marca junta: 'fitban' es errata de
    'Nordika Fit Band' y comparandola solo contra 'fit' o 'band' no se reconoce.
    """
    limpio = normaliza(nombre.split("|")[0])
    palabras = [w for w in re.findall(r"[a-z0-9]+", limpio) if len(w) >= 3]
    formas = list(palabras)
    for a, b in zip(palabras, palabras[1:]):
        formas.append(a + b)
    if len(palabras) > 1:
        formas.append("".join(palabras))
    return formas


def es_variante_del_nombre(token, formas):
    """Una errata de la marca (velux, nordica, fitban) NO es un disparador generico."""
    if len(token) < 3:
        return False
    for w in formas:
        if difflib.SequenceMatcher(None, token, w).ratio() >= 0.7:
            return True
        if len(token) >= 5 and (token in w or w in token):
            return True
    return False


def palabras_distintivas(nombre):
    """Palabras del nombre que sirven para DESEMPATAR: las largas y no vacias."""
    fuera = {"de", "la", "el", "los", "las", "y", "con", "para", "premium", "original", "ml", "g"}
    # str() a proposito: este detector corre DESPUES de que se hayan apuntado los errores de tipo,
    # y un `name` que no es string tiene que salir como ERROR REPORTADO, no como AttributeError.
    # Un validador que revienta a mitad se lleva por delante los avisos que ya habia encontrado.
    return {w for w in normaliza(str(nombre)).split() if len(w) >= 4 and w not in fuera}


def colisiones_entre(productos):
    """Etiquetas que DOS productos del mismo catalogo pueden reclamar.

    Devuelve (gravedad, etiqueta_a, indice_a, etiqueta_b, indice_b):
      IDENTICO     la misma etiqueta literal en dos productos
      NORMALIZADO  la misma sin tildes/mayusculas/signos ('Le'coterra' vs 'lecoterra')
      CONTENIDO    una contenida en otra ('base coreana' dentro de 'base coreana hidratante')

    NO marca una etiqueta que ya lleva una palabra distintiva de SU producto: ahi el nombre
    comercial ya desempata, que es exactamente la salida de Kevin en 2:15:02.
    """
    idx = []
    for i, p in enumerate(productos):
        if not isinstance(p, dict):
            continue
        propias = palabras_distintivas(p.get("name", ""))
        for e in disparadores(str(p.get("rela", ""))):
            n = normaliza(str(e))
            idx.append((i, e, n, bool(propias & set(n.split()))))

    choques = []
    for a in range(len(idx)):
        ia, ea, na, anca = idx[a]
        for b in range(a + 1, len(idx)):
            ib, eb, nb, ancb = idx[b]
            if ia == ib:
                continue
            if na == nb:
                choques.append(("IDENTICA" if ea == eb else "NORMALIZADA", ea, ia, eb, ib))
            elif len(na) >= 9 and len(nb) >= 9 and (na in nb or nb in na) \
                    and not (anca and ancb):
                choques.append(("CONTENIDA", ea, ia, eb, ib))
    return choques


def cargar(ruta):
    try:
        crudo = sys.stdin.read() if ruta == "-" else open(ruta, encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR  no se pudo leer '{ruta}': {e.strerror}", file=sys.stderr)
        sys.exit(1)
    crudo = crudo.strip()
    try:
        datos = json.loads(crudo)
    except json.JSONDecodeError as e:
        print(f"ERROR  el archivo no es JSON valido: {e}", file=sys.stderr)
        sys.exit(1)
    # El campo puede venir como el string que guarda la API (JSON dentro de JSON).
    if isinstance(datos, str):
        notas.append("el archivo traia el valor como string; se decodifico una capa mas")
        try:
            datos = json.loads(datos)
        except json.JSONDecodeError as e:
            print(f"ERROR  el string interior no es JSON valido: {e}", file=sys.stderr)
            sys.exit(1)
    return datos


def modo_medir(ruta):
    """Mide un borrador de `desc` mientras se recorta, sin montar el JSON entero."""
    try:
        texto = sys.stdin.read() if ruta == "-" else open(ruta, encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR  no se pudo leer '{ruta}': {e.strerror}", file=sys.stderr)
        sys.exit(1)
    texto = texto.strip("\n")
    n = len(texto)
    sobra = n - TOPE_DESC
    print(f"\n  desc: {n} / {TOPE_DESC} caracteres")
    if sobra > 0:
        print(f"  SE PASA POR {sobra}. Recorta en este orden:")
        print("    1. adjetivos del bloque descriptivo")
        print("    2. la linea de confianza (envio / pago / original)")
        print("    3. la regla de marca menos especifica")
        print("  Nunca: los precios ni las dos reglas de marca duras.")
    else:
        print(f"  Cabe, con {-sobra} de margen.")
    lineas = [l for l in texto.split("\n") if l.strip()]
    if lineas:
        print("\n  Peso por linea (para saber que recortar):")
        for l in sorted(lineas, key=len, reverse=True)[:6]:
            print(f"    {len(l):>4}  {l[:66]}")
    print()
    return 0 if sobra <= 0 else 1


def valida_producto(i, p):
    etq = f"producto {i}"
    if not isinstance(p, dict):
        err(f"{etq}: no es un objeto (es {type(p).__name__})")
        return

    nombre = p.get("name") if isinstance(p.get("name"), str) else ""
    if nombre:
        etq = f"producto {i} ({nombre[:40]})"

    llaves = list(p.keys())
    faltan = [k for k in LLAVES if k not in llaves]
    sobran = [k for k in llaves if k not in LLAVES]

    if faltan:
        err(f"{etq}: FALTAN llaves {faltan} — con 4 llaves el panel no interpreta el producto")
    if sobran:
        err(f"{etq}: llaves de mas {sobran} — el esquema es exactamente {LLAVES}")
    if not faltan and not sobran and llaves != LLAVES:
        avi(f"{etq}: las 5 llaves estan pero desordenadas ({llaves}); el orden canonico es {LLAVES}")

    for k in LLAVES:
        if k in p and not isinstance(p[k], str):
            err(f"{etq}: '{k}' es {type(p[k]).__name__}, debe ser string — otro tipo se pierde al guardar")

    img = p.get("img")
    if isinstance(img, str):
        if not img.strip():
            avi(f"{etq}: 'img' vacio — pendiente de subir la imagen desde el panel y pegar la URL")
        elif RE_MARCADOR.match(img):
            avi(f"{etq}: 'img' es un marcador de pendiente ({img.strip()}) — sustituyelo antes de escribir")
        elif "media.chateapro.app" in img:
            m = re.search(r"/temp/\d{6}/([^/]+)/", img)
            cuenta = m.group(1) if m else "?"
            avi(
                f"{etq}: 'img' apunta a media.chateapro.app con ID de cuenta '{cuenta}'. "
                "Si no es la cuenta de ESTE workspace, la imagen apunta a la cuenta de origen"
            )
        elif not img.startswith(("http://", "https://")):
            err(f"{etq}: 'img' no es una URL ni un marcador de pendiente")

    if isinstance(nombre, str):
        if not nombre.strip():
            err(f"{etq}: 'name' vacio")
        elif len(nombre) > TOPE_NAME:
            msg = (f"{etq}: 'name' mide {len(nombre)} — se pasa por {len(nombre) - TOPE_NAME} "
                   f"del tope del formulario ({TOPE_NAME})")
            err(msg + ". La via es FORMULARIO: el campo CORTA al guardar") if VIA == "formulario" \
                else avi(msg + ". Por la via JSON entra, pero se corta si alguien abre el formulario")

    desc = p.get("desc")
    if isinstance(desc, str):
        n = len(desc)
        if n > TOPE_DESC:
            if VIA == "formulario":
                err(
                    f"{etq}: 'desc' mide {n} — se pasa por {n - TOPE_DESC} del tope nativo "
                    f"({TOPE_DESC}) y la via es FORMULARIO: el campo CORTA al guardar y el texto "
                    "sobrante se pierde. Recortala con --medir, o entrega la version larga solo "
                    "por la via json"
                )
            else:
                avi(
                    f"{etq}: 'desc' mide {n} (tope nativo {TOPE_DESC}). Por la via JSON entra "
                    "completa, pero el dia que alguien abra ESE producto en el formulario del "
                    "panel y guarde, se corta. Entrega tambien la version de 500 y dilo"
                )
        elif n > TOPE_DESC * 0.96:
            avi(f"{etq}: 'desc' en {n} de {TOPE_DESC} ({n * 100 // TOPE_DESC}%) — queda poco margen")
        if not desc.strip():
            err(f"{etq}: 'desc' vacia — es lo que alimenta {{DESCRIPCION_PRODUCTO}}")
        elif not re.search(r"regla[s]?\s+de\s+marca", desc, re.I):
            avi(f"{etq}: 'desc' sin bloque REGLAS DE MARCA — sin el, la IA rellena los huecos sola")

    estado = p.get("estado")
    if isinstance(estado, str) and estado not in ESTADOS:
        err(f"{etq}: 'estado' = '{estado}'; solo vale {sorted(ESTADOS)} en minuscula")

    rela = p.get("rela")
    if isinstance(rela, str):
        toks = disparadores(rela)
        marca = palabras_del_nombre(nombre) if nombre else []
        if not toks:
            err(f"{etq}: 'rela' vacio — el bot no podra reconocer ningun comentario de este producto")
        elif len(toks) < MIN_DISPARADORES:
            err(
                f"{etq}: 'rela' con {len(toks)} disparadores (minimo {MIN_DISPARADORES}, "
                f"ideal {IDEAL_DISPARADORES}-30) — va a fallar el emparejamiento"
            )
        elif len(toks) < IDEAL_DISPARADORES:
            avi(f"{etq}: 'rela' con {len(toks)} disparadores; apunta a {IDEAL_DISPARADORES}-30")

        if len(toks) > TOPE_ETIQUETAS:
            sobran = len(toks) - TOPE_ETIQUETAS
            if VIA == "formulario":
                err(f"{etq}: 'rela' con {len(toks)} etiquetas y el formulario topa en "
                    f"{TOPE_ETIQUETAS}: por esa via se PIERDEN {sobran}, que es justo la capa 4 "
                    "(los hooks del anuncio). Entra completo solo por la via json")
            else:
                avi(f"{etq}: 'rela' con {len(toks)} etiquetas (el formulario topa en "
                    f"{TOPE_ETIQUETAS}). Por JSON entran todas, pero si alguien abre ese producto "
                    f"en el panel y guarda, se quedan {TOPE_ETIQUETAS} y se van {sobran}")

        for t in toks:
            plano = normaliza(t)
            palabras = [w for w in re.findall(r"[a-z0-9]+", plano) if len(w) >= 3]
            contenido = [w for w in palabras if w not in VACIAS]
            solo_categoria = len(contenido) == 1 and contenido[0] in NUNCA_SOLAS
            if not solo_categoria:
                if any(es_variante_del_nombre(w, marca) for w in palabras):
                    continue  # trae la marca (o una errata suya): distingue por definicion
                if len(contenido) >= 2 or any(len(w) >= 7 for w in contenido):
                    continue
            avi(
                f"{etq}: disparador generico '{t}' — no distingue este producto de otro, "
                "asi que secuestra comentarios ajenos o colisiona. Metele el nombre del "
                "producto o su categoria completa"
            )

        if marca:
            planos = [normaliza(t) for t in toks]
            if not any(marca[0] in t for t in planos):
                avi(f"{etq}: el nombre '{marca[0]}' no aparece en ningun disparador del 'rela'")

    return p


def main():
    ap = argparse.ArgumentParser(description="Valida el campo [Comentarios] Productos de Chatea Pro")
    ap.add_argument("archivo", nargs="?", help="JSON con la lista de productos, o '-' para stdin")
    ap.add_argument("--json", action="store_true", help="salida estructurada")
    ap.add_argument("--long-json", action="store_true",
                    help="el campo destino es de tipo LONG JSON (techo 500.000, no 20.000)")
    ap.add_argument("--via", choices=VIAS,
                    help="POR DONDE entra el producto: 'formulario' (se pega en el panel: el "
                         "tope de 500 BLOQUEA) o 'json' (Campos de Bot / API: 500 solo avisa). "
                         "Obligatoria al validar un archivo")
    ap.add_argument("--medir", metavar="ARCHIVO",
                    help="mide un borrador de desc contra el tope de 500 ('-' para stdin)")
    args = ap.parse_args()

    if args.medir:
        if args.archivo:
            # Silenciar la validacion del array porque tambien pasaron --medir seria
            # exactamente el fallo silencioso que esta skill existe para evitar.
            ap.error(f"--medir y un archivo JSON ('{args.archivo}') son excluyentes: "
                     "--medir solo mide una desc suelta y NO valida nada mas. "
                     "Corre los dos por separado")
        return modo_medir(args.medir)
    if not args.archivo:
        ap.error("falta el archivo JSON (o usa --medir para medir una desc suelta)")

    if not args.via:
        ap.error("falta --via. La via NO se supone: decide si el tope de 500 bloquea o avisa.\n"
                 "  --via formulario  el producto se pega en el formulario del panel (500 CORTA)\n"
                 "  --via json        entra por Campos de Bot / API (500 solo avisa)\n"
                 "Preguntasela al usuario si no la sabes.")
    global VIA, TECHO
    VIA = args.via
    TECHO = TOPE_CRUDO_LONG if args.long_json else TOPE_CRUDO

    datos = cargar(args.archivo)

    if isinstance(datos, dict):
        err("el valor es un objeto suelto, no una lista — sin corchetes el producto no se renderiza")
        datos = [datos]
    if not isinstance(datos, list):
        print(f"ERROR  se esperaba una lista de productos, llego {type(datos).__name__}", file=sys.stderr)
        sys.exit(1)
    if not datos:
        err("la lista esta VACIA — sintoma clasico: 'Comentario NO automatizado'. "
            "Revisa si los productos viven en '[Comentarios] Productos extendido'")

    for i, p in enumerate(datos, 1):
        valida_producto(i, p)

    # Colisiones entre productos: el bot elige uno y elige distinto cada vez.
    mapa = {}
    for i, p in enumerate(datos, 1):
        if not isinstance(p, dict) or not isinstance(p.get("rela"), str):
            continue
        for t in disparadores(p["rela"]):
            mapa.setdefault(normaliza(t), []).append((i, t))

    for plano, usos in mapa.items():
        idx = sorted({i for i, _ in usos})
        if len(idx) > 1:
            err(f"disparador '{usos[0][1]}' repetido en los productos {idx} — "
                "el bot elegira uno distinto cada vez")

    # Contencion entre productos: 'entrenar en casa' dentro de 'entrenar en casa sin excusas'
    # engancha igual que un duplicado. Dentro del MISMO producto es normal (hook con y sin emoji).
    planos = sorted(mapa, key=len)
    for a in planos:
        for b in planos:
            if a is b or len(a) >= len(b) or a not in b:
                continue
            ia = {i for i, _ in mapa[a]}
            ib = {i for i, _ in mapa[b]}
            cruce = sorted(ia | ib)
            if ia - ib and ib - ia:
                err(f"disparador '{mapa[a][0][1]}' esta contenido en '{mapa[b][0][1]}' "
                    f"de otro producto {cruce} — mismo secuestro que un duplicado")

    nombres = {}
    for i, p in enumerate(datos, 1):
        if isinstance(p, dict) and isinstance(p.get("name"), str):
            nombres.setdefault(normaliza(p["name"]), []).append(i)
    for n, idx in nombres.items():
        if len(idx) > 1:
            avi(f"nombre repetido en los productos {idx}")

    compacto = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    crudo = len(compacto)
    esc = escapado(compacto)

    # 1 · GUARDAR. Medido escribiendo y releyendo: se topa en CRUDOS. Esto bloquea.
    if crudo > TECHO:
        err(f"NO VA A GUARDAR ENTERO: {crudo} crudos sobre {TECHO}. 🔴 Y NO VAS A VER EL FALLO: "
            f"medido directo el 2026-09-22 sobre un campo `array` propio, la API acepta el "
            f"payload, responde HTTP 200 y TRUNCA EN SILENCIO a {TOPE_CRUDO} exactos (19.898 "
            f"entra entero; 20.128, 23.125 y 60.000 vuelven todos releidos en 20.000). El corte "
            f"cae a mitad de palabra, el JSON deja de parsear y el bot se queda SIN productos. "
            f"Aqui perderias {crudo - TECHO} caracteres sin un solo aviso")
    elif TECHO == TOPE_CRUDO and crudo > OBJETIVO_CRUDO:
        avi(f"{crudo} crudos — sobre el objetivo de {OBJETIVO_CRUDO}, sin margen para crecer")

    # 2 · EJECUTAR. Otro limite, mas estrecho, y la unica evidencia esta en escapados. AVISA,
    # no bloquea: hay produccion viva por encima de este numero.
    if esc > AVISO_ESCAPADO and crudo <= TECHO:
        avi(f"{esc} escapados. El campo GUARDA (los crudos caben). AVISO CON FRONTERA HEREDADA: "
            "las unicas observaciones de que un campo demasiado grande deja de DISPARAR el bot "
            "(19.895 si / 23.266 no) se midieron en campos [Producto Ventas Wp], NO en el de "
            "comentarios, asi que para ESTE campo el limite de ejecucion no esta medido ni por "
            "arriba ni por abajo. No recortes por este numero: si el asistente se queda mudo sin "
            "error visible, mira Panel -> Registros de errores y sospecha de esto")

    # 3 · COLISIONES ENTRE PRODUCTOS. La regla CENTRAL de Kevin, y la unica que no se puede
    # comprobar mirando un producto de uno en uno: el criterio no es "describe bien el producto"
    # sino "solo ESTE producto puede reclamar la etiqueta".
    #   CITA 1:50:24: "vendemos 3 tipos de magnesio. Si solo le pongo magnesio, el bot se me va a
    #   enloquecer sin saber a cual de los 3 responder."
    #   CITA misma escena: "le voy a poner dormir... NO, porque tengo otro magnesio que tambien
    #   sirve para dormir."
    # Fijate en el segundo descarte: "dormir" DESCRIBE PERFECTAMENTE el producto. Lo descarta por
    # COMPARTIDO. Por eso el detector de genericos de arriba NO cubre esto: mide cada producto
    # por separado, y una colision solo existe cuando se miran DOS a la vez.
    for grav, ea, ia, eb, ib in colisiones_entre(datos):
        na = str(datos[ia].get("name", f"#{ia}"))[:32]
        nb = str(datos[ib].get("name", f"#{ib}"))[:32]
        err(f"COLISION {grav}: la etiqueta '{ea}' ({na}) y '{eb}' ({nb}) las pueden reclamar los "
            f"DOS productos. El bot no sabra a cual responder. Metele a cada una el nombre "
            f"comercial que las distinga, que es la salida que da el propio Kevin "
            f"(`Magnesio Complex 8 en 1` contra `Magnesio 2 en 1`)")

    activos = sum(1 for p in datos if isinstance(p, dict) and p.get("estado") == "activo")
    if activos > MAX_ACTIVOS_COMODOS:
        avi(f"{activos} productos en 'activo' — cada activo de mas es un candidato mas al que el bot "
            "puede anclar un comentario generico. Pon en 'inactivo' los que no tengan pauta corriendo")

    if args.json:
        print(json.dumps({
            "ok": not errores,
            "via": VIA,
            "productos": len(datos),
            "activos": activos,
            "crudo": crudo,
            "escapado": esc,
            "errores": errores,
            "avisos": avisos,
            "notas": notas,
            "compacto": compacto,
        }, ensure_ascii=False, indent=2))
        return 1 if errores else 0

    print(f"\n  Via:       {VIA}  ({'el tope de 500 BLOQUEA' if VIA == 'formulario' else 'el tope de 500 solo avisa'})")
    print(f"  Productos: {len(datos)}  ({activos} activo(s), {len(datos) - activos} inactivo(s))")
    tipo = "LONG JSON" if TECHO == TOPE_CRUDO_LONG else "JSON"
    print(f"  Campo:     {crudo} crudos / {esc} escapados  (tipo {tipo}, guardado topa en {TECHO} CRUDOS)")
    for i, p in enumerate(datos, 1):
        if isinstance(p, dict):
            d = p.get("desc") if isinstance(p.get("desc"), str) else ""
            r = p.get("rela") if isinstance(p.get("rela"), str) else ""
            nm = (p.get("name") or "")[:44] if isinstance(p.get("name"), str) else "?"
            nd = len(disparadores(r))
            marca = "!" if (len(d) > TOPE_DESC or nd > TOPE_ETIQUETAS) else " "
            print(f"   {marca}{i}. desc {len(d):>4}/{TOPE_DESC}   rela {nd:>3}/{TOPE_ETIQUETAS} etiq.   {nm}")

    for n in notas:
        print(f"\n  nota: {n}")
    if avisos:
        print(f"\n  AVISOS ({len(avisos)})")
        for a in avisos:
            print(f"    ~ {a}")
    if errores:
        print(f"\n  ERRORES ({len(errores)})")
        for e in errores:
            print(f"    x {e}")
        print("\n  NO ESCRIBAS todavia. Corrige y vuelve a correr.\n")
        return 1

    print("\n  OK — el esquema, los topes y los disparadores pasan.")
    print("  JSON compacto listo para pegar:\n")
    print(compacto)
    print("\n  Recuerda: escribir con PUT (POST devuelve 200 y no escribe), y RELEER del servidor.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
