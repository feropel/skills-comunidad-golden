"""
calculate_unit_economics.py — Cálculo de CPA breakeven y umbrales de margen.

Uso:
    from calculate_unit_economics import calculate_unit_economics, print_summary
    
    result = calculate_unit_economics(
        precio=75000,
        costo_producto=15000,
        flete_entregada=17000,
        flete_fallida=12000,
        tasa_cancelacion=0.10,
        tasa_devolucion=0.25,
        base_devolucion='enviadas',
        producto_recuperable=True,
        costo_cancelacion=0
    )
    print_summary(result)
"""


def calculate_unit_economics(
    precio,
    costo_producto,
    flete_entregada=17000,
    flete_fallida=12000,
    tasa_cancelacion=0.10,
    tasa_devolucion=0.25,
    base_devolucion='enviadas',
    producto_recuperable=True,
    costo_cancelacion=None
):
    """
    Calcula unit economics completos para una pauta de Meta Ads.
    
    Args:
        precio: precio de venta al cliente
        costo_producto: costo unitario del producto
        flete_entregada: costo del flete cuando llega al cliente
        flete_fallida: costo del flete en devolución (rechazo al recibir)
        tasa_cancelacion: % de órdenes que se cancelan antes de envío (0-1)
        tasa_devolucion: % de devoluciones (0-1)
        base_devolucion: 'enviadas' o 'total' — sobre qué se calcula la tasa
        producto_recuperable: True si el producto en devolución se revende
        costo_cancelacion: costo de flete en cancelación. Si None, asume = flete_fallida.
                           Pasar 0 si no se paga nada en cancelaciones.
    
    Returns:
        dict con todos los cálculos
    """
    
    if costo_cancelacion is None:
        costo_cancelacion = flete_fallida
    
    # Calcular flujo sobre 100 órdenes
    n = 100
    canceladas = n * tasa_cancelacion
    
    if base_devolucion == 'enviadas':
        enviadas = n - canceladas
        devueltas = enviadas * tasa_devolucion
        entregadas = enviadas - devueltas
    elif base_devolucion == 'total':
        devueltas = n * tasa_devolucion
        entregadas = n - canceladas - devueltas
        enviadas = entregadas + devueltas
    else:
        raise ValueError(f"base_devolucion debe ser 'enviadas' o 'total', no '{base_devolucion}'")
    
    # Ingresos
    ingresos = entregadas * precio
    
    # Costo de producto
    if producto_recuperable:
        costo_prod = entregadas * costo_producto
    else:
        # En devoluciones el producto se pierde (devueltas), en canceladas no se envió
        costo_prod = (entregadas + devueltas) * costo_producto
    
    # Fletes
    flete_cancel_total = canceladas * costo_cancelacion
    flete_dev_total = devueltas * flete_fallida
    flete_ent_total = entregadas * flete_entregada
    fletes_total = flete_cancel_total + flete_dev_total + flete_ent_total
    
    # Margen pre-pauta
    margen_pre_pauta = ingresos - costo_prod - fletes_total
    cpa_breakeven = margen_pre_pauta / n
    margen_por_entregada = margen_pre_pauta / entregadas if entregadas > 0 else 0
    
    # CPA según margen neto deseado
    cpa_por_margen = {}
    for pct in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        margen_deseado = ingresos * pct
        pauta_max = margen_pre_pauta - margen_deseado
        cpa_max = pauta_max / n
        roas_obj = ingresos / pauta_max if pauta_max > 0 else 0
        ganancia_por_100 = pauta_max - cpa_max * n + margen_deseado  # = margen_deseado
        cpa_por_margen[f'margen_{int(pct*100)}pct'] = {
            'cpa_max': round(cpa_max, 0),
            'roas_objetivo': round(roas_obj, 2),
            'ganancia_por_100_ordenes': round(margen_deseado, 0)
        }
    
    # ROAS breakeven (sobre Meta, considerando que solo entregadas pagan)
    # ROAS = ingresos / gasto_pauta_para_breakeven
    roas_breakeven = ingresos / (cpa_breakeven * n) if cpa_breakeven > 0 else 0
    
    return {
        'inputs': {
            'precio': precio,
            'costo_producto': costo_producto,
            'flete_entregada': flete_entregada,
            'flete_fallida': flete_fallida,
            'costo_cancelacion': costo_cancelacion,
            'tasa_cancelacion': tasa_cancelacion,
            'tasa_devolucion': tasa_devolucion,
            'base_devolucion': base_devolucion,
            'producto_recuperable': producto_recuperable
        },
        'flujo_100_ordenes': {
            'canceladas': round(canceladas, 2),
            'enviadas': round(enviadas, 2),
            'devueltas': round(devueltas, 2),
            'entregadas': round(entregadas, 2),
            'tasa_entrega_real_pct': round(entregadas / n * 100, 2)
        },
        'pyl': {
            'ingresos': round(ingresos, 0),
            'costo_producto_total': round(costo_prod, 0),
            'fletes_total': round(fletes_total, 0),
            'flete_canceladas': round(flete_cancel_total, 0),
            'flete_devueltas': round(flete_dev_total, 0),
            'flete_entregadas': round(flete_ent_total, 0),
            'margen_pre_pauta': round(margen_pre_pauta, 0),
            'margen_pre_pauta_pct': round(margen_pre_pauta / ingresos * 100, 1) if ingresos > 0 else 0
        },
        'cpa_breakeven': round(cpa_breakeven, 0),
        'roas_breakeven': round(roas_breakeven, 2),
        'margen_por_entregada': round(margen_por_entregada, 0),
        'cpa_por_margen_objetivo': cpa_por_margen
    }


