"""Validate vector-dot-product data, cross-check two accepted solutions and reject wrong solutions."""
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
BUILD.mkdir(exist_ok=True)
MAX_N = 1000
MAX_ABS = 1000


def build(source: str) -> Path:
    exe = BUILD / (Path(source).stem + ".exe")
    subprocess.run(
        ["g++", "-std=gnu++20", "-O2", "-Wall", "-Wextra", str(ROOT / source), "-o", str(exe)],
        check=True,
    )
    return exe


def run(exe: Path, raw: bytes) -> int:
    return int(subprocess.check_output([str(exe)], input=raw).strip())


def parse(raw: bytes) -> tuple[int, list[int], list[int]]:
    values = list(map(int, raw.split()))
    assert values, "空输入"
    n = values[0]
    assert 1 <= n <= MAX_N, f"n 越界：{n}"
    assert len(values) == 1 + 2 * n, f"期望 1+2n 个整数，实际 {len(values)}"
    a, b = values[1 : 1 + n], values[1 + n :]
    assert all(-MAX_ABS <= x <= MAX_ABS for x in a + b), "数值越界"
    return n, a, b


def expected(a: list[int], b: list[int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def check(raw: bytes) -> int:
    n, a, b = parse(raw)
    answer = expected(a, b)
    got = run(accepted_cpp, raw)
    assert got == answer, f"solution.cpp：n={n} 输出 {got}，应为 {answer}"
    got = int(subprocess.check_output([sys.executable, str(ROOT / "solution2.py")], input=raw).strip())
    assert got == answer, f"solution2.py：n={n} 输出 {got}，应为 {answer}"
    return answer


accepted_cpp = build("solution.cpp")
wrong_off_by_one = build("wrong_off_by_one.cpp")
wrong_reuse_a = build("wrong_reuse_a.cpp")

all_inputs: list[Path] = []
for directory in (ROOT / "data/samples", ROOT / "data/tests"):
    inputs = sorted(directory.glob("*.in"))
    assert inputs, f"{directory} 中没有测试数据"
    assert {p.stem for p in inputs} == {p.stem for p in directory.glob("*.out")}, f"{directory} 中 .in / .out 未成对"
    for inp in inputs:
        answer = int(inp.with_suffix(".out").read_text(encoding="utf-8").strip())
        oracle = check(inp.read_bytes())
        assert answer == oracle, f"{inp.name} 的答案文件 {answer} 与独立计算 {oracle} 不一致"
        all_inputs.append(inp)
    print(f"{directory.name}: {len(inputs)} 个用例通过")

statement = (ROOT / "statement.md").read_text(encoding="utf-8")
sample_in = (ROOT / "data/samples/01.in").read_text(encoding="utf-8").strip()
sample_out = (ROOT / "data/samples/01.out").read_text(encoding="utf-8").strip()
assert f"```text\n{sample_in}\n```" in statement, "题面样例输入与 data/samples/01.in 不一致"
assert f"```text\n{sample_out}\n```" in statement, "题面样例输出与 data/samples/01.out 不一致"
print("statement: 样例与 data/samples 一致")

rng = random.Random(20261031)
for _ in range(500):
    n = rng.randint(1, MAX_N)
    a = [rng.randint(-MAX_ABS, MAX_ABS) for _ in range(n)]
    b = [rng.randint(-MAX_ABS, MAX_ABS) for _ in range(n)]
    check(f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n".encode())
print("random: 500 个用例通过")

sys.path.insert(0, str(ROOT))
from generator import KINDS, generate, dot  # noqa: E402

for kind in KINDS:
    for seed in (1, 2, 3, 20261031):
        n, a, b = generate(kind, seed)
        assert 1 <= n <= MAX_N and len(a) == len(b) == n, f"generator {kind}/{seed} 结构错误"
        assert all(-MAX_ABS <= x <= MAX_ABS for x in a + b), f"generator {kind}/{seed} 越界"
        raw = f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n".encode()
        check(raw)
print(f"generator: {len(KINDS)} 种类型 × 4 个种子通过")

for name, exe in (("wrong_off_by_one", wrong_off_by_one), ("wrong_reuse_a", wrong_reuse_a)):
    rejected = []
    for inp in all_inputs:
        raw = inp.read_bytes()
        n, a, b = parse(raw)
        if run(exe, raw) != expected(a, b):
            rejected.append(inp.name)
    assert rejected, f"{name} 没有被任何用例拒绝"
    print(f"{name}: 被 {len(rejected)} 个用例拒绝（例如 {rejected[0]}）")
print("全部检查通过")
