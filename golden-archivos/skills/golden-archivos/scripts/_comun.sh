#!/bin/bash
# _comun.sh — lo que comparten los scripts que ESCRIBEN en disco.
# Se carga con:  . "$(dirname "$0")/_comun.sh"
#
# Vive en UN solo archivo a proposito: cinco copias de la misma comprobacion
# divergen. Esta skill ya lo pago con las listas de extensiones de clasificar.sh
# y nombrar.sh, que se declararon "alineadas" y no lo estaban.

NUBE_ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

# ---------------------------------------------------------------------------
# Resuelve symlinks para juzgar la ruta REAL. Hace falta porque el enlace puede
# no parecer nube: en este equipo ~/Desktop/OneDrive apunta a
# ~/Library/CloudStorage/OneDrive-Personal(2), y juzgar por el nombre visible
# diria "es el Escritorio" cuando cada movimiento se sincroniza a la nube.
ruta_real() {
  local p="$1"
  if [ -d "$p" ]; then
    (cd "$p" 2>/dev/null && pwd -P)
  else
    local d
    d="$(cd "$(dirname "$p")" 2>/dev/null && pwd -P)" || return 1
    printf '%s/%s' "$d" "$(basename "$p")"
  fi
}

# ---------------------------------------------------------------------------
# "Escritorio y Documentos en iCloud" (ajuste de macOS). Es el caso que se le
# escapo a la primera version de esta compuerta, y se le escapo por el lado
# PEOR: daba verde sobre el disco de trabajo entero.
#
# Por que no lo veia: `pwd -P` no lo delata. Medido el 27-sep en este equipo,
# ~/Desktop resuelve a /Users/<usuario>/Desktop — a si mismo, sin enlace que
# seguir — y aun asi su contenido ESTA en iCloud. macOS no usa un symlink: los
# hijos son el MISMO objeto de disco que los de
# ~/Library/Mobile Documents/com~apple~CloudDocs/Desktop.
#
# Por eso la prueba es el INODO, no el nombre: ~/Desktop/⭐️ MASTER ⭐️ y su
# gemelo en CloudDocs dieron el mismo 16777233:237859135. Comparar por nombre
# daria un falso positivo en cuanto alguien tenga una carpeta llamada "Desktop"
# en su iCloud sin el ajuste activo.
#
# El propio ~/Desktop es la excepcion: NO comparte inodo con su gemelo (medido,
# 260833 contra 3878501), asi que ahi se pregunta por un hijo cualquiera.
espejo_icloud() {
  local real="$1" base sub twin hijo nombre i1 i2

  for base in Desktop Documents; do
    if [ "$real" = "$NUBE_ICLOUD/$base" ] || [[ "$real" == "$NUBE_ICLOUD/$base/"* ]]; then
      printf '%s' "$base"; return 0        # ya viene por el lado de iCloud
    fi
  done

  for base in Desktop Documents; do
    [ "$real" = "$HOME/$base" ] || [[ "$real" == "$HOME/$base/"* ]] || continue
    [ -d "$NUBE_ICLOUD/$base" ] || continue

    if [ "$real" != "$HOME/$base" ]; then
      sub="${real#"$HOME"/"$base"}"
      twin="$NUBE_ICLOUD/$base$sub"
      [ -e "$twin" ] || continue
      i1="$(stat -f '%d:%i' "$real" 2>/dev/null)"
      i2="$(stat -f '%d:%i' "$twin" 2>/dev/null)"
      if [ -n "$i1" ] && [ "$i1" = "$i2" ]; then printf '%s' "$base"; return 0; fi
    else
      for hijo in "$real"/*; do
        [ -e "$hijo" ] || continue
        nombre="${hijo##*/}"
        [ -e "$NUBE_ICLOUD/$base/$nombre" ] || continue
        i1="$(stat -f '%d:%i' "$hijo" 2>/dev/null)"
        i2="$(stat -f '%d:%i' "$NUBE_ICLOUD/$base/$nombre" 2>/dev/null)"
        if [ -n "$i1" ] && [ "$i1" = "$i2" ]; then printf '%s' "$base"; return 0; fi
      done
    fi
  done
  return 1
}

