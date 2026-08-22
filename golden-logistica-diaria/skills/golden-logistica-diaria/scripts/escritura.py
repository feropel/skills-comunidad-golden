#!/usr/bin/env python3
"""Escritura de archivos que no puede dejar un archivo a medias.

POR QUE EXISTE, y el caso es real: el barrido de conversaciones aceptaba el mismo
archivo como `--previo` y como `--salida` — de hecho ese fue el comando que esta
fabrica recomendo. Si el proceso muere MIENTRAS escribe, el archivo queda truncado
y se lleva por delante el previo, que era la unica copia. La compuerta que detecta
"previo corrupto" evita el rebarrido silencioso, que es el segundo daño; **no evita
el primero**. Para cuando la compuerta habla, el dato ya no esta.

LA CLASE, formulada por el chat LOGISTICA DOLCE al reportarlo:
**un banco de pruebas comprueba que hace el codigo cuando TERMINA; nadie comprueba
que queda en disco si NO termina.** Son dos preguntas distintas, y la segunda es la
unica que importa cuando algo se corta.

COMO SE RESUELVE: se escribe a un temporal EN EL MISMO DIRECTORIO — tiene que ser el
mismo sistema de archivos, si no `os.replace` deja de ser atomico — y al terminar se
renombra. `os.replace` es atomico: el destino queda como el viejo entero o como el
nuevo entero, nunca una mezcla. Si el proceso muere antes del renombrado, el destino
sigue intacto y solo queda un temporal que se puede borrar.

  from escritura import escribir_json, escribir_texto, exigir_salida_distinta
"""
import json, os, sys, tempfile


def exigir_salida_distinta(salida, *insumos):
    """La salida no puede ser tambien un insumo. Muere antes de tocar nada.

    Escribir encima de lo que se lee es la unica forma de perder el dato aunque la
    escritura sea atomica: el original deja de existir por diseño.
    """
    s = os.path.abspath(salida)
    for i in insumos:
        if i and os.path.abspath(i) == s:
            raise SystemExit(
                f"LA SALIDA NO PUEDE SER TAMBIEN UN INSUMO: {salida}\n"
                "  Escribir encima de lo que se lee destruye la unica copia si algo "
                "sale mal.\n"
                "  Usa un archivo distinto y renombra despues si quedas conforme.")


# ------------------------------------------------------------------------------
# LA GUARDA VIVE AQUI DENTRO, NO EN LA MEMORIA DEL QUE LLAMA.
#
# EL CASO, y costo cinco horas de barrido: `exigir_salida_distinta` estaba IMPORTADA
# en siete scripts y LLAMADA en uno. El verificador paso el mismo archivo como entrada
# y como salida del embudo y se llevo por delante 278KB de conversaciones — dejando
# 14KB, salida 0 y ni un aviso. La proteccion existia, estaba escrita, estaba probada
# y estaba importada. No servia de nada.
#
# LA CLASE: **importar una proteccion no es llamarla.** Una salvaguarda que depende de
# que alguien se acuerde de invocarla en cada sitio nuevo es una salvaguarda que ya
# fallo, solo que todavia no se sabe donde. La unica version que aguanta es la que se
# aplica POR CONSTRUCCION: aqui se apunta todo archivo que se LEE, y el escritor se
# niega solo si el destino es uno de ellos.
#
# ALCANCE, Y SE DICE ENTERO (esta es la segunda leccion, y me la gane yo):
# la primera version guardaba el registro en memoria, asi que protegia DENTRO de un
# proceso y no entre dos scripts encadenados. Yo la describi como "una que nadie puede
# olvidar", que es mas ancha que lo que media. **Una proteccion que se describe mas
# fuerte de lo que es acaba usandose donde no cubre.** Ahora:
#   - el registro se PERSISTE en disco, asi que los scripts de la misma corrida se
#     protegen entre si (el verificador lo demostro encadenando dos);
#   - se compara con `realpath`, no con `abspath`: `abspath` resuelve `..` pero NO
#     sigue enlaces, y un symlink destruyo un insumo en la verificacion;
#   - **sigue sin cubrir**: dos corridas de dias distintos (el registro es del dia), y
#     cualquier lectura que no pase por la familia `leer_*`. Por eso el banco cuenta
#     los `open(` crudos y exige cero.
_LEIDOS = set()
_ESCRITOS = set()
_NO_ENTENDIDAS = 0


def _registro_del_dia():
    """Donde viven los insumos apuntados. Compartido por los scripts de la corrida."""
    ruta = os.environ.get("GLD_REGISTRO_INSUMOS")
    if ruta:
        return ruta
    import datetime as _dt
    base = os.path.expanduser("~/.golden")
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = tempfile.gettempdir()
    return os.path.join(base, "insumos-" + _dt.date.today().isoformat() + ".txt")


