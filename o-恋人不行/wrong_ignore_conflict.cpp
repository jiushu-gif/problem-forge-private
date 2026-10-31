#include <bits/stdc++.h>
// Wrong: 完全不检查矛盾，把互相冲突的传闻也当成可以并起来的。
const long long MOD = 1000000007LL;

struct DSU {
    std::vector<int> parent;
    explicit DSU(int n) : parent(n + 1) { std::iota(parent.begin(), parent.end(), 0); }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
    void unite(int x, int y) {
        x = find(x);
        y = find(y);
        if (x != y) parent[x] = y;
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
        dsu.unite(a, b);
    }
    int components = 0;
    for (int i = 1; i <= n; ++i)
        if (dsu.find(i) == i) ++components;
    std::cout << power(2, components - 1) << '\n';
    return 0;
}
