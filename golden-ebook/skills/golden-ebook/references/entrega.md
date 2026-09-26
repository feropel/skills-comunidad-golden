# Entrega: cuándo y cómo le llega al cliente

Lee este archivo en el **Paso 6**, cuando el PDF ya pasó el verificador.

## El momento

El ebook se entrega **cuando se genera la guía de envío**, no antes ni después de la entrega:

- Antes de la guía el cliente todavía no sabe si el pedido salió; el libro se siente como relleno.
- Después de la entrega ya tiene el producto y el libro compite con abrir la caja.
- Entre la guía y la entrega (2 a 6 días en Colombia) está la ventana en la que el cliente se
  enfría. En contra entrega el rechazo crece con los días de espera (ver `evidencia.md`).

En Chatea Pro eso corresponde a los ganchos del **asistente logístico**: "Guía Generada" (el que
entrega el ebook) y "Reparto" (el que lo recuerda). Cada gancho tiene un tope de 3.000 caracteres
(medido en el espacio de Golden el 2026-08; verificar en vivo). **Esta skill no configura Chatea**:
entrega el PDF, el enlace y los textos, y la configuración la hace `golden-chatea-pro-config-logistico`.

## Dónde se aloja el PDF

El mensaje necesita un enlace público y estable. En orden de preferencia:

1. **Archivos de Shopify** de la tienda (Contenido, Archivos): enlace del CDN de la propia marca.
   Súbelo con el método de archivos grandes de la tienda y **abre el enlace en una ventana privada
   antes de usarlo**: una subida puede aceptarse sin escribir nada.
2. La web de la marca, si tiene una carpeta pública.
3. Google Drive con "cualquiera con el enlace puede ver", como último recurso: pide inicio de
   sesión en algunos celulares y se ve menos profesional.

Adjuntar el PDF como documento de WhatsApp muestra la portada como miniatura, lo que ayuda a que se
abra. Si el canal lo permite, adjúntalo; si solo acepta texto, manda el enlace.

## Textos para los ganchos

Van **sin signos de apertura** (es un mensaje que simula a una persona escribiendo) y sin promesas
del producto. Reemplaza lo que va entre llaves.

**Guía generada (entrega el libro):**

```
{nombre}, tu pedido ya salió 📦 Tu guía es {guia} con {transportadora}.

Mientras llega te preparamos un regalo: un libro corto sobre {tema en 5 palabras}. Son {minutos} minutos de lectura y lo puedes leer desde el celular 👇
{enlace}
```

**Reparto (lo recuerda y prepara la entrega):**

```
{nombre}, hoy tu pedido sale a reparto 🚚 Ten listo el pago de {valor} para recibirlo.

Si no alcanzaste a leer tu libro, el capítulo {n} se lee en {minutos} minutos: {titulo del capitulo} 👇
{enlace}
```

El segundo mensaje no repite el libro entero: apunta a UN capítulo concreto, que es más fácil de
abrir que un libro completo. Los `{minutos}` se calculan con las palabras de ese capítulo a 230 por
minuto, redondeando hacia arriba: nunca se ponen a ojo.

## Cómo saber si funciona

No existe un estudio publicado que mida el efecto de un contenido de valor sobre el rechazo en
contra entrega. Se mide con la operación propia:

1. Durante 2 a 4 semanas, manda el ebook a la mitad de los pedidos (por ejemplo, número de pedido
   par) y a la otra mitad no.
2. Compara la **tasa de entrega efectiva** de los dos grupos con los datos de Dropi
   (`golden-dropi-analisis` o `golden-logistica-diaria`).
3. Con menos de unos 300 pedidos por grupo, la diferencia puede ser ruido: dilo en el informe en
   vez de declarar un ganador.
4. Mide también las aperturas del enlace si el alojamiento las cuenta.

Hasta tener ese resultado, el informe dice "sin medir", nunca "reduce el rechazo".
