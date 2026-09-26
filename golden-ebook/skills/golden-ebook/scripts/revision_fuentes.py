#!/usr/bin/env python3
"""revision_fuentes.py · golden-ebook

Prepara la hoja del Paso 5b: la lista de TODAS las frases que el lector ve (menos títulos,
rótulos, firmas y autores de cita), cada una con las fuentes que cita, más la pregunta del
puente entre los capítulos y el cierre. El verificador (C25) no aprueba
el ebook hasta que esa hoja esté completa y corresponda a esta versión exacta del ebook.json.

Por qué existe: ningún detector de palabras ve una frase que dice más que su fuente. En el
primer ebook real, seis frases exageradas pasaron todas las comprobaciones automáticas. Una
instrucción de "léelo contra las fuentes" se puede saltar; una hoja que el verificador exige
completa y atada al JSON, no.

Uso:
    $PY scripts/revision_fuentes.py EBOOK/ebook.json
      → crea o actualiza EBOOK/revision-fuentes.json. Conserva lo ya revisado de las frases que
        no cambiaron; las frases nuevas o modificadas quedan en "PENDIENTE".

Antes, `guardar_fuentes.py` deja el texto de cada fuente en fuentes-texto/<id>.txt. Después,
quien revisa abre revision-fuentes.json y en cada frase escribe:
    "estado": "fiel"            la fuente dice exactamente eso (ni más fuerte ni más amplio), y
      "fuente_usada": "<id>"    el número de la fuente (o "producto" para lo que se dice del
                                producto: se busca en producto.claims_permitidos y modo_uso)
      "cita_fuente": "..."      el pasaje LITERAL que lo sostiene, 20 caracteres o más, copiado
                                del .txt de esa fuente. Si la frase trae un número, la cita también.
    "estado": "sin afirmacion"  la frase no afirma un hecho (saludo, transición, instrucción). No
                                vale para frases con número, [n] o cuantificadores ("casi nadie").
    "excepcion_claim": "..."    solo si el verificador acusa un claim que no lo es (p. ej. "solo un
                                dermatólogo puede tratar la alopecia"): el motivo, 30+ caracteres.
                                Sale como AVISO visible, nunca como aprobación silenciosa.
C25 busca cada cita en el texto guardado: una nota inventada no la encuentra.
Si una frase no es fiel, se corrige el TEXTO en ebook.json y se vuelve a correr este script.
Y en "puente": "estado": "revisado" con la nota de por qué ningún capítulo describe un
problema de salud que el cierre resuelva con el producto.
"""
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from verificar_ebook import frases_a_revisar  # noqa: E402

ESTADOS_VALIDOS = ("fiel", "sin afirmacion")


def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print(__doc__)
        sys.exit(2)
    ruta = sys.argv[1]
    crudo = open(ruta, "rb").read()
    e = json.loads(crudo)
    destino = os.path.join(os.path.dirname(os.path.abspath(ruta)), "revision-fuentes.json")
    previa = {}
    puente = {"estado": "PENDIENTE", "nota": ""}
    if os.path.exists(destino):
        viejo = json.load(open(destino, encoding="utf-8"))
        previa = {f["frase"]: f for f in viejo.get("frases", [])}
        if viejo.get("puente", {}).get("estado") == "revisado":
            puente = viejo["puente"]
            puente["estado"] = "PENDIENTE"  # el texto cambió: el puente se vuelve a leer
            puente["nota_anterior"] = puente.pop("nota", "")
            puente["nota"] = ""
    lista, conservadas = [], 0
    for i, (ruta_campo, frase, refs) in enumerate(frases_a_revisar(e), 1):
        antes = previa.get(frase)
        if antes and antes.get("estado") in ESTADOS_VALIDOS:
            conservadas += 1
            lista.append({**antes, "id": i, "ruta": ruta_campo, "fuentes": refs})
        else:
            lista.append({"id": i, "ruta": ruta_campo, "frase": frase, "fuentes": refs,
                          "estado": "PENDIENTE", "fuente_usada": refs[0] if len(refs) == 1 else "",
                          "cita_fuente": ""})
    hoja = {"ebook_sha256": hashlib.sha256(crudo).hexdigest(),
            "instrucciones": "estado: fiel (con fuente_usada y cita_fuente literal de fuentes-texto/<id>.txt) "
                             "| sin afirmacion (no vale con números ni cuantificadores); "
                             "excepcion_claim solo con motivo; puente.estado: revisado.",
            "puente": puente, "frases": lista}
    json.dump(hoja, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    pend = sum(1 for f in lista if f["estado"] == "PENDIENTE")
    print(json.dumps({"hoja": destino, "frases": len(lista), "conservadas": conservadas,
                      "pendientes": pend, "puente": puente["estado"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
