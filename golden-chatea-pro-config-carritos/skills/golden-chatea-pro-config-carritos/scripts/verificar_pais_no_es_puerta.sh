#!/bin/bash
# verificar_pais_no_es_puerta.sh — guardarrail de la DOCTRINA, no de un dato.
#
# HISTORIA, porque explica el cambio de oficio. Su antecesor (verificar_paises.sh) comprobaba que
# el cuerpo declarara la lista COMPLETA de paises aceptados. Nacio de un fallo real: el 05-sep el
# cuerpo decia "solo acepta 7 paises" cuando eran 10, y con eso la skill RECHAZABA Guatemala,
# Argentina y Brasil. El script funcionaba y cazaba el sabotaje.
# Pero defendia lo que no habia que defender: obligaba a mantener en el cuerpo un dato que CADUCA
# SOLO. FER lo zanjo el 06-sep: "ahorita son diez, manana doce, pasado veinte; el pais es para
# saber como enfocarlo, no para prohibir". La cura de un dato que caduca no es vigilarlo: es no
# depender de el.
# Asi que este script hace lo contrario que su antecesor: FALLA SI LA LISTA VUELVE.
#
# QUE ES UNA PUERTA (falla) vs QUE ES CONTEXTO (pasa):
#   puerta  = una lista de paises en el cuerpo, o un numero que los cuente, o un "uno de los N"
#   contexto= nombrar un pais en un EJEMPLO, o remitir al dato duro para saber si hay pack conocido
#
# ALCANCE: solo texto vivo. Los comentarios HTML son historia (los changelogs citan la lista vieja
# a proposito) y no se miden — misma leccion que dejo el antecesor.
#
# USO:  bash scripts/verificar_pais_no_es_puerta.sh [ruta-de-la-skill]
# SALE: 0 = el pais es parametro · 1 = volvio a ser puerta

set -u
SKILL_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CUERPO="$SKILL_DIR/SKILL.md"
[ -f "$CUERPO" ] || { echo "🔴 no encuentro SKILL.md en $SKILL_DIR"; exit 1; }

VIVO=$(python3 -c "
import re,sys
s=open(sys.argv[1],encoding='utf-8').read()
print(re.sub(r'<!--.*?-->','',s,flags=re.S))
" "$CUERPO")

RC=0
echo "ALCANCE: solo texto vivo (comentarios HTML descartados)"

# 1 · un numero haciendo de censo de paises
if printf '%s' "$VIVO" | grep -qiE '(acepta|solo|unicamente|únicamente)[^.]{0,30}[0-9]+ (países|paises)'; then
  echo "🔴 PUERTA: el cuerpo declara una CANTIDAD de paises aceptados"
  printf '%s' "$VIVO" | grep -inE '(acepta|solo|unicamente|únicamente)[^.]{0,30}[0-9]+ (países|paises)' | head -3 | sed 's/^/     /'
  RC=1
fi

# 2 · una enumeracion de paises en MAYUSCULA (3 o mas seguidos = lista, no ejemplo)
if printf '%s' "$VIVO" | grep -qE '(ARGENTINA|BRASIL|CHILE|COLOMBIA|ECUADOR|GUATEMALA|MEXICO|PANAMA|PARAGUAY|PERU)([ ,·]+(ARGENTINA|BRASIL|CHILE|COLOMBIA|ECUADOR|GUATEMALA|MEXICO|PANAMA|PARAGUAY|PERU)){2,}'; then
  echo "🔴 PUERTA: hay una ENUMERACION de paises en el cuerpo (3 o mas seguidos)"
  RC=1
fi

# 2b · una enumeracion de paises EN PROSA (3 o mas seguidos, en cualquier caja). La v3.3 solo
# miraba MAYUSCULAS y dejaba pasar "solo se configura para Colombia, Mexico, Chile y Peru".
if printf '%s' "$VIVO" | grep -qiE '(argentina|brasil|chile|colombia|ecuador|guatemala|m[eé]xico|panam[aá]|paraguay|per[uú])([ ,·]+(y )?(argentina|brasil|chile|colombia|ecuador|guatemala|m[eé]xico|panam[aá]|paraguay|per[uú])){2,}'; then
  echo "🔴 PUERTA: hay una ENUMERACION de paises en prosa (3 o mas seguidos)"
  printf '%s' "$VIVO" | grep -inE '(argentina|brasil|chile|colombia|ecuador|guatemala|m[eé]xico|panam[aá]|paraguay|per[uú])([ ,·]+(y )?(argentina|brasil|chile|colombia|ecuador|guatemala|m[eé]xico|panam[aá]|paraguay|per[uú])){2,}' | head -3 | sed 's/^/     /'
  RC=1
fi

# 2c · la frase que rechaza por pais
if printf '%s' "$VIVO" | grep -qiE 'si el (país|pais) no (está|esta)[^.]{0,30}(rechaz|no se configura)|no se configura (si|cuando)[^.]{0,20}(país|pais)'; then
  echo "🔴 PUERTA: hay una frase que RECHAZA por pais"
  RC=1
fi

# 3 · el intake volviendo a filtrar
if printf '%s' "$VIVO" | grep -qiE 'uno de los [0-9]+|de los [0-9]+ de arriba|solo si (el )?(país|pais) (está|esta) en'; then
  echo "🔴 PUERTA: el intake vuelve a validar el pais contra una lista"
  RC=1
fi

# 4 · lo que SI tiene que estar: el pais como parametro
# OJO: el patron evita a proposito la palabra acentuada (PARAMETRO). `grep -i` NO pliega acentos
# en locale C, asi que buscar 'par[aá]metro' falla contra 'PARÁMETRO' en mayuscula. Trampa medida.
if ! printf '%s' "$VIVO" | grep -qiE '(nunca|no) como puerta'; then
  echo "⚠️  falta la declaracion explicita de que el pais es PARAMETRO y no puerta"
  RC=1
fi

[ $RC -eq 0 ] && echo "✅ el pais es parametro: sin censo, sin enumeracion, sin filtro en el intake"
exit $RC
