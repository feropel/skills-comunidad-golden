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
VALIDADOR = os.environ.get("VALIDAR_ARSENAL_MUTANTE") or os.path.join(AQUI, "validar_arsenal.py")

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
    rutas = d if isinstance(d, list) else [d]
    r = subprocess.run([sys.executable, VALIDADOR, *rutas], capture_output=True, text=True)
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
        # ---- LEY DE LOS REQUISITOS (27-sep): las dos direcciones y la frontera ----
        casos.append(("caza: usa mcp__ y no declara requisitos",
                      skill(tmp, "sin-requisitos", BUENA, cuerpo="# Flujo\nLlama a mcp__shopify__get-order.\n"), 1, "REQUISITOS SIN DECLARAR"))
        casos.append(("caza: llave en .secrets/ con la seccion enterrada al final",
                      skill(tmp, "enterrada", BUENA, cuerpo="# Flujo\nLee .secrets/token.txt\n" + "x\n" * 120 + "## Requisitos\nSi falta, pidela.\n"), 1, "REQUISITOS SIN DECLARAR"))
        casos.append(("no dispara: declara requisitos y dice que hacer si falta",
                      skill(tmp, "con-requisitos", BUENA, cuerpo="## Requisitos\nEl token del espacio. Si falta, para y pidelo: que es, donde se saca, donde se pega.\n\n# Flujo\nLee .secrets/token.txt\n"), 0, None))
        casos.append(("caza: pide el token del workspace EN PROSA (el caso de Chatea)",
                      skill(tmp, "prosa-credencial", BUENA, cuerpo="# Flujo\nEl usuario entrega los datos del negocio y el token del workspace.\n"), 1, "REQUISITOS SIN DECLARAR"))
        _d = skill(tmp, "narrado", BUENA, cuerpo="# Flujo\nEscribe el guion.\n")
        os.makedirs(os.path.join(_d, "references"), exist_ok=True)
        open(os.path.join(_d, "references", "ejemplo.md"), "w").write("En ese estudio, ElevenLabs pone la voz y ffmpeg une los clips.\n")
        open(os.path.join(_d, "references", "changelog.md"), "w").write("v1: antes usaba mcp__viejo y .secrets/x\n")
        casos.append(("no dispara: programa NARRADO en una referencia y dependencias viejas en el changelog", _d, 0, None))
        casos.append(("no dispara: herramientas propias de la app (mcp__ccd_) y un sello de version",
                      skill(tmp, "app-propia", BUENA, cuerpo="<!-- v1: antes usaba mcp__shopify__x -->\n# Flujo\nAvisa con mcp__ccd_session_mgmt__send_message.\n"), 0, None))
        casos.append(("caza: usa la cuenta de Google Calendar del usuario sin declararla",
                      skill(tmp, "calendario", BUENA, cuerpo="# Flujo\nConsulta la disponibilidad real en Google Calendar.\n"), 1, "REQUISITOS SIN DECLARAR"))
        casos.append(("no dispara: Canva o Notion nombrados como referencia de estilo",
                      skill(tmp, "referencia-estilo", BUENA, cuerpo="# Flujo\nUn look limpio, como una plantilla de Canva o una página de Notion.\n"), 0, None))
        casos.append(("no dispara: titulo impersonal QUE NECESITA ESTA SKILL (falso cazado por el auditor, 27-sep)",
                      skill(tmp, "impersonal", BUENA, cuerpo="## 📋 QUÉ NECESITA ESTA SKILL\nEl token de Meta. Si falta, para y pídelo.\n\n# Flujo\nUsa mcp__meta__ads.\n"), 0, None))
        casos.append(("no dispara: credencial NOMBRADA en una historia o prohibición (no se pide)",
                      skill(tmp, "historia-llave", BUENA, cuerpo="# Flujo\nAl clonar se colaron la llave de ElevenLabs y el token del espacio de origen. Nunca heredar el token de la cuenta.\n"), 0, None))
        casos.append(("no avisa: '## Requisitos' que SÍ dice qué hacer si falta (el fallo del 27-sep daba aviso)",
                      skill(tmp, "doble-almohadilla", BUENA, cuerpo="## Requisitos\nEl token del espacio. Si falta, para y pídelo.\n\n## Flujo\nLee .secrets/t.txt\n"), 0, "!no dice que hacer si falta"))
        casos.append(("avisa: '## Requisitos' que NO dice qué hacer si falta",
                      skill(tmp, "sin-plan", BUENA, cuerpo="## Requisitos\nEl token del espacio.\n\n## Flujo\nLee .secrets/t.txt\n"), 0, "no dice que hacer si falta"))
        casos.append(("avisa: 'no se pregunta' NO cuenta como pedir al correr (verde barato cazado el 27-sep)",
                      skill(tmp, "negada", BUENA, cuerpo="## Requisitos\nEl token del espacio. El nicho no se pregunta.\n\n## Flujo\nLee .secrets/t.txt\n"), 0, "no dice que hacer si falta"))
        casos.append(("no dispara: la palabra token suelta en prosa no es dependencia",
                      skill(tmp, "prosa", BUENA, cuerpo="# Flujo\nCuenta cada token del texto.\n"), 0, None))
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
        # P59 (27-sep): estos dos casos citaban un archivo INVENTADO ("references/x.md",
        # "scripts/otro.json") que nunca existio en golden-shopify — la version vieja del
        # detector exoneraba solo por el NOMBRE cercano, sin comprobar el archivo, y estos
        # casos pasaban por el hueco. Ahora citan un archivo REAL de golden-shopify: si de
        # verdad esta ahi, "no dispara" sigue siendo lo correcto.
        d = skill(tmp, "ref-calificada-antes", BUENA,
                  cuerpo="La receta vive en `golden-shopify` -> `references/arquetipos.md`.\n")
        casos.append(("no dispara: ruta calificada con la skill dueña ANTES (archivo real)", d, 0, None))
        d = skill(tmp, "ref-calificada-despues", BUENA,
                  cuerpo="Usa `scripts/autocheck.py` de golden-shopify, que lo mantiene.\n")
        casos.append(("no dispara: dueño nombrado DESPUES de la ruta (archivo real)", d, 0, None))
        # Gemelo real del P59: la MISMA cita calificada, pero el archivo que promete NO existe
        # en la skill dueña. Esto es exactamente lo que se colaba antes del arreglo (SKILL.md
        # con dos rutas inexistentes junto a "golden-shopify" -> 0 fallos, 0 avisos).
        d = skill(tmp, "ref-calificada-pero-falsa", BUENA,
                  cuerpo="La receta vive en `golden-shopify` -> `references/no-existe-ahi.md`.\n")
        casos.append(("caza: calificada con dueño real pero el archivo NO esta ahi", d, 1, "referencia rota"))
        d = skill(tmp, "ref-calificada-despues-pero-falsa", BUENA,
                  cuerpo="Usa `scripts/tampoco-existe.py` de golden-shopify, que lo mantiene.\n")
        casos.append(("caza: dueño DESPUES pero el archivo NO esta ahi", d, 1, "referencia rota"))
        d = skill(tmp, "ref-en-historia", BUENA,
                  cuerpo="<!-- v1.0: se renombro references/viejo.md a nuevo.md -->\ncuerpo\n")
        casos.append(("no dispara: referencia dentro de un comentario (historia)", d, 0, None))

        # P65 (28-sep, CdM): documentar una TRAMPA ("esta ruta no debe existir") no puede
        # penalizar igual que una cita muerta de verdad. Se baja a aviso, no se calla.
        d = skill(tmp, "ref-trampa-negada", BUENA,
                  cuerpo="Cuidado: `scripts/__pycache__/` no debe existir en el repo publicado.\n")
        casos.append(("no dispara: ruta con trampa documentada (no debe existir)", d, 0, None))
        d = skill(tmp, "script-trampa-se-borra", BUENA,
                  cuerpo="Antes de publicar, `scripts/temporal.py` se borra del paquete.\n")
        casos.append(("no dispara: script con trampa documentada (se borra)", d, 0, None))
        # Gemelo del contagio (la MISMA clase que ya se cazo dos veces en conexiones.py,
        # ahora DENTRO de una frase): la negacion de una ruta no puede rescatar a la OTRA
        # ruta que comparte la frase y de verdad esta rota.
        d = skill(tmp, "trampa-no-contagia-a-la-real", BUENA,
                  cuerpo="`scripts/temporal-trampa.py` no debe existir, y aparte corre "
                        "`scripts/real-sin-negacion.py` siempre al cerrar.\n")
        casos.append(("caza: la negacion de UNA ruta no contagia a la OTRA en la misma frase",
                      d, 1, "referencia rota"))
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

        # ---- VARIAS RUTAS: se revisan TODAS (26-sep). Con un glob el shell entrega N rutas
        # y el validador miraba solo la primera: "1 de 1 sanas" sobre 41 skills. La mala va
        # SEGUNDA a proposito: si solo se mira la primera, esta prueba sale en verde y falla.
        casos.append(("caza: varias rutas, la mala va SEGUNDA",
                      [_os.path.join(tmp, "sana"), _os.path.join(tmp, "larga")], 1, "UNIVERSO: 2"))

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
            if debe_decir and debe_decir.startswith("!"):
                bien = (rc == esperado) and (debe_decir[1:] not in salida)
            else:
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
