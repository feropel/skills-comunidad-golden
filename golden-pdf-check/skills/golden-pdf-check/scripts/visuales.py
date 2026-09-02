#!/usr/bin/env python3
"""
GOLDEN PDF · visuales.py — los componentes que hacen que un documento se MIRE.

POR QUE EXISTE: durante 20 versiones esta skill perfeccionó el envase (márgenes,
cortes, contraste, fuentes) y no sabía dibujar ni una barra. Un informe con datos
en párrafos se lee como un muro; los mismos datos en una escala o una barra se
entienden de un vistazo. Esto es lo que pidió FER: "esquemas con dibujos,
escalas, gráficos, barras, estadísticas, al estilo Apple".

TODO ES SVG GENERADO A MANO. Sin librerías de gráficos, sin CDN, sin fuentes
externas: el PDF sigue siendo autocontenido y el componente hereda los tokens de
color del tema activo (variables CSS), así que cambia de identidad sin tocar
código.

MÉTODO: se sigue la skill `dataviz` de Anthropic (elegir la forma → asignar color
por su trabajo → validar la paleta con su script → specs de marca). La paleta
categórica Golden pasó sus seis checks sin un solo aviso.

DONDE EL MEDIO ENDURECE EL MÉTODO — esto es propio y hay que respetarlo:
`dataviz` asume pantalla (hover, tooltip, vista de tabla, modo oscuro). Un PDF
IMPRESO no tiene nada de eso. Consecuencia práctica:
  · las etiquetas directas NO son opcionales: cada dato lleva su número visible,
    porque no hay tooltip que lo rescate;
  · el aviso de contraste no se alivia con interacción, solo con la etiqueta;
  · nada depende del color a solas: cada serie lleva su etiqueta de texto.
"""
import html as _html
import re


def esc(s):
    return _html.escape(str(s), quote=True)


# ── utilidades de escala ───────────────────────────────────────────────────────
def _nice_max(valores):
    """Techo 'redondo' por encima del dato mayor, para que la escala no corte."""
    m = max(valores) if valores else 0
    if m <= 0:
        return 1.0
    import math
    exp = math.floor(math.log10(m))
    base = 10 ** exp
    for mult in (1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10):
        if base * mult >= m:
            return base * mult
    return m


def _fmt(v, unidad=""):
    """Número legible: sin decimales cuando es entero, con punto de miles."""
    if isinstance(v, float) and abs(v - round(v)) < 1e-9:
        v = int(round(v))
    if isinstance(v, int):
        s = f"{v:,}".replace(",", ".")
    else:
        s = f"{v:,.1f}".replace(",", "·").replace(".", ",").replace("·", ".")
    u = (unidad or "").strip()
    if not u:
        return s
    # "%" y los símbolos van pegados; una palabra ("pedidos") lleva espacio.
    # Sin esto salía "4.820pedidos", que se lee como un error de imprenta.
    return s + u if u[0] in "%°" else s + " " + u


# ── 1. KPI / número protagonista ───────────────────────────────────────────────
def kpi(items):
    """Fila de cifras protagonistas. Cuando el dato ES el titular, un número
    grande comunica más que cualquier gráfico (regla de `dataviz`: a veces la
    respuesta NO es un gráfico)."""
    celdas = []
    for it in items:
        etq = esc(it.get("etiqueta", ""))
        val = esc(it.get("valor", ""))
        nota = it.get("nota", "")
        tono = it.get("tono", "")          # bien | mal | neutro
        cls = " kpi-" + tono if tono in ("bien", "mal") else ""
        nota_html = ('<div class="kpi-nota' + cls + '">' + esc(nota) + "</div>") if nota else ""
        celdas.append(
            '<div class="kpi-celda">'
            '<div class="kpi-etq">' + etq + "</div>"
            '<div class="kpi-val">' + val + "</div>"
            + nota_html + "</div>")
    return '<div class="kpi-fila">' + "".join(celdas) + "</div>"


