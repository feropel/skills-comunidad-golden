#!/usr/bin/env python3
"""
CANDADO MAESTRO (FASE 9) — verifica que el paquete de lanzamiento esté COMPLETO.
Uso:  python3 candado.py <carpeta PROYECTOS/<PRODUCTO>>          → verifica artefactos
      python3 candado.py --skills                                 → verifica skills hijas instaladas
      python3 candado.py --autochequeo                            → la skill se revisa a sí misma
Salida: checklist ✅/❌ + conteo de [PENDIENTE]. Exit 0 si completo, 1 si falta algo.
Si este script no puede correr (sin python3), haz el checklist a mano con la lista de la Fase 9.

Numeración canónica del pipeline R1.0 (manda SKILL.md): -1 forense · 0 intake · 0.5 reconocimiento ·
1 investigación · 2 documento || C1 VIABILIDAD || 3 SEO · 4 destino de venta · 5 creativos ||
C2 VERACIDAD || 6 orgánico · 7 pauta · 8 bot · 9 paquete || C3 MONTAJE || C4 QA || 10 seguimiento ·
11 retro.
"""
import glob
import json
import os
import re
import sys

SKILLS_DIR = os.path.expanduser("~/.claude/skills")

# Skills hijas del pipeline (nombre → para qué). Mantener alineado con REQUISITOS de SKILL.md.
HIJAS = {
    "golden-brand-brain": "cerebro de marca — Paso 0, obligatorio ANTES de generar",
    "golden-investigacion-mercado": "Bloque 1 completo: forense + investigación + dossier + .docx",
    "golden-shopify": "página COD (Fase 4)",
    "golden-web": "sitio/landing no-COD (Fase 4, alternativa)",
    "golden-agenda-citas": "agenda de citas (Fase 4, servicios)",
    "golden-imagen-arena": "imágenes/GIF de producto por API (Fase 5)",
    "golden-ugc-avatar": "video/avatar UGC (Fase 5)",
    "golden-video-teardown": "desarmar cada video antes de escribir su copy (Fase 5B)",
    "golden-ads": "pauta Meta+TikTok+Google (Fase 7) + seguimiento (Fase 10)",
    "golden-copywriting": "copys 5/5/5 y textos de orgánico (Fases 6-7)",
    "golden-chatea-pro-prompt-ventas": "venta WhatsApp del producto (Fase 8)",
    "golden-chatea-pro-config-comentarios": "comentarios del producto (Fase 8)",
    "golden-dropkiller-productos-ganadores": "validar demanda (Compuerta 1)",
    "golden-meta-ads-analysis": "auditar pauta previa (Fase 0.5)",
    "golden-pdf-check": "PDF Golden del paquete (Fase 9)",
    # golden-qa es un AGENTE (Agent tool), no una skill instalada — no se chequea aquí.
}

# Auxiliares de la Fase 0.5 (reconocimiento). Su ausencia NO degrada el pipeline: se sustituyen por
# lectura manual del disco / de los informes. Se reportan aparte para no gritar ❌ por algo opcional.
AUXILIARES = {
    "golden-archivos": "inventario de archivos del producto (Fase 0.5)",
    "golden-dropi-analisis": "pedidos reales = fuente reina de demografía (Fase 0.5)",
}

# Skills que NO forman parte del ecosistema publicado: son del dueño y operan una cuenta
# personal suya. Si no están, NO es un hueco — el pipeline las sustituye por su equivalente
# de HIJAS. Listarlas como faltantes hacía que un alumno con el ecosistema completo viera
# "❌ NO instalada" y creyera que le faltaba algo. (Corregido 2026-07-27.)
SOLO_DEL_DUENO = {
    "golden-ecom-magic": "imágenes por navegador — se sustituye por golden-imagen-arena (API)",
}

