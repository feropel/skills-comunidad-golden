# Plan de testeo de la tanda de estáticos

Se lee en el paso 6. Esta skill **propone** el plan; lo monta `golden-ads`, siempre en pausa, y la
decisión de apagar o escalar la toma con sus propias reglas. Aquí no se fijan umbrales propios porque
la casa no tiene ninguno medido para estáticos con contraentrega.

## Estructura

1. **Máximo 3 piezas por conjunto.** Medido en la casa sobre 307 anuncios en 13 cuentas. Alejo lanza
   10 o más por conjunto (M13, 01:27:30); queda registrado como dato contrario hasta que la primera
   tanda real lo resuelva.
2. **Presupuesto parejo entre ángulos** (documento de Kevin). Las piezas del hueco de la matriz de
   referencias van primero.
3. **Se mide por conjunto, no por anuncio suelto.** Alejo: si apagas los que "no compran", *"usted deja
   de vender"* (01:24:30). FER: *"tienen que ir al conjunto… y si son rentables, no apaguen nada"*
   (01:24:59).
4. **TOFU va a prospección. MOFU y BOFU necesitan públicos de retargeting y píxel con API de
   conversiones.** Si la cuenta no los tiene, esas columnas salen `[PENDIENTE: requiere públicos]`. En
   cuenta nueva el TOFU es el más arriesgado en alcance; si Meta lo limita, el MOFU es el que mejor
   explica el producto (cierre del documento de Kevin).
5. **Imagen y video en campañas separadas**: combinados, Meta le da la entrega al video (Alejo,
   01:50:06).
6. **Nombre del anuncio**: `ANGULO-ETAPA-FORMATO-v<n>` (ej. `MALARACHA-TOFU-SIMBOLO-v1`), para leer
   el ganador en el reporte sin abrir el creativo.

## Presupuesto de prueba (dato de mentores, no medido en Golden)

| Quién | Cuánto |
|---|---|
| Alejo (M13, 01:51:04) | De $50.000 a $60.000 COP por campaña, "por lo menos 20 dólares" |
| FER (M13, 01:51:16) | $20.000 COP durante 3 a 5 días, con la campaña duplicada 3 veces |

Los montos van en pesos ×1 y `golden-ads` los relee del servidor después de montarlos.

## Qué se mira (referencias, no umbrales de la casa)

**Hoja "Banco de Creativos" de Kevin** (en pantalla, taller 01-oct, 02:21:00; él no la explicó):

| Métrica | Guatemala | Colombia | Lectura de Kevin |
|---|---|---|---|
| CPM | Q12 a Q27 | $5.000 a $10.000 COP | Si se pasa, revisar audiencia o creativo |
| CTR saliente | 2,5% a 5% | 2% a 4,5% | 2% es el mínimo; por debajo de 1,5%, cambiar los ganchos |
| Costo por conversación | Q1,50 a Q5 | $1.200 a $1.800 COP | Por encima de Q8 o $5.000 COP, la oferta y el anuncio no cuadran |
| Tasa de conexión clic → mensaje | (fila incoherente: dice 30-15%) | igual | Pide 7 u 8 de cada 10 clics; menos de 50% es fuga en el enlace. No usar sin aclararla |

Alejo: un buen anuncio tiene CTR de 2 a 5% (M13, 00:44:33). En campañas a WhatsApp se mira el costo
por conversación iniciada; una conversación muy barata puede ser curiosidad (00:47:14).

**Diagnóstico** (M13, 00:42:29):
- CTR alto y pocas ventas: el gancho funciona; fallan la promesa, la oferta, la página o el tráfico.
- CTR bajo: revisar gancho, ángulo, formato, claridad visual y encaje mensaje-público.

**Veredicto:** el que fije `golden-ads` con su matriz MUERTO / SEÑAL / SEMI-GANADOR / GANADOR. Regla
interna de Golden que se suma (no vive en `golden-ads`): se escala cuando el CPA es menor al 18% del
ticket. Ranking por compras entregadas y utilidad después de la entrega, nunca por CTR.

## Lo que vuelve para el módulo 1

Del ángulo ganador: la ficha, el nivel, y 4 métricas reales: **días activo, CTR, CPA y ventas**
(documento de Kevin). Con eso se corre el traspaso de `traspaso-modulos-1-4-2.md`.

## Hueco abierto

Días y presupuesto **por estático** y un umbral propio de ganador para estáticos con contraentrega. Se
miden en la primera tanda real y se anotan aquí con fecha y cuenta.
