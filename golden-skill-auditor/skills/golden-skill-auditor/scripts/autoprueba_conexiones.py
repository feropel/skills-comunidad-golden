#!/usr/bin/env python3
"""Banco de `revisar_conexiones()` — la clase "lista blanca que calla".

POR QUE EXISTE (medido 2026-09-05, barrido de listas de excepcion del arsenal):
El detector de citas muertas traia una lista de excusas en PROSA —
("si el equipo", "si lo tiene", "opcional", "atajo", "si existe")— que apagaba el
aviso cuando alguna aparecia en una ventana de +-120 caracteres alrededor de la cita.
Nacio para no avisar de herramientas de terceros mencionadas condicionalmente
("usa `ripgrep` si lo tiene en el PATH"). Legitimo. Pero traia DOS defectos medidos:

  1. CONTAGIO POR PROXIMIDAD. La ventana no respeta frases: una excusa escrita para
     una cosa silencia CUALQUIER cita que caiga a menos de 120 caracteres. Medido: la
     palabra "atajo" de una frase anterior, sin relacion, silencio una cita limpia.
  2. LA EXCUSA NO APLICA AL ARSENAL PROPIO. Una skill `golden-*` existe o no existe en
     ~/.claude/skills. "Opcional" describe si se USA, no si EXISTE: una skill Golden
     citada y ausente es una cita muerta aunque la frase diga "opcional".

Ademas la ventana se calculaba con `prosa.find(c)` — la PRIMERA aparicion del token en
todo el documento, no la que se esta juzgando. Con el token repetido, se miraba el
contexto equivocado.

LA CLASE: una excusa vale para LO QUE LA FRASE DICE, no para todo lo que le queda
cerca; y una lista de excusas nunca puede eximir al universo que la skill SI controla.

Uso:  python3 scripts/autoprueba_conexiones.py     (0 = pasa, 1 = falla)
"""
import importlib.util
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "conexiones", os.path.join(AQUI, "conexiones.py"))
cx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cx)

FANTASMA = "golden-tercera-fantasma"   # no existe en ~/.claude/skills
OTRA = "golden-inexistente-total"

