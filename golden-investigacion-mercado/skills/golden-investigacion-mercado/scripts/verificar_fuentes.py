#!/usr/bin/env python3
"""
SUITE DE VERIFICACION DE FUENTES — Golden Group

El problema que resuelve: la matriz de fuentes de `scraping-firecrawl.md` esta MEDIDA, pero
medida UNA VEZ. Los sitios cambian sus defensas cada pocos meses y nadie se entera: las skills
siguen afirmando "Amazon funciona por navegador" con total seguridad hasta que un dia no.

QUE ES Y QUE NO ES
  ES  un DETECTOR DE CAMBIO. Toma la huella de cada fuente y la compara con la del dia que se
      midio. Si algo se movio, te lo dice para que se re-verifique con la herramienta de verdad.
  NO  es un verificador de funcionamiento. Amazon devuelve firma anti-bot por HTTP plano y aun
      asi FUNCIONA por navegador (medido 2026-08-02). Una firma no prueba que este roto.
      Por eso el veredicto es CAMBIO / IGUAL, nunca FUNCIONA / NO FUNCIONA.

  Las sondas de yt-dlp SI son definitivas: usan la herramienta real.
  Las de Firecrawl y navegador NO se pueden correr desde aqui (son MCP): el script las imprime
  como checklist con sus parametros exactos y el resultado esperado, para que Claude las corra.

⚠️ CORRERLA UNA VEZ AL MES, NO A CADA RATO. Sondear dispara las defensas que la suite mide:
   medido el 2026-08-02, tras varias sondas seguidas AliExpress paso de 640.990b a 2.391b con
   captcha. El sitio no habia cambiado nada — nos limito a nosotros. El script marca ese patron
   como PROBABLE AUTO-BLOQUEO para que no se confunda con un cambio real, pero la disciplina de
   no abusar es lo que evita el falso positivo.

USO
  python3 verificar_fuentes.py                 # comparar contra la linea base
  python3 verificar_fuentes.py --baseline      # grabar la linea base de HOY (primera vez)
  python3 verificar_fuentes.py --solo-http     # sin yt-dlp (mas rapido)
  python3 verificar_fuentes.py --json          # salida para maquina

Registro: fuentes_baseline.json (junto a este script)
Manual:   ../references/scraping-firecrawl.md
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "fuentes_baseline.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
DIAS_CADUCIDAD = 60

# Marcas que delatan un muro. Se cuentan, no se interpretan.
MARCAS = ["captcha", "anti-csrftoken", "account-verification", "iniciar sesion",
          "iniciar sesión", "robot check", "enter the characters", "verifica que eres"]

# --- SONDAS HTTP (corren solas; detectan CAMBIO de huella) -----------------------------
SONDAS_HTTP = [
    {"id": "aliexpress", "url": "https://www.aliexpress.com/w/wholesale-wart-remover.html",
     "estado_medido": "✅ funciona por Firecrawl (json sin actions)"},
    {"id": "amazon", "url": "https://www.amazon.com/s?k=wart+remover",
     "estado_medido": "✅ funciona por NAVEGADOR · ❌ por Firecrawl (muro anti-bot)"},
    {"id": "temu", "url": "https://www.temu.com/search_result.html?search_key=wart%20remover",
     "estado_medido": "❌ muro de sesion por toda via"},
    {"id": "mercadolibre", "url": "https://listado.mercadolibre.com.co/removedor-de-verrugas",
     "estado_medido": "❌ captcha por Firecrawl (inventa datos) · muro de sesion por navegador"},
]

# --- SONDAS yt-dlp (definitivas: usan la herramienta real) -----------------------------
SONDAS_YTDLP = [
    {"id": "youtube_comentarios", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     "espera_comentarios": True, "estado_medido": "✅ comentarios con like_count"},
    {"id": "tiktok_comentarios",
     "url": "https://www.tiktok.com/@philsmypharmacist/video/7593089613560827191",
     "espera_comentarios": False, "estado_medido": "✅ metadatos · ❌ comentarios (cero)"},
]

# --- SONDAS MCP (no se pueden correr desde bash; se imprimen como checklist) -----------
CHECKLIST_MCP = [
    ("Firecrawl · AliExpress listado",
     'firecrawl_scrape formats=["json"] proxy="stealth" location={country:"CO"} SIN actions',
     "8-12 productos reales con precio y 'N sold'. Pasar por candado_scraping.py"),
    ("Firecrawl · MercadoLibre",
     'firecrawl_scrape formats=["json"] proxy="stealth"',
     "DEBE fallar: metadata.url con /captcha/ y json inventado tipo 'Producto 1'"),
    ("Navegador · Amazon",
     "navigate amazon.com/s?k=<producto> + querySelectorAll('[data-component-type=\"s-search-result\"]')",
     "~48 tarjetas, ~70% con 'comprados el mes pasado', precios en COP"),
    ("Navegador · Temu",
     "navigate temu.com/search_result.html?search_key=<producto>",
     "DEBE mostrar muro: 'Email o numero de telefono / Continuar'"),
]


def _dominio(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return m.group(1).replace("www.", "") if m else ""


def huella(url):
    """Descarga la url y devuelve su huella: tamano, codigo, redireccion y marcas de muro."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", UA, "--max-time", "30", "-w",
             "\n@@%{http_code}@@%{url_effective}", url],
            capture_output=True, text=True, timeout=45)
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    if r.returncode != 0:
        return {"error": f"curl salio {r.returncode}"}

    salida = r.stdout
    corte = salida.rfind("\n@@")
    if corte == -1:
        return {"error": "respuesta ilegible"}
    cuerpo, cola = salida[:corte], salida[corte + 3:]
    partes = cola.split("@@")
    code = partes[0] if partes else "?"
    final = partes[1] if len(partes) > 1 else ""

    bajo = cuerpo.lower()
    return {
        "http": code,
        "bytes": len(cuerpo),
        # el tamano exacto varia por sesion; se compara por ORDEN DE MAGNITUD
        "magnitud": len(str(len(cuerpo))),
        "redirigido": _dominio(final) != _dominio(url),
        "destino": _dominio(final),
        "marcas": sorted({m for m in MARCAS if m in bajo}),
    }


