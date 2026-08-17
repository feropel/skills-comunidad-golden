# Auto-verificación de cierre (correr ANTES de entregar)

Objetivo: que los errores que ya pasaron (rating 0.0, color viejo, sin sello, JSON roto)
sean IMPOSIBLES de entregar. Correr este script sobre el `product.json` generado.

⚠️ **G4.2 — verificación OBLIGATORIA en cada entrega:** el check 21 mide cada valor
`custom_liquid` del template en **bytes UTF-8** (no caracteres) y FALLA si alguno llega a
50.000 — el tope duro de Shopify en todos los temas. Sin pasar ese check, no se entrega.

```python
import json, re, sys
RUTA = "RUTA_DEL_PRODUCT_JSON"   # ← cámbiala
raw = open(RUTA, encoding="utf-8").read()
c = re.match(r'^(/\*.*?\*/\s*)', raw, flags=re.S)
body = raw[len(c.group(1)):] if c else raw
fallos = []

# 1) JSON válido
try:
    d = json.loads(body, strict=False)
except Exception as e:
    print("❌ JSON NO parsea:", e); sys.exit(1)

allcl = "\n".join(
    b.get("settings", {}).get("custom_liquid", "")
    for s in d["sections"].values()
    for b in [s] + list(s.get("blocks", {}).values())
)

# 2) Sin colores DEMO viejos (rojo base / verde proyekta) fuera del producto
for hexd in ["#b82622", "#8e1c19", "#ff5247", "#0F6F5C", "#0B5345", "#0bd4fd"]:
    if re.search(hexd, allcl, re.I): fallos.append(f"color demo/huérfano presente: {hexd} (acento que no es de la paleta → usar var(--brand-*))")

# 3) Rating nunca 0.0
if re.search(r'\b0\.0\s*/\s*5', allcl) or '>0.0<' in allcl:
    fallos.append('rating en 0.0/5')

# 4) CTA verde tokenizado presente
if "var(--cta)" not in allcl: fallos.append("falta var(--cta) (botón de compra)")

# 5) Sello de versión presente
if "GOLDEN SHOPIFY" not in allcl and "GFS_VERSION" not in allcl:
    fallos.append("falta el sello de versión")

# 6) Intro Ignition presente (bloque 1) — salvo que el usuario lo haya quitado a propósito
if "ignition" not in allcl.lower(): fallos.append("falta el intro IGNITION del bloque 1")

# 7) Releasit motor presente
if "releasit" not in allcl.lower() and "_rsi-buy-now" not in allcl:
    fallos.append("no se detecta el motor Releasit")

# === ESTÁNDARES LIQUID (references/estandares-liquid.md) ===
# 8) Accesibilidad: si hay acordeón FAQ, debe ser operable/anunciado (aria-expanded/role)
if "gfs-faq__item" in allcl and "aria-expanded" not in allcl and "role=\"button\"" not in allcl:
    fallos.append("FAQ sin accesibilidad (falta aria-expanded/role en la pregunta) — estandares-liquid §5")
# 9) Rendimiento: toda imagen bajo el pliegue debe ir lazy + sin CLS
imgs = re.findall(r'<img\b[^>]*>', allcl, re.I)
if any('loading=' not in tag.lower() for tag in imgs):
    fallos.append("hay <img> sin loading=\"lazy\" (riesgo de CLS/peso) — estandares-liquid §4")
# 10) Movimiento accesible: si hay animaciones, respetar prefers-reduced-motion
if "@keyframes" in allcl and "prefers-reduced-motion" not in allcl:
    fallos.append("hay animaciones sin @media (prefers-reduced-motion: reduce) — estandares-liquid §4/§5")
# 11) Accesibilidad: toda imagen con alt (descriptivo o "" decorativo), nunca sin alt
if any('alt=' not in tag.lower() for tag in imgs):
    fallos.append("hay <img> sin atributo alt — estandares-liquid §7")
# 12) Sin CLS: la imagen debe declarar dimensiones (width/height o aspect-ratio)
def _has_dims(tag):
    t = tag.lower()
    return ('width=' in t and 'height=' in t) or 'aspect-ratio' in t
if any(not _has_dims(tag) for tag in imgs) and 'aspect-ratio' not in allcl:
    fallos.append("hay <img> sin dimensiones (width/height o aspect-ratio) → riesgo CLS — estandares-liquid §6")
# 13) BEM/scope: clases con nombres genéricos sin prefijo (colisionan con el tema)
if re.search(r'class="(card|title|button|wrapper|container|item|grid|badge|price)"', allcl):
    fallos.append("clase genérica sin prefijo (card/title/button/...) → colisión con el tema — estandares-liquid §4")

# === G3.4: landing bloqueada + cero copy demo fósil ===
# 14) Copy DEMO fósil que NO puede sobrevivir en una página real (ticker/FAQ heredados)
DEMO = ["energía y vitalidad","vitalidad y energía","borojó","guaraná","chontaduro",
        "tapa-vaso","la bebes","viertes la porción","máxima energía","potencia desbloqueada"]
for w in DEMO:
    if w in allcl.lower():
        fallos.append(f"copy DEMO fósil presente: «{w}» → reescribir por producto (reglas-de-oro 0-B)")
# 15) Candado landing presente (header/footer ocultos → cliente no se va al home)
if "gfs-lock-landing" not in allcl and "custom_liquid_lock" not in body:
    fallos.append("falta el CANDADO LANDING (custom_liquid_lock) → el cliente puede irse al home")
# 16) Relacionados apagados por defecto
rp = d["sections"].get("related-products")
if rp and rp.get("disabled") is not True:
    fallos.append("related-products está ENCENDIDO → apagar por defecto (el usuario lo abre manual)")
# 17) G3.5: FUGA de comentario Liquid. {# ... #} NO es comentario válido en Liquid (lo es {% comment %}).
#     Si queda en un custom_liquid, se IMPRIME como texto en la página ("las letras" del build verrugas).
#     Ojo: en CSS `{#id{...}` es válido → por eso exigimos {# seguido de espacio, o el cierre #}.
if re.search(r'\{#\s', allcl) or re.search(r'\s#\}', allcl):
    fallos.append("comentario {# #} en custom_liquid → se verá como TEXTO en la página. Usa {% comment %}...{% endcomment %}")
# 18) G3.10: texto DEMO VISIBLE (fuera de comentarios). Caza fósiles que NO son {% assign %} sino
#     texto dentro de configs JS: RELEASIT_BUTTON_CONFIG.text, PRICE_CONFIG, sticky, títulos, etc.
visible = re.sub(r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}', '', allcl, flags=re.S)
for w in ["PRODUCTO DEMO", "MARCA DEMO"]:
    if w in visible:
        fallos.append(f"texto DEMO visible: «{w}» → revisa RELEASIT_BUTTON_CONFIG.text, sticky, títulos (no solo los assign)")
# 19) G3.11: paddings THEME-SAFE. Shrine rechaza al guardar muchos valores de padding_top/bottom
#     ("Setting 'padding_top' must be a step in the range"). Lo seguro es NO emitirlos → el tema
#     aplica su default. Si aparecen, quítalos de TODAS las secciones.
for skey, s in d["sections"].items():
    st = s.get("settings", {})
    if "padding_top" in st or "padding_bottom" in st:
        fallos.append("hay secciones con padding_top/bottom → Shrine puede rechazar al guardar. Quítalos (theme-safe).")
        break

# 20) G3.15: IGNITION con motor de salida JS (nunca queda montado tapando la página)
if "ignition" in allcl.lower() or "gfs-ign" in allcl.lower():
    if "removeChild" not in allcl or "pointer-events:none" not in allcl.replace(" ", ""):
        fallos.append("IGNITION sin motor de salida JS (removeChild + pointer-events:none) → puede quedar MONTADO. Ver ignition-variantes.md REGLA DE SALIDA")

# 21) G4.2 — OBLIGATORIO: TOPE SHOPIFY DE 50 KB POR SETTING custom_liquid (bytes UTF-8, NO caracteres).
#     Aplica a TODOS los temas. Shopify rechaza el guardado del template con:
#     "Setting 'custom_liquid' is invalid. ['Liquid file size cannot exceed 50 kilobytes.']"
#     (FileSaveError descubierto en tienda real, chat Insulinum 2026-08-07.)
#     Se mide CADA valor por separado (jamás el total concatenado) y en BYTES UTF-8: los acentos,
#     emojis y símbolos ocupan más de 1 byte, así que len(texto) en caracteres MIENTE.
for skey, s in d["sections"].items():
    for okey, obj in [(skey, s)] + list(s.get("blocks", {}).items()):
        cl = obj.get("settings", {}).get("custom_liquid", "")
        if not cl:
            continue
        nbytes = len(cl.encode("utf-8"))
        if nbytes >= 50_000:
            fallos.append(f"custom_liquid de «{okey}» pesa {nbytes} bytes UTF-8 (tope Shopify: 50.000) → PARTIR en secciones más pequeñas (una sección por pieza, REGLA #5)")
        elif nbytes >= 45_000:
            fallos.append(f"custom_liquid de «{okey}» pesa {nbytes} bytes UTF-8 (>90% del tope de 50.000) → aviso: al próximo retoque revienta; considera partirlo ya")

print("✅ TODO OK" if not fallos else "⚠️ REVISAR:\n- " + "\n- ".join(fallos))
```

Además, **SIEMPRE** (REGLA VISUAL — el JSON válido NO garantiza que se vea bien):
- [ ] **Vi la página renderizada** (screenshot), no solo el JSON. Prohibido decir "100/100" sin verla.
- [ ] País correcto en tiempos de entrega (Guatemala 1-4 / Colombia 3-7 — ver `paises-entrega.md`).
- [ ] Armonía de paleta (máx 2 colores fuertes, 1 acento de urgencia).

### Procedimiento de RENDER REAL (repetible, obligatorio antes de "listo")
El script de arriba es estático (regex/JSON): NO ejecuta Liquid ni ve el layout. Por eso, tras pasarlo:
1. **Sube el `product.json` a un tema NO publicado** (ej. el tema `golden` en Dawn, unpublished) con
   `themeFilesUpsert` por el MCP de Shopify → así no tocas la tienda en vivo.
2. **Abre el preview** (`preview_theme_id` / link de vista previa del tema) del producto real.
3. **Verifica en los 3 escenarios SIEMPRE — MÓVIL (~390px), TABLET (~768px) y PC (~1440-1920px)** (regla
   del usuario G3.16: "perfecto en todos los escenarios"; viewport del navegador, `preview_resize` o capturas
   independientes por dispositivo). En CADA tamaño: sin scroll horizontal, nada cortado ni encogido, y todo
   overlay `position:fixed` ocupa el viewport completo (`getBoundingClientRect()` = `innerWidth×innerHeight`,
   nunca un "cuadrito" — si falla, re-parent al body, ver tabla de errores):
   - El **CTA verde sobresale** al primer vistazo (REGLA #2); sticky visible al hacer scroll.
   - **FAQ:** abre/cierra con teclado (Tab + Enter) y el foco se ve (anillo). Lee bien con lector.
   - **Sin saltos de layout** (CLS) al cargar imágenes; nada tapado por el sticky/WhatsApp.
   - Ninguna sección vacía ni con placeholder `[...]` visible (REGLA #3/#4).
   - **INTRO IGNITION (ciclo de vida completo)**: con recarga limpia (borrar `gfs_ign_seen` del
     sessionStorage) el intro APARECE y a los ~3s DESAPARECE del DOM (`querySelector` = null).
     Probar también abriendo la pestaña en segundo plano (ahí es donde históricamente quedaba montado).
   - **IMÁGENES QUE ENCAJAN (G3.15)**: cada imagen llena su recuadro SIN cortar contenido — verificar
     `naturalWidth/naturalHeight` vs el ratio del contenedor. Infografías con TEXTO QUEMADO jamás van
     en slots con `object-fit:cover`: o crop fotográfico exacto al ratio del slot, o imagen completa a
     proporción natural (`height:auto`). El copy vive en el HTML, no dentro de la imagen.
4. **Screenshot** de la página completa (móvil) como prueba. Sin ese screenshot, NO es "listo".
> Un render headless 100% automático depende de una tienda/preview Shopify en vivo (es del entorno,
> no del archivo de skill): por eso este procedimiento es la forma correcta de cerrarlo cada vez.
