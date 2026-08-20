#!/usr/bin/env python3
"""
AUTOPRUEBA · golden-chatea-auditoria

Fabrica un espacio de Chatea que se SABE roto, con defectos sembrados uno por uno, y exige
que auditar.py los encuentre TODOS.

Por que existe: un auditor que sale en verde contra un espacio sano no prueba que el espacio
este sano, prueba que el auditor no mira. La higiene es al reves — si un script dice que todo
esta bien a la primera, lo primero que se sospecha es el script. Por eso el detector se prueba
contra un caso que se sabe malo ANTES de correrlo contra datos reales.

Uso:
    python3 autoprueba.py          # sale 0 si el auditor encuentra los N defectos
"""

import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from auditar import Auditoria                                    # noqa: E402


def producto(nombre, **cambios):
    """Un producto sano al que luego se le siembra el defecto que toque."""
    p = {
        "informacion_de_producto": {
            "id": "111", "nombre": nombre, "precio": "74900", "moneda": "COP",
            "id_dropi": "111", "tipo": "fisico", "variable": "SIMPLE",
            "imagen": "https://media.chateapro.app/temp/202607/236245/x_1",
            "estado": "activo", "dta_prompt": "",
        },
        "embudo_de_ventas": {
            "mensaje_inicial": "Hola, bienvenido a la empresa",
            "multimedia": ["https://media.chateapro.app/temp/202607/236245/v_1"],
            "pregunta_de_entrada": "Cuentame una cosa para asesorarte mejor",
        },
        "prompt": {"tipo_de_prompt": "libre", "prompt_libre": "Prompt sano. " * 20},
        "voz_con_ia": {"proveedor": "chatea_pro", "id": "v1", "api_key": "",
                       "habilitar": "no"},
        "recordatorios": {"activar_1": "si", "tiempo_1": "2 horas",
                          "mensaje_1": "Recordatorio. " * 40},
        "remarketing": {"activar_1": "si", "prompt_1": "Remarketing. " * 30},
        "activadores_del_flujo": {
            "palabras_clave": f"Hola quiero informacion y precio de {nombre},,,,,,",
            "ids_de_anuncio": "1234567890,,,,,,"},
        "meta_conversion": {"habilitado": True},
        "upsells": {},
    }
    p.update(cambios)
    return p


def campo(nombre, valor, tipo="array"):
    return {"name": nombre, "var_ns": "f999999v1", "var_type": tipo,
            "description": "", "is_template_field": "False",
            "value": valor if isinstance(valor, str)
            else json.dumps(valor, ensure_ascii=False)}


