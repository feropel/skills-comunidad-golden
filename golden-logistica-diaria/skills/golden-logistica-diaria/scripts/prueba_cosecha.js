// Banco de pruebas del cosechador. Simula fetch y localStorage: nada de red real.
const casos = [];
let FALLOS = 0;
const juzgar = (nombre, ok) => { if (!ok) FALLOS++; return ok ? '· BIEN' : '· MAL'; };
const RUTA = process.argv[2];
if (!process.argv[2]) {
  // Sin argumento moria con un TypeError crudo. Un banco que no sabe decir como se
  // usa es un banco que nadie corre dos veces. `prueba_e2e.js` ya lo hacia bien.
  console.error('uso: node prueba_cosecha.js <ruta a cosecha-dropi.js>');
  process.exit(2);
}
let SIN_DETALLE = false;
function simular(nombre, ordenes, shops, cortarEnPagina, conDetalle) {
  global.window = global;
  global.localStorage = { length: 1, key: () => 'tk',
    getItem: () => 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjF9.x' };
  global.sessionStorage = { length: 0, key: () => null, getItem: () => null };
  global.document = { title: '', createElement: () => ({ click(){}, remove(){}, style:{} }),
    body: { appendChild(){}, removeChild(){} } };
  global.URL = { createObjectURL: () => 'blob:x' };
  global.Blob = class { constructor(a){ this.txt = a[0]; global.__ULTIMO = a[0]; } };
  let pagina = 0;
  global.fetch = async (url) => {
    if (url.includes('result_number=1')) return { ok: true, json: async () => ({ objects: [] }) };
    const md = url.match(/orders\/myorders\/(\d+)$/);
    if (md) {   // el DETALLE por id: la pieza que el banco no probaba
      if (SIN_DETALLE) return { ok: false, status: 500 };
      return { ok: true, json: async () => ({
        shipping_amount: '19105.50', dropshipper_amount_to_win: '30794.50',
        orderdetails: [{ product: { name: 'Bolso' }, product_id: null, variation_id: 829674,
          variation: { values: [] }, quantity: '2.00', price: '69900.00',
          supplier_price: '20000.00' }] }) };
    }
    if (url.includes('myorders/v2')) {
      if (cortarEnPagina !== null && pagina === cortarEnPagina) return { ok: false, status: 500 };
      pagina++;
      // pagina llena (500) para forzar que siga pidiendo
      const llena = [];
      for (let i = 0; i < 500; i++) llena.push(O(1000 * pagina + i, 900001));
      return { ok: true, json: async () => ({ objects: pagina === 1 ? llena : ordenes }) };
    }
    return { ok: false, status: 404 };
  };
  const fs = require('fs');
  const src = fs.readFileSync(RUTA, 'utf8');
  return (async () => {
    (0, eval)(src);
    await new Promise(r => setTimeout(r, 30));
    const r = await global.cosechar(shops);
    if (conDetalle) await global.detallar();
    global.__ULTIMO = null;
    global.descargar();
    return { resultado: r, json: global.__ULTIMO ? JSON.parse(global.__ULTIMO) : null,
             D: global.DROPI };
  })();
}
const O = (id, shop, st) => ({ id, shop_id: shop, status: st || 'PENDIENTE',
  orderdetails: [], distribution_company: { id: 1, name: 'ENVIA' }, phone: '3001112233' });

(async () => {
  // F5: shop_id como TEXTO debe cosecharse igual, no dar cero en silencio
  let a = await simular('F5', [O(7001, '900001'), O(7002, '900001')], [900001], null);
  const ids = a.json ? a.json.ordenes.map(o => o.id) : [];
  const entraron = ids.includes(7001) && ids.includes(7002);
  console.log('F5 shop_id en TEXTO -> las 2 en texto entraron:', entraron ? 'SI' : 'NO',
              '· total cosechado', ids.length, juzgar('F5', entraron));

  // F6: compuerta falla -> descargar() NO debe emitir nada
  let b = await simular('F6', [O(1, 900001)], [900001, 999999], null);
  console.log('F6 compuerta abortada -> JSON emitido:', b.json ? 'SI' : 'NO',
              '· abortada =', b.D.abortada, juzgar('F6', !b.json && b.D.abortada));

  // F7: pagina caida -> cosecha_completa debe ser false
  let c = await simular('F7', [O(1, 900001)], [900001], 0);
  console.log('F7 pagina caida en la primera -> ', c.json ? ('cosecha_completa=' + c.json.cosecha_completa) : 'sin JSON (compuerta lo freno, tambien BIEN)');

  // F7c: la SEGUNDA pagina cae, ya hay 500 ordenes cosechadas. El caso peligroso:
  // hay datos, parecen validos, y el total es mentira.
  let e = await simular('F7c', [O(1, 900001)], [900001], 1);
  console.log('F7c cae la 2a pagina con 500 ya cosechadas -> cosecha_completa =',
              e.json ? e.json.cosecha_completa : 'sin JSON',
              '· motivo:', e.json ? e.json.motivo_corte : '-',
              juzgar('F7c', e.json && e.json.cosecha_completa === false));

  // B2: detallar() SI se ejecuta y SI llena el contrato que el motor consume
  SIN_DETALLE = false;
  let g = await simular('B2', [O(8001, 900001)], [900001], null, true);
  const acc0 = g.json ? g.json.ordenes.filter(o => g.json.accionables.includes(o.id))[0] : null;
  console.log('B2 detallar() llena el contrato -> cantidad_dropi =', acc0 && acc0.cantidad_dropi,
              'costo =', acc0 && acc0.costo, 'flete =', acc0 && acc0.flete,
              juzgar('B2', acc0 && acc0.cantidad_dropi === 2 && acc0.costo === 40000 && acc0.flete === 19105.5));

  // B2b: si el detalle FALLA, los campos van en null, JAMAS en cero
  SIN_DETALLE = true;
  let h = await simular('B2b', [O(8002, 900001)], [900001], null, true);
  const acc1 = h.json ? h.json.ordenes.filter(o => h.json.accionables.includes(o.id))[0] : null;
  SIN_DETALLE = false;
  console.log('B2b detalle caido -> costo =', acc1 && acc1.costo, '· detalles_completos =',
              h.json && h.json.detalles_completos,
              juzgar('B2b', acc1 && acc1.costo === null && h.json.detalles_completos === false));

  // F7b: cosecha normal -> completa true
  let d = await simular('F7b', [O(1, 900001)], [900001], null);
  console.log('F7b cosecha normal -> cosecha_completa =', d.json.cosecha_completa,
              juzgar('F7b', d.json.cosecha_completa === true));
  // LO ACCIONABLE SE DEFINE POR NEGACION, Y EL BANCO TIENE QUE VERLO.
  // El banco viejo mandaba 501 ordenes TODAS en PENDIENTE: con ese fixture, una lista
  // positiva de estados y la negacion dan el mismo resultado, asi que el banco pasaba
  // entero sin poder distinguirlos — y la afirmacion falsa de que GUIA_GENERADA no
  // existia vivio meses debajo de un verde. **Un fixture de un solo estado no puede
  // probar una regla sobre estados.** Aqui van los tres casos que si la separan:
  // uno cerrado (fuera), uno con guia (dentro, y ademas «ya salio») y uno que no esta
  // en ninguna lista escrita a mano (dentro, que es el punto de la negacion).
  const mezcla = [O(9001, 900001, 'ENTREGADO'), O(9002, 900001, 'GUIA_GENERADA'),
                  O(9003, 900001, 'EN PUNTO DROOP')];
  let m = await simular('NEG', mezcla, [900001], null);
  const idsNeg = new Set(m.json.accionables || []);
  console.log('NEG entregado FUERA de accionables', juzgar('NEG-cerrado', !idsNeg.has(9001)));
  console.log('NEG guia generada DENTRO           ', juzgar('NEG-guia', idsNeg.has(9002)));
  console.log('NEG estado nunca listado DENTRO    ', juzgar('NEG-nuevo', idsNeg.has(9003)));
  const guia = (m.json.ordenes || []).find(o => o.id === 9002);
  console.log('NEG guia generada cuenta como «ya salio»',
              juzgar('NEG-yasalio', !!guia && m.json.ya_salieron > 0));

  // Sin esto el banco salia 0 aunque todo fallara, y una prueba que siempre pasa
  // no distingue "esta bien" de "no esta mirando".
  if (FALLOS) { console.error('\nPRUEBAS FALLIDAS: ' + FALLOS); process.exit(1); }
  console.log('\ntodas las pruebas del cosechador pasaron');
})();
