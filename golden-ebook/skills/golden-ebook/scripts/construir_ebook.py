#!/usr/bin/env python3
"""construir_ebook.py · golden-ebook

Convierte un ebook.json (contenido + marca + fuentes) en un PDF editorial listo
para leer en el celular, y exporta la portada en PNG.

Uso:
    $PY scripts/construir_ebook.py ebook.json salida.pdf [--formato movil|a5]
                                   [--portada-png portada.png] [--html-debug x.html]
                                   [--cuerpo-pt N]

Salida: JSON con el reporte de la construcción por stdout.
Códigos: 0 construido · 2 error de uso o de entrada (falta marca, archivo, etc.)

La IDENTIDAD SE PIDE, NO SE HEREDA: sin marca.nombre y marca.colores el motor
se niega a construir. Un ebook con la marca de otro es una atribución falsa.
"""
import argparse
import base64
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FUENTES_DIR = os.path.join(RAIZ, "assets", "fuentes")

# Formatos: medidas en mm. El móvil está calculado para que el cuerpo a 13 pt se
# lea a ~16,6 px cuando el visor del celular ajusta la página al ancho (390 px):
# 13 pt = 4,59 mm; 4,59 / 108 x 390 = 16,6 px. Apple usa 17 pt de cuerpo en iOS.
FORMATOS = {
    "movil": {"w": 108, "h": 192, "m": (14, 11, 17, 11), "cuerpo_pt": 13.0,
              "titulo_pt": 30, "viewport_px": 390},
    "a5":    {"w": 148, "h": 210, "m": (18, 16, 20, 16), "cuerpo_pt": 11.0,
              "titulo_pt": 38, "viewport_px": 768},
}

NOTA_IA = ("Este libro se escribió con apoyo de inteligencia artificial y cada dato se "
           "verificó contra las fuentes citadas.")

TIPOS_BLOQUE = {"parrafo", "subtitulo", "dato", "cita", "lista", "prueba_hoy",
                "mito", "imagen", "nota"}


def falla(msg):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(2)


# ---------------------------------------------------------------- color
def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"color inválido: #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(hex_rgb(a)), luminancia(hex_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def texto_sobre(fondo, candidatos=("#FFFFFF", "#111111")):
    return max(candidatos, key=lambda c: contraste(c, fondo))


