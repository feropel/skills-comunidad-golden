# -*- coding: utf-8 -*-
"""Decision final con cotizacion EN VIVO + huella del cliente por transportadora + vetos de la bodega (RECHAZOS-FULFILLMENT.json)."""
import json, unicodedata, os, sys
DATA = os.environ.get("DROPI_DATA") or os.path.expanduser("~/DROPI-LOGISTICA")
if not os.path.isdir(os.path.join(DATA, 'datos')):
    sys.exit('No encuentro el cerebro de datos en %s.\n'
             'Apunta DROPI_DATA a tu carpeta DROPI-LOGISTICA:\n'
             '  export DROPI_DATA="/ruta/a/DROPI-LOGISTICA"' % DATA)
def D(p): return os.path.join(DATA, p)
def huellas_recientes():
    import glob
    f=sorted(glob.glob(D('datos/huellas/*.psv')))
    if not f: raise SystemExit('No hay huellas capturadas en datos/huellas/. Corre primero la cosecha del panel.')
    return f[-1]


def N(s):
    s=unicodedata.normalize('NFD',str(s));return ''.join(c for c in s if unicodedata.category(c)!='Mn').upper().strip()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from efectividad import Efectividad, marca
EFEC = Efectividad(D)
for _a in EFEC.avisos:
    print(_a, file=sys.stderr)
if not EFEC.dep and not EFEC.ciu:
    sys.exit('No hay NINGUNA fuente de efectividad con procedencia declarada en datos/.')
try:
    Q=json.load(open(D('datos/COTIZACIONES-VIVO.json')))
except Exception:
    sys.exit('Falta datos/COTIZACIONES-VIVO.json (las cotizaciones en vivo del Paso 5). '
             'Sin ellas este script no tiene con qué re-decidir: registrarlas primero.')
try:
    R=json.load(open(D('datos/RECHAZOS-FULFILLMENT.json')))['rechazos']
except Exception:
    R=[]
    print('AVISO: sin RECHAZOS-FULFILLMENT.json — no se puede filtrar por veto de bodega; verificar a mano', file=sys.stderr)
VET_C={(N(r['transportadora']),N(r['ciudad']),N(r['departamento'])) for r in R if r['alcance']=='CIUDAD'}
VET_D={(N(r['transportadora']),N(r['departamento'])) for r in R if r['alcance']=='DEPARTAMENTO'}
VET_N={N(r['transportadora']) for r in R if r['alcance']=='NACIONAL'}
# Costo del retorno: fraccion medida por transportadora.
# LEY DE NO-HEREDAR: los parametros son de ESTA empresa, con SU mix de ciudades.
# Se prefiere el archivo por negocio (COSTO-RETORNO-<NEGOCIO>.json, variable
# DROPI_NEGOCIO) y solo se cae al generico si no existe, avisando cual se uso.
# Trampa 5: solo entra la fraccion con confianza alta o media; el resto asume
# 1.00 (conservador). Un caso suelto en $0 NO es "no cobra retorno": ya produjo
# cuatro recomendaciones equivocadas.
RET_DEF=1.00
_neg=(os.environ.get('DROPI_NEGOCIO') or '').strip().upper()
_cands=([ 'datos/COSTO-RETORNO-%s.json'%_neg ] if _neg else [])+['datos/COSTO-RETORNO.json']
RET={}; FUENTE_RETORNO=None
for _rel in _cands:
    try:
        _cr=json.load(open(D(_rel)))
    except Exception:
        continue
    _k=[k for k in _cr if k.startswith('medido')]
    if not _k: continue
    _med=_cr[sorted(_k)[-1]]
    RET={N(k):v['fraccion'] for k,v in _med.items()
         if isinstance(v,dict) and str(v.get('confianza','')).lower() in ('alta','media')}
    FUENTE_RETORNO=_rel.split('/')[-1]
    break
if FUENTE_RETORNO is None:
    RET={'INTERRAPIDISIMO':1.00,'ENVIA':0.72}   # ultimo medido conocido, por si falta el archivo
    FUENTE_RETORNO='(sin archivo: ultimo medido conocido)'
    print('AVISO: sin COSTO-RETORNO en datos/ — se usa el ultimo medido conocido.', file=sys.stderr)
# GD1.1: la bodega manda — TRANSPORTADORAS-OPERATIVAS.json se antepone a todo calculo.
try:
    _op=json.load(open(D('datos/TRANSPORTADORAS-OPERATIVAS.json')))
    _opm=_op[sorted(k for k in _op if k.startswith('medido'))[-1]]
    ESTADO_BODEGA={N(k):v['estado'] for k,v in _opm.items() if isinstance(v,dict) and 'estado' in v}
except Exception:
    ESTADO_BODEGA={}
    print('AVISO: sin TRANSPORTADORAS-OPERATIVAS.json — no se puede filtrar por bodega; verificar a mano', file=sys.stderr)
def bodega_ok(car): return (not ESTADO_BODEGA) or ESTADO_BODEGA.get(car) in ('OPERATIVA','MARGINAL')
try:
    O={x['orden']:x for x in json.load(open(D('salidas/salida-v3.json')))}
except Exception:
    sys.exit('Falta salidas/salida-v3.json. Corre primero scripts/calificar.py: '
             'este script re-decide sobre lo que ese calculo masivo produjo.')
def m(n): return '$'+format(int(round(n)),',d').replace(',','.')