# ── 2. Barras horizontales ─────────────────────────────────────────────────────
def barras(filas, unidad="", titulo=""):
    """Comparar magnitudes. Horizontal a propósito: las etiquetas de categoría
    caben sin rotarse (rotar texto es un anti-patrón: obliga a torcer la cabeza,
    y en papel no hay tooltip que lo compense)."""
    if not filas:
        return ""
    vals = [f[1] for f in filas]
    techo = _nice_max(vals)
    lineas = []
    for i, (etq, val) in enumerate(filas):
        pct = max(0.0, min(1.0, val / techo)) * 100
        serie = (i % 6) + 1
        lineas.append(
            '<div class="bar-fila">'
            '<div class="bar-etq">' + esc(etq) + "</div>"
            '<div class="bar-pista">'
            '<div class="bar-marca bar-s' + str(serie) + '" style="width:' + f"{pct:.1f}" + '%"></div>'
            "</div>"
            '<div class="bar-val">' + esc(_fmt(val, unidad)) + "</div>"
            "</div>")
    cab = ('<p class="viz-titulo">' + esc(titulo) + "</p>") if titulo else ""
    return '<figure class="viz">' + cab + '<div class="barras">' + "".join(lineas) + "</div></figure>"


# ── 3. Escala contra meta ──────────────────────────────────────────────────────
def escala(actual, meta, etiqueta="", unidad=""):
    """Avance hacia un objetivo. La meta se marca con una línea, no con otro
    color de relleno: el ojo compara posición mucho mejor que tono."""
    meta = float(meta) if meta else 1.0
    pct = max(0.0, min(1.0, actual / meta))
    falta = max(0.0, meta - actual)
    return (
        '<figure class="viz escala">'
        + (('<p class="viz-titulo">' + esc(etiqueta) + "</p>") if etiqueta else "")
        + '<div class="esc-pista">'
          '<div class="esc-marca" style="width:' + f"{pct*100:.1f}" + '%"></div>'
          '<div class="esc-meta"></div>'
          "</div>"
          '<div class="esc-pie">'
          '<span class="esc-actual">' + esc(_fmt(actual, unidad)) + "</span>"
          '<span class="esc-sep">de</span>'
          '<span class="esc-total">' + esc(_fmt(meta, unidad)) + "</span>"
          '<span class="esc-falta">' + ("meta cumplida" if falta <= 0
                                        else "faltan " + esc(_fmt(falta, unidad))) + "</span>"
          "</div>"
        "</figure>")


# ── 4. Comparativa antes / después ─────────────────────────────────────────────
def comparativa(filas, unidad="", titulo=""):
    """Dos estados del MISMO indicador. Una sola escala compartida — nunca dos
    ejes (el error de gráfico número uno según `dataviz`)."""
    if not filas:
        return ""
    techo = _nice_max([max(a, b) for _, a, b in filas])
    bloques = []
    for etq, antes, despues in filas:
        pa = max(0.0, min(1.0, antes / techo)) * 100
        pd = max(0.0, min(1.0, despues / techo)) * 100
        delta = despues - antes
        signo = "+" if delta > 0 else ""
        tono = "bien" if delta > 0 else ("mal" if delta < 0 else "neutro")
        bloques.append(
            '<div class="cmp-bloque">'
            '<div class="cmp-etq">' + esc(etq) + "</div>"
            '<div class="cmp-par">'
            '<div class="cmp-linea"><span class="cmp-rot">antes</span>'
            '<div class="bar-pista"><div class="bar-marca cmp-antes" style="width:' + f"{pa:.1f}" + '%"></div></div>'
            '<span class="bar-val">' + esc(_fmt(antes, unidad)) + "</span></div>"
            '<div class="cmp-linea"><span class="cmp-rot">después</span>'
            '<div class="bar-pista"><div class="bar-marca cmp-despues" style="width:' + f"{pd:.1f}" + '%"></div></div>'
            '<span class="bar-val">' + esc(_fmt(despues, unidad)) + "</span></div>"
            "</div>"
            '<div class="cmp-delta cmp-' + tono + '">' + signo + esc(_fmt(delta, unidad)) + "</div>"
            "</div>")
    cab = ('<p class="viz-titulo">' + esc(titulo) + "</p>") if titulo else ""
    return '<figure class="viz">' + cab + "".join(bloques) + "</figure>"


# ── 5. Diagrama de pasos ───────────────────────────────────────────────────────
def pasos(items, titulo=""):
    """Esquema de proceso. Un manual de pasos en viñetas se lee como lista de
    compras; numerado y con conector se lee como un camino."""
    if not items:
        return ""
    celdas = []
    for i, it in enumerate(items, 1):
        if isinstance(it, (list, tuple)):
            tit, desc = it[0], (it[1] if len(it) > 1 else "")
        else:
            tit, desc = it, ""
        celdas.append(
            '<li class="paso">'
            '<span class="paso-num">' + str(i) + "</span>"
            '<div class="paso-cuerpo">'
            '<div class="paso-tit">' + esc(tit) + "</div>"
            + (('<div class="paso-desc">' + esc(desc) + "</div>") if desc else "")
            + "</div></li>")
    cab = ('<p class="viz-titulo">' + esc(titulo) + "</p>") if titulo else ""
    return '<figure class="viz"><ol class="pasos">' + cab + "".join(celdas) + "</ol></figure>"


