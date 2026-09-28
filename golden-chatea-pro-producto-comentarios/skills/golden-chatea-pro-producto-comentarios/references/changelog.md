# Changelog · golden-chatea-pro-producto-comentarios

## v1.11.1 · 2026-09-27 · Limpieza de datos internos para el repo público (aplicó el CENTRO DE MANDO)

La compuerta de publicación bloqueaba la skill por nombres internos: el nombre del chat y de la empresa de un espacio ajeno, y el código de un espacio real. Se cambiaron por formulaciones genéricas con el mismo sentido; la excepción operativa que nombraba espacios concretos vive ahora en la memoria del proyecto. Solo prosa y comentarios; ninguna regla cambió.

## v1.6 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

### 1 · 🔴 El validador decidía sobre datos de clientes reales sin estar validado

`scripts/validar_producto.py` son **449 líneas y 19 puntos de chequeo** que dictaminan si el campo
`[Comentarios] Productos` de un cliente está bien o mal. **No tenía banco.** Nadie había
comprobado nunca que mordiera. Es la misma laguna que se encontró el mismo día en
`golden-chatea-pro-prompt-ventas`, y en las dos el patrón es idéntico: el validador se construyó
con cuidado y nadie construyó la prueba de que el cuidado funciona.

**Nace `scripts/autoprueba.py`, 14 de 14**, con sabotaje por pieza. Cubre las 19 clases en 14
casos, incluido el inverso: **el producto bien formado tiene que PASAR**, porque un validador que
bloquea todo tampoco discrimina.

Los tres casos que más valen:
· **6 y 7 juntos** — la misma `desc` de 600 caracteres **BLOQUEA por formulario y solo AVISA por
  JSON**. Es la ley de las dos vías, ejercida: el mismo dato es error o aviso según por dónde
  entra, y confundirlas recorta sin motivo al que pega en el panel o corta en silencio al que
  escribe por API.
· **11** — una `img` de `media.chateapro.app` con el ID de OTRA cuenta tiene que avisar. Es la
  fuga documentada entre espacios: copiar esa URL muestra la imagen de la cuenta de origen, **y en
  el panel se ve bien**.
· **13** — si el nombre del producto no aparece en ningún disparador del `rela`, el cliente
  escribe el nombre de la marca y el bot no lo reconoce. Es el fallo más caro y el más fácil de
  no ver mirando el JSON.

### 2 · La contraprueba, porque 14 de 14 a la primera es sospechoso

Ley de la casa: *"si tu script dice que todo está bien a la primera, sospecha del script"*. Se
saboteó el validador en una copia —degradando el error de llaves faltantes a aviso y subiendo
`TOPE_DESC` de 500 a 99.999— y el banco **cayó a 12 de 14 nombrando exactamente esos dos casos**.
El banco muerde.

### 3 · La "referencia rota" era un FALSO POSITIVO, y se cerró para que no vuelva a distraer

El inventario del auditor marcaba `assets/index-BS1l9mqS.js` como *"mencionada pero NO existe"*.
No es un archivo de la skill: es el **bundle vivo de Chatea** citado como fuente autoritativa de
la tabla de países, con su tamaño y su sha256. El detector ve el segmento canónico `assets/` y lo
busca en el disco. Se le antepuso el esquema `https://` para que lo reconozca como URL, con la
nota explicando por qué. **Un falso positivo que nadie cierra se persigue en cada auditoría**, y
acaba enseñando a ignorar la sección donde algún día habrá una rota de verdad.

### 4 · Faltaba la línea de versión bajo el H1

Estándar de la casa; el inventario lo marcaba como aviso.

### 5 · 🔴 Había una COPIA de la `description` dentro del cuerpo, y ya había divergido

Bajo "Fronteras y desambiguacion" vivía la description entera con el rótulo *"se conserva para no
perder ningún matiz de frontera"*. **Ya no coincidía con la viva**: la copia llevaba dos frases de
frontera de más.

Esa clase de copia está explícitamente prohibida y esta skill es el caso que originó la regla —
`golden-chatea-pro-config-ventas-wp` la tiene escrita así: *"esa clase de copia ya mordió dos veces
en el arsenal: envejece y acaba contradiciendo a la description viva; así se coló el dato falso de
'7 países' en una hermana"*. **La hermana era esta.**

Retirada. Lo que es frontera se escribe **como frontera**, en una sola versión que se mantiene: qué
hace esta skill, qué hace `config-comentarios`, qué hace `prompt-ventas` y qué hace
`chatea-auditoria`.

## 2026-09-07 · CUPO DE LA API repartido a toda la familia (orden de FER)

**Dato de FER vía el desarrollador de Chatea, verificado contra la API viva:** el límite es
**1.000 peticiones por HORA**, pasarse **bloquea una hora entera**, y la respuesta trae el contador:

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: <las que quedan>

En inglés **X-RateLimit-Limit** y **X-RateLimit-Remaining**. **Se repone cada hora.**

🔴 **La trampa está en el CUÁNDO, no en el cuánto.** No viene `x-ratelimit-reset`: el servidor no
dice a qué minuto empezó la ventana. Observado por nuestro lado: dentro de la misma hora el
contador **solo baja** — no gotea crédito, se repone de golpe. Por eso, si te bloqueas, se espera
una **hora completa** desde ese momento y se comprueba **mirando** el contador
(`golden-chatea-cupo`, 1 petición), nunca calculándolo.

**Hasta hoy ninguna de las diez skills leía ese contador.** Se trabajaba a ciegas y el bloqueo
aparecía a mitad de la operación.

**Reparto, y cada bloque está escrito para SU skill** —lo que cambia entre ellas es cuánto cuesta
y qué se rompe si el cupo se agota a mitad; un bloque idéntico en diez sitios sería ruido:

· **Con CÓDIGO** (leen el contador de cada respuesta, avisan y no reintentan ante un 429):
  `chatea-auditoria` (comprueba antes de arrancar sus 137 peticiones y se niega si no caben),
  `chatea-operacion` (cuenta lo gastado; su coste **no es constante**),
  `config-logistico` (el PASO 0 de las cuatro hijas y el orquestador),
  `config-ventas-wp` (**el que escribe**, donde un 429 a mitad deja la config a medias).
· **Con DOCTRINA en el cuerpo** (producen texto o JSON que otro escribe por API):
  `config-carritos`, `config-comentarios`, `full-configuracion`, `producto-comentarios`,
  `prompt-ventas`, `validacion-direcciones`.

**Cobertura: 10 de 10.** Herramienta de casa: `golden-chatea-cupo [token] [--necesito N]`.
