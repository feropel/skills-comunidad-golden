#!/usr/bin/env bash
# Validador de prompts Chatea PRO — mide los DOS techos y BLOQUEA (exit != 0) si algo falla.
# Uso: bash validar.sh <archivo.txt> [límite_crudos]        → valida un PROMPT (límite default 12000, objetivo 9000-11000)
#      bash validar.sh --activador <archivo.txt>            → valida un ACTIVADOR (0 emojis de CUALQUIER tipo, sin BOM)
# Conteo por python (independiente del locale; wc -m cuenta BYTES bajo LC_CTYPE=C y miente).

set -uo pipefail
MODE="prompt"; FILE=""; LIMIT="12000"
for a in "$@"; do
  case "$a" in
    --activador) MODE="activador" ;;
    *) if [ -z "$FILE" ]; then FILE="$a"; elif [[ "$a" =~ ^[0-9]+$ ]]; then LIMIT="$a"; else
         echo "❌ Argumento inválido: '$a'. Uso: bash validar.sh [--activador] <archivo.txt> [límite numérico]"; exit 1; fi ;;
  esac
done
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "❌ Uso: bash validar.sh [--activador] <archivo.txt> [límite]"; exit 1
fi

python3 - "$FILE" "$LIMIT" "$MODE" << 'PY'
import json, sys
path, limit, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
data = open(path, "rb").read()
bom = data.startswith(b"\xef\xbb\xbf")
try:
    text = data.decode("utf-8-sig" if bom else "utf-8")
except UnicodeDecodeError:
    print("❌ El archivo NO es UTF-8 válido (típico al pegar desde Word/Excel).")
    print("   No se puede medir con seguridad: guárdalo como UTF-8 y vuelve a correr. NO entregues sin validar.")
    sys.exit(2)

raw = len(text)
escaped = len(json.dumps(text)[1:-1])  # default ensure_ascii=True: tilde=6, emoji=12 — la fórmula del briefing
four = sum(1 for c in text if ord(c) >= 0x10000)
# ACTIVADOR = WHITELIST (cierra la CLASE, no una lista de emojis): solo texto que un activador legítimo necesita.
# Todo lo demás (emojis de 3 o 4 bytes, keycaps, CJK, símbolos raros, BOM residual) queda fuera y bloquea.
ALLOWED = set(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áéíóúüñÁÉÍÓÚÜÑ.,;:()?!'\"$%+-/&#@_")
extranos = sorted({c for c in text.replace("\n", "").replace("\r", "") if c not in ALLOWED})

print("=" * 46)
print(" VALIDADOR CHATEA PRO — modo:", mode.upper())
print("=" * 46)
print(f" Archivo:    {path}")
print(f" Crudos:     {raw}")
print(f" Escapados:  {escaped}  (techo bot field legacy: <19.000; pasarse mata el producto SIN error visible)")
print(f" 4 bytes:    {four}   BOM: {'SÍ' if bom else 'no'}")

fails = []
if not text.strip():
    fails.append("El archivo está VACÍO (o solo espacios): no hay nada que validar.")

if mode == "activador":
    if bom:
        fails.append("El archivo trae BOM invisible (\\ufeff, típico de Word/Excel): rompe el match exacto del trigger. Guárdalo como UTF-8 sin BOM.")
    if extranos:
        muestra = " ".join(repr(c) for c in extranos[:8])
        fails.append(f"{len(extranos)} caracter(es) fuera de la lista permitida del activador: {muestra}. Un activador solo lleva letras, números y puntuación básica — los 4 bytes corrompen el trigger (probado) y CUALQUIER emoji o símbolo raro es riesgo: quítalos todos.")
    if not fails:
        print(" Estado:     ✅ ACTIVADOR VÁLIDO (solo texto permitido, sin BOM)")
else:
    if bom:
        print(" ⚠️ El archivo trae BOM (típico de Word). No bloquea el prompt, pero re-guárdalo como UTF-8 sin BOM antes de pegar.")
    if raw > limit:
        fails.append(f"EXCEDE el tope nativo del campo: {raw} > {limit} crudos (el panel corta al guardar). Recorta.")
    if escaped >= 19000:
        fails.append(f"EXCEDE el techo ESCAPADO del bot field: {escaped} >= 19.000 (probado en vivo: 19.895 dispara, 23.266 muere en silencio). Recorta tildes/emojis o texto.")
    if not fails:
        target = "dentro del objetivo 9.000-11.000" if 9000 <= raw <= 11000 else ("CORTO para el objetivo 9.000-11.000 (revisa qué venta falta: FAQ, objeciones, escenarios)" if raw < 9000 else "sobre el objetivo pero bajo el techo")
        print(f" Estado:     ✅ VÁLIDO — {raw}/{limit} crudos ({target}); escapado {escaped}/19.000")
        print(" Recuerda:   corre también `validar.sh --activador <archivo>` sobre CADA activador (ahí el veredicto exige 0 emojis).")

if fails:
    print(" Estado:     ❌ BLOQUEADO — corrige antes de entregar:")
    for f in fails: print(f"   · {f}")
    sys.exit(3)

if mode == "activador":
    sys.exit(0)

print("-" * 46)
print(" Checklist de apoyo (guía tu juicio holístico; la nota /100 NO es una suma):")
for item in [
    "Precio inmediato sin esconder",
    "Pago anticipado blindado (sin comprobante NO confirma)",
    "Captura en un mensaje + compuerta del resumen",
    "Objeciones cubiertas (caro/funciona/seguro/médico/pensar/otro producto)",
    "Espeja el dolor antes de vender",
    "Combos y matemática de upsell (costo incremental + beneficio)",
    "OFICINA según la política del negocio Y el país (México: no existe)",
    "Presupuesto aprovechado con sustancia, sin relleno",
    "Tono humano (≤35 palabras, ≤2 emojis, sin signos de apertura, nunca dice IA)",
    "Upsell solo tras el cierre · FAQ · cumplimiento sin claims",
]:
    print(f"   [ ] {item}")
print("   NOTA HOLÍSTICA: ___/100 y ___/1000 + qué falta para 1000")
PY
exit $?
