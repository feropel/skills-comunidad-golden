#!/usr/bin/env python3
"""Lo que TODOS los generadores usan. UNA copia, importada.

POR QUE EXISTE, y la historia es la mejor prueba de que hacia falta:

Este expediente lleva tres rondas arreglando el mismo fallo — un telefono pintado como
"57" pelado cuando la persona no tiene telefono (llega por comentario de Facebook, no
por WhatsApp). Ronda 12: se arreglo en la tabla estrella. Ronda 13: se arreglo en las
otras tres... y quedaron OCHO sitios mas vivos, porque existia una SEGUNDA funcion
(`tel_de`) con el bug original. Y la funcion "unica" `contacto_de` estaba duplicada
byte a byte en los dos generadores, mientras `tel10` vivia en TRES copias.

LA CLASE: **la duplicacion no es un problema de estilo, es un problema de VERDAD**. Dos
copias de una funcion no son una funcion escrita dos veces: son dos funciones que hoy
coinciden y que en la primera correccion dejan de coincidir — y la que no se toca no
avisa. Por eso `denominador.py` existe (la regla de negocio) y por eso existe este
modulo (las funciones de pintar). Un arreglo aplicado a "la familia" solo vale si la
familia esta ENUMERADA en un sitio; si hay que acordarse de los miembros, se olvida uno.

COMO SE COMPRUEBA QUE NO VOLVIO: `prueba_escritura.py` corre un grep sobre los scripts y
exige CERO definiciones locales de estas funciones fuera de aqui. La regla que no se
puede comprobar sola se rompe sin ruido.

  from comun import contacto_de, tel10, miles, pesos, nom_de, huella_txt
"""
import os, re


def tel10(x):
    """Los ultimos 10 digitos. Colombia manda el mismo numero con y sin el 57 delante.

    Devuelve "" cuando no hay nada utilizable, y ese "" SIGNIFICA "sin telefono" — no
    es un fallo silencioso: quien lo recibe tiene que decidir que hacer con el, y en
    esta skill la decision es "esto no es WhatsApp, es un comentario publico".
    """
    return re.sub(r"\D", "", x or "")[-10:]


def contacto_de(e):
    """Como se contacta a esta persona. UNA definicion para TODAS las tablas.

    NORMALIZA, NO PREFIJA. Las dos familias traen el telefono en formatos distintos: el
    analisis lo da sin indicativo ("3000000001") y las decisiones ya lo dan con el
    ("573000000001"). Pegar "57" delante sin mirar producia "5757...". Se reduce a
    digitos, se toman los ultimos 10 y se pone UN indicativo.

    Acepta tanto un dict con "tel" como uno con "phone": las dos familias los nombran
    distinto y hacer que el llamador se acuerde de cual es cual es pedir el mismo fallo.
    """
    d = tel10(e.get("tel") or e.get("phone") or "")
    if not d:
        return "**comentario publico** · sin telefono"
    # SE IMPRIME SIN EL 57. Dictado por FER el 2026-08-14: «los telefonos SIN el 57 —
    # eso no me deja encontrar a las personas». El indicativo rompe la busqueda en el
    # panel de Dropi, o sea que el numero impreso **no sirve para lo unico que se hace
    # con el**: pegarlo en el buscador. Un identificador que no se puede buscar no
    # identifica.
    #
    # UN DATO, DOS REPRESENTACIONES, y hay que decirlo porque parece incoherencia:
    # por dentro se sigue guardando y cruzando con 57+10 (asi lo emite el motor y asi
    # casan las dos familias de insumos); lo que cambia es **lo que se imprime**. La
    # conversion vive aqui, en el unico sitio que pinta telefonos.
    return d


def miles(x):
    """Los dos informes escriben los numeros igual.

    El 360 ponia 3.416 y el corto 3416: el mismo dato con dos grafias en dos PDF del
    mismo dia se lee como dos datos distintos.
    """
    return f"{int(x):,}".replace(",", ".")


def miles_seguro(x):
    """`miles()` cuando se puede, el valor tal cual cuando no. Para buscar en el texto."""
    try:
        return miles(x)
    except (TypeError, ValueError):
        return str(x)


def pesos(x):
    return f"${float(x or 0):,.0f}".replace(",", ".")


def nom_de(o):
    return f"{o.get('name','')} {o.get('surname','')}".strip()


