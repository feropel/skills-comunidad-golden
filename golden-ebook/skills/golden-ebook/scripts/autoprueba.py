#!/usr/bin/env python3
"""autoprueba.py · golden-ebook

Prueba el motor y el verificador en las DOS direcciones: que la muestra sana
salga ENTREGABLE y que cada sabotaje sea cazado por la comprobación que le toca.
Un verificador que nunca falla no protege; uno que falla con lo sano, estorba.

Uso:  $PY scripts/autoprueba.py        (imprime TODO OK con N de N, o qué falló)
Códigos: 0 todo OK · 1 algún caso no dio lo esperado.
"""
import copy
import shutil
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MUESTRA = os.path.join(RAIZ, "assets", "muestra", "ebook.json")
PY = sys.executable


def correr(args):
    r = subprocess.run([PY] + args, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def estados(salida):
    out = {}
    for linea in salida.splitlines():
        partes = linea.split()
        if len(partes) >= 2 and partes[0] in ("OK", "AVISO", "FALLA", "N/D"):
            out[partes[1]] = partes[0]
    return out


def main():
    base = json.load(open(MUESTRA, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="ebook-auto-")
    # Los recursos de la muestra (logo) viajan con ella: las rutas del JSON son relativas.
    for f in os.listdir(os.path.dirname(MUESTRA)):
        if not f.endswith(".json"):
            shutil.copy(os.path.join(os.path.dirname(MUESTRA), f), tmp)
    construir = os.path.join(AQUI, "construir_ebook.py")
    verificar = os.path.join(AQUI, "verificar_ebook.py")

    def escribir(e, nombre):
        ruta = os.path.join(tmp, nombre + ".json")
        json.dump(e, open(ruta, "w", encoding="utf-8"), ensure_ascii=False)
        return ruta

    sano_json = escribir(base, "sano")
    sano_pdf = os.path.join(tmp, "sano.pdf")
    code, out = correr([construir, sano_json, sano_pdf])
    revisar = os.path.join(AQUI, "revision_fuentes.py")
    hoja_ruta = os.path.join(tmp, "revision-fuentes.json")

    import re as _re
    sys.path.insert(0, AQUI)
    from verificar_ebook import REF as _REF
    carpeta_f = os.path.join(tmp, "fuentes-texto")

    def hoja_completa(e_json=None):
        correr([revisar, sano_json])
        hoja = json.load(open(hoja_ruta, encoding="utf-8"))
        sinteticas = {}
        for f in hoja["frases"]:
            refs = f.get("fuentes") or []
            fuente = refs[0] if refs else "1"
            limpia = _REF.sub("", f["frase"]).strip()
            sinteticas.setdefault(fuente, []).append(f"FIXTURE {f['id']}: {limpia} 12345.")
            f.update(estado="fiel", fuente_usada=fuente, cita_fuente=f"FIXTURE {f['id']}: {limpia} 12345.")
        os.makedirs(carpeta_f, exist_ok=True)
        for fu in (str(x.get("id")) for x in base["fuentes"]):
            with open(os.path.join(carpeta_f, f"{fu}.txt"), "w", encoding="utf-8") as out:
                out.write("# fuente sintética de la autoprueba\n\n" + "\n".join(sinteticas.get(fu, ["vacía"])))
        hoja["puente"] = {"estado": "revisado", "nota": "fixture: puente revisado en el ebook real"}
        json.dump(hoja, open(hoja_ruta, "w", encoding="utf-8"), ensure_ascii=False)
    hoja_completa()
    resultados = []
    if code != 0:
        print("El motor no construyó la muestra sana:\n" + out)
        shutil.rmtree(tmp, ignore_errors=True)
        sys.exit(1)

    def caso(nombre, mutar, esperado_id, esperado_estado, pdf_propio=None, extra=None):
        e = copy.deepcopy(base)
        mutar(e)
        j = escribir(e, nombre)
        pdf = sano_pdf
        if pdf_propio:
            pdf = os.path.join(tmp, nombre + ".pdf")
            c, o = correr([construir, j, pdf] + (extra or []))
            if c != 0:
                resultados.append((nombre, False, f"el motor no construyó: {o[:200]}"))
                return
        c, o = correr([verificar, j, pdf])
        st = estados(o).get(esperado_id)
        ok = st == esperado_estado
        resultados.append((nombre, ok, f"{esperado_id} esperado {esperado_estado}, salió {st}"))

    # 0. Control: la muestra sana no tiene fallas.
    c, o = correr([verificar, sano_json, sano_pdf])
    est = estados(o)
    no_ok = {k: v for k, v in est.items() if v != "OK"}
    resultados.append(("0 muestra sana → ENTREGABLE sin avisos", c == 0 and not no_ok,
                       f"exit {c}, no OK: {no_ok}"))
    resultados.append(("0b logo presente → P6 OK", est.get("P6") == "OK", f"P6 salió {est.get('P6')}"))

    p0 = lambda e: e["capitulos"][0]["bloques"][0]  # noqa: E731
    caso("1 cita a fuente inexistente", lambda e: p0(e).update(texto=p0(e)["texto"] + " Dato [99]."), "C2", "FALLA")
    caso("2 dato sin fuente", lambda e: e["capitulos"][0]["bloques"].append(
        {"tipo": "dato", "cifra": "7", "texto": "de cada 10 personas"}), "C3", "FALLA")
    caso("3 claim prohibido del producto", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Este producto hace crecer el cabello."), "C7", "FALLA")
    caso("4 claim terapéutico genérico", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Es un remedio milagroso."), "C7", "FALLA")
    caso("5 marcador sin llenar", lambda e: e["cierre"].update(texto="Escríbenos al [WHATSAPP PENDIENTE]."),
         "C8", "FALLA")
    caso("6 pregunta sin signo de apertura", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Qué pasa si no lo haces?"), "C9", "FALLA")
    caso("7 línea de rayas separadora", lambda e: p0(e).update(texto=p0(e)["texto"] + "\n---\nSigue."),
         "C10", "FALLA")
    caso("8 acento de texto sin contraste", lambda e: e["marca"]["colores"].update(acento_texto="#e9c46a"),
         "C13", "FALLA")
    caso("9 catálogo disfrazado", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Producto Demo, Producto Demo y Producto Demo."), "C11", "AVISO")
    caso("10 letra ilegible en el celular", lambda e: None, "P4", "FALLA", pdf_propio=True,
         extra=["--cuerpo-pt", "9"])
    # Lado bueno: lo que NO debe morder.
    caso("11 negación permitida (no cura)", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Ningún cosmético cura la alopecia, y este tampoco lo promete."), "C7", "OK")
    caso("14 'Sin duda, cura' no se disfraza de negación", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Sin duda, cura la alopecia."), "C7", "FALLA")
    caso("12 la palabra 'todo' no es marcador", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Todo esto es normal y todo tiene explicación."), "C8", "OK")

    caso("15 claim del producto negado y luego afirmado", lambda e: p0(e).update(
        texto=p0(e)["texto"] + " Ningún champú detiene la caída. Pero este producto detiene la caída."),
        "C7", "FALLA")
    caso("16 acento ilegible sobre el primario", lambda e: e["marca"]["colores"].update(acento="#1a3a55"),
         "C13", "FALLA")
    caso("17 menos de 3 capítulos", lambda e: e.update(capitulos=e["capitulos"][:2]), "C1", "FALLA")
    caso("18 menos de 5 fuentes", lambda e: e.update(fuentes=e["fuentes"][:3]), "C5", "FALLA")

    def corto(e):
        for c in e["capitulos"]:
            c["bloques"] = [{"tipo": "parrafo", "texto": "Texto breve [1]."}]
    caso("19 libro demasiado corto", corto, "C12", "FALLA")
    caso("20 carta que desborda su página", lambda e: e["bienvenida"].update(
        texto=" ".join(["palabra"] * 120)), "C16", "AVISO")
    caso("21 portada sin logo → aviso", lambda e: e["marca"].pop("logo"), "P6", "AVISO", pdf_propio=True)

    # 24 a 39: los sabotajes que la verificación adversarial de EB1.1 logró colar.
    mas = lambda txt: (lambda e: p0(e).update(texto=p0(e)["texto"] + " " + txt))  # noqa: E731
    caso("24 claim por sinónimo (frena, estimula)", mas("Frena la caída y estimula el crecimiento."), "C7", "FALLA")
    caso("25 claim 'trata tu alopecia'", mas("Esto trata tu alopecia."), "C7", "FALLA")
    caso("26 claim conjugado 'detener la caída'", mas("Ayuda a detener la caída."), "C7", "FALLA")
    caso("27 negación falsa a través de dos puntos", mas("No lo dudes más: esto hace crecer el pelo."),
         "C7", "FALLA")
    caso("28 claim en un rótulo que se imprime", lambda e: e["cierre"].update(kicker="CURA LA ALOPECIA HOY"),
         "C7", "FALLA")
    caso("29 verbo de efecto en el botón", lambda e: e["cierre"]["cta"].update(texto="Compra y recupera tu pelo"),
         "C7", "FALLA")
    caso("30 texto en inglés", mas("This is the best way to care for your hair and the results are great."),
         "C18", "FALLA")
    caso("31 apertura sin cierre", mas("¿Sabías que esto pasa."), "C9", "FALLA")
    caso("32 pregunta sin apertura en un rótulo", lambda e: e["cierre"].update(kicker="Y AHORA QUE?"),
         "C9", "FALLA")
    caso("33 doble puntuación", mas("Qué curioso!."), "C9", "FALLA")
    caso("34 URL de fuente vacía", lambda e: e["fuentes"][0].update(url="https://"), "C6", "FALLA")
    caso("35 porcentaje sin fuente", mas("El 85 % de las personas lo nota."), "C3", "FALLA")
    caso("40 porcentaje con su cita tras un punto y coma", mas("Subió del 50 % al 60 %; en las ciudades se estancó [1]."),
         "C3", "OK")
    caso("36 texto sin tildes", mas("Tambien pasa despues de un dia largo."), "C17", "FALLA")
    caso("37 bloque de tipo inexistente", lambda e: e["capitulos"][0]["bloques"].append(
        {"tipo": "tabla", "texto": "inocuo"}), "C19", "FALLA")
    caso("38 catálogo con 5 menciones", mas("Producto Demo, Producto Demo, Producto Demo, Producto Demo y "
                                           "Producto Demo."), "C11", "FALLA")
    caso("39 alusión al pedido dentro de un capítulo", lambda e: e["capitulos"][0].update(
        cierre="Y para verte bien hoy ya tienes algo en camino."), "C11", "AVISO")

    # 41 a 60: segunda auditoría y segunda verificación adversarial (EB1.3).
    caso("41 'no solo cura' no es negación", mas("No solo cura la alopecia: también la previene."), "C7", "FALLA")
    caso("42 claim escondido en el aviso", lambda e: e.update(aviso="Producto Demo cura la alopecia."), "C7", "FALLA")
    caso("43 datos privados", lambda e: e["bienvenida"].update(
        texto=e["bienvenida"]["texto"] + "\n\nEscríbele al 300 123 4567 o a juan.perez@gmail.com."), "C20", "FALLA")
    caso("44 cifra en palabras sin fuente", mas("El 40 por ciento lo nota antes de los 35 años."), "C3", "FALLA")
    caso("45 'este producto previene' en un capítulo", mas("Este producto previene la calvicie."), "C7", "FALLA")
    caso("46 catálogo genérico", mas("Nuestro producto es ideal. Nuestro producto funciona. Nuestro producto llega hoy. "
                                     "Pide nuestro producto. Nuestro producto gusta."), "C11", "FALLA")
    caso("47 fecha de consulta futura", lambda e: e["fuentes"][0].update(consultado="2099-01-01"), "C6", "FALLA")
    caso("48 nivel A sin justificar", lambda e: e["fuentes"][0].update(
        url="https://miblogdeventas.com/pelo", nivel="A", nivel_porque=""), "C21", "AVISO")
    caso("49 negación lejana ('Nunca fue tan fácil...')", mas("Nunca fue tan fácil hacer crecer tu cabello."),
         "C7", "FALLA")
    caso("50 verbo nuevo en el cierre ('combate')", lambda e: e["cierre"].update(
        texto="Esto combate la calvicie."), "C7", "FALLA")
    caso("51 palabra partida con guion suave", mas("Esto hace cre\u00adcer el pelo."), "C8", "FALLA")
    caso("52 cifra con miles sin fuente", mas("Más de 3.000 personas lo usan."), "C3", "FALLA")
    caso("53 palabras sin tilde fuera de la lista", mas("Es la opcion mas economica."), "C17", "FALLA")
    caso("54 inglés sin palabras de la lista corta", mas("Stay confident every single day."), "C18", "FALLA")
    caso("55 marcador genérico sin llenar", mas("Escribe a <NUMERO DE WHATSAPP> o a [NOMBRE DEL ASESOR]."),
         "C8", "FALLA")
    caso("56 separador de caracteres de caja", mas("\n━━━━━━\nSigue."), "C10", "FALLA")
    caso("57 'agua potable' junto al producto", lambda e: e["cierre"].update(texto="Te deja agua potable."),
         "C7", "FALLA")
    # Lado bueno: lo que la versión anterior acusaba en falso.
    caso("58 homógrafo sin tilde ('seria')", mas("Es una decisión seria."), "C17", "OK")
    caso("59 abreviatura no corta la pregunta", mas("¿Sabías que en EE. UU. pasa lo mismo?"), "C9", "OK")
    caso("60 'garantizado' lejos del producto", mas("Es un derecho garantizado por la Constitución."), "C7", "OK")
    caso("61 título de obra en inglés, en cursiva", mas("El artículo se llama *The effect of the sun on your skin*."),
         "C18", "OK")
    caso("62 'milagro' como figura, lejos del producto", mas("Parece un milagro, pero es biología."), "C7", "OK")

    # 67 a 90: tercera auditoría y tercera verificación adversarial (EB1.4).
    caso("67 claim en la nota de IA impresa", lambda e: e.update(nota_ia="Este libro cura la alopecia."), "C7", "FALLA")
    caso("68 verbos nuevos junto al producto", lambda e: e["cierre"].update(texto="Alivia y calma el cuero cabelludo."),
         "C7", "FALLA")
    caso("69 datos privados en una fuente", lambda e: e["fuentes"][0].update(editor="Escribe a juan@gmail.com"),
         "C20", "FALLA")
    caso("70 enlace con número de plantilla", lambda e: e["cierre"]["cta"].update(url="https://wa.me/57XXXXXXXXXX"),
         "C8", "FALLA")
    caso("71 letra cirílica en 'cura'", mas("Esto с\u0443ra."), "C8", "FALLA")
    caso("72 'no dudes que' no es negación", mas("No dudes que cura la alopecia."), "C7", "FALLA")
    caso("73 cifra en palabras sin fuente", mas("Tres de cada cuatro personas lo notan."), "C3", "FALLA")
    caso("74 teléfono de otro país", mas("Llama al +52 55 1234 5678."), "C20", "FALLA")
    caso("75 fecha imposible", lambda e: e["fuentes"][0].update(consultado="2026-02-30"), "C6", "FALLA")
    caso("76 formato a5 en el celular → aviso", lambda e: e["meta"].update(formato="a5"), "P4", "AVISO",
         pdf_propio=True)
    # Lado bueno.
    caso("77 precio no es cifra sin fuente", mas("Cuesta $ 45.900."), "C3", "OK")
    caso("78 correo de la propia empresa con web www", lambda e: (e["marca"].update(web="www.example.com"),
         e["cierre"].update(texto="Escríbenos a hola@example.com.")), "C20", "OK")
    caso("79 abreviatura 'vs.'", mas("¿Es mejor el peine vs. el cepillo? Depende."), "C9", "OK")

    # 80 · logo SVG: se rasteriza y se mide como imagen.
    svg = os.path.join(tmp, "logo.svg")
    open(svg, "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 100">'
                         '<rect width="300" height="100" fill="#e9a23b"/></svg>')
    caso("80 logo SVG → se ve y se mide", lambda e: e["marca"].update(logo="logo.svg"), "P13", "OK", pdf_propio=True)
    # 81 · logo de 3000 x 40 px: su lado menor no se lee.
    from PIL import Image
    Image.new("RGBA", (3000, 40), (233, 162, 59, 255)).save(os.path.join(tmp, "logo-fino.png"))
    caso("81 logo demasiado fino", lambda e: e["marca"].update(logo="logo-fino.png"), "P13", "FALLA", pdf_propio=True)

    # 82 a 86 · compuertas que se intentaron burlar sin revisar nada.
    hoja = json.load(open(hoja_ruta, encoding="utf-8"))
    for f in hoja["frases"]:
        f["cita_fuente"] = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
    json.dump(hoja, open(hoja_ruta, "w", encoding="utf-8"), ensure_ascii=False)
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("82 hoja con citas inventadas → C25 FALLA", estados(o).get("C25") == "FALLA",
                       f"C25 {estados(o).get('C25')}"))
    hoja_completa()
    hoja = json.load(open(hoja_ruta, encoding="utf-8"))
    con_numero = next(f for f in hoja["frases"] if _re.search(r"\d", _REF.sub("", f["frase"])))
    con_numero.update(estado="sin afirmacion", cita_fuente="")
    json.dump(hoja, open(hoja_ruta, "w", encoding="utf-8"), ensure_ascii=False)
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("83 frase con número como 'sin afirmacion' → C25 FALLA", estados(o).get("C25") == "FALLA",
                       f"C25 {estados(o).get('C25')}"))
    hoja_completa()
    # 84 · PDF con un claim, sellado a mano con el sha del JSON limpio.
    malo = copy.deepcopy(base)
    malo["capitulos"][0]["bloques"][0]["texto"] += " Este remedio milagroso cura la alopecia."
    malo_json = escribir(malo, "malo")
    malo_pdf = os.path.join(tmp, "malo.pdf")
    correr([construir, malo_json, malo_pdf])
    from pypdf import PdfReader, PdfWriter
    import hashlib
    wr = PdfWriter(clone_from=PdfReader(malo_pdf))
    wr.add_metadata({"/EbookJSONSHA256": hashlib.sha256(open(sano_json, "rb").read()).hexdigest()})
    sellado = os.path.join(tmp, "sellado-a-mano.pdf")
    with open(sellado, "wb") as fh:
        wr.write(fh)
    c, o = correr([verificar, sano_json, sellado])
    est = estados(o)
    resultados.append(("84 PDF sellado a mano con un claim → P14 FALLA", est.get("P14") == "FALLA",
                       f"P12 {est.get('P12')}, P14 {est.get('P14')}"))
    # 85 · un título nuevo agregado después de revisar: entra a la hoja y queda sin revisar.
    otro = copy.deepcopy(base)
    otro["capitulos"][0]["titulo"] = "Un título nuevo que afirma 10 cosas"
    json.dump(otro, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    correr([revisar, sano_json])
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("85 título agregado después de revisar → C25 FALLA", estados(o).get("C25") == "FALLA",
                       f"C25 {estados(o).get('C25')}"))
    json.dump(base, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    hoja_completa()
    # 86 y 87 · un claim que no lo es: FALLA sin excepción, AVISO visible con excepción revisada.
    fp = copy.deepcopy(base)
    fp["capitulos"][0]["bloques"][0]["texto"] += " Solo un dermatólogo puede tratar la alopecia."
    json.dump(fp, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    hoja_completa()
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("86 falso positivo sin excepción → C7 FALLA", estados(o).get("C7") == "FALLA",
                       f"C7 {estados(o).get('C7')}"))
    hoja = json.load(open(hoja_ruta, encoding="utf-8"))
    for f in hoja["frases"]:
        if f["frase"].startswith("Solo un dermatólogo"):
            f["excepcion_claim"] = "Remite al médico; no atribuye al producto ningún efecto sobre la alopecia."
    json.dump(hoja, open(hoja_ruta, "w", encoding="utf-8"), ensure_ascii=False)
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("87 con excepción revisada → C7 AVISO (visible, no OK)", estados(o).get("C7") == "AVISO",
                       f"C7 {estados(o).get('C7')}"))
    json.dump(base, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    hoja_completa()

    # 63 a 66: la hoja del Paso 5b y el sello del PDF.
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("63 hoja completa y del mismo JSON → C25 OK", estados(o).get("C25") == "OK",
                       f"C25 salió {estados(o).get('C25')}"))
    hoja = json.load(open(hoja_ruta, encoding="utf-8"))
    hoja["frases"][0]["estado"] = "PENDIENTE"
    json.dump(hoja, open(hoja_ruta, "w", encoding="utf-8"), ensure_ascii=False)
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("64 una frase sin revisar → C25 FALLA", estados(o).get("C25") == "FALLA",
                       f"C25 salió {estados(o).get('C25')}"))
    hoja_completa()
    otro = copy.deepcopy(base)
    otro["meta"]["subtitulo"] += " Edición corregida."
    json.dump(otro, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    c, o = correr([verificar, sano_json, sano_pdf])
    est = estados(o)
    resultados.append(("65 JSON cambiado después → C25 y P12 FALLA",
                       est.get("C25") == "FALLA" and est.get("P12") == "FALLA", f"C25 {est.get('C25')}, P12 {est.get('P12')}"))
    json.dump(base, open(sano_json, "w", encoding="utf-8"), ensure_ascii=False)
    hoja_completa()
    c, o = correr([verificar, sano_json, sano_pdf])
    resultados.append(("66 restaurado → C25 y P12 OK", estados(o).get("C25") == "OK" and estados(o).get("P12") == "OK",
                       f"C25 {estados(o).get('C25')}, P12 {estados(o).get('P12')}"))

    # 22. Marcadores ausentes: se le quitan al PDF sano.
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for pg in PdfReader(sano_pdf).pages:
        w.add_page(pg)
    sin_marc = os.path.join(tmp, "sin-marcadores.pdf")
    with open(sin_marc, "wb") as f:
        w.write(f)
    c, o = correr([verificar, sano_json, sin_marc])
    st = estados(o).get("P11")
    resultados.append(("22 PDF sin marcadores → P11 aviso", st == "AVISO", f"P11 salió {st}"))

    # 23. Si falta una librería, el veredicto es NO VERIFICADO (exit 3), nunca ENTREGABLE.
    envoltura = ("import sys, runpy; sys.modules['pypdf'] = None; "
                 f"sys.argv = ['v', {sano_json!r}, {sano_pdf!r}]; "
                 f"runpy.run_path({verificar!r}, run_name='__main__')")
    c, o = correr(["-c", envoltura])
    resultados.append(("23 falta pypdf → NO VERIFICADO", c == 3 and "NO VERIFICADO" in o, f"exit {c}"))

    # 13. El motor se niega sin identidad (la identidad se pide, no se hereda).
    e = copy.deepcopy(base)
    e["marca"].pop("nombre")
    j = escribir(e, "sin-marca")
    c, o = correr([construir, j, os.path.join(tmp, "sin-marca.pdf")])
    resultados.append(("13 sin marca.nombre → el motor se niega", c == 2, f"exit {c}"))

    buenos = sum(1 for _, ok, _ in resultados if ok)
    for nombre, ok, det in resultados:
        print(f"{'OK  ' if ok else 'MAL '} {nombre} · {det}")
    total = len(resultados)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{'TODO OK' if buenos == total else 'HAY FALLOS'} · {buenos} de {total}")
    sys.exit(0 if buenos == total else 1)


if __name__ == "__main__":
    main()
