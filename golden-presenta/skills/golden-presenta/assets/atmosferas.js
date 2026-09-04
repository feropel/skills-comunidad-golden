/* ============================================================================
   GOLDEN PRESENTA · MOTOR DE ATMOSFERAS v1.0
   Fondos vivos para las presentaciones. Ocho, una por tipo de tema.

   POR QUE WEBGL PURO Y NO THREE.JS (decision medida, no gusto):
     - La ley de la skill es CERO dependencias de red. Three.js entra por CDN,
       y un CDN caido el dia de la presentacion es el desastre entero.
     - Hallazgo registrado en el Centro de Mando: un fragment shader de ~1 KB,
       interactivo al puntero, aguanta framerate pleno en movil donde una escena
       Three.js no. En trafico movil de Golden eso no es poca cosa.
     - Resultado: 8 atmosferas en un archivo, sin una sola peticion de red.

   COMO SE USA
     <body data-atmosfera="nebulosa">   ->  se activa sola al cargar
     Atmosfera.usar('enjambre')          ->  cambiar en caliente
     Atmosfera.apagar()

   SE TINE SOLA con los tokens de marca del deck: lee --accent, --accent-2 y
   --bg del CSS. Cambiar la paleta cambia el fondo. No hay color escrito aqui.

   RESPETA: prefers-reduced-motion (pinta UN fotograma y se detiene),
            document.hidden (se pausa, no quema bateria),
            dpr limitado a 1.5, y densidad reducida por debajo de 900 px.
   ============================================================================ */