def _real(ruta):
    """`realpath`, no `abspath`. Un symlink es el MISMO archivo con otro nombre."""
    return os.path.realpath(os.path.abspath(ruta))


def _quien():
    """Quien corre, DERIVADO de la ruta real. Devuelve "" si no se puede saber.

    AUTODENUNCIA CONVERTIDA EN CODIGO. Esto devolvia `basename(argv[0])`, asi que
    **cualquier archivo llamado `embudo_chatea.py` heredaba el permiso del embudo de
    verdad** — no habia que romper la guarda, bastaba con llamarse igual. Y con
    `python3 -c` o con `argv[0]` vacio todo colapsaba en una sola identidad
    compartida, que es justo como se corren los apaños de una corrida manual.

    LA CLASE: **toda regla necesita una identidad, y una identidad debil convierte la
    regla en un permiso.** Al pasar de "no" a "depende" — por una razon buena, que el
    "no" bloqueaba la operacion diaria — abri la puerta por la que se cuela lo
    ilegitimo. De ahi las tres reglas: la identidad se DERIVA (no se declara), LO
    DUDOSO NO HEREDA PRIVILEGIOS, y cada excepcion se mide como se mide un ataque.

    Cadena vacia = no se sabe = **no hay permiso de productor**, y la guarda cae a la
    regla binaria, que es la tosca y la segura.
    """
    argv = getattr(sys, "argv", None) or []
    if not argv or not argv[0] or argv[0] in ("-c", "-m"):
        return ""                     # invocacion sin script identificable
    ruta = _real(argv[0])
    if not os.path.isfile(ruta):
        return ""                     # no apunta a un archivo: no se hereda nada
    return ruta                       # RUTA REAL COMPLETA, no el nombre suelto


def _anotar(marca, ruta):
    try:
        with open(_registro_del_dia(), "a", encoding="utf-8") as f:
            f.write(f"{marca}\t{_real(ruta)}\t{_quien()}\n")
    except OSError:
        pass          # no poder persistir no justifica dejar de proteger en memoria


def _apuntar(ruta):
    _LEIDOS.add(_real(ruta))
    _anotar("R", ruta)


def _apuntar_escrito(ruta):
    _ESCRITOS.add((_real(ruta), _quien()))
    _anotar("W", ruta)


