# Los dos techos · y por qué hay que respetar los dos

Un campo se puede escribir por API por encima de su tope y todo se ve bien: la API responde
`ok`, el JSON queda válido y el asistente funciona. Los dos techos fallan **en silencio**, en
momentos distintos.

| Techo | Qué es | Cuándo mata | Cuánto |
|---|---|---|---|
| **A · bot field** | el JSON completo del campo, **escapado** | al ejecutarse el flujo | 19.000 escapados (práctico) |
| **B · campo nativo** | el formulario del panel | el día que alguien abra ese formulario y guarde | ver tabla |

## Techo A · el escapado

Al ejecutarse, el flujo copia la configuración a un campo intermedio **escapada**. Cada tilde
ocupa **6** caracteres y cada emoji **12**. El campo guarda bien y el JSON es válido, pero el
flujo muere antes de disparar y el asistente **deja de responder sin un solo error visible**
(solo aparece en Panel → Registros de errores).

Medido en vivo, dos veces:

| crudo | escapado | dispara |
|---|---|---|
| 15.329 | 18.229 | sí |
| 16.882 | 19.895 | sí |
| 19.922 | 23.266 | **NO** |

En crudos el techo práctico queda en **~17.000**, no 20.000. La relación típica es 1,10 a 1,15
según cuántas tildes y emojis tenga.

```python
escapado = len(json.dumps(valor)[1:-1])   # y que quede por debajo de 19.000
```

**Los dos umbrales, y por qué son dos.** 19.000 es la alerta prudente; el último valor que se
vio **disparar** es 19.895 y el primero que se vio **no disparar** es 23.266. Entre 19.895 y
23.266 no hay medición: por eso el auditor declara 🔴 solo por encima de 19.895 y 🟠 entre
19.000 y 19.895. Tratar los dos casos igual es gritar muerte donde hay riesgo, y el dueño deja
de creerle al informe.

Los números no viven en el código: están en **`assets/topes-nativos.json`**, que es de donde
los lee `auditar.py`. Si Chatea cambia de versión, se corrige ese archivo y no hay que tocar
ningún script.

Los emojis decorativos son los que más pesan: 12 escapados cada uno. Compactarlos es la forma
más barata de bajar un campo que está contra el techo.

**Caso real:** el campo de configuración de Comentarios de un cliente estaba en 17.030 crudos =
**21.302 escapados** desde antes de tocarlo — llevaba tiempo muerto y nadie lo sabía.

## Techo B · el tope nativo de cada campo del formulario

Extraídos del **código de la propia aplicación**
(`https://instalacion-asistentes.chateapro.app/assets/*.js`), no de la documentación.

### Comentarios

| Campo del JSON | Tope |
|---|---|
| `comentarios_negativos.prompt_general` | 10.000 |
| `venta_conversacional.prompt` | 8.000 |
| `respuesta_publica.prompt` | 3.000 |
| `comentarios_negativos.ej_a_eliminar` · `ej_a_no_eliminar` | 1.000 c/u |
| `informacion_del_negocio.info_extra` | 500 |
| `informacion_del_negocio.contacto` · `t_envio` · `venta_conversacional.datos_req` | 200 c/u |
| descripción del producto (`desc`) | 500 |

### Ventas WhatsApp

| Campo del JSON | Tope |
|---|---|
| `prompt.prompt_libre` | 12.000 |
| `producto_segundos.prompt_datos` | 4.000 |
| `comportamiento_ia.rol` · `restricciones` · `analizar_palabra.prompt` | 2.000 c/u |
| `embudo_de_ventas.mensaje_inicial` · `pregunta_de_entrada` | 1.000 c/u |
| `remarketing.prompt_1` · `prompt_2` | 1.000 c/u |
| `notificaciones.notificacion_N.mensaje` | 400 |
| `informacion_de_producto` · descripción | 500 |
| token de proveedor en Dropi | 1.200 |
| upsell · mensaje inicial · descripción | 200 c/u |

### Logístico

**Sin tope de caracteres en los campos de texto.** Los únicos `maxLength` del chunk son 2, 3 y
10, y son campos numéricos de días y horas. Aquí manda únicamente el techo A.

### Carritos

Sin `maxLength` propio. Solo los campos de correo validan longitud.

## Cómo se verifica

```python
assert len(texto) <= TOPE_NATIVO                        # techo B
assert len(json.dumps(valor_completo)[1:-1]) <= 19000   # techo A
```

## Si la versión de Chatea cambia

Los topes se vuelven a extraer del código, no de la memoria: el panel embebe la app en un iframe
de otro origen (no se puede leer por JS ni por accesibilidad), pero **los chunks son estáticos y
públicos**. Los nombres salen del `index-*.js` y los topes están ahí, como `maxCharacters:` en
Comentarios y escritos en el JSX (`" / 2000 caracteres"`) en Ventas WP.
