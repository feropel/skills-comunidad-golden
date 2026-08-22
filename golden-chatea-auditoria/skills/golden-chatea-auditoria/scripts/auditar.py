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

NO escribe nada en Chatea. Audita y reporta.

Lo que este script NO puede juzgar y queda para lectura humana (marcado H en el catalogo):
coherencia del prompt con el producto real, estructura narrativa, claims del empaque,
URLs vivas, subflujo vivo detras de un disparador, y los cruces contra Dropi, Shopify y Meta.
Esos se declaran como NO VERIFICADO en la cobertura, nunca se omiten en silencio.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TOPES = json.loads((RAIZ / "assets" / "topes-nativos.json").read_text())

TECHO_ESCAPADO = TOPES["techo_bot_field"]["practico_escapado"]
ALERTA = TOPES["techo_bot_field"]["alerta_porcentaje"]

PREFIJOS_CONOCIDOS = [
    "[Comentarios]", "[Comentarios IA]", "[Ventas Wp]", "[Producto Ventas Wp]",
    "[Logistico]", "[Logistica]", "[Logístico]", "[Carritos IA]", "[Carritos]",
    "[Remarketing IA]", "[WhatsApp IA]", "[Whatsapp IA]", "[Novedades]",
    "[Minimax]", "[Meta]", "[Integraciones]", "[General]", "[Confirmaciones]",
    "[GOLDEN Comentarios]",
]

# Secuencias que delatan un texto que se guardo con la codificacion rota. El acento se
# verifica EN EL RENDER: aqui se mira el valor tal como quedo guardado en el servidor.
MOJIBAKE = ["Ã¡", "Ã©", "Ã­", "Ã³", "Ãº", "Ã±", "Ã‘", "â€™", "â€œ", "â€\x9d",
            "Â¿", "Â¡", "Ã\x81", "ï¿½", "�"]

PLACEHOLDERS = ["{{", "TU_TOKEN", "TU_NOMBRE", "TU_TIENDA", "XXXX", "[NOMBRE",
                "[PRODUCTO", "lorem ipsum", "ejemplo.com", "PONER AQUI", "PENDIENTE:"]

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