HABILITADAS={'INTERRAPIDISIMO','ENVIA','TCC','VELOCES','COORDINADORA','DOMINA','JAMV-DRIVE'}
res=[]
for oid,precios in Q.items():
    x=O[oid]; prepago=bool(x.get('prepago'))
    cli={}
    import csv
    for row in csv.DictReader(open(huellas_recientes()),delimiter='|'):
        if row['orden']==oid:
            for tok in (row['por_transportadora'] or '').split(';'):
                if ':' in tok:
                    k,v=tok.split(':'); e,d=v.split('/'); cli[N(k)]=(int(e),int(d))
    cands=[]
    for car,fl in precios.items():
        if car not in HABILITADAS: continue          # colombia.md: Servientrega y otras no habilitadas nunca compiten
        if not bodega_ok(car): continue
        _e=EFEC.get(car,x['ciu'],x['dep'])
        if _e is None: continue
        base=_e['pct']
        if (car,x['ciu'],x['dep']) in VET_C or (car,x['dep']) in VET_D or car in VET_N: continue
        if x['forzada'] and car!=x['forzada']: continue
        p=base/100
        if not prepago:
            if x['tot']>0: p=(x['entP']/100*x['tot'] + 10*p)/(x['tot']+10)
            e,d=cli.get(car,(0,0)); n=e+d
            if n>0: p=(e + 3*p)/(n+3)
        else:
            p=max(p,0.97)                            # 9 de 9 prepagos resueltos se entregaron
            e,d=cli.get(car,(0,0)); n=e+d
        ret=0 if prepago else fl*RET.get(car,1.00)    # criterios-decision.md: prepago sin costo de retorno
        ev=p*(x['ticket']-x['costo']-fl) - (1-p)*(fl+ret)
        cands.append(dict(car=car,fl=fl,base=round(base,2),p=round(p*100,1),ev=round(ev),
                          hist=('%d/%d'%(e,d)) if n else '—',
                          muestra_envios=_e['muestra_envios'], fuente_efectividad=_e['fuente_efectividad'],
                          marca_ef=marca(_e['fuente_efectividad'], _e['muestra_envios']),
                          marg=ESTADO_BODEGA.get(car)=='MARGINAL'))
    if prepago:
        # criterios-decision.md: en prepago manda el precio, no el valor esperado.
        # Descarta las que estan a mas de 3 puntos de la mejor efectividad; entre las
        # que quedan, la mas barata, salvo que una con mejor efectividad cueste <$1.500 mas.
        if cands:
            mejorEf=max(c['base'] for c in cands)
            viables=[c for c in cands if c['base']>=mejorEf-3]
            viables.sort(key=lambda c:c['fl'])
            barato=viables[0]
            up=[c for c in viables if c['base']>barato['base'] and c['fl']-barato['fl']<=1500]
            b=max(up,key=lambda c:c['base']) if up else barato
            cands.sort(key=lambda c:c['fl'])
        else: b=None
    else:
        cands.sort(key=lambda c:-c['ev']); b=cands[0] if cands else None
    a=next((c for c in cands if c['car']==x['asig']),None)
    res.append((x,a,b,cands,prepago))
def _d(a,b,prepago):
    # prepago manda el precio (ahorro de flete, cierto e inmediato); contra entrega manda el valor esperado.
    # criterios-decision.md: "Nunca sumarlos en una sola cifra" — no confundir ahorro con valor esperado.
    if not (a and b): return None
    return (a['fl']-b['fl']) if prepago else (b['ev']-a['ev'])
res.sort(key=lambda r:-(_d(r[1],r[2],r[4]) or 0))
tot=0
print('%-9s %-19s %-15s %-26s %-26s %9s %-12s'%('ORDEN','CLIENTE','CIUDAD','ACTUAL','RECOMENDADA','GANA','EFECTIVIDAD'))
for x,a,b,c,prepago in res:
    d=_d(a,b,prepago)
    if d and d>500: tot+=d
    print('%-9s %-19s %-15s %-26s %-26s %9s %-12s'%(x['orden'],x['cli'][:18],x['ciu'][:14],
      '%s%s %s [%s]'%(a['car'][:8],'*' if a.get('marg') else '',m(a['fl']),a['hist']) if a else '—',
      '%s%s %s [%s]'%(b['car'][:8],'*' if b.get('marg') else '',m(b['fl']),b['hist']) if b else '—',
      m(d) if d and d>500 else 'queda igual',
      (b or a or {}).get('marca_ef','—')))
print(); print('TOTAL:',m(tot))
print('fuente de costo de retorno:', FUENTE_RETORNO)
print('fuente de efectividad — municipio:', EFEC.nivel_disponible()['fuente_municipio'] or 'NO disponible')
print('                    — departamento:', EFEC.nivel_disponible()['fuente_departamento'] or 'NO disponible')
print('EFECTIVIDAD: mun/dep/nac = de donde salio el dato · n = envios de esa muestra (sin umbral: 1 envio ya es el dato)')
if any(b and b.get('marg') for _,_,b,_,_ in res):
    print('* = MARGINAL para la bodega: proponer avisando el riesgo y confirmar con la bodega antes de asignar')
json.dump([{**{'orden':x['orden'],'cli':x['cli'],'ciu':x['ciu'],'prepago':prepago},'actual':a,'mejor':b,'cands':c} for x,a,b,c,prepago in res],
          open(D('salidas/DECISION-VIVO.json'),'w'),ensure_ascii=False,indent=1)
