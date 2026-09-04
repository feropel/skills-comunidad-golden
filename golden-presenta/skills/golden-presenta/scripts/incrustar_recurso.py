#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
incrustar_recurso.py - Convierte un logo o una tipografia en algo que cabe
DENTRO del deck, sin una sola peticion de red.

La ley de la skill es cero dependencias: un CDN caido o una sala sin wifi el dia
de la presentacion es el desastre entero. Todo recurso viaja incrustado.

USO

  Logo o imagen  ->  data URI listo para pegar en un src=""
      python3 incrustar_recurso.py imagen /ruta/logo.png
      python3 incrustar_recurso.py imagen /ruta/logo.png --salida uri.txt

  Tipografia     ->  bloque @font-face completo para pegar en el <style>
      python3 incrustar_recurso.py fuente /ruta/BigShoulders-Bold.ttf --nombre "Big Shoulders" --peso 700
      python3 incrustar_recurso.py fuente ... --salida fuente.css

  Ver que condensadas hay ya en casa, con licencia libre, sin descargar nada:
      python3 incrustar_recurso.py catalogo

AVISO DE PESO
  Cada recurso incrustado crece ~33% al pasar a base64. Una fuente de 100 KB
  ocupa ~133 KB dentro del archivo. El script avisa cuando el deck se pasaria
  de 3 MB, que es donde empieza a tardar en abrir desde WhatsApp.

LICENCIAS
  Las fuentes de `canvas-design/canvas-fonts/` son OFL (SIL Open Font License):
  se pueden incrustar y distribuir. El script copia el .txt de licencia al lado
  del deck cuando lo encuentra. Una fuente comercial NO se incrusta sin comprobar
  antes que su licencia lo permita.
