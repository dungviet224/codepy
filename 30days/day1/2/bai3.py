n,m = list(map(int,input().split()))
a = list(map(int,input().split()))
res = []
for i in range(n):
    for j in range(n):
        if a[j] < a[i] and a[j] + a[i] % m == 0:  
            res.append((a[i],a[j]))

print(res)