class Auditoria:
    def __init__(self, dump):
        self.d = dump
        self.hallazgos = []
        self.cobertura = []          # (bloque, control, estado, revisados, nota)
        self.campos = {}
        self.universo = {}
        self.productos = {}
        self._cache = {}
        self._vistos = set()
        self.decisiones = {}     # clave -> {motivo, fecha, reabrir_si}
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
        clave = f"{control}|{objetivo or campo or titulo}"
        h = {
            "control": control, "severidad": sev, "titulo": titulo,
            "evidencia": evidencia, "consecuencia": consecuencia, "accion": accion,
            "clave": clave, "campo": campo, "skill_duena": skill_duena,
        }
        # El libro de decisiones: lo que el dueno ya resolvio no se vuelve a gritar.
        d = self.decisiones.get(clave)
        if d:
            h["severidad_original"] = sev
            h["severidad"] = "DECIDIDO"
            h["decision"] = d
        self.hallazgos.append(h)

    def cubre(self, control, estado, revisados=None, nota=""):
        self.cobertura.append({"control": control, "estado": estado,
                               "revisados": revisados, "nota": nota})

    @staticmethod
    def escapado(valor):
        """El techo real: el flujo copia la config ESCAPADA. Tilde=6, emoji=12."""
        return len(json.dumps(valor if isinstance(valor, str) else
                              json.dumps(valor, ensure_ascii=False))[1:-1])

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
        array/longtext es sospecha de truncada silenciosa, no un descuido de formato."""
        v = campo.get("value")
        if campo.get("var_type") in ("array", "longtext") and isinstance(v, str) and v.strip():
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
        return v

    def campos_pre(self):
        """Los campos indexados, disponibles ya en el bloque A."""
        if not self.campos:
            self.campos = {c["name"]: c for c in (self.d.get("/flow/bot-fields") or [])
                           if isinstance(c, dict) and "name" in c}
        return self.campos

    # ------------------------------------------------------- A · identidad y acceso
    def bloque_a(self):
        me = self.d.get("/me") or {}
        if "_ERROR_HTTP" in me or "_ERROR" in me:
            self.falla("A1", "MUERTO", "El token no responde", json.dumps(me)[:200])
            self.cubre("A1", "corrido")
            return
        self.universo["cuenta"] = me.get("email") or me.get("name") or "?"
        self.cubre("A1", "corrido", nota=f"/me respondio: {self.universo['cuenta']}")

        # La identidad sale del servidor: el prefijo del var_ns de los campos, nunca el
        # nombre del archivo del token.
        campos = self.d.get("/flow/bot-fields") or []
        ns = {re.match(r"^(f\d+)", c.get("var_ns", "")).group(1)
              for c in campos if re.match(r"^(f\d+)", c.get("var_ns", ""))}
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
                     "ECUADOR": "USD", "PANAMA": "USD", "PARAGUAY": "PYG"}
        esperada = COHERENTE.get(pais.strip().upper())
        if esperada and monedas and monedas != {esperada}:
            self.falla("A3", "DUDA",
                       "El pais declarado y la moneda de los productos no concuerdan",
                       f"pais={pais.strip()!r} espera {esperada}, productos en {sorted(monedas)}",
                       "Es la firma de una plantilla clonada de otro pais.",
                       "Confirmar cual manda antes de tocar nada.")
        self.cubre("A3", "corrido", len(monedas) + 1,
                   f"pais {pais.strip() or '(vacio)'} contra {sorted(monedas)}")

        # A4 · los canales, uno por uno (no basta con que el endpoint responda)
        canales = self.d.get("/workspace-settings/channels")
        conectados, caidos = [], []
        if canales:
            for ruta, hoja in self.caminar(canales):
                if isinstance(hoja, bool) or str(hoja).lower() in ("connected", "verified",
                                                                   "active", "ok"):
                    (conectados if hoja not in (False, "false") else caidos).append(ruta)
                elif str(hoja).lower() in ("disconnected", "expired", "invalid", "failed"):
                    caidos.append(f"{ruta}={hoja}")
        for c in caidos:
            self.falla("A4", "MUERTO", "Hay un canal caido o desconectado", str(c),
                       "El asistente que dependa de ese canal esta muerto, y la config "
                       "se ve perfecta.")
        self.universo["canales"] = {"conectados": len(conectados), "caidos": len(caidos)}
        self.cubre("A4", "corrido" if canales else "sin_datos",
                   len(conectados) + len(caidos),
                   "canales inspeccionados uno a uno" if canales else "el endpoint no devolvio datos")
        self.cubre("A5", "NO_VERIFICADO",
                   nota="el token de Meta se comprueba en el panel; la API no lo expone")

    # ---------------------------------------------------------- B · inventario
    def bloque_b(self):
        campos = self.d.get("/flow/bot-fields") or []
        self.campos = {c["name"]: c for c in campos if isinstance(c, dict) and "name" in c}
        conteo = (self.d.get("_conteos") or {}).get("/flow/bot-fields") or {}
        traidos, declarados = conteo.get("traidos"), conteo.get("declarados_por_servidor")
        self.universo["campos_bot"] = len(self.campos)
        self.universo["campos_declarados"] = declarados

        if isinstance(declarados, int) and traidos != declarados:
            self.falla("B1", "MUERTO",
                       "El inventario esta incompleto: la paginacion no se agoto",
                       f"traidos {traidos}, el servidor declara {declarados}",
                       "Un denominador incompleto invalida el resto del informe.",
                       "Repetir la extraccion antes de leer ningun hallazgo.")
        self.cubre("B1", "corrido", len(self.campos),
                   f"servidor declara {declarados}")

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

        uf = self.d.get("/flow/user-fields")
        self.universo["campos_usuario"] = len(uf) if isinstance(uf, list) else None
        dec_uf = ((self.d.get("_conteos") or {}).get("/flow/user-fields") or {}
                  ).get("declarados_por_servidor")
        completo = (dec_uf is None) or (self.universo["campos_usuario"] == dec_uf)
        self.cubre("B2", "corrido" if (isinstance(uf, list) and completo) else
                   "PARCIAL" if isinstance(uf, list) else "sin_datos",
                   self.universo["campos_usuario"],
                   (f"el servidor declara {dec_uf}: revisados "
                    f"{self.universo['campos_usuario']} de {dec_uf}" if not completo else
                    "el limite por workspace se lee en el panel, no por API"))

        # Asistentes por prefijo real, no por lo que se supone instalado.
        prefijos = {}
        for n in self.campos:
            m = re.match(r"^\[[^\]]+\]", n)
            prefijos.setdefault(m.group(0) if m else "(sin prefijo)", []).append(n)
        self.universo["asistentes"] = {k: len(v) for k, v in sorted(prefijos.items())}
        desconocidos = [p for p in prefijos if p not in PREFIJOS_CONOCIDOS]
        if "(sin prefijo)" in prefijos:
            self.falla("B3", "DUDA",
                       f"{len(prefijos['(sin prefijo)'])} campos no pertenecen a ningun asistente",
                       f"{sorted(prefijos['(sin prefijo)'])}",
                       "Quedan fuera de los controles por asistente: no se sabe quien los lee.",
                       "Clasificarlos o declararlos fuera de alcance.")
        if desconocidos:
            self.falla("B3", "DUDA",
                       "Hay asistentes o versiones que esta skill todavia no sabe auditar",
                       f"prefijos no catalogados: {desconocidos}",
                       "Sus campos quedan fuera de los controles especificos.",
                       "Anadirlos al catalogo o declararlos fuera de alcance en el informe.")
        self.cubre("B3", "corrido", len(prefijos))

        # B6 · lo que FALTA, no solo lo que hay. Detectar prefijos presentes nunca puede
        # contestar "esta completa la instalacion": para eso hace falta la lista de esperados.
        esperados = json.loads((RAIZ / "assets" / "asistentes-esperados.json").read_text())
        faltan = []
        for nombre, firma in esperados["asistentes"].items():
            presentes = [f for f in firma["campos_firma"] if f in self.campos]
            if not presentes:
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
        self.universo["asistentes_esperados"] = (
            f"{len(esperados['asistentes']) - len(faltan)} de {len(esperados['asistentes'])} presentes")
        self.cubre("B6", "corrido", len(esperados["asistentes"]),
                   f"{len(faltan)} sin instalar")

        for clave in ("/flow/subflows", "/flow/tags", "/flow/ai-agents", "/flow/ai-tasks",
                      "/flow/inbound-webhooks"):
            v = self.d.get(clave)
            self.universo[clave] = len(v) if isinstance(v, list) else None
        self.cubre("B4", "corrido")

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
                    continue
                rutas_revisadas += 1
                if len(hoja) > tope:
                    self.falla("C3", "ANUNCIADA",
                               f"`{n}` → `{ruta}` supera su tope nativo",
                               f"{len(hoja):,} caracteres sobre {tope:,}",
                               "Funciona hoy, pero el dia que alguien abra ese formulario en "
                               "el panel y guarde, el campo se corta y se pierde el texto.",
                               f"Recortar a {tope:,} con la skill de configuracion.")
        self.cubre("C3", "corrido", rutas_revisadas)

        # C4 · tipo del campo
        candidatos = [(n, c) for n, c in self.campos.items()
                      if c.get("var_type") == "array"
                      and len(json.dumps(c.get("value") or "")[1:-1]) > TECHO_ESCAPADO * 0.8]
        for n, c in candidatos:
            esc = len(json.dumps(c.get("value") or "")[1:-1])
            self.falla("C4", "ANUNCIADA",
                       f"`{n}` sigue siendo `array` y va por el {esc / TECHO_ESCAPADO:.0%}",
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
                    continue
                destino = (e.get("name") or "").strip()
                if not destino:
                    self.falla("D3", "MUERTO",
                               f"`{nombre_disp}`: hay una entrada SIN destino",
                               f"entrada {i}: {json.dumps(e, ensure_ascii=False)[:160]}",
                               "Un disparo que entra por ahi no lleva a ningun producto.")
                    continue
                registrados[destino] = e
                registrados_todos.setdefault(destino, []).append(nombre_disp)

                # D5 · las siete ranuras · se revisa TODA entrada, tenga producto o no
                for etiqueta in ("keyW", "idAd"):
                    valor = e.get(etiqueta) or ""
                    if not isinstance(valor, str):
                        continue
                    ranuras = valor.count(",") + 1
                    if ranuras != 7:
                        self.falla("D5", "DUDA",
                                   f"`{nombre_disp}` → `{destino}`: `{etiqueta}` no tiene 7 ranuras",
                                   f"{ranuras} ranuras: {valor[:120]!r}",
                                   "O el estandar de 7 esta viejo o el valor esta malformado: "
                                   "se confirma en el panel antes de tocarlo.")
                    if etiqueta == "keyW" and not valor.strip(", "):
                        self.falla("D3", "MUERTO",
                                   f"`{nombre_disp}` → `{destino}`: la palabra clave esta VACIA",
                                   f"{valor!r} · estado {e.get('estado')!r}",
                                   "Una entrada activa sin palabra clave no puede entrar.")

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

            # D3 · entradas que apuntan al vacio
            al_vacio = sorted(set(registrados) - cargados, key=self.orden_ranura)
            if al_vacio:
                self.falla("D3", "MUERTO",
                           f"`{nombre_disp}`: {len(al_vacio)} de {len(registrados)} entradas "
                           "apuntan a un campo vacio o inexistente",
                           f"{al_vacio}",
                           "El disparo entra y no encuentra producto.")

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
                        self.falla("D1", "MUERTO",
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

        # E3 · credencial de voz heredada
        for n, prod in self.productos.items():
            voz = prod.get("voz_con_ia") or {}
            api = voz.get("api_key") or ""
            if api and not str(api).startswith("<<REDACTADO"):
                self.falla("E3", "FUGA",
                           f"`{n}` lleva una credencial de voz dentro del producto",
                           f"`voz_con_ia.api_key` presente, {len(str(api))} caracteres, "
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
            for ruta, hoja in self.caminar(prod):
                if isinstance(hoja, str) and "media.chateapro.app" in hoja:
                    m = re.search(r"media\.chateapro\.app/temp/\d{6}/(\d+)/", hoja)
                    if m:
                        cuentas_img.setdefault(m.group(1), []).append(f"{n} → {ruta}")
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
        self.cubre("F7", "corrido", len(self.productos))
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
        self.cubre("G2", "corrido" if dominio else "sin_datos")
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
        objetos = cadenas = 0
        moji, apert, marcas = [], [], []
        for etiqueta, zona in zonas.items():
            if not isinstance(zona, dict):
                continue
            for ns, cuerpo in zona.items():
                objetos += 1
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
        self.universo["zona_ia"] = {"objetos": objetos, "cadenas": cadenas}
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
        self.cubre("F13", "corrido", objetos,
                   f"{cadenas} cadenas de agentes y tareas de IA")

    # ------------------------------------------- I · cordura del propio auditor
    def bloque_i(self):
        # I3 · lo que entra al DUMP se audita o se declara. Nada en tierra de nadie.
        auditadas = {"/me", "/team-info", "/flow/bot-fields", "/flow/user-fields",
                     "/workspace-settings/channels", "_agentes_detalle", "_tareas_detalle",
                     "_conteos", "_etiqueta", "_extraido", "_token_archivo"}
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
        viejos = {c["name"]: c for c in (anterior.get("/flow/bot-fields") or [])
                  if isinstance(c, dict) and "name" in c}
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
            self.cambios.append(("EDITADO", n,
                                 f"{len(va):,} → {len(vn):,} caracteres "
                                 f"({signo}{en - ea:,} escapados)"))
            if ea <= TECHO_ESCAPADO < en:
                self.falla("C1", "MUERTO",
                           f"`{n}` CRUZO el techo escapado desde la corrida anterior",
                           f"{ea:,} → {en:,} escapados",
                           "El cambio que lo cruzo es el sospechoso inmediato.",
                           "Revertir o compactar ese cambio.", objetivo=f"cruce-techo-{n}")
        self.universo["cambios_desde_anterior"] = len(self.cambios)
        self.cubre("J1", "corrido", len(set(viejos) | set(nuevos)),
                   f"diff contra {anterior.get('_extraido', 'corrida anterior')}")

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
        self.bloque_i()
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

    if decididos:
        print(f"\nYA DECIDIDO POR EL DUENO ({len(decididos)}) · no se vuelve a levantar")
        for h in decididos:
            d = h["decision"]
            print(f"  ⚪ {h['control']} · {h['titulo']}")
            print(f"       decision: {d.get('motivo', '(sin motivo)')}"
                  f"  [{d.get('fecha', 'sin fecha')}]")
            if d.get("reabrir_si"):
                print(f"       reabre si: {d['reabrir_si']}")

    print("\nCOBERTURA")
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
    porskill = {}
    for h in a.hallazgos:
        if h["severidad"] in ("DECIDIDO", "DUDA") or not h.get("accion"):
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
    return sum(len(v) for v in porskill.values())


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    def opcion(bandera):
        return (Path(sys.argv[sys.argv.index(bandera) + 1])
                if bandera in sys.argv else None)

    dump = json.loads(Path(sys.argv[1]).read_text())
    a = Auditoria(dump)

    ruta_dec = opcion("--decisiones")
    if ruta_dec and ruta_dec.exists():
        libro = json.loads(ruta_dec.read_text())
        espacio = libro.get("espacio")
        medido = (a.d.get("/flow/bot-fields") or [{}])[0].get("var_ns", "")
        if espacio and not str(medido).startswith(str(espacio)):
            sys.exit(f"El libro de decisiones es del espacio {espacio} y este DUMP es de "
                     f"{medido[:8]}. Un libro de otro espacio silenciaria hallazgos reales.")
        a.decisiones = {d["clave"]: d for d in libro.get("decisiones", [])}
        print(f"Libro de decisiones: {len(a.decisiones)} resueltas por el dueno\n")
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
            {"universo": a.universo, "hallazgos": a.hallazgos, "cobertura": a.cobertura,
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
