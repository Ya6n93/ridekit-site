"""Vérifie un site construit (jekyll build) avant de le publier.

    python3 -I scripts/check.py <dossier _site>

- chaque lien interne (href, src, srcset, poster) mène à un fichier qui existe ;
- chaque bloc JSON-LD est du JSON valide ;
- chaque page indexable a un <title> et une description, uniques ;
- chaque <img> a un attribut alt ;
- aucune ressource n'est chargée depuis un autre domaine (le site promet de n'en charger aucune).
Affiche les problèmes et sort en erreur s'il y en a.
"""
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE = "https://ridekit-app.com"


def target(root: Path, url: str):
    path = unquote(urlparse(url).path)
    p = root / path.lstrip("/")
    if path.endswith("/"):
        p = p / "index.html"
    if p.exists():
        return p
    if (root / (path.lstrip("/") + ".html")).exists():
        return root / (path.lstrip("/") + ".html")
    return None


def main(root_dir: str):
    root = Path(root_dir)
    problems = []
    titles, descs = defaultdict(list), defaultdict(list)
    pages = [p for p in root.rglob("*.html") if not p.name.startswith("__")]
    for f in pages:
        rel = "/" + str(f.relative_to(root)).replace("index.html", "")
        text = f.read_text()
        noindex = 'content="noindex' in text
        # Liens et ressources
        refs = re.findall(r'(?:href|src|poster)="([^"]+)"', text)
        for srcset in re.findall(r'srcset="([^"]+)"', text):
            refs += [part.strip().split(" ")[0] for part in srcset.split(",")]
        for r in refs:
            r = html.unescape(r)
            if r.startswith(("mailto:", "tel:", "#", "data:")):
                continue
            if r.startswith(SITE):
                r = r[len(SITE):] or "/"
            if r.startswith("http"):
                continue
            if r.startswith("/") and not target(root, r.split("#")[0]):
                problems.append(f"{rel} : lien cassé {r}")
        # Ressources tierces chargées (pas les liens)
        for tag in re.findall(r"<(?:img|script|source|video|iframe|link)\b[^>]*>", text):
            m = re.search(r'(?:src|href)="(https?://[^"]+)"', tag)
            if m and not m.group(1).startswith(SITE) and "rel=\"alternate\"" not in tag and "rel=\"canonical\"" not in tag:
                problems.append(f"{rel} : ressource tierce {m.group(1)}")
        # JSON-LD
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                json.loads(block)
            except Exception as err:  # noqa: BLE001
                problems.append(f"{rel} : JSON-LD invalide ({err})")
        # alt
        for img in re.findall(r"<img\b[^>]*>", text):
            if " alt=" not in img:
                problems.append(f"{rel} : image sans alt {img[:80]}")
        if noindex or f.name == "404.html":
            continue
        t = re.search(r"<title>(.*?)</title>", text, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', text)
        if not t:
            problems.append(f"{rel} : pas de <title>")
        else:
            titles[html.unescape(t.group(1)).strip()].append(rel)
        if not d or len(d.group(1)) < 50:
            problems.append(f"{rel} : description absente ou trop courte")
        else:
            descs[d.group(1)].append(rel)
    for k, v in titles.items():
        if len(v) > 1:
            problems.append(f"titre en double « {k} » : {', '.join(v)}")
    for k, v in descs.items():
        if len(v) > 1:
            problems.append(f"description en double : {', '.join(v)}")
    for p in problems:
        print(p)
    print(f"{len(pages)} pages, {len(problems)} problème(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main(sys.argv[1])
