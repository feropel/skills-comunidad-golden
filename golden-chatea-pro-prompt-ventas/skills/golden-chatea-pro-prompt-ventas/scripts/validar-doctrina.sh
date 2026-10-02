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
 ("CAPTURA — pide los datos del pedido", ["nombre completo","direccion","ciudad","datos"]),
]
# ESPERADOS: doctrina completa (no bloquean, restan)
esp = [
 ("RAZÓN DE PREFERENCIA — por qué a nosotros", ["por que a nosotros","original","pagas al recibir","paga al recibir","garantia de cambio","revisas antes de pagar","revisa antes de pagar","por que con nosotros","respaldo","acompanamiento"]),
 ("PRUEBA — testimonios, casos o antes/después", ["testimonio","caso de","antes y despues","antes/despues","clientes"]),
 ("TRAMO LOGÍSTICO — confirmación y expectativa", ["dias habiles","llega a","pagas al recibir","entrega"]),
 ("POSTVENTA / REACTIVACIÓN", ["como te fue","como le fue","seguimiento","recompra","postventa","novedad"]),
]
# ANTIPATRONES: lo que la doctrina prohíbe
anti = [
 ("urgencia inventada / escasez sin respaldo", [r"promo\s+(de|es de)\s+hoy", r"(ultim[ao]s?|quedan?)\s+\w*\s*unidad", r"solo por hoy", r"se (vence|acaba|agota) hoy", r"el precio sube", r"te lo apart", r"antes de que se agote"]),
 ("testimonio o prueba fabricada", [r"nombres?\s+fals", r"testimonios?\s+(fals|inventad)", r"chat\s+fals", r"captura[s]?\s+(fals|inventad|generad)", r"inventa\s+(un|dos|tres|el)?\s*(testimonio|caso|cliente)"]),
 ("precio Antes inflado (descuento falso)", [r"antes\s+lo\s+(sub|infl)", r"para que el descuento se vea", r"precio\s+antes\s+infl"]),
 ("claim regulatorio falso", [r"(aprobad|avalad|certificad)[oa]s?\s+por\s+la\s+fda", r"fda\s+aprob", r"avalad[oa]s?\s+por\s+(dermatolog|medic)"]),
 ("claim de cura o tratamiento", [r"(?<!no )(?<!nunca )(?<!ni )\bcura\b(?! ni)", r"(?<!no )(?<!puede )\bcurar\b", r"(?<!no )elimina la enfermedad", r"(?<!no )trata la enfermedad", r"garantiza(mos)? (la )?(curaci|sanaci)"]),
 # LEY DEL CLAIM ACOTADO (v3.45.0): el superlativo absoluto lo dice el que vende, asi que el cliente lo descuenta
 # solo. Se caza el ABSOLUTO, no el dato acotado: "mas vendido EN BOGOTA EL MES PASADO" debe pasar, "somos el
 # numero 1" no. Por eso cada patron exige la marca de totalidad (del mercado, del pais, todos, miles) o el
 # superlativo desnudo, y lleva lookahead negativo para no morder la version acotada.
 # 🔴 v3.46.0: estos patrones estaban SIN ANCLAR y cazaban "la mejor recomendacion" y "la mejor oferta",
 # que la propia skill ORDENA escribir (SKILL.md, plantilla-prompt.md, objeciones.md). El superlativo solo
 # es un claim cuando se mide contra EL MERCADO o contra TODOS; "la mejor opcion para ti" es asesoria.
 # Por eso cada superlativo exige ahora su anclaje comparativo explícito.
 # SALUDO ROBOTICO (v3.53.0, doctrina de JuanMa Gaviria). "En que le puedo servir/ayudar/colaborar"
 # falla por tres razones a la vez: lo puede decir un robot, es una BARRERA (la respuesta natural es
 # "no, gracias") e ignora que la persona ya vio el anuncio y viene pensando en el producto.
 # El saludo va a lo unico que comparten comprador y vendedor: EL PRODUCTO.
 # Se exige la formula completa (verbo de servicio + "puedo"), no la palabra suelta, para no morder
 # un "cuentame como te puedo ayudar a elegir la talla", que si es legitimo y especifico.
 ("saludo robotico de mostrador", [
   r"\ben\s+que\s+(te|le|los|las)\s+(puedo|podemos)\s+(servir|ayudar|colaborar|asistir)\b",
   r"\bcomo\s+(te|le)\s+(puedo|podemos)\s+(servir|colaborar)\b",
   r"\bestamos\s+para\s+servirle\b",
 ]),
 ("claim absoluto / superlativo sin acotar", [
   r"\b(somos|son|es)\s+(el|la|los|las)\s+(marca\s+)?(numero|n\.?\s?)\s*(1|uno)\b",
   r"\b(el|la)\s+(mejor|unic[oa])\s+\w*\s*(del\s+mercado|del\s+pais|de\s+colombia|de\s+mexico|de\s+chile|del\s+mundo|que\s+existe|de\s+todos)\b",
   r"\bmiles\s+de\s+(clientes|personas|usuarios)\s+(satisfech|content|felic)",
   r"\b(lider|lideres|los\s+numero\s+uno)\s+(del|en\s+el)\s+mercado\b",
   r"\b100\s*%\s+garantizad",
   r"\bgarantia\s+en\s+todos\s+(nuestros|los)\s+productos\b",
 ]),
]
# ENCABEZADOS que declaran el tramo por su nombre. Si el prompt titula una seccion
# "DIAGNOSTICO" o "REGLA DE DIAGNOSTICO", el tramo esta aunque el cuerpo lo diga
# con otras palabras. Se exige que el nombre viva SOLO en su linea (encabezado),
# no suelto en una frase, para no cazar "sin diagnostico medico".
ENCAB = {
 "DIAGNOSTICO": [r"^[^a-z0-9]{0,4}(regla\s+de\s+|paso\s*\d*\s*[-:.]?\s*)?diagnostico\b.{0,40}$"],
 "PERSUASI": [r"^[^a-z0-9]{0,4}(regla\s+de\s+|paso\s*\d*\s*[-:.]?\s*)?persuasi[oó]n\b.{0,40}$"],
 "OBJECIONES": [r"^[^a-z0-9]{0,4}(manejo\s+de\s+)?objeciones\b.{0,40}$"],
 "CIERRE": [r"^[^a-z0-9]{0,4}(paso\s*\d*\s*[-:.]?\s*)?cierre\b.{0,40}$"],
}
# CONCEPTO: preguntar ANTES de recomendar. Independiente de como se redacte la
# pregunta concreta, que es justo lo que cambia de un producto a otro.
CONCEPTO = {
 "DIAGNOSTICO": [
   r"pregunta[^.]{0,60}antes de (recomendar|proponer|ofrecer)",
   r"(nunca|no) (recomiendes|recomendar|propongas|ofrezcas)[^.]{0,30}(a ciegas|sin saber|sin preguntar)",
   r"si no sabes (que|qu[eé])[^.]{0,40}(lo|la|le) (trae|busca|necesita)",
   r"antes de recomendar[^.]{0,40}pregunta",
 ],
}
LINEAS = [l.strip() for l in T.split("\n") if l.strip()]

