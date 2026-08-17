# -*- coding: utf-8 -*-
"""Detecta pedidos duplicados: mismo cliente pidiendo dos veces lo mismo."""
import collections, re, unicodedata, datetime, json, sys
try:
    import openpyxl
except ModuleNotFoundError:
    sys.exit('Falta openpyxl (lee los .xlsx de Dropi). Instalar una vez:  pip3 install openpyxl')
def N(s):
    s=unicodedata.normalize('NFD',str(s) if s is not None else '')
    return ''.join(c for c in s if unicodedata.category(c)!='Mn').upper().strip()
import glob, os
XL = sys.argv[1] if len(sys.argv)>1 else os.environ.get('DROPI_ORDENES')
if not XL:
    _c=[x for x in sorted(glob.glob(os.path.expanduser('~/Desktop/ordenes_*.xlsx'))) if 'productos' not in os.path.basename(x)]
    XL=_c[-1] if _c else None
if not XL:
    sys.exit("Falta el export de Dropi. Uso: python3 duplicados.py <ordenes.xlsx>")
wb=openpyxl.load_workbook(XL,read_only=True,data_only=True); ws=wb.active
rows=list(ws.iter_rows(values_only=True)); H={c:i for i,c in enumerate(rows[0])}; data=rows[1:]; wb.close()
f=lambda r,k: r[H[k]]
tel=lambda r: re.sub(r'\D','',str(f(r,'TELÉFONO') or ''))
def fch(r):
    try: return datetime.datetime.strptime(str(f(r,'FECHA')),'%d-%m-%Y').date()
    except: return None
PEND={'PENDIENTE','PENDIENTE CONFIRMACION'}
MUERTO={'CANCELADO','RECHAZADO','GUIA_ANULADA'}

def firma(r):
    """clave de identidad del cliente: telefono, o nombre+ciudad si no hay telefono"""
    t=tel(r)
    return t if t else re.sub(r'[^A-Z]','',N(f(r,'NOMBRE CLIENTE')))[:14]+'@'+N(f(r,'CIUDAD DESTINO'))

g=collections.defaultdict(list)
for r in data: g[firma(r)].append(r)

alertas=[]
for k,rs in g.items():
    pend=[r for r in rs if f(r,'ESTATUS') in PEND]
    if not pend: continue
    vivos=[r for r in rs if f(r,'ESTATUS') not in MUERTO]
    for p in pend:
        fp=fch(p); vp=float(f(p,'VALOR DE COMPRA EN PRODUCTOS') or 0)
        for o in vivos:
            if o is p: continue
            if f(o,'ID')==f(p,'ID'): continue
            fo=fch(o)
            dias=abs((fp-fo).days) if (fp and fo) else 999
            vo=float(f(o,'VALOR DE COMPRA EN PRODUCTOS') or 0)
            similar = vp>0 and vo>0 and abs(vp-vo)/max(vp,vo)<=0.10
            mismaCiudad = N(f(p,'CIUDAD DESTINO'))==N(f(o,'CIUDAD DESTINO'))
            if not mismaCiudad: continue
            if f(o,'ESTATUS') in PEND and dias<=3:
                nivel,por='CRITICO','dos pedidos sin despachar, %d dia(s) de diferencia'%dias
            elif dias<=15 and similar:
                nivel,por='ALTO','el otro ya va en camino o llego, %d dias antes y por practicamente el mismo valor'%dias
            elif dias<=15:
                nivel,por='MEDIO','otro pedido activo %d dias antes, valor distinto'%dias
            elif dias<=45 and similar:
                nivel,por='VIGILAR','recompra a los %d dias por el mismo valor'%dias
            else: continue
            alertas.append(dict(nivel=nivel, por=por, tel=tel(p), cliente=str(f(p,'NOMBRE CLIENTE')),
                ciudad=str(f(p,'CIUDAD DESTINO')),
                pendiente=dict(id=f(p,'ID'),fecha=str(f(p,'FECHA')),estatus=f(p,'ESTATUS'),valor=vp,dir=str(f(p,'DIRECCION')).replace('\n',' ')),
                otro=dict(id=f(o,'ID'),fecha=str(f(o,'FECHA')),estatus=f(o,'ESTATUS'),valor=vo,dir=str(f(o,'DIRECCION')).replace('\n',' '))))
orden={'CRITICO':0,'ALTO':1,'MEDIO':2,'VIGILAR':3}
alertas.sort(key=lambda a:orden[a['nivel']])
# la salida cae en DROPI-LOGISTICA/salidas si el cerebro esta a mano; si no, en la carpeta actual
_dl=os.path.join(os.environ.get('DROPI_DATA') or os.path.expanduser('~/DROPI-LOGISTICA'),'salidas')
_out=os.path.join(_dl,'DUPLICADOS.json') if os.path.isdir(_dl) else 'DUPLICADOS.json'
json.dump(alertas,open(_out,'w'),ensure_ascii=False,indent=1)
print('escrito:',_out)
p=lambda n:'$'+format(int(n),',d').replace(',','.')
if not alertas: print('sin duplicados')
for a in alertas:
    print('%-8s %-13s %-26s %s'%(a['nivel'],a['tel'],a['cliente'][:25],a['ciudad']))
    print('        motivo: '+a['por'])
    print('        PENDIENTE  %-10s %-11s %-22s %s'%(a['pendiente']['id'],a['pendiente']['fecha'],a['pendiente']['estatus'],p(a['pendiente']['valor'])))
    print('        el otro    %-10s %-11s %-22s %s'%(a['otro']['id'],a['otro']['fecha'],a['otro']['estatus'],p(a['otro']['valor'])))
print()
print('total alertas:',len(alertas))
