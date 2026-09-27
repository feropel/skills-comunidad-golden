#!/usr/bin/env python3
"""
validar_arsenal.py — GUARDIAN DE LA ESPECIFICACION + REGLAS DURAS DE FER.

Nace del fallo del 2026-09-02: el inventario MEDIA la description y NUNCA la
comparaba contra un tope, asi que 33 skills de la casa estaban fuera de norma
y ninguna auditoria lo cazo. Aqui se compara, y ademas se comprueban las
reglas duras de la casa, que ningun validador miraba.

Topes de la spec (agentskills.io/specification, leida 2026-09-02):
  name          1-64, minusculas a-z 0-9 y guiones, sin guion inicial/final,
                sin guiones dobles, y DEBE coincidir con la carpeta.
  description   1-1024  (DURO: si se pasa, la validacion falla)
  compatibility 1-500 si se usa
  cuerpo        <500 lineas es RECOMENDACION, no falla

Reglas duras de FER (aplican a lo que se PUBLICA, aqui a la description):
  - nunca signos de apertura   ¿ ¡
  - acentos correctos: se prohibe el mojibake, NO se exige tilde
  - nunca rayas separadoras de 3+ guiones seguidos
  - lenguaje EMPRESA, no "tienda" refiriendose a la propia

SALIDA:  0 = todo en norma · 1 = hay fallos · 2 = no se pudo leer

Si el validador oficial esta instalado (agentskills), se usa TAMBIEN y su
veredicto manda sobre la spec. Si no esta, se avisa y se aplica el chequeo
propio, declarando que es equivalente pero no oficial.
"""
import os, re, sys, glob, subprocess, shutil
try:
    from conexiones import universo, revisar_conexiones
except ImportError:
    universo = revisar_conexiones = None

TOPE_DESC, TOPE_NAME, TOPE_COMPAT = 1024, 64, 500
CAMPOS_OK = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RX_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RX_MOJIBAKE = re.compile(r"Ã[\x80-\xbf]|Â[\xa0-\xbf]|â€[\x9c\x9d\x99]")
RX_APERTURA = re.compile(r"[¿¡]")
RX_RAYA = re.compile(r"-{3,}|—{2,}")
RX_TIENDA = re.compile(r"\b(nuestra|mi)\s+tienda\b", re.I)


