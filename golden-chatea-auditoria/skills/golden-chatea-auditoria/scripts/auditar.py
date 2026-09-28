#!/usr/bin/env python3
"""
AUDITOR · golden-chatea-auditoria

Corre los controles mecanicos del catalogo (references/controles.md) sobre un DUMP
producido por extraer.py y emite hallazgos con evidencia y cobertura medida.

Uso:
    python3 auditar.py <DUMP.json> [opciones]

Opciones:
    --json <archivo>        vuelca universo, hallazgos y cobertura como JSON
    --decisiones <archivo>  libro de decisiones del dueno: lo ya resuelto NO se vuelve a
                            gritar (se muestra aparte, con su motivo y su fecha)
    --anterior <DUMP.json>  diff contra una corrida previa: que se movio desde entonces
    --handoff <archivo.md>  escribe el paquete listo para la skill que SI corrige
    --alcance <que>         config (POR DEFECTO) · productos · todo. Esta skill audita la
                            CONFIGURACION de los asistentes; lo de producto se aparta y se
                            DECLARA con su severidad, nunca se omite en silencio.
    --incluir-excluidos     audita tambien los asistentes que FER saco del ecosistema
                            (hoy: Remarketing IA). Solo cuando FER lo pida para un espacio;
                            sin la bandera se apartan y se declaran contados en el universo.

NO escribe nada en Chatea. Audita y reporta.

Lo que este script NO puede juzgar y queda para lectura humana (marcado H en el catalogo):
coherencia del prompt con el producto real, estructura narrativa, claims del empaque,
URLs vivas, subflujo vivo detras de un disparador, y los cruces contra Dropi, Shopify y Meta.
Esos se declaran como NO VERIFICADO en la cobertura, nunca se omiten en silencio.
"""

import hashlib
import os
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TOPES = json.loads((RAIZ / "assets" / "topes-nativos.json").read_text())

# 🔴 ASISTENTES QUE FER SACO DEL ECOSISTEMA. No se auditan por NINGUNA puerta: ni como faltantes
# (B6), ni su pais (L4), sus topes, su disparador (D3/D5) o su contenido. Hasta el 2026-09-24 el
# JSON de esperados ya decia `"opcional": true` para Remarketing IA y este script no leia esa
# bandera (0 usos): B6 lo gritaba igual. Una regla escrita donde se lee y no donde se ejecuta.
# Por eso el corte se hace AL CARGAR el inventario: sus campos se apartan antes de que los vea
# ningun control, y se DECLARAN contados en el universo (apartar es legitimo; esconder, no).
# Opt-in: vuelven solo si FER lo pide para un espacio concreto, con --incluir-excluidos.
EXCLUIDOS_POR_FER = {
    "[remarketing ia": "FER: salio del ecosistema el 21-sep-2026; no se configura ni se audita (24-sep)",
}


def _llave(s):
    """Minusculas, sin tildes y sin nada que no sea letra o numero: "[Remarketing  IA]",
    "[REMARKETING-IA]" y "[Remarketing IA]" dan la misma llave (verificador, 24-sep)."""
    s = unicodedata.normalize("NFKD", str(s or "")).lower()
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)))


# Las mismas exclusiones, pasadas por _llave: un campo es del asistente si su nombre EMPIEZA asi.
_LLAVES_EXCLUIDAS = [_llave(p) for p in EXCLUIDOS_POR_FER]


def es_excluido_por_fer(nombre):
    """Campo de bot de un asistente excluido: el nombre empieza por su prefijo."""
    k = _llave(nombre)
    return any(k.startswith(p) for p in _LLAVES_EXCLUIDAS)


# Los agentes de IA no se llaman como los campos: el de Remarketing es "Agente de Remarketing",
# sin "IA". Comparar contra la llave del campo ("remarketingia") no lo encontraba (medido 24-sep).
_AGENTES_EXCLUIDOS = ["remarketing"]


def es_agente_excluido_por_fer(nombre):
    """Agente o tarea de IA de un asistente excluido: su nombre CONTIENE la palabra."""
    k = _llave(nombre)
    return any(p in k for p in _AGENTES_EXCLUIDOS)

# Los endpoints puramente de conteo que B4 audita. I3 (bloque_i, "lo que entra al DUMP se
# audita o se declara") usa esta MISMA lista para decidir que zonas quedan sin control: dos
# listas separadas se desincronizan la primera vez que alguien edita una y no la otra — medido:
# I3 decia que estos endpoints no tenian control cuando B4 ya los contaba. Una sola lista, dos
# lectores.
ENDPOINTS_B4 = ("/flow/subflows", "/flow/tags", "/flow/ai-agents", "/flow/ai-tasks",
                "/flow/inbound-webhooks", "/flow/segments", "/flow/agents")

TECHO_ESCAPADO = TOPES["techo_bot_field"]["practico_escapado"]
ALERTA = TOPES["techo_bot_field"]["alerta_porcentaje"]

_ruta_prod = RAIZ / "assets" / "campos-de-producto.json"
PATRONES_PRODUCTO = [re.compile(p) for p in (
    json.loads(_ruta_prod.read_text())["patrones"] if _ruta_prod.exists() else [])]


def es_campo_de_producto(nombre):
    """El disparador NO entra: nombra productos pero es cableado, o sea configuracion."""
    return any(rx.match(nombre or "") for rx in PATRONES_PRODUCTO)


PREFIJOS_CONOCIDOS = [
    "[Comentarios]", "[Comentarios IA]", "[Ventas Wp]", "[Producto Ventas Wp]",
    "[Logistico]", "[Logistica]", "[Logístico]", "[Carritos IA]", "[Carritos]",
    "[Remarketing IA]", "[WhatsApp IA]", "[Whatsapp IA]", "[Novedades]",
    "[Minimax]", "[Meta]", "[Integraciones]", "[General]", "[Confirmaciones]",
    "[GOLDEN Comentarios]",
]

# Secuencias que delatan un texto que se guardo con la codificacion rota. El acento se
# verifica EN EL RENDER: aqui se mira el valor tal como quedo guardado en el servidor.
# El escapado se mide SIEMPRE asi, en linea, sobre el valor tal como lo guarda el servidor:
#     len(json.dumps(valor)[1:-1])
# Hubo un helper `escapado()` que hacia doble codificacion para los no-str y devolvia otro
# numero; se borro en GCA1.4 porque un helper que mide distinto que el codigo real es una
# trampa para el proximo editor, no una comodidad.

MOJIBAKE = ["Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "Ã‘", "â€™", "â€œ", "â€\x9d",
            "Â¿", "Â¡", "Ã\x81", "ï¿½", "�"]

PLACEHOLDERS = ["{{", "TU_TOKEN", "TU_NOMBRE", "TU_TIENDA", "XXXX", "[NOMBRE",
                "[PRODUCTO", "lorem ipsum", "ejemplo.com", "PONER AQUI", "PENDIENTE:"]

# La LISTA de arriba caza los huecos que ya conocemos por su nombre. Eso es exactamente el
# modo de fallo que esta skill le prohibe a los demas: el detector solo mira donde le
# sembraron el defecto. Medido en Golden el 2026-08-22: un producto ACTIVO y registrado en el
# disparador llevaba `[AQUI VAN LOS DATOS DE PAGO ANTICIPADO: Nequi/Daviplata + titular]` en
# pleno paso de cobro, y `[IMAGEN 1 — URL]` en el embudo. Ninguno estaba en la lista, asi que
# el auditor los dio por buenos. Se caza la CLASE: corchete con mayusculas sostenidas o con
# una palabra de encargo dentro — el idioma con el que un humano se deja una nota a si mismo.
# El corchete de VARIABLE del flujo va en minusculas ([total], [saldo]) y no dispara.
# DOS niveles de confianza, porque medir importa mas que gritar. Contrastado contra los 12
# productos reales de un espacio: la version que trataba "mayusculas sostenidas" como hueco acuso 4
# corchetes y solo 1 era real — los otros 3 eran variables de plantilla ([CATEGORIA],
# [NOMBRE ASESORA]) que el motor de "Producto en Segundos" rellena, y una variable larga con
# instruccion adentro en la lista de datos del pedido. Un auditor que acusa 3 de 4 en falso
# ensena al dueno a ignorarlo.
#
# ALTA confianza: el corchete lleva un VERBO DE ENCARGO — un humano dejandose una nota.
HUECO_DE_EDITOR = re.compile(
    r"\[[^\]\n]{0,90}"
    r"(AQU[IÍ] VA|AQU[IÍ] IR|PONER|POR COMPLETAR|FALTA |COMPLETAR|PENDIENTE|REEMPLAZAR|"
    r"TU NOMBRE|TU TIENDA|XXX)"
    r"[^\]\n]{0,90}\]", re.I)

# BAJA confianza: corchete en mayusculas sostenidas. Puede ser plantilla viva o hueco.
# Se reporta como DUDA para confirmar, nunca como muerte.
CORCHETE_MAYUSCULAS = re.compile(r"\[[^\]\n]{0,90}[A-ZÁÉÍÓÚÑ]{4,}[^\]\n]{0,90}\]")

