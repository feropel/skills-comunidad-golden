# PERFILES — un solo motor, dos formas de vender

> Introducido en **G4.0**. Antes la skill tenía un solo esquema y el copy se improvisaba
> según el producto. Ahora el perfil es una **decisión declarada** que cambia qué secciones
> entran, en qué orden y con qué tono.

## La regla

**El MOTOR es único. El PERFIL solo cambia el énfasis.**

Nunca se bifurca el sistema en dos plantillas paralelas: eso garantiza que una se quede
atrás (pasó con el embudo de 17 secciones mientras la página real ya iba en 24). Hay un
solo `product.base.json`, un solo set de componentes y un solo changelog. El perfil vive
en el config center:

```liquid
{% assign PERFIL = "marca" %}   {% comment %} "marca" | "catalogo" {% endcomment %}
```

## Qué NO cambia nunca (el motor)

Releasit y el motor COD · precio dinámico · sticky · candado de landing · WhatsApp flotante ·
tickers · countdown · FAQ + JSON-LD · barra logística · convención `📝 EDITAR AQUI` /
`NO TOCAR` · estándares de código sano, accesible y rápido · las reglas de oro de copy y
legales · el CTA verde `#1D9E06` · la cadencia de 4 puertas.

## Perfil A — MARCA PROPIA

**Cuándo:** el producto es tuyo o de un cliente con marca real (nombre, identidad, línea de
productos, recompra). Ejemplo del sistema: la línea de 3 fragancias.

**Qué estás construyendo:** una marca. El activo es que vuelvan y que te reconozcan.

**Secciones que ENTRAN:**
- **Manifiesto** — el cierre identitario ("hay quien… este producto es para las terceras").
- **Historia / origen** — de dónde sale la fórmula, quién la hace.
- **Línea de productos** — las otras referencias, cross-sell, "conoce la línea".
- **Dolor segmentado por público** cuando la marca le habla a más de un perfil
  (`sec-dolor-segmentado.liquid`).
- **Seguridad / objeción #1** — cuando la marca vive o muere por la confianza
  (`sec-seguridad.liquid`).

**Tono:** identidad y pertenencia. Se puede ser aspiracional. Paleta propia de la marca.
El precio se justifica con marca, no solo con oferta.

**Palancas de venta:** confianza → identidad → recompra.

## Perfil B — CATÁLOGO PÚBLICO / DROPSHIPPING

**Cuándo:** el producto viene de un catálogo (Dropi y similares) y otras tiendas venden
exactamente el mismo. No hay marca que defender.

**Qué estás construyendo:** una oferta y una página. Eso es lo único que te diferencia,
porque el producto no es exclusivo.

**Secciones que ENTRAN (y son estructurales, no un extra):**
- **Escalera de combos** (`sec-combos.liquid`) — 1 / 2 / 3 unidades con el ahorro visible.
  En dropshipping el margen sale del ticket promedio; sin combos la página está incompleta.
- **Demostración** — el producto funcionando: video, GIF, antes/después. Es lo que convence
  cuando no hay marca que respalde.
- **Comparativa** (`sec-por-que-elegir.liquid`) — contra alternativas por CATEGORÍA, nunca
  nombrando marcas ajenas.
- **Urgencia real** — countdown activo y stock/lote honesto.
- **Prueba social reforzada** — más peso a reseñas y a la banda de autoridad.

**Secciones que SALEN:** manifiesto identitario, historia de marca, línea de productos.
Suenan falsas en un producto de catálogo y roban espacio a lo que sí vende.

**Tono:** demostración y beneficio concreto. Menos aspiracional, más "mira cómo funciona".

**⚠️ Reglas de copy propias de este perfil (riesgo real):**
- **NUNCA** "original", "réplica", "imitación", "copia", "versión".
- **SÍ** "sellado", "presentación premium", "calidad premium", "inspirado en".
- La garantía es de **proceso** (pagas al recibir, producto sellado), jamás de resultados
  ni de devolución de dinero.
- No se inventan certificaciones ni avales.

**Palancas de venta:** demostración → oferta → urgencia.

## Tabla rápida

| | Marca propia | Catálogo / dropshipping |
|---|---|---|
| Activo | La marca | La oferta y la página |
| Manifiesto | Sí | No |
| Historia / origen | Sí | No |
| Línea de productos | Sí | No |
| Escalera de combos | Opcional | **Obligatoria** |
| Demostración | Apoya | **Protagonista** |
| Comparativa | Opcional | **Sí** |
| Countdown | Suele ir apagado | **Activo** |
| Paleta | De la marca | Del producto y la conversión |
| Tono | Identidad, pertenencia | Demostración, beneficio |

## Cómo se elige

En las preguntas iniciales, junto con el tema y el país:

> **El producto es de marca propia o sale de un catálogo público (Dropi y similares)?**

Si el usuario no lo dice y no se puede deducir, **preguntar**. Un producto de catálogo
vendido con manifiesto de marca se siente falso; una marca propia vendida como saldo de
catálogo pierde el valor que justifica su precio.

Si el usuario pide expresamente una sección que su perfil no trae, **se pone**: la
instrucción del usuario pisa el perfil (Regla 0).
