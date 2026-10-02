# -*- coding: utf-8 -*-
"""Por que una transportadora sale de las candidatas: UNA puerta, con razon SIEMPRE.

P59 (Centro de Mando): una herramienta que DESCARTA datos del usuario tiene que
CONTARLOS y NOMBRARLOS. Una exclusion correcta que no se declara no se distingue
de un olvido.

El defecto que arregla, medido en `decidir_vivo.py`: la transportadora ASIGNADA se
buscaba DENTRO de las candidatas (`next(c for c in cands if c['car']==asig)`), asi
que si cualquiera de los cinco filtros la habia excluido, la columna ACTUAL
imprimia «—» y la columna GANA decia «queda igual» sobre un pedido que hay que
cambiar OBLIGATORIAMENTE — una asignada vetada por el fulfillment, o que la bodega
no usa, salia del informe como si no hubiera nada que hacer. Seis de las diez
exclusiones silenciosas de la skill eran esa.

Por eso aqui hay dos cosas, y las dos importan:
  - `razon(...)` devuelve el motivo (o None si compite), para poder CONTAR y NOMBRAR.
  - `ORDEN_RAZONES` fija cual motivo se reporta cuando aplican varios: primero los
    operativos duros (la bodega o el fulfillment no lo despachan), al final los
    huecos de dato. Reportar «sin efectividad medida» sobre una vetada esconde lo
    que de verdad bloquea el despacho.

    python3 exclusiones.py --autoprueba
"""
import sys

# Orden deliberado: de lo que IMPIDE despachar a lo que solo es falta de dato.
ORDEN_RAZONES = (
    'no habilitada en Colombia',
    'la bodega nunca la ha usado',
    'vetada por el fulfillment en ese destino',
    'la direccion exige %s (retiro en oficina)',
    'sin tarifa cotizada',
    'sin efectividad medida en municipio, departamento ni nacional',
)


def razon(car, ciu, dep, habilitadas, bodega_ok, vetada, forzada, efec, cotizada=True):
    """Devuelve el motivo por el que `car` no compite, o None si compite.

    `bodega_ok` y `vetada` son funciones; `efec` es lo que devolvio la puerta de
    efectividad (None = sin dato en ningun nivel).
    """
    if car not in habilitadas:
        return ORDEN_RAZONES[0]
    if not bodega_ok(car):
        return ORDEN_RAZONES[1]
    if vetada(car, ciu, dep):
        return ORDEN_RAZONES[2]
    if forzada and car != forzada:
        return ORDEN_RAZONES[3] % forzada
    if not cotizada:
        return ORDEN_RAZONES[4]
    if efec is None:
        return ORDEN_RAZONES[5]
    return None


def resumen(excluidas):
    """Una linea por motivo, con la cuenta y los nombres. Nunca un total pelado."""
    if not excluidas:
        return []
    por_razon = {}
    for e in excluidas:
        por_razon.setdefault(e['razon'], []).append(e['car'])
    return ['%d excluida(s) por %s: %s' % (len(v), k, ', '.join(sorted(set(v))))
            for k, v in sorted(por_razon.items())]


