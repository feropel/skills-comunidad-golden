"""
trm_resolver.py — Resuelve la TRM USD→COP a aplicar en el análisis.

ORDEN DE PRIORIDAD:
1. Si el usuario provee una TRM explícita → usar esa.
2. Si Claude tiene acceso a web → debe consultar "dólar a peso colombiano hoy"
   con la herramienta web_search y pasar el valor a esta función.
3. Si no hay acceso a internet → fallback a $4,000 COP/USD (conservador) y
   AVISAR EXPLÍCITAMENTE al usuario que se aplicó tasa de referencia.

Este módulo NO consulta la web por sí solo — Claude (el modelo) es quien tiene
la herramienta web_search. Este módulo registra qué tasa se usó y de qué fuente,
para que el reporte pueda decirlo con honestidad.

Uso típico:

    # Si Claude pudo consultar web_search:
    trm = resolve_trm(valor_de_web_search=4180)
    # → {"valor": 4180, "fuente": "web_search", "es_referencia": False}

    # Si Claude no pudo (sin internet o tool no disponible):
    trm = resolve_trm()
    # → {"valor": 4000, "fuente": "fallback_4000", "es_referencia": True}

    # Si el usuario explícitamente dio una TRM:
    trm = resolve_trm(valor_provisto_usuario=4150)
    # → {"valor": 4150, "fuente": "usuario", "es_referencia": False}
"""

FALLBACK_TRM = 4000.0  # COP/USD — conservador, validado con el equipo Golden Group


def resolve_trm(valor_de_web_search=None, valor_provisto_usuario=None):
    """
    Resuelve la TRM a usar y registra de dónde viene.

    Args:
        valor_de_web_search: TRM numérica obtenida por Claude vía web_search,
                             típicamente buscando "dólar a peso colombiano hoy".
                             None si Claude no pudo consultar.
        valor_provisto_usuario: TRM que el usuario indicó explícitamente.

    Returns:
        dict con:
            valor (float): TRM a aplicar en COP por USD
            fuente (str): "usuario" | "web_search" | "fallback_4000"
            es_referencia (bool): True si es el fallback (no tasa real del día)
            mensaje_usuario (str): texto listo para mostrarle al usuario
    """
    # Prioridad 1: input del usuario
    if valor_provisto_usuario is not None:
        v = float(valor_provisto_usuario)
        return {
            "valor": v,
            "fuente": "usuario",
            "es_referencia": False,
            "mensaje_usuario": f"Aplicando TRM ${v:,.0f} COP/USD según indicación del usuario."
        }

    # Prioridad 2: web search
    if valor_de_web_search is not None:
        v = float(valor_de_web_search)
        return {
            "valor": v,
            "fuente": "web_search",
            "es_referencia": False,
            "mensaje_usuario": f"Aplicando TRM ${v:,.0f} COP/USD (tasa real del día, consultada en internet)."
        }

    # Fallback
    return {
        "valor": FALLBACK_TRM,
        "fuente": "fallback_4000",
        "es_referencia": True,
        "mensaje_usuario": (
            f"⚠ No se pudo consultar la TRM real del día. Aplicando tasa de referencia "
            f"${FALLBACK_TRM:,.0f} COP/USD (conservadora). Si necesitas precisión exacta, "
            f"indica la TRM del día manualmente."
        )
    }


def convertir_usd_a_cop(valor_usd, trm_dict):
    """
    Convierte un valor de USD a COP usando el dict producido por resolve_trm.

    Args:
        valor_usd: número o iterable de números.
        trm_dict: output de resolve_trm()

    Returns:
        Valor (o lista) convertido a COP.
    """
    trm = trm_dict["valor"]
    if hasattr(valor_usd, '__iter__') and not isinstance(valor_usd, str):
        return [float(x) * trm for x in valor_usd]
    return float(valor_usd) * trm


def convertir_dataframe_usd_a_cop(df, columnas, trm_dict):
    """
    Convierte columnas de un DataFrame de USD a COP in-place.

    Args:
        df: pandas DataFrame
        columnas: lista de nombres de columna a convertir
        trm_dict: output de resolve_trm()
    """
    trm = trm_dict["valor"]
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype(float) * trm
    return df


if __name__ == "__main__":
    # Tests
    print("Caso 1 — Claude consultó la web:")
    r = resolve_trm(valor_de_web_search=4180)
    print(f"  {r}")

    print("\nCaso 2 — Sin acceso a internet:")
    r = resolve_trm()
    print(f"  {r}")

    print("\nCaso 3 — Usuario dio TRM:")
    r = resolve_trm(valor_provisto_usuario=4150)
    print(f"  {r}")

    print("\nConversión 1000 USD con fallback:")
    trm = resolve_trm()
    print(f"  ${convertir_usd_a_cop(1000, trm):,.0f} COP")