# Artefactos del paquete (patrón glob → descripción). El README y el .docx son obligatorios;
# /creativos puede traer solo prompts (warn, no falla).
ARTEFACTOS = [
    ("PRODUCTO.json", "Expediente único del producto (columna vertebral)", True),
    ("*.docx", "Documento maestro Word REAL (Fase 2)", True),
    ("*DOSSIER*.md", "Dossier psicológico 30 capas (Fase 1; válido si vive DENTRO del .docx)", False),
    ("product*.json", "Destino de venta JSON de golden-shopify (si es golden-web: enlace en README)", False),
    ("PAUTA*.md", "Pauta Meta+TikTok+Google de golden-ads (Fase 7)", True),
    ("ORGANICO*.md", "Contenido orgánico por canal (Fase 6)", True),
    ("CHATEA-PRO*.md", "Chatea PRO del producto — 2 piezas (Fase 8)", True),
    ("README.md", "Índice + checklist de lanzamiento (Fase 9)", True),
    ("creativos", "Carpeta /creativos (recursos o prompts)", False),
    ("*.pdf", "PDF Golden del paquete (Fase 9, golden-pdf-check)", False),
]


def check_producto_json(carpeta: str) -> int:
    """G4.0: valida el expediente PRODUCTO.json — compuertas pasadas y nulls honestos."""
    ruta = os.path.join(carpeta, "PRODUCTO.json")
    if not os.path.isfile(ruta):
        return 0  # su ausencia ya la reporta ARTEFACTOS como obligatorio
    fallos = 0
    try:
        exp = json.load(open(ruta, encoding="utf-8"))
    except Exception as e:
        print(f"  ❌ PRODUCTO.json ilegible: {e}")
        return 1
    estado = exp.get("estado", {}) or {}
    pasadas = estado.get("compuertas_pasadas", []) or []
    pendientes = [str(p).lower() for p in (estado.get("pendientes", []) or [])]
    # Compuertas mínimas para que el PAQUETE pueda entregarse (montaje y qa vienen al encender)
    for c in ("viabilidad", "veracidad"):
        if c in pasadas:
            print(f"  ✅ Compuerta pasada: {c}")
        else:
            print(f"  ❌ COMPUERTA SIN PASAR: {c} — el paquete NO puede entregarse")
            fallos += 1
    # Nulls honestos: todo null/vacío crítico debe estar declarado en estado.pendientes
    criticos = []
    for k, v in (exp.get("negocio", {}) or {}).items():
        if v is None:
            criticos.append(f"negocio.{k}")
    act = exp.get("activacion", {}) or {}
    for k in ("keyword_bot", "whatsapp"):
        if not act.get(k):
            criticos.append(f"activacion.{k}")
    sin_declarar = [c for c in criticos if not any(c.split('.')[-1] in p for p in pendientes)]
    if sin_declarar:
        print(f"  ❌ Campos críticos en null/vacío SIN declarar en estado.pendientes: {', '.join(sin_declarar)}")
        fallos += 1
    elif criticos:
        print(f"  ⚠️  {len(criticos)} campo(s) crítico(s) en null — declarados como pendientes (honesto)")
    if act.get("cargado_en_bot") is False and act.get("keyword_bot"):
        print("  ⚠️  cargado_en_bot=false → el botón de WhatsApp queda BLOQUEADO hasta que el bot escuche el trigger")
    return fallos


def check_creativos(carpeta: str) -> None:
    """Fase 5 es puerta dura: cada pieza existe como ARCHIVO o como PROMPT completo.
    El GIF de demostración se pide explícitamente en la Fase 5, así que se busca aparte: es la pieza
    que más se olvida y la que más levanta la conversión en la escalera. Solo advierte (un GIF
    entregado como prompt es válido mientras no haya créditos)."""
    carp = os.path.join(carpeta, "creativos")
    piezas = []
    if os.path.isdir(carp):
        for raiz, _dirs, archivos in os.walk(carp):
            piezas += [os.path.join(raiz, a) for a in archivos if not a.startswith(".")]
    texto_md = ""
    for f in glob.glob(os.path.join(carpeta, "*.md")):
        texto_md += open(f, encoding="utf-8", errors="ignore").read().lower()
    if piezas:
        print(f"  ✅ /creativos con {len(piezas)} pieza(s) entregada(s)")
    elif "prompt" in texto_md:
        print("  ⚠️  /creativos sin archivos — válido solo si TODAS las piezas están como PROMPT completo")
    else:
        print("  ❌ Fase 5 vacía: ni archivos en /creativos ni prompts en el paquete — sin creativo no hay campaña")
    tiene_gif = any(p.lower().endswith(".gif") for p in piezas) or "gif" in texto_md
    print(f"  {'✅' if tiene_gif else '⚠️ '} GIF de demostración (Fase 5): {'presente' if tiene_gif else 'AUSENTE — archivo o prompt'}")


