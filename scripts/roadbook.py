"""Pages du Roadbook moto : une page par road trip de France, une par région et par département.

    python3 -I scripts/roadbook.py <chemin de src/data/roadbooks.json de l'app>

Lit le roadbook de l'app (données DATAtourisme et data.gouv.fr sous Licence Ouverte 2.0,
tracés OSRM et lieux © les contributeurs d'OpenStreetMap) et écrit, dans ce dépôt :

- _roadtrips/<slug>.md : une page par road trip (tout en front matter, rendu par
  _layouts/roadtrip.html) ;
- roadbook-moto/<région>/index.html et roadbook-moto/<région>/<département>/index.html ;
- _data/roadbook.json : les régions et départements, pour l'accueil du Roadbook ;
- assets/gpx/<slug>.gpx : la trace de chaque road trip, avec son attribution ;
- assets/img/roadbook/<slug>-<largeur>.(webp|avif) : la photo de couverture, seulement
  quand sa licence permet de la réutiliser (Wikimedia Commons sous licence libre) ;
- assets/img/og/roadbook/<slug>.jpg : l'image de partage (le tracé, dessiné ici).

Les communes et départements traversés viennent de l'API Géo de l'État
(geo.api.gouv.fr, Licence Ouverte 2.0), relevés tous les 3 km ; les réponses sont gardées
dans scripts/cache/geo.json pour qu'une reconstruction ne refasse pas les appels.
Rien n'est inventé : chaque chiffre vient des données ou d'un calcul sur le tracé.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import sys
import unicodedata
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "scripts" / "cache"
SITE = "https://ridekit-app.com"
UA = "RideKitSiteBuilder/1.0 (https://ridekit-app.com; contact@ridekit-app.com)"
FONTS = Path.home() / "Documents/GIT/Ridekit/node_modules/@expo-google-fonts/barlow-condensed"

# Photos reprises seulement sous ces licences (Wikimedia Commons). « Droits réservés,
# diffusé par DATAtourisme » : jamais reprise sur le site.
LICENCES = {
    "CC0": "https://creativecommons.org/publicdomain/zero/1.0/deed.fr",
    "Public domain": None,
    "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.fr",
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.fr",
    "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.fr",
    "CC BY-SA 2.5": "https://creativecommons.org/licenses/by-sa/2.5/deed.fr",
    "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.fr",
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.fr",
}
LICENCE_OUVERTE = "https://www.etalab.gouv.fr/licence-ouverte-open-licence/"
SAMPLE_KM = 3.0


# ————— Géométrie (reprise de src/lib/geo.ts et route.ts de l'app) —————

def decode(text: str, precision: int = 5) -> list[tuple[float, float]]:
    factor = 10 ** precision
    coords, i, lat, lng = [], 0, 0, 0

    def nxt():
        nonlocal i
        result = shift = 0
        while True:
            if i >= len(text):
                return None
            b = ord(text[i]) - 63
            i += 1
            if not (0 <= b < 64) or shift > 30:
                return None
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        return ~(result >> 1) if result & 1 else result >> 1

    while i < len(text):
        d_lat, d_lng = nxt(), nxt()
        if d_lat is None or d_lng is None:
            break
        lat += d_lat
        lng += d_lng
        coords.append((lat / factor, lng / factor))
    return coords


def hav(a, b) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    x = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(x))


def cumkm(coords):
    out = [0.0]
    for k in range(1, len(coords)):
        out.append(out[-1] + hav(coords[k - 1], coords[k]))
    return out


def seg_at(cum, km):
    lo, hi = 0, len(cum) - 1
    while lo < hi - 1:
        mid = (lo + hi) >> 1
        if cum[mid] <= km:
            lo = mid
        else:
            hi = mid
    return lo


def point_at(coords, cum, km):
    if len(coords) < 2:
        return coords[0]
    lo = seg_at(cum, km)
    hi = lo + 1
    f = 0 if cum[hi] == cum[lo] else min(1, max(0, (km - cum[lo]) / (cum[hi] - cum[lo])))
    a, b = coords[lo], coords[hi]
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)


def bearing(a, b):
    la1, la2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1])
    y = math.sin(dl) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dl)
    return math.degrees(math.atan2(y, x))


def bearing_at(coords, cum, km, back, ahead):
    end = cum[-1]
    span = back + ahead
    frm = max(0, min(km - back, end - span))
    return bearing(point_at(coords, cum, frm), point_at(coords, cum, min(end, max(km + ahead, frm + span))))


def heading_diff(a, b):
    d = (a - b) % 360
    if d > 180:
        d -= 360
    if d <= -180:
        d += 360
    return abs(d)


def curviness(coords) -> float:
    """1,5 – 9,9 : la mesure de l'app (degrés de virage par km, lissés sur 50 m)."""
    cum = cumkm(coords)
    end = cum[-1]
    if not end:
        return 1.5
    step = 0.05
    deg, prev, km = 0.0, bearing_at(coords, cum, 0, step, step), step
    while km <= end:
        h = bearing_at(coords, cum, km, step, step)
        deg += heading_diff(prev, h)
        prev = h
        km += step
    return max(1.5, min(9.9, 1 + (deg / end) / 40))


