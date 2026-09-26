// Barrido de letras montadas: recorre la página y cruza las cajas de todos los textos visibles.
// Se pega en la consola (o por javascript_tool) con la página cargada, a 390 y a 1280 de ancho.
// CONTRATO con la página (ver references/piezas-pagina-por-escenas.md, pieza 1):
//   · escenas: <section data-scene="nombre"> y una función global prog(seccion) → 0..1.
//   · la función que pinta cada escena: window.ESCENAS = { nombre: fn } si existe; si no, se busca
//     window[nombre]. Una escena sin función NO se salta en silencio: sale en `escenasSinFuncion`.
//   · texto que no cuenta (logos, adornos): marcarlo con data-barrido-ignorar.
//   · la barra fija superior se mide sola (primer nav/header fijo); se puede forzar con
//     window.BARRIDO_BARRA = 64.
(async () => {
  // Con el panel del navegador oculto, innerHeight vale 0 y el paso de media pantalla también:
  // el bucle no avanza nunca y el barrido se cuelga en silencio (medido el 24-sep). Se niega en voz alta.
  if (innerHeight < 200 || innerWidth < 200)
    return { error: `ventana de ${innerWidth}x${innerHeight}: con la pantalla oculta no se puede barrer. Hacerla visible o emular 390x844.` };
  const scenes =[...document.querySelectorAll("[data-scene]")];
  const fn = window.ESCENAS || {};
  const sinFuncion = new Set();
  const pintar = s => {
    const f = fn[s.dataset.scene] || window[s.dataset.scene];
    if (typeof f !== "function" || typeof window.prog !== "function") { sinFuncion.add(s.dataset.scene); return; }
    f(window.prog(s));
  };
  const fija = [...document.querySelectorAll("nav,header")].find(e => ["fixed", "sticky"].includes(getComputedStyle(e).position));
  const BARRA = window.BARRIDO_BARRA ?? (fija ? Math.round(fija.getBoundingClientRect().height) : 0);
  document.querySelectorAll(".reveal,[data-on]").forEach(e => e.classList.add("on"));
  document.querySelectorAll(".reveal").forEach(e => { e.style.transition = "none"; });
  const opEf = e => { let o = 1; for (let n = e; n && n !== document.body; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= +cs.opacity; } return o; };
  // Todo el body, no solo <main>: con "main *" una página sin <main> devolvía 0 textos y
  // "encimes: []", un verde falso (verificador, 24-sep). Se excluyen script, style y noscript.
  const textos = [...document.body.querySelectorAll("*")].filter(e =>
    !e.closest("script,style,noscript,template") &&
    [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1));
  if (!textos.length)
    return { error: "0 textos con contenido en la página: el barrido no midió nada. Revisar que la página cargó." };
  const pares = new Map();
  const H = innerHeight, total = document.documentElement.scrollHeight;
  for (let y = 0; y < total; y += H * 0.5) {
    scrollTo(0, y);
    // las escenas fijas se actualizan a mano: con la pestaña oculta el navegador casi no pinta cuadros
    scenes.forEach(s => { const r = s.getBoundingClientRect(); if (r.bottom < -50 || r.top > H + 50) return; pintar(s); });
    await new Promise(r => setTimeout(r, 30));
    // la barra superior tapa lo que pasa por debajo: sus textos y lo que queda bajo ella no cuentan
    const vis = textos.filter(e => !e.closest("[data-barrido-ignorar],.brand") && !(fija && fija.contains(e)))
      .map(e => { const b = e.getBoundingClientRect(); return { e, r: { left: b.left, right: b.right, bottom: b.bottom, top: Math.max(b.top, BARRA), width: b.width, height: b.bottom - Math.max(b.top, BARRA) } }; })
      .filter(o => o.r.width > 2 && o.r.height > 2 && o.r.bottom > BARRA && o.r.top < H && opEf(o.e) > 0.3);
    for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
      const A = vis[i], B = vis[j];
      if (A.e.contains(B.e) || B.e.contains(A.e)) continue;
      const ix = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left);
      const iy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
      if (ix > 4 && iy > 4) {
        const k = (A.e.textContent.trim().slice(0, 30)) + "  ×  " + (B.e.textContent.trim().slice(0, 30));
        if (!pares.has(k)) pares.set(k, Math.round(y));
      }
    }
  }
  window.__encimes = [...pares.entries()];
  return { ancho: innerWidth, barra: BARRA, escenas: scenes.length, escenasSinFuncion: [...sinFuncion],
           textosRevisados: textos.length, pasos: Math.ceil(total / (H * 0.5)), encimes: window.__encimes };
})();
