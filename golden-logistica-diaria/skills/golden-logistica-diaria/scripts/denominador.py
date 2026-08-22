#!/usr/bin/env python3
"""LA regla del denominador de conversion. UN solo sitio, dos consumidores.

POR QUE EXISTE, y el caso es real: el embudo excluia del universo los contactos que
crea la integracion de Dropi (`opted_in_through: "dropi"` — nacen de un pedido que YA
existia y nunca pasaron por el bot) y el analizador no los excluia. Dos scripts, dos
reglas, y el mismo informe publicando las dos: la conversion salio **10,44%** cuando
la cifra consistente con la regla escrita de esta misma skill es **6,07%**.

LA CLASE: una regla de negocio que vive en dos implementaciones tiene dos versiones en
cuanto alguien toca una. No se arregla copiando la regla al otro script — se arregla
sacandola de los dos y poniendola donde solo puede existir una vez. Es lo mismo que ya
se hizo con `canal_de()` y con `escritura.py`.

Y el numero de la conversion es el mas visible del informe: es el que el dueño repite.
Publicarlo con dos denominadores distintos segun quien lo calcule no es un decimal, es
decir dos cosas contrarias sobre el mismo negocio en la misma pagina.

  from denominador import es_de_integracion, medir_conversion
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import tel10   # UNA definicion: vivia en tres copias y esa es la clase que este modulo combate

MARCADOR_INTEGRACION = "dropi"
POR_QUE_SE_EXCLUYEN = (
    "nacen de un pedido que YA existia (opted_in_through=dropi): la integracion los "
    "crea despues de la compra, nunca pasaron por el embudo del bot. Contarlos infla "
    "la conversion porque entran al numerador sin haber podido estar en el denominador "
    "de verdad. Se descuentan DECLARADOS, jamas borrados en silencio"
)


def es_de_integracion(contacto):
    """AUTODENUNCIA, y ahora banco: esto comparaba SIN `.lower()`.

    Lo escribi consolidando dos implementaciones y me quede con la mia, que comparaba
    exacto; la del embudo bajaba a minusculas. El API devuelve el marcador en minusculas
    hoy, asi que el resultado no cambio — pero el dia que devuelva "Dropi" o "DROPI",
    ninguno de los dos contactos se excluye y la conversion vuelve a inflarse sin que
    nada falle a la vista.

    LA CLASE: **consolidar conserva lo que las dos hacen y puede perder lo que UNA SOLA
    protegia.** El diff obligatorio de toda consolidacion no es "que devuelven", es
    "que sabia cada una que la otra no" — defensas, no solo salidas. Y una defensa que
    se pierde no falla el dia que se pierde: falla el dia que hacia falta.
    """
    v = contacto.get("opted_in_through")
    if v is None:
        return False
    return str(v).strip().lower() == MARCADOR_INTEGRACION


def medir_conversion(contactos, telefonos_en_dropi):
    """La conversion de la cuenta, con TODO lo que hace falta para leerla.

    Devuelve tambien lo que NO se puede saber, porque un porcentaje sin sus sesgos
    declarados se lee como si fuera exacto:

    - `sin_telefono`: contactos que no pueden aparecer JAMAS en el numerador, porque
      el cruce contra Dropi es por telefono y ellos no tienen. Son los comentarios de
      Facebook e Instagram. Estan en el denominador y no pueden estar arriba: eso es
      un sesgo ESTRUCTURAL a la baja, no un dato que falte. **Que se hace con ellos es
      una decision de negocio, no del codigo**, asi que aqui se declaran y no se tocan.
    - `personas`: telefonos distintos entre los compradores. Dos contactos con el mismo
      telefono son una persona y dos filas. Cual de los dos se cuenta cambia el numero.
    """
    # EL CONTRATO DE `telefonos_en_dropi` SE DECLARA Y SE APLICA AQUI DENTRO.
    # Antes se esperaba que llegaran ya normalizados y el llamador lo hacia con SU copia
    # de tel10. Si alguien pasa los telefonos crudos, el cruce no falla: da CERO
    # compradores en silencio, que es la peor forma de fallar. Se normaliza aqui, con
    # la misma funcion que se usa para el otro lado del cruce: los dos lados iguales
    # por construccion, no por acuerdo entre dos ficheros.
    if contactos is None or telefonos_en_dropi is None:
        raise ValueError("medir_conversion necesita la lista de contactos y los telefonos "
                         "de Dropi; recibio None. Sin uno de los dos no hay conversion "
                         "que medir, y no se devuelve un cero que parezca medido.")
    tel = {t for t in (tel10(x) for x in telefonos_en_dropi) if t}
    integracion = [c for c in contactos if es_de_integracion(c)]
    sin_marcador = [c for c in contactos if c.get("opted_in_through") in (None, "")]
    base = [c for c in contactos if not es_de_integracion(c)]
    compradores = [c for c in base if tel10(c.get("phone")) in tel]
    personas = {tel10(c.get("phone")) for c in compradores}
    sin_tel = [c for c in base if not tel10(c.get("phone"))]
    d = len(base)
    return {
        "universo_bruto": len(contactos),
        "excluidos_integracion": len(integracion),
        "_por_que_excluidos": POR_QUE_SE_EXCLUYEN,
        "denominador": d,
        "compradores": len(compradores),
        "personas_distintas": len(personas),
        "_contactos_vs_personas": (
            f"{len(compradores)} contactos-comprador son {len(personas)} personas: "
            f"{len(compradores) - len(personas)} telefonos aparecen repetidos. Se publica "
            f"el conteo de CONTACTOS, que es la unidad del embudo (cada contacto es una "
            f"conversacion); las personas se declaran al lado para que nadie los sume"),
        "conversion_pct": round(100 * len(compradores) / d, 2) if d else None,
        "sin_telefono": len(sin_tel),
        "sin_marcador_de_origen": len(sin_marcador),
        "_que_es_sin_marcador": (
            f"{len(sin_marcador)} contactos no traen `opted_in_through`, asi que no se "
            f"puede saber si entraron por el bot o los creo una integracion. Se cuentan "
            f"en el denominador (es lo conservador: no se descarta a nadie por falta de "
            f"dato) y se declaran aqui para que se sepa sobre cuantos no hay certeza"),
        "_sesgo_sin_telefono": (
            f"{len(sin_tel)} contactos del denominador NO TIENEN TELEFONO (comentarios de "
            f"Facebook e Instagram). El cruce contra Dropi es por telefono, asi que no "
            f"pueden aparecer en el numerador ni comprando: la conversion queda sesgada a "
            f"la BAJA en ese tanto. Declarado, no corregido — que hacer con ellos es "
            f"regla de negocio") if sin_tel else "",
    }
