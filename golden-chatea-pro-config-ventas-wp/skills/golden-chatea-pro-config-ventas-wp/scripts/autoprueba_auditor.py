#!/usr/bin/env python3
"""
autoprueba_auditor.py — Banco de pruebas de scripts/auditar_espacio.py, SIN tocar ningun espacio.

POR QUE EXISTE: un auditor que da 1000 a todo no audita. Este banco lo prueba en los DOS
sentidos: (1) un espacio limpio, construido por la propia skill para dos paises y tres modelos, debe dar
1000/1000 sin defectos (si no, el auditor acusa en falso); (2) dieciseis sabotajes, cada uno con el
hallazgo EXACTO que debe aparecer (si no aparece, el auditor esta ciego a esa clase de fallo).

Uso:  python3 autoprueba_auditor.py      # exit 0 si todo en verde
"""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
ASSETS = os.path.join(SKILL, "assets")
AUD = os.path.join(AQUI, "auditar_espacio.py")
BUILD = os.path.join(AQUI, "build_config.py")
CS = json.load(open(os.path.join(ASSETS, "campos-sueltos.json"), encoding="utf-8"))
TMP = tempfile.mkdtemp(prefix="autoprueba_aud_")


def construir(pais, extra, modelo="dropshipping"):
    """Espacio limpio: lo que la propia skill produciria, mas 2 productos validos."""
    pm = os.path.join(TMP, "pm.txt")
    open(pm, "w", encoding="utf-8").write("Prompt maestro de prueba para el banco.")
    pref = os.path.join(TMP, pais)
    cmd = [sys.executable, BUILD, "--pais", pais, "--url-tienda", "https://ejemplo.test",
           "--nombre-bot", "Ana", "--nombre-tienda", "Empresa Uno", "--modelo", modelo,
           "--whatsapp-notif", "573001112233", "--prompt-maestro", pm, "--out-prefix", pref] + extra
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ERROR armando la base de {pais}: {r.stdout[-300:]} {r.stderr[-300:]}")
    campos = []
    for suf, nom in (("_BOTFIELD_1.json", "[Ventas Wp] Configuracion general"),
                     ("_BOTFIELD_2.json", "[Ventas Wp] Configuracion general 2")):
        campos.append({"name": nom, "var_type": "longtext",
                       "value": open(pref + suf, encoding="utf-8").read()})
    for n, d in CS["booleanos"].items():
        if d.get("DERIVADO_DE") == "pais":
            v = "false" if pais == "mexico" else "true"
        elif d.get("DERIVADO_DE") == "modelo":
            con = modelo in ("dropshipping", "mixto")
            v = ("true" if con else "false") if "Con Recaudo" in n else ("false" if con else "true")
        else:
            v = d["valor"]
        campos.append({"name": n, "var_type": "boolean", "value": v})
    for n, d in CS["textos"].items():
        campos.append({"name": n, "var_type": "text", "value": d["valor"]})
    for n, d in CS["interruptores_operativos_whatsapp_ia"].items():
        if not n.startswith("_"):
            campos.append({"name": n, "var_type": "boolean", "value": d["valor_por_defecto"]})
    plant = open(os.path.join(ASSETS, "template-botfield-producto.json"), encoding="utf-8").read()
    reg = []
    for i, (nom, clave) in enumerate((("Producto Uno", "CLAVEUNO"), ("Producto Dos", "CLAVEDOS")), 1):
        sust = {"ID_DROPI": "12345", "NOMBRE_PRODUCTO": nom, "PRECIO_SOLO_DIGITOS": "50000", "MONEDA": "COP",
                "SIMPLE_O_VARIABLE": "SIMPLE", "URL_IMAGEN_PORTADA": "https://ejemplo.test/a.jpg",
                "MENSAJE_INICIAL": "Hola, te cuento del producto", "URL_VIDEO_O_IMAGEN_1": "https://ejemplo.test/v.mp4",
                "URL_IMAGEN_2": "https://ejemplo.test/b.jpg", "PREGUNTA_ENTRADA": "Cual te interesa",
                "PROMPT_VENTA": f"Vendes {nom} a $50.000 con envio incluido y pago al recibir",
                "ID_VOZ_O_VACIO": "", "API_KEY_ELEVENLABS_O_VACIO": "", "VOZ_SI_NO": "no",
                "RECORDATORIO_1": "EVENTO: el usuario no respondio. MINIMO 35 palabras. Pregunta si sigue interesado.",
                "RECORDATORIO_2": "EVENTO: sigue sin responder. MINIMO 35 palabras. Ultimo aviso amable.",
                "PROMPT_REMARKETING_1": "Reactiva con suavidad", "PROMPT_REMARKETING_2": "Ultimo llamado con urgencia",
                "PLANTILLA_1_O_NO_ENVIAR": "no enviar plantilla", "PLANTILLA_2_O_NO_ENVIAR": "no enviar plantilla",
                "PALABRA_CLAVE": clave, "IDS_ANUNCIO_O_VACIO": "", "N": str(i)}
        t = plant
        for k, v in sust.items():
            t = t.replace("{{" + k + "}}", v)
        j = json.loads(t)
        for k in [k for k in j if k.startswith("_")]:
            del j[k]
        val = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
        campos.append({"name": f"[Producto Ventas Wp] {i}", "var_type": "longtext", "value": val})
        reg.append({"name": f"[Producto Ventas Wp] {i}", "keyW": f"{clave},,,,,,", "idAd": ",,,,,,",
                    "estado": "activo", "producto": nom})
    campos.append({"name": "[Ventas Wp] Disparador de productos Extendido", "var_type": "longtext",
                   "value": json.dumps(reg, ensure_ascii=False)})
    return campos


