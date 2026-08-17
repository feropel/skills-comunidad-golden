# El expediente · `PRODUCTO.json`

Fuente única de verdad del producto. Se crea en la **Fase -1**, vive en
`PROYECTOS/<PRODUCTO>/PRODUCTO.json`, y **toda skill lo lee antes de generar y lo escribe al
terminar su fase**.

Por qué existe: antes, cada fase escribía su propio archivo y al final un grep intentaba cazar las
incoherencias (keyword distinta en el orgánico, precios que no cuadran, dos números de WhatsApp).
Eso es curar en vez de prevenir. Con el expediente, **quien se sale del expediente se sale de la
fuente**, y la incoherencia se vuelve visible en el momento, no al final.

## Esquema

```json
{
  "identidad": {
    "nombre_oficial": "", "nombre_comercial": "", "marca": "", "handle": "",
    "alias_dropi": [], "slug_archivos": "", "pais": "", "vertical": "",
    "forma": "", "verbo_uso": ""
  },
  "producto_real": {
    "contenido_neto": "", "activos_frente": [], "inci_completo": [], "fuente_inci": "",
    "modo_uso_oficial": "", "tiempo_resultado": "", "origen": "",
    "registro_sanitario": "", "foto_etiqueta": ""
  },
  "claims": { "permitidos": [], "prohibidos": [], "no_verificables": [] },
  "negocio": {
    "modelo_pago": "", "costo_proveedor": null, "proveedor": "", "stock": null,
    "precio_venta": null, "compare_at": null, "combos": [],
    "flete_comision": null, "tasa_entrega": null, "breakeven_cpa": null
  },
  "activacion": {
    "keyword_bot": "", "whatsapp": "", "cargado_en_bot": false,
    "pixel_id": "", "evento_probado": false
  },
  "assets": {
    "foto_real_hero": "", "imagenes": [], "videos": [], "gifs": [], "antes_despues_real": ""
  },
  "seo": {
    "titulo_seo": "", "meta_descripcion": "", "keywords": [], "coleccion": "", "tags": []
  },
  "estado": { "fase_actual": "", "compuertas_pasadas": [], "pendientes": [] }
}
```

## Quién escribe qué

> Nota post-split: las Fases 3/5/8 y las Compuertas 2–4 de esta tabla son del pipeline de
> **`golden360`** (el orquestador). Esta skill llena `identidad`, `producto_real`, `negocio`
> (los 4 números) y arranca `estado`; el resto lo van llenando las fases de la ruta.

| Bloque del JSON | Lo llena | Lo consume |
|---|---|---|
| `identidad` | Fase -1 y Fase 0 | todas: nombres de archivo, copys, campañas, bot |
| `producto_real` | Fase -1 (etiqueta + fabricante) | Compuerta 2, página, copys, bot |
| `claims` | Compuerta 2 | página, ads, orgánico, bot |
| `negocio` | Fase 0 (los 4 números) + Compuerta 3 | combos, tabla del bot, breakeven, presupuesto |
| `activacion` | Fase 8 y Compuerta 4 | botón de la página, ads, orgánico |
| `assets` | Fase 0.5 (inventario) y Fase 5 | página, ads, orgánico, bot |
| `seo` | Fase 3 | página, schema, colección |
| `estado` | cada fase al cerrar | candado maestro |

## Reglas del expediente

1. **Nada se escribe sin fuente.** Los campos de `producto_real` llevan su URL en `fuente_inci` o el
   archivo de la foto en `foto_etiqueta`.
2. **`claims.permitidos` es la única lista que puede usarse.** Si un copy quiere decir algo que no
   está ahí, o se respalda y se agrega, o no se dice.
3. **`keyword_bot` es UNA sola.** La misma en botón de página, anuncios, orgánico y activador de
   Chatea. Cambiarla es cambiarla en el expediente y volver a propagar, nunca a mano en un archivo.
4. **`whatsapp` es UN solo número** en todas las piezas.
5. **`verbo_uso`** manda en todo el copy: gota se aplica, cápsula se toma, spray se rocía, gadget se usa.
6. **Los `null` son honestos.** Un precio que no confirmó el dueño se queda en `null` y en
   `estado.pendientes`, nunca se rellena con el precio sugerido por el estudio.
7. **`cargado_en_bot: false` bloquea el botón de WhatsApp.** Un botón que dispara a un bot que no
   conoce el producto es un embudo roto.
8. **`compuertas_pasadas`** es el registro de por dónde va: `["viabilidad","veracidad"]`. El candado
   maestro lo lee para saber si el paquete puede entregarse.

## Cómo se usa en la práctica

- Antes de generar cualquier pieza: **leer el expediente**, no la memoria de la conversación.
- Al terminar la fase: **escribir lo nuevo** y actualizar `estado.fase_actual`.
- Al detectar una contradicción entre una pieza y el expediente: **gana el expediente**, y si el
  expediente está mal, se corrige ahí primero y luego se propaga.
