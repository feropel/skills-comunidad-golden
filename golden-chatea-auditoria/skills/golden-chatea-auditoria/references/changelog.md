# Changelog · golden-chatea-auditoria

La historia completa de la skill. Vive aquí y no en `SKILL.md` porque el cuerpo se carga
ENTERO en cada invocación: 158 de sus 401 líneas eran historia, el 39% del archivo, y la
historia no hace falta para ejecutar. En `SKILL.md` se queda el acta del Centro de Mando y
la entrada VIGENTE, que es lo que un editor necesita ver antes de tocar nada.

Las entradas van de la más nueva a la más vieja.

## v3.1 — 2026-09-24 — Remarketing IA fuera, y la bandera `opcional` que nadie leía

**Disparador:** en la auditoría de un cliente, B6 reportó "Remarketing IA NO está instalado". FER lo
cortó: *"no más asistente de remarketing, ni lo vamos a revisar, ni lo vamos a auditar, nada, hasta el
momento que yo vuelva y te diga"*. Ya lo había sacado del ecosistema el 21-sep; esa fila llegó al
instalador y no a este auditor, que es hermano. **Lección de proceso: una fila que retira un asistente
se reparte a todas las skills que lo nombran, no solo a la que lo instala.**

**Lo que se midió antes de tocar:** `assets/asistentes-esperados.json` ya tenía Remarketing IA con
`"opcional": true`, y `references/controles.md` decía que los opcionales no se reportan. **El código
no leía la bandera** (`grep -c opcional auditar.py` = 0). Línea base del banco: 33 sembrados + 27
pruebas en verde, con B6 gritando el opcional y 7 hallazgos que nombraban Remarketing (B6, D3, D5).

**Qué cambió:**
- `EXCLUIDOS_POR_FER` en `auditar.py`: los campos del asistente se apartan AL CARGAR el inventario,
  así que ningún control los ve (B6, el país de L4, los topes, el disparador en D3/D5). Se declaran en el
  universo (`campos_excluidos_por_fer`) con su conteo y motivo. `campos_bot` sigue contando el total.
- B6 lee `opcional` y saca del denominador a los opcionales y a los excluidos: "4 de 4 presentes · no
  se esperan por decisión de FER: Remarketing IA".
- `--incluir-excluidos`: opt-in, solo cuando FER lo pida para un espacio concreto.
- Autoprueba: el sabotaje de D3b vivía en el disparador de Remarketing; se mudó a
  `[Ventas Wp] Disparador de productos` para no perder su banco en silencio. Prueba nueva **EXCL**.

**Verificación:** 33 sembrados + 28 pruebas en verde, y la única línea que cambió frente a la base es
EXCL. Dos mutantes la hacen fallar: vaciar `EXCLUIDOS_POR_FER` (2 hallazgos nombran Remarketing, nada
declarado) y quitar la lectura de `opcional` (el opcional vuelve a gritarse). El control negativo, un
espacio sin `[Carritos] Configuracion`, sigue dando B6.

**No se tocó:** el remarketing POR PRODUCTO de Ventas WhatsApp (`estandar-prompts.md`, llaves
`remarketing.activar_1/2 · prompt_1/2`). Es el seguimiento de cada producto, no el asistente.

**Segunda ronda, el mismo día, tras el `golden-verificador`** (que encontró 5 fallas donde la primera
ronda daba verde). La lección es la de siempre: **un filtro puesto al cargar no cubre los caminos que
leen el DUMP crudo.**
- **El diff con `--anterior` daba 9 "BORRADO" falsos:** filtraba el lado nuevo y no el viejo. Ahora
  los dos pasan por el mismo filtro.
- **F13 auditaba el "Agente de Remarketing"**, que vive en `_agentes_detalle`, otra zona del DUMP. Se
  aparta por nombre (`/flow/ai-agents`, `/flow/ai-tasks`) y se declara en
  `agentes_ia_excluidos_por_fer`. Primer intento fallido y medido: comparaba el nombre del agente
  contra "remarketingia", y el agente se llama sin "IA".
- **La acción de L4 seguía nombrando Remarketing** y la prueba no lo veía, porque solo miraba título,
  evidencia y campo. La prueba ahora mira el hallazgo ENTERO.
- **Variantes del nombre** (doble espacio, guion, espacio no separable) se escapaban: el filtro usa
  una llave sin tildes ni signos.
- **Quien opera la skill no se enteraba:** bandera en la tabla del SKILL.md, nota en la fase manual
  y fila "Apartados por decisión de FER" en el universo del informe. B1 dice por qué faltan los
  apartados. Un nombre de cliente que había entrado en el sello del SKILL.md, fuera.
- Índice del changelog rehecho: decía "499 líneas" con 661 y sus números de línea no calzaban.

Verificación de la segunda ronda: autoprueba 33 + 28 en verde; **4 mutantes, uno por arreglo, los 4
cazados** (diff sin filtrar · agentes sin filtrar · llave vieja · L4 nombrando al excluido). Contra un
DUMP real con el agente: 9 campos y 1 agente apartados, 0 hallazgos que los nombren, B1 lo explica.

<!-- skill v2.8 — 2026-09-08 — EL CONTROL QUE FALTABA: LA COHERENCIA DE PAIS, COMPLETA.
El encargo es de FER y lo dio con su ejemplo: *"si esta en Guatemala y su validacion de
direcciones es de Colombia, pues hay que decir: no, eso esta mal, hay que corregirlo."*

POR QUE NINGUNO DE LOS 53 CONTROLES ANTERIORES LO VEIA, que es lo que hace que valga la pena.
No fue un descuido: cada uno mira una dimension distinta y el pais se cuela entre todas.
F14 compara contra la plantilla de FABRICA -- y la de fabrica es COLOMBIANA siempre, elijas el
pais que elijas (61 de 61 campos identicos byte a byte entre un espacio de Colombia y uno
creado eligiendo Mexico), asi que lo colombiano no le parece anomalo. L3 compara contra otro
CLIENTE. L1 exige que la llave exista. L2 que no este de compromiso. **Una configuracion puede
pasar los cuatro y seguir diciendole a un guatemalteco que su garantia se rige por el Estatuto
del Consumidor colombiano.**

SON DOS CONTROLES, PORQUE HAY DOS FORMAS DE QUE EL PAIS ESTE MAL:
· **L4 — los paises declarados no coinciden entre si.** El pais no vive en un sitio: vive en
  CINCO, uno por asistente, cada uno con su llave y su propio nombre de llave. Un espacio medio
  migrado tiene tres asistentes en un pais y dos en otro y cada uno decide con el suyo.
· **L4b — el contenido es de otro pais.** Medido contra `assets/lexico-por-pais.json`.

