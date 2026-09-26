#!/usr/bin/env python3
"""Autoprueba de golden-chatea-pro-config-comentarios.

Corre el builder de verdad contra casos buenos Y contra casos que se SABEN malos,
y verifica lo que esta skill promete. No mide estilo: mide las promesas que, si se
rompen, le cuestan dinero o la cuenta a quien la use.

Uso:  python3 scripts/autoprueba.py
Sale 0 si TODO pasa; 1 si alguna prueba falla (imprime cual y por que).

Las 16 pruebas, agrupadas por lo que protegen:

  VIA (1-4)        La normal es el default y cabe en el formulario; la VIP excede
                   a proposito; sin bandera sale normal.
  CUENTA (5-7)     Las 4 estructuras anti-baneo y las 6 tecnicas sobreviven en las
                   DOS vias, y el maximo de 40 palabras sigue escrito. Si esto se
                   pierde, Meta inhabilita la fanpage (3 baneos de Kevin, 2 de un
                   alumno arrastrando fanpage, BM y perfil).
  CLIENTES (8-10)  NEUTRO existe, el emoji suelto NO se borra, y el guardarrail
                   anti-dolencias se rellena con los productos reales.
  TOPES (11-13)    Margen >=15% en los dos campos que corta el Save del panel, y
                   en modo normal un exceso ABORTA sin escribir archivo.
  INTEGRIDAD (14-16) Cero placeholders literales, JSON valido, packs por pais.
"""
import json, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(AQUI, "build_config.py")
BASE = ["--contacto", "WhatsApp: +57 300 000 0000",
        "--t-envio", "Principales 1 a 2 dias habiles. Interior 3 a 4.",
        "--info-extra", "Pago contra entrega en todo el pais.",
        "--producto", "Serum X:hongos en las unas",
        "--producto", "Crema Y:piel flacida en el cuello"]

fallos = []
corridos = []          # numeros de caso que REALMENTE se ejecutaron


def corre(args, salida=None):
    """Devuelve (exit_code, stdout+stderr, cfg_o_None)."""
    tmp = salida or os.path.join(tempfile.mkdtemp(), "out.json")
    r = subprocess.run([sys.executable, BUILD, *args, "--out", tmp],
                       capture_output=True, text=True)
    cfg = None
    if os.path.exists(tmp):
        try:
            with open(tmp, encoding="utf-8") as f:
                cfg = json.load(f)
        except json.JSONDecodeError:
            cfg = "JSON_ROTO"
    return r.returncode, r.stdout + r.stderr, cfg, tmp


def check(n, nombre, cond, detalle=""):
    # 🔴 el total se CUENTA, no se escribe a mano: un total clavado sigue diciendo
    # "24 de 24" aunque alguien borre un caso. Y dos casos con el mismo numero se avisan,
    # porque el segundo tapa al primero en la lectura del informe.
    if n in corridos:
        print(f"[AVISO] numero de caso REPETIDO: {n} — renumera, el informe enmascara uno")
    corridos.append(n)
    print(f"[{'PASS' if cond else 'FALLA'}] {n:>2}. {nombre}" + (f"  ·  {detalle}" if detalle else ""))
    if not cond:
        fallos.append(f"{n}. {nombre}" + (f" ({detalle})" if detalle else ""))


print("=" * 68)
print("AUTOPRUEBA golden-chatea-pro-config-comentarios")
print("=" * 68)

# ---------- BASE UNICA (FER 2026-09-22: se derogo la via VIP) ----------
c_def, o_def, cfg_def, _ = corre(["--pais", "colombia", *BASE])
check(1, "La base unica se entrega sin ninguna bandera", c_def == 0, f"exit {c_def}")

c_vip, o_vip, cfg_vip, _ = corre(["--pais", "colombia", *BASE, "--vip", "si"])
check(2, "--vip esta derogado: avisa y NO cambia la salida",
      c_vip == 0 and "DEROGADO" in o_vip and cfg_vip == cfg_def,
      f"exit {c_vip} · salida identica: {cfg_vip == cfg_def}")

if cfg_def and cfg_def != "JSON_ROTO":
    rp, vc = len(cfg_def["respuesta_publica"]["prompt"]), len(cfg_def["venta_conversacional"]["prompt"])
    check(3, "La base cabe en los topes del formulario", rp <= 3000 and vc <= 8000,
          f"respuesta {rp}/3000 · venta {vc}/8000")
