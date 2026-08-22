#!/usr/bin/env python3
"""Banco del detector de recogida en punto. Los DOS primeros casos son ajenos y reales.

LOS MIDIO LOGISTICA DOLCE contra la sesion viva el 2026-08-11, y son complementarios:
uno es el acierto que hay que conservar y el otro es el falso positivo que costaba plata.
El detector viejo (`oficina|reclame` a secas) daba VERDE en los dos, o sea: no detectaba
nada, solo repetia la palabra. Un detector que dice que si a todo no es un detector.

  · el ACIERTO: la clienta pide recoger en un punto de una transportadora concreta. Si el
    motor le cambia la transportadora por costo, el punto donde la mandaron a recoger
    **deja de existir** — el ahorro calculado era, en realidad, una devolucion.
  · el FALSO POSITIVO: «oficina 303» es donde trabaja la clienta. Excluirla del cambio
    por costo le regala a la operacion un sobrecosto por una palabra mal leida.

LOS DATOS VAN ANONIMIZADOS a proposito. Lo que este banco tiene que conservar es la
FORMA de la direccion, no la persona: un banco no es sitio para el dato de una clienta.

  python3 prueba_oficina.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import pide_oficina   # noqa: E402

# Las de la cuenta de Dolce el dia de la medicion.
OPER = ["ENVIA", "INTERRAPIDISIMO", "VELOCES"]
FALLOS = []


def juzgar(nombre, ok, detalle=""):
    print(f"  {'BIEN ' if ok else 'FALLA'}  {nombre}" + (f"  · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def caso(nombre, direccion, esperado, oper=OPER):
    veredicto, razon = pide_oficina(direccion, oper)
    juzgar(f"{nombre}: «{direccion}» -> {esperado}", veredicto == esperado,
           f"dio {veredicto} ({razon})")


def main():
    print("banco del detector de recogida en punto · 2 casos ajenos + adversariales\n")

    # ---- LOS DOS CASOS MEDIDOS, uno de cada signo ----
    caso("ajeno 1 · punto de recogida real",
         "Oficina InterRapidisimo del parque principal", "punto")
    caso("ajeno 2 · falso positivo medido (es la direccion de la clienta)",
         "Carrera 15 # 20-40 oficina 303 Edificio Central", "direccion")

    # ---- LA PALABRA SOLA NO DECIDE, en los dos sentidos ----
    caso("acento: «Interrapidísimo» con tilde tambien casa",
         "reclamar en la oficina de Interrapidísimo", "punto")
    caso("la transportadora ANTES del gatillo tambien cuenta",
         "ENVIA, oficina del centro", "punto")
    caso("piso pegado al gatillo es direccion",
         "Calle 8 numero 3-21 oficina piso 4", "direccion")
    caso("torre pegada al gatillo es direccion",
         "Av Siempreviza 100 oficina torre B", "direccion")

    # ---- EL NOMBRE ROTO SIGUE SIENDO EL NOMBRE ----
    # Los dos casos son textuales de las 12 direcciones de Dolce que hablan de recoger:
    # 1 de cada 6 trae la transportadora partida o escrita como suena. Con comparacion
    # literal caian en «dudoso», que es seguro pero deja plata en la mesa sin motivo.
    caso("nombre partido por un espacio", "Oficina de Inter rapidísimo", "punto")
    caso("nombre escrito como suena (c por s)",
         "Oficina interrapidicimo Barrio Cubis - Recoge en oficina", "punto")

    # ---- EL TERCER ESTADO: lo que no se sabe se devuelve sin saber ----
    #
    # Y ESTE ES EL CASO QUE MAS IMPORTA. Con dos estados, esta direccion caia en
    # «direccion» y el motor quedaba libre para cambiarle la transportadora. Si de
    # verdad era un punto, el ahorro impreso era una devolucion. Un detector binario
    # convierte «no lo se» en un permiso.
    caso("gatillo sin transportadora ni numero -> DUDOSO, no direccion",
         "reclamar en oficina", "dudoso")
    caso("«recoge en la agencia» tampoco se resuelve solo",
         "que lo recoja en la agencia del pueblo", "dudoso")

    # ---- SIN LISTA DE TRANSPORTADORAS NO SE PUEDE AFIRMAR «PUNTO» ----
    # No es lo mismo «no es un punto» que «no tengo con que saberlo».
    v, _ = pide_oficina("Oficina InterRapidisimo del parque", [])
    juzgar("sin lista de transportadoras el mismo texto es DUDOSO, no punto",
           v == "dudoso", f"dio {v}")

    # ---- LO QUE NO HABLA DE RECOGER NO ES NADA DE ESTO ----
    caso("una direccion normal no dispara", "Calle 44 # 12-33 barrio Centro", "direccion")
    caso("vacia no revienta", "", "direccion")
    v, _ = pide_oficina(None, OPER)
    juzgar("None no revienta", v == "direccion", f"dio {v}")

    # ---- EL GATILLO DENTRO DE OTRA PALABRA NO ES UN GATILLO ----
    # `\b` existe por esto: «Puntolargo» o «Recogetas» no piden recoger nada.
    caso("el gatillo dentro de otra palabra no cuenta",
         "Conjunto Puntolargo casa 12", "direccion")

    print()
    if FALLOS:
        print(f"FALLARON {len(FALLOS)}: " + "; ".join(FALLOS))
        sys.exit(1)
    print("todas las pruebas del detector de recogida en punto pasaron")


if __name__ == "__main__":
    main()
