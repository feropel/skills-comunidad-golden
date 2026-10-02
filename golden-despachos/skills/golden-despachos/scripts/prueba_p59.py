# -*- coding: utf-8 -*-
"""Corre decidir_vivo.py contra el sembrado PERMANENTE de la FILA P59 y verifica que
ninguna exclusion vuelva a ser silenciosa.

No es una autoprueba de funcion pura: ejecuta el script REAL de punta a punta sobre
datos en disco, que es la fase que mas se salta. El sembrado vive en
`DROPI-LOGISTICA/pruebas/sembrado-p59/` (permanente, con git), no en un temporal,
para que el proximo arreglo se pueda medir contra el caso original.

    python3 prueba_p59.py
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SEMBRADO = os.path.expanduser('~/Desktop/⭐️ MASTER ⭐️/🤖 IA/🟠 CLAUDE/🌐 PROYECTOS/'
                              'DROPI-LOGISTICA/pruebas/sembrado-p59')

# (orden, asignada, trozo que DEBE aparecer en la salida)
ESPERADO = [
    ('90000001', 'SERVIENTREGA', 'no habilitada en Colombia'),
    ('90000002', 'TCC', 'la bodega nunca la ha usado'),
    ('90000003', 'COORDINADORA', 'vetada por el fulfillment'),
    ('90000004', 'ENVIA', 'la direccion exige INTERRAPIDISIMO'),
    ('90000005', 'DOMINA', 'sin efectividad medida'),
]
CONTROL = '90000006'


def main():
    if not os.path.isdir(SEMBRADO):
        print('🔴 falta el sembrado permanente en %s' % SEMBRADO)
        print('   se crea con el generador que dejo la FILA P59 (ver LEEME.md de esa carpeta)')
        return 1
    env = dict(os.environ, DROPI_DATA=SEMBRADO, DROPI_NEGOCIO='SEMBRADO')
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'decidir_vivo.py')],
                       capture_output=True, text=True, env=env, cwd=AQUI)
    salida = r.stdout + r.stderr
    if r.returncode != 0:
        print('🔴 decidir_vivo.py murio (exit %d):' % r.returncode)
        print(salida[-2500:])
        return 1

    mal = 0

    def caso(nombre, cond, detalle=''):
        nonlocal mal
        if not cond:
            mal += 1
            print('  🔴 %s %s' % (nombre, detalle))

    # 1. cada asignada excluida sale NOMBRADA y con su razon
    #
    # 🔴 OJO, ESTO SE MIDE EN LA LINEA DEL PEDIDO, NO EN TODA LA SALIDA. Buscar
    # `razon in salida` se validaba SOLO: el resumen del pie ya nombra cada motivo y
    # cada transportadora, asi que quitar la razon de la fila del pedido no movia el
    # veredicto. Dos sabotajes pasaron en verde hasta que se acoto a la fila y a su
    # linea de continuacion. Es la trampa 14 otra vez, y la del modal de huellas: un
    # chequeo que busca en todo el documento encuentra su propia respuesta.
    lineas = salida.splitlines()
    for orden, asig, razon in ESPERADO:
        i = next((k for k, l in enumerate(lineas) if l.startswith(orden)), None)
        caso('%s aparece en el informe' % orden, i is not None)
        if i is None:
            continue
        linea = lineas[i]
        sigue = lineas[i + 1] if i + 1 < len(lineas) else ''
        bloque = linea + '\n' + (sigue if '↳' in sigue else '')
        caso('%s nombra a la asignada %s en SU fila' % (orden, asig),
             asig[:8] in linea, '-> %s' % linea.strip())
        caso('%s no deja la columna ACTUAL en guion' % orden,
             ' — ' not in linea and not linea.rstrip().endswith('—'),
             '-> %s' % linea.strip())
        caso('%s declara la razon junto al pedido' % orden, razon in bloque,
             '(falta "%s" en su bloque) -> %s' % (razon, bloque.strip()))
        caso('%s NO dice "queda igual"' % orden, 'queda igual' not in linea,
             '-> %s' % linea.strip())
        caso('%s se marca CAMBIO OBLIGADO' % orden, 'CAMBIO OBLIGADO' in linea,
             '-> %s' % linea.strip())

    # 2. el CONTROL SANO no puede dar cambio obligado (el sentido que nadie prueba)
    ctrl = next((l for l in salida.splitlines() if CONTROL in l), '')
    caso('control sano aparece', bool(ctrl))
    caso('control sano NO es cambio obligado', 'CAMBIO OBLIGADO' not in ctrl,
         '-> %s' % ctrl.strip())
    caso('control sano nombra su transportadora', 'ENVIA' in ctrl, '-> %s' % ctrl.strip())

    # 3. el costo de retorno del negocio esta ROTO: tiene que decirlo, no callarse
    caso('el archivo de retorno roto se NOMBRA',
         'EXISTE pero no se pudo leer' in salida)
    caso('se declara que se uso el generico', 'COSTO-RETORNO.json' in salida)
    # 4. la transportadora en confianza baja se excluye PERO se nombra
    caso('la confianza baja se NOMBRA', 'VELOCES' in salida and 'confianza baja' in salida)
    # 5. las candidatas descartadas se cuentan y se nombran
    caso('las descartadas del lote se resumen', 'transportadoras descartadas en el lote' in salida)

    total = len(ESPERADO) * 6 + 3 + 4
    print('PRUEBA P59 (decidir_vivo contra el sembrado): %s, %d de %d'
          % ('OK' if not mal else 'FALLA', total - mal, total))
    if mal:
        print('\n--- salida completa para diagnostico ---')
        print(salida)
    return 1 if mal else 0


if __name__ == '__main__':
    sys.exit(main())