def huella_base(ordenes):
    """La huella de cada cliente calculada DE LA PROPIA BASE, agrupando por telefono.

    POR QUE EXISTE, y es una degradacion silenciosa medida el 2026-08-17: el volcado
    oficial de la API **no trae el campo `huellas`** (lo llenaba el cosechador de
    navegador con la huella de Dropi, y CONFIO no entrega `client_total_orders`).
    Con ese volcado, `huella_txt` respondia **«sin historial» al 100% de los pedidos**
    — 400 de 400 en la muestra — mientras la base tenia **2.637 telefonos con pedidos
    cerrados**. La regla de FER «si devuelve mucho, no sale sin anticipo» quedaba
    muerta, y muerta en silencio: «sin historial» es una respuesta plausible, no un
    error, asi que nadie la mira dos veces.

    LA MISMA CLASE OTRA VEZ: un campo opcional que al faltar degrada a una respuesta
    creible en lugar de decir «no pude mirar». Es la tercera de la semana.

    Dictado de FER (2026-08-14): la huella se calcula de la propia base — agrupar por
    telefono, entregadas contra devueltas **sobre los cerrados**. Un pedido en transito
    no fracaso todavia; contarlo como fallo pinta de rojo a quien apenas empieza.
    """
    ent = {"ENTREGADO"}
    dev = {"DEVOLUCION", "DEVOLUCION EN BODEGA", "EN PROCESO DE DEVOLUCION",
           "TRANSITO A DEVOLUCION PROVEEDOR"}
    idx = {}
    for o in ordenes or []:
        t = tel10(o.get("phone"))
        if not t:
            continue
        est = str(o.get("status") or "").upper().strip()
        if est in ent:
            idx.setdefault(t, {"ent": 0, "dev": 0})["ent"] += 1
        elif est in dev:
            idx.setdefault(t, {"ent": 0, "dev": 0})["dev"] += 1
    for v in idx.values():
        v["n"] = v["ent"] + v["dev"]
        v["pct"] = round(100 * v["ent"] / v["n"], 1) if v["n"] else None
    return idx


def huella_txt(D, o):
    """El denominador son los pedidos CERRADOS, nunca el total.

    Un pedido en transito todavia no fracaso. Contarlo como fracaso pinta de rojo a
    quien apenas empieza — es exactamente el bug del "% de Entrega" de Chatea, que
    cuenta el transito como fallo y hace ver malos a clientes que no lo son.
    """
    t = tel10(o.get("phone"))
    h = (D.get("huellas") or {}).get(t)
    if not (h and h.get("found")):
        # SIN HUELLA DE DROPI SE CALCULA DE LA BASE, y se dice de donde sale.
        # Antes esto devolvia «sin historial» y punto — con el volcado oficial, que no
        # trae `huellas`, eso era el 100% de los pedidos. «Sin historial» y «no pude
        # mirar» no son lo mismo, y aqui se estaba imprimiendo el primero cuando la
        # verdad era el segundo.
        if "_huella_base" not in D:
            D["_huella_base"] = huella_base(D.get("ordenes") or [])
        b = D["_huella_base"].get(t)
        if not b or not b["n"]:
            return "sin cerrados en esta cuenta"
        return (f"devuelve {100 * b['dev'] / b['n']:.0f}% de {b['n']} cerrados "
                "(calculado de esta cuenta)")
    lt = h["global_profile"]["lifetime_totals"]
    ent, dev = lt["delivered"], lt["returned"]
    cerradas = ent + dev
    transito = lt["orders"] - cerradas
    if cerradas == 0:
        return "primera compra" if not lt["orders"] else f"{transito} en camino, ninguno cerrado"
    txt = f"devuelve {100 * dev / cerradas:.0f}% de {cerradas} cerrados"
    return txt + (f", {transito} en camino" if transito else "")


def concuerda(n, singular, plural):
    """«1 fila no tiene» / «3 filas no tienen». La concordancia, como clase.

    Se arreglo una frase a mano y quedaron las demas. Una funcion no se olvida de
    ninguna.
    """
    return f"{miles(n)} {singular if n == 1 else plural}"


# ------------------------------------------------------------------------------
# LA POLITICA DEL PDF, UNA SOLA, PARA LOS DOS GENERADORES.
# Estaban en contradiccion: el informe corto se NEGABA si el archivo existia, y el 360
# ARCHIVABA lo que hubiera — incluido un PDF de otro chat. Y el comentario del 360 decia,
# literalmente, "lo ajeno no se pisa nunca" mientras el codigo movia lo ajeno. Un
# comentario correcto encima de un codigo que hace lo contrario es peor que no tenerlo:
# quien lo lee deja de mirar.
#
# COMO SE DISTINGUE LO PROPIO DE LO AJENO SIN ADIVINAR: cuando esta skill escribe un PDF
# deja al lado una marca (un archivo oculto con su nombre). Si la marca esta, el PDF es
# suyo y se archiva; si no esta, es de otro y NO SE TOCA. Sin marca no se supone nada.
MARCA_SUFIJO = ".golden-logistica"


def _marca_de(ruta_pdf):
    d, n = os.path.split(os.path.abspath(ruta_pdf))
    return os.path.join(d, "." + n + MARCA_SUFIJO)


def marcar_como_propio(ruta_pdf):
    """Deja la senal de autoria al lado del PDF. Se llama DESPUES de escribirlo.

    Aqui SI se usa `open` directo, y va explicado porque el banco lo cuenta: esto no
    lee ni produce un entregable, escribe una marca de control de tres lineas que se
    puede perder sin consecuencia. Pasarla por `escribir_texto` la apuntaria como
    insumo y ensuciaria el registro de la corrida con archivos que no son datos.
    """
    try:
        with open(_marca_de(ruta_pdf), "w", encoding="utf-8") as f:   # noqa: marca de control
            f.write("Lo escribio la skill golden-logistica-diaria. Si borras este archivo, "
                    "el PDF de al lado pasa a tratarse como AJENO y no se sobrescribira.\n")
    except OSError:
        pass          # no poder marcar no justifica no entregar el informe


