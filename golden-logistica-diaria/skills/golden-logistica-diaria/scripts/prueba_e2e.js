/* PRUEBA DE PUNTA A PUNTA · cosechar -> detallar -> descargar
   ------------------------------------------------------------------------------
   Corre el cosechador REAL de la skill contra un Dropi SIMULADO con la forma real
   de las respuestas, y comprueba que el archivo que sale trae el contrato que
   consumen el motor y el cruce.

   POR QUE EXISTE: se afirmo una vez "e2e con las piezas propias, 72 de 72" sin que
   existiera el script ni la salida. Toda corrida que se afirme apunta a su artefacto,
   y este es el artefacto.

   LIMITE, declarado: la red esta SIMULADA. Lo que queda probado es el CONTRATO entre
   las piezas, no la respuesta viva del servidor de Dropi. La corrida contra el API
   vivo sigue pendiente y esta declarada en SKILL.md.

     node prueba_e2e.js <ruta de cosecha-dropi.js> [salida.json]
*/
const fs = require('fs');
const RUTA = process.argv[2];
const SALIDA = process.argv[3] || '/tmp/e2e-volcado.json';
if (!RUTA) { console.error('uso: node prueba_e2e.js <cosecha-dropi.js> [salida.json]'); process.exit(2); }

let fallos = 0;
const juzgar = (q, ok) => { if (!ok) fallos++; return ok ? '· BIEN' : '· FALLA'; };

const N_ORD = 120, SHOP = 900001;
const ESTADOS = ['PENDIENTE', 'PREPARADO PARA TRANSPORTADORA', 'NOVEDAD', 'ENTREGADO',
                 'DEVOLUCION', 'RECLAME EN OFICINA', 'DESPACHADA', 'NOVEDAD SOLUCIONADA'];
const orden = i => ({
  id: 90000 + i, shop_id: i % 7 === 0 ? String(SHOP) : SHOP,   // uno de cada 7 en TEXTO
  status: ESTADOS[i % ESTADOS.length],
  name: 'Cliente' + i, surname: 'Prueba', phone: '30011122' + String(i).padStart(2, '0'),
  dir: 'Calle ' + i + ' # 3 - 4', city: 'MEDELLIN', state: 'ANTIOQUIA',
  total_order: '69900.00', shipping_company: 'ENVIA',
  distribution_company: { id: 1, name: 'ENVIA' },
  shipping_guide: 'G' + i, notes: 'Bolso: Negro Azabache ***',
  created_at: '2026-08-01 10:00:00', warehouse: { name: 'SUPPLI' }, shop: { name: 'Dolce' },
  orderdetails: [{ product: { name: 'Bolso' }, product_id: null, variation_id: 829674,
                   variation: { values: [] } }]
});

global.window = global;
global.localStorage = { length: 1, key: () => 'tk',
  getItem: () => 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQ1MjU3Nn0.x' };
global.sessionStorage = { length: 0, key: () => null, getItem: () => null };
global.document = { title: '', createElement: () => ({ click(){}, remove(){}, style: {} }),
  body: { appendChild(){}, removeChild(){} } };
global.URL = { createObjectURL: () => 'blob:x' };
global.Blob = class { constructor(a) { global.__ULTIMO = a[0]; } };

let pagina = 0;
global.fetch = async (url) => {
  const md = url.match(/orders\/myorders\/(\d+)$/);
  if (md) {
    // el DETALLE: la unica via para cantidad, costo, flete y ganancia
    return { ok: true, json: async () => ({
      shipping_amount: '19105.50', dropshipper_amount_to_win: '30794.50',
      orderdetails: [{ product: { name: 'Bolso' }, product_id: null, variation_id: 829674,
        variation: { values: [] }, quantity: '2.00', price: '69900.00',
        supplier_price: '20000.00' }] }) };
  }
  if (url.includes('fingerprint')) {
    return { ok: true, json: async () => ({ data: { found: true, phone: 'x',
      global_profile: { risk_label: 'Probable', lifetime_totals: { orders: 5, delivered: 3, returned: 1 } },
      context_analysis: { my_shop: { by_courier: [{ courier_id: 1, delivered: 3, returned: 1 }] },
                          other_shops: { by_courier: [] } } } }) };
  }
  if (url.includes('result_number=1')) return { ok: true, json: async () => ({ objects: [] }) };
  if (url.includes('myorders/v2')) {
    pagina++;
    const arr = pagina === 1 ? Array.from({ length: N_ORD }, (_, i) => orden(i)) : [];
    return { ok: true, json: async () => ({ objects: arr }) };
  }
  return { ok: false, status: 404 };
};

(async () => {
  (0, eval)(fs.readFileSync(RUTA, 'utf8'));
  await new Promise(r => setTimeout(r, 40));

  console.log('--- 1 · cosechar()');
  const c = await global.cosechar([SHOP]);
  console.log('   ordenes', c.ordenes, '· accionables', c.accionables, '· huellas', c.huellas,
              juzgar('cosecha', c.ordenes === N_ORD));

  console.log('--- 2 · detallar()');
  const d = await global.detallar();
  console.log('   pedidos', d.pedidos, '· guardados', d.guardados, '· fallidos', d.fallidos,
              juzgar('detalle', d.guardados === d.pedidos && d.fallidos === 0));

  console.log('--- 3 · descargar()');
  global.descargar();
  const J = JSON.parse(global.__ULTIMO);
  fs.writeFileSync(SALIDA, JSON.stringify(J));

  const acc = new Set(J.accionables);
  const A = J.ordenes.filter(o => acc.has(o.id));
  const noAcc = J.ordenes.filter(o => !acc.has(o.id));

  console.log('--- 4 · el CONTRATO que consumen el motor y el cruce');
  const conCant = A.filter(o => o.cantidad_dropi === 2).length;
  const conCosto = A.filter(o => o.costo === 40000).length;
  const conFlete = A.filter(o => o.flete === 19105.5).length;
  const conGan = A.filter(o => o.ganancia === 30794.5).length;
  console.log('   cantidad_dropi', conCant + '/' + A.length, juzgar('cant', conCant === A.length));
  console.log('   costo         ', conCosto + '/' + A.length, juzgar('costo', conCosto === A.length));
  console.log('   flete         ', conFlete + '/' + A.length, juzgar('flete', conFlete === A.length));
  console.log('   ganancia      ', conGan + '/' + A.length, juzgar('gan', conGan === A.length));

  console.log('--- 5 · null JAMAS cero en las que no se detallaron');
  const ceros = noAcc.filter(o => o.costo === 0 || o.flete === 0 || o.ganancia === 0).length;
  const nulos = noAcc.filter(o => o.costo === null && o.flete === null && o.ganancia === null).length;
  console.log('   sin detalle', noAcc.length, '· en null', nulos, '· en CERO', ceros,
              juzgar('nulos', ceros === 0 && nulos === noAcc.length));

  console.log('--- 6 · marcas de completitud');
  console.log('   cosecha_completa', J.cosecha_completa, '· detalles_completos', J.detalles_completos,
              juzgar('marcas', J.cosecha_completa === true && J.detalles_completos === true));

  console.log('--- 7 · shop_id en TEXTO entra igual');
  const enTexto = J.ordenes.filter(o => o.id % 7 === 0).length;
  console.log('   ordenes con shop_id de texto cosechadas:', enTexto,
              juzgar('texto', enTexto > 0));

  console.log(fallos ? `\nFALLARON ${fallos} comprobaciones` :
              `\ntodas las comprobaciones e2e pasaron · volcado en ${SALIDA}`);
  process.exit(fallos ? 1 : 0);
})();
