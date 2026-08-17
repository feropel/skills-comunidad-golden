/* ============================================================
   GOLDEN PDF · auto-fit de tarjetas de prompt
   Corre en el navegador (Playwright / Chrome headless) ANTES de
   imprimir. Para cada .prompt-card:
     1) si es más alta que una página, baja el tamaño de letra
        (paso 0.5px) hasta que quepa — se mantiene nítida;
     2) como último recurso, escala la tarjeta para caber exacto.
   Así el bloque copiable SIEMPRE ocupa una sola página y nunca
   sale cortado. Al terminar marca window.__golden_fit_done = true
   para que el renderizador sepa que puede imprimir.
   ============================================================ */
function __goldenFit() {
  var PX_PER_MM = 3.7795275591; // 96dpi
  var rootStyle = getComputedStyle(document.documentElement);
  var maxMM = parseFloat(rootStyle.getPropertyValue('--card-max-mm')) || 250;
  var maxPx = maxMM * PX_PER_MM;

  // Avisos para el usuario: prompts que quedaron muy reducidos o escalados
  // (señal de que conviene partirlos en el contenido, no en la maquetación).
  window.__golden_warnings = [];

  var cards = document.querySelectorAll('.prompt-card');
  cards.forEach(function (card, i) {
    var body = card.querySelector('.prompt-body') || card;

    // 1) reducir tipografía hasta caber
    var fs = parseFloat(getComputedStyle(body).fontSize);
    var guard = 0;
    while (card.getBoundingClientRect().height > maxPx && fs > 7 && guard < 120) {
      fs -= 0.5;
      body.style.fontSize = fs + 'px';
      body.style.lineHeight = (fs * 1.4) + 'px';
      guard++;
    }

    // 2) último recurso: escalar la tarjeta completa para caber exacto
    var scaled = false;
    var h = card.getBoundingClientRect().height;
    if (h > maxPx) {
      var k = maxPx / h;
      card.style.transformOrigin = 'top left';
      card.style.width = (100 / k) + '%';   // compensa el ancho antes de escalar
      card.style.transform = 'scale(' + k + ')';
      card.classList.add('was-scaled');
      scaled = true;
    }

    var finalFs = parseFloat(getComputedStyle(body).fontSize);
    var title = (card.querySelector('.prompt-title') || {}).textContent || '';
    if (scaled || finalFs < 8) {
      window.__golden_warnings.push({
        index: i + 1, title: title,
        font_px: Math.round(finalFs * 10) / 10, scaled: scaled
      });
    }
  });

  window.__golden_fit_done = true;
}

// Correr el auto-fit SOLO cuando las fuentes de marca ya cargaron: si no,
// se mide (y se imprime) con métricas equivocadas y el texto puede salir con
// la fuente de respaldo, corrompiendo hasta el copiar-pegar.
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(__goldenFit);
} else {
  __goldenFit();
}