def evaluar_cpa(cpa_real, ue):
    """
    Asigna semáforo a un CPA dado los unit economics.
    
    Returns: (tier, descripcion, margen_neto_por_compra_meta)
    """
    cpa_be = ue['cpa_breakeven']
    cpa_5 = ue['cpa_por_margen_objetivo']['margen_5pct']['cpa_max']
    cpa_10 = ue['cpa_por_margen_objetivo']['margen_10pct']['cpa_max']
    cpa_15 = ue['cpa_por_margen_objetivo']['margen_15pct']['cpa_max']
    cpa_20 = ue['cpa_por_margen_objetivo']['margen_20pct']['cpa_max']
    
    margen_neto = (cpa_be - cpa_real)  # margen neto por compra Meta
    
    if cpa_real <= cpa_20:
        tier = '🟢 EXCELENTE'
        descripcion = '20%+ margen — escalar agresivamente'
    elif cpa_real <= cpa_15:
        tier = '🟢 MUY BUENO'
        descripcion = '15-20% margen — escalar'
    elif cpa_real <= cpa_10:
        tier = '🟢 BUENO'
        descripcion = '10-15% margen — escalar moderadamente'
    elif cpa_real <= cpa_5:
        tier = '🟡 ACEPTABLE'
        descripcion = '5-10% margen — mantener'
    elif cpa_real <= cpa_be:
        tier = '🟡 MARGINAL'
        descripcion = '0-5% margen — revisar tendencia'
    elif cpa_real <= cpa_be * 1.3:
        tier = '🔴 PIERDE'
        descripcion = 'Pierde plata, hasta 30% sobre breakeven — pausar y rediseñar'
    else:
        tier = '⚫ DESCARTAR'
        descripcion = '>30% sobre breakeven — apagar, no rescatar'
    
    return tier, descripcion, round(margen_neto, 0)


