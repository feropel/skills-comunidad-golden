# Changelog · golden-despachos

Orden cronológico, lo más nuevo arriba.

## GD1.8 — 2026-09-20
Auditoría con `golden-skill-auditor`.

- **La description no decía a dónde derivar las novedades ya trabadas.** El cuerpo (sección
  "Fronteras y desambiguación") sí tenía la frontera completa con `golden-logistica`, pero el
  disparador — el único mecanismo que compite entre skills hermanas antes de que el modelo lea el
  cuerpo — no la mencionaba. Se agregó "Novedades ya despachadas: golden-logistica." al final de la
  description (944 → 988 de 1024 caracteres, sigue con margen). Ningún disparador existente se quitó
  ni se movió.
- **Resto de la auditoría en verde, sin hallazgos nuevos**: `inventario.sh` (0 rotas, 0 huérfanos,
  sintaxis OK en los 5 `.py`, sin secretos, sin signos de apertura), `validar_arsenal.py` (exit 0,
  compuerta pasada), y las tres autopruebas de `scripts/` (`direcciones.py` 27/27,
  `duplicados.py` 7/7, `efectividad.py` 6/6) corridas de nuevo y en verde.
- **Conexión con el ecosistema**: cambios relevantes de esta skill se reportan a
  🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR (Estándar 9).

## GD1.7 — 2026-09-06
Auditoría con `golden-skill-auditor`, EJECUTANDO los cinco scripts (no solo leyéndolos) contra
datos reales y contra carpetas vacías a propósito.

- **Cuatro rutas sin guardia terminaban en traceback crudo**, la misma clase de defecto en dos
  archivos: `scripts/calificar.py` moría si faltaba `datos/FLETES-CALI.json` (las otras tres
  fuentes de ese mismo script — COSTO-RETORNO, TRANSPORTADORAS-OPERATIVAS, RECHAZOS-FULFILLMENT —
  ya tenían `try/except` con aviso; esta se quedó sin él). `scripts/decidir_vivo.py` tenía tres
  huecos: `datos/COTIZACIONES-VIVO.json`, `datos/RECHAZOS-FULFILLMENT.json` (que en `calificar.py`
  SÍ estaba guardado — la duplicación de ese bloque entre los dos scripts los había
  desincronizado) y `salidas/salida-v3.json`.
- **Causa de fondo**: el bloque de carga de RECHAZOS-FULFILLMENT/COSTO-RETORNO/TRANSPORTADORAS
  vive copiado entero en `calificar.py` y en `decidir_vivo.py`. Un arreglo hecho en una copia no
  llega a la otra — la misma lección que ya dictó `EFECTIVIDAD-PLATAFORMA.json` en GD1.5, aplicada
  esta vez al manejo de errores en vez de al dato.
- **Arreglo**: los cuatro puntos ahora terminan con `sys.exit` (o aviso + lista vacía, igual que
  su gemelo en `calificar.py`) con el nombre exacto de lo que falta — nunca un traceback.
- **Verificado, no solo leído**: se reprodujeron los cuatro tracebacks con `DROPI_DATA` apuntando
  a una carpeta vacía, se aplicó el arreglo, y se repitió la misma corrida confirmando el mensaje
  claro en vez del traceback. Regresión contra los datos reales de Golden: `duplicados.py` sobre
  las 895 órdenes reales sigue en `0 alertas` (mismo universo que GD1.6), `direcciones.py` sobre
  esas mismas 895 direcciones repite el reparto exacto de GD1.6 (OK 626, INCOMPLETA 112,
  BLOQUEO 6, REVISAR 32, RURAL 6, OFICINA 113), y las tres autopruebas (`direcciones.py`,
  `duplicados.py`, `efectividad.py`) siguen en verde sin cambios.
- **No verificado en esta ronda** (mismo hueco que GD1.6, sigue abierto): `calificar.py` de punta
  a punta con los dos exports reales — sigue sin estar en disco el de *órdenes con productos*.
