/* ============================================================================================
   VIDRIO TEMPLADO · implementación de REFERENCIA, no una pieza lista para pegar.
   Ver references/piezas-pagina-por-escenas.md, pieza 2.

   Salió de una página real y depende de ella. Para usarla hay que proveerle este CONTRATO, que es
   COMPLETO: son los 11 nombres que el código usa y no declara (medidos el 24-sep-2026 con un
   barrido de identificadores libres, tras cargarla con el contrato viejo y ver "seg is not defined"):
     · $(id)               → document.getElementById
     · lerp(a, b, t)       → interpolación lineal
     · seg(x, a, b)        → avance 0..1 de x entre a y b, recortado
     · ease(t), easeOut(t) → curvas 0..1 (las de la pieza 1: motor de escenas)
     · sizeCanvas(canvas)  → ajusta el canvas a la ventana por dpr
     · dpr                 → devicePixelRatio con tope (la página usa [1, 2])
     · reduced             → true si prefers-reduced-motion
     · heroIntro           → el elemento al que se le añade la clase "go" al terminar
     · introK              → variable 0..1 que el resto de la página lee para su propia entrada
     · dibujarObjeto(ctx, x, y, radio, alfa, giro) → pinta el objeto que atraviesa el vidrio.
       Es de cada página: en la de origen era una esfera con textura
     · elementos: <canvas id="shatter">, <video id="vImpacto"> (el clip que se congela),
       <video id="vSigue"> (el que sigue después) y un "#hero .pin".
   🔴 Si falta uno, NO revienta: el try/catch de cada cuadro lo manda a console.error y SALTA la
   entrada entera (introK pasa a 1 al instante). Se ve como "la página cargó bien". Medido el
   24-sep en Chromium: con el contrato completo, introK va por 0,77 a los 3,5 s; sin `seg`, vale 1
   de inmediato. Tras adaptarla, mirar la consola, no la pantalla.

   LO QUE NO SE TOCA sin medir de nuevo: la geometría (22 rayos x 12 anillos, RAD), los tiempos
   (450 / 170 / 420 / 950 ms, retraso 230 ms), el seguro de 9 s y el try/catch de cada cuadro.
   ============================================================================================ */

