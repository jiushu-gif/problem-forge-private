#include <bits/stdc++.h>
// Wrong: 连通块 flip 后当成了不同的世界线，答案多乘了一个 2。
const long long MOD = 1000000007LL;

struct DSU {
    std::vector<int> parent, parity;
    explicit DSU(int n) : parent(n + 1), parity(n + 1, 0) { std::iota(parent.begin(), parent.end(), 0); }
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
        if (!dsu.unite(a, b, c == 1 ? 0 : 1)) {
            std::cout << 0 << '\n';
            return 0;
        }
    }
    int components = 0;
    for (int i = 1; i <= n; ++i)
        if (dsu.find(i) == i) ++components;
    std::cout << power(2, components) << '\n';
    return 0;
}
