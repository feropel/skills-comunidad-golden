#!/usr/bin/env python3
"""
metricas_saturacion.py — cálculo determinista de cobertura y cementerio
(golden-productos-ganadores). Evita el error de redondeo/memoria al hacerlo
a mano cada corrida. Ver references/ad-library-metodo.md §2 y §4 para la
definición de cada métrica.

Uso:
  python3 metricas_saturacion.py cobertura --reportado 1496 --revisados 50
  python3 metricas_saturacion.py cementerio --activos 1496 --historicos 2014

Salida: JSON de una línea, listo para pegar en la ficha.
"""
import argparse
import json
import sys


def cobertura(reportado: int, revisados: int) -> dict:
    if reportado < 0 or revisados < 0:
        raise ValueError("reportado y revisados deben ser >= 0")
    if revisados > reportado:
        # el propio MCP puede reportar un total desactualizado; no es un error duro
        pct = 100.0
    elif reportado == 0:
        pct = 0.0
    else:
        pct = round(revisados / reportado * 100, 1)
    if pct >= 70:
        confianza = "Alta"
    elif pct >= 40:
        confianza = "Media"
    else:
        confianza = "Baja"
    return {
        "metrica": "cobertura",
        "reportado_por_meta": reportado,
        "revisados": revisados,
        "sin_revisar": max(reportado - revisados, 0),
        "cobertura_pct": pct,
        "confianza": confianza,
    }


def cementerio(activos: int, historicos: int) -> dict:
    if activos < 0 or historicos < 0:
        raise ValueError("activos y historicos deben ser >= 0")
    if historicos == 0:
        return {
            "metrica": "cementerio",
            "activos": activos,
            "historicos": historicos,
            "apagados": 0,
            "supervivencia_pct": None,
            "lectura": "sin datos históricos — no concluir",
        }
    apagados = historicos - activos
    pct = round(activos / historicos * 100, 1)
    if historicos < 30:
        lectura = "muestra <30 históricos — no concluir, ratio no significativo"
    elif pct > 70:
        lectura = "categoría sana: quien entra, se queda"
    elif pct >= 40:
        lectura = "normal, hay rotación de testeo"
    else:
        lectura = "🚩 cementerio: mucha gente probó y apagó. Bandera roja"
    return {
        "metrica": "cementerio",
        "activos": activos,
        "historicos": historicos,
        "apagados": apagados,
        "supervivencia_pct": pct,
        "lectura": lectura,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="modo", required=True)

    pc = sub.add_parser("cobertura", help="cobertura de keywords revisadas vs reportadas por Meta")
    pc.add_argument("--reportado", type=int, required=True, help="estimated_total_count de Meta")
    pc.add_argument("--revisados", type=int, required=True, help="cuántos anuncios se revisaron uno a uno")

    pt = sub.add_parser("cementerio", help="tasa de supervivencia activos vs históricos")
    pt.add_argument("--activos", type=int, required=True, help="ad_active_status=ACTIVE, limit:1 -> estimated_total_count")
    pt.add_argument("--historicos", type=int, required=True, help="ad_active_status=ALL, limit:1 -> estimated_total_count")

    args = p.parse_args()

    try:
        if args.modo == "cobertura":
            out = cobertura(args.reportado, args.revisados)
        else:
            out = cementerio(args.activos, args.historicos)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
