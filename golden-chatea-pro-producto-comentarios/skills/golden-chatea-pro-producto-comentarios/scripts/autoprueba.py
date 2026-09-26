#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autoprueba.py — el banco que validar_producto.py NO TENIA.

POR QUE EXISTE (auditoria del Centro de Mando, 2026-09-07, orden de FER)
`validar_producto.py` son 449 lineas y 19 puntos de chequeo que deciden si el campo
[Comentarios] Productos de un cliente real esta bien o mal. **Nadie habia comprobado nunca
que mordiera.** Ley de la casa: "si tu script dice que todo esta bien a la primera, sospecha
del script -- pruebalo contra un caso que sepas malo". Y la del barrido de listas blancas:
**el banco debe MORDER ante el sabotaje de CADA pieza**, no solo del conjunto.

COMO ESTA HECHO
Se parte de un producto que SI pasa y se le mete un sabotaje cada vez. Cada sabotaje tiene que
producir su error Y nombrar su motivo. Si un sabotaje pasa en verde, ese chequeo esta muerto.
Incluye el caso inverso -- el producto bueno tiene que PASAR --, porque un validador que
bloquea todo tampoco discrimina, y eso tambien es estar roto.

USO
  python3 autoprueba.py        ·  0 = todo muerde  ·  1 = hay un chequeo muerto
