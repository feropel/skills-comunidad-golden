# Producción de creativos + copys (golden-ads SÍ los hace)

`golden-ads` es dueño de la **producción de creativos y copys para pauta**. Usa `golden-copywriting`
como motor de frameworks (AIDA/PAS/4U/BAB) y la generación de medios (Higgsfield/Nano Banana/Seedance
vía `golden-ugc-avatar` + MCP). El copy SIEMPRE nace del **creativo + la investigación**, no al aire.

## PASO 1 — Intake de creativos (SIEMPRE preguntar primero)
> "Tienes **videos y/o imágenes** del producto? Súbelos. Si no tienes, los generamos nosotros."

## Árbol de decisión
### A) El cliente TIENE media → ANALIZAR y escribir copys desde ahí
1. **Analiza cada pieza**:
   - Imágenes → léelas (qué muestra, producto fiel, gancho visual, texto en imagen, calidad).
   - Videos → analízalos (hook 0–2s, ángulo, demo, ritmo, subtítulos, duración, CTA). Puedes usar
     `video_analysis_create` / `virality_predictor` del MCP de Higgsfield para hook/retención.
2. **Escribe los copys emparejados a cada creativo**: por pieza, **5 hooks + 5 títulos + 5 descripciones**
   (con emojis, compliant), alineados a lo que el video/imagen ya comunica. Marca el A/B recomendado.
3. Detecta huecos: si falta un ángulo fuerte de la investigación sin creativo → proponlo (ir a B).

### B) NO tiene media, pero TENEMOS generación (APIs/integraciones) → generamos nosotros
1. Desde los **ángulos de la investigación** (persona, dolores, deseos), genera:
   - **Imágenes** con IA (producto fiel — nunca redibujar el producto; WebP liviano). 3 variantes/ángulo.
   - **Videos/UGC** (Higgsfield Soul→imagen, Seedance→video): guion **Hook(0–2s) → demo(3–10s) →
     prueba/beneficio(10–20s) → oferta+CTA(20–30s)**, vertical 9:16.
2. Confirma datos reales que cuestan render ANTES (precio, claims, WhatsApp) — no quemar créditos.
3. Con las piezas generadas → escribe los copys (como en A.2).

### C) NO tiene media y NO hay saldo/API → prompts + LIBRETO ultra-detallado
1. **Prompt de imagen** listo para pegar en la IA que el cliente prefiera (sujeto/producto fiel +
   escena de la persona + estilo foto real + ratio 1:1 o 9:16 + negativos: no redibujar el producto).
2. **LIBRETO de video segundo a segundo** (ver plantilla abajo) — no un "guion vago" sino un informe
   recontra-full: qué grabar en cada segundo, qué decir, qué mostrar, texto en pantalla, tomas, sonido.
3. Deja **slots** en la campaña y marca el creativo como `[PENDIENTE GENERAR]`. Todo lo demás sigue.

## LIBRETO DE VIDEO — plantilla segundo a segundo (UGC/COD, 9:16, 20–35s)
Entrega esto por cada ángulo. Es lo que separa "hazte un video" de un creativo ganador.
| Tiempo | Fase | Qué DICE (voz) | Qué SE VE (toma) | Texto en pantalla |
|---|---|---|---|---|
| **0–3s** | 🪝 HOOK | Frase-gancho con el dolor/curiosidad (de la investigación). Pattern interrupt. | Primer plano cara o el problema en acción | Hook en grande |
| 3–8s | Problema/agitación | "Te pasa que…?" — agita el dolor con palabras del cliente | Muestra el problema real | frase corta |
| 8–15s | Producto + cómo actúa | Presenta el producto y **cómo funciona** (mecanismo) | Demo del producto en uso | nombre + beneficio |
| 15–22s | Prueba | Resultado/antes-después HONESTO, testimonio | Resultado, reacción real | "resultados reales" |
| 22–28s | Oferta + garantía COD | Precio/oferta + "pagas al recibir, sin adelantos" | Producto + empaque | oferta + 🚚 |
| 28–35s | CTA | "Pide el tuyo ahora, escribe/da clic" | CTA claro | botón/CTA |
- **Reglas**: hook en <3s o se pierde · subtítulos quemados · sonido en tendencia · vertical 9:16 ·
  producto fiel (no redibujar) · compliance (sin claims médicos/atributos personales) · 3 variantes de HOOK.
- Añade **lista de tomas/b-roll** a grabar y notas de edición (ritmo rápido, cortes cada 1–2s).

## PASO 2 — Emparejar y montar
- Cada creativo va con su set de copys. Súbelos al ad account (imagen/video → `ads_create_creative`)
  y monta la campaña (`05-publicar-mcp.md`), todo EN PAUSA.
- Compliance en todo (sin atributos personales/claims prohibidos). Producto fiel + WebP <150KB.

> Regla: el copy se escribe DESPUÉS de ver/definir el creativo, no antes. Un copy suelto sin pieza
> que lo respalde no se entrega.
