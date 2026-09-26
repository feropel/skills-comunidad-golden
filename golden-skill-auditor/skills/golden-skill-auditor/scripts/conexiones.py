"""
conexiones.py — CHEQUEO DE CONEXIONES. Se importa desde validar_arsenal.py.

Encargo de FER (2026-09-03): el auditor tiene que revisar tambien que cada skill
este BIEN CONECTADA, no solo bien redactada y dentro de los topes.

TRES REGLAS QUE EVITAN EL RUIDO, y las tres salieron de medir en vez de suponer.
Sin ellas este chequeo daba 39 "rotas" cuando las rotas de verdad eran CERO:

1. Lo que vive en un COMENTARIO HTML es HISTORIA (changelogs que documentan un
   renombrado). No se juzga: el acta no se reescribe.
2. Una ruta CALIFICADA con la skill dueña en la misma frase es correcta aunque
   el archivo no exista aqui. Ejemplo real y valido:
   `golden-investigacion-mercado` → `references/01-investigacion-360.md`
3. Un nombre tipo golden-* puede ser un AGENTE, una MEMORIA, un prefijo de
   FAMILIA o un token de marca (golden-gold-deep), no solo una skill. Se
   resuelve contra todos esos universos antes de declararlo huerfano.
"""
import os, re, glob

RX_COMENT = re.compile(r"<!--.*?-->", re.S)
RX_RUTA = re.compile(r"(?:\]\(|`)((?:references|scripts|assets)/[A-Za-z0-9_./\-]+)")
RX_NOMBRE = re.compile(r"\b((?:golden|fer)[a-z0-9-]{3,})\b")


def universo(raiz_skills):
    H = os.path.expanduser("~")
    # El universo es SIEMPRE el arsenal instalado, mas lo que haya en la raiz
    # que se este auditando. Una skill puede citar legitimamente a cualquier
    # skill instalada aunque ella viva en otra carpeta (o en un temporal de
    # pruebas): resolver solo contra su vecindario daba falsos positivos.
    skills = {os.path.basename(d.rstrip("/")) for d in glob.glob(raiz_skills + "/*/")}
    skills |= {os.path.basename(d.rstrip("/")) for d in glob.glob(f"{H}/.claude/skills/*/")}
    ag = f"{H}/.claude/agents"
    agentes = {os.path.splitext(f)[0] for f in os.listdir(ag)} if os.path.isdir(ag) else set()
    memoria = set()
    for m in glob.glob(f"{H}/.claude/projects/*/memory"):
        memoria |= {os.path.splitext(f)[0] for f in os.listdir(m)}
    # TODOS los prefijos, no solo uno: "golden-chatea-pro" es familia legitima
    # aunque ninguna skill se llame exactamente asi.
    # Binarios de la casa: ~/.golden/bin/ tiene herramientas reales (golden-transcribe,
    # golden-alarma, golden-bandeja...). Citarlas es correcto y no son skills.
    bindir = f"{H}/.golden/bin"
    binarios = set(os.listdir(bindir)) if os.path.isdir(bindir) else set()
    agentes |= binarios

    familias = set()
    for s in skills:
        partes = s.split("-")
        for i in range(2, len(partes)):
            familias.add("-".join(partes[:i]))
    return skills, agentes, memoria, familias


def sin_historia(texto):
    """Quita los comentarios HTML: ahi vive el changelog, que es historia."""
    return RX_COMENT.sub(" ", texto)


# Prefijo del arsenal propio: `golden-algo` y `golden360`. Sobre estos, la lista de
# excusas en prosa no tiene efecto — su existencia es un hecho comprobable, no una
# opinion del que escribe la frase.
RX_ARSENAL_PROPIO = re.compile(r"^golden(?:360|-[a-z0-9-]+)$")

# NO hay lista de excusas en prosa, ni para el arsenal ni para nada. Hubo una,
# `EXCUSAS_CONDICIONALES`, justificada como "usa `ripgrep` si lo tiene en el PATH".
# Al ir a cubrirla con un caso de banco se vio que esa justificacion era falsa:
# `RX_NOMBRE` solo captura tokens que empiezan por `golden` o `fer`, o sea que el
# detector NUNCA pudo ver una herramienta de terceros. La lista llevaba versiones
# apagando avisos de tokens `fer*` y `golden*` — el universo que esta skill SI
# controla — bajo una coartada que no correspondia a nada.
# LA CLASE: una lista de excepciones cuya justificacion escrita no corresponde a nada
# que el detector pueda ver no cubre ese caso: solo tapa los que si ve.

# NO hay lista de excusas para el arsenal propio, y no debe volver a haberla.
# Hubo una, `DECLARA_INEXISTENCIA`, con la idea de que "planeado, no construido todavia"
# ya reporta el hallazgo. El verificador adversarial la tumbo el mismo dia: era un
# `any(w in frase)` sin ninguna comprobacion, asi que bastaba escribir "planeado" para
# tapar una cita muerta de verdad — y el caso peligroso pasaba igual:
#     "La skill `golden-x` aun no la usamos, pero es la que corre el cierre."
# La frase dice que la skill SE USA y aun asi quedaba exenta.
# LA REGLA: la existencia de una skill se comprueba con os.path.exists, no leyendo un
# adjetivo. Ninguna declaracion en prosa, del signo que sea, sustituye a esa comprobacion.
# Los avisos que esto produce son VERDADEROS (3 en 189 skills, medido) y por eso se dejan.


