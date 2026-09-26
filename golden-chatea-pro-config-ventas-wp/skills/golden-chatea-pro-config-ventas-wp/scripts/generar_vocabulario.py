#!/usr/bin/env python3
"""generar_vocabulario.py — deriva assets/limites.json -> vocabulario_direccion_por_pais
de los PACKS de golden-chatea-pro-validacion-direcciones/references/<pais>.md.

Por que un generador y no un mapa escrito a mano
  Ley de FER (references/paises.md): el vocabulario de direccion NO se hereda de un pais a
  otro. La fuente es el pack autoritativo de cada pais, no una traduccion mia. Este script
  copia del pack, sin interpretar:
    campos_memoria  <- la linea "Bien estructurada: a + b + c" del pack, partida por " + "
    aclaracion      <- la linea "... no es direccion: pide ..." del pack, sin los ejemplos
                       entre parentesis
    aclaracion_corta<- esa misma linea, solo la parte anterior a ":"
  y guarda la cita literal (cita_estructura, cita_aclaracion) para que un banco pueda
  comprobar, sin este script, que el pack sigue diciendo lo mismo.

Lo que NO hace
  * No inventa un pais que no tiene pack: sin pack, sin entrada (cae al generico neutro
    declarado de build_config.py; jamas hereda a Colombia).
  * No toca COLOMBIA ni MEXICO (escritos a mano; Colombia sale byte a byte igual al espacio
    real de Golden). Solo les ancla fuente y citas.
  * No decide por un pack ambiguo: los paises sin linea limpia (chile, guatemala, panama)
    van en PARAFRASEADOS, con la cita literal del pack que los respalda, y quedan marcados
    origen="parafraseado del pack" para que se vean como lo que son.

Uso:  python3 scripts/generar_vocabulario.py [--packs RUTA] [--escribir]
      sin --escribir solo muestra lo que haria (y los largos contra el techo).

Correccion 2026-09-21 (Centro de Mando, sobre la v4.13): tres puntos ciegos medidos con
sabotajes que el banco anterior dejaba en 100% verde:
  1. `campos_memoria` alterado (Colombia "departamento" -> "provincia") pasaba, porque solo se
     comprobaba que la CITA siguiera literal en el pack, nunca el CAMPO derivado -- que es lo
     que termina en el prompt del asistente. Cura: `faltantes_contra_pack()` exige que cada
     termino de 4+ letras del campo este tambien en el TEXTO COMPLETO del pack (no solo en su
     cita), para los TRES campos (campos_memoria, aclaracion, aclaracion_corta) y las DOS
     entradas a mano ademas de las derivadas.
  2. `aclaracion` alterada ("Da igual el barrio.") pasaba porque nada la comparaba contra el
     pack. Misma cura: sus terminos ("igual") no estan en el pack y el banco la rechaza.
  3. `origen` borrado en un parafraseado pasaba porque nada exigia que existiera. Cura:
     `ORIGENES_VALIDOS` es un conjunto cerrado y cada entrada se valida contra el.
  Y el total de paises pasaba de 267 a 268 verdes con un campo malo, porque el banco derivaba
  sus propios casos del contenido que estaba revisando. Cura: `PAISES_ESPERADOS` (23) es un
  numero ANCLADO, no lo que salga de contar el mapa.

Pulido 2026-09-21 (Centro de Mando, reverificacion sobre v4.14): dos hallazgos mas, con sus
propios sabotajes:
  4. meter "estado" (la excepcion de Mexico) en COLOMBIA -- probar que la excepcion de
     `A_MANO` queda atada al PAIS y no es una puerta lateral que sirva para cualquiera.
  5. borrar un pais entero del mapa (probado con CHILE) no fallaba limpio: reventaba con
     `KeyError: 'CHILE'` en vez de decir que faltaba. `PAISES_ESPERADOS` solo anclaba el
     NUMERO, no la lista, y nada comparaba presencia/ausencia contra un roster con nombre.
     Cura: `PAISES_MAPA` es el roster ANCLADO (23 nombres, no una cuenta) y
     `diferencias_de_roster()` compara el mapa contra el y dice "falta CHILE" o "sobra X" en
     vez de dejar que un indice directo reviente con traceback.
"""
import argparse, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
LIMITES = os.path.join(AQUI, "..", "assets", "limites.json")
PACKS_DEFECTO = os.path.expanduser(
    "~/.claude/skills/golden-chatea-pro-validacion-direcciones/references")
