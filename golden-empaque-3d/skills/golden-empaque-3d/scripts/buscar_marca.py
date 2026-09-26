#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca rastros de una marca en un arbol de ficheros, SIN que el acento la esconda.

    python3 buscar_marca.py <carpeta> "Le'côterra" [otra marca...]

POR QUE EXISTE (medido el 22-sep-2026)
Se declaro "CERO rastros de Le'coterra en los 7 ficheros" con este comando:

    grep -ric -E "coterra|bergamot|vanilla|athletix" . | grep -v ":0$"

Y quedaba una mencion. El grep funciono perfecto: el patron estaba mal. La marca se
escribe **Le'côterra**, con o circunfleja (U+00F4), asi que la cadena "coterra" NO es
subcadena de "côterra" -- entre la c y la t no hay una o, hay una o-con-acento. El
patron sin acento nunca pudo encontrarla, y el cero era real para ese patron y falso
para la pregunta.

La leccion no es "grep falla con acentos". Es que **buscar una marca escribiendola sin
su acento es buscar otra palabra**, y el resultado vacio se lee como limpio.

COMO LO RESUELVE
Normaliza texto y patron a ASCII plegado (NFD, se tiran los diacriticos) y ademas ignora
apostrofos y espacios. Asi "Le'côterra", "Lecoterra", "LE COTERRA" y "le'coterra" caen
todas en la misma llave. Tambien imprime SIEMPRE el universo revisado, ficheros con cero
incluidos, para que un cero no se pueda confundir con un fichero que no se miro.
"""
import io
import os
import sys
import unicodedata

SALTAR = {".git", "node_modules", "__pycache__", ".DS_Store"}


def plegar(t):
    """minusculas, sin diacriticos, sin apostrofos ni espacios."""
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for basura in ("'", "’", "`", " ", " ", "-", "_"):
        t = t.replace(basura, "")
    return t


def main():
    if len(sys.argv) < 3:
        print('uso: python3 buscar_marca.py <carpeta> "Marca" ["Otra"...]')
        return 2
    raiz = sys.argv[1]
    marcas = [(m, plegar(m)) for m in sys.argv[2:]]

    ficheros = []
    for base, dirs, nombres in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in SALTAR]
        for n in nombres:
            if n in SALTAR:
                continue
            ficheros.append(os.path.join(base, n))
    ficheros.sort()

    print("UNIVERSO: %d ficheros bajo %s" % (len(ficheros), raiz))
    print("MARCAS BUSCADAS (plegadas): %s" % ", ".join("%s -> %s" % m for m in marcas))
    print("-" * 66)

    total = 0
    ilegibles = []
    for ruta in ficheros:
        try:
            with io.open(ruta, "r", encoding="utf-8") as fh:
                bruto = fh.read()
        except (UnicodeDecodeError, OSError):
            ilegibles.append(ruta)
            print("  ??  %s  (no es texto utf-8, NO revisado)" % os.path.relpath(ruta, raiz))
            continue
        plegado = plegar(bruto)
        hits = [(orig, plegado.count(pl)) for orig, pl in marcas if plegado.count(pl)]
        rel = os.path.relpath(ruta, raiz)
        if hits:
            n = sum(c for _, c in hits)
            total += n
            print("  %2d  %s  ->  %s" % (n, rel, ", ".join("%s x%d" % h for h in hits)))
            # mostrar la linea exacta, en el texto original
            for num, linea in enumerate(bruto.splitlines(), 1):
                if any(pl in plegar(linea) for _, pl in marcas):
                    print("        linea %d: %s" % (num, linea.strip()[:110]))
        else:
            print("   0  %s" % rel)

    print("-" * 66)
    print("TOTAL: %d menciones en %d ficheros revisados" % (total, len(ficheros) - len(ilegibles)))
    if ilegibles:
        print("NO REVISADOS (%d): %s" % (len(ilegibles), ", ".join(os.path.basename(f) for f in ilegibles)))
        print("Este total NO cubre esos ficheros. Declararlo, no ocultarlo.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
