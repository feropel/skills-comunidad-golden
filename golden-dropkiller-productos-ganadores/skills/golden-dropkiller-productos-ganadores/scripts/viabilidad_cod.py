#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""viabilidad_cod.py — dice si un producto DEJA PLATA, con los numeros reales de Golden.

POR QUE EXISTE
La rubrica puntuaba el margen "a ojo": PVP/costo >= 3x = puntos llenos. Eso no es una
cuenta, es una regla de pulgar heredada de un curso -- y el curso usa numeros PRESTADOS que
no son los de Golden. Medido contra 18.391 pedidos reales de Dropi:
  tasa de entrega  73,5%   (el curso asume 75%)
  flete de entrega $15.664 (el curso asume $12.000)
  pedido FALLIDO   $12.518 (el curso asume $8.000) -- n=4.074, el 99% de las devoluciones y
                   TODAS las transportadoras. Es UN SOLO cobro y siempre MENOR que el flete
                   de ida (0,73 a 1,00 segun transportadora): si el pedido se devuelve no
                   hubo recaudo, asi que no se paga la gestion de cobro.
                   🔴 NO usar $29.182: salia del informe 'por producto', donde esa columna
                   la llena UNA sola transportadora (37% de las filas) y ademas inflada.
Con los numeros del curso un producto parece viable y con los de Golden pierde plata.

LA CUENTA, y por que es POR PEDIDO GENERADO y no por entregado
La pauta se paga por cada pedido que entra, entregue o no. Contar solo los entregados
esconde el 26,6% que cuesta y no paga. Por cada pedido GENERADO:

  utilidad = p*(PVP*(1-comision) - costo - flete)  -  (1-p)*fallido  -  CPA

  p = tasa de entrega. El primer termino solo ocurre si el pedido llega; el segundo es lo
  que cuesta cada uno que no llega; el CPA se paga siempre.

🔴 EL CPA ESTA MEDIDO ($21.428) PERO ES UN PISO, NO UN PUNTO: el denominador incluye
pedidos que no vinieron de anuncio y un mes puede estar incompleto, asi que el real es
igual o mayor. Todo veredicto de aqui es OPTIMISTA por construccion, y por eso el informe
dice CUANTO CPA AGUANTA el producto en vez de solo un si o un no.
🔴 LA COMISION DE RECAUDO ES 0, Y NO ES QUE NO SE COBRE: ES QUE YA ESTA EN EL FLETE.
La transportadora cobra ~5% del flete base por recaudar, y Dropi ya lo incluye al generar
la orden (FER, 2026-09-23). El flete medido sale de lo que Dropi COBRO, asi que ya la trae.
Restar ademas un % del PVP era cobrarla dos veces, y sobre la base equivocada. Comprobado
contra los 17 informes 'por pedido': 1 entregado de 11.669 trae comision > 0 (0,0086%).
El termino sigue en la formula: si algun dia se cobra por fuera, --comision lo revive.

USO
  python3 viabilidad_cod.py --costo 30000 --pvp 90215
  python3 viabilidad_cod.py --costo 30000                 (dice el PVP minimo)
  python3 viabilidad_cod.py --costo 30000 --pvp 80000 --cpa 0 --comision 0
  python3 viabilidad_cod.py --autoprueba
Salida: 0 el producto pasa el piso · 1 no lo pasa · 2 error de uso.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "assets", "economia-cod-golden.json")


def cargar():
    d = json.load(open(ASSET, encoding="utf-8"))
    m = d["medidos"]
    return {
        "p": m["tasa_entrega"]["valor"],
        "flete": m["flete_entrega_cop"]["valor"],
        "fallido": m["costo_pedido_fallido_cop"]["valor"],
        # 0 desde el 2026-09-23: la gestion de cobro va DENTRO del flete, no aparte.
        # El termino sigue vivo en la formula por si alguna transportadora la cobra por fuera.
        "comision": m["comision_recaudo"]["valor"],
        "cpa": m["cpa_cop"]["valor"],   # medido, y es un PISO
        "piso": d["umbral"]["utilidad_minima_por_pedido_generado_cop"],
    }


def utilidad(pvp, costo, p, flete, fallido, comision, cpa):
    """Utilidad esperada por PEDIDO GENERADO."""
    return p * (pvp * (1 - comision) - costo - flete) - (1 - p) * fallido - cpa