def preparar_destino_pdf(ruta_pdf, carpeta_archivo):
    """Deja el sitio libre para escribir, sin destruir nada de nadie.

    Devuelve (se_puede, mensaje). Propio -> se archiva y se puede. Ajeno -> NO.
    """
    if not os.path.exists(ruta_pdf):
        return True, ""
    if not os.path.exists(_marca_de(ruta_pdf)):
        return False, (f"YA HAY UN PDF AHI Y NO LO ESCRIBIO ESTA SKILL: {ruta_pdf}\n"
                       "  No se archiva ni se sobrescribe un entregable ajeno: puede ser "
                       "el informe que otro chat dejo para hoy.\n"
                       "  Ya paso una vez. Elige otra ruta, o borra ese archivo a mano si "
                       "de verdad sobra.")
    import datetime as _dt, shutil
    os.makedirs(carpeta_archivo, exist_ok=True)
    base = os.path.basename(ruta_pdf).rsplit(".", 1)[0]
    fecha = _dt.datetime.fromtimestamp(os.path.getmtime(ruta_pdf)).strftime("%Y-%m-%d")
    destino = os.path.join(carpeta_archivo, f"{base}-{fecha}.pdf")
    n = 2
    while os.path.exists(destino):
        destino = os.path.join(carpeta_archivo, f"{base}-{fecha}-{n}.pdf")
        n += 1
    shutil.move(ruta_pdf, destino)
    try:
        os.unlink(_marca_de(ruta_pdf))
    except OSError:
        pass
    return True, f"  el informe anterior (propio) se archivo en {destino}"


# LAS CLAVES QUE ESTA SKILL ENTIENDE. UNA lista, porque el config es UNO.
# La primera version puso la lista dentro de cada generador y el aviso empezo a marcar
# como desconocidas las claves que lee el MOTOR (`mala_huella`, `ventaja_minima`...).
# Un aviso que grita en falso se ignora a los dos dias, y entonces ya no avisa de nada.
BANDERAS_CONOCIDAS = {
    # identidad y rutas
    "tienda", "dropi", "salida", "nombre_informe", "shop_id", "user_id", "flow_ns",
    # estados y seleccion
    "estados", "estados_accionables", "operativas", "origen", "oficina_solo",
    # economia y decision
    "margen", "factor_tienda", "apretado", "ventaja_minima", "mala_huella", "min_huella",
    "min_envios_muni", "min_cuota_muni",
    # fuentes de datos
    "torre", "retorno", "calibracion", "fletes", "huellas",
    # banderas de operacion
    "aceptar_cosecha_incompleta", "opciones_no_producto",
    # `pisar_pdf` ESTUVO AQUI SIN QUE NADIE LA LEYERA: documentada, listada como
    # conocida... y sin efecto. Es el caso exacto que `avisar_banderas` combate, y la
    # propia lista la eximia del aviso. Una lista de "claves validas" que incluye una
    # clave muerta convierte la compuerta en su contrario: certifica lo que no existe.
    # Se saca. Si alguien la pone, ahora SI se avisa de que no hace nada.
}


def avisar_banderas(cfg, ruta):
    """Nombra las claves que la skill no conoce. No mata: avisa.

    Una bandera mal escrita no hace nada y NO AVISA. El config de produccion llevaba
    `aceptar_cosecha_parcial` cuando el codigo lee `aceptar_cosecha_incompleta`: el
    dueño creia haber configurado algo que nunca estuvo configurado. Un config que
    acepta cualquier cosa en silencio miente sobre lo que esta puesto.
    """
    raras = sorted(k for k in cfg if not k.startswith("_") and k not in BANDERAS_CONOCIDAS)
    if raras:
        import sys as _s
        print(f"AVISO · {os.path.basename(ruta)} tiene claves que esta skill NO LEE: "
              + ", ".join(raras) + ". Si esperabas que hicieran algo, estan mal escritas.",
              file=_s.stderr)