# ---------------------------------------------------------------- activos
def data_uri(ruta, mime=None):
    if mime is None:
        ext = os.path.splitext(ruta)[1].lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".webp": "image/webp", ".svg": "image/svg+xml",
                ".ttf": "font/ttf"}.get(ext, "application/octet-stream")
    with open(ruta, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def css_fuentes():
    pares = [("Cuerpo", "Lora-Regular", "normal", 400), ("Cuerpo", "Lora-Italic", "italic", 400),
             ("Cuerpo", "Lora-Bold", "normal", 700), ("Sans", "Outfit-Regular", "normal", 400),
             ("Sans", "Outfit-Bold", "normal", 700), ("Display", "Gloock-Regular", "normal", 400)]
    out = []
    for fam, archivo, estilo, peso in pares:
        ruta = os.path.join(FUENTES_DIR, archivo + ".ttf")
        if not os.path.exists(ruta):
            falla(f"falta la fuente {ruta}: la skill está incompleta")
        out.append(f"@font-face{{font-family:'{fam}';src:url({data_uri(ruta)});"
                   f"font-style:{estilo};font-weight:{peso};}}")
    return "\n".join(out)


def luz_del_logo(ruta):
    """Luminancia media de los píxeles opacos del logo (None si no se puede medir)."""
    try:
        from PIL import Image
    except ImportError:
        return None
    if ruta.lower().endswith(".svg"):
        return None
    im = Image.open(ruta).convert("RGBA")
    im.thumbnail((200, 200))
    tot, n = 0.0, 0
    px = im.load()
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = px[x, y]
            if a <= 128:
                continue
            tot += luminancia((r, g, b))
            n += 1
    return tot / n if n else None


# ---------------------------------------------------------------- texto
REF = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def inline(txt):
    """Escapa y aplica el marcado mínimo: **negrita**, *cursiva*, [n] citas."""
    t = html.escape(str(txt), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)

    def cita(m):
        ids = [i.strip() for i in m.group(1).split(",")]
        enl = ",".join(f'<a href="#f-{i}">{i}</a>' for i in ids)
        return f'<sup class="ref">{enl}</sup>'
    # La cita se pega a la palabra y el % a su número: con un espacio normal el visor
    # los separa en líneas distintas (medido: 49 citas y un "34 / %" partido).
    t = re.sub(r"\s+(?=\[\d+(?:\s*,\s*\d+)*\])", "", t)
    t = re.sub(r"(\d)\s%", "\\1\u00a0%", t)
    # Comillas tipográficas en vez de rectas.
    t = re.sub(r'(^|[\s(¿¡])"', "\\1\u201c", t).replace('"', "\u201d")
    # La última palabra viaja con su cita: sin esto la separación silábica dejaba "ciudade-" en
    # una línea y "s" con su número en la siguiente (medido en el ebook del filtro).
    t = re.sub(r"(\S+)(\[\d+(?:\s*,\s*\d+)*\])", lambda m: f'<span class="nw">{m.group(1)}{REF.sub(cita, m.group(2))}</span>', t)
    t = REF.sub(cita, t)  # una cita al comienzo del texto no tiene palabra antes
    return t


def parrafos(txt):
    return "".join(f"<p>{inline(p.strip())}</p>" for p in str(txt).split("\n\n") if p.strip())


# ---------------------------------------------------------------- arte
def arte_portada(semilla, acento, claro):
    """Arte vectorial determinista (misma semilla = misma portada)."""
    h = hashlib.sha256(semilla.encode()).digest()
    # El arte vive en el tercio superior y se desvanece antes de la zona del título
    # (y > 100 de 192): medido en la primera versión, las líneas cruzaban el título.
    cx = 58 + h[0] % 36
    cy = 52 + h[1] % 26
    capas = []
    for i in range(9):
        r = 10 + i * (7 + h[2] % 4)
        op = 0.10 + 0.07 * ((h[3 + i] % 5) / 4)
        grosor = 0.5 + (h[12 + i] % 3) * 0.6
        capas.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                     f'stroke="{acento}" stroke-width="{grosor:.1f}" opacity="{op:.2f}"/>')
    ang = h[20] % 360
    for i in range(3):
        a = math.radians(ang + i * 37)
        x2, y2 = cx + 120 * math.cos(a), cy + 120 * math.sin(a)
        capas.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{claro}" stroke-width="0.4" opacity="0.35"/>')
    capas.append(f'<circle cx="{cx}" cy="{cy}" r="{6 + h[25] % 6}" fill="{acento}" opacity="0.9"/>')
    return ('<svg class="arte" viewBox="0 0 108 192" preserveAspectRatio="xMidYMid slice" '
            'xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="fade" x1="0" y1="0" '
            'x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#fff"/>'
            '<stop offset=".64" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<mask id="m"><rect width="108" height="192" fill="url(#fade)"/></mask></defs>'
            f'<g mask="url(#m)">{"".join(capas)}</g></svg>')


