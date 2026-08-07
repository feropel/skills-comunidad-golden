---
name: golden-chatea-pro-config-logistico
description: Golden Group — Configura el asistente LOGÍSTICO de Chatea Pro (el PADRE). Deja listo el asistente que valida la dirección del cliente antes del envío contra entrega (COD) para minimizar devoluciones: define los datos operativos del negocio (transportadoras habilitadas para domicilio y recogida en oficina, transportadoras prohibidas, tiempos de entrega por zona) y arma el prompt de validación llamando a su skill HIJA golden-chatea-pro-validacion-direcciones (que trae los packs por país: Colombia patrón oro, Guatemala, Chile, México, Ecuador). Úsala SIEMPRE que el usuario quiera montar o configurar el asistente logístico / de direcciones de Chatea Pro, "configurar logística de chatea pro", "el bot que revisa direcciones antes de despachar", o dejar listo el asistente logístico completo. Para configurar TODOS los asistentes a la vez, usa golden-chatea-pro-full-configuracion.
---

# Golden · Chatea Pro — Asistente Logístico (padre)

Configura el **asistente logístico** de un espacio de trabajo de Chatea Pro. Su misión: **validar la dirección del cliente antes del despacho COD** para minimizar devoluciones y reprocesos de última milla.

Tiene dos niveles:
1. **Config del asistente (esta skill, el padre):** los datos operativos del negocio — transportadoras habilitadas, recogida en oficina, transportadoras prohibidas, tiempos de entrega por zona.
2. **El prompt de validación (la skill hija):** el cerebro que lee la dirección y decide si es entregable. Lo genera `golden-chatea-pro-validacion-direcciones`.

> **Regla de Chatea Pro:** 1 espacio de trabajo = 1 país. Este asistente se configura con el país del workspace.

## Flujo de configuración

### PASO 0 — Intake operativo del negocio (pregunta 1 a la vez, no inventes nada)
1. **País** del workspace.
2. **Transportadoras habilitadas** para **domicilio** (las que el negocio realmente tiene contratadas).
3. Si ofrece **recogida en oficina** y con qué transportadoras.
4. **Transportadoras prohibidas** (ej. en Colombia, muchos negocios no usan Servientrega).
5. **Tiempos de entrega por zona** (capital 2-3 días, intermedia 3-4, rural 5-7) — dato compartido con Ventas y Carritos.
6. Si conserva los emojis de estado (✅/⚠️) en las respuestas.

### PASO 1 — Generar el prompt de validación (delega en la hija)
Con los datos del intake, **invoca `golden-chatea-pro-validacion-direcciones`** pasándole el país y las transportadoras confirmadas. La hija carga el pack del país (Colombia = patrón oro) y devuelve el prompt de validación con:
- Contrato de salida en **una sola línea** (`dirección correcta` / `Para completar su envío, nos regala [dato]?`).
- Interpretación de nomenclatura local, vivienda colectiva, rural y GPS.
- Principio rector: si un mensajero puede llegar sin llamar → válida; si hay riesgo de devolución → falta info.

### PASO 2 — Entregar
Entrega al usuario: (a) el resumen de la config operativa (transportadoras/tiempos), y (b) el prompt de validación listo para pegar en el campo del asistente logístico de Chatea Pro.

## Reglas de oro
- **Nunca inventes transportadoras ni tiempos:** se preguntan/confirman por negocio y país.
- **No reimplementes la validación:** el prompt lo hace la hija `golden-chatea-pro-validacion-direcciones`. Este padre solo aporta los datos operativos y coordina.
- **Tiempos de entrega coherentes** con Ventas (`golden-chatea-pro-config-ventas-wp`) y Carritos (`golden-chatea-pro-config-carritos`).

## Conexiones (skills hermanas)
- 🧭 Hijo — prompt de validación de direcciones → `golden-chatea-pro-validacion-direcciones`
- 🛒 Asistente de ventas (dispara el logístico al pedir la dirección) → `golden-chatea-pro-config-ventas-wp`
- 🔁 Asistente de carritos (mismos tiempos de entrega) → `golden-chatea-pro-config-carritos`
- 🎬 Coordinar los 4 asistentes → `golden-chatea-pro-full-configuracion`

## Privacidad (skill compartible)
Nunca hornees datos reales (transportadoras contratadas, tienda, cuentas) en los archivos de la skill. Se preguntan en cada uso.