# ------------------------------------------------------------------------------
# AQUI VIVIO `tabla()`, UN PARTIDOR DE TABLAS, Y DURO UNA RONDA.
#
# Lo escribi porque el PDF salio REQUIERE ARREGLO al incrustar las acciones, y razone
# que una tabla de 18 filas es un bloque atomico que no cabe. Lo puse, el PDF paso, y
# di la causa por probada. **El PDF paso porque el contenido cambio y la paginacion se
# corrio, no por el mecanismo que yo describi.**
#
# MEDIDO EL 2026-08-11 contra el `golden-pdf-check` de HOY: una tabla de 40 filas SIN
# partir da APROBADO en 2 paginas. `build_pdf` ya repite la cabecera al cortar y el
# auditor solo marca bloques monoespaciados. Retirado el partidor, los dos informes
# siguen dando APROBADO. La premisa era falsa.
#
# LA CLASE: **una justificacion escrita contra un sistema que ya cambio es una
# justificacion falsa que se lee como cierta.** El sintoma desaparecio, asi que nadie
# vuelve a mirar — y queda codigo cuyo comentario explica un mecanismo que no existe.
# De ahi la regla nueva: **toda afirmacion sobre un sistema EXTERNO lleva la fecha en
# que se midio**, igual que los pendientes. Sin fecha no se sabe si sigue siendo cierta.
#
# Y la segunda mitad, que es la que duele: el sintoma se fue y yo lo conte como arreglo.
# Que el problema desaparezca no prueba que la causa fuera la que uno dijo.
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# CIRUGIA EN EL AIRE · un matcher que no coincide NO es "nada que hacer".
#
# EL CASO: un `re.sub` que quitaba una seccion duplicada del ensamble buscaba el titulo
# "Los que decides tu" y el titulo REAL era "🟡 Decides tu · 1". No coincidia con nada,
# devolvia el texto intacto — 9.597 caracteres antes y despues — y **yo reporte la
# seccion como eliminada**. El codigo no fallo: hizo exactamente lo que se le pidio, que
# era nada. Y "nada" y "lo que yo creia" se ven igual cuando no se cuenta.
#
# LA CLASE: **toda cirugia sobre texto asevera que encontro su objetivo.** Sustituir,
# borrar o recortar sin comprobar el numero de coincidencias es operar con los ojos
# cerrados y salir diciendo que sali bien. Vale para `re.sub`, para `replace` y para
# cualquier busqueda de la que dependa una afirmacion posterior.
def sustituir_exigiendo(patron, reemplazo, texto, que, flags=0, minimo=1):
    """`re.sub` que MUERE si no coincidio lo que se esperaba."""
    import re as _re
    nuevo, n = _re.subn(patron, reemplazo, texto, flags=flags)
    if n < minimo:
        raise SystemExit(
            f"CIRUGIA EN EL AIRE: {que}\n"
            f"  El patron no coincidio con nada (esperaba al menos {minimo}, hubo {n}).\n"
            f"  Patron: {patron!r}\n"
            "  Un matcher que no encuentra su objetivo no es 'nada que hacer': es una\n"
            "  operacion que se reporta como hecha y no se hizo. Se corrige el patron o\n"
            "  se corrige la expectativa, pero no se sigue en silencio.")
    return nuevo


def _sin_tildes(s):
    import unicodedata as _u
    return "".join(c for c in _u.normalize("NFD", str(s or "").lower())
                   if _u.category(c) != "Mn")


def _como_suena(s):
    """El nombre de la transportadora como lo escribe quien lo dicta por WhatsApp.

    MEDIDO sobre las 12 direcciones de Dolce que hablan de recoger: dos de ellas — una
    de cada seis — traen el nombre roto, y no de cualquier forma:
      · «Oficina de Inter rapidisimo»  -> partido por un espacio
      · «Oficina interrapidicimo ...»  -> escrito como suena (c por s)
    Comparar la cadena tal cual las dejaba en DUDOSO, que es seguro pero pobre: son
    puntos de recogida perfectamente identificables. Se quitan los separadores y se
    funden c/z en s, que es la confusion ortografica del castellano de aca. La ventana
    donde se busca sigue siendo de 40 caracteres pegados a la palabra que dispara, asi
    que el pliegue no puede casar con cualquier cosa del resto de la direccion.
    """
    s = _sin_tildes(s)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s.replace("z", "s").replace("c", "s")


# Las palabras que DISPARAN la sospecha de recogida en punto. Ninguna decide sola.
_GATILLO = re.compile(r"\b(oficina|sucursal|agencia|punto|reclam\w*|recog\w*|recoj\w*)\b")
# Lo que, PEGADO al gatillo, dice que NO es un punto de recogida sino la direccion del
# cliente: un numero de oficina, un piso, una torre, un edificio.
_ES_DIRECCION = re.compile(
    r"^[\s.,#-]*(?:n[or]?[.\s]*)?\d|^[\s.,#-]*(?:piso|torre|apto|apartamento|bloque|"
    r"local|interior|edificio|conjunto|barrio|casa)\b")


