#!/bin/bash
# comprobar-nube.sh — dice, para ESTE equipo, que carpetas se sincronizan y que
# haria la compuerta en cada una. No mueve ni escribe nada.
#
# Por que existe aparte del banco: la asercion 9 de `autoprueba.sh` prueba que la
# LOGICA acierta, con casos sinteticos y portatiles. Esto contesta otra pregunta,
# la que hizo FER: "que pasa con MIS carpetas". La respuesta cambia cuando el
# usuario activa o desactiva "Escritorio y Documentos en iCloud", asi que se
# vuelve a medir en vez de fiarse de lo que decia la ultima vez.
set -u
DIR="$(cd "$(dirname "$0")" && pwd -P)"
. "$DIR/_comun.sh"

veredicto() {
  local ruta="$1" servicio rc
  [ -e "$ruta" ] || { printf '  %-58s %s\n' "$ruta" "no existe en este equipo"; return 0; }
  servicio="$(carpeta_sincronizada "$ruta")"; rc=$?
  if   [ "$rc" -eq 1 ]; then printf '  ✅ %-55s LOCAL\n' "$ruta"
  elif [ "$rc" -eq 2 ]; then printf '  ⚠️  %-55s AVISA y sigue · %s\n' "$ruta" "$servicio"
  else                       printf '  🔴 %-55s PARA (exit 3) · %s\n' "$ruta" "$servicio"
  fi
}

echo "Servicios de nube instalados (~/Library/CloudStorage):"
if ls -1 "$HOME/Library/CloudStorage" 2>/dev/null; then :; else echo "  ninguno, o macOS no deja enumerarlo"; fi

echo ""
echo "Que haria la compuerta en cada carpeta:"
veredicto "$HOME/Desktop"
veredicto "$HOME/Documents"
veredicto "$HOME/Downloads"
for s in "$HOME/Library/CloudStorage"/*; do veredicto "$s"; done
veredicto "$HOME/Google Drive"
veredicto "$HOME/Dropbox"
veredicto "$HOME/Desktop/OneDrive"
veredicto "$HOME/Library/Mobile Documents/com~apple~CloudDocs"

echo ""
echo "Lectura real (una carpeta puede detectarse y aun asi no poderse leer):"
for s in "$HOME/Library/CloudStorage"/* "$HOME/Library/Mobile Documents/com~apple~CloudDocs"; do
  [ -e "$s" ] || continue
  if ls -1 "$s" >/dev/null 2>&1; then
    printf '  ✅ se lee   %s (%s entradas en el nivel 1)\n' "$s" "$(ls -1 "$s" 2>/dev/null | wc -l | tr -d ' ')"
  else
    printf '  🚫 NO se lee %s — macOS lo niega, su contenido no entra a ninguna corrida\n' "$s"
  fi
done
