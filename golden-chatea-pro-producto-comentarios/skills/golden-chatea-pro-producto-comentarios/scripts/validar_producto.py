#!/usr/bin/env python3
"""
Validador del campo [Comentarios] Productos de Chatea Pro.

Comprueba lo que rompe en silencio: las 5 llaves exactas, los tipos, el tope nativo de
`desc` (500), los dos techos del bot field (20.000 escapados / ~17.000 crudos), las
colisiones de disparadores entre productos y los disparadores demasiado genericos.

Termina en 0 si no hay errores, en 1 si los hay. Los avisos no hacen fallar.

Uso:
    python3 validar_producto.py productos.json
    python3 validar_producto.py productos.json --json     # salida estructurada
    cat productos.json | python3 validar_producto.py -

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
TOPE_DESC = 500
TOPE_ESCAPADO = 20000
OBJETIVO_ESCAPADO = 19000
ESTADOS = {"activo", "inactivo"}

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


def cargar(ruta):
    crudo = sys.stdin.read() if ruta == "-" else open(ruta, encoding="utf-8").read()
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
    texto = sys.stdin.read() if ruta == "-" else open(ruta, encoding="utf-8").read()
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

    if isinstance(nombre, str) and not nombre.strip():
        err(f"{etq}: 'name' vacio")

    desc = p.get("desc")
    if isinstance(desc, str):
        n = len(desc)
        if n > TOPE_DESC:
            err(
                f"{etq}: 'desc' mide {n} — se pasa por {n - TOPE_DESC} del tope nativo ({TOPE_DESC}). "
                "Por API entra, pero se corta el dia que alguien guarde desde el panel. "
                "Recortala con --medir"
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

    if esc > TOPE_ESCAPADO:
        err(f"TECHO DEL BOT FIELD: {esc} escapados sobre {TOPE_ESCAPADO}. "
            "La API responde 200 ok, guarda el JSON CORTADO y el asistente muere en silencio")
    elif esc > OBJETIVO_ESCAPADO:
        avi(f"{esc} escapados — sobre el objetivo de {OBJETIVO_ESCAPADO}, sin margen para crecer")

    activos = sum(1 for p in datos if isinstance(p, dict) and p.get("estado") == "activo")
    if activos > MAX_ACTIVOS_COMODOS:
        avi(f"{activos} productos en 'activo' — cada activo de mas es un candidato mas al que el bot "
            "puede anclar un comentario generico. Pon en 'inactivo' los que no tengan pauta corriendo")

    if args.json:
        print(json.dumps({
            "ok": not errores,
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

    print(f"\n  Productos: {len(datos)}  ({activos} activo(s), {len(datos) - activos} inactivo(s))")
    print(f"  Campo:     {crudo} crudos / {esc} escapados  (techo {TOPE_ESCAPADO}, objetivo {OBJETIVO_ESCAPADO})")
    for i, p in enumerate(datos, 1):
        if isinstance(p, dict):
            d = p.get("desc") if isinstance(p.get("desc"), str) else ""
            r = p.get("rela") if isinstance(p.get("rela"), str) else ""
            nm = (p.get("name") or "")[:44] if isinstance(p.get("name"), str) else "?"
            print(f"    {i}. desc {len(d):>4}/{TOPE_DESC}   rela {len(disparadores(r)):>3} disp.   {nm}")

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