SIGLAS = {"CP", "CEP", "UF"}
# Tope de la clausula: restricciones.txt de MEXICO llega a 1989/2000 con una aclaracion de
# 92 caracteres; el generador avisa por encima de 100 y build_config se niega si se pasa.
TOPE_ACLARACION = 100
TOPE_CAMPOS = 120

# Roster de paises ANCLADO (no se calcula de las llaves del mapa): los 23 packs de hoy de
# golden-chatea-pro-validacion-direcciones. Si un pack nuevo entra o uno sale, esta lista se
# edita a mano, a proposito -- para que el cambio se note por NOMBRE, no solo por numero.
PAISES_MAPA = {
    "ARGENTINA", "BRASIL", "BULGARIA", "CHEQUIA", "CHILE", "COLOMBIA", "COSTA RICA", "CROACIA",
    "ECUADOR", "ESLOVAQUIA", "ESLOVENIA", "ESPANA", "GRECIA", "GUATEMALA", "HUNGRIA", "MEXICO",
    "PANAMA", "PARAGUAY", "PERU", "POLONIA", "PORTUGAL", "RUMANIA", "VENEZUELA",
}
PAISES_ESPERADOS = len(PAISES_MAPA)  # se lee DEL roster de arriba, nunca al reves

# Los TRES origenes posibles. Un cuarto valor, o ausente, es una entrada rota.
ORIGENES_VALIDOS = {
    "escrito a mano; anclado al pack",
    "derivado mecanicamente del pack",
    "parafraseado del pack",
}

# Conectores que no dicen nada del pais: no se exige que aparezcan literal en el pack.
CONECTORES = {
    "para", "pide", "esta", "está", "ciudad", "region", "región", "sola", "solo", "mas",
    "más", "con", "sin", "que", "los", "las", "una", "por", "del", "referencia", "vivienda",
}


def _sin_acentos(t):
    s = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _terminos(texto):
    """Palabras de 4+ letras, sin acentos ni conectores: lo que un campo dice de VERDAD."""
    return {_sin_acentos(w) for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", texto)
            if _sin_acentos(w) not in CONECTORES}


