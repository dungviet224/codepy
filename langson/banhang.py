n, S = map(int, input().split())
a =list(map(int, input().split()))

tong = 0
chon = []
for i in range(n - 1, -1, -1): 
    if tong + a[i] <= S:
        tong += a[i]
        chon.append(i + 1)
print(len(chon))
print(*chon[::-1])