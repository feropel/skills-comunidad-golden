# Mapa de Ecom Magic AI + navegación con Chrome MCP

> ⚠️ **ESTA ES LA VÍA FALLBACK.** Desde v2.0 la vía principal es el **MCP oficial**
> (`references/mcp-api.md`): sin navegador, sin subir la foto, 100% autónoma. Usa este
> documento solo si el MCP no está conectado o falla — y avísale al usuario que conectando el
> MCP (4 pasos, una vez) el flujo deja de necesitar su intervención.

## Herramientas Chrome MCP a cargar (una sola llamada a ToolSearch)

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,
mcp__claude-in-chrome__computer,mcp__claude-in-chrome__find,
mcp__claude-in-chrome__file_upload,mcp__claude-in-chrome__browser_batch
```

Verifica sesión de navegador con `list_connected_browsers`. Crea/obtén el grupo de pestañas
con `tabs_context_mcp{createIfEmpty:true}`. Encadena acciones con `browser_batch`
(click → wait → screenshot) para ir rápido.

## Estructura de la app (barra lateral)

- **Galería de la Comunidad** — inspiración (piezas públicas de otros usuarios).
- **Academia** — tutoriales.
- **Acceso Rápido:**
  - **Generador de Anuncios** (`/products`) — el módulo principal para nuestras imágenes.
  - **Generador de Landings** (`/landings`) — secciones de landing.
  - **Investigación de Producto**.
- **Menú:** Herramientas de Espionaje, Análisis Financiero, Investigación de Ángulos de
  Venta, Investigación de Avatar, **Generador de Mockups**, **Generador de Logos**.
  (Generador de Guiones / Videos / Emails = "Pronto".)
- **Uso de Créditos:** "Créditos del Plan  N/200" — LÉELO al inicio y repórtalo. 1 crédito
  por imagen.
- Abajo: usuario logueado (nombre + correo).

## Flujo de pantallas para generar

1. **`/products`** — grilla de productos. Cada tarjeta = un producto con N "Anuncios".
   - **ABRIR producto:** click en el **centro/imagen** de la tarjeta.
   - **⚠️ NO** clickees el ícono de basura (aparece al pasar el mouse, esquina de la tarjeta)
     → dispara "Eliminar producto".
   - **"+ Nuevo Producto"** (arriba a la derecha) o la tarjeta **"Agregar producto"** → crear
     uno nuevo (pide nombre + foto + datos).
2. **`/products/<id>`** — pantalla del producto:
   - Arriba: **"Generar Nuevo Anuncio"** con todos los campos (ver `campos-generacion.md`).
   - Botón **"Generar Anuncio Profesional"** ("consumirá 1 crédito").
   - Abajo: **"Descargar anuncios de forma masiva"** + galería **"Anuncios Generados"**
     (cada uno con **"Ver Anuncio"** y un ícono de basura para borrar esa pieza).
3. **Modal "Ver Anuncio"** (al abrir una pieza generada) — opciones:
   - **Descargar en 2K** — alta resolución.
   - **Descargar optimizada** — **WebP liviano → esta es la que usamos para Shopify.**
   - **Editar anuncio** — instruir cambios sobre la pieza.
   - **Redimensionar** — otro tamaño.
   - **Traducir** (Nuevo).
   - **Compartir (+1 Crédito)** — publica en la comunidad y regala 1 crédito. NO parte del
     flujo; nosotros solo descargamos.
   - **Solicitar reembolso de crédito** — si la pieza salió mala, recupera el crédito.
   - Muestra la **Referencia** usada (miniatura).

## Login (credenciales las pone el usuario)

- Header con **"Iniciar Sesión" / "Comenzar"** = NO hay sesión.
- Abre `ecom-magic.ai` → botón **"Iniciar Sesión"** → pantalla con Correo + Contraseña.
- **Detente ahí.** Pide al usuario que escriba correo y contraseña y dé "Iniciar sesión".
- Cuando confirme, sigue: el dashboard queda en `/dashboard`.
- Nunca escribas tú credenciales ni datos de pago. La página pública "Pruébalo" es solo un
  video demo (no genera nada sin cuenta).

## Subir la FOTO del producto (regla dura, aprendida en validación)

El input `Imagen 1/2/3` se llenaría, en teoría, con `file_upload` — PERO `file_upload` SOLO
acepta archivos genuinamente compartidos con la sesión, y en **Claude Code (terminal) eso casi
nunca se cumple**. Verificado en validación:
- Las imágenes que el usuario **pega en el chat NO llegan al disco**, así que no hay ruta que
  pasarle a `file_upload`.
- `file_upload` **rechaza** scratchpad, la carpeta del proyecto y hasta el Escritorio
  ("only files the user has shared with this session").
- `upload_image` tampoco sirve ("Unable to access message history to retrieve image").
- Descargar la foto desde una **URL/CDN** al disco tampoco ayuda: `file_upload` igual la rechaza.
- Ecom Magic **no tiene API/MCP** (verificado en la cuenta y en la web), así que no hay atajo.

**Solución primaria (Claude Code) — handoff de 3 segundos, igual que el login:** pide al usuario
que **arrastre él mismo la foto al recuadro "Imagen 1"** en su Chrome (o use "Subir desde PC").
En cuanto la suelte, TÚ retomas y haces TODO el resto (plantilla, campos, generar, descargar).
**NO insistas** con subidas programáticas ni gastes tiempo probándolas — ya sabemos que fallan aquí.

**Cuándo SÍ funciona `file_upload` (otros entornos):** solo si el adjunto del usuario queda en una
carpeta realmente conectada/compartida con la sesión. Ahí: localiza el input con `find` ("file
input for product photo Imagen 1") → `file_upload({paths:[ruta], ref, tabId})` (nunca cliquees el
botón: abre un selector nativo invisible).

## Descargas

El botón **"Descargar optimizada"** (WebP) / **"2K"** dispara una descarga del navegador. En
algunos entornos ese archivo NO aterriza en `~/Downloads` (el Chrome del usuario puede
preguntar dónde guardar, o usar otra carpeta) — verifícalo con Bash y no asumas.

**Método fiable (verificado en validación):** en vez de depender de la descarga del navegador,
saca la URL de la pieza generada desde el DOM y bájala tú directo:
1. Con `javascript_tool`: `Array.from(document.querySelectorAll('img')).map(i=>i.src)` y busca la
   que contenga `/public-banners/banner-...` con `?original=1` (esa es la imagen full-res).
2. `curl -sL "<url>?original=1" -o hero-original.png` en la carpeta del proyecto
   (`PROYECTOS/<PRODUCTO>/`).
3. Optimiza a **WebP < 150 KB** con el script incluido (sips de macOS no exporta WebP;
   `cwebp`/`magick` pueden no estar). Pásale el tamaño como `AnchoxAlto`: cuadrado de
   carrusel `1080x1080`, infografía de sección `1080x1350` (si no lo pasas, asume
   cuadrado y una infografía vertical se deformaría):
   ```bash
   python3 ~/.claude/skills/golden-ecom-magic/scripts/optimizar-webp.py hero-original.png tag-recede-hero.webp 1080x1080
   python3 ~/.claude/skills/golden-ecom-magic/scripts/optimizar-webp.py seccion-original.png tag-recede-seccion.webp 1080x1350
   ```
   (Ej. real Tag Recede: quality 85 → 124.8 KB. Requiere Pillow: `pip install Pillow`.
   Si no logra bajar del límite ni en quality 40, imprime `AVISO` en vez de `OK`.)
4. Entrega el `.webp` a golden-shopify / golden-ads y reporta peso + créditos gastados.

## Fallas conocidas y troubleshooting

- **Grupo de pestañas perdido** tras reconexión del MCP → recrear pestaña y volver a la URL;
  la sesión persiste por cookies.
- **Clasificador de seguridad temporalmente no disponible** → espera unos segundos y reintenta
  la misma acción.
- **El scroll se "come" dentro de un textarea** → haz scroll sobre el margen (ej. x≈1450) para
  mover la página, no sobre el cuadro de texto.
- **La imagen salió rara / ignoró las instrucciones** → usa **"Editar anuncio"** con una orden
  concreta (no regeneres de cero). Si quedó inservible → **"Solicitar reembolso"** y regenera
  cambiando el molde o afinando "Instrucciones Adicionales". El modelo **"GPT Image 2"** a veces
  da mejor estética.
- **La generación tarda** 1-3 min por pieza (normal). Espera en tramos y vigila la card
  "Generando…" en "Anuncios Generados"; **no re-dispares** el botón (gastarías otro crédito).
- **Se acabaron los créditos** (0/200) → no se puede generar; informa el saldo al usuario y
  para. (Compartir una pieza a la comunidad regala +1 crédito, pero no es parte del flujo.)
- **El botón "Generar" está gris** → falta la referencia o la foto del producto; complétalas.