# ---------------------------------------------------------------- bloques
def bloque(b, n_cap, idx):
    tipo = b.get("tipo")
    if tipo not in TIPOS_BLOQUE:
        falla(f"capítulo {n_cap}, bloque {idx}: tipo desconocido '{tipo}' "
              f"(válidos: {', '.join(sorted(TIPOS_BLOQUE))})")
    if tipo == "parrafo":
        return parrafos(b.get("texto", ""))
    if tipo == "subtitulo":
        return f'<h3>{inline(b.get("texto", ""))}</h3>'
    if tipo == "dato":
        ref = f'<sup class="ref"><a href="#f-{b["fuente"]}">{b["fuente"]}</a></sup>' if b.get("fuente") else ""
        return (f'<div class="dato"><div class="cifra">{inline(b.get("cifra", ""))}</div>'
                f'<div class="dato-txt">{inline(b.get("texto", ""))}{ref}</div></div>')
    if tipo == "cita":
        autor = f'<div class="cita-autor">{inline(b["autor"])}</div>' if b.get("autor") else ""
        return f'<blockquote class="cita"><p>{inline(b.get("texto", ""))}</p>{autor}</blockquote>'
    if tipo == "lista":
        tit = f'<div class="lista-tit">{inline(b["titulo"])}</div>' if b.get("titulo") else ""
        items = "".join(f"<li>{inline(i)}</li>" for i in b.get("items", []))
        return f'<div class="lista">{tit}<ul>{items}</ul></div>'
    if tipo == "prueba_hoy":
        items = "".join(f'<li><span class="caja"></span><span>{inline(i)}</span></li>'
                        for i in b.get("items", []))
        tit = inline(b.get("titulo", "Pruébalo hoy"))
        return f'<div class="prueba"><div class="prueba-tit">{tit}</div><ul>{items}</ul></div>'
    if tipo == "mito":
        ref = f'<sup class="ref"><a href="#f-{b["fuente"]}">{b["fuente"]}</a></sup>' if b.get("fuente") else ""
        return (f'<div class="mito"><div class="mito-a"><span class="et">Mito</span>'
                f'<p>{inline(b.get("mito", ""))}</p></div><div class="mito-b">'
                f'<span class="et">Lo que dice la evidencia</span>'
                f'<p>{inline(b.get("realidad", ""))}{ref}</p></div></div>')
    if tipo == "nota":
        tit = f'<div class="nota-tit">{inline(b["titulo"])}</div>' if b.get("titulo") else ""
        return f'<div class="nota">{tit}{parrafos(b.get("texto", ""))}</div>'
    if tipo == "imagen":
        ruta = b.get("_ruta_abs")
        if not ruta or not os.path.exists(ruta):
            falla(f"capítulo {n_cap}: no existe la imagen {b.get('ruta')}")
        cred = f' <span class="credito">{inline(b["credito"])}</span>' if b.get("credito") else ""
        return (f'<figure><img src="{data_uri(ruta)}" alt="{html.escape(b.get("pie", ""))}"/>'
                f'<figcaption>{inline(b.get("pie", ""))}{cred}</figcaption></figure>')
    return ""


