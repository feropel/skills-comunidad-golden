#!/usr/bin/env python3
"""Productor del embudo de Chatea para golden-logistica-diaria.

Toma el barrido fresco de contactos de Chatea y el volcado de Dropi, y produce:
  1. El archivo --embudo que consume generar_informe_diario.py (fuga = dieron
     todos los datos y NO hay orden en Dropi con ese telefono).
  2. La radiografia del embudo por etapa (Tablero), con el corte de HOY.
  3. La lista plana de contactos para --chatea (el cruce chat-vs-orden).

REGLA: cada cero dice de donde sale. Un contacto sin Tablero no se cuenta como
"saludo": se cuenta como "sin clasificar" y se declara.

  python3 embudo_chatea.py --contactos c.json --dropi v.json \
      --embudo-out e.json --chatea-out ch.json [--hoy 2026-08-10]
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json
from denominador import es_de_integracion, POR_QUE_SE_EXCLUYEN
from comun import tel10
from collections import Counter


def uf(c, name):
    for f in (c.get("user_fields") or []):
        if f.get("name") == name:
            return f.get("value")
    return None




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contactos", required=True)
    ap.add_argument("--dropi", required=True)
    ap.add_argument("--embudo-out", required=True)
    ap.add_argument("--chatea-out", required=True)
    ap.add_argument("--hoy", default=None)
    a = ap.parse_args()

    C = leer_json(a.contactos)
    contactos = C["contactos"] if isinstance(C, dict) else C
    contactos_brutos = list(contactos)   # antes de excluir, para la cobertura
    if isinstance(C, dict) and C.get("cosecha_completa") is not True:
        sys.exit("EMBUDO NO CONFIABLE: el barrido de contactos no dice cosecha_completa=true.")
    D = leer_json(a.dropi)
    if D.get("cosecha_completa") is not True:
        sys.exit("EMBUDO NO CONFIABLE: el volcado de Dropi no dice cosecha_completa=true.")

    # Telefonos con orden en Dropi (TODAS las ordenes, no solo accionables:
    # una venta de hace 3 dias que ya esta ENTREGADA sigue siendo orden).
    tel_dropi = {tel10(o.get("phone")) for o in D["ordenes"] if tel10(o.get("phone"))}

    # R13: EL DENOMINADOR NO SON TODOS LOS CONTACTOS.
    # Los que trae la integracion de Dropi (`opted_in_through == "dropi"`) NACEN de un
    # pedido que ya existe: nunca pasaron por el embudo del bot. Contarlos como si
    # hubieran entrado por el anuncio infla la base y hunde la conversion. Medido en
    # Golden: incluirlos movia la conversion de 68% a 32%.
    # La regla vive en `denominador.py`, no aqui. Este script y el analizador la
    # aplicaban por separado: uno excluia y el otro no, y el informe publicaba las dos
    # respuestas a la vez (10,44% contra 6,07%). Una regla de negocio con dos
    # implementaciones tiene dos versiones en cuanto alguien toca una.
    de_integracion = [c for c in contactos if es_de_integracion(c)]
    if de_integracion:
        contactos = [c for c in contactos if not es_de_integracion(c)]

    etapas = Counter()
    hoy_etapas = Counter()
    fuga, potenciales, saludo, sin_clasificar = [], [], [], 0
    for c in contactos:
        tab = uf(c, "Tablero") or ""
        tel = tel10(c.get("phone"))
        sub = (c.get("subscribed") or "")[:10]
        etapas[tab or "(sin Tablero)"] += 1
        if a.hoy and sub == a.hoy:
            hoy_etapas[tab or "(sin Tablero)"] += 1
        if not tab:
            sin_clasificar += 1

        direccion = (uf(c, "Dirección") or "").strip()
        ciudad = (uf(c, "Ciudad") or "").strip()
        productos = (uf(c, "Productos escogidos") or "").strip()
        datos_completos = bool(direccion and ciudad and productos)
        item = {"tel": tel, "nombre": c.get("name") or "",
                "ciudad": ciudad, "productos": productos,
                "ult": c.get("last_interaction") or c.get("subscribed"),
                "tablero": tab, "subscribed": sub}
        if datos_completos and tel and tel not in tel_dropi:
            fuga.append(item)
        elif tab.startswith("Cliente potencial"):
            potenciales.append(item)
        elif tab.startswith("Contacto inicial"):
            saludo.append(item)

    # sin_respuesta: la senal honesta que tenemos sin leer los chats uno a uno
    # es el tag de seguimiento "Aun no hay interaccion".
    sin_resp = sum(1 for c in contactos for t in (c.get("tags") or [])
                   if "no hay interacci" in str(t.get("name") if isinstance(t, dict) else t).lower())

    fuga.sort(key=lambda x: x.get("ult") or "", reverse=True)
    embudo = {
        "pedidos": len(contactos),          # universo barrido
        "revisados": len(contactos),        # todos pasaron por el clasificador
        "sin_respuesta": sin_resp,
        "fuga": len(fuga),
        "lista": fuga,
        # B4/B5: LA COBERTURA VIAJA CON EL DATO, no muere en el insumo. Antes el
        # informe decia "son TODOS los contactos" mientras el archivo de entrada
        # declaraba 218 nunca leidos. Aqui se RE-EMITE, para que quien reciba este
        # archivo pueda decir de cuantos habla — y para que no pueda decir "todos"
        # si no lo son.
        "excluidos_de_integracion": len(de_integracion),
        "_por_que_excluidos": POR_QUE_SE_EXCLUYEN,
        # EL DEFECTO NO AFIRMA COMPLETITUD. Aqui, cuando el insumo no traia cobertura,
        # se rellenaba con "universo == con_campos, sin_campos: 0" — o sea, se declaraba
        # una cosecha perfecta precisamente en el caso en que NO SE SABE nada. La nota
        # explicaba el apaño, pero quien lee el JSON (y el informe que lo consume) ve
        # tres numeros que dicen "no falto nadie". No saber y estar completo son estados
        # distintos y el archivo tiene que poder distinguirlos: `None` significa "no se
        # midio", y el informe ya sabe decir que no puede afirmar cobertura.
        # Y ANTES DE RENDIRSE, SE MIRA LO QUE EL INSUMO SI DECLARA. El archivo de
        # contactos trae `total` y `cosecha_completa` en su cabecera: con eso la
        # cobertura se puede construir. El informe llego a decir "no se declaro la
        # cobertura" mientras su propia tabla imprimia 900 — o sea, el dato estaba y
        # nadie lo leyo. Rendirse cuando falta el campo con MI nombre, teniendo el dato
        # con otro nombre al lado, es otra forma de no mirar.
        "_cobertura": (C.get("_cobertura") if isinstance(C, dict) else None) or (
            {"universo": C.get("total"), "con_campos": len(contactos_brutos),
             "sin_campos": max(0, (C.get("total") or 0) - len(contactos_brutos)),
             "declarada": True,
             "_nota": ("derivada de la cabecera del archivo de contactos: declara "
                       f"total={C.get('total')} y cosecha_completa="
                       f"{C.get('cosecha_completa')}")}
            if isinstance(C, dict) and C.get("total") else None) or {
            "universo": None, "con_campos": None, "sin_campos": None,
            "declarada": False,
            "_nota": "EL INSUMO NO DECLARO COBERTURA. No se sabe cuantos contactos tiene "
                     "el espacio ni de cuantos se leyeron los campos, asi que este informe "
                     "NO afirma que esten todos. Antes aqui se rellenaba con 'completo', "
                     "que convertia la ignorancia en una garantia"},
        "etapas": dict(etapas.most_common()),
        "hoy": a.hoy,
        "hoy_etapas": dict(hoy_etapas.most_common()),
        "potenciales": potenciales,
        "saludo": saludo,
        "sin_clasificar": sin_clasificar,
    }
    escribir_json(a.embudo_out, embudo, indent=1)
    escribir_json(a.chatea_out, contactos)
    print(f"excluidos por venir de la integracion de Dropi: {len(de_integracion)}")
    print(f"contactos: {len(contactos)} | fuga (venta sin orden): {len(fuga)} | "
          f"potenciales: {len(potenciales)} | en saludo: {len(saludo)} | "
          f"sin clasificar: {sin_clasificar} | sin respuesta (tag): {sin_resp}")
    if a.hoy:
        print(f"entraron HOY {sum(hoy_etapas.values())}: {dict(hoy_etapas)}")


if __name__ == "__main__":
    main()
