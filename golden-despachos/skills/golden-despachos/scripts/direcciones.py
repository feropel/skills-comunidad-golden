# -*- coding: utf-8 -*-
"""Analisis de direcciones colombianas: unica puerta, con banco de pruebas propio.

Un detector de patrones acusa el LENGUAJE, no el defecto. Por eso este modulo se
prueba en los DOS sentidos: los casos que debe morder y los que debe dejar pasar.
El banco nacio midiendo: sobre 895 direcciones reales del export habia 12 mal
clasificadas (1,3%), y las tres clases estaban justo en el sentido que nadie
habia probado.

    python3 direcciones.py --autoprueba
"""
import re, sys, unicodedata


def N(s):
    s = unicodedata.normalize('NFD', str(s) if s is not None else '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper().strip()


# Puerta: "# 30-45", "#30A-45", "# 1 OESTE - 03" y tambien "# 65 GG - 22".
# OJO CON LAS LETRAS: son HASTA TRES, no una. Medellin y Bogota usan dobles
# ("100 AB - 03", "34 AA - 80", "66 BB - 51") y Cali del norte agrega la N de
# norte ("23AN-45"). Con [A-Z]? esas direcciones salian INCOMPLETA y se le
# pedia al cliente un numero de puerta que ya estaba escrito.
RE_PUERTA = re.compile(r'#\s*\d+\s*[A-Z]{0,3}\s*(OESTE|ESTE|SUR|NORTE|BIS)?\s*-\s*\d+')
RE_PUERTA_SIN_NUMERAL = re.compile(r'\b\d+\s*[A-Z]{0,3}\s*-\s*\d+')
RE_VIA = re.compile(r'\b(CL|CLL|CALLE|KR|CRA|CR|CARRERA|AV|AVENIDA|DG|DIAGONAL|'
                    r'TV|TRANSVERSAL|AK|AC|MZ|MANZANA|VEREDA|KM)\b')
RE_MZCS = re.compile(r'\b(MZ|MANZANA)\b.*\b(CS|CASA)\b')
RE_INTERNO = re.compile(r'\b(AP|APTO|APTM|APARTAMENTO|CASA|CS|INT|INTERIOR|PISO|PI|LOCAL|OF)\b\s*\.?\s*\d*')
RE_COLECTIVA = re.compile(r'\b(CONJUNTO|CONJ|UNIDAD|EDIFICIO|EDIFICO|ED|TORRE|TO|BLOQUE|BL)\b')
RE_PUBLICO = re.compile(r'\b(ESTACION DE POLICIA|HOTEL|TERMINAL|CENTRO DE NEGOCIOS|CC|CENTRO COMERCIAL)\b')
# Zona rural: alli NO hay numero de puerta y nunca lo habra. Se entrega por punto
# de referencia. "FINCA" a secas NO entra: hay edificios urbanos llamados "La
# Finca" y meterlo se traga direcciones de ciudad.
RE_RURAL = re.compile(r'\b(VEREDA|VDA|CORREGIMIENTO|CORREG|PARCELACION|KM\s*\d)\b')
RE_TRANSPORTADORA_AJENA = ('SERVIENTREGA', 'RAPIENTREGA', 'DEPRISA', 'SATURNO')


def analiza_dir(d, ciudad=''):
    """Devuelve (estado, detalle, transportadora_forzada).

    Estados: OFICINA (retiro en punto, bloquea el cambio de transportadora),
    BLOQUEO, INCOMPLETA, RURAL, REVISAR, OK.
    """
    t = N(d)
    puerta = bool(RE_PUERTA.search(t)) or bool(RE_PUERTA_SIN_NUMERAL.search(t))
    tiene_num = puerta or bool(RE_MZCS.search(t))

    # 1. recogida en oficina de una transportadora
    comp = t.replace(' ', '').replace('.', '')
    pickup = ('RETIRA EN' in t) or ('RECOGE EN' in t)
    if 'OFICINA' in t or pickup:
        if 'INTERRAPID' in comp or 'INTERRAPIS' in comp:
            return ('OFICINA', 'retiro en oficina InterRapidisimo — la transportadora NO se puede cambiar', 'INTERRAPIDISIMO')
        if 'COORDINADORA' in comp:
            return ('OFICINA', 'retiro en oficina Coordinadora — la transportadora NO se puede cambiar', 'COORDINADORA')
        if 'SERVIENTREGA' in comp:
            return ('BLOQUEO', 'pide oficina Servientrega, que NO esta habilitada — hay que reconfirmar con el cliente', None)
        # "OFICINA" sin transportadora y CON nomenclatura completa es la oficina
        # PROPIA del cliente ("Calle 17 # 2E-30 oficina EMNFC SAS"): es un destino
        # normal y entregable, no un punto de retiro. Bloquearlo mandaba a
        # reconfirmar una direccion que ya estaba bien.
        if pickup or not tiene_num:
            return ('BLOQUEO', 'dice oficina pero no se identifica cual — confirmar transportadora y ciudad', None)

    # 2. transportadora ajena mencionada en la direccion
    for x in RE_TRANSPORTADORA_AJENA:
        if x in t:
            return ('REVISAR', 'la direccion menciona "%s"; si es punto de esa empresa no sirve — confirmar' % x.title(), None)

    # 3. nomenclatura
    if len(re.findall(r'#', t)) >= 2:
        return ('REVISAR', 'la direccion trae DOS nomenclaturas distintas — confirmar cual es la buena', None)
    if re.search(r'#\s*\d+\s*[A-Z]{0,3}\s*$', t) or (re.search(r'#\s*\d', t) and not puerta):
        return ('INCOMPLETA', 'la nomenclatura queda cortada: falta el numero de puerta despues del guion', None)
    tiene_via = bool(RE_VIA.search(t))
    tres = len(re.findall(r'\d+', t)) >= 3
    # Zona rural ANTES de exigir puerta: pedirle el numero de la casa a quien vive
    # en una vereda es pedir algo que no existe. Se pide punto de referencia.
    if not tiene_num and RE_RURAL.search(t):
        return ('RURAL', 'zona rural sin numero de puerta (normal alli): confirmar punto de referencia y que la transportadora llegue', None)
    if not tiene_via and not tiene_num:
        return ('INCOMPLETA', 'no hay nomenclatura: falta via y numeros (Calle/Carrera # __-__)', None)
    if tiene_via and not tiene_num and not tres:
        return ('INCOMPLETA', 'falta el numero de puerta: solo trae la via', None)
    if not tiene_num and tres:
        return ('REVISAR', 'numeracion sin formato # __-__; verificar que sea la puerta correcta', None)

    # 4. vivienda colectiva sin numero interno
    colect = RE_COLECTIVA.search(t)
    interno = RE_INTERNO.search(t)
    if colect and not interno:
        return ('INCOMPLETA', 'menciona %s pero no da torre/apartamento' % colect.group(1).lower(), None)

    # 5. lugar publico o comercial sin punto exacto
    if RE_PUBLICO.search(t) and not interno:
        return ('REVISAR', 'entrega en lugar publico o comercial sin oficina/local — confirmar a quien se entrega', None)
    return ('OK', '', None)


# --------------------------------------------------------------------- banco
# En los DOS sentidos. Las direcciones marcadas [REAL] salieron del export de
# 895 pedidos y estaban mal clasificadas antes de este arreglo.
CASOS = [
    # --- deben MORDER ---
    ('CALLE 10 OFICINA INTERRAPIDISIMO CENTRO', 'OFICINA', 'retiro en oficina Inter, fuerza transportadora'),
    ('RECOGE EN OFICINA COORDINADORA PARQUE', 'OFICINA', 'retiro en oficina Coordinadora'),
    ('OFICINA SERVIENTREGA DEL CENTRO', 'BLOQUEO', 'oficina de empresa NO habilitada'),
    ('OFICINA DEL CENTRO', 'BLOQUEO', 'dice oficina, sin transportadora y SIN nomenclatura'),
    ('RETIRA EN OFICINA CALLE 5 # 10-20', 'BLOQUEO', 'retiro explicito: aunque traiga nomenclatura, es punto'),
    ('BARRIO EL PORVENIR CASA VERDE', 'INCOMPLETA', 'sin via ni numeros'),
    ('CALLE 45', 'INCOMPLETA', 'via sin numero de puerta'),
    ('CRA 7 # 23-', 'INCOMPLETA', 'nomenclatura cortada'),
    ('CL 5 # 10-20 CONJUNTO LOS ROBLES', 'INCOMPLETA', 'colectiva sin torre ni apto'),
    ('CL 5 # 10-20 Y TAMBIEN CRA 8 # 4-11', 'REVISAR', 'dos nomenclaturas en un campo'),
    ('CL 5 # 10-20 PUNTO SERVIENTREGA', 'REVISAR', 'menciona transportadora ajena'),
    ('CL 5 # 10-20 HOTEL DANN', 'REVISAR', 'lugar publico sin habitacion'),
    ('VEREDA LA ESPERANZA KM 4 VIA AL MAR', 'RURAL', 'rural: se pide referencia, NO numero de puerta'),
    ('VE YERBABUENA PARCELACION PAN DE AZUCAR CASA 13 VEREDA YERBABUENA', 'RURAL', '[REAL] antes salia INCOMPLETA'),
    # --- NO deben morder ---
    ('Calle 17 # 2e-30 Barrio Caobos oficina EMNFC SAS', 'OK', '[REAL] oficina PROPIA del cliente, antes BLOQUEO'),
    ('CL 20 # 65 GG - 22 TRINIDAD', 'OK', '[REAL] doble letra, antes INCOMPLETA'),
    ('KR 79 B # 100 AB - 03 BR ANTONIO', 'OK', '[REAL] doble letra, antes INCOMPLETA'),
    ('CL 56 # 66 BB - 51 EL PARAISO', 'OK', '[REAL] doble letra, antes INCOMPLETA'),
    ('AV 6N # 23AN-45', 'OK', 'Cali norte: letra + N de norte'),
    ('CALLE 44 # 30-45', 'OK', 'nomenclatura completa'),
    ('CRA 100 # 11A-99 APTO 502 TORRE 3', 'OK', 'colectiva CON interno'),
    ('MZ D CS 14 BARRIO SAN JUDAS', 'OK', 'manzana y casa'),
    ('CALLE 1 OESTE # 1 OESTE - 03', 'OK', 'nomenclatura del Valle con OESTE'),
    ('CL 22 # 8-30 EDIFICIO BOLIVAR LOCAL 4', 'OK', 'edificio CON local'),
    ('Calle 22 este #169-04 La finca apartamento 604', 'OK', '[REAL] nomenclatura completa con nombre de edificio'),
    # Este caso SI alcanza la rama rural (no hay puerta) y es el que sostiene que
    # FINCA no sea marca rural: sin via ni numeros la direccion esta incompleta,
    # se llame como se llame el edificio. Metiendo FINCA en RE_RURAL sale RURAL
    # y el banco muerde; sin este caso, esa guardia era decorativa.
    ('EDIFICIO LA FINCA APARTAMENTO 604', 'INCOMPLETA', '"finca" en nombre de edificio no vuelve rural la direccion'),
]


def autoprueba():
    mal = 0
    for d, esperado, por in CASOS:
        got = analiza_dir(d)[0]
        if got != esperado:
            mal += 1
            print('  🔴 %s\n     esperado %s, obtuvo %s  (%s)' % (d[:70], esperado, got, por))
    # la que fuerza transportadora debe forzarla de verdad, no solo etiquetar
    if analiza_dir('CALLE 10 OFICINA INTERRAPIDISIMO')[2] != 'INTERRAPIDISIMO':
        mal += 1
        print('  🔴 oficina Inter no devolvio la transportadora forzada')
    print('AUTOPRUEBA direcciones: %s, %d de %d' % ('OK' if not mal else 'FALLA', len(CASOS) + 1 - mal, len(CASOS) + 1))
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(autoprueba() if '--autoprueba' in sys.argv else
             print('Uso: python3 direcciones.py --autoprueba') or 0)
