# -*- coding: utf-8 -*-
"""Detecta pedidos duplicados y ORDENES FANTASMA del mismo cliente.

TRES LEYES DE IDENTIDAD, las tres de errores ya cometidos y medidos:

1. LA CLAVE ES (TELEFONO, ID DE ORDEN), nunca el telefono solo. Un mismo
   telefono tiene un ID por cada pedido; filtrar por cliente borraria del radar
   a un comprador recurrente con una orden nueva viva.

2. EDITAR UNA ORDEN LE CAMBIA EL ID. La version vieja desaparece del panel pero
   sobrevive en un export ya descargado, y entonces la MISMA venta aparece dos
   veces: mismo telefono, mismo monto, una atrasada y otra mas avanzada con id
   mayor. Eso NO es un cliente pidiendo dos veces, es un fantasma. Marcarlo como
   duplicado manda a preguntarle al cliente por un pedido que no hizo.
   Discriminador AUTORITATIVO (probado): `GET /integrations/orders/myorders/{id}`
   sobre la vieja devuelve `isSuccess:false, "Orden no encontrada"`, mientras que
   una orden real, incluso CANCELADA, responde `isSuccess:true`. El listado tiene
   fantasmas; el detalle no miente. Aqui se marca la SOSPECHA; confirmarla pide
   esa consulta.

3. CUATRO ESTADOS TERMINALES: ENTREGADO, DEVOLUCION, CANCELADO, RECHAZADO. Y
   `ENTREGADO A TRANSPORTADORA` NO es ENTREGADO: es entrega al courier, la plata
   no ha entrado. Por eso se compara por IGUALDAD EXACTA, jamas por substring
   (un `/entregad/` clasifico 3 ordenes como venta cobrada sin serlo).
   Terminal no es lo mismo que ignorable: una orden ENTREGADA es justamente la
   evidencia de que el cliente ya recibio, asi que cuenta para detectar la
   recompra. Los ANULADOS (cancelado, rechazado, guia anulada) si se excluyen:
   no son un pedido que exista.
"""
import collections, re, unicodedata, datetime, json, sys, glob, os

