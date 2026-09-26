#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida los packs de pais de golden-chatea-pro-validacion-direcciones.

NO comprueba estilo: comprueba lo que ya rompio esta familia de skills.

  1. EL TECHO. El campo 'Prompt de analisis de direccion' corta en 8.000 y NO da error:
     se guarda cortado y el panel se ve normal. Un prompt de validacion cortado valida
     peor y deja pasar direcciones malas.

  2. EL CRITERIO DE CODIGO POSTAL, contra references/limites.json y no contra la prosa.
     Mexico heredo de Colombia un "NUNCA exijas codigo postal" que en Mexico es falso.
     En Europa y Brasil el CP es OBLIGATORIO: clonar Colombia alli rompe 12 paises.

  3. LA SENAL POSITIVA. 'direccion correcta' es senal de MAQUINA: el flujo la lee para
     avanzar. Traducida, o con un emoji pegado delante, puede dejar de casar.

  4. DATOS DE UN NEGOCIO REAL dentro del pack. El repo es PUBLICO y un pack es del PAIS,
     nunca del cliente que lo motivo.

REESCRITO EL 2026-09-08 tras una verificacion adversarial que demostro, con mutaciones,
que tres comprobaciones de la version anterior NO PODIAN FALLAR:
  · la senal se buscaba con `in`, asi que "✅ direccion correcta" pasaba;
  · el criterio de CP se apoyaba en una lista de frases quemadas, y una de sus entradas
    era "pidelo" — tan laxa que Brasil pasaba por ella y no por su frase real; una
    negacion parafraseada ("No lo solicites nunca") no la cazaba nadie;
  · el "control inverso" de --casos era una expresion constante que no ejecutaba nada.
Ahora las comprobaciones son estructurales (frase a frase, no lista de frases) y TODAS
las contrapruebas entran por la puerta principal del comprobador.

Uso:
    python3 validar_pack.py                 # los 23 packs
    python3 validar_pack.py mexico          # uno
    python3 validar_pack.py --autoprueba    # contra casos que se SABEN malos
    python3 validar_pack.py --casos         # banco de direcciones trampa

