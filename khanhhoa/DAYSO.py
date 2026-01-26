n = int(input())
nlist = list(map(int, input().split()))

res = []
trc = 0
for i in range(n):
    soluong = i+1
    so_hientai = nlist[i] * soluong
    kq = so_hientai - trc
    res.append(kq)
    trc = so_hientai
print(res)