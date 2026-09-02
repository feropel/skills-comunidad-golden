#!/usr/bin/env python3
"""
GOLDEN SHOPIFY · autocheck.py
Auto-verificacion de cierre EJECUTABLE sobre un product.json generado.

Antes vivia como bloque de codigo dentro de references/auto-check.md, con la ruta
escrita a mano ("RUTA_DEL_PRODUCT_JSON  # <- cambiala"). Un validador que hay que
copiar, pegar y editar cada vez no se corre siempre: se corre cuando uno se acuerda.
Ahora es un archivo que se ejecuta, devuelve codigo de salida y TIENE AUTOPRUEBA
(scripts/autoprueba.py), que es lo que impide que el propio validador se pudra.

USO
  python3 autocheck.py <ruta/al/product.json>          # entrega final (estricto)
  python3 autocheck.py <ruta/al/product.base.json> --base   # plantilla base de la skill

  --base   la plantilla base SI puede llevar la paleta demo y el placeholder
           "PRODUCTO DEMO": son su contenido legitimo, no suciedad. Sin este flag
           esos hallazgos son fallos de verdad.

SALIDA   0 = limpio · 1 = hay fallos · 2 = no se pudo leer/parsear
"""
import json, re, sys

VERSION_CHECKS = 29  # sube cuando agregues un check (y agregale su caso en autoprueba.py)


def cargar(ruta):
    raw = open(ruta, encoding="utf-8").read()
    c = re.match(r'^(/\*.*?\*/\s*)', raw, flags=re.S)
    body = raw[len(c.group(1)):] if c else raw
    return raw, body, json.loads(body, strict=False)


def solo_visible(txt):
    """Lo que de verdad se PUBLICA: sin comentarios de ningun tipo.

    Estaba incompleta y afectaba a CUATRO checks a la vez (DEMO visible, apertura, rayas y
    lenguaje de tienda): solo quitaba `{% comment %}` y dejaba pasar `{%- comment -%}` (con
    guiones de control de espacios, que es como escribe la mitad de esta skill) y los
    comentarios de JavaScript `/* ... */`. Resultado medido: los separadores decorativos que
    los componentes usan para orientar a quien EDITA el codigo — `/* ═══ EDITAR AQUI ═══ */` —
    se leian como rayas publicadas. Buscar la CLASE y no el caso: un arreglo, cuatro checks.
    """
    txt = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', txt, flags=re.S)
    txt = re.sub(r'/\*.*?\*/', '', txt, flags=re.S)          # comentario JS/CSS
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)          # comentario HTML
    return txt