# ---------------------------------------------------------------- html
def construir_html(e, fmt, cuerpo_pt, base):
    F = FORMATOS[fmt]
    W, H = F["w"], F["h"]
    mt, mr, mb, ml = F["m"]
    marca = e["marca"]
    col = marca["colores"]
    prim, acento, fondo, texto = col["primario"], col["acento"], col["fondo"], col["texto"]
    # acento_texto: el acento que se LEE sobre el fondo claro. Muchos acentos de marca
    # (dorados, amarillos) no llegan a 4.5:1 sobre fondo claro; la marca suele tener un
    # tono oscuro del mismo color para texto. Si no lo trae, se usa el acento y el
    # verificador mide el contraste y lo acusa.
    ac_t = col.get("acento_texto") or acento
    sobre_prim = texto_sobre(prim, ("#FFFFFF", texto, "#111111"))
    meta = e["meta"]
    nombre = marca["nombre"]
    esc_nombre = nombre.replace('"', "'")

    logo_html, logo_info = "", {"logo": "ausente"}
    logo_ruta = marca.get("_logo_abs")
    if logo_ruta:
        lz = luz_del_logo(logo_ruta)
        placa = False
        if lz is not None:
            c_logo = (max(lz, luminancia(hex_rgb(prim))) + 0.05) / (min(lz, luminancia(hex_rgb(prim))) + 0.05)
            placa = c_logo < 2.2
            logo_info = {"logo": "presente", "contraste_logo_portada": round(c_logo, 2), "placa": placa}
        else:
            logo_info = {"logo": "presente", "contraste_logo_portada": None, "placa": False}
        cls = "logo placa" if placa else "logo"
        logo_html = f'<div class="{cls}"><img src="{data_uri(logo_ruta)}" alt="{html.escape(nombre)}"/></div>'
    else:
        # Sin logo no se inventa uno: el nombre va en tipografía y se avisa.
        print("AVISO: marca.logo vacío. La portada lleva el nombre en tipografía; "
              "pídele el logo a la marca.", file=sys.stderr)
        logo_html = f'<div class="logo marca-texto">{html.escape(nombre)}</div>'

    port = e.get("portada", {})
    img_port = port.get("_imagen_abs")
    if img_port:
        fondo_port = (f'<img class="foto" src="{data_uri(img_port)}" alt=""/>'
                      f'<div class="velo"></div>')
    else:
        fondo_port = arte_portada(meta["titulo"], acento, sobre_prim)
    cred_port = (f'<div class="cred-port">{inline(port["credito_imagen"])}</div>'
                 if img_port and port.get("credito_imagen") else "")

    portada = f"""
<section class="portada">
  {fondo_port}
  <div class="port-in">
    {logo_html}
    <div class="port-txt">
      <div class="kicker">{inline(port.get("kicker", ""))}</div>
      <h1>{inline(meta["titulo"])}</h1>
      <div class="sub">{inline(meta.get("subtitulo", ""))}</div>
    </div>
    <div class="port-pie">{html.escape(nombre)}</div>
  </div>{cred_port}
</section>"""

    bien = e.get("bienvenida", {})
    bienvenida = f"""
<section class="bienvenida">
  <div class="bv-kicker">{inline(bien.get("kicker", "Antes de empezar"))}</div>
  <h2>{inline(bien.get("titulo", ""))}</h2>
  {parrafos(bien.get("texto", ""))}
  <div class="firma">{inline(bien.get("firma", nombre))}</div>
</section>"""

    caps = e["capitulos"]
    indice_items = "".join(
        f'<li><a href="#cap-{i}"><span class="n">{i:02d}</span>'
        f'<span class="t">{inline(c["titulo"])}</span></a></li>'
        for i, c in enumerate(caps, 1))
    indice = f"""
<section class="indice">
  <div class="bv-kicker">En este libro</div>
  <ol>{indice_items}</ol>
</section>"""

    cuerpo = []
    for i, c in enumerate(caps, 1):
        piezas = [bloque(b, i, j) for j, b in enumerate(c.get("bloques", []), 1)]
        cierre = ""
        if c.get("cierre"):
            # El cierre viaja pegado al último bloque: una frase de cierre sola en una
            # página es una página viuda (medido en la primera versión: 3 de 40).
            ult = piezas.pop() if piezas else ""
            cierre = (f'<div class="final-cap">{ult}<div class="cierre-cap">'
                      f'{inline(c["cierre"])}</div></div>')
        bloques = "".join(piezas)
        cuerpo.append(f"""
<section class="apertura" id="cap-{i}">
  <div class="ap-num">{i:02d}</div>
  <div class="ap-et">Capítulo {i}</div>
  <h2>{inline(c["titulo"])}</h2>
  <div class="ap-gancho">{inline(c.get("gancho", ""))}</div>
</section>
<section class="cuerpo">{bloques}{cierre}</section>""")

    ci = e.get("cierre", {})
    cta = ci.get("cta") or {}
    cta_html = (f'<a class="cta" href="{html.escape(cta["url"])}">{inline(cta["texto"])}</a>'
                if cta.get("url") and cta.get("texto") else "")
    cierre = f"""
<section class="final">
  <div class="bv-kicker">{inline(ci.get("kicker", "Para cerrar"))}</div>
  <h2>{inline(ci.get("titulo", ""))}</h2>
  {parrafos(ci.get("texto", ""))}
  {cta_html}
</section>"""

    fuentes = "".join(
        f'<li id="f-{f["id"]}"><span class="fid">{f["id"]}</span><span>'
        f'{inline(f.get("titulo", ""))}{"" if str(f.get("titulo", "")).rstrip()[-1:] in "?!." else "."} '
        f'{inline(f.get("editor", ""))}'
        f'{", " + str(f["anio"]) if f.get("anio") else ""}. '
        f'<a href="{html.escape(f["url"])}">{html.escape(f["url"])}</a>'
        f'{" · consultado " + html.escape(f["consultado"]) if f.get("consultado") else ""}</span></li>'
        for f in e.get("fuentes", []))
    fuentes_html = f"""
<section class="fuentes">
  <div class="bv-kicker">Fuentes</div>
  <h2>De dónde sale cada dato</h2>
  <p class="fuentes-intro">{inline(e.get("fuentes_intro", "Cada número entre corchetes del texto remite a esta lista. Puedes abrir cualquiera y leerla completa."))}</p>
  <ol>{fuentes}</ol>
</section>"""

    web = marca.get("web", "")
    contra = f"""
<section class="contra">
  {logo_html}
  <div class="contra-nombre">{html.escape(nombre)}</div>
  {f'<div class="contra-web">{html.escape(web)}</div>' if web else ''}
  <div class="aviso">{inline(e.get("aviso", ""))}</div>
  <div class="aviso">{inline(e.get("nota_ia", NOTA_IA))}</div>
  <div class="copy">© {html.escape(str(meta.get("anio", "")))} {html.escape(nombre)}</div>
</section>"""

    tpt = F["titulo_pt"]
    css = f"""
{css_fuentes()}
@page {{ size:{W}mm {H}mm; margin:{mt}mm {mr}mm {mb}mm {ml}mm; background:{fondo};
  @bottom-left {{ content:"{esc_nombre}"; font:7pt 'Sans'; color:{texto}; opacity:.55; }}
  @bottom-right {{ content:counter(page); font:8pt 'Sans'; color:{ac_t}; }} }}
@page lleno {{ margin:0; @bottom-left {{content:none}} @bottom-right {{content:none}} }}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Cuerpo';font-size:{cuerpo_pt}pt;line-height:1.55;color:{texto};background:{fondo};
  hyphens:auto;-webkit-hyphens:auto;orphans:3;widows:3}}
a{{color:inherit}}
.portada,.apertura,.contra{{page:lleno;width:{W}mm;height:{H - 0.3}mm;position:relative;overflow:hidden;
  break-after:page}}
.portada{{background:{prim};color:{sobre_prim}}}
.portada .arte{{position:absolute;inset:0;width:100%;height:100%}}
.portada .foto{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.portada .velo{{position:absolute;inset:0;background:linear-gradient(180deg,{prim}33 0%,{prim}cc 55%,{prim} 100%)}}
.port-in{{position:absolute;inset:0;padding:{mt}mm {mr + 1}mm {mb - 4}mm {ml + 1}mm;display:flex;flex-direction:column}}
.logo img{{max-height:26mm;max-width:62mm;display:block}}
.logo.placa{{align-self:flex-start;background:{fondo};padding:2.4mm 3.4mm;border-radius:2mm}}
.marca-texto{{font-family:'Sans';font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:9pt}}
.port-txt{{margin-top:auto}}
.kicker{{font-family:'Sans';font-weight:700;font-size:8pt;letter-spacing:.18em;text-transform:uppercase;color:{acento};margin-bottom:3mm}}
.portada h1{{font-family:'Display';font-weight:400;font-size:{tpt}pt;line-height:1.02;letter-spacing:-.01em}}
.portada .sub{{font-size:{cuerpo_pt}pt;line-height:1.4;margin-top:4mm;opacity:.92}}
.port-pie{{margin-top:8mm;font-family:'Sans';font-weight:700;font-size:9.5pt;letter-spacing:.16em;text-transform:uppercase;opacity:.9}}
.cred-port{{position:absolute;right:3mm;bottom:2mm;font:5.5pt 'Sans';opacity:.7}}
.bienvenida,.indice,.final,.fuentes{{break-after:page}}
.bv-kicker{{font-family:'Sans';font-weight:700;font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:{ac_t};margin-bottom:3mm}}
h2{{font-family:'Display';font-weight:400;font-size:{round(tpt * .72)}pt;line-height:1.08;margin-bottom:5mm}}
.nw{{white-space:nowrap;hyphens:none;-webkit-hyphens:none}}
h1,h2,h3,.kicker,.ap-gancho,.sub,.bv-kicker,.ap-et,.et,.cita-autor,.prueba-tit,.lista-tit,.nota-tit,.port-pie,
.cta,.contra-nombre,.fuentes{{hyphens:manual;-webkit-hyphens:manual}}
.final-cap{{break-inside:avoid}}
h3{{font-family:'Sans';font-weight:700;font-size:{cuerpo_pt + 1}pt;line-height:1.3;margin:6mm 0 2mm;break-after:avoid}}
p{{margin-bottom:3.2mm;text-align:left}}
.firma{{font-style:italic;margin-top:6mm;color:{ac_t}}}
.indice ol{{list-style:none}}
.indice li{{border-bottom:.3pt solid {texto}33;padding:3mm 0}}
.indice a{{text-decoration:none;display:flex;gap:4mm;align-items:baseline}}
.indice .n{{font-family:'Display';font-size:{cuerpo_pt + 6}pt;color:{ac_t};min-width:9mm}}
.indice .t{{font-family:'Sans';font-size:{cuerpo_pt}pt;line-height:1.3}}
.apertura{{background:{prim};color:{sobre_prim};padding:{mt + 8}mm {mr + 1}mm {mb}mm {ml + 1}mm;display:flex;flex-direction:column}}
.ap-num{{font-family:'Display';font-size:{tpt * 2.6:.0f}pt;line-height:.9;color:{acento}}}
.ap-et{{font-family:'Sans';font-weight:700;font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;margin:4mm 0 3mm;opacity:.8}}
.apertura h2{{font-size:{round(tpt * .8)}pt;margin-bottom:6mm}}
.ap-gancho{{font-style:italic;font-size:{cuerpo_pt + .5}pt;line-height:1.5;margin-top:auto;opacity:.95}}
.cuerpo{{break-after:page}}
.cuerpo>p:first-child::first-letter{{font-family:'Display';float:left;font-size:{cuerpo_pt * 3.3:.1f}pt;line-height:.85;margin:1mm 2mm 0 0;color:{ac_t}}}
sup.ref{{font-family:'Sans';font-size:.62em;color:{ac_t};line-height:0}}
sup.ref a{{text-decoration:none}}
.dato,.cita,.lista,.prueba,.mito,.nota,figure{{break-inside:avoid;margin:5mm 0}}
.dato{{border-left:1.2mm solid {acento};padding:1mm 0 1mm 4mm}}
.dato .cifra{{font-family:'Display';font-size:{cuerpo_pt * 2.4:.1f}pt;line-height:1;color:{ac_t};margin-bottom:1.5mm}}
.dato-txt{{font-family:'Sans';font-size:{cuerpo_pt - .5}pt;line-height:1.4}}
.cita p{{font-family:'Display';font-size:{cuerpo_pt + 3}pt;line-height:1.3;margin:0}}
.cita-autor{{font-family:'Sans';font-size:{cuerpo_pt - 2}pt;margin-top:2mm;color:{ac_t};letter-spacing:.06em;text-transform:uppercase}}
.lista-tit,.prueba-tit,.nota-tit{{font-family:'Sans';font-weight:700;font-size:{cuerpo_pt - .5}pt;margin-bottom:2mm;letter-spacing:.02em}}
.lista ul{{padding-left:5mm}} .lista li{{margin-bottom:1.6mm}}
.prueba{{background:{prim};color:{sobre_prim};border-radius:2.5mm;padding:4mm 4.5mm}}
.prueba-tit{{color:{acento};text-transform:uppercase;letter-spacing:.12em;font-size:{cuerpo_pt - 3}pt}}
.prueba sup.ref{{color:{acento}}} .prueba .et{{color:{acento}}}
.prueba ul{{list-style:none}} .prueba li{{display:flex;gap:2.5mm;margin-bottom:2mm;font-size:{cuerpo_pt - .5}pt;line-height:1.4}}
.caja{{flex:0 0 3.4mm;height:3.4mm;border:.45mm solid {acento};border-radius:.6mm;margin-top:1mm}}
.mito{{border:.35mm solid {texto}33;border-radius:2.5mm;overflow:hidden}}
.mito-a{{padding:3mm 4mm;background:{texto}0d}} .mito-b{{padding:3mm 4mm}}
.mito p{{margin:1mm 0 0;font-size:{cuerpo_pt - .5}pt;line-height:1.45}}
.mito-a p{{text-decoration:line-through;text-decoration-color:{acento};text-decoration-thickness:.3mm}}
.et{{font-family:'Sans';font-weight:700;font-size:{cuerpo_pt - 4}pt;letter-spacing:.14em;text-transform:uppercase;color:{ac_t}}}
.nota{{background:{texto}0d;border-radius:2.5mm;padding:4mm}}
figure img{{width:100%;border-radius:2mm;display:block}}
figcaption{{font-family:'Sans';font-size:{cuerpo_pt - 3}pt;margin-top:1.5mm;opacity:.8}}
.credito{{opacity:.7}}
.cierre-cap{{font-style:italic;margin-top:6mm;padding-top:4mm;border-top:.3pt solid {acento}}}
.cta{{display:block;margin-top:7mm;background:{acento};color:{texto_sobre(acento, ('#FFFFFF', '#111111'))};text-decoration:none;
  font-family:'Sans';font-weight:700;text-align:center;padding:4mm;border-radius:2.5mm;font-size:{cuerpo_pt}pt}}
.fuentes ol{{list-style:none}}
.fuentes li{{display:flex;gap:2.5mm;font-family:'Sans';font-size:{max(cuerpo_pt - 4, 8)}pt;line-height:1.35;margin-bottom:1.6mm;break-inside:avoid;overflow-wrap:anywhere}}
.fid{{color:{ac_t};font-weight:700;min-width:5mm}}
.fuentes-intro{{font-size:{cuerpo_pt - 1.5}pt}}
.contra{{background:{prim};color:{sobre_prim};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:14mm}}
.contra .logo img{{max-height:16mm}}
.contra-nombre{{font-family:'Display';font-size:{cuerpo_pt + 8}pt;margin-top:5mm}}
.contra-web{{font-family:'Sans';font-size:{cuerpo_pt - 2}pt;margin-top:2mm;color:{acento}}}
.aviso{{font-family:'Sans';font-size:{max(cuerpo_pt - 4, 7.5)}pt;line-height:1.45;margin-top:10mm;opacity:.85;max-width:80mm}}
.copy{{font-family:'Sans';font-size:7pt;margin-top:6mm;opacity:.7}}
"""
    lang = meta.get("idioma", "es")
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<title>{html.escape(meta["titulo"])}</title><style>{css}</style></head><body>'
            f'{portada}{bienvenida}{indice}{"".join(cuerpo)}{cierre}{fuentes_html}{contra}'
            f'</body></html>'), {"contraste_portada": round(contraste(sobre_prim, prim), 2),
                                 "contraste_acento_texto": round(contraste(ac_t, fondo), 2),
                                 "texto_sobre_primario": sobre_prim, **logo_info}


