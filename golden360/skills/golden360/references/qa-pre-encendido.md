# COMPUERTA 4 · QA antes de encender

Nada se enciende sin esto probado. No es una revisión visual: son cinco pruebas con evidencia.
Motor: `golden-qa` (funcional) y, si hay servidor, `webapp-testing`.

## 1 · Render real

- **390 / 768 / PC**, midiendo el DOM, no a ojo ni por porcentajes.
- Sin desborde horizontal en ningún ancho; tablas, bloques anchos y videos con su propio scroll.
- El **CTA nunca queda oculto** por revelados, sticky o popups.
- Evidencia: capturas de los tres anchos.

## 2 · El botón de WhatsApp dispara el bot de verdad

- Se pulsa el botón y se verifica que **abre WhatsApp con la keyword correcta**, la misma del expediente.
- Se verifica que **el bot responde** a esa keyword con el flujo del producto.
- Si `activacion.cargado_en_bot` es `false`, **el botón no se monta**. Un botón que dispara a un bot
  que no conoce el producto es un embudo roto: el cliente escribe y no pasa nada.

## 3 · Orden de prueba completa

- Se llena el formulario COD como lo haría un cliente y se envía.
- Se verifica que **la orden aparece donde tiene que aparecer** (Shopify, y de ahí a Dropi si aplica).
- Se anota **quién creó la orden** (formulario COD, bot, API) porque eso explica la atribución después.
- Se borra o marca la orden de prueba.

## 4 · Medición viva

- **Pixel + CAPI** instalados y disparando.
- **Evento de compra probado** de punta a punta, no solo "el pixel carga".
- **Dominio verificado** y evento de conversión priorizado correctamente.
- Sin señal de compra probada, la pauta no aprende y el test no sirve: esto es bloqueante.

> **El referrer de Shopify NO atribuye nada.** Las órdenes que nacen en el formulario COD, en el bot
> o por API llegan **en blanco**. En una tienda real el 94% de las órdenes de un producto figuraban
> sin referrer. Quien lea el referrer para decidir el origen del tráfico, se equivoca. Para atribuir
> se cruza gasto de pauta contra órdenes reales por ventana de tiempo.

## 5 · Peso y consola

- Cada imagen **<150 KB** en WebP, con `width`, `height` y `alt` (sin CLS).
- Video con carga diferida.
- **Cero errores en consola**.
- Las imágenes "cuadradas" que no son 1:1 exactas se recortan antes de subir.

## Salida

Checklist con ✅ / ❌ por prueba y la evidencia adjunta. **Un ❌ en las pruebas 2, 3 o 4 bloquea el
encendido**; un ❌ en 1 o 5 se corrige antes de gastar, no después.

Se escribe al expediente: `activacion.evento_probado` y `estado.compuertas_pasadas`.
