# Estándar de contenido · qué debe tener un producto sano

Contra esto se lee cada prompt, entero. La fuente de cómo se ESCRIBE un prompt de venta es la
skill `golden-chatea-pro-prompt-ventas`; aquí está lo que se AUDITA.

## Esqueleto de un producto en `[Producto Ventas Wp] N`

```
informacion_de_producto   id · nombre · precio · moneda · id_dropi · tipo · variable ·
                          imagen · estado · dta_prompt
embudo_de_ventas          mensaje_inicial · multimedia (LISTA) · pregunta_de_entrada
prompt                    tipo_de_prompt · prompt_libre  (o los cinco prompt_guiado_*)
voz_con_ia                proveedor · id · api_key · habilitar · reglas
recordatorios             activar_1/2 · tiempo_1/2 · mensaje_1/2 · activar_rango · hora_min/max
remarketing               activar_1/2 · prompt_1/2 · tiempo_1/2 · plantilla_1/2 · hora_min/max
activadores_del_flujo     palabras_clave · ids_de_anuncio
meta_conversion           habilitado · por_defecto · id · aud_id
upsells                   N → activo · imagen · titulo · descripcion · boton · momento ·
                          nombre · precio · id_dropi · variaciones
```

Una llave que falte no es cosmética: el panel puede dejar de interpretar el objeto. El producto
de **Comentarios** es un objeto de **5 llaves exactas** — `img`, `name`, `desc`, `rela`,
`estado`. Con 4 llaves el panel no lo interpreta.

## Lo que se revisa en el contenido

### Identidad y voz
- La asesora tiene nombre y es el mismo en todo el espacio.
- La empresa se nombra como empresa, nunca como "tienda".
- El tono corresponde al país del espacio.

### Oferta
- El precio del prompt coincide con `informacion_de_producto.precio`, con la tienda y con el
  creativo que trae al cliente. Un precio distinto en tres sitios es una discusión con el
  cliente en el chat.
- La moneda corresponde al país.
- El modelo de pago está declarado y es el correcto: catálogo = contra entrega, marca =
  anticipado. Un prompt que ofrece contra entrega en un producto de pago anticipado rompe la
  venta y al revés.
- Los combos y la escalera de precios cuadran aritméticamente.

### Claims
- **Lo que la caja dice no se inventa, y lo que la caja no dice no se afirma.** Los claims del
  empaque se citan; los demás no existen.
- Nada de promesas médicas ni garantías de resultado que el producto no respalde.
- Si el producto es unisex, se afirma sin nombrar género.

### Ortografía y forma
- Acentos correctos **en el render**, no en el archivo.
- **Sin signos de apertura** `¿` `¡`.
- Sin rayas separadoras.
- Emojis coherentes con el copy, y contados: cada uno pesa 12 escapados contra el techo.

### Embudo
- `mensaje_inicial` presenta empresa y asesora, y no repite lo que ya dijo el anuncio.
- `pregunta_de_entrada` es una sola pregunta, y sirve para segmentar.
- `multimedia` es **lista**, con URLs vivas, y el primer archivo es del producto.
- Un video sin poster parece una imagen rota.

### Recordatorios y remarketing
- Los interruptores encendidos si hay contenido.
- El rango horario es humano (no escribirle a alguien a las 3 de la mañana).
- Los mensajes no repiten el mismo gancho.
- Una plantilla de WhatsApp **con malas métricas reincide**: si está marcada, se cambia.

### Upsells
- `id_dropi` de cada upsell existe.
- El precio del upsell cuadra con el descuento que promete.
- `momento` es coherente con lo que vende.

## Fugas que se buscan siempre

| Fuga | Por qué importa |
|---|---|
| Nombre de otra tienda o de otra asesora | quedó de la cuenta de origen |
| Transportadoras de otro país | la IA las imita como ejemplo |
| WhatsApp o dominio de otro | el cliente termina escribiéndole a otro |
| `voz_con_ia.api_key` heredada | es la credencial de ElevenLabs del origen |
| Un producto concreto horneado en un campo "genérico" | actúa de fallback para todos los demás |
| Placeholders (`{{`, `TU_`, `XXX`, `[NOMBRE`) | se publicó sin terminar |

## Por país

La plataforma solo acepta **7**: COLOMBIA, ECUADOR, CHILE, MEXICO, PANAMA, PERU, PARAGUAY, en
mayúscula y sin acentos.

| | México | Colombia |
|---|---|---|
| División | Estado · municipio o alcaldía · colonia | departamento · ciudad · barrio |
| Código postal | **REQUERIDO** | no se exige |
| Recolección en oficina | **NO EXISTE** | sí |
| Regulador | PROFECO | SIC |
| Palabras | paquetería · pedido · dinero · repartidor | transportadora · domicilio · plata · mensajero |

**Trampa medida:** una plantilla de México decía "NUNCA exijas código postal", que era criterio
de Colombia copiado. **Cualquier país clonado de otra plantilla hereda el criterio equivocado**:
se revisa uno por uno, no se asume. Y "domicilio" en Colombia es el pedido, en México es la casa.

## Valores por defecto que NO son defectos

No se "arreglan" — comprobados idénticos en un espacio que vende a diario:

- `[WhatsApp IA] Instrucciones recolección de datos` vacío.
- `[Ventas Wp] Disparador de productos` (el `array`) vacío, con los datos en el Extendido.
- `voice_id: "English_MaturePartner"`, con el activador apagado y sin API key.
- Eventos de `[Meta]` en cero.

**El método ante la duda: comparar contra un workspace que funcione, no contra lo que uno supone
que debería haber.**
