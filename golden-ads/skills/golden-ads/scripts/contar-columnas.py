#!/usr/bin/env python3
"""Cuenta los bloques y las columnas del preset GOLDEN PRO.

POR QUE EXISTE: el numero "40 columnas / 5 bloques" se citaba a mano en varios
archivos y caduca solo cada vez que alguien toca la lista. Este script es LA
FUENTE: se corre, y lo que diga manda sobre cualquier cifra escrita en prosa.

POR QUE LEE ENTRE MARCAS Y NO POR FORMATO: la primera version contaba cualquier
linea con formato **Etiqueta:** y por eso se contaba a si misma cuando se le
escribia una nota al lado (devolvia 6 y 42 sin que cambiara un dato). Un detector
hecho de patrones acusa al IDIOMA, no al defecto. Por eso la lista va encerrada
entre <!-- COLUMNAS:INICIO --> y <!-- COLUMNAS:FIN -->: lo de fuera no se cuenta,
se escriba como se escriba.

AUTOPRUEBA EN LOS DOS SENTIDOS (obligatoria, `--test`): debe MORDER el caso malo
(una columna sembrada sube el conteo) y CALLAR ante el bueno (prosa nueva, y
tambien prosa disfrazada con el mismo formato de los bloques, no lo mueven).
Probar solo el lado malo es lo que deja pasar un instrumento roto: muerde, y por
eso parece bueno.

Uso:  python3 contar-columnas.py [ruta/19-golden-pro-preset.md] [--test]
"""
import re, sys, pathlib

INICIO = "<!-- COLUMNAS:INICIO -->"
FIN    = "<!-- COLUMNAS:FIN -->"

def contar(texto):
    if INICIO not in texto or FIN not in texto:
        raise SystemExit("FALLO: no encuentro las marcas COLUMNAS:INICIO/FIN. "
                         "Sin region delimitada no se cuenta: se reporta.")
    region = texto.split(INICIO, 1)[1].split(FIN, 1)[0]
    bloques = [b for b in re.split(r'\n(?=\*\*)', region.strip()) if ':**' in b]
    total = 0
    for b in bloques:
        cuerpo = ' '.join(b.split()).split(':**', 1)[1]
        items = [x.strip() for x in cuerpo.split('·') if x.strip()]
        total += len(items)                                   # una columna por nombre
        total += sum(x.count('(+costo)') for x in items)      # "(+costo)" = columna extra
        total += 1 if '**Ident:**' in cuerpo else 0           # el identificador
    return len(bloques), total

def autoprueba(texto):
    base = contar(texto)
    casos = []
    # BUENO 1 · prosa nueva fuera de la region
    casos.append(("BUENO · prosa nueva fuera", texto.replace(FIN, "Nota suelta.\n" + FIN, 1)
                  if False else texto + "\n\nProsa nueva al final del archivo.\n", base))
    # BUENO 2 · prosa DISFRAZADA con el mismo formato de los bloques, fuera de la region
    disfraz = texto.replace(FIN, FIN + "\n**Nota con formato de bloque:** no es columna · ni esto\n", 1)
    casos.append(("BUENO · nota disfrazada fuera", disfraz, base))
    # MALO · columna sembrada DENTRO de la region
    reg = texto.split(INICIO,1)[1].split(FIN,1)[0]
    malo = texto.replace(reg, reg.replace("· ROAS de compras", "· ROAS de compras · SEMBRADA", 1), 1)
    casos.append(("MALO · columna sembrada", malo, (base[0], base[1] + 1)))
    ok = True
    print(f"referencia -> bloques={base[0]} columnas={base[1]}")
    for nombre, t, esperado in casos:
        got = contar(t)
        bien = got == esperado
        ok = ok and bien
        print(f"  [{'OK ' if bien else 'FALLA'}] {nombre}: {got}  esperado {esperado}")
    if not ok:
        raise SystemExit("AUTOPRUEBA FALLIDA: el contador no distingue el dato del formato.")
    print("AUTOPRUEBA OK en los dos sentidos (muerde el malo, calla ante el bueno).")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--test"]
    ruta = pathlib.Path(args[0]) if args else \
        pathlib.Path(__file__).resolve().parent.parent / "references" / "19-golden-pro-preset.md"
    texto = ruta.read_text(encoding="utf-8")
    if "--test" in sys.argv:
        autoprueba(texto)
    else:
        b, c = contar(texto)
        print(f"GOLDEN PRO · bloques={b} columnas={c}  (fuente: {ruta.name})")
