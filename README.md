# Skills de la Comunidad Golden

La familia completa de **Chatea Pro** para **Claude Code**. Instala la que necesites y tu
Claude arma solo la configuración de tus asistentes de venta por WhatsApp.

Ninguna skill contiene datos privados: cada una te pide tus datos cuando la usas.

---

## Skills disponibles (familia Chatea Pro)

| Skill | Para qué sirve |
|---|---|
| **golden-chatea-pro-full-configuracion** | Orquesta los 4 asistentes en una sola configuración coordinada. |
| **golden-chatea-pro-config-ventas-wp** | Configura el asistente de ventas por WhatsApp (Bot Fields nativos). |
| **golden-chatea-pro-prompt-ventas** | Crea el paquete de venta por producto (prompt, recordatorios, remarketing). |
| **golden-chatea-pro-config-comentarios** | Asistente que responde comentarios de anuncios y los convierte en ventas. |
| **golden-chatea-pro-config-logistico** | Asistente logístico: valida direcciones y coordina la entrega. |
| **golden-chatea-pro-validacion-direcciones** | Valida y corrige direcciones en la conversación (hija del logístico). |
| **golden-chatea-pro-config-carritos** | Recupera carritos abandonados por WhatsApp. |

---

## Cómo instalar — Manera 1: con un comando (recomendada)

Dentro de Claude Code, conecta esta tienda de skills una sola vez:

```
/plugin marketplace add feropel/skills-comunidad-golden
```

Y luego instala la que quieras (o varias):

```
/plugin install golden-chatea-pro-config-ventas-wp
```

Para tener toda la familia, instala cada una por su nombre. Actualiza todo con:

```
/plugin marketplace update skills-comunidad-golden
```

## Cómo instalar — Manera 2: descargar el ZIP

Cada skill tiene su `.zip` en la carpeta **descargas/**. Descárgalo, descomprímelo y en la
app **Terminal** de tu Mac pega (cambia el nombre por el de la skill):

```
mkdir -p ~/.claude/skills && cp -R ~/Desktop/NOMBRE-DE-LA-SKILL ~/.claude/skills/ && echo "LISTO"
```

La guía **GUIA-INSTALAR-Configurador-Ventas-WhatsApp.pdf** explica el método manual paso a
paso, como para principiantes.

---

*Comunidad Golden · para nuestros miembros. Cualquier duda, escríbenos.*