"""

import base64
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES_CASA = os.path.expanduser('~/.claude/skills/canvas-design/canvas-fonts')

MIME = {
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
    '.ttf': 'font/ttf', '.otf': 'font/otf',
    '.woff': 'font/woff', '.woff2': 'font/woff2',
}

FORMATO_CSS = {'.ttf': 'truetype', '.otf': 'opentype',
               '.woff': 'woff', '.woff2': 'woff2'}

# Condensadas y display que ya estan en el Mac, con licencia libre.
# Se listan para no salir a Google Fonts por costumbre.
CONDENSADAS = [
    ('BigShoulders-Bold.ttf', 'Big Shoulders', 'Condensada display. La mas cercana a Anton. Titulares de evento.'),
    ('BigShoulders-Regular.ttf', 'Big Shoulders', 'La misma, en regular, para bajadas.'),
    ('Boldonse-Regular.ttf', 'Boldonse', 'Display pesada y rara. Para un titular que grite.'),
    ('EricaOne-Regular.ttf', 'Erica One', 'Display gorda con caracter. Carteles.'),
    ('Tektur-Bold.ttf', 'Tektur', 'Tecnica, angular. Para producto digital.'),
    ('Outfit-Bold.ttf', 'Outfit', 'Grotesca geometrica limpia. Corporativa moderna.'),
    ('Gloock-Regular.ttf', 'Gloock', 'Serif display de contraste alto. Editorial cara.'),
    ('YoungSerif-Regular.ttf', 'Young Serif', 'Serif con peso. Marca de producto.'),
]


def leer(ruta):
    if not os.path.isfile(ruta):
        print('No existe: %s' % ruta)
        sys.exit(2)
    with open(ruta, 'rb') as f:
        return f.read()


def avisar_peso(nombre, bytes_originales):
    kb = len(bytes_originales) / 1024.0
    kb64 = kb * 4 / 3
    print('# %s: %.0f KB en disco -> ~%.0f KB dentro del deck' % (nombre, kb, kb64),
          file=sys.stderr)
    if kb64 > 900:
        print('# AVISO: pasa de 900 KB. Comprime la imagen o usa una version mas '
              'pequena antes de incrustarla.', file=sys.stderr)


def cmd_imagen(args):
    ruta = args[0]
    ext = os.path.splitext(ruta)[1].lower()
    if ext not in MIME:
        print('Extension no soportada: %s' % ext)
        return 2
    datos = leer(ruta)
    avisar_peso(os.path.basename(ruta), datos)

    if ext == '.svg':
        # Un SVG cabe tal cual y pesa menos inline que en base64.
        texto = datos.decode('utf-8', errors='replace')
        print('# SVG: lo mas limpio es pegarlo INLINE dentro de la lamina,',
              file=sys.stderr)
        print('# dentro de <figure class="marco limpio">...</figure>.', file=sys.stderr)
        print('# Asi hereda los colores del deck con fill="currentColor".', file=sys.stderr)
        salida = texto
    else:
        b64 = base64.b64encode(datos).decode('ascii')
        salida = 'data:%s;base64,%s' % (MIME[ext], b64)

    destino = _destino(args)
    if destino:
        io.open(destino, 'w', encoding='utf-8').write(salida)
        print('Escrito en %s (%d caracteres)' % (destino, len(salida)), file=sys.stderr)
    else:
        print(salida)
    return 0


def cmd_fuente(args):
    ruta = args[0]
    ext = os.path.splitext(ruta)[1].lower()
    if ext not in FORMATO_CSS:
        print('No es una fuente reconocida: %s' % ext)
        return 2

    nombre = _opcion(args, '--nombre') or os.path.splitext(os.path.basename(ruta))[0]
    peso = _opcion(args, '--peso') or '400'
    estilo = _opcion(args, '--estilo') or 'normal'

    datos = leer(ruta)
    avisar_peso(os.path.basename(ruta), datos)
    b64 = base64.b64encode(datos).decode('ascii')

    css = (
        '/* %s · incrustada, sin peticiones de red.\n'
        '   Generada con scripts/incrustar_recurso.py */\n'
        '@font-face{\n'
        '  font-family:"%s";\n'
        '  font-style:%s;\n'
        '  font-weight:%s;\n'
        '  font-display:block;\n'
        '  src:url(data:%s;base64,%s) format("%s");\n'
        '}\n'
        '/* Y en :root ->  --font-display: "%s", "Arial Narrow", sans-serif; */\n'
        % (os.path.basename(ruta), nombre, estilo, peso,
           MIME[ext], b64, FORMATO_CSS[ext], nombre)
    )

    lic = _buscar_licencia(ruta)
    if lic:
        print('# Licencia encontrada: %s' % lic, file=sys.stderr)
        print('# Es OFL: se puede incrustar y distribuir. Guarda el .txt junto al deck.',
              file=sys.stderr)
    else:
        print('# AVISO: no encuentro archivo de licencia junto a la fuente.',
              file=sys.stderr)
        print('# Comprueba que su licencia permite incrustarla ANTES de entregar el deck.',
              file=sys.stderr)

    destino = _destino(args)
    if destino:
        io.open(destino, 'w', encoding='utf-8').write(css)
        print('Escrito en %s' % destino, file=sys.stderr)
    else:
        print(css)
    return 0


def cmd_catalogo(args):
    print('')
    print('CONDENSADAS Y DISPLAY QUE YA ESTAN EN CASA (licencia libre OFL)')
    print('Ruta: %s' % FUENTES_CASA)
    print('')
    if not os.path.isdir(FUENTES_CASA):
        print('  No encuentro la carpeta. La trae la skill `canvas-design`.')
        return 1
    hay = 0
    for archivo, nombre, para_que in CONDENSADAS:
        ruta = os.path.join(FUENTES_CASA, archivo)
        if os.path.isfile(ruta):
            kb = os.path.getsize(ruta) / 1024.0
            print('  %-28s %-18s %5.0f KB   %s' % (archivo, nombre, kb, para_que))
            hay += 1
        else:
            print('  %-28s %-18s   --      (no esta)' % (archivo, nombre))
    print('')
    print('  %d disponibles. Para incrustar una:' % hay)
    print('  python3 incrustar_recurso.py fuente "%s/BigShoulders-Bold.ttf" \\' % FUENTES_CASA)
    print('      --nombre "Big Shoulders" --peso 700')
    print('')
    print('  NO se sale a Google Fonts: rompe la ley de cero dependencias y el')
    print('  verificador lo marca como FALLA.')
    print('')
    return 0


def _opcion(args, clave):
    if clave in args:
        i = args.index(clave)
        if i + 1 < len(args):
            return args[i + 1]
    return None


def _destino(args):
    return _opcion(args, '--salida')


def _buscar_licencia(ruta_fuente):
    carpeta = os.path.dirname(ruta_fuente)
    base = os.path.basename(ruta_fuente).split('-')[0]
    for f in os.listdir(carpeta) if os.path.isdir(carpeta) else []:
        if f.startswith(base) and ('OFL' in f.upper() or 'LICEN' in f.upper()):
            return os.path.join(carpeta, f)
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == 'catalogo':
        return cmd_catalogo(args)
    if not args:
        print(__doc__)
        return 2
    if cmd == 'imagen':
        return cmd_imagen(args)
    if cmd == 'fuente':
        return cmd_fuente(args)
    print('Comando no reconocido: %s (usa imagen, fuente o catalogo)' % cmd)
    return 2


if __name__ == '__main__':
    sys.exit(main())
