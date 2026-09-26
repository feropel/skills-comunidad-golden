# Los 10 países que acepta la plataforma

**Remedido de primera mano el 2026-09-05** contra el bundle vivo
`https://instalacion-asistentes.chateapro.app/assets/index-BS1l9mqS.js` (501.151 bytes,
<!-- URL EXTERNA, no un archivo de esta skill. El detector de referencias del auditor la marca
     como "mencionada pero NO existe" porque ve el segmento canónico assets/ y la busca en el
     disco. Es un FALSO POSITIVO conocido: el bundle vive en el servidor de Chatea. Se deja el
     esquema https:// delante para que el detector la reconozca como URL y deje de perseguirla. -->
sha256 `e792b3a3…`), constante `me` + tabla de metadata `DA`. Confirma la medición del
2026-08-29 con un bundle distinto: la lista es la misma.

| País | Moneda | Cómo se escribe un precio |
|---|---|---|
| COLOMBIA | COP | `$89.900` — punto de miles, sin decimales |
| ARGENTINA | ARS | `$24.500` — punto de miles, coma decimal |
| BRASIL | BRL | `R$ 149,90` — punto de miles, coma decimal |
| CHILE | CLP | `$24.990` — punto de miles, sin decimales |
| ECUADOR | USD | `$29,90` |
| GUATEMALA | GTQ | `Q199` |
| MEXICO | MXN | `$499` / `$1,299` — coma de miles |
| PANAMA | USD (balboa a la par) | `$29.90` — punto decimal |
| PARAGUAY | PYG | `Gs. 250.000` — punto de miles, sin decimales |
| PERU | PEN | `S/ 89` |

La moneda de cada fila sale del bundle. El **formato** de miles y decimales es convención local,
no viene en el bundle: si el vendedor escribe sus precios de otra forma, manda la suya.

**Contraprueba (lista cerrada):** Bolivia, Uruguay, Venezuela y Costa Rica **no aparecen**. Si el
negocio opera fuera de estos 10, dilo antes de construir nada.

> **Esta lista se REMIDE, no se copia.** El "solo 7 países" que circuló hasta agosto venía de un
> briefing, se copió como verdad y nadie lo volvió a medir — y rechazar una instalación de
> Argentina, Brasil o Guatemala es negocio perdido. Para remedir en 2 comandos: `curl` a
> `https://instalacion-asistentes.chateapro.app/` para sacar el `index-*.js` del día, y buscar en
> ese archivo la constante `const me={COLOMBIA:...}`. Si el resultado difiere de esta tabla,
> **actualízala aquí con la fecha y el hash del bundle**, y avisa al Centro de Mando.

## El valor del campo `[Comentarios IA] País`: copia el que ya está

Medición cruzada, y **no coinciden**: la constante del bundle guarda los valores en **minúscula**
(`"colombia"`, `"mexico"`, `"brasil"`), pero un workspace real en producción tiene el campo con
`COLOMBIA` en **mayúscula** — y funciona.

Regla operativa, hasta que alguien mida cuál acepta el flujo: **si el campo ya tiene valor, NO lo
toques**; si hay que escribirlo de cero, usa la misma forma que ya use esa cuenta en sus otros
campos de país. Sin acentos en ninguno de los dos casos. Esto es un dato de la configuración
general, no del producto: quien lo escribe es `golden-chatea-pro-config-comentarios`.

## 1 · Idioma: BRASIL no es español

**La `desc` y el `rela` se escriben en el idioma en que comenta el cliente.** Para nueve de los
diez eso es español. **Brasil es portugués**, y es el país donde más caro sale copiar la
plantilla de otro:

- La `desc` va en portugués — es el texto con el que el bot responde **en público**.
- El `rela` va en portugués, con sus propias erratas y acentos (`ç`, `ã`, `õ`) y con los hooks
  literales de los copys en portugués.
- El vocabulario comercial cambia entero: `frete` (envío), `entrega`, `pagamento na entrega`
  (contra entrega), `parcelado`, `boleto`, `Pix`.
