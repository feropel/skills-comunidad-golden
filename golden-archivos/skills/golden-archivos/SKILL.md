---
name: golden-archivos
description: >-
  Golden Group — ORGANIZADOR DE BIBLIOTECAS DE ARCHIVOS. Toma control de carpetas caóticas
  (productos, creativos, marca, informes) y las deja coherentes: clasifica por tipo, pone
  nombres auto-descriptivos con el producto adentro, separa el material WEB listo para subir
  de los originales HD, aplica la regla anti-mezcla (ninguna carpeta con archivos sueltos al
  lado de subcarpetas), reubica lo que está en el producto equivocado y elimina duplicados
  reales, todo con log reversible y verificación VISUAL antes de borrar. Úsala SIEMPRE que
  el usuario quiera organizar, ordenar, limpiar, clasificar o auditar archivos y carpetas:
  "organiza mi escritorio", "acomódame estas carpetas", "esto está hecho un desastre",
  "tengo archivos duplicados", "no sé qué es este archivo", "revisa que todo esté en su
  sitio", "clasifica estas fotos o videos", "separa lo que subo a Shopify de los
  originales", "hay imágenes repetidas", "esto no va en esa carpeta", o cuando arrastre una
  carpeta suelta pidiendo que la ubique.
---

**Fábrica:** chat «✅ SKILL golden-archivos»
<!-- CENTRO DE MANDO · 2026-09-03 · PUESTA EN NORMA DEL ARSENAL (mandato de FER: "arregla todas las skill para que queden perfectas y estos errores no pueden volver a pasar nunca mas").
     QUE SE LE HIZO A ESTA SKILL: (2) DESCRIPTION puesta dentro del tope DURO de la especificacion: hoy mide 1004 caracteres (tope 1024). Antes se pasaba, y lo que se pasa se TRUNCA: los disparadores del final son los mas nuevos y son los primeros en perderse · (3) Lo que sobraba NO SE BORRO: la parte de fronteras y desambiguacion BAJO AL CUERPO, a la seccion '## Fronteras y desambiguacion', que no tiene tope duro. Los disparadores se quedaron arriba, que es lo que hace que la skill dispare.
     POR QUE NADIE LO HABIA VISTO: 'golden-skill-auditor/scripts/inventario.sh' MEDIA la longitud de la description y la IMPRIMIA, pero NUNCA la comparaba contra un tope ('1024' aparecia cero veces en sus scripts). Medir no es comparar: un numero sin vara al lado no es un chequeo, es decoracion. Por eso 33 skills de la casa quedaron fuera de norma, varias selladas ORO.
     QUE LO IMPIDE AHORA: 'golden-skill-auditor/scripts/validar_arsenal.py' compara contra los topes REALES de agentskills.io/specification y contra las reglas duras de FER (sin signos de apertura, sin acentos rotos, sin rayas separadoras, lenguaje de EMPRESA), revisa ademas que la skill este BIEN CONECTADA, y tiene su propia autoprueba de 26 casos en las dos direcciones. Compuerta dura en la rubrica: una skill que no lo pase NO puede pasar de 700/1000.
     COMO COMPROBARLO TU MISMO: python3 ~/.claude/skills/golden-skill-auditor/scripts/validar_arsenal.py <ruta-de-esta-skill>   (salida 0 = en norma)
     SI ALGO DE ESTO CHOCA CON TU DISENO, dilo al Centro de Mando y se revierte: hay respaldo. -->
# Golden Archivos — orden de bibliotecas de archivos