def _es_insumo(ruta):
    """True si escribir aqui destruiria un insumo de la corrida.

    UN PRODUCTOR PUEDE REESCRIBIR SU PROPIA SALIDA, y esto no es una excepcion comoda:
    es la diferencia entre las dos situaciones. El desastre fue leer un archivo y
    escribir ENCIMA de el en el mismo paso. Volver a correr el motor, que genera ese
    archivo desde cero y no lo lee, es la operacion normal de cualquier dia — y la
    primera version de esta guarda la BLOQUEABA. Una proteccion que impide la corrida
    normal se desactiva al segundo dia, y entonces no protege de nada.

    Y LA GUARDA FALLA CERRADO. Esta es la leccion que costo mas cara del expediente,
    porque el fallo estaba VIVO en produccion y lo encontro el verificador, no yo:
    el registro cambio de formato (1 campo -> 3 campos) y la version anterior hacia
    `continue` con las entradas viejas. **36 entradas del registro real quedaron
    ignoradas en silencio, y entre ellas habia un insumo de verdad, desprotegido.**
    Una linea que no se entiende NO es una linea que no existe: es una linea sobre la
    que no se sabe nada, y de lo que no se sabe no se puede concluir "se puede
    escribir". Se trata como insumo — la regla binaria, la segura — y el numero de
    entradas no entendidas SE DECLARA, porque esta skill no tiene ceros mudos.

    Esta regla ya existia en la skill para otra cosa: "un previo ilegible mata la
    corrida en vez de rebarrer en silencio". No se aplico aqui. Una politica que vale
    para los datos de fuera vale igual para los archivos de control propios.
    """
    r, yo = _real(ruta), _quien()
    if yo and (r, yo) in _ESCRITOS:
        return False
    leido = r in _LEIDOS            # lo leyo ALGUIEN (yo o otro script de la corrida)
    leido_por_mi = r in _LEIDOS     # lo lei YO, que es lo que hace peligroso escribirlo
    escrita_por_mi = False
    global _NO_ENTENDIDAS
    try:
        with open(_registro_del_dia(), encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                if not linea.strip():
                    continue
                partes = linea.split("\t")
                if len(partes) != 3:
                    # NO SE ENTIENDE -> SE ASUME LO PEOR. Si la ruta aparece ahi
                    # dentro de cualquier forma, se trata como insumo.
                    _NO_ENTENDIDAS += 1
                    if r in linea:
                        leido = True
                    continue
                marca, ruta_reg, autor = partes
                if ruta_reg != r:
                    continue
                if marca == "W" and yo and autor == yo:
                    escrita_por_mi = True
                elif marca == "R":
                    leido = True
                    if yo and autor == yo:
                        leido_por_mi = True
    except OSError as e:
        # EL REGISTRO NO SE PUDO LEER: modo binario total. No se sabe quien escribio
        # que, asi que nadie es productor de nada y solo vale lo leido en memoria.
        print(f"AVISO · no se pudo leer el registro de insumos ({e}). Se protege en modo "
              f"estricto: solo cuenta lo leido en este proceso y nadie hereda permiso "
              f"de productor.", file=sys.stderr)
        return leido
    if _NO_ENTENDIDAS:
        print(f"AVISO · el registro de insumos tiene {_NO_ENTENDIDAS} entradas que este "
              f"codigo no entiende (formato viejo o linea rota). Se tratan como insumos, "
              f"que es lo seguro. Purga o migra {_registro_del_dia()}.", file=sys.stderr)
        _NO_ENTENDIDAS = 0
    # EL PRODUCTOR REHACE LO SUYO AUNQUE OTRO LO HAYA LEIDO.
    # Segunda vez que un falso positivo bloquea la operacion normal, y esta es la del
    # gesto de la mañana: se mira el informe, se corrige algo, se rehacen las acciones.
    # Como el informe 360 habia LEIDO el archivo de acciones, el generador que lo
    # ESCRIBIO no podia rehacerlo. Pero que otro lo haya leido no hace peligroso que su
    # autor lo regenere: lo peligroso es que YO lea un archivo y escriba encima de EL,
    # que es el desastre original. Asi que la pregunta correcta no es "lo leyo alguien"
    # sino **"lo lei YO"**.
    # Sigue bloqueado: el encadenado (un script escribe donde otro leyo y el no lo
    # produjo) y el clasico (leer y escribir el mismo archivo en el mismo paso).
    if escrita_por_mi and not leido_por_mi:
        return False
    return leido


# DOS PRODUCTORES DISTINTOS AL MISMO DESTINO: politica DECLARADA, no accidente.
# Hoy se PERMITE — el segundo escribe encima del primero — porque el registro guarda
# quien escribio cada cosa y esa pista queda. No se bloquea por una razon medida: los
# dos informes escriben en `_archivo/` y en las mismas carpetas, y bloquear ahi seria
# el falso positivo de siempre. **Lo que NO se permite es leer algo y escribir encima**,
# que es el desastre real. Si algun dia dos productores compiten por un entregable,
# el registro dice quien fue el ultimo y con que script.


def leer_json(ruta, encoding="utf-8"):
    """Lee un JSON y lo APUNTA como insumo. Usar SIEMPRE para leer entradas."""
    with open(_real(ruta), encoding=encoding) as f:
        dato = json.load(f)
    _apuntar(ruta)
    return dato


def leer_texto(ruta, encoding="utf-8"):
    """Lo mismo para cualquier texto: markdown, tokens, listas.

    Existia solo la version JSON, y quedaron dos `open()` crudos en produccion. Los dos
    eran explotables: uno se llevo por delante un informe entregado, y el otro **el
    TOKEN de Chatea** — pasar `--salida` apuntando al archivo del token lo pisaba con
    el JSON de salida, con codigo de salida 0. Un secreto destruido en silencio.
    Si se lee algo, se lee con la familia `leer_*`. No hay lecturas de segunda clase.
    """
    with open(_real(ruta), encoding=encoding) as f:
        dato = f.read()
    _apuntar(ruta)
    return dato


def _escribir(ruta, escritor):
    """Temporal en el mismo directorio + replace atomico."""
    ruta = os.path.abspath(ruta)
    if _es_insumo(ruta):
        raise SystemExit(
            f"ESTE ARCHIVO ES UN INSUMO DE ESTA MISMA CORRIDA: {ruta}\n"
            "  Escribir encima de lo que se acaba de leer destruye la unica copia, y la\n"
            "  escritura atomica no salva de eso: el original deja de existir por diseño.\n"
            "  Ya paso: 278KB de conversaciones quedaron en 14KB, con salida 0 y sin aviso.\n"
            "  Usa un archivo distinto y renombra despues si quedas conforme.")
    carpeta = os.path.dirname(ruta) or "."
    os.makedirs(carpeta, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=carpeta, prefix=".tmp-", suffix=".parcial")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            escritor(f)
            f.flush()
            os.fsync(f.fileno())      # el contenido en disco ANTES del rename
        os.replace(tmp, ruta)         # atomico: o el viejo entero, o el nuevo entero
        _apuntar_escrito(ruta)        # queda constancia de quien la hizo: puede rehacerla
    except BaseException:
        # Se limpia el temporal y el destino queda como estaba. Nunca a medias.
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def escribir_texto(ruta, texto):
    _escribir(ruta, lambda f: f.write(texto))


def escribir_json(ruta, obj, indent=None):
    _escribir(ruta, lambda f: json.dump(obj, f, ensure_ascii=False, indent=indent))
