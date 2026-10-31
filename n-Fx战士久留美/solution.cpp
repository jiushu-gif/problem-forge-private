#include <bits/stdc++.h>
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<long long> a(n);
    for (auto& x : a) std::cin >> x;
    long long answer = 0;
    for (int i = 0; i < n; ++i) {
        long long b;
        std::cin >> b;
        answer += a[i] * b;
    }
    std::cout << answer << '\n';
    return 0;
}
