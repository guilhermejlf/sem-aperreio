"""Generate PWA icons from favicon.png."""
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "frontend" / "public" / "favicon.png"
OUT_DIR = BASE_DIR / "frontend" / "public" / "icons"
OUT_DIR.mkdir(parents=True, exist_ok=True)

THEME_BG = (26, 29, 35)  # #1a1d23


def generate_icons():
    img = Image.open(SRC).convert("RGBA")

    for size in (192, 512):
        # Standard icon
        resized = img.resize((size, size), Image.LANCZOS)
        resized.save(OUT_DIR / f"icon-{size}x{size}.png", "PNG")
        print(f"Generated icon-{size}x{size}.png")

        # Maskable icon (safe zone = 40% of canvas, icon fits in 80% center)
        canvas = Image.new("RGBA", (size, size), THEME_BG + (255,))
        icon_size = int(size * 0.6)  # 60% of canvas for safe zone compliance
        maskable = img.resize((icon_size, icon_size), Image.LANCZOS)
        offset = (size - icon_size) // 2
        canvas.paste(maskable, (offset, offset), maskable)
        canvas.save(OUT_DIR / f"icon-maskable-{size}x{size}.png", "PNG")
        print(f"Generated icon-maskable-{size}x{size}.png")


if __name__ == "__main__":
    generate_icons()
