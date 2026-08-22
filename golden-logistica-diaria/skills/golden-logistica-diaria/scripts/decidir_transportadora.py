#!/usr/bin/env python3
"""Decide transportadora pedido por pedido.

  1. Precio de TODAS las que llegan a ese municipio, re-evaluando desde cero
  2. Cómo se comporta cada una EN ESE MUNICIPIO (Torre de Dropi)
  3. Balance precio contra efectividad -> costo real
  4. La huella del cliente entra SOLO a desempatar cuando está apretado

REGLA: que un cliente no tenga historial con una transportadora NO es una mancha.
La ausencia nunca penaliza; simplemente no participa del desempate.

Todo lo específico de una tienda es PARÁMETRO. No hay nada quemado.

  python3 decidir_transportadora.py --config config.json
  python3 decidir_transportadora.py --dropi d.json --torre t.json --fletes f.json \\
      --retorno r.json --operativas ENVIA,INTERRAPIDISIMO,VELOCES --factor <el de calibracion>
"""
import argparse, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json
from comun import (tel10, pesos, avisar_banderas, pide_oficina, es_oficina_de_inter,
                   indice_de_oficinas)   # `pesos` vivia aqui duplicado: un solo formato, un solo sitio


def norm(t):
    t = unicodedata.normalize("NFD", (t or "").upper())
    return "".join(c for c in t if unicodedata.category(c) != "Mn").strip()


def fila_torre(fila):
    """UNA fila de la Torre, venga como venga, normalizada a un dict interno.

    POR QUE EXISTE, y es una rotura en produccion del 2026-08-16: la rutina que
    regenera `TORRE-MUNICIPIOS.json` migro a la API FENIX y **cambio el contrato de las
    filas sin avisar y sin version de esquema**:
      antes  {"t": "ENVIA", "pct": 81.93, "ent": 38353, "dev": 8457, "dias": 2.82, ...}
      ahora  ["ENVIA", 73.83, 149568]                        = [transportadora, pct, n]
    El motor hacia `{x["t"]: x for x in v}` y murio con
    `TypeError: list indices must be integers or slices, not str` — para CUALQUIER
    tienda, sin decir que archivo ni por que. **Un insumo externo puede cambiar de forma
    cualquier dia; el que lo lee es quien tiene que estar preparado.**

    DOS COSAS SE PIERDEN CON EL FORMATO NUEVO, y las dos se declaran en vez de fingirse:
      · `ent`/`dev` por separado -> solo queda el total `n`. El motor solo necesitaba la
        suma, asi que aqui no hay dano: se rellena `n` y `ent`/`dev` quedan en None.
      · **`dias` ya no viene**, y esa si duele: el motor la imprimia con
        `round(m.get("dias", 0), 1)`, o sea que con el formato nuevo **habria impreso
        «0 dias de entrega» para todo el mundo**. Eso no es una rotura, es algo peor:
        un numero falso con cara de medido. Se devuelve None y el informe dice que la
        Torre ya no lo trae.

    Levanta ValueError con la fila de muestra si la forma no es ninguna de las dos: el
    proximo cambio de contrato tiene que morir hablando, no con un TypeError crudo.
    """
    if isinstance(fila, dict) and "t" in fila and "pct" in fila:
        ent, dev = fila.get("ent"), fila.get("dev")
        n = (ent + dev) if (ent is not None and dev is not None) else fila.get("n")
        return {"t": fila["t"], "pct": float(fila["pct"]), "n": n,
                "ent": ent, "dev": dev, "dias": fila.get("dias")}
    if (isinstance(fila, (list, tuple)) and len(fila) == 3
            and isinstance(fila[0], str) and not isinstance(fila[1], str)):
        return {"t": fila[0], "pct": float(fila[1]), "n": int(fila[2]),
                "ent": None, "dev": None, "dias": None}
    raise ValueError(repr(fila)[:140])


