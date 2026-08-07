# Skills de la Comunidad Golden

Habilidades listas para instalar en **Claude Code**. Instálalas y tu Claude sabe hacer
tareas nuevas por ti. Ninguna contiene datos privados: cada skill te pide tus datos cuando
la usas.

---

## Skills disponibles

### Configurador del Asistente de Ventas WhatsApp (Chatea Pro)
Arma sola, y sin errores, toda la configuración del asistente de ventas por WhatsApp de
Chatea Pro. Le das los datos de tu negocio y te entrega los Bot Fields listos para pegar.
- Nombre para instalar: **golden-chatea-pro-config-ventas-wp**
- Guía paso a paso: **GUIA-INSTALAR-Configurador-Ventas-WhatsApp.pdf**

---

## Cómo instalar — Manera 1: con un comando (recomendada)

Dentro de Claude Code, escribe una sola vez para conectar esta tienda de skills:

```
/plugin marketplace add feropel/skills-comunidad-golden
```

Y luego instala la que quieras:

```
/plugin install golden-chatea-pro-config-ventas-wp
```

Claude la descarga e instala solo. Cuando saquemos mejoras, actualizas con:

```
/plugin marketplace update skills-comunidad-golden
```

## Cómo instalar — Manera 2: descargar el ZIP

Para quien prefiere hacerlo a mano (lo explica el PDF con lujo de detalle):

1. Descarga **descargas/golden-chatea-pro-config-ventas-wp.zip**.
2. Descomprímelo (doble clic).
3. Abre la app **Terminal** de tu Mac y pega:

```
mkdir -p ~/.claude/skills && cp -R ~/Desktop/golden-chatea-pro-config-ventas-wp ~/.claude/skills/ && echo "LISTO"
```

4. Abre Claude Code y escribe `/golden-chatea-pro-config-ventas-wp` para comprobar.

---

*Comunidad Golden · para nuestros miembros. Cualquier duda, escríbenos.*
