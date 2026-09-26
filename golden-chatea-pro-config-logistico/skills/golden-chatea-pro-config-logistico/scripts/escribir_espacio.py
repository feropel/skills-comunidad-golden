#!/usr/bin/env python3
"""Escribe la configuracion del asistente LOGISTICO de Chatea Pro en un espacio, por API.

Nunca sube un archivo entero: lee lo VIVO, calcula que llaves difieren de la propuesta, parchea
solo esas sobre lo vivo, mide topes, escribe, relee del servidor y compara el JSON parseado.

Uso:
  escribir_espacio.py leer     --token-file T --nombre-esperado "Empresa" --backup-dir D
  escribir_espacio.py diff     --token-file T --nombre-esperado "Empresa" --prop-dir P
  escribir_espacio.py escribir --token-file T --nombre-esperado "Empresa" --prop-dir P --backup-dir D
  escribir_espacio.py --autoprueba        (sin red: servidor falso, casos buenos y malos)

--prop-dir lleva un JSON por campo: configuracion_general.json, confirmaciones.json,
seguimiento.json, novedad.json (los que falten no se tocan).
--nombre-esperado es datos_de_la_tienda.nombre del espacio: si no coincide, NO escribe
(un token de otro espacio es el error mas caro posible).
Salida: 0 ok · 1 fallo de verificacion o tope · 2 aborto por estructura, nombre o argumentos.
"""
import json, os, sys, time, datetime, urllib.request

BASE = "https://chateapro.app/api"
UA = "Mozilla/5.0 golden-logistico"
CAMPOS = {
    "[Logistico] Configuracion General": "configuracion_general",
    "[Logistico] Confirmaciones": "confirmaciones",
    "[Logistico] Seguimiento": "seguimiento",
    "[Logistico] Novedad": "novedad",
}
# Topes MEDIDOS del contador del panel (08-sep y 18-sep). Llave sin tope medido: no se inventa.
TOPES = {
    "nombre": 250, "enlace": 250, "id_de_la_voz": 250, "token": 250,
    "ubicacion": 2000, "politicas_de_garantia": 2000, "adaptacion_del_lenguaje": 2000,
    "saludo_del_asesor": 2000, "metodo_anticancelacion": 2000, "restricciones": 2000,
    "mensaje_agradecimiento": 2000, "tiempos": 2000, "desde_guia_generada": 2000,
    "desde_en_reparto": 2000,
    "guia_generada": 3000, "en_reparto": 3000, "en_oficina": 3000, "entregado": 3000,
    "prompt_analisis": 8000,
    "r_1": 250, "r_2": 250, "r_3": 250, "r_4": 250, "r_5": 250,
}
TECHO_BOT_FIELD = 19000   # escapados, campo JSON legacy (corta a 20.000 en silencio)

def u16(s): return len(str(s).encode("utf-16-le")) // 2

def hojas(o, p=()):
    for k, v in o.items():
        if isinstance(v, dict): yield from hojas(v, p + (k,))
        else: yield p + (k,), v

def get(o, r):
    for k in r: o = o[k]
    return o

def put(o, r, v):
    for k in r[:-1]: o = o[k]
    o[r[-1]] = v