(function (global) {
  'use strict';

  /* ---------- utilidades ---------- */

  function tokenColor(nombre, respaldo) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();
    return hexARgb(v || respaldo);
  }

  function hexARgb(h) {
    h = (h || '').replace('#', '');
    if (h.length === 3) h = h.charAt(0) + h.charAt(0) + h.charAt(1) + h.charAt(1) + h.charAt(2) + h.charAt(2);
    if (h.length !== 6) return [1, 1, 1];
    return [
      parseInt(h.substr(0, 2), 16) / 255,
      parseInt(h.substr(2, 2), 16) / 255,
      parseInt(h.substr(4, 2), 16) / 255
    ];
  }

  function rgbCss(c, alfa) {
    return 'rgba(' + Math.round(c[0] * 255) + ',' + Math.round(c[1] * 255) + ',' +
           Math.round(c[2] * 255) + ',' + alfa + ')';
  }

  var reduce = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DPR = Math.min(global.devicePixelRatio || 1, 1.5);

  /* ---------- ciclo de vida compartido ---------- */

  var actual = null;   // { canvas, parar }

  function crearLienzo() {
    var c = document.createElement('canvas');
    c.id = 'atmosfera';
    c.setAttribute('aria-hidden', 'true');
    // La opacidad sale del token --atmosfera-fuerza, para poder calmar el fondo
    // sin cambiar de atmosfera ni tocar el shader.
    var fuerza = getComputedStyle(document.documentElement)
                   .getPropertyValue('--atmosfera-fuerza').trim() || '1';
    c.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:0;' +
                      'pointer-events:none;display:block;opacity:' + fuerza;
    document.body.insertBefore(c, document.body.firstChild);
    return c;
  }

  function medir(c) {
    var w = Math.max(1, Math.floor(global.innerWidth * DPR));
    var h = Math.max(1, Math.floor(global.innerHeight * DPR));
    if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
    return [w, h];
  }

  /* Bucle con pausa por visibilidad y parada limpia. Todas las atmosferas
     pasan por aqui: es el unico sitio donde vive requestAnimationFrame. */
  function bucle(dibuja) {
    var vivo = true, rafId = null, t0 = performance.now();

    function frame(now) {
      if (!vivo) return;
      if (document.hidden) { rafId = requestAnimationFrame(frame); return; }
      dibuja((now - t0) / 1000);
      if (reduce) { vivo = false; return; }   // movimiento reducido: un solo fotograma
      rafId = requestAnimationFrame(frame);
    }
    rafId = requestAnimationFrame(frame);

    return function parar() {
      vivo = false;
      if (rafId) cancelAnimationFrame(rafId);
    };
  }

  /* Puntero con inercia: el fondo responde, pero nunca de golpe. */
  function puntero() {
    var o = { x: 0.5, y: 0.5, sx: 0.5, sy: 0.5 };
    function mover(e) {
      var t = e.touches ? e.touches[0] : e;
      o.x = t.clientX / global.innerWidth;
      o.y = t.clientY / global.innerHeight;
    }
    global.addEventListener('mousemove', mover, { passive: true });
    global.addEventListener('touchmove', mover, { passive: true });
    o.suavizar = function () {
      o.sx += (o.x - o.sx) * 0.045;   // 0.045 = estela larga, de cine
      o.sy += (o.y - o.sy) * 0.045;
    };
    return o;
  }

  /* ======================================================================
     WEBGL · el nucleo compartido de las atmosferas de shader
     ====================================================================== */

  var VERT = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';

  /* Ruido y fbm compartidos. Un solo bloque para los tres shaders. */
  var RUIDO = [
    'vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));',
    'return -1.+2.*fract(sin(p)*43758.5453123);}',
    'float nz(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);',
    'return mix(mix(dot(h2(i+vec2(0,0)),f-vec2(0,0)),dot(h2(i+vec2(1,0)),f-vec2(1,0)),u.x),',
    'mix(dot(h2(i+vec2(0,1)),f-vec2(0,1)),dot(h2(i+vec2(1,1)),f-vec2(1,1)),u.x),u.y);}',
    'float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*nz(p);p*=2.02;a*=.5;}return v;}'
  ].join('');

  function compilar(gl, tipo, src) {
    var s = gl.createShader(tipo);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn('[atmosfera] shader:', gl.getShaderInfoLog(s));
      return null;
    }
    return s;
  }

  /* Monta un fragment shader a pantalla completa. Devuelve la funcion de parada,
     o null si WebGL no esta disponible (ahi el llamador cae a una atmosfera 2D). */
  function montarShader(fragCuerpo) {
    var c = crearLienzo();
    var gl = c.getContext('webgl', { antialias: false, alpha: false, depth: false }) ||
             c.getContext('experimental-webgl');
    if (!gl) { c.parentNode.removeChild(c); return null; }

    var FRAG = 'precision mediump float;uniform vec2 u_res;uniform float u_t;' +
               'uniform vec2 u_m;uniform vec3 u_a;uniform vec3 u_b;uniform vec3 u_bg;' +
               RUIDO + 'void main(){vec2 uv=gl_FragCoord.xy/u_res.xy;' +
               'vec2 st=(gl_FragCoord.xy-.5*u_res.xy)/min(u_res.x,u_res.y);' + fragCuerpo + '}';

    var vs = compilar(gl, gl.VERTEX_SHADER, VERT);
    var fs = compilar(gl, gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) { c.parentNode.removeChild(c); return null; }

    var prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { c.parentNode.removeChild(c); return null; }
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'p');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var uRes = gl.getUniformLocation(prog, 'u_res'),
        uT   = gl.getUniformLocation(prog, 'u_t'),
        uM   = gl.getUniformLocation(prog, 'u_m'),
        uA   = gl.getUniformLocation(prog, 'u_a'),
        uB   = gl.getUniformLocation(prog, 'u_b'),
        uBg  = gl.getUniformLocation(prog, 'u_bg');

    var A  = tokenColor('--accent',   '#FFC637');
    var B  = tokenColor('--accent-2', '#6CCFFF');
    var BG = tokenColor('--bg',       '#07080B');
    var pt = puntero();

    var parar = bucle(function (t) {
      var wh = medir(c);
      pt.suavizar();
      gl.viewport(0, 0, wh[0], wh[1]);
      gl.uniform2f(uRes, wh[0], wh[1]);
      gl.uniform1f(uT, t);
      gl.uniform2f(uM, pt.sx, 1.0 - pt.sy);
      gl.uniform3f(uA, A[0], A[1], A[2]);
      gl.uniform3f(uB, B[0], B[1], B[2]);
      gl.uniform3f(uBg, BG[0], BG[1], BG[2]);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    });

    return { canvas: c, parar: parar };
  }

  /* Monta una atmosfera de canvas 2D. */
  function montar2D(dibuja) {
    var c = crearLienzo();
    var ctx = c.getContext('2d');
    var A  = tokenColor('--accent',   '#FFC637');
    var B  = tokenColor('--accent-2', '#6CCFFF');
    var pt = puntero();
    var estado = {};
    var parar = bucle(function (t) {
      var wh = medir(c);
      pt.suavizar();
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, wh[0], wh[1]);
      dibuja(ctx, wh[0], wh[1], t, pt, A, B, estado);
    });
    return { canvas: c, parar: parar };
  }

  /* ======================================================================
     LAS OCHO ATMOSFERAS
     ====================================================================== */

  var ATM = {};

  /* 1 · NEBULOSA — flujo de tinta lento. Lujo, marca, cosmetica, propuesta cara. */
  ATM.nebulosa = function () {
    return montarShader([
      'vec2 q=st*1.25;',
      'q+=(u_m-.5)*.35;',
      'float f=fbm(q*1.6+vec2(u_t*.045,u_t*.028));',
      'float g=fbm(q*2.4-vec2(u_t*.032,u_t*.05)+f*.9);',
      'float m=smoothstep(.05,.95,f*.6+g*.55+.5);',
      'vec3 col=mix(u_bg,mix(u_bg,u_a,.85),pow(m,2.4));',
      'col=mix(col,u_b,pow(smoothstep(.62,1.,g+.4),3.)*.35);',
      'col+=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)*.02;',
      'gl_FragColor=vec4(col,1.);'
    ].join(''));
  };

  /* 2 · AURORA — bandas verticales que respiran. Formacion, comunidad, MBA. */
  ATM.aurora = function () {
    return montarShader([
      'vec2 q=st;',
      'float on=0.;',
      'for(int i=0;i<3;i++){float fi=float(i);',
      'float x=q.x*1.1+fi*.55+(u_m.x-.5)*.4;',
      'float y=q.y+sin(x*2.1+u_t*(.22+fi*.07))*.22+fbm(vec2(x*1.4,u_t*.12+fi))*.3;',
      'on+=exp(-abs(y)*(5.5+fi*1.8))*(.55-fi*.11);}',
      'vec3 col=u_bg+mix(u_a,u_b,.5+.5*sin(u_t*.18+st.x*1.6))*on*1.35;',
      'col+=u_b*exp(-abs(st.y+.55)*7.)*.12;',
      'col+=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)*.018;',
      'gl_FragColor=vec4(col,1.);'
    ].join(''));
  };

  /* 3 · PULSO — anillos de interferencia. Evento, lanzamiento, energia, Cartel. */
  ATM.pulso = function () {
    return montarShader([
      'vec2 q=st;',
      'vec2 c1=vec2(sin(u_t*.19)*.42,cos(u_t*.15)*.3);',
      'vec2 c2=(u_m-.5)*1.5;',
      'float d1=length(q-c1),d2=length(q-c2);',
      'float w=sin(d1*17.-u_t*1.7)*.5+sin(d2*13.-u_t*1.15)*.5;',
      'float m=smoothstep(.15,1.,abs(w));',
      'float halo=exp(-d2*2.6)*.5;',
      'vec3 col=u_bg+mix(u_a,u_b,smoothstep(0.,1.,d1*1.3))*( (1.-m)*.42+halo*.55 );',
      'col*=1.-smoothstep(.55,1.35,length(q))*.55;',
      'gl_FragColor=vec4(col,1.);'
    ].join(''));
  };

  /* 3b · CANDELA — nube de brasa naranja a la izquierda, frio cian a la derecha,
     campo de estrellas detras. Evento del Cartel, marca personal con fuego,
     lanzamiento. Origen: el fondo del video de los 7 mentores de El Cartel del
     Chat (sitio/cartel-6.mp4), colores MUESTREADOS del frame a t=2s:
       candela pico #ff6926 · medio #854225 · base #4f2817
       cian #247684 · base cian #073238 · negro calido #280b05
     Esos hex viven aqui solo como documentacion: el shader NO los lleva quemados,
     usa u_a / u_b / u_bg como todas las demas, asi que cada deck se sigue viendo
     distinto segun sus tokens. Construida por el chat "Estructura y componentes
     de un skill" y verificada leyendo pixeles de vuelta (5 de 5 en su banco de
     pruebas, contra 2 de 5 del caso de control). Adoptada como NOVENA atmosfera,
     sin tocar `nebulosa`, para no cambiar los decks que ya la usan. */
  ATM.candela = function () {
    return montarShader([

  /* --- coordenadas: st centrado, uv 0..1 --- */
  'vec2 q=st*1.15;',
  'q+=(u_m-.5)*.18;',                       // el puntero mueve la nube, suave

  /* --- domain warping: da los filamentos de humo, no manchas --- */
  'float w1=fbm(q*1.30+vec2(u_t*.028,u_t*.017));',
  'float w2=fbm(q*1.90+vec2(-u_t*.021,u_t*.033)+w1*1.15);',
  'vec2 qw=q+vec2(w1,w2)*.55;',
  'float n=fbm(qw*2.10+vec2(u_t*.019,-u_t*.024));',
  'float d=fbm(qw*4.30-vec2(u_t*.037,u_t*.015));',

  /* --- densidad de nube --- */
  'float nube=smoothstep(-.18,.62,n*.85+d*.35);',

  /* --- ASIMETRIA: candela pesa a la izquierda, frio a la derecha --- */
  'float izq=smoothstep(.72,.02,uv.x);',
  'float der=smoothstep(.18,.92,uv.x);',

  /* --- nucleo de brasa: lo mas caliente, solo donde la nube es densa y a la izquierda --- */
  'float brasa=pow(smoothstep(.42,1.,nube),2.6)*izq;',
  'float vena=pow(smoothstep(.60,1.,n+d*.5),3.4)*izq;',   // filamentos encendidos

  /* --- composicion sobre negro calido --- */
  'vec3 col=u_bg;',
  'col=mix(col,u_a*.58,nube*izq*1.00);',                    // halo naranja
  'col=mix(col,u_a,brasa*.85);',                           // cuerpo de candela
  'col+=u_a*vena*.55;',                                    // venas encendidas
  'col=mix(col,u_b*1.05,pow(smoothstep(.12,.92,nube),1.25)*der*1.00);',  // frio a la derecha
  'col+=u_b*pow(smoothstep(.48,1.,d),2.2)*der*.85;',
  'col+=u_b*pow(der,2.2)*(.30+.55*nube)*.55;',   // halo frio de borde

  /* --- CAMPO DE ESTRELLAS: rejilla con hash, parpadeo lento --- */
  'vec2 sg=gl_FragCoord.xy/max(u_res.y,1.)*118.;',
  'vec2 si=floor(sg);',
  'float sh=fract(sin(dot(si,vec2(41.13,289.7)))*43758.5453);',
  'float est=step(.9955,sh);',                             // ~0.45% de celdas son estrella
  'vec2 sf=fract(sg)-.5;',
  'float sd=1.-smoothstep(.0,.34,length(sf));',
  'float tw=.72+.28*sin(u_t*1.6+sh*63.0);',                // titileo
  'float cielo=1.-smoothstep(.10,.72,nube);',              // la nube tapa las estrellas
  'col+=vec3(.88,.93,1.)*est*sd*tw*cielo*1.35;',

  /* --- vineta y grano (mata el banding del degradado) --- */
  'col*=1.-.24*pow(length(st)*.74,2.1);',
  'col+=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)*.022;',
  'gl_FragColor=vec4(col,1.);'
    ].join(''));
  };

  /* 4 · ENJAMBRE — nodos y enlaces. Comunidad, red, alumnos, networking. */
  ATM.enjambre = function () {
    return montar2D(function (ctx, w, h, t, pt, A, B, st) {
      if (!st.n) {
        var densidad = w < 900 * DPR ? 34 : 68;
        st.n = [];
        for (var i = 0; i < densidad; i++) {
          st.n.push({
            x: Math.random() * w, y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.22 * DPR,
            vy: (Math.random() - 0.5) * 0.22 * DPR,
            r: (Math.random() * 1.5 + 0.9) * DPR
          });
        }
      }
      var mx = pt.sx * w, my = pt.sy * h;
      var lim = Math.min(w, h) * 0.20;
      var n = st.n, i2, j;

      for (i2 = 0; i2 < n.length; i2++) {
        var p = n[i2];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
        // el puntero atrae con suavidad: la red se abre al pasar
        var dx = mx - p.x, dy = my - p.y, d = Math.hypot(dx, dy);
        if (d < lim * 1.5 && d > 1) { p.x += dx / d * 0.32; p.y += dy / d * 0.32; }
      }
      ctx.lineWidth = DPR;
      for (i2 = 0; i2 < n.length; i2++) {
        for (j = i2 + 1; j < n.length; j++) {
          var ax = n[i2].x - n[j].x, ay = n[i2].y - n[j].y;
          var dd = Math.hypot(ax, ay);
          if (dd < lim) {
            ctx.strokeStyle = rgbCss(A, (1 - dd / lim) * 0.20);
            ctx.beginPath(); ctx.moveTo(n[i2].x, n[i2].y); ctx.lineTo(n[j].x, n[j].y); ctx.stroke();
          }
        }
      }
      for (i2 = 0; i2 < n.length; i2++) {
        ctx.fillStyle = rgbCss(i2 % 5 === 0 ? B : A, 0.55);
        ctx.beginPath(); ctx.arc(n[i2].x, n[i2].y, n[i2].r, 0, 6.2832); ctx.fill();
      }
    });
  };

  /* 5 · RETICULA — malla que se hunde bajo el cursor. Tecnologia, datos, panel. */
  ATM.retabla = null;
  ATM.reticula = function () {
    return montar2D(function (ctx, w, h, t, pt, A, B, st) {
      var paso = (w < 900 * DPR ? 34 : 46) * DPR;
      var mx = pt.sx * w, my = pt.sy * h;
      var radio = Math.min(w, h) * 0.30;
      for (var x = paso * 0.5; x < w; x += paso) {
        for (var y = paso * 0.5; y < h; y += paso) {
          var dx = x - mx, dy = y - my, d = Math.hypot(dx, dy);
          var onda = Math.sin(d * 0.016 - t * 2.1) * Math.exp(-d / radio);
          var ox = (dx / (d || 1)) * onda * 11 * DPR;
          var oy = (dy / (d || 1)) * onda * 11 * DPR;
          var brillo = 0.10 + Math.max(0, onda) * 0.62;
          var r = (0.9 + Math.max(0, onda) * 1.7) * DPR;
          ctx.fillStyle = rgbCss(onda > 0.35 ? B : A, brillo);
          ctx.beginPath(); ctx.arc(x + ox, y + oy, r, 0, 6.2832); ctx.fill();
        }
      }
    });
  };

  /* 6 · DUNA — campo en perspectiva que ondula. Producto, marca propia, catalogo.
     Port 2D de la receta 2 de golden-cinematica, sin Three.js. */
  ATM.duna = function () {
    return montar2D(function (ctx, w, h, t, pt, A, B, st) {
      var COLS = w < 900 * DPR ? 46 : 88, ROWS = w < 900 * DPR ? 22 : 34;
      var horizonte = h * 0.42;
      ctx.globalCompositeOperation = 'lighter';   // el additive es lo que incendia las crestas
      for (var z = ROWS - 1; z >= 0; z--) {
        var pz = z / ROWS;
        var esc = 1 / (0.16 + pz * 1.5);
        var yBase = horizonte + (h - horizonte) * (1 - pz) * 0.98;
        for (var x = 0; x < COLS; x++) {
          var px = (x / COLS - 0.5);
          var sx = w * 0.5 + px * w * 1.45 * (0.22 + pz * 0.9);
          var onda = Math.sin(px * 7.0 + t * 0.9) * Math.cos(pz * 5.2 + t * 0.62) +
                     Math.sin((px + pz) * 4.1 + t * 0.4) * 0.35;
          var sy = yBase - onda * 26 * DPR * (0.3 + pz * 0.9);
          var m = Math.min(1, Math.max(0, (onda + 1.35) / 2.7));
          var col = [A[0] + (B[0] - A[0]) * m, A[1] + (B[1] - A[1]) * m, A[2] + (B[2] - A[2]) * m];
          ctx.fillStyle = rgbCss(col, (0.06 + m * 0.30) * (0.25 + pz * 0.75));
          ctx.beginPath(); ctx.arc(sx, sy, Math.max(0.6, esc * 0.55 * DPR), 0, 6.2832); ctx.fill();
        }
      }
      ctx.globalCompositeOperation = 'source-over';
    });
  };

  /* 7 · VIAJE — campo de estrellas con dolly. Vision, lanzamiento, apertura. */
  ATM.viaje = function () {
    return montar2D(function (ctx, w, h, t, pt, A, B, st) {
      if (!st.e) {
        st.e = [];
        var cuantas = w < 900 * DPR ? 130 : 280;
        for (var i = 0; i < cuantas; i++) {
          st.e.push({ x: (Math.random() - 0.5) * 2, y: (Math.random() - 0.5) * 2, z: Math.random() });
        }
      }
      var cx = w * 0.5 + (pt.sx - 0.5) * w * 0.10;
      var cy = h * 0.5 + (pt.sy - 0.5) * h * 0.10;
      var e = st.e;
      for (var i2 = 0; i2 < e.length; i2++) {
        var s = e[i2];
        s.z -= 0.0016;
        if (s.z <= 0.02) { s.z = 1; s.x = (Math.random() - 0.5) * 2; s.y = (Math.random() - 0.5) * 2; }
        var k = 0.55 / s.z;
        var sx = cx + s.x * k * w * 0.5;
        var sy = cy + s.y * k * h * 0.5;
        if (sx < -50 || sx > w + 50 || sy < -50 || sy > h + 50) continue;
        var kAnt = 0.55 / Math.min(1, s.z + 0.03);
        var px = cx + s.x * kAnt * w * 0.5, py = cy + s.y * kAnt * h * 0.5;
        var alfa = (1 - s.z) * 0.75;
        ctx.strokeStyle = rgbCss(i2 % 7 === 0 ? B : A, alfa);
        ctx.lineWidth = Math.max(0.6, (1 - s.z) * 2.1) * DPR;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(sx, sy); ctx.stroke();
      }
    });
  };

  /* 8 · NINGUNA — sin fondo. Corporativo sobrio, o cuando el contenido manda solo. */
  ATM.ninguna = function () { return null; };

  /* ======================================================================
     API
     ====================================================================== */

  var Atmosfera = {
    lista: ['nebulosa', 'candela', 'aurora', 'pulso', 'enjambre',
            'reticula', 'duna', 'viaje', 'ninguna'],

    usar: function (nombre) {
      this.apagar();
      var f = ATM[nombre];
      if (!f) { console.warn('[atmosfera] no existe:', nombre); return null; }
      var r = f();
      // Si WebGL no esta disponible, las de shader caen a una 2D equivalente.
      if (!r && nombre !== 'ninguna') {
        var respaldo = { nebulosa: 'duna', candela: 'duna',
                         aurora: 'reticula', pulso: 'enjambre' }[nombre];
        if (respaldo) {
          console.warn('[atmosfera] sin WebGL, se usa', respaldo);
          r = ATM[respaldo]();
        }
      }
      actual = r;
      document.body.setAttribute('data-atmosfera', nombre);
      return r;
    },

    apagar: function () {
      if (actual) {
        if (actual.parar) actual.parar();
        if (actual.canvas && actual.canvas.parentNode) {
          actual.canvas.parentNode.removeChild(actual.canvas);
        }
        actual = null;
      }
    },

    activa: function () { return document.body.getAttribute('data-atmosfera'); }
  };

  global.Atmosfera = Atmosfera;

  /* Arranque automatico por atributo del body */
  function arrancar() {
    var n = document.body.getAttribute('data-atmosfera');
    if (n && n !== 'ninguna') Atmosfera.usar(n);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }

})(window);
