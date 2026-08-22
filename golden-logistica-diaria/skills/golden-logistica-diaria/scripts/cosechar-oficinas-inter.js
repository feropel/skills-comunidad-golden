/* LAS OFICINAS DE INTERRAPIDISIMO EN TODA COLOMBIA · se pega en la consola de Chrome
   ------------------------------------------------------------------------------
   Se abre esta pagina, se pega esto en la consola (Cmd+Option+J) y se corre:

     https://www3.interrapidisimo.com/portalconsulta/Vista/Cobertura/CoberturaNacional.aspx

     await cosecharOficinas()      <- baja el pais entero y descarga el JSON

   Solo LECTURAS de una consulta publica. No manda ni un dato de nadie.

   POR QUE EXISTE, y es un mandato de FER del 2026-08-16 nacido de devoluciones reales:
   **quien se sabe la direccion de la oficina la escribe pelada.** «Carrera 7 # 4-47»,
   sin decir «oficina» ni nombrar la transportadora. El motor la lee como la casa del
   cliente, ve que otra transportadora es mas barata y cambia — y el paquete sale a
   repartir a la oficina de la competencia. En el informe eso salia como un ahorro.
   Palabras de FER: «muchas de las devoluciones es porque ponian la direccion asi».
   Y no es solo de pueblo: en Bogota pasa igual con quien vive cerca de una oficina.

   SE BAJA UNA VEZ Y QUEDA EN DISCO. La corrida diaria NO entra aqui: compara contra el
   archivo. Asi no depende de que el sitio este arriba a las 7 de la manana, no hay
   limite de consultas, y el insumo lleva su fecha como todos los demas.

   POR QUE NO ES UN SCRIPT DE PYTHON, que seria lo comodo: se intento y NO se puede.
   La pagina es un WebForms de ASP.NET cuyos dos desplegables hacen su propia ida y
   vuelta al servidor antes de que «Consultar» valga. Un POST sintetico con los combos
   ya rellenos responde **HTTP 500 siempre** — medido con seis variantes distintas. Hay
   que pasar por la interfaz. De ahi que esto viva en la consola, igual que
   `cosecha-dropi.js`.
*/
(() => {
  const REJILLA = 'gvCoberturaNacional';

  const filasDe = (doc) => {
    const g = doc.getElementById(REJILLA);
    if (!g) return null;
    return [...g.rows].slice(1)
      .filter(r => r.cells.length >= 4)
      .map(r => [...r.cells].slice(0, 4).map(c => c.innerText.trim()))
      .filter(f => f[0] && f[0] !== 'Departamento');
  };

  window.cosecharOficinas = async () => {
    if (!document.getElementById(REJILLA)) {
      console.error('ALTO. Primero elige «TODOS LOS DEPARTAMENTO» y «TODAS LAS CIUDADES» ' +
                    'y dale a Consultar. Esto pagina lo que ya esta en pantalla.');
      return null;
    }
    const F = document.forms[0];
    let estado = {};
    for (const el of F.elements) if (el.name && el.type !== 'submit') estado[el.name] = el.value;

    const vistos = new Set(), oficinas = [], porPagina = [];
    let corte = null;
    const prim = filasDe(document);
    porPagina.push(prim.length);
    prim.forEach(f => { vistos.add(f.join('|')); oficinas.push(f); });

    for (let p = 2; p < 400; p++) {
      const body = new URLSearchParams({ ...estado, __EVENTTARGET: REJILLA,
                                         __EVENTARGUMENT: 'Page$' + p });
      const r = await fetch(location.href, { method: 'POST', body,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
      if (!r.ok) { corte = 'la pagina ' + p + ' respondio HTTP ' + r.status; break; }
      const doc = new DOMParser().parseFromString(await r.text(), 'text/html');
      const filas = filasDe(doc);
      if (!filas || !filas.length) { corte = 'la pagina ' + p + ' no trajo filas'; break; }
      let nuevas = 0;
      filas.forEach(f => { const k = f.join('|');
        if (!vistos.has(k)) { vistos.add(k); oficinas.push(f); nuevas++; } });
      if (!nuevas) { corte = 'la pagina ' + p + ' repitio la anterior'; break; }
      porPagina.push(filas.length);
      // EL VIEWSTATE NUEVO ES OBLIGATORIO. Reenviar el viejo da 500 en la siguiente.
      const nf = doc.forms[0]; const ne = {};
      for (const el of nf.elements) if (el.name && el.type !== 'submit') ne[el.name] = el.value;
      estado = ne;
      document.title = 'oficinas ' + oficinas.length;
    }

    /* LA COMPUERTA DE COMPLETITUD, Y NO ES DECORATIVA.
       El final llega SIEMPRE como un error: pedir la pagina siguiente a la ultima
       devuelve HTTP 500. Asi que «hubo un error» **no distingue** «se acabo» de «se
       cayo a la mitad» — y en este expediente una cosecha a medias que parece entera
       es el fallo mas caro que hay.
       Lo que si distingue es la FORMA: todas las paginas llenas menos la ultima. Si la
       ultima viene llena, el corte ocurrio en medio y esto NO esta completo.
       Comprobado el 2026-08-16 en tres corridas: 92 paginas, 91 de 15 y una de 12,
       1.377 oficinas en 32 departamentos. */
    const llenas = porPagina.slice(0, -1);
    const tam = llenas.length ? Math.max(...llenas) : 0;
    const completa = porPagina.length > 1 && llenas.every(x => x === tam)
                     && porPagina[porPagina.length - 1] < tam;

    const D = {
      _fuente: 'consulta publica de cobertura nacional de Interrapidisimo',
      _url: location.href,
      generado: new Date().toISOString().slice(0, 10),
      cosecha_completa: completa,
      motivo_corte: corte,
      paginas: porPagina.length,
      filas_por_pagina: porPagina,
      total: oficinas.length,
      _ALCANCE: 'UNA oficina por municipio. En las ciudades grandes la fuente publica ' +
        'solo lista la PRINCIPAL (sale rotulada «OF. PRINC»), no las sucursales de ' +
        'barrio: medido, Bogota, Medellin, Barranquilla y Cartagena traen una sola fila ' +
        'cada una. Por eso este cruce NO cubre a quien escribe la direccion de una ' +
        'sucursal de barrio en una ciudad grande. Se declara para que nadie lea el ' +
        'cero de esa ciudad como «ahi no pasa».',
      oficinas: oficinas.map(f => ({ departamento: f[0], ciudad: f[1].split('\\')[0],
        ciudad_cruda: f[1], direccion: f[2].replace(/\s+/g, ' ').trim(),
        telefono: f[3].replace(/\s+/g, ' ').trim() })),
    };

    if (!completa) {
      console.error('COSECHA INCOMPLETA: ' + corte + '. Se descarga igual, pero va ' +
                    'marcada: el motor NO la usa para decidir envios.');
    }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(D, null, 1)],
                                          { type: 'application/json' }));
    a.download = 'OFICINAS-INTERRAPIDISIMO.json';
    document.body.appendChild(a); a.click(); a.remove();
    console.log(D.total + ' oficinas · ' + D.paginas + ' paginas · completa=' + completa);
    window.OFICINAS = D;
    return D;
  };

  console.log('listo. Elige TODOS/TODAS, dale Consultar, y corre:  await cosecharOficinas()');
})();