def espacio_roto():
    """Un DUMP con 18 defectos sembrados. Cada uno esta comentado con su control."""
    campos = []
    disparador = []

    # --- producto 1: SANO y bien registrado (el control negativo del auditor)
    campos.append(campo("[Producto Ventas Wp] 1", producto("SANO")))
    disparador.append({"producto": "SANO", "name": "[Producto Ventas Wp] 1",
                       "keyW": "Hola quiero informacion y precio de SANO,,,,,,",
                       "idAd": "1234567890,,,,,,", "estado": "activo"})

    # --- D1: la palabra clave difiere en UN ACENTO entre sus dos sitios
    campos.append(campo("[Producto Ventas Wp] 2", producto("ACENTO")))
    disparador.append({"producto": "ACENTO", "name": "[Producto Ventas Wp] 2",
                       "keyW": "Hola quiero información y precio de ACENTO,,,,,,",
                       "idAd": "999,,,,,,", "estado": "activo"})

    # --- D2: emoji (4 bytes) en el disparador · D5: ranuras mal contadas
    campos.append(campo("[Producto Ventas Wp] 3", producto("EMOJI")))
    disparador.append({"producto": "EMOJI", "name": "[Producto Ventas Wp] 3",
                       "keyW": "Quiero el producto 🔥,,",
                       "idAd": ",,,,,,", "estado": "activo"})

    # --- D3: cargado y HUERFANO (sin entrada en el disparador)
    campos.append(campo("[Producto Ventas Wp] 4", producto("HUERFANO")))

    # --- D3: entrada del disparador que apunta a un campo que no existe
    disparador.append({"producto": "FANTASMA", "name": "[Producto Ventas Wp] 44",
                       "keyW": "fantasma,,,,,,", "idAd": ",,,,,,", "estado": "activo"})

    # --- D4: estado incoherente · D6: activo sin ningun idAd
    p5 = producto("ESTADO")
    p5["informacion_de_producto"]["estado"] = "inactivo"
    campos.append(campo("[Producto Ventas Wp] 5", p5))
    disparador.append({"producto": "ESTADO", "name": "[Producto Ventas Wp] 5",
                       "keyW": "Hola quiero informacion y precio de ESTADO,,,,,,",
                       "idAd": ",,,,,,", "estado": "activo"})

    # --- E3: credencial de voz heredada · F6: multimedia como cadena
    # --- F5: precio que no es numero limpio · C3: prompt_libre sobre su tope nativo
    p6 = producto("FUGAS")
    p6["voz_con_ia"]["api_key"] = "sk_" + "a" * 45
    p6["voz_con_ia"]["habilitar"] = "si"
    p6["embudo_de_ventas"]["multimedia"] = "https://una-sola-url-como-cadena"
    p6["informacion_de_producto"]["precio"] = "74.900 COP"
    p6["prompt"]["prompt_libre"] = "L" * 12_500
    campos.append(campo("[Producto Ventas Wp] 6", p6))
    disparador.append({"producto": "FUGAS", "name": "[Producto Ventas Wp] 6",
                       "keyW": "Hola quiero informacion y precio de FUGAS,,,,,,",
                       "idAd": "1,,,,,,", "estado": "activo"})

    # --- F7: imagen de OTRA cuenta de Chatea. La cuenta propia se declara en /team-info
    # como 236245, asi que 999888 es heredada aunque fuera la unica del espacio.
    p7 = producto("OTRACUENTA")
    p7["informacion_de_producto"]["imagen"] = \
        "https://media.chateapro.app/temp/202607/999888/ajeno_1"
    campos.append(campo("[Producto Ventas Wp] 7", p7))
    disparador.append({"producto": "OTRACUENTA", "name": "[Producto Ventas Wp] 7",
                       "keyW": "Hola quiero informacion y precio de OTRACUENTA,,,,,,",
                       "idAd": "2,,,,,,", "estado": "activo"})

    # --- G3/G1: credencial EN CLARO dentro de un campo con nombre inocente.
    # Buscar por nombre de campo no la veia. Es la clase que dejo llaves en un DUMP.
    campos.append(campo("[Integraciones] Datos de integracion",
                        {"dropi": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghij",
                         "openai": "sk-proj-" + "A" * 40,
                         "meta": "EAA" + "B" * 50}, "array"))

    # --- E2 a profundidad 1 y a profundidad 3: el bucle viejo solo veia la 2
    campos.append(campo("[Carritos] Configuracion",
                        {"activar_ia": "no", "prompt": "P" * 7000}, "array"))
    campos.append(campo("[Novedades] Mensajes por tipo de novedad",
                        {"g": {"sub": {"evaluar_novedad": "no",
                                       "prompt": "N" * 7000}}}, "array"))

    # --- D5/D3: entrada de disparador SIN producto detras (el bucle viejo la saltaba)
    #     y una entrada con el destino vacio
    segundo = [
        {"producto": "RANURA QUE NO EXISTE", "name": "[Producto Ventas Wp] 28",
         "keyW": "solo,dos", "idAd": "x", "estado": "activo"},
        {"producto": "SIN DESTINO", "name": "", "keyW": "cla, , , , , , ",
         "idAd": ",,,,,,", "estado": "activo"},
    ]
    campos.append(campo("[Remarketing IA] Disparador de productos", segundo, "array"))

    campos.append(campo("[Ventas Wp] Disparador de productos Extendido",
                        disparador, "longtext"))

    # --- C1: por ENCIMA del techo escapado (muerto, no dispara)
    campos.append(campo("[Comentarios] Configuracion General",
                        {"texto": "á" * 9_000}, "array"))

    # --- C2: al 95% del techo escapado (muerte anunciada)
    campos.append(campo("[Logistico] Configuracion General",
                        {"texto": "x" * 18_400}, "array"))

    # --- C5: par poblado de los DOS lados
    campos.append(campo("[Comentarios] Productos", {"p": ["uno"]}, "array"))
    campos.append(campo("[Comentarios] Productos extendido", {"p": ["dos"]}, "longtext"))

    # --- C6: declarado array y NO parsea (patron de truncada silenciosa)
    campos.append(campo("[Carritos IA] Informacion de productos #1",
                        '{"cortado": "esto se corto por la mit', "array"))

    # --- E2: interruptor APAGADO gobernando contenido lleno
    campos.append(campo("[Logistico] Confirmaciones",
                        {"analisis_direccion": {"evaluar_direccion": "no",
                                                "prompt": "P" * 7_243}}, "array"))

    # --- F1 mojibake · F2 signos de apertura · F3 marcador sin reemplazar
    campos.append(campo("[Ventas Wp] Configuracion general",
                        {"rol": "La asesora se llama MarÃ­a. ¿Como te ayudo? "
                                "Escribe a {{WHATSAPP}}"}, "array"))

    # --- G3: credencial guardada como valor de un campo
    campos.append(campo("TOKEN DROPI", "d" * 491, "text"))

    # --- A3: el pais dice MEXICO y todos los productos estan en COP (plantilla clonada)
    campos.append(campo("[Comentarios IA] Pais", "MEXICO", "text"))

    return {
        "_etiqueta": "AUTOPRUEBA-espacio-roto",
        "_extraido": "2026-01-01T00:00:00",
        "_conteos": {"/flow/bot-fields": {"traidos": len(campos),
                                          # B1: el servidor declara uno mas del que trajimos
                                          "declarados_por_servidor": len(campos) + 1},
                     # B1b: un listado que NO es el de campos tambien llego corto
                     "/flow/user-fields": {"traidos": 350,
                                           "declarados_por_servidor": 423}},
        "/me": {"id": 1, "name": "Autoprueba", "email": "autoprueba@local"},
        "/flow/bot-fields": campos,
        "/flow/user-fields": [],
        # I3: zona extraida que ningun control mira (aqui, los subflujos)
        "/flow/subflows": [{"ns": "f999999s1", "name": "un subflujo"}],
        # G1/G2: el payload real viene ANIDADO bajo `data`. Mirar solo el primer nivel
        # devolvia CERO credenciales teniendo seis. El falso negativo se siembra aqui.
        "/integration/shopify": {"data": {"url": "una-tienda-ajena.myshopify.com",
                                          "token": "<<REDACTADO len=38>>",
                                          "status": "verified"}, "status": "ok"},
        "/integration/openai": {"data": {"api_key": "<<REDACTADO len=164>>",
                                         "status": "verified"}, "status": "ok"},
        # A4: un canal caido, que el control viejo no miraba (solo veia si el dict existia)
        "/workspace-settings/channels": {"whatsapp": True, "facebook": "expired"},
        # F7: la cuenta propia sale del servidor, no de suponer cual es la mayoritaria
        "/team-info": {"data": {"id": 236245, "name": "Autoprueba"}},
        # F13: zona extraida que antes no auditaba nadie
        "_tareas_detalle": {"f999999at1": {"task_prompt": "¿Como te ayudo? Mira "
                                                          "https://ejemplo.com/rojo.jpg"}},
    }