def check_paquete(carpeta: str) -> int:
    if not os.path.isdir(carpeta):
        print(f"❌ La carpeta no existe: {carpeta}")
        return 1
    fallos = 0
    print(f"═══ CANDADO MAESTRO · {os.path.basename(carpeta)} ═══")
    for patron, desc, obligatorio in ARTEFACTOS:
        hits = glob.glob(os.path.join(carpeta, patron))
        if patron == "PAUTA*.md" and not hits:
            # convención alterna: golden-ads entrega en subcarpeta ADS/
            hits = [d for d in glob.glob(os.path.join(carpeta, "ADS")) if os.path.isdir(d) and os.listdir(d)]
        if hits:
            print(f"  ✅ {desc}  ({os.path.basename(hits[0])})")
        elif obligatorio:
            print(f"  ❌ FALTA: {desc}  (patrón {patron})")
            fallos += 1
        else:
            print(f"  ⚠️  Opcional ausente: {desc}")

    # Fase 5: creativos completos (archivo o prompt) + el GIF que siempre se olvida
    check_creativos(carpeta)

    # Fase 8: el CHATEA-PRO debe traer las 2 piezas (venta + comentarios)
    for f in glob.glob(os.path.join(carpeta, "CHATEA-PRO*.md")):
        txt = open(f, encoding="utf-8", errors="ignore").read().lower()
        tiene_venta = "venta" in txt and ("prompt de venta" in txt or "saludo" in txt)
        tiene_comentarios = "comentario" in txt
        if not (tiene_venta and tiene_comentarios):
            faltan = [n for ok, n in [(tiene_venta, "VENTA"), (tiene_comentarios, "COMENTARIOS")] if not ok]
            print(f"  ❌ {os.path.basename(f)} incompleto: falta pieza {' y '.join(faltan)} (Fase 8 = 2 piezas)")
            fallos += 1
        else:
            print(f"  ✅ Fase 8 con sus 2 piezas (venta + comentarios)")

    # Pendientes marcados (válidos, pero se reportan)
    pendientes = 0
    for f in glob.glob(os.path.join(carpeta, "*.md")):
        pendientes += len(re.findall(r"\[(?:[A-ZÁÉÍÓÚÑ ]*PENDIENTE[A-ZÁÉÍÓÚÑ ]*|PARCIAL[^\]]*)\]",
                                     open(f, encoding="utf-8", errors="ignore").read()))
    print(f"  📌 Marcadores [PENDIENTE]/[PARCIAL]: {pendientes} (válidos si están listados en el README)")

    # Expediente único: compuertas + nulls honestos
    fallos += check_producto_json(carpeta)

    print("═══ RESULTADO:", "✅ PAQUETE COMPLETO" if fallos == 0 else f"❌ {fallos} artefacto(s) faltante(s) — la fase NO cierra", "═══")
    print("⛔ COMPUERTA 3 · MONTAJE: la entrega cierra preguntando 'Deseas que lo monte?' +")
    print("   pidiendo precios/combos reales, WhatsApp, costo y marca. NUNCA montar con precios del estudio.")
    print("⛔ COMPUERTA 4 · QA: aunque el paquete cierre, nada se ENCIENDE sin el QA pre-encendido")
    print("   (render 390/768/PC, botón que dispara el bot, orden de prueba, pixel+CAPI probado).")
    return 0 if fallos == 0 else 1



