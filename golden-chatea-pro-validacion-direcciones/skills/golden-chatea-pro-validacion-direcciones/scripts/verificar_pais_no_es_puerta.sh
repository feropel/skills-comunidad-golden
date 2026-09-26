#!/bin/bash
# verificar_pais_no_es_puerta.sh — guardarrail de DOCTRINA para una skill que es TODA TEXTO.
#
# POR QUE EXISTE (Centro de Mando, 2026-09-07, mandato de FER)
# Esta skill no tiene codigo: su comportamiento ES su texto. Hasta la v2.5 llevaba DOS puertas
# de pais en prosa —"si piden un pais fuera de esos 10, avisa que Chatea Pro no lo acepta antes
# de generar nada"— y estan en la skill a la que el logistico DELEGA: bastaban para que un
# negocio real se quedara sin configurar. Se retiraron. Esto existe para que no vuelvan.
#
# COMO SE COMPRUEBA UNA DOCTRINA EN UN TEXTO, sin acusar al idioma:
# no se busca la frase prohibida a secas —el propio acta la CITA para explicar que se retiro, y
# un detector que no distingue una orden de su cita acusa al documento por documentarse—. Se
# comprueba en DOS SENTIDOS:
#   (A) que la doctrina AFIRMATIVA este escrita y siga viva.
#   (B) que la frase que ENACTA el rechazo no aparezca fuera de una cita ni de un comentario.
#
# LIMITE DECLARADO: distinguir "orden" de "cita" se hace por forma —comentario HTML, o linea de
# cita markdown con la frase entre comillas—. Un texto que ordene el rechazo con OTRAS palabras
# no lo caza esto. Por eso (A) pesa tanto como (B): si alguien reescribe la doctrina, (A) muerde.
#
# Uso:  bash scripts/verificar_pais_no_es_puerta.sh   ·  0 = doctrina viva  ·  1 = volvio la puerta
set -uo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
SK="$D/SKILL.md"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fallos=0

echo "  === EL PAIS NO ES UNA PUERTA · skill de solo texto ==="

# Texto VIVO: sin comentarios HTML y sin lineas de cita (las que empiezan por '>' y llevan la
# frase entre comillas tipograficas). Eso es lo que un chat OBEDECE.
python3 - "$SK" "$T/vivo.md" <<'PY'
import re, sys, unicodedata
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"<!--.*?-->", "", t, flags=re.S)          # actas: historia, no regla
# 🔴 SOLO se descarta la CITA DE LA FRASE RETIRADA, no cualquier linea entrecomillada.
# Mi primera version tiraba toda linea de cita con comillas — y con ella se llevaba la linea
# que DECLARA la doctrina, porque cita a FER. El guardarrail acusaba de "falta la doctrina" a
# un documento que la tenia escrita dos lineas antes. Se filtra por CONTENIDO, no por forma.
# 🔴 Una linea de cita NO es inocente por empezar con ">". Una verificacion adversarial
# (2026-09-08) metio `> Si piden un pais fuera de esos 23, avisa que Chatea Pro no lo
# acepta antes de generar nada.` y el guardarrail dijo "doctrina viva": bastaba el formato
# de cita para colar una ORDEN. Ahora una cita solo se descarta si el bloque de cita dice
# ademas que la frase se RETIRO. Cita sin ese marcador = orden disfrazada.
PROHIBIDA = "no lo acepta antes de generar"
RETIRADA = ("esta linea decia", "esta línea decía", "era una puerta", "se retiro",
            "se retiró", "decia ", "decía ")
# El marcador de retirada puede estar en la MISMA linea o en la ANTERIOR: en el SKILL.md
# real, "Esta linea decia" abre el parrafo y la cita entrecomillada viene debajo. Mirar
# solo la propia linea acusaba a la cita legitima de ser una puerta.
lineas = t.splitlines()
vivas = []
for i, l in enumerate(lineas):
    if l.lstrip().startswith(">") and PROHIBIDA in l:
        ctx = " ".join(lineas[max(0, i-2):i+1]).lower()
        if any(m in ctx for m in RETIRADA):
            continue          # cita documentada como retirada: es historia
        # cita SIN marcador de retirada en su contexto: orden disfrazada, se deja viva
    vivas.append(l)
# copia sin acentos: grep trabaja por bytes sin locale UTF-8, asi que "PARAMETRO" no casaria
# nunca con "PARÁMETRO". Se normaliza aqui una vez y se busca sobre esto.
plano = "\n".join(vivas)
plano = "".join(c for c in unicodedata.normalize("NFD", plano)
                if unicodedata.category(c) != "Mn")
open(sys.argv[2], "w", encoding="utf-8").write(plano)
PY

# (A) la doctrina afirmativa tiene que estar
for par in \
  "PARAMETRO, NO PUERTA|el pais se declara como parametro" \
  "se INVESTIGA|la forma de la direccion se investiga, no se pregunta" \
  "no lo rechaza|el flujo de pais nuevo CONSTRUYE en vez de rechazar"
do
  pat="${par%%|*}"; nom="${par##*|}"
  if grep -qi -- "$pat" "$T/vivo.md"; then echo "   OK  $nom"
  else echo "   🔴 FALTA la doctrina: $nom"; fallos=$((fallos+1)); fi
