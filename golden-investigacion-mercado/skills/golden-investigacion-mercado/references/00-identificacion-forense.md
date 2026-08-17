# FASE -1 · Identificación forense (de una foto a un producto real)

El arranque normal no es un brief: es **una foto de un producto que el dueño vio por ahí**. Sin
nombre oficial, sin URL, sin fabricante, sin saber si está en Dropi ni a qué costo. Sacar todo eso
es trabajo de esta fase, no un dato que el usuario deba traer.

Salida obligatoria: `PRODUCTO.json` con `identidad` y `producto_real` llenos, cada dato con fuente.

## Paso 1 · Leer la etiqueta (de la imagen, jamás de memoria)

Extraer del envase, literal:
- **Nombre exacto** del producto (el de la etiqueta, no el que le dice el vendedor)
- **Marca** y país de origen
- **Contenido neto** (ml, g, fl oz, unidades) — anotar las DOS unidades si vienen
- **Activos del frente con porcentajes** (ej. "4% X, 2.5% Y")
- **Registro sanitario** si aparece (INVIMA, ISP, FDA, CE)
- Cualquier claim impreso (sirve después para la Compuerta 2)

Si la foto no permite leer algo, se marca `[ILEGIBLE]` y se pide otra foto de ese lado. No se
completa por parecido ni por lo que "suele decir" ese tipo de producto.

## Paso 2 · Llegar al fabricante

Buscar marca + nombre exacto hasta dar con la **ficha oficial del fabricante**. De ahí se saca lo
que la foto no da:
- **INCI completo** (lista de ingredientes en orden) → es lo que decide qué claims son legales
- **Modo de uso oficial** (cuántas veces al día, dónde, con qué)
- **Tiempos reales de resultado** (ej. visibles a 4 semanas, serios a 8)
- **Para qué tipo de piel/persona** lo posiciona el fabricante
- **Claims de la marca** y si son autorreportados o de estudio

Precedente: con solo el packshot se consiguió el INCI oficial del fabricante, mismo SKU, y eso
desmontó tres claims que la ficha viva afirmaba. **No hace falta tener el frasco en la mano.**

Contrastar siempre: los sitios afiliados inventan atributos que la marca nunca dijo. La fuente
válida es el fabricante, no un revendedor.

## 🚧 COMPUERTA DE IDENTIDAD DEL PRODUCTO (paso duro, ANTES de cualquier claim de ingrediente)

**La versión local puede declarar OTRA FÓRMULA que la marca original.** Caso real (chat Dental
el producto del estudio, Chile, 2026-08-07): los revendedores chilenos del mismo frasco declaraban
**glicerina, pantenol y PCA de sodio** — humectantes — mientras la marca original (Amazon
B0DB2ZBXZD, US$69) declara **nano-hidroxiapatita** como activo. El ingrediente estrella podría
no estar en el frasco que se despacha.

Reglas de la compuerta:
1. **Rastrear el producto ORIGINAL** (Amazon / eBay / AliExpress) para obtener **costo real,
   contenido (ml) e ingredientes declarados por la marca de origen**, y contrastarlos contra lo
   que declara la versión local que el negocio va a despachar.
2. **PROHIBIDO escribir un claim de ingrediente sin la foto macro de la etiqueta del frasco que
   el dueño va a despachar.** Ni el listing original ni el del revendedor sustituyen esa foto:
   son dos fuentes que pueden describir dos fórmulas distintas.
3. Si las fórmulas difieren o la etiqueta local no se ha visto, el ingrediente entra al
   expediente como `[PENDIENTE]` / `claims.no_verificables` y NINGÚN copy lo afirma.

Es la regla anti-invención aplicada a la ficha técnica: no basta con que el dato tenga fuente —
tiene que ser la fuente del frasco que de verdad viaja en el paquete.

## 🚧 El NOMBRE del producto es un ítem de COMPLIANCE (evaluarlo en esta fase)

Un nombre puede prometer cura: **"Dental el producto del estudio" promete curación** — era el mayor
pasivo legal del negocio y ninguna revisión lo detectaba, porque el mapa de compliance mira el
copy, no el nombre. Regla: evaluar el nombre en Fase 0/1 y, si promete cura o resultado médico,
**proponer renombre** (en el caso real se propuso "Dental Shield / Escudo Dental"). El veredicto
del nombre se anota en el expediente y alimenta la Compuerta 2 de compliance.

