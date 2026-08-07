# Packs por país (COD / venta conversacional LatAm)

Al construir, usa el pack del país del negocio: nomenclatura de dirección, medios de pago y tono. Conserva SIEMPRE los mismos emojis del bloque de captura (ver plantilla-prompt.md), solo cambian los campos.

## 🇨🇴 Colombia (patrón oro)
- **Dirección:** 🆔 Nombre · 🏙 Ciudad · 🗺 Departamento · 🏠 Dirección u OFICINA · 📍 Barrio · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Coordinadora, Servientrega, Interrapidísimo, Envía, TCC.
- **Pago anticipado:** Nequi, Daviplata, Bancolombia (llave/QR).
- **Tono:** cálido, cercano, "tú"/"vos" según región. Moneda: COP ($59.000).

## 🇲🇽 México
- **Dirección:** 🆔 Nombre · 🏠 Calle y número · 🏘 Colonia · 🏙 Municipio/Alcaldía · 🗺 Estado · 🔢 CP · 🔢 Cantidad · 💳 Pago
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

## 🇬🇹 Guatemala
- **Dirección:** 🆔 Nombre · 🏠 Dirección · 🏙 Municipio · 🗺 Departamento · 📍 Zona · 📍 Referencia · 🔢 Cantidad · 💳 Pago
- **Transportadoras:** Guatex, Cargo Expreso, Forza.
- **Pago anticipado:** transferencia, depósito bancario.
- **Tono:** cálido, "usted". Moneda: GTQ (Q199).

## Regla
Si el país no está listado, pregunta la nomenclatura de dirección y los medios de pago locales, y arma el pack sobre la marcha. Nunca uses "barrio/departamento" (CO) en un país que usa "colonia/estado" (MX).