- **Conexión con el ecosistema**: cambios relevantes de esta skill se reportan a
  🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR (Estándar 9).

## GD1.6 — 2026-09-05
Aplicación de la ley que acababa de dictar el Centro de Mando: **un detector de patrones acusa el
lenguaje, no el defecto, así que se prueba en los DOS sentidos.** El único detector de la skill sin
banco era el de direcciones, y estaba mal justo en el sentido que nadie había probado: el de los
casos buenos.

- **Las direcciones salen a su propia puerta, `scripts/direcciones.py`**, con 27 casos de autoprueba
  (14 que deben morder, 13 que no). `calificar.py` ya no lleva su propia copia de `analiza_dir`.
- **Medido sobre las 895 direcciones reales del export: 12 mal clasificadas (1,3%)**, en tres clases:
  la palabra «oficina» bloqueaba la oficina PROPIA del cliente (`Calle 17 # 2E-30 … oficina EMNFC
  SAS` salía `BLOQUEO`); las nomenclaturas de **dos letras** (`# 100 AB - 03`, `# 65 GG - 22`,
  `# 66 BB - 51`, `# 23AN-45`) salían `INCOMPLETA` porque el patrón admitía una sola letra; y a las
  veredas se les pedía un número de puerta que allí no existe.
- **Nuevo estado `RURAL`**: cambia la pregunta al cliente, que pasa de «cuál es el número» a «por
  dónde se llega». Reparto antes → después: OK 620→626, INCOMPLETA 120→112, BLOQUEO 8→6,
  REVISAR 34→32, RURAL 0→6. La aritmética cierra exactamente sobre las 12 medidas.
- **Las tres correcciones se vieron MORDER bajo sabotaje**: volver a una sola letra tumba 4 casos,
  quitar la excepción de la oficina propia tumba 1, meter «finca» como marca rural tumba 1.
- **Un caso del propio banco resultó DECORATIVO.** El sabotaje de «finca» no movía nada: la
  dirección elegida traía puerta completa, así que la rama rural nunca se ejecutaba y el comentario
  prometía una guardia que el banco no verificaba. Se reemplazó por uno que sí alcanza esa rama. De
  ahí sale la mitad nueva de la trampa 14: al escribir un caso hay que comprobar que **llegue a la
  rama** que dice proteger.
- Ojo con el atajo fácil: **«finca» no es marca de zona rural**, hay edificios urbanos que se llaman
  así. Las marcas son vereda, corregimiento, parcelación y kilómetro.

**No verificado en esta ronda:** `calificar.py` no se pudo correr de punta a punta porque el export
de *órdenes con productos* no está en disco (solo el de órdenes). Se comprobó que el script carga el
cerebro y resuelve el nuevo import sin error, y se detiene justo en el archivo que falta.
`decidir_vivo.py` sigue sin analizar direcciones: no las mira, ni antes ni ahora.

## GD1.5 — 2026-09-05
Ronda de autocalificación y automejora (mandato del Centro de Mando). Partía de **880/1000**, y el
hallazgo crítico era que la skill corría impecable y **respondía mal**.

- **La efectividad entra por UNA sola puerta: `scripts/efectividad.py`.** Antes `calificar.py` y
  `decidir_vivo.py` leían cada uno `EFECTIVIDAD-PLATAFORMA.json`, un archivo **sin `_fuente` ni
  fecha** que traía Envía al 95,51% cuando la Torre madura da 81,09% sobre 1.337.159 envíos. No era
  cosmético: corriendo los mismos pedidos con una fuente y con la otra, **la recomendación número
  uno cambia de transportadora** (Cajamarca pasaba de Coordinadora $20.891 a Interrapidísimo
  $21.825) y aparecen cambios que antes no salían. Medido antes y después contra el cerebro real.
- **Cascada municipio → departamento → nacional, SIN umbral de muestra** (orden de FER 2026-08-16:
  si hay un envío, ese es el dato). El informe imprime ahora `mun/n=8340`, `dep/n=59894`: de dónde
  salió el número y con cuánta muestra detrás. La transparencia sustituye al umbral.
