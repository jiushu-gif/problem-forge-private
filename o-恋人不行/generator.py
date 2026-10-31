"""Generate one test case for watanare-lovers: python generator.py <kind> <seed>."""
import random
import sys

MAX_N = 10 ** 5
MAX_M = 10 ** 5
KINDS = ("empty", "path", "star", "consistent", "any", "max")


def generate(kind: str, seed: int) -> tuple[int, list[tuple[int, int, int]]]:
    rng = random.Random(seed * 1000003 + KINDS.index(kind))
    if kind == "empty":
        return rng.randint(1, MAX_N), []
    if kind == "max":
        n = MAX_N
        color = [rng.randint(0, 1) for _ in range(n + 1)]
        edges = []
        for _ in range(MAX_M):
            a, b = rng.sample(range(1, n + 1), 2)
            edges.append((a, b, 1 if color[a] == color[b] else 0))
        return n, edges
    if kind == "path":
        n = rng.randint(2, 1000)
        return n, [(i, i + 1, rng.randint(0, 1)) for i in range(1, n)]
    if kind == "star":
        n = rng.randint(2, 1000)
        c = rng.randint(0, 1)
        return n, [(1, i, c) for i in range(2, n + 1)]
    if kind == "consistent":
        n = rng.randint(1, 2000)
        color = [rng.randint(0, 1) for _ in range(n + 1)]
        m = rng.randint(0, min(MAX_M, 4000))
        edges = []
        for _ in range(m):
            a, b = rng.sample(range(1, n + 1), 2)
            edges.append((a, b, 1 if color[a] == color[b] else 0))
        return n, edges
    n = rng.randint(2, 2000)
    m = rng.randint(1, min(MAX_M, 4000))
    edges = []
    for _ in range(m):
        a, b = rng.sample(range(1, n + 1), 2)
        edges.append((a, b, rng.randint(0, 1)))
    return n, edges


def main() -> int:
    kind = sys.argv[1] if len(sys.argv) > 1 else "any"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if kind not in KINDS:
        raise SystemExit(f"unknown kind: {kind}")
    n, edges = generate(kind, seed)
    out = [f"{n} {len(edges)}"]
    out.extend(f"{a} {b} {c}" for a, b, c in edges)
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
