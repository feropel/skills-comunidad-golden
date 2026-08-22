#!/usr/bin/env python3
"""Banco del verificador del papel. Los casos son AJENOS: los construyo el verificador.

POR QUE IMPORTA QUE SEAN AJENOS: el banco de la regex de plantillas lo escribi yo, pasaba
entero, y no contenia ninguna de las dos clases que la tumbaron. **Un banco escrito por
el autor de la regla prueba lo que su autor ya sabia.** Estos diez casos salieron de la
decimoctava verificacion, contra un parser mio que yo daba por bueno.

  python3 prueba_verificador.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_informe import partir_secciones, celdas, verificar

FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def main():
    print("banco del verificador del papel · casos adversariales ajenos\n")

    # 1 · DOS TABLAS EN UNA SECCION. El parser viejo sumaba las filas de las dos y
    #     gritaba en falso. Yo declare este flanco sin medirlo; el verificador lo midio.
    md = ("## Una seccion\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |\n\n"
          "texto entre medias\n\n| c | d |\n| --- | --- |\n| 5 | 6 |\n")
    s = partir_secciones(md)
    juzgar("dos tablas en una seccion son DOS, no una suma",
           len(s[0]["tablas"]) == 2 and [len(t) for t in s[0]["tablas"]] == [2, 1],
           str([len(t) for t in s[0]["tablas"]]))

    # 2 · CELDA CON `|` ESCAPADO
    juzgar("una celda con pipe escapado no parte la fila",
           celdas(r"| uno \| dos | tres |") == ["uno | dos", "tres"],
           str(celdas(r"| uno \| dos | tres |")))

    # 3 · FILA DE GUIONES EN MEDIO DEL CUERPO
    md = "## X\n\n| a |\n| --- |\n| 1 |\n| --- |\n| 2 |\n"
    s = partir_secciones(md)
    juzgar("una fila de guiones en medio no cuenta como dato",
           len(s[0]["tablas"][0]) == 2, str([len(t) for t in s[0]["tablas"]]))

    # 4 · `#` DENTRO DE UN BLOQUE DE CODIGO
    md = "## Real\n\n```bash\n# esto NO es un encabezado\n```\n\n| a |\n| --- |\n| 1 |\n"
    s = partir_secciones(md)
    juzgar("un # dentro de codigo no abre seccion", len(s) == 1 and s[0]["titulo"] == "Real",
           str([x["titulo"] for x in s]))

    # 5 · DOS SECCIONES CON EL MISMO TITULO
    md = "## Igual\n\n| a |\n| --- |\n| 1 |\n\n## Igual\n\n| a |\n| --- |\n| 2 |\n"
    s = partir_secciones(md)
    juzgar("dos secciones con el mismo titulo son dos entradas", len(s) == 2)
    juzgar("y el verificador las denuncia como duplicadas",
           any("duplicadas" in p for p in verificar(md, {"motivos": {}, "calientes": []})[0]))

    # 6 · TABLA AL FINAL DEL ARCHIVO, sin linea en blanco detras
    md = "## Fin\n\n| a |\n| --- |\n| 1 |\n| 2 |"
    s = partir_secciones(md)
    juzgar("una tabla al final del archivo se cierra igual",
           s[0]["tablas"] and len(s[0]["tablas"][0]) == 2,
           str([len(t) for t in s[0]["tablas"]]))

    # 7 · SECCION SIN NINGUNA TABLA
    md = "## Solo prosa\n\nnada de tablas aqui.\n"
    s = partir_secciones(md)
    juzgar("una seccion sin tablas no revienta y queda con cero",
           len(s) == 1 and s[0]["tablas"] == [])

    # 8 · PROSA CON PIPES QUE NO ES TABLA (no hay separador)
    md = "## Prosa\n\n| esto no es tabla porque no tiene separador |\n"
    s = partir_secciones(md)
    juzgar("pipes sin separador no son una tabla", s[0]["tablas"] == [],
           str(s[0]["tablas"]))

    # 9 · EL RECORTE DECLARADO NO ES UNA MENTIRA. La lista de calientes se capa a 30 a
    #     proposito: si el papel lo DICE, no hay discrepancia; si lo calla, si.
    filas = "\n".join(f"| 5730000000{i:02d} | Cliente {i} | - | hola | 2026-08-11 |"
                      for i in range(30))
    cab = ("## Responder hoy · 45 clientes dejados esperando\n\n"
           "| Como responder | Cliente | Ciudad | Lo ultimo | Cuando |\n"
           "| --- | --- | --- | --- | --- |\n")
    ANA = {"motivos": {}, "calientes": [{"x": i} for i in range(45)]}
    con_decl = cab + filas + "\n\nSe listan los 30 mas recientes de **45**.\n"
    sin_decl = cab + filas + "\n"
    juzgar("recorte DECLARADO: no es discrepancia",
           not any("Responder hoy" in p for p in verificar(con_decl, ANA)[0]),
           str(verificar(con_decl, ANA)[0]))
    juzgar("recorte CALLADO: si es discrepancia",
           any("NO declara el recorte" in p for p in verificar(sin_decl, ANA)[0]),
           str(verificar(sin_decl, ANA)[0]))

    # 10 · LA CONVERSION QUE EL ANALISIS NO MIDIO NO PUEDE ESTAR EN EL PAPEL.
    #      El caso se ACTUALIZO al anclar el chequeo a la Parte 1: antes bastaba con
    #      que la frase apareciera en cualquier parte del documento, y una frase suelta
    #      fuera de seccion pasaba de largo. El caso viejo usaba un "## X" que ya no es
    #      Parte 1 — asi que fallaba por la razon correcta. Se corrige el CASO, no la
    #      regla: aflojar la regla para que el banco pase es como se pierden.
    ANA = {"motivos": {}, "calientes": [], "conversion_universo_pct": None}
    md = ("## Parte 1 · El asistente de WhatsApp\n\n"
          "La conversion de la cuenta es **6.07%**, medida sobre 857.\n")
    juzgar("publicar una conversion no medida se denuncia",
           any("no pudo" in p for p in verificar(md, ANA)[0]), str(verificar(md, ANA)[0]))

    # ================================================================
    # UN CHEQUEO SIN CASO ES UN CHEQUEO QUE SE PUEDE BORRAR SIN QUE NADIE SE ENTERE.
    # Medido por la decimonovena verificacion: 3 de los 5 chequeos semanticos no tenian
    # ni un caso — se borraban enteros y el banco seguia verde. **El banco probaba el
    # parser, no las reglas.** Un caso por chequeo, minimo, y cada uno tiene que FALLAR
    # cuando el chequeo se rompe.
    # ================================================================

    # CHEQUEO 1 · motivos: una fila por cubo (off-by-one)
    #
    # EL CASO SE CORRIGIO al pasar el chequeo de "buscar el titulo" a "buscar el
    # contenido": ahora la tabla de motivos se reconoce porque sus filas llevan los
    # NOMBRES de los cubos, asi que el caso tiene que traerlos. El caso viejo usaba
    # filas «uno/dos» contra cubos «a/b/c» y ya no era reconocible como tabla de
    # motivos. Se corrige el caso, no la regla.
    md = ("### Por que no compraron · los 10 que no llegaron a pedido\n\n"
          "| Motivo | Contactos | Que significa |\n| --- | --- | --- |\n"
          "| Se cayo en la direccion | 5 | x |\n| Escribio una vez | 5 | y |\n")
    tres = {"Se cayo en la direccion": 5, "Escribio una vez": 5, "Nunca escribio": 3}
    dos = {"Se cayo en la direccion": 5, "Escribio una vez": 5}
    juzgar("chequeo 1: sobra un cubo en el analisis -> se denuncia",
           any("cubos" in p for p in verificar(md, {"motivos": tres, "calientes": []})[0]),
           str(verificar(md, {"motivos": tres, "calientes": []})[0]))
    juzgar("chequeo 1: cuadran -> no se denuncia",
           not any("cubos" in p for p in verificar(md, {"motivos": dos, "calientes": []})[0]))
    # Y EL CASO NUEVO: el mismo contenido bajo OTRO TITULO tiene que pasar.
    md_otro = md.replace("### Por que no compraron · los 10 que no llegaron a pedido",
                         "### Motivos de la no compra")
    juzgar("chequeo 1: el mismo contenido con OTRO titulo no se reprueba",
           not any("motivos" in p for p in verificar(md_otro, {"motivos": dos,
                                                              "calientes": []})[0]),
           str(verificar(md_otro, {"motivos": dos, "calientes": []})[0]))

    # CHEQUEO 3 · la conversion medida TIENE que estar en el papel
    ANA3 = {"motivos": {}, "calientes": [], "conversion_universo_pct": 6.07,
            "universo_completo": 857, "compradores_universo": 52}
    juzgar("chequeo 3: la conversion medida y ausente del papel -> se denuncia",
           any("6.07" in p for p in verificar("## X\n\nnada.\n", ANA3)[0]))
    bueno = ("## X\n\nLa conversion de la cuenta es **6.07%**, medida sobre los 857. "
             "Y 805 no compraron.\n")
    juzgar("chequeo 3: la conversion presente -> no se denuncia",
           not any("6.07" in p for p in verificar(bueno, ANA3)[0]))

    # CHEQUEO 3b · CLAVE AUSENTE no es MEDIDO-EN-NONE (el falso positivo canonico)
    viejo = {"motivos": {}, "calientes": [], "conversion_pct": 0.0}   # esquema antiguo
    juzgar("chequeo 3b: esquema sin la clave -> NO se juzga (era un falso positivo)",
           not any("conversion" in p for p in verificar(bueno, viejo)[0]),
           str(verificar(bueno, viejo)[0]))
    pedido_no_medido = {"motivos": {}, "calientes": [], "conversion_universo_pct": None}
    md_p1 = "## El denominador: 857 contactos\n\nLa conversion de la cuenta es **6.07%**.\n"
    juzgar("chequeo 3b: pedido y no medido, pero publicado -> se denuncia",
           any("no pudo" in p for p in verificar(md_p1, pedido_no_medido)[0]),
           str(verificar(md_p1, pedido_no_medido)[0]))

    # CHEQUEO 4 · dos coberturas sin ambito
    dos_sin = ("## Que se reviso\n\n| a |\n| --- |\n| 1 |\n\n"
               "## Que se reviso\n\n| a |\n| --- |\n| 2 |\n")
    juzgar("chequeo 4: dos coberturas sin ambito -> se denuncia",
           any("ambito" in p for p in verificar(dos_sin, {"motivos": {}, "calientes": []})[0]))
    dos_con = ("## Que se reviso · todo el espacio\n\n| a |\n| --- |\n| 1 |\n\n"
               "## Que se reviso · SOLO logistica\n\n| a |\n| --- |\n| 2 |\n")
    juzgar("chequeo 4: dos coberturas CON ambito -> no se denuncia",
           not any("ambito" in p for p in verificar(dos_con, {"motivos": {}, "calientes": []})[0]))

    # CHEQUEO 6 · cabecera y separador con el MISMO numero de columnas
    #
    # EL CASO ES DE UN DESTROZO PROPIO: al quitar la columna «Pedido» de seis tablas,
    # los seis separadores se quedaron con una columna de mas y las seis tablas dejaron
    # de renderizar. El JSON seguia cuadrando; solo se ve abriendo el archivo.
    VACIO = {"motivos": {}, "calientes": []}
    rota = "## Rota\n\n| a | b | c |\n| --- | --- | --- | --- |\n| 1 | 2 | 3 |\n"
    juzgar("chequeo 6: separador con una columna de mas -> se denuncia",
           any("mal formada" in p for p in verificar(rota, VACIO)[0]),
           str(verificar(rota, VACIO)[0]))
    sana = "## Sana\n\n| a | b | c |\n| --- | --- | --- |\n| 1 | 2 | 3 |\n"
    juzgar("chequeo 6: la tabla bien formada no se denuncia",
           not any("mal formada" in p for p in verificar(sana, VACIO)[0]),
           str(verificar(sana, VACIO)[0]))
    corta = "## Corta\n\n| a | b | c |\n| --- | --- |\n| 1 | 2 | 3 |\n"
    juzgar("chequeo 6: separador con una columna de MENOS tambien se denuncia",
           any("mal formada" in p for p in verificar(corta, VACIO)[0]),
           str(verificar(corta, VACIO)[0]))
    # Y LA SEGUNDA TABLA DE UNA SECCION TAMBIEN SE MIRA: si solo se guardara la
    # primera, una tabla rota mas abajo pasaria de largo.
    dos = ("## Dos\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n\ntexto\n\n"
           "| a | b |\n| --- | --- | --- |\n| 1 | 2 |\n")
    juzgar("chequeo 6: la SEGUNDA tabla de la seccion tambien se juzga",
           any("mal formada" in p for p in verificar(dos, VACIO)[0]),
           str(verificar(dos, VACIO)[0]))

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + ", ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del verificador del papel pasaron")


if __name__ == "__main__":
    main()