# Los mismos patrones que redacta el extractor. Aqui sirven para lo contrario: detectar
# lo que NO se redacto, y para contar credenciales alli donde el nombre del campo no delata.
PATRONES_SECRETO = [
    ("OpenAI", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}")),
    ("ElevenLabs", re.compile(r"sk_[A-Za-z0-9]{24,}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("Meta", re.compile(r"EAA[A-Za-z0-9]{40,}")),
    ("Shopify", re.compile(r"shpat_[A-Fa-f0-9]{20,}")),
    ("xAI", re.compile(r"xai-[A-Za-z0-9]{20,}")),
    ("Google", re.compile(r"AIza[A-Za-z0-9_\-]{30,}")),
]

INTERRUPTOR = re.compile(r"^(activar|activo|habilitar|habilitado|esta_activo|evaluar)")
APAGADO = {"no", "false", "0", "off", "No", "NO", "False", False, 0}

SEV = {"MUERTO": "🔴", "ANUNCIADA": "🟠", "FUGA": "🟡", "DUDA": "🔵"}

# Esta skill audita y NO escribe. Cada hallazgo corregible se reparte a la skill que SI
# escribe ese campo, para que el paquete de correccion salga masticado y no en prosa.
DUENA_POR_PREFIJO = {
    "[Producto Ventas Wp]": "golden-chatea-pro-config-ventas-wp",
    "[Ventas Wp]": "golden-chatea-pro-config-ventas-wp",
    "[Comentarios": "golden-chatea-pro-config-comentarios",
    "[GOLDEN Comentarios]": "golden-chatea-pro-config-comentarios",
    "[Logistico]": "golden-chatea-pro-config-logistico",
    "[Logístico]": "golden-chatea-pro-config-logistico",
    "[Logistica]": "golden-chatea-pro-config-logistico",
    "[Novedades]": "golden-chatea-pro-config-logistico",
    "[Carritos": "golden-chatea-pro-config-carritos",
    "[Remarketing IA]": "golden-chatea-pro-config-ventas-wp",
    "[Integraciones]": "(panel de Chatea · no hay skill: se toca a mano)",
}


def _valor_trivial(v):
    """Un valor es TRIVIAL si por su FORMA no puede llegarle a un cliente: booleano, numero,
    version, o un JSON cuyas hojas son todas de esas. NO se mide por longitud -- medir por
    longitud acusaria al idioma y dejaria pasar un placeholder corto que si sale en pantalla
    (el caso real: "string" repetido en los 13 huecos de plantilla de mensaje)."""
    import re as _re
    SIMPLE = _re.compile(r"^(true|false|si|no|none|null|0|1|\d+|\d+(?:\.\d+)+)$", _re.I)

    def hoja_trivial(x):
        if isinstance(x, bool) or isinstance(x, (int, float)) or x is None:
            return True
        if isinstance(x, str):
            return not x.strip() or bool(SIMPLE.match(x.strip()))
        return False

    if isinstance(v, str):
        t = v.strip()
        if hoja_trivial(t):
            return True
        try:
            v = json.loads(t)
        except Exception:                                     # noqa: BLE001
            return False
    if isinstance(v, dict):
        return all(_valor_trivial(x) if isinstance(x, (dict, list)) else hoja_trivial(x)
                   for x in v.values()) and bool(v)
    if isinstance(v, list):
        return all(_valor_trivial(x) if isinstance(x, (dict, list)) else hoja_trivial(x)
                   for x in v) and bool(v)
    return hoja_trivial(v)


class Auditoria:
    # Ley de FER, 2026-09-05, en su voz: "esta skill es exclusivamente para analizar
    # configuracion, configuracion de asistentes, no vemos productos". Por eso el alcance
    # por defecto es `config` y hay que PEDIR explicitamente el de producto.
    ALCANCES = ("config", "productos", "todo")

    def __init__(self, dump, alcance="config"):
        if alcance not in self.ALCANCES:
            raise ValueError(f"alcance debe ser uno de {self.ALCANCES}, no {alcance!r}")
        self.d = dump
        self.alcance = alcance
        # Lo que el alcance aparta NO se tira: se guarda con su severidad y se cuenta en el
        # informe. Recortar es legitimo; esconder es lo que convierte un auditor en adorno.
        self.fuera_de_alcance = []
        self.hallazgos = []
        self.cobertura = []          # (bloque, control, estado, revisados, nota)
        self.campos = {}
        self.incluir_excluidos = False   # opt-in de FER: ver EXCLUIDOS_POR_FER
        self.excluidos_por_fer = []      # nombres de campo apartados, se declaran en el universo
        self.universo = {}
        self.productos = {}
        self._cache = {}
        self._vistos = set()
        # CONTROL K1 · la decision CADUCA sola: `evidencia_al_decidir` es la foto del dia
        # en que se tomo, y si la de hoy difiere el hallazgo vuelve a contar.
        self.decisiones = {}     # clave -> {motivo, fecha, reabrir_si, evidencia_al_decidir}
        self._reabiertos = []    # decisiones que caducaron porque la situacion cambio
        self._sin_foto = []      # decisiones sin evidencia_al_decidir: no pueden caducar
        self.cambios = []        # diff contra la corrida anterior

    # ---------------------------------------------------------------- utilidades
    def falla(self, control, sev, titulo, evidencia, consecuencia="", accion="",
              objetivo="", campo="", skill_duena=""):
        """objetivo: identificador ESTABLE de lo que falla (campo, producto, grupo).

        Es lo que permite que una decision del dueno sobreviva a la siguiente corrida:
        el titulo lleva conteos que cambian ("8 de 12 ranuras"), el objetivo no.
        """
        huella = (control, titulo, evidencia[:200])
        if huella in self._vistos:      # un mismo defecto se reporta UNA vez
            return
        self._vistos.add(huella)
        # La skill duena se infiere del prefijo del campo cuando no se declara: asi el
        # paquete de correccion sale repartido sin tener que anotarlo en cada hallazgo.
        if not skill_duena:
            marca = campo or titulo
            for prefijo, duena in DUENA_POR_PREFIJO.items():
                if prefijo in marca:
                    skill_duena = duena
                    break
        if not campo:
            m = re.search(r"`(\[[^`]+\]?[^`]*)`", titulo)
            if m:
                campo = m.group(1)
        clave_base = f"{control}|{objetivo or campo or titulo}"
        if objetivo:
            # `objetivo` fue elegido a mano por la llamada como identificador AGREGADO y
            # deliberado (ej. "huerfanos-con-pauta" agrupa varios productos a proposito):
            # se respeta tal cual, es la clave estable que sobrevive a los conteos del titulo.
            clave = clave_base
        else:
            # Sin un `objetivo` explicito, dos hallazgos DISTINTOS del mismo campo (dos huecos
            # de texto distintos, dos entradas distintas del mismo disparador) caian bajo la
            # MISMA clave `control|campo`: una sola decision del dueno los silenciaba a los dos
            # sin que nadie lo notara. Medido: `D3|[Remarketing IA] Disparador de productos`
            # cubria 5 hallazgos de una sola vez, y `F3|[Producto Ventas Wp] 8` mezclaba un
            # rojo con un azul bajo la misma clave. Se afina con una huella corta del contenido
            # especifico (la evidencia), no con la posicion en la corrida: el contenido no se
            # mueve aunque el orden de iteracion cambie.
            huella_corta = hashlib.sha1(evidencia.encode("utf-8", "replace")).hexdigest()[:8]
            clave = f"{clave_base}::{huella_corta}"
        h = {
            "control": control, "severidad": sev, "titulo": titulo,
            "evidencia": evidencia, "consecuencia": consecuencia, "accion": accion,
            "clave": clave, "campo": campo, "skill_duena": skill_duena,
        }
        # El libro de decisiones: lo que el dueno ya resolvio no se vuelve a gritar.
        #
        # Se acepta la clave en DOS formas, y las dos son legitimas:
        #   FINA   `control|campo::huella` — silencia UN hallazgo concreto.
        #   AMPLIA `control|campo`         — silencia TODOS los de ese campo/control.
        # Sin esta doble lectura, anadir la huella corta rompio EN SILENCIO todas las
        # decisiones ya escritas: medido el 2026-08-25, 4 de las 6 decisiones del libro de
        # Golden dejaron de casar y sus hallazgos volvieron a gritar como si nadie los
        # hubiera resuelto. Una clave que cambia de forma con una mejora del codigo no es
        # una clave estable, y el libro entero vale por su estabilidad.
        d = self.decisiones.get(clave)
        forma = "fina"
        if d is None:
            d = self.decisiones.get(clave_base)
            forma = "amplia"
        if d:
            h["decision"] = d
            h["decision_forma"] = forma
            h["clave_decidida"] = clave if forma == "fina" else clave_base
            # `reabrir_si` era PROSA que nadie evaluaba: solo se imprimia. La decision de los
            # huerfanos dice "reabre si se les carga un id de anuncio" y el dia que se cargara,
            # el hallazgo habria seguido silenciado — la promesa de que el libro no es una
            # alfombra no la sostenia nada. Lo que el codigo SI puede verificar es si la
            # SITUACION cambio: se guarda la evidencia del dia en que se decidio y se compara.
            # Cubre el caso general (se cargo un anuncio, el campo crecio, aparecio otro
            # producto) sin inventar un lenguaje de condiciones que nadie va a escribir bien.
            antes = d.get("evidencia_al_decidir")
            if antes is not None and antes.strip() != evidencia.strip():
                h["severidad_original"] = sev
                h["decision_caduca"] = True
                h["evidencia_al_decidir"] = antes
                self._reabiertos.append((h["clave_decidida"], antes, evidencia))
            else:
                h["severidad_original"] = sev
                h["severidad"] = "DECIDIDO"
                if antes is None:
                    self._sin_foto.append(h["clave_decidida"])
        # El alcance se aplica AQUI y no al leer los campos: asi todos los controles
        # siguen corriendo sobre el universo entero y los conteos del informe no mienten.
        # Lo unico que cambia es donde aterriza el hallazgo.
        # 🔴 EL FILTRO VA POR LO QUE EL CONTROL JUZGA, NO POR EL NOMBRE DEL CAMPO.
        # Hasta el 2026-09-08 casaba solo `es_campo_de_producto(h["campo"])`, y con eso
        # **le estaba ocultando a FER parte de SU configuracion**: D1 (la palabra clave que
        # tiene que coincidir BYTE A BYTE entre el producto y el disparador) apunta a
        # `[Producto Ventas Wp] N`, asi que en la corrida por defecto se archivaba como "de
        # producto" y no se reportaba. Un desajuste de palabra clave es CABLEADO puro y deja
        # el producto sin arrancar. El propio SKILL.md ya decia lo contrario que el codigo:
        # "el disparador NO entra ahi: nombra productos, pero es cableado del asistente".
        # Lo caz el golden-verificador sembrando el sabotaje y viendo el hallazgo aterrizar
        # en `fuera_de_alcance`.
        #
        # LA FRONTERA, y es la que cierra el hueco por el que dos chats se metieron en
        # productos el mismo dia: **un control de configuracion que APUNTA a un campo de
        # producto mira el CABLEADO del campo, jamas su CONTENIDO.** El nombre de la ranura,
        # si esta registrada en el disparador, si su palabra clave coincide, si esta activa,
        # cuanto ocupa el campo y si lleva una credencial: todo eso es cableado. Que producto
        # es, su marca, su precio, sus imagenes: eso es contenido, y solo se juzga con
        # --alcance productos.
        CABLEADO = {
            "D1",  # palabra clave byte a byte producto <-> disparador
            "D2",  # emoji de 4 bytes en el disparador
            "D3",  # ranura sin entrada en el disparador (y su gemelo D3b)
            "D3b",
            "D4",  # estado incoherente entre producto y disparador
            "D5",  # ranuras del disparador mal contadas
            "D6",  # producto activo sin ningun id de anuncio
            "C1", "C2", "C3", "C4", "C5", "C6",   # techos y tipo del campo
            "E3",  # credencial de voz heredada
            "G3",  # credencial guardada como valor de un campo
        }
        de_producto = es_campo_de_producto(h["campo"]) and h.get("control") not in CABLEADO
        if (self.alcance == "config" and de_producto) or \
           (self.alcance == "productos" and not de_producto):
            self.fuera_de_alcance.append(h)
            return
        self.hallazgos.append(h)

    def cubre(self, control, estado, revisados=None, nota=""):
        self.cobertura.append({"control": control, "estado": estado,
                               "revisados": revisados, "nota": nota})

    @staticmethod
    def contenedores(obj, ruta=""):
        """Va soltando (ruta, dict) de cada diccionario a cualquier profundidad."""
        if isinstance(obj, dict):
            yield ruta, obj
            for k, v in obj.items():
                yield from Auditoria.contenedores(v, f"{ruta}.{k}" if ruta else str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from Auditoria.contenedores(v, f"{ruta}.{i}")

    @staticmethod
    def caminar(obj, ruta=""):
        """Recorre un objeto anidado y va soltando (ruta, valor) de cada hoja."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from Auditoria.caminar(v, f"{ruta}.{k}" if ruta else str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from Auditoria.caminar(v, f"{ruta}.{i}")
        else:
            yield ruta, obj

    def valor_json(self, campo):
        if campo["name"] in self._cache:
            return self._cache[campo["name"]]
        v = self._valor_json(campo)
        self._cache[campo["name"]] = v
        return v

    def _valor_json(self, campo):
        """Parsea el valor de un campo. Un valor que no parsea estando declarado
        array/longtext es sospecha de truncada silenciosa, no un descuido de formato.

        `text` topa igual que `array` (controles.md C4) y en la practica puede
        guardar el mismo JSON de producto que `array` — el tipo declarado no
        decide si el contenido es JSON, intentar parsear si. Por eso `text`
        tambien se intenta, pero SIN levantar C6 si falla: un campo `text`
        corriente (no producto) no tiene por que ser JSON, y no es sospechoso."""
        v = campo.get("value")
        if not (isinstance(v, str) and v.strip()):
            return v
        tipo = campo.get("var_type")
        if tipo in ("array", "longtext"):
            try:
                return json.loads(v)
            except json.JSONDecodeError as e:
                self.falla("C6", "MUERTO",
                           f"El campo `{campo['name']}` no parsea como JSON",
                           f"tipo {campo['var_type']}, {len(v):,} caracteres, error: {e}",
                           "Es el patron de una truncada silenciosa: la API responde 200 ok "
                           "y guarda el contenido cortado.",
                           "Reescribir el campo completo y releerlo del servidor.")
                return None
        if tipo == "text":
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    def filas(self, clave):
        """Las filas de un endpoint paginado, o [] si respondio con error.

        El extractor guarda el error del servidor TAL CUAL cuando la primera pagina falla:
        el valor deja de ser una lista y pasa a ser un diccionario de error. Iterarlo como
        si fuera lista revienta la auditoria entera con un traceback, y un 500 puntual de
        la API no puede costar el informe completo. Aqui se degrada: se declara la zona
        como no medida y se sigue.
        """
        v = self.d.get(clave)
        if isinstance(v, list):
            return v
        if isinstance(v, dict) and ("_ERROR" in v or "_ERROR_HTTP" in v):
            self.falla("B1", "DUDA",
                       f"`{clave}` no se pudo leer del servidor",
                       f"{json.dumps(v, ensure_ascii=False)[:160]}",
                       "Esa zona queda sin medir: su silencio NO es salud.",
                       "Repetir la extraccion de ese endpoint antes de concluir sobre el.",
                       objetivo=f"ilegible-{clave}")
            return []
        return []

    def _apartar_excluidos(self, campos):
        """Indexa los campos y aparta los de asistentes que FER saco del ecosistema."""
        todos = {c["name"]: c for c in campos if isinstance(c, dict) and "name" in c}
        if self.incluir_excluidos:
            self.excluidos_por_fer = []
            return todos
        self.excluidos_por_fer = sorted(n for n in todos if es_excluido_por_fer(n))
        return {n: c for n, c in todos.items() if n not in self.excluidos_por_fer}

    def campos_pre(self):
        """Los campos indexados, disponibles ya en el bloque A."""
        if not self.campos:
            self.campos = self._apartar_excluidos(self.filas("/flow/bot-fields"))
        return self.campos

    # ------------------------------------------------------- A · identidad y acceso
    def bloque_a(self):
        me = self.d.get("/me") or {}
        if "_ERROR_HTTP" in me or "_ERROR" in me:
            self.falla("A1", "MUERTO", "El token no responde", json.dumps(me)[:200])
            self.cubre("A1", "corrido", 1, "1 endpoint revisado: /me no respondio 200")
            return
        self.universo["cuenta"] = me.get("email") or me.get("name") or "?"
        self.cubre("A1", "corrido", 1, f"/me respondio: {self.universo['cuenta']}")

        # La identidad sale del servidor: el prefijo del var_ns de los campos, nunca el
        # nombre del archivo del token.
        campos = self.filas("/flow/bot-fields")
        ns = {re.match(r"^(f\d+)", c.get("var_ns", "")).group(1)
              for c in campos if isinstance(c, dict)
              and re.match(r"^(f\d+)", c.get("var_ns", "") or "")}
        self.universo["espacios_ns"] = sorted(ns)
        if len(ns) > 1:
            self.falla("A2", "DUDA", "Los campos vienen de mas de un espacio",
                       f"prefijos var_ns encontrados: {sorted(ns)}")
        self.cubre("A2", "corrido", len(campos),
                   f"espacio medido en el servidor: {sorted(ns) or 'no determinado'}")

        # A3 · el espacio corresponde al negocio que se dijo auditar
        pais = (self.campos_pre().get("[Comentarios IA] Pais")
                or self.campos_pre().get("[Comentarios IA] País") or {}).get("value") or ""
        monedas = {str(v) for r, v in self.caminar(
            [self.valor_json(c) for c in self.campos_pre().values()
             if c.get("name", "").startswith("[Producto Ventas Wp]")])
            if r.endswith(".moneda") and v}
        self.universo["pais_declarado"] = pais.strip() or "(vacio)"
        self.universo["monedas_en_productos"] = sorted(monedas)
        COHERENTE = {"COLOMBIA": "COP", "MEXICO": "MXN", "CHILE": "CLP", "PERU": "PEN",
                     "ECUADOR": "USD", "PANAMA": "USD", "PARAGUAY": "PYG",
                     "GUATEMALA": "GTQ", "ARGENTINA": "ARS", "BRASIL": "BRL"}
        esperada = COHERENTE.get(pais.strip().upper())
        if esperada and monedas and monedas != {esperada}:
            self.falla("A3", "DUDA",
                       "El pais declarado y la moneda de los productos no concuerdan",
                       f"pais={pais.strip()!r} espera {esperada}, productos en {sorted(monedas)}",
                       "Es la firma de una plantilla clonada de otro pais.",
                       "Confirmar cual manda antes de tocar nada.")
        self.cubre("A3", "corrido", len(monedas) + 1,
                   f"pais {pais.strip() or '(vacio)'} contra {sorted(monedas)}")

        # A4 · los canales. OJO CON LO QUE MIDE ESTE ENDPOINT: devuelve que canales estan
        # DISPONIBLES en el plan (1 disponible / 0 no), NO si estan conectados y vivos. Leer
        # el 0 como "canal caido" es un falso positivo medido: Golden tiene `apple: 0` — un
        # canal que su plan no incluye y que ningun asistente usa — y salio en 🔴 MUERTO.
        # La conexion VIVA no la expone la API: se mira en el panel, y eso ya lo declara A5.
        REQUERIDOS = ("whatsapp", "whatsapp_cloud", "facebook", "instagram")
        canales = self.d.get("/workspace-settings/channels")
        disponibles, no_disponibles, ilegibles = [], [], []
        if canales:
            for ruta, hoja in self.caminar(canales):
                nombre = ruta.split(".")[-1]
                if nombre in ("status",):
                    continue
                if not isinstance(hoja, (int, bool)):
                    # P59: la hoja se tiraba en silencio y, al calcular los requeridos por
                    # los que estan en `no_disponibles`, un canal en null salia PRESENTE.
                    # Medido por ARSENAL: whatsapp=None daba "requeridos presentes 4 de 4".
                    ilegibles.append(f"{nombre} ({type(hoja).__name__})")
                    continue
                (disponibles if hoja else no_disponibles).append(nombre)
        # Dos cosas distintas, y antes se mezclaban en una: el plan que NO lo incluye (rojo,
        # el asistente no puede operar) y el que no se pudo COMPROBAR (duda: ausente de la
        # respuesta o con un valor que no es un interruptor).
        faltan_req = [c for c in REQUERIDOS if c in no_disponibles]
        sin_comprobar = [c for c in REQUERIDOS
                         if c not in no_disponibles and c not in disponibles]
        if canales and sin_comprobar:
            self.falla("A4", "DUDA",
                       f"{len(sin_comprobar)} canales REQUERIDOS no se pudieron comprobar",
                       f"{sin_comprobar} · hojas ilegibles: {ilegibles or 'ninguna'}",
                       "No estan en la respuesta del endpoint o su valor no es un "
                       "interruptor. No se sabe si el plan los incluye: antes contaban "
                       "como presentes.",
                       "Mirarlos en el panel del workspace.",
                       objetivo="canal-requerido-sin-comprobar")
        if faltan_req:
            self.falla("A4", "MUERTO",
                       "Un canal que los asistentes NECESITAN no esta disponible en el plan",
                       f"{faltan_req} · disponibles: {len(disponibles)}",
                       "El asistente que dependa de ese canal no puede operar.",
                       "Revisar el plan del workspace en el panel.",
                       objetivo="canal-requerido")
        self.universo["canales"] = {
            "disponibles en el plan": len(disponibles),
            "no disponibles": ", ".join(no_disponibles) or "ninguno",
            "requeridos presentes":
                f"{len([c for c in REQUERIDOS if c in disponibles])} de {len(REQUERIDOS)}"
                + (f" · {len(sin_comprobar)} sin comprobar" if sin_comprobar else ""),
            "hojas ilegibles": ", ".join(ilegibles) or "ninguna"}
        self.cubre("A4", "corrido" if canales else "sin_datos",
                   len(disponibles) + len(no_disponibles),
                   "disponibilidad en el plan; la conexion VIVA se mira en el panel (A5)"
                   if canales else "el endpoint no devolvio datos")

        self.cubre("A5", "NO_VERIFICADO",
                   nota="el token de Meta se comprueba en el panel; la API no lo expone")

    # ---------------------------------------------------------- B · inventario
    def bloque_b(self):
        campos = self.filas("/flow/bot-fields")
        self.campos = self._apartar_excluidos(campos)
        conteo = (self.d.get("_conteos") or {}).get("/flow/bot-fields") or {}
        traidos, declarados = conteo.get("traidos"), conteo.get("declarados_por_servidor")
        self.universo["campos_bot"] = len(self.campos) + len(self.excluidos_por_fer)
        self.universo["campos_excluidos_por_fer"] = {
            "cuantos": len(self.excluidos_por_fer), "campos": self.excluidos_por_fer,
            "motivo": "; ".join(EXCLUIDOS_POR_FER.values())} if self.excluidos_por_fer else 0
        self.universo["campos_declarados"] = declarados

        if isinstance(declarados, int) and traidos != declarados:
            self.falla("B1", "MUERTO",
                       "El inventario esta incompleto: la paginacion no se agoto",
                       f"traidos {traidos}, el servidor declara {declarados}",
                       "Un denominador incompleto invalida el resto del informe.",
                       "Repetir la extraccion antes de leer ningun hallazgo.")
        self.cubre("B1", "corrido", len(self.campos),
                   f"servidor declara {declarados}"
                   + (f" · {len(self.excluidos_por_fer)} apartados por decision de FER "
                      f"(no faltan: se traen y no se auditan)" if self.excluidos_por_fer else ""))

        # El mismo control sobre TODO lo que pagina. Ausencia no es prueba: un listado
        # corto puede ser "medido y vacio" o "no medido", y hay que distinguirlo.
        incompletos = 0
        for ruta, c in (self.d.get("_conteos") or {}).items():
            if ruta == "/flow/bot-fields":
                continue
            t, dec = c.get("traidos"), c.get("declarados_por_servidor")
            if isinstance(t, int) and isinstance(dec, int) and t != dec:
                incompletos += 1
                self.falla("B1", "DUDA",
                           f"`{ruta}` se trajo incompleto",
                           f"traidos {t}, el servidor declara {dec} (faltan {dec - t})",
                           "Todo control que dependa de ese listado tiene un denominador corto: "
                           "lo que no aparece puede existir y no haberse medido.",
                           "Repetir la extraccion de ese endpoint antes de concluir nada sobre el.")
        self.cubre("B1b", "corrido", len(self.d.get("_conteos") or {}),
                   f"{incompletos} listados incompletos")
        ilegibles = [h for h in self.hallazgos if h["clave"].startswith("B1|ilegible")]
        self.cubre("B7", "corrido", len(self.d.get("_conteos") or {}),
                   f"{len(ilegibles)} endpoints ilegibles declarados en vez de reventar")

        # B2 · el CONTEO se puede medir por API, pero el LIMITE del workspace (lo que el
        # control realmente tiene que juzgar, controles.md B2) no lo expone ningun endpoint —
        # se lee en el panel. Declararlo "corrido" cuando la paginacion se agoto sonaba a
        # verificado, pero nunca se comparo contra ningun tope: es NO_VERIFICADO siempre, con
        # el conteo (y si la paginacion quedo corta) como nota, no como veredicto.
        uf = self.filas("/flow/user-fields")
        self.universo["campos_usuario"] = len(uf) if uf else None
        dec_uf = ((self.d.get("_conteos") or {}).get("/flow/user-fields") or {}
                  ).get("declarados_por_servidor")
        completo = (dec_uf is None) or (self.universo["campos_usuario"] == dec_uf)
        nota_b2 = "el limite por workspace se lee en el panel, no por API"
        if isinstance(uf, list) and not completo:
            nota_b2 = (f"el servidor declara {dec_uf}: contados "
                       f"{self.universo['campos_usuario']} de {dec_uf}; ademas, {nota_b2}")
        self.cubre("B2", "NO_VERIFICADO", self.universo["campos_usuario"], nota_b2)

        # Asistentes por prefijo real, no por lo que se supone instalado.
        prefijos = {}
        for n in self.campos:
            m = re.match(r"^\[[^\]]+\]", n)
            prefijos.setdefault(m.group(0) if m else "(sin prefijo)", []).append(n)
        self.universo["asistentes"] = {k: len(v) for k, v in sorted(prefijos.items())}
        desconocidos = [p for p in prefijos if p not in PREFIJOS_CONOCIDOS]
        if "(sin prefijo)" in prefijos:
            # 🔴 SIN CLASIFICAR NO ES "CONFIGURACION". Hasta el 2026-09-08 la configuracion
            # se definia POR EXCLUSION -- existia campos-de-producto.json y todo lo demas se
            # asumia configuracion -- asi que un campo que nadie habia clasificado entraba
            # como config sin que nadie lo decidiera, y "auditar la configuracion" no tenia
            # denominador. Ahora se DECLARA como lo que es: sin clasificar.
            self.falla("B3", "DUDA",
                       f"{len(prefijos['(sin prefijo)'])} campos SIN CLASIFICAR: no estan en "
                       f"campos-de-configuracion.json ni en campos-de-producto.json",
                       f"{sorted(prefijos['(sin prefijo)'])}",
                       "NO se asumen configuracion: un campo que nadie clasifico no es config "
                       "por defecto. Quedan fuera de los controles por asistente porque no se "
                       "sabe quien los lee, y eso se dice en vez de callarlo.",
                       "Clasificarlos en assets/campos-de-configuracion.json (si son del "
                       "negocio) o en campos-de-producto.json (si son contenido), o declararlos "
                       "fuera de alcance con su motivo.")
        if desconocidos:
            self.falla("B3", "DUDA",
                       "Hay asistentes o versiones que esta skill todavia no sabe auditar",
                       f"prefijos no catalogados: {desconocidos}",
                       "Sus campos quedan fuera de los controles especificos.",
                       "Anadirlos al catalogo o declararlos fuera de alcance en el informe.")
        self.cubre("B3", "corrido", len(prefijos))

        # B8 · el MISMO asistente escrito de dos formas. El catalogo PREFIJOS_CONOCIDOS
        # absorbio las variantes ([Logistico] con y sin tilde, [WhatsApp IA] con y sin
        # mayuscula) y al catalogarlas las volvio invisibles: B3 solo mira lo que NO esta
        # en el catalogo. Medido el 2026-09-05 sobre los dos unicos espacios auditados
        # hasta entonces, de dos paises distintos: LOS DOS las traen. Diez
        # versiones de esta skill pasaron por encima sin verlo.
        def _plano(p):
            d = unicodedata.normalize("NFD", p)
            return "".join(c for c in d if unicodedata.category(c) != "Mn").lower()

        familias = {}
        for p in prefijos:
            familias.setdefault(_plano(p), []).append(p)
        for _, variantes in sorted(familias.items()):
            if len(variantes) < 2:
                continue
            variantes = sorted(variantes, key=lambda v: (-len(prefijos[v]), v))
            mayor, menores = variantes[0], variantes[1:]
            self.falla("B8", "DUDA",
                       "El mismo asistente aparece escrito de dos formas",
                       " · ".join(f"`{v}` en {len(prefijos[v])} campos" for v in variantes),
                       "Todo control que agrupa por prefijo los cuenta como asistentes "
                       "distintos: el inventario miente y los campos de la variante rara "
                       "quedan fuera de su familia.",
                       f"Confirmar en el panel que ningun flujo referencie el nombre viejo y "
                       f"renombrar los campos de {', '.join(menores)} a {mayor}.",
                       objetivo=mayor)
        self.cubre("B8", "corrido", len(familias),
                   "prefijos normalizados sin tildes ni mayusculas")

        # B6 · lo que FALTA, no solo lo que hay. Detectar prefijos presentes nunca puede
        # contestar "esta completa la instalacion": para eso hace falta la lista de esperados.
        ruta_esp = RAIZ / "assets" / "asistentes-esperados.json"
        if not ruta_esp.exists():
            self.falla("B6", "DUDA", "Falta la lista de asistentes esperados",
                       f"no existe {ruta_esp}",
                       "Sin ella no se puede decir si la instalacion esta completa.",
                       "Restaurar el asset desde el backup de la skill.",
                       objetivo="asset-esperados")
            self.cubre("B6", "no_corrido", 0, "falta assets/asistentes-esperados.json")
            contados = 0
            for clave in ENDPOINTS_B4:
                v = self.d.get(clave)
                self.universo[clave] = len(v) if isinstance(v, list) else None
                if isinstance(v, list):
                    contados += len(v)
            self.cubre("B4", "corrido", len(ENDPOINTS_B4),
                       f"{contados} objetos contados en {len(ENDPOINTS_B4)} endpoints")
            self._productos()
            return
        esperados = json.loads(ruta_esp.read_text())
        # Un asistente sacado del ecosistema por FER no es "esperado", y uno `opcional` no se
        # reporta cuando falta. Ninguno de los dos cuenta en el denominador: "4 de 5" con uno
        # opcional ausente lee como una instalacion incompleta que no lo es.
        evaluados = {n: f for n, f in esperados["asistentes"].items()
                     if not (not self.incluir_excluidos
                             and all(es_excluido_por_fer(c) for c in f["campos_firma"]))}
        faltan = []
        for nombre, firma in evaluados.items():
            presentes = [f for f in firma["campos_firma"] if f in self.campos]
            if not presentes:
                if firma.get("opcional"):
                    continue
                faltan.append((nombre, firma["campos_firma"]))
            elif len(presentes) < len(firma["campos_firma"]):
                self.falla("B6", "DUDA",
                           f"El asistente {nombre} esta instalado a medias",
                           f"tiene {presentes}, le faltan "
                           f"{[f for f in firma['campos_firma'] if f not in self.campos]}",
                           "Una instalacion parcial se comporta distinto segun el camino "
                           "que tome el flujo.",
                           objetivo=f"parcial-{nombre}")
        for nombre, firma in faltan:
            self.falla("B6", "DUDA",
                       f"El asistente {nombre} NO esta instalado",
                       f"no existe ninguno de sus campos firma: {firma}",
                       "Si el espacio deberia tenerlo, no esta funcionando; si no, sobra "
                       "declararlo fuera de alcance.",
                       "Instalarlo o declararlo fuera de alcance en el informe.",
                       objetivo=f"falta-{nombre}")
        obligatorios = [n for n, f in evaluados.items() if not f.get("opcional")]
        fuera = sorted(set(esperados["asistentes"]) - set(evaluados))
        self.universo["asistentes_esperados"] = (
            f"{len(obligatorios) - len(faltan)} de {len(obligatorios)} presentes"
            + (f" · no se esperan por decision de FER: {', '.join(fuera)}" if fuera else ""))
        self.cubre("B6", "corrido", len(evaluados),
                   f"{len(faltan)} sin instalar"
                   + (f" · {len(fuera)} fuera por decision de FER" if fuera else ""))

        contados = 0
        for clave in ENDPOINTS_B4:
            v = self.d.get(clave)
            self.universo[clave] = len(v) if isinstance(v, list) else None
            if isinstance(v, list):
                contados += len(v)
        self.cubre("B4", "corrido", len(ENDPOINTS_B4),
                   f"{contados} objetos contados en {len(ENDPOINTS_B4)} endpoints")

        self._productos()

    def _productos(self):
        self.productos = {}
        for n, c in self.campos.items():
            m = re.match(r"^\[Producto Ventas Wp\] (\d+)$", n)
            if m and (c.get("value") or "").strip():
                p = self.valor_json(c)
                if isinstance(p, dict):
                    self.productos[n] = p
        self.universo["ranuras_producto"] = len(self.productos)
        self.cubre("B5", "corrido", len(self.productos))

    # ------------------------------------------------------------- C · los techos
    def bloque_c(self):
        revisados = 0
        for n, c in self.campos.items():
            v = c.get("value")
            if not isinstance(v, str) or not v:
                continue
            revisados += 1
            esc = len(json.dumps(v)[1:-1])
            tipo = c.get("var_type")
            techo = TECHO_ESCAPADO if tipo in ("text", "array") else \
                TOPES["techo_bot_field"]["longtext"]
            # La frontera MEDIDA en vivo esta entre 19.895 (dispara) y 23.266 (no dispara).
            # 19.000 es la alerta prudente, no una prueba de muerte: por encima del ultimo
            # valor que se vio disparar, MUERTO; entre los dos, muerte anunciada.
            ULTIMO_VIVO = TOPES["techo_bot_field"].get("ultimo_medido_que_dispara", 19895)
            if esc > ULTIMO_VIVO and tipo in ("text", "array"):
                self.falla("C1", "MUERTO",
                           f"`{n}` pasa el ultimo tamano que se vio disparar",
                           f"{esc:,} escapados (crudo {len(v):,}, tipo {tipo}); medido en vivo: "
                           f"{ULTIMO_VIVO:,} dispara, 23.266 no",
                           "El flujo copia la config escapada y muere antes de disparar: el "
                           "asistente deja de responder sin un solo error visible.",
                           "Compactar (cada emoji pesa 12 escapados) o migrar el campo a longtext.")
            elif esc > techo:
                self.falla("C1", "ANUNCIADA",
                           f"`{n}` esta sobre el techo prudente de {techo:,} escapados",
                           f"{esc:,} escapados (crudo {len(v):,}, tipo {tipo}); la frontera "
                           f"medida esta entre {ULTIMO_VIVO:,} y 23.266",
                           "Zona en la que no se ha medido si dispara: se trata como riesgo.",
                           "Compactar hasta bajar de 19.000 escapados.")
            elif esc > techo * ALERTA:
                self.falla("C2", "ANUNCIADA",
                           f"`{n}` esta al {esc / techo:.0%} del techo escapado",
                           f"{esc:,} de {techo:,} escapados (quedan {techo - esc:,})",
                           "La proxima linea que alguien agregue lo corta solo.",
                           "Compactar ahora o migrarlo a longtext.")
        self.cubre("C1", "corrido", revisados)
        self.cubre("C2", "corrido", revisados)

        # C3 · tope nativo del formulario, ruta por ruta
        rutas_revisadas = 0
        rutas_sin_tope = 0
        sin_tope = tuple(TOPES["sin_tope_nativo"])
        for n, c in self.campos.items():
            if n.startswith(sin_tope):
                continue
            val = self.valor_json(c)
            if not isinstance(val, (dict, list)):
                continue
            for ruta, hoja in self.caminar(val):
                if not isinstance(hoja, str) or not hoja:
                    continue
                tope = self.tope_de(ruta)
                if tope is None:
                    rutas_sin_tope += 1        # P59: se cuentan y salen en la cobertura
                    continue
                rutas_revisadas += 1
                if len(hoja) > tope:
                    self.falla("C3", "ANUNCIADA",
                               f"`{n}` → `{ruta}` supera su tope nativo",
                               f"{len(hoja):,} caracteres sobre {tope:,}",
                               "Funciona hoy, pero el dia que alguien abra ese formulario en "
                               "el panel y guarde, el campo se corta y se pierde el texto.",
                               f"Recortar a {tope:,} con la skill de configuracion.")
        self.cubre("C3", "corrido", rutas_revisadas,
                   f"{rutas_sin_tope} rutas sin tope conocido, no juzgadas"
                   if rutas_sin_tope else "todas las rutas tenian tope conocido")

        # C4 · tipo del campo — text y array topan igual en 20.000 (controles.md)
        candidatos = [(n, c) for n, c in self.campos.items()
                      if c.get("var_type") in ("array", "text")
                      and len(json.dumps(c.get("value") or "")[1:-1]) > TECHO_ESCAPADO * 0.8]
        for n, c in candidatos:
            esc = len(json.dumps(c.get("value") or "")[1:-1])
            tipo = c.get("var_type")
            self.falla("C4", "ANUNCIADA",
                       f"`{n}` sigue siendo `{tipo}` y va por el {esc / TECHO_ESCAPADO:.0%}",
                       f"{esc:,} escapados; longtext daria 500.000",
                       "El tipo es inmutable: no se cambia ni por UI ni por API.",
                       "Crear un campo nuevo longtext y repuntar la referencia del flujo.")
        self.cubre("C4", "corrido", len(self.campos))

        # C5 · pares X / X Extendido
        pares = 0
        for n in list(self.campos):
            for suf in (" extendido", " Extendido"):
                if n.endswith(suf):
                    base = n[: -len(suf)]
                    if base in self.campos:
                        pares += 1
                        lb = len((self.campos[base].get("value") or "").strip())
                        le = len((self.campos[n].get("value") or "").strip())
                        if lb and le:
                            self.falla("C5", "ANUNCIADA",
                                       f"El par `{base}` / `{n}` esta poblado de los DOS lados",
                                       f"array {lb:,} caracteres · longtext {le:,}",
                                       "No se sabe cual lee el flujo, y editar el equivocado "
                                       "no cambia nada.",
                                       "Confirmar en el panel cual lee el flujo y vaciar el otro.")
                        elif lb and not le:
                            self.falla("C5", "DUDA",
                                       f"`{n}` (el longtext) esta VACIO y el array tiene datos",
                                       f"array {lb:,} · extendido 0",
                                       "Si el flujo ya migro al Extendido, esta leyendo vacio.")
        self.cubre("C5", "corrido", pares)

    def tope_de(self, ruta):
        if ruta in TOPES["por_ruta"]:
            return TOPES["por_ruta"][ruta]
        hoja = ruta.split(".")[-1]
        if hoja in TOPES["por_ruta"]:
            return TOPES["por_ruta"][hoja]
        for patron, tope in TOPES["por_sufijo_de_ruta"].items():
            pre, _, post = patron.partition(".*.")
            if pre in ruta and ruta.endswith("." + post):
                return tope
        return None

    # -------------------------------------------------------- D · disparadores
    def bloque_d(self):
        """Audita TODOS los disparadores del espacio, no solo el de Ventas Wp.

        Medido en Golden: existe ademas `[Remarketing IA] Disparador de productos`, con
        entradas que apuntan a ranuras que no existen. Mirar dos nombres fijos dejaba dos
        de cada tres disparadores sin auditar, y el informe no lo decia.
        """
        disparadores = {n: self.valor_json(c) for n, c in self.campos.items()
                        if "Disparador de productos" in n and (c.get("value") or "").strip()}
        self.universo["disparadores"] = {n: (len(v) if isinstance(v, list) else "ilegible")
                                         for n, v in disparadores.items()}
        if not disparadores:
            self.falla("D3", "MUERTO", "No hay ningun disparador de productos legible",
                       "ningun campo con 'Disparador de productos' trae contenido",
                       "Sin disparador ningun producto arranca.")
            for c in ("D1", "D2", "D3", "D4", "D5", "D6"):
                self.cubre(c, "no_corrido", 0, "sin disparador que comparar")
            return

        cargados = set(self.productos)
        comparados = entradas_totales = 0
        registrados_todos = {}

        for nombre_disp, entradas in disparadores.items():
            if not isinstance(entradas, list):
                self.falla("D3", "MUERTO", f"`{nombre_disp}` no es una lista legible",
                           f"tipo {type(entradas).__name__}")
                continue
            registrados = {}
            for i, e in enumerate(entradas):
                entradas_totales += 1
                if not isinstance(e, dict):
                    # P59: se sumaba a las entradas "revisadas" de D2/D5/D6 y no se revisaba
                    # ni se nombraba. Cobertura falsa: el denominador crecia sin denominar.
                    self.falla("D9", "MUERTO",
                               f"`{nombre_disp}`: la entrada {i} no es un objeto legible",
                               f"tipo {type(e).__name__}: "
                               f"{json.dumps(e, ensure_ascii=False)[:120]}",
                               "Ningun control la puede leer, y aun asi contaba como "
                               "entrada revisada.",
                               "Corregir o borrar esa entrada del disparador en el panel.",
                               objetivo=f"entrada-ilegible-{nombre_disp}-{i}")
                    continue
                destino = (e.get("name") or "").strip()
                if not destino:
                    self.falla("D3", self.sev_segun_estado(e, "MUERTO"),
                               f"`{nombre_disp}`: hay una entrada SIN destino",
                               f"entrada {i}: {json.dumps(e, ensure_ascii=False)[:160]}",
                               "Un disparo que entra por ahi no lleva a ningun producto."
                               + self.nota_estado(e))
                    continue
                registrados[destino] = e
                registrados_todos.setdefault(destino, []).append(nombre_disp)

                # D5 · las siete ranuras · se revisa TODA entrada, tenga producto o no
                for etiqueta in ("keyW", "idAd"):
                    valor = e.get(etiqueta) or ""
                    if not isinstance(valor, str):
                        # P59: se saltaba de D5 y del chequeo de palabra clave vacia sin
                        # decir nada. Un keyW que es lista no tiene ranuras que contar, pero
                        # que NO se pueda contar es el hallazgo.
                        self.falla("D9", "MUERTO",
                                   f"`{nombre_disp}` → `{destino}`: `{etiqueta}` no es texto",
                                   f"tipo {type(valor).__name__}: {valor!r:.120}",
                                   "El disparador espera una cadena con siete ranuras "
                                   "separadas por comas. Con otro tipo, ningun control lo "
                                   "puede juzgar.",
                                   "Corregir el tipo del campo en el panel.",
                                   objetivo=f"tipo-{etiqueta}-{nombre_disp}-{destino}")
                        continue
                    ranuras = valor.count(",") + 1
                    if ranuras != 7:
                        self.falla("D5", "DUDA",
                                   f"`{nombre_disp}` → `{destino}`: `{etiqueta}` no tiene 7 ranuras",
                                   f"{ranuras} ranuras: {valor[:120]!r}",
                                   "O el estandar de 7 esta viejo o el valor esta malformado: "
                                   "se confirma en el panel antes de tocarlo.")
                    if etiqueta == "keyW" and not valor.strip(", "):
                        self.falla("D3", self.sev_segun_estado(e, "MUERTO"),
                                   f"`{nombre_disp}` → `{destino}`: la palabra clave esta VACIA",
                                   f"{valor!r} · estado {e.get('estado')!r}",
                                   "Una entrada activa sin palabra clave no puede entrar."
                                   + self.nota_estado(e))

                # D2 · caracteres de 4 bytes
                for etiqueta in ("keyW", "idAd"):
                    texto = e.get(etiqueta) or ""
                    cuatro = [c for c in str(texto) if ord(c) >= 0x10000]
                    if cuatro:
                        self.falla("D2", "MUERTO",
                                   f"`{nombre_disp}` → `{destino}`: `{etiqueta}` tiene "
                                   "caracteres de 4 bytes",
                                   f"{[unicodedata.name(c, hex(ord(c))) for c in cuatro]}",
                                   "El disparador no los admite: se corrompe y el bot no "
                                   "arranca nunca.",
                                   "Quitar el emoji del disparador.")

            # D3 · entradas que apuntan a un campo que NO EXISTE
            # 🔴 EL DENOMINADOR ES DEL MISMO UNIVERSO QUE EL NUMERADOR. Medido el 2026-09-17
            # en el espacio de un cliente: decia "29 de 71 ACTIVAS", con 29 activas-al-vacio
            # sobre un total de 71 entradas de las que solo 55 estaban activas. El numerador
            # contaba activas y el denominador contaba todas: dos universos en una sola frase,
            # que es la puerta de cobertura falsa de la casa. Lo correcto es 29 de 55.
            # Y la PALABRA tambien estaba mal: esos campos no estan "vacios", NO EXISTEN. Un
            # campo vacio se arregla llenandolo; uno inexistente hay que crearlo o repuntar la
            # entrada. Nombrar mal el defecto manda al dueno a la pantalla equivocada.
            todas = list(registrados)
            act_todas = [n for n in todas if self.activa(registrados[n])]
            inact_todas = [n for n in todas if not self.activa(registrados[n])]
            al_vacio = sorted(set(registrados) - cargados, key=self.orden_ranura)
            vivas = [n for n in al_vacio if self.activa(registrados[n])]
            apagadas = [n for n in al_vacio if not self.activa(registrados[n])]
            if vivas:
                self.falla("D3", "MUERTO",
                           f"`{nombre_disp}`: {len(vivas)} de {len(act_todas)} entradas "
                           f"ACTIVAS apuntan a un campo que NO EXISTE "
                           f"(el disparador trae {len(todas)} entradas en total)",
                           f"{vivas}",
                           "El disparo entra y no encuentra producto.")
            if apagadas:
                self.falla("D3", "DUDA",
                           f"`{nombre_disp}`: {len(apagadas)} de {len(inact_todas)} entradas "
                           f"INACTIVAS apuntan a un campo que NO EXISTE "
                           f"(el disparador trae {len(todas)} entradas en total)",
                           f"{apagadas}",
                           "Estan apagadas, asi que hoy no disparan ni cuestan nada. Es "
                           "basura de configuracion: limpieza, no urgencia.",
                           "Borrarlas o repuntarlas cuando se vayan a encender.")

            # D1/D4 · contra el producto, cuando existe
            for destino, e in registrados.items():
                prod = self.productos.get(destino)
                if prod is None:
                    continue
                comparados += 1
                act = ((prod.get("activadores_del_flujo") or {}).get("palabras_clave") or "")
                key = e.get("keyW") or ""
                if act != key:
                    # Un producto cuya PRIMERA ranura coincide sigue arrancando: lo que
                    # esta muerto es la ranura que falta, no el producto entero.
                    prim_a = act.split(",")[0].strip()
                    prim_k = str(key).split(",")[0].strip()
                    if prim_a and prim_a == prim_k:
                        faltan = [r.strip() for r in act.split(",") if r.strip()
                                  and r.strip() not in str(key)]
                        sobran = [r.strip() for r in str(key).split(",") if r.strip()
                                  and r.strip() not in act]
                        self.falla("D1", "ANUNCIADA",
                                   f"`{destino}`: las palabras clave no coinciden, pero la "
                                   "principal si",
                                   f"en el producto: {act!r}\n     en el disparador: {key!r}\n"
                                   f"     solo en el producto: {faltan} · solo en el "
                                   f"disparador: {sobran}",
                                   "El producto arranca con la principal; las ranuras que "
                                   "faltan de un lado no disparan.",
                                   "Igualar las dos listas byte a byte.")
                    else:
                        self.falla("D1", self.sev_segun_estado(e, "MUERTO"),
                                   f"`{destino}`: la palabra clave PRINCIPAL difiere entre "
                                   "sus dos sitios",
                                   f"en el producto: {act!r}\n     en el disparador: {key!r}\n"
                                   f"     diferencia: {self.diff(act, str(key))}",
                                   "Si difieren aunque sea en un acento, el producto no arranca.",
                                   "Igualarlos byte a byte con la skill de configuracion.")
                e_prod = ((prod.get("informacion_de_producto") or {}).get("estado") or "").lower()
                e_disp = str(e.get("estado") or "").lower()
                if e_prod and e_disp and e_prod != e_disp:
                    self.falla("D4", "DUDA",
                               f"`{destino}`: el estado no coincide entre producto y disparador",
                               f"producto={e_prod!r} · disparador={e_disp!r} "
                               f"(en {nombre_disp})",
                               "Ambiguedad sobre si debe vender o no.")

            # D6 · activos sin ningun id de anuncio
            sin_ad = [n for n, e in registrados.items()
                      if not str(e.get("idAd") or "").strip(", ")
                      and str(e.get("estado") or "").lower() == "activo"]
            if sin_ad:
                self.falla("D6", "DUDA",
                           f"`{nombre_disp}`: {len(sin_ad)} de {len(registrados)} entradas "
                           "activas sin ningun ID de anuncio",
                           f"{sorted(sin_ad, key=self.orden_ranura)}",
                           "Si se estan pautando, se pierde la atribucion del anuncio al chat.",
                           "Contrastar contra las campanas activas antes de tocar nada.")

        # D3 · huerfanos: cargados que no estan en NINGUN disparador.
        # La severidad la decide el NEGOCIO, no la estructura: un producto sin pauta activa
        # no recibe mensajes, asi que estar fuera del disparador no cuesta nada hoy. Con
        # pauta encima, cada clic del anuncio se pierde. Criterio del dueno, en codigo.
        huerfanos = sorted(cargados - set(registrados_todos), key=self.orden_ranura)
        con_pauta, sin_pauta = [], []
        for n in huerfanos:
            ads = ((self.productos[n].get("activadores_del_flujo") or {})
                   .get("ids_de_anuncio") or "")
            (con_pauta if str(ads).strip(", ") else sin_pauta).append(n)
        if con_pauta:
            self.falla("D3", "MUERTO",
                       f"{len(con_pauta)} productos CON anuncios cargados no estan en "
                       "ningun disparador",
                       f"{con_pauta}\n     tienen ids_de_anuncio y ninguna entrada de "
                       "disparador que los reciba",
                       "Cada clic de esos anuncios entra y no encuentra producto: es plata "
                       "de pauta que no puede convertir.",
                       "Registrarlos en el disparador antes de seguir pautando.",
                       objetivo="huerfanos-con-pauta",
                       skill_duena="golden-chatea-pro-config-ventas-wp")
        if sin_pauta:
            self.falla("D3", "DUDA",
                       f"{len(sin_pauta)} de {len(cargados)} ranuras cargadas no estan en "
                       "ningun disparador, y no tienen anuncios",
                       f"{sin_pauta}\n     registradas: "
                       f"{sorted(registrados_todos, key=self.orden_ranura)}",
                       "Sin pauta activa no llegan mensajes de esos productos, asi que hoy "
                       "no se pierde nada. Se vuelven urgentes el dia que se les ponga pauta.",
                       "Registrarlos cuando se les haga pauta, o dejarlos como borrador.",
                       objetivo="huerfanos-sin-pauta",
                       skill_duena="golden-chatea-pro-config-ventas-wp")

        # Un producto en DOS disparadores a la vez es ambiguedad, no redundancia
        for destino, donde in registrados_todos.items():
            if len(donde) > 1:
                self.falla("D3", "DUDA",
                           f"`{destino}` esta registrado en {len(donde)} disparadores",
                           f"{donde}",
                           "Dos disparadores compitiendo por el mismo producto.")

        self.cubre("D1", "corrido", comparados,
                   f"de {len(cargados)} productos cargados")
        self.cubre("D2", "corrido", entradas_totales, "todas las entradas de todos los disparadores")
        self.cubre("D3", "corrido", len(cargados | set(registrados_todos)))
        self.cubre("D4", "corrido", comparados, f"de {len(cargados)} productos cargados")
        self.cubre("D5", "corrido", entradas_totales, "toda entrada, tenga producto o no")
        self.cubre("D6", "corrido", entradas_totales)
        self.cubre("D7", "NO_VERIFICADO",
                   nota="el ns del subflujo detras del disparador se cruza en el panel")
        self.cubre("D8", "NO_VERIFICADO",
                   nota="la palabra clave contra el texto real del anuncio necesita el creativo")

    @staticmethod
    def activa(entrada):
        """Una entrada del disparador cuenta como viva solo si su estado dice activo.

        Sin esto, el auditor grita MUERTO por entradas que estan APAGADAS a proposito. Medido
        en Golden el 2026-08-25 y reportado por la verificacion adversarial: 4 de las 5
        entradas del disparador de Remarketing estan `inactivo` en el servidor y salieron en
        rojo igual — la evidencia hasta imprimia "estado 'inactivo'" y el codigo no lo miraba.
        Es el gemelo de la regla que ya existia para los huerfanos (la severidad la decide el
        negocio, no la estructura) y que no se busco al arreglarla la primera vez.
        """
        return str((entrada or {}).get("estado") or "").strip().lower() == "activo"

    @staticmethod
    def sev_segun_estado(entrada, sev_si_viva):
        """Rojo solo si la entrada esta viva; apagada, es una duda de limpieza."""
        return sev_si_viva if Auditoria.activa(entrada) else "DUDA"

    @staticmethod
    def nota_estado(entrada):
        return "" if Auditoria.activa(entrada) else \
            " (la entrada esta INACTIVA: no dispara, asi que hoy no cuesta nada; " \
            "es limpieza, no urgencia)"

    @staticmethod
    def orden_ranura(n):
        m = re.search(r"(\d+)$", n)
        return (int(m.group(1)) if m else 0, n)

    @staticmethod
    def diff(a, b):
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return (f"posicion {i}: {x!r} ({unicodedata.name(x, '?')}) "
                        f"contra {y!r} ({unicodedata.name(y, '?')})")
        return f"uno es mas largo: {len(a)} contra {len(b)} caracteres"

    # ------------------------------------------------------- E · interruptores
    def bloque_e(self):
        self.interruptores = []
        for n, c in self.campos.items():
            if c.get("var_type") == "boolean":
                self.interruptores.append((n, "", c.get("value")))
            val = self.valor_json(c)
            if isinstance(val, (dict, list)):
                for ruta, hoja in self.caminar(val):
                    if INTERRUPTOR.match(ruta.split(".")[-1]):
                        self.interruptores.append((n, ruta, hoja))
        self.universo["interruptores"] = len(self.interruptores)
        self.cubre("E1", "corrido", len(self.interruptores))

        # E2 · apagado gobernando contenido lleno, a CUALQUIER profundidad.
        # La version anterior solo veia interruptores a profundidad exactamente 2: un
        # `activar` en la raiz del campo o a tres niveles se le escapaba entero.
        grupos_revisados = 0
        for n, c in self.campos.items():
            val = self.valor_json(c)
            if not isinstance(val, (dict, list)):
                continue
            for ruta_padre, cuerpo in self.contenedores(val):
                if not isinstance(cuerpo, dict):
                    continue
                grupos_revisados += 1
                for llave, hoja in cuerpo.items():
                    if not INTERRUPTOR.match(llave) or hoja not in APAGADO:
                        continue
                    sufijo = llave.split("_")[-1] if "_" in llave else ""
                    # el contenido que gobierna puede estar en el mismo nivel o debajo
                    candidatos = [(r, v) for r, v in self.caminar(cuerpo)
                                  if isinstance(v, str) and len(v) >= 400]
                    if sufijo.isdigit():
                        mismos = [x for x in candidatos if x[0].endswith("_" + sufijo)]
                        candidatos = mismos or candidatos
                    if not candidatos:
                        continue
                    ruta_txt, texto = max(candidatos, key=lambda x: len(x[1]))
                    donde = f"{ruta_padre}." if ruta_padre else ""
                    self.falla("E2", "MUERTO",
                               f"`{n}` → `{donde}{llave}` esta APAGADO con contenido cargado",
                               f"`{donde}{ruta_txt}` tiene {len(texto):,} caracteres y "
                               f"`{llave}` = {hoja!r}",
                               "Un prompt perfecto detras de un interruptor apagado no hace "
                               "nada, y ningun chequeo del contenido lo detecta.",
                               "Confirmar con FER si es a proposito antes de encenderlo.")
        self.cubre("E2", "corrido", grupos_revisados, "grupos con interruptor, a toda profundidad")

        # E4 · eventos de Meta, listados para contrastar (en cero no es defecto por si solo)
        metas = {n: (c.get("value") or "") for n, c in self.campos.items()
                 if n.startswith("[Meta]")}
        self.universo["eventos_meta"] = metas
        en_cero = [n for n, v in metas.items() if str(v).strip() in ("0", "")]
        if en_cero and len(en_cero) == len(metas) and metas:
            self.falla("E4", "DUDA", "Todos los eventos de Meta estan en cero",
                       f"{sorted(metas)}",
                       "En produccion tambien estan asi, o sea que no prueba nada por si solo; "
                       "se contrasta contra el pixel.")
        self.cubre("E4", "corrido", len(metas))

        # E3 · credencial de voz heredada. extraer.py REDACTA por patron de valor (PATRONES_SECRETO)
        # antes de que este script vea el DUMP, asi que en un DUMP real `api_key` SIEMPRE llega
        # como `<<REDACTADO...>>` cuando hubo una credencial (o vacio cuando no la hubo). La
        # version vieja exigia lo contrario — "no empieza por REDACTADO" — que solo era cierto
        # en el fixture de la propia autoprueba (armado a mano, sin pasar por el redactor): contra
        # un DUMP real la condicion nunca se cumplia y E3 jamas disparaba. El dato que hay que
        # juzgar no es si esta redactado, es si HABIA algo que redactar.
        for n, prod in self.productos.items():
            voz = prod.get("voz_con_ia") or {}
            api = voz.get("api_key") or ""
            if api:
                redactada = str(api).startswith("<<REDACTADO")
                self.falla("E3", "FUGA",
                           f"`{n}` lleva una credencial de voz dentro del producto",
                           f"`voz_con_ia.api_key` presente, {len(str(api))} caracteres "
                           f"({'redactada en el DUMP, viva en el servidor' if redactada else 'EN CLARO en el DUMP'}), "
                           f"habilitar={voz.get('habilitar')!r}",
                           "Copiar un producto 'exacto' copia tambien la credencial de la "
                           "cuenta de origen.",
                           "Vaciarla si el espacio no es el dueno de esa cuenta de voz.")
        self.cubre("E3", "corrido", len(self.productos), "productos revisados")
        self.cubre("C6", "corrido", len(self.campos),
                   "truncada silenciosa: campos array/longtext que no parsean")

    # ------------------------------------------------------------ F · contenido
    def bloque_f(self):
        textos = 0
        mojibake_campos, apertura_campos = [], []
        for n, c in self.campos.items():
            v = c.get("value")
            if not isinstance(v, str) or not v:
                continue
            textos += 1
            rotos = [s for s in MOJIBAKE if s in v]
            if rotos:
                mojibake_campos.append((n, rotos))
            if "¿" in v or "¡" in v:
                apertura_campos.append(n)
            hallados = [p for p in PLACEHOLDERS if p in v]
            if hallados:
                self.falla("F3", "FUGA",
                           f"`{n}` tiene marcadores de posicion sin reemplazar",
                           f"{hallados}",
                           "Se publico sin terminar de parametrizar.")
            # OJO: se busca en las HOJAS DE TEXTO, no en el JSON crudo. Aplicado al crudo,
            # el `[` que abre un array parece la apertura de un hueco y cualquier palabra en
            # mayusculas dentro del array dispara un falso positivo (medido: los dos campos
            # de disparador salieron acusados). La sintaxis no es contenido.
            val = self.valor_json(c)
            hojas = ([h for _, h in self.caminar(val) if isinstance(h, str)]
                     if isinstance(val, (dict, list)) else [v])
            huecos = sorted({m.group(0) for h in hojas
                             for m in HUECO_DE_EDITOR.finditer(h)})
            dudosos = sorted({m.group(0) for h in hojas
                              for m in CORCHETE_MAYUSCULAS.finditer(h)}) 
            dudosos = [x for x in dudosos if x not in huecos]
            if dudosos:
                self.falla("F3", "DUDA",
                           f"`{n}` tiene {len(dudosos)} corchete(s) en mayusculas: "
                           "plantilla viva o hueco",
                           "\n     ".join(x[:120] for x in dudosos[:8]),
                           "Si el motor los rellena son plantilla y estan bien; si no, el "
                           "cliente los lee tal cual.",
                           "Confirmar cual de los dos es antes de tocar nada.")
            if huecos:
                # Si el campo es un producto ACTIVO, el cliente lee ese corchete tal cual.
                activo = "[Producto Ventas Wp]" in n and '"estado":"activo"' in \
                    v.replace(" ", "")
                self.falla("F3", "MUERTO" if activo else "FUGA",
                           f"`{n}` tiene {len(huecos)} hueco(s) que quedo(aron) sin llenar",
                           "\n     ".join(h[:120] for h in huecos),
                           "El cliente recibe el corchete tal cual, y si cae en el paso de "
                           "cobro se pierde la venta ahi mismo."
                           if activo else
                           "Quedo sin terminar de parametrizar.",
                           "Llenarlos con la skill duena antes de que ese producto reciba "
                           "un mensaje mas.")
        if mojibake_campos:
            self.falla("F1", "FUGA",
                       f"{len(mojibake_campos)} de {textos} campos tienen la codificacion rota",
                       "\n     ".join(f"{n}: {r}" for n, r in mojibake_campos[:12]),
                       "Un acento roto suele ser cien: el cliente lee el texto asi.",
                       "Corregir la clase entera, no el caso suelto.")
        if apertura_campos:
            self.falla("F2", "FUGA",
                       f"{len(apertura_campos)} de {textos} campos usan signos de apertura",
                       f"{apertura_campos[:15]}",
                       "Regla de Golden: el texto que le llega al cliente va sin ¿ ni ¡.")
        self.cubre("F1", "corrido", textos)
        self.cubre("F2", "corrido", textos)
        self.cubre("F3", "corrido", textos)

        # F5 · ficha del producto · F6 multimedia · F7 imagenes de otra cuenta
        cuentas_img = {}
        for n, prod in self.productos.items():
            info = prod.get("informacion_de_producto") or {}
            for llave in ("nombre", "precio", "moneda", "estado", "tipo", "id_dropi"):
                if not str(info.get(llave) or "").strip():
                    self.falla("F5", "DUDA", f"`{n}`: la ficha no declara `{llave}`",
                               f"informacion_de_producto = "
                               f"{ {k: v for k, v in info.items() if k != 'dta_prompt'} }")
            precio = str(info.get("precio") or "")
            if precio and not precio.isdigit():
                self.falla("F5", "DUDA", f"`{n}`: el precio no es un numero limpio",
                           f"precio = {precio!r}",
                           "Los separadores conviven en dos formatos y un parser los confunde.")
            multi = (prod.get("embudo_de_ventas") or {}).get("multimedia")
            if isinstance(multi, str):
                self.falla("F6", "MUERTO", f"`{n}`: `multimedia` esta escrita como cadena",
                           f"{multi[:120]!r}",
                           "El panel la muestra vacia y al guardar la deja en [], sin un solo error.",
                           "Reescribirla como lista.")
        # F7 recorre TODOS los campos de bot, no solo self.productos: una imagen
        # ajena puede vivir en cualquier asistente (Comentarios, Logistico...),
        # no solo en Ventas WhatsApp. Se cuentan URLs distintas, no rutas/hojas.
        vistas = set()
        for n, c in self.campos.items():
            val = self.valor_json(c)
            objetivo = val if isinstance(val, (dict, list)) else c.get("value")
            for ruta, hoja in self.caminar(objetivo) if isinstance(objetivo, (dict, list)) \
                    else ([("", objetivo)] if isinstance(objetivo, str) else []):
                if isinstance(hoja, str) and "media.chateapro.app" in hoja:
                    m = re.search(r"media\.chateapro\.app/temp/\d{6}/(\d+)/", hoja)
                    if m and (n, hoja) not in vistas:
                        vistas.add((n, hoja))
                        cuentas_img.setdefault(m.group(1), []).append(f"{n} → {ruta or 'value'}")
        # La cuenta propia sale del SERVIDOR (/team-info), no de suponer que la mayoritaria
        # es la buena. Un espacio clonado ENTERO tiene una sola cuenta y es la ajena: el
        # control de "mas de una cuenta" no lo veia.
        propia = ""
        ti = self.d.get("/team-info") or {}
        for ruta, hoja in self.caminar(ti):
            if ruta.endswith("id") and str(hoja).isdigit() and len(str(hoja)) >= 5:
                propia = str(hoja)
                break
        self.universo["cuenta_de_medios_propia"] = propia or "(no determinada)"
        self.universo["cuentas_de_imagen"] = sorted(cuentas_img)
        if not propia:
            self.falla("F7", "DUDA",
                       "No se pudo determinar la cuenta propia de medios",
                       f"cuentas vistas en las imagenes: {sorted(cuentas_img)}",
                       "Sin la cuenta propia no se puede decir si una imagen es heredada.",
                       "Leer el id de la cuenta en /team-info o en el panel.")
        else:
            ajenas = {c: v for c, v in cuentas_img.items() if c != propia}
            if ajenas:
                self.falla("F7", "FUGA",
                           f"Hay imagenes de {len(ajenas)} cuenta(s) que NO son esta",
                           f"esta cuenta es {propia} · "
                           + " · ".join(f"cuenta {c}: {len(v)} imagenes (ej. {v[0]})"
                                        for c, v in ajenas.items()),
                           "Apuntan al espacio de origen, no al propio.",
                           "Volver a subir esas imagenes desde el panel de este espacio.")
        self.cubre("F5", "corrido", len(self.productos))
        self.cubre("F6", "corrido", len(self.productos))
        self.cubre("F7", "corrido", len(self.campos))
        for control, nota in (("F4", "las fugas de marca se leen contra el negocio real"),
                              ("F8", "las URLs se piden una por una"),
                              ("F9", "el prompt contra el producto real"),
                              ("F10", "estructura contra el estandar"),
                              ("F11", "prompt 'generico' con un producto horneado"),
                              ("F12", "criterio de pais heredado de otra plantilla")):
            self.cubre(control, "NO_VERIFICADO", nota="lectura humana: " + nota)

    # ------------------------------------------------------------ G · seguridad
    def bloque_g(self):
        con_credencial = []
        # El payload viene ANIDADO bajo `data`: mirar solo el primer nivel daba cero
        # teniendo seis credenciales cargadas. Se recorre el objeto entero.
        for clave, valor in self.d.items():
            if not clave.startswith("/integration/") or not isinstance(valor, dict):
                continue
            for ruta, hoja in self.caminar(valor):
                if not isinstance(hoja, str) or not hoja:
                    continue
                hojita = ruta.split(".")[-1].lower()
                if hoja.startswith("<<REDACTADO"):
                    con_credencial.append(f"{clave} → {ruta} ({hoja})")
                elif any(s in hojita for s in ("token", "key", "secret", "password")):
                    self.falla("G1", "MUERTO",
                               f"Una credencial salio SIN redactar en {clave}",
                               f"ruta `{ruta}`",
                               "El extractor debe redactar siempre. Este DUMP no se comparte.",
                               "Borrar el DUMP, arreglar la lista de redaccion y repetir.")
        self.universo["integraciones_con_credencial"] = len(con_credencial)
        if con_credencial:
            self.falla("G1", "FUGA",
                       f"{len(con_credencial)} credenciales viven en las integraciones del workspace",
                       "\n     ".join(con_credencial),
                       "La API las devuelve EN TEXTO PLANO: cualquiera con el token del bot "
                       "lee todas las llaves del workspace.",
                       "Nunca darle un token de bot a un alumno o cliente. Rotar lo compartido.")

        shop = self.d.get("/integration/shopify") or {}
        dominio = next((str(v) for r, v in self.caminar(shop)
                        if isinstance(v, str) and "myshopify.com" in v), "")
        if dominio:
            self.universo["shopify_conectada"] = dominio
            self.falla("G2", "DUDA",
                       "Confirmar a que tienda apunta la integracion de Shopify",
                       f"{dominio}",
                       "Ya paso: apuntaba a un dominio myshopify que no era la tienda.")

        # Buscar por NOMBRE de campo dejaba fuera las credenciales que viven dentro de un
        # JSON de configuracion. Medido: `[Integraciones] Datos de integracion` llevaba tres
        # llaves y no disparaba. Se busca por PATRON, en el valor de todos los campos.
        for n, c in self.campos.items():
            v = c.get("value")
            if not isinstance(v, str) or not v:
                continue
            for etiqueta, patron in PATRONES_SECRETO:
                for m in patron.finditer(v):
                    self.falla("G3", "MUERTO",
                               f"El campo `{n}` guarda una credencial EN CLARO",
                               f"{etiqueta}, {len(m.group(0))} caracteres",
                               "El DUMP no esta redactado o el extractor no conoce ese patron: "
                               "este archivo no se comparte.",
                               "Anadir el patron al extractor, borrar el DUMP y repetir.")
            for m in re.finditer(r"<<REDACTADO ?([A-Za-z]*) ?len=(\d+)>>", v):
                self.falla("G3", "FUGA",
                           f"El campo `{n}` guarda una credencial como valor",
                           f"{m.group(1) or 'sin identificar'}, {m.group(2)} caracteres "
                           "(redactada en el DUMP, viva en el servidor)",
                           "Queda expuesta a cualquiera que lea los bot fields de este bot.")
        self.universo["credenciales_en_integraciones"] = len(con_credencial)
        self.cubre("G1", "corrido",
                   sum(1 for k in self.d if k.startswith("/integration/")),
                   f"{len(con_credencial)} credenciales halladas")
        # G2 solo EXTRAE el dominio y le hace una pregunta al dueno: no tiene contra que
        # comparar para decidir si es el correcto (no hay un dominio esperado en ningun
        # asset), asi que marcarlo "corrido" sonaba a verificado cuando en realidad nunca
        # produjo un veredicto, solo una duda. Es NO_VERIFICADO con evidencia, no una
        # verificacion completa.
        self.cubre("G2", "NO_VERIFICADO" if dominio else "sin_datos",
                   nota=f"dominio encontrado: {dominio}" if dominio else
                   "la integracion de Shopify no trajo dominio")
        self.cubre("G3", "corrido", len(self.campos))
        self.cubre("G4", "NO_VERIFICADO", nota="la rotacion se decide con FER")

    # ---------------------- F bis · la zona de agentes y tareas de IA, que tambien es texto
    def bloque_ia(self):
        """El extractor baja los prompts de los agentes y las tareas de IA. Estaban
        extraidos y sin auditar: 74 objetos y 51.000 caracteres fuera de todo control,
        con signos de apertura y una URL de ejemplo dentro. Lo que entra al DUMP se
        audita o se declara, nunca se queda en tierra de nadie."""
        zonas = {"agentes IA": self.d.get("_agentes_detalle") or {},
                 "tareas IA": self.d.get("_tareas_detalle") or {}}
        # Los agentes de un asistente que FER saco del ecosistema tampoco se auditan aqui
        # (el verificador del 24-sep sembro "¿" en el "Agente de Remarketing" y F13 lo grito).
        # El detalle viene por ns; el nombre, de /flow/ai-agents y /flow/ai-tasks.
        if not self.incluir_excluidos:
            fuera = set()
            for lista in ("/flow/ai-agents", "/flow/ai-tasks"):
                for x in self.d.get(lista) or []:
                    if isinstance(x, dict) and es_agente_excluido_por_fer(x.get("name")):
                        fuera.update(v for k, v in x.items() if k.endswith("_ns") and k != "flow_ns"
                                     and isinstance(v, str))
            if fuera:
                zonas = {e: ({ns: c for ns, c in z.items() if ns not in fuera}
                             if isinstance(z, dict) else z) for e, z in zonas.items()}
                self.universo["agentes_ia_excluidos_por_fer"] = sorted(fuera)
        objetos = cadenas = 0
        # 🔴 EL DENOMINADOR NO ES "objetos": es "objetos QUE TRAIAN TEXTO". Un agente o una
        # tarea que el extractor baja `locked` llega sin una sola cadena, asi que ningun
        # control lo mira -- y aun asi engordaba el numero que F13 declaraba como cobertura.
        # Medido por el verificador el 2026-09-08 sobre un espacio en produccion: 72 objetos
        # declarados, 40 sin
        # texto. Eso es cobertura FALSA, la clase de mentira que este auditor existe para no
        # cometer: "N de N revisados" donde 40 nunca se revisaron porque no habia que ver.
        # Se cuentan aparte y se declaran; no se esconden ni se suman.
        vacios = []
        moji, apert, marcas = [], [], []
        for etiqueta, zona in zonas.items():
            if not isinstance(zona, dict):
                continue
            for ns, cuerpo in zona.items():
                objetos += 1
                antes = cadenas
                for ruta, hoja in self.caminar(cuerpo):
                    if not isinstance(hoja, str) or not hoja:
                        continue
                    cadenas += 1
                    donde = f"{etiqueta} {ns} → {ruta}"
                    if any(s in hoja for s in MOJIBAKE):
                        moji.append(donde)
                    if "¿" in hoja or "¡" in hoja:
                        apert.append(donde)
                    for ph in PLACEHOLDERS:
                        if ph in hoja and ph != "{{":   # {{ }} es sintaxis viva de Chatea
                            marcas.append(f"{donde}: {ph!r}")
                    for m in HUECO_DE_EDITOR.finditer(hoja):
                        marcas.append(f"{donde}: {m.group(0)[:90]!r}")
                if cadenas == antes:
                    vacios.append(f"{etiqueta} {ns}")
        con_texto = objetos - len(vacios)
        self.universo["zona_ia"] = {"objetos": objetos, "cadenas": cadenas,
                                    "con_texto": con_texto, "sin_texto": len(vacios)}
        if moji:
            self.falla("F13", "FUGA",
                       f"{len(moji)} textos de agentes o tareas de IA con la codificacion rota",
                       "\n     ".join(moji[:10]))
        if apert:
            self.falla("F13", "FUGA",
                       f"{len(apert)} textos de agentes o tareas de IA usan signos de apertura",
                       "\n     ".join(apert[:10]),
                       "Esta zona no la cubria ningun control: el denominador de F2 la excluia.")
        if marcas:
            self.falla("F13", "FUGA",
                       f"{len(marcas)} marcadores de posicion en agentes o tareas de IA",
                       "\n     ".join(marcas[:10]),
                       "Contrastar contra un espacio virgen antes de tocar: si no aparece "
                       "alli, no es default de fabrica.")
        if vacios:
            # No es un defecto del espacio: es un limite de la LECTURA. Un objeto sin texto
            # puede estar vacio de verdad o puede que el extractor no pudiera abrirlo. Lo
            # que no se puede es contarlo como revisado.
            self.falla("F13", "DUDA",
                       f"{len(vacios)} de {objetos} agentes o tareas de IA llegaron SIN "
                       f"una sola cadena: no se pudieron auditar",
                       "\n     ".join(vacios[:10]),
                       "Mirarlos en el panel. Si tienen texto alli, el extractor no los "
                       "esta bajando y la cobertura de esta zona es menor de lo que parece.")
        self.cubre("F13",
                   "corrido" if con_texto else "sin_datos",
                   con_texto,
                   f"{cadenas} cadenas de agentes y tareas de IA · "
                   f"{len(vacios)} de {objetos} objetos llegaron sin texto y NO se auditaron")

    # ------------------------------------- F14 · la PLANTILLA DE FABRICA de la plataforma
    def bloque_fabrica(self):
        """F14 — el hueco mas grande que tenia este auditor, y se cerro el 2026-09-07.

        Los 13 controles anteriores buscaban DOS cosas: huecos sin llenar (F3: '{{', 'TU_',
        marcadores) y fugas de OTRA cuenta (F4). **El contenido de fabrica no es ninguna de las
        dos**: es de Chatea, no de otro cliente, y no parece un marcador -- parece configuracion.
        Medido el 2026-09-06 contra la API en dos espacios recien creados: **61 de 61 campos
        identicos byte a byte** entre uno nacido en Colombia y otro creado eligiendo Mexico. La
        plataforma nace colombiana elijas el pais que elijas.

        Con los 13 controles, un espacio ENTERO sin tocar salia sano en esta dimension: el bot le
        entrega a un cliente de verdad un telefono que no es de nadie, un asesor llamado Santiago
        y la ley colombiana en la garantia, y en el panel todo se ve bien.

        LA BANDERA is_template_field DE LA PLATAFORMA NO SIRVE: viene en falso en 9 de cada 10
        campos. Se mide por el VALOR, contra la huella md5 de la plantilla medida.

        COBERTURA DECLARADA: la huella vive en la hermana logistica y trae los 61 campos. Si el
        asset no esta, F14 se declara NO CORRIDO -- no se calla ni se da por sano."""
        import hashlib
        ruta = os.path.expanduser(
            "~/.claude/skills/golden-chatea-pro-config-logistico/assets/plantilla-fabrica.json")
        if not os.path.exists(ruta):
            self.cubre("F14", "NO CORRIDO", 0,
                       "falta la huella de la plantilla de fabrica "
                       "(golden-chatea-pro-config-logistico/assets/plantilla-fabrica.json): "
                       "la contaminacion de fabrica NO se comprobo")
            return
        try:
            with open(ruta, encoding="utf-8") as f:
                huella = json.load(f)["huella_md5"]
        except Exception as e:
            self.cubre("F14", "NO CORRIDO", 0, f"no se pudo leer la huella: {e}")
            return

        de_fabrica, revisados = [], 0
        for nombre, campo in self.campos.items():
            if nombre not in huella:
                continue
            v = campo.get("value")
            texto = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            if not (texto or "").strip():
                continue
            revisados += 1
            if hashlib.md5(texto.encode("utf-8")).hexdigest() == huella[nombre]["md5"]:
                de_fabrica.append(nombre)

        # 🔴 DOS SEVERIDADES, y la separacion vino de campo (chat de un espacio real, 2026-09-08).
        # La primera version de F14 metia los 32 hallazgos en un solo saco y todos pesaban igual.
        # Medido en un espacio real: **27 de 32 eran interruptores, versiones o valores triviales**
        # (false / true / 1 / 2.1.3) -- default legitimo que nadie tiene que tocar. Solo **5**
        # llevaban texto que le LLEGA AL CLIENTE. Un informe donde lo urgente y lo irrelevante
        # pesan igual obliga a filtrar a mano, y lo que se filtra a mano se acaba ignorando entero.
        #
        # El criterio NO es la longitud -- eso acusaria al idioma. Es la FORMA del valor: un
        # booleano, un numero o una version no puede leerlos un cliente. Todo lo demas si puede,
        # y por eso el placeholder "string" repetido en los huecos de plantilla cae en el lado
        # que importa, aunque sea corto.
        caliente = [n for n in de_fabrica if not _valor_trivial(self.campos[n].get("value"))]
        trivial = [n for n in de_fabrica if n not in caliente]

        if caliente:
            self.falla("F14", "FUGA",
                       f"{len(caliente)} campos de FABRICA con texto que LE LLEGA AL CLIENTE",
                       "\n     ".join(caliente[:12]),
                       "Un campo de fabrica NO se ve vacio: se ve configurado, y por eso ningun "
                       # 🔴 ESTA CONSECUENCIA DESCRIBE LA CLASE, NUNCA UN CONTENIDO CONCRETO.
                       # Medido el 2026-09-17 en el espacio de un cliente: aqui habia escrito
                       # "un asesor llamado Santiago" y "5 anos en el logistico" como si fueran
                       # datos de ESE espacio. No lo eran -- salian del espacio de referencia
                       # donde se levanto la huella. El cliente auditado no tenia ningun
                       # "Santiago" y su logistico decia "3 anos".
                       # Un texto enlatado dentro de un hallazgo es una INFERENCIA con forma de
                       # medida, y hereda la credibilidad del informe entero: es exactamente la
                       # puerta de reference_inferencia_de_subagente_no_es_medida, esta vez
                       # abierta por nuestro propio auditor. Lo concreto sale del DUMP (la
                       # evidencia de arriba lo trae) o no sale.
                       "control de huecos lo caza. Segun el campo, puede traer telefonos de "
                       "relleno que no son de nadie, nombre y biografia de un asesor que no "
                       "existe, cifras de trayectoria inventadas y contradictorias entre "
                       "asistentes, y la ley de OTRO pais en la garantia. **Lo que trae ESTE "
                       "espacio esta en la evidencia de arriba, leida de su propio dump.** "
                       "Se limpian ANTES de dar el espacio por instalado.")
        if trivial:
            self.falla("F14", "DUDA",
                       f"{len(trivial)} campos de fabrica TRIVIALES (interruptor, numero o version)",
                       "\n     ".join(trivial[:8]),
                       "Estos son el default de la plataforma y en su mayoria NO hay que tocarlos: "
                       "un booleano o una version no los lee ningun cliente. Se listan para que el "
                       "denominador sea honesto, no para que se limpien uno por uno. Miralos solo "
                       "si un interruptor concreto deberia estar en el otro estado.")
        self.cubre("F14", "corrido", revisados,
                   f"{revisados} campos con valor comparados contra la huella de {len(huella)} "
                   f"de la plantilla medida · {len(de_fabrica)} de fabrica "
                   f"({len(caliente)} con texto al cliente · {len(trivial)} triviales)")

    # ------------------------------------------- I · cordura del propio auditor
    def bloque_i(self):
        # I3 · lo que entra al DUMP se audita o se declara. Nada en tierra de nadie.
        # ENDPOINTS_B4 es la MISMA lista que usa bloque_b para contar subflujos, tags,
        # agentes/tareas IA y webhooks: antes esta lista vivia duplicada e incompleta aqui, asi
        # que I3 acusaba como "sin control" endpoints que B4 ya contaba (medido: 7 falsos
        # positivos). Una sola lista, importada, no copiada.
        auditadas = {"/me", "/team-info", "/flow/bot-fields", "/flow/user-fields",
                     "/workspace-settings/channels", "_agentes_detalle", "_tareas_detalle",
                     "_conteos", "_etiqueta", "_extraido", "_token_archivo",
                     *ENDPOINTS_B4}
        sin_control = [k for k, v in self.d.items()
                       if k not in auditadas and not k.startswith("/integration/")
                       and v not in (None, [], {}, "")]
        if sin_control:
            self.falla("I3", "DUDA",
                       f"{len(sin_control)} zonas del DUMP no las mira ningun control",
                       f"{sorted(sin_control)}",
                       "Estan extraidas y sin auditar: no se sabe si estan sanas, y su "
                       "ausencia de hallazgos no prueba nada.",
                       "Anadirles control o declararlas fuera de alcance en el informe.")
        self.cubre("I3", "corrido", len(self.d), f"{len(sin_control)} zonas sin control")
        self.cubre("I1", "NO_VERIFICADO",
                   nota="la autoprueba se corre aparte: sin su salida en verde este informe "
                        "no se publica")
        self.cubre("I2", "corrido", len(self.cobertura),
                   "un cero solo prueba algo si el bloque cubrio todo")

        # I4 · ausencia no es prueba. Cada bloque ya distingue "medido y vacio" de "no
        # medido" (B1b compara traidos contra meta.total; A4/B2 marcan sin_datos cuando
        # el endpoint no trajo nada). Aqui se declara el conteo para que la distincion
        # quede en la cobertura final, no solo dispersa dentro de cada bloque.
        medidos_y_vacios = sum(1 for c in self.cobertura if c["estado"] == "sin_datos")
        no_medidos = sum(1 for c in self.cobertura if c["estado"] == "PARCIAL")
        self.cubre("I4", "corrido", len(self.cobertura),
                   f"{medidos_y_vacios} controles en 'sin_datos' (medido y vacio), "
                   f"{no_medidos} en 'PARCIAL' (no se agoto la paginacion)")

    def bloque_h(self):
        for control, nota in (("H1", "id_dropi contra Dropi"),
                              ("H2", "precio contra la tienda"),
                              ("H3", "idAd contra los anuncios activos de Meta"),
                              ("H4", "no heredar datos entre las tres empresas")):
            self.cubre(control, "NO_VERIFICADO", nota="cruce externo: " + nota)

    # ------------------------------------------- diff contra la corrida anterior
    def comparar(self, anterior):
        """Que cambio desde la ultima auditoria.

        Sin esto la skill es una foto: cada corrida repite los mismos 40 hallazgos y el
        dueno deja de leerlos. Con esto se puede preguntar lo unico que importa a diario:
        que se movio.
        """
        # Los dos lados pasan por el MISMO filtro: si solo se filtra el nuevo, cada campo
        # apartado sale como "BORRADO" sin haberse borrado (verificador, 24-sep: 9 falsos).
        viejos = {c["name"]: c for c in (anterior.get("/flow/bot-fields") or [])
                  if isinstance(c, dict) and "name" in c
                  and (self.incluir_excluidos or not es_excluido_por_fer(c["name"]))}
        nuevos = self.campos
        for n in sorted(set(nuevos) - set(viejos)):
            self.cambios.append(("NUEVO", n, f"campo creado ({nuevos[n].get('var_type')})"))
        for n in sorted(set(viejos) - set(nuevos)):
            self.cambios.append(("BORRADO", n,
                                 "el campo ya no existe: un flujo que lo referencie por "
                                 "var_ns queda apuntando al vacio"))
        for n in sorted(set(viejos) & set(nuevos)):
            va, vn = viejos[n].get("value") or "", nuevos[n].get("value") or ""
            if va == vn:
                continue
            ea, en = len(json.dumps(va)[1:-1]), len(json.dumps(vn)[1:-1])
            signo = "+" if en >= ea else ""
            # El escapado (json.dumps(...)[1:-1]) es la unidad que importa: es contra la que
            # se mide el techo de 19.000 (bloque C). El largo crudo (len(va)/len(vn)) es
            # SIEMPRE menor o igual — cada tilde pesa 6 escapados y cada emoji 12 — y mostrarlo
            # como si fuera el escapado le miente al lector el margen real que queda contra el
            # techo. Se muestra el escapado PRIMERO y con su nombre, el crudo aparte y marcado.
            self.cambios.append(("EDITADO", n,
                                 f"{ea:,} → {en:,} escapados ({signo}{en - ea:,}) "
                                 f"[crudo {len(va):,} → {len(vn):,} caracteres]"))
            if ea <= TECHO_ESCAPADO < en:
                self.falla("C1", "MUERTO",
                           f"`{n}` CRUZO el techo escapado desde la corrida anterior",
                           f"{ea:,} → {en:,} escapados",
                           "El cambio que lo cruzo es el sospechoso inmediato.",
                           "Revertir o compactar ese cambio.", objetivo=f"cruce-techo-{n}")
        self.universo["cambios_desde_anterior"] = len(self.cambios)
        # correr() ya dejo J1 declarado como NO_CORRIDO. Ahora SI se corrio, asi que esa
        # linea se sustituye en vez de anadirse: dos entradas del mismo control en la tabla
        # de cobertura dicen dos cosas distintas y el lector se queda con la que ve primero.
        self.cobertura = [c for c in self.cobertura if c["control"] != "J1"]
        self.cubre("J1", "corrido", len(set(viejos) | set(nuevos)),
                   f"diff contra {anterior.get('_extraido', 'corrida anterior')}")

    # ------------------------------- L · LA CONFIGURACION CONTRA EL ESQUEMA DE REFERENCIA
    def bloque_esquema(self):
        """L1/L2/L3 — 'a esta tienda le falta esto, esto y lo otro'.

        ENCARGO DE FER, 2026-09-08, con sus palabras: *"Antes yo copiaba y pegaba mi espacio
        al del cliente, era una copia identica y me tocaba cambiar a mano el nombre. Lo que
        quiero ahora es que no sea un espejo: que se interprete lo que cada tienda es -si es
        una marca o si es multinicho- y se adapten estos campos a la personalidad de cada
        tienda. La MISMA ESTRUCTURA, pero con SU personalidad."*

        De ahi salen exactamente TRES controles, y son tres porque hay tres formas distintas
        de estar mal:

        · **L1 · LA LLAVE NO ESTA.** El asistente lee ese trozo de su configuracion vacio y
          se inventa el comportamiento. Es lo mas grave y es MUERTO.
        · **L2 · LA LLAVE ESTA Y ESTA VACIA, o puesta de compromiso.** Existe pero no dice
          nada. El umbral no es un minimo inventado: se compara contra el orden de magnitud
          del patron, y solo se marca cuando la diferencia es de otra escala (menos del 15%
          de lo que mide el mismo campo bien puesto). Es FUGA: llega al cliente.
        · **L3 · LA LLAVE ES UN ESPEJO.** Identica byte a byte al patron en un campo que
          DEBERIA llevar la personalidad de esa tienda. Es justo lo que FER quiere dejar de
          hacer, y ningun otro control lo ve: F14 compara contra la plantilla de FABRICA, no
          contra otro cliente. Un espejo se ve perfectamente configurado.

        L2 y L3 son GEMELOS OPUESTOS y por eso van juntos: demasiado corto y demasiado igual.
        Arreglar uno sin el otro deja la puerta abierta por el lado contrario -- la clase que
        esta casa ya se ha comido dos veces.

        COBERTURA DECLARADA: sin el asset, los tres se declaran NO CORRIDO. Y el esquema solo
        cubre los asistentes que se han medido: lo que no esta en el, no se juzga.
        """
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "assets", "esquema-configuracion.json")
        if not os.path.exists(ruta):
            for c in ("L1", "L2", "L3", "L5"):
                self.cubre(c, "NO CORRIDO", 0, "falta assets/esquema-configuracion.json")
            return
        esquema = json.load(open(ruta, encoding="utf-8"))["asistentes"]

        # Aplanar el esquema: nombre-de-campo-normalizado -> {llave: [tipo, medida]}
        def _norm(s):
            return re.sub(r"[^a-z0-9]", "", str(s).lower())
        por_campo = {}
        for asistente, campos in esquema.items():
            for nombre, cuerpo in campos.items():
                por_campo[_norm(nombre)] = (asistente, nombre, cuerpo["llaves"])

        def _hojas(o, ruta=""):
            """Las hojas del JSON de ESTE espacio, con su ruta de llave."""
            if isinstance(o, dict):
                for k, v in o.items():
                    r = f"{ruta}.{k}" if ruta else k
                    if isinstance(v, (dict, list)):
                        yield from _hojas(v, r)
                    else:
                        yield r, v
            elif isinstance(o, list):
                yield (ruta or "(raiz)"), o
                if o:
                    yield from _hojas(o[0], (ruta or "") + "[]")

        revisados = faltan = flojos = espejos = 0
        sin_esquema = []
        # self.campos es {nombre: campo}, no una lista. Lo aprendi rompiendome contra la
        # autoprueba, que es justo para lo que esta.
        for nombre, campo in self.campos.items():
            clave = _norm(nombre)
            if clave not in por_campo:
                # L5 · NO se salta en silencio. Medido el 2026-09-22 contra las skills
                # hermanas: de los 9 campos que configura el logistico, el esquema conoce 2.
                # Los otros caian aqui, el bloque L seguia de largo y la cobertura solo
                # decia cuantos reviso. Un campo que nadie juzga y que nadie declara es
                # cobertura falsa -- el pecado que esta skill le persigue a las demas.
                if not es_campo_de_producto(nombre):
                    v = campo.get("value")
                    if isinstance(v, str) and v.strip():
                        try:
                            cuerpo = json.loads(v)
                        except Exception:                          # noqa: BLE001
                            cuerpo = None
                        if isinstance(cuerpo, dict) and cuerpo:
                            sin_esquema.append((nombre, len(dict(_hojas(cuerpo)))))
                continue
            valor = campo.get("value")
            if not isinstance(valor, str) or not valor.strip():
                continue
            try:
                d = json.loads(valor)
            except Exception:                                      # noqa: BLE001
                continue   # C6 ya reporta el JSON roto; aqui no se duplica
            revisados += 1
            _, patron_nombre, llaves = por_campo[clave]
            hojas = dict(_hojas(d))

            ausentes = [k for k in llaves if k not in hojas]
            if ausentes:
                faltan += len(ausentes)
                self.falla("L1", "MUERTO",
                           f"`{nombre}`: {len(ausentes)} llaves de la configuracion NO EXISTEN",
                           ", ".join(ausentes[:12]),
                           "El asistente lee ese trozo vacio y se inventa el comportamiento. "
                           "La ESTRUCTURA se exige aunque el contenido se adapte.",
                           f"Anadirlas al JSON. El esquema esta en assets/esquema-configuracion.json",
                           objetivo=f"llaves-ausentes-{nombre}")

            cortos, iguales, comparables = [], [], 0
            for k, meta in llaves.items():
                if meta[0] != "texto" or len(meta) < 2:
                    continue
                v = hojas.get(k)
                if not isinstance(v, str):
                    # P59: una cadena vacia SI se acusaba y un null no. La llave existe, asi
                    # que L1 no la ve; y al saltarla aqui tampoco entraba en `comparables`,
                    # con lo que ademas falseaba la proporcion que usa L3 para el espejo.
                    if k in hojas and meta[1] >= 120:
                        comparables += 1
                        cortos.append(f"{k} (valor {type(v).__name__}, no es texto; "
                                      f"~{meta[1]} en el patron)")
                    continue
                patron = meta[1]
                # Solo se juzgan los campos que en el patron llevan CONTENIDO de verdad.
                # Un campo que en el patron mide 2 caracteres ("si"/"no") no admite escalas.
                if patron >= 120:
                    comparables += 1
                    if len(v) < patron * 0.15:
                        cortos.append(f"{k} ({len(v)} contra ~{patron} del patron)")
                    elif len(v) == patron:
                        iguales.append(f"{k} ({len(v)} caracteres, identico de largo)")
            if cortos:
                flojos += len(cortos)
                self.falla("L2", "FUGA",
                           f"`{nombre}`: {len(cortos)} campos puestos de compromiso",
                           "\n     ".join(cortos[:8]),
                           "El largo del patron no es un objetivo ni un minimo: es el orden "
                           "de magnitud de ese mismo campo bien puesto. Una decima parte no "
                           "es 'adaptado'.",
                           objetivo=f"campos-flojos-{nombre}")
            # 🔴 UN ESPEJO SE RECONOCE POR EL CONJUNTO, NO POR UN CAMPO. La primera version
            # disparaba campo a campo y era ruido: que UN texto largo coincida al caracter
            # con el patron puede ser casualidad, y un hallazgo por cada campo entierra la
            # senal. Lo que delata al espejo es la PROPORCION -- quien clona y solo cambia el
            # nombre deja casi todos los campos intactos. Se exige mas de la mitad de los
            # campos comparables y al menos dos, y la evidencia lleva el reparto: "8 de 10"
            # convence, "1 campo coincide" no.
            if len(iguales) >= 2 and comparables and len(iguales) / comparables > 0.5:
                espejos += len(iguales)
                self.falla("L3", "DUDA",
                           f"`{nombre}`: {len(iguales)} de {comparables} campos largos miden "
                           f"EXACTAMENTE lo mismo que el patron",
                           "\n     ".join(iguales[:8]),
                           "Esa proporcion es la firma de una configuracion CLONADA a la que "
                           "solo se le cambio el nombre. Un campo coincidiendo es casualidad; "
                           "la mayoria, no. Comparar el TEXTO antes de concluir: el largo "
                           "igual es indicio, no prueba.",
                           objetivo=f"posible-espejo-{nombre}")

        if sin_esquema:
            detalle = " · ".join(f"`{n}` ({k} llaves)" for n, k in sorted(sin_esquema))
            self.falla("L5", "DUDA",
                       f"{len(sin_esquema)} campos de configuracion que el esquema de "
                       f"referencia NO cubre",
                       detalle,
                       "El bloque L no los juzga: L1, L2 y L3 solo miran lo que esta en el "
                       "esquema. Que no salgan hallazgos de estos campos no significa que "
                       "esten sanos, significa que nadie los miro.",
                       "Medirlos en un espacio de referencia y anadirlos a "
                       "assets/esquema-configuracion.json, o declararlos fuera de alcance "
                       "con su motivo.",
                       objetivo="campos-fuera-del-esquema")
        self.cubre("L5", "corrido", len(self.campos),
                   f"{len(sin_esquema)} campos de configuracion sin cubrir por el esquema")

        if not revisados:
            for c in ("L1", "L2", "L3"):
                self.cubre(c, "sin_datos", 0,
                           "ningun campo del espacio casa con los del esquema medido")
            return
        self.cubre("L1", "corrido", revisados, f"{faltan} llaves ausentes")
        self.cubre("L2", "corrido", revisados, f"{flojos} campos por debajo de su escala")
        self.cubre("L3", "corrido", revisados, f"{espejos} sospechas de espejo")

    def bloque_pais(self):
        """L4 · COHERENCIA DE PAIS COMPLETA — el control que FER pidio con su ejemplo.

        Sus palabras, 2026-09-08: *"si esta en Guatemala y su validacion de direcciones es
        de Colombia, pues hay que decir: no, eso esta mal, hay que corregirlo."*

        Ningun control anterior lo veia, y no por descuido sino porque cada uno mira una
        dimension distinta: F14 compara contra la plantilla de FABRICA (y la de fabrica es
        colombiana SIEMPRE, elijas el pais que elijas, medido 61 de 61); L3 compara contra
        otro CLIENTE; L1 exige que la llave exista; L2 que no este de compromiso. Una
        configuracion puede pasar los cuatro y seguir diciendole a un guatemalteco que su
        garantia se rige por el Estatuto del Consumidor colombiano.

        Son DOS controles porque hay dos formas de que el pais este mal, y solo la primera
        se ve mirando un campo:

        · **L4 · LOS PAISES DECLARADOS NO COINCIDEN ENTRE SI.** El pais no vive en un sitio:
          vive en uno por asistente (logistico, ventas, carritos y comentarios; el de
          remarketing era el quinto y desde el 24-sep se aparta antes de llegar aqui), cada uno
          con su propia llave y su propio nombre de llave. Un espacio
          medio migrado tiene tres asistentes en un pais y dos en otro, y cada uno se
          comporta segun el suyo. Severidad MUERTO. Un pais VACIO teniendo los demas puesto
          es 🟠: no contradice, pero ese asistente decide sin dato.

        · **L4b · EL CONTENIDO ES DE OTRO PAIS.** El pais declarado dice Guatemala y el texto
          dice PROFECO, Servientrega o COP. Se mide contra `assets/lexico-por-pais.json`.

        🔴 LAS DOS TRAMPAS QUE ESTE CONTROL PODIA TRAER, y como se cierran:

        1. **El marcador ambiguo.** "Envia" es una transportadora colombiana Y el verbo mas
           corriente de un texto de logistica. Un marcador asi no acusa poco: acusa SIEMPRE,
           y a los tres informes el dueno deja de leer el control. Por eso el lexico se
           genera con una regla de admision y guarda los rechazados a la vista.
        2. **El lexico CADUCA.** Una transportadora nueva o una que cierra no da ningun error:
           deja de verse. Por eso las familias se marcan, los hallazgos que salen SOLO de una
           familia que caduca bajan a FUGA, y la cobertura imprime la fecha de medicion. Lo
           que NO caduca -- la moneda y el organismo de consumo -- sostiene la severidad alta.

        Y la cobertura es la de la casa: **un pais que no este en el lexico no se juzga y se
        DECLARA**. El pais es parametro, no puerta: no tener su lexico jamas autoriza a decir
        que su configuracion esta sana.
        """
        def _sin_tildes(s):
            return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                           if unicodedata.category(c) != "Mn")

        # 🔴 EL ALCANCE, y por que hubo que ponerlo: la primera version barria TODOS los
        # campos y acuso a los DOCE productos del fixture por llevar moneda "COP" en un
        # espacio ecuatoriano. El hallazgo no era falso -- era de OTRA auditoria. La moneda
        # de un producto la mira F5, que es de productos; L4 y L4b son de CONFIGURACION, y
        # un control que se sale de su alcance no descubre mas: entierra lo suyo bajo doce
        # lineas que el dueno no puede accionar desde aqui. Se limita a los campos que estan
        # en el esquema medido, y cuando el esquema no esta, se DECLARA que se barrio todo.
        ruta_esq = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "assets", "esquema-configuracion.json")
        solo_config, nota_alcance = None, ""
        if os.path.exists(ruta_esq):
            _esq = json.load(open(ruta_esq, encoding="utf-8"))["asistentes"]
            solo_config = {re.sub(r"[^a-z0-9]", "", n.lower())
                           for campos in _esq.values() for n in campos}
        else:
            nota_alcance = (" · SIN esquema: se barrieron TODOS los campos, tambien los de "
                            "producto, que son de otra auditoria")

        # --------------------------------------------------------------- L4 · los cinco paises
        declarados = {}          # nombre de campo -> (ruta de la llave, valor tal cual)
        textos = {}              # nombre de campo -> [(ruta, texto)] para L4b
        for nombre, campo in self.campos.items():
            if solo_config is not None and \
                    re.sub(r"[^a-z0-9]", "", nombre.lower()) not in solo_config:
                continue
            d = self.valor_json(campo)
            if not isinstance(d, (dict, list)):
                continue
            for ruta, valor in self.caminar(d):
                if not isinstance(valor, str):
                    continue
                ultima = ruta.rsplit(".", 1)[-1]
                if ultima == "pais":
                    declarados[f"{nombre} · {ruta}"] = valor.strip()
                elif len(valor.strip()) >= 3:
                    textos.setdefault(nombre, []).append((ruta, valor))

        if not declarados:
            self.cubre("L4", "sin_datos", 0,
                       "ningun campo del espacio declara pais: no hay nada que cruzar")
            self.cubre("L4b", "NO_CORRIDO", 0,
                       "sin pais declarado no se puede juzgar si el contenido es de otro")
            return

        puestos = {k: v for k, v in declarados.items() if v}
        vacios = [k for k, v in declarados.items() if not v]
        distintos = sorted({_sin_tildes(v) for v in puestos.values()})
        if len(distintos) > 1:
            self.falla("L4", "MUERTO",
                       f"el espacio declara {len(distintos)} PAISES DISTINTOS "
                       f"en {len(puestos)} campos",
                       "\n     ".join(f"{k} = {v!r}" for k, v in sorted(puestos.items())),
                       "El pais no vive en un sitio: cada asistente lee el suyo y decide con "
                       "el. Con dos paises puestos, dos asistentes del mismo espacio validan "
                       "direcciones, calculan tiempos y citan leyes de paises distintos, y "
                       "ninguno da error.",
                       "Decidir cual es el pais del negocio y ponerlo IGUAL en los "
                       f"{len(declarados)} sitios. Es un valor por asistente, no uno global.",
                       objetivo="paises-en-desacuerdo")
        if vacios and puestos:
            self.falla("L4", "ANUNCIADA",
                       f"{len(vacios)} de {len(declarados)} campos declaran el pais VACIO",
                       "\n     ".join(sorted(vacios)),
                       "No contradice a nadie, y por eso no se ve: ese asistente decide sin "
                       "el dato y toma el criterio que traiga horneado, que en la plantilla "
                       "de fabrica es el colombiano.",
                       "Poner el pais tambien ahi. Un pais vacio se ve igual que uno "
                       "configurado: solo se nota contando.",
                       objetivo="paises-vacios")
        self.cubre("L4", "corrido", len(declarados),
                   f"{len(distintos)} pais(es) distinto(s) entre {len(puestos)} campos con "
                   f"valor y {len(vacios)} vacios{nota_alcance}")

        # --------------------------------------------------------------- L4b · el contenido
        ruta_lex = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "assets", "lexico-por-pais.json")
        if not os.path.exists(ruta_lex):
            self.cubre("L4b", "NO_CORRIDO", 0, "falta assets/lexico-por-pais.json")
            return
        lex = json.load(open(ruta_lex, encoding="utf-8"))
        alias, marcadores = lex["alias_de_pais"], lex["marcadores"]
        caduca = lex["familias_que_caducan"]

        if not puestos:
            self.cubre("L4b", "NO_CORRIDO", 0,
                       "todos los campos declaran el pais vacio: no hay contra que comparar")
            return
        # Con dos paises en desacuerdo NO se elige uno: elegir seria inventarse cual es el
        # bueno y acusar al otro de fuga. L4 ya grito; L4b se declara sin correr.
        if len(distintos) > 1:
            self.cubre("L4b", "NO_CORRIDO", 0,
                       "el espacio declara mas de un pais (L4): no hay un pais de referencia "
                       "contra el que juzgar el contenido, y elegir uno seria inventarlo")
            return
        crudo = distintos[0]
        pais = next((p for p, formas in alias.items()
                     if crudo in [_sin_tildes(f) for f in formas]), None)
        if not pais:
            self.cubre("L4b", "NO_CORRIDO", 0,
                       f"el pais declarado ({crudo!r}) no esta en el lexico "
                       f"({lex['_medido']}): NO se juzga y NO se da por sano")
            return

        # 🔴 LA TERCERA TRAMPA, y la descubrio un cliente REAL el 2026-09-17: LA ENUMERACION
        # MULTI-PAIS INTENCIONAL. Un prompt decia "la normativa publicitaria de tu pais -- ej.:
        # SIC en Colombia, PROFECO en Mexico, DIACO en Guatemala" en un espacio declarado
        # COLOMBIA, y este control lo marco MUERTO por PROFECO y DIACO. No era contaminacion:
        # era un texto escrito A PROPOSITO para varios paises, **que nombra el pais declarado y
        # ademas lo pone primero**.
        # La señal que lo distingue: si en la MISMA cadena aparece tambien un marcador del pais
        # declarado, no es contenido heredado de otro espacio -- es una lista. El control no
        # puede callarse (una lista asi tampoco es ideal para un espacio de un solo pais), pero
        # acusar MUERTO es un falso positivo, y un control que acusa en falso se deja de leer a
        # los tres informes. Baja a DUDA y se dice por que.
        propios = {m for m, meta in marcadores.items() if pais in meta["paises"]}

        def _nombra_su_pais(texto, plano):
            for m in propios:
                meta = marcadores[m]
                if meta.get("sigla"):
                    if re.search(rf"\b{re.escape(m)}\b", texto):
                        return meta["literal"]
                elif re.search(rf"\b{re.escape(m)}\b", plano):
                    return meta["literal"]
            # el nombre del pais escrito con todas sus letras tambien cuenta
            for forma in alias.get(pais, []):
                if re.search(rf"\b{re.escape(_sin_tildes(forma))}\b", plano):
                    return forma
            return None

        ajenos, revisados = {}, 0
        enumeraciones = {}
        for nombre, hojas in textos.items():
            for ruta, texto in hojas:
                revisados += 1
                plano = _sin_tildes(texto)
                propio_en_texto = _nombra_su_pais(texto, plano)
                for marca, meta in marcadores.items():
                    if pais in meta["paises"]:
                        continue                      # es del pais declarado: no acusa
                    if meta.get("sigla"):
                        # sensible a mayusculas y a proposito: "COP" suelto es inequivoco,
                        # "cop" en minusculas seria ruido.
                        if not re.search(rf"\b{re.escape(marca)}\b", texto):
                            continue
                    elif not re.search(rf"\b{re.escape(marca)}\b", plano):
                        continue
                    destino = enumeraciones if propio_en_texto else ajenos
                    destino.setdefault(nombre, []).append(
                        (ruta, meta["literal"], meta["familia"], meta["paises"],
                         propio_en_texto))

        # Enumeraciones multi-pais: se DICEN, con severidad baja y nombrando la señal que las
        # separo de una contaminacion. No se callan: en un espacio de un solo pais, una lista
        # de organismos ajenos sigue siendo texto que el cliente no necesita leer.
        for nombre, lista in sorted(enumeraciones.items()):
            propio = next((p for *_, p in lista if p), "el pais declarado")
            self.falla("L4b", "DUDA",
                       f"`{nombre}`: {len(lista)} marcas de otro pais, pero el MISMO texto "
                       f"nombra tambien {propio!r}: parece una ENUMERACION a proposito, "
                       f"no contenido heredado",
                       "\n     ".join(f"{r} -> {lit!r} ({fam}, es de {'/'.join(ps)})"
                                      for r, lit, fam, ps, _ in lista[:10]),
                       f"No se acusa como contaminacion porque el texto SI menciona {pais}. "
                       "Aun asi, en un espacio de un solo pais una lista de organismos o "
                       "monedas ajenas es texto de mas: el cliente lee opciones que no le "
                       "aplican. Se confirma con el dueno si la lista es intencional.",
                       "Si es intencional, se deja y se anota. Si se copio de una plantilla "
                       "multipais, se recorta al pais del espacio.")

        for nombre, lista in sorted(ajenos.items()):
            familias = {f for _, _, f, _, _ in lista}
            # Si TODO lo encontrado sale de familias que caducan, la severidad baja: puede
            # ser un lexico viejo antes que una configuracion mala.
            solo_caduca = all(caduca.get(f, True) for f in familias)
            sev = "FUGA" if solo_caduca else "MUERTO"
            self.falla("L4b", sev,
                       f"`{nombre}`: {len(lista)} marcas de OTRO PAIS en un espacio "
                       f"declarado {pais}",
                       "\n     ".join(f"{r} -> {lit!r} ({fam}, es de {'/'.join(ps)})"
                                      for r, lit, fam, ps, _ in lista[:10]),
                       f"El espacio dice {pais} y su texto habla del sistema de otro pais. "
                       "Al cliente le llega una transportadora que no lo cubre, una moneda "
                       "que no es la suya o una ley que no lo protege, y el asistente lo "
                       "dice con toda seguridad porque para el es su configuracion.",
                       "Reescribir esas llaves con los datos del pais real. Si alguna es "
                       "correcta a proposito (una tienda que si envia a ese pais), va al "
                       "libro de decisiones con su motivo.",
                       objetivo=f"marcas-de-otro-pais-{nombre}")
        self.cubre("L4b", "corrido", revisados,
                   f"{sum(len(v) for v in ajenos.values())} marcas ajenas en "
                   f"{len(ajenos)} campos · lexico de {lex['_medido']}, "
                   f"{len(marcadores)} marcadores, {len(alias)} paises "
                   f"(un pais fuera del lexico NO se juzga){nota_alcance}")

    # ------------------------------------------------------------------ correr
    def correr(self):
        self.bloque_a()
        self.bloque_b()
        if not self.campos:
            self.falla("B1", "MUERTO", "El DUMP no trae campos de bot",
                       "sin campos no hay nada que auditar")
            return self
        self.bloque_c()
        self.bloque_d()
        self.bloque_e()
        self.bloque_f()
        self.bloque_ia()
        self.bloque_g()
        self.bloque_h()
        self.bloque_fabrica()
        self.bloque_i()
        self.bloque_esquema()
        self.bloque_pais()
        # 🔴 J1 · UN CONTROL QUE NO DECLARA ES UN CONTROL INVISIBLE. El diff contra la
        # corrida anterior solo se ejecuta si hay dump anterior, y su `cubre` vivia DENTRO de
        # `comparar()`: sin dump anterior, J1 no aparecia en la tabla de cobertura y su
        # ausencia se leia como "no tenia nada que decir" en vez de "no se corrio". Es la
        # misma cobertura falsa que F13, por otra puerta. Ahora se declara SIEMPRE, y
        # `comparar()` sustituye esta linea cuando de verdad corre.
        self.cubre("J1", "NO_CORRIDO", 0,
                   "no habia dump anterior con el que comparar: esta corrida es una foto, "
                   "no dice que se movio")
        # J2 · el libro de decisiones tambien se declara: si no aparece en la cobertura,
        # nadie sabe si esta corrida silencio hallazgos ni cuantos.
        self.cubre("J2", "corrido" if self.decisiones else "no_corrido",
                   len(self.decisiones),
                   f"{sum(1 for h in self.hallazgos if h['severidad'] == 'DECIDIDO')} "
                   "hallazgos silenciados por decision del dueno"
                   if self.decisiones else "sin libro de decisiones en esta corrida")
        return self


def imprimir(a):
    print("=" * 78)
    print(f"AUDITORIA · {a.d.get('_etiqueta')} · extraido {a.d.get('_extraido')}")
    print("=" * 78)

    print("\nUNIVERSO MEDIDO")
    for k, v in a.universo.items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for kk, vv in v.items():
                print(f"      {kk:32} {vv}")
        else:
            print(f"  {k:34} {v}")

    if a.cambios:
        print(f"\nQUE CAMBIO DESDE LA CORRIDA ANTERIOR ({len(a.cambios)})")
        for tipo, nombre, detalle in a.cambios:
            print(f"  {tipo:8} {nombre:52} {detalle}")
    elif "cambios_desde_anterior" in a.universo:
        print("\nQUE CAMBIO DESDE LA CORRIDA ANTERIOR: nada en los campos de bot")

    decididos = [h for h in a.hallazgos if h["severidad"] == "DECIDIDO"]
    activos = [h for h in a.hallazgos if h["severidad"] != "DECIDIDO"]

    orden = {"MUERTO": 0, "ANUNCIADA": 1, "FUGA": 2, "DUDA": 3}
    if a.alcance != "todo":
        que = ("la CONFIGURACION de los asistentes" if a.alcance == "config"
               else "el CONTENIDO DE PRODUCTO")
        print(f"\nALCANCE · esta corrida juzga {que}.")
        if a.fuera_de_alcance:
            # 🔴 CONTEO Y NADA MAS. Aqui se imprimia ademas el reparto por severidad
            # ("2 muerto · 3 fuga"), y eso era la misma contradiccion que la ley traia en
            # prosa: un conteo se obtiene sin mirar, pero **una severidad exige haber
            # juzgado** -- justo lo que esta corrida tenia prohibido. Decir "3 fuga" sobre
            # productos ES auditar productos, aunque no se nombre el campo. La ley se
            # corrigio el 2026-09-08; el codigo la seguia contradiciendo.
            print(f"  {len(a.fuera_de_alcance)} hallazgos quedaron FUERA DE ALCANCE. No se "
                  f"juzgan aqui y NO estan resueltos: se ven con `--alcance todo`. Aqui no "
                  f"se dice de que son ni como de graves son, porque eso ya seria juzgarlos.")
        else:
            print("  0 hallazgos quedaron fuera de alcance.")
    print(f"\nHALLAZGOS ({len(activos)} sin resolver"
          + (f" · {len(decididos)} ya decididos por el dueno)" if decididos else ")"))
    if not a.hallazgos:
        print("  Ninguno de los controles mecanicos disparo. Eso NO significa que el espacio")
        print("  este sano: mira la cobertura, hay controles que solo se verifican leyendo.")
    for h in sorted(activos, key=lambda x: orden.get(x["severidad"], 9)):
        print(f"\n{SEV.get(h['severidad'], '')} {h['severidad']} · {h['control']} · {h['titulo']}")
        print(f"     evidencia: {h['evidencia']}")
        if h["consecuencia"]:
            print(f"     consecuencia: {h['consecuencia']}")
        if h["accion"]:
            print(f"     accion: {h['accion']}")

    if a._reabiertos:
        print(f"\nDECISIONES QUE CADUCARON ({len(a._reabiertos)}) · la situacion cambio "
              "desde que se decidieron, asi que el hallazgo VUELVE a contar")
        for clave, antes, ahora in a._reabiertos:
            print(f"  🔓 {clave}")
            print(f"       cuando se decidio: {antes[:150]}")
            print(f"       hoy:               {ahora[:150]}")
    if a._sin_foto:
        print(f"\n  aviso: {len(a._sin_foto)} decision(es) sin `evidencia_al_decidir` — NO "
              "pueden caducar solas, quedan silenciadas hasta que alguien las revise a mano. "
              "Anade ese campo con la evidencia del dia en que se decidio.")

    if decididos:
        print(f"\nYA DECIDIDO POR EL DUENO ({len(decididos)}) · no se vuelve a levantar")
        # Una decision AMPLIA que silencia varios hallazgos se declara: silenciar de mas
        # sin avisar es el abuso que el libro podria habilitar.
        from collections import Counter
        amplias = Counter(h.get("clave_decidida") for h in decididos
                          if h.get("decision_forma") == "amplia")
        for c, n in amplias.items():
            if n > 1:
                print(f"  aviso: la decision AMPLIA `{c}` silencia {n} hallazgos a la vez. "
                      "Para silenciar solo uno, escribe su clave completa con `::`.")
        for h in decididos:
            d = h["decision"]
            print(f"  ⚪ {h['control']} · {h['titulo']}")
            print(f"       decision: {d.get('motivo', '(sin motivo)')}"
                  f"  [{d.get('fecha', 'sin fecha')}]")
            if d.get("reabrir_si"):
                print(f"       reabre si: {d['reabrir_si']}")

    print("\nCOBERTURA")

    def orden_control(c):
        m = re.match(r"([A-Z]+)(\d+)([a-z]?)", c["control"])
        return (m.group(1), int(m.group(2)), m.group(3)) if m else (c["control"], 0, "")

    a.cobertura.sort(key=orden_control)
    corridos = sum(1 for c in a.cobertura if c["estado"] == "corrido")
    sin_ver = [c for c in a.cobertura if c["estado"] == "NO_VERIFICADO"]
    for c in a.cobertura:
        rev = f"{c['revisados']} objetos" if c["revisados"] is not None else ""
        print(f"  {c['control']:5} {c['estado']:14} {rev:14} {c['nota']}")
    print(f"\n  {corridos} de {len(a.cobertura)} controles corridos por codigo · "
          f"{len(sin_ver)} exigen lectura humana o panel")
    print("\n  Un cero de hallazgos solo prueba algo si la cobertura fue completa.")
    print("  Lo NO VERIFICADO va al informe declarado, nunca omitido.")


def escribir_handoff(a, destino):
    """El paquete para la skill que SI corrige.

    Esta skill no escribe en Chatea a proposito, pero dejar el arreglo en prosa obliga al
    siguiente chat a reconstruir el contexto entero. Aqui sale ya masticado.
    """
    porskill, preguntas, sin_accion = {}, [], []
    for h in a.hallazgos:
        if h["severidad"] == "DECIDIDO":
            continue
        # Filtrar por "¿tiene `accion`?" ANTES de mirar la severidad descartaba rojos y
        # naranjas reales que se reportan sin una `accion` de una linea (varios D3, C4...):
        # medido en Golden, 22 de 39 hallazgos abiertos se quedaron fuera del paquete, 5 de
        # ellos rojos de un solo disparador. Un 🔴 o 🟠 entra SIEMPRE, tenga o no `accion`
        # explicita: la severidad decide, no la presencia de ese campo.
        # 🔴 EL ARREGLO DE ARRIBA SE HIZO SOLO PARA MUERTO/ANUNCIADA Y NO SE BUSCO SU GEMELO.
        # La rama de FUGA (🟡) conservaba el `if not h.get("accion"): continue` y seguia
        # tirando hallazgos abiertos: medido por el verificador el 2026-09-08, se caian 11
        # mas (F14, F2, G2, los 6 de G3 y los 2 de F13). Clase conocida de esta casa: al
        # tocar una regla de filtrado, buscar sus HERMANAS antes de sellar.
        # Ahora la regla es una sola: **la severidad decide, no la presencia de `accion`.**
        # Solo las DUDAS sin accion concreta se quedan fuera, y hasta esas se cuentan abajo.
        if h["severidad"] in ("MUERTO", "ANUNCIADA", "FUGA"):
            porskill.setdefault(h.get("skill_duena") or "(por determinar)", []).append(h)
            continue
        if not h.get("accion"):
            sin_accion.append(h)
            continue
        if h["severidad"] == "DUDA":
            # Una duda con accion concreta no es basura: es una pregunta que hay que
            # contestar ANTES de tocar. Tirarla dejaba fuera del paquete cosas como
            # "hay entradas activas sin id de anuncio".
            preguntas.append(h)
            continue
        porskill.setdefault(h.get("skill_duena") or "(por determinar)", []).append(h)
    lineas = [f"# Paquete de correccion · {a.d.get('_etiqueta')}",
              "",
              f"Generado por golden-chatea-auditoria sobre el DUMP del "
              f"{a.d.get('_extraido')}. Esta skill NO escribe en Chatea: cada bloque va a "
              "la skill duena del campo.",
              "",
              "**Antes de escribir nada:** medir el escapado del campo completo "
              "(`len(json.dumps(valor)[1:-1])`) y no pasar de 19.000. **Despues de escribir:** "
              "releer del servidor y comparar, porque un `200 ok` puede haber guardado el "
              "contenido cortado.",
              ""]

    # 🔴 CABECERA DE ALCANCE. El paquete se leia como si fuera TODO lo encontrado, y no lo
    # era: lo apartado por alcance no viajaba y nadie lo sabia. Se declara el CONTEO Y NADA
    # MAS -- ni severidad ni control ni campo. Una severidad exige haber JUZGADO el campo, y
    # juzgar productos dentro de una auditoria de configuracion es justo lo prohibido
    # (orden de FER, reincidente). Contar no obliga a mirar; describir, si.
    fuera = getattr(a, "fuera_de_alcance", None) or []
    if fuera or sin_accion:
        lineas.append("## Lo que NO viaja en este paquete")
        lineas.append("")
        if fuera:
            lineas.append(f"- **{len(fuera)} apartados por ALCANCE** (`--alcance "
                          f"{a.alcance}`). Conteo y nada mas: describirlos seria juzgar "
                          "campos que esta corrida tenia prohibido juzgar. Para verlos, "
                          "otra corrida con el alcance que corresponda.")
        if sin_accion:
            lineas.append(f"- **{len(sin_accion)} dudas (🔵) sin accion concreta.** No son "
                          "defectos: son campos sobre los que la herramienta no puede "
                          "decidir sola. Estan en el informe, no en el paquete.")
        lineas.append("")

    if preguntas:
        lineas.append("## Antes de tocar nada · preguntas que hay que contestar")
        lineas.append("")
        lineas.append("Una duda con accion concreta no se corrige a ciegas: se contesta, y la "
                      "respuesta se escribe en el libro de decisiones para que no vuelva a "
                      "levantarse en la proxima corrida.")
        lineas.append("")
        for h in preguntas:
            lineas.append(f"- **{h['control']} · {h['titulo']}** — {h['accion']}")
            lineas.append(f"  - clave para el libro: `{h['clave']}`")
        lineas.append("")

    for skill, hs in sorted(porskill.items()):
        lineas.append(f"## {skill}")
        lineas.append("")
        for h in hs:
            lineas.append(f"### {SEV.get(h['severidad'], '')} {h['control']} · {h['titulo']}")
            if h.get("campo"):
                lineas.append(f"- **Campo:** `{h['campo']}`")
            lineas.append(f"- **Evidencia:** {h['evidencia']}")
            if h.get("consecuencia"):
                lineas.append(f"- **Por que importa:** {h['consecuencia']}")
            lineas.append(f"- **Que hacer:** {h['accion']}")
            lineas.append("")
    Path(destino).write_text("\n".join(lineas))
    return sum(len(v) for v in porskill.values()) + len(preguntas)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    def opcion(bandera):
        return (Path(sys.argv[sys.argv.index(bandera) + 1])
                if bandera in sys.argv else None)

    alcance = "config"
    if "--alcance" in sys.argv:
        alcance = sys.argv[sys.argv.index("--alcance") + 1]
        if alcance not in Auditoria.ALCANCES:
            sys.exit(f"--alcance acepta {' | '.join(Auditoria.ALCANCES)}, no {alcance!r}")
    dump = json.loads(Path(sys.argv[1]).read_text())
    a = Auditoria(dump, alcance=alcance)
    # opt-in: solo cuando FER pide auditar un asistente que saco del ecosistema, en un espacio
    a.incluir_excluidos = "--incluir-excluidos" in sys.argv

    ruta_dec = opcion("--decisiones")
    if ruta_dec and ruta_dec.exists():
        libro = json.loads(ruta_dec.read_text())
        espacio = libro.get("espacio")
        medido = (a.d.get("/flow/bot-fields") or [{}])[0].get("var_ns", "")
        if espacio and not str(medido).startswith(str(espacio)):
            sys.exit(f"El libro de decisiones es del espacio {espacio} y este DUMP es de "
                     f"{medido[:8]}. Un libro de otro espacio silenciaria hallazgos reales.")
        flojas = [d.get("clave", "(sin clave)") for d in libro.get("decisiones", [])
                  if not d.get("motivo") or not d.get("fecha")]
        if flojas:
            sys.exit("El libro tiene decisiones sin motivo o sin fecha: "
                     + ", ".join(flojas)
                     + "\nUna decision sin motivo y sin fecha silencia un hallazgo sin dejar "
                       "rastro de quien lo decidio ni cuando: dentro de tres meses nadie sabe "
                       "si sigue vigente. Completa esos campos y vuelve a correr.")
        a.decisiones = {d["clave"]: d for d in libro.get("decisiones", [])}
        sin_reabrir = [c for c, d in a.decisiones.items() if not d.get("reabrir_si")]
        print(f"Libro de decisiones: {len(a.decisiones)} resueltas por el dueno")
        if sin_reabrir:
            print(f"  aviso: {len(sin_reabrir)} sin `reabrir_si` "
                  f"({', '.join(sin_reabrir)}) — quedan silenciadas para siempre")
        print()
    elif ruta_dec:
        print(f"(no existe {ruta_dec}: se audita sin libro de decisiones)\n")

    a.correr()

    ruta_ant = opcion("--anterior")
    if ruta_ant:
        a.comparar(json.loads(ruta_ant.read_text()))

    imprimir(a)

    destino = opcion("--json")
    if destino:
        destino.write_text(json.dumps(
            {"universo": a.universo, "alcance": a.alcance, "hallazgos": a.hallazgos,
             "fuera_de_alcance": a.fuera_de_alcance, "cobertura": a.cobertura,
             "cambios": a.cambios},
            ensure_ascii=False, indent=1))
        print(f"\nHallazgos en {destino}")

    ho = opcion("--handoff")
    if ho:
        n = escribir_handoff(a, ho)
        print(f"Paquete de correccion ({n} hallazgos accionables) en {ho}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