# ---------------------------------------------------------------- validación de entrada
def resolver(e, base):
    for campo in ("meta", "marca", "capitulos"):
        if campo not in e:
            falla(f"falta el bloque '{campo}' en el ebook.json")
    if not e["meta"].get("titulo"):
        falla("falta meta.titulo")
    m = e["marca"]
    if not m.get("nombre"):
        falla("falta marca.nombre: la identidad se pide, no se hereda. Dame el nombre de la empresa.")
    col = m.get("colores") or {}
    for k in ("primario", "acento", "fondo", "texto"):
        if not col.get(k):
            falla(f"falta marca.colores.{k}: toma los colores del cerebro de marca, no los inventes")
        try:
            hex_rgb(col[k])
        except ValueError as ex:
            falla(f"marca.colores.{k}: {ex}")
    if m.get("logo"):
        ruta = m["logo"] if os.path.isabs(m["logo"]) else os.path.join(base, m["logo"])
        if not os.path.exists(ruta):
            falla(f"marca.logo apunta a un archivo que no existe: {ruta}")
        if ruta.lower().endswith(".svg"):
            ruta = svg_a_png(ruta)
        m["_logo_abs"] = ruta
    p = e.get("portada") or {}
    if p.get("imagen"):
        ruta = p["imagen"] if os.path.isabs(p["imagen"]) else os.path.join(base, p["imagen"])
        if not os.path.exists(ruta):
            falla(f"portada.imagen no existe: {ruta}")
        p["_imagen_abs"] = ruta
    if not e["capitulos"]:
        falla("el ebook no tiene capítulos")
    for i, c in enumerate(e["capitulos"], 1):
        if not c.get("titulo"):
            falla(f"el capítulo {i} no tiene título")
        for b in c.get("bloques", []):
            if b.get("tipo") == "imagen" and b.get("ruta"):
                b["_ruta_abs"] = b["ruta"] if os.path.isabs(b["ruta"]) else os.path.join(base, b["ruta"])


