# El cable · sin integración de Shopify no llega ni un carrito

**Esto es INSTALACIÓN, no configuración.** Va antes de que exista nada que configurar. La
configuración son las 29 llaves del campo JSON; esto es el cable que conecta la tienda con
Chatea Pro. **Los carritos entran por el webhook de Shopify** — no se cargan a mano, no hay
campo donde meterlos. Sin el cable, se puede dejar el asistente perfecto y no va a recuperar
un solo carrito, sin que nada dé error.

Fuente: vídeo oficial de Chatea Pro *"Nuevo método integración de Shopify y Chatea Pro"*
(16:02), transcrito completo el 2026-09-08.

## Por qué hay un método "nuevo"

**Shopify cambió sus políticas el 1 de enero y el método anterior dejó de funcionar.** El panel
de Shopify lo avisa cuando alguien intenta el camino viejo. Un tutorial antiguo estrella al que
lo siga, así que lo primero es comprobar que no se está usando el método muerto.

## Los tres datos que pide Chatea Pro

**URL de la tienda · Access Token (`shpat_`) · API key (Client ID).** Todo el procedimiento
existe para conseguir el segundo.

## El procedimiento, en dos mitades

Explicarlo en dos mitades lo hace fácil: la primera es *darle permiso a Chatea dentro de
Shopify*; la segunda es *convertir ese permiso en una llave permanente*. Los dos flujos de la
plantilla existen solo porque Shopify no entrega la llave directamente: hay que pedir un código
y canjearlo.

**MITAD 1 · crear la app privada en Shopify**

1. Shopify → Configuración → Apps → **Desarrollar apps** → *Go to the Dashboard* → Crear app.
   El nombre da igual.
2. **App URL**: `https://chateapro.app`. La versión del webhook se deja como viene.
3. **Access / scopes** → Seleccionar → pegar **los 24 permisos de golpe**
   (`assets/permisos-shopify-24.txt`). Uno por uno son veinte minutos tirados.
4. **No tocar nada más.** El vídeo insiste tres veces en esto.
5. **Release** (el mensaje de versión es opcional) → Home → **Instalar aplicación** → elegir la
   tienda → Instalar. Si Chatea Pro aparece dentro de Shopify, aunque sea una página sin acceso,
   va bien.

**MITAD 2 · sacar el token bueno**

6. Instalar en el espacio de Chatea la **plantilla de flujos** que da Chatea Pro para esto
   (el enlace lo entrega Chatea; no se guarda aquí porque es material suyo y puede cambiar) →
   elegir el canal → Instalar. Aparece la carpeta **"Crear Token Permanente de Shopify"** con
   tres flujos: uno con candado, un **Paso 1** y un **Paso 2**.
7. **Paso 1** pide tres cosas: el dominio `.myshopify.com` **sin `https://`** (Shopify →
   Dominios), el **Client ID** (Settings de la app) y una **URL de redirección** — sirve
   *cualquiera* que empiece por `chateapro.app`. Guardar cada campo, publicar y ejecutar con el
   triángulo azul → *vista previa en ventana emergente*. Devuelve un enlace.
8. Abrir ese enlace, **copiar el `code`** y llevarlo al **Paso 2**, que pide además el dominio,
   el Client ID y el **Secret** (`shpss_`). Publicar y ejecutar: devuelve el token **`shpat_`**.
9. En Chatea: Integraciones → Shopify → Access Token (`shpat_`) + Client ID + URL de la tienda
   → Conectar.

## 🔴 Los CUATRO sitios donde se atasca, en orden de cuánta gente se cae

1. **EL SECRET NO ES EL TOKEN, Y LOS DOS EMPIEZAN POR `sh`.** El Secret de la app es `shpss_…`
   y el que sirve es `shpat_…`. Es el error número uno, y el vídeo lo demuestra fallando a
   propósito. Enseñando esto en vivo, hacer el fallo delante enseña más que advertirlo.
2. **El enlace del Paso 1 se abre en la MISMA ventana donde está la sesión de Shopify.** En otra
   ventana no hay sesión y el `code` no sirve. Y **da igual que la página salga en error**: lo
   único que importa es que se abrió.
3. **El `code` se corta con precisión**: lo que va **después de `code=` y antes del `&`**. Ni un
   carácter de más ni de menos. Si sale mal, se genera otro abriendo el enlace de nuevo — no hay
   que rehacer nada.
4. **Quien no sea DUEÑO de la tienda no puede instalar la app.** Desde una cuenta de colaborador
   o de asesor con permisos limitados hay que pedirle permisos al dueño. **Esto no se arregla en
   el momento**, así que se pregunta ANTES de empezar.

## Qué comprobar antes de dar la configuración por buena

- La integración de Shopify aparece **conectada** en el panel de Chatea.
- El token empieza por **`shpat_`**, no por `shpss_`.
- `acciones_especiales.origen_datos` del campo de configuración dice **`shopify`** — si dice
  otra cosa, el asistente está esperando los carritos por una vía que no es la que se conectó.

Sin esos tres, la configuración de las 29 llaves está bien escrita y **no la va a leer nadie**.

Relacionado: `SKILL.md` (sección del cable) · `references/ley-datos-entre-espacios.md`
(el `shpat_` es un secreto y nunca se copia entre espacios).