# ── AUTOCHEQUEO DE LA PROPIA SKILL ──────────────────────────────────────────────
# Por qué existe: tres veces se rompió lo mismo por vivir SOLO en prosa que nadie verifica.
#   (1) 2026-08-07 y (2) 2026-09-03: al recortar la description por el tope del listado se
#       borraron las FRONTERAS con las hermanas — justo lo que evita que un orquestador se
#       dispare cuando el usuario quería una pieza suelta.
#   (3) R1.8 y la adenda del cerebro se sellaron sin entrada de changelog.
# Una regla que no se puede correr no es una regla: es un buen propósito. Esto la vuelve candado.
# DOS techos distintos, y confundirlos invalida la skill (pasó aquí el 2026-09-05):
#   1024 = LÍMITE DE VALIDACIÓN de la especificación. DURO: por encima, `agentskills validate`
#          sale con código 1 y la skill NO ES VÁLIDA. Es el que manda.
#   ~1536 = truncado de RUNTIME: donde el motor corta al cargar el listado. Otra cosa. NO decide
#          validez, y usarlo como tope deja pasar una skill que el validador rechaza.
TOPE_DESCRIPTION = 1024

def check_autochequeo() -> int:
    import io
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill = os.path.join(base, "SKILL.md")
    fallos = 0
    print("═══ AUTOCHEQUEO · la skill se revisa a sí misma ═══")
    if not os.path.isfile(skill):
        print("  ❌ no encuentro SKILL.md"); return 1
    txt = open(skill, encoding="utf-8").read()

    # 0 · el VALIDADOR OFICIAL manda: si él dice que no, no hay nota que discutir
    import shutil, subprocess
    oficial = shutil.which("agentskills")
    if oficial:
        r = subprocess.run([oficial, "validate", base], capture_output=True, text=True)
        ok = r.returncode == 0
        print(f"  {'✅' if ok else '❌'} validador oficial (agentskills validate): exit {r.returncode}")
        if not ok:
            for linea in (r.stdout + r.stderr).strip().splitlines()[:4]:
                print(f"      {linea.strip()}")
            fallos += 1
    else:
        print("  ⚠️  `agentskills` no está en PATH — se valida solo con el conteo propio (respaldo)")

    # 1 · description: existe, cabe en el tope DURO y CONSERVA las fronteras
    m = re.search(r"^description: >-?\n((?:  .*\n)+)", txt, re.M)
    if not m:
        print("  ❌ sin description en el frontmatter"); fallos += 1
    else:
        plano = " ".join(l.strip() for l in m.group(1).strip().split("\n"))
        print(f"  {'✅' if len(plano) <= TOPE_DESCRIPTION else '❌'} largo: {len(plano)} de {TOPE_DESCRIPTION} (límite DURO de la spec)")
        fallos += 0 if len(plano) <= TOPE_DESCRIPTION else 1
        # La frontera se reconoce por SENTIDO, no por un carácter: un "NO es para X" que además
        # dice a dónde va lo que no es de esta skill. Atarlo a la flecha "→" era frágil — al
        # recortar por el tope de 1024 desapareció la flecha y el chequeo gritó un falso rojo.
        # MIRAR LA COSA, NO EL VECINDARIO (fallo medido del CdM el 2026-09-05: probaba el
        # placeholder contra el contexto en vez de contra el valor, y 4 de 5 credenciales reales
        # quedaban sin detectar). Aquí pasaba lo simétrico: las señales miraban TODO el texto, así
        # que una frontera propia y sana MORÍA si en otra frase aparecía "se repuso" o el nombre de
        # una hermana. Ahora cada aparición se juzga POR SÍ MISMA y basta UNA limpia: un texto no
        # deja de establecer su frontera porque además cite la de otro.
        MARCAS = ("NO es para", "NO usar", "NO para")
        def es_frontera_propia(t, i):
            """i = posición de una marca de negación. Decide si ESA aparición manda aquí."""
            antes, despues = t[max(0, i-45):i], t[i:i+160]
            if not any(x in despues for x in ("deriva", "→", "es de ", "usa la hermana")):
                return False                                   # no dice a dónde va: no es frontera
            if re.search(r'golden-[a-z0-9-]+[\s,;]*$', antes):
                return False                                   # una hermana es el SUJETO: regla ajena
            if re.search(r'["\u201c\u00ab][^"\u201d\u00bb]{0,10}$', antes):
                return False                                   # abre entrecomillada: es cita
            if re.search(r'(historial|ejemplo|se repuso|escriben|decía|catálogo)[^.]{0,60}$',
                         antes, re.I):
                return False                                   # narrada en su propia cláusula
            return True
        tiene_frontera = any(es_frontera_propia(plano, m.start())
                             for marca in MARCAS
                             for m in re.finditer(re.escape(marca), plano))
        print(f"  {'✅' if tiene_frontera else '❌'} FRONTERAS con las hermanas presentes"
              f"{'' if tiene_frontera else ' — un recorte se las llevó; sin esto la skill se dispara sobre piezas sueltas'}")
        fallos += 0 if tiene_frontera else 1
        if tiene_frontera:
            print("      límite declarado: esto mide PRESENCIA de la frontera, no que esté bien "
                  "REDACTADA. Una cita disfrazada de regla se caza; una regla mal escrita, no.")
            # Se busca con la MISMA lista MARCAS: al ampliarla con "NO para" esta línea se quedó
            # con dos de las tres y REVENTÓ con una frontera legítima. Un crash sale con exit 1,
            # igual que "muerde bien", así que por el lado malo era invisible: lo destapó el lado
            # BUENO. Dos fuentes de verdad para la misma lista es la deuda que se paga así.
            posiciones = [plano.index(x) for x in MARCAS if x in plano]
            pos = min(posiciones) if posiciones else 0
            if posiciones and pos > len(plano) * 0.6:
                print("  ⚠️  las fronteras viven en el último 40% — el próximo recorte por el final las borra otra vez")

    # 2 · el sello más nuevo tiene su entrada en el changelog
    chlog = os.path.join(base, "references", "changelog.md")
    sellos = re.findall(r"GR360_VERSION:\s*(R[0-9.]+[a-z]?)", txt)
    if sellos and os.path.isfile(chlog):
        ultimo = sellos[0]
        cl = open(chlog, encoding="utf-8").read()
        ok = re.search(r"^##\s*" + re.escape(ultimo) + r"\b", cl, re.M) is not None
        print(f"  {'✅' if ok else '❌'} el sello {ultimo} tiene entrada en el changelog"
              f"{'' if ok else ' — sellar sin registrar deja el historial mintiendo'}")
        fallos += 0 if ok else 1

    # 3 · toda hija nombrada en HIJAS existe en disco
    faltan = [n for n in HIJAS if not os.path.isdir(os.path.join(SKILLS_DIR, n))]
    print(f"  {'✅' if not faltan else '❌'} {len(HIJAS)} hijas declaradas, {len(faltan)} sin instalar"
          + (f": {', '.join(faltan)}" if faltan else ""))
    fallos += 0 if not faltan else 1

    print("═══ RESULTADO:", "✅ la skill se sostiene" if fallos == 0 else f"❌ {fallos} fallo(s) propios", "═══")
    return 0 if fallos == 0 else 1


