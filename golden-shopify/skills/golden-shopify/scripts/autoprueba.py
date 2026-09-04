#!/usr/bin/env python3
"""
GOLDEN SHOPIFY · autoprueba.py
Prueba de regresion DEL PROPIO VALIDADOR (patron heredado de golden-pdf-check).

POR QUE SE LLAMA ASI
  Se llamaba selftest.py. Un censo del arsenal buscando "selftest" encontro 2 skills con
  prueba de regresion; buscando tambien "autoprueba" encontro SEIS. Esta casa nombra sus
  pruebas en espanol (golden-chatea-auditoria, golden-chatea-operacion, golden-skill-auditor),
  asi que un archivo llamado en ingles es invisible al proximo censo. Se arregla el
  instrumento, no el acuerdo: mismo idioma que el resto del arsenal.

POR QUE EXISTE
  Ley de higiene de FER: "si tu script dice que todo esta bien a la primera, sospecha
  del script: pruebalo contra un caso que sepas malo". Un validador sin selftest se
  pudre en silencio — sigue imprimiendo el tic verde mucho despues de haber dejado de
  mirar. Aqui cada bug que esta skill ya PAGO en produccion tiene su caso, construido
  saboteando la plantilla base real (nada simulado).

REGLA AL AGREGAR UN CHECK
  Todo check nuevo de autocheck.py entra aqui con DOS casos: uno malo que debe cazar
  y, si el check puede confundirse, uno BUENO que NO debe disparar. Sin su caso, el
  check no esta terminado. Los casos buenos son los que detectan falsos positivos, y
  un falso positivo entrena a ignorar la salida entera: es tan grave como no cazar.

USO   python3 autoprueba.py            (usa ../assets/product.base.json)
      python3 autoprueba.py <base.json>
SALIDA 0 = todas pasan · 1 = alguna falla
"""
import json, os, re, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import autocheck  # noqa: E402
import sellos     # noqa: E402


def base_por_defecto():
    p = os.path.join(AQUI, "..", "assets", "product.base.json")
    return os.path.normpath(p)


def cargar(ruta):
    raw = open(ruta, encoding="utf-8").read()
    c = re.match(r'^(/\*.*?\*/\s*)', raw, flags=re.S)
    head = c.group(1) if c else ""
    return head, json.loads(raw[len(head):], strict=False)


def escribir(head, d):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    f.write(head + json.dumps(d, ensure_ascii=False, indent=2))
    f.close()
    return f.name


def primera_seccion_cl(d):
    """La primera seccion con custom_liquid, para inyectarle el sabotaje."""
    for k, s in d["sections"].items():
        if s.get("settings", {}).get("custom_liquid"):
            return k
    return list(d["sections"].keys())[0]


# ── cada entrada: (nombre, sabotaje, fragmento que DEBE aparecer en el fallo) ──
def sab_fuga(d, k):      d["sections"][k]["settings"]["custom_liquid"] += "\n{# fuga #}"
def sab_padding(d, k):   d["sections"][k]["settings"]["padding_top"] = 36
def sab_demo(d, k):      d["sections"][k]["settings"]["custom_liquid"] += "\n<h2>PRODUCTO DEMO</h2>"
def sab_candado(d, k):
    """El check mira DOS senales (la clase gfs-lock-landing y la clave custom_liquid_lock
    en el JSON crudo), asi que hay que apagar las dos: apagar solo una no lo disparaba, y
    ese fue un fallo del CASO de prueba, no del validador (medido al estrenarlo)."""
    for s in d["sections"].values():
        st = s.get("settings", {})
        if "gfs-lock-landing" in st.get("custom_liquid", ""):
            st["custom_liquid"] = st["custom_liquid"].replace("gfs-lock-landing", "x-quitado")
        for bk in list(s.get("blocks", {}).keys()):
            if re.search(r'(?<!b)lock', bk.lower()):
                s["blocks"].pop(bk)
                s["block_order"] = [b for b in s.get("block_order", []) if b != bk]
    for k2 in [x for x in d["sections"] if re.search(r'(?<!b)lock', x.lower())]:
        d["sections"][k2 + "_x"] = d["sections"].pop(k2)
        d["order"] = [o if o != k2 else k2 + "_x" for o in d.get("order", [])]


