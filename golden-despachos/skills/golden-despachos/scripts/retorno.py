# -*- coding: utf-8 -*-
"""Costo de retorno por transportadora: UNA puerta, y ninguna exclusion callada.

LEY DE NO-HEREDAR: los parametros son de ESTA empresa, con SU mix de ciudades. Se
prefiere COSTO-RETORNO-<NEGOCIO>.json (variable DROPI_NEGOCIO) y solo se cae al
generico si no se pudo usar el del negocio.

P59 (Centro de Mando): una herramienta que DESCARTA datos del usuario tiene que
CONTARLOS y NOMBRARLOS. Antes este bloque vivia duplicado en calificar.py y
decidir_vivo.py con un `except Exception: continue`, asi que un archivo del
negocio que existia y estaba roto caia al generico **sin decirlo** y rompia la
ley de no-heredar en silencio. Cuatro de las diez exclusiones silenciosas de la
skill salian de aqui.

Trampa 5: solo entra la fraccion con confianza alta o media; el resto asume 1.00
(conservador). Un caso suelto en $0 NO es "no cobra retorno": ya produjo cuatro
recomendaciones equivocadas. Pero esa exclusion tambien se NOMBRA.

    python3 retorno.py --autoprueba
"""
import json, os, sys, unicodedata

RET_DEF = 1.00
CONFIABLES = ('alta', 'media')
# ultimo medido conocido, por si no hay ningun archivo legible
ULTIMO_CONOCIDO = {'INTERRAPIDISIMO': 1.00, 'ENVIA': 0.72}


