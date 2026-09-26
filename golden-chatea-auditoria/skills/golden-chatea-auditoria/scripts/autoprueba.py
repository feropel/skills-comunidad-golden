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

import re
import json
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

    # --- D3: cargado y HUERFANO **CON** anuncios cargados = plata de pauta que no
    # convierte (el default de producto() trae ids_de_anuncio)
    campos.append(campo("[Producto Ventas Wp] 4", producto("HUERFANO")))

    # --- D3: huerfano SIN anuncios = no cuesta nada hoy. La severidad la decide el
    # negocio, no la estructura: este NO puede salir en rojo.
    p8 = producto("HUERFANO SIN PAUTA")
    p8["activadores_del_flujo"]["ids_de_anuncio"] = ",,,,,,"
    campos.append(campo("[Producto Ventas Wp] 8", p8))

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
    # El api_key va REDACTADO (`<<REDACTADO...>>`), la forma REAL en la que llega a este
    # script: extraer.py ya lo redacto por patron de valor antes de que auditar.py vea el
    # DUMP. Un fixture con la llave en claro (como antes) solo probaba una forma que el
    # propio auditor real nunca recibe.
    p6 = producto("FUGAS")
    p6["voz_con_ia"]["api_key"] = "<<REDACTADO ElevenLabs len=48>>"
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
    # --- ESTADO: una entrada APAGADA no puede estar MUERTA. Caso real medido en Golden el
    # 2026-08-25: 4 de las 5 entradas del disparador de Remarketing estaban `inactivo` y el
    # auditor las grito en rojo igual. La de abajo esta inactiva y con la clave vacia: tiene
    # que salir DUDA, no MUERTO. La de arriba (28) esta activa y si es roja.
    segundo.append({"producto": "APAGADA", "name": "[Producto Ventas Wp] 33",
                    "keyW": ",,,,,,", "idAd": ",,,,,,", "estado": "inactivo"})
    # Hasta el 2026-09-24 este segundo disparador se llamaba `[Remarketing IA] ...` (el caso
    # real). FER saco Remarketing del ecosistema y el auditor ya no lo ve, asi que el sabotaje
    # se muda a un nombre que SI se audita: si no, D3b dejaba de tener banco sin avisar.
    campos.append(campo("[Ventas Wp] Disparador de productos", segundo, "array"))

    campos.append(campo("[Ventas Wp] Disparador de productos Extendido",
                        disparador, "longtext"))

    # --- C1: por ENCIMA del techo escapado (muerto, no dispara)
    campos.append(campo("[Comentarios] Configuracion General",
                        {"texto": "á" * 9_000}, "array"))

    # --- C2: al 95% del techo escapado (muerte anunciada)
    # --- L5: un campo de configuracion REAL que el esquema de referencia no cubre. La
    # skill hermana del logistico lo configura; el esquema del auditor solo conoce 2 de sus
    # 9 campos. Sin L5 este campo se salta en silencio y la cobertura no lo confiesa.
    campos.append(campo("[Logistico] Seguimiento",
                        {"guia_generada": {"activo": "si", "mensaje": "x" * 200}}))

    campos.append(campo("[Logistico] Configuracion General",
                        {"texto": "x" * 18_400}, "array"))

    # --- C5: par poblado de los DOS lados
    campos.append(campo("[Comentarios] Productos", {"p": ["uno"]}, "array"))
    campos.append(campo("[Comentarios] Productos extendido", {"p": ["dos"]}, "longtext"))

    # --- C6: declarado array y NO parsea (patron de truncada silenciosa)
    campos.append(campo("[Carritos IA] Informacion de productos #1",
                        '{"cortado": "esto se corto por la mit', "array"))

    # --- E2: interruptor APAGADO gobernando contenido lleno
    # --- B8: el MISMO asistente escrito de dos formas. Las dos variantes estan en el
    # catalogo de prefijos del auditor, asi que B3 no las ve: ese es justo el punto.
    # Medido el 2026-09-05 en los DOS espacios auditados hasta entonces, de dos paises:
    # los dos traen [Logistico]/[Logistico con tilde] y [WhatsApp IA]/[Whatsapp IA].
    campos.append(campo("[Log\u00edstico] Novedades", "{}"))

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

    # --- F3 clase: hueco de editor dentro de un producto ACTIVO. Caso REAL medido en Golden
    # el 2026-08-22: un producto vendiendo llevaba el corchete en pleno paso de cobro y la
    # lista de placeholders conocidos no lo veia. El de minusculas ([total]) NO debe disparar.
    p9 = producto("HUECOS")
    p9["prompt"]["prompt_libre"] = (
        "Envia los datos de pago [AQUI VAN LOS DATOS DE PAGO ANTICIPADO: Nequi + titular] "
        "y el valor $[total] al cliente. Foto: [IMAGEN 1 — URL]")
    campos.append(campo("[Producto Ventas Wp] 9", p9))
    disparador.append({"producto": "HUECOS", "name": "[Producto Ventas Wp] 9",
                       "keyW": "Hola quiero informacion y precio de HUECOS,,,,,,",
                       "idAd": "9,,,,,,", "estado": "activo"})

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
        # 🔴 F14 va AQUI, con los campos — mi primera version lo metio entre los ENDPOINTS
        # del dump y por eso el control no lo veia. El banco sembraba en un sitio donde el
        # auditor no mira, y el informe decia "el auditor NO detecta F14" acusando al control.
        # Un fallo del banco y un fallo de la herramienta se ven IGUAL desde fuera.
        "/flow/bot-fields": campos + list(_campo_de_fabrica().values()),
        "/flow/user-fields": [],
        # I3: zona extraida que NINGUN control mira. custom-events no lo audita nadie: tiene
        # que seguir apareciendo como sin cubrir. subflows/segments/agents SI tienen control
        # (B4 los cuenta) y NO deben aparecer aqui: es la regresion del bug de la lista
        # `auditadas` desincronizada de lo que B4 realmente audita.
        "/flow/custom-events": [{"name": "un_evento"}],
        "/flow/subflows": [{"ns": "f999999s1", "name": "un subflujo"}],
        "/flow/segments": [{"ns": "f999999sg1", "name": "un segmento"}],
        "/flow/agents": [{"ns": "f999999ag1", "name": "un agente"}],
        # G1/G2: el payload real viene ANIDADO bajo `data`. Mirar solo el primer nivel
        # devolvia CERO credenciales teniendo seis. El falso negativo se siembra aqui.
        "/integration/shopify": {"data": {"url": "una-tienda-ajena.myshopify.com",
                                          "token": "<<REDACTADO len=38>>",
                                          "status": "verified"}, "status": "ok"},
        "/integration/openai": {"data": {"api_key": "<<REDACTADO len=164>>",
                                         "status": "verified"}, "status": "ok"},
        # A4: la FORMA REAL del endpoint (medida contra un espacio en produccion): enteros
        # anidados bajo `data`, no booleanos ni strings "connected"/"active" en la raiz. El
        # control viejo solo reconocia esa segunda forma inventada, que ningun canal real usa
        # -- lo unico que le disparaba era el `status:"ok"` del sobre HTTP. whatsapp=1 conectado,
        # facebook=0 caido.
        "/workspace-settings/channels": {"data": {"whatsapp": 1, "facebook": 0,
                                                   "instagram": 1}, "status": "ok"},
        # F7: la cuenta propia sale del servidor, no de suponer cual es la mayoritaria
        "/team-info": {"data": {"id": 236245, "name": "Autoprueba"}},
        # F13: zona extraida que antes no auditaba nadie
        "_tareas_detalle": {"f999999at1": {"task_prompt": "¿Como te ayudo? Mira "
                                                          "https://ejemplo.com/rojo.jpg"},
                            # F13cob: dos objetos SIN una sola cadena. Asi llegan los
                            # `locked` que el extractor no puede abrir. No son un defecto
                            # del espacio: son un limite de la LECTURA, y engordaban el
                            # denominador que F13 declaraba como "revisado".
                            "f999999at2": {"locked": True, "id": 2},
                            "f999999at3": {}},
    }


