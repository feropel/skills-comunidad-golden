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
    "alergenos": [], "alergenos_verificados": false, "fuente_etiqueta": "",
    "registro_sanitario": "", "foto_etiqueta": ""
  },
  "claims": { "permitidos": [], "prohibidos": [], "no_verificables": [] },
  "mercado_dropkiller": {
    "fecha_medicion": "", "pais": "", "terminos_buscados": [],
    "conteo_cerrado": false, "unidades_depuradas": null, "unidades_reportadas": null,
    "fichas_unicas": null, "proveedores_activos": null, "etapa": "",
    "confianza_ventas": "", "fuente": "plataformas de dropshipping (no es el mercado total)"
  },
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
  "mercado_en_vivo": {
    "medido_el": "",
    "paises": [
      { "pais": "", "vendedores": [], "precio_local": null, "moneda": "", "precio_usd": null,
        "oferta": "", "modelo_pago": "", "anuncios_activos": null, "conteo_cerrado": false,
        "antiguedad_max_dias": null, "fuente": "" }
    ],
    "ofertas_competencia": [
      { "competidor": "", "url": "", "p1": null, "p2": null, "p3": null, "regalo": "",
        "envio": "", "garantia": "", "ancla": null, "urgencia": "", "pago": "" }
    ],
    "autopsia_paginas": [
      { "competidor": "", "url": "", "orden_secciones": [], "prueba_social": "",
        "campos_formulario": null, "plataforma": "", "apps_detectadas": [] }
    ],
    "creativos": [
      { "competidor": "", "id": "", "red": "", "formato": "", "dias_activo": null,
        "gancho_3s": "", "que_muestra": "", "texto_en_pantalla": "", "url_pieza": "" }
    ],
    "huecos": [
      { "tipo": "", "descripcion": "", "evidencia_de_que_esta_vacio": "", "por_que_podria_estarlo": "" }
    ]
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
| `mercado_en_vivo` | **Fase 3** de esta skill | oferta y precio, ángulos de ads, estructura de la página, briefs de creativos |
| `seo` | Fase 3 | página, schema, colección |
| `estado` | cada fase al cerrar | candado maestro |

## Reglas del expediente

0.bis **`mercado_dropkiller` solo acepta cifras DEPURADAS y con su marca de cierre.**
   `unidades_depuradas` sale de `ventas_reales.py`, nunca de `totalSoldUnits` crudo (cuenta ajustes
   de inventario). `conteo_cerrado: false` significa que la búsqueda tocó un tope o quedaron
   términos sin correr: esa cifra se escribe `N+` en el documento y **no se compara con otra**.
   `etapa` y `proveedores_activos` caducan en semanas: sin `fecha_medicion` el bloque no vale.
0. **`alergenos` se llena de la ETIQUETA o queda `alergenos_verificados: false`.** Lista vacía con
   `verificados: false` significa "no comprobado", NO "no tiene" — y bloquea publicar la ficha.
   `fuente_etiqueta` guarda la ruta de la foto/fotograma del que se leyó (ver
   `scripts/etiqueta_desde_video.py`). La página de un competidor NUNCA es esa fuente.
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

## Regla de coherencia de `mercado_en_vivo` (G5.18)

- **`medido_el` es obligatorio.** Precios, ofertas y saturación se mueven en semanas: un bloque sin
  fecha se trata como `[PENDIENTE]`, no como dato.
- **`anuncios_activos` no se escribe solo.** Va siempre con `conteo_cerrado`. Si es `false`, el número
  se lee como *"al menos N"* y **jamás** como saturación del nicho — de ahí sale una decisión de
  lanzar o matar, y el 40 de la primera versión de la receta de Google era el tope de página, no un
  conteo.
- **Dos filas con `conteo_cerrado: false` NO se comparan entre sí.** Dos `100+` pueden ser 101 y 4.000.
  Ordenar países o competidores por un número abierto es la trampa de conteo un piso más arriba. Para
  comparar: se cierran los dos, o no se compara.
- **Un `hueco` sin `evidencia_de_que_esta_vacio` es una corazonada.** Y sin
  `por_que_podria_estarlo` está a medias: a veces nadie lo hace porque no funciona, y eso también
  es un hallazgo.
- **Los precios de aquí son REFERENCIA de mercado.** `negocio.precio_venta` solo lo fija el dueño
  (REGLA 11); nunca se rellena con lo que se encontró en esta fase.