def sonda_ytdlp(s):
    """Corre yt-dlp de verdad. Este veredicto SI es definitivo."""
    if not shutil.which("yt-dlp"):
        return {"error": "yt-dlp no instalado (brew install yt-dlp)"}
    dest = os.path.join("/tmp", f"vf_{s['id']}")
    f = dest + ".info.json"
    try:
        os.remove(f)
    except OSError:
        pass
    cmd = ["yt-dlp", "--skip-download", "--no-warnings", "--write-info-json",
           "--write-comments", "--extractor-args",
           "youtube:comment_sort=top;max_comments=15",
           "-o", dest + ".%(ext)s", s["url"]]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    if not os.path.exists(f):
        return {"error": "no genero .info.json (la extraccion se rompio)"}
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        return {"error": f"json ilegible: {e}"}
    finally:
        try:
            os.remove(f)
        except OSError:
            pass
    return {"titulo_ok": bool(d.get("title")), "vistas": d.get("view_count"),
            "likes": d.get("like_count"), "comentarios": len(d.get("comments") or [])}


def autobloqueo(ahora, antes):
    """
    Detecta el patron de AUTO-BLOQUEO: la pagina se desploma de tamano Y aparece marca de
    captcha. Medido el 2026-08-02: tras sondear AliExpress varias veces el mismo dia, paso de
    640.990b a 2.391b con marca 'captcha'. El sitio no cambio su politica — nos limito A NOSOTROS.
    Sondear dispara las defensas que esta misma suite mide: por eso se corre UNA VEZ AL MES.
    """
    if not antes or "error" in ahora:
        return False
    encogio = ahora.get("bytes", 0) < antes.get("bytes", 1) * 0.2
    nuevo_captcha = "captcha" in set(ahora.get("marcas", [])) - set(antes.get("marcas", []))
    return encogio and nuevo_captcha


def comparar(ahora, antes):
    """Devuelve lista de diferencias legibles entre dos huellas."""
    if "error" in ahora:
        return [f"error al sondear: {ahora['error']}"]
    if not antes:
        return ["sin linea base (corre --baseline)"]
    d = []
    if autobloqueo(ahora, antes):
        d.append("⚠️ PROBABLE AUTO-BLOQUEO, no un cambio del sitio: la pagina se desplomo "
                 f"({antes.get('bytes')}b → {ahora.get('bytes')}b) y aparecio captcha. "
                 "Suele pasar al sondear la misma fuente varias veces seguidas. "
                 "Esperar unas horas y repetir ANTES de tocar la matriz.")
    if ahora.get("magnitud") != antes.get("magnitud"):
        d.append(f"tamano cambio de orden: {antes.get('bytes')}b → {ahora.get('bytes')}b")
    if ahora.get("redirigido") != antes.get("redirigido"):
        d.append(f"redireccion: {antes.get('redirigido')} → {ahora.get('redirigido')} "
                 f"(destino {ahora.get('destino')})")
    na, nb = set(ahora.get("marcas", [])), set(antes.get("marcas", []))
    if na - nb:
        d.append(f"marcas de muro NUEVAS: {sorted(na - nb)}")
    if nb - na:
        d.append(f"marcas que desaparecieron: {sorted(nb - na)}")
    if ahora.get("http") != antes.get("http"):
        d.append(f"HTTP {antes.get('http')} → {ahora.get('http')}")
    return d


