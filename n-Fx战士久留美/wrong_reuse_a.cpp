#include <bits/stdc++.h>
// Wrong: 以为两个向量相同，读完 a 行后直接拿 a 当 b。
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<long long> a(n);
    for (auto& x : a) std::cin >> x;
    long long answer = 0;
    for (int i = 0; i < n; ++i) answer += a[i] * a[i];
    std::cout << answer << '\n';
    return 0;
}
