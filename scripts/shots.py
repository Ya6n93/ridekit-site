"""Captures de l'app pour le site : WebP et AVIF en 320, 480 et 720 px de large.

    python3 -I scripts/shots.py <dossier des captures> <liste nom|chemin relatif>

Les fichiers vont dans assets/img/shots/<nom>-<largeur>.(webp|avif). La liste
vient des captures iPhone 17 Pro (1206 × 2622) de ~/Documents/RideKit-screens.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "shots"
WIDTHS = (320, 480, 720)


def main(src_dir: str, listing: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for line in Path(listing).read_text().splitlines():
        if not line.strip():
            continue
        name, rel = line.split("|")
        im = Image.open(Path(src_dir) / rel).convert("RGB")
        for w in WIDTHS:
            h = round(im.height * w / im.width)
            small = im.resize((w, h), Image.LANCZOS)
            small.save(OUT / f"{name}-{w}.webp", "WEBP", quality=74, method=6)
            small.save(OUT / f"{name}-{w}.avif", "AVIF", quality=52, speed=4)
        print(name, im.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
