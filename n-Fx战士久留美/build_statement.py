"""Render the approved statement with the contest header, run info and sample table.

Body text uses a small CJK-aware line breaker instead of reportlab Paragraph:
Chinese text must not start a line with closing punctuation, and Latin words or
numbers must never be split across lines. `_{i}` and `^{4}` render as sub/superscripts.
"""
import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
TITLE = "久留美的 FX 账户"
FONT = "SimHei"
BODY_SIZE = 11
LEADING = 18.5
NO_START = set("！？，。、；：）」』】》〉…—·")
NO_END = set("（「『【《〈+=")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--contest", default="比赛名称待确认", help="页眉里的比赛名称")
parser.add_argument("--index", type=int, default=8, help="比赛题序：A=1、B=2……")
args = parser.parse_args()
if not 1 <= args.index <= 26:
    parser.error("--index 必须是 1 到 26")
LETTER = chr(64 + args.index)

config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
assert config["time_limit_ms"] > 0 and config["memory_limit_mb"] > 0
pdfmetrics.registerFont(TTFont(FONT, r"C:\Windows\Fonts\simhei.ttf"))
c = canvas.Canvas(str(ROOT / "statement.pdf"), pagesize=A4)
width, height = A4
left, right = 58, 58
TEXT_WIDTH = width - left - right
y = height - 48

Char = tuple[str, int]
Unit = list[Char]


def char_width(ch: str, level: int) -> float:
    return pdfmetrics.stringWidth(ch, FONT, BODY_SIZE * 0.7 if level else BODY_SIZE)


def unit_width(unit: Unit) -> float:
    return sum(char_width(ch, level) for ch, level in unit)


def rich(text: str) -> Unit:
    """Parse `_{i}` / `^{4}` into characters with a script level."""
    chars: Unit = []
    i = 0
    while i < len(text):
        if text[i] in "_^" and i + 1 < len(text) and text[i + 1] == "{":
            end = text.index("}", i)
            level = 1 if text[i] == "^" else -1
            chars.extend((ch, level) for ch in text[i + 2 : end])
            i = end + 1
        else:
            chars.append((text[i], 0))
            i += 1
    return chars


def split_units(chars: Unit) -> list[Unit]:
    """Latin words and numbers stay whole; CJK characters are single units."""
    units: list[Unit] = []
    current: Unit = []
    for ch, level in chars:
        if ch.isascii() and not ch.isspace():
            current.append((ch, level))
            continue
        if current:
            units.append(current)
            current = []
        units.append([(ch, level)])
    if current:
        units.append(current)
    return units


def wrap(units: list[Unit], limit: float) -> list[list[Unit]]:
    lines: list[list[Unit]] = []
    current: list[Unit] = []

    def width(line: list[Unit]) -> float:
        return sum(unit_width(u) for u in line)

    for unit in units:
        if not current and unit[0][0].isspace():
            continue
        if not current or width(current) + unit_width(unit) <= limit:
            current.append(unit)
            continue
        trimmed = list(current)
        while len(trimmed) > 1 and trimmed[-1][0][0].isspace():
            trimmed.pop()
        previous = trimmed[-1]
        if len(unit) == 1 and len(previous) == 1 and unit[0][0] in NO_START and len(trimmed) > 1:
            trimmed.pop()
            lines.append(trimmed)
            current = [previous, unit]
        elif len(previous) == 1 and previous[0][0] in NO_END:
            trimmed.pop()
            lines.append(trimmed)
            current = [previous, unit]
        else:
            lines.append(trimmed)
            current = [unit]
    if current:
        lines.append(current)
    return lines


def paragraph(text: str, after: float = 6):
    global y
    for line in wrap(split_units(rich(text)), TEXT_WIDTH):
        x = left
        for unit in line:
            for ch, level in unit:
                c.setFont(FONT, BODY_SIZE * 0.7 if level else BODY_SIZE)
                c.drawString(x, y + (3.5 if level > 0 else (-2.5 if level < 0 else 0)), ch)
                x += char_width(ch, level)
        y -= LEADING
    y -= after