def pide_oficina(direccion, transportadoras=()):
    """TRES ESTADOS: «punto», «direccion» o «dudoso». Nunca dos.

    POR QUE EXISTE, y el caso es de FER via LOGISTICA DOLCE (2026-08-11): el detector
    viejo era `re.search(r"oficina|reclame", dir)` — la palabra suelta, sin mirar nada
    mas. Con eso:
      · «Oficina InterRapidisimo» -> recogida en punto. CORRECTO.
      · «oficina 303 Edificio Central» -> recogida en punto. **FALSO POSITIVO MEDIDO**, y
        era la direccion de trabajo de una clienta de Pereira.
    La palabra no distingue. **Lo que distingue es lo que va PEGADO a la palabra**: si al
    lado esta el nombre de una transportadora, es un punto de esa transportadora; si al
    lado hay un numero, un piso o una torre, es donde vive o trabaja el cliente.

    Y el tercer estado NO es un lujo. Una direccion que dice «reclamar en oficina» a
    secas no es ninguna de las dos cosas: es una que **nadie ha medido**. Devolverla como
    «direccion» seria darle permiso al motor para cambiarle la transportadora, y ese
    cambio, si de verdad era un punto, no es un ahorro: es una devolucion. Lo dudoso se
    devuelve dudoso y el informe lo dice.

    `transportadoras` son los nombres reales de la cuenta (config «operativas» + la que
    el pedido ya trae). Sin lista no se puede afirmar «punto»: se devuelve «dudoso», que
    es lo que de verdad se sabe.
    """
    d = _sin_tildes(direccion)
    if not d.strip():
        return "direccion", "no dice nada de recoger"
    nombres = [(_como_suena(t), t) for t in (transportadoras or []) if str(t).strip()]
    razones_dudoso = []
    for m in _GATILLO.finditer(d):
        ventana = d[m.end():m.end() + 40]
        antes = d[max(0, m.start() - 25):m.start()]
        # El pliegue fonetico se usa SOLO para reconocer la transportadora. La prueba de
        # «esto es una direccion» necesita la ventana CRUDA: al plegarla, «oficina piso
        # 4» se volvia «ofisinapiso4» y el patron, que se apoya en el espacio y en el
        # limite de palabra, dejaba de casar. Lo midio el banco en la misma corrida.
        for plano, original in nombres:
            if plano and (plano in _como_suena(ventana) or plano in _como_suena(antes)):
                return "punto", f"dice «{m.group(1)}» junto a {original}"
        if _ES_DIRECCION.match(ventana):
            continue          # «oficina 303», «oficina piso 4»: es donde esta el cliente
        razones_dudoso.append(m.group(1))
    if razones_dudoso:
        return "dudoso", (f"dice «{razones_dudoso[0]}» pero no nombra transportadora "
                          "ni numero: no se puede saber si es punto de recogida")
    return "direccion", "no pide recogida en punto"


# El paquete ya se movio: aqui la guia ya no se cambia, solo se llama.
YA_NO_SE_REASIGNA_POR_DEFECTO = ("EN REPARTO", "EN TERMINAL DESTINO", "EN BODEGA DESTINO",
                                 "BODEGA DESTINO", "EN RUTA", "EN CAMINO",
                                 "INTENTO DE ENTREGA", "EN REEXPEDICION")


def guias_por_corregir(decisiones, ya_no_se_reasigna=None):
    """Los pedidos CON GUIA que todavia se alcanzan a corregir, y lo que hay en juego.

    UNA DEFINICION, DOS CONSUMIDORES, y la razon es un fallo de esta misma ronda: al
    escribir el Paso 1 en los dos generadores lo defini dos veces — el de acciones por
    ESTADO y el de 360 por CAMPO `guia` — y la misma seccion del mismo dia salio con
    **13 pedidos y $36.222 en un papel y 21 y $43.725 en el otro**. Las dos cuentas eran
    ciertas y contaban cosas distintas; para el que las lee eso no es matiz, es que uno
    de los dos documentos miente. Es la falta que este expediente ya pago una vez con
    los dos denominadores de la conversion, asi que la definicion vive aqui sola.

    QUE CUENTA COMO GUIA POR CORREGIR: **tiene guia** (el hecho: ya se genero) **y el
    paquete no se ha movido** (por eso todavia se cambia) **y hace falta hacer algo**.
    El estado no define la guia: la guia la define el campo `guia`. El estado define si
    la ventana sigue abierta.

    Devuelve (lista ordenada por valor, plata en juego).
    """
    cerrados = set(ya_no_se_reasigna or YA_NO_SE_REASIGNA_POR_DEFECTO)
    fuera = []
    for d in decisiones or []:
        if not isinstance(d, dict):
            continue
        if not str(d.get("guia") or "").strip():
            continue
        if str(d.get("status") or "").upper().strip() in cerrados:
            continue
        if d.get("rec") not in ("CAMBIAR", "ASIGNAR", "SIN COBERTURA"):
            continue
        fuera.append(d)
    plata = 0
    for d in fuera:
        e = d.get("elegida")
        act = [c for c in (d.get("cands") or []) if c.get("t") == d.get("actual")]
        if e and act:
            plata += max(0, act[0]["costo"] - e["costo"])
    # EL ORDEN LO DICTO FER (2026-08-14) Y NO ES EL DEL VALOR: primero las guias con
    # ERROR DE OFICINA — «lo primordial», porque el cliente quedo en recoger en un punto
    # y la guia va por otra transportadora: **eso no es un sobrecosto, es una devolucion
    # segura**. Despues las de mal balance, que solo cuestan plata.
    # Ordenar por valor ponia arriba el pedido caro con un ahorro de mil pesos y abajo
    # el barato que se va a perder entero.
    def _clave(z):
        de_oficina = (z.get("oficina") in ("punto", "dudoso")
                      or z.get("cruce_oficina") == "igual")
        return (0 if de_oficina else 1, -float(z.get("total") or 0))
    fuera.sort(key=_clave)
    return fuera, plata


def causa_de_guia(d):
    """Por que hay que corregir esta guia. Sale impreso: un «corrige» sin causa se pospone."""
    if d.get("cruce_oficina") == "igual" or d.get("oficina") == "punto":
        return "🔴 error de oficina · la clienta recoge en punto y la guia va por otra"
    if d.get("oficina") == "dudoso":
        return "🔴 posible error de oficina · confirmar con la clienta"
    return "🟡 balance · " + (d.get("motivo") or "conviene otra transportadora")


