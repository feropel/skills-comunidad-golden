#!/usr/bin/env python3
"""Banco del cruce contra las oficinas de Interrapidisimo.

EL CASO ES DE FER, 2026-08-16, y sale de devoluciones reales: quien se sabe la
direccion de la oficina **la escribe pelada**, sin decir «oficina» ni nombrar la
transportadora. Ningun detector de palabras puede cazar eso — no hay palabra. Solo se
caza comparando contra el listado real de oficinas del pais.

LAS DIRECCIONES DE OFICINA SON REALES (listado publico de cobertura de Inter, no son
datos de ninguna clienta). Las de clientes van INVENTADAS a proposito: lo que este
banco tiene que conservar es la FORMA, no la persona.

  python3 prueba_oficinas_inter.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import (es_oficina_de_inter, normalizar_direccion,   # noqa: E402
                   indice_de_oficinas)

# Textual del listado publico: asi las escribe Interrapidisimo.
OF = {"QUINCHIA": ["CRA 7 # 4 - 47 local 4"],
      "LETICIA": ["CALLE 7 # 9 - 65"],
      "BOGOTA": ["OF. PRINC CALLE 18 # 65 A 03"],
      "ARBOLETES": ["CRA 31 DIAGONAL IGLESIA"]}
FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def caso(nombre, direccion, ciudad, esperado):
    v, razon = es_oficina_de_inter(direccion, ciudad, OF)
    juzgar(f"{nombre}: «{direccion}» -> {esperado}", v == esperado, f"dio {v} ({razon})")


def main():
    print("banco del cruce contra las oficinas de Interrapidisimo\n")

    # 1 · LA MISMA DIRECCION, ESCRITA COMO LA ESCRIBE LA GENTE.
    #     Este es EL caso: ninguna de estas dice «oficina» ni «Interrapidisimo».
    caso("identica", "CRA 7 # 4 - 47 local 4", "QUINCHIA", "igual")
    caso("otra grafia de la via", "Carrera 7 No 4-47 Local 4", "QUINCHIA", "igual")
    caso("sin adornos ni puntuacion", "cra 7 4 47", "QUINCHIA", "igual")
    caso("con el numero pegado", "Kra 7 #4-47", "QUINCHIA", "igual")
    caso("sin el local (misma puerta)", "CARRERA 7 # 4 - 47", "QUINCHIA", "igual")
    caso("«calle» escrita entera", "Calle 7 numero 9 - 65", "LETICIA", "igual")

    # 2 · LA CASA DE AL LADO NO ES LA OFICINA. Si esto fallara, el cruce mandaria por
    #     Inter a media ciudad — el falso positivo barato, pero no gratis.
    caso("otro numero en la misma via", "CRA 7 # 30 - 12", "QUINCHIA", "parecida")
    caso("otra via distinta", "CALLE 15 # 8 - 20", "QUINCHIA", "no")
    caso("un barrio sin numeros", "Barrio El Jardin casa 3", "QUINCHIA", "no")

    # 2b · UNA CASA CON SENAS DE CASA NO SE PARECE A NADA.
    #      Los dos casos son TEXTUALES de la primera corrida real (Dolce, 2026-08-17):
    #      fueron las dos unicas «parecidas» de 78 pedidos y las dos eran falsa alarma.
    #      Con «misma via y mismo primer numero», en un pueblo cuya oficina esta en la
    #      calle 9 **media calle 9 sale sospechosa**. Una regla que grita en cada cuadra
    #      se deja de leer, y el dia que grite de verdad tampoco la miran.
    caso("apto y torre: es vivienda, no se parece a nada",
         "Calle 50 # 39 - 27 urbanizacion reservas de San Juan 1 torre 5 apto 33",
         "ARBOLETES", "no")
    # OJO CON ESTE CASO: la primera version usaba la direccion EXACTA de la oficina y
    # esperaba «no». Fallaba con razon — la coincidencia exacta gana sobre las senas de
    # vivienda, que es justo lo que asegura el caso de abajo. Se corrige el CASO, no la
    # regla: aflojar la regla para que pase el banco es como se pierden.
    caso("conjunto cerrado en la misma calle: vivienda",
         "CRA 7 # 88 - 12 conjunto Los Almendros casa 12", "QUINCHIA", "no")
    # Y EL LIMITE: la sena de vivienda NO puede tapar una coincidencia EXACTA. Si la
    # direccion ES la oficina, que ademas diga «casa» no la convierte en una casa.
    v, _ = es_oficina_de_inter("CRA 7 # 4 - 47 local 4", "QUINCHIA", OF)
    juzgar("la sena de vivienda no anula una coincidencia exacta", v == "igual", v)

    # 3 · «PARECIDA» NO CAMBIA NADA, Y ESE ES EL PUNTO.
    #     Con dos estados esto caeria en «igual» (y se cambiaria por una corazonada) o
    #     en «no» (y se perderia). Un «casi» lo mira una persona.
    v, razon = es_oficina_de_inter("CRA 7 # 30 - 12", "QUINCHIA", OF)
    juzgar("«parecida» explica que hay que confirmar con la clienta",
           v == "parecida" and "confirmalo" in razon, razon)

    # 4 · LO QUE NO SE PUEDE COMPARAR NO SE DECLARA LIMPIO.
    #     Un municipio ausente del listado devuelve «no» CON motivo: no es lo mismo
    #     «no es una oficina» que «no tengo listado de esa ciudad».
    v, razon = es_oficina_de_inter("CRA 7 # 4 - 47", "PUEBLO QUE NO ESTA", OF)
    juzgar("ciudad ausente del listado: dice que no pudo comparar",
           v == "no" and "no esta en el listado" in razon, razon)
    v, _ = es_oficina_de_inter("CRA 7 # 4 - 47", "QUINCHIA", {})
    juzgar("sin listado no se afirma nada", v == "no")

    # 5 · LA NORMALIZACION, sola, porque es de donde sale todo lo demas.
    juzgar("las tres grafias colapsan a la misma cadena",
           normalizar_direccion("CRA 7 # 4 - 47")
           == normalizar_direccion("Carrera 7 No 4-47")
           == normalizar_direccion("kra 7 4 47"),
           normalizar_direccion("Carrera 7 No 4-47"))
    juzgar("vacio y None no revientan",
           normalizar_direccion("") == "" and normalizar_direccion(None) == "")

    # 6 · EL INDICE LLEVA LA FECHA DEL INSUMO.
    #     Un listado de oficinas envejece: abren y cierran puntos. Sin fecha, un
    #     archivo de hace un ano decide igual que uno de hoy y nadie se entera.
    idx, fecha, total = indice_de_oficinas(
        {"generado": "2026-08-16",
         "oficinas": [{"ciudad": "QUINCHIA", "direccion": "CRA 7 # 4 - 47 local 4"},
                      {"ciudad": "LETICIA", "direccion": "CALLE 7 # 9 - 65"}]})
    juzgar("el indice agrupa por ciudad y trae fecha y total",
           len(idx) == 2 and fecha == "2026-08-16" and total == 2, f"{len(idx)} ciudades")
    idx, fecha, total = indice_de_oficinas(None)
    juzgar("sin insumo el indice va vacio y la fecha en None",
           idx == {} and fecha is None and total == 0)

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + "; ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del cruce contra oficinas pasaron")


if __name__ == "__main__":
    main()
