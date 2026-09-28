#!/usr/bin/env python3
"""
autoprueba_deck.py — prueba a verificar_deck.py contra casos que SE SABE que
son malos y contra casos que SE SABE que son buenos.

Ley de la casa (2026-09-02, mandato de FER): un validador sin autoprueba es una
opinion con sintaxis, y se prueba en las DOS direcciones. Un detector agresivo
hace tanto daño como uno ciego y cuesta mas descubrirlo.

Cada caso malo sale de un fallo real: la plantilla sin rellenar, el placeholder
sustituido a medias (por reemplazar de la clave corta a la larga), la atmosfera
inventada que deja el fondo muerto, el titulo vacio y los acentos sin poner.

El deck BUENO se construye rellenando la plantilla REAL de la skill, asi que
esta autoprueba tambien comprueba que el motor produce un deck entregable de
punta a punta, no solo que el verificador opina.
"""
import io, os, re, sys, subprocess, tempfile, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
BASE = os.path.join(SKILL, "assets", "deck-base.html")
VERIF = os.path.join(AQUI, "verificar_deck.py")

VALORES = {
    "GP_ATMOSFERA": "enjambre", "GP_MARCA": "Marca Demo",
    "GP_ACENTO_HEX": "d9a441",
    "GP_TITULO": "Título de la presentación", "GP_SUBTITULO": "Subtítulo con acentuación correcta",
    "GP_ETIQUETA": "Demo", "GP_FECHA": "Septiembre 2026",
    "GP_DESCRIPCION": "Descripción breve de la presentación para el enlace compartido.",
    "GP_LOGO_URI": "", "GP_CONTEXTO": "Contexto de la charla, con su acentuación en orden.",
    "GP_FRASE": "Una frase que resume la idea central.",
    "GP_CITA": "Una cita breve y verificable.", "GP_AUTOR_CITA": "Autor de la cita",
    "GP_CIFRA": "22", "GP_UNIDAD": "países", "GP_TITULO_TARJETAS": "Las tres piezas",
    "GP_T1": "Primera", "GP_T2": "Segunda", "GP_T3": "Tercera",
    "GP_D1": "Descripción de la primera pieza.", "GP_D2": "Descripción de la segunda pieza.",
    "GP_D3": "Descripción de la tercera pieza.", "GP_TITULO_PROCESO": "Cómo funciona",
    "GP_P1": "Paso uno", "GP_P2": "Paso dos", "GP_P3": "Paso tres", "GP_P4": "Paso cuatro",
    "GP_PD1": "Detalle del paso uno.", "GP_PD2": "Detalle del paso dos.",
    "GP_PD3": "Detalle del paso tres.", "GP_PD4": "Detalle del paso cuatro.",
    "GP_TITULO_COMPARACION": "Antes y después", "GP_LADO_A": "Antes", "GP_LADO_B": "Después",
    "GP_A1": "Punto uno", "GP_A2": "Punto dos", "GP_A3": "Punto tres",
    "GP_B1": "Punto uno", "GP_B2": "Punto dos", "GP_B3": "Punto tres",
    "GP_VISUAL_TITULO": "El esquema", "GP_VISUAL_TEXTO": "Explicación del esquema.",
    "GP_VISUAL_IMG": "", "GP_VISUAL_ALT": "Esquema de la operación",
    "GP_PANTALLA_TITULO": "En vivo", "GP_PANTALLA_IMG": "",
    "GP_PANTALLA_ALT": "Captura de pantalla", "GP_PANTALLA_URL": "https://example.com",
    "GP_CIERRE": "La conclusión de la presentación.",
    "GP_CTA_TEXTO": "Ver más", "GP_CTA_URL": "https://example.com",
    "GP_CONTACTO": "example.com",
}


