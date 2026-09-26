# API de Chatea Pro y los DOS techos — detalle técnico medido

**Cuándo leer este archivo:** SIEMPRE, completo, ANTES de cualquier lectura o escritura por API
a un workspace (MODO A o MODO B), y antes de cada push de un prompt. La regla resumida vive en
SKILL.md (método cien de cien, punto 3); aquí están las tablas medidas y los gotchas que evitan
matar un asistente en silencio. El chequeo determinista de techos se corre con
`scripts/medir_techos.py`, no a ojo.

## Techo A · el bot field: 20.000 ESCAPADOS, no crudos

Al ejecutarse, el flujo copia la configuración **escapada**: cada tilde ocupa 6 caracteres y cada
emoji 12. El techo práctico en crudos queda en **~17.000**. Medido (2026-08-07):

| crudo | escapado | el asistente arranca |
|---|---|---|
| 16.882 | 19.895 | sí |
| 19.922 | 23.266 | **NO** |

```python
escapado = len(json.dumps(valor)[1:-1])   # regla dura: < 19.000
```
⚠️ **Pasarse NO da error:** la API responde `200 {"status":"ok"}`, guarda el JSON **cortado**
y el asistente **muere en silencio**. El error solo aparece en Panel → Registros de errores.

## Techo B · el campo nativo del formulario

Cada campo del panel tiene su propio tope. Escribir por encima por API funciona y no da error,
pero el día que alguien abra ese formulario y pulse Guardar, **el campo se corta y se pierde el
texto**.

**MEDIDOS en el código vivo de la app** (`maxLength`, notación minificada `2e3`=2.000,
`1e4`=10.000 — un regex que no la contemple reporta "sin tope" en falso):
Comentarios → `comentarios_negativos.prompt_general` 10.000 · `venta_conversacional.prompt`
8.000 · `respuesta_publica.prompt` 3.000 · `ej_a_eliminar` / `ej_a_no_eliminar` 1.000 ·
`info_extra` 500 · `contacto` / `t_envio` / `datos_req` 200.
Ventas (`Configuracion general 2`) → `comportamiento_ia.rol` / `restricciones` /
`analizar_palabra.prompt` 2.000 c/u · descripción del producto 500 · `mensaje_inicial` /
`pregunta_de_entrada` / `remarketing.prompt_N` 1.000 · `notificacion.mensaje` 400.
Logístico → `pago_anticipado.estrategia_persuasion` **2.000** (`maxLength` + un
`slice(0,2000)` en `onChange`).
⚠️ **"El Logístico no tiene tope" es FALSO** — lo decía una versión anterior de esta skill y lo
sigue diciendo `TOPES-NATIVOS-POR-CAMPO.md`. El validador de la casa ya lo tiene bien.

**NO medidos en código, vienen de capturas de pantalla** (trátalos como orientativos, no como
verdad): `prompt_libre` 12.000 · `producto_segundos.prompt_datos` 4.000. No hay ningún
`maxLength` de esos valores en el bundle.

**Sin documentar todavía:** Carritos (el briefing dice "solo los de correo"; `CartsPage` no
tiene ningún `maxLength`, así que viven en un módulo compartido sin localizar) y varios topes
sueltos de Ventas medidos pero sin mapear a su campo (300 ×6, 800 ×2, 1.500).

`TOPES-NATIVOS-POR-CAMPO.md` en `PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/` tiene la tabla
completa, **pero arrastra los dos errores de arriba**: consúltala sabiéndolo, y ante un campo
crítico remídelo contra el bundle en vez de creerle a la tabla.

Sobre el TIPO de campo: **JSON** = 20.000 · **LONG JSON** = 500.000 (medido 2026-07-25). Crear
los campos nuevos como LONG JSON da aire para el JSON completo, **pero NO levanta el Techo A**
(el flujo sigue copiando escapado) **ni el Techo B** (el formulario corta igual). Los campos
que ya existen como JSON **no se convierten por API**: borrar y recrear cambia el `var_ns` y
rompe las referencias del flujo. El tipo se cambia en la UI.

La vara de "cuánta potencia debe tener el prompt" sigue siendo llenar el campo de verdad — pero
contra el **crudo ~17.000**, nunca contra 19.000 crudos, que es exactamente el rango medido que
deja el asistente muerto.

## Carga automática por API (verificado en vivo 2026-07-09)

Chatea Pro es whitelabel de **UChat**: TODA la config de los 4 asistentes vive en **Bot Fields
JSON** y se lee/escribe por API (`https://chateapro.app/api`, auth Bearer atada al bot/flujo).
Esto permite armar el workspace COMPLETO por API, sin pegar a mano. El mapa maestro (Bot Fields
clasificados por asistente, con el esquema de claves de cada config) está levantado en
`PROYECTOS/CHATEA-PRO-ASISTENTES-MAPA/MAPA-FULL-CONFIGURACION.md` + `extraccion/esquemas/`, y el
briefing operativo completo en `BRIEFING-PARA-SKILLS.md` de esa misma carpeta — **léelo antes de
instalar una cuenta nueva**.

