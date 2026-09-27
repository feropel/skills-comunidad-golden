#!/bin/bash
# autoprueba.sh  — banco de regresión de la skill. Sin argumentos.
# Corre los scripts contra un sandbox sembrado y EXIGE invariantes medidas.
# Si tocas cualquier script, corre esto antes de sellar.
#
# Existe por una falla real (2026-09-05): separar-web.sh devolvía "0 piezas"
# cuando la ruta traía barra final — y `for U in "$R"/*/`, la forma canónica de
# recorrer productos, SIEMPRE la trae. No daba error: daba cero. Un informe
# entero ("la biblioteca ya está separada") salió de ese cero falso.
# La lección: un cero hay que probarlo, no creerlo.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
T="$(mktemp -d 2>/dev/null)" || T=""
# Si mktemp falla (sandbox sin acceso a TMPDIR, disco lleno) T queda VACIO y
# "$T/a" se vuelve "/a": el sembrado muere, pero las aserciones siguen corriendo
# sobre carpetas que no existen y salen en VERDE por vacio. Medido 2026-09-27:
# 3 verdes mentirosos (deshacer "restaura" comparando vacio con vacio, eliminar
# "se niega" porque los archivos no existen, separar-web "respeta" porque no hay
# nada que grepear). Un banco que miente en verde es peor que no tenerlo.
[ -n "$T" ] && [ -d "$T" ] || { echo "🔴 No se pudo crear el sandbox temporal (mktemp fallo). El banco NO corre: sin sembrado sus verdes no valen." >&2; exit 1; }
trap 'rm -rf "$T"' EXIT
OK=0; FALLA=0
ok(){ OK=$((OK+1)); echo "  ✅ $1"; }
no(){ FALLA=$((FALLA+1)); echo "  🔴 $1"; }

# NOTA (2026-09-06): este banco prueba mover/renombrar/deshacer por EXTENSIÓN y
# contenido byte a byte — ningún bloque de abajo abre ni mira un píxel. Sembrar
# con ffmpeg era una dependencia de sobra: si ffmpeg faltaba (sandbox, CI, otra
# máquina) el banco entero se negaba a correr aunque nada de lo que prueba
# necesitara una imagen real (medido 2026-09-06: exit 1 "falta ffmpeg" en un
# entorno sin ffmpeg, pese a que los 6 bloques pasan igual con bytes planos).
# Se siembra con `printf` puro; el único script que sí necesita ffmpeg de
# verdad es hoja-contactos.sh, y ese lo declara y verifica él mismo.
sembrar(){ # sembrar <raiz>
  rm -rf "$1"; mkdir -p "$1/PROD/IMÁGENES" "$1/PROD/ANTES Y DESPUES/VIDEO"
  printf 'PNGDATA-placeholder-rojo' > "$1/PROD/suelto.png"
  printf d > "$1/PROD/datos.xlsx"
  printf 'PNGDATA-placeholder-azul' > "$1/PROD/IMÁGENES/master.png"
  # webp: basta el contenido mínimo reconocible por extensión, no se renderiza en este banco.
  printf 'RIFF$\000\000\000WEBPVP8L\027\000\000\000/\000\000\000\020\007\020\021\021\210\210\376\007\000' > "$1/PROD/IMÁGENES/web.webp"
  cp "$1/PROD/IMÁGENES/master.png" "$1/PROD/ANTES Y DESPUES/VIDEO/deliberado.webp"
  # El sembrado se COMPRUEBA: si no, una asercion sobre una carpeta vacia pasa
  # por vacio y el banco declara sano lo que ni siquiera se probo.
  for obligatorio in "$1/PROD/suelto.png" "$1/PROD/datos.xlsx" \
                     "$1/PROD/IMÁGENES/web.webp" \
                     "$1/PROD/ANTES Y DESPUES/VIDEO/deliberado.webp"; do
    [ -s "$obligatorio" ] || { echo "🔴 El sembrado fallo: falta $obligatorio. El banco NO puede dar veredicto." >&2; exit 1; }
  done
}

echo "== 1. Barra final: mismo resultado con y sin ella =="
for s in separar-web clasificar nombrar auditar hoja-contactos; do
  grep -q 'quita las barras finales' "$DIR/$s.sh" && ok "$s.sh normaliza la ruta" || no "$s.sh NO normaliza (volvería el cero falso)"
done