def deck_bueno():
    """Rellena la plantilla REAL, de la clave mas larga a la mas corta."""
    t = open(BASE, encoding="utf-8").read()
    for k in sorted(VALORES, key=len, reverse=True):
        t = t.replace(k, VALORES[k])
    return t


def corre(ruta):
    r = subprocess.run([sys.executable, VERIF, ruta], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def _documentacion_viva(texto):
    """Quita lo que PARECE documentacion pero no manda a nadie.

    Lo pidio el Centro de Mando y tenia razon: el lado bueno de una prueba no
    puede ser solo prosa legitima, tiene que incluir el CASO DISFRAZADO, escrito
    con la sintaxis exacta del dato real. Medido: la version anterior acuso a los
    tres disfraces que probe.
      · bloque de codigo cercado -> suele ser un CONTRAEJEMPLO ("esto NO se
        escribe"), y acusarlo castiga justo a quien documenta el error;
      · cita en bloque (">")     -> es historia o el catalogo de OTRA skill.
    Lo que queda es lo que un lector tomaria como instruccion vigente.
    """
    fuera, dentro = [], False
    for linea in texto.split("\n"):
        if linea.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if dentro or linea.lstrip().startswith(">"):
            continue
        fuera.append(linea)
    return "\n".join(fuera)


def _sin_tildes(s):
    for a, b in (("\u00e1","a"),("\u00e9","e"),("\u00ed","i"),
                 ("\u00f3","o"),("\u00fa","u")):
        s = s.replace(a, b)
    return s


def coherencia_docs_motor():
    """Comprueba que los nombres de atmosfera escritos en la documentacion
    existan de verdad en el motor.

    Fallo que obliga a esto (2026-09-05): SKILL.md anunciaba nueve atmosferas y
    listaba una llamada `retabla` que el motor NO implementaba (habia quedado un
    `ATM.retabla = null`, dedazo de `reticula`). Quien siguiera la documentacion
    al pie de la letra se llevaba un fondo MUERTO.

    POR QUE ESTE CHEQUEO SE REESCRIBIO EL MISMO DIA QUE SE ESCRIBIO. La primera
    version buscaba listas en negrita en cualquier linea que hablara de
    atmosferas. Mordia el caso malo, asi que parecia buena. Probada en el otro
    sentido, acuso a "oro, cian, magenta", a "outfit, gloock, tektur" y a
    "elegir, calmar, apagar": 3 de 3 falsos positivos. Estaba acusando al
    IDIOMA, no al defecto (ley del Centro de Mando, 2026-09-05).

    Esta version no lee prosa. Se agarra de DOS anclas sintacticas:
      · lo que va entre comillas en un `data-atmosfera="X"`, que solo puede ser
        un nombre de atmosfera;
      · los tokens entre acentos graves del parrafo que abre la seccion
        "Atmosferas disponibles" — un acento grave significa "esto se escribe
        tal cual", asi que ahi no cabe una palabra del idioma.
    Y ademas mira la COBERTURA al reves: que ninguna atmosfera del motor se
    quede sin documentar, para que no se pueda añadir una en silencio.
    """
    sys.path.insert(0, AQUI)
    import verificar_deck
    motor = verificar_deck.atmosferas_del_motor()
    pruebas = []
    pruebas.append(("la lista del motor se puede derivar de assets/atmosferas.js",
                    bool(motor), "no pude leer `Atmosfera.lista`",
                    "lee la LISTA declarada; no comprueba que cada una PINTE: "
                    "eso pide un navegador real"))
    if not motor:
        return pruebas

    def catalogo(texto):
        """Tokens entre acentos graves de la linea marcada como catalogo.

        El ancla es la etiqueta literal "Catalogo del motor:", no la posicion.
        Probado: coger "el primer parrafo tras el titulo" acusaba a cualquier
        frase que alguien metiera ahi. Y el ancla va VISIBLE en el texto, nunca
        dentro de un comentario HTML: un comentario ya se trago esta seccion
        entera una vez.
        """
        nombres = []
        for linea in _documentacion_viva(texto).split("\n"):
            # AL PRINCIPIO de la linea: el catalogo abre su propia linea. Si el
            # marcador va a media frase es una MENCION, no el catalogo.
            if not _sin_tildes(linea).startswith("Catalogo del motor:"):
                continue
            # Solo minusculas puras: deja fuera `Atmosfera.lista` y `assets/x.js`.
            nombres += [x for x in re.findall(r"`([^`]+)`", linea)
                        if re.match(r"^[a-z]+$", x)]
        return nombres

    for rel in ("SKILL.md", os.path.join("references", "atmosferas.md")):
        ruta = os.path.join(SKILL, rel)
        if not os.path.isfile(ruta):
            continue
        texto = io.open(ruta, encoding="utf-8").read()
        vivo = _documentacion_viva(texto)
        citados = set(re.findall(r'data-atmosfera=["\']([a-z]+)', vivo))
        citados.update(catalogo(texto))
        intrusos = sorted(n for n in citados if n not in motor)
        pruebas.append(("%s no nombra ninguna atmosfera que el motor no tenga" % rel,
                        not intrusos,
                        "nombres que el motor no implementa: %s" % ", ".join(intrusos),
                        "mira `data-atmosfera=` y la linea `Catalogo del motor:`; "
                        "un nombre suelto en prosa NO se revisa, a proposito"))

    # Al reves: que no se pueda añadir NI QUITAR una atmosfera en silencio.
    doc = io.open(os.path.join(SKILL, "references", "atmosferas.md"),
                  encoding="utf-8").read()
    sueltas = sorted(n for n in motor if n != "ninguna" and n not in doc)
    pruebas.append(("ninguna atmosfera del motor falta en references/atmosferas.md",
                    not sueltas,
                    "estan en el motor y no en el mapa: %s" % ", ".join(sueltas),
                    "comprueba que el NOMBRE aparezca; no que lo que se dice de "
                    "el sea cierto"))

    cat = set(catalogo(io.open(os.path.join(SKILL, "SKILL.md"),
                               encoding="utf-8").read()))
    faltan = sorted(n for n in motor if n not in cat)
    pruebas.append(("el catalogo de SKILL.md nombra las %d del motor" % len(motor),
                    not faltan,
                    "el motor las tiene y el catalogo no: %s" % ", ".join(faltan),
                    "exige que esten TODAS; no juzga el orden ni la descripcion"))
    return pruebas


def main():
    if not os.path.exists(BASE):
        print("  no encuentro assets/deck-base.html"); return 2
    tmp = tempfile.mkdtemp(prefix="autoprueba-deck-")
    bueno = deck_bueno()
    sobran = sorted(set(re.findall(r"GP_[A-Z0-9_]+", bueno)))
    casos = []
    try:
        def guarda(nombre, contenido):
            p = os.path.join(tmp, nombre)
            open(p, "w", encoding="utf-8").write(contenido)
            return p

        # ---- BUENO: el motor produce un deck entregable ----
        casos.append(("no dispara: deck completo salido de la plantilla real",
                      guarda("bueno.html", bueno), 0, None))

        # ---- MALOS: cada uno es un fallo real ya pagado ----
        casos.append(("caza: plantilla SIN rellenar",
                      guarda("crudo.html", open(BASE, encoding="utf-8").read()), 1, "placeholders"))
        casos.append(("caza: placeholder sustituido A MEDIAS",
                      guarda("medias.html", bueno.replace("Cómo funciona", "_PROCESO")), 1, "medias"))
        casos.append(("caza: atmosfera inventada (fondo muerto)",
                      guarda("atmos.html", bueno.replace('data-atmosfera="enjambre"',
                                                         'data-atmosfera="galaxia"')), 1, "atmosfera"))
        vacio = re.sub(r"<title>.*?</title>", "<title></title>", bueno, flags=re.S)
        casos.append(("caza: title vacio", guarda("title.html", vacio), 1, "title"))
        casos.append(("caza: acentos SIN poner en el texto visible",
                      guarda("acentos.html",
                             bueno.replace("Descripción", "Descripcion")
                                  .replace("Explicación", "Explicacion")
                                  .replace("conclusión", "conclusion")
                                  .replace("acentuación", "acentuacion")), 1, "Acentos"))

        # ---- AMBIGUAS verbo/sustantivo: NO deben bloquear (falso positivo real
        # del 2026-09-03: 'publica' bloqueo un deck correcto y hubo que reescribirlo)
        ctx = "Contexto de la charla, con su acentuación en orden."
        casos.append(("no bloquea: 'el sistema publica gratis' (verbo, va sin tilde)",
                      guarda("verbo1.html", bueno.replace(ctx, "El sistema publica gratis cada semana.")), 0, None))
        casos.append(("no bloquea: 'la empresa practica esto' (verbo, va sin tilde)",
                      guarda("verbo2.html", bueno.replace(ctx, "La empresa practica esto a diario.")), 0, None))
        casos.append(("caza: 'informacion' sin tilde (inequivoca, siempre lleva)",
                      guarda("inequiv.html", bueno.replace(ctx, "La informacion del cliente llega tarde.")), 1, "Acentos"))

        # ---- CSS que NO llego a entrar (fallo real del 2026-09-03 reportado por
        # el chat del Cartel: un replace con el ancla equivocada fallo en silencio,
        # el HTML tenia las clases y el CSS ni una regla, y el verificador dio
        # 30 de 30. En pantalla: texto a 16px sin estilo en una lamina vacia).
        casos.append(("caza: CSS que no llego a entrar (clase sin ninguna regla)",
                      guarda("css_huerfano.html",
                             bueno.replace('<div class="par"',
                                           '<div class="par sk-lista"', 1)), 1, "regla CSS"))

        ok = 0
        print(f"  placeholders sin rellenar en el deck bueno: {len(sobran)}")
        for etiqueta, ruta, esperado, debe_decir in casos:
            rc, salida = corre(ruta)
            bien = (rc == esperado) and (debe_decir is None or debe_decir.lower() in salida.lower())
            print(f"  {'OK  ' if bien else 'MAL '} {etiqueta}  (salida {rc}, esperada {esperado})")
            ok += bien

        # Coherencia entre lo que dice la documentacion y lo que hace el motor.
        # No usa un deck: compara los dos archivos directamente.
        coh = coherencia_docs_motor()
        for etiqueta, bien, porque, limite in coh:
            print(f"  {'OK  ' if bien else 'MAL '} {etiqueta}"
                  + (f"  [no cubre: {limite}]" if bien else f"  -> {porque}"))
            ok += bien

        total = len(casos) + len(coh)
        print(f"\n  {ok} de {total} pruebas pasan")
        # Un verde liso miente por omision (ley de golden360, 2026-09-05): el
        # remate declara lo que la bateria NO cubre, o "15 de 15" se lee como
        # "el verificador esta bien" y solo dice "estos 15 casos salen".
        print("  LO QUE ESTA BATERIA NO CUBRE:")
        print("    · que el deck se VEA bien: mide salidas del verificador, no pixeles")
        print("    · que las atmosferas pinten y se muevan: pide navegador real")
        print("      (con Playwright, no el panel integrado, que congela lo oculto),")
        print("      y leer un canvas WebGL con drawImage lo da por muerto: readPixels")
        print("      dentro de requestAnimationFrame")
        print("    · los 60fps del viaje de camara y el render en sala")
        print("    · que los datos y las citas del deck sean CIERTOS")
        print("    · fallos del verificador en comprobaciones sin caso malo aqui:")
        print("      lo probado son estos casos, no todo el script")
        return 0 if ok == total and not sobran else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
