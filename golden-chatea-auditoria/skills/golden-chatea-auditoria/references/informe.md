# Formato del informe

El entregable es un informe de **cobertura**, no un veredicto. Se escribe en un archivo con el
espacio y la fecha en el nombre: `AUDITORIA-<espacio>-<AAAA-MM-DD>.md`, en la carpeta del
proyecto, sobre el mismo archivo si es del mismo día (estado vivo, nunca respaldos numerados).

**Frases prohibidas:** "quedó perfecto", "todo bien", "está listo", "debería funcionar".

## Esqueleto

```markdown
# Auditoría de Chatea Pro · <NOMBRE DEL ESPACIO>
<fecha y hora> · espacio medido `<user_ns>` · token `<archivo>` · API respondió <código>

## 1. Universo medido
| Objeto | N |
|---|---|
| Campos de bot | 95 de 95 declarados por el servidor |
| Campos de usuario | N de límite M |
| Asistentes detectados | N (lista) |
| Ranuras de producto ocupadas | N |
| Subflujos | N |
| Integraciones con credencial cargada | N |

## 2. Cobertura
| Bloque | Controles | Corridos | Objetos revisados | Sin verificar |
|---|---|---|---|---|
| A · Identidad | 5 | 4 | — | A5 (necesita panel) |
| ... una fila por bloque ...

**Lo que NO se verificó y por qué** — lista explícita. Un bloque sin correr se nombra.

## 3. Hallazgos
Ordenados por severidad. Uno por bloque, con esta forma:

### 🔴 MUERTO · D3 · Ocho productos cargados que el bot no puede disparar
**Qué pasa:** hay 12 ranuras `[Producto Ventas Wp]` con contenido y solo 4 registradas en
`[Ventas Wp] Disparador de productos Extendido`.
**Evidencia:** ranuras ocupadas 1,2,3,4,5,6,7,8,9,10,11,12 · registradas 4, 8, 9, 10.
**Consecuencia:** los 8 productos restantes no arrancan por ninguna vía.
**Qué habría que hacer:** registrarlos en el disparador con la skill de configuración, o
declararlos inactivos si es a propósito.
**Confianza:** medido contra el servidor el <fecha>.

## 4. Lo que está sano y cómo se comprobó
Se nombra lo verificado con su método, sin adjetivos: "los 12 campos de producto parsean como
JSON válido y ninguno supera el techo escapado; máximo medido 18.807 sobre 19.000".

## 5. Preguntas para FER
Los hallazgos 🔵 DUDA. Un hallazgo contra la configuración no es un bug hasta contrastarlo.

## 6. Verificación adversarial
Resultado de `golden-verificador`: qué intentó romper, qué encontró, y qué declaró como no
verificable.
```

## Reglas de escritura

- **Cada hallazgo lleva evidencia citada**: el campo, el valor medido, la fecha. Un hallazgo sin
  evidencia es indistinguible de una opinión.
- **Los números llevan su denominador.** "8 productos huérfanos" no dice nada; "8 de 12
  ranuras ocupadas" sí.
- **Nunca se pega una credencial**, ni siquiera parcial. Se dice que existe y de qué largo.
- **La moneda no se convierte.** Si el espacio es COP, el informe es en COP.
- **Lo transitorio no es veredicto.** Un endpoint que respondió lento o un 500 puntual se
  reintenta antes de reportarse como falla.
- **Cuando aparece un fallo, se busca LA CLASE, no el caso.** Un acento roto suele ser cien: si
  aparece uno, el informe dice cuántos campos tienen el mismo patrón.

## Después del informe

- Los hallazgos que hay que corregir se pasan a la skill dueña del campo, con el campo exacto y
  el valor propuesto. Esta skill no escribe.
- Corregido algo, **se vuelve a extraer y a auditar**. La respuesta de escritura no prueba nada.
- Si el hallazgo cambia el estándar de trabajo, se registra en memoria canónica y se avisa al
  Centro de Mando.