LAS DOS TRAMPAS QUE ESTE CONTROL TRAIA, Y COMO SE CERRARON ANTES DE SELLAR:
1. **El marcador ambiguo acusa SIEMPRE.** "Envia" es una transportadora colombiana Y el verbo
   mas corriente de un texto de logistica; "Domina" y "Correos" igual. Un control que acusa de
   mas no es un control severo: a los tres informes el dueno deja de leerlo. El lexico se
   GENERA con una regla de admision (5 caracteres y no ser palabra corriente) y **guarda a la
   vista los 7 rechazados con su motivo**. La excepcion son las siglas de moneda -- COP, MXN,
   GTQ, ARS -- que se admiten cortas pero se buscan SENSIBLES A MAYUSCULAS; USD, EUR, PEN y PAB
   quedan fuera a proposito por compartidas o ambiguas.
2. **El lexico CADUCA en silencio.** Una transportadora nueva no da error: deja de verse. Por
   eso las familias se marcan, los hallazgos que salen SOLO de una familia que caduca bajan a
   FUGA, las estables (moneda, organismo de consumo) sostienen el MUERTO, y la cobertura
   imprime la fecha de medicion. Y **un pais que no este en el lexico NO se juzga y se
   DECLARA**: el pais es parametro, no puerta.

🔴 EL ERROR QUE COMETI Y QUE ESTABA DOCUMENTADO A DIEZ LINEAS DE DONDE ESCRIBIA. La primera
version de L4b barria TODOS los campos y acuso a los DOCE productos del fixture por llevar
moneda "COP" en un espacio ecuatoriano. El hallazgo no era falso: **era de OTRA auditoria** --
la moneda de un producto la mira F5, que es de productos. Un control que se sale de su alcance
no descubre mas: entierra lo suyo bajo doce lineas que el dueno no puede accionar desde aqui.
Acotado a los campos del esquema, y declarado en la cobertura cuando el esquema no esta.
Y en la prueba repeti literalmente el fallo que la prueba ESQ ya tenia comentado: coger el
primer hallazgo del control en vez del del campo sembrado, que daba un verde por orden
alfabetico. **Un comentario que avisa de un error no impide cometerlo doce lineas mas abajo.**

🔴 LA RAMA GEMELA, ABIERTA Y CERRADA EL MISMO DIA. La prueba CAT medía catalogo -> codigo. Al
cablear L4 y L4b, el CODIGO se adelanto al catalogo y nada mordio: dos controles corriendo, sin
documentar, saliendo en el informe sin que el dueno tuviera donde leer que miden. CAT mide ya
los DOS sentidos. Catalogo 53 -> 55 automaticos.

VERIFICACION (fase 4, ejecutado, no razonado):
· Autoprueba: 32 defectos sembrados + 26 pruebas de comportamiento, todas en verde.
· SABOTAJE, uno por uno y cada uno muerde POR SU RAZON: quitado L4b del catalogo -> cae la rama
  gemela nueva de CAT · quitado el permiso del marcador compartido -> cae PAISC por
  "compartido" · forzado a juzgar un pais fuera del lexico -> cae PAISC por "fuera_lexico".
· CONTRA DATOS REALES, los 6 de los 7 campos de configuracion que hay en disco: **L4 encuentra
  el pais VACIO de Remarketing IA** (4 con valor, 1 vacio) y L4b da CERO marcas ajenas sobre 78
  hojas de texto. **Un cero se ve igual sano que ciego**, asi que se corrio la contraprueba: los
  MISMOS campos reales declarando GUATEMALA dan **14 marcas ajenas en 5 de los 6 campos** --
  Nequi y Daviplata en los datos de pago, Servientrega/Coordinadora/Interrapidisimo en las
  transportadoras y en el prompt de direcciones, COP y "pesos colombianos" en dos monedas.
  Ese es, literalmente, el caso que planteo FER.

LO QUE NO SE VERIFICO: el septimo campo (`[Ventas Wp] Configuracion general 2`) no esta en
disco, asi que la corrida real cubre 6 de 7. Y el lexico cubre 9 paises: cualquier otro NO se
juzga. -->

<!-- skill v2.7 — 2026-09-08 — LA CONFIGURACION YA TIENE ESQUEMA, Y CON EL LOS TRES CONTROLES QUE FER PEDIA.
FER lo dijo asi: *"Antes yo copiaba y pegaba mi espacio al del cliente, era una copia identica y
me tocaba cambiar a mano el nombre. Lo que quiero ahora es que no sea un espejo: que se
interprete lo que cada tienda es -si es una marca o si es multinicho- y se adapten estos campos
a la personalidad de cada tienda. La MISMA ESTRUCTURA, pero con SU personalidad."*

LEIDO POR API, no deducido: 95 bot fields del espacio de referencia en 11 peticiones, y de ahi
los 7 campos JSON que son LA configuracion de los 6 asistentes. **156 llaves.** Viven en
`assets/esquema-configuracion.json` con su tipo y el orden de magnitud de cada campo bien
puesto, y **sin un solo valor dentro**: el repo es publico, y ademas el texto de una tienda
concreta es justo la plantilla que hay que dejar de clonar.

🔴 MI ERROR EN EL CAMINO, Y VALE LA PENA QUE QUEDE. Al leer los bot fields corte la paginacion
con `len(lote) < 100` dando por hecho que la API respeta `per_page`. **No lo respeta: devuelve
10 por pagina.** Con eso lei 10 campos de 95 y **conclui que el token era de otro espacio**, y
se lo dije a FER. Un negativo sacado de una lectura truncada, que es la clase que esta casa ya
tiene registrada. La unica parada honesta es la PAGINA VACIA, y asi quedo.

TRES CONTROLES NUEVOS (bloque L), tres porque hay tres formas distintas de estar mal:
· **L1 MUERTO · la llave NO ESTA.** El asistente lee ese trozo vacio y se inventa el
  comportamiento. La estructura se exige aunque el contenido se adapte.
· **L2 FUGA · la llave esta puesta de compromiso.** Se compara contra el orden de magnitud del
  MISMO campo en el patron y solo salta por debajo del 15%, y solo en campos que en el patron
  llevan contenido de verdad (>=120 caracteres): un `si`/`no` no admite escalas.
· **L3 DUDA · la configuracion es un ESPEJO.** Ningun otro control lo veia: F14 compara contra
  la plantilla de FABRICA, no contra otro cliente, y un espejo se ve perfectamente configurado.

L2 y L3 son GEMELOS OPUESTOS —demasiado corto y demasiado igual— y van juntos a proposito: cerrar
uno sin el otro deja la puerta abierta por el lado contrario, que es como se colaron los dos
ultimos defectos de esta skill.

L3 SE REESCRIBIO ANTES DE SELLAR. La primera version disparaba campo a campo y era ruido: que UN
texto largo coincida al caracter con el patron puede ser casualidad, y un hallazgo por campo
entierra la senal. Lo que delata al espejo es la PROPORCION -- quien clona y solo cambia el
nombre deja casi todos los campos intactos. Ahora exige mas de la mitad de los campos
comparables y al menos dos, y la evidencia lleva el reparto: "4 de 5" convence, "1 campo
coincide" no. No es un control mas flojo: es mas exacto y mucho menos ruidoso.

