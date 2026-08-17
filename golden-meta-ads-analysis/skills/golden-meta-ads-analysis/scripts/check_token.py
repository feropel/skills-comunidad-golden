"""
check_token.py — Preflight de SEGURIDAD del Access Token (Modo B, en vivo).

Antes de bajar cualquier dato, verifica con el endpoint /debug_token de Meta que
el token sea SOLO-LECTURA. Aborta (exit 1) si detecta un scope de ESCRITURA
(`ads_management`), si el token es inválido/expiró, o si le falta `ads_read`.

Esto protege sobre todo a la comunidad: ningún usuario se auto-expone por generar
por error un token con más permisos de la cuenta. Un token solo-lectura, aunque se
filtre, no puede crear, pausar ni gastar — solo leer métricas.

Uso:
    python3 scripts/check_token.py
Lee META_ACCESS_TOKEN de env o del .env (vía _common.load_config).
"""

import sys
import json

from _common import load_config, BASE_URL  # noqa: E402

try:
    import requests
except ImportError:
    print("\n❌ Falta la librería `requests`.  → pip install requests\n")
    sys.exit(1)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Scopes que JAMÁS debe tener un token de análisis (permiten gastar / editar / pausar)
WRITE_SCOPES = {"ads_management", "business_management_write", "manage_pages"}
# Scope mínimo requerido para leer insights
REQUIRED_READ = "ads_read"


def main():
    cfg = load_config(required=("META_ACCESS_TOKEN",))
    token = cfg["access_token"]

    try:
        r = requests.get(
            f"{BASE_URL}/debug_token",
            params={"input_token": token, "access_token": token},
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"\n❌ No se pudo verificar el token (error de red): {e}")
        sys.exit(1)

    body = r.json()
    if "error" in body:
        msg = body["error"].get("message", "desconocido")
        print(f"\n❌ El token no se pudo validar: {msg}")
        print("   → Genera un System User Token solo-lectura (ver references/extraccion_en_vivo.md).")
        sys.exit(1)

    data = body.get("data", {})
    scopes = set(data.get("scopes", []))
    is_valid = data.get("is_valid", False)
    ttype = data.get("type", "DESCONOCIDO")

    # Persistir para trazabilidad (nunca guarda el token, solo el diagnóstico)
    diag = {
        "is_valid": is_valid,
        "type": ttype,
        "scopes": sorted(scopes),
        "expires_at": data.get("expires_at"),
        "data_access_expires_at": data.get("data_access_expires_at"),
    }
    with open("token_check.json", "w", encoding="utf-8") as f:
        json.dump(diag, f, indent=2, ensure_ascii=False)

    print("🔎 Verificación del token:")
    print(f"   Válido : {is_valid}")
    print(f"   Tipo   : {ttype}")
    print(f"   Scopes : {', '.join(sorted(scopes)) or '(ninguno)'}")

    # ── Reglas de bloqueo ──────────────────────────────────────────
    if not is_valid:
        print("\n❌ ABORTADO — el token es inválido o expiró. Genera uno nuevo.")
        sys.exit(1)

    offending = scopes & WRITE_SCOPES
    if offending:
        print(f"\n🚫 ABORTADO — el token tiene permiso(s) de ESCRITURA: {', '.join(sorted(offending))}.")
        print("   Esta skill SOLO analiza (lee). Un token de análisis nunca debe poder gastar,")
        print("   pausar ni editar campañas. Genera un System User Token con SOLO:")
        print("       ads_read, business_management")
        print("   y vuelve a intentar. (ver references/extraccion_en_vivo.md)")
        sys.exit(1)

    if REQUIRED_READ not in scopes:
        print(f"\n❌ ABORTADO — al token le falta el scope `{REQUIRED_READ}` (necesario para leer insights).")
        print("   Regenéralo con: ads_read, business_management.")
        sys.exit(1)

    # ── Advertencias no bloqueantes ────────────────────────────────
    if ttype != "SYSTEM_USER":
        print("\n⚠️  Advertencia: el token NO es de System User (parece personal/temporal).")
        print("   Funciona para probar, pero para uso continuo genera un System User Token")
        print("   (no expira y no arriesga tu cuenta personal). Ver references/extraccion_en_vivo.md.")

    print("\n✅ Token solo-lectura verificado. Seguro para continuar con la extracción.")
    sys.exit(0)


if __name__ == "__main__":
    main()
