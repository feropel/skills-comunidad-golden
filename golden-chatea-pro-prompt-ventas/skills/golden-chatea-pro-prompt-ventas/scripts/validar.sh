#!/usr/bin/env bash
# Validador de prompts Chatea PRO — mide los DOS techos y BLOQUEA (exit != 0) si algo falla.
# Uso: bash validar.sh <archivo.txt> [límite_crudos]        → valida un PROMPT (límite default 12000, objetivo 9000-11800)
#      bash validar.sh --activador <archivo.txt>            → valida un ACTIVADOR (0 emojis de CUALQUIER tipo, sin BOM)
#      bash validar.sh --minimo <archivo.txt>               → juzga contra el rango de la VARA MÍNIMA VIABLE (4.000-6.000), no contra el de la completa
#      bash validar.sh --campo <tipo> <archivo.txt>          → valida un CAMPO VECINO contra SU tope: saludo/pregunta/remarketing 1.000 · recordatorio 800 · prompt-datos 4.000 · notificacion 400
#      bash validar.sh --vara <archivo.md>                  → extrae el bloque ``` del .md y mide SOLO el prompt entregable (la unidad autoritativa)
# Conteo por python (independiente del locale; wc -m cuenta BYTES bajo LC_CTYPE=C y miente).

set -uo pipefail
MODE="prompt"; FILE=""; LIMIT="12000"; MINOBJ=""; VARA=""; CAMPO=""
for a in "$@"; do
  case "$a" in
    --activador) MODE="activador" ;;
    --minimo) MINOBJ="1" ;;
    # v3.48.0 — TOPES DE LOS CAMPOS VECINOS. SKILL.md los declaraba desde siempre y el validador
    # NO tenia modo para ninguno: usaba 12.000 por defecto. Medido el dano: un saludo de 1.938 en un
    # tope de 1.000 (194%) pasaba con exit 0 Y el validador le decia al vendedor que estaba "CORTO"
    # y que anadiera contenido, a un campo que Chatea CORTA EN SILENCIO al guardar en el panel.
    --campo) CAMPO="NEXT" ;;
    --vara) VARA="1" ;;
    *) if [ "$CAMPO" = "NEXT" ]; then CAMPO="$a";
       elif [ -z "$FILE" ]; then FILE="$a"; elif [[ "$a" =~ ^[0-9]+$ ]]; then LIMIT="$a"; else
         echo "❌ Argumento inválido: '$a'. Uso: bash validar.sh [--activador] <archivo.txt> [límite numérico]"; exit 1; fi ;;
  esac
done
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "❌ Uso: bash validar.sh [--activador] <archivo.txt> [límite]"; exit 1
fi

case "$CAMPO" in
  saludo|mensaje-inicial) LIMIT="1000" ;;
  pregunta|pregunta-entrada) LIMIT="1000" ;;
  remarketing) LIMIT="1000" ;;
  recordatorio) LIMIT="800" ;;
  prompt-datos|producto-segundos) LIMIT="4000" ;;
  notificacion|notificaciones) LIMIT="400" ;;
  NEXT|"") : ;;
  *) echo "Campo desconocido: '$CAMPO'. Validos: saludo | pregunta | remarketing | recordatorio | prompt-datos | notificacion"; exit 1 ;;
esac
[ -n "$CAMPO" ] && [ "$CAMPO" != "NEXT" ] && MODE="campo:$CAMPO"

# 🔴 GUARDARRAIL v3.60.0 — el modo equivocado inventa hallazgos.
# Medido: correr el modo PROMPT sobre un recordatorio de 62 caracteres devolvio
# 6 bloqueos falsos (le exigia la regla de brevedad del prompt). Un archivo tan
# corto no puede ser un prompt: no le caben los tramos de la doctrina.
if [ "$MODE" = "prompt" ]; then
  N=$(wc -m < "$FILE" | tr -d ' ')
  if [ "$N" -lt 400 ]; then
    echo "❌ DEMASIADO CORTO PARA SER UN PROMPT: $N caracteres."
    echo "   Un prompt completo no baja de 400; esto es casi seguro un CAMPO VECINO."
    echo "   Corrigelo asi, con SU tope, y no con las reglas del prompt:"
    echo "     bash validar.sh --campo saludo|pregunta|remarketing|recordatorio|prompt-datos|notificacion \"$FILE\""
    echo "   Si de verdad es un prompt, esta incompleto: le faltan tramos."
    exit 1
  fi
