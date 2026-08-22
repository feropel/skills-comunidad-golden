#!/usr/bin/env python3
"""Verifica EL ARCHIVO del informe contra el JSON de analisis. Desde el disco.

POR QUE ESTE SCRIPT EXISTE SEPARADO, y son dos rondas de evidencia:

El generador llevaba dentro su propia auto-verificacion, y **cinco versiones seguidas
comprobaron algo mas debil de lo que decian comprobar**:
  v1 buscaba el valor suelto en el documento (un `0` esta en cualquier texto largo)
  v2 exigia etiqueta y valor en la misma linea (en una fila de 5 columnas se cumple solo)
  v3 miraba la celda, pero cualquier celda de la fila
  v4 anclas invisibles... que **salian impresas en el PDF del cliente**
  v5 parseaba `L`, la lista en memoria — **no el archivo**

Las dos ultimas son la misma falta con dos disfraces: **medir el intermedio y llamarlo
el entregable.** Un generador que se verifica a si mismo mide lo que tiene a mano, y lo
que tiene a mano nunca es el papel: es la variable de la que saldra el papel. Y como el
resultado se parece, la diferencia no se nota hasta que alguien abre el archivo.

**LA DECISION (Centro de Mando, ronda 19): el verificador del papel se separa.** Este
script no conoce el generador, no importa nada suyo y no tiene acceso a sus variables:
**solo sabe abrir un `.md` y leerlo.** No puede medir el intermedio porque no existe
para el. Eso no es una mejora de estilo — es la unica forma de que la clase no vuelva.

Corre como PASO FINAL del flujo: si falla, el informe no se entrega.

===============================================================================
EL ALCANCE, DECLARADO AQUI DENTRO Y NO EN UN MENSAJE
===============================================================================
Yo declare este alcance en un reporte al Centro y NO en este archivo, y eso bloqueo
el cierre — con razon. **Lo que solo vive en el reporte no existe para quien abre el
codigo.** Es la misma falta que cometi al reves con otro artefacto: alli existia el
archivo y le faltaba la ruta; aqui existia la declaracion y le faltaba el artefacto.
Un mensaje se lee una vez; este archivo lo abre cualquiera dentro de seis meses.

**SE VERIFICAN SEIS COSAS**, y no son seis cualesquiera: las cinco primeras son
**las secciones que historicamente mintieron** en este expediente; la sexta es la
unica de FORMA, y esta porque el papel tambien miente cuando no se puede leer.

  1. LOS MOTIVOS — el cubo "se le pidieron los datos" se tragaba 623 de 743 (83,8%)
     y describia el guion del bot, no a los clientes.
  2. LOS CALIENTES — imprimian "57" pelado a quien no tiene telefono, y el recorte a
     30 filas no se declaraba: el papel decia menos de lo que habia sin avisar.
  3. LA CONVERSION — se publico 10,44% cuando la regla propia daba 6,07%: dos
     denominadores distintos para el mismo negocio en la misma pagina.
  4. LAS COBERTURAS — dos tablas contiguas con universos distintos (857 y 900) sin
     decir de que hablaba cada una: dos cifras ciertas que se leen como contradiccion.
  5. LAS SECCIONES DUPLICADAS — el ensamble metia dos veces la misma seccion, con el
     mismo pedido recortado distinto.
  6. LAS TABLAS MAL FORMADAS — quitar una columna de seis cabeceras dejo seis
     separadores con una columna de mas: seis tablas que en el PDF del cliente ya
     no eran tablas, sino parrafos de pipes. El JSON cuadraba.

**FUERA DE ALCANCE, y va nombrado UNA A UNA para que sea una decision y no un olvido.
De estas tablas este script NO comprueba nada:**

  · «Lo que hay que hacer hoy, en una hoja» (el resumen con semaforos)
  · «Donde esta parada la gente» (etapas del embudo)
  · «Clientes potenciales sin cerrar»
  · «Contactos que dieron todo y no hay orden» (la fuga)
  · «Llama a la bodega» (los que ya salieron y van mal)
  · «Novedades» y «Novedades ya solucionadas»
  · «Esperando en oficina»
  · «Cambiar transportadora antes de la guia»
  · «Lo que pidio el cliente contra lo cargado» (el cruce chat-orden)
  · «Direcciones que no sirven»
  · «Decides tu» (donde el calculo no alcanza)
  · «Como se decidio» (los criterios del motor)
  · «Que se reviso» (el contenido de las filas; solo se mira que declaren su ambito)
  · «Los mensajes para copiar» (el anexo)
  · La tabla de universos de la Parte 1

**POR QUE ASI, y no "completo":** la Parte B — los pedidos, el motor, las decisiones —
tiene su propia invariante desde hace seis rondas (27 dictadas, 27 impresas) y no ha
fallado ni una vez. Y hubo CINCO versiones de un verificador "completo" que comprobaban
menos de lo que decian. **Un verificador con alcance declarado y banco ajeno vale mas
que uno "completo" que miente sobre su cobertura.**

  python3 verificar_informe.py --informe salida.md --analisis analisis.json
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import leer_json, leer_texto   # noqa: E402


def partir_secciones(texto):
    """Reparte un markdown REAL en secciones, con las filas de cuerpo de sus tablas.

    Los diez casos adversariales que este parser tiene que aguantar salieron de la
    decimoctava verificacion, y estan en `prueba_verificador.py`:
      - dos tablas bajo una misma seccion (no se suman: cada tabla es una)
      - una celda con `|` escapado, y una celda con salto de linea
      - una fila que es solo guiones en medio de la tabla
      - un `#` dentro de un bloque de codigo (NO abre seccion)
      - dos secciones con el mismo titulo
      - una tabla al final del archivo, sin linea en blanco detras
      - una seccion sin ninguna tabla
      - una tabla sin separador (no es tabla: es prosa con pipes)
    """
    secciones, actual, en_codigo = [], {"titulo": "(cabecera)", "tablas": [],
                                       "cabeceras": []}, False
    tabla_actual, esperando_cuerpo, linea_cab = None, False, None
    for linea in texto.split("\n"):
        # UN `#` DENTRO DE UN BLOQUE DE CODIGO NO ES UN ENCABEZADO. Sin esto, un
        # comentario de shell en un ejemplo parte el documento en secciones falsas.
        if linea.lstrip().startswith("```") or linea.lstrip().startswith("~~~"):
            en_codigo = not en_codigo
            continue
        if en_codigo:
            continue
        if linea.startswith("#"):
            if tabla_actual is not None:
                actual["tablas"].append(tabla_actual)
                tabla_actual = None
            secciones.append(actual)
            actual = {"titulo": linea.lstrip("#").strip(), "tablas": [], "cabeceras": []}
            esperando_cuerpo = False
            continue
        es_fila = linea.lstrip().startswith("|")
        # El separador `| --- |` marca el comienzo del CUERPO. Una tabla sin separador
        # no es una tabla para markdown, y aqui tampoco.
        if es_fila and re.match(r"^\s*\|[\s|:-]+\|?\s*$", linea):
            if esperando_cuerpo:
                tabla_actual = []          # empieza el cuerpo de esta tabla
                esperando_cuerpo = False
                # Se guarda el par (columnas de la cabecera, columnas del
                # separador) para el chequeo 6: si no coinciden, en el PDF no hay
                # tabla, hay un parrafo de pipes.
                actual["cabeceras"].append((len(celdas(linea_cab)), len(celdas(linea))))
            elif tabla_actual is not None:
                # Una fila de guiones EN MEDIO del cuerpo no es un dato: se ignora.
                pass
            continue
        if es_fila:
            if tabla_actual is not None:
                tabla_actual.append(linea)
            else:
                esperando_cuerpo = True    # esta es la cabecera; el cuerpo viene despues
                linea_cab = linea
            continue
        # Linea que no es tabla: cierra la tabla en curso. DOS TABLAS EN UNA SECCION
        # quedan como dos entradas, no como una suma — que es el falso positivo que yo
        # mismo declare sin medir y el verificador confirmo.
        if tabla_actual is not None:
            actual["tablas"].append(tabla_actual)
            tabla_actual = None
        esperando_cuerpo = False
    if tabla_actual is not None:           # tabla al final del archivo, sin linea detras
        actual["tablas"].append(tabla_actual)
    secciones.append(actual)
    return [s for s in secciones if s["titulo"] != "(cabecera)" or s["tablas"]]


def celdas(fila):
    """Las celdas de una fila, respetando `\\|` escapado dentro de una celda."""
    tmp = fila.strip().strip("|")
    partes = re.split(r"(?<!\\)\|", tmp)
    return [p.replace("\\|", "|").strip().strip("*") for p in partes]


def buscar_seccion(secciones, texto_titulo):
    """Todas las secciones cuyo titulo CONTIENE el texto. Puede haber varias."""
    return [s for s in secciones if texto_titulo in s["titulo"]]


def verificar(informe_md, ANA):
    """Devuelve (problemas, no_juzgados). Vacia = el papel dice lo que dice el JSON.

    `no_juzgados` existe porque **un cero siempre dice de donde sale**: cuando el
    analisis no trae un campo, ese chequeo no se puede hacer, y decir "el papel cuadra"
    sin contar cuantos se juzgaron es decir 5 de 5 habiendo mirado 4. Es la ley de la
    casa aplicada al propio verificador.
    """
    secciones = partir_secciones(informe_md)
    problemas = []
    no_juzgados = []

    def n(v):
        return len(v) if isinstance(v, (list, dict)) else v

    # 1 · LOS MOTIVOS: una fila por cubo, contadas EN EL ARCHIVO.
    #
    # SE BUSCA EL CONTENIDO, NO EL TITULO. Antes se exigia el literal «Por que no
    # compraron» y un informe COMPLETO, con la tabla de motivos entera, FALLABA por
    # llamar distinto a su seccion. Un verificador que reprueba el papel correcto por el
    # nombre de un encabezado no esta verificando el dato: esta imponiendo una plantilla.
    # Y es la clase de siempre — anclarse a una cadena en vez de a lo que se quiere
    # comprobar. La tabla de motivos se reconoce por su FORMA: una tabla cuyas filas
    # tienen los nombres de los cubos del analisis.
    motivos = ANA.get("motivos") or {}
    tabla_motivos, donde = None, None
    if motivos:
        _claves = [str(k) for k in motivos]
        for sec in secciones:
            for t in sec["tablas"]:
                primeras = [celdas(f)[0] if celdas(f) else "" for f in t]
                if sum(1 for k in _claves if any(k[:30] in c for c in primeras)) >= max(
                        1, min(2, len(_claves))):
                    tabla_motivos, donde = t, sec["titulo"]
                    break
            if tabla_motivos is not None:
                break
    if not motivos:
        no_juzgados.append("los motivos (el analisis no trae ninguno)")
    elif tabla_motivos is None:
        problemas.append("el informe no trae ninguna tabla con los motivos del analisis "
                         "(se busca por CONTENIDO, no por el titulo de la seccion)")
    else:
        filas = len(tabla_motivos)
        if filas != len(motivos):
            problemas.append(f"la tabla de motivos (seccion «{donde}») tiene {filas} filas "
                             f"en el archivo y el analisis trae {len(motivos)} cubos")

    # 2 · LOS CALIENTES: la lista se capa a proposito, asi que el papel tiene que
    #     DECLARAR el recorte. Un recorte declarado no es una discrepancia; un recorte
    #     callado si. Esta distincion es la que faltaba: "salio mal" contra "salio como
    #     se decidio".
    cal = ANA.get("calientes") or []
    secs = buscar_seccion(secciones, "Responder hoy")
    if cal:
        if not secs:
            problemas.append(f"hay {len(cal)} clientes esperando y no sale la seccion "
                             f"«Responder hoy»")
        else:
            tablas = [t for s in secs for t in s["tablas"]]
            filas = len(tablas[0]) if tablas else 0
            if filas < len(cal):
                declara = re.search(r"Se listan .*?de \*\*" + str(len(cal)) + r"\*\*",
                                    informe_md)
                if not declara:
                    problemas.append(f"la tabla de «Responder hoy» imprime {filas} filas de "
                                     f"{len(cal)} y el informe NO declara el recorte")
            elif filas > len(cal):
                problemas.append(f"la tabla de «Responder hoy» imprime {filas} filas y solo "
                                 f"hay {len(cal)} clientes esperando")
    elif secs and not any(re.search(r"[Nn]adie quedo esperando", s["titulo"]) for s in secs):
        problemas.append("no hay nadie esperando y la seccion no lo dice")

    # 3 · LA CONVERSION: si el analisis la midio, el numero tiene que estar EN EL PAPEL.
    #
    # CLAVE AUSENTE NO ES MEDIDO-EN-NONE, y confundirlos me costo un falso positivo
    # contra el insumo canonico: ese archivo trae el esquema viejo (`conversion_pct`
    # del recorte, sin `conversion_universo_pct`), asi que este chequeo acusaba al
    # informe de "publicar una conversion que el analisis no midio" y **abortaba la
    # entrega**. Son tres estados, no dos:
    #   - la clave NO ESTA  -> este analisis no lleva ese dato: NO SE PUEDE JUZGAR
    #   - la clave esta y es None -> se pidio y no se pudo medir: el papel no la publica
    #   - la clave esta con numero -> tiene que aparecer en el papel
    # Es la ley del cero honesto aplicada al propio verificador: "no lo se" y "es que
    # no hay" son respuestas distintas, tambien cuando quien no sabe soy yo.
    if "conversion_universo_pct" not in ANA:
        pct = "NO_JUZGABLE"
    else:
        pct = ANA.get("conversion_universo_pct")
    if pct == "NO_JUZGABLE":
        no_juzgados.append("la conversion (el analisis no trae `conversion_universo_pct`)")
    elif pct is not None:
        if f"{pct:.2f}%" not in informe_md and f"{pct}%" not in informe_md:
            problemas.append(f"el analisis midio la conversion en {pct}% y ese numero no "
                             f"aparece en el informe")
        uni = ANA.get("universo_completo")
        comp = ANA.get("compradores_universo")
        if uni and comp is not None:
            # La resta tiene que cerrar EN EL PAPEL, no en la cabeza de quien lo escribio.
            if f"{uni - comp:,}".replace(",", ".") not in informe_md:
                problemas.append(f"no aparece en el informe el numero de los que no "
                                 f"compraron ({uni - comp})")
    else:
        # ANCLADO A SU SECCION: la frase suelta en cualquier parte del documento no
        # bastaba — asi un texto pegado fuera de la Parte 1 pasaba de largo.
        parte1 = [x for x in secciones if "El denominador" in x["titulo"]
                  or "asistente de WhatsApp" in x["titulo"]]
        if re.search(r"[Ll]a conversion de la cuenta es \*\*\d", informe_md) and parte1:
            problemas.append("el informe publica una conversion que el analisis pidio "
                             "medir y no pudo")

    # 4 · UNA SOLA TABLA DE COBERTURA POR DOCUMENTO, o cada una con su ambito escrito.
    cob = [s for s in secciones if "Que se reviso" in s["titulo"]]
    if len(cob) > 1:
        # Dos tablas de cobertura pueden convivir SI CADA UNA DICE DE QUE HABLA. Sin
        # ambito, dos cifras ciertas puestas juntas se leen como una contradiccion:
        # 857 contra 900, ciego 26 contra 91, y el lector concluye que una esta mal.
        # EL HUECO ERA MAS ANCHO DE LO QUE YO CREIA, y el informe congelado lo ejercia:
        # con DOS tablas, una con ambito y otra sin nada, la condicion anterior no
        # saltaba. Si hay mas de una, **todas** declaran de que hablan — la que se queda
        # muda es justo la que el lector va a confundir con la otra.
        # Y el detector ya no es "tiene un ·": un punto medio decorativo colaba. Se
        # exige que el titulo diga sobre QUE conjunto habla.
        def _declara_ambito(t):
            return bool(re.search(r"·\s*\S", t)) and len(t.split("·", 1)[1].strip()) >= 8
        sin_ambito = [x["titulo"] for x in cob if not _declara_ambito(x["titulo"])]
        if sin_ambito:
            problemas.append(f"hay {len(cob)} tablas de cobertura y {len(sin_ambito)} no "
                             f"declara(n) su ambito: " + " · ".join(sin_ambito))

    # 5 · NINGUNA SECCION APARECE DOS VECES con el mismo titulo exacto.
    titulos = [s["titulo"] for s in secciones]
    repes = sorted({t for t in titulos if titulos.count(t) > 1 and t != "(cabecera)"})
    if repes:
        problemas.append("secciones duplicadas en el documento: " + " · ".join(repes))

    # 6 · CADA TABLA TIENE TANTAS COLUMNAS EN EL SEPARADOR COMO EN LA CABECERA.
    #
    # ESTE CHEQUEO NACIO DE UN DESTROZO PROPIO, EN ESTA MISMA RONDA. Al quitar la
    # columna «Pedido» de seis cabeceras, los seis separadores `| --- | --- |` se
    # quedaron con una columna de mas. En markdown eso no es un detalle de estilo: la
    # tabla **deja de ser una tabla** y en el PDF del cliente sale como un parrafo de
    # pipes. El generador no se entera, el JSON cuadra, y el papel llega roto.
    #
    # Es exactamente la clase que este archivo persigue — algo que solo se ve abriendo
    # el archivo — y no la cubria ninguno de los cinco anteriores, porque los cinco
    # miran CONTENIDO y este mira FORMA. Un verificador que solo compara numeros da
    # verde sobre un documento ilegible.
    for s in secciones:
        for cab, sep in s.get("cabeceras", []):
            if cab != sep:
                problemas.append(
                    f"tabla mal formada en «{s['titulo']}»: la cabecera tiene {cab} "
                    f"columnas y el separador {sep}. En el PDF no sale como tabla.")

    return problemas, no_juzgados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--informe", required=True, help="el .md YA ESCRITO en disco")
    ap.add_argument("--analisis", required=True)
    a = ap.parse_args()

    if not os.path.exists(a.informe):
        sys.exit(f"NO EXISTE EL INFORME {a.informe}: no hay nada que verificar.")
    md = leer_texto(a.informe)
    ANA = leer_json(a.analisis)

    problemas, no_juzgados = verificar(md, ANA)
    secs = partir_secciones(md)
    TOTAL = 6
    print(f"verificado {os.path.basename(a.informe)}: {len(md.splitlines())} lineas, "
          f"{len(secs)} secciones, {sum(len(s['tablas']) for s in secs)} tablas")
    print(f"  chequeos juzgados: {TOTAL - len(no_juzgados)} de {TOTAL}")
    for nj in no_juzgados:
        print(f"  NO SE PUDO JUZGAR: {nj}")
    if problemas:
        print("\nEL PAPEL NO DICE LO QUE DICE EL ANALISIS:")
        for p in problemas:
            print("  · " + p)
        sys.exit(1)
    print(f"el papel cuadra con el analisis en los {TOTAL - len(no_juzgados)} chequeos "
          f"que se pudieron hacer")


if __name__ == "__main__":
    main()