def revisar(ruta, es_base=False):
    """Devuelve la lista de fallos. Lista vacia = limpio."""
    try:
        raw, body, d = cargar(ruta)
    except FileNotFoundError:
        print(f"❌ no existe el archivo: {ruta}"); sys.exit(2)
    except Exception as e:
        print(f"❌ JSON NO parsea: {e}"); sys.exit(2)

    fallos = []
    allcl = "\n".join(
        b.get("settings", {}).get("custom_liquid", "")
        for s in d["sections"].values()
        for b in [s] + list(s.get("blocks", {}).values())
    )

    # 2) Colores DEMO/huerfanos.
    #    OJO (falso positivo medido 2026-09-02): NO son suciedad ni la DEFINICION de la
    #    paleta ({% assign BRAND_PRIMARY = "#b82622" %}) ni el FALLBACK dentro de
    #    var(--brand-primary,#b82622) — este ultimo es justo el patron que la skill EXIGE.
    #    Marcar esos dos hacia 4 avisos falsos en cada corrida, y un validador que siempre
    #    grita en falso ensena a ignorar su salida. Se buscan solo los hex SUELTOS.
    sueltos = re.sub(r'\{%\s*assign\s+[A-Z_]*BRAND[A-Z_]*\s*=\s*"[^"]*"\s*%\}', '', allcl)
    sueltos = re.sub(r'var\(\s*--[a-z0-9-]+\s*,\s*#[0-9a-fA-F]{3,8}\s*\)', '', sueltos)
    for hexd in ["#b82622", "#8e1c19", "#ff5247", "#0F6F5C", "#0B5345", "#0bd4fd"]:
        if re.search(hexd, sueltos, re.I):
            fallos.append(f"color demo/huerfano SUELTO: {hexd} (fuera de la paleta y sin var(--brand-*)) — regla 0-C")

    # 3) Rating nunca 0.0
    if re.search(r'\b0\.0\s*/\s*5', allcl) or '>0.0<' in allcl:
        fallos.append("rating en 0.0/5")

    # 4) CTA tokenizado presente
    if "var(--cta)" not in allcl:
        fallos.append("falta var(--cta) (boton de compra)")

    # 5) Sello de version presente
    if "GOLDEN SHOPIFY" not in allcl and "GFS_VERSION" not in allcl:
        fallos.append("falta el sello de version")

    # 6) Intro Ignition presente
    if "ignition" not in allcl.lower():
        fallos.append("falta el intro IGNITION (sec-ignition.liquid)")

    # 7) Motor Releasit presente
    if "releasit" not in allcl.lower() and "_rsi-buy-now" not in allcl:
        fallos.append("no se detecta el motor Releasit")

    # === ESTANDARES LIQUID ===
    # 8) FAQ accesible
    if "gfs-faq__item" in allcl and "aria-expanded" not in allcl and 'role="button"' not in allcl:
        fallos.append("FAQ sin accesibilidad (falta aria-expanded/role) — estandares-liquid §5")
    imgs = re.findall(r'<img\b[^>]*>', allcl, re.I)
    # 9) lazy
    if any('loading=' not in t.lower() for t in imgs):
        fallos.append('hay <img> sin loading="lazy" — estandares-liquid §4')
    # 10) reduced-motion
    if "@keyframes" in allcl and "prefers-reduced-motion" not in allcl:
        fallos.append("animaciones sin @media (prefers-reduced-motion: reduce) — estandares-liquid §4/§5")
    # 11) alt
    if any('alt=' not in t.lower() for t in imgs):
        fallos.append("hay <img> sin atributo alt — estandares-liquid §7")
    # 12) dimensiones (CLS)
    def _dims(t):
        t = t.lower()
        return ('width=' in t and 'height=' in t) or 'aspect-ratio' in t
    if any(not _dims(t) for t in imgs) and 'aspect-ratio' not in allcl:
        fallos.append("hay <img> sin dimensiones → riesgo CLS — estandares-liquid §6")
    # 13) clases genericas
    if re.search(r'class="(card|title|button|wrapper|container|item|grid|badge|price)"', allcl):
        fallos.append("clase generica sin prefijo → colision con el tema — estandares-liquid §4")

    # === LANDING BLOQUEADA + CERO FOSIL ===
    # 14) copy DEMO fosil
    DEMO = ["energía y vitalidad", "vitalidad y energía", "borojó", "guaraná", "chontaduro",
            "tapa-vaso", "la bebes", "viertes la porción", "máxima energía", "potencia desbloqueada"]
    for w in DEMO:
        if w in allcl.lower():
            fallos.append(f"copy DEMO fosil presente: «{w}» → reescribir por producto (regla 0-B)")
    # 15) candado presente
    if "gfs-lock-landing" not in allcl and "custom_liquid_lock" not in body:
        fallos.append("falta el CANDADO LANDING → el cliente puede irse al home")
    # 24) candado DUPLICADO (medido 2026-09-02 en el propio generador).
    #     G4.0 saco el candado del main a seccion suelta, pero el bloque viejo se quedo:
    #     el base traia el bloque G3.14 dentro de main (1.005 bytes) Y la seccion sec_lock
    #     (2.128 bytes), con contenidos DISTINTOS. No rompe la pagina (ambos hacen
    #     display:none) pero son dos fuentes de verdad: quien edite una deja la otra viva
    #     con el comportamiento anterior. Un candado, un sitio.
    #     OJO: "block" CONTIENE "lock" como substring, asi que un `"lock" in bk` ingenuo
    #     marca cualquier id tipo `..._app_block_xxx`. Se exige "lock" NO precedido de "b".
    _es_lock = lambda s: bool(re.search(r'(?<!b)lock', s.lower()))
    hay_bloque_lock = any(_es_lock(bk) for s in d["sections"].values() for bk in s.get("blocks", {}))
    hay_seccion_lock = any(_es_lock(sk) for sk in d["sections"])
    if hay_bloque_lock and hay_seccion_lock:
        fallos.append("CANDADO DUPLICADO: hay bloque de candado dentro de una seccion Y seccion "
                      "de candado suelta → dejar SOLO la seccion (el bloque es fosil pre-G4.0)")
    # 16) relacionados apagados
    rp = d["sections"].get("related-products")
    if rp and rp.get("disabled") is not True:
        fallos.append("related-products ENCENDIDO → apagar por defecto")
    # 17) fuga {# #}
    if re.search(r'\{#\s', allcl) or re.search(r'\s#\}', allcl):
        fallos.append("comentario {# #} en custom_liquid → se IMPRIME como texto. Usa {% comment %}")
    # 18) texto DEMO visible (la plantilla base SI lo lleva: es su placeholder)
    visible = solo_visible(allcl)
    if not es_base:
        for w in ["PRODUCTO DEMO", "MARCA DEMO"]:
            if w in visible:
                fallos.append(f"texto DEMO visible: «{w}» → revisa configs JS, sticky y titulos")
    # 19) paddings theme-safe
    for s in d["sections"].values():
        st = s.get("settings", {})
        if "padding_top" in st or "padding_bottom" in st:
            fallos.append("hay secciones con padding_top/bottom → Shrine rechaza al guardar. Quitalos.")
            break
    # 20) Ignition con motor de salida
    if "ignition" in allcl.lower() or "gfs-ign" in allcl.lower():
        if "removeChild" not in allcl or "pointer-events:none" not in allcl.replace(" ", ""):
            fallos.append("IGNITION sin motor de salida JS (removeChild + pointer-events:none) → puede quedar MONTADO")
    # 21) tope de 50 KB por setting, en BYTES UTF-8 (los acentos pesan mas de 1 byte)
    for skey, s in d["sections"].items():
        for okey, obj in [(skey, s)] + list(s.get("blocks", {}).items()):
            cl = obj.get("settings", {}).get("custom_liquid", "")
            if not cl:
                continue
            n = len(cl.encode("utf-8"))
            if n >= 50_000:
                fallos.append(f"custom_liquid de «{okey}»: {n} bytes UTF-8 (tope 50.000) → PARTIR (REGLA #5)")
            elif n >= 45_000:
                fallos.append(f"custom_liquid de «{okey}»: {n} bytes UTF-8 (>90% del tope) → partelo ya")

    # 22) G4.9 — DISPARADOR de Chatea byte a byte (regla 0-G).
    #     El mensaje del boton de WhatsApp NO es texto: si apunta al bot debe casar EXACTO
    #     con un disparador registrado, o cae en el tablero "No automatizado" que nadie mira.
    #     Este check nacio de un fallo propio: G4.8 emitia "Hola, quiero informacion de X"
    #     (coma de mas, "y precio" de menos) y no casaba con nada.
    for m in re.finditer(r'(?i)hola,?\s+quiero\s+informaci[oó]n[^"\'<}\n]{0,60}', allcl):
        frag = m.group(0)
        if not re.match(r'(?i)^hola quiero informaci[oó]n y precio de ', frag.strip()):
            fallos.append(f"mensaje de WhatsApp que NO casa con el disparador: «{frag.strip()[:52]}» "
                          f"→ formula exacta 'Hola quiero información y precio de <PRODUCTO>' (regla 0-G)")
            break
    # === REGLAS DURAS DE FER (2026-09-02) — FALLAN, nunca son aviso ===
    #     Clase de fallo medida por golden-verificador en golden-presenta: los validadores
    #     degradan reglas duras a "aviso" y devuelven exit 0. Gana el script, porque es el
    #     que da el semaforo verde, y un entregable que viola una regla de FER pasa la
    #     auditoria. Peor que no tener validador: da confianza falsa.
    #     Aqui era mas grave que una degradacion — **no estaban comprobadas en absoluto**,
    #     ni siquiera como aviso, mientras la documentacion daba por hecho que si.
    # 25) Signos de APERTURA. Regla dura de FER: se escriben solo los de cierre.
    #     Se mira el texto VISIBLE (fuera de comentarios): un comentario del codigo no se
    #     publica, y marcarlo seria el falso positivo que la regla 0-H prohibe.
    visible_txt = solo_visible(allcl)
    apertura = re.findall(r'[¿¡][^\n]{0,40}', visible_txt)
    if apertura:
        fallos.append(f"signo de APERTURA en texto visible ({len(apertura)}): «{apertura[0][:40]}» "
                      "→ regla dura: solo se escriben los de cierre")
    # 26) ACENTOS ROTOS (mojibake). Regla dura: los acentos se verifican EN EL RENDER.
    #     Se buscan las secuencias inequivocas de UTF-8 mal decodificado (Ã©, Ã³, Â…), NO la
    #     ausencia de tildes: exigir tildes daria falsos positivos en marcas y siglas, y un
    #     aviso que grita en falso entrena a ignorar la salida entera.
    roto = re.findall(r'(?:Ã[\x80-\xbf©³¡­±º¼½]|Â[\xa0-\xbf]|â€[\x9c\x9d\x99])', allcl)
    if roto:
        fallos.append(f"ACENTOS ROTOS (mojibake) en {len(roto)} sitios: «{roto[0]}» → el texto se "
                      "publicaria con caracteres corruptos. Revisar codificacion UTF-8")

    # 27) RAYAS SEPARADORAS. Regla dura de FER: nunca lineas separadoras decorativas.
    #     Se exigen TRES O MAS seguidas: una raya em suelta en prosa ("natural — y sin quimicos")
    #     es correcta y marcarla seria el falso positivo que empujaria a escribir peor.
    if re.search(r'[—–─═-]{3,}', visible_txt) or re.search(r'<hr\b', visible_txt, re.I):
        fallos.append("RAYA SEPARADORA en el texto visible (3+ seguidas o <hr>) → regla dura: "
                      "la separacion se hace con espacio y jerarquia, no con lineas")
    # 28) LENGUAJE DE EMPRESA, nunca "tienda". Regla dura de FER.
    tienda = re.findall(r'(?i)\b(?:nuestra|la|esta|mi)\s+tienda\b', visible_txt)
    if tienda:
        fallos.append(f"lenguaje de TIENDA en texto visible ({len(tienda)}): «{tienda[0]}» → "
                      "regla dura: se habla como EMPRESA, no como tienda")
    # 29) CREDENCIALES en el entregable. La skill se comparte con la comunidad y el JSON se
    #     pega en tiendas de clientes: un token filtrado viaja con la plantilla.
    #     Se buscan formas inequivocas de credencial, NO correos: el correo de contacto de una
    #     marca es legitimo en una ficha y marcarlo seria falso positivo.
    cred = re.findall(r'(?:sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|shpat_[a-f0-9]{32}|'
                      r'Bearer\s+[A-Za-z0-9._\-]{20,}|AIza[A-Za-z0-9_\-]{30,})', allcl)
    if cred:
        fallos.append(f"CREDENCIAL en el entregable ({len(cred)}): «{cred[0][:14]}…» → nunca viaja "
                      "un token en la plantilla (se comparte con la comunidad)")

    # 23) WhatsApp: nunca el numero placeholder (regla 0-C: un solo WhatsApp REAL).
    #     En la plantilla base SI es legitimo: ahi es un placeholder por diseno.
    if not es_base and "573001234567" in allcl:
        fallos.append("WhatsApp con el numero PLACEHOLDER 573001234567 → poner el real (regla 0-C)")

    return fallos


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    es_base = "--base" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    fallos = revisar(args[0], es_base)
    modo = "plantilla base" if es_base else "entrega final"
    if fallos:
        print(f"⚠️ REVISAR ({len(fallos)} hallazgos · modo {modo} · {VERSION_CHECKS} checks)\n- " + "\n- ".join(fallos))
        sys.exit(1)
    print(f"✅ LIMPIO · {VERSION_CHECKS} checks corridos · modo {modo}")
    sys.exit(0)


if __name__ == "__main__":
    main()
