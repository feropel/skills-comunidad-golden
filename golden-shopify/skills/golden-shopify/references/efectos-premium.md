# Efectos premium — catalogo de snippets

Todos los snippets estan listos para copiar y pegar dentro de un bloque
`custom_liquid` o una seccion. Cada uno incluye lo necesario (CSS + HTML/JS).
Los snippets completos y conectados viven en `references/componentes/` y en los ejemplos (`examples/demo-shrine.json`).

## 1) Motor global de animaciones (reveal + tilt + contador)

Va en el **bloque 1 PROPUESTA DE VALOR** (primer bloque a cargar). Habilita
fade-in al scroll, tilt 3D en cards y contadores animados en TODA la pagina.

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

/* Montserrat para body en todos los containers premium */
.gg-formula-header,.pe-pyramid,.pe-reviews,.pe-faq,.pe-manifesto,.logistics-bar,.gg-benefits,.gg-launch-banner,.gg-countdown,.gg-guarantee,.custom-price-section,.pe-mq,.pe-mqb,.pe-ptitle,.product-rating{font-family:'Montserrat',sans-serif;}

/* Reveal: elementos invisibles hasta que entran al viewport */
.gg-guarantee,.pe-pyramid,.pe-reviews,.pe-faq,.pe-manifesto,.logistics-bar,.gg-benefits{opacity:0;transform:translateY(28px);transition:opacity .85s cubic-bezier(.16,1,.3,1),transform .85s cubic-bezier(.16,1,.3,1);}
.pe-revealed{opacity:1 !important;transform:translateY(0) !important;}

/* Tilt: cards listas para reaccionar al mouse */
.pe-review,.pe-note,.pe-faq__item{transition:transform .35s cubic-bezier(.16,1,.3,1),box-shadow .35s ease;transform-style:preserve-3d;will-change:transform;}
</style>