def pvp_minimo(costo, piso, p, flete, fallido, comision, cpa):
    """Despeje directo de la formula. Sin busqueda: la funcion es lineal en el PVP."""
    necesario = (piso + cpa + (1 - p) * fallido) / p + costo + flete
    return necesario / (1 - comision)


def informe(costo, pvp, par):
    p, flete, fallido = par["p"], par["flete"], par["fallido"]
    com, cpa, piso = par["comision"], par["cpa"], par["piso"]
    minimo = pvp_minimo(costo, piso, p, flete, fallido, com, cpa)
    mult_min = minimo / costo if costo else float("inf")

    print(f"  ECONOMIA COD DE GOLDEN (medida sobre 18.391 pedidos)")
    print(f"    entrega {p:.1%} · flete ${flete:,.0f}  (medidos)")
    print(f"    pedido fallido ${fallido:,.0f}  (medido: UN solo cobro, menor que el flete)")
    print(f"    CPA ${cpa:,.0f} MEDIDO — pero es un PISO: el real es igual o mayor")
    if com:
        print(f"    comision de recaudo {com:.1%} POR FUERA del flete (dada por parametro)")
    else:
        print(f"    comision de recaudo 0 — la gestion de cobro ya viene DENTRO del flete")
    print(f"  PISO: ${piso:,.0f} de utilidad por pedido GENERADO\n")
    print(f"  Costo del producto: ${costo:,.0f}")
    print(f"  PVP MINIMO para pasar el piso: ${minimo:,.0f}  =  {mult_min:.2f}x el costo")

    if pvp is None:
        print("\n  (sin --pvp no hay veredicto: esto es el minimo, no una recomendacion de precio)")
        robustez(costo, None, minimo, p, flete, fallido, com, cpa, piso)
        return 0
    u = utilidad(pvp, costo, p, flete, fallido, com, cpa)
    mult = pvp / costo if costo else float("inf")
    print(f"  PVP propuesto: ${pvp:,.0f}  =  {mult:.2f}x")
    print(f"  Utilidad por pedido generado: ${u:,.0f}")
    if u >= piso:
        print(f"\n  ✅ PASA. Deja ${u - piso:,.0f} por encima del piso.")
        veredicto = 0
    else:
        falta = minimo - pvp
        print(f"\n  🔴 NO PASA. Le faltan ${falta:,.0f} de precio "
              f"({(minimo/costo) - mult:+.2f}x).")
        if u > 0:
            print(f"     Ojo: deja ${u:,.0f}, o sea NO pierde plata — pero ocupa operacion,")
            print(f"     inventario y atencion para dejar propina. Por eso el piso existe.")
        veredicto = 1
    # 🔴 El CPA ya esta MEDIDO, pero es un PISO: el denominador incluye pedidos que no
    # vinieron de anuncio y un mes puede estar incompleto, asi que el real es igual o mayor.
    # Un veredicto contra un piso es OPTIMISTA por construccion. En vez de esconderlo detras
    # de un si o un no, se dice CUANTO CPA aguanta el producto: eso es un dato derivado, no
    # un supuesto inventado, y es lo que de verdad decide si el margen es real o de papel.
    cpa_tope = None
    if pvp is not None:
        cpa_tope = p * (pvp * (1 - com) - costo - flete) - (1 - p) * fallido - piso
        print(f"\n  AGUANTE · este producto soporta hasta ${cpa_tope:,.0f} de CPA")
        print(f"    CPA medido hoy: ${cpa:,.0f}  🔴 y es un PISO, no un punto: el real es "
              f"igual o mayor.")
        if cpa_tope < cpa:
            print(f"    🔴 No aguanta ni el piso. Le sobran ${cpa - cpa_tope:,.0f} de pauta.")
        else:
            holgura = (cpa_tope - cpa) / cpa
            if holgura < 0.20:
                print(f"    ⚠️ Aguanta solo un {holgura:.0%} por encima del piso medido. Como el")
                print(f"       CPA real es MAYOR que ese piso, este margen puede no existir.")
            else:
                print(f"    ✅ Aguanta un {holgura:.0%} por encima del piso medido.")
    robustez(costo, pvp, minimo, p, flete, fallido, com, cpa, piso)
    return veredicto


