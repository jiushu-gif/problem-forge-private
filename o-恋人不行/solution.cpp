#include <bits/stdc++.h>
const long long MOD = 1000000007LL;

struct DSU {
    std::vector<int> parent, parity;  // parity[x] = 与父亲的「异或关系」

    explicit DSU(int n) : parent(n + 1), parity(n + 1, 0) {
        std::iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        std::vector<int> path;
        int root = x;
        while (parent[root] != root) {
            path.push_back(root);
            root = parent[root];
        }
        int acc = 0;
        for (int i = static_cast<int>(path.size()) - 1; i >= 0; --i) {
            acc ^= parity[path[i]];
            parity[path[i]] = acc;
            parent[path[i]] = root;
        }
        return root;
    }

    // 要求 value(x) xor value(y) == diff，返回 false 表示矛盾。
    bool unite(int x, int y, int diff) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return (parity[x] ^ parity[y]) == diff;
        parent[rx] = ry;
        parity[rx] = parity[x] ^ parity[y] ^ diff;
        return true;
    }
};

long long power(long long base, long long exp) {
    long long result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n, m;
    if (!(std::cin >> n >> m)) return 0;
    DSU dsu(n);
    for (int i = 0; i < m; ++i) {
        int a, b, c;
        std::cin >> a >> b >> c;
        int diff = (c == 1 ? 0 : 1);  // 恋人是同一边，不可能在另一边
        if (!dsu.unite(a, b, diff)) {
            std::cout << 0 << '\n';
            return 0;
        }
    }
    int components = 0;
    for (int i = 1; i <= n; ++i)
        if (dsu.find(i) == i) ++components;
    std::cout << power(2, components - 1) << '\n';
    return 0;
}