# ---------------------------------------------------------------------------
# Imprime el nombre del servicio si la ruta esta dentro de una carpeta
# sincronizada. Tres salidas, no dos, porque no todas las nubes pesan igual:
#   1 -> local, no hay nada que avisar
#   0 -> nube donde se PARA (Google Drive, OneDrive, Dropbox, iCloud Drive
#        suelto): son carpetas que alguien puso ahi a proposito y que a menudo
#        estan compartidas con otras personas
#   2 -> el espejo de "Escritorio y Documentos en iCloud": es la configuracion
#        por defecto del propio equipo y cubre el disco de trabajo completo.
#        Ahi se AVISA y se sigue. Parar seria bloquear el uso principal de la
#        skill en cada corrida, y un aviso que siempre bloquea se acaba
#        desactivando entero, que es peor que no tenerlo.
carpeta_sincronizada() {
  local real espejo
  real="$(ruta_real "$1")" || return 1
  [ -n "$real" ] || return 1

  # macOS moderno mete todos los servicios aqui y el nombre del servicio es la
  # primera carpeta (GoogleDrive-correo, OneDrive-Personal, Dropbox...).
  if [[ "$real" == "$HOME/Library/CloudStorage/"* ]]; then
    local resto="${real#"$HOME"/Library/CloudStorage/}"
    printf '%s' "${resto%%/*}"
    return 0
  fi

  espejo="$(espejo_icloud "$real")" \
    && { printf 'iCloud Drive (%s del equipo)' "$espejo"; return 2; }

  if [[ "$real" == "$HOME/Library/Mobile Documents/"* ]]; then
    printf 'iCloud Drive'; return 0
  fi
  # Rutas antiguas, anteriores a CloudStorage.
  local legado
  for legado in "Google Drive" "OneDrive" "Dropbox"; do
    if [[ "$real" == "$HOME/$legado" || "$real" == "$HOME/$legado/"* ]]; then
      printf '%s' "$legado"; return 0
    fi
  done
  return 1
}

# ---------------------------------------------------------------------------
# Compuerta: se llama ANTES de la primera escritura.
#   exigir_local "<ruta>" "<que se va a hacer>"
# Si la ruta esta sincronizada, PARA con exit 3 y explica la consecuencia.
# No pregunta por teclado a proposito: estos scripts corren desatendidos desde
# el agente, y un `read` ahi se cuelga para siempre. La confirmacion se da
# volviendo a llamar con GOLDEN_NUBE_OK=1, que obliga a que alguien decida.
exigir_local() {
  local ruta="$1" accion="${2:-escribir}" servicio rc
  servicio="$(carpeta_sincronizada "$ruta")"; rc=$?
  [ "$rc" -eq 1 ] && return 0                              # local: adelante

  if [ "$rc" -eq 2 ]; then
    echo "⚠️  $servicio: lo que se haga aqui se sincroniza a los otros equipos del usuario." >&2
    echo "   $accion en esta carpeta llega al iPhone y al iPad; un borrado tambien." >&2
    return 0
  fi

  if [ "${GOLDEN_NUBE_OK:-}" = "1" ]; then
    echo "⚠️  Confirmado por el usuario: se va a $accion dentro de $servicio (se sincroniza a la nube)." >&2
    return 0
  fi
  echo "🔴 ALTO. Esta carpeta esta dentro de $servicio, que se sincroniza." >&2
  echo "   Ruta: $(ruta_real "$ruta")" >&2
  echo "   $accion aqui NO se queda en este equipo: el cambio viaja a la nube," >&2
  echo "   a los demas equipos y a quien tenga acceso compartido. Si es un borrado," >&2
  echo "   desaparece para todos." >&2
  echo "   Preguntale al usuario y, si confirma, repite con GOLDEN_NUBE_OK=1 delante." >&2
  exit 3
}
