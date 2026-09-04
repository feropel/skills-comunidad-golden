#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_deck.py - Auditor de decks de Golden Presenta.

Uso:
    python3 verificar_deck.py /ruta/al/deck.html
    python3 verificar_deck.py /ruta/al/deck.html --json

Filosofia (Protocolo de Verificacion Golden):
    Reporta COBERTURA, no veredicto. Dice cuantas comprobaciones corrio,
    cuantas laminas inspecciono, que falla y que NO pudo verificar.
    Nunca imprime "quedo perfecto".

Salida:
    codigo 0 = sin FALLAS (puede haber avisos)
    codigo 1 = hay al menos una FALLA
    codigo 2 = no se pudo leer el archivo
"""

import sys
import os
import re
import json

# ----------------------------------------------------------------------
# Utilidades de color WCAG
# ----------------------------------------------------------------------

def hex_a_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def luminancia(rgb):
    def canal(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(hex_a, hex_b):
    ra, rb = hex_a_rgb(hex_a), hex_a_rgb(hex_b)
    if not ra or not rb:
        return None
    la, lb = luminancia(ra), luminancia(rb)
    claro, oscuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (oscuro + 0.05)


# ----------------------------------------------------------------------
# Auditor
# ----------------------------------------------------------------------

class Auditoria(object):
    def __init__(self, ruta):
        self.ruta = ruta
        self.fallas = []
        self.avisos = []
        self.ok = []
        self.no_verificado = []
        self.corridas = 0

    def check(self, nombre, condicion, detalle_falla, grave=True):
        """Registra UNA comprobacion. condicion True = pasa."""
        self.corridas += 1
        if condicion:
            self.ok.append(nombre)
        elif grave:
            self.fallas.append((nombre, detalle_falla))
        else:
            self.avisos.append((nombre, detalle_falla))

    def sin_verificar(self, que, porque):
        self.no_verificado.append((que, porque))


def auditar(ruta):
    a = Auditoria(ruta)

    # --- Lectura estricta en UTF-8: si truena aqui, los acentos estan rotos ---
    with open(ruta, 'rb') as f:
        crudo = f.read()
    try:
        html = crudo.decode('utf-8')
        a.check('Archivo decodifica en UTF-8', True, '')
    except UnicodeDecodeError as e:
        a.check('Archivo decodifica en UTF-8', False,
                'El archivo NO es UTF-8 valido (%s). Los acentos saldran rotos en el render.' % e)
        html = crudo.decode('utf-8', errors='replace')

    tam_kb = len(crudo) / 1024.0

    # Vista SIN comentarios HTML. Todo lo que mide CONTENIDO usa esta vista.
    # Motivo medido (2026-09-02): la plantilla documenta su propio uso con un
    # ejemplo <section class="slide"> dentro de un comentario. Contarlo inflaba
    # el inventario en +1 lamina y hacia que la falsa lamina se tragara el CSS
    # entero (12.320 caracteres). La clase del fallo es "el auditor lee lo que
    # el navegador ignora", no este caso puntual.
    visible = re.sub(r'<!--.*?-->', '', html, flags=re.S)

    # Solo el contenido que llega al usuario: fuera CSS y JS. Las constantes del
    # motor (MODO_CANVAS_PX, MIN_VISIBLE_MS) no son texto de nadie, y colarlas
    # produce falsos positivos justo en los checks de redaccion.
    cuerpo = re.sub(r'<style[^>]*>.*?</style>', ' ', visible, flags=re.S | re.I)
    cuerpo = re.sub(r'<script[^>]*>.*?</script>', ' ', cuerpo, flags=re.S | re.I)

    # ------------------------------------------------------------------
    # 1 · Placeholders sin rellenar
    # ------------------------------------------------------------------
    pend = sorted(set(re.findall(r'GP_[A-Z0-9_]+', visible)))
    a.check('Sin placeholders GP_ sin rellenar', not pend,
            'Quedaron %d placeholders sin contenido real: %s'
            % (len(pend), ', '.join(pend[:12]) + ('...' if len(pend) > 12 else '')))

    # Restos de sustitucion PARCIAL. Un placeholder que es prefijo de otro
    # (GP_TITULO dentro de GP_TITULO_TARJETAS) se sustituye a medias y deja
    # colgando "_TARJETAS" en mitad de un titular. Ya no hay ningun "GP_" que
    # buscar, asi que el check anterior lo daba por bueno. Medido en navegador
    # el 2026-09-02: el titulo salio "MBA Comunidad Golden_TARJETAS".
    restos = sorted(set(re.findall(r'_[A-Z]{3,}(?![A-Za-z0-9_])',
                                   re.sub(r'<[^>]+>', ' ', cuerpo))))
    a.check('Sin restos de placeholder sustituido a medias', not restos,
            'Aparecen fragmentos en mayusculas con guion bajo: %s. Sintoma de un '
            'placeholder que es prefijo de otro y se reemplazo a medias. Sustituir '
            'SIEMPRE de la clave mas larga a la mas corta.' % ', '.join(restos[:8]))

    # ------------------------------------------------------------------
    # 2 · Acentos: mojibake y charset  (regla de FER: verificar en el render)
    # ------------------------------------------------------------------
    a.check('Declara charset UTF-8',
            re.search(r'<meta\s+charset=["\']?utf-8', html, re.I) is not None,
            'Falta <meta charset="utf-8"> en el <head>: el navegador puede romper los acentos.')

    # Clase ampliada (F4, verificador adversarial 2026-09-02): la version anterior
    # usaba los controles latin-1 (U+009C) en vez de los caracteres cp1252 REALES
    # que produce Word/Excel (U+0153, U+201C, U+201D, U+2122). Medido: 2 de 6
    # variantes de mojibake pasaban sin detectar, incluida la comilla curva, que
    # es la mas comun al pegar desde un documento.
    mojibake = re.findall(u'\u00e2\u20ac.|\u00c3[\u0080-\u00ff]|\u00c2[\u00a0-\u00bf]', html)
    a.check('Sin mojibake de doble codificacion', not mojibake,
            'Se encontraron %d secuencias tipo "Ã©"/"â€": el texto se codifico dos veces.'
            % len(mojibake))

    # Acentos presentes: un deck en espanol sin una sola tilde es sospechoso
    tildes = len(re.findall(r'[áéíóúñÁÉÍÓÚÑ]', visible))

    # F1 (verificador adversarial 2026-09-02): antes esta variable se contaba,
    # se imprimia en la linea "Universo" y NUNCA se comprobaba. Un deck entero
    # sin un solo acento pasaba con 26/26. El comentario decia "es sospechoso"
    # y no habia check detras. Ahora si lo hay, y busca la CLASE: palabras que
    # en espanol SIEMPRE llevan tilde y aparecen escritas sin ella.
    SIEMPRE_CON_TILDE = [
    'operacion', 'ubicacion', 'sesion', 'union', 'mision', 'presion', 'ocasion', 'oracion', 'estacion', 'duracion', 'relacion', 'solucion', 'situacion', 'condicion', 'division', 'revision', 'emision', 'fusion', 'tension', 'pension', 'organizacion', 'participacion', 'optimizacion', 'automatizacion', 'integracion', 'validacion', 'medicion', 'edicion', 'creacion', 'ejecucion', 'distribucion', 'instalacion', 'migracion', 'notificacion', 'planificacion', 'clasificacion', 
   
        'presentacion', 'informacion', 'configuracion', 'aplicacion', 'seccion',
        'opcion', 'version', 'atencion', 'decision', 'direccion', 'produccion',
        'comunicacion', 'introduccion', 'conclusion', 'inversion', 'gestion',
        'ademas', 'tambien', 'despues', 'ultimo', 'ultima', 'ultimas', 'ultimos',
        'unico', 'unica', 'rapido', 'rapida', 'facil', 'dificil', 'numero',
        'numeros', 'maximo', 'minimo', 'proximo', 'proxima', 'credito', 'telefono',
        'articulo', 'publico', 'publica', 'practica', 'tecnica', 'analisis',
        'categoria', 'dia', 'dias', 'aqui', 'alli', 'ahi', 'asi', 'lamina',
        'laminas', 'pagina', 'paginas', 'reves', 'quizas', 'segun', 'aun',
        'estara', 'sera', 'hara', 'podra', 'vendra', 'ingles', 'espanol',
    ]
    # Se analiza SOLO lo que llega al usuario: el texto de las laminas, los
    # atributos que lee un lector de pantalla, y las cadenas literales del JS.
    # Quedan fuera el CSS, los comentarios de codigo y los identificadores
    # (un `id` como "lamina-3" no es texto que nadie lea).
    atributos = ' '.join(
        x for t in re.findall(
            r'(?:aria-label|title|alt|placeholder|data-notas)\s*=\s*["\']([^"\']*)',
            visible, re.I) for x in [t])
    cadenas_js = ''
    # Todos los bloques de script: el deck lleva el motor de atmosferas y el
    # motor de camara, y el texto que ve el usuario puede salir de cualquiera.
    for mjs in re.findall(r'<script[^>]*>(.*?)</script>', visible, re.S | re.I):
        js = re.sub(r'/\*.*?\*/', ' ', mjs, flags=re.S)
        js = re.sub(r'(?m)//.*$', ' ', js)
        cadenas_js += ' ' + ' '.join(
            a or b for a, b in re.findall(r"'([^'\n]{3,})'|\"([^\"\n]{3,})\"", js))
    texto_plano = re.sub(r'<[^>]+>', ' ', cuerpo) + ' ' + atributos + ' ' + cadenas_js

    # AMBIGUAS: cada una es tambien una forma VERBAL que va SIN tilde.
    # "el sistema publica gratis" es correcto; "la pagina publica" (adjetivo) no.
    # La palabra suelta no permite decidir, asi que estas NO bloquean: avisan.
    # Origen: 2026-09-03, un deck CORRECTO quedo bloqueado por 'publica' y hubo
    # que reescribir la frase para poder entregar. Un detector agresivo hace
    # tanto daño como uno ciego, y cuesta mas descubrirlo.
    AMBIGUAS_VERBO = {'publica', 'publico', 'practica', 'numero', 'articulo', 'ultimo'}

    def _aparece(w):
        return re.search(r'(?<![\w\-_áéíóúñ])' + w + r'(?![\w\-_áéíóúñ])', texto_plano, re.I)

    sin_tilde = sorted(set(
        w for w in SIEMPRE_CON_TILDE
        if w not in AMBIGUAS_VERBO and _aparece(w)))
    dudosas = sorted(set(
        w for w in SIEMPRE_CON_TILDE
        if w in AMBIGUAS_VERBO and _aparece(w)))

    a.check('Acentos puestos en el texto que se ve',
            not sin_tilde,
            'Palabras escritas SIN su tilde en el contenido: %s. '
            'El deck se entrega con los acentos sin poner, y eso se ve en pantalla '
            'y lo lee en voz alta un lector de pantalla.'
            % ', '.join(sin_tilde[:15]))

    a.check('Palabras que pueden ir con o sin tilde',
            not dudosas,
            'Aparecen sin tilde: %s. Cada una es tambien un VERBO y entonces va '
            'sin tilde ("el sistema publica gratis" es correcto). Si en tu frase '
            'es sustantivo o adjetivo, ponsela ("la pagina publica" -> publica). '
            'No bloquea la entrega: lo decide quien escribe.'
            % ', '.join(dudosas[:15]),
            grave=False)

    # ------------------------------------------------------------------
    # 3 · Reglas de escritura Golden
    # ------------------------------------------------------------------
    # ESTANDAR CORREGIDO (FER, 2026-09-03): "las presentaciones si deben llevar la
    # manera ortografica correcta. Solamente cuando escribimos, que no parezcamos
    # un bot". O sea: la regla de escribir sin ¿ ¡ es para NUESTRA prosa en el chat
    # y los informes, NO para el texto que se publica y proyecta. En un deck los
    # signos de apertura son LO CORRECTO.
    #
    # El check estaba INVERTIDO y bloqueaba la entrega de decks bien escritos.
    # Ahora comprueba lo contrario: que no falte el signo de apertura.
    frases = re.split(r'[\n\r]+', re.sub(r'<[^>]+>', '\n', cuerpo))
    sin_apertura = []
    for f in frases:
        f = f.strip()
        if not f or len(f) > 300:
            continue
        # Cierra con ? o ! pero en toda la frase no hay signo de apertura
        if re.search(r'[?!]\s*$', f) and not re.search(r'[¿¡]', f):
            sin_apertura.append(f[:60])
    a.check('Interrogaciones y exclamaciones bien abiertas',
            not sin_apertura,
            'Frases que cierran con ? o ! y les falta el signo de apertura: %s. '
            'En una presentacion se escribe con ortografia correcta: "¿Que pasa?", '
            'no "Que pasa?".' % ' · '.join('"%s"' % x for x in sin_apertura[:5]))

    # ------------------------------------------------------------------
    # 4 · Estructura del motor
    # ------------------------------------------------------------------
    for nombre, patron, detalle in [
        ('Existe el lienzo #stage', r'id=["\']stage["\']',
         'Sin #stage no hay camara: el motor no puede mover nada.'),
        ('Existe el HUD de navegacion', r'id=["\']hud["\']',
         'Sin HUD no hay contador ni botones de avance.'),
        ('Existe la barra de progreso', r'id=["\']progreso["\']',
         'Sin barra el publico no sabe cuanto falta.'),
        ('Respeta prefers-reduced-motion', r'prefers-reduced-motion',
         'Sin este bloque, quien tenga movimiento reducido activado igual recibe el viaje de camara.'),
        ('Tiene modo flujo para movil', r'max-width\s*:\s*899px',
         'Sin el corte a 899px la camara sigue activa en celular y el texto queda ilegible.'),
        ('Tiene salida a PDF (@media print)', r'@media\s+print',
         'Sin @media print no se puede exportar el deck a PDF con una lamina por pagina.'),
        ('Tiene modo presentador', r'id=["\']presentador["\']',
         'Sin modo presentador no hay notas ni cronometro al exponer.'),
        ('Tiene preloader con contador', r'id=["\']pre-num["\']',
         'Falta el ritual de entrada (contador 0-100 + cortina).'),
    ]:
        a.check(nombre, re.search(patron, html, re.I) is not None, detalle)

    # ------------------------------------------------------------------
    # 5 · Dependencias externas (lo que se puede caer)
    # ------------------------------------------------------------------
    # F3 (verificador adversarial 2026-09-02): la version anterior solo miraba
    # <script> y <link>. Una <img>, un <iframe> o un @import de red pasaban con
    # 26/26, y encima Google Fonts estaba excluido a proposito. Eso contradecia
    # de frente la promesa de la skill ("cero dependencias externas"). Ahora se
    # mira CUALQUIER referencia de red y es FALLA, no aviso: un deck que depende
    # de internet se rompe el dia de la presentacion, que es el unico dia que importa.
    externos = re.findall(
        r'<(?:script|link|img|iframe|video|audio|source|embed|object|track)[^>]+'
        r'(?:src|href|data|poster)=["\'](https?://[^"\']+)', visible, re.I)
    externos += re.findall(r'@import\s+(?:url\()?["\']?(https?://[^"\')\s]+)', visible, re.I)
    externos += re.findall(r'url\(\s*["\']?(https?://[^"\')\s]+)', visible, re.I)
    externos = sorted(set(externos))
    a.check('Sin dependencias externas que se puedan caer', not externos,
            'El deck carga %d recurso(s) de red: %s. Si el CDN cae o la sala no tiene '
            'internet, el deck se rompe. Se incrusta el recurso en el archivo o se quita.'
            % (len(externos), ', '.join(externos[:3])))

    # ------------------------------------------------------------------
    # 6 · Laminas: posicion, colision, notas, densidad
    # ------------------------------------------------------------------
    laminas = re.findall(r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>(.*?)</section>',
                         visible, re.S | re.I)
    cabeceras = re.findall(r'<section[^>]*class=["\'][^"\']*\bslide\b[^"\']*["\'][^>]*>', visible, re.I)
    n_lam = len(cabeceras)

    a.check('El deck tiene laminas', n_lam > 0,
            'No se encontro ninguna <section class="slide">.')

    if n_lam:
        a.check('Cantidad de laminas razonable (3 a 25)', 3 <= n_lam <= 25,
                'El deck tiene %d laminas. Menos de 3 no cuenta una historia; mas de 25 pierde a la sala.'
                % n_lam, grave=False)

        posiciones = {}
        sin_pos, sin_notas, colisiones = [], [], []
        for i, cab in enumerate(cabeceras, start=1):
            # F2 (verificador adversarial 2026-09-02): las notas se comprueban ANTES
            # del continue. Antes, una lamina sin posicion saltaba el resto del bucle
            # y su falta de notas nunca se reportaba: tenia dos defectos y solo salia uno.
            if 'data-notas' not in cab:
                sin_notas.append(i)
            mx = re.search(r'data-x=["\']([-\d.]+)["\']', cab)
            my = re.search(r'data-y=["\']([-\d.]+)["\']', cab)
            if not mx or not my:
                sin_pos.append(i)
                continue
            clave = (float(mx.group(1)), float(my.group(1)))
            if clave in posiciones:
                colisiones.append((posiciones[clave], i, clave))
            else:
                posiciones[clave] = i

        a.check('Todas las laminas tienen posicion (data-x / data-y)', not sin_pos,
                'Laminas sin posicion: %s. La camara las apilara todas en el centro del lienzo.'
                % sin_pos)

        a.check('Sin laminas superpuestas en el lienzo', not colisiones,
                'Estas laminas comparten coordenada: %s. Se van a tapar entre si.'
                % '; '.join('%d y %d en %s' % (c[0], c[1], c[2]) for c in colisiones))

        a.check('Todas las laminas tienen notas de presentador', not sin_notas,
                'Laminas sin data-notas: %s. El modo presentador saldra vacio ahi.' % sin_notas,
                grave=False)

        # Densidad de texto: una lamina no es un documento
        cargadas = []
        # OJO: esta variable NO puede llamarse `cuerpo`. Lo hacia, y al ser el
        # bucle del nivel de la funcion, pisaba la variable `cuerpo` que guarda
        # el documento entero. Todo check posterior al bucle recibia solo la
        # ULTIMA lamina. Medido el 2026-09-03: el check de clases huerfanas veia
        # 300 caracteres y 3 clases en vez del documento de 1,2 MB, y por eso no
        # cazaba nada. Clase del fallo: variable de bucle que sombrea una global.
        for i, cuerpo_lamina in enumerate(laminas, start=1):
            texto = re.sub(r'<[^>]+>', ' ', cuerpo_lamina)
            texto = re.sub(r'\s+', ' ', texto).strip()
            if len(texto) > 550:
                cargadas.append((i, len(texto)))
        a.check('Ninguna lamina esta sobrecargada de texto', not cargadas,
                'Laminas con mas de 550 caracteres: %s. Eso ya no se lee de pie: se parte '
                'la lamina en dos o el detalle se va a un anexo.'
                % ', '.join('#%d (%d)' % c for c in cargadas))

    # ------------------------------------------------------------------
    # 6b · Atmosfera: la que se declara tiene que existir en el motor
    # ------------------------------------------------------------------
    ATMOSFERAS = ['nebulosa', 'candela', 'aurora', 'pulso', 'enjambre',
                  'reticula', 'duna', 'viaje', 'ninguna']
    matm = re.search(r'<body[^>]*data-atmosfera=["\']([^"\']*)', visible, re.I)
    if matm:
        nombre_atm = matm.group(1).strip()
        a.check('La atmosfera declarada existe', nombre_atm in ATMOSFERAS,
                'El body declara data-atmosfera="%s", que no es ninguna de las 8 del motor '
                '(%s). El deck saldria con fondo muerto.'
                % (nombre_atm, ', '.join(ATMOSFERAS)))
        tiene_motor = 'window.Atmosfera' in visible or 'global.Atmosfera' in visible
        a.check('El motor de atmosferas esta incrustado',
                nombre_atm == 'ninguna' or tiene_motor,
                'Se declara la atmosfera "%s" pero el motor no esta en el archivo. '
                'Correr scripts/incrustar_atmosferas.py sobre el deck.' % nombre_atm)
    else:
        a.sin_verificar('Atmosfera del deck',
                        'El body no declara data-atmosfera. El deck saldra sin fondo vivo, '
                        'que es valido solo si se eligio "ninguna" a proposito.')

    # ------------------------------------------------------------------
    # 6c · Clases usadas en el HTML que NO tienen ninguna regla CSS
    # ------------------------------------------------------------------
    # Reportado por el chat del Cartel el 2026-09-03: inyecto el CSS de sus
    # laminas con un `replace` cuyo ancla ya no existia. Fallo EN SILENCIO: el
    # HTML tenia las clases, el CSS no tenia ni una regla, y el verificador dio
    # 30 de 30. FER lo vio en pantalla: texto a 16px con la fuente del sistema
    # en una lamina vacia. Comprobarlo es baratisimo y lo habria cazado.
    css_todo = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', visible, re.S | re.I))
    clases_html = set()
    for attr in re.findall(r'class=["\']([^"\']+)["\']', cuerpo, re.I):
        for c in attr.split():
            if c and not c.startswith('GP_'):
                clases_html.add(c)
    # Clases que el motor aplica desde JS y por tanto no siempre estan en el HTML
    VIVEN_EN_JS = {'is-active', 'go', 'vista-general', 'presentador', 'con-logo'}
    huerfanas = sorted(
        c for c in clases_html
        if c not in VIVEN_EN_JS
        and not re.search(r'\.' + re.escape(c) + r'(?![\w-])', css_todo)
    )
    a.check('Toda clase usada tiene alguna regla CSS', not huerfanas,
            'Clases en el HTML sin ni una regla que las nombre: %s. Sintoma de CSS '
            'que no llego a entrar (un replace con el ancla equivocada falla en '
            'silencio). En pantalla se ve como texto sin estilo en una lamina vacia.'
            % ', '.join(huerfanas[:10]))

    # ------------------------------------------------------------------
    # 7 · Contraste real de la paleta declarada (WCAG AA = 4.5)
    # ------------------------------------------------------------------
    tokens = dict(re.findall(r'--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,6})\s*;', html))
    faltan = [t for t in ('ink', 'muted', 'surface', 'accent') if t not in tokens]

    if faltan:
        a.sin_verificar('Contraste de la paleta',
                        'Faltan tokens hex en :root (%s). No se pudo calcular.' % ', '.join(faltan))
    else:
        pares = [
            ('Texto principal sobre lamina', tokens['ink'], tokens['surface'], 4.5, True),
            ('Texto secundario sobre lamina', tokens['muted'], tokens['surface'], 4.5, False),
            ('Acento sobre lamina', tokens['accent'], tokens['surface'], 3.0, False),
        ]
        for nombre, fg, bg, minimo, grave in pares:
            r = contraste(fg, bg)
            if r is None:
                a.sin_verificar(nombre, 'Hex ilegible: %s sobre %s' % (fg, bg))
                continue
            a.check('%s (AA >= %.1f)' % (nombre, minimo), r >= minimo,
                    'Contraste medido %.2f:1 entre %s y %s. Minimo exigido %.1f:1. No se lee al fondo de la sala.'
                    % (r, fg, bg, minimo), grave=grave)

    # ------------------------------------------------------------------
    # 8 · Metadatos
    # ------------------------------------------------------------------
    mt = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    titulo = mt.group(1).strip() if mt else ''
    a.check('Tiene <title> con contenido real',
            bool(titulo) and not titulo.startswith('GP_'),
            'El <title> esta vacio o sin rellenar. Es el nombre de la pestana y del enlace compartido.')

    a.check('Tiene meta description',
            re.search(r'<meta\s+name=["\']description["\'][^>]*content=["\'](?!GP_)[^"\']{10,}',
                      html, re.I) is not None,
            'Falta meta description util: al compartir el enlace sale sin resumen.', grave=False)

    a.check('Declara idioma', re.search(r'<html[^>]+lang=', html, re.I) is not None,
            'Falta lang en <html>: los lectores de pantalla no saben en que idioma leer.', grave=False)

    # ------------------------------------------------------------------
    # 9 · Lo que este script NO puede verificar (se declara, no se calla)
    # ------------------------------------------------------------------
    a.sin_verificar('60fps del viaje de camara',
                    'Requiere abrir el deck en un navegador real y medir. Este script solo lee el archivo.')
    a.sin_verificar('Que los datos y citas sean ciertos',
                    'La veracidad del contenido no es automatizable. La verifica una persona contra la fuente.')
    a.sin_verificar('Render de acentos en pantalla',
                    'Se comprueba la codificacion del archivo, no el render. Hay que abrirlo y mirarlo.')

    return a, dict(laminas=n_lam, tam_kb=tam_kb, tildes=tildes, titulo=titulo)


# ----------------------------------------------------------------------
# Informe
# ----------------------------------------------------------------------

def informe(a, meta):
    L = []
    L.append('')
    L.append('COBERTURA DE VERIFICACION - Golden Presenta')
    L.append('Archivo: %s' % os.path.basename(a.ruta))
    L.append('Universo: %d laminas, %.1f KB, %d caracteres acentuados'
             % (meta['laminas'], meta['tam_kb'], meta['tildes']))
    L.append('Metodo: lectura estatica del HTML (no se abrio un navegador)')
    L.append('Comprobaciones corridas: %d' % a.corridas)
    L.append('   pasan: %d   fallan: %d   avisos: %d'
             % (len(a.ok), len(a.fallas), len(a.avisos)))
    L.append('')

    if a.fallas:
        L.append('FALLAS (%d) - no se entrega asi:' % len(a.fallas))
        for n, d in a.fallas:
            L.append('  [FALLA] %s' % n)
            L.append('          %s' % d)
        L.append('')

    if a.avisos:
        L.append('AVISOS (%d) - decision del autor:' % len(a.avisos))
        for n, d in a.avisos:
            L.append('  [AVISO] %s' % n)
            L.append('          %s' % d)
        L.append('')

    if a.no_verificado:
        L.append('NO VERIFICADO (%d) - fuera del alcance de este script:' % len(a.no_verificado))
        for q, p in a.no_verificado:
            L.append('  [ ? ] %s' % q)
            L.append('        %s' % p)
        L.append('')

    if not a.fallas:
        L.append('Resultado: %d de %d comprobaciones automatizables pasan, con %d aviso(s).'
                 % (len(a.ok), a.corridas, len(a.avisos)))
        L.append('Queda pendiente lo de la lista NO VERIFICADO: eso se comprueba abriendo el deck.')
    else:
        L.append('Resultado: %d falla(s) bloquean la entrega.' % len(a.fallas))
    L.append('')
    return '\n'.join(L)


def main():
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    como_json = '--json' in sys.argv

    if not args:
        print(__doc__)
        return 2

    ruta = args[0]
    if not os.path.isfile(ruta):
        print('No existe el archivo: %s' % ruta)
        return 2

    a, meta = auditar(ruta)

    if como_json:
        print(json.dumps({
            'archivo': ruta,
            'laminas': meta['laminas'],
            'corridas': a.corridas,
            'pasan': len(a.ok),
            'fallas': [{'check': n, 'detalle': d} for n, d in a.fallas],
            'avisos': [{'check': n, 'detalle': d} for n, d in a.avisos],
            'no_verificado': [{'que': q, 'porque': p} for q, p in a.no_verificado],
        }, ensure_ascii=False, indent=2))
    else:
        print(informe(a, meta))

    return 1 if a.fallas else 0


if __name__ == '__main__':
    sys.exit(main())