def sab_lock_dup(d, k):
    """Reintroduce el fosil que traia el generador: candado como bloque del main Y como
    seccion suelta a la vez (dos fuentes de verdad para la misma regla)."""
    main = d["sections"].get("main", {})
    main.setdefault("blocks", {})["custom_liquid_lock"] = {
        "type": "custom_liquid", "settings": {"custom_liquid": "<style>#shopify-section-header{display:none}</style>"}}
    main.setdefault("block_order", []).append("custom_liquid_lock")
def sab_peso(d, k):      d["sections"][k]["settings"]["custom_liquid"] += "á" * 26_000  # >50KB en UTF-8
def sab_trigger(d, k):   d["sections"][k]["settings"]["custom_liquid"] += '\n<a href="https://wa.me/57300?text=Hola, quiero informacion de Marca">wa</a>'
def sab_wa_place(d, k):  d["sections"][k]["settings"]["custom_liquid"] += '\n<a href="https://wa.me/573001234567">wa</a>'
def sab_related(d, k):
    d["sections"].setdefault("related-products", {"type": "related-products"})["disabled"] = False
def sab_apertura(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += "\n<h2>¿Como funciona el producto?</h2>"
def sab_mojibake(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += "\n<p>informaciÃ³n del producto</p>"
def sab_raya(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += "\n<p>beneficios ———————— envio</p>"
def sab_tienda(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += "\n<p>Gracias por visitar nuestra tienda</p>"
def sab_credencial(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += "\n<script>var t='shpat_" + "a1b2c3d4"*4 + "';</script>"
def sab_hex(d, k):       d["sections"][k]["settings"]["custom_liquid"] += "\n<div style='color:#0bd4fd'>x</div>"

# ── casos BUENOS: contenido legitimo que NO debe disparar ningun fallo ──
#    El check 22 (disparador) es el que mas facil se pasa de listo: tiene que aceptar la
#    formula exacta CON y SIN tilde, porque el disparador registrado en Chatea puede estar
#    escrito de las dos formas (arte previo: golden-chatea-auditoria sabotea con y sin tilde).
def ok_trigger_tilde(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += (
        '\n<a href="https://wa.me/57300?text=Hola quiero información y precio de Marca">wa</a>')
def ok_trigger_sin_tilde(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += (
        '\n<a href="https://wa.me/57300?text=Hola quiero informacion y precio de Marca">wa</a>')
def ok_apertura_en_comentario(d, k):
    """Un signo de apertura DENTRO de un comentario Liquid no se publica: no debe fallar."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n{% comment %} ¿esto se publica? no: es un comentario {% endcomment %}")
def ok_tildes_correctas(d, k):
    """Tildes bien escritas NO son mojibake. Confundirlas seria el falso positivo que mas
    dano hace, porque empujaria a quitar acentos correctos del copy."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n<p>Información, presentación, atención y también acción — todo con tilde.</p>")
def ok_raya_em_en_prosa(d, k):
    """Una raya em suelta en prosa es correcta. Marcarla empujaria a escribir peor."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n<p>Formula natural — sin quimicos agresivos — apta para piel sensible.</p>")
def ok_palabra_tienda_suelta(d, k):
    """«tienda» sin posesivo (una direccion, un horario) no es el vicio que la regla persigue."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n<p>Disponible tambien en tiendas fisicas de Bogota.</p>")
def ok_clase_larga_no_es_token(d, k):
    """Una clase o un hash CSS largo NO es una credencial."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n<div class='gfs-bloque-alternado-imagen-derecha-variante-larga-a1b2c3d4e5'>x</div>")
def ok_raya_en_comentario_js(d, k):
    """Los componentes usan separadores para orientar a quien EDITA el codigo. No se publican."""
    d["sections"][k]["settings"]["custom_liquid"] += (
        "\n<script>/* ═══ EDITAR AQUI ═══ */</script>\n{%- comment -%} ───── nota ───── {%- endcomment -%}")
def ok_atencion(d, k):
    d["sections"][k]["settings"]["custom_liquid"] += (
        '\n<a href="https://wa.me/57300?text=Hola, tengo una pregunta sobre Marca">wa</a>')

CASOS_BUENOS = [
    ("disparador correcto CON tilde",     ok_trigger_tilde,     "disparador"),
    ("disparador correcto SIN tilde",     ok_trigger_sin_tilde, "disparador"),
    ("mensaje libre a atencion al cliente", ok_atencion,        "disparador"),
    ("apertura ¿ DENTRO de un comentario (no se publica)", ok_apertura_en_comentario, "APERTURA"),
    ("tildes correctas NO son mojibake",                   ok_tildes_correctas,       "ACENTOS ROTOS"),
    ("raya em suelta en prosa es correcta",                ok_raya_em_en_prosa,       "RAYA SEPARADORA"),
    ("separador dentro de comentario de codigo no se publica", ok_raya_en_comentario_js, "RAYA SEPARADORA"),
    ("«tiendas fisicas» sin posesivo no es el vicio",      ok_palabra_tienda_suelta,  "lenguaje de TIENDA"),
    ("clase CSS larga NO es una credencial",               ok_clase_larga_no_es_token, "CREDENCIAL"),
]

CASOS_MALOS = [
    ("fuga de comentario {# #} (bug de 'las letras' en la pagina)", sab_fuga,     "{# #}"),
    ("padding_top que Shrine rechaza al guardar",                   sab_padding,  "padding_top"),
    ("texto DEMO visible en la entrega final",                      sab_demo,     "DEMO visible"),
    ("candado landing ausente (el cliente se va al home)",          sab_candado,  "CANDADO"),
    ("custom_liquid sobre el tope de 50 KB en bytes UTF-8",         sab_peso,     "bytes UTF-8"),
    ("disparador de Chatea que NO casa byte a byte (bug G4.8)",     sab_trigger,  "disparador"),
    ("WhatsApp con el numero placeholder",                          sab_wa_place, "PLACEHOLDER"),
    ("related-products encendido",                                  sab_related,  "related-products"),
    ("hex huerfano suelto fuera de la paleta",                       sab_hex,      "#0bd4fd"),
    ("candado DUPLICADO (bloque en main + seccion suelta)",          sab_lock_dup, "DUPLICADO"),
    ("REGLA DURA: signo de apertura ¿ en texto visible",             sab_apertura, "APERTURA"),
    ("REGLA DURA: acentos rotos (mojibake) en el texto",             sab_mojibake, "ACENTOS ROTOS"),
    ("REGLA DURA: raya separadora decorativa",                       sab_raya,     "RAYA SEPARADORA"),
    ("REGLA DURA: lenguaje de tienda («nuestra tienda»)",            sab_tienda,   "lenguaje de TIENDA"),
    ("REGLA DURA: credencial filtrada en el entregable",             sab_credencial, "CREDENCIAL"),
]


def pruebas_de_sellos():
    """Casos de scripts/sellos.py — el validador de las CUATRO CARAS de la version.

    Se horneo el mismo dia que la Regla 0-H y nacio SIN pruebas: lo cazo el Centro de
    Mando, y es la tercera vez en el dia que 0-H se aplica a si misma. El modo de fallo
    que vigilan estos casos es silencioso: si un regex deja de casar y el codigo tratara
    "no encontre version" como "coinciden", sellos.py saldria 0 SIEMPRE y nadie se
    enteraria. El verde eterno.

    Todo corre sobre COPIAS temporales: un validador que para probarse tiene que escribir
    en el registro real no es un validador, es un riesgo.
    """
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "references"))
    def escribir_skill(sello, changelog):
        open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(
            f"# GOLDEN SHOPIFY\n<!-- skill {sello} · prueba -->\n")
        open(os.path.join(d, "references", "changelog.md"), "w", encoding="utf-8").write(
            f"## {changelog} — prueba\n")
    def escribir_registro(version):
        p = os.path.join(d, "REGISTRO.md")
        open(p, "w", encoding="utf-8").write(
            f"| skill | version |\n| golden-shopify | {version} | chat | declaracion |\n")
        return p

    casos = []
    # S1 — las tres caras iguales: 0 fallos. Ademas prueba el SEGUNDO EJE: la skill real
    #      tiene GFS_VERSION distinta del sello y eso NO debe contar como desfase, porque
    #      sellos.py no lo mira. Si alguien lo "sincroniza", rompe el otro eje.
    escribir_skill("G9.01", "G9.01")
    _, f, av = sellos.revisar(d, escribir_registro("G9.01"))
    casos.append(("S1 tres caras iguales → sin fallos ni avisos", not f and not av, f + av))
    # S2 — el caso que regalo el CdM ya corrido: registro con version falsa.
    _, f, av = sellos.revisar(d, escribir_registro("G9.99"))
    #   El registro NO bloquea (otro escritor, ventana legitima): debe salir como AVISO,
    #   y ademas NO debe contaminar los fallos, o volveria a ser bloqueante por la puerta de atras.
    casos.append(("S2 registro desfasado → AVISA sin bloquear",
                  any("registro" in x for x in av) and not f, (f, av)))
    # S3 — el bump toco una cara y no la otra.
    escribir_skill("G9.02", "G9.01")
    _, f, av = sellos.revisar(d, escribir_registro("G9.02"))
    #   Este SI bloquea: vive dentro del arbol y no tiene segundo escritor.
    casos.append(("S3 sello != changelog → BLOQUEA (dentro del arbol)",
                  any("changelog" in x for x in f), f))
    # S4 — registro AUSENTE: debe fallar, no dar por bueno (ausencia no es prueba).
    escribir_skill("G9.01", "G9.01")
    _, f, av = sellos.revisar(d, os.path.join(d, "NO-EXISTE.md"))
    casos.append(("S4 registro ausente → avisa, no lo da por bueno",
                  any("no se pudo leer" in x for x in av), av))
    # S5 — registro presente pero SIN la fila: mismo trato que ausente.
    p5 = os.path.join(d, "vacio.md")
    open(p5, "w", encoding="utf-8").write("| skill | version |\n| otra-skill | X |\n")
    _, f, av = sellos.revisar(d, p5)
    casos.append(("S5 registro sin la fila → avisa, no lo da por bueno",
                  any("no se pudo leer" in x for x in av), av))
    shutil.rmtree(d, ignore_errors=True)
    return casos


def prueba_spec_oficial():
    """La skill se valida A SI MISMA contra la spec de publicacion.

    HUECO QUE CIERRA (medido 2026-09-02): esta skill validaba a fondo el product.json que
    PRODUCE, pero no se validaba a si misma como artefacto publicable — y se publica al
    marketplace de la comunidad. La `description` llevaba `product.<tema>.json` y la spec
    prohibe los angulares; lo caza el validador OFICIAL que trae skill-creator, que ninguna
    de nuestras herramientas corria. Un validador propio muy pulido no sustituye al de la
    plataforma que publica.

    BLOQUEA si el validador existe y falla (el fallo es NUESTRO, esta en nuestro SKILL.md).
    AVISA si no se encuentra: vive fuera de nuestro arbol, lo mantiene otro, y no podemos
    romper la corrida por algo que no controlamos (refinacion 2 de la ley).
    """
    cand = [os.path.expanduser("~/.claude/skills/skill-creator/scripts/quick_validate.py")]
    v = next((c for c in cand if os.path.exists(c)), None)
    skill = os.path.normpath(os.path.join(AQUI, ".."))
    if not v:
        return [("spec oficial: validador no encontrado (AVISO, vive fuera del arbol)", True,
                 "no bloquea: no lo mantenemos nosotros")]
    r = subprocess.run([sys.executable, v, skill], capture_output=True, text=True)
    salida = (r.stdout + r.stderr).strip()
    return [(f"spec oficial de publicacion ({os.path.basename(v)})", r.returncode == 0, salida)]


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else base_por_defecto()
    if not os.path.exists(ruta):
        print(f"❌ no encuentro la plantilla base: {ruta}"); sys.exit(1)
    head, base = cargar(ruta)
    ok = fail = 0
    print(f"GOLDEN SHOPIFY · autoprueba · base: {os.path.basename(ruta)}\n")

    # CASO 0 (anti-falso-positivo): la plantilla base, en modo --base, debe salir LIMPIA.
    # Si este falla, el validador grita en falso y la gente aprende a ignorarlo.
    fallos = autocheck.revisar(ruta, es_base=True)
    if fallos:
        print(f"❌ base limpia → esperaba 0 hallazgos, salieron {len(fallos)}:")
        for f in fallos:
            print(f"     · {f}")
        fail += 1
    else:
        print("✅ base limpia → 0 hallazgos (sin falsos positivos)")
        ok += 1

    # CASOS MALOS: cada uno debe ser cazado, y por el check correcto.
    for nombre, sabotaje, esperado in CASOS_MALOS:
        head2, d = cargar(ruta)
        k = primera_seccion_cl(d)
        d["sections"][k].setdefault("settings", {})
        sabotaje(d, k)
        tmp = escribir(head2, d)
        try:
            fallos = autocheck.revisar(tmp, es_base=False)
            cazado = any(esperado.lower() in f.lower() for f in fallos)
            if cazado:
                print(f"✅ caza: {nombre}")
                ok += 1
            else:
                print(f"❌ NO caza: {nombre}\n     esperaba un fallo con «{esperado}», salieron: {fallos or 'ninguno'}")
                fail += 1
        finally:
            os.unlink(tmp)

    # CASOS BUENOS: lo legitimo NO puede disparar el check (caza de falsos positivos).
    for nombre, arreglo, no_esperado in CASOS_BUENOS:
        head2, d = cargar(ruta)
        k = primera_seccion_cl(d)
        d["sections"][k].setdefault("settings", {})
        arreglo(d, k)
        tmp = escribir(head2, d)
        try:
            fallos = autocheck.revisar(tmp, es_base=False)
            falso = [f for f in fallos if no_esperado.lower() in f.lower()]
            if falso:
                print(f"❌ FALSO POSITIVO: {nombre}\n     no debia disparar y disparo: {falso}")
                fail += 1
            else:
                print(f"✅ no dispara (correcto): {nombre}")
                ok += 1
        finally:
            os.unlink(tmp)

    # LA SKILL CONTRA LA SPEC OFICIAL DE PUBLICACION
    print()
    for nombre, paso, detalle in prueba_spec_oficial():
        if paso:
            print(f"✅ {nombre}")
            ok += 1
        else:
            print(f"❌ {nombre}\n     {detalle}")
            fail += 1

    # PRUEBAS DE sellos.py (el otro validador de la skill)
    print()
    for nombre, paso, detalle in pruebas_de_sellos():
        if paso:
            print(f"✅ {nombre}")
            ok += 1
        else:
            print(f"❌ {nombre}\n     salieron: {detalle or 'ningun fallo'}")
            fail += 1

    total = ok + fail
    print(f"\n{'✅' if not fail else '❌'} {ok} de {total} pruebas pasan"
          f"{'' if not fail else f' · {fail} FALLAN'}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