# ── 6. Código QR ───────────────────────────────────────────────────────────────
def qr(dato, pie="", tam_mm=28):
    """QR en SVG vectorial (segno). Nítido a cualquier zoom, ligero, y el PDF
    sigue autocontenido. Si segno falta, se declara el hueco en vez de romper:
    el lector ve que había un QR y cuál era su destino."""
    try:
        import segno
        import io
        q = segno.make(dato, error="m")
        # segno escribe BYTES: con un buffer de texto revienta (medido).
        buf = io.BytesIO()
        q.save(buf, kind="svg", scale=1, border=2, xmldecl=False, svgns=True,
               omitsize=True, dark="#17140d", light=None)
        svg = buf.getvalue().decode("utf-8")
    except ImportError:
        svg = ('<div class="qr-hueco">QR no generado: falta la librería '
               "<code>segno</code></div>")
    destino = esc(dato)
    pie_html = ('<figcaption class="qr-pie">' + esc(pie) + "</figcaption>") if pie else ""
    return (
        '<figure class="viz qr-bloque" style="--qr-mm:' + str(int(tam_mm)) + '">'
        '<div class="qr-lienzo">' + svg + "</div>"
        '<div class="qr-lado">' + pie_html
        + '<a class="qr-url" href="' + destino + '">' + destino + "</a></div>"
        "</figure>")


# ── parser de los bloques en Markdown-Golden ───────────────────────────────────
def _pares(lineas, sep="|"):
    out = []
    for ln in lineas:
        if not ln.strip() or sep not in ln:
            continue
        partes = [p.strip() for p in ln.split(sep)]
        out.append(partes)
    return out


def render_bloque(nombre, titulo, cuerpo):
    """Convierte un bloque ::: <nombre> ... ::: en su componente.
    Devuelve None si el nombre no es un visual (para que el llamador lo trate
    como bloque de estilo normal)."""
    n = nombre.lower()
    lineas = cuerpo.split("\n")

    if n == "kpi":
        items = []
        for p in _pares(lineas):
            items.append({"etiqueta": p[0],
                          "valor": p[1] if len(p) > 1 else "",
                          "nota": p[2] if len(p) > 2 else "",
                          "tono": p[3] if len(p) > 3 else ""})
        return kpi(items)

    if n in ("barras", "grafico", "gráfico"):
        filas, unidad = [], ""
        for p in _pares(lineas):
            if p[0].lower() in ("unidad", "unidades") and len(p) > 1:
                unidad = p[1]; continue
            try:
                filas.append((p[0], float(str(p[1]).replace(",", "."))))
            except (ValueError, IndexError):
                continue
        return barras(filas, unidad, titulo)

    if n in ("escala", "medidor", "meta"):
        d = {}
        for p in _pares(lineas, ":"):
            if len(p) > 1:
                d[p[0].lower()] = p[1]
        try:
            return escala(float(d.get("actual", 0)), float(d.get("meta", 1)),
                          titulo, d.get("unidad", ""))
        except ValueError:
            return None

    if n in ("comparativa", "antesdespues", "antes-despues"):
        filas, unidad = [], ""
        for p in _pares(lineas):
            if p[0].lower() in ("unidad", "unidades") and len(p) > 1:
                unidad = p[1]; continue
            try:
                filas.append((p[0], float(str(p[1]).replace(",", ".")),
                              float(str(p[2]).replace(",", "."))))
            except (ValueError, IndexError):
                continue
        return comparativa(filas, unidad, titulo)

    if n in ("pasos", "esquema", "flujo"):
        items = []
        for ln in lineas:
            if not ln.strip():
                continue
            if "|" in ln:
                a, b = ln.split("|", 1)
                items.append((a.strip(), b.strip()))
            else:
                items.append(ln.strip())
        return pasos(items, titulo)

    if n == "qr":
        texto = "\n".join(l for l in lineas if l.strip())
        if "|" in texto:
            dato, pie = texto.split("|", 1)
            return qr(dato.strip(), pie.strip())
        return qr(texto.strip(), titulo)

    return None


NOMBRES = ("kpi", "barras", "grafico", "gráfico", "escala", "medidor", "meta",
           "comparativa", "antesdespues", "antes-despues", "pasos", "esquema",
           "flujo", "qr")
