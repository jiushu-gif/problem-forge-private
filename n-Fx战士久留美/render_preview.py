"""Render statement.pdf to an image and verify the required content is visible."""
import argparse
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--contest", default="2026 HHACM 招新赛")
parser.add_argument("--index", type=int, default=8)
args = parser.parse_args()
letter = chr(64 + args.index)

PDF = ROOT / "statement.pdf"
doc = fitz.open(PDF)
assert doc.page_count == 1, f"expected a single page, got {doc.page_count}"
page = doc[0]
text = page.get_text()
for needle in (
    args.contest,
    f"Problem {letter}. 久留美的 FX 账户",
    "输入文件",
    "输出文件",
    "时间限制",
    "内存限制",
    "输入格式",
    "输出格式",
    "数据范围",
    "久留美",
    "杠杆",
    "本金",
    "36",
    "1 4 6",
    "1000",
):
    assert needle in text, f"missing on page: {needle}"
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
preview = ROOT / "statement-preview.png"
pix.save(preview)
print(preview)