- El regulador es el **Procon** y el marco es el Código de Defesa do Consumidor.

Si te piden Brasil y no tienes los copys ni la ficha en portugués, **pídelos**: traducir un `rela`
de español a portugués palabra por palabra no empareja comentarios reales, porque la gente no
comenta traduciendo.

## 2 · Vocabulario · aplica siempre

Son las palabras del texto que el bot escribe **en público**. Usar la de otro país delata que el
asistente es de fuera y baja la confianza.

| País | Transporte | El envío a casa | Dinero | Tratamiento |
|---|---|---|---|---|
| COLOMBIA | transportadora, mensajero | domicilio (= el pedido) | plata | tú, cálido |
| ARGENTINA | correo, cadetería | envío a domicilio | plata | vos, cercano |
| BRASIL | transportadora, correios | entrega, frete | dinheiro | você, cordial |
| CHILE | courier, empresa de despacho | despacho | plata | tú, directo |
| ECUADOR | courier, transportadora | envío a domicilio | plata, dinero | usted, cordial |
| GUATEMALA | empresa de envíos | entrega a domicilio | pisto, dinero | usted, cálido |
| MEXICO | paquetería, repartidor | pedido, envío a domicilio | dinero | tú o usted según producto |
| PANAMA | courier | entrega | plata, dinero | tú, cercano |
| PARAGUAY | courier, empresa de envíos | envío a domicilio | plata | vos, usted, cálido |
| PERU | courier | envío a domicilio | plata | usted, amable |

> **Ojo con "domicilio".** En Colombia el domicilio es **el pedido**; en México es **la casa**. Un
> texto que diga "para recibir tu domicilio" no se entiende en México.

El vocabulario de esta tabla es criterio de la casa, no medición del bundle: si el vendedor usa
otra palabra en su mercado, manda la suya.

## 3 · Modelo de pago

**Contra entrega es el default de esta operación** y así se escribe en la `desc`. Pero la marca
propia suele ir con pago anticipado, y en Brasil el estándar local es Pix o boleto. Si el vendedor
no lo dice, ponlo como supuesto en el borrador y sigue: es una línea de la `desc`, no una ronda de
preguntas.

## 4 · Claims y regulador · aplica siempre

En los 10 países la frontera es la misma y no hay margen: un cosmético o un suplemento **no cura,
no trata, no elimina** nada. Cambia el regulador (SIC en Colombia, PROFECO en México, Procon en
Brasil, su equivalente local en los demás), no la regla. Se escribe en el bloque de **reglas de
marca** de la `desc` (ver `desc-plantilla.md`).

No es cautela decorativa: el asistente responde **en público, en el post**, donde cualquiera —el
regulador y la competencia incluidos— puede leerlo y capturarlo.

## 5 · Detalle Colombia / México

Solo para quien trabaje esos dos. **De los otros ocho está verificada la moneda (bundle) y
propuesto el vocabulario: no afirmes en la `desc` lo que no esté confirmado** — sobre todo si hay
recolección en oficina o no. Si el vendedor no lo dice, no lo menciones.

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

## La trampa: un país copiado de otro hereda el criterio equivocado

Es el error más caro de esta familia de skills y ya mordió dos veces:

1. Una plantilla de México decía *"NUNCA exijas código postal"* — falso: en México el CP es
   **requerido**. Era criterio de Colombia copiado tal cual.
2. Este mismo archivo decía *"7 países… no hay más, ni Argentina ni Guatemala"* durante una
   semana **después** de que la casa remidiera 10. La corrección del 29-ago cambió los conteos del
   `SKILL.md` y no abrió este archivo. Una lista negada es más cara que un número desactualizado:
   el número confunde, la negación **rechaza a un cliente que sí se podía instalar**.

Cuando adaptes un producto de un país a otro, **revisa campo por campo**, y cuando corrijas un
conteo, abre también el archivo que tiene la lista.
