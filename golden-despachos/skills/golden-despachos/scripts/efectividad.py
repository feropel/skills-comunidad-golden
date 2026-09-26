# -*- coding: utf-8 -*-
"""Efectividad de entrega con PROCEDENCIA declarada.

Una sola puerta para los dos scripts de decision. Resuelve en cascada
MUNICIPIO -> DEPARTAMENTO -> NACIONAL y devuelve SIEMPRE, junto al pct,
`muestra_envios` y `fuente_efectividad`.

TRES REGLAS DURAS, las tres nacidas de un error ya cometido:

1. SIN UMBRAL (orden de FER, 2026-08-16). Si el municipio tiene UN envio, ese
   es el dato: no se sustituye por el promedio departamental, que no describe
   ese sitio. La transparencia sustituye al umbral, por eso `muestra_envios`
   viaja pegado al numero y el informe lo imprime.

2. GUARDIA DE PROCEDENCIA. Un archivo de efectividad sin `_fuente` y sin
   `_nota` NO se usa en silencio. `EFECTIVIDAD-PLATAFORMA.json` vivio tres
   semanas dentro del calculo con Envia al 95,51% cuando la Torre madura da
   ~76-81%, y nadie lo vio porque el numero no traia de donde salia. Medir sin
   declarar de donde viene es como no medir.

3. `__NACIONAL__` ES DATO, NO METADATO. Empieza por guion bajo como las claves
   de metadatos, y filtrarlo por el prefijo deja la caida a nacional MUERTA en
   silencio: un departamento desconocido devolvia None y la transportadora
   quedaba fuera de las candidatas sin que nadie lo notara. Cazado en la
   autoprueba de este mismo archivo.
"""
import json, os, unicodedata, sys