fi

python3 - "$FILE" "$LIMIT" "$MODE" "$MINOBJ" "$VARA" << 'PY'
import json, re, sys
path, limit, mode = sys.argv[1], int(sys.argv[2]), sys.argv[3]
minimo = len(sys.argv) > 4 and sys.argv[4] == "1"
vara   = len(sys.argv) > 5 and sys.argv[5] == "1"
LO, HI = (4000, 6000) if minimo else (9000, 11800)   # 11.800 medido: con la doctrina completa (nivel de conciencia + 5 pasos + situaciones + escalada + tramo logístico) el prompt no cabe en 11.000; el techo del campo sigue siendo 12.000
data = open(path, "rb").read()
bom = data.startswith(b"\xef\xbb\xbf")
try:
    text = data.decode("utf-8-sig" if bom else "utf-8")
except UnicodeDecodeError:
    print("❌ El archivo NO es UTF-8 válido (típico al pegar desde Word/Excel).")
    print("   No se puede medir con seguridad: guárdalo como UTF-8 y vuelve a correr. NO entregues sin validar.")
    sys.exit(2)

if vara:
    # UNIDAD AUTORITATIVA = el PROMPT ENTREGABLE, no el archivo de documentación.
    # Extrae el primer bloque ``` del .md de la vara; sin esto se mide el .md entero
    # (anotaciones incluidas) y "cumple/no cumple" deja de significar lo mismo.
    import re as _re
    m = _re.search(r"```\n(.*?)```", text, _re.S)
    if not m:
        print("❌ --vara: no encontré un bloque ``` con el prompt en este archivo.")
        sys.exit(1)
    text = m.group(1)
    print(" (modo --vara: se mide SOLO el bloque de prompt, no el archivo completo)")

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
print(f" Escapados:  {escaped}  (INFORMATIVO: el tope NO se mide así. Medido en vivo 2026-09-05: son 20.000 puntos de código)")
print(f" 4 bytes:    {four}   BOM: {'SÍ' if bom else 'no'}")

fails = []
# 🔴 CANAL DE AVISOS (v3.49.0). Hasta hoy este validador era BINARIO: o bloqueaba o pasaba en
# verde. Sin un canal intermedio, todo lo que no se puede bloquear con certeza simplemente NO SE
# DICE — y lo que no se dice, no se revisa. Es la misma trampa de la lista blanca que calla: el
# silencio se lee como aprobación. Un aviso no frena la entrega; obliga a mirar.
avisos = []
if not text.strip():
    fails.append("El archivo está VACÍO (o solo espacios): no hay nada que validar.")

