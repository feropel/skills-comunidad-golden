#!/usr/bin/env python3
"""
GOLDEN BLINDAJE · chequeo.py
Auditoría de seguridad del PROPIO entorno de agentes (~/.claude).

Revisa lo que ninguna herramienta de código revisa: la configuración con la
que corren los agentes. Secretos escritos a mano, permisos demasiado abiertos,
hooks inyectables, MCP con credenciales, blindaje de skills y caché acumulada.

GARANTÍA DE DISEÑO: CERO SALIDA DE RED.
No importa requests, urllib, http ni socket. Todo se lee y se reporta local.
Esa es la razón de existir de este script frente a las alternativas de
terceros: las que auditan agentes suelen mandar tus archivos afuera.

REGLA DE ORO: nunca imprime el VALOR de un secreto, solo su TIPO y DÓNDE está.
Un reporte que contiene los secretos es tan peligroso como los secretos.

Uso:
  python3 chequeo.py              # reporte en pantalla
  python3 chequeo.py --json       # salida JSON para encadenar
  python3 chequeo.py --cache-dias 15   # umbral de caché vieja (default 15)

Salida: exit 0 si todo bien, exit 1 si hay hallazgos ALTOS.
"""
import os
import re
import sys
import json
import stat
import argparse
from datetime import datetime, timedelta

HOME = os.path.expanduser("~")
CLAUDE = os.path.join(HOME, ".claude")

# Patrones de secretos con FORMATO REAL (prefijo + longitud), no palabras sueltas.
# Buscar la palabra "token" produce cientos de falsos positivos en documentación;
# buscar "shpat_" seguido de 20+ caracteres encuentra un token de verdad.
SECRET_PATTERNS = {
    "Shopify Admin API": r"shpat_[A-Za-z0-9]{20,}",
    "Shopify privada":   r"shppa_[A-Za-z0-9]{20,}",
    "Shopify custom":    r"shpca_[A-Za-z0-9]{20,}",
    "Stripe LIVE":       r"sk_live_[A-Za-z0-9]{20,}",
    "Stripe restringida": r"rk_live_[A-Za-z0-9]{20,}",
    "GitHub PAT":        r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}",
    "OpenAI":            r"sk-[A-Za-z0-9]{45,}",
    "Anthropic":         r"sk-ant-[A-Za-z0-9_-]{40,}",
    "Google API":        r"AIza[A-Za-z0-9_-]{33,}",
    "AWS":               r"AKIA[A-Z0-9]{16}",
    "Slack":             r"xox[baprs]-[A-Za-z0-9-]{20,}",
    "Meta / Facebook":   r"\bEAA[A-Za-z0-9]{80,}",
    "JWT":               r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}",
}

# Un JWT o una cadena larga dentro de estos contextos casi nunca es un secreto:
# son datos de imagen en base64 o fuentes incrustadas. Sin este filtro, un PNG
# incrustado se reporta como token de Meta (pasó en la auditoría de jul-2026).
FALSE_POSITIVE_CONTEXT = re.compile(
    r"data:image/|data:font/|base64,|iVBORw0KGgo|/9j/4AAQSkZ|AAAAB3NzaC1|"
    r"@font-face|\.woff|\.ttf|\.png|\.jpg",
    re.I,
)

# La otra familia de falsos positivos: DOCUMENTACIÓN sobre secretos.
# Una skill que enseña a detectar credenciales (cyber-neo) lleva ejemplos y
# expresiones regulares en sus referencias. Reportarlas como fuga es ruido, y
# el ruido hace que se deje de leer el reporte.
DOC_CONTEXT = re.compile(
    r"ejemplo|example|patr[oó]n|pattern|regex|detect|placeholder|"
    r"no\s+hardcode|nunca\s+pongas|mal:|bad:|❌|\[A-Za-z0-9\]|\{\d+,?\d*\}|"
    r"tu[_-]?token|your[_-]?token|xxx|<[a-z_]+>|\.\.\.",
    re.I,
)

# Cadenas que son claramente relleno, no una credencial real.
PLACEHOLDER = re.compile(
    r"(.)\1{6,}|EXAMPLE|SAMPLE|XXXX|1234567890|ABCDEFGH|TU_|YOUR_|FAKE|DUMMY|TEST",
    re.I,
)


