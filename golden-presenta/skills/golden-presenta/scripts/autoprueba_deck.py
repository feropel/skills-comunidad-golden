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
import os, re, sys, subprocess, tempfile, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
BASE = os.path.join(SKILL, "assets", "deck-base.html")
VERIF = os.path.join(AQUI, "verificar_deck.py")

VALORES = {
    "GP_ATMOSFERA": "enjambre", "GP_MARCA": "Marca Demo",
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
        print(f"\n  {ok} de {len(casos)} pruebas pasan")
        return 0 if ok == len(casos) and not sobran else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