Medido al cerrar: autoprueba 32 defectos sembrados + 26 pruebas de comportamiento, todas verdes.
La prueba ESQ lleva las tres formas de estar mal en el mismo campo sembrado, y **se filtra por el
campo, no por `[0]`**: el fixture base ya trae configuraciones casi vacias, asi que coger el
primer hallazgo hacia que la prueba mirase otro campo y diera un verde que no probaba nada.
Contraprueba una por una: saboteado L1 caen solo L1, saboteado L2 solo L2, saboteado L3 solo L3.
Catalogo 50 -> 53 controles automaticos, todos cableados. -->

## Índice (entrada más nueva arriba · se busca por el TÍTULO: los números de línea caducaban solos)

| Versión | Fecha | Qué cambió |
|---|---|---|
| v3.1 | 2026-09-24 | Remarketing IA fuera y la bandera `opcional` que nadie leía |
| v3.0 | 2026-09-22 | La cobertura del esquema medida contra las hermanas, control L5 (en el SKILL.md, comentario HTML) |
| v2.9 | 2026-09-20 | Fronteras reescritas, description con la hermana de operación (en el SKILL.md, comentario HTML) |
| v2.8 | 2026-09-08 | L4 y L4b · la coherencia de país, completa |
| v2.6 (narrativa) | 2026-09-08 | Cuatro defectos del verificador (comentario HTML) |
| v1.9 | 2026-09-02 | Dos alcances, dos frases (comentario HTML) |
| v2.5 (acta corta) | 2026-09-07 | F14, plantilla de fábrica (comentario HTML) |
| v2.3 | 2026-09-05 | La skill guarda el estándar, no a los clientes (comentario HTML) |
| v2.2 | 2026-09-05 | El alcance ya es código (comentario HTML) |
| v2.1 | 2026-09-05 | B8, el defecto que el catálogo tapaba (comentario HTML) |
| v2.0 | 2026-09-05 | Auditoría fresca, mandato 2026-09-03 (comentario HTML) |
| v1.0 | 2026-08-20 | Versión inicial declarada por el Centro de Mando |
| v2.5 (narrativa) | 2026-09-07 | F14 con su historia completa |
| — | 2026-09-07 | Cupo de la API: se lee, se avisa, se frena |
| v2.6 (narrativa) | 2026-09-08 | La frontera cerrada, el D1 archivado |

Las entradas "narrativa" y "acta corta" del mismo número de versión son el mismo cierre contado
dos veces (el acta compacta que vivió bajo el H1 de `SKILL.md` y la crónica larga del día);
no son versiones distintas ni se contradicen.

## v2.8 — 2026-09-08 — L4 y L4b · la coherencia de país, completa

Encargo de FER con su ejemplo: *"si está en Guatemala y su validación de direcciones es de
Colombia, pues hay que decir: no, eso está mal, hay que corregirlo."*

**Por qué ninguno de los 53 controles anteriores lo veía.** No fue descuido: F14 compara contra
la plantilla de FÁBRICA y la de fábrica es colombiana siempre (61 de 61 campos idénticos entre
un espacio de Colombia y uno creado eligiendo México), así que lo colombiano no le parece
anómalo; L3 compara contra otro CLIENTE; L1 exige que la llave exista; L2 que no esté de
compromiso. Una configuración puede pasar los cuatro y seguir citándole a un guatemalteco el
Estatuto del Consumidor colombiano.

- **L4** · los países declarados no coinciden entre sí. El país vive en CINCO sitios, uno por
  asistente. Desacuerdo = MUERTO; uno vacío teniendo los demás puestos = ANUNCIADA.
- **L4b** · el contenido es de otro país, medido contra `assets/lexico-por-pais.json`
  (77 marcadores, 9 países, generado con regla de admisión y con los 7 rechazados a la vista).

**Las dos trampas, cerradas antes de sellar:** el marcador ambiguo (`Envía` es transportadora
colombiana y el verbo más corriente de logística) y el léxico que caduca (las familias que
caducan bajan la severidad a FUGA; moneda y organismo de consumo la sostienen en MUERTO). Un
país fuera del léxico **no se juzga y se declara**.

**Dos errores propios que quedan escritos.** L4b barría al principio TODOS los campos y acusó a
los doce productos del fixture por su moneda: el hallazgo no era falso, era **de otra
auditoría** (la moneda de un producto la mira F5). Y en la prueba repetí el fallo que la prueba
ESQ ya llevaba comentado a doce líneas: coger el primer hallazgo del control en vez del del
campo sembrado, que daba un verde por orden alfabético.

**Rama gemela, abierta y cerrada el mismo día:** CAT medía catálogo → código; al cablear L4 el
código se adelantó al catálogo y nada mordió. CAT mide ya los dos sentidos. 53 → **55**
controles automáticos.

**Verificado ejecutando:** autoprueba 32 + 25 en verde · tres sabotajes, cada uno muerde por su
razón · contra datos reales (6 de los 7 campos de configuración que hay en disco) L4 encuentra
el país vacío de Remarketing IA y L4b da cero sobre 78 hojas — y la contraprueba con los mismos
campos declarando GUATEMALA da **14 marcas ajenas en 5 de los 6 campos**.

<!-- skill v2.6 — 2026-09-08 — LOS CUATRO DEFECTOS DEL VERIFICADOR, Y LOS TRES ERAN COBERTURA FALSA.
Un verificador adversarial leyó el estado final tras la auditoría de un cliente y encontró
cuatro cosas. Tres son la MISMA clase con tres caras: el informe decía haber mirado más de lo
que miró.

(1) EL PAQUETE DE CORRECCION ESCONDIA 23 DE 36 HALLAZGOS. Dos huecos a la vez. Uno: la rama de
FUGA (🟡) conservaba `if not h.get("accion"): continue`. El arreglo original se hizo en su día
solo para MUERTO/ANUNCIADA y NADIE BUSCO SU HERMANA, aunque el propio comentario del código ya
decía "la severidad decide, no la presencia de ese campo" — la regla estaba escrita y a medio
implementar. Se caían 11 hallazgos abiertos, y una FUGA es justo lo que LLEGA AL CLIENTE. Dos:
`escribir_handoff` solo recorría `a.hallazgos`, así que lo apartado por alcance no viajaba ni
se mencionaba, y el paquete se leía como si fuera todo lo encontrado. Ahora lleva cabecera con
el CONTEO Y NADA MÁS.

(2) Y esa cabecera destapó que EL CODIGO SEGUIA CONTRADICIENDO LA LEY QUE SE CORRIGIO EN PROSA.
El informe imprimía el reparto por severidad de lo apartado ("2 muerto · 3 fuga"). Un conteo se
obtiene sin mirar; una severidad EXIGE haber juzgado. Decir "3 fuga" sobre productos ES auditar
productos aunque no se nombre el campo — la reincidencia que FER corrigió dos veces el mismo
día. La ley se arregló el 05-sep en el texto y el código llevaba desde entonces desmintiéndola.

(3) F13 DECLARABA 72 OBJETOS DE LA ZONA IA Y 40 LLEGARON SIN UNA SOLA CADENA. Un agente `locked`
que el extractor no puede abrir engordaba el denominador de "revisados". Ahora el numerador son
los objetos CON texto, los vacíos salen como DUDA declarada, y se dice que mirarlos en el panel
es la forma de saber si el extractor se los está dejando.

