"""Generate one test case for vector-dot-product: python generator.py <kind> <seed>."""
import random
import sys

MAX_N = 1000
MAX_ABS = 1000
KINDS = ("min", "max", "random", "small", "zeros", "edge")


def generate(kind: str, seed: int) -> tuple[int, list[int], list[int]]:
    rng = random.Random(seed * 1000003 + KINDS.index(kind))
    if kind == "min":
        n = 1
        return n, [rng.randint(-9, 9)], [rng.randint(-9, 9)]
    if kind == "max":
        return MAX_N, [MAX_ABS] * MAX_N, [MAX_ABS] * MAX_N
    if kind == "small":
        n = rng.randint(1, 5)
        return n, [rng.randint(-5, 5) for _ in range(n)], [rng.randint(-5, 5) for _ in range(n)]
    if kind == "zeros":
        n = rng.randint(1, MAX_N)
        return n, [0] * n, [rng.randint(-MAX_ABS, MAX_ABS) for _ in range(n)]
    if kind == "edge":
        # 极值：每一维都取 ±1000，让答案落在 ±10^9 附近。
        n = rng.choice((1, 2, 999, MAX_N))
        a = [rng.choice((-MAX_ABS, MAX_ABS)) for _ in range(n)]
        b = [rng.choice((-MAX_ABS, MAX_ABS)) for _ in range(n)]
        return n, a, b
    n = rng.randint(1, MAX_N)
    return n, [rng.randint(-MAX_ABS, MAX_ABS) for _ in range(n)], [
        rng.randint(-MAX_ABS, MAX_ABS) for _ in range(n)
    ]


def dot(a: list[int], b: list[int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def main() -> int:
    kind = sys.argv[1] if len(sys.argv) > 1 else "random"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if kind not in KINDS:
        raise SystemExit(f"unknown kind: {kind}")
    n, a, b = generate(kind, seed)
    print(n)
    print(" ".join(map(str, a)))
    print(" ".join(map(str, b)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
