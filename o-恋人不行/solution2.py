"""Independent solution: parity DSU, answer = 2^(components-1) mod 1e9+7."""
import sys

MOD = 10 ** 9 + 7


def solve(data: list[str]) -> int:
    n = int(data[0])
    m = int(data[1])
    parent = list(range(n + 1))
    parity = [0] * (n + 1)

    def find(x: int) -> int:
        path = []
        root = x
        while parent[root] != root:
            path.append(root)
            root = parent[root]
        acc = 0
        for node in reversed(path):
            acc ^= parity[node]
            parity[node] = acc
            parent[node] = root
        return root

    index = 2
    for _ in range(m):
        a, b, c = int(data[index]), int(data[index + 1]), int(data[index + 2])
        index += 3
        need = 0 if c == 1 else 1
        ra, rb = find(a), find(b)
        if ra == rb:
            if parity[a] ^ parity[b] != need:
                return 0
        else:
            parent[ra] = rb
            parity[ra] = parity[a] ^ parity[b] ^ need

    components = sum(1 for i in range(1, n + 1) if find(i) == i)
    return pow(2, components - 1, MOD)


if __name__ == "__main__":
    tokens = sys.stdin.read().split()
    if tokens:
        print(solve(tokens))