(4) J1 NO DECLARABA CUANDO NO CORRIA. Su `cubre` vivía dentro de `comparar()`, que solo se
ejecuta si hay dump anterior. Sin dump previo, J1 desaparecía de la tabla y su ausencia se leía
como "no tenía nada que decir" en vez de "no se corrió". Ahora declara NO_CORRIDO siempre, y
`comparar()` sustituye esa línea en vez de añadir una segunda.

Y dos clases cerradas, no dos casos:
· CONTROL PROMETIDO SIN INSTRUMENTO. `references/controles.md` marca cada control A (automático)
  o H (a mano). Seis marcados A no aparecían por su nombre en ningún script: D3b, I1b, J1, K1, K2
  y K3. Cinco sí estaban implementados —sin nombre— y J1 era el defecto (4). La prueba CAT cruza
  el catálogo contra las fuentes y muerde ante cualquier control A que se documente y no se
  cablee. Contraprueba: un `Z9` inventado la hace fallar.
· LA CIFRA DE LA AUTOPRUEBA SE MIDE, NO SE ESCRIBE. Vivía a mano en tres sitios y decía "31+16"
  y "31+11" cuando ya iba por otro número. Ahora la autoprueba imprime su propio conteo y los
  documentos apuntan a esa línea.

Medido al cerrar: autoprueba 32 defectos sembrados + 19 pruebas de comportamiento, todas en
verde, y las cuatro nuevas (HO3, HO4, F13c, CAT) verificadas MORDIENDO con el defecto repuesto
en una copia — la copia hereda el 444 del blindaje, así que va con `chmod u+w`. HO2 se quedó en
verde ante el sabotaje de HO3, que es lo correcto: son hermanas, no la misma. -->

<!-- skill v1.9 (GCA1.9) — 2026-09-02 — nueva seccion "Dos alcances, dos frases": FER pidio
poder auditar SOLO la configuracion general sin que la corrida entre a leer los 12 productos
(o al reves, solo productos), y no tener que reexplicarlo cada vez. No hacia falta una skill
nueva: los bloques ya estaban separados en controles.md (bloque F = contenido de producto,
el resto = estructura/config). Se documenta la convencion de dos frases disparadoras y que
alcance de bloques activa cada una, con la cobertura declarando "fuera de alcance" en vez de
omitir el bloque en silencio. Pendiente de implementar en auditar.py: hoy el recorte de
alcance es una instruccion para quien ejecuta la skill (leer solo los bloques que tocan), no
un flag del script -- --alcance config|productos en auditar.py queda como fila declarada. -->

<!-- skill v2.5 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA, orden de FER): control F14 NUEVO — los 13 anteriores buscaban huecos (F3) y fugas de otra cuenta (F4), y la PLANTILLA DE FÁBRICA no es ninguna de las dos: es de Chatea y se ve configurada, así que un espacio entero sin tocar salía sano. Sembrado en el banco con su sabotaje y contraprueba. Retirada la copia de la description del cuerpo. Historial en references/changelog.md. -->

<!-- skill v2.3 (GCA2.3) — 2026-09-05 — LA SKILL GUARDA EL ESTANDAR, NO A LOS CLIENTES.
FER: "en esta skill no puede haber informacion de ningun VIP, ningun miembro ni mio... aqui no
deberia haber informacion de alumnos ni de nada que corrio. Eso es en cada chat." Medido: la
skill llevaba 13 datos de espacio concreto — `user_ns` de dos workspaces en SKILL.md, changelog,
controles.md, `auditar.py` y el asset de asistentes esperados, mas el nombre de un cliente, el de
una marca de producto y la ruta al deposito de tokens. No entraron de golpe: entraron como
JUSTIFICACION ("medido contra el espacio de tal cliente"), que es exactamente la forma en que se cuela
lo que no deberia estar. Se generalizaron todos: la leccion se queda, la identidad sale.
Y como una regla sin instrumento es decoracion, se agrego `scripts/sin_datos_de_cliente.py`:
caza identificadores de espacio, dominios de tienda, correos, telefonos y credenciales; trae su
propia autoprueba en los dos sentidos (4 casos malos + control negativo sobre texto sano) y corre
DENTRO de `autoprueba.py` como prueba PRIV. Sus propios ejemplos se arman en tiempo de ejecucion
para que el archivo del guardia no lleve datos con forma real y no haya que exceptuarlo — la
unica excepcion es `autoprueba.py`, que fabrica un espacio roto por diseno, y esta escrita con su
razon. Declarado y NO cubierto por codigo: los NOMBRES propios, que solo los caza leer.
Medido al cerrar: guardia 0 hallazgos · autoprueba 31/31 + 16 de 16 · simulador 7 de 7. -->

<!-- skill v2.2 (GCA2.2) — 2026-09-05 — EL ALCANCE YA ES CODIGO, Y SU DEFECTO ES CONFIGURACION.
FER lo dijo sin rodeos: "esta skill es exclusivamente para analizar configuracion, configuracion
de asistentes, no vemos productos". Desde GCA1.9 la seccion "Dos alcances, dos frases" prometia
el recorte y advertia que lo aplicaba A MANO quien ejecutaba: `--alcance` llevaba tres semanas
como fila declarada. Ahora existe: `--alcance config|productos|todo`, con **config por defecto**.
Tres decisiones de diseno, todas medidas: (1) el filtro se aplica SOBRE EL HALLAZGO y no al leer
los campos, para que todos los controles sigan corriendo y el inventario no mienta (recortar la
lectura habria hecho que el informe dijera 78 campos donde hay 95). (2) Lo apartado se DECLARA en
la cabecera con su conteo y su reparto de severidades — un rojo de producto sigue contando, solo
que no se juzga aqui. [🔴 CORREGIDO EN v2.6, 2026-09-08: el reparto de severidades se RETIRO.
Un conteo se obtiene sin mirar, pero una severidad exige haber juzgado el campo, que es justo
lo prohibido: decir "3 fuga" sobre productos ya es auditarlos. Hoy se declara CONTEO Y NADA MAS.
Esta linea era la causa raiz de las dos reincidencias que FER corrigio el 05-sep.] (3) Que cuenta como campo de producto vive en `assets/campos-de-producto.json`,
no en el criterio del momento, y el DISPARADOR queda del lado de configuracion porque es cableado,
que es la misma linea que se trazo en el paquete del 28-ago. Orden respetado: la prueba ALC se
sembro primero y fallo (`TypeError: alcance`), y de paso el primer intento de prueba dio un falso
negativo por contar solo `[Producto Ventas Wp]` — se afino a usar el MISMO predicado que el codigo.
Medido al cerrar: autoprueba 31/31 + 15 de 15 · Golden 09-04 da 25 hallazgos de configuracion con
11 apartados y declarados, contra 35 con `--alcance todo`. -->

