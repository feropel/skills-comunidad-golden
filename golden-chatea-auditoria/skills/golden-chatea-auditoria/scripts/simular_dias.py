#!/usr/bin/env python3
"""
SIMULADOR DE DIAS · golden-chatea-auditoria

Corre el ciclo de vigilancia sobre un espacio que EVOLUCIONA dia a dia, en vez de esperar a
que pasen los dias de verdad. Cada dia aplica un evento que ocurre en la vida real de un
espacio de Chatea (alguien edita desde el panel, se enciende pauta, se reinstala un asistente,
la API falla) y verifica que el auditor reaccione como debe.

POR QUE EXISTE: el modo "propuesta con aprobacion" del ciclo 360 se valida dejandolo correr
unos dias reales. Eso cuesta dias y descubre los fallos EN PRODUCCION. Simularlos cuesta
minutos y los descubre antes de escribir la primera linea del orquestador.
Hallazgo que lo justifico: `reabrir_si` era prosa que NADIE evaluaba — una decision quedaba
silenciada para siempre aunque su condicion de reapertura se cumpliera. Se descubrio aqui.

Los fixtures se generan con codigo, no a mano: es mas barato, produce dias de verdad y no saca
datos del negocio mientras el ciclo todavia se esta moviendo.

Uso:
    python3 simular_dias.py            # corre los dias y dice cuales fallan
    python3 simular_dias.py --detalle  # ademas imprime los hallazgos de cada dia
"""

import copy
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from auditar import Auditoria                                    # noqa: E402
from autoprueba import campo, producto                           # noqa: E402


# --------------------------------------------------------------------- el espacio inicial
def dia_cero():
    """Un espacio SANO. Los defectos los va metiendo la vida, dia a dia."""
    prods, disparador, campos = {}, [], []
    for i, (nombre, ads) in enumerate(
            [("ESTRELLA", "111,,,,,,"), ("SEGUNDO", "222,,,,,,"),
             ("BORRADOR", ",,,,,,")], start=1):
        p = producto(nombre)
        p["activadores_del_flujo"]["ids_de_anuncio"] = ads
        prods[i] = p
        campos.append(campo(f"[Producto Ventas Wp] {i}", p))
        if nombre != "BORRADOR":            # el borrador nace fuera del disparador, a proposito
            disparador.append({"producto": nombre, "name": f"[Producto Ventas Wp] {i}",
                               "keyW": f"Hola quiero informacion y precio de {nombre},,,,,,",
                               "idAd": ads, "estado": "activo"})
    campos.append(campo("[Ventas Wp] Disparador de productos Extendido",
                        disparador, "longtext"))
    campos.append(campo("[Comentarios] Configuracion General", {"texto": "ok"}, "array"))
    campos.append(campo("[Ventas Wp] Configuracion general", {"rol": "Asesora Valentina"}))
    campos.append(campo("[Logistico] Configuracion General", {"t": "ok"}))
    campos.append(campo("[Logistico] Confirmaciones", {"c": "ok"}))
    campos.append(campo("[Carritos] Configuracion", {"c": "ok"}))
    campos.append(campo("[Comentarios IA] Tipo de actividad", "1", "text"))
    return {
        "_etiqueta": "simulacion", "_extraido": "2026-09-01T08:00:00",
        "_conteos": {"/flow/bot-fields": {"traidos": len(campos),
                                          "declarados_por_servidor": len(campos)}},
        "/me": {"id": 1, "email": "tienda@ejemplo"},
        "/team-info": {"data": {"id": 236245}},
        "/flow/bot-fields": campos,
        "/flow/user-fields": [],
        "/workspace-settings/channels": {"data": {"whatsapp": 1, "whatsapp_cloud": 1,
                                                  "facebook": 1, "instagram": 1}},
    }


# ------------------------------------------------------------------ utilidades de edicion
def campo_de(dump, nombre):
    for c in dump["/flow/bot-fields"]:
        if c["name"] == nombre:
            return c
    raise KeyError(nombre)


def edita(dump, nombre, fn):
    c = campo_de(dump, nombre)
    v = json.loads(c["value"])
    fn(v)
    c["value"] = json.dumps(v, ensure_ascii=False)


def resellar(dump, fecha):
    dump["_extraido"] = fecha
    n = len(dump["/flow/bot-fields"])
    dump["_conteos"]["/flow/bot-fields"] = {"traidos": n, "declarados_por_servidor": n}
    return dump


