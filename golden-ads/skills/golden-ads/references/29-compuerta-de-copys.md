# 29 · COMPUERTA DE COPYS — lo que hace entregable un copy de Meta

Nace de una prueba REAL que FER declaró como prueba de esta skill (Candida Cleanse · CP6 ·
2026-09-05). Se escribieron 60 copys que cumplían el estándar de largos y **FER los rechazó**:
*"colocaste unos copies muy malos, sin emojis, corticos, y así no debe ser"*.

**La causa medida:** se escribió **contra el límite en vez de contra el lector**, y **no se invocó
`golden-copywriting`** — que esta misma skill declara como su hermana. Ni se invocó ni se declaró
que se había ido sin ella. Salió ficha técnica: *"Apoyo digestivo diario"*, *"60 cápsulas por
frasco"*, *"Sin efecto laxante"*. **Eso son etiquetas de empaque, no anuncios.**

---

## 🔴 Las 4 compuertas (si una falla, el copy NO se entrega)

### 1. `golden-copywriting` es PASO OBLIGATORIO, no una sugerencia
No es "el motor que se puede usar": es **por donde pasan los copys**. Si no está instalada, se
escribe igual — pero **se DECLARA en el chat**: *"copys escritos sin el motor de frameworks"*.
**Prohibido no invocarla y no decirlo.** Ese fue exactamente el fallo.

### 2. Emojis OBLIGATORIOS en el texto principal
**Cero emojis = copy NO entregable.** No es decoración: es lo que rompe el bloque de texto y frena
el scroll en un feed. Un texto principal sin un solo emoji se devuelve y se reescribe.

### 3. El HOOK vive en los primeros ~40 caracteres
Es **lo único que se ve antes del "ver más"**. Si el gancho está en la línea 3, no existe. La
primera frase carga el peso: dolor, promesa o curiosidad — nunca el nombre del producto a secas.

### 4. 125/40/25 es un TECHO, no un OBJETIVO
Escribir corto **para cumplir** es el error que produjo los 60 copys rechazados. El largo lo manda
**lo que hay que decir para vender**, no la regla. Si el copy bueno usa 118 de los 125, perfecto;
si usa 40 porque no tenía nada que decir, está mal escrito.

---

## 🔴 El TECHO REAL de opciones por anuncio: **5 + 5 + 1**, no 5×5×5

**MEDIDO por DOM** en el editor standalone, tipo de anuncio **"Crear anuncio y mensaje"**
(2026-09-05): Meta ofrece **"Agregar opción"** en **Texto principal (hasta 5)** y en **Título
(hasta 5)**. En **Descripción ese botón NO EXISTE**. Techo real de carga: **11**, no 15.

⚠️ **NO generalizar a otros objetivos ni a otros tipos de anuncio sin medirlo allí.** Generalizar
sin medir es lo que creó la regla equivocada de los 15. Antes de prometer un número, **mirar la
interfaz de ESE tipo de anuncio**.

**Cómo se resuelve la diferencia entre lo escrito y lo que cabe:**
1. Se **escriben** las variantes buenas (5 textos + 5 títulos + las descripciones que hagan falta).
2. Se **cargan** las que quepan según el techo medido de ese tipo de anuncio.
3. 🔴 **Se DECLARA qué quedó fuera y por qué.** *"Cargué 5 textos, 5 títulos y 1 descripción; las
   otras 4 descripciones quedan aquí por si cambias el tipo de anuncio."* Nunca callar el recorte.

---

## 🔴 INVENTARIAR lo que el anuncio YA tiene, ANTES de escribir

En la prueba, los cuatro anuncios **ya traían un texto y un título puestos por API**. Al agregar
opciones encima, **el viejo se quedó como opción 1** y eso no se declaró hasta el final.

**Antes de tocar un anuncio existente:**
- [ ] Leer qué copys tiene YA (por API o mirando el editor). **"Vacío" se comprueba, no se supone.**
- [ ] Decidir explícitamente: el existente **se conserva** como opción 1, **se reemplaza**, o **se
      borra**. Y decírselo al usuario.
- [ ] Si el techo obliga a elegir, decir **cuál se sacrifica** y por qué.

---

## Y si el bot de WhatsApp tiene DISPARADOR, el copy lo lleva DENTRO
Cuando el destino es Chatea PRO y el flujo arranca con un **disparador literal**, ese texto **tiene
que ir dentro del texto principal del anuncio, byte a byte**. Un copy hermoso sin la cadena del
disparador **no activa el bot**: la conversación entra a atención humana y se pierde la venta.
Se verifica ANTES de dar por bueno el copy. (Ver `reference_disparador_chatea_no_se_automatiza`.)

---

## ✅ Lo que en esa prueba SÍ salió bien (conservar, no perder)
- **Presupuesto COP ×1 releído del servidor**: $1.000.000/día correcto, sin el error de los centavos.
- **Multianunciante OFF** aplicado y verificado en los cuatro anuncios.
- **Los copys se escribieron contra el CREATIVO REAL** — abierto con vista previa — **y no contra el
  nombre del conjunto**. Por eso el de la pieza antes/después habla de transformación, y el de la
  pieza mixta nombra a ellos y ellas. **Eso es doctrina: el copy nace del creativo, no del nombre.**
- **El ingrediente falso también entra por la IMAGEN** (se detectó jengibre en las cuatro piezas de
  un producto que no lo lleva). Revisar la imagen con el mismo rigor que el texto.

Relacionado: `25-cuenta-sin-creativos.md` (analizar el creativo) · `26-intake-montar-campana.md` ·
`reglas-de-oro.md` §15 (formato de entrega) · skill `golden-copywriting`.
