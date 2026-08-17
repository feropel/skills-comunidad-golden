# Países y tiempos de entrega

El **país define los tiempos de entrega** que van en la landing (barra logística,
copy de envío, FAQ "cuánto demora?", garantía). Usar las fechas equivocadas es un
error grave: rompe la promesa y genera reclamos. **NUNCA poner fechas de un país en otro.**

## Tabla de tiempos (datos confirmados por el usuario)

### 🇬🇹 Guatemala
- **Entrega total: 1 a 4 días hábiles.**
- Copy sugerido: "Recíbelo en **1 a 4 días hábiles**. Pagas al recibir."

### 🇨🇴 Colombia (más lento — desglose real)
- **Preparación / despacho:** 1 día (el mismo día del pedido o el siguiente).
- **Tránsito de la transportadora:** 2 a 3 días.
- **Entrega final total: 3 a 7 días hábiles** (según ciudad; capitales más rápido,
  zonas alejadas hasta 7).
- Copy sugerido: "Recíbelo en **3 a 7 días hábiles**. Pagas al recibir, en la puerta
  de tu casa." (No prometer 1-4 días en Colombia.)
- **Barra logística (3 pasos) — formato preferido por el usuario:**
  Pedido realizado **Día 1** · En camino **2-3 días** · Entrega estimada **3-7 días**.
  Usar SOLO esa barra pequeña; NO añadir un bloque grande extra de tiempos (queda duplicado).
- Desglose por ciudad (solo referencia interna, NO ponerlo como bloque): principal 2-3 ·
  intermedia 3-4 · rural 5-7 días hábiles.

## Regla de oro
- Si el país **NO está en esta tabla**, **pregúntale al cliente** los tiempos reales
  (preparación + tránsito + entrega) antes de construir. No inventar ni asumir.
- Una vez confirmado un país nuevo, **absórbelo aquí** (ritual de auto-mejora) para
  no volver a preguntarlo.
- Ajustar SIEMPRE: barra logística (`componentes/10-barra-logistica.liquid`), el copy
  de envío, la FAQ de tiempos y la garantía al país correcto.

## Error real a no repetir
En el proyecto "Tienda Demo/banca" se pusieron fechas de **Guatemala (1-4 días)** cuando el
país podía ser **Colombia (3-7 días)**. Confirmar el país ANTES de escribir cualquier
fecha de entrega.
