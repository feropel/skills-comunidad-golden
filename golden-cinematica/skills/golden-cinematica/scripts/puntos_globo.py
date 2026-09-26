"""Decodifica land-110m (TopoJSON) y genera los puntos de tierra del globo: [lat*10, lon*10, ...].

Uso:  python3 puntos_globo.py <land-110m.json> <salida/globo-puntos.json>
El TopoJSON es de world-atlas (Natural Earth, dominio público):
  https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json
Requiere Pillow. Deja al lado de la salida `mapa_control.png` para mirarlo, y termina con tres
controles (Bogotá y Madrid en tierra, el Atlántico no): si alguno sale al revés, el mapa está mal."""
import json, math, os, sys
from PIL import Image, ImageDraw

if len(sys.argv) != 3:
    sys.exit(__doc__)
ENTRADA, SALIDA = sys.argv[1], sys.argv[2]
topo = json.load(open(ENTRADA))
sc, tr = topo["transform"]["scale"], topo["transform"]["translate"]

arcs = []
for arc in topo["arcs"]:
    x = y = 0; pts = []
    for dx, dy in arc:
        x += dx; y += dy
        pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)

def anillo(idx):
    out = []
    for i in idx:
        seg = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(seg if not out else seg[1:])
    return out

# raster equirectangular: 8 px por grado
F = 8
img = Image.new("L", (360 * F, 180 * F), 0)
d = ImageDraw.Draw(img)
for g in topo["objects"]["land"]["geometries"]:
    polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
    for poly in polys:
        for k, ring in enumerate(poly):
            raw = anillo(ring)
            if len(raw) < 3:
                continue
            # longitudes continuas: un anillo que cruza el meridiano 180 no se dibuja de lado a lado
            uw = [list(raw[0])]
            for lon, lat in raw[1:]:
                p = uw[-1][0]
                uw.append([p + (lon - p + 180) % 360 - 180, lat])
            if abs(uw[-1][0] - uw[0][0]) > 300:  # anillo que rodea el polo (Antártida): se cierra por el polo
                polo = -90 if sum(q[1] for q in uw) < 0 else 90
                uw += [[uw[-1][0], polo], [uw[0][0], polo]]
            for sh in (-360, 0, 360):
                d.polygon([((lon + sh + 180) * F, (90 - lat) * F) for lon, lat in uw], fill=255 if k == 0 else 0)

# rejilla de puntos de densidad pareja sobre la esfera
out = []
PASO = 1.15
lat = -84.0
while lat <= 84:
    n = max(1, int(round(360 * math.cos(math.radians(lat)) / PASO)))
    for j in range(n):
        lon = -180 + (j + .5) * 360 / n
        px, py = int((lon + 180) * F), int((90 - lat) * F)
        if img.getpixel((min(px, 360 * F - 1), min(py, 180 * F - 1))) > 0:
            out += [round(lat * 10), round(lon * 10)]
    lat += PASO

json.dump(out, open(SALIDA, "w"), separators=(",", ":"))
img.resize((720, 360)).save(os.path.join(os.path.dirname(os.path.abspath(SALIDA)), "mapa_control.png"))
print("puntos de tierra:", len(out) // 2, "bytes:", os.path.getsize(SALIDA))
# control: Bogotá y Madrid deben caer en tierra; el centro del Atlántico, no
malos = 0
for nombre, la, lo, tierra in [("Bogotá", 4.7, -74.1, True), ("Madrid", 40.4, -3.7, True), ("Atlántico", 25, -40, False)]:
    en_tierra = img.getpixel((int((lo + 180) * F), int((90 - la) * F))) > 0
    malos += en_tierra != tierra
    print(nombre, "en tierra" if en_tierra else "en mar", "OK" if en_tierra == tierra else "🔴 MAL")
sys.exit(1 if malos else 0)