def svg_a_png(ruta):
    """Un logo SVG se dibuja como vectores y el verificador no lo ve como imagen (ni mide su
    tamaño ni su contraste). Se rasteriza con el mismo Chromium, fondo transparente, a 1200 px."""
    from playwright.sync_api import sync_playwright
    salida = os.path.join(tempfile.gettempdir(), "golden-ebook-logo-" +
                          hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:12] + ".png")
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page()
        pg.set_content(f'<html><body style="margin:0;background:transparent">'
                       f'<img id="l" src="{data_uri(ruta)}" style="width:1200px;display:block"></body></html>')
        pg.locator("#l").screenshot(path=salida, omit_background=True)
        nav.close()
    return salida


# ---------------------------------------------------------------- render
def render_pdf(html_txt, salida):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        falla("falta playwright. Usa el intérprete ~/.golden/pdfenv/bin/python o instala: "
              "pip install playwright && python -m playwright install chromium")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html_txt)
        tmp = t.name
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch()
            pg = nav.new_page()
            pg.goto("file://" + tmp)
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            # Sin outline=True a propósito: Chromium arma los marcadores con el texto
            # renderizado y se come el espacio donde el título salta de línea
            # ("Lo que nadie tecontó"). Los marcadores se ponen después, desde el JSON.
            pg.pdf(path=salida, prefer_css_page_size=True, print_background=True, tagged=True)
            version = nav.version
            nav.close()
    finally:
        os.unlink(tmp)
    return version


