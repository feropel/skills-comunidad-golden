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


# P65 (28-sep, CdM, reportado por la fabrica de golden-logistica-diaria): una skill que
# documenta una TRAMPA citando una ruta que a proposito NO debe existir ("cuidado:
# `scripts/__pycache__/` no debe existir en el repo publicado") salia con "referencia
# rota" — penaliza documentar bien. PERO este archivo ya mato DOS listas de excusas en
# prosa por la misma razon: un `any(palabra in frase)` sin comprobacion deja tapar una
# cita muerta real con cualquier frase que contenga la palabra magica (ver DECLARA_
# INEXISTENCIA y EXCUSAS_CONDICIONALES arriba). La leccion de la casa no es "no hagas
# excepciones por prosa", es "una excepcion por prosa nunca es SILENCIOSA": se REPORTA
# igual, solo que como AVISO en vez de FALLO — visible, no tapado — y el marcador es una
# lista CERRADA de frases que afirman un ESTADO comprobable ("no debe existir", "se
# borra"), nunca un adjetivo de intencion ("planeado", "opcional") que ya se demostro
# manipulable. Sigue mordiendo una referencia rota real: solo baja su severidad cuando
# la propia frase, y nada mas que la frase que contiene la cita, declara la ausencia.
_RX_LIMITE_FRASE = re.compile(r"[.!?](?:\s|$)|\n[ \t]*\n|\n[ \t]*[-*][ \t]|\n[ \t]*\d+[.)][ \t]")
RX_NEGACION_RUTA = re.compile(
    r"no\s+debe\s+existir|nunca\s+debe\s+(?:existir|estar)|no\s+exist[ei]|"
    r"si\s+aparece|se\s+borra|se\s+elimina|jam[aá]s\s+debe\s+existir", re.I)


def _limites_frase(vivo, inicio, fin):
    """(ini, final): posiciones absolutas de la frase (o vineta, o parrafo) que contiene
    el tramo [inicio, fin), ni una letra mas."""
    ini = 0
    for m in _RX_LIMITE_FRASE.finditer(vivo, 0, inicio):
        ini = m.end()
    m = _RX_LIMITE_FRASE.search(vivo, fin)
    final = m.start() if m else len(vivo)
    return ini, final


def _niega_esta_cita(vivo, inicio, fin):
    """True solo si el marcador de negacion esta CERCA de ESTA cita en particular, no de
    cualquier otra que comparta la misma frase. Medido (28-sep): sin esta ventana local,
    "`temporal.py` no debe existir, y aparte corre `real.py` siempre" callaba las DOS —
    el mismo contagio por proximidad que ya se cazo dos veces en este archivo, ahora
    dentro de una frase en vez de entre frases. La frase sigue siendo el TECHO: la
    ventana nunca cruza a la frase vecina."""
    frase_ini, frase_fin = _limites_frase(vivo, inicio, fin)
    ventana = vivo[max(frase_ini, inicio - 20):min(frase_fin, fin + 20)]
    return bool(RX_NEGACION_RUTA.search(ventana))


def _dueno_ajeno(dir_skill, skills, nombre, vivo, inicio, fin, r):
    """Regla 2 del modulo: una ruta calificada con la skill dueña CERCA (antes o DESPUES)
    es correcta aunque el archivo no exista AQUI — pero solo si de verdad esta ALLA.
    Devuelve (ajena, confirmada): ajena = lista de dueños candidatos citados cerca (vacia
    si ninguno); confirmada = True si el archivo r existe de verdad en algun candidato.

    P59 (27-sep, medido: SKILL.md con dos rutas inexistentes junto a "golden-shopify" daba
    0 fallos y 0 avisos, sin comprobar nada). Nombrar al dueño no basta: se confirma que el
    archivo EXISTE ahi. El dueño citado puede vivir junto a esta skill (fixtures de prueba,
    otro arsenal) o ser una skill YA INSTALADA en ~/.claude/skills — universo() resuelve
    nombres contra los dos sitios, y esta comprobacion mira en los mismos dos."""
    ventana = vivo[max(0, inicio - 160):fin + 160]
    duenos = [d for d in RX_NOMBRE.findall(ventana) if d in skills and d != nombre]
    otras = re.findall(r"`([a-z0-9-]{4,})`", ventana)
    ajena = duenos or [o for o in otras if o in skills and o != nombre]
    if not ajena:
        return [], False
    raices = {os.path.dirname(dir_skill.rstrip("/")), os.path.expanduser("~/.claude/skills")}
    confirmada = any(os.path.exists(os.path.join(raiz, d, r)) for raiz in raices for d in ajena)
    return ajena, confirmada


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
        # (Sin ruta literal en el comentario de este bloque a proposito: un ejemplo con
        # "scripts/" entre comillas confundia a inventario.sh, que lo leia como cita real
        # de ESTA skill y la marcaba rota — bug medido 2026-09-05, ver changelog v1.17.)
        ajena, confirmada = _dueno_ajeno(dir_skill, skills, nombre, vivo, m.start(), m.end(), r)
        if ajena:
            if confirmada:
                continue  # apunta a archivo de OTRA skill, y el archivo SI esta ahi
            fallos.append(
                f"referencia rota: {r} (dice ser de {'/'.join(ajena)} pero el archivo no existe ahi)")
            continue
        if _niega_esta_cita(vivo, m.start(), m.end()):
            avisos.append(f"cita '{r}' que su propia frase declara que NO debe existir "
                          f"(confirmar a mano que es una trampa documentada, no una cita muerta)")
            continue
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
    # P48 (27-sep): `~/.golden-rembg` es una CARPETA (el venv de rembg), no una cita a una skill
    # `golden-rembg`. Ninguna skill empieza por punto, asi que una ruta con `/.golden-` es sintaxis de
    # carpeta. Se decide por la forma y no por si existe en este Mac: en el equipo de otro no existira.
    prosa = re.sub(r"(?:~|\$HOME)?/\.golden[\w.-]*", " ", prosa)
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
        r = m.group(1)
        if os.path.exists(os.path.join(dir_skill, r)):
            continue
        # Mismo hueco que las rutas internas y por la misma regla 2 (encontrado probando
        # el arreglo de arriba, no en el expediente P59): este chequeo nunca aplicaba la
        # excusa de "calificada con la skill dueña", y un script real de una hermana, citado
        # con su nombre completo, salia igual como ausente. (Sin ruta literal aqui a
        # proposito, misma leccion que arriba: un ejemplo entre comillas confunde a
        # inventario.sh, que lo lee como cita real de ESTA skill.)
        ajena, confirmada = _dueno_ajeno(dir_skill, skills, nombre, vivo, m.start(), m.end(), r)
        if ajena:
            if confirmada:
                continue
            fallos.append(f"script declarado y ausente: {r} (dice ser de {'/'.join(ajena)} pero no esta ahi)")
            continue
        if _niega_esta_cita(vivo, m.start(), m.end()):
            avisos.append(f"cita '{r}' que su propia frase declara que NO debe existir "
                          f"(confirmar a mano que es una trampa documentada, no un script ausente de verdad)")
            continue
        fallos.append(f"script declarado y ausente: {r}")

    return fallos, avisos