# --------------------------------------------------------------------- banco
def autoprueba():
    HAB = {'ENVIA', 'INTERRAPIDISIMO', 'COORDINADORA', 'VELOCES'}
    EFEC_OK = {'pct': 80.0, 'muestra_envios': 10, 'fuente_efectividad': 'municipio'}
    si = lambda car: True                      # la bodega la usa
    no = lambda car: False                     # la bodega NO la usa
    libre = lambda car, ciu, dep: False         # sin veto
    vetada_todo = lambda car, ciu, dep: True    # vetada

    mal = 0

    def caso(nombre, obtenido, esperado):
        nonlocal mal
        if obtenido != esperado:
            mal += 1
            print('  🔴 %s\n     esperado %r, obtuvo %r' % (nombre, esperado, obtenido))

    # --- deben dar RAZON (y la razon correcta, no una cualquiera) ---
    caso('no habilitada',
         razon('SERVIENTREGA', 'CALI', 'VALLE', HAB, si, libre, None, EFEC_OK),
         'no habilitada en Colombia')
    caso('la bodega no la usa',
         razon('ENVIA', 'CALI', 'VALLE', HAB, no, libre, None, EFEC_OK),
         'la bodega nunca la ha usado')
    caso('vetada por fulfillment',
         razon('ENVIA', 'LA HORMIGA', 'PUTUMAYO', HAB, si, vetada_todo, None, EFEC_OK),
         'vetada por el fulfillment en ese destino')
    caso('la direccion exige otra',
         razon('ENVIA', 'CALI', 'VALLE', HAB, si, libre, 'INTERRAPIDISIMO', EFEC_OK),
         'la direccion exige INTERRAPIDISIMO (retiro en oficina)')
    caso('sin tarifa cotizada',
         razon('ENVIA', 'CALI', 'VALLE', HAB, si, libre, None, EFEC_OK, cotizada=False),
         'sin tarifa cotizada')
    caso('sin efectividad',
         razon('ENVIA', 'CALI', 'VALLE', HAB, si, libre, None, None),
         'sin efectividad medida en municipio, departamento ni nacional')

    # --- NO deben dar razon: la que compite, compite ---
    caso('la sana compite',
         razon('ENVIA', 'CALI', 'VALLE', HAB, si, libre, None, EFEC_OK), None)
    caso('la forzada compite consigo misma',
         razon('INTERRAPIDISIMO', 'CALI', 'VALLE', HAB, si, libre, 'INTERRAPIDISIMO', EFEC_OK), None)
    caso('efectividad de 1 solo envio SIRVE (orden de FER: sin umbral)',
         razon('ENVIA', 'X', 'Y', HAB, si, libre, None,
               {'pct': 100.0, 'muestra_envios': 1, 'fuente_efectividad': 'municipio'}), None)
    caso('efectividad en CERO por ciento es DATO, no ausencia',
         razon('ENVIA', 'X', 'Y', HAB, si, libre, None,
               {'pct': 0.0, 'muestra_envios': 4, 'fuente_efectividad': 'municipio'}), None)
    caso('bodega vacia (sin archivo) no excluye a nadie',
         razon('ENVIA', 'CALI', 'VALLE', HAB, lambda c: True, libre, None, EFEC_OK), None)

    # --- el ORDEN importa: lo duro manda sobre el hueco de dato ---
    caso('vetada Y sin efectividad reporta el VETO, no el hueco',
         razon('ENVIA', 'LA HORMIGA', 'PUTUMAYO', HAB, si, vetada_todo, None, None),
         'vetada por el fulfillment en ese destino')
    caso('no usada por la bodega Y vetada reporta la BODEGA primero',
         razon('ENVIA', 'LA HORMIGA', 'PUTUMAYO', HAB, no, vetada_todo, None, EFEC_OK),
         'la bodega nunca la ha usado')

    # --- el resumen cuenta y nombra, nunca da un total pelado ---
    r = resumen([{'car': 'TCC', 'razon': 'sin efectividad medida en municipio, departamento ni nacional'},
                 {'car': 'DOMINA', 'razon': 'sin efectividad medida en municipio, departamento ni nacional'},
                 {'car': 'SERVIENTREGA', 'razon': 'no habilitada en Colombia'}])
    caso('resumen agrupa por motivo', len(r), 2)
    caso('resumen nombra a las excluidas',
         any('TCC' in x and 'DOMINA' in x and x.startswith('2 ') for x in r), True)
    caso('resumen vacio cuando no hay exclusiones', resumen([]), [])

    total = 16
    print('AUTOPRUEBA exclusiones: %s, %d de %d' % ('OK' if not mal else 'FALLA', total - mal, total))
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(autoprueba() if '--autoprueba' in sys.argv else
             print('Uso: python3 exclusiones.py --autoprueba') or 0)