## ⚠️ La FICHA VIEJA es una FUENTE CONTAMINADA (regla dura, incidente 2026-07-27)

Cuando el producto YA tiene ficha en la tienda (descripción, infografías, plantilla, prompt del
bot), esa ficha **NO es fuente de verdad de ingredientes ni de specs** — solo la etiqueta o el
fabricante lo son. La ficha vieja tiene la misma autoridad APARENTE que la etiqueta y es de donde
se copia sin darse cuenta: así se heredan claims que nadie verificó nunca.

- Todo dato que venga de la ficha existente entra al expediente como `claims.no_verificables`
  hasta contrastarlo contra etiqueta/INCI. Si se confirma, sube a `permitidos`; si no, se ELIMINA
  de la ficha (descripción + imágenes + plantilla + bot, barrido COMPLETO, no solo el foco).
- Caso real que parió esta regla: el mismo día en que se documentaba el incidente de claims
  inventados en un producto, otro chat re-publicó "glicerina, sin parabenos, sin fragancias
  agresivas, 30 ml" heredados de la descripción vieja — la etiqueta real no decía NADA de eso.
  La compuerta de veracidad lo cazó al crear el expediente. Dejar `_incidente` anotado en el
  PRODUCTO.json para que el próximo no reintroduzca los claims eliminados.

## Paso 3 · Existencia en el ecosistema

- **Dropi**: buscar por nombre exacto **y por alias**. Los alias engañan: un mismo producto puede
  figurar con tres nombres distintos según quién lo cargó. Anotar todos los alias al expediente.
- **Catálogo Shopify**: existe ya como producto. Si existe → la fase de página (Fase 4 de
  `golden360`) irá por la **rama B (mejorar)**; se anota en el expediente.
- **Biblioteca de archivos**: qué material real ya hay en disco (fotos, videos, GIF, packshots).

## Paso 4 · Existencia en el mercado

- Quién más lo vende en el país y a qué precio
- Con qué ángulo lo venden (eso marca el hueco por donde diferenciarse)
- Qué anuncios tiene activos el nicho (Ad Library) y con qué nivel de producción
- Si hay reseñas reales, guardar citas textuales con su URL (insumo de la Fase 1)

## Paso 5 · Compuerta de realidad

**Si el producto no existe, no se consigue o no se puede traer al país, se dice y se para ahí.**
No se inventa el envase, ni los activos, ni un modelado 3D genérico como relleno. Si las fotos
disponibles son malas, el camino es **mejorar la foto real** (fondo, luz, resolución), nunca
sustituir el producto por otro parecido.

## Trampas conocidas

| Trampa | Cómo se ve | Qué hacer |
|---|---|---|
| Etiqueta distinta | dos fotos del "mismo" producto con activos o gramaje diferentes | quedarse con la del envase que se va a vender; despublicar la otra |
| Alias de proveedor | el nombre en Dropi no se parece al de la etiqueta | mapear todos los alias en el expediente |
| Claim de afiliado | un blog llama "péptido" a un activo que la marca nunca describe así | descartar; solo vale la fuente del fabricante |
| Carpeta contaminada | archivos con el prefijo del producto que son de OTRO producto | verificar contenido, no confiar en el nombre |
| Fórmula por país | la versión que importa el negocio puede no ser la de EE.UU. | marcar `[PENDIENTE]` hasta ver el reverso del frasco real |

## Checklist de cierre de la Fase -1

- [ ] Nombre exacto, marca, contenido neto y activos leídos de la etiqueta
- [ ] Compuerta de identidad: producto original rastreado (costo, ml, ingredientes) y fórmula
      local contrastada; ningún claim de ingrediente sin foto macro de la etiqueta que se despacha
- [ ] Nombre evaluado como ítem de compliance (promete cura? → proponer renombre)
- [ ] INCI completo con URL del fabricante
- [ ] Modo de uso y tiempos oficiales
- [ ] Alias de Dropi mapeados (o "no está en Dropi")
- [ ] Existe o no en el catálogo Shopify → decide rama A o B
- [ ] Competidores y precios del país anotados con fuente
- [ ] `PRODUCTO.json` creado con `identidad` y `producto_real`