Salida 0 = en norma. 1 = al menos un fallo.
"""
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(RAIZ, "references")
LIMITES = os.path.join(REFS, "limites.json")

ROJO, VERDE, AMAR, GRIS, FIN = "\033[91m", "\033[92m", "\033[93m", "\033[90m", "\033[0m"


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn").lower()


def cuerpo_entregable(texto):
    """Lo que de verdad se pega en el campo: sin los comentarios HTML de nota interna."""
    return re.sub(r"<!--.*?-->", "", texto, flags=re.S).strip()


def escapado(texto):
    return len(json.dumps(texto, ensure_ascii=True)[1:-1])


# --- 1 · techo ---------------------------------------------------------------

def check_techo(cuerpo, lim):
    fallos, avisos = [], []
    tope, margen = lim["topes"]["campo_nativo"], lim["topes"]["margen_recomendado"]
    n = len(cuerpo)
    if n > tope:
        fallos.append(f"TECHO: {n} caracteres, el campo corta en {tope} (se guarda CORTADO, sin error)")
    elif n > tope - margen:
        avisos.append(f"techo: {n}/{tope}, quedan {tope-n} (bajo el margen de {margen})")
    esc = escapado(cuerpo)
    if esc > lim["topes"]["bot_field_escapado"]:
        fallos.append(f"BOT FIELD: {esc} escapados sobre {lim['topes']['bot_field_escapado']}")
    return fallos, avisos, n, esc


# --- 2 · codigo postal, por ESTRUCTURA y no por lista quemada ----------------

# Como se nombra el codigo postal en cada idioma del arsenal. Es el unico dato de
# vocabulario que queda, y es cerrado: lo dice limites.json con el idioma del pack.
TOKENS_CP = ["codigo postal", "cod. postal", "cp", "cep", "zip",
             "kod pocztowy", "iranyitoszam", "psc", "postanski broj", "postna stevilka",
             "cod postal", "tachydromiko", "poshtenski", "postal code"]

OBLIGA = ["requerido", "obligatorio", "es necesario", "hace falta", "sin el no", "sin ella no",
          "sin cep no", "pidelo", "pide el", "pidela", "solicitalo", "debe traer", "siempre con",
          "no hay envio", "no rutea", "no hay ruteo", "no roteia"]
NIEGA = ["nunca pid", "no pidas", "no se pide", "no pedir", "no lo pidas", "no lo solicites",
         "no hace falta", "no se usa", "no la pidas", "jamas pid", "no exijas", "sin pedir",
         "opcional", "puede omitirse", "puedes omitirlo", "no es obligatorio", "no es necesario",
         "es opcional", "omitirlo", "dar la direccion por buena sin"]
# 🔴 Esta lista es VOCABULARIO CERRADO y lo sigue siendo aunque decida por ventana de proximidad
# en vez de por frase entera (ver VENTANA arriba). Una verificacion adversarial (2026-09-22)
# inyecto en espana.md una frase real de negocio ("el codigo postal es OPCIONAL en Espana...
# puedes OMITIRLO") y el validador dio "sano": ni "opcional" ni "omitir" estaban aqui. Anadidas
# esas formas, pero el problema de fondo no se cierra por completo con keywords: cualquier
# parafraseo nuevo que no estipule NIEGA sigue colandose. Este chequeo reduce el riesgo, no lo
# elimina — no declarar "el criterio de CP esta blindado" sin decir esto.


# 🔴 Historial de esta funcion, dos bugs opuestos ya medidos:
#   v2.9  · frase ENTERA: "NO pidas de mas: ... y el codigo postal, es valida" cazaba una
#           negacion que no lo era -> 11 falsos positivos de 11.
#   v2.9b · ventana FIJA de 45 caracteres: la corrigio, pero un bullet corto seguido de otro
#           bullet que empieza con una frase generica de "no pidas de mas" (la tienen los
#           23 packs, es la validacion avanzada de complemento) cae dentro de los 45
#           caracteres del bullet ANTERIOR si ese bullet termina justo en el token del CP
#           -> 13 falsos positivos de 23 (verificacion adversarial 2026-09-22, Argentina y
#           otros 12 packs cortos).
# Ahora la ventana es la ORACION/VIÑETA que contiene el token, delimitada por el punto o el
# salto de linea mas cercano a cada lado — no un numero de caracteres. Une los dos bugs: no
# cruza a la vineta siguiente (arregla v2.9b) y sigue sin depender de que la negacion este
# pegada letra a letra al token (arregla v2.9).
# NOTA: "no pidas" es ambiguo. Los 23 packs comparten la frase "NO pidas de mas: si ya trae ... y el codigo postal, es valida" (no repetir un dato que YA esta) en la MISMA oracion/vineta que menciona el codigo postal como uno de varios items de una lista -- no es una negacion del requisito. Verificacion adversarial 2026-09-22: 12 de 23 packs (los REQUERIDO) daban FALLO por esto tras pasar a ventana por oracion. Costa Rica en cambio SI usa "no pidas" como negacion real ("no pidas calle, numero ni codigo postal"), asi que la palabra no se puede quitar de NIEGA sin perder ese caso: se excluye especificamente el modismo "de mas", no la palabra.
def _niega_real(ventana):
    limpia = ventana.replace("no pidas de mas", "")
    return any(m in limpia for m in NIEGA)


def _ventanas_cp(plano):
    """Oracion o vineta que contiene cada mencion del codigo postal, acotada por '.' o salto
    de linea. La decision se toma por la frase que SI habla del CP, nunca por una vecina."""
    out = []
    for tk in TOKENS_CP:
        for m in re.finditer(rf"\b{re.escape(tk)}\b", plano):
            ini = max(plano.rfind(".", 0, m.start()), plano.rfind("\n", 0, m.start()))
            fin_punto = plano.find(".", m.end())
            fin_salto = plano.find("\n", m.end())
            candidatos = [f for f in (fin_punto, fin_salto) if f != -1]
            fin = min(candidatos) if candidatos else len(plano)
            out.append(plano[ini + 1: fin + 1])
    return out


def check_codigo_postal(cuerpo, datos, pais):
    """Decide por lo que se dice JUNTO al codigo postal, no por listas de frases exactas."""
    fallos = []
    plano = sin_acentos(cuerpo)
    obliga = niega = False
    for f in _ventanas_cp(plano):
        # La negacion se mira PRIMERO y excluye: "no hace falta" contiene "hace falta",
        # que esta en OBLIGA. Con dos `if` la ventana marcaba las dos cosas, se anulaban
        # entre si y una negacion parafraseada pasaba sin que nadie la viera.
        if _niega_real(f):
            niega = True
        elif any(m in f for m in OBLIGA):
            obliga = True

    # 🔴 SIN mutua exclusion: antes, si el pack tenia AMBAS senales (la genuina y una inyectada
    # o contradictoria), "niega and not obliga" daba False y "not obliga" tambien, y el fallo
    # NUNCA se disparaba — la contradiccion se cancelaba sola en silencio. Verificacion
    # adversarial (2026-09-22): inyecte "el CP es OPCIONAL, puedes omitirlo" en espana.md, que YA
    # tenia su frase correcta de "REQUERIDO", y el resultado seguia siendo "sano". Ahora CUALQUIER
    # senal en la direccion equivocada es fallo por si sola, tenga o no compania la correcta: un
    # pack de un pais REQUERIDO no puede contener NINGUNA ventana que niegue, y viceversa.
    if datos["cp_requerido"]:
        if niega:
            fallos.append(f"CODIGO POSTAL: el pack contiene una frase que NIEGA el CP y en "
                          f"{datos['nombre']} es REQUERIDO ({datos['cp_formato']}). Aunque el pack "
                          f"tambien lo exija en otro sitio, la contradiccion queda dentro del texto "
                          f"que se pega — el modelo puede leer cualquiera de las dos.")
        elif not obliga:
            fallos.append(f"CODIGO POSTAL: en {datos['nombre']} es REQUERIDO ({datos['cp_formato']}) "
                          f"y ninguna frase del pack lo exige.")
    else:
        if obliga:
            fallos.append(f"CODIGO POSTAL: el pack contiene una frase que EXIGE el CP y en "
                          f"{datos['nombre']} no se usa en ultima milla. Aunque el pack tambien lo "
                          f"niegue en otro sitio, pedirlo de mas frena pedidos buenos.")
        elif not niega:
            fallos.append(f"CODIGO POSTAL: en {datos['nombre']} NO se pide y el pack no lo dice en "
                          f"ninguna frase. Sin decirlo, el modelo lo pedira por analogia.")
    return fallos


# --- 3 · la senal positiva, LIMPIA -------------------------------------------

def check_contrato(cuerpo, lim, datos):
    """La senal tiene que estar y tiene que estar SOLA: un emoji pegado delante puede
    romper el match del flujo. Se comprueba la linea, no la subcadena."""
    fallos, avisos = [], []
    senal = lim["contrato_salida"]["senal_positiva_literal"]
    if senal not in cuerpo:
        fallos.append(f"CONTRATO: falta la senal positiva literal '{senal}'. Es senal de MAQUINA.")
        return fallos, avisos

    # SOLO emoji pictografico pegado a la senal. La flecha "→" de "llegar sin llamar →
    # direccion correcta" es estructura del documento, no contaminacion: contarla daba 23
    # falsos positivos de 23. Lo que rompe el match es un ✅ o un ⚠️ delante.
    def es_pictografico(c):
        o = ord(c)
        return (0x1F300 <= o <= 0x1FAFF or o in (0x2705, 0x274C, 0x2757, 0x2B55)
                or 0x26A0 <= o <= 0x26FF or 0x2B00 <= o <= 0x2BFF and o != 0x2B95)
    sucias = re.findall(rf"(\S{{1,3}})[  ]{{0,2}}{re.escape(senal)}", cuerpo)
    malas = [s for s in sucias if any(es_pictografico(c) for c in s)]
    if malas:
        fallos.append(f"CONTRATO: la senal lleva un simbolo pegado delante ({' '.join(sorted(set(malas)))}). "
                      f"'{senal}' es senal de MAQUINA y va sola: un emoji puede romper el match del flujo.")

    if datos["idioma"] != "es":
        plano = sin_acentos(cuerpo)
        if not any(m in plano for m in ("no se traduce", "senal interna", "no traducir", "sin traducir")):
            avisos.append(f"contrato: pack en '{datos['idioma']}' que no avisa de que la senal NO se traduce; "
                          f"la siguiente mano que lo edite la traducira.")
    return fallos, avisos


# --- 4 · higiene: esto SI puede tumbar la corrida ----------------------------

SECRETOS = [
    (r"sk[-_](live|test|proj|ant)[-_][A-Za-z0-9_\-]{6,}", "clave tipo sk_live_/sk-proj-"),
    (r"\bsk-[A-Za-z0-9]{20,}", "clave tipo sk-"),
    (r"shpat_[A-Za-z0-9]{8,}", "token Shopify"),
    (r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
    (r"\+\d{1,3}[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{3,4}\b", "telefono con prefijo"),
    # 🔴 telefono SIN '+': un movil colombiano "3105551234" (10 digitos, empieza en 3) no llevaba
    # prefijo y el patron de arriba no lo cazaba. Verificacion adversarial 2026-09-22: inyecte
    # "Telefono de la bodega: 3105551234" en un pack real y paso con exit 0. Con \d{10} se
    # corre el riesgo de casar un CEP brasileno sin guion o un CP argentino largo por accidente;
    # se acota a que EMPIECE por 2-9 (los moviles LatAm no empiezan en 0 o 1) y no vaya pegado a
    # mas digitos ni a un guion (para no comerse "70862-020" ni "011853" partido).
    (r"(?<![\d-])[2-9]\d{9}(?![\d-])", "posible telefono local sin prefijo"),
    (r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", "correo"),
    # 🔴 frases de negocio en prosa libre, sin nombre propio de transportadora: la version
    # anterior solo cazaba nombres de courier conocidos (lista cerrada) y una lista de negocio
    # generica ("Transportadoras habilitadas de este negocio: ..., PROHIBIDA: ...") no llevaba
    # ningun nombre de la lista y pasaba. Esto es heuristico por FRASE, no por nombre.
    (r"de este negocio\b", "frase de negocio de este negocio fuera de un bloque PENDIENTE"),
    (r"tel[eé]fono de la (bodega|tienda|negocio)", "telefono operativo del negocio en prosa"),
]


def check_higiene(cuerpo):
    """FALLA, no avisa. El repo de skills es PUBLICO. La version anterior solo avisaba y
    ademas su patron no cazaba los formatos reales de clave: una clave sk_live_ metida a
    proposito en un pack pasaba la corrida entera con exit 0."""
    fallos, avisos = [], []
    for patron, que in SECRETOS:
        m = re.search(patron, cuerpo)
        if m:
            fallos.append(f"HIGIENE: {que} DENTRO del pack ({m.group(0)[:14]}…). El repo es PUBLICO.")
    # El [PENDIENTE] NO es aviso: es el diseno del pack (el hueco de transportadoras que
    # llena el negocio). Cuando lo era, 23 de 23 packs salian en amarillo, y un estado que
    # siempre sale amarillo deja de leerse y tapa los avisos que si importan.
    return fallos, avisos


# --- recorrido ---------------------------------------------------------------

def validar_uno(datos, lim):
    ruta = os.path.join(REFS, datos["pack"])
    if not os.path.exists(ruta):
        return None, [f"pack declarado en limites.json pero AUSENTE en disco: {datos['pack']}"], []
    cuerpo = cuerpo_entregable(open(ruta, encoding="utf-8").read())
    return evaluar(cuerpo, datos, lim)


def evaluar(cuerpo, datos, lim):
    """La puerta principal. Todo lo que comprueba esta herramienta pasa por aqui, y por
    aqui entran tambien sus contrapruebas: un comprobador que se prueba por un atajo se
    prueba a si mismo, no a lo que hace."""
    fallos, avisos, n, esc = check_techo(cuerpo, lim)
    fallos += check_codigo_postal(cuerpo, datos, datos["nombre"])
    f2, a2 = check_contrato(cuerpo, lim, datos)
    f3, a3 = check_higiene(cuerpo)
    return (n, esc), fallos + f2 + f3, avisos + a2 + a3


def main(argv):
    lim = json.load(open(LIMITES, encoding="utf-8"))
    paises = lim["paises"]
    filtro = [a for a in argv if not a.startswith("-")]
    objetivo = {k: v for k, v in paises.items()
                if not filtro or any(sin_acentos(f) in sin_acentos(k) or
                                     sin_acentos(f) in sin_acentos(v["pack"]) for f in filtro)}
    if not objetivo:
        print(f"{ROJO}Ningun pais casa con {filtro}{FIN}")
        return 1

    print(f"UNIVERSO declarado en limites.json: {len(paises)} paises · REVISADOS: {len(objetivo)}")
    print(f"TOPE del campo: {lim['topes']['campo_nativo']} · margen sano: {lim['topes']['margen_recomendado']}")
    print("-" * 78)
    print(f"{'PAIS':<14}{'CRUDO':>7}{'/8000':>7}{'ESCAP':>8}  {'CP':<10}{'HUECO':<7}ESTADO")
    print("-" * 78)

    sanos = con_aviso = con_fallo = ausentes = 0
    detalle = []
    for pais, datos in sorted(objetivo.items()):
        med, fallos, avisos = validar_uno(datos, lim)
        cp = "REQUERIDO" if datos["cp_requerido"] else "no se pide"
        if med is None:
            ausentes += 1
            print(f"{pais:<14}{'-':>7}{'-':>7}{'-':>8}  {cp:<10}{ROJO}AUSENTE{FIN}")
            detalle.append((pais, fallos, avisos)); continue
        n, esc = med
        estado = (f"{ROJO}FALLO{FIN}" if fallos else f"{AMAR}aviso{FIN}" if avisos else f"{VERDE}sano{FIN}")
        if fallos: con_fallo += 1
        elif avisos: con_aviso += 1
        else: sanos += 1
        hueco = "si" if "[PENDIENTE" in cuerpo_entregable(
            open(os.path.join(REFS, datos["pack"]), encoding="utf-8").read()) else "-"
        print(f"{pais:<14}{n:>7}{100*n/lim['topes']['campo_nativo']:>6.0f}%{esc:>8}  {cp:<10}{hueco:<7}{estado}")
        if fallos or avisos:
            detalle.append((pais, fallos, avisos))

    if detalle:
        print("\n" + "=" * 78)
        for pais, fallos, avisos in detalle:
            print(f"\n{pais}")
            for f in fallos: print(f"  {ROJO}FALLO{FIN}  {f}")
            for a in avisos: print(f"  {AMAR}aviso{FIN}  {a}")

    print("\n" + "=" * 78)
    print(f"COBERTURA: {len(objetivo)} de {len(paises)} revisados · sanos {sanos} · "
          f"con aviso {con_aviso} · CON FALLO {con_fallo} · ausentes {ausentes}")
    return 1 if (con_fallo or ausentes) else 0


# --- autoprueba: TODA entra por evaluar() ------------------------------------

def autoprueba():
    lim = json.load(open(LIMITES, encoding="utf-8"))
    P = lim["paises"]
    BASE_OK = ("dirección correcta\nEn México el CÓDIGO POSTAL es REQUERIDO: define la zona de "
               "reparto. Si la dirección no trae CP, pídelo (5 dígitos).")
    casos = [
        ("CP negado donde es REQUERIDO (el defecto de Mexico y el de Europa entera)",
         "dirección correcta\nNUNCA pides código postal.", P["MEXICO"], "codigo postal"),
        ("CP negado con OTRAS PALABRAS (parafraseo que la lista quemada no cazaba)",
         "dirección correcta\nNo hace falta el código postal. No lo solicites nunca.",
         P["POLONIA"], "codigo postal"),
        ("CP exigido donde no se usa (frena pedidos buenos)",
         "dirección correcta\nEl código postal es obligatorio, pídelo siempre.",
         P["COLOMBIA"], "codigo postal"),
        ("pack que NO dice nada del CP donde es requerido",
         "dirección correcta\nPide la calle y el número.", P["ESPANA"], "codigo postal"),
        ("senal positiva traducida (el flujo no la reconoce)",
         "endereço correto\nO CEP é obrigatório, peça sempre.", P["BRASIL"], "contrato"),
        ("senal positiva con EMOJI pegado (pasaba con la comprobacion por subcadena)",
         "• Entregable → escribe literal: ✅ dirección correcta\nEl CP es requerido, pídelo.",
         P["MEXICO"], "contrato"),
        ("prompt por encima de 8.000 (se guarda cortado, sin error)",
         BASE_OK + "\n" + "x" * 8100, P["MEXICO"], "techo"),
        ("clave sk_live_ dentro del pack (el repo es PUBLICO)",
         BASE_OK + "\nclave: sk_live_9f3aBcD8xKq2mNp7", P["MEXICO"], "higiene"),
        ("correo dentro del pack",
         BASE_OK + "\nescribe a soporte@undominio.com", P["MEXICO"], "higiene"),
    ]
    print("AUTOPRUEBA · casos que se SABEN malos. Cada uno DEBE fallar, y por evaluar().")
    print("-" * 78)
    ok = 0
    for nombre, cuerpo, datos, espera in casos:
        _, fallos, _ = evaluar(cuerpo, datos, lim)
        if any(espera in sin_acentos(f) for f in fallos):
            ok += 1; print(f"  {VERDE}cazado{FIN}   {nombre}")
        else:
            print(f"  {ROJO}NO CAZADO{FIN}  {nombre}\n           devolvio: {fallos}")

    _, f, _ = evaluar(BASE_OK, P["MEXICO"], lim)
    if not f:
        ok += 1; print(f"  {VERDE}limpio{FIN}   control: un pack correcto NO da falso positivo")
    else:
        print(f"  {ROJO}FALSO POSITIVO{FIN} el control correcto dio: {f}")

    total = len(casos) + 1
    print("-" * 78)
    print(f"AUTOPRUEBA: {ok} de {total}")
    if ok != total:
        print(f"{ROJO}El validador no caza lo que dice cazar. Sus 'sano' no valen.{FIN}")
    return 0 if ok == total else 1


# --- banco de casos trampa ---------------------------------------------------

def _huecos_de(plano, lista):
    """Puerta principal del banco. La contraprueba entra por aqui, no por un atajo."""
    out = []
    for c in lista:
        falta = [m for m in c["marcas"] if sin_acentos(m) not in plano]
        if falta:
            out.append((c["entrada"], c["esperado"], falta))
    return out


def casos():
    lim = json.load(open(LIMITES, encoding="utf-8"))
    banco = json.load(open(os.path.join(REFS, "casos.json"), encoding="utf-8"))["casos"]
    por_pais = {}
    for c in banco:
        por_pais.setdefault(c["pais"], []).append(c)

    print("BANCO DE CASOS TRAMPA · la regla tiene que estar ESCRITA en el pack")
    print("-" * 78)
    cubiertos, huecos = 0, []
    planos = {}
    for pais in sorted(por_pais):
        datos = lim["paises"].get(pais)
        f = os.path.join(REFS, datos["pack"]) if datos else None
        if not f or not os.path.exists(f):
            for c in por_pais[pais]:
                huecos.append((pais, c["entrada"], "pack ausente"))
            continue
        plano = sin_acentos(cuerpo_entregable(open(f, encoding="utf-8").read()))
        planos[pais] = plano
        hs = _huecos_de(plano, por_pais[pais])
        cubiertos += len(por_pais[pais]) - len(hs)
        for entrada, esperado, falta in hs:
            huecos.append((pais, entrada, f"sin la regla: {esperado} (marca {falta})"))

    for pais, entrada, motivo in huecos:
        print(f"  {ROJO}HUECO{FIN}  {pais} · \"{entrada}\" · {motivo}")
    if not huecos:
        print(f"  {VERDE}todos los casos tienen su regla escrita en el pack{FIN}")
    print("-" * 78)
    print(f"COBERTURA DE CASOS: {cubiertos} de {len(banco)} · huecos {len(huecos)}")

    # CONTRAPRUEBA REAL: se le quita la regla a un pack de verdad, en memoria, y se vuelve
    # a entrar por _huecos_de. La version anterior comparaba una constante y no ejecutaba
    # nada: el comprobador se aprobaba a si mismo.
    print("\nCONTRAPRUEBA (mutacion en memoria, por la puerta principal):")
    fallos_cp = 0
    for pais, lista in sorted(por_pais.items()):
        if pais not in planos or not lista:
            continue
        marca = lista[0]["marcas"][0]
        mutado = planos[pais].replace(sin_acentos(marca), "")
        if _huecos_de(mutado, [lista[0]]):
            print(f"  {VERDE}ok{FIN}      {pais}: quitada la regla \"{marca}\", el banco lo caza")
        else:
            print(f"  {ROJO}ROTO{FIN}    {pais}: quitada la regla \"{marca}\" y sigue diciendo que esta")
            fallos_cp += 1
        break  # una basta para demostrar que el mecanismo corre; se rota cambiando el orden
    return 1 if (huecos or fallos_cp) else 0


if __name__ == "__main__":
    if "--autoprueba" in sys.argv:
        sys.exit(autoprueba())
    if "--casos" in sys.argv:
        sys.exit(casos())
    sys.exit(main(sys.argv[1:]))
