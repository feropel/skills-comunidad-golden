#!/usr/bin/env python3
"""
autoprueba_arsenal.py — prueba a validar_arsenal.py contra casos que SE SABE
que son malos y contra casos que SE SABE que son buenos.

Ley de la casa (2026-09-02): un validador sin autoprueba es una opinion con
sintaxis. Y se prueba en las DOS direcciones: que cace lo malo Y que deje
pasar lo bueno. Un check agresivo hace tanto daño como uno ciego, y cuesta
mas descubrirlo.

Cada caso malo viene de un fallo REAL ya pagado por la casa.
"""
import os, re, sys, tempfile, shutil, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
VALIDADOR = os.path.join(AQUI, "validar_arsenal.py")

BUENA = ("Golden Group — hace una cosa concreta y util para la empresa. Usala cuando el usuario "
         "diga \"haz esto\", \"arma lo otro\" o pida el informe. Acentos correctos: operacion, "
         "logistica, produccion, analisis.")


def skill(tmp, nombre, desc, name=None, extra_fm="", cuerpo="cuerpo\n"):
    d = os.path.join(tmp, nombre)
    os.makedirs(d, exist_ok=True)
    fm = f"name: {name or nombre}\ndescription: >-\n  " + desc.replace("\n", " ") + "\n" + extra_fm
    open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(f"---\n{fm}---\n\n{cuerpo}")
    return d


def corre(d):
    r = subprocess.run([sys.executable, VALIDADOR, d], capture_output=True, text=True)
    return r.returncode, r.stdout