def _campo_de_fabrica():
    """Devuelve {nombre: campo} con UN valor de fabrica REAL, sacado de la huella medida.

    🔴 No se inventa el valor. Si se inventara, la prueba comprobaria que el auditor reconoce
    una cadena de mentira, no la plantilla que la plataforma instala de verdad. Si la huella no
    esta disponible, se devuelve vacio y el caso F14 se declara NO SEMBRADO en vez de dar un
    verde que no probo nada."""
    import os as _os
    ruta = _os.path.expanduser("~/.claude/skills/golden-chatea-pro-config-logistico/"
                               "assets/plantilla-fabrica.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            a = json.load(f)
        nombre, valor = next(iter(a["valores_del_logistico"].items()))
        return {nombre: {"name": nombre, "var_ns": "fab1", "var_type": "text", "value": valor}}
    except Exception:
        return {}


# Cada defecto sembrado, con el control que TIENE que dispararlo.
ESPERADOS = {
    "L5": "campo de configuracion que el esquema de referencia no cubre",
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
    "A4": "un canal REQUERIDO no disponible (y apple=0 NO debe disparar)",
    "F13": "signos de apertura y marcador dentro de las tareas de IA",
    "F14": "un campo identico a la PLANTILLA DE FABRICA (parece configurado, no lo esta)",
    "I3": "zonas del DUMP que no mira ningun control",
    "B3": "campos que no pertenecen a ningun asistente",
    "B6": "asistentes esperados que NO estan instalados",
    "B8": "el mismo asistente escrito de dos formas (variante con tilde)",
}


def main():
    print("AUTOPRUEBA · fabricando un espacio que se SABE roto\n")
    dump = espacio_roto()
    a = Auditoria(dump, alcance="todo").correr()

    disparados = {h["control"] for h in a.hallazgos}
    faltan = [c for c in ESPERADOS if c not in disparados]
    sobran = disparados - set(ESPERADOS)

    for c, desc in ESPERADOS.items():
        marca = "OK  " if c in disparados else "FALLA"
        print(f"  {marca}  {c:4} {desc}")

    if sobran:
        print(f"\n  Ademas disparo (no sembrado, revisar si es falso positivo): {sorted(sobran)}")

    # --- prueba PRIV: la skill guarda el ESTANDAR, no a los clientes (ley de FER,
    # 2026-09-05). Corre el guardia de privacidad sobre la skill entera: identificadores de
    # espacio, dominios de tienda, correos, telefonos y credenciales. Va DENTRO del banco
    # porque una regla que solo vive en el SKILL.md la incumple el proximo que edite.
    import subprocess
    guardia = subprocess.run(
        ["python3", str(Path(__file__).resolve().parent / "sin_datos_de_cliente.py")],
        capture_output=True, text=True)
    if guardia.returncode == 0:
        print("  OK    PRIV la skill no lleva datos de ningun espacio, cliente ni persona")
    else:
        print("  FALLA PRIV el guardia de privacidad encontro datos que no deberian estar:")
        for linea in guardia.stdout.splitlines():
            if linea.strip().startswith(("references/", "scripts/", "assets/", "SKILL.md")):
                print(f"        {linea.strip()}")
        faltan.append("datos-de-cliente-en-la-skill")

    # --- prueba L5: declarar lo que NO se juzgo. El bloque L salta los campos que no
    # estan en el esquema; el hallazgo tiene que NOMBRARLOS, porque "reviso 4" sin decir
    # "se salto 1" es exactamente la cobertura falsa que esta skill persigue.
    l5 = [h for h in a.hallazgos if h["control"] == "L5"]
    nombra = any("[Logistico] Seguimiento" in (h["evidencia"] + h["titulo"]) for h in l5)
    cob_l5 = [c for c in a.cobertura if c["control"] == "L5"]
    if l5 and nombra and cob_l5:
        print("  OK    L5   declara por su nombre el campo de configuracion que no supo juzgar")
    else:
        print(f"  FALLA L5   hallazgos={len(l5)} nombra={nombra} cobertura={len(cob_l5)}")
        faltan.append("campo-de-config-sin-declarar")

    # --- prueba ALC: el alcance por defecto es CONFIGURACION (ley de FER, 2026-09-05:
    # "esta skill es exclusivamente para analizar configuracion, no vemos productos").
    # Lo que se aparta NO se pierde: queda declarado y contado, con su severidad, para que
    # nadie confunda "fuera de alcance" con "no hay nada". Es la diferencia entre recortar
    # y esconder.
    cfg = Auditoria(espacio_roto())            # sin argumento = config, ese es el punto
    cfg.correr()
    tod = Auditoria(espacio_roto(), alcance="todo")
    tod.correr()
    from auditar import es_campo_de_producto
    def _prod(hs):
        return [h for h in hs if es_campo_de_producto(h.get("campo"))]
    apartados = getattr(cfg, "fuera_de_alcance", None)
    # 🔴 LA FRONTERA, corregida el 2026-09-08. Este caso exigia `not _prod(cfg.hallazgos)`:
    # que NINGUN hallazgo sobre un campo de producto saliera en modo config. Eso codificaba
    # el defecto que caz el golden-verificador -- con esa regla, **D1 (la palabra clave que
    # debe coincidir BYTE A BYTE entre el producto y el disparador) se archivaba y no se le
    # reportaba a FER**, aunque un desajuste ahi deje el producto sin arrancar. El SKILL.md
    # ya decia lo correcto ("el disparador es cableado, aunque nombre productos") y el codigo
    # hacia lo contrario.
    #
    # Lo que se exige ahora: en modo config puede haber hallazgos que APUNTEN a un campo de
    # producto, pero SOLO de controles de CABLEADO. Los de CONTENIDO van a fuera_de_alcance.
    CABLEADO = {"D1", "D2", "D3", "D3b", "D4", "D5", "D6",
                "C1", "C2", "C3", "C4", "C5", "C6", "E3", "G3"}
    prod_en_config = _prod(cfg.hallazgos)
    contenido_colado = [h for h in prod_en_config if h.get("control") not in CABLEADO]
    # 🔴 LA ASERCION QUE DE VERDAD MUERDE, y me faltaba: no basta con que el CONTENIDO no se
    # cuele — hay que exigir que el CABLEADO SI SALGA. Mi primera version solo comprobaba lo
    # primero, y la contraprueba (reponer el filtro por nombre de campo) seguia en verde: un
    # banco que no muerde ante el defecto que existe para cazar no vale nada.
    # El banco siembra D1 (palabra clave que difiere en un acento) sobre una ranura de
    # producto. Con el defecto puesto, ese hallazgo aterriza en fuera_de_alcance y FER no lo
    # ve, aunque deje el producto sin arrancar. Aqui se exige que salga en la corrida normal.
    d1_en_config = [h for h in cfg.hallazgos if h.get("control") == "D1"]
    d1_apartado = [h for h in (apartados or []) if h.get("control") == "D1"]
    ok = (cfg.alcance == "config"
          and not contenido_colado                      # nada de CONTENIDO se cuela
          and d1_en_config and not d1_apartado          # 🔴 el CABLEADO SI sale
          and _prod(tod.hallazgos)                      # en modo todo si aparecen
          and apartados                                 # y lo apartado se declara
          and any(h["severidad"] in ("MUERTO", "ANUNCIADA") for h in apartados))
    if ok:
        print(f"  OK    ALC  audita CONFIGURACION: {len(prod_en_config)} hallazgos de "
              f"CABLEADO sobre ranuras de producto SI salen · {len(apartados)} de "
              f"CONTENIDO apartados y declarados")
    else:
        print(f"  FALLA ALC  alcance={getattr(cfg, 'alcance', 'no existe')} · "
              f"D1 en config={len(d1_en_config)} (debe ser >0) · D1 apartado="
              f"{len(d1_apartado)} (debe ser 0) · CONTENIDO colado={len(contenido_colado)} "
              f"{[h.get('control') for h in contenido_colado][:5]} · "
              f"producto en todo={len(_prod(tod.hallazgos))} · "
              f"apartados={len(apartados or [])}")
        faltan.append("alcance-config")

    print(f"\n  {len(ESPERADOS) - len(faltan)} de {len(ESPERADOS)} defectos sembrados "
          f"fueron detectados")

    # El producto 1 esta sano: si el auditor lo acusa, tiene un falso positivo.
    falsos = [h for h in a.hallazgos if "[Producto Ventas Wp] 1`" in h["evidencia"]
              or h["titulo"].endswith("[Producto Ventas Wp] 1")]
    if falsos:
        print(f"  AVISO: {len(falsos)} hallazgos contra el producto SANO (falso positivo)")

    # --- prueba 2: la severidad la decide el NEGOCIO
    # El huerfano CON anuncios tiene que salir MUERTO y el que no tiene pauta, no.
    d3 = [h for h in a.hallazgos if h["control"] == "D3"]
    con = [h for h in d3 if h.get("clave") == "D3|huerfanos-con-pauta"]
    sin = [h for h in d3 if h.get("clave") == "D3|huerfanos-sin-pauta"]
    print()
    if con and con[0]["severidad"] == "MUERTO":
        print("  OK    D3   el huerfano CON pauta sale en rojo")
    else:
        print("  FALLA D3   el huerfano CON pauta deberia salir MUERTO")
        faltan.append("D3-con-pauta")
    if sin and sin[0]["severidad"] == "DUDA":
        print("  OK    D3   el huerfano SIN pauta NO alarma")
    else:
        print("  FALLA D3   el huerfano SIN pauta no deberia salir en rojo")
        faltan.append("D3-sin-pauta")

    # --- prueba B8: la variante sembrada esta EN el catalogo de prefijos conocidos.
    # Si B3 la acusa, el mensaje es falso ("no la se auditar" cuando si la sabe); y si
    # nadie la acusa, el catalogo se convirtio en la alfombra que escondio el defecto.
    from auditar import PREFIJOS_CONOCIDOS
    b8 = [h for h in a.hallazgos if h["control"] == "B8"]
    b3_desc = [h for h in a.hallazgos if h["control"] == "B3" and "no catalogados" in h["evidencia"]]
    catalogadas = "[Log\u00edstico]" in PREFIJOS_CONOCIDOS and "[Logistico]" in PREFIJOS_CONOCIDOS
    variante_en_b3 = any("Log" in h["evidencia"] for h in b3_desc)
    if b8 and catalogadas and not variante_en_b3:
        print("  OK    B8   la colision de prefijos sale aunque las dos variantes esten catalogadas")
    else:
        print(f"  FALLA B8   b8={len(b8)} catalogadas={catalogadas} variante_en_b3={variante_en_b3}")
        faltan.append("colision-de-prefijos")

    # --- prueba 3: el libro de decisiones silencia lo ya resuelto, sin borrarlo
    b = Auditoria(espacio_roto(), alcance="todo")
    b.decisiones = {"D3|huerfanos-sin-pauta": {
        "motivo": "sin pauta activa, se registran cuando se les ponga",
        "fecha": "2026-08-20", "reabrir_si": "se les carga un id de anuncio"}}
    b.correr()
    decididos = [h for h in b.hallazgos if h["severidad"] == "DECIDIDO"]
    otros = [h for h in b.hallazgos if h["control"] == "D3"
             and h["clave"] == "D3|huerfanos-con-pauta"]
    if len(decididos) == 1 and otros and otros[0]["severidad"] == "MUERTO":
        print("  OK    LD   el libro silencia SOLO lo decidido y deja el resto intacto")
    else:
        print(f"  FALLA LD   el libro deberia silenciar 1 y dejo {len(decididos)}")
        faltan.append("libro-de-decisiones")

    # --- prueba 4: el diff ve lo que se movio
    import copy
    anterior = copy.deepcopy(espacio_roto())
    anterior["/flow/bot-fields"] = [c for c in anterior["/flow/bot-fields"]
                                    if c["name"] != "TOKEN DROPI"]
    for c in anterior["/flow/bot-fields"]:
        if c["name"] == "[Carritos] Configuracion":
            c["value"] = "{}"
        # --- J1b: un valor CORTO en la corrida anterior, con muchas tildes en la actual —
        # el hueco entre crudo y escapado es grande (cada tilde pesa 6 escapados) y sirve
        # para probar que el diff muestra el escapado REAL, no el largo crudo del JSON.
        if c["name"] == "[Comentarios] Configuracion General":
            c["value"] = json.dumps({"texto": "corto"})
    c2 = Auditoria(espacio_roto(), alcance="todo"); c2.correr(); c2.comparar(anterior)
    tipos = {t for t, _, _ in c2.cambios}
    if {"NUEVO", "EDITADO"} <= tipos:
        print("  OK    J1   el diff detecta campos nuevos y editados")
    else:
        print(f"  FALLA J1   el diff solo vio {tipos}")
        faltan.append("diff")

    # --- prueba 4c (J1b): el diff calcula y muestra el ESCAPADO real, no el largo crudo
    import re as _re
    valor_nuevo = next(c["value"] for c in espacio_roto()["/flow/bot-fields"]
                       if c["name"] == "[Comentarios] Configuracion General")
    esc_esperado = len(json.dumps(valor_nuevo)[1:-1])
    crudo_esperado = len(valor_nuevo)
    detalle_cfg = next((d for t, n, d in c2.cambios
                        if n == "[Comentarios] Configuracion General"), "")
    m = _re.search(r"([\d,]+) → ([\d,]+) escapados", detalle_cfg)
    mostrado_en = int(m.group(2).replace(",", "")) if m else None
    if mostrado_en == esc_esperado and esc_esperado != crudo_esperado:
        print("  OK    J1b  el diff muestra el escapado real, no el largo crudo del JSON")
    else:
        print(f"  FALLA J1b  el diff mostro {mostrado_en}, el escapado real es {esc_esperado} "
              f"(crudo {crudo_esperado})")
        faltan.append("diff-escapado")

    # --- prueba 4b: los DOS niveles de confianza del corchete.
    # Contrastado contra los 12 productos reales de un espacio en produccion: tratar "mayusculas sostenidas"
    # como hueco acusaba 3 falsos de cada 4. El verbo de encargo es rojo; el resto, duda.
    g = Auditoria(espacio_roto(), alcance="todo"); g.correr()
    f3 = [h for h in g.hallazgos if h["control"] == "F3"]
    rojo = [h for h in f3 if h["severidad"] == "MUERTO" and "AQUI VAN" in h["evidencia"]]
    duda = [h for h in f3 if h["severidad"] == "DUDA" and "IMAGEN 1" in h["evidencia"]]
    falso = [h for h in f3 if "[total]" in h["evidencia"]]
    if rojo and duda and not falso:
        print("  OK    F3   verbo de encargo = rojo · mayusculas = duda · [total] no dispara")
    else:
        print(f"  FALLA F3   rojo={len(rojo)} duda={len(duda)} falso_positivo={len(falso)}")
        faltan.append("corchetes-dos-niveles")

    # --- prueba CLV: una clave de decision no puede fusionar dos hallazgos DISTINTOS.
    # `[Producto Ventas Wp] 9` (HUECOS) ya trae, sembrados arriba, un hueco de editor (rojo,
    # producto activo) Y un corchete en mayusculas (duda) EN EL MISMO CAMPO. Sin la huella
    # de la evidencia en la clave, los dos colapsaban bajo `F3|[Producto Ventas Wp] 9` y una
    # sola decision del dueno silenciaba a los dos de una vez.
    f3_p9 = [h for h in g.hallazgos
             if h["control"] == "F3" and h["campo"] == "[Producto Ventas Wp] 9"]
    claves_p9 = {h["clave"] for h in f3_p9}
    if len(f3_p9) >= 2 and len(claves_p9) == len(f3_p9):
        print("  OK    CLV  dos hallazgos F3 del mismo campo tienen claves distintas")
    else:
        print(f"  FALLA CLV  {len(f3_p9)} hallazgos comparten {len(claves_p9)} clave(s): "
              "una decision silenciaria mas de uno")
        faltan.append("clave-colision")

    # --- prueba 4c: la severidad respeta el ESTADO de la entrada.
    h = Auditoria(espacio_roto(), alcance="todo"); h.correr()
    d3 = [x for x in h.hallazgos if x["control"] == "D3"]
    apagada = [x for x in d3 if "INACTIVAS" in x["titulo"] or "33" in x["evidencia"]]
    rojo_vivo = [x for x in d3 if x["severidad"] == "MUERTO" and "ACTIVAS" in x["titulo"]]
    mal = [x for x in d3 if x["severidad"] == "MUERTO"
           and ("INACTIVA" in x["titulo"] or "] 33" in x["evidencia"])]
    if apagada and rojo_vivo and not mal:
        print("  OK    EST  entrada activa = rojo · entrada apagada = duda, nunca rojo")
    else:
        print(f"  FALLA EST  apagada={len(apagada)} rojo_vivo={len(rojo_vivo)} en_rojo_mal={len(mal)}")
        faltan.append("severidad-por-estado")

    # --- prueba 4d: el libro acepta clave AMPLIA y clave FINA.
    # La huella corta `::hash` se anadio para no silenciar 5 hallazgos con una decision; el
    # efecto colateral fue romper las decisiones ya escritas (medido: 4 de 6 dejaron de casar).
    k = Auditoria(espacio_roto(), alcance="todo"); k.correr()
    finas = [x["clave"] for x in k.hallazgos if "::" in x["clave"]]
    assert finas, "el fixture ya no produce claves finas"
    base = finas[0].split("::")[0]
    amplia = Auditoria(espacio_roto(), alcance="todo")
    amplia.decisiones = {base: {"motivo": "m", "fecha": "2026-01-01", "reabrir_si": "r"}}
    amplia.correr()
    fina = Auditoria(espacio_roto(), alcance="todo")
    fina.decisiones = {finas[0]: {"motivo": "m", "fecha": "2026-01-01", "reabrir_si": "r"}}
    fina.correr()
    n_amplia = sum(1 for x in amplia.hallazgos if x["severidad"] == "DECIDIDO")
    n_fina = sum(1 for x in fina.hallazgos if x["severidad"] == "DECIDIDO")
    if n_amplia >= 1 and n_fina == 1:
        print(f"  OK    LIB  clave amplia silencia {n_amplia} · clave fina silencia exactamente 1")
    else:
        print(f"  FALLA LIB  amplia={n_amplia} fina={n_fina} (la amplia debe cubrir, la fina una)")
        faltan.append("libro-clave-amplia")

    # --- prueba 5: degradacion elegante. Un endpoint que respondio con error NO puede
    # tumbar la auditoria entera: un 500 puntual de la API costaria el informe completo.
    roto = espacio_roto()
    roto["/flow/user-fields"] = {"_ERROR_HTTP": 500, "_detalle": "server error"}
    try:
        e = Auditoria(roto).correr()
        ileg = [h for h in e.hallazgos if h["clave"].startswith("B1|ilegible")]
        if ileg:
            print("  OK    DEG  un endpoint con error se declara y la auditoria sigue")
        else:
            print("  FALLA DEG  el endpoint ilegible paso en silencio")
            faltan.append("degradacion")
    except Exception as ex:                                       # noqa: BLE001
        print(f"  FALLA DEG  la auditoria REVIENTA: {type(ex).__name__}")
        faltan.append("degradacion")

    # --- prueba 6: el paquete de correccion no puede tirar las dudas accionables
    import tempfile, os
    from auditar import escribir_handoff
    f = Auditoria(espacio_roto(), alcance="todo"); f.correr()
    tmp = Path(tempfile.gettempdir()) / "autoprueba-handoff.md"
    escribir_handoff(f, tmp)
    texto = tmp.read_text()
    dudas_con_accion = [h for h in f.hallazgos
                        if h["severidad"] == "DUDA" and h.get("accion")]
    if not dudas_con_accion or "preguntas que hay que contestar" in texto:
        print("  OK    HO   las dudas accionables salen en el paquete, no a la basura")
    else:
        print(f"  FALLA HO   {len(dudas_con_accion)} dudas con accion quedaron fuera")
        faltan.append("handoff-dudas")

    # --- prueba HO2: todo rojo o naranja entra al paquete, TENGA O NO `accion` explicita.
    # Filtrar por "tiene accion" antes de mirar severidad tiraba rojos/naranjas reales
    # (medido: 22 de 39 hallazgos abiertos, 5 rojos de un disparador). Se busca un caso
    # sembrado que YA no trae `accion` (varios D3 y el propio C4 no la traen) y se confirma
    # que su titulo aparece en el paquete escrito.
    graves_sin_accion = [h for h in f.hallazgos
                         if h["severidad"] in ("MUERTO", "ANUNCIADA") and not h.get("accion")]
    faltantes_ho2 = [h for h in graves_sin_accion if h["titulo"] not in texto]
    if graves_sin_accion and not faltantes_ho2:
        print(f"  OK    HO2  {len(graves_sin_accion)} rojos/naranjas sin accion "
              "entraron al paquete")
    elif not graves_sin_accion:
        print("  FALLA HO2  no hay ningun caso sembrado de rojo/naranja sin accion para probarlo")
        faltan.append("handoff-severidad-sin-fixture")
    else:
        print(f"  FALLA HO2  {len(faltantes_ho2)} de {len(graves_sin_accion)} quedaron fuera")
        faltan.append("handoff-severidad")

    # --- prueba HO3: la RAMA GEMELA. El arreglo de HO2 se hizo solo para MUERTO/ANUNCIADA
    # y nadie busco su hermana: la rama de FUGA (🟡) conservaba el `if not accion: continue`
    # y se comia 11 hallazgos abiertos mas (medido en Dolce el 2026-09-08: F14, F2, G2, los
    # 6 de G3 y los 2 de F13). Una FUGA es lo que LLEGA AL CLIENTE, asi que caerse del
    # paquete es lo peor que le puede pasar. Clase, no caso: al tocar un filtro, buscar sus
    # hermanas. Por eso esta prueba es hermana literal de HO2.
    fugas_sin_accion = [h for h in f.hallazgos
                        if h["severidad"] == "FUGA" and not h.get("accion")]
    faltantes_ho3 = [h for h in fugas_sin_accion if h["titulo"] not in texto]
    if fugas_sin_accion and not faltantes_ho3:
        print(f"  OK    HO3  {len(fugas_sin_accion)} fugas sin accion entraron al paquete")
    elif not fugas_sin_accion:
        print("  FALLA HO3  no hay ninguna FUGA sin accion sembrada para probarlo")
        faltan.append("handoff-fuga-sin-fixture")
    else:
        print(f"  FALLA HO3  {len(faltantes_ho3)} de {len(fugas_sin_accion)} fugas fuera")
        faltan.append("handoff-fuga")

    # --- prueba HO4: el paquete DECLARA cuanto quedo fuera por alcance, y NO lo describe.
    # Dos fallos en uno: (a) el paquete se leia como si fuera todo lo encontrado y no lo
    # era; (b) declararlo con severidades seria juzgar productos, que es lo prohibido.
    # Se exige el numero literal y se PROHIBE el vocabulario de severidad en esa seccion.
    g = Auditoria(espacio_roto(), alcance="config"); g.correr()
    tmp2 = Path(tempfile.gettempdir()) / "autoprueba-handoff-config.md"
    escribir_handoff(g, tmp2)
    t2 = tmp2.read_text()
    n_fuera = len(g.fuera_de_alcance)
    trozo = t2.split("## Lo que NO viaja")[1].split("\n##")[0] if "## Lo que NO viaja" in t2 else ""
    describe = [w for w in ("MUERTO", "ANUNCIADA", "FUGA", "muerto", "anunciada", "fuga")
                if w in trozo]
    if n_fuera and f"{n_fuera} apartados" in t2 and not describe:
        print(f"  OK    HO4  el paquete declara {n_fuera} apartados, sin describirlos")
    elif not n_fuera:
        print("  FALLA HO4  con alcance config no quedo nada fuera: no hay caso que probar")
        faltan.append("handoff-alcance-sin-fixture")
    elif describe:
        print(f"  FALLA HO4  la cabecera JUZGA lo apartado: {describe}")
        faltan.append("handoff-alcance-describe")
    else:
        print(f"  FALLA HO4  el paquete no declara los {n_fuera} apartados")
        faltan.append("handoff-alcance")
    os.unlink(tmp2)

    # --- prueba F13cob: la COBERTURA de la zona IA cuenta lo que se AUDITO, no lo que se
    # bajo. Dos objetos sin texto van sembrados en la fixture: el numerador de F13 tiene que
    # ser 1 (el unico con cadenas), no 3, y los 2 vacios tienen que salir DECLARADOS. Un
    # "3 de 3 revisados" donde 2 no se miraron es cobertura falsa: la mentira exacta que
    # este auditor existe para no cometer.
    cob = next((c for c in g.cobertura if c["control"] == "F13"), None)
    zona = g.universo.get("zona_ia") or {}
    dudas_f13 = [h for h in (g.hallazgos + g.fuera_de_alcance)
                 if h["control"] == "F13" and h["severidad"] == "DUDA"]
    if (cob and zona.get("objetos") == 3 and zona.get("sin_texto") == 2
            and cob.get("revisados") == 1 and dudas_f13):
        print("  OK    F13c la cobertura de la zona IA cuenta 1 de 3 y declara los 2 vacios")
    else:
        print(f"  FALLA F13c cobertura={cob} zona={zona} dudas={len(dudas_f13)}")
        faltan.append("f13-cobertura-falsa")

    # --- prueba CAT: el CATALOGO no puede prometer lo que ningun instrumento hace.
    # `references/controles.md` marca cada control como A (automatico) o H (a mano). Un
    # control marcado A que no aparece por su nombre en ningun script es una promesa sin
    # instrumento: el lector del catalogo cuenta con el y nadie lo corre. Medido el
    # 2026-09-08: D3b, I1b, J1, K1, K2 y K3 estaban asi. Se cierra la CLASE, no los seis
    # casos: cualquier control A que se documente manana y no se cablee, muerde aqui.
    cat = Path(__file__).resolve().parent.parent / "references" / "controles.md"
    if not cat.exists():
        print("  FALLA CAT  no existe references/controles.md: el catalogo es el denominador")
        faltan.append("catalogo-ausente")
    else:
        automaticos = []
        for linea in cat.read_text(encoding="utf-8").splitlines():
            trozos = [t.strip() for t in linea.split("|")]
            # fila de tabla: ['', ID, modo, texto, ''] -- se exige el modo EXACTO "A"
            if len(trozos) >= 4 and re.fullmatch(r"[A-Z]\d+[a-z]?", trozos[1]) \
                    and trozos[2] == "A":
                automaticos.append(trozos[1])
        fuentes = "\n".join(f.read_text(encoding="utf-8")
                             for f in Path(__file__).resolve().parent.glob("*.py"))
        huerfanos = [c for c in automaticos
                     if not re.search(rf"\b{re.escape(c)}\b", fuentes)]
        # 🔴 LA RAMA GEMELA, y la abri yo mismo el 2026-09-08 el mismo dia que la cierro:
        # CAT medía catalogo -> codigo, y al cablear L4 y L4b el codigo se adelanto al
        # catalogo sin que nada mordiera. Los dos sentidos fallan igual de callados, pero al
        # reves: un control que CORRE y no esta documentado sale en el informe y el dueno no
        # tiene donde leer que mide ni por que existe -- y nadie lo revisa al cambiarlo.
        # La ley de la casa: corregir es MOVER un criterio, y se cierra midiendo los DOS
        # sentidos. Se lee del codigo lo que DECLARA (cubre/falla), que es lo unico que
        # llega al informe.
        todos_cat = set()
        for linea in cat.read_text(encoding="utf-8").splitlines():
            trozos = [t.strip() for t in linea.split("|")]
            if len(trozos) >= 4 and re.fullmatch(r"[A-Z]\d+[a-z]?", trozos[1]):
                todos_cat.add(trozos[1])
        declarados_en_codigo = set(re.findall(
            r'self\.(?:cubre|falla)\(\s*"([A-Z]\d+[a-z]?)"', fuentes))
        sin_documentar = sorted(declarados_en_codigo - todos_cat)
        if automaticos and not huerfanos and not sin_documentar:
            print(f"  OK    CAT  los {len(automaticos)} controles automaticos del catalogo "
                  f"estan cableados, y los {len(declarados_en_codigo)} que el codigo declara "
                  "estan documentados")
        elif sin_documentar and not huerfanos:
            print(f"  FALLA CAT  {len(sin_documentar)} controles CORREN y no estan en el "
                  f"catalogo: {sin_documentar}")
            faltan.append("codigo-corre-sin-documentar")
        elif not automaticos:
            print("  FALLA CAT  el catalogo no declaro ni un control automatico: no se parseo")
            faltan.append("catalogo-sin-parsear")
        else:
            print(f"  FALLA CAT  {len(huerfanos)} controles marcados A sin instrumento: "
                  f"{huerfanos}")
            faltan.append("catalogo-promete-sin-cablear")

    # --- prueba VER: la version del cuerpo tiene que ser la del acta mas nueva.
    # Medido el 2026-09-08: el cuerpo decia `GCA2.4` y la cabecera ya iba por v2.5. Nadie
    # miente a proposito: se escribe el acta arriba y se olvida la linea de abajo, y a
    # partir de ahi el lector no sabe que version esta leyendo. Se ancla a las DOS formas
    # reales del archivo y se exige que coincidan.
    sk = (Path(__file__).resolve().parent.parent / "SKILL.md").read_text(encoding="utf-8")
    m_acta = re.search(r"<!--\s*skill v(\d+\.\d+)", sk)
    m_cuerpo = re.search(r"\*\*Versi[oó]n:\*\*\s*`GCA(\d+\.\d+)`", sk)
    if not m_acta or not m_cuerpo:
        print(f"  FALLA VER  no se encontro la version (acta={bool(m_acta)} "
              f"cuerpo={bool(m_cuerpo)}): el ancla dejo de casar con el archivo")
        faltan.append("version-sin-ancla")
    elif m_acta.group(1) != m_cuerpo.group(1):
        print(f"  FALLA VER  el acta dice v{m_acta.group(1)} y el cuerpo GCA"
              f"{m_cuerpo.group(1)}")
        faltan.append("version-desincronizada")
    else:
        print(f"  OK    VER  acta y cuerpo dicen lo mismo: v{m_acta.group(1)}")

    # --- prueba ESQ: L1/L2/L3 contra el esquema de referencia (encargo de FER 08-sep).
    # Fixture con las TRES formas de estar mal a la vez, sobre el mismo campo:
    #   · faltan 2 llaves (ej_a_eliminar y datos_req)          -> L1 MUERTO
    #   · prompt_general con 20 caracteres contra ~1.548        -> L2 FUGA
    #   · respuesta_publica.prompt con EXACTAMENTE 1.467        -> L3 DUDA (espejo)
    # Se exige que salgan LAS TRES: L2 y L3 son gemelos opuestos —demasiado corto y demasiado
    # igual— y una prueba que solo mire uno deja la puerta abierta por el lado contrario.
    esq_dump = espacio_roto()
    esq_dump["/flow/bot-fields"] = list(esq_dump["/flow/bot-fields"]) + [{
        "name": "[Comentarios] Configuracion General", "var_ns": "f1v_esq",
        "value": json.dumps({
            "informacion_del_negocio": {"pais": "colombia", "contacto": "x" * 82,
                                        "t_envio": "y" * 112, "info_extra": "z" * 306},
            "comentarios_negativos": {"habilitar": "si", "prompt_general": "a" * 20,
                                      "ej_a_no_eliminar": "b" * 995},
            "respuesta_publica": {"habilitar": "si", "prompt": "c" * 1467,
                                  "aut_link_pub": "si", "aut_precio_pub": "no"},
            "venta_conversacional": {"habilitar": "si", "prompt": "d" * 5091},
        }, ensure_ascii=False)}]
    e = Auditoria(esq_dump, alcance="todo"); e.correr()
    _todos = e.hallazgos + e.fuera_de_alcance
    # 🔴 El fixture base YA trae campos de configuracion casi vacios, asi que L1 dispara en
    # varios. Se filtra por EL CAMPO SEMBRADO, no se coge el primero: coger [0] hacia que la
    # prueba mirase el hallazgo de otro campo y diera un verde que no probaba nada.
    def _del_campo(c):
        return [h for h in _todos if h["control"] == c
                and "[Comentarios] Configuracion General" in h["titulo"]]
    _l1, _l2, _l3 = _del_campo("L1"), _del_campo("L2"), _del_campo("L3")
    _falta_bien = _l1 and "ej_a_eliminar" in _l1[0]["evidencia"] and \
                  "datos_req" in _l1[0]["evidencia"]
    _corto_bien = _l2 and "prompt_general" in _l2[0]["evidencia"]
    # L3 es AGREGADO: se exige que declare la proporcion, no un campo suelto
    _espejo_bien = _l3 and "de 5 campos largos" in _l3[0]["titulo"]
    # contraparte: el campo corto NO puede contarse tambien como espejo
    _sano_colado = any("prompt_general" in h["evidencia"] for h in _l3)
    if _falta_bien and _corto_bien and _espejo_bien and not _sano_colado:
        print("  OK    ESQ  L1 llave ausente · L2 puesto de compromiso · L3 espejo, "
              "y los sanos no se cuelan")
    else:
        print(f"  FALLA ESQ  L1={bool(_falta_bien)} L2={bool(_corto_bien)} "
              f"L3={bool(_espejo_bien)} sano_colado={_sano_colado}")
        faltan.append("esquema-referencia")

    # --- prueba PAIS: L4 · los PAISES DECLARADOS no coinciden entre si.
    # El pais no vive en un sitio: vive en cinco, uno por asistente. Se siembran dos en
    # desacuerdo y uno vacio, y se exigen LOS DOS hallazgos: el desacuerdo (MUERTO) y el
    # vacio (ANUNCIADA). Y una tercera cosa, que es la que evita el invento: con dos paises
    # puestos, L4b NO puede correr -- elegir uno de los dos como "el bueno" seria acusar al
    # otro de fuga sin saber cual es.
    def _dump_pais(campos_pais):
        d = espacio_roto()
        d["/flow/bot-fields"] = list(d["/flow/bot-fields"]) + [
            campo(n, v) for n, v in campos_pais]
        return d

    p_dump = _dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "GUATEMALA"}}),
        ("[Carritos] Configuracion", {"datos_tienda": {"pais": "COLOMBIA"}}),
        ("[Comentarios] Configuracion General", {"informacion_del_negocio": {"pais": ""}}),
    ])
    pa = Auditoria(p_dump, alcance="todo"); pa.correr()
    _pt = pa.hallazgos + pa.fuera_de_alcance
    _desacuerdo = [h for h in _pt if h["control"] == "L4" and h["severidad"] == "MUERTO"]
    _vacio = [h for h in _pt if h["control"] == "L4" and h["severidad"] == "ANUNCIADA"]
    _cob_l4b = [c for c in pa.cobertura if c["control"] == "L4b"]
    _l4b_callado = (_cob_l4b and _cob_l4b[0]["estado"] == "NO_CORRIDO"
                    and not [h for h in _pt if h["control"] == "L4b"])
    _cita_los_dos = _desacuerdo and "GUATEMALA" in _desacuerdo[0]["evidencia"] \
                    and "COLOMBIA" in _desacuerdo[0]["evidencia"]
    if _cita_los_dos and _vacio and _l4b_callado:
        print("  OK    PAIS L4 ve los dos paises en desacuerdo y el vacio, y con el "
              "desacuerdo abierto L4b se declara sin correr en vez de elegir uno")
    else:
        print(f"  FALLA PAIS desacuerdo={bool(_cita_los_dos)} vacio={bool(_vacio)} "
              f"l4b_callado={bool(_l4b_callado)}")
        faltan.append("coherencia-de-pais")

    # --- prueba PAISB: L4b · el CONTENIDO es de otro pais, y la severidad depende de si el
    # lexico que lo delata CADUCA. Un espacio declarado GUATEMALA:
    #   · con PROFECO (organismo de consumo mexicano, familia ESTABLE) -> MUERTO
    #   · con solo Servientrega (transportadora, familia que CADUCA)   -> FUGA
    # Las dos a la vez, porque bajar la severidad de todo seria tan falso como subirla.
    pb = Auditoria(_dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "GUATEMALA"},
                                          "politicas_de_garantia": "La garantia se tramita "
                                          "ante la PROFECO en un plazo de 30 dias."}),
    ]), alcance="todo"); pb.correr()
    def _l4b_de(aud, campo_):
        return [h for h in aud.hallazgos + aud.fuera_de_alcance
                if h["control"] == "L4b" and campo_ in h["titulo"]]
    _b = _l4b_de(pb, "[Logistico] Configuracion General")
    _estable_muerde = _b and _b[0]["severidad"] == "MUERTO" and "PROFECO" in _b[0]["evidencia"]

    pc = Auditoria(_dump_pais([
        ("[Logistico] Confirmaciones", {"datos_de_la_tienda": {"pais": "GUATEMALA"},
                                           "transportadoras": "Enviamos con Servientrega."}),
    ]), alcance="todo"); pc.correr()
    _c = _l4b_de(pc, "[Logistico] Confirmaciones")
    _caduca_baja = _c and _c[0]["severidad"] == "FUGA"
    if _estable_muerde and _caduca_baja:
        print("  OK    PAISB L4b muerde el contenido ajeno, y baja a FUGA cuando lo unico "
              "que lo delata es un lexico que caduca")
    else:
        print(f"  FALLA PAISB estable_muerde={bool(_estable_muerde)} "
              f"caduca_baja={bool(_caduca_baja)}")
        faltan.append("contenido-de-otro-pais")

    # --- prueba PAISC: los TRES silencios que tienen que ser silencio. Un control de pais
    # que acusa de mas es peor que no tenerlo: a los tres informes el dueno deja de leerlo.
    #   1. Un pais que NO esta en el lexico no se juzga y se DECLARA. Lleva PROFECO dentro a
    #      proposito: si acusara, estaria juzgando un pais del que no sabe nada.
    #   2. Un marcador COMPARTIDO no acusa a ninguno de sus duenos (Servientrega opera en
    #      Colombia Y Ecuador; en un espacio ecuatoriano es lo correcto).
    #   3. Una palabra CORRIENTE del espanol no es un marcador. La transportadora colombiana
    #      "Envia" quedo fuera del lexico por esto, y esta prueba es la que lo sostiene.
    pd_ = Auditoria(_dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "BOLIVIA"},
                                          "politicas_de_garantia": "Reclamos ante PROFECO."}),
    ]), alcance="todo"); pd_.correr()
    _cob = [c for c in pd_.cobertura if c["control"] == "L4b"]
    _fuera_lexico = (not _l4b_de(pd_, "[Logistico] Configuracion General")
                     and _cob and _cob[0]["estado"] == "NO_CORRIDO"
                     and "no se juzga" in _cob[0]["nota"].lower())

    pe = Auditoria(_dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "ECUADOR"},
                                          "transportadoras": "Enviamos con Servientrega."}),
    ]), alcance="todo"); pe.correr()
    _compartido = not _l4b_de(pe, "[Logistico] Configuracion General")

    pf = Auditoria(_dump_pais([
        ("[Logistico] Confirmaciones", {"datos_de_la_tienda": {"pais": "GUATEMALA"},
                                           "tiempos": "Se envia a domicilio y el correo "
                                           "llega en 2 dias; el servicio nacional domina "
                                           "la entrega urbana."}),
    ]), alcance="todo"); pf.correr()
    _corrientes = not _l4b_de(pf, "[Logistico] Confirmaciones")
    if _fuera_lexico and _compartido and _corrientes:
        print("  OK    PAISC los tres silencios: pais fuera del lexico se DECLARA sin "
              "juzgar · marcador compartido no acusa · palabra corriente no es marcador")
    else:
        print(f"  FALLA PAISC fuera_lexico={bool(_fuera_lexico)} "
              f"compartido={bool(_compartido)} corrientes={bool(_corrientes)}")
        faltan.append("pais-falsos-positivos")

    # --- prueba PAISD: EL CUARTO SILENCIO, que este banco NO cubria y encontro un cliente
    # real el 2026-09-17. LA ENUMERACION MULTI-PAIS INTENCIONAL.
    # Un prompt escrito a proposito para varios paises —"la normativa de tu pais: SIC en
    # Colombia, PROFECO en Mexico, DIACO en Guatemala"— en un espacio declarado COLOMBIA
    # salia 🔴 MUERTO por PROFECO y DIACO. Y era correcto: nombra Colombia, y primero.
    # La señal que lo separa de una contaminacion real es que el MISMO texto mencione el pais
    # declarado. No se calla (en un espacio de un solo pais esa lista sigue sobrando), pero
    # baja a DUDA. Las DOS mitades se prueban, porque bajar la severidad de todo seria tan
    # falso como subirla: el mismo texto SIN mencionar Colombia tiene que seguir mordiendo.
    pg = Auditoria(_dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "COLOMBIA"},
                                          "politicas_de_garantia": "Cumplimos la normativa "
                                          "publicitaria de tu pais, por ejemplo la SIC en "
                                          "Colombia, PROFECO en Mexico o DIACO en Guatemala."}),
    ]), alcance="todo"); pg.correr()
    _g = _l4b_de(pg, "[Logistico] Configuracion General")
    _enum_baja = _g and _g[0]["severidad"] == "DUDA" and "enumeracion" in _g[0]["titulo"].lower()

    # control negativo de la propia cura: el MISMO texto sin nombrar Colombia sigue en rojo
    ph = Auditoria(_dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "COLOMBIA"},
                                          "politicas_de_garantia": "Reclamos ante la PROFECO "
                                          "en un plazo de 30 dias."}),
    ]), alcance="todo"); ph.correr()
    _h = _l4b_de(ph, "[Logistico] Configuracion General")
    _sigue_mordiendo = _h and _h[0]["severidad"] == "MUERTO"

    if _enum_baja and _sigue_mordiendo:
        print("  OK    PAISD la enumeracion que NOMBRA su pais baja a DUDA, y el mismo texto "
              "sin nombrarlo sigue MUERTO")
    else:
        print(f"  FALLA PAISD enum_baja={bool(_enum_baja)} "
              f"sigue_mordiendo={bool(_sigue_mordiendo)}")
        faltan.append("enumeracion-multipais")

    # --- prueba RES: la skill declara DENTRO lo que no esta verificado.
    # Clase medida el 2026-09-08 y cometida por mi mismo: las reservas de esta skill vivian
    # en el informe del chat que la cerro. Una reserva en un informe es un RECUERDO -- se va
    # con el chat, y quien active la skill manana no la lee. Un guardarraiil vive donde se
    # lee siempre. Se exige la seccion y que nombre el riesgo concreto, no una frase vacia.
    _res = sk.split("Lo que NO está verificado en esta skill")
    if len(_res) < 2:
        print("  FALLA RES  la skill no declara DENTRO lo que no esta verificado")
        faltan.append("sin-reservas-declaradas")
    else:
        _cuerpo = _res[1][:4000]
        # el riesgo que de verdad puede morder a un cliente: el esquema sale de UN espacio
        _nombra = "un solo espacio" in _cuerpo.lower() or "un SOLO espacio" in _cuerpo
        # 🔴 CADA RESERVA NOMBRA QUIEN LA CIERRA (mejora de la fabrica de golden-imagen-arena,
        # adoptada el 2026-09-08). Es mas fuerte que exigir que "nombre el riesgo": obliga a
        # que la seccion no se pueda vaciar EN SILENCIO, porque vaciarla exige borrar
        # cerradores concretos y no ablandar un adjetivo. Y una reserva que no puede nombrar
        # a su cerrador o ya esta cerrada y sobra, o nadie la ha pensado.
        _cerradores = _cuerpo.count("**La cierra:**")
        if _nombra and "banco" in _cuerpo and _cerradores >= 5:
            print(f"  OK    RES  declara sus reservas dentro, con el riesgo nombrado y "
                  f"{_cerradores} cerradores")
        else:
            print(f"  FALLA RES  seccion floja (riesgo nombrado={_nombra} · "
                  f"cerradores={_cerradores}, hacen falta 5)")
            faltan.append("reservas-vacias")

    # --- prueba EXCL: lo que FER saco del ecosistema (EXCLUIDOS_POR_FER, hoy Remarketing IA)
    # no se audita por NINGUNA puerta, y el corte se prueba en los dos sentidos. Caso real del
    # 2026-09-24: el JSON de esperados decia `opcional: true` y el script no leia la bandera, asi
    # que B6 gritaba "Remarketing IA NO esta instalado" en un cliente. Se exige: (1) ningun
    # hallazgo nombra el asistente excluido, ni por B6 ni por el pais vacio de L4; (2) lo
    # apartado se DECLARA contado; (3) con --incluir-excluidos el MISMO pais vacio si sale, o
    # sea, lo que calla es el corte y no un control roto; (4) `opcional` se respeta aunque se
    # incluya; (5) control negativo: quitar un asistente OBLIGATORIO sigue dando B6.
    e_dump = _dump_pais([
        ("[Logistico] Configuracion General", {"datos_de_la_tienda": {"pais": "COLOMBIA"}}),
        ("[Carritos] Configuracion", {"datos_tienda": {"pais": "COLOMBIA"}}),
        ("[Remarketing IA] Configuracion general", {"datos_tienda": {"pais": ""}}),
        # un pais vacio de un asistente que SI se audita: obliga a L4 a emitir su hallazgo, y
        # asi se ve si su texto de accion vuelve a nombrar al asistente excluido
        ("[Comentarios] Configuracion General", {"informacion_del_negocio": {"pais": ""}}),
    ])

    # Tres puertas traseras que el verificador encontro el 24-sep, sembradas aqui para que no
    # vuelvan: (a) una variante del nombre con doble espacio y guion; (b) el AGENTE de IA del
    # asistente, que vive en otra zona del DUMP (F13) y trae "¿"; (c) el diff con --anterior.
    e_dump["/flow/bot-fields"].append(campo("[Remarketing  -IA] Mensajes", {"texto": "¿Sigues ahi?"}))
    e_dump.setdefault("/flow/ai-agents", []).append(
        {"name": "Agente de Remarketing", "ai_agent_ns": "f999999ag777", "flow_ns": "f999999"})
    e_dump.setdefault("_agentes_detalle", {})["f999999ag777"] = {
        "data": {"prompt": "¿Te acuerdas de tu carrito? [PONER NOMBRE]"}, "status": "ok"}

    # El hallazgo se mira ENTERO: titulo, evidencia, consecuencia, accion y campo. Hasta el
    # 24-sep solo se miraban tres, y la accion de L4 seguia nombrando Remarketing sin que
    # esta prueba lo viera (el paquete de correccion SI la entrega).
    # El agente se nombra por su ns (f999999ag777), no por "Remarketing": se buscan los dos.
    def _rm(aud):
        return [h for h in aud.hallazgos + aud.fuera_de_alcance
                if "emarketing" in json.dumps(h, ensure_ascii=False).lower()
                or "ag777" in json.dumps(h)]
    ex = Auditoria(e_dump, alcance="todo"); ex.correr()
    ex.comparar(e_dump)
    _borrados_falsos = [c for c in ex.cambios if c[0] == "BORRADO"]
    _decl = ex.universo.get("campos_excluidos_por_fer") or {}
    _esp = str(ex.universo.get("asistentes_esperados", ""))
    inc = Auditoria(e_dump, alcance="todo"); inc.incluir_excluidos = True; inc.correr()
    _l4_inc = [h for h in inc.hallazgos if h["control"] == "L4" and "remarketing" in
               (h["titulo"] + h["evidencia"]).lower()]
    op = Auditoria(espacio_roto(), alcance="todo"); op.incluir_excluidos = True; op.correr()
    _op_grita = [h for h in op.hallazgos if h["control"] == "B6" and "Remarketing" in h["titulo"]]
    sin_car = espacio_roto()
    sin_car["/flow/bot-fields"] = [c for c in sin_car["/flow/bot-fields"]
                                   if c["name"] != "[Carritos] Configuracion"]
    nc = Auditoria(sin_car, alcance="todo"); nc.correr()
    _car = [h for h in nc.hallazgos if h["control"] == "B6" and "Carritos" in h["titulo"]]
    # y en el sentido contrario: con --incluir-excluidos el agente SI se audita (F13 lo ve)
    _f13_inc = [h for h in inc.hallazgos if h["control"] == "F13" and "ag777" in json.dumps(h)]
    _variante = "[Remarketing  -IA] Mensajes" in (_decl.get("campos") or [])
    _l4_ex = [h for h in ex.hallazgos if h["control"] == "L4" and h["severidad"] == "ANUNCIADA"]
    _variante = _variante and bool(_l4_ex)   # sin el L4 emitido, la revision de su texto no prueba nada
    if (not _rm(ex) and _decl and _decl.get("cuantos", 0) >= 1
            and "de 4 presentes" in _esp and "Remarketing IA" in _esp
            and _l4_inc and not _op_grita and _car
            and not _borrados_falsos and _f13_inc and _variante):
        print("  OK    EXCL lo que FER saco no se audita por ninguna puerta, se declara contado, "
              "vuelve con --incluir-excluidos, `opcional` se respeta y B6 sigue mordiendo")
    else:
        print(f"  FALLA EXCL nombrados={len(_rm(ex))} declarado={bool(_decl)} esperados={_esp!r} "
              f"l4_con_inclusion={len(_l4_inc)} opcional_gritado={len(_op_grita)} "
              f"b6_carritos={len(_car)} borrados_falsos={len(_borrados_falsos)} "
              f"f13_agente_con_inclusion={len(_f13_inc)} variante_apartada={_variante}")
        faltan.append("excluidos-por-fer")

    # --- prueba I3: B4 e I3 comparten la MISMA lista de endpoints auditados (ENDPOINTS_B4).
    # custom-events no lo cubre nadie y tiene que seguir apareciendo; subflows/segments/agents
    # SI los cubre B4 y no deben aparecer como sin control.
    k = Auditoria(espacio_roto(), alcance="todo"); k.correr()
    i3h = next((h for h in k.hallazgos if h["control"] == "I3"), None)
    ev_i3 = i3h["evidencia"] if i3h else ""
    if ("/flow/custom-events" in ev_i3 and "/flow/segments" not in ev_i3
            and "/flow/agents" not in ev_i3 and "/flow/subflows" not in ev_i3):
        print("  OK    I3B4 B4 e I3 comparten la lista real de endpoints auditados")
    else:
        print(f"  FALLA I3B4 desincronizado: {ev_i3}")
        faltan.append("i3-b4-desync")
    os.unlink(tmp)

    if faltan:
        print(f"\nAUTOPRUEBA FALLIDA · el auditor NO detecta: {faltan}")
        print("El auditor esta roto. No se corre contra datos reales hasta arreglarlo.")
        return 1

    # 🔴 EL CONTEO SE MIDE, NO SE ESCRIBE. Los numeros vivian a mano en tres sitios
    # (SKILL.md dos veces y controles.md) y decian "31+16" y "31+11" cuando ya iban por
    # otro numero: una cifra en prosa desincroniza EL DIA que alguien anade una prueba, y
    # entonces la documentacion miente sobre su propia cobertura. Se imprime medido, y los
    # documentos apuntan a esta linea en vez de repetir la cifra.
    n_comport = Path(__file__).read_text(encoding="utf-8").count("\n    # --- prueba ")
    print(f"\nAutoprueba pasada: {len(ESPERADOS)} defectos sembrados + {n_comport} pruebas "
          f"de comportamiento. El auditor detecta los defectos sembrados.")
    print("Esto valida el DETECTOR, no valida ningun espacio real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
