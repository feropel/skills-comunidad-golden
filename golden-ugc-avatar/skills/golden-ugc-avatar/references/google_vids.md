# Google Vids — ruta verificada (0 créditos)

<!-- Extraído de SKILL.md v1.14 (2026-09-05) para bajar el coste de activación. Fuente única: este archivo. -->

## Alternative route — Google Vids (Workspace)

Higgsfield is not the only way to put a talking avatar on screen: **Google Vids** (part of Google
Workspace, which Golden already pays for) also generates avatars that read a script. Keep it on the
table so nobody pays credits for a job the subscription already covers.

**When Vids is the better call:** corporate / training / internal-comms pieces, announcements, and
anything horizontal that lives inside Workspace — the avatar reads a script, the file stays in
Drive, and it does not spend Higgsfield credits.

**When this skill's Higgsfield route still wins:** vertical UGC and paid-ad creative. The whole
point here is the *unpolished iPhone-selfie* read plus fine control of identity lock and
voice-body coherence through the Seedance prompt — that is what makes an ad stop the scroll, and
it is not what a clean corporate avatar tool is built for.

**What transfers either way:** the script craft in this skill is model-agnostic. The 5-layer stack,
the A–E avatar profiles with their vocabulary DNA, the voice-body coherence table
(`references/seedance_prompt_system.md` §8) and the compliance mirror above apply exactly the same
to a script you paste into Vids. Write the script here, render it wherever fits the job.

**Status — VERIFICADA EN VIVO (2026-08-29), 0 créditos.** Procedimiento medido paso a paso. Alcance exacto: se verificó hasta que `Generar` arrancó (5%); **el MP4 final no fue observado** porque se cayó la conexión del navegador. Las 5 trampas de abajo sí están medidas una a una:

1. **Avatar desde una FOTO PROPIA:** panel `Avatar` → `Cambiar` → **"Diseñar un avatar
   personalizado"**. El campo de carga es un `<input type=file>` **oculto**: se sube con la
   herramienta `file_upload` del navegador. **Nunca hagas clic en un file input** — abre el selector
   del sistema operativo, que el agente no puede manejar, y deja el flujo colgado.
2. Asistente de **4 pasos**: (1) foto propia o atributos, (2) *Original* vs **Mejorada** (Vids
   reencuadra a horizontal; fidelidad de rostro medida ALTA), (3) retoques — **déjalo vacío**:
   describir rasgos aleja el resultado de la cara real, (4) nombre + voz.
3. **Tope real: 800 caracteres de guion POR ESCENA.** Pegar un documento largo deja el botón en gris
   con "Se alcanzó el límite de caracteres".
4. **El guion de una escena ya poblada es de SOLO LECTURA** (medido: clic + escribir no entra). La
   salida es **crear una escena nueva** (`Escena → Nueva escena`), donde nace vacío y editable. El
   nodo que acepta el texto es el **formulario** del panel, no el párrafo visible.
5. **Son DOS botones en secuencia:** `Obtener vista previa` solo crea el preview; el que renderiza es
   **`Generar`**, que aparece después. El error **"Couldn't insert avatar. No generated videos
   found."** significa exactamente eso: se intentó insertar un video que todavía no se había generado.

**Mientras la congelación de Higgsfield siga vigente, ESTA es la ruta para un talking-head**:
HyperFrames no hace una persona fotorrealista hablando y Seedance está en pausa. Coste: incluido en
Workspace, cero créditos. (Ruta señalada por FER 2026-08-24; verificada 2026-08-29.)