<!-- skill v2.1 (GCA2.1) — 2026-09-05 — B8, EL DEFECTO QUE EL CATALOGO ESTABA TAPANDO.
La skill se habia corrido siempre contra UN solo espacio, asi que A3 (pais
contra moneda) y F12 (criterio de pais heredado) nunca habian disparado en campo. Se extrajo y
audito un SEGUNDO espacio, de otro pais: A3 corrio con MEXICO contra MXN y no encontro
contradiccion (el control ya no es teorico, pero un caso consistente no prueba que muerda: eso
sigue cubierto solo por la autoprueba), F12 sigue NO_VERIFICADO por ser lectura humana.
Lo que si aparecio al comparar los dos espacios fue un defecto que llevaba diez versiones en
frente de la skill: **el mismo asistente escrito de dos formas** — `[Logistico]`/`[Logistico]`
con tilde y `[WhatsApp IA]`/`[Whatsapp IA]` —, presente en LOS DOS espacios. No se reportaba
porque alguna version anterior metio las dos variantes en `PREFIJOS_CONOCIDOS` y B3 solo mira
lo que NO esta catalogado: **el catalogo se uso para callar la anomalia en vez de reportarla.**
Arreglo: control B8, que normaliza los prefijos sin tildes ni mayusculas y reporta la colision
AUNQUE las dos variantes esten catalogadas. Orden respetado: el caso malo se sembro primero en
`autoprueba.py` (defecto 31 + prueba de comportamiento 14), se comprobo que FALLABA, y solo
despues se escribio el control. Medido al cerrar: autoprueba 31/31 + 14 de 14; B8 dispara 2
veces en cada uno de los dos espacios reales. Leccion de clase para todo el arsenal: **una
lista blanca que crece para silenciar hallazgos deja de ser catalogo y pasa a ser alfombra.** -->

<!-- skill v2.0 (GCA2.0) — 2026-09-05 — auditoria fresca con el mandato del 2026-09-03 (validador
PRIMERO y auto-evaluacion del auditor antes de juzgar). Compuerta `validar_arsenal.py`: PASA (name
coincide con la carpeta, description 1.013 de 1.024 duros). Cuatro arreglos, ninguno critico:
(1) CONTEXTO BARATO: el changelog ocupaba 158 de 401 lineas del SKILL.md — el 39% del archivo que
se carga ENTERO en cada invocacion, y la historia no hace falta para ejecutar. Las 9 entradas
antiguas se MUDARON a `references/changelog.md` (nada se borra: se muda); se quedan arriba el acta
del Centro de Mando y la entrada vigente, que es lo que un editor necesita ver antes de tocar.
SKILL.md 401 → 257 lineas. (2) CIFRA DESINCRONIZADA: `controles.md` I1 decia "30 defectos + 11
pruebas de comportamiento" y la corrida real da **13**. El propio I1 advierte que si los dos sitios
no se actualizan "el informe siguiente miente sobre su propia cobertura" — la skill habia escrito
la regla y la incumplia. Corregida, y ahora la cifra se comprueba corriendo, no de memoria.
(3) PROMESA QUE EL CODIGO NO CUMPLE: la seccion "Dos alcances, dos frases" prometia que la
cobertura y el paquete declaran `no_corrido: fuera de alcance`, y `auditar.py` no conoce
`--alcance` (cero menciones). El aviso de que el recorte es MANUAL vivia solo en el changelog —
historia que nadie lee al ejecutar. Ahora lo dice la propia seccion. (4) El simulador de dias no
estaba en el criterio de "terminado": la autoprueba valida el DETECTOR y `simular_dias.py` valida
el CICLO; hacen falta los dos, y ahora los dos estan en el bloque de comandos de la Fase 4 y en I1.
Medido al cerrar: autoprueba 30/30 + 13 de 13, simulador 7 de 7 dias, validador en norma,
inventario sin rotas ni huerfanas, 0 dudosos. -->

skill v1.8 (GCA1.8) — 2026-08-26 — SIMULACION DE DIAS en vez de esperar los dias.
El ciclo de vigilancia (auditoria → decision → cambio → re-medicion) se iba a validar dejandolo
correr unos dias reales; eso cuesta dias y descubre los fallos EN PRODUCCION. Se construyo
`scripts/simular_dias.py`, que corre el ciclo sobre un espacio que EVOLUCIONA (alguien corta un
campo desde el panel, un campo cruza el techo, se borra un campo, la API falla un dia, se
enciende pauta). Encontro el fallo de fondo el primer intento: **`reabrir_si` era PROSA que
nadie evaluaba** — solo se imprimia. La decision de los huerfanos dice "reabre si se les carga
un id de anuncio" y el dia que se cargara habria seguido silenciada: la promesa de que el libro
no es una alfombra no la sostenia nada. Arreglo: la decision guarda `evidencia_al_decidir`, la
foto de la situacion ese dia, y **CADUCA sola cuando la evidencia cambia** — cubre el caso
general (se cargo un anuncio, el campo crecio, aparecio otro producto) sin inventar un lenguaje
de condiciones que nadie escribiria bien. Las decisiones sin esa foto se avisan: no pueden
caducar. LECCION DEL PROPIO BANCO: el dia 7 pasaba con el arreglo SABOTEADO, porque registraba
el producto y el hallazgo desaparecia — la comprobacion se auto-aprobaba por una via que no
probaba nada. Se reescribio para que el hallazgo PERSISTA y solo cambie su evidencia. Medido:
7 de 7 dias con el arreglo vivo, 6 de 7 con el sabotaje, y el que se cae es el de la caducidad.

---

skill v1.7 (GCA1.7) — 2026-08-26 — auditoria fresca (el numero v1.6 ya
lo habia tomado otro chat el mismo dia con sus propios cambios; esta entrada es POSTERIOR). Tres defectos, dos de ellos de la
MISMA clase que la skill ya habia arreglado en otro sitio y cuyo GEMELO nadie busco.
(1) 🔴 LA SEVERIDAD IGNORABA EL `estado` DE LA ENTRADA: 8 de los 14 hallazgos del bloque D
gritaban sin mirarlo, 5 de ellos en rojo. Medido en Golden y reportado por la verificacion
adversarial: 4 de las 5 entradas del disparador de Remarketing estan `inactivo` en el servidor y
salieron en 🔴 igual — la evidencia hasta imprimia "estado 'inactivo'" y el codigo no lo leia. El
cuadro real no era "el disparador entero roto" sino UNA entrada activa mal cableada y cinco
apagadas de basura. Es el gemelo exacto de la regla que ya existia para los huerfanos (la
severidad la decide el negocio, no la estructura). Helpers `activa` / `sev_segun_estado` /
`nota_estado`, y las entradas al vacio se separan en ACTIVAS (rojo) e INACTIVAS (duda de
limpieza). (2) 🔴 EL LIBRO DE DECISIONES SE ROMPIO HACIA ATRAS EN SILENCIO: la huella corta
`::hash` que se anadio para que una decision no silenciara 5 hallazgos a la vez cambio la forma
de la clave, y 4 de las 6 decisiones ya escritas dejaron de casar — sus hallazgos volvieron a
gritar como si nadie los hubiera resuelto. Una clave que cambia de forma con una mejora del
codigo no es una clave estable, y el libro entero vale por su estabilidad. Ahora se aceptan las
DOS formas: FINA (`control|campo::huella`, silencia uno) y AMPLIA (`control|campo`, silencia
todos los de ese campo), y el informe AVISA cuando una decision amplia silencia mas de uno.
(3) 🟡 A4 leia mal su propio endpoint: `/workspace-settings/channels` dice que canales estan
DISPONIBLES en el plan (1/0), no si estan conectados. `apple: 0` — un canal que el plan de
Golden no incluye y que ningun asistente usa — salia en 🔴 MUERTO. Ahora solo dispara si falta
un canal REQUERIDO (whatsapp, whatsapp_cloud, facebook, instagram) y declara que la conexion
viva se mira en el panel, que es lo que ya dice A5. Autoprueba: 30 defectos + 12 pruebas de
comportamiento (EST y LIB nuevas).