def N(s):
    s = unicodedata.normalize('NFD', str(s) if s is not None else '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper().strip()

PEND = {'PENDIENTE', 'PENDIENTE CONFIRMACION'}
ANULADOS = {'CANCELADO', 'RECHAZADO', 'GUIA_ANULADA'}
TERMINALES = {'ENTREGADO', 'DEVOLUCION', 'CANCELADO', 'RECHAZADO'}
# Avance logistico, para saber cual de dos ordenes va MAS adelante.
AVANCE = {'PENDIENTE CONFIRMACION': 0, 'PENDIENTE': 1, 'GENERANDO_GUIA': 2,
          'GUIA_GENERADA': 3, 'PREPARADO PARA TRANSPORTADORA': 4,
          'ENTREGADO A TRANSPORTADORA': 5, 'DESPACHADA': 5, 'EN TRANSITO': 6,
          'EN REPARTO': 7, 'NOVEDAD': 7, 'ENTREGADO': 9, 'DEVOLUCION': 9}


def clasificar(pend, otro, dias, similar):
    """(nivel, motivo) o None. pend/otro son (id, estatus, valor)."""
    pid, pest, _ = pend
    oid, oest, _ = otro
    # FANTASMA: mismo valor, la vieja mas atrasada y con id MENOR que la avanzada
    if similar and dias <= 3:
        try:
            menor = int(pid) < int(oid)
        except (TypeError, ValueError):
            menor = None
        if menor is not None:
            av_p, av_o = AVANCE.get(pest, 1), AVANCE.get(oest, 1)
            if menor and av_p < av_o:
                return ('EDICION', 'sospecha de orden FANTASMA: mismo valor, esta tiene id MENOR '
                        'y va mas atrasada que la %s. Editar una orden le cambia el id. '
                        'Confirmar con GET /integrations/orders/myorders/%s: si responde '
                        '"Orden no encontrada", esta ya no existe y no se despacha.' % (oid, pid))
    if oest in PEND and dias <= 3:
        return ('CRITICO', 'dos pedidos sin despachar, %d dia(s) de diferencia' % dias)
    if dias <= 15 and similar:
        cerrado = ' (ese ya cerro: %s)' % oest if oest in TERMINALES else ''
        return ('ALTO', 'el otro ya va en camino o llego, %d dias antes y por practicamente '
                        'el mismo valor%s' % (dias, cerrado))
    if dias <= 15:
        return ('MEDIO', 'otro pedido activo %d dias antes, valor distinto' % dias)
    if dias <= 45 and similar:
        return ('VIGILAR', 'recompra a los %d dias por el mismo valor' % dias)
    return None


def analizar(filas):
    """filas: dicts con id, estatus, tel, ciudad, valor, fecha (date o None),
    nombre, direccion. Devuelve la lista de alertas ordenada por gravedad."""
    def firma(r):
        t = re.sub(r'\D', '', str(r.get('tel') or ''))
        return t if t else re.sub(r'[^A-Z]', '', N(r.get('nombre')))[:14] + '@' + N(r.get('ciudad'))

    g = collections.defaultdict(list)
    for r in filas:
        g[firma(r)].append(r)

    alertas = []
    for _, rs in g.items():
        pend = [r for r in rs if r['estatus'] in PEND]
        if not pend:
            continue
        vivos = [r for r in rs if r['estatus'] not in ANULADOS]
        for p in pend:
            vp = float(p.get('valor') or 0)
            for o in vivos:
                if o is p or str(o['id']) == str(p['id']):
                    continue               # la clave es (tel, ID de orden)
                if N(o.get('ciudad')) != N(p.get('ciudad')):
                    continue
                fp, fo = p.get('fecha'), o.get('fecha')
                dias = abs((fp - fo).days) if (fp and fo) else 999
                vo = float(o.get('valor') or 0)
                similar = vp > 0 and vo > 0 and abs(vp - vo) / max(vp, vo) <= 0.10
                r = clasificar((p['id'], p['estatus'], vp), (o['id'], o['estatus'], vo), dias, similar)
                if not r:
                    continue
                nivel, motivo = r
                alertas.append(dict(nivel=nivel, por=motivo,
                    tel=re.sub(r'\D', '', str(p.get('tel') or '')),
                    cliente=str(p.get('nombre')), ciudad=str(p.get('ciudad')),
                    pendiente=dict(id=p['id'], fecha=str(p.get('fecha')), estatus=p['estatus'],
                                   valor=vp, dir=str(p.get('direccion') or '').replace('\n', ' ')),
                    otro=dict(id=o['id'], fecha=str(o.get('fecha')), estatus=o['estatus'],
                              valor=vo, dir=str(o.get('direccion') or '').replace('\n', ' '))))
    orden = {'EDICION': 0, 'CRITICO': 1, 'ALTO': 2, 'MEDIO': 3, 'VIGILAR': 4}
    alertas.sort(key=lambda a: orden[a['nivel']])
    return alertas


# --------------------------------------------------------------------------
# AUTOPRUEBA. Un cero se PRUEBA, no se cree: se siembran casos que DEBEN salir
# y casos que NO deben salir, y el banco falla si el detector se come alguno.
# --------------------------------------------------------------------------
def autoprueba():
    d = datetime.date(2026, 8, 1)
    def f(i, est, tel, val, dia, ciu='BOGOTA', nom='Cliente X'):
        return dict(id=i, estatus=est, tel=tel, ciudad=ciu, valor=val,
                    fecha=d + datetime.timedelta(days=dia), nombre=nom, direccion='CL 1 # 2-3')
    fallos = []

    def nivel_de(filas, pid):
        return next((a['nivel'] for a in analizar(filas) if str(a['pendiente']['id']) == str(pid)), None)

    # 1. FANTASMA: id menor + mas atrasada + mismo valor -> EDICION, no CRITICO
    r = nivel_de([f('100', 'PENDIENTE CONFIRMACION', '3001', 118704, 0),
                  f('200', 'ENTREGADO', '3001', 118704, 1)], '100')
    if r != 'EDICION':
        fallos.append('fantasma no detectado: salio %s, se esperaba EDICION' % r)

    # 2. DUPLICADO REAL: dos pendientes mismo dia, ninguna mas avanzada -> CRITICO
    r = nivel_de([f('300', 'PENDIENTE', '3002', 90000, 0),
                  f('301', 'PENDIENTE', '3002', 90000, 0)], '300')
    if r != 'CRITICO':
        fallos.append('duplicado real no detectado: salio %s, se esperaba CRITICO' % r)

    # 3. RECOMPRA tras entrega (caso Niurka): entregado y vuelve a pedir a los 3 dias
    r = nivel_de([f('500', 'ENTREGADO', '3003', 118704, 0),
                  f('600', 'PENDIENTE', '3003', 118700, 3)], '600')
    if r != 'ALTO':
        fallos.append('recompra tras entrega no detectada: salio %s, se esperaba ALTO' % r)

    # 4. NO debe saltar: ciudades distintas
    if analizar([f('700', 'PENDIENTE', '3004', 90000, 0),
                 f('701', 'PENDIENTE', '3004', 90000, 0, ciu='CALI')]):
        fallos.append('falso positivo: dos ciudades distintas no son duplicado')

    # 5. NO debe saltar: la otra esta ANULADA (no es un pedido que exista)
    if analizar([f('800', 'PENDIENTE', '3005', 90000, 0),
                 f('801', 'CANCELADO', '3005', 90000, 0)]):
        fallos.append('falso positivo: una orden CANCELADA no es un pedido vivo')

    # 6. ENTREGADO A TRANSPORTADORA no es ENTREGADO (no es venta, es el courier)
    if 'ENTREGADO A TRANSPORTADORA' in TERMINALES:
        fallos.append('ENTREGADO A TRANSPORTADORA quedo como terminal: es entrega al courier')
    a = analizar([f('900', 'PENDIENTE', '3006', 90000, 0),
                  f('901', 'ENTREGADO A TRANSPORTADORA', '3006', 90000, 1)])
    if a and '(ese ya cerro' in a[0]['por']:
        fallos.append('ENTREGADO A TRANSPORTADORA se reporto como cerrado')

    # 7. El mismo ID no se compara consigo mismo
    if analizar([f('950', 'PENDIENTE', '3007', 90000, 0)]):
        fallos.append('una sola orden genero alerta contra si misma')

    return fallos


def _cargar_export(XL):
    try:
        import openpyxl
    except ModuleNotFoundError:
        sys.exit('Falta openpyxl (lee los .xlsx de Dropi). Instalar una vez:  pip3 install openpyxl')
    wb = openpyxl.load_workbook(XL, read_only=True, data_only=True); ws = wb.active
    rows = list(ws.iter_rows(values_only=True)); H = {c: i for i, c in enumerate(rows[0])}
    out = []
    for r in rows[1:]:
        try:
            fecha = datetime.datetime.strptime(str(r[H['FECHA']]), '%d-%m-%Y').date()
        except Exception:
            fecha = None
        out.append(dict(id=r[H['ID']], estatus=r[H['ESTATUS']], tel=r[H['TELÉFONO']],
                        ciudad=r[H['CIUDAD DESTINO']], valor=r[H['VALOR DE COMPRA EN PRODUCTOS']],
                        fecha=fecha, nombre=r[H['NOMBRE CLIENTE']], direccion=r[H['DIRECCION']]))
    wb.close()
    return out


if __name__ == '__main__':
    if '--autoprueba' in sys.argv:
        fl = autoprueba()
        print('AUTOPRUEBA duplicados: %s' % ('OK, 7 de 7' if not fl else 'FALLA'))
        for x in fl:
            print('  🔴 ' + x)
        sys.exit(1 if fl else 0)

    XL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('DROPI_ORDENES')
    if not XL:
        c = [x for x in sorted(glob.glob(os.path.expanduser('~/Desktop/ordenes_*.xlsx')))
             if 'productos' not in os.path.basename(x)]
        XL = c[-1] if c else None
    if not XL:
        sys.exit('Falta el export de Dropi. Uso: python3 duplicados.py <ordenes.xlsx>')

    filas = _cargar_export(XL)
    alertas = analizar(filas)
    _dl = os.path.join(os.environ.get('DROPI_DATA') or os.path.expanduser('~/DROPI-LOGISTICA'), 'salidas')
    _out = os.path.join(_dl, 'DUPLICADOS.json') if os.path.isdir(_dl) else 'DUPLICADOS.json'
    json.dump(alertas, open(_out, 'w'), ensure_ascii=False, indent=1)
    print('escrito:', _out)
    p = lambda n: '$' + format(int(n), ',d').replace(',', '.')
    # Un cero se PRUEBA: se dice sobre cuantas ordenes se busco, no un "sin duplicados" pelado.
    pend = sum(1 for r in filas if r['estatus'] in PEND)
    if not alertas:
        print('0 alertas sobre %d ordenes (%d de ellas pendientes). '
              'El detector se prueba con: python3 duplicados.py --autoprueba' % (len(filas), pend))
    for a in alertas:
        print('%-8s %-13s %-26s %s' % (a['nivel'], a['tel'], a['cliente'][:25], a['ciudad']))
        print('        motivo: ' + a['por'])
        print('        PENDIENTE  %-10s %-11s %-22s %s' % (a['pendiente']['id'], a['pendiente']['fecha'],
                                                           a['pendiente']['estatus'], p(a['pendiente']['valor'])))
        print('        el otro    %-10s %-11s %-22s %s' % (a['otro']['id'], a['otro']['fecha'],
                                                           a['otro']['estatus'], p(a['otro']['valor'])))
    print()
    print('total alertas: %d  ·  universo: %d ordenes, %d pendientes' % (len(alertas), len(filas), pend))
