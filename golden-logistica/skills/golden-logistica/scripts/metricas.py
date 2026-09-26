# -*- coding: utf-8 -*-
"""Metricas del Modo 2 de golden-logistica, con las leyes DENTRO del calculo.

POR QUE EXISTE ESTE FICHERO. Hasta GL1.4 las cuatro formulas del Modo 2 vivian en
prosa dentro del SKILL.md. Una regla que solo vive en prosa se aplica cuando el que
lee se acuerda, y el dia que no se acuerda el numero sale mal SIN QUE NADA FALLE.
Medido en la simulacion del 2026-09-09 sobre 10 guias: leer `entregados` como
substring en vez de igualdad exacta daba **20% de efectividad donde hay 10%**. Ese
numero alimenta el breakeven COD de `golden-ads`, asi que el error no se queda aqui.

LAS TRES LEYES QUE ESTE MODULO HACE CUMPLIR, y las tres son de error ya cometido:

1. `ENTREGADO A TRANSPORTADORA` NO ES `ENTREGADO`. Es entrega al courier, la plata
   no ha entrado. Se compara por IGUALDAD EXACTA sobre el estado normalizado, jamas
   por substring: un filtro `/entregad/` ya clasifico 3 ordenes como venta cobrada
   sin serlo. El modulo se NIEGA a contar por substring, no es opcional.

2. TODA CIFRA VIAJA CON SU VENTANA. Los dos barridos de efectividad de la casa usan
   ventanas distintas y no se cruzan. Aqui la ventana es un argumento OBLIGATORIO y
   sale impresa pegada al porcentaje: un porcentaje sin ventana se lee como si fuera
   de siempre.

3. UN CERO SE PRUEBA. Cuando una metrica da 0 se imprime sobre cuantas se calculo.
   "0 devoluciones" a secas puede ser una operacion sana o un export vacio, y son
   cosas contrarias.

Uso:
    python3 metricas.py --autoprueba
    from metricas import Metricas
"""
import unicodedata