---

skill v1.6 (GCA1.6) — 2026-08-25 — verificacion adversarial (golden-verificador) contra el
un espacio REAL en produccion: ocho hallazgos, los ocho con su caso malo sembrado
en autoprueba.py ANTES de arreglar el codigo. (1) A4 no evaluaba NINGUN canal real: el endpoint
real trae enteros anidados bajo `data` (`{"data":{"whatsapp":1,...}}`) y el codigo solo
reconocia booleanos o strings "connected/active/ok" — lo unico que disparaba era el
`status:"ok"` del SOBRE HTTP, no un canal. Corregido para leer la forma real, con el fixture
reproduciendola. (2) E3 (credencial de voz heredada) NUNCA podia disparar contra un DUMP real:
comparaba `api_key` contra el string YA REDACTADO por extraer.py (`<<REDACTADO...>>`), que
siempre falla esa condicion — el fixture viejo probaba una forma en claro que el auditor real
jamas recibe. Ahora el control juzga si HABIA algo que redactar, no si sigue en claro. (3) El
paquete `--handoff` filtraba por "¿tiene `accion`?" ANTES de mirar la severidad: 22 de 39
hallazgos abiertos no llegaban al paquete en la corrida real, 5 de ellos rojos de un solo
disparador y 11 fugas de credenciales. Ahora todo 🔴 o 🟠 entra siempre, tenga o no `accion`.
(4) La clave del libro de decisiones (`control|objetivo`) no era unica cuando un mismo campo
acumulaba varios hallazgos distintos sin `objetivo` explicito (`D3|[Remarketing IA]...` cubria
5 hallazgos de una sola vez; `F3|[Producto Ventas Wp] 8` mezclaba un rojo con un azul bajo la
misma clave): una decision del dueno podia silenciar mas de uno sin que nadie lo notara. Se
afina con una huella corta de la evidencia cuando no hay `objetivo` (los agregados deliberados,
como `huerfanos-con-pauta`, siguen con su clave estable de siempre). (5) El diff (`--anterior`,
J1) mostraba el largo crudo del JSON prominente y solo el DELTA como "escapados": un campo cerca
del techo no tenia forma de leer su escapado absoluto real. Ahora muestra el escapado real
primero (`ea → en escapados`) y el crudo aparte, marcado. (6) Varios controles se declaraban
"corrido" sin denominador o sin ejecutar su medida real: B2 (el limite de campos de usuario no
lo expone la API — ahora NO_VERIFICADO siempre, nunca "corrido"), A1 (sin denominador, ahora
`1 endpoint`), B4 (contaba objetos sin declarar cuantos ni cuales, ahora lo declara), G2 (solo
hacia una pregunta y se marcaba "corrido" como si hubiera verificado algo — ahora NO_VERIFICADO
con la evidencia encontrada). Y F4/F12/I1 estaban en `A` en controles.md pero el codigo los
reporta NO_VERIFICADO (lectura humana): sincronizados a `H`. (7) Cifras de la autoprueba
desincronizadas entre SKILL.md y controles.md: quedan en **30 defectos + 11 pruebas de
comportamiento** en los dos lugares (las 4 nuevas: J1b escapado real, CLV colision de claves,
HO2 severidad en el handoff, I3B4 sincronia de la lista de endpoints auditados). (8) La lista
`auditadas` de I3 (bloque_i) vivia hardcodeada y desincronizada de lo que B4 realmente audita:
decia que subflows/tags/ai-agents/ai-tasks/inbound-webhooks/segments/agents no tenian control
cuando B4 ya los contaba — 7 falsos positivos. Ahora ambas comparten la constante
`ENDPOINTS_B4`, una sola lista para los dos lectores.

---

skill v1.5 (GCA1.5) — 2026-08-22 — PRIMERA lectura profunda de los 12 prompts de
producto en campo: los controles F4/F9/F10/F11/F12 estaban escritos desde el primer dia y NUNCA
se habian ejercido. Encontraron un defecto REAL en produccion que el auditor no veia:
un `[Producto Ventas Wp] N` ACTIVO y registrado en el disparador llevaba
`[AQUI VAN LOS DATOS DE PAGO ANTICIPADO: Nequi/Daviplata + titular]` en pleno paso de cobro. La
lista de placeholders conocidos (`[NOMBRE`, `TU_TOKEN`...) no lo cazaba — el mismo modo de fallo
que esta skill le prohibe a los demas: el detector solo mira donde le sembraron el defecto.
Ahora F3 caza la CLASE, en DOS niveles de confianza MEDIDOS contra los 12 productos reales:
verbo de encargo (AQUI VA, PONER, FALTA, COMPLETAR, REEMPLAZAR) = rojo si el producto esta
activo; corchete en mayusculas sostenidas = DUDA, porque 3 de cada 4 eran plantilla viva del
motor de Producto en Segundos ([CATEGORIA], [NOMBRE ASESORA]) y un auditor que acusa 3 falsos de
4 le ensena al dueno a ignorarlo. El corchete de variable en minusculas ([total]) no dispara.
F3 mira las HOJAS DE TEXTO, no el JSON crudo: aplicado al crudo, el `[` que abre un array
fabricaba falsos positivos en los dos disparadores. Mismo criterio en la zona de agentes y
tareas de IA. Autoprueba: 30 defectos + 7 pruebas de comportamiento.
NOTA DE PROCESO: el turno que iba a escribir esta entrada se corto por un AbortError del canal
de permisos, y la skill quedo con el codigo de GCA1.5 y el SKILL.md diciendo GCA1.4 — el censo
diario no habria visto la edicion. Leccion: la version se escribe en el MISMO comando que el
ultimo cambio de codigo, no en uno posterior.

---