def es_falso_positivo(texto, match, path):
    """Decide si una coincidencia es ruido en vez de una credencial real.

    Se mira el contexto de ambos lados y la pinta del propio valor. Vale más
    dejar pasar un caso dudoso que ahogar el reporte en falsos positivos: un
    reporte con ruido se ignora, y entonces no protege nada.
    """
    ini, fin = match.start(), match.end()
    antes = texto[max(0, ini - 250):ini]
    despues = texto[fin:fin + 120]
    valor = match.group()

    if FALSE_POSITIVE_CONTEXT.search(antes):
        return True
    if PLACEHOLDER.search(valor):
        return True
    # Documentación: la referencia de una skill que habla de secretos.
    if "/references/" in path or path.endswith(".md"):
        if DOC_CONTEXT.search(antes) or DOC_CONTEXT.search(despues):
            return True
    # El valor está dentro de una expresión regular, no es un dato.
    if re.search(r"[\[\]{}\\+*?]", valor):
        return True
    return False

SCAN_EXTS = (".md", ".json", ".py", ".sh", ".js", ".ts", ".mjs", ".yaml",
             ".yml", ".txt", ".env", ".toml", ".zsh", ".bash")

SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv",
             "dist", "build", ".next", "vendor"}

# Reglas de permiso que anulan la confirmación para cualquier comando.
# Una sola de estas convierte al agente en algo que puede hacer lo que sea sin preguntar.
DANGEROUS_ALLOW = [
    (r"^Bash\(\*\)$",            "Bash sin restricción: cualquier comando se auto-aprueba"),
    (r"^Bash\(sudo",             "sudo auto-aprobado"),
    (r"^Bash\(rm\b",             "borrado auto-aprobado"),
    (r"^Bash\(curl[^)]*\|",      "descargar-y-ejecutar auto-aprobado"),
    (r"^Bash\(chmod\s+777",      "permisos 777 auto-aprobados"),
    (r"^Write\(\*\)$",           "escritura sin restricción"),
    (r"^Edit\(\*\)$",            "edición sin restricción"),
    (r"^\*$",                    "TODO auto-aprobado"),
]

RESET = "\033[0m"
COLORS = {"ALTO": "\033[91m", "MEDIO": "\033[93m", "BAJO": "\033[94m", "OK": "\033[92m"}


class Hallazgo:
    def __init__(self, nivel, area, que, donde="", accion=""):
        self.nivel, self.area, self.que = nivel, area, que
        self.donde, self.accion = donde, accion

    def dict(self):
        return {"nivel": self.nivel, "area": self.area, "que": self.que,
                "donde": self.donde, "accion": self.accion}


