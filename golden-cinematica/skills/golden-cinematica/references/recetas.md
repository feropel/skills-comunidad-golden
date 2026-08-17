# Recetas Golden Cinemática — código real, con sus números

Todo probado para la **ruta HTML de un archivo** (el entregable normal de Golden): sin
npm, sin build, se publica en Vercel tal cual. Para Next/React, la misma lógica con
`@react-three/fiber`.

**Regla:** copia la receta y **cambia los tokens del bloque de arriba**. No toques el
motor hasta que la escena se vea bien quieta.

## Base — importmap (va en todas)

```html
<script type="importmap">
{"imports":{
  "three":"https://unpkg.com/three@0.169.0/build/three.module.js",
  "three/addons/":"https://unpkg.com/three@0.169.0/examples/jsm/"
}}
</script>
```

Sin esto nada funciona. La versión se fija a propósito: `latest` rompe páginas ya publicadas.

## 1 · Preloader con contador y cortina

El ritual de entrada. Es lo primero que separa "página" de "experiencia".

```html
<div id="pre">
  <div id="pre-bar"></div>
  <span id="pre-num">0</span>
</div>
<style>
:root{ --curtain:#FF6A1A; --ink:#fff; --ease:cubic-bezier(.76,0,.24,1); }
#pre{position:fixed;inset:0;z-index:99;background:#000;display:grid;place-items:center;
     clip-path:inset(0 0 0 0);transition:clip-path 900ms var(--ease)}
#pre.go{clip-path:inset(0 0 100% 0)}           /* la cortina sube y revela */
#pre-bar{position:absolute;bottom:0;left:0;height:2px;width:0;background:var(--curtain);
         transition:width 240ms linear}
#pre-num{font:600 clamp(48px,12vw,160px)/1 system-ui;color:var(--ink);
         font-variant-numeric:tabular-nums}
</style>
<script type="module">
const HOLD_AT = 90;          // se planta en 90 hasta que todo cargó de verdad
const MIN_VISIBLE_MS = 1300; // mínimo en pantalla aunque cargue al instante
const t0 = performance.now();
const num = document.getElementById('pre-num'), bar = document.getElementById('pre-bar');
let n = 0, listo = false;
window.addEventListener('load', () => { listo = true; });
const tick = () => {
  const techo = listo ? 100 : HOLD_AT;
  if (n < techo) n += Math.max(0.6, (techo - n) * 0.06);
  num.textContent = Math.round(n); bar.style.width = n + '%';
  const yaVaTiempo = performance.now() - t0 >= MIN_VISIBLE_MS;
  if (n >= 99.4 && yaVaTiempo) {
    num.textContent = '100'; bar.style.width = '100%';
    setTimeout(() => document.getElementById('pre').classList.add('go'), 180);
    return;
  }
  requestAnimationFrame(tick);
};
tick();
</script>
```

**Tokens que se cambian:** `--curtain` (color de la cortina), `HOLD_AT`, `MIN_VISIBLE_MS`,
la duración del `clip-path`. Nada más.

## 2 · Duna de partículas que ondula en loop

El fondo vivo. Miles de puntos emisivos formando una onda que nunca se detiene.

