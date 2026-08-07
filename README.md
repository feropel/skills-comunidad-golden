# Skills de la Comunidad Golden · Familia Chatea Pro

Habilidades para **Claude Code** que arman, solas y sin errores, la configuración de tus
asistentes de venta por WhatsApp en **Chatea Pro**. Instala la que necesites; cada una te
pide tus datos cuando la usas (ninguna guarda datos privados).

---

## Cómo se organiza la familia (2 niveles)

**Nivel 1 — Los 4 asistentes** (se configuran una vez por tienda):

| Asistente | Skill | Qué hace |
|---|---|---|
| Ventas WhatsApp | `golden-chatea-pro-config-ventas-wp` | El bot que vende por WhatsApp (Bot Fields nativos). |
| Comentarios | `golden-chatea-pro-config-comentarios` | Modera y responde comentarios de tus anuncios y los mete al chat a comprar. |
| Logístico | `golden-chatea-pro-config-logistico` | Valida la dirección antes de despachar (baja devoluciones). |
| Carritos | `golden-chatea-pro-config-carritos` | Recupera por WhatsApp los carritos abandonados. |

**El orquestador** (arma los 4 de una sola vez, coherentes entre sí):

| Skill | Qué hace |
|---|---|
| `golden-chatea-pro-full-configuracion` | Configura TODO Chatea Pro llamando a los 4 asistentes. |

**Nivel 2 — Piezas que alimentan a un asistente:**

| Pieza | Alimenta a | Qué es |
|---|---|---|
| `golden-chatea-pro-prompt-ventas` | Ventas WhatsApp | El guion de venta **de cada producto**. |
| `golden-chatea-pro-validacion-direcciones` | Logístico | El prompt que lee y corrige direcciones (packs por país). |

---

## Cuándo llamar cada una

| Lo que quieres | Usa |
|---|---|
| Montar TODO Chatea Pro de una | `full-configuracion` |
| Solo el asistente de ventas por WhatsApp | `config-ventas-wp` |
| El guion de venta de un producto nuevo | `prompt-ventas` |
| Solo el asistente de comentarios | `config-comentarios` |
| Solo el asistente logístico completo | `config-logistico` |
| Solo validar/corregir direcciones | `validacion-direcciones` |
| Solo recuperar carritos abandonados | `config-carritos` |

---

## Cómo instalar — Manera 1: con un comando (recomendada)

Dentro de Claude Code, conecta esta tienda de skills una sola vez:

```
/plugin marketplace add feropel/skills-comunidad-golden
```

Luego instala la que quieras (o varias, una por su nombre):

```
/plugin install golden-chatea-pro-config-ventas-wp
```

Actualiza todo con:

```
/plugin marketplace update skills-comunidad-golden
```

## Cómo instalar — Manera 2: descargar el ZIP

Cada skill tiene su `.zip` en **descargas/**. Descárgalo, descomprímelo y en la app
**Terminal** de tu Mac pega (cambia el nombre por el de la skill):

```
mkdir -p ~/.claude/skills && cp -R ~/Desktop/NOMBRE-DE-LA-SKILL ~/.claude/skills/ && echo "LISTO"
```

La guía **GUIA-INSTALAR-Configurador-Ventas-WhatsApp.pdf** (y **MAPA-FAMILIA-CHATEA-PRO.pdf**)
explican todo paso a paso, como para principiantes.

---

*Comunidad Golden · para nuestros miembros. Cualquier duda, escríbenos.*
