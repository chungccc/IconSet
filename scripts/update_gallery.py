
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_FILE = ROOT / "chungccicon.json"
README_FILE = ROOT / "README.md"

START_MARKER = "<!-- ICON-GALLERY:START -->"
END_MARKER = "<!-- ICON-GALLERY:END -->"

COLUMNS = 6
ICON_SIZE = 48


def build_gallery(icons):
    cells = []

    for icon in icons:
        if not isinstance(icon, dict):
            continue

        name = str(icon.get("name", "")).strip()
        url = str(icon.get("url", "")).strip()

        if not name or not url:
            continue

        safe_name = html.escape(name, quote=True)
        safe_url = html.escape(url, quote=True)

        cells.append(
            '      <td align="center" valign="middle">'
            f'<img src="{safe_url}" alt="{safe_name}" '
            f'title="{safe_name}" width="{ICON_SIZE}" '
            f'height="{ICON_SIZE}" '
            'style="object-fit:contain;" /><br />'
            f"<sub>{safe_name}</sub>"
            "</td>"
        )

    if not cells:
        return '<p align="center">暂无可预览的图标。</p>'

    rows = []

    for index in range(0, len(cells), COLUMNS):
        row_cells = cells[index:index + COLUMNS]
        row_cells.extend(
            ["      <td></td>"] * (COLUMNS - len(row_cells))
        )

        rows.append(
            "    <tr>\n"
            + "\n".join(row_cells)
            + "\n    </tr>"
        )

    return (
        '<table align="center">\n'
        "  <tbody>\n"
        + "\n".join(rows)
        + "\n  </tbody>\n"
        "</table>"
    )


def main():
    data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    icons = data.get("icons", [])

    if not isinstance(icons, list):
        raise ValueError('"icons" must be a JSON array')

    readme = README_FILE.read_text(encoding="utf-8")

    if (
        readme.count(START_MARKER) != 1
        or readme.count(END_MARKER) != 1
    ):
        raise ValueError(
            "README.md must contain exactly one gallery start and end marker"
        )

    start = readme.index(START_MARKER) + len(START_MARKER)
    end = readme.index(END_MARKER)

    if start > end:
        raise ValueError("README.md gallery markers are in the wrong order")

    gallery = "\n\n" + build_gallery(icons) + "\n\n"

    updated = readme[:start] + gallery + readme[end:]

    if updated != readme:
        README_FILE.write_text(updated, encoding="utf-8")

    print(f"Updated README.md gallery: {len(icons)} icons")


if __name__ == "__main__":
    main()