def frontmatter(ruta):
    t = open(ruta, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", t, re.S)
    if not m:
        return None, None, t
    fm = m.group(1)
    campos = {}
    for cm in re.finditer(r"^([a-zA-Z_-]+):\s*(.*?)(?=\n[a-zA-Z_-]+:\s|\Z)", fm, re.S | re.M):
        v = cm.group(2).strip()
        v = re.sub(r"^[>|][-+]?\s*", "", v)
        campos[cm.group(1)] = re.sub(r"\s+", " ", v).strip()
    return fm, campos, t[m.end():]


_UNIV = None


# --- LEY DE LOS REQUISITOS DEL USUARIO (FER, 02-sep-2026; casilla instalada por el CdM el 27-sep) ---
# "Todo lo que necesite intervencion del usuario, ponlo dentro de cada skill, y cuando la vayan a correr
# que le diga: ok, aqui va tu API, ponla aqui, dame estos datos." Vivio 25 dias solo en prosa y paso de
# 20 a 28 skills sin declararlo: lo que no tiene casilla no se cumple. Dos obligaciones:
#   1) DECLARAR ANTES: una seccion de requisitos cerca del principio del SKILL.md  -> si falta, FALLO
#   2) PEDIR AL CORRER: esa seccion dice que hacer si falta algo (parar y pedirlo)  -> si no, AVISO
# Senales de dependencia, estrechas a proposito (una palabra suelta como "token" en prosa NO cuenta):
RX_DEP = [
    # mcp__ccd_* son herramientas de la propia app de escritorio: vienen con ella, el usuario no trae nada
    ("herramientas MCP", re.compile(r"\bmcp__(?!ccd_)[a-z0-9]")),
    ("llave en .secrets/", re.compile(r"\.secrets/")),
    ("credencial por variable de entorno", re.compile(r"environ(?:\.get)?\(\s*['\"][A-Z0-9_]*(?:TOKEN|KEY|SECRET)[A-Z0-9_]*['\"]")),
    ("cabecera de autenticacion", re.compile(r"Authorization['\"]?\s*[:,]\s*f?['\"]Bearer|X-Shopify-Access-Token|dropi-integration-key", re.I)),
    ("programa local", re.compile(r"\b(?:ffmpeg|ffprobe|yt-dlp|whisper)\b")),
]
RX_SECCION = re.compile(r"^#{1,3}\s.*\b(requisitos?|qu[eé] necesitas|antes de (?:empezar|correr|usar))\b", re.I | re.M)
RX_PEDIR = re.compile(r"si (?:falta|no (?:est[aá]|hay|tienes|existe))|p[ií]de(?:lo|la|los)?\b|para y pide|pregunta", re.I)
LINEAS_CABECERA = 80


# Calibracion medida el 27-sep sobre las 43 skills (falsos en las dos direcciones):
#  · un programa local NARRADO en una referencia ("ElevenLabs pone la voz y ffmpeg...") no es dependencia:
#    los programas cuentan solo si los usa el CUERPO de la skill o sus scripts.
#  · los registros de historia (changelog, bitacora) nunca cuentan: citan lo que fue, no lo que se usa.
#  · el archivo que DEFINE este detector lleva sus propios patrones: no se barre (el instrumento no se
#    caza a si mismo).
#  · FALTANTE que se escapaba: la credencial pedida EN PROSA ("el token del workspace"), que es justo
#    como la piden las skills de Chatea. Cuenta si esta en el SKILL.md.
RX_PROSA_CREDENCIAL = re.compile(
    r"\b(?:token|api[ _-]?key|llave|credenciales?)\s+(?:del?|de la)\s+(?:propio\s+)?"
    r"(?:espacio|workspace|cliente|api|chatea|shopify|meta|dropi|heygen|higgsfield|elevenlabs|google|openai|cuenta)\b", re.I)
RX_HISTORIA = re.compile(r"(changelog|bit[aá]cora|historial)", re.I)


def requisitos(dir_skill, cuerpo):
    senales = []
    skill_md = os.path.join(dir_skill, "SKILL.md")
    for ruta in [skill_md] + glob.glob(os.path.join(dir_skill, "scripts", "**", "*"), recursive=True) \
            + glob.glob(os.path.join(dir_skill, "references", "*.md")):
        if not os.path.isfile(ruta) or "__pycache__" in ruta or RX_HISTORIA.search(os.path.basename(ruta)):
            continue
        try:
            t = open(ruta, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if "RX_DEP = [" in t or "REQUISITOS SIN DECLARAR" in t:
            continue   # el detector y su autoprueba llevan los patrones a proposito
        if ruta == skill_md:
            # los sellos de version (comentario html) son historia, no uso
            t = "\n".join(l for l in t.split("\n") if not l.strip().startswith("<!--"))
        es_referencia = os.sep + "references" + os.sep in ruta
        for nombre, rx in RX_DEP:
            if nombre == "programa local" and es_referencia:
                continue
            if nombre not in senales and rx.search(t):
                senales.append(nombre)
        # FALTANTE medido el 27-sep (golden-agenda-citas: Google Calendar). Solo servicios que exigen la CUENTA
        # del usuario; Canva, Notion, Slack o Stripe nombrados como referencia daban 4 falsos de 8.
        if ruta == skill_md and "cuenta de un servicio" not in senales and re.search(
                r"\b(Google Calendar|Gmail|Google Drive|Google Sheets|Mercado Pago)\b", t):
            senales.append("cuenta de un servicio")
        if ruta == skill_md and "credencial pedida en prosa" not in senales and RX_PROSA_CREDENCIAL.search(t):
            senales.append("credencial pedida en prosa")
    if not senales:
        return [], []
    cabecera = "\n".join(cuerpo.split("\n")[:LINEAS_CABECERA])
    m = RX_SECCION.search(cabecera)
    if not m:
        return [f"REQUISITOS SIN DECLARAR: la skill necesita algo del usuario ({', '.join(senales)}) y no tiene "
                f"seccion de requisitos en sus primeras {LINEAS_CABECERA} lineas (ley de FER del 02-sep: declarar "
                f"antes y pedir al correr)"], []
    seccion = cabecera[m.start():]
    sig = re.search(r"^#{1,3}\s", seccion[1:], re.M)
    seccion = seccion[:sig.start() + 1] if sig else seccion
    if not RX_PEDIR.search(seccion):
        return [], ["la seccion de requisitos no dice que hacer si falta algo (pedir al correr: parar y pedirlo con nombre propio)"]
    return [], []


def revisar(dir_skill):
    """Devuelve (fallos, avisos). Fallos rompen; avisos informan."""
    nombre = os.path.basename(dir_skill.rstrip("/"))
    p = os.path.join(dir_skill, "SKILL.md")
    fallos, avisos = [], []
    if not os.path.exists(p):
        return ["falta SKILL.md"], []
    fm, campos, cuerpo = frontmatter(p)
    if fm is None:
        return ["sin frontmatter YAML"], []

    # --- spec ---
    n = campos.get("name", "")
    if not n:
        fallos.append("falta el campo name")
    else:
        if n != nombre:
            fallos.append(f"name '{n}' no coincide con la carpeta '{nombre}' (la skill NO CARGA)")
        if len(n) > TOPE_NAME:
            fallos.append(f"name de {len(n)} chars (tope {TOPE_NAME})")
        if not RX_NAME.match(n):
            fallos.append(f"name '{n}' con formato invalido (minusculas, digitos y guiones simples)")
    d = campos.get("description", "")
    if not d:
        fallos.append("falta el campo description")
    elif "<" in d or ">" in d:
        # Regla del validador OFICIAL local (skill-creator/scripts/quick_validate.py):
        # la description no admite angulares. Medido 2026-09-03: golden-shopify caia
        # por un literal `product.<tema>.json` con la description en 1010 chars, o sea
        # DENTRO del tope. El CdM no lo veia porque su validador no tenia esta regla.
        fallos.append("la description contiene ANGULARES (< o >), prohibidos por la spec; "
                      "escribe el marcador sin ellos (product.tema.json)")
    elif len(d) > TOPE_DESC:
        fallos.append(f"description de {len(d)} chars (tope DURO {TOPE_DESC}, sobra {len(d)-TOPE_DESC})")
    c = campos.get("compatibility", "")
    if c and len(c) > TOPE_COMPAT:
        fallos.append(f"compatibility de {len(c)} chars (tope {TOPE_COMPAT})")
    extra = set(campos) - CAMPOS_OK
    if extra:
        fallos.append(f"campos no permitidos en frontmatter: {sorted(extra)}")

    # --- reglas duras de FER sobre la description ---
    if d:
        if RX_APERTURA.search(d):
            fallos.append("signo de APERTURA en la description (regla dura: solo los de cierre)")
        if RX_MOJIBAKE.search(d):
            fallos.append("ACENTOS ROTOS (mojibake) en la description")
        if RX_RAYA.search(d):
            fallos.append("RAYA SEPARADORA en la description")
        # La regla EMPRESA-no-tienda juzga como habla GOLDEN, no las frases que
        # el CLIENTE dice y que aqui se citan como disparadores. Por eso se
        # ignoran los tramos entrecomillados antes de buscar.
        sin_citas = re.sub(r'"[^"]*"', " ", d)
        if RX_TIENDA.search(sin_citas):
            avisos.append("dice 'nuestra/mi tienda' fuera de una cita (regla: se habla como EMPRESA)")

    # --- conexiones (encargo de FER 2026-09-03: que este BIEN CONECTADA) ---
    if revisar_conexiones and _UNIV is not None:
        fc, ac = revisar_conexiones(dir_skill, _UNIV)
        fallos += fc
        avisos += ac

    # --- ley de los requisitos del usuario ---
    fr, ar = requisitos(dir_skill, cuerpo)
    fallos += fr
    avisos += ar

    # --- recomendaciones ---
    lineas = cuerpo.count("\n") + 1
    if lineas > 500:
        avisos.append(f"cuerpo de {lineas} lineas (recomendado <500; encarece la activacion, no falla)")
    return fallos, avisos


def oficial(dir_skill, binario):
    r = subprocess.run([binario, "validate", dir_skill], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    solo_casa = "--casa" in sys.argv
    # 🔴 TODAS las rutas que se pasan, no solo la primera (26-sep, CdM). Con
    # `validar_arsenal.py ~/.claude/skills/golden-*` el shell entrega 41 rutas y el script
    # revisaba solo args[0]: imprimia "UNIVERSO: 1 · 1 de 1 sanas" y salia 0 sobre 41 skills.
    # Un verde sobre un universo que el que lo corre no eligio.
    raices = args or [os.path.expanduser("~/.claude/skills")]
    raiz = raices[0] if len(raices) == 1 else os.path.dirname(os.path.commonpath(raices)) or "/"
    dirs, vistos = [], set()
    for r in raices:
        if not os.path.exists(r):
            print("no existe la ruta:", r); return 2
        if os.path.exists(os.path.join(r, "SKILL.md")):
            encontrados = [r]
        else:
            # BARRIDO RECURSIVO, no de un solo nivel.
            # Medido 2026-09-03: el patron '*/SKILL.md' se saltaba 20 skills ANIDADAS
            # dentro del plugin claude-ads (claude-ads/ads/ y claude-ads/skills/ads-*).
            # No fallaban: NI SE MIRABAN. El instrumento no reportaba rojo, reportaba
            # MENOS FILAS — la trampa de conteo en su forma mas silenciosa.
            encontrados = [os.path.dirname(sk) + "/" for sk in
                           sorted(glob.glob(r + "/**/SKILL.md", recursive=True))]
            if not encontrados and os.path.isdir(r):
                # Un directorio que existe pero no tiene SKILL.md ni skills hijas es una
                # skill INCOMPLETA, no una ruta ilegible: eso es FALLO, no error de lectura.
                encontrados = [r]
        for d in encontrados:
            if d.rstrip("/") not in vistos:
                vistos.add(d.rstrip("/"))
                dirs.append(d)
    if solo_casa:
        dirs = [d for d in dirs if os.path.basename(d.rstrip("/")).startswith(("golden", "fer-"))]
    if not dirs:
        print("no existe la ruta:", raiz); return 2

    global _UNIV
    if universo:
        _UNIV = universo(os.path.dirname(dirs[0].rstrip("/")) if len(dirs) == 1 else raiz)
    # El validador OFICIAL LOCAL de skill-creator siempre esta instalado y es la
    # fuente autoritativa de publicacion. Se usa SIEMPRE; el de PyPI, si aparece.
    local = os.path.expanduser("~/.claude/skills/skill-creator/scripts/quick_validate.py")
    oficial_local = local if os.path.exists(local) else None
    binario = shutil.which("agentskills")
    print(f"VALIDADOR OFICIAL LOCAL: {'si' if oficial_local else 'NO ENCONTRADO'}")
    print(f"VALIDADOR OFICIAL: {'si, ' + binario if binario else 'NO INSTALADO (se usa el chequeo propio, equivalente pero no oficial)'}")
    print(f"UNIVERSO: {len(dirs)} skills\n")

    con_fallo = con_aviso = 0
    for d in dirs:
        n = os.path.basename(d.rstrip("/"))
        fallos, avisos = revisar(d)
        if oficial_local:
            r = subprocess.run([sys.executable, oficial_local, os.path.abspath(d)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                for l in (r.stdout + r.stderr).splitlines():
                    l = l.strip(" -")
                    if l and "valid" not in l.lower() and l not in fallos:
                        fallos.append("[oficial-local] " + l)
        if binario:
            rc, salida = oficial(d, binario)
            if rc != 0:
                for l in salida.splitlines():
                    l = l.strip(" -")
                    if l and not l.startswith("Validation failed") and l not in fallos:
                        fallos.append("[oficial] " + l)
        if fallos:
            con_fallo += 1
            print(f"FALLA  {n}")
            for f in fallos: print(f"         - {f}")
        elif avisos:
            con_aviso += 1
            print(f"aviso  {n}")
            for a in avisos: print(f"         · {a}")
    sanas = len(dirs) - con_fallo - con_aviso
    print(f"\nCOBERTURA: {len(dirs)} de {len(dirs)} revisadas · sanas {sanas} · con aviso {con_aviso} · CON FALLO {con_fallo}")
    return 1 if con_fallo else 0


if __name__ == "__main__":
    sys.exit(main())
