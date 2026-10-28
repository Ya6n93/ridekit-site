"""Images de partage (Open Graph, 1200 × 630) des pages et des articles.

    python3 -I scripts/og.py

- pages : assets/img/og/<nom>.jpg, le titre à gauche, une capture de l'app à droite ;
- articles : assets/img/og/blog/<slug>.jpg, d'après le titre et la catégorie de chaque
  _posts/*.md, et assets/img/og/blog/en-<slug>.jpg pour les guides en anglais (en/blog/).
Les road trips ont les leurs, dessinées par scripts/roadbook.py.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path.home() / "Documents/GIT/Ridekit/node_modules/@expo-google-fonts/barlow-condensed"
OUT = ROOT / "assets/img/og"
S = 2  # dessiné en 2× puis réduit

PAGES = [
    ("default", "L'app moto pour iPhone", "Ta balade parfaite en un tap.", "boucle-en-un-tap"),
    ("generateur-balade-moto", "Générateur de balade moto", "Ta balade moto en un tap", "boucle-apercu"),
    ("sortie-moto-en-groupe", "Sortie moto en groupe", "Tes potes sur la carte", "sortie-de-groupe"),
    ("detection-chute-moto", "Détection de chute · RideKit Pro", "Si tu tombes, un proche le sait", "detection-de-chute"),
    ("roadbook", "Roadbook moto", "97 road trips moto en France", "roadbook"),
    ("meteo-moto", "Météo moto", "Le meilleur créneau pour rouler", "meteo"),
    ("gps-moto", "GPS moto gratuit sur iPhone", "Le guidage vocal, virage par virage", "navigation-lacets"),
    ("itineraire-moto", "Itinéraire moto", "Par les belles routes, sans autoroute", "points-de-vue"),
    ("partage-balade-moto", "Partage façon Strava", "Ta sortie, en une image", "partage"),
    ("prix-essence-moto", "Prix de l'essence", "Le plein au meilleur prix", "essence"),
    ("gpx-moto", "GPX moto", "Tes traces GPX, guidées à la voix", "gpx-trace"),
    ("carnet-entretien-moto", "Garage et entretien", "Ta moto, ses entretiens, ses rappels", "garage-entretien"),
    ("pro", "RideKit Pro", "49,99 € par an, 7 jours gratuits", "paywall"),
    ("en", "The motorcycle app for iPhone", "Your ride. One tap. Let's go.", "boucle-en-un-tap"),
]

CATEGORIES = {
    "routes": "Routes et road trips", "groupe": "Rouler en groupe", "securite": "Sécurité",
    "meteo": "Météo et moto", "entretien": "Entretien et carburant", "applis": "GPS, GPX et applis",
}


def font(weight: str, size: int):
    name = {"800": "800ExtraBold/BarlowCondensed_800ExtraBold.ttf", "600": "600SemiBold/BarlowCondensed_600SemiBold.ttf"}
    return ImageFont.truetype(str(FONTS / name[weight]), size * S)


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


def title_block(d, x0, y0, width, eyebrow, title, max_lines=4, start=92):
    d.text((x0, y0), eyebrow.upper(), font=font("600", 30), fill="#E8590C")
    size = start
    while True:
        f = font("800", size)
        lines = wrap(d, title.upper(), f, width)
        if len(lines) <= max_lines or size <= 50:
            break
        size -= 4
    y = y0 + 50 * S
    for line in lines[:max_lines]:
        d.text((x0, y), line, font=f, fill="#F5F5F2")
        y += int(size * 0.98) * S
    return y


def brand(d, x0, y0, tagline):
    f = font("800", 50)
    d.text((x0, y0), "RIDE", font=f, fill="#F5F5F2")
    d.text((x0 + d.textlength("RIDE", font=f), y0), "KIT", font=f, fill="#E8590C")
    d.text((x0, y0 + 58 * S), tagline, font=font("600", 24), fill="#9A9892")


def page_image(name, eyebrow, title, shot):
    W, H = 1200, 630
    im = Image.new("RGB", (W * S, H * S), "#0B0B0B")
    d = ImageDraw.Draw(im)
    # La capture, dans un cadre de téléphone, coupée en bas
    src = Image.open(ROOT / f"assets/img/shots/{shot}-720.webp").convert("RGB")
    pw = 330 * S
    ph = round(src.height * pw / src.width)
    src = src.resize((pw, ph), Image.LANCZOS)
    px, py = 810 * S, 46 * S
    frame = Image.new("RGB", (pw + 16 * S, ph + 16 * S), "#2A2A2A")
    mask = Image.new("L", frame.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, frame.width, frame.height), radius=52 * S, fill=255)
    im.paste(frame, (px - 8 * S, py - 8 * S), mask)
    mask2 = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask2).rounded_rectangle((0, 0, pw, ph), radius=44 * S, fill=255)
    im.paste(src, (px, py), mask2)
    d.ellipse((-260 * S, -300 * S, 520 * S, 480 * S), outline="#3A2414", width=3 * S)
    title_block(d, 64 * S, 70 * S, 680 * S, eyebrow, title)
    brand(d, 64 * S, 500 * S, "ridekit-app.com")
    im = im.resize((W, H), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / f"{name}.jpg", "JPEG", quality=80, optimize=True, progressive=True)


def post_image(path: Path, title: str, eyebrow: str, en=False):
    W, H = 1200, 630
    im = Image.new("RGB", (W * S, H * S), "#0B0B0B")
    d = ImageDraw.Draw(im)
    # Une route qui tourne, à droite : la signature des images RideKit
    pts = []
    for k in range(0, 101):
        t = k / 100
        x = 860 + 230 * __import__("math").sin(t * 6.2) * (1 - t * 0.4)
        y = -40 + t * 720
        pts.append((x * S, y * S))
    d.line(pts, fill="#2A2A2A", width=46 * S, joint="curve")
    d.line(pts, fill="#E8590C", width=8 * S, joint="curve")
    title_block(d, 64 * S, 64 * S, 760 * S, eyebrow, title, max_lines=4, start=86)
    brand(d, 64 * S, 500 * S, "ridekit-app.com" + (" · Guides" if en else " · Blog"))
    im = im.resize((W, H), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=80, optimize=True, progressive=True)


def front(path: Path) -> dict:
    txt = path.read_text().split("---")[1]
    out = {}
    for line in txt.splitlines():
        m = re.match(r'^(title|category|lang):\s*"?(.*?)"?\s*$', line)
        if m:
            out[m[1]] = m[2]
    return out


def main():
    for p in PAGES:
        page_image(*p)
    for f in sorted((ROOT / "_posts").glob("*.md")):
        fm = front(f)
        slug = re.sub(r"^\d{4}-\d\d-\d\d-", "", f.stem)
        post_image(OUT / "blog" / f"{slug}.jpg", fm.get("title", slug), CATEGORIES.get(fm.get("category", ""), "Blog RideKit"))
    # Guides en anglais : en/blog/<slug>/index.md
    for f in sorted((ROOT / "en/blog").glob("*/index.md")):
        fm = front(f)
        post_image(OUT / "blog" / f"en-{f.parent.name}.jpg", fm.get("title", f.parent.name), "RideKit guide", True)
    print("ok")


if __name__ == "__main__":
    main()
