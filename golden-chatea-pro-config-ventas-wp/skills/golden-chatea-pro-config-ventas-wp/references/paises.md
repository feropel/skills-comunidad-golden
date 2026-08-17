# Países — parametrización del asistente de ventas WhatsApp

Chatea Pro **solo acepta 7 países** (campo `[Comentarios IA] País`, en mayúscula y sin
acentos): **COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY**. No existe
Guatemala, Argentina, Bolivia ni Costa Rica. `build_config.py` rechaza cualquier otro.

En el JSON de ventas-wp, `conexion_con_dropi.pais` va en **minúscula** (ej: `colombia`), pero
debe ser uno de esos 7.

Fuente: briefing de instalación de Chatea Pro (verificado en vivo 2026-08-07 contra dos
workspaces reales).

## Lo que cambia por país (y no es solo el acento)

Estos deltas afectan sobre todo a los TEXTOS de venta (prompt del producto, que hace
`golden-chatea-pro-prompt-ventas`) y a la validación de direcciones (asistente logístico). Aquí
se documentan para que quien llene los textos del producto no arrastre el criterio de otro país.

| | Colombia (patrón oro) | México |
|---|---|---|
| División geográfica | departamento · ciudad · barrio | estado · municipio o alcaldía · colonia |
| Código postal | no se exige | **REQUERIDO** — define la zona de reparto |
| Recolección en oficina | sí (oficina de la transportadora) | **NO EXISTE** — todo a domicilio |
| Zonificación | principal / intermedia / lejana | metropolitana / interior de la república / alejadas |
| Regulador | SIC | PROFECO |
| Vocabulario | transportadora · domicilio (=el pedido) · plata · mensajero | paquetería · pedido · dinero · repartidor |
| Particular | — | Supermanzana en Quintana Roo · alcaldía en CDMX |

**Ecuador, Chile, Panamá, Perú, Paraguay:** usan su propia división administrativa y
vocabulario; los packs por país viven en `golden-chatea-pro-validacion-direcciones`. Al
parametrizar un país nuevo, NO copies el criterio de Colombia: revísalo uno por uno.

## Trampas verificadas

- **"Domicilio" cambia de significado.** En Colombia el domicilio es el PEDIDO; en México es la
  CASA. Un mensaje que diga "para recibir tu domicilio" no se entiende en México. En los textos
  del producto, usar el vocabulario del país.
- **Código postal en México.** La plantilla `03-MEXICO-v100.md` decía "NUNCA exijas código
  postal" — era criterio de Colombia copiado. En México el CP es obligatorio. Cualquier país
  clonado de otra plantilla hereda el criterio equivocado: revisar, no asumir.
- El país NO cambia la ESTRUCTURA del JSON de ventas-wp (las claves son las mismas); cambia el
  valor de `pais`, la `moneda`, los tiempos de entrega y el vocabulario de los textos.