def main():
    args = sys.argv[1:]
    grabar = "--baseline" in args
    solo_http = "--solo-http" in args
    como_json = "--json" in args

    base = {}
    if os.path.exists(BASE):
        try:
            base = json.load(open(BASE, encoding="utf-8"))
        except Exception:
            base = {}

    hoy = date.today().isoformat()
    res = {"fecha": hoy, "http": {}, "ytdlp": {}}
    cambios, avisos = [], []

    for s in SONDAS_HTTP:
        h = huella(s["url"])
        res["http"][s["id"]] = h
        if not grabar:
            difs = comparar(h, (base.get("http") or {}).get(s["id"]))
            if difs:
                cambios.append((s["id"], s["estado_medido"], difs))

    if not solo_http:
        for s in SONDAS_YTDLP:
            r = sonda_ytdlp(s)
            res["ytdlp"][s["id"]] = r
            if "error" in r:
                avisos.append((s["id"], [r["error"]]))
                continue
            if grabar:
                continue
            difs = []
            tiene = (r.get("comentarios") or 0) > 0
            if tiene != s["espera_comentarios"]:
                difs.append(f"comentarios: se esperaban "
                            f"{'SI' if s['espera_comentarios'] else 'NO'} "
                            f"y hubo {r.get('comentarios')}")
            if not r.get("titulo_ok"):
                difs.append("no devolvio titulo (la extraccion se rompio)")
            if difs:
                cambios.append((s["id"], s["estado_medido"], difs))

    if grabar:
        json.dump(res, open(BASE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"Linea base grabada en {BASE} ({hoy}).")
        print("A partir de ahora, correr sin --baseline compara contra esta foto.")
        return 0

    if como_json:
        print(json.dumps({"fecha": hoy, "cambios": cambios, "avisos": avisos},
                         ensure_ascii=False))
        return 1 if cambios else 0

    edad = None
    if base.get("fecha"):
        try:
            edad = (date.today() - datetime.fromisoformat(base["fecha"]).date()).days
        except Exception:
            pass

    print("=" * 70)
    print("  SUITE DE VERIFICACION DE FUENTES — Golden")
    print("=" * 70)
    print(f"  Linea base: {base.get('fecha', 'NO EXISTE')}"
          + (f"  ({edad} dias)" if edad is not None else ""))
    if edad is not None and edad > DIAS_CADUCIDAD:
        print(f"  ⚠️  La linea base tiene mas de {DIAS_CADUCIDAD} dias. Re-verificar con las")
        print("      herramientas de verdad y volver a grabar con --baseline.")
    print()

    if not cambios and not avisos:
        print("  ✅ SIN CAMBIOS. Todas las fuentes responden igual que en la linea base.")
        print("     Ojo: esto dice que NADA SE MOVIO, no que todo funcione. Lo segundo")
        print("     solo lo prueba correr las sondas MCP de abajo.")
        print()
    for cid, estado, difs in cambios:
        print(f"  🔶 CAMBIO en {cid}")
        print(f"     estado registrado: {estado}")
        for d in difs:
            print(f"     · {d}")
        print()
    for cid, difs in avisos:
        print(f"  ⚪ {cid}: {'; '.join(difs)}")
    if avisos:
        print()

    print("-" * 70)
    print("  SONDAS QUE ESTE SCRIPT NO PUEDE CORRER (son MCP) — que las corra Claude:")
    for n, (titulo, como, espera) in enumerate(CHECKLIST_MCP, 1):
        print(f"  {n}. {titulo}")
        print(f"     como:   {como}")
        print(f"     espera: {espera}")
    print("-" * 70)
    print("  Si algo cambio: re-verificar con la herramienta real, actualizar la matriz de")
    print("  `scraping-firecrawl.md`, y volver a grabar la base con --baseline.")
    print()
    return 1 if cambios else 0


if __name__ == "__main__":
    sys.exit(main())