def faltantes_contra_pack(campo_texto, texto_pack):
    """Terminos de `campo_texto` que NO aparecen en el TEXTO COMPLETO del pack (no solo en
    su cita). Vacio = el campo esta anclado al pack; cualquier termino devuelto es un dato
    que el campo afirma y el pack no respalda -- la clase de fallo del 21-sep."""
    pack_tokens = {_sin_acentos(w) for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", texto_pack)}
    return sorted(t for t in _terminos(campo_texto) if t not in pack_tokens)


def excepciones_desde_a_mano():
    """La UNICA fuente de las excepciones geograficas de A_MANO (ver comentario ahi). El
    banco importa esta misma funcion en vez de copiar la lista: una excepcion nueva se agrega
    en un solo lugar."""
    return {k: set(datos[2]) for k, datos in A_MANO.items()}


def validar_contenido_contra_pack(voc, packs_dir, excepciones=None):
    """Recorre TODA entrada del mapa (a mano y derivada) y devuelve la lista de avisos:
    origen fuera del conjunto cerrado, o un campo con terminos que el pack no dice (salvo
    los de `excepciones`, documentados y nombrados uno por uno en A_MANO)."""
    excepciones = excepciones or {}
    avisos = []
    for k, v in sorted(voc.items()):
        if k.startswith("_"):
            continue
        if v.get("origen") not in ORIGENES_VALIDOS:
            avisos.append(f"{k}: origen '{v.get('origen')}' no esta en ORIGENES_VALIDOS "
                          f"{sorted(ORIGENES_VALIDOS)}")
        fuente = v.get("fuente")
        ruta = os.path.join(packs_dir, fuente) if fuente else None
        if not ruta or not os.path.exists(ruta):
            avisos.append(f"{k}: no se puede validar contenido, falta o no existe 'fuente'")
            continue
        texto_pack = leer_pack(ruta)
        excusados = excepciones.get(k, set())
        for campo in ("campos_memoria", "aclaracion", "aclaracion_corta"):
            if campo not in v:
                continue
            falt = [t for t in faltantes_contra_pack(v[campo], texto_pack) if t not in excusados]
            if falt:
                avisos.append(f"{k}: {campo} tiene terminos que el pack NO dice: {falt} "
                              f"-> {v[campo]!r}")
    return avisos


def diferencias_de_roster(voc):
    """Compara las llaves de `voc` contra el roster ANCLADO `PAISES_MAPA`, por NOMBRE, no
    por numero. Un pais borrado no revienta con KeyError en el primer sitio que lo indexe
    directo: se nombra aqui, primero, con su propio nombre (hallazgo del Centro de Mando,
    21-sep: borrar CHILE reventaba un traceback en vez de decir 'falta CHILE')."""
    actual = {k for k in voc if not k.startswith("_")}
    faltan = sorted(PAISES_MAPA - actual)
    sobran = sorted(actual - PAISES_MAPA)
    return faltan, sobran


# Escritos a mano y NO regenerados: solo se les ancla la fuente.
# `fuera_del_pack`: el pack de validacion-direcciones valida la CALLE (que no necesita nombrar
# la division administrativa superior), pero `campos_memoria` es la ficha COMPLETA que el
# asistente de VENTAS recuerda (ciudad + division superior + calle + barrio/colonia). Por eso
# "departamento" y "estado" no estan en su pack y no es un hueco: es un dato geografico estable
# y publico (la division de primer nivel de Colombia es "departamento" desde la Constitucion de
# 1991; en Mexico, "estado"), no algo que este script haya inventado. Es la UNICA excepcion, y
# se excusa termino por termino: no ablanda el chequeo para nada mas.
A_MANO = {
    "COLOMBIA": ("colombia", ["Una ciudad sola (Bogotá", "barrio claro"], {"departamento"}),
    "MEXICO": ("mexico", ["Una ciudad/colonia sola", "colonia/fraccionamiento"], {"estado"}),
}

# Sin linea limpia en el pack: se parafrasea y se cita el pack. Nada mas se parafrasea.
PARAFRASEADOS = {
    "chile": {
        "aclaracion": "Ciudad o región sin comuna está incompleta: pide la comuna.",
        "aclaracion_corta": "una ciudad sin comuna está incompleta",
        "citas": ["ciudad/región grande sin comuna"],
    },
    "guatemala": {
        "aclaracion": "Guatemala a secas es ambiguo: pide la zona o el municipio.",
        "aclaracion_corta": "el país a secas es ambiguo",
        "citas": ["a secas es ambiguo", "pide la zona o el municipio"],
    },
    "panama": {
        "aclaracion": ("Panamá a secas es ambiguo: pide el corregimiento o el distrito "
                       "y la referencia."),
        "aclaracion_corta": "el país a secas es ambiguo",
        "citas": ["a secas es ambiguo", "pide el corregimiento o el distrito y la referencia"],
    },
}


def clave(nombre_archivo):
    """costa-rica -> COSTA RICA ; espana -> ESPANA (sin acentos, mayusculas)."""
    s = unicodedata.normalize("NFD", nombre_archivo.replace("-", " "))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper()


def _sin_parentesis(t):
    return re.sub(r"\s*\([^)]*\)", "", t)


def _minusculas_salvo_siglas(t):
    return " ".join(w if (w.strip(".,;:") in SIGLAS) else (w.lower() if w.isupper() else w)
                    for w in t.split(" "))


def campos_desde_estructura(linea):
    """'a + b (c) + d' -> 'a, b (c), d'. Solo se quita un ejemplo FINAL entre parentesis."""
    cuerpo = linea.strip().rstrip(".")
    if cuerpo.endswith(")"):
        cuerpo = re.sub(r"\s*\([^()]*\)$", "", cuerpo)
    partes = [p.strip() for p in cuerpo.split(" + ")]
    return _minusculas_salvo_siglas(", ".join(partes))


def aclaracion_desde_linea(linea):
    t = linea.strip().lstrip("•").strip()
    t = _sin_parentesis(t)
    return t[:1].upper() + t[1:]


def corta_desde_linea(linea):
    t = _sin_parentesis(linea.strip().lstrip("•").strip()).split(":")[0].strip()
    return t[:1].lower() + t[1:]


def leer_pack(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def linea_estructura(texto):
    m = re.search(r"^Bien estructurada[^:\n]*:\s*(.+)$", texto, re.M)
    return m.group(0), m.group(1)


def linea_aclaracion(texto):
    m = re.search(r"^•[^\n]*no es dirección: (?:pide|pedí)[^\n]*$", texto, re.M)
    return m.group(0) if m else None


def derivar(packs):
    salida, avisos = {}, []
    for f in sorted(os.listdir(packs)):
        if not f.endswith(".md") or f == "changelog.md":
            continue
        n = f[:-3]
        k = clave(n)
        if k in A_MANO:
            continue
        texto = leer_pack(os.path.join(packs, f))
        try:
            cita_est, cuerpo = linea_estructura(texto)
        except AttributeError:
            avisos.append(f"{k}: el pack no tiene linea 'Bien estructurada:'; SIN entrada")
            continue
        entrada = {"origen": "derivado mecanicamente del pack", "fuente": f"{n}.md",
                   "cita_estructura": cita_est,
                   "campos_memoria": campos_desde_estructura(cuerpo)}
        if n in PARAFRASEADOS:
            p = PARAFRASEADOS[n]
            faltan = [c for c in p["citas"] if c not in texto]
            if faltan:
                avisos.append(f"{k}: el pack ya no contiene {faltan}; SIN entrada")
                continue
            entrada["origen"] = "parafraseado del pack"
            entrada["citas_pack"] = p["citas"]
            entrada["aclaracion"] = p["aclaracion"]
            entrada["aclaracion_corta"] = p["aclaracion_corta"]
        else:
            lin = linea_aclaracion(texto)
            if not lin:
                avisos.append(f"{k}: sin linea 'no es dirección: pide' ni parafrasis; SIN entrada")
                continue
            entrada["cita_aclaracion"] = lin
            entrada["aclaracion"] = aclaracion_desde_linea(lin)
            entrada["aclaracion_corta"] = corta_desde_linea(lin)
        if len(entrada["aclaracion"]) > TOPE_ACLARACION:
            avisos.append(f"{k}: aclaracion de {len(entrada['aclaracion'])} > {TOPE_ACLARACION}")
        if len(entrada["campos_memoria"]) > TOPE_CAMPOS:
            avisos.append(f"{k}: campos_memoria de {len(entrada['campos_memoria'])} > {TOPE_CAMPOS}")
        salida[k] = entrada
    return salida, avisos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packs", default=PACKS_DEFECTO)
    ap.add_argument("--escribir", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.packs):
        sys.exit(f"ERROR: no existe {a.packs}. La skill golden-chatea-pro-validacion-direcciones "
                 "es la fuente; sin ella no se genera nada.")
    lim = json.load(open(LIMITES, encoding="utf-8"))
    voc = lim["vocabulario_direccion_por_pais"]
    nuevo, avisos = derivar(a.packs)
    for k, (arch, citas, _fuera_del_pack) in A_MANO.items():
        texto = leer_pack(os.path.join(a.packs, arch + ".md"))
        faltan = [c for c in citas if c not in texto]
        if faltan:
            avisos.append(f"{k}: las citas de anclaje {faltan} ya no estan en el pack")
        voc[k]["origen"] = "escrito a mano; anclado al pack"
        voc[k]["fuente"] = f"{arch}.md"
        voc[k]["citas_pack"] = citas
    for k, v in nuevo.items():
        voc[k] = v
    for k, v in sorted(nuevo.items()):
        print(f"  {k:12} campos[{len(v['campos_memoria']):3}] {v['campos_memoria']}")
        print(f"  {'':12} aclar[{len(v['aclaracion']):3}] {v['aclaracion']}")
    total = sum(1 for x in voc if not x.startswith("_"))
    print(f"\n  derivados: {len(nuevo)} · anclados a mano: {len(A_MANO)} · "
          f"total en el mapa: {total} (anclado a {PAISES_ESPERADOS})")
    faltan, sobran = diferencias_de_roster(voc)
    if faltan:
        avisos.append(f"faltan del roster anclado (PAISES_MAPA): {faltan}")
    if sobran:
        avisos.append(f"sobran del roster anclado (PAISES_MAPA), no estaban previstos: {sobran}")
    # Contenido contra el PACK COMPLETO, no solo contra su cita -- de las DOS entradas a mano
    # tambien, que es exactamente donde se colaron los sabotajes del 21-sep.
    avisos += validar_contenido_contra_pack(voc, a.packs, excepciones_desde_a_mano())
    for av in avisos:
        print("  AVISO:", av)
    if a.escribir:
        if avisos:
            sys.exit("NO se escribio: hay avisos arriba. Un pack cambiado se revisa a ojo.")
        with open(LIMITES, "w", encoding="utf-8") as f:
            json.dump(lim, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("  escrito assets/limites.json")


if __name__ == "__main__":
    main()