- **Guardia de procedencia.** Un archivo de efectividad sin `_fuente` ni `_nota` se descarta con
  aviso en vez de entrar callado. Esa es la causa raíz de que el dato inflado viviera semanas dentro
  del cálculo: el número no traía de dónde salía.
- **Bug propio cazado por la autoprueba:** `__NACIONAL__` empieza por guion bajo igual que las claves
  de metadatos, y el filtro por prefijo dejaba **la caída a nacional muerta en silencio** — un
  departamento desconocido devolvía None y la transportadora quedaba fuera de las candidatas.
- **Duplicados distingue FANTASMA de duplicado.** Editar una orden le cambia el ID; la vieja
  desaparece del panel pero sigue en el export ya descargado, y la misma venta aparecía como dos
  pedidos. Marcarla como duplicado manda a preguntarle al cliente por un pedido que no hizo. Nuevo
  nivel `EDICION` con el discriminador autoritativo escrito al lado: el DETALLE
  (`GET /integrations/orders/myorders/{id}`) responde "Orden no encontrada" sobre la vieja, mientras
  que una real, incluso CANCELADA, responde `isSuccess:true`.
- **Cuatro estados terminales por igualdad exacta**: ENTREGADO, DEVOLUCIÓN, CANCELADO, RECHAZADO.
  `ENTREGADO A TRANSPORTADORA` no es venta, es entrega al courier — por eso nunca se compara por
  substring. Terminal no es ignorable: una orden entregada es justo la evidencia de la recompra.
- **Un cero se prueba, no se cree.** `duplicados.py` ya no imprime "sin duplicados" pelado: reporta
  el universo ("0 alertas sobre 895 órdenes, 5 de ellas pendientes") y apunta a su banco.
- **Dos bancos de autoprueba, y los dos se vieron MORDER.** `efectividad.py --autoprueba` (6 casos:
  guardia, cascada completa, sin umbral) y `duplicados.py --autoprueba` (7 casos: fantasma,
  duplicado real, recompra tras entrega, y los cuatro falsos positivos que NO deben saltar).
  Apagando el detector de fantasmas el banco pasa a FALLA con exit 1: no es decoración.
- **Costo de retorno por NEGOCIO.** Se prefiere `COSTO-RETORNO-<NEGOCIO>.json` con `DROPI_NEGOCIO`;
  sin la variable cae al genérico y **lo declara en el informe**. La ley de no-heredar aplica también
  a los parámetros: el mix de ciudades de una empresa no es el de otra. Probadas las dos ramas.
- Variable muerta `orig` fuera de `calificar.py`; changelog en orden cronológico con GD1.4 incluida.

**Sigue abierto, y solo lo cierra un hecho externo:** la Torre está rescatada del `localStorage` del
2026-08-03, y esa cosecha **incluye el mes frontera inmaduro** y cubre municipio en 20 de 33
departamentos (corte alfabético en MAGDALENA, sin VALLE, que es donde está la bodega). Bajarla con
la ventana madura por API es el paso que falta.

## GD1.4 — 2026-09-03
Estándar 9 del Centro de Mando: los cambios relevantes de esta skill se reportan a
🧠 GOLDEN - CENTRO DE MANDO - NO BORRAR. En la misma pasada, el Centro de Mando puso la
`description` dentro del tope duro de la especificación (944 de 1024 caracteres) y bajó las
fronteras al cuerpo, porque lo que se pasa del tope se trunca y los disparadores del final son los
primeros en perderse.

## GD1.3 — 2026-08-21
Auditoría con `golden-skill-auditor`.

- **`decidir_vivo.py` no tenía rama para prepago.** Calificaba TODOS los pedidos con la fórmula de
  valor esperado de contra entrega, que resta probabilidad de devolución y costo de retorno. Un
  pedido prepago nunca paga eso. Efecto real: la recomendación podía irse a una transportadora más
  cara persiguiendo un valor esperado que no aplicaba, y la columna GANA mostraba ese valor esperado
  en vez del ahorro de flete cierto.
