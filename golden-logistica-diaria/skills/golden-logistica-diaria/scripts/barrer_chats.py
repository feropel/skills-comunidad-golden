#!/usr/bin/env python3
"""Baja la conversacion COMPLETA de cada contacto de Chatea (entrantes + bot).

OJO: sin `include_bot=1` el endpoint solo devuelve mensajes ENTRANTES, y entonces
"el bot nunca respondio" y "el bot respondio y el cliente se fue" se ven igual.
Ese fue el error que hacia imposible responder POR QUE no compraron.

INCREMENTAL: con --previo se reusa lo que ya se bajo y solo se piden los que faltan.
No es comodidad, es la condicion para que esto sea una rutina diaria. Medido: 900
contactos a ritmo suave son ~5 horas, casi todas en reintentos de 429, y sin
incremental una corrida que se corta a la hora cuatro se pierde ENTERA. Con previo,
cada tanda que sobrevive queda ganada.

  python3 barrer_chats.py --contactos c.json --token t.txt --salida chats.json \
      [--previo chats-de-antes.json]
"""
import argparse, concurrent.futures as cf, json, os, sys, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escritura import escribir_json, escribir_texto, exigir_salida_distinta, leer_json, leer_texto

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
MAX_PAG = 12   # con 5 se truncaba el 5% de los hilos; en paralelo subirlo no duele


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contactos", required=True)
    ap.add_argument("--token", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--pausa", type=float, default=0.25)
    ap.add_argument("--hilos", type=int, default=10)
    ap.add_argument("--previo", help="archivo de una corrida anterior: sus conversaciones se "
                    "reusan y solo se piden las que falten. Acepta archivos PARCIALES.")
    a = ap.parse_args()

    # La salida no puede ser tambien el previo: escribir encima de lo que se lee
    # destruye la unica copia si algo sale mal, y ese fue el comando que esta
    # fabrica llego a recomendar.
    exigir_salida_distinta(a.salida, a.previo, a.contactos)

    # EL TOKEN SE LEE CON LA FAMILIA `leer_*`, COMO TODO LO DEMAS.
    # Aqui habia un `open()` crudo, y era destruible: pasar `--salida` apuntando al
    # archivo del token lo pisaba con el JSON de la corrida, con salida 0. Un secreto
    # borrado en silencio, y el barrido siguiente sin con que autenticarse.
    tok = leer_texto(a.token).strip()
    H = {"Authorization": "Bearer " + tok, "User-Agent": UA, "Accept": "application/json"}

    def req(path, intentos=6):
        """El API tira 429 en cuanto se paraleliza. Sin reintento, el barrido
        'termina bien' habiendo perdido la mitad de las conversaciones, y el
        informe reparte motivos sobre lo que quedo. Se espera y se reintenta."""
        espera = 2.0
        for n in range(intentos):
            try:
                r = urllib.request.Request("https://chateapro.app/api" + path, headers=H)
                return json.load(urllib.request.urlopen(r, timeout=60))
            except urllib.error.HTTPError as e:
                if e.code != 429 or n == intentos - 1:
                    raise
                time.sleep(espera)
                espera = min(espera * 2, 30)   # 2, 4, 8, 16, 30…
            except urllib.error.URLError:
                if n == intentos - 1:
                    raise
                time.sleep(espera)
        raise RuntimeError("inalcanzable")

    C = leer_json(a.contactos)
    contactos = C["contactos"] if isinstance(C, dict) else C

    # ---- INCREMENTAL ----
    # Acepta parciales a proposito: una corrida a medias es presupuesto de 429 ya
    # gastado, y perderlo es pagar dos veces por el mismo dato.
    out, fallos = {}, []
    prev_meta = None
    if a.previo:
        try:
            P = leer_json(a.previo)
            reusados = P.get("chats") or {}
            out.update(reusados)
            prev_meta = {"archivo": a.previo,
                         "generado": P.get("generado"),
                         "reusados": len(reusados),
                         "venia_completo": P.get("cosecha_completa")}
            print(f"previo: {len(reusados)} conversaciones reusadas de {a.previo}"
                  + ("" if P.get("cosecha_completa") else "  (venia INCOMPLETO)"),
                  file=sys.stderr, flush=True)
        except Exception as e:
            sys.exit(f"No se pudo leer el previo {a.previo}: {type(e).__name__}: {e}. "
                     "Corrige la ruta o quita --previo; no se sigue a medias porque "
                     "rebarrer entero sin querer cuesta horas de 429.")

    pendientes = [c for c in contactos if c.get("user_ns") not in out]
    if a.previo:
        print(f"faltan por bajar: {len(pendientes)} de {len(contactos)}",
              file=sys.stderr, flush=True)
    # En serie, 900 contactos tardan mas de una hora contra este API: medido el
    # 2026-08-10, se aborto a los 45 minutos sin terminar. Un informe que hay que
    # correr TODAS las mañanas no puede tardar eso, asi que el barrido va en
    # paralelo. El orden de llegada no importa: la salida es un dict por user_ns.
    def uno(c):
        ns = c.get("user_ns")
        if not ns:
            return None, {"ns": None, "razon": "el contacto no trae user_ns"}
        base = (f"/subscriber/chat-messages?user_ns={ns}"
                f"&include_bot=1&include_note=1&include_system=1")
        try:
            d = req(base)
            msgs = list(d.get("data", []))
            lp = (d.get("meta") or {}).get("last_page", 1) or 1
            for pg in range(2, min(lp, MAX_PAG) + 1):
                msgs += req(base + f"&page={pg}").get("data", [])
            # `payload.referral` del primer entrante trae el ID DEL ANUNCIO de Meta
            # (source_id) por el que llegó esa persona, mas headline y ctwa_clid. Es
            # la unica forma de atribuir contacto -> anuncio sin tocar la API de Meta,
            # y si no se guarda aqui se pierde: hay que volver a barrer para tenerlo.
            # EL CAMPO DE TIEMPO ES `ts`, NO `created_at` NI `date`.
            # Medido: created_at/date vienen VACIOS en 6.911 de 6.911 mensajes. Con el
            # campo vacio no solo se pierde la hora: es imposible reordenar despues, asi
            # que un hilo mal guardado hay que RE-BARRERLO entero.
            #
            # Y EL API ENTREGA DEL MAS RECIENTE AL MAS VIEJO. La inversion va AQUI, donde
            # se guarda, no en quien lee: asi cualquiera que abra este archivo recibe
            # cronologia sin tener que conocer la trampa. Costo de no hacerlo, medido por
            # el verificador: "responder hoy" listaba 314 clientes cuando el real era 1.
            hilo = [{"t": m.get("type"), "c": m.get("content"),
                     "ts": m.get("ts"),
                     "f": m.get("created_at") or m.get("date"),
                     "ref": ((m.get("payload") or {}).get("referral")
                             if isinstance(m.get("payload"), dict) else None)}
                    for m in msgs]
            hilo.sort(key=lambda x: x.get("ts") or 0)          # CRONOLOGICO, siempre
            sin_ts = sum(1 for x in hilo if not x.get("ts"))
            fallo = None
            if sin_ts:
                fallo = {"ns": ns, "razon": f"{sin_ts} de {len(hilo)} mensajes sin 'ts': "
                                            "el orden de ese hilo no es de fiar"}
            if lp > MAX_PAG:
                fallo = {"ns": ns, "razon": f"conversacion de {lp} paginas, se leyeron {MAX_PAG}"}
            return (ns, hilo), fallo
        except Exception as e:
            return None, {"ns": ns, "razon": f"{type(e).__name__}: {e}"}

    hechos = 0
    with cf.ThreadPoolExecutor(max_workers=a.hilos) as ex:
        for res, fallo in ex.map(uno, pendientes):
            if res:
                out[res[0]] = res[1]
            if fallo:
                fallos.append(fallo)
            hechos += 1
            if hechos % 100 == 0:
                # A stderr: stdout puede estar detras de un `tail` que lo retiene
                # hasta el final, y entonces no hay forma de ver el progreso.
                print(f"  {hechos}/{len(pendientes)}", file=sys.stderr, flush=True)

    # UN ARCHIVO MEZCLADO DE DOS CORRIDAS SON DOS FOTOS, y esa clase ya cobro dos
    # veces en este ecosistema. Asi que el archivo lo DICE: cuanto vino del previo,
    # cuanto se bajo fresco, y de cuando es el dato mas viejo que se esta reusando.
    frescos = len(out) - (prev_meta["reusados"] if prev_meta else 0)
    escribir_json(a.salida, {"generado": time.strftime("%Y-%m-%dT%H:%M:%S"),
               # R6: la bandera se DERIVA de los conteos. Escribirla a mano es
               # exactamente la mentira que las compuertas vienen a impedir.
               "cosecha_completa": (len(fallos) == 0 and len(out) == len(contactos)),
               "pedidos": len(contactos), "traidos": len(out),
               "incremental": bool(a.previo),
               "reusados_del_previo": prev_meta["reusados"] if prev_meta else 0,
               "bajados_frescos": frescos,
               "dato_mas_viejo_reusado": prev_meta["generado"] if prev_meta else None,
               "previo": prev_meta,
               "_ojo_dos_fotos": ("cuando 'incremental' es true este archivo mezcla dos "
                                  "momentos: lo reusado es de 'dato_mas_viejo_reusado' y lo "
                                  "fresco es de 'generado'. Para medir conducta del cliente "
                                  "no estorba; para medir un instante exacto, si."),
               "fallos": fallos, "chats": out},
              )
    print(f"listo: {len(out)} conversaciones de {len(contactos)} contactos | "
          f"reusadas {prev_meta['reusados'] if prev_meta else 0} · frescas {frescos} | "
          f"fallos: {len(fallos)}")


if __name__ == "__main__":
    main()
