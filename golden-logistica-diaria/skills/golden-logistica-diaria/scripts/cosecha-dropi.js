/* COSECHA DE DROPI DESDE LA CONSOLA · v2 · rutas confirmadas en vivo
   ------------------------------------------------------------------------------
   Se pega en la consola de Chrome (Cmd+Option+J) ESTANDO LOGUEADO en Dropi.
   Solo LECTURAS: no confirma, no edita, no genera guias.

   USO
     await cosechar([{ID_TIENDA}, {ID_TIENDA_2}])     <- TODAS las tiendas de esa marca
     descargar()

   Recibe una LISTA de shop_id porque una misma marca suele tener varias conexiones
   en Dropi: la de Shopify y la del bot son tiendas distintas. Excluir una pierde
   ventas reales — pasó, y por eso el argumento es lista y no numero suelto.

   COMPUERTA: si alguna de las tiendas pedidas NO aparece en lo que trajo, borra todo
   y se detiene. Sacar ordenes de una cuenta y presentarlas como de otra es el error
   mas caro de aqui.

   RUTAS CONFIRMADAS
     ordenes : GET  api.dropi.co/api/orders/myorders/v2?result_number=500&start=N
     huella  : GET  api-v2.dropi.co/bff/customers/fingerprint/v2
                    ?country_code=<PAIS>&user_id=<USER>&phone=<TEL>&months=0
     auth    : JWT de localStorage, cabecera  X-Authorization: Bearer
*/
(async () => {
  const dormir = ms => new Promise(s => setTimeout(s, ms));
  const D = window.DROPI = { ordenes: {}, huellas: {}, couriers: {}, user_id: null, shops: [] };

  let T = [];
  for (const s of [localStorage, sessionStorage])
    for (let i = 0; i < s.length; i++) {
      const x = s.getItem(s.key(i)) || '';
      (x.match(/eyJ[\w-]+\.[\w-]+\.[\w-]+/g) || []).forEach(m => T.push(m));
    }
  let H = null;
  for (const t of [...new Set(T)]) {
    try {
      const r = await fetch('https://api.dropi.co/api/orders/myorders/v2?result_number=1&start=0',
                            { headers: { 'X-Authorization': 'Bearer ' + t } });
      if (r.ok) {
        H = { 'X-Authorization': 'Bearer ' + t };
        try { D.user_id = JSON.parse(atob(t.split('.')[1])).sub; } catch (e) {}
        break;
      }
    } catch (e) {}
  }
  if (!H) { console.error('SIN AUTH. Recarga Dropi logueado y vuelve a pegar esto.'); return; }
  console.log('autenticado · user_id ' + D.user_id);

  /* LO ACCIONABLE SE DEFINE POR NEGACION, Y ESA ELECCION TIENE FACTURA.
     Aqui vivia una LISTA de estados accionables sacada del enum de UNA cuenta, con
     este comentario: "OJO: 'GUIA_GENERADA' NO existe en este panel". Se midio el
     2026-08-11 contra dos volcados reales y la afirmacion es FALSA:
       · volcado de GOLDEN del 11-ago: 54 pedidos en GUIA_GENERADA, de 3.426.
       · volcado de DOLCE del 10-ago: cero.
     Se midio en la unica cuenta donde daba cero y se escribio como ley del sistema.
     Contra los accionables REALES de Golden, esta lista habria conservado 49 de 132
     y perdido 83 — **$8.516.104 desaparecidos en silencio**, entre ellos los 54 con
     guia generada, que son justo los de la seccion que mas importa.

     LA CLASE: una lista de lo que SI entra convierte cualquier estado nuevo en un
     pedido invisible. La lista de lo que ya esta CERRADO, en cambio, es corta y
     estable, y un estado nuevo cae del lado visible: molesta, pero se ve. Se prefiere
     el ruido al silencio.
     Comprobado: por negacion salen exactamente los 78 accionables de Dolce y los 132
     de Golden, mas 'EN PUNTO DROOP', que ninguna lista escrita a mano tenia. */
  const CERRADOS = ['ENTREGADO', 'CANCELADO', 'RECHAZADO', 'SINIESTRO', 'DEVOLUCION',
                    'DEVOLUCION EN BODEGA', 'EN PROCESO DE DEVOLUCION',
                    'TRANSITO A DEVOLUCION PROVEEDOR'];
  const esAccionable = s => !CERRADOS.includes(String(s || '').toUpperCase().trim());
  /* Los que ya tienen guia o ya se movieron. GUIA_GENERADA va PRIMERO porque es la
     unica ventana que todavia se cierra a mano: mientras el paquete no salga, una
     guia mala aun se cambia. Esta lista SI es positiva a proposito — no marca que
     revisar, marca en que orden urge — y el config la pisa con 'estados'. */
  const YA_SALIO = ['GUIA_GENERADA', 'PREPARADO PARA TRANSPORTADORA', 'DESPACHADA',
                    'ENTREGADO A TRANSPORTADORA', 'RECOGIDO POR DROPI', 'EN REPARTO',
                    'EN RUTA', 'EN CAMINO', 'INTENTO DE ENTREGA', 'EN REEXPEDICION',
                    'EN TERMINAL DESTINO', 'EN BODEGA DESTINO', 'BODEGA DESTINO'];

  const traer = async url => {
    const r = await fetch(url, { headers: H });
    if (!r.ok) return null;
    const j = await r.json();
    return j.objects || j.data || null;
  };

  window.cosechar = async (shop_ids, pais, maxPag) => {
    pais = pais || 'CO'; maxPag = maxPag || 30;
    if (!Array.isArray(shop_ids) || !shop_ids.length) {
      console.error('Pasa una LISTA de shop_id. Ej: await cosechar([{ID_TIENDA}, {ID_TIENDA_2}])'); return;
    }
    D.shops = shop_ids.map(Number);
    if (D.shops.some(isNaN)) { console.error('Algun shop_id no es numero.'); return; }

    let start = 0; const paginas = [];
    D.completa = false; D.corte = null;
    for (let p = 0; p < maxPag; p++) {
      const arr = await traer('https://api.dropi.co/api/orders/myorders/v2?result_number=500&start=' + start);
      if (!arr) {
        // F7: una pagina caida a mitad NO puede pasar por "ya termine". Antes se hacia
        // break en silencio y se grababa el parcial como si fuera el total de la cuenta.
        D.corte = 'la pagina ' + p + ' no respondio';
        console.error('COSECHA INCOMPLETA: ' + D.corte + '. El volcado va marcado como incompleto.');
        break;
      }
      const antes = Object.keys(D.ordenes).length;
      for (const o of arr) {
        // F5: el shop_id llega a veces como texto. Si la compuerta compara por clave de
        // objeto (tolera texto) y la seleccion compara con === (no tolera), un shop_id
        // en texto pasa la compuerta y cosecha CERO sin dar error. Se normaliza aqui,
        // una sola vez, para que las dos comparaciones vean el mismo tipo.
        o.shop_id = (o.shop_id === null || o.shop_id === undefined) ? null : Number(o.shop_id);
        D.ordenes[o.id] = o;
        const dc = o.distribution_company;
        if (dc && dc.id != null && dc.name) D.couriers[dc.id] = dc.name;
      }
      paginas.push({ start: start, devolvio: arr.length, nuevos: Object.keys(D.ordenes).length - antes });
      start += arr.length;
      document.title = 'ordenes ' + Object.keys(D.ordenes).length;
      if (arr.length < 500) { D.completa = true; break; }
      await dormir(200);
    }
    if (!D.completa && !D.corte) { D.corte = 'se alcanzo el tope de ' + maxPag + ' paginas'; }
    D.paginas = paginas.length;
    const todas = Object.values(D.ordenes);
    const tiendas = {};
    for (const o of todas) tiendas[o.shop_id] = (tiendas[o.shop_id] || 0) + 1;
    console.table(paginas);
    console.log('tiendas en esta cuenta:', tiendas);

    const faltan = D.shops.filter(s => !tiendas[s]);
    if (faltan.length) {
      console.error('ALTO. Pediste ' + D.shops.join(', ') + ' y NO aparecen: ' + faltan.join(', '));
      console.error('Estas en el Chrome o el login equivocado. NO uses estos datos.');
      // F6: no basta con vaciar las ordenes. Antes D.shops quedaba puesto y descargar()
      // seguia vivo: emitia un JSON valido con CERO ordenes, y el motor y el informe
      // decian "todo en orden" sobre un conjunto que nunca se poblo.
      D.ordenes = {}; D.shops = []; D.abortada = true;
      D.corte = 'compuerta: faltaban las tiendas ' + faltan.join(', ');
      return;
    }
    const mias = todas.filter(o => D.shops.indexOf(o.shop_id) >= 0);
    const estados = {};
    for (const o of mias) estados[o.status] = (estados[o.status] || 0) + 1;
    console.log('tiendas ' + D.shops.join(' + ') + ': ' + mias.length + ' ordenes');
    console.log('estados reales:', estados);

    const acc = mias.filter(o => esAccionable(o.status));
    D.accionables = acc.map(o => o.id);
    const tels = [];
    for (const o of acc) {
      const t = (o.phone || '').replace(/\D/g, '').slice(-10);
      if (t.length === 10 && tels.indexOf(t) < 0) tels.push(t);
    }
    for (const t of tels) {
      if (D.huellas[t]) continue;
      try {
        const u = 'https://api-v2.dropi.co/bff/customers/fingerprint/v2?country_code=' + pais +
                  '&user_id=' + D.user_id + '&phone=' + t + '&months=0';
        const r = await fetch(u, { headers: H });
        D.huellas[t] = r.ok ? (await r.json()).data : { error: r.status };
      } catch (e) { D.huellas[t] = { error: 'fetch' }; }
      document.title = 'huellas ' + Object.keys(D.huellas).length + '/' + tels.length;
      await dormir(150);
    }
    let conH = 0;
    for (const k in D.huellas) if (D.huellas[k] && D.huellas[k].found) conH++;
    console.log('accionables ' + acc.length + ' · huellas con historial ' + conH + ' de ' + tels.length);
    return { tiendas: D.shops, ordenes: mias.length, accionables: acc.length, huellas: conH, estados: estados };
  };

  /* EL DETALLE POR ID. Verificado en vivo 2026-08-10:
     el LISTADO no trae `quantity`, ni `price`, ni `supplier_price`, ni `shipping_amount`,
     ni `dropshipper_amount_to_win`. Sus orderdetails traen cinco claves y ninguna es de
     plata ni de cantidad. Todo eso vive SOLO en el detalle, y la ruta buena lleva
     `myorders`: `/api/orders/{id}` a secas responde 404.
     Sin esta pasada, el volcado sale sin los campos que el motor y el cruce consumen. */
  window.detallar = async (ids) => {
    if (D.abortada) { console.error('La cosecha aborto. No se piden detalles.'); return; }
    ids = ids || D.accionables || [];
    D.detalles = D.detalles || {}; D.det_fallidos = [];
    let hechos = 0;
    for (const id of ids) {
      if (D.detalles[id]) { hechos++; continue; }
      try {
        const r = await fetch('https://api.dropi.co/api/orders/myorders/' + id, { headers: H });
        if (r.ok) { const j = await r.json(); D.detalles[id] = j.objects || j.data || j; }
        else D.det_fallidos.push({ id: id, status: r.status });
      } catch (e) { D.det_fallidos.push({ id: id, status: 'fetch' }); }
      hechos++;
      document.title = 'detalles ' + Object.keys(D.detalles).length + '/' + ids.length;
    }
    // Se cuenta lo GUARDADO, no lo intentado. Un bucle con la ruta mala devolvia 404 en
    // todas y el contador seguia subiendo como si todo fuera bien.
    const ok = Object.keys(D.detalles).length;
    D.detalles_completos = (ok === ids.length);
    console.log('detalles: ' + ok + ' de ' + ids.length + ' guardados' +
                (D.det_fallidos.length ? ' · fallaron ' + D.det_fallidos.length : ''));
    return { pedidos: ids.length, guardados: ok, fallidos: D.det_fallidos.length };
  };

  window.descargar = () => {
    if (D.abortada) {
      console.error('La cosecha ABORTO en la compuerta (' + D.corte + '). No se descarga nada.');
      return;
    }
    if (!D.shops.length) { console.error('Corre cosechar() primero.'); return; }
    const mias = Object.values(D.ordenes).filter(o => D.shops.indexOf(o.shop_id) >= 0);
    const acc = mias.filter(o => esAccionable(o.status));
    const salio = mias.filter(o => YA_SALIO.indexOf(o.status) >= 0);
    const num = x => (x === null || x === undefined || x === '') ? null : parseFloat(x);
    /* Las lineas se arman del DETALLE si lo hay, y si no del listado. Lo que no se
       sabe va en null, JAMAS en cero: un cero se suma como si fuera real.
       OJO CON EL COLOR: `variation.values` viene VACIO en el 100% de las lineas y
       `variation_id` no decodifica (el mismo id sale con diez colores distintos).
       El color de verdad vive en `notes`, como texto, una entrada por producto. */
    const lineas = o => {
      const det = (D.detalles || {})[o.id];
      const src = det ? (det.orderdetails || []) : (o.orderdetails || []);
      return src.map(d => ({
        product_id: d.product_id, variation_id: d.variation_id,
        producto: (d.product || {}).name || '',
        cantidad: num(d.quantity), precio: num(d.price), costo: num(d.supplier_price),
        valores: ((d.variation || {}).values || []).map(v => v.value)
      }));
    };
    const pack = o => {
      const det = (D.detalles || {})[o.id];
      const ls = lineas(o);
      const cant = ls.length && ls.every(l => l.cantidad !== null)
        ? ls.reduce((a, l) => a + l.cantidad, 0) : null;
      const costo = ls.length && ls.every(l => l.costo !== null && l.cantidad !== null)
        ? ls.reduce((a, l) => a + l.costo * l.cantidad, 0) : null;
      return {
      id: o.id, status: o.status, created: o.created_at,
      name: o.name, surname: o.surname, phone: o.phone, email: o.email,
      dir: o.dir, city: o.city, state: o.state, total: o.total_order, rate: o.rate_type,
      carrier: o.shipping_company, carrier_id: (o.distribution_company || {}).id,
      guide: o.shipping_guide, supplier: o.supplier_id, shop_id: o.shop_id,
      shop_name: (o.shop || {}).name, shop_type: (o.shop || {}).type,
      notes: o.notes, shop_order: o.shop_order_id, warehouse: (o.warehouse || {}).name,
      // lo que el motor y el cruce consumen. Sin detalle, todo esto va en null.
      tiene_detalle: !!det,
      cantidad_dropi: cant,
      costo: costo,
      flete: det ? num(det.shipping_amount) : null,
      ganancia: det ? num(det.dropshipper_amount_to_win) : null,
      lineas: ls
    };};
    const payload = {
      generado: new Date().toISOString(), shops: D.shops, user_id: D.user_id,
      // F7: el que lea este archivo tiene que poder distinguir "no hay mas" de
      // "no pude traer mas". El motor rechaza cosecha_completa:false salvo bandera.
      cosecha_completa: !!D.completa,
      paginas_traidas: D.paginas || 0,
      motivo_corte: D.corte || null,
      total_ordenes_cuenta: Object.keys(D.ordenes).length,
      ordenes: mias.map(pack),
      accionables: acc.map(o => o.id),
      detalles_pedidos: Object.keys(D.detalles || {}).length,
      detalles_completos: D.detalles_completos === true,
      detalles_fallidos: D.det_fallidos || [],
      ya_salieron: salio.map(o => o.id),
      huellas: D.huellas, couriers: D.couriers
    };
    const b = new Blob([JSON.stringify(payload)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b);
    a.download = 'dropi-' + D.shops.join('-') + '-' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a); a.click(); a.remove();
    console.log('descargado: ' + mias.length + ' ordenes · ' + acc.length + ' accionables · ' +
                salio.length + ' ya salieron · cosecha ' +
                (D.completa ? 'COMPLETA' : 'INCOMPLETA (' + D.corte + ')'));
  };

  console.log('listo. Corre, EN ESTE ORDEN:');
  console.log('  await cosechar([{ID_TIENDA}, {ID_TIENDA_2}])   <- ordenes y huellas');
  console.log('  await detallar()                   <- costo, flete, ganancia y cantidad');
  console.log('  descargar()');
})();
