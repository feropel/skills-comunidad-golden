#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""leer_frontmatter.py — lee name y description del frontmatter de un SKILL.md. Lo llama inventario.sh.
Uso: python3 -X utf8 leer_frontmatter.py <SKILL.md>
Salida, una linea separada por tabuladores:
  OK\t<name>\t<caracteres de la description>   el frontmatter existe y se leyo
  SINFM\t\t                                     la skill NO tiene frontmatter (veredicto sobre la SKILL)
Cualquier otra cosa (salida vacia, excepcion, codigo distinto de 0) es un fallo del INSTRUMENTO, no de
la skill, e inventario.sh lo declara asi.
P61 (27-sep): antes vivia como heredoc dentro de inventario.sh. Bash guarda el heredoc en un temporal;
en una sesion cuyo sandbox no dejaba escribirlo, la salida venia vacia y el inventario decia
"SIN FRONTMATTER" sobre una skill sana, y cerraba con "Inventario completo". Como archivo, no hay temporal.
"""
import sys, re

lines = [l.rstrip('\r') for l in open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\n')]
if not lines or lines[0].strip() != '---':
    print("SINFM\t\t"); sys.exit()
fm = []
cerrado = False
for l in lines[1:]:
    if l.strip() == '---':
        cerrado = True
        break
    fm.append(l)
if not cerrado:
    print("SINFM\t\t"); sys.exit()
key = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):(.*)$')  # C7: claves raíz con dígito cierran
vals = {}
cur = None
for l in fm:
    m = key.match(l)  # C7-corte-clave
    if m:
        cur = m.group(1)
        v = m.group(2).strip()
        vals[cur] = [] if v in ('>-', '>', '|', '|-', '>+', '|+') else [v]
    elif cur is not None and (l.startswith(' ') or not l.strip()):
        vals[cur].append(l.strip())
name = ' '.join(x for x in vals.get('name', []) if x).strip()
desc = ' '.join(x for x in vals.get('description', []) if x).strip()
print("OK\t%s\t%d" % (name, len(desc)))