else:
    check(3, "La base cabe en los topes del formulario", False, "no generó config")

# Lo que de verdad hay que impedir que vuelva: que exista un entregable que NO
# quepa. Esa era la razon de ser del VIP y el origen de todo el enredo.
if cfg_def and cfg_def != "JSON_ROTO":
    crudo = len(json.dumps(cfg_def, ensure_ascii=False, separators=(",", ":")))
    check(4, "El entregable cabe en el campo (20.000 CRUDOS, medido 2026-09-22)",
          crudo <= 19600, f"{crudo} / 19600 · margen {20000 - crudo} contra el tope real")
else:
    check(4, "El entregable cabe en el campo", False, "no generó config")

# ---------- CUENTA: el guardarrail anti-baneo ----------
for n, (etiqueta, cfg) in enumerate([("NORMAL", cfg_def), ("VIP", cfg_vip)], start=5):
    ok = False
    if cfg and cfg != "JSON_ROTO":
        p = cfg["respuesta_publica"]["prompt"]
        estructuras = sum(f"\n{i}- " in p for i in range(1, 5))
        tecnicas = sum(f"\n{i}. " in p for i in range(1, 7))
        ok = estructuras == 4 and tecnicas == 6
        det = f"{estructuras}/4 estructuras · {tecnicas}/6 tecnicas"
    else:
        det = "sin config"
    check(n, f"Anti-baneo intacto en la via {etiqueta}", ok, det)

ok40 = all(cfg and cfg != "JSON_ROTO" and "40 palabras" in cfg["respuesta_publica"]["prompt"]
           for cfg in (cfg_def, cfg_vip))
check(7, "El maximo de 40 palabras sigue escrito en las dos vias", ok40)

# ---------- CLIENTES: a quien NO se borra ----------
pg = cfg_def["comentarios_negativos"]["prompt_general"] if cfg_def and cfg_def != "JSON_ROTO" else ""
check(8, "NEUTRO existe como categoria", "NEUTRO" in pg)
check(9, "El emoji suelto NO se manda a borrar",
      "emojis sueltos, letras" not in pg and "es NEUTRO" in pg)
ne = cfg_def["comentarios_negativos"]["ej_a_no_eliminar"] if cfg_def and cfg_def != "JSON_ROTO" else ""
check(10, "Guardarrail anti-dolencias relleno con los productos reales",
      "hongos en las unas" in pg and "piel flacida" in pg and "dolencia" in ne.lower())

# ---------- TOPES ----------
if cfg_def and cfg_def != "JSON_ROTO":
    # Antes esta prueba exigia un 15% de margen libre. Era doctrina equivocada y
    # contradecia la ley de la casa: "el techo del campo NO es defecto, 1.999 de
    # 2.000 pasa". Exigir margen obliga a tirar contenido util que si cabe.
    # Lo que importa es no PASARSE: eso es lo que el Save del panel corta.
    cn = cfg_def["comentarios_negativos"]
    n_el, n_no = len(cn["ej_a_eliminar"]), len(cn["ej_a_no_eliminar"])
    check(11, "Los campos que corta el Save del panel NO se pasan de 1.000",
          n_el <= 1000 and n_no <= 1000, f"a-eliminar {n_el}/1000 · no-eliminar {n_no}/1000")
else:
    check(11, "Los campos que corta el Save del panel NO se pasan", False, "sin config")

# caso que se SABE malo: datos_req inflado sobre su tope de 200, en via normal
largo = "Nombre completo; " * 30
c_mal, o_mal, cfg_mal, ruta_mal = corre(["--pais", "colombia", *BASE,
                                         "--datos-cliente", largo, "--destino", "longjson"])
check(12, "Un tope reventado ABORTA en via normal", c_mal == 1 and "ERROR" in o_mal, f"exit {c_mal}")
check(13, "Y no deja archivo a medias", not os.path.exists(ruta_mal))

# ---------- INTEGRIDAD ----------
crudo = json.dumps(cfg_def, ensure_ascii=False) if cfg_def and cfg_def != "JSON_ROTO" else "{{ROTO}}"
check(14, "Cero placeholders literales en la salida", "{{" not in crudo)
check(15, "La salida es JSON valido", cfg_def not in (None, "JSON_ROTO"))

