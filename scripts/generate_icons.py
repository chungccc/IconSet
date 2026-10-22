import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "chungccicon.json"

# Scan image files in the repository, excluding .git and generated output.
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
EXCLUDED_DIRS = {".git", ".github", "scripts"}

icons = []

for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path == OUTPUT:
        continue
    if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
        continue
    if path.suffix.lower() not in EXTENSIONS:
        continue

    name = path.stem
    url = (
        "https://raw.githubusercontent.com/"
        "chungccc/IconSet/main/"
        + path.relative_to(ROOT).as_posix()
    )

    icons.append({"name": name, "url": url})

data = {
    "name": "IconSet",
    "description": "Personal icon collection",
    "icons": icons,
}

OUTPUT.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(f"Generated {OUTPUT.name}: {len(icons)} icons")