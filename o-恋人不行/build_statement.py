"""Render the statement: contest header, run info, story, axioms and samples.

Body text uses a small CJK-aware line breaker; long statements flow onto a new
page automatically. `_{i}` / `^{4}` render as sub/superscripts.
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
TITLE = "恋人不行·世界线"
FONT = "SimHei"
BODY_SIZE = 10.5
LEADING = 18
NO_START = set("！？，。、；：）」』】》〉…—·")
NO_END = set("（「『【《〈+=")
BOTTOM = 70

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--contest", default="2026 HHACM 招新赛", help="页眉里的比赛名称")
parser.add_argument("--index", type=int, default=15, help="比赛题序：A=1、B=2……")
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
page = 1

Char = tuple[str, int]
Unit = list[Char]


def new_page():
    global y, page
    c.showPage()
    page += 1
    c.setFont(FONT, 9)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(width / 2, height - 40, f"{args.contest} · Problem {LETTER}. {TITLE}")
    c.drawRightString(width - right, height - 40, f"第 {page} 页")
    c.setStrokeColor(colors.HexColor("#999999"))
    c.line(left, height - 48, width - right, height - 48)
    c.setFillColor(colors.black)
    y = height - 70


def ensure(space: float):
    if y - space < BOTTOM:
        new_page()


def char_width(ch: str, level: int) -> float:
    return pdfmetrics.stringWidth(ch, FONT, BODY_SIZE * 0.7 if level else BODY_SIZE)


def unit_width(unit: Unit) -> float:
    return sum(char_width(ch, level) for ch, level in unit)


def rich(text: str) -> Unit:
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
        ensure(LEADING)
        x = left
        for unit in line:
            for ch, level in unit:
                c.setFont(FONT, BODY_SIZE * 0.7 if level else BODY_SIZE)
                c.drawString(x, y + (3 if level > 0 else (-2.2 if level < 0 else 0)), ch)
                x += char_width(ch, level)
        y -= LEADING
    y -= after


def heading(text, size=14, before=16, after=13):
    global y
    ensure(before + after + size + 6)
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
    note_lines = wrap(split_units(rich(note)), TEXT_WIDTH)
    rows = max(len(input_lines), len(output_lines))
    table_h = 24 + rows * 15 + 10
    ensure(16 + 13 + table_h + 14 + len(note_lines) * LEADING + 12)
    y -= 16
    c.setFont(FONT, 14)
    c.drawString(left, y, f"样例 {number}")
    y -= 13
    top = y
    mid = left + TEXT_WIDTH / 2
    c.setStrokeColor(colors.HexColor("#555555"))
    c.rect(left, top - table_h, TEXT_WIDTH, table_h, fill=0, stroke=1)
    c.line(mid, top, mid, top - table_h)
    c.line(left, top - 24, width - right, top - 24)
    c.setFont(FONT, 10)
    c.drawCentredString((left + mid) / 2, top - 17, "标准输入")
    c.drawCentredString((mid + width - right) / 2, top - 17, "标准输出")
    c.setFont("Courier", 9.5)
    for i, line in enumerate(input_lines):
        c.drawString(left + 8, top - 39 - 15 * i, line)
    for i, line in enumerate(output_lines):
        c.drawString(mid + 8, top - 39 - 15 * i, line)
    y = top - table_h - 14
    paragraph(note, after=4)


c.setFont(FONT, 11)
c.drawCentredString(width / 2, y, args.contest)
y -= 17
c.setStrokeColor(colors.HexColor("#555555"))
c.line(left, y, width - right, y)
y -= 26
c.setFont(FONT, 18)
c.drawString(left, y, f"Problem {LETTER}. {TITLE}")
y -= 30
info_row("输入文件:", "标准输入")
info_row("输出文件:", "标准输出")
info_row("时间限制:", f"{config['time_limit_ms'] / 1000:g} s")
info_row("内存限制:", f"{config['memory_limit_mb']} MB")
y -= 12
paragraph("玲奈子一直坚信一件事：她不可能成为谁的恋人，绝对不行。")
paragraph(
    "然而世界似乎并不打算放过她。某天早晨，她的手机收到一条来自「世界线观测局」的推送："
    "在这条世界线上，一共有 n 位少女，任意两位之间只有两种关系——"
    "要么是恋人，要么是「绝对不可能」。"
)
paragraph("更麻烦的是，这个世界还额外遵守两条八卦定律：")
paragraph(
    "1. 恋人的恋人也是恋人：如果 a 和 b 是恋人，b 和 c 也是恋人，那么 a 和 c 必定是恋人。"
)
paragraph(
    "2. 两条「不可能」会互相抵消：如果 a 和 b 不可能成为恋人，b 和 c 也不可能成为恋人，"
    "那么 a 和 c 反而会成为恋人。"
)
paragraph(
    "观测局已经记录下 m 条传闻，每条传闻形如「a 和 b 是恋人」或者「a 和 b 绝不可能在一起」。"
    "玲奈子想知道：有多少种不同的世界线，能让这 m 条传闻同时成立？"
)
paragraph(
    "两条世界线不同，当且仅当存在一对少女，她们在两条世界线里的关系不同。"
    "答案对 10^{9}+7 取模；如果这些传闻本身就自相矛盾，那么一条世界线都不存在，请输出 0。"
)
heading("输入格式")
paragraph("第一行包含两个整数 n 和 m，分别表示少女的人数和传闻的条数。")
paragraph(
    "接下来 m 行，每行包含三个整数 a, b, c（1 ≤ a, b ≤ n，a ≠ b，c ∈ {0,1}）："
    "c = 1 表示传闻说 a 和 b 是恋人；c = 0 表示传闻说 a 和 b 绝不可能在一起。"
)
paragraph("同一对少女可能被多次提及。")
heading("输出格式")
paragraph(
    "输出一行一个整数，表示满足全部传闻的世界线数量对 10^{9}+7 取模的结果；"
    "若传闻自相矛盾，输出 0。"
)
heading("数据范围")
paragraph("对于全部测试点，1 ≤ n ≤ 10^{5}，0 ≤ m ≤ 10^{5}，1 ≤ a, b ≤ n，a ≠ b，c ∈ {0,1}。")
sample_table(
    1,
    ["3 1", "1 2 1"],
    ["2"],
    "1 号和 2 号是恋人。3 号可以和他们站在同一边（三对关系全是恋人），"
    "也可以站到另一边（3 号与另外两人都「绝对不可能」），所以答案是 2。",
)
sample_table(
    2,
    ["3 3", "1 2 1", "2 3 1", "1 3 0"],
    ["0"],
    "前两条传闻要求 1、2、3 属于同一边，于是 1 号和 3 号必须是恋人；"
    "但第三条传闻说她们「绝不可能」，冲突，所以答案是 0。",
)
ensure(LEADING)
c.showPage()
c.save()
print(ROOT / "statement.pdf")