skill v1.4 (GCA1.4) — 2026-08-22 — auditoria golden-skill-auditor (850 PLATA), pasada
fresca. Lo grave era del MISMO tipo que esta skill le prohibe a los demas: (1) B7 y J2 estaban
declarados en el catalogo como controles automaticos y NO aparecian en la tabla de cobertura —
invisibles en el informe, gemelo exacto del hallazgo I4 que arreglo el Centro de Mando en
GCA1.1; ahora los dos se declaran, y J2 dice cuantos hallazgos silencio el libro. (2) La
plantilla de references/informe.md estaba VIEJA respecto al codigo: no contemplaba las secciones
"que cambio desde la corrida anterior" ni "ya decidido por el dueno", asi que quien la siguiera
entregaba un informe sin el diff ni las decisiones. (3) El helper `escapado()` estaba muerto Y
media DISTINTO que el codigo real (doble codificacion) — un helper que mide distinto es una
trampa para el proximo editor, no una comodidad: borrado, con la formula unica documentada.
(4) La cifra de la autoprueba decia 29 en SKILL.md y en controles.md y son 30 + 6. (5) El ns
real del espacio auditado salio de los ejemplos (estandar 5: nada de IDs de cuenta en una skill
que se comparte) y la receta del libro de decisiones dejo de estar duplicada: vive solo en el
bloque J. (6) Nueva seccion "Conexion con el ecosistema" (estandar 9): cada cierre se reporta al
Centro de Mando, haya hallazgos o no, y se declaran las dependencias. (7) La cobertura se
imprime ordenada por control, e `import subprocess` muerto fuera.

---

skill v1.3 (GCA1.3) — 2026-08-21 — re-auditoria: los arreglos de GCA1.2 metieron sus
propios defectos, encontrados probando la skill contra casos que se saben malos. (1) ROBUSTEZ:
un endpoint que respondia con error (dict en vez de lista) tumbaba la auditoria entera con un
traceback — un 500 puntual de la API costaba el informe completo; ahora se declara la zona como
no medida y se sigue (control B7). (2) El asset de asistentes esperados ausente reventaba igual:
ahora degrada. (3) La regla escrita "una decision sin motivo y sin fecha no se acepta" NO la
aplicaba el codigo: se aceptaba en silencio y se imprimia "(sin motivo)". Ahora detiene la
corrida, y avisa de las decisiones sin `reabrir_si`. (4) El handoff descartaba las dudas
accionables: 5 hallazgos con accion concreta quedaban fuera del paquete; ahora abren el
documento como "preguntas que hay que contestar antes de tocar", con su clave para el libro.
Autoprueba: 30 defectos + 6 pruebas de comportamiento.

---

skill v1.2 (GCA1.2) — 2026-08-21 — auditoria golden-skill-auditor (874/1000) mas
simulacion de cliente: la skill diagnosticaba bien y COMUNICABA mal. Seis arreglos.
(1) LIBRO DE DECISIONES `--decisiones`: cada hallazgo tiene clave estable control|objetivo y lo
que el dueno ya resolvio sale aparte con motivo y fecha — antes cada corrida repetia los mismos
40 hallazgos, incluido uno que FER ya habia descartado. (2) SEVERIDAD POR NEGOCIO: un producto
huerfano CON anuncios es rojo y SIN anuncios es duda; era el criterio del dueno y no estaba en
codigo. (3) DIFF `--anterior`: que se movio desde la corrida pasada, con alerta si un campo
cruzo el techo. (4) B6 asistentes ESPERADOS contra instalados (assets/asistentes-esperados.json),
que es lo unico que contesta "esta completa esta instalacion". (5) HANDOFF `--handoff`: paquete
de correccion agrupado por la skill duena de cada campo. (6) Cerrada la contradiccion del techo
entre SKILL.md, controles.md y el codigo — una sola verdad, con los dos umbrales medidos — y
documentados los dos assets. Autoprueba de 29 a 30 defectos mas 4 pruebas de comportamiento
(negocio, libro, diff).

---

skill v1.1 (GCA1.1) — 2026-08-21 — auditoría golden-skill-auditor: I4 (controles.md:122,
"ausencia no es prueba") estaba definido pero auditar.py nunca lo reportaba en la cobertura —
quedaba invisible en el informe final, justo el modo de fallo que esta skill le prohíbe al
bloque D. Se agregó self.cubre("I4", ...) en bloque_i. También se documentó B1b en
controles.md (existía en el código sin entrada en el catálogo) y se reordenó F12/F13 a orden
numérico. Ver detalle completo debajo.

---

skill v1.0 (GCA1.0) — 2026-08-20 — versión inicial declarada por el Centro de Mando: la
skill nació sin CHANGELOG y sin número, y sin versión el censo diario no puede ver que alguien
la editó.

---


## v2.5 · 2026-09-07 · auditoría golden-skill-auditor (AUDITA+ARREGLA), orden directa de FER

### 1 · 🔴 F14 · LA PLANTILLA DE FÁBRICA — el hueco más grande que tenía este auditor

Los 13 controles buscaban **dos cosas**: huecos sin llenar (F3: `{{`, `TU_`, marcadores) y fugas de
**otra cuenta** (F4). **El contenido de fábrica no es ninguna de las dos.** Es de Chatea, no de
otro cliente, y no parece un marcador: **parece configuración.**

Medido el 2026-09-06 contra la API en dos espacios recién creados: **61 de 61 campos idénticos
byte a byte** entre uno nacido en Colombia y otro creado eligiendo México. **Nace colombiana elijas
el país que elijas.**

Con los 13 controles, **un espacio entero sin tocar salía SANO en esta dimensión** — con su
teléfono de relleno, su asesor llamado Santiago, dos biografías falsas y contradictorias (5 años en
el logístico, 7 años y 3.000 clientes en comentarios, en el mismo espacio) y la ley colombiana
citada en la garantía de un negocio que no es colombiano. Todo eso en un panel donde se ve bien.

Esta es **la skill que dictamina si una instalación está sana**. Que no mirara lo que la plataforma
escribe por defecto es el defecto más caro de la ronda.

**Cómo mide:** por el VALOR, contra la huella md5 de los 61 campos que vive en la hermana logística.
**La bandera `is_template_field` de la plataforma NO SIRVE**: viene en falso en 9 de cada 10 campos.
Si la huella no está disponible, F14 se declara **NO CORRIDO** — no se calla ni se da por sano.

### 2 · Sembrado en el banco, con su sabotaje y su contraprueba

El caso F14 toma el valor **de la huella real**, no inventado: si se inventara, la prueba
comprobaría que el auditor reconoce una cadena de mentira en vez de la plantilla que la plataforma
instala de verdad. Contraprueba: desactivado el bloque en una copia, el banco falla nombrando F14.

### 🔴 Y volví a equivocarme sembrando

La primera versión metió el campo de fábrica **entre los ENDPOINTS del dump**, no entre los campos.
El auditor no mira ahí, así que no disparó — y el informe dijo *"el auditor NO detecta F14"*,
acusando a un control que estaba bien. **Un fallo del banco y un fallo de la herramienta se ven
igual desde fuera**, y es la cuarta vez en el día que me pasa. Se comprueba SIEMPRE dónde mira la
herramienta antes de concluir que no ve.

### 3 · Había una copia de la `description` en el cuerpo

Con el rótulo de conservarla *"para no perder ningún matiz"*. Es el mismo defecto encontrado hoy en
`golden-chatea-pro-producto-comentarios`, y la regla ya está escrita en `config-ventas-wp`: esa
clase de copia **envejece y acaba contradiciendo a la description viva** — así se coló el dato
falso de "7 países" en una hermana. Retirada; lo que es frontera se escribe como frontera.

## 2026-09-07 · CUPO DE LA API: se lee, se avisa y se frena antes de gastarlo