def sello_json(ruta_json):
    """sha256 del ebook.json tal como está en disco: ata el PDF al contenido que se verificó."""
    import hashlib as _h
    with open(ruta_json, "rb") as f:
        return _h.sha256(f.read()).hexdigest()


def poner_metadatos(pdf, e, sello=""):
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return False
    lector = PdfReader(pdf)
    w = PdfWriter(clone_from=lector)
    meta = e["meta"]
    # Marcadores desde el JSON: título exacto y página de apertura de cada capítulo.
    paginas = [re.sub(r"\s+", "", (p.extract_text() or "")).casefold() for p in lector.pages]
    w.add_outline_item("Portada", 0)
    for i, c in enumerate(e["capitulos"], 1):
        clave = re.sub(r"\s+", "", c["titulo"]).casefold()
        rotulo = f"capítulo{i}"
        pag = next((k for k, t in enumerate(paginas) if rotulo in t and clave in t
                    and t.startswith(f"{i:02d}")), None)
        if pag is not None:
            w.add_outline_item(c["titulo"], pag)
    pag_f = next((k for k, t in enumerate(paginas) if t.startswith("fuentes")), None)
    if pag_f is not None:
        w.add_outline_item("Fuentes", pag_f)
    w.add_metadata({"/Title": meta["titulo"], "/Author": e["marca"]["nombre"],
                    "/Subject": meta.get("subtitulo", ""),
                    "/Keywords": ", ".join(meta.get("palabras_clave", [])),
                    "/Creator": "golden-ebook",
                    # El verificador compara este sello con el JSON que recibe (P12): sin él,
                    # un PDF viejo con claims se podía verificar contra un JSON ya limpio.
                    "/EbookJSONSHA256": sello})
    tmp = pdf + ".tmp"
    with open(tmp, "wb") as f:
        w.write(f)
    os.replace(tmp, pdf)
    return True