def robustez(costo, pvp, minimo, p, flete, fallido, com, cpa, piso):
    """Mueve los parametros que TODAVIA pueden moverse y muestra que pasa.

    Hasta el 2026-09-23 esta seccion comparaba "con comision" contra "sin comision", porque
    la comision era el unico numero supuesto. Ya no lo es: es 0 medido. Comparar 0 contra 0
    habria impreso dos lineas identicas y un aviso falso — la clase de verde barato que la
    casa no admite. Ahora se mueve el CPA (es un PISO: el real es igual o mayor) y la entrega
    (hay una senal en vigilancia). Y si alguien revive la comision por parametro, se compara
    contra quitarla, que es el caso que le interesa.

    Vive aparte porque sin --pvp el informe retornaba ANTES de llegar aqui: la seccion
    existia y no se imprimia nunca. Se vio corriendo el script, no leyendolo.
    """
    if com:
        cabeza = f"la comision del {com:.1%} la diste tu por parametro; medida, es 0"
    else:
        cabeza = "la comision ya esta medida en 0"
    print(f"\n  ROBUSTEZ · se mueve lo que todavia puede moverse ({cabeza}).")
    escenarios = [("CPA +20% (es un piso)", {"cpa": cpa * 1.2}),
                  ("CPA +50%", {"cpa": cpa * 1.5}),
                  ("entrega 76,5% (senal may-ago)", {"p": 0.765})]
    if com:
        escenarios.insert(0, (f"sin la comision del {com:.1%}", {"comision": 0.0}))
    for nombre, cambio in escenarios:
        q = {"p": p, "flete": flete, "fallido": fallido, "comision": com, "cpa": cpa}
        q.update(cambio)
        if pvp is None:
            mk = pvp_minimo(costo, piso, q["p"], q["flete"], q["fallido"], q["comision"], q["cpa"])
            print(f"    {nombre:<30} minimo ${mk:>9,.0f} = {mk/costo:.2f}x  ({mk - minimo:+,.0f})")
        else:
            uk = utilidad(pvp, costo, q["p"], q["flete"], q["fallido"], q["comision"], q["cpa"])
            print(f"    {nombre:<30} ${uk:>9,.0f}  {'PASA' if uk >= piso else 'NO PASA'}")