# packs por pais: el despectivo NO puede ser el mismo en dos paises distintos.
# Se comprueba el MECANISMO (que cambie), no una palabra concreta: la semilla se
# edita y un test clavado a "chichipato" se rompe sin que nada este mal.
import re as _re
def _desp(cfg):
    if not cfg or cfg == "JSON_ROTO":
        return None
    m = _re.search(r"despectiva local[^:]*: (.+)", cfg["comentarios_negativos"]["prompt_general"])
    return m.group(1).strip() if m else None

_, _, cfg_mx, _ = corre(["--pais", "mexico", *BASE, "--destino", "longjson"])
d_co, d_mx = _desp(cfg_def), _desp(cfg_mx)
check(16, "El despectivo local cambia con el pais",
      bool(d_co) and bool(d_mx) and d_co != d_mx,
      f"colombia=«{(d_co or 'nada')[:24]}» · mexico=«{(d_mx or 'nada')[:24]}»")

# ---------- PROCEDENCIA: semilla vs dato del dueño ----------
_, o_sem, _, _ = corre(["--pais", "colombia", *BASE, "--destino", "longjson"])
check(17, "Avisa cuando el despectivo es SEMILLA y no dato medido",
      "SEMILLA" in o_sem and "--despectivo" in o_sem)

# 🔴 POR QUE ESTAS TRES SE ANCLAN A LA BANDERA Y NO A LA PALABRA DEL MENSAJE:
# un `not in` sobre la REDACCION de un aviso es un FALSO VERDE esperando. El dia que
# alguien mejore el texto y quite la palabra "SEMILLA", la prueba pasa siempre, aunque
# el detector este roto. Un `in` que se rompe da rojo, que se ve; un `not in` que se
# rompe da verde, que no se ve. Se anclan a `--despectivo`, que es INTERFAZ (el nombre
# de la bandera) y no prosa. Y quedan en cobertura cruzada con la 17, que exige que SI
# aparezca: si alguien renombra la bandera, la 17 se pone roja y delata a las otras dos.
# Es el mismo fallo que ya mordio a la 21 y la 22 el 06-sep, y que no se habia aplicado
# a sus vecinas.
_, o_gt, _, _ = corre(["--pais", "guatemala", *BASE, "--destino", "longjson"])
check(18, "NO avisa en el unico pais con fuente real (guatemala)",
      "--despectivo" not in o_gt)

_, o_real, cfg_real, _ = corre(["--pais", "colombia", *BASE, "--destino", "longjson",
                                "--despectivo", "chichipato, bareto"])
usa_real = (cfg_real not in (None, "JSON_ROTO")
            and "chichipato, bareto" in cfg_real["comentarios_negativos"]["prompt_general"]
            and "corroncho" not in cfg_real["comentarios_negativos"]["prompt_general"])
check(19, "La palabra del dueño REEMPLAZA la semilla (no se suma)",
      usa_real and "--despectivo" not in o_real)

# ---------- ESTANDAR DE PAISES: 10, no 7 ----------
# Aqui el `not in` sobre el aviso sobraba: lo que prueba que Guatemala tiene pack propio
# no es que falte un mensaje, es que el resultado SALE con ZONA y NO sale con el pack de
# Colombia. Eso es conducta, y no depende de como este redactado ningun aviso.
rc_gt2, o_gt2, cfg_gt, _ = corre(["--pais", "guatemala", *BASE, "--destino", "longjson"])
tiene_zona = (cfg_gt not in (None, "JSON_ROTO")
              and "ZONA" in cfg_gt["venta_conversacional"]["datos_req"]
              and "Barrio o punto de referencia" not in cfg_gt["venta_conversacional"]["datos_req"])
# El exit esperado es 2, no 0: con un pais distinto de colombia el detector de
# colombianismos salta y marca ADAPTACION MANUAL PENDIENTE. Medido, no supuesto — la
# primera version de esta linea exigia 0 y se puso roja, que es el banco haciendo su
# trabajo sobre quien lo escribe.
check(20, "Guatemala tiene pack propio (ZONAS), no hereda el de Colombia",
      rc_gt2 == 2 and tiene_zona, f"exit {rc_gt2} · datos_req con ZONA y sin pack CO")

# 🔴 ESTAS TRES MIRAN EL RESULTADO, NO EL AVISO. Hasta el 2026-09-06 la 21 y la 22
# comprobaban que se hubiera IMPRESO un texto, y pasaban en verde mientras el JSON salia
# con el pack de Colombia para argentina y bolivia ("Barrio…; Ciudad; Departamento" — y en
# Argentina no hay departamentos). Un banco que comprueba el mensaje certifica la intencion,
# no la conducta. Se compara contra el pack colombiano REAL, no contra una cadena a mano.
PACK_CO = "Barrio o punto de referencia"

