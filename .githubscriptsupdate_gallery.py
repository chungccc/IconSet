
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_FILE = ROOT / "chungccicon.json"
README_FILE = ROOT / "README.md"

START = "<!-- ICON-GALLERY:START -->"
END = "<!-- ICON-GALLERY:END -->"

# 读取图标索引
data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
icons = data.get("icons", [])

# 生成缩略图表格，每行 4 个
rows = []

for i in range(0, len(icons), 4):
    cells = []

    for item in icons[i:i + 4]:
        name = html.escape(str(item["name"]))
        url = html.escape(str(item["url"]), quote=True)

        cells.append(
            f'<td align="center" valign="middle">'
            f'<img src="{url}" alt="{name}" width="64"><br>'
            f'<sub>{name}</sub></td>'
        )

    while len(cells) < 4:
        cells.append("<td></td>")

    rows.append("<tr>" + "".join(cells) + "</tr>")

gallery = (
    f"\n<table>\n"
    + "\n".join(rows)
    + "\n</table>\n"
)

# 仅替换 README 指定区域
readme = README_FILE.read_text(encoding="utf-8")

if START not in readme or END not in readme:
    raise RuntimeError("README 缺少图标预览标记，请先添加 START 和 END 标记。")

before, remainder = readme.split(START, 1)
_, after = remainder.split(END, 1)

updated = before + START + gallery + END + after

README_FILE.write_text(updated, encoding="utf-8")

print(f"图标缩略图更新完成：{len(icons)} 个")