# Como escribe la gente una direccion, reducido a lo que NO cambia entre grafias.
_ABREV = [
    (r"\b(carrera|carrena|kra|kr|cra|crra|crr|cr|kk|k)\b", "CR"),
    (r"\b(calle|clle|cll|cl|cle|ca)\b", "CL"),
    (r"\b(avenida|aven|avda|av)\b", "AV"),
    (r"\b(diagonal|diag|dg|dig)\b", "DG"),
    (r"\b(transversal|transv|trans|tv|tr)\b", "TV"),
    (r"\b(numero|numeral|num|nro|nr|no|n)\b", " "),
    (r"\b(local|lc|lo)\b", "LC"),
    (r"\b(piso|ps|p)\b", "PS"),
    (r"\b(bis)\b", "BIS"),
    (r"\b(sur)\b", "SUR"), (r"\b(norte|nte)\b", "NORTE"),
    (r"\b(este|oriente)\b", "ESTE"), (r"\b(oeste|occidente)\b", "OESTE"),
]


def normalizar_direccion(d):
    """La direccion reducida a su esqueleto: via, numeros y sufijos. Sin adornos.

    `CRA 7 # 4 - 47 local 4`, `Carrera 7 No 4-47 Lc 4` y `cra 7 4 47 lc4` son LA MISMA
    direccion escrita por tres personas distintas. Comparar cadenas crudas las declara
    diferentes, y en este cruce «diferente» significa mandar el paquete a repartir a la
    oficina de la competencia.
    """
    t = _sin_tildes(d)
    t = re.sub(r"[#°ºªnN][\s.]*(?=\d)", " ", t)      # «# 4», «No 4», «N° 4» -> « 4»
    t = re.sub(r"[^\w\s]", " ", t)
    for pat, rep in _ABREV:
        t = re.sub(pat, rep, t)
    t = re.sub(r"\s+", " ", t).strip().upper()
    return t


def _nucleo(d):
    """La via y sus TRES numeros: lo que identifica la puerta, sin el «local 4».

    TRES Y NO DOS, y lo midio el banco: con dos, «CR 7 4 99» casaba con la oficina
    «CR 7 4 47» — misma via, misma esquina, otra puerta. **Un nucleo corto convierte a
    los vecinos de la oficina en la oficina**, y mandaria por Interrapidisimo a media
    cuadra que no lo pidio.
    """
    n = normalizar_direccion(d)
    m = re.match(r"^(CR|CL|AV|DG|TV)\s+(\w+)\s+(\w+)\s+(\w+)", n)
    return " ".join(m.groups()) if m else None


def es_oficina_de_inter(direccion, ciudad, oficinas):
    """TRES ESTADOS otra vez: «igual», «parecida» o «no». Nunca dos.

    POR QUE EXISTE, y es un mandato de FER del 2026-08-16 nacido de devoluciones reales:

    **La gente que se sabe la direccion de la oficina la escribe pelada.** «Carrera 7
    # 4-47», sin decir «oficina» ni nombrar la transportadora. El detector de palabras
    (`pide_oficina`) no puede cazar esto **ni en principio**: no hay palabra que
    detectar. El motor lo lee como la casa del cliente, ve que otra transportadora es
    mas barata, y cambia. **El paquete sale a repartir a la oficina de la competencia y
    se devuelve.** En el informe eso salia como un ahorro.
    Palabras de FER: «muchas de las devoluciones es porque ponian la direccion asi».

    Y NO ES SOLO DE PUEBLO. Tambien pasa en Bogota: quien vive cerca de una oficina se
    sabe la direccion igual. Por eso el cruce va contra TODO el pais.

    LOS DOS ERRORES NO CUESTAN LO MISMO, y por eso el sesgo va escrito:
      · marcar como oficina una casa -> se manda por Inter algo que pudo ir mas barato.
        Se pierden unos pesos de flete.
      · NO marcarla -> se devuelve el pedido entero. Cien veces mas caro.
    Asi que «igual» cambia la transportadora sola y **«parecida» no cambia nada pero
    sale marcada en el informe**: un «casi» no se decide solo, lo mira una persona.

    `oficinas` es el indice {ciudad normalizada: [direcciones]} del insumo nacional.
    Si el municipio no esta en el insumo se devuelve «no» — y quien llama tiene que
    saber que eso significa «no hay con que comparar», no «no es una oficina».
    """
    if not direccion or not oficinas:
        return "no", ""
    cand = oficinas.get(_ciudad_clave(ciudad)) or []
    if not cand:
        return "no", "esa ciudad no esta en el listado de oficinas"
    mia, nucleo_mio = normalizar_direccion(direccion), _nucleo(direccion)
    for od in cand:
        suya = normalizar_direccion(od)
        if mia == suya:
            return "igual", f"es exactamente la oficina de Interrapidisimo ({od})"
        if nucleo_mio and nucleo_mio == _nucleo(od):
            return "igual", f"misma puerta que la oficina de Interrapidisimo ({od})"
    # UNA CASA CON SENAS DE CASA NO SE PARECE A NADA, aunque comparta la calle.
    #
    # MEDIDO en la primera corrida real (Dolce, 78 pedidos vivos, 2026-08-17): las DOS
    # unicas «parecidas» eran falsas alarmas, y las dos se delataban solas —
    # «...urbanizacion reservas de San Juan torre 5 apto 33» y una calle 9 contra una
    # oficina en la 9 B. El criterio de semejanza era «misma via y mismo primer numero»,
    # y en un pueblo donde la oficina esta en la calle 9 **eso convierte en sospechosa a
    # media calle 9**. Una regla que grita en cada cuadra no se lee: se ignora, y el dia
    # que grite de verdad tampoco la miran. Un falso positivo no es gratis aunque no
    # cambie ninguna decision — se paga en atencion, que es lo que escasea a las 7am.
    #
    # Estas senas no aparecen en la direccion de una oficina y si en la de una casa.
    if re.search(r"\b(apto|apartamento|apt|torre|casa|conjunto|urbanizacion|urb|"
                 r"manzana|mz|interior|int|bloque|etapa|unidad|finca|vereda|vda)\b",
                 _sin_tildes(direccion)):
        return "no", "la direccion lleva senas de vivienda (apto, torre, conjunto...)"

    for od in cand:
        # Se parece cuando comparten la via y el PRIMER numero, que es lo que casi
        # nadie escribe mal. No alcanza para cambiar sola, si para que alguien mire.
        a = re.match(r"^(CR|CL|AV|DG|TV)\s+(\w+)", mia)
        b = re.match(r"^(CR|CL|AV|DG|TV)\s+(\w+)", normalizar_direccion(od))
        if a and b and a.group(0) == b.group(0):
            return "parecida", (f"se parece a la oficina de Interrapidisimo ({od}): "
                                "confirmalo con la clienta antes de mover nada")
    return "no", ""


