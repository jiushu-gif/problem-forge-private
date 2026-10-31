"""Independent solution: sum of a[i] * b[i]."""
import sys

data = sys.stdin.read().split()
if data:
    n = int(data[0])
    a = [int(x) for x in data[1 : 1 + n]]
    b = [int(x) for x in data[1 + n : 1 + 2 * n]]
    print(sum(x * y for x, y in zip(a, b)))