class Api:
    def __init__(self, token): self.token = token
    def pedir(self, metodo, ruta, cuerpo=None):
        datos = json.dumps(cuerpo, ensure_ascii=False).encode() if cuerpo is not None else None
        req = urllib.request.Request(BASE + ruta, data=datos, method=metodo, headers={
            "Authorization": "Bearer " + self.token, "User-Agent": UA,
            "Accept": "application/json", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    def campos(self):
        todos, vistos, page = {}, set(), 1
        while page <= 40:          # GET pagina y per_page se ignora: recorrer hasta que no haya nuevos
            d = self.pedir("GET", f"/flow/bot-fields?page={page}")
            filas = d.get("data", d if isinstance(d, list) else [])
            nuevos = [f for f in filas if f.get("name") not in vistos]
            if not nuevos: break
            for f in nuevos:
                vistos.add(f["name"]); todos[f["name"]] = f
            page += 1
        return todos
    def escribir(self, data):
        return self.pedir("PUT", "/flow/set-bot-fields-by-name", {"data": data})

def valor(f):
    v = f.get("value")
    return json.loads(v) if isinstance(v, str) else v

def cargar_vivo(api, nombre_esperado, salida=print):
    campos = api.campos()
    faltan = [c for c in CAMPOS if c not in campos and c != "[Logistico] Novedad"]
    if faltan:
        salida(f"ABORTA: el espacio no tiene {faltan}"); return None, None, 2
    vivo = {c: valor(campos[c]) for c in CAMPOS if c in campos}
    nombre = vivo["[Logistico] Configuracion General"]["datos_de_la_tienda"]["nombre"]
    if nombre != nombre_esperado:
        salida(f"ABORTA: el token es del espacio {nombre!r}, no de {nombre_esperado!r}"); return None, None, 2
    return campos, vivo, 0

def calcular_diff(vivo, prop_dir, salida=print):
    llaves = []
    for c, arch in CAMPOS.items():
        ruta = os.path.join(prop_dir, arch + ".json")
        if c not in vivo or not os.path.exists(ruta): continue
        hv, hp = dict(hojas(vivo[c])), dict(hojas(json.load(open(ruta))))
        if set(hv) != set(hp):
            salida(f"ABORTA: la estructura de llaves de {c} no coincide con lo vivo: {sorted(set(hv) ^ set(hp))}")
            return None, 2
        llaves += [(c, k, hp[k]) for k in hp if hv[k] != hp[k]]
    return llaves, 0

def escribir(api, campos, vivo, llaves, salida=print, espera=3):
    nuevo = json.loads(json.dumps(vivo))
    for c, k, v in llaves:
        t = TOPES.get(k[-1])
        if t is not None and u16(v) > t:
            salida(f"FALLO: {c} > {k[-1]} mide {u16(v)} y su tope es {t}. No se escribe nada."); return 1
        put(nuevo[c], k, v)
    tocados = sorted({c for c, _, _ in llaves})
    data = []
    for c in tocados:
        s = json.dumps(nuevo[c], ensure_ascii=False, separators=(",", ":"))
        esc = len(json.dumps(s)[1:-1])
        if esc > TECHO_BOT_FIELD and campos[c].get("var_type") != "longtext":
            salida(f"FALLO: {c} escapado {esc} pasa {TECHO_BOT_FIELD} en un campo que no es LONG JSON"); return 1
        data.append({"name": c, "value": s})
    api.escribir(data)
    time.sleep(espera)
    releido = {c: valor(f) for c, f in api.campos().items() if c in CAMPOS}
    ok = 0
    for c, k, v in llaves:
        g = get(releido[c], k)
        igual = (g.rstrip("\n") == v.rstrip("\n")) if isinstance(v, str) and isinstance(g, str) else g == v
        ok += igual
        salida(f"  {'OK ' if igual else 'MAL'} {c} > {' > '.join(k)}")
    intactos = True
    for c in tocados:
        a, b = json.loads(json.dumps(releido[c])), json.loads(json.dumps(nuevo[c]))
        for cc, k, _ in llaves:
            if cc == c: put(a, k, None); put(b, k, None)
        if a != b:
            intactos = False; salida(f"  MAL resto de {c} cambió")
    salida(f"VERIFICADO DEL SERVIDOR: {ok} de {len(llaves)} llaves · resto intacto: {intactos}")
    return 0 if ok == len(llaves) and intactos else 1

def respaldar(campos, backup_dir, salida=print):
    os.makedirs(backup_dir, exist_ok=True)
    ruta = os.path.join(backup_dir, "logistico-ANTES-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json")
    json.dump({c: campos[c] for c in CAMPOS if c in campos}, open(ruta, "w"), ensure_ascii=False, indent=2)
    salida("respaldo: " + ruta)

# ------------------------------------------------------------------ autoprueba (sin red)
class ApiFalsa:
    def __init__(self, nombre, guarda=True, corta_en=None):
        self.guarda, self.corta_en = guarda, corta_en
        cg = {"datos_de_la_tienda": {"nombre": nombre, "ubicacion": "A"}, "comportamiento_de_la_ia": {"restricciones": "R"}}
        cf = {"analisis_direccion": {"prompt_analisis": "P"}, "pago_anticipado": {"activo": "no"}}
        sg = {"ganchos_de_venta": {"entregado": "E"}}
        self.srv = {"[Logistico] Configuracion General": cg, "[Logistico] Confirmaciones": cf, "[Logistico] Seguimiento": sg}
    def campos(self):
        return {c: {"name": c, "var_type": "array", "value": json.dumps(v, ensure_ascii=False)} for c, v in self.srv.items()}
    def escribir(self, data):
        if not self.guarda: return {"status": "ok"}          # responde ok y no guarda: el caso silencioso
        for d in data:
            v = d["value"]
            if self.corta_en: v = v[:self.corta_en]
            try: self.srv[d["name"]] = json.loads(v)
            except ValueError: pass
        return {"status": "ok"}

def autoprueba():
    import tempfile
    mudo = lambda *a, **k: None
    def prop(api, cambios, extra=None):
        d = tempfile.mkdtemp()
        for c, arch in CAMPOS.items():
            if c not in api.srv: continue
            v = json.loads(json.dumps(api.srv[c]))
            for (cc, k), val in cambios.items():
                if cc == c: put(v, k, val)
            if extra and c in extra: v.update(extra[c])
            json.dump(v, open(os.path.join(d, arch + ".json"), "w"), ensure_ascii=False)
        return d
    CG, CF = "[Logistico] Configuracion General", "[Logistico] Confirmaciones"
    casos = []
    # 1 bueno: dos llaves, se escriben, se verifican
    a = ApiFalsa("Emp"); c, v, _ = cargar_vivo(a, "Emp", mudo)
    ll, _ = calcular_diff(v, prop(a, {(CG, ("comportamiento_de_la_ia", "restricciones")): "R2", (CF, ("pago_anticipado", "activo")): "si"}), mudo)
    casos.append(("escribe 2 llaves y verifica", len(ll) == 2 and escribir(a, c, v, ll, mudo, 0) == 0))
    # 2 malo: token de otro espacio
    casos.append(("aborta si el espacio no es el esperado", cargar_vivo(ApiFalsa("Otra"), "Emp", mudo)[2] == 2))
    # 3 malo: estructura distinta
    a = ApiFalsa("Emp"); c, v, _ = cargar_vivo(a, "Emp", mudo)
    casos.append(("aborta si la propuesta cambia la estructura", calcular_diff(v, prop(a, {}, {CF: {"llave_nueva": "x"}}), mudo)[1] == 2))
    # 4 malo: pasa el tope
    a = ApiFalsa("Emp"); c, v, _ = cargar_vivo(a, "Emp", mudo)
    ll, _ = calcular_diff(v, prop(a, {(CG, ("comportamiento_de_la_ia", "restricciones")): "x" * 2001}), mudo)
    casos.append(("no escribe si una llave pasa su tope", escribir(a, c, v, ll, mudo, 0) == 1 and a.srv[CG]["comportamiento_de_la_ia"]["restricciones"] == "R"))
    # 5 bueno: 2.000 exactos PASA (el techo no es defecto)
    a = ApiFalsa("Emp"); c, v, _ = cargar_vivo(a, "Emp", mudo)
    ll, _ = calcular_diff(v, prop(a, {(CG, ("comportamiento_de_la_ia", "restricciones")): "x" * 2000}), mudo)
    casos.append(("2.000 de 2.000 se escribe sin quejarse", escribir(a, c, v, ll, mudo, 0) == 0))
    # 6 malo: el servidor responde ok y no guarda -> la verificacion debe MORDER
    a = ApiFalsa("Emp", guarda=False); c, v, _ = cargar_vivo(a, "Emp", mudo)
    ll, _ = calcular_diff(v, prop(a, {(CG, ("comportamiento_de_la_ia", "restricciones")): "R2"}), mudo)
    casos.append(("detecta 200 ok que no guardo", escribir(a, c, v, ll, mudo, 0) == 1))
    # 7 bueno: sin cambios -> 0 llaves
    a = ApiFalsa("Emp"); c, v, _ = cargar_vivo(a, "Emp", mudo)
    casos.append(("propuesta igual a lo vivo = 0 llaves", calcular_diff(v, prop(a, {}), mudo)[0] == []))
    for n, okk in casos: print(f"  {'OK ' if okk else 'MAL'} {n}")
    bien = sum(o for _, o in casos)
    print(f"\n  {bien} de {len(casos)} pruebas pasan")
    return 0 if bien == len(casos) else 1

def main(argv):
    if "--autoprueba" in argv: return autoprueba()
    def arg(n):
        return argv[argv.index(n) + 1] if n in argv else None
    modo = argv[1] if len(argv) > 1 else ""
    tok, nombre = arg("--token-file"), arg("--nombre-esperado")
    if modo not in ("leer", "diff", "escribir") or not tok or not nombre:
        print(__doc__); return 2
    api = Api(open(tok).read().strip())
    campos, vivo, e = cargar_vivo(api, nombre)
    if e: return e
    if modo == "leer":
        if not arg("--backup-dir"): print("falta --backup-dir"); return 2
        respaldar(campos, arg("--backup-dir")); return 0
    if not arg("--prop-dir"): print("falta --prop-dir"); return 2
    llaves, e = calcular_diff(vivo, arg("--prop-dir"))
    if e: return e
    print(f"llaves que cambian: {len(llaves)}")
    for c, k, _ in llaves: print(f"  {c} > {' > '.join(k)}")
    if modo == "diff" or not llaves: return 0
    if not arg("--backup-dir"): print("falta --backup-dir: no se escribe sin respaldo"); return 2
    respaldar(campos, arg("--backup-dir"))
    return escribir(api, campos, vivo, llaves)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