# Cada defecto sembrado, con el control que TIENE que dispararlo.
ESPERADOS = {
    "B1": "la paginacion no cuadra con el total del servidor",
    "C1": "campo por encima del techo escapado",
    "C2": "campo al 95% del techo escapado",
    "C3": "prompt_libre sobre su tope nativo del formulario",
    "C4": "array grande que deberia ser longtext",
    "C5": "par array/Extendido poblado de los dos lados",
    "C6": "valor declarado array que no parsea",
    "D1": "palabra clave que difiere en un acento",
    "D2": "emoji de 4 bytes en el disparador",
    "D3": "producto huerfano y entrada al vacio",
    "D4": "estado incoherente entre producto y disparador",
    "D5": "ranuras del disparador mal contadas",
    "D6": "producto activo sin ningun id de anuncio",
    "E2": "interruptor apagado con contenido cargado",
    "E3": "credencial de voz heredada",
    "F1": "codificacion rota (mojibake)",
    "F2": "signos de apertura",
    "F3": "marcador de posicion sin reemplazar",
    "F5": "precio que no es un numero limpio",
    "F6": "multimedia escrita como cadena",
    "F7": "imagenes de mas de una cuenta",
    "G1": "credenciales en las integraciones",
    "G2": "la integracion de Shopify apunta a un dominio ajeno",
    "G3": "credencial guardada como valor de un campo",
    "A3": "pais declarado que no concuerda con la moneda de los productos",
    "A4": "un canal caido o desconectado",
    "F13": "signos de apertura y marcador dentro de las tareas de IA",
    "I3": "zonas del DUMP que no mira ningun control",
    "B3": "campos que no pertenecen a ningun asistente",
}


def main():
    print("AUTOPRUEBA · fabricando un espacio que se SABE roto\n")
    dump = espacio_roto()
    a = Auditoria(dump).correr()

    disparados = {h["control"] for h in a.hallazgos}
    faltan = [c for c in ESPERADOS if c not in disparados]
    sobran = disparados - set(ESPERADOS)

    for c, desc in ESPERADOS.items():
        marca = "OK  " if c in disparados else "FALLA"
        print(f"  {marca}  {c:4} {desc}")

    if sobran:
        print(f"\n  Ademas disparo (no sembrado, revisar si es falso positivo): {sorted(sobran)}")

    print(f"\n  {len(ESPERADOS) - len(faltan)} de {len(ESPERADOS)} defectos sembrados "
          f"fueron detectados")

    # El producto 1 esta sano: si el auditor lo acusa, tiene un falso positivo.
    falsos = [h for h in a.hallazgos if "[Producto Ventas Wp] 1`" in h["evidencia"]
              or h["titulo"].endswith("[Producto Ventas Wp] 1")]
    if falsos:
        print(f"  AVISO: {len(falsos)} hallazgos contra el producto SANO (falso positivo)")

    if faltan:
        print(f"\nAUTOPRUEBA FALLIDA · el auditor NO detecta: {faltan}")
        print("El auditor esta roto. No se corre contra datos reales hasta arreglarlo.")
        return 1

    print("\nAutoprueba pasada: el auditor detecta los defectos sembrados.")
    print("Esto valida el DETECTOR, no valida ningun espacio real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