def autoprueba():
    """Muerde pieza por pieza. Un banco que solo prueba el caso global da verde con media
    herramienta rota (ley de la casa). Aqui ademas se exige reproducir los DOS casos ancla
    que midio el chat FILTRO: si la formula no los reproduce, es otra formula."""
    par = cargar()
    casos, ok = [], 0

    def u(pvp, costo=30000, **kw):
        q = dict(par)
        q.update(kw)
        return utilidad(pvp, costo, q["p"], q["flete"], q["fallido"], q["comision"], q["cpa"])

    # --- anclas: los dos numeros que el chat FILTRO midio y publico ---
    casos.append((f"a costo 30.000, 2,5x NO alcanza (75.000 da ${u(75000):,.0f})",
                  u(75000) < par["piso"]))
    casos.append((f"a costo 30.000, 3,13x SI alcanza (94.000 da ${u(94000):,.0f})",
                  u(94000) >= par["piso"]))
    # 🔴 el ancla que se movio el 2026-09-23: hasta ese dia $80.000 NO pasaba (-$1.860) y el
    #    minimo era 3,13x. Sin la comision duplicada pasa a $492, que sigue SIN alcanzar el
    #    piso de $8.000. Quitar la comision ABARATA el minimo, no regala veredictos.
    casos.append((f"quitar la comision NO vuelve viable a 80.000 (da ${u(80000):,.0f}, "
                  f"piso ${par['piso']:,.0f})", 0 < u(80000) < par["piso"]))

    # --- la regla corta: 2,5x NO alcanza y ~3x si ---

    # --- el despeje tiene que coincidir con la evaluacion (dos caminos, un resultado) ---
    m = pvp_minimo(30000, par["piso"], par["p"], par["flete"], par["fallido"],
                   par["comision"], par["cpa"])
    casos.append((f"el PVP minimo despejado (${m:,.0f}) deja exactamente el piso",
                  abs(u(m) - par["piso"]) < 1))

    # --- SABOTAJE de cada numero medido: si cambiarlo no mueve el veredicto,
    #     ese numero no se esta usando y la formula es decorativa ---
    base = u(80000)
    casos.append(("usa la TASA DE ENTREGA (cambiarla mueve el resultado)",
                  abs(u(80000, p=0.75) - base) > 100))
    casos.append(("usa el FLETE (cambiarlo mueve el resultado)",
                  abs(u(80000, flete=12000) - base) > 100))
    casos.append(("usa el COSTO DEL FALLIDO (cambiarlo mueve el resultado)",
                  abs(u(80000, fallido=8000) - base) > 100))
    casos.append(("usa el CPA (cambiarlo mueve el resultado)",
                  abs(u(80000, cpa=0) - base) > 100))
    # La comision vigente es 0, asi que sabotearla a 0 no probaria nada: se sabotea al REVES,
    # poniendole el 4% que se retiro. Si esto no mueve el resultado, el termino esta muerto
    # y el dia que una transportadora cobre el recaudo por fuera nadie se enterara.
    casos.append(("el termino COMISION sigue VIVO (ponerle 4% mueve el resultado)",
                  abs(u(80000, comision=0.04) - base) > 100))
    casos.append(("la comision vigente es 0 y viene de 'medidos', no de un supuesto",
                  par["comision"] == 0))

    # --- con los numeros del CURSO el mismo producto parece viable: esa es la trampa ---
    curso = u(80000, p=0.75, flete=12000, fallido=8000, cpa=0, comision=0)
    casos.append((f"con los numeros del curso el producto malo 'pasa' (${curso:,.0f}) "
                  f"y con los de Golden no (${base:,.0f})",
                  curso >= par["piso"] and base < par["piso"]))

    # --- el multiplicador NO es constante: si alguien lo vuelve a clavar como cifra,
    #     esta prueba lo caza. Flete, fallido y CPA son FIJOS por pedido y no escalan. ---
    def mult(c):
        return pvp_minimo(c, par["piso"], par["p"], par["flete"], par["fallido"],
                          par["comision"], par["cpa"]) / c
    casos.append((f"el multiplicador NO es constante "
                  f"(costo 10k -> {mult(10000):.2f}x · 80k -> {mult(80000):.2f}x)",
                  mult(10000) > 6 and mult(80000) < 2))
    casos.append(("un producto barato a 5x su costo NO pasa (el error caro)",
                  u(50000, costo=10000) < par["piso"]))

    # --- la tabla que publica la skill, contra la formula. Los cuatro primeros los midio
    #     tambien el FILTRO por separado: dos caminos, un resultado. ---
    for c, esperado in ((10000, 7.02), (20000, 4.01), (30000, 3.01), (50000, 2.20)):
        casos.append((f"costo ${c:,} -> {esperado}x", abs(mult(c) - esperado) < 0.01))
    # el fallido inflado NO puede volver: exigia ~$6.258 de PVP de mas a cualquier costo
    m_malo = pvp_minimo(30000, par["piso"], par["p"], par["flete"], 29182,
                        par["comision"], par["cpa"])
    casos.append((f"el fallido retirado exigia ${m_malo - mult(30000)*30000:,.0f} de PVP de mas",
                  par["fallido"] == 12518 and 5900 < (m_malo - mult(30000)*30000) < 6100))
    # el CPA supuesto tampoco: se quedaba 53% corto y ABARATABA el minimo
    m_sup = pvp_minimo(30000, par["piso"], par["p"], par["flete"], par["fallido"],
                       par["comision"], 14000)
    casos.append((f"el CPA supuesto abarataba el minimo en ${mult(30000)*30000 - m_sup:,.0f}",
                  par["cpa"] == 21428 and (mult(30000) * 30000 - m_sup) > 9000))
    # 🔴 los DOS errores se compensaban: con los dos malos salia 2,99x y con los dos buenos
    #    3,13x. Arreglar solo uno habria EMPEORADO la regla creyendo que se mejoraba.
    #    Es un caso HISTORICO: se fija con los parametros de aquel dia, comision del 4%
    #    incluida. Calcularlo con la comision de hoy (0) daria otro numero y borraria
    #    la leccion sin que nadie se diera cuenta.
    m_ambos_malos = pvp_minimo(30000, par["piso"], par["p"], par["flete"], 29182,
                               0.04, 14000) / 30000
    m_bien_entonces = pvp_minimo(30000, par["piso"], par["p"], par["flete"], par["fallido"],
                                 0.04, par["cpa"]) / 30000
    casos.append((f"los dos errores se compensaban, con la comision de entonces "
                  f"({m_ambos_malos:.2f}x contra {m_bien_entonces:.2f}x)",
                  abs(m_ambos_malos - 2.99) < 0.01 and abs(m_bien_entonces - 3.13) < 0.01))
    # --- el AGUANTE de CPA: derivado, no inventado. A su PVP minimo tiene que aguantar
    #     exactamente el CPA medido, ni un peso mas. ---
    mn = mult(30000) * 30000
    aguante = par["p"] * (mn * (1 - par["comision"]) - 30000 - par["flete"]) \
        - (1 - par["p"]) * par["fallido"] - par["piso"]
    casos.append((f"en su PVP minimo aguanta justo el CPA medido (${aguante:,.0f})",
                  abs(aguante - par["cpa"]) < 2))

    print("  === AUTOPRUEBA · anclas medidas + sabotaje pieza por pieza ===")
    for nombre, bien in casos:
        ok += bien
        print(f"   {'OK ' if bien else '🔴 '} {nombre}")
    print(f"\n  {ok} de {len(casos)}")
    return 0 if ok == len(casos) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    # Todo como texto y leído con comun.numero(): "30.000" son treinta mil pesos, no $30 (el
    # verificador encontró que aquí era $30 y en correr_lote $30.000). NaN e inf no son números.
    for b in ("--costo", "--pvp", "--cpa", "--comision", "--entrega", "--piso"):
        ap.add_argument(b)
    ap.add_argument("--autoprueba", action="store_true")
    a = ap.parse_args()
    if a.autoprueba:
        sys.exit(autoprueba())
    if a.costo is None:
        ap.error("hace falta --costo (o --autoprueba)")
    for nombre in ("costo", "pvp", "cpa", "comision", "entrega", "piso"):
        crudo = getattr(a, nombre)
        if crudo is None:
            continue
        v = comun.numero(crudo, miles=nombre not in ("comision", "entrega"))
        if v is None:
            ap.error("--%s: %r no es un número" % (nombre, crudo))
        setattr(a, nombre, v)
    if a.costo <= 0:
        ap.error("--costo debe ser mayor que 0: sin costo del proveedor no hay PVP mínimo (regla 9)")
    if a.pvp is not None and a.pvp <= 0:
        ap.error("--pvp debe ser mayor que 0")
    if a.piso is not None and a.piso < 0:
        ap.error("--piso no puede ser negativo: un piso negativo aprueba productos que pierden plata")
    # Tasas como FRACCIÓN. Un 73.5 escrito como porcentaje daba un PVP mínimo de $24.705 y
    # --comision 4 daba un PVP NEGATIVO, sin error (verificador, 2026-09-18).
    for nombre, v, cero_ok in (("--entrega", a.entrega, False), ("--comision", a.comision, True)):
        if v is None:
            continue
        if v > 1:
            ap.error("%s va como fracción entre 0 y 1: %s parece un porcentaje (quizá quisiste %s)"
                     % (nombre, v, v / 100 if v <= 100 else "?"))
        if v < 0 or (v == 0 and not cero_ok):
            ap.error("%s fuera de rango: %s (entrega en (0, 1], comisión en [0, 1))" % (nombre, v))
    if a.comision is not None and a.comision >= 1:
        ap.error("--comision debe ser menor que 1: con 1 o más no existe precio que deje plata")
    for nombre, v in (("--costo", a.costo), ("--cpa", a.cpa), ("--pvp", a.pvp)):
        if v is not None and v < 0:
            ap.error("%s no puede ser negativo: %s" % (nombre, v))
    par = cargar()
    for k, v in (("cpa", a.cpa), ("comision", a.comision), ("p", a.entrega), ("piso", a.piso)):
        if v is not None:
            par[k] = v
    sys.exit(informe(a.costo, a.pvp, par))


if __name__ == "__main__":
    main()