```js
import * as THREE from 'three';

// ── TOKENS
const COLS = 220, ROWS = 120, SEP = 0.055;   // densidad de la malla
const AMP = 0.9, VEL = 0.00035;              // altura de la onda y velocidad
const C_VALLE = 0xFFF1D0, C_CRESTA = 0xE03A00;
const FONDO = 0x000000;

const esc = new THREE.Scene();
esc.background = new THREE.Color(FONDO);
const cam = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.1, 100);
cam.position.set(0, 2.6, 7);
cam.lookAt(0, 0, 0);

const N = COLS * ROWS;
const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
const a = new THREE.Color(C_VALLE), b = new THREE.Color(C_CRESTA);
let i = 0;
for (let x = 0; x < COLS; x++) for (let z = 0; z < ROWS; z++, i++) {
  pos[i*3]   = (x - COLS/2) * SEP;
  pos[i*3+2] = (z - ROWS/2) * SEP;
}
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
g.setAttribute('color',    new THREE.BufferAttribute(col, 3));
const puntos = new THREE.Points(g, new THREE.PointsMaterial({
  size: 0.018, vertexColors: true, transparent: true, opacity: 0.95,
  blending: THREE.AdditiveBlending, depthWrite: false   // el additive es lo que hace la brasa
}));
esc.add(puntos);

const rend = new THREE.WebGLRenderer({ antialias: true, alpha: false });
rend.setPixelRatio(Math.min(devicePixelRatio, 2));       // cap obligatorio
rend.setSize(innerWidth, innerHeight);
document.body.appendChild(rend.domElement);

// Onda: dos senos cruzados = ondulación orgánica sin librería de ruido
function anima(t) {
  const p = g.attributes.position.array, c = g.attributes.color.array;
  for (let k = 0; k < N; k++) {
    const x = p[k*3], z = p[k*3+2];
    const y = Math.sin(x*1.4 + t*VEL*1000) * Math.cos(z*1.1 + t*VEL*700) * AMP
            + Math.sin((x+z)*0.6 + t*VEL*400) * AMP * 0.35;
    p[k*3+1] = y;
    // altura → color. OJO: las dos ondas suman hasta AMP*1.35, no AMP.
    // Normalizar con AMP*2 saca el color de rango (-0.15 a 1.05) y ensucia los tonos.
    const m = Math.min(1, Math.max(0, (y + AMP*1.35) / (AMP*2.7)));
    c[k*3] = a.r + (b.r-a.r)*m; c[k*3+1] = a.g + (b.g-a.g)*m; c[k*3+2] = a.b + (b.b-a.b)*m;
  }
  g.attributes.position.needsUpdate = true;
  g.attributes.color.needsUpdate = true;
  rend.render(esc, cam);
  requestAnimationFrame(anima);
}
requestAnimationFrame(anima);
addEventListener('resize', () => {
  cam.aspect = innerWidth/innerHeight; cam.updateProjectionMatrix();
  rend.setSize(innerWidth, innerHeight);
});
```

**Por qué se ve caro:** `AdditiveBlending` + gradiente por altura = las crestas se
incendian solas. Sin eso son puntos grises.

## 3 · Objeto cromado que refleja el entorno

El "producto héroe". El reflejo es lo que lo hace ver caro, y sale **sin archivo HDRI**.

```js
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const rend = new THREE.WebGLRenderer({ antialias: true });
rend.setPixelRatio(Math.min(devicePixelRatio, 2));
rend.setSize(innerWidth, innerHeight);
rend.toneMapping = THREE.ACESFilmicToneMapping;   // sin esto el cromo se quema
rend.toneMappingExposure = 1.15;
document.body.appendChild(rend.domElement);

const esc = new THREE.Scene();
esc.background = new THREE.Color(0x000000);

// Entorno para los reflejos, generado en memoria (cero assets que descargar)
const pmrem = new THREE.PMREMGenerator(rend);
esc.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

const obj = new THREE.Mesh(
  new THREE.TorusKnotGeometry(1, 0.32, 220, 32),
  new THREE.MeshStandardMaterial({ metalness: 1, roughness: 0.05, color: 0xffffff })
);
esc.add(obj);

// UNA sola luz cálida — la regla del mecanismo 2
const key = new THREE.DirectionalLight(0xFFD9A0, 2.4);
key.position.set(3, 4, 2);
esc.add(key);

const cam = new THREE.PerspectiveCamera(45, innerWidth/innerHeight, 0.1, 100);
cam.position.set(0, 0, 5);

(function loop(t){
  obj.rotation.y = t * 0.00018;    // lento. Si se ve "girando", va muy rápido
  obj.rotation.x = Math.sin(t * 0.0002) * 0.15;
  rend.render(esc, cam);
  requestAnimationFrame(loop);
})(0);
```

**Variantes de material (solo cambia el bloque):**

```js
// Vidrio esmerilado
new THREE.MeshPhysicalMaterial({ transmission:1, thickness:1.2, roughness:0.2, ior:1.5, color:0xffffff })
// Mercurio líquido
new THREE.MeshStandardMaterial({ metalness:1, roughness:0, color:0xdfe6ee })
// Cerámica mate
new THREE.MeshStandardMaterial({ metalness:0, roughness:0.92, color:0xF5F2EA })
// Emisivo (brilla desde adentro)
new THREE.MeshStandardMaterial({ color:0x1B4CFF, emissive:0x1B4CFF, emissiveIntensity:1.6 })
```

