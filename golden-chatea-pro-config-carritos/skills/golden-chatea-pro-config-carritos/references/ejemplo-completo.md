# Ejemplo completo — Secuencia de carritos abandonados (FICTICIO)

> Vara de calidad de la salida. **Datos inventados** (producto, precio, marca): en uso real todo se pregunta y nunca se hornea en la skill. Sirve para calibrar tono, longitud y formato de entrega.

## Contexto ficticio del intake
- **País:** Colombia
- **Producto / oferta:** Sérum Aurora 30 ml — 1 und $89.900 · 2 und $149.900 (envío gratis)
- **Pago:** Contra entrega + anticipado (cuenta que entregue el negocio)
- **Incentivo de recuperación:** envío gratis + mini-muestra de regalo en el último intento
- **Tiempos de entrega:** capital 2-3 días, intermedia 3-4, rural 5-7
- **Asistente:** "Vale", tono cálido y cercano
- **Prueba social real (confirmada por el negocio en el intake):** 12.000 clientas — dato ficticio de este ejemplo, pero en uso real solo se escribe si el negocio la entrega; sin ella, REACTIVACIÓN 2 se apoya en garantía y contra entrega, nunca en una cifra inventada.
- **Tipo de contacto:** carrito frío (dejó el checkout en la tienda, no había escrito al WhatsApp) → el primer toque necesita plantilla de Meta

---

## Secuencia entregada

### REACTIVACIÓN 1 — recordatorio suave
*Dispara a ~20-30 min · contacto frío → con plantilla de Meta*

**Plantilla de Meta**
- **Nombre:** `carrito_recordatorio`
- **Categoría:** Marketing · **Idioma:** español
- **Cuerpo:**
```
Hola {{1}}, soy Vale 🙂 vi que dejaste tu Sérum Aurora casi listo. Te ayudo a cerrar el pedido en 1 minuto, lo quieres para 1 o 2 unidades.
```
- **Botón:** Respuesta rápida → "Sí, ayúdame"

---

### REACTIVACIÓN 2 — resolver objeción (confianza + pago)
*Dispara a ~3-4 h · si el cliente ya respondió va como texto libre; si sigue frío, con plantilla*

```
Con el Sérum Aurora no arriesgas nada: pagas contra entrega cuando lo recibes en tu casa. Más de 12.000 clientas ya lo usan. Te lo despacho hoy.
```

---

### REACTIVACIÓN 3 — urgencia honesta
*Dispara a ~20-24 h · texto libre si la ventana sigue abierta; con plantilla si ya pasó de 24 h*

```
Nos queda poco stock de esta tanda del Sérum Aurora y la promo de envío gratis cierra pronto. Te aparto el tuyo hoy, lo confirmo.
```

---

### REACTIVACIÓN 4 — último intento + incentivo
*Dispara a ~24-48 h · casi siempre fuera de las 24 h → con plantilla de Meta*

**Plantilla de Meta**
- **Nombre:** `carrito_ultimo_intento`
- **Categoría:** Marketing · **Idioma:** español
- **Cuerpo:**
```
Hola {{1}}, te guardé tu Sérum Aurora con envío gratis y una mini-muestra de regalo. Lo activo hoy y te llega contra entrega. Lo cerramos.
```
- **Botón:** Respuesta rápida → "Sí, lo quiero"

**Campo Instrucción especial (mensaje + [Instrucción IA])**
```
Hola {{1}}, te guardé tu Sérum Aurora con envío gratis y una mini-muestra de regalo. Lo activo hoy y te llega contra entrega. Lo cerramos.
[Instrucción IA: si responde que sí, dispara el flujo de venta/logístico para tomar la dirección y confirmar el pedido. Si tiene una objeción, resuélvela y ofrece cerrar contra entrega. No repitas descuento si ya lo diste. Máximo 1 reactivación más y suelta.]
```

---

## Resumen de configuración (lo que se pega en el módulo Carritos)

| Etiqueta | Ángulo | Tiempo | Plantilla Meta |
|----------|--------|--------|----------------|
| REACTIVACIÓN 1 | Recordatorio suave | 20-30 min | `carrito_recordatorio` (contacto frío) |
| REACTIVACIÓN 2 | Confianza + pago COD | 3-4 h | Texto libre si respondió · plantilla si sigue frío |
| REACTIVACIÓN 3 | Urgencia honesta | 20-24 h | Texto libre en ventana · plantilla si pasó 24 h |
| REACTIVACIÓN 4 | Último intento + incentivo | 24-48 h | `carrito_ultimo_intento` |

Al cerrar cualquier paso, el control pasa al **asistente de ventas/logístico** para dirección y confirmación. Este asistente no valida direcciones (eso es `golden-chatea-pro-config-logistico`).

> Las etiquetas `REACTIVACIÓN N` son neutrales a propósito: cuando se verifiquen en vivo los nombres reales de los campos del módulo Carritos, se renombran para que calcen con el módulo.