<!-- skill v1.22 · 2026-09-27 · EL DETECTOR DE NOMBRES CRIPTICOS ENCONTRABA EL 12%. Medido por un agente sobre un archivo real de 689 piezas: `auditar.sh` reporto **44 cripticos y habia 361**. El patron cubria `IMG_*`, `DSC*`, `Captura*`, `RPReplay*`, `ChatGPT Image*` y los UUID, y se dejaba fuera justo lo que llena un disco de verdad: `WhatsApp Image…`, `_MG_####` de Canon, `PXL_*` de Pixel, `IMG-*` con guion, ids numericos de Facebook de 10+ digitos, `Screenshot`, `Untitled`, `descarga (1)`, `banner-#####`, `wetransfer-*`. ESTO ES PEOR QUE NO TENER EL DETECTOR, y por eso entra con candado: `auditar.sh` es la herramienta que arma LA LISTA DE TRABAJO al abrir una carpeta. Si encuentra 44 de 361, la lista sale ocho veces mas corta que el trabajo y **quien la sigue cree haber terminado**. No es un cero falso — esos ya los persigue la skill desde la v1.7 — es algo mas dificil de ver: **un numero que parece un hallazgo**. Un detector que encuentra el 12% no es un detector, es un muestreo presentado como total. Arreglo medido: de 6 formas a 24, y cada una aparecio DE VERDAD en este disco. CANDADO, la asercion 14: siembra las 14 formas reales MAS un nombre sano (`TAG RECEDE - demo cuello 01.jpg`) y exige las dos cosas a la vez — exactamente 14, ni una menos, y que NO acuse al sano. Las dos juntas porque ensanchar el patron hasta acusar a los nombres buenos vuelve la lista inservible por el otro lado, y ese error ya lo cometi hoy dos veces: la asercion 8 acusaba a `duplicados.sh` por limpiar sus temporales, y mi barrido de "Read" dio 129 sospechas de las que casi todas eran ruido. Probada en las tres direcciones: sano 20 de 20 · devolver el patron viejo muerde y dice cuantas de 14 encontro · y ensancharlo a `-iname '*'` muerde tambien, por acusar al nombre sano. LECCION: **una herramienta que produce LISTAS DE TRABAJO tiene que declarar su cobertura igual que una que produce veredictos.** El mosaico dice "N de M piezas" desde la v1.6; el auditor decia "total: 44" sin decir sobre que universo, y 44 sobre 689 se lee como un hallazgo completo cuando es una muestra. -->
<!-- skill v1.21 · 2026-09-27 · EL ARREGLO DE LA v1.19, APLICADO A LA HERRAMIENTA DE AL LADO, ROMPE. La v1.19 exigio `-nostdin` en todo ffmpeg porque sin el se come la lista del bucle. Horas despues, un agente midiendo 178 videos descubrio la otra mitad: **`ffprobe` NO acepta `-nostdin`**. Se traga el argumento SIGUIENTE y hace otra cosa, sin decir que el argumento era malo. Medido aqui sobre un mp4 real: `ffprobe -nostdin -v error -show_entries format=duration ...` imprime el BANNER DE VERSION; la misma linea sin el y con `</dev/null` imprime `10667.375000`. Al agente le devolvio **NA en los 178 videos, sin un solo error**: si no llega a mirar la salida, habria clasificado doce horas de grabacion con duracion desconocida y nadie se entera. Esta skill no usa ffprobe (0 coincidencias, comprobado) y la asercion 12 busca el patron `ffmpeg`, que NO casa con `ffprobe` (comprobado pasandole una linea de ffprobe: 0 coincidencias), asi que el candado no estaba induciendo el fallo. Se arregla igual, y por la razon que importa: **un candado que EXIGE algo tiene que PROHIBIR ese algo mal aplicado**, o se convierte en la fuente del proximo fallo. La asercion 12 gana la guarda simetrica y ahora falla en las dos direcciones — si algun script llama a ffmpeg sin `-nostdin`, y si alguno se lo pone a ffprobe. Probada en las tres direcciones: sano 19 de 19 · quitar el `-nostdin` de ffmpeg muerde · y ponerselo a ffprobe muerde con su propio mensaje, que es el señuelo que importa porque es el error que comete quien aplica bien la leccion al sitio equivocado. La regla, para que quede escrita donde se ejecuta: **ffmpeg lleva `-nostdin`; ffprobe lleva `</dev/null` y JAMAS `-nostdin`**. LECCION: una leccion verdadera se vuelve falsa al cruzar de herramienta, y la version que la publica tiene la obligacion de decir donde NO aplica. Es la misma familia que `feedback_corregir_produce_el_fallo_simetrico` de la casa, esta vez con la fabrica publicando el arreglo y la trampa el mismo dia. -->
<!-- skill v1.20 · 2026-09-27 · EL HASH DEL VACIO AGRUPA LO QUE NO TIENE NADA EN COMUN, y la correccion mas util de esta version es a mi favor y en mi contra a la vez. Barriendo un respaldo real de 5.768 archivos, un script improvisado MIO reporto "16 copias" de una foto. No lo eran: eran **16 archivos de CERO bytes**, imagenes de WhatsApp que nunca terminaron de bajar, que comparten md5 porque todas estan vacias. Son 16 fallos DISTINTOS, no un grupo de duplicados, y borrar 15 "dejando la buena" deja viva otra igual de rota. LO PRIMERO QUE HAY QUE DECIR es que `duplicados.sh` YA LO HACIA BIEN: excluye los de tamaño 0 del hasheo desde siempre. El fallo fue mio por saltarme la herramienta de la skill y escribir uno a mano para ir rapido. La leccion no es sobre archivos vacios: **una skill que ya resolvio un caso no protege a quien la rodea**, y el atajo reintrodujo un fallo que la herramienta buena no tiene. Si hay tentacion de improvisar el barrido, se usa el script. PERO SI HABIA ALGO QUE ARREGLAR, y es de la clase que esta skill persigue: excluia en SILENCIO. Con 6 archivos en la carpeta imprimia "Archivos analizados: 3" y los otros 3 desaparecian sin una palabra. **16 archivos rotos en una biblioteca de fotos son un HALLAZGO, no ruido**: dicen que hubo 16 fotos que se perdieron en la transferencia. Ahora los cuenta, los nombra y explica por que no entran. Es exactamente el censo que la v1.6 le puso al mosaico ("un mosaico que calla piezas invalida la verificacion"), aplicado al deduplicador cinco versiones despues: el mismo principio faltaba en la herramienta de al lado. CANDADO, la asercion 13: siembra 3 vacios y 2 iguales y exige las tres cosas a la vez — que cuente los 3, que NOMBRE uno de ellos, y que siga reportando UN solo grupo de duplicados. Las tres juntas, porque contar sin nombrar no deja actuar y nombrar sin contar no deja medir. Probada en las tres direcciones: sano 19 de 19 · quitando el censo muerde · y el señuelo tambien, quitar el `-size 0` del `find` para que los vacios vuelvan a entrar al hasheo y se agrupen como copias. LECCION: cuando una herramienta descarta algo por una razon buena, la razon buena no la exime de DECIRLO. Lo descartado en silencio es indistinguible de lo que nunca estuvo. -->
<!-- skill v1.19 · 2026-09-27 · DOS FALLOS EN `hoja-contactos.sh`, encontrados por un agente que usaba la skill sobre una biblioteca real de 613 piezas. Los dos atacan el corazon del metodo: la hoja de contactos es COMO se cumple la ley de "abrelo y miralo", asi que una pieza que no entra al mosaico es una pieza que se clasifica a ciegas. (1) **HEIC nunca renderizaba.** `heic` esta en MEDIA_EXTS desde la v1.6, pero un HEIC es una imagen en MOSAICOS: ffmpeg le arma por dentro un filtergraph complejo y el `-vf` simple choca con el, con el error "Simple and complex filtering cannot be used together for the same stream". Reproducido aqui: 2 HEIC + 1 JPG daban "1 de 3". Importa porque el iPhone dispara en HEIC por defecto, asi que era TODA la fotografia de telefono la que quedaba fuera de la verificacion visual. Arreglo: se intenta el camino directo (rapido, sirve para todo lo demas) y solo si no produce nada se decodifica en dos pasos. Generaliza a cualquier formato con filtergraph interno, no solo HEIC. Verificado con la misma prueba que fallaba: 3 de 3, y abriendo la hoja se ve la foto de verdad, no un mosaico en blanco. (2) **`ffmpeg` se comia la lista del bucle.** Sin `-nostdin`, ffmpeg DRENA la entrada estandar, y aqui la entrada del `while read` ES la lista de candidatos: se tragaba lineas. Medido por el agente sobre su biblioteca: 85 renderizadas de 92, sin un solo mensaje de error. LO QUE SALVO LOS DOS CASOS fue el censo de la v1.6, que imprime SIEMPRE "N de M piezas renderizadas" y avisa si M>N: ninguno de los dos fallos pudo esconderse, y por eso el agente los vio en vez de dar por buena una hoja incompleta. Es la vindicacion del principio de esa version — "un mosaico que calla piezas invalida la verificacion" — y la razon de que el arreglo llegara el mismo dia. CANDADO, la asercion 12, solo para el segundo, porque es el mecanico: recorre los scripts y falla si algun `ffmpeg` corre sin `-nostdin`, en codigo vivo. El primero no lleva candado nuevo a proposito: fabricar un HEIC sintetico para el banco no se puede sin una fuente, y el censo YA muerde ese caso y lo demostro. Un candado de adorno donde ya hay uno que funciona es ruido. LECCION: la herramienta que verifica tiene que declarar su propia cobertura. Las dos veces el fallo fue invisible para quien lo miraba por encima y evidente para quien leyo el "N de M". -->
<!-- skill v1.18 · 2026-09-27 · FUGA DE LA RUTA ABSOLUTA, encontrada por el barrido de publicacion del chat ARSENAL Y SKILLS y arreglada EN ORIGEN. `scripts/_comun.sh` traia en un COMENTARIO la ruta `/Users/<usuario>/Desktop`, con el nombre de usuario del Mac de FER. Entro con la v1.15-1.16, escribiendo la evidencia del espejo de iCloud: la medicion era real y por eso la pegue tal cual, que es justo como se cuela este fallo — no por descuido, sino por querer dejar el dato exacto. El repo del arsenal es PUBLICO y eso NO se borra despues: ni del historial de git ni de los clones que ya se hicieron. El Arsenal lo redacto en su copia publica y publico la v1.17 limpia (commit 9c8fce4), pero pidio el arreglo en origen con el argumento correcto: redactar al publicar es una red que solo existe mientras alguien use esa herramienta, y el dia que se sincronice sin ella, se publica. LA CLASE, NO EL CASO: se barrio la skill entera y la ruta absoluta era UNA sola, pero el barrido destapo otra cosa — `grep -ric` daba 2 coincidencias de "feropel" en SKILL.md y `grep -rn` daba 0, porque el segundo iba sin `-i` y la variante escrita es "Feropel". Dos medidas del mismo hecho que se contradicen significan que UNA MIENTE, y la que miente es la que cambio de instrumento entre una y otra; nunca se elige la que conviene. Resultaron dos menciones de la marca personal de FER usadas como ejemplo didactico ("el logo de Feropel entre los logos de Golden"): es marca PUBLICA suya, no una credencial, asi que se deja y se le avisa al Arsenal para que decida en su copia, en vez de sobre-redactar y perder el ejemplo. CANDADO, la asercion 11: recorre los scripts, SKILL.md y las referencias y falla si alguno trae `/Users/<alguien>/`, con el patron generico y no el nombre de este equipo, para que sirva en cualquier maquina. Probada en las TRES direcciones: sano 17 de 17 exit 0 · devolviendo la ruta al comentario de `_comun.sh` muerde y nombra el archivo · metiendola en SKILL.md, que es donde nadie mira porque "es solo documentacion", muerde igual. LECCION: un dato medido se cita por su FORMA, no por su valor literal — `/Users/<usuario>/Desktop` prueba lo mismo que la ruta real y no publica de quien es el equipo. -->
<!-- skill v1.17 · 2026-09-27 · FILA DEL CHAT ARSENAL Y SKILLS, con su verificador adversarial (golden-verificador) sobre la seccion "Antes de empezar". CUATRO hallazgos, los cuatro comprobados aqui contra los archivos antes de tocar nada, los cuatro reales. (1) El parrafo de `deshacer.sh` estaba SIN ACENTOS en texto vivo ("excepcion", "asi", "boton", "ahi", "lo que si rompe") y ademas le hablaba a quien vaya a PORTAR la skill, no a quien la usa, en mitad de una tabla de requisitos del usuario. Se saca del cuerpo y el hecho se conserva aqui: `deshacer.sh` ya resuelve la portabilidad solo (usa `tac` donde existe y `tail -r` en macOS), asi que el boton de revertir funciona en los dos sistemas; quien porte la skill no tiene nada que arreglar ahi, y lo que si rompe fuera de macOS son `md5 -q` y `stat -f`. (2) EL HALLAZGO QUE VALE, y es una promesa falsa que la skill llevaba dentro: decia que sin ffmpeg "los videos se verifican abriendolos uno a uno", y la herramienta Read NO ABRE MP4 — abre imagenes y PDF. La misma frase estaba en `hoja-contactos.sh` (mensaje de falta ffmpeg), y el chat del Arsenal declaro que de ahi la copio a su propio texto: un error se propaga por copia entre skills igual que entre scripts. El arreglo NO es el que venia propuesto ("los videos quedan sin clasificar"): se midio y hay una salida real. `qlmanage -t -s 400 -o <salida> "<video>"` viene en todo Mac, no necesita instalar nada y deja un PNG que Read si abre. Probado sobre un MP4 real del disco: devolvio un fotograma legible de 120 KB con el texto de la pieza perfectamente visible. Asi que sin ffmpeg: imagenes y PDF con Read, videos con QuickLook y luego Read, y lo que aun asi no se vea NO se clasifica por el nombre, se reporta pendiente. Corregido en los dos sitios. (3) La comprobacion de macOS (`uname` = `Darwin`) solo vivia en la tabla de requisitos; la Fase 0, que es donde se ejecuta, arrancaba creando la carpeta de control sin comprobar nada. Un requisito escrito donde se LEE y no donde se CORRE no lo comprueba nadie: pasa a ser el primer paso de la Fase 0. (4) La fila de ffmpeg decia "saca fotogramas de los videos", y es menos de lo que pasa: el bucle de `hoja-contactos.sh` corre el MISMO ffmpeg sobre todas las piezas, imagenes incluidas, asi que sin ffmpeg tampoco hay mosaico de imagenes. CANDADO, la asercion 10, porque el hallazgo 2 no fue un error suelto sino una frase repetida en dos archivos que divergieron de la realidad a la vez: el banco exige ahora que SKILL.md y el mensaje de `hoja-contactos.sh` nombren los dos el mismo metodo de reserva, y que ninguno de los dos siga diciendo que un video se abre con Read. Es la misma forma del candado de las listas de extensiones de la v1.6: lo que se declara alineado se demuestra con una comprobacion, no se afirma. Probada en las TRES direcciones: sano 16 de 16 exit 0 · devolverle a SKILL.md la frase de que el video se abre con Read muerde · y el SEÑUELO muerde igual, que es el que importa: el script deja de nombrar qlmanage y ofrece otra cosa, sin decir una sola falsedad, solo divergiendo — que es exactamente como nacio el hallazgo, uno se movio y el otro se quedo. LECCION: la tabla de requisitos ya se habia corregido en la v1.11 y en la v1.12 y seguia teniendo una promesa falsa, porque las dos veces se reviso lo que la tabla DECLARABA y no lo que las herramientas PUEDEN. Un requisito se mide contra la capacidad real de la herramienta, no contra la intencion de quien lo escribio. -->
<!-- skill v1.16 · 2026-09-27 · LA COMPUERTA DE LA v1.15 DABA VERDE SOBRE EL DISCO DE TRABAJO ENTERO, y se descubrio al medir para responderle a FER una pregunta suya de una linea ("esta skill revisa mis archivos en Google Drive o solo mi computador"). Fallo del lado PEOR, el falso verde: `exigir_local` resolvia enlaces con `pwd -P` y `~/Desktop` resuelve A SI MISMO, sin enlace que seguir, asi que la compuerta lo declaraba local. Y no lo es. Medido en este equipo: ~/Desktop/⭐️ MASTER ⭐️ y ~/Library/Mobile Documents/com~apple~CloudDocs/Desktop/⭐️ MASTER ⭐️ tienen el MISMO inodo (16777233:237859135) — son el mismo objeto de disco. El ajuste "Escritorio y Documentos en iCloud" esta activo, macOS no lo implementa con un symlink, y por eso TODO lo que esta skill ordeno en el Escritorio llevaba semanas sincronizandose a iCloud sin que la compuerta dijera una palabra. La leccion de la v1.7 otra vez y mas caro: la comprobacion no se hace donde es COMODO mirar (el enlace), se hace donde esta el hecho (el inodo). Arreglo: `espejo_icloud()` en `_comun.sh` compara `stat -f '%d:%i'` de la ruta contra su gemelo bajo CloudDocs, y para el propio ~/Desktop —que es la excepcion, NO comparte inodo con su gemelo, medido 260833 contra 3878501— pregunta por un hijo cualquiera. Por nombre no se puede: una carpeta llamada "Desktop" en iCloud sin el ajuste activo daria falso positivo, y eso esta probado con un senuelo. SEGUNDA DECISION, de diseño y no de deteccion: `carpeta_sincronizada` ahora tiene TRES salidas y no dos. Google Drive, OneDrive, Dropbox e iCloud Drive suelto PARAN (exit 3) porque son carpetas que alguien puso ahi a proposito y a menudo estan compartidas con otras personas. El espejo del Escritorio AVISA y sigue, porque es la configuracion por defecto del equipo y cubre el disco de trabajo completo: pararse ahi bloquearia el uso principal de la skill en cada corrida, y un aviso que siempre bloquea se acaba desactivando entero — que es el mismo razonamiento del falso positivo de la v1.15, aplicado antes de que duela. El aviso nombra el servicio y la consecuencia (llega al iPhone y al iPad, un borrado tambien). MEDICION, 8 de 8 contra rutas reales: carpeta temporal LOCAL · ~/_prueba-golden-local LOCAL · ~/Desktop AVISA · ~/Desktop/⭐️ MASTER ⭐️ AVISA · CloudStorage/GoogleDrive PARA · ~/Google Drive PARA · el symlink ~/Desktop/OneDrive PARA · GOLDEN_NUBE_OK=1 sigue. Senuelo del inodo, 3 de 3: mismo nombre con objetos DISTINTOS da LOCAL (si fuera por nombre daria nube) · llegar por el lado de CloudDocs da nube · Escritorio sin gemelo da LOCAL. El caso positivo de la rama del inodo NO se puede fabricar (APFS no permite enlaces duros de directorio), asi que se mide sobre el equipo real y se dice que es asi, en vez de inventar un verde sintetico. DOS PRUEBAS MIAS MINTIERON antes de dar el verde y las dos quedan escritas porque son la misma clase: (a) `mktemp` devuelve /var/... y `pwd -P` devuelve /private/var/..., asi que las comparaciones de prefijo no casaban y el control positivo salia rojo por el motivo equivocado; (b) el doble sabotaje de la asercion 8 reventaba con PermissionError porque `copytree` se lleva el `chflags uchg` del blindaje y la copia no se podia sabotear. Un banco que muere a medias no da veredicto: las dos corregidas y re-corridas. CANDADO NUEVO, la asercion 9, porque la 8 no cubre esto: la 8 comprueba que la compuerta se LLAMA y la v1.16 nacio justamente de una compuerta que se llamaba en los cinco scripts y aun asi declaraba local el disco de trabajo entero. La 9 comprueba que ACIERTA, con tres casos sinteticos (no dependen de como tenga iCloud la maquina donde corra) y probada en las TRES direcciones: sano 15 de 15 exit 0 · con `espejo_icloud` devolviendo siempre 1 muerde · y con la version que detecta por NOMBRE en vez de por inodo muerde igual, que es el señuelo que importa porque es la implementacion equivocada que un test por nombre aprobaria. Se agrega `scripts/comprobar-nube.sh`, que no prueba la logica sino que contesta la pregunta de FER sobre SUS carpetas y la deja re-medible: recorre las nubes instaladas y dice que haria la compuerta en cada una y si macOS deja leerla, porque el veredicto cambia en cuanto se active o desactive el ajuste. Su primera corrida encontro que Documents TAMBIEN esta en el espejo, no solo Desktop. Banco completo 15 de 15, validar_arsenal exit 0. DATO QUE FER PREGUNTO, medido y no supuesto: Google Drive NO se puede leer desde aqui — la carpeta existe con permisos dr-x------ y enumerarla devuelve "Operation not permitted" (privacidad de macOS), asi que su contenido no entra a ninguna corrida. iCloud Drive y OneDrive SI se leen enteros. -->
<!-- skill v1.15 · 2026-09-27 · COMPUERTA DE NUBE, fila del Centro de Mando (regla suya del 27-sep, asignada a esta skill por ser la que MUEVE archivos: "el numero es tuyo"). El fallo que cierra no es un bug de un script, es un supuesto de toda la skill: daba por hecho que una ruta del disco es LOCAL, y en este equipo eso es falso de forma medible. `~/Google Drive` y `~/Desktop/OneDrive` se ven como carpetas normales y las dos resuelven por enlace a `~/Library/CloudStorage/`: ordenar 300 archivos ahi no ordena el equipo, ordena la carpeta COMPARTIDA y el cambio le llega a todo el que tenga acceso. Sin error, sin aviso y sin vuelta atras del lado del otro. Implementado como `scripts/_comun.sh` con tres funciones (`ruta_real` resuelve enlaces con `cd`+`pwd -P`, `carpeta_sincronizada` nombra el servicio, `exigir_local` para con exit 3), cableado en los CINCO scripts que tocan archivos del usuario: clasificar, nombrar, separar-web, eliminar, deshacer. NO mira el nombre de la ruta que le dan, resuelve el enlace y mira donde acaba: un detector que se fia del nombre no habria visto ninguno de los dos casos reales. Escape explicito `GOLDEN_NUBE_OK=1`, que avisa por cual servicio viaja el cambio y sigue, porque a veces hay que ordenar la carpeta compartida a proposito. Medido contra rutas REALES de este equipo, 6 de 6: carpeta temporal SIGUE · ~/Desktop SIGUE · CloudStorage/GoogleDrive PARA · ~/Google Drive PARA · el enlace ~/Desktop/OneDrive PARA · con GOLDEN_NUBE_OK=1 sigue avisando. CANDADO: asercion 8 del banco, que RECORRE el directorio de scripts y exige la llamada en codigo VIVO (quita los comentarios antes de buscar), para que el script que se agregue manana nazca con la compuerta. EL DETECTOR SE TUVO QUE AFINAR, y eso es lo que merece quedar escrito: la primera version contaba cualquier `mv` o `rm`, asi que acusaba a `duplicados.sh` y a `hoja-contactos.sh` por su `rm -f "$SIZES"` y su `rm -rf "$WORK"` — limpieza de sus PROPIOS temporales, ni un archivo del usuario. Con eso el caso SANO ya salia en rojo y los tres casos daban 13/1 exit=1 identicos: un detector que no distingue el sabotaje de la linea base no mide nada. Ahora excluye los objetivos temporales y probado en las TRES direcciones, con resultados DISTINGUIBLES: sano 14 de 14 exit 0 · quitar la llamada muerde y nombra solo nombrar.sh · dejarla como COMENTARIO muerde igual. LECCION, que es la de esta skill un nivel mas arriba otra vez: un detector que grita de mas acaba ignorandose, que es la forma educada de no existir — un falso positivo en la linea base es tan grave como un fallo que pasa, porque ambos terminan en que nadie mira el rojo. -->
<!-- skill v1.14 · 2026-09-27 · LA MISMA CLASE, UN NIVEL MAS ABAJO: la v1.13 arreglo el mktemp del BANCO, pero las HERRAMIENTAS seguian igual. Fila del Centro de Mando, verificada y ampliada: su lista (duplicados, hoja-contactos, nombrar, separar-web) resulto exacta y completa — barri los 9 scripts y no hay un quinto. La MEDICION fue peor que el aviso. Con un mktemp falso (exit 1, salida vacia) puesto delante en el PATH: `nombrar.sh` salia con EXIT 0 habiendo prefijado 0 de 3 archivos y con el log en 0 lineas; `separar-web.sh` EXIT 0 habiendo movido 0 de 1; `duplicados.sh` EXIT 0 analizando 0 archivos. Solo `hoja-contactos.sh` fallaba ruidoso (exit 1). Tres herramientas DEVOLVIENDO EXITO SIN HACER NADA es peor que el fallo del banco: quien las llama en un bucle ve exit 0 y da el trabajo por hecho mientras los archivos siguen intactos. Arreglo: las cuatro usan `mktemp "${TMPDIR:-/tmp}/golden-archivos.XXXXXX" || abortar` con mensaje propio. Verificado en las dos direcciones: con mktemp roto las cuatro dan exit 1 (antes tres daban 0), y con mktemp sano `nombrar.sh` sigue prefijando 3 de 3. CANDADO, porque el caso ya se arreglo dos veces y la clase no: el banco gana la asercion 7, que RECORRE el directorio de scripts (no una lista fija) y falla si encuentra cualquier `mktemp` sin `||` — cubre los scripts de hoy y los que se agreguen manana. EL CANDADO TUVO QUE ENDURECERSE, y eso merece quedar escrito: la primera version aceptaba `TMP="$(mktemp)"; : || {` — un `||` que protege a OTRA cosa — porque buscaba `mktemp[^|]*\|\|` y se conformaba con que hubiera un `||` en la linea. Ahora quita comentarios, une las lineas partidas con barra invertida (duplicados.sh encadena dos mktemp con &&) y exige el `||` ANTES del siguiente `;`. Probado en las TRES direcciones: sano 13 de 13 · mktemp desnudo muerde (exit 1) · el `||` señuelo tambien muerde (exit 1). Un candado que acepta un señuelo no es candado, es adorno — y la unica forma de saberlo es intentar colarse a proposito. LECCION: arreglar el caso en el banco y no barrer sus hermanos en las herramientas es medio arreglo; cuando aparece un fallo se busca LA CLASE en todo el arbol, el mismo dia. -->
<!-- skill v1.13 · 2026-09-27 · EL BANCO MENTIA EN VERDE, y se descubrio por accidente al correrlo dentro del sandbox. `mktemp -d` fallo sin que nadie lo mirara, `T` quedo VACIO, y `"$T/a"` se volvio `/a`: el sembrado murio entero pero las 6 aserciones siguieron corriendo sobre carpetas inexistentes. Resultado medido: 10 verdes y 2 rojos, y de esos verdes TRES eran falsos — "deshacer restaura el arbol identico" comparaba vacio contra vacio, "eliminar se niega con md5 distinto" se negaba porque los archivos no existian, y "separar-web respeta sets deliberados" pasaba porque no habia nada que grepear. Los 2 rojos tampoco eran defectos de las herramientas: eran el sembrado roto. Un banco asi no solo deja pasar fallos, ademas ACUSA a herramientas sanas. Arreglado en los dos puntos donde se rompe la cadena: (1) si `mktemp` falla, el banco ABORTA con exit 1 en vez de seguir con T vacio; (2) `sembrar()` COMPRUEBA con `-s` que los cuatro archivos obligatorios existen y no estan vacios, y aborta si no. Verificado en las tres direcciones: dentro del sandbox se niega (exit 1) en vez de inventar veredicto; fuera del sandbox pasa 12 de 12; y saboteando a proposito el sembrado del webp muerde con exit 1 y nombra el archivo que falta. LECCION, que es la misma de esta skill aplicada un nivel mas arriba: un banco de pruebas tambien es una herramienta que puede fallar en silencio, y la primera cosa que tiene que verificar es que sus propias condiciones de partida se cumplieron. Verde sin sembrado comprobado no es un verde. -->
<!-- skill v1.12 · 2026-09-27 · fabrica de golden-archivos: ratificado el numero v1.11 del chat ARSENAL Y SKILLS (su cambio es valido y cierra un fallo real del validador; respaldo verificado byte a byte, huella 3cd470318bb70d1b486858731d096fd9, y diff medido +12/-0 solo en SKILL.md, cero scripts tocados). SE CORRIGE UN ERROR DE HECHO de esa tabla: citaba `tail -r` entre los comandos que solo trae macOS, y es justo al reves — `deshacer.sh` es el UNICO script que ya resolvio la portabilidad (`tac` en Linux, `tail -r` en macOS). Medido con grep sobre los 9 scripts: los bloqueantes reales son `md5 -q` en 3 scripts y `stat -f` en 2, y ahora la tabla los nombra con su script. Verificado tambien que `ffmpeg` solo es codigo vivo en `hoja-contactos.sh` (en `autoprueba.sh` aparece unicamente en comentarios desde la v1.8), asi que esa fila si estaba bien. LECCION: una tabla de requisitos es una AFIRMACION MEDIBLE — se comprueba con grep contra los scripts, no se redacta de memoria; citar como roto lo unico que esta bien manda a arreglar lo sano y deja pasar lo que si rompe. -->
<!-- skill v1.11 · 2026-09-27 · LEY DE LOS REQUISITOS DEL USUARIO (FER, 02-sep): el validador la marcaba con FALLO (usa ffmpeg y no lo declaraba). Se agrega "Antes de empezar" encima de los limites duros con los DOS requisitos reales, medidos en los scripts: macOS (md5 -q, stat -f y tail -r solo existen ahi; en Windows o Linux no corren) y ffmpeg (hoja-contactos.sh). hoja-contactos.sh YA paraba si faltaba ffmpeg; se añade la comprobacion de macOS al arrancar para no dejar una carpeta a medio ordenar. Ninguna linea existente cambia. Chat del Arsenal con orden directa de FER, informado al Centro de Mando. -->
<!-- skill v1.10 · auditoría golden-skill-auditor 2026-09-20 (990→1000): mismo principio que el v1.6 ("un mosaico que calla piezas invalida la verificación") reaparecido en dos formatos que se le habían escapado a ese arreglo — `scripts/hoja-contactos.sh` MEDIA_EXTS no incluía `ai` ni `eps`, que `scripts/clasificar.sh` SÍ manda a IMÁGENES; esos archivos ni entraban al mosaico ni salían en "no se pudo leer": caían en silencio en el bucket "no son media (docs, datos)", mal etiquetados. El propio banco de regresión no lo veía porque su test 3 solo comparaba clasificar↔nombrar, nunca clasificar↔hoja-contactos. Arreglada LA CLASE: MEDIA_EXTS ahora incluye ai/eps, y `scripts/autoprueba.sh` gana un segundo diff (clasificar → IMÁGENES/GIFS/VIDEOS vs MEDIA_EXTS) que exige lo mismo por construcción, no por memoria. Verificado que MUERDE: sabotaje real (quitar ai/eps de MEDIA_EXTS en una copia aislada) produce 11 verde/1 rojo, exit 1. Re-corrido con el fix: 12 de 12 en verde. `validar_arsenal.py` exit 0, `inventario.sh` 0 rotas/0 huérfanos/0 dudosos, sintaxis de los 9 scripts OK. -->
<!-- skill v1.9 · auditoría golden-skill-auditor 2026-09-13 (980→990): hallazgo único en Activación/Instrucciones — el description promete "reubica lo que está en el producto equivocado" (líneas 7-8 y 239) pero la Fase 6 (Coherencia de contenido) solo enseñaba a DETECTAR intrusos con el mosaico y nunca decía cómo reubicarlos: ni comando, ni formato de log. Se agregó el bloque "Cómo reubicar un intruso confirmado" con el mv + línea de log exacta (mismo contrato MV<TAB>origen<TAB>destino de Fase 0) y el puntero a estructura.md para elegir destino. Resto de la skill verificado sin novedad: validar_arsenal.py exit 0, autoprueba.sh 11/11, inventario.sh 0 rotas/0 huérfanos/0 dudosos, referencias cruzadas a golden-dropi-analisis y golden-imagen-arena vigentes, sin secretos ni signos de apertura. -->
<!-- skill v1.8 · auditoría golden-skill-auditor 2026-09-06 (970→980): hallazgo único de robustez, mismo principio que el v1.7 ("un cero se prueba, no se cree") aplicado al PROPIO banco. `scripts/autoprueba.sh` seedeaba sus archivos de prueba con `ffmpeg -f lavfi` para fabricar pixeles de color, pero ninguno de los 6 bloques del banco abre ni mira contenido de imagen — todos verifican destino de movimiento, listas de extensión, entradas de log y md5 byte a byte. Consecuencia medida: en cualquier entorno sin ffmpeg (sandbox, CI, otra máquina) el banco entero se negaba a correr con "🔴 falta ffmpeg: el banco no puede sembrar imágenes", aunque las 6 pruebas pasan igual con bytes planos — verificado corriendo el mismo banco reparado en un entorno sin ffmpeg: 11 de 11 en verde. `sembrar()` ahora usa `printf` puro (sin ffmpeg) salvo el WebP mínimo que ya se fabricaba a mano. Confirmado que sigue mordiendo: sabotaje real de la normalización de barra en `separar-web.sh` (copia aislada) produce 10 verde/1 rojo, exit 1, igual que antes del cambio. `hoja-contactos.sh` sigue exigiendo ffmpeg de verdad para su propio uso (renderizar el mosaico) — eso no cambia, es un requisito real de esa herramienta, no del banco de regresión. -->
<!-- skill v1.7 · auditoría 2026-09-05 (970→): FALLA DE LA PROPIA CLASE QUE ESTA SKILL PERSIGUE, encontrada dentro de ella. separar-web.sh devolvía "0 piezas" cuando la ruta traía BARRA FINAL — y `for U in "$R"/*/`, la forma canónica de recorrer productos, SIEMPRE la trae: `${f#$UNIT/}` no recorta, la ruta relativa queda absoluta, ningún tramo resulta genérico y el filtro descarta todo. Sin error, sin aviso: cero. Medido: 1 pieza sin barra vs 0 con barra sobre el MISMO sandbox. Consecuencia real: el informe del 23-ago dijo "0 piezas, la biblioteca ya está separada" y era falso; al re-correrlo bien aparecieron 12 webp de Tag Recede que llevaban semanas mezcladas con los masters. Arreglada LA CLASE, no el caso: los 5 scripts que reciben ruta (separar-web, clasificar, nombrar, auditar, hoja-contactos) normalizan las barras finales; clasificar ya no escribe doble barra en el log y auditar imprime "(raiz)" en vez de la ruta absoluta cuando la carpeta mixta es la raíz. Candado nuevo: scripts/autoprueba.sh, banco de 11 invariantes que exige resultado IDÉNTICO con y sin barra, sets deliberados intactos, listas clasificar-nombrar alineadas por diff, negativa a mover sin log, ida y vuelta de deshacer byte a byte y negativa de eliminar con md5 distinto — verificado que MUERDE: saboteando la normalización sale 10 verde y 1 rojo, exit 1. Se halló además el blindaje INCONSISTENTE (SKILL.md en chmod 0444 mientras el resto estaba en uchg); se unificó en uchg, el estándar de la casa. LECCIÓN QUE VALE MÁS QUE EL PARCHE: un cero se prueba, no se cree; "no encontré nada" exige la misma evidencia que un hallazgo. -->
<!-- skill v1.6 · auditoría golden-skill-auditor 2026-08-23 (947→): TRES hallazgos, todos de la MISMA CLASE — trabajo que se calla sin error. (1) nombrar.sh ALLOW seguía sin `mkv` pese a que el changelog de v1.5 declaraba las listas "alineadas": clasificar.sh lo manda a VIDEOS y nunca recibía prefijo; verificado ahora por diff programático de ambas listas (huecos restantes: 0) — la lección es que "alineadas" se demuestra con un diff, no se afirma. (2) hoja-contactos.sh solo intentaba 8 formatos (jpg jpeg png webp gif heic mp4 mov): tiff/bmp/heif/webm/m4v/avi/mkv/svg/psd no se intentaban siquiera, así que no salían en el mosaico NI en la línea "no se pudo leer" — medido en sandbox: 4 archivos → "1 pieza". Eso contradecía la regla propia de la skill ("un mosaico que calla piezas invalida la verificación") en la herramienta de la fase 6, que es el corazón del método. Ahora la lista MEDIA_EXTS cubre todo lo que clasificar.sh trata como media, y el cierre imprime SIEMPRE "N de M piezas renderizadas" más un aviso si M>N y otro con los archivos no-media: el censo hace imposible la omisión silenciosa. (3) Sección "Conexión con el ecosistema" (estándar 9): los cambios y hallazgos relevantes se reportan a 🧠 GOLDEN - CENTRO DE MANDO — un criterio descubierto organizando (ej. dos marcas que son el mismo producto físico) le sirve a la tienda, la pauta y el bot, y si se queda en el chat se pierde. Blindaje: chflags -R uchg re-aplicado al cierre. -->
<!-- skill v1.5 · auditoría golden-skill-auditor 2026-08-21, verificada corriendo los 8 scripts contra un sandbox sintético (clasificar, nombrar DRY+real, separar-web dry+aplicar, duplicados, eliminar ok/rechazo, hoja-contactos con imágenes reales, deshacer): nombrar.sh ALLOW list (scripts/nombrar.sh:21) le faltaban 22 extensiones que clasificar.sh SÍ clasifica (svg, psd, ai, eps, tiff, bmp, numbers, tsv, zip, rar, 7z, rtf, txt, md, ppt, key, pages, hevc) — un logo .svg o un .zip de datos quedaban correctamente ubicados en su carpeta pero NUNCA se les anteponía el prefijo del producto, en silencio; ahora ambas listas están alineadas. Documentado en SKILL.md el formato real que escribe eliminar.sh con FORCE (dos md5 distintos separados por "!=", no un solo hash) — antes el ejemplo de formato del log no cubría ese caso. Blindaje: chflags -R uchg (mecanismo confirmado y re-aplicado al cierre de esta auditoría). -->
<!-- skill v1.4 · fix auditoría 2026-07-25: separar-web.sh es_generica ahora pliega casing y tilde (nocasematch + IMÁGENES explícito), así "Fotos"/"Canva"/"IMÁGENES" del usuario sí se reconocen — antes daba "0 piezas" en silencio con carpetas en casing natural; auditar.sh usa emojis en las cabeceras en vez de rayas de caja (regla global sin separadores de rayas) -->
<!-- skill v1.3 · ejercida en fuego real 2026-07-23 (986→1000): duplicados.sh sobre biblioteca real (1515 archivos), separar-web.sh exige que TODA la ascendencia entre unidad y archivo sea genérica (ruta_solo_generica) -->
<!-- skill v1.2 · auditoría 2026-07-23 (931→): eliminar.sh (el formato RM de ELIMINADOS.log se exigía pero ningún script lo producía y la corrida real ya se había desviado; ahora verifica md5 y se niega si no coinciden), separar-web.sh (la fase 4 no tenía herramienta y se escribía a mano cada vez, con criterios distintos entre imágenes y videos; corre en seco por defecto), auditar.sh chequeo 3 ahora aplica EXCL como los otros 5, hoja-contactos avisa y sugiere tandas cuando el mosaico pasa de 8 filas. CRÍTICO: auditar.sh daba falsos ✅ — usaba los filtros de exclusión como texto sin comillas, el shell los glob-expandía y find fallaba en silencio; ahora es array (un auditor que miente en verde es peor que no tenerlo). El detector de UUID pasó de "4 guiones" a la forma hex real 8-4-4-4-12: atrapaba nombres claros como "2026-07 (Jul-Ago) - por pedido.xlsx" y ahogaba los hallazgos reales en ruido -->
<!-- skill v1.1 · auditoría 2026-07-23: deshacer.sh portable a macOS (tac no existe en Darwin → tail -r, mv -n, resumen), log OBLIGATORIO y verificado escribible ANTES de mover en clasificar/nombrar (mover sin registro = irreversible), modo DRY de nombrar.sh documentado, hoja-contactos con filas automáticas (mosaico corto callaba piezas) y chequeo de ffmpeg, formato exacto de ELIMINADOS.log, duplicados.sh exige argumento y limpia temporales, auditar.sh cableado al flujo (apertura + QA de cierre) -->
<!-- skill v1.0 · GA1.0 original: 5 scripts + flujo de 9 fases, conocimiento de campo del ordenamiento MASTER (TOPPIK, LE'CÔTERRA, Logos Golden) -->

Tu trabajo es convertir carpetas caóticas en una biblioteca donde FER encuentre cualquier cosa en segundos y **nunca dude de qué es un archivo**. No es mover archivos por mover: es entender qué es cada pieza y ponerla donde tiene sentido.

## El principio que manda sobre todos

**Nunca clasifiques por el nombre del archivo. Ábrelo y míralo.**

Esta regla nació de errores reales y caros:
- Seis archivos llamados `Video 1 Shopify`…`Video 6 Shopify` parecían carpetas de un proyecto. Eran MP4 sin extensión, y al mirar un fotograma resultaron ser videos de **fibra capilar** — pertenecían a TOPPIK.
- Seis GIFs de 14-50 MB dentro de una carpeta llamada "Logos Golden" no eran logos: eran **tarjetas de presentación animadas del equipo**, con el nombre y cargo de cada persona.
- Un archivo llamado `Proyecto-Creador-de-Contenido.png` era el **logo de otra marca** (Feropel), no de Golden.

El nombre miente. El contenido no. Si vas a decidir el destino de un archivo, míralo primero.

## Antes de empezar — lo que TÚ tienes que tener

Esta skill mueve y renombra archivos con sus propios scripts, así que depende de dos cosas del equipo donde corre. Mejor saberlo ahora que con la carpeta a medio ordenar.

| Qué necesitas | Para qué | Cómo se consigue |
|---|---|---|
| Un **Mac** | Los scripts usan comandos que solo trae macOS: `md5 -q` (`autoprueba.sh`, `duplicados.sh`, `eliminar.sh`) y `stat -f` (`duplicados.sh`, `separar-web.sh`). En Windows o Linux no corren. | Es un requisito del equipo, no se instala |
| **ffmpeg** | Arma la hoja de contactos de `hoja-contactos.sh`, que es como se mira el material antes de clasificarlo. No es solo para video: el mismo `ffmpeg` compone el mosaico de **todas** las piezas, imágenes incluidas, así que sin él no hay mosaico de nada | En la Terminal, `brew install ffmpeg` (necesita Homebrew, de brew.sh) |

**Si falta algo, se para y se pide antes del primer movimiento.** La comprobación de macOS se ejecuta al arrancar la Fase 0, no aquí.

**Sin ffmpeg no se clasifica a ciegas: se verifica más despacio.** `hoja-contactos.sh` se detiene con el comando exacto para instalarlo, y mientras tanto:

- Las **imágenes y los PDF** se abren y se miran uno a uno con Read, que es justo para lo que sirve.
- Los **videos** no se pueden abrir con Read. Se les saca un fotograma con QuickLook, que viene en todo Mac y no necesita instalar nada, y ese PNG sí se mira con Read:
  `qlmanage -t -s 400 -o <carpeta-de-salida> "<video>"` deja `<video>.png` al lado.
  Medido el 27-sep-2026 sobre un MP4 real: devolvió un fotograma legible de 120 KB.
- Lo que aun así no se pueda ver, **no se clasifica por el nombre**: se reporta como pendiente. Esa es la regla que manda sobre todo lo demás.

## Antes de tocar nada: los límites duros

Estas carpetas se ven, se reportan, pero **no se reorganizan**:

- **Código y proyectos**: repos, `node_modules`, `.git`, temas Shopify (`.liquid`, `.json`, `settings_data`), builds. Renombrar ahí rompe cosas.
- **Datos de aplicaciones**: CapCut, JianyingPro, librerías de Photos. Son bases de datos internas.
- **Personal**: fotos familiares, eventos, documentos privados. Aunque estén desordenados, no son material de trabajo.

Si dudas si algo es código o creativo: los creativos son `jpg png webp gif mp4 mov pdf docx xlsx csv`. Todo lo demás, déjalo quieto.

## Una carpeta sincronizada no es una carpeta local

Antes del primer movimiento, cada script mira si la raíz que le diste se sincroniza a la nube.
La comprobación vive en `scripts/_comun.sh` (`exigir_local`) y la llaman los cinco scripts que
tocan archivos del usuario: `clasificar.sh`, `nombrar.sh`, `separar-web.sh`, `eliminar.sh` y
`deshacer.sh`.

**No todas las nubes pesan igual, así que hay dos comportamientos distintos.**

**Se PARA** (exit 3) en Google Drive, OneDrive, Dropbox y rutas de iCloud Drive sueltas. Son
carpetas que alguien puso ahí a propósito y a menudo están compartidas: ordenar 300 archivos
ahí es ordenárselos también a los demás, y un borrado desaparece para todos. Si aun así hay que
hacerlo, se le pregunta a FER y se corre con `GOLDEN_NUBE_OK=1` delante del comando.

**Se AVISA y se sigue** cuando la carpeta es el Escritorio o Documentos del propio equipo con
el ajuste de macOS "Escritorio y Documentos en iCloud" activo. Es la configuración por defecto
de esta máquina y cubre el disco de trabajo entero, así que pararse ahí bloquearía el uso
principal de la skill en cada corrida, y un aviso que siempre bloquea se acaba desactivando
completo. El aviso dice el servicio y la consecuencia: lo que se mueva llega al iPhone y al
iPad, y un borrado también.

**Las dos trampas medidas en este equipo, que es por lo que la comprobación es como es:**

1. **El enlace que no parece nube.** `~/Google Drive` y `~/Desktop/OneDrive` se ven como rutas
   normales del disco y las dos resuelven a `~/Library/CloudStorage/`. Por eso no se juzga el
   nombre de la ruta: se resuelven los enlaces con `pwd -P` y se mira dónde acaba.
2. **El espejo que ni `pwd -P` delata.** `~/Desktop` resuelve a sí mismo, sin enlace que
   seguir, y aun así su contenido está en iCloud: macOS no usa un symlink, hace que los hijos
   sean el **mismo objeto de disco** que los de `~/Library/Mobile Documents/com~apple~CloudDocs/Desktop`.
   Por eso la prueba es el **inodo** (`stat -f '%d:%i'`) contra el gemelo, no el nombre — con el
   nombre bastaría una carpeta llamada "Desktop" en iCloud para dar un falso positivo.

**Para saber qué haría la compuerta en este equipo, se mide, no se recuerda:**
`bash scripts/comprobar-nube.sh` recorre las carpetas de nube instaladas y dice, una por una,
si sería LOCAL, si avisaría o si pararía — y además si macOS deja leerla, que es otra cosa. La
respuesta cambia en cuanto el usuario activa o desactiva "Escritorio y Documentos en iCloud",
así que se vuelve a correr en vez de fiarse de la última vez.

Medido el 27-sep-2026 en el equipo de FER: Escritorio y Documentos **avisan** (están en iCloud,
el disco de trabajo `⭐️ MASTER ⭐️` incluido) · Descargas es local · Google Drive, las dos
cuentas de OneDrive y iCloud Drive suelto **paran**. Y un dato que no se ve en la detección:
la carpeta de Google Drive **no se puede leer** desde aquí, macOS lo niega con "Operation not
permitted", así que su contenido nunca entra a una corrida. iCloud Drive y OneDrive sí se leen
enteros.

## Flujo de trabajo

Trabaja en este orden. Cada fase asume la anterior hecha.

### 0. Infraestructura de seguridad (siempre primero)

**Primer paso, antes de crear nada:** comprueba que estás en macOS con `uname`, que debe
responder `Darwin`. Si no lo es, dilo y no muevas un solo archivo — `md5 -q` y `stat -f` no
existen fuera de macOS y los scripts fallarían con la carpeta a medio ordenar. Esto vive aquí,
en la fase que se ejecuta, y no solo en la tabla de requisitos de arriba: un requisito que solo
está escrito donde se lee, y no donde se corre, no lo comprueba nadie.

Después, crea la carpeta de control y el log **antes del primer movimiento**:

```
<raíz>/_ORGANIZACION-PRODUCTOS/
├── movimientos.log      ← cada operación, formato: MV<TAB>origen<TAB>destino
├── ELIMINADOS.log       ← cada borrado, formato: RM<TAB>ruta-borrada<TAB>ruta-del-sobreviviente<TAB>md5
│                          (con FORCE el cuarto campo es md5-borrado!=md5-sobreviviente: dos hashes distintos,
│                           prueba de que NO era un duplicado exacto — ver scripts/eliminar.sh)
└── LEEME.md             ← acta de qué se hizo y cómo revertir
```

Todo movimiento y renombrado se registra. Nada se borra sin quedar anotado junto a su sobreviviente: el md5 compartido en la línea RM es la prueba de que lo borrado y lo conservado eran el mismo contenido, y la ruta del sobreviviente es la recuperación (copiar de vuelta). Esto es lo que permite decir con certeza "esto no lo perdí yo" cuando el usuario pregunte — y esa pregunta llega.

Los scripts que mueven (`clasificar.sh`, `nombrar.sh`) exigen el log y verifican que sea escribible ANTES del primer movimiento: si el log no se puede escribir, no se mueve nada. Nunca los invoques sin log — un movimiento sin registro es un movimiento que no se puede deshacer.

`scripts/deshacer.sh "<log>"` revierte todo en orden inverso (nunca sobrescribe; reporta al final cuántos revirtió y cuáles no encontró).

### 1. Reconocimiento

**Empieza siempre por `scripts/auditar.sh "<raíz>"`.** Es de solo lectura y en una pasada te da la lista de trabajo completa: carpetas que mezclan archivos con subcarpetas, carpetas vacías, basura de descargas, nombres crípticos que hay que mirar, copias sueltas y carpetas donde el material web está revuelto con los masters. Lo que sale con ✅ ya está sano y no hay que tocarlo — eso evita trabajo inútil y movimientos de riesgo.

Al cerrar, vuelve a correrlo: es la prueba objetiva de que el trabajo quedó bien.

Mide también el tamaño del terreno:

```bash
find "<raíz>" -type f ! -path '*/node_modules/*' ! -path '*/.git/*' | wc -l
du -sh "<raíz>"/*/ | sort -rh
```

Identifica las **unidades de producto** (cada carpeta que representa un producto o marca) y separa lo que es material de trabajo de lo que es personal/código. Reporta el mapa al usuario antes de mover masivamente.

### 2. Clasificación por tipo

`scripts/clasificar.sh "<carpeta>" "<log>"` mueve los archivos **sueltos de esa carpeta** (no entra en subcarpetas) a:

`IMÁGENES · VIDEOS · GIFS · LOGOS Y MARCA · DOCUMENTOS · DATOS Y EXCEL · OTROS`

Aplícalo solo a carpetas **planas y revueltas**. Si una carpeta ya tiene una estructura pensada (por orientación: `Img Cuadradas`/`Img Verticales`; por tamaño: `1080x1080`; por propósito: `ADS`, `ANTES Y DESPUES`), **respétala** — esa organización suele ser mejor que la genérica y aplanarla destruye trabajo del usuario.

Si algo cae en `OTROS`, revísalo a mano: es señal de que el clasificador no supo qué era.

### 3. Nombrado auto-descriptivo

`scripts/nombrar.sh "<carpeta-unidad>" "<log>" [DRY]` antepone el nombre del producto. Con el tercer argumento `DRY` solo imprime lo que haría sin tocar nada — úsalo SIEMPRE en la primera pasada de una unidad nueva para revisar el prefijo resultante antes de renombrar en masa:

```
VIDEO 8.mov        →  ACEITE ANTI HONGOS - VIDEO 8.mov
_prompt_a_2025…mp4 →  SERUM 7DAYS - _prompt_a_2025…mp4
```

**Conserva el nombre original, no renumeres desde cero.** Es contraintuitivo pero importante: en un caso real la secuencia era VIDEO 1,2,3,4,5,8 — renumerar habría convertido el 8 en 6 y **ocultado que faltaban dos videos**. El hueco es información. Preservarlo permitió demostrar que la ausencia era anterior a nuestro trabajo.

El script solo renombra creativos y documentos; nunca código ni configuración.

**Nombres crípticos** (`IMG_4924`, UUIDs, `RPReplay_Final…`): esos sí merecen nombre nuevo, pero **solo después de mirar el contenido**. `IMG_4924.GIF` se convirtió en `Tarjeta - Nombre Apellido (Gerente Comercial).GIF` porque abrimos el archivo y leímos el nombre y el cargo del integrante.

### 4. Separar WEB de HD/master

El usuario necesita saber, sin pensar, qué sube y qué no.

- **WebP y MP4 liviano (<10 MB)** = web, listo para subir → carpeta `🌐 WEB SHOPIFY` del producto
- **PNG/JPG pesados, `.mov`, 4K** = master/original → se quedan en las carpetas de estudio

Regla operativa: abre `🌐 WEB SHOPIFY` y todo lo que hay ahí es subible. Lo demás es material de trabajo.

`scripts/separar-web.sh "<carpeta-unidad>" "<log>" [APLICAR]` lo hace por ti: sin `APLICAR` corre en seco y lista lo que movería. Corre siempre en seco primero — este paso reubica material que el dueño reconoce de memoria, y leer la lista antes evita sustos.

Solo toca carpetas-librería **genéricas** (`IMÁGENES`, `FOTOS`, `VIDEOS`, `CANVA`). No arrastra sets creativos deliberados (piezas de pauta por orientación, infografías con nombre propio): son creativos de anuncios, no assets de ficha de producto, y mezclarlos rompe el criterio de "todo lo que hay aquí se sube".

### 5. Regla anti-mezcla

**Ninguna carpeta debe tener archivos sueltos al lado de subcarpetas.** Al abrirla, o ves solo archivos, o ves solo carpetas. Detecta las infractoras:

```bash
find "<raíz>" -type d | while IFS= read -r d; do
  f=$(find "$d" -maxdepth 1 -type f ! -name '.*' | wc -l | tr -d ' ')
  s=$(find "$d" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')
  [ "$f" -gt 0 ] && [ "$s" -gt 0 ] && echo "[$f archivos + $s carpetas] $d"
done
```

Para cada una, agrupa los sueltos según **lo que son**, con un nombre que lo diga: scripts y configs → `_MOTOR`; informes PDF → `INFORMES`; documentos de un producto → `DOCUMENTOS`; videos que comparten origen → `Biblioteca de Anuncios`, `Videos Fibra`. El nombre de la subcarpeta debe explicar por qué esos archivos están juntos.

### 6. Coherencia de contenido

Aquí es donde de verdad aportas valor: **abre las carpetas y verifica que lo de adentro pertenezca ahí**.

Usa `scripts/hoja-contactos.sh "<carpeta>" "<salida.png>"` para generar un mosaico y **verlo todo de un golpe**. Luego lee la imagen. Es rapidísimo comparado con abrir archivo por archivo, y es como se cazan los intrusos. Si no pasas filas, el script las calcula para que entren TODAS las piezas — un mosaico que calla piezas invalida la verificación. Requiere ffmpeg (`brew install ffmpeg`); si no está, verifica abriendo los archivos uno a uno con Read — más lento, pero la verificación visual no se salta jamás.

Qué buscar:
- Material de **otro producto** (un banner de TOPPIK viviendo en la carpeta de banners de marca)
- Material de **otra marca** (el logo de Feropel entre los logos de Golden)
- Archivos que **no son lo que dice la carpeta** (tarjetas de presentación entre logos)
- Basura: `.crdownload` (descargas a medias), `.DS_Store`, carpetas vacías

Cuando dos productos son **el mismo producto físico con distinto nombre comercial**, el criterio es la marca visible: un creativo que no muestre marca sirve para ambos; si la muestra, pertenece a esa marca. Pregunta al usuario por estas equivalencias — no las adivines.

**Cómo reubicar un intruso confirmado.** El mosaico solo detecta; mover el archivo sigue el mismo contrato de Fase 0 — nunca `mv` suelto, siempre con línea en el log:

```bash
mkdir -p "<carpeta-destino>"
mv "<archivo-intruso>" "<carpeta-destino>/"
printf 'MV\t%s\t%s\n' "<archivo-intruso>" "<carpeta-destino>/$(basename "<archivo-intruso>")" >> "<movimientos.log>"
```

Destino según lo que resultó ser: producto correcto (su carpeta por tipo, ej. `IMÁGENES/`), marca corporativa o material no-producto (ver `references/estructura.md`, "Qué no es material de producto"). Si el archivo colisiona con uno del mismo nombre en el destino, agrega ` (2)` — nunca sobrescribas (ver "Colisiones de nombre" más abajo).

### 7. Duplicados

`scripts/duplicados.sh "<carpeta>" [...]` encuentra duplicados **exactos** agrupando primero por tamaño y hasheando solo los que colisionan (sobre bibliotecas de decenas de GB, esto es la diferencia entre segundos y colgarse).

**Antes de borrar cualquier cosa, míralas lado a lado.** La detección por similitud visual produce falsos positivos que destruyen material único. Casos reales que *parecían* duplicados y no lo eran:

- La **misma pieza en dos idiomas** (español / inglés)
- El **mismo producto en dos tonos** (IVORY / NATURE)
- El **mismo logo en dos colores** (beige / verde)
- **Fragancias distintas** de la misma línea, con arte casi idéntico
- Un **GIF animado** y su fotograma fijo
- La **versión web y la master** de la misma imagen — ambas se necesitan

Solo elimina cuando sea **el mismo archivo byte a byte**, o la misma imagen en menor resolución teniendo la mayor. Conserva siempre la de mayor calidad y la que esté mejor ubicada.

**Borra siempre con `scripts/eliminar.sh "<a-borrar>" "<sobreviviente>" "<ELIMINADOS.log>"`**, nunca con `rm` suelto. El script se niega a borrar si los md5 no coinciden y escribe la línea exacta que el log promete. Eso importa por dos razones: exige nombrar al sobreviviente (borrar sin saber qué queda es como no tener respaldo), y deja el md5 compartido como prueba de que lo borrado y lo conservado eran el mismo contenido. Para el caso legítimo de "misma imagen en menor resolución", añade `FORCE` como cuarto argumento — queda registrado con los dos md5 distintos para que se vea que no fue un duplicado exacto.

Ante la duda: no borres. Repórtalo y deja que el usuario decida.

**Atajo para copias sueltas.** Los archivos que aparecen en el Escritorio o en Descargas con prefijo `Copia de …`, ` (1)`, ` copy` casi siempre salieron de una carpeta ya organizada. Quítale el prefijo al nombre, busca ese nombre exacto en la biblioteca y compara md5:

```bash
orig="${f#Copia de }"
match=$(find "<biblioteca>" -type f -name "$orig" | head -1)
[ "$(md5 -q "$f")" = "$(md5 -q "$match")" ] && echo "duplicado exacto: borrar"
```

Si coinciden byte a byte y el original está bien ubicado, la copia suelta es basura segura de eliminar. Es el caso más limpio de deduplicado: cero riesgo, cero ambigüedad. Aun así se registra: línea `RM` en `ELIMINADOS.log` con la copia borrada, el original que sobrevive y el md5 compartido.

### 8. Cierre

Re-corre `scripts/auditar.sh "<raíz>"` — el mismo diagnóstico del inicio, ahora como QA: todo punto debe salir en ✅ o estar justificado en el reporte. Verifica y reporta:
- Cero carpetas mezcladas
- Cero carpetas vacías — salvo las que representen un producto real sin material aún (consérvalas a propósito y dilo)
- Cobertura de nombrado al 100%
- Total de operaciones reversibles

Actualiza `LEEME.md` con lo hecho, lo que dejaste intacto **y por qué**.

## Trampas técnicas que cuestan horas

**Antes de sellar cualquier cambio a un script, corre `scripts/autoprueba.sh`** (sin argumentos). Siembra un sandbox y exige 11 invariantes medidas: mismo resultado con y sin barra final en la ruta, sets deliberados intactos, listas de clasificar y nombrar alineadas por diff, negativa a mover sin log escribible, ida y vuelta de deshacer byte a byte, y negativa de eliminar con md5 distinto. Un banco que nunca falla no sirve: este está probado saboteándolo, y muerde con exit 1.

**Un cero se prueba, no se cree.** El fallo más caro de esta skill no fue un error: fue un `0` sin error. "No encontré nada" es una afirmación tan fuerte como un hallazgo y necesita la misma evidencia — corre el mismo caso por otra vía, o siembra a propósito algo que DEBA aparecer y comprueba que aparece. Si tu barrido sale limpio a la primera, sospecha del barrido.

**Renombrar mientras `find` recorre.** Si haces `find … | while read f; do mv …; done`, el recorrido se desincroniza y **se salta archivos en silencio**. Pasó de verdad: la primera pasada dejó LE'CÔTERRA con 5 de 126 archivos renombrados y no dio ningún error. Toma la lista completa primero (a un temporal), después renombra. Los scripts de esta skill ya lo hacen.

**Verifica cobertura, no confíes en el contador.** Después de una pasada masiva, cuenta cuántos archivos quedaron sin procesar. Un "1388 renombrados" suena a éxito y puede esconder un 20% saltado.

**Colisiones de nombre.** Al mover a una carpeta común, dos archivos pueden llamarse igual. Nunca sobrescribas: agrega ` (2)`.

**Rutas con emojis, tildes y espacios.** Son la norma aquí (`⭐️ MASTER ⭐️`, `LE'CÔTERRA`, `🌐 WEB SHOPIFY`). Entrecomilla siempre las variables e usa `IFS= read -r`.

**Mosaicos con ffmpeg.** Usa `format=rgb24` — mezclar PNG con transparencia y JPG hace fallar el filtro `tile` y devuelve un mosaico vacío. No uses `drawtext` para numerar: sin fuente configurada el filtro se cae en silencio; imprime el índice por consola y mapea número → nombre.

## Cómo reportar

FER decide rápido si le das evidencia, no adjetivos. En cada reporte:
- **Qué encontraste**, con números (`16 web + 9 master revueltos`)
- **Qué hiciste**, agrupado por decisión
- **Qué dejaste intacto y por qué** — esto genera tanta confianza como lo que tocaste
- **Qué queda pendiente** o necesita su criterio

Si el usuario sospecha que perdiste algo, no te defiendas: **ve al log y demuéstralo** con datos (`311 operaciones, todas MV, cero borrados`).

## Conexión con el ecosistema

Los cambios relevantes de esta skill — y los hallazgos que deje una corrida grande (una biblioteca reorganizada, una clase de error nueva, un criterio que FER dictó) — se reportan a **🧠 GOLDEN - CENTRO DE MANDO**. Quien ejecuta la skill hace ese reporte al cerrar; esta skill no tiene mensajería propia ni la necesita. El motivo es que el ecosistema decida como un solo sistema: un criterio de organización que se descubre aquí (ej. "Marbella y Candy Bella son el mismo producto físico") le sirve a la tienda, a la pauta y al bot, y si se queda en este chat se pierde.

## Referencias

- `references/estructura.md` — léela ANTES de crear o reorganizar cualquier carpeta de producto (fases 2 a 5): trae la anatomía estándar, la regla de nombrado, WEB vs MASTER y las reglas de identidad entre productos

## Fronteras y desambiguacion

Descripcion completa anterior (se conserva para no perder ningun matiz de frontera):

> Golden Group — ORGANIZADOR DE BIBLIOTECAS DE ARCHIVOS. Toma control de carpetas caóticas (productos, creativos, marca, informes) y las deja coherentes: clasifica por tipo, pone nombres auto-descriptivos con el producto adentro, separa el material WEB listo para subir de los originales HD/master, aplica la regla anti-mezcla (ninguna carpeta con archivos sueltos al lado de subcarpetas), reubica lo que está en el producto equivocado y elimina duplicados reales — todo con log reversible y verificación VISUAL antes de borrar. Úsala SIEMPRE que el usuario quiera organizar, ordenar, limpiar, clasificar o auditar archivos y carpetas — "organiza mi escritorio", "acomódame estas carpetas", "esto está hecho un desastre", "tengo archivos duplicados", "no sé qué es este archivo", "revisa que todo esté en su sitio", "clasifica estas fotos/videos", "separa lo que subo a Shopify de los originales", "hay imágenes repetidas", "esto no va en esa carpeta" — o cuando arrastre una carpeta suelta pidiendo que la ubique. Dispara aunque no diga "organizar": basta con desorden de archivos, duplicados, nombres crípticos (IMG_4924, UUID, "Video 1") o material de producto mezclado. NO para código/repos, datos de ventas (golden-dropi-analisis) ni generar imágenes (golden-imagen-arena).

