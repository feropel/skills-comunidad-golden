# Los 7 países que acepta la plataforma

El campo `[Comentarios IA] País` los lista literalmente, **en mayúscula y sin acentos**:

```
COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY
```

**No hay más.** Ni Argentina, ni Bolivia, ni Costa Rica, ni Guatemala. Si el negocio opera fuera de
esta lista, dilo antes de construir nada: la parametrización del asistente no lo va a contemplar.

*(La mayúscula sin acentos es solo para ese campo. La `desc` y el `rela` del producto van con
tildes normales.)*

---

## 1 · Moneda y formato · aplica siempre

Un precio mal formateado se lee como otro precio.

| País | Moneda | Cómo se escribe |
|---|---|---|
| COLOMBIA | COP | `$89.900` — punto de miles, sin decimales |
| ECUADOR | USD | `$29,90` — dólar con decimales |
| CHILE | CLP | `$24.990` — punto de miles, sin decimales |
| MEXICO | MXN | `$499` / `$1,299` — coma de miles |
| PANAMA | USD (balboa a la par) | `$29.90` — punto decimal |
| PERU | PEN | `S/ 89` |
| PARAGUAY | PYG | `Gs. 250.000` — punto de miles, sin decimales |

Nunca escribas el precio crudo (`59900`): el bot lo lee tal cual y lo dice así en público.

---

## 2 · Vocabulario · aplica siempre

Son las palabras del texto que el bot escribe **en público**. Usar la de otro país delata que el
asistente es de fuera y baja la confianza.

| País | Transporte | El envío a casa | Dinero | Tratamiento |
|---|---|---|---|---|
| COLOMBIA | transportadora, mensajero | domicilio (= el pedido) | plata | tú, cálido |
| ECUADOR | courier / transportadora | envío a domicilio | plata / dinero | usted, cordial |
| CHILE | courier / empresa de despacho | despacho | plata | tú, directo |
| MEXICO | paquetería, repartidor | pedido, envío a domicilio | dinero | tú o usted según producto |
| PANAMA | courier | entrega | plata / dinero | tú, cercano |
| PERU | courier | envío a domicilio | plata | usted, amable |
| PARAGUAY | courier / empresa de envíos | envío a domicilio | plata | vos / usted, cálido |

> **Ojo con "domicilio".** En Colombia el domicilio es **el pedido**; en México es **la casa**. Un
> texto que diga "para recibir tu domicilio" no se entiende en México.

---

## 3 · Modelo de pago

**Contra entrega es el default de esta operación** y así se escribe en la `desc`. Pero la marca
propia suele ir con pago anticipado. Si el vendedor no lo dice, ponlo como supuesto en el borrador
y sigue: es una línea de la `desc`, no una ronda de preguntas.

---

## 4 · Claims y regulador · aplica siempre

En los 7 países la frontera es la misma y no hay margen: un cosmético o un suplemento **no cura,
no trata, no elimina** nada. Cambia el regulador (SIC en Colombia, PROFECO en México, su
equivalente local en los demás), no la regla. Se escribe en el bloque de **reglas de marca** de la
`desc` (ver `desc-plantilla.md`).

No es cautela decorativa: el asistente responde **en público, en el post**, donde cualquiera —el
regulador y la competencia incluidos— puede leerlo y capturarlo.

---

## 5 · Detalle Colombia / México

Solo para quien trabaje esos dos. **De los otros cinco está verificada la moneda y el vocabulario,
nada más: no afirmes en la `desc` lo que no esté confirmado** — sobre todo si hay recolección en
oficina o no. Si el vendedor no lo dice, no lo menciones.

| | 🇨🇴 COLOMBIA | 🇲🇽 MEXICO |
|---|---|---|
| División territorial | departamento · ciudad · barrio | Estado · municipio o alcaldía · colonia |
| Código postal | no se exige | **REQUERIDO**, define la zona de reparto |
| Recolección en oficina | sí, oficina de la transportadora | **NO EXISTE**, todo a domicilio |
| Zonificación | principal / intermedia / lejana | metropolitana / interior de la república / alejadas |
| Regulador | SIC | PROFECO |
| Particular | — | Supermanzana en Quintana Roo · alcaldía en CDMX |

*(La nomenclatura de dirección afecta sobre todo al campo `datos_req` de la configuración general
—`golden-chatea-pro-config-comentarios`— y al asistente logístico. Aquí importa por el vocabulario
y por no prometer una modalidad de entrega que en ese país no existe.)*

---

## La trampa: un país copiado de otro hereda el criterio equivocado

Es el error más caro de esta familia de skills y ya mordió una vez. Una plantilla de México decía
*"NUNCA exijas código postal"* — falso: en México el CP es **requerido**. Era criterio de Colombia
copiado tal cual.

Cuando adaptes un producto de un país a otro, **revisa campo por campo**. No asumas que lo único
que cambia es la moneda.