- **Filtro explícito de `HABILITADAS`** también en `decidir_vivo.py`; antes solo vivía en
  `calificar.py` y confiaba en que otros archivos excluyeran de facto a las no habilitadas.
- Bucle muerto `for c in x['cands']: pass` eliminado.
- `CHANGELOG.md` se movió a `references/changelog.md`: vivía suelto en la raíz, que es material que
  se publicaría tal cual al marketplace.
- Verificado con fixtures sintéticos: antes del arreglo el prepago se decidía igual que el contra
  entrega; después, manda el precio y el GANA es el ahorro de flete real.

## GD1.2 — 2026-08-03
Auditoría con `golden-skill-auditor` (retomada tras una interrupción).

- **Los scripts aplican por fin la regla insignia de GD1.1**: filtran candidatas por
  `TRANSPORTADORAS-OPERATIVAS.json`. Se descubrió EJECUTANDO: la corrida de prueba reprodujo el
  total de $108.620 que GD1.1 había declarado equivocado, porque el filtro solo existía en prosa.
- **El retorno ya no está horneado**: se lee de `COSTO-RETORNO.json` filtrando por confianza
  alta o media (trampa 5). El hardcode anterior traía Coordinadora y Veloces en 0,0.
- **Scripts portables**: cero rutas personales. Exports por argumento, variable de entorno o el más
  reciente del Escritorio; el cerebro por `DROPI_DATA` con mensaje claro si falta.
- **Pipeline documentado**: formato del `.psv` de huellas y esquema de `COTIZACIONES-VIVO.json`.
- `DUPLICADOS.json` cae en `DROPI-LOGISTICA/salidas/`, no donde se corrió.
- Frontera con `golden-chatea-pro-validacion-direcciones` declarada también en el description.

## GD1.1 — 2026-08-01
Corrección mayor, disparada por el segundo rechazo de la bodega (Fusagasugá).

- **`TRANSPORTADORAS-OPERATIVAS.json` se antepone a todo el cálculo.** Dropi cotiza 10 empresas; la
  bodega solo había generado guías con 4. Recomendar las otras era recomendar rechazos.
- El **protocolo de rechazo** mira el patrón acumulado: si una transportadora junta rechazos, contar
  sus guías antes de concluir que fue mala suerte.
- Nueva trampa 13.

**Efecto sobre la corrida real:** las recomendaciones bajan de 7 a 3, y el valor esperado de
$108.620 a $39.338. Menos plata en el papel, pero ejecutable de verdad.

## GD1.0 — 2026-08-01
Creación de la skill, destilada de una corrida real sobre 34 pedidos.

- **Seis criterios en orden**, con los tres bloqueantes primero: duplicado → dirección → veto de
  bodega → huella → precio → efectividad.
- **Regla de huella por transportadora**: pesa desde el primer envío con corrección bayesiana
  (peso 10 para el historial global, 3 para el de esa transportadora). Funciona en los dos sentidos.
- **Regla de prepago**: manda el precio, con piso de 3 puntos y excepción de $1.500.
- **Costo de retorno medido por empresa**, no supuesto, y con nivel de confianza explícito.
- **Detección de duplicados** cruzando por teléfono y por nombre más dirección.
- **Protocolo de rechazo de bodega**: contrastar contra Torre Logística y cotización antes de
  dictaminar si es puntual o general.
- **Teléfono obligatorio junto al ID** en todo informe.
- **Retiro en oficina bloquea la transportadora.**
- Datos separados en `PROYECTOS/DROPI-LOGISTICA/` con git, para que sobrevivan al chat.
- `references/trampas.md` nace con 12 entradas, todas de errores realmente cometidos.

**Autocalificación de la corrida fundacional: 92/100.** Restan 8 por un pedido cuya huella el panel
se negó a abrir y por dos recomendaciones publicadas antes de revisar la dirección de retiro en
oficina, ya corregidas y horneadas como trampa 3.