def simplify(xy, tol):
    if len(xy) < 3:
        return xy
    keep = [False] * len(xy)
    keep[0] = keep[-1] = True
    stack = [(0, len(xy) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = xy[a]
        bx, by = xy[b]
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy
        worst, worst_d = -1, tol
        for k in range(a + 1, b):
            px, py = xy[k]
            t = 0 if not l2 else min(1, max(0, ((px - ax) * dx + (py - ay) * dy) / l2))
            d = math.hypot(px - ax - t * dx, py - ay - t * dy)
            if d > worst_d:
                worst_d, worst = d, k
        if worst > 0:
            keep[worst] = True
            stack += [(a, worst), (worst, b)]
    return [p for p, k in zip(xy, keep) if k]


class Projector:
    """Projection plate (équirectangulaire corrigée de la latitude) dans une boîte w × h."""

    def __init__(self, lines, w, h, pad):
        pts = [p for line in lines for p in line]
        self.lat0 = sum(p[0] for p in pts) / len(pts)
        self.kx = math.cos(math.radians(self.lat0))
        xs = [p[1] * self.kx for p in pts]
        ys = [-p[0] for p in pts]
        self.minx, self.maxx, self.miny, self.maxy = min(xs), max(xs), min(ys), max(ys)
        spanx = max(self.maxx - self.minx, 1e-6)
        spany = max(self.maxy - self.miny, 1e-6)
        self.s = min((w - 2 * pad) / spanx, (h - 2 * pad) / spany)
        self.ox = (w - spanx * self.s) / 2
        self.oy = (h - spany * self.s) / 2
        self.w, self.h = w, h

    def __call__(self, p):
        return ((p[1] * self.kx - self.minx) * self.s + self.ox, (-p[0] - self.miny) * self.s + self.oy)

    def km_per_unit(self):
        # 1 degré de latitude ≈ 111,2 km ; une unité de la boîte = 1/s degré.
        return 111.2 / self.s


def path_d(xy, dec=1):
    fmt = f"{{:.{dec}f}}"
    out = []
    for k, (x, y) in enumerate(xy):
        out.append(("M" if k == 0 else "L") + fmt.format(x) + " " + fmt.format(y))
    return "".join(out)


def nice_scale(km_per_unit, target_units):
    raw = km_per_unit * target_units
    for v in (0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200):
        if v >= raw * 0.6:
            return v, v / km_per_unit
    return 200, 200 / km_per_unit


# ————— Textes —————

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("’", "-").replace("'", "-")).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)


