#!/usr/bin/env python3
"""
GUARDIA DE PRIVACIDAD DE LA SKILL · golden-chatea-auditoria · CONTROL I1b

Ley de FER, 2026-09-05, en su voz: "en esta skill no puede haber informacion de ningun VIP,
ningun miembro ni mio... aqui no deberian haber informacion de alumnos ni de nada que corrio.
Eso es en cada chat."

Esta skill guarda el ESTANDAR: como se instala cada asistente y como se ve una auditoria
completa. Lo que paso en un espacio concreto —quien es el dueno, que ns tiene, que tienda,
que producto— vive en el chat de ese cliente y en el Centro de Mando, no aqui.

Por que hace falta un script y no basta la regla: una regla sin instrumento es decoracion, y
esta casa ya lo midio. El dato de cliente no entra de golpe: entra como ejemplo ("medido contra
el espacio de tal cliente"), que es exactamente como se justifica lo que no deberia estar.

Uso:
    python3 sin_datos_de_cliente.py            # revisa la skill entera
    python3 sin_datos_de_cliente.py --autoprueba   # se prueba a si mismo contra un caso malo

Lo que SI puede cazar el codigo (mecanico):
    identificadores de espacio, dominios de tienda, correos, telefonos y credenciales.
Lo que NO puede cazar y queda para lectura humana (H):
    NOMBRES de personas, marcas o negocios. Un nombre propio no tiene forma reconocible; el
    unico filtro es leer. Se declara aqui para que nadie confunda "el script paso" con
    "no hay datos de nadie".
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# `autoprueba.py` FABRICA un espacio roto de la nada: sus dominios y llaves son inventados y
# tienen que parecer reales para que el detector se ejercite. Es la unica excepcion, es de UN
# archivo, y esta es su razon. Cualquier otra excepcion que aparezca aqui sin razon escrita es
# la alfombra que esta casa ya aprendio a reconocer.
EXCEPCIONES = {"scripts/autoprueba.py": ("dominios y llaves FABRICADOS para el banco de "
                                         "pruebas: no salen de ningun espacio real")}

PATRONES = [
    ("identificador de espacio", re.compile(r"\bf\d{6,7}\b")),
    ("dominio de tienda", re.compile(r"\b[a-z0-9][a-z0-9-]*\.myshopify\.com\b")),
    ("correo", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("telefono", re.compile(r"(?<![\d.])\+?(?:57|52|56|507|1)[\s-]?3?\d{9,10}\b")),
    ("credencial", re.compile(r"\b(?:sk-(?:proj-)?[A-Za-z0-9_\-]{20,}"
                              r"|shpat_[A-Za-z0-9]{16,}"
                              r"|eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,})")),
]


def revisar(raiz=RAIZ):
    """Devuelve [(archivo_relativo, linea, que, texto)] de todo lo que no deberia estar."""
    hallazgos = []
    for ruta in sorted(raiz.rglob("*")):
        if not ruta.is_file() or "__pycache__" in ruta.parts or ruta.name == ".DS_Store":
            continue
        rel = str(ruta.relative_to(raiz))
        if rel in EXCEPCIONES:
            continue
        try:
            texto = ruta.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            for que, rx in PATRONES:
                m = rx.search(linea)
                if m:
                    hallazgos.append((rel, n, que, m.group(0)))
    return hallazgos


def autoprueba():
    """Un guardia que nunca ha visto un caso malo no es un guardia."""
    import tempfile
    # Los casos se ARMAN aqui, no se escriben literales: un guardia cuyo propio archivo
    # lleva datos con forma real no se puede revisar a si mismo, y exceptuarlo seria abrir
    # justo la puerta que este script existe para cerrar.
    casos = {
        "identificador de espacio": "medido contra el espacio " + "f" + "9" * 6,
        "dominio de tienda": "apunta a " + "tienda-de-prueba" + ".myshopify" + ".com",
        "correo": "el dueno es " + "nadie@ejemplo" + ".invalid",
        "credencial": "token sk-proj-" + "A" * 30,
    }
    fallos = []
    for que, linea in casos.items():
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "references").mkdir()
            (Path(d) / "references" / "x.md").write_text(linea + "\n")
            vistos = {h[2] for h in revisar(Path(d))}
            marca = "OK   " if que in vistos else "FALLA"
            print(f"  {marca} caza {que}")
            if que not in vistos:
                fallos.append(que)
    # y el control negativo: un texto sano NO puede disparar
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "references").mkdir()
        (Path(d) / "references" / "x.md").write_text(
            "Se mide el escapado del campo antes de escribir, bajo 19.000.\n")
        if revisar(Path(d)):
            print("  FALLA falso positivo sobre texto sano")
            fallos.append("falso positivo")
        else:
            print("  OK    no dispara sobre texto sano")
    return 1 if fallos else 0


def main():
    if "--autoprueba" in sys.argv:
        print("AUTOPRUEBA del guardia de privacidad\n")
        codigo = autoprueba()
        print("\n" + ("El guardia esta roto." if codigo else "El guardia muerde."))
        return codigo
    hallazgos = revisar()
    print(f"GUARDIA DE PRIVACIDAD · {RAIZ.name}")
    for rel, razon in EXCEPCIONES.items():
        print(f"  excepcion declarada: {rel} — {razon}")
    if not hallazgos:
        print("\n  0 datos de espacio, tienda, correo, telefono o credencial en la skill.")
        print("  NO VERIFICADO por codigo: los NOMBRES de personas, marcas o negocios. "
              "Eso se lee.")
        return 0
    print(f"\n  {len(hallazgos)} DATOS QUE NO DEBERIAN ESTAR EN LA SKILL:")
    for rel, n, que, txt in hallazgos:
        print(f"    {rel}:{n}  {que}: {txt}")
    print("\n  El estandar se queda; lo que paso en un espacio concreto va al chat de ese "
          "cliente y al Centro de Mando.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
