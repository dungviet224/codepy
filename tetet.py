from itertools import combinations
from bisect import bisect_left, bisect_right

n, M = map(int, input().split())
a = list(map(int, input().split()))

mid = n // 2
L = a[:mid]
R = a[mid:]

LS = []
for k in range(len(L) + 1):
    for c in combinations(range(len(L)), k):
        s = 0
        for i in c:
            s += L[i]
        if s <= M:
            LS.append((s, k))

RS = []
for k in range(len(R) + 1):
    for c in combinations(range(len(R)), k):
        s = 0
        for i in c:
            s += R[i]
        if s <= M:
            RS.append((s, k))

RS.sort()

vals = [x[0] for x in RS]

total_ways = 0
min_cows = 10**18

for sL, kL in LS:
    need = M - sL
    l = bisect_left(vals, need)
    r = bisect_right(vals, need)
    if l < r:
        total_ways += (r - l)
        for i in range(l, r):
            min_cows = min(min_cows, kL + RS[i][1])

print(total_ways, min_cows)
