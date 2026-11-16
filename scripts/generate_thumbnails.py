
import json
import re
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
JSON_FILE = ROOT / "chungccicon.json"
OUTPUT_DIR = ROOT / "thumbnails"

SIZE = (96, 96)

def main():
    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    icons = data.get("icons", [])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0

    for icon in icons:
        name = str(icon.get("name", "")).strip()
        url = str(icon.get("url", "")).strip()

        if not name or not url:
            continue

        filename = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
        output = OUTPUT_DIR / f"{filename}.png"

        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "IconSet-Thumbnail-Generator"}
            )

            with urllib.request.urlopen(request, timeout=30) as response:
                image_data = response.read()

            with Image.open(BytesIO(image_data)) as image:
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGBA")
                image.thumbnail(SIZE, Image.Resampling.LANCZOS)

                canvas = Image.new("RGBA", SIZE, (0, 0, 0, 0))
                x = (SIZE[0] - image.width) // 2
                y = (SIZE[1] - image.height) // 2
                canvas.alpha_composite(image, (x, y))

                canvas.save(output, "PNG")

            success += 1
            print(f"Generated: {filename}.png")

        except Exception as error:
            failed += 1
            print(f"Skipped: {name} - {error}")

    print(f"Thumbnail generation complete: {success} successful, {failed} failed.")

if __name__ == "__main__":
    main()

