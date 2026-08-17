# Changelog · golden-despachos

## GD1.0 — 2026-08-01
Creación de la skill, destilada de una corrida real sobre 34 pedidos de Golden.

- **Seis criterios en orden**, con los tres bloqueantes primero: duplicado → dirección → veto de
  bodega → huella → precio → efectividad.
- **Regla de huella por transportadora**: pesa desde el primer envío con corrección bayesiana
  (peso 10 para el historial global, 3 para el de esa transportadora). Funciona en los dos
  sentidos: rescata a la barata que ya le funcionó al cliente y descarta a la que le falló.
- **Regla de prepago**: manda el precio, con piso de 3 puntos de efectividad y excepción de $1.500.
  Validada con 9 de 9 prepagos entregados.
- **Costo de retorno medido por empresa**, no supuesto, y con nivel de confianza explícito.
- **Detección de duplicados** en cuatro niveles, cruzando por teléfono y por nombre+dirección.
- **Protocolo de rechazo de bodega**: contrastar contra Torre Logística y cotización antes de
  dictaminar si es puntual o general.
- **Teléfono obligatorio junto al ID** en todo informe: Dropi cambia el ID al editar la orden.
- **Retiro en oficina bloquea la transportadora.**
- Datos separados en `PROYECTOS/DROPI-LOGISTICA/` con git, para que sobrevivan al chat.
- `references/trampas.md` nace con 12 entradas, todas de errores realmente cometidos.

**Autocalificación de la corrida fundacional: 92/100.** Restan 8 por un pedido cuya huella el panel
se negó a abrir y por dos recomendaciones publicadas antes de revisar la
dirección de retiro en oficina, ya corregidas y horneadas como trampa 3.

## GD1.1 — 2026-08-01
Corrección mayor, disparada por el segundo rechazo de Suppli (Fusagasugá).

- **`TRANSPORTADORAS-OPERATIVAS.json` se antepone a todo el cálculo.** Dropi cotiza 10 empresas;
  Suppli solo ha generado guías con 4 (Envía 104, Interrapidísimo 68, Veloces 57, Coordinadora 7).
  Domina, TCC, Jamv-Drive, Derocha, Wiilog y 99minutos: cero. Recomendarlas era recomendar rechazos.
- El **protocolo de rechazo** ahora mira el patrón acumulado: si una transportadora junta rechazos,
  contar sus guías antes de concluir que fue mala suerte.
- Nueva trampa 13.

**Efecto sobre la corrida real:** las recomendaciones bajan de 7 a 3, y el valor esperado de
$108.620 a $39.338. Menos plata en el papel, pero ejecutable de verdad.

## GD1.2 — 2026-08-03
Auditoría con `golden-skill-auditor` (retomada tras una interrupción; los arreglos parciales del
primer intento se verificaron sanos y se conservaron).

- **Los scripts ahora aplican la regla insignia de GD1.1**: `calificar.py` y `decidir_vivo.py`
  filtran candidatas por `TRANSPORTADORAS-OPERATIVAS.json` — NUNCA USADA no compite aunque gane el
  cálculo; MARGINAL se marca con `*` y aviso de confirmar con la bodega. Se descubrió EJECUTANDO:
  la corrida de prueba reprodujo el TOTAL de $108.620 que GD1.1 había declarado equivocado, porque
  el filtro solo existía en prosa, no en código.
- **El retorno ya no está horneado en `calificar.py`**: se lee de `COSTO-RETORNO.json` filtrando
  por confianza alta/media (trampa 5). El hardcode anterior traía Coordinadora y Veloces en 0,0 —
  exactamente el error que la trampa 5 documenta como ya cometido. `decidir_vivo.py` lee igual.
- **Scripts portables**: cero rutas personales. Exports por argumento, variable de entorno o el
  más reciente del Escritorio; el cerebro de datos por `DROPI_DATA` con mensaje claro si falta
  (antes: traceback críptico). Dependencia `openpyxl` declarada en SKILL.md.
- **Pipeline documentado**: formato exacto del `.psv` de huellas y esquema de
  `COTIZACIONES-VIVO.json` en `references/captura-panel.md`; los cuatro scripts ahora tienen
  puntero desde el proceso (antes `decidir_vivo.py` y `huellas-consola.js` eran huérfanos).
- `DUPLICADOS.json` cae en `DROPI-LOGISTICA/salidas/`, no en la carpeta donde se corrió.
- **Frontera declarada también en el description** contra
  `golden-chatea-pro-validacion-direcciones` (hallazgo del mapa neuronal: solo se declaraba la de
  `golden-logistica`).
- Changelog deduplicado (SKILL.md apunta aquí), dato de cliente anonimizado, código muerto fuera
  de `analiza_dir`, versión al patrón de la casa (comentario HTML bajo el H1).