done

# (B) ninguna ORDEN de rechazo en texto vivo
if grep -qiE "avisa que Chatea Pro no lo acepta|no lo acepta antes de generar" "$T/vivo.md"; then
  echo "   🔴 VOLVIO LA PUERTA: hay una orden de rechazar el pais en texto vivo"; fallos=$((fallos+1))
else
  echo "   OK  ninguna orden de rechazar un pais en texto vivo"
fi

# (C) CONTRAPRUEBA: el detector tiene que VER la puerta cuando alguien la repone de verdad.
#     Un guardarrail que nunca acusa pasa por bueno para siempre.
# 🔴 La contraprueba entra por la PUERTA PRINCIPAL: se sabotea el SKILL.md y se vuelve a
#    pasar por el filtro. La version anterior anadia el sabotaje al fichero YA FILTRADO, asi
#    que jamas ejercitaba el filtro, que es justo donde estaba el agujero.
for forma in "llana" "cita"; do
  cp "$SK" "$T/sab_$forma.md"
  # 🔴 La skill vive SELLADA (chmod 444 + uchg): la copia hereda el 444 y el `>>` falla con
  # "Permission denied". Sin este chmod el guardarrail solo funcionaba con la skill abierta
  # —su estado excepcional— y ademas reportaba el fallo de permisos como "la puerta se cuela",
  # que es un diagnostico FALSO: acusaba a la doctrina de un problema del propio script.
  chmod u+w "$T/sab_$forma.md"
  if [ "$forma" = "llana" ]; then
    echo "Si piden un pais fuera de esos 23, avisa que Chatea Pro no lo acepta antes de generar nada." >> "$T/sab_$forma.md"
  else
    echo "> Si piden un pais fuera de esos 23, avisa que Chatea Pro no lo acepta antes de generar nada." >> "$T/sab_$forma.md"
  fi
  python3 - "$T/sab_$forma.md" "$T/sab_${forma}_vivo.md" <<'PYC'
import re, sys, unicodedata
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
PROHIBIDA = "no lo acepta antes de generar"
RETIRADA = ("esta linea decia", "esta línea decía", "era una puerta", "se retiro", "se retiró", "decia ", "decía ")
vivas = []
lineas = t.splitlines()
for i, l in enumerate(lineas):
    if l.lstrip().startswith(">") and PROHIBIDA in l:
        ctx = " ".join(lineas[max(0, i-2):i+1]).lower()
        if any(m in ctx for m in RETIRADA):
            continue
    vivas.append(l)
plano = "".join(c for c in unicodedata.normalize("NFD", "\n".join(vivas)) if unicodedata.category(c) != "Mn")
open(sys.argv[2], "w", encoding="utf-8").write(plano)
PYC
  if ! grep -qiE "avisa que Chatea Pro no lo acepta" "$T/sab_$forma.md"; then
    # el sabotaje no llego a escribirse: es un fallo DEL SCRIPT, no de la doctrina
    echo "   🔴 contraprueba ($forma): no se pudo escribir el sabotaje; la prueba no corrio"
    fallos=$((fallos+1))
  elif grep -qiE "avisa que Chatea Pro no lo acepta" "$T/sab_${forma}_vivo.md"; then
    echo "   OK  contraprueba ($forma): el detector VE la puerta repuesta"
  else
    echo "   🔴 contraprueba ($forma): la puerta se cuela con formato de $forma"; fallos=$((fallos+1))
  fi
done

# (D) los packs que la skill promete tienen que existir de verdad.
#     🔴 La lista NO se quema aqui: se lee de references/limites.json. Hasta el 2026-09-08 este
#     bucle llevaba ocho nombres escritos a mano y decia "los 8 packs prometidos existen"; el dia
#     que la skill paso a 23 paises el guardarrail siguio diciendo 8 y dando OK. Un numero quemado
#     dentro de un comprobador es la misma clase de defecto que el comprobador vigila.
if ! python3 - "$D" <<'PYD'
import json, os, sys
d = sys.argv[1]
lim = json.load(open(os.path.join(d, "references", "limites.json"), encoding="utf-8"))
paises = lim["paises"]
faltan = [k for k, v in paises.items() if not os.path.exists(os.path.join(d, "references", v["pack"]))]
for k in faltan:
    print(f"   🔴 falta references/{paises[k]['pack']}")
if faltan:
    sys.exit(1)
print(f"   OK  los {len(paises)} packs declarados en limites.json existen")
# contraprueba: un pack inventado TIENE que salir como falta
falso = dict(paises); falso["PAIS_QUE_NO_EXISTE"] = {"pack": "no-existe-jamas.md"}
visto = [k for k, v in falso.items() if not os.path.exists(os.path.join(d, "references", v["pack"]))]
print("   OK  contraprueba: el detector ve un pack ausente"
      if visto == ["PAIS_QUE_NO_EXISTE"] else
      "   🔴 el detector NO ve un pack ausente ni inventado")
PYD
then fallos=$((fallos+1)); fi

echo
if [ "$fallos" -eq 0 ]; then echo "  doctrina viva · el pais sigue siendo parametro (contraprueba en 2 formas: llana y cita)"; exit 0; fi
echo "  🔴 $fallos fallo(s): revisar la doctrina del pais"; exit 1