def N(s):
    """Normaliza un estado: sin tildes, mayusculas, sin espacios de sobra."""
    s = unicodedata.normalize('NFD', str(s) if s is not None else '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return ' '.join(s.upper().split())


# IGUALDAD EXACTA. La lista es corta a proposito: cualquier estado que no este aqui
# NO es una entrega cobrada, y en la duda no se cuenta.
ENTREGA_COBRADA = {'ENTREGADO'}
# El impostor, con nombre propio para poder DECLARARLO en la salida.
IMPOSTOR = 'ENTREGADO A TRANSPORTADORA'
DEVOLUCION = {'DEVOLUCION'}
NOVEDAD = {'NOVEDAD'}


class Metricas(object):
    """Calcula el Modo 2 sobre una lista de dicts con 'estatus'.

    ventana: texto obligatorio que describe el periodo, p.ej. '2026-09-01 a 09-07'.
    despachos: denominador real del periodo. Si no se pasa, se usa len(filas) y se
    DECLARA que se uso, porque no es lo mismo y confundirlos infla la efectividad.
    """

    def __init__(self, filas, ventana, despachos=None, flete_ida=None, flete_retorno=None):
        if not ventana or not str(ventana).strip():
            raise ValueError(
                'ventana OBLIGATORIA: un porcentaje sin ventana no se puede comparar '
                'con nada y los dos barridos de la casa usan ventanas distintas')
        self.ventana = str(ventana).strip()
        self.filas = list(filas)
        self.estados = [N(f.get('estatus')) for f in self.filas]
        self.despachos = despachos if despachos is not None else len(self.filas)
        self.despachos_asumidos = despachos is None
        self.flete_ida = flete_ida
        self.flete_retorno = flete_retorno
        self.avisos = []
        if self.despachos_asumidos:
            self.avisos.append(
                'despachos del periodo NO declarados: se uso el tamano de la lista (%d). '
                'Si la lista es solo de novedades, la efectividad sale MAL' % len(self.filas))
        n_imp = self.estados.count(IMPOSTOR)
        if n_imp:
            self.avisos.append(
                '%d guias en %s: NO cuentan como venta (estan con el courier, la plata no entro)'
                % (n_imp, IMPOSTOR))

    # --- conteos, todos por igualdad exacta ---
    def _cuenta(self, conjunto):
        return sum(1 for e in self.estados if e in conjunto)

    @property
    def entregados(self):
        return self._cuenta(ENTREGA_COBRADA)

    @property
    def devoluciones(self):
        return self._cuenta(DEVOLUCION)

    @property
    def novedades(self):
        return self._cuenta(NOVEDAD)

    # --- metricas ---
    def efectividad(self):
        """ENTREGADO (exacto) / despachados del MISMO periodo."""
        return self._pct(self.entregados, self.despachos, 'efectividad de entrega')

    def tasa_novedad(self):
        return self._pct(self.novedades, self.despachos, 'tasa de novedad')

    def tasa_devolucion(self):
        return self._pct(self.devoluciones, self.despachos, 'tasa de devolucion')

    def flete_efectivo(self):
        """(despachos*ida + devoluciones*retorno) / entregas. El costo que manda."""
        if self.flete_ida is None or self.flete_retorno is None:
            return None, 'fletes no declarados: no se puede calcular el flete efectivo'
        if not self.entregados:
            return None, 'cero entregas en la ventana %s: el flete efectivo no existe' % self.ventana
        v = (self.despachos * self.flete_ida + self.devoluciones * self.flete_retorno) / float(self.entregados)
        return v, 'sobre %d entregas · ventana %s' % (self.entregados, self.ventana)

    def _pct(self, num, den, nombre):
        """Devuelve (pct, texto). El cero se PRUEBA: dice sobre cuantas se calculo."""
        if not den:
            return None, '%s: denominador CERO, no se puede calcular (ventana %s)' % (nombre, self.ventana)
        pct = 100.0 * num / den
        txt = '%s: %d de %d = %.1f%% · ventana %s' % (nombre, num, den, pct, self.ventana)
        if num == 0:
            txt += ' · CERO PROBADO sobre %d filas revisadas' % len(self.filas)
        return pct, txt

    def informe(self):
        lineas = ['MODO 2 · ventana %s · %d filas' % (self.ventana, len(self.filas))]
        for m in (self.efectividad, self.tasa_novedad, self.tasa_devolucion):
            lineas.append('  ' + m()[1])
        v, nota = self.flete_efectivo()
        lineas.append('  flete efectivo: %s · %s' % ('%.2f' % v if v is not None else 'n/d', nota))
        for a in self.avisos:
            lineas.append('  AVISO: ' + a)
        lineas.append('  Umbrales del SKILL.md son CRITERIO sin N ni fecha, no tasa medida.')
        return '\n'.join(lineas)


def autoprueba():
    """Nueve casos. Cada uno nacio de una forma concreta de dar mal el numero."""
    fl = []

    def chk(cond, msg):
        if not cond:
            fl.append(msg)

    base = [{'estatus': 'ENTREGADO'},
            {'estatus': 'ENTREGADO A TRANSPORTADORA'},
            {'estatus': 'Entregado a transportadora'},
            {'estatus': 'NOVEDAD'},
            {'estatus': 'DEVOLUCION'}]

    m = Metricas(base, ventana='prueba', despachos=10)

    # 1. EL CASO QUE ORIGINO TODO: el impostor no puede contar como entrega
    chk(m.entregados == 1, 'CONTO EL IMPOSTOR: entregados=%d, debe ser 1' % m.entregados)
    # 2. y no lo cuenta ni con tilde, ni en minusculas, ni con espacios raros
    chk(Metricas([{'estatus': ' entregado  a   transportadora '}],
                 ventana='p', despachos=1).entregados == 0,
        'la normalizacion dejo pasar el impostor escrito distinto')
    # 3. control en el otro sentido: un ENTREGADO raro SI se cuenta
    chk(Metricas([{'estatus': ' entregado '}], ventana='p', despachos=1).entregados == 1,
        'la normalizacion se comio un ENTREGADO legitimo')
    # 4. la efectividad usa el denominador declarado, no el largo de la lista
    chk(abs(m.efectividad()[0] - 10.0) < 1e-9,
        'efectividad %.2f, debe ser 10.0 (1 de 10)' % m.efectividad()[0])
    # 5. la ventana es obligatoria
    try:
        Metricas(base, ventana='')
        fl.append('acepto ventana vacia: un porcentaje sin ventana no se puede comparar')
    except ValueError:
        pass
    # 6. el cero se PRUEBA
    _, txt = Metricas([{'estatus': 'NOVEDAD'}], ventana='p', despachos=5).efectividad()
    chk('CERO PROBADO' in txt, 'un cero salio pelado, sin decir sobre cuantas: %s' % txt)
    # 7. denominador cero no revienta ni inventa
    v, txt = Metricas([], ventana='p', despachos=0).efectividad()
    chk(v is None and 'CERO' in txt.upper(), 'denominador cero mal manejado: %s' % txt)
    # 8. sin despachos declarados, lo DICE (no lo asume en silencio)
    chk(any('NO declarados' in a for a in Metricas(base, ventana='p').avisos),
        'asumio el denominador sin declararlo')
    # 9. flete efectivo sale mayor que el nominal cuando hay devoluciones
    mf = Metricas(base, ventana='p', despachos=10, flete_ida=8, flete_retorno=6.5)
    v, _ = mf.flete_efectivo()
    chk(v is not None and v > 8, 'flete efectivo %s no supera al nominal habiendo devoluciones' % v)
    return fl


if __name__ == '__main__':
    import sys
    if '--autoprueba' in sys.argv:
        f = autoprueba()
        print('AUTOPRUEBA metricas: %s' % ('OK, 9 de 9' if not f else 'FALLA'))
        for x in f:
            print('  🔴 ' + x)
        sys.exit(1 if f else 0)
    print(__doc__)