def calcular_pyl_historico(compras_meta, gasto_pauta_total, ue):
    """
    Aplica unit economics al gasto histórico real para saber si la cuenta perdió o ganó.
    """
    inputs = ue['inputs']
    n = compras_meta
    
    # Replicar flujo
    canceladas = n * inputs['tasa_cancelacion']
    if inputs['base_devolucion'] == 'enviadas':
        enviadas = n - canceladas
        devueltas = enviadas * inputs['tasa_devolucion']
        entregadas = enviadas - devueltas
    else:
        devueltas = n * inputs['tasa_devolucion']
        entregadas = n - canceladas - devueltas
    
    ingresos = entregadas * inputs['precio']
    
    if inputs['producto_recuperable']:
        costo_prod = entregadas * inputs['costo_producto']
    else:
        costo_prod = (entregadas + devueltas) * inputs['costo_producto']
    
    fletes = (canceladas * inputs['costo_cancelacion'] + 
              devueltas * inputs['flete_fallida'] + 
              entregadas * inputs['flete_entregada'])
    
    margen_pre = ingresos - costo_prod - fletes
    margen_neto = margen_pre - gasto_pauta_total
    margen_pct = margen_neto / ingresos * 100 if ingresos > 0 else 0
    cpa_promedio = gasto_pauta_total / compras_meta if compras_meta > 0 else 0
    
    return {
        'gasto_pauta': round(gasto_pauta_total, 0),
        'compras_meta': round(compras_meta, 0),
        'cpa_promedio': round(cpa_promedio, 0),
        'entregadas_reales': round(entregadas, 0),
        'ingresos_reales': round(ingresos, 0),
        'margen_pre_pauta': round(margen_pre, 0),
        'margen_neto_final': round(margen_neto, 0),
        'margen_pct': round(margen_pct, 2),
        'rentable': margen_neto > 0
    }


def print_summary(ue):
    """Imprime resumen legible de unit economics."""
    print("="*70)
    print("UNIT ECONOMICS")
    print("="*70)
    
    f = ue['flujo_100_ordenes']
    p = ue['pyl']
    
    print(f"\nFlujo sobre 100 órdenes Meta:")
    print(f"  Canceladas: {f['canceladas']}")
    print(f"  Enviadas: {f['enviadas']}")
    print(f"  Devueltas: {f['devueltas']}")
    print(f"  Entregadas: {f['entregadas']} ({f['tasa_entrega_real_pct']}%)")
    
    print(f"\nP&L sobre 100 órdenes:")
    print(f"  Ingresos: ${p['ingresos']:,.0f}")
    print(f"  Costo producto: ${p['costo_producto_total']:,.0f}")
    print(f"  Fletes total: ${p['fletes_total']:,.0f}")
    print(f"  Margen pre-pauta: ${p['margen_pre_pauta']:,.0f} ({p['margen_pre_pauta_pct']}%)")
    
    print(f"\n>>> CPA BREAKEVEN: ${ue['cpa_breakeven']:,.0f}")
    print(f">>> ROAS breakeven: {ue['roas_breakeven']}x")
    print(f">>> Margen por entrega real: ${ue['margen_por_entregada']:,.0f}")
    
    print(f"\nCPA objetivo según margen neto deseado:")
    for k, v in ue['cpa_por_margen_objetivo'].items():
        pct = k.replace('margen_', '').replace('pct', '')
        print(f"  Margen {pct}% → CPA máx ${v['cpa_max']:,.0f} | ROAS {v['roas_objetivo']}x")


if __name__ == '__main__':
    # Ejemplo genérico: producto COD con cancelaciones sin costo
    print("EJEMPLO: Producto COD")
    ue = calculate_unit_economics(
        precio=75000,
        costo_producto=15000,
        flete_entregada=17000,
        flete_fallida=12000,
        tasa_cancelacion=0.10,
        tasa_devolucion=0.25,
        base_devolucion='enviadas',
        producto_recuperable=True,
        costo_cancelacion=0
    )
    print_summary(ue)
    
    print("\n\nEvaluación CPA $22,000:")
    tier, desc, margen = evaluar_cpa(22000, ue)
    print(f"  {tier} | {desc} | Margen ${margen:,.0f}/compra")