def por_encabezado(nombre):
    for clave, pats in ENCAB.items():
        if clave in nombre.upper():
            return any(re.search(p, l, re.I) for p in pats for l in LINEAS)
    return False

def por_concepto(nombre):
    for clave, pats in CONCEPTO.items():
        if clave in nombre.upper():
            return any(re.search(p, T, re.I) for p in pats)
    return False

def hay(ks, nombre=""):
    if any(k in T for k in ks):
        return True
    return por_encabezado(nombre) or por_concepto(nombre)
print("="*52); print(" VALIDADOR DE DOCTRINA — venta conversacional Golden"); print("="*52)
print(f" Archivo: {path}\n Nota: NO se evalúa identidad (marca/tono/país). Solo el PROCESO.\n")
faltan=[]; flojo=[]
print(" TRAMOS CRÍTICOS:")
for n,ks in crit:
    ok=hay(ks, n); print(f"   {'✅' if ok else '❌'} {n}")
    if not ok: faltan.append(n)
print("\n TRAMOS ESPERADOS:")
for n,ks in esp:
    ok=hay(ks, n); print(f"   {'✅' if ok else '⚠️ '} {n}")
    if not ok: flojo.append(n)
print("\n ANTIPATRONES:")
malos=[]
# 🔴 REPARACIÓN v3.46.0 (verificador adversarial: 8 de 8 inyecciones de texto OBLIGATORIO de la skill
# daban exit 3, y la propia vara mínima estaba BLOQUEADA). CAUSA DE CLASE: los antipatrones se buscaban
# sobre el texto entero, así que la frase que PROHÍBE una práctica disparaba igual que la práctica.
# "NUNCA inventes que quedan pocas unidades" contiene "quedan pocas unidades".
# ARREGLO DE CLASE: se evalúa LÍNEA A LÍNEA y se saltan las líneas que son una PROHIBICIÓN.
# Los marcadores son explícitos a propósito: un "no" suelto NO alcanza, porque "no te quedes sin stock,
# ultimas unidades" es copy de venta real y tiene que seguir cazándose.
PROHIBICION = re.compile(
    r"(nunca|jamas|prohibid|linea roja|antipatron|no digas|no afirmes|no inventes|no uses|no prometas|"
    r"no menciones|no se puede|no vale|evita|evitar|esta mal|es falso|es mentira|en vez de|sin respaldo|"
    r"o no existe|debe ser cierta|tiene que ser cierta)"
)
# 🔴 REPARACIÓN v3.54.0 — LA PROHIBICIÓN TAMBIÉN SE DECLARA COMO ENCABEZADO DE SECCIÓN.
# Medido contra los prompts VIVOS del espacio Golden: 7 de 8 productos daban "claim de cura"
# y los 7 eran FALSOS POSITIVOS MÍOS. El prompt real dice:
#     L78: PROHIBIDO
#     L79: Prometer crecimiento de cabello, cura de la alopecia o resultados medicos.
# La palabra que prohíbe está en el ENCABEZADO y lo prohibido va listado debajo. Mirando solo
# la línea, la L79 parece un claim de cura cuando es justo lo contrario.
# ARREGLO DE CLASE: el alcance de una prohibición se ARRASTRA hacia abajo hasta que termina la
# sección (línea en blanco). Es la misma clase que ya me mordió dos veces: el detector acusa al
# idioma cuando no entiende la ESTRUCTURA del texto, no solo sus palabras.
# 🔴 REPARACIÓN v3.64.0 — EL ARREGLO DE v3.54.0 ABRIÓ UN CORREDOR CIEGO (fila P59 del CdM).
# El arrastre de arriba no distinguía un ENCABEZADO que prohíbe de una línea de COPY que
# casualmente lleva una palabra de prohibición dentro. Medido sobre la vara mínima, que pasa
# limpia: añadirle "Evita la caída del cabello y recupera densidad en semanas." y debajo
# "quedan pocas unidades, solo por hoy" daba **exit 0 y ANTIPATRONES: ✅ ninguno detectado**.
# Sin la línea del "Evita", la misma escasez se cazaba. Una frase de venta cualquiera abría un
# pasillo por el que entraba la mentira, y el validador certificaba CUMPLE.
# Es el FALLO SIMÉTRICO de la corrección anterior: arreglar el falso positivo creó el falso
# negativo, que es el peor de los dos porque un "no hay nada" se cree igual que un hallazgo.
#
# ARREGLO: la prohibición SIEMPRE exime su PROPIA línea (eso es lo correcto de v3.46.0), pero
# solo ARRASTRA el alcance hacia abajo cuando la línea es de verdad un ENCABEZADO:
#   · queda en ≤3 palabras al quitarle el marcador (el caso vivo "PROHIBIDO"), o
#   · termina en ":" porque anuncia una lista ("⛔ NUNCA digas:"), o
#   · abre con un emoji de prohibición, o va toda en MAYÚSCULAS (los títulos de estos prompts).
# Así el caso vivo de v3.54.0 (L78 "PROHIBIDO" / L79 lo prohibido debajo) sigue sin dar falso
# positivo, y una frase de copy ya no tapa lo que viene después.
_EMOJI_PROH = ("⛔", "🚫", "🔴", "❌")