class Motor:
    def __init__(self, cfg):
        self.cfg = cfg
        self.D = leer_json(cfg["dropi"])
        # F7: una cosecha a medias no se decide. El volcado viejo no traia la marca;
        # ausencia se trata como desconocida y tambien frena, salvo bandera explicita.
        completa = self.D.get("cosecha_completa")
        if completa is not True and not cfg.get("aceptar_cosecha_incompleta"):
            motivo = self.D.get("motivo_corte") or (
                "el volcado no dice si la cosecha quedo completa (es de una version vieja)")
            sys.exit(
                f"COSECHA NO CONFIABLE: {motivo}.\n"
                "Decidir sobre un conjunto incompleto produce un informe que parece entero "
                "y no lo es. Vuelve a cosechar, o pon 'aceptar_cosecha_incompleta': true "
                "en el config si sabes lo que estas haciendo.")
        _torre = leer_json(cfg["torre"])
        self.TC = _torre["TC"]
        # DE QUE TORRE SE DECIDIO HOY. Va a la decision y al informe, no solo a la
        # consola: el factor de calibracion de Golden salto 0,92 -> 1,00 el 2026-08-16
        # sin que nadie tocara un pedido, solo porque la ventana de la Torre cambio.
        # Un numero que se mueve por debajo del lector, sin decirlo, es un numero que
        # el lector no puede defender cuando le pregunten.
        self.torre_generado = _torre.get("generado")
        self.torre_rango = _torre.get("rango")
        self.torre_nota = _torre.get("nota_ventana")
        self.torre_fuente = _torre.get("fuente")
        # EL LISTADO DE OFICINAS DE INTERRAPIDISIMO. Opcional a proposito: la skill
        # tiene que seguir corriendo sin el. Pero si falta, el informe lo DICE — no
        # poder cruzar no es lo mismo que haber cruzado y no encontrar nada.
        self.OFI, self.ofi_fecha, self.ofi_total = {}, None, 0
        if cfg.get("oficinas_inter"):
            _of = leer_json(cfg["oficinas_inter"])
            if _of.get("cosecha_completa") is not True:
                sys.exit(
                    f"EL LISTADO DE OFICINAS ESTA INCOMPLETO: {cfg['oficinas_inter']}\n"
                    f"  motivo: {_of.get('motivo_corte') or 'no lo declara'}\n"
                    "  Un listado a medias es peor que ninguno: los municipios que\n"
                    "  faltan salen como «no es una oficina» y esa es justo la\n"
                    "  respuesta que manda el paquete a la competencia. Vuelve a\n"
                    "  cosecharlo con scripts/cosechar-oficinas-inter.js.")
            self.OFI, self.ofi_fecha, self.ofi_total = indice_de_oficinas(_of)
        self.FLET = leer_json(cfg["fletes"])["R"]
        _ret = leer_json(cfg["retorno"])
        _claves = sorted(k for k in _ret if k.startswith("medido_"))
        if not _claves:
            sys.exit(f"El archivo de retorno {cfg['retorno']} no trae ninguna clave 'medido_*'.")
        self.retorno_medido_el = _claves[-1]      # la mas reciente, no una quemada
        self.RET = _ret[self.retorno_medido_el]
        self.OPER = set(cfg["operativas"])
        # B9: el factor NO se copia a mano al config. Si se copia, envejece y contradice
        # al archivo; y si falta, caer a 1.0 en silencio infla la efectividad un 34%.
        if cfg.get("calibracion"):
            # Presente pero corrupta = mensaje legible, no KeyError ni ValueError crudos.
            try:
                _cal = leer_json(cfg["calibracion"])
                self.factor = float(_cal["factor"])
            except (KeyError, ValueError, TypeError) as e:
                sys.exit(f"El archivo de calibracion {cfg['calibracion']} existe pero no se "
                         f"puede leer su factor ({type(e).__name__}: {e}). No se asume 1.0.")
            self.factor_de = f"{cfg['calibracion']} (calculado {_cal.get('_calculado','?')})"
            self.factor_fuente = _cal.get("_FUENTE", "el archivo no declara de donde sale")
        elif cfg.get("factor_tienda") is not None:
            self.factor = float(cfg["factor_tienda"])
            self.factor_de = "el config, a mano"
            print("AVISO: el factor viene copiado en el config. Lo correcto es apuntar "
                  "'calibracion' al archivo, que se recalcula solo.", file=sys.stderr)
        else:
            sys.exit("Falta el factor de la tienda. Pon 'calibracion' apuntando al archivo "
                     "de calibracion, o 'factor_tienda' con el numero. No se asume 1.0: "
                     "asumirlo infla la efectividad y mueve pedidos por una diferencia falsa.")
        # B9: nada de 0.40 quemado. Ese numero era la ganancia NETA puesta donde va la
        # BRUTA, y subvaluaba en un tercio lo que cuesta una entrega fallida: con 0,40
        # salian 11 cambios, con 0,60 salen 27. Un default silencioso cambia decisiones
        # sin que nadie se entere.
        if cfg.get("margen") is None:
            sys.exit("Falta 'margen' en el config: la fraccion de la venta que se pierde si "
                     "el pedido se devuelve, medida como (venta - costo) / venta. NO se asume: "
                     "un margen supuesto mueve pedidos por una diferencia que no existe.")
        self.margen = float(cfg["margen"])
        self.apretado = float(cfg.get("apretado", 3000))
        self.min_huella = int(cfg.get("min_huella", 3))
        self.mala_huella = float(cfg.get("mala_huella", 60))
        self.ventaja_min = float(cfg.get("ventaja_minima", 20))
        # Sin default quemado: si no se declara, no se restringe a ninguna.
        self.oficina_solo = cfg.get("oficina_solo")
        # Filtro de volumen: un porcentaje sin muestra no decide. La Torre daba
        # Envia "100%" en Leticia con n=4 y en vivo no cubria; la buena era Inter
        # con 1.961 envios. Una transportadora entra a comparar solo si tiene
        # min_envios_muni Y min_cuota_muni del total del municipio.
        self.min_envios_muni = int(cfg.get("min_envios_muni", 50))
        self.min_cuota_muni = float(cfg.get("min_cuota_muni", 5.0))
        self.FL = {(norm(r["dep"]), norm(r["ciu"])): r for r in self.FLET}
        # EL ESQUEMA DE LA TORRE SE VALIDA AL CARGAR, y muere hablando.
        # Aqui vivia `{x["t"]: x for x in v}`: un dict comprehension que, el dia que el
        # insumo cambio de forma, reviento con un TypeError crudo sin nombrar el archivo
        # ni la fecha ni la fila. **La compuerta no puede estar en el uso del dato: tiene
        # que estar en su lectura**, que es el unico sitio donde todavia se sabe de que
        # archivo se habla.
        self.TORRE = {}
        self.torre_sin_dias = 0
        _total_filas = 0
        for k, v in self.TC.items():
            st, ci = k.split("|")
            filas = {}
            for cruda in v:
                try:
                    f = fila_torre(cruda)
                except (ValueError, TypeError, IndexError, KeyError) as e:
                    sys.exit(
                        f"TORRE-MUNICIPIOS CON ESQUEMA DESCONOCIDO: {cfg['torre']}\n"
                        f"  municipio de la muestra : {k}\n"
                        f"  fila que no se entiende : {repr(cruda)[:140]}\n"
                        f"  generado                : {self.torre_generado or 'no lo declara'}\n"
                        f"  rango                   : {self.torre_rango or 'no lo declara'}\n"
                        f"  fuente                  : {self.torre_fuente or 'no la declara'}\n"
                        f"  ({type(e).__name__}: {e})\n"
                        "  Se conocen DOS formas de fila: el objeto {t, pct, ent, dev, dias}\n"
                        "  y la lista posicional [transportadora, pct, n]. Esta no es ninguna.\n"
                        "  El archivo NO lleva version de esquema, asi que un cambio de "
                        "contrato\n  solo se descubre aqui. No se decide sobre un insumo que "
                        "no se entiende.")
                filas[f["t"]] = f
                _total_filas += 1
                if f["dias"] is None:
                    self.torre_sin_dias += 1
            self.TORRE[(norm(st), norm(ci))] = filas
        self.torre_filas = _total_filas
        self.COUR = {int(k): v for k, v in (self.D.get("couriers") or {}).items()}

    def frac_ret(self, t):
        d = self.RET.get(t, {})
        return d["fraccion"] if d.get("confianza") in ("alta", "media") else 1.0

    def huella(self, h, nombre):
        if not h or not h.get("found"):
            return None
        ent = dev = 0
        for b in ("my_shop", "other_shops"):
            for c in (h.get("context_analysis", {}).get(b, {}) or {}).get("by_courier", []) or []:
                if self.COUR.get(c.get("courier_id")) == nombre:
                    ent += c.get("delivered", 0); dev += c.get("returned", 0)
        n = ent + dev
        return {"n": n, "ent": ent, "dev": dev, "pct": round(100 * ent / n, 1)} if n else None

    def candidatas(self, o, h):
        dep, ciu = norm(o.get("state")), norm(o.get("city"))
        precios = {k: round(v) for k, v in (self.FL.get((dep, ciu)) or {}).get("m", {}).items()}
        muni = self.TORRE.get((dep, ciu), {})
        # LA RECOGIDA EN PUNTO SE DETECTA POR LO PEGADO A LA PALABRA, no por la palabra.
        # Aqui vivia `re.search(r"oficina|reclame", dir)` y daba VERDE a «oficina 303
        # Edificio Central», que es la direccion de trabajo de una clienta. El detector
        # entero, con sus tres estados y su banco ajeno, vive en comun.pide_oficina.
        # Se le pasan las operativas Y la que el pedido ya trae: un punto puede ser de
        # una transportadora que la bodega hoy no despacha, y seguir siendo un punto.
        modo_ofi, self.razon_oficina = pide_oficina(
            o.get("dir"), list(self.OPER) + ([o.get("carrier")] if o.get("carrier") else []))
        # Y EL CRUCE CONTRA EL LISTADO REAL, que caza lo que ninguna palabra delata:
        # la direccion de la oficina escrita pelada. Manda sobre el detector de
        # palabras porque es un HECHO comprobado contra una lista, no una lectura de
        # texto. Si sale «igual», esto es un punto de recogida aunque no lo diga.
        cruce, razon_cruce = es_oficina_de_inter(o.get("dir"), o.get("city"), self.OFI)
        if cruce == "igual":
            modo_ofi, self.razon_oficina = "punto", razon_cruce
        elif cruce == "parecida" and modo_ofi == "direccion":
            modo_ofi, self.razon_oficina = "dudoso", razon_cruce
        self.cruce_oficina = cruce
        oficina = modo_ofi in ("punto", "dudoso")
        self.modo_oficina = modo_ofi
        ticket = float(o.get("total") or 0)
        # LA UTILIDAD QUE SE PIERDE: LA REAL DEL PEDIDO SI EL VOLCADO LA TRAE.
        #
        # Aqui se calculaba SIEMPRE `ticket × margen`, con el margen del config — un
        # supuesto igual para todos los pedidos. Pero Dropi manda la ganancia real de
        # cada pedido en `dropshipper_amount_to_win`, y usar el supuesto teniendo el
        # dato es decidir con una estimacion habiendo un hecho al lado.
        #
        # MEDIDO POR LOGISTICA GOLDEN el 2026-08-11 sobre sus 132 pedidos accionables
        # (todos traian el campo): la diferencia media contra el 0,35 supuesto fue de
        # **$14.085 por pedido**, y en el pedido {PEDIDO_EJEMPLO_5} la decision CAMBIA —
        # con la ganancia real gana una transportadora y con el supuesto, otra.
        # (En el volcado de Dolce del mismo dia el campo no venia en ninguno de sus 23
        # accionables: por eso el respaldo importa tanto como el dato.)
        #
        # El margen del config queda como RESPALDO DECLARADO: se usa cuando el pedido
        # no trae su ganancia, y el informe dice cual de los dos uso — un numero que
        # unas veces es medido y otras supuesto, sin decir cual, no se puede leer.
        _real = o.get("dropshipper_amount_to_win")
        try:
            utilidad = float(_real) if _real not in (None, "") else None
        except (TypeError, ValueError):
            utilidad = None
        if utilidad is None:
            utilidad = ticket * self.margen
            self.utilidad_fuente = "margen del config (el pedido no trae ganancia real)"
            self.n_supuesta = getattr(self, "n_supuesta", 0) + 1
        else:
            self.utilidad_fuente = "ganancia REAL del pedido (dropshipper_amount_to_win)"
            self.n_real = getattr(self, "n_real", 0) + 1
        # `n` lo rellena `fila_torre` con la suma en el formato viejo y con el total
        # que ya viene sumado en el nuevo. Un solo campo, dos contratos.
        total_muni = sum((v["n"] or 0) for v in muni.values())
        out, descartadas = [], []
        for t, flete in precios.items():
            if t not in self.OPER:
                continue
            if oficina and self.oficina_solo and t != self.oficina_solo:
                continue
            m = muni.get(t)
            if not m:
                continue
            envios = m["n"] or 0
            cuota = (100.0 * envios / total_muni) if total_muni else 0.0
            if envios < self.min_envios_muni or cuota < self.min_cuota_muni:
                descartadas.append({"t": t, "envios": envios, "cuota": round(cuota, 1),
                                    "razon": "muestra insuficiente en ese municipio"})
                continue
            p = m["pct"] / 100 * self.factor
            costo = flete + (1 - p) * (flete * self.frac_ret(t) + utilidad)
            out.append({"t": t, "flete": flete, "pct_muni": m["pct"],
                        "envios_muni": m["n"],
                        # None, NUNCA 0: la Torre nueva no trae `dias` y un cero aqui
                        # se lee como «entrega el mismo dia». La ausencia se declara.
                        "dias": round(m["dias"], 1) if m["dias"] is not None else None,
                        "p": round(100 * p, 1), "costo": round(costo), "huella": self.huella(h, t)})
        out.sort(key=lambda c: c["costo"])
        self.ultimas_descartadas = descartadas
        return out, oficina

    def _tasa(self, c):
        """% de entrega de ESTE cliente con ESA transportadora, o None sin muestra."""
        hh = c.get("huella")
        if not hh or hh["n"] < self.min_huella:
            return None
        return hh["ent"] / hh["n"] * 100

    def decidir(self, o, h):
        cands, _ = self.candidatas(o, h)
        if not cands:
            return None, "SIN COBERTURA", []

        # ------------------------------------------------------------------
        # REGLA (a) DE FER, y va ANTES de todo lo demas.
        # Su palabra: "solo se paga mas si a la otra le ha ido mucho mejor, O SI A LA
        # BARATA LE HA IDO MAL DE VERDAD, por debajo del 60%". La segunda mitad NO
        # esta condicionada a que el empate sea apretado — la banda fue invento
        # nuestro, no suyo.
        # Vivia dentro del desempate, asi que cuando una ganaba clara por costo la
        # huella no se miraba nunca. Caso real: {CLIENTA_A}, a quien Veloces le
        # habia fallado 5 de 8 veces, salia asignada a Veloces porque ganaba por
        # costo. A un cliente al que una transportadora le ha fallado de verdad no se
        # le manda por ahi aunque sea la mas barata.
        # ------------------------------------------------------------------
        gana = cands[0]
        tasa_g = self._tasa(gana)
        if tasa_g is not None and tasa_g < self.mala_huella:
            otras = cands[1:]
            buenas = [c for c in otras if (t := self._tasa(c)) is not None and t >= self.mala_huella]
            if buenas:
                return max(buenas, key=self._tasa), "HUELLA_MALA", cands
            if otras:
                # ninguna con historial decente: la siguiente por costo, que ya viene ordenada
                return otras[0], "HUELLA_MALA", cands

        if len(cands) == 1 or (cands[1]["costo"] - cands[0]["costo"]) >= self.apretado:
            return cands[0], "CLARO", cands

        empate = [c for c in cands if c["costo"] - cands[0]["costo"] < self.apretado]
        barata = min(empate, key=lambda c: c["flete"])
        tasa_b = self._tasa(barata)

        # b) solo se paga más si a otra le ha ido MUCHO mejor. 5 de 6 es bueno.
        for c in sorted(empate, key=lambda x: x["costo"]):
            if c is barata or not c["huella"] or c["huella"]["n"] < self.min_huella:
                continue
            if tasa_b is not None and (c["huella"]["ent"] / c["huella"]["n"] * 100) - tasa_b >= self.ventaja_min:
                return c, "HUELLA_VENTAJA", cands

        # La huella no decidio. Entonces manda el COSTO ESPERADO, no el flete pelado:
        # irse por el flete mas barato dentro de la banda puede salir mas caro cuando
        # la otra entrega mejor. (Caso Villamaria: $140 menos de flete y 2.426 mas de
        # costo real.) cands ya viene ordenado por costo.
        return cands[0], "PRECIO", cands

    def correr(self):
        ords = self.D.get("ordenes") or []
        acc = set(self.D.get("accionables") or [])
        if not acc:
            print("AVISO: el volcado no trae 'accionables'. Se decide sobre TODAS las órdenes "
                  "cuyo estado esté en 'estados_accionables' del config.", file=sys.stderr)
            est = set(self.cfg.get("estados_accionables", []))
            acc = {o["id"] for o in ords if o.get("status") in est}
        out = []
        for o in [x for x in ords if x["id"] in acc]:
            tel = tel10(o.get("phone"))
            h = (self.D.get("huellas") or {}).get(tel)
            elegida, criterio, cands = self.decidir(o, h)
            actual = o.get("carrier")
            # `decidir` llama a `candidatas`, que deja aqui el veredicto de recogida.
            oficina_modo = getattr(self, "modo_oficina", "direccion")
            oficina_razon = getattr(self, "razon_oficina", "")
            if not elegida:
                # B4: el motivo tiene que decir la causa REAL. Antes decia siempre
                # "ninguna operativa llega", y era falso: a {CLIENTA_C} si le
                # llegaba Envia por $16.612 con 84,63% sobre 423 envios. La causa era
                # que el pedido pedia oficina y solo una transportadora la ofrece.
                rec = "SIN COBERTURA"
                desc = getattr(self, "ultimas_descartadas", []) or []
                _, era_oficina = self.candidatas(o, h)
                if era_oficina and self.oficina_solo:
                    motivo = (f"pidio recoger en oficina y solo {self.oficina_solo} la ofrece, "
                              f"pero no hay tarifa suya para ese municipio")
                elif desc:
                    d0 = max(desc, key=lambda z: z["envios"])
                    motivo = (f"las que llegan no tienen muestra suficiente ahi "
                              f"(la mejor, {d0['t']}, con {d0['envios']} envios y "
                              f"{d0['cuota']}% del municipio)")
                else:
                    motivo = "no hay tarifa ni datos de entrega para ese municipio"
                if actual and actual not in self.OPER:
                    motivo += f"; ademas la bodega no despacha por {actual}"
            elif not actual:
                rec, motivo = "ASIGNAR", "no tiene transportadora asignada"
            # ------------------------------------------------------------------
            # QUIEN PIDE RECOGER EN PUNTO NO ENTRA AL CAMBIO POR COSTO. Dictado por FER
            # el 2026-08-11 sobre un caso medido: el balance recomendo pasar a Envia un
            # pedido de una clienta que habia quedado en recoger en un punto de
            # Interrapidisimo, donde Envia no tiene punto. **El ahorro de $5.632 no era
            # un ahorro: era una devolucion**, porque el sitio al que mandaron a la
            # clienta deja de existir en cuanto cambia la transportadora.
            #
            # El punto pertenece a la transportadora, no al pedido: por eso la
            # restriccion es PREVIA al balance y no un desempate dentro de el. Un
            # criterio economico no puede arbitrar contra un compromiso ya hecho con la
            # clienta — el motor no sabe que a ella ya le dijeron donde ir.
            #
            # Lo DUDOSO cae del mismo lado a proposito: equivocarse hacia «no cambio»
            # cuesta el ahorro; equivocarse hacia «cambio» cuesta el pedido entero.
            # Y el informe lo DICE, para que nadie lo revierta por comodidad viendo una
            # columna de ahorro sin explicar.
            # ------------------------------------------------------------------
            elif oficina_modo in ("punto", "dudoso") and actual in self.OPER:
                rec = "DEJAR"
                motivo = ("recoge en punto de " + str(actual) + ": no se cambia por costo, "
                          "el punto es de esa transportadora"
                          if oficina_modo == "punto" else
                          "la direccion habla de recoger y no se pudo saber si es un punto: "
                          "no se cambia por costo hasta confirmarlo con la clienta")
            elif elegida["t"] == actual:
                rec, motivo = "DEJAR", ""
            elif actual not in self.OPER:
                rec, motivo = "CAMBIAR", f"la bodega no despacha por {actual}"
                if oficina_modo in ("punto", "dudoso"):
                    # Aqui el cambio NO es por costo — es que no hay alternativa — pero
                    # el punto de recogida se pierde igual. Se cambia y se avisa.
                    motivo += ("; OJO: quedo en recoger en punto, hay que decirle a "
                               "donde va ahora")
            else:
                act = [c for c in cands if c["t"] == actual]
                ahorro = (act[0]["costo"] - elegida["costo"]) if act else None
                rec = "CAMBIAR"
                motivo = {"CLARO": "gana claro por costo",
                          "HUELLA_MALA": "al cliente le ha ido mal con la actual",
                          "HUELLA_VENTAJA": "al cliente le va mucho mejor con la nueva",
                          "PRECIO": "empate resuelto por precio"}[criterio]
                if ahorro is not None:
                    motivo += f", ahorra {pesos(ahorro)} de costo real"
            out.append({"id": o["id"], "status": o["status"], "tel": "57" + tel if tel else "",
                        "cliente": f"{o.get('name','')} {o.get('surname','')}".strip(),
                        "ciudad": o.get("city"), "depto": o.get("state"), "dir": o.get("dir"),
                        "total": float(o.get("total") or 0), "actual": actual, "guia": o.get("guide"),
                        "elegida": elegida, "criterio": criterio, "rec": rec, "motivo": motivo,
                        "cands": cands,
                        # El veredicto de recogida viaja con la decision: el informe lo
                        # imprime como razon, y sin el la columna «se deja» no se explica.
                        "oficina": oficina_modo, "oficina_razon": oficina_razon,
                        "cruce_oficina": getattr(self, "cruce_oficina", "no"),
                        # LA FECHA DEL LISTADO, o None si no habia listado. Sin esto
                        # el informe imprimia «0 direcciones resultaron ser la oficina»
                        # cuando la verdad era «no habia contra que comparar»: un cero
                        # que no dice de donde sale, que es la falta que esta skill
                        # lleva 30 rondas persiguiendo.
                        "oficinas_fecha": self.ofi_fecha,
                        "oficinas_total": self.ofi_total,
                        # De donde salio la utilidad que se uso para castigar el fallo.
                        "utilidad_fuente": getattr(self, "utilidad_fuente", None),
                        # CONTRA QUE TORRE SE DECIDIO. Viaja pegado a la decision, no en
                        # una cabecera aparte, porque la salida es una LISTA y meterle un
                        # sobre la rompe para el generador de acciones. Y viaja porque el
                        # factor de calibracion de Golden se movio 0,92 -> 1,00 en un dia
                        # sin que nadie tocara un pedido: solo cambio la ventana de la
                        # Torre. Quien lee el informe tiene derecho a saber contra que
                        # medicion se decidio, sobre todo cuando cambia sola.
                        "torre_generado": self.torre_generado,
                        "torre_rango": self.torre_rango,
                        "torre_nota": self.torre_nota,
                        "descartadas_por_muestra": getattr(self, "ultimas_descartadas", [])})
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    for k in ("dropi", "torre", "fletes", "retorno", "salida"):
        ap.add_argument("--" + k)
    ap.add_argument("--operativas")
    ap.add_argument("--factor", type=float)
    ap.add_argument("--margen", type=float)
    a = ap.parse_args()
    cfg = leer_json(a.config) if a.config else {}
    if a.config:
        avisar_banderas(cfg, a.config)   # el motor tambien avisa: callaba con claves inventadas
    for k in ("dropi", "torre", "fletes", "retorno"):
        if getattr(a, k):
            cfg[k] = getattr(a, k)
    if a.operativas:
        cfg["operativas"] = [x.strip() for x in a.operativas.split(",")]
    if a.factor is not None:
        cfg["factor_tienda"] = a.factor
    if a.margen is not None:
        cfg["margen"] = a.margen
    faltan = [k for k in ("dropi", "torre", "fletes", "retorno", "operativas") if not cfg.get(k)]
    if faltan:
        sys.exit(f"Faltan parámetros: {', '.join(faltan)}. Pásalos por --config o por bandera.")
    # COMPUERTA DE LOS DATOS DE FLETES. Esta skill NO calcula tarifas: las lee del
    # proyecto FLETES-DROPI-COLOMBIA, que es quien las cosecha del panel. Esa
    # dependencia era de facto — una ruta escrita en un config — asi que si esa
    # carpeta se movia o se renombraba, el motor moria con un traceback y nadie
    # sabia por que. Ahora muere diciendo QUE falta, DONDE vivia y QUIEN lo produce.
    QUE_ES = {
        "fletes": ("las TARIFAS por transportadora y municipio",
                   "el proyecto FLETES-DROPI-COLOMBIA (barrido del panel de Dropi)"),
        "torre": ("la EFECTIVIDAD de entrega por municipio",
                  "la Torre Logistica de Dropi, 90 dias, via FLETES-DROPI-COLOMBIA"),
        "retorno": ("cuanto cobra cada transportadora por DEVOLVER un pedido",
                    "las devoluciones reales medidas de la tienda"),
        "calibracion": ("el FACTOR de la tienda contra su municipio",
                        "el calculo de calibracion de esta misma tienda"),
        "dropi": ("el VOLCADO de ordenes del dia",
                  "scripts/cosecha-dropi.js de esta skill"),
    }
    for k in ("dropi", "torre", "fletes", "retorno", "calibracion"):
        if not cfg.get(k):
            continue
        if not os.path.exists(cfg[k]):
            que, quien = QUE_ES.get(k, ("un insumo", "no declarado"))
            sys.exit(
                f"FALTA UN INSUMO: no existe '{cfg[k]}'.\n"
                f"  Ahi viven {que}.\n"
                f"  Los produce {quien}.\n"
                "  Sin eso no se decide nada: el motor NO inventa tarifas ni efectividades. "
                "Si la carpeta se movio, corrige la ruta en el config; si nunca se cosecho, "
                "hay que cosecharla primero.")

    m = Motor(cfg)
    out = m.correr()
    destino = a.salida or cfg.get("salida") or "decisiones.json"
    escribir_json(destino, out, indent=1)
    import collections
    print("recomendación:", dict(collections.Counter(x["rec"] for x in out)))
    print("criterio:", dict(collections.Counter(x["criterio"] for x in out)))
    print(f"escrito: {destino}  ({len(out)} pedidos)")
    print(f"Torre: generada {m.torre_generado or 'sin fecha'} · rango {m.torre_rango or 'sin rango'}"
          f" · {m.torre_filas} filas")
    if m.torre_sin_dias:
        # No es un aviso decorativo: sin `dias` el informe deja de poder prometer tiempo
        # de entrega, y es mejor que lo diga la corrida que descubrirlo en el PDF.
        print(f"  AVISO: {m.torre_sin_dias} de {m.torre_filas} filas NO traen 'dias'. "
              "El informe no promete tiempo de entrega con esta Torre.", file=sys.stderr)


if __name__ == "__main__":
    main()
