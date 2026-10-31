"""Render statement.pdf pages to images and verify required content is visible."""
import argparse
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--contest", default="2026 HHACM 招新赛")
parser.add_argument("--index", type=int, default=15)
args = parser.parse_args()
letter = chr(64 + args.index)

doc = fitz.open(ROOT / "statement.pdf")
text = "\n".join(page.get_text() for page in doc)
for needle in (
    args.contest,
    f"Problem {letter}. 恋人不行·世界线",
    "输入文件",
    "输出文件",
    "时间限制",
    "内存限制",
    "输入格式",
    "输出格式",
    "数据范围",
    "玲奈子",
    "世界线",
    "取模",
    "3 1",
    "1 2 1",
):
    assert needle in text, f"missing in statement: {needle}"
for i, page in enumerate(doc, start=1):
    preview = ROOT / f"statement-preview-{i}.png"
    page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(preview)
    print(preview)
print(f"pages: {doc.page_count}")