rc_ar, o_ar, cfg_ar, _ = corre(["--pais", "argentina", *BASE, "--destino", "longjson"])
check(21, "Argentina SIN pack: no construye y NO hereda el pack de Colombia",
      rc_ar != 0 and cfg_ar is None and PACK_CO not in o_ar and "--datos-cliente" in o_ar)

rc_bo, o_bo, cfg_bo, _ = corre(["--pais", "bolivia", *BASE, "--destino", "longjson"])
check(22, "Un pais sin pack tampoco hereda: se niega y pide la lista real",
      rc_bo != 0 and cfg_bo is None and PACK_CO not in o_bo and "--datos-cliente" in o_bo)

# El pais NO se rechaza: lo unico que se rechaza es INVENTARLE la direccion. Con la lista
# real del negocio, el mismo pais construye sin problema. Sin este caso, la negativa de
# arriba pasaria por una puerta de pais — que es justo lo que la doctrina prohibe.
rc_ok, o_ok, cfg_ok, _ = corre(["--pais", "argentina", *BASE, "--destino", "longjson",
                                "--datos-cliente",
                                "Nombre completo; WhatsApp; Calle y numero; Piso y depto; "
                                "Localidad; Provincia; Codigo postal"])
check(23, "Argentina CON --datos-cliente: la DIRECCION queda argentina",
      cfg_ok not in (None, "JSON_ROTO")
      and "Provincia" in cfg_ok["venta_conversacional"]["datos_req"]
      and PACK_CO not in cfg_ok["venta_conversacional"]["datos_req"])

# …y aun asi NO se da por entregable: el detector de colombianismos salta porque el resto
# del prompt (moneda, ciudades, jerga) sigue siendo colombiano. Son DOS capas: --datos-cliente
# arregla la direccion, no el idioma. Sin este caso, alguien podria "arreglar" el exit 2
# creyendolo un fallo y apagaria el unico aviso que queda de que falta trabajo a mano.
check(24, "…y el detector de colombianismos SIGUE saltando: la direccion no es el idioma",
      rc_ok != 0 and "colombianismos" in o_ok.lower())

# ---------- LA DESCRIPTION ES EL DISPARADOR Y SU TOPE ES DURO ----------
# 1024 VALIDA (duro, lo rechaza el validador oficial) y ~1536 TRUNCA en runtime:
# no son el mismo techo. Sin esta prueba, meter una palabra de disparador deja la
# skill invalida EN SILENCIO. Aviso del Centro de Mando 2026-09-05: se llego a
# estar a 19 caracteres del muro.
try:
    import yaml as _yaml
except ImportError:
    print("ERROR: falta pyyaml (pip install pyyaml) — lo necesitan las pruebas 23-24,")
    print("       que leen el frontmatter de SKILL.md. El resto del builder no lo usa.")
    sys.exit(1)
_sk = os.path.join(AQUI, "..", "SKILL.md")
with open(_sk, encoding="utf-8") as _f:
    _txt = _f.read()
_fm = re.match(r"^---\n(.*?)\n---\n", _txt, re.S)
_desc = _yaml.safe_load(_fm.group(1))["description"] if _fm else ""
_n = len(_desc)
check(25, "La description cabe en el tope DURO de 1024 con margen",
      0 < _n <= 1024 and (1024 - _n) >= 40, f"{_n} / 1024 · margen {1024 - _n}")

check(26, "La description conserva VIP como DISPARADOR (ya no como via)",
      "VIP" in _desc, "sin el, 'configura la chatea VIP' no dispara igual")

# ---- 27-28 · la doctrina de FER: lo del pais se INVESTIGA, no se pregunta ----
# 🔴 El 2026-09-07 el mensaje de error del builder ordenaba "Pregúntale al negocio qué campos
# lleva una dirección ahí". El BLOQUEO estaba bien; el SIGUIENTE PASO que ordenaba estaba mal,
# y contradecía de frente la ley de FER del 06-sep. Un mensaje de error es una INSTRUCCIÓN: se
# obedece tal cual, así que un builder que bloquea bien y luego manda hacer lo prohibido deja
# el mismo daño que si no bloqueara. Este par muerde si la frase vuelve.
_bc = os.path.join(AQUI, "build_config.py")
with open(_bc, encoding="utf-8") as _f:
    _src = _f.read()
