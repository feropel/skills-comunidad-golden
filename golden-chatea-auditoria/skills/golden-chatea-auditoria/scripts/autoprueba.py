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
        "/flow/bot-fields": campos,
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
        # A4: la FORMA REAL del endpoint (medida contra Golden Colombia, fXXXXXX): enteros
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
    "B6": "asistentes esperados que NO estan instalados",
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

    # --- prueba 3: el libro de decisiones silencia lo ya resuelto, sin borrarlo
    b = Auditoria(espacio_roto())
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
    c2 = Auditoria(espacio_roto()); c2.correr(); c2.comparar(anterior)
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
    # Contrastado contra los 12 productos reales de Golden: tratar "mayusculas sostenidas"
    # como hueco acusaba 3 falsos de cada 4. El verbo de encargo es rojo; el resto, duda.
    g = Auditoria(espacio_roto()); g.correr()
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
    f = Auditoria(espacio_roto()); f.correr()
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

    # --- prueba I3: B4 e I3 comparten la MISMA lista de endpoints auditados (ENDPOINTS_B4).
    # custom-events no lo cubre nadie y tiene que seguir apareciendo; subflows/segments/agents
    # SI los cubre B4 y no deben aparecer como sin control.
    k = Auditoria(espacio_roto()); k.correr()
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

    print("\nAutoprueba pasada: el auditor detecta los defectos sembrados.")
    print("Esto valida el DETECTOR, no valida ningun espacio real.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