def por(c, nombre):
    return next(x for x in c if x["name"] == nombre)


def cambiar_json(c, nombre, fn):
    x = por(c, nombre)
    j = json.loads(x["value"])
    fn(j)
    x["value"] = json.dumps(j, ensure_ascii=False, separators=(",", ":"))


def auditar(campos):
    f = os.path.join(TMP, "volcado.json")
    json.dump(campos, open(f, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run([sys.executable, AUD, "--volcado", f], capture_output=True, text=True)
    m = re.search(r"NOTA: (\d+)/1000", r.stdout)
    return (int(m.group(1)) if m else -1), r.returncode, r.stdout + r.stderr


N1, N2 = "[Ventas Wp] Configuracion general", "[Ventas Wp] Configuracion general 2"
REG = "[Ventas Wp] Disparador de productos Extendido"
hechas, fallos = [], []


def check(nombre, cond, detalle=""):
    hechas.append(nombre)
    print(("  OK   " if cond else "  FALLA") + f" · {nombre}" + (f" :: {detalle}" if not cond else ""))
    if not cond:
        fallos.append(nombre)


def sabotaje(nombre, base, mutar, esperado, defecto=True):
    c = copy.deepcopy(base)
    mutar(c)
    nota, rc, out = auditar(c)
    check(f"sabotaje: {nombre}", esperado in out and nota < 1000 and (rc == 1) == defecto,
          f"nota={nota} rc={rc} esperaba {esperado!r}")


print("BANCO del auditor (sin tocar ningun espacio)")
co = construir("colombia", [])
mx = construir("mexico", ["--flete-max", "300"])
mixto = construir("colombia", [], "mixto")
marca = construir("colombia", [], "marca")
for nom, base in (("colombia", co), ("mexico", mx), ("colombia con modelo MIXTO", mixto),
                  ("colombia con modelo MARCA PROPIA", marca)):
    nota, rc, out = auditar(base)
    check(f"base limpia de {nom}: 1000/1000 y sin defectos", nota == 1000 and rc == 0, f"nota={nota} rc={rc}\n{out[-500:]}")

sabotaje("un producto ACTIVO sin entrada en el Disparador (decision del dueño, no defecto)", co,
         lambda c: por(c, REG).update(value=json.dumps(json.loads(por(c, REG)["value"])[:1])),
         "no tiene entrada en el", defecto=False)
sabotaje("vocabulario de COLOMBIA colado en un espacio de MEXICO", mx,
         lambda c: cambiar_json(c, N2, lambda j: j["comportamiento_ia"].update(
             rol=j["comportamiento_ia"]["rol"].replace("colonia", "barrio").replace("estado", "departamento"))),
         "propio de COLOMBIA")
# Generalizacion (hallazgo golden-skill-auditor 2026-09-22): el detector viejo SOLO conocia
# Colombia; una fuga de vocabulario MEXICANO en un espacio de otro pais pasaba muda. Prueba
# cruzada real: ARGENTINA (campos_memoria "calle, altura, localidad, CP", sin 'colonia' ni
# 'estado') recibe el rol de MEXICO tal cual, con sus dos terminos propios.
ar = construir("argentina", ["--flete-max", "23000"])
sabotaje("vocabulario de MEXICO colado en un espacio de ARGENTINA (generalizacion, no solo Colombia)",
         ar, lambda c: cambiar_json(c, N2, lambda j: j["comportamiento_ia"].update(
             rol="Vive en la colonia y su estado es X. " + j["comportamiento_ia"]["rol"])),
         "propio de MEXICO")
sabotaje("rol por encima del tope de 2000", co,
         lambda c: cambiar_json(c, N2, lambda j: j["comportamiento_ia"].update(rol=j["comportamiento_ia"]["rol"] + "x" * 300)),
         "> 2000")
sabotaje("campo 2 con JSON cortado", co,
         lambda c: por(c, N2).update(value=por(c, N2)["value"][:-40]), "NO es JSON valido")
sabotaje("moneda que no corresponde al pais", mx,
         lambda c: cambiar_json(c, N1, lambda j: j["acciones_especiales"]["validaciones_orden"]["validar_flete"].update(moneda="COP")),
         "no corresponde a MEXICO")
sabotaje("hueco {{IDENTIDAD}} sin llenar", co,
         lambda c: cambiar_json(c, N2, lambda j: j["comportamiento_ia"].update(
             rol="{{IDENTIDAD}} " + j["comportamiento_ia"]["rol"])), "hueco de plantilla")
sabotaje("hueco (Producto 1) entre parentesis en el analisis", co,
         lambda c: cambiar_json(c, N2, lambda j: j["comportamiento_ia"]["analizar_palabra"].update(
             prompt=j["comportamiento_ia"]["analizar_palabra"]["prompt"] + "\n(Producto 1)")), "hueco entre parentesis")
sabotaje("falta un interruptor suelto", co,
         lambda c: c.remove(por(c, "[Ventas Wp] Respuesta Múltiple")), "no existe el interruptor")
sabotaje("D1 roto: misma palabra en OTRO slot del registro", co,
         lambda c: por(c, REG).update(value=por(c, REG)["value"].replace("CLAVEUNO,,,,,,", ",CLAVEUNO,,,,,")),
         "no pasa el validador")
sabotaje("Oficina en true en un espacio de MEXICO", mx,
         lambda c: por(c, "[Ventas Wp] Oficina 📦").update(value="true"), "Oficina esta en true")
sabotaje("Solo Con Recaudo y Solo Sin Recaudo iguales", co,
         lambda c: por(c, "[Ventas Wp] Solo Sin Recaudo").update(value="true"), "IGUALES")
sabotaje("notificacion activa sin numero", co,
         lambda c: cambiar_json(c, N1, lambda j: j["notificaciones"]["notificacion_1"].update(whatsapp="")),
         "SIN numero")
sabotaje("el Disparador apunta a un campo que no existe", co,
         lambda c: por(c, REG).update(value=json.dumps(json.loads(por(c, REG)["value"]) + [
             {"name": "[Producto Ventas Wp] 99", "keyW": "FANTASMA,,,,,,", "idAd": ",,,,,,", "estado": "activo",
              "producto": "Fantasma"}])), "no existe: [Producto Ventas Wp] 99")
sabotaje("palabra clave duplicada en el Disparador", co,
         lambda c: por(c, REG).update(value=json.dumps([
             dict(e, keyW="CLAVEUNO,,,,,,") for e in json.loads(por(c, REG)["value"])])), "DUPLICADA")
sabotaje("signo de apertura en remarketing.prompt_1 (hallazgo golden-skill-auditor 2026-09-22: "
         "check_apertura no cubria remarketing ni upsells)", co,
         lambda c: cambiar_json(c, "[Producto Ventas Wp] 1", lambda j: j["remarketing"].update(
             prompt_1="¿Sigues interesado? " + j["remarketing"]["prompt_1"])),
         "no pasa el validador")

# ---- FLETE (estandar de FER 2026-09-19): promedio nativo + corte del cliente ----
def build_flete(pais, extra, pref):
    pm = os.path.join(TMP, "pm.txt")
    cmd = [sys.executable, BUILD, "--pais", pais, "--url-tienda", "https://ejemplo.test", "--nombre-bot", "Ana",
           "--nombre-tienda", "Empresa Uno", "--modelo", "dropshipping", "--whatsapp-notif", "573001112233",
           "--prompt-maestro", pm, "--out-prefix", os.path.join(TMP, pref)] + extra
    r = subprocess.run(cmd, capture_output=True, text=True)
    f = None
    if r.returncode == 0:
        j = json.load(open(os.path.join(TMP, pref + "_BOTFIELD_1.json"), encoding="utf-8"))
        f = j["acciones_especiales"]["validaciones_orden"]["validar_flete"]["flete_minimo"]
    return r.returncode, f, r.stdout + r.stderr


rc, f, _o = build_flete("colombia", [], "f1")
check("flete: sin corte del cliente se usa el promedio nativo del pais", rc == 0 and f == "25000", f"rc={rc} f={f}")
rc, f, _o = build_flete("colombia", ["--flete-max", "18000"], "f2")
check("flete: el corte del cliente MANDA sobre el nativo", rc == 0 and f == "18000", f"rc={rc} f={f}")
rc, f, _o = build_flete("colombia", ["--flete-max", "$18.000"], "f3")
check("flete: el corte se normaliza ('$18.000' -> 18000)", rc == 0 and f == "18000", f"rc={rc} f={f}")
rc, f, o = build_flete("peru", [], "f4")
check("flete: pais SIN promedio y sin corte se detiene y pide el dato (no copia el de otro pais)",
      rc != 0 and "Centro de Mando" in o and f is None, f"rc={rc}")
rc, f, o = build_flete("colombia", ["--flete-max", "abc"], "f5")
check("flete: un corte no numerico da error legible y no escribe", rc != 0 and "no es un valor valido" in o, f"rc={rc}")
if True:
    c18 = construir("colombia", ["--flete-max", "18000"])
    nota, rc2, out2 = auditar(c18)
    check("auditor: un corte del cliente distinto del nativo se acepta (1000) y se anota como aviso",
          nota == 1000 and rc2 == 0 and "corte que dijo el cliente" in out2, f"nota={nota} rc={rc2}")

total = len(hechas)
print(f"\nCOBERTURA: {total - len(fallos)} de {total} pruebas en verde")
if fallos:
    print("FALLAN: " + ", ".join(fallos))
    sys.exit(1)
print("Banco en verde: el auditor da 1000 a lo limpio y muerde cada clase de fallo probada.")
sys.exit(0)