_i = _src.find("NO se hereda el pack de otro")
_msg = _src[_i - 600:_i + 1400] if _i > 0 else ""
check(27, "El aviso sin pack manda INVESTIGAR, no preguntarle al negocio",
      "se INVESTIGA" in _msg and "NO se le pregunta al negocio" in _msg,
      "la forma de la direccion no se pregunta: es justo lo que la skill existe para resolver")
check(28, "🔴 y NO quedo ninguna orden de preguntarle la direccion al negocio",
      "Pregúntale al negocio qué campos lleva una dirección" not in _src,
      "la frase prohibida no puede volver por un refactor")

# ---- 29 · el sello de version del cuerpo no puede ir por detras del acta ----
# El 2026-09-07 el cuerpo estampaba v1.16 mientras references/changelog.md ya iba por v1.17:
# la skill mentia sobre su propia version, y una version que miente hace que dos chats crean
# estar mirando lo mismo cuando no lo estan.
_ch = os.path.join(AQUI, "..", "references", "changelog.md")
with open(_ch, encoding="utf-8") as _f:
    _cl = _f.read()
# 🔴 Anclado al ENCABEZADO del acta y al SELLO del cuerpo, no a cualquier "vX.Y" del texto:
# la primera version de esta prueba grepeaba todo el changelog y sacaba v4.1 — que es la version
# de una skill HERMANA citada en la prosa. Un detector que barre el texto entero acusa al idioma.
def _vs(t, patron):
    return [tuple(int(x) for x in v.split(".")) for v in re.findall(patron, t)]
_v_cuerpo = max(_vs(_txt, r"<!--\s*skill v(\d+\.\d+)") or [(0, 0)])
_v_acta = max(_vs(_cl, r"(?m)^##\s*v(\d+\.\d+)") or [(0, 0)])
check(29, "El sello de version del cuerpo NO va por detras del changelog",
      _v_cuerpo >= _v_acta,
      f"cuerpo v{_v_cuerpo[0]}.{_v_cuerpo[1]} · acta v{_v_acta[0]}.{_v_acta[1]}")

# ---------- LO APRENDIDO EL 2026-09-22, clavado para que no derive otra vez ----------

# 30. El catalogo grande. Antes el guardarrail escribia una linea POR PRODUCTO con
#     su nombre, asi que a los ~50 productos la config reventaba el campo. Pregunta
#     literal de FER: "y que tal que tuviera mil productos?".
_p1000 = []
for _i in range(1000):
    _p1000 += ["--producto", f"Producto {_i+1}:dolencia tipo {_i % 20}"]
_c_mil, _o_mil, _cfg_mil, _ = corre(["--pais", "colombia", "--contacto", "WhatsApp +57 300 000 0000",
                                     "--t-envio", "Ciudad principal 2-3 dias.",
                                     "--info-extra", "Pago contra entrega.", *_p1000])
_crudo_mil = (len(json.dumps(_cfg_mil, ensure_ascii=False, separators=(",", ":")))
              if _cfg_mil and _cfg_mil != "JSON_ROTO" else 0)
check(30, "1.000 productos NO revientan el campo (el guardarrail satura)",
      _c_mil == 0 and 0 < _crudo_mil <= 19600,
      f"exit {_c_mil} · {_crudo_mil} crudos · margen {20000 - _crudo_mil}")

# 31. Y la razon por la que satura: ya no cita el catalogo. Un prompt que nombra
#     productos caduca solo el dia que la tienda los saca, sin dar ningun error.
if _cfg_mil and _cfg_mil != "JSON_ROTO":
    _pg_mil = _cfg_mil["comentarios_negativos"]["prompt_general"]
    check(31, "El clasificador NO cita nombres de producto (no caduca con el catalogo)",
          "Producto 1" not in _pg_mil and "Producto 500" not in _pg_mil,
          "el prompt habla de dolencias, no de referencias del catalogo")
else:
    check(31, "El clasificador NO cita nombres de producto", False, "sin config")

# 32. El caso que se SABE malo: una config pasada del techo del campo tiene que
#     BLOQUEAR con exit 1 y sin archivo. Inflar un campo de negocio NO basta
#     (miden cientos de caracteres y el techo esta a miles); lo que si empuja el
#     total es el guardarrail, porque cada dolencia entra DOS veces (en la lista
#     y en las frases). Doce dolencias largas pasan el techo sin pasarse de
#     ningun tope nativo: es exactamente el fallo que el panel no sabe avisar.
_dolencia_larga = "una condicion descrita con mucho detalle clinico y palabras de mas " * 3
_gordos = []
for _i in range(12):
    _gordos += ["--producto", f"Producto {_i+1}:{_dolencia_larga}{_i}"]