def N(s):
    s = unicodedata.normalize('NFD', str(s) if s is not None else '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper().strip()

# Archivos candidatos, del mejor al peor. El primero que exista Y pase la
# guardia de procedencia es el que manda. EFECTIVIDAD-PLATAFORMA.json queda de
# ultimo a proposito: no declara fuente ni ventana, asi que la guardia lo
# rechaza y solo entra si alguien le agrega la procedencia.
CANDIDATOS_DEP = ['datos/T90-DEPARTAMENTO.json', 'datos/EFECTIVIDAD-PLATAFORMA.json']
CANDIDATOS_CIU = ['datos/EFECTIVIDAD-PLATAFORMA-CIUDAD.json']

NACIONAL = '__NACIONAL__'


def _procedencia(doc):
    """Devuelve (ok, etiqueta). Un doc sin _fuente ni _nota no es confiable."""
    if not isinstance(doc, dict):
        return False, 'no es un objeto'
    fuente = doc.get('_fuente') or doc.get('_nota')
    if not fuente:
        return False, 'sin _fuente ni _nota (no se sabe de donde salio)'
    return True, str(fuente)[:120]


class Efectividad:
    def __init__(self, D, avisar=None):
        """D: funcion que resuelve rutas dentro del cerebro de datos."""
        self.avisos = []
        self._avisar = avisar or self.avisos.append
        self.dep, self.fuente_dep = self._cargar(D, CANDIDATOS_DEP)
        self.ciu, self.fuente_ciu = self._cargar(D, CANDIDATOS_CIU)

    def _cargar(self, D, candidatos):
        for rel in candidatos:
            p = D(rel)
            if not os.path.exists(p):
                continue
            try:
                doc = json.load(open(p))
            except Exception as e:
                self._avisar('AVISO: %s no se pudo leer (%s)' % (rel, str(e)[:60]))
                continue
            ok, etiqueta = _procedencia(doc)
            if not ok:
                self._avisar('AVISO: %s se DESCARTA por procedencia — %s. '
                             'Un numero sin fuente no entra al calculo.' % (rel, etiqueta))
                continue
            datos = doc.get('datos', doc)
            tabla = {}
            for k, v in datos.items():
                # OJO: NACIONAL empieza por guion bajo pero es DATO, no metadato.
                if (k.startswith('_') and k != NACIONAL) or not isinstance(v, dict):
                    continue
                fila = {}
                for car, d in v.items():
                    if not isinstance(d, dict) or 'pct' not in d:
                        continue
                    n = d.get('envios')
                    if n is None:
                        n = d.get('muestra_envios')
                    fila[N(car)] = {'pct': float(d['pct']),
                                    'envios': int(n) if n is not None else None}
                if fila:
                    tabla[N(k)] = fila
            if tabla:
                return tabla, '%s (%s)' % (rel.split('/')[-1], etiqueta)
        return {}, None

    def nivel_disponible(self):
        return {'municipio': bool(self.ciu), 'departamento': bool(self.dep),
                'fuente_municipio': self.fuente_ciu, 'fuente_departamento': self.fuente_dep}

    def get(self, car, ciudad, depto):
        """dict(pct, muestra_envios, fuente_efectividad) o None.
        Cascada municipio -> departamento -> nacional, SIN umbral de muestra."""
        car, ciudad, depto = N(car), N(ciudad), N(depto)
        for tabla, clave, nivel in ((self.ciu, '%s|%s' % (depto, ciudad), 'municipio'),
                                    (self.dep, depto, 'departamento'),
                                    (self.dep, NACIONAL, 'nacional')):
            fila = tabla.get(clave)
            if fila and car in fila:
                d = fila[car]
                return {'pct': d['pct'], 'muestra_envios': d['envios'],
                        'fuente_efectividad': nivel}
        return None


def marca(fuente, muestra):
    """Sufijo corto para el informe: de donde salio y con cuanta muestra."""
    ini = {'municipio': 'mun', 'departamento': 'dep', 'nacional': 'nac'}.get(fuente, '?')
    return '%s/%s' % (ini, ('n=%s' % muestra) if muestra is not None else 'n?')


# --------------------------------------------------------------------------
# AUTOPRUEBA. Un validador que no se ha visto MORDER no vale: aqui se siembran
# los dos casos malos conocidos y se exige que fallen.
# --------------------------------------------------------------------------
def autoprueba():
    import tempfile, shutil
    fallos = []
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, 'datos'))
        D = lambda p: os.path.join(tmp, p)

        # Caso 1: archivo SIN procedencia -> la guardia lo debe rechazar
        json.dump({'CUNDINAMARCA': {'ENVIA': {'pct': 95.51, 'envios': 424466}}},
                  open(D('datos/EFECTIVIDAD-PLATAFORMA.json'), 'w'))
        ef = Efectividad(D)
        if ef.dep:
            fallos.append('la guardia NO mordio: uso un archivo sin _fuente')
        if not any('DESCARTA por procedencia' in a for a in ef.avisos):
            fallos.append('la guardia no aviso del descarte')

        # Caso 2: con procedencia -> entra, y la caida a NACIONAL funciona
        json.dump({'_fuente': 'prueba sembrada',
                   'datos': {NACIONAL: {'ENVIA': {'pct': 81.09, 'envios': 1337159}},
                             'VALLE': {'VELOCES': {'pct': 83.27, 'envios': 27704}}}},
                  open(D('datos/T90-DEPARTAMENTO.json'), 'w'))
        json.dump({'_fuente': 'prueba sembrada',
                   'datos': {'ANTIOQUIA|BELLO': {'COORDINADORA': {'pct': 85, 'envios': 4097}}}},
                  open(D('datos/EFECTIVIDAD-PLATAFORMA-CIUDAD.json'), 'w'))
        ef = Efectividad(D)
        pruebas = [
            (('COORDINADORA', 'BELLO', 'ANTIOQUIA'), 'municipio', 4097),
            (('VELOCES', 'CIUDAD-INEXISTENTE', 'VALLE'), 'departamento', 27704),
            (('ENVIA', 'X', 'DEPTO-INEXISTENTE'), 'nacional', 1337159),
        ]
        for args, nivel, muestra in pruebas:
            r = ef.get(*args)
            if not r:
                fallos.append('%s devolvio None, se esperaba nivel %s' % (args[0], nivel)); continue
            if r['fuente_efectividad'] != nivel:
                fallos.append('%s salio de %s, se esperaba %s' % (args[0], r['fuente_efectividad'], nivel))
            if r['muestra_envios'] != muestra:
                fallos.append('%s trajo muestra %s, se esperaba %s' % (args[0], r['muestra_envios'], muestra))

        # Caso 3: SIN UMBRAL — un municipio de 1 envio manda sobre el departamento
        json.dump({'_fuente': 'prueba sembrada',
                   'datos': {'VALLE|PUEBLITO': {'VELOCES': {'pct': 100.0, 'envios': 1}}}},
                  open(D('datos/EFECTIVIDAD-PLATAFORMA-CIUDAD.json'), 'w'))
        ef = Efectividad(D)
        r = ef.get('VELOCES', 'PUEBLITO', 'VALLE')
        if not r or r['fuente_efectividad'] != 'municipio' or r['muestra_envios'] != 1:
            fallos.append('el umbral revivio: un municipio de 1 envio no mando')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fallos


if __name__ == '__main__':
    if '--autoprueba' in sys.argv:
        f = autoprueba()
        print('AUTOPRUEBA: %s' % ('OK, 6 de 6' if not f else 'FALLA'))
        for x in f:
            print('  🔴 ' + x)
        sys.exit(1 if f else 0)
    DATA = os.environ.get('DROPI_DATA') or os.path.expanduser('~/DROPI-LOGISTICA')
    D = lambda p: os.path.join(DATA, p)
    ef = Efectividad(D)
    for a in ef.avisos:
        print(a)
    print('niveles:', ef.nivel_disponible())
    for car, ciu, dep in [('COORDINADORA', 'BELLO', 'ANTIOQUIA'),
                          ('ENVIA', 'BOGOTA', 'CUNDINAMARCA'),
                          ('VELOCES', 'CIUDAD-QUE-NO-EXISTE', 'VALLE'),
                          ('ENVIA', 'X', 'DEPTO-QUE-NO-EXISTE')]:
        print('  %-14s %-22s %-14s -> %s' % (car, ciu, dep, ef.get(car, ciu, dep)))