def heading(text, size=15, before=16, after=20):
    global y
    y -= before
    c.setFont(FONT, size)
    c.drawString(left, y, text)
    y -= after


def info_row(label, value):
    global y
    c.setFont(FONT, 10.5)
    c.drawString(left + 25, y, label)
    c.drawString(left + 108, y, value)
    y -= 17


def sample_table(number, input_lines, output_lines, note):
    global y
    heading(f"样例 {number}", before=16, after=20)
    top = y
    mid = left + TEXT_WIDTH / 2
    rows = max(len(input_lines), len(output_lines))
    table_h = 24 + rows * 16 + 10
    c.setStrokeColor(colors.HexColor("#555555"))
    c.rect(left, top - table_h, TEXT_WIDTH, table_h, fill=0, stroke=1)
    c.line(mid, top, mid, top - table_h)
    c.line(left, top - 24, width - right, top - 24)
    c.setFont(FONT, 10.5)
    c.drawCentredString((left + mid) / 2, top - 17, "标准输入")
    c.drawCentredString((mid + width - right) / 2, top - 17, "标准输出")
    c.setFont("Courier", 10)
    for i, line in enumerate(input_lines):
        c.drawString(left + 8, top - 40 - 16 * i, line)
    for i, line in enumerate(output_lines):
        c.drawString(mid + 8, top - 40 - 16 * i, line)
    y = top - table_h - 20
    paragraph(note, after=2)


c.setFont(FONT, 11)
c.drawCentredString(width / 2, y, args.contest)
y -= 17
c.setStrokeColor(colors.HexColor("#555555"))
c.line(left, y, width - right, y)
y -= 28
c.setFont(FONT, 19)
c.drawString(left, y, f"Problem {LETTER}. {TITLE}")
y -= 34
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 14
paragraph(
    "久留美是一位FX战士。这一天，她一口气开了 n 笔仓位："
    "第 i 笔仓位投入的本金是 a_{i}，她给这笔仓位加的杠杆是 b_{i} 倍。"
)
paragraph(
    "在久留美看来，一笔仓位最终能变成多少钱，就是本金乘上杠杆；"
    "整个账户的最终金额，则是这 n 笔仓位的金额之和："
    "a_{1}b_{1} + a_{2}b_{2} + … + a_{n}b_{n}。"
)
paragraph("请你帮久留美算一算，这个账户的最终金额是多少。")
paragraph("本金可能为负，表示这笔仓位目前处于浮亏；杠杆取正数表示做多，取负数表示做空，取 0 表示这笔仓位没有开。")
heading("输入格式")
paragraph("第一行是一个整数 n，1 ≤ n ≤ 1000。")
paragraph("第二行包含 n 个整数 a_{1}, a_{2}, …, a_{n}，依次表示每笔仓位的本金。")
paragraph("第三行包含 n 个整数 b_{1}, b_{2}, …, b_{n}，依次表示每笔仓位的杠杆。")
paragraph("相邻整数之间用单个空格隔开。")
heading("输出格式")
paragraph("输出一个整数，表示这个账户的最终金额。")
heading("数据范围")
paragraph("对于全部测试点，1 ≤ n ≤ 1000，且对于 1 ≤ i ≤ n，|a_{i}| ≤ 1000，|b_{i}| ≤ 1000。")
sample_table(
    1,
    ["3", "1 4 6", "2 1 5"],
    ["36"],
    "第 1 笔仓位 1 × 2 = 2，第 2 笔仓位 4 × 1 = 4，第 3 笔仓位 6 × 5 = 30，合计 2 + 4 + 30 = 36。",
)
assert y > 40, f"题面超出一页：y={y}"
c.showPage()
c.save()
print(ROOT / "statement.pdf")