if mode == "activador":
    if bom:
        fails.append("El archivo trae BOM invisible (\\ufeff, típico de Word/Excel): rompe el match exacto del trigger. Guárdalo como UTF-8 sin BOM.")
    if extranos:
        muestra = " ".join(repr(c) for c in extranos[:8])
        fails.append(f"{len(extranos)} caracter(es) fuera de la lista permitida del activador: {muestra}. Un activador solo lleva letras, números y puntuación básica — los 4 bytes corrompen el trigger (probado) y CUALQUIER emoji o símbolo raro es riesgo: quítalos todos.")
    # GENÉRICO = NO ES ACTIVADOR (v3.45.0). Un activador dispara UN bot concreto; si es una frase que
    # cualquier cliente le escribe a cualquier tienda, choca con los demás bots de la cuenta y el disparo
    # se vuelve lotería. Se compara la cadena COMPLETA normalizada, nunca por substring: "INFO CEPILLO 360"
    # es legítimo aunque contenga "info", y debe pasar.
    import unicodedata as _ud
    _n = "".join(c for c in _ud.normalize("NFD", text.strip().lower()) if _ud.category(c) != "Mn")
    _n = " ".join("".join(ch for ch in _n if ch.isalnum() or ch.isspace()).split())
    GENERICOS = {
        "informacion", "info", "mas informacion", "quiero informacion", "quiero mas informacion",
        "necesito informacion", "info por favor", "hola", "buenas", "buenos dias", "buenas tardes",
        "precio", "precios", "cuanto cuesta", "quiero", "me interesa", "quiero comprar",
        "disponible", "disponibilidad", "pedido", "comprar",
        # v3.46.0: SKILL.md prohíbe "promo" POR NOMBRE y la lista no lo tenía.
        "promo", "promocion", "oferta", "ofertas", "catalogo", "mas info", "info porfa",
        "quiero saber mas", "interesado", "interesada", "cuanto vale",
    }
    # 🔴 FÓRMULA CANÓNICA DEL DISPARADOR (v3.49.0). El trigger casa BYTE A BYTE: un carácter de más
    # y el cliente cae en "Producto/Servicio no encontrado" → tablero "No automatizado", que no mira
    # nadie. Sin error visible y sin alerta: solo clientes que escribieron y nunca fueron atendidos.
    # SOLO se juzga la FAMILIA "Hola quiero informacion…", que es la del botón de tienda. Un activador
    # de otra forma ("QUIERO EL CEPILLO 360") es legítimo y no se toca — por eso la compuerta se
    # activa por el prefijo, no por parecido general.
    if _n.startswith("hola") and "informacion" in _n:
        _crudo = text.strip()
        _fallos = []
        if re.match(r"^\s*hola\s*,", _crudo, re.I):
            _fallos.append("lleva COMA después de 'Hola' (la fórmula no la tiene)")
        if "y precio" not in _n:
            _fallos.append("le falta 'y precio'")
        if _fallos:
            fails.append("DISPARADOR FUERA DE LA FÓRMULA CANÓNICA: " + " · ".join(_fallos) +
                         ". La fórmula casa BYTE A BYTE y es exactamente: \"Hola quiero información y precio de <PRODUCTO>\". "
                         "Un carácter de diferencia manda al cliente al tablero 'No automatizado', que nadie revisa: "
                         "no verás un error, verás menos ventas. Y recuerda que <PRODUCTO> se copia A MANO del bot field, "
                         "NUNCA del título comercial de la tienda — tomar el título automáticamente es lo que rompe el match.")
    if _n in GENERICOS:
        fails.append(f"ACTIVADOR GENÉRICO: '{text.strip()}' es una frase que cualquier cliente le escribe a cualquier tienda. El activador tiene que ser ÚNICO en la cuenta y nombrar el producto o la campaña (ej.: 'QUIERO EL CEPILLO 360'), porque si dos bots comparten disparador el match se vuelve lotería y contestan el que no era.")
    if not fails:
        print(" Estado:     ✅ ACTIVADOR VÁLIDO (solo texto permitido, sin BOM, no genérico)")
