#!/usr/bin/env python3
"""
auditar_espacio.py — Audita, en SOLO LECTURA, la configuracion de Ventas WhatsApp de un espacio
de Chatea Pro contra lo que ESTA skill produciria para el pais y el modelo de ese espacio, y da
una nota medida sobre 1000. No escribe nada en el espacio.

POR QUE EXISTE: "revisa mi espacio y calificalo" se hacia a ojo y cada vez daba un numero
distinto. Esto lo vuelve REPETIBLE: mismas comprobaciones, mismos pesos, y cada punto que se
resta se imprime con su motivo.

Uso:
    python3 auditar_espacio.py --token-file RUTA          # lee el espacio por API
    python3 auditar_espacio.py --token TOKEN              # idem
    python3 auditar_espacio.py --volcado archivo.json     # offline, desde un volcado de bot fields
    ... --guardar-volcado RUTA                            # ademas guarda el estado leido (chmod 600)

Exit 0 si no hay DEFECTOS; exit 1 si los hay. Las DECISIONES (algo que puede ser eleccion del
negocio) y los AVISOS no hacen fallar: se reportan para que Golden decida.

Tres severidades:
  DEFECTO   algo roto o contradictorio: se arregla.
  DECISION  puede ser una eleccion legitima del negocio: la resuelve Golden, NO se escribe por su cuenta.
  AVISO     informativo.

LIMITE DECLARADO: esto valida los JSON contra el estandar; NO sustituye una conversacion de
prueba real por WhatsApp (el runtime del bot no se ejerce aqui).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
ASSETS = os.path.join(SKILL, "assets")
LIM = json.load(open(os.path.join(ASSETS, "limites.json"), encoding="utf-8"))


def _sin_acentos(t):
    s = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# Palabras del español corriente que SALEN textualmente unicas de un solo pais en su
# campos_memoria (por el fraseo del pack, no por ser jerga administrativa) y que por eso
# disparan falsos positivos fuera de contexto de direccion. Medido (golden-skill-auditor,
# 2026-09-22): 'tipo' viene de 'tipo de via' en el pack de Guatemala, y aparecia tambien en
# 'TIPO Y NOMBRE / tipo de producto' de reglas-estructura-producto.txt -- un DEFECTO falso
# sobre la base LIMPIA de Mexico. Cada entrada aqui se explica por que es generica, no jerga:
GENERICOS = {
    "tipo", "zona", "metros", "rumbo", "principal", "secundaria", "sector", "color",
    "piso", "apto",
}


def _terminos_propios_por_pais():
    """Para cada pais del mapa de vocabulario, los terminos de su `campos_memoria` que NO
    aparecen en el `campos_memoria` de NINGUN otro pais Y que no son espanol generico
    (GENERICOS) -- la fuga que un texto de OTRO pais puede colar sin que nadie lo note.
    Generalizado a los 23 paises del mapa (hallazgo golden-skill-auditor 2026-09-22: antes
    solo se miraban 'departamento' y 'barrio', hardcodeados para Colombia, y 'barrio' ni
    siquiera es unico de Colombia -- lo comparte Paraguay -- asi que quedaba fuera de este
    calculo por construccion, no por eleccion)."""
    voc = LIM.get("vocabulario_direccion_por_pais", {})
    por_termino = {}
    for pais, v in voc.items():
        if pais.startswith("_"):
            continue
        for t in re.findall(r"[A-Za-zÀ-ÿ]{4,}", v.get("campos_memoria", "")):
            tn = _sin_acentos(t)
            if tn in GENERICOS:
                continue
            por_termino.setdefault(tn, set()).add(pais)
    propios = {}
    for termino, paises_con in por_termino.items():
        if len(paises_con) == 1:
            (unico,) = paises_con
            propios.setdefault(unico, set()).add(termino)
    return propios


TERMINOS_PROPIOS_POR_PAIS = _terminos_propios_por_pais()
NAT = LIM["capa_nativa"]
PESOS = {"estructura": 150, "prompts": 300, "operativa": 150, "interruptores": 100, "productos": 300}

N1 = "[Ventas Wp] Configuracion general"
N2 = "[Ventas Wp] Configuracion general 2"
NREG = "[Ventas Wp] Disparador de productos Extendido"
PREF_PROD = "[Producto Ventas Wp]"

hallazgos = []   # (severidad, categoria, mensaje, puntos)


def h(sev, cat, msg, pts=0):
    hallazgos.append((sev, cat, msg, pts))


def u16(t):
    return len((t or "").encode("utf-16-le")) // 2


def escapado(v):
    return len(json.dumps(v, ensure_ascii=True)[1:-1])


def hojas(o, p=""):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(hojas(v, f"{p}.{k}" if p else k))
        return r
    return {p: o}


def sin_meta(o):
    if isinstance(o, dict):
        return {k: sin_meta(v) for k, v in o.items() if not k.startswith("_")}
    return o


def leer_espacio(a):
    if a.volcado:
        return json.load(open(a.volcado, encoding="utf-8"))
    tok = a.token or open(a.token_file).read().strip()
    hd = {"Authorization": f"Bearer {tok}", "User-Agent": "curl/8.7.1", "Accept": "application/json"}
    todos = []
    for pg in range(1, 60):
        rq = urllib.request.Request(f"https://chateapro.app/api/flow/bot-fields?page={pg}", headers=hd)
        it = json.load(urllib.request.urlopen(rq, timeout=30)).get("data") or []
        if not it:
            break
        todos += it
    if a.guardar_volcado:
        json.dump(todos, open(a.guardar_volcado, "w", encoding="utf-8"), ensure_ascii=False)
        os.chmod(a.guardar_volcado, 0o600)
    return todos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token")
    ap.add_argument("--token-file", dest="token_file")
    ap.add_argument("--volcado")
    ap.add_argument("--guardar-volcado", dest="guardar_volcado")
    a = ap.parse_args()
    if not (a.token or a.token_file or a.volcado):
        sys.exit("ERROR: pasa --token, --token-file o --volcado.")

    todos = leer_espacio(a)
    por = {x["name"]: x for x in todos}
    print(f"ESPACIO: {len(todos)} bot fields leidos (solo lectura, no se escribio nada)\n")

    # ------------------------------------------------------------------ ESTRUCTURA
    c1 = c2 = None
    for nombre, clave in ((N1, "c1"), (N2, "c2")):
        if nombre not in por:
            h("DEFECTO", "estructura", f"no existe el campo '{nombre}'", 150)
            continue
        try:
            j = json.loads(por[nombre]["value"])
        except Exception as e:
            h("DEFECTO", "estructura", f"'{nombre}' NO es JSON valido ({e}): el panel lo muestra en blanco", 150)
            continue
        if clave == "c1":
            c1 = j
        else:
            c2 = j
    plant = {"c1": "template-botfield-1-configuracion.json", "c2": "template-botfield-2-comportamiento.json"}
    for clave, j in (("c1", c1), ("c2", c2)):
        if j is None:
            continue
        esp = set(hojas(sin_meta(json.load(open(os.path.join(ASSETS, plant[clave]), encoding="utf-8")))))
        viv = set(hojas(j))
        for k in sorted(esp - viv):
            h("DEFECTO", "estructura", f"falta la llave {k} en {'general' if clave == 'c1' else 'general 2'}", 10)
        for k in sorted(viv - esp):
            h("AVISO", "estructura", f"llave que la skill no conoce: {k}")

    pais = ""
    if c1:
        pais = str(c1.get("conexion_con_dropi", {}).get("pais", "")).strip().upper()
    con_rec = str(por.get("[Ventas Wp] Solo Con Recaudo", {}).get("value", "")).lower() == "true"

    # ------------------------------------------------------------------ PROMPTS
    if c1 and c2:
        rol = c2.get("comportamiento_ia", {}).get("rol", "") or ""
        res = c2.get("comportamiento_ia", {}).get("restricciones", "") or ""
        ana = c2.get("comportamiento_ia", {}).get("analizar_palabra", {}).get("prompt", "") or ""
        dat = c1.get("producto_segundos", {}).get("prompt_datos", "") or ""
        msg = c1.get("notificaciones", {}).get("notificacion_1", {}).get("mensaje", "") or ""
        textos = [("rol", rol, NAT["rol_general"]), ("restricciones", res, NAT["restricciones_generales"]),
                  ("analisis de palabra clave", ana, NAT["prompt_analisis"]),
                  ("prompt_datos (Producto en Segundos)", dat, NAT["reglas_estructura"]),
                  ("mensaje de notificacion", msg, NAT["mensaje_libre"])]
        for nom, t, tope in textos:
            if not t.strip():
                h("DEFECTO", "prompts", f"{nom} esta VACIO", 60)
                continue
            n = u16(t)
            if n > tope:
                h("DEFECTO", "prompts", f"{nom}: {n} > {tope} (UTF-16): el panel lo corta al guardar", 60)
            if "{{" in t:
                h("DEFECTO", "prompts", f"{nom}: quedo un hueco de plantilla {{{{...}}}} sin llenar", 60)
        if re.search(r"\((?:[Pp]roducto|[Nn]ombre)[^)]{0,12}\)", ana):
            h("DEFECTO", "prompts", "analisis de palabra clave: hueco entre parentesis tipo (Producto 1): "
              "el bot puede mandarselo tal cual al cliente", 60)
        for nom, t in (("rol", rol), ("restricciones", res), ("analisis de palabra clave", ana)):
            if re.search(r"[¿¡]", t):
                h("DEFECTO", "prompts", f"{nom}: lleva signos de apertura y el propio prompt manda no usarlos", 20)
        if pais:
            # Fuga de vocabulario de CUALQUIER otro pais del mapa (23 hoy), no solo Colombia.
            # 'continue' salta el propio pais (no es fuga verse a si mismo); 'break' SOLO
            # cuando ya se encontro algo -- un bug medido (golden-skill-auditor 2026-09-22):
            # usar el mismo 'break' para las dos cosas cortaba el bucle ENTERO en el primer
            # pais que alfabeticamente coincidiera con el propio, y como ARGENTINA es la
            # primera letra del roster, un espacio de Argentina NUNCA llegaba a compararse
            # contra ningun otro pais.
            encontrada = False
            for otro_pais, terminos in sorted(TERMINOS_PROPIOS_POR_PAIS.items()):
                if otro_pais == pais:
                    continue
                for nom, t in (("rol", rol), ("restricciones", res), ("prompt_datos", dat)):
                    bajo = _sin_acentos(t)
                    coladas = sorted(w for w in terminos if re.search(rf"\b{w}\b", bajo))
                    if coladas:
                        h("DEFECTO", "prompts", f"{nom} de un espacio de {pais} trae vocabulario "
                          f"propio de {otro_pais}: {', '.join(coladas)}", 80)
                        encontrada = True
                        break
                if encontrada:
                    break
        voc = LIM.get("vocabulario_direccion_por_pais", {}).get(pais)
        if voc and rol:
            faltan = [t.strip() for t in voc["campos_memoria"].split(",") if t.strip().lower() not in rol.lower()]
            if faltan:
                h("DEFECTO", "prompts", f"el rol no nombra los datos de direccion de {pais}: falta {', '.join(faltan)}", 40)
            if voc["aclaracion"] not in res:
                h("AVISO", "prompts", f"las restricciones no traen la aclaracion de direccion de {pais}", 10)
        elif pais and not voc:
            h("AVISO", "prompts", f"{pais} no tiene vocabulario de direccion en limites.json: se reviso solo lo generico")
        if rol and not rol.startswith("Te llamas "):
            h("AVISO", "prompts", "el rol no abre con la identidad ('Te llamas <bot>, asesora de <empresa>')", 10)
        if ana and "https://" not in ana and "http://" not in ana:
            h("AVISO", "prompts", "el analisis de palabra clave no trae la URL a la que redirige lo no configurado", 10)

        # -------------------------------------------------------------- OPERATIVA
        d = c1.get("conexion_con_dropi", {})
        if str(d.get("conectar", "")).lower() != "si":
            h("AVISO", "operativa", "Dropi no esta conectado (conectar != si)", 10)
        if pais and pais not in [p.upper() for p in LIM["paises_validos"]]:
            h("AVISO", "operativa", f"pais '{pais}' fuera de la lista que la plataforma ha confirmado", 10)
        vo = c1.get("acciones_especiales", {}).get("validaciones_orden", {})
        vf = vo.get("validar_flete", {})
        moneda_esp = LIM.get("moneda_por_pais", {}).get(pais)
        if moneda_esp and str(vf.get("moneda", "")).upper() != moneda_esp:
            h("DEFECTO", "operativa", f"moneda {vf.get('moneda')!r} no corresponde a {pais} (esperada {moneda_esp})", 50)
        if str(vf.get("esta_activo", "")).lower() == "si":
            if not str(vf.get("flete_minimo", "")).strip().isdigit() or int(vf.get("flete_minimo")) <= 0:
                h("DEFECTO", "operativa", "validar_flete activo con flete_minimo vacio o cero", 30)
            else:
                nat = LIM.get("flete_max_por_pais", {}).get(pais)
                if nat and int(vf["flete_minimo"]) != int(nat):
                    h("AVISO", "operativa", f"flete_minimo {vf['flete_minimo']} distinto del promedio nativo de "
                      f"{pais} ({nat}): debe ser el corte que dijo el cliente (dato 7)")
        ve = vo.get("validar_entregas", {})
        if str(ve.get("esta_activo", "")).lower() == "si":
            pm, mo = str(ve.get("porcentaje_minimo", "")), str(ve.get("minimo_de_ordenes", ""))
            if not (pm.isdigit() and 1 <= int(pm) <= 100 and mo.isdigit() and int(mo) >= 1):
                h("DEFECTO", "operativa", "validar_entregas activo con porcentaje u ordenes minimas invalidos", 30)
        dv = c2.get("comportamiento_ia", {}).get("division", {})
        if dv.get("cantidad") == "varios" and str(dv.get("limite")) != "2":
            h("AVISO", "operativa", f"division en 'varios' con limite {dv.get('limite')}: el estandar es 2 "
              "(con 3 la IA responde en rafagas)", 10)
        if not c2.get("comportamiento_ia", {}).get("analizar_palabra", {}).get("activar"):
            h("AVISO", "operativa", "analisis de palabra clave apagado: los productos solo arrancan por clave exacta", 10)
        n1 = c1.get("notificaciones", {}).get("notificacion_1", {})
        tel = str(n1.get("whatsapp", "")).strip()
        if str(n1.get("activa", "")).lower() == "si":
            if not tel:
                h("DEFECTO", "operativa", "notificacion activa SIN numero de WhatsApp: no llega a nadie", 30)
            elif not re.match(r"^\+?\d{8,15}$", tel):
                h("DEFECTO", "operativa", f"numero de notificacion con formato invalido: {tel!r}", 20)
        else:
            h("AVISO", "operativa", "la notificacion de venta esta apagada", 10)

    # ------------------------------------------------------------------ INTERRUPTORES
    cs = json.load(open(os.path.join(ASSETS, "campos-sueltos.json"), encoding="utf-8"))
    esperado = {}
    for n, dd in cs["booleanos"].items():
        if dd.get("DERIVADO_DE") == "pais":
            esperado[n] = "false" if pais == "MEXICO" else "true"
        elif dd.get("DERIVADO_DE") == "modelo":
            esperado[n] = ("true" if con_rec else "false") if "Con Recaudo" in n else ("false" if con_rec else "true")
        else:
            esperado[n] = dd["valor"]
    for n, dd in cs["interruptores_operativos_whatsapp_ia"].items():
        if not n.startswith("_"):
            esperado[n] = dd["valor_por_defecto"]
    for n in cs["textos"]:
        if n not in por:
            h("DEFECTO", "interruptores", f"no existe el campo de texto '{n}'", 8)
    difs = 0
    for n, v in esperado.items():
        if n not in por:
            h("DEFECTO", "interruptores", f"no existe el interruptor '{n}'", 8)
            continue
        vivo = str(por[n].get("value", "")).lower()
        if vivo != v:
            if n.endswith("Oficina 📦") and pais == "MEXICO":
                h("DEFECTO", "interruptores", "Oficina esta en true en un espacio de MEXICO: alli no existe "
                  "recogida en oficina", 30)
            else:
                difs += 1
                h("DECISION", "interruptores", f"{n}: vivo={vivo} · estandar de la skill={v} "
                  "(puede ser una eleccion del negocio)", 3 if difs <= 10 else 0)
    if str(por.get("[Ventas Wp] Solo Con Recaudo", {}).get("value", "")).lower() == \
            str(por.get("[Ventas Wp] Solo Sin Recaudo", {}).get("value", "")).lower() != "":
        h("DEFECTO", "interruptores", "'Solo Con Recaudo' y 'Solo Sin Recaudo' estan IGUALES: son espejo", 30)

    # ------------------------------------------------------------------ PRODUCTOS + REGISTRO
    prods = sorted([x for x in todos if x["name"].startswith(PREF_PROD)],
                   key=lambda z: int(re.sub(r"\D", "", z["name"].split()[-1]) or 0))
    reg = None
    if prods:
        if NREG not in por:
            h("DEFECTO", "productos", "hay productos pero NO existe el Disparador de productos Extendido", 150)
        else:
            try:
                reg = json.loads(por[NREG]["value"])
                if not isinstance(reg, list):
                    raise ValueError("no es un array")
            except Exception as e:
                h("DEFECTO", "productos", f"el Disparador Extendido no es un array JSON valido ({e})", 150)
    else:
        h("AVISO", "productos", "el espacio no tiene productos cargados: esta categoria no es evaluable")
    if prods and reg is not None:
        nombres_reg = [e.get("name") for e in reg if isinstance(e, dict)]
        for nm in sorted({n for n in nombres_reg if n not in por}):
            h("DEFECTO", "productos", f"el Disparador apunta a un campo que no existe: {nm}", 30)
        claves = [e.get("keyW") for e in reg if isinstance(e, dict)]
        for k in sorted({k for k in claves if k and claves.count(k) > 1}):
            h("DEFECTO", "productos", f"palabra clave DUPLICADA en el Disparador: {k[:60]!r}", 40)
        tmp = tempfile.mkdtemp(prefix="auditoria_")
        try:
            rp = os.path.join(tmp, "registro.json")
            n = len(prods)
            avisos_v = {}
            for x in prods:
                fp = os.path.join(tmp, "p.json")
                open(fp, "w", encoding="utf-8").write(x["value"])
                try:
                    estado = json.loads(x["value"]).get("informacion_de_producto", {}).get("estado", "")
                except Exception:
                    estado = ""
                # El vinculo real producto<->registro es el NOMBRE DEL CAMPO que lleva cada entrada.
                # Se empareja por ahi y se le da al validador SOLO esa entrada: con un registro de
                # una sola entrada el validador la asume del producto y daria un D1 falso.
                mia = [e for e in reg if isinstance(e, dict) and e.get("name") == x["name"]]
                if not mia:
                    if str(estado).lower() == "activo":
                        h("DECISION", "productos", f"{x['name']} esta ACTIVO pero no tiene entrada en el "
                          "Disparador Extendido: no arranca por su palabra clave", min(100 / n, 25))
                    pr = subprocess.run([sys.executable, os.path.join(AQUI, "valida_producto.py"), "--in", fp],
                                        capture_output=True, text=True)
                else:
                    json.dump([mia[0]], open(rp, "w", encoding="utf-8"), ensure_ascii=False)
                    pr = subprocess.run([sys.executable, os.path.join(AQUI, "valida_producto.py"), "--in", fp,
                                         "--registro", rp], capture_output=True, text=True)
                out = pr.stdout + pr.stderr
                if pr.returncode != 0:
                    motivos = [l.strip() for l in out.splitlines() if "ERROR" in l or l.strip().startswith("❌")]
                    h("DEFECTO", "productos", f"{x['name']} no pasa el validador: {' | '.join(motivos)[:200]}", 150 / n)
                for l in out.splitlines():
                    if l.strip().startswith("- ") and "NO se verifico D1" not in l \
                            and "El bot field escapado tiene" not in l:
                        avisos_v.setdefault(l.strip()[2:], []).append(x["name"].split()[-1])
                tope = LIM["bot_field"]["longtext_escapado"] if x.get("var_type") == "longtext" \
                    else LIM["bot_field"]["legacy_json_escapado"]
                e = escapado(x["value"])
                if e > tope:
                    h("DEFECTO", "productos", f"{x['name']}: {e} escapados > {tope} del tipo {x.get('var_type')}: "
                      "se guarda CORTADO", 40)
                elif e > tope * 0.95:
                    h("AVISO", "productos", f"{x['name']}: {e} de {tope} escapados: cualquier edicion lo puede pasar")
            for msg, quien in avisos_v.items():
                corto = re.sub(r"\(visto: '[^']{0,60}[^']*'\)", "(ver el campo)", msg)
                h("AVISO", "productos", f"{corto[:200]} (productos: {', '.join(quien)})")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ------------------------------------------------------------------ REPORTE
    pen = {c: 0.0 for c in PESOS}
    for sev, cat, msg, pts in hallazgos:
        pen[cat] += pts
    total = 0
    print("NOTA POR CATEGORIA:")
    for c, peso in PESOS.items():
        v = max(0, round(peso - min(pen[c], peso)))
        total += v
        print(f"  {c:14} {v:4} / {peso}")
    plural = {"DEFECTO": "DEFECTOS", "DECISION": "DECISIONES (las resuelve Golden, no se escriben solas)", "AVISO": "AVISOS"}
    for sev in ("DEFECTO", "DECISION", "AVISO"):
        lista = [x for x in hallazgos if x[0] == sev]
        if lista:
            print(f"\n{plural[sev]} ({len(lista)}):")
            for _, cat, msg, pts in lista:
                print(f"  [{cat}] {msg}" + (f"   (-{pts:.0f})" if pts else ""))
    print(f"\nNOTA: {total}/1000")
    ndef = sum(1 for x in hallazgos if x[0] == "DEFECTO")
    print(f"DEFECTOS: {ndef} · DECISIONES pendientes de Golden: "
          f"{sum(1 for x in hallazgos if x[0] == 'DECISION')} · AVISOS: {sum(1 for x in hallazgos if x[0] == 'AVISO')}")
    print("LIMITE: valida los JSON contra el estandar; no ejerce el runtime real del bot en WhatsApp.")
    sys.exit(1 if ndef else 0)


if __name__ == "__main__":
    main()
