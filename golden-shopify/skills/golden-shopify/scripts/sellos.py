#!/usr/bin/env python3
"""
GOLDEN SHOPIFY · sellos.py
Comprueba que las CUATRO CARAS de la version dicen lo mismo.

POR QUE EXISTE (medido 2026-09-02, dos veces el mismo dia)
  La version de esta skill vive en cuatro sitios y tres estan dentro de la skill:
    1. el sello bajo el H1 de SKILL.md
    2. la primera entrada de references/changelog.md
    3. GFS_VERSION en assets/config-center.liquid  ← OTRO EJE, no tiene que coincidir
    4. la fila de STACK-GOLDEN/REGISTRO-FABRICAS.md ← VIVE FUERA DE LA SKILL
  La cuarta es la que leen los OTROS chats para saber en que va esta skill, y es justo la
  que el ritual de blindaje no toca: al quedar fuera del arbol, un bump la deja atras sin
  que nada avise. Se desfaso 4 versiones (registro G4.7 vs disco G4.11b), lo corrigio el
  Centro de Mando, y **volvio a desfasarse en minutos** con el siguiente bump. No es
  descuido: es estructural. Por eso ahora hay un script que lo mide.

  LA CUARTA CARA TIENE UN SOLO ESCRITOR: el Centro de Mando (zanjado 2026-09-02). Antes
  escribian dos —esta fabrica y el CdM— y un dia escribimos casi a la vez: se salvo solo
  por el orden de llegada, porque si la escritura vieja aterriza de ultima el registro
  RETROCEDE y el desfase vuelve en silencio. Un escritor unico elimina la carrera de raiz,
  que es mejor que un acuerdo de tener cuidado entre dos. **La fabrica sella y reporta; el
  CdM escribe la fila.** No editar el registro desde aqui.

  CONSECUENCIA: entre que la fabrica sella y el CdM regenera hay una VENTANA DE DESFASE
  LEGITIMA. Por eso el desfase del registro es AVISO, no fallo: hacerlo bloquear seria el
  detector agresivo que la Regla 0-H persigue — un aviso que salta durante una ventana
  normal entrena a ignorar la salida entera. Sello y changelog SI bloquean: viven dentro
  del arbol, los toca el mismo ritual y no tienen segundo escritor, asi que ahi un desfase
  nunca es legitimo.

  OJO CON EL SEGUNDO EJE: GFS_VERSION es lo que se estampa en la PAGINA GENERADA y solo
  sube cuando cambia lo que la pagina produce. Que difiera del sello NO es un fallo — seria
  un fallo tratarlo como tal y "sincronizarlo" a ciegas. Este script NO lo mira, y su
  autoprueba tiene un caso que lo garantiza.

  MODO DE FALLO QUE VIGILA SU AUTOPRUEBA: si un regex deja de casar y el codigo tratara
  "no encontre version" como "coinciden", saldria 0 SIEMPRE y nadie se enteraria — el verde
  eterno. Por eso `revisar()` distingue None de "distinto", y hay casos que lo prueban.

USO    python3 sellos.py            SALIDA  0 = coinciden · 1 = hay desfase
"""
import os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(AQUI, ".."))
# El registro vive en el arbol de PROYECTOS, fuera de la skill. Se busca por nombre para no
# clavar una ruta con emojis que cambia de maquina.
CANDIDATOS = [
    os.path.expanduser("~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/🌐 PROYECTOS/STACK-GOLDEN/REGISTRO-FABRICAS.md"),
]
RX = r'(G\d+\.\d+[a-z]?)'


def sello_skill(skill_dir=None):
    p = os.path.join(skill_dir or SKILL, "SKILL.md")
    if not os.path.exists(p):
        return None
    m = re.search(r'skill ' + RX, open(p, encoding="utf-8").read())
    return m.group(1) if m else None


def sello_changelog(skill_dir=None):
    p = os.path.join(skill_dir or SKILL, "references", "changelog.md")
    if not os.path.exists(p):
        return None
    m = re.search(r'^## ' + RX, open(p, encoding="utf-8").read(), re.M)
    return m.group(1) if m else None


def sello_registro(registro=None):
    """Devuelve (version, ruta). version None = no se pudo leer (NO es 'coincide')."""
    rutas = [registro] if registro else CANDIDATOS
    for p in rutas:
        if p and os.path.exists(p):
            for linea in open(p, encoding="utf-8"):
                if "golden-shopify" in linea:
                    m = re.search(RX, linea)
                    return (m.group(1) if m else None), p
            return None, p          # el archivo existe pero no tiene la fila
    return None, (rutas[0] if rutas else None)


def revisar(skill_dir=None, registro=None):
    """Devuelve (caras, fallos, avisos).

    fallos  = BLOQUEANTES: solo lo que vive dentro del arbol (sello y changelog), donde un
              desfase nunca es legitimo porque los toca el mismo ritual.
    avisos  = INFORMATIVOS: el registro, que tiene otro escritor (el CdM) y por tanto una
              ventana de desfase normal. Se imprime siempre, no rompe la corrida.

    Separado de main() a proposito: asi la autoprueba puede llamarlo con archivos
    temporales y NUNCA tocar el registro real (un validador que para probarse tiene
    que escribir en produccion no es un validador, es un riesgo)."""
    s, c = sello_skill(skill_dir), sello_changelog(skill_dir)
    r, ruta = sello_registro(registro)
    caras = {"skill": s, "changelog": c, "registro": r, "ruta_registro": ruta}
    fallos, avisos = [], []
    # None NUNCA se trata como "coincide": es justo el modo de fallo silencioso a evitar.
    if s is None:
        fallos.append("no se pudo leer el sello de SKILL.md → revisar A MANO (ausencia no es prueba)")
    if c is None:
        fallos.append("no se pudo leer la version del changelog → revisar A MANO")
    if s and c and s != c:
        fallos.append(f"sello ({s}) != changelog ({c}) → el bump toco una cara y no la otra")
    # ── el registro NO bloquea: otro escritor, ventana legitima. Pero se dice siempre.
    if r is None:
        avisos.append(f"no se pudo leer la fila de golden-shopify en el registro ({ruta}) → "
                      "revisar A MANO: NO se da por bueno solo porque no se encuentre")
    elif s and r != s:
        avisos.append(f"registro ({r}) != sello ({s}) → normal si acabas de sellar y el CdM aun no "
                      "regenera; si persiste, reportaselo. NO lo edites desde aqui: escribe el CdM")
    return caras, fallos, avisos


def main():
    caras, fallos, avisos = revisar()
    print(f"1. sello SKILL.md ......... {caras['skill']}")
    print(f"2. changelog .............. {caras['changelog']}")
    print(f"3. registro de fabricas ... {caras['registro'] or '(no encontrado)'}")
    if avisos:
        print("\nℹ️ AVISO (no bloquea — el registro lo escribe el CdM):\n- " + "\n- ".join(avisos))
    if fallos:
        print("\n⚠️ DESFASE DENTRO DE LA SKILL:\n- " + "\n- ".join(fallos))
        sys.exit(1)
    print(f"\n✅ sello y changelog coinciden en {caras['skill']}"
          + ("" if avisos else f" · registro al dia"))
    print("   (GFS_VERSION es el OTRO eje: solo sube si cambia lo que la pagina produce)")
    sys.exit(0)


if __name__ == "__main__":
    main()
