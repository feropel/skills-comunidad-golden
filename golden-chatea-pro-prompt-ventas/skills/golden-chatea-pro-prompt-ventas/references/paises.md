# Packs por país (COD / venta conversacional LatAm)

## SOLO 7 PAÍSES (tope de la plataforma)
Chatea Pro solo acepta estos países, en mayúscula y sin acentos: **COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY**. Nada de Guatemala, Argentina, Bolivia ni Costa Rica. Si el vendedor está en un país no listado, avísale que la plataforma no lo soporta.
⚠️ País clonado de otra plantilla HEREDA el criterio equivocado (caso real: el pack México decía "nunca exijas código postal" — era criterio de Colombia copiado). Revisa el pack del país, no asumas.

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

## Regla
Solo los 7 países de la plataforma. Nunca uses "barrio/departamento" (CO) en un país que usa "colonia/estado" (MX), y revisa SIEMPRE el pack del país destino antes de construir: cada campo de captura, la zonificación y el vocabulario salen del pack, no de otra plantilla.