**Pregunta de FER, y el desarrollador de Chatea tenía razón:** el API limita a **1.000 peticiones
por hora** y pasarse **bloquea una hora entera**. La respuesta trae el contador de las que quedan.

**MEDIDO contra la API viva** (una lectura real, no documentación):

    x-ratelimit-limit: 1000
    x-ratelimit-remaining: 999

En inglés: **X-RateLimit-Limit** y **X-RateLimit-Remaining** — "las peticiones que quedan".

🔴 **Hasta hoy NINGUNA de las diez skills de la familia leía ese contador.** Se trabajaba a
ciegas: se arrancaba una operación cara sin saber si cabía, y el bloqueo aparecía **a mitad**, con
el inventario incompleto o la configuración escrita por la mitad.

**Coste medido de una auditoría completa: 137 peticiones** (espacio de referencia casi vacío: 61
bot fields, 6 agentes IA, 45 tareas IA; uno de cliente cuesta más). **Con 1.000/hora caben ~7.**

**Qué se cableó:**
· El contador se lee de **cada** respuesta — viaja gratis en la cabecera que ya llegó — y se
  **dice** al terminar, con cuántas operaciones más caben.
· **Comprobación previa** antes de una operación cara: cuesta 1 petición saberlo antes y cuesta
  una hora averiguarlo después.
· Ante un **429 no se reintenta**: reintentar sobre un bloqueo lo alarga. Se declara qué quedó a
  medias, porque ni el panel ni un inventario parcial lo delatan solos.
· Herramienta de casa nueva: **`golden-chatea-cupo [token] [--necesito N]`**, que responde en una
  sola petición si cabe lo que se va a hacer.

⚠️ **Límite declarado:** la respuesta **NO trae `x-ratelimit-reset`**. El servidor **no dice
cuándo** se repone el cupo. La ventana es de una hora; si es fija o deslizante **no está medido** y
no se afirma. Lo único seguro es el número que queda AHORA.

## v2.6 · 2026-09-08 · LA FRONTERA CERRADA (orden de FER, tras dos reincidencias el mismo día)

### 1 · 🔴 El recorte por alcance le estaba OCULTANDO configuración a FER

Lo cazó el `golden-verificador` sembrando un sabotaje: cambió la palabra clave del producto 3 y
**D1 no salió en `hallazgos`, salió en `fuera_de_alcance`**.

**Causa:** el filtro casaba `es_campo_de_producto(h["campo"])` — el NOMBRE del campo — sin mirar
qué juzga el control. Como D1 apunta a `[Producto Ventas Wp] N`, se archivaba. Y el `SKILL.md`
decía literalmente lo contrario: *"el disparador NO entra ahí: nombra productos, pero es cableado
del asistente, o sea configuración"*.

**Le da la vuelta a la queja de FER.** Él no pedía menos de lo que necesitaba: pedía lo correcto,
y la herramienta no se lo entregaba entero. **Medido en el banco: de 12 hallazgos apartados, 8
eran CABLEADO suyo** — incluido un desajuste de palabra clave que deja un producto sin arrancar.

**Corregido:** el filtro va por lo que el control JUZGA. Conjunto `CABLEADO` explícito (D1-D6,
C1-C6, E3, G3) que sale siempre, aunque apunte a una ranura de producto.

### 2 · La aserción que no mordía, y me la encontré yo

Reescribí el caso `alcance-config` para la frontera nueva… y **la contraprueba pasó en verde con
el defecto repuesto**. Mi aserción solo exigía que el CONTENIDO no se colara, no que el CABLEADO
**sí saliera**. Un banco que no muerde ante el defecto que existe para cazar no vale nada.
Añadida la aserción positiva: **D1 tiene que estar en `hallazgos` y NO en `fuera_de_alcance`**.
Ahora la contraprueba falla como debe: *"D1 en config=0 (debe ser >0) · D1 apartado=2"*.

### 3 · `assets/campos-de-configuracion.json` (NUEVO) — la lista que faltaba

Hasta hoy **la configuración se definía POR EXCLUSIÓN**: solo existía `campos-de-producto.json`
con 4 patrones, y todo lo demás se asumía configuración. Consecuencias: nadie había listado nunca
qué campos son configuración, y **un campo nuevo que Chatea añadiera mañana entraba como
configuración sin que nadie lo decidiera**. "Auditar la configuración" no tenía denominador.

El asset nuevo lo cierra, **con evidencia, no con deducción**: sale de las capturas del panel vivo
que FER entregó el 2026-09-08, pantalla por pantalla del asistente de Ventas WhatsApp, más los dos
bot fields JSON abiertos en el editor. **Ventas WhatsApp queda completo** (6 secciones mapeadas a
sus llaves); comentarios, logístico y carritos esperan sus capturas y así está declarado.

Y la regla que evita que el hueco vuelva: **un campo que no esté en ninguna de las dos listas NO
se asume configuración — se declara como sin clasificar.**

### 4 · La frontera, escrita donde se lee

> **Un control de configuración que APUNTA a un campo de producto mira el CABLEADO del campo,
> JAMÁS su CONTENIDO.**

Cableado: si la ranura está registrada en el disparador, si la palabra clave coincide byte a byte,
si está activa, cuánto ocupa, si lleva una credencial. Contenido: qué producto es, su marca, su
precio, sus imágenes, si sus anuncios viven. **Abrir el JSON del producto para "confirmar" un
hallazgo de configuración es donde se cayeron los dos chats** — y no hacía falta.

### 5 · La regla del asset, CABLEADA (antes existía y no hacía nada)

`campos-de-configuracion.json` nació el 08-sep y **nada lo leía**: los campos huérfanos seguían
saliendo como una duda B3 genérica *"no pertenecen a ningún asistente"*. Lo señaló el chat de Dolce
sobre su corrida real: 7 campos (`Pedidos_Diarios`, `TODAY_PROV`, `TOKEN DROPI`, `Tipo de
referencia`, `Today_previo`, `YA PAGUE`, `recordatorio_general`).

B3 ahora los declara **SIN CLASIFICAR**, con la regla escrita en el hallazgo: *"NO se asumen
configuración: un campo que nadie clasificó no es config por defecto"*, y con la acción concreta
—clasificarlo en uno de los dos assets o declararlo fuera de alcance con su motivo—. Un asset que
nadie lee es documentación, no un guardarraíl.

### Confirmación en campo del arreglo del filtro

El chat de Dolce rehizo la corrida **sobre el mismo DUMP, sin gastar cupo**: de **25 hallazgos a
36**, y de **12 apartados a 1**. Lo que estaba archivado y era cableado: un **C1** con
`[Producto Ventas Wp] 2` en **20.163 escapados** contra los 19.895 que matan al asistente, y la
ranura **registrada y ACTIVA en el disparador**; C2/C4 de tres ranuras al 96%, 97% y 106%; C3 con
dos `desc` de 3.973 y 4.572 sobre un tope de 500; E3 con una credencial de voz dentro de una
ranura; F7 con 6 imágenes de otra cuenta. **Todo eso es configuración, y llevaba archivado.**