def main():
    tmp = tempfile.mkdtemp(prefix="autoprueba-arsenal-")
    casos = []
    try:
        # ---- MALOS: deben salir 1 ----
        casos.append(("caza: description de 1200 chars",
                      skill(tmp, "larga", "x" * 1200), 1, "1200"))
        casos.append(("caza: name que no coincide con la carpeta",
                      skill(tmp, "carpeta-a", BUENA, name="otro-nombre"), 1, "no coincide"))
        casos.append(("caza: name con mayusculas",
                      skill(tmp, "MalNombre", BUENA, name="MalNombre"), 1, "invalido"))
        casos.append(("caza: name con guiones dobles",
                      skill(tmp, "dos--guiones", BUENA), 1, "invalido"))
        casos.append(("caza: signo de apertura en la description",
                      skill(tmp, "apertura", "¿Quieres esto? " + BUENA), 1, "APERTURA"))
        casos.append(("caza: acentos rotos (mojibake)",
                      skill(tmp, "mojibake", "informaciÃ³n del producto. " + BUENA), 1, "ACENTOS ROTOS"))
        casos.append(("caza: raya separadora en la description",
                      skill(tmp, "raya", "------------ " + BUENA), 1, "RAYA"))
        casos.append(("caza: campo no permitido en el frontmatter",
                      skill(tmp, "campo-raro", BUENA, extra_fm="version: 1.0\n"), 1, "no permitidos"))
        casos.append(("caza: compatibility de 600 chars",
                      skill(tmp, "compat", BUENA, extra_fm="compatibility: " + "y" * 600 + "\n"), 1, "compatibility"))
        casos.append(("caza: sin SKILL.md", os.path.join(tmp, "vacia"), 1, "falta SKILL.md"))
        os.makedirs(os.path.join(tmp, "vacia"), exist_ok=True)

        # ---- BUENOS: deben salir 0 (aqui vive el riesgo del check agresivo) ----
        casos.append(("no dispara: skill legitima y corta",
                      skill(tmp, "sana", BUENA), 0, None))
        casos.append(("no dispara: description de exactamente 1024",
                      skill(tmp, "justa", "a" * 1024), 0, None))
        casos.append(("no dispara: tildes y eñe CORRECTAS",
                      skill(tmp, "tildes", "Configuracion con acentos correctos: nº, año, "
                            "logística, gestión, diseño, análisis. " + BUENA), 0, None))
        casos.append(("no dispara: guion simple en el nombre",
                      skill(tmp, "nombre-con-guion", BUENA), 0, None))
        casos.append(("no dispara: un guion suelto en el texto",
                      skill(tmp, "guion-suelto", "Algo - con guion simple. " + BUENA), 0, None))
        casos.append(("no dispara: 'mi tienda' DENTRO de una cita del cliente",
                      skill(tmp, "cita-tienda", 'Usala cuando diga "monta la respuesta de mi tienda". ' + BUENA), 0, None))
        casos.append(("no dispara: la palabra tienda en sentido ajeno",
                      skill(tmp, "tienda-ajena", "Monta la tienda del cliente. " + BUENA), 0, None))

        # ---- CONEXIONES: malos ----
        d = skill(tmp, "ref-rota", BUENA, cuerpo="Lee `references/no-existe.md` para el detalle.\n")
        casos.append(("caza: referencia a un archivo que no existe", d, 1, "referencia rota"))
        d = skill(tmp, "script-fantasma", BUENA, cuerpo="Corre `scripts/no-esta.py` al cerrar.\n")
        casos.append(("caza: script declarado y ausente", d, 1, "script declarado y ausente"))

        # ---- CONEXIONES: buenos (aqui vive el ruido si el check es tosco) ----
        d = skill(tmp, "ref-calificada-antes", BUENA,
                  cuerpo="La receta vive en `golden-shopify` -> `references/x.md`.\n")
        casos.append(("no dispara: ruta calificada con la skill dueña ANTES", d, 0, None))
        d = skill(tmp, "ref-calificada-despues", BUENA,
                  cuerpo="Usa `scripts/otro.json` de golden-shopify, que lo mantiene.\n")
        casos.append(("no dispara: dueño nombrado DESPUES de la ruta", d, 0, None))
        d = skill(tmp, "ref-en-historia", BUENA,
                  cuerpo="<!-- v1.0: se renombro references/viejo.md a nuevo.md -->\ncuerpo\n")
        casos.append(("no dispara: referencia dentro de un comentario (historia)", d, 0, None))
        d = skill(tmp, "cita-familia", BUENA,
                  cuerpo="Para el bot usa la familia golden-chatea-pro completa.\n")
        casos.append(("no dispara: cita a un PREFIJO de familia", d, 0, None))

        # ---- CONTEXTO QUE NO ES UNA CITA (falsos positivos medidos el 2026-09-03
        # sobre golden-ads, reportados por su propia fabrica) ----
        d = skill(tmp, "cita-binario", BUENA,
                  cuerpo="Transcribe en local con golden-transcribe antes de escribir.\n")
        casos.append(("no dispara: binario de la casa (~/.golden/bin)", d, 0, None))
        d = skill(tmp, "cita-archivo", BUENA,
                  cuerpo="El detalle vive en references/19-golden-pro-preset.md y en PRESET-columnas-golden-09.2025.md.\n")
        casos.append(("no dispara: nombre de ARCHIVO, no cita de skill", d, 0, None))
        d = skill(tmp, "cita-ancla", BUENA,
                  cuerpo="Ver el indice: [G39](#g39--2026-06-25--golden-pro-preset-unico).\n")
        casos.append(("no dispara: ancla de indice de Markdown", d, 0, None))

        # ---- ANGULARES: regla del validador oficial local, medida el 2026-09-03
        # sobre golden-shopify (caia por `product.<tema>.json` con 1010 chars, DENTRO del tope)
        casos.append(("caza: angulares en la description",
                      skill(tmp, "angulares", "Arma el archivo product.<tema>.json. " + BUENA), 1, "ANGULARES"))
        casos.append(("no dispara: el mismo marcador SIN angulares",
                      skill(tmp, "sin-angulares", "Arma el archivo product.tema.json. " + BUENA), 0, None))

        # ---- SKILL ANIDADA: el barrido debe VERLA. Medido 2026-09-03: el patron
        # de un solo nivel se saltaba 20 skills dentro del plugin claude-ads.
        # No fallaban: ni se miraban. El instrumento reportaba MENOS FILAS, no rojo.
        import os as _os
        nido = _os.path.join(tmp, "plugin-x", "skills", "anidada-mala")
        _os.makedirs(nido, exist_ok=True)
        open(_os.path.join(nido, "SKILL.md"), "w", encoding="utf-8").write(
            "---\nname: anidada-mala\ndescription: >-\n  " + ("z" * 1200) + "\n---\n\ncuerpo\n")
        casos.append(("caza: skill ANIDADA con description de 1200 (barrido recursivo)",
                      _os.path.join(tmp, "plugin-x"), 1, "1200"))

        # ---- LA SKILL SE VALIDA A SI MISMA COMO ARTEFACTO PUBLICABLE ----
        # Pregunta de la fabrica de golden-shopify (2026-09-03): "tu validador te
        # valida a TI, o solo a lo que produces?". Punto ciego natural: uno mira
        # hacia afuera. Esta autoprueba probaba el validador contra casos inventados
        # y NUNCA validaba el SKILL.md de su propia skill.
        propia = _os.path.dirname(AQUI)
        casos.append(("no dispara: el AUDITOR se valida a SI MISMO", propia, 0, None))

        ok = 0
        for etiqueta, d, esperado, debe_decir in casos:
            rc, salida = corre(d)
            bien = (rc == esperado) and (debe_decir is None or debe_decir in salida)
            print(f"  {'OK  ' if bien else 'MAL '} {etiqueta}  (salida {rc}, esperada {esperado})")
            if not bien and debe_decir:
                print(f"        esperaba ver: {debe_decir}")
            ok += bien
        print(f"\n  {ok} de {len(casos)} pruebas pasan")
        return 0 if ok == len(casos) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