def exportar_portada(pdf, png):
    if not shutil.which("pdftoppm"):
        return "N/D: falta pdftoppm (brew install poppler)"
    raiz = os.path.splitext(png)[0]
    subprocess.run(["pdftoppm", "-png", "-f", "1", "-l", "1", "-scale-to-x", "1080",
                    "-scale-to-y", "-1", "-singlefile", pdf, raiz], check=True)
    return raiz + ".png"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ebook_json")
    ap.add_argument("salida_pdf")
    ap.add_argument("--formato", choices=sorted(FORMATOS))
    ap.add_argument("--portada-png")
    ap.add_argument("--html-debug")
    ap.add_argument("--cuerpo-pt", type=float, help="solo para pruebas: fuerza el tamaño del cuerpo")
    a = ap.parse_args()

    if not os.path.exists(a.ebook_json):
        falla(f"no existe {a.ebook_json}")
    try:
        with open(a.ebook_json, encoding="utf-8") as f:
            e = json.load(f)
    except json.JSONDecodeError as ex:
        falla(f"el ebook.json no es JSON válido: {ex}")
    base = os.path.dirname(os.path.abspath(a.ebook_json))
    resolver(e, base)
    fmt = a.formato or e["meta"].get("formato", "movil")
    if fmt not in FORMATOS:
        falla(f"formato '{fmt}' desconocido: usa movil o a5")
    cuerpo_pt = a.cuerpo_pt or FORMATOS[fmt]["cuerpo_pt"]

    html_txt, info = construir_html(e, fmt, cuerpo_pt, base)
    if a.html_debug:
        with open(a.html_debug, "w", encoding="utf-8") as f:
            f.write(html_txt)
    os.makedirs(os.path.dirname(os.path.abspath(a.salida_pdf)), exist_ok=True)
    motor = render_pdf(html_txt, a.salida_pdf)
    meta_ok = poner_metadatos(a.salida_pdf, e, sello_json(a.ebook_json))
    portada = exportar_portada(a.salida_pdf, a.portada_png) if a.portada_png else None

    print(json.dumps({"ok": True, "pdf": a.salida_pdf, "formato": fmt, "cuerpo_pt": cuerpo_pt,
                      "motor": f"chromium {motor}", "metadatos": meta_ok, "portada_png": portada,
                      "bytes": os.path.getsize(a.salida_pdf), **info}, ensure_ascii=False))


if __name__ == "__main__":
    main()
