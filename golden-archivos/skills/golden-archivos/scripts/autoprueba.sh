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

echo "== 7. Temporales con guarda: ningun mktemp a pelo =="
# La CLASE, no el caso. Medido 2026-09-27: con un mktemp falso, nombrar.sh y
# separar-web.sh salian con EXIT 0 habiendo hecho CERO trabajo, y duplicados.sh
# reportaba cero duplicados sobre cero archivos. Un mktemp sin `||` es esa bomba
# esperando: la variable queda vacia, "$VAR/x" se vuelve "/x" y la herramienta
# sigue como si nada. Esta asercion cubre los scripts que existan hoy y los que
# se agreguen manana, porque recorre el directorio en vez de una lista fija.
sin_guarda=""
for f in "$DIR"/*.sh; do
  grep -q 'mktemp' "$f" || continue
  # Se normaliza antes de juzgar: fuera comentarios y se unen las lineas
  # partidas con "\" (duplicados.sh encadena dos mktemp con && en dos lineas).
  # Despues, TODA linea viva que llame a mktemp debe tener su `||` ANTES del
  # siguiente `;`. Medido 2026-09-27: la version laxa `mktemp[^|]*\|\|` daba por
  # bueno `TMP="$(mktemp)"; : || {`, donde el `||` protege a otra cosa — un
  # candado que acepta eso no es candado, es adorno.
  malas=$(sed -e 's/[[:space:]]*#.*$//' -e ':a' -e '/\\$/N; s/\\\n//; ta' "$f" \
    | grep 'mktemp' | grep -vE 'mktemp[^;]*\|\|' \
    | grep -vE '^[[:space:]]*$' | wc -l | tr -d ' ')
  # autoprueba.sh se protege con un chequeo de la variable en la linea siguiente
  grep -q 'No se pudo crear el sandbox temporal' "$f" && malas=0
  [ "$malas" -eq 0 ] || sin_guarda="$sin_guarda $(basename "$f")"
done
[ -z "${sin_guarda// /}" ] && ok "todos los mktemp abortan si fallan" \
  || no "mktemp sin guarda (darian exit 0 sin trabajo):$sin_guarda"

echo "== 8. Compuerta de nube: todo script que escribe la llama =="
# Regla del CdM (27-sep): una skill que MUEVE, RENOMBRA o BORRA declara si su
# raiz esta sincronizada antes de la primera operacion, porque ahi el cambio no
# se queda en el equipo: viaja a la nube y a quien tenga acceso compartido.
# El detector busca la LLAMADA en codigo vivo, no la palabra: se quitan los
# comentarios primero. Un script que solo NOMBRE la compuerta en una nota sigue
# siendo un script que mueve archivos a ciegas.
sin_compuerta=""
for f in "$DIR"/*.sh; do
  base=$(basename "$f")
  [ "$base" = "autoprueba.sh" ] && continue   # no mueve nada: es el banco
  [ "$base" = "_comun.sh" ] && continue       # es quien DEFINE la compuerta
  vivo=$(sed -e 's/[[:space:]]*#.*$//' "$f")
  # "Escribe" significa tocar archivos DEL USUARIO. Un `rm -f "$TMP"` o un
  # `rm -rf "$WORK"` son limpieza de temporales propios y no necesitan compuerta:
  # contarlos daba dos falsos positivos (duplicados.sh, hoja-contactos.sh), y un
  # detector que grita de mas acaba ignorandose, que es la forma educada de no
  # existir. `rmdir` tampoco cuenta: solo quita carpetas ya vacias.
  toca=$(printf '%s' "$vivo" | grep -E '(^|[^[:alnum:]_])(mv|rm)[[:space:]]' \
         | grep -vcE '\$\{?(TMP|WORK|SIZES|HASHES)')
  [ "${toca:-0}" -gt 0 ] || continue
  printf '%s' "$vivo" | grep -q 'exigir_local' || sin_compuerta="$sin_compuerta $base"
done
[ -z "${sin_compuerta// /}" ] && ok "todo script que escribe avisa si la ruta es de nube" \
  || no "escriben sin comprobar si es carpeta sincronizada:$sin_compuerta"

echo "== 9. Espejo de iCloud: se detecta por INODO, no por nombre =="
# La asercion 8 comprueba que la compuerta se LLAMA. Esta comprueba que ACIERTA,
# que es otra cosa: la v1.16 nacio de una compuerta que se llamaba en los cinco
# scripts y declaraba local el disco de trabajo entero.
# Todo sintetico a proposito, para que no dependa de como tenga iCloud la maquina
# donde corra. El caso positivo de la rama del inodo no se puede fabricar (APFS
# no permite enlaces duros de directorio): ese se mide sobre el equipo real.
# `pwd -P` da /private/var donde mktemp da /var, asi que la raiz se resuelve de
# entrada o las comparaciones de prefijo no casan y esto sale verde por el
# motivo equivocado.
ESPEJO_OK=1
EB="$(cd "$T" && pwd -P)"

juzgar() { # juzgar <HOME sintetico> <ruta>  ->  imprime NUBE o LOCAL
  HOME="$1" bash -c '. "'"$DIR"'/_comun.sh"; if espejo_icloud "$1" >/dev/null; then echo NUBE; else echo LOCAL; fi' _ "$2" 2>/dev/null
}

# Senuelo: mismo nombre, objetos DISTINTOS. Por nombre diria nube.
H="$EB/esp-distinto"
mkdir -p "$H/Desktop/CARPETA" "$H/Library/Mobile Documents/com~apple~CloudDocs/Desktop/CARPETA"
[ "$(juzgar "$H" "$H/Desktop/CARPETA")" = "LOCAL" ] || ESPEJO_OK=0

# Sin gemelo en la nube: local.
H="$EB/esp-sinespejo"
mkdir -p "$H/Desktop/CARPETA" "$H/Library/Mobile Documents/com~apple~CloudDocs/OtraCosa"
[ "$(juzgar "$H" "$H/Desktop/CARPETA")" = "LOCAL" ] || ESPEJO_OK=0

# Llegar por el lado de iCloud: nube.
H="$EB/esp-porlanube"
mkdir -p "$H/Desktop" "$H/Library/Mobile Documents/com~apple~CloudDocs/Desktop/CARPETA"
[ "$(juzgar "$H" "$H/Library/Mobile Documents/com~apple~CloudDocs/Desktop/CARPETA")" = "NUBE" ] || ESPEJO_OK=0

[ "$ESPEJO_OK" -eq 1 ] && ok "el espejo de iCloud se juzga por inodo, no por nombre" \
  || no "la deteccion del espejo de iCloud falla: revisa espejo_icloud en _comun.sh"

echo "== 10. Sin ffmpeg: la skill y el script dicen lo MISMO, y ninguno miente =="
# El hallazgo de la v1.17: los dos declaraban que sin ffmpeg "los videos se
# verifican abriendolos uno a uno con Read", y Read NO abre MP4 — abre imagenes
# y PDF. Estaba en los DOS sitios porque uno se copio del otro, que es como se
# propaga esta clase. Por eso el candado exige las dos cosas a la vez: que
# ninguno prometa lo imposible, y que los dos nombren el mismo metodo de
# reserva (`qlmanage`), para que no vuelvan a divergir en silencio.
SKMD="$(dirname "$DIR")/SKILL.md"
MSG=$(grep -h 'Falta ffmpeg' "$DIR/hoja-contactos.sh")
FF_OK=1
[ -n "$MSG" ] || FF_OK=0
printf '%s' "$MSG"  | grep -q 'qlmanage' || FF_OK=0
grep -q 'qlmanage' "$SKMD"                || FF_OK=0
# la promesa falsa: "video ... Read" en la misma frase, en cualquiera de los dos
for archivo in "$SKMD" "$DIR/hoja-contactos.sh"; do
  grep -iE '[Vv]ideos?[^.]{0,80}con Read' "$archivo" | grep -viE 'no los abre|no abre|no se pueden abrir' \
    | grep -q . && FF_OK=0
done
[ "$FF_OK" -eq 1 ] && ok "el metodo sin ffmpeg es el mismo en los dos sitios y no promete abrir video con Read" \
  || no "SKILL.md y hoja-contactos.sh no coinciden sobre que hacer sin ffmpeg, o alguno dice que un video se abre con Read"

echo "== 11. Sin rutas absolutas de usuario: nada que identifique al dueno del Mac =="
# Fila del chat ARSENAL Y SKILLS (27-sep): su barrido de publicacion encontro
# `/Users/<usuario>/Desktop` en un COMENTARIO de _comun.sh. El repo es PUBLICO y
# eso no se borra despues: ni del historial de git ni de los clones que ya se
# hicieron. Lo redactaron en la copia publica, pero redactar al publicar es una
# red que solo existe mientras alguien use esa herramienta; el dia que se
# sincronice sin ella, se publica. Por eso la comprobacion vive AQUI, en origen.
# Cubre cualquier usuario, no solo el de este equipo.
fugas=""
for f in "$DIR"/*.sh "$(dirname "$DIR")"/SKILL.md "$(dirname "$DIR")"/references/*.md; do
  [ -f "$f" ] || continue
  if grep -qE '/Users/[A-Za-z0-9._-]+/' "$f"; then
    fugas="$fugas $(basename "$f")"
  fi
done
[ -z "${fugas// /}" ] && ok "ningun archivo trae una ruta absoluta de usuario" \
  || no "traen /Users/<alguien>/ y el repo es publico:$fugas"

echo "== 12. ffmpeg con -nostdin: que no se coma la lista del bucle =="
# Sin `-nostdin`, ffmpeg DRENA la entrada estandar. Cuando corre dentro de un
# `while read` cuya entrada es la lista de archivos, se come lineas y esas
# piezas no se procesan. Medido el 27-09-2026 en una biblioteca real: 85
# renderizadas de 92 candidatas, sin un solo mensaje de error.
# Mecanico y generalizable, asi que va como candado: cubre los scripts de hoy y
# los que se agreguen. Se quitan los comentarios antes de buscar.
sin_nostdin=""
for f in "$DIR"/*.sh; do
  # El banco se excluye: su PROPIO detector contiene la palabra que busca, asi
  # que sin esto se acusa a si mismo. Un detector que no puede mirarse sin
  # morderse no esta midiendo el disco, se esta mirando al espejo.
  [ "$(basename "$f")" = "autoprueba.sh" ] && continue
  vivo=$(sed -e 's/[[:space:]]*#.*$//' "$f")
  printf '%s' "$vivo" | grep -qE '(^|[^[:alnum:]_-])ffmpeg[[:space:]]' || continue
  # `command -v ffmpeg` y `which ffmpeg` NO son llamadas: comprueban si existe.
  # Contarlas acusaba al script que hace justo lo correcto, comprobar antes de usar.
  crudas=$(printf '%s' "$vivo" | grep -E '(^|[^[:alnum:]_-])ffmpeg[[:space:]]' \
           | grep -vE '(command -v|which|type)[[:space:]]+ffmpeg' \
           | grep -vc -- '-nostdin')
  [ "${crudas:-0}" -eq 0 ] || sin_nostdin="$sin_nostdin $(basename "$f")"
done
# GUARDA SIMETRICA, y es la mitad que importa: `ffprobe` NO acepta `-nostdin`.
# Se TRAGA el argumento siguiente y hace otra cosa sin decir que el argumento
# era malo. Medido el 27-09-2026 sobre un mp4 real: con `-nostdin` imprime el
# banner de version; sin el y con `</dev/null` imprime 10667.375000. Un agente
# lo sufrio en 178 videos: NA en los 178, sin un solo error.
# Un candado que EXIGE algo tiene que prohibir ese algo mal aplicado, o se
# convierte en la fuente del proximo fallo. La regla correcta es:
#   ffmpeg  -> -nostdin
#   ffprobe -> </dev/null, JAMAS -nostdin
ffprobe_malo=""
for f in "$DIR"/*.sh; do
  [ "$(basename "$f")" = "autoprueba.sh" ] && continue
  sed -e 's/[[:space:]]*#.*$//' "$f" | grep -qE 'ffprobe[[:space:]]+-nostdin' \
    && ffprobe_malo="$ffprobe_malo $(basename "$f")"
done

if [ -n "${ffprobe_malo// /}" ]; then
  no "le ponen -nostdin a ffprobe, que se traga el argumento siguiente y devuelve otra cosa:$ffprobe_malo"
elif [ -z "${sin_nostdin// /}" ]; then
  ok "ffmpeg lleva -nostdin, ffprobe no lo lleva: cada uno con lo suyo"
else
  no "llaman a ffmpeg sin -nostdin y pueden comerse piezas del bucle:$sin_nostdin"
fi

echo "== 13. Los de 0 bytes se CENSAN, no se tragan =="
# `duplicados.sh` ya los excluia del hasheo, y eso esta bien: todos comparten el
# md5 del vacio y agruparlos los presenta como copias de algo cuando son fallos
# distintos. Lo que estaba mal era excluirlos CALLANDO. Aqui se exige lo mismo
# que al mosaico desde la v1.6: si una pieza no entra al analisis, se dice.
V="$T/vacios"; mkdir -p "$V"
: > "$V/roto1.jpg"; : > "$V/roto2.jpg"; : > "$V/roto3.jpg"
printf 'igual' > "$V/a.txt"; printf 'igual' > "$V/b.txt"
sal=$(bash "$DIR/duplicados.sh" "$V" 2>&1)
vac_ok=1
printf '%s' "$sal" | grep -q '3 archivo(s) de 0 bytes' || vac_ok=0     # los cuenta
printf '%s' "$sal" | grep -q 'roto2.jpg'                || vac_ok=0     # los nombra
printf '%s' "$sal" | grep -q 'Grupos de duplicados exactos: 1' || vac_ok=0  # y no los agrupa
[ "$vac_ok" -eq 1 ] && ok "los archivos de 0 bytes se cuentan, se nombran y no se agrupan como duplicados" \
  || no "duplicados.sh no censa los archivos de 0 bytes, o los esta agrupando como si fueran copias"

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