<script>
document.addEventListener('DOMContentLoaded',function(){
  // REVEAL ON SCROLL (anti-flash: marca como revealed si ya esta visible)
  var sel='.gg-guarantee,.pe-pyramid,.pe-reviews,.pe-faq,.pe-manifesto,.logistics-bar,.gg-benefits';
  function inView(el){var r=el.getBoundingClientRect();return r.top<window.innerHeight*0.95 && r.bottom>0;}
  var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('pe-revealed');io.unobserve(e.target);}});},{threshold:0.12,rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll(sel).forEach(function(el){if(inView(el))el.classList.add('pe-revealed');else io.observe(el);});

  // TILT 3D EN CARDS (mouse-based rotation)
  document.querySelectorAll('.pe-review,.pe-note,.pe-faq__item').forEach(function(card){
    card.addEventListener('mousemove',function(e){
      var r=card.getBoundingClientRect();
      var rx=((e.clientY-r.top-r.height/2)/(r.height/2))*-5;
      var ry=((e.clientX-r.left-r.width/2)/(r.width/2))*5;
      card.style.transform='perspective(900px) rotateX('+rx+'deg) rotateY('+ry+'deg) translateZ(8px)';
    });
    card.addEventListener('mouseleave',function(){
      card.style.transform='perspective(900px) rotateX(0) rotateY(0) translateZ(0)';
    });
  });

  // CONTADOR ANIMADO (numeros que suben hasta el valor real al entrar al viewport)
  // ANTI-BUG 0.0: si por cualquier razon el observer no dispara, el numero queda en su
  // valor final (data-target), nunca en 0.0. Fallback a los 1.2s por si acaso.
  function setFinal(el){var t=parseFloat(el.dataset.target);var d=(el.dataset.target.indexOf('.')>=0)?1:0;el.textContent=t.toFixed(d);}
  var cIO=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){var el=e.target;var t=parseFloat(el.dataset.target);var d=(el.dataset.target.indexOf('.')>=0)?1:0;var dur=1400;var start=performance.now();function tick(now){var p=Math.min((now-start)/dur,1);var eased=1-Math.pow(1-p,3);el.textContent=(t*eased).toFixed(d);if(p<1)requestAnimationFrame(tick);else setFinal(el);}requestAnimationFrame(tick);cIO.unobserve(el);}});},{threshold:0.4});
  document.querySelectorAll('.pe-counter').forEach(function(c){cIO.observe(c);setTimeout(function(){if(parseFloat(c.textContent)===0)setFinal(c);},1200);});
});
</script>
```

Para usar el contador: poner `<span class="pe-counter" data-target="4.9">4.9</span>` en cualquier numero.
**IMPORTANTE (anti-bug 0.0):** el texto inicial del span debe ser el **valor final** (`4.9`),
NUNCA `0.0`. Así, si el JS no corre, igual se ve el número real y nunca un "0.0/5" roto.

Para usar tilt 3D: la card debe tener una de estas clases: `.pe-review`, `.pe-note`, `.pe-faq__item`. Para extender, agregar la clase a otros elementos y agregarla al `querySelectorAll` arriba.

## 2) Boton 3D premium con shine

```css
#custom-releasit-btn{
  all:unset;position:relative;display:flex;align-items:center;justify-content:center;
  cursor:pointer;user-select:none;
  width:100%;min-height:58px;padding:14px 20px;margin:12px 0;
  background:linear-gradient(180deg,#0F6F5C 0%,#0B5345 100%);
  color:#FFFFFF;font-size:16px;font-weight:800;letter-spacing:.6px;
  border-radius:16px;
  box-shadow:0 6px 0 #084035, 0 10px 20px rgba(15,111,92,.45),
             inset 0 1px 0 rgba(255,255,255,.25),
             inset 0 -2px 0 rgba(0,0,0,.15);
  overflow:hidden;text-shadow:0 1px 2px rgba(0,0,0,.2);
  transition:transform .2s ease,box-shadow .2s ease;
}
#custom-releasit-btn::before{content:"";position:absolute;top:0;left:-100%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);animation:ggBtnShine 3.5s infinite;pointer-events:none;}
#custom-releasit-btn:hover{transform:translateY(-3px);box-shadow:0 9px 0 #084035, 0 14px 28px rgba(15,111,92,.55), inset 0 1px 0 rgba(255,255,255,.3);}
#custom-releasit-btn:active{transform:translateY(3px);box-shadow:0 3px 0 #084035, 0 5px 10px rgba(15,111,92,.35), inset 0 1px 0 rgba(255,255,255,.2);}
@keyframes ggBtnShine{0%{left:-100%;}40%{left:140%;}100%{left:140%;}}
```

Adaptar el color con las variables Liquid del bloque (BTN_BG, BTN_BG_DARK, BTN_BG_HOVER).

## 3) Glassmorphism (vidrio esmerilado)

Aplicar a tarjetas (garantia, resenas, FAQ items, notas piramide):
```css
.elemento{
  background:rgba(255,255,255,.7);  /* o color claro con baja opacidad */
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(0,0,0,.06);
  border-radius:16px;
  box-shadow:0 8px 28px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.7);
}
```

Variante con tinte de color de acento:
```css
background:rgba(238,246,243,.6);  /* mint claro */
border:1px solid rgba(15,111,92,.3);
```

## 4) Particulas verdes flotantes

15 spans + animation. Va dentro de la seccion donde quieras particulas.

```html
<div class="pe-particles">
  <span></span><span></span><span></span><span></span><span></span>
  <span></span><span></span><span></span><span></span><span></span>
  <span></span><span></span><span></span><span></span><span></span>