else:
    if bom:
        print(" ⚠️ El archivo trae BOM (típico de Word). No bloquea el prompt, pero re-guárdalo como UTF-8 sin BOM antes de pegar.")
    if raw > limit:
        fails.append(f"EXCEDE el tope nativo del campo: {raw} > {limit} crudos (el panel corta al guardar). Recorta.")

    # 🔴 v3.60.0 — GENERO ASIGNADO EN EL SALUDO (orden de FER 2026-09-22).
    # Solo aplica al campo SALUDO: en el prompt, "bienvenida" puede aparecer
    # dentro de una instruccion legitima sobre como tratar a una clienta.
    if mode == "campo:saludo":
        import re as _re
        _neutro = _re.compile(r"(?i)bienvenid[oa]\s*[/@]|bienvenid@|bienvenid[oa]\s*\(a\)")
        _genero = _re.compile(r"(?i)\b(bienvenid[oa]|querid[oa]|estimad[oa]|se[nñ]or[ae]?)\b")
        _m = _genero.search(text)
        if _m and not _neutro.search(text):
            fails.append(
                f"EL SALUDO LE ASIGNA GENERO AL CLIENTE: '{_m.group(0)}'. "
                "Lo compran hombres y mujeres, y ademas se compra de regalo. "
                "El que se siente en la conversacion equivocada no reclama: se va, "
                "y esa fuga no aparece en ninguna metrica. Tres salidas validas: "
                "(1) saluda al PRODUCTO y no a la persona, que es la doctrina y no "
                "necesita genero ('Hola! Te muestro el <producto>'); "
                "(2) usa el NOMBRE del cliente; "
                "(3) forma neutra explicita ('Bienvenido/a', 'Bienvenid@').")
    # 🔴 CORREGIDO v3.46.0 CON MEDICIÓN EN VIVO (espacio f218311, 2026-09-05, escribiendo y releyendo
    # del servidor). Lo anterior decía "techo ESCAPADO <19.000, probado en vivo" y era FALSO en la
    # unidad Y en el número: 20.000 tildes (=120.000 escapados) sobrevivieron intactas, y 20.000 emojis
    # (=80.000 bytes) también. El tope real son 20.000 PUNTOS DE CÓDIGO y nada más cuenta.
    # Frontera medida: 20.000 pasa, 20.001 se corta. Un emoji de 4 bytes cuenta 1, no 2.
    # El corte es SILENCIOSO: HTTP 200 y el valor guardado exactamente en 20.000.
    if raw > 20000:
        fails.append(f"EXCEDE el tope del BOT FIELD: {raw} > 20.000 puntos de código (medido en vivo 2026-09-05: 20.000 pasa, 20.001 se corta en silencio con HTTP 200). Recorta texto — quitar tildes o emojis NO ayuda, porque no cuentan distinto.")
    # SIGNOS DE APERTURA ¿ ¡ (v3.45.0). El checklist de este mismo validador los prohibía desde siempre, pero
    # solo los IMPRIMÍA: una regla dura degradada a aviso. Probado por inyección: pasaba con exit 0.
    # Al conversar por WhatsApp no se usan; el bot que los escribe suena a texto redactado, no a persona.
    _ap = {c: text.count(c) for c in "¿¡" if c in text}
    if _ap:
        _d = " y ".join(f"{v} '{k}'" for k, v in _ap.items())
        fails.append(f"SIGNOS DE APERTURA en el prompt: {_d}. Al conversar no se escriben (sí en presentaciones y PDFs). Un bot que abre con ¿ o ¡ se lee como texto redactado y rompe la ilusión de persona. Quítalos y deja solo el signo de cierre.")
    # ── COMPUERTAS v3.47.0 ────────────────────────────────────────────────────────────────────
    # El verificador adversarial probó por inyección los 7 ítems que este checklist IMPRIMÍA:
    # 6 pasaban con exit 0. "Regla dura degradada a aviso", la ley de la casa. Aquí se cierran las
    # que se pueden cerrar SIN falsos positivos. Las dos que NO se cierran quedan declaradas abajo,
    # porque una compuerta que bloquea trabajo legítimo hace más daño que la regla que no existe:
    # eso ya pasó hoy en validar-doctrina.sh y dejó la vara mínima de la skill bloqueada.
    #
    # Técnica común: se salta la línea que PROHÍBE la práctica, si no el patrón caza su propia
    # prohibición ("NUNCA digas que eres una IA" contiene "eres una IA").
    import unicodedata as _u2
    def _sin(s):
        s = _u2.normalize("NFD", s.lower())
        return "".join(c for c in s if _u2.category(c) != "Mn")
    # v3.50.0 — SE SALTAN DOS CLASES DE LÍNEA, no una:
    #  (a) la que PROHÍBE la práctica;
    #  (b) 🔴 la que reporta lo que dice EL CLIENTE (discurso referido). Esta segunda la descubrí
    #      estresando el detector contra español legítimo que SE PARECE al defecto, siguiendo la ley
    #      del CdM: "un detector de patrones acusa al IDIOMA, no al defecto". Caso real cazado:
    #      "Si el cliente dice que somos una inteligencia artificial, no discutas" — el bot NO se
    #      declara IA, está recibiendo instrucciones sobre una acusación ajena, y mi patrón la
    #      bloqueaba. El bot solo comete la violación cuando la afirma EN PRIMERA PERSONA.
    _PROH = re.compile(r"(nunca|jamas|prohibid|no digas|no afirmes|no reveles|no menciones|evita|"
                       r"linea roja|antipatron|en vez de|no uses|no incluyas|"
                       r"si (el cliente|te|le|los?|las?) (dice|dicen|pregunta|preguntan|acusa|acusan|insinua|insinuan)|"
                       r"cuando (digan|pregunten|acusen|insinuen)|"
                       r"si (sospechan|creen|piensan|dudan) que|te acusan de|si preguntan)")
    _lineas = [l for l in text.split("\n") if l.strip()]

    # 1) EL BOT NO DICE QUE ES IA. Es la ilusión que sostiene toda la venta conversacional.
    _ia = re.compile(r"\b(soy|somos)\s+(una?\s+)?(inteligencia artificial|ia\b|bot|chatbot|asistente virtual|robot)")
    _culp = next((l for l in _lineas if not _PROH.search(_sin(l)) and _ia.search(_sin(l))), None)
    if _culp:
        fails.append(f"EL BOT SE DELATA COMO IA: \"{_culp.strip()[:80]}\". La venta conversacional se sostiene sobre que el cliente hable con una persona; en el segundo en que el bot dice que es un bot, el cliente deja de negociar y se va. El prompt debe PROHIBIRLO, nunca afirmarlo.")

    # 2) CREDENCIALES HEREDADAS (LEY NUNCA HEREDAR). Un token de otro negocio dentro de un prompt
    #    es fuga de datos, no un descuido de formato. Solo patrones que NUNCA son legítimos aquí:
    #    los datos bancarios del vendedor SÍ son legítimos y por eso no se tocan.
    # 🔴 sk-ant- (Anthropic) FALTABA en esta lista, y el barrido de publicacion de la casa si lo
    # cubre: un prompt con una clave de Anthropic pasaba en verde por este validador. Anadido el
    # 2026-09-07. Ojo con el guion: Anthropic usa sk-ant-, con GUION, no sk_ant_ con guion bajo —
    # copiar el patron de las otras familias habria dejado la laguna abierta igual.
    _sec = re.search(r"\b(sk-ant-[A-Za-z0-9_-]{12,}|sk_live_[A-Za-z0-9]{8,}|sk_test_[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{20,}|"
                     r"AIza[A-Za-z0-9_\-]{20,}|EAA[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._\-]{20,})", text)
    if _sec:
        fails.append(f"CREDENCIAL DENTRO DEL PROMPT: '{_sec.group(1)[:14]}…'. Una clave o token jamás va en un prompt — se lo lleva quien vea la configuración, y si vino heredado de otra plantilla es dato de OTRO negocio. Bórralo y rota la credencial.")

    # 3) VERSIÓN EN EL HEADER. El header lo LEE EL CLIENTE en el primer mensaje: un "v7" ahí le dice
    #    que habla con una plantilla. Solo se mira la primera línea, que es donde vive el header.
    _h = _lineas[0] if _lineas else ""
    if re.search(r"\bv\s?\d+(\.\d+)*\b|\bversi[oó]n\s*\d", _sin(_h)):
        fails.append(f"VERSIÓN EN EL HEADER: \"{_h.strip()[:70]}\". El header es lo primero que el cliente asocia al negocio; un número de versión lo delata como plantilla. El versionado va en tu documentación, no en el prompt.")

    # 4) ABUSO DE EMOJIS. La regla es ≤2 POR MENSAJE y un validador no puede saber dónde corta cada
    #    mensaje, así que se usa la línea como proxy y un umbral GENEROSO (>4): caza el abuso real
    #    sin morder una línea legítima de 2 o 3.
    _em = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
    _ab = next(((l, len(_em.findall(l))) for l in _lineas
                if not _PROH.search(_sin(l)) and len(_em.findall(l)) > 4), None)
    if _ab:
        fails.append(f"ABUSO DE EMOJIS: {_ab[1]} en una sola línea (\"{_ab[0].strip()[:55]}…\"). La regla es máximo 2 por mensaje: más emojis no suman calidez, restan credibilidad y hacen que el mensaje se lea como spam.")

    # ── CONTAMINACIÓN DE LA PLANTILLA DE FÁBRICA (v3.49.0, auditoría del CdM 2026-09-07) ──
    # POR QUÉ FALTABA Y POR QUÉ DUELE: toda la familia golden-chatea-pro-* documenta que la
    # plataforma instala los asistentes con una PLANTILLA DE FÁBRICA ya escrita (61 de 61 campos
    # idénticos byte a byte entre un espacio de Colombia y uno de México), y que un campo de
    # fábrica NO SE VE VACÍO: SE VE CONFIGURADO. La LEY de FER del 2026-08-08 lo dice sin
    # rodeos: los claims y cifras de negocio "no rompen nada técnico, ningún barrido de llaves
    # los detecta, pero ponen al bot a MENTIRLE al cliente con datos de otra empresa".
    # Este validador —el de la skill más grande del arsenal— no miraba nada de eso. Medido el
    # 2026-09-07 contra un prompt sembrado a propósito: cazó los signos de apertura y la falta
    # de regla de brevedad, y dejó pasar el asesor de fábrica y la cifra heredada.
    #
    # DOS NIVELES, y la diferencia es deliberada:
    #  · BLOQUEA solo los literales VERIFICADOS byte a byte en el servidor.
    #  · AVISA sobre la CLASE (cualquier cifra de negocio), porque una cifra puede ser real y
    #    del propio negocio. Bloquear la clase sería acusar al idioma — el error que esta casa
    #    ya cometió con los detectores de país y de secretos.
    #
    # COBERTURA DECLARADA: los literales de fábrica salen de
    # golden-chatea-pro-config-logistico/assets/plantilla-fabrica.json, que trae la huella md5
    # de los 61 campos pero los VALORES completos de 9. Lo que se bloquea aquí está medido en
    # esos 9; el resto se avisa. No se bloquea lo que no se ha medido.
    _FABRICA = [
        ("Santiago",
         "el asesor que la plataforma instala DE FÁBRICA en el saludo"),
        ("5 años de experiencia",
         "la biografía de fábrica (y el asistente de comentarios trae otra que dice 7: dos "
         "biografías falsas y contradictorias en el mismo espacio)"),
    ]
    for _lit, _pq in _FABRICA:
        if re.search(r"\b" + re.escape(_lit) + r"\b", text, re.I):
            fails.append(
                f"DATO DE FÁBRICA SIN LIMPIAR: \"{_lit}\" — {_pq}. Está medido byte a byte en el "
                f"servidor, así que si aparece aquí es que se heredó, no que el negocio lo eligió. "
                f"Un dato de fábrica no se ve vacío: se ve configurado, y el bot termina "
                f"diciéndoselo a un cliente de verdad. Reemplázalo por el dato REAL del negocio.")

    # 🔴 DOS REGLAS QUE VIVÍAN SOLO EN LOS .md (cerradas 2026-09-23).
    #    Medido: la escasez inventada está prohibida en CUATRO ficheros de doctrina
    #    (cumplimiento §4, objeciones.md, elemento 8 de oferta-irresistible.md y la propia
    #    SKILL.md) y el validador NO la miraba; el apodo de falsa cercanía está prohibido con ⛔
    #    en psicologia-del-chat.md y tampoco. Es la ley de la casa: una regla que vive solo en un
    #    .md no es un guardarraíl, es un recuerdo. Salieron a la luz al medir un juego de
    #    plantillas de terceros donde la escasez aparecía en 5 de 5.
    import unicodedata as _ud
    _plano = "".join(c for c in _ud.normalize("NFD", text)
                     if _ud.category(c) != "Mn").lower()

    # BLOQUEO: apodo de falsa cercanía. Se exige MARCA VOCATIVA (saludo delante, o "mi X"):
    # sin ella se acusaría al idioma — "cuida tu corazón" y "la reina del hogar" son legítimos,
    # y bloquear la clase entera es el error que esta casa ya cometió con los detectores de país.
    _APODO = re.compile(
        r"\b(?:hola|buenas|buenos dias|buenas tardes|buenas noches|querid[oa]|"
        r"hermos[oa]|magnific[oa]|bienvenid[oa])\s*,?\s*"
        r"(reina|rey|amor|corazon|princesa|bella|bello|mami|papi)\b"
        r"|\bmi\s+(amor|vida|cielo|reina|rey|corazon)\b")
    _ap = sorted({m.group(0).strip() for m in _APODO.finditer(_plano)})
    if _ap:
        fails.append(
            f"APODO DE FALSA CERCANÍA: \"{_ap[0]}\". El límite lo marca expresamente Gaviria en "
            f"`psicologia-del-chat.md`: reina, amor, princesa y compañía NO son cercanía, son un "
            f"disfraz de cercanía, y se notan. La cercanía está en el interés, no en el apodo. "
            f"Saluda neutro o con @ (\"Hola 😊\", \"Bienvenid@\") o por su nombre si ya lo dio.")

    # AVISO (no bloqueo): escasez sin confirmar. No se bloquea porque PUEDE ser cierta —
    # la doctrina la admite si el vendedor confirmó el stock. Lo que no se admite es que
    # entre por herencia de una plantilla y nadie la mire.
    _ESCASEZ = re.compile(
        r"solo\s+(nos\s+)?quedan\b|quedan\s+poc[ao]s\b|ultim[ao]s?\s+\d{1,3}\s*unidades"
        r"|ultimas\s+unidades|se\s+(estan\s+)?agotando|quedan\s+\d{1,3}\s*unidades")
    _es = sorted({m.group(0).strip() for m in _ESCASEZ.finditer(_plano)})
    if _es:
        avisos.append(
            f"ESCASEZ SIN CONFIRMAR: {', '.join(_es[:3])}. No se bloquea porque puede ser REAL "
            f"(elemento 8: solo si el vendedor confirmó el stock) — pero es la vía por la que "
            f"las plantillas heredadas meten urgencia inventada: medido el 2026-09-23, un juego "
            f"de plantillas de terceros la traía en 5 de 5. En COD se paga caro: el cliente que "
            f"vuelve y encuentra la misma promo entiende que le mintieron y rechaza el pedido "
            f"con el flete ya gastado. CONFIRMA el stock con el dueño; si no lo puede sostener, "
            f"usa la urgencia operativa, que siempre es cierta: \"si confirmas hoy, sale mañana\".")

    # AVISO (no bloqueo): cifras de negocio. Pueden ser ciertas — o heredadas.
    _CIFRAS = re.compile(
        r"(m[áa]s de\s+)?[\d][\d.,]{2,}\s*(clientes|clientas|pedidos|ventas|familias)"
        r"|\b\d+\s*a[ñn]os\s+(de\s+)?(experiencia|en el mercado|trayectoria)"
        r"|\b\d{1,3}\s*%\s*(de\s+)?(entrega|satisfacci[óo]n|efectividad)", re.I)
    _c = sorted({m.group(0).strip() for m in _CIFRAS.finditer(text)})
    if _c:
        avisos.append(
            f"CIFRAS DE NEGOCIO en el prompt: {', '.join(_c[:4])}. No se bloquean porque pueden "
            f"ser REALES de este negocio — pero son la vía por la que la plantilla de fábrica y "
            f"las configuraciones heredadas meten datos de OTRA empresa en boca del bot (caso "
            f"real 2026-08-08: \"Más de 100.000 clientes atendidos en Colombia\", dato de Golden, "
            f"a punto de quedar en el bot de otro espacio). CONFIRMA cada una con el dueño del "
            f"negocio; si no la puede sostener, se quita — no se rebaja.")

    # ── LAS DOS QUE PARECÍAN INCERRABLES (v3.48.0) ────────────────────────────────────────────
    # v3.47.0 las dejó como reserva declarada: "no se puede medir el mensaje que el bot enviará
    # desde el texto del prompt". Cierto — y era la pregunta equivocada.
    # LA SALIDA: no se mide la SALIDA del bot, se verifica que el prompt CONTENGA LA REGLA que la
    # gobierna. Un prompt sin la regla producirá la violación siempre; con ella, el modelo la respeta.
    # Cero falsos positivos, porque se busca la presencia de una instrucción, no la ausencia de un vicio.
    # Solo aplica al PROMPT de venta: un saludo o un recordatorio no llevan estas reglas dentro.
    if not mode.startswith("campo:"):
        # 5) EL CORCHETE QUE SALE LITERAL. [NOMBRE] es sintaxis LEGÍTIMA de variable
        #    (sintaxis-del-prompt.md §4), así que su presencia NO es el fallo. El fallo es que el
        #    prompt use corchetes SIN la instrucción que impide que lleguen crudos al cliente
        #    ("Hola [NOMBRE]" enviado tal cual). La skill declara esa instrucción OBLIGATORIA.
        #    ⚠️ HAY DOS CLASES DE CORCHETE Y SOLO UNA ES RIESGO (aprendido al probar: la primera
        #    versión de esta compuerta BLOQUEÓ las dos varas de la skill):
        #      · MARCADOR DE CONSTRUCCIÓN — [URL TESTIMONIOS], [URL MODO DE USO]. Lo sustituye
        #        QUIEN ARMA el paquete antes de entregar; nunca llega vivo al bot. NO es riesgo.
        #      · VARIABLE DE CONVERSACIÓN — [NOMBRE], [PRODUCTO], [PRECIO]… Las rellena el modelo
        #        MIENTRAS habla, y son las que pueden salir crudas si falta el dato. Esas sí.
        #    Por eso se busca la lista cerrada de variables de conversación, no cualquier corchete.
        _VARS = r"\[(NOMBRE|PRODUCTO|PRECIO|BENEFICIO|MARCA|CIUDAD|DOLOR|DESEO|CLIENTE|N)\]"
        if re.search(_VARS, text):
            #    Se detecta el CONCEPTO, no una frase literal. La primera versión llevaba una lista
            #    cerrada de redacciones y bloqueó la vara mínima de la skill, que dice la regla con
            #    otras palabras ("los [corchetes] son para TI, JAMÁS salen en el mensaje"). Una
            #    compuerta que exige una redacción exacta no valida doctrina: valida ortografía.
            _tiene = any(
                "corchete" in _sin(l)
                and re.search(r"\b(jamas|nunca|no)\b", _sin(l))
                and re.search(r"\b(sale|salen|aparece|aparecen|escrib|dejes|van|mandes|envies)", _sin(l))
                for l in _lineas)
            if not _tiene:
                fails.append("CORCHETES SIN LA REGLA QUE LOS PROTEGE: el prompt usa variables tipo [NOMBRE] pero NO trae la instrucción de que jamás salgan literales al cliente. Sin esa línea, el día que falte un dato el bot escribe \"Hola [NOMBRE]\" tal cual y la conversación se cae sola. Añade: \"los [corchetes] son instrucciones para TI, jamás aparecen en el mensaje; si falta el dato, no lo inventes ni dejes el corchete: pídelo\".")

        # 6) LA REGLA DE BREVEDAD. Tampoco se cuenta el mensaje del bot: se exige que el prompt
        #    LLEVE su propio límite escrito. Sin él, el modelo escribe párrafos y el chat se lee
        #    como un folleto, que es el fallo que la skill entera persigue.
        if not re.search(r"(maximo|max\.?|no mas de|no superes|hasta)\s*\d{1,3}\s*palabras", _sin(text)):
            fails.append("EL PROMPT NO LLEVA SU REGLA DE BREVEDAD: no aparece ningún límite de palabras por mensaje. Sin ese techo escrito, el modelo responde en párrafos y el chat deja de parecer una persona. Escribe el límite explícito (la doctrina usa ~35 palabras, con los dos tramos largos permitidos: conexión aspiracional y presentación de la oferta).")

    # ⚠️ NO SE CIERRAN, y se dice por qué (reserva declarada, no hueco disimulado):
    #    · "máximo 35 palabras por mensaje": el validador no sabe dónde empieza y termina cada
    #      mensaje dentro del prompt, y contar el bloque entero castigaría los dos tramos que la
    #      doctrina permite largos (conexión aspiracional y presentación de la oferta).
    #    · "corchetes que salen literales": [NOMBRE] es sintaxis LEGÍTIMA de variable según
    #      sintaxis-del-prompt.md. Distinguir la variable buena del marcador olvidado exige saber
    #      si Chatea la resuelve, y eso no se puede leer desde el texto.
    #    Las dos siguen en el checklist de abajo, para juicio humano.
    if not fails:
        if mode.startswith("campo:"):
            # 🔴 v3.48.0. Antes se caía al mismo texto del PROMPT y le decía a un saludo de 1.938
            # que estaba "CORTO para el objetivo 9.000-11.800" y que añadiera FAQ y objeciones —
            # a un campo cuyo tope son 1.000 y que Chatea corta en silencio. Un validador que
            # aconseja lo contrario de lo correcto es peor que no tener validador.
            _c = mode.split(":", 1)[1]
            _pct = raw * 100 // limit if limit else 0
            print(f" Estado:     ✅ VÁLIDO — campo '{_c}': {raw}/{limit} crudos ({_pct}% del tope). Aquí NO se busca llenar el campo: se busca que quepa.")
        else:
            rango = f"{LO:,}-{HI:,}".replace(",", ".")
            etiqueta = "VARA MÍNIMA VIABLE" if minimo else "objetivo"
            target = f"dentro del {etiqueta} {rango}" if LO <= raw <= HI else ((f"CORTO para el {etiqueta} {rango}" + ("" if minimo else " (revisa qué venta falta: FAQ, objeciones, escenarios)")) if raw < LO else f"sobre el {etiqueta} {rango} pero bajo el techo")
            print(f" Estado:     ✅ VÁLIDO — {raw}/{limit} crudos ({target}); bot field {raw}/20.000 puntos de código")
        print(" Recuerda:   corre también `validar.sh --activador <archivo>` sobre CADA activador (ahí el veredicto exige 0 emojis).")

# Los AVISOS se imprimen SIEMPRE: bloquee o no. Un aviso que solo sale cuando ya hay un bloqueo
# no sirve de nada — el caso peligroso es justo el prompt que pasa en verde con una cifra
# heredada dentro.
if avisos:
    print(" ⚠️ AVISOS — no frenan la entrega, pero hay que mirarlos antes de cerrar:")
    for a in avisos: print(f"   · {a}")

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