def check_skills() -> int:
    print("═══ DEPENDENCIAS · skills hijas instaladas ═══")
    faltan = 0
    for nombre, para in HIJAS.items():
        if os.path.isdir(os.path.join(SKILLS_DIR, nombre)):
            print(f"  ✅ {nombre}")
        else:
            print(f"  ❌ NO instalada: {nombre} — {para} → esa fase se marca [PARCIAL]")
            faltan += 1
    for nombre, para in AUXILIARES.items():
        estado = "✅" if os.path.isdir(os.path.join(SKILLS_DIR, nombre)) else "⚪ ausente (opcional)"
        print(f"  {estado} {nombre} — {para}")
    for nombre, para in SOLO_DEL_DUENO.items():
        if os.path.isdir(os.path.join(SKILLS_DIR, nombre)):
            print(f"  ➕ {nombre} (extra del dueño) — {para}")
    print("═══ RESULTADO:", "✅ ecosistema completo" if faltan == 0 else f"⚠️ {faltan} skill(s) faltante(s) — el pipeline sigue, marcando [PARCIAL]", "═══")
    return 0 if faltan == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "--skills":
        sys.exit(check_skills())
    if arg == "--autochequeo":
        sys.exit(check_autochequeo())
    sys.exit(check_paquete(arg))