def leer_json(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return json.load(f)
    except Exception:
        return None


# ─────────────────────────── 1 · SECRETOS ───────────────────────────

def buscar_secretos(hallazgos):
    """Busca credenciales escritas a mano en skills, agentes, comandos y hooks.

    Es el chequeo más importante: una skill se sincroniza al marketplace y se
    comparte con alumnos. Un token adentro se publica con ella.
    """
    raices = ["skills", "agents", "commands", "hooks", "plugins",
              "scheduled-tasks", "CLAUDE.md"]
    escaneados = 0
    encontrados = 0

    for raiz in raices:
        base = os.path.join(CLAUDE, raiz)
        if not os.path.exists(base):
            continue
        recorrido = [(os.path.dirname(base), [], [os.path.basename(base)])] \
            if os.path.isfile(base) else os.walk(base)

        for dp, dn, fn in recorrido:
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in fn:
                if not f.endswith(SCAN_EXTS):
                    continue
                p = os.path.join(dp, f)
                try:
                    if os.path.getsize(p) > 5_000_000:
                        continue
                    texto = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                escaneados += 1

                rel = os.path.relpath(p, CLAUDE)
                for tipo, patron in SECRET_PATTERNS.items():
                    for m in re.finditer(patron, texto):
                        if es_falso_positivo(texto, m, rel):
                            continue
                        hallazgos.append(Hallazgo(
                            "ALTO", "Secretos",
                            f"Credencial {tipo} escrita a mano",
                            rel,
                            "Sácala del archivo y ponla en una variable de entorno. "
                            "Rótala: si la skill ya se sincronizó, se publicó con ella.",
                        ))
                        encontrados += 1
                        break  # un hallazgo por tipo y archivo basta
    return escaneados, encontrados


# ─────────────────────────── 2 · PERMISOS ───────────────────────────

def revisar_permisos(hallazgos):
    for nombre in ("settings.json", "settings.local.json"):
        p = os.path.join(CLAUDE, nombre)
        d = leer_json(p)
        if not d:
            continue

        for regla in d.get("permissions", {}).get("allow", []):
            for patron, explicacion in DANGEROUS_ALLOW:
                if re.search(patron, regla):
                    hallazgos.append(Hallazgo(
                        "ALTO", "Permisos",
                        f"Regla peligrosa: {explicacion}",
                        f"{nombre} → {regla}",
                        "Quítala o acótala a un comando concreto.",
                    ))

        if d.get("skipDangerousModePermissionPrompt") is True:
            hallazgos.append(Hallazgo(
                "MEDIO", "Permisos",
                "skipDangerousModePermissionPrompt activo: el modo sin "
                "confirmaciones no avisa antes de entrar",
                nombre,
                "Es aceptable SOLO si el hook guardián está activo. Verifica el "
                "bloque de Hooks de este mismo reporte.",
            ))

        env = d.get("env", {})
        for k, v in env.items():
            if isinstance(v, str) and len(v) > 20:
                for tipo, patron in SECRET_PATTERNS.items():
                    if re.search(patron, v):
                        hallazgos.append(Hallazgo(
                            "ALTO", "Permisos",
                            f"Credencial {tipo} en la variable de entorno {k}",
                            nombre,
                            "settings.json suele tener permisos de lectura para "
                            "todos. Sácala de ahí.",
                        ))
                        break


# ─────────────────────────── 3 · HOOKS ───────────────────────────

def revisar_hooks(hallazgos):
    """Los hooks corren SOLOS antes o después de cada herramienta.

    Es el punto más sensible de todo el sistema: un hook malicioso no necesita
    que el modelo coopere, se ejecuta por diseño.
    """
    guardian = False
    for nombre in ("settings.json", "settings.local.json"):
        d = leer_json(os.path.join(CLAUDE, nombre))
        if not d:
            continue
        for evento, entradas in (d.get("hooks") or {}).items():
            for entrada in entradas:
                for h in entrada.get("hooks", []):
                    cmd = h.get("command", "")
                    if "golden-careful" in cmd:
                        guardian = True
                    if re.search(r"curl|wget|nc\s|\bssh\b", cmd):
                        hallazgos.append(Hallazgo(
                            "ALTO", "Hooks",
                            f"Hook {evento} hace salida de red",
                            cmd[:90],
                            "Un hook con red puede sacar lo que ve. Revísalo línea a línea.",
                        ))
                    if "|" in cmd and "sh" in cmd:
                        hallazgos.append(Hallazgo(
                            "ALTO", "Hooks",
                            f"Hook {evento} con descargar-y-ejecutar",
                            cmd[:90],
                            "Quítalo.",
                        ))
                    ruta = re.search(r'"?\$?\{?HOME\}?[^"\s]*\.(py|sh|js)', cmd)
                    if ruta:
                        real = ruta.group(0).strip('"').replace("$HOME", HOME) \
                            .replace("${HOME}", HOME)
                        if not os.path.exists(real):
                            hallazgos.append(Hallazgo(
                                "MEDIO", "Hooks",
                                f"Hook {evento} apunta a un archivo que no existe",
                                real,
                                "Restáuralo o quita el hook: hoy no protege nada.",
                            ))

    hooks_dir = os.path.join(CLAUDE, "hooks")
    if os.path.isdir(hooks_dir):
        for f in os.listdir(hooks_dir):
            p = os.path.join(hooks_dir, f)
            if not os.path.isfile(p):
                continue
            modo = os.stat(p).st_mode
            if modo & stat.S_IWOTH:
                hallazgos.append(Hallazgo(
                    "ALTO", "Hooks",
                    "Hook escribible por CUALQUIER usuario del sistema",
                    f"hooks/{f}",
                    f"chmod 755 '{p}' — si otro usuario lo edita, corre con tus permisos.",
                ))

    if not guardian:
        hallazgos.append(Hallazgo(
            "MEDIO", "Hooks",
            "No se detectó el guardián golden-careful",
            "settings.json",
            "Sin él, los comandos destructivos no piden confirmación.",
        ))
    return guardian


# ─────────────────────────── 4 · MCP ───────────────────────────

def revisar_mcp(hallazgos):
    """Los MCP traen las llaves del reino: Shopify, Meta, Stripe, Supabase."""
    for p in (os.path.join(HOME, ".claude.json"), os.path.join(CLAUDE, ".mcp.json")):
        if not os.path.exists(p):
            continue

        modo = os.stat(p).st_mode
        if modo & (stat.S_IRGRP | stat.S_IROTH):
            hallazgos.append(Hallazgo(
                "ALTO", "MCP",
                "El archivo con las credenciales MCP lo puede leer otro usuario",
                os.path.basename(p),
                f"chmod 600 '{p}'",
            ))

        d = leer_json(p)
        if not d:
            continue
        for nombre, cfg in (d.get("mcpServers") or {}).items():
            crudo = json.dumps(cfg)
            for tipo, patron in SECRET_PATTERNS.items():
                if re.search(patron, crudo):
                    hallazgos.append(Hallazgo(
                        "MEDIO", "MCP",
                        f"El MCP '{nombre}' guarda una credencial {tipo} en texto plano",
                        os.path.basename(p),
                        "Esperable si el archivo es 600. Rótala si alguna vez lo compartiste.",
                    ))
                    break
            cmd = str(cfg.get("command", "")) + " " + " ".join(
                str(a) for a in cfg.get("args", []))
            if re.search(r"curl|wget", cmd):
                hallazgos.append(Hallazgo(
                    "ALTO", "MCP",
                    f"El MCP '{nombre}' descarga algo al arrancar",
                    cmd[:90],
                    "Fija la versión o instálalo local.",
                ))


# ─────────────────────────── 5 · BLINDAJE ───────────────────────────

def revisar_blindaje(hallazgos):
    """Las skills golden-* van con chflags uchg para que nada las edite sola."""
    base = os.path.join(CLAUDE, "skills")
    if not os.path.isdir(base):
        return 0, 0
    # Excepciones por diseño: skills que una rutina programada ESCRIBE sola.
    # Blindarlas no las protege, las rompe en silencio (la rutina falla sin avisar).
    # golden-copywriting: la rutina copywriting-tendencias-8-dias le escribe su propio
    # skills/golden-copywriting/references/tendencias-vivas.md cada 8 dias (archivo de
    # esa skill, no de esta). Verificado el 2026-08-19: llevaba 3 dias blindada por
    # seguir el consejo de este mismo chequeo.
    SIN_BLINDAJE_POR_DISENO = {"golden-copywriting"}
    protegidas, abiertas, exentas = 0, [], []
    for d in sorted(os.listdir(base)):
        if not d.startswith("golden-"):
            continue
        skill_md = os.path.join(base, d, "SKILL.md")
        if not os.path.exists(skill_md):
            hallazgos.append(Hallazgo(
                "MEDIO", "Blindaje", f"La skill {d} no tiene SKILL.md", d,
                "Sin SKILL.md la skill no dispara nunca.",
            ))
            continue
        try:
            blindada = bool(os.stat(skill_md).st_flags & 0x00000002)  # UF_IMMUTABLE
        except (AttributeError, OSError):
            continue
        if d in SIN_BLINDAJE_POR_DISENO:
            if blindada:
                exentas.append(d)
            continue
        if blindada:
            protegidas += 1
        else:
            abiertas.append(d)
    if exentas:
        hallazgos.append(Hallazgo(
            "ALTO", "Blindaje",
            f"{len(exentas)} skill(s) blindada(s) que NO deben estarlo",
            ", ".join(exentas),
            "Una rutina programada les escribe: con uchg falla EN SILENCIO. "
            "Desblindar (el directorio primero, luego -R): "
            "chflags nouchg <skill> && chflags -R nouchg <skill> && chmod -R u+w <skill>",
        ))
    if abiertas:
        hallazgos.append(Hallazgo(
            "BAJO", "Blindaje",
            f"{len(abiertas)} skill(s) golden sin blindar",
            ", ".join(abiertas),
            "Normal si la estás editando. Al terminar: "
            "chflags -R uchg ~/.claude/skills/<skill>",
        ))
    return protegidas, len(abiertas)


# ─────────────────────────── 6 · CACHÉ ───────────────────────────

def revisar_cache(hallazgos, dias):
    """El punto ciego real.

    Los resultados de herramientas se guardan tal cual llegan de la API. Si una
    consulta devolvió un token, ese token queda en disco para siempre. Ninguna
    herramienta de terceros mira acá porque no es "configuración".
    """
    proyectos = os.path.join(CLAUDE, "projects")
    if not os.path.isdir(proyectos):
        return {}

    total = viejos = 0
    bytes_total = 0
    con_secreto = []
    limite = datetime.now() - timedelta(days=dias)

    for dp, dn, fn in os.walk(proyectos):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        # Basta con que 'tool-results' esté en la ruta: hay resultados guardados
        # en subcarpetas más abajo, y contarlos solo en el nivel exacto deja
        # archivos fuera del reporte.
        if "tool-results" not in dp.split(os.sep):
            continue
        for f in fn:
            p = os.path.join(dp, f)
            try:
                st = os.stat(p)
            except OSError:
                continue
            total += 1
            bytes_total += st.st_size
            if datetime.fromtimestamp(st.st_mtime) < limite:
                viejos += 1
            try:
                if st.st_size > 20_000_000:
                    continue
                texto = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            rel = os.path.relpath(p, CLAUDE)
            for tipo, patron in SECRET_PATTERNS.items():
                for m in re.finditer(patron, texto):
                    if es_falso_positivo(texto, m, rel):
                        continue
                    con_secreto.append((rel, tipo))
                    break
                else:
                    continue
                break

    gb = bytes_total / 1_073_741_824
    if con_secreto:
        detalle = "; ".join(f"{t} en {os.path.basename(f)}" for f, t in con_secreto[:5])
        hallazgos.append(Hallazgo(
            "MEDIO", "Caché",
            f"{len(con_secreto)} archivo(s) de caché contienen credenciales "
            "devueltas por una API",
            detalle,
            "No salieron de tu equipo, pero no deberían quedarse. Bórralos.",
        ))
    if viejos:
        hallazgos.append(Hallazgo(
            "BAJO", "Caché",
            f"{viejos} archivo(s) de caché con más de {dias} días ({gb:.2f} GB en total)",
            "projects/*/tool-results/",
            f"Limpieza: find ~/.claude/projects -path '*tool-results*' -type f "
            f"-mtime +{dias} -delete",
        ))
    return {"archivos": total, "viejos": viejos, "gb": round(gb, 2),
            "con_secreto": len(con_secreto)}


# ─────────────────────────── REPORTE ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Auditoría local del entorno Claude")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--cache-dias", type=int, default=15)
    args = ap.parse_args()

    if not os.path.isdir(CLAUDE):
        print(f"No existe {CLAUDE}", file=sys.stderr)
        return 2

    hallazgos = []
    escaneados, _ = buscar_secretos(hallazgos)
    revisar_permisos(hallazgos)
    guardian = revisar_hooks(hallazgos)
    revisar_mcp(hallazgos)
    protegidas, abiertas = revisar_blindaje(hallazgos)
    cache = revisar_cache(hallazgos, args.cache_dias)

    altos = sum(1 for h in hallazgos if h.nivel == "ALTO")

    if args.json:
        print(json.dumps({
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "archivos_escaneados": escaneados,
            "skills_blindadas": protegidas,
            "skills_abiertas": abiertas,
            "guardian_activo": guardian,
            "cache": cache,
            "hallazgos": [h.dict() for h in hallazgos],
        }, ensure_ascii=False, indent=2))
        return 1 if altos else 0

    def c(txt, nivel):
        return f"{COLORS.get(nivel, '')}{txt}{RESET}" if sys.stdout.isatty() else txt

    print()
    print("  GOLDEN BLINDAJE · auditoría del entorno de agentes")
    print(f"  {datetime.now():%Y-%m-%d %H:%M}   ·   sin salida de red")
    print()
    print(f"  📂 {escaneados} archivos revisados")
    print(f"  🛡️  {protegidas} skills golden blindadas, {abiertas} abiertas")
    print(f"  🪝 guardián golden-careful: {'activo' if guardian else 'AUSENTE'}")
    if cache:
        print(f"  🗃️  caché: {cache['archivos']} archivos · {cache['gb']} GB")
    print()

    if not hallazgos:
        print(c("  ✅ Sin hallazgos. El entorno está sano.", "OK"))
        print()
        return 0

    for nivel in ("ALTO", "MEDIO", "BAJO"):
        grupo = [h for h in hallazgos if h.nivel == nivel]
        if not grupo:
            continue
        print(c(f"  ── {nivel} ({len(grupo)})", nivel))
        for h in grupo:
            print(f"     {c('•', nivel)} [{h.area}] {h.que}")
            if h.donde:
                print(f"       dónde:  {h.donde}")
            if h.accion:
                print(f"       arreglo: {h.accion}")
        print()

    print(c(f"  {'⛔' if altos else '✅'} {altos} hallazgo(s) de nivel ALTO",
            "ALTO" if altos else "OK"))
    print()
    return 1 if altos else 0


if __name__ == "__main__":
    sys.exit(main())