def N(s):
    s = unicodedata.normalize('NFD', str(s) if s is not None else '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper().strip()


def cargar(D, negocio=None):
    """Devuelve (fracciones, fuente, avisos, baja_confianza).

    `D` es la funcion que resuelve rutas dentro del cerebro de datos.
    `avisos` va SIEMPRE al informe: es la lista de lo que se descarto y por que.
    """
    neg = (negocio if negocio is not None else os.environ.get('DROPI_NEGOCIO') or '').strip().upper()
    cands = ([('negocio', 'datos/COSTO-RETORNO-%s.json' % neg)] if neg else []) \
        + [('generico', 'datos/COSTO-RETORNO.json')]
    avisos = []
    for etiqueta, rel in cands:
        nombre = rel.split('/')[-1]
        try:
            doc = json.load(open(D(rel)))
        except FileNotFoundError:
            # que el del negocio no exista es normal la primera vez; se dice, no se calla
            if etiqueta == 'negocio':
                avisos.append('%s no existe: se busca el generico' % nombre)
            continue
        except Exception as e:
            # ESTA es la que rompia la ley en silencio: el archivo del negocio
            # existe, esta roto, y antes se caia al generico sin una palabra.
            avisos.append('%s EXISTE pero no se pudo leer (%s: %s): no se aplica el costo de '
                          'retorno de este negocio' % (nombre, type(e).__name__, e))
            continue
        claves = [k for k in doc if k.startswith('medido')]
        if not claves:
            avisos.append('%s no trae bloque medido*: no se puede usar' % nombre)
            continue
        med = doc[sorted(claves)[-1]]
        fracciones, baja = {}, []
        for k, v in med.items():
            if not isinstance(v, dict) or 'fraccion' not in v:
                continue
            conf = str(v.get('confianza', '')).lower()
            if conf in CONFIABLES:
                fracciones[N(k)] = v['fraccion']
            else:
                baja.append('%s (confianza %s)' % (N(k), conf or 'sin declarar'))
        if baja:
            # trampa 5 aplicada, pero declarada: estas asumen 1.00
            avisos.append('%d transportadoras fuera del costo medido por confianza baja, asumen '
                          '%.2f: %s' % (len(baja), RET_DEF, ', '.join(sorted(baja))))
        if not fracciones:
            avisos.append('%s no dejo ninguna fraccion utilizable: TODAS asumen %.2f'
                          % (nombre, RET_DEF))
        return fracciones, nombre, avisos, baja
    avisos.append('sin ningun COSTO-RETORNO utilizable en datos/: se usa el ultimo medido conocido')
    return dict(ULTIMO_CONOCIDO), '(sin archivo: ultimo medido conocido)', avisos, []


def imprime_avisos(avisos, fuente, salida=None):
    """El informe declara la fuente Y lo que quedo fuera. Nunca solo la fuente."""
    f = salida or sys.stderr
    print('fuente de costo de retorno:', fuente, file=f)
    for a in avisos:
        print('  AVISO retorno:', a, file=f)


# --------------------------------------------------------------------- banco
def autoprueba():
    import tempfile, shutil
    raiz = tempfile.mkdtemp()
    os.makedirs(os.path.join(raiz, 'datos'))

    def D(rel):
        return os.path.join(raiz, rel)

    def escribe(nombre, texto):
        with open(os.path.join(raiz, 'datos', nombre), 'w') as fh:
            fh.write(texto)

    bueno = json.dumps({'medido-2026-08': {
        'ENVIA': {'fraccion': 0.72, 'confianza': 'alta'},
        'INTERRAPIDISIMO': {'fraccion': 1.00, 'confianza': 'media'}}})
    mal = 0

    def caso(nombre, cond, detalle=''):
        nonlocal mal
        if not cond:
            mal += 1
            print('  🔴 %s %s' % (nombre, detalle))

    # 1. el del negocio manda cuando esta sano, y no inventa avisos de alarma
    escribe('COSTO-RETORNO-GOLDEN.json', bueno)
    escribe('COSTO-RETORNO.json', json.dumps({'medido-2026-01': {
        'ENVIA': {'fraccion': 0.10, 'confianza': 'alta'}}}))
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('negocio sano manda', f == 'COSTO-RETORNO-GOLDEN.json' and r.get('ENVIA') == 0.72, f)
    caso('negocio sano no deja avisos', av == [], str(av))

    # 2. el del negocio EXISTE y esta ROTO: cae al generico PERO lo dice (P59)
    escribe('COSTO-RETORNO-GOLDEN.json', '{ esto no es json')
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('roto cae al generico', f == 'COSTO-RETORNO.json' and r.get('ENVIA') == 0.10, f)
    caso('roto se NOMBRA', any('EXISTE pero no se pudo leer' in a for a in av), str(av))

    # 3. el del negocio sin bloque medido*: cae al generico y lo dice
    escribe('COSTO-RETORNO-GOLDEN.json', json.dumps({'notas': 'pendiente de medir'}))
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('sin medido cae al generico', f == 'COSTO-RETORNO.json', f)
    caso('sin medido se NOMBRA', any('no trae bloque medido' in a for a in av), str(av))

    # 4. confianza baja: se excluye (trampa 5) pero se NOMBRA, no desaparece
    escribe('COSTO-RETORNO-GOLDEN.json', json.dumps({'medido-2026-08': {
        'ENVIA': {'fraccion': 0.72, 'confianza': 'alta'},
        'VELOCES': {'fraccion': 0.0, 'confianza': 'baja'}}}))
    r, f, av, baja = cargar(D, 'GOLDEN')
    caso('confianza baja fuera del calculo', 'VELOCES' not in r, str(r))
    caso('confianza baja se NOMBRA', any('VELOCES' in a and 'confianza baja' in a for a in av), str(av))
    caso('confianza baja se devuelve contada', len(baja) == 1, str(baja))

    # 5. TODAS en confianza baja: RET vacio, y se avisa que todas asumen 1.00
    escribe('COSTO-RETORNO-GOLDEN.json', json.dumps({'medido-2026-08': {
        'VELOCES': {'fraccion': 0.0, 'confianza': 'baja'}}}))
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('todas baja deja RET vacio', r == {}, str(r))
    caso('todas baja se NOMBRA', any('TODAS asumen' in a for a in av), str(av))

    # 6. sin negocio declarado: usa el generico y NO se queja del que no pidio
    r, f, av, _ = cargar(D, '')
    caso('sin negocio usa generico', f == 'COSTO-RETORNO.json', f)
    caso('sin negocio no inventa aviso de negocio',
         not any('COSTO-RETORNO-' in a for a in av), str(av))

    # 7. el del negocio NO existe: se dice, y se cae al generico
    os.remove(os.path.join(raiz, 'datos', 'COSTO-RETORNO-GOLDEN.json'))
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('negocio ausente cae al generico', f == 'COSTO-RETORNO.json', f)
    caso('negocio ausente se NOMBRA', any('no existe' in a for a in av), str(av))

    # 8. ningun archivo: ultimo medido conocido, declarado
    os.remove(os.path.join(raiz, 'datos', 'COSTO-RETORNO.json'))
    r, f, av, _ = cargar(D, 'GOLDEN')
    caso('sin archivos usa el ultimo conocido', r == ULTIMO_CONOCIDO, str(r))
    caso('sin archivos lo declara', any('ultimo medido conocido' in a for a in av), str(av))

    shutil.rmtree(raiz)
    total = 17
    print('AUTOPRUEBA retorno: %s, %d de %d' % ('OK' if not mal else 'FALLA', total - mal, total))
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(autoprueba() if '--autoprueba' in sys.argv else
             print('Uso: python3 retorno.py --autoprueba') or 0)
