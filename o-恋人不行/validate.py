"""Validate watanare-lovers data, cross-check two accepted solutions and reject wrong solutions."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)
MAX_N = 10 ** 5
MAX_M = 10 ** 5

sys.path.insert(0, str(ROOT))
from reference import solve as reference_solve  # noqa: E402


def build(source: str) -> Path:
    exe = BUILD / (Path(source).stem + ".exe")
    subprocess.run(
        ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / source), "-o", str(exe)],
        check=True,
    )
    return exe


def run(exe: Path, raw: bytes) -> int:
    return int(subprocess.check_output([str(exe)], input=raw).strip())


def parse(raw: bytes) -> tuple[int, list[tuple[int, int, int]]]:
    values = list(map(int, raw.split()))
    assert len(values) >= 2, "输入为空"
    n, m = values[0], values[1]
    assert 1 <= n <= MAX_N and 0 <= m <= MAX_M, f"n / m 越界：{n} {m}"
    assert len(values) == 2 + 3 * m, f"行数与 m 不符：{len(values)} vs {2 + 3 * m}"
    edges = []
    for i in range(m):
        a, b, c = values[2 + 3 * i : 5 + 3 * i]
        assert 1 <= a <= n and 1 <= b <= n and a != b, f"端点非法：{a} {b}"
        assert c in (0, 1), f"c 非法：{c}"
        edges.append((a, b, c))
    return n, edges


def check(raw: bytes) -> int:
    n, edges = parse(raw)
    answer = reference_solve(n, edges)
    got = run(accepted_cpp, raw)
    assert got == answer, f"solution.cpp：n={n} m={len(edges)} 输出 {got}，应为 {answer}"
    py = int(subprocess.check_output([sys.executable, str(ROOT / "solution2.py")], input=raw).strip())
    assert py == answer, f"solution2.py：n={n} m={len(edges)} 输出 {py}，应为 {answer}"
    return answer


accepted_cpp = build("solution.cpp")
wrong_ignore_conflict = build("wrong_ignore_conflict.cpp")
wrong_exponent = build("wrong_exponent.cpp")

all_inputs: list[Path] = []
for directory in (ROOT / "data/samples", ROOT / "data/tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs, f"{directory} 中没有测试数据"
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}, f"{directory} 中 .in / .out 未成对"
    zeros = 0
    for inp in inputs:
        answer = int(inp.with_suffix(".out").read_text(encoding="utf-8").strip())
        oracle = check(inp.read_bytes())
        assert answer == oracle, f"{inp.name} 的答案文件 {answer} 与参考实现 {oracle} 不一致"
        zeros += oracle == 0
        all_inputs.append(inp)
    print(f"{directory.name}: {len(inputs)} 个用例通过（其中答案为 0 的 {zeros} 个）")

statement = (ROOT / "statement.md").read_text(encoding="utf-8")
for stem in ("01", "02"):
    sample_in = (ROOT / f"data/samples/{stem}.in").read_text(encoding="utf-8").strip()
    sample_out = (ROOT / f"data/samples/{stem}.out").read_text(encoding="utf-8").strip()
    assert f"```text\n{sample_in}\n```" in statement, f"题面样例 {stem} 输入与样例文件不一致"
    assert f"```text\n{sample_out}\n```" in statement, f"题面样例 {stem} 输出与样例文件不一致"
print("statement: 两个样例与 data/samples 一致")

import random  # noqa: E402

rng = random.Random(20261101)
for _ in range(300):
    n = rng.randint(2, 30)
    m = rng.randint(0, 60)
    edges = []
    for _ in range(m):
        a, b = rng.sample(range(1, n + 1), 2)
        edges.append((a, b, rng.randint(0, 1)))
    raw = (f"{n} {len(edges)}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in edges)).encode()
    check(raw)
print("random: 300 个用例通过")

from generator import KINDS, generate  # noqa: E402

for kind in KINDS:
    for seed in (1, 2, 20261101):
        n, edges = generate(kind, seed)
        raw = (f"{n} {len(edges)}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in edges)).encode()
        check(raw)
print(f"generator: {len(KINDS)} 种类型 × 3 个种子通过")

for name, exe in (("wrong_ignore_conflict", wrong_ignore_conflict), ("wrong_exponent", wrong_exponent)):
    rejected = []
    for inp in all_inputs:
        raw = inp.read_bytes()
        n, edges = parse(raw)
        if run(exe, raw) != reference_solve(n, edges):
            rejected.append(inp.name)
    assert rejected, f"{name} 没有被任何用例拒绝"
    print(f"{name}: 被 {len(rejected)} 个用例拒绝（例如 {rejected[0]}）")
print("全部检查通过")