def _es_encabezado(l):
    s = l.strip()
    if s.endswith(":"):
        return True
    if s.startswith(_EMOJI_PROH):
        return True
    _letras = [c for c in s if c.isalpha()]
    if _letras and all(c.isupper() for c in _letras):
        return True
    # lo que queda al quitarle el marcador y la puntuación: un título no deja frase detrás
    _resto = PROHIBICION.sub(" ", s)
    _resto = re.sub(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", " ", _resto)
    return len([p for p in _resto.split() if len(p) > 1]) <= 3


lineas_crudas = T.split("\n")
en_prohibicion = False
lineas = []
excluidas = []                           # nada se excluye en silencio
for l in lineas_crudas:
    if not l.strip():
        en_prohibicion = False           # la línea en blanco cierra la sección
        continue
    if PROHIBICION.search(l):
        # arrastra SOLO si es un encabezado; si es copy, se exime ella y nada más
        en_prohibicion = _es_encabezado(l)
        excluidas.append(("encabezado" if en_prohibicion else "prohibe en la linea",
                          l.strip()[:80]))
        continue
    if en_prohibicion:
        excluidas.append(("bajo encabezado", l.strip()[:80]))
    lineas.append(("PROH" if en_prohibicion else "VIVA", l))

for n, ps in anti:
    culpable = None
    for clase, l in lineas:
        if clase == "PROH":
            continue                      # está bajo un encabezado que la prohíbe
        if any(re.search(p, l) for p in ps):
            culpable = l.strip()[:90]
            break
    if culpable:
        malos.append(n)
        print(f"   ❌ {n}")
        print(f"        └ línea: \"{culpable}\"")
if not malos: print("   ✅ ninguno detectado")
# 🔴 EL VEREDICTO VIENE CON SU COBERTURA (fila P59): un "ninguno detectado" sobre un texto del
# que se excluyeron líneas no es lo mismo que sobre el texto entero. Se declara SIEMPRE, y se
# nombran, porque una exclusión que no se ve es la que esconde el hallazgo.
if excluidas:
    print(f"   ⚠️  {len(excluidas)} líneas excluidas del barrido de antipatrones "
          f"(de {len(lineas)+len(excluidas)} con contenido):")
    for _razon, _l in excluidas[:12]:
        print(f"        · [{_razon}] \"{_l}\"")
    if len(excluidas) > 12:
        print(f"        · … y {len(excluidas)-12} más")
else:
    print(f"   · cobertura: {len(lineas)} de {len(lineas)} líneas con contenido barridas")
# 🔴 LA COLA EXENTA (medido el 2026-09-28 sobre los 15 prompts vivos del espacio Golden: 8 de 15
# terminan asi). Si el prompt ACABA dentro de una seccion de prohibicion —una lista de "NUNCA
# hagas esto" sin linea en blanco despues—, todo lo que se le AÑADA luego cae dentro de esa
# seccion y nace exento. Y por el panel se edita añadiendo al final, que es justo ahi.
# No es un fallo del prompt ni se bloquea: es un aviso de forma, y se arregla con una linea en
# blanco al final o cerrando con una instruccion que no prohíba.
# ⚠️ Y OJO CON EL \n DE CIERRE DEL FICHERO, que me mordió montando esto: `T.split("\n")` deja un
# "" final que NO es una línea en blanco del autor, sino el salto que cierra el archivo. Leyendo
# el flag después del bucle, ese "" cerraba la sección siempre y el aviso no salía nunca (caso 21
# del banco en rojo, caso 22 en verde: muerto en un solo sentido). Se descuenta UN solo "" final.
_c = T.split("\n")
if T.endswith("\n") and _c and _c[-1] == "":
    _c.pop()
_en = False
for _l in _c:
    if not _l.strip():
        _en = False
    elif PROHIBICION.search(_l):
        _en = _es_encabezado(_l)
if _en and lineas:
    print("   ⚠️  EL PROMPT TERMINA DENTRO DE UNA SECCIÓN DE PROHIBICIÓN: todo lo que se le")
    print("        añada después (y por el panel se añade AL FINAL) nacerá exento del barrido.")
    print("        Cierra la sección con una línea en blanco antes de entregar.")
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