def fr_num(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def duration_label(minutes: int) -> str:
    h, m = divmod(int(round(minutes)), 60)
    if not h:
        return f"{m} min"
    return f"{h} h {m:02d}" if m else f"{h} h"


def curviness_label(c: float) -> str:
    if c < 2.5:
        return "routes plutôt roulantes"
    if c < 4:
        return "roulant, avec de beaux virages"
    if c < 5.5:
        return "sinueux par endroits"
    if c < 7:
        return "sinueux"
    return "très sinueux"


KIND = {"loop": "Boucle", "linear": "Itinéraire", "multiday": "Road trip"}


def fr_list(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " et " + items[-1]


def de(name: str) -> str:
    """« de Cluny », « d'Autun »."""
    return ("d’" if name[:1].lower() in "aeiouyhéèêâîôû" else "de ") + name


def dept_in(name: str) -> str:
    """« en Saône-et-Loire », « dans le Doubs », « dans les Vosges », « dans l'Aveyron »."""
    special = {
        "Doubs": "dans le Doubs", "Jura": "dans le Jura", "Lot": "dans le Lot", "Gard": "dans le Gard",
        "Tarn": "dans le Tarn", "Gers": "dans le Gers", "Var": "dans le Var", "Cher": "dans le Cher",
        "Nord": "dans le Nord", "Calvados": "dans le Calvados", "Morbihan": "dans le Morbihan",
        "Finistère": "dans le Finistère", "Cantal": "dans le Cantal", "Loiret": "dans le Loiret",
        "Rhône": "dans le Rhône", "Bas-Rhin": "dans le Bas-Rhin", "Haut-Rhin": "dans le Haut-Rhin",
        "Territoire de Belfort": "dans le Territoire de Belfort", "Vosges": "dans les Vosges",
        "Ardennes": "dans les Ardennes", "Yvelines": "dans les Yvelines", "Landes": "dans les Landes",
        "Pyrénées-Orientales": "dans les Pyrénées-Orientales", "Hautes-Pyrénées": "dans les Hautes-Pyrénées",
        "Pyrénées-Atlantiques": "dans les Pyrénées-Atlantiques", "Bouches-du-Rhône": "dans les Bouches-du-Rhône",
        "Côtes-d'Armor": "dans les Côtes-d’Armor", "Deux-Sèvres": "dans les Deux-Sèvres",
        "Hautes-Alpes": "dans les Hautes-Alpes", "Alpes-Maritimes": "dans les Alpes-Maritimes",
        "Haute-Marne": "en Haute-Marne", "Meuse": "dans la Meuse", "Marne": "dans la Marne",
        "Moselle": "en Moselle", "Aube": "dans l’Aube", "Aveyron": "dans l’Aveyron", "Hérault": "dans l’Hérault",
        "Yonne": "dans l’Yonne", "Aude": "dans l’Aude", "Ariège": "en Ariège", "Ain": "dans l’Ain",
        "Allier": "dans l’Allier", "Orne": "dans l’Orne", "Eure": "dans l’Eure", "Isère": "en Isère",
        "Indre": "dans l’Indre", "Oise": "dans l’Oise", "Aisne": "dans l’Aisne", "Ardèche": "en Ardèche",
        "Lozère": "en Lozère", "Nièvre": "dans la Nièvre", "Manche": "dans la Manche",
        "Somme": "dans la Somme", "Sarthe": "dans la Sarthe", "Creuse": "dans la Creuse",
        "Corrèze": "en Corrèze", "Dordogne": "en Dordogne", "Gironde": "en Gironde", "Drôme": "dans la Drôme",
        "Savoie": "en Savoie", "Haute-Savoie": "en Haute-Savoie", "Côte-d'Or": "en Côte-d’Or",
        "Saône-et-Loire": "en Saône-et-Loire", "Haute-Saône": "en Haute-Saône",
        "Meurthe-et-Moselle": "en Meurthe-et-Moselle", "Seine-Maritime": "en Seine-Maritime",
        "Tarn-et-Garonne": "dans le Tarn-et-Garonne", "Lot-et-Garonne": "dans le Lot-et-Garonne",
        "Haute-Garonne": "en Haute-Garonne", "Haute-Loire": "en Haute-Loire", "Loire": "dans la Loire",
        "Puy-de-Dôme": "dans le Puy-de-Dôme",
    }
    return special.get(name.replace("’", "'"), "en " + name)


def dept_par(name: str) -> str:
    """« par le Cantal », « par la Lozère », « par l'Allier », « par les Vosges »."""
    phrase = dept_in(name)
    for a, b in (("dans le ", "le "), ("dans les ", "les "), ("dans la ", "la "), ("dans l’", "l’")):
        if phrase.startswith(a):
            return b + phrase[len(a):]
    feminine = {"Lozère", "Haute-Savoie", "Savoie", "Corrèze", "Dordogne", "Gironde", "Haute-Garonne", "Haute-Loire",
                "Côte-d'Or", "Saône-et-Loire", "Haute-Saône", "Meurthe-et-Moselle", "Moselle", "Haute-Marne",
                "Seine-Maritime", "Haute-Vienne", "Haute-Corse", "Corse-du-Sud", "Charente", "Charente-Maritime"}
    vowel = {"Ariège", "Isère", "Ardèche", "Orne", "Eure", "Aube", "Ain", "Allier", "Indre", "Oise", "Aisne"}
    if name in vowel:
        return "l’" + name
    if name.replace("’", "'") in feminine:
        return "la " + name.replace("'", "’")
    return "le " + name


def region_in(name: str) -> str:
    return {"Grand Est": "dans le Grand Est", "Centre-Val de Loire": "en Centre-Val de Loire"}.get(name, "en " + name)


def clean_paragraphs(text: str) -> list[str]:
    """Les paragraphes de la source, sans les renvois à sa propre page (« Téléchargez ci-dessous… »)."""
    paras = [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", text or "")]
    out = []
    for p in paras:
        p = p.replace("\n", " ")
        p = re.sub(r"\s*>?\s*(Pour connaître toutes les étapes|Téléchargez ci-dessous)[^>]*", "", p).strip()
        if p:
            out.append(p)
    return out


# ————— Réseau —————

def get(url: str, timeout=30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


class Geo:
    """Commune sous un point, par l'API Géo ; réponses gardées sur disque."""

    def __init__(self):
        CACHE.mkdir(parents=True, exist_ok=True)
        self.path = CACHE / "geo.json"
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    @staticmethod
    def key(p):
        return f"{p[0]:.4f},{p[1]:.4f}"

    def fetch(self, p):
        url = (
            "https://geo.api.gouv.fr/communes?lat=%.5f&lon=%.5f&fields=nom,code,codeDepartement,departement,region"
            "&format=json" % p
        )
        for _ in range(3):
            try:
                res = json.loads(get(url))
                if not res:
                    return None
                c = res[0]
                return {
                    "nom": c["nom"], "code": c["code"],
                    "dep": c["departement"]["nom"], "depCode": c["codeDepartement"],
                    "reg": c["region"]["nom"],
                }
            except Exception:  # noqa: BLE001 — réessaie, puis abandonne ce point
                continue
        return None

    def lookup(self, points):
        todo = [p for p in points if self.key(p) not in self.data]
        if todo:
            with ThreadPoolExecutor(max_workers=8) as pool:
                for p, res in zip(todo, pool.map(self.fetch, todo)):
                    self.data[self.key(p)] = res
            self.path.write_text(json.dumps(self.data, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
        return [self.data.get(self.key(p)) for p in points]


# ————— Fichiers produits —————

def yaml_value(v) -> str:
    return json.dumps(v, ensure_ascii=False, separators=(", ", ": "))


def front_matter(data: dict) -> str:
    lines = ["---"]
    for k, v in data.items():
        lines.append(f"{k}: {yaml_value(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def write_gpx(path: Path, trip, lines, page_url, attribution):
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="RideKit (ridekit-app.com)" xmlns="http://www.topografix.com/GPX/1/1">',
        "<metadata>",
        f"<name>{xml_escape(trip['title'])}</name>",
        f"<desc>{xml_escape(attribution)}</desc>",
        f'<link href="{page_url}"><text>{xml_escape(trip["title"])} — Roadbook RideKit</text></link>',
        "</metadata>",
    ]
    for h in trip["highlights"]:
        ele = f"<ele>{h['ele']}</ele>" if h.get("ele") is not None else ""
        kind = "Col" if h["type"] == "col" else "Point de vue"
        parts.append(f'<wpt lat="{h["lat"]:.5f}" lon="{h["lon"]:.5f}">{ele}<name>{xml_escape(h["name"])}</name><type>{kind}</type></wpt>')
    for stage, coords in zip(trip["stages"], lines):
        parts.append(f"<trk><name>{xml_escape(stage['title'])}</name><trkseg>")
        parts.append("".join(f'<trkpt lat="{la:.5f}" lon="{lo:.5f}"/>' for la, lo in coords))
        parts.append("</trkseg></trk>")
    parts.append("</gpx>")
    path.write_text("\n".join(parts) + "\n")


def save_photo(url: str, base: Path) -> tuple[int, int] | None:
    """La photo en 480 et 960 px de large (WebP et AVIF) ; None si elle ne se télécharge pas."""
    if (base.parent / f"{base.name}-960.webp").exists():
        im = Image.open(base.parent / f"{base.name}-960.webp")
        return im.size
    u = url
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/([^/]+)$", url)
    if m:  # original : demander la vignette de 1280 px, pas le fichier d'origine
        u = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m[1]}/{m[2]}/{m[3]}/1280px-{m[3]}"
        if m[3].lower().endswith((".tif", ".tiff")):
            u += ".jpg"
    try:
        raw = get(u, timeout=60)
    except Exception:  # noqa: BLE001
        try:
            raw = get(url, timeout=90)
        except Exception as err:  # noqa: BLE001
            print("  photo introuvable", url, err)
            return None
    im = Image.open(BytesIO(raw)).convert("RGB")
    # Recadrage 3:2 centré : toutes les couvertures au même format.
    tw, th = im.width, round(im.width * 2 / 3)
    if th > im.height:
        th, tw = im.height, round(im.height * 3 / 2)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    base.parent.mkdir(parents=True, exist_ok=True)
    for w in (480, 960):
        s = im.resize((w, round(w * 2 / 3)), Image.LANCZOS)
        s.save(base.parent / f"{base.name}-{w}.webp", "WEBP", quality=72, method=6)
        s.save(base.parent / f"{base.name}-{w}.avif", "AVIF", quality=48, speed=4)
    return (960, 640)


def font(weight: str, size: int):
    name = {"800": "800ExtraBold/BarlowCondensed_800ExtraBold.ttf", "600": "600SemiBold/BarlowCondensed_600SemiBold.ttf"}
    return ImageFont.truetype(str(FONTS / name[weight]), size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def og_image(path: Path, title: str, eyebrow: str, stats: str, lines_ll, credit: str):
    W, H, S = 1200, 630, 2  # dessiné en 2× puis réduit : traits lisses
    im = Image.new("RGB", (W * S, H * S), "#0B0B0B")
    d = ImageDraw.Draw(im)
    # Tracé à droite
    proj = Projector(lines_ll, 520 * S, 520 * S, 30 * S)
    ox, oy = 640 * S, 55 * S
    d.rounded_rectangle((ox, oy, ox + 520 * S, oy + 520 * S), radius=36 * S, fill="#1A1A1A")
    for line in lines_ll:
        xy = [(x + ox, y + oy) for x, y in simplify([proj(p) for p in line], 1.5)]
        d.line(xy, fill="#E8590C", width=9 * S, joint="curve")
    sx, sy = proj(lines_ll[0][0])
    r = 13 * S
    d.ellipse((sx + ox - r, sy + oy - r, sx + ox + r, sy + oy + r), fill="#F5F5F2", outline="#0B0B0B", width=4 * S)
    # Textes à gauche
    x0 = 64 * S
    d.text((x0, 70 * S), eyebrow.upper(), font=font("600", 30 * S), fill="#E8590C")
    size = 84
    while True:
        f = font("800", size * S)
        tl = wrap(d, title.upper(), f, 540 * S)
        if len(tl) <= 3 or size <= 52:
            break
        size -= 6
    tl = tl[:3]
    y = 118 * S
    for line in tl:
        d.text((x0, y), line, font=f, fill="#F5F5F2")
        y += int(size * 0.98) * S
    d.text((x0, y + 18 * S), stats.upper(), font=font("600", 34 * S), fill="#9A9892")
    d.text((x0, 520 * S), "RIDE", font=font("800", 52 * S), fill="#F5F5F2")
    rw = d.textlength("RIDE", font=font("800", 52 * S))
    d.text((x0 + rw, 520 * S), "KIT", font=font("800", 52 * S), fill="#E8590C")
    d.text((x0, 578 * S), "ridekit-app.com · Roadbook moto", font=font("600", 24 * S), fill="#9A9892")
    cw = d.textlength(credit, font=font("600", 18 * S))
    d.text((ox + 520 * S - cw, 590 * S), credit, font=font("600", 18 * S), fill="#6B6964")
    im = im.resize((W, H), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=80, optimize=True, progressive=True)


# ————— Construction —————

def main(src: str):
    data = json.loads(Path(src).read_text())
    trips = [t for t in data["trips"] if t["country"] == "FR"]
    geo = Geo()
    out_trips = ROOT / "_roadtrips"
    out_pages = ROOT / "roadbook-moto"
    for p in (out_trips, ROOT / "assets/gpx", ROOT / "assets/img/og/roadbook"):
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)
    # Les pages de région et de département sont regénérées ; roadbook-moto/index.html (l'accueil, écrit
    # à la main) reste.
    if out_pages.exists():
        for child in out_pages.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
    out_pages.mkdir(exist_ok=True)

    built = []
    for t in trips:
        lines = [decode(s["polyline"]) for s in t["stages"]]
        all_pts = [p for line in lines for p in line]
        # Communes tous les 3 km, le départ et l'arrivée compris
        samples = []
        for line in lines:
            cum = cumkm(line)
            k = 0.0
            while k < cum[-1]:
                samples.append(point_at(line, cum, k))
                k += SAMPLE_KM
            samples.append(line[-1])
        places = geo.lookup(samples)
        communes, depts = [], []
        for c in places:
            if not c:
                continue
            if c["nom"] not in communes:
                communes.append(c["nom"])
            dkey = (c["dep"], c["depCode"], c["reg"])
            if dkey not in depts:
                depts.append(dkey)
        start_place = next((c for c in places if c), None)
        stage_curv = [curviness(line) for line in lines]
        km_list = [s["distanceKm"] for s in t["stages"]]
        tot = sum(km_list)
        curv = sum(c * k for c, k in zip(stage_curv, km_list)) / tot if tot else stage_curv[0]
        built.append({"t": t, "lines": lines, "pts": all_pts, "communes": communes, "depts": depts,
                      "start": start_place, "curv": curv, "stage_curv": stage_curv})

    # Régions et départements (celui du départ)
    regions: dict[str, dict] = {}
    for b in built:
        t = b["t"]
        st = b["start"]
        reg = t["region"]
        dep_name, dep_code = (st["dep"], st["depCode"]) if st else (None, None)
        r = regions.setdefault(reg, {"name": reg, "slug": slugify(reg), "trips": [], "depts": {}})
        r["trips"].append(b)
        if dep_name:
            dd = r["depts"].setdefault(dep_code, {"name": dep_name, "code": dep_code, "slug": slugify(dep_name), "trips": []})
            dd["trips"].append(b)
        b["region_slug"] = r["slug"]
        b["dep"] = (dep_name, dep_code)
        b["url"] = f"/roadbook-moto/{r['slug']}/{t['slug']}/"

    # Un département ne prend jamais l'adresse d'un road trip de sa région
    for r in regions.values():
        trip_slugs = {b["t"]["slug"] for b in r["trips"]}
        for dd in r["depts"].values():
            if dd["slug"] in trip_slugs:
                dd["slug"] = "departement-" + dd["slug"]

    # Voisins : les road trips qui partent le plus près
    for b in built:
        dists = sorted(
            ((hav(b["pts"][0], o["pts"][0]), o) for o in built if o is not b), key=lambda x: x[0]
        )[:4]
        b["nearby"] = [
            {"title": o["t"]["title"], "url": o["url"], "km_away": round(d), "km": o["t"]["distanceKm"],
             "kind": KIND[o["t"]["kind"]], "mini": mini_path(o["lines"])}
            for d, o in dists
        ]

    for b in built:
        write_trip(b, regions)

    write_lists(regions)
    print(f"{len(built)} road trips, {len(regions)} régions")


def mini_path(lines):
    proj = Projector(lines, 120, 84, 6)
    return " ".join(path_d(simplify([proj(p) for p in line], 0.8), 1) for line in lines)


def write_trip(b, regions):
    t = b["t"]
    slug = t["slug"]
    lines = b["lines"]
    dep_name, dep_code = b["dep"]
    region = t["region"]
    reg = regions[region]
    dep_slug = reg["depts"][dep_code]["slug"] if dep_code in reg["depts"] else None
    first, last = t["stages"][0], t["stages"][-1]
    start, end = first["start"], last["end"]
    km = t["distanceKm"]
    kind = t["kind"]
    curv = round(b["curv"], 1)

    # Carte SVG (640 × 440)
    W, H = 640, 440
    proj = Projector(lines, W, H, 34)
    paths = [path_d(simplify([proj(p) for p in line], 0.7), 1) for line in lines]
    sx, sy = proj(lines[0][0])
    ex, ey = proj(lines[-1][-1])
    marks = []
    for h in t["highlights"]:
        x, y = proj((h["lat"], h["lon"]))
        if -10 <= x <= W + 10 and -10 <= y <= H + 10:
            marks.append({"x": round(x, 1), "y": round(y, 1), "type": h["type"], "name": h["name"],
                          "ele": h.get("ele")})
    stage_marks = []
    if len(lines) > 1:
        for k, line in enumerate(lines[:-1]):
            x, y = proj(line[-1])
            stage_marks.append({"x": round(x, 1), "y": round(y, 1), "n": k + 2})
    scale_km, scale_px = nice_scale(proj.km_per_unit(), 110)
    svg = {
        "w": W, "h": H, "paths": paths,
        "start": [round(sx, 1), round(sy, 1)], "end": [round(ex, 1), round(ey, 1)],
        "loop": hav(lines[0][0], lines[-1][-1]) < 0.3,
        "marks": marks, "stages": stage_marks,
        "scale": {"px": round(scale_px, 1), "label": (fr_num(scale_km, 1) if scale_km < 1 else str(int(scale_km))) + " km"},
    }

    lats = [p[0] for p in b["pts"]]
    lons = [p[1] for p in b["pts"]]
    bbox = [round(min(lons), 4), round(min(lats), 4), round(max(lons), 4), round(max(lats), 4)]

    # Attribution de la source
    src = t["source"]
    m = re.search(r"mise à jour du (\d\d/\d\d/\d{4})", src.get("attribution", ""))
    updated = m[1] if m else None
    producer = src.get("attribution", "")
    producer = re.sub(r",? via DATAtourisme.*$", "", producer).replace("│", "·").strip()
    producer = re.sub(r"\s*\((Licence Ouverte[^)]*)\)\)?", "", producer).strip()
    routed = any(s.get("gpxOrigin") == "routed" for s in t["stages"])
    source = {
        "provider": src["provider"], "producer": producer, "url": src.get("sourceUrl"),
        "licence": "Licence Ouverte 2.0 (Etalab)", "licence_url": LICENCE_OUVERTE,
        "updated": updated, "retrieved": src.get("retrievedAt"), "routed": routed,
    }

    # Photo
    photo = None
    cov = t.get("cover")
    if cov and cov.get("provider") == "Wikimedia Commons" and cov.get("licence") in LICENCES:
        size = save_photo(cov["url"], ROOT / "assets/img/roadbook" / slug)
        if size:
            place, _, author = cov.get("credit", "").partition(" · ")
            photo = {
                "base": f"/assets/img/roadbook/{slug}", "place": place.strip() or None,
                "author": author.strip() or cov.get("credit"), "licence": cov["licence"],
                "licence_url": LICENCES[cov["licence"]], "link": cov.get("link"),
            }

    # Textes
    dep_phrase = dept_in(dep_name) if dep_name else region_in(region)
    if kind == "loop":
        lead = f"Boucle de {km} km au départ {de(start)}, {dep_phrase}"
    elif kind == "multiday":
        lead = f"Road trip de {km} km en {t['days']} jours, {de(start)} à {end}, {dep_phrase}"
    else:
        lead = f"Itinéraire de {km} km {de(start)} à {end}, {dep_phrase}"
    other_depts = [d[0] for d in b["depts"] if d[0] != dep_name]
    facts = [lead + "."]
    facts.append(
        f"Compte environ {duration_label(t['durationMin'])} de route à allure de balade, sans les pauses"
        + (f", en {len(t['stages'])} étapes." if len(t["stages"]) > 1 else ".")
    )
    facts.append(f"Sinuosité {fr_num(curv)}/10 : {curviness_label(curv)}.")
    if other_depts:
        facts.append(f"Le tracé passe aussi par {fr_list([dept_par(d) for d in other_depts])}.")
    cols = [h for h in t["highlights"] if h["type"] == "col"]
    views = [h for h in t["highlights"] if h["type"] == "viewpoint"]
    if cols or views:
        bits = []
        if cols:
            bits.append(f"{len(cols)} col{'s' if len(cols) > 1 else ''}")
        if views:
            bits.append(f"{len(views)} point{'s' if len(views) > 1 else ''} de vue")
        facts.append(f"Sur la route : {fr_list(bits)}.")
    intro = " ".join(facts)

    kind_word = {"loop": "Boucle moto", "linear": "Itinéraire moto", "multiday": "Road trip moto"}[kind]
    where = dep_name or region
    seo_title = f"{t['title']} : {kind_word.lower()} de {km} km ({where})"
    if len(seo_title) > 70:
        seo_title = f"{t['title']} : {kind_word.lower()}, {km} km"
    if len(seo_title) > 70:
        seo_title = t["title"]
    desc = (
        f"{kind_word} de {km} km "
        + (f"au départ {de(start)}" if kind == "loop" else f"{de(start)} à {end}")
        + f" ({where}) : tracé, étapes, sinuosité {fr_num(curv)}/10"
        + (", cols et points de vue" if t["highlights"] else "")
        + ", trace GPX gratuite."
    )

    stages = []
    for s, c in zip(t["stages"], b["stage_curv"]):
        stages.append({"title": s["title"], "start": s["start"], "end": s["end"], "km": s["distanceKm"],
                       "duration": duration_label(s["durationMin"]), "curv": fr_num(round(c, 1))})

    gpx_path = ROOT / "assets/gpx" / f"{slug}.gpx"
    attribution_txt = (
        f"{t['title']}. Source : {producer}"
        + (", via DATAtourisme" if src["provider"] == "DATAtourisme" else "")
        + f", Licence Ouverte 2.0 ({LICENCE_OUVERTE})"
        + (". Tracé recalculé avec OSRM, données © les contributeurs d'OpenStreetMap (ODbL)" if routed else "")
        + ". Cols et points de vue © les contributeurs d'OpenStreetMap (ODbL). Mis en forme par RideKit."
    )
    write_gpx(gpx_path, t, lines, SITE + b["url"], attribution_txt)
    gpx_kb = max(1, round(gpx_path.stat().st_size / 1024))

    og = f"/assets/img/og/roadbook/{slug}.jpg"
    og_image(
        ROOT / og.lstrip("/"), t["title"], f"Roadbook moto · {where}",
        f"{km} km · {KIND[kind].lower()} · sinuosité {fr_num(curv)}/10",
        lines, "Tracé : DATAtourisme · © OpenStreetMap",
    )

    fm = {
        "title": t["title"],
        "seo_title": seo_title,
        "description": desc,
        "permalink": b["url"],
        "trip_id": t["id"],
        "region": region, "region_slug": reg["slug"],
        "dept": dep_name, "dept_code": dep_code, "dept_slug": dep_slug,
        "depts": [d[0] for d in b["depts"]],
        "kind": kind, "kind_label": KIND[kind], "days": t["days"],
        "km": km, "minutes": t["durationMin"], "duration": duration_label(t["durationMin"]),
        "curv": fr_num(curv), "curv_value": curv, "curv_label": curviness_label(curv),
        "start": start, "end": end,
        "intro": intro,
        "summary": re.sub(r"\s+", " ", t["summary"]).strip(),
        "paragraphs": clean_paragraphs(t["description"]),
        "tags": t["tags"],
        "stages": stages,
        "highlights": [{"type": h["type"], "name": h["name"], "ele": h.get("ele"), "lat": h["lat"], "lon": h["lon"]}
                       for h in t["highlights"]],
        "communes": b["communes"],
        "svg": svg,
        "mini": mini_path(lines),
        "bbox": bbox,
        "gpx": f"/assets/gpx/{slug}.gpx", "gpx_kb": gpx_kb,
        "photo": photo,
        "image": og,
        "source": source,
        "nearby": b["nearby"],
        "last_modified_at": src.get("retrievedAt"),
    }
    (ROOT / "_roadtrips" / f"{slug}.md").write_text(front_matter(fm))


def write_lists(regions):
    index = {"regions": [], "total": 0, "km": 0}
    for r in sorted(regions.values(), key=lambda r: -len(r["trips"])):
        trips = r["trips"]
        n = len(trips)
        index["total"] += n
        index["km"] += sum(b["t"]["distanceKm"] for b in trips)
        depts = sorted(r["depts"].values(), key=lambda d: (-len(d["trips"]), d["name"]))
        entry = {"name": r["name"], "slug": r["slug"], "count": n, "url": f"/roadbook-moto/{r['slug']}/",
                 "indexed": n >= 3, "depts": []}
        for d in depts:
            entry["depts"].append({"name": d["name"], "code": d["code"], "slug": d["slug"], "count": len(d["trips"]),
                                   "url": f"/roadbook-moto/{r['slug']}/{d['slug']}/", "indexed": len(d["trips"]) >= 3})
        index["regions"].append(entry)
        write_list_page(r, None, trips, entry)
        for d in depts:
            write_list_page(r, d, d["trips"], entry)
    (ROOT / "_data").mkdir(exist_ok=True)
    (ROOT / "_data/roadbook.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))


def write_list_page(r, d, trips, entry):
    n = len(trips)
    name = d["name"] if d else r["name"]
    where = dept_in(d["name"]) if d else region_in(r["name"])
    kinds = {"loop": 0, "linear": 0, "multiday": 0}
    for b in trips:
        kinds[b["t"]["kind"]] += 1
    kms = [b["t"]["distanceKm"] for b in trips]
    twisty = sorted(trips, key=lambda b: -b["curv"])[:3]
    cols = sorted(
        {(h["name"], h.get("ele")) for b in trips for h in b["t"]["highlights"] if h["type"] == "col" and h.get("ele")},
        key=lambda c: -(c[1] or 0),
    )[:5]
    parts = []
    if n == 1:
        parts.append(f"1 road trip moto {where} pour l’instant, de {kms[0]} km.")
    else:
        kb = []
        if kinds["loop"]:
            kb.append(f"{kinds['loop']} boucle{'s' if kinds['loop'] > 1 else ''}")
        if kinds["linear"]:
            kb.append(f"{kinds['linear']} itinéraire{'s' if kinds['linear'] > 1 else ''} d’un point à un autre")
        if kinds["multiday"]:
            kb.append(f"{kinds['multiday']} road trip{'s' if kinds['multiday'] > 1 else ''} sur plusieurs jours")
        parts.append(f"{n} road trips moto {where}, de {min(kms)} à {max(kms)} km : {fr_list(kb)}.")
        parts.append(
            "Les plus sinueux : "
            + fr_list([f"{b['t']['title']} ({fr_num(round(b['curv'], 1))}/10)" for b in twisty]) + "."
        )
    if cols:
        parts.append("Les cols les plus hauts sur ces tracés : " + fr_list([f"{c[0]} ({c[1]} m)" for c in cols]) + ".")
    # Carte d'ensemble : tous les tracés dans une même boîte
    W, H = 640, 480
    all_lines = [line for b in trips for line in b["lines"]]
    proj = Projector(all_lines, W, H, 20)
    overview = []
    for b in trips:
        overview.append({
            "url": b["url"], "title": b["t"]["title"],
            "d": " ".join(path_d(simplify([proj(p) for p in line], 1.0), 1) for line in b["lines"]),
            "start": [round(v, 1) for v in proj(b["lines"][0][0])],
        })
    if d:
        url = f"/roadbook-moto/{r['slug']}/{d['slug']}/"
        title = f"Road trips moto {where}"
        seo_title = f"Balades et road trips moto {where} : {n} tracés GPX"
    else:
        url = f"/roadbook-moto/{r['slug']}/"
        title = f"Road trips moto {where}"
        seo_title = f"Road trips et balades moto {where} : {n} tracés GPX"
    if n == 1:
        seo_title = f"Road trip moto {where}"
    desc = (
        f"{n} balade{'s' if n > 1 else ''} et road trip{'s' if n > 1 else ''} moto {where} : tracés, étapes, "
        "sinuosité, cols et points de vue, traces GPX gratuites. Données ouvertes DATAtourisme et data.gouv.fr."
    )
    fm = {
        "layout": "roadbook-list",
        "title": title,
        "seo_title": seo_title,
        "description": desc,
        "permalink": url,
        "scope": "dept" if d else "region",
        "region": r["name"], "region_slug": r["slug"],
        "dept": d["name"] if d else None, "dept_code": d["code"] if d else None,
        "dept_slug": d["slug"] if d else None,
        "count": n,
        "intro": " ".join(parts),
        "overview": {"w": W, "h": H, "trips": overview},
        "noindex": n < 3,
        "image": "/assets/img/og/roadbook.jpg",
    }
    path = ROOT / url.strip("/") / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(fm))


if __name__ == "__main__":
    main(sys.argv[1])
