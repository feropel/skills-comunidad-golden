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
EF={N(k):v for k,v in json.load(open(D('datos/EFECTIVIDAD-PLATAFORMA.json'))).items()}
Q=json.load(open(D('datos/COTIZACIONES-VIVO.json')))
R=json.load(open(D('datos/RECHAZOS-FULFILLMENT.json')))['rechazos']
VET_C={(N(r['transportadora']),N(r['ciudad']),N(r['departamento'])) for r in R if r['alcance']=='CIUDAD'}
VET_D={(N(r['transportadora']),N(r['departamento'])) for r in R if r['alcance']=='DEPARTAMENTO'}
VET_N={N(r['transportadora']) for r in R if r['alcance']=='NACIONAL'}
# retorno: fraccion medida por transportadora (trampa 5: solo confianza alta/media; el resto 1.00)
try:
    _cr=json.load(open(D('datos/COSTO-RETORNO.json')))
    _med=_cr[sorted(k for k in _cr if k.startswith('medido'))[-1]]
    RET={N(k):v['fraccion'] for k,v in _med.items() if str(v.get('confianza','')).lower() in ('alta','media')}
except Exception:
    RET={'INTERRAPIDISIMO':1.00,'ENVIA':0.72}   # ultimo medido conocido, por si falta el archivo
# GD1.1: la bodega manda — TRANSPORTADORAS-OPERATIVAS.json se antepone a todo calculo.
try:
    _op=json.load(open(D('datos/TRANSPORTADORAS-OPERATIVAS.json')))
    _opm=_op[sorted(k for k in _op if k.startswith('medido'))[-1]]
    ESTADO_BODEGA={N(k):v['estado'] for k,v in _opm.items() if isinstance(v,dict) and 'estado' in v}
except Exception:
    ESTADO_BODEGA={}
    print('AVISO: sin TRANSPORTADORAS-OPERATIVAS.json — no se puede filtrar por bodega; verificar a mano', file=sys.stderr)
def bodega_ok(car): return (not ESTADO_BODEGA) or ESTADO_BODEGA.get(car) in ('OPERATIVA','MARGINAL')
O={x['orden']:x for x in json.load(open(D('salidas/salida-v3.json')))}
def m(n): return '$'+format(int(round(n)),',d').replace(',','.')

HABILITADAS={'INTERRAPIDISIMO','ENVIA','TCC','VELOCES','COORDINADORA','DOMINA','JAMV-DRIVE'}
res=[]
for oid,precios in Q.items():
    x=O[oid]; ef=EF.get(x['dep'],{}); prepago=bool(x.get('prepago'))
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
        base=ef.get(car,{}).get('pct')
        if base is None: continue
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
print('%-9s %-19s %-15s %-26s %-26s %9s'%('ORDEN','CLIENTE','CIUDAD','ACTUAL','RECOMENDADA','GANA'))
for x,a,b,c,prepago in res:
    d=_d(a,b,prepago)
    if d and d>500: tot+=d
    print('%-9s %-19s %-15s %-26s %-26s %9s'%(x['orden'],x['cli'][:18],x['ciu'][:14],
      '%s%s %s [%s]'%(a['car'][:8],'*' if a.get('marg') else '',m(a['fl']),a['hist']) if a else '—',
      '%s%s %s [%s]'%(b['car'][:8],'*' if b.get('marg') else '',m(b['fl']),b['hist']) if b else '—',
      m(d) if d and d>500 else 'queda igual'))
print(); print('TOTAL:',m(tot))
if any(b and b.get('marg') for _,_,b,_,_ in res):
    print('* = MARGINAL para la bodega: proponer avisando el riesgo y confirmar con la bodega antes de asignar')
json.dump([{**{'orden':x['orden'],'cli':x['cli'],'ciu':x['ciu'],'prepago':prepago},'actual':a,'mejor':b,'cands':c} for x,a,b,c,prepago in res],
          open(D('salidas/DECISION-VIVO.json'),'w'),ensure_ascii=False,indent=1)
