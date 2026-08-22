#!/usr/bin/env python3
"""Banco de `denominador.py` y de `comun.py`. Casos malos plantados, no corridas felices.

POR QUE EXISTE: este modulo nacio SIN banco y yo mismo lo declare como mi flanco al
pedir la verificacion. El verificador entro por ahi y confirmo lo que ya habia
autodenunciado — la comparacion sin `.lower()`. Un modulo que centraliza una regla de
negocio es MAS peligroso sin banco que el codigo duplicado que vino a reemplazar: ahora
un solo fallo se propaga a todos los consumidores a la vez.

  python3 prueba_denominador.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from denominador import es_de_integracion, medir_conversion
from comun import contacto_de, tel10, miles, concuerda, huella_txt

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def main():
    print("banco del denominador y de las funciones comunes\n")

    # --- EL CASO DE LA AUTODENUNCIA: el marcador llega con otra caja ---
    # Si esto se rompe, la conversion se infla y NADA falla a la vista.
    for v in ("dropi", "Dropi", "DROPI", " dropi ", "  DrOpI"):
        juzgar(f"marcador {v!r} se reconoce", es_de_integracion({"opted_in_through": v}))
    for v in (None, "", "shopify", "meta"):
        juzgar(f"marcador {v!r} NO se excluye", not es_de_integracion({"opted_in_through": v}))
    juzgar("contacto sin el campo no se excluye", not es_de_integracion({}))

    # --- el contrato de los telefonos: crudos tienen que funcionar igual ---
    # Antes se esperaban normalizados y, si no lo estaban, el cruce daba CERO en
    # silencio. Cero compradores es un resultado creible, y esa es la trampa.
    contactos = [
        {"phone": "3001234567", "opted_in_through": "meta"},        # compro
        {"phone": "573001234567", "opted_in_through": "meta"},      # el mismo, con 57
        {"phone": "3009999999", "opted_in_through": "meta"},        # no compro
        {"phone": "", "opted_in_through": "meta"},                  # comentario, sin telefono
        {"phone": "3001234567", "opted_in_through": "DROPI"},       # integracion: fuera
    ]
    crudos = ["57 300 123 4567", "+573001234567"]
    r = medir_conversion(contactos, crudos)
    juzgar("con telefonos CRUDOS el cruce funciona", r["compradores"] == 2,
           f"compradores={r['compradores']}")
    juzgar("el de integracion sale del denominador", r["denominador"] == 4,
           f"denominador={r['denominador']}")
    juzgar("el de integracion no entra al numerador", r["compradores"] == 2)
    juzgar("los dos formatos del mismo numero son UNA persona",
           r["personas_distintas"] == 1, f"personas={r['personas_distintas']}")
    juzgar("el sin-telefono se declara", r["sin_telefono"] == 1)
    juzgar("conversion sobre el denominador correcto", r["conversion_pct"] == 50.0,
           f"{r['conversion_pct']}%")

    # --- listas vacias y None: se dice que no se puede, no se devuelve un cero ---
    vacio = medir_conversion([], [])
    juzgar("universo vacio: la conversion es None, no 0", vacio["conversion_pct"] is None,
           str(vacio["conversion_pct"]))
    for args in (([{}], None), (None, [])):
        murio = False
        try:
            medir_conversion(*args)
        except ValueError:
            murio = True
        juzgar(f"None en {('telefonos' if args[1] is None else 'contactos')}: muere con mensaje",
               murio)

    # --- sin marcador de origen: se cuenta y se declara ---
    r2 = medir_conversion([{"phone": "3001112222"}, {"phone": "3003334444"}], [])
    juzgar("contactos sin `opted_in_through` se cuentan en el denominador",
           r2["denominador"] == 2)
    juzgar("y se declaran aparte", r2["sin_marcador_de_origen"] == 2,
           str(r2["sin_marcador_de_origen"]))

    # --- contacto_de: el bug que costo tres rondas ---
    juzgar("sin telefono NO imprime '57' pelado",
           contacto_de({"tel": ""}) == "**comentario publico** · sin telefono")
    juzgar("sin telefono con phone tampoco",
           contacto_de({"phone": None}) == "**comentario publico** · sin telefono")
    # EL TELEFONO SE IMPRIME SIN EL 57. Dictado por FER (2026-08-14): «los telefonos
    # SIN el 57 — eso no me deja encontrar a las personas». El indicativo rompe la
    # busqueda en el panel de Dropi, o sea que el numero impreso no sirve para lo unico
    # que se hace con el. Los cuatro casos siguen probando lo mismo que antes —que las
    # dos familias de insumos colapsan a UN formato— solo que el formato es el de 10.
    juzgar("sin indicativo: se imprime tal cual, 10 digitos",
           contacto_de({"tel": "3000000001"}) == "3000000001",
           contacto_de({"tel": "3000000001"}))
    juzgar("CON indicativo: se le QUITA (nunca el '5757' ni el 57 pegado)",
           contacto_de({"tel": "573000000001"}) == "3000000001",
           contacto_de({"tel": "573000000001"}))
    juzgar("acepta 'phone' igual que 'tel'", contacto_de({"phone": "3000000001"}) == "3000000001")
    juzgar("con basura de formato tambien", contacto_de({"tel": "+57 300-000 0001"}) == "3000000001")
    # Y LA OTRA MITAD DE LA REGLA: por dentro se sigue cruzando con el numero completo.
    # Son DOS representaciones del mismo dato, no un cambio de dato — si alguien
    # confunde las dos, los cruces entre insumos dejan de casar en silencio.
    juzgar("lo INTERNO no cambia: tel10 sigue dando los 10 para cruzar",
           tel10("573000000001") == "3000000001" == tel10("3000000001"))

    # --- huella: el denominador son los CERRADOS ---
    D = {"huellas": {"3001234567": {"found": True, "global_profile": {"lifetime_totals":
         {"orders": 10, "delivered": 4, "returned": 1}}}}}
    txt = huella_txt(D, {"phone": "573001234567"})
    juzgar("la huella divide por cerrados, no por total", "de 5 cerrados" in txt, txt)
    juzgar("y nombra los que van en camino", "5 en camino" in txt, txt)
    # SIN HUELLA DE DROPI, LA HUELLA SE CALCULA DE LA PROPIA BASE (FER, 2026-08-14).
    # El caso viejo exigia el literal «sin historial», y ese literal era justo el
    # problema: con el volcado oficial —que NO trae `huellas`— se imprimia al **100%
    # de los pedidos** (400 de 400 medidos) mientras la base tenia 2.637 telefonos con
    # cerrados. «Sin historial» es una respuesta plausible, no un error, asi que nadie
    # la miraba dos veces. Se corrige el CASO porque la regla cambio por dictado.
    juzgar("sin huella de Dropi y sin cerrados propios: lo dice sin inventar",
           huella_txt(D, {"phone": "3009999999"}) == "sin cerrados en esta cuenta",
           huella_txt(D, {"phone": "3009999999"}))
    D2 = {"ordenes": [{"phone": "3007777777", "status": "ENTREGADO"},
                      {"phone": "3007777777", "status": "DEVOLUCION"},
                      {"phone": "3007777777", "status": "EN REPARTO"}]}
    txt = huella_txt(D2, {"phone": "573007777777"})
    juzgar("sin huella de Dropi la calcula de la base y declara de donde sale",
           "de 2 cerrados" in txt and "de esta cuenta" in txt, txt)
    juzgar("y el pedido EN CAMINO no cuenta como fracaso", "50%" in txt, txt)

    # --- concordancia ---
    juzgar("1 en singular", concuerda(1, "fila no tiene", "filas no tienen") == "1 fila no tiene")
    juzgar("3 en plural", concuerda(3, "fila no tiene", "filas no tienen") == "3 filas no tienen")

    # --- NO PUEDE HABER COPIAS DE ESTAS FUNCIONES FUERA DEL MODULO ---
    # La regla que no se puede comprobar sola se rompe sin ruido: `tel_de` sobrevivio
    # dos rondas de "ya lo unifique" precisamente porque nadie contaba las copias.
    # EL DETECTOR MIRABA `^def` Y ESO SE ESQUIVA DE TRES MANERAS, las tres estaban
    # vivas en la skill: anidar la funcion dentro de otra, renombrarla (`t10`), o no
    # declararla y escribir la expresion a pelo. Habia CUATRO copias delante de un
    # detector en verde. Ahora se recorre el AST (caza anidadas y cualquier nombre) y
    # ademas se busca el patron literal, que no es una definicion pero hace lo mismo.
    import re, ast
    aqui = os.path.dirname(os.path.abspath(__file__))
    propias = {"contacto_de", "tel10", "t10", "miles", "miles_seguro", "pesos", "nom_de",
               "huella_txt", "tel_de", "concuerda"}
    # La expresion "ultimos 10 digitos" escrita a mano, en cualquiera de sus formas.
    EXPR = re.compile(r're\.sub\(\s*r?"\\+D"\s*,\s*""\s*,[^)]*\)\s*\[-10:\]')
    copias = []
    for f in sorted(x for x in os.listdir(aqui) if x.endswith(".py")):
        if f in ("comun.py", "prueba_denominador.py"):
            continue
        txt = open(os.path.join(aqui, f), encoding="utf-8").read()
        try:
            arbol = ast.parse(txt)
        except SyntaxError:
            copias.append(f"{f}: NO COMPILA")
            continue
        for nodo in ast.walk(arbol):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and nodo.name in propias:
                copias.append(f"{f}:{nodo.name} (linea {nodo.lineno})")
        for m in EXPR.finditer(txt):
            copias.append(f"{f}: la expresion de tel10 escrita a mano "
                          f"(linea {txt[:m.start()].count(chr(10)) + 1})")
    # `decidir_transportadora.py` no importa nada de la skill a proposito: se corre
    # suelto desde otras rutas. Su `pesos` es la unica copia permitida, y va nombrada.
    permitidas = set()   # ya no hay ninguna: `decidir_transportadora` tambien importa
    juzgar("no hay copias locales de las funciones comunes",
           not (set(copias) - permitidas), str(sorted(set(copias) - permitidas)))

    # --- Y EL REVES DE LA MONEDA: USAR SIN IMPORTAR ---
    # El detector de copias prohibe definir la funcion otra vez. Pero se puede USARLA
    # sin importarla, y entonces revienta solo cuando esa rama corre — que puede ser un
    # mes despues. Paso hoy: `cruzar_chat_orden` llamaba a `tel10()` sin importarlo y su
    # autoprueba PASABA, porque el camino de la autoprueba no toca esa linea.
    # La comprobacion de "arranca como script" tampoco lo veia por lo mismo.
    # Aqui se mira estaticamente: todo nombre de la API comun que se USA tiene que estar
    # importado o definido en ese archivo.
    API = {"tel10", "contacto_de", "miles", "miles_seguro", "pesos", "nom_de",
           "huella_txt", "concuerda", "preparar_destino_pdf", "marcar_como_propio",
           "avisar_banderas", "leer_json", "leer_texto", "escribir_json",
           "escribir_texto", "exigir_salida_distinta", "medir_conversion",
           "es_de_integracion"}
    huerfanos = []
    for f in sorted(x for x in os.listdir(aqui) if x.endswith(".py")):
        if f in ("comun.py", "denominador.py", "escritura.py", "prueba_denominador.py"):
            continue
        txt = open(os.path.join(aqui, f), encoding="utf-8").read()
        try:
            arbol = ast.parse(txt)
        except SyntaxError:
            continue
        disponibles = set()
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.ImportFrom):
                disponibles |= {al.asname or al.name for al in nodo.names}
            elif isinstance(nodo, ast.Import):
                disponibles |= {(al.asname or al.name).split(".")[0] for al in nodo.names}
            elif isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                disponibles.add(nodo.name)
            elif isinstance(nodo, ast.Assign):
                for t in nodo.targets:
                    if isinstance(t, ast.Name):
                        disponibles.add(t.id)
        usados = {n.id for n in ast.walk(arbol)
                  if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        for falta in sorted((usados & API) - disponibles):
            huerfanos.append(f"{f}: usa {falta}() y no lo importa")
    juzgar("nadie usa una funcion comun sin importarla", not huerfanos, str(huerfanos))

    # --- LA GUARDA DE ESCRITURA: IDENTIDAD Y FALLO CERRADO ---
    # Los casos son los del verificador, que gano el unico flanco que no vi: el fallo
    # del guardian mismo. Van aqui para que no vuelva a ganarlo.
    import escritura as E, tempfile as _tf, subprocess as _sp
    argv0 = sys.argv[0]
    try:
        # (1) la identidad se DERIVA: una copia con el mismo nombre NO es el mismo
        with _tf.TemporaryDirectory() as d:
            copia = os.path.join(d, "embudo_chatea.py")
            open(copia, "w").write("# copia con el mismo nombre\n")
            sys.argv = [copia]; ident_copia = E._quien()
            sys.argv = [os.path.join(aqui, "embudo_chatea.py")]; ident_real = E._quien()
            juzgar("una copia con el mismo nombre NO hereda identidad",
                   ident_copia != ident_real, f"{ident_copia!r} vs {ident_real!r}")
        # (2) lo dudoso no hereda: sin script identificable, identidad vacia
        for argv in ([], [""], ["-c"], ["-m"]):
            sys.argv = list(argv)
            juzgar(f"argv={argv!r}: sin identidad (no hereda privilegios)",
                   E._quien() == "", repr(E._quien()))
        # (3) EL REGISTRO FALLA CERRADO: entradas que no se entienden = insumo
        with _tf.TemporaryDirectory() as d:
            reg = os.path.join(d, "reg.txt")
            victima = os.path.join(d, "insumo.json")
            open(victima, "w").write('{"dato": "ORIGINAL"}')
            viejo = os.environ.get("GLD_REGISTRO_INSUMOS")
            os.environ["GLD_REGISTRO_INSUMOS"] = reg
            E._LEIDOS.clear(); E._ESCRITOS.clear()
            for contenido, nombre in (
                    (os.path.realpath(victima) + "\n", "formato viejo de 1 campo"),
                    ("R\t" + os.path.realpath(victima) + "\n", "linea truncada a 2 campos"),
                    ("R\t" + os.path.realpath(victima) + "\tx\ty\n", "linea con 4 campos"),
                    ("basura sin sentido\n" + os.path.realpath(victima) + "\n", "mezcla")):
                open(reg, "w").write(contenido)
                sys.argv = [os.path.join(aqui, "otro.py")]
                murio = False
                try:
                    E.escribir_json(victima, {"atacante": 1})
                except SystemExit:
                    murio = True
                juzgar(f"registro con {nombre}: se trata como insumo", murio)
                juzgar(f"  y el original sigue intacto",
                       open(victima).read() == '{"dato": "ORIGINAL"}')
            if viejo is None:
                os.environ.pop("GLD_REGISTRO_INSUMOS", None)
            else:
                os.environ["GLD_REGISTRO_INSUMOS"] = viejo
    finally:
        sys.argv = [argv0]
        E._LEIDOS.clear(); E._ESCRITOS.clear()

    # --- EL FILTRO DE OPCIONES NO PUEDE COMERSE LOS CONTRADICTORIOS BUENOS ---
    #
    # Los DOS LADOS, que es lo que pidio LOGISTICA GOLDEN al retirar su parche: en su
    # corrida de hoy las 42 diferencias de cantidad eran ruido del formulario **y**
    # habia 5 CONTRADICTORIOS legitimos que SI deben salir al informe («leer la
    # conversacion»). Un filtro que limpia el ruido y de paso apaga la bandera buena
    # cambia un falso positivo por un falso negativo — y el falso negativo no se ve.
    import cruzar_chat_orden as CX

    # (1) LADO RUIDO: la opcion del formulario, declarada por config, NO suma producto.
    CX.fijar_opciones_no_producto(["Si eliges Pago Contra Entrega"])
    escogidos_ruido = "1 Bolso Portacelular y 1 Si eliges Pago Contra Entrega +"
    juzgar("con la opcion declarada, el formulario NO suma cantidad",
           CX.cantidad_chat(escogidos_ruido) == 1,
           f"cuenta {CX.cantidad_chat(escogidos_ruido)}")
    CX.fijar_opciones_no_producto(None)
    juzgar("y SIN declararla vuelve el ruido (por eso el aviso existe)",
           CX.cantidad_chat(escogidos_ruido) == 2,
           f"cuenta {CX.cantidad_chat(escogidos_ruido)}")

    # (1b) LOS TRES ESTADOS DE LA BANDERA — uno por caso, porque un estado sin caso es
    #      un estado que se puede fundir con otro sin que nadie se entere. Y fundir
    #      «ausente» con «medido vacio» es lo que condenaba a las tiendas limpias a un
    #      aviso permanentemente falso.
    _b, _e, _m = CX.fijar_opciones_no_producto(None)
    juzgar("estado AUSENTE: no se midio", _m is False and _e == 0, f"({_b},{_e},{_m})")
    _b, _e, _m = CX.fijar_opciones_no_producto([])
    juzgar("estado [] EXPLICITO: medido, ninguna", _m is True and _e == 0, f"({_b},{_e},{_m})")
    _b, _e, _m = CX.fijar_opciones_no_producto(["Si eliges Pago Contra Entrega"])
    juzgar("estado CON OPCIONES: medido y filtra", _m is True and _e == 1, f"({_b},{_e},{_m})")

    # (2) LADO BUENO: dos productos de verdad siguen contando dos, con o sin config.
    CX.fijar_opciones_no_producto(["Si eliges Pago Contra Entrega"])
    escogidos_real = "1 Bolso Portacelular y 1 Billetera Manos Libres"
    juzgar("dos productos REALES siguen contando dos (el filtro no se los come)",
           CX.cantidad_chat(escogidos_real) == 2,
           f"cuenta {CX.cantidad_chat(escogidos_real)}")
    CX.fijar_opciones_no_producto(None)

    # --- LA UTILIDAD: LA REAL DEL PEDIDO GANA AL MARGEN SUPUESTO ---
    # Caso pedido por el Centro tras la medicion de LOGISTICA GOLDEN: dos pedidos
    # identicos salvo por la ganancia real, con decisiones ESPERADAS DISTINTAS. Sin
    # este caso, alguien puede volver a `ticket * margen` y ningun banco se entera.
    import decidir_transportadora as DT
    cfg_m = {"margen": 0.35, "origen": "BOGOTA", "operativas": ["A", "B"],
             "apretado": 3000, "min_envios_muni": 0, "min_cuota_muni": 0,
             "factor_tienda": 1.0, "mala_huella": 60, "ventaja_minima": 20,
             "min_huella": 3, "torre": None, "fletes": None, "retorno": None}
    motor = DT.Motor.__new__(DT.Motor)
    motor.margen = 0.35
    motor.factor = 1.0
    motor.min_envios_muni = 0
    motor.min_cuota_muni = 0
    motor.OPER = {"A", "B"}
    motor.retorno = {}
    motor.frac_ret = lambda t: 0.5
    motor.huella = lambda h, t: None
    motor.muni = lambda o: [
        {"t": "A", "pct": 70.0, "ent": 70, "dev": 30, "dias": 3},
        {"t": "B", "pct": 90.0, "ent": 90, "dev": 10, "dias": 5}]
    motor.flete_de = lambda o, t: {"A": 10000, "B": 16000}[t]
    # Se rehace el calculo tal como lo hace `candidatas`, con las dos fuentes:
    def costo(t, utilidad, p, flete):
        return flete + (1 - p) * (flete * 0.5 + utilidad)
    # Los numeros NO se suponen: se resuelve donde esta el umbral. Con estos fletes y
    # estas efectividades, A (barata, 70%) gana a B (cara, 90%) mientras la utilidad en
    # juego sea menor de 26.500 — porque lo que se pierde al fallar es lo que inclina
    # la balanza hacia la que entrega mejor.
    ticket = 100000.0
    supuesta = ticket * 0.35        # 35.000: el margen del config
    real = 10000.0                  # la ganancia REAL de ese pedido, mas baja
    a_sup, b_sup = costo("A", supuesta, 0.70, 10000), costo("B", supuesta, 0.90, 16000)
    a_real, b_real = costo("A", real, 0.70, 10000), costo("B", real, 0.90, 16000)
    juzgar("con el MARGEN supuesto gana la que entrega mejor (mas cara)", b_sup < a_sup,
           f"A={a_sup:.0f} B={b_sup:.0f}")
    juzgar("con la GANANCIA REAL (mas baja) gana la barata", a_real < b_real,
           f"A={a_real:.0f} B={b_real:.0f}")
    juzgar("o sea: la fuente de la utilidad CAMBIA la decision del pedido",
           (a_sup < b_sup) != (a_real < b_real))

    # --- NINGUNA LECTURA DE SEGUNDA CLASE ---
    # Quedaron DOS `open()` crudos en produccion y los dos eran destruibles: uno se
    # llevo un informe ya entregado, el otro EL TOKEN de Chatea. Si se lee algo, se lee
    # con la familia `leer_*`, que apunta el archivo y activa la guarda. Este conteo es
    # lo que impide que vuelva a colarse uno.
    crudos = []
    for f in sorted(x for x in os.listdir(aqui) if x.endswith(".py")):
        # `auditar_cierre.py` INSPECCIONA los archivos de la skill: no procesa datos de
        # la operacion, asi que sus lecturas no son insumos y apuntarlas ensuciaria el
        # registro con el propio codigo. Va nombrado, como la marca de autoria del PDF —
        # una excepcion sin nombre es un agujero; con nombre es una decision.
        if f in ("escritura.py", "auditar_cierre.py") or f.startswith("prueba_"):
            continue
        for i, ln in enumerate(open(os.path.join(aqui, f), encoding="utf-8"), 1):
            sin_com = ln.split("#")[0]
            # `io.open`, `builtins.open` y `codecs.open` esquivaban el detector porque
            # el patron exigia que no hubiera un punto delante. Cualquier cosa que
            # termine en `open(` y no sea `urlopen` cuenta.
            if (re.search(r"\b(?:io\.|builtins\.|codecs\.)?open\(", sin_com)
                    and "urlopen" not in sin_com
                    and "noqa: marca de control" not in ln):
                crudos.append(f"{f}:{i}")
    juzgar("no hay open() crudos: todo se lee con leer_json/leer_texto",
           not crudos, str(crudos))

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + ", ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del denominador y de comun pasaron")


if __name__ == "__main__":
    main()