def _ciudad_clave(c):
    return _sin_tildes(str(c or "").split("\\")[0]).strip().upper()


def indice_de_oficinas(datos):
    """{ciudad: [direcciones]} a partir del insumo nacional, con su fecha al lado.

    Devuelve (indice, fecha, total). La fecha viaja porque un listado de oficinas
    envejece igual que la Torre: abren y cierran puntos, y un insumo viejo que nadie
    compara contra el reloj sigue pareciendo valido.
    """
    if not isinstance(datos, dict) or not datos.get("oficinas"):
        return {}, None, 0
    idx = {}
    for o in datos["oficinas"]:
        idx.setdefault(_ciudad_clave(o.get("ciudad")), []).append(o.get("direccion") or "")
    return idx, datos.get("generado"), len(datos["oficinas"])


# Lo que ya esta cerrado: corta, estable, y un estado nuevo cae del lado que SE VE.
CERRADOS = ("ENTREGADO", "CANCELADO", "RECHAZADO", "SINIESTRO", "DEVOLUCION",
            "DEVOLUCION EN BODEGA", "EN PROCESO DE DEVOLUCION",
            "TRANSITO A DEVOLUCION PROVEEDOR")


def ventana_accionable(D):
    """Los ids sobre los que se trabaja hoy, y DE DONDE salieron. Un solo sitio.

    POR QUE EXISTE, y es un defecto real del canonico medido el 2026-08-17:
    el generador hacia

        acc = set(D.get("accionables") or [])
        if acc:                       # <-- aqui
            ords = [o for o in ords if o["id"] in acc]

    y el volcado oficial de la API trae **`accionables: null`** (ausencia DECLARADA a
    proposito). Con null el `if` no dispara y **el informe barre la cuenta entera**:
    medido sobre el volcado real de Dolce, **124 «direcciones malas» de las que 120 eran
    pedidos ya cerrados** — direcciones que nadie puede ni debe corregir. Con la ventana
    derivada son **4**.

    LA CLASE, y es la tercera vez en una semana: **un campo opcional cuya ausencia
    significa «no filtrar» en vez de «avisar».** Es la familia del `.get(campo, 0)` que
    rellena con un valor plausible: aqui el valor plausible era «todo», y «todo» pasa por
    normal porque un informe mas largo no parece roto, parece completo.

    Dos productores midieron 124 y 2 con el mismo codigo, y **ninguno mentia**: cada uno
    uso un volcado distinto. Cuando dos capas dan distinto, antes de acusar a una hay que
    buscar el tercer factor.

    Devuelve (ids, origen). `origen` va al informe: quien lee tiene derecho a saber si la
    ventana la declaro el volcado o la dedujo la skill.
    """
    ords = D.get("ordenes") or []
    declarados = D.get("accionables")
    if declarados:
        return set(declarados), f"declarados por el volcado ({len(set(declarados))})"
    vivos = {o["id"] for o in ords if str(o.get("status") or "").upper().strip()
             not in CERRADOS}
    cerrados = len(ords) - len(vivos)
    return vivos, (f"DERIVADOS por negacion ({len(vivos)} de {len(ords)}; "
                   f"{cerrados} cerrados fuera) porque el volcado no los declara")


# Lo unico que todavia se puede reasignar: sin guia, o con guia recien generada.
# La lista POSITIVA es corta y estable a proposito — lo contrario de la de estados,
# que se hace larga y deja huecos. Un estado nuevo cae en «no se reasigna», que es el
# lado seguro: se llama, que nunca hace dano.
CAMBIABLES_CON_GUIA = ("GUIA_GENERADA", "PREPARADO PARA TRANSPORTADORA")


