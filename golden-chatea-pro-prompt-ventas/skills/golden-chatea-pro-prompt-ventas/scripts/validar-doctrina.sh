#!/usr/bin/env bash
# Mide un PROMPT DE VENTA contra las varas de la doctrina Golden (FER 2026-09-02).
# NO mide identidad (marca, tono, país): la identidad DEBE variar entre espacios.
# Mide que estén los TRAMOS DEL PROCESO PERSUASIVO. Bloquea (exit 3) si falta un tramo crítico.
# Uso: bash validar-doctrina.sh <archivo.txt>   ·   bash validar-doctrina.sh --vara <archivo.md>
set -uo pipefail
VARA=""; FILE=""
for a in "$@"; do case "$a" in --vara) VARA=1 ;; *) FILE="$a" ;; esac; done
[ -z "$FILE" ] || [ ! -f "$FILE" ] && { echo "❌ Uso: bash validar-doctrina.sh [--vara] <archivo>"; exit 1; }

python3 - "$FILE" "$VARA" << 'PY'
import sys, re
path, vara = sys.argv[1], sys.argv[2] == "1"
t = open(path, encoding="utf-8", errors="replace").read()
if vara:
    m = re.search(r"```\n(.*?)```", t, re.S)
    if not m: print("❌ --vara: no encontré bloque de prompt."); sys.exit(1)
    t = m.group(1)
import unicodedata
def norm(x):
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(c for c in x if unicodedata.category(c) != "Mn")
T = norm(t)   # sin tildes y en minúscula: el registro y la acentuación NO son doctrina

# CRÍTICOS: sin esto el prompt informa pero no vende
crit = [
 ("DIAGNOSTICO — pregunta la causa/necesidad", ["te hizo buscar","lo hizo buscar","la hizo buscar","que problema","es lo principal","cuentame","cuenteme","buscas resolver","busca resolver","te gustaria mejorar","le gustaria mejorar","que necesitas","que necesita"]),
 ("PERSUASIÓN — beneficio/deseo, no solo ficha", ["para que puedas","para que pueda","beneficio","te ayuda","le ayuda","resultado","deseo"]),
 ("PRECIO/OFERTA — presenta opciones y precio", ["precio","hoy:","$","opciones","unidad"]),
 ("OBJECIONES — al menos las de fondo", ["objeci","esta caro","funciona","es seguro","lo voy a pensar","desconf","pensarlo"]),
 ("CIERRE — resumen y confirmación explícita", ["responde si","confirmo asi","todo esta correcto","resumen","confirmar","confirmas"]),
 ("CAPTURA — pide los datos del pedido", ["nombre completo","dirección","ciudad","datos"]),
]
# ESPERADOS: doctrina completa (no bloquean, restan)
esp = [
 ("RAZÓN DE PREFERENCIA — por qué a nosotros", ["por que a nosotros","original","pagas al recibir","paga al recibir","garantia de cambio","revisas antes de pagar","revisa antes de pagar","por que con nosotros","respaldo","acompanamiento"]),
 ("PRUEBA — testimonios, casos o antes/después", ["testimonio","caso de","antes y después","antes/después","clientes"]),
 ("TRAMO LOGÍSTICO — confirmación y expectativa", ["días hábiles","llega a","pagas al recibir","entrega"]),
 ("POSTVENTA / REACTIVACIÓN", ["como te fue","como le fue","seguimiento","recompra","postventa","novedad"]),
]
# ANTIPATRONES: lo que la doctrina prohíbe
anti = [
 ("urgencia inventada / escasez sin respaldo", [r"promo\s+(de|es de)\s+hoy", r"(ultim[ao]s?|quedan?)\s+\w*\s*unidad", r"solo por hoy", r"se (vence|acaba|agota) hoy", r"el precio sube", r"te lo apart", r"antes de que se agote"]),
 ("testimonio o prueba fabricada", [r"nombres?\s+fals", r"testimonios?\s+(fals|inventad)", r"chat\s+fals", r"captura[s]?\s+(fals|inventad|generad)", r"inventa\s+(un|dos|tres|el)?\s*(testimonio|caso|cliente)"]),
 ("precio Antes inflado (descuento falso)", [r"antes\s+lo\s+(sub|infl)", r"para que el descuento se vea", r"precio\s+antes\s+infl"]),
 ("claim regulatorio falso", [r"(aprobad|avalad|certificad)[oa]s?\s+por\s+la\s+fda", r"fda\s+aprob", r"avalad[oa]s?\s+por\s+(dermatolog|medic)"]),
 ("claim de cura o tratamiento", [r"(?<!no )(?<!nunca )(?<!ni )\bcura\b(?! ni)", r"(?<!no )(?<!puede )\bcurar\b", r"(?<!no )elimina la enfermedad", r"(?<!no )trata la enfermedad", r"garantiza(mos)? (la )?(curaci|sanaci)"]),
]
def hay(ks): return any(k in T for k in ks)
print("="*52); print(" VALIDADOR DE DOCTRINA — venta conversacional Golden"); print("="*52)
print(f" Archivo: {path}\n Nota: NO se evalúa identidad (marca/tono/país). Solo el PROCESO.\n")
faltan=[]; flojo=[]
print(" TRAMOS CRÍTICOS:")
for n,ks in crit:
    ok=hay(ks); print(f"   {'✅' if ok else '❌'} {n}")
    if not ok: faltan.append(n)
print("\n TRAMOS ESPERADOS:")
for n,ks in esp:
    ok=hay(ks); print(f"   {'✅' if ok else '⚠️ '} {n}")
    if not ok: flojo.append(n)
print("\n ANTIPATRONES:")
malos=[]
for n,ps in anti:
    hit=[p for p in ps if re.search(p,T)]
    if hit: malos.append(n); print(f"   ❌ {n}")
if not malos: print("   ✅ ninguno detectado")
print("\n"+"-"*52)
if faltan or malos:
    print(" ❌ BLOQUEADO — este prompt informa pero no cumple la doctrina:")
    for f in faltan: print(f"   · FALTA tramo crítico: {f}")
    for m in malos: print(f"   · ANTIPATRÓN: {m}")
    sys.exit(3)
if flojo:
    print(f" ⚠️  PASA con {len(flojo)} tramo(s) esperado(s) ausente(s):")
    for f in flojo: print(f"   · {f}")
    sys.exit(0)
print(" ✅ CUMPLE LA DOCTRINA — todos los tramos del proceso persuasivo presentes.")
sys.exit(0)
PY
