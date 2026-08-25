## Estructura canónica = EMBUDO CON RITMO (G4.0 — 24 secciones, 4 puertas, PAS + neuroventa)
La página NO es una lista de secciones: es un **embudo con ritmo** donde **cada fase pide la venta** y,
a quien no compra, la siguiente lo recupera atacando **la objeción exacta**. El blueprint completo con
los principios de neuroventa está en `references/reglas-de-oro.md` (Regla 0-A).

**Cambio estructural de G4.0** (absorbido de la página real en producción, que ya iba en 24 mientras
la skill seguía documentando 17):
- **Candado, Ignition y WhatsApp salen del main y pasan a ser SECCIONES sueltas.** Son overlays
  `position:fixed` o CSS puro: su orden no afecta al layout, y como secciones el cliente las
  prende y apaga sin entrar a los bloques del producto.
- **El cuerpo de la landing se construye con `sec-bloque-alternado.liquid`** (imagen + texto, el
  lado alterna). Menos texto, más imagen, y la página respira sola.
- **El schema JSON-LD vive en su propia sección invisible** (`sec-seo-aio-schema.liquid`), no
  dentro del FAQ: si el cliente apaga o mueve el FAQ, el SEO sobrevive.
- **3 tickers** (arriba, medio, abajo) en vez de 2: el del medio es el respiro entre las dos
  mitades pesadas del embudo.

| # | Fase | Sección | Trabajo | Puerta |
|---|---|---|---|---|
| — | Sistema | **Candado landing** (sección) | Sin salidas al home | |
| — | Sistema | **Ignition** (sección) | Intro cinematográfico, 1 vez por sesión | |
| — | Sistema | **WhatsApp flotante** (sección) | Canal directo, siempre visible | |
| 1 | Atención | Ticker superior | Micro-confianza (envío gratis · contra entrega) | |
| 2 | Oferta | **HERO/main** (galería+título+oferta+precio+**CTA#1**+logística+sticky) | Cierre del comprador caliente | **🚪1** |
| 3 | Problema | Dolor · público A | El cliente se reconoce | |
| 4 | Problema | Dolor · público B *(solo si hay 2 públicos reales)* | El otro perfil se reconoce | |
| 5 | | **CTA#2** (`sec-cta-suelto`) | Cierra al que ya se vio retratado | **🚪2** |
| 6 | Confianza | **Seguridad · objeción #1** | Desactiva el miedo ANTES de las features | |
| 7 | Solución | Mecanismo / cómo actúa | El "ajá" | |
| 8 | Respiro | Ticker medio | Corta entre las dos mitades pesadas | |
| 9 | | **CTA#3** (`sec-cta-suelto`) | Pico de convicción | **🚪3** |
| 10 | Demostración | Secuencia / demo / escalera | Verlo funcionando | |
| 11 | Alcance | Variantes o usos *(si el producto los tiene)* | Cada quién encuentra el suyo | |
| 12 | Uso | Modo de uso | Baja la fricción del "y cómo se usa" | |
| 13 | Calificación | Es para ti | Auto-selección → menos devoluciones | |
| 14 | Prueba social | Reseñas | Confianza de otros | |
| 15 | Respiro | Ticker inferior | | |
| 16 | Oferta | **Escalera de combos** (`sec-combos`) | Sube el ticket. **Obligatoria en `catalogo`** | |
| 17 | Riesgo→0 | Envío + garantía | Reversión de riesgo justo antes del cierre | |
| 18 | Cierre | **CTA final** (`sec-cta-suelto`) | Última puerta | **🚪4** |
| 19 | Objeciones | **FAQ** | El último "pero" cuando ya lo quiere | |
| 20 | Legal | Disclaimer | Ligero, cumplimiento | |
| 21 | SEO/AIO | **Schema invisible** (`sec-seo-aio-schema`) | Google + buscadores con IA | |

**Por PERFIL** (ver `references/perfiles.md`):
- **`marca`** añade manifiesto, historia/origen y línea de productos; la escalera de combos es opcional.
- **`catalogo`** quita manifiesto e historia, y hace **obligatorias** la escalera de combos, la
  demostración y la comparativa.

**Estado por defecto en producción** (aprendido de la página real): countdown, garantía-bloque y
descripción nativa van **apagados** cuando ya hay una sección que hace ese trabajo mejor. No es que
sobren: es que duplicados restan.

**Off por defecto** (ruido / condicional): autoridad (cifras placeholder), ficha técnica, related-products.
WhatsApp flota (posición indiferente) + Sticky siempre visible.

- **Cadencia de CTA:** una puerta cada 2-3 secciones — todas disparan
  `#custom-releasit-btn`. El **FAQ baja a antes del cierre** (G2.6): las objeciones solo importan
  cuando ya hay deseo, así que se resuelven tras la prueba social y justo antes del último CTA.
  La **tranquilidad COD inmediata** (garantía + "pagas al recibir" + logística) ya vive en
  *Riesgo→0* dentro de `main`, así que el comprador caliente no necesita la FAQ arriba.
- **Activos por defecto** (antes off/sueltos): escalera, doble CTA, autoridad, por qué elegir?,
  CTA del manifiesto. **Ficha técnica** va incluida pero **apagada** (solo gadget/kit; sus specs
  son datos duros `[confirmar]` → no se envían activas, REGLA #3).
- **Bloques del main:** config center · propuesta  ·  título · oferta · countdown ·
  verificado · precio · **CTA #1 Releasit** · garantía · barra logística · **descripción** · sticky.

> ✅ Los ejemplos `references/examples/demo-shrine.json` y `references/examples/demo-dawn-v2.json` están **sincronizados
> con la arquitectura actual (G3.8+)**. Aun así, la referencia de orden canónica es **`product.base.json`** (regenerado a las 24 en G4.5);
> ante cualquier duda base-vs-ejemplo, gana el base.
>
Antes del Paso 1, elige **arquetipo** por vertical (define énfasis/orden, no si los bloques
existen — REGLA #4): A) Perfume · B) Salud lean · C) Vitalidad full · D) Gadget/Demo · E) Kit.
Matriz completa en `references/arquetipos.md`.