def se_puede_reasignar(orden):
    """Si a este pedido todavia se le puede cambiar la transportadora. Y por que no.

    POR QUE EXISTE, y lo dicto FER el 2026-08-17: *«este informe va a ser siempre para
    confirmar los pedidos, tiene que estar perfecto»*, y un informe que propone acciones
    imposibles **invita al error**.

    MEDIDO en el canonico: de los pedidos en NOVEDAD de Dolce, **los 5 tenian guia y ya
    habian despachado, y a 3 el informe les decia «pasar a otra transportadora»**. No es
    una recomendacion discutible: es una instruccion que no se puede ejecutar. Quien la
    lee pierde el tiempo, y quien la lee dos veces deja de confiar en la seccion entera.

    El criterio NO es el estado (esa lista se alarga y deja huecos), es **el hecho**:
    si no hay guia, se cambia; si hay guia pero el paquete no se ha movido, todavia se
    cambia; en cuanto se movio, **se llama, no se mueve**.
    """
    est = str(orden.get("status") or "").upper().strip()
    if not str(orden.get("guia") or orden.get("guide") or "").strip():
        return True, ""
    if est in CAMBIABLES_CON_GUIA:
        return True, ""
    return False, f"ya tiene guia y esta en {est.lower()}: llama, no reasignes"


def recortar(lista, tope):
    """Las filas que se imprimen y la nota que declara el recorte. SIEMPRE las dos.

    POR QUE EXISTE, y sale de un barrido propio del 2026-08-18: la skill tenia CUATRO
    tablas que recortaban filas (calientes a 30, fuga a 25 en dos sitios, potenciales a
    20) y **dos declaraban el corte y dos no**. La de «Clientes potenciales sin cerrar»
    imprimia 20 filas de una lista de N sin decirlo en ninguna parte.

    No es un fallo de calculo: el titulo llevaba el total correcto. Es que el lector ve
    un numero arriba y cuenta otro abajo, **sin nada que explique la diferencia** — y en
    ese hueco caben dos lecturas, «hay mas» y «se filtraron», que llevan a acciones
    distintas. La regla de la casa ya estaba escrita para los calientes: *recorte
    declarado no es mentira; recorte callado si*.

    LA CORRECCION VA A LA CLASE, no al caso: quien recorta ya no puede olvidarse de
    declararlo, porque el recorte y su nota **salen de la misma llamada**. Dos de cuatro
    se olvidaron cuando declararlo era un renglon aparte; ninguna puede olvidarse ahora.
    """
    total = len(lista)
    if total <= tope:
        return lista, ""
    # La nota va SIN salto delante: quien la imprime decide el espaciado, y asi esta
    # funcion no lleva ni un caracter de escape que una edicion pueda estropear.
    return lista[:tope], "Se listan %d de **%d**." % (tope, total)


def aviso_default_bodega(cfg):
    """El aviso de que la bodega tiene un default que este informe todavia no lee.

    POR QUE EXISTE: el 2026-08-17 se escribieron en Dropi **1.027 preferencias de
    transportadora por municipio** para la cuenta de Golden. La skill no las lee. Desde
    la corrida siguiente, en los **42 municipios** donde el motor difiere del default, el
    informe dice «pasar a Coordinadora» sobre un pedido que la bodega ve con Envia
    **puesta por el sistema** — y no explica por que. Quien lo lee no ve dos capas
    complementandose: ve **dos sistemas contradiciendose**, y en esa duda gana el que
    esta escrito en el panel.

    Las dos capas son correctas y hacen cosas distintas: el default es la regla general
    de la bodega; la skill decide fino por pedido con la ganancia real, la huella y la
    recogida en punto. Lo que faltaba no era codigo: era **decirselo al que lee**.

    SE RETIRA SOLO, y eso es deliberado. El aviso desaparece en cuanto el config declara
    que la skill ya lee el default (`preferencia_municipio`). **Un aviso que sobrevive a
    su motivo es ruido**, y el ruido no se va porque alguien se acuerde de borrarlo: se
    va porque su condicion deja de cumplirse. Un aviso que hay que acordarse de quitar
    es un aviso que seguira ahi dentro de un ano.
    """
    if cfg.get("preferencia_municipio"):
        return ""
    return (
        "> **La bodega tiene un default que este informe todavia no lee.** Desde el "
        "2026-08-17 la cuenta de GOLDEN tiene escrito en Dropi un default de "
        "transportadora **por municipio** (1.027 municipios). Este informe decide pedido "
        "por pedido y **no lee ese default**, asi que si lo que dice aqui difiere de lo "
        "que muestra el panel, **puede ser el default y no un error**. Leer el default y "
        "declarar cada diferencia como excepcion entra en una ronda proxima. "
        "(En cuentas sin default escrito — Dolce hoy — este aviso no aplica todavia.)")


def exigir_presente(texto, aguja, que, minimo=1):
    """La otra mitad: una BUSQUEDA de la que depende una afirmacion tambien asevera."""
    n = texto.count(aguja)
    if n < minimo:
        raise SystemExit(
            f"NO ESTA LO QUE SE BUSCABA: {que}\n"
            f"  «{aguja}» aparece {n} veces y se esperaban al menos {minimo}.")
    return n
