# Packs por país (COD / venta conversacional LatAm)

## 10 PAÍSES (corregido 2026-09-05 — antes decía 7 y era FALSO)
Chatea Pro acepta **10 países** (remedido 2026-08-29 por la familia). Hay PACK completo para 8: **COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY, GUATEMALA**. **ARGENTINA y BRASIL** están soportados por la plataforma pero AÚN SIN PACK: hueco declarado — se le preguntan los datos de dirección y logística al negocio, no se inventan ni se clonan de otro país.
🔴 Esta ficha decía "SOLO 7 PAÍSES... nada de Guatemala" hasta 2026-09-05, contradiciendo a `golden-chatea-pro-validacion-direcciones` y a `config-ventas-wp`, que ya decían 10. Consecuencia real: la skill le negaba el servicio a un cliente activo del ecosistema en Guatemala. **Lección: cuando dos skills hermanas discrepan sobre un dato de plataforma, gana la que lo REMIDIÓ, y la fecha de medición debe ir escrita al lado del número.**
⚠️ País clonado de otra plantilla HEREDA el criterio equivocado (caso real: el pack México decía "nunca exijas código postal", criterio de Colombia copiado). Revisa el pack del país, no asumas.
## Tiempos de entrega DEFAULT (regla de FER: NO se preguntan)
Los tiempos de entrega NO se le preguntan al vendedor: se aplican estos predeterminados (todos los países LatAm COD) y se muestran en el borrador como supuesto; solo se ajustan si el vendedor los corrige por iniciativa propia.
```
Ciudades principales: 2 a 3 días hábiles
Intermedias: 3 a 5 días hábiles
Rurales: 5 a 7 días hábiles
Lunes a sábado, 8am a 6pm
```
Transportadora default: "varias transportadoras seguras según tu zona" (sin nombrar una). Solo se nombra o excluye una transportadora si el vendedor lo dice por su cuenta.

Al construir, usa el pack del país del negocio: nomenclatura de dirección, medios de pago y tono. Conserva SIEMPRE los mismos emojis del bloque de captura (ver plantilla-prompt.md), solo cambian los campos.

## 🇨🇴 Colombia (patrón oro)
- **Vocabulario:** transportadora · domicilio (= el pedido) · plata · mensajero. Regulador: SIC.
- **Dirección:** 🆔 Nombre · 🏙 Ciudad · 🗺 Departamento · 🏠 Dirección u OFICINA · 📍 Barrio · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Coordinadora, Servientrega, Interrapidísimo, Envía, TCC.
- **Pago anticipado:** Nequi, Daviplata, Bancolombia (llave/QR).
- **Tono:** cálido, cercano, "tú"/"vos" según región. Moneda: COP ($59.000).

## 🇲🇽 México
- **Dirección:** 🆔 Nombre · 🏠 Calle y número · 🏘 Colonia · 🏙 Municipio o Alcaldía · 🗺 Estado · 🔢 Código Postal (**REQUERIDO** — define la zona de reparto, jamás omitirlo) · 🔢 Cantidad · 💳 Pago
- ⛔ **NO EXISTE recolección en oficina**: todo se entrega a domicilio. El prompt mexicano NUNCA ofrece "recoger en oficina".
- **Zonificación:** metropolitana / interior de la república / alejadas (no "principal/intermedia/rural").
- **Vocabulario:** paquetería (no transportadora) · pedido (no domicilio) · dinero (no plata) · repartidor (no mensajero). ⚠️ "domicilio" en México es LA CASA, no el pedido: "para recibir tu domicilio" no se entiende — di "para recibir tu pedido". Regulador: PROFECO.
- **Particulares:** Supermanzana en Quintana Roo · alcaldía en CDMX.
- **Transportadoras:** Estafeta, Paquetexpress, FedEx, DHL, Sendex.
- **Pago anticipado:** SPEI, transferencia, OXXO (depósito).
- **Tono:** cordial, "usted"/"tú" según producto. Moneda: MXN ($499).

## 🇵🇪 Perú
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Distrito · 🏙 Provincia · 🗺 Departamento · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Olva Courier, Shalom, Marvisur.
- **Pago anticipado:** Yape, Plin, transferencia BCP/Interbank.
- **Tono:** amable, "usted" frecuente. Moneda: PEN (S/ 89).

## 🇨🇱 Chile
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Comuna · 🗺 Región · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Chilexpress, Starken, Correos de Chile, Bluexpress.
- **Pago anticipado:** transferencia, Mercado Pago, Webpay.
- **Tono:** directo, cercano. Moneda: CLP ($24.990).

## 🇪🇨 Ecuador
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Ciudad · 🗺 Provincia · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Servientrega, Laarcourier, Tramaco.
- **Pago anticipado:** transferencia, Deuna, Payphone.
- **Tono:** cordial. Moneda: USD ($29,90).

## 🇵🇦 Panamá
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Corregimiento · 🗺 Provincia · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** las define la operación local — usa el default "varias transportadoras según tu zona" y solo nombra una si el vendedor la da.
- **Vocabulario:** pedido · repartidor · dinero (neutro; confirma modismos con el vendedor).
- **Pago anticipado:** transferencia, Yappy.
- **Tono:** cercano. Moneda: USD ($29.90).

## 🇵🇾 Paraguay
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Ciudad · 🗺 Departamento · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** las define la operación local — usa el default "varias transportadoras según tu zona" y solo nombra una si el vendedor la da.
- **Vocabulario:** pedido · repartidor · plata (voseo; confirma modismos con el vendedor).
- **Pago anticipado:** transferencia, giros.
- **Tono:** cercano, voseo suave. Moneda: PYG (Gs. 150.000).

## 🇬🇹 Guatemala
- **Dirección:** 🆔 Nombre · 📱 Teléfono · 🗺 Departamento · 🏙 Ciudad/Municipio · 🏠 Dirección completa · 📍 **ZONA** (particularidad guatemalteca: las ciudades se organizan por zonas — zona 1, zona 10; sin zona el mensajero no llega) · 📍 Punto de referencia · 🔢 Cantidad · 💳 Pago
- **Moneda:** quetzales, con espacio tras la Q: `Q 189` · `Q 249` · `Q 299`.
- **Vocabulario:** pedido · repartidor · pisto (dinero, coloquial) · "va pues" para cerrar. Tono amable, claro y cercano.
- **Transportadoras:** las define la operación local — usa el default "varias transportadoras según tu zona" y solo nombra una si el vendedor la da.
- **Pago anticipado:** transferencia bancaria, depósito. Confirma con el vendedor qué usa de verdad.

## FORMATO DE LA MONEDA (se escribe distinto en cada país y el bot lo nota)
Colombia `$59.900` · México `$499` · Guatemala `Q 189` · Ecuador `$29,90 USD` · Perú `S/ 89` · Chile `$24.990` · Panamá `$29.90` · Paraguay `Gs. 150.000`.
Escribir la moneda como no se escribe en ese país delata al bot en el primer mensaje de precio, que es justo donde más se lee.

## Regla
Solo los 10 países de la plataforma (8 con pack, 2 declarados sin pack). Nunca uses "barrio/departamento" (CO) en un país que usa "colonia/estado" (MX), y revisa SIEMPRE el pack del país destino antes de construir: cada campo de captura, la zonificación y el vocabulario salen del pack, no de otra plantilla.
