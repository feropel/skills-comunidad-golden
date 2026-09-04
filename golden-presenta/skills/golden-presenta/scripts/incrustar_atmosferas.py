#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
incrustar_atmosferas.py - Mete assets/atmosferas.js dentro de un deck HTML.

El deck tiene que ser UN SOLO ARCHIVO (esa es la ley de la skill: sin peticiones
de red). Pero mantener el mismo codigo copiado en dos sitios es como se desincronizan
las cosas. Este script resuelve las dos: `atmosferas.js` es la unica fuente de verdad
y aqui se inyecta entre marcadores.

Uso:
    python3 incrustar_atmosferas.py                 # actualiza assets/deck-base.html
    python3 incrustar_atmosferas.py /ruta/deck.html # actualiza otro deck

Es idempotente: correrlo dos veces deja el mismo resultado.
"""

import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
FUENTE = os.path.join(SKILL, 'assets', 'atmosferas.js')
DESTINO_POR_DEFECTO = os.path.join(SKILL, 'assets', 'deck-base.html')

INICIO = '<!-- ATMOSFERAS:INICIO (generado por scripts/incrustar_atmosferas.py) -->'
FIN = '<!-- ATMOSFERAS:FIN -->'


def main():
    destino = sys.argv[1] if len(sys.argv) > 1 else DESTINO_POR_DEFECTO

    if not os.path.isfile(FUENTE):
        print('No encuentro la fuente: %s' % FUENTE)
        return 2
    if not os.path.isfile(destino):
        print('No encuentro el deck: %s' % destino)
        return 2

    js = io.open(FUENTE, encoding='utf-8').read()
    if '</script' in js:
        print('La fuente contiene "</script": eso romperia el HTML. Abortado.')
        return 1

    html = io.open(destino, encoding='utf-8').read()
    bloque = INICIO + '\n<script>\n' + js + '\n</script>\n' + FIN

    if INICIO in html and FIN in html:
        patron = re.compile(re.escape(INICIO) + '.*?' + re.escape(FIN), re.S)
        html_nuevo = patron.sub(lambda m: bloque, html)
        # Decir "actualizado" cuando el archivo queda identico byte a byte es una
        # confirmacion falsa: manda a buscar el fallo donde no esta. Reportado por
        # el chat del Cartel el 2026-09-03 mientras diagnosticaba un fondo que no
        # se veia (y cuya causa era otra).
        accion = 'actualizado' if html_nuevo != html else 'ya estaba al dia, sin cambios'
    else:
        # Primera vez: se ancla justo antes del script del motor, para que
        # window.Atmosfera exista cuando el motor arranque.
        ancla = '<script>\n/* ============================================================'
        if ancla not in html:
            print('No encuentro donde anclar el bloque en %s' % destino)
            return 1
        html_nuevo = html.replace(ancla, bloque + '\n\n' + ancla, 1)
        accion = 'insertado'

    if html_nuevo == html:
        print('Bloque de atmosferas %s en %s (%d KB de JS). No se reescribio el archivo.'
              % (accion, os.path.basename(destino), len(js) / 1024))
        return 0

    io.open(destino, 'w', encoding='utf-8').write(html_nuevo)
    print('Bloque de atmosferas %s en %s (%d KB de JS)'
          % (accion, os.path.basename(destino), len(js) / 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main())