</div>
<style>
.pe-particles{position:absolute;inset:0;pointer-events:none;overflow:hidden;}
.pe-particles span{position:absolute;width:5px;height:5px;border-radius:50%;background:#0F6F5C;opacity:.4;animation:peFloat 14s linear infinite;bottom:-10px;box-shadow:0 0 6px #0F6F5C;}
.pe-particles span:nth-child(1){left:6%;animation-delay:0s;animation-duration:11s;}
.pe-particles span:nth-child(2){left:14%;animation-delay:2s;animation-duration:13s;}
.pe-particles span:nth-child(3){left:22%;animation-delay:4s;animation-duration:10s;}
.pe-particles span:nth-child(4){left:32%;animation-delay:1s;animation-duration:15s;}
.pe-particles span:nth-child(5){left:42%;animation-delay:3s;animation-duration:12s;}
.pe-particles span:nth-child(6){left:52%;animation-delay:5s;animation-duration:11s;}
.pe-particles span:nth-child(7){left:62%;animation-delay:0s;animation-duration:14s;}
.pe-particles span:nth-child(8){left:72%;animation-delay:2s;animation-duration:13s;}
.pe-particles span:nth-child(9){left:82%;animation-delay:4s;animation-duration:10s;}
.pe-particles span:nth-child(10){left:92%;animation-delay:6s;animation-duration:12s;}
.pe-particles span:nth-child(11){left:18%;animation-delay:7s;animation-duration:14s;width:3px;height:3px;}
.pe-particles span:nth-child(12){left:38%;animation-delay:8s;animation-duration:11s;width:3px;height:3px;}
.pe-particles span:nth-child(13){left:58%;animation-delay:9s;animation-duration:13s;width:3px;height:3px;}
.pe-particles span:nth-child(14){left:78%;animation-delay:10s;animation-duration:12s;width:3px;height:3px;}
.pe-particles span:nth-child(15){left:48%;animation-delay:11s;animation-duration:15s;width:7px;height:7px;opacity:.3;}
@keyframes peFloat{0%{transform:translateY(0);opacity:0;}10%{opacity:.55;}90%{opacity:.4;}100%{transform:translateY(-120vh);opacity:0;}}
</style>
```

Para que las particulas no rompan el layout, el contenedor padre debe tener `position:relative; overflow:hidden;`.

## 5) Seccion Manifiesto cinematografica

Va como seccion full-width entre resenas y FAQ (o donde se quiera un momento emocional).
Las lineas aparecen con stagger (350ms cada una) al entrar al viewport.

```liquid
{% assign LINE_1 = "Hay mujeres que pasan." %}
{% assign LINE_2 = "Hay mujeres que se notan." %}
{% assign LINE_3 = "Y hay mujeres" %}
{% assign LINE_4 = "que dejan huella." %}
{% assign CLOSING = "Este perfume es para las terceras." %}

<section class="pe-manifesto">
  <!-- particulas (ver snippet 4) -->
  <div class="pe-manifesto__content">
    <p class="pe-manifesto__line" data-delay="0">{{ LINE_1 }}</p>
    <p class="pe-manifesto__line" data-delay="350">{{ LINE_2 }}</p>
    <p class="pe-manifesto__line" data-delay="700">{{ LINE_3 }}</p>
    <p class="pe-manifesto__line" data-delay="1050"><strong>{{ LINE_4 }}</strong></p>
    <p class="pe-manifesto__closing">{{ CLOSING }}</p>
  </div>
</section>
```

CSS clave:
```css
.pe-manifesto{position:relative;background:linear-gradient(135deg,#0d0f12 0%,#0F6F5C 100%);padding:70px 24px;overflow:hidden;text-align:center;color:#fff;}
.pe-manifesto__line{font-size:22px;font-family:'Playfair Display',Georgia,serif;font-weight:300;opacity:0;transform:translateY(20px);transition:opacity 1s cubic-bezier(.16,1,.3,1),transform 1s cubic-bezier(.16,1,.3,1);}
.pe-manifesto__line.pe-shown{opacity:1;transform:translateY(0);}
@media(min-width:990px){.pe-manifesto{padding:110px 24px;}.pe-manifesto__line{font-size:34px;}}
```

JS de stagger:
```js
(function(){var s=document.querySelector('.pe-manifesto');if(!s)return;var lines=s.querySelectorAll('.pe-manifesto__line');var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){lines.forEach(function(l){var d=parseInt(l.dataset.delay||0,10);setTimeout(function(){l.classList.add('pe-shown');},d);});io.unobserve(s);}});},{threshold:0.25});io.observe(s);})();
```

**Variante con partículas que se elevan (G2.3, absorbida de un build real).** En vez de remitir al
snippet 4, el manifiesto puede llevar su propia capa de partículas auto-contenida (puntos del color
`--brand-light` que suben y se desvanecen, 8 `span` con `left`/`animation-delay`/`duration` distintos):
```html
<div class="pe-manifesto__particles"><span></span>…×8</div>
```
```css
.pe-manifesto__particles{position:absolute;inset:0;pointer-events:none;}
.pe-manifesto__particles span{position:absolute;bottom:-10px;width:5px;height:5px;border-radius:50%;background:var(--brand-light);opacity:.45;box-shadow:0 0 6px var(--brand-light);animation:peFloat 14s linear infinite;}
.pe-manifesto__particles span:nth-child(1){left:8%;animation-delay:0s;animation-duration:11s;}
/* …nth-child(2..8): left 20/33/46/58/70/82/92%, delays y durations 10–15s distintos… */
@keyframes peFloat{0%{transform:translateY(0) translateX(0);opacity:0;}10%{opacity:.55;}90%{opacity:.4;}100%{transform:translateY(-120vh) translateX(30px);opacity:0;}}
```
Ventaja: no depende de otra sección, las partículas heredan el color de marca y suben atravesando
todo el bloque. Ideal para cierres emocionales (bienestar, salud, respiración).

## 6) Piramide olfativa 3D escalonada (perfumes)

En desktop, las 3 notas se inclinan creando profundidad (la del centro al frente,
las laterales rotadas hacia adentro). En movil, vertical normal.

```css
@media(min-width:990px){
  .pe-pyramid__grid{display:flex;flex-direction:row;gap:20px;perspective:1200px;transform-style:preserve-3d;}
  .pe-pyramid__grid .pe-note{flex:1;transform-style:preserve-3d;}
  .pe-pyramid__grid .pe-note:nth-child(1){transform:rotateY(12deg) translateZ(-30px) translateY(20px);transform-origin:right center;}
  .pe-pyramid__grid .pe-note:nth-child(2){transform:translateZ(20px);z-index:3;}
  .pe-pyramid__grid .pe-note:nth-child(3){transform:rotateY(-12deg) translateZ(-30px) translateY(20px);transform-origin:left center;}
  .pe-pyramid__grid .pe-note:hover{transform:translateZ(40px) translateY(-8px) rotateY(0);z-index:5;}
}
```

## 7) Tickers premium con shimmer + edge fade

**Ticker TOP** (fondo claro, separadores con diamantes):
```css
.pe-mq{position:relative;overflow:hidden;background:#ffffff;}
.pe-mq::before,.pe-mq::after{content:"";position:absolute;top:0;bottom:0;width:80px;z-index:2;pointer-events:none;}
.pe-mq::before{left:0;background:linear-gradient(90deg,#fff 0%,transparent 100%);}
.pe-mq::after{right:0;background:linear-gradient(-90deg,#fff 0%,transparent 100%);}
.pe-mq__track span::before{content:"◆";color:#0F6F5C;font-size:8px;margin-right:14px;opacity:.55;}
```

**Ticker BOT** (gradient + shimmer animado):
```css
.pe-mqb{position:relative;overflow:hidden;background:linear-gradient(135deg,#0B5345 0%,#0F6F5C 50%,#0B5345 100%);box-shadow:0 4px 24px rgba(15,111,92,.3),inset 0 1px 0 rgba(255,255,255,.15);}
.pe-mqb::before{content:"";position:absolute;top:0;left:-50%;width:50%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.14),transparent);animation:peShimmerBot 6s infinite;pointer-events:none;}
@keyframes peShimmerBot{0%{left:-50%;}40%{left:150%;}100%{left:150%;}}
.pe-mqb__track span::before{content:"✦";color:rgba(255,255,255,.65);font-size:11px;margin-right:14px;}
```

**⚠️ Marquee SIN HUECOS en PC ancho (G3.17).** Un ticker con pocos ítems deja un **espacio en blanco**
en PC ancho al hacer loop: la animación clásica es `translateX(0 → -50%)` con **dos mitades idénticas**,
así que a `-50%` la segunda mitad ya está calzando donde estaba la primera y el giro es continuo. El
problema aparece cuando **el contenido de cada mitad es más corto que un viewport de PC** (~1920px): entre
un ciclo y otro se ve el blanco. Regla: **repite el contenido las veces necesarias para que CADA mitad
supere el ancho de un viewport PC** (~1920px) y **mantén 2 mitades EXACTAMENTE idénticas** (para que `-50%`
sea continuo). Así SIEMPRE hay texto girando, sin blancos, en móvil y en PC.
```css
/* patrón anti-hueco: track = 2 mitades idénticas, cada mitad ≥ 1 viewport PC */
.pe-mqb__track{display:flex;width:max-content;animation:peMarquee 22s linear infinite;}
@keyframes peMarquee{from{transform:translateX(0);}to{transform:translateX(-50%);}}
/* cada .pe-mqb__half repite los ítems hasta pasar ~1920px; ambas mitades son copia exacta */
```

## 8) Featured-collection nativa con custom_css premium

Para productos relacionados con dropdown nativo de Shopify para elegir coleccion.
Va en el JSON template como una seccion (no como bloque):

```json
"seccion_relacionados": {
  "type": "featured-collection",
  "name": "PRODUCTOS RELACIONADOS",
  "custom_css": ["...CSS premium scoped..."],
  "settings": {
    "title": "También te puede encantar",
    "heading_size": "h2",
    "description": "<p>Otras fragancias que están conquistando</p>",
    "show_description": true,
    "description_style": "subtitle",
    "collection": "",
    "products_to_show": 4,
    "columns_desktop": 4,
    "color_scheme": "scheme-1",
    "image_ratio": "square",
    "show_view_all": true,
    "view_all_style": "solid",
    "columns_mobile": "1",
    "padding_top": 40,
    "padding_bottom": 40
  }
}
```

**ATENCION:** En Dawn, el campo `description` exige rich text → envolver en `<p>...</p>`
o Shopify rechazara con `FileSaveError: El parametro "description" no es valido`.

CSS premium scoped (incluir en el array `custom_css`):
```css
.card-wrapper{position:relative;transition:transform .4s cubic-bezier(.16,1,.3,1);opacity:0;animation:peCardIn .8s cubic-bezier(.16,1,.3,1) forwards;}
.card-wrapper:nth-child(1){animation-delay:.1s;}
.card-wrapper:nth-child(2){animation-delay:.22s;}
.card-wrapper:nth-child(3){animation-delay:.34s;}
.card-wrapper:nth-child(4){animation-delay:.46s;}
@keyframes peCardIn{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:translateY(0);}}
.card-wrapper:hover{transform:translateY(-10px);}
.card{border-radius:18px !important;box-shadow:0 4px 18px rgba(0,0,0,.06) !important;}
.card__media img{transition:transform .7s cubic-bezier(.16,1,.3,1) !important;}
.card-wrapper:hover .card__media img{transform:scale(1.08) !important;}
.card__badge .badge{background:linear-gradient(135deg,#ef4444,#dc2626) !important;color:#fff !important;border-radius:20px !important;}
.collection__view-all .button{background:linear-gradient(135deg,#0F6F5C,#0B5345) !important;color:#fff !important;border:none !important;border-radius:12px !important;}
```

Ver el CSS completo en `assets/related-products.premium.css.txt`.

## 9) Garantia con MODE de pago (3 variantes)

Variable Liquid arriba del bloque:
```liquid
{%- comment -%}
  MODE = como vendes en esta tienda. Opciones:
    "contraentrega" → solo pago al recibir
    "anticipado"    → solo pago anticipado online
    "ambos"         → contra entrega + pago anticipado (default recomendado)
{%- endcomment -%}
{% assign MODE = "ambos" %}
```

Render con `if/elsif/else`:
```liquid
{%- if MODE == "anticipado" -%}
  <strong>Pago 100% seguro</strong> con tarjetas, PSE o transferencia.
{%- elsif MODE == "ambos" -%}
  Elige cómo pagar: <strong>contra entrega</strong> al recibir o <strong>pago anticipado</strong> seguro online.
{%- else -%}
  <strong>Pagas al recibir</strong>, en la puerta de tu casa — sin transferencias.
{%- endif -%}
```

## 10) Precio dinamico con badge rojo pulse

Badge animado que contrasta con el verde de la marca:
```css
.custom-badge{position:relative;display:inline-block;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;font-size:11px;font-weight:800;padding:5px 11px;border-radius:8px;margin-left:12px;text-transform:uppercase;letter-spacing:.6px;box-shadow:0 4px 14px rgba(220,38,38,.45),inset 0 1px 0 rgba(255,255,255,.25);overflow:hidden;animation:peBadgePulse 2.2s ease-in-out infinite;}
.custom-badge::before{content:"";position:absolute;top:0;left:-100%;width:50%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);animation:peBadgeShine 3.5s infinite;}
@keyframes peBadgePulse{0%,100%{transform:scale(1);}50%{transform:scale(1.06);}}
@keyframes peBadgeShine{0%{left:-100%;}45%{left:200%;}100%{left:200%;}}
```

Pill "estas ahorrando":
```css
.custom-saving{display:inline-block;margin-top:8px;font-size:13px;color:#0F6F5C;font-weight:700;background:rgba(15,111,92,.08);padding:5px 14px;border-radius:20px;border:1px dashed rgba(15,111,92,.4);}
```

## 11) Fuentes Playfair Display + Montserrat

Cargar en bloque PROPUESTA DE VALOR (primer bloque) con `@import` al inicio del `<style>`:
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');
```

Aplicar:
- **Titulos** (`.pe-pyramid__title`, `.pe-reviews__title`, `.pe-faq__title`, `.gg-title`, etc.) → `font-family:'Playfair Display',Georgia,serif;`
- **Cuerpo y containers** (regla global en el bloque propuesta) → `font-family:'Montserrat',sans-serif;`
- **Manifesto lines** → `'Playfair Display'` (peso 300 light + cursiva queda hermoso)

Combos por vertical:
- **Perfume / belleza:** Playfair Display (titulos) + Montserrat (cuerpo) ← default
- **Salud / cosmetica:** Cormorant Garamond (titulos) + DM Sans (cuerpo)
- **Tech / modern:** Inter o Montserrat para todo
- **Lujo extremo / fashion:** Bodoni Moda (titulos) + Inter (cuerpo)

## 12) "Por que comprar?" responsive 4 columnas

Layout adaptativo: 1 col movil, 2 cols tablet, 4 cols desktop. Card oscura con
particulas, gradiente radial, hover lift, brillo sweep, subrayado animado.

Estructura:
```html
<div class="gg-wrapper">
  <div class="gg-benefits">
    <div class="gg-particles">...8 spans...</div>
    <h2 class="gg-title">{{ TITLE_TEXT }}</h2>
    <p class="gg-subtitle">{{ SUBTITLE_TEXT }}</p>
    <div class="gg-grid">
      <div class="gg-item">...</div>
      ...4 items...
    </div>
  </div>
</div>
```

Grid responsive:
```css
.gg-benefits{max-width:1100px;padding:50px 32px;background:linear-gradient(135deg,#0a0b0d 0%,#0F2E26 100%);border-radius:24px;}
.gg-grid{display:grid;grid-template-columns:1fr;gap:16px;}
@media(min-width:600px){.gg-grid{grid-template-columns:repeat(2,1fr);}}
@media(min-width:900px){.gg-grid{grid-template-columns:repeat(4,1fr);}}
.gg-item:hover{transform:translateY(-8px);border-color:rgba(15,111,92,.7);}
```

Ver el snippet equivalente en `references/componentes/` (efectos de la familia `efx-*`).