sembrar "$T/a"; A=$(bash "$DIR/separar-web.sh" "$T/a/PROD"  2>/dev/null | grep -oE '[0-9]+ piezas' | head -1)
sembrar "$T/b"; B=$(bash "$DIR/separar-web.sh" "$T/b/PROD/" 2>/dev/null | grep -oE '[0-9]+ piezas' | head -1)
[ -n "$A" ] && [ "$A" = "$B" ] && ok "separar-web: '$A' con y sin barra" || no "separar-web difiere: sin='$A' con='$B'"

echo "== 2. Sets deliberados intactos =="
echo "$(bash "$DIR/separar-web.sh" "$T/a/PROD" 2>/dev/null)" | grep -q 'ANTES Y DESPUES' \
  && no "separar-web se lleva material de ANTES Y DESPUES" || ok "separar-web respeta sets deliberados"

echo "== 3. Listas alineadas (se demuestra con diff, no se declara) =="
CLAS=$(sed -n '/^  case "\$ext" in/,/esac/p' "$DIR/clasificar.sh" | grep -oE '^[[:space:]]+[a-z0-9|]+\)' | tr -d ' )' | tr '|' '\n' | sort -u | grep -v '^\*$')
ALLOW=$(grep '^ALLOW=' "$DIR/nombrar.sh" | sed 's/.*"\(.*\)".*/\1/' | tr ' ' '\n' | sort -u)
H=$(comm -23 <(echo "$CLAS") <(echo "$ALLOW") | tr '\n' ' ')
[ -z "${H// /}" ] && ok "todo lo que clasificar mueve, nombrar lo prefija" || no "clasifica pero NO prefija: $H"

# El mismo diff, contra hoja-contactos.sh: un formato que clasificar.sh manda a
# IMÁGENES/GIFS/VIDEOS y que MEDIA_EXTS no cubre desaparece en silencio del
# mosaico (cae en "no son media" en vez de en el mosaico o en "no se pudo leer").
# Real 2026-09-20: faltaban ai/eps (clasificar.sh los manda a IMÁGENES).
CLAS_IMG=$(sed -n '/^  case "\$ext" in/,/esac/p' "$DIR/clasificar.sh" \
  | grep -E 'IMÁGENES|GIFS|VIDEOS' | grep -oE '^[[:space:]]+[a-z0-9|]+\)' | tr -d ' )' | tr '|' '\n' | sort -u | grep -v '^\*$')
MEDIA=$(grep '^MEDIA_EXTS=' "$DIR/hoja-contactos.sh" | sed 's/.*"\(.*\)".*/\1/' | tr ' ' '\n' | sort -u)
HM=$(comm -23 <(echo "$CLAS_IMG") <(echo "$MEDIA") | tr '\n' ' ')
[ -z "${HM// /}" ] && ok "todo lo que clasifica a IMÁGENES/GIFS/VIDEOS entra al mosaico" || no "clasifica pero el mosaico lo calla: $HM"

echo "== 4. El log manda: sin log no se mueve =="
sembrar "$T/c"
bash "$DIR/clasificar.sh" "$T/c/PROD" "/ruta/imposible/x.log" >/dev/null 2>&1 \
  && no "clasificar movió con log no escribible" || ok "clasificar se niega sin log escribible"

echo "== 5. Ida y vuelta: deshacer devuelve el árbol exacto =="
sembrar "$T/d"; ANTES=$(cd "$T/d/PROD" && find . -type f | sort | md5 -q)
L="$T/d/m.log"; : > "$L"
bash "$DIR/clasificar.sh" "$T/d/PROD" "$L" >/dev/null 2>&1
bash "$DIR/nombrar.sh"    "$T/d/PROD" "$L" >/dev/null 2>&1
bash "$DIR/deshacer.sh" "$L" >/dev/null 2>&1
DESPUES=$(cd "$T/d/PROD" && find . -type f | sort | md5 -q)
[ "$ANTES" = "$DESPUES" ] && ok "deshacer restaura el árbol idéntico" || no "deshacer NO restauró el árbol"

echo "== 6. eliminar.sh se niega si no son idénticos =="
sembrar "$T/e"; printf 'uno' > "$T/e/x"; printf 'dos' > "$T/e/y"
bash "$DIR/eliminar.sh" "$T/e/x" "$T/e/y" "$T/e/del.log" >/dev/null 2>&1 \
  && no "eliminar borró archivos DISTINTOS" || ok "eliminar se niega con md5 distinto"

echo ""
echo "RESULTADO: $OK en verde · $FALLA en rojo"
[ "$FALLA" -eq 0 ] || exit 1