/* ===== Entrada: un video real se congela y quiebra la pantalla ===== */
(function intro(){
  const cv=$("shatter"), ctx=cv.getContext("2d"), heroPin=document.querySelector("#hero .pin");
  const vG=$("vImpacto"), vP=$("vSigue");
  if("scrollRestoration" in history) history.scrollRestoration="manual";
  const arrancaSigue=()=>{ vP.play().catch(()=>{}); };
  let cerrada=false;
  const terminar=()=>{ if(cerrada) return; cerrada=true; cv.remove(); vG.style.display="none"; document.documentElement.style.overflow=""; heroIntro.classList.add("go"); introK=1; arrancaSigue(); };
  if(reduced || scrollY>40){ terminar(); return; }
  scrollTo(0,0);
  document.documentElement.style.overflow="hidden";
  sizeCanvas(cv);
  const W=cv.width, H=cv.height, ix=W*.5, iy=H*.46;
  const diag=Math.hypot(Math.max(ix,W-ix),Math.max(iy,H-iy))*1.05;
  const rnd=(a,b)=>a+Math.random()*(b-a);
  const off=(w,h)=>{ const c=document.createElement("canvas"); c.width=w; c.height=h; return c; };
  // punto del video (0..1) llevado a la pantalla con object-fit: cover
  const cover=(u,v)=>{ const vr=16/9, sr=W/H; let dw=W, dh=H, ox=0, oy=0;
    if(sr>vr){ dh=W/vr; oy=(H-dh)/2; } else { dw=H*vr; ox=(W-dw)/2; }
    return [ox+u*dw, oy+v*dh, dw, dh, ox, oy]; };

  /* ---------- geometría de un vidrio templado: rayos irregulares + anillos parciales ---------- */
  const N=22, RAD=[0,.018,.045,.085,.14,.21,.3,.41,.55,.72,.93,1.2], K=RAD.length;
  const angs=[...Array(N)].map((_,i)=>(i+rnd(-.38,.38))/N*Math.PI*2).sort((a,b)=>a-b);
  const node=angs.map(a0=>RAD.map((f,k)=>{ if(k===0) return [ix,iy];
    const a=a0+rnd(-.05,.05)*(1+k*.18), r=f*diag*rnd(.84,1.16); return [ix+Math.cos(a)*r, iy+Math.sin(a)*r]; }));
  // arista dentada, compartida por los dos fragmentos que separa
  const jag=(p,q,amp)=>{ const n=Math.max(2,Math.round(Math.hypot(q[0]-p[0],q[1]-p[1])/(11*dpr)));
    const nx=-(q[1]-p[1]), ny=q[0]-p[0], L=Math.hypot(nx,ny)||1, out=[p];
    for(let j=1;j<n;j++){ const t=j/n, o=rnd(-amp,amp)*Math.sin(Math.PI*t); out.push([lerp(p[0],q[0],t)+nx/L*o, lerp(p[1],q[1],t)+ny/L*o]); }
    out.push(q); return out; };
  const radial=node.map(row=>row.slice(0,-1).map((p,k)=>jag(p,row[k+1],(1.6+k*.9)*dpr)));
  const ring=[]; for(let k=1;k<K;k++) ring[k]=node.map((row,i)=>jag(row[k],node[(i+1)%N][k],(1.4+k*.7)*dpr));
  const ringVis=[]; for(let k=1;k<K;k++) ringVis[k]=node.map(()=>Math.random()<(k<4?.97:k<7?.6:.28));
  const shards=[];
  for(let i=0;i<N;i++){ const i2=(i+1)%N;
    for(let k=0;k<K-1;k++){
      const a=radial[i][k], b=radial[i2][k].slice().reverse();
      const pts = k===0 ? [...a, ...ring[1][i].slice(1), ...b.slice(1,-1)]
                        : [...a, ...ring[k+1][i].slice(1), ...b.slice(1), ...ring[k][i].slice().reverse().slice(1,-1)];
      const xs=pts.map(q=>q[0]), ys=pts.map(q=>q[1]);
      const c=[xs.reduce((s,v)=>s+v,0)/xs.length, ys.reduce((s,v)=>s+v,0)/ys.length];
      const x0=Math.max(0,Math.min(...xs)-4), y0=Math.max(0,Math.min(...ys)-4);
      const bb=[x0,y0,Math.min(W,Math.max(...xs)+4)-x0,Math.min(H,Math.max(...ys)+4)-y0];
      if(bb[2]<=0||bb[3]<=0) continue;
      const dx=c[0]-ix, dy=c[1]-iy, d=Math.hypot(dx,dy)||1, near=1-Math.min(1,d/diag);
      shards.push({pts,c,d,bb,ux:dx/d,uy:dy/d,near,
        rx:rnd(-2.4,2.4)*dpr, ry:rnd(-2.4,2.4)*dpr, tint:rnd(-.09,.09),        // refracción: cada trozo desvía la imagen
        ax:rnd(0,Math.PI), flip:rnd(.7,2.4)*(Math.random()<.5?-1:1), spin:rnd(-1.4,1.4), ph:rnd(0,6.28),
        push:rnd(.75,1.25)*(.35+near*1.1), zc:near*near*rnd(1.1,2.2), grav:rnd(.6,1.3)*(1.2-near),
        delay:(d/diag)*230+rnd(0,40) });
    } }
  const path=(c2,pts)=>{ c2.beginPath(); c2.moveTo(pts[0][0],pts[0][1]); for(let j=1;j<pts.length;j++) c2.lineTo(pts[j][0],pts[j][1]); c2.closePath(); };

  /* ---------- capas que se pintan una sola vez al romper ---------- */
  const snap=off(W,H), sctx=snap.getContext("2d");
  const frac=off(W,H), fctx=frac.getContext("2d");
  const crk=off(W,H), kctx=crk.getContext("2d");
  let usaVideo=false, fuenteVideo=false, from=null;
  const foto=new Image(); foto.src=vG.getAttribute("poster");
  const congelar=()=>{ sctx.fillStyle="#07080a"; sctx.fillRect(0,0,W,H);
    try{ const src=(fuenteVideo&&vG.readyState>=2)?vG:(foto.complete&&foto.naturalWidth?foto:null);
      if(src){ const c=cover(0,0); sctx.drawImage(src,c[4],c[5],c[2],c[3]); } }catch(e){}
    sctx.fillStyle="rgba(7,8,10,.12)"; sctx.fillRect(0,0,W,H); };
  const pintarVidrio=()=>{
    // imagen fracturada: cada fragmento desplazado y con su propio brillo
    fctx.drawImage(snap,0,0);
    shards.forEach(s=>{ fctx.save(); path(fctx,s.pts); fctx.clip();
      const b=s.bb; fctx.drawImage(snap,b[0],b[1],b[2],b[3],b[0]+s.rx,b[1]+s.ry,b[2],b[3]);
      fctx.fillStyle=s.tint>0?`rgba(255,255,255,${s.tint})`:`rgba(0,0,0,${-s.tint*1.4})`; fctx.fill(); fctx.restore(); });
    // grietas: sombra + filo de luz, más finas y tenues lejos del impacto
    const linea=(pts,fuerza)=>{
      kctx.beginPath(); kctx.moveTo(pts[0][0]+.8*dpr,pts[0][1]+.8*dpr); for(let j=1;j<pts.length;j++) kctx.lineTo(pts[j][0]+.8*dpr,pts[j][1]+.8*dpr);
      kctx.strokeStyle=`rgba(0,0,0,${.55*fuerza})`; kctx.lineWidth=2.2*dpr; kctx.stroke();
      kctx.beginPath(); kctx.moveTo(pts[0][0],pts[0][1]); for(let j=1;j<pts.length;j++) kctx.lineTo(pts[j][0],pts[j][1]);
      kctx.strokeStyle=`rgba(235,244,255,${.92*fuerza})`; kctx.lineWidth=(.7+fuerza*.6)*dpr; kctx.stroke(); };
    kctx.lineJoin="round"; kctx.lineCap="round";
    radial.forEach(row=>row.forEach((e,k)=>linea(e,Math.max(.25,1-k*.07))));
    for(let k=1;k<K;k++) ring[k].forEach((e,i)=>{ if(ringVis[k][i]) linea(e,Math.max(.2,.9-k*.08)); });
    // ramitas sueltas que salen de las grietas
    radial.forEach(row=>row.forEach((e,k)=>{ if(k<1||Math.random()>.45) return;
      const p=e[Math.floor(rnd(1,e.length-1))], a=rnd(0,6.28), l=rnd(8,34)*dpr;
      linea(jag(p,[p[0]+Math.cos(a)*l,p[1]+Math.sin(a)*l],1.2*dpr),Math.max(.2,.7-k*.06)); }));
    // zona triturada del impacto
    for(let j=0;j<90;j++){ const a=rnd(0,6.28), r=Math.pow(Math.random(),1.7)*diag*.05, l=rnd(3,16)*dpr, b=a+rnd(-.8,.8);
      const p=[ix+Math.cos(a)*r,iy+Math.sin(a)*r]; linea([p,[p[0]+Math.cos(b)*l,p[1]+Math.sin(b)*l]],rnd(.4,.9)); }
    const g=kctx.createRadialGradient(ix,iy,0,ix,iy,diag*.045); g.addColorStop(0,"rgba(255,255,255,.62)"); g.addColorStop(.5,"rgba(230,240,255,.2)"); g.addColorStop(1,"rgba(255,255,255,0)");
    kctx.fillStyle=g; kctx.beginPath(); kctx.arc(ix,iy,diag*.045,0,6.28); kctx.fill();
    for(let j=0;j<140;j++){ const a=rnd(0,6.28), r=Math.pow(Math.random(),1.4)*diag*.04, z=rnd(.6,2.6)*dpr;
      kctx.fillStyle=`rgba(255,255,255,${rnd(.25,.9)})`; kctx.beginPath(); kctx.moveTo(ix+Math.cos(a)*r,iy+Math.sin(a)*r);
      kctx.lineTo(ix+Math.cos(a)*r+z,iy+Math.sin(a)*r+z*.4); kctx.lineTo(ix+Math.cos(a)*r+z*.3,iy+Math.sin(a)*r-z); kctx.fill(); }
  };

  /* ---------- esquirlas finas que saltan al romper ---------- */
  const polvo=[...Array(260)].map(()=>{ const a=rnd(0,6.28), v=rnd(.25,1.6)*diag;
    return {x:ix+rnd(-6,6)*dpr, y:iy+rnd(-6,6)*dpr, vx:Math.cos(a)*v, vy:Math.sin(a)*v-rnd(0,.35)*diag, z:rnd(1,4.5)*dpr, rot:rnd(0,6.28), vr:rnd(-14,14), tw:rnd(0,6.28)}; });

  /* ---------- tiempos: el video llega al impacto, el objeto viene, el vidrio cede ---------- */
  let tA=null, APPROACH=620;
  const CONTACTO=.42; // segundo del clip en que el objeto sale hacia la cámara
  const conVideo=()=>{
    usaVideo=true; fuenteVideo=true; APPROACH=450; const p=cover(.66,.5); from=[p[0],p[1]];
    (function espera(){ if(vG.currentTime>=CONTACTO || vG.ended){ vG.pause(); tA=performance.now(); } else requestAnimationFrame(espera); })();
  };
  const sinVideo=()=>{ if(tA!==null||usaVideo) return; vG.pause(); usaVideo=true; fuenteVideo=false; APPROACH=450; const p=cover(.66,.5); from=[p[0],p[1]]; tA=performance.now()+300; };
  vG.addEventListener("playing",()=>{ if(tA===null && !usaVideo) conVideo(); },{once:true});
  vG.play().catch(sinVideo);
  setTimeout(()=>{ if(!usaVideo) sinVideo(); },1800);
  const saltar=()=>{ if(tA===null){ sinVideo(); } if(performance.now()-tA<APPROACH+420) tA=performance.now()-(APPROACH+420); };
  ["pointerdown","keydown","wheel","touchstart"].forEach(ev=>addEventListener(ev,saltar,{once:true,passive:true}));

  let roto=false, shook=false, went=false, prev=null, tPolvo=null, rotObjeto=0;
  // seguros: un error dentro de la animación o una pestaña congelada nunca dejan la página bloqueada
  setTimeout(terminar,9000);
  function tick(now){ if(cerrada) return; try{ cuadro(now); }catch(e){ console.error(e); terminar(); } }
  function cuadro(now){
    ctx.clearRect(0,0,W,H);
    if(tA===null || now<tA) return requestAnimationFrame(tick);
    const ms=now-tA, IMP=APPROACH, ROMPE=IMP+420, FIN=ROMPE+1350;

    if(ms<IMP){
      // el objeto sale del video y viene directo a la cámara, girando y con estela de velocidad
      const t=seg(ms,0,IMP), e=t*t*t;
      ctx.fillStyle=`rgba(7,8,10,${t*.3})`; ctx.fillRect(0,0,W,H);
      const bx=lerp(from[0],ix,ease(t)), by=lerp(from[1],iy,t)-Math.sin(t*Math.PI)*H*.05, br=lerp(.011*H,Math.min(W,H)*.085,e);
      rotObjeto+=.35;
      if(prev){ for(let j=5;j>=1;j--){ const f=j/6; dibujarObjeto(ctx,lerp(bx,prev[0],f*1.6),lerp(by,prev[1],f*1.6),br*(1-f*.12),.13*(1-f),rotObjeto-j*.08); } }
      dibujarObjeto(ctx,bx,by,br,1,rotObjeto);
      prev=[bx,by];
    } else {
      if(!roto){ roto=true; if(usaVideo) congelar(); else { sctx.fillStyle="#07080a"; sctx.fillRect(0,0,W,H); } vG.style.display="none"; pintarVidrio(); arrancaSigue(); }
      if(!shook){ shook=true; heroPin.classList.add("shake"); setTimeout(()=>heroPin.classList.remove("shake"),520); }
      const vuela=ms>ROMPE;
      if(!vuela){
        // el vidrio se fractura en una fracción de segundo, del centro hacia afuera
        const front=easeOut(seg(ms,IMP,IMP+170))*diag*1.3;
        ctx.drawImage(snap,0,0);
        ctx.save(); ctx.beginPath(); ctx.arc(ix,iy,front,0,6.28); ctx.clip(); ctx.drawImage(frac,0,0); ctx.drawImage(crk,0,0); ctx.restore();
        // el objeto se aplasta contra el vidrio y rebota hacia atrás
        const rb=seg(ms,IMP,IMP+380), r0=Math.min(W,H)*.085;
        const sq=Math.sin(Math.min(1,seg(ms,IMP,IMP+110))*Math.PI);
        ctx.save(); ctx.translate(ix,iy+rb*rb*H*.22); ctx.scale((1+sq*.16)*(1-rb*.45),(1-sq*.14)*(1-rb*.45)); dibujarObjeto(ctx,0,0,r0,1-rb,rotObjeto+rb*2); ctx.restore();
      } else {
        if(!went){ went=true; heroIntro.classList.add("go"); tPolvo=now; }
        introK=seg(ms,ROMPE,ROMPE+700);
        // los fragmentos saltan: giran en 3D, atrapan la luz en el canto y caen
        shards.forEach(s=>{
          const lt=seg(ms,ROMPE+s.delay,ROMPE+s.delay+950);
          if(lt>=1) return;
          const e=lt*lt, th=s.flip*lt*Math.PI, sx=Math.cos(th);
          const dist=e*(diag*.4+s.d*.55)*s.push, sc=1+e*s.zc;
          ctx.save();
          ctx.globalAlpha=1-Math.pow(seg(lt,.55,1),1.5);
          ctx.translate(s.c[0]+s.ux*dist, s.c[1]+s.uy*dist+e*e*H*.9*s.grav);
          ctx.rotate(s.spin*lt); ctx.rotate(s.ax); ctx.scale(Math.abs(sx)<.06?.06*Math.sign(sx||1):sx,1); ctx.rotate(-s.ax); ctx.scale(sc,sc);
          ctx.translate(-s.c[0],-s.c[1]);
          path(ctx,s.pts); ctx.save(); ctx.clip();
          const b=s.bb; ctx.drawImage(frac,b[0],b[1],b[2],b[3],b[0],b[1],b[2],b[3]);
          const luz=Math.pow(Math.max(0,Math.sin(th+s.ph)),10)*.75, sombra=(1-Math.abs(sx))*.4;
          if(luz>.01){ ctx.fillStyle=`rgba(255,255,255,${luz})`; ctx.fill(); }
          if(sombra>.01){ ctx.fillStyle=`rgba(0,0,0,${sombra})`; ctx.fill(); }
          ctx.restore();
          ctx.lineJoin="round"; ctx.strokeStyle=`rgba(205,230,255,${.35+luz*.6})`; ctx.lineWidth=1.3*dpr/sc; ctx.stroke();
          ctx.restore();
        });
        // polvo de vidrio: esquirlas que brillan al girar
        const dt=(now-tPolvo)/1000;
        polvo.forEach(p=>{ const x=p.x+p.vx*dt, y=p.y+p.vy*dt+.5*1.9*diag*dt*dt, a=Math.max(0,1-dt/1.15);
          if(a<=0) return; const tw=.35+.65*Math.abs(Math.sin(p.tw+dt*18));
          ctx.save(); ctx.globalAlpha=a*tw; ctx.translate(x,y); ctx.rotate(p.rot+p.vr*dt);
          ctx.fillStyle="rgba(235,245,255,.95)"; ctx.beginPath(); ctx.moveTo(-p.z,-p.z*.3); ctx.lineTo(p.z,-p.z*.1); ctx.lineTo(0,p.z*.8); ctx.closePath(); ctx.fill(); ctx.restore(); });
      }
      // destello del impacto: blanco, corto
      const f=1-seg(ms,IMP,IMP+140);
      if(f>0){ const g=ctx.createRadialGradient(ix,iy,0,ix,iy,diag*.6); g.addColorStop(0,`rgba(255,255,255,${.85*f})`); g.addColorStop(.25,`rgba(255,255,255,${.25*f})`); g.addColorStop(1,"rgba(255,255,255,0)"); ctx.fillStyle=g; ctx.fillRect(0,0,W,H); }
      if(ms>=FIN) return terminar();
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