"""
import copy
import io
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.join(AQUI, "validar_producto.py")

BUENO = {
    "img": "https://cdn.shopify.com/s/files/1/0001/serum.jpg",
    "name": "Serum Aurora",
    "desc": ("Serum Aurora 30 ml para manchas y marcas. Se aplica de noche sobre rostro limpio. "
             "Resultados visibles desde la cuarta semana de uso constante. Apto para piel "
             "sensible. REGLAS DE MARCA: no prometas curas ni resultados medicos, no compares "
             "con marcas de la competencia, no inventes cifras de clientes ni porcentajes."),
    "rela": ("serum, serum aurora, aurora, manchas, mancha, marcas en la cara, melasma, "
             "hiperpigmentacion, tono desigual, aclarar piel, despigmentante, precio serum, "
             "cuanto vale el serum, quiero el serum, me interesa aurora"),
    "estado": "activo",
}

# El BUENO de arriba lleva 16 disparadores porque esa es la DOCTRINA (15-30). Por eso su via
# natural es `json`: el FORMULARIO del panel topa en 10 etiquetas (medido 2026-09-22), asi que
# un producto bien hecho segun la doctrina NO CABE por formulario. No es contradiccion, es la
# razon por la que existen dos vias. Este segundo fixture es el mismo producto RECORTADO a las
# 10 que mas rinden, que es lo que de verdad se pega en el panel.
BUENO_FORMULARIO = dict(BUENO, rela=(
    "serum aurora, aurora, serum aurora manchas, manchas en la cara, melasma, "
    "hiperpigmentacion, tono desigual de la piel, aclarar manchas del rostro, "
    "precio del serum Aurora, cuanto vale el serum Aurora"))

def veredicto(productos, via="formulario", extra=None):
    """Corre el validador en modo --json y devuelve (exit, errores, avisos) como LISTAS.

    Por que existe: el banco comprobaba el TEXTO de cada mensaje con `in`, asi que cambiar la
    redaccion de un error ponia el banco en rojo sin que el comportamiento hubiera cambiado
    (paso de verdad con el caso 18 el 2026-09-22). Un banco que mide la redaccion da falsos
    rojos y entrena a ignorarlo. Con --json se mide lo que el validador HACE; el motivo se
    ancla a una palabra estable (la llave afectada), nunca a la frase entera.
    """
    ec, sal = correr(productos, via=via, extra=list(extra or []) + ["--json"])
    try:
        d = json.loads(sal[sal.index("{"):sal.rindex("}") + 1])
    except (ValueError, json.JSONDecodeError):
        return ec, [], []
    return ec, d.get("errores", []), d.get("avisos", [])


def hay(lista, *palabras):
    """True si ALGUN mensaje de la lista menciona TODAS las palabras dadas."""
    return any(all(p.lower() in m.lower() for p in palabras) for m in lista)


fallos = []
corridos = []


def correr(productos, via="formulario", extra=None):
    """Devuelve (exit_code, salida). Se escribe a fichero temporal porque es como lo usa la
    skill de verdad -- probar por stdin validaria un camino que casi nadie recorre."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False)
        ruta = f.name
    try:
        r = subprocess.run([sys.executable, VAL, ruta, "--via", via] + list(extra or []),
                           capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    finally:
        os.unlink(ruta)


def check(n, nombre, cond, detalle=""):
    # 🔴 AVISO DE NUMERO REPETIDO: sin esto, dos casos con el mismo numero se pisan en el
    # informe y uno queda enmascarado. Pasó de verdad en config-comentarios el 06-sep.
    if n in corridos:
        print(f"[AVISO] numero de caso REPETIDO: {n} — renumera, el informe enmascara uno")
    corridos.append(n)
    print(f"   {'OK ' if cond else '🔴 '} {n}. {nombre}" + (f"  ·  {detalle}" if detalle else ""))
    if not cond:
        fallos.append(f"{n}. {nombre}")


def roto(cambios, quitar=None):
    """Copia del bueno con los cambios aplicados."""
    p = copy.deepcopy(BUENO)
    p.update(cambios)
    for k in (quitar or []):
        p.pop(k, None)
    return [p]


print("  === AUTOPRUEBA · los dos sentidos, sabotaje por PIEZA ===")

# 1 · el caso BUENO tiene que pasar POR SU VIA. Un producto con los 15-30 disparadores de la
# doctrina va por `json`; por formulario no cabe (tope de 10 etiquetas) y eso lo prueba el 15.
ec, sal = correr([BUENO], via="json")
check(1, "un producto BIEN FORMADO (doctrina, 16 disp.) pasa por JSON", ec == 0, f"exit={ec}")

# 1b · y el mismo producto recortado a 10 tiene que pasar POR FORMULARIO. Sin este caso, el
# validador podria estar bloqueando TODO por esa via y el banco no se enteraria.
ec, sal = correr([BUENO_FORMULARIO], via="formulario")
check("1b", "el mismo producto RECORTADO a 10 pasa por FORMULARIO", ec == 0, f"exit={ec}")

# 2 · falta una llave del esquema
ec, errs, _ = veredicto(roto({}, quitar=["estado"]))
check(2, "muerde una LLAVE QUE FALTA", ec != 0 and hay(errs, "estado"))

# 3 · llave de mas
ec, errs, _ = veredicto(roto({"precio": "90000"}))
check(3, "muerde una LLAVE DE MAS", ec != 0 and hay(errs, "precio"))

# 4 · tipo equivocado (numero donde va string)
ec, errs, _ = veredicto(roto({"name": 12345}))
check(4, "muerde un TIPO equivocado (int donde va string)", ec != 0 and hay(errs, "name", "string"))

# 5 · desc vacia
ec, errs, _ = veredicto(roto({"desc": ""}))
check(5, "muerde la DESC VACIA", ec != 0 and hay(errs, "desc"))

# 6 · desc por encima del tope de 500 EN LA VIA FORMULARIO (ahi BLOQUEA)
ec, errs, _ = veredicto(roto({"desc": "REGLAS DE MARCA: " + ("x" * 600)}), via="formulario")
check(6, "por FORMULARIO, una desc >500 BLOQUEA", ec != 0 and hay(errs, "desc", "500"))

# 7 · la MISMA desc por la via JSON solo avisa. Es la ley de las dos vias: el mismo dato es
#     error o aviso segun POR DONDE entra, y confundirlas recorta sin motivo o corta en silencio.
ec7, sal7 = correr(roto({"desc": "REGLAS DE MARCA: " + ("x" * 600)}), via="json")
check(7, "por JSON, la misma desc >500 solo AVISA (no bloquea)", ec7 == 0, f"exit={ec7}")

# 8 · rela vacio: sin disparadores el bot no reconoce ningun comentario
ec, sal = correr(roto({"rela": ""}))
check(8, "muerde el RELA VACIO", ec != 0 and "rela" in sal.lower())

# 9 · estado invalido
ec, sal = correr(roto({"estado": "ACTIVO"}))
check(9, "muerde un ESTADO fuera de la lista (mayuscula incluida)", ec != 0 and "estado" in sal.lower())

# 10 · img que no es URL ni marcador
ec, sal = correr(roto({"img": "foto del serum"}))
check(10, "muerde una IMG que no es URL ni marcador", ec != 0 and "img" in sal.lower())

# 11 · 🔴 img apuntando a la cuenta de OTRO workspace. No bloquea (puede ser la propia) pero
#      TIENE que avisar: es la fuga documentada — copiar esa URL muestra la imagen de la
#      cuenta ajena, y en el panel se ve bien.
ec, sal = correr(roto({"img": "https://media.chateapro.app/temp/202608/f300829/serum.jpg"}))
check(11, "AVISA de una img de la cuenta de ORIGEN (fuga entre espacios)",
      "media.chateapro.app" in sal or "cuenta" in sal.lower())

# 12 · el archivo no es una lista de objetos
ec, sal = correr(["esto no es un producto"])
check(12, "muerde un elemento que NO es un objeto", ec != 0 and "no es un objeto" in sal)

# 13 · 🔴 el nombre del producto no aparece en ningun disparador: el cliente escribe el nombre
#      de la marca y el bot no lo reconoce. Es el fallo mas caro y el mas facil de no ver.
ec, sal = correr(roto({"rela": "manchas, mancha, melasma, tono desigual, aclarar piel, "
                               "despigmentante, precio, cuanto vale, lo quiero, me interesa"}))
check(13, "AVISA si el NOMBRE no aparece en ningun disparador", "disparador" in sal.lower())

# 14 · rela con pocos disparadores
ec, sal = correr(roto({"rela": "serum, aurora"}))
check(14, "AVISA de un RELA con muy pocos disparadores", "disparador" in sal.lower())

# 15 · el tope de 10 ETIQUETAS del formulario (medido 2026-09-22 en el contador del panel).
# Es un tope de CANTIDAD, no de caracteres, y lo que se pierde es la COLA: la capa 4, que son
# los hooks del anuncio. Por eso un producto de la doctrina (15-30) NO cabe por formulario.
ec, errs, _ = veredicto([BUENO], via="formulario")
check(15, "por FORMULARIO, un rela de 16 etiquetas BLOQUEA (topa en 10)",
      ec != 0 and hay(errs, "rela", "10"), f"exit={ec}")

# 16 · el mismo rela por JSON solo avisa. Misma ley de las dos vias que la desc de 500.
ec, errs, avs = veredicto([BUENO], via="json")
check(16, "por JSON, el mismo rela de 16 etiquetas solo AVISA",
      not hay(errs, "rela", "10") and hay(avs, "rela", "10"), f"exit={ec}")

# 17 · el tope de 255 del NOMBRE, tambien leido del contador del panel
ec, errs, _ = veredicto(roto({"name": "A" * 300}), via="formulario")
check(17, "por FORMULARIO, un name >255 BLOQUEA", ec != 0 and hay(errs, "name", "255"))

# 18 · el techo del CAMPO depende del TIPO: JSON 20.000, LONG JSON 500.000. Con 60 productos
# el de tipo JSON revienta y el Long JSON no. Prueba la bandera --long-json en los dos sentidos.
gordo = [dict(BUENO, name=f"Producto numero {i}") for i in range(60)]
ec, errs, _ = veredicto(gordo, via="json")
ec2, errs2, _ = veredicto(gordo, via="json", extra=["--long-json"])
# La etiqueta informa LO QUE SE ASERTA, no el exit code. Imprimir `longjson=1` junto al texto
# "LONG JSON no aprieta" hacia leer un fallo donde no lo habia: ese 1 viene de OTROS errores del
# fixture de 60 productos, no del techo. Una etiqueta que contradice su propio caso entrena a
# desconfiar del banco -- y un banco del que se desconfia ya no sirve de guardarrail.
check(18, "el techo del campo depende del TIPO: JSON aprieta, LONG JSON no",
      hay(errs, "crudos") and not hay(errs2, "crudos"),
      f"error de crudos: JSON={'si' if hay(errs, 'crudos') else 'NO'} "
      f"LONG JSON={'SI' if hay(errs2, 'crudos') else 'no'}")

# 19 · EL CASO QUE ANTES RECHAZABA TRABAJO BUENO. Hay produccion viva con 19.617 crudos /
# 21.457 escapados: GUARDA y se relee identica. Cuando el validador media el techo en
# escapados, esa configuracion daba ERROR y exit 1. Un guardarrail que bloquea trabajo bueno
# cuesta mas que no tenerlo. Ahora tiene que AVISAR y dejar pasar.
#
# El fixture se CALIBRA, no se adivina: se anaden productos cargados de tildes (cada tilde pesa
# 1 en crudo y 6 en escapado) hasta caer en la ventana crudo<=20.000 y escapado>20.000, que es
# justo donde vive el caso real.
def _mide(lista):
    crudo = json.dumps(lista, ensure_ascii=False, separators=(",", ":"))
    return len(crudo), len(json.dumps(crudo)[1:-1])

_tildado = dict(BUENO, desc=(
    "Serum Aurora 30 ml. Aplicacion topica de absorcion rapida con formulacion "
    "hipoalergenica. REGLAS DE MARCA: no prometas curas. "
    + "accion antioxidante e hidratacion profunda con vitamina C estabilizada. " * 3
).replace("a", "\u00e1").replace("o", "\u00f3"))

_ventana = None
for _n in range(2, 60):
    _lista = [dict(_tildado, name=f"Producto {_i}") for _i in range(_n)]
    _cr, _es = _mide(_lista)
    if _cr > 20000:
        break
    if _es > 20000:
        _ventana = (_lista, _cr, _es)
        break

if _ventana is None:
    check(19, "un campo que GUARDA en crudos pero se pasa en escapados AVISA, no bloquea",
          False, "no se pudo construir un fixture en la ventana")
else:
    _lista, _cr, _es = _ventana
    ec, _errs, _avs = veredicto(_lista, via="json")
    check(19, "un campo que GUARDA en crudos pero se pasa en escapados AVISA, no bloquea",
          not hay(_errs, "crudos") and hay(_avs, "escapados"),
          f"crudo={_cr} esc={_es} · error de crudos: "
          f"{'SI' if hay(_errs, 'crudos') else 'no'} · aviso de escapados: "
          f"{'si' if hay(_avs, 'escapados') else 'NO'}")

# 20 · EL BANCO NO PUEDE DEPENDER DE LA REDACCION. Se comprueba que los mensajes viajan por
# --json como listas estructuradas, que es lo que permite medir comportamiento en vez de texto.
# Si alguien devuelve los checks a `"frase exacta" in salida`, este caso no lo caza -- pero al
# menos deja escrito por que existe el modo --json y que el banco depende de el.
ec, errs, avs = veredicto(roto({"estado": "ACTIVO"}))
check(20, "el veredicto viaja ESTRUCTURADO (--json), no como texto que se pueda re-redactar",
      isinstance(errs, list) and isinstance(avs, list) and len(errs) >= 1 and hay(errs, "estado"),
      f"errores={len(errs)} avisos={len(avs)}")

# 21 y 22 · LA REGLA CENTRAL DE KEVIN: una etiqueta que un SEGUNDO producto pueda reclamar no
# entra. Es el caso que el detector de genericos NO cubre, porque mide cada producto por separado
# y una colision solo existe mirando dos a la vez. El fixture es el ejemplo literal de la clase:
# dos magnesios que comparten "dormir" -- una etiqueta que DESCRIBE PERFECTAMENTE el producto y
# que Kevin descarta igual, por compartida.
_m1 = dict(BUENO, name="Magnesio Complex 8 en 1",
           rela=("Magnesio Complex 8 en 1, magnesio complex, dormir, calambres nocturnos, "
                 "magnesio de 8 ingredientes, precio del Magnesio Complex, "
                 "cuanto vale el Magnesio Complex, hacen envios del Magnesio Complex"))
_m2 = dict(BUENO, name="Magnesio 2 en 1",
           rela=("Magnesio 2 en 1, magnesio dos en uno, dormir, relajacion muscular, "
                 "precio del Magnesio 2 en 1, cuanto vale el Magnesio 2 en 1, "
                 "hacen envios del Magnesio 2 en 1"))
ec, errs, _ = veredicto([_m1, _m2], via="json")
check(21, "muerde una etiqueta COMPARTIDA entre dos productos (la regla central de Kevin)",
      ec != 0 and hay(errs, "colision", "dormir"),
      f"error de colision: {'si' if hay(errs, 'colision') else 'NO'}")

# 22 · EL FALSO POSITIVO, que es el fallo caro del otro lado. Dos productos que comparten
# CATEGORIA pero cuyas etiquetas llevan cada una su nombre comercial NO colisionan: ahi el
# nombre ya desempata, que es exactamente la salida que da Kevin en 2:15:02. Un detector que
# marcase esto obligaria a borrar disparadores buenos.
_s1 = dict(BUENO, name="Magnesio Complex 8 en 1",
           rela=("Magnesio Complex 8 en 1, magnesio complex para dormir, "
                 "precio del Magnesio Complex, cuanto vale el Magnesio Complex, "
                 "hacen envios del Magnesio Complex, calambres con Magnesio Complex"))
_s2 = dict(BUENO, name="Magnesio 2 en 1",
           rela=("Magnesio 2 en 1, magnesio dos en uno para dormir, precio del Magnesio 2 en 1, "
                 "cuanto vale el Magnesio 2 en 1, hacen envios del Magnesio 2 en 1, "
                 "relajacion con Magnesio 2 en 1"))
ec, errs, _ = veredicto([_s1, _s2], via="json")
check(22, "NO da falso positivo cuando cada etiqueta lleva su nombre comercial",
      not hay(errs, "colision"),
      f"error de colision: {'SI (falso positivo)' if hay(errs, 'colision') else 'no'}")

print()
if fallos:
    print(f"  🔴 {len(corridos) - len(fallos)} de {len(corridos)} — CHEQUEOS MUERTOS:")
    for f in fallos:
        print(f"     · {f}")
    sys.exit(1)
print(f"  {len(corridos)} de {len(corridos)} · el validador muerde pieza por pieza")
sys.exit(0)
