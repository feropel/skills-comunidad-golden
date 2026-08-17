/* Cosecha de huellas del panel de Dropi.
   Se pega en la consola (Cmd+Option+J) con la cola YA filtrada y Mostrar 500.
   Verifica el telefono DENTRO del modal antes de dar por buena cada huella. */
(() => {
  const tick = () => new Promise(r => { const c = new MessageChannel(); c.port1.onmessage = () => r(); c.port2.postMessage(0); });
  const wait = async ms => { const end = Date.now() + ms; while (Date.now() < end) await tick(); };
  const cerrar = () => {
    const x = [...document.querySelectorAll('button,.close,[aria-label="Close"],.modal-header span')]
      .find(b => /^(×|x|cerrar)$/i.test(b.textContent.trim()));
    if (x) x.click(); else document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', keyCode:27, bubbles:true}));
  };
  const filas = () => [...document.querySelectorAll('tbody tr')].map(tr => {
    const td = [...tr.querySelectorAll('td')].map(c => c.innerText.replace(/\s+/g,' ').trim());
    const tel = (tr.innerText.match(/Tel:\s*(\d[\d\s]{6,14})/) || [])[1];
    return { tr, orden: td[1], cliente: td[3], estatus: td[4], transp: td[5],
             tel: tel ? tel.replace(/\s/g,'') : null,
             sinRegistro: /Sin registro|no ha realizado órdenes/i.test(tr.innerText) };
  });

  window.HUELLAS = window.HUELLAS || {};
  window.cosechar = async (max = 5) => {
    const log = []; let n = 0;
    for (const f of filas()) {
      if (n >= max || window.HUELLAS[f.orden]) continue;
      if (f.sinRegistro) { window.HUELLAS[f.orden] = {sinRegistro:true, tel:f.tel}; log.push(f.orden+' sin-registro'); n++; continue; }
      cerrar(); await wait(500);
      const ic = f.tr.querySelector('.buyer-history-icon');
      if (!ic) { window.HUELLAS[f.orden] = {error:'sin icono'}; log.push(f.orden+' sin-icono'); n++; continue; }
      ic.click();
      let ok = false;
      for (let w = 0; w < 20; w++) {
        await wait(350);
        const t = document.body.innerText, k = t.indexOf('Historial del comprador');
        if (k < 0) continue;
        const seg = t.slice(k, k + 3000);
        // la cuarta linea del modal es el telefono: comparar AHI, no en toda la pagina
        if (seg.split('\n').map(s => s.trim())[3] === f.tel) {
          window.HUELLAS[f.orden] = {tel:f.tel, cliente:f.cliente, transp:f.transp, texto:seg};
          ok = true; break;
        }
      }
      log.push(f.orden + (ok ? ' OK' : ' FALLO'));
      n++; cerrar(); await wait(400);
    }
    document.title = Object.keys(window.HUELLAS).length + ' huellas';
    return log;
  };
  window.descargar = () => {
    const b = new Blob([JSON.stringify(window.HUELLAS, null, 1)], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = 'huellas-dropi.json'; a.click();
  };
  console.log('listo · corre: await cosechar(5) las veces que haga falta · luego descargar()');
})();