# ------------------------------------------------------------------------------ los dias
def dias():
    """Cada dia: (titulo, funcion que edita el espacio, que se espera, como se comprueba)."""

    def d1(dump):
        """Se enciende pauta al BORRADOR sin registrarlo en el disparador."""
        edita(dump, "[Producto Ventas Wp] 3",
              lambda v: v["activadores_del_flujo"].update(ids_de_anuncio="333,,,,,,"))

    def d2(dump):
        """Nada cambia: el dueno esta pensando la decision."""

    def d3(dump):
        """Alguien edita desde el panel y CORTA el campo de Comentarios."""
        campo_de(dump, "[Comentarios] Configuracion General")["value"] = '{"texto": "ok'

    def d4(dump):
        """Se repara el corte, y de paso el campo crece hasta cruzar el techo."""
        edita_ = campo_de(dump, "[Comentarios] Configuracion General")
        edita_["value"] = json.dumps({"texto": "á" * 9000}, ensure_ascii=False)

    def d5(dump):
        """Se compacta el campo y se borra un campo que un flujo podria referenciar."""
        edita(dump, "[Comentarios] Configuracion General",
              lambda v: v.update(texto="compactado"))
        dump["/flow/bot-fields"] = [c for c in dump["/flow/bot-fields"]
                                    if c["name"] != "[Carritos] Configuracion"]

    def d6(dump):
        """La API falla al traer los campos de usuario."""
        dump["/flow/user-fields"] = {"_ERROR_HTTP": 500, "_detalle": "server error"}

    def d7(dump):
        """Vuelve la API. Se le enciende pauta a OTRO producto que tampoco esta registrado.

        OJO CON COMO SE PRUEBA ESTO: la primera version del dia 7 REGISTRABA el producto
        decidido, con lo cual el hallazgo desaparecia y la comprobacion pasaba por una via
        que no probaba nada — con el arreglo de la caducidad SABOTEADO, el dia 7 seguia en
        verde. Un banco que se auto-aprueba es peor que no tener banco. Ahora el hallazgo
        SIGUE existiendo y solo cambia su EVIDENCIA (ya son dos productos, no uno), asi que
        la unica forma de pasar es que la decision caduque de verdad.
        """
        dump["/flow/user-fields"] = []
        nuevo = producto("TARDIO")
        nuevo["activadores_del_flujo"]["ids_de_anuncio"] = "444,,,,,,"
        dump["/flow/bot-fields"].append(campo("[Producto Ventas Wp] 4", nuevo))

    return [
        ("D1 · se enciende pauta a un producto que NO esta en el disparador", d1,
         "un rojo por producto con pauta fuera del disparador",
         lambda a: any(h["clave"] == "D3|huerfanos-con-pauta" and h["severidad"] == "MUERTO"
                       for h in a.hallazgos)),
        ("D2 · el dueno decide: 'lo registro la semana que viene'", d2,
         "el hallazgo queda SILENCIADO por el libro",
         lambda a: any(h.get("severidad") == "DECIDIDO" for h in a.hallazgos)),
        ("D3 · alguien corta el campo desde el panel", d3,
         "truncada silenciosa detectada (C6)",
         lambda a: any(h["control"] == "C6" for h in a.hallazgos)),
        ("D4 · el campo se repara pero cruza el techo", d4,
         "aviso de que el campo CRUZO el techo entre corridas",
         lambda a: any("CRUZO el techo" in h["titulo"] for h in a.hallazgos)),
        ("D5 · se compacta, y se BORRA un campo", d5,
         "el diff nombra el campo borrado",
         lambda a: any(t == "BORRADO" for t, _, _ in a.cambios)),
        ("D6 · la API falla al traer los campos de usuario", d6,
         "la zona se declara sin medir y la auditoria SIGUE",
         lambda a: any(h["clave"].startswith("B1|ilegible") for h in a.hallazgos)),
        ("D7 · aparece OTRO huerfano con pauta: la decision del D2 debe CADUCAR", d7,
         "la decision caduca y el hallazgo VUELVE a contar (no basta con que desaparezca)",
         lambda a: bool(a._reabiertos)
         and any(h.get("decision_caduca") for h in a.hallazgos)),
    ]


# ---------------------------------------------------------------------------------- run
def main():
    detalle = "--detalle" in sys.argv
    dump = dia_cero()
    anterior = copy.deepcopy(dump)
    decisiones = {}
    fallos = []

    print("SIMULACION DE DIAS · el ciclo corrido sobre un espacio que cambia\n")
    for n, (titulo, evento, esperado, comprueba) in enumerate(dias(), start=1):
        evento(dump)
        resellar(dump, f"2026-09-{n + 1:02d}T08:00:00")

        a = Auditoria(copy.deepcopy(dump))
        a.decisiones = dict(decisiones)
        a.correr()
        a.comparar(anterior)

        ok = False
        try:
            ok = bool(comprueba(a))
        except Exception as e:                                    # noqa: BLE001
            print(f"  REVIENTA en {titulo}: {type(e).__name__}: {e}")
        marca = "OK   " if ok else "FALLA"
        if not ok:
            fallos.append(titulo)
        print(f"  {marca} {titulo}")
        print(f"        esperado: {esperado}")
        if detalle:
            for h in a.hallazgos[:6]:
                print(f"           · {h['severidad']:9} {h['control']} {h['titulo'][:70]}")

        # El dueno decide al final del dia 1, con la evidencia de ESE dia.
        if n == 1:
            hu = [h for h in a.hallazgos if h["clave"] == "D3|huerfanos-con-pauta"]
            if hu:
                decisiones["D3|huerfanos-con-pauta"] = {
                    "motivo": "lo registro la semana que viene",
                    "fecha": "2026-09-02",
                    "reabrir_si": "se registra en el disparador o cambia su pauta",
                    "evidencia_al_decidir": hu[0]["evidencia"]}

        anterior = copy.deepcopy(dump)

    print(f"\n  {len(dias()) - len(fallos)} de {len(dias())} dias se comportaron como debian")
    if fallos:
        print("\nDIAS QUE FALLARON:")
        for f in fallos:
            print(f"  · {f}")
        print("\nEl ciclo NO esta listo para correr solo. Arreglar antes de construir el 360.")
        return 1
    print("\nLos dias simulados se comportaron como debian. Esto valida el CICLO sobre un")
    print("espacio fabricado, no valida ningun espacio real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
