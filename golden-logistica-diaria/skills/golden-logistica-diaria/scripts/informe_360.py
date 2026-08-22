#!/usr/bin/env python3
"""El informe 360 de una operacion COD: el asistente de WhatsApp y la logistica.

Norma FER (2026-08-10): un solo documento con las DOS mitades del negocio.
  PARTE 1 · el asistente de WhatsApp: TODOS los contactos, el embudo, donde se
           quedaron y POR QUE no compraron.
  PARTE 2 · la logistica: los pedidos que si entraron, transportadora, precio,
           efectividad y huella del cliente.

Sale en Markdown-Golden para build_pdf.py de golden-pdf-check.

REGLA HEREDADA de generar_informe_diario.py, y aqui vale igual: toda frase con
veredicto sale de una VARIABLE. Y cada cero dice si es "no hay" o "no se pudo ver".

  python3 informe_360.py --config cfg.json --decisiones d.json --embudo e.json \
      --analisis a.json --acciones dia.md --salida informe.md
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import (escribir_json, escribir_texto, exigir_salida_distinta,
                       leer_json, leer_texto)
from comun import (contacto_de, tel10, miles, miles_seguro, pesos, concuerda,
                   sustituir_exigiendo, exigir_presente,
                   preparar_destino_pdf, marcar_como_propio,
                   avisar_banderas, guias_por_corregir, causa_de_guia,
                   aviso_default_bodega, recortar)
from collections import Counter

ROJO, AMARILLO, VERDE = "🔴", "🟡", "🟢"



def _cob_universo(EMB):
    """La frase de cobertura del universo, SACADA DE LA VARIABLE.

    Aqui habia un literal: "Son todos los contactos del espacio de Chatea, no una
    muestra" — escrito a mano, y por tanto verdadero para siempre aunque el barrido
    se quedara a medias. En la misma pagina, tres clausulas mas abajo, el informe
    explicaba que el analisis corria sobre un subconjunto. Las dos frases no podian
    ser ciertas a la vez.
    Es la misma ley del cero honesto aplicada a la cobertura: una afirmacion de
    completitud sale del dato que la sostiene, o no sale.
    """
    cob = (EMB or {}).get("_cobertura") or {}
    uni, con = cob.get("universo"), cob.get("con_campos")
    if uni and con is not None and con < uni:
        return (f"Son **{miles(uni)}** contactos en el espacio y de **{miles(con)}** se "
                f"pudieron leer los campos: **{miles(uni - con)} quedaron sin mirar** y "
                f"cuentan como sin clasificar, no como vacios.")
    if uni and con is not None:
        return f"Son **{miles(uni)}** contactos y se leyeron los **{miles(con)}**, sin huecos."
    return ("**No se declaro la cobertura del universo**, asi que este informe no afirma "
            "si estan todos los contactos o solo una parte.")


def cargar(ruta, que):
    """Nunca devuelve un vacio mudo: o el dato, o por que no esta."""
    if not ruta:
        return None, f"no se paso {que}"
    if not os.path.exists(ruta):
        return None, f"no existe {ruta}"
    try:
        return leer_json(ruta), None
    except Exception as e:
        return None, f"{que} ilegible: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--decisiones", required=True)
    ap.add_argument("--pdf", metavar="RUTA",
                    help="genera tambien el PDF con golden-pdf-check. El informe SIEMPRE se "
                         "entrega en PDF, con el nombre del chat que corre la tienda.")
    ap.add_argument("--embudo")
    ap.add_argument("--analisis")
    ap.add_argument("--acciones", help="el informe diario ya generado, se incrusta como parte 2")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--empresa", default=None)
    ap.add_argument("--fecha", required=True)
    a = ap.parse_args()

    cfg = leer_json(a.config)
    avisar_banderas(cfg, a.config)
    empresa = a.empresa or cfg.get("tienda") or "la empresa"
    DEC, err_dec = cargar(a.decisiones, "las decisiones")
    if DEC is None:
        sys.exit(f"sin decisiones no hay informe: {err_dec}")
    EMB, err_emb = cargar(a.embudo, "el embudo")
    ANA, err_ana = cargar(a.analisis, "el analisis de conversaciones")

    # B10: la FORMA se valida en TODOS los insumos, no solo en uno. Un archivo
    # presente con otra estructura es tan inservible como uno ausente, y reventar a
    # mitad del informe es la peor de las dos maneras de fallar. Se valida DESPUES de
    # cargarlos todos: la primera version validaba antes de cargar y no miraba nada.
    def forma(valor, err, nombre, exige, productor):
        if valor is None:
            return None, err
        ok = isinstance(valor, dict) and all(k in valor for k in exige)
        if not ok:
            return None, (f"el archivo de {nombre} no tiene la forma que este informe "
                          f"espera (le falta {', '.join(exige)}). Lo produce {productor}")
        return valor, err

    EMB, err_emb = forma(EMB, err_emb, "el embudo", ["etapas"], "scripts/embudo_chatea.py")
    ANA, err_ana = forma(ANA, err_ana, "los motivos", ["quien_habla_de_ultimo"],
                         "scripts/analizar_conversaciones.py")
    if not isinstance(DEC, (list, dict)):
        sys.exit("sin decisiones no hay informe: el archivo no es una lista ni un objeto. "
                 "Lo produce scripts/decidir_transportadora.py")

    D = leer_json(cfg["dropi"])
    if D.get("cosecha_completa") is not True:
        sys.exit("COSECHA NO CONFIABLE: el volcado no dice cosecha_completa=true.")
    ordenes = D["ordenes"]
    acc = [o for o in ordenes if o.get("status") in cfg["estados_accionables"]]

    L = []
    A = L.append

    A("---")
    A(f"title: {empresa} · informe 360 de la operacion")
    A(f"subtitle: {a.fecha} · el asistente de WhatsApp y la logistica, en un solo documento")
    A("kicker: Comunidad Golden · Logistica diaria")
    A("author: Golden Group")
    A("---")
    A("")

    # ------------------------------------------------------------------ RESUMEN
    # B3: LA LISTA ESTRELLA VA PRIMERA. El contrato lo dice dos veces y estaba cuarta.
    # Si el cliente escribio de ultimo, el que se fue no fue el cliente: fue la empresa.
    # Es lo unico del informe que se enfria por horas, asi que abre el documento.
    _cal = (ANA or {}).get("calientes", [])
    if _cal:
        # ANCLA UNICA, INVISIBLE EN EL PDF. La comprobacion se anclaba a la frase
        # "Responder hoy", que aparece TAMBIEN en el titular verde del dia bueno: la
        # etiqueta escudaba al chequeo y lo daba por bueno sin mirar el dato. Es la
        # clase de la identidad debil un nivel arriba — **una comprobacion anclada a
        # una cadena corta y repetida se satisface por casualidad**. Un ancla que no
        # existe en ningun otro sitio no se puede satisfacer por accidente.
        A(f"## {ROJO} Responder hoy · {len(_cal)} clientes dejados esperando")
        A("")
        A("Escribieron de ultimos y nadie contesto. **El que se fue no fue el cliente.**")
        A("Ordenados por lo mas reciente.")
        A("")
        # EL CANAL VA EN LA TABLA, NO SOLO EN EL JSON.
        # Este arreglo ya existia y se quedaba en el archivo: la columna de WhatsApp
        # imprimia "| 57 |" pelado para los tres que son comentarios de Facebook y no
        # tienen telefono. Una fila que dice "llama a este numero" cuando no hay numero
        # se queda sin hacer y nadie se entera. La accion la manda el canal.
        A("| Como responder | Cliente | Ciudad | Lo ultimo que escribio | Cuando |")
        A("| --- | --- | --- | --- | --- |")
        _visC, _notaC = recortar(_cal, 30)
        for e in _visC:
            # UNA FILA QUE PIDE UNA ACCION NO SE TRUNCA A MITAD DE LA ACCION.
            # El aviso del mensaje sin texto termina en "HAY QUE ABRIR LA CONVERSACION
            # EN CHATEA" y el corte a 60 se comia justo esa parte: quedaba una fila que
            # describe un problema y no dice que hacer. Si es el aviso, va entero y corto.
            _t = (e.get("ultimo_texto") or "").replace("|", "/").replace("\n", " ")
            txt = ("**mando un audio o una imagen** · ABRIR LA CONVERSACION EN CHATEA"
                   if e.get("sin_texto") else _t[:60])
            solo_boton = e.get("solo_toco_el_boton")
            donde = (contacto_de(e) if e.get("canal") == "whatsapp"
                     else "**comentario publico** · responder en el anuncio")
            A(f"| {donde} | {(e['nombre'] or '')[:14]} | {(e['ciudad'] or '-')[:11]} | "
              f"{txt or ('(solo toco el boton del anuncio)' if solo_boton else '')} | "
              f"{str(e.get('ult'))[:10]} |")
        if len(_cal) > 30:
            A("")
            A(_notaC)
        A("")
        _canal = (ANA or {}).get("calientes_por_canal") or {}
        _pub = _canal.get("comentario_publico") or 0
        if _pub:
            A(f"**{_pub} de estos {len(_cal)} no tienen telefono**: son comentarios "
              f"publicos de Facebook o Instagram. A esos no se les puede llamar, y "
              f"**urgen mas**: un mensaje sin responder lo lee una persona, un comentario "
              f"sin responder debajo de un anuncio vivo lo lee todo el que llegue al "
              f"anuncio.")
            A("")
        # DOS CIFRAS DE "SIN TELEFONO" EN EL MISMO DOCUMENTO, DE DOS UNIVERSOS.
        # Esta sale del recorte analizado (84) y mas abajo hay otra del universo
        # completo (94). Las dos son ciertas y juntas parecen un error de alguien.
        # Cada numero lleva pegado de donde sale; si no cabe su universo, no se imprime.
        _sin_tel = (ANA or {}).get("contactos_sin_telefono")
        _uni_ana = (ANA or {}).get("universo")
        if _sin_tel and _uni_ana:
            A(f"De las **{miles(_uni_ana)}** conversaciones analizadas, **{miles(_sin_tel)}** "
              f"contactos sin telefono, por la misma razon. *(Mas abajo aparece otra cifra "
              f"de sin-telefono: esa es sobre el universo completo del espacio, no sobre "
              f"este recorte.)*")
            A("")
        if any(e.get("sin_texto") for e in _cal):
            _n = sum(1 for e in _cal if e.get("sin_texto"))
            A(f"**{concuerda(_n, 'de estas filas no tiene', 'de estas filas no tienen')} "
              f"texto que mostrar.** El cliente mando algo "
              f"que no es texto — casi seguro una nota de voz o una imagen — y el barrido "
              f"no guarda el tipo de mensaje. **Hay que abrir esa conversacion en Chatea**: "
              f"un audio sin escuchar es la fila mas caliente de esta tabla, no la mas "
              f"vacia.")
            A("")
    elif ANA is not None:
        # EL DIA BUENO NO PUEDE PARECERSE AL DIA QUE NO SE MIRO.
        # La seccion DESAPARECIA cuando no habia nadie esperando, asi que el mejor dia
        # del mes se veia igual que un dia sin datos. Es la ley del cero honesto, que
        # esta skill aplica en las tablas y no aplicaba en su seccion mas importante.
        A(f"## {VERDE} Responder hoy · nadie quedo esperando")
        A("")
        A(f"**Nadie quedo esperando respuesta.** Se revisaron las "
          f"{miles_seguro(ANA.get('universo')) if ANA.get('universo') is not None else '???'} conversaciones sin compra y en todas hablo "
          f"de ultimo el bot: no hay ninguna pregunta sin contestar. Es un cero medido, "
          f"no una seccion que falta.")
        A("")
        _st = ANA.get("contactos_sin_telefono")
        if _st == 0:
            A("Ademas, todos los contactos analizados tienen telefono, asi que no hay "
              "comentarios publicos pendientes de responder.")
            A("")
    elif ANA is None:
        A(f"## {ROJO} Responder hoy · no se pudo saber")
        A("")
        A(f"**{err_ana}.** No se afirma que no haya nadie esperando: no se miro.")
        A("")

    A("## Lo que hay que hacer hoy, en una hoja")
    A("")
    calientes = len(ANA.get("calientes", [])) if ANA else None
    fuga = EMB.get("fuga") if EMB else None
    A("| | Cuanto | Que es | Que hago |")
    A("| --- | --- | --- | --- |")
    if calientes is not None:
        A(f"| {ROJO} | **{calientes}** | clientes que escribieron y **nadie les respondio** | "
          f"contestar hoy: es la plata mas barata de recuperar |")
    else:
        A(f"| {ROJO} | ? | no se pudo leer las conversaciones | {err_ana} |")
    if fuga is not None:
        A(f"| {ROJO} | **{fuga}** | dieron todos los datos y **no hay orden en Dropi** | subirlos |")
    else:
        A(f"| {ROJO} | ? | no se pudo medir la fuga | {err_emb} |")
    A(f"| {ROJO} | **{len(acc)}** | pedidos vivos en Dropi | la parte 2 dice uno por uno que hacer |")
    # Un pedido SIN total no vendio cero: no se sabe cuanto vendio. Sumarlo como 0
    # baja el total y lo presenta como medido. Se suma lo que hay y se declara el resto.
    _con_total = [o for o in acc if o.get("total") not in (None, "")]
    _sin_total = len(acc) - len(_con_total)
    _con_gan = [o for o in acc if o.get("ganancia") not in (None, "")]
    _cola = pesos(sum(float(o["total"]) for o in _con_total))
    _util = pesos(sum(float(o["ganancia"]) for o in _con_gan))
    A(f"| {AMARILLO} | **{_cola}** | vendido en la cola viva"
      + (f" (de {len(_con_total)} de {len(acc)} pedidos: a {_sin_total} no se les leyo el "
         f"valor)" if _sin_total else "")
      + f" | {_util} de utilidad si todo entrega"
      + (f", sobre {len(_con_gan)} de {len(acc)}" if len(_con_gan) != len(acc) else "")
      + " |")
    A("")
    A(f"En orden de plata: **responder a quien pregunto** cuesta un mensaje y ya esta vendido a medias; "
      f"**subir a Dropi lo que ya se vendio** cuesta cinco minutos; **arreglar una transportadora** "
      f"cuesta un clic mientras no haya guia.")
    A("")

    # ------------------------------------------------------------------
    # PASO 1 · LAS GUIAS YA GENERADAS. Dictado por FER el 2026-08-11.
    #
    # No es una seccion mas: es la unica que caduca hoy. Mientras el paquete no salga
    # de la bodega, una guia mal puesta todavia se cambia sola; en cuanto sale, lo
    # unico que queda es llamar y pedir el favor. Por eso va ANTES de la parte 1, que
    # es la que mas se lee, y por eso trae la plata al lado: una seccion que pide
    # trabajo sin decir cuanto vale se pospone hasta que deja de servir.
    # ------------------------------------------------------------------
    _lista_dec = DEC if isinstance(DEC, list) else (DEC.get("decisiones") or [])
    con_guia, _plata = guias_por_corregir(
        _lista_dec, (cfg.get("estados") or {}).get("ya_no_se_reasigna"))
    if con_guia:
        A(f"## {ROJO} Paso 1 · Guias ya generadas que hay que corregir · {len(con_guia)}"
          + (f" · {pesos(_plata)} en juego" if _plata else ""))
        A("")
        A("Esto va primero porque es lo unico que caduca hoy: **mientras el paquete no "
          "salga de la bodega, la guia todavia se cambia**. Manana ya no se cambia, se "
          "llama a pedir el favor.")
        A("")
        A("| Por que | WhatsApp | Cliente | Ciudad | Va por | Pasar a |")
        A("| --- | --- | --- | --- | --- | --- |")
        for d in con_guia:   # ya viene ordenado por valor
            e = d.get("elegida")
            A(f"| {causa_de_guia(d)} | {contacto_de(d)} | "
              f"{(d.get('cliente') or '')[:18]} | {(d.get('ciudad') or '')[:14]} | "
              f"{d.get('actual') or 'ninguna'} | **{e['t'] if e else 'decides tu'}** |")
        A("")

    # POR QUE EL IDENTIFICADOR ES EL TELEFONO Y NO EL NUMERO DE PEDIDO.
    # Lo dicto FER, y la razon va IMPRESA porque sin ella el cambio se revierte por
    # comodidad la primera vez que alguien eche de menos la columna.
    A("> **El identificador de cada fila es el WhatsApp, no el numero de pedido.** Dropi "
      "le cambia el numero al pedido cuando se edita, asi que un informe que pide "
      "corregir un pedido y lo nombra por su numero **se invalida a si mismo en cuanto "
      "lo obedeces**: corriges, el numero cambia, y la fila ya no apunta a nada. El "
      "telefono no cambia nunca y ademas es con lo que se busca en Dropi y en WhatsApp.")
    A("")

    # ------------------------------------------------- PARTE 1 · EL ASISTENTE
    # B4/B5: LA COBERTURA VIAJA CON EL DATO. Antes el informe decia "son TODOS los
    # contactos, no una muestra" mientras el insumo declaraba 218 nunca leidos. El
    # titular sale de una variable que lo prueba, o no se dice.
    cob = (EMB or {}).get("_cobertura") or {}
    universo = cob.get("universo")
    con_campos = cob.get("con_campos")
    sin_campos = cob.get("sin_campos") or 0
    if universo and con_campos is not None:
        completo = (sin_campos == 0)
        frase_cob = (f"Son **los {universo} contactos** del espacio, no una muestra."
                     if completo else
                     f"De **{universo} contactos**, se leyeron los campos de **{con_campos}**. "
                     f"Los otros **{sin_campos} no se leyeron** y caen en «sin etapa» por eso, "
                     f"no porque no tengan etapa.")
    else:
        completo = False
        frase_cob = ("**El insumo no declara su cobertura**, asi que no se puede decir sobre "
                     "cuantos contactos habla esta parte.")

    A("## Parte 1 · El asistente de WhatsApp")
    A("")
    A(frase_cob)
    A("")
    if EMB is None:
        A(f"**Esta parte no se pudo construir:** {err_emb}. No se afirma nada sobre el embudo.")
        A("")
    else:
        # CADA CIFRA SE ATA A SU UNIVERSO, EN SU PROPIA FRASE.
        # El titular decia "El universo: 857" y dos lineas despues "Son 900 contactos".
        # Son los dos ciertos y hablan de cosas distintas: 900 es el espacio, 857 el
        # denominador tras excluir la integracion. Una resta cuyo minuendo esta en otro
        # parrafo es una resta que el lector no puede comprobar.
        tot = EMB["pedidos"]
        A(f"### El denominador: {miles(tot)} contactos que si pasaron por el bot")
        A("")
        # LOS DOS NUMEROS DE ESTA FRASE SALIERON FALSOS Y POR LA MISMA CAUSA:
        # MEZCLAR DOS UNIVERSOS EN UNA RESTA. Aqui se restaba `ANA['no_compradores']`
        # a los pedidos del embudo. Pero cuando el analisis corre sobre un RECORTE, ese
        # numero es el tamaño del recorte, no el de los no compradores reales: daba
        # «157 llegaron a ser pedido» cuando eran 94. El arreglo y su diagnostico son
        # de LOGISTICA DOLCE (scripts/dolce/informe_360.py:151), adoptados con credito:
        # LOS QUE COMPRARON SALEN DEL EMBUDO, que si mira el universo entero.
        #
        # Y la frase abria con "son TODOS los contactos, no una muestra" en literal,
        # afirmando completitud tres clausulas antes de negarla razonadamente. Una
        # afirmacion de cobertura no se escribe a mano: sale de la variable o no sale.
        _compraron = (ANA or {}).get("compradores_universo")
        _uni = (ANA or {}).get("universo_completo")
        # "De ellos" necesita un antecedente. Si la cobertura no se declaro, la frase
        # anterior no da un numero al que referirse y la continuacion queda coja.
        _hay_universo = bool(((EMB or {}).get("_cobertura") or {}).get("universo"))
        _enlace = " De ellos, " if _hay_universo else " De la lista completa, "
        A(_cob_universo(EMB) +
          (f"{_enlace}**{miles(_compraron)} llegaron a ser pedido en Dropi**"
           if _compraron is not None else ""))
        if ANA:
            # LA FRASE NO PUEDE EMPEZAR POR "y" SI LA ANTERIOR NO SE IMPRIMIO.
            # Sin `--contactos-universo` la primera clausula no sale y quedaba
            # "y 743 de los analizados no compraron", colgando de nada.
            _liga = "y " if _compraron is not None else ""
            # LA CONVERSION SE MIDE SOBRE EL UNIVERSO COMPLETO, NUNCA SOBRE EL RECORTE.
            # Sobre el recorte da 0% por construccion — no hay un solo comprador dentro —
            # y publicar ese 0 es decirle al dueño que su bot no vende nada. Antes se
            # imprimia el 0; despues se nego a imprimir nada; lo correcto es lo tercero:
            # imprimir el numero VERDADERO, medido cruzando la lista COMPLETA contra
            # Dropi. Ese cruce no lo puede hacer el embudo ni la resta: hay que traer
            # la lista completa a proposito, y si no vino, no se publica.
            if _compraron is not None and _uni:
                A(f"{_liga}**{miles(_uni - _compraron)} de esos {miles(_uni)} no compraron**. "
                  f"La conversion de la cuenta es "
                  f"**{ANA['conversion_universo_pct']:.2f}%**, medida sobre los "
                  f"{miles(_uni)} contactos de la lista completa.")
                # EN ESTA SECCION HAY TRES NUMEROS DISTINTOS PARA "EL UNIVERSO" Y HAY
                # QUE EXPLICARLOS EN EL PAPEL. Antes esta explicacion estaba gateada por
                # un campo que en la corrida real venia en None, asi que el dia que mas
                # falta hacia era justo el dia que no salia. Ahora sale siempre: si un
                # numero no se sabe, se dice que no se sabe, que es la otra mitad.
                _d = ANA.get("conversion_detalle") or {}
                _cob_uni = ((EMB or {}).get("_cobertura") or {}).get("universo")
                A("")
                A("**Los numeros de universo de esta pagina no son el mismo, a proposito:**")
                A("")
                A("| Cifra | Cuanto | Que es |")
                A("| --- | --- | --- |")
                A(f"| Contactos en el espacio | {miles(_d.get('universo_bruto'))} | "
                  f"todo lo que hay en Chatea, sin filtrar |")
                A(f"| Menos los de la integracion | −{miles(_d.get('excluidos_integracion'))} | "
                  f"los crea Dropi DESPUES de una compra: nunca pasaron por el bot, asi que "
                  f"no pueden contar como embudo |")
                A(f"| **Denominador de la conversion** | **{miles(_d.get('denominador'))}** | "
                  f"los que si tuvieron la oportunidad de comprar por el bot |")
                if _cob_uni is not None and _d.get("universo_bruto") is not None \
                        and _cob_uni != _d["universo_bruto"]:
                    A(f"| Lo que conto el embudo | {miles(_cob_uni)} | otra bajada, de otra "
                      f"hora: el espacio cambia solo. Ninguna esta mal, no son de la misma "
                      f"foto |")
                elif _cob_uni is None:
                    A("| Lo que conto el embudo | no declarado | el embudo no dijo su "
                      "universo, asi que no se puede contrastar |")
                A("")
                if _d.get("sin_telefono"):
                    # PARRAFO PARTIDO A PROPOSITO. Era el bloque mas largo del informe
                    # (392 caracteres) y es el que empuja la paginacion: la auditoria de
                    # golden-pdf-check lo dejo a 1,3mm del borde. Partir por sentido —no
                    # por longitud— es la decision de contenido que manda esa skill.
                    A(f"**Y un sesgo que hay que saber para leer ese porcentaje:** "
                      f"{miles(_d['sin_telefono'])} de los {miles(_d.get('denominador'))} "
                      f"contactos **no tienen telefono**: son comentarios de Facebook e "
                      f"Instagram.")
                    A("")
                    A("El cruce contra Dropi es por telefono, asi que esos **no pueden "
                      "aparecer como compradores ni aunque compren**, y la conversion "
                      "queda sesgada hacia abajo. Se declara y no se corrige: que hacer "
                      "con ellos es una decision del negocio, no del calculo.")
                    A("")
                if _d.get("personas_distintas") is not None and \
                        _d["personas_distintas"] != _d.get("compradores"):
                    A(f"Los {miles(_d['compradores'])} compradores son "
                      f"**{miles(_d['personas_distintas'])} personas**: hay telefonos "
                      f"repetidos. Se cuenta por CONTACTO, que es la unidad del embudo "
                      f"(cada contacto es una conversacion).")
                    A("")
                if not ANA.get("conversion_pct_se_puede_leer"):
                    A("")
                    A(f"El analisis de por que no compraron corre sobre "
                      f"**{miles(ANA['universo'])}** de ellos — los que no compraron y "
                      f"hablaron en las ultimas dos semanas — porque para eso, quien "
                      f"compro no aporta y quien no habla hace un mes no es accionable "
                      f"hoy. Es un subconjunto **elegido**, no un hueco.")
            elif ANA.get("conversion_pct_se_puede_leer"):
                A(f"{_liga}**{miles(ANA['no_compradores'])} no compraron**. "
                  f"La conversion de la cuenta es **{ANA['conversion_pct']}%**.")
            else:
                A(f"{_liga}**{miles(ANA['no_compradores'])} de los analizados no compraron**. "
                  "**La conversion de la cuenta no se publica**: el analisis corrio sobre "
                  "el recorte de no compradores, donde da cero por construccion, y no se "
                  "entrego la lista completa del espacio para medirla de verdad "
                  "(`--contactos-universo`). No se estima.")
        A("")
        A("### Donde esta parada la gente")
        A("")
        A("| Etapa del embudo | Contactos | De hoy |")
        A("| --- | --- | --- |")
        hoy = EMB.get("hoy_etapas", {})
        orden = ["Contacto inicial 🔵", "Interacción con IA 🤖", "Cliente potencial 🚨",
                 "Pedido Confirmado 🟩", "REVISADOS ✅", "(sin Tablero)"]
        for k in orden:
            if k in EMB["etapas"]:
                A(f"| {k} | {miles(EMB['etapas'][k])} | {hoy.get(k, 0)} |")
        otros = {k: v for k, v in EMB["etapas"].items() if k not in orden}
        if otros:
            A(f"| Estados logisticos (ya son pedido) | {miles(sum(otros.values()))} | "
              f"{sum(v for k, v in hoy.items() if k not in orden)} |")
        A("")
        A(f"**Hoy entraron {sum(hoy.values())} contactos nuevos.** Los que aparecen en "
          f"«Contacto inicial» son los que vio el anuncio, abrio WhatsApp y no siguio: "
          f"esa cifra es la que mide si el primer mensaje del bot engancha.")
        A("")

    if ANA is None:
        A(f"### Por que no compraron")
        A("")
        A(f"**No se pudo responder:** {err_ana}. No se reparten motivos inventados.")
        A("")
    else:
        A("### Por que no compraron · los " + miles(ANA["no_compradores"]) + " que no llegaron a pedido")
        A("")
        A("Cada contacto cae en un motivo **porque hay una senal en su conversacion**. "
          "El motivo se lee de lo que escribio **el cliente**, nunca de lo que dijo el bot: "
          "el bot habla de precio y de envio en todos los chats, y buscarlo ahi clasificaria "
          "a todo el mundo igual. Los que no dan senal quedan como tales y se cuentan.")
        A("")
        # El ancla lleva el CONTEO: asi la comprobacion puede probar que la coleccion
        # llego al papel entera, no solo que la seccion existe.
        A("| Motivo | Contactos | Que significa |")
        A("| --- | --- | --- |")
        # LA GLOSA SE QUEDO VIEJA CUANDO CAMBIARON LOS CUBOS, y una tabla con la columna
        # "que significa" en blanco es peor que no tenerla: el lector cree que ese cubo
        # no tiene explicacion, no que a nadie se le olvido escribirla. Habia cuatro
        # filas vacias y dos entradas muertas — una de ellas la del cubo que enterramos.
        # Por eso ahora no basta con el diccionario: la compuerta de abajo exige que
        # TODO cubo que se imprima tenga glosa.
        GLOSA = {
            "LA PELOTA LA TIENE LA EMPRESA: el cliente escribio de ultimo y nadie respondio":
                "**venta a medio cerrar**: preguntaron y se quedaron esperando",
            "Nunca escribio: entro y no dijo nada":
                "abrio el chat desde el anuncio y no llego a escribir",
            "Escribio una sola vez y no volvio":
                "un mensaje y silencio: el enganche del bot no agarro",
            "Solo el clic del anuncio: nunca escribio nada suyo":
                "solo toco el boton: **no hay a quien llamar**, todo lo que 'dijo' lo puso Meta",
            "Se cayo en la direccion: dio la ciudad y falto la direccion":
                "**el mas recuperable**: iba comprando y le falta UN dato",
            "Dio todos los datos y no hay pedido":
                "dio todo y la orden no existe en Dropi: **revisar si se cayo al subirla**",
            "Converso y nunca llego a dar la ubicacion":
                "hubo dialogo real y nunca solto donde vive",
        }
        # LOS CUBOS DE CEGUERA LLEVAN GLOSA POR CONSTRUCCION, NO POR LISTA.
        #
        # ESTE FUE EL PEOR FALLO DE TODO EL EXPEDIENTE, y era de diseño: con un barrido
        # incompleto — que es el modo de operacion DIARIO de esta skill, por incremental —
        # el analisis emite el cubo "NO SE PUDO MIRAR: no se bajo la conversacion". Ese
        # cubo era el unico sin glosa en la lista, asi que la compuerta MATABA el informe.
        # O sea: **el sistema construido para declarar ceguera se caia justo cuando
        # aparecia ceguera**, y el dia degradado es exactamente el dia en que el informe
        # mas falta hace. Corria solo porque tres contadores valian cero.
        #
        # La leccion general: una compuerta que se dispara con un valor que CRECE en el
        # escenario degradado no protege el informe, lo secuestra. Aqui la glosa se
        # DERIVA del nombre del cubo, asi que un cubo de ceguera nuevo nace explicado.
        def _glosa_de(m):
            if m in GLOSA:
                return GLOSA[m]
            if m.startswith("Objecion"):
                return "objecion dicha por el cliente"
            if m.startswith("NO SE PUDO MIRAR"):
                return ("**no es un motivo, es un hueco**: de estos contactos no se sabe "
                        "por que no compraron porque no se pudo leer su conversacion")
            return ""

        _sin_glosa = []
        for m, n in ANA["motivos"].items():
            g = _glosa_de(m)
            if not g:
                _sin_glosa.append(m)
            A(f"| {m} | **{n}** | {g} |")
        if _sin_glosa:
            # Y AUN ASI NO SE MATA EL INFORME. Un cubo sin explicar es un defecto de
            # documentacion; no publicar el informe del dia es un defecto de operacion,
            # y es mucho mas caro. Se imprime el aviso EN EL PAPEL — donde lo ve quien
            # puede arreglarlo — y el informe sale.
            A("")
            A(f"> ⚠️ **Estos motivos salen sin explicar y hay que documentarlos en la "
              f"skill:** {' · '.join(_sin_glosa)}. El informe se publica igual: una "
              f"columna sin glosa es un defecto de esta documentacion, no una razon para "
              f"dejar a la operacion sin su informe del dia.")
        A("")
        qc = ANA.get("quien_habla_de_ultimo", {})
        if qc:
            A(f"**Quien hablo de ultimo** en los chats sin compra: el cliente en "
              f"**{qc['cliente'] if 'cliente' in qc else 'no medido'}** y el bot en "
              f"**{qc['bot'] if 'bot' in qc else 'no medido'}** "
              f"(de {miles(sum(v for v in qc.values() if isinstance(v, int)))} "
              f"conversaciones con algun mensaje; las demas del universo entraron y "
              f"nadie escribio nunca). "
              f"Solo en los segundos se puede decir que el cliente se fue; en los primeros "
              f"el que se fue fue el negocio.")
            A("")

    if EMB and EMB.get("lista"):
        A(f"### {ROJO} Vendido y sin orden · {EMB['fuga']}")
        A("")
        A("Dieron producto, ciudad y direccion completa, y **no existe la orden en Dropi**. "
          "Se comprobo contra las " + miles(len(ordenes)) + " ordenes de la cuenta, por telefono.")
        A("")
        A("| WhatsApp | Cliente | Ciudad | Pidio | Ultima vez |")
        A("| --- | --- | --- | --- | --- |")
        _visF, _notaF = recortar(EMB["lista"], 25)
        for e in _visF:
            A(f"| {contacto_de(e)} | {(e.get('nombre') or '')[:14]} | {(e.get('ciudad') or '-')[:11]} | "
              f"{(e.get('productos') or '')[:26]} | {str(e.get('ult'))[:10]} |")
        if len(EMB["lista"]) > 25:
            A("")
            A(_notaF)
        A("")

    if EMB and EMB.get("potenciales"):
        A(f"### {AMARILLO} Clientes potenciales sin cerrar · {len(EMB['potenciales'])}")
        A("")
        A("El bot ya los marco como interesados reales y se frenaron antes de dar los datos.")
        A("")
        A("| WhatsApp | Cliente | Ciudad | Le interesa | Ultima vez |")
        A("| --- | --- | --- | --- | --- |")
        _vis, _nota = recortar(EMB["potenciales"], 20)
        for e in _vis:
            A(f"| {contacto_de(e)} | {(e.get('nombre') or '')[:14]} | {(e.get('ciudad') or '-')[:11]} | "
              f"{(e.get('productos') or '')[:26]} | {str(e.get('ult'))[:16]} |")
        if _nota:
            A(_nota)
        A("")

    # ------------------------------------------------- PARTE 2 · LA LOGISTICA
    A("## Parte 2 · La logistica")
    A("")
    A(f"### Como se comporta cada transportadora en esta cuenta")
    A("")
    A("Medido sobre los pedidos **cerrados** de la cuenta (entregado o devuelto). "
      "Un pedido en camino todavia no fracaso, asi que no entra al denominador: "
      "meterlo pinta de rojo a la transportadora que acaba de recibir carga.")
    A("")
    cer = {"ENTREGADO", "DEVOLUCION", "DEVOLUCION EN BODEGA", "RECHAZADO", "SINIESTRO"}
    per = {}
    for o in ordenes:
        c = o.get("carrier") or "?"
        if o.get("status") not in cer:
            continue
        d = per.setdefault(c, {"ent": 0, "tot": 0})
        d["tot"] += 1
        if o["status"] == "ENTREGADO":
            d["ent"] += 1
    A("| Transportadora | Cerrados | Entrega | La bodega la despacha |")
    A("| --- | --- | --- | --- |")
    oper = set(cfg["operativas"])
    for c, d in sorted(per.items(), key=lambda kv: -kv[1]["tot"]):
        if d["tot"] < 20:
            continue
        marca = "si" if c in oper else "**NO**"
        A(f"| {c} | {miles(d['tot'])} | **{100*d['ent']/d['tot']:.1f}%** | {marca} |")
    A("")
    chicas = [c for c, d in per.items() if d["tot"] < 20]
    if chicas:
        A(f"Se omiten {len(chicas)} transportadoras con menos de 20 cerrados "
          f"({', '.join(sorted(chicas)[:6])}): con esa muestra el porcentaje no dice nada.")
        A("")
    A("**Ojo con leer esta tabla como un ranking.** Es el promedio de la cuenta, y cada "
      "transportadora lleva una mezcla distinta de ciudades: la que mas pueblos lejanos "
      "carga sale peor sin ser peor. La decision pedido por pedido se toma **por municipio**, "
      "que es lo que hace la tabla siguiente.")
    A("")

    # decisiones: donde se gana plata cambiando
    lista_dec = DEC if isinstance(DEC, list) else DEC.get("decisiones", [])
    cambios = [d for d in lista_dec if isinstance(d, dict) and d.get("rec") == "CAMBIAR"]
    # LO QUE NO ES "CAMBIAR" TAMBIEN ES UNA DECISION. Esta version solo imprimia los
    # cambios: sin cobertura, sin transportadora asignada y los que el motor no
    # devolvio desaparecian del papel. Es el mismo bloqueante que costo dos rondas
    # en el generador anterior, reaparecido en el archivo nuevo.
    sin_cob = [d for d in lista_dec if isinstance(d, dict) and d.get("rec") == "SIN COBERTURA"]
    asignar = [d for d in lista_dec if isinstance(d, dict) and d.get("rec") == "ASIGNAR"]
    otros = [d for d in lista_dec if isinstance(d, dict)
             and d.get("rec") not in ("CAMBIAR", "DEJAR", "SIN COBERTURA", "ASIGNAR")]
    rendido = set()
    crit = Counter(d.get("criterio") for d in lista_dec if isinstance(d, dict))
    A(f"### La decision de hoy, pedido por pedido")
    A("")
    # Partido por sentido: que se miro / que se ignoro. Eran 379 caracteres de un tiron
    # y este es uno de los bloques que empujaban la paginacion contra el borde.
    A(f"El motor volvio a cotizar **las {len(acc)}** ordenes vivas desde cero: precio de "
      f"todas las transportadoras que llegan a ese municipio, cuanto entrega cada una "
      f"**en ese municipio** segun la Torre de Dropi, y el costo real de cada opcion "
      f"(flete mas lo que cuesta la devolucion cuando no entrega).")
    A("")
    # CONTRA QUE TORRE SE DECIDIO, IMPRESO. El 2026-08-16 el factor de calibracion de
    # Golden paso de 0,92 a 1,00 en un dia **sin que nadie tocara un pedido**: la rutina
    # de la Torre habia cambiado su ventana. Decir «segun la Torre» sin decir cual es
    # pedirle al lector que defienda un numero que se mueve solo por debajo.
    _t0 = next((d for d in lista_dec if isinstance(d, dict) and d.get("torre_generado")), None)
    if _t0:
        _linea = (f"Los porcentajes de entrega salen de la Torre de Dropi **generada el "
                  f"{_t0['torre_generado']}**")
        if _t0.get("torre_rango"):
            _linea += f", sobre la ventana **{_t0['torre_rango']}**"
        A(_linea + ". Si esa ventana cambia, los porcentajes cambian aunque los pedidos "
                   "sean los mismos.")
        if _t0.get("torre_nota"):
            A("")
            A(f"> {_t0['torre_nota']}")
    else:
        A("**Este informe no puede decir de que Torre salieron los porcentajes**: las "
          "decisiones no traen su fecha. Se decidio con la que hubiera en disco.")
    A("")

    # EL CRUCE CONTRA LAS OFICINAS DE INTERRAPIDISIMO, y su ausencia tambien se dice.
    # No poder cruzar y cruzar sin encontrar nada se leen igual en el papel si nadie
    # los separa — y son cosas opuestas.
    _cru = [d for d in lista_dec if isinstance(d, dict) and d.get("cruce_oficina")
            in ("igual", "parecida")]
    _hay_listado = next((d for d in lista_dec if isinstance(d, dict)
                         and d.get("oficinas_fecha")), None)
    if _hay_listado:
        _ig = [d for d in _cru if d["cruce_oficina"] == "igual"]
        _pa = [d for d in _cru if d["cruce_oficina"] == "parecida"]
        A(f"**Direcciones que resultaron ser la oficina de Interrapidisimo: {len(_ig)}.** "
          "Son clientes que se saben la direccion de memoria y la escriben pelada, sin "
          "decir «oficina». A esos **no se les cambia la transportadora**: el punto donde "
          "los mandaron a recoger deja de existir si se cambia, y el paquete se devuelve."
          + f" Se cruzo contra el listado de **{_hay_listado['oficinas_total']} oficinas** "
            f"cosechado el **{_hay_listado['oficinas_fecha']}**."
          + (f" Otras **{len(_pa)} se parecen** y quedan marcadas para que alguien las "
             "confirme con el cliente: un «casi» no se decide solo." if _pa else ""))
        A("")
    else:
        A("**No se cruzo contra el listado de oficinas de Interrapidisimo**: el config no "
          "lo trae. Eso no quiere decir que ningun cliente haya puesto la direccion de "
          "una oficina — quiere decir que no se miro.")
        A("")
    A("La seleccion que Dropi trae puesta se ignora a proposito: es automatica y puede "
      "estar vieja.")
    A("")
    A(f"Resultado: **{len(cambios)} pedidos conviene moverlos** y el resto esta bien como esta.")
    A("")
    _av = aviso_default_bodega(cfg)
    if _av:
        A(_av)
        A("")
    A("| Como se decidio | Pedidos | Que quiere decir |")
    A("| --- | --- | --- |")
    # LA GLOSA DE LOS CRITERIOS ES LA MISMA FAMILIA QUE LA DE LOS MOTIVOS, y tenia el
    # mismo agujero: faltaban criterios que el motor SI emite (HUELLA_MALA salia con la
    # columna en blanco). Arreglar una tabla y no su familia es como no arreglarla: el
    # lector se encuentra el hueco en la de al lado. Por eso aqui tambien hay compuerta.
    GL = {"CLARO": "una opcion gana por costo sin discusion",
          "PRECIO": "estaban empatadas en costo y mando la de menor costo esperado",
          "HUELLA_VENTAJA": "estaba apretado y desempato el historial de ese cliente",
          "HUELLA_MALA": "a la mas barata le ha ido MAL con este cliente (por debajo del "
                         "60% de sus pedidos cerrados), asi que se descarta aunque gane "
                         "en costo",
          "ASIGNAR": "el pedido salio sin transportadora y hay que ponerle una",
          "SIN DECISION": "el motor no pudo decidir: falta el dato que dice la fila",
          "SIN COBERTURA": "ninguna transportadora operativa llega alli"}
    _crit_sin_glosa = []
    for k, v in crit.most_common():
        g = GL.get(k, "")
        if not g:
            _crit_sin_glosa.append(str(k))
        A(f"| {k} | {v} | {g} |")
    if _crit_sin_glosa:
        # Mismo criterio que arriba: se avisa en el papel, no se secuestra el informe.
        A("")
        A(f"> ⚠️ **Criterios que este informe no sabe explicar y hay que documentar:** "
          f"{' · '.join(_crit_sin_glosa)}.")
    A("")
    A("**La huella del cliente casi nunca decide, y eso esta bien.** Solo entra cuando las "
      "dos mejores opciones quedan a menos de " + pesos(cfg.get("apretado", 3000)) +
      " de diferencia.")
    A("")
    A("Un cliente sin historial con una transportadora no pierde por eso: la ausencia de "
      "historial no es una mancha. Lo mas probable es que compro en otra tienda que no "
      "la usaba.")
    A("")

    # El ahorro sale de comparar el costo de la ELEGIDA contra el de la que lleva
    # puesta hoy, tomando ambos del mismo calculo (la lista de candidatas del pedido).
    # No se usa el texto del motivo: un numero que sale de una frase ya escrita no
    # es un calculo, es una cita.
    ahorro, medidos, sin_medir = 0.0, 0, 0
    for d in cambios:
        e = d.get("elegida") or {}
        actual = d.get("actual")
        cand = {c.get("t"): c for c in (d.get("cands") or []) if isinstance(c, dict)}
        hoy_c = cand.get(actual, {}).get("costo")
        if e.get("costo") is not None and hoy_c is not None:
            ahorro += max(0.0, float(hoy_c) - float(e["costo"]))
            medidos += 1
        else:
            sin_medir += 1
    if medidos:
        A(f"Aplicar los cambios vale **{pesos(ahorro)}** de costo real evitado, medido sobre "
          f"{medidos} de los {len(cambios)} pedidos a mover. No es plata que entra: es plata "
          f"que se deja de perder en fletes de ida y vuelta de lo que no se entrega.")
        if sin_medir:
            A("")
            A(f"En **{sin_medir}** de esos cambios no se pudo poner cifra, porque la "
              f"transportadora que llevan hoy no cotiza en ese municipio y no hay contra que "
              f"compararla. Se cambian igual: la razon ahi no es el precio, es que no sirve.")
        A("")

    dias = [(d.get("elegida") or {}).get("dias") for d in lista_dec]
    dias = [x for x in dias if x]
    if dias:
        A(f"El tiempo de entrega que promete la eleccion de hoy es de **{sum(dias)/len(dias):.1f} "
          f"dias** en promedio, medido sobre {len(dias)} de los {len(lista_dec)} pedidos. "
          f"En contra entrega el dia de mas no es solo espera: es tiempo para arrepentirse.")
        A("")
    else:
        # UNA PROMESA QUE DESAPARECE TIENE QUE DECIR QUE DESAPARECIO.
        #
        # Cuando la Torre dejo de traer `dias` (2026-08-16), esta frase simplemente
        # **dejo de imprimirse**. Nadie miente: es que la seccion se encoge y el lector
        # no tiene forma de distinguir «hoy no habia nada que decir» de «el insumo dejo
        # de traer el dato». El aviso existia, pero salia solo por consola con codigo 0
        # — y `2>/dev/null` lo borra. **Un aviso cierto que nadie ve equivale a no
        # tenerlo**, que es justo lo que dice el pendiente de la politica de canal.
        #
        # LA REGLA, que ya se aplico al default de bodega y al origen de la ventana:
        # una advertencia que califica el ENTREGABLE viaja DENTRO del entregable, no
        # solo al terminal de quien lo corrio.
        _con_dias = sum(1 for d in lista_dec
                        if isinstance(d, dict) and (d.get("elegida") or {}).get("dias"))
        if lista_dec and not _con_dias:
            A("**Este informe no promete tiempo de entrega.** La Torre de Dropi dejo de "
              "traer los dias por transportadora, asi que el dato no existe para "
              "ninguno de los " + miles(len(lista_dec)) + " pedidos de hoy. No es que "
              "hoy no se midiera: es que la fuente ya no lo entrega.")
            A("")

    # ------------------------------------------------- ACCIONES (informe diario)
    if a.acciones and os.path.exists(a.acciones):
        # Se lee con `leer_texto` para que quede APUNTADO: el verificador destruyo el
        # ACCIONES.md pasandolo como `--salida`, y salio con codigo 0.
        cuerpo = leer_texto(a.acciones)
        # LAS DOS CIRUGIAS DEL INCRUSTADO TAMBIEN ASEVERAN.
        # Este bloque hacia CUATRO operaciones sobre el cuerpo incrustado y solo dos
        # aseveraban que habian encontrado su objetivo — las otras dos eran `re.sub`
        # crudos. Es el mismo dos-de-cuatro que aparecio en los recortes de tablas: la
        # regla existia, estaba escrita, y se aplico donde alguien se acordo.
        #
        # QUE PASA SI FALLAN EN SILENCIO: el front matter del informe corto (su bloque
        # `---titulo---`) queda incrustado A MITAD del 360, y los `##` del corto se
        # mezclan con la jerarquia del 360 en vez de colgar de ella. Ninguna de las dos
        # cosas revienta nada: salen impresas, y solo se ven abriendo el PDF.
        cuerpo = sustituir_exigiendo(
            r"^---.*?---\n", "", cuerpo,
            "quitarle el front matter al informe corto antes de incrustarlo (si no "
            "aparece, el archivo que llego NO es el informe de acciones)", flags=re.S)
        # La bajada de nivel NO exige coincidencias: un dia sin nada que hacer trae un
        # informe corto sin secciones, y ahi no hay nada que bajar. Lo que si se exige
        # es el RESULTADO — que no sobreviva ningun `##`, porque uno solo ya rompe la
        # jerarquia del documento.
        cuerpo = re.sub(r"^## ", "### ", cuerpo, flags=re.M)
        _sobran = re.findall(r"^## ", cuerpo, flags=re.M)
        if _sobran:
            sys.exit(
                "EL INCRUSTADO CONSERVA %d ENCABEZADOS DE NIVEL 2 despues de bajarlos.\n"
                "  Colgarian del documento como hermanos de «Parte 1» y «Parte 2» en vez\n"
                "  de colgar de ellas. No se entrega un informe con la jerarquia rota."
                % len(_sobran))
        # CADA TABLA DE COBERTURA DICE DE QUE UNIVERSO HABLA.
        # El informe corto trae la suya (solo la logistica: 78 pedidos vivos) y este
        # documento tiene la suya (todo: 900 contactos). Incrustadas sin rotular
        # quedaban dos tablas contiguas con universos distintos — 857 contra 900, ciego
        # 26 contra 91 — y quien lee no puede saber que hablan de cosas distintas. Dos
        # cifras ciertas puestas juntas sin su ambito se leen como una contradiccion.
        cuerpo = sustituir_exigiendo(
            r"### Que se reviso(?! ·)",
            "### Que se reviso · SOLO la parte de logistica (viene del informe de acciones)",
            cuerpo, "rotular el ambito de la tabla de cobertura que viene del informe corto")
        # Y la seccion "Los que decides tu" existe en los dos: al incrustar quedaba dos
        # veces, con el mismo pedido recortado distinto. Se queda la del 360, que es la
        # completa.
        # El titulo REAL de esa seccion en el informe corto es «🟡 Decides tu · N».
        # El patron anterior buscaba "Los que decides tu" — el titulo del 360, no el
        # del corto — asi que no coincidia con nada y yo reporte la seccion como
        # eliminada. Ahora la sustitucion ASEVERA que encontro su objetivo.
        cuerpo = sustituir_exigiendo(
            r"\n### [^\n]*Decides tu[^\n]*\n.*?(?=\n### |\Z)", "\n", cuerpo,
            "quitar del bloque incrustado la seccion «Decides tu», que el 360 ya trae "
            "completa (si no, sale dos veces con el mismo pedido recortado distinto)",
            flags=re.S)
        # EL PASO 1 EXISTE EN LOS DOS PAPELES Y AQUI SOLO PUEDE SALIR UNA VEZ.
        # El 360 lo imprime arriba del todo, que es donde FER lo quiere; el informe
        # corto lo lleva porque tambien se entrega suelto. Al incrustar salian los dos y
        # el chequeo de secciones duplicadas lo freno — funcionando exactamente para lo
        # que existe. Se quita el del bloque incrustado, no el de arriba: mandarlo al
        # final de un documento de 365 lineas es lo contrario de llamarlo Paso 1.
        # Solo se exige la coincidencia SI el 360 imprimio el suyo: cuando no hay guias
        # que corregir no hay nada que quitar, y morir ahi seria inventar un fallo.
        if con_guia:
            cuerpo = sustituir_exigiendo(
                r"\n### [^\n]*Paso 1 · Guias ya generadas[^\n]*\n.*?(?=\n### |\Z)", "\n",
                cuerpo, "quitar del bloque incrustado el Paso 1, que el 360 ya imprime "
                        "arriba (si no, la misma seccion sale dos veces)", flags=re.S)
        A("### Las acciones de hoy, una por una")
        A("")
        A(cuerpo)
    else:
        A("### Las acciones de hoy")
        A("")
        A(f"**No se incrustaron:** no se paso `--acciones` o el archivo no existe.")
        A("")

    # ------------------------------------------------------------- COBERTURA
    # EL AMBITO SE DECLARA AUNQUE SEA LA UNICA TABLA — porque cuando se incrusta el
    # bloque de acciones deja de serlo, y entonces las dos se leen como contradictorias.
    # El chequeo reforzado del verificador encontro esto en el informe ya congelado.
    A("## Que se reviso · TODO el dia (Dropi, WhatsApp y las conversaciones)")
    A("")
    A("| Revision | Universo | Se miro | Ciego |")
    A("| --- | --- | --- | --- |")
    # EL UNIVERSO DE LAS ORDENES ES EL QUE DECLARA DROPI, NO EL QUE TRAJO LA COSECHA.
    # Aqui salia "3.094 de 3.094, ciego 0" mientras el propio volcado decia
    # total_ordenes_cuenta: 3.416. Poner como universo lo que uno alcanzo a bajar
    # convierte cualquier cosecha incompleta en cobertura perfecta: la fila se mide
    # contra si misma y siempre da cero ciego. El universo lo dice la fuente.
    # Y AQUI ESTABA `or len(ordenes)`, CINCO LINEAS DEBAJO DEL COMENTARIO QUE LO PROHIBE.
    # El comentario explicaba que medirse contra lo propio da cobertura perfecta, y el
    # codigo, si el volcado no traia el total, hacia exactamente eso. Un comentario no
    # arregla nada: el default tiene que decir "no se puede medir", nunca un numero que
    # tranquiliza. Es la clase entera — el fallback que restituye el fallo que la linea
    # de arriba dice haber matado.
    _univ_ord = D.get("total_ordenes_cuenta")
    _ciego_ord = max(0, _univ_ord - len(ordenes)) if _univ_ord else 0
    if _univ_ord:
        A(f"| Ordenes de la cuenta | {miles(_univ_ord)} | {miles(len(ordenes))} | "
          f"{('**' + miles(_ciego_ord) + ' sin bajar**') if _ciego_ord else '0'} |")
    else:
        A(f"| Ordenes de la cuenta | **no declarado** | {miles(len(ordenes))} | "
          f"**no se puede medir: el volcado no dice cuantas ordenes tiene la cuenta** |")
    A(f"| Pedidos vivos decididos | {len(acc)} | {len(acc)} | 0 |")
    if EMB:
        # MISMA FAMILIA QUE LA FILA DE ARRIBA: esta decia "857 | 857 | 229 sin etapa",
        # o sea universo igual a revisado — y 229 sin clasificar al lado, que es una
        # ceguera parcial contada en la columna equivocada. El universo es el BRUTO,
        # antes de la exclusion por regla; lo excluido se nombra como excluido, que no
        # es lo mismo que no visto.
        _dd = (ANA or {}).get("conversion_detalle") or {}
        _bruto = _dd.get("universo_bruto")
        _excl = _dd.get("excluidos_integracion")
        _sinet = EMB["sin_clasificar"] if "sin_clasificar" in EMB else None
        # Sin `_bruto` NO se cae a EMB['pedidos'], que es el mismo numero de la columna
        # "Se miro": eso es medirse contra si mismo otra vez, con otra ropa.
        A(f"| Contactos de WhatsApp | {miles(_bruto) if _bruto else '**no declarado**'} | "
          f"{miles(EMB['revisados'])} | "
          # "sin etapa" NO es "no se pudo leer". Estos contactos SE LEYERON: lo que
          # no tienen es Tablero asignado en Chatea. La glosa anterior los llamaba
          # "no se les pudo leer los campos" e INVENTABA una ceguera que no existe —
          # y ademas contradecia, en la misma pagina, el "sin huecos" de mas arriba.
          + (f"{miles(_sinet)} leidos sin etapa asignada" if _sinet else
             ("0" if _sinet == 0 else "**no declarado**"))
          + (f" · {miles(_excl)} excluidos por regla (integracion de Dropi)" if _excl else "")
          + " |")
    else:
        A(f"| Contactos de WhatsApp | ? | **0** | **todo: {err_emb}** |")
    if ANA:
        # NINGUNA FILA SE MIDE CONTRA SI MISMA. Aqui salia "743 | 743 | 0": el universo
        # era el mismo numero que lo revisado, asi que el ciego daba cero por
        # construccion — la fila no podia decir otra cosa aunque faltara medio mundo.
        # El ciego se SUMA de todos los contadores de ceguera que produce el analisis,
        # no de uno elegido a mano.
        # LOS CONTADORES DE CEGUERA TIENEN QUE SER DISJUNTOS O LA SUMA MIENTE.
        # Un chat que fallo al bajarse entra en `sin_chat_bajado` Y en `fallos_barrido`:
        # sumarlos lo cuenta dos veces y produce aritmetica imposible (723 leidas + 25
        # ciegas sobre un universo de 743). En el modo degradado, que es el diario, el
        # ciego se inflaba al doble justo el dia en que la cifra importa.
        # `fallos_barrido` es un SUBCONJUNTO de `sin_chat_bajado`: el que fallo no se
        # bajo. Se cuenta una vez, en el conjunto grande, y el detalle se nombra aparte.
        _huerf = ANA.get("conversaciones_sin_contacto") or 0
        _nobaj = ANA.get("sin_chat_bajado") or 0
        _leidas = ANA["no_compradores"] - _nobaj
        _ciego_conv = _nobaj + _huerf
        # La celda lleva SOLO el numero: "743 sin compra" no es un numero, es una
        # frase, y ninguna comprobacion de valor puede leerla. La aclaracion va en la
        # etiqueta, que es su sitio.
        A(f"| Conversaciones leidas (sin compra) | {miles(ANA['no_compradores'])} | "
          f"{miles(_leidas)} | "
          f"{('**' + miles(_ciego_conv) + '**') if _ciego_conv else '0'} |")
        # ESTAS DOS FILAS SE IMPRIMEN AUNQUE DEN CERO, y esa es la gracia.
        # Salian solo cuando habia algo, asi que el dia bueno el informe no se
        # distinguia del dia en que el contador no corrio. Un cero MEDIDO es la prueba
        # de que se miro; la ausencia de la fila no prueba nada. Es la ley del cero
        # honesto aplicada a la tabla de cobertura, no solo a la prosa.
        A(f"| — bajadas **sin contacto en la lista** | {miles(_huerf)} | "
          f"{'0 utilizables' if _huerf else 'ninguna: las listas cuadran'} | "
          f"{('**' + miles(_huerf) + '**') if _huerf else '0'} |")
        _hst = ANA.get("hilos_sin_tiempo") or 0
        A(f"| — hilos sin tiempo (orden dudoso) | {miles(_hst)} | "
          f"{'leidos por posicion' if _hst else 'ninguno: todos traen ts'} | "
          f"{('**' + miles(_hst) + '**') if _hst else '0'} |")
    else:
        A(f"| Conversaciones leidas | ? | **0** | **todo: {err_ana}** |")
    A("")
    # LA LISTA DE CIEGOS SE CONSTRUYE DESDE TODOS LOS CONTADORES, NO DESDE TRES.
    # Esta lista miraba tres campos y el informe imprimia "No hubo zonas ciegas" con
    # 322 ordenes sin bajar declaradas en la tabla de ENCIMA. Una conclusion que
    # contradice la tabla que tiene tres centimetros arriba es peor que no tenerla:
    # el lector se queda con la frase, que es la que suena a veredicto.
    ciegos = []
    if _ciego_ord:
        ciegos.append(f"**{miles(_ciego_ord)} ordenes** que Dropi declara y la cosecha no bajo")
    if ANA and ANA.get("sin_chat_bajado"):
        ciegos.append(f"**{ANA['sin_chat_bajado']} conversaciones** que no se pudieron bajar")
    if ANA and ANA.get("conversaciones_sin_contacto"):
        ciegos.append(f"**{ANA['conversaciones_sin_contacto']} conversaciones** bajadas cuyo "
                      f"contacto no esta en la lista: hay dato y no se puede usar")
    if ANA and ANA.get("hilos_sin_tiempo"):
        ciegos.append(f"**{ANA['hilos_sin_tiempo']} hilos** sin marca de tiempo, leidos por "
                      f"posicion")
    if EMB and EMB.get("sin_clasificar"):
        ciegos.append(f"**{EMB['sin_clasificar']} contactos** leidos pero sin etapa "
                      f"asignada en Chatea (no es ceguera de lectura: es que el bot no "
                      f"les puso Tablero)")
    if ANA and ANA.get("n_fallos_barrido"):
        # Detalle DENTRO de las no bajadas, no un ciego aparte: ya estan contadas.
        ciegos.append(f"**{ANA['n_fallos_barrido']} de esas** fallaron al leerse (no se "
                      f"suman aparte: ya van contadas arriba)")
    if EMB and EMB.get("sin_respuesta"):
        ciegos.append(f"**{EMB['sin_respuesta']} contactos** marcados sin interaccion")
    if ciegos:
        A("**No se dio por bueno lo que no se miro.** Quedo sin verificar: " + "; ".join(ciegos) + ".")
    else:
        A("**Todo lo que entra en este informe se pudo mirar.** No hubo zonas ciegas.")
    A("")

    # ---- los que no son cambio, pero llevan decision ----
    tuyos = sin_cob + asignar + otros
    if tuyos:
        A("### Los que decides tu")
        A("")
        A("Aqui el calculo no alcanza y la decision es del responsable.")
        A("")
        A("| WhatsApp | Cliente | Ciudad | Situacion |")
        A("| --- | --- | --- | --- |")
        for d in tuyos:
            rendido.add(d.get("id"))
            A(f"| {contacto_de(d)} | {(d.get('cliente') or '')[:18]} | "
              f"{(d.get('ciudad') or '')[:14]} | {d.get('motivo') or d.get('rec')} |")
        A("")

    # ------------------------------------------------------------------
    # LA INVARIANTE. Un veredicto que el motor dicta y el informe no imprime es una
    # decision que nunca llega a nadie. No se arregla mirando: se cuenta y se muere.
    # ------------------------------------------------------------------
    for d in cambios:
        rendido.add(d.get("id"))
    debian = {d.get("id") for d in lista_dec
              if isinstance(d, dict) and d.get("rec") and d.get("rec") != "DEJAR"}
    faltan = debian - rendido
    if faltan:
        detalle = ", ".join(str(i) for i in sorted(x for x in faltan if x is not None)[:12])
        sys.exit(
            f"INFORME INCOMPLETO: el motor dicta {len(debian)} decisiones que no son DEJAR y "
            f"el informe imprime {len(rendido & debian)}. Se pierden {len(faltan)}: {detalle}.\n"
            "No se escribe un informe al que le faltan decisiones: quien lo lea creeria que "
            "esos pedidos van bien.")

    # ------------------------------------------------------------------
    # SEGUNDA INVARIANTE · TODO CAMPO DEL ANALISIS SE IMPRIME O SE DECLARA NO-IMPRESO.
    #
    # Nacio de un fallo real y de una clase nueva: los campos `canal`, `accion`,
    # `calientes_por_canal` y `contactos_sin_telefono` se construyeron, se probaron, se
    # congelaron... y no aparecian en el PDF. Cero ocurrencias en el generador. El
    # arreglo vivia en el JSON y moria antes del papel — y el JSON no lo lee nadie.
    # La invariante de decisiones ya vigilaba ese salto para la Parte B; esta lo vigila
    # para la Parte A.
    #
    # No comprueba que el texto contenga el valor (eso seria fragil y se engañaria
    # solo): comprueba que ALGUIEN HAYA DECIDIDO. Un campo nuevo en el analisis obliga
    # a decir si va al papel o por que no. El silencio no es una opcion.
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # AQUI VIVIA LA AUTO-VERIFICACION DEL GENERADOR (`CAMPOS_ANA`), Y SE MURIO ENTERA.
    #
    # Cinco versiones, y cada una comprobaba algo MAS DEBIL de lo que decia comprobar:
    #   v1  buscaba el valor suelto en el documento — un `0` esta en cualquier texto
    #   v2  exigia etiqueta y valor en la misma linea — en una fila de 5 columnas se
    #       cumple por casualidad
    #   v3  miraba la celda... pero cualquier celda de la fila
    #   v4  anclas invisibles `<!--v:...-->` — que **salieron impresas en el PDF del
    #       cliente**, las siete, la primera en la pagina 1
    #   v5  parseaba `L`, la lista en memoria — **no el archivo**
    #
    # Las dos ultimas son la misma falta con dos disfraces: **medir el intermedio y
    # llamarlo el entregable**. Y es inevitable aqui dentro: un generador solo tiene a
    # mano la variable de la que saldra el papel, nunca el papel. Cinco intentos son
    # evidencia suficiente de que el diseño en-banda no converge — no de que me faltara
    # una version mas.
    #
    # El verificador se separo: `verificar_informe.py` abre el `.md` DEL DISCO y no
    # conoce este modulo. No puede medir el intermedio porque no existe para el.
    # Corre como paso final del flujo; si falla, el informe no se entrega.
    #
    # De aqui solo queda lo probado en batalla: la invariante de decisiones (27/27,
    # cinco rondas sin fallar) y el cero honesto, que estan arriba.
    # ------------------------------------------------------------------

    escribir_texto(a.salida, "\n".join(L))

    # PASO FINAL: EL VERIFICADOR DEL PAPEL, SOBRE EL ARCHIVO YA ESCRITO.
    # Se llama como PROCESO APARTE a proposito. Importarlo aqui volveria a mezclar el
    # generador con su verificador, y toda la historia de las cinco versiones dice que
    # esa mezcla es la que produce "medir el intermedio y llamarlo el entregable".
    # Si el papel no cuadra con el analisis, se dice y se sale con error: no se entrega.
    if ANA and a.analisis:
        import subprocess
        _v = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verificar_informe.py")
        _r = subprocess.run([sys.executable, _v, "--informe", a.salida,
                             "--analisis", a.analisis], capture_output=True, text=True)
        for _ln in (_r.stdout + _r.stderr).strip().splitlines():
            print("  " + _ln)
        if _r.returncode != 0:
            sys.exit("EL PAPEL NO CUADRA CON EL ANALISIS: no se entrega.")


    print(f"informe: {a.salida}")
    print(f"  parte 1: {'OK' if EMB else 'NO CORRIDA'} embudo · {'OK' if ANA else 'NO CORRIDO'} motivos")
    print(f"  parte 2: {len(acc)} vivos, {len(cambios)} cambios de transportadora")
    print(f"  invariante: {len(debian)} decisiones no-DEJAR dictadas, {len(rendido & debian)} impresas")

    if a.pdf:
        import subprocess
        # Un entregable ajeno no se pisa aunque el nombre coincida. Paso de verdad:
        # una corrida de prueba sobrescribio el informe que otro chat habia dejado.
        # EL INFORME PROPIO SE REEMPLAZA POR DISEÑO; LO AJENO NO SE PISA NUNCA.
        # El nombre no lleva fecha a proposito — el del dia siempre en el mismo sitio —
        # asi que el de ayer se ARCHIVA antes de escribir el de hoy. Sin esto, la
        # segunda corrida sale con error y NO HAY PDF.
        ok, msg = preparar_destino_pdf(
            a.pdf, os.path.join(os.path.dirname(os.path.abspath(a.salida)), "_archivo"))
        if not ok:
            sys.exit(msg)
        if msg:
            print(msg)
        PY_PDF = os.path.expanduser("~/.golden/pdfenv/bin/python")
        SK = os.path.expanduser("~/.claude/skills/golden-pdf-check/scripts")
        if not os.path.exists(PY_PDF):
            print(f"AVISO: no se genero el PDF, no existe {PY_PDF}. La regla de entrega NO se "
                  "cumplio.", file=sys.stderr)
        else:
            r = subprocess.run([PY_PDF, f"{SK}/build_pdf.py", a.salida, a.pdf, "--no-index"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print(f"AVISO: el PDF FALLO.\n{r.stderr[-400:]}", file=sys.stderr)
            else:
                au = subprocess.run([PY_PDF, f"{SK}/audit_pdf.py", a.pdf],
                                    capture_output=True, text=True)
                # NO-AUDITADO NO ES APROBADO, y hay que leer el CODIGO DE SALIDA para
                # saberlo. Si al auditor le falta una libreria, imprime que la instales
                # y termina — y esta lectura, que solo buscaba la palabra "Veredicto",
                # se quedaba con "SIN VEREDICTO" y seguia adelante marcando el PDF como
                # propio. Un PDF sin auditar quedaba indistinguible de uno aprobado.
                # Es la ley del cero honesto en el ultimo paso de la entrega: "no se
                # pudo mirar" y "esta bien" son respuestas distintas.
                ver = "SIN VEREDICTO"
                if au.returncode != 0:
                    ver = f"NO AUDITADO (el auditor fallo, salida {au.returncode})"
                    print(f"  AVISO: {(au.stderr or au.stdout).strip()[:200]}",
                          file=sys.stderr)
                else:
                    for ln in au.stdout.splitlines():
                        if "Veredicto" in ln:
                            ver = ln.rsplit("**", 1)[-1].strip() if "**" in ln else ln.strip()
                            break
                print(f"  PDF: {a.pdf} · auditoria {ver}")
                marcar_como_propio(a.pdf)   # deja la senal: el de manana sabra que es nuestro
                if "APROBADO" not in ver:
                    print("  OJO: el PDF no quedo aprobado por el estandar.", file=sys.stderr)


if __name__ == "__main__":
    main()