_c_gordo, _o_gordo, _cfg_gordo, _ruta_gordo = corre(
    ["--pais", "colombia", "--contacto", "WhatsApp +57 300 000 0000",
     "--t-envio", "Ciudad principal 2-3 dias.",
     "--info-extra", "x" * 480, *_gordos])
check(32, "Una config que se pasa del techo del campo BLOQUEA",
      _c_gordo == 1 and not os.path.exists(_ruta_gordo),
      f"exit {_c_gordo} · sin archivo: {not os.path.exists(_ruta_gordo)}")

# 33. Que no vuelvan los numeros derogados. El techo se mide en CRUDOS: tratarlo
#     como escapados producia un "techo practico de 17.000" que RECHAZABA config
#     buena, y mandaba convertir el campo a LONG JSON, que no se puede ni hace falta.
#     OJO CON EL DETECTOR: la primera version de esta prueba grepeaba las frases
#     del error ("~17.000 crudos", "19.000 escapados") y saltaba sobre el parrafo
#     que las CORRIGE, porque para corregir una frase hay que citarla. Un detector
#     por palabra acusa al texto que explica el fallo. Por eso aqui se busca la
#     ORDEN vigente y el nombre de la constante, que no aparecen al explicar nada.
_codigo = open(os.path.join(AQUI, "build_config.py"), encoding="utf-8").read()
_zombis = []
if "LIMITE_ESCAPADO_SEGURO" in _codigo:
    _zombis.append("constante del techo falso viva en el codigo")
if "LIMITE_CRUDO" not in _codigo:
    _zombis.append("falta la constante del techo medido")
if "Crea el campo como LONG JSON" in _txt:
    _zombis.append("SKILL.md sigue ordenando convertir el campo a LONG JSON")
if "19.617" not in _txt:
    _zombis.append("SKILL.md no trae la medicion del 2026-09-22")
check(33, "El techo vigente es el MEDIDO en crudos, no el heredado en escapados",
      not _zombis, "; ".join(_zombis) if _zombis else "constante y doc alineadas con la medicion")

# 34. El nombre del negocio. Es la primera pieza de la parte dinamica que FER
#     enumero, y durante mucho tiempo NO existia como parametro: el ROL decia
#     "esta tienda" mientras el espacio vivo decia el nombre real, asi que la
#     skill y el espacio se separaban desde la primera linea del prompt. Se
#     comprueba que entra cuando se pasa, que NO se hornea cuando no, y que
#     ningun nombre concreto queda pegado en la plantilla.
_c_neg, _o_neg, _cfg_neg, _ = corre(["--pais", "colombia", *BASE, "--negocio", "Tienda Ejemplo"])
_c_gen, _o_gen, _cfg_gen, _ = corre(["--pais", "colombia", *BASE])
_rol_neg = _cfg_neg["comentarios_negativos"]["prompt_general"][:130] if _cfg_neg and _cfg_neg != "JSON_ROTO" else ""
_rol_gen = _cfg_gen["comentarios_negativos"]["prompt_general"][:130] if _cfg_gen and _cfg_gen != "JSON_ROTO" else ""
check(34, "El nombre del negocio entra por parametro y no se hornea",
      "Tienda Ejemplo" in _rol_neg and "esta tienda" in _rol_gen,
      "con --negocio nombra al negocio · sin el, generico")

# 35. Y la plantilla NO puede traer el nombre de nadie: la skill se comparte.
_tpl = open(os.path.join(AQUI, "..", "assets", "template.json"), encoding="utf-8").read()
_pegados = [m for m in ("Golden", "Le'coterra", "Tag Recede", "Toppik", "Marbella") if m in _tpl]
check(35, "La plantilla compartible no lleva el nombre de ningun cliente",
      not _pegados, f"encontrados: {_pegados}" if _pegados else "limpia")

print("=" * 68)
if fallos:
    print(f"RESULTADO: {len(fallos)} de {len(corridos)} FALLAN")
    for f in fallos:
        print("  - " + f)
    sys.exit(1)
print(f"RESULTADO: {len(corridos)} de {len(corridos)} · TODO OK")
sys.exit(0)
