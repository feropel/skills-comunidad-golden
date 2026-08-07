#!/usr/bin/env bash
# Validador de prompts Chatea PRO — cuenta caracteres y despliega la checklist de apoyo para la evaluación holística.
# Uso: bash validar.sh <archivo-del-prompt.txt> [limite]
# El límite por defecto es 10000 (techo de trabajo). El campo acepta hasta 12000.

set -euo pipefail
FILE="${1:-}"
LIMIT="${2:-10000}"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "❌ Uso: bash validar.sh <archivo-del-prompt.txt> [limite]"
  exit 1
fi

CHARS=$(wc -m < "$FILE" | tr -d ' ')
echo "════════════════════════════════════════════"
echo " VALIDADOR CHATEA PRO"
echo "════════════════════════════════════════════"
echo " Archivo:     $FILE"
echo " Caracteres:  $CHARS"
echo " Límite:      $LIMIT (máx del campo: 12000)"
if [ "$CHARS" -le "$LIMIT" ]; then
  echo " Estado:      ✅ DENTRO del límite ($((LIMIT - CHARS)) de margen)"
else
  echo " Estado:      ❌ EXCEDE por $((CHARS - LIMIT)) — RECORTAR antes de entregar"
fi
echo "════════════════════════════════════════════"
echo " CHECKLIST DE APOYO (guía tu juicio; la nota /100 es holística, NO una suma):"
echo "  [ ] 15  Precio inmediato sin esconder"
echo "  [ ] 15  Pago anticipado blindado (sin comprobante NO confirma)"
echo "  [ ] 12  Captura en un mensaje + anti-error"
echo "  [ ] 10  Objeciones cubiertas (caro/funciona/seguro/médico/pensar)"
echo "  [ ] 10  Espeja el dolor antes de vender"
echo "  [ ]  8  Conteo de unidades/combos correcto"
echo "  [ ]  8  OFICINA según transportadora"
echo "  [ ]  8  Caracteres OK + URLs conversacionales adentro"
echo "  [ ]  7  Tono humano (<=35 palabras, <=2 emojis, no bot)"
echo "  [ ]  7  Upsell solo tras el cierre"
echo "  ─────────────────────────────────────────"
echo "  NOTA HOLÍSTICA: ___/100   y luego ___/1000 + qué falta para 1000"
echo "════════════════════════════════════════════"