**El censo de campos NO es fijo**: varía por workspace y en el tiempo (se han medido 56, 69, 79 y
82 en distintos espacios y fechas). Cualquier número escrito aquí sería una foto vencida:
**re-extrae paginando y clasifica lo que HAY**, nunca asumas que existen todos (Remarketing puede
no estar según la versión del bot).

Campos de config por asistente: Ventas (`[Ventas Wp] Configuracion general` +2), Logístico
(`[Logistico] Configuracion General` + Confirmaciones + Seguimiento + Novedad), Carritos
(`[Carritos] Configuracion` + Información de productos), Comentarios
(`[Comentarios] Configuracion General` + Productos), Remarketing, Meta pixel, Integraciones.

⚠️ **`[Logistico] Plantillas de mensaje` es un CAMPO MUERTO** (verificado 2026-08-03): contiene
relleno (`"namespace":"string"`). Las plantillas que de verdad trabajan están declaradas DENTRO
de Confirmaciones, Seguimiento y Novedad. No lo leas ni lo escribas: es gastar tokens en un campo
que nadie interpreta.

El pusher genérico vive en `golden-chatea-pro-config-ventas-wp/scripts/push_config.py`
(read → backup → push --confirm por `set-bot-fields-by-name`). Gotchas: token atado a flujo
(sin flujo = 404 "Flow not found"), User-Agent de navegador (Cloudflare 1010), pares
nombre=archivo antes de --confirm. Token = dato sensible: scope mínimo, rotar al terminar.

**Gotchas adicionales (producción, 2026-07-09):**
- `GET /flow/bot-fields` está **PAGINADO: 10 campos por página**. Para leer/respaldar TODO hay
  que recorrer `meta.last_page` (`?page=N`) y unir los `data`. Un backup de una sola página
  pierde ~85% del workspace. (`push_config.py read/backup` consulta por nombre, eso sí trae el
  campo completo; el inventario total requiere paginar.)
- Verificación de escritura: el `PUT` responde 200 con `matched_items`; aún así, relee el campo
  y compara — es la única prueba real (y detecta si alguien pisó tu cambio desde la UI).
- Las plantillas de Meta (namespace propio por cliente) solo se REFERENCIAN por API, no se crean
  ni se aprueban: si una está `PENDING`, se resuelve en Meta, no aquí.
- El `PUT /flow/set-bot-fields-by-name` usa la llave **`data`**: `{"data":[{"name","value"}]}`.
  Con `bot_fields` responde **400**.
- El alta `POST /flow/create-bot-field` usa **`var_type`** (no `type`) y **exige `value`**. Con
  otra llave, **422**.
- El valor se guarda como string con `ensure_ascii=False, separators=(',',':')`. Otro formato
  infla el conteo contra el Techo A sin cambiar el contenido.
- **El trigger no admite caracteres de 4 bytes.** Un emoji lo corrompe y el bot no arranca nunca:
  `[c for c in texto if ord(c) >= 0x10000] == []`.
- **Cada llave conserva su tipo.** `multimedia` escrita como cadena se ve vacía y el panel la deja
  en `[]` al guardar, sin un solo error.
- El producto de Comentarios es un objeto de **5 llaves exactas** (`img`, `name`, `desc`, `rela`,
  `estado`). Con 4 llaves el panel no lo interpreta.
- **Pares `array` / `Extendido`:** los workspaces migrados dejan el campo `array` vacío y los datos
  en el `longtext` `... Extendido`. Verificado en un espacio que vende a diario: `[Ventas Wp]
  Disparador de productos` vacío con 4 productos activos en el Extendido. **Leer el `array` y
  concluir "no hay productos" es un error.** Pero **NO lo generalices al revés**: el par puede
  estar poblado de LOS DOS lados (medido: `[Comentarios] Productos` con 6.980 caracteres Y su
  Extendido con 7 productos). **Mira siempre los dos campos.** Sobre cambiar el tipo de un campo
  existente, la regla única está en el método cien de cien: por API no se convierte (borrar y
  recrear cambia el `var_ns` y rompe el flujo) — se cambia en la UI.
- **Imágenes:** `multimedia` e `imagen` aceptan URLs externas (CDN de Shopify, probado). Pero el
  `img` del producto de Comentarios usa `media.chateapro.app/temp/AAAAMM/<ID_DE_CUENTA>/...` y
  esas URLs **solo nacen subiendo la imagen en el panel** — no hay endpoint de subida. Copiar la
  URL de una cuenta a otra apunta a la cuenta de origen, no a la propia.
- **Valores por defecto que NO son defectos** (comprobado comparando dos workspaces sanos): las
  instrucciones de recolección vacías, el disparador `array` vacío, `voice_id:
  "English_MaturePartner"` y los eventos de `[Meta]` en cero. **No los "arregles".** El método
  ante la duda es comparar contra un workspace que funcione, no contra lo que uno supone.
