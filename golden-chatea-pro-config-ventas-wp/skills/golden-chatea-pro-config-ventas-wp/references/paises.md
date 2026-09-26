# Países — parametrización del asistente de ventas WhatsApp

Chatea Pro acepta **10 países** (campo `[Comentarios IA] País`, en mayúscula y sin
acentos): **COLOMBIA · ECUADOR · CHILE · MEXICO · PANAMA · PERU · PARAGUAY · GUATEMALA · ARGENTINA · BRASIL**
(remedido 2026-08-29 contra el bundle vivo: se sumaron los 3 últimos). No existe Bolivia ni Costa Rica.

🔴 **Esa lista dice DÓNDE YA NO HAY QUE INVESTIGAR, no a quién se puede configurar.** Hasta la
v4.7 la frase de aquí decía *"`build_config.py` rechaza cualquier otro"*, y era cierta: la puerta
estaba viva en el código. Se retiró el 2026-09-06 por mandato de FER — *"el país se pide para
saber cómo enfocarlo, no para prohibir"*. Hoy un país fuera de la lista **se configura igual**:
el script avisa, pide `--moneda` (que se **investiga**, no se pregunta) y sigue. Guardarraíl:
`scripts/verificar_pais_no_es_puerta.sh`.

En el JSON de ventas-wp, `conexion_con_dropi.pais` va en **minúscula** (ej: `colombia`), pero
debe ser uno de esos 10.

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

**Ecuador, Chile, Panamá, Perú, Paraguay, Guatemala, Argentina, Brasil y 15 países más:** usan
su propia división administrativa y vocabulario, derivado de su pack en
`golden-chatea-pro-validacion-direcciones` — ver "Vocabulario de dirección" más abajo, que es la
sección viva (23 países). Brasil no es hispanohablante: los textos del producto van en portugués.

🔴 **Hueco CERRADO el 2026-09-20 (v4.13):** hasta esa fecha esta sección decía que Argentina y
Brasil no tenían pack y había que preguntarle al negocio su división geográfica. Ya no es así: el
mapa de vocabulario se extendió a los 23 países de la hermana, Argentina y Brasil incluidos. Se
deja el rastro aquí a propósito — es la clase exacta de "dato que caduca solo" que esta skill
existe para no repetir: una sección se actualiza y otra, veinte líneas más abajo en el mismo
archivo, se queda diciendo lo viejo (medido por golden-skill-auditor, 2026-09-22).

Al parametrizar cualquier país nuevo, NO copies el criterio de Colombia: revísalo uno por uno.

## Trampas verificadas

- **"Domicilio" cambia de significado.** En Colombia el domicilio es el PEDIDO; en México es la
  CASA. Un mensaje que diga "para recibir tu domicilio" no se entiende en México. En los textos
  del producto, usar el vocabulario del país.
- **Código postal en México.** La plantilla `03-MEXICO-v100.md` decía "NUNCA exijas código
  postal" — era criterio de Colombia copiado. En México el CP es obligatorio. Cualquier país
  clonado de otra plantilla hereda el criterio equivocado: revisar, no asumir.
- El país NO cambia la ESTRUCTURA del JSON de ventas-wp (las claves son las mismas); cambia el
  valor de `pais`, la `moneda`, los tiempos de entrega y el vocabulario de los textos.

## Vocabulario de dirección: se DERIVA del país, nunca se escribe a mano

`build_config.py` toma de `assets/limites.json → vocabulario_direccion_por_pais[PAIS]` cuatro cosas y las
inyecta en los huecos de los assets: `campos_memoria` → `{{CAMPOS_DIRECCION}}` (rol, PRIORIDAD 3),
`aclaracion` → `{{ACLARACION_DIRECCION}}` (restricciones) y `aclaracion_corta` → `{{ACLARACION_CORTA}}`
(prompt_datos). **Hoy el mapa tiene 23 países**, uno por pack de `golden-chatea-pro-validacion-direcciones`
(Colombia y México escritos a mano y anclados al pack; los otros 21 derivados por
`scripts/generar_vocabulario.py`, que copia del pack sin interpretar: `campos_memoria` sale de la línea
"Bien estructurada: a + b + c" y `aclaracion` de la línea "… no es dirección: pide …"). Cada entrada guarda
`fuente` y la cita literal. Tres países no tienen línea limpia en su pack (Chile, Guatemala, Panamá): van
marcados `origen: parafraseado del pack`, con la cita que los respalda. **Un país SIN pack NO bloquea y NO
hereda a Colombia:** cae a un genérico neutro ("ciudad, división administrativa, dirección, barrio o
colonia") y el script lo declara.

El mapa no dice más que su pack: Argentina sin provincia, Chile sin código postal y Costa Rica con referencia,
metros y rumbo son lo que esos packs piden. Ecuador toma la variante Sierra/general (la de Guayaquil/Costa
queda en el pack). Brasil conserva los términos del pack en portugués.

Para AÑADIR un país: primero su pack en `golden-chatea-pro-validacion-direcciones/references/<pais>.md`
(esa es la fuente; no se inventa); luego `python3 scripts/generar_vocabulario.py` (muestra) y `--escribir`;
luego `python3 scripts/autoprueba_vocabulario.py`. Con `PYTHONDONTWRITEBYTECODE=1` en ambos.
🔴 **`aclaracion_corta` no puede pasar de ~19 caracteres más que la colombiana:** `prompt_datos` vive a
~15 caracteres de su tope nativo de 4.000 y `build_config.py` se niega a escribir si se pasa (probado).
Lo largo, como "el código postal es obligatorio", va en `aclaracion`, que tiene holgura.
