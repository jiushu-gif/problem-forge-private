"""Build the Hydro import archive after the contest PID is confirmed."""
import argparse
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
PREFIX = "N"
TITLE = "久留美的 FX 账户"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pid", nargs="?", default="ZXS2026N", help="Hydro 题号，默认取已确认的 ZXS2026N")
args = parser.parse_args()
if not re.fullmatch(r'[^\s/\\:*?"<>|]+', args.pid):
    parser.error("invalid Hydro PID")

config = json.loads((ROOT / "problem.json").read_text(encoding="utf-8"))
pdf = ROOT / "statement.pdf"
if not pdf.is_file():
    raise SystemExit("缺少 statement.pdf：先运行 build_statement.py")

name = f"{PREFIX}-{TITLE}"
target = ROOT / "hydro" / name
(testdata := target / "testdata").mkdir(parents=True, exist_ok=True)
(target / "additional_file").mkdir(exist_ok=True)
(target / "problem.yaml").write_text(
    f"pid: {args.pid}\nowner: 1\ntitle: {TITLE}\ntag: []\nnSubmit: 0\nnAccept: 0\n",
    encoding="utf-8",
)
(target / "problem_zh.md").write_text("@[pdf](file://statement.pdf)\n", encoding="utf-8")
shutil.copy2(pdf, target / "additional_file" / "statement.pdf")

cases = []
for folder, prefix in ((ROOT / "data" / "samples", "sample"), (ROOT / "data" / "tests", "case")):
    for inp in sorted(folder.glob("*.in")):
        stem = f"{prefix}{inp.stem}"
        out = inp.with_suffix(".out")
        if not out.is_file():
            raise SystemExit(f"缺少答案文件：{out}")
        shutil.copy2(inp, testdata / f"{stem}.in")
        shutil.copy2(out, testdata / f"{stem}.ans")
        cases.append(stem)

lines = [
    "type: default",
    "checker_type: default",
    f"time: {config['time_limit_ms'] / 1000:g}s",
    f"memory: {config['memory_limit_mb']}m",
    "cases:",
]
for stem in cases:
    lines.append(f"  - input: {stem}.in")
    lines.append(f"    output: {stem}.ans")
(testdata / "config.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")

archive = ROOT / "hydro" / f"{name}.zip"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for path in sorted(target.rglob("*")):
        if path.is_file():
            z.write(path, Path(name) / path.relative_to(target))
print(archive)
