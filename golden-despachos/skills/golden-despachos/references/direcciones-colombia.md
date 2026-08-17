# Direcciones · Colombia

Criterio único: **si un mensajero puede llegar sin llamar, la dirección sirve.** Si hay duda real de
ubicación, se pide el dato que falta.

El estándar preventivo vive en `golden-chatea-pro-validacion-direcciones`; aquí se aplica a pedidos
ya creados, donde además hay que mirar la relación entre la dirección y la transportadora asignada.

## Transportadoras habilitadas

- **A domicilio:** InterRapidísimo, Envía, TCC, Veloces, Coordinadora, Domina, Jamv-Drive.
- **Recogida en oficina:** **únicamente InterRapidísimo y Coordinadora.**
- **Servientrega no se usa en ninguna modalidad.** Si la dirección la menciona, es inválida aunque
  esté bien escrita.

## Retiro en oficina: bloquea la transportadora

**Si la dirección nombra la oficina de una transportadora, esa transportadora NO se cambia.**
Cambiarla es devolución garantizada: el cliente va a un punto donde su paquete nunca llegó.

Frases que lo activan: "Oficina InterRapidisimo", "Retira en oficina de …", "Recoge en …",
incluso mal escritas ("interrapisimo"). Normalizar sin espacios ni tildes antes de comparar.

Si dice "oficina" pero no se identifica cuál, o nombra una no habilitada → confirmar con el cliente.
Si trae la transportadora pero no la ciudad → pedir la ciudad de la oficina.

## Qué hace entregable una dirección urbana

Vía + número principal + `#` + número secundario + **número de puerta**: `Calle 25 # 30-45`.
Acepta sufijos (`30A-45`, `Bis`, `Sur`, `Este`, `Oeste`) y abreviaturas
(Cl, Cll, Cra, Kr, Cr, K, Av, AC, AK, Dg, Tv, Tr).

También sirve:
- Vía + numeración parcial + **barrio claro**.
- Vía + **referencia fuerte** ("frente al Éxito", "al lado de la iglesia", portería de color).
- **Manzana + Casa** + barrio, que es como se ubica en barrios populares.
- Conjunto o edificio reconocible **+ torre/apto**.
- **Ubicación de Google Maps o coordenadas**, con barrio o ciudad.

Rural: vereda + finca, corregimiento + referencia, o Km de vía + punto conocido.

## Cuándo marcarla incompleta

| Caso | Qué pedir |
|---|---|
| Sin vía ni números | la vía y los números (`Calle o Carrera # __-__`) |
| Solo la vía, sin puerta | el número de puerta |
| Nomenclatura cortada: `CL 36 # 36a` sin lo de después del guion | el número que va después del guion |
| Conjunto, edificio, torre o bloque sin número interno | la torre o el apartamento |
| Comercial sin oficina, local o punto | la oficina o el local |
| Solo barrio, solo ciudad, "mi casa", "cerca al parque" | la dirección completa |
| Rural sin finca ni referencia | la finca o una referencia clara |
| **Dos nomenclaturas en el mismo campo** | cuál de las dos se usa |
| Lugar público (estación de policía, terminal) sin más datos | la dirección de residencia, o si prefiere recoger en oficina |
| Menciona una transportadora no habilitada | si la entrega es en su casa o en ese punto |

**No pedir de más.** Si ya trae casa, apto, torre, bloque, interior, local, oficina, piso, barrio
claro o referencia fuerte, es válida. Solo se pide ante duda operativa real.

## La plantilla de la pregunta

Una sola línea, trato de usted, sin saludo (el bot ya saludó), sin emojis, sin explicaciones:

> **Para completar su envío, nos regala [lo que falta]?**

Nunca pedir código postal.

## Ojo con el texto basura

Los campos vienen sucios: correos metidos en la dirección, el nombre repetido, guiones sueltos al
final, dobles espacios. Eso no invalida la dirección — se ignora y se evalúa lo que sí es dirección.