## 4 · Wireframe blanco de 1px encima

Lo que convierte un objeto bonito en un instrumento técnico.

```js
const aro = new THREE.LineSegments(
  new THREE.WireframeGeometry(new THREE.IcosahedronGeometry(1.9, 1)),
  new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.16 })
);
esc.add(aro);
// gira al revés que el objeto: la contradicción es lo que se lee como "técnico"
aro.rotation.y = -obj.rotation.y * 0.6;
```

**Opacidad entre 0.10 y 0.20.** Más que eso se ve a jaula, no a instrumento.

## 5 · Cursor con inercia

Ningún objeto salta al cursor. **Lo persigue.**

```js
const LERP = 0.08;                    // 0.04 muy pesado · 0.15 muy nervioso
const mouse = {x:0,y:0}, suave = {x:0,y:0};
addEventListener('pointermove', e => {
  mouse.x = (e.clientX/innerWidth)*2 - 1;
  mouse.y = -(e.clientY/innerHeight)*2 + 1;
});
// dentro del loop:
suave.x += (mouse.x - suave.x) * LERP;
suave.y += (mouse.y - suave.y) * LERP;
obj.position.x = suave.x * 0.6;
obj.position.y = suave.y * 0.4;
cam.position.x = suave.x * 0.25;      // la cámara también, más sutil: da profundidad
```

## 6 · Bloom (el halo premium)

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const comp = new EffectComposer(rend);
comp.addPass(new RenderPass(esc, cam));
comp.addPass(new UnrealBloomPass(
  new THREE.Vector2(innerWidth, innerHeight),
  0.9,   // strength — 0.6-1.2. Arriba de 1.5 es una lámpara, no una página
  0.5,   // radius
  0.22   // threshold — qué tan brillante debe ser algo para florecer
));
// en el loop, comp.render() reemplaza a rend.render()
```

## 7 · Scroll cinemático (la cámara como dolly)

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
```

```js
gsap.registerPlugin(ScrollTrigger);
gsap.timeline({ scrollTrigger:{ trigger:'#acto2', start:'top bottom', end:'bottom top', scrub:1.2 }})
  .to(cam.position, { z: 2.4, y: 0.8, ease:'none' })
  .to(obj.rotation, { y: Math.PI * 1.5, ease:'none' }, 0);
```

**`scrub: 1.2`** es lo que da la sensación de cámara con peso. Con `scrub: true` el
movimiento va pegado al dedo y se siente barato.

## 8 · Rendimiento y fallback (obligatorio antes de entregar)

```js
// Pausa fuera del viewport: no quema batería
let visible = true;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; })
  .observe(rend.domElement);
// en el loop: if (!visible) { requestAnimationFrame(loop); return; }

// Respeta a quien pidió menos movimiento
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  rend.domElement.replaceWith(Object.assign(new Image(), {
    src:'/hero-fallback.webp', alt:'', style:'width:100%;height:100%;object-fit:cover'
  }));
}
```

El `hero-fallback.webp` es **un render de la misma escena**, no una foto cualquiera. Se
genera con Higgsfield o capturando el canvas: `rend.domElement.toDataURL('image/webp')`.

## 9 · Fondo de video pre-renderizado

El truco de rendimiento de los sitios de referencia: **lo caro se pre-renderiza.**

```html
<video autoplay muted loop playsinline poster="/hero-poster.webp"
       style="position:fixed;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2">
  <source src="/hero.webm" type="video/webm">
  <source src="/hero.mp4"  type="video/mp4">
</video>
```

**Reglas:** ≤ 3 MB, `muted loop playsinline` (sin `muted` iOS no reproduce solo),
`poster` siempre, y la capa WebGL o de UI va encima con `z-index` mayor. El video hace
el 80% del trabajo visual al 5% del costo de GPU.

## Checklist de la escena

- [ ] Bloque de tokens escrito ANTES del código
- [ ] Se ve bien **quieta** antes de animarla
- [ ] `setPixelRatio` con cap en 2
- [ ] Una sola escena WebGL en la página
- [ ] Pausa fuera del viewport
- [ ] Fallback para `prefers-reduced-motion` y gama baja
- [ ] Probada en móvil real, no solo en el Mac
- [ ] El texto encima se lee con contraste AA