# NOTA: aqui vivio `_frases_con()`, el cortador de frases que servia a las dos listas
# de excusas. Al borrarlas quedo sin un solo llamador. Un validador no guarda funciones
# "por si acaso": codigo muerto en un validador es de la misma familia que una lista de
# excepciones vacia de contenido — aparenta cubrir algo y no cubre nada. Si vuelve a
# hacer falta cortar por frase, se reescribe con su banco al lado, y el corte reconoce
# fin de frase, parrafo Y vineta (un item de lista es una unidad propia: sin eso, una
# excusa en el ultimo item silenciaba los de arriba).
def _solo_como_variable_css(texto, token):
    """True si TODAS las apariciones del token van precedidas de `--`.

    Con una sola aparicion suelta ya no es sintaxis: es una cita, y se juzga como tal.
    """
    total = len(re.findall(re.escape(token), texto))
    css = len(re.findall(r"--" + re.escape(token), texto))
    return total > 0 and total == css


def revisar_conexiones(dir_skill, univ):
    """Devuelve (fallos, avisos) de conexion."""
    skills, agentes, memoria, familias = univ
    nombre = os.path.basename(dir_skill.rstrip("/"))
    p = os.path.join(dir_skill, "SKILL.md")
    if not os.path.exists(p):
        return [], []
    crudo = open(p, encoding="utf-8", errors="replace").read()
    vivo = sin_historia(crudo)
    fallos, avisos = [], []

    # --- rutas internas ---
    for m in RX_RUTA.finditer(vivo):
        r = m.group(1)
        if os.path.exists(os.path.join(dir_skill, r)):
            continue
        # regla 2: calificada con la skill dueña CERCA — antes o DESPUES.
        # Medido: una ruta seguida de "de golden-investigacion-mercado" nombra
        # al dueño DESPUES de la ruta. Mirar solo hacia atras daba falso positivo.
        # (Sin ruta literal aqui a proposito: un ejemplo con "scripts/" entre
        # comillas confundia a inventario.sh, que lo leia como cita real de ESTA
        # skill y la marcaba rota — bug medido 2026-09-05, ver changelog v1.17.)
        ventana = vivo[max(0, m.start() - 160):m.end() + 160]
        duenos = [d for d in RX_NOMBRE.findall(ventana) if d in skills and d != nombre]
        otras = re.findall(r"`([a-z0-9-]{4,})`", ventana)
        ajena = duenos or [o for o in otras if o in skills and o != nombre]
        if ajena:
            continue  # apunta a archivo de OTRA skill, y lo dice
        fallos.append(f"referencia rota: {r} (no existe y no dice de quien es)")

    # --- nombres de skills/agentes citados ---
    # ANTES de buscar nombres se descuenta el contexto que NO es una cita de skill.
    # Medido 2026-09-03 sobre golden-ads: el detector avisaba de 'golden-09' y
    # 'golden-pro-preset', que son trozos de NOMBRES DE ARCHIVO
    # (PRESET-columnas-golden-09.2025.md, 19-golden-pro-preset.md) y de ANCLAS de
    # indice de Markdown. Medir bien y no descontar el contexto es la misma familia
    # que medir la description sin compararla con nada.
    prosa = re.sub(r"[A-Za-z0-9_./-]*golden[a-z0-9.-]*\.(?:md|py|sh|json|css|js|html)", " ", vivo)
    prosa = re.sub(r"(?m)^#{1,6}[^\n]*$", " ", prosa)          # titulares
    prosa = re.sub(r"\(#[^)]*\)", " ", prosa)                   # anclas de indice
    prosa = re.sub(r"\b\d{1,2}-(?=golden)", " ", prosa)         # prefijo de orden 19-golden-...
    for c in {x.rstrip("-") for x in RX_NOMBRE.findall(prosa)}:
        if c == nombre or c in skills or c in agentes or c in memoria or c in familias:
            continue
        # token de marca o archivo propio (golden-print.css, golden-brand.json…)
        if any(os.path.exists(os.path.join(dir_skill, sub, c + ext))
               for sub in ("assets", "references")
               for ext in (".css", ".json", ".js", ".md", ".png", ".svg")):
            continue
        # La existencia se COMPRUEBA, no se excusa. Un token `golden-*` o `fer*` citado
        # y ausente de ~/.claude/skills es una cita muerta, y ninguna frase la revive.
        if RX_ARSENAL_PROPIO.match(c):
            # Sintaxis, no cita: `--golden-gold` es una variable CSS. Se distingue por
            # el guion doble, no por una lista de nombres permitidos — pero se exige que
            # lo sean TODAS sus apariciones. Antes bastaba una: declarar la variable en
            # cualquier punto del documento tapaba una cita real en otro (F8, medido por
            # el verificador adversarial). Una puerta de alcance DOCUMENTO contradice la
            # doctrina de esta skill, que es que cada mencion se juzga donde vive.
            if _solo_como_variable_css(vivo, c):
                continue
            avisos.append(f"cita '{c}', que parece skill golden y NO existe en el arsenal "
                          f"(una excusa de prosa no la hace existir)")
            continue
        avisos.append(f"cita '{c}', que no resuelve a skill, agente ni memoria (puede ser un token de marca)")

    # --- scripts declarados que no estan ---
    for m in re.finditer(r"`(scripts/[A-Za-z0-9_.\-]+\.(?:py|sh))`", vivo):
        if not os.path.exists(os.path.join(dir_skill, m.group(1))):
            fallos.append(f"script declarado y ausente: {m.group(1)}")

    return fallos, avisos
