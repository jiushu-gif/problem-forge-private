"""Reference implementation shared by the data generator and the validator."""
MOD = 10 ** 9 + 7


def solve(n: int, edges: list[tuple[int, int, int]]) -> int:
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

    for a, b, c in edges:
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
