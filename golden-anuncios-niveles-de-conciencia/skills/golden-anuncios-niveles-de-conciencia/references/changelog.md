# Changelog de golden-anuncios-niveles-de-conciencia

## v1.2 · 2026-10-02 · ronda contra el verificador adversarial

`golden-verificador` dio 885/1000. Encontró que el validador de la v1.1 dejaba pasar una matriz vacía
y 31 de 33 matrices malas construidas fuera de su banco, y que daba 11 falsos rojos ("2.000 años"
leído como precio). La autoprueba pasaba 22 de 22 porque tenía un solo sabotaje por casilla: verde
barato. Lo que cambió, por clase y no por caso:
- **Validador v2, 25 casillas.**
  - Vocabularios cerrados (`pago`, `vertical`, `nivel`, `etapa`, `destino`, `relacion`).
  - Mínimo y máximo de ángulos (2 a 3), así que la matriz vacía ya no pasa.
  - Listas de palabras comparadas sin tildes ni mayúsculas y por palabra completa.
  - Cada casilla mira todos los campos de texto y el prompt.
  - Detector de precio que reconoce la unidad ("2.000 años", "4.000 mAh") y lee la "Q" como quetzal solo en Guatemala.
  - Casillas nuevas: texto literal dentro del prompt, datos privados, públicos pendientes, edad mínima, estudio que exista en disco, empresa y canal, plan que cubra todas las piezas.
  - Exit 2 ante forma inválida (antes salía con un error de Python y exit 1).
- **Autoprueba de 61 casos.** Dos matrices sanas a propósito incómodas (belleza en Colombia; hogar en
  Guatemala con pago mixto, cifras que no son precio y un nombre corto que es subcadena de otra
  palabra), 56 sabotajes con variantes por casilla y 3 de forma rota.
- **Contradicción rostros contra persona:** el negativo de la plantilla ahora excluye a famosos y a
  personas reales identificables, no a la persona de la escena.
- **Estudio anterior a la Fase 3.5:** se toman los ángulos de "Estrategia de mensaje" y de los huecos,
  y si no alcanzan se pide solo la Fase 3.5. Al terminar el estudio se retoma en la misma conversación.
- **Belleza y salud:** el ángulo de nivel bajo va como `unaware`, para no endurecer el claim.
- **Kevin pide un banco de 10 ángulos; la tanda lleva de 2 a 3.** Queda declarado en `fuentes-kevin.md`.
- La regla del 18% de Tasa de CPA se aclara como regla interna de Golden, que no vive en `golden-ads`.
- Ruta del changelog corregida tras el renombre.
- **Corrida real 1 (filtro de grifo):** matriz válida a la primera. El control malo, hecho con dos
  prompts reales de la casa, destapó un hueco nuevo de la casilla 14 ("PROHIBIDO… que diga"); se cerró
  y quedó en el banco. Entrega en `golden-despliegue-creativo-diseno/pruebas/`.

## v1.1 · 2026-10-02 · primera auditoría

Corrida de `golden-skill-auditor` desde la fábrica, el mismo día del nacimiento:
- Se eliminó `.claude/.cc-writes/`, una carpeta vacía que dejó el sandbox al escribir. El inventario la
  marcó como material fuera de las carpetas canónicas: se habría publicado.
- `evals/evals.json` pasó a `references/evals.json` (carpetas canónicas de la casa).
- **Contradicción corregida:** `formatos-de-estatico.md` decía "4:5 y 1:1 por pieza" mientras el
  esquema lleva una sola relación por pieza. Ahora: 4:5 por defecto y 1:1 como pieza aparte.
- El umbral del 40% para bajar el nivel se declara como punto de partida de la casa, sin medición.
- Casilla 06 del validador: además del nombre completo, revisa `nombre_corto`. Antes "Pixiu" en un
  titular TOFU pasaba si el producto se llamaba "Combo Pulsera Pixiu + Anillo". Nuevo sabotaje en la
  autoprueba (22 casos).
- Nombre final de la skill elegido por FER: `golden-anuncios-niveles-de-conciencia` (pasó por
  `golden-despliegue-creativo` y `golden-niveles-de-conciencia` el mismo día).

## v1.0 · 2026-10-02 · nace

- Pedido y aval de FER en el chat «✅ SKILL golden-anuncios-niveles-de-conciencia»: "vuélvelo una skill".
- Decisión de FER del mismo día: **exige estudio de mercado** mientras Kevin comparte su skill original.
- Base: demostración de Kevin Galeano en el taller del MBA del 01-oct (skill `vertex-despliegue-creativo`,
  módulo 3), clase M13 de Alejo del 30-sep, plano y anexos en
  `PROYECTOS/EL-CARTEL-DEL-CHAT/bootcamp-sep/mentores/golden-despliegue-creativo-diseno/` (49 leyes de
  la casa con casilla, investigación externa con fuentes, formatos 2026 verificados el 01-oct).
- Construye completo el módulo 3; los módulos 1, 4 y 2 son traspaso a skills existentes.
- `scripts/validar_matriz.py` con 20 casillas y autoprueba de 21 casos (1 sana y 20 saboteadas). En su
  primera corrida la autoprueba atrapó un fallo real del propio script: la casilla del sello BOFU
  contaba el CTA, que va fuera de la imagen. Corregido antes de instalar.
- Construida desde el chat de la fábrica, con aval directo de FER; reportada al Centro de Mando con
  `golden-bandeja`.
- Blindaje: se aplica cuando cierre en 1000 sin pendientes con dueño (estándar `chflags -R uchg`).

## Cómo se reporta

Cada cambio relevante de esta skill y cada corrida cerrada se reporta al Centro de Mando con
`golden-bandeja <ruta-del-parte.md>`, una sola llamada por parte.