# (nombre, cuerpo del SKILL.md, avisos_esperados)
CASOS = [
    ("CONTROL · cita desnuda a skill golden inexistente",
     f"Encadena con `{FANTASMA}` al terminar.", 1),

    ("Arsenal propio marcado 'opcional' — la excusa NO aplica",
     f"Usa `{OTRA}` de forma opcional.", 1),

    ("Arsenal propio marcado 'si existe' — la excusa NO aplica",
     f"Llama a `{FANTASMA}` si existe en el equipo.", 1),

    ("CONTAGIO · 'atajo' en OTRA frase no puede silenciar esta cita",
     "Corre el script como atajo rapido cuando tengas prisa.\n\n"
     f"Y esta cita `{FANTASMA}` no lleva excusa ninguna.", 1),

    ("CONTAGIO · 'opcional' en la frase ANTERIOR",
     "El segundo paso es opcional segun el caso.\n\n"
     f"Despues corre `{FANTASMA}` siempre.", 1),

    # --- ruido legitimo: herramienta de TERCEROS, condicional, en su propia frase ---
    ("Terceros condicional en su frase — sigue callado",
     "Usa `ripgrep` si lo tiene en el PATH.", 0),

    ("Terceros condicional 'si el equipo' — sigue callado",
     "Corre `fdfind` si el equipo lo trae instalado.", 0),

    ("Skill golden que SI existe — jamas avisa",
     "Encadena con `golden-blindaje` al cerrar.", 0),

    # --- medidos en el arsenal real al instalar el control (2026-09-05) ---
    # No son citas: son SINTAXIS (variable CSS) o el autor DECLARANDO que no existe.
    # La linea que separa esto de la alfombra: se exime una declaracion de
    # INEXISTENCIA ("planeado, no construido"), jamas una de OPCIONALIDAD
    # ("opcional", "si lo tiene") — la primera ya reporta el hallazgo, la segunda lo tapa.
    ("Variable CSS --golden-gold no es una cita de skill",
     "Paleta: `--golden-gold` #e8b84b y `--golden-gold-light` #f7e3a1.", 0),

    # F6 (verificador adversarial): `DECLARA_INEXISTENCIA` era ella misma una alfombra.
    # Bastaba una palabra, sin ninguna comprobacion: `any(w in frase)`. Y el caso
    # peligroso es el que dice que la skill SI se usa. Se ELIMINO la lista entera: la
    # existencia de una skill se comprueba con os.path.exists, no leyendo un adjetivo.
    # Estos avisos son VERDADEROS — la skill citada no existe — y son 3 en 189 skills.
    ("F6 · 'planeado' ya no tapa nada",
     f"Mientras no exista `{FANTASMA}` (PLANEADO, no construido todavia), "
     "la lista se arma a mano.", 1),

    ("F6 · 'aun no' con la skill declarada EN USO — el caso peligroso",
     f"La skill `{FANTASMA}` aun no la usamos, pero es la que corre el cierre.", 1),

    ("F6 · 'nombre de trabajo' ya no tapa nada",
     f"Se guarda un preset (nombre de trabajo `{OTRA}`) con la paleta.", 1),

    # F7 · el contagio que el arreglo anterior decia haber matado seguia vivo: una lista
    # de vinetas sin puntuacion final es UNA sola frase para el cortador.
    ("F7 · lista de vinetas: 3 citas muertas, 3 avisos",
     f"- `{FANTASMA}` corre primero\n"
     f"- `{OTRA}` corre despues\n"
     "- `golden-muerta-real` todavia no existe", 3),

    ("F7 · tres citas en UNA frase, una con excusa",
     f"Encadena `{FANTASMA}`, `{OTRA}` y `golden-muerta-real` (el ultimo esta planeado).", 3),

    # F8 · la puerta CSS miraba el DOCUMENTO entero: bastaba declarar la variable en
    # cualquier otro punto para tapar una cita real. Ahora se exige que TODAS las
    # apariciones del token vayan precedidas de `--`.
    ("F8 · cita real + la misma palabra como variable CSS en otro punto",
     f"Cita real: encadena con `{FANTASMA}` al cerrar.\n\n"
     f"Paleta CSS: `--{FANTASMA}: #fff;`", 1),

    ("F8 · variable CSS de verdad (todas las apariciones llevan --)",
     "Paleta: `--golden-gold` #e8b84b y `--golden-gold-light` #f7e3a1.", 0),

    # F9 · el banco no ejercitaba `_frase_excusa`, y al ir a cubrirla se vio POR QUE:
    # `RX_NOMBRE` solo captura tokens que empiezan por `golden` o `fer`, asi que el
    # detector NUNCA pudo ver una herramienta de terceros. La justificacion escrita de
    # `EXCUSAS_CONDICIONALES` ("usa `ripgrep` si lo tiene en el PATH") no correspondia a
    # nada detectable: era decoracion que aparentaba cubrir un caso inexistente. Se
    # borro la lista entera. Lo unico que esa rama alcanzaba de verdad son los tokens
    # `fer*`, y para esos vale la misma regla que para el arsenal: existe o no existe.
    ("F9 · token fer* inexistente — avisa",
     "Encadena con `fer-modulo-fantasma` al terminar.", 1),

    ("F9 · token fer* con excusa en su propia frase — ya no la tapa",
     "Corre `fer-modulo-fantasma` si lo tiene en el equipo.", 1),

    ("F9 · token fer* en lista de vinetas con excusa en otro item",
     "- `fer-modulo-fantasma` corre primero\n"
     "- el segundo paso es opcional", 1),
]


def correr(cuerpo, univ, tmp):
    d = os.path.join(tmp, "golden-falsa")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("---\nname: golden-falsa\ndescription: banco\n---\n# Banco\n\n"
                 + cuerpo + "\n")
    return cx.revisar_conexiones(d, univ)


def main():
    univ = cx.universo(os.path.expanduser("~/.claude/skills"))
    tmp = tempfile.mkdtemp(prefix="autoprueba_conexiones_")
    fallos = []
    try:
        for nombre, cuerpo, esperados in CASOS:
            _f, avisos = correr(cuerpo, univ, tmp)
            if len(avisos) != esperados:
                que = ("SILENCIA una cita muerta" if len(avisos) < esperados
                       else "AVISA de mas")
                fallos.append(f"  [FALLA] {nombre}: {que} "
                              f"(esperados {esperados}, obtenidos {len(avisos)})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("=" * 70)
    print(" AUTOPRUEBA · revisar_conexiones() de conexiones.py")
    print("=" * 70)
    print(f" Casos: {len(CASOS)}   pasan: {len(CASOS) - len(fallos)}   fallan: {len(fallos)}")
    if fallos:
        print("\n".join(fallos))
        print("\n Las excusas en prosa se estan aplicando por PROXIMIDAD y sobre el")
        print(" arsenal propio. Ver el encabezado de este archivo.")
        return 1
    print(" La excusa alcanza solo a su propia frase, y nunca al arsenal golden-*.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